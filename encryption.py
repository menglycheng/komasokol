from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
import base64
from dotenv import load_dotenv
load_dotenv()

# Load the key from the .env file
KEY = os.getenv("SERCET_KEY")

# Function to encrypt a message with base64 encoding using CTR mode
def encrypt_message_ctr(message):
    key = base64.urlsafe_b64decode(KEY)
    nonce = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CTR(nonce), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(message.encode()) + encryptor.finalize()
    encoded_ciphertext = base64.urlsafe_b64encode(nonce + ciphertext).decode().rstrip('=')

    return encoded_ciphertext

