# Sprint-Based Learning Workflow for VITA Students

## Overview
Students work in 1-2 week sprints using FLOW methodology and SAFE principles. Each sprint includes planning, daily implementation with protected focus time, and retrospective learning.

> "Plan once, implement many, reflect and improve."

## Sprint Structure

### Sprint Cadence Options

#### **Option A: 1-Week Sprints** (Recommended for beginners)
```
Monday: Sprint Planning (2 hours)
Tue-Thu: Implementation Days 
Friday: Demo + Retrospective + Next Sprint Planning (2 hours)
```

#### **Option B: 2-Week Sprints** (For advanced students)
```
Week 1 Monday: Sprint Planning (2 hours)
Week 1-2: Implementation Days (8-9 days)
Week 2 Friday: Demo + Retrospective + Next Sprint Planning (3 hours)
```

## The Sprint Workflow

### 🎯 Sprint Planning Session (PLAN Multiple Issues)
**Duration:** 1.5-3 hours
**Participants:** Student + Mentor/Study Group
**Environment:** 🟢 Green Light - Collaborative planning

#### FLOW Steps for Sprint Planning:
1. **LEARN**: Review learning goals and available time
2. **UNDERSTAND**: Assess current skills and knowledge gaps  
3. **PLAN**: Select and break down issues for the sprint

#### Planning Activities:
- [ ] Review previous sprint outcomes
- [ ] Assess available capacity (hours/week)
- [ ] Select learning objectives that fit sprint goal
- [ ] Break down large tasks into manageable issues
- [ ] Estimate story points for each issue
- [ ] Create acceptance criteria
- [ ] Identify learning resources needed
- [ ] Plan daily work schedule

#### Sprint Planning Output:
```markdown
## Sprint Goal
What I want to achieve: _______________

## Sprint Backlog (Selected Issues)
1. [Issue #X] Learn Python classes (5 points)
2. [Issue #Y] Build calculator with OOP (8 points)  
3. [Issue #Z] Write unit tests for calculator (3 points)
Total: 16 points

## Learning Focus
Primary: Object-Oriented Programming
Secondary: Test-Driven Development

## Success Metrics
- Complete 80% of planned story points
- Can explain OOP concepts to another student
- Working, tested code in repository

## Daily Schedule
Monday: Planning
Tuesday: Issue #X (classes)
Wednesday: Issue #Y (calculator part 1)
Thursday: Issue #Y (calculator part 2) 
Friday: Issue #Z (testing) + retrospective
```

---

### 🔨 Daily Implementation (EXECUTE Individual Issues)
**Duration:** 2-4 hours focused work per day
**Environment:** 🟡/🔴 Yellow/Red Light - Protected focus time

#### Daily FLOW Pattern:
Each day, for each issue you work on:

1. **LEARN**: Review issue requirements and gather resources
2. **UNDERSTAND**: Clarify what needs to be built
3. **PLAN**: Break today's work into 2-3 hour chunks
4. **EXECUTE**: Implement with frequent commits
5. **VERIFY**: Test your work
6. **DOCUMENT**: Update issue with progress, learnings

#### Daily Structure:
```
9:00-9:30   🟢 Daily standup (what did I learn yesterday, what will I work on today, any blockers)
9:30-12:00  🔴 Deep Work Block 1 (2.5 hours)
12:00-1:00  Break
1:00-3:30   🔴 Deep Work Block 2 (2.5 hours)  
3:30-4:00   🟡 Update issues, commit work, plan tomorrow
```

#### Issue Progression During Sprint:
- **Day 1**: Learn + Understand + Plan the issue
- **Day 2-3**: Execute implementation
- **Day 4**: Verify + Document + Move to next issue

---

### 📈 Sprint Review & Retrospective
**Duration:** 1-2 hours
**Environment:** 🟢 Green Light - Collaborative reflection

#### Sprint Review (What We Built):
- [ ] Demo completed work
- [ ] Review each issue's outcomes
- [ ] Celebrate successes
- [ ] Identify incomplete work
- [ ] Update learning portfolio

#### Sprint Retrospective (How We Worked):
1. **What went well?** (Keep doing)
2. **What was challenging?** (Improve)
3. **What did we learn?** (Knowledge gained)
4. **What should we try next sprint?** (Experiments)

## FOCUS System in Sprints

### Sprint Planning Day: 🟢 Green Light All Day
- Collaboration encouraged
- Questions and discussion welcome
- Mentor/peer input valuable
- Brainstorming and exploration

### Implementation Days: Mixed Lights
- **Morning Standup:** 🟢 Green (15 minutes)
- **Deep Work Blocks:** 🔴 Red (2-3 hours each)
- **Breaks:** 🟢 Green (social, questions)
- **End of Day Updates:** 🟡 Yellow (brief check-ins)

### Retrospective Day: 🟢 Green Light
- Reflection and sharing
- Learning from each other
- Planning improvements
- Celebrating progress

## Sprint Artifacts

### 1. Sprint Backlog (GitHub Project Board)
```
| To Do | In Progress | Review | Done |
|-------|------------|--------|------|
| Issue #3 | Issue #1 | Issue #2 | ✅ |
| Issue #4 |          |        | ✅ |
```

### 2. Daily Learning Log (Issue Comments)
```markdown
## Day 2 Progress on Issue #123

### What I accomplished:
- Completed user input validation
- Added error handling for edge cases

### What I learned:
- Try/catch blocks are essential for robust code
- Input validation should happen early

### Challenges faced:
- Regex syntax took longer than expected
- Found good tutorial: [link]

### Tomorrow's plan:
- Implement the calculation logic
- Add unit tests

### Time logged: 4.5 hours
### Confidence level: Medium
```

### 3. Sprint Burndown (Story Points)
Track remaining story points each day:
```
Day 1: 20 points remaining
Day 2: 17 points remaining  
Day 3: 12 points remaining
Day 4: 8 points remaining
Day 5: 3 points remaining
```

## Issue Management in Sprints

### Issue Lifecycle:
1. **Created during Sprint Planning** with clear acceptance criteria
2. **Assigned to Sprint Milestone**
3. **Worked on during Implementation Days**
4. **Updated daily** with progress and learnings
5. **Closed when complete** with reflection

### Issue Types for Learning:
- **Learning Objective**: "Learn Python decorators"
- **Implementation Task**: "Build user authentication system"  
- **Practice Exercise**: "Solve 5 algorithm problems"
- **Research Spike**: "Investigate best testing frameworks"

### Draft PR Workflow:
1. **Start of Sprint**: Create feature branch
2. **Day 1**: Open Draft PR with implementation plan
3. **Daily**: Commit progress with clear messages
4. **End of Sprint**: Convert to Ready for Review
5. **Retrospective**: Merge or plan continuation

## Educational Benefits

### For Students:
- **Sustainable Pace**: Avoid burnout with planned work
- **Clear Progress**: Visible advancement each sprint
- **Learning Focus**: Concentrated effort on specific skills
- **Professional Practice**: Real-world agile experience
- **Protected Time**: Deep work without constant interruption

### For Mentors:
- **Predictable Support**: Know when students need help
- **Batch Guidance**: Focused planning and review sessions
- **Quality Mentoring**: Deeper conversations during reviews
- **Scalable Teaching**: Support multiple students efficiently

### For Study Groups:
- **Synchronized Learning**: Work on related topics together
- **Peer Support**: Help each other during implementation
- **Shared Retrospectives**: Learn from each other's experiences
- **Collaborative Planning**: Choose complementary learning paths

## Sprint Patterns

### **Learning Sprint** (New Concepts)
- Focus: Understanding and practicing new skills
- Issues: Tutorials, exercises, small projects
- Success: Can explain concepts and apply them

### **Project Sprint** (Building Something)
- Focus: Creating a working application or feature
- Issues: Design, implement, test, deploy
- Success: Working software that meets requirements

### **Practice Sprint** (Skill Building)
- Focus: Repetition and pattern recognition
- Issues: Algorithm practice, code challenges, refactoring
- Success: Improved speed and confidence

### **Research Sprint** (Exploration)
- Focus: Investigating technologies or approaches
- Issues: Spikes, prototypes, comparisons
- Success: Clear understanding of options and recommendations

## Common Sprint Anti-Patterns

### ❌ Over-Planning
- Planning for more than 2 weeks out
- Too much detail in distant future
- Trying to plan every learning moment

### ❌ Under-Planning  
- No clear sprint goal
- Vague acceptance criteria
- No time estimates

### ❌ Scope Creep
- Adding new issues mid-sprint
- Expanding existing issues
- Changing goals without replanning

### ❌ No Protection
- Constant interruptions during deep work
- No respect for Red Light status
- Meetings during implementation time

## Getting Started

### Your First Sprint:
1. **Choose 1-week sprints** to start
2. **Pick 3-5 small issues** (total 10-15 story points)
3. **Focus on one learning area** (don't spread too thin)
4. **Plan your daily schedule** with protected time
5. **Find an accountability partner** or mentor
6. **Track everything** for retrospective learning

### Sprint 0 (Setup Sprint):
- Set up development environment
- Create GitHub repository structure
- Learn the FLOW methodology
- Practice estimation on small tasks
- Establish daily routine

## Remember

> "Sprints are not about going fast - they're about going at a sustainable pace in the right direction."

### Key Principles:
1. **Plan together, work alone** - Collaborative planning, protected implementation
2. **Commit to the sprint** - Honor your commitments to yourself and team
3. **Reflect and adapt** - Use retrospectives to improve your process
4. **Protect the focus** - Respect Red Light time for yourself and others
5. **Celebrate progress** - Acknowledge learning and growth each sprint

**Start your first learning sprint this week. Notice how much more you accomplish with structure and protection.**