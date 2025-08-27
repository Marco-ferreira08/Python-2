import argparse

from rich.layout import Layout
from rich.panel import Panel
from rich.live import Live
from rich.text import Text
from rich.align import Align
from pynput.keyboard import Listener

from aventura_pkg import jogador, labirinto, utils

parser = argparse.ArgumentParser()

parser.add_argument("filename", type=str,
                    help="Nome do arquivo de texto com o labirinto, o script busca os labirintos dentro da pasta aventura_no_labirinto/data/labirintos (não é necessário passar o caminho completo, apenas o nome)")

parser.add_argument("-d", "--demonstration", action="store_true",
                    help="Inidca que o jogo deve rodar no modo demonstração")

parser.add_argument("-c", "--color", default="white", type=str, 
                    help="Cor da interface do jogo")

parser.add_argument("-p", "--player", default=" X ", type=str,
                    help="Personagem do jogador, o qual pode ter 1 ou 3 caracteres")

parser.add_argument("-pc", "--player_color", default="white", type=str,
                    help="Cor do personagem do jogador seguindo as normas da biblioteca rich. Acesse https://rich.readthedocs.io/en/stable/style.html para mais informações.")

args = parser.parse_args()

if args.filename[-4::] == ".txt":
    maze_path = f"./data/labirintos/{args.filename}"

else:
    maze_path = f"./data/labirintos/{args.filename}.txt"


if len(args.player) == 1:
    character = " " + args.player + " "
elif len(args.player) == 3:
    character = args.player
else:
    character = " X "
character = f"[{args.player_color}]" + character + "[/]"

color = args.color
is_demonstration = args.demonstration


# Montagem do layout da tela
layout = Layout()

layout.split_column(
    Layout(name="header"),
    Layout(name="body")
)

layout["body"].split_row(
    Layout(name="aside"),
    Layout(name="main")
)

layout["header"].size = None
layout["body"].size = None
layout["aside"].size = None
layout["main"].size = None

layout["header"].ratio = 1
layout["body"].ratio = 9
layout["aside"].ratio = 2
layout["main"].ratio = 8

title = Text("Aventura no Labirinto", justify="center")
title.stylize("bold green")


layout["header"].update(Panel(title, style=color))
layout["main"].update(Panel(Align(utils.initial_screen(), vertical="middle", align="center"), style=color))

# Gerando labirnto
simple_maze = labirinto.gerar_labirinto(maze_path)

if is_demonstration:
    aside_text = "Aperte 'Ctrl + C' para sair"
    layout["aside"].update(Panel(Align(aside_text, vertical="middle", align="center"), style=color))
    with Live(auto_refresh=False) as live:
        utils.resolve_maze(simple_maze, [1,1], [], live, layout["main"], character, color)
    exit()

# Função que monta visualmente um menu e gerencia as interações com o mesmo (através do teclado)
def menu_inicial(live):
    global layout
    string_menu = "Menu de opções\n\n\n=> 1 - Jogar        <=\n\n=> 2 - Instruções   <=\n\n=> 0 - Sair         <=\n\n\nDigite o número da opção que deseja selecionar"
    text_menu = Text(string_menu, justify="center")

    layout["aside"].update(Panel(Align(text_menu, vertical="middle", align="center"), style=color))
    live.update(layout)
    live.refresh()

    # Função que rebebe a interação do teclado e processa qual ação tomar
    def menu(key):
        global acao
        try:
            # Pegando o código numérico da tecla
            opcao = key.vk

            match opcao:
                # Ao apertar a tecla 0
                case 48 | 96:
                    
                    acao = "sair"
                    return False

                # Ao apertar a tecla 1
                case 49 | 97:
                    acao = "jogar"
                    return False
                
                # Ao apertar a tecla 2
                case 50 | 98:
                    global layout
                    layout["main"].update(Panel(Align(utils.get_intrucoes(), vertical="middle", align="center"), style=color))
                    live.update(layout)
                    live.refresh()

                case outro:
                    live.refresh()

        except AttributeError: pass

        
    # Iniciando leitura do teclado
    with Listener(on_press=menu) as listener:
        try:
            listener.join()
        except AttributeError: pass


# Função que inicia o menu de "Jogar Novamente"
def menu_replay(live):
    global layout
    string_menu = "Gostaria de jogar novamente?\n\n\n=> 1 - Sim\n\n=> 2 - Não\n\n\nDigite o número da opção que deseja selecionar"
    text_menu = Text(string_menu, justify="center")
    text_menu.stylize("")

    layout["aside"].update(Panel(Align(text_menu, vertical="middle", align="center"), style=color))
    live.update(layout)
    live.refresh()

    def menu(key):
        global acao
        acao = "sair"

        try:
            opcao = key.vk

            match opcao:
                # Tecla 2
                case 50 | 98:
                    
                    acao = "sair"
                    return False

                # Tecla 1
                case 49 | 97:
                    acao = "jogar"
                    return False
                
        except AttributeError: pass


    with Listener(on_press=menu) as listener:
        try:
            listener.join()
        except AttributeError: pass  

# Função que inicia o jogo, mostrando o layout de forma dinâmica
def jogo(live):
    global layout

    # Montando labirinto
    maze_data = labirinto.montar_labirinto(simple_maze)

    # Iniciando jogador
    jogador.iniciar(maze_data[0], maze_data[1], character)

    # Função que atualiza o labirinto na tela
    def carrega_display(key):
        maze = labirinto.get_labirinto()
        maze_string = labirinto.imprimir_labirinto(maze)
        
        layout["main"].update(Panel(Align(maze_string, vertical="middle", align="center"), style=color))
        live.update(layout)
        live.refresh()

    # Preparando display para iniciar a gameplay
    maze = labirinto.get_labirinto()
    maze_string = labirinto.imprimir_labirinto(maze)

    string_menu = "Controles\n\n\nAndar:\n\n--> Cima =>     W\n--> Baixo =>    S\n--> Esquerda => A\n--> Direita =>  D\n\nSair => 'Esc'\n\nAo cheagar na saída ([O]) aperte 'Espaço'"
    text_menu = Text(string_menu, justify="center")
    text_menu.stylize("")

    layout["aside"].update(Panel(Align(text_menu, vertical="middle", align="center"), style=color))
    layout["main"].update(Panel(Align(maze_string, vertical="middle", align="center"), style=color))
    live.update(layout)
    live.refresh()


    # Iniando leitura do teclado, chamando a função para mover o jogador a atualizar a tela
    with Listener(on_press=jogador.mover, on_release=carrega_display) as listener:
        try:
            listener.join()
        except AttributeError: pass

    # Fim de jogo, pegando circustância em que o jogo acabou
    player_status = jogador.get_status()

    # Caso o jogador tiver ganhado, coloca tela de vitória
    if player_status == "win":
        win_screen = utils.win_screen(jogador.pontuar(True))
        layout["main"].update(Panel(Align(win_screen, vertical="middle", align="center"), style=color))
        
    # Caso o jogador tiver perdido, tela de derrota    
    elif player_status == "exit":
        end_screen = utils.end_screen()
        layout["main"].update(Panel(Align(end_screen, vertical="middle", align="center"), style=color))
    
    live.refresh()
    
    # Chamando menu de replay
    menu_replay(live)


    match acao:
        case "sair":
            exit()
        
        # Caso o jogador escolha para jogar novamente a função chama a si mesma para recomeçar
        case "jogar":
            jogo(live)


with Live(auto_refresh=False, screen=True) as live:
    acao = ""

    menu_inicial(live)

    match acao:
        case "sair":
            exit()

        case "jogar":
            jogo(live)