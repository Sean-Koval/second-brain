"""Sensitive data pattern definitions.

Defines patterns for detecting potentially sensitive information that should be encrypted.
"""

# High-confidence sensitive data patterns (will block commits)
# These patterns are strong indicators of sensitive data
HIGH_CONFIDENCE_PATTERNS = [
    # Private keys
    r'-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----',

    # API keys (various formats)
    r'api[_-]?key\s*[=:]\s*["\']?[a-zA-Z0-9_\-]{20,}',
    r'apikey\s*[=:]\s*["\']?[a-zA-Z0-9_\-]{20,}',

    # Passwords
    r'password\s*[=:]\s*["\']?[^"\'\s]{8,}["\']?',
    r'passwd\s*[=:]\s*["\']?[^"\'\s]{8,}["\']?',

    # Secret keys
    r'secret[_-]?key\s*[=:]\s*["\']?[a-zA-Z0-9_\-]{20,}',
    r'secretkey\s*[=:]\s*["\']?[a-zA-Z0-9_\-]{20,}',

    # AWS credentials
    r'aws[_-]?secret[_-]?access[_-]?key\s*[=:]\s*["\']?[a-zA-Z0-9/+=]{40}["\']?',
    r'aws[_-]?access[_-]?key[_-]?id\s*[=:]\s*["\']?AKIA[a-zA-Z0-9]{16}["\']?',

    # Private key IDs
    r'private[_-]?key[_-]?id\s*[=:]\s*["\']?[a-zA-Z0-9_\-]{20,}',

    # Tokens (various types)
    r'token\s*[=:]\s*["\']?[a-zA-Z0-9_\-]{20,}',
    r'access[_-]?token\s*[=:]\s*["\']?[a-zA-Z0-9_\-]{20,}',
    r'auth[_-]?token\s*[=:]\s*["\']?[a-zA-Z0-9_\-]{20,}',

    # Client secrets
    r'client[_-]?secret\s*[=:]\s*["\']?[a-zA-Z0-9_\-]{20,}',

    # GitHub tokens
    r'gh[pous]_[a-zA-Z0-9]{36,}',

    # Slack tokens
    r'xox[baprs]-[a-zA-Z0-9-]{10,}',

    # Generic secret patterns
    r'["\']secret["\']\s*:\s*["\'][^"\']{8,}["\']',
    r'["\']key["\']\s*:\s*["\'][a-zA-Z0-9_\-]{20,}["\']',
]

# Medium-confidence patterns (will warn but not block)
# These are markers or indicators that should be reviewed
MEDIUM_CONFIDENCE_PATTERNS = [
    # Custom sensitive markers
    r'SENSITIVE:',
    r'@sensitive',
    r'\[SENSITIVE\]',

    # TODO markers about encryption
    r'TODO:.*encrypt',
    r'FIXME:.*encrypt',
    r'XXX.*sensitive',
    r'NOTE:.*sensitive',

    # Credential-related terms (may be false positives)
    r'\bcredentials?\b',
    r'\bauth\b',
    r'\bsecret\b',
]

# File patterns that should never be committed
DANGEROUS_FILE_PATTERNS = [
    'keys/private_key.pem',
    'keys/*.key',
    'keys/*_private*',
    '*.pem.backup',
    '.env',
    '.env.local',
    '.env.*.local',
    'credentials.json',
    'service-account.json',
    '*-key.pem',
    '*-private-key.pem',
]

# File extensions to scan for sensitive data
SCANNABLE_EXTENSIONS = [
    '.md',
    '.txt',
    '.json',
    '.yaml',
    '.yml',
    '.toml',
    '.ini',
    '.conf',
    '.config',
]


def should_scan_file(filename: str) -> bool:
    """Determine if a file should be scanned for sensitive data.

    Args:
        filename: Path to the file

    Returns:
        True if the file should be scanned
    """
    # Check if it has a scannable extension
    return any(filename.endswith(ext) for ext in SCANNABLE_EXTENSIONS)


def is_dangerous_file(filename: str) -> bool:
    """Check if filename matches dangerous file patterns.

    Args:
        filename: Path to the file

    Returns:
        True if file matches dangerous patterns
    """
    import fnmatch
    return any(fnmatch.fnmatch(filename, pattern) for pattern in DANGEROUS_FILE_PATTERNS)
