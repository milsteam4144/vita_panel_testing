# VITA Memory Store

A simple JSON-based memory store for the VITA Panel Testing system. This component provides synthetic dummy data for testing the memory functionality described in issues #7 and #10.

## Overview

The memory store contains synthetic educational data that simulates student-teacher interactions without using any real student PII (Personally Identifiable Information). This allows safe testing of the memory store functionality.

## Files

- `memory_store.py`: Core memory store functionality for loading, saving, and accessing interaction data
- `data/dummy_data.json`: Synthetic dummy data with 10 realistic student-teacher interactions
- `test_memory_store.py`: Comprehensive test suite validating data quality and functionality
- `example_integration.py`: Demonstration of how to integrate the memory store with VITA panel

## Dummy Data Structure

Each interaction in the memory store contains:

```json
{
  "assignment_id": "intro_001_loops",
  "code_snippet": "for i in range(5)\n    print(i)",
  "student_prompt": "My for loop isn't working. I keep getting a syntax error...",
  "teacher_response": "I can see you're working with a for loop - that's great!..."
}
```

### Fields Description

- **assignment_id**: Anonymized identifier (e.g., "intro_001_loops") with no student PII
- **code_snippet**: Python code containing realistic beginner errors
- **student_prompt**: Authentic-sounding questions students might ask for help
- **teacher_response**: Pedagogical responses that guide students without giving direct answers

## Quick Start

```python
from memory_store import MemoryStore

# Initialize the memory store
store = MemoryStore()

# Get all interactions
interactions = store.get_all_interactions()
print(f"Loaded {store.get_interactions_count()} interactions")

# Get a specific interaction
interaction = store.get_interaction_by_id("intro_001_loops")
print(interaction["teacher_response"])
```

## Testing

Run the comprehensive test suite:

```bash
python3 test_memory_store.py
```

This validates:
- Data structure integrity
- Required field presence
- Data quality (realistic prompts, pedagogical responses)
- Unique assignment IDs
- Code snippet validity

## Integration Example

Run the integration demo:

```bash
python3 example_integration.py
```

This demonstrates how the memory store can:
- Find similar code examples based on student input
- Provide consistent pedagogical response styles
- Support contextual help in the VITA chat interface

## Data Quality Standards

The synthetic data follows these guidelines:

1. **No Real PII**: All assignment IDs are generic (e.g., "intro_001_loops")
2. **Realistic Errors**: Code snippets contain common beginner Python mistakes
3. **Authentic Questions**: Student prompts sound like real help requests
4. **Pedagogical Responses**: Teacher responses guide rather than solve directly
5. **Educational Focus**: All examples target fundamental Python concepts

## Educational Topics Covered

The dummy data includes examples for:
- For loops and while loops
- Conditionals (if/else statements)  
- Variables and string operations
- Functions and method calls
- Lists and dictionaries
- File handling basics
- Common syntax errors

## Future Enhancements

Potential improvements for the memory store:
- Search and similarity matching algorithms
- Integration with existing autogen agents
- User session tracking
- Performance analytics
- More sophisticated data structures

## Safety Notes

- All data is synthetic and contains no real student information
- Safe for development, testing, and demonstration purposes
- Designed to support educational use cases without privacy concerns