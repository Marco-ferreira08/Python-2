""" Aglutina funções relacionadas a dados e ações do jogador

Necessita das seguintes bibliotecas e módulos:

    --> json - biblioteca nativa do python
    --> pynput - biblioteca externa para leitura do teclado (pip install pynput)
    --> labirinto - módulo do pacote aventura_pkg como o próprio módulo jogador


Funções:

    --> salva_jogador
    --> get_character
    --> get_position
    --> get_status
    --> get_steps
    --> get_score
    --> iniciar
    --> pontuar
    --> mover 
"""

import json

from pynput import keyboard

from aventura_pkg import labirinto



# Funções referentes ao armazenamento de dados do jogador

def salva_jogador(character, position, steps, score, status="in_game"):
    """ Salva os dados do jogador em um arquivo json (player_data.json)

        Argumentos:

            - character str() : personagem do jogador, o qual contém 1 ou três caracteres
            - position list() : coordenadas do jogador no labirinto, representadas por uma 
                lista de dois números int()
            - steps int() : número de passos dados pelo jogador no labirinto
            - score int() : pontuação do jogador
            - status str() (opcional = 'in_game') : estado do jogador que varia entre win,
                exit e in_game
            
        A função cria um dicionário com os dados acima e escreve um arquivo json dentro
        da pasta data/dinamic, nomeado como player_data.json
    """

    dados = {
        "character" : character,
        "player_position": position, 
        "steps_n": steps, 
        "score": score, 
        "player_status": status
        }

    with open("./data/dinamic/player_data.json", "w") as file:
        json.dump(dados, file)

def get_character():
    """ Abre o arquivo json do jogador e retorna o personagem (character str()) """

    with open("./data/dinamic/player_data.json", "r") as file:
            return json.load(file)["character"]

def get_position():
    """ Abre o arquivo json do jogador e retorna suas coordenadas (position list()) """

    with open("./data/dinamic/player_data.json", "r") as file:
        return json.load(file)["player_position"]

def get_status():
    """ Abre o arquivo json do jogador e retorna o seu status (status str()) """

    with open("./data/dinamic/player_data.json", "r") as file:
        return json.load(file)["player_status"]

def get_steps():
    """ Abre o arquivo json do jogador e retorna o número de passos (steps int()) """

    with open("./data/dinamic/player_data.json", "r") as file:
        return json.load(file)["steps_n"]

def get_score():
    """ Abre o arquivo json do jogador e retorna a pontuação (score int()) """

    with open("./data/dinamic/player_data.json", "r") as file:
        return json.load(file)["score"]


def iniciar(maze, pontos, character):
    """ Posiciona o jogador no início do labirinto e salva os seus e os dados do labirinto

        Argumentos:

            - maze list() : lista de listas contendo o labirinto
            - pontos list() : lista de listas contendo coordenadas de tesouros no labirinto
            - character str() : personagem do jogador

        A função coloca o personagem do jogador jo canto superior esquerdo do labirinto,
        além disso, salva os dados do jogador, iniciando seus passos e pontuação como 0
        e sua posição/coordenadas como [1, 1]. Como ele modifica o labirinto posicionando
        o personagem, a função também o salva, passando o labirinto modificado e os pontos
        como argumentos
    """

    maze[1][1] = character
    salva_jogador(character, [1,1], 0, 0) # Dados do jogador
    labirinto.salva_labirinto(maze, pontos)

def pontuar(isEnd = False):
    """ Retorna a pontuação do jogador após coletar um tesouro ou escapar do labirinto

        Parâmetro:
            - isEnd bool() (opcional = False) : indicativo se a função deve calcular a 
            pontuação final do jogador

        Quando o valor isEnd é False, significa que o jogador apenas coletou um tesouro,
        logo, a função simplesmente retorna a pontuação atual do jogador somada a 500.

        Quando o valor isEnd é True, significa que o jogador escapou do labirinto. Assim
        é feito um cálculo em cima do tamanho da área do labirinto e o número de passos
        dados pelo jogador, de modo que, quanto mais passos, menor é a pontuação. Então
        a função retorna esse valor calculado somado à pontuação do jogador.
    """


    if isEnd:
        steps = get_steps()
        maze = labirinto.get_labirinto()

        # Verifica o tamanho do labirinto ignorando as "paredes"
        x = len(maze[0]) // 2
        y = len(maze) // 2

        # Calcula a área do labirinto multiplicada por 5
        maze_score = (x * y) * 5
        
        # Divide a área elo número de passos do jogador e múltiplica por 100
        # para que a pontuação possua 2 zeros
        score = maze_score // steps if steps > 0 else 0
        score *= 100

        # Por fim retorna esse valor calculado somado à pontuação do jogador
        return int(score + get_score())
    else:
        return int(get_score() + 500)

def mover(key):
    """ Move o jogador pelo labirinto verificando se ele coletou um tesouro ou se conseguiu escapar
    
        Argumento:

            - key pynput.keyboard.Key() ou pynput.keyboard.KeyCode() : tecla pressionada
            pelo jogador, podendo ser uma tecla de texto (KeyCode()) ou uma tecla especial (Key()) 
    
        A função verifica se a tecla pressionada pelo jogador (a qual é recebida como 
        argumento) é uma das tecla direcionais (wasd) ou se é uma das teclas com funções
        especiais no jogo, como o Esc, que faz o jogador sair da partida, ou o espaço,
        o qual faz o jogador sair do labirinto caso o mesmo esteja na saída.

        Sempre que o jogador aperta uma tecla direcional, a função posiciona o seu personagem
        na nova posição e o remove da função anterior. Em seguida ela salva seus novos dados,
        como número de passos e coordenadas. Ela também verifica se o jogador está na mesma
        posição de que algum tesouro, atualizando sua pontuação e removendo-o da lista de
        tesouros a serem coletados.
    """

    # Dados do labirinto
    maze = labirinto.get_labirinto()
    maze_end = labirinto.get_fim()
    pontos = labirinto.get_pontos()

    # Dados do jogador
    character = get_character()
    steps = get_steps()
    player_position = get_position()
    initial_score = get_score()
    x = player_position[0]
    y = player_position[1]


    # If/Else que lê o teclado do jogador

    try:

        if key == keyboard.Key.space and player_position == maze_end:
            final_score = pontuar(isEnd=True)
            salva_jogador(character, player_position, steps, score=final_score, status="win")
            labirinto.salva_labirinto(maze, pontos)

            return False

        elif key == keyboard.Key.esc:
            # Caso apert esc, o jogador sai do jogo
            salva_jogador(character, player_position, steps, 0, status="exit")
            labirinto.salva_labirinto(maze, pontos)

            return False

        elif key.char == "w" and maze[y - 1][x] != "---":
            new_position = [x, y - 2]
            steps += 1
            
        elif key.char == "s" and maze[y + 1][x] != "---":
            new_position = [x, y + 2]
            steps += 1

        elif key.char == "a" and maze[y][x - 1] != "|":
            new_position = [x - 2, y]
            steps += 1


        elif key.char == "d" and maze[y][x + 1] != "|":
            new_position = [x + 2, y]
            steps += 1

        else:
            new_position = player_position
    
    except AttributeError: new_position = player_position
    
    x1 = new_position[0]
    y1 = new_position[1]


    maze[y][x] = "[O]" if player_position == maze_end else "   "
    maze[y1][x1] = character

    if new_position in pontos:
        pontos.remove(new_position)

        score = pontuar()
        salva_jogador(character, new_position, steps, score)
    else:
        salva_jogador(character, new_position,steps, initial_score)
    labirinto.salva_labirinto(maze, pontos)