# claude-conduit

**VIBE-powered bridge connecting Claude Code to MCP servers**

*"teacherbot.help has a posse"*

## Overview

claude-conduit is a lightweight HTTP bridge that enables Claude Code CLI to access Model Context Protocol (MCP) servers. It translates HTTP requests into MCP protocol calls, providing seamless integration between Claude Code and your existing MCP infrastructure.

### VIBE System

**VIBE** (Verify, and Inspirational Behaviors Emerge) delivers randomized educational fortunes on startup, combining:
- **Technical wisdom** (SOLID, Agile, FLOW principles)
- **Embedded NLP commands** ("Notice how...", "Feel the...")
- **Community encouragement** (teacherbot.help references)
- **Future Live2D emotion channels** (metadata for avatar expressions)

## Architecture

```
┌─────────────────┐    HTTP     ┌─────────────────┐    MCP     ┌─────────────────┐
│   Claude Code   │─────────────►│  claude-conduit │─────────────►│   MCP Servers   │
│      CLI        │             │    (Bridge)     │             │  (taskmaster,   │
│                 │             │                 │             │   filesystem,   │
│                 │◄─────────────│                 │◄─────────────│   scout, etc.)  │
└─────────────────┘   JSON      └─────────────────┘   Protocol  └─────────────────┘
```

## Features

### Core Bridge Functionality
- **Multi-server support**: Connect to all configured MCP servers simultaneously
- **Tool discovery**: Automatic enumeration of available MCP tools
- **Request translation**: HTTP → MCP protocol conversion
- **Error handling**: Graceful degradation and meaningful error messages
- **Health monitoring**: Status endpoints for service monitoring

### VIBE Fortune System
- **Startup fortunes**: Random educational wisdom on service start
- **JSON format**: Structured fortune data with metadata
- **Multiple categories**: FLOW, VIBE, HYPE, MOOD, ENERGY acronyms
- **Embedded commands**: NLP patterns for learning enhancement
- **API endpoint**: Programmatic fortune access

### Educational Integration
- **FLOW methodology**: Following Logical Work Order principles
- **SAFE framework**: Scaled Agile Framework for Education
- **Learning patterns**: Embedded commands for skill development
- **Community building**: teacherbot.help solidarity messages

## API Reference

### Endpoints

#### `GET /health`
Service health check and connected server status.

**Response:**
```json
{
  "status": "ok",
  "servers": ["taskmaster-ai", "filesystem", "scout"],
  "uptime": 3600,
  "version": "1.0.0"
}
```

#### `GET /tools`
List all available tools across connected MCP servers.

**Response:**
```json
{
  "taskmaster-ai": [
    {
      "name": "create_project",
      "description": "Create a new project with subtasks",
      "input_schema": {...}
    }
  ],
  "filesystem": [...],
  "scout": [...]
}
```

#### `POST /execute/{server}/{tool}`
Execute a specific tool on a given MCP server.

**Parameters:**
- `server`: MCP server name (e.g., "taskmaster-ai")
- `tool`: Tool name (e.g., "create_project")

**Request Body:**
```json
{
  "name": "VITA Enhancement Sprint",
  "description": "Implement multi-agent debugging system",
  "subtasks": 5,
  "priority": "high"
}
```

**Response:**
```json
{
  "success": true,
  "result": {
    "project_id": "proj_12345",
    "subtasks": [
      {"id": "task_1", "title": "Design agent architecture"},
      {"id": "task_2", "title": "Implement communication protocol"}
    ]
  }
}
```

#### `GET /fortune`
Get a random VIBE fortune for inspiration.

**Response:**
```json
{
  "claude-conduit": {
    "vibe_check": "You're already doing it",
    "VIBE": "Validating Inspirational Backend Encouragement",
    "confidence": "deserved"
  },
  "timestamp": "2025-06-25T19:00:00.000Z"
}
```

## Configuration

### Environment Variables

```bash
# Required
export ANTHROPIC_API_KEY="sk-ant-api03-..."
export MCP_CONFIG_PATH="/path/to/claude_desktop_config.json"

# Optional
export CONDUIT_PORT="3001"
export CONDUIT_HOST="localhost"
export LOG_LEVEL="info"
export FORTUNE_ENABLED="true"
```

### MCP Server Configuration

claude-conduit reads from your existing `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "taskmaster-ai": {
      "command": "npx",
      "args": ["-y", "--package=task-master-ai", "task-master-ai"],
      "env": {
        "ANTHROPIC_API_KEY": "${ANTHROPIC_API_KEY}",
        "MODEL": "claude-3-5-sonnet-20241022"
      }
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/workspace"],
      "env": {}
    }
  }
}
```

## Usage Examples

### Claude Code Integration

```javascript
// claude-code-tool.js
async function callMCP(server, tool, params) {
  const response = await fetch(`http://localhost:3001/execute/${server}/${tool}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(params)
  });
  return await response.json();
}

// Create a project using taskmaster-ai
const project = await callMCP('taskmaster-ai', 'create_project', {
  name: 'VITA Sprint 1',
  description: 'Multi-agent debugging system',
  subtasks: 5
});

// Read file using filesystem server
const fileContent = await callMCP('filesystem', 'read_file', {
  path: '/workspace/src/main.py'
});
```

### Educational Workflow Integration

```javascript
// FLOW methodology example
async function implementFlowTask(taskDescription) {
  // LEARN - Gather requirements
  const requirements = await callMCP('scout', 'search', {
    query: taskDescription,
    context: 'educational'
  });
  
  // UNDERSTAND - Break down the task
  const project = await callMCP('taskmaster-ai', 'create_project', {
    name: taskDescription,
    requirements: requirements.result
  });
  
  // PLAN - Structure the work
  const plan = await callMCP('taskmaster-ai', 'generate_plan', {
    project_id: project.project_id,
    methodology: 'FLOW'
  });
  
  return { requirements, project, plan };
}
```

## Testing Strategy

### Unit Tests
- **Fortune system**: Verify random selection and JSON structure
- **MCP client initialization**: Mock server connections
- **HTTP endpoints**: Request/response validation
- **Error handling**: Graceful failure scenarios

### Integration Tests
- **End-to-end workflows**: Claude Code → conduit → MCP server
- **Multi-server coordination**: Concurrent MCP server access
- **Configuration loading**: Various config file formats
- **Network resilience**: Connection failure recovery

### Educational Scenario Tests
- **FLOW methodology**: Complete learning cycle execution
- **VIBE fortune delivery**: Startup and API fortune generation
- **Task management**: Project creation and tracking workflows
- **File operations**: Cross-repository code analysis

## Development

### Getting Started

```bash
# Clone and setup
cd /path/to/your/project
mkdir claude-conduit && cd claude-conduit

# Install dependencies
npm install

# Set environment variables
export ANTHROPIC_API_KEY="your-key-here"
export MCP_CONFIG_PATH="$HOME/.config/claude/claude_desktop_config.json"

# Start development server
npm run dev
```

### Project Structure

```
claude-conduit/
├── package.json              # Dependencies and scripts
├── README.md                 # This documentation
├── server.js                 # Main bridge server
├── claude-conduit-fortunes.js # VIBE fortune system
├── lib/
│   ├── mcp-client.js         # MCP protocol client
│   ├── fortune-engine.js     # Fortune selection logic
│   └── health-monitor.js     # Service monitoring
├── tests/
│   ├── unit/                 # Unit tests
│   ├── integration/          # Integration tests
│   └── fixtures/             # Test data
└── docs/
    ├── api.md               # Detailed API documentation
    ├── deployment.md        # Production deployment guide
    └── troubleshooting.md   # Common issues and solutions
```

## Troubleshooting

### Common Issues

**Connection Refused (Port 3001)**
```bash
# Check if port is in use
lsof -i :3001

# Try alternative port
export CONDUIT_PORT=3002
npm start
```

**MCP Server Not Responding**
```bash
# Verify MCP config
cat $HOME/.config/claude/claude_desktop_config.json

# Test individual server
npx -y --package=task-master-ai task-master-ai --help
```

**Missing API Keys**
```bash
# Verify environment
echo $ANTHROPIC_API_KEY | head -c 20

# Check config file permissions
ls -la $HOME/.config/claude/
```

## Educational Philosophy

claude-conduit embodies the FLOW methodology:

- **F**un Learning Optimizes Wisdom
- **L**ogical work order prevents chaos
- **O**rganized structure enables creativity
- **W**isdom emerges through consistent practice

The VIBE system demonstrates that when you **Verify, and Inspirational Behaviors Emerge** - clear, documented processes become automatic teaching moments. Students, interns, and junior developers learn by watching transparent verification in action. Even the AI models integrated into claude-conduit learn from this principle: observable process verification creates inspiring patterns for others to follow.

## Future Enhancements

### Planned Features
- **Live2D emotion integration**: VIBE metadata drives avatar expressions
- **Learning analytics**: Track educational pattern recognition
- **Multi-user support**: Team-based MCP server access
- **Plugin architecture**: Custom fortune categories and MCP protocols

### Research Areas
- **Adaptive fortune selection**: AI-driven encouragement optimization
- **Cross-server workflows**: Complex multi-MCP operations
- **Educational metrics**: Learning effectiveness measurement
- **Community features**: Shared fortunes and collaborative debugging

## Contributing

claude-conduit follows the FLOW methodology for contributions:

1. **LEARN**: Understand the codebase and requirements
2. **UNDERSTAND**: Process the change request thoroughly
3. **PLAN**: Design your approach in issues/PRs
4. **EXECUTE**: Implement following the plan
5. **VERIFY**: Test thoroughly with provided test suites
6. **DOCUMENT**: Update docs and share learnings

See `CONTRIBUTING.md` for detailed guidelines.

## License

MIT License - see LICENSE file for details.

---

*"Notice how your skills keep improving" - claude-conduit VIBE fortune*

**teacherbot.help has a posse** 🎯