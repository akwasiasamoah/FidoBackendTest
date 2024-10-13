import os
from cryptography.fernet import Fernet

ENV_FILE_PATH = 'src/utils/env.py'
def get_or_create_key():
    """Gets the Fernet key from env.py or generates a new one if it doesn't exist."""
    if not os.path.isfile(ENV_FILE_PATH):
        # Create the env.py file if it doesn't exist
        with open(ENV_FILE_PATH, 'w') as env_file:
            env_file.write("# This file stores configuration variables\n")
    
    try:
        from src.utils.env import ENCRYPTION_KEY
        return ENCRYPTION_KEY.encode()
    except ImportError:
        # Generate and store a new key if not found
        key = Fernet.generate_key()
        with open(ENV_FILE_PATH, 'a') as env_file:
             env_file.write(f'ENCRYPTION_KEY = "{key.decode()}"\n') 
        return key
