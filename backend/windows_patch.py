"""Windows asyncio compatibility patch.

Silences harmless `ConnectionResetError: [WinError 10054]` exceptions on Windows.

Why this happens:
    Python's asyncio on Windows uses `ProactorEventLoop` by default. When a web client
    (browser tab, iframe, Vite dev proxy, or WebSocket) abruptly disconnects, refreshes,
    or navigates away, the remote host terminates the TCP socket. During disconnection
    cleanup in `asyncio.proactor_events._ProactorBasePipeTransport._call_connection_lost()`,
    Python invokes `self._sock.shutdown(socket.SHUT_RDWR)`. Since the remote connection was
    already severed, Windows raises `[WinError 10054] An existing connection was forcibly
    closed by the remote host`.

    Because standard library `proactor_events.py` does not catch this error during socket
    shutdown, it bubbles up to the event loop callback runner, producing noisy tracebacks.

This patch:
    1. Wraps `_ProactorBasePipeTransport._call_connection_lost()` to safely swallow
       `ConnectionResetError` and related Winsock teardown errors during shutdown,
       ensuring the underlying socket is still properly closed and cleaned up.
    2. Installs an asyncio exception handler to suppress any unhandled WinError 10054/10053
       noise across running event loops (FastAPI / Uvicorn / Tornado / Streamlit).
"""

from __future__ import annotations

import logging
import socket
import sys

log = logging.getLogger("synaptiq.windows_patch")

_CLASS_PATCHED = False


def _patch_proactor_transport() -> None:
    """Monkey-patch asyncio's Windows Proactor transport to ignore shutdown reset errors."""
    global _CLASS_PATCHED
    if _CLASS_PATCHED:
        return

    try:
        import asyncio.proactor_events

        transport_cls = asyncio.proactor_events._ProactorBasePipeTransport
        if getattr(transport_cls, "_synaptiq_patched", False):
            _CLASS_PATCHED = True
            return

        def _safe_call_connection_lost(self, exc):
            if getattr(self, "_called_connection_lost", False):
                return
            try:
                protocol = getattr(self, "_protocol", None)
                if protocol is not None:
                    protocol.connection_lost(exc)
            finally:
                # On Windows, calling shutdown() on a socket that the remote
                # end already forcibly closed raises WinError 10054. We catch
                # it and proceed to close the socket safely.
                sock = getattr(self, "_sock", None)
                if sock is not None:
                    if hasattr(sock, "shutdown") and getattr(sock, "fileno", lambda: -1)() != -1:
                        try:
                            sock.shutdown(socket.SHUT_RDWR)
                        except (ConnectionResetError, OSError):
                            pass
                    try:
                        sock.close()
                    except Exception:
                        pass
                    self._sock = None

                server = getattr(self, "_server", None)
                if server is not None:
                    try:
                        server._detach(self)
                    except Exception:
                        pass
                    self._server = None

                self._called_connection_lost = True

        transport_cls._call_connection_lost = _safe_call_connection_lost
        transport_cls._synaptiq_patched = True
        _CLASS_PATCHED = True
        log.debug("Applied Windows ProactorBasePipeTransport._call_connection_lost patch.")
    except Exception as exc:
        log.debug("Could not patch _ProactorBasePipeTransport: %s", exc)


def _silence_connection_reset(loop, context):
    exc = context.get("exception")
    winerror = getattr(exc, "winerror", None)

    # 10054: WSAECONNRESET (forcibly closed by remote host)
    # 10053: WSAECONNABORTED (software caused connection abort)
    # 10038: WSAENOTSOCK (operation on non-socket)
    if isinstance(exc, ConnectionResetError) or winerror in (10054, 10053, 10038):
        return

    msg = context.get("message") or ""
    if "_call_connection_lost" in msg or "WinError 10054" in msg:
        return

    loop.default_exception_handler(context)


def _attach_loop_handlers() -> None:
    """Attach the suppression exception handler to active event loops."""
    try:
        import asyncio

        try:
            loop = asyncio.get_running_loop()
            loop.set_exception_handler(_silence_connection_reset)
        except RuntimeError:
            pass

        if "tornado.ioloop" in sys.modules:
            try:
                import tornado.ioloop
                tloop = tornado.ioloop.IOLoop.current().asyncio_loop
                tloop.set_exception_handler(_silence_connection_reset)
            except Exception:
                pass
    except Exception as exc:
        log.debug("Could not configure asyncio exception handler: %s", exc)


def patch_windows_asyncio() -> None:
    """Apply the Windows Proactor connection-lost error suppression patch."""
    if sys.platform != "win32":
        return

    _patch_proactor_transport()
    _attach_loop_handlers()
