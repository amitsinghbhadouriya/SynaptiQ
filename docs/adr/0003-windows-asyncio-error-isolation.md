# ADR 0003: Windows Asyncio Proactor Error Isolation Strategy

## Status
Accepted

## Context
On Windows, abrupt client disconnects raise `ConnectionResetError: [WinError 10054]` in `_call_connection_lost`.

## Decision
Monkey-patch `_ProactorBasePipeTransport._call_connection_lost` to safely swallow disconnect resets during shutdown.
