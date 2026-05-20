from Proyect2.parser import parser
from Proyect1.globalTypes import globales
from Proyect3.semantica import *
import os
import sys
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "sample.c-")

    f = open(file_path, "r")
    programa = f.read()
    f.close()

    progLong = len(programa)
    programa = programa + "$"
    posicion = 0

    os.system("cls" if os.name == "nt" else "clear")

    globales(programa, posicion, progLong)

    AST = parser(False)
    scope = tabla(AST, imprime=False)

    # inspect global scope
    print(scope.global_scope.symbols)

    # check a specific symbol
    sym = scope.global_scope.lookup("gcd")
    print(sym.kind, sym.type_, sym.params)
