import socket      # Biblioteca socket para implementação  

#----------------------------
#---FUNÇÕES DE COMUNICAÇÃO---
#----------------------------
def receive():
    msg = client.recv(1024).decode()
    return msg

def send(msg):
    client.send(msg.encode())

#Ip e Porta
IP = "127.0.0.1"
PORT = 5000

client = socket.socket()    # Criação do socket do cliente
client.connect((IP,PORT))   # Conexão com o socket do servidor

enemy = "0000000000000000"
me =    "0000000000000000"

#---------------------
#---FUNÇÕES DO JOGO---
#---------------------
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
    print("~  Água desconhecida\no  Tiro na água\nX  Acerto\n#  Navio afundado\n")
    print("CAMPO DO ADVERSÁRIO:\n")
    print(enemyMap(m))

def play():
    r = input("\nQual casa deseja atacar? ")
    print(f"\nVocê atacou: {r}")

def result(r):
    if r == "1/0":
        print("Você perdeu!:(")

    elif r == "0/1":
        print("Parabéns! Você venceu! :)")

def select_boat(n):
    boat = input(f"\nSelecione posições do navio {n}: ")
    print(f"\nNavio {n} em {boat}")

#---------------------
#-------HANDLES-------
#---------------------
def handle_200():
    pass

def handle_201():
    print("\n=== JOGO INICIADO ===")
    printMy(me)
    print("--------------------------------")
    printEnemy(enemy)   # Apresentação do tabuleiro

def handle_202():
    print(enemyMap(enemy))  # Apresentação do tabuleiro
    play()              # Jogada do jogador

def handle_203(msg):
    select_boat(msg[4])

def handle_204(msg):
    global enemy

    enemy = msg[4:]
    print("CAMPO INIMIGO:")
    print(enemyMap(enemy))
    print("--------------------------------")

def handle_205(msg):
    global me

    me = msg[4:]
    print("SEU CAMPO:")
    print(myMap(me))
    print("--------------------------------")

def handle_206():
    result(msg[4:])

def handle_207():
    client.close()
    print("Desconectado.")

#EXECUÇÃO:

while True:

    msg = receive()

    match msg[0:3]:

        case "200":             # Servidor confirma conexão
            handle_200()

        case "201":             # Início do Jogo
           handle_201()

        case "202":             # Vez do Cliente jogar
            handle_202()
        
        case "203":             # O Server pede a alocação dos navios
            handle_203(msg)

        case "204":             # Jogo do adversário atualizado
            handle_204(msg)

        case "205":             # Atualização do tabuleiro
            handle_205(msg)

        case "206":             # Resultado da partida 
            handle_206(msg)

        case "207":             # Desconexão do Servidor 
            handle_207()
            break
        
        case _: 
            print("Mensagem inválida do servidor.")