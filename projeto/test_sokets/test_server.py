from Server import server

#cria o objeto servidor com a porta 12000, usa conexão tcp, e ja tem o IP automaticment
Server = server(12000) 

#aceita a conexão de 2 usuários
Server.aceitar_conexao()
Server.aceitar_conexao()

#lista as portas dos usuarios ativos
Server.listar_clients()

#loop para ficar recebendo mensagem - não necessário
while 1:
    #recebendo a mensagem do primeiro que conectou, para isso, passe o parametro 0
    #recebe mensagem com o parametro sendo de qual cliente
    sentence = Server.recibe_msg(0) 
    #mandando menssagem, o parametro é de quem
    Server.send_msg(0, sentence)
    print(sentence)
    if sentence == 'quit': 
        print('q')
        exit()
    #
    #
    #recebendo mensagem do 2 usuario
    sentence = Server.recibe_msg(1)
    Server.send_msg(1, sentence)
    print(sentence)
    if sentence == 'exit': 
        print('saindo')
        break


print('a')
#fechando a conexão somente de 1, atenção, os que estão apos dele, decrementam
#1 no contador de seus indices
Server.fechar_conexao_individual(Server.get_port(0))#soquer
Server.listar_clients()
#fecha a conexão de todo mundo
Server.fechar_conexao_geral()
Server.listar_clients()