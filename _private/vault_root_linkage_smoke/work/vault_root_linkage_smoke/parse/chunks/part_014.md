<!-- part 14/15 chars 78695-84504 -->

ning rate of Wweight decay of Θweight decay of Wabpropagation parameter αpropagation parameter α</td><td rowspan=1 colspan=2>AllAll</td><td rowspan=1 colspan=1>0.5,0.70.5,0.7</td></tr><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>AllAll</td><td rowspan=2 colspan=1>0.001, 0.010.01,0.050.0,0.00050.0, 0.0005-0.5,0.5−0.5,0.50.1,0.9</td></tr><tr><td rowspan=2 colspan=2>AllAllJacobiConvJacobiConvJacobiConvGPRGNN</td></tr><tr><td rowspan=1 colspan=1>0.1, 0.2, 0.9</td></tr></table>

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