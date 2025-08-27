""" Este módulo possui funções que imprimem textos coloridos no terminal

    Este módulo e suas funções utilizam recursos da biblioteca Rich do Python, logo é
estritamente necessário que possua a biblioteca instalada em sua máquina.

    As funções do módulo rebebem uma string e um valor booleano que diz se a string é
o caminho de um arquivo o não. Primeiramente elas exigem do usuário uma cor através de
um input para pintar o texto ou o fundo do texto.

    Há duas funções disponíveis:
        
        --> text_color = pinta o texto
        --> background_color = pinta o fundo
"""

from personalizador import progresso
from rich.console import Console

console = Console()

def text_color(isArquivo, filename):

    """ Esta função pinta o texto recebido utilizando a biblioteca Rich do Python

        Para ela funcionar, precisa de dois argumentos iniciais: isArquivo (booleano)
    e filename (string). isArquivo é para dizer se a string recebida é um caminho de 
    arquivo ou apenas uma string qualquer. Caso seja um caminho de arquivo, a função
    lê o arquivo e aplica a estilização sobre o texto do arquivo.

        Quando executada ela exige que digite uma cor para pintar o texto, a cor pode 
    ser passada de três fomas: código hexadecimal, rgb e "color tag". A seguir tem 
    exemplos de sintaxe para cor branco para código hexadecimal, rgb e "color tag", 
    respectivamente: #ffffff, rgb(255, 255, 255), white. Na biblioteca rich há 256 
    cores padrão que são nomeadas com "color tag", para conhecê-las acesse o link 
    abaixo:

    https://rich.readthedocs.io/en/stable/appendix/colors.html

        A verdade é que esta função é simples e apenas solicita uma string como uma
    e aplica ela na propriedade style que vai estilizar o texto, logo, ao passar uma 
    cor que não existe na biblioteca rich ou passá-la com erro de sintaxeserá retornado 
    um erro da biblioteca Rich.
        Porém, isso também significa que, se você desejar, é possível aplicar outras 
    estilizações sobre o texto que não sejam a cor propriamente dita. Caso deseje 
    descobrir como estilizar o texto de outras formas digite:

    "python3 -m rich.default_styles"

    """

    color = input("Digite a cor que deseja pintar o texto: ")
    progresso.loading_style(isArquivo)
    if isArquivo:
        with open(filename, "r") as file:
            for line in file:
                console.print(line.rstrip(), style=color)
    else:
        console.print(filename, style=color)

def background_color(isArquivo, filename):

    """ Esta função pinta o fundo texto recebido utilizando a biblioteca Rich do Python

        Para ela funcionar, precisa de dois argumentos iniciais: isArquivo (booleano)
    e filename (string). isArquivo é para dizer se a string recebida é um caminho de 
    arquivo ou apenas uma string qualquer. Caso seja um caminho de arquivo, a função
    lê o arquivo e aplica a estilização sobre o texto do arquivo.

        Quando executada ela exige que digite uma cor para pintar o fundo, a cor pode 
    ser passada de três fomas: código hexadecimal, rgb e "color tag". A seguir tem 
    exemplos de sintaxe para cor branco para código hexadecimal, rgb e "color tag", 
    respectivamente: #ffffff, rgb(255, 255, 255), white. Na biblioteca rich há 256 
    cores padrão que são nomeadas com "color tag", para conhecê-las acesse o link 
    abaixo:

    https://rich.readthedocs.io/en/stable/appendix/colors.html

        Nesta função é necessário que passe apenas a cor que deseja pintar o fundo do
    texto, qualquer texto além traz grandes riscos da função não funcionar e retornar 
    um erro de sintaxe. Passar cores com sintaxe inadequada também retornará um erro.

    """

    color = input("Digite a cor que deseja pintar o texto: ")
    color = "on " + color
    progresso.loading_style(isArquivo)
    if isArquivo:
        with open(filename, "r") as file:
            for line in file:
                console.print(line.rstrip(), style=color)
    else:
        console.print(filename, style=color)