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

    # Inicializar las variables globales
    globales(programa, posicion, progLong)

    # 1. Ejecutar análisis sintáctico (Parser)
    AST = parser(False)

    # 2. Ejecutar análisis semántico (Construye tablas y realiza las impresiones)
    scope = semantica(AST, imprime=True)
