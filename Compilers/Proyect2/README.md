<div style="text-align: center;">
<h1>Project 2</h1>
<h2>Syntax Analyzer</h2>
<h6>Language C-</h6>
</div>

<h3>Description</h3>
Create a program in Python, called `Parser.py` that contains a function called `parser(print = true)`, which receives a boolean flag `print`, with default value true (its use is explained later) and returns the Abstract Syntax Tree (AST, for its acronym in English) or an error message.

Use the Top-Down Recursive Descent algorithm. Your function, when it needs the next token, will call your function `getToken`, that you implemented in your `lexer`.

The program `Parser.py`, at the beginning, must import the file that contains the `lexer`:
`from lexer import \*`

Afterwards, it will continue with the definition of the function `parser(print = true)` and all the auxiliary functions that it requires.

The function `parser(print = true)`

• It must declare the <u>global variables</u> that it requires so that your `lexer` works (see the “program testing” section).

• By means of these variables it will be able to handle the text file containing a program in C- that is to be analyzed.

• If the flag `print` is true, the function must print at the end, the generated AST, simply with indentation per node, that is, the children of a node indented with respect to its parent.

<h3>Error detection and recovery</h3>

If the syntax analyzer finds an error (remember that the syntax analyzer only finds errors in the structure of the program with respect to the tokens), it must mark the line and the place (token) where it found the error. For example, if line 22 of the file is:

`counter += counter + index`

It receives the token: **(ID, “counter”)**

And when receiving the token: **(PLUS, “+”)**

It will mark an error, sending a message such as for example (knowing that after the identifier there must follow an assignment):

```py
Line 22: Error in the assignment expression:
counter += counter + index
        ^
```

Where the line number is indicated and the caret (^) will indicate the position of the token where it found the error.

After this, it must have a mechanism to try to **recover from the error** (remember that it is recommended to implement the “panic button” method, to traverse the following tokens until finding one that makes sense again) and continue with the syntax analysis. Of course, nothing guarantees the accuracy of what is detected afterwards, which will depend on the mechanism used and, above all, on the intention that the programmer had when writing the code, which we completely do not know and we can only suppose.

<h3>Program testing</h3>

All the files necessary for it to run (all those that are delivered in Bb, including `lexer.py` and the one that contains the test file) will be placed in the same folder to avoid the use of additional paths.

The syntax analyzer will be tested with a script that will begin by importing both the file with the global types and the one that contains your syntax analyzer. Afterwards it will continue invoking your function to obtain the AST, with the print option activated, until the file ends, that is, until it reaches the token that indicates the end of file.

The function `parser(print)` must handle the following global variables:

`position`: contains the position of the next character of the string that must be analyzed. It must be able to modify it in its operation.

`progLong`: contains the length of the program. It will only read it when required.

`program`: contains the string of the complete program. It will only read it when required.

Due to the way in which Python works when defining variables and making `imports`, the only way we have to pass these global variables will be by means of a function that receives them and passes the received value to the global variables that your program uses.

The function for passing global values <u>must be added to your program</u> and will have the following form:

```py
def globales(prog, pos, long):
  global program
  global position
  global progLong
  program = prog
  position = pos
  progLong = long
```

The script with which it is tested will be the following:

```py
from globalTypes import *
from Parser import *

f = open('sample.c-', 'r')
program = f.read() # reads the entire file to compile
progLong = len(program) # original length of the program
program = program + '$' # add a character $ that represents EOF
position = 0 # position of the current character of the string

# function to pass the initial values of the global variables
globales(program, position, progLong)

AST = parser(True)
```

<h3>For the submission</h3>

• A document with:

o The grammar in the form in which it was used to program the parser.

• All the Python (commented) and TXT files necessary for it to run.

The appropriate grammar for the implementation can be created manually, as long as it accepts correct C- programs.

The user manual will not be necessary because the definition of the C- language and the way in which the program will be tested has already been given.

If this project were to be delivered to a third party, it is essential to deliver the entire definition of the language and the way in which the user must use the lexical analyzer, step by step.
