# VITA Panel Test Protocol

## Pre-Commit Protocol (MANDATORY)

**Before every commit, run the following sequence:**

### 1. Run All Tests
```bash
# Activate environment
source venv/bin/activate

# Run test suite
pytest tests/ -v

# Check coverage (optional but recommended)
pytest tests/ --cov=. --cov-report=term-missing
```

### 2. Manual Smoke Test
```bash
# Test console version (when available)
python vita_console_demo.py

# Quick Panel test (30 seconds max)
panel serve test.py --show
# Upload test file, click debug, verify no crashes
```

### 3. Code Quality Check
```bash
# Check for syntax issues
python -m py_compile test.py
python -m py_compile main_test.py

# Optional: Run linting
black --check .
flake8 --max-line-length=100 .
```

### 4. Git Commit
```bash
# Only if all tests pass
git add .
git commit -m "descriptive message with issue numbers"
# DO NOT PUSH until tests pass
```

## Test Categories

### Unit Tests (Fast - <1 second each)
- File upload processing
- Message filtering 
- Agent configuration
- Environment handling

### Integration Tests (Medium - <10 seconds each)
- Agent interaction flow
- Error handling paths
- Configuration switching

### Console Tests (Fast - <5 seconds)
- Full conversation flow
- File processing end-to-end
- Error scenarios

### Manual Tests (Quick - <2 minutes)
- Panel UI basic flow
- LM Studio connectivity
- File upload/debug cycle

## Test Data

### Standard Test Files
```python
# tests/test_data/valid_code.py
print("hello world")

# tests/test_data/syntax_error.py  
print("hello world'  # Missing closing quote

# tests/test_data/empty_file.py
# (empty file)

# tests/test_data/large_file.py
# (100+ lines for performance testing)
```

## Continuous Integration

When GitHub Actions is set up:
```yaml
# .github/workflows/test.yml
- name: Run Tests
  run: |
    pytest tests/ -v
    python vita_console_demo.py < tests/test_input.txt
```

## Protocol Enforcement

**REMEMBER**: 
- 🚫 **No commits without passing tests**
- 🚫 **No pushes without protocol completion**  
- ✅ **Always run full protocol before demo**
- ✅ **Document any test failures in commit message**

This protocol ensures we never break the main branch and always have a working demo.