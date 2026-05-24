import socket
from server_comm import server

# Endereço IP e porta utilizados pelo servidor.
HOST_IP = "127.0.0.1"
PORT = 12000

# Cliente
CLI_ACK = 100
CLI_HELLO = 101
CLI_SHOT = 102
CLI_PLACE = 103
CLI_DISCONNECT = 104

# Servidor
SRV_ACK = 200
SRV_START = 201
SRV_REQUEST_SHOT = 202
SRV_REQUEST_PLACE = 203
SRV_ENEMY_BOARD = 204
SRV_OWN_BOARD = 205
SRV_GAME_OVER = 206
SRV_DISCONNECT = 207

# Erros
ERR_INVALID_POSITION = 400
ERR_INVALID_FORMAT = 401
ERR_ALREADY_HIT = 402
ERR_GENERIC = 404

AGUA = 0
AGUA_ATACADA = 1

BARCO_INTACTO = 0
BARCO_ATACADO = 1
BARCO_DESTRUIDO = 2

ESTADO = 0
BARCO_ID = 1

TAM_BARCOS = [1,2,3,4]
N_BARCOS = 4

# Representação do campo do jogador 1 e 2.
# Valores possíveis:
# 0 -> neblina / mar não atacado
# 1 -> mar atacado
# Lista -> primeiro valor define o estado:
# 0 -> barco não atacado
# 1 -> barco atacado
# 2 -> barco destruído
# O segundo valor define qual barco pertence a casa:
# [0, ..., N_BARCOS]
campos: list[list[list[int] | int]] = [[AGUA,AGUA,AGUA,AGUA,
                                        AGUA,AGUA,AGUA,AGUA,
                                        AGUA,AGUA,AGUA,AGUA,
                                        AGUA,AGUA,AGUA,AGUA],
                                       [AGUA,AGUA,AGUA,AGUA,
                                        AGUA,AGUA,AGUA,AGUA,
                                        AGUA,AGUA,AGUA,AGUA,
                                        AGUA,AGUA,AGUA,AGUA]]


# Barcos alocados se refere a quantos
# barcos alocados já foram alocados para
# cada campo. barcos_alocados[0] representa
# jogador 1, barcos_alocados[1] representa o
# jogador 2
barcos_alocados = [0,0]

# Representação dos barcos já atacados de cada campo
# Definido como 4 barcos, ordenados por tamanho crescente
# de 1 até 4* (*por enquanto, harcoded)
barcos_atacados = [[0,0,0,0],[0,0,0,0]] 

# Para cada jogador, um dicionário que mapeia
# o id do barco (1, ..., 4) para a lista de índices
# que ele ocupa no tabuleiro.
posicoes_barcos = [{}, {}]

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

error_codes: dict[type[Exception], tuple[int, str]] = {
    # Exceções customizadas mapeadas para os erros de protocolo do cliente
    ForaDosLimitesError: (400, "Posição inválida"),
    FormatoError:        (401, "Formato inválido"),
    CasaInvalidaError:   (402, "Casa já atacada"),
    
    # Exceções da standard library
    KeyError:            (404, "Erro genérico / não especificado"),
    IndexError:          (404, "Erro genérico / não especificado"),
    TypeError:           (404, "Erro genérico / não especificado"),
    ValueError:          (404, "Erro genérico / não especificado")
}

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

def ehCasa(casa) -> bool:
    # Verifica se a mensagem possui dois caracteres.
    if len(casa) == 2:
        if casa[0].isalpha() and casa[1].isnumeric():
            return True

    return False

def calcularCasa(casa): 
    # Converte linha e coluna para índices numéricos.
    i = letra_to_numero(casa[0])
    j = int(casa[1])

    # Verifica se a linha está dentro dos limites.
    if i < 1 or i > 4:
        raise ForaDosLimitesError("Valor das linhas inválido")

    # Verifica se a coluna está dentro dos limites.
    if j < 1 or j > 4:
        raise ForaDosLimitesError("Valor das colunas inválido")

    # Converte coordenada 2D em índice linear do vetor.
    pos = 4*(i-1)+(j-1)

    return pos


def ehMesmaLinha(casas):
    if len(casas) != 2:
        raise FormatoError("Casas em excesso")

    casa1 = calcularCasa(casas[0])
    casa2 = calcularCasa(casas[1])

    if int((casa1 / 4)) == int((casa2 / 4)):
        return True

    return False


def ehMesmaColuna(casas):
    if len(casas) != 2:
        raise FormatoError("Casas em excesso")

    casa1 = calcularCasa(casas[0])
    casa2 = calcularCasa(casas[1])

    if (casa1 % 4) == (casa2 % 4):
        return True

    return False

def ehBarco(casa):
    if isinstance(casa, list):
        return True

    if isinstance(casa, int) and casa in (0, 1):
        return False

    return False

# Função que, ao exceder o limite
# de casas destruídas para um barco
# de dado tamanho, substitua os estados
# de cada barco com o identificador desse
# tamanho para 2
def destruir_barco(num_barco, jog1):
    i = int(not jog1)
    barco_id = num_barco + 1

    for pos in posicoes_barcos[i][barco_id]:
        campos[i][pos][0] = BARCO_DESTRUIDO

def processar_jogada(jogada: str, jog1: bool) -> bool | None:
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
        jogada: String recebida do cliente.
        jog1: Define qual campo será atacado.
              True  -> campo 1
              False -> campo 2

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
    jogada = jogada.lower().strip()


    # Verifica se o formato é letra+número.
    if ehCasa(jogada):

        pos = calcularCasa(jogada)
        i = int(not jog1)


        if not ehBarco(campos[i][pos]):
            # Água não descoberta.
            if campos[i][pos] == AGUA:
                campos[i][pos] = AGUA_ATACADA
                return False

        else:
            # Navio ainda não destruído.
            if campos[i][pos][ESTADO] == BARCO_INTACTO:
                campos[i][pos][ESTADO] = BARCO_ATACADO
                num_barco = campos[i][pos][BARCO_ID] - 1
                if barcos_atacados[i][num_barco] < TAM_BARCOS[num_barco]:
                    barcos_atacados[i][num_barco] += 1
                    if barcos_atacados[i][num_barco] == TAM_BARCOS[num_barco]:
                        destruir_barco(num_barco, jog1)
                return True

        # Caso a posição já tenha sido atacada.
        raise CasaInvalidaError(
            "Valor de casa inválido, pois já foi atacada"
        )

    # Caso o formato da mensagem seja inválido.
    raise FormatoError("Formato da mensagem inválido")

def processar_campo(barco: str, jog1: bool):
    i = int(not jog1)
    
    if barcos_alocados[i] >= N_BARCOS:
        return False
    
    casas = barco.split(' ')

    if not all(ehCasa(x) for x in casas):
        raise FormatoError("Formato das casas inválidos")

    if len(casas) == 1:
        pos = calcularCasa(casas[0])
        if not ehBarco(campos[i][pos]):
            campos[i][pos] = [BARCO_INTACTO, barcos_alocados[i]+1]
            barcos_alocados[i] += 1
            return True
        raise CasaInvalidaError("Barco já alocado para essa casa")


    idx_inicio = calcularCasa(casas[0])
    idx_fim = calcularCasa(casas[-1])

    inicio = min(idx_inicio, idx_fim)
    fim = max(idx_inicio, idx_fim)

    if ehMesmaLinha(casas):
        posicoes = list(range(inicio, fim + 1))
    elif ehMesmaColuna(casas):
        posicoes = list(range(inicio, fim + 1, 4))
    else:
        raise FormatoError("Casas não formam uma linha nem uma coluna")

    if any(campos[i][pos] != AGUA for pos in posicoes):
        raise CasaInvalidaError("Barco já alocado para alguma das casas")

    tam_esperado = TAM_BARCOS[barcos_alocados[i]]
    if len(posicoes) != tam_esperado:
        raise FormatoError("Tamanho do barco fora do tamanho esperado")

    barco_novo = [BARCO_INTACTO, barcos_alocados[i] + 1]
    for pos in posicoes:
        campos[i][pos] = list(barco_novo)

    barcos_alocados[i] += 1

    posicoes_barcos[i][barcos_alocados[i]] = posicoes.copy()


# Gera uma string generalista que 
# cria uma string com um return code
# e uma breve mensagem para ser enviada
# para o(s) cliente(s)
def gerar_msg(codigo: int, payload: str | None = None) -> str:
    if codigo in {101, 104, 200, 201, 202, 207}:
        if payload is not None:
            raise ValueError(f"Código {codigo} não aceita payload")
        return str(codigo)

    if codigo in {102, 103, 203, 204, 205, 206, 400, 401, 402, 404}:
        return f"{codigo} {payload}" if payload is not None else str(codigo)
    raise ValueError("Código desconhecido")

def gerar_erro(e: Exception) -> str:
    rc, msg = error_codes.get(type(e), (404, "Erro desconhecido"))
    return gerar_msg(rc, msg)

# O campo gerado dever conter apenas 5 estados:
# 0 -> mar não descoberto
# 1 -> mar descoberto
# 2 -> barco não descoberto
# 3 -> barco descoberto
# 4 -> barco destruído
def gerar_campo_str(campo):
    campo_gerado = []

    for casa in campo:
        if isinstance(casa, int):
            campo_gerado.append(str(casa))

        elif isinstance(casa, list):
            barco_estado = casa[ESTADO]

            if barco_estado == BARCO_INTACTO:
                campo_gerado.append("2")

            elif barco_estado == BARCO_ATACADO:
                campo_gerado.append("3")

            elif barco_estado == BARCO_DESTRUIDO:
                campo_gerado.append("4")

            else:
                raise ValueError("Estado do barco inválido")

        else:
            raise TypeError("Tipo de casa inválido")
    return ' '.join(campo_gerado)


# Usa a classe de comunicação para envio
# da mensagem
def enviar_msg(jog1: bool):
    pass

# O usuário também deve receber o 
# campo do adversário, mas sem saber
# onde estão os barcos
# Logo, os estados são:
# 0 -> mar não desoberto
# 1 -> mar descoberto
# 2 -> barco atacado
# 3 -> barco destruído
def mask_campo_str(campo):
    campo_list = campo.split()
    campo_convertido = []

    MAPA = {"0": "0",
            "1": "1",
            "2": "0",
            "3": "2",
            "4": "3"}

    for casa in campo_list:
        campo_convertido.append(MAPA[casa])

    return ' '.join(campo_convertido)

def recibe_code(msg):
    rc = msg[0:3]
    return int(rc)


if __name__ == "__main__":
    s = server(PORT)
    
    s.aceitar_conexao()

    txt = s.recibe_msg(0)
    code = recibe_code(txt)
    if code == CLI_HELLO:
        txt = gerar_msg(SRV_ACK)
        s.send_msg(0, txt)
    
    txt = s.recibe_msg(0)
    code = recibe_code(txt)

    s.aceitar_conexao()

    txt = s.recibe_msg(1)
    code = recibe_code(txt)

    if code == CLI_HELLO:
        txt = gerar_msg(SRV_ACK)
        s.send_msg(1, txt)

    txt = s.recibe_msg(1)
    flag = False
    
    jogador_atual = False
    acertou_navio_flag = True
    
    # Processamento do posicionamento dos barcos
    # do jogador 1
    for i in range(4):
        flag = True
        s.send_msg(0, gerar_msg(SRV_REQUEST_PLACE, str(barcos_alocados[jogador_atual] + 1)))
        txt = s.recibe_msg(0)
        code = recibe_code(txt)

        if code == CLI_PLACE:
            try:
                processar_campo(txt[4:], True)
            except Exception as e:
                flag = False
                print(e)
            

    s.send_msg(0, gerar_msg(SRV_OWN_BOARD, gerar_campo_str(campos[jogador_atual])))

    
    for i in range(4):
        flag = True
        s.send_msg(1, gerar_msg(SRV_REQUEST_PLACE, str(barcos_alocados[not jogador_atual] + 1)))
        txt = s.recibe_msg(1)
        code = recibe_code(txt)

        if code == CLI_PLACE:
            try:
                processar_campo(txt[4:], False)
            except Exception as e:
                flag = False
                print("oioioi")


    
    s.send_msg(1, gerar_msg(SRV_OWN_BOARD, gerar_campo_str(campos[not jogador_atual])))

    s.send_msg(0, gerar_msg(SRV_START))
    s.send_msg(1, gerar_msg(SRV_START))


    while True:
        s.send_msg(int(jogador_atual), gerar_msg(SRV_REQUEST_SHOT))
        txt = s.recibe_msg(int(jogador_atual))
        code = recibe_code(txt)
        if code == CLI_SHOT:
            try:
                acertou_navio_flag = processar_jogada(txt[4:], not jogador_atual)
            except Exception as e:
                print(e)
                
            campo_adv = gerar_campo_str(campos[int(jogador_atual)])
            s.send_msg(int(not jogador_atual), gerar_msg(SRV_OWN_BOARD, campo_adv))

            campo_adv = mask_campo_str(campo_adv)
            s.send_msg(jogador_atual, gerar_msg(SRV_ENEMY_BOARD, campo_adv))

            if not acertou_navio_flag:
                jogador_atual = not jogador_atual
                continue
            else:
                for i in range(4):
                    if not barcos_atacados[int(not jogador_atual)][i] == TAM_BARCOS[i]:
                        break
                break

    s.send_msg(jogador_atual, gerar_msg(SRV_GAME_OVER, "1"))
    txt = s.recibe_msg(jogador_atual)
    code = recibe_code(txt)

    if code == CLI_ACK:
        s.send_msg(jogador_atual, gerar_msg(SRV_DISCONNECT))
        if recibe_code(s.recibe_msg(jogador_atual)) == CLI_DISCONNECT:
            s.fechar_conexao_individual(s.get_port(jogador_atual))

    s.send_msg(not jogador_atual, gerar_msg(SRV_GAME_OVER, "0"))
    txt = s.recibe_msg(not jogador_atual)
    code = recibe_code(txt)

    if code == CLI_ACK:
        s.send_msg(not jogador_atual, gerar_msg(SRV_DISCONNECT))
        if recibe_code(s.recibe_msg(not jogador_atual)) == CLI_DISCONNECT:
            s.fechar_conexao_individual(s.get_port(not jogador_atual))

    s.fechar_conexao_geral()
    





    




