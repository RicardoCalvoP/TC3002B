<div align="center">

<img src="https://wiki.labnuevoleon.mx/images/4/4b/Tec-de-monterrey-logo.png" alt="Gymiq logo" width="400"/>

## INSTITUTO TECNOLÓGICO Y DE ESTUDIOS SUPERIORES DE MONTERREY

**Campus Santa Fe**

# Project 1

### Desarrollo de aplicaciones avanzadas de ciencias computacionales

**Group 501**

Student
Ricardo Alfredo Calvo Pérez - A01028889

Professor
Victor Manuel de la Cueva Hernández

_April 2026_

</div>

<h4>DFA</h4>

```dot
digraph finite_state_machine {
	fontname="Helvetica,Arial,sans-serif"
	node [fontname="Helvetica,Arial,sans-serif"]
	edge [fontname="Helvetica,Arial,sans-serif"]
	rankdir=LR;
node [shape = doublecircle]; 20; 21; 22; 23; 24; 25; 26; 27; 28; 29; 30; 31; 40; 41; 42; 43; 44; 45; 46; 47; 48; 49; 90; 91; 92; 93; 94;
	node [shape = circle];
	0 -> 0 [label = "blank"];
	0 -> 1 [label = "[0-9]"];
  0 -> 2 [label = "[a-zA-Z]"];
	0 -> 3 [label = "/"];
	0 -> 4 [label = "<"];
	0 -> 5 [label = ">"];
	0 -> 6 [label = "="];
	0 -> 7 [label = "!"];

	// COMMENT START
  3 -> 8 [label = "*"];
	// IN COMMENT
	8 -> 8 [label = "not '*'"]
	// SEE END COMMENT
	8 -> 9 [label = "*"]
	// IN END COMMENT
	9 -> 9 [label = "*"]
	// BACK IN COMMENT
	9 -> 8 [label = "not '/'"]
	// COMMENT END
	9 -> 0 [label = "/"]

	0 -> 20  [label = "*"];
	0 -> 21 [label = "+"];
	0 -> 22 [label = "-"];
	0 -> 23 [label = ";"];
	0 -> 24 [label = ","];
	0 -> 25 [label = "("];
	0 -> 26 [label = ")"];
	0 -> 27 [label = "{"];
	0 -> 28 [label = "}"];
	0 -> 29 [label = "["];
	0 -> 30 [label = "]"];
	0 -> 31 [label = "EOF"];

	# START ERROR
	0 -> 90 [label = "invalid caracter"];
	# NUM ERROR
	1 -> 91 [label = "[a-zA-Z]"];
	# ID ERROR
	2 -> 92 [label = "[0-9]"];
	# BANG ERROR
	7 -> 93 [label = "not '='"]
	# COMMENT ERROR
	8 -> 94 [label = "EOF"]
	9 -> 94 [label = "EOF"]

	1 -> 1 [label = "[0-9]"]
	// NUM
  1 -> 40 [label = "blank | special symbol | EOF"];

	2 -> 2 [label = "[a-zA-Z]"]
	// ID
  2 -> 41 [label = "blank | special symbol | EOF"];

	// DIV
  3 -> 42 [label = "not '*'"];

	// LT
	4 -> 43 [label = "not '='"]
	// LTEQ
	4 -> 44 [label = "="]

	// GT
	5 -> 45 [label = "not '='"]
	// GTEQ
	5 -> 46 [label = "="]

	// ASSIGN
	6 -> 47 [label = "not '='"]
	// EQ
	6 -> 48 [label = "="]
	// NEQ
	7 -> 49 [label = "="]

}
```

<h4>States Table</h4>

|     Meaning     | State | blank | letter | digit |  /  | \*  |  <  |  >  |  =  |  !  |  +  |  -  |  ;  |  ,  |  (  |  )  |  {  |  }  |  [  |  ]  | EOF | other |
| :-------------: | :---: | :---: | :----: | :---: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :---: |
|      START      |   0   |   0   |   2    |   1   |  3  | 20  |  4  |  5  |  6  |  7  | 21  | 22  | 23  | 24  | 25  | 26  | 27  | 28  | 29  | 30  | 31  |  90   |
|     IN_NUM      |   1   |  40   |   91   |   1   | 40  | 40  | 40  | 40  | 40  | 40  | 40  | 40  | 40  | 40  | 40  | 40  | 40  | 40  | 40  | 40  | 40  |  91   |
|      IN_ID      |   2   |  41   |   2    |  92   | 41  | 41  | 41  | 41  | 41  | 41  | 41  | 41  | 41  | 41  | 41  | 41  | 41  | 41  | 41  | 41  | 41  |  92   |
|    SAW_SLASH    |   3   |  42   |   42   |  42   | 42  |  8  | 42  | 42  | 42  | 42  | 42  | 42  | 42  | 42  | 42  | 42  | 42  | 42  | 42  | 42  | 42  |  90   |
|     SAW_LT      |   4   |  43   |   43   |  43   | 43  | 43  | 43  | 43  | 44  | 43  | 43  | 43  | 43  | 43  | 43  | 43  | 43  | 43  | 43  | 43  | 43  |  90   |
|     SAW_GT      |   5   |  45   |   45   |  45   | 45  | 45  | 45  | 45  | 46  | 45  | 45  | 45  | 45  | 45  | 45  | 45  | 45  | 45  | 45  | 45  | 45  |  90   |
|     SAW_EQ      |   6   |  47   |   47   |  47   | 47  | 47  | 47  | 47  | 48  | 47  | 47  | 47  | 47  | 47  | 47  | 47  | 47  | 47  | 47  | 47  | 47  |  90   |
|    SAW_BANG     |   7   |  93   |   93   |  93   | 93  | 93  | 93  | 93  | 49  | 93  | 93  | 93  | 93  | 93  | 93  | 93  | 93  | 93  | 93  | 93  | 93  |  90   |
|   IN_COMMENT    |   8   |   8   |   8    |   8   |  8  |  9  |  8  |  8  |  8  |  8  |  8  |  8  |  8  |  8  |  8  |  8  |  8  |  8  |  8  |  8  | 94  |   8   |
| SEE_END_COMMENT |   9   |   8   |   8    |   8   |  0  |  9  |  8  |  8  |  8  |  8  |  8  |  8  |  8  |  8  |  8  |  8  |  8  |  8  |  8  |  8  | 94  |   8   |

> [!NOTE]
> If the DFA or State table doesn't look properly please consider checking the original file in Markdown here: [Original File](https://github.com/RicardoCalvoP/TC3002B/blob/master/Compilers/Proyect1/solution.md)
