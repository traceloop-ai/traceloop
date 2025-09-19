#!/usr/bin/env python3
"""
Test script for the Traceloop Python SDK
"""

import traceloop
import time
import requests

def test_basic_tracing():
    """Test basic tracing functionality"""
    print("🧪 Testing basic tracing...")
    
    # Initialize traceloop
    traceloop.init(
        endpoint="http://localhost:8080",
        service_name="test-service"
    )
    
    # Test decorator
    @traceloop.trace("test-function")
    def test_function(x, y):
        time.sleep(0.1)  # Simulate some work
        return x + y
    
    # Test agent decorator
    @traceloop.trace_agent("test-agent")
    def test_agent(input_text):
        time.sleep(0.1)
        return f"Processed: {input_text}"
    
    # Test LLM decorator
    @traceloop.trace_llm("gpt-4", capture_prompts=True)
    def test_llm_call(prompt):
        time.sleep(0.1)
        return f"AI Response to: {prompt}"
    
    # Run the tests
    result1 = test_function(5, 3)
    print(f"✅ test_function result: {result1}")
    
    result2 = test_agent("Hello World")
    print(f"✅ test_agent result: {result2}")
    
    result3 = test_llm_call("What is AI?")
    print(f"✅ test_llm_call result: {result3}")
    
    print("✅ Basic tracing tests completed!")

def test_server_connection():
    """Test connection to the traceloop server"""
    print("\n🌐 Testing server connection...")
    
    try:
        # Test health endpoint
        response = requests.get("http://localhost:8080/health", timeout=5)
        if response.status_code == 200:
            print("✅ Server health check passed")
        else:
            print(f"❌ Server health check failed: {response.status_code}")
            return False
            
        # Test API endpoints
        response = requests.get("http://localhost:8080/api/v1/traces", timeout=5)
        if response.status_code == 200:
            print("✅ Traces API accessible")
        else:
            print(f"❌ Traces API failed: {response.status_code}")
            return False
            
        response = requests.get("http://localhost:8080/api/v1/stats", timeout=5)
        if response.status_code == 200:
            print("✅ Stats API accessible")
            print(f"📊 Server stats: {response.json()}")
        else:
            print(f"❌ Stats API failed: {response.status_code}")
            return False
            
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Server connection failed: {e}")
        return False

def test_manual_tracing():
    """Test manual tracing without decorators"""
    print("\n🔧 Testing manual tracing...")
    
    try:
        # Start a trace manually
        trace = traceloop.start_trace("manual-test")
        print(f"✅ Started trace: {trace.trace_id}")
        
        # Add an event
        traceloop.add_event(trace.trace_id, "test-event", test_data="hello")
        print("✅ Added event to trace")
        
        # End the trace
        traceloop.end_trace(trace.trace_id)
        print("✅ Ended trace")
        
        return True
        
    except Exception as e:
        print(f"❌ Manual tracing failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting Traceloop Python SDK Tests")
    print("=" * 50)
    
    # Test server connection first
    if not test_server_connection():
        print("\n❌ Server connection failed. Make sure the traceloop server is running.")
        print("   Run: ./build/traceloop server --port 8080")
        exit(1)
    
    # Test basic tracing
    test_basic_tracing()
    
    # Test manual tracing
    test_manual_tracing()
    
    print("\n" + "=" * 50)
    print("🎉 All tests completed successfully!")
    print("\n💡 Check the traceloop dashboard at: http://localhost:8080")
    print("   You should see traces from this test run.")
