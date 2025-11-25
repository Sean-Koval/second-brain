# Installation Guide - Encryption & Pre-commit Hooks

This guide walks you through setting up encryption and the pre-commit validation hook for your Second Brain installation.

## Prerequisites

Before you begin, ensure you have:

- **Second Brain installed:** `uv tool install second-brain` or `uv pip install -e .` for development
- **Git repository initialized:** Your `~/.second-brain/` directory should be a git repository
- **Command line access:** You'll need terminal access to run `sb` commands

## Installation Steps

### Step 1: Generate Encryption Keys

The first step is to generate your RSA key pair for encrypting sensitive data.

```bash
sb key generate
```

**What this does:**
- Generates a 4096-bit RSA key pair
- Saves keys to `~/.second-brain/keys/`
  - `private_key.pem` (600 permissions - owner only)
  - `public_key.pem` (644 permissions - readable by all)
  - `.key_metadata.json` (key fingerprint and creation date)
- Automatically adds `keys/` to `.gitignore` to prevent accidental commits

**Expected output:**
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

**Verify key generation:**

```bash
sb key info
```

This shows your key details:
```
Key pair found: Yes
Private key: /Users/username/.second-brain/keys/private_key.pem
Public key:  /Users/username/.second-brain/keys/public_key.pem
Fingerprint: sha256:abc123...xyz789
Created: 2025-11-24 10:30:00
```

### Step 2: Install Git Pre-commit Hook

The pre-commit hook validates that no unencrypted sensitive data is committed to your repository.

```bash
sb install-hooks
```

**What this does:**
- Creates `.git/hooks/pre-commit` in `~/.second-brain/`
- Configures hook to use the correct Python interpreter
- Makes hook executable (755 permissions)
- Hook will run automatically before every `git commit`

**Expected output:**
```
✅ Pre-commit hook installed successfully!

📁 Hook location: /Users/username/.second-brain/.git/hooks/pre-commit

The hook will now validate commits to prevent accidental exposure of sensitive data.

To check hook status: sb install-hooks --check
To reinstall: sb install-hooks --force
```

**Verify installation:**

```bash
sb install-hooks --check
```

**Expected output:**
```
✅ Pre-commit hook is installed
   Location: /Users/username/.second-brain/.git/hooks/pre-commit
   Executable: Yes
   Valid: Yes
```

### Step 3: Test the Setup

It's important to verify that the protection system is working correctly.

#### Test 1: Verify Keys Work

```bash
# Encrypt a test string
echo "Secret data" | sb encrypt

# You should see encrypted output like:
# v1:RSA-AES256-GCM:abc123...:def456...:ghi789...
```

#### Test 2: Verify Hook Blocks Sensitive Data

```bash
cd ~/.second-brain

# Create a test file with fake sensitive data
echo "api_key = sk_test_fake123" > data/notes/test-hook.md

# Try to commit it
git add data/notes/test-hook.md
git commit -m "test commit"
```

**Expected result:** Commit should be BLOCKED with error message:

```
❌ Commit blocked: Sensitive data validation failed

  ❌ data/notes/test-hook.md:1
     Unencrypted sensitive data detected: api_key = "sk_test_fake123"
     💡 Encrypt this content or remove the sensitive data

💡 To bypass this check (NOT recommended):
   git commit --no-verify
```

**Clean up test:**
```bash
rm data/notes/test-hook.md
git reset
```

#### Test 3: Verify Encrypted Content is Allowed

```bash
# Create a note
sb note create "Test Note" --project test

# Mark it as sensitive (encrypts content)
sb mark-sensitive --note-id <note-id>

# Commit the encrypted note
cd ~/.second-brain
git add data/notes/note-<id>.md
git commit -m "Add encrypted note"
```

**Expected result:** Commit should succeed with no errors.

### Step 4: Backup Your Private Key

**CRITICAL:** Your private key is the only way to decrypt your sensitive data.

```bash
# Option 1: Copy to secure location
cp ~/.second-brain/keys/private_key.pem /path/to/secure/backup/

# Option 2: Export to password manager
cat ~/.second-brain/keys/private_key.pem
# Copy output and save in password manager

# Option 3: Create encrypted backup
gpg -c ~/.second-brain/keys/private_key.pem
# Save private_key.pem.gpg somewhere safe
```

**Important notes:**
- Never commit your private key to git
- Keep multiple backups in different locations
- Consider printing a paper backup for ultimate resilience
- Test your backup by restoring it on another machine

## Troubleshooting Installation Issues

### Issue: "sb: command not found"

**Solution:** Second Brain is not in your PATH

```bash
# If installed with uv tool:
uv tool install second-brain

# Add to PATH (add to ~/.bashrc or ~/.zshrc):
export PATH="$HOME/.local/bin:$PATH"

# Reload shell
source ~/.bashrc  # or source ~/.zshrc
```

### Issue: Keys already exist

**Symptom:** `sb key generate` says keys already exist

**Solution:** This is safe! Your existing keys are protected. If you want to regenerate:

```bash
# Backup existing keys first!
cp -r ~/.second-brain/keys ~/.second-brain/keys.backup

# Remove old keys
rm -rf ~/.second-brain/keys

# Generate new keys
sb key generate

# Important: You cannot decrypt old data with new keys!
```

### Issue: Hook not blocking commits

**Symptom:** Commits succeed even with sensitive data

**Check 1:** Verify hook is installed

```bash
sb install-hooks --check
```

**Check 2:** Verify hook is executable

```bash
ls -l ~/.second-brain/.git/hooks/pre-commit
# Should show: -rwxr-xr-x (executable)
```

**Check 3:** Reinstall hook

```bash
sb install-hooks --force
```

**Check 4:** Test hook directly

```bash
cd ~/.second-brain
echo "password = test123" > test.md
git add test.md
git commit -m "test"
# Should block with error

# Clean up
rm test.md
git reset
```

### Issue: Permission denied on private key

**Symptom:** Cannot read private key file

**Solution:** Fix permissions

```bash
chmod 600 ~/.second-brain/keys/private_key.pem
```

### Issue: Hook fails with Python import error

**Symptom:** Hook output shows "No module named 'second_brain'"

**Solution:** Reinstall hook (it will use correct Python path)

```bash
sb install-hooks --force
```

## Verifying Complete Installation

Run this checklist to ensure everything is set up correctly:

```bash
# 1. Check keys exist
sb key info
# Expected: Shows key information

# 2. Check hook is installed
sb install-hooks --check
# Expected: ✅ Pre-commit hook is installed

# 3. Test encryption
echo "test" | sb encrypt
# Expected: v1:RSA-AES256-GCM:...

# 4. Test decryption
ENCRYPTED=$(echo "test" | sb encrypt)
echo "$ENCRYPTED" | sb decrypt
# Expected: test

# 5. Test hook blocking (should FAIL - this is good!)
cd ~/.second-brain
echo "api_key = sk_test_fake" > test.md
git add test.md
git commit -m "test" 2>&1 | grep "Commit blocked"
# Expected: Output contains "Commit blocked"
rm test.md
git reset
```

If all 5 tests pass, your installation is complete and working correctly!

## Next Steps

Now that encryption is set up, you can:

1. **Read the [Pre-commit Hook Guide](./precommit-hook.md)** - Learn how the hook works
2. **Review [CLI Reference](./cli-reference.md)** - Learn all encryption commands
3. **Check [Best Practices](./best-practices.md)** - Security recommendations
4. **Start using encryption:**
   ```bash
   # Create a note
   sb note create "Passwords" --project security

   # Add sensitive content to the note
   # (edit the markdown file in ~/.second-brain/data/notes/)

   # Mark it as sensitive
   sb mark-sensitive --note-id <id>

   # Commit safely
   cd ~/.second-brain
   git add data/notes/note-<id>.md
   git commit -m "Add encrypted passwords"
   git push
   ```

## Uninstalling

If you need to remove the encryption system:

```bash
# Remove pre-commit hook
rm ~/.second-brain/.git/hooks/pre-commit

# Remove keys (WARNING: You cannot decrypt data after this!)
# Backup first if you have encrypted data!
cp -r ~/.second-brain/keys ~/keys-backup
rm -rf ~/.second-brain/keys
```

**Warning:** If you have encrypted notes or logs, you will not be able to decrypt them after removing your private key. Always backup first!

## Getting Help

- **Documentation:** [Encryption README](./README.md)
- **Troubleshooting:** [Common Issues](./troubleshooting.md)
- **CLI Help:** Run `sb --help` or `sb <command> --help`
- **Report Issues:** [GitHub Issues](https://github.com/seanm/second-brain/issues)
