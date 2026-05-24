import socket

class client:
    def __init__(self):
        self.serverName = ''
        self.serverPort = 0
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientIP = self.obter_ip_local()
        # self.endereco_cliente = self.clientSocket.getsockname()
        # self.porta_cliente = self.endereco_cliente[1]
        pass
    
    def obter_ip_local(self):
        try:
            nome_host = socket.gethostname()
            ip_local = socket.gethostbyname(nome_host) 
            return ip_local
        except Exception as e:            
            print(f"Erro ao obter o IP local: {e}")
            return None
        pass
    
    def conectar(self, IP_server, PORT_server):  
        self.serverName =  IP_server
        self.serverPort = PORT_server
        try:
            self.clientSocket.connect((self.serverName,self.serverPort))
        except Exception as e:
            print(f"Erro ao se conectar: {e}")
    pass

    def send_msg(self, msg):
        try: 
            self.clientSocket.send(msg.encode())
        except Exception as e:
            print(f"Erro ao mandar mensagem: {e}")
        pass

    def recibe_msg(self):
        try:
            sentence = self.clientSocket.recv(1024)
        except Exception as e:
            print(f"Erro ao receber mensagem: {e}")
        return sentence.decode()
    
    def desconectar(self):
        try: 
            self.clientSocket.close()
        except Exception as e:
            print(f"Erro ao fechar conexão com o servidor: {e}")
        pass
    

    pass
