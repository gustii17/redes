import socket      # Biblioteca socket para implementação   

# Funções de comunicação com o server:
def receive():
    msg = client.recv(1024).decode()
    return msg

def send(msg):
    client.send(msg.encode())

# Funções do jogo

def myMap(s):
    slots_my = {
        "0": "~",  # água
        "1": "o",  # tiro na água
        "2": "B",  # barco intacto
        "3": "X",  # barco atingido
        "4": "#"   # barco destruído
    }
    t = ["  1 2 3 4", "A", "B", "C", "D"]
    mapa = t[0]

    for i in range(4):
        sub_s = s[i*4 : (i+1)*4]
        sub_st = [slots_my[c] for c in sub_s]

        t[i+1] += " " + " ".join(sub_st)
        mapa += "\n" + t[i+1]

    return mapa


def enemyMap(s):

    slots_enemy = {
    "0" : "~", # Espaço de água 
    "1" : "o", # Espaço de água atingido
    "2" : "X", # Barco acertado
    "3" : "#" # Barco destruido
}
    
    t = ["  1 2 3 4", "A", "B", "C", "D"]
    mapa = t[0]
    
    for i in range(4):
        sub_s = s[i*4 : (i+1)*4]
        sub_st = [slots_enemy[c] for c in sub_s] # uso do dicionário
        t[i+1] += " " + " ".join(sub_st) # ou seja, t[i+1] = "a b c d"
        mapa += "\n" + t[i+1]
    return mapa    

def printMy(m):
    print("SEU CAMPO:")
    print(myMap(m))

def printEnemy(m):
    print("Identificação:")
    print("~ água desconhecida\no  tiro na água\nX  acerto\n#  navio afundado")
    print("CAMPO DO ADVERSÁRIO:\n")
    print(enemyMap(m))

def play():
    r = input("Qual casa você deseja atirar?(ex:A4,d2)")
    send("102 " + r)

def result(r):
    if r == "1/0":
        print("Você perdeu!:(")

    elif r == "0/1":
        print("Parabéns! Você venceu! :)")

def select_boat(n):
    boat_space = input("Selecione o as casas para alocar o navio " + n +"(ex: c3 para 1 casa e  a3 - a4):")
    send("103 " + boat_space)

#Ip e Porta
IP = "127.0.0.1"
PORT = 5000

client = socket.socket()    # Criação do socket do cliente
client.connect((IP,PORT))   # Conexão com o socket do servidor

enemy = "0000000000000000"
me =    "0000000000000000"

while True:
    msg = receive()

    match msg[0:3]:

        case "200":             # Servidor confirma conexão
            continue   

        case "201":             # Início do Jogo
            print("Jogo Iniciado!")
            printMy(me)
            print("--------------------------------------------")
            printEnemy(enemy)    # Apresentação do tabuleiro

        case "202":             # Vez do Cliente jogar
            printEnemy(enemy)   # Apresentação do tabuleiro
            play()              # Jogada do jogador
        
        case "203":             # O Server pede a alocação dos navios
            select_boat(msg[4:])

        case "204":             # Jogo do adversário atualizado
            enemy = msg[4:]
            printEnemy(enemy)

        case "205":             # Atualização do tabuleiro
            me = msg[4:]
            printMy(me)

        case "206":             # Resultado da partida 
            result(msg[4:])

        case "207":             # Desconexão do Servidor 
            client.close()
            print("Desconectado.")
            break