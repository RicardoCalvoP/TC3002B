from ..Proyect1.lexer import *
from enum import Enum


class TypeExpression(Enum):
    Op = 0
    Const = 1
    Id = 2


class TreeNode:
    def __init__(self):
        self.left_child = None
        self.right_child = None
        self.exp = None
        self.op = None
        self.val = None
        self.name = None


def new_node(type_):
    node = TreeNode()
    if (node == None):
        print("Memory is over")
    else:
        node.exp = type_
    return node


def advance():
    global token, lexema
    token, lexema = getToken(False)


def match(expected):
    global token

    if token == expected:
        advance()
        return True
    else:
        syntax_error(f"Token inesperado. Se esperaba {expected}")
        return False


def exp():
    t = term()

    while token in [TokenType.PLUS, TokenType.MINUS]:
        p = new_node(TypeExpression.Op)
        p.left_child = t
        p.op = lexema
        t = p

        match(token)

        t.right_child = term()

    return t


def term():
    t = factor()

    while token in [TokenType.TIMES, TokenType.DIVIDE]:
        p = new_node(TypeExpression.Op)
        p.left_child = t
        p.op = lexema
        t = p

        match(token)

        t.right_child = factor()

    return t


def factor():
    if token == TokenType.NUM:
        t = new_node(TypeExpression.Const)
        t.val = lexema
        match(TokenType.NUM)
        return t

    elif token == TokenType.ID:
        t = new_node(TypeExpression.Id)
        t.name = lexema
        match(TokenType.ID)
        return t

    elif token == TokenType.LPAREN:
        match(TokenType.LPAREN)
        t = exp()
        match(TokenType.RPAREN)
        return t

    else:
        syntax_error("Token inesperado en factor")
        advance()
        return None


def print_spaces():
    print(' '*endentation, end='')


def syntax_error(msg, line):
    print(">>> syntax error:", msg, "in line", line)
    print("Token actual:", token)
    print("Lexema actual:", lexema)


def print_AST(tree):
    global endentation
    endentation += 2
    if tree != None:
        print_spaces()
        if tree.exp == TypeExpression.Op:
            print('Op: ', tree.op)
        elif tree.exp == TypeExpression.Const:
            print('Const: ', tree.val)
        else:
            print('ExpNode of this type unknown')
        print_AST(tree.left_child)
        print_AST(tree.right_child)
    endentation -= 2


def parser(imprime=True):
    global token, lexema, indentation

    indentation = 0
    advance()

    AST = exp()

    if token != TokenType.ENDFILE:
        syntax_error("Code ends before file")
    else:
        if imprime:
            print_AST(AST)

    return AST
