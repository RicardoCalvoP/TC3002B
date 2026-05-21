import os
import sys

from Proyect1.globalTypes import *
from Proyect2.parser import *


# ---------------------------------------------------------------------------
# Symbol
# ---------------------------------------------------------------------------

class Symbol:
    def __init__(self, name, kind, type_, params=None, lineno=0):
        self.name = name
        self.kind = kind
        self.type_ = type_
        self.params = params or []
        self.lineno = lineno

    def __repr__(self):
        if self.kind == 'function':
            param_str = ', '.join(
                f"{p.type_}{'[]' if p.kind == 'array' else ''}" for p in self.params
            )
            return f"[{self.kind}] {self.type_} {self.name}({param_str})"
        suffix = '[]' if self.kind == 'array' else ''
        return f"[{self.kind}] {self.type_} {self.name}{suffix}"


# ---------------------------------------------------------------------------
# Table  (one scope's symbol dictionary)
# ---------------------------------------------------------------------------

class Table:
    def __init__(self, scope_name, parent=None):
        self.scope_name = scope_name
        self.parent = parent
        self.symbols = {}
        self.children = []

    def define(self, symbol: Symbol):
        """Add symbol; return False if already declared in THIS scope."""
        if symbol.name in self.symbols:
            return False
        self.symbols[symbol.name] = symbol
        return True

    def lookup(self, name):
        """Search this scope, then walk up the parent chain."""
        result = self.symbols.get(name)
        if result is not None:
            return result
        if self.parent is not None:
            return self.parent.lookup(name)
        return None


# ---------------------------------------------------------------------------
# Scope
# ---------------------------------------------------------------------------

class Scope:
    def __init__(self):
        self.global_scope = Table("global")
        self.current = self.global_scope
        self._preload_builtins()

    def _preload_builtins(self):
        """Pre-load C- built-in functions: input() and output()."""
        self.global_scope.define(
            Symbol("input",  "function", "int",  params=[]))
        self.global_scope.define(
            Symbol("output", "function", "void",
                   params=[Symbol("x", "var", "int")]))

    def enter_scope(self, scope_name):
        new_scope = Table(scope_name, parent=self.current)
        self.current.children.append(new_scope)
        self.current = new_scope

    def exit_scope(self):
        if self.current.parent is not None:
            self.current = self.current.parent

    def define(self, symbol: Symbol):
        return self.current.define(symbol)

    def lookup(self, name):
        return self.current.lookup(name)


# ---------------------------------------------------------------------------
# Pass 1 helpers
# ---------------------------------------------------------------------------

def _collect_params(param_node):

    if param_node is None:
        return []

    if param_node.exp != TypeExpression.Param:
        return []

    if param_node.name is not None:
        kind = 'array' if param_node.is_array else 'var'
        return [Symbol(param_node.name, kind, param_node.type)]
    else:
        return (_collect_params(param_node.left_child) +
                _collect_params(param_node.right_child))


def _build_table(node, scope, enter_compound=False):

    if node is None:
        return

    exp = node.exp

    # Program
    if exp == TypeExpression.Program:
        _build_table(node.left_child,  scope)
        _build_table(node.right_child, scope)

    # Variable declaration
    elif exp == TypeExpression.VarDeclaration:
        if node.name is not None:
            kind = 'array' if node.is_array else 'var'
            symbol = Symbol(node.name, kind, node.type)   # .type NOT .type_
            if not scope.define(symbol):
                _reportar_error(
                    node, f"'{node.name}' ya fue declarado en este ámbito")
        else:
            _build_table(node.left_child,  scope)
            _build_table(node.right_child, scope)

    # Function declaration
    elif exp == TypeExpression.FunDeclaration:
        param_symbols = _collect_params(node.left_child)

        fun_sym = Symbol(node.name, 'function', node.type,   # .type NOT .type_
                         params=param_symbols)
        if not scope.define(fun_sym):
            _reportar_error(
                node, f"Error semántico: función '{node.name}' ya fue declarada")

        scope.enter_scope(node.name)

        for p in param_symbols:
            scope.define(p)

        _build_table(node.right_child, scope, enter_compound=True)

        scope.exit_scope()

    # Compound statement
    elif exp == TypeExpression.Compound:
        if enter_compound:
            scope.enter_scope("bloque_local")

            _build_table(node.left_child,  scope)
            _build_table(node.right_child, scope)

            scope.exit_scope()
        else:
            _build_table(node.left_child,  scope)
            _build_table(node.right_child, scope)

    # If statement
    elif exp == TypeExpression.If:
        _build_table(node.left_child,  scope)
        _build_table(node.right_child, scope,
                     enter_compound=(node.right_child is not None and
                                     node.right_child.exp == TypeExpression.Compound))

    # While statement
    elif exp == TypeExpression.While:
        _build_table(node.left_child,  scope)
        _build_table(node.right_child, scope,
                     enter_compound=(node.right_child is not None and
                                     node.right_child.exp == TypeExpression.Compound))

    else:
        _build_table(node.left_child,  scope)
        _build_table(node.right_child, scope)


def _reportar_error(nodo, mensaje):

    lineno = getattr(nodo, 'lineno', 0)

    if lineno > 0:
        print(f"Error semántico (línea {lineno}): {mensaje}")
        from Proyect1 import globalTypes
        prog = getattr(globalTypes, 'programa', None)
        if prog:
            lineas = prog.split('\n')
            if 0 < lineno <= len(lineas):
                print(lineas[lineno - 1])
                print("^")
    else:
        print(f"Error semántico: {mensaje}")

    print("-" * 50)

# ---------------------------------------------------------------------------
# Pass 2: Type Checking and Inference Engine
# ---------------------------------------------------------------------------


def _check_types(node, scope, current_table=None, current_function_type=None):
    if node is None:
        return None

    if current_table is None:
        current_table = scope.global_scope

        def _reset_tables(table):
            table._next_child_idx = 0
            for child in table.children:
                _reset_tables(child)
        _reset_tables(current_table)

    exp = node.exp

    # Programa
    if exp == TypeExpression.Program:
        _check_types(node.left_child, scope,
                     current_table, current_function_type)
        _check_types(node.right_child, scope,
                     current_table, current_function_type)
        return None

    # Declaración de Variables
    elif exp == TypeExpression.VarDeclaration:
        if node.name is None:  # Nodo conector/wrapper de encadenamiento
            _check_types(node.left_child, scope,
                         current_table, current_function_type)
            _check_types(node.right_child, scope,
                         current_table, current_function_type)
        return None

    # Declaración de Funciones
    elif exp == TypeExpression.FunDeclaration:
        next_table = None
        for child in current_table.children:
            if child.scope_name == node.name:
                next_table = child
                break

        if next_table:
            _check_types(node.right_child, scope, next_table,
                         current_function_type=node.type)
        return None

    # Bloques Compuestos { }
    elif exp == TypeExpression.Compound:
        next_table = current_table

        if len(current_table.children) > 0:
            idx = current_table._next_child_idx
            if idx < len(current_table.children):
                next_table = current_table.children[idx]
                current_table._next_child_idx += 1

        _check_types(node.left_child, scope, next_table, current_function_type)
        _check_types(node.right_child, scope,
                     next_table, current_function_type)
        return None

    # Constantes Numéricas
    elif exp == TypeExpression.Const:
        return 'int'

    # Identificadores (Variables Simples)
    elif exp == TypeExpression.Id:
        sym = current_table.lookup(node.name)
        if sym is None:
            _reportar_error(
                node, f"El identificador '{node.name}' no ha sido declarado.")
            return 'int'
        if sym.kind == 'function':
            _reportar_error(
                node, f"El identificador '{node.name}' es una función y no puede usarse como variable.")
            return 'int'
        if sym.kind == 'array':
            _reportar_error(
                node, f"El identificador de arreglo '{node.name}' requiere un índice.")
            return 'int'
        return sym.type_

    # Arreglos con Índice (ArrayId)
    elif exp == TypeExpression.ArrayId:
        sym = current_table.lookup(node.name)
        tipo_idx = _check_types(node.left_child, scope,
                                current_table, current_function_type)

        if sym is None:
            _reportar_error(
                node, f"El arreglo '{node.name}' no ha sido declarado.")
            return 'int'

        if sym.kind != 'array':
            _reportar_error(
                node, f"El identificador '{node.name}' no es un arreglo.")

        if tipo_idx != 'int':
            _reportar_error(
                node, f"El índice del arreglo '{node.name}' debe ser de tipo entero, se encontró '{tipo_idx}'.")

        return sym.type_

    # Operaciones Matemáticas y Lógicas (Op)
    elif exp == TypeExpression.Op:
        tipo_izq = _check_types(node.left_child, scope,
                                current_table, current_function_type)
        tipo_der = _check_types(node.right_child, scope,
                                current_table, current_function_type)

        if tipo_izq != 'int' or tipo_der != 'int':
            _reportar_error(
                node, f"Los operadores de '{node.op}' deben ser de tipo entero. Se encontró '{tipo_izq}' {node.op} '{tipo_der}'.")
        return 'int'

    # Asignaciones (Assign)
    elif exp == TypeExpression.Assign:
        tipo_izq = _check_types(node.left_child, scope,
                                current_table, current_function_type)
        tipo_der = _check_types(node.right_child, scope,
                                current_table, current_function_type)

        if tipo_izq != 'int' or tipo_der != 'int':
            _reportar_error(
                node, f"No se puede asignar un valor de tipo '{tipo_der}' a una variable de tipo '{tipo_izq}'.")
        return 'int'

    # Sentencias de Retorno (Return)
    elif exp == TypeExpression.Return:
        tipo_retornado = 'void'
        if node.right_child is not None:
            tipo_retornado = _check_types(
                node.right_child, scope, current_table, current_function_type)

        if current_function_type is not None and tipo_retornado != current_function_type:
            _reportar_error(
                node, f"La función actual espera un retorno de tipo '{current_function_type}', pero se retornó '{tipo_retornado}'.")
        return tipo_retornado

    # Condicionales (If) y Bucles (While)
    elif exp == TypeExpression.If or exp == TypeExpression.While:
        if node.left_child is not None and node.left_child.exp == TypeExpression.If:
            _check_types(node.left_child, scope,
                         current_table, current_function_type)
            tipo_cond = 'int'
        else:
            tipo_cond = _check_types(
                node.left_child, scope, current_table, current_function_type)

        if tipo_cond != 'int':
            _reportar_error(
                node, f"La condición del '{exp.name.lower()}' debe ser de tipo entero, se encontró '{tipo_cond}'.")

        _check_types(node.right_child, scope,
                     current_table, current_function_type)
        return None

    # Llamadas a Funciones (Call)
    elif exp == TypeExpression.Call:
        sym = current_table.lookup(node.name)

        argumentos_tipos = []

        def _recolectar_argumentos(arg_node):
            if arg_node is None:
                return
            if arg_node.exp == TypeExpression.ExpressionStmt:
                _recolectar_argumentos(arg_node.left_child)
                _recolectar_argumentos(arg_node.right_child)
            else:
                t = _check_types(arg_node, scope, current_table,
                                 current_function_type)
                if t is not None:
                    argumentos_tipos.append(t)

        _recolectar_argumentos(node.left_child)

        if sym is None:
            _reportar_error(
                node, f"La función '{node.name}' no ha sido declarada.")
            return 'int'

        if sym.kind != 'function':
            _reportar_error(
                node, f"El identificador '{node.name}' se está llamando como función pero es un(a) {sym.kind}.")
            return 'int'

        if len(argumentos_tipos) != len(sym.params):
            _reportar_error(
                node, f"La función '{node.name}' requiere {len(sym.params)} argumentos, pero se pasaron {len(argumentos_tipos)}.")
        else:
            # Validar tipos de los parámetros
            for i, tipo_arg in enumerate(argumentos_tipos):
                tipo_param = sym.params[i].type_
                if tipo_arg != tipo_param:
                    _reportar_error(
                        node, f"El argumento {i+1} de la función '{node.name}' debería ser '{tipo_param}', se recibió '{tipo_arg}'.")

        return sym.type_

    # --- Nodos estructurales -------
    else:
        _check_types(node.left_child, scope,
                     current_table, current_function_type)
        _check_types(node.right_child, scope,
                     current_table, current_function_type)
        return None


def tabla(tree, imprime=True):
    scope = Scope()
    _build_table(tree, scope)

    if imprime:
        _print_scope(scope.global_scope)

    return scope


def _print_scope(table, indent=0):
    pad = "  " * indent
    print(f"{pad}[ Scope: {table.scope_name} ]")
    for sym in table.symbols.values():
        print(f"{pad}  {sym}")
    for child in table.children:
        _print_scope(child, indent + 1)


def semantica(tree, imprime=True):
    scope = tabla(tree, imprime=False)

    _check_types(tree, scope)

    if imprime:
        print("=== Global scope ===")
        for sym in scope.global_scope.symbols.values():
            print(f"  {sym}")

        print("\n=== Function details ===")
        for sym in scope.global_scope.symbols.values():
            if sym.kind == 'function':
                print(f"\n  {sym}")
                print(f"    name:   {sym.name}")
                print(f"    kind:   {sym.kind}")
                print(f"    type:   {sym.type_}")
                print(f"    params: {sym.params}")

        print("\n=== Function scopes ===")
        for child in scope.global_scope.children:
            print(f"  Scope [{child.scope_name}]:")
            for s in child.symbols.values():
                print(f"    {s}")

    return scope
