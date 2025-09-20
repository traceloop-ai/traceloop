# Traceloop AI

**Local-first observability platform for AI agents. Monitor, debug, and improve your LLM applications with confidence.**

[![CI](https://github.com/traceloop-ai/traceloop/workflows/CI/badge.svg)](https://github.com/traceloop-ai/traceloop/actions)
[![Go Report Card](https://goreportcard.com/badge/github.com/traceloop-ai/traceloop)](https://goreportcard.com/report/github.com/traceloop-ai/traceloop)
[![Coverage](https://codecov.io/gh/traceloop-ai/traceloop/branch/main/graph/badge.svg)](https://codecov.io/gh/traceloop-ai/traceloop)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

Traceloop provides comprehensive observability and monitoring for AI agents, offering trace collection, visualization, and performance analytics for production AI systems. Built with privacy and control in mind - your data never leaves your machine.

**🌐 Official Domains:** [traceloop-ai.dev](https://traceloop-ai.dev) | [traceloop-ai.io](https://traceloop-ai.io) | [traceloop-ai.ai](https://traceloop-ai.ai)

## 🚀 Features

- **🔍 Complete Trace Visibility** - See every LLM call, tool use, and decision
- **💻 Local-First** - Your data never leaves your machine
- **🚀 Production Ready** - From local development to cloud deployment  
- **🔧 Framework Agnostic** - Works with LangChain, CrewAI, raw OpenAI, and more
- **📊 Real-time Dashboard** - Beautiful web interface for trace visualization
- **⚡ High Performance** - Minimal overhead with efficient data collection
- **🎯 Agent-specific Insights** - Purpose-built for AI agent observability

## 💻 Why Local-First?

**Privacy & Control**: Your AI traces, prompts, and responses stay on your machine. No data sent to external services.

**Performance**: Zero network latency for trace collection and analysis.

**Compliance**: Meet strict data governance requirements with complete data sovereignty.

**Offline Ready**: Work without internet connection - perfect for sensitive environments.

## 📦 Quick Start

**Get started with Traceloop in under 2 minutes - everything runs locally on your machine.**

### Server Installation

**Using Go:**
```bash
go install github.com/traceloop-ai/traceloop/cmd/traceloop@latest
traceloop server
```

**Using Docker:**
```bash
# Using published image (after first release)
docker run -p 8080:8080 ghcr.io/traceloop-ai/traceloop:latest

# Or build from source
git clone https://github.com/traceloop-ai/traceloop.git
cd traceloop
docker build -f docker/Dockerfile -t traceloop .
docker run -p 8080:8080 traceloop
```

**Using Homebrew:**
```bash
brew install traceloop-ai/tap/traceloop
traceloop server
```

### Python SDK

```bash
pip install traceloop
```

```python
import traceloop

# Initialize traceloop
traceloop.init(
    endpoint="http://localhost:8080",
    service_name="my-ai-agent"
)

# Automatic tracing with decorators
@traceloop.trace_agent("my-agent")
def my_agent_function(user_input: str) -> str:
    # Your agent logic here
    response = call_llm(user_input)
    return response

@traceloop.trace_llm("gpt-4")
def call_llm(prompt: str) -> str:
    # LLM call logic
    return "AI response"
```

## 🏗️ Local-First Architecture

**Everything runs on your machine - no external dependencies or data transmission.**

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Python SDK    │    │   TypeScript    │    │   Other SDKs    │
│                 │    │      SDK        │    │                 │
└─────────┬───────┘    └─────────┬───────┘    └─────────┬───────┘
          │                      │                      │
          └──────────────┬───────────────────────────────┘
                         │ gRPC/HTTP (localhost)
                         ▼
          ┌─────────────────────────────────┐
          │     Traceloop Server (Local)    │
          │  ┌─────────────┬─────────────┐ │
          │  │ Trace API   │   Web UI    │ │
          │  └─────────────┴─────────────┘ │
          │  ┌─────────────────────────────┐ │
          │  │   Local Storage (BadgerDB)  │ │
          │  └─────────────────────────────┘ │
          └─────────────────────────────────┘
```

**🔒 Data Sovereignty**: All traces, prompts, and responses stored locally on your machine.

## 🎯 Use Cases

**Works with any AI framework - LangChain, CrewAI, raw OpenAI, Anthropic, and more.**

### AI Agent Debugging
```python
@traceloop.trace_agent("research-agent")
def research_agent(query: str):
    # Automatically trace the entire agent execution
    search_results = web_search(query)
    summary = summarize_results(search_results)
    return generate_response(summary)
```

### LLM Performance Monitoring
```python
@traceloop.trace_llm("gpt-4", capture_prompts=True)
def generate_response(context: str):
    response = openai_client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": context}]
    )
    return response.choices[0].message.content
```

### Multi-Agent Coordination
```python
# Trace complex multi-agent workflows
with traceloop.start_trace("multi-agent-task") as trace:
    agent1_result = planning_agent.execute(task)
    agent2_result = execution_agent.execute(agent1_result)
    final_result = review_agent.execute(agent2_result)
```

## 📊 Dashboard Features

- **Trace Timeline**: Visualize agent execution flows
- **Performance Metrics**: Response times, token usage, error rates
- **Search & Filter**: Find specific traces by agent, time, or attributes
- **Real-time Monitoring**: Live view of running agents
- **Error Analysis**: Detailed error tracking and debugging

## 🔧 Configuration

### Server Configuration

```bash
# Basic server start
traceloop server --port 8080 --host 0.0.0.0

# With custom storage
traceloop server --storage-path ./traceloop-data

# Production configuration
traceloop server \
  --port 8080 \
  --storage-path /var/lib/traceloop \
  --log-level info \
  --metrics-enabled
```

### Python SDK Configuration

```python
import traceloop

# Development setup
traceloop.init(
    endpoint="http://localhost:8080",
    service_name="my-service",
    capture_args=True,
    capture_results=True
)

# Production setup
traceloop.init(
    endpoint="https://traceloop.your-domain.com",
    api_key="your-api-key",
    service_name="production-agent",
    sampling_rate=0.1,  # Sample 10% of traces
    batch_size=100
)
```

## 🚀 Development

### Prerequisites

- Go 1.21+
- Python 3.8+
- Node.js 18+ (for web dashboard)
- Make

### Building from Source

```bash
# Clone the repository
git clone https://github.com/traceloop-ai/traceloop.git
cd traceloop

# Initialize dependencies
make init

# Run tests
make test

# Build the binary
make build

# Run locally
make dev
```

### Project Structure

```
traceloop/
├── cmd/traceloop/          # CLI entry point
├── server/                 # Server implementation
│   ├── grpc/              # gRPC service for SDKs
│   ├── http/              # REST API & web server
│   └── storage/           # Data storage layer
├── sdk/
│   ├── python/            # Python SDK
│   ├── typescript/        # TypeScript SDK
│   └── proto/             # Protocol buffer definitions
├── web/dashboard/         # React dashboard
├── examples/              # Usage examples
└── docs/                  # Documentation
```

## 🧪 Examples

### LangChain Integration

```python
import traceloop
from langchain.agents import create_openai_functions_agent

# Initialize traceloop
traceloop.init(service_name="langchain-agent")

# Your existing LangChain code works unchanged
# Traceloop automatically instruments LangChain components
agent = create_openai_functions_agent(llm, tools, prompt)
result = agent.invoke({"input": "What's the weather like?"})
```

### OpenAI Integration

```python
import traceloop
import openai

traceloop.init(service_name="openai-app")

# Automatic instrumentation for OpenAI calls
@traceloop.trace
def chat_with_ai(message: str):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": message}]
    )
    return response.choices[0].message.content
```

### CrewAI Integration

```python
import traceloop
from crewai import Agent, Task, Crew

traceloop.init(service_name="crewai-workflow")

# Define agents with automatic tracing
researcher = Agent(
    role='Researcher',
    goal='Find relevant information',
    backstory='Expert researcher'
)

# Crew execution is automatically traced
crew = Crew(agents=[researcher], tasks=[task])
result = crew.kickoff()
```

## 📚 Documentation

- [Installation Guide](docs/installation.md)
- [Python SDK Reference](docs/python-sdk.md)
- [Server Configuration](docs/server-config.md)
- [Dashboard Guide](docs/dashboard.md)
- [API Reference](docs/api.md)

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Workflow

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes and add tests
4. Run the test suite: `make test`
5. Commit your changes: `git commit -m 'Add amazing feature'`
6. Push to your fork: `git push origin feature/amazing-feature`
7. Open a Pull Request

## 📝 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- 🌐 **Website:** [traceloop-ai.dev](https://traceloop-ai.dev) | [traceloop-ai.io](https://traceloop-ai.io) | [traceloop-ai.ai](https://traceloop-ai.ai)
- 📖 [Documentation](https://docs.traceloop-ai.dev)
- 💬 [Discord Community](https://discord.gg/traceloop)
- 🐛 [GitHub Issues](https://github.com/traceloop-ai/traceloop/issues)
- 📧 [Email Support](mailto:support@traceloop-ai.dev)

## 🌟 Roadmap

- [ ] **Multi-tenant support** - Enterprise-ready isolation
- [ ] **Advanced analytics** - ML-powered insights
- [ ] **Custom dashboards** - Build your own views
- [ ] **Alerting & notifications** - Proactive monitoring
- [ ] **More SDK languages** - Java, Rust, and more
- [ ] **Cloud deployment** - Managed service offering

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=traceloop-ai/traceloop&type=Date)](https://star-history.com/#traceloop-ai/traceloop&Date)

---

Built with ❤️ for the AI community
