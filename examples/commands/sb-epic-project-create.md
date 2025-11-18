Create an epic and linked Second Brain project together for a new initiative.

This is the **recommended way to start a new feature or complex work**. It creates both:
- A **Beads epic** for high-level coordination, dependency tracking, and blockers
- A **Second Brain project** for day-to-day notes, tasks, and time tracking
- Links them together with the same title and tags

This command supports TWO MODES:

## Quick Mode (with arguments)

If the user provides arguments after the command, parse them and execute immediately.

Examples:
```
/sb-epic-project-create "New Feature X" --description "Build feature X" --priority 3 --labels feature,backend
/sb-epic-project-create "API Redesign" --labels api,refactor
/sb-epic-project-create "Mobile App" --description "iOS and Android apps" --priority 4 --labels mobile,frontend --jira-project MOB
```

Syntax:
```
/sb-epic-project-create "TITLE" [OPTIONS]

Options:
  --description, -d TEXT    Description for both epic and project
  --priority, -p INT        Epic priority 0-4 (0=lowest, 4=highest) [default: 2]
  --labels, -l TEXT         Comma-separated labels/tags for both
  --jira-project, -j TEXT   Jira project key for the project (optional)
```

## Conversational Mode (no arguments)

If the user just types `/sb-epic-project-create` with no arguments, guide them through creating an epic + project by asking:

1. **Title**: What's the name of this initiative? (will be used for both epic and project)
2. **Description**: Brief description? (optional, used for both)
3. **Priority**: What priority? (0=lowest, 1=low, 2=medium, 3=high, 4=highest) [default: 2]
4. **Labels/Tags**: Any labels or tags? (comma-separated, optional, used for both)
5. **Jira Project Key**: Jira project key? (optional, for project only)

Then execute either:

### Using MCP Tool (preferred)
```python
create_epic_with_project(
    title="TITLE",
    description="DESCRIPTION",
    priority=PRIORITY,
    labels=["label1", "label2"],
    jira_project_key="JIRA"
)
```

### Using CLI Command (alternative)
```bash
sb issue create-with-project "TITLE" \
  --description "DESCRIPTION" \
  --priority PRIORITY \
  --labels label1,label2 \
  --jira-project JIRA
```

## What This Creates

### Epic (in Beads)
- High-level work item for coordination
- Tracks dependencies between issues
- Identifies blockers
- Can have child issues
- Used for `sb issue ready` to find unblocked work

### Project (in Second Brain)
- Container for tasks, notes, and work logs
- Detailed implementation tracking
- Time tracking
- Markdown file for rich notes
- Database for fast queries

### Next Steps After Creation

After creating the epic + project, guide the user on:

1. **Create issues under the epic**:
   ```bash
   sb issue create "Issue Title" --epic EPIC_ID --type feature
   ```

2. **Create tasks in the project**:
   ```bash
   sb task add "Task Title" --project PROJECT_SLUG
   ```

3. **Link issues to tasks** (recommended):
   ```bash
   sb issue create "Issue Title" --epic EPIC_ID --with-task --project PROJECT_SLUG
   ```

4. **Add notes to project or tasks**:
   ```bash
   sb note create "Architecture Notes" --project PROJECT_SLUG
   sb note create "Implementation Notes" --task-id TASK_ID
   ```

5. **Track work**:
   ```bash
   sb log add "Work description" --task-id TASK_ID --time 90
   ```

## Example Workflow

**User**: "I'm starting a new feature to add user authentication"

**Agent**:
```
I'll create an epic and project for "User Authentication".

Creating:
- Epic in Beads for dependency tracking
- Project in Second Brain for notes and time tracking

✓ Epic created: auth-001
✓ Project created: user-authentication

Next steps:
1. Create issues for the work items:
   - sb issue create "OAuth integration" --epic auth-001 --with-task --project user-authentication
   - sb issue create "Login UI" --epic auth-001 --with-task --project user-authentication

2. Add architectural notes:
   - sb note create "Auth Architecture" --project user-authentication

3. Track dependencies:
   - If OAuth blocks Login UI: sb issue add-dependency login-ui-id oauth-id blocks
```

## When to Use This

✅ **Use this when:**
- Starting a new feature or initiative
- Work requires both dependency tracking AND detailed notes
- Multiple people will work on related issues
- You need to track blockers and find ready work
- Complex work that spans multiple tasks/issues

❌ **Don't use this when:**
- Quick one-off task (just use `sb task add`)
- No dependencies or blockers to track
- Simple work that doesn't need an epic

## Key Benefits

1. **One command** creates both coordination (epic) and execution (project) structures
2. **Same title and tags** keeps them synchronized
3. **Clear next steps** guide the user on how to populate the epic and project
4. **Integration** between Second Brain and Beads from day one
5. **Dependency tracking** via Beads + **detailed notes** via Second Brain

## Output Format

Show the user:
1. Epic details (ID, title, priority, labels)
2. Project details (ID, slug, markdown path, tags)
3. Integration mapping (Epic ID ↔️ Project Slug)
4. Concrete next steps with example commands

Make it clear which system each piece lives in (Beads vs Second Brain).
