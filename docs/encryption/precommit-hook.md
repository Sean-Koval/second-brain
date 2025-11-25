# Pre-commit Hook Guide

The Second Brain pre-commit hook is an automated validation system that prevents you from accidentally committing unencrypted sensitive data to your git repository.

## Overview

The hook runs automatically before every `git commit` in your `~/.second-brain/` directory and:

1. **Scans staged files** for sensitive data patterns
2. **Validates frontmatter** flags match actual encryption status
3. **Blocks commits** if unencrypted sensitive data is detected
4. **Shows warnings** for potential sensitive content
5. **Allows commits** with properly encrypted content

## How It Works

```
┌──────────────────────────────────────────┐
│  User: git commit -m "message"           │
└──────────────────────────────────────────┘
                  ↓
┌──────────────────────────────────────────┐
│  Pre-commit Hook Triggers                │
├──────────────────────────────────────────┤
│  1. Get list of staged files             │
│  2. Filter to data files (notes/logs)    │
│  3. For each file:                       │
│     a. Parse frontmatter                 │
│     b. Extract encrypted blocks          │
│     c. Scan remaining content            │
│     d. Check for sensitive patterns      │
│  4. Collect all issues                   │
└──────────────────────────────────────────┘
                  ↓
         ┌────────┴────────┐
         │                 │
    ❌ Errors          ✅ No errors
    found?              found?
         │                 │
         ↓                 ↓
┌────────────────┐  ┌────────────────┐
│ Block commit   │  │ Show warnings  │
│ Show errors    │  │ Allow commit   │
│ Exit code: 1   │  │ Exit code: 0   │
└────────────────┘  └────────────────┘
```

## What Gets Detected

### High-Confidence Patterns (BLOCKS commits)

These patterns indicate actual sensitive data and will **block your commit**:

#### 1. API Keys
**Pattern:** `api_key = "..."`

**Examples that trigger:**
```markdown
api_key = "sk_test_1234567890abcdefghijklmnop"
API_KEY="live_key_abcdefghijklmnopqrst"
apiKey: "1234567890abcdefghijklmnop"
```

**Why it's detected:** API keys typically start with prefixes like `sk_`, `pk_`, `live_`, or are long alphanumeric strings assigned to "api_key" variables.

#### 2. Passwords
**Pattern:** `password = "..."`

**Examples that trigger:**
```markdown
password = "mySecretP@ssw0rd"
PASSWORD: "hunter2"
db_password="sup3rs3cr3t"
```

**Why it's detected:** Password assignments are clear indicators of credentials being hardcoded.

#### 3. Secret Keys
**Pattern:** `secret_key = "..."`

**Examples that trigger:**
```markdown
secret_key = "django-secret-key-abc123xyz789"
SECRET_KEY: "flask_secret_here"
secretKey="jwt-signing-key"
```

**Why it's detected:** Secret keys are used for signing, encryption, and should never be in plain text.

#### 4. AWS Credentials
**Patterns:**
- `aws_access_key_id = "AKIA..."`
- `aws_secret_access_key = "..."`

**Examples that trigger:**
```markdown
aws_access_key_id = "AKIAIOSFODNN7EXAMPLE"
aws_secret_access_key = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
```

**Why it's detected:** AWS credentials follow specific formats and grant cloud access.

#### 5. Private Keys (PEM format)
**Pattern:** `-----BEGIN PRIVATE KEY-----`

**Examples that trigger:**
```markdown
-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEA...
-----END RSA PRIVATE KEY-----

-----BEGIN EC PRIVATE KEY-----
...
-----END EC PRIVATE KEY-----

-----BEGIN OPENSSH PRIVATE KEY-----
...
-----END OPENSSH PRIVATE KEY-----
```

**Why it's detected:** Private keys in PEM format are cryptographic secrets that must never be shared.

#### 6. Generic Tokens
**Pattern:** `token = "..."`

**Examples that trigger:**
```markdown
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
access_token: "1234567890abcdefghijklmnop"
auth_token="bearer_token_here"
```

**Why it's detected:** Tokens grant authentication/authorization and should be protected.

#### 7. GitHub Tokens
**Pattern:** `ghp_...`, `gho_...`, `ghu_...`, `ghs_...`

**Examples that trigger:**
```markdown
ghp_1234567890abcdefghijklmnopqrstuvwxyz
token = "gho_abcdefghijklmnopqrstuvwxyz123456"
```

**Why it's detected:** GitHub personal access tokens follow the `gh[pous]_` prefix format.

#### 8. Slack Tokens
**Pattern:** `xoxb-...`, `xoxp-...`, `xoxa-...`, `xoxr-...`

**Examples that trigger:**
```markdown
xoxb-EXAMPLE-EXAMPLE-exampleexampleexample
slack_token = "xoxp-EXAMPLE-EXAMPLE"
```

**Why it's detected:** Slack OAuth tokens follow the `xox[bpar]` prefix format.

#### 9. Client Secrets (OAuth)
**Pattern:** `client_secret = "..."`

**Examples that trigger:**
```markdown
client_secret = "abc123def456ghi789jkl012"
CLIENT_SECRET: "oauth_secret_here"
```

**Why it's detected:** OAuth client secrets authenticate applications.

#### 10-18. Additional Patterns

The hook also detects:
- **Database URLs** with credentials: `postgresql://user:pass@host/db`
- **Connection strings** with passwords
- **JWT secrets**
- **Stripe keys**: `sk_live_...`, `pk_live_...`
- **Twilio credentials**: `AC...` + `auth_token`
- **SendGrid keys**: `SG...`
- **Bearer tokens**: `Bearer ...`
- **Basic auth**: `Authorization: Basic ...`

See the full list in the [test results](../testing/precommit-hook-test-results.md#pattern-coverage).

### Medium-Confidence Patterns (WARNINGS only)

These patterns suggest you should review the content, but won't block commits:

#### 1. TODO Comments about Encryption
**Pattern:** `TODO: encrypt`, `FIXME: encrypt`

**Examples:**
```markdown
<!-- TODO: encrypt this section -->
# FIXME: encrypt before committing
```

**Why it warns:** Indicates you're aware content should be encrypted but haven't done it yet.

#### 2. SENSITIVE Markers
**Pattern:** `SENSITIVE:`, `@sensitive`, `[SENSITIVE]`

**Examples:**
```markdown
SENSITIVE: API keys below
@sensitive
[SENSITIVE] Database passwords
```

**Why it warns:** Explicit markers that content is sensitive.

#### 3. Other Warning Patterns

- `XXX: sensitive`, `HACK: encrypt`
- Comments with "password", "secret", "credential"
- `# pragma: sensitive` style markers

## Common Scenarios

### Scenario 1: Forgot to Encrypt

**What happens:**
```bash
cd ~/.second-brain

# You create a note with sensitive data
echo "API Key: sk_live_abc123..." >> data/notes/note-5.md

# Try to commit
git add data/notes/note-5.md
git commit -m "Add API documentation"
```

**Hook output:**
```
❌ Commit blocked: Sensitive data validation failed

  ❌ data/notes/note-5.md:1
     Unencrypted sensitive data detected: API Key: sk_live_abc123...
     💡 Encrypt this content or remove the sensitive data

💡 To bypass this check (NOT recommended):
   git commit --no-verify
```

**How to fix:**
```bash
# Mark the note as sensitive (encrypts it)
sb mark-sensitive --note-id 5

# Try commit again
git add data/notes/note-5.md
git commit -m "Add API documentation"
# ✅ Passes!
```

### Scenario 2: Encrypted Content

**What happens:**
```bash
# You properly encrypt before committing
sb note create "Credentials" --project security
# Edit the note to add sensitive content
sb mark-sensitive --note-id 6

# Commit
cd ~/.second-brain
git add data/notes/note-6.md
git commit -m "Add credentials"
```

**Hook output:**
```
✅ Validation passed - No sensitive data issues detected
```

**Why it passes:** The hook detects:
- Frontmatter has `encrypted: true`
- File contains `<!-- ENCRYPTED:v1:RSA-AES256-GCM -->` blocks
- Encrypted content is excluded from pattern scanning

### Scenario 3: Warning Markers

**What happens:**
```bash
# You add a TODO comment
echo "TODO: encrypt this later" >> data/notes/note-7.md

# Commit
git add data/notes/note-7.md
git commit -m "Add note"
```

**Hook output:**
```
⚠️  Warnings detected:

  ⚠️  data/notes/note-7.md:1
     Possible sensitive content marker: TODO: encrypt this later
     💡 Review and encrypt if needed

💡 Review these warnings before committing

✅ Validation passed - No sensitive data issues detected
```

**Why it warns:** The TODO comment suggests content might need encryption, but commit is allowed.

### Scenario 4: Multiple Issues

**What happens:**
```bash
# File with multiple sensitive items
cat > data/notes/note-8.md <<EOF
api_key = "sk_test_123..."
password = "mypass123"
token = "bearer_token_here"
EOF

git add data/notes/note-8.md
git commit -m "Add auth info"
```

**Hook output:**
```
❌ Commit blocked: Sensitive data validation failed

  ❌ data/notes/note-8.md:1
     Unencrypted sensitive data detected: api_key = "sk_test_123..."
     💡 Encrypt this content or remove the sensitive data

  ❌ data/notes/note-8.md:2
     Unencrypted sensitive data detected: password = "mypass123"
     💡 Encrypt this content or remove the sensitive data

  ❌ data/notes/note-8.md:3
     Unencrypted sensitive data detected: token = "bearer_token_here"
     💡 Encrypt this content or remove the sensitive data

💡 To bypass this check (NOT recommended):
   git commit --no-verify
```

**How to fix:** Encrypt the entire note with `sb mark-sensitive --note-id 8`

### Scenario 5: False Positives

**What happens:**
```bash
# Documentation about passwords (not actual passwords)
echo "The password field should be at least 8 characters" >> README.md

git add README.md
git commit -m "Update docs"
```

**Hook output:**
```
❌ Commit blocked: Sensitive data validation failed

  ❌ README.md:1
     Unencrypted sensitive data detected: password field should be...
     💡 Encrypt this content or remove the sensitive data
```

**Why it triggers:** The pattern `password\s*[=:]` is broad and may match documentation.

**How to handle:**
```bash
# Option 1: Rephrase to avoid pattern
echo "The user's secret should be at least 8 characters" >> README.md

# Option 2: Use bypass for this specific commit (carefully!)
git commit --no-verify -m "Update docs"
```

**Note:** README.md shouldn't normally be scanned (hook focuses on `data/notes/` and `data/work_logs/`), but this illustrates the concept.

## Working with the Hook

### When Hook Blocks Your Commit

**Step 1:** Read the error message carefully
- Note the file path and line number
- See what pattern was matched

**Step 2:** Decide on action:

**Option A: Content is actually sensitive** → Encrypt it
```bash
sb mark-sensitive --note-id <id>
git add data/notes/note-<id>.md
git commit -m "..."  # Try again
```

**Option B: False positive** → Rephrase content
```bash
# Edit the file to rephrase
vim ~/.second-brain/data/notes/note-<id>.md

git add data/notes/note-<id>.md
git commit -m "..."  # Try again
```

**Option C: Documentation/example** → Bypass cautiously
```bash
# Only use if you're CERTAIN content is safe
git commit --no-verify -m "..."
```

### Checking Hook Status

```bash
# Check if hook is installed
sb install-hooks --check

# View hook file
cat ~/.second-brain/.git/hooks/pre-commit

# Test hook manually (without committing)
cd ~/.second-brain
.git/hooks/pre-commit
```

### Reinstalling Hook

```bash
# If hook is broken or outdated
sb install-hooks --force
```

### Temporarily Disabling Hook

**Warning:** This defeats the purpose of the protection system!

```bash
# Option 1: Use --no-verify flag (per-commit)
git commit --no-verify -m "message"

# Option 2: Remove hook (not recommended)
rm ~/.second-brain/.git/hooks/pre-commit

# Option 3: Make hook non-executable (not recommended)
chmod -x ~/.second-brain/.git/hooks/pre-commit
```

**When to disable:**
- False positives you can't rephrase
- Emergency commits (but review later!)
- Testing/debugging
- **NEVER** for actual sensitive data

## Hook Behavior Details

### Files Scanned

The hook only scans:
- `data/notes/*.md` - Your notes
- `data/work_logs/*.md` - Your work logs

**Not scanned:**
- `.git/` directory
- `keys/` directory
- Documentation files
- Configuration files
- Non-markdown files

### Encrypted Block Handling

When a file contains encrypted blocks:

```markdown
<!-- ENCRYPTED:v1:RSA-AES256-GCM -->
v1:RSA-AES256-GCM:encrypted_key:nonce:ciphertext
<!-- END ENCRYPTED -->
```

The hook:
1. Extracts these blocks
2. Excludes them from pattern scanning
3. Validates frontmatter has `encrypted: true`
4. Scans only the remaining plain text

### Frontmatter Validation

**Valid encrypted file:**
```markdown
---
encrypted: true
is_sensitive: true
---

Some plain text content

<!-- ENCRYPTED:v1:RSA-AES256-GCM -->
v1:RSA-AES256-GCM:...
<!-- END ENCRYPTED -->
```

**Invalid encrypted file:**
```markdown
---
is_sensitive: true
---

No encrypted blocks but marked sensitive!
```

This will be **blocked** with error: "File marked as sensitive but contains no encrypted blocks"

### Error Handling

The hook is designed to "fail open" - if validation encounters an unexpected error:

```
⚠️  Warning: Validation check encountered an error
Error details: [error message]

💡 Allowing commit to proceed (fail-open behavior)
💡 Please report this issue if it persists
```

**Why fail-open:**
- Don't block legitimate work due to bugs
- Hook errors shouldn't prevent commits
- Errors are logged for debugging

## Testing the Hook

### Manual Test 1: API Key Detection

```bash
cd ~/.second-brain
echo "api_key = sk_test_fake123" > test.md
git add test.md
git commit -m "test"
# Expected: ❌ Blocked

rm test.md
git reset
```

### Manual Test 2: Encrypted Content

```bash
sb note create "Test" --project test
sb mark-sensitive --note-id <id>

git add data/notes/note-<id>.md
git commit -m "test"
# Expected: ✅ Allowed

git reset HEAD~1
```

### Manual Test 3: Warning Markers

```bash
echo "TODO: encrypt later" > test.md
git add test.md
git commit -m "test"
# Expected: ⚠️ Warning but allowed

rm test.md
git reset
```

### Automated Tests

See the [comprehensive test results](../testing/precommit-hook-test-results.md) for:
- 12 test scenarios
- Pattern coverage matrix
- Performance benchmarks
- Edge case handling

## Troubleshooting

### Hook not blocking commits

**Check 1:** Verify hook is installed and executable
```bash
ls -la ~/.second-brain/.git/hooks/pre-commit
# Should show: -rwxr-xr-x
```

**Check 2:** Reinstall hook
```bash
sb install-hooks --force
```

**Check 3:** Test hook directly
```bash
cd ~/.second-brain
.git/hooks/pre-commit
echo $?  # Should be 0 if no staged files, 1 if errors
```

### Hook shows import errors

**Symptom:** "No module named 'second_brain'"

**Fix:** Hook needs to use correct Python interpreter
```bash
sb install-hooks --force
```

This will regenerate the hook with the correct Python path.

### Hook is too strict (false positives)

**Option 1:** Rephrase content to avoid patterns
```markdown
# Instead of:
password = "..."

# Use:
credential field = "..."
```

**Option 2:** Use bypass for specific commits
```bash
git commit --no-verify -m "Documentation update"
```

**Option 3:** Report false positives so patterns can be improved

### Hook is too slow

**Current performance:** ~3-5 seconds per commit with multiple files

**If slower:**
- Check file sizes (very large files take longer)
- Check number of staged files
- Report performance issues with details

## Security Considerations

### What the Hook Protects Against

✅ **Accidentally committing:**
- API keys and tokens
- Passwords and secrets
- AWS/cloud credentials
- Private keys
- OAuth secrets

### What the Hook Does NOT Protect Against

❌ **Does not prevent:**
- Intentional bypasses with `--no-verify`
- Commits made before hook installation
- Direct file pushes without git
- Sensitive data in commit messages
- Encrypted data with weak/compromised keys

### Best Practices

1. **Install immediately** after setting up Second Brain
2. **Never bypass** for actual sensitive data
3. **Test regularly** to ensure hook is working
4. **Report issues** if patterns miss sensitive data
5. **Combine with other security measures** (encryption, access control, etc.)

## Related Documentation

- **[Installation Guide](./installation.md)** - Set up the hook
- **[CLI Reference](./cli-reference.md)** - Encryption commands
- **[Best Practices](./best-practices.md)** - Security recommendations
- **[Troubleshooting](./troubleshooting.md)** - Common issues

## Getting Help

- **Hook not working?** See [Troubleshooting](./troubleshooting.md)
- **False positives?** Report at [GitHub Issues](https://github.com/seanm/second-brain/issues)
- **Pattern suggestions?** Open a feature request
- **General questions?** Run `sb --help` or `sb install-hooks --help`
