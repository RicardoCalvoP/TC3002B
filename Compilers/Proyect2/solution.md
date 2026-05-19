<div align="center">

<img src="https://wiki.labnuevoleon.mx/images/4/4b/Tec-de-monterrey-logo.png" alt="Gymiq logo" width="400"/>

## INSTITUTO TECNOLÓGICO Y DE ESTUDIOS SUPERIORES DE MONTERREY

**Campus Santa Fe**

# Project 2

### Desarrollo de aplicaciones avanzadas de ciencias computacionales

**Group 501**

Student
Ricardo Alfredo Calvo Pérez - A01028889

Professor
Victor Manuel de la Cueva Hernández

_April 2026_

</div>

$$
\begin{array}{lcl}
program &\Rightarrow& declaration\_list \\
declaration\_list &\Rightarrow& declaration\_list\ declaration \mid declaration \\
declaration &\Rightarrow& var\_declaration \mid fun\_declaration \\
var\_declaration &\Rightarrow& type\_specifier\ ID\ ; \mid type\_specifier\ ID\ [\ NUM\ ]\ ; \\
type\_specifier &\Rightarrow& int \mid void \\
fun\_declaration &\Rightarrow& type\_specifier\ ID\ (\ params\ )\ compound\_stmt \\
params &\Rightarrow& param\_list \mid void \\
param\_list &\Rightarrow& param\_list\ ,\ param \mid param \\
param &\Rightarrow& type\_specifier\ ID \mid type\_specifier\ ID\ [\ ] \\
compound\_stmt &\Rightarrow& \{\ local\_declarations\ statement\_list\ \} \\
local\_declarations &\Rightarrow& local\_declarations\ var\_declaration \mid \varepsilon \\
statement\_list &\Rightarrow& statement\_list\ statement \mid \varepsilon \\
statement &\Rightarrow& expression\_stmt \mid compound\_stmt \mid selection\_stmt \mid iteration\_stmt \mid return\_stmt \\
expression\_stmt &\Rightarrow& expression\ ; \mid ; \\
selection\_stmt &\Rightarrow& if\ (\ expression\ )\ statement \mid if\ (\ expression\ )\ statement\ else\ statement \\
iteration\_stmt &\Rightarrow& while\ (\ expression\ )\ statement \\
return\_stmt &\Rightarrow& return\ ; \mid return\ expression\ ; \\
expression &\Rightarrow& var\ =\ expression \mid simple\_expression \\
var &\Rightarrow& ID \mid ID\ [\ expression\ ] \\
simple\_expression &\Rightarrow& additive\_expression\ relop\ additive\_expression \mid additive\_expression \\
relop &\Rightarrow& < \mid \leq \mid > \mid \geq \mid == \mid \neq \\
additive\_expression &\Rightarrow& additive\_expression\ addop\ term \mid term \\
addop &\Rightarrow& + \mid - \\
term &\Rightarrow& term\ mulop\ factor \mid factor \\
mulop &\Rightarrow& * \mid / \\
factor &\Rightarrow& (\ expression\ ) \mid var \mid call \mid NUM \\
call &\Rightarrow& ID\ (\ args\ ) \\
args &\Rightarrow& arg\_list \mid \varepsilon \\
arg\_list &\Rightarrow& arg\_list\ ,\ expression \mid expression \\
\end{array}
$$

Text to test:

```c-
int main(void) {
    int x;
    x = 7 + (1 - 2) + 6;

    if (x > 5) {
        x = x - 1;
    } else {
        x = x + 1;
    }

    while (x < 10) {
        x = x + 1;
    }

    return x;
}
```