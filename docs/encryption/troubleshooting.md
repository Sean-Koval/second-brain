# Troubleshooting - Encryption & Pre-commit Hooks

Common issues and solutions for the Second Brain encryption system.

## Table of Contents

- [Key Generation Issues](#key-generation-issues)
- [Encryption/Decryption Issues](#encryptiondecryption-issues)
- [Pre-commit Hook Issues](#pre-commit-hook-issues)
- [Permission Issues](#permission-issues)
- [Performance Issues](#performance-issues)
- [Data Recovery](#data-recovery)

---

## Key Generation Issues

### Keys Already Exist

**Symptom:**
```
❌ Error: Keys already exist at /Users/username/.second-brain/keys/
   Use --force to regenerate (WARNING: You will lose access to existing encrypted data!)
```

**Cause:** You already have encryption keys generated.

**Solutions:**

**Option 1: Keep existing keys (recommended)**
```bash
# Verify keys work
sb key info

# Test encryption
echo "test" | sb encrypt | sb decrypt
```

**Option 2: Regenerate keys (DANGER: loses access to encrypted data!)**
```bash
# ⚠️  WARNING: Backup keys first!
cp -r ~/.second-brain/keys ~/keys-backup-$(date +%Y%m%d)

# Remove old keys
rm -rf ~/.second-brain/keys

# Generate new keys
sb key generate
```

**Important:** If you have encrypted notes/logs, you CANNOT decrypt them with new keys!

---

### Permission Denied During Key Generation

**Symptom:**
```
❌ Error: Permission denied: '/Users/username/.second-brain/keys/private_key.pem'
```

**Cause:** Cannot write to `~/.second-brain/keys/` directory.

**Solutions:**

**Fix directory permissions:**
```bash
# Check directory exists
mkdir -p ~/.second-brain/keys

# Fix permissions
chmod 755 ~/.second-brain
chmod 755 ~/.second-brain/keys

# Retry
sb key generate
```

**Check disk space:**
```bash
df -h ~
# Ensure you have free space
```

---

### .second-brain Directory Not Found

**Symptom:**
```
❌ Error: Directory '/Users/username/.second-brain' does not exist
```

**Cause:** Second Brain not initialized.

**Solution:**
```bash
# Initialize Second Brain
sb init

# Verify
ls -la ~/.second-brain

# Try again
sb key generate
```

---

## Encryption/Decryption Issues

### Cannot Read Public/Private Key

**Symptom:**
```
❌ Error: No keys found. Generate keys with: sb key generate
```

**Cause:** Keys don't exist or aren't readable.

**Diagnosis:**
```bash
# Check keys exist
ls -la ~/.second-brain/keys/

# Check permissions
ls -l ~/.second-brain/keys/*.pem
# Should show:
# -rw------- (600) private_key.pem
# -rw-r--r-- (644) public_key.pem

# Check key info
sb key info
```

**Solutions:**

**If keys don't exist:**
```bash
sb key generate
```

**If permissions are wrong:**
```bash
chmod 600 ~/.second-brain/keys/private_key.pem
chmod 644 ~/.second-brain/keys/public_key.pem
```

**If keys are corrupted:**
```bash
# Check key format
head -1 ~/.second-brain/keys/private_key.pem
# Should show: -----BEGIN RSA PRIVATE KEY-----

head -1 ~/.second-brain/keys/public_key.pem
# Should show: -----BEGIN PUBLIC KEY-----

# If corrupted, regenerate (WARNING: loses access to encrypted data)
rm -rf ~/.second-brain/keys
sb key generate
```

---

### Decryption Failed

**Symptom:**
```
❌ Error: Decryption failed: Invalid ciphertext or wrong key
```

**Causes:**
1. Wrong private key (not the one used for encryption)
2. Corrupted encrypted data
3. Invalid encrypted format

**Diagnosis:**

**Check encrypted format:**
```bash
# Valid format:
# v1:RSA-AES256-GCM:encrypted_key:nonce:ciphertext

# Count colons (should be 4)
echo "v1:RSA-AES256-GCM:..." | tr -cd ':' | wc -c
# Should output: 4
```

**Check key fingerprint:**
```bash
sb key info
# Note the fingerprint

# If you have the original encryption key fingerprint, compare
# If different, you're using wrong key
```

**Solutions:**

**If wrong key:**
- Restore original private key from backup
- Cannot decrypt with different key

**If corrupted data:**
- Data may be unrecoverable
- Restore from backup if available

**If format error:**
```bash
# Ensure proper format (no extra spaces/newlines)
echo "v1:RSA-AES256-GCM:key:nonce:cipher" | tr -d '\n' | sb decrypt
```

---

### Encryption Produces Empty Output

**Symptom:**
```bash
echo "test" | sb encrypt
# No output
```

**Cause:** Input is empty or encryption failed silently.

**Diagnosis:**
```bash
# Check input reaches command
echo "test" | tee /dev/stderr | sb encrypt

# Check command output
sb encrypt "test" ; echo "Exit code: $?"
# Exit code should be 0 for success
```

**Solutions:**

**Verify keys work:**
```bash
sb key info
# Should show keys exist

# Test directly
sb encrypt "test data"
# Should output: v1:RSA-AES256-GCM:...
```

**Check for errors:**
```bash
sb encrypt "test" 2>&1 | tee output.log
cat output.log
```

---

## Pre-commit Hook Issues

### Hook Not Blocking Sensitive Data

**Symptom:** Commits succeed even with API keys, passwords, etc.

**Diagnosis:**

**Step 1: Check hook is installed**
```bash
sb install-hooks --check
# Should show: ✅ Pre-commit hook is installed
```

**Step 2: Check hook is executable**
```bash
ls -l ~/.second-brain/.git/hooks/pre-commit
# Should show: -rwxr-xr-x (executable)
```

**Step 3: Test hook directly**
```bash
cd ~/.second-brain
echo "api_key = sk_test_fake" > test.md
git add test.md
.git/hooks/pre-commit
echo "Exit code: $?"
# Should be 1 (error)

rm test.md
git reset
```

**Step 4: Check hook output**
```bash
# Run hook with output
cd ~/.second-brain
echo "password = test123" > test.md
git add test.md
.git/hooks/pre-commit 2>&1 | tee hook-output.log
cat hook-output.log

rm test.md
git reset
```

**Solutions:**

**Reinstall hook:**
```bash
sb install-hooks --force
```

**Check Python path:**
```bash
head -1 ~/.second-brain/.git/hooks/pre-commit
# Should show: #!/path/to/python

# Verify that Python has second_brain module
/path/to/python -c "import second_brain; print('OK')"
# Should output: OK
```

**Check git invocation:**
```bash
# Ensure not using --no-verify
git commit -m "test"  # Correct
git commit --no-verify -m "test"  # Bypasses hook!
```

---

### Hook Shows Module Import Error

**Symptom:**
```
❌ Error: No module named 'second_brain'
```

**Cause:** Hook is using wrong Python interpreter.

**Solutions:**

**Reinstall hook (fixes Python path):**
```bash
sb install-hooks --force
```

**Verify Python path:**
```bash
# Check which Python sb uses
which sb
# Example: /Users/username/.local/bin/sb

# Check Python in hook
head -1 ~/.second-brain/.git/hooks/pre-commit
# Should point to same Python environment
```

**Manual fix (if needed):**
```bash
# Find correct Python
python3 -c "import second_brain; import sys; print(sys.executable)"
# Example: /Users/username/.local/share/uv/tools/second-brain/bin/python3

# Edit hook shebang
vim ~/.second-brain/.git/hooks/pre-commit
# Change first line to: #!/path/to/python3
```

---

### Hook Shows Frontmatter Error

**Symptom:**
```
❌ Error: No module named 'frontmatter'
```

**Cause:** `python-frontmatter` package not installed in hook's Python environment.

**Solutions:**

**Reinstall Second Brain:**
```bash
uv tool reinstall second-brain
# or
cd /path/to/second-brain-repo
uv pip install -e .
```

**Verify installation:**
```bash
python3 -c "import frontmatter; print('OK')"
# Should output: OK
```

**Reinstall hook:**
```bash
sb install-hooks --force
```

---

### Hook Blocks False Positives

**Symptom:** Hook blocks documentation or non-sensitive content.

**Examples:**
```
❌ data/notes/README.md:10
   Unencrypted sensitive data detected: password field should be...
```

**Cause:** Pattern matching is broad and catches documentation about passwords.

**Solutions:**

**Option 1: Rephrase content**
```markdown
# Instead of:
The password should be at least 8 characters

# Use:
The credential should be at least 8 characters
The user's secret should be at least 8 characters
Authentication requires 8+ characters
```

**Option 2: Use bypass (carefully!)**
```bash
# Only if you're CERTAIN content is safe
git commit --no-verify -m "Update documentation"
```

**Option 3: Report false positive**
```bash
# Create issue with:
# - Exact pattern matched
# - Why it's a false positive
# - Suggested pattern improvement
```

**Note:** Most false positives occur with:
- Documentation about passwords/keys
- Example code with "password = "
- Comments about security

The patterns are intentionally conservative to avoid missing real secrets.

---

### Hook is Too Slow

**Symptom:** Commits take >10 seconds.

**Diagnosis:**
```bash
cd ~/.second-brain

# Time hook execution
time .git/hooks/pre-commit
# Should be <5 seconds normally
```

**Causes:**
1. Very large files
2. Many staged files
3. Disk I/O issues

**Solutions:**

**Check file sizes:**
```bash
git diff --staged --name-only | xargs ls -lh
# Look for files >1MB
```

**Check file count:**
```bash
git diff --staged --name-only | wc -l
# If >100 files, consider smaller commits
```

**Optimize commits:**
```bash
# Commit smaller batches
git add data/notes/note-1.md data/notes/note-2.md
git commit -m "Add notes 1-2"

git add data/notes/note-3.md data/notes/note-4.md
git commit -m "Add notes 3-4"
```

---

## Permission Issues

### Private Key Permission Denied

**Symptom:**
```
❌ Error: Permission denied: '/Users/username/.second-brain/keys/private_key.pem'
```

**Cause:** Insufficient permissions to read private key.

**Diagnosis:**
```bash
ls -l ~/.second-brain/keys/private_key.pem
# Should show: -rw------- (600)
```

**Solutions:**

**Fix file permissions:**
```bash
chmod 600 ~/.second-brain/keys/private_key.pem
```

**Fix ownership (if needed):**
```bash
# If file is owned by different user
sudo chown $USER:$USER ~/.second-brain/keys/private_key.pem
chmod 600 ~/.second-brain/keys/private_key.pem
```

---

### Hook Permission Denied

**Symptom:**
```
-bash: /Users/username/.second-brain/.git/hooks/pre-commit: Permission denied
```

**Cause:** Hook is not executable.

**Solution:**
```bash
chmod +x ~/.second-brain/.git/hooks/pre-commit

# Verify
ls -l ~/.second-brain/.git/hooks/pre-commit
# Should show: -rwxr-xr-x
```

---

## Performance Issues

### Slow Key Generation

**Symptom:** `sb key generate` takes >30 seconds.

**Cause:** RSA-4096 key generation is CPU-intensive (normal).

**Expected time:**
- Fast machines: 5-15 seconds
- Slow machines: 30-60 seconds

**Not a problem unless:**
- Takes >2 minutes
- System becomes unresponsive

**Solutions if too slow:**
```bash
# Check system load
top
# Look for other CPU-intensive processes

# Try again with less load
sb key generate
```

---

### Slow Encryption/Decryption

**Symptom:** Encrypting/decrypting takes >5 seconds for small data.

**Diagnosis:**
```bash
# Time encryption
time echo "test" | sb encrypt
# Should be <1 second

# Time decryption
ENCRYPTED=$(echo "test" | sb encrypt)
time echo "$ENCRYPTED" | sb decrypt
# Should be <1 second
```

**Causes:**
- Very large data
- Disk I/O issues
- Key access problems

**Solutions:**

**For large data:**
```bash
# Encrypt smaller chunks
# Or use file-based encryption
```

**Check key access:**
```bash
time cat ~/.second-brain/keys/private_key.pem > /dev/null
# Should be instant (<0.1s)
```

---

## Data Recovery

### Lost Private Key

**Symptom:** Private key deleted or corrupted, cannot decrypt data.

**Solutions:**

**Option 1: Restore from backup**
```bash
# If you have backup
cp ~/backup/private_key.pem ~/.second-brain/keys/
chmod 600 ~/.second-brain/keys/private_key.pem

# Verify
sb key info
echo "test" | sb encrypt | sb decrypt
```

**Option 2: Search for key backup**
```bash
# Check common locations
find ~ -name "private_key.pem" 2>/dev/null
find ~ -name "*second-brain*backup*" 2>/dev/null

# Check Time Machine (macOS)
# Check backup drives
```

**Option 3: Accept data loss**
- If no backup exists, encrypted data is unrecoverable
- RSA encryption is cryptographically secure - cannot be broken
- Generate new keys for future data:
  ```bash
  rm -rf ~/.second-brain/keys
  sb key generate
  ```

**Prevention:**
```bash
# Create multiple backups
cp ~/.second-brain/keys/private_key.pem ~/Dropbox/backups/
cp ~/.second-brain/keys/private_key.pem /external-drive/backups/

# Print paper backup
cat ~/.second-brain/keys/private_key.pem | lpr
```

---

### Corrupted Encrypted Data

**Symptom:** Cannot decrypt specific note/log entry.

**Diagnosis:**
```bash
# Extract encrypted block
grep -A2 "ENCRYPTED:v1" ~/.second-brain/data/notes/note-5.md

# Try to decrypt
grep "v1:RSA-AES256-GCM" ~/.second-brain/data/notes/note-5.md | sb decrypt
```

**Causes:**
1. File was manually edited and broke encryption format
2. Disk corruption
3. Incomplete encryption operation

**Solutions:**

**Option 1: Restore from git history**
```bash
cd ~/.second-brain

# Check git history
git log --oneline data/notes/note-5.md

# Restore previous version
git show HEAD^:data/notes/note-5.md > data/notes/note-5.md

# Try decryption again
```

**Option 2: Restore from backup**
```bash
# If you have external backups
cp ~/backup/note-5.md ~/.second-brain/data/notes/
```

**Option 3: Accept loss of specific entry**
- If no backup, that specific note/log is unrecoverable
- Other encrypted items should still work

---

### Database Out of Sync with Files

**Symptom:** `sb mark-sensitive --note-id 5` shows note in database, but file doesn't exist or vice versa.

**Diagnosis:**
```bash
# Check database
sb note list | grep "#5"

# Check file
ls ~/.second-brain/data/notes/note-5.md

# Check file content
cat ~/.second-brain/data/notes/note-5.md
```

**Solutions:**

**If file exists but not in database:**
```bash
# Re-sync database (future feature)
# Current workaround: Manually add to database
# Or recreate note
```

**If database entry exists but file doesn't:**
```bash
# Delete database entry (future feature)
# Current workaround: Ignore the entry
# Or restore file from backup
```

---

## Getting Additional Help

### Enable Debug Output

```bash
# Run commands with verbose output
sb --debug encrypt "test"  # Future feature

# Check logs
cat ~/.second-brain/logs/second-brain.log  # Future feature
```

### Collect Diagnostic Information

```bash
# System info
uname -a
python3 --version

# Second Brain version
sb --version

# Key status
sb key info

# Hook status
sb install-hooks --check

# Git status
cd ~/.second-brain
git status
ls -la .git/hooks/

# Permissions
ls -la ~/.second-brain/keys/
```

### Report Issues

When reporting issues, include:

1. **Command that failed:**
   ```bash
   sb mark-sensitive --note-id 5
   ```

2. **Error message:**
   ```
   ❌ Error: ...
   ```

3. **System information:**
   - OS: macOS 14.0
   - Python: 3.14
   - Second Brain version: 1.0.0

4. **Steps to reproduce:**
   - Step 1: ...
   - Step 2: ...
   - Result: ...

5. **Diagnostic output:**
   ```bash
   sb key info
   sb install-hooks --check
   ```

**Where to report:**
- GitHub Issues: https://github.com/seanm/second-brain/issues
- Include "encryption" or "pre-commit" label

---

## Quick Reference

### Most Common Issues

| Issue | Quick Fix |
|-------|-----------|
| Hook not blocking | `sb install-hooks --force` |
| Module import error | `sb install-hooks --force` |
| Permission denied (private key) | `chmod 600 ~/.second-brain/keys/private_key.pem` |
| Hook not executable | `chmod +x ~/.second-brain/.git/hooks/pre-commit` |
| Decryption failed | Verify using correct key: `sb key info` |
| Keys don't exist | `sb key generate` |

### Diagnostic Commands

```bash
# Check everything
sb key info
sb install-hooks --check
cd ~/.second-brain && .git/hooks/pre-commit

# Test encryption cycle
echo "test" | sb encrypt | sb decrypt

# Check file permissions
ls -la ~/.second-brain/keys/
ls -l ~/.second-brain/.git/hooks/pre-commit
```

---

## Related Documentation

- **[Installation Guide](./installation.md)** - Setup instructions
- **[CLI Reference](./cli-reference.md)** - Command documentation
- **[Pre-commit Hook Guide](./precommit-hook.md)** - Hook behavior
- **[Best Practices](./best-practices.md)** - Avoid common issues
