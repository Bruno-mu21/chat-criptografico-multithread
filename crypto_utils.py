from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.fernet import Fernet

class CryptoUtils:

    @staticmethod
    def generate_rsa_keys():
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        public_key = private_key.public_key()
        return private_key, public_key

    @staticmethod
    def serialize_public_key(public_key):
        return public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

    @staticmethod
    def load_public_key(pem_data):
        return serialization.load_pem_public_key(pem_data)

    @staticmethod
    def encrypt_with_public_key(message: bytes, public_key):
        return public_key.encrypt(
            message,
            padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
        )

    @staticmethod
    def decrypt_with_private_key(encrypted_data, private_key):
        return private_key.decrypt(
            encrypted_data,
            padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
        )

    @staticmethod
    def generate_symmetric_key():
        return Fernet.generate_key()

    @staticmethod
    def encrypt_symmetric(message: str, key: bytes):
        return Fernet(key).encrypt(message.encode())

    @staticmethod
    def decrypt_symmetric(encrypted_message: bytes, key: bytes):
        return Fernet(key).decrypt(encrypted_message).decode()
