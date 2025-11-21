"""RSA key management for Second Brain encryption.

Handles generation, storage, and loading of RSA key pairs with proper
security measures including permission validation and passphrase protection.
"""

import json
import os
from pathlib import Path
from typing import Optional, Tuple

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend

from ..utils import datetime_utils


class KeyExistsError(Exception):
    """Raised when attempting to create keys that already exist."""
    pass


class KeyManager:
    """Manage RSA key pairs for encryption.

    Handles secure generation, storage, and loading of RSA keys with
    proper file permissions and optional passphrase protection.
    """

    def __init__(self, keys_dir: Path):
        """Initialize key manager.

        Args:
            keys_dir: Directory where keys will be stored
        """
        self.keys_dir = Path(keys_dir)
        self.private_key_path = self.keys_dir / "private_key.pem"
        self.public_key_path = self.keys_dir / "public_key.pem"
        self.metadata_path = self.keys_dir / ".key_metadata.json"

    def keys_exist(self) -> bool:
        """Check if keys already exist.

        Returns:
            True if both private and public keys exist
        """
        return self.private_key_path.exists() and self.public_key_path.exists()

    def generate_key_pair(
        self,
        key_size: int = 4096,
        passphrase: Optional[str] = None
    ) -> Tuple[rsa.RSAPrivateKey, rsa.RSAPublicKey]:
        """Generate RSA key pair.

        Args:
            key_size: Key size in bits (default 4096)
            passphrase: Optional passphrase for private key encryption

        Returns:
            Tuple of (private_key, public_key)

        Note:
            This method only generates keys, it does not save them.
            Use save_keys() to persist to disk.
        """
        # Generate private key
        private_key = rsa.generate_private_key(
            public_exponent=65537,  # Standard public exponent
            key_size=key_size,
            backend=default_backend()
        )

        # Derive public key
        public_key = private_key.public_key()

        return private_key, public_key

    def save_keys(
        self,
        private_key: rsa.RSAPrivateKey,
        public_key: rsa.RSAPublicKey,
        passphrase: Optional[str] = None
    ) -> None:
        """Save keys to disk with proper permissions.

        Args:
            private_key: RSA private key to save
            public_key: RSA public key to save
            passphrase: Optional passphrase to encrypt private key

        Note:
            - Private key is saved with 600 permissions (owner read/write only)
            - Public key is saved with 644 permissions (world readable)
            - Metadata file is created with key information
        """
        # Create keys directory if it doesn't exist
        self.keys_dir.mkdir(parents=True, exist_ok=True)

        # Save private key with restricted permissions
        self._save_private_key(private_key, passphrase)

        # Save public key (world readable)
        self._save_public_key(public_key)

        # Create metadata file
        metadata = self.create_metadata(public_key)
        metadata['has_passphrase'] = passphrase is not None

        with open(self.metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)

    def _save_private_key(
        self,
        private_key: rsa.RSAPrivateKey,
        passphrase: Optional[str]
    ) -> None:
        """Save private key with 600 permissions.

        Args:
            private_key: RSA private key
            passphrase: Optional passphrase for encryption
        """
        # Set umask to create file with restricted permissions
        old_umask = os.umask(0o077)

        try:
            # Determine encryption algorithm
            if passphrase:
                encryption = serialization.BestAvailableEncryption(
                    passphrase.encode('utf-8')
                )
            else:
                encryption = serialization.NoEncryption()

            # Serialize private key to PEM format
            pem = private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=encryption
            )

            # Write to file
            with open(self.private_key_path, 'wb') as f:
                f.write(pem)

            # Explicitly set permissions to 600
            self.private_key_path.chmod(0o600)
        finally:
            # Restore original umask
            os.umask(old_umask)

    def _save_public_key(self, public_key: rsa.RSAPublicKey) -> None:
        """Save public key with 644 permissions.

        Args:
            public_key: RSA public key
        """
        # Serialize public key to PEM format
        pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        # Write to file
        self.public_key_path.write_bytes(pem)

        # Set permissions to 644 (world readable)
        self.public_key_path.chmod(0o644)

    def load_private_key(
        self,
        passphrase: Optional[str] = None
    ) -> rsa.RSAPrivateKey:
        """Load private key from disk.

        Args:
            passphrase: Passphrase if key is encrypted

        Returns:
            RSA private key

        Raises:
            FileNotFoundError: If private key doesn't exist
            PermissionError: If private key has unsafe permissions
            ValueError: If passphrase is incorrect
        """
        # Check file exists
        if not self.private_key_path.exists():
            raise FileNotFoundError(
                f"Private key not found at {self.private_key_path}\n"
                f"Generate keys with: sb key generate"
            )

        # Validate permissions
        self._validate_private_key_permissions()

        # Read key file
        with open(self.private_key_path, 'rb') as f:
            key_data = f.read()

        # Deserialize key
        password_bytes = passphrase.encode('utf-8') if passphrase else None

        try:
            private_key = serialization.load_pem_private_key(
                key_data,
                password=password_bytes,
                backend=default_backend()
            )
        except TypeError:
            raise ValueError(
                "Key is encrypted but no passphrase provided, or "
                "key is not encrypted but passphrase was provided"
            )
        except Exception as e:
            raise ValueError(f"Failed to load private key: {e}")

        return private_key

    def load_public_key(self) -> rsa.RSAPublicKey:
        """Load public key from disk.

        Returns:
            RSA public key

        Raises:
            FileNotFoundError: If public key doesn't exist
        """
        if not self.public_key_path.exists():
            raise FileNotFoundError(
                f"Public key not found at {self.public_key_path}\n"
                f"Generate keys with: sb key generate"
            )

        # Read and deserialize key
        with open(self.public_key_path, 'rb') as f:
            key_data = f.read()

        public_key = serialization.load_pem_public_key(
            key_data,
            backend=default_backend()
        )

        return public_key

    def _validate_private_key_permissions(self) -> None:
        """Validate private key has 600 permissions.

        Raises:
            PermissionError: If permissions are not restrictive enough
        """
        stat_info = self.private_key_path.stat()
        mode = stat_info.st_mode

        # Check permissions (should be 600 = rw-------)
        # Check if group or other have any permissions
        if mode & 0o077:
            current_perms = oct(mode)[-3:]
            raise PermissionError(
                f"Private key {self.private_key_path} has unsafe permissions.\n"
                f"Current: {current_perms}\n"
                f"Required: 600\n"
                f"Fix with: chmod 600 {self.private_key_path}"
            )

    def get_fingerprint(self, public_key: rsa.RSAPublicKey) -> str:
        """Get SHA256 fingerprint of public key.

        Args:
            public_key: RSA public key

        Returns:
            Fingerprint string in format "SHA256:base64..."
        """
        # Get public key bytes
        public_bytes = public_key.public_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        # Compute SHA256 hash
        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.primitives.hashes import Hash

        digest = Hash(hashes.SHA256(), backend=default_backend())
        digest.update(public_bytes)
        hash_bytes = digest.finalize()

        # Encode as base64
        import base64
        fingerprint = base64.b64encode(hash_bytes).decode('ascii')

        return f"SHA256:{fingerprint}"

    def create_metadata(self, public_key: rsa.RSAPublicKey) -> dict:
        """Create key metadata.

        Args:
            public_key: RSA public key

        Returns:
            Dictionary with key metadata
        """
        # Get key size
        key_size = public_key.key_size

        # Get current time in configured timezone
        created_at = datetime_utils.now().isoformat()

        return {
            "created_at": created_at,
            "algorithm": f"RSA-{key_size}",
            "public_key_fingerprint": self.get_fingerprint(public_key),
            "version": "v1"
        }

    def load_metadata(self) -> Optional[dict]:
        """Load key metadata if it exists.

        Returns:
            Metadata dictionary or None if doesn't exist
        """
        if not self.metadata_path.exists():
            return None

        try:
            with open(self.metadata_path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return None
