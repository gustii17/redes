from socket import *
import time

serverName = '127.0.0.1'  #cadeia contendo ou o IP ou o nome do servidor
serverPort = 12000  #porta

clientSocket = socket(AF_INET, SOCK_DGRAM) 
#1 parametro - familia do protocolo de endereçamento (IPv4)
#2 parametro - tipo do socket (SOCK_DGRAM para UDP)
#deixamos o SO escolher a porta do cliente, ou seja, não fazemos bind


message = input('Input lowercase sentence:')
#obtem string do usuario
                    
clientSocket.sendto(message.encode(),(serverName, serverPort))
#envia para o soquete();
time.sleep(3)
modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
# modifiedMessage recebe a resposta do servidor,
#  serverAddress recebe o endereço do servidor + porta do servidor

print(modifiedMessage.decode())
clientSocket.close()