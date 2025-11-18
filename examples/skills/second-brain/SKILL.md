---
name: second-brain
description: Use Second Brain CLI for persistent work tracking, notes, and task management. Works globally across all projects with rich markdown notes, time tracking, and AI agent integration. For complex dependency tracking, use bd (beads); for simple checklists, use TodoWrite.
---

# Second Brain CLI

## Overview

Second Brain is a **global, persistent knowledge base** for tracking work, managing tasks, and maintaining notes across all your projects. It's installed once in `~/.second-brain/` and accessible from any directory.

## When to Use Second Brain vs Other Tools

### Use Second Brain when:
- **Persistent work tracking** - Work logs, tasks, and notes that need to survive across projects
- **Time tracking** - Need to track time spent on tasks for performance reviews or reporting
- **Cross-project work** - Tasks that span multiple repositories or projects
- **Rich documentation** - Need markdown notes with full context for tasks/projects
- **Performance reviews** - Need comprehensive reports of work completed over time
- **Daily work logging** - Track what you did each day with timestamps

### Use bd (beads) when:
- **Complex dependencies** - Work with blockers, prerequisites, or hierarchical epics
- **Dependency graphs** - Need to visualize what blocks what
- **Ready work detection** - Automatically find work with no blockers

### Use TodoWrite when:
- **Single-session checklists** - Simple task lists for current work
- **Immediate progress tracking** - Show user what you're working on right now
- **Ephemeral tasks** - Tasks that don't need to persist beyond this session

**Key insight**: Second Brain is your **persistent work database**. bd handles **dependencies**. TodoWrite handles **current session checklists**.

## Global Setup

Second Brain is **always available** from any directory:

```bash
# Check if Second Brain is installed
sb --version

# Environment variable should be set
echo $SECOND_BRAIN_DIR
# Should show: /home/user/.second-brain (or wherever it's installed)
```

**If not set:**
```bash
export SECOND_BRAIN_DIR="$HOME/.second-brain"
# Add to ~/.bashrc or ~/.zshrc for persistence
```

**Key difference from bd:** Second Brain doesn't auto-discover databases. It uses one global database (`~/.second-brain/data/index.db`) that works from ANY directory.

## Session Start Protocol

At the start of any session, **check Second Brain** to establish context:

### Session Start Checklist

```
Session Start:
- [ ] Run sb task list --status in_progress to see active work
- [ ] Run sb log show --days 1 to see today's work
- [ ] Run sb issue ready (if using Beads integration)
- [ ] Report to user: "X tasks in progress: [summary]"
- [ ] Report: "Today's logs: [summary]" or "No work logged yet today"
```

**Report format:**
- "You have 3 tasks in progress: [list tasks]"
- "Today you've logged: [summarize logs]"
- "Issue X is ready to work on (no blockers)"

This establishes immediate shared context without requiring user prompting.

## Core Operations

### Work Log Tracking

**Log work as you go:**
```bash
sb log add "Implemented OAuth integration" --task-id 42 --time 120
sb log add "Code review for PR #234" --time 30
sb log add "Fixed authentication bug"
```

**View recent work:**
```bash
sb log show                    # Last 7 days
sb log show --days 1           # Today only
sb log show --days 30          # Last month
```

**When to log:**
- After completing significant work (30+ minutes)
- End of day summary
- When switching tasks
- Before session end

---

### Task Management

**Create tasks:**
```bash
sb task add "Implement rate limiting" --project backend-api --priority high
sb task add "Write tests for auth" --project backend-api
sb task add "Fix login timeout bug" --priority urgent
```

**Update tasks:**
```bash
sb task update 42 --status in_progress
sb task update 42 --status done --time 180
sb task update 42 --priority high
```

**List tasks:**
```bash
sb task list --status in_progress     # Current work
sb task list --project backend-api    # Project-specific
sb task list --priority high          # High priority
```

**When to create tasks:**
- User explicitly asks to track work
- Multi-step work that needs organization
- Work that will span multiple days
- Work that needs time tracking

---

### Note-Taking

**Create notes:**
```bash
# Task-specific note
sb note create "API Architecture" \
  --task-id 42 \
  --content "Using REST over GraphQL because..."

# Project-wide note
sb note create "Design Decisions" \
  --project backend-api \
  --content "## Authentication\nUsing JWT with RS256..."

# Standalone note
sb note create "Research: Redis vs Memcached" \
  --tags research,caching \
  --content "Comparison of caching solutions..."
```

**Search notes:**
```bash
sb note search "authentication"
sb note list --project backend-api
sb note list --tags research
sb note list --task-id 42
```

**When to create notes:**
- Design decisions that need documentation
- Research findings
- API documentation
- Implementation details for tasks
- Meeting notes linked to projects

---

### Project Management

**Create projects:**
```bash
sb project create "Backend API" \
  --description "Core API services" \
  --tags backend,api

sb project create "Mobile App" \
  --description "iOS and Android apps" \
  --tags mobile,frontend
```

**Project status:**
```bash
sb project status backend-api     # Detailed status
sb project list                   # All projects
sb project list --status active   # Only active
```

**When to create projects:**
- Starting new major initiatives
- Need to organize multiple related tasks
- Want to track progress over time
- Group work across multiple repos

---

### Issue/Epic Management (Beads Integration)

**Create epic + project together (RECOMMENDED):**
```bash
sb issue create-with-project "Payment Integration" \
  --priority 4 \
  --labels backend,payments
```

**Create issues:**
```bash
sb issue create "Implement Stripe API" \
  --epic epic-042 \
  --with-task \
  --project payment-integration

sb issue create "Add payment UI" \
  --epic epic-042 \
  --priority 3
```

**Find ready work:**
```bash
sb issue ready              # All ready work
sb issue ready --priority 4 # Critical only
```

**When to use issues:**
- Complex multi-step features
- Work with dependencies/blockers
- Team collaboration
- Need epic breakdown

---

### Reports

**Generate reports:**
```bash
sb report work --days 7      # Weekly report
sb report work --days 90     # Quarterly (for reviews)
```

**When to generate reports:**
- End of week summaries
- Performance review preparation
- Team status updates
- Project retrospectives

---

## CLI vs MCP vs Slash Commands

Second Brain supports **three interfaces**:

### 1. CLI (sb commands)
**Use for:**
- Direct execution from terminal
- User explicitly wants to run commands
- Scripting or automation
- Lower context usage

**Examples:**
```bash
sb log add "Fixed bug" --task-id 42 --time 90
sb task list --status in_progress
```

### 2. MCP Server
**Use for:**
- AI agent needs to query data
- Complex operations requiring multiple steps
- User asks questions about their work
- Need to analyze patterns

**Examples:**
- "What did I work on last week?"
- "Show me all high priority tasks"
- "Generate a report for my manager"

### 3. Slash Commands
**Use for:**
- Guided workflows with user interaction
- User prefers conversational interface
- Complex multi-step processes
- Quick mode for power users

**Examples:**
- `/sb-log "work" --task-id 42` (quick mode)
- `/sb-log` then conversational prompts
- `/sb-daily-summary` (generates summary)

**Decision guide:**
- User in terminal context → CLI
- User asking questions → MCP
- User wants guided workflow → Slash commands
- All three work! Choose based on user preference and context.

**For detailed CLI reference, read:** [references/CLI_REFERENCE.md](references/CLI_REFERENCE.md)
**For MCP integration patterns, read:** [references/MCP_INTEGRATION.md](references/MCP_INTEGRATION.md)
**For slash command workflows, read:** [references/SLASH_COMMANDS.md](references/SLASH_COMMANDS.md)

---

## Common Workflows

### Pattern 1: Daily Development Workflow

**Morning:**
```bash
# Check active work
sb task list --status in_progress

# Review yesterday
sb log show --days 1
```

**During work:**
```bash
# Log as you go
sb log add "Implemented feature X" --task-id 42 --time 120

# Update task status
sb task update 42 --status in_progress
```

**End of day:**
```bash
# Final log
sb log add "Code review, deployed to staging" --time 45

# Mark tasks done
sb task update 42 --status done --time 180

# Review the day
sb log show --days 1
```

---

### Pattern 2: Starting New Feature

**Create epic + project:**
```bash
sb issue create-with-project "User Authentication" \
  --priority 4 \
  --labels backend,security
```

**Create issues and tasks:**
```bash
sb issue create "OAuth integration" \
  --epic epic-042 \
  --with-task \
  --project user-authentication

sb issue create "Password reset flow" \
  --epic epic-042 \
  --with-task \
  --project user-authentication
```

**Add notes:**
```bash
sb note create "Auth Architecture" \
  --project user-authentication \
  --content "Using JWT with RS256, 1hr access tokens..."
```

---

### Pattern 3: Weekly Review

```bash
# Generate report
sb report work --days 7

# Review all closed tasks
sb task list --status done --days 7

# Check what's still in progress
sb task list --status in_progress

# Plan next week
sb issue ready --priority 3,4
```

**For complete workflow walkthroughs with checklists, read:** [references/WORKFLOWS.md](references/WORKFLOWS.md)

---

## Integration with bd (Beads)

Second Brain and bd work together:

**Second Brain provides:**
- Rich markdown notes
- Time tracking
- Work logs
- Project organization

**bd (Beads) provides:**
- Dependency graphs
- Blocker detection
- Ready work finder
- Epic breakdown

**Integration points:**

1. **Epic + Project creation:**
   ```bash
   sb issue create-with-project "Feature"
   # Creates: Epic in Beads + Project in Second Brain
   ```

2. **Issue + Task linking:**
   ```bash
   sb issue create "Issue" --with-task --project PROJECT_SLUG
   # Creates: Issue in Beads + Task in Second Brain (linked)
   ```

3. **Workflow:**
   - Use bd to find ready work: `bd ready` or `sb issue ready`
   - Create task in Second Brain for notes/time: `sb task add`
   - Log work: `sb log add --task-id`
   - Track dependencies in bd: `bd dep add`

---

## Best Practices

### Work Log Quality

**Good work log:**
```bash
sb log add "Implemented OAuth2 flow with JWT tokens (RS256). Added refresh token rotation. Tests passing." --task-id 42 --time 180
```

**Bad work log:**
```bash
sb log add "worked on stuff" --time 120
```

**Guidelines:**
- Be specific: WHAT you did, not just "worked on"
- Include outcomes: "Tests passing", "Deployed to staging"
- Link to tasks when possible
- Track time for all significant work (30+ minutes)

---

### Task Organization

**Good task:**
- Clear, actionable title: "Implement rate limiting for API endpoints"
- Specific description: "Add rate limiting middleware (100 req/min per IP)"
- Appropriate priority: high/medium/low based on impact
- Linked to project: --project backend-api

**Bad task:**
- Vague title: "Fix stuff"
- No description
- Wrong priority
- Not linked to anything

---

### Note-Taking

**Good note:**
```markdown
## Authentication Decision

Using JWT with RS256 (not HS256) because:
- Enables key rotation without downtime
- Public key verification in microservices
- Industry standard for distributed systems

Access tokens: 1hr expiry
Refresh tokens: 7 day expiry, rotation on use

Trade-off: RS256 slower than HS256, but security > performance for auth
```

**Bad note:**
```markdown
using jwt
```

**Guidelines:**
- Explain WHY, not just WHAT
- Document trade-offs and decisions
- Include enough context to understand later
- Use markdown formatting
- Link to relevant tasks/projects

---

## Time Tracking

Second Brain automatically tracks time when you specify `--time`:

```bash
sb log add "Work description" --task-id 42 --time 120  # 2 hours

sb task update 42 --time 90  # Add 1.5 hours to task
```

**Time aggregation:**
- Task total time = Sum of all work logs + direct time updates
- Project time = Sum of all task times in project
- Reports show time breakdown by project/task

**When to track time:**
- All work > 30 minutes
- Context switches (log previous work)
- End of day
- Before performance reviews

---

## Reports and Analytics

**Weekly report:**
```bash
sb report work --days 7
```

Shows:
- Total time worked
- Tasks completed
- Projects worked on
- Work logs summary

**Quarterly report (performance review):**
```bash
sb report work --days 90 > Q1-accomplishments.md
```

**Project-specific:**
```bash
sb project status backend-api
```

Shows:
- Task breakdown
- Time spent
- Completion rate
- Recent activity

---

## Troubleshooting

**If sb command not found:**
```bash
# Check installation
sb --version

# Check environment variable
echo $SECOND_BRAIN_DIR
# Should output: /home/user/.second-brain

# If not set, add to shell profile:
echo 'export SECOND_BRAIN_DIR="$HOME/.second-brain"' >> ~/.bashrc
source ~/.bashrc
```

**If "No second brain found":**
- Second Brain requires `SECOND_BRAIN_DIR` environment variable
- Must be initialized: `sb init --global`
- Check: `ls -la ~/.second-brain`

**If tasks/logs not showing:**
- Verify you're querying correct filters
- Check status: `sb task list` (no filters shows all)
- Check date range: `sb log show --days 30`

---

## Quick Reference

| Command | Purpose | Example |
|---------|---------|---------|
| `sb log add` | Log work | `sb log add "Fixed bug" --task-id 42 --time 90` |
| `sb log show` | View logs | `sb log show --days 7` |
| `sb task add` | Create task | `sb task add "Title" --project api --priority high` |
| `sb task update` | Update task | `sb task update 42 --status done` |
| `sb task list` | List tasks | `sb task list --status in_progress` |
| `sb note create` | Create note | `sb note create "Title" --task-id 42` |
| `sb note search` | Search notes | `sb note search "keyword"` |
| `sb project create` | Create project | `sb project create "Name" --tags tag1,tag2` |
| `sb project status` | Project details | `sb project status PROJECT_SLUG` |
| `sb issue create-with-project` | Epic + Project | `sb issue create-with-project "Feature" -p 4` |
| `sb issue ready` | Find ready work | `sb issue ready --priority 4` |
| `sb report work` | Generate report | `sb report work --days 30` |

---

## Reference Files

Detailed information organized by topic:

| Reference | Read When |
|-----------|-----------|
| [references/CLI_REFERENCE.md](references/CLI_REFERENCE.md) | Need complete command reference with all flags and options |
| [references/WORKFLOWS.md](references/WORKFLOWS.md) | Need step-by-step workflows for common scenarios |
| [references/MCP_INTEGRATION.md](references/MCP_INTEGRATION.md) | Using MCP server with AI agents, need tool reference |
| [references/SLASH_COMMANDS.md](references/SLASH_COMMANDS.md) | Using slash commands in Claude Code, need workflow examples |
