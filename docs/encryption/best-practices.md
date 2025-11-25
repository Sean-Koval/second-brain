# Best Practices - Encryption & Security

Security recommendations and best practices for using Second Brain's encryption system.

## Table of Contents

- [Key Management](#key-management)
- [Encryption Practices](#encryption-practices)
- [Git and Version Control](#git-and-version-control)
- [Workflow Recommendations](#workflow-recommendations)
- [Security Hardening](#security-hardening)
- [Team Collaboration](#team-collaboration)

---

## Key Management

### Generate Keys Immediately

**✅ DO:**
```bash
# Generate keys as first step after installing Second Brain
sb init
sb key generate
sb install-hooks
```

**❌ DON'T:**
- Wait until you have sensitive data to generate keys
- Create notes with sensitive data before encryption is set up
- Skip key generation "for later"

**Why:** Pre-commit hook can only protect you if keys and hooks are installed. Generate keys proactively.

---

### Backup Private Key Multiple Times

**✅ DO: Create Multiple Backups**

**Backup 1: Secure local location**
```bash
# External drive
cp ~/.second-brain/keys/private_key.pem /Volumes/ExternalDrive/backups/second-brain-key.pem

# Or USB drive
cp ~/.second-brain/keys/private_key.pem /media/usb/backups/
```

**Backup 2: Cloud storage (encrypted)**
```bash
# Encrypt with GPG before uploading
gpg -c ~/.second-brain/keys/private_key.pem
# Creates private_key.pem.gpg

# Upload encrypted file to Dropbox/iCloud/etc
cp ~/.second-brain/keys/private_key.pem.gpg ~/Dropbox/backups/
```

**Backup 3: Password manager**
```bash
# Copy key content
cat ~/.second-brain/keys/private_key.pem | pbcopy  # macOS
cat ~/.second-brain/keys/private_key.pem | xclip  # Linux

# Paste into password manager as secure note
# 1Password, LastPass, Bitwarden, etc.
```

**Backup 4: Paper backup (optional but ultimate resilience)**
```bash
# Print to paper and store in safe
cat ~/.second-brain/keys/private_key.pem | lpr

# Or print to PDF
cat ~/.second-brain/keys/private_key.pem | ps2pdf - > private-key-backup.pdf
```

**❌ DON'T:**
- Keep only one copy of your private key
- Store backup in same location as original
- Upload unencrypted key to cloud storage
- Email key to yourself
- Store key in plain text in notes app

**Why:** If you lose your private key, all encrypted data is permanently unrecoverable. No backdoor exists.

---

### Verify Backups Regularly

**✅ DO:**
```bash
# Monthly verification
# 1. Restore key from backup to temp location
cp ~/backup/private_key.pem /tmp/test-key.pem

# 2. Test decryption with backup key
# (requires temporarily swapping keys or using custom key path - future feature)

# 3. Verify fingerprint matches
sha256sum /tmp/test-key.pem
sha256sum ~/.second-brain/keys/private_key.pem
# Should be identical

# 4. Clean up
rm /tmp/test-key.pem
```

**❌ DON'T:**
- Assume backups are valid without testing
- Wait until disaster to discover backup is corrupted

**Why:** Backups are only useful if they actually work. Regular verification prevents nasty surprises.

---

### Protect Private Key File

**✅ DO:**
```bash
# Ensure correct permissions (owner-only read/write)
chmod 600 ~/.second-brain/keys/private_key.pem

# Verify
ls -l ~/.second-brain/keys/private_key.pem
# Should show: -rw------- (600)
```

**❌ DON'T:**
```bash
# Never make private key world-readable
chmod 644 ~/.second-brain/keys/private_key.pem  # INSECURE!
chmod 777 ~/.second-brain/keys/private_key.pem  # VERY INSECURE!
```

**Why:** Private key should only be readable by you. Other users on the system shouldn't access it.

---

### Use Key Fingerprints for Verification

**✅ DO:**
```bash
# Record key fingerprint in safe location
sb key info | grep Fingerprint > ~/key-fingerprint.txt

# Store in password manager
# Compare fingerprints when restoring from backup
```

**Why:** Fingerprints help verify you're using the correct key without exposing the key itself.

---

## Encryption Practices

### Encrypt Before Committing

**✅ DO:**
```bash
# Create note
sb note create "API Keys" --project security

# Add sensitive content
# (edit file)

# Encrypt BEFORE git commit
sb mark-sensitive --note-id 5

# Then commit
cd ~/.second-brain
git add data/notes/note-5.md
git commit -m "Add encrypted API keys"
```

**❌ DON'T:**
```bash
# Create note with sensitive data
echo "api_key = sk_live_..." > ~/.second-brain/data/notes/note-5.md

# Commit without encrypting
git commit -am "Add API keys"  # ❌ Hook will block, but bad workflow
```

**Why:** Encrypt proactively. Don't rely solely on hook to catch mistakes.

---

### Encrypt Entire Notes, Not Individual Fields

**✅ DO:**
```markdown
<!-- Encrypt entire note -->
---
id: 5
title: Production Credentials
encrypted: true
---

<!-- ENCRYPTED:v1:RSA-AES256-GCM -->
v1:RSA-AES256-GCM:...
<!-- END ENCRYPTED -->
```

**❌ DON'T:**
```markdown
<!-- Don't mix encrypted and plain text -->
---
id: 5
title: Production Credentials
---

API Key: <!-- ENCRYPTED -->...<!-- END ENCRYPTED -->
Password: mypassword123  # ❌ Unencrypted!
```

**Why:**
- Cleaner, less error-prone
- All-or-nothing encryption reduces mistakes
- Easier to audit (either encrypted or not)

---

### Use Descriptive Titles for Encrypted Notes

**✅ DO:**
```markdown
---
title: AWS Production Credentials
encrypted: true
---
```

**❌ DON'T:**
```markdown
---
title: Secret Stuff
encrypted: true
---
```

**Why:** You still want to know what the encrypted note contains without decrypting it. Titles are not encrypted.

---

### Encrypt Before Syncing to Cloud

**✅ DO:**
```bash
# Workflow: Edit → Encrypt → Commit → Push
sb note create "Secrets"
# Edit note
sb mark-sensitive --note-id 5
cd ~/.second-brain
git add .
git commit -m "Add encrypted secrets"
git push  # Safe: content is encrypted
```

**❌ DON'T:**
```bash
# Don't push unencrypted sensitive data
cd ~/.second-brain
git commit -am "Add secrets"  # Might forget to encrypt!
git push  # ❌ Unencrypted data now on GitHub
```

**Why:** Once pushed to GitHub (even private repo), data is harder to fully remove from history.

---

## Git and Version Control

### Always Use Pre-commit Hook

**✅ DO:**
```bash
# Install hook immediately
sb install-hooks

# Verify it's working
sb install-hooks --check
```

**❌ DON'T:**
```bash
# Don't bypass hook without good reason
git commit --no-verify -m "quick fix"  # Dangerous!
```

**Why:** Hook is your last line of defense. Bypassing it defeats the purpose.

---

### Review Hook Warnings

**✅ DO:**
When you see warnings:
```
⚠️  Warnings detected:
  ⚠️  data/notes/note-7.md:1
     Possible sensitive content marker: TODO: encrypt this
```

**Action:**
```bash
# Stop and review
cat ~/.second-brain/data/notes/note-7.md

# Encrypt if needed
sb mark-sensitive --note-id 7

# Or remove TODO if not needed
```

**❌ DON'T:**
- Ignore warnings
- Assume warnings are always false positives

**Why:** Warnings indicate potential issues. Review them before committing.

---

### Never Push Keys to Git

**✅ DO:**
```bash
# Verify .gitignore includes keys/
grep "keys/" ~/.second-brain/.gitignore

# Check nothing from keys/ is tracked
cd ~/.second-brain
git ls-files | grep keys/
# Should return empty
```

**❌ DON'T:**
```bash
# Never force-add keys
git add -f ~/.second-brain/keys/private_key.pem  # NEVER DO THIS!
```

**Why:** Private keys in git history = game over. Even if you delete the commit, it's in history forever.

---

### Review Commits Before Pushing

**✅ DO:**
```bash
# Before git push, review what you're pushing
git log origin/main..HEAD --oneline

# Check diffs
git diff origin/main..HEAD

# Look for any sensitive data
git diff origin/main..HEAD | grep -i "password\|api_key\|secret"
```

**❌ DON'T:**
```bash
# Don't blind push
git push  # Without reviewing
```

**Why:** Last chance to catch issues before data goes to cloud.

---

## Workflow Recommendations

### Daily Workflow

**✅ Recommended Daily Workflow:**

```bash
# Morning: Start work
sb note create "Work Log - Nov 24" --project daily

# During day: Add content
# (edit notes, add tasks, etc.)

# End of day: Review and encrypt
sb note list --today
# For each sensitive note:
sb mark-sensitive --note-id <id>

# Commit and push
cd ~/.second-brain
git add .
git status  # Review changes
git commit -m "Daily notes for Nov 24"
git push
```

---

### Project Workflow

**✅ Recommended Project Workflow:**

```bash
# Start new project
sb note create "Project Alpha - Credentials" --project alpha
sb note create "Project Alpha - Notes" --project alpha

# Mark credentials note as sensitive immediately
sb mark-sensitive --note-id <credentials-id>

# Work on project
# (add notes, logs, etc.)

# End of project: Review all notes
sb note list --project alpha
# Encrypt any that became sensitive during project
```

---

### Credential Management Workflow

**✅ Recommended for Managing Credentials:**

```bash
# Create dedicated credential notes per service
sb note create "AWS Credentials" --project infra
sb note create "GitHub Tokens" --project infra
sb note create "Database Passwords" --project infra

# Encrypt immediately
sb mark-sensitive --note-id <aws-id>
sb mark-sensitive --note-id <github-id>
sb mark-sensitive --note-id <db-id>

# To access:
grep "v1:RSA-AES256-GCM" ~/.second-brain/data/notes/note-<id>.md | sb decrypt
```

**Why:** Dedicated notes per service make it easier to manage and rotate credentials.

---

## Security Hardening

### Use Full Disk Encryption

**✅ DO:**
- Enable FileVault (macOS)
- Enable BitLocker (Windows)
- Enable LUKS (Linux)

**Why:** Encrypting individual notes doesn't help if someone steals your laptop and reads the keys from disk. Full disk encryption protects the keys themselves.

---

### Secure Your Shell History

**✅ DO:**
```bash
# Don't put secrets in commands
sb encrypt "my secret"  # ❌ Secret in shell history!

# Instead, use stdin
echo "my secret" | sb encrypt  # Better, but still in history

# Best: use file or editor
vim secret.txt  # Enter secret here
cat secret.txt | sb encrypt
rm secret.txt

# Or disable history for sensitive commands
set +o history
sb encrypt "secret"
set -o history
```

**❌ DON'T:**
```bash
# Don't pass secrets as CLI arguments
sb encrypt "api_key=sk_live_abc123..."  # ❌ In shell history!
```

**Why:** Shell history is often unencrypted and readable. Sensitive data in commands = exposure risk.

---

### Limit Key Access

**✅ DO:**
```bash
# Restrict key directory
chmod 700 ~/.second-brain/keys

# Restrict private key
chmod 600 ~/.second-brain/keys/private_key.pem

# Verify no other users can access
ls -la ~/.second-brain/keys/
```

**❌ DON'T:**
```bash
# Don't make keys readable by group/others
chmod 755 ~/.second-brain/keys  # ❌ Allows others to read
```

**Why:** Defense in depth. Even on single-user machines, proper permissions are good practice.

---

### Use Screen Lock

**✅ DO:**
- Lock screen when away from computer
- Enable auto-lock after 5-10 minutes
- Use strong login password

**Why:** Encrypted data doesn't help if someone has physical access to your logged-in session.

---

### Rotate Credentials Regularly

**✅ DO:**
```bash
# Every 90 days:
# 1. Update credentials in encrypted notes
# 2. Rotate API keys, passwords, tokens
# 3. Re-encrypt notes with updated content

# Track rotation dates
sb note create "Credential Rotation Log" --project security
# Document when each credential was last rotated
```

**Why:** Even encrypted credentials should be rotated periodically for defense in depth.

---

## Team Collaboration

### Individual Keys Per Person

**✅ DO:**
- Each team member generates their own key pair
- Each person encrypts their own sensitive notes
- Don't share private keys

**❌ DON'T:**
- Share private keys between team members
- Email private keys
- Use single shared key for team

**Why:** If one person's key is compromised, only their data is affected. Shared keys = shared risk.

---

### Use Shared Secret Management for Team Secrets

**✅ DO:**
For secrets that need to be shared across team:
- Use proper secret management tools (HashiCorp Vault, AWS Secrets Manager)
- Use shared password managers (1Password Teams, LastPass Enterprise)
- Document secret locations in encrypted Second Brain notes

**❌ DON'T:**
- Store team secrets in individual Second Brain instances
- Try to share encrypted notes between team members (different keys!)

**Why:** Second Brain is for personal knowledge management. Teams need proper shared secret infrastructure.

---

### Document Team Processes

**✅ DO:**
```bash
# Create process documentation
sb note create "Team Secret Management Process" --project team

# Document:
# - Where team secrets are stored (Vault, password manager)
# - How to request access
# - Rotation schedules
# - Incident response procedures

# Keep process docs unencrypted (not secret themselves)
```

**Why:** Team needs to access process docs even if individual secrets are encrypted/protected.

---

## Checklist: Security Audit

Perform this audit monthly:

### Key Security
- [ ] Private key backed up in 3+ locations
- [ ] Backup restoration tested in last 30 days
- [ ] Private key permissions are 600
- [ ] Key directory permissions are 700
- [ ] No keys tracked in git (`git ls-files | grep keys/` returns empty)

### Hook Security
- [ ] Pre-commit hook installed (`sb install-hooks --check`)
- [ ] Hook is executable
- [ ] Hook blocking tested in last 30 days
- [ ] No commits made with `--no-verify` flag

### Encryption Status
- [ ] All sensitive notes encrypted
- [ ] No unencrypted credentials in notes
- [ ] Encrypted note titles are descriptive
- [ ] No sensitive data in commit messages

### System Security
- [ ] Full disk encryption enabled
- [ ] Screen lock enabled (auto-lock < 10 min)
- [ ] Strong login password
- [ ] Shell history reviewed for secrets

### Backup Status
- [ ] Git repository backed up
- [ ] Private keys backed up
- [ ] Encrypted notes synced to GitHub
- [ ] Local backups up to date

### Operational Security
- [ ] Credentials rotated in last 90 days
- [ ] Access logs reviewed (if applicable)
- [ ] No suspicious git activity
- [ ] Team members' access reviewed

---

## Common Mistakes to Avoid

### ❌ Mistake 1: Forgetting to Install Hook
**Problem:** Create encrypted notes but forget to install pre-commit hook.

**Result:** Hook doesn't protect you. Might commit unencrypted data without realizing.

**Solution:** Install hook as part of initial setup. Make it automatic.

### ❌ Mistake 2: Encrypting After Committing
**Problem:** Commit sensitive data, then encrypt it in a second commit.

**Result:** Sensitive data is in git history forever, even if encrypted later.

**Solution:** Always encrypt BEFORE committing.

### ❌ Mistake 3: Only One Key Backup
**Problem:** Keep only one backup of private key.

**Result:** If backup drive fails, all encrypted data is lost.

**Solution:** Multiple backups in different locations.

### ❌ Mistake 4: Treating Encrypted Data as Public
**Problem:** Assume "it's encrypted, so it's safe to share anywhere."

**Result:** If encryption is broken in future, data is exposed.

**Solution:** Defense in depth. Encrypt + access control + secure transport.

### ❌ Mistake 5: Weak System Security
**Problem:** Strong encryption, but weak laptop password and no full disk encryption.

**Result:** Attacker steals laptop, boots into recovery mode, reads keys directly from disk.

**Solution:** Full disk encryption + strong passwords + screen lock.

### ❌ Mistake 6: Bypassing Hook Frequently
**Problem:** Use `git commit --no-verify` regularly "to save time."

**Result:** Eventually commit actual sensitive data without noticing.

**Solution:** Almost never bypass hook. If hook is too restrictive, improve patterns instead.

### ❌ Mistake 7: Sharing Private Keys
**Problem:** Send private key to teammate so they can decrypt your notes.

**Result:** Now two people have your key. If their system is compromised, your data is too.

**Solution:** Never share private keys. Use proper shared secret management for team secrets.

---

## Security Philosophy

### Defense in Depth

Don't rely on any single security measure:

**Layer 1: Encryption**
- Strong encryption (RSA-4096 + AES-256-GCM)

**Layer 2: Access Control**
- File permissions (600 on private key)
- User authentication

**Layer 3: System Security**
- Full disk encryption
- Screen lock
- Strong passwords

**Layer 4: Operational Security**
- Pre-commit hooks
- Code review
- Audit logs

**Layer 5: Backup & Recovery**
- Multiple key backups
- Tested recovery procedures
- Disaster recovery plan

**Why:** If one layer fails, others still protect you.

---

### Assume Breach

Plan for the worst:

**Assume:**
- GitHub might be breached
- Your laptop might be stolen
- Backup might be discovered
- Encryption might be broken in future

**Therefore:**
- Don't store ultra-sensitive data even encrypted
- Rotate credentials regularly
- Monitor access
- Have incident response plan

**Why:** Security is not about preventing all attacks, it's about minimizing damage when attacks succeed.

---

### Minimize Sensitive Data

**✅ Best practice:**
```bash
# Don't store if you don't need to
# Option 1: Don't store long-term
echo "API Key: sk_live_123" | sb encrypt  # Encrypt
# Copy output and use immediately
# Don't save to note

# Option 2: Reference instead of storing
sb note create "AWS Access" --project infra
# Content: "AWS credentials stored in 1Password vault 'Infrastructure'"
# Not: actual credentials
```

**Why:** The most secure data is data you don't have. Store references, not secrets when possible.

---

## Related Documentation

- **[Installation Guide](./installation.md)** - Set up encryption
- **[CLI Reference](./cli-reference.md)** - Command documentation
- **[Pre-commit Hook Guide](./precommit-hook.md)** - Hook behavior
- **[Troubleshooting](./troubleshooting.md)** - Fix issues

---

## Security Resources

### Learn More

- **[OWASP Cryptographic Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html)**
- **[NIST Cryptographic Standards](https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines)**
- **[EFF Surveillance Self-Defense](https://ssd.eff.org/)**

### Report Security Issues

**Found a security vulnerability?**
- Email: security@example.com (private disclosure)
- GitHub Security Advisory (private)
- DO NOT open public issues for security vulnerabilities

**Response time:**
- Acknowledgment: 24-48 hours
- Fix timeline: Based on severity
- Credit: Public thanks after fix (if desired)
