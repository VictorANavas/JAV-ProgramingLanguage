#-----------------------------------------------------------
#                  JAV Programming Language
#  For kids focusing in coding and mathematical development
#           By: Victor Navas and Jorge Alonso
#-----------------------------------------------------------
import ply.lex as lex
import ply.yacc as yacc
import math

#Are used as identification words in PLY
tokens = (
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
    'LESS'
)

#This list defines what all the tokens are going to be
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


def t_error(character):
    print('Illegal character.')
    character.lexer.skip(1)


lex.lex()

#Parsing rules
precedence = (
    ('left', 'GREATER', 'SAME', 'LESS'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULTIPLY', 'DIVIDE'),
    ('left', 'POWER'),
)

#Dictionary
variables = {}


#Is the function that defines what a statement will be and is going to be the output
def p_statement_expr(tree):
    # YACC.PY parse language syntax
    '''
    statement : expression
              | if_expression
              | empty
    '''
    print(tree[1])


#Function that makes the variable assign possible
def p_var_assign(tree):
    #YACC.PY parse language syntax
    '''
    statement : STRING EQUALS expression
    '''
    #Adds variables to the dictionary
    variables[tree[1]] = tree[3]


#Function that declarates what an expression will look like
def p_expression(tree):
    # YACC.PY parse language syntax
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
    #Depending on the option above, it will do the algebra calculations
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


#Adds to the definition of a function
def p_trigonometric(tree):
    # YACC.PY parse language syntax
    '''
    expression : STRING LEFTPARENTHESIS expression RIGHTPARENTHESIS
    '''
    #Depending on the option above, it will do the trigonometry calculations
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


#Defines the statement: if_expression
def p_if_then_else(tree):
    # YACC.PY parse language syntax
    '''
    if_expression : STRING expression STRING expression STRING expression
    '''
    # Validates if all 3 words are the exact code words for this function
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


#Adds to the definition of expression and is used for the use of parenthesis
def p_expression_group(tree):
    # YACC.PY parse language syntax
    '''
    expression : LEFTPARENTHESIS expression RIGHTPARENTHESIS
    '''
    #This makes the tree do the math when its used
    tree[0] = tree[2]


#Defines that INT and FLOAT are expressions
def p_expression_int_float(tree):
    # YACC.PY parse language syntax
    '''
    expression : INT
               | FLOAT
    '''
    #It identifies the INT and FLOAT
    tree[0] = tree[1]


#Defines that STRING is an expression
def p_expression_var(tree):
    # YACC.PY parse language syntax
    '''
    expression : STRING
    '''
    # It identifies the STRING
    tree[0] = variables[tree[1]]


#Defines what an empty tree looks like
def p_empty(tree):
    # YACC.PY parse language syntax
    '''
    empty :
    '''


#Prints out when its a syntax error
def p_error(tree):
    print("Syntax error.")


yacc.yacc()

while True:
    try:
        value = input('Calculate : ')
    except EOFError:
        break
    yacc.parse(value)

    # infile = open('prueba.txt', 'r')
    # # Mostramos por pantalla lo que leemos desde el fichero
    # print
    # 'Probando Vector'
    # for line in infile:
    #     parse.parse(line)
    #
    # # Cerramos el fichero.
    # infile.close()
