#!/usr/bin/env python3
"""
Basic LangChain Agent Example with Traceloop

This example demonstrates how to use Traceloop with a simple LangChain agent
to automatically trace agent execution, tool usage, and LLM calls.
"""

import os
import traceloop
from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder

# Initialize Traceloop
traceloop.init(
    endpoint="http://localhost:8080",
    service_name="langchain-agent-example"
)

# Define a simple tool
@tool
def get_weather(location: str) -> str:
    """Get the current weather for a location."""
    # Simulate weather API call
    return f"The weather in {location} is sunny and 72°F"

# Create the LLM
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.7,
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

# Define the prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant that can check the weather."),
    ("user", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

# Create the agent
tools = [get_weather]
agent = create_openai_functions_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Example usage
if __name__ == "__main__":
    # This will be automatically traced by Traceloop
    result = agent_executor.invoke({
        "input": "What's the weather like in San Francisco?"
    })
    
    print(f"Agent response: {result['output']}")
    
    # The trace will be available in the Traceloop dashboard
    # Visit http://localhost:8080 to view the trace
