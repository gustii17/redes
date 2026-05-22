from socket import *
import time

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)

serverSocket.bind(('', serverPort))
#vincula o numero da porta 12000 para o servidor
print('The server is ready to receive')


while 1:
    time.sleep(10)
    print('a')
    message, clientAddress = serverSocket.recvfrom(2048)
    #message recebe a mensagem do cliente, 
    #clientAddress recebe o endereço do cliente + porta do cliente
    modifiedMessage = message.decode().upper()
    #vai para maiusculo
    serverSocket.sendto(modifiedMessage.encode(), clientAddress)
    #manda a mensagem