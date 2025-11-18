# Common Workflows

Real-world usage patterns and workflows for Second Brain.

> **All workflows work 100% offline** - Jira integration is completely optional!

## Table of Contents

- [Daily Development Workflow](#daily-development-workflow)
- [Weekly Planning & Review](#weekly-planning--review)
- [Project-Based Workflow](#project-based-workflow)
- [Performance Review Preparation](#performance-review-preparation)
- [Bug Tracking Workflow](#bug-tracking-workflow)
- [Learning & Research Workflow](#learning--research-workflow)
- [Meeting & Collaboration Workflow](#meeting--collaboration-workflow)
- [Time Tracking Workflow](#time-tracking-workflow)
- [Using with AI Agents](#using-with-ai-agents)

---

## Daily Development Workflow

### Morning Routine

```bash
# 1. Check what's on your plate
sb task list --status in_progress
sb task list --status todo --priority high

# 2. Add morning standup notes
sb log add "Daily standup - discussed sprint progress and blockers"

# 3. Plan your day - pick a task
sb task update 15 --status in_progress
```

### During Work

```bash
# Log work as you go
sb log add "Debugging authentication timeout issue" --task-id 15 --time 45
sb log add "Found root cause - connection pool exhaustion" --task-id 15

# Quick notes without task linking
sb log add "Team discussion about API design patterns" --time 30
sb log add "Code review for Sarah's PR on user service"

# Update task status as you progress
sb task update 15 --time 90  # Add more time
```

### End of Day

```bash
# 1. Update task status
sb task update 15 --status done --time 30

# 2. Review your day
sb log show --days 1

# 3. Plan tomorrow - add high-priority items
sb task add "Deploy authentication fix to staging" \
  --project user-service \
  --priority high
```

**Example daily log:**
```markdown
# Work Log - 2025-01-17

- **09:15**: Daily standup - discussed sprint progress and blockers
- **09:30** [Debug auth timeout]: Debugging authentication timeout issue (45m)
- **10:30** [Debug auth timeout]: Found root cause - connection pool exhaustion
- **11:30**: Team discussion about API design patterns (30m)
- **14:00**: Code review for Sarah's PR on user service
- **15:00** [Debug auth timeout]: Implemented fix and added tests (90m)
```

---

## Weekly Planning & Review

### Monday Planning

```bash
# 1. Review last week's accomplishments
sb report work --days 7

# 2. Check project status
sb project list --status active
sb project status api-v2-migration

# 3. Create tasks for the week
sb task add "Implement rate limiting" \
  --project api-v2-migration \
  --priority high

sb task add "Update API documentation" \
  --project api-v2-migration \
  --priority medium

sb task add "Performance testing" \
  --project api-v2-migration \
  --priority medium

# 4. Log your planning session
sb log add "Weekly planning - created tasks for sprint goals" --time 30
```

### Friday Review

```bash
# 1. Generate weekly report
sb report work --days 7 > weekly-report.md

# 2. Review completed tasks
sb task list --status done

# 3. Check what's in progress
sb task list --status in_progress

# 4. Add end-of-week summary
sb log add "End of week - completed 8 tasks, 2 still in progress"

# 5. Review the report
cat weekly-report.md
```

---

## Project-Based Workflow

### Starting a New Project

```bash
# 1. Create the project
sb project create "Mobile App Redesign" \
  --description "Complete redesign of mobile UI/UX with new design system" \
  --tags "mobile,frontend,design"

# 2. Break down into initial tasks
sb task add "Research design systems and component libraries" \
  --project mobile-app-redesign \
  --priority high

sb task add "Create design mockups for main screens" \
  --project mobile-app-redesign \
  --priority high

sb task add "Set up new frontend build pipeline" \
  --project mobile-app-redesign \
  --priority medium

sb task add "Implement new navigation system" \
  --project mobile-app-redesign \
  --priority medium

# 3. Log project kickoff
sb log add "Started Mobile App Redesign project - created initial task breakdown" --time 45
```

### Working on the Project

```bash
# View project dashboard
sb project status mobile-app-redesign

# Work on tasks
sb task list --project mobile-app-redesign --status todo
sb task update 20 --status in_progress

# Log project work
sb log add "Researching component libraries" --task-id 20 --time 120
sb log add "Decided on React Native Paper for components" --task-id 20
```

### Project Completion

```bash
# 1. Complete final tasks
sb task update 25 --status done

# 2. Generate project report
sb report work --days 60 --project mobile-app-redesign > project-summary.md

# 3. Archive the project
# Edit data/projects/mobile-app-redesign.md
# Change status: completed

# 4. Log completion
sb log add "Completed Mobile App Redesign project - shipped to production"
```

---

## Performance Review Preparation

### Quarterly Review (Every 3 months)

```bash
# 1. Generate comprehensive report
sb report work --days 90 > q4-2024-performance.md

# 2. Review all completed tasks
sb task list --status done | grep "2024-10\|2024-11\|2024-12"

# 3. Check project contributions
sb project list

# For each major project:
sb project status api-v2-migration
sb project status mobile-app-redesign

# 4. Create summary document
cat > performance-review-q4.md <<EOF
# Q4 2024 Performance Review

## Summary
- Projects: 3 completed, 2 in progress
- Tasks completed: 47
- Time tracked: 240+ hours

## Key Accomplishments
1. Led API v2 Migration (completed)
2. Shipped Mobile App Redesign (completed)
3. Reduced API latency by 40%

## Detailed Report
$(cat q4-2024-performance.md)
EOF
```

### Annual Review

```bash
# Generate full year report
sb report work --days 365 > annual-review-2024.md

# Count projects by status
sb project list --status completed
sb project list --status active

# Review impact
cat annual-review-2024.md
```

### Promotion Documentation

Your Second Brain is perfect for documenting impact:

```bash
# 1. Gather data
sb report work --days 180  # Last 6 months

# 2. Extract key projects
sb project status critical-infrastructure-upgrade
sb project status performance-optimization
sb project status team-onboarding-program

# 3. Create promotion packet
# All your work is documented with:
# - Specific tasks completed
# - Time invested
# - Project outcomes
# - Technical decisions (in work logs)
```

---

## Bug Tracking Workflow

### Recording a Bug

```bash
# 1. Create task for the bug
sb task add "Fix: Memory leak in background worker" \
  --description "Workers accumulate memory over 24h, eventually OOM" \
  --priority urgent \
  --project backend-services

# 2. Start investigation
sb task update 30 --status in_progress

# 3. Log investigation work
sb log add "Investigating memory leak - added memory profiling" --task-id 30 --time 45
sb log add "Found leak: Event listeners not being removed" --task-id 30
sb log add "Implemented fix with WeakRef pattern" --task-id 30 --time 90
```

### Production Incident

```bash
# Log the incident
sb log add "INCIDENT: Production API returning 500s for /users endpoint" --time 15
sb log add "Root cause: Database connection pool exhausted" --time 30
sb log add "Fix: Increased pool size and added circuit breaker" --time 60
sb log add "Monitoring post-fix, writing incident report" --time 45

# Create follow-up tasks
sb task add "Write postmortem for API incident" --priority high
sb task add "Implement better connection pool monitoring" --priority high
sb task add "Add circuit breaker to other endpoints" --priority medium
```

---

## Learning & Research Workflow

### Learning a New Technology

```bash
# 1. Create a learning project
sb project create "Learning Rust" \
  --description "Learning Rust programming language and ecosystem" \
  --tags "learning,rust,professional-development"

# 2. Break into learning goals
sb task add "Complete Rust Book chapters 1-10" --project learning-rust
sb task add "Build CLI tool in Rust" --project learning-rust
sb task add "Understand ownership and borrowing" --project learning-rust

# 3. Log learning sessions
sb log add "Read Rust Book ch 1-3 - variables and data types" \
  --task-id 35 --time 120

sb log add "Built simple CLI calculator in Rust - practiced pattern matching" \
  --task-id 36 --time 90

# 4. Track progress
sb project status learning-rust
```

### Research & Experimentation

```bash
# Create research project
sb project create "Database Performance Research" \
  --description "Investigating query optimization and indexing strategies" \
  --tags "research,database,performance"

# Log research activities
sb log add "Benchmarked different index types - B-tree vs Hash" --time 60
sb log add "Tested query planner with EXPLAIN ANALYZE" --time 45
sb log add "Found N+1 query in user service - 100x speedup possible" --time 30

# Create actionable tasks from research
sb task add "Implement composite index on users table" \
  --project database-performance-research \
  --priority high
```

---

## Meeting & Collaboration Workflow

### Recording Meeting Notes

Using the CLI for quick notes:

```bash
# During/after meeting
sb log add "Team sync - discussed Q1 roadmap priorities" --time 30
sb log add "1:1 with manager - performance review scheduled for next week" --time 30
sb log add "Architecture review - approved design for new caching layer" --time 60
```

Using MCP tools for full transcripts (via AI agent):

```
"I have a transcript from today's planning meeting. Can you process it?"

Agent uses create_transcript:
- Saves raw transcript
- Creates processed markdown
- Extracts action items
- Links to relevant projects
```

### Following Up on Action Items

```bash
# Create tasks from meeting action items
sb task add "Prepare architecture diagram for next review" \
  --priority high

sb task add "Send performance metrics to stakeholders" \
  --priority medium

# Track completion
sb task list --priority high
```

---

## Time Tracking Workflow

### Detailed Time Tracking

```bash
# Start working on a task
sb task update 40 --status in_progress
sb log add "Starting work on user authentication refactor" --task-id 40

# Log time in increments
sb log add "Implemented new auth middleware" --task-id 40 --time 60
sb log add "Added unit tests for auth logic" --task-id 40 --time 45
sb log add "Updated documentation" --task-id 40 --time 30

# Complete task with final time entry
sb task update 40 --status done --time 15
```

### Weekly Time Report

```bash
# See how you spent your time
sb report work --days 7

# By project
sb report work --days 7 --project mobile-app-redesign
sb report work --days 7 --project api-v2-migration

# Monthly summary
sb report work --days 30
```

### Billable Hours Tracking

```bash
# Tag billable projects
sb project create "Client Project Alpha" \
  --tags "client,billable,consulting"

# Track time on client work
sb log add "Client call - requirements gathering" \
  --project client-project-alpha \
  --time 60

sb log add "Development work on feature X" \
  --project client-project-alpha \
  --time 240

# Generate invoice report
sb report work --days 30 --project client-project-alpha > invoice-report.md
```

---

## Using with AI Agents

Once you configure the MCP server, AI agents can help automate your workflows.

### Configuration

Add to your MCP config:
```json
{
  "mcpServers": {
    "second-brain": {
      "command": "python",
      "args": ["-m", "second_brain.mcp_server"],
      "env": {
        "SECOND_BRAIN_DATA_DIR": "/home/seanm/repos/second-brain/data"
      }
    }
  }
}
```

### Example Interactions

**End of Day Summary**
```
You: "Add today's work to my log"

Agent: "What did you work on today?"

You: "Fixed a production bug in the authentication service,
      spent about 2 hours on it. Also did code reviews."

Agent uses: create_work_log_entry
- Logs the work with proper formatting
- Estimates time tracking
- Asks if you want to link to a task
```

**Project Status Check**
```
You: "What's the status of the mobile app redesign?"

Agent uses: get_project_status
- Retrieves project details
- Shows task breakdown
- Highlights blockers
- Summarizes progress
```

**Weekly Planning**
```
You: "Help me plan next week based on what I did this week"

Agent uses: get_work_logs, get_projects, get_tasks
- Reviews last week's activities
- Identifies incomplete tasks
- Suggests priorities
- Creates new tasks
```

**Performance Review Prep**
```
You: "Generate a summary of my work for Q4 2024 for my performance review"

Agent uses: generate_report, get_projects, get_tasks
- Compiles all work from Oct-Dec
- Groups by project
- Highlights completed tasks
- Calculates time invested
- Formats for review submission
```

**Meeting Follow-up**
```
You: "Process this meeting transcript: [paste transcript]"

Agent uses: create_transcript, update_transcript, create_task
- Saves the transcript
- Extracts key points
- Identifies action items
- Creates tasks for follow-ups
- Links to relevant projects
```

**Quick Task Creation**
```
You: "I need to implement rate limiting for the API,
      it's high priority"

Agent uses: create_task, get_projects
- Suggests relevant project
- Creates task with proper priority
- Asks for additional details
```

---

## Workflow Combinations

### The Comprehensive Workflow

Combining all practices:

```bash
# Monday morning
sb report work --days 7                    # Review last week
sb project list --status active             # Check active projects
sb task list --status in_progress           # See what's ongoing

# Create weekly plan
sb log add "Weekly planning session" --time 30

# Daily work (repeated each day)
sb log add "Daily standup"
sb task update XX --status in_progress
sb log add "Work description" --task-id XX --time YY
sb task update XX --status done

# Friday afternoon
sb report work --days 7 > weekly-summary.md
sb log add "End of week summary - completed N tasks"

# Monthly review
sb report work --days 30
sb project status PROJECT_SLUG             # For each active project

# Quarterly review
sb report work --days 90 > q1-review.md
```

---

## Offline-First Workflow

Everything works without internet:

```bash
# 1. All data is local
ls data/projects/           # Your projects
ls data/work_logs/          # Your work logs
cat data/index.db           # SQLite database

# 2. No external dependencies needed
sb project create "Offline Project"
sb task add "Works without internet"
sb log add "Completely offline workflow"

# 3. Search your data
grep -r "authentication" data/
grep -r "performance" data/projects/

# 4. Backup locally
tar -czf backup.tar.gz data/
# or
cp -r data/ backup/
# or
cd data && git init && git add . && git commit -m "backup"

# 5. Sync when you want (optional)
# Only if you set up Jira:
sb jira sync
```

---

## Tips for Effective Workflows

### 1. Be Consistent

Pick a workflow and stick with it:
- Log work at the same times each day
- Review weekly on the same day
- Use consistent tags and project names

### 2. Start Small

Don't try to track everything:
```bash
# Week 1: Just log daily work
sb log add "Description of work"

# Week 2: Add time tracking
sb log add "Description" --time MINUTES

# Week 3: Link to tasks
sb task add "Task name"
sb log add "Description" --task-id ID --time MINUTES

# Week 4: Organize into projects
sb project create "Project"
sb task add "Task" --project slug
```

### 3. Use Templates

Create template tasks for recurring work:
```bash
# Create standard tasks
sb task add "Weekly team meeting notes" --priority low
sb task add "Code review" --priority medium
sb task add "Documentation updates" --priority low
```

### 4. Review Regularly

```bash
# Daily: Quick check
sb log show --days 1

# Weekly: Detailed review
sb report work --days 7

# Monthly: Big picture
sb report work --days 30
sb project list
```

### 5. Keep It Simple

The best workflow is the one you'll actually use:
```bash
# Minimum viable workflow:
sb log add "What I did"          # Daily
sb report work --days 7           # Weekly
```

---

## Next Steps

1. Pick one workflow to start with
2. Practice it for a week
3. Adjust based on what works for you
4. Add complexity gradually
5. Review and iterate

Remember: **Your Second Brain should make your life easier, not more complicated!**
