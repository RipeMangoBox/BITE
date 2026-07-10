<!-- part 11/15 chars 63695-71523 -->

\lambda _ { k } ) } ] u _ { k } ^ { \top } X _ { : i } + O ( \epsilon ^ { 2 } ) } \end{array}
$$

When there exist k that $u _ { k } ^ { T } X _ { : i } \ne 0$ and there exist l that $u _ { k } ^ { \top } X _ { : l } \ne 0 , u _ { j } ^ { \top } X _ { : l } \ne 0$ . Thus, $( u _ { k } ^ { \top } X _ { : l } ) ( X _ { : l } ^ { \top } u _ { j } ) \neq 0$ and $\tilde { u } _ { k } ^ { \top } X _ { : i } \ne 0$

It indicates that the zero-components of $X _ { : i }$ in eigenspace of $C$ becomes non-zero components in eigenspace of $C + \epsilon \Omega _ { F }$

In summary, when perturbing matrix $C$ with $\epsilon \Omega _ { F }$ , the non-zero frequency component $\| \tilde { X } _ { : i } ^ { ( C + \epsilon \Omega _ { F } ) } \| _ { 0 } > \| \tilde { X } _ { : i } ^ { ( C ) } \| _ { 0 }$ .

Theorem 5.4. For a graph $G ,$ , the learnable matrix $\Omega ( A , X )$ is commutative with $\operatorname { A u t } ( G )$ and preserves edge connectivity.

Proof. (1) $\Omega ( A , X )$ commutes with $A u t ( G )$

For any permutation matrix $P \in A u t ( G )$ , we have $P A P = A , P ^ { - 1 } = P ^ { \top }$ and $P D P ^ { \top } = D$ Therefore:

$$
\begin{array} { l } { P ( D + B ) P ^ { \top } = P D P ^ { \top } + P B P ^ { \top } = D + B } \\ { P ( D + B ) ^ { - 1 / 2 } P ^ { \top } = ( D + B ) ^ { - 1 / 2 } } \end{array}
$$

For two isomorphic nodes $u \sim v ,$ , they will have same node labels. Each element in B is updated by gradient, when $u \sim v ,$ the gradient of $b _ { u }$ and $b _ { v }$ are the same. As we initial all $\begin{array} { r } { b _ { u } = \frac { 1 } { n } } \end{array}$ , we will get $b _ { u } = b _ { v }$ . Thus, $P B P ^ { \top } = B$

$$
\begin{array} { r l } { \mathrm { E e r } \ : \Omega _ { D } ( A ) = ( D + B ) ^ { - 1 / 2 } ( A + B ) ( D + B ) ^ { - 1 / 2 } } \\ { \quad } & { \mathrm { F i n p } ( A ) \ : P ^ { \top } } \\ { \quad } & { = P ( D + B ) ^ { - 1 / 2 } ( A + B ) ( D + B ) ^ { - 1 / 2 } P ^ { \top } } \\ { \quad } & { = P ( D + B ) ^ { - 1 / 2 } ( A ( D + B ) ^ { - 1 / 2 } P ^ { \top } } \\ { \quad } & { = P ( D + B ) ^ { - 1 / 2 } A ( D + B ) ^ { - 1 / 2 } P ^ { \top } } \\ { \quad } & { \quad + P ( D + B ) ^ { - 1 / 2 } B ( D + B ) ^ { - 1 / 2 } P ^ { \top } } \\ { \quad } & { = ( D + B ) ^ { - 1 / 2 } P A P ^ { \top } ( D + B ) ^ { - 1 / 2 } } \\ { \quad } & { \quad + ( D + B ) ^ { - 1 / 2 } P B P ^ { \top } ( D + B ) ^ { - 1 / 2 } } \\ { \quad } & { = ( D + B ) ^ { - 1 / 2 } A ( D + B ) ^ { - 1 / 2 } } \\ { \quad } & { \quad + ( D + B ) ^ { - 1 / 2 } B ( D + B ) ^ { - 1 / 2 } } \\ { \quad } & { = ( D + B ) ^ { - 1 / 2 } ( A + B ) ( D + B ) ^ { - 1 / 2 } } \\ { \quad } & { = ( D + B ) ^ { - 1 / 2 } ( A + B ) ( D + B ) ^ { - 1 / 2 } } \\ { \quad } & { = \Omega _ { D } ( A ) } \end{array}
$$

Obviously, for $\Omega _ { S } ( A ) = I _ { \ O }$ , we have $P I P ^ { \top } = I , \mathrm { i . e . , } P \Omega _ { S } ( A ) P ^ { \top } = \Omega _ { S } ( A )$

For $\begin{array} { r } { \Omega _ { F } ( X ) = \sum _ { i = 1 } ^ { h } \frac { X _ { : i } X _ { : i } ^ { \top } } { \| X _ { : i } \| _ { F } ^ { 2 } } \circ A } \end{array}$ , we have

$$
\begin{array} { r l } & { P \Omega _ { F } ( X ) P ^ { \top } } \\ & { = P \left( \frac { X _ { : i } X _ { : i } ^ { \top } } { \| X _ { : i } \| _ { F } ^ { 2 } } \circ A \right) P ^ { \top } } \\ & { = \frac { \left( P X _ { : i } \right) \left( P X _ { : i } \right) ^ { \top } } { \| X _ { : i } \| _ { F } ^ { 2 } } \circ A } \\ & { = \frac { X _ { : i } X _ { : i } ^ { \top } } { \| X _ { : i } \| _ { F } ^ { 2 } } \circ A } \\ & { = \frac { \sum _ { f } } { \| X _ { : i } \| _ { F } ^ { 2 } } \circ A } \\ & { = \Omega _ { F } ( X ) } \end{array}
$$

As each term in $\Omega ( A , X )$ commutes with $A u t ( G )$ , putting them together, we have

$$
P \Omega ( A , X ) P ^ { \top } = \Omega ( A , X )
$$

(2) $\Omega ( A , X )$ preserves edge connectivity.

For $\Omega _ { D } ( A ) = ( D + B ) ^ { - 1 / 2 } ( A + B ) ( D + B ) ^ { - 1 / 2 }$ , B is a diagonal matrix and A represents the edge connectivity, $( D + B ) ^ { - 1 / 2 } ( A + B ) ( D + B ) ^ { - 1 / 2 }$ ensures that all original edges are scaled but not removed.

For $\Omega _ { S } ( D ) = I _ { \ O }$ , it adds self-loops but does not affect the existing edges.

For $\begin{array} { r } { \Omega _ { F } ( X ) = \sum _ { i = 1 } ^ { h } \frac { X _ { : i } X _ { : i } ^ { \top } } { \| X _ { : i } \| _ { F } ^ { 2 } } \circ A } \end{array}$ , the Hadamard product ◦A ensures that only weights of existing edges are modified (no new edges are added), the edge connectivity is preserved.

In summary, $\Omega ( A , X )$ commutes with $A u t ( G )$ and preserves edge connectivity.

Proposition 5.5. When $f _ { W }$ is permutation equivariant, spectral GNNs $\Psi ^ { + } ( A , X )$ augmented with AdaSpec is permutation equivariant.

Proof. The spectrum GNNs in Equation (2) has the format $\Psi ^ { + } ( A , X ) = g _ { \Theta } ( \Omega ( A , X ) ) f _ { W } ( X )$ . We denote $M = { \bf \bar { \Omega } }$ ) to simplify the analysis.

It has been proved in Theorem 5.4 that $M = \Omega ( A , X )$ is commutative with $A u t ( G )$ and preserves edge connectivity.

(1) Permuted Graph.

Let $\pi \in \operatorname { S y m } ( \mathcal { V } )$ be a permutation of the nodes. Applying π to G results in a permuted graph $\pi ( G )$ , where both the adjacency matrix M and the feature matrix X are permuted:

$$
\begin{array} { c } { { \pi ( M ) = P _ { \pi } M P _ { \pi } ^ { \top } } } \\ { { \pi ( X ) = P _ { \pi } X } } \end{array}
$$

where $P _ { \pi }$ is the permutation matrix corresponding to π.

(2) Applying $\Psi ^ { + }$ to the Permuted Graph π(G).

$$
\begin{array} { l } { \displaystyle \Psi ^ { + } ( \pi ( G ) ) = g _ { \Theta } ( \pi ( M ) ) f _ { W } ( \pi ( X ) ) } \\ { \displaystyle = \left( \sum _ { k = 0 } ^ { K } \theta _ { k } T _ { k } ( \pi ( M ) ) \right) f _ { W } ( P _ { \pi } X ) } \end{array}
$$

(3) Term $T _ { k } ( \pi ( M ) )$

Since $T _ { k }$ is a polynomial basis and $M = \Omega ( A , X )$ commutes with $P _ { \sigma }$ for all $\sigma \in \operatorname { A u t } ( G )$ , we have:

$$
T _ { k } ( \pi ( M ) ) = P _ { \pi } T _ { k } ( M ) P _ { \pi } ^ { \top }
$$

Therefore:

$$
g _ { \Theta } ( \pi ( M ) ) = \sum _ { k = 0 } ^ { K } \theta _ { k } T _ { k } ( \pi ( M ) ) = \sum _ { k = 0 } ^ { K } \theta _ { k } P _ { \pi } T _ { k } ( M ) P _ { \pi } ^ { \top } = P _ { \pi } g _ { \Theta } ( M ) P _ { \pi } ^ { \top }
$$

(4) Term $f _ { W } ( \pi ( X ) )$ ).

As fW is permutation equivariant, we have

$$
f _ { W } ( \pi ( X ) ) = P _ { \pi } f _ { W } ( X )
$$

Therefore,

$$
\Psi ^ { + } ( \pi ( G ) ) = P _ { \pi } g _ { \Theta } ( M ) P _ { \pi } ^ { \top } \cdot P _ { \pi } f _ { W } ( X ) = P _ { \pi } g _ { \Theta } ( M ) f _ { W } ( X ) = P _ { \pi } \Psi ^ { + } ( G )
$$

Thus, a spectral GNN $\Psi ^ { + } ( A , X )$ is permutation equivariant.

![](images/27039b425ca96aeeac153464638cbe1cd69504fc58fa4955785997fa6c3eef32.jpg)

![](images/4d3d4ce5ba06a1c0359c39b9b2e6f0da4f0b2782dbb8db737528f50902085e4e.jpg)  
(a)  
(b)

![](images/d88d4d09a0405cd929d092e17ebcae324de3c641e2052f4cb50eb6013c5cee1f.jpg)  
(c)

![](images/9ff78ec000112ff3df072fde8bf7a8a37f414b898fbba5c149623bce82b6f6f8.jpg)

![](images/827ee8c3cd64f8c97f7128421ea1851d41d66b38c8e095fdb7529952e8b0c98f.jpg)  
(e)

(d)  
![](images/33c6ca8063437eb19169e7725717708e08c349f73b03f51911ab7e74ac5a37ad.jpg)  
(f)

![](images/37273ea8639d634099f73a3654a7ea03ead3a3a9f0c3a59d8a0b9f34c569ed21.jpg)  
(g)

![](images/95cef3697426b07386685eb9442669cfbbaab2beb604f67a1f58163e6ffd9dac.jpg)  
(h)

![](images/b77b29bbfec12a9e20d082ea5ed23850060eac6a4e3dabc65f9456a8b9a042fe.jpg)  
(i)  
Figure 3: Distributions of eigenvalues of normalized graph adjacency matrix.