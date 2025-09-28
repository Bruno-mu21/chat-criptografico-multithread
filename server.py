import socket, threading
from crypto_utils import CryptoUtils

class ClientHandler(threading.Thread):
    def __init__(self, conn, addr, server):
        super().__init__()
        self.conn = conn
        self.addr = addr
        self.server = server
        self.key = None
        self.name = None

    def run(self):
        try:
            
            self.conn.send(CryptoUtils.serialize_public_key(self.server.public_key))

            
            encrypted_symmetric_key = self.conn.recv(512)
            self.key = CryptoUtils.decrypt_with_private_key(encrypted_symmetric_key, self.server.private_key)

            
            encrypted_name = self.conn.recv(1024)
            self.name = CryptoUtils.decrypt_symmetric(encrypted_name, self.key)

            self.server.broadcast(f"{self.name} conectado", self)

            while True:
                encrypted_msg = self.conn.recv(4096)
                if not encrypted_msg:
                    break
                message = CryptoUtils.decrypt_symmetric(encrypted_msg, self.key)
                full_msg = f"({self.name}): {message}"
                self.server.broadcast(full_msg, self)

        except Exception as e:
            print(f"Erro com {self.addr}: {e}")
        finally:
            self.conn.close()
            self.server.remove_client(self)

    def send_message(self, message):
        encrypted = CryptoUtils.encrypt_symmetric(message, self.key)
        self.conn.send(encrypted)

class ChatServer:
    def __init__(self, host='127.0.0.1', port=12345):
        self.clients = []
        self.private_key, self.public_key = CryptoUtils.generate_rsa_keys()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((host, port))
        self.socket.listen()
        print(f"Servidor escutando em {host}:{port}")

    def broadcast(self, message, origin_client):
        print("Broadcast:", message)
        for client in self.clients:
            if client != origin_client:
                client.send_message(message)

    def remove_client(self, client):
        if client in self.clients:
            self.clients.remove(client)

    def start(self):
        while True:
            conn, addr = self.socket.accept()
            client_handler = ClientHandler(conn, addr, self)
            self.clients.append(client_handler)
            client_handler.start()
