Search notes by keyword, tag, project, or task.

This command supports TWO MODES:

## Quick Mode (with arguments)

```
/sb-note-search "keyword to search"
/sb-note-search --tags research,important
/sb-note-search --project backend-api
/sb-note-search --task-id 42
```

## Conversational Mode (no arguments)

If no arguments provided, ask:
1. What would you like to search for? (keyword, or leave empty for all)
2. Filter by project? (project slug, optional)
3. Filter by task? (task ID, optional)
4. Filter by tags? (comma-separated, optional)

## Using MCP Tools

Use the MCP tool `search_notes` for keyword search:
```python
search_notes(query="keyword")
```

Or use `get_notes` for filtering:
```python
get_notes(
    project_slug="backend-api",
    task_id=42,
    tags=["research", "important"]
)
```

## Output Format

Present results in a clean, readable format:

```
Found X notes:

📝 Note #123: "Redis Caching Strategy"
   Project: backend-api
   Task: #42
   Tags: performance, caching, redis
   Created: 2025-01-15
   Preview: "We decided to use Redis cluster with 3 nodes..."

📝 Note #124: "API Design Decisions"
   Project: backend-api
   Tags: architecture, design
   Created: 2025-01-14
   Preview: "REST vs GraphQL trade-offs..."

📝 Note #125: "Performance Benchmarks"
   Task: #42
   Tags: performance, testing
   Created: 2025-01-16
   Preview: "Baseline: 50ms, After optimization: 5ms..."
```

## Usage Examples

### Find notes about a specific topic
```
User: /sb-note-search "caching"
Agent: Shows all notes mentioning "caching"
```

### Find research notes
```
User: /sb-note-search --tags research
Agent: Shows all notes tagged with "research"
```

### Find notes for a task
```
User: /sb-note-search --task-id 42
Agent: Shows all notes linked to task #42
```

### Find project notes
```
User: /sb-note-search --project backend-api
Agent: Shows all notes for backend-api project
```

### Combined search
```
User: /sb-note-search "performance" --project backend-api --tags optimization
Agent: Shows performance-related optimization notes in backend-api
```

## CLI Commands

If using CLI instead of MCP:

```bash
# Search by keyword
sb note search "keyword"

# List with filters
sb note list --project backend-api
sb note list --task-id 42
sb note list --tags research,important
```

## Follow-up Actions

After showing results, offer to:
- Show full content of a specific note
- Create a new related note
- Add content to an existing note
- Export notes to a file
