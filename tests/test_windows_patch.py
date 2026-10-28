"""Unit tests for Windows asyncio WinError 10054 handling."""

import asyncio
import sys
from unittest.mock import MagicMock

from backend.windows_patch import _silence_connection_reset, patch_windows_asyncio


def test_patch_windows_asyncio_idempotent():
    # Calling it multiple times should never raise
    patch_windows_asyncio()
    patch_windows_asyncio()


def test_patched_proactor_transport_handles_reset():
    if sys.platform != "win32":
        return

    import asyncio.proactor_events

    transport_cls = asyncio.proactor_events._ProactorBasePipeTransport
    patch_windows_asyncio()

    # Create a mock transport instance
    transport = object.__new__(transport_cls)
    mock_protocol = MagicMock()
    mock_sock = MagicMock()
    # Mock shutdown to raise WinError 10054 ConnectionResetError
    err = ConnectionResetError(10054, "An existing connection was forcibly closed by the remote host")
    err.winerror = 10054
    mock_sock.shutdown.side_effect = err
    mock_sock.fileno.return_value = 42

    mock_server = MagicMock()

    transport._protocol = mock_protocol
    transport._sock = mock_sock
    transport._server = mock_server
    transport._called_connection_lost = False

    # Calling _call_connection_lost should NOT raise ConnectionResetError
    transport._call_connection_lost(None)

    # Verify protocol was notified
    mock_protocol.connection_lost.assert_called_once_with(None)
    # Verify socket close was attempted
    mock_sock.close.assert_called_once()
    # Verify server detached
    mock_server._detach.assert_called_once_with(transport)
    # Verify called flag set
    assert transport._called_connection_lost is True
    assert transport._sock is None


def test_silence_connection_reset_handler():
    loop = MagicMock()

    # Should silence WinError 10054
    exc_10054 = ConnectionResetError(10054, "Forcibly closed")
    exc_10054.winerror = 10054
    _silence_connection_reset(loop, {"exception": exc_10054})
    loop.default_exception_handler.assert_not_called()

    # Should silence callback message
    _silence_connection_reset(loop, {"message": "Exception in callback _ProactorBasePipeTransport._call_connection_lost()"})
    loop.default_exception_handler.assert_not_called()

    # Other exceptions should pass to default handler
    runtime_err = RuntimeError("Real error")
    context = {"exception": runtime_err, "message": "Something broke"}
    _silence_connection_reset(loop, context)
    loop.default_exception_handler.assert_called_once_with(context)
