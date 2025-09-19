"""
Type definitions for the Traceloop SDK.
"""

from enum import Enum
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass
from datetime import datetime
import uuid

class TraceStatus(Enum):
    """Status of a trace or span."""
    OK = "ok"
    ERROR = "error"
    TIMEOUT = "timeout"
    CANCELLED = "cancelled"

@dataclass
class Span:
    """Represents a span within a trace."""
    span_id: str
    trace_id: str
    parent_span_id: Optional[str]
    name: str
    start_time: datetime
    end_time: Optional[datetime]
    status: TraceStatus
    attributes: Dict[str, Any]
    events: List[Dict[str, Any]]
    
    def __post_init__(self):
        if not self.span_id:
            self.span_id = str(uuid.uuid4())
        if self.events is None:
            self.events = []
        if self.attributes is None:
            self.attributes = {}

@dataclass 
class Trace:
    """Represents a complete trace."""
    trace_id: str
    name: str
    start_time: datetime
    end_time: Optional[datetime]
    status: TraceStatus
    spans: List[Span]
    attributes: Dict[str, Any]
    service_name: Optional[str]
    
    def __post_init__(self):
        if not self.trace_id:
            self.trace_id = str(uuid.uuid4())
        if self.spans is None:
            self.spans = []
        if self.attributes is None:
            self.attributes = {}

@dataclass
class TraceEvent:
    """Represents an event within a trace/span."""
    name: str
    timestamp: datetime
    attributes: Dict[str, Any]
    
    def __post_init__(self):
        if self.attributes is None:
            self.attributes = {}

@dataclass
class TraceContext:
    """Context information for the current trace."""
    trace_id: str
    span_id: Optional[str]
    service_name: Optional[str]
    attributes: Dict[str, Any]
    
    def __post_init__(self):
        if self.attributes is None:
            self.attributes = {}

# Type aliases for common data structures
AttributeValue = Union[str, int, float, bool, None]
Attributes = Dict[str, AttributeValue]
SpanKind = str  # Can be extended to enum later

# Common attribute keys following OpenTelemetry conventions
class AttributeKeys:
    """Standard attribute keys for traces and spans."""
    
    # Service attributes
    SERVICE_NAME = "service.name"
    SERVICE_VERSION = "service.version"
    
    # Agent attributes  
    AGENT_NAME = "agent.name"
    AGENT_TYPE = "agent.type"
    AGENT_VERSION = "agent.version"
    
    # LLM attributes
    LLM_MODEL = "llm.model"
    LLM_PROVIDER = "llm.provider"
    LLM_PROMPT_TOKENS = "llm.prompt_tokens"
    LLM_COMPLETION_TOKENS = "llm.completion_tokens"
    LLM_TOTAL_TOKENS = "llm.total_tokens"
    LLM_TEMPERATURE = "llm.temperature"
    LLM_MAX_TOKENS = "llm.max_tokens"
    
    # Function attributes
    FUNCTION_NAME = "function.name"
    FUNCTION_MODULE = "function.module"
    FUNCTION_DURATION = "function.duration_ms"
    
    # Error attributes
    ERROR_TYPE = "error.type"
    ERROR_MESSAGE = "error.message"
    ERROR_STACK = "error.stack"
    
    # Component attributes
    COMPONENT_TYPE = "component.type"  # "agent", "llm", "tool", "retriever", etc.
    COMPONENT_NAME = "component.name"

# Common span names
class SpanNames:
    """Standard span names for different components."""
    
    AGENT_EXECUTION = "agent.execute"
    LLM_CALL = "llm.call"
    TOOL_EXECUTION = "tool.execute"
    RETRIEVAL = "retrieval.search"
    MEMORY_READ = "memory.read"
    MEMORY_WRITE = "memory.write"
