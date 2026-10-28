# ADR 0002: Sliding Window Rate Limiting and Token Blacklisting

## Status
Accepted

## Context
Fixed-window rate limiters suffer from burst edge traffic doubling quotas at boundary transitions.

## Decision
Implement a rolling double-ended queue sliding window enforcing a strict 30 req/min limit per client.
