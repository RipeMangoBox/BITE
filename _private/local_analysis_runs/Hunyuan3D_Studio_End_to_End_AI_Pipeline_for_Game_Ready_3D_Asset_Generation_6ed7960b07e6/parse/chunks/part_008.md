<!-- part 8/12 chars 51202-58953 -->

i_{\text{ref}}(\mathcal{M}_{\mathcal{P}}^- | \mathcal{P}) \odot (1-\phi(\mathcal{M}_{\mathcal{P}}^-))\right|_1}
\end{aligned}
\end{equation}
Here, $\odot$ denotes element-wise multiplication and $|\cdot|_1$ is the $\ell_1$ norm. M-DPO enables targeted refinement of low-quality regions while preserving satisfactory areas.


\subsection{Experiments}


\begin{figure*}[htbp]
    \centering
    \includegraphics[width=\linewidth]{figures/poly_figures/comp_sota.pdf}
    \caption{\textbf{Generalization results on dense, out-of-distribution meshes.} Our model demonstrates superior geometric fidelity and surface continuity, maintaining high-quality reconstruction even under complex and unseen input conditions.}
    \label{fig:poly-comparison}

\end{figure*}


\begin{figure*}[htbp]
    \centering
    \includegraphics[width=0.65\linewidth]{figures/poly_figures/part.pdf}
    \caption{\textbf{Part-aware polygon generation.} With shapes segmented into several parts as input, our model can generate the corresponding meshes conditioned on partial point clouds separately without further fine-tuning. }
    \label{fig:poly-part}
\end{figure*}



\paragraph{Pre-training vs. post-training.}
In Figure \ref{fig:poly-prepost}, we show the improvement after the post-training.
In our experiments, we found that the post-training stage is crucial for improving the completeness and topology quality of the generated meshes.



\paragraph{Comparison with existing methods.}

As shown in Figure \ref{fig:poly-comparison}, we compare our model with existing polygon generation methods.
Our model can generate much more complex meshes with significantly improved topology quality and stability.







\paragraph{Part-aware polygon generation.}

With shapes segmented into several parts as input, our model can generate the corresponding meshes conditioned on partial point clouds separately without further fine-tuning as shown in Figure \ref{fig:poly-part}.
This would be much easier for the model to generate the topology for complicated meshes.


  \label{sec:polygen}

\section{Semantic UV}  \label{sec:uv}

The results of traditional UV unwrapping methods often lack semantic significance, which notably affects the quality of downstream texturing and the efficiency of resource utilization. Consequently, these traditional methods cannot be directly applied in professional pipelines, such as those used in game development and film production. To handle this challenge, we introduce SeamGPT, a novel framework that generates artist-style cutting seams through an auto-regressive approach. Our method formulates surface cutting as a sequence prediction problem, where cutting seams are represented as an ordered series of 3D line segments. Given an input mesh $\mathit{M}$, our goal is to generate seam edges $S = \{s^{i}\}_{i \in [N_s]}$. The overview of SeamGPT is shown in Fig.~\ref{fig:pipeline}. We first introduce our seam representation strategy in Sec.~\ref{sec.4.1}, which encodes cutting seams as sequential tokens. In Sec.~\ref{sec.4.2}, we detail our auto-regressive generation process, which mimics the sequential decision-making of professional artists.

\begin{figure*}[htp]
    \centering
    \includegraphics[width=\textwidth]{figures/uv_figs/pipeline.jpg}
    \caption{SeamGPT architecture:  Point cloud encoder extracts shape context; Causal transformer decoder generates axis-ordered seam coordinates.
    Color indicates the prediction order is of the seam segments (red to blue).
    }
    \label{fig:pipeline}
\end{figure*}


\subsection{Mesh Seam Representation}
\label{sec.4.1}
A seam sequence $S$ of $N_s$ segments $\{s^i\}_{i \in [N_s]}$ is defined as: $S = \{s^1, s^2, \ldots s^{N_s}\}$, where each segment $s^i$ is a 3D line segment represented by two vertices: $s^i = (p^i_h, p^i_t)$, i.e. head and tail. Each vertex $p$ is defined by its 3D coordinates: $p = (x, y, z)$.
Thus, a seam sequence can be decomposed at multiple levels:
\begin{align}
 S &= \{s^1, s^2, \ldots s^{N_s}\} && \mathrm{Segment\quad level} \nonumber\\
 &= \{p^1_h, p^1_t, p^2_h, p^2_t, \ldots, p^{N_h}_t, p^{N_h}_t\} && \mathrm{Point \quad level} \label{eq:seam_levels} \\
 &= \{x^1_h, y^1_h, z^1_h, x^1_t, y^1_t, z^1_t, \ldots, x^{N_s}_t, y^{N_s}_t, z^{N_s}_t\} && \mathrm{Coord. \quad level} \nonumber
\end{align}
\textbf{Seam ordering.}
For an auto-regressive model to function properly, a consistent order of sequences is required.
Following existing practice for mesh generation~\cite{siddiqui2023meshgpt, bpt, hao2024meshtron} and wireframe generation ~\cite{ma2024generating},
we first sort vertices $yzx$ order, where $y$ represents the vertical axis, and then sort two vertices within an edge lexicographically, placing the lowest $yzx$-ordered vertex first.
Finally, seam edges are sorted in ascending $yzx$-order based on the sorted values of their vertices.
The resulting order can be seen through the color coding of the generated meshes presented in Figure~\ref{fig:pipeline}, i.e. from red to blue.

\textbf{Quantization of coordinates.} Autoregressive models typically sample from a multinomial distribution over a discrete set of possible values. To adhere to this convention, we quantize vertex coordinates into a fixed number of discrete bins. The quantization resolution—determined by the number of bins—directly affects the precision of the predicted seam. Higher quantization levels yield more detailed and accurate representations but also increase the complexity of the generation process. To balance precision and tractability, we employ 1024-level quantization, enabling effective representation of complex seams.


\subsection{Autoregressive Seam Prediction}
\label{sec.4.2}

In autoregressive seam prediction, a seam sequence $S$ is generated by sequentially predicting each coordinate $c_i$ based on its conditional probability given all previously generated coordinates $P(c_i | c_{<i})$. The probability of the entire seam is then given by the joint probability of all its coordinates:
\begin{equation}
    P(S) = \prod_{i=1}^{6N_s} P(c_i | c_{<i}).
    \label{eq:seam_arm}
\end{equation}
\textbf{Global Shape Conditioning.}
Point clouds are a flexible and universal 3D representation that can be efficiently derived from other 3D formats, including meshes.
We use a point cloud encoder to extract representative features for characterizing the input 3D shapes.
In the context of surface cutting, seams are encouraged to align with the vertices and edges of the original mesh, such that cutting the mesh along seams does not create excessive extra faces.
To guide the decoder in producing vertex and edge-aligned seam placement, instead of sampling point clouds uniformly, we sample structural points only on vertices and along edges.
Specifically, we sample a total of 61,440 points, evenly split between: 30,720 points on vertices and 30,720 points on edges.
If the input mesh has fewer than 30,720 vertices, we use repeated over-sampling.
Points along an edge are sampled uniformly by interpolating between its start and end points with K samples, where K is determined based on the edge's length.
Finally, the input points are fed into a jointly trained point cloud encoder from~\cite{hunyuan3d22025tencent}, which processes the point cloud through a series of cross- and self-attention layers and compresses the point cloud to a latent shape embedding of length 3072 and dimension 1024.
Another option to create shape embeddings is to use mesh encoders, such as~\cite{zhou2020fullymeshae}. However, the computational cost of mesh encoder does not scale well when the input has a large number of vertices. We show in the ablation study that point cloud conditioning produces much better results than mesh conditioning.