<p align="center">
  <img src="https://raw.githubusercontent.com/getbindu/create-bindu-agent/refs/heads/main/assets/light.svg" alt="bindu Logo" width="200">
</p>

<h1 align="center">article-explainer-agent</h1>

<p align="center">
  <strong>AI-powered multi-specialist article analysis agent</strong>
</p>

<p align="center">
  <a href="https://github.com/Paraschamoli/article-explainer-agent/actions/workflows/main.yml?query=branch%3Amain">
    <img src="https://img.shields.io/github/actions/workflow/status/Paraschamoli/article-explainer-agent/main.yml?branch=main" alt="Build status">
  </a>
  <a href="https://img.shields.io/github/license/Paraschamoli/article-explainer-agent">
    <img src="https://img.shields.io/github/license/Paraschamoli/article-explainer-agent" alt="License">
  </a>
  <a href="https://img.shields.io/badge/Python-3.12+-blue.svg">
    <img src="https://img.shields.io/badge/Python-3.12+-blue.svg" alt="Python 3.12+">
  </a>
</p>

---

## 📖 Overview

**article-explainer-agent** is an advanced AI agent that provides comprehensive article analysis through the collaboration of five specialist experts. Built on the [Bindu Agent Framework](https://github.com/getbindu/bindu), it delivers multi-perspective insights on any article or technical content.

### 🚀 Key Features

- **👥 Multi-Specialist Team**: 5 AI experts working concurrently
  - **Developer**: Technical implementation details, code examples, APIs
  - **Summarizer**: Concise summaries and key takeaways
  - **Explainer**: Step-by-step conceptual breakdowns
  - **Analogy Creator**: Real-world analogies and metaphors
  - **Vulnerability Expert**: Security analysis and risk assessment

- **⚡ Concurrent Processing**: All specialists analyze simultaneously for faster results
- **🎯 Comprehensive Analysis**: Technical, conceptual, practical, and security perspectives
- **� Production Ready**: Built-in error handling, type safety, and comprehensive testing
- **🌐 API-First**: RESTful API with OpenRouter integration

---

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) package manager
- OpenRouter API key (free tier available)

### Installation

```bash
# Clone the repository
git clone https://github.com/Paraschamoli/article-explainer-agent.git
cd article-explainer-agent

# Install dependencies
uv sync

# Install pre-commit hooks
uv run pre-commit install

# Configure environment
cp .env.example .env
```

### Configuration

Edit `.env` and add your API key:

```bash
OPENROUTER_API_KEY=your_openrouter_api_key_here
MODEL_NAME=gpt-4o  # Optional: defaults to gpt-4o
```

Get your free API key from [OpenRouter](https://openrouter.ai/keys).

### Run the Agent

```bash
# Start the agent
uv run python -m article_explainer_agent

# Agent will be available at http://localhost:3773
```

### Github Setup

```bash
# Initialize git repository and commit your code
git init -b main
git add .
git commit -m "Initial commit"

# Create repository on GitHub and push (replace with your GitHub username)
gh repo create Paraschamoli/article-explainer-agent --public --source=. --remote=origin --push
```

---

## 💡 Usage Examples

### Example Queries

```bash
# Technical article analysis
"Explain the concept of 'Microservices Architecture in Modern Cloud Systems' using multiple perspectives including developer analysis, summarization, conceptual explanation, analogy creation, and security assessment."

# Research paper breakdown
"Analyze this research paper about 'How Retrieval-Augmented Generation (RAG) improves the accuracy of large language models' with technical implementation details, concise summary, beginner-friendly explanations, real-world analogies, and vulnerability considerations."

# Technology concept explanation
"Provide a comprehensive analysis of 'Container Orchestration with Kubernetes' including developer implementation details, key takeaways, step-by-step explanations, practical analogies, and security considerations."
```

### Input Format

Simply provide the article topic or content you want analyzed. The agent will:

1. **Concurrently process** the content through all 5 specialists
2. **Synthesize** the insights into a comprehensive analysis
3. **Deliver** structured output with clear sections for each perspective

### Output Structure

```
### Article Analysis:

# Comprehensive Analysis of [Topic]

## Developer Perspective
[Technical implementation details, code examples, APIs, tools]

## Summarizer Perspective
[Concise summary, key points, TL;DR]

## Explainer Perspective
[Step-by-step explanation, beginner-friendly breakdown]

## Analogy Creator Perspective
[Real-world analogies, metaphors, simple comparisons]

## Vulnerability Expert Perspective
[Security risks, vulnerabilities, mitigation strategies]

## Final Synthesis
[Comprehensive conclusion combining all insights]

---
*Analysis performed by AI Article Explainer Agent*
*Specialist inputs: Developer, Summarizer, Explainer, Analogy Creator, Vulnerability Expert*
*Model: gpt-4o*
```

---

## 🔌 API Usage

The agent exposes a RESTful API when running on `http://localhost:3773`.

### Quick Start

**Send Message to Agent:**
```bash
curl -X POST http://localhost:3773 \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "Explain quantum computing with multiple perspectives..."
      }
    ]
  }'
```

### API Documentation

For complete API documentation, visit:
- 📚 **[Bindu API Reference](https://docs.getbindu.com/api-reference/all-the-tasks/send-message-to-agent)**
- 📦 **[Postman Collections](https://github.com/GetBindu/Bindu/tree/main/postman/collections)**

---

## 🎯 Skills

### article-explain (v1.0.0)

**Primary Capability:**
- Multi-perspective article analysis through specialist AI collaboration
- Concurrent processing for faster comprehensive insights
- Structured output with clear expert perspectives

**Features:**
- ✅ 5 specialist agents working simultaneously
- ✅ Technical implementation analysis (Developer)
- ✅ Concise summarization (Summarizer)
- ✅ Beginner-friendly explanations (Explainer)
- ✅ Real-world analogies (Analogy Creator)
- ✅ Security vulnerability assessment (Vulnerability Expert)
- ✅ Comprehensive synthesis of all perspectives

**Best Used For:**
- Research paper analysis and breakdown
- Technical documentation explanation
- Educational content creation
- Security assessment of technical concepts
- Multi-perspective understanding of complex topics

**Performance:**
- Average processing time: ~15-20 seconds
- Concurrent specialist execution: 5 agents
- Memory per request: ~50MB

---

## 🐳 Docker Deployment

### Local Docker Setup

```bash
# Build and run with Docker Compose
docker-compose up --build

# Agent will be available at http://localhost:3773
```

### Docker Configuration

The agent runs on port `3773` and requires:
- `OPENROUTER_API_KEY` environment variable

Configure this in your `.env` file before running.

---

## 🌐 Deploy to bindus.directory

Make your agent discoverable worldwide and enable agent-to-agent collaboration.

### Setup GitHub Secrets

```bash
# Authenticate with GitHub
gh auth login

# Set deployment secrets
gh secret set BINDU_API_TOKEN --body "<your-bindu-api-key>"
gh secret set DOCKERHUB_TOKEN --body "<your-dockerhub-token>"
```

Get your keys:
- **Bindu API Key**: [bindus.directory](https://bindus.directory) dashboard
- **Docker Hub Token**: [Docker Hub Security Settings](https://hub.docker.com/settings/security)

### Deploy

```bash
# Push to trigger automatic deployment
git push origin main
```

GitHub Actions will automatically:
1. Build your agent
2. Create Docker container
3. Push to Docker Hub
4. Register on bindus.directory

---

## 🛠️ Development

### Project Structure

```
article-explainer-agent/
├── article_explainer_agent/
│   ├── agents.py                  # Multi-specialist agent implementation
│   ├── main.py                    # Agent entry point and Bindu integration
│   ├── service.py                 # Model configuration and PDF processing
│   ├── skills/
│   │   └── article-explain/
│   │       └── skill.yaml        # Skill configuration
│   └── agent_config.json         # Agent configuration
├── tests/
│   └── test_main.py               # Test suite
├── Makefile                       # Development commands
├── pyproject.toml                 # Dependencies and project config
└── README.md
```

### Code Quality

```bash
# Windows equivalent of make commands
uv run pre-commit run -a          # All quality checks
uv run ruff check .              # Linting
uv run ruff format .             # Formatting
uv run mypy .                   # Type checking
uv run pytest                   # Tests
```

### Pre-commit Hooks

All code quality checks are automated:
- ✅ Ruff linting and formatting
- ✅ MyPy static type checking
- ✅ Pydocstyle documentation
- ✅ pytest testing
- ✅ JSON/YAML/TOML validation

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

### Development Requirements

- All code must pass pre-commit hooks
- New features should include tests
- Follow existing code style and patterns
- Update documentation as needed

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Powered by Bindu

Built with the [Bindu Agent Framework](https://github.com/getbindu/bindu)

**Why Bindu?**
- 🌐 **Internet of Agents**: A2A, AP2, X402 protocols for agent collaboration
- ⚡ **Zero-config setup**: From idea to production in minutes
- 🛠️ **Production-ready**: Built-in deployment, monitoring, and scaling

**Build Your Own Agent:**
```bash
uvx cookiecutter https://github.com/getbindu/create-bindu-agent.git
```

---

## 📚 Resources

- 📖 [Full Documentation](https://Paraschamoli.github.io/article-explainer-agent/)
- 💻 [GitHub Repository](https://github.com/Paraschamoli/article-explainer-agent/)
- 🐛 [Report Issues](https://github.com/Paraschamoli/article-explainer-agent/issues)
- 💬 [Join Discord](https://discord.gg/3w5zuYUuwt)
- 🌐 [Agent Directory](https://bindus.directory)
- 📚 [Bindu Documentation](https://docs.getbindu.com)

---

## 🔍 Architecture

This agent uses a **concurrent multi-specialist architecture**:

1. **ArticleAgent Base Class**: Foundation for all specialist agents
2. **5 Specialist Agents**: Each with focused expertise and prompts
3. **MultiSpecialistTeam**: Synthesizes all specialist outputs
4. **Concurrent Execution**: `asyncio.gather()` for parallel processing
5. **Bindu Integration**: Server deployment and API exposure

**Key Improvements over Original:**
- ✅ No LangGraph Swarm tool call errors
- ✅ True concurrent execution vs sequential handoffs
- ✅ Better error handling and reliability
- ✅ Comprehensive type safety
- ✅ Production-ready code quality

---

<p align="center">
  <strong>Built with 💛 by the AI Agent Community 🌻</strong>
</p>

<p align="center">
  <a href="https://github.com/Paraschamoli/article-explainer-agent">⭐ Star this repo</a> •
  <a href="https://discord.gg/3w5zuYUuwt">💬 Join Discord</a> •
  <a href="https://bindus.directory">🌐 Agent Directory</a>
</p>

#   a r t i c l e - e x p l a i n e r - a g e n t 
 
 
