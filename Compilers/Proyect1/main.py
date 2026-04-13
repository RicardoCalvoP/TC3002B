from globalTypes import *
from lexer import *
import os
if __name__ == "__main__":
    f = open('sample.c-', 'r')
    programa = f.read()
    progLong = len(programa)
    programa = programa + '$'
    posicion = 0
    os.system('cls' if os.name == 'nt' else 'clear')
    # Function to set the initial values of the global variables
    globales(programa, posicion, progLong)
    token, tokenString = getToken(True)

    while (token != TokenType.ENDFILE and token != TokenType.ERROR):
        token, tokenString = getToken(True)
