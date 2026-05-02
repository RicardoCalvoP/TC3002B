from Proyect1.lexer import *
import os
import sys
from enum import Enum

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)


"""
---------------------------------------------------
AST node building
---------------------------------------------------
"""


class TypeExpression(Enum):
    Program = 0
    VarDeclaration = 1
    FunDeclaration = 2
    Param = 3
    Compound = 4
    If = 5
    While = 6
    Return = 7
    ExpressionStmt = 8

    Assign = 9
    Op = 10
    Const = 11
    Id = 12
    Call = 13

    ArrayId = 14


class TreeNode:
    def __init__(self):
        self.left_child = None
        self.right_child = None
        self.exp = None

        self.name = None
        self.val = None
        self.op = None
        self.type = None
        self.is_array = False


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
    return declaration_list()


def declaration_list():
    # declaration_list -> declaration_list declaration | declaration
    first_node = declaration()

    while token in [TokenType.INT, TokenType.VOID]:
        node = new_node(TypeExpression.Program)
        node.left_child = first_node
        node.right_child = declaration()
        first_node = node

    return first_node


def declaration():
    # declaration -> var_declaration | fun_declaration
    type_name = type_specifier()
    name = lexema
    match(TokenType.ID)

    if token in [TokenType.SEMICOLON, TokenType.LBRACKET]:
        node = new_node(TypeExpression.VarDeclaration)
        node.name = name
        node.type = type_name
        var_declaration()
        return node

    elif token == TokenType.LPAREN:
        func_node = fun_declaration()
        func_node.name = name
        func_node.type = type_name
        return func_node

    else:
        syntax_error("Expected ;, [, or ( after declaration ID")
        return None


def var_declaration():
    # var_declaration -> type_specifier ID ; | type_specifier ID [ NUM ] ;

    if token == TokenType.LBRACKET:
        match(TokenType.LBRACKET)
        match(TokenType.NUM)
        match(TokenType.RBRACKET)
    match(TokenType.SEMICOLON)


def type_specifier():
    # type_specifier -> int | void
    if token == TokenType.INT:
        match(TokenType.INT)
        return "int"
    elif token == TokenType.VOID:
        match(TokenType.VOID)
        return "void"
    else:
        syntax_error("Tipo de dato inesperado")
        advance_token()


def fun_declaration():
    # fun_declaration -> type_specifier ID ( params ) compound_stmt
    node = new_node(TypeExpression.FunDeclaration)

    match(TokenType.LPAREN)

    node.left_child = params()

    match(TokenType.RPAREN)

    node.right_child = compound_stmt()

    return node


def params():
    # params -> param_list | void
    if token == TokenType.VOID:
        match(TokenType.VOID)
        return None
    else:
        return param_list()


def param_list():
    # param_list -> param_list , param | param
    first_node = param()
    while token == TokenType.COMMA:
        match(TokenType.COMMA)

        node = new_node(TypeExpression.Param)
        node.left_child = first_node
        node.right_child = param()
        first_node = node

    return first_node


def param():
    # param -> type_specifier ID | type_specifier ID [ ]
    node = new_node(TypeExpression.Param)

    type_name = type_specifier()
    node.type = type_name

    node.name = lexema
    match(TokenType.ID)

    if token == TokenType.LBRACKET:
        match(TokenType.LBRACKET)
        match(TokenType.RBRACKET)
        node.is_array = True

    return node


def compound_stmt():
    # compound_stmt -> { local_declarations statement_list }
    node = new_node(TypeExpression.Compound)

    match(TokenType.LBRACE)

    node.left_child = local_declarations()
    node.right_child = statement_list()

    match(TokenType.RBRACE)

    return node


def local_declarations():
    # local_declarations -> local_declarations var_declaration | empty
    first_node = None

    while token in [TokenType.INT, TokenType.VOID]:
        type_name = type_specifier()
        name = lexema
        match(TokenType.ID)

        node = new_node(TypeExpression.VarDeclaration)
        node.name = name
        node.type = type_name
        var_declaration()

        if first_node is None:
            first_node = node
        else:
            declaration_wrapper = new_node(TypeExpression.VarDeclaration)
            declaration_wrapper.left_child = first_node
            declaration_wrapper.right_child = node
            first_node = declaration_wrapper

    return first_node


def statement_list():
    # statement_list -> statement_list statement | empty
    first_node = None
    while token in [TokenType.IF, TokenType.WHILE, TokenType.RETURN,
                    TokenType.LBRACE, TokenType.ID, TokenType.NUM,
                    TokenType.LPAREN, TokenType.SEMICOLON]:
        first_statement = statement()
        if first_node is None:
            first_node = first_statement
        else:
            node = new_node(TypeExpression.Compound)
            node.left_child = first_node
            node.right_child = first_statement
            first_node = node

    return first_node


def statement():
    # statement -> expression_stmt | compound_stmt | selection_stmt | iteration_stmt | return_stmt
    if token in [TokenType.ID, TokenType.NUM, TokenType.LPAREN, TokenType.SEMICOLON]:
        return expression_stmt()
    elif token == TokenType.LBRACE:
        return compound_stmt()
    elif token == TokenType.IF:
        return selection_stmt()
    elif token == TokenType.WHILE:
        return iteration_stmt()
    elif token == TokenType.RETURN:
        return return_stmt()


def expression_stmt():
    # expression_stmt -> expression ; | ;
    if token != TokenType.SEMICOLON:
        node = expression()
    else:
        node = None

    match(TokenType.SEMICOLON)
    return node


def selection_stmt():
    # selection_stmt -> if ( expression ) statement | if ( expression ) statement else statement
    node = new_node(TypeExpression.If)

    match(TokenType.IF)
    match(TokenType.LPAREN)

    node.left_child = expression()

    match(TokenType.RPAREN)

    then_node = statement()

    if token == TokenType.ELSE:
        match(TokenType.ELSE)
        else_node = statement()

        wrapper = new_node(TypeExpression.If)
        wrapper.left_child = node
        wrapper.right_child = else_node
        node.right_child = then_node
        return wrapper

    node.right_child = then_node
    return node


def iteration_stmt():
    # iteration_stmt -> while ( expression ) statement
    node = new_node(TypeExpression.While)

    match(TokenType.WHILE)
    match(TokenType.LPAREN)

    node.left_child = expression()

    match(TokenType.RPAREN)

    node.right_child = statement()

    return node


def return_stmt():
    # return_stmt -> return ; | return expression ;
    node = new_node(TypeExpression.Return)
    match(TokenType.RETURN)

    if token != TokenType.SEMICOLON:
        node.right_child = expression()

    match(TokenType.SEMICOLON)

    return node


def expression():
    # expression -> var = expression | simple_expression
    if token == TokenType.ID:
        name = lexema
        match(TokenType.ID)

        if token == TokenType.LPAREN:
            first_node = call(name)
            return simple_expression(first_node)

        else:
            first_node = new_node(TypeExpression.Id)
            first_node.name = name

            if token == TokenType.LBRACKET:
                first_node.exp = TypeExpression.ArrayId
                var(first_node)

            if token == TokenType.ASSIGN:
                assign_node = new_node(TypeExpression.Assign)
                assign_node.left_child = first_node

                match(TokenType.ASSIGN)

                assign_node.right_child = expression()
                return assign_node

            return simple_expression(first_node)

    else:
        return simple_expression()


def var(node):
    # var -> ID | ID [ expression ]
    if token == TokenType.LBRACKET:
        match(TokenType.LBRACKET)
        node.left_child = expression()
        match(TokenType.RBRACKET)
        return node


def simple_expression(first_node=None):
    # simple_expression -> additive_expression relop additive_expression | additive_expression
    node = additive_expression(first_node)

    if token in [TokenType.LT, TokenType.LTEQ, TokenType.GT,
                 TokenType.GTEQ, TokenType.EQ, TokenType.NEQ]:
        op_node = new_node(TypeExpression.Op)
        op_node.op = lexema
        op_node.left_child = node

        relop()

        op_node.right_child = additive_expression()
        node = op_node

    return node


def relop():
    # relop -> < | <= | > | >= | == | !=
    if token in [TokenType.LT, TokenType.LTEQ, TokenType.GT, TokenType.GTEQ, TokenType.EQ, TokenType.NEQ]:
        match(token)
    else:
        syntax_error("Operador relacional inesperado")
        advance_token()


def additive_expression(first_node=None):
    # additive_expression -> additive_expression addop term | term
    node = term(first_node)

    while token in [TokenType.PLUS, TokenType.MINUS]:
        op_node = new_node(TypeExpression.Op)
        op_node.op = lexema
        op_node.left_child = node

        addop()

        op_node.right_child = term()
        node = op_node

    return node


def addop():
    # addop -> + | -
    if token in [TokenType.PLUS, TokenType.MINUS]:
        match(token)
    else:
        syntax_error("Operador aditivo inesperado")
        advance_token()


def term(first_node=None):
    # term -> term mulop factor | factor
    if first_node is not None:
        node = first_node
    else:
        node = factor()

    while token in [TokenType.TIMES, TokenType.DIVIDE]:
        op_node = new_node(TypeExpression.Op)
        op_node.op = lexema
        op_node.left_child = node

        mulop()

        op_node.right_child = factor()
        node = op_node

    return node


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
        node = expression()
        match(TokenType.RPAREN)
        return node

    elif token == TokenType.ID:
        name = lexema  # Save the name of the ID for later use in the AST
        match(TokenType.ID)

        if token == TokenType.LBRACKET:
            node = new_node(TypeExpression.ArrayId)
            node.name = name
            var(node)
            return node

        elif token == TokenType.LPAREN:
            return call(name)

        else:
            node = new_node(TypeExpression.Id)
            node.name = name
            return node

    elif token == TokenType.NUM:
        node = new_node(TypeExpression.Const)
        node.val = lexema
        match(TokenType.NUM)
        return node

    else:
        syntax_error("Unexpected token in factor")
        advance_token()
        return None


def call(name):
    # call -> ID ( args )
    node = new_node(TypeExpression.Call)
    node.name = name  # Save the name of the function being called for later use in the AST

    match(TokenType.LPAREN)
    node.left_child = args()
    match(TokenType.RPAREN)
    return node


def args():
    # args -> arg-list | empty
    if token != TokenType.RPAREN:
        return arg_list()
    return None  # Return None for empty args


def arg_list():
    # arg_list -> arg-list , expression | expression
    firstExpression = expression()
    if token == TokenType.COMMA:
        match(TokenType.COMMA)
        node = new_node(TypeExpression.ExpressionStmt)
        node.left_child = firstExpression
        node.right_child = arg_list()
        return node

    return firstExpression


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


def node_label(tree):
    if tree.exp == TypeExpression.Op:
        return f"Op: {tree.op}"
    elif tree.exp == TypeExpression.Const:
        return f"Const: {tree.val}"
    elif tree.exp == TypeExpression.Id:
        return f"Id: {tree.name}"
    elif tree.exp == TypeExpression.ArrayId:
        return f"ArrayId: {tree.name}"
    elif tree.exp == TypeExpression.Assign:
        return "Assign"
    elif tree.exp == TypeExpression.Call:
        return f"Call: {tree.name}"
    elif tree.exp == TypeExpression.VarDeclaration:
        return f"VarDecl: {tree.type} {tree.name}"
    elif tree.exp == TypeExpression.FunDeclaration:
        return f"FunDecl: {tree.type} {tree.name}"
    elif tree.exp == TypeExpression.Param:
        suffix = "[]" if tree.is_array else ""
        return f"Param: {tree.type} {tree.name}{suffix}"
    elif tree.exp == TypeExpression.Compound:
        return "Compound"
    elif tree.exp == TypeExpression.If:
        return "If"
    elif tree.exp == TypeExpression.While:
        return "While"
    elif tree.exp == TypeExpression.Return:
        return "Return"
    elif tree.exp == TypeExpression.Program:
        return "Program"
    elif tree.exp == TypeExpression.ExpressionStmt:
        return "ExpressionStmt"
    else:
        return "Unknown"


def print_AST(tree, prefix="", is_left=True):
    if tree is None:
        return

    connector = "|---- " if is_left else "`---- "
    print(prefix + connector + node_label(tree))

    child_prefix = prefix + ("|     " if is_left else "      ")

    if tree.left_child is not None:
        print_AST(tree.left_child, child_prefix, True)

    if tree.right_child is not None:
        print_AST(tree.right_child, child_prefix, False)


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
