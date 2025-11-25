# CLI Reference - Encryption Commands

Complete reference for all Second Brain encryption and validation commands.

## Command Overview

| Command | Purpose | Common Use |
|---------|---------|------------|
| `sb key generate` | Generate RSA key pair | Initial setup |
| `sb key info` | View key information | Verify keys exist |
| `sb encrypt` | Encrypt text | Manual encryption |
| `sb decrypt` | Decrypt text | View encrypted content |
| `sb mark-sensitive` | Encrypt note/log | Protect sensitive notes |
| `sb install-hooks` | Install pre-commit hook | Initial setup |

---

## `sb key generate`

Generate a new RSA-4096 key pair for encryption.

### Syntax

```bash
sb key generate [OPTIONS]
```

### Options

| Option | Description | Default |
|--------|-------------|---------|
| `--passphrase` | Prompt for key passphrase (future) | No passphrase |

### Behavior

1. Generates 4096-bit RSA key pair
2. Saves to `~/.second-brain/keys/`
   - `private_key.pem` (mode 600)
   - `public_key.pem` (mode 644)
   - `.key_metadata.json` (fingerprint, timestamp)
3. Adds `keys/` to `.gitignore` if not present
4. Refuses to overwrite existing keys

### Examples

**Basic usage:**
```bash
sb key generate
```

**Output:**
```
✅ Keys generated successfully!

📁 Key locations:
   Private key: /Users/username/.second-brain/keys/private_key.pem
   Public key:  /Users/username/.second-brain/keys/public_key.pem

🔒 Private key permissions: 600 (owner only)
📋 Key fingerprint: sha256:abc123...xyz789

⚠️  IMPORTANT: Backup your private key securely!
   Without it, you cannot decrypt your data.
```

**With existing keys:**
```bash
sb key generate
# ❌ Error: Keys already exist at /Users/username/.second-brain/keys/
#    Use --force to regenerate (WARNING: You will lose access to existing encrypted data!)
```

### Error Conditions

| Error | Cause | Solution |
|-------|-------|----------|
| Keys already exist | Keys present in `~/.second-brain/keys/` | Backup and remove old keys first |
| Permission denied | Cannot write to `~/.second-brain/keys/` | Check directory permissions |
| No .second-brain directory | `~/.second-brain/` doesn't exist | Run `sb init` first |

### Related Commands

- `sb key info` - View key information after generation
- `sb encrypt` - Use keys to encrypt data
- `sb install-hooks` - Set up validation after key generation

---

## `sb key info`

Display information about your encryption keys.

### Syntax

```bash
sb key info [OPTIONS]
```

### Options

Currently no options.

### Output

Displays:
- Key pair existence status
- Private key path
- Public key path
- Key fingerprint (SHA-256)
- Creation timestamp

### Examples

**With keys present:**
```bash
sb key info
```

**Output:**
```
✅ Key pair found

Private key: /Users/username/.second-brain/keys/private_key.pem
Public key:  /Users/username/.second-brain/keys/public_key.pem

Fingerprint: sha256:abc123...xyz789
Created:     2025-11-24 10:30:00 UTC
Permissions: 600 (private), 644 (public)
```

**Without keys:**
```bash
sb key info
```

**Output:**
```
❌ No key pair found

Keys should be located at:
  /Users/username/.second-brain/keys/

To generate keys:
  sb key generate
```

### Error Conditions

| Error | Cause | Solution |
|-------|-------|----------|
| No keys found | Keys not generated yet | Run `sb key generate` |
| Permission denied | Cannot read keys | Check file permissions |
| Corrupted metadata | `.key_metadata.json` invalid | Regenerate keys |

### Use Cases

- **Verify setup:** Check keys exist after installation
- **Debug issues:** Confirm keys are readable
- **Audit keys:** Get fingerprint for key verification
- **Check permissions:** Ensure private key is secure

---

## `sb encrypt`

Encrypt text using your public key.

### Syntax

```bash
sb encrypt [OPTIONS] [TEXT]
echo "text" | sb encrypt
```

### Options

| Option | Description | Default |
|--------|-------------|---------|
| `TEXT` | Text to encrypt (optional) | Read from stdin |
| `--output` | Output format | `base64` |

### Output Format

Encrypted data format:
```
v1:RSA-AES256-GCM:encrypted_key:nonce:ciphertext
```

Components:
- `v1` - Format version
- `RSA-AES256-GCM` - Algorithm
- `encrypted_key` - RSA-encrypted AES key (base64)
- `nonce` - AES-GCM nonce (base64)
- `ciphertext` - Encrypted data (base64)

### Examples

**Encrypt from argument:**
```bash
sb encrypt "Secret password"
```

**Output:**
```
v1:RSA-AES256-GCM:abc123...:def456...:ghi789...
```

**Encrypt from stdin:**
```bash
echo "API key: sk_live_123..." | sb encrypt
```

**Encrypt file contents:**
```bash
cat credentials.txt | sb encrypt > credentials.enc
```

**Encrypt multiline text:**
```bash
sb encrypt "Line 1
Line 2
Line 3"
```

### Error Conditions

| Error | Cause | Solution |
|-------|-------|----------|
| No keys found | Keys not generated | Run `sb key generate` |
| Permission denied | Cannot read public key | Check key permissions |
| Empty input | No text provided | Provide text or pipe input |
| Encryption failed | Invalid key or crypto error | Check key integrity |

### Use Cases

- **Manual encryption:** Encrypt specific values
- **Testing:** Verify encryption works
- **Integration:** Encrypt data from scripts
- **Backup:** Encrypt sensitive files

### Related Commands

- `sb decrypt` - Decrypt encrypted text
- `sb mark-sensitive` - Encrypt entire notes/logs

---

## `sb decrypt`

Decrypt text using your private key.

### Syntax

```bash
sb decrypt [OPTIONS] [ENCRYPTED_TEXT]
echo "v1:RSA-AES256-GCM:..." | sb decrypt
```

### Options

| Option | Description | Default |
|--------|-------------|---------|
| `ENCRYPTED_TEXT` | Encrypted text (optional) | Read from stdin |
| `--passphrase` | Prompt for key passphrase (future) | No passphrase |

### Input Format

Expects encrypted data in format:
```
v1:RSA-AES256-GCM:encrypted_key:nonce:ciphertext
```

### Examples

**Decrypt from argument:**
```bash
sb decrypt "v1:RSA-AES256-GCM:abc123...:def456...:ghi789..."
```

**Output:**
```
Secret password
```

**Decrypt from stdin:**
```bash
echo "v1:RSA-AES256-GCM:..." | sb decrypt
```

**Decrypt file:**
```bash
cat encrypted.txt | sb decrypt
```

**Decrypt and save:**
```bash
sb decrypt "v1:RSA-AES256-GCM:..." > decrypted.txt
```

**Decrypt from note:**
```bash
# Extract encrypted block from note
grep "v1:RSA-AES256-GCM" ~/.second-brain/data/notes/note-5.md | sb decrypt
```

### Error Conditions

| Error | Cause | Solution |
|-------|-------|----------|
| No keys found | Private key missing | Check key exists |
| Invalid format | Wrong encrypted format | Check input format |
| Decryption failed | Wrong key or corrupted data | Verify key matches encryption key |
| Permission denied | Cannot read private key | Check key permissions (should be 600) |

### Security Notes

- Decrypted data is output to stdout - be careful with sensitive data
- Consider piping to `less` or redirecting to secure location
- Never commit decrypted data to git

### Use Cases

- **View encrypted notes:** Read sensitive content
- **Verify encryption:** Test encrypt/decrypt cycle
- **Extract secrets:** Get credentials from encrypted storage
- **Debugging:** Verify content was encrypted correctly

### Related Commands

- `sb encrypt` - Encrypt text
- `sb mark-sensitive` - View encrypted notes/logs

---

## `sb mark-sensitive`

Mark a note or work log entry as sensitive (encrypts all content).

### Syntax

```bash
sb mark-sensitive [OPTIONS]
```

### Options

| Option | Description | Required |
|--------|-------------|----------|
| `--note-id ID` | Note ID to mark sensitive | One of note-id or log-id |
| `--log-id ID` | Work log entry ID | One of note-id or log-id |
| `--passphrase` | Prompt for key passphrase (future) | No |

### Behavior

1. Reads note/log content from markdown file
2. Extracts frontmatter metadata
3. Encrypts all content (except frontmatter)
4. Updates frontmatter:
   - Sets `is_sensitive: true`
   - Sets `encrypted: true`
5. Wraps encrypted content in markdown blocks:
   ```markdown
   <!-- ENCRYPTED:v1:RSA-AES256-GCM -->
   v1:RSA-AES256-GCM:...
   <!-- END ENCRYPTED -->
   ```
6. Updates database record
7. Saves updated markdown file

### Examples

**Encrypt a note:**
```bash
sb mark-sensitive --note-id 5
```

**Output:**
```
✅ Note #5 marked as sensitive and encrypted

📝 Note: "API Keys Documentation"
🔒 Encryption: v1:RSA-AES256-GCM
📁 File: /Users/username/.second-brain/data/notes/note-5.md

The note content is now encrypted. Use 'sb decrypt' to view.
```

**Encrypt a work log entry:**
```bash
sb mark-sensitive --log-id 10
```

**Encrypt multiple items:**
```bash
# Encrypt notes 5, 6, 7
for id in 5 6 7; do
    sb mark-sensitive --note-id $id
done
```

### File Changes

**Before:**
```markdown
---
id: 5
title: API Keys
created: 2025-11-24
---

Production API: sk_live_abc123...
Staging API: sk_test_xyz789...
```

**After:**
```markdown
---
id: 5
title: API Keys
created: 2025-11-24
is_sensitive: true
encrypted: true
---

<!-- ENCRYPTED:v1:RSA-AES256-GCM -->
v1:RSA-AES256-GCM:encrypted_key:nonce:ciphertext
<!-- END ENCRYPTED -->
```

### Error Conditions

| Error | Cause | Solution |
|-------|-------|----------|
| Note/log not found | Invalid ID | Check ID exists with `sb note list` |
| No keys found | Keys not generated | Run `sb key generate` |
| Already encrypted | Content already encrypted | Already protected, no action needed |
| Permission denied | Cannot write file | Check file/directory permissions |
| File not found | Markdown file missing | Database may be corrupted |

### Important Notes

**Irreversible:** Once encrypted, you cannot decrypt with a different key. Backup your private key!

**Database and Files:** Both the database and markdown file are updated for consistency.

**Git Integration:** After marking as sensitive:
```bash
cd ~/.second-brain
git add data/notes/note-5.md
git commit -m "Encrypt API keys"
# ✅ Pre-commit hook will allow this (content is encrypted)
```

### Use Cases

- **Protect credentials:** Encrypt notes containing API keys, passwords
- **Secure personal data:** Protect SSN, account numbers, etc.
- **Work logs:** Encrypt logs containing sensitive project details
- **Before syncing:** Encrypt before pushing to GitHub

### Related Commands

- `sb decrypt` - View encrypted content
- `sb note create` - Create notes to encrypt
- `sb log create` - Create work logs to encrypt

---

## `sb install-hooks`

Install git pre-commit hooks for validation.

### Syntax

```bash
sb install-hooks [OPTIONS]
```

### Options

| Option | Description | Default |
|--------|-------------|---------|
| `--check` | Check hook installation status | False |
| `--force` | Reinstall even if exists | False |

### Behavior

1. Locates `.git/hooks/` in `~/.second-brain/`
2. Creates `pre-commit` hook script
3. Configures hook to use correct Python interpreter
4. Makes hook executable (mode 755)
5. Verifies installation

### Examples

**Install hook:**
```bash
sb install-hooks
```

**Output:**
```
✅ Pre-commit hook installed successfully!

📁 Hook location: /Users/username/.second-brain/.git/hooks/pre-commit

The hook will now validate commits to prevent accidental exposure of sensitive data.

To check hook status: sb install-hooks --check
To reinstall: sb install-hooks --force
```

**Check installation status:**
```bash
sb install-hooks --check
```

**Output (installed):**
```
✅ Pre-commit hook is installed

Location:    /Users/username/.second-brain/.git/hooks/pre-commit
Executable:  Yes
Valid:       Yes
Python path: /Users/username/.local/share/uv/tools/second-brain/bin/python3

The hook will run automatically before each commit.
```

**Output (not installed):**
```
❌ Pre-commit hook is NOT installed

Expected location: /Users/username/.second-brain/.git/hooks/pre-commit

To install:
  sb install-hooks
```

**Reinstall hook:**
```bash
sb install-hooks --force
```

**Output:**
```
⚠️  Existing hook found, reinstalling (--force)

✅ Pre-commit hook reinstalled successfully!
```

### Hook Behavior

Once installed, the hook:
- Runs automatically before every `git commit`
- Scans staged files for sensitive data patterns
- Blocks commits with unencrypted sensitive data
- Shows warnings for potential issues
- Allows commits with encrypted content

### Error Conditions

| Error | Cause | Solution |
|-------|-------|----------|
| Not a git repository | `~/.second-brain/.git/` missing | Initialize git: `cd ~/.second-brain && git init` |
| Permission denied | Cannot write to `.git/hooks/` | Check directory permissions |
| Hook exists | Hook already installed | Use `--force` to reinstall |
| Python not found | Cannot determine Python path | Check Second Brain installation |

### Testing Installation

```bash
# Test 1: Check status
sb install-hooks --check

# Test 2: Manual run
cd ~/.second-brain
.git/hooks/pre-commit
# Should output: ✅ Validation passed (no staged files)

# Test 3: Test blocking
echo "api_key = sk_test_fake" > test.md
git add test.md
git commit -m "test"
# Should block with error

# Clean up
rm test.md
git reset
```

### Maintenance

**Update hook:** When Second Brain is updated, reinstall the hook:
```bash
sb install-hooks --force
```

**Remove hook:** To uninstall:
```bash
rm ~/.second-brain/.git/hooks/pre-commit
```

**Verify hook:** Periodically check hook is working:
```bash
sb install-hooks --check
```

### Use Cases

- **Initial setup:** Install as part of Second Brain setup
- **After updates:** Reinstall when Second Brain is updated
- **Troubleshooting:** Reinstall if hook stops working
- **Verification:** Check hook is properly configured

### Related Commands

- `sb key generate` - Generate keys before installing hook
- `sb mark-sensitive` - Fix issues found by hook

---

## Common Workflows

### Initial Setup

```bash
# 1. Generate keys
sb key generate

# 2. Install pre-commit hook
sb install-hooks

# 3. Verify setup
sb key info
sb install-hooks --check

# 4. Test encryption
echo "test" | sb encrypt | sb decrypt
```

### Daily Use - Protect Sensitive Note

```bash
# 1. Create note
sb note create "Credentials" --project security

# 2. Edit note to add sensitive content
# (use your editor)

# 3. Encrypt note
sb mark-sensitive --note-id 5

# 4. Commit safely
cd ~/.second-brain
git add data/notes/note-5.md
git commit -m "Add encrypted credentials"
git push
```

### View Encrypted Content

```bash
# Option 1: Decrypt specific block
grep "v1:RSA-AES256-GCM" ~/.second-brain/data/notes/note-5.md | sb decrypt

# Option 2: Decrypt entire file content
# (extract encrypted blocks and decrypt each)
```

### Handle Pre-commit Blocking

```bash
# Scenario: Hook blocks your commit

# 1. See what was detected
# (error message shows file and line)

# 2. Encrypt the content
sb mark-sensitive --note-id 5

# 3. Stage changes
git add data/notes/note-5.md

# 4. Retry commit
git commit -m "Add note"
# ✅ Should pass now
```

### Backup and Restore Keys

```bash
# Backup keys
cp -r ~/.second-brain/keys ~/backup/second-brain-keys-2025-11-24/

# Restore keys (on new machine)
mkdir -p ~/.second-brain/keys
cp ~/backup/second-brain-keys-2025-11-24/* ~/.second-brain/keys/
chmod 600 ~/.second-brain/keys/private_key.pem
chmod 644 ~/.second-brain/keys/public_key.pem

# Verify restoration
sb key info
```

---

## Exit Codes

All commands use standard exit codes:

| Code | Meaning | Example |
|------|---------|---------|
| `0` | Success | Encryption successful |
| `1` | Error | Keys not found |
| `2` | Invalid arguments | Missing required option |

Pre-commit hook specific:
| Code | Meaning | Action |
|------|---------|--------|
| `0` | Validation passed | Commit allowed |
| `1` | Validation failed | Commit blocked |

---

## Environment Variables

Currently, no environment variables are used. All configuration is file-based.

Future environment variables may include:
- `SECOND_BRAIN_KEYS_DIR` - Custom keys location
- `SECOND_BRAIN_KEY_PASSPHRASE` - Non-interactive key passphrase

---

## Related Documentation

- **[Installation Guide](./installation.md)** - Set up encryption
- **[Pre-commit Hook Guide](./precommit-hook.md)** - Understanding the hook
- **[Best Practices](./best-practices.md)** - Security recommendations
- **[Troubleshooting](./troubleshooting.md)** - Fixing common issues

---

## Getting Help

**Command help:**
```bash
sb --help
sb key --help
sb encrypt --help
sb mark-sensitive --help
sb install-hooks --help
```

**Documentation:**
- Online docs: https://github.com/seanm/second-brain/tree/main/docs
- README: `~/.second-brain/README.md`

**Issues:**
- Report bugs: https://github.com/seanm/second-brain/issues
- Feature requests: https://github.com/seanm/second-brain/issues/new
