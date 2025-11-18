Guide the user through investigating and fixing bugs with thorough documentation.

Perfect for complex bugs requiring investigation!

## Initial Report

```bash
# Create bug issue with high priority
sb issue create "API returning 500 on user profile endpoint" \
  --type bug \
  --priority 4 \
  --with-task \
  --project backend \
  --description "Users reporting 500 errors when accessing /api/users/me endpoint"

# Start investigation
sb task update TASK_ID --status in_progress

# Create investigation note
sb note create "Profile API 500 Error - Investigation" \
  --task-id TASK_ID \
  --tags bug,investigation,api \
  --content "## Bug Report

**Endpoint:** GET /api/users/me
**Error:** HTTP 500
**Frequency:** ~5% of requests
**First seen:** $(date)

## Initial Hypothesis

Possible causes:
- Database connection issue?
- Race condition?
- Bad data in DB?

## Investigation Steps

- [ ] Check error logs
- [ ] Identify affected users
- [ ] Reproduce locally
- [ ] Check database state"

# Log start of investigation
sb log add "Started investigating profile API 500 error" \
  --task-id TASK_ID
```

## Investigation Process

```bash
# Update investigation note with findings
sb note add INVESTIGATION_NOTE_ID "## Log Analysis

Checked production logs:

\`\`\`
ERROR: NoneType object has no attribute 'email'
File: /app/routes/users.py, line 42
\`\`\`

**Finding:** Error occurs when user.profile is None

Affected users: 127
Common pattern: Users who signed up before 2024-12-01"

# Log investigation work
sb log add "Analyzed logs, found NoneType error on user.profile" \
  --task-id TASK_ID \
  --time 45

# Add more findings
sb note add INVESTIGATION_NOTE_ID "## Database Analysis

Checked database:

\`\`\`sql
SELECT COUNT(*) FROM users WHERE profile_id IS NULL;
-- Result: 127 users
\`\`\`

**Root Cause Found:**
Migration on 2024-12-01 added profile table but didn't create
profiles for existing users. New code assumes profile exists.

## Error Flow

1. User with profile_id=NULL requests /api/users/me
2. Code: user.profile.email (NPE because profile is None)
3. Unhandled exception -> 500 error"

# Log breakthrough
sb log add "Root cause identified: missing profiles for old users" \
  --task-id TASK_ID \
  --time 60
```

## Solution Planning

```bash
# Create solution note
sb note create "Profile API Fix - Solution Plan" \
  --task-id TASK_ID \
  --tags solution,fix \
  --content "## Solution Options

### Option 1: Backfill Profiles (Recommended)
Create profiles for all users missing them

**Pros:**
- Fixes root cause
- No code changes needed

**Cons:**
- Need to run migration
- Takes time for 127 users

### Option 2: Handle None Case
Add null check in code

**Pros:**
- Quick fix
- No migration needed

**Cons:**
- Doesn't fix underlying issue
- Will fail elsewhere

### Option 3: Combination
Backfill + add defensive check

**Pros:**
- Robust solution
- Prevents future issues

**Cons:**
- Most work

## Decision: Option 3

Will implement both:
1. Data migration to create missing profiles
2. Defensive null check in code

## Implementation Plan

- [ ] Write migration script
- [ ] Test migration on staging
- [ ] Add null checks to code
- [ ] Add monitoring for profile=None cases
- [ ] Deploy fix"

# Log planning work
sb log add "Created solution plan: backfill + null checks" \
  --task-id TASK_ID \
  --time 30
```

## Implementation

```bash
# Update investigation note with implementation details
sb note add INVESTIGATION_NOTE_ID "## Implementation

### 1. Migration Script

Created script to backfill profiles:

\`\`\`python
# scripts/backfill_profiles.py
from models import User, Profile

users_without_profiles = User.query.filter_by(profile_id=None).all()
for user in users_without_profiles:
    profile = Profile(email=user.email, name=user.name)
    db.session.add(profile)
    user.profile = profile

db.session.commit()
print(f\"Created {len(users_without_profiles)} profiles\")
\`\`\`

### 2. Code Fix

Added defensive check:

\`\`\`python
@app.get(\"/api/users/me\")
def get_current_user():
    user = get_current_user_from_token()

    # Defensive check
    if not user.profile:
        logger.error(f\"User {user.id} missing profile\")
        # Create profile on-the-fly
        user.profile = Profile(email=user.email, name=user.name)
        db.session.commit()

    return user.serialize()
\`\`\`

### 3. Testing

Tested on staging:
- ✅ Migration creates profiles successfully
- ✅ Code handles None case gracefully
- ✅ No 500 errors after fix"

# Log implementation
sb log add "Implemented backfill script and null checks" \
  --task-id TASK_ID \
  --time 120
```

## Deployment

```bash
# Create deployment note
sb note create "Profile API Fix - Deployment" \
  --task-id TASK_ID \
  --tags deployment,runbook \
  --content "## Deployment Steps

### 1. Run Migration (Staging)
\`\`\`bash
python scripts/backfill_profiles.py --env staging
# Expected: Created 127 profiles
\`\`\`

### 2. Verify Staging
\`\`\`bash
# Check no users without profiles
psql -c \"SELECT COUNT(*) FROM users WHERE profile_id IS NULL;\"
# Expected: 0

# Test API endpoint
curl https://staging.api.com/users/me
# Expected: 200 OK
\`\`\`

### 3. Deploy Code (Staging)
\`\`\`bash
git push staging fix/profile-api-500
\`\`\`

### 4. Run Migration (Production)
\`\`\`bash
python scripts/backfill_profiles.py --env production
\`\`\`

### 5. Deploy Code (Production)
\`\`\`bash
git push production fix/profile-api-500
\`\`\`

### 6. Monitor
Watch error rate for 1 hour:
- Check CloudWatch for 500 errors
- Verify profile=None logging is silent

## Rollback Plan

If issues occur:
\`\`\`bash
git revert HEAD
git push production main
\`\`\`"

# Log deployment
sb log add "Deployed fix to staging, testing before production" \
  --task-id TASK_ID \
  --time 45

sb log add "Deployed fix to production, monitoring errors" \
  --task-id TASK_ID \
  --time 30
```

## Post-Deployment

```bash
# Update investigation note with results
sb note add INVESTIGATION_NOTE_ID "## Resolution

**Status:** Fixed ✅

**Deployment date:** $(date)

**Results:**
- All 127 profiles created successfully
- 500 error rate: 5% -> 0%
- No new profile=None errors logged

## Monitoring (24h post-deploy)

- Total requests: 45,000
- 500 errors: 0
- Profile=None cases: 0

Fix confirmed successful!"

# Create postmortem
sb note create "Profile API 500 - Postmortem" \
  --task-id TASK_ID \
  --tags postmortem,learning \
  --content "## Incident Summary

**What happened:**
Migration added profile table but didn't backfill existing users,
causing 500 errors for 5% of profile requests.

**Impact:**
- Affected: 127 users
- Duration: 3 days
- Error rate: ~5% of /api/users/me requests

**Root cause:**
Incomplete migration - added schema but not data.

## Timeline

- 2024-12-01: Profile migration deployed
- 2024-12-04: Errors first reported
- 2024-12-04 10:00: Investigation started
- 2024-12-04 12:30: Root cause identified
- 2024-12-04 15:00: Fix deployed to staging
- 2024-12-04 16:00: Fix deployed to production
- 2024-12-04 17:00: Confirmed resolved

## What went well

- Quick root cause identification (2.5h)
- Thorough testing on staging
- Defensive code prevents recurrence

## What could be improved

- **Migration process:** Need better migration testing
- **Monitoring:** Should alert on NULL foreign keys
- **Code review:** Check for nullable relationship assumptions

## Action Items

- [ ] Add migration testing to CI/CD
- [ ] Add database constraint checks
- [ ] Create migration checklist
- [ ] Add monitoring for NULL relationships
- [ ] Document migration best practices

## Prevention

To prevent similar issues:
1. All migrations must include data backfill if needed
2. Add database constraints where possible
3. Code should handle NULL relationships gracefully
4. Test migrations on staging with production-like data"

# Mark task complete
sb task update TASK_ID --status done

# Close issue
sb issue close ISSUE_ID --reason "Fixed - backfilled profiles and added defensive null checks"

# Final log entry
sb log add "Bug fixed and deployed, created postmortem" \
  --task-id TASK_ID \
  --time 30
```

**Guide them through:**

1. **Document everything** - Logs, database queries, error messages
2. **Track hypotheses** - What you thought vs what you found
3. **Show investigation path** - Others can learn from your process
4. **Include code snippets** - Actual queries, errors, fixes
5. **Create postmortem** - Turn bugs into learning opportunities

**Essential Notes for Bugs:**
- Investigation note (findings as you go)
- Solution plan (options considered)
- Deployment runbook (exact steps)
- Postmortem (learnings and prevention)

**Pro Tips:**
- Start investigation note immediately
- Update with each finding (use `sb note add`)
- Include error messages and stack traces
- Document what DIDN'T work (saves others time)
- Create postmortem even for small bugs
- Tag with `bug`, `postmortem`, affected component

**Time tracking:**
- Log investigation time separately
- Track solution planning time
- Track implementation time
- Track testing/deployment time
- Shows true cost of bugs (for prioritization)
