<!-- part 5/12 chars 29210-36448 -->

on: (1) the noise-free latent of the single-view image, which is concatenated with the noised multiview latent, providing structural guidance; and (2) a semantic condition vector extracted from the input image using a pretrained SigLIP vision encoder~\citep{zhai2023siglip}. The LoRA parameters are then optimized using a standard flow-matching loss.

\textbf{Multi-view image injection.} Similar to the single image condition, we first encode all the images into image latents $\{\mathbf{c}_I^i|i={\rm org, front, left, back, right}\}$. Each non-original view is marked by a sinusoidal positional embedding with a fixed index. After positional encoding, the latents from generated views are concatenated with the original-image latent to form the final condition.


\subsection{Visualization}
\textbf{Bbox condition.} As illustrated in Figure~\ref{fig:image-generation bbox}, the bbox control signal not only succeeds in producing high-quality geometry when image-only geometric generation fails, but also generates 3D assets with appropriate proportions and well-structured forms according to the given bbox.

\begin{figure}[ht]
    \centering
    \includegraphics[width=0.95\linewidth]{figures/geo_figures/bbox_vis.png}
    \caption{3D geometry generated with bounding box control.}
    \label{fig:image-generation bbox}
\end{figure}

\textbf{Generated multi-view image condition.} Leveraging a state-of-the-art multi-view generation model as guidance, our approach produces high-fidelity 3D character assets, as exemplified in Figure~\ref{fig:image-generation character}.

\begin{figure}[ht]
    \centering
    \includegraphics[width=0.95\linewidth]{./figures/geo_figures/character_vis.png}
    \caption{3D geometry generated with generated multi-view image control.}
    \label{fig:image-generation character}
\end{figure}

\section{Part-level 3D Generation}

\begin{figure}[!ht]
    \centering
    \includegraphics[width=1\linewidth]{./figures/part/xpart/x-part-v4.jpg}
    \caption{Our part level shape generation results.}
    \label{fig:part-teaser}
\end{figure}


Generating 3D shapes at part level is pivotal for downstream applications such as mesh retopology, UV mapping, and 3D printing.
However, existing part-based generation methods often lack sufficient controllability, produce inadequate geometric quality in generated parts, and suffer from limited semantic coherence.
This section establishes a new paradigm for creating production-ready, editable, and structurally sound 3D assets. Fig.~\ref{fig:part-teaser} shows our part-level shape generation results.

As shown in Figure. ~\ref{fig:part-whole-pipeline}, given an input image, we first obtain the holistic shape using Huyuan3D 2.5~\cite{lai2025hunyuan3d}.
The holistic mesh is then fed to part detection module \textbf{P$^3$-SAM}~\cite{P3_SAM} to obtain the semantic features and part bounding boxes.
Finally, \textbf{X-Part}~\cite{X-part} decompose the holistic shape into parts.
\textbf{P$^3$-SAM} and \textbf{X-Part} will be introduced in section~\ref{sec:p3sam} and~\ref{sec:x-part}

\begin{figure}[!ht]
    \centering
    \includegraphics[width=1\linewidth]{./figures/part/whole_pipe.jpg}
    \caption{Pipeline of our image to 3D part generation. Given an input image, we first obtain the holistic shape using Huyuan3D 2.5~\cite{lai2025hunyuan3d}.
The holistic mesh is then fed to part detection module \textbf{P$^3$-SAM}~\cite{P3_SAM} to obtain the semantic features and part bounding boxes.}
    \label{fig:part-whole-pipeline}
\end{figure}

\begin{figure}[!t]
    \centering
    \includegraphics[width=1\linewidth]{./figures/part/p3sam/method.png}
    \caption{Training pipeline of \textbf{P}$^3$-SAM.}
    \label{fig:p3sam-pipeline}
\end{figure}




\subsection{ P$^3$-SAM: Native 3D Part Segmentation~\cite{P3_SAM}  }\label{sec:p3sam}

3D part segmentation is a fundamental step in our part generation pipeline.
In this section, we propose a native 3D \underline{\textbf{P}}oint-\underline{\textbf{P}}romptable \underline{\textbf{P}}art segmentation model termed \underline{\textbf{P}}$^3$-SAM, designed to fully automate the segmentation of any complex 3D objects into components with precise mask and strong robustness.
As a pioneering promptable image segmentation work, SAM provides a feasible implementation approach.
However, our method focuses on achieving precise part segmentation automatically, and we simplify the architecture of SAM.
Without adopting the complex segmentation decoder and multiple types of prompts from SAM, our model is designed to handle only one positive point prompt.

Specifically, as shown in Fig.~\ref{fig:p3sam-pipeline}, \textbf{P}$^3$-SAM contains a feature extractor, three segmentation heads, and an IoU prediction head.
We employ PointTransformerV3 as our feature extractor and integrate its features from different levels as extracted point-wise features.
The input point prompt and feature are fused and passed to the segmentation heads to predict three multi-scale masks and an IoU (Intersection of Union) predictor is utilized to evaluate the quality of the masks.

To automatically segment an object, as shown in Fig.~\ref{fig:p3sam-seg_pipe}, we apply our segmentation model using point prompts sampled by FPS (Farthest Point Sampling) and utilize NMS (Non-Maximum Suppression) to merge redundant masks.
The point-level masks are then projected onto mesh faces to obtain the part segmentation results.


Another key aspect of this method is to eliminate the influence of 2D SAM, and rely exclusively on raw 3D part supervision for training a native 3D segmentation model.
While existing 3D part segmentation datasets are either too small  or lack part annotation, this work addresses the data scarcity by developing an automated part annotation pipeline for artist-created meshes and used it to generate a dataset comprising 3.7 million meshes with high-quality part-level masks.
Our model demonstrates excellent scalability with this dataset and achieves robust, precise, and globally coherent part segmentation.

For more details of \textbf{P}$^3$-SAM, please refer to the paper~\cite{P3_SAM}.

\paragraph{Comparison with SOTA.}
We evaluate each method on three datasets: PartObj-Tiny, PartObj-Tiny-WT, and PartNetE.
PartObj-Tiny is a subset of Objarvse, containing 200 data samples across 8 categories, with manually annotated part segmentation information.
PartObj-Tiny-WT is the watertight version of PartObj-Tiny. To evaluate the performance of various networks on watertight data, we converted the meshes from PartObj-Tiny to watertight versions and successfully obtained 189 watertight meshes.
PartNetE, derived from PartNet-Mobility, contains 1,906 shapes covering 45 object categories in the form of point clouds. We also evaluate various networks on it to verify their generalization performance on point cloud.
Table \ref{tab:p3sam-main_compare} and \ref{tab:main_compare_wt}  confirming the  superior performance of \textbf{P}$^3$-SAM under diverse conditions.


\begin{figure}[!t]
    \centering
    \includegraphics[width=1\linewidth]{./figures/part/p3sam/auto_seg.png}
    \caption{Pipeline of automatic segmentation using \textbf{P}$^3$-SAM.}
    \label{fig:p3sam-seg_pipe}
\end{figure}