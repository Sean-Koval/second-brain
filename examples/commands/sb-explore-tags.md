Explore and visualize content organized by tags across all Second Brain entities.

This command supports TWO MODES:

## Quick Mode (with arguments)

```
/sb-explore-tags performance
/sb-explore-tags research,ml,experiments
/sb-explore-tags --show-all
```

## Conversational Mode (no arguments)

If no tags specified, ask:
1. Would you like to:
   a) Explore a specific tag
   b) See all tags and their usage
   c) Find content with multiple tags

## What to Show

### Mode 1: Specific Tag(s)

Show all content tagged with specified tag(s):

```python
# Get all tagged content
notes = get_notes(tags=["performance"])
tasks = get_tasks(tags=["performance"])
transcripts = get_transcripts(tags=["performance"])

# Present organized view
```

### Mode 2: All Tags Overview

Show tag cloud / usage statistics:

```python
# Gather all tags from all entities
# Count usage
# Sort by frequency
# Present as tag cloud or table
```

## Output Format

### Single Tag View

```
╔════════════════════════════════════════════════════════════╗
║ 🏷️  TAG EXPLORATION: "performance"                         ║
╚════════════════════════════════════════════════════════════╝

📊 Usage: 23 items tagged with "performance"

Breakdown:
  📝 Notes:        12 items
  📋 Tasks:         8 items
  📞 Transcripts:   2 items
  📦 Projects:      1 item

─────────────────────────────────────────────────────────────

📝 NOTES (12)

Related Tags: caching (5), testing (4), optimization (8), metrics (3)

📄 "Redis Caching Strategy"
   Project: backend-api | Task: #42
   Tags: performance, caching, redis
   Created: 2025-01-15
   "We decided to use Redis cluster..."
   [View: /sb-note-show 156]

📄 "Performance Benchmarks"
   Task: #42
   Tags: performance, testing, metrics
   Created: 2025-01-17
   "Baseline: 50ms, Optimized: 5ms..."
   [View: /sb-note-show 158]

📄 "Database Query Optimization"
   Project: backend-api
   Tags: performance, database, optimization
   Created: 2025-01-10
   "Identified N+1 query problems..."
   [View: /sb-note-show 143]

... (9 more notes)

─────────────────────────────────────────────────────────────

📋 TASKS (8)

Active: 3 tasks | Completed: 5 tasks

🚧 #42: Implement Redis caching (in_progress)
   Project: backend-api
   Priority: high
   Time tracked: 4h 30m
   "Improve API response times"
   [View: /sb-task-view 42]

🚧 #67: API rate limiting (in_progress)
   Project: backend-api
   Priority: high
   Time tracked: 3h 00m
   [View: /sb-task-view 67]

✅ #35: Database connection pooling (done)
   Project: backend-api
   Time tracked: 2h 45m
   Completed: 2025-01-12
   [View: /sb-task-view 35]

... (5 more tasks)

─────────────────────────────────────────────────────────────

📞 TRANSCRIPTS (2)

📞 "API Performance Review"
   Date: 2025-01-11
   Type: meeting
   Tags: performance, planning
   "Discussed caching strategy and performance targets..."
   [View: /sb-transcript-view 45]

📞 "Q1 Engineering Planning"
   Date: 2025-01-05
   Type: planning
   Tags: performance, architecture
   "Performance improvements are Q1 priority..."
   [View: /sb-transcript-view 40]

─────────────────────────────────────────────────────────────

📦 PROJECTS (1)

📦 Backend API (backend-api)
   Status: active
   Tags: backend, api, performance, microservices
   "REST API service..."
   [View: /sb-project-view backend-api]

─────────────────────────────────────────────────────────────

🔗 RELATED TAGS

Tags commonly used with "performance":

  caching (5)        █████████░
  optimization (8)   ████████████░
  testing (4)        ███████░
  metrics (3)        █████░
  database (3)       █████░
  redis (2)          ███░
  api (6)            ██████████░

Consider exploring:
  /sb-explore-tags performance,caching
  /sb-explore-tags performance,optimization

─────────────────────────────────────────────────────────────

📈 INSIGHTS

Tag Usage Timeline:
  Last 7 days:  8 new items tagged "performance"
  Last 30 days: 15 new items tagged "performance"

Most Active:
  • Spike in Jan 10-17 (performance sprint)
  • Concentrated in backend-api project
  • Associated with tasks #42, #67, #35

Key Topics:
  • Redis caching implementation
  • Database optimization
  • API response time improvements

─────────────────────────────────────────────────────────────
```

### Multiple Tags View (Intersection)

```
╔════════════════════════════════════════════════════════════╗
║ 🏷️  TAGS: "research" + "ml" + "experiments"                ║
╚════════════════════════════════════════════════════════════╝

📊 Found: 8 items with ALL of these tags

─────────────────────────────────────────────────────────────

📝 NOTES (6)

📄 "BERT Fine-tuning Experiments"
   Tags: research, ml, experiments, nlp
   Created: 2025-01-12
   "Trying different learning rates..."
   [View: /sb-note-show 201]

📄 "Model Comparison - RoBERTa vs ALBERT"
   Tags: research, ml, experiments, comparison
   Created: 2025-01-14
   "## Results Table..."
   [View: /sb-note-show 203]

... (4 more notes)

─────────────────────────────────────────────────────────────

📋 TASKS (2)

🚧 #89: Literature review on transformers (in_progress)
   Tags: research, ml, experiments, nlp
   Time tracked: 6h 00m
   [View: /sb-task-view 89]

✅ #87: Baseline model training (done)
   Tags: research, ml, experiments
   Time tracked: 8h 30m
   Completed: 2025-01-13
   [View: /sb-task-view 87]

─────────────────────────────────────────────────────────────
```

### All Tags Overview

```
╔════════════════════════════════════════════════════════════╗
║ 🏷️  ALL TAGS OVERVIEW                                      ║
╚════════════════════════════════════════════════════════════╝

Total unique tags: 47
Total items tagged: 156

─────────────────────────────────────────────────────────────

📊 TOP TAGS (by usage)

 1. performance      (23) ████████████████████████
 2. backend          (18) ███████████████████
 3. research         (15) ████████████████
 4. api              (14) ███████████████
 5. documentation    (12) █████████████
 6. architecture     (11) ████████████
 7. ml               (10) ███████████
 8. optimization     (10) ███████████
 9. testing          (9)  ██████████
10. caching          (8)  █████████

[View all 47 tags]

─────────────────────────────────────────────────────────────

📂 TAGS BY CATEGORY

🔧 Technical:
  performance, optimization, caching, database, redis,
  api, backend, frontend, microservices

🔬 Research:
  research, ml, experiments, nlp, deep-learning,
  transformers, training

📚 Documentation:
  documentation, docs, runbook, guide, howto,
  architecture, design

🏗️ Project Management:
  planning, meeting, decision, postmortem, review

🐛 Bug Tracking:
  bug, hotfix, production, incident, debugging

─────────────────────────────────────────────────────────────

🔍 TAG SEARCH

Explore specific tags:
  /sb-explore-tags performance
  /sb-explore-tags research,ml

Search by pattern:
  /sb-explore-tags --pattern "perf*"
  /sb-explore-tags --pattern "*optimization"

Find unused tags:
  /sb-explore-tags --unused

─────────────────────────────────────────────────────────────

💡 TAG SUGGESTIONS

Commonly misspelled/similar:
  • perfomance → performance
  • optimisation → optimization
  • chaching → caching

Consider consolidating:
  • ml, machine-learning, machinelearning
  • docs, documentation
  • backend, back-end

Suggested new tags based on content:
  • scalability (appears in 8 notes, not tagged)
  • monitoring (appears in 6 notes, not tagged)

─────────────────────────────────────────────────────────────
```

## Follow-up Actions

After showing tag exploration, offer to:
- Drill down into specific item
- Search for related tags
- Create new content with these tags
- Rename/consolidate tags
- Generate tag-based report
- Export tagged content

## MCP Tools Used

```python
# For specific tag(s)
notes = get_notes(tags=["performance"])
tasks = get_tasks(tags=["performance"])
transcripts = get_transcripts(tags=["performance"])

# For all tags overview
# Query all entities and extract tags
# Count and aggregate
```

## CLI Commands

If using CLI instead of MCP:

```bash
# List with tags filter
sb note list --tags performance
sb task list --tags performance,optimization
sb transcript list --tags research,ml

# No direct "show all tags" command
# Would need to parse output or query DB
```

## Usage Examples

### Explore single tag
```
User: /sb-explore-tags performance

Agent: [Shows all performance-tagged content organized by type]
```

### Explore multiple tags (AND)
```
User: /sb-explore-tags research,ml,experiments

Agent: [Shows only items with ALL three tags]
```

### See all tags
```
User: /sb-explore-tags --show-all

Agent: [Shows tag cloud and statistics]
```

### Conversational
```
User: /sb-explore-tags

Agent: "What would you like to do?"
       1. Explore a specific tag
       2. See all tags
       3. Find content with multiple tags

User: "1"

Agent: "Which tag?"
       Top tags: performance, research, backend, api...

User: "research"

Agent: [Shows all research-tagged content]
```

### Discovery workflow
```
User: /sb-explore-tags --show-all

Agent: [Shows top tags include "performance" (23 items)]

User: "Show me performance"

Agent: [Uses /sb-explore-tags performance]
       [Shows 12 notes, 8 tasks, 2 transcripts]

User: "Show me the Redis caching note"

Agent: [Uses /sb-note-show 156]
```

## Pro Tips

### 1. Tag Naming Conventions

Establish consistent conventions:

```
# Use lowercase
performance ✅
Performance ❌

# Use hyphens for multi-word
deep-learning ✅
deep_learning ❌
deeplearning ❌

# Be specific
ml-experiments ✅
experiments ❌ (too generic)

# Group with prefixes
proj-backend ✅
proj-frontend ✅
```

### 2. Tag Hierarchies

Use prefixes to create hierarchies:

```
# Project tags
proj-backend
proj-frontend
proj-mobile

# Technology tags
tech-python
tech-javascript
tech-rust

# Status tags
status-draft
status-review
status-final
```

### 3. Cross-cutting Tags

Use tags to find themes across projects:

```
# Find all architecture decisions
/sb-explore-tags architecture,decision

# Find all production issues
/sb-explore-tags production,incident

# Find all research findings
/sb-explore-tags research,findings
```

### 4. Tag-based Reviews

Use for periodic reviews:

```
# Weekly: Review important items
/sb-explore-tags important,review

# Monthly: Review decisions
/sb-explore-tags decision

# Quarterly: Review architecture
/sb-explore-tags architecture
```

### 5. Clean Up Tags

Periodically review and consolidate:

```
# Find similar tags
/sb-explore-tags --show-all

# Consolidate
# ml, machine-learning → ml
# docs, documentation → documentation
```

## Common Tag Patterns

```
# Research workflow
research, literature-review, paper-notes
research, experiments, results
research, ml, training
research, findings, decision

# Feature development
feature, design, architecture
feature, implementation, progress
feature, testing, qa
feature, deployed, production

# Bug tracking
bug, investigation, root-cause
bug, fix, solution
bug, testing, verified
bug, postmortem, learning

# Meeting notes
meeting, standup, notes
meeting, planning, decisions
meeting, review, feedback
meeting, action-items, todos
```

---

Use tag exploration to:
- Discover related content
- Find themes across projects
- Review work by topic
- Generate topic-based reports
- Improve your tagging strategy
