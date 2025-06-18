# VITA Panel User Stories and Test Requirements

## User Stories

### Story 1: Student Uploads Python Code for Debugging
**As a** student learning Python  
**I want to** upload my Python code file  
**So that** I can get help debugging syntax errors  

**Acceptance Criteria:**
- File upload accepts only .py files
- Code displays with line numbers
- Upload feedback shows success/failure
- File content persists during session

**Tests:**
- `test_file_upload_valid_python()`
- `test_file_upload_invalid_type()`
- `test_file_upload_empty_file()`
- `test_file_upload_large_file()`
- `test_line_numbering_display()`

### Story 2: Student Requests Code Debugging
**As a** student with buggy code  
**I want to** click "Debug the uploaded code"  
**So that** AI agents identify my syntax errors  

**Acceptance Criteria:**
- Debug button disabled until file uploaded
- Agents provide specific error locations
- Errors explained in simple English
- No corrected code shown (learning focused)

**Tests:**
- `test_debug_button_state_management()`
- `test_debugger_agent_identifies_syntax_errors()`
- `test_debugger_agent_line_number_accuracy()`
- `test_debugger_agent_no_code_correction()`

### Story 3: Student Receives Correction Guidance
**As a** student who understands the error  
**I want to** receive guidance on fixing it  
**So that** I can learn to fix it myself  

**Acceptance Criteria:**
- Corrector provides step-by-step guidance
- Examples use different content (not the solution)
- Student can ask follow-up questions
- Conversation continues until student satisfied

**Tests:**
- `test_corrector_agent_provides_guidance()`
- `test_corrector_agent_no_direct_solutions()`
- `test_multi_turn_conversation()`
- `test_conversation_termination()`

### Story 4: Student Explores Programming Concepts
**As a** student learning Python basics  
**I want to** select and learn about programming concepts  
**So that** I understand fundamental concepts  

**Acceptance Criteria:**
- Dropdown shows categorized concepts
- AI provides brief overviews
- Instructor examples link works
- Independent from debugging flow

**Tests:**
- `test_concept_dropdown_categories()`
- `test_ai_concept_explanation()`
- `test_instructor_examples_link()`
- `test_concept_flow_independence()`

### Story 5: Student Toggles Code Display
**As a** student using limited screen space  
**I want to** hide/show the code panel  
**So that** I can focus on the chat or code as needed  

**Acceptance Criteria:**
- Toggle button clearly labeled
- State persists during session
- Chat expands when code hidden
- Smooth transition animation

**Tests:**
- `test_toggle_button_functionality()`
- `test_toggle_state_persistence()`
- `test_layout_responsiveness()`
- `test_toggle_animation()`

## Test Suite Structure

```python
# tests/test_unit_agents.py
class TestDebuggerAgent:
    def test_debugger_isolation(self):
        """Test Debugger agent with mocked LM Studio"""
        
    def test_debugger_syntax_error_detection(self):
        """Test various syntax error patterns"""
        
    def test_debugger_empty_input_handling(self):
        """Test behavior with empty/invalid input"""

class TestCorrectorAgent:
    def test_corrector_isolation(self):
        """Test Corrector agent with mocked LM Studio"""
        
    def test_corrector_guidance_generation(self):
        """Test guidance without revealing solution"""
        
    def test_corrector_example_generation(self):
        """Test that examples differ from student code"""

# tests/test_integration.py
class TestAgentOrchestration:
    def test_agent_handoff(self):
        """Test Debugger to Corrector transition"""
        
    def test_conversation_termination(self):
        """Test proper conversation ending"""
        
    def test_no_empty_message_loops(self):
        """Test that agents don't send empty messages"""

# tests/test_ui_components.py
class TestFileUpload:
    def test_file_validation(self):
        """Test file type and size validation"""
        
    def test_upload_feedback(self):
        """Test user feedback on upload status"""

class TestChatInterface:
    def test_message_rendering(self):
        """Test chat messages display correctly"""
        
    def test_avatar_display(self):
        """Test agent avatars show properly"""

# tests/test_error_handling.py
class TestErrorRecovery:
    def test_lm_studio_offline(self):
        """Test graceful handling when LM Studio unavailable"""
        
    def test_api_timeout(self):
        """Test timeout handling for slow responses"""
        
    def test_concurrent_requests(self):
        """Test multiple simultaneous user actions"""

# tests/test_performance.py
class TestPerformance:
    def test_response_time_baseline(self):
        """Establish baseline response times"""
        
    def test_large_file_handling(self):
        """Test performance with large Python files"""
        
    def test_memory_usage(self):
        """Monitor memory during extended sessions"""
```

## LM Studio Performance Investigation

### Potential Causes:
1. **Context Length**: AutoGen may be sending full conversation history each time
2. **System Prompts**: Long system prompts for each agent increase token count
3. **Model Loading**: Dolphin model might be larger/slower than others
4. **API Overhead**: OpenAI compatibility layer adds latency
5. **Temperature Setting**: Temperature=0 might cause more processing

### Quick Optimizations:
```python
# Reduce context window
gpt4_config = {
    "config_list": config_list, 
    "temperature": 0.1,  # Slightly higher for faster generation
    "max_tokens": 500,   # Limit response length
    "seed": 53
}

# Add request timeout
config_list = [{
    'model': 'dolphin-2.1-mistral-7b',
    'base_url': 'http://localhost:1234/v1',
    'api_key': 'lm-studio',
    'timeout': 30  # 30 second timeout
}]
```

### Performance Test Plan:
1. Measure baseline response time with curl
2. Compare AutoGen vs direct API calls
3. Profile token usage per request
4. Test with different models (smaller = faster?)
5. Monitor LM Studio resource usage