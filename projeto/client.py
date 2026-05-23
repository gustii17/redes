import socket      # Biblioteca socket para implementação   

# Funções de comunicação com o server:
def receive():
    msg = client.recv(1024).decode()
    return msg

def send(msg):
    client.send(msg.encode())

# Funções do jogo:
slots = {
    "0" : "~", # Espaço de água 
    "1" : "o", # Espaço de água atingido
    "2" : "X", # Barco acertado
    "3" : "#" # Barco destruido
}

def mapa_usuario(s):
    t = ["  1 2 3 4", "A", "B", "C", "D"]
    mapa = t[0]
    
    for i in range(4):
        sub_s = s[i*4 : (i+1)*4]
        sub_st = [slots[c] for c in sub_s] # uso do dicionário
        t[i+1] += " " + " ".join(sub_st) # ou seja, t[i+1] = "a b c d"
        mapa += "\n" + t[i+1]
    return mapa    

def print_mapa(m):
    print("Identificação:")
    print("~ água desconhecida\no  tiro na água\nX  acerto\n#  navio afundado")
    print("CAMPO DO ADVERSÁRIO:\n")
    print(mapa_usuario(m))

def jogada():
    r = input("Qual casa você deseja atirar?(ex:A4,d2)")
    send(r)

def resultado():
    if(msg[4:] == "1/0"):
        print("Você perdeu!:(")
    elif(msg[4:] == "0/1"):
        print("Parabéns! Você venceu! :)")

#Ip e Porta
IP = "127.0.0.1"
PORT = 5000

client = socket.socket()    # Criação do socket do cliente
client.connect((IP,PORT))   # Conexão com o socket do servidor

while True:
    msg = receive()
    match msg[0:3]:
        case "200":            # Servidor confirma conexão
            continue           
        case "201":            # Início do Jogo
           print_mapa(msg[4:]) # Apresentação do tabuleiro

        case "202":             # Vez do Cliente jogar
            print_mapa(msg[4:]) # Apresentação do tabuleiro
            jogada()            # Jogada do jogador
        
        case "204":             # Jogo do adversário atualizado
            continue

        case "205":             # Atualização do tabuleiro
            print_mapa(msg[4:])
        case "206":             # Resultado da partida 
            resultado()

        case "207":             # Desconexão do Servidor 
            client.close()
            print("Desconectado.")