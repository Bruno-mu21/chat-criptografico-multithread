from client import ChatClient

name = input("Seu nome: ")
client = ChatClient(name)

while True:
    msg = input("Mensagem: ")
    client.send(msg)

