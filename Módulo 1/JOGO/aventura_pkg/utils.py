""" Aglutina funções diversas utilizadas no jogo Aventura no Labirinto

Necessita das seguintes bibliotecas e módulos:

    --> sleep - biclioteca nativa do python
    --> rich - biblioteca externa para estilização do terminal (pip  install rich)
    --> labirinto - módulo do pacote aventura_pkg como o próprio utils


Funções:

    --> win_screen
    --> end_screen
    --> initial_screen
    --> get_instrucoes
    --> resolve_maze
"""



from time import sleep

from rich.layout import Layout
from rich.panel import Panel
from rich.live import Live
from rich.align import Align

from aventura_pkg import labirinto

def win_screen(score):
    """ Retorna a tela de vitória do jogo
    
        A função recebe como argumento a pontuação do jogador int() e retorna a tela de 
        vitória com a pontuação str()

        A tela em si está armazenada no arquivo win.txt na pasta data/screens, a função
        apenas adiciona a pontuação retorna a nova string.
    """

    with open("./data/screens/win.txt") as file:
        screen = "".join([
            "[yellow]", 
            file.read(), 
            "\n[green bold]Parabéns! \nVocê saiu do labirinto!",
            f"\n\n[yellow]Sua pontuação =[/] {score}"
            ])
    return screen


def end_screen():
    """ Retorna a tela de derrota do jogo
    
        A função lê o arquivo game-over.txt na pasta data/screens e retorna o seu
        conteúdo (a tela de game over) em forma de sting
    """

    with open("./data/screens/game-over.txt") as file:
        screen = "".join([
            "[purple]", 
            file.read(),
            "\n\n[red bold]Game Over! \nVocê saiu da partida"
            ])
    return screen

def initial_screen():
    """ Retorna a tela inicial do jogo
    
        A função lê o arquivo menu.txt na pasta data/screens e retorna o seu
        conteúdo (a tela do menu) em forma de sting
    """

    with open("./data/screens/menu.txt") as file:
        return file.read()

def get_intrucoes():
    """ Retorna as intruções do jogo
    
        A função lê o arquivo instrucoes.txt na pasta data/screens e retorna o seu
        conteúdo em forma de string.
    """
    with open("./data/screens/instrucoes.txt", encoding="utf-8") as file:
        return file.read()

def resolve_maze(maze, position, past_list, live, layout, character, color):
    """ Algorítimo de árvore que anda por todo o labirinto testando todos os caminhos

        Argumentos:
            - maze list() : lista de listas do labirinto

            - position list() : coordenadas atuais do algorítimo

            - past_list list() : lista de posições pelas quais o algorítmo já passou

            - live Live() : live display em execução oriundo da biblioteca rich.
                Acesse https://rich.readthedocs.io/en/stable/live.html para mais informações

            - layout Layout() : layout do terminal oriundo da biblioteca rich.
                Acesse https://rich.readthedocs.io/en/stable/layout.html para mais informações

            - character str() : personagem que será exibido se movendo pelo labirinto. Pode
                conter 1 ou três caracteres

            - color str() : string que contém estilização nas normas da biblioteca Rich.
                Acesse https://rich.readthedocs.io/en/stable/style.html para mis informações

        ALERTA! Para que esta função funcione é necessário passar o objeto Live() do live
        display em execução. Além disso, o layout passado como argumento deve conter a 
        subdivisão "main".

        A função verifica se ela pode mover-se para cima, para esquerda, para baixo ou para
        a direita. Essa verificação leva em conta paredes no labirinto e se ela já passou 
        por aquela posição. Ao indentificar que é possível mover-se para aquela direção
        ela chama a si mesma e repete o processo.

        Quando é identificado que não é possível ir para nenhuma direção ela termina e a
        função anterior verifica a póxima direção. Devido a esses fatores ela caracteriza-se
        como uma função recursiva.
    """

    x = position[0]
    y = position[1]

    maze[y][x] = character
    maze_string = labirinto.imprimir_labirinto(maze)
    layout["main"].update(Panel(Align(maze_string, vertical="middle", align="center"),style=color))
    live.update(layout)
    live.refresh()

    def callback(direction):
        past_list.append(position)
        maze[y][x] = "   "

        sleep(0.8)
        resolve_maze(maze, direction, past_list, live, layout, character, color)
        sleep(0.8)

        dx = direction[0]
        dy = direction[1]

        maze[y][x] = character
        maze[dy][dx] = "   "
        maze_string = labirinto.imprimir_labirinto(maze)
        layout["main"].update(Panel(Align(maze_string, vertical="middle", align="center"),style=color))
        live.update(layout)
        live.refresh()

    up = [x, y - 2]
    right = [x + 2, y]
    down = [x, y + 2]
    left = [x - 2, y]

    if maze[y - 1][x] == "   " and up not in past_list:
        callback(up)
    
    if maze[y][x - 1] == " " and left not in past_list:
        callback(left)

    if maze[y + 1][x] == "   " and down not in past_list:
        callback(down)

    if maze[y][x + 1] == " " and right not in past_list:
        callback(right)
