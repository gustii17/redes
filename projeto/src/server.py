import socket

HOST_IP = "127.0.0.1"
PORT = 61432

campo1 = [0,0,0,1,
          0,0,0,0,
          0,0,0,0,
          0,0,0,0]

campo2 = [0,0,0,0,
          0,0,0,0,
          0,0,0,0,
          0,0,0,0]

class ForaDosLimitesError(Exception):
    pass

class FormatoError(Exception):
    pass

class CasaInvalidaError(Exception):
    pass

def letra_to_numero(letra) -> int:
    return ord(letra) - ord('a') + 1

def sock_init(s: socket.socket):
    s.bind((HOST_IP, PORT))
    s.listen(8)

def processar_jogada(data: str, jog1: bool) -> bool | None:
    data = data.lower().strip()

    if len(data) < 2:
        raise FormatoError("Mensagem curta")

    if data[0].isalpha() and data[1].isnumeric():
        i = letra_to_numero(data[0])
        j = int(data[1])
        
        if i < 1 or i > 4:
            raise ForaDosLimitesError("Valor das linhas inválido")
        if j < 1 or j > 4:
            raise ForaDosLimitesError("Valor das colunas inválido")
        pos = 4*(i-1)+(j-1)
        
        if jog1:
            if campo1[pos] == 0:
                return False
            if campo1[pos] != 2:
                campo1[pos] = 2
                return True
        else:
            if campo2[pos] == 0:
                return False
            if campo2[pos] != 2:
                campo2[pos] = 2
                return True

        raise CasaInvalidaError("Valor de casa inválido, pois já foi atacada")

    raise FormatoError("Formato da mensagem inválido")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    sock_init(s)
    player1, player1_addr = s.accept()
    with player1:
        print(f"Conectado por {player1}")
        data = player1.recv(1024)

        try:
            processar_jogada(data.decode(), True)

        except ForaDosLimitesError as e:
            print("""Jogada com limites errados. Os limites são: a-d (linha) e 1-4 (coluna).\n
                  Exemplo: d2""")
        except CasaInvalidaError as e:
            print("A casa selecionada já foi destruída. Por favor, selecione outra casa.")
        except FormatoError as e:
            print("Formato da mensagem errado. Por favor, jogue novamente. Exemplo: d2")

        print(campo1)

