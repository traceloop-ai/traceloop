#!/usr/bin/env python3
"""
Test script to verify Python SDK functionality
"""

import sys
import os
import time
import requests
from datetime import datetime

# Add the SDK to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'sdk', 'python'))

try:
    import traceloop
    from traceloop.types import Trace, Span, TraceStatus
    print("✅ Traceloop SDK imported successfully")
except ImportError as e:
    print(f"❌ Failed to import traceloop: {e}")
    sys.exit(1)

def test_basic_functionality():
    """Test basic SDK functionality"""
    print("\n🧪 Testing basic functionality...")
    
    # Test client initialization
    try:
        client = traceloop.init(endpoint="http://localhost:8080")
        print("✅ Client initialized successfully")
    except Exception as e:
        print(f"❌ Client initialization failed: {e}")
        return False
    
    # Test trace creation
    try:
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
        print("✅ Trace creation works")
    except Exception as e:
        print(f"❌ Trace creation failed: {e}")
        return False
    
    # Test span creation
    try:
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
        print("✅ Span creation works")
    except Exception as e:
        print(f"❌ Span creation failed: {e}")
        return False
    
    return True

def test_server_connection():
    """Test connection to Traceloop server"""
    print("\n🌐 Testing server connection...")
    
    try:
        response = requests.get("http://localhost:8080/health", timeout=5)
        if response.status_code == 200:
            print("✅ Server is running and responding")
            return True
        else:
            print(f"❌ Server returned status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to server: {e}")
        print("💡 Make sure to start the server with: ./build/traceloop server")
        return False

def main():
    """Main test function"""
    print("🚀 Traceloop Python SDK Test")
    print("=" * 40)
    
    # Test server connection first
    if not test_server_connection():
        print("\n❌ Server connection failed. Please start the server first.")
        return False
    
    # Test basic functionality
    if not test_basic_functionality():
        print("\n❌ Basic functionality tests failed.")
        return False
    
    print("\n✅ All tests passed! Python SDK is working correctly.")
    print("\n📝 To use the SDK in your code:")
    print("   import traceloop")
    print("   traceloop.init(endpoint='http://localhost:8080')")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)