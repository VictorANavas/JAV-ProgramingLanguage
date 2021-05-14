#TIENE ERROR CON <,== PERO LA MATEMÁTICA FUNCIONA
import ply.lex as lex
import ply.yacc as yacc
import sys

tokens = [

    'FLOAT',
    'INT',
    'STRING',
    'SPECIALCHAR',
    'PLUS',
    'MINUS',
    'DIVIDE',
    'MULTIPLY',
    'SAME',
    'EQUALS',
    'GREATER',
    'LESS'
]

t_PLUS = r'\+'
t_MINUS = r'\-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'\/'
t_SAME = r'\=\='
t_EQUALS = r'\='
t_GREATER = r'\>'
t_LESS = r'\<'

t_ignore = r' '


def t_FLOAT(number):
    r'\d+\.\d+'
    number.value = float(number.value)
    return number


def t_INT(number):
    r'\d+'
    number.value = int(number.value)
    return number


def t_STRING(letters):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    letters.type = 'STRING'
    return letters

def SPECIALCHAR(letters):
    r'\<|\>|\=\='
    letters.type = 'SCHAR'
    return letters


def t_error(character):
    print('Illegal character.')
    character.lexer.skip(1)


lexer = lex.lex(optimize=1)

precedence = (
    ('left', 'GREATER', 'SAME', 'LESS'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULTIPLY', 'DIVIDE')
)


def p_calc(tree):
    '''
    calc : expression
         | var_assign
         | empty
    '''
    print(run(tree[1]))


def p_var_assign(tree):
    '''
    var_assign : STRING EQUALS expression
    '''
    tree[0] = ('=', tree[1], tree[3])


def p_expression(tree):
    '''
    expression : expression MULTIPLY expression
               | expression DIVIDE expression
               | expression PLUS expression
               | expression MINUS expression
    '''
    tree[0] = (tree[2], tree[1], tree[3])


def p_relexpr(p):
    '''
    expression : expression GREATER expression
               | expression SAME expression
               | expression LESS expression
    '''
    p[0] = (p[2], p[1], p[3])


def p_expression_int_float(tree):
    '''
    expression : INT
               | FLOAT
    '''
    tree[0] = tree[1]


def p_expression_var(tree):
    '''
    expression : STRING
    '''
    tree[0] = ('var', tree[1])


def p_error(tree):
    print("Syntax error.")


def p_empty(tree):
    '''
    empty :
    '''
    tree[0] = None


parser = yacc.yacc()
env = {}


def run(tree):
    global env
    if type(tree) == tuple:
        if tree[0] == '+':
            return run(tree[1]) + run(tree[2])
        elif tree[0] == '-':
            return run(tree[1]) - run(tree[2])
        elif tree[0] == '*':
            return run(tree[1]) * run(tree[2])
        elif tree[0] == '/':
            return run(tree[1]) / run(tree[2])
        elif tree[0] == '==':
            return run(tree[1]) == run(tree[2])
        elif tree[0] == '=':
            env[tree[1]] = run(tree[2])
        elif tree[0] == '>':
            return run(tree[1]) > run(tree[2])
        elif tree[0] == '<':
            return run(tree[1]) < run(tree[2])
        elif tree[0] == 'var':
            if tree[1] not in env:
                return 'Undeclared variable'
            else:
                return env[tree[1]]

    else:
        return tree


while True:
    try:
        val = input('')
    except EOFError:
        break
    parser.parse(val)
