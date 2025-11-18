Guide the user through a complete daily development workflow using Second Brain.

Perfect for starting and ending each workday!

## Morning: Plan Your Day

```bash
# 1. Check what's ready to work on (from Beads)
sb issue ready --limit 5

# 2. Check your in-progress tasks
sb task list --status in_progress

# 3. Check high-priority todos
sb task list --priority high --status todo

# 4. Review yesterday's work
sb log show --days 1
```

**Help them decide what to work on:**
- Look at issue dependencies - what's unblocked?
- Consider task priority
- Review time spent to estimate capacity
- Check project deadlines

**Start a task:**
```bash
# Option 1: Start from a Beads issue (complex work)
sb issue create "Implement caching layer" \
  --type feature \
  --priority 3 \
  --with-task \
  --project backend

# Option 2: Create a simple task (independent work)
sb task add "Fix validation bug" \
  --project auth \
  --priority high

# Update status to in_progress
sb task update TASK_ID --status in_progress
```

## During the Day: Track Work

```bash
# Log work with time tracking
sb log add "Implemented Redis caching for user sessions" \
  --task-id TASK_ID \
  --time 90

# Add implementation notes
sb note create "Caching Strategy" \
  --task-id TASK_ID \
  --content "## Approach

- Using Redis for session cache
- TTL set to 30 minutes
- Cache invalidation on user update"

# Update notes as you discover things
sb note add NOTE_ID "## Performance Results

Cache hit rate: 85%
Response time: 50ms (was 200ms)"
```

**When switching tasks:**
```bash
# Log what you finished
sb log add "Completed cache implementation, tests passing" \
  --task-id TASK_ID \
  --time 45

# Start new task
sb log add "Started investigating login bug" \
  --task-id NEW_TASK_ID
```

## End of Day: Wrap Up

```bash
# 1. Update task statuses
sb task update TASK_ID --status done

# Or if still in progress, add time spent
sb task update TASK_ID --time 30

# 2. Add final log entry
sb log add "Wrapped up caching feature, ready for code review tomorrow"

# 3. Create handoff notes if needed
sb note create "Tomorrow's TODO" \
  --tags tomorrow,handoff \
  --content "## Continue Work

- [ ] Add unit tests for cache invalidation
- [ ] Update API documentation
- [ ] Performance testing in staging"

# 4. Review what you accomplished
sb log show --days 1
```

## Weekly: Generate Summary

```bash
# Generate weekly report
sb report work --days 7

# Review notes from the week
sb note list --tags important

# Check project status
sb project status my-project
```

**Help them celebrate wins and plan ahead!**

Remind them:
- Log work regularly (don't wait until end of day)
- Add notes when solving tricky problems (future you will thank you)
- Update task status to keep dashboards accurate
- Use `--time` to track actual hours (helps with planning)

**Pro tips:**
1. Log work immediately when switching contexts
2. Create notes for non-obvious decisions
3. Tag notes for easy retrieval later
4. Link tasks to issues for complex features
5. Use priorities to guide daily planning
