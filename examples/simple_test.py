#!/usr/bin/env python3
"""
Simple Traceloop Example - No External Dependencies

This example demonstrates basic traceloop functionality without requiring
external AI libraries like OpenAI or LangChain.
"""

import traceloop
import time
import random

# Initialize traceloop
traceloop.init(
    endpoint="http://localhost:8080",
    service_name="simple-example"
)

@traceloop.trace_agent("math-agent")
def math_agent(operation: str, a: float, b: float) -> float:
    """A simple math agent that performs basic operations."""
    time.sleep(0.1)  # Simulate processing time
    
    if operation == "add":
        return a + b
    elif operation == "subtract":
        return a - b
    elif operation == "multiply":
        return a * b
    elif operation == "divide":
        if b != 0:
            return a / b
        else:
            raise ValueError("Cannot divide by zero")
    else:
        raise ValueError(f"Unknown operation: {operation}")

@traceloop.trace_llm("mock-llm", capture_prompts=True)
def mock_llm_call(prompt: str, temperature: float = 0.7) -> str:
    """Mock LLM call for demonstration purposes."""
    time.sleep(0.2)  # Simulate API call delay
    
    # Simple mock responses based on prompt keywords
    if "weather" in prompt.lower():
        return "The weather is sunny and 72°F"
    elif "joke" in prompt.lower():
        return "Why don't scientists trust atoms? Because they make up everything!"
    elif "help" in prompt.lower():
        return "I'm here to help! What would you like to know?"
    else:
        return f"I received your message: '{prompt}'. How can I assist you?"

@traceloop.trace("data-processing")
def process_data(data: list) -> dict:
    """Process a list of data and return statistics."""
    time.sleep(0.15)  # Simulate processing time
    
    if not data:
        return {"count": 0, "sum": 0, "average": 0}
    
    return {
        "count": len(data),
        "sum": sum(data),
        "average": sum(data) / len(data),
        "min": min(data),
        "max": max(data)
    }

def main():
    """Main function demonstrating traceloop usage."""
    print("🚀 Traceloop Simple Example")
    print("=" * 40)
    
    # Test math agent
    print("\n🧮 Testing Math Agent:")
    try:
        result = math_agent("add", 10, 5)
        print(f"  10 + 5 = {result}")
        
        result = math_agent("multiply", 7, 8)
        print(f"  7 × 8 = {result}")
        
        result = math_agent("divide", 20, 4)
        print(f"  20 ÷ 4 = {result}")
        
    except Exception as e:
        print(f"  Math agent error: {e}")
    
    # Test mock LLM
    print("\n🤖 Testing Mock LLM:")
    prompts = [
        "What's the weather like?",
        "Tell me a joke",
        "I need help with my code",
        "How do I learn Python?"
    ]
    
    for prompt in prompts:
        try:
            response = mock_llm_call(prompt, temperature=0.8)
            print(f"  Q: {prompt}")
            print(f"  A: {response}")
        except Exception as e:
            print(f"  LLM error: {e}")
    
    # Test data processing
    print("\n📊 Testing Data Processing:")
    test_data = [random.randint(1, 100) for _ in range(10)]
    print(f"  Input data: {test_data}")
    
    try:
        stats = process_data(test_data)
        print(f"  Statistics: {stats}")
    except Exception as e:
        print(f"  Processing error: {e}")
    
    # Test manual tracing
    print("\n🔧 Testing Manual Tracing:")
    try:
        trace = traceloop.start_trace("manual-workflow")
        print(f"  Started trace: {trace.trace_id}")
        
        # Simulate some work
        time.sleep(0.1)
        
        # Add events
        traceloop.add_event(trace.trace_id, "step-1", action="initialization")
        traceloop.add_event(trace.trace_id, "step-2", action="processing")
        traceloop.add_event(trace.trace_id, "step-3", action="completion")
        
        # End trace
        traceloop.end_trace(trace.trace_id)
        print("  ✅ Manual trace completed")
        
    except Exception as e:
        print(f"  Manual tracing error: {e}")
    
    print("\n" + "=" * 40)
    print("🎉 Example completed successfully!")
    print("\n💡 Check the traceloop dashboard at: http://localhost:8080")
    print("   You should see all the traces from this example.")

if __name__ == "__main__":
    main()
