Generate a comprehensive weekly summary with completed work, key notes, and planning.

Perfect for weekly updates, stand-ups, or personal reflection!

## Step 1: Gather Data

```bash
# Work logs for the week
sb log show --days 7

# All tasks (we'll filter for completed ones)
sb task list

# Recent notes
sb note list

# Epic/issue stats
sb issue stats

# Weekly work report
sb report work --days 7
```

## Step 2: Analyze Completions

**Help them identify completed work:**

```bash
# Tasks completed this week (check for status=done and completed_at in last 7 days)
sb task list --status done

# Closed issues
sb issue list --status closed --limit 20

# By project
sb project status PROJECT_SLUG
```

## Step 3: Review Important Notes

```bash
# Notes from this week (check created_at)
# We'll manually filter recent ones from the list

# Key decisions
sb note list --tags decision

# Search for specific topics
sb note search "implemented"
sb note search "decided"
```

## Step 4: Generate Summary

Create a comprehensive weekly summary note:

```bash
sb note create "Weekly Summary - Week of $(date +%Y-%m-%d)" \
  --tags weekly,summary,review \
  --content "# Weekly Summary - $(date '+%B %d, %Y')

## 📊 Stats at a Glance

**Time Logged:** [Calculate from work logs]
- Monday: Xh
- Tuesday: Xh
- Wednesday: Xh
- Thursday: Xh
- Friday: Xh
- **Total:** XXh

**Tasks Completed:** X
**Issues Closed:** X
**Notes Created:** X
**Projects Active:** X

## ✅ Completed Work

### Major Achievements

1. **[Task/Feature Name]** (#TASK_ID)
   - Project: [PROJECT]
   - Time spent: Xh
   - Key outcome: [What was delivered]

2. **[Another Task]** (#TASK_ID)
   - Project: [PROJECT]
   - Time spent: Xh
   - Key outcome: [What was delivered]

### Bug Fixes

- Fixed [Bug description] (#TASK_ID)
- Resolved [Another bug] (#TASK_ID)

### Other Completed Tasks

- [Quick wins and smaller tasks]

## 🔄 In Progress

### Active Work

1. **[Feature Name]** (#TASK_ID) - 60% complete
   - Status: [Current state]
   - Next steps: [What's coming]
   - Blockers: [Any issues]

2. **[Another Feature]** (#TASK_ID) - 30% complete
   - Status: [Current state]

## 📝 Key Decisions & Learnings

### Technical Decisions

1. **[Decision Topic]**
   - **What:** [Description]
   - **Why:** [Rationale]
   - **Impact:** [Effect on project]
   - Reference: See note #[NOTE_ID]

2. **[Another Decision]**
   - [Details]

### Learnings

- Learned [something new]
- Discovered [useful technique/tool]
- Found solution to [problem]

## 🎯 Next Week's Priorities

### High Priority

1. [ ] Complete [Task/Feature]
2. [ ] Start [New Task]
3. [ ] Review [Something]

### Medium Priority

1. [ ] Investigate [Topic]
2. [ ] Document [Feature]

### Research/Exploration

1. [ ] Explore [New technology/approach]

## 📈 Project Health

### [Project Name]

- **Status:** On track / At risk / Blocked
- **Progress:** X/Y tasks completed
- **Concerns:** [Any risks or issues]
- **Next milestone:** [Upcoming milestone]

### [Another Project]

- **Status:** [Status]
- **Progress:** [Progress]

## 🚧 Blockers & Challenges

1. **[Blocker Description]**
   - Issue: [Problem]
   - Impact: [Effect]
   - Action: [What's being done]

2. **[Challenge]**
   - [Details]

## 💡 Ideas & Future Work

- [New idea for improvement]
- [Technical debt to address]
- [Research topic to explore]

## 🎉 Wins & Celebrations

- [Something that went really well]
- [Achievement worth celebrating]
- [Positive feedback received]

---

## Time Breakdown by Project

| Project | Hours | % |
|---------|-------|---|
| [Project A] | XXh | 40% |
| [Project B] | XXh | 35% |
| [Other] | XXh | 25% |

## Time Breakdown by Activity

| Activity | Hours | % |
|----------|-------|---|
| Development | XXh | 60% |
| Meetings | XXh | 15% |
| Planning | XXh | 10% |
| Bug Fixing | XXh | 10% |
| Documentation | XXh | 5% |"
```

## Step 5: Share Summary

**For team updates:**

```bash
# Export the note to share
sb note show SUMMARY_NOTE_ID

# Or create a shorter version for standup
sb note create "Standup Summary - Week $(date +%W)" \
  --tags standup,brief \
  --content "## This Week

**Shipped:**
- [Feature X] - Improved Y by 30%
- [Bug fix] - Resolved Z issue affecting users

**Next Week:**
- Continue work on [Feature]
- Start [New project]

**Blockers:**
- None / [Specific blocker]

**Help Needed:**
- [If anything needed from team]"
```

## Step 6: Planning for Next Week

```bash
# Review ready work
sb issue ready --limit 10

# Check priorities
sb task list --priority high --status todo

# Create planning note
sb note create "Week $(date +%W) - Planning" \
  --tags planning,weekly \
  --content "## Goals for Week $(date +%W)

### Primary Goals (Must Do)

1. [ ] [Goal 1]
2. [ ] [Goal 2]
3. [ ] [Goal 3]

### Secondary Goals (Should Do)

1. [ ] [Goal 4]
2. [ ] [Goal 5]

### Nice to Have

1. [ ] [Goal 6]

## Time Allocation

- Feature development: 60%
- Bug fixes: 20%
- Meetings: 15%
- Learning: 5%

## Focus Areas

- [Area 1]
- [Area 2]

## Things to Remember

- [Important meeting on X]
- [Deadline for Y]
- [Team member OOO on Z]"
```

## Monthly Rollup

```bash
# For monthly summaries, aggregate 4 weeks
sb report work --days 30

# Create monthly note
sb note create "Monthly Summary - $(date +%B) $(date +%Y)" \
  --tags monthly,summary \
  --content "# Monthly Summary - $(date +%B) $(date +%Y)

## Overview

**Total Time Logged:** XXXh
**Tasks Completed:** XX
**Issues Closed:** XX
**Projects:** X active

## Major Accomplishments

1. **[Major Feature/Project]**
   - [Details and impact]

2. **[Another Achievement]**
   - [Details]

## Metrics

- Code deployed: XX commits
- Bugs fixed: XX
- Features shipped: XX
- Documentation created: XX notes

## Key Learnings

- [Important learning 1]
- [Important learning 2]

## Areas for Improvement

- [Thing to improve]
- [Another area]

## Next Month's Focus

- [Focus area 1]
- [Focus area 2]"
```

**Help them create a narrative:**

Transform data into a story:
- **What** was accomplished (concrete deliverables)
- **Why** it matters (impact, value)
- **How** it went (challenges, learnings)
- **What's** next (forward-looking)

**Encourage reflection:**
- What went well?
- What was challenging?
- What would you do differently?
- What did you learn?
- What are you proud of?

**Pro Tips:**

1. **Do it Friday afternoon** - While week is fresh
2. **Use tags to find content** - `decision`, `completed`, `important`
3. **Include metrics** - Numbers tell the story
4. **Be honest about blockers** - Helps get help
5. **Celebrate wins** - Acknowledge achievements
6. **Look forward** - Plan next week while reviewing

**Time Investment:**
- Weekly summary: 30-60 minutes
- Monthly summary: 1-2 hours
- ROI: Better planning, clear communication, career documentation

**Uses for summaries:**
- Performance reviews
- Project updates
- Team standups
- Personal reflection
- Resume/portfolio building
- Learning documentation
