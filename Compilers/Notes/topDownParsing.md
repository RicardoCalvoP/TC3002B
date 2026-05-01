## Gramática

$$
\begin{array}{lcl}
E \Rightarrow T\ X \\
X \Rightarrow +\ E \mid \epsilon \\
T \Rightarrow int\ Y \mid (E) \\
Y \Rightarrow *\ T \mid \epsilon \\
\end{array}
$$

---

## FIRST y FOLLOW

| Símbolo | FIRST  |   FOLLOW    |
| :-----: | :----: | :---------: |
|    +    |   +    |    int,(    |
|   \*    |   \*   |    int,(    |
|    (    |   (    |    int,(    |
|    )    |   )    |   +, ), $   |
|   int   |  int   | \*, +, ), $ |
|    E    | int, ( |    ), $     |
|    T    | int,(  |   +, ), $   |
|    X    |  +, ε  |    ), $     |
|    Y    | \*, ε  |   +, ), $   |

---

## Notas clave

- `$ ∈ FOLLOW(E)` porque `E` es el símbolo inicial.
- De `T → ( E )` se obtiene `) ∈ FOLLOW(E)`.
- De `E → T X`:
  - `FIRST(X) - {ε} = { + } ⊆ FOLLOW(T)`
  - Como `X → ε`, entonces `FOLLOW(E) ⊆ FOLLOW(T)`
- De `T → int Y`:
  - `FOLLOW(Y) = FOLLOW(T)`
- De `E → T X`:
  - `FOLLOW(X) = FOLLOW(E)`
