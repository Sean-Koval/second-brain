# Note Taking

Second Brain includes a powerful note-taking system for capturing thoughts, context, and important information about your work.

## Overview

Notes in Second Brain are:
- **Markdown-based**: Rich text formatting with full markdown support
- **Indexed**: Fast searchable database + human-readable files
- **Flexible**: Can be standalone or attached to projects/tasks
- **Timestamped**: Automatic tracking of creation and updates
- **Taggable**: Organize with tags for easy discovery

## Creating Notes

### Standalone Notes

Create a note without any attachments:

```bash
sb note create "Meeting Notes" --content "Key points from today's discussion"
```

### Project Notes

Attach a note to a project:

```bash
sb note create "Architecture Decisions" \
  --project my-project \
  --content "## Tech Stack\n\n- Backend: Python/FastAPI\n- DB: PostgreSQL"
```

### Task Notes

Attach a note to a specific task:

```bash
sb note create "Implementation Details" \
  --task-id 42 \
  --content "## Approach\n\nWe'll use async patterns..."
```

### Tagged Notes

Add tags for organization:

```bash
sb note create "Research Findings" \
  --content "..." \
  --tags research,ai,embeddings
```

## Managing Notes

### List Notes

List all notes:

```bash
sb note list
```

Filter by project:

```bash
sb note list --project my-project
```

Filter by task:

```bash
sb note list --task-id 42
```

Filter by tags:

```bash
sb note list --tags research,ai
```

### View Note

Show full note content:

```bash
sb note show 5
```

### Append Content

Add timestamped content to an existing note:

```bash
sb note add 5 "## Update\n\nNew findings from testing..."
```

This appends with a timestamp separator, preserving the note's history.

### Search Notes

Full-text search across all notes:

```bash
sb note search "dependency injection"
```

Searches both titles and content.

## MCP Server Tools

### create_note

Create a new note:

```python
{
  "title": "API Design Decisions",
  "content": "## REST vs GraphQL\n\nWe decided to use REST because...",
  "project_slug": "backend-api",
  "tags": ["architecture", "api"]
}
```

### append_to_note

Add content to existing note:

```python
{
  "note_id": 5,
  "content": "## Follow-up\n\nAfter discussion with team..."
}
```

### update_note

Update note properties:

```python
{
  "note_id": 5,
  "title": "Updated Title",
  "content": "Completely new content",
  "tags": ["updated", "tags"]
}
```

### get_notes

Query notes with filters:

```python
{
  "project_slug": "my-project",
  "tags": ["architecture"]
}
```

### get_note

Get specific note:

```python
{
  "note_id": 5
}
```

### search_notes

Full-text search:

```python
{
  "query": "authentication"
}
```

## File Structure

Notes are stored as markdown files:

```
data/notes/
  note-1.md
  note-2.md
  note-3.md
```

Each file has YAML frontmatter with metadata:

```markdown
---
id: 1
title: "My Note"
created_at: "2025-01-15T10:30:00"
updated_at: "2025-01-15T14:20:00"
project_id: 5
task_id: 42
tags:
  - research
  - important
---

# My Note

Note content here...
```

## Use Cases

### 1. Meeting Notes

Capture meeting notes and link to relevant project:

```bash
sb note create "Weekly Standup 2025-01-15" \
  --project team-project \
  --content "## Attendees\n\n- Alice\n- Bob\n\n## Discussion\n\n..."
```

### 2. Task Context

Add detailed context to a task:

```bash
# Create task
sb task add "Implement OAuth" --project auth-service

# Add detailed implementation notes
sb note create "OAuth Implementation Details" \
  --task-id 15 \
  --content "## Libraries\n\n- authlib\n- python-jose\n\n## Flow\n\n..."
```

### 3. Research Notes

Organize research with tags:

```bash
sb note create "Vector DB Comparison" \
  --tags research,databases,vectors \
  --content "## Options\n\n### Pinecone\n- Pros:...\n\n### Weaviate\n- Pros:..."
```

### 4. Knowledge Base

Build a searchable knowledge base:

```bash
# Add various notes
sb note create "How to Deploy" --tags deployment,howto
sb note create "Debugging Guide" --tags debugging,howto
sb note create "API Patterns" --tags architecture,patterns

# Search later
sb note search "deployment"
sb note list --tags howto
```

### 5. Incremental Documentation

Build documentation incrementally:

```bash
# Create initial note
sb note create "System Design" --project my-app

# Add to it over time
sb note add 1 "## Database Schema\n\nAdded users table..."
sb note add 1 "## API Endpoints\n\nAdded /auth endpoints..."
```

## Best Practices

### 1. Use Descriptive Titles

Good:
- "Authentication Flow Decisions"
- "Performance Testing Results - Jan 2025"
- "Customer Feedback - Feature X"

Bad:
- "Notes"
- "TODO"
- "Stuff"

### 2. Tag Consistently

Create a tagging scheme and stick to it:

```bash
# Domain tags
--tags backend,frontend,database,devops

# Type tags
--tags research,decision,reference,howto

# Status tags
--tags draft,final,archived
```

### 3. Link to Context

Always attach notes to projects/tasks when relevant:

```bash
# ✅ Good - provides context
sb note create "Performance Analysis" --project api-service

# ❌ Less useful - orphaned note
sb note create "Performance Analysis"
```

### 4. Append Don't Rewrite

Use `sb note add` to preserve history:

```bash
# ✅ Good - preserves timeline
sb note add 5 "## Update 2025-01-16\n\nNew findings..."

# ❌ Bad - loses history
sb note show 5 > temp.md
# edit temp.md
sb note update 5 --content "$(cat temp.md)"
```

### 5. Search-Optimized Content

Write notes to be discoverable:

```markdown
# OAuth Implementation

Keywords: authentication, authorization, JWT, tokens, security

## Overview

This note covers our OAuth 2.0 implementation using the authorization code flow...
```

## Tips

### Quick Capture

Create a quick note template:

```bash
# Save to ~/.bashrc or ~/.zshrc
qnote() {
  sb note create "$1" --content "Quick note created $(date)"
}

# Usage
qnote "Remember to check the logs"
```

### Batch Viewing

View multiple notes:

```bash
for id in 1 2 3 4 5; do
  echo "=== Note $id ==="
  sb note show $id
  echo
done
```

### Export Notes

Export notes to a single file:

```bash
sb note list --project my-project | grep "^#" | while read -r line; do
  id=$(echo $line | grep -oP '#\K\d+')
  sb note show $id
  echo "---"
done > project-notes.md
```

## Integration with Tasks and Issues

Notes work seamlessly with both Second Brain tasks and Beads issues. See the [Task-Issue Integration](task-issue-integration.md) guide for complete workflows.

Quick example:

```bash
# Create issue with linked task
sb issue create "Build Dashboard" --with-task --project analytics

# Add implementation notes to the task
sb note create "Dashboard Implementation" \
  --task-id 10 \
  --content "## Component Structure\n\n..."
```

The note is attached to the Second Brain task, which is linked to the Beads issue, giving you the full stack:
- **Beads Issue**: Dependency tracking, blockers
- **SB Task**: Time tracking, project linking
- **Note**: Rich documentation, implementation details
