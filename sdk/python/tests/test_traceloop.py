import pytest
import traceloop
from traceloop.client import TraceloopClient
from traceloop.types import Trace, Span, TraceStatus
from datetime import datetime


def test_traceloop_init():
    """Test traceloop initialization"""
    client = traceloop.init(endpoint="http://localhost:8080")
    assert isinstance(client, TraceloopClient)
    assert client.endpoint == "http://localhost:8080"


def test_trace_creation():
    """Test trace creation"""
    now = datetime.now()
    trace = Trace(
        trace_id="test-trace-1",
        name="test-trace",
        start_time=now,
        end_time=None,
        status=TraceStatus.OK,
        spans=[],
        attributes={},
        service_name="test-service"
    )
    
    assert trace.trace_id == "test-trace-1"
    assert trace.name == "test-trace"
    assert trace.service_name == "test-service"
    assert trace.status == TraceStatus.OK


def test_span_creation():
    """Test span creation"""
    now = datetime.now()
    span = Span(
        span_id="test-span-1",
        trace_id="test-trace-1",
        parent_span_id=None,
        name="test-span",
        start_time=now,
        end_time=None,
        status=TraceStatus.OK,
        attributes={},
        events=[]
    )
    
    assert span.span_id == "test-span-1"
    assert span.trace_id == "test-trace-1"
    assert span.name == "test-span"
    assert span.status == TraceStatus.OK


def test_trace_with_spans():
    """Test trace with spans"""
    now = datetime.now()
    trace = Trace(
        trace_id="test-trace-2",
        name="test-trace-with-spans",
        start_time=now,
        end_time=None,
        status=TraceStatus.OK,
        spans=[],
        attributes={},
        service_name="test-service"
    )
    
    span1 = Span(
        span_id="span-1",
        trace_id="test-trace-2",
        parent_span_id=None,
        name="span-1",
        start_time=now,
        end_time=None,
        status=TraceStatus.OK,
        attributes={},
        events=[]
    )
    
    span2 = Span(
        span_id="span-2",
        trace_id="test-trace-2",
        parent_span_id=None,
        name="span-2",
        start_time=now,
        end_time=None,
        status=TraceStatus.OK,
        attributes={},
        events=[]
    )
    
    trace.spans = [span1, span2]
    
    assert len(trace.spans) == 2
    assert trace.spans[0].name == "span-1"
    assert trace.spans[1].name == "span-2"


def test_client_creation():
    """Test client creation with custom settings"""
    client = TraceloopClient(
        endpoint="http://localhost:8080",
        api_key="test-key",
        service_name="test-service"
    )
    
    assert client.endpoint == "http://localhost:8080"
    assert client.api_key == "test-key"
    assert client.service_name == "test-service"


if __name__ == "__main__":
    pytest.main([__file__])
