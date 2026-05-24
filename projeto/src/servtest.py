import socket

# =========================
# CONFIGURAÇÃO
# =========================

IP = "127.0.0.1"
PORT = 5000

# =========================
# SOCKET SERVIDOR
# =========================

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((IP, PORT))

server.listen(1)

print(f"Servidor iniciado em {IP}:{PORT}")
print("Esperando cliente conectar...\n")

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
# LOOP PRINCIPAL
# =========================

while True:

    print("\n==============================")
    print("Digite uma mensagem ao cliente")
    print("==============================")

    print("\nExemplos:")
    print("200")
    print("201")
    print("202")
    print("203 2")
    print("204 0000111100001111")
    print("205 2222000033330000")
    print("206 0/1")
    print("207")

    msg = input("\nMensagem: ")

    # envia pro cliente
    send(msg)

    print("\nMensagem enviada.")

    # =========================
    # recebe resposta do cliente
    # =========================

    codigo = msg[0:3]

    # cliente deve responder
    if codigo == "202" or codigo == "203":

        print("\nEsperando resposta do cliente...\n")

        resposta = receive()

        print(f"Cliente respondeu: {resposta}")

    # =========================
    # desconexão
    # =========================

    if codigo == "207":

        conn.close()

        server.close()

        print("\nServidor encerrado.")

        break