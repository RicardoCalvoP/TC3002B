<div align="center">

<img src="https://wiki.labnuevoleon.mx/images/4/4b/Tec-de-monterrey-logo.png" alt="Gymiq logo" width="400"/>

## INSTITUTO TECNOLÓGICO Y DE ESTUDIOS SUPERIORES DE MONTERREY

**Campus Santa Fe**

# Tarea 2: Gramáticas

### Desarrollo de aplicaciones avanzadas de ciencias computacionales

**Group 501**

Student
Ricardo Alfredo Calvo Pérez - A01028889

Professor
Victor Manuel de la Cueva Hernández

_April 2026_

</div>

### 2.1

a. Escriba una gramática no ambigua que genere el conjunto de cadenas

$${ s;,\space s;s;,\space s;s;s;,\space s;s;s;s;, \dots}$$

$$S \rightarrow s;|s;  S$$

b. Dé una derivación por la izquierda y por la derecha para la cadena `s;s;` utilizando su gramática.

---

### 2.2

Dada la gramática:

$$A \rightarrow AA \mid (A) \mid \varepsilon$$

1. Describa el lenguaje que genera.
1. Muestre que es ambigua.

---

### 2.3

Dada la gramática:

$$
\begin{array}{lcl}
exp &\rightarrow& exp\; opsuma\; term \mid term \\
opsuma &\rightarrow& + \mid - \\
term &\rightarrow& term\; opmult\; factor \mid factor \\
opmult &\rightarrow& * \\
factor &\rightarrow& (exp) \mid \text{número}
\end{array}
$$

Escriba derivaciones por la izquierda, árboles de análisis gramatical y árboles sintácticos abstractos para las siguientes expresiones:

1. `3 + 4 * 5 - 6`
1. `3 * (4 - 5 + 6)`
1. `3 - (4 + 5 * 6)`

---

### 2.4

La gramática siguiente genera todas las expresiones regulares sobre el alfabeto de letras
(utilizamos comillas para encerrar operadores, puesto que la barra vertical también es un operador además de un metasímbolo):

$$
\begin{array}{lcl}
rexp &\rightarrow& rexp\; "\mid"\; rexp \\
 &\mid& rexp\; rexp \\
 &\mid& rexp\; "*" \\
 &\mid& "("\; rexp\; ")" \\
 &\mid& letra
\end{array}
$$

1. Proporcione una derivación para la expresión regular `(a|b)*` utilizando esta gramática.
1. Muestre que esta gramática es ambigua.
1. Vuelva a escribir esta gramática para establecer las precedencias correctas para los operadores (véase el capítulo 2).
1. ¿Qué asociatividad da su respuesta en el inciso c para los operadores binarios? Explique su respuesta.
