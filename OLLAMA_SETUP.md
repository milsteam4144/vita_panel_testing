# VITA - Ollama Integration Setup

## Overview
VITA now uses Ollama exclusively for local LLM inference, replacing LM Studio.

## Prerequisites
1. Install Ollama from https://ollama.ai
2. Pull a model: `ollama pull llama2`
3. Start Ollama service: `ollama serve`

## Quick Start
```bash
# 1. Start Ollama
ollama serve

# 2. In another terminal, start VITA
panel serve vita_test_minimal.py --show --dev
```

## Configuration
- **Default model**: `llama2`
- **Endpoint**: `http://localhost:11434/v1/chat/completions`
- **Timeout**: 30 seconds

## Files Modified
- `llm_connect.py`: Pure Ollama integration
- `vita_test_minimal.py`: OAuth-free test interface

## Testing
Run: `python -c "from llm_connect import call_local_llm; print(call_local_llm('Hello'))"`

## Next Steps
- Set up environment variables for model selection
- Add error handling improvements
- Implement proper authentication for production