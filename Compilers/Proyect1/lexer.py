import globalTypes
from globalTypes import TokenType


def getToken(imprime=True):
    globalTypes.posicion
    globalTypes.programa
    state = 0
    lexema = ""

    table = [
        [0,   2,   1,  3, 20,  4,  5,  6,  7, 21, 22,
            23, 24, 25, 26, 27, 28, 29, 30, 31,  90, ],
        [40,   91,   1, 40, 40, 40, 40, 40, 40, 40, 40,
            40, 40, 40, 40, 40, 40, 40, 40, 40,  91, ],
        [41,   2,  92, 41, 41, 41, 41, 41, 41, 41, 41,
            41, 41, 41, 41, 41, 41, 41, 41, 41,  92, ],
        [42,   42,  42, 42,  8, 42, 42, 42, 42, 42, 42,
            42, 42, 42, 42, 42, 42, 42, 42, 42,  90, ],
        [43,   43,  43, 43, 43, 43, 43, 44, 43, 43, 43,
            43, 43, 43, 43, 43, 43, 43, 43, 43,  90, ],
        [45,   45,  45, 45, 45, 45, 45, 46, 45, 45, 45,
            45, 45, 45, 45, 45, 45, 45, 45, 45,  90, ],
        [47,   47,  47, 47, 47, 47, 47, 48, 47, 47, 47,
            47, 47, 47, 47, 47, 47, 47, 47, 47,  90, ],
        [93,   93,  93, 93, 93, 93, 93, 49, 93, 93, 93,
            93, 93, 93, 93, 93, 93, 93, 93, 93,  90, ],
        [8,   8,   8,  8,  9,  8,  8,  8,  8,  8,  8,
            8,  8,  8,  8,  8,  8,  8,  8, 94,   8, ],
        [8,   8,   8,  0,  9,  8,  8,  8,  8,  8,  8,
            8,  8,  8,  8,  8,  8,  8,  8, 94,   8, ],
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

        if state in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
            globalTypes.posicion += 1

        if state == 0:
            lexema = ""

        if state == 20:
            token = TokenType.TIMES
            globalTypes.posicion += 1
            if imprime:
                print(f"Token: {token}, Lexema: *")
            return token, lexema
        elif state == 21:
            token = TokenType.PLUS
            globalTypes.posicion += 1
            if imprime:
                print(f"Token: {token}, Lexema: +")
            return token, '+'

        elif state == 22:
            token = TokenType.MINUS
            globalTypes.posicion += 1
            if imprime:
                print(f"Token: {token}, Lexema: -")
            return token, '-'

        elif state == 23:
            token = TokenType.SEMICOLON
            globalTypes.posicion += 1
            if imprime:
                print(f"Token: {token}, Lexema: ;")
            return token, ';'

        elif state == 24:
            token = TokenType.COMMA
            globalTypes.posicion += 1
            if imprime:
                print(f"Token: {token}, Lexema: ,")
            return token, ','

        elif state == 25:
            token = TokenType.LPAREN
            globalTypes.posicion += 1
            if imprime:
                print(f"Token: {token}, Lexema: (")
            return token, '('

        elif state == 26:
            token = TokenType.RPAREN
            globalTypes.posicion += 1
            if imprime:
                print(f"Token: {token}, Lexema: )")
            return token, ')'

        elif state == 27:
            token = TokenType.LBRACE
            globalTypes.posicion += 1
            if imprime:
                print(f"Token: {token}," + " Lexema: {")
            return token, '{'

        elif state == 28:
            token = TokenType.RBRACE
            globalTypes.posicion += 1
            if imprime:
                print(f"Token: {token}," + "Lexema: }")
            return token, '}'

        elif state == 29:
            token = TokenType.LBRACKET
            globalTypes.posicion += 1
            if imprime:
                print(f"Token: {token}, Lexema: [")
            return token, '['

        elif state == 30:
            token = TokenType.RBRACKET
            globalTypes.posicion += 1
            if imprime:
                print(f"Token: {token}, Lexema: ]")
            return token, ']'

        elif state == 40:
            token = TokenType.NUM
            if imprime:
                print(f"Token: {token}, Lexema: {lexema}")
            return token, lexema

        elif state == 41:
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

        elif state == 42:
            token = TokenType.DIVIDE
            if imprime:
                print(f"Token: {token}, Lexema: {lexema}")
            return token, lexema

        elif state == 43:
            token = TokenType.LT
            if imprime:
                print(f"Token: {token}, Lexema: {lexema}")
            return token, lexema

        elif state == 44:
            token = TokenType.LTEQ
            lexema += char
            globalTypes.posicion += 1
            if imprime:
                print(f"Token: {token}, Lexema: {lexema}")
            return token, lexema

        elif state == 45:
            token = TokenType.GT
            if imprime:
                print(f"Token: {token}, Lexema: {lexema}")
            return token, lexema

        elif state == 46:
            token = TokenType.GTEQ
            lexema += char
            globalTypes.posicion += 1
            if imprime:
                print(f"Token: {token}, Lexema: {lexema}")
            return token, lexema

        elif state == 47:
            token = TokenType.ASSIGN
            if imprime:
                print(f"Token: {token}, Lexema: {lexema}")
            return token, lexema

        elif state == 48:
            token = TokenType.EQ
            lexema += char
            globalTypes.posicion += 1
            if imprime:
                print(f"Token: {token}, Lexema: {lexema}")
            return token, lexema

        elif state == 49:
            token = TokenType.NEQ
            lexema += char
            globalTypes.posicion += 1
            if imprime:
                print(f"Token: {token}, Lexema: {lexema}")
            return token, lexema

        elif state == 31:
            token = TokenType.ENDFILE
            if imprime:
                print(f"Token: {token}, Lexema: $")
            return token, '$'

        elif state >= 90:
            token = TokenType.ERROR
            globalTypes.posicion += 1
            if imprime:
                message = f"Token: {token}, Lexema: {lexema}{char}"
                print(f"Token: {token}, Lexema: {lexema}{char}")
                print(' ' * (len(message)-1) + '^')
                if state == 90:
                    print("Error 90: Invalid character")
                elif state == 91:
                    print("Error 91: Faild while creating a number")
                elif state == 92:
                    print("Error 92: Faild while creating an id")
                elif state == 93:
                    print(f"Error 93: {char} can be after a '!'")
                elif state == 94:
                    print(f"Error 94: comment tag close missing")
                    return TokenType.ENDFILE, lexema

            return token, lexema

        if state != 0:
            lexema += char
