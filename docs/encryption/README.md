# Encryption & Sensitive Data Protection

## Overview

Second Brain includes a comprehensive encryption system to protect sensitive information before syncing to GitHub. The system uses hybrid RSA-4096 + AES-256-GCM encryption with automated pre-commit validation to prevent accidental exposure of secrets.

## Quick Start

### 1. Generate Encryption Keys

```bash
# Generate RSA key pair
sb key generate

# View key information
sb key info
```

**Important:** Backup your private key securely! Without it, you cannot decrypt your data.

### 2. Install Git Pre-commit Hook

```bash
# Install validation hook
sb install-hooks

# Verify installation
sb install-hooks --check
```

### 3. Mark Sensitive Content

```bash
# Encrypt a note
sb mark-sensitive --note-id 5

# Encrypt a work log entry
sb mark-sensitive --log-id 10
```

### 4. Test the Protection

```bash
cd ~/.second-brain

# Create a file with fake sensitive data
echo "api_key = sk_test_fake123" > data/notes/test.md
git add data/notes/test.md
git commit -m "test"

# Hook will block the commit ✓
```

## What Gets Protected

### High-Confidence Patterns (Blocks Commits)

The pre-commit hook automatically detects and blocks:

- **API Keys:** `api_key = "sk_..."`
- **Passwords:** `password = "..."`
- **Secret Keys:** `secret_key = "..."`
- **AWS Credentials:** `aws_access_key_id`, `aws_secret_access_key`
- **Private Keys:** `-----BEGIN RSA PRIVATE KEY-----`
- **Tokens:** `token = "..."`, GitHub tokens (`ghp_...`), Slack tokens (`xox...`)
- **Client Secrets:** `client_secret = "..."`

### Medium-Confidence Patterns (Shows Warnings)

The hook warns about but allows:

- **Markers:** `SENSITIVE:`, `@sensitive`, `[SENSITIVE]`
- **TODO Comments:** `TODO: encrypt this`, `FIXME: encrypt`

## Documentation

- **[Installation Guide](./installation.md)** - Step-by-step setup
- **[Pre-commit Hook Guide](./precommit-hook.md)** - Hook installation and usage
- **[CLI Reference](./cli-reference.md)** - All encryption commands
- **[Troubleshooting](./troubleshooting.md)** - Common issues and solutions
- **[Best Practices](./best-practices.md)** - Security recommendations

## Architecture

```
┌─────────────────────────────────────────────┐
│         Encryption System                   │
├─────────────────────────────────────────────┤
│                                             │
│  RSA-4096 Key Pair                         │
│  └─ ~/.second-brain/keys/                  │
│      ├── private_key.pem (600)             │
│      └── public_key.pem (644)              │
│                                             │
│  AES-256-GCM Data Encryption               │
│  └─ Hybrid: RSA for keys, AES for data    │
│                                             │
│  Encrypted Block Format                    │
│  └─ <!-- ENCRYPTED:v1:RSA-AES256-GCM --> │
│      v1:RSA-AES256-GCM:key:nonce:cipher   │
│      <!-- END ENCRYPTED -->                │
│                                             │
│  Pre-commit Validation                     │
│  └─ ~/.second-brain/.git/hooks/pre-commit │
│      └─ Pattern detection (18 patterns)    │
│      └─ Frontmatter validation             │
│      └─ Encrypted block handling           │
│                                             │
└─────────────────────────────────────────────┘
```

## Files & Locations

```
~/.second-brain/
├── keys/
│   ├── private_key.pem      # Your private key (NEVER commit!)
│   ├── public_key.pem       # Public key (safe to share)
│   └── .key_metadata.json   # Key fingerprint and info
├── .git/hooks/
│   └── pre-commit           # Validation hook
└── data/
    ├── notes/               # Encrypted notes here
    └── work_logs/           # Encrypted logs here
```

## Security Features

✅ **4096-bit RSA Keys** - Industry-standard key length
✅ **AES-256-GCM** - Authenticated encryption with integrity checks
✅ **Automatic Validation** - Pre-commit hook blocks unencrypted secrets
✅ **Pattern Detection** - 18 high-confidence + 10 warning patterns
✅ **Proper Permissions** - Private key locked to 600 (owner-only)
✅ **Gitignore Protection** - Private keys automatically excluded
✅ **Markdown Integration** - Encrypted blocks in human-readable format

## Workflow Example

### Typical Daily Use

```bash
# Morning - work on sensitive project
sb note create "API Keys" --project my-app

# Add sensitive content
echo "Production API: sk_live_abc123..." >> ~/.second-brain/data/notes/note-5.md

# Mark as sensitive (encrypts content)
sb mark-sensitive --note-id 5

# Commit safely
cd ~/.second-brain
git add data/notes/note-5.md
git commit -m "Add API documentation"  # ✓ Passes validation

# Decrypt to view
sb decrypt "$(cat data/notes/note-5.md | grep 'v1:RSA')"
```

### If You Forget to Encrypt

```bash
# Create note with API key
echo "api_key = sk_live_secret123" >> data/notes/note-6.md

# Try to commit
git add data/notes/note-6.md
git commit -m "Add API notes"

# ❌ Hook blocks:
# Commit blocked: Sensitive data validation failed
#   ❌ data/notes/note-6.md:1
#      Unencrypted sensitive data detected: api_key = "sk_live_secret123"
#      💡 Run: sb mark-sensitive --note-id 6

# Fix it
sb mark-sensitive --note-id 6
git add data/notes/note-6.md
git commit -m "Add API notes"  # ✓ Now passes
```

## Testing Your Setup

```bash
# 1. Verify keys exist
sb key info

# 2. Verify hook is installed
sb install-hooks --check

# 3. Test encryption
echo "Secret data" | sb encrypt

# 4. Test hook blocking
cd ~/.second-brain
echo "password = test123" > data/notes/test-hook.md
git add data/notes/test-hook.md
git commit -m "test"  # Should block

# 5. Clean up
rm data/notes/test-hook.md
git reset
```

## Getting Help

- **Issues:** Report bugs at [GitHub Issues](https://github.com/seanm/second-brain/issues)
- **Documentation:** See [docs/encryption/](.)
- **CLI Help:** `sb --help`, `sb encrypt --help`, `sb install-hooks --help`

## Next Steps

1. Read the [Installation Guide](./installation.md) for detailed setup
2. Review [Best Practices](./best-practices.md) for security tips
3. Check [Troubleshooting](./troubleshooting.md) if you encounter issues
