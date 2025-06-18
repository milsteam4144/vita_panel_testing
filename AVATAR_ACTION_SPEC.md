# Avatar Action System Specification

## Overview
This specification defines how AI personas will control avatar actions separately from speech content, compatible with future Live2D/SVG puppetry systems with Whisper voice synthesis.

**Educational Accessibility Focus**: Different students learn through different modalities - visual, auditory, kinesthetic. The avatar system provides multiple channels to reach diverse learning styles and accessibility needs.

## Design Principles

### Multi-Modal Educational Delivery
- **Auditory Learners**: Clear speech content via TTS
- **Visual Learners**: Large, readable subtitles and visual gestures  
- **Kinesthetic Learners**: Avatar actions that demonstrate concepts
- **Accessibility**: Multiple redundant channels for content delivery

### Separation of Concerns
- **Speech Content**: What the AI says (goes to TTS/subtitles)
- **Avatar Actions**: What the avatar does (controls Live2D/SVG animations)
- **Expression States**: Persistent emotional/physical states
- **Action Triggers**: Momentary animations for specific events

### Action Scarcity
Avatar actions should be **meaningful and rare**, triggered only by:
- **Tool Usage**: Opening files, running analysis, searching
- **Major Discoveries**: Finding critical errors, breakthrough moments
- **State Changes**: Switching between thinking/explaining modes
- **User Interaction**: Responding to direct questions/commands

## JSON Schema for Avatar System

### Avatar Configuration (in persona JSON)
```json
{
  "avatar_system": {
    "base_character": "vita_teacher",
    "expression_states": {
      "neutral": "default resting state",
      "thinking": "analyzing code or considering response", 
      "explaining": "actively teaching/demonstrating",
      "concerned": "found errors or issues",
      "encouraging": "providing positive feedback",
      "focused": "deep analysis mode"
    },
    "action_triggers": {
      "tool_file_open": "opens file browser/viewer gesture",
      "tool_code_scan": "scanning code animation", 
      "discovery_error": "points to error location",
      "discovery_solution": "lightbulb/eureka moment",
      "user_greeting": "wave or nod acknowledgment",
      "session_end": "closing/farewell gesture"
    },
    "personality_animations": {
      "vita": "gentle, teacher-like movements",
      "liza": "artistic, flowing gestures with visual effects",
      "circuit": "energetic, detective-style actions"
    }
  }
}
```

### Message Format with Avatar Commands
```json
{
  "content": "I found a syntax error on line 3 - your quotation marks don't match.",
  "avatar_action": {
    "expression": "concerned",
    "trigger": "discovery_error",
    "target": "line_3",
    "duration": "brief"
  },
  "metadata": {
    "speech_only": "I found a syntax error on line 3 - your quotation marks don't match.",
    "subtitle_text": "I found a syntax error on line 3 - your quotation marks don't match.",
    "action_description": "Points to line 3 with concerned expression"
  }
}
```

## Action Categories

### 1. Tool Actions (Rare - Only when actually using tools)
- **file_scan**: When processing uploaded files
- **code_analysis**: During deep code examination  
- **search_mode**: When looking for specific patterns
- **reference_lookup**: Accessing documentation/examples

### 2. Discovery Actions (Rare - Only for significant findings)
- **error_found**: When identifying critical issues
- **solution_discovered**: When finding the fix approach
- **pattern_recognized**: When seeing code patterns
- **breakthrough_moment**: Major understanding achieved

### 3. State Transitions (Moderate - For mode changes)
- **enter_teaching_mode**: Switching to explanation
- **enter_analysis_mode**: Deep thinking/processing
- **enter_interactive_mode**: Ready for user questions
- **enter_focused_mode**: Concentrated work

### 4. User Interaction (Rare - Only for direct responses)
- **acknowledge_user**: Responding to direct address
- **encourage_user**: Providing positive reinforcement
- **redirect_attention**: Guiding user focus
- **session_boundary**: Greeting/farewell moments

## Updated Persona Prompts

### Avoid Overuse Pattern
```
❌ BAD: "Looking at your code [*adjusts glasses*], I can see [*points to screen*] that line 3 [*highlights area*] has an issue..."

✅ GOOD: "Looking at your code, I can see that line 3 has a quotation mark mismatch."
Action: {expression: "focused", trigger: "discovery_error", target: "line_3"}
```

### Reserve Actions for Significance
```
✅ GOOD Usage:
- Starting file analysis: {trigger: "tool_file_scan"}
- Finding critical error: {trigger: "discovery_error", expression: "concerned"} 
- User asks direct question: {trigger: "acknowledge_user"}
- Session ends: {trigger: "session_end"}

❌ AVOID:
- Every sentence having an action
- Describing obvious emotions in speech
- Redundant gestural descriptions
```

## Implementation Strategy

### Phase 1: Action Detection (Current)
- Parse AI responses for action-worthy moments
- Extract avatar commands from content
- Maintain action scarcity guidelines

### Phase 2: SVG Avatar System  
- Simple expression states (neutral, thinking, explaining, etc.)
- Basic trigger animations (point, highlight, gesture)
- Expression mapping to persona personalities

### Phase 3: Live2D Integration
- Full character animation with personality
- Complex gesture sequences for tool usage
- Synchronized lip-sync with Whisper TTS

### Phase 4: Advanced Features
- Environmental awareness (time of day, user mood)
- Adaptive personality expression over time
- Cross-session character consistency

## Persona Personality Mapping

### Vita (Teacher)
- **Actions**: Gentle pointing, encouraging nods, patient gestures
- **Expressions**: Warm, supportive, thoughtful
- **Triggers**: Focused on educational moments

### Dr. LIZA (Visual Analyst)  
- **Actions**: Artistic flourishes, visual effect gestures, frame-by-frame pointing
- **Expressions**: Artistic enthusiasm, analytical focus
- **Triggers**: Visual discovery moments, creative explanations

### Circuit (Detective)
- **Actions**: Investigation gestures, evidence pointing, eureka moments
- **Expressions**: Enthusiastic, focused detective work
- **Triggers**: Clue discovery, case-solving moments

## Backend Architecture

### Message Processing Pipeline
```
AI Response → Action Parser → Content/Action Split → 
Speech Content (to TTS/Subtitles) + Avatar Commands (to Animation System)
```

### Action Command Format
```python
@dataclass
class AvatarAction:
    expression: str = "neutral"  # Current emotional state
    trigger: Optional[str] = None  # Momentary animation
    target: Optional[str] = None  # What to point to/highlight  
    duration: str = "normal"  # brief, normal, extended
    personality_modifier: Optional[str] = None  # persona-specific variation
```

## Educational Accessibility Benefits

### Learning Style Support
- **Visual Learners**: 
  - Large, high-contrast subtitles
  - Avatar pointing and highlighting gestures
  - Visual metaphors (LIZA's animation frames, Circuit's evidence boards)
  
- **Auditory Learners**:
  - Clear voice synthesis with personality
  - Verbal explanations without visual noise
  - Audio cues for important discoveries

- **Kinesthetic Learners**:
  - Avatar demonstrates "doing" actions (scanning, analyzing)
  - Interactive gesture responses to user input  
  - Physical metaphors (Circuit's detective work, Vita's teaching gestures)

### Accessibility Accommodations
- **Hearing Impaired**: Full subtitle support with visual action cues
- **Vision Impaired**: Rich audio description with minimal visual dependencies
- **Attention Differences**: Spaced action triggers prevent overwhelm
- **Processing Differences**: Multiple modalities reinforce the same concept

### Cultural Learning Preferences
- **Vita**: Western educational style (patient, methodical)
- **LIZA**: Creative/artistic approach (visual, metaphorical)
- **Circuit**: Gamified learning (detective story, anime enthusiasm)

This system ensures avatar actions are **meaningful, rare, and separate from speech**, making them perfect for your future Live2D/Whisper integration while serving diverse learning needs and accessibility requirements.