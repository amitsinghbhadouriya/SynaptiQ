"""Unit tests for W3C trace context."""

from backend.trace_context import generate_trace_id, parse_traceparent


def test_trace_context():
    tid = generate_trace_id()
    assert len(tid) == 32

    valid = f"00-{tid}-1234567890abcdef-01"
    parsed = parse_traceparent(valid)
    assert parsed is not None
    assert parsed[0] == tid
