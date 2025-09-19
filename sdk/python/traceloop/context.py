"""
Context management for traces and spans.
"""

import threading
from typing import Optional
from .types import TraceContext

# Thread-local storage for trace context
_context = threading.local()

def get_current_trace() -> Optional[TraceContext]:
    """Get the current trace context from thread-local storage."""
    return getattr(_context, 'current_trace', None)

def set_current_trace(trace_context: TraceContext):
    """Set the current trace context in thread-local storage."""
    _context.current_trace = trace_context

def create_span_context(name: str, trace_id: str) -> str:
    """Create a new span context."""
    import uuid
    span_id = str(uuid.uuid4())
    
    # Store span context in thread-local storage
    if not hasattr(_context, 'spans'):
        _context.spans = {}
    
    _context.spans[span_id] = {
        'name': name,
        'trace_id': trace_id,
        'span_id': span_id
    }
    
    return span_id

def get_span_context(span_id: str) -> Optional[dict]:
    """Get span context by ID."""
    if not hasattr(_context, 'spans'):
        return None
    return _context.spans.get(span_id)

def set_trace_attribute(key: str, value):
    """Set an attribute on the current trace."""
    trace = get_current_trace()
    if trace:
        trace.attributes[key] = value

def clear_context():
    """Clear the current trace context."""
    if hasattr(_context, 'current_trace'):
        delattr(_context, 'current_trace')
    if hasattr(_context, 'spans'):
        delattr(_context, 'spans')
