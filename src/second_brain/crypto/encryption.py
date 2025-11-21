"""Core encryption/decryption operations.

Implements hybrid RSA+AES encryption for secure data storage.
Uses AES-256-GCM for data encryption and RSA-OAEP for key encryption.
"""

from pathlib import Path
from typing import Tuple, Optional
import os
import base64
import re

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

from .key_manager import KeyManager


class EncryptionError(Exception):
    """Raised when encryption/decryption fails."""
    pass


class Encryptor:
    """Handles encryption and decryption of data."""

    VERSION = "v1"
    ALGORITHM = "RSA-AES256-GCM"
    AES_KEY_SIZE = 32  # 256 bits
    NONCE_SIZE = 12    # 96 bits (recommended for GCM)

    def __init__(self, key_manager: KeyManager):
        """Initialize encryptor with key manager.

        Args:
            key_manager: KeyManager instance for loading keys
        """
        self.key_manager = key_manager

    def encrypt(
        self,
        plaintext: str,
        passphrase: Optional[str] = None
    ) -> str:
        """Encrypt plaintext string.

        Args:
            plaintext: String to encrypt
            passphrase: Passphrase if private key is encrypted

        Returns:
            Encrypted string in format:
            v1:RSA-AES256-GCM:encrypted_key:nonce:ciphertext

        Raises:
            EncryptionError: If encryption fails
        """
        try:
            # Load public key
            public_key = self.key_manager.load_public_key()

            # Generate random AES key
            aes_key = os.urandom(self.AES_KEY_SIZE)

            # Generate random nonce
            nonce = os.urandom(self.NONCE_SIZE)

            # Encrypt data with AES-256-GCM
            aesgcm = AESGCM(aes_key)
            ciphertext = aesgcm.encrypt(
                nonce,
                plaintext.encode('utf-8'),
                None  # No additional data
            )

            # Encrypt AES key with RSA public key
            encrypted_key = public_key.encrypt(
                aes_key,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )

            # Encode to base64
            encrypted_key_b64 = base64.b64encode(encrypted_key).decode('ascii')
            nonce_b64 = base64.b64encode(nonce).decode('ascii')
            ciphertext_b64 = base64.b64encode(ciphertext).decode('ascii')

            # Format: version:algorithm:encrypted_key:nonce:ciphertext
            return f"{self.VERSION}:{self.ALGORITHM}:{encrypted_key_b64}:{nonce_b64}:{ciphertext_b64}"

        except Exception as e:
            raise EncryptionError(f"Encryption failed: {e}")

    def decrypt(
        self,
        encrypted_data: str,
        passphrase: Optional[str] = None
    ) -> str:
        """Decrypt encrypted string.

        Args:
            encrypted_data: Encrypted string from encrypt()
            passphrase: Passphrase if private key is encrypted

        Returns:
            Decrypted plaintext string

        Raises:
            EncryptionError: If decryption fails
        """
        try:
            # Parse format string
            parts = encrypted_data.split(':')
            if len(parts) != 5:
                raise EncryptionError("Invalid encrypted data format")

            version, algorithm, encrypted_key_b64, nonce_b64, ciphertext_b64 = parts

            # Validate version
            if version != self.VERSION:
                raise EncryptionError(f"Unsupported version: {version}")

            # Validate algorithm
            if algorithm != self.ALGORITHM:
                raise EncryptionError(f"Unsupported algorithm: {algorithm}")

            # Decode from base64
            encrypted_key = base64.b64decode(encrypted_key_b64)
            nonce = base64.b64decode(nonce_b64)
            ciphertext = base64.b64decode(ciphertext_b64)

            # Load private key
            private_key = self.key_manager.load_private_key(passphrase)

            # Decrypt AES key with RSA private key
            aes_key = private_key.decrypt(
                encrypted_key,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )

            # Decrypt data with AES-256-GCM
            aesgcm = AESGCM(aes_key)
            plaintext_bytes = aesgcm.decrypt(nonce, ciphertext, None)

            return plaintext_bytes.decode('utf-8')

        except Exception as e:
            raise EncryptionError(f"Decryption failed: {e}")

    def is_encrypted(self, data: str) -> bool:
        """Check if string is encrypted data.

        Args:
            data: String to check

        Returns:
            True if data appears to be encrypted
        """
        return data.startswith(f"{self.VERSION}:{self.ALGORITHM}:")

    def create_encrypted_block(self, plaintext: str) -> str:
        """Create markdown encrypted block.

        Args:
            plaintext: Text to encrypt and wrap

        Returns:
            Markdown encrypted block:
            <!-- ENCRYPTED:v1:RSA-AES256-GCM -->
            encrypted_data_here
            <!-- END ENCRYPTED -->
        """
        encrypted = self.encrypt(plaintext)
        return (
            f"<!-- ENCRYPTED:{self.VERSION}:{self.ALGORITHM} -->\n"
            f"{encrypted}\n"
            f"<!-- END ENCRYPTED -->"
        )

    def extract_encrypted_blocks(self, markdown: str) -> list[Tuple[str, str]]:
        """Extract encrypted blocks from markdown.

        Args:
            markdown: Markdown content

        Returns:
            List of (block_text, encrypted_data) tuples
        """
        pattern = r'<!-- ENCRYPTED:(.+?) -->\n(.+?)\n<!-- END ENCRYPTED -->'
        matches = re.findall(pattern, markdown, re.DOTALL)

        results = []
        for algorithm, encrypted_data in matches:
            block_text = f"<!-- ENCRYPTED:{algorithm} -->\n{encrypted_data}\n<!-- END ENCRYPTED -->"
            results.append((block_text, encrypted_data.strip()))

        return results

    def decrypt_markdown(
        self,
        markdown: str,
        passphrase: Optional[str] = None
    ) -> str:
        """Decrypt all encrypted blocks in markdown.

        Args:
            markdown: Markdown with encrypted blocks
            passphrase: Passphrase if private key is encrypted

        Returns:
            Markdown with decrypted content
        """
        blocks = self.extract_encrypted_blocks(markdown)
        result = markdown

        for block_text, encrypted_data in blocks:
            try:
                plaintext = self.decrypt(encrypted_data, passphrase)
                result = result.replace(block_text, plaintext)
            except EncryptionError:
                # Leave encrypted if can't decrypt
                pass

        return result
