#!/usr/bin/env python3
"""
Integration test for Traceloop - Tests the full flow from Python SDK to Go server
"""

import traceloop
import requests
import time
import json

def test_server_health():
    """Test that the server is running and healthy."""
    print("🏥 Testing server health...")
    
    try:
        response = requests.get("http://localhost:8080/health", timeout=5)
        if response.status_code == 200:
            print("✅ Server is healthy")
            return True
        else:
            print(f"❌ Server health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Server connection failed: {e}")
        return False

def test_api_endpoints():
    """Test that all API endpoints are working."""
    print("\n🌐 Testing API endpoints...")
    
    endpoints = [
        ("/health", "Health check"),
        ("/api/v1/traces", "Get traces"),
        ("/api/v1/stats", "Get statistics")
    ]
    
    for endpoint, description in endpoints:
        try:
            response = requests.get(f"http://localhost:8080{endpoint}", timeout=5)
            if response.status_code == 200:
                print(f"✅ {description}: OK")
            else:
                print(f"❌ {description}: Failed ({response.status_code})")
                return False
        except Exception as e:
            print(f"❌ {description}: Error - {e}")
            return False
    
    return True

def test_trace_creation():
    """Test creating traces and sending them to the server."""
    print("\n📝 Testing trace creation...")
    
    # Initialize traceloop
    traceloop.init(
        endpoint="http://localhost:8080",
        service_name="integration-test"
    )
    
    # Create a simple trace
    @traceloop.trace("integration-test-function")
    def test_function(x, y):
        time.sleep(0.1)
        return x + y
    
    # Run the function
    result = test_function(5, 3)
    print(f"✅ Function executed: 5 + 3 = {result}")
    
    # Test manual trace creation
    trace = traceloop.start_trace("manual-integration-test")
    print(f"✅ Created manual trace: {trace.trace_id}")
    
    # Add some events
    traceloop.add_event(trace.trace_id, "test-event-1", data="hello")
    traceloop.add_event(trace.trace_id, "test-event-2", data="world")
    
    # End the trace
    traceloop.end_trace(trace.trace_id)
    print("✅ Manual trace completed")
    
    return True

def test_server_logs():
    """Test that we can see server logs (if any)."""
    print("\n📋 Checking server status...")
    
    try:
        # Get stats to see if server is processing anything
        response = requests.get("http://localhost:8080/api/v1/stats", timeout=5)
        if response.status_code == 200:
            stats = response.json()
            print(f"📊 Server stats: {json.dumps(stats, indent=2)}")
        else:
            print(f"❌ Failed to get stats: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error getting stats: {e}")
        return False
    
    return True

def main():
    """Run all integration tests."""
    print("🧪 Traceloop Integration Tests")
    print("=" * 50)
    
    # Test server health
    if not test_server_health():
        print("\n❌ Server health check failed. Make sure the server is running:")
        print("   cd /Users/shaileshpant/src/traceloop-ai/traceloop")
        print("   ./build/traceloop server --port 8080")
        return False
    
    # Test API endpoints
    if not test_api_endpoints():
        print("\n❌ API endpoint tests failed.")
        return False
    
    # Test trace creation
    if not test_trace_creation():
        print("\n❌ Trace creation tests failed.")
        return False
    
    # Test server logs
    if not test_server_logs():
        print("\n❌ Server log tests failed.")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 All integration tests passed!")
    print("\n💡 The traceloop system is working correctly:")
    print("   ✅ Go server is running and healthy")
    print("   ✅ Python SDK is working")
    print("   ✅ API endpoints are accessible")
    print("   ✅ Trace creation is functional")
    print("\n🌐 Dashboard: http://localhost:8080")
    print("📊 Stats: http://localhost:8080/api/v1/stats")
    print("🔍 Traces: http://localhost:8080/api/v1/traces")
    
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
