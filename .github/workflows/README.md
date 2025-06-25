# GitHub Actions Workflows

## Active Workflows

### 1. `claude-code-review.yml` 🤖
**Purpose:** Automated code review using Claude Code CLI

**Triggers:**
- Pull request opened/updated (non-draft)
- Review requested

**Capabilities:**
- ✅ Comprehensive code review following FLOW methodology
- ✅ Security scanning for exposed secrets
- ✅ SOLID principles and best practices checking
- ✅ Educational framework integration review
- ✅ Automated comment posting with suggestions
- ✅ VIBE-powered encouragement and guidance

**Required Secrets:**
- `ANTHROPIC_API_KEY` - For Claude Code CLI access

**Review Standards:**
- 🔒 Security and best practices
- 🎯 Code quality and SOLID principles  
- 📚 Educational framework integration (FLOW/SAFE/VIBE)
- 🧪 Test coverage and documentation
- 🌊 FLOW methodology adherence

### 2. `flow-metrics.yml` 📊
**Purpose:** FLOW methodology metrics collection

**Triggers:**
- Issues opened/closed/labeled
- Pull requests opened/closed
- Manual dispatch

**Capabilities:**
- ✅ Cycle time calculation
- ✅ Lead time tracking
- ✅ Work-in-progress monitoring
- ✅ Flow efficiency metrics

## Workflow Integration

### FLOW Methodology Support
All workflows follow our educational principles:
- **F**un Learning Optimizes Wisdom
- **L**ogical work order prevents chaos
- **O**rganized structure enables creativity  
- **W**isdom emerges through consistent practice

### VIBE System Integration
Claude Code reviews include:
- **V**erify, and **I**nspirational **B**ehaviors **E**merge
- Encouraging feedback with embedded learning commands
- Educational fortune delivery
- Professional development guidance

### SAFE Framework
- **S**tructure that serves learning
- **A**lways creating better outcomes
- **F**rees creative potential
- **E**xcellence becomes inevitable

## Setup Instructions

### 1. Configure Repository Secrets
```bash
# Add to GitHub repository secrets
ANTHROPIC_API_KEY=sk-ant-api03-...
```

### 2. Enable Workflows
1. Navigate to repository Settings → Actions
2. Ensure "Allow all actions and reusable workflows" is selected
3. Workflows will auto-trigger on PR creation

### 3. Test Claude Code Review
1. Create a test PR
2. Verify Claude Code review comment appears
3. Check that security scans pass
4. Confirm FLOW methodology checks run

## Troubleshooting

### Claude Code Review Not Running
1. **Check API key:** Verify `ANTHROPIC_API_KEY` secret is set
2. **Check permissions:** Ensure workflow has PR write permissions
3. **Check triggers:** Only runs on non-draft PRs
4. **Check logs:** View Actions tab for detailed error logs

### Review Quality Issues
1. **Update context:** Modify `review_context.md` generation
2. **Adjust focus areas:** Update `--focus` parameters
3. **Refine prompts:** Enhance educational framework integration
4. **Check limits:** Verify API rate limits not exceeded

### Security Scan False Positives
1. **Update patterns:** Modify security scan regex patterns
2. **Add exclusions:** Use `--exclude-dir` for irrelevant directories
3. **Whitelist files:** Add exceptions for documentation

## Educational Value

### For Students
- **Learn from review feedback:** Claude provides educational explanations
- **Understand best practices:** Reviews highlight SOLID principles
- **See professional workflow:** Experience industry-standard review process

### For Instructors
- **Consistent review quality:** Automated standards enforcement
- **Educational integration:** Reviews reinforce course concepts
- **Time savings:** Pre-review filtering of common issues

### For Development Teams
- **Knowledge sharing:** Reviews capture institutional knowledge
- **Quality assurance:** Consistent application of standards
- **Continuous improvement:** Metrics inform process optimization

## Future Enhancements

### Planned Features
- **Live2D integration:** VIBE emotions drive avatar expressions
- **Multi-agent reviews:** Different agents for security, education, style
- **Learning analytics:** Track student improvement through review history
- **Custom educational prompts:** Course-specific review criteria

### Integration Opportunities
- **claude-conduit bridge:** Enhanced MCP server integration
- **VITA educational system:** Direct learning platform integration
- **Student portfolio:** Review feedback contributes to learning records

---

**"Verify, and Inspirational Behaviors Emerge"** - Our workflows model the professional practices we teach.

**teacherbot.help has a posse** 🎯