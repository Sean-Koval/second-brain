Global search across all Second Brain content: notes, tasks, projects, work logs, transcripts, and issues.

This command supports TWO MODES:

## Quick Mode (with arguments)

```
/sb-search-all "caching strategy"
/sb-search-all "performance" --type note
/sb-search-all "API" --project backend-api
/sb-search-all "bug" --date-range last-week
```

## Conversational Mode (no arguments)

If no search query specified, ask:
1. What would you like to search for?
2. Filter by type? (note, task, project, transcript, issue, work_log, all)
3. Filter by project? (optional)
4. Filter by date range? (optional)

## What to Search

Search across ALL content types:
- ✅ Notes (title + content)
- ✅ Tasks (title + description)
- ✅ Projects (name + description)
- ✅ Work Logs (entry text)
- ✅ Transcripts (summary + raw content)
- ✅ Beads Issues (title + description)

## Output Format

```
╔════════════════════════════════════════════════════════════╗
║ 🔍 SEARCH: "caching"                                       ║
╚════════════════════════════════════════════════════════════╝

Found 24 results across 5 content types

─────────────────────────────────────────────────────────────

📝 NOTES (8 results)

📄 Note #156: "Redis Caching Strategy"
   Project: backend-api | Task: #42
   Tags: architecture, caching, redis
   Created: 2025-01-15

   Match: "We decided to use Redis cluster for **caching**
          with 3 nodes and 2 replicas per master for high
          availability..."

   [View: /sb-note-show 156]

📄 Note #143: "Database Query **Caching**"
   Project: backend-api
   Tags: performance, database, caching
   Created: 2025-01-10

   Match: "Implemented query result **caching** to reduce
          database load. Using 5-minute TTL..."

   [View: /sb-note-show 143]

... (6 more notes)

─────────────────────────────────────────────────────────────

📋 TASKS (6 results)

🚧 #42: "Implement Redis **caching**"
   Project: backend-api
   Status: in_progress | Priority: high
   Created: 2025-01-10

   Match in description: "Improve API response times using
   Redis **caching**. Target: <10ms avg response time."

   [View: /sb-task-view 42]

✅ #35: "Add database connection pool and **caching**"
   Project: backend-api
   Status: done | Completed: 2025-01-12

   [View: /sb-task-view 35]

... (4 more tasks)

─────────────────────────────────────────────────────────────

💼 WORK LOGS (5 results)

2025-01-17 | Task #42
   "Completed Redis cluster configuration for **caching**"
   Time: 90m

2025-01-16 | Task #42
   "Implemented **caching** invalidation logic"
   Time: 75m

2025-01-15 | Task #42
   "Initial Redis **caching** setup and testing"
   Time: 60m

... (2 more logs)

─────────────────────────────────────────────────────────────

📞 TRANSCRIPTS (2 results)

📞 Transcript #45: "API Performance Review"
   Date: 2025-01-11 | Type: meeting
   Tags: performance, planning, api

   Match: [03:20] sarah: "We could use Redis for **caching**.
          I'm thinking 3 master nodes with 2 replicas each..."

   [View: /sb-transcript-view 45]

📞 Transcript #40: "Q1 Engineering Planning"
   Date: 2025-01-05 | Type: planning
   Tags: planning, architecture

   Match in summary: "Discussed implementing **caching**
   layer as Q1 priority for performance improvements"

   [View: /sb-transcript-view 40]

─────────────────────────────────────────────────────────────

🎯 ISSUES (3 results)

Issue API-046: "Redis **caching** implementation"
   Status: in_progress | Priority: 4 (urgent)
   Epic: API Performance Improvements
   Linked to: Task #42

   Match: "Implement distributed **caching** using Redis
   cluster to improve API response times"

   [View: /sb-issue-view API-046]

Issue API-032: "Evaluate **caching** strategies"
   Status: done | Completed: 2025-01-09
   Epic: API Performance Improvements

   [View: /sb-issue-view API-032]

... (1 more issue)

─────────────────────────────────────────────────────────────

📊 SEARCH INSIGHTS

Timeline:
  • First mention: 2025-01-05 (Q1 Planning transcript)
  • Peak activity: 2025-01-15 - 2025-01-17
  • Latest mention: 2025-01-17

Content Clusters:
  • Redis cluster implementation (8 items)
  • Database query caching (4 items)
  • API response caching (6 items)

Most Related:
  • Project: backend-api (18 results)
  • Task: #42 (10 results)
  • Tags: performance, redis, optimization

Suggested Next:
  • View task #42 for full context
  • Explore "performance" tag
  • View API-046 issue details

─────────────────────────────────────────────────────────────
```

## Filtered Search

### By Type

```
/sb-search-all "API" --type note

╔════════════════════════════════════════════════════════════╗
║ 🔍 SEARCH: "API" | Type: notes                             ║
╚════════════════════════════════════════════════════════════╝

Found 12 notes

📄 Note #201: "**API** Design Decisions"
📄 Note #156: "Redis Caching for **API**"
📄 Note #189: "**API** Rate Limiting Strategy"
...
```

### By Project

```
/sb-search-all "performance" --project backend-api

╔════════════════════════════════════════════════════════════╗
║ 🔍 SEARCH: "performance" | Project: backend-api            ║
╚════════════════════════════════════════════════════════════╝

Found 18 results in backend-api project

📝 Notes: 7 results
📋 Tasks: 6 results
💼 Work Logs: 5 results
...
```

### By Date Range

```
/sb-search-all "bug" --date-range last-week

╔════════════════════════════════════════════════════════════╗
║ 🔍 SEARCH: "bug" | Date: Last 7 days                       ║
╚════════════════════════════════════════════════════════════╝

Found 9 results in last week

📋 Task #55: "Fix authentication **bug**" (created 2025-01-14)
💼 Work Log: "Fixed login **bug**" (2025-01-15)
📝 Note #167: "**Bug** Investigation" (2025-01-15)
...
```

## Follow-up Actions

After showing search results, offer to:
- View detailed content of specific result
- Narrow search with additional filters
- Create new content related to search
- Export search results
- Save search as filter

## MCP Tools Used

```python
# Search across different types
search_notes(query="caching")
get_tasks()  # then filter by keyword
get_work_logs()  # then filter by keyword
get_transcripts()  # then filter by keyword
list_issues()  # then filter by keyword

# Apply filters
if project_slug:
    # Filter results by project
if date_range:
    # Filter results by date
if content_type:
    # Only search specific type
```

## CLI Commands

If using CLI instead of MCP:

```bash
# Note search
sb note search "caching"

# Task search (manual grep)
sb task list | grep -i "caching"

# Work log search
sb log show --days 30 | grep -i "caching"

# No unified search command
# Need to search each type separately
```

## Usage Examples

### Quick global search
```
User: /sb-search-all "caching"

Agent: [Searches all content types]
       Found 24 results:
       - 8 notes
       - 6 tasks
       - 5 work logs
       - 2 transcripts
       - 3 issues
```

### Search specific type
```
User: /sb-search-all "API" --type note

Agent: [Searches only notes]
       Found 12 notes matching "API"
```

### Search in project
```
User: /sb-search-all "performance" --project backend-api

Agent: [Searches only backend-api content]
       Found 18 results in backend-api
```

### Search recent content
```
User: /sb-search-all "bug" --date-range last-week

Agent: [Searches last 7 days]
       Found 9 results in last week
```

### Conversational search
```
User: /sb-search-all

Agent: "What would you like to search for?"

User: "authentication"

Agent: "Filter by type? (note, task, all, etc.)"

User: "all"

Agent: [Shows all results for "authentication"]
```

### Discovery workflow
```
User: /sb-search-all "Redis"

Agent: [Shows 15 results including notes, tasks, transcripts]

User: "Show me the Redis strategy note"

Agent: [Uses /sb-note-show 156]
```

### Drill down
```
User: /sb-search-all "caching"

Agent: [Shows results including Task #42 mentioned 10 times]

User: "Show me task 42"

Agent: [Uses /sb-task-view 42]
       [Shows full task with all caching-related content]
```

## Pro Tips

### 1. Use Quotes for Exact Phrases

```
/sb-search-all "Redis cluster"    # Exact phrase
/sb-search-all Redis cluster      # Either word
```

### 2. Combine with Type Filter

```
# Find all bug-related notes
/sb-search-all "bug" --type note

# Find all performance tasks
/sb-search-all "performance" --type task
```

### 3. Use Date Filters for Recent Work

```
# What did I work on with caching this week?
/sb-search-all "caching" --date-range last-week

# Find old decisions
/sb-search-all "decided" --date-range 2024
```

### 4. Project-Scoped Search

```
# Everything about API in backend project
/sb-search-all "API" --project backend-api

# Find all frontend notes
/sb-search-all "" --type note --project frontend
```

### 5. Search for Decisions

```
# Find all decision records
/sb-search-all "decided" --type note

# Or use tags
/sb-explore-tags decision
```

### 6. Find Incomplete Work

```
# Search for "TODO" in notes
/sb-search-all "TODO" --type note

# Find tasks mentioning "later"
/sb-search-all "later" --type task
```

### 7. Research Preparation

Before starting work:
```
/sb-search-all "topic name"
[See all past work on this topic]
[Avoid duplicating research]
```

### 8. Knowledge Recovery

Can't remember where you documented something?
```
/sb-search-all "that specific detail"
[Find across all content types]
```

## Search Best Practices

### Tag Important Content

Make it easier to find:
```
Tags: decision, important, key-finding
```

### Use Consistent Terminology

Standardize terms:
```
"Redis cache" (not "Redis caching", "cache with Redis")
"API endpoint" (not "API route", "endpoint")
```

### Document Decisions

Make them searchable:
```
"We decided to use X because Y"
"Decision: Use Redis cluster"
```

### Reference Related Content

In notes:
```
"See Task #42 for implementation"
"Related to Note #156 (architecture)"
```

## Common Search Patterns

```
# Research topic
/sb-search-all "topic" --type note

# Find task
/sb-search-all "feature name" --type task

# Track decision
/sb-search-all "decided" --type transcript

# Find bug work
/sb-search-all "bug" --project PROJECT

# Recent activity
/sb-search-all "" --date-range last-week

# Meeting discussions
/sb-search-all "topic" --type transcript

# Work timeline
/sb-search-all "feature" --type work_log
```

---

Use global search to:
- Find information quickly
- Discover related content
- Avoid duplicate work
- Track decisions across time
- Research before starting work
- Recover lost context
- Generate reports by keyword
