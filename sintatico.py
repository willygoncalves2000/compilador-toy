#---------------------------------------------------
# Sintático para a linguagem TOY com logs detalhados
#
# versão inicial (set-2025)
#---------------------------------------------------
from ttoken import TOKEN
from lexico import Lexico
# from semantico import Semantico

class Sintatico:

    def __init__(self, lexico):
        self.lexico = lexico
        # self.nomeAlvo = 'alvo.out'
        # self.semantico = Semantico(self.nomeAlvo)
        self.identacao = 0 # usado apenas para logs

    # -------------------- logging --------------------
    def log(self, msg):
        print(f"[Linha {self.tokenLido[2]}] {msg}")

    # -------------------- consumo de tokens --------------------
    ### verifica se o tokenAtual é igual ao token lido
    ### se sim, lê o próximo token
    ### se não, mostra erro detalhado, lança exceção e interrompe o parser
    def consome(self, tokenAtual):
        (token, lexema, linha, coluna) = self.tokenLido
        if tokenAtual == token:
            self.log(f"Token consumido: {TOKEN.msg(token)} ('{lexema}')")
            self.tokenLido = self.lexico.getToken()
        else:
            msgTokenLido = TOKEN.msg(token)
            msgTokenAtual = TOKEN.msg(tokenAtual)
            print(f'Erro na linha {linha}, coluna {coluna}: Esperado {msgTokenAtual} mas veio {msgTokenLido}')
            raise Exception

    # -------------------- teste léxico --------------------
    ### apenas percorre todos os tokens do léxico e imprime
    ### útil para testar o analisador léxico
    ### não faz parsing
    def testaLexico(self):
        self.tokenLido = self.lexico.getToken()
        (token, lexema, linha, coluna) = self.tokenLido
        while token != TOKEN.eof:
            self.lexico.imprimeToken(self.tokenLido)
            self.tokenLido = self.lexico.getToken()
            (token, lexema, linha, coluna) = self.tokenLido

    # -------------------- tradução --------------------
    ### inicia o parsing e a tradução
    ### chama self.p() que é a regra inicial da gramática
    ### se ocorrer erro, interrompe o parsing
    ### se tudo ocorrer bem, termina normalmente
    def traduz(self):
        self.tokenLido = self.lexico.getToken()
        self.log("Iniciando análise sintática")
        try:
            self.p()
            self.log("Análise concluída com sucesso")
        except:
            self.log("Análise interrompida devido a erro")

    #----------------- Gramática da linguagem TOY -----------------
    ### programa <p> começa com inicio
    ### processa comandos com self.cons()
    ### termina com fim. .
    def p(self):
        # <p> -> inicio <cons> fim .
        self.consome(TOKEN.INICIO)
        self.log("Entrada no programa")
        self.identacao = 1
        self.cons()
        self.consome(TOKEN.FIM)
        self.consome(TOKEN.pto)
        self.log("Fim do programa")

    # processa lista de comandos
    def cons(self):
        # <cons> -> LAMBDA | <com> <cons>
        while self.tokenLido[0] in [TOKEN.ident, TOKEN.IF, TOKEN.LEIA, TOKEN.ESCREVA, TOKEN.abreChave]:
            self.com()

    # escolhe qual comando executar de acordo com o token atual
    def com(self):
        # <com> -> <atrib> | <if> | <ler> | <escrever> | <bloco>
        tok = self.tokenLido[0]
        if tok == TOKEN.ident:
            self.atrib()
        elif tok == TOKEN.IF:
            self.se()
        elif tok == TOKEN.LEIA:
            self.ler()
        elif tok == TOKEN.ESCREVA:
            self.escrever()
        elif tok == TOKEN.abreChave:
            self.bloco()
        else:
            self.log(f"Comando inesperado: {TOKEN.msg(tok)}")
            raise Exception

    # chama self.exp() para processar expressões
    def atrib(self):
        # <atrib> -> ident = <exp> ;
        var = self.tokenLido[1]
        self.consome(TOKEN.ident)
        self.consome(TOKEN.atrib)
        valor = self.exp()
        self.consome(TOKEN.ptoVirg)
        self.log(f"Atribuição: {var} = {valor}")
        # self.semantico.gera(self.identacao, f"{var} = {valor}\n")

    def se(self):
        # <if> -> if ( <exp> ) <com> <elseopc>
        self.consome(TOKEN.IF)
        self.consome(TOKEN.abrePar)
        cond = self.exp()
        self.consome(TOKEN.fechaPar)
        self.log(f"Entrada em IF com condição: {cond}")
        self.identacao += 1
        self.com()
        self.identacao -= 1
        self.elseopc()

    def elseopc(self):
        if self.tokenLido[0] == TOKEN.ELSE:
            self.consome(TOKEN.ELSE)
            self.log("Entrada em ELSE")
            self.identacao += 1
            self.com()
            self.identacao -= 1

    # permite agrupar comandos em { ... }
    def bloco(self):
        # <bloco> -> { <cons> }
        self.consome(TOKEN.abreChave)
        self.log("Entrada em bloco {")
        self.cons()
        self.consome(TOKEN.fechaChave)
        self.log("Saída de bloco }")

    def ler(self):
        # <ler> -> leia ( string , ident ) ;
        self.consome(TOKEN.LEIA)
        self.consome(TOKEN.abrePar)
        prompt = self.tokenLido[1]
        self.consome(TOKEN.string)
        self.consome(TOKEN.virg)
        variavel = self.tokenLido[1]
        self.consome(TOKEN.ident)
        self.consome(TOKEN.fechaPar)
        self.consome(TOKEN.ptoVirg)
        self.log(f"Leitura de variável '{variavel}' com prompt {prompt}")
        # self.semantico.gera(self.identacao, f"{variavel} = int(input({prompt}))\n")

    def escrever(self):
        # <escrever> -> escreva ( <msg> ) ;
        self.consome(TOKEN.ESCREVA)
        self.consome(TOKEN.abrePar)
        msg = self.msg()
        self.consome(TOKEN.fechaPar)
        self.consome(TOKEN.ptoVirg)
        self.log(f"Escrita: {msg}")
        # self.semantico.gera(self.identacao, f"print({msg})\n")

    # -------------------- expressões --------------------
    def msg(self):
        parte1 = self.coisa()
        parte2 = self.restomsg()
        return parte1 + parte2

    def coisa(self):
        lexema = self.tokenLido[1]
        if self.tokenLido[0] == TOKEN.string:
            self.consome(TOKEN.string)
        else:
            self.consome(TOKEN.ident)
        return lexema

    def restomsg(self):
        if self.tokenLido[0] == TOKEN.virg:
            self.consome(TOKEN.virg)
            parte = self.msg()
            return " , " + parte
        else:
            return ""

    def exp(self):
        return self.ou()

    def ou(self):
        parte1 = self.e()
        while self.tokenLido[0] == TOKEN.OR:
            self.consome(TOKEN.OR)
            parte2 = self.e()
            parte1 = f"{parte1} or {parte2}"
        return parte1

    def e(self):
        parte1 = self.nao()
        while self.tokenLido[0] == TOKEN.AND:
            self.consome(TOKEN.AND)
            parte2 = self.nao()
            parte1 = f"{parte1} and {parte2}"
        return parte1

    def nao(self):
        if self.tokenLido[0] == TOKEN.NOT:
            self.consome(TOKEN.NOT)
            parte = self.nao()
            return f"not {parte}"
        else:
            return self.rel()

    def rel(self):
        parte1 = self.soma()
        if self.tokenLido[0] == TOKEN.OpRel:
            op = self.tokenLido[1]
            self.consome(TOKEN.OpRel)
            parte2 = self.soma()
            return f"{parte1} {op} {parte2}"
        return parte1

    def soma(self):
        parte1 = self.mult()
        while self.tokenLido[0] in [TOKEN.mais, TOKEN.menos]:
            if self.tokenLido[0] == TOKEN.mais:
                self.consome(TOKEN.mais)
                parte2 = self.mult()
                parte1 = f"{parte1} + {parte2}"
            elif self.tokenLido[0] == TOKEN.menos:
                self.consome(TOKEN.menos)
                parte2 = self.mult()
                parte1 = f"{parte1} - {parte2}"
        return parte1

    def mult(self):
        parte1 = self.folha()
        while self.tokenLido[0] in [TOKEN.multiplica, TOKEN.divide, TOKEN.mod]:
            if self.tokenLido[0] == TOKEN.multiplica:
                self.consome(TOKEN.multiplica)
                parte2 = self.folha()
                parte1 = f"{parte1} * {parte2}"
            elif self.tokenLido[0] == TOKEN.divide:
                self.consome(TOKEN.divide)
                parte2 = self.folha()
                parte1 = f"{parte1} / {parte2}"
            elif self.tokenLido[0] == TOKEN.mod:
                self.consome(TOKEN.mod)
                parte2 = self.folha()
                parte1 = f"{parte1} % {parte2}"
        return parte1

    def folha(self):
        if self.tokenLido[0] == TOKEN.num:
            salva = self.tokenLido[1]
            self.consome(TOKEN.num)
            return salva
        elif self.tokenLido[0] == TOKEN.ident:
            salva = self.tokenLido[1]
            self.consome(TOKEN.ident)
            return salva
        else:
            self.consome(TOKEN.abrePar)
            salva = self.exp()
            self.consome(TOKEN.fechaPar)
            return f"({salva})"


if __name__ == '__main__':
    print("Para testar, chame o Tradutor no main.py")
