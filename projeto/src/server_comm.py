#include socket
#ip, porta, conexao, etc
import socket


class server:
    def __init__(self,  PORT):
        self.serverPort = PORT
        self.ServerIP = self.obter_ip_local()
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientSocket.bind((self.ServerIP, self.serverPort))
        self.clientSocket.listen(2)
        self.clients = []
        print(f'Servidor rodando em {self.ServerIP}:{self.serverPort}')

    def obter_ip_local(self):
        try:
            nome_host = socket.gethostname()
            ip_local = socket.gethostbyname(nome_host) 
            return ip_local
        except Exception as e:            
            print(f"Erro ao obter o IP local: {e}")
            return None

    def aceitar_conexao(self):
        try:
            print('Aguardando conexão...')
            connectionSocket, addr = self.clientSocket.accept()
            print(f'Conexão aceita de {addr}, em IP: {connectionSocket}')
            self.clients.append(connectionSocket)
        except Exception as e:
            print(f"Erro ao aceitar conexão: {e}")

    def listar_clients(self):
        print("Clientes conectados:")
        for client in self.clients:
            print(client.getpeername())

    def fechar_conexao_geral(self):
        for client in self.clients:
            client.close()
        self.clients.clear()

    def fechar_conexao_individual(self, client):
        if client in self.clients:
            client.close()
            self.clients.remove(client)
        else:
            print("Cliente não encontrado.")
    
    
    def send_msg(self, num_client, msg):
        self.clients[num_client].send(msg.encode())
    
    def recibe_msg(self, num_client):
        sentence = self.clients[num_client].recv(1024)
        return sentence.decode()

    def get_port(self, num_client):
        return self.clients[num_client] 


    
