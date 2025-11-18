## Claude Code Skill for Second Brain

A comprehensive Claude Code skill that teaches Claude how to use Second Brain effectively for work tracking, note-taking, and task management in daily development workflows.

## What is This?

This is a [Claude Code](https://claude.com/claude-code) skill - a markdown-based instruction set that teaches Claude AI how to use Second Brain CLI effectively. While the MCP server and slash commands provide interactive interfaces, this skill teaches the **philosophy and patterns** of effective Second Brain usage.

## What Does It Provide?

**Main skill file (`SKILL.md`):**
- Core workflow patterns (daily dev, feature development, weekly review)
- Decision criteria for when to use Second Brain vs bd vs TodoWrite
- Session start protocols for establishing context
- Work logging, task management, and note-taking patterns
- Integration patterns with bd (beads) for dependency tracking
- CLI vs MCP vs Slash Command decision guide
- Best practices for work logs, tasks, notes, and time tracking

**Reference documentation:**
- `references/CLI_REFERENCE.md` - Complete CLI command reference with all options
- `references/WORKFLOWS.md` - Step-by-step workflows with examples
- `references/MCP_INTEGRATION.md` - MCP server tools and integration patterns
- `references/SLASH_COMMANDS.md` - Slash command workflows and quick mode syntax

## Why is This Useful?

The skill helps Claude understand:

1. **When to use Second Brain** - For persistent work tracking, notes, and time management across all projects

2. **How to structure work** - Proper use of work logs, tasks, notes, and projects with quality guidelines

3. **Workflow patterns** - Daily development, feature creation, weekly reviews, performance reporting

4. **Integration** - How Second Brain, bd (beads), and TodoWrite complement each other

## Installation

### Prerequisites

1. Install Second Brain:
   ```bash
   uv tool install git+https://github.com/seanm/second-brain.git
   ```

2. Initialize globally:
   ```bash
   sb init --global
   export SECOND_BRAIN_DIR="$HOME/.second-brain"
   # Add to ~/.bashrc or ~/.zshrc
   ```

3. Have [Claude Code](https://claude.com/claude-code) installed

### Install the Skill

You can install this skill in two ways:

#### Option 1: Copy to Claude Code Skills Directory

```bash
# From the second-brain repository
cd /path/to/second-brain/examples/skills

# Create a symlink in your Claude Code skills directory
ln -s "$(pwd)/second-brain" ~/.claude/skills/second-brain
```

#### Option 2: Copy Files Directly

```bash
# Create the skill directory
mkdir -p ~/.claude/skills/second-brain

# Copy the skill files
cp -r /path/to/second-brain/examples/skills/second-brain/* ~/.claude/skills/second-brain/
```

### Verify Installation

Restart Claude Code, then in a new session, ask:

```
Do you have the Second Brain skill installed?
```

Claude should confirm it has access to the Second Brain skill and can help with work tracking.

## How It Works

Claude Code automatically loads skills from `~/.claude/skills/`. When this skill is installed:

1. Claude gets the core workflow from `SKILL.md` immediately
2. Claude can read reference docs when it needs detailed information
3. The skill uses progressive disclosure - quick reference in SKILL.md, details in references/

## Usage Examples

Once installed, Claude will automatically:

- Check for active work at session start
- Show today's work logs
- Suggest creating tasks for multi-day work
- Know when to use CLI vs MCP vs slash commands
- Maintain proper time tracking on work logs
- Generate reports for performance reviews

You can also explicitly ask Claude to use Second Brain:

```
Let's track this work in Second Brain since it spans multiple days
```

```
Log this work to Second Brain with time tracking
```

```
Show me what I've been working on this week
```

```
Create a task for this feature work
```

## Relationship to MCP Server and Slash Commands

This skill complements the other Second Brain interfaces:

- **MCP Server**: Provides tools for AI agents to query and update Second Brain data
- **Slash Commands**: Pre-built workflows for common operations (27 commands)
- **Skill** (this directory): Teaches Claude the patterns, philosophy, and decision-making for effective usage

You can use all three together for the best experience:
- MCP Server for data queries and updates
- Slash Commands for guided workflows
- Skill for intelligent decision-making and best practices

### Why CLI Instead of MCP?

This skill teaches Claude to use the `sb` CLI directly (via Bash commands like `sb log add`, `sb task update`, etc.) rather than relying solely on MCP tools. This approach has several benefits:

- **Lower context usage** - No MCP server prompt loaded unless needed, saving tokens
- **Works everywhere** - Only requires `sb` binary installed and `SECOND_BRAIN_DIR` set
- **Explicit operations** - All commands visible in conversation history for transparency
- **Full functionality** - CLI supports all features including advanced filtering and reporting
- **User familiar** - Users can copy-paste commands to run themselves

The MCP server is excellent for complex queries and updates, but for straightforward operations where context efficiency matters, direct CLI usage is more practical. The skill provides the guidance Claude needs to use both effectively.

## Integration with bd (Beads)

Second Brain integrates seamlessly with bd (beads) for dependency tracking:

- **Second Brain**: Rich notes, time tracking, work logs, project organization
- **bd (beads)**: Dependency graphs, blocker detection, ready work finder, epic breakdown

**Use both together:**
```bash
# Create epic + project in one command
sb issue create-with-project "New Feature" --priority 4

# Create issues under epic with linked tasks
sb issue create "Component A" --epic epic-042 --with-task --project new-feature

# Find ready work (no blockers)
sb issue ready

# Log work on tasks
sb log add "Implemented Component A" --task-id 42 --time 120

# Track dependencies in beads
bd dep add component-b component-a --type blocks
```

The skill teaches Claude when to use each tool and how they complement each other.

## Contributing

Found ways to improve the skill? Contributions welcome! Open an issue or pull request at the Second Brain repository.

## License

MIT License - Same as Second Brain. See LICENSE in the main repository.
