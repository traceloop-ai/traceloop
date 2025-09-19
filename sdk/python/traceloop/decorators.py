"""
Decorators for automatic tracing of functions and methods.
"""

import functools
import inspect
import time
from typing import Any, Callable, Dict, Optional, TypeVar, Union
from .types import TraceStatus
from .context import get_current_trace, create_span_context

F = TypeVar('F', bound=Callable[..., Any])

def trace(
    name: Optional[str] = None,
    capture_args: bool = True,
    capture_result: bool = True,
    ignore_errors: bool = False,
    **span_attributes
) -> Callable[[F], F]:
    """
    Decorator to automatically trace function execution.
    
    Args:
        name: Custom name for the trace/span. Defaults to function name.
        capture_args: Whether to capture function arguments as span attributes
        capture_result: Whether to capture function return value as span attribute
        ignore_errors: Whether to continue tracing even if function raises exception
        **span_attributes: Additional attributes to add to the span
    
    Returns:
        Decorated function that will be automatically traced
    """
    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Determine span name
            span_name = name or f"{func.__module__}.{func.__qualname__}"
            
            # Get or create trace context
            trace_context = get_current_trace()
            if trace_context is None:
                from . import get_client
                client = get_client()
                trace_context = client.start_trace(span_name)
            
            # Create span
            span_id = create_span_context(span_name, trace_context.trace_id)
            
            # Capture function metadata
            attributes = {
                "function.name": func.__name__,
                "function.module": func.__module__,
                "function.qualname": func.__qualname__,
                **span_attributes
            }
            
            # Capture arguments if requested
            if capture_args:
                sig = inspect.signature(func)
                bound_args = sig.bind(*args, **kwargs)
                bound_args.apply_defaults()
                
                for param_name, param_value in bound_args.arguments.items():
                    # Only capture serializable argument values
                    if isinstance(param_value, (str, int, float, bool, type(None))):
                        attributes[f"function.args.{param_name}"] = param_value
                    else:
                        attributes[f"function.args.{param_name}.type"] = type(param_value).__name__
            
            start_time = time.time()
            status = TraceStatus.OK
            error_msg = None
            result = None
            
            try:
                result = func(*args, **kwargs)
                
                # Capture result if requested
                if capture_result and result is not None:
                    if isinstance(result, (str, int, float, bool)):
                        attributes["function.result"] = result
                    else:
                        attributes["function.result.type"] = type(result).__name__
                
                return result
                
            except Exception as e:
                status = TraceStatus.ERROR
                error_msg = str(e)
                attributes["error.type"] = type(e).__name__
                attributes["error.message"] = error_msg
                
                if not ignore_errors:
                    raise
                
            finally:
                end_time = time.time()
                attributes["function.duration_ms"] = (end_time - start_time) * 1000
                
                # Update span with final attributes
                from . import get_client
                client = get_client()
                client.update_span(span_id, attributes, status)
                
        return wrapper
    return decorator

def trace_agent(
    agent_name: Optional[str] = None,
    capture_inputs: bool = True,
    capture_outputs: bool = True,
    **attributes
) -> Callable[[F], F]:
    """
    Decorator specifically for tracing AI agent execution.
    
    Args:
        agent_name: Custom name for the agent. Defaults to function name.
        capture_inputs: Whether to capture agent inputs
        capture_outputs: Whether to capture agent outputs
        **attributes: Additional agent-specific attributes
    
    Returns:
        Decorated function optimized for agent tracing
    """
    def decorator(func: F) -> F:
        agent_attrs = {
            "component.type": "agent",
            "agent.name": agent_name or func.__name__,
            **attributes
        }
        
        return trace(
            name=f"agent.{agent_name or func.__name__}",
            capture_args=capture_inputs,
            capture_result=capture_outputs,
            **agent_attrs
        )(func)
    
    return decorator

def trace_llm(
    model_name: Optional[str] = None,
    capture_prompts: bool = True,
    capture_responses: bool = True,
    **attributes
) -> Callable[[F], F]:
    """
    Decorator specifically for tracing LLM calls.
    
    Args:
        model_name: Name of the LLM model being used
        capture_prompts: Whether to capture LLM prompts
        capture_responses: Whether to capture LLM responses
        **attributes: Additional LLM-specific attributes
        
    Returns:
        Decorated function optimized for LLM call tracing
    """
    def decorator(func: F) -> F:
        llm_attrs = {
            "component.type": "llm",
            "llm.model": model_name,
            **attributes
        }
        
        return trace(
            name=f"llm.{model_name or func.__name__}",
            capture_args=capture_prompts,
            capture_result=capture_responses,
            **llm_attrs
        )(func)
    
    return decorator
