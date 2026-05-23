import socket

# =========================
# CONFIGURAÇÃO
# =========================

IP = "127.0.0.1"
PORT = 5000

# =========================
# CRIAÇÃO DO SERVIDOR
# =========================

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((IP, PORT))

server.listen(1)

print(f"\nServidor iniciado em {IP}:{PORT}")
print("Aguardando conexão do cliente...\n")

# =========================
# ESPERA CONEXÃO
# =========================

conn, addr = server.accept()

print(f"Cliente conectado: {addr}")

# =========================
# FUNÇÕES
# =========================

def send(msg):

    conn.send(msg.encode())

def receive():

    msg = conn.recv(1024).decode()

    return msg

# =========================
# ESTADO DO JOGO
# =========================

enemy = "0000000000000000"
me    = "2222000000000000"

# =========================
# LOOP PRINCIPAL
# =========================

while True:

    print("\n========================")
    print("1 -> iniciar jogo")
    print("2 -> pedir jogada")
    print("3 -> pedir barcos")
    print("4 -> atualizar inimigo")
    print("5 -> atualizar jogador")
    print("6 -> vitória")
    print("7 -> derrota")
    print("0 -> desconectar")
    print("========================")

    op = input("\nEscolha: ")

    # -------------------------
    # 201 -> iniciar jogo
    # -------------------------

    if op == "1":

        send("201")

        print("\nMensagem 201 enviada.")

    # -------------------------
    # 202 -> pedir jogada
    # -------------------------

    elif op == "2":

        send("202")

        print("\nEsperando resposta do cliente...\n")

        resposta = receive()

        print(f"Recebido: {resposta}")

    # -------------------------
    # 203 -> pedir barcos
    # -------------------------

    elif op == "3":

        barco = input("\nNúmero do navio: ")

        send("203 " + barco)

        print("\nEsperando resposta do cliente...\n")

        resposta = receive()

        print(f"Recebido: {resposta}")

    # -------------------------
    # 204 -> atualizar inimigo
    # -------------------------

    elif op == "4":

        enemy = input("\nNovo mapa inimigo (16 chars): ")

        send("204 " + enemy)

        print("\nMapa inimigo enviado.")

    # -------------------------
    # 205 -> atualizar jogador
    # -------------------------

    elif op == "5":

        me = input("\nNovo mapa jogador (16 chars): ")

        send("205 " + me)

        print("\nMapa jogador enviado.")

    # -------------------------
    # 206 -> resultado
    # -------------------------

    elif op == "6":

        send("206 0/1")

        print("\nVitória enviada.")

    elif op == "7":

        send("206 1/0")

        print("\nDerrota enviada.")

    # -------------------------
    # 207 -> desconectar
    # -------------------------

    elif op == "0":

        send("207")

        conn.close()

        server.close()

        print("\nServidor encerrado.")

        break

    # -------------------------
    # inválido
    # -------------------------

    else:

        print("\nOpção inválida.")