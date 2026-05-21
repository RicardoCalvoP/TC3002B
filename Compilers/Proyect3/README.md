<div style="text-align: center;">
<h1>Project 3</h1>
<h2>Semantic Analyzer</h2>
<h6>Language C-</h6>
</div>

<h3>Description</h3>

Create a program in Python, called `semantica.py` that contains two functions:

- `tabla(tree, imprime = True)`
  - Receives `tree`, the Abstract Syntax Tree (AST) created by the parser (Project 2), and a variable `imprime` which is `True` by default.
  - If `imprime` is `True`, it must print the generated symbol table(s).
  - Generates one symbol table per block.

- `semantica(tree, imprime = True)`
  - Receives `tree`, the Abstract Syntax Tree (AST) created by the parser (Project 2), and a variable `imprime` which is `True` by default.
  - Passes the `imprime` value when calling `tabla`.
  - Calls the `tabla` function and uses the generated symbol table(s).
  - Uses logical type inference rules to implement the semantics of C-.

Afterwards, continue with the definition of the two main functions and all required auxiliary functions.

<h3>Error detection and recovery</h3>

If the semantic analyzer finds an error (remember that the semantic analyzer only detects errors related to identifier declarations and expression types), it must indicate the line and token where the error was found.

For example, if line 22 of the file is:

```c
if (contador + fact(n)) then
```

And the analyzer detects that the function `fact` is not of type `int` but `void`, it must generate a semantic error because the expression cannot be evaluated.

Example error message:

```py
Line 22: Error in expression type:
if (contador + fact(n)) then
             ^
```

Where the line number is indicated and the caret (`^`) points as closely as possible to the token where the error was detected.

After this, the analyzer must implement an error recovery mechanism. For example, it may assume that the `void` type is correct and continue the analysis from that point. Of course, the correctness of subsequent detections is not guaranteed and depends on the recovery strategy and the programmer's intended code.

<h3>Program testing</h3>

All files necessary for execution (including `lexer.py`, `parser.py`, and the test file) will be placed in the same folder to avoid additional paths.

The semantic analyzer will be tested using a script that imports both the global types file and the semantic analyzer file. Afterwards, it will invoke the parser, assign its result to an `AST` variable, and then invoke the semantic analyzer.

The function `parser(imprime)` must manage the following global variables:

`posicion`: contains the position of the next character in the string being analyzed. It must be modifiable.

`progLong`: contains the length of the program. It will only be read when required.

`programa`: contains the complete program string. It will only be read when required.

Due to how Python handles variable definitions and imports, the only way to pass these global variables is through a function that receives them and assigns them to the global variables used by the program.

The function for passing global values must be added to the program and should have the following structure:

```py
def globales(prog, pos, long):
    global programa
    global posicion
    global progLong
    programa = prog
    posicion = pos
    progLong = long
```

The testing script will be the following:

```py
from globalTypes import *
from Parser import *
from semantica import *

f = open('sample.c-', 'r')
programa = f.read()          # reads the complete file
progLong = len(programa)     # original program length
programa = programa + '$'    # append EOF character
posicion = 0                 # current character position

# function to pass initial global variable values
globales(programa, posicion, progLong)

AST = parser(True)
semantica(AST, True)
```

<h3>For submission</h3>

- A document containing:
  - The logical type inference rules used to implement the semantic analyzer.
  - An explanation of the symbol table structure (and stack, if used).

- All necessary Python (commented) and TXT files required for execution.

A user manual is not required because the C- language definition and the testing procedure have already been provided.

If this project were delivered to a third party, it would be essential to provide the full language definition and detailed instructions for using the lexical analyzer.

<h3>Final Note</h3>

Although some tools exist, none of them has become a standard for the automatic generation of semantic analyzers (such as Lex or Yacc for previous compiler stages). Therefore, in this third project, the use of this type of tool is NOT allowed.
