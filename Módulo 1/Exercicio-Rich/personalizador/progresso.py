""" Este módulo possuem funções simulam barra e animação de carregamento no terminal

    O módulo utiliza recursos da biblioteca Rich do Python, logo é estritamente necessário
que tenha a biblioteca instalada em sua máquina.

    Há duas funções neste módulo:
        --> reading_arquive = gera uma barra de carregamento que simula uma leitura de arquivo
        --> loading_style = gera uma animação de carregamento que simular a rederização de estilos
"""

from time import sleep
from rich import print
from rich.progress import Progress
from rich.console import Console

def reading_arquive(isArquivo, size):
    """ Esta função gera uma barra de carregamento simulando uma leitura de arquivo

        A função recebe dois argumentos: isArquivo (booleano) e size (int). "isArquivo" 
    indica se esta sendo feita uma "leitura" de um arquivo ou de uma string, mudando as 
    mensagens exibidas, e a velociadade em que é feita a "leitura", já que arquivos 
    costuman ser muito mais pesados que strings. "size" indica o tamanho do arquivo em 
    bytes e influencia diretamente no tempo que a "leitura" irá durar.

        Quando a "leitura" é finalizada é imprimida uma mesagem indicado que ela foi 
    concluida.

    """
    with Progress() as progress:
        
        if isArquivo:
            print("Iniciando leitura do arquivo...")
            sleep(0.8)
            task = progress.add_task("Lendo arquivo...", total=size * 5)
        else:
            print("Iniciando leitura da string...")
            sleep(0.8)
            
            task = progress.add_task("Lendo string...", total=size * 1000)
            
        while not progress.finished:
            progress.update(task, advance=0.2)
        print("[green]Leitura finalizada![/]")

def loading_style(isArquivo):
    """ Esta função gera uma animação carregamento simulando a rederização da estilização do arquivo

        A função recebe um argumentos: isArquivo (booleano). "isArquivo" indica se esta 
    sendo feita a "rederização" da estilização aplicada sobre um arquivo ou de uma string, 
    mudando apenas a mensagem que é exibida na tela. O tempo da rederização já é 
    predeterminado, sendo de 2.5 segundos.

        Quando a "rederização" é finalizada é imprimida uma mesagem indicado que ela foi 
    concluida.

    """

    console = Console()
    text = "[green]Carregando estilização do arquivo[/]" if isArquivo else "[green]Carregando estilização do texto[/]"
    with console.status(text):
        sleep(2.5)
    print("[green]Estilização carregada com sucesso![/]")