from lexico import Lexico


class Tradutor:

    def __init__(self, nomeArq):
        self.nomeArq = nomeArq

    def inicializa(self):
        self.arq = open(self.nomeArq, "r")
        self.lexico = Lexico(self.arq)

    def testaLexico(self):
        print("🔎 Iniciando análise léxica...\n")
        while True:
            token = self.lexico.getToken()
            self.lexico.imprimeToken(token)
            if token[0].name == "eof":  # quando chega no EOF, encerra
                break

    def finaliza(self):
        self.arq.close()


# inicia a tradução
if __name__ == '__main__':
    x = Tradutor('toy.txt')
    x.inicializa()
    x.testaLexico()
    x.finaliza()
