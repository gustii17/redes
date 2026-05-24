import socket      # Biblioteca socket para implementação  
from ClientClass import client #importando a classe

#----------------------------
#---FUNÇÕES DE COMUNICAÇÃO---
#----------------------------

#Ip e Porta
IP = "127.0.1.1"
PORT = 12000

cliente = client()
cliente.conectar(IP,PORT)   # Conexão com o socket do servidor
cliente.send_msg("101")

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

def printId():
    print("Identificação:")
    print("~  Água desconhecida\no  Tiro na água\nB  Barco intacto\nX  Acerto\n#  Navio afundado\n")

def printMy(m):
    print("SEU CAMPO:")
    print(myMap(m))

def printEnemy(m):
    print("CAMPO DO INIMIGO:\n")
    print(enemyMap(m))

def valid_house(pos):

    pos = pos.lower()

    if len(pos) != 2:
        return False
    
    letra = pos[0]
    numero = pos[1]

    if letra not in "abcd":
        return False
    if numero not in "1234":
        return False

    return True

def play():
    while True:
        r = input("\nQual casa deseja atacar? ")

        if valid_house(r):
            cliente.send_msg("102 " + r)
            print(f"\nVocê atacou: {r}")
            break
        
        print("Posição inválida.Tente novamente. Ex: a1,c4,b2")

def select_boat(n):

    n = int(n)

    while True:

        boat = input(f"\nSelecione posições do navio {n}: ").lower()

        casas = boat.split()

        if n == 1:
            if len(casas) != 1:
                print("Digite apenas uma casa. Ex: a1, b2, c3")
                continue

            if not valid_house(casas[0]):
                print("Casa inválida.")
                continue

        else:
            if len(casas) != 2:
                print("Digite posição inicial e final. Ex: a1 a3")
                continue

            if not valid_house(casas[0]):
                print("Casa inicial inválida.")
                continue

            if not valid_house(casas[1]):
                print("Casa final inválida.")
                continue

        cliente.send_msg("103 " + boat)
        print(f"Navio {n} nas posições {boat}")
        break  

def result(r):
    if r == "0":
        print("Você perdeu!:(")

    elif r == "1":
        print("Parabéns! Você venceu! :)")

#---------------------
#-------HANDLES-------
#---------------------
def handle_200():
    cliente.send_msg("100")
    print("Aguardando o início do jogo...")

def handle_201():
    print("\n=== JOGO INICIADO ===")
    printId()
    printMy(me)
    print("--------------------------------")
    printEnemy(enemy)   # Apresentação do tabuleiro

def handle_202(): #colocar a verificação de jogada letra:numero
    play()              # Jogada do jogador

def handle_203(msg): #colocar a verificação de jogada letra:numero
    try:
        n = msg[4]
        select_boat(n)

    except:
        print("Mensagem inválida do server. Cod:203 error")

def handle_204(msg):
    global enemy

    enemy = msg[4:]
    print("CAMPO DO INIMIGO:")
    print(enemyMap(enemy))  # Apresentação do tabuleiro

def handle_205(msg):
    global me

    me = msg[4:]
    print("SEU CAMPO:")
    print(myMap(me  ))  # Apresentação do tabuleiro    

def handle_206(msg):
    result(msg[4:])

def handle_207():
    cliente.send_msg("104")
    cliente.desconectar()
    print("Desconectado.")

#EXECUÇÃO:

while True:

    msg = cliente.recibe_msg() #203 0101010101010101
    msg = msg[:4] + msg[4:].replace(" ", "")
    
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
