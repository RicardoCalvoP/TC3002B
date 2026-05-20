from enum import Enum, auto


def globales(prog, pos, long):
    global programa
    global posicion
    global progLong
    programa = prog
    posicion = pos
    progLong = long


class TokenType(Enum):
    # reseved words
    ELSE = 'else'
    IF = 'if'
    INT = 'int'
    RETURN = 'return'
    VOID = 'void'
    WHILE = 'while'
    # symbols
    PLUS = '+'
    MINUS = '-'
    TIMES = '*'
    DIVIDE = '/'
    LT = '<'  # Less Than
    LTEQ = '<='  # Less Than or Equal To
    GT = '>'  # Greater Than
    GTEQ = '>='  # Greater Than or Equal To
    EQ = '=='  # Equal To
    NEQ = '!='  # Not Equal To
    ASSIGN = '='  # Assignment
    SEMICOLON = ';'  # Semicolon
    COMMA = ','  # Comma
    LPAREN = '('  # Left Parenthesis
    RPAREN = ')'  # Right Parenthesis
    LBRACE = '{'  # Left Brace
    RBRACE = '}'  # Right Brace
    RBRACKET = ']'  # Right Bracket
    LBRACKET = '['  # Left Bracket
    LCOMMENT = '/*'  # Left Comment
    RCOMMENT = '*/'  # Right Comment
    # other tokens
    ID = 'id'
    NUM = 'num'
    ENDFILE = 'endfile'
    ERROR = 'error'


"""
====================================================
Sintactic Categories
====================================================
"""


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
