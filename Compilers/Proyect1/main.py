from globalTypes import *
from lexer import *
import os
if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))

    file_path = os.path.join(script_dir, "sample.c-")

    f = open(file_path, 'r')
    programa = f.read()
    progLong = len(programa)
    programa = programa + '$'
    posicion = 0
    os.system('cls' if os.name == 'nt' else 'clear')
    # Function to set the initial values of the global variables
    globales(programa, posicion, progLong)
    token, tokenString = getToken(True)
    tokens = 0
    while (token != TokenType.ENDFILE and tokens < 1000000):
        token, tokenString = getToken()
        tokens += 1
