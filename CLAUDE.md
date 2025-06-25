# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

VITA (Virtual Interactive Teaching Assistant) is a Python web application that creates an interactive chat interface for debugging and explaining code. It uses Panel for the web UI and AutoGen for multi-agent conversations with LLMs.

## Architecture

### Core Components

- **Panel UI Framework**: Creates web interface with file upload, chat interface, and programming concept examples
- **AutoGen Multi-Agent System**: Implements three agent roles:
  - `Student` (MyConversableAgent): Human user proxy with input handling
  - `Debugger`: Identifies syntax errors in uploaded Python code
  - `Corrector`: Suggests fixes for identified errors
- **File Processing**: Handles Python file uploads with syntax highlighting and line numbering

### Key Files

- `test.py`: Main application file (newer version)
- `main_test.py`: Alternative main file (similar functionality)
- `logo.png`: VITA logo displayed in header

### Current Model Configuration

The application is configured to use OpenAI's GPT-4o model via the `config_list` in both files:
```python
config_list = [
    {
        'model': 'gpt-4o',
        'api_key': os.environ.get("OPENAI_API_KEY"),
    }
]
```

## Commands

### Running the Application
```bash
# Install dependencies
pip install panel pyautogen openai

# Set OpenAI API key
export OPENAI_API_KEY='your_api_key_here'

# Run the application (test.py is the main file)
panel serve test.py

# Alternative main file
panel serve main_test.py

# Access at http://localhost:5006
```

### Development Commands
```bash
# Run with auto-reload for development
panel serve test.py --autoreload

# Serve on different port
panel serve test.py --port 5007

# Show verbose output
panel serve test.py --show
```

## Environment Setup

Required environment variables:
- `OPENAI_API_KEY`: OpenAI API key for GPT model access
- `AUTOGEN_USE_DOCKER`: Set to "False" in code (Docker disabled)

Dependencies:
- `panel`: Web UI framework
- `pyautogen`: Multi-agent conversation framework  
- `openai`: OpenAI API client
- `param`: Parameter validation for Panel components

## UI Features

- File upload for Python (.py) files with syntax highlighting
- Toggle show/hide for uploaded code
- Debug button to analyze uploaded code
- Programming concept selector with AI examples
- Link to instructor examples (external website)
- Multi-agent chat interface with avatars

## Development Notes

- Both `test.py` and `main_test.py` contain nearly identical code with minor differences
- Uses asyncio for handling user input in multi-agent conversations
- Custom CSS styling with golden background (#f1b825) and dark code sections
- Global variable `test` stores uploaded file content
- Chat interface uses callback system for agent communication

## Recent Fixes (June 2025)

### Critical Issues Resolved
- **Issue #001**: Fixed Corrector agent infinite empty message loop by adding content validation
- **Issue #002**: Added error handling for LM Studio disconnections with user-friendly messages
- **Issue #003**: Implemented conversation lock to prevent multiple concurrent agent conversations

### Code Quality Improvements
- Fixed syntax warning: `is not ""` changed to `!= ""`
- Updated model name to match actual LM Studio model: `dolphin-2.1-mistral-7b`
- Added proper error recovery and user feedback

## Known Issues
- LM Studio may have higher latency compared to other local model implementations
- Global state management could benefit from refactoring
- No automated test coverage yet

## MVP Demo Readiness
The application is now stable for demo purposes with proper error handling and agent orchestration fixes.

## Educational Framework Integration

### FLOW Methodology (Following Logical Work Order)
VITA now implements FLOW methodology for educational purposes:
1. **LEARN** - Understand concepts and requirements
2. **UNDERSTAND** - Process and internalize information  
3. **PLAN** - Design approach step-by-step
4. **EXECUTE** - Implement following the plan
5. **VERIFY** - Test and validate results
6. **DOCUMENT** - Capture knowledge for future use

### SAFE Framework (Scaled Agile Framework for Education)
Educational adaptation of SAFe principles:
- **Structure** that serves learning
- **Always** creating better outcomes  
- **Frees** creative potential
- **Excellence** becomes inevitable

### Three-Session Learning Structure
Each major learning activity follows three distinct sessions:
1. **Discovery & Planning** (🟢 Green Light) - Collaborative exploration
2. **Design & Review** (🟡 Yellow Light) - Structured planning with feedback
3. **Deep Work Implementation** (🔴 Red Light) - Protected focus time

### Task Management
Current project tasks are tracked in `/tasks.md` with GitHub integration for proper FLOW methodology implementation. See:
- [Three-Session Workflow Guide](./vita-project/docs/three-session-workflow.md)
- [FOCUS System for Students](./vita-project/docs/focus-system-for-students.md)
- [GitHub Workflow Guide](./docs/github-workflow-guide.md)
- [Why FLOW Works](./vita-project/docs/why-flow-works.md)