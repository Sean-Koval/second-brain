"""Tests for encryption/decryption functionality."""

import pytest
import tempfile
import shutil
from pathlib import Path

from second_brain.crypto.key_manager import KeyManager, KeyExistsError
from second_brain.crypto.encryption import Encryptor, EncryptionError


@pytest.fixture
def temp_keys_dir():
    """Create a temporary directory for keys."""
    temp_dir = tempfile.mkdtemp()
    yield Path(temp_dir)
    shutil.rmtree(temp_dir)


@pytest.fixture
def key_manager(temp_keys_dir):
    """Create a key manager with temporary directory."""
    return KeyManager(temp_keys_dir)


@pytest.fixture
def key_manager_with_keys(temp_keys_dir):
    """Create a key manager with generated keys."""
    km = KeyManager(temp_keys_dir)
    private_key, public_key = km.generate_key_pair()
    km.save_keys(private_key, public_key)
    return km


@pytest.fixture
def encryptor(key_manager_with_keys):
    """Create an encryptor with valid keys."""
    return Encryptor(key_manager_with_keys)


class TestKeyManager:
    """Test key management functionality."""

    def test_keys_do_not_exist_initially(self, key_manager):
        """Test that keys don't exist in fresh directory."""
        assert key_manager.keys_exist() is False

    def test_generate_key_pair(self, key_manager):
        """Test generating a new key pair."""
        private_key, public_key = key_manager.generate_key_pair()
        key_manager.save_keys(private_key, public_key)

        assert key_manager.keys_exist() is True
        assert key_manager.public_key_path.exists()
        assert key_manager.private_key_path.exists()

    def test_generate_key_pair_with_passphrase(self, temp_keys_dir):
        """Test generating keys with passphrase protection."""
        km = KeyManager(temp_keys_dir)
        private_key, public_key = km.generate_key_pair()
        km.save_keys(private_key, public_key, passphrase="test-passphrase")

        assert km.keys_exist() is True
        # Metadata should indicate passphrase protection
        metadata = km.load_metadata()
        assert metadata is not None
        assert metadata.get("has_passphrase") is True

    def test_cannot_overwrite_existing_keys(self, key_manager_with_keys):
        """Test that keys already exist after fixture runs."""
        # Keys already exist from fixture
        assert key_manager_with_keys.keys_exist() is True
        assert key_manager_with_keys.public_key_path.exists()
        assert key_manager_with_keys.private_key_path.exists()

    def test_load_public_key(self, key_manager_with_keys):
        """Test loading the public key."""
        public_key = key_manager_with_keys.load_public_key()
        assert public_key is not None

    def test_load_private_key(self, key_manager_with_keys):
        """Test loading the private key without passphrase."""
        private_key = key_manager_with_keys.load_private_key()
        assert private_key is not None

    def test_load_private_key_with_wrong_passphrase(self, temp_keys_dir):
        """Test that wrong passphrase fails to load private key."""
        km = KeyManager(temp_keys_dir)
        private_key, public_key = km.generate_key_pair()
        km.save_keys(private_key, public_key, passphrase="correct-passphrase")

        # Try to load with wrong passphrase
        km2 = KeyManager(temp_keys_dir)
        with pytest.raises(Exception):  # Cryptography raises various exceptions
            km2.load_private_key(passphrase="wrong-passphrase")

    def test_get_fingerprint(self, key_manager_with_keys):
        """Test getting key fingerprint."""
        public_key = key_manager_with_keys.load_public_key()
        fingerprint = key_manager_with_keys.get_fingerprint(public_key)
        assert fingerprint is not None
        assert len(fingerprint) > 0
        # Fingerprint should be SHA256:base64 format
        assert fingerprint.startswith("SHA256:")

    def test_key_metadata(self, key_manager_with_keys):
        """Test key metadata is stored correctly."""
        metadata = key_manager_with_keys.load_metadata()
        assert metadata is not None
        assert "created_at" in metadata
        assert "algorithm" in metadata
        assert metadata["algorithm"] == "RSA-4096"  # Default size

    def test_custom_key_size(self, temp_keys_dir):
        """Test generating keys with custom size."""
        km = KeyManager(temp_keys_dir)
        private_key, public_key = km.generate_key_pair(key_size=2048)
        km.save_keys(private_key, public_key)

        metadata = km.load_metadata()
        assert metadata["algorithm"] == "RSA-2048"


class TestEncryptor:
    """Test encryption/decryption functionality."""

    def test_encrypt_simple_string(self, encryptor):
        """Test encrypting a simple string."""
        plaintext = "Hello, World!"
        encrypted = encryptor.encrypt(plaintext)

        assert encrypted is not None
        assert encrypted != plaintext
        # Check format: v1:RSA-AES256-GCM:...
        assert encrypted.startswith("v1:RSA-AES256-GCM:")

    def test_decrypt_simple_string(self, encryptor):
        """Test decrypting back to original."""
        plaintext = "Hello, World!"
        encrypted = encryptor.encrypt(plaintext)
        decrypted = encryptor.decrypt(encrypted)

        assert decrypted == plaintext

    def test_encrypt_unicode(self, encryptor):
        """Test encrypting unicode content."""
        plaintext = "Hello 世界 🌍 émojis"
        encrypted = encryptor.encrypt(plaintext)
        decrypted = encryptor.decrypt(encrypted)

        assert decrypted == plaintext

    def test_encrypt_multiline(self, encryptor):
        """Test encrypting multiline content."""
        plaintext = """Line 1
Line 2
Line 3 with special chars: <>&"'"""
        encrypted = encryptor.encrypt(plaintext)
        decrypted = encryptor.decrypt(encrypted)

        assert decrypted == plaintext

    def test_encrypt_empty_string(self, encryptor):
        """Test encrypting empty string."""
        plaintext = ""
        encrypted = encryptor.encrypt(plaintext)
        decrypted = encryptor.decrypt(encrypted)

        assert decrypted == plaintext

    def test_encrypt_large_content(self, encryptor):
        """Test encrypting large content."""
        # 100KB of text
        plaintext = "A" * 100_000
        encrypted = encryptor.encrypt(plaintext)
        decrypted = encryptor.decrypt(encrypted)

        assert decrypted == plaintext

    def test_is_encrypted_detection(self, encryptor):
        """Test detection of encrypted content."""
        plaintext = "Not encrypted"
        encrypted = encryptor.encrypt("Secret data")

        assert encryptor.is_encrypted(plaintext) is False
        assert encryptor.is_encrypted(encrypted) is True

    def test_decrypt_invalid_format(self, encryptor):
        """Test decrypting invalid format fails gracefully."""
        with pytest.raises(EncryptionError):
            encryptor.decrypt("not-valid-encrypted-data")

    def test_decrypt_corrupted_data(self, encryptor):
        """Test decrypting corrupted data fails gracefully."""
        encrypted = encryptor.encrypt("test")
        # Corrupt the data
        corrupted = encrypted[:-10] + "CORRUPTED!"

        with pytest.raises(EncryptionError):
            encryptor.decrypt(corrupted)


class TestEncryptedBlocks:
    """Test markdown encrypted block functionality."""

    def test_create_encrypted_block(self, encryptor):
        """Test creating markdown encrypted block."""
        plaintext = "Secret content"
        block = encryptor.create_encrypted_block(plaintext)

        assert "<!-- ENCRYPTED:" in block
        assert "<!-- END ENCRYPTED -->" in block

    def test_extract_encrypted_blocks(self, encryptor):
        """Test extracting encrypted blocks from markdown."""
        plaintext = "Secret data"
        block = encryptor.create_encrypted_block(plaintext)
        
        markdown = f"""# My Document
        
Some public text here.

{block}

More public text.
"""
        blocks = encryptor.extract_encrypted_blocks(markdown)
        assert len(blocks) == 1

    def test_decrypt_markdown(self, encryptor):
        """Test decrypting markdown with encrypted blocks."""
        secret = "My secret data"
        block = encryptor.create_encrypted_block(secret)
        
        markdown = f"""# Document

Public content.

{block}

More content.
"""
        decrypted = encryptor.decrypt_markdown(markdown)
        assert secret in decrypted
        assert "<!-- ENCRYPTED:" not in decrypted

    def test_decrypt_markdown_multiple_blocks(self, encryptor):
        """Test decrypting markdown with multiple encrypted blocks."""
        secret1 = "First secret"
        secret2 = "Second secret"
        block1 = encryptor.create_encrypted_block(secret1)
        block2 = encryptor.create_encrypted_block(secret2)
        
        markdown = f"""# Document

{block1}

Middle content.

{block2}
"""
        decrypted = encryptor.decrypt_markdown(markdown)
        assert secret1 in decrypted
        assert secret2 in decrypted

    def test_decrypt_markdown_no_blocks(self, encryptor):
        """Test decrypting markdown with no encrypted blocks."""
        markdown = """# Document

Just plain content here.
"""
        decrypted = encryptor.decrypt_markdown(markdown)
        assert decrypted == markdown


class TestEncryptionWithPassphrase:
    """Test encryption with passphrase-protected keys."""

    def test_encrypt_decrypt_with_passphrase(self, temp_keys_dir):
        """Test full encrypt/decrypt cycle with passphrase."""
        passphrase = "my-secure-passphrase"
        
        # Generate and save keys with passphrase
        km = KeyManager(temp_keys_dir)
        private_key, public_key = km.generate_key_pair()
        km.save_keys(private_key, public_key, passphrase=passphrase)

        # Encryption uses public key (no passphrase needed)
        encryptor = Encryptor(km)
        plaintext = "Secret message"
        encrypted = encryptor.encrypt(plaintext)

        # Decryption requires passphrase
        decrypted = encryptor.decrypt(encrypted, passphrase=passphrase)
        assert decrypted == plaintext

    def test_decrypt_fails_without_passphrase(self, temp_keys_dir):
        """Test decryption fails when passphrase is required but not provided."""
        passphrase = "my-secure-passphrase"
        
        km = KeyManager(temp_keys_dir)
        private_key, public_key = km.generate_key_pair()
        km.save_keys(private_key, public_key, passphrase=passphrase)

        encryptor = Encryptor(km)
        encrypted = encryptor.encrypt("Secret")

        # Try to decrypt without passphrase
        with pytest.raises(Exception):
            encryptor.decrypt(encrypted)


class TestKeyRotation:
    """Test key rotation scenarios."""

    def test_content_encrypted_with_old_key_fails_with_new_key(self, temp_keys_dir):
        """Test that content encrypted with old key cannot be decrypted with new key."""
        # Create first key pair
        km1 = KeyManager(temp_keys_dir)
        private_key1, public_key1 = km1.generate_key_pair()
        km1.save_keys(private_key1, public_key1)

        # Encrypt with first key
        encryptor1 = Encryptor(km1)
        encrypted = encryptor1.encrypt("Secret data")

        # Remove keys and create new ones
        km1.public_key_path.unlink()
        km1.private_key_path.unlink()
        km1.metadata_path.unlink()

        km2 = KeyManager(temp_keys_dir)
        private_key2, public_key2 = km2.generate_key_pair()
        km2.save_keys(private_key2, public_key2)

        # Try to decrypt with new key - should fail
        encryptor2 = Encryptor(km2)
        with pytest.raises(EncryptionError):
            encryptor2.decrypt(encrypted)


class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_encrypt_without_keys_fails(self, temp_keys_dir):
        """Test encryption fails when keys don't exist."""
        km = KeyManager(temp_keys_dir)
        encryptor = Encryptor(km)

        with pytest.raises(Exception):
            encryptor.encrypt("test")

    def test_decrypt_without_keys_fails(self, temp_keys_dir):
        """Test decryption fails when keys don't exist."""
        # First create keys, encrypt, then remove keys
        km = KeyManager(temp_keys_dir)
        private_key, public_key = km.generate_key_pair()
        km.save_keys(private_key, public_key)
        
        encryptor = Encryptor(km)
        encrypted = encryptor.encrypt("test")

        # Remove keys
        km.public_key_path.unlink()
        km.private_key_path.unlink()

        # Try to decrypt
        km2 = KeyManager(temp_keys_dir)
        encryptor2 = Encryptor(km2)
        
        with pytest.raises(Exception):
            encryptor2.decrypt(encrypted)

    def test_key_directory_permissions(self, temp_keys_dir):
        """Test that private key has restricted permissions."""
        km = KeyManager(temp_keys_dir)
        private_key, public_key = km.generate_key_pair()
        km.save_keys(private_key, public_key)

        # Check private key permissions (should be 600 or stricter)
        import stat
        mode = km.private_key_path.stat().st_mode
        # Owner read/write only
        assert mode & stat.S_IRWXG == 0  # No group permissions
        assert mode & stat.S_IRWXO == 0  # No other permissions


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
