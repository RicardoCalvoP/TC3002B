from enum import Enum, auto


def globales(prog, pos, long):
    global programa
    global posicion
    global progLong
    programa = prog
    posicion = pos
    progLong = long


class TokenType(Enum):
    # reseved words
    ELSE = 'else'
    IF = 'if'
    INT = 'int'
    RETURN = 'return'
    VOID = 'void'
    WHILE = 'while'
    # symbols
    PLUS = '+'
    MINUS = '-'
    TIMES = '*'
    DIVIDE = '/'
    LT = '<'  # Less Than
    LTEQ = '<='  # Less Than or Equal To
    GT = '>'  # Greater Than
    GTEQ = '>='  # Greater Than or Equal To
    EQ = '=='  # Equal To
    NEQ = '!='  # Not Equal To
    ASSIGN = '='  # Assignment
    SEMICOLON = ';'  # Semicolon
    COMMA = ','  # Comma
    LPAREN = '('  # Left Parenthesis
    RPAREN = ')'  # Right Parenthesis
    LBRACE = '{'  # Left Brace
    RBRACE = '}'  # Right Brace
    RBRACKET = ']'  # Right Bracket
    LBRACKET = '['  # Left Bracket
    LCOMMENT = '/*'  # Left Comment
    RCOMMENT = '*/'  # Right Comment
    # other tokens
    ID = 'id'
    NUM = 'num'
    ENDFILE = 'endfile'
    ERROR = 'error'
