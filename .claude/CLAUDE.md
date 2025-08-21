# VITA Panel Testing - Claude Development Guide

## Project Overview
VITA (Virtual Interactive Teaching Assistant) is a Panel-based educational platform for Python programming assistance, powered by local Ollama LLM integration.

## Architecture Approach
- **Modular Design**: Easy component swapping and testing
- **Local LLM**: Ollama integration for privacy and control
- **Educational Focus**: Code debugging and concept explanation
- **OAuth Ready**: GitHub authentication (can be stubbed for development)

## Key Components

### Core Modules
- `llm_connect.py` - Ollama API integration (modular LLM interface)
- `auth.py` - GitHub OAuth authentication  
- `file_uploader.py` - Python file upload handling
- `vita_app.py` - Main Panel application
- `vita_test_minimal.py` - OAuth-free test interface

### Development Setup
- **LLM Provider**: Ollama (localhost:11434)
- **Default Model**: llama2
- **Framework**: Panel for web interface
- **Testing**: Modular components allow easy mocking

## Development Guidelines

### LLM Integration
```python
# Current approach - modular and swappable
from llm_connect import call_local_llm, build_chat_callback

# Easy to change providers by modifying llm_connect.py only
response = call_local_llm("Debug this Python code")
```

### Component Design
- Keep modules focused and single-responsibility
- Use dependency injection where possible
- Support both production and test configurations
- Graceful error handling with informative messages

### Testing Strategy
- `vita_test_minimal.py` for OAuth-free development
- Mock responses when LLM services unavailable
- Modular design allows component-level testing
- Environment variables for configuration flexibility

## Quick Start Commands
```bash
# Start Ollama service
ollama serve

# Install model
ollama pull llama2

# Run development server (OAuth-free)
panel serve vita_test_minimal.py --show --dev

# Run full app (requires GitHub OAuth setup)
panel serve vita_app.py --show --dev
```

## Environment Configuration
```bash
# Optional - for production OAuth
export GITHUB_CLIENT_ID=your_client_id
export GITHUB_CLIENT_SECRET=your_client_secret

# Ollama configuration (defaults shown)
export OLLAMA_HOST=localhost:11434
export OLLAMA_MODEL=llama2
export OLLAMA_TIMEOUT=30
```

## Code Quality Tools
- **Linting**: Run `make lint` or `flake8 .`
- **Testing**: Run `make test` or `pytest`
- **Format**: Run `make format` or `black .`

## Development Workflow
1. **Component Development**: Work on individual modules
2. **Local Testing**: Use `vita_test_minimal.py` for rapid iteration
3. **Integration Testing**: Test with real Ollama when ready
4. **Production Testing**: Enable OAuth for full workflow

## Key Design Decisions
- **Ollama over LM Studio**: Better API stability and model selection
- **Modular LLM Interface**: Easy to swap providers or add fallbacks
- **OAuth Flexibility**: Can be enabled/disabled for development
- **Panel Framework**: Python-native web interface for educators

## Branch Strategy
- `main`: Stable releases
- `vita-sandbox`: Active development
- Feature branches for major changes

This modular approach ensures easy maintenance, testing, and adaptation as requirements evolve.