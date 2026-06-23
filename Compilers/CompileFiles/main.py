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
    print("=== Global scope ===")
    for name, sym in scope.global_scope.symbols.items():
        print(f"  {sym}")

    # check a specific function in detail
    print("\n=== gcd detail ===")
    sym = scope.global_scope.lookup("gcd")
    print(f"  name:   {sym.name}")
    print(f"  kind:   {sym.kind}")
    print(f"  type:   {sym.type_}")
    print(f"  params: {sym.params}")

    # inspect function-level scopes
    print("\n=== Function scopes ===")
    for child in scope.global_scope.children:
        print(f"  Scope [{child.scope_name}]:")
        for s in child.symbols.values():
            print(f"    {s}")
