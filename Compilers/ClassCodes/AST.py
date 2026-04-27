from enum import Enum


class TypeExpression(Enum):
    Op = 0
    Const = 1


class TreeNode:
    def __init__(self):
        self.left_child = None
        self.right_child = None
        self.exp = None  # Tipo de expresión
        self.op = None
        self.val = None


def new_node(type_):
    t = TreeNode()
    if (t == None):
        print("Memory is over")
    else:
        t.exp = type_
    return t


def syntax_error(msg):
    print('>>> syntax error: ' + msg)


def print_spaces():
    print(' '*endentation, end='')


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


def match(c):
    global token, pos
    if token == c:
        pos += 1
        if pos == len(string):
            token = "$"
        else:
            token = string[pos]
        return True
    else:
        syntax_error('Token unexpected')


def exp():
    t = term()
    while token in "+-":
        p = new_node(TypeExpression.Op)
        p.left_child = t
        p.op = token
        t = p
        match(token)
        t.right_child = term()
    return t


def term():
    t = factor()
    while token == "*":
        p = new_node(TypeExpression.Op)
        p.left_child = t
        p.op = token
        t = p
        match(token)
        t.right_child = factor()
    return t


def factor():
    if token in '0123456789':
        t = new_node(TypeExpression.Const)
        t.val = token
        match(token)
    elif token == "(":
        match("(")
        t = exp()
        match(")")
    else:
        syntax_error('Token unexpected')
    return t


string = input("Write an expression: ")
pos = 0
token = string[pos]
AST = exp()
endentation = 0
if token != '$':
    syntax_error('Code ends before file')
else:
    print_AST(AST)
