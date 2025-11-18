# Second Brain Slash Commands for Claude Code

This directory contains example slash commands for using the Second Brain **CLI tool** with Claude Code and other AI agents.

## What are Slash Commands?

Slash commands are shortcuts that let you quickly trigger specific workflows in Claude Code. The agent will help you construct and run the appropriate `sb` CLI commands.

For example:
- Type `/sb-log` → Agent helps you construct `sb log add` command
- Type `/sb-report` → Agent runs `sb report work` and shows results
- Type `/sb-current-work` → Agent runs multiple commands to show your status

**Key Point:** These slash commands teach the AI agent how to use the Second Brain **CLI tool** (`sb` commands). The agent will help you:
1. Understand which `sb` command to use
2. Construct the command with proper options
3. Execute it for you (with confirmation)
4. Interpret the results

## CLI vs MCP Server

Second Brain can be used in two ways:

**1. CLI Tool (`sb` commands)**
- Run commands directly in your terminal
- Example: `sb log add "Working on feature X"`
- **These slash commands teach the agent to use the CLI**

**2. MCP Server (for agents like Claude Code)**
- Agent calls MCP tools directly
- Example: Agent uses `create_work_log_entry` MCP tool
- See [MCP_TOOLS.md](../MCP_TOOLS.md) for MCP tool reference

**Which should you use?**
- **CLI + Slash Commands**: Simpler, direct terminal commands, agent helps construct them
- **MCP Server**: More integrated, agent has direct access to your data

Both work! These slash commands use the CLI approach, teaching the agent to run `sb` commands via bash. The agent can also use the MCP server if it's configured (see [INSTALLATION.md](../INSTALLATION.md)).

## Installation

### Step 1: Copy Commands to Your Project

Copy the command files to your project's `.claude/commands/` directory:

```bash
# Navigate to your project
cd ~/your-project

# Create commands directory if it doesn't exist
mkdir -p .claude/commands

# Copy all Second Brain commands
cp /path/to/second-brain/examples/commands/*.md .claude/commands/

# Or copy selectively
cp /path/to/second-brain/examples/commands/sb-log.md .claude/commands/
cp /path/to/second-brain/examples/commands/sb-report.md .claude/commands/
```

### Step 2: Restart Claude Code

After copying the commands, restart Claude Code to load them.

### Step 3: Verify Commands Loaded

In Claude Code, type `/sb-` and you should see autocomplete suggestions for all Second Brain commands.

## Getting Started

**New to Second Brain?** Start here:

1. **First Day:** Try `/sb-daily-dev-workflow` - walks you through a complete workday
2. **Small Tasks:** Use `/sb-quick-tasks` - learn to manage quick wins
3. **Weekly Review:** Run `/sb-weekly-summary` - see your accomplishments

**Choose Your Path:**

| You Are | Start With | Then Try |
|---------|------------|----------|
| Software Engineer | `/sb-daily-dev-workflow` | `/sb-feature-development` |
| ML/Data Scientist | `/sb-ml-research-workflow` | `/sb-weekly-summary` |
| Bug Hunter | `/sb-bug-investigation` | `/sb-quick-tasks` |
| Project Manager | `/sb-projects-overview` | `/sb-weekly-summary` |
| Need Quick Wins | `/sb-quick-tasks` | `/sb-daily-dev-workflow` |

## Available Commands

### 🌟 Complete Workflow Guides

These comprehensive workflow guides demonstrate real-world usage patterns:

#### `/sb-daily-dev-workflow`
**Complete daily development workflow** ⭐ RECOMMENDED

Guides you through a full dev day: morning planning, tracking work, taking notes, and end-of-day wrap-up.

Perfect for:
- Regular development work
- Tracking multiple tasks
- Building a daily rhythm

Covers:
- Morning: Check ready work, plan day
- During: Log work, add notes, track time
- Evening: Update statuses, create handoff notes
- Weekly: Generate summaries

---

#### `/sb-ml-research-workflow`
**ML research and experimentation workflow** 🔬

Specialized for data scientists and ML engineers doing research.

Perfect for:
- Literature reviews
- Experiment tracking
- Model comparison
- Research documentation

Covers:
- Creating research notes
- Tracking experiments
- Comparing models
- Organizing findings
- Weekly research summaries

---

#### `/sb-feature-development`
**Complex feature development with full integration** 🏗️

Shows how to develop a large feature using epics, issues, tasks, and notes.

Perfect for:
- Multi-component features
- Team collaboration
- Full documentation
- Handoff to other teams

Covers:
- Planning with epics
- Breaking down into issues
- Implementation notes
- API documentation
- Deployment checklists
- Epic summaries

---

#### `/sb-bug-investigation`
**Thorough bug investigation and documentation** 🐛

Shows how to investigate complex bugs with detailed documentation.

Perfect for:
- Tricky bugs
- Production incidents
- Postmortems
- Root cause analysis

Covers:
- Investigation notes
- Solution planning
- Implementation tracking
- Deployment runbooks
- Postmortem creation

---

#### `/sb-weekly-summary`
**Comprehensive weekly summary and reporting** 📊

Generate complete weekly summaries with stats, accomplishments, and planning.

Perfect for:
- Weekly updates
- Team standups
- Manager reviews
- Personal reflection

Covers:
- Gathering metrics
- Analyzing completions
- Reviewing notes
- Planning next week
- Monthly rollups

---

#### `/sb-quick-tasks`
**Fast execution of small tasks** ⚡

Shows how to handle quick wins without overengineering.

Perfect for:
- Small bug fixes
- Documentation updates
- Quick refactors
- Urgent hotfixes

Covers:
- Quick task creation
- Batch processing
- Organization strategies
- When to promote to issues
- Anti-patterns to avoid

---

#### `/sb-epic-project-create` ⭐
**Create epic + project together for new initiatives**

The **recommended way** to start complex work that needs both:
- **Beads epic** for dependency tracking and high-level coordination
- **Second Brain project** for day-to-day notes, tasks, and time tracking

Automatically links them together with the same title and tags.

Perfect for:
- Starting new features or major initiatives
- Complex work requiring dependency management AND detailed notes
- Team collaboration projects
- Work spanning multiple tasks/issues

Covers:
- Creating both epic and project in one command
- Linking strategy
- Creating issues under the epic
- Creating tasks in the project
- Adding notes and tracking work
- Full workflow from initialization to completion

---

### 🔍 Query & Visualization Commands

These commands help you **find, explore, and visualize** your Second Brain content:

#### `/sb-search-all`
**Global search across all content**

Search everything: notes, tasks, work logs, transcripts, issues, projects.

Quick mode:
```
/sb-search-all "caching"
/sb-search-all "API" --type note
/sb-search-all "performance" --project backend-api
```

Perfect for:
- Finding information quickly
- Discovering related content
- Avoiding duplicate work
- Recovering lost context

---

#### `/sb-note-search`
**Search and filter notes**

Find notes by keyword, tags, project, or task.

Quick mode:
```
/sb-note-search "Redis"
/sb-note-search --tags research,important
/sb-note-search --task-id 42
```

Perfect for:
- Finding specific notes
- Filtering by context
- Discovering related documentation

---

#### `/sb-project-view`
**Comprehensive project visualization**

See everything related to a project: tasks, notes, work logs, progress.

Quick mode:
```
/sb-project-view backend-api
```

Shows:
- Task breakdown by status/priority
- Recent work activity
- Project notes
- Linked issues
- Project health metrics

Perfect for:
- Daily standup prep
- Weekly project reviews
- Onboarding team members
- Manager updates

---

#### `/sb-task-view`
**Complete task context**

View everything about a task: notes, work logs, linked issue, timeline.

Quick mode:
```
/sb-task-view 42
```

Shows:
- Task details and status
- All linked notes
- Work log timeline
- Linked Beads issue
- Next steps
- Completion criteria

Perfect for:
- Before starting work
- During standup
- Creating handoffs
- Resuming after interruption

---

#### `/sb-issue-view`
**Issue/Epic visualization**

View Beads issues with Second Brain context: tasks, notes, time tracking.

Quick mode:
```
/sb-issue-view BACK-123
/sb-issue-view epic-042
```

Shows:
- Issue/epic details
- Dependencies and blockers
- Linked Second Brain tasks
- Work progress and timeline
- Child issues (for epics)

Perfect for:
- Sprint planning
- Dependency management
- Epic progress tracking
- Status updates

---

#### `/sb-explore-tags`
**Discover content by tags**

Explore all content tagged with specific tags, see tag usage statistics.

Quick mode:
```
/sb-explore-tags performance
/sb-explore-tags research,ml,experiments
/sb-explore-tags --show-all
```

Shows:
- All content with tag(s)
- Related tags
- Tag usage statistics
- Content breakdown

Perfect for:
- Finding themes across projects
- Topic-based reviews
- Improving tagging strategy
- Discovering related work

---

#### `/sb-transcript-view`
**Meeting transcript viewer**

View transcripts with action items, linked tasks, and related content.

Quick mode:
```
/sb-transcript-view 45
/sb-transcript-list --tags meeting,planning
```

Shows:
- Full transcript
- Summary and action items
- Linked tasks and projects
- Related notes
- Action item tracking

Perfect for:
- Reviewing meeting decisions
- Tracking action items
- Finding past discussions
- Calculating meeting ROI

---

### Basic CLI Commands

#### `/sb-log`
**Add a work log entry using CLI**

Agent helps you construct the `sb log add` command with proper options.

Example usage:
```
/sb-log
```

Agent asks: "What did you work on?"
You: "Fixed authentication bug in production"
Agent: "Any task ID? Time spent?"
You: "Task #15, spent 90 minutes"
Agent shows: `sb log add "Fixed authentication bug in production" --task-id 15 --time 90`
Agent: "Should I run this for you?"
You: "Yes"
Agent: Executes the command and confirms it was added

---

#### `/sb-current-work`
**Show what you're currently working on**

Runs multiple `sb` commands to give you a quick status check.

Example usage:
```
/sb-current-work
```

Agent runs:
- `sb task list --status in_progress` - Active work
- `sb log show --days 1` - Today's log
- `sb task list --priority high --status todo` - Urgent items

Agent shows formatted summary of all results.

---

#### `/sb-daily-summary`
**End-of-day summary using CLI**

Runs `sb` commands to create an end-of-day wrap-up.

Example usage:
```
/sb-daily-summary
```

Agent runs:
- `sb log show --days 1` - Today's work
- `sb task list` - All tasks to find completed ones

Agent creates summary:
- Work logged today
- Tasks completed
- What's still in progress
- Encouraging wrap-up message

---

### Task Management Commands

#### `/sb-task-create`
**Create a new task using CLI**

Helps construct the `sb task add` command with all options.

Example usage:
```
/sb-task-create
```

Agent asks:
- Task title
- Which project
- Priority level
- Description

Agent shows: `sb task add "Title" --project SLUG --priority high`
Agent executes and shows you the task ID for future reference.

---

#### `/sb-task-update`
**Update task status, priority, or time**

Change task status, add time tracking, or update priority.

Example usage:
```
/sb-task-update
```

If you don't provide a task ID:
- Agent shows current tasks to choose from

Then agent asks what to update:
- Status (todo → in_progress → done)
- Time spent
- Priority

---

#### `/sb-find-task`
**Find tasks with filters**

Search and filter tasks by project, status, or priority.

Example usage:
```
/sb-find-task
```

Agent asks:
- Filter by project?
- Filter by status?
- Filter by priority?

Returns matching tasks with IDs for quick reference.

---

### Project Management Commands

#### `/sb-project-create`
**Create a new project**

Set up a new project with description, tags, and optional Jira integration.

Example usage:
```
/sb-project-create
```

Agent asks:
- Project name
- Description
- Tags
- Jira project key (if you use Jira)

Agent creates project and tells you the slug to use for referencing it.

---

#### `/sb-project-status`
**Get detailed project status**

See comprehensive project overview with task breakdown, time tracking, and recent activity.

Example usage:
```
/sb-project-status
```

If you don't specify a project:
- Agent shows list of active projects to choose from

Shows:
- Task breakdown by status
- Active and completed tasks
- Time tracked
- Blockers

---

#### `/sb-projects-overview`
**Overview of all projects**

Birds-eye view of all active and completed projects.

Example usage:
```
/sb-projects-overview
```

Shows:
- All active projects with task counts
- Recently completed projects
- Overall statistics
- Recommendations

---

### Reporting Commands

#### `/sb-report`
**Generate comprehensive work report**

Create detailed report for any time period - perfect for status updates and reviews.

Example usage:
```
/sb-report
```

Agent asks:
- Time period (last week, last month, etc.)
- Filter by project?

Generates report with:
- Summary statistics
- Completed tasks
- Daily work logs
- Project breakdown

Great for:
- Weekly status updates
- Performance reviews
- Promotion documentation

---

#### `/sb-weekly-review`
**Comprehensive weekly review**

Structured weekly review with accomplishments, in-progress work, blockers, and planning for next week.

Example usage:
```
/sb-weekly-review
```

Agent creates structured review with:
- Week at a glance statistics
- Accomplishments
- In-progress items
- Blockers to address
- Project breakdown
- Reflection questions
- Next week planning

Perfect for Friday afternoon wrap-up!

---

## Usage Tips

### 1. Start with Workflow Guides

**Instead of piecing together individual commands, use the comprehensive workflow guides:**

```
# Complete daily workflow
/sb-daily-dev-workflow    # Full morning → evening routine

# Research workflow
/sb-ml-research-workflow  # Complete experiment tracking

# Feature development
/sb-feature-development   # Epic → issues → tasks → notes
```

These guides show you the full picture and teach Second Brain patterns.

---

### 2. Combine Commands for Custom Workflows

**Once you know the basics, combine commands:**

**Morning routine:**
```
/sb-current-work          # See what's active
/sb-task-update           # Start working on a task
```

**During work:**
```
/sb-log                   # Log work as you go
/sb-task-update           # Add time tracking
```

**End of day:**
```
/sb-daily-summary         # Review the day
/sb-task-update           # Mark tasks as done
```

**Weekly:**
```
/sb-weekly-summary        # Friday review
/sb-report                # Generate report
```

---

### 3. Use Quick Mode for Speed

**All commands support quick mode with arguments:**

Instead of conversational back-and-forth:
```
# Quick mode - instant execution
/sb-log "Fixed bug" --task-id 42 --time 90
/sb-task-create "Feature" --project backend --priority high
/sb-note-search "Redis" --tags performance

# vs Conversational mode - agent asks questions
/sb-log
[Agent asks: "What did you work on?"]
[Agent asks: "Task ID?"]
[Agent asks: "Time spent?"]
```

See `/sb-quick-mode` for full syntax reference.

Perfect for:
- Repetitive operations
- Batch processing
- When you know all parameters
- Speed over guidance

---

### 4. Keep Task IDs Handy

Many commands need task IDs. Quick ways to find them:

```
/sb-current-work          # Shows in-progress tasks with IDs
/sb-find-task            # Search for specific tasks
/sb-project-status       # See all tasks for a project
```

Save common task IDs in a note for quick reference!

---

### 4. Use Natural Language

You don't need to be formal. The commands are designed for natural conversation:

```
User: /sb-log
Agent: "What did you work on?"
User: "fixed that annoying bug in the auth service, took forever"
Agent: "Great! Any task ID? Time spent?"
User: "15, like 2 hours"
Agent: Logs it with proper formatting
```

---

### 5. Customize Commands

These are examples! Edit them to fit your workflow:

```bash
# Edit a command
vim .claude/commands/sb-log.md

# Add custom fields
# Change the questions asked
# Modify the output format
```

---

### 6. Create Your Own

Create custom commands for your specific needs:

```bash
# Example: Daily standup helper
cat > .claude/commands/sb-standup.md <<'EOF'
Use Second Brain MCP tools to prepare for daily standup.

Show:
1. What I did yesterday (yesterday's work log)
2. What I'm doing today (in-progress tasks)
3. Any blockers (blocked tasks)

Format as a standup update.
EOF
```

---

## Command Quick Reference

### Workflow Guides (Comprehensive)

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `/sb-daily-dev-workflow` ⭐ | Complete daily dev workflow | Every workday - morning to evening |
| `/sb-ml-research-workflow` | ML research & experiments | Research projects, model development |
| `/sb-feature-development` | Large feature development | Complex multi-component features |
| `/sb-bug-investigation` | Bug investigation & postmortem | Complex bugs, production incidents |
| `/sb-weekly-summary` | Weekly summary & reporting | Friday wrap-up, team updates |
| `/sb-quick-tasks` | Small task management | Quick wins, small fixes |
| `/sb-epic-project-create` ⭐ | Create epic + project together | Starting new features, complex initiatives |

### Query & Visualization Commands

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `/sb-search-all` | Global search across everything | Finding info, discovering related content |
| `/sb-note-search` | Search/filter notes | Finding specific notes, filtering by context |
| `/sb-project-view` | Comprehensive project view | Standup prep, project reviews, updates |
| `/sb-task-view` | Complete task context | Before starting work, creating handoffs |
| `/sb-issue-view` | Issue/Epic visualization | Sprint planning, dependency management |
| `/sb-explore-tags` | Discover content by tags | Finding themes, topic-based reviews |
| `/sb-transcript-view` | Meeting transcript viewer | Reviewing decisions, tracking actions |

### Basic Commands

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `/sb-log` | Add work log entry | Throughout the day, logging work |
| `/sb-current-work` | Show active work | Starting work, after breaks |
| `/sb-daily-summary` | Day summary | End of day review |
| `/sb-task-create` | Create task | Planning, breaking down work |
| `/sb-task-update` | Update task | Changing status, tracking time |
| `/sb-find-task` | Search tasks | Finding specific tasks |
| `/sb-project-create` | Create project | Starting new initiatives |
| `/sb-project-status` | Project details | Checking project progress |
| `/sb-projects-overview` | All projects | Weekly planning, big picture |
| `/sb-report` | Generate report | Status updates, reviews |
| `/sb-weekly-review` | Weekly review | Friday wrap-up, planning |

---

## Troubleshooting

### Slash Command Not Found

**Problem:** Typing `/sb-log` doesn't show in autocomplete

**Solutions:**
1. Check file is in `.claude/commands/` directory
2. Ensure file has `.md` extension
3. Restart Claude Code
4. Verify file permissions (should be readable)

---

### Command Runs But Doesn't Work

**Problem:** Command executes but MCP tools fail

**Solutions:**
1. Verify MCP server is configured (see [INSTALLATION.md](../INSTALLATION.md))
2. Check MCP server is running (test with direct MCP tool call)
3. Verify SECOND_BRAIN_DATA_DIR is set correctly
4. Check Second Brain is properly installed

Test MCP server:
```
In Claude Code:
"Use Second Brain to list my projects"
```

If this works, slash commands should work too.

---

### Commands Are Slow

**Problem:** Slash commands take a long time to execute

This is normal! The agent needs to:
1. Read the command prompt
2. Ask clarifying questions
3. Call MCP tools
4. Format results

To speed up:
- Provide all info upfront: `/sb-log` then immediately say "Worked on task 5 for 60 minutes"
- Use simpler commands for quick checks
- Combine multiple operations into one custom command

---

## Advanced Usage

### Creating Contextual Commands

Create commands specific to your project:

```bash
# Mobile app project specific
cat > .claude/commands/sb-mobile-status.md <<'EOF'
Use Second Brain to show status of the "mobile-app-redesign" project.
Include active tasks and recent progress.
EOF
```

### Combining with Other Tools

Slash commands can use multiple MCP servers:

```bash
cat > .claude/commands/dev-status.md <<'EOF'
1. Use Second Brain to show my current tasks
2. Use GitHub MCP to show my open PRs
3. Combine into a comprehensive dev status
EOF
```

### Creating Workflows

Chain multiple commands:

```bash
cat > .claude/commands/sb-end-day.md <<'EOF'
Execute end-of-day workflow:
1. Use /sb-daily-summary to review the day
2. Ask if any tasks should be marked done
3. Use /sb-task-update to update task statuses
4. Suggest what to work on tomorrow
EOF
```

---

## Examples in Action

### Example 1: Quick Work Logging

```
You: /sb-log
Agent: What did you work on?
You: Code review for PR #234
Agent: Any task ID to link this to?
You: No
Agent: Time spent in minutes?
You: 30
Agent: ✓ Work log entry added for 2025-01-17
Entry: Code review for PR #234 (30m)
```

---

### Example 2: Task Management

```
You: /sb-task-create
Agent: What is the task title?
You: Implement rate limiting for API
Agent: Which project?
You: api-v2-migration
Agent: Priority?
You: high
Agent: Any description?
You: Add rate limiting middleware to prevent abuse
Agent: ✓ Task created!
ID: 42
Title: Implement rate limiting for API
Project: API v2 Migration
Priority: high
Status: todo

Tip: Start working with /sb-task-update
```

Later:
```
You: /sb-task-update
Agent: Which task? (showing in-progress tasks)
You: 42
Agent: What to update?
You: Change status to in_progress
Agent: ✓ Task #42 updated!
Status: in_progress
```

---

### Example 3: Weekly Review

```
You: /sb-weekly-review
Agent: [Generates comprehensive weekly review]

**Weekly Review** (Jan 10-17, 2025)

**📊 Week at a Glance:**
- Work days logged: 5
- Tasks completed: 12
- Total time tracked: 28h 30m
- Active projects: 3

**✅ Accomplishments:**
- Implemented rate limiting (API v2 Migration)
- Fixed authentication bug (Backend Services)
- Completed mobile UI mockups (Mobile Redesign)
[... more details ...]

Agent: Great week! You completed 12 tasks. What went well?
You: Good progress on the API migration
Agent: Nice! Any blockers to address next week?
```

---

## Next Steps

1. ✅ Copy commands to your `.claude/commands/` directory
2. ✅ Restart Claude Code
3. ✅ Try `/sb-current-work` to start
4. ✅ Customize commands to fit your workflow
5. ✅ Create your own custom commands

For more information:
- [Installation Guide](../docs/installation.md) - Setup instructions
- [CLI Reference](../docs/cli-reference.md) - CLI command reference
- [Workflows Guide](../docs/workflows.md) - Usage patterns
- [MCP Server Guide](../docs/mcp-server.md) - MCP tool details
- [Slash Commands](../docs/slash-commands.md) - This guide in docs/

---

**Happy tracking! 🧠**

Use these commands to make Second Brain a seamless part of your daily workflow!
