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
        self.kind = kind    # 'var' | 'array' | 'function'
        self.type_ = type_   # 'int' | 'void'
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
# Scope  (stack manager)
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
    """
    Flatten the param / param_list sub-tree into a list of Symbols.

    Parser structure:
      - Leaf Param  : name is set, represents one parameter.
      - Chain Param : name is None, left_child = earlier params,
                      right_child = next leaf param.
    """
    if param_node is None:
        return []

    if param_node.exp != TypeExpression.Param:
        return []

    if param_node.name is not None:
        # Leaf: one real parameter
        kind = 'array' if param_node.is_array else 'var'
        # .type NOT .type_
        return [Symbol(param_node.name, kind, param_node.type)]
    else:
        # Chain: gather both sides
        return (_collect_params(param_node.left_child) +
                _collect_params(param_node.right_child))


def _build_table(node, scope, enter_compound=False):
    """
    Recursively walk the AST and populate symbol tables.

    enter_compound=True tells the function that this Compound node is a
    real { } block (not a statement-list spine), so it should open a scope.
    The parser reuses TypeExpression.Compound for both purposes:
      - real block  : right_child of FunDeclaration, or a nested { } statement
      - spine node  : chains statements inside statement_list (name=None, no { })
    We distinguish them by passing enter_compound explicitly from FunDeclaration
    and from selection/iteration statements.
    """
    if node is None:
        return

    exp = node.exp

    # --- Program: spine linking top-level declarations ----------------------
    if exp == TypeExpression.Program:
        _build_table(node.left_child,  scope)
        _build_table(node.right_child, scope)

    # --- Variable declaration -----------------------------------------------
    elif exp == TypeExpression.VarDeclaration:
        if node.name is not None:
            # Leaf: real declaration
            kind = 'array' if node.is_array else 'var'
            symbol = Symbol(node.name, kind, node.type)   # .type NOT .type_
            if not scope.define(symbol):
                print(
                    f"Error semántico: '{node.name}' ya fue declarado en este ámbito")
        else:
            # Wrapper chaining two declarations — recurse both sides
            _build_table(node.left_child,  scope)
            _build_table(node.right_child, scope)

    # --- Function declaration -----------------------------------------------
    elif exp == TypeExpression.FunDeclaration:
        param_symbols = _collect_params(node.left_child)

        # Register function in the OUTER (current) scope
        fun_sym = Symbol(node.name, 'function', node.type,   # .type NOT .type_
                         params=param_symbols)
        if not scope.define(fun_sym):
            print(f"Error semántico: función '{node.name}' ya fue declarada")

        # Open a new scope named after the function
        scope.enter_scope(node.name)

        # Register parameters inside the function scope
        for p in param_symbols:
            scope.define(p)

        # Visit the function body — right_child is always a real { } block
        _build_table(node.right_child, scope, enter_compound=True)

        scope.exit_scope()

    # --- Compound statement -------------------------------------------------
    elif exp == TypeExpression.Compound:
        if enter_compound:
            # Real { } block: left_child = local declarations,
            #                 right_child = statement list
            # local declarations
            _build_table(node.left_child,  scope)
            # statements (no new scope)
            _build_table(node.right_child, scope)
        else:
            # Statement-list spine: both children are statements — just recurse
            _build_table(node.left_child,  scope)
            _build_table(node.right_child, scope)

    # --- If statement -------------------------------------------------------
    elif exp == TypeExpression.If:
        # left_child  = condition expression
        # right_child = then-statement (may be a Compound block)
        # wrapper If  : left_child = original If, right_child = else-statement
        _build_table(node.left_child,  scope)
        # The then/else branches can be { } blocks — pass enter_compound
        _build_table(node.right_child, scope,
                     enter_compound=(node.right_child is not None and
                                     node.right_child.exp == TypeExpression.Compound))

    # --- While statement ----------------------------------------------------
    elif exp == TypeExpression.While:
        # left_child = condition, right_child = body statement
        _build_table(node.left_child,  scope)
        _build_table(node.right_child, scope,
                     enter_compound=(node.right_child is not None and
                                     node.right_child.exp == TypeExpression.Compound))

    # --- Everything else (Return, Assign, Op, Id, ArrayId, Call, Const,
    #     ExpressionStmt): just recurse — nothing to declare -------------------
    else:
        _build_table(node.left_child,  scope)
        _build_table(node.right_child, scope)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def tabla(tree, imprime=True):
    """
    Build the symbol table(s) for the given AST.

    Parameters
    ----------
    tree    : root TreeNode from parser()
    imprime : if True, print all scopes and their symbols

    Returns
    -------
    Scope object with the full scope hierarchy.
    """
    scope = Scope()
    _build_table(tree, scope)

    if imprime:
        _print_scope(scope.global_scope)

    return scope


def _print_scope(table, indent=0):
    """Recursively print a Table and all its children."""
    pad = "  " * indent
    print(f"{pad}[ Scope: {table.scope_name} ]")
    for sym in table.symbols.values():
        print(f"{pad}  {sym}")
    for child in table.children:
        _print_scope(child, indent + 1)


def semantica(tree, imprime=True):
    pass
