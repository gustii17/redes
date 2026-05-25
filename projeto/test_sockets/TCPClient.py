from socket import *

#quando vc for testar, o servidor ele printa o seu IP, vc tem que substituir 
#no servername
serverName = '192.168.1.131'
serverPort = 12000

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))

while 1:
    sentence = input('Input lowercase sentence:')
    clientSocket.send(sentence.encode())
    modifiedSentence = clientSocket.recv(1024)
    print('From Server:', modifiedSentence.decode())

clientSocket.close()