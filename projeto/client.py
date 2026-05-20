import socket      # Biblioteca socket para implementação   

def receive():
    client.recv(1024).decode()

def send(msg):
    client.send(msg).encode()

IP = "127.0.0.1"   # Ip do server
PORT = 5000        # Porta do server

client = socket.socket()    # Criação do socket do cliente
client.connect((IP,PORT))   # Conexão com o socket do servidor

while(True):