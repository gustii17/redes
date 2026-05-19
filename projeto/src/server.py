import socket

# Endereço IP e porta utilizados pelo servidor.
HOST_IP = "127.0.0.1"
PORT = 61432

# Representação do campo do jogador 1.
# Valores possíveis:
# 0 -> água / vazio
# 1 -> navio presente
# 2 -> posição já atacada
campo1 = [0,0,0,1,
          0,0,0,0,
          0,0,0,0,
          0,0,0,0]

# Representação do campo do jogador 2.
campo2 = [0,0,0,0,
          0,0,0,0,
          0,0,0,0,
          0,0,0,0]


# Exceção utilizada quando a jogada possui
# coordenadas fora dos limites do tabuleiro.
class ForaDosLimitesError(Exception):
    pass


# Exceção utilizada quando a mensagem recebida
# não segue o formato esperado.
class FormatoError(Exception):
    pass


# Exceção utilizada quando o jogador tenta
# atacar uma posição já destruída anteriormente.
class CasaInvalidaError(Exception):
    pass


def letra_to_numero(letra) -> int:
    """
    Converte uma letra minúscula em um número.

    Exemplos:
        a -> 1
        b -> 2
        d -> 4

    Args:
        letra: Letra minúscula representando a linha.

    Returns:
        Valor numérico correspondente à letra.
    """

    return ord(letra) - ord('a') + 1


def sock_init(s: socket.socket):
    """
    Inicializa o socket do servidor.

    A função realiza:
    - bind do IP e porta definidos globalmente
    - entrada em modo de escuta

    Args:
        s: Socket TCP já criado.
    """

    s.bind((HOST_IP, PORT))
    s.listen(8)


def processar_jogada(data: str, jog1: bool) -> bool | None:
    """
    Processa uma jogada recebida de um cliente.

    O formato esperado da jogada é:
        <linha><coluna>

    Exemplo:
        d2

    Onde:
        - a-d representam as linhas
        - 1-4 representam as colunas

    A função valida:
        - tamanho da mensagem
        - formato da coordenada
        - limites do tabuleiro
        - se a casa já foi atacada

    Args:
        data: String recebida do cliente.
        jog1: Define qual campo será atacado.
              True  -> campo1
              False -> campo2

    Returns:
        True  -> ataque acertou um navio
        False -> ataque caiu na água

    Raises:
        FormatoError:
            Mensagem inválida ou fora do padrão esperado.

        ForaDosLimitesError:
            Coordenadas fora dos limites do tabuleiro.

        CasaInvalidaError:
            Posição já atacada anteriormente.
    """

    # Remove espaços extras e converte a mensagem para minúsculo.
    data = data.lower().strip()

    # Verifica se a mensagem possui ao menos dois caracteres.
    if len(data) < 2:
        raise FormatoError("Mensagem curta")

    # Verifica se o formato é letra+número.
    if data[0].isalpha() and data[1].isnumeric():

        # Converte linha e coluna para índices numéricos.
        i = letra_to_numero(data[0])
        j = int(data[1])

        # Verifica se a linha está dentro dos limites.
        if i < 1 or i > 4:
            raise ForaDosLimitesError("Valor das linhas inválido")

        # Verifica se a coluna está dentro dos limites.
        if j < 1 or j > 4:
            raise ForaDosLimitesError("Valor das colunas inválido")

        # Converte coordenada 2D em índice linear do vetor.
        pos = 4*(i-1)+(j-1)

        # Processamento do ataque no campo do jogador 1.
        if jog1:

            # Água.
            if campo1[pos] == 0:
                return False

            # Navio ainda não destruído.
            if campo1[pos] != 2:
                campo1[pos] = 2
                return True

        # Processamento do ataque no campo do jogador 2.
        else:

            # Água.
            if campo2[pos] == 0:
                return False

            # Navio ainda não destruído.
            if campo2[pos] != 2:
                campo2[pos] = 2
                return True

        # Caso a posição já tenha sido atacada.
        raise CasaInvalidaError(
            "Valor de casa inválido, pois já foi atacada"
        )

    # Caso o formato da mensagem seja inválido.
    raise FormatoError("Formato da mensagem inválido")


# ==========================================================
# Código de teste do servidor.
# ==========================================================

# Criação do socket TCP IPv4.
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

    # Inicializa o socket do servidor.
    sock_init(s)

    # Aguarda conexão de um cliente.
    player1, player1_addr = s.accept()

    # Context manager para fechamento automático da conexão.
    with player1:

        print(f"Conectado por {player1}")

        # Recebe até 1024 bytes do cliente.
        data = player1.recv(1024)

        try:
            # Processa a jogada recebida.
            processar_jogada(data.decode(), True)

        except ForaDosLimitesError as e:

            print("""Jogada com limites errados.
Os limites são:
- a-d (linha)
- 1-4 (coluna)

Exemplo: d2""")

        except CasaInvalidaError as e:

            print(
                "A casa selecionada já foi destruída. "
                "Por favor, selecione outra casa."
            )

        except FormatoError as e:

            print(
                "Formato da mensagem errado. "
                "Por favor, jogue novamente. Exemplo: d2"
            )

        # Exibe o estado final do campo.
        print(campo1)
