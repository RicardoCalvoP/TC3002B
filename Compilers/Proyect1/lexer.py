import globalTypes
from globalTypes import TokenType


def getToken(imprime=True):
    globalTypes.posicion
    globalTypes.programa
    state = 0
    lexema = ""

    table = [
        # blank letter digit /  *  <  >  =  !  +  -  ;  ,  (  )  {  }  [  ] EOF other
        [0,    2,    1,    3, 4, 5, 6, 7, 8, 9, 10, 11,
            12, 13, 14, 15, 16, 17, 18, 19, 20],  # 0 START
        [21,   21,   1,   21, 21, 21, 21, 21, 21, 21, 21, 21, 21,
            21, 21, 21, 21, 21, 21, 21, 21],            # 1 IN_NUM
        [22,    2,  22,   22, 22, 22, 22, 22, 22, 22, 22, 22, 22,
            22, 22, 22, 22, 22, 22, 22, 22],            # 2 IN_ID
        [23,   23,  23,   23, 24, 23, 23, 23, 23, 23, 23, 23, 23,
            23, 23, 23, 23, 23, 23, 23, 23],            # 3 SAW_SLASH
        [25,   25,  25,   26, 25, 25, 25, 25, 25, 25, 25, 25, 25,
            25, 25, 25, 25, 25, 25, 25, 25],            # 4 SAW_STAR
        [27,   27,  27,   27, 27, 27, 27, 28, 27, 27, 27, 27, 27,
            27, 27, 27, 27, 27, 27, 27, 27],            # 5 SAW_LT
        [29,   29,  29,   29, 29, 29, 29, 30, 29, 29, 29, 29, 29,
            29, 29, 29, 29, 29, 29, 29, 29],            # 6 SAW_GT
        [31,   31,  31,   31, 31, 31, 31, 32, 31, 31, 31, 31, 31,
            31, 31, 31, 31, 31, 31, 31, 31],            # 7 SAW_EQ
        [20,   20,  20,   20, 20, 20, 20, 33, 20, 20, 20, 20, 20,
            20, 20, 20, 20, 20, 20, 20, 20],            # 8 SAW_BANG
    ]

    digits = '0123456789'
    letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

    while True:
        char = globalTypes.programa[globalTypes.posicion]
        if char.isspace() or char == '\t' or char == '\n':
            # Skip whitespace characters
            col = 0
        elif char in letters:
            # Process letter
            col = 1
        elif char in digits:
            # Process digit
            col = 2
        elif char == '/':
            # Process division symbol
            col = 3
        elif char == '*':
            # Process multiplication symbol
            col = 4
        elif char == '<':
            # Process less than symbol
            col = 5
        elif char == '>':
            # Process greater than symbol
            col = 6
        elif char == '=':
            # Process assignment symbol
            col = 7
        elif char == '!':
            # Process exclamation mark symbol
            col = 8
        elif char == '+':
            # Process plus symbol
            col = 9
        elif char == '-':
            # Process minus symbol
            col = 10
        elif char == ';':
            # Process semicolon symbol
            col = 11
        elif char == ',':
            # Process comma symbol
            col = 12
        elif char == '(':
            # Process left parenthesis symbol
            col = 13
        elif char == ')':
            # Process right parenthesis symbol
            col = 14
        elif char == '{':
            # Process left brace symbol
            col = 15
        elif char == '}':
            # Process right brace symbol
            col = 16
        elif char == '[':
            # Process left bracket symbol
            col = 17
        elif char == ']':
            # Process right bracket symbol
            col = 18
        elif char == '$':
            # Process end of file character
            col = 19
        else:
            # Process unknown character
            col = 20

        state = table[state][col]

        if state in [0, 1, 2, 3, 4, 5, 6, 7, 8]:
            globalTypes.posicion += 1

        if state == 9:
            token = TokenType.PLUS
            globalTypes.posicion += 1
            if imprime:
                print(f"Token: {token}, Lexema: +")
            return token, '+'

        elif state == 10:
            token = TokenType.MINUS
            globalTypes.posicion += 1
            if imprime:
                print(f"Token: {token}, Lexema: -")
            return token, '-'

        elif state == 11:
            token = TokenType.SEMICOLON
            globalTypes.posicion += 1
            if imprime:
                print(f"Token: {token}, Lexema: ;")
            return token, ';'

        elif state == 12:
            token = TokenType.COMMA
            globalTypes.posicion += 1
            if imprime:
                print(f"Token: {token}, Lexema: ,")
            return token, ','

        elif state == 13:
            token = TokenType.LPAREN
            globalTypes.posicion += 1
            if imprime:
                print(f"Token: {token}, Lexema: (")
            return token, '('

        elif state == 14:
            token = TokenType.RPAREN
            globalTypes.posicion += 1
            if imprime:
                print(f"Token: {token}, Lexema: )")
            return token, ')'

        elif state == 15:
            token = TokenType.LBRACE
            globalTypes.posicion += 1
            if imprime:
                print(f"Token: {token}," + " Lexema: {")
            return token, '{'

        elif state == 16:
            token = TokenType.RBRACE
            globalTypes.posicion += 1
            if imprime:
                print(f"Token: {token}," + "Lexema: }")
            return token, '}'

        elif state == 17:
            token = TokenType.LBRACKET
            globalTypes.posicion += 1
            if imprime:
                print(f"Token: {token}, Lexema: [")
            return token, '['

        elif state == 18:
            token = TokenType.RBRACKET
            globalTypes.posicion += 1
            if imprime:
                print(f"Token: {token}, Lexema: ]")
            return token, ']'

        elif state == 21:
            token = TokenType.NUM
            if imprime:
                print(f"Token: {token}, Lexema: {lexema}")
            return token, lexema

        elif state == 22:
            reserved_words = {
                "else": TokenType.ELSE,
                "if": TokenType.IF,
                "int": TokenType.INT,
                "return": TokenType.RETURN,
                "void": TokenType.VOID,
                "while": TokenType.WHILE
            }

            if lexema in reserved_words:
                token = reserved_words[lexema]
            else:
                token = TokenType.ID
            if imprime:
                print(f"Token: {token}, Lexema: {lexema}")
            return token, lexema

        elif state == 23:
            token = TokenType.DIVIDE
            if imprime:
                print(f"Token: {token}, Lexema: {lexema}")
            return token, lexema

        elif state == 24:
            token = TokenType.LCOMMENT
            lexema += char
            globalTypes.posicion += 1
            if imprime:
                print(f"Token: {token}, Lexema: {lexema}")
            return token, lexema

        elif state == 25:
            token = TokenType.TIMES
            if imprime:
                print(f"Token: {token}, Lexema: {lexema}")
            return token, lexema

        elif state == 26:
            token = TokenType.RCOMMENT
            lexema += char
            globalTypes.posicion += 1
            if imprime:
                print(f"Token: {token}, Lexema: {lexema}")
            return token, lexema

        elif state == 27:
            token = TokenType.LT
            if imprime:
                print(f"Token: {token}, Lexema: {lexema}")
            return token, lexema

        elif state == 28:
            token = TokenType.LTEQ
            lexema += char
            globalTypes.posicion += 1
            if imprime:
                print(f"Token: {token}, Lexema: {lexema}")
            return token, lexema

        elif state == 29:
            token = TokenType.GT
            if imprime:
                print(f"Token: {token}, Lexema: {lexema}")
            return token, lexema

        elif state == 30:
            token = TokenType.GTEQ
            lexema += char
            globalTypes.posicion += 1
            if imprime:
                print(f"Token: {token}, Lexema: {lexema}")
            return token, lexema

        elif state == 31:
            token = TokenType.ASSIGN
            if imprime:
                print(f"Token: {token}, Lexema: {lexema}")
            return token, lexema

        elif state == 32:
            token = TokenType.EQ
            lexema += char
            globalTypes.posicion += 1
            if imprime:
                print(f"Token: {token}, Lexema: {lexema}")
            return token, lexema

        elif state == 33:
            token = TokenType.NEQ
            lexema += char
            globalTypes.posicion += 1
            if imprime:
                print(f"Token: {token}, Lexema: {lexema}")
            return token, lexema

        elif state == 19:
            token = TokenType.ENDFILE
            if imprime:
                print(f"Token: {token}, Lexema: $")
            return token, '$'

        elif state == 20:
            token = TokenType.ERROR
            globalTypes.posicion += 1
            if imprime:
                message = f"Token: {token}, Lexema: {lexema}{char}"
                print(f"Token: {token}, Lexema: {lexema}{char}")
                print(' ' * (len(message)-1) + '^')
            return token, lexema

        if state != 0:
            lexema += char
