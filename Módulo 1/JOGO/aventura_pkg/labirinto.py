""" Aglutina funções relacionadas a dados e ações do labirinto

Necessita das seguintes bibliotecas e módulos:

    --> json - módulo nativo do python
    --> sleep - módulo nativo do python
    --> random - módulo nativo do python


Funções:

    --> salva_labirinto
    --> get_labirinto
    --> get_fim
    --> get_pontos
    --> gerar_labirinto
    --> gerar_pontos
    --> montar_labirinto
    --> imprimir_labirinto
"""

from json import dump, load
import random

# Funções referentes ao armazenamento de dados do Labirinto

def salva_labirinto(maze, pontos):
    """ Salva os dados do labirinto em um arquivo json (labirinto_data.json)

        Argumentos:

            - maze list() : lista de listas contendo o labirinto dividido em linhas
            - pontos list() : coordenadas de tesouros no labirinto
            
        A função cria um dicionário com os dados acima e escreve um arquivo json dentro
        da pasta data/dinamic, nomeado como labirinto_data.json. Ela tem um papel importante,
        já que o labirinto e a lista de pontos são constantemente atualizadas durante a
        execução do jogo.
    """
    dados = {"maze": maze, "pontos": pontos}

    with open("./data/dinamic/labirinto_data.json", "w") as file:
        dump(dados, file)

def get_labirinto():
    """ Abre o arquivo json do jogador e retorna o labirinto (maze list()) """

    with open("./data/dinamic/labirinto_data.json", "r") as file:
        return load(file)["maze"]

def get_fim():
    """ Retorna as coordenadas do canto inferior direito do labirinto, que é a saída 
    
        A função não requer argumentos, porém, é necessário que o arquivo labirinto_data.json
        exista e possua dados atualizados do labirinto.'
    """

    maze = get_labirinto()
    end_x = len(maze[0]) - 2
    end_y = len(maze) - 2

    return [end_x, end_y]

def get_pontos():
    """ Abre o arquivo json do jogador e retorna a lista de pontos (pontos list()) """

    with open("./data/dinamic/labirinto_data.json", "r") as file:
        return load(file)["pontos"]


# Funções avulsas

def gerar_labirinto(path):
    """ Lê um arquivo de texto que contenha um labirinto e retorna lista de listas do labirinto

        A função recebe path str() como argumento, que é o caminho do arquivo e retorna uma 
        lista de listas que representa o labirinto.

        Quando a função não encontra o arquivo, ela lê por padrão o labirinto_medio.txt o 
        qual está na pasta data/labirintos.
        
        A função lê a string do labirinto dentro do arquivo, quebra em linhas que são 
        adicionadas a uma lista. Depois cada linha é quebrada em uma lista de strings
        seguido uma lógica matemática, de modo que a cada 4 caracteres ela gera 2
        strings. Exemplo:

        Exemplo 1:
            string1 = "+---" => "+" e "---"
            string2 = "|   " => "|" e "   "

        Exemplo 2:
            string1 = "+---+---+   +" => "+", "---", "+", "---", "+", "   " e "+"
            string2 = "|   |       |" => "|", "   ", "|", "   ", " ", "   " e "|"

        Ela se comporta desse modo para separar as "paredes" do labrinto dos espaços
        em que o jogador pode "andar", além de separar as paredes horizontais das
        divisórias.
    """
    try:
        with open(path) as fp:
            lines = fp.readlines()
    except IOError:
        with open("./data/labirintos/labirinto_medio.txt") as fp:
            lines = fp.readlines()

    n = 0
    maze = []

    for line in lines:
        brokenLine = []
        for i in range(len(line.rstrip())):
            if i % 4 == 0:
                n = 0
                brokenLine.append(line[i])
            elif n == 1:
                n = 0
                brokenLine.append(line[i] * 3)
            elif line[i] == line[i - 1]:
                n +=1

        maze.append(brokenLine)

    return maze

def gerar_pontos(maze):
    """ Gera coordenadas de tesouros no labirinto dependendo de seu tamanho

        A função recebe um labirinto no formato de lista de listas e retorna outra lista 
        de listas, que contêm as coordenadas de tesouros no labirinto em questão.

        O número de tesouros gerados depende do tamanho do labirinto, sendo que esse número
        é resultado da divisão da área do labirinto (levando em consideração o número de 
        casas) por 25. Porém, cada labirinto tem que ter no mínimo 1 tesouro.

        Não podem ser gerados pontos no cando superior esquerdo nem no canto inferior
        direito, pois, essas são a posição inicial do jogador a posição da saída, 
        respectivamente
    """
    x = int((len(maze[0]) - 1) / 2)
    y = int((len(maze) - 1) / 2)
    maze_area = x * y
    end_x = len(maze[0]) - 2
    end_y = len(maze) - 2
    maze_end = [end_x, end_y]
    
    n = int(maze_area // 25 if maze_area >= 25 else 1)

    pontos = []

    for i in range(n):
        while True:
            px = random.randint(1, x) * 2 - 1
            py = random.randint(1, y) * 2 - 1

            if px % 2 == 0 or py % 2 == 0:
                continue

            ponto = [px, py]

            if (ponto != [1,1]) and (ponto != maze_end) and ponto not in pontos:
                break
        
        pontos.append(ponto)
    
    return pontos

def montar_labirinto(maze):
    """ Posiciona a saída e os tesouros do labirinto

        Recebe um labirinto no formato de lista de listas e retorna outra lista de listas
        do labirinto modificado.

        A função simplesmente coloca "[O]" na saída do labirinto e " $ " nas posições em
        que estão os tesouros.
    """


    end_x = len(maze[0]) - 2
    end_y = len(maze) - 2

    maze[end_y][end_x] = "[green][O][/]"

    pontos = gerar_pontos(maze)

    for ponto in pontos:
        x = ponto[0]
        y = ponto[1]

        maze[y][x] = "[yellow] $ [/]"
    
    return [maze, pontos]


def imprimir_labirinto(maze):
    """ Converte o labirinto em uma string

        A função recebe um labirinto em formato de lista de listas e retorna o mesmo em 
        formato de string, para que possa ser impresso na tela com facilidade.
    """

    maze_lines = []
    for line in maze:
            str_line = "".join(line) + "\n"
            maze_lines.append(str_line)
    
    return "".join(maze_lines)


    