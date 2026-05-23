from clientClass import client #importando a lasse

client1 = client() # criando o objeto
#consectando ao server, passe como parametro o IP e a porta
client1.conectar('192.168.0.51', 12000) 

while 1:
    msg = input('sentence: ')
    #função para mandar mensagem
    client1.send_msg(msg)
    #função para receber mensagem
    sentence = client1.recibe_msg()
    print("mensagem recebida: ", sentence)
    if sentence == 'exit':
        #função para desconectar do servidor
        client1.desconectar()
