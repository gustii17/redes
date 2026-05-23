# =========================
# SIMULADOR OFFLINE CLIENTE
# =========================

enemy = "0000000000000000"
me    = "2222000000000000"

# ---------------------
# FUNÇÕES DO JOGO
# ---------------------

def myMap(s):

    slots_my = {
        "0": "~",
        "1": "o",
        "2": "B",
        "3": "X",
        "4": "#"
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
        "0": "~",
        "1": "o",
        "2": "X",
        "3": "#"
    }

    t = ["  1 2 3 4", "A", "B", "C", "D"]
    mapa = t[0]

    for i in range(4):

        sub_s = s[i*4 : (i+1)*4]
        sub_st = [slots_enemy[c] for c in sub_s]

        t[i+1] += " " + " ".join(sub_st)
        mapa += "\n" + t[i+1]

    return mapa


def printMy(m):

    print("\nSEU CAMPO:")
    print(myMap(m))


def printEnemy(m):

    print("\nCAMPO DO ADVERSÁRIO:")
    print(enemyMap(m))


def play():

    r = input("\nQual casa deseja atacar? ")
    print(f"\nVocê atacou: {r}")


def result(r):

    if r == "1/0":
        print("\nVocê perdeu!")

    elif r == "0/1":
        print("\nVocê venceu!")


def select_boat(n):

    boat = input(f"\nSelecione posições do navio {n}: ")
    print(f"\nNavio enviado: {boat}")


# ---------------------
# HANDLERS
# ---------------------

def handle_201():

    print("\n=== JOGO INICIADO ===")

    printMy(me)

    print("--------------------------------")

    printEnemy(enemy)


def handle_202():

    printEnemy(enemy)
    play()


def handle_203():

    select_boat("1")


def handle_204():

    global enemy

    enemy = "1000200030000000"

    print("\nMapa inimigo atualizado!")

    printEnemy(enemy)


def handle_205():

    global me

    me = "2222300000000000"

    print("\nSeu mapa atualizado!")

    printMy(me)


def handle_206():

    result("0/1")


def handle_207():

    print("\nDesconectado.")


# =========================
# LOOP OFFLINE
# =========================

while True:

    print("\n")
    print("201 -> iniciar jogo")
    print("202 -> jogar")
    print("203 -> posicionar barco")
    print("204 -> atualizar inimigo")
    print("205 -> atualizar jogador")
    print("206 -> resultado")
    print("207 -> sair")

    op = input("\nDigite código: ")

    match op:

        case "201":
            handle_201()

        case "202":
            handle_202()

        case "203":
            handle_203()

        case "204":
            handle_204()

        case "205":
            handle_205()

        case "206":
            handle_206()

        case "207":
            handle_207()
            break

        case _:
            print("\nCódigo inválido.")