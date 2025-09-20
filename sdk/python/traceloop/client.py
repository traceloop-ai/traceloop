"""
Traceloop client for sending traces to the server.
"""

import uuid
from typing import Any, Dict, Optional

import requests

from .types import Trace, TraceContext, TraceStatus


class TraceloopClient:
    """Client for sending traces to the Traceloop server."""

    def __init__(
        self,
        endpoint: str = "http://localhost:8080",
        api_key: Optional[str] = None,
        service_name: Optional[str] = None,
        **kwargs,
    ):
        self.endpoint = endpoint.rstrip("/")
        self.api_key = api_key
        self.service_name = service_name or "unknown-service"
        self.session = requests.Session()

        # Set up headers
        if self.api_key:
            self.session.headers.update({"Authorization": f"Bearer {self.api_key}"})

        self.session.headers.update(
            {
                "Content-Type": "application/json",
                "User-Agent": "traceloop-python-sdk/0.1.0",
            }
        )

    def start_trace(self, name: str, **attributes) -> TraceContext:
        """Start a new trace."""
        trace_id = str(uuid.uuid4())

        trace_context = TraceContext(
            trace_id=trace_id,
            span_id=str(uuid.uuid4()),
            service_name=self.service_name,
            attributes={
                "trace.name": name,
                "service.name": self.service_name,
                **attributes,
            },
        )

        # For now, just return the context
        # In a real implementation, this would send to the server
        return trace_context

    def end_trace(self, trace_id: str, status: TraceStatus = TraceStatus.OK):
        """End a trace."""
        # For now, just log
        print(f"Ending trace {trace_id} with status {status.value}")
        return True

    def add_event(self, trace_id: str, name: str, **attributes):
        """Add an event to a trace."""
        # For now, just log
        print(f"Adding event '{name}' to trace {trace_id}")
        return True

    def update_span(
        self,
        span_id: str,
        attributes: Dict[str, Any],
        status: TraceStatus = TraceStatus.OK,
    ):
        """Update a span with attributes and status."""
        # For now, just log
        print(f"Updating span {span_id} with {len(attributes)} attributes")
        return True

    def send_trace(self, trace: Trace) -> bool:
        """Send a trace to the server."""
        try:
            # Convert trace to dict for JSON serialization
            trace_data = {
                "trace_id": trace.trace_id,
                "name": trace.name,
                "start_time": trace.start_time.isoformat(),
                "end_time": trace.end_time.isoformat() if trace.end_time else None,
                "status": trace.status.value,
                "spans": [
                    {
                        "span_id": span.span_id,
                        "trace_id": span.trace_id,
                        "parent_span_id": span.parent_span_id,
                        "name": span.name,
                        "start_time": span.start_time.isoformat(),
                        "end_time": (
                            span.end_time.isoformat() if span.end_time else None
                        ),
                        "status": span.status.value,
                        "attributes": span.attributes,
                        "events": span.events,
                    }
                    for span in trace.spans
                ],
                "attributes": trace.attributes,
                "service_name": trace.service_name,
            }

            response = self.session.post(
                f"{self.endpoint}/api/v1/traces", json=trace_data, timeout=5
            )

            if response.status_code == 200:
                return True
            else:
                print(f"Failed to send trace: {response.status_code} - {response.text}")
                return False

        except Exception as e:
            print(f"Error sending trace: {e}")
            return False
