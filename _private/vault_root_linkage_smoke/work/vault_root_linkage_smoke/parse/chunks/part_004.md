<!-- part 4/15 chars 14916-22753 -->

s the i-th frequency component. The number of non-zero frequency components is $\lVert \tilde { X } ^ { ( M ) } \rVert _ { 0 } = \lvert \{ \tilde { X } _ { i } \ \lvert \ \tilde { X } _ { i } \neq 0 _ { h } \}$ |. ②

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