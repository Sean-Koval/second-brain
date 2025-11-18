Show a comprehensive visualization of a task with all related content.

This command supports TWO MODES:

## Quick Mode (with arguments)

```
/sb-task-view 42
/sb-task-view 55
```

## Conversational Mode (no arguments)

If no task ID specified, ask:
1. Which task would you like to view? (show list of active tasks to choose from, or ask for ID)

## What to Show

Gather and present a comprehensive task overview:

### 1. Task Details
Query the task to get:
- Title, description
- Status, priority
- Project linkage
- Created/updated dates
- Time tracked
- Tags

### 2. Linked Issue (if any)
If task has `issue_id`, use `get_issue(issue_id)` to show:
- Issue title, status
- Epic membership
- Dependencies/blockers
- External reference

### 3. Task Notes
Use `get_notes(task_id=task_id)` to get:
- All notes attached to this task
- Implementation details
- Decision records
- Progress updates

### 4. Work Log History
Use `get_work_logs(start_date, end_date)` and filter by task:
- All logged work for this task
- Time spent breakdown
- Activity timeline

### 5. Related Transcripts (if any)
Use `get_transcripts()` and check for task references:
- Meeting discussions about this task
- Decisions made in calls

## Output Format

```
╔════════════════════════════════════════════════════════════╗
║ 📋 TASK #42: Implement Redis caching                       ║
╚════════════════════════════════════════════════════════════╝

📦 Project: Backend API (backend-api)
📊 Status: in_progress
⚡ Priority: high
📅 Created: 2025-01-10
🏷️  Tags: caching, redis, performance

📝 Description:
Implement distributed caching using Redis cluster to improve
API response times. Target: reduce average response time from
50ms to <10ms.

─────────────────────────────────────────────────────────────

⏱️  TIME TRACKING

Total time tracked: 4h 30m

Breakdown:
  • Research & planning:    1h 00m
  • Implementation:         2h 30m
  • Testing:                1h 00m

─────────────────────────────────────────────────────────────

🔗 LINKED BEADS ISSUE

Issue ID: sb-task-42
Status: In Progress
Epic: API Performance Improvements
Dependencies: None
Blockers: None

View full issue: /sb-issue-view sb-task-42

─────────────────────────────────────────────────────────────

📝 TASK NOTES (3 notes)

📄 Note #156: "Redis Caching Strategy"
   Created: 2025-01-15
   Tags: architecture, caching, redis

   ## Overview
   We decided to use Redis cluster with 3 nodes for high
   availability and automatic failover.

   ## Configuration
   - 3 master nodes
   - 2 replicas per master
   - Sentinel for monitoring

   [View full note: /sb-note-show 156]

📄 Note #157: "Implementation Progress"
   Created: 2025-01-16
   Tags: progress, implementation

   ## Completed
   - ✅ Redis cluster setup
   - ✅ Connection pooling
   - ✅ Basic cache operations

   ## In Progress
   - 🚧 Cache invalidation strategy
   - 🚧 Monitoring and metrics

   ## TODO
   - ⏳ Load testing
   - ⏳ Documentation

   [View full note: /sb-note-show 157]

📄 Note #158: "Performance Benchmarks"
   Created: 2025-01-17
   Tags: testing, performance

   ## Results

   Baseline (no cache):
   - Avg response: 50ms
   - P95: 120ms
   - P99: 250ms

   With Redis cache:
   - Avg response: 5ms ✅ (90% improvement)
   - P95: 12ms ✅
   - P99: 25ms ✅

   [View full note: /sb-note-show 158]

─────────────────────────────────────────────────────────────

📅 WORK LOG TIMELINE

2025-01-17 (90m total)
  ✓ Completed Redis cluster configuration (90m)
    Notes: 3 nodes deployed, replication configured

2025-01-16 (120m total)
  ✓ Implemented cache invalidation logic (75m)
  ✓ Added monitoring and metrics (45m)

2025-01-15 (60m total)
  ✓ Initial Redis setup and testing (60m)
    Notes: Local cluster working, ready for staging

2025-01-14 (45m total)
  ✓ Research Redis cluster best practices (45m)
    Notes: Documented findings in architecture note

─────────────────────────────────────────────────────────────

📞 RELATED TRANSCRIPTS

Transcript #45: "API Performance Review"
  Date: 2025-01-11
  Type: meeting

  Summary: Discussed caching strategy and decided on Redis
  cluster approach. Reviewed performance targets and timeline.

  [View full transcript: /sb-transcript-view 45]

─────────────────────────────────────────────────────────────

✅ NEXT STEPS

Based on notes and work log:
  1. Complete cache invalidation strategy
  2. Set up monitoring dashboards
  3. Run load tests in staging
  4. Update API documentation
  5. Deploy to production

Blockers: None
Estimated remaining: ~2h

─────────────────────────────────────────────────────────────

🎯 COMPLETION CRITERIA

From task description and notes:
  ✅ Redis cluster deployed (3 nodes)
  ✅ Cache operations implemented
  ✅ Performance target met (<10ms avg)
  🚧 Monitoring configured
  ⏳ Load testing completed
  ⏳ Documentation updated

Progress: ~75% complete

─────────────────────────────────────────────────────────────
```

## Follow-up Actions

After showing the task view, offer to:
- Update task status or add time
- Create or append to a task note
- Log additional work
- View linked issue details
- View related notes in full
- Mark task as done
- Generate task summary for handoff

## MCP Tools Used

```python
# Get task details
get_tasks(task_id=42)

# Get task notes
get_notes(task_id=42)

# Get work logs (filter by task_id)
get_work_logs(start_date, end_date)  # then filter

# Get linked issue
if task.issue_id:
    get_issue(task.issue_id)

# Get transcripts (search for task reference)
get_transcripts()  # then filter
```

## CLI Commands

If using CLI instead of MCP:

```bash
# Task details
sb task list | grep "^42"

# Task notes
sb note list --task-id 42

# Work logs (manual filter)
sb log show --days 30 | grep "#42"
```

## Usage Examples

### Quick task check
```
User: /sb-task-view 42

Agent: [Shows comprehensive task view with all notes, logs, linked issue]
```

### Find task first
```
User: /sb-task-view

Agent: "Which task? Here are your active tasks:"
       #42: Implement Redis caching (in_progress)
       #55: Fix auth bug (in_progress)
       #67: API rate limiting (todo)

User: "42"

Agent: [Shows comprehensive view]
```

### Update after viewing
```
User: /sb-task-view 42

Agent: [Shows view]

User: "Add a note about the deployment plan"

Agent: "I'll create a note for task #42"
       [Uses create_note with task_id=42]
```

### Complete the task
```
User: /sb-task-view 42

Agent: [Shows 75% complete]

User: "Mark it as done and log 120 minutes"

Agent: [Uses update_task(42, status="done", time_spent_minutes=120)]
       "✅ Task #42 marked as done! Total time: 6h 30m"
```

## Pro Tips

- Use this command:
  - Before starting work (review context)
  - During standup (quick status)
  - Before handoff (see all info)
  - When resuming after interruption
  - To create task summaries

- The visualization helps you:
  - See progress at a glance
  - Find all related documentation
  - Track time accurately
  - Identify next steps
  - Create handoff notes
