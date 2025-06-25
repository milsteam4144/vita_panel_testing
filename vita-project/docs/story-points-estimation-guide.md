# Story Points & Estimation Guide for Students

## Learning Objectives
By the end of this guide, students will:
- Understand what story points represent
- Learn multiple estimation techniques
- Practice estimating their own work
- Improve estimation accuracy over time
- Use estimates for planning and reflection

## What Are Story Points?

Story points are a unit of measure for expressing the **effort** required to complete a task. They consider:
- **Complexity**: How hard is the problem?
- **Uncertainty**: How much do we understand?
- **Effort**: How much work is involved?

### Key Principles
- Points are **relative**, not absolute
- Compare to previous tasks, not hours
- Include learning time for new concepts
- Account for debugging and testing

## The Fibonacci Scale

We use: **1, 2, 3, 5, 8, 13, 21**

### What Each Number Means:

**1 Point** - Trivial
- Fix a typo
- Add a comment
- Change a variable name
- 15-30 minutes

**2 Points** - Simple
- Small bug fix
- Add print statement for debugging
- Write a basic test
- 30-60 minutes

**3 Points** - Straightforward
- Implement simple function
- Write multiple test cases
- Refactor small section
- 1-2 hours

**5 Points** - Moderate
- New feature with multiple steps
- Debug complex logic error
- Write integration test
- 2-4 hours

**8 Points** - Complex
- Multi-file changes
- Learn new concept and apply
- Significant refactoring
- 4-8 hours

**13 Points** - Very Complex
- Major feature implementation
- Research and prototype
- Multiple integration points
- 1-2 days

**21 Points** - Epic
- Break this down into smaller tasks!
- Too big to estimate accurately
- Should be multiple stories

## FLOW-Based Estimation Process

### 1. LEARN - Understand the Task
```markdown
Before estimating, answer:
- What exactly needs to be done?
- What are the acceptance criteria?
- What technologies are involved?
- What might go wrong?
```

### 2. UNDERSTAND - Compare to Known Work
```markdown
Think of similar tasks you've done:
- "This is like [previous task] but with X added"
- "I've never done Y before, so add uncertainty"
- "This touches the same code as [difficult task]"
```

### 3. PLAN - Break Down if Needed
```markdown
If > 8 points, break into smaller pieces:
- What are the main steps?
- Which parts are unknown?
- What can be done independently?
```

### 4. EXECUTE - Make Your Estimate
```markdown
Choose the closest Fibonacci number:
- When in doubt, round up
- Include time for testing
- Add points for learning curve
```

### 5. VERIFY - Validate with Others
```markdown
Estimation is a team activity:
- Compare with teammates
- Discuss differences
- Reach consensus
```

### 6. DOCUMENT - Track Actual vs Estimate
```markdown
After completion:
- How long did it actually take?
- What made it harder/easier?
- How to improve next estimate?
```

## Estimation Techniques

### 1. Planning Poker (Team Estimation)
```markdown
1. Read the story aloud
2. Everyone estimates privately
3. Reveal estimates simultaneously
4. Discuss differences
5. Re-estimate until consensus
```

### 2. T-Shirt Sizing (Quick Estimates)
```markdown
XS = 1 point
S  = 2 points  
M  = 3 points
L  = 5 points
XL = 8 points
XXL = 13 points
```

### 3. Comparative Estimation
```markdown
Sort stories by relative complexity:
- Start with a known baseline
- "This is bigger than X but smaller than Y"
- Assign points based on position
```

### 4. Wideband Delphi
```markdown
1. Initial individual estimates
2. Share reasoning (not numbers)
3. Re-estimate individually
4. Repeat until convergence
```

## Common Estimation Mistakes

### ❌ Estimating in Hours
- Hours vary by person and day
- Hard to compare across team
- Creates pressure and stress

### ❌ Being Too Precise
- "This is exactly 4.5 points"
- Precision implies false accuracy
- Use the Fibonacci scale

### ❌ Ignoring Uncertainty
- "I think I know how to do this"
- New concepts take longer
- Always add buffer for unknowns

### ❌ Forgetting Testing
- Code + tests + debugging
- Include time for verification
- Account for integration issues

### ❌ Individual Estimation
- Team estimates are more accurate
- Different perspectives help
- Builds shared understanding

## Educational Estimation Exercises

### Exercise 1: Calibration
```markdown
Estimate these common programming tasks:
- [ ] Write a function to add two numbers
- [ ] Debug a for-loop that's infinite
- [ ] Implement bubble sort from scratch
- [ ] Connect to a database
- [ ] Write unit tests for a class

Then do them and compare actual vs estimate!
```

### Exercise 2: Historical Analysis
```markdown
Look at your last 10 completed issues:
- What was your estimate?
- How long did it actually take?
- What patterns do you notice?
- Where were you most/least accurate?
```

### Exercise 3: Team Calibration
```markdown
With your study group:
1. Pick 5 upcoming tasks
2. Estimate individually
3. Compare estimates
4. Discuss differences
5. Try consensus estimation
```

## Tracking Your Estimation Skills

### Weekly Reflection
```markdown
This week I:
- Estimated X tasks
- Was accurate on Y of them
- Consistently underestimated: [pattern]
- Consistently overestimated: [pattern]
- Learned: [insight]
```

### Improvement Metrics
- **Accuracy**: How often within 1 point of actual?
- **Consistency**: Do similar tasks get similar estimates?
- **Learning**: Are estimates improving over time?

## Using Estimates for Planning

### Sprint Planning
```markdown
If your velocity is 15 points per week:
- Choose 12-15 points of work
- Leave buffer for unexpected issues
- Include mix of sizes
```

### Personal Planning
```markdown  
For your study schedule:
- 1-2 points = Quick wins
- 3-5 points = Main focus tasks
- 8+ points = Break down first
```

## Template: Estimation in Issues

Add this to your issue templates:

```markdown
## Estimation

### Initial Estimate: [X] points

**Reasoning:**
- Similar to: [reference task]
- Complexity factors: [list]
- Uncertainty factors: [list]
- Includes: [scope]

### Actual Effort: [Y] points (after completion)

**Reflection:**
- What took longer than expected?
- What was easier than expected?
- How to improve next estimate?
```

## Advanced Techniques

### Velocity Tracking
```markdown
Track your team's velocity:
- Week 1: 12 points completed
- Week 2: 15 points completed  
- Week 3: 11 points completed
- Average: 12.7 points/week
```

### Estimation Confidence
```markdown
Add confidence levels:
- Estimate: 5 points
- Confidence: 70%
- Meaning: "Could be 3-8 points"
```

### Risk-Adjusted Estimation
```markdown
Base estimate: 5 points
Risk factors:
- New technology: +2 points
- Complex integration: +1 point
- Time pressure: +1 point
Final estimate: 9 points → 8 points
```

## Remember

> "Estimates are not commitments - they're learning tools."

### Key Takeaways:
1. **Estimation is a skill** - improves with practice
2. **Team estimates are better** - different perspectives help
3. **Track and reflect** - learn from your patterns
4. **Embrace uncertainty** - it's normal and valuable
5. **Focus on learning** - not perfect predictions

The goal is to get better at planning your learning and work, not to predict the future perfectly!