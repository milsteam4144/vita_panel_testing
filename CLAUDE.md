# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

VITA (Virtual Intelligent Teaching Assistant) is a Python web application built with Panel that provides an interactive learning environment for Python programming. It uses GitHub OAuth for authentication and integrates with a local LLM for AI-powered debugging and concept explanations.

## Development Commands

### Setup and Running
```bash
# Install dependencies (note: pywin32 is Windows-only and excluded on Linux)
pip install -r requirements.txt        # Windows
pip install -r requirements-linux.txt  # Linux/macOS (auto-created by run_vita_app.sh)

# Set environment variables to enable OAuth (optional - OAuth is skipped by default)
# Linux/macOS:
export SKIP_OAUTH=False  # Set to False to enable OAuth
export GITHUB_CLIENT_ID=your_client_id
export GITHUB_CLIENT_SECRET=your_client_secret

# Windows:
set SKIP_OAUTH=False  # Set to False to enable OAuth
set GITHUB_CLIENT_ID=your_client_id
set GITHUB_CLIENT_SECRET=your_client_secret

# Run the application (Linux/macOS)
./run_vita_app.sh

# Run the application (Windows)
run_vita_app.bat

# Manual Panel server command
python3 -m panel serve vita_app.py --port 8501 --allow-websocket-origin=localhost:8501 --show --dev
```

### Virtual Environment Management
```bash
# Activate virtual environment (if using vita_venv)
source vita_venv/bin/activate  # Linux/macOS
vita_venv\Scripts\activate     # Windows
```

## Architecture and Key Components

### Core Application Structure
- **vita_app.py**: Main application entry point that creates the Panel interface
- **auth.py**: GitHub OAuth authentication implementation
- **file_uploader.py**: Handles Python file uploads for debugging
- **llm_connect.py**: Integration with local LLM server (expects LM Studio at http://localhost:1234)

### Dependencies and Integration Points
- **Panel Framework**: Used for building the interactive web interface
- **AG2**: AI/agent framework (formerly AutoGen) for intelligent interactions
- **Local LLM**: Supports both LM Studio and Ollama backends
  - **LM Studio** (default): Expects TinyLlama model on port 1234
  - **Ollama** (Linux-friendly): Native Linux LLM runtime with easy model management
- **GitHub OAuth**: Required for user authentication (can be disabled)

### Educational Content Structure
The `instructor_created_data/` directory contains educational materials:
- HTML guides organized by module in `HTML_Guides_byModule/`
- Jupyter notebooks for interactive lessons
- PowerPoint slides for Python and HTML topics
- Q&A resources for student reference

## Important Considerations

### Environment Requirements
- GitHub OAuth credentials must be set as environment variables (or skip with SKIP_OAUTH=True)
- Local LLM server must be running:
  - **LM Studio**: http://localhost:1234 (default)
  - **Ollama**: http://localhost:11434 (set LLM_BACKEND=ollama)
- Python 3.x with pip package manager

### Current State
- No automated testing framework in place
- No linting or code formatting tools configured
- Simple deployment using Panel's built-in development server
- Educational focus with extensive teaching materials included
- OAuth authentication can be skipped via SKIP_OAUTH environment variable (defaults to True)
- Linux compatibility: Windows-specific packages (pywin32) automatically excluded

### Development Mode
The application runs with Panel's `--dev` flag, enabling:
- Auto-reload on code changes
- Development-friendly error messages
- WebSocket connections from localhost:8501