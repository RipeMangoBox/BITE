<!-- part 5/15 chars 21953-29307 -->

_ { \sigma }$ is the permutation matrix corresponding to the automorphism $\sigma ; ( 2 ) M$ preserves edge connectivity: $M _ { i j } \neq 0 \Leftrightarrow e _ { i j } \in \mathcal { E }$ and $M _ { i j } = 0 \Leftrightarrow e _ { i j } \notin \mathcal { E }$ . Thus, we design $\Omega ( A , X )$ as

$$
\Omega ( A , X ) = \Omega _ { { D } } ( A ) + \alpha _ { 1 } \Omega _ { { S } } ( A ) + \alpha _ { 2 } \Omega _ { { F } } ( X )\tag{3}
$$

where $\Omega _ { D } ( A )$ is designed to increase the number of distinct eigenvalues, $\Omega _ { S } ( A )$ aims to reduce the multiplicity of zero eigenvalues, and $\Omega _ { F } ( X )$ is designed to decrease missing frequency components of X. The hyperparameters $\alpha _ { 1 } , \alpha _ { 2 }$ control the eigenvalue range for stable training.

## 5.1 INCREASE DISTINCT EIGENVALUES

According to Theorem 4.3, increasing the number of distinct eigenvalues of the graph matrix can raise the lower bound of number of nodes distinguished by a spectral GNN, thereby increasing its node distinguishability. To achieve this, the term ${ \bar { \Omega } } _ { D } ( A )$ in AdaSpec is designed as follows:

$$
\Omega _ { D } ( A ) = \left( D + B \right) ^ { - 1 / 2 } \left( A + B \right) \left( D + B \right) ^ { - 1 / 2 } ,
$$

where A and D are the graph adjacency matrix and the degree matrix, respectively, and $B = \mathrm { d i a g } ( b )$ is a learnable diagonal matrix with non-negative elements.

The diagonal element of B is initialized as $b _ { u } = 1 / D _ { u u }$ , ensuring nodes with the same degree start with the same bias. For isomorphic nodes $u \sim v$ , we have $b _ { u } = b _ { \imath }$ throughout training; for u $\nsim$ , training yields $b _ { u } \neq b _ { v }$ . This initialization preserves permutation equivariance of $\Psi ^ { + } ( \bar { A } , X )$ , as shown in Proposition 5.5. Adding B to A introduces node-specific flexibility, enabling $A + B$ and $D + B$ to adapt to graphs. This enhances node distinguishability by allowing structurally equivalent but feature different nodes to play distinct roles. For two non-isomorphic nodes $u ,$ v that u $\nsim v ,$ , if $s _ { u } \sim s _ { v }$ but $X ( u ) \neq X ( v )$ , introducing different biases $b _ { u } \neq b _ { v }$ breaks structure symmetry and reduces eigenvalue multiplicity. Intuitively, B modifies the self-loop strength, altering information flow from the node itself. We later provide theoretical justification that this increases the number of distinct eigenvalues.

Theorem 5.1 (Increased Distinct Eigenvalues). Given a graph G with the adjacency matrix A, and the degree matrix D, we have:

$$
d _ { \Omega _ { D } ( A ) } \geq d _ { \tilde { A } }
$$

We prove that for any A, there exist a diagonal matrix B so that $\Omega _ { D } ( A )$ has n distinct eigenvalues. This indicates that the lower bound of the number of distinguishable nodes for spectral GNNs using $\Omega _ { D }$ is greater than or equal to that for those using ${ \tilde { A } } ,$ according to Theorem 4.3.

## 5.2 SHIFTS EIGENVALUES FROM ZERO

The presence of zero eigenvalues forces spectral filters to suppress the associated frequency components, thereby hindering node distinguishability. We shift eigenvalues away from zero by using:

$$
\Omega _ { S } ( A ) = I .
$$

We choose the identity matrix because adding it to any matrix shifts the eigenvalues while preserving the eigenvectors. This ensures minimal alteration to the original matrix.

Adding term $\epsilon \Omega _ { S }$ to any matrix $C$ can reduce the number of zero eigenvalues. As all eigenvalues of C add the same scalar ϵ, distinct eigenvalues remain distinct after addition. As all eigenvectors of $C$ stays the same, so the number of non-zero frequency component of node feature stays the same.

## 5.3 INCREASE FREQUENCY COMPONENTS

We can increase the number of non-zero frequency component to the node distinguishability of spectral GNNs. Given a node feature matrix $\dot { X }$ , we design a matrix $\Omega _ { F }$ that adapts to X to increase the frequency components:

$$
\Omega _ { F } ( X ) = \sum _ { i = 1 } ^ { h } \frac { X _ { : i } X _ { : i } ^ { \top } } { \| X _ { : i } \| _ { F } ^ { 2 } } \circ A\tag{4}
$$

where ◦ denotes the Hadamard product.

By dividing by the Frobenius norm $\| X _ { : i } \| _ { F } ^ { 2 }$ , features with larger magnitudes don’t dominate the transformation. We prove in theory that for any symmetric matrix $C$ of no repeated eigenvalues, adding $\epsilon \Omega _ { F } ( X )$ can increase non-zero frequency components.

Theorem 5.2 (Non-Decreasing Frequency Components). For a real symmetric matrix $C \in \mathbb { R } ^ { n \times n }$ $o f$ no repeated eigenvalues with orthonormal basis $\{ u _ { r } \} _ { r \in [ n ] }$ . Under Condition 5.3, the following holds for index $i \in [ h ]$ :

$$
\| \tilde { X } _ { : i } ^ { ( C + \epsilon \Omega _ { F } ) } \| _ { 0 } > \| \tilde { X } _ { : i } ^ { ( C ) } \| _ { 0 }
$$

where ϵ is a non-zero constant.

Condition 5.3 (Non-zero feature projections). Let $C \in \mathbb { R } ^ { n \times n }$ be a real symmetric matrix with orthonormal eigenbasis $\{ u _ { r } \} _ { r = 1 } ^ { n }$ . There exist two column node feature vectors $X _ { : i }$ and $X _ { : l }$ with $i , l \in [ h ]$ and $i \ne l$ such that $\bar { u } _ { k } ^ { \top } \bar { X } _ { : i } \neq 0 , u _ { k } ^ { \top } X _ { : l } \neq 0$ , and $u _ { j } ^ { \top } X _ { : l } \ne 0$ for some indices $k , j \in [ n ]$ .

Condition 5.3 are naturally satisfied in most real-world graph datasets. This condition requires that node features have non-zero projections onto certain eigenvectors of the graph matrix. Natural heterogeneity in node features makes it likely that different nodes will have diverse nonzero projections onto eigenvectors, even with sparse features. Additionally, while feature correlation exists, real-world graph typically varies a lot along certain dimensions, satisfying our non-zero projection condition. Therefore, incorporating $\Omega _ { F } ( X )$ ensures that the number of non-zero frequency components of node features is increased in real-world graphs.

In summary, each component of $\Omega ( A , X )$ either increases the number of distinct eigenvalues or the number of non-zero frequency components of the node features in the eigenbasis of the graph matrix. By Theorem 4.3, this leads to a higher lower bound on the number of distinguishable nodes, thereby enhancing node distinguishability. We show properties of our design $\Omega ( A , { \bar { X } } )$ as below.

Theorem 5.4. For a graph $G ,$ the learnable matrix $\Omega ( A , X )$ is commutative with $\operatorname { A u t } ( G )$ and preserves edge connectivity.

As $\Omega ( A , X )$ satisfies desirable properties, it ensures that the augmented spectral GNNs $\Psi ^ { + } ( A , X )$ with AdaSpec remains permutation equivariant.

Proposition 5.5. When $f _ { W }$ is permutation equivariant, spectral GNNs $\Psi ^ { + } ( A , X )$ augmented with AdaSpec is permutation equivariant.

Theorem 5.4 and Proposition 5.5 ensures that for spectral GNNs $\Psi ^ { + } ( A , X )$ , reordering the graph nodes results in a corresponding reordering of node embeddings. AdaSpec can be combined with any spectral GNNs to enhance their node distinguishability.