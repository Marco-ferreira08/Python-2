""" Este programa permite visualizar algumas funcionalidades da biblioteca Rich do Python

    Sendo uma demostração da biblioteca Rich, para funcionar é necessário que essa esteja
baixada em sua máquina. Para isso digite o comando "pip install rich".
    Para acessar os recursos diponibilizados pelo prgrama é necessário digitar um comando
argparse que será detalhado abaixo:

    Exemplo de comando:
        python3 main.py "String" -a -m "Módulo" -f "Função"
    
    -a => Indica que a string passada é um caminho de arquivo, logo, caso não seja adi-
onado a estilização será aplicada deretamente sobre ela. Não necessita de argumento.

    -m => Junto a ele deve ser passado o módulo que deseja acessar, havendo 3: estilo, 
layout, painel e progresso. O módulo padrão acessado é "estilo".

    -f => Junto a ele dive ser passada a função que deseja acessar, a seguir serão indi-
cadas as funções pertecentes a cada módulo:

    --> estilo
        # text_color
        # background_color
    
    --> layout
        # one_column
        # two_column
    
    --> painel
        # panel_color
        # border_color
    
    --> Progresso
        # reading_arquive
        # loading_style

    A função padrão é text_color.
    Algumas funções pedirão que digite uma cor através de um input. Você pode passar
a cor que deseja de três formas: código hexadecimal = #FFFFFF (branco), rgb = 
rgb(255, 255, 255) (branco), color_tag = white (branco). No caso das color tags,
a biblioteca Rich tem 256 cores padrão nomeadas, você pode acessá-las através do 
link: https://rich.readthedocs.io/en/stable/appendix/colors.html#appendix-colors
"""

import argparse
import personalizador

# Criando parser

parser = argparse.ArgumentParser(
    prog="Leitor Dinâmico",
    description="O programa exibe de forma customizada o conteúdo de arquivos e strings, permitindo testar algumas estilizaçõs da biblioteca rich",
    )

parser.add_argument("filename", help="Caminho do arquivo ou string a ser imprimida")
parser.add_argument("-a", "--arquivo", action="store_true", 
                    help="Avisa que a string enviada é um caminho de arquivo")
parser.add_argument("-m", "--modulo", type=str, default="estilo", 
                    help="Módulo da função: estilo, layout, painel ou progresso")
parser.add_argument("-f", "--função", type=str, default="text_color",
    help="Função do módulo a ser acessada: estilo: text_color e background_color || layout: one_column e two_column || painel: panel_color e border_color || progresso: reading_arquive e loading_style")
args = parser.parse_args()

arquivo = args.filename
isArquivo = args.arquivo
modulo = args.modulo
funcao = args.função

size = 0
if isArquivo:
        with open(arquivo, "r")as fp:
            file = fp.read()
            for line in file:
                size += len(line)
else:
        size = len(arquivo)

if modulo == "estilo":

    if funcao == "text_color":

        personalizador.personalizador.progresso.reading_arquive(isArquivo, size)
        personalizador.estilo.text_color(isArquivo, arquivo)


    elif funcao == "background_color":

        personalizador.progresso.reading_arquive(isArquivo, size)
        personalizador.estilo.background_color(isArquivo, arquivo)


    else:

        print(f"A função {funcao} no modulo {modulo} não existe")


elif modulo == "layout":

    if funcao == "one_column":

        personalizador.progresso.reading_arquive(isArquivo, size)
        personalizador.layout.one_column(isArquivo, arquivo)


    elif funcao == "two_column":

        personalizador.progresso.reading_arquive(isArquivo, size)
        personalizador.layout.two_column(isArquivo, arquivo)


    else:

        print(f"A função {funcao} no modulo {modulo} não existe")


elif modulo == "painel":

    if funcao == "panel_color":

        personalizador.progresso.reading_arquive(isArquivo, size)
        personalizador.painel.panel_color(isArquivo, arquivo)


    elif funcao == "border_color":

        personalizador.progresso.reading_arquive(isArquivo, size)
        personalizador.painel.border_color(isArquivo, arquivo)


    else:

        print(f"A função {funcao} no modulo {modulo} não existe")


elif modulo == "progresso":

    if isArquivo:
        with open(arquivo) as file:
            text = file.read()
    else:
        text = arquivo
    
    if funcao == "reading_arquive":

        personalizador.progresso.reading_arquive(isArquivo, size)
        print(text)
    

    elif funcao == "loading_style":

        personalizador.progresso.loading_style(isArquivo)
        print(text)
    
    else:

        print(f"A função {funcao} no modulo {modulo} não existe")


else:
    
    print(f"O módulo {modulo} não existe")
