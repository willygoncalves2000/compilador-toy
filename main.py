#---------------------------------------------------
# Tradutor para a linguagem TOY
#
# baseado no main da linguagem CALC
#---------------------------------------------------
from lexico import Lexico
from sintatico import Sintatico

class Tradutor:

    def __init__(self, nomeArq):
        self.nomeArq = nomeArq

    def inicializa(self):
        self.arq = open(self.nomeArq, "r")
        self.lexico = Lexico(self.arq)
        self.sintatico = Sintatico(self.lexico)

    def traduz(self):
        print("🚀 Iniciando tradução (análise sintática)...\n")
        self.sintatico.traduz()

    def testaLexico(self):
        print("🔎 Iniciando análise léxica...\n")
        self.sintatico.testaLexico()

    def finaliza(self):
        self.arq.close()


# inicia a tradução
if __name__ == '__main__':
    x = Tradutor('toy.txt')  # arquivo fonte da linguagem TOY
    x.inicializa()

    # escolha o que rodar:
    #x.testaLexico()   # análise léxica
    x.traduz()         # tradução + análise sintática

    x.finaliza()
