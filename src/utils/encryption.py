from cryptography.fernet import Fernet
from src.utils.config import get_or_create_key


ENCRYPTION_KEY = get_or_create_key()
cipher_suite = Fernet(ENCRYPTION_KEY)

def encrypt(data: str) -> str:
    """Encrypts the given data using Fernet symmetric encryption."""
    return cipher_suite.encrypt(data.encode()).decode()

def decrypt(data: str) -> str:
    """Decrypts the given data using Fernet symmetric encryption."""
    return cipher_suite.decrypt(data.encode()).decode()
