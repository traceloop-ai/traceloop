"""
Traceloop - Production observability for AI agents

This package provides comprehensive observability and monitoring capabilities
for AI agents and language model applications.
"""

__version__ = "0.1.0"
__author__ = "Shailesh Pant"
__email__ = "shailesh@traceloop-ai.dev"

from typing import Optional

from .client import TraceloopClient
from .context import get_current_trace, set_trace_attribute
from .decorators import trace, trace_agent, trace_llm
from .types import Span, Trace, TraceStatus

# Main client instance
_default_client = None


def init(
    endpoint: str = "http://localhost:8080",
    api_key: Optional[str] = None,
    service_name: Optional[str] = None,
    **kwargs
) -> TraceloopClient:
    """
    Initialize the global Traceloop client.

    Args:
        endpoint: The traceloop server endpoint
        api_key: API key for authentication (optional for local development)
        service_name: Name of the service being traced
        **kwargs: Additional configuration options

    Returns:
        TraceloopClient: The initialized client instance
    """
    global _default_client
    _default_client = TraceloopClient(
        endpoint=endpoint, api_key=api_key, service_name=service_name, **kwargs
    )
    return _default_client


def get_client() -> TraceloopClient:
    """Get the default client instance."""
    if _default_client is None:
        raise RuntimeError("Traceloop not initialized. Call traceloop.init() first.")
    return _default_client


# Convenience functions that use the default client
def start_trace(name: str, **attributes):
    """Start a new trace using the default client."""
    return get_client().start_trace(name, **attributes)


def end_trace(trace_id: str, status: TraceStatus = TraceStatus.OK):
    """End a trace using the default client."""
    return get_client().end_trace(trace_id, status)


def add_event(trace_id: str, name: str, **attributes):
    """Add an event to a trace using the default client."""
    return get_client().add_event(trace_id, name, **attributes)


# Export all public symbols
__all__ = [
    "__version__",
    "init",
    "get_client",
    "start_trace",
    "end_trace",
    "add_event",
    "trace",
    "trace_agent",
    "trace_llm",
    "get_current_trace",
    "set_trace_attribute",
    "TraceloopClient",
    "Trace",
    "Span",
    "TraceStatus",
]
