"""Este módulo possui funções que imprimem textos e conteúdos de arquivos em paineis coloridos

    O módulo utiliza recursos da biblioteca Rich do Python, logo é estritamente necessário
que tenha a biblioteca instalada em sua máquina.

    Há duas funções neste módulo:
        --> panel_color = imprime o texto ou conteúdo de arquivo em um painel colorido
        --> boder_color = imprime o texto ou conteúdo de arquivo em um painel com borda colorida

"""

from rich import print
from rich.panel import Panel
from personalizador import progresso

def panel_color(isArquivo, filename):
    """ Esta função imprime uma string ou conteúdo de arquivo em um painel com texto e borda coloridos

        A função recebe dois argumentos: isArquivo (booleano) filename (string). IsArquivo
    indica que a string recebida é um arquivo, assim o conteúdo do arquivo é impresso é
    impresso dentro do painel e seu caminho/nome é impresso no topo do painel. Caso o texto
    recebido seja uma string qualquer ela é impressa dentro do painel.

        Quando executada a função solicita, através de um input, a cor que deseja pintar o
    texto e a borda do painel. A cor pode ser passada por meio de código hexadecimal, rgb
    ou "color tag". A seguir temos um exemplo de cada uma das três forma, respectivamente, 
    para a cor branco:
    #ffffff, rgb(255, 255, 255), white

        A biblioteca Rich possui 256 cores padrão nomeadas com "color tag", você pode
    acessá-las pelo link abaixo:

    https://rich.readthedocs.io/en/stable/appendix/colors.html

        Esta é uma função simples, que apenas aplica a cor solicitada como propriedade
    style do painel. Isso significa que você pode passar outros tipos de estilizações
    além das cores para personalizar o painel. Caso queira conhecer outras formas de
    estilizar a saída da função, digite o seguinte comando no terminal:

    python3 -m rich.default_styles

    """
    color = str(input("Digite uma cor para pintar a o texto e borda do painel: "))
    progresso.loading_style(isArquivo)

    if isArquivo:
        with open(filename, "r") as file:
            reader = file.read()
            painel = Panel(
                reader,
                title=filename,
                style=color
            )
        print(painel)

    else:
        painel = Panel(
            filename,
            style=color
        )
        print(painel)

def border_color(isArquivo, filename):
    """ Esta função imprime uma string ou conteúdo de arquivo em um painel com borda colorida

        A função recebe dois argumentos: isArquivo (booleano) filename (string). IsArquivo
    indica que a string recebida é um arquivo, assim o conteúdo do arquivo é impresso é
    impresso dentro do painel e seu caminho/nome é impresso no topo do painel. Caso o texto
    recebido seja uma string qualquer ela será impressa diretamente dentro do painel.

        Quando executada a função solicita, através de um input, a cor que deseja pintar o
    texto e a borda do painel. A cor pode ser passada por meio de código hexadecimal, rgb
    ou "color tag". A seguir temos um exemplo de cada uma das três forma, respectivamente, 
    para a cor branco:
    #ffffff, rgb(255, 255, 255), white

        A biblioteca Rich possui 256 cores padrão nomeadas com "color tag", você pode
    acessá-las pelo link abaixo:

    https://rich.readthedocs.io/en/stable/appendix/colors.html

        Esta é uma função simples, que apenas aplica a cor solicitada como propriedade
    style do painel. Isso significa que você pode passar outros tipos de estilizações
    além das cores para personalizar o borda. Caso queira conhecer outras formas de
    estilizar a saída da função, digite o seguinte comando no terminal:

    python3 -m rich.default_styles

    """

    color = str(input("Digite uma cor para pintar a borda do painel: "))

    if isArquivo:
        with open(filename, "r") as file:
            reader = file.read()
            painel = Panel(
                reader,
                title=filename,
                border_style=color
            )
        print(painel)

    else:
        painel = Panel(
            filename,
            border_style=color
        )
        print(painel)