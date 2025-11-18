View and explore meeting/call transcripts with related content.

This command supports TWO MODES:

## Quick Mode (with arguments)

```
/sb-transcript-view 45
/sb-transcript-list --tags meeting,planning
```

## Conversational Mode (no arguments)

If no transcript ID specified, ask:
1. Would you like to:
   a) View a specific transcript
   b) List recent transcripts
   c) Search transcripts by tags/date

## What to Show

### View Specific Transcript

Use `get_transcript_content(transcript_id)` to get:
- Full transcript with raw content
- Summary and action items (if processed)
- Linked projects and tasks
- Tags and metadata
- Related notes and work logs

## Output Format

```
╔════════════════════════════════════════════════════════════╗
║ 📞 TRANSCRIPT #45: API Performance Review                  ║
╚════════════════════════════════════════════════════════════╝

📅 Date: 2025-01-11 14:00
⏱️  Duration: 45 minutes
🎙️  Type: meeting
👥 Participants: 4
🏷️  Tags: performance, planning, api

─────────────────────────────────────────────────────────────

📋 SUMMARY

Discussion of Q1 performance improvement initiative for
the Backend API project. Team reviewed current metrics,
decided on caching strategy using Redis cluster, and
established performance targets.

Key Decisions:
  • Redis cluster for caching (3 nodes + replication)
  • Target: <10ms avg response time (from 50ms)
  • Timeline: 2 weeks for implementation
  • Weekly performance reviews during rollout

─────────────────────────────────────────────────────────────

✅ ACTION ITEMS

1. [ ] Research Redis cluster best practices
   Owner: @john
   Due: 2025-01-15
   Status: ✅ Done (see Task #41)

2. [ ] Set up Redis cluster in staging
   Owner: @sarah
   Due: 2025-01-17
   Status: ✅ Done (see Task #42)

3. [ ] Create performance benchmark suite
   Owner: @mike
   Due: 2025-01-14
   Status: ✅ Done (see Note #158)

4. [ ] Update architecture documentation
   Owner: @john
   Due: 2025-01-20
   Status: 🚧 In Progress (see Task #70)

─────────────────────────────────────────────────────────────

🔗 LINKED CONTENT

Projects:
  📦 backend-api
     [View: /sb-project-view backend-api]

Tasks Created/Discussed:
  📋 #42: Implement Redis caching (in_progress)
     Created from action item #2
     Time tracked: 4h 30m
     [View: /sb-task-view 42]

  📋 #70: Update architecture docs (in_progress)
     Created from action item #4
     Time tracked: 1h 15m
     [View: /sb-task-view 70]

Related Notes:
  📄 Note #156: "Redis Caching Strategy"
     Created after this meeting
     Captures decisions from discussion
     [View: /sb-note-show 156]

  📄 Note #158: "Performance Benchmarks"
     Benchmark results referenced
     [View: /sb-note-show 158]

─────────────────────────────────────────────────────────────

📝 RAW TRANSCRIPT

[00:00] john: Thanks everyone for joining. Let's talk about
        the performance improvements we need for Q1.

[00:45] sarah: I've been looking at our current metrics.
        Average response time is around 50ms, but P95 is
        hitting 120ms. We need to do better.

[01:20] mike: I ran some profiling. The bottleneck is
        definitely database queries. We're making too many
        round trips.

[02:15] john: Have we considered caching?

[02:30] sarah: Yes! I think Redis would work well here.
        We could use a cluster for high availability.

[03:00] john: That makes sense. What about the architecture?

[03:20] sarah: I'm thinking 3 master nodes with 2 replicas
        each. Use Sentinel for automatic failover.

[04:45] mike: What's our performance target?

[05:10] john: I'd like to see average response time under
        10ms. That's an 80% improvement.

[05:45] sarah: That's aggressive but doable with caching.

[...transcript continues...]

[42:30] john: Okay, let's summarize the action items...

[Full transcript: 1,450 words]

[Show full transcript]

─────────────────────────────────────────────────────────────

📊 FOLLOW-UP TRACKING

Action Items Status:
  ✅ Complete: 3/4 (75%)
  🚧 In Progress: 1/4 (25%)

Tasks Created: 2
  • 1 in progress
  • 1 in progress

Notes Created: 2
  • Caching strategy documented
  • Benchmarks recorded

Impact:
  • Led to Task #42 (4.5h work tracked)
  • Performance goal achieved (5ms avg)
  • 2 comprehensive notes created

Meeting ROI: ✅ High Impact

─────────────────────────────────────────────────────────────
```

## List Transcripts View

```
╔════════════════════════════════════════════════════════════╗
║ 📞 RECENT TRANSCRIPTS                                      ║
╚════════════════════════════════════════════════════════════╝

Showing last 30 days | Total: 8 transcripts

─────────────────────────────────────────────────────────────

📞 #50: "Sprint Planning - Week 3"
   Date: 2025-01-17 | Type: planning | Duration: 60min
   Tags: planning, sprint, team
   Action items: 5 (3 done, 2 in progress)
   Linked: 3 tasks created
   [View: /sb-transcript-view 50]

📞 #48: "Backend API Architecture Review"
   Date: 2025-01-15 | Type: review | Duration: 90min
   Tags: architecture, review, backend
   Action items: 7 (5 done, 1 in progress, 1 todo)
   Linked: 4 tasks, 2 notes
   [View: /sb-transcript-view 48]

📞 #45: "API Performance Review"
   Date: 2025-01-11 | Type: meeting | Duration: 45min
   Tags: performance, planning, api
   Action items: 4 (3 done, 1 in progress)
   Linked: 2 tasks, 2 notes
   [View: /sb-transcript-view 45]

📞 #42: "Client Feedback Session"
   Date: 2025-01-09 | Type: client | Duration: 30min
   Tags: client, feedback, feature-requests
   Action items: 8 (2 done, 3 in progress, 3 todo)
   Linked: 1 epic, 3 issues created
   [View: /sb-transcript-view 42]

... (4 more transcripts)

─────────────────────────────────────────────────────────────

📊 TRANSCRIPT STATS

Total transcripts: 8 (last 30 days)
Total meeting time: 7h 15m
Avg duration: 54 minutes

By Type:
  • Meetings: 4
  • Planning: 2
  • Reviews: 1
  • Client calls: 1

Action Items:
  • Total: 37 action items
  • Complete: 18 (49%)
  • In Progress: 12 (32%)
  • Todo: 7 (19%)

Content Created:
  • Tasks: 12 tasks
  • Notes: 8 notes
  • Issues: 4 issues

Most Productive:
  #42: Client Feedback → 1 epic, 3 issues
  #48: Architecture Review → 4 tasks, 2 notes

─────────────────────────────────────────────────────────────

🏷️  COMMON TAGS

planning (4)        ████████
meeting (3)         ██████
architecture (3)    ██████
review (2)          ████
performance (2)     ████
client (1)          ██

[Explore by tag: /sb-explore-tags meeting]

─────────────────────────────────────────────────────────────
```

## Follow-up Actions

After showing transcript view, offer to:
- Create tasks from action items
- Create notes from key decisions
- Link to related projects/tasks
- Update action item status
- Search for related transcripts
- Generate meeting summary
- Export transcript

## MCP Tools Used

```python
# View specific transcript
get_transcript_content(transcript_id)

# List transcripts
get_transcripts(
    transcript_type="meeting",
    tags=["planning"],
    start_date="2025-01-01",
    end_date="2025-01-31"
)

# Get related tasks (search by mention)
get_tasks()  # filter by tasks created around same time

# Get related notes
get_notes()  # search for notes referencing transcript
```

## CLI Commands

If using CLI instead of MCP:

```bash
# View transcript
sb transcript show 45

# List transcripts
sb transcript list
sb transcript list --type meeting
sb transcript list --tags planning,review

# List by date
sb transcript list --start-date 2025-01-01 --end-date 2025-01-31
```

## Usage Examples

### View specific transcript
```
User: /sb-transcript-view 45

Agent: [Shows full transcript with summary, action items, linked content]
```

### List recent transcripts
```
User: /sb-transcript-list

Agent: [Shows last 30 days of transcripts with stats]
```

### Filter by tags
```
User: /sb-transcript-list --tags planning,sprint

Agent: [Shows only planning/sprint-related transcripts]
```

### Create tasks from transcript
```
User: /sb-transcript-view 45

Agent: [Shows 4 action items, 1 still todo]

User: "Create a task for action item #4"

Agent: [Uses create_task with details from action item]
       "✓ Created Task #71: Update architecture docs"
```

### Find related transcripts
```
User: /sb-task-view 42

Agent: [Shows task is related to Transcript #45]

User: "Show me that transcript"

Agent: [Uses /sb-transcript-view 45]
```

### Track action items
```
User: /sb-transcript-view 48

Agent: [Shows 7 action items: 5 done, 1 in progress, 1 todo]

User: "What's still todo?"

Agent: "Action item #6: 'Review security implications'"
       "Would you like to create a task for this?"
```

## Pro Tips

### 1. Process Transcripts Immediately

After a meeting:
```
1. Upload transcript
2. Add summary and action items
3. Create tasks for action items
4. Tag appropriately
5. Link to relevant projects
```

### 2. Use Transcripts for Context

When working on a task:
```
/sb-task-view 42
[Shows linked to Transcript #45]

/sb-transcript-view 45
[See full context of why task was created]
```

### 3. Track Meeting ROI

Review transcripts to see:
- Which meetings led to actual work
- Action item completion rate
- Time from meeting to task completion

### 4. Create Decision Records

Extract key decisions to notes:
```
Meeting → Transcript → Extract decision → Create note

Tags: decision, architecture, from-transcript-45
```

### 5. Search Across Transcripts

Find when topics were discussed:
```
# When did we discuss caching?
/sb-search-all "caching" --type transcript

# Find all architecture discussions
/sb-transcript-list --tags architecture
```

## Common Patterns

### Pattern 1: Meeting → Tasks
```
1. Record meeting (create transcript)
2. Add summary and action items
3. Create task for each action item
4. Link transcript to tasks
5. Track completion
```

### Pattern 2: Meeting → Decisions
```
1. Record meeting
2. Extract key decisions
3. Create decision note
4. Link to transcript
5. Tag for discoverability
```

### Pattern 3: Client Feedback → Epic
```
1. Record client call
2. Capture feature requests
3. Create epic for initiative
4. Create issues for features
5. Link back to transcript
```

### Pattern 4: Review → Improvements
```
1. Record review meeting
2. Identify improvement areas
3. Create tasks for improvements
4. Track over time
5. Reference in retrospectives
```

---

Use transcript view to:
- Capture meeting decisions
- Track action items
- Link meetings to work
- Maintain context
- Search past discussions
- Calculate meeting ROI
