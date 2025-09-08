# Tradutor para a linguagem TOY

from enum import IntEnum

class TOKEN(IntEnum):
    erro = 1
    eof = 2
    ident = 3
    num = 4
    string = 5

    IF = 6
    ELSE = 7
    INICIO = 8
    FIM = 9
    LEIA = 10
    ESCREVA = 11

    abrePar = 12
    fechaPar = 13
    virg = 14
    ptoVirg = 15
    pto = 16
    OpRel = 17     # todos os operadores relacionais (==, !=, <, >, <=, >=)
    AND = 18
    OR = 19
    NOT = 20
    mais = 21
    menos = 22
    multiplica = 23
    divide = 24
    mod = 25
    abreChave = 26
    fechaChave = 27
    atrib = 28     # '=' de atribuição

    @classmethod
    def msg(cls, token):
        nomes = {
            1:'erro',
            2:'<eof>',
            3:'ident',
            4:'numero',
            5:'string',
            6:'if',
            7:'else',
            8:'inicio',
            9:'fim',
            10:'leia',
            11:'escreva',
            12:'(',
            13:')',
            14:',',
            15:';',
            16:'.',
            17:'opRel',     # engloba ==, !=, <, >, <=, >=
            18:'and',
            19:'or',
            20:'not',
            21:'+',
            22:'-',
            23:'*',
            24:'/',
            25:'%',
            26:'{',
            27:'}',
            28:'='
        }
        return nomes[token]

    @classmethod
    def reservada(cls, lexema):
        reservadas = {
            'if': TOKEN.IF,
            'else': TOKEN.ELSE,
            'inicio': TOKEN.INICIO,
            'fim': TOKEN.FIM,
            'leia': TOKEN.LEIA,
            'escreva': TOKEN.ESCREVA,
            'and': TOKEN.AND,
            'or': TOKEN.OR,
            'not': TOKEN.NOT
        }
        if lexema in reservadas:
            return reservadas[lexema]
        else:
            return TOKEN.ident
