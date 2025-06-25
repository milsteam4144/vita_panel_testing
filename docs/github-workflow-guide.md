# VITA GitHub Workflow Guide

## FLOW (Following Logical Work Order) & SAFe Implementation

### Overview
This guide demonstrates how to implement FLOW (Following Logical Work Order) principles with SAFe methodology, creating repeatable, modelable processes that students can learn and apply safely.

## FLOW Principles

### Core Tenets
1. **Logical Sequence**: Every task follows a clear, logical order
2. **Repeatability**: Processes can be repeated with consistent results
3. **Modelability**: Students can observe, learn, and replicate workflows
4. **Safety**: Built-in checkpoints prevent errors and ensure quality

## Work Item Types (Following Logical Order)

### 1. Learning Objectives (Epics)
- Define what students will learn
- Break down into teachable components
- Create clear success criteria
- Link to educational outcomes

### 2. Learning Activities (User Stories)
- Step-by-step tasks students complete
- Clear prerequisites and outcomes
- Follows "Learn → Practice → Apply" pattern
- Measurable progress indicators

### 3. Foundation Work (Enablers)
- Setup and configuration tasks
- Knowledge prerequisites
- Tool familiarization
- Safety checks and validations

## FLOW Process Steps

### The Logical Work Order
1. **Understand** - Read and comprehend the task
2. **Plan** - Break down into logical steps
3. **Prepare** - Gather resources and tools
4. **Execute** - Follow the plan step-by-step
5. **Verify** - Check work against criteria
6. **Document** - Record learnings and results
7. **Reflect** - Consider improvements

## GitHub Implementation for FLOW

### Project Board - Following Logical Order
```
┌─────────────┬──────────────┬──────────────┬──────────────┬──────────────┬──────────────┐
│   Learn     │  Understand  │    Plan      │   Execute    │   Verify     │   Complete   │
│  (Step 1)   │  (Step 2)    │  (Step 3)    │  (Step 4)    │  (Step 5)    │  (Step 6)    │
└─────────────┴──────────────┴──────────────┴──────────────┴──────────────┴──────────────┘
```

### Column Definitions
1. **Learn**: New concepts to study
2. **Understand**: Tasks being comprehended
3. **Plan**: Breaking down into steps
4. **Execute**: Active implementation
5. **Verify**: Testing and validation
6. **Complete**: Documented and reflected

## Safe Learning Process

### 1. Creating Learning Objectives (Epics)
```markdown
# Template for Educational Epic
Title: [LEARN] Master Python Debugging Techniques
Body:
- Learning Outcome: Students will debug Python code effectively
- Prerequisites: Basic Python knowledge
- Success Criteria: Can identify and fix 5 types of errors
- Safety Checks: Practice in sandbox environment first
```

### 2. Designing Learning Activities (Stories)
```markdown
# Template for Learning Activity
Title: [ACTIVITY] Debug a syntax error in student code
Body:
- Step 1: LEARN - Review Python syntax rules
- Step 2: UNDERSTAND - Analyze the error message
- Step 3: PLAN - Identify potential fixes
- Step 4: EXECUTE - Apply the correction
- Step 5: VERIFY - Run tests to confirm fix
- Step 6: DOCUMENT - Explain why the fix works
```

### 3. Following the Logical Work Order
```yaml
For each GitHub issue:
  1. Start in "Learn" column
  2. Move to "Understand" when concept is grasped
  3. Progress to "Plan" with clear steps outlined
  4. Advance to "Execute" only after plan approval
  5. Enter "Verify" with defined test criteria
  6. Complete with documentation and reflection
```

### 4. Safe Execution Pattern
```markdown
Before moving any issue forward:
- ✓ Prerequisites met?
- ✓ Resources available?
- ✓ Safety checks passed?
- ✓ Mentor/peer review completed?
- ✓ Rollback plan defined?
```

### 5. Repeatable Process Documentation
```markdown
Every completed task must include:
1. Step-by-step guide for reproduction
2. Common pitfalls and how to avoid them
3. Troubleshooting checklist
4. Links to learning resources
5. Student feedback incorporated
```

## Educational Ceremonies in GitHub

### Learning Module Planning
- Create milestones for each learning module
- Define clear learning objectives
- Map prerequisite knowledge
- Set measurable outcomes

### Weekly Learning Checkpoint
- Review student progress in GitHub Projects
- Identify common struggle points
- Adjust teaching approach based on data
- Celebrate completed learning objectives

### Daily Reflection
- Students comment on their learning journey
- Share "aha!" moments in discussions
- Ask for help when stuck
- Peer support and collaboration

### Module Completion Review
- Students demonstrate mastery
- Portfolio pieces added to repos
- Knowledge gaps identified
- Next learning path recommended

### Continuous Improvement
- Gather student feedback via issues
- Refine learning materials
- Update based on common errors
- Share success patterns

## Best Practices for Educational FLOW

### Learning Issue Management
1. One issue = one learning objective
2. Clear success criteria for mastery
3. Difficulty labels (beginner/intermediate/advanced)
4. Prerequisite links clearly marked
5. Progress updates with reflections

### Code Submission Guidelines
1. Working code with comments explaining logic
2. Test cases demonstrating understanding
3. README explaining approach
4. Reflection on what was learned
5. Questions for further exploration

### Safe Learning Environment
1. Sandbox branches for experimentation
2. No fear of "breaking things"
3. Peer code reviews for learning
4. Mentorship through PR comments
5. Celebrate attempts, not just successes

### Repeatable Success Patterns
1. Document what works
2. Create templates from successful approaches
3. Share debugging strategies
4. Build a knowledge base
5. Iterate based on outcomes

## Automation

### GitHub Actions for FLOW
- Automatic cycle time calculation
- WIP limit enforcement
- Stale issue management
- Automated labeling
- Metrics dashboard updates

### Integration Points
- Taskmaster-AI for task breakdown
- MCP servers for automation
- External dashboards for metrics
- Slack notifications for updates

## Example Issue Creation

```markdown
## Epic Example
Title: [EPIC] Multi-Agent System Enhancement
Labels: epic, safe, PI-1
Body:
- Business Value: Enable personalized learning experiences
- WSJF Score: 15.5
- Features: Agent personas, PRISM framework, Memory system

## Story Example
Title: [STORY] As a student I want multiple AI tutors So that I can get specialized help
Labels: story, flow, 5-points
Body:
- Given a complex programming problem
- When I request help
- Then I receive guidance from the most appropriate AI tutor
```

## Metrics Dashboard

Track these metrics weekly:
- Average cycle time per story type
- Flow efficiency percentage
- WIP vs throughput
- Blocker frequency
- Team velocity trends

## The FLOW Philosophy

Remember: FLOW means Following Logical Work Order
- Every step builds on the previous one
- No skipping ahead without mastery
- Safety checks prevent costly mistakes
- Documentation enables others to follow
- Success is measured by reproducibility

> "If a student can't replicate your process, it's not truly educational."

### Student Success Metrics
- Can they explain each step?
- Can they teach it to others?
- Can they adapt it to new problems?
- Do they know when they need help?
- Are they building confidence?