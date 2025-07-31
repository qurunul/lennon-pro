from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import os

class Encryption:
    """Kelas untuk enkripsi dan dekripsi AES-128 dalam mode CBC."""
    
    def __init__(self):
        self.key_length = 16  # 128-bit key
        self.block_size = 16  # AES block size

    def _pad_key(self, password: str) -> bytes:
        """Memastikan kunci memiliki panjang 16 byte."""
        return password.encode('utf-8')[:self.key_length].ljust(self.key_length, b'\0')

    def _pad_data(self, data: bytes) -> bytes:
        """Menambahkan padding ke data."""
        padder = padding.PKCS7(self.block_size * 8).padder()
        return padder.update(data) + padder.finalize()

    def _unpad_data(self, padded_data: bytes) -> bytes:
        """Menghapus padding dari data."""
        unpadder = padding.PKCS7(self.block_size * 8).unpadder()
        return unpadder.update(padded_data) + unpadder.finalize()

    def encrypt(self, data: bytes, password: str) -> bytes:
        """Mengenkripsi data dengan AES-128."""
        try:
            key = self._pad_key(password)
            iv = os.urandom(self.block_size)
            cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
            encryptor = cipher.encryptor()
            padded_data = self._pad_data(data)
            encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
            return iv + encrypted_data
        except Exception as e:
            raise ValueError(f"Gagal mengenkripsi: {str(e)}")

    def decrypt(self, encrypted_data: bytes, password: str) -> bytes:
        """Mendekripsi data dengan AES-128."""
        try:
            key = self._pad_key(password)
            iv = encrypted_data[:self.block_size]
            cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
            decryptor = cipher.decryptor()
            padded_data = decryptor.update(encrypted_data[self.block_size:]) + decryptor.finalize()
            return self._unpad_data(padded_data)
        except Exception as e:
            raise ValueError(f"Gagal mendekripsi: {str(e)}")