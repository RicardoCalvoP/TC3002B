import os
import sys
from enum import Enum

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from Proyect1.lexer import *

"""
---------------------------------------------------
AST node building
---------------------------------------------------
"""
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


def new_node(type_expression):
    node = TreeNode()
    node.exp = type_expression
    return node
"""
---------------------------------------------------
Parser helpers
---------------------------------------------------
"""

def advance_token():
    global token, lexema
    token, lexema = getToken(False)


def match(expected_token):
    if token == expected_token:
        advance_token()
        return True

    syntax_error(f"Token inesperado. Se esperaba {expected_token}")
    return False

"""
---------------------------------------------------
Grammar rules
---------------------------------------------------
"""

def program():
    # program -> declaration_list
    declaration_list()

def declaration_list(something="to be decalred"):
    # declaration_list -> declaration_list declaration | declaration
    declaration(something)
    while token in [TokenType.INT, TokenType.VOID]:
        declaration(something)

def declaration(something="to be decalred"):
    # declaration -> var_declaration | fun_declaration
    if something:
        var_declaration()
    else:
        fun_declaration()

def var_declaration():
    # var_declaration -> type_specifier ID ; | type_specifier ID [ NUM ] ;
    type_specifier()
    match(TokenType.ID)
    if token == TokenType.LBRACKET:
        match(TokenType.LBRACKET)
        match(TokenType.NUM)
        match(TokenType.RBRACKET)
    match(TokenType.SEMICOLON)

def type_specifier():
    # type_specifier -> int | void
    if token == TokenType.INT:
        match(TokenType.INT)
    elif token == TokenType.VOID:
        match(TokenType.VOID)
    else:
        syntax_error("Tipo de dato inesperado")
        advance_token()

def fun_declaration():
    # fun_declaration -> type_specifier ID ( params ) compound_stmt
    type_specifier()
    match(TokenType.ID)
    match(TokenType.LPAREN)
    params()
    match(TokenType.RPAREN)
    compound_stmt()

def params():
    # params -> param_list | void
    if token == TokenType.VOID:
        match(TokenType.VOID)
    else:
        param_list()

def param_list():
    # param_list -> param_list , param | param
    param()
    if token == TokenType.COMMA:
        while token == TokenType.COMMA:
            match(TokenType.COMMA)
            param()

def param():
    # param -> type_specifier ID | type_specifier ID [ ]
    type_specifier()
    match(TokenType.ID)
    if token == TokenType.LBRACKET:
        match(TokenType.LBRACKET)
        match(TokenType.RBRACKET)

def compound_stmt():
    # compound_stmt -> { local_declarations statement_list }
    match(TokenType.LBRACE)
    local_declarations()
    statement_list()
    match(TokenType.RBRACE)

def local_declarations():
    # local_declarations -> local_declarations var_declaration | empty
    while token in [TokenType.INT, TokenType.VOID]:
        var_declaration()

def statement_list():
    # statement_list -> statement_list statement | empty
    while token in [TokenType.IF, TokenType.WHILE, TokenType.RETURN, TokenType.LBRACE, TokenType.ID]:
        statement()

def statement():
    # statement -> expression_stmt | compound_stmt | selection_stmt | iteration_stmt | return_stmt
    if token == TokenType.ID:
        expression_stmt()
    elif token == TokenType.LBRACE:
        compound_stmt()
    elif token == TokenType.IF:
        selection_stmt()
    elif token == TokenType.WHILE:
        iteration_stmt()
    elif token == TokenType.RETURN:
        return_stmt()

def expression_stmt():
    # expression_stmt -> expression ; | ;
    if token != TokenType.SEMICOLON:
        expression()
    match(TokenType.SEMICOLON)

def selection_stmt():
    # selection_stmt -> if ( expression ) statement | if ( expression ) statement else statement
    match(TokenType.IF)
    match(TokenType.LPAREN)
    expression()
    match(TokenType.RPAREN)
    statement()
    if token == TokenType.ELSE:
        match(TokenType.ELSE)
        statement()

def iteration_stmt():
    # iteration_stmt -> while ( expression ) statement
    match(TokenType.WHILE)
    match(TokenType.LPAREN)
    expression()
    match(TokenType.RPAREN)
    statement()

def return_stmt():
    # return_stmt -> return ; | return expression ;
    match(TokenType.RETURN)
    if token != TokenType.SEMICOLON:
        expression()
    match(TokenType.SEMICOLON)

def expression():
    # expression -> var = expression | simple_expression
    if token == TokenType.ID:
        var()
        if token == TokenType.ASSIGN:
            match(TokenType.ASSIGN)
            expression()
    else:
        simple_expression()

def var():
    # var -> ID | ID [ expression ]
    match(TokenType.ID)
    if token == TokenType.LBRACKET:
        match(TokenType.LBRACKET)
        expression()
        match(TokenType.RBRACKET)

def simple_expression():
    # simple_expression -> additive_expression relop additive_expression | additive_expression
    additive_expression()
    if token in [TokenType.LESS, TokenType.LEQ, TokenType.GREATER, TokenType.GEQ, TokenType.EQ, TokenType.NEQ]:
        relop()
        additive_expression()

def relop():
    # relop -> < | <= | > | >= | == | !=
    if token in [TokenType.LESS, TokenType.LEQ, TokenType.GREATER, TokenType.GEQ, TokenType.EQ, TokenType.NEQ]:
        match(token)
    else:
        syntax_error("Operador relacional inesperado")
        advance_token()

def additive_expression():
    # additive_expression -> additive_expression addop term  | term
    term()
    while token in [TokenType.PLUS, TokenType.MINUS]:
        addop()
        term()

def addop():
    # addop -> + | -
    if token in [TokenType.PLUS, TokenType.MINUS]:
        match(token)
    else:
        syntax_error("Operador aditivo inesperado")
        advance_token()

def term():
    # term -> term mulop factor | factor
    factor()
    while token in [TokenType.TIMES, TokenType.DIVIDE]:
        mulop()
        factor()

def mulop():
    # mulop -> * | /
    if token in [TokenType.TIMES, TokenType.DIVIDE]:
        match(token)
    else:
        syntax_error("Operador multiplicativo inesperado")
        advance_token()

def factor():
    # factor -> ( expression ) | var | call | NUM
    if token == TokenType.LPAREN:
        match(TokenType.LPAREN)
        expression()
        match(TokenType.RPAREN)
    elif token == TokenType.ID:
        var()
    elif token == TokenType.NUM:
        match(TokenType.NUM)

def call():
    # call -> ID ( args )
    match(TokenType.ID)
    match(TokenType.LPAREN)
    args()
    match(TokenType.RPAREN)

def args():
    # args -> arg-list | empty
    if token != TokenType.RPAREN:
        arg_list()

def arg_list():
    # arg_list -> arg-list , expression | expression
    expression()
    if token == TokenType.COMMA:
        while token == TokenType.COMMA:
            match(TokenType.COMMA)
            expression()

"""
---------------------------------------------------
Prints
---------------------------------------------------
"""


def print_spaces():
    print(" " * indentation, end="")


def syntax_error(msg):
    print(">>> syntax error:", msg)
    print("Token actual:", token)
    print("Lexema actual:", lexema)


def print_AST(tree):
    global indentation

    indentation += 2

    if tree is not None:
        print_spaces()

        if tree.exp == TypeExpression.Op:
            print("Op:", tree.op)
        elif tree.exp == TypeExpression.Const:
            print("Const:", tree.val)
        elif tree.exp == TypeExpression.Id:
            print("Id:", tree.name)
        else:
            print("ExpNode of this type unknown")

        print_AST(tree.left_child)
        print_AST(tree.right_child)

    indentation -= 2


def parser(imprime=True):
    global token, lexema, indentation

    indentation = 0
    advance_token()

    AST = program()

    if token != TokenType.ENDFILE:
        syntax_error("Code ends before file")
    elif imprime:
        print_AST(AST)

    return AST
