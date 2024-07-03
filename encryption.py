from cryptography.fernet import Fernet
import urllib.parse

# Function to encrypt a message
def encrypt_message(message, key):
    cipher_suite = Fernet(key.encode())
    ciphertext = cipher_suite.encrypt(message.encode())
    encoded_ciphertext = urllib.parse.quote(ciphertext)
    return encoded_ciphertext


