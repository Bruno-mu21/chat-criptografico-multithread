import socket, threading
from crypto_utils import CryptoUtils

class ChatClient:
    def __init__(self, name, host='127.0.0.1', port=12345):
        self.name = name
        self.key = CryptoUtils.generate_symmetric_key()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))

        
        public_key_bytes = self.socket.recv(1024)
        self.server_public_key = CryptoUtils.load_public_key(public_key_bytes)

        
        encrypted_key = CryptoUtils.encrypt_with_public_key(self.key, self.server_public_key)
        self.socket.send(encrypted_key)

        
        encrypted_name = CryptoUtils.encrypt_symmetric(name, self.key)
        self.socket.send(encrypted_name)

        self.listener_thread = threading.Thread(target=self.listen)
        self.listener_thread.start()

    def listen(self):
        while True:
            try:
                encrypted_message = self.socket.recv(4096)
                message = CryptoUtils.decrypt_symmetric(encrypted_message, self.key)
                print(message)
            except:
                break

    def send(self, message):
        encrypted = CryptoUtils.encrypt_symmetric(message, self.key)
        self.socket.send(encrypted)
