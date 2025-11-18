Guide the user through developing a complex feature with full task-issue-note integration.

Perfect for larger features requiring planning, implementation, and documentation!

## Phase 1: Planning

```bash
# Create an epic for the feature
sb epic create "User Authentication System" \
  --description "Implement OAuth2 + JWT authentication" \
  --priority 4 \
  --labels feature,auth,security

# Create a planning note
sb note create "Auth System Design" \
  --tags architecture,planning,auth \
  --content "## Requirements

- OAuth2 authorization code flow
- JWT tokens (access + refresh)
- Multi-provider support (Google, GitHub)
- Session management

## Tech Stack

- authlib for OAuth2
- python-jose for JWT
- Redis for refresh tokens

## Architecture

\`\`\`
User -> Frontend -> Backend API -> OAuth Provider
                   ↓
                   Redis (sessions)
                   ↓
                   PostgreSQL (users)
\`\`\`"
```

## Phase 2: Break Down Work

```bash
# Create issues for each component with dependencies

# Backend work
sb issue create "OAuth2 Backend Integration" \
  --epic EPIC_ID \
  --type feature \
  --priority 4 \
  --with-task \
  --project backend \
  --description "Implement OAuth2 providers and callback handling"

# Frontend depends on backend
sb issue create "Login UI Components" \
  --epic EPIC_ID \
  --blocks BACKEND_ISSUE \
  --type feature \
  --priority 3 \
  --with-task \
  --project frontend

# Testing depends on both
sb issue create "Auth E2E Tests" \
  --epic EPIC_ID \
  --blocks BACKEND_ISSUE,FRONTEND_ISSUE \
  --type task \
  --priority 3 \
  --with-task \
  --project qa
```

## Phase 3: Implementation (Backend Example)

```bash
# Check what's ready to work on
sb issue ready --limit 10

# Start work on backend issue
sb task update BACKEND_TASK_ID --status in_progress

# Create detailed implementation note
sb note create "OAuth2 Implementation Details" \
  --task-id BACKEND_TASK_ID \
  --tags implementation,oauth,backend \
  --content "## Provider Configuration

### Google OAuth2
- Client ID: ENV var GOOGLE_CLIENT_ID
- Redirect URI: /auth/google/callback
- Scopes: openid, email, profile

### GitHub OAuth2
- Client ID: ENV var GITHUB_CLIENT_ID
- Redirect URI: /auth/github/callback
- Scopes: read:user, user:email

## Implementation Steps

- [x] Create OAuth provider configs
- [x] Implement authorization URL generation
- [ ] Implement callback handler
- [ ] Implement token exchange
- [ ] Store user data
- [ ] Generate JWT tokens"

# Log work as you go
sb log add "Set up OAuth provider configurations" \
  --task-id BACKEND_TASK_ID \
  --time 45

sb log add "Implemented Google OAuth callback" \
  --task-id BACKEND_TASK_ID \
  --time 90

# Update implementation notes
sb note add IMPL_NOTE_ID "## Token Exchange

Implemented token exchange with error handling:
- Validates state parameter
- Exchanges code for tokens
- Fetches user profile
- Creates or updates user in DB

Error cases handled:
- Invalid state (CSRF)
- Failed token exchange
- Invalid tokens
- Missing user data"
```

## Phase 4: Documentation

```bash
# Create API documentation note
sb note create "Auth API Documentation" \
  --task-id BACKEND_TASK_ID \
  --tags documentation,api,auth \
  --content "## Endpoints

### GET /auth/{provider}/login
Initiates OAuth flow

**Parameters:**
- provider: 'google' or 'github'

**Response:**
\`\`\`json
{
  \"authorization_url\": \"https://...\"
}
\`\`\`

### GET /auth/{provider}/callback
OAuth callback endpoint

**Parameters:**
- code: Authorization code
- state: CSRF token

**Response:**
\`\`\`json
{
  \"access_token\": \"eyJ...\",
  \"refresh_token\": \"eyJ...\",
  \"user\": {...}
}
\`\`\`

## Token Format

Access tokens expire in 1 hour.
Refresh tokens expire in 30 days."

# Create deployment notes
sb note create "Auth Deployment Checklist" \
  --task-id BACKEND_TASK_ID \
  --tags deployment,checklist \
  --content "## Environment Variables

- [ ] GOOGLE_CLIENT_ID
- [ ] GOOGLE_CLIENT_SECRET
- [ ] GITHUB_CLIENT_ID
- [ ] GITHUB_CLIENT_SECRET
- [ ] JWT_SECRET_KEY
- [ ] REDIS_URL

## Database Migrations

- [ ] Run auth migration
- [ ] Verify users table

## Testing

- [ ] Test OAuth flow in staging
- [ ] Verify token generation
- [ ] Test token refresh"
```

## Phase 5: Testing & Review

```bash
# Mark implementation done
sb task update BACKEND_TASK_ID --status done

# Close the issue
sb issue close BACKEND_ISSUE_ID --reason "Implementation complete, tests passing"

# Create summary
sb note create "Auth Backend - Implementation Summary" \
  --task-id BACKEND_TASK_ID \
  --tags summary,completed \
  --content "## What Was Built

OAuth2 integration supporting Google and GitHub.

## Time Spent

Total: 12 hours
- Setup & research: 2h
- Google OAuth: 4h
- GitHub OAuth: 3h
- Testing: 2h
- Documentation: 1h

## Challenges

1. State parameter validation
   - Solution: Use secure random strings, store in Redis

2. Token refresh logic
   - Solution: Background job to refresh expiring tokens

## Links

- Implementation: /backend/auth/oauth.py
- Tests: /tests/test_oauth.py
- Docs: See 'Auth API Documentation' note"
```

## Phase 6: Handoff

```bash
# Create handoff note for frontend team
sb note create "Auth API - Frontend Integration Guide" \
  --tags handoff,frontend,api \
  --content "## Quick Start

The OAuth endpoints are ready! Here's how to integrate:

### 1. Initiate Login

\`\`\`javascript
// Redirect user to get authorization URL
const response = await fetch('/auth/google/login');
const { authorization_url } = await response.json();
window.location.href = authorization_url;
\`\`\`

### 2. Handle Callback

The OAuth provider redirects to your callback route with code & state.
Send these to our backend:

\`\`\`javascript
// In your callback component
const code = params.get('code');
const state = params.get('state');

const response = await fetch(
  \`/auth/google/callback?code=\${code}&state=\${state}\`
);
const { access_token, user } = await response.json();

// Store token, redirect to app
localStorage.setItem('token', access_token);
\`\`\`

## Testing

Staging endpoints:
- https://staging-api.example.com/auth/...

Test users:
- See auth-test-users note

## Questions?

Ping @backend-team or check the 'Auth API Documentation' note!"
```

## Reviewing the Epic

```bash
# Check epic status
sb issue show EPIC_ID

# See all related issues
sb issue list --epic EPIC_ID

# Review all tasks
sb task list --project backend | grep -i auth
sb task list --project frontend | grep -i auth

# See all related notes
sb note search "auth"
sb note list --tags auth

# Generate epic summary
sb note create "Auth System - Epic Summary" \
  --tags epic,summary,completed \
  --content "## Epic: User Authentication System

**Status:** Completed ✅

**Components Delivered:**
- OAuth2 backend (Google + GitHub)
- Login UI components
- E2E tests
- API documentation

**Total Time:** 24 hours
- Backend: 12h
- Frontend: 8h
- Testing: 4h

**Key Decisions:**
- Using JWT for tokens
- Redis for session management
- 1-hour access token expiry

**Documentation:**
- API docs: see 'Auth API Documentation'
- Deployment: see 'Auth Deployment Checklist'
- Frontend guide: see 'Auth API - Frontend Integration Guide'

**Metrics:**
- Issues: 3 created, 3 closed
- Tasks: 3 completed
- Notes: 6 created

Excellent work team! 🎉"
```

**Guide them through this flow:**

1. **Start with Epic** - Big picture planning
2. **Break into Issues** - Define dependencies
3. **Create Tasks** - Link to issues with `--with-task`
4. **Add Notes Early** - Capture decisions as you make them
5. **Update Notes** - Append new findings
6. **Track Time** - Use `--time` on every log entry
7. **Document API/Usage** - Create notes for other teams
8. **Create Summaries** - After completion, summarize learnings

**Tags to use:**
- `architecture` - Design decisions
- `implementation` - Code implementation notes
- `documentation` - API/usage docs
- `deployment` - Deployment guides
- `handoff` - Information for other teams
- `summary` - Post-completion summaries
- `decision` - Key decisions made

**Pro Tips:**
- Create notes before coding (planning)
- Update notes during coding (discoveries)
- Finalize notes after coding (documentation)
- One note per major topic
- Link everything (epic -> issues -> tasks -> notes)
