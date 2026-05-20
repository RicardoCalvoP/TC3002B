import os
import sys

from Proyect1.globalTypes import *
from Proyect2.parser import *


class Symbol:
    def __init__(self, name, kind, type_, params=None, lineno=0):
        self.name = name
        self.kind = kind
        self.type_ = type_
        self.params = params or []
        self.lineno = lineno


class Table:
    def __init__(self, scope_name, parent=None):
        self.symbols = {}
        self.scope_name = scope_name
        self.parent = parent
        self.children = []

    def define(self, symbol: Symbol):
        if symbol.name in self.symbols:
            return False

        self.symbols[symbol.name] = symbol
        return True

    def lookup(self, name):
        result = self.symbols.get(name)
        if result is not None:
            return result
        if self.parent is not None:
            return self.parent.lookup(name)
        return None


class Scope:
    def __init__(self):
        self.global_scope = Table("global")
        self.current = self.global_scope
        # Pre-load built-in functions  input() and output()
        self._scopes()

    def _scopes(self):
        input_symbol = Symbol(
            name="input", kind="function", type_="int", params=[])
        output_symbol = Symbol(
            name="output", kind="function", type_="void", params=[Symbol("x", "var", "int")])
        self.global_scope.define(input_symbol)
        self.global_scope.define(output_symbol)

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
# Helpers for tabla
# ---------------------------------------------------------------------------

def _collect_params(param_node):
    """
    Walk the param / param_list sub-tree and return a flat list of Symbols.

    The parser builds param_list as a chain:
        Param node with name=None  ->  left_child = previous params
                                       right_child = one leaf param
    A leaf param node has name set directly.
    """
    if param_node is None:
        return []

    if param_node.exp == TypeExpression.Param:
        if param_node.name is not None:
            # Leaf: this node IS the parameter
            kind = 'array' if param_node.is_array else 'var'
            return [Symbol(param_node.name, kind, param_node.type_)]
        else:
            # Chain node: gather left side + right side
            return (_collect_params(param_node.left_child) +
                    _collect_params(param_node.right_child))

    return []


def _build_table(node, scope):
    """
    Recursively walk the AST and populate symbol tables.
    Detects duplicate declarations and reports them.
    """
    if node is None:
        return

    exp = node.exp

    # --- Variable declaration -----------------------------------------------
    if exp == TypeExpression.VarDeclaration:
        if node.name is not None:
            # Leaf declaration node
            kind = 'array' if node.is_array else 'var'
            symbol = Symbol(node.name, kind, node.type_)
            if not scope.define(symbol):
                print(f"Error: '{node.name}' ya fue declarado en este ámbito")
        else:
            # Wrapper node linking two declarations — recurse both sides
            _build_table(node.left_child, scope)
            _build_table(node.right_child, scope)
        return

    # --- Function declaration -----------------------------------------------
    if exp == TypeExpression.FunDeclaration:
        # 1. Collect params before opening the function scope
        param_symbols = _collect_params(node.left_child)

        # 2. Register the function itself in the CURRENT (outer) scope
        fun_sym = Symbol(node.name, 'function',
                         node.type_, params=param_symbols)
        if not scope.define(fun_sym):
            print(f"Error: función '{node.name}' ya fue declarada")

        # 3. Open a new scope for the function body
        scope.enter_scope(node.name)

        # 4. Register each parameter inside the function scope
        for p in param_symbols:
            scope.define(p)

        # 5. Visit the function body (right_child = compound_stmt)
        _build_table(node.right_child, scope)

        scope.exit_scope()
        return

    # --- Program spine (links multiple top-level declarations) --------------
    if exp == TypeExpression.Program:
        _build_table(node.left_child, scope)
        _build_table(node.right_child, scope)
        return

    # --- Compound statement (opens a nested block scope) --------------------
    if exp == TypeExpression.Compound:
        scope.enter_scope("block")
        _build_table(node.left_child, scope)   # local declarations
        _build_table(node.right_child, scope)  # statement list
        scope.exit_scope()
        return

    # --- Everything else: just recurse into children ------------------------
    _build_table(node.left_child, scope)
    _build_table(node.right_child, scope)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def tabla(tree, imprime=True):
    """
    Build the symbol table(s) for the given AST.
    Returns the Scope object containing the full scope hierarchy.
    """
    scope = Scope()
    _build_table(tree, scope)
    return scope


def semantica(tree, imprime=True):
    pass
