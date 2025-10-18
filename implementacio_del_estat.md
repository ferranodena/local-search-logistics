# Implementació de l'estat

## Càlcul del benefici

El benefici total es calcula com els ingressos dels dipòsits servits avui menys els costos de desplaçament, incorporant una penalització pel valor que es perd si es deixen peticions pendents un dia més per la rebaixa del preu aplicable l’endemà.

Cada petició equival a omplir un dipòsit d’una gasolinera; el camió té capacitat per a dos dipòsits, de manera que pot atendre fins a dues peticions per viatge. El preu base serà $P$ i té associat un factor de preu que el modifica en funció dels dies que la petició ha estat pendent. Aquest factor de preu es defineix com:

$$
f(d) = \begin{cases}
  1.02  \text{  si } d = 0 \\
  \max(0,1-0.02 \cdot d) \text{  si } d > 0
\end{cases}
$$

On $d$ és el nombre de dies que la petició ha estat pendent. Així, el preu efectiu per una petició pendent $d$ dies és $P \cdot f(d)$.

Per tant, si $S$ és el conjunt de peticions complertes avui (per a tota la flota de camions), els ingressos totals dels dipòsits servits avui es poden expressar com:

$$
I = \sum_{p \in S}^{n} P \cdot f(d_p)
$$

La distància sobre la quadrícula es calcula amb la mètrica Manhattan:

$$
d_1((x_1, y_1), (x_2, y_2)) = |x_1 - x_2| + |y_1 - y_2|
$$

La llargada total d'un viatge serà:

- Si se serveix una única gasolinera G des d'un centre C: $L = d(C, G) + d(G, C)$
- Si se serveixen dues gasolineres G1 i G2 des d'un centre C: $L = d(C, G1) + d(G1, G2) + d(G2, C)$

Si el cost per quilòmetre és $C_k$, el cost total $C$ per una quantitat de viatges $t$ de llargada $L$ serà:

$$
C = C_k \cdot \sum_{i=1}^{t} L_i
$$

Finalment, el benefici total $B$ es calcula com:

$$
B = I - C
$$

Per tal de minimitzar les penalitzacions i així maximitzar el benefici, definirem una funció que calculi aquesta penalització total, que podem fer servir per comparar diferents estats i com a ajuda a la nostra heurística:

- El preu d'una petició pendent $d$ dies és $P \cdot f(d)$.
- Si no s'atén avui la petició, demà el preu serà $P \cdot f(d+1)$, per tant la pèrdua potencial és: $ \Delta_ u = P \cdot (f(d) - f(d+1))$, on $u$ és la petició pendent.
- Si $U$ és el conjunt de peticions pendents avui, la penalització total $Pen$ es pot expressar com:
    $$
    Pen = \sum_{u \in U} P \cdot (f(d_u) - f(d_u + 1))
    $$

La funció de benefici total, doncs, quedaria:

$$
B_{total} = B - C - Pen
$$

