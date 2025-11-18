# Second Brain Workflows

Step-by-step workflows for common Second Brain usage patterns.

## Contents

- [Daily Development Workflow](#daily-development-workflow)
- [Starting a New Feature](#starting-a-new-feature)
- [Bug Investigation and Fix](#bug-investigation-and-fix)
- [Weekly Review](#weekly-review)
- [Performance Review Preparation](#performance-review-preparation)
- [Research and Learning](#research-and-learning)
- [Team Collaboration](#team-collaboration)

---

## Daily Development Workflow

**Use this for:** Regular development work with task and time tracking.

### Morning Routine

**1. Check active work:**
```bash
sb task list --status in_progress
```

**Expected output:**
```
📋 Tasks (in_progress):
  #42 Implement rate limiting (backend-api) [high]
  #45 Write integration tests (backend-api) [medium]
```

**2. Review yesterday's work:**
```bash
sb log show --days 1
```

**3. Find ready work (if using Beads):**
```bash
sb issue ready --priority 3,4
```

### During Work

**1. Log work as you go:**
```bash
# After implementing a feature
sb log add "Implemented rate limiting middleware with Redis backend" \
  --task-id 42 \
  --time 120

# After code review
sb log add "Reviewed PR #234 - auth refactoring" --time 30

# After meetings
sb log add "Sprint planning meeting" --time 60
```

**2. Update task status:**
```bash
# When starting work
sb task update 42 --status in_progress

# When switching tasks
sb task update 42 --status in_progress
sb log add "Context switch to tests" --time 15
sb task update 45 --status in_progress
```

**3. Create notes for important context:**
```bash
sb note create "Rate Limiting Implementation" \
  --task-id 42 \
  --content "Using sliding window algorithm with Redis sorted sets.
100 requests/minute per IP. Configured via env var RATE_LIMIT_RPM."
```

### End of Day

**1. Final work log:**
```bash
sb log add "Deployed rate limiting to staging, monitoring for issues" \
  --task-id 42 \
  --time 45
```

**2. Mark tasks complete:**
```bash
sb task update 42 --status done --time 180
```

**3. Review the day:**
```bash
sb log show --days 1
```

**Expected output:**
```
📅 2025-01-17

Implemented rate limiting middleware with Redis backend [2h] #42
Reviewed PR #234 - auth refactoring [30m]
Sprint planning meeting [1h]
Deployed rate limiting to staging, monitoring for issues [45m]

Total: 4h 15m
```

---

## Starting a New Feature

**Use this for:** Complex features with multiple components and dependencies.

### Step 1: Create Epic + Project

```bash
sb issue create-with-project "Payment Integration" \
  --description "Integrate Stripe for payment processing" \
  --priority 4 \
  --labels backend,payments,critical
```

**What this creates:**
```
✓ Epic + Project created successfully!

📋 Epic (Beads):
  ID: epic-042
  Title: Payment Integration
  Priority: Highest (4)

📦 Project (Second Brain):
  ID: 15
  Name: Payment Integration
  Slug: payment-integration

🔗 Epic ID: epic-042 ↔️ Project Slug: payment-integration
```

### Step 2: Break Down into Issues and Tasks

```bash
# Create issues under epic with linked tasks
sb issue create "Stripe API integration" \
  --epic epic-042 \
  --with-task \
  --project payment-integration \
  --priority 4

sb issue create "Payment UI components" \
  --epic epic-042 \
  --with-task \
  --project payment-integration \
  --priority 3

sb issue create "Webhook handling" \
  --epic epic-042 \
  --with-task \
  --project payment-integration \
  --priority 3
```

### Step 3: Add Dependencies (if needed)

```bash
# UI depends on API being done
bd dep add payment-ui stripe-api --type blocks
```

### Step 4: Create Initial Notes

```bash
sb note create "Payment Architecture" \
  --project payment-integration \
  --content "## Design Decisions

Using Stripe Checkout for PCI compliance.
Webhooks for async payment status.
PostgreSQL for payment records (not Stripe as source of truth)."
```

### Step 5: Find and Start Ready Work

```bash
sb issue ready --priority 4
# Start with stripe-api issue since it's not blocked

sb task update <task-id> --status in_progress
```

### Step 6: Work and Log Progress

```bash
sb log add "Implemented Stripe SDK integration, created payment intent endpoint" \
  --task-id <task-id> \
  --time 180

sb note add <note-id> "## API Endpoints

POST /payments/create-intent
  - Creates Stripe PaymentIntent
  - Returns client_secret

POST /payments/confirm
  - Confirms payment
  - Updates order status"
```

---

## Bug Investigation and Fix

**Use this for:** Investigating and fixing bugs with full context capture.

### Step 1: Create Task for Bug

```bash
sb task add "Fix login timeout bug" \
  --project backend-api \
  --priority urgent \
  --description "Users getting logged out after 5 minutes instead of 1 hour"
```

### Step 2: Create Investigation Note

```bash
sb note create "Login Timeout Investigation" \
  --task-id <task-id> \
  --content "## Problem
Users report being logged out after ~5 minutes.
Expected: 1 hour session timeout.

## Investigation Steps
- [ ] Check JWT token expiry configuration
- [ ] Verify session middleware settings
- [ ] Review recent auth changes
- [ ] Test token refresh logic"
```

### Step 3: Log Investigation Work

```bash
# As you investigate
sb log add "Investigated JWT config, found token expiry set to 300s instead of 3600s" \
  --task-id <task-id> \
  --time 45
```

### Step 4: Update Note with Findings

```bash
sb note add <note-id> "## Root Cause
Environment variable JWT_EXPIRY accidentally set to 300 (5 min) instead of 3600 (1 hour).

## Fix
Updated .env file: JWT_EXPIRY=3600
Deployed to staging, verified 1hr timeout works."
```

### Step 5: Log Fix and Close

```bash
sb log add "Fixed JWT expiry config, deployed to production, monitoring" \
  --task-id <task-id> \
  --time 30

sb task update <task-id> --status done --time 75
```

---

## Weekly Review

**Use this for:** Friday wrap-ups, team status updates.

### Step 1: Generate Report

```bash
sb report work --days 7
```

**Review output:**
```
📊 Work Report (Last 7 days)

Time Worked: 38h 30m

Projects:
  backend-api: 24h (62%)
  mobile-app: 10h (26%)
  ml-pipeline: 4h 30m (12%)

Tasks Completed: 8

Top Tasks by Time:
  #42 Implement rate limiting: 6h
  #45 Integration tests: 4h 30m
  #48 Payment UI: 5h

Work Logs: 32 entries
```

### Step 2: Review Completed Tasks

```bash
sb task list --status done
```

### Step 3: Check In-Progress Work

```bash
sb task list --status in_progress
```

### Step 4: Plan Next Week

```bash
# Find ready work
sb issue ready --priority 3,4

# Create tasks for next week's priorities
sb task add "Implement Redis caching layer" \
  --project backend-api \
  --priority high
```

### Step 5: Create Summary Note

```bash
sb note create "Week of Jan 13-17 Summary" \
  --tags weekly-summary \
  --content "## Completed
- Payment integration (Stripe API + UI)
- Rate limiting implementation
- Integration test coverage

## In Progress
- Redis caching layer
- Mobile app refactor

## Blockers
None

## Next Week
- Complete caching implementation
- Start mobile app redesign"
```

---

## Performance Review Preparation

**Use this for:** Quarterly or annual performance reviews.

### Step 1: Generate Quarterly Report

```bash
sb report work --days 90 > Q1-2025-accomplishments.md
```

### Step 2: Review Major Projects

```bash
# List all projects worked on
sb project list

# Get detailed status for each
sb project status backend-api
sb project status mobile-app
sb project status ml-pipeline
```

### Step 3: Extract Completed Tasks

```bash
# All tasks completed in Q1
sb task list --status done
```

### Step 4: Review Notes for Highlights

```bash
# Search for design decisions
sb note search "design decision"
sb note search "architecture"

# Review project notes
sb note list --project backend-api
```

### Step 5: Compile Accomplishments

Create a summary document with:
- Total time worked
- Major projects completed
- Technical achievements (from notes)
- Impact metrics (from work logs)
- Skills developed (from research notes)

---

## Research and Learning

**Use this for:** Learning new technologies, research projects.

### Step 1: Create Research Project

```bash
sb project create "Learning Rust" \
  --description "Learning Rust programming language" \
  --tags learning,rust
```

### Step 2: Create Research Notes

```bash
sb note create "Rust Ownership System" \
  --project learning-rust \
  --tags research \
  --content "## Key Concepts

Ownership Rules:
1. Each value has one owner
2. Only one owner at a time
3. Value dropped when owner goes out of scope

## Benefits
- Memory safety without GC
- Thread safety guaranteed
- Zero-cost abstractions"
```

### Step 3: Log Learning Time

```bash
sb log add "Completed Rust Book chapters 4-6 (ownership, borrowing, lifetimes)" \
  --time 180

sb log add "Built CLI tool in Rust - learned about error handling with Result<T,E>" \
  --time 240
```

### Step 4: Create Learning Tasks

```bash
sb task add "Complete Rust Book Chapter 10 (Generics)" \
  --project learning-rust \
  --priority medium

sb task add "Build REST API in Rust" \
  --project learning-rust \
  --priority high
```

### Step 5: Track Progress

```bash
# Weekly review of learning
sb log show --project learning-rust --days 7

# Review all learning notes
sb note list --project learning-rust
```

---

## Team Collaboration

**Use this for:** Coordinating work with team members.

### Step 1: Create Shared Epic + Project

```bash
sb issue create-with-project "Backend Services Rewrite" \
  --priority 4 \
  --labels backend,team \
  --description "Microservices migration from monolith"
```

### Step 2: Break Down by Owner

```bash
# Your work
sb issue create "Auth service migration" \
  --epic epic-042 \
  --with-task \
  --project backend-services-rewrite \
  --priority 4

# Team member's work (track dependencies)
bd create "Database migration" \
  --epic epic-042 \
  --priority 4

# Add dependency
bd dep add auth-service database-migration --type blocks
```

### Step 3: Log Your Contributions

```bash
sb log add "Completed auth service migration, deployed to staging" \
  --task-id <task-id> \
  --time 360

sb log add "Helped Sarah debug database migration issue" \
  --time 90
```

### Step 4: Track Team Status

```bash
# Check what's ready for anyone to work on
sb issue ready

# Check blockers
bd blocked
```

### Step 5: Create Handoff Notes

```bash
sb note create "Auth Service Migration Handoff" \
  --project backend-services-rewrite \
  --content "## Status
Auth service fully migrated and deployed.

## Configuration
- OAuth2 with Okta
- JWT tokens (1hr expiry, 7d refresh)
- Rate limiting: 100 req/min per user

## Monitoring
- Grafana dashboard: /dashboards/auth-service
- Alert on >1% error rate

## Known Issues
None

## Next Steps
- Monitor for 48hrs
- Document API endpoints
- Train team on new auth flow"
```

---

## Tips for All Workflows

1. **Log work immediately** - Don't wait until end of day, you'll forget details
2. **Be specific in logs** - "Fixed bug" → "Fixed null pointer in auth middleware line 42"
3. **Link logs to tasks** - Enables automatic time tracking and context
4. **Create notes for decisions** - Future you will want to know WHY, not just WHAT
5. **Use projects to organize** - Group related tasks for better reporting
6. **Track time on everything** - Even meetings and code reviews (>15 min)
7. **Review regularly** - Daily for logs, weekly for summary, quarterly for reviews
8. **Use priorities** - Helps focus on what matters when reviewing tasks
