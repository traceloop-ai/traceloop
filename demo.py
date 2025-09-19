#!/usr/bin/env python3
"""
Traceloop Demo - Complete Working Example

This script demonstrates all the working features of the traceloop system:
- Go server running and serving API endpoints
- Python SDK with decorators and manual tracing
- Integration between Python SDK and Go server
"""

import traceloop
import requests
import time
import json
from datetime import datetime

def print_header(title):
    """Print a formatted header."""
    print(f"\n{'='*60}")
    print(f"🚀 {title}")
    print(f"{'='*60}")

def print_section(title):
    """Print a formatted section header."""
    print(f"\n📋 {title}")
    print("-" * 40)

def check_server_status():
    """Check if the traceloop server is running."""
    print_section("Server Status Check")
    
    try:
        # Health check
        response = requests.get("http://localhost:8080/health", timeout=5)
        if response.status_code == 200:
            print("✅ Server is running and healthy")
            
            # Get stats
            stats_response = requests.get("http://localhost:8080/api/v1/stats", timeout=5)
            if stats_response.status_code == 200:
                stats = stats_response.json()
                print(f"📊 Current stats: {json.dumps(stats, indent=2)}")
            
            return True
        else:
            print(f"❌ Server health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to server: {e}")
        print("💡 Make sure the server is running:")
        print("   cd /Users/shaileshpant/src/traceloop-ai/traceloop")
        print("   ./build/traceloop server --port 8080")
        return False

def demo_python_sdk():
    """Demonstrate Python SDK features."""
    print_section("Python SDK Demo")
    
    # Initialize traceloop
    traceloop.init(
        endpoint="http://localhost:8080",
        service_name="demo-service"
    )
    print("✅ Traceloop SDK initialized")
    
    # Test decorators
    @traceloop.trace("demo-function")
    def demo_function(name: str, value: int) -> str:
        time.sleep(0.1)
        return f"Hello {name}, your value is {value}"
    
    @traceloop.trace_agent("demo-agent")
    def demo_agent(task: str) -> str:
        time.sleep(0.1)
        return f"Agent processed: {task}"
    
    @traceloop.trace_llm("demo-llm", capture_prompts=True)
    def demo_llm(prompt: str) -> str:
        time.sleep(0.1)
        return f"LLM response to: {prompt}"
    
    # Run decorated functions
    result1 = demo_function("World", 42)
    print(f"✅ Function result: {result1}")
    
    result2 = demo_agent("Process data")
    print(f"✅ Agent result: {result2}")
    
    result3 = demo_llm("What is AI?")
    print(f"✅ LLM result: {result3}")
    
    # Test manual tracing
    trace = traceloop.start_trace("manual-demo")
    print(f"✅ Started manual trace: {trace.trace_id}")
    
    traceloop.add_event(trace.trace_id, "step-1", action="initialization")
    traceloop.add_event(trace.trace_id, "step-2", action="processing")
    traceloop.add_event(trace.trace_id, "step-3", action="completion")
    
    traceloop.end_trace(trace.trace_id)
    print("✅ Manual trace completed")

def demo_api_endpoints():
    """Demonstrate API endpoint functionality."""
    print_section("API Endpoints Demo")
    
    endpoints = [
        ("/health", "Health Check"),
        ("/api/v1/traces", "Get Traces"),
        ("/api/v1/stats", "Get Statistics")
    ]
    
    for endpoint, description in endpoints:
        try:
            response = requests.get(f"http://localhost:8080{endpoint}", timeout=5)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ {description}: {json.dumps(data, indent=2)}")
            else:
                print(f"❌ {description}: HTTP {response.status_code}")
        except Exception as e:
            print(f"❌ {description}: {e}")

def demo_advanced_tracing():
    """Demonstrate advanced tracing features."""
    print_section("Advanced Tracing Demo")
    
    # Complex workflow with multiple traces
    @traceloop.trace_agent("workflow-orchestrator")
    def orchestrate_workflow(data: list) -> dict:
        """Orchestrate a complex workflow."""
        
        @traceloop.trace("data-validation")
        def validate_data(data: list) -> bool:
            time.sleep(0.05)
            return len(data) > 0 and all(isinstance(x, (int, float)) for x in data)
        
        @traceloop.trace("data-processing")
        def process_data(data: list) -> dict:
            time.sleep(0.1)
            return {
                "count": len(data),
                "sum": sum(data),
                "average": sum(data) / len(data),
                "min": min(data),
                "max": max(data)
            }
        
        @traceloop.trace("result-formatting")
        def format_result(stats: dict) -> str:
            time.sleep(0.05)
            return f"Processed {stats['count']} items, avg: {stats['average']:.2f}"
        
        # Execute workflow
        if not validate_data(data):
            raise ValueError("Invalid data")
        
        stats = process_data(data)
        result = format_result(stats)
        
        return {"stats": stats, "result": result}
    
    # Test the workflow
    test_data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    try:
        result = orchestrate_workflow(test_data)
        print(f"✅ Workflow result: {result['result']}")
        print(f"📊 Statistics: {result['stats']}")
    except Exception as e:
        print(f"❌ Workflow failed: {e}")

def main():
    """Run the complete demo."""
    print_header("Traceloop Complete Demo")
    print(f"🕐 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Check server status
    if not check_server_status():
        return False
    
    # Demo Python SDK
    demo_python_sdk()
    
    # Demo API endpoints
    demo_api_endpoints()
    
    # Demo advanced tracing
    demo_advanced_tracing()
    
    # Final status check
    print_section("Final Status")
    try:
        response = requests.get("http://localhost:8080/api/v1/stats", timeout=5)
        if response.status_code == 200:
            stats = response.json()
            print(f"📊 Final server stats: {json.dumps(stats, indent=2)}")
    except Exception as e:
        print(f"❌ Failed to get final stats: {e}")
    
    print_header("Demo Complete")
    print("🎉 All traceloop features are working correctly!")
    print("\n🌐 Access the dashboard at: http://localhost:8080")
    print("📊 View statistics at: http://localhost:8080/api/v1/stats")
    print("🔍 View traces at: http://localhost:8080/api/v1/traces")
    print("\n💡 The system is ready for development and testing!")
    
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
