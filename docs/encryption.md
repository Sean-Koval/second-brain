# Encryption Guide

Second Brain supports encryption for sensitive data, allowing you to safely sync your knowledge base to a private GitHub repository without exposing secrets.

---

## Overview

Second Brain uses **hybrid encryption** (RSA + AES-256-GCM) to protect sensitive content:

- **RSA-4096**: Asymmetric encryption for key exchange
- **AES-256-GCM**: Symmetric encryption for data (fast, authenticated)

This approach ensures:
- Strong encryption for any content size
- Authentication to detect tampering
- Forward secrecy per encrypted block

---

## Quick Start

### 1. Generate Encryption Keys

```bash
# Generate a 4096-bit RSA key pair
sb key generate

# Or with passphrase protection (recommended)
sb key generate --passphrase
```

### 2. Encrypt Sensitive Content

```bash
# Encrypt text directly
sb encrypt "my-api-key-12345"

# Encrypt as markdown block
sb encrypt "secret data" --block

# Mark a note as sensitive and encrypt
sb note mark-sensitive 42 --encrypt
```

### 3. Decrypt Content

```bash
# Decrypt text
sb decrypt "v1:RSA-AES256-GCM:..."

# Decrypt from file
sb decrypt --file encrypted.txt

# Decrypt a note
sb note decrypt 42
```

### 4. Install Pre-Commit Hook (Recommended)

```bash
# Install hook to prevent accidental commits of sensitive data
sb hook install

# Check hook status
sb hook status
```

---

## Key Management

### Key Storage

Keys are stored in `~/.second-brain/keys/`:

```
~/.second-brain/keys/
├── private_key.pem    # Private key (600 permissions)
├── public_key.pem     # Public key (644 permissions)
└── .key_metadata.json # Key metadata
```

### Key Information

```bash
sb key info
```

Output:
```
Encryption Keys

Algorithm:   RSA-4096
Fingerprint: SHA256:abc123...
Created:     2025-01-15 10:30:00 EST
Passphrase:  Yes

Location:    /home/user/.second-brain/keys

Private key: ✓ Found (permissions: 600)
Public key:  ✓ Found (permissions: 644)
```

### Passphrase Protection

We recommend protecting your private key with a passphrase:

```bash
# Generate with passphrase
sb key generate --passphrase

# When decrypting, you'll be prompted for the passphrase
sb decrypt --passphrase "v1:RSA-AES256-GCM:..."
```

**Benefits:**
- Even if someone accesses your key file, they can't use it without the passphrase
- Adds a second factor of protection

**Trade-offs:**
- You must enter the passphrase for decryption operations
- If you forget the passphrase, you cannot decrypt your data

### Exporting Keys

For backup purposes, you can export your keys:

```bash
# Export public key (safe to share)
sb key export --public my-public-key.pem

# Export private key (with security warnings)
sb key export --private my-private-key.pem

# Export in SSH format
sb key export --public --format ssh
```

**Private Key Export Warning:**
- Only export to encrypted storage (encrypted drive, password manager)
- Never commit private keys to version control
- Delete exports after transferring to secure storage

---

## Encrypting Notes

### Mark Notes as Sensitive

```bash
# Mark a note as sensitive (enables encryption flag in database)
sb note mark-sensitive 42

# Mark and encrypt immediately
sb note mark-sensitive 42 --encrypt

# Remove sensitive marking
sb note mark-sensitive 42 --unmark
```

### How Note Encryption Works

When you encrypt a note:

1. The note content is wrapped in an encrypted block:
   ```markdown
   <!-- ENCRYPTED:v1:RSA-AES256-GCM -->
   v1:RSA-AES256-GCM:encrypted_key:nonce:ciphertext
   <!-- END ENCRYPTED -->
   ```

2. The database is updated:
   - `is_sensitive = True`
   - `encrypted = True`

3. The markdown file is updated with encrypted content

### Viewing Encrypted Notes

```bash
# Show note (will display encrypted block)
sb note show 42

# To view decrypted content
sb note decrypt 42
```

---

## Pre-Commit Hook

The pre-commit hook prevents accidentally committing sensitive data.

### Installation

```bash
# Install to current repository
sb hook install

# Install to specific repository
sb hook install --path /path/to/repo

# Force overwrite existing hook
sb hook install --force
```

### What It Checks

The hook scans staged files for:

| Pattern Type | Examples |
|--------------|----------|
| API Keys | `api_key=abc123`, `apiKey: "xyz"` |
| Secrets | `password=`, `secret_token=` |
| AWS Credentials | `AKIA...`, `aws_secret_access_key` |
| Private Keys | `-----BEGIN PRIVATE KEY-----` |
| Connection Strings | `mongodb://user:pass@host` |
| Bearer Tokens | `Bearer eyJ...` |

### Manual Check

Run the check without committing:

```bash
# Quick check
sb hook check

# Verbose output
sb hook check -v
```

### Bypassing the Hook

If you need to commit despite warnings:

```bash
git commit --no-verify -m "message"
```

**Use with caution!** Only bypass when you're certain the flagged content is safe.

### Uninstalling

```bash
sb hook uninstall
```

---

## Encryption Format

Second Brain uses a versioned, self-describing format:

```
v1:RSA-AES256-GCM:encrypted_key:nonce:ciphertext
```

| Component | Description |
|-----------|-------------|
| `v1` | Format version |
| `RSA-AES256-GCM` | Algorithm identifier |
| `encrypted_key` | AES key encrypted with RSA (base64) |
| `nonce` | Random nonce for AES-GCM (base64) |
| `ciphertext` | Encrypted data with auth tag (base64) |

### Markdown Blocks

For embedding in markdown files:

```markdown
<!-- ENCRYPTED:v1:RSA-AES256-GCM -->
v1:RSA-AES256-GCM:AAA...base64...
<!-- END ENCRYPTED -->
```

---

## Best Practices

### Do's

- **Use passphrase protection** for your private key
- **Backup your keys** to secure, encrypted storage
- **Install the pre-commit hook** in all repositories with Second Brain data
- **Use `mark-sensitive`** to flag notes containing secrets
- **Regularly check** for unencrypted sensitive data: `sb hook check`

### Don'ts

- **Never commit** private keys to version control
- **Don't share** private keys via email or chat
- **Don't store** unencrypted API keys in notes
- **Don't disable** the pre-commit hook without good reason

### Key Backup Strategy

1. **Primary storage**: `~/.second-brain/keys/`
2. **Backup 1**: Encrypted USB drive stored securely
3. **Backup 2**: Password manager (e.g., 1Password, Bitwarden)
4. **Document**: Store passphrase separately from key backup

---

## Recovery Procedures

### Lost Passphrase

If you forget your key passphrase:

1. **If you have unencrypted backups**: Restore from backup
2. **If all backups are encrypted**: Data cannot be recovered
   - Generate new keys: `sb key generate --force`
   - Re-encrypt sensitive notes with new keys
   - Previous encrypted data is lost

### Corrupted Keys

If key files are corrupted:

1. Check for backups in secure storage
2. Restore `private_key.pem` and `public_key.pem` to `~/.second-brain/keys/`
3. Verify: `sb key info`

### Key Rotation

To rotate to new keys:

1. **Decrypt all content** with old keys
2. **Backup old keys** to secure storage
3. **Generate new keys**: `sb key generate --force`
4. **Re-encrypt content** with new keys
5. **Verify** decryption works with new keys
6. **Delete old key backups** after confirming

---

## Troubleshooting

### "No encryption keys found"

```bash
# Generate keys
sb key generate
```

### "Decryption failed"

Possible causes:
- Wrong passphrase
- Content encrypted with different key
- Corrupted encrypted data

Solutions:
```bash
# Check key info
sb key info

# Try with explicit passphrase
sb decrypt --passphrase "encrypted_text"
```

### "Private key permissions too open"

Private key must have restricted permissions:

```bash
chmod 600 ~/.second-brain/keys/private_key.pem
```

### Pre-commit hook false positives

If the hook flags safe content:

1. Check if it's actually safe
2. If safe, add to `.gitignore` or modify the pattern
3. Bypass with `--no-verify` for one commit

---

## CLI Reference

### Key Commands

| Command | Description |
|---------|-------------|
| `sb key generate` | Generate new RSA key pair |
| `sb key info` | Show key information |
| `sb key export` | Export keys to files |

### Encryption Commands

| Command | Description |
|---------|-------------|
| `sb encrypt <text>` | Encrypt text |
| `sb decrypt <text>` | Decrypt text |
| `sb note mark-sensitive <id>` | Mark note as sensitive |
| `sb note decrypt <id>` | Decrypt a note |

### Hook Commands

| Command | Description |
|---------|-------------|
| `sb hook install` | Install pre-commit hook |
| `sb hook uninstall` | Remove pre-commit hook |
| `sb hook check` | Run encryption check |
| `sb hook status` | Check hook installation |

---

## Security Considerations

### Threat Model

Second Brain encryption protects against:
- **Repository exposure**: If your private repo is leaked, encrypted content remains protected
- **Stolen laptop**: Passphrase-protected keys require the passphrase to use
- **Accidental commits**: Pre-commit hook catches sensitive data before it's committed

It does **not** protect against:
- **Compromised system**: If your machine is compromised, keys may be accessible
- **Key theft + passphrase**: If both are obtained, data can be decrypted
- **Memory attacks**: Content is decrypted in memory during use

### Recommendations

1. Use full-disk encryption on your machine
2. Use a strong, unique passphrase for keys
3. Keep your system and Second Brain updated
4. Review the pre-commit hook logs regularly

---

## Technical Details

### Algorithm Details

- **RSA**: 4096-bit key, OAEP padding with SHA-256
- **AES**: 256-bit key, GCM mode with 96-bit nonce
- **Key derivation**: Random 256-bit AES key per encryption

### Dependencies

- `cryptography` library (Python)
- No external key management services required

### Performance

- Key generation: ~2 seconds (one-time)
- Encryption: ~1ms for 1KB of data
- Decryption: ~1ms for 1KB of data

Large files are encrypted efficiently using AES streaming.

---

## Next Steps

- [Quick Start Guide](quickstart.md) - Get started with Second Brain
- [CLI Reference](cli-reference.md) - Full command documentation
- [Workflows](workflows.md) - Common usage patterns
