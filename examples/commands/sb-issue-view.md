Show a comprehensive visualization of a Beads issue/epic with all related content.

This command supports TWO MODES:

## Quick Mode (with arguments)

```
/sb-issue-view ISSUE-123
/sb-issue-view epic-456
```

## Conversational Mode (no arguments)

If no issue ID specified, ask:
1. Which issue would you like to view? (show list of recent issues to choose from, or ask for ID)

## What to Show

Gather and present a comprehensive issue/epic overview:

### 1. Issue/Epic Details
Use `get_issue(issue_id)` to get:
- Title, description
- Status, priority
- Issue type (task, bug, feature, epic)
- Labels/tags
- Created/updated dates
- External reference (if any)

### 2. Dependencies & Relationships
- Parent epic (if this is a sub-issue)
- Child issues (if this is an epic)
- Blocks/blocked by relationships
- Related issues

### 3. Linked Second Brain Task (if any)
If issue has `external_ref` like "sb-task-42", query that task:
- Task status and progress
- Time tracked in Second Brain
- Work logs
- Notes

### 4. Work Progress
- Ready work calculation
- Completion percentage
- Timeline/milestones

## Output Format

### For Regular Issue

```
╔════════════════════════════════════════════════════════════╗
║ 🎯 ISSUE: BACK-123                                         ║
║ Fix OAuth login timeout                                    ║
╚════════════════════════════════════════════════════════════╝

📌 Type: bug
📊 Status: in_progress
⚡ Priority: 4 (urgent)
🏷️  Labels: authentication, oauth, production
📅 Created: 2025-01-14
📅 Updated: 2025-01-17

📝 Description:
Users experiencing timeout errors when logging in via OAuth.
Affects ~5% of login attempts. Error occurs after 5 minutes
of inactivity.

─────────────────────────────────────────────────────────────

🏛️  EPIC MEMBERSHIP

Part of Epic: API Stability Improvements (epic-042)
Status: In Progress (3/8 issues complete)

[View epic: /sb-issue-view epic-042]

─────────────────────────────────────────────────────────────

🔗 DEPENDENCIES

Blocks:
  • BACK-145: Implement rate limiting
    Status: blocked (waiting on this)

Blocked by:
  None

Depends on:
  • BACK-100: Session management refactor
    Status: done ✅

─────────────────────────────────────────────────────────────

📋 LINKED SECOND BRAIN TASK

Task #55: "Fix authentication bug"
  Project: backend-api
  Status: in_progress
  Priority: urgent
  Time tracked: 2h 45m

Recent work logs:
  • 2025-01-17: Investigating login timeout issue (45m)
  • 2025-01-15: Fixed session timeout configuration (120m)

Notes (1):
  📄 "Login Timeout Root Cause"
     "Session timeout too short at 5 minutes. Changed to 30min."

[View full task: /sb-task-view 55]

─────────────────────────────────────────────────────────────

📈 PROGRESS

Status: In Progress
Estimated completion: 80%

Timeline:
  ✅ 2025-01-14: Issue created
  ✅ 2025-01-15: Root cause identified
  ✅ 2025-01-15: Fix implemented
  🚧 2025-01-17: Testing in staging
  ⏳ Pending: Production deployment

─────────────────────────────────────────────────────────────

✅ NEXT STEPS

1. Complete staging tests
2. Schedule production deployment
3. Monitor error rates post-deploy
4. Update documentation
5. Close issue

─────────────────────────────────────────────────────────────
```

### For Epic

```
╔════════════════════════════════════════════════════════════╗
║ 🎪 EPIC: API-042                                           ║
║ API Performance Improvements                               ║
╚════════════════════════════════════════════════════════════╝

📊 Status: in_progress
⚡ Priority: 3 (high)
🏷️  Labels: performance, api, infrastructure
📅 Created: 2025-01-01
📅 Target: 2025-02-28

📝 Description:
Comprehensive initiative to improve API performance and
scalability. Goals: reduce response times by 80%, support
10x traffic increase, improve cache hit rates.

─────────────────────────────────────────────────────────────

📊 EPIC PROGRESS

Status: 🟡 In Progress (3/8 issues complete, 37.5%)

Completed: 3 issues ✅
  ✓ API-043: Implement database connection pooling
  ✓ API-044: Add response compression
  ✓ API-045: Optimize slow queries

In Progress: 2 issues 🚧
  • API-046: Redis caching implementation
  • API-047: Add API rate limiting

Ready: 1 issue 📝
  • API-048: Load balancer optimization

Blocked: 1 issue 🚫
  • API-049: CDN integration (waiting on infra)

Not Started: 1 issue ⏳
  • API-050: Performance monitoring dashboard

─────────────────────────────────────────────────────────────

🔗 CHILD ISSUES

API-046: "Redis caching implementation" (in_progress)
  Priority: 4 (urgent)
  Linked to: Second Brain Task #42
  Time tracked: 4h 30m
  Dependencies: None
  [View: /sb-issue-view API-046]

API-047: "Add API rate limiting" (in_progress)
  Priority: 3 (high)
  Linked to: Second Brain Task #67
  Time tracked: 3h 00m
  Blocks: 1 issue
  [View: /sb-issue-view API-047]

API-048: "Load balancer optimization" (ready)
  Priority: 2 (medium)
  No Second Brain task yet
  Dependencies: None
  [View: /sb-issue-view API-048]

API-049: "CDN integration" (blocked)
  Priority: 3 (high)
  Blocked by: INFRA-123 (Infrastructure setup)
  [View: /sb-issue-view API-049]

API-050: "Performance monitoring" (open)
  Priority: 2 (medium)
  Not started yet
  [View: /sb-issue-view API-050]

─────────────────────────────────────────────────────────────

⏱️  TIME TRACKING (via Second Brain)

Total time tracked: 12h 15m

By issue:
  • API-046 (Redis caching):      4h 30m
  • API-047 (Rate limiting):      3h 00m
  • API-043 (Connection pool):    2h 45m
  • API-044 (Compression):        1h 30m
  • API-045 (Query optimization): 30m

─────────────────────────────────────────────────────────────

🎯 EPIC GOALS & METRICS

Performance Targets:
  ✅ Avg response time: 50ms → 10ms (achieved: 5ms)
  🚧 P95 response time: 120ms → 25ms (current: 30ms)
  🚧 Cache hit rate: 20% → 80% (current: 65%)
  ⏳ Traffic capacity: 1k rps → 10k rps (not tested yet)

Success Criteria:
  ✅ Database connection pooling
  ✅ Response compression enabled
  ✅ Slow queries optimized
  🚧 Redis caching deployed
  🚧 Rate limiting active
  ⏳ Load balancer optimized
  ⏳ CDN integrated
  ⏳ Monitoring dashboard live

─────────────────────────────────────────────────────────────

📝 EPIC NOTES (via Second Brain)

Project notes for related tasks:

📄 "API Performance Architecture"
   From: Task #42 (API-046)
   Tags: architecture, performance
   "Overall strategy for performance improvements..."

📄 "Performance Benchmarks"
   From: Task #42 (API-046)
   Tags: testing, metrics
   "Baseline and target performance metrics..."

📄 "Rate Limiting Strategy"
   From: Task #67 (API-047)
   Tags: architecture, security
   "Token bucket algorithm with Redis backend..."

─────────────────────────────────────────────────────────────

🚧 BLOCKERS & RISKS

Active Blockers:
  • API-049 blocked by infrastructure team
    Impact: Prevents CDN integration
    Action: Following up with infra team

Risks:
  • Cache invalidation complexity
    Mitigation: Thorough testing in staging
  • Rate limiting false positives
    Mitigation: Configurable thresholds

─────────────────────────────────────────────────────────────

✅ NEXT MILESTONES

Week 3 (Jan 22):
  • Complete Redis caching (API-046)
  • Complete rate limiting (API-047)
  • Test performance improvements

Week 4 (Jan 29):
  • Resolve infrastructure blocker
  • Start CDN integration (API-049)
  • Deploy load balancer optimization (API-048)

Week 5 (Feb 05):
  • Complete CDN integration
  • Set up monitoring dashboard (API-050)
  • Final performance testing

Week 6 (Feb 12):
  • Production rollout
  • Validate metrics
  • Close epic

─────────────────────────────────────────────────────────────

📊 STATISTICS

Issues:
  • Total: 8
  • Completed: 3 (37.5%)
  • In Progress: 2 (25%)
  • Ready: 1 (12.5%)
  • Blocked: 1 (12.5%)
  • Open: 1 (12.5%)

Velocity:
  • Avg completion time: ~5 days per issue
  • Remaining work: ~4 weeks estimated

Health: 🟡 On Track (minor blockers)

─────────────────────────────────────────────────────────────
```

## Follow-up Actions

After showing the issue/epic view, offer to:
- View child issues (for epics)
- View parent epic (for issues)
- View linked Second Brain task
- Update issue status
- Add/remove dependencies
- Create related tasks
- Generate epic summary report
- Close issue/epic

## MCP Tools Used

```python
# Get issue/epic details
get_issue(issue_id)

# For epics, get child issues
list_issues()  # filter by parent_epic_id

# Get dependencies
# (included in get_issue response)

# Get linked Second Brain task
if issue.external_ref:
    task_id = extract_from_ref(issue.external_ref)
    get_tasks()  # filter by task_id
    get_notes(task_id=task_id)
    get_work_logs()  # filter by task_id

# Get epic stats
if is_epic:
    get_epic_stats()
```

## CLI Commands

If using CLI instead of MCP:

```bash
# Issue details
sb issue show BACK-123

# List child issues of epic
sb issue list --epic epic-042

# Get stats
sb issue stats

# Get linked task
# (manual - parse external_ref)
sb task list | grep "BACK-123"
```

## Usage Examples

### View active issue
```
User: /sb-issue-view BACK-123

Agent: [Shows comprehensive issue view with task, progress, dependencies]
```

### View epic progress
```
User: /sb-issue-view epic-042

Agent: [Shows epic with all child issues, progress, timeline]
```

### From task to issue
```
User: /sb-task-view 42

Agent: [Shows task with linked issue ID]

User: "Show me the full issue"

Agent: [Uses /sb-issue-view for linked issue]
```

### Epic planning
```
User: /sb-issue-view epic-042

Agent: [Shows epic is 37.5% complete, 1 blocked issue]

User: "What's blocking API-049?"

Agent: "Waiting on INFRA-123. Would you like to view that issue or update the blocker?"
```

## Pro Tips

- Use for:
  - Sprint planning (view epic progress)
  - Dependency management (see what's blocked)
  - Status updates (comprehensive view)
  - Handoffs (all context in one place)

- Combine with task view:
  - Issue view shows high-level deps
  - Task view shows detailed work logs and notes
  - Together give complete picture
