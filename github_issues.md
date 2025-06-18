# GitHub Issues for VITA Panel MVP

## Critical Issues (P0 - Show Stoppers)

### Issue #001: Corrector Agent Infinite Empty Message Loop
**Priority:** P0 - Critical  
**Labels:** bug, show-stopper, agents  
**Description:** After initial response, Corrector agent sends empty messages indefinitely  
**Root Cause:** No empty message filtering in print_messages()  
**Fix:** Add content validation before sending to chat interface  

### Issue #002: No Error Handling for Offline LM Studio
**Priority:** P0 - Critical  
**Labels:** bug, error-handling, demo-risk  
**Description:** Application crashes when LM Studio is unavailable  
**Impact:** Demo failure if LM Studio crashes  
**Fix:** Wrap API calls in try-catch with user-friendly error messages  

### Issue #003: Multiple Concurrent Conversations Spawn
**Priority:** P0 - Critical  
**Labels:** bug, concurrency, agents  
**Description:** Rapid clicks create multiple agent conversations  
**Root Cause:** No conversation state management  
**Fix:** Implement single conversation enforcement  

## High Priority Issues (P1)

### Issue #004: No Agent Termination Conditions
**Priority:** P1 - High  
**Labels:** bug, agents, ux  
**Description:** Conversations continue indefinitely with no clear end  
**Fix:** Add termination after solution provided or max rounds  

### Issue #005: Missing UI Loading States
**Priority:** P1 - High  
**Labels:** enhancement, ux  
**Description:** No visual feedback during agent processing  
**Fix:** Add spinners and disable buttons during operations  

### Issue #006: Syntax Warning - String Comparison
**Priority:** P1 - High  
**Labels:** bug, code-quality  
**Description:** `if test is not ""` causes syntax warning  
**Status:** FIXED ✓  

## Medium Priority Issues (P2)

### Issue #007: LM Studio Performance Degradation
**Priority:** P2 - Medium  
**Labels:** performance, investigation  
**Description:** Higher latency compared to other local model implementations  
**Investigation:** Context length, API overhead, token limits  

### Issue #008: No Test Coverage
**Priority:** P2 - Medium  
**Labels:** testing, technical-debt  
**Description:** No unit or integration tests exist  
**Fix:** Implement test suite per user_stories_and_tests.md  

### Issue #009: Global State Management
**Priority:** P2 - Medium  
**Labels:** technical-debt, refactor  
**Description:** Multiple global variables create race conditions  
**Fix:** Refactor to proper state management  

## TRIAGE OPTION: Single Agent MVP

### Proposal: Simplify to Single Debugger Agent
**Pros:**
- Eliminates agent orchestration complexity
- Removes Corrector loop issue (#001)
- Reduces LM Studio API calls by 50%
- Simpler error handling
- Faster response times
- More predictable demo

**Cons:**
- Loses multi-agent teaching approach
- Less sophisticated interaction
- Reduces project scope

**Implementation Time:**
- Multi-agent fixes: 6-8 hours
- Single agent pivot: 2-3 hours

### Single Agent Architecture:
```python
# Simplified flow
1. Student uploads file
2. Student clicks debug
3. Debugger identifies ALL errors
4. Debugger provides guidance (combines both roles)
5. Conversation ends cleanly
```

## Metrics Summary
- **Total Issues:** 9
- **Critical (P0):** 3 (33%)
- **High (P1):** 3 (33%)
- **Medium (P2):** 3 (33%)
- **Fixed:** 4 (44%) ✅
- **Remaining Critical:** 0 ✅

### Fixed Issues
- ✅ **Issue #001**: Corrector agent empty message loop - RESOLVED
- ✅ **Issue #002**: LM Studio error handling - RESOLVED  
- ✅ **Issue #003**: Multiple conversation prevention - RESOLVED
- ✅ **Issue #006**: Syntax warning fix - RESOLVED

## Decision Matrix
| Option | Time | Risk | Demo Success % |
|--------|------|------|----------------|
| Fix All Critical | 6-8h | Medium | 70% |
| Single Agent MVP | 2-3h | Low | 90% |
| No Changes | 0h | Very High | 30% |

## Recommendation
Given 48-hour timeline, implement Single Agent MVP first (2-3 hours), then attempt multi-agent fixes with remaining time. This ensures a working demo with option to showcase advanced version.