# ADASPEC: ADAPTIVE SPECTRUM FOR ENHANCED NODE DISTINGUISHABILITY

Fangbing Liu & Qing Wang The Australian National University fangbing.liu,qing.wang@anu.edu.edu

## ABSTRACT

Spectral Graph Neural Networks (GNNs) achieve strong performance in node classification, yet their node distinguishability remains poorly understood. We analyze how graph matrices and node features jointly influence node distinguishability. Further, we derive a theoretical lower bound on the number of distinguishable nodes, which is governed by two key factors: distinct eigenvalues in the graph matrix and nonzero frequency components of node features in the eigenbasis. Based on these insights, we propose AdaSpec, an adaptive graph matrix generation module that enhances node distinguishability of spectral GNNs without increasing the order of computational complexity. We prove that AdaSpec preserves permutation equivariance, ensuring that reordering the graph nodes results in a corresponding reordering of the node embeddings. Experiments across eighteen benchmark datasets validate AdaSpec’s effectiveness in improving node distinguishability of spectral GNNs. Code: https://github.com/Mia-321/AdaSpec

## 1 INTRODUCTION

Graph Neural Networks (GNNs) have become increasingly popular for graph learning tasks due to their strong performance in tasks such as graph and node classification (Kipf & Welling, 2017; Xu et al., 2019; He et al., 2021; Wang & Zhang, 2022; Qin et al., 2025). Among the various GNN models, spectral GNNs represent a prominent class that transforms graph signals into the spectral domain, enabling graph filters to process information for downstream tasks. Although numerous spectral GNNs have been proposed, their node distinguishability remains insufficiently understood. Node distinguishability refers to the capacity of a GNN to map topologically or feature-different nodes to different embeddings. These models typically utilize different graph matrices, such as the normalized adjacency or Laplacian matrix. Further, the distribution of node features across the graph plays a crucial role in model performance (He et al., 2022b; Platonov et al., 2023). To the best of our knowledge, no existing work has systematically analyzed the interaction between the graph matrix and node features in determining node distinguishability in spectral GNNs.

Spectral GNNs with state-of-the-art performance generally follow the form:

$$
\Psi ( M , X ) = g _ { \Theta } ( M ) f _ { W } ( X ) ,\tag{1}
$$

where $M \in \mathbb { R } ^ { n \times n }$ represents the graph matrix (such as the Laplacian or adjacency matrix), $X \in$ $\mathbb { R } ^ { n \times h }$ denotes the node feature matrix, $\begin{array} { r } { g _ { \Theta } ( M ) = \sum _ { k = 0 } ^ { K } \theta _ { k } T _ { k } ( M ) } \end{array}$ is the graph convolution function parameterized by $\Theta = \{ \theta _ { k } \} _ { k = 0 } ^ { K } .$ , and $T _ { k } ( \cdot )$ denotes the k-th polynomial basis. The term $f _ { W } ( X )$ represents the feature transformation function parameterized by W . Spectral GNNs learn meaningful node features by optimizing W , projecting them into the spectral domain. By adjusting Θ, spectral GNNs filter out unnecessary information and enhance useful information for downstream tasks.

While this formulation illustrates how spectral GNNs process node features through graph convolution, their capacity for node distinguishability remains inadequately understood. This leads to a fundamental question: how does the interaction between the graph matrix M and the node features X projected into the spectral domain affect the node distinguishability of spectral GNNs? In this work, we demonstrate that node distinguishability is influenced by the eigenvalue multiplicity and the missing frequency components of node features in the eigenbasis of the graph matrix. Further, we derive a theoretical lower bound on the number of nodes that can be distinguished by spectral GNNs, given a specific graph matrix and node features.

Motivated by our theoretical analysis of node distinguishability, we introduce AdaSpec, an adaptive graph matrix generation module that optimizes the graph matrix to maximize its lower bound on node distinguishability. Designed as a plug-in, AdaSpec can be seamlessly integrated into any spectral GNN to enhance node distinguishability. Moreover, spectral GNNs augmented with AdaSpec preserve permutation equivariance, ensuring that reordering graph nodes results in a corresponding reordering of node embeddings. Finally, AdaSpec maintains the graph’s connectivity, guaranteeing that the learned embeddings accurately reflect the underlying graph structure.

We evaluate our approach on eighteen benchmark node classification datasets, covering a range of small- and large-scale graphs with both homophilic and heterophilic structures in Section 6. Spectral GNNs with AdaSpec achieve notable performance improvements on heterophilic graphs, while maintaining or slightly improving accuracy on homophilic ones. These results validate the effectiveness of AdaSpec in boosting node distinguishability. Additionally, experimental results show that the order of time complexity of spectral GNNs with and without AdaSpec are the same.

## 2 RELATED WORKS

Spectral GNNs. Spectral GNNs perform graph convolution by applying filters in the spectral domain for representation learning. Based on the design of their graph filters, spectral GNNs can be categorized into polynomial (He et al., 2022a; 2021) and rational types (Levie et al., 2019; Bianchi et al., 2021; Li et al., 2025). Polynomial graph filters are computationally efficient and localized in the vertex domain (Hammond et al., 2009; Defferrard et al., 2016), and this paper focuses on their analysis. Recent studies primarily investigate how different polynomial bases affect spectral GNN performance, for instance, ChebNet, ChebNetII, JacobiConv, BernNet, GPRGNN and GLN (Defferrard et al., 2016; He et al., 2022a; Wang & Zhang, 2022; He et al., 2021; Chien et al., 2021; Li & Wang, 2024). Further, FavardGNN, UniFilter and PolyCF learn polynomial bases that adapt to different graph structures (Guo & Wei, 2023; Huang et al., 2024; Qin et al., 2025).

Above spectral GNNs use fixed graph matrices like normalized adjacency or Laplacian matrices. While research has focused on effect of polynomial bases on performance of spectral GNNs, we demonstrate the critical role of the graph matrix. We analyze how the interaction between the graph matrix and node features affects spectral GNN performance. Further, we propose AdaSpec, a graph matrix generation module to enhance the performance of spectral GNNs.

Expressive Power of Spectral GNNs. The expressive power of GNNs in graph classification has been extensively analyzed through the Weisfeiler-Lehman (WL) test (Li & Leskovec, 2022; Zhang et al., 2023; Jin et al., 2025), which are algorithms determining graph isomorphism (Weisfeiler & Leman, 1968). In contrast, the expressive power of GNNs for node classification remains less explored. The expressive capacity of linear spectral GNNs has been analyzed via the uniform approximation theorem in (Wang & Zhang, 2022), which shows that when the graph matrix has no repeated eigenvalues and node features span all frequency components, the model can approximate any one-dimensional function. However, these conditions rarely hold in real-world graphs, where symmetric structures are common and node features are often sparse. An eigenvalue correction method was proposed in (Lu et al., 2024) to enhance the expressiveness of spectral GNNs. This method reassigns eigenvalues purely by their sorted index, it does not preserve eigenspaces under node permutations, thereby breaking permutation equivariance, which is theoretically unsound.

Our work investigates the expressive power of spectral GNNs from the perspective of node distinguishability. We extend the understanding of how the interaction between the graph matrix and node features influences node distinguishability in spectral GNNs. Notably, our analysis goes beyond linear GNNs by incorporating nonlinear feature transformations fW . Moreover, we rigorously establish a theoretical lower bound on the number of distinguishable nodes in spectral GNNs.

Graph Rewiring. Another line of works focuses on improving the performance of GNNs through graph rewiring techniques. Early methods include DropEdge and EDGEWIRE, which randomly remove edges to alleviate over-smoothing (Rong et al., 2020; Chan & Akoglu, 2016). Curvaturebased approaches (Topping et al., 2022) adjust connectivity using discrete Ricci curvature to combat over-squashing, while locality-aware strategies preserve structures efficiency (Barbero et al., 2024). Recent methods include DiffWire, a differentiable and parameter-free approach guided by the Lovász bound (Arnaiz-Rodrıéguez et al., 2022); FoSR, improving spectral expansion (Karhadkar et al., 2023); and GPER, selecting edges based on resistance to enhance information flow (Shen et al., 2024).

Objectives and underlying mechanisms of graph rewiring methods differ fundamentally from ours. Graph rewiring addresses structural issues by modifying graph topology in the spatial domain, our method enhances node distinguishability in the spectral domain. Our AdaSpec is not a competitor to graph rewiring. It is a plug-and-play spectral enhancement and can be seamlessly integrated with existing graph rewiring methods to achieve superior performance.

## 3 PRELIMINARIES

Let $G = ( \nu , \mathcal { E } , X )$ denote an undirected, simple graph, where V is the set of nodes with cardinality $| \nu | = n , \mathcal { E }$ is the set of edges, and $X \in \mathbb { R } ^ { n \times h }$ is the node feature matrix. For each node $v \in \mathcal V$ $\ b { \bar { X ( v ) } } \in \mathbb { R } ^ { h }$ denotes its associated feature vector. The graph structure is represented by the adjacency matrix $A \ \in \ \{ 0 , 1 \} ^ { n \times n }$ , where $A _ { i j } = 1 \mathrm { ~ i f ~ } ( v _ { i } , v _ { j } ) \stackrel { - } { \in } \mathcal { E }$ , and 0 otherwise. The degree matrix $D \in \mathbb { R } ^ { n \times n }$ is diagonal with entries $D _ { i i }$ equal to the degree of node $v _ { i }$ . The normalized adjacency matrix is defined as $\tilde { A } = D ^ { - \frac { 1 } { 2 } } A D ^ { - \frac { 1 } { 2 } }$ . The normalized graph Laplacian is given by $\tilde { L } = I - \tilde { A }$ where $\ b { I } \in \mathbb { R } ^ { n \times n }$ is the identity matrix.

Two nodes u and v in an undirected graph G are structurally equivalent $s _ { u } \sim s _ { v }$ if they share exactly the same neighbors; formally, for every other node $w \in \mathcal { V } \setminus \{ u , v \} , ( u , w ) \in \mathcal { E } \iff$ $( v , w ) \in \mathcal { E }$ . In effect, swapping u and v leaves the graph’s adjacency relation unchanged.

A permutation of the node set V is a bijection $\pi : \mathcal { V }  \mathcal { V }$ . The set of all permutations on V forms the symmetric group $\operatorname { S y m } ( \nu )$ . An automorphism of the graph G is a permutation $\pi \in \operatorname { S y m } ( \mathcal { V } )$ satisfying the following conditions: (1) edge preservation: $( v , u ) \in \mathcal { E } \iff ( \pi ( v ) , \pi ( u ) ) \ \in$ $\mathcal { E } , \quad \dot { \forall } v , \bar { u } \in \mathcal { V }$ , and (2) feature preservation: $\mathbf { \bar { \boldsymbol { X } } } ( \pi ( v ) ) = \mathbf { \boldsymbol { X } } ( v )$ ∀v $\in \mathcal { V }$ . The automorphism group of $G ,$ denoted $\operatorname { A u t } ( G )$ , is the set of all such automorphisms.

Two nodes u and v are said to be isomorphic, denoted $u \sim v ,$ , if they belong to the same orbit under $\operatorname { A u t } ( G )$ ; that is, there exists a permutation $\pi \in \operatorname { A u t } ( G )$ such that $\pi ( v ) = u$ . Otherwise, u and v are non-isomorphic.

An important property of functions defined on graphs is permutation equivariance, which ensures that the output remains consistent under any reordering of the nodes. Formally,

Definition 3.1 (Permutation Equivariance). Let $\mathcal { G }$ denote the set of graphs. A function $f : \mathcal { G }  \mathbb { R } ^ { n \times d }$ is said to be permutation equivariant if, for any graph $G \in { \mathcal { G } }$ and any permutation $\pi \in \operatorname { S y m } ( \mathcal { V } )$ , it holds that

$$
f ( \pi ( G ) ) = \pi ( f ( G ) ) ,
$$

where $\pi ( G )$ denotes the graph obtained by permuting the nodes of G according to π, and $\pi ( f ( G ) )$ denotes the corresponding permutation of the output of $f .$

## 4 NODE DISTINGUISHABILITY OF SPECTRAL GNNS

The node distinguishability of a spectral GNN refers to its ability to distinguish non-isomorphic nodes within graphs. Formally,

Definition 4.1 (Node Distinguishability). For a spectral GNN with function class ${ \mathcal { F } } ,$ , where each $f \in \mathcal { F } : \mathcal { G } \to \mathbb { R } ^ { n \times d }$ maps a graph to node representations, node distinguishability refers to the ability to learn a function that assigns distinct representations to non-isomorphic nodes:

$$
f ( G ) _ { v } \neq f ( G ) _ { u } \quad { \mathrm { f o r ~ a l l ~ } } v , u \in \mathcal { V } { \mathrm { ~ w h e r e ~ } } v \not \sim u
$$

where $f ( G )$ v and $f ( G ) _ { u }$ denote representations of node v and u. v $\nsim$ u indicates node $u , v$ are non-isomorphic.

The spectral GNN’s node distinguishability capacity that mapping non-isomorphic nodes to distinct representations is determined by its function class $\mathcal { F }$ . To understand the distinguishability of spectral GNNs in the form of Equation (1) with input of graph matrix M and feature matrix $X .$ , we begin by formally defining the spectrum of M and the frequency components of X.

Definition 4.2 (Spectrum and Frequency Components). Let $M = U \Lambda U ^ { \top }$ be the eigendecomposition of a graph matrix $M \in \mathbb { R } ^ { n \times n }$ , where Λ is a diagonal matrix of eigenvalues and ${ \bar { U } } = [ u _ { 1 } , \dotsc , u _ { n } ]$ contains the corresponding eigenvectors. The spectrum of M, denoted spec $( M )$ , is the multiset of eigenvalues: spec $( M ) \stackrel { = } { = } \{ \bar { \{ }  \lambda _ { 1 } , \lambda _ { 2 } , . . . , \lambda _ { n } \} \}$ , where $\lambda _ { i } = \Lambda _ { i i }$ . Let support $\mathrm { s u p p } ( \mathrm { s p e c } ( M ) )$ be the underlying set of spec(M). Define $d _ { M } = | \operatorname { s u p p } ( \operatorname { s p e c } ( M ) ) |$ , which is the number of distinct eigenvalues. Given node features $\boldsymbol { X } \in \mathbb { R } ^ { n \times h }$ , the frequency components in the eigenbasis of M are ${ \tilde { X } } = U ^ { \top } X$ , where $\tilde { X } _ { i } = u _ { i } ^ { \top } .$ X is the i-th frequency component. The number of non-zero frequency components is $\lVert \tilde { X } ^ { ( M ) } \rVert _ { 0 } = \lvert \{ \tilde { X } _ { i } \ \lvert \ \tilde { X } _ { i } \neq 0 _ { h } \}$ |. ②

![](images/82a657c2ab6e82c100d0fd302a7efdc2adccbf4deabef76c98f2d11189de1047.jpg)  
(a)

![](images/d5432892de3fd52f5a10f6756811a84b720df67856cc100db1f7da9cbfe7fd71.jpg)  
(b)

![](images/9db69f65f2b7099768483fff629350ba0c658b34afd1a5018357b388cba456d1.jpg)  
(c)

![](images/92005ff8750efaaa9abd09736142ecda741c49119336cfa5a2b09f683eff80a7.jpg)  
(d)  
Figure 2: Eigenvalues and frequency component distributions.

![](images/0064dc4120ce66ec3dc396d213f510643d3bcfee36b4fd3121ab6160db4001b0.jpg)

![](images/919d283cccf856d16bcac5e635335005ac14e41cb935ef377f22ef5fd1bc4f7a.jpg)  
(a)

The limitations of node distinguishability in spectral GNNs stem from two key factors: Eigenvalue multiplicity of the graph matrix M and the missing of frequency components of node features X when projected onto the eigenbasis of M. In Figure 1, we show that spectral GNNs with a first-order polynomial filter and normalized adjacency matrix $\tilde { A }$ as graph matrix cannot distinguish node 1 and 6. (1) Non-distinguishable nodes can exist when there are missing frequency components that $d _ { \tilde { A } } = 6 = n$ but $\| X ^ { ( \tilde { A } ) } \| _ { 0 } = 5 < n$ in Figure 1(a). (2) Non-distinguishable nodes can exist when there are repeated eigenvalues $d _ { \tilde { A } } = 3 < n$ even if $\| X ^ { ( \tilde { A } ) } \| _ { 0 } = 6 = n$ in Figure 1(b). Nodes 1 and 6 in both subfigures are non-isomorphic but spectral GNNs yield identical embeddings for them. Hence they are indistinguishable. We provide a theoretical bound on the number of nodes that can be distinguished by spectral GNNs, stated as follo

(b)

Figure 1: Nodes 1 and 6 cannot be distinguished by spectral GNNs of $K = 1$ with A˜ when graph signal $X = [ 1 , 0 , 0 , 0 , 0 , 1 ]$ . (a) Missing frequency components: $d _ { \tilde { A } } \ = \ 6 , \ \lVert X ^ { ( \tilde { A } ) } \rVert _ { 0 } \ = \ 5 .$ (b) Eigenvalue multiplicity: , $d _ { \tilde { A } } =$ $3 , \| X ^ { ( \tilde { A } ) } \| _ { 0 } = 5$

Theorem 4.3. For $X \neq 0 _ { n \times n } ,$ there exist a spectral GNN $\Psi ( M , X )$ that can distinguish at least min $( d _ { M } , \Vert \tilde { X } ^ { ( M ) } \Vert _ { 0 } )$ nodes on graph.

This result provides a fundamental guarantee on the node distinguishability of spectral GNNs. The lower bound depends on both the number of distinct eigenvalues $d _ { M }$ and the number of non-zero frequency components $\| { \tilde { X } } ^ { ( M ) } \| _ { 0 } ,$ which together characterize the alignment between the graph matrix M and the node features X. When multiple eigenvectors share the same eigenvalue, the graph filter $g _ { \Theta }$ applies identical transformations to them, preventing from distinguishing different structural patterns. Similarly, if node features lack frequency components corresponding to certain eigenvectors, structural differences captured by those eigenvectors become invisible in embeddings. This has practical implications: increasing distinct eigenvlaue number $d _ { M }$ and non-zero frequency components of X in the eigenbasis of $M$ improves the theoretical guarantee on the lower bound of number of distinguishable nodes, offering a clear direction for enhancing the expressive power of spectral GNNs.

In real-world graphs, we observe that eigenvalue multiplicity and missing frequency component are very common.

Observation I (Eigenvalues of Multiplicity.) The normalized graph adjacency matrix $\tilde { A } \ =$ $D ^ { - 1 / 2 } A D ^ { - 1 / 2 }$ often contains eigenvalues with multiplicities greater than one and the eigenvalue zero has largest multiplicity.

We illustrate the eigenvalue distribution of the normalized graph adjacency matrix for the Texas and Cora datasets in Figure 2(a-b). Additional eigenvalue distributions for various other real-world datasets are provided in Figure 3 (Appendix). This phenomenon is also observed in (Lim et al., 2023). Graph symmetry, repeated substructures often lead to repeated eigenvalues in the normalized adjacency matrix and reduce its rank. Real-world graphs also tend to be sparse due to many lowdegree nodes, further lowering the rank. Since the rank of a real symmetric matrix equals the number of non-zero eigenvalues, low-rank matrices imply high multiplicity of the zero eigenvalue.

Node features in connected real-world graphs are sampled independently of the graph structure. For instance, in citation networks (such as Cora and PubMed), node features are the textual content of papers, which are collected independently of the graph structure. Thus, graph signals are not aligned with the graph’s eigenvectors. We have below observations.

Observation II (Missing Frequency Components.) Many frequency components of graph signal (node feature) is zero in the eigenbasis of normalized graph adjacency matrix $\tilde { A }$

We illustrate the distribution of frequency components for Texas and Cora in Figure 2(c-d), where most components are zero. Additional results for other real-world datasets are provided in Figure 4 (Appendix). Zero frequency component means that the frequency component in the direction of corresponding eigenvectors is missing. Real-world node features are often either smooth or oscillatory, containing only low or high-frequency components, leading to many others to be zero or negligible. Additionally, features are typically sparse, with only k non-zero entries that √ $k \ll n$ . When projected onto the eigenbasis, each component scales as $O ( \bar { k } / \sqrt { n } )$ . As $n \to \infty$ , the proportion of non-zero frequency components tends toward zero.

Based on above observations and Theorem 4.3, we propose AdaSpec to enhance the node distinguishability of spectral GNNs.

## 5 ADASPEC

AdaSpec generates a graph matrix that adapts to both the graph structure and node features, enabling it to serve as a plug-in module for any spectral GNN $\bar { \Psi ( M , X ) }$ of the form in Equation (1). The spectral GNN augmented with AdaSpec is defined as:

$$
\Psi ^ { + } ( A , X ) = g _ { \Theta } ( \Omega ( A , X ) ) f _ { W } ( X ) ,\tag{2}
$$

where Ω maps the adjacency matrix A and node features X to a new graph matrix. The functions gΘ and $f _ { W } ( X )$ remain the same as those in $\Psi ( M , X )$ .

AdaSpec enables $\Psi ^ { + } ( A , X )$ to capture richer interactions between graph structure and node features, which are not possible using fixed matrices in classic spectral GNNs $\Psi ( M , X )$ . To ensure permutation equivariance of node embeddings, the generated graph matrix $\boldsymbol { M } ^ { \setminus } = \Omega ( A , \boldsymbol { X } )$ must satisfy two key properties: (1) M commutes with $\operatorname { A u t } ( G ) \colon P _ { \sigma } { \bar { M } } = M P _ { \sigma } , \forall \sigma \in \operatorname { A u t } ( G )$ where $P _ { \sigma }$ is the permutation matrix corresponding to the automorphism $\sigma ; ( 2 ) M$ preserves edge connectivity: $M _ { i j } \neq 0 \Leftrightarrow e _ { i j } \in \mathcal { E }$ and $M _ { i j } = 0 \Leftrightarrow e _ { i j } \notin \mathcal { E }$ . Thus, we design $\Omega ( A , X )$ as

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

## 5.4 TIME COMPLEXITY ANALYSIS

The time complexity of classic spectral GNNs $\Psi ( M , X )$ and $\Psi ^ { + } ( A , X )$ augmented with AdaSpec is in the same order in both forward and backward propagation. $\Omega _ { F } ( X )$ in AdaSpec will increase the pre-computing time, but it needs to be computed only once. We list the time complexity in Table 1.

The time complexity can be analyzed in two main phases: pre-computation and forward/backward propagation. During pre-computation, graph matrix normalization requires $O ( | \mathcal { V } | + | \mathcal { E } | )$ operations such as graph adjacency matrix normalization. $\Omega _ { F } ( X ) \mathrm { i n } \Psi ^ { + } ( A , X )$ requires an additional $O ( h ( | \nu | +$ |E|)) where computation is efficiently limited to non-zero entries in the adjacency matrix. Thus, the one-off pre-computing of $\Psi ^ { + } ( A , X )$ scales linearly in the size of graph and node feature dimension.

For forward and backward propagation, the feature transformation step $f _ { W } ( X )$ incurs a complexity of $O ( | W | h )$ , while graph convolution $g _ { \Theta }$ requires $O ( K T | \mathcal { E } | )$ operations when $T _ { k } ( M )$ is computed recursively, such as in ChebNet, JacobiConv. Although $\Ddot { \Psi } ^ { + } ( A , X )$ requires additional computation of $\Omega ( A , X )$ during each forward pass and gradient calculation for matrix B during backpropagation at a cost of $O ( | \mathcal { V } | + | \mathcal { E } | )$ , this does not change the overall asymptotic complexity.

## 6 EXPERIMENTS

We design our experiments to investigate the following research questions: (1) Q1: To what extent does AdaSpec generate task-adaptive graph matrices that enhance node distinguishability in spectral GNNs? (2) Q2: What is the contribution of each component within AdaSpec to overall performance? (3) Q3: How does AdaSpec affect the spectral properties of the graph matrix, particularly in terms of increasing the number of distinct eigenvalues? (4) Q4: What is the computational overhead introduced by integrating AdaSpec into spectral GNNs during training?

Experimental Setup. We conduct experiments on eighteen benchmark datasets for node classification to verify the effectiveness of AdaSpec. Datasets includes: six small heterophilic graphs (Texas, Wisconsin, Actor, Chameleon, Squirrel, Cornell), five large heterophilic graphs (Roman\_Empire, Amazon\_Ratings, Minesweeper, Tolokers, Questions) and seven homophilic graphs (Citeseer, Pubmed, Cora, Computers, Photo, Coauthor-CS, Coauthor-Physics). Statistics of datasets, details about the baselines, and the setting of hyperparameters are included in Appendix B. For each dataset, we follow (Chien et al., 2021; He et al., 2022a) and use sparse splitting that nodes are randomly divided into training/validation/testing with ratios of $2 . 5 \% / 2 . 5 \% / 9 5 \%$ , respectively. Notably, for Citeseer, Pubmed, and Cora datasets, 20 nodes per class are for training, 500 nodes for validation, and 1,000 nodes for testing.

We chose five popular spectral GNNs as our baselines: ChebNet (Defferrard et al., 2016), GPRGNN (Chien et al., 2021), BernNet (He et al., 2021), JacobiConv (Wang & Zhang, 2022), and ChebNetII (He et al., 2022a), and compare their performances augmented with AdaSpec and with fixed graph matrix across all datasets. For each spectral GNN, we use GNN (O) to denote the original model and GNN (M) to denote the spectral GNNs augmented by AdaSpec, with $\Delta$ ↑ indicating the performance improvement.

Effectiveness of AdaSpec. We present the node classification performance with and without the AdaSpec on all small heterophilic datasets and a subset of large heterophilic datasets in Table 2. The Minesweeper and Question datasets are particularly challenging to classify, as their label informativeness (i.e., the mutual information between the labels of the central node and its neighbors) is zero (Platonov et al., 2023). The complete experimental results are in Table 9 (Appendix). Results on homophilic graphs are shown in Table 3 .
<table><tr><td></td><td></td><td></td><td>Spectral GNNs | Parameter Count Pre-computing Complexity Forward/Backward Complexity</td></tr><tr><td> $\Psi ( M , X )$ </td><td>1 + K</td><td> $O ( | \mathcal { V } | + | \mathcal { E } | )$ </td><td>O(KT|ε| + |V||W |)</td></tr><tr><td> $\Psi ^ { \dagger } ( \dot { A } , \dot { X } )$ </td><td> $1 + K + | \nu |$ </td><td> $O ( h \dot { ( } \vert \dot { \nu } \vert + \dot { \vert } \dot { \varepsilon } \vert ) )$ </td><td>O(KT ξ| + |V|W|)</td></tr></table>

Table 1: Time complexity comparison of GNNs with and without AdaSpec. V and E denotes the node and edge set respectively. h is the node feature dimension. T is the node class number. K is the polynomial order of spectral GNNs.

<table><tr><td>Model</td><td>Texas</td><td>Wisconsin</td><td>Actor</td><td>Chameleon</td><td>Squirrel</td><td>Cornell</td><td>Minesweeper</td><td>Questions</td></tr><tr><td>ChebNet(O) ChebNet(M)</td><td>38.67±9.31 51.16±8.56</td><td>32.92±7.38 33.83±9.38</td><td>25.15±0.69 25.38±0.67</td><td>29.32±4.13 29.73±3.3</td><td>24.23±3.24 23.2±3.94</td><td>31.33±7.51 33.47±7.92</td><td>86.29±0.2 86.7±0.23</td><td>55.13±0.54 55.2±1.52</td></tr><tr><td>△↑ ChebNetII(O) ChebNetII(M)</td><td>+12.49 56.24±1.39 56.76±3.12</td><td>+0.91 51.5±5.63 52.0±7.75</td><td>+0.23 29.89±0.68 30.43±1.23</td><td>+0.41 35.26±3.66 35.62±3.52</td><td>-1.03 37.19±0.66 36.88±0.69</td><td>+2.14 39.54±6.88 39.94±7.05</td><td>+0.41 78.35±0.14 79.1±0.09</td><td>+0.07 64.13±0.95 65.54±0.7</td></tr><tr><td>△↑ JacobiConv(O) JacobiConv(M)</td><td>+0.52 55.09±5.95 57.4±3.93</td><td>+0.5 49.0±10.51 52.33±8.88</td><td>+0.54 32.15±0.77 32.52±0.75</td><td>+0.36 34.29±3.82 38.16±1.18</td><td>-0.31 29.29±1.99 31.35±1.68</td><td>+0.4 38.96±8.79 41.62±10.06</td><td>+0.75 87.34±0.12 89.13±0.1</td><td>+1.41 64.72±0.38 65.8±0.18</td></tr><tr><td>△↑ GPRGNN(O) GPRGNN(M)</td><td>+2.31 48.15±4.74 58.27±4.97</td><td>+3.33 44.25±5.92 53.25±7.21</td><td>+0.37 30.39±1.24</td><td>+3.87 32.5±2.92</td><td>+2.06 27.7±3.88</td><td>+2.66 34.39±6.88</td><td>+1.79 87.15±0.49</td><td>+1.08 53.14±0.27 58.19±0.36</td></tr><tr><td>△↑ BernNet(O) BernNet(M) Δ↑</td><td>+10.12 56.19±7.52 58.9±4.11</td><td>+9.0 49.38±5.75 51.96±7.84</td><td>30.4±1.51 +0.01 30.5±1.18 30.61±0.67</td><td>32.82±4.76 +0.32 35.35±3.46 39.61±1.55</td><td>27.3±6.03±4.77 -0.4 33.41±3.42 34.46±3.52</td><td>36.13±7.52 +1.74 36.82±10.64 40.23±5.66</td><td>88.58±0.18 +1.43 76.54±0.23 76.95±0.21</td><td>+5.05 64.86±0.37 65.2±0.31</td></tr></table>

Table 2: Performance of spectral GNNs with/without AdaSpec on heterophilic datasets. ROC AUC is reported on Minesweeper, Questions. Testing accuracy is reported on other datasets. High accuracy and ROC AUC indicate good performance.

<table><tr><td>Model</td><td>Citeseer</td><td>Pubmed</td><td>Cora</td><td>Computers</td><td>Photo</td><td>Coauthor-CS</td><td>Coauthor-Physics</td></tr><tr><td>ChebNet(O)</td><td>69.21±0.87</td><td>75.29±2.34</td><td>80.45±1.09</td><td>82.64±1.76</td><td>91.77±0.32</td><td>90.95±0.34</td><td>95.03±0.11</td></tr><tr><td rowspan="3">ChebNet(M) △↑</td><td>68.52±0.86</td><td>77.38±1.45</td><td>82.26±0.84</td><td>85.14±0.89</td><td>92.34±0.41</td><td>91.54±0.22</td><td>94.93±0.09</td></tr><tr><td>-0.69</td><td>+2.09</td><td>+1.81</td><td>+2.5</td><td>+0.57</td><td>+0.59</td><td>-0.1</td></tr><tr><td>69.93±1.15</td><td>78.42±1.48</td><td>81.64±0.86</td><td>84.96±0.97</td><td>92.71±0.46</td><td>93.08±0.27</td><td>95.23±0.1</td></tr><tr><td rowspan="3">ChebNetII(O) ChebNetII(M) △↑</td><td>69.54±0.9</td><td>78.59±1.52</td><td>81.97±0.86</td><td>84.79±0.83</td><td>92.58±0.31</td><td>93.11±0.25</td><td>95.26±0.11</td></tr><tr><td>-0.39</td><td>+0.17</td><td>+0.33</td><td>-0.17</td><td>-0.13</td><td>+0.03</td><td>+0.03</td></tr><tr><td>70.8±0.7</td><td>79.43±1.45</td><td>77.15±0.96</td><td>85.39±0.95</td><td>92.79±0.38</td><td>93.33±0.23</td><td>95.32±0.15</td></tr><tr><td rowspan="3">JacobiConv(M) △↑</td><td>JacobiConv(O) 70.91±0.66</td><td>79.65±1.25</td><td>83.52±0.69</td><td>84.92±0.92</td><td>92.83±0.36</td><td>93.27±0.25</td><td>95.43±0.11</td></tr><tr><td>+0.11</td><td>+0.22</td><td>+6.37</td><td>-0.47</td><td>+0.04</td><td>-0.06</td><td>+0.11</td></tr><tr><td>70.02±0.7</td><td>79.24±1.1</td><td>82.24±0.86</td><td>84.09±0.81</td><td>92.43±0.24</td><td>92.99±0.22</td><td>95.28±0.04</td></tr><tr><td rowspan="3">GPRGNN(O) GPRGNN(M) △↑</td><td>70.4±0.41</td><td>79.6±0.97</td><td>82.19±0.79</td><td>84.28±0.86</td><td>92.53±0.38</td><td>93.33±0.29</td><td>95.32±0.15</td></tr><tr><td>+0.38</td><td>+0.36</td><td>-0.05</td><td>+0.19</td><td>+0.1</td><td>+0.34</td><td></td></tr><tr><td></td><td>78.9±1.04</td><td>81.9±0.8</td><td>85.15±1.14</td><td></td><td></td><td>+0.04</td></tr><tr><td rowspan="3">BernNet(O) BernNet(M) ∆↑</td><td>69.12±0.96</td><td></td><td></td><td></td><td>92.63±0.29</td><td>93.11±0.23</td><td>95.3±0.17</td></tr><tr><td>69.45±0.64</td><td>79.07±1.03</td><td>82.5±0.78</td><td>85.18±0.77</td><td>92.58±0.36</td><td>93.07±0.29</td><td>95.32±0.15</td></tr><tr><td>+0.33</td><td>+0.17</td><td>+0.6</td><td>+0.03</td><td>-0.05</td><td>-0.04</td><td>+0.02</td></tr></table>

Table 3: Test accuracy of spectral GNNs with/without AdaSpec on homophilic datasets. High accuracy indicates good performance.

From Tables 2 and 3, we observe the following: (1) AdaSpec significantly improves performance on heterophilic graphs compared to homophilic graphs. There is an average accuracy improvement of 1.89% on small heterophilic graphs, an average ROC AUC improvement of 1.27% on large heterophilic graphs, and an average accuracy improvement of 0.43% on homophilic graphs. (2) AdaSpec shows greater performance improvement on small-sized graphs compared to large-sized graphs. The average node classification accuracy improvement on small graphs (Texas, Wisconsin, Cornell) is 3.45%, whereas the improvement on larger graphs (Chameleon, Squirrel) is 0.46%.

The main performance improvement stems from AdaSpec’s ability to increase node distinguishability in spectral GNNs. By refining the graph structure representation, AdaSpec enables the model to better separate nodes with similar features or structures. In homophilic graphs, low-frequency components are sufficient for smooth features, so adding more may hurt. Heterophilic graphs require richer spectral patterns, and AdaSpec help by increasing useful frequency components. In small graphs, changes in graph matrix can reveal critical structure. In large graphs, existing structure dominates, changes in graph matrix are less effective.

Component-wise Analysis. We report ChebNet performance augmented with AdaSpec across multiple datasets and conduct an ablation study to isolate the effects of each component. Results in Table 4 show: (1) Full components: Combining all three components consistently yields the best performance. (2) Structure-dominated graphs (e.g., Chameleon, Cora): $\Omega _ { D }$ outperforms $\Omega _ { S }$ . (3) Feature-dominated graphs (e.g., Texas, Roman\_Empire): ΩS outperforms $\Omega _ { D }$ . (4) Frequency components: Increasing non-zero frequency components via $\Omega _ { F } ( X )$ improves performance, even when used alone. Each component within AdaSpec independently improves node distinguishability. When combined, these mechanisms complement each other, leading to the strongest overall performance.

<table><tr><td>AdaSpec</td><td>Texas</td><td>Chameleon</td><td>Roman Empire</td><td>Amazon Ratings</td><td>Citeseer</td><td>Cora</td></tr><tr><td>ChebNet(O)</td><td>38.67</td><td>29.32</td><td>47.15</td><td>39.79</td><td>69.21</td><td>80.45</td></tr><tr><td> $\Omega _ { D } ( A )$ </td><td>40.75</td><td>26.71</td><td>22.70</td><td>40.75</td><td>68.27</td><td>81.53</td></tr><tr><td> $\Omega _ { S } ( A )$ </td><td>44.51</td><td>23.27</td><td>54.04</td><td>35.28</td><td>52.29</td><td>55.63</td></tr><tr><td> $\tilde { \Omega _ { F } ( X ) }$ </td><td>26.24</td><td>28.22</td><td>54.12</td><td>37.16</td><td>29.49</td><td>65.49</td></tr><tr><td> $\Omega ( \dot { A } , \dot { X } )$ </td><td>51.16</td><td>29.73</td><td>54.55</td><td>40.92</td><td>68.52</td><td>82.26</td></tr></table>

Table 4: Test accuracy of ChebNet with different components of AdaSpec across datasets that $\Omega ( A , X )$ contains all three components.

Increased Distinct Eigenvalue Number. We compare the number of distinct eigenvalues between the original normalized adjacency matrix A˜ and the modified matrix $\Omega _ { D } ( A )$ from AdaSpec when using ChebNet. Due to the computational cost of full eigendecomposition, we conduct this analysis on small-scale homophilic and heterophilic datasets. As shown in Table $5 , \Omega _ { D } ( A )$ consistently increases the number of distinct eigenvalues, supporting Theorem 5.1. Standard normalized adjacency matrix A˜ and its self-loop version Aˆ are specific cases of the component $\Omega _ { D } ( A )$ in AdaSpec by setting $B = 0$ and $B = 1$ respectively. We introduces richer structural information in spectral GNNs by making B learnable matrix (updated via gradient descent) in AdaSpec. The increased number of distinct eigenvalues directly enhances the model’s ability to differentiate non-isomorphic nodes.

<table><tr><td>Dataset</td><td>Texas</td><td>Wisconsin</td><td>Chameleon</td><td>Squirrel</td><td>Cornell</td><td>Citeseer</td><td>Cora</td></tr><tr><td>|2</td><td>183</td><td>251</td><td>890</td><td>2,223</td><td>183</td><td>3,327</td><td>2,708</td></tr><tr><td> $d _ { \tilde { A } }$ </td><td>113</td><td>178</td><td>845</td><td>2,213</td><td>122</td><td>2,508</td><td>2,395</td></tr><tr><td> $d _ { \Omega _ { D } ( A ) }$ </td><td>181</td><td>229</td><td>888</td><td>2,221</td><td>144</td><td>3,227</td><td>2,645</td></tr><tr><td> $\triangle \uparrow$ </td><td>68</td><td>51</td><td>43</td><td>8</td><td>22</td><td>719</td><td>250</td></tr></table>

Table 5: Number of distinct eigenvalues of the graph matrix. |V| denotes the number of nodes in graphs. $d _ { \tilde { A } }$ and $d _ { \Omega _ { D } ( A ) }$ are numbers of distinct eigenvalues of A˜ and $\Omega _ { D } ( A )$ in AdaSpec respectively.

Time Complexity of AdaSpec. We evaluate the training efficiency of ChebNet with and without AdaSpec across multiple datasets. For each dataset, we conduct ten independent runs. We report the average training time per run and the pre-computing time of $\Psi ^ { + } ( A , X )$ in Table 6. The results show that AdaSpec introduces minimal overhead and can even accelerate convergence on large heterophilic graphs (e.g., Roman\_Empire, Amazon\_Ratings). When increase graph size from Amazon\_Ratings to Coauthor-Physics, the pre-computation time rises from 0.03s to 12.44s, which is consistent with our time complexity analysis in Section 5.4. By incorporating structural and feature bias into the node representation, AdaSpec enables faster convergence and more efficient training.

<table><tr><td rowspan="2">Datasets</td><td rowspan="2">Roman _Empire</td><td rowspan="2">Amazon _Ratings</td><td rowspan="2">Tolokers</td><td rowspan="2">Minesweeper</td><td rowspan="2">Questions</td><td rowspan="2">Computers</td><td rowspan="2">Photo</td><td rowspan="2">Coauthor -CS</td><td rowspan="2">Coauthor -Physics</td></tr><tr><td></td></tr><tr><td>ChebNet (O)</td><td>1.93</td><td>1.91</td><td>1.76</td><td>1.28</td><td>2.53</td><td>4.73</td><td>3.4</td><td>3.67</td><td>4.54</td></tr><tr><td>ChebNet (M)</td><td>1.88</td><td>1.35</td><td>2.51</td><td>2.18</td><td>3.05</td><td>5.32</td><td>4.83</td><td>4.11</td><td>4.60</td></tr><tr><td>∆↑</td><td>-0.05</td><td>-0.56</td><td>0.75</td><td>0.9</td><td>0.52</td><td>0.59</td><td>1.43</td><td>0.44</td><td>0.06</td></tr><tr><td>Pre-Computing</td><td>0.26</td><td>0.03</td><td>0.44</td><td>0.08</td><td>0.56</td><td>1.83</td><td>0.9</td><td>4.1</td><td>12.44</td></tr></table>

Table 6: Average training and pre-computing time (in seconds) for ChebNet with and without AdaSpec on large heterophilic and homophilic datasets. Pre-computing is for $\Omega _ { F } ( X )$ in AdaSpec.

## 7 CONCLUSION AND LIMITATIONS

This work analyzes node distinguishability of spectral GNNs and shows it is governed by the interplay between the graph matrix and node features. Specifically, by the number of distinct eigenvalues and nonzero frequency components in the graph matrix’s eigenbasis. We propose AdaSpec, a plug-in module that enhances the node distinguishability of spectral GNNs, offering theoretical guarantees and empirical gains.

While effective, our approach is limited to spectral GNNs and provides only a lower bound on distinguishability. The design of AdaSpec is tailored to certain data distributions and may not generalize universally. Future work could explore more generalizable graph matrix designs, applications to dynamic graphs, and integration with advanced spectral GNNs for broader applicability.

## REFERENCES

Adrián Arnaiz-Rodrıéguez, Ahmed Begga, Francisco Escolano, and Nuria M Oliver. Diffwire: Inductive graph rewiring via the lovász bound. In Learning on Graphs Conference, pp. 15–1. PMLR, 2022.

Federico Barbero, Ameya Velingker, Amin Saberi, Michael M Bronstein, and Francesco Di Giovanni. Locality-aware graph rewiring in gnns. In ICLR, 2024.

Filippo Maria Bianchi, Daniele Grattarola, Lorenzo Francesco Livi, and Cesare Alippi. Graph neural networks with convolutional arma filters. IEEE transactions on pattern analysis and machine intelligence, 2021.

Hau Chan and Leman Akoglu. Optimizing network robustness by edge rewiring: a general framework. Data Mining and Knowledge Discovery, 30:1395–1425, 2016.

Eli Chien, Jianhao Peng, Pan Li, and Olgica Milenkovic. Adaptive universal generalized pagerank graph neural network. arXiv: Learning, 2021.

Michaël Defferrard, Xavier Bresson, and Pierre Vandergheynst. Convolutional neural networks on graphs with fast localized spectral filtering. In NIPS, 2016.

Yu Tang Guo and Zhewei Wei. Graph neural networks with learnable and optimal polynomial bases. ArXiv, abs/2302.12432, 2023. URL https://api.semanticscholar.org/CorpusID: 257205644.

David K. Hammond, Pierre Vandergheynst, and Rémi Gribonval. Wavelets on graphs via spectral graph theory. ArXiv, abs/0912.3848, 2009.

Mingguo He, Zhewei Wei, Zengfeng Huang, and Hongteng Xu. Bernnet: Learning arbitrary graph spectral filters via bernstein approximation. In Advances in Neural Information Processing Systems (NeurIPS), 2021.

Mingguo He, Zhewei Wei, and Ji rong Wen. Convolutional neural networks on graphs with chebyshev approximation, revisited. ArXiv, abs/2202.03580, 2022a. URL https://api. semanticscholar.org/CorpusID:246652363.

Mingguo He, Zhewei Wei, and Ji rong Wen. Convolutional neural networks on graphs with chebyshev approximation, revisited. ArXiv, abs/2202.03580, 2022b. URL https://api. semanticscholar.org/CorpusID:246652363.

Keke Huang, Yu Guang Wang, Ming Li, et al. How universal polynomial bases enhance spectral graph neural networks: Heterophily, over-smoothing, and over-squashing. arXiv preprint arXiv:2405.12474, 2024.

Ming Jin, Guangsi Shi, Yuan-Fang Li, Bo Xiong, Tian Zhou, Flora D Salim, Liang Zhao, Lingfei Wu, Qingsong Wen, and Shirui Pan. Towards expressive spectral-temporal graph neural networks for time series forecasting. IEEE transactions on pattern analysis and machine intelligence, 2025.

Kedar Karhadkar, Pradeep Kr Banerjee, and Guido Montufar. Fosr: First-order spectral rewiring for addressing oversquashing in gnns. In ICLR, 2023.

Tosio Kato. Perturbation theory for linear operators, volume 132. Springer Science & Business Media, 2013.

Thomas Kipf and M. Welling. Semi-supervised classification with graph convolutional networks. In International Conference on Learning Representations, 2017.

Ron Levie, Federico Monti, Xavier Bresson, and Michael M. Bronstein. Cayleynets: Graph convolutional neural networks with complex rational spectral filters. IEEE Transactions on Signal Processing, 67:97–109, 2019.

Guoming Li, Jian Yang, and Shangsong Liang. Ergnn: Spectral graph neural network with explicitlyoptimized rational graph filters. In ICASSP 2025-2025 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), pp. 1–5. IEEE, 2025.

Pan Li and Jure Leskovec. The expressive power of graph neural networks. Graph Neural Networks: Foundations, Frontiers, and Applications, pp. 63–98, 2022.

Zhengpin Li and Jian Wang. Spectral graph neural networks with generalized laguerre approximation. In ICASSP 2024-2024 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), pp. 7760–7764. IEEE, 2024.

Derek Lim, Joshua David Robinson, Lingxiao Zhao, Tess Smidt, Suvrit Sra, Haggai Maron, and Stefanie Jegelka. Sign and basis invariant networks for spectral graph representation learning. In ICLR, 2023.

Kangkang Lu, Yanhua Yu, Hao Fei, Xuan Li, Zixuan Yang, Zirui Guo, Meiyu Liang, Mengran Yin, and Tat-Seng Chua. Improving expressive power of spectral graph neural networks with eigenvalue correction. In Proceedings of the AAAI Conference on Artificial Intelligence, volume 38, pp. 14158–14166, 2024.

Hongbin Pei, Bingzhen Wei, K. Chang, Yu Lei, and Bo Yang. Geom-gcn: Geometric graph convolutional networks. ArXiv, abs/2002.05287, 2020.

Oleg Platonov, Denis Kuznedelev, Michael Diskin, Artem Babenko, and Liudmila Prokhorenkova. A critical look at the evaluation of gnns under heterophily: Are we really making progress? arXiv preprint arXiv:2302.11640, 2023.

Yifang Qin, Wei Ju, Yiyang Gu, Ziyue Qiao, Zhiping Xiao, and Ming Zhang. Polycf: Towards optimal spectral graph filters for collaborative filtering. ACM Transactions on Information Systems, 43(4):1–28, 2025.

Yu Rong, Wenbing Huang, Tingyang Xu, and Junzhou Huang. Dropedge: Towards deep graph convolutional networks on node classification. In ICLR, 2020.

Benedek Rozemberczki, Carl Allen, and Rik Sarkar. Multi-scale attributed node embedding. J. Complex Networks, 9, 2021.

Oleksandr Shchur, Maximilian Mumme, Aleksandar Bojchevski, and Stephan Günnemann. Pitfalls of graph neural network evaluation. arXiv preprint arXiv:1811.05868, 2018.

Xu Shen, Pietro Lio, Lintao Yang, Ru Yuan, Yuyang Zhang, and Chengbin Peng. Graph rewiring and preprocessing for graph neural networks based on effective resistance. IEEE Transactions on Knowledge and Data Engineering, 2024.

GW Stewart. Matrix perturbation theory. Computer Science and Scientific Computing/Academic Press, Inc, 1990.

Jake Topping, Francesco Di Giovanni, Benjamin Paul Chamberlain, Xiaowen Dong, and Michael M Bronstein. Understanding over-squashing and bottlenecks on graphs via curvature. 2022.

Xiyuan Wang and Muhan Zhang. How powerful are spectral graph neural networks. ArXiv, abs/2205.11172, 2022.

Boris Weisfeiler and Andrei Leman. The reduction of a graph to canonical form and the algebra which appears therein. NTI, Series, 2(9):12–16, 1968.

Keyulu Xu, Weihua Hu, Jure Leskovec, and Stefanie Jegelka. How powerful are graph neural networks? In International Conference on Learning Representations, 2019.

Hanqing Zeng, Hongkuan Zhou, Ajitesh Srivastava, Rajgopal Kannan, and Viktor K. Prasanna. Graphsaint: Graph sampling based inductive learning method. ArXiv, abs/1907.04931, 2020.

Bingxu Zhang, Changjun Fan, Shixuan Liu, Kuihua Huang, Xiang Zhao, Jincai Huang, and Zhong Liu. The expressive power of graph neural networks: A survey. arXiv preprint arXiv:2308.08235, 2023.

Jiong Zhu, Yujun Yan, Lingxiao Zhao, Mark Heimann, Leman Akoglu, and Danai Koutra. Beyond homophily in graph neural networks: Current limitations and effective designs. In Advances in Neural Information Processing Systems, 2020.

## APPENDIX

## A PROOFS

Detailed proofs of theorems and propositions are provided.

Theorem ${ \bf 4 . 3 . }$ For $X \neq 0 _ { n \times n } ,$ , there exist a spectral GNN $\Psi ( M , X )$ that can distinguish at least min $( d _ { M } , \Vert \tilde { X } ^ { ( M ) } \Vert _ { 0 } )$ nodes on graph.

Proof. (1) Rank of $f _ { W }$

The rank of a matrix corresponds to the dimension of its column space. When $f _ { W }$ is MLP, which can approximate any function, there exist a parameter $W ^ { \prime }$ so that $f _ { W ^ { \prime } }$ is injective function, and rank $( \bar { f } _ { W ^ { \prime } } ( X ) ) = \mathrm { r a n k } ( X )$ .

(2) Rank of $g _ { \Theta } ( M )$

For K order polynomial function on symmetric graph matrix $g ( M )$ , we can represent it as $\begin{array} { r } { g ( M ) = \sum _ { k = 0 } \dot { \alpha _ { k } } \dot { M } ^ { k } } \end{array}$ . We conduct eigendecomposition $M = U \Lambda U ^ { T }$ , thus, $g ( M ) \stackrel { \bullet } { = } U g ( \Lambda ) U ^ { T }$ where $\begin{array} { r } { g ( \lambda _ { i } ) = \sum _ { k = 0 } ^ { K } \alpha _ { k } \lambda _ { i } ^ { k } } \end{array}$ $R a n k ( g ( M ) )$ equals the number of non-zeros in $g ( \Lambda )$ . When $\alpha _ { 0 } \neq 0$ we have $R a n k ( g ( M )$ = n as I is full rank matrix. Therefore, there exist a parameter $\Theta ^ { \prime }$ that $\theta _ { 0 } ^ { \prime } \neq 0 .$ such that rank $( g _ { \Theta ^ { \prime } } ( M ) ) = n \ge \mathrm { r a n k } ( M )$ .

(3) Rank and eigenvalues.

As $g _ { \Theta ^ { \prime } } ( M )$ is a full rank matrix, so rank $( g _ { \Theta ^ { \prime } } ( M ) ) \geq \operatorname { r a n k } ( M ) \geq d _ { M }$

As eigenvectors of M are linearly independent, if X has r non-zero frequency components, then there at least r linearly independent directions to represent X in eigenbasis of M , i.e., rank $( X ) \geq$ $\lVert \tilde { X } ^ { ( M ) } \rVert _ { 0 }$

Thus, for spectral GNN Ψ in Equation (1), there exist a parameter $\Theta ^ { \prime } , W ^ { \prime }$ that

$$
\begin{array} { r l } & { \mathrm { r a n k } ( \Psi ( M , X ) ) } \\ & { ~ = \mathrm { r a n k } ( g _ { \Theta ^ { \prime } } ( M ) f _ { W ^ { \prime } } ( X ) ) } \\ & { ~ \geq \operatorname* { m i n } ( \mathrm { r a n k } ( g _ { \Theta ^ { \prime } } ( M ) ) , \mathrm { r a n k } ( f _ { W ^ { \prime } } ( X ) ) ) } \\ & { ~ \geq \operatorname* { m i n } ( d _ { M } , \mathrm { r a n k } ( X ) ) } \\ & { ~ \geq \operatorname* { m i n } ( d _ { M } , \| \tilde { X } ^ { ( M ) } \| _ { 0 } ) } \end{array}\tag{5}
$$

If rank $( \Psi ( M , X ) ) \ge r$ , it means that at least r rows in embeddings $\Psi ( M , X )$ are linearly independent. Thus, $\Psi ( M , X )$ can distinguish r nodes in graph.

In summary, there exist a spectral GNN that can distinguish at least min $( d _ { M } , \Vert \tilde { X } ^ { ( M ) } \Vert _ { 0 } )$ on graph.

Lemma A.1 (First-Order Eigenvalue Perturbation (Kato, 2013)). Let $\Omega ( t )$ be an analytic family of real symmetric matrices, and let λ be an eigenvalue of Ω(0) with multiplicity m. Let $V _ { \lambda } \stackrel { \cdot } { \in } \mathbb { R } ^ { \dot { n } \times \dot { m } }$ have orthonormal columns spanning the eigenspace of λ. Then there exist real-analytic eigenvalue branches $\lambda _ { 1 } ( t ) , \ldots , \lambda _ { m } ( t )$ of Ω(t) with $\lambda _ { i } ( 0 ) \bar { = } \lambda ,$ , and their first-order derivatives at $t = 0$ satisfy

$$
\lambda _ { i } ^ { \prime } ( 0 ) = \mu _ { i } ,
$$

where $\mu _ { 1 } , \ldots , \mu _ { m }$ are the eigenvalues of the compressed matrix

$$
H _ { \lambda } \ = \ V _ { \lambda } ^ { \top } \ { \frac { d } { d t } } \Omega ( t ) { \bigg | } _ { t = 0 } V _ { \lambda } .
$$

In particular, the multiplicity-m eigenvalue λ splits to first order precisely when $H _ { \lambda }$ is not a scalar multiple of the identity.

Theorem 5.1 (Increased Distinct Eigenvalues). Given a graph G with the adjacency matrix A, and the degree matrix $D ,$ we have:

$$
d _ { \Omega _ { D } ( A ) } \geq d _ { \tilde { A } }
$$

Proof. When $\tilde { A }$ has an eigenvalue λ of multiplicity $k > 1$ and let $V _ { \lambda } \in \mathbb { R } ^ { n \times k }$ have orthonormal columns spanning the corresponding eigenspace $E _ { \lambda }$

Consider the analytic family

$$
\Omega ( t ) : = ( D + t B ) ^ { - 1 / 2 } ( A + t B ) ( D + t B ) ^ { - 1 / 2 } , \qquad t \in [ 0 , t _ { 0 } ] ,
$$

so $\Omega ( 0 ) = { \widetilde A }$ . The first-order perturbation matrix at $t = 0$ is

$$
P : = \left. { \frac { d } { d t } } \Omega ( t ) \right| _ { t = 0 } = - { \textstyle { \frac { 1 } { 2 } } } D ^ { - 3 / 2 } B A D ^ { - 1 / 2 } + D ^ { - 1 / 2 } B D ^ { - 1 / 2 } - { \textstyle { \frac { 1 } { 2 } } } D ^ { - 1 / 2 } A D ^ { - 3 / 2 } B .
$$

Equivalently, conjugating by $D ^ { 1 / 2 }$ yields the simpler form

$$
\begin{array} { r } { Q : = D ^ { 1 / 2 } P D ^ { 1 / 2 } = B - \frac { 1 } { 2 } \big ( D ^ { - 1 } B A + A D ^ { - 1 } B \big ) , } \end{array}
$$

from which $P = D ^ { - 1 / 2 } Q D ^ { - 1 / 2 }$

$B = d i a g ( b ) = ( b _ { 1 } , \dots , b _ { n } )$ and Q depends linearly on the diagonal vector $b ,$ hence so does $P .$

By Lemma A.1, the first-order shifts of the k eigenvalue branches emanating from λ are the eigenvalues of the $k \times k$ symmetric matrix

$$
H _ { \lambda } \ = \ V _ { \lambda } ^ { \top } P V _ { \lambda } = V _ { \lambda } ^ { \top } D ^ { - 1 / 2 } Q D ^ { - 1 / 2 } V _ { \lambda } .
$$

Since $Q$ and $H _ { \lambda }$ is linear in b, the condition that $H _ { \lambda }$ be a scalar matrix is a finite system of homogeneous linear equations in b. Thus the “bad set”

$$
S _ { \lambda } : = \{ b \in \mathbb { R } ^ { n } : H _ { \lambda } { \mathrm { ~ i s ~ s c a l a r } } \}
$$

is a proper linear subspace of $\mathbb { R } ^ { n }$ (for $k > 1$ the system is nontrivial unless the eigenspace has a special coordinate structure). Taking the finite union over all repeated eigenvalues produces a proper algebraic subset $\textstyle S = \bigcup _ { \lambda } S _ { \lambda } \subset \mathbb { R } ^ { n }$

Choose $b ^ { * } \notin S$ (and $b _ { i } ^ { * } > 0 )$ . Then for each repeated eigenvalue λ the corresponding $H _ { \lambda }$ is non-scalar, so the multiplicity of λ splits into at least two distinct eigenvalue branches for small $t > 0$ Therefore for sufficiently small $t > 0$ the matrix Ω(t) has strictly more distinct eigenvalues than A˜. Setting $B ^ { * } = t \ \mathrm { d i a g } ( b ^ { * } ) $ yields the desired diagonal perturbation.

Because we have produced a point outside the discriminant variety, the discriminant polynomial is not identically zero; hence the complement (the set of B giving simple spectrum) is Zariski-open and dense in $\mathbb { R } ^ { \bar { n } }$

In summary, there exists a diagonal $B ^ { * }$ (indeed a Zariski-open dense set of such diagonals) for which $\Omega _ { D } ( A ) = ( D + B ^ { * } ) ^ { - 1 / 2 } ( A + B ^ { * } ) ( D + B ^ { * } ) ^ { - 1 / 2 }$ has all eigenvalues simple, i.e., $d _ { \Omega _ { D } ( A ) } =$ $n \geq d _ { \tilde { A } }$

Theorem A.2 (First-order Perturbation Theorem (Stewart, 1990)). When a system described by a matrix $A \in \mathbb { R } ^ { n \times n }$ of no repeated eigenvalues is slightly altered by a small perturbation $\boldsymbol { \zeta } \in \mathbb { R } ^ { n \times n }$ and the new new system can be represented as $A ^ { \prime } = \dot { A _ { } } + \epsilon \zeta ,$ , where ϵ is a non-zero constant. A has eigenvalues $\{ \lambda _ { i } \} _ { i \in [ n ] }$ and eigenvectors $\{ u _ { i } \} _ { i \in [ n ] }$ . A′ has eigenvalues $\{ \lambda _ { i } ^ { \prime } \} _ { i \in [ n ] }$ and eigenvectors $\{ u _ { i } ^ { \prime } \} _ { i \in [ n ] }$

Relations between eigenvalues and eigenvectors of $A , A ^ { \prime }$ are:

$$
\lambda _ { i } ^ { \prime } = \lambda _ { i } + \epsilon \delta \lambda _ { i } = u _ { i } ^ { \top } \zeta u _ { i } + O ( \epsilon ^ { 2 } )
$$

$$
u _ { i } ^ { \prime } = u _ { i } + \epsilon \sum _ { j \neq i } \frac { u _ { j } ^ { \top } \zeta u _ { i } } { \lambda _ { i } - \lambda _ { j } } u _ { j } + O ( \epsilon ^ { 2 } )
$$

Theorem 5.2 (Non-Decreasing Frequency Components). For a real symmetric matrix $C \in \mathbb { R } ^ { n \times n }$ of no repeated eigenvalues with orthonormal basis $\{ u _ { r } \} _ { r \in [ n ] }$ . Under Condition 5.3, the following holds for index $i \in [ h ] .$

$$
\| \tilde { X } _ { : i } ^ { ( C + \epsilon \Omega _ { F } ) } \| _ { 0 } > \| \tilde { X } _ { : i } ^ { ( C ) } \| _ { 0 }
$$

where ϵ is a non-zero constant.

Proof. Since C is a real symmetric matrix, it can be diagonalized

$$
\boldsymbol { C } = \boldsymbol { U } \boldsymbol { \Lambda } \boldsymbol { U } ^ { T }
$$

where $U = [ u _ { 1 } , \dotsc , u _ { n } ]$ is orthonormal eigenvectors and $\boldsymbol { \Lambda } = \operatorname { d i a g } ( \lambda _ { 1 } , \ldots , \lambda _ { n } )$ is the diagonal matrix of eigenvalues.

We denote $\{ \tilde { \lambda } _ { i } \} _ { i \in [ n ] }$ and $\{ \tilde { u } _ { i } \} _ { i \in [ n ] }$ eigenvalues and eigenvectors of $C + \epsilon \Omega _ { F }$

According to Theorem $\mathbf { A . } 2 .$ , we have

$$
\tilde { u } _ { j } = u _ { j } + \epsilon \sum _ { k \neq j } \frac { u _ { k } ^ { \top } \Omega _ { F } u _ { j } } { \lambda _ { j } - \lambda _ { k } } u _ { k } + O ( \epsilon ^ { 2 } )
$$

Then,

$$
\tilde { u } _ { j } ^ { \top } X _ { : i } = u _ { j } ^ { \top } X _ { : i } + \epsilon \sum _ { k \neq j } \frac { u _ { k } ^ { \top } \Omega _ { F } u _ { j } } { \lambda _ { j } - \lambda _ { k } } u _ { k } X _ { : i } + O ( \epsilon ^ { 2 } )
$$

(1) For $\{ j | u _ { j } ^ { T } X _ { : i } \neq 0 \}$

The leading term $u _ { j } ^ { T } X _ { : i } \neq 0$ ensures that $\tilde { u } _ { j } ^ { \top } X _ { : i } \ne 0$

It indicates that non-zero components of $X _ { : i }$ in eigenspace of C is still non-zero components in eigenspace of $C + \epsilon \Omega _ { F }$

(2) For $\{ j | u _ { i } ^ { T } X _ { : i } = 0 \}$

We have

$$
\begin{array} { r l r } {  { \widetilde { u } _ { j } ^ { \top } X _ { : i } = \epsilon \sum _ { k \neq j } \frac { u _ { k } ^ { \top } \Omega _ { F } u _ { j } } { \lambda _ { j } - \lambda _ { k } } u _ { k } X _ { : i } + O ( \epsilon ^ { 2 } ) } } \\ & { } & { = \epsilon \sum _ { j \neq i } [ \sum _ { l = 1 } ^ { h } \frac { ( u _ { k } ^ { \top } X _ { : l } ) ( X _ { : l } ^ { \top } u _ { j } ) } { \| X _ { : l } \| _ { F } ^ { 2 } ( \lambda _ { j } - \lambda _ { k } ) } ] u _ { k } ^ { \top } X _ { : i } + O ( \epsilon ^ { 2 } ) } \end{array}
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

## B EXPERIMENTAL SETTINGS AND RESULTS

We introduce statistical information of datasets, details of spectral GNNs, hyperparameter setting, distribution of graph matrix spectrum and frequency components of node features of real-world datasets and more experimental results in this section.

<table><tr><td>Statistics</td><td>Texas</td><td>Wisconsin</td><td>Cornell</td><td>Actor</td><td>Chameleon</td><td>Squirrel</td></tr><tr><td>#Nodes</td><td>183</td><td>251</td><td>183</td><td>7,600</td><td>890</td><td>2,223</td></tr><tr><td>#Edges</td><td>295</td><td>466</td><td>280</td><td>26,752</td><td>27,168</td><td>131,436</td></tr><tr><td>#Features</td><td>1,703</td><td>1,703</td><td>1,703</td><td>932</td><td>2,325</td><td>2,089</td></tr><tr><td>#Classes</td><td>5</td><td>5</td><td>5</td><td>5</td><td>5</td><td>5</td></tr><tr><td># Edge Homophily</td><td>0.11</td><td>0.21</td><td>0.3</td><td>0.22</td><td>0.24</td><td>0.22</td></tr></table>

Statistics of six small heterophilic datasets (Pei et al., 2020; Rozemberczki et al., 2021; Platonov et al., 2023).
<table><tr><td>Statistics</td><td>Roman_Empire</td><td>Amazon_Ratings</td><td>Tolokers</td><td>Minesweeper</td><td>Questions</td></tr><tr><td>#Nodes</td><td>22,662</td><td>24,492</td><td>11,758</td><td>10,000</td><td>48,921</td></tr><tr><td>#Edges</td><td>32,927</td><td>93,050</td><td>519,000</td><td>39,402</td><td>153,540</td></tr><tr><td># Features</td><td>300</td><td>300</td><td>10</td><td>7</td><td>301</td></tr><tr><td># Classes</td><td>18</td><td>5</td><td>2</td><td>2</td><td>2</td></tr><tr><td># Edge Homophily</td><td>0.05</td><td>0.38</td><td>0.59</td><td>0.68</td><td>0.84</td></tr></table>

Statistics of five large heterophilic datasets Platonov et al. (2023).
<table><tr><td>Statistics</td><td>Citeseer</td><td>Pubmed</td><td>Cora</td><td>Computers</td><td>Photo</td><td>Coauthor-CS</td><td>Coauthor-Physics</td></tr><tr><td>#Nodes</td><td>3,327</td><td>19,717</td><td>2,708</td><td>13,752</td><td>7,650</td><td>18,333</td><td>134,493</td></tr><tr><td>#Edges</td><td>4,676</td><td>44,327</td><td>5,278</td><td>491,722</td><td>238,162</td><td>163,788</td><td>495,924</td></tr><tr><td>#Features</td><td>3,703</td><td>500</td><td>1,433</td><td>767</td><td>745</td><td>6,805</td><td>8,415</td></tr><tr><td>#Classes</td><td>6</td><td>5</td><td>7</td><td>10</td><td>8</td><td>15</td><td>5</td></tr><tr><td># Edge Homophily</td><td>0.74</td><td>0.8</td><td>0.81</td><td>0.78</td><td>0.83</td><td>0.81</td><td>0.93</td></tr></table>

Statistics of homophilic datasets, including three small datasets (Citeseer, Pubmed, Cora) and four large datasets (Computers, Photo, Coauthor-CS, Coauthor-Physics) (Kipf & Welling, 2017; Zeng et al., 2020; Shchur et al., 2018).  
Table 7: Statistics of real-world datasets.

## B.1 DATASETS

The statistical information of the datasets, including node numbers, edge number, feature dimensions, node class numbers, edge homophilic ratios are summarized in in Table 7.

We use the directed clean version of Chameleon and Squirrel provided by (Platonov et al., 2023) which removes repeated nodes in graphs. The large heterophilic dataset is proposed in (Platonov et al., 2023). The datasets Tolokers, Minesweeper and Questions are classified as homophilic datasets under the $H _ { e d g e }$ metric (Zhu et al., 2020), although they belong to heterophilic datasets according to the adjusted homophily metric in (Platonov et al., 2023).

## B.2 DATA DISTRIBUTION IN REAL-WORLD DATASETS

We show eigenvalues distributions of normalized graph adjacency matrix of real-world datasets in Figure 3. Distributions of frequency components of node feature column vectors in eigenspace of normalized graph adjacency matrix in Figure 4.

## B.3 HYPERPARAMETER SETTINGS

All experiments are run on a GPU NVIDIA RTX A6000 with 48G memory.

Following (Platonov et al., 2023), we fix the hidden size of the MLP to 512 and set early stopping with patience of 100 steps on five large heterophilic datasets (Roman\_Empire, Amazon\_Ratings, Tolokers, Minesweeper, Questions). Following (Chien et al., 2021; He et al., 2021), we For all other fix the hidden size of the MLP to 64 and set early stopping with patience of 200 steps on all other datatsets. The maximum number of epochs is set to 1,000.

We conduct a grid search for hyperparameters used during the training of spectral GNNs, including learning rates, dropout rates, exponential decay parameters, propagating coefficient for GPRGNN and JacobiConv, parameters a, b in JacobiConv. For different datasets, we use different grid search range, The exact search ranges for different hyperparameters on different datasets are detailed in Table 8.

![](images/250e10f1155fe98f4ae3bd6a1655a03ef27c219da4e5c99fa4777d198a045c21.jpg)

![](images/34fce409145ea6a71fbc94f87d1f0a7cc8a15f34b75d07b1275a7d191a1ac087.jpg)  
(a)

![](images/ca1a4bc0f0136e5b3b7065ad8724fb5ffc5e806b325767fef864b24fbf15ed9c.jpg)

(b)  
![](images/3f6e5bca981ec9aea2a9038710a55ab53c3b66c245bfe1805e75c5397ebc2df6.jpg)

![](images/e9d344a946e526cbcdde3b03e8e198fa0691a7a18c83db757a2a06c05a66353c.jpg)

(e)  
![](images/93a67d4f741ebdb1f40937cedda1cc5124d4b1fe657a22a3593b00ecc0454ccd.jpg)  
(f)

(c)  
![](images/0224a1b2e3bee7474ba823b8240711faeac75021201886f338d04a4aaed47564.jpg)  
(g)

![](images/58d73823547e4ffb5356379dfeba0a6eafbc2bb6a82b37cacf34f35ace9236d0.jpg)  
(h)

![](images/5fde20020b42994a7ce5ce658ef0990e293f59836154dd6e0129ee99f377a00e.jpg)  
(i)  
Figure 4: Distributions of frequency components of graph signals in eigenspace of normalized graph adjacency matrix.

<table><tr><td rowspan=1 colspan=1>Datasets</td><td rowspan=1 colspan=2>Hyperparameters</td><td rowspan=1 colspan=2>GNNs</td><td rowspan=1 colspan=1>Range</td></tr><tr><td rowspan=2 colspan=3>&#x27;Cora&#x27;,&#x27;Citeseer&#x27;, &#x27;Pubmed&#x27;,            dropout in MLP&#x27;Chameleon&#x27;,&#x27;Squirrel&#x27;,&#x27;Actor&#x27;,       dropout after MLP&#x27;Texas&#x27;,&#x27;Cornell&#x27;,&#x27;Wisconsin&#x27;          dropout in MLPdropout after MLPlearning rate of Θlearning rate of Wweight decay of Oweight decay of Wabpropagation parameter αpropagation parameter α&#x27;amazon_ratings&#x27;,&#x27;minesweeper&#x27;,       dropout in MLP&#x27;questions&#x27;,&#x27;roman_empire&#x27;,           dropout after MLP&#x27;tolokers&#x27;                              learning rate of Θlearning rate of Wweight decay of Θweight decay of Wabpropagation parameter αpropagation parameter α</td><td rowspan=1 colspan=2>All/JacobiConvAll/JacobiConvJacobiConvJacobiConvAllAllAllAllJacobiConvJacobiConvJacobiConvGPRGNN</td><td rowspan=1 colspan=1>0.5,0.7, 0.90.5,0.7, 0.90.5,0.70.5,0.70.001, 0.010.01,0.050.0, 0.00050.0,0.0005−0.5,0.5−0.5,0.50.1, 0.90.1, 0.2, 0.9</td></tr><tr><td rowspan=1 colspan=2>AllAllAllAllAllAllJacobiConvJacobiConvJacobiConvGPRGNN</td><td rowspan=1 colspan=1>0.50.5,0.70.001, 0.010.01, 0.050.0,0.00050.0,0.0005−0.5,0.5−0.5,0.50.1, 1.00.0,0.9</td></tr><tr><td rowspan=4 colspan=1>&#x27;computers&#x27;,&#x27;photo&#x27;,&#x27;coauthor-cs&#x27;,&#x27;coauthor-physics&#x27;</td><td rowspan=4 colspan=2>dropout in MLPdropout after MLPlearning rate of Θlearning rate of Wweight decay of Θweight decay of Wabpropagation parameter αpropagation parameter α</td><td rowspan=1 colspan=2>AllAll</td><td rowspan=1 colspan=1>0.5,0.70.5,0.7</td></tr><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>AllAll</td><td rowspan=2 colspan=1>0.001, 0.010.01,0.050.0,0.00050.0, 0.0005-0.5,0.5−0.5,0.50.1,0.9</td></tr><tr><td rowspan=2 colspan=2>AllAllJacobiConvJacobiConvJacobiConvGPRGNN</td></tr><tr><td rowspan=1 colspan=1>0.1, 0.2, 0.9</td></tr></table>

Table 8: Grid search ranges of hyperparameters. Dropout search ranges of JacobiConv is smaller than other spectral GNNs as it contains too many hyperparameters, we have to reduce the search range to guarantee that the searching process can be finished in accepted computing time.

## B.4 SPECTRAL GNNS

We provide the detailed description for spectral GNNs used in our experiments in the following.

For a graph with the adjacency matrix A, the degree matrix D, and the identity matrix I, we use $\hat { L } = I - \bar { D } ^ { - 1 / 2 } A D ^ { - 1 / 2 } , \tilde { \bar { L } } = - \bar { D } ^ { - 1 / 2 } A D ^ { - 1 / 2 } , \tilde { \bar { A } } = D ^ { - 1 / 2 } A D ^ { - 1 / 2 }$ , and $\tilde { A } ^ { \prime } = ( D + I ) ^ { - 1 / 2 } ( A +$ $I ) ( D + I ) ^ { - 1 / 2 }$ to denote the normalized Laplacian matrix, the shifted normalized Laplacian matrix, the normalized adjacency, matrix and the normalized adjacency matrix with self-loops, respectively.

ChebNet (Defferrard et al., 2016): This model uses the Chebyshev basis to approximate a spectral filter:

$$
\hat { Y } = \sum _ { k = 0 } ^ { K } \theta _ { k } T _ { k } ( \tilde { L } ) f _ { W } ( X )
$$

where X is the raw feature matrix, $\Theta = [ \theta _ { 0 } , \theta _ { 1 } , \dots , \theta _ { K } ]$ is the graph convolution parameter, $W$ is the feature transformation parameter and $f _ { W } ( X )$ is usually a 2-layer MLP. $T _ { k } ( \tilde { L } )$ is the k-th Chebyshev basis expanded on the shifted normalized graph Laplacian matrix $\tilde { L }$ and is recursively calculated:

$$
\begin{array} { r l } & { T _ { 0 } ( \tilde { L } ) = I } \\ & { T _ { 1 } ( \tilde { L } ) = \tilde { L } } \\ & { T _ { k } ( \tilde { L } ) = 2 \tilde { L } T _ { k - 1 } ( \tilde { L } ) - T _ { k - 2 } ( \tilde { L } ) } \end{array}
$$

ChebNetII (He et al., 2022a): The model is formulated as

$$
\hat { Y } = \frac { 2 } { K + 2 } \sum _ { k = 0 } ^ { K } \sum _ { j = 0 } ^ { K } \theta _ { j } T _ { k } ( x _ { j } ) T _ { k } ( \tilde { L } ) f _ { W } ( X ) ,
$$

where X is the input feature matrix, $W$ is the feature transformation parameter, $f _ { W } ( X )$ is usually a 2-layer $\mathrm { M L P } , T _ { k } ( \cdot )$ is the k-th Chebyshev basis expanded on $\cdot , x _ { j } = \cos \left( \left( j + 1 / 2 \right) \pi / \left( K + 1 \right) \right)$ is the j-th Chebyshev node, which is the root of the Chebyshev polynomials of the first kind with degree $K + 1$ , and $\theta _ { j }$ is a learnable parameter. Graph convolution parameter in ChebNet is reparameterized with Chebyshev nodes and learnable parameters $\theta _ { j }$

JacobiNet (Wang & Zhang, 2022): This model uses the Jacobi basis to approximate a filter as:

$$
\hat { Y } = \sum _ { k = 0 } ^ { K } \theta _ { k } P _ { k } ^ { a , b } ( \tilde { A } ) f _ { W } ( X ) ,
$$

where X is the input feature matrix, $\Theta = [ \theta _ { 0 } , \theta _ { 1 } , \dots , \theta _ { K } ]$ is the graph convolution parameter, $W$ is the feature transformation parameter and $f _ { W } ( X )$ is usually a 2-layer MLP. $P _ { k } ^ { a , b } ( \tilde { A } )$ is the Jacobi basis on normalized graph adjacency matrix $\tilde { A }$ and is recursively calculated as

$$
\begin{array} { r l } & { P _ { k } ^ { a , b } ( \tilde { A } ) = { I } } \\ & { P _ { k } ^ { a , b } ( \tilde { A } ) = \displaystyle \frac { 1 - b } { 2 } { I } + \frac { a + b + 2 } { 2 } \tilde { A } } \\ & { P _ { k } ^ { a , b } ( \tilde { A } ) = \gamma _ { k } \tilde { A } P _ { k - 1 } ^ { a , b } ( \tilde { A } ) + \gamma _ { k } ^ { \prime } P _ { k - 1 } ^ { a , b } ( \tilde { A } ) + \gamma _ { k } ^ { \prime \prime } P _ { k - 2 } ^ { a , b } ( \tilde { A } ) } \end{array}
$$

where $\begin{array} { r } { \gamma _ { k } = \frac { ( 2 k + a + b ) ( 2 k + a + b - 1 ) } { 2 k ( k + a + b ) } , \gamma _ { k } ^ { \prime } = \frac { ( 2 k + a + b - 1 ) ( a ^ { 2 } - b ^ { 2 } ) } { 2 k ( k + a + b ) ( 2 k + a + b - 2 ) } , \gamma _ { k } ^ { \prime \prime } = \frac { ( k + 1 - 1 ) ( k + b - 1 ) ( 2 k + a + b ) } { k ( k + a + b ) ( 2 k + a + b - 2 ) } } \end{array}$ . a and b are hyperparameters. Usually, grid search is used to find the optimal a and b values. GPRGNN (Chien et a1 61

GPRGNN (Chien et al., 2021): This model uses the monomial basis to approximate a filter:

$$
\hat { Y } = \sum _ { k = 0 } ^ { K } \theta _ { k } \tilde { A } ^ { \prime k } f _ { W } ( X )
$$

where X is the input feature matrix, $\Theta = [ \theta _ { 0 } , \theta _ { 1 } , \dots , \theta _ { K } ]$ is the graph convolution parameter, W is the feature transformation parameter and $f _ { W } ( X )$ is usually a 2-layer MLP. ${ \tilde { A } } ^ { \prime }$ is the normalized adjacency matrix with self-loops.

BernNet (He et al., 2021): This model uses the Bernstein basis for approximation:

$$
\hat { Y } = \sum _ { k = 0 } ^ { K } \theta _ { k } \frac { 1 } { 2 ^ { K } } \binom { K } { k } ( 2 I - \hat { L } ) ^ { K - k } \hat { L } ^ { k } f _ { W } ( X )
$$

where X is the input feature matrix, $\Theta = [ \theta _ { 0 } , \theta _ { 1 } , \dots , \theta _ { K } ]$ is the graph convolution parameter, W is the feature transformation parameter and $f _ { W } ( X )$ is usually a 2-layer MLP. Lˆ is the normalized Laplacian matrix.

## B.5 FULL EXPERIMENTAL RESULTS ON LARGE HETEROPHILIC GRAPHS

We show our full experimental results on large heterophilic graphs in Table 9. There is an average 1.08% accuracy improvement on Roman\_Empire, Amazon\_Ratings and an average 1.1% ROC AUC improvement on the rest datasets.

<table><tr><td>Model</td><td>Roman_Empire</td><td>Amazon_Ratings</td><td>Tolokers</td><td>Minesweeper</td><td>Questions</td></tr><tr><td rowspan="3">ChebNet(O) cheb (M) △↑$</td><td>47.15±0.42</td><td>39.79±0.29</td><td>70.1±0.25</td><td>86.29±0.2</td><td>55.13±0.54</td></tr><tr><td>54.55±0.3</td><td>40.92±0.27</td><td>69.2±0.61</td><td>86.7±0.23</td><td>55.2±1.52</td></tr><tr><td>+7.4</td><td>+1.13</td><td>-0.9</td><td>+0.41</td><td>+0.07</td></tr><tr><td rowspan="3">ChebNetII (O) ChebNetII (M) ∆↑</td><td>55.44±0.19</td><td>39.99±0.28</td><td>69.93±0.83</td><td>78.35±0.14</td><td>64.13±0.95</td></tr><tr><td>55.1±0.35</td><td>40.66±0.33</td><td>70.94±0.36</td><td>79.1±0.09</td><td>65.54±0.7</td></tr><tr><td>-0.34</td><td>+0.67</td><td>+1.01</td><td>+0.75</td><td>+1.41</td></tr><tr><td rowspan="3">JacobiConv (O) JacobiConv (M) △↑</td><td>55.86±0.57</td><td>40.27±0.3</td><td>70.1±0.22</td><td>87.34±0.12</td><td>64.72±0.38</td></tr><tr><td>56.21±0.38</td><td>40.17±0.24</td><td>71.04±0.22</td><td>89.13±0.1</td><td>65.8±0.18</td></tr><tr><td>+0.35</td><td>-0.1</td><td>+0.94</td><td>+1.79</td><td>+1.08</td></tr><tr><td rowspan="3">GPRGNN (O) GPRGNN (M) △↑</td><td>56.33±1.51</td><td>40.07±0.25</td><td>66.34±1.76</td><td>87.15±0.49</td><td>53.14±0.27</td></tr><tr><td>56.96±1.59</td><td>40.14±0.38</td><td>68.44±0.39</td><td>88.58±0.18</td><td>58.19±0.36</td></tr><tr><td>+0.63</td><td>+0.07</td><td>+2.1</td><td>+1.43</td><td>+5.05</td></tr><tr><td rowspan="3">BernNet (O) BernNet (M) ∆↑</td><td>55.06±0.3</td><td>39.36±0.37</td><td>68.81±0.91</td><td>76.54±0.23</td><td>64.86±0.37</td></tr><tr><td>55.51±0.91</td><td>39.85±0.23</td><td>69.49±0.72</td><td>76.95±0.21</td><td>65.2±0.31</td></tr><tr><td>+0.45</td><td>+0.49</td><td>+0.68</td><td>+0.41</td><td>+0.34</td></tr></table>

Table 9: Performance with/without AdaSpec on large heterophilic datasets (Roman\_Empire, Amazon\_Ratings, Tolokers, Minesweeper, Questions ). Test accuracy is used as the metric for Roman-Empire and Amazon-Ratings datasets and ROC AUC is reported on Minesweeper, Tolokers, Questions. High accuracy and ROC AUC indicate good performance.

<table><tr><td>Model</td><td>Texas</td><td>Wisconsin</td><td>Actor</td><td>Chameleon</td><td>Squirrel</td><td>Cornell</td><td>Citeseer</td><td>Pubmed</td><td> $\mathrm { { C o r a } }$ </td></tr><tr><td>ChebNet(O)</td><td> $3 8 . 6 7 \pm 9 . 3 1 $ </td><td> $3 2 . 9 2 { \scriptstyle \pm 7 . 3 8 }$ </td><td> $2 5 . 1 5 { \scriptstyle \pm 0 . 6 9 }$ </td><td> $2 9 . 3 2 { \scriptstyle \pm 4 . 1 3 }$ </td><td>24.23±3.24</td><td> $3 1 . 3 3 { \pm } 7 . 5 1$ </td><td>69.21±0.87</td><td> $7 5 . 2 9 { \scriptstyle \pm 2 . 3 4 }$ </td><td>80.45±1.09</td></tr><tr><td>GDC + ChebNet(O)</td><td> $5 0 . 5 8 { \scriptstyle \pm 8 . 1 3 }$ </td><td> $3 4 . 0 0 { \scriptstyle \pm 7 . 6 2 }$ </td><td> $2 4 . 9 2 { \scriptstyle \pm 0 . 7 3 }$ </td><td> $2 1 . 5 2 { \scriptstyle \pm 2 . 6 2 }$ </td><td> $2 0 . 6 2 \pm 1 . 5 7$ </td><td>28.50±7.63</td><td> $6 7 . 5 2 { \pm } 1 . 3 7$ </td><td> $7 4 . 5 3 { \pm } 1 . 9 5 $ </td><td> $7 5 . 9 1 { \scriptstyle \pm 1 . 3 6 }$ </td></tr><tr><td>GDC + ChebNet(M)</td><td> ${ \pm 2 . 1 4 \pm 8 . 2 7 }$ </td><td> $3 6 . 3 3 { \scriptstyle \pm 9 . 3 8 }$ </td><td> $2 4 . 1 5 { \scriptstyle \pm 1 . 0 2 }$ </td><td>31.84±2.68</td><td> $2 2 . 0 2 { \scriptstyle \pm 4 . 5 9 }$ </td><td> $\mathbf { 3 4 . 9 1 } \pm \mathrm { 1 0 . 8 }$ </td><td>68.26±0.98</td><td> $7 7 . 2 2 { \scriptstyle \pm 1 . 4 3 }$ </td><td> ${ \bf 8 1 . 0 1 } { \scriptstyle \pm 1 . 1 1 }$ </td></tr><tr><td>△↑</td><td>+1.56</td><td>+2.33</td><td>-0.77</td><td>+10.32</td><td>+1.40</td><td>+6.41</td><td>+0.74</td><td>+2.69</td><td>+5.10</td></tr></table>

Table 10: Impact of AdaSpec applied on top of GDC. Our method (GDC + ChebNet(M)) consistently improves performance across most benchmarks. Three configurations: (1) Standard ChebNet ( ChebNet(O) ), (2) ChebNet with GDC ( GDC+ChebNet(O) ), and (3) ChebNet with GDC + AdaSpec ( GDC+ChebNet(M) ).

## B.6 EXPERIMENTAL RESULTS OF ADASPEC WITH GRAPH DIFFUSION CONVOLUTION

Our AdaSpec is not a competitor to graph rewiring; it is a plug-and-play spectral enhancement. We demonstrate below that, it can be seamlessly integrated with existing graph rewiring methods like graph diffusion convolution (GDC) to achieve superior performance, validating its unique value proposition beyond standard rewiring.

we conducted a set of experiments combining AdaSpec with GDC and results are shown in Table 10. Our key findings are as follows. (1) Performance improvement: GDC+ChebNet(M) improves performance than GDC+ChebNet(O) In 8 out of 9 reported cases. (2) Orthogonality: If AdaSpec and GDC were solving the exact same problem (competitive mechanisms), stacking them would yield diminishing returns. The fact that AdaSpec provides significant gains on top of GDC proves they address orthogonal limitations of the graph structure. (3) Spatial rewiring optimizes topological connectivity (e.g., denoising edges to improve homophily). AdaSpec optimizes the eigenspace. Even a graph that is topologically clean (via GDC) may still suffer from eigenvalue multiplicity or missing frequency components in the spectral domain. AdaSpec resolves these spectral collisions, which GDC cannot detect or repair.