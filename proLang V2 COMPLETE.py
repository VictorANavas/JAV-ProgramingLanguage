import ply.lex as lex
import ply.yacc as yacc
import sys
import math

keywords = (
    'THEN',
    'ELSE',
    'SIN',
    'COS'
)

tokens = keywords + (
    'FLOAT',
    'INT',
    'STRING',
    'PLUS',
    'MINUS',
    'DIVIDE',
    'MULTIPLY',
    'SAME',
    'EQUALS',
    'POWER',
    'LEFTPARENTHESIS',
    'RIGHTPARENTHESIS',
    'GREATER',
    'IF',
    'LESS'
)

t_PLUS = r'\+'
t_MINUS = r'\-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'\/'
t_SAME = r'\=\='
t_EQUALS = r'\='
t_POWER = r'\^'
t_LEFTPARENTHESIS = r'\('
t_RIGHTPARENTHESIS = r'\)'
t_GREATER = r'\>'
t_LESS = r'\<'
t_SIN = r'sin'
t_COS = r'cos'
t_IF = r'if'
t_THEN = r'then'
t_ELSE = r'else'


t_ignore = r' '


def t_FLOAT(number):
    r'\d+\.\d+'
    number.value = float(number.value)
    return number


def t_INT(number):
    r'\d+'
    number.value = int(number.value)
    return number


# def t_SIN(p):
#     r' sin '
#     p.type = 'IF'
#     return p


def t_STRING(letters):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    letters.type = 'STRING'
    return letters


#Sacado de github
def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_error(character):
    print('Illegal character.')
    character.lexer.skip(1)


#optimize=1 lo use pq lo usan para eliminar un warning
lex.lex()

#Parsing rules
precedence = (
    ('left', 'GREATER', 'SAME', 'LESS'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULTIPLY', 'DIVIDE'),
    ('left', 'POWER', 'SIN', 'COS'),
)

#Dictionary
variables = {}


def p_var_assign(tree):
    '''
    statement : STRING EQUALS expression
    '''
    #tree[0] = ('=', tree[1], tree[3])
    variables[tree[1]] = tree[3]


def p_statement_expr(tree):
    '''
    statement : expression
              | if_expression
              | empty
    '''
    print(tree[1])


def p_expression(tree):
    '''
    expression : expression POWER expression
               | expression MULTIPLY expression
               | expression DIVIDE expression
               | expression PLUS expression
               | expression MINUS expression
               | expression GREATER expression
               | expression SAME expression
               | expression LESS expression
    '''
    #tree[0] = (tree[2], tree[1], tree[3])
    if tree[2] == '^':
        tree[0] = tree[1] ** tree[3]
    elif tree[2] == '*':
        tree[0] = tree[1] * tree[3]
    elif tree[2] == '/':
        tree[0] = tree[1] / tree[3]
    elif tree[2] == '+':
        tree[0] = tree[1] + tree[3]
    elif tree[2] == '-':
        tree[0] = tree[1] - tree[3]
    if tree[2] == '>':
        tree[0] = tree[1] > tree[3]
    elif tree[2] == '==':
        tree[0] = tree[1] == tree[3]
    elif tree[2] == '<':
        tree[0] = tree[1] < tree[3]


def p_trigonometric(tree):
    '''
    expression : SIN LEFTPARENTHESIS expression RIGHTPARENTHESIS
    '''
    #print('tree:', tree[0], tree[1], tree[2], tree[3], tree[4])
    if tree[1] == 'sin':
        tree[0] = math.sin(tree[3])
    elif tree[1] == 'cos':
        tree[0] = math.cos(tree[3])
    elif tree[1] == 'tan':
        tree[0] = math.tan(tree[3])
    elif tree[1] == 'csc':
        tree[0] = 1/(math.sin(tree[3]))
    elif tree[1] == 'sec':
        tree[0] = 1/(math.cos(tree[3]))
    elif tree[1] == 'cot':
        tree[0] = 1/(math.tan(tree[3]))
    else:
        pass


# def p_cos(tree):
#     '''
#     expression : STRING LEFTPARENTHESIS expression RIGHTPARENTHESIS
#     '''
#     if tree[1] == 'cos':
#         tree[0] = math.cos(tree[3])
#     else:
#         pass


def p_if_then_else(tree):
    '''
    if_expression : STRING expression STRING expression STRING expression
    '''
    if tree[1] == 'if':
        if tree[3] == 'then':
            if tree[5] == 'else':
                if tree[2]:
                    tree[0] = tree[4]
                else:
                    tree[0] = tree[6]
            else:
                pass
        else:
            pass
    else:
        pass

# def p_expression_bool(tree):
#     '''
#     expression : expression GREATER expression
#                | expression SAME expression
#                | expression LESS expression
#     '''
#     #p[0] = (p[2], p[1], p[3])
#     if tree[2] == '>':
#         tree[0] = tree[1] > tree[2]
#     elif tree[2] == '==':
#         tree[0] = tree[1] == tree[2]
#     elif tree[2] == '<':
#         tree[0] = tree[1] < tree[2]
#
#     return tree[0]


# #Sacado de github
# def p_expression_uminus(tree):
#     '''
#     expression : MINUS expression %prec UMINUS
#     '''
#     tree[0] = -tree[2]


def p_expression_group(tree):
    '''
    expression : LEFTPARENTHESIS expression RIGHTPARENTHESIS
    '''
    tree[0] = tree[2]


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
    tree[0] = variables[tree[1]]
    #tree[0] = ('var', tree[1])
    # try:
    #     tree[0] = variables[tree[1]]
    # except LookupError:
    #     print("Undefined name")
    #     tree[0] = 0


# def p_expression_aritmetic(tree):
#     '''
#     expression : expression SIN LEFTPARENTHESIS INT RIGHTPARENTHESIS expression
#                | expression SIN LEFTPARENTHESIS FLOAT RIGHTPARENTHESIS expression
#                | expression SIN LEFTPARENTHESIS expression RIGHTPARENTHESIS expression
#                | expression COS LEFTPARENTHESIS INT RIGHTPARENTHESIS expression
#                | expression COS LEFTPARENTHESIS FLOAT RIGHTPARENTHESIS expression
#                | expression COS LEFTPARENTHESIS expression RIGHTPARENTHESIS expression
#     '''
#     if tree[2] == 'SIN':
#         tree[0] = float(math.sin(tree[4]))
#     elif tree[2] == 'COS':
#         tree[0] = float(math.cos(tree[4]))



# def p_calc(tree):
#     '''
#     calc : expression
#          | empty
#     '''
#     #print(tree[1])      #Para ver el arbol
#     #print(tree[1]) #Para que corra


def p_empty(tree):
    '''
    empty :
    '''


# def run(tree):
#     global variables
#     if type(tree) == tuple:
#         # if tree[0] == '+':
#         #     return run(tree[1]) + run(tree[2])
#         # elif tree[0] == '-':
#         #     return run(tree[1]) - run(tree[2])
#         # elif tree[0] == '*':
#         #     return run(tree[1]) * run(tree[2])
#         # elif tree[0] == '/':
#         #     return run(tree[1]) / run(tree[2])
#         # if tree[0] == '==':
#         #     return run(tree[1]) == run(tree[2])
#         # elif tree[0] == '=':
#         #     variables[tree[1]] = run(tree[2])
#         # elif tree[0] == '>':
#         #     return run(tree[1]) > run(tree[2])
#         # elif tree[0] == '<':
#         #     return run(tree[1]) < run(tree[2])
#         # elif tree[0] == '^':
#         #     return run(tree[1]) ** run(tree[2])
#         if tree[0] == '(':
#             return run(tree[1])
#         elif tree[0] == 'var':
#             if tree[1] not in variables:
#                 return 'Undeclared variable'
#             else:
#                 return variables[tree[1]]
#     else:
#         return tree


def p_error(tree):
    print("Syntax error.")


yacc.yacc()

while True:
    try:
        value = input('Calculate : ')
    except EOFError:
        break
    yacc.parse(value)
