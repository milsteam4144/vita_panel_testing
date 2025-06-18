# VITA Testing Guide

## Quick Start Testing

### 1. Run All Tests
```bash
# Activate environment and run tests
./start_console.sh  # This will setup dependencies
python -m pytest tests/ -v
```

### 2. Test Specific Components

**Persona Behavior Tests:**
```bash
python -m pytest tests/test_persona_behavior.py -v
```

**VITA Trio Tests:**
```bash
python -m pytest tests/test_vita_trio.py -v
```

**Console Demo Tests:**
```bash
python -m pytest tests/test_console_demo.py -v
```

## Testing VITA Trio (New Multi-Agent System)

### Configuration Test
```bash
# Test that VITA Trio loads correctly
python -c "
from persona_manager import PersonaManager
pm = PersonaManager()
trio = pm.get_persona('vita_trio')
print(f'Loaded: {trio.display_name}')
print(f'Agents: {list(trio.roles.keys())}')
config = pm.create_agent_config('vita_trio', 'dolphin-2.1-mistral-7b')
print('✅ Configuration created successfully')
"
```

### Interactive Testing Steps

1. **Start Console Demo:**
   ```bash
   python vita_console_demo.py
   ```

2. **Test Persona Loading:**
   - Run console demo
   - Try loading different personas: `vita`, `liza`, `circuit`, `vita_trio`
   - Verify each loads without errors

3. **Test File Processing:**
   - Upload a Python file with syntax errors
   - Verify agents identify issues correctly
   - Check that responses match persona characteristics

## Testing Individual Personas

### Dr. LIZA (Visual/Animation Style)
```python
# Quick test for LIZA's animation metaphors
from persona_manager import PersonaManager
pm = PersonaManager()
liza = pm.get_persona('liza')
debugger_prompt = liza.roles['debugger'].system_prompt
assert 'frame' in debugger_prompt.lower() or 'animation' in debugger_prompt.lower()
print("✅ LIZA uses animation metaphors")
```

### Circuit (Detective Style)
```python
# Quick test for Circuit's detective language
circuit = pm.get_persona('circuit')
debugger_prompt = circuit.roles['debugger'].system_prompt
assert 'investigate' in debugger_prompt.lower() or 'clues' in debugger_prompt.lower()
print("✅ Circuit uses detective language")
```

### VITA Trio (Multi-Agent)
```python
# Quick test for Trio coordination
trio = pm.get_persona('vita_trio')
trio_data = str(trio.__dict__).lower()
assert 'coordinator' in trio_data and 'coder' in trio_data and 'cheerleader' in trio_data
print("✅ VITA Trio has all three agent roles")
```

## Performance Testing

### Response Time Test
```bash
# Time how long persona loading takes
time python -c "
from persona_manager import PersonaManager
pm = PersonaManager()
for persona in ['vita', 'liza', 'circuit', 'vita_trio']:
    config = pm.create_agent_config(persona, 'dolphin-2.1-mistral-7b')
    print(f'✅ {persona} config created')
"
```

### Model Compatibility Test
```bash
# Test different model configurations
python -c "
from persona_manager import PersonaManager
pm = PersonaManager()

# Test with different models
models = ['dolphin-2.1-mistral-7b', 'phi-4-mini-reasoning']
personas = ['vita', 'liza', 'circuit', 'vita_trio']

for persona in personas:
    for model in models:
        try:
            config = pm.create_agent_config(persona, model)
            print(f'✅ {persona} + {model}')
        except Exception as e:
            print(f'❌ {persona} + {model}: {e}')
"
```

## Real-World Testing Scenarios

### 1. Student With Syntax Error
Create test file `test_syntax_error.py`:
```python
print('Hello World'  # Missing closing parenthesis
x = 5
print(x
```

Upload via console demo and test each persona's response.

### 2. Student With Logic Error
Create test file `test_logic_error.py`:
```python
def calculate_average(numbers):
    total = 0
    for num in numbers:
        total += num
    return total / 0  # Division by zero error
```

### 3. Perfect Code Test
Create test file `test_perfect_code.py`:
```python
def greet(name):
    """Greet a person by name."""
    return f"Hello, {name}!"

if __name__ == "__main__":
    print(greet("Student"))
```

## Expected Behaviors

### VITA (Default)
- **Style**: Educational, encouraging, clear
- **Response**: "Line 1: Missing closing parenthesis. To fix this..."
- **Tone**: Patient teacher

### Dr. LIZA 
- **Style**: Animation/visual metaphors
- **Response**: "Looking at frame 1, your quote marks don't match - like a broken animation loop!"
- **Tone**: Artistic, visual

### Circuit
- **Style**: Detective/investigation 
- **Response**: "Found suspicious activity on line 1 - mismatched quotes detected!"
- **Tone**: Enthusiastic detective

### VITA Trio
- **Style**: Collaborative team
- **Response**: Coordinator opens, Coder finds issues, Cheerleader encourages, natural flow
- **Tone**: Supportive team

## Troubleshooting

### Common Issues

**"Persona not found":**
```bash
# Check available personas
python -c "
from persona_manager import PersonaManager
pm = PersonaManager()
print('Available personas:', pm.list_personas())
"
```

**"Model not found":**
```bash
# Check available models
python -c "
from persona_manager import PersonaManager
pm = PersonaManager()
print('Available models:', pm.list_models())
"
```

**LM Studio Connection Issues:**
- Ensure LM Studio is running on `localhost:1234`
- Check that a model is loaded in LM Studio
- Verify API is enabled in LM Studio settings

### Testing Without LM Studio
```bash
# Test with OpenAI API (requires API key)
export OPENAI_API_KEY="your-key-here"
python -c "
from persona_manager import PersonaManager
pm = PersonaManager()
config = pm.create_agent_config('vita', 'gpt-4o')
print('✅ OpenAI config created')
"
```

## Continuous Testing

### Pre-commit Testing
```bash
# Run before committing changes
python -m pytest tests/ --tb=short
```

### Development Testing
```bash
# Run with auto-reload during development
python -m pytest tests/ -v --tb=short -x
```

### Performance Monitoring
```bash
# Time all tests
time python -m pytest tests/ -v
```

## Next Steps for Testing

1. **Load Testing**: Test with multiple concurrent users
2. **Integration Testing**: Test full AutoGen group chat flows  
3. **User Experience Testing**: Test with actual students
4. **Performance Optimization**: Benchmark response times
5. **Error Recovery Testing**: Test handling of model failures

---

*Last updated: June 18, 2025*