#!/usr/bin/env python3
"""
Simple OpenAI Chat Example with Traceloop

This example demonstrates how to use Traceloop with OpenAI's chat completions
to automatically trace LLM calls, including prompts, responses, and metadata.
"""

import os
import traceloop
import openai

# Initialize Traceloop
traceloop.init(
    endpoint="http://localhost:8080",
    service_name="openai-chat-example"
)

# Set up OpenAI client
openai.api_key = os.getenv("OPENAI_API_KEY")

@traceloop.trace_llm("gpt-4", capture_prompts=True, capture_responses=True)
def chat_with_ai(message: str, model: str = "gpt-4") -> str:
    """Chat with OpenAI's GPT model."""
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": message}
            ],
            temperature=0.7,
            max_tokens=150
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        # Traceloop will automatically capture this error
        raise Exception(f"OpenAI API error: {str(e)}")

@traceloop.trace_agent("conversation-agent")
def conversation_agent(user_input: str) -> str:
    """A simple conversation agent that uses multiple LLM calls."""
    
    # First, understand the user's intent
    intent_prompt = f"Analyze this user input and determine the intent: {user_input}"
    intent = chat_with_ai(intent_prompt, model="gpt-3.5-turbo")
    
    # Then, generate an appropriate response
    response_prompt = f"Based on this intent '{intent}', respond to: {user_input}"
    response = chat_with_ai(response_prompt, model="gpt-4")
    
    return response

if __name__ == "__main__":
    # Example conversation
    user_message = "I'm feeling stressed about work. Can you help me with some advice?"
    
    try:
        response = conversation_agent(user_message)
        print(f"User: {user_message}")
        print(f"Agent: {response}")
        
    except Exception as e:
        print(f"Error: {e}")
    
    # The traces will be available in the Traceloop dashboard
    # Visit http://localhost:8080 to view the traces
