# claude-conduit Testing & Verification Documentation

## Status: MOCK MODE vs LIVE MODE

🚨 **CRITICAL: Always identify simulation vs reality**

### Current Status: MOCK MODE ✋
claude-conduit is currently running in **MOCK MODE** with simulated MCP server responses. This is clearly indicated by:

- Server logs: `📝 Running in mock mode for development`
- Mock responses: `"result": "Mock execution result - MCP integration pending"`
- Mock server names: `"servers": ["mock-server"]`

### Live Mode Requirements 🎯
For **LIVE MODE** with real MCP integration:
- ✅ MCP config found at `~/.config/claude/claude_desktop_config.json`
- ✅ Real MCP servers (taskmaster-ai, filesystem, scout) responding
- ✅ Actual API keys configured
- ✅ Server logs: `🔗 Connected to taskmaster-ai` (not mock-server)

## Verification Test Results ✅

### Test Session: 2025-06-25 23:43 UTC

**Environment:**
- Status: MOCK MODE
- Node.js: v23.11.0
- Platform: darwin arm64
- Port: 3001

**Endpoints Tested:**

#### `/health` ✅
```json
{
  "status": "ok",
  "servers": ["mock-server"],  ← MOCK MODE INDICATOR
  "uptime": 127,
  "version": "1.0.0"
}
```

#### `/fortune` ✅ 
```json
{
  "claude-conduit": {
    "rubber_duck": "Remember how explaining to a duck reveals solutions",
    "debugging": "classic",
    "revelation": "coming"
  },
  "timestamp": "2025-06-25T23:43:06.500Z"
}
```

#### `/tools` ✅
```json
{
  "mock-server": [  ← MOCK MODE INDICATOR
    {
      "name": "example_tool",
      "description": "Example tool for testing"
    }
  ]
}
```

#### `POST /execute/mock-server/example_tool` ✅
```json
{
  "success": true,
  "server": "mock-server",  ← MOCK MODE INDICATOR
  "result": {
    "result": "Mock execution result - MCP integration pending"  ← CLEAR MOCK INDICATOR
  }
}
```

## Devil's Advocate Use Case 🔍

### Scenario: "Verify this critical assumption"

**User Request:** *"A particular fact or piece of information is key to our plan. I should spawn an agent through claude-conduit to determine whether or not this is correct or not. Also known as 'devil's advocate me'"*

### Implementation Design:

#### 1. Live Mode Integration Required
```javascript
// POST /execute/taskmaster-ai/spawn_devil_advocate
{
  "assumption": "VIBE fortunes improve learning outcomes",
  "context": "Educational framework for VITA project",
  "evidence_required": ["research", "user_feedback", "metrics"],
  "devil_advocate_mode": true
}
```

#### 2. Expected Live Response
```json
{
  "success": true,
  "server": "taskmaster-ai",
  "tool": "spawn_devil_advocate",
  "result": {
    "agent_id": "devil_advocate_001",
    "assumption_analyzed": "VIBE fortunes improve learning outcomes",
    "counter_arguments": [
      "No empirical data on fortune effectiveness",
      "Potential distraction from actual learning",
      "Unclear measurement criteria"
    ],
    "evidence_gaps": [
      "User testing data needed",
      "Learning outcome metrics required",
      "Comparative studies missing"
    ],
    "recommendations": [
      "Implement A/B testing",
      "Track engagement metrics",
      "Survey learner feedback"
    ],
    "confidence": "medium_skepticism"
  }
}
```

#### 3. Mock Mode Response (Current)
```json
{
  "success": true,
  "server": "mock-server",
  "result": "Mock execution result - MCP integration pending"
}
```

### Clear Differentiation Strategy

#### Visual Indicators
- **Mock Mode:** 🎭 Mock responses, clear simulation labels
- **Live Mode:** 🔴 Real agent spawning, actual analysis

#### Response Headers
```http
X-Claude-Conduit-Mode: mock
X-MCP-Integration: simulated
X-Agent-Type: mock_devil_advocate
```

vs

```http
X-Claude-Conduit-Mode: live
X-MCP-Integration: real
X-Agent-Type: taskmaster_ai_agent
```

#### Logging Standards
```
MOCK: 🎭 Simulating devil's advocate analysis...
LIVE: 🔴 Spawning real taskmaster-ai devil's advocate agent...
```

## Testing Checklist for Live Integration

### Before Claiming "Live Mode"
- [ ] Verify real MCP config loaded
- [ ] Confirm taskmaster-ai responds to ping
- [ ] Test actual agent spawning
- [ ] Validate devil's advocate reasoning quality
- [ ] Ensure non-mock responses
- [ ] Check agent memory persistence
- [ ] Verify task breakdown functionality

### Transparency Requirements
- [ ] Always label simulation vs reality
- [ ] Clear mock indicators in all responses
- [ ] Explicit mode declaration in logs
- [ ] User warnings about current capabilities
- [ ] Honest assessment of agent intelligence

## Future Live Mode Features

### Real Devil's Advocate Agent
- **Spawn dedicated skeptical agent**
- **Challenge assumptions with evidence**
- **Provide counter-research**
- **Generate alternative hypotheses**
- **Rate argument strength**

### Agent Coordination
- **Multi-agent debate simulation**
- **Evidence gathering from multiple sources**
- **Collaborative fact-checking**
- **Cross-validation of claims**

## VIBE Verification Example

**Claim:** "VIBE system effectiveness"
**Devil's Advocate Questions:**
- How do we measure inspiration?
- Could fortunes become noise?
- Do embedded commands actually work?
- Is randomness optimal for learning?
- Where's the educational research backing?

**Current Status:** MOCK MODE - these are designed questions, not AI-generated skepticism

**Live Mode Goal:** Real agent generates novel counter-arguments we haven't considered

---

## Testing Philosophy

**"Verify, and Inspirational Behaviors Emerge"** applies to our testing:
- **Verify** our claims with transparent testing
- **Document** simulation vs reality clearly
- **Enable** others to learn from our verification process
- **Model** honest assessment of capabilities

**Bottom Line:** Never mislead about AI capabilities. Always distinguish mock from live integration.