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

Derivada por al izquierda

$$
\begin{array}{lcl}
S \Rightarrow s;S \\
s;S \Rightarrow s;s; \\
\end{array}
$$

Derivada por al derecha

$$
\begin{array}{lcl}
S \Rightarrow s;S \\
s;S \Rightarrow s;s; \\
\end{array}
$$

---

### 2.2

Dada la gramática:

$$A \rightarrow AA \mid (A) \mid \varepsilon$$

1. Describa el lenguaje que genera.

Esta gramática nos da como resultado una cadena que puede resultar desde vacío $\epsilon$ hasta una cadena de paréntesis ordenados. Estos paréntesis pueden ir unos dentro de otros e incluso unos a lados de otros, pero siempre ordenados con su paréntesis que abre y su paréntesis que cierra.

1. Muestre que es ambigua.

$$
\begin{array}{lcl}
A \Rightarrow AA \\
AA \Rightarrow (A)A \\
(A)A \Rightarrow ()A \\
()A \Rightarrow ()(A) \\
()(A) \Rightarrow ()() \\
\end{array}
$$

$$
\begin{array}{lcl}
A \Rightarrow AA \\
AA \Rightarrow A(A) \\
A(A) \Rightarrow A() \\
A() \Rightarrow (A)() \\
(A)() \Rightarrow ()() \\
\end{array}
$$

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

#### Derivaciones por la izquierda

$$
\begin{array}{lcl}
exp &\Rightarrow& exp\; opsuma\; term \\
    &\Rightarrow& exp\; opsuma\; term\; opsuma\; term \\
    &\Rightarrow& term\; opsuma\; term\; opsuma\; term \\
    &\Rightarrow& factor\; opsuma\; term\; opsuma\; term \\
    &\Rightarrow& \text{número}\; opsuma\; term\; opsuma\; term \\
    &\Rightarrow& 3\; opsuma\; term\; opsuma\; term \\
    &\Rightarrow& 3\; +\; term\; opsuma\; term \\
    &\Rightarrow& 3\; +\; term\; opmult\; factor\; opsuma\; term \\
    &\Rightarrow& 3\; +\; factor\; opmult\; factor\; opsuma\; term \\
    &\Rightarrow& 3\; +\; \text{número}\; opmult\; factor\; opsuma\; term \\
    &\Rightarrow& 3\; +\; 4\; opmult\; factor\; opsuma\; term \\
    &\Rightarrow& 3\; +\; 4\; * factor\; opsuma\; term \\
    &\Rightarrow& 3\; +\; 4\; * \text{número}\; opsuma\; term \\
    &\Rightarrow& 3\; +\; 4\; * 5\; opsuma\; term \\
    &\Rightarrow& 3\; +\; 4\; * 5\; -\; term \\
    &\Rightarrow& 3\; +\; 4\; * 5\; -\; factor \\
    &\Rightarrow& 3\; +\; 4\; * 5\; -\; \text{número} \\
    &\Rightarrow& 3\; +\; 4\; * 5\; -\; 6 \\
\end{array}
$$

#### Árboles de análisis gramatical

```mermaid
graph TD
    E1["exp"] --> E2["exp"]
    E1 --> minus["-"]
    E1 --> T3["term"]

    E2 --> E3["exp"]
    E2 --> plus["+"]
    E2 --> T2["term"]

    E3 --> T1["term"]
    T1 --> F1["factor"]
    F1 --> n3["3"]

    T2 --> T21["term"]
    T2 --> mult["*"]
    T2 --> F3["factor"]

    T21 --> F2["factor"]
    F2 --> n4["4"]

    F3 --> n5["5"]

    T3 --> F4["factor"]
    F4 --> n6["6"]
```

#### Árboles sintácticos abstractos

```mermaid
graph TD
    minus["-"] --> plus["+"]
    minus --> n6["6"]

    plus --> n3["3"]
    plus --> mult["*"]

    mult --> n4["4"]
    mult --> n5["5"]
```

2. `3 * (4 - 5 + 6)`

#### Derivaciones por la izquierda

$$
\begin{array}{lcl}
exp &\Rightarrow& term \\
    &\Rightarrow& term\; opmult\; factor\; \\
    &\Rightarrow& factor\; opmult\; factor\; \\
    &\Rightarrow& \text{número}\; opmult\; factor\; \\
    &\Rightarrow& 3\; opmult\; factor\; \\
    &\Rightarrow& 3\; * factor\; \\
    &\Rightarrow& 3\; * (exp)\; \\
    &\Rightarrow& 3\; * (exp\; opsuma\; term)\; \\
    &\Rightarrow& 3\; * (exp\; opsuma\; term\; opsuma\; term)\; \\
    &\Rightarrow& 3\; * (term\; opsuma\; term\; opsuma\; term)\; \\
    &\Rightarrow& 3\; * (factor\; opsuma\; term\; opsuma\; term)\; \\
    &\Rightarrow& 3\; * (\text{número}\; opsuma\; term\; opsuma\; term)\; \\
    &\Rightarrow& 3\; * (4\; opsuma\; term\; opsuma\; term)\; \\
    &\Rightarrow& 3\; * (4\; -\; term\; opsuma\; term)\; \\
    &\Rightarrow& 3\; * (4\; -\; factor\; opsuma\; term)\; \\
    &\Rightarrow& 3\; * (4\; -\; \text{número}\; opsuma\; term)\; \\
    &\Rightarrow& 3\; * (4\; -\; 5\; opsuma\; term)\; \\
    &\Rightarrow& 3\; * (4\; -\; 5\; +\; term)\; \\
    &\Rightarrow& 3\; * (4\; -\; 5\; +\; factor)\; \\
    &\Rightarrow& 3\; * (4\; -\; 5\; +\; \text{número})\; \\
    &\Rightarrow& 3\; * (4\; -\; 5\; +\; 6)\; \\
\end{array}
$$

#### Árboles de análisis gramatical

```mermaid
graph TD
    E["exp"] --> T["term"]

    T --> T1["term"]
    T --> opm["*"]
    T --> Fp["factor"]

    T1 --> F1["factor"]
    F1 --> n3["número: 3"]

    Fp --> P["(exp)"]
    P --> E2["exp"]

    E2 --> E3["exp"]
    E2 --> plus["+"]
    E2 --> T3["term"]

    E3 --> E4["exp"]
    E3 --> minus["-"]
    E3 --> T2["term"]

    E4 --> T4["term"]
    T4 --> F4["factor"]
    F4 --> n4["número: 4"]

    T2 --> F5["factor"]
    F5 --> n5["número: 5"]

    T3 --> F6["factor"]
    F6 --> n6["número: 6"]


```

#### Árboles sintácticos abstractos

```mermaid
graph TD
    mult["*"] --> n3["3"]
    mult --> minus["-"]

    minus --> plus["+"]
    minus --> n4["4"]

    plus --> n5["5"]
    plus --> n6["6"]
```

3. `3 - (4 + 5 * 6)`

#### Derivaciones por la izquierda

$$
\begin{array}{lcl}
exp &\Rightarrow& exp\; opsuma\; term \\
    &\Rightarrow& term\; opsuma\; term\\
    &\Rightarrow& factor\; opsuma\; term\\
    &\Rightarrow& \text{número}\; opsuma\; term\\
    &\Rightarrow& 3\; opsuma\; term\\
    &\Rightarrow& 3\; -\; term\\
    &\Rightarrow& 3\; -\; factor\\
    &\Rightarrow& 3\; -\; (exp)\\
    &\Rightarrow& 3\; -\; (exp\; opsuma\; term)\\
    &\Rightarrow& 3\; -\; (term\; opsuma\; term)\\
    &\Rightarrow& 3\; -\; (factor\; opsuma\; term)\\
    &\Rightarrow& 3\; -\; (\text{número}\; opsuma\; term)\\
    &\Rightarrow& 3\; -\; (4\; opsuma\; term)\\
    &\Rightarrow& 3\; -\; (4\; +\; term)\\
    &\Rightarrow& 3\; -\; (4\; +\; term\; opmult\; factor)\\
    &\Rightarrow& 3\; -\; (4\; +\; factor\; opmult\; factor)\\
    &\Rightarrow& 3\; -\; (4\; +\; \text{número}\; opmult\; factor)\\
    &\Rightarrow& 3\; -\; (4\; +\; 5\; opmult\; factor)\\
    &\Rightarrow& 3\; -\; (4\; +\; 5\; * factor)\\
    &\Rightarrow& 3\; -\; (4\; +\; 5\; * \text{número})\\
    &\Rightarrow& 3\; -\; (4\; +\; 5\; * 6)\\
\end{array}
$$

#### Árboles de análisis gramatical

```mermaid
graph TD
    E["exp"] --> E1["exp"]
    E --> OS1["opsuma"]
    E --> T2["term"]

    E1 --> T1["term"]
    T1 --> F1["factor"]
    F1 --> N3["número: 3"]

    OS1 --> MINUS["-"]

    T2 --> F2["factor"]
    F2 --> P["(exp)"]
    P --> E2["exp"]

    E2 --> E3["exp"]
    E2 --> OS2["opsuma"]
    E2 --> T4["term"]

    E3 --> T3["term"]
    T3 --> F3["factor"]
    F3 --> N4["número: 4"]

    OS2 --> PLUS["+"]

    T4 --> T5["term"]
    T4 --> OM1["opmult"]
    T4 --> F5["factor"]

    T5 --> F4["factor"]
    F4 --> N5["número: 5"]

    OM1 --> MULT["*"]

    F5 --> N6["número: 6"]
```

#### Árboles sintácticos abstractos

```mermaid
graph TD
    MINUS["-"] --> N3["3"]
    MINUS --> PLUS["+"]

    PLUS --> N4["4"]
    PLUS --> MULT["*"]

    MULT --> N5["5"]
    MULT --> N6["6"]
```

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

$$
   \begin{array}{lcl}
   rexp &\mid& rexp\ "\*" \\
   &\Rightarrow& "("\ rexp ")"* \\
   &\Rightarrow& "("\ rexp\ "\mid"\ rexp\ ")"* \\
   &\Rightarrow& "("\ letra\ "\mid"\ rexp\ ")"* \\
   &\Rightarrow& "("\ a\ "\mid"\ rexp\ ")"* \\
   &\Rightarrow& "("\ a\ "\mid"\ letra\ ")"* \\
   &\Rightarrow& "("\ a\ "\mid"\ b\ ")"* \\
   \end{array}
$$

2. Muestre que esta gramática es ambigua.

Para esta demostración vamos a usar la siguiente cadena `a|bs`

$$
   \begin{array}{lcl}
   rexp &\rightarrow& rexp\ "\mid"\ rexp \\
   rexp &\rightarrow& a\ "\mid"\ rexp \\
   rexp &\rightarrow& a\ "\mid"\ rexp\ rexp \\
   rexp &\rightarrow& a\ "\mid"\ b\ c \\
   \end{array}
$$

$$
   \begin{array}{lcl}
   rexp &\rightarrow& rexp\ rexp \\
   rexp &\rightarrow& rexp\ "\mid"\ rexp\ rexp \\
   rexp &\rightarrow& a\ "\mid"\ rexp\ rexp \\
   rexp &\rightarrow& a\ "\mid"\ b\ c \\
   \end{array}
$$

3. Vuelva a escribir esta gramática para establecer las precedencias correctas para los operadores (véase el capítulo 2).
4. ¿Qué asociatividad da su respuesta en el inciso c para los operadores binarios? Explique su respuesta.
   $$
