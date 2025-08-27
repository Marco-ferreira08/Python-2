""" Este módulo possui funções que mudam o layout de como strings e conteúdos de arquivos 
são impressos no terminal

    O módulo utiliza recursos da biblioteca Rich do Python, logo é estritamente necessário
que tenha a biblioteca instalada em sua máquina.

    Há duas funções neste módulo:
        --> one_column = imprime sua string ou texto de arquivo em uma coluna
        --> two_cloumn = imprime sua string ou texto de arquivo em duas colunas
"""


from rich import print
from rich.layout import Layout
from rich.panel import Panel
from personalizador import progresso

def one_column(isArquivo, filename):
    """ Esta função imprime a string recebida ou o texto do arquivo em coluna única

        A função recebe dois argumentos: isArquivo (booleano) filename (string). IsArquivo
    indica que a string recebida é um arquivo, para assim imprimir seu conteúdo em layout
    de uma coluna, além do seu caminho no topo dentro de um painel. Caso a string não seja
    indicada como caminho de arquivo, a função simplesmente a imprime dentro de um painel.

        ATENÇÃO: Não passe como argumento arquivos cujo conteúdo não caiba inteiro no terminal
    em tela cheia, caso contrário este será impresso de forma incompleta.
    
    """
    layout = Layout()
    progresso.loading_style(isArquivo)

    if isArquivo:
        file = open(filename, "r")
        reader = file.read()
        layout.split_column(
            Layout(name="header", ratio=1),
            Layout(name="body", ratio=9)
        )
        layout["header"].update(Panel(filename, height=3))
        layout["body"].update(reader)
        print(layout)
    else:
        layout.update(Panel(filename, height=3))
        print(layout)



def two_column(isArquivo, filename):
    """ Esta função imprime a string recebida ou  o texto do arquivo em duas colunas
    
        A função recebe dois argumentos: isArquivo (booleano) filename (string). IsArquivo
    indica que a string recebida é um arquivo, para assim imprimir seu conteúdo em layout
    de duas colunas, além do seu caminho no topo dentro de um painel. Caso a string não 
    seja indicada como caminho de arquivo, a função irá repartir a string em palavras,
    imprimindo metade das palavras na primeira coluna e metade na segunda.

        ATENÇÃO: Não passe como argumento arquivos cujo conteúdo não caiba inteiro no terminal
    em tela cheia, caso contrário este será impresso de forma incompleta e quebrada.
    """

    layout = Layout()
    painel = Panel(filename, height=3)
    progresso.loading_style(isArquivo)

    if isArquivo:
        file =open(filename, "r")
        lineList = file.readlines()

        lines_n = len(lineList)

        

        layout.split_column(
            Layout(name="header", ratio=1),
            Layout(name="body", ratio=9)
        )
        layout["header"].update(painel)

        if lines_n > 1:
            n = int(lines_n/2 if lines_n % 2 == 0 else lines_n//2 + 1)
            left_string = ""
            right_string = ""
        
            for i in range(n):
                left_string += lineList[i]
            for i in range(n, lines_n, 1):
                right_string += lineList[i]
            layout["body"].split_row(
                Layout(name="left"),
                Layout(name="right")
            )
            layout["left"].width = 10
            layout["right"].width = 10
            layout["left"].update(left_string)
            layout["right"].update(right_string)

        else:
            layout["body"].update(file.read())

        print(layout)

    else:

        wordList = filename.split(" ")

        words_n = len(wordList)

        if words_n > 1:

            n = int(words_n/2 if words_n % 2 == 0 else words_n//2 + 1)

            left_list = wordList[:n:]
            right_list = wordList[n::]

            left_string = " ".join(left_list)
            right_string = " ".join(right_list)

            layout.split_row(
                Layout(name="left"),
                Layout(name="right")
            )

            layout["left"].update(left_string)
            layout["right"].update(right_string)
            print(layout)
        
        else:
            painel
            layout.update(painel)
            print(layout)