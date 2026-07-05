"""
ATP — the Agentic Training Platform data + store layer.

`atp.get_data()` returns the full `window.ATP_DATA` payload (seed, cached).
The store also exposes append-only HITL reward logging and the compose /
train-to-order request log.
"""

from .store import (
    get_data,
    append_hitl,
    read_hitl,
    append_request,
    read_requests,
)

__all__ = [
    "get_data",
    "append_hitl",
    "read_hitl",
    "append_request",
    "read_requests",
]
