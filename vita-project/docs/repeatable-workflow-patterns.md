# Repeatable Workflow Patterns for VITA Students

## Overview
These patterns provide students with proven, step-by-step approaches to common programming tasks. Each pattern follows FLOW (Following Logical Work Order) methodology to ensure safe, repeatable success.

## Pattern Categories

### 1. Debugging Patterns

#### Pattern: Syntax Error Resolution
```yaml
Name: Fix-Syntax-Error
When to use: Code won't run due to syntax error
Safety level: High (no data loss risk)

FLOW Steps:
  1. LEARN:
     - Read the FULL error message
     - Identify the line number
     - Note the error type
  
  2. UNDERSTAND:
     - What was Python expecting?
     - What did it find instead?
     - Is this a common pattern?
  
  3. PLAN:
     - Check for missing colons
     - Verify parentheses/brackets match
     - Look for typos in keywords
  
  4. EXECUTE:
     - Make ONE change at a time
     - Save after each change
     - Keep original in comments
  
  5. VERIFY:
     - Run the code
     - Confirm error is gone
     - Check no new errors introduced
  
  6. DOCUMENT:
     - Comment what was wrong
     - Explain why fix works
     - Note for future reference
```

#### Pattern: Logic Error Investigation
```yaml
Name: Debug-Logic-Error
When to use: Code runs but gives wrong results
Safety level: Medium (test with sample data first)

FLOW Steps:
  1. LEARN:
     - Define expected vs actual behavior
     - Gather test cases
     - Identify where divergence occurs
  
  2. UNDERSTAND:
     - Trace through code mentally
     - Add print statements
     - Check variable values
  
  3. PLAN:
     - Isolate problem section
     - Design fix approach
     - Consider edge cases
  
  4. EXECUTE:
     - Implement fix incrementally
     - Test after each change
     - Keep working version safe
  
  5. VERIFY:
     - Test with original case
     - Test with edge cases
     - Verify no regressions
  
  6. DOCUMENT:
     - Explain the bug
     - Document the fix
     - Add test to prevent recurrence
```

### 2. Feature Implementation Patterns

#### Pattern: Add New Function
```yaml
Name: Implement-New-Function
When to use: Adding new functionality to existing code
Safety level: High (work in separate function)

FLOW Steps:
  1. LEARN:
     - Understand requirements
     - Study existing code style
     - Identify integration points
  
  2. UNDERSTAND:
     - What inputs are needed?
     - What output is expected?
     - What errors might occur?
  
  3. PLAN:
     - Write function signature
     - List implementation steps
     - Design test cases
  
  4. EXECUTE:
     - Write function skeleton
     - Implement core logic
     - Add error handling
  
  5. VERIFY:
     - Unit test the function
     - Integration test
     - Edge case testing
  
  6. DOCUMENT:
     - Add docstring
     - Include usage examples
     - Update project docs
```

#### Pattern: Refactor Existing Code
```yaml
Name: Safe-Refactor
When to use: Improving code without changing behavior
Safety level: Medium (requires careful testing)

FLOW Steps:
  1. LEARN:
     - Understand current behavior
     - Identify improvement goals
     - Review refactoring patterns
  
  2. UNDERSTAND:
     - Map all code dependencies
     - Document current behavior
     - Write characterization tests
  
  3. PLAN:
     - Choose refactoring technique
     - Plan incremental steps
     - Set rollback points
  
  4. EXECUTE:
     - Make small changes
     - Run tests frequently
     - Commit working states
  
  5. VERIFY:
     - All tests still pass
     - Performance acceptable
     - Code is clearer
  
  6. DOCUMENT:
     - Explain what changed
     - Show before/after
     - Update affected docs
```

### 3. Learning Patterns

#### Pattern: Understand New Concept
```yaml
Name: Learn-New-Concept
When to use: Encountering unfamiliar programming concept
Safety level: High (learning only)

FLOW Steps:
  1. LEARN:
     - Find 3 different explanations
     - Watch video tutorial
     - Read official documentation
  
  2. UNDERSTAND:
     - Explain in own words
     - Draw diagram/flowchart
     - Find real-world analogy
  
  3. PLAN:
     - Design simple experiment
     - Create minimal example
     - List variations to try
  
  4. EXECUTE:
     - Code minimal example
     - Try variations
     - Break it intentionally
  
  5. VERIFY:
     - Can explain to others
     - Can apply to new problem
     - Understand limitations
  
  6. DOCUMENT:
     - Create personal notes
     - Build example library
     - Share with study group
```

#### Pattern: Review Code
```yaml
Name: Peer-Code-Review
When to use: Reviewing another student's code
Safety level: High (read-only activity)

FLOW Steps:
  1. LEARN:
     - Understand the requirements
     - Read through code once
     - Note initial impressions
  
  2. UNDERSTAND:
     - Trace execution path
     - Check logic flow
     - Verify requirements met
  
  3. PLAN:
     - List improvements
     - Prioritize feedback
     - Frame constructively
  
  4. EXECUTE:
     - Add inline comments
     - Suggest alternatives
     - Highlight good practices
  
  5. VERIFY:
     - Feedback is helpful
     - Tone is encouraging
     - Suggestions are clear
  
  6. DOCUMENT:
     - Summarize key points
     - Provide resources
     - Offer follow-up help
```

### 4. Problem-Solving Patterns

#### Pattern: Break Down Complex Problem
```yaml
Name: Decompose-Problem
When to use: Facing overwhelming/complex task
Safety level: High (planning phase)

FLOW Steps:
  1. LEARN:
     - Read full requirements
     - Identify all components
     - Note dependencies
  
  2. UNDERSTAND:
     - What's the core problem?
     - What are constraints?
     - What's negotiable?
  
  3. PLAN:
     - Divide into sub-problems
     - Order by dependency
     - Estimate complexity
  
  4. EXECUTE:
     - Solve simplest first
     - Build incrementally
     - Test each component
  
  5. VERIFY:
     - Components work alone
     - Integration successful
     - Meets requirements
  
  6. DOCUMENT:
     - Explain decomposition
     - Show component diagram
     - Note lessons learned
```

## Pattern Selection Guide

### When debugging:
- Syntax Error? → Use `Fix-Syntax-Error`
- Wrong Output? → Use `Debug-Logic-Error`
- Not Sure? → Use `Safe-Practice` environment first

### When building:
- New Feature? → Use `Implement-New-Function`
- Improving Code? → Use `Safe-Refactor`
- Complex Task? → Use `Decompose-Problem`

### When learning:
- New Topic? → Use `Learn-New-Concept`
- Help Others? → Use `Peer-Code-Review`
- Practice Safely? → Use sandbox patterns

## Creating Your Own Patterns

Students are encouraged to document their own successful patterns:

1. **Identify** repeated successful approaches
2. **Document** the steps you followed
3. **Test** pattern with new problem
4. **Refine** based on results
5. **Share** with classmates
6. **Iterate** based on feedback

## Pattern Anti-Patterns (What NOT to Do)

### ❌ Skip-to-Execute
- Jumping straight to coding
- Missing understanding phase
- No plan = more debugging

### ❌ Change-Everything
- Making multiple changes at once
- Can't identify what fixed issue
- Introduces new bugs

### ❌ No-Document
- Solving without recording
- Can't remember solution later
- Others can't learn from you

### ❌ Work-in-Production
- Testing on live data
- No rollback plan
- Risk of data loss

## Success Metrics

A pattern is working when:
- ✅ You complete tasks faster each time
- ✅ Fewer errors on subsequent uses
- ✅ You can adapt it to new situations
- ✅ You can teach it to others
- ✅ It becomes second nature

## Remember

> "The goal isn't to memorize patterns, but to understand why they work and when to apply them."

Every expert was once a beginner who learned to recognize patterns and apply them appropriately!