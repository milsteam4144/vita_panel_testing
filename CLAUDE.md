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

### Git Flow Management
```bash
# Use stash to maintain flow when switching contexts
git stash                    # Save current work without committing
git stash pop               # Restore stashed changes
git stash list              # View all stashes

# Create cozy branches for safe experimentation
git checkout -b feature/cozy-experiment
git push -u origin feature/cozy-experiment
```

**FLOW Principle**: Both `git stash` and cozy branches preserve your flow when context switching is necessary. Stash for quick switches, cozy branches for longer experiments.

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

## claude-conduit MCP Bridge Integration

### Enhanced AI Capabilities

VITA development is enhanced through **claude-conduit**, an HTTP bridge that connects Claude Code to Model Context Protocol (MCP) servers, providing advanced AI tooling capabilities that persist across sessions.

#### Available MCP Servers

**taskmaster-ai** - Advanced task planning and management:
```bash
# Example usage through claude-conduit
POST http://localhost:3001/execute/taskmaster-ai/create_project
{
  "name": "VITA Enhancement Sprint",
  "description": "Multi-agent debugging system",
  "subtasks": 5,
  "methodology": "FLOW"
}
```

**filesystem** - Enhanced file operations:
```bash
# Cross-repository analysis
POST http://localhost:3001/execute/filesystem/analyze_codebase
{
  "path": "/workspace",
  "pattern": "*.py",
  "analysis": "educational_patterns"
}
```

**scout** - Advanced search and context:
```bash
# Research educational patterns
POST http://localhost:3001/execute/scout/research
{
  "query": "error handling patterns for students",
  "context": "educational"
}
```

**cloud-memory** - Persistent project context:
```bash
# Store/retrieve project knowledge across sessions
POST https://csi-prism-remote-mcp-production.up.railway.app/store
{
  "path": "vita/project_context",
  "data": {"current_phase": "VERIFY", "methodology": "FLOW"}
}
```

### Advanced Workflows

#### Devil's Advocate Analysis
Spawn skeptical agents to challenge assumptions and verify critical information:
```bash
POST /execute/taskmaster-ai/spawn_devil_advocate
{
  "assumption": "This code pattern helps student learning",
  "context": "VITA educational framework",
  "evidence_required": ["research", "user_feedback", "metrics"]
}
```

#### Enhanced Code Review
Multi-agent collaboration for educational code review:
- Security and best practices analysis
- Educational value assessment
- SOLID principles verification
- Learning progression evaluation

#### FLOW Methodology Automation
- **LEARN**: Research educational context through scout
- **UNDERSTAND**: Challenge assumptions with devil's advocate
- **PLAN**: Generate structured breakdowns with taskmaster-ai
- **EXECUTE**: Implement guided solutions using MCP tools
- **VERIFY**: Validate and test with multi-agent collaboration
- **DOCUMENT**: Capture knowledge automatically to cloud memory

### VIBE System Integration

**VIBE** (Verify, and Inspirational Behaviors Emerge) - The principle that clear, documented processes become automatic teaching moments. When you verify your work transparently, others learn by watching.

#### VIBE Fortune System
claude-conduit includes an educational fortune system with 45+ fortunes covering:
- FLOW methodology principles
- SAFE framework guidance
- SOLID programming principles
- Agile development practices
- Embedded learning commands ("Notice how...", "Feel the...", "Watch yourself...")

Access random educational wisdom:
```bash
GET http://localhost:3001/fortune
```

### Setup and Configuration

#### Starting claude-conduit
```bash
# Navigate to claude-conduit directory
cd claude-conduit

# Install dependencies
npm install

# Start the bridge server
npm start

# Verify health
curl http://localhost:3001/health
```

#### MCP Server Configuration
claude-conduit reads from your MCP configuration file:
```bash
# Default config location
~/.config/claude/claude_desktop_config.json
```

#### Environment Variables
```bash
# Required for enhanced capabilities
export ANTHROPIC_API_KEY="sk-ant-api03-..."
export MCP_CONFIG_PATH="~/.config/claude/claude_desktop_config.json"

# Optional
export CONDUIT_PORT="3001"
export LOG_LEVEL="info"
```

### Cloud Memory Persistence

#### Railway App Integration
- **Endpoint**: https://csi-prism-remote-mcp-production.up.railway.app/
- **Purpose**: Persistent project memory across sessions
- **Backend**: Supabase database for reliable storage
- **Features**: Hierarchical paths, JSON content, bulk operations

#### Persistent Context
The cloud memory server retains:
- Project learning objectives and methodology decisions
- FLOW phase progress and completion status
- Educational framework choices and rationale
- Code review insights and pattern recognition
- Student progression and learning analytics

### Troubleshooting

#### Connection Issues
```bash
# Test claude-conduit connectivity
curl http://localhost:3001/health

# Check MCP server status
curl http://localhost:3001/tools

# Verify cloud memory access
curl https://csi-prism-remote-mcp-production.up.railway.app/health
```

#### Common Problems
- **Port conflicts**: Change CONDUIT_PORT environment variable
- **MCP config not found**: Verify MCP_CONFIG_PATH points to valid config
- **Authentication errors**: Check ANTHROPIC_API_KEY is set correctly
- **Cloud memory timeouts**: Railway app may be sleeping, retry request

### Educational Philosophy Integration

#### FLOW Methodology (Following Logical Work Order)
VITA development follows FLOW principles enhanced by MCP capabilities:
1. **LEARN** - Use scout for educational research
2. **UNDERSTAND** - Devil's advocate challenges assumptions  
3. **PLAN** - taskmaster-ai creates structured approaches
4. **EXECUTE** - Enhanced tools guide implementation
5. **VERIFY** - Multi-agent validation processes
6. **DOCUMENT** - Cloud memory preserves knowledge

#### SAFE Framework (Scaled Agile Framework for Education)
- **Structure** that serves learning through organized MCP workflows
- **Always** creating better outcomes with enhanced AI tooling
- **Frees** creative potential through automated task management
- **Excellence** becomes inevitable through persistent memory and iteration

The enhanced AI capabilities demonstrate that when you **Verify, and Inspirational Behaviors Emerge** - transparent use of advanced tools becomes a teaching moment for students and team members observing the development process.