####################################### CONSTANTS #######################################
#This is used to tell which characters are named 'DIGITS'
DIGITS = '0123456789'

####################################### ERRORS #######################################
#This class is an error class which returns the necesary error text
class Error:
    def __init__(self, startPosition, endPosition, errorName, details):
        self.startPosition = startPosition
        self.endPosition = endPosition
        self.errorName = errorName
        self.details = details
    
    def as_string(self):
        result  = f'{self.errorName}: {self.details}\n'
        result += f'File {self.startPosition.fn}, line {self.startPosition.ln + 1}'
        return result

#This is an error class uses the class above which is just going to do the error text when there is an illegal character
class IllegalCharError(Error):
    def __init__(self, startPosition, endPosition, details):
        super().__init__(startPosition, endPosition, 'Illegal Character', details)

####################################### POSITION #######################################
#This class creates the movement in terms of reading the input 
class Position:
    def __init__(self, idx, ln, col, fn, ftxt):
        self.idx = idx
        self.ln = ln
        self.col = col
        self.fn = fn
        self.ftxt = ftxt

    def advance(self, current_char):
        self.idx += 1
        self.col += 1

        if current_char == '\n':
            self.ln += 1
            self.col = 0

        return self

    def copy(self):
        return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)

####################################### TOKENS #######################################
#These are the tokens which will be used to determine what is going on in the mathematical equation 
INT_TOKEN = 'INT'
FLOAT_TOKEN = 'FLOAT'
PLUS_TOKEN = 'PLUS'
MINUS_TOKEN = 'MINUS'
MULTIPLICATION_TOKEN = 'MUL'
DIVISION_TOKEN = 'DIV'
SQUARE_ROOT_TOKEN = 'SQRT'
ELEVATION_TOKEN = 'ELEV'
LEFT_PAREN_TOKEN = 'LPAREN'
RIGHT_PAREN_TOKEN = 'RPAREN'

#The class token so it can return the necesary token 
class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value
    
    def __repr__(self):
        if self.value: return f'{self.type}:{self.value}'
        return f'{self.type}'

####################################### LEXER #######################################
#The lexer class will have the validation for every character it inputs
class Lexer:
    def __init__(self, fn, text):
        self.fn = fn
        self.text = text
        self.pos = Position(-1, 0, -1, fn, text)
        self.current_char = None
        self.advance()
    
    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None

    def make_tokens(self):
        tokens = []

        while self.current_char != None:
            if self.current_char in ' \t':
                self.advance()
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
            elif self.current_char == '+':
                tokens.append(Token(PLUS_TOKEN))
                self.advance()
            elif self.current_char == '-':
                tokens.append(Token(MINUS_TOKEN))
                self.advance()
            elif self.current_char == '*':
                tokens.append(Token(MULTIPLICATION_TOKEN))
                self.advance()
            elif self.current_char == '/':
                tokens.append(Token(DIVISION_TOKEN))
                self.advance()
            elif self.current_char == '|':
                tokens.append(Token(SQUARE_ROOT_TOKEN))
                self.advance()
            elif self.current_char == '^':
                tokens.append(Token(ELEVATION_TOKEN))
                self.advance()
            elif self.current_char == '(':
                tokens.append(Token(LEFT_PAREN_TOKEN))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(RIGHT_PAREN_TOKEN))
                self.advance()
            else:
                startPosition = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharError(startPosition, self.pos, "'" + char + "'")

        return tokens, None

    def make_number(self):
        num_str = ''
        dot_count = 0

        while self.current_char != None and self.current_char in DIGITS + '.':
            if self.current_char == '.':
                if dot_count == 1: break
                dot_count += 1
                num_str += '.'
            else:
                num_str += self.current_char
            self.advance()

        if dot_count == 0:
            return Token(INT_TOKEN, int(num_str))
        else:
            return Token(FLOAT_TOKEN, float(num_str))

####################################### RUN #######################################
#Basic run functions which runs the lexer, tokens and error messages
def run(fn, text):
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()

    return tokens, error
