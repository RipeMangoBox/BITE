<!-- part 6/12 chars 36098-44068 -->

re} and \ref{tab:main_compare_wt}  confirming the  superior performance of \textbf{P}$^3$-SAM under diverse conditions.


\begin{figure}[!t]
    \centering
    \includegraphics[width=1\linewidth]{./figures/part/p3sam/auto_seg.png}
    \caption{Pipeline of automatic segmentation using \textbf{P}$^3$-SAM.}
    \label{fig:p3sam-seg_pipe}
\end{figure}


\begin{table}
\small
\centering
\setlength{\tabcolsep}{5pt}
\begin{tabular}{c|r|cccccccc|c}
\toprule
Task       & Method    & Human & Animals & Daily & Build. & Trans. & Plants & Food  & Elec.  & AVG.    \\
\midrule
          & Find3D    & 23.99 & 23.99   & 22.67 & 16.03    & 14.11  & 21.77  & 25.71 & 19.83 & 21.28    \\
Fully   & SAMPart3D & 55.03 & 57.98   & 49.17 & 40.36    & 47.38  & 62.14  & \textbf{64.59} & 51.15 & 53.47     \\
Seg. w/o  & SAMesh    & \textbf{66.03} & \textbf{60.89}   & 56.53 & 41.03    & 46.89  & 65.12  & 60.56 & 57.81 & 56.86     \\
 Connect. & PartField & 54.52 & 58.07   & 56.46 & 42.47    & 49.09  & 59.16  & 55.4  & 56.29 & 53.93    \\
          & Ours      & 60.77 & 59.43   & \textbf{62.98} & \textbf{50.82}    & \textbf{57.72}  & \textbf{70.53}  & 54.04 & \textbf{61.96} & \textbf{59.88}    \\
\midrule
Seg. w/     & PartField & 80.85 & 83.43   & 77.83 & \textbf{69.66}    & \textbf{73.85}  & 80.21  & 85.27 & \textbf{82.30}  & 79.18  \\
Connect.    & Ours      & \textbf{80.77} & \textbf{86.46}   & \textbf{80.97} & 67.77    & 68.44  & \textbf{90.30}   & \textbf{92.90}  & 81.52 & \textbf{81.14}   \\
\midrule
\multirow{2}{*}{Interact.}          & Point-SAM & 8.63  & 9.38    & 17.47 & 11.19    & 7.63   & 13.95  & 23.02 & 12.73 & 13.00    \\
                                     & Ours      & \textbf{49.01} & \textbf{53.45}   & \textbf{52.36} & \textbf{38.50}     & \textbf{51.52}  & \textbf{62.57}  & \textbf{50.80}  & \textbf{51.86} & \textbf{51.23}   \\
\bottomrule
\end{tabular}
\caption{The comparison of our method with previous methods on PartObjectarverse-Tiny. The first two blocks represent class-agnostic part segmentation without and with connectivity, respectively, and the last block represents interactive segmentation.}
\label{tab:p3sam-main_compare}
\end{table}

\begin{table}[!ht]
\small
\centering
\begin{tabular}{r|ccccc|cc}
\toprule
Task     & \multicolumn{5}{c|}{Fully Segmentation w/o Connectivity}               & \multicolumn{2}{c}{Interactive Seg.}  \\
\midrule
Method   & Find3D & SAMPart3D & SAMesh & PartField & Ours  & Point-SAM & Ours                      \\
\midrule
PartObj-Tiny-WT & wait   & wait      & wait   & wait      & \textbf{55.35} & 13.11     & \textbf{49.11}                     \\
PartNetE & 21.69   &  56.17    & 26.66   &  59.1     & \textbf{65.39} & 15.06     & \textbf{63.48}                     \\
\bottomrule
\end{tabular}
\caption{The comparison of our method with previous methods on the watertight version of PartObjectarverse-Tiny.}
\label{tab:main_compare_wt}

\end{table}






\subsection{ $\mathcal{X}$-Part: high-fidelity and structure-coherent shape decomposition ~\cite{X-part} }\label{sec:x-part}




This section shows how to decompose the shapes into parts.
Decomposing a complete 3D shape into meaningful semantic parts would greatly facilitate various downstream tasks.
For instance, breaking down a complex geometry into simpler parts can significantly ease the process of mesh re-topology  and uv-unwrapping.
However, generating shapes at the part level presents two major challenges: 1) The decomposed geometry must maintain meaningful part-level semantics, and 2) The generation process must recover geometrically plausible structures for internal regions.


Mainstream part-generation methods adopt the latent vecset diffusion framework~\cite{zhao2025hunyuan3d}, where each part is represented as an independent set of latent codes for diffusion.

The generation process can be executed independently for individual parts (e.g., HoloPart~\cite{yang2025holopart}) or simultaneously for all parts (e.g., PartCrafter~\cite{lin2025partcrafter}, PartPacker~\cite{tang2024partpacker}) to enhance part synchronization. Furthermore, multi-view or 3D segmentation are frequently employed for better part decomposition~\cite{yang2025holopart,yang2025omnipart}. However, these approaches are highly sensitive to inaccuracies in the segmentation results. Alternative works~\cite{lin2025partcrafter,tang2024partpacker} do not explicitly rely on segmentation, but they still fail to offer controllable part-based generation and often produce decomposed parts with ambiguous boundary.


Motivated by these observations, we introduce $\mathcal{X}$-Part, a controllable and editable diffusion framework, which enables semantically meaningful and structurally coherent part generation.
Our objective is to generate high-fidelity and structure-coherent part geometries from a given object point cloud, while ensuring flexible controllability over the decomposition process.
Figure.~\ref{fig:xpart-pipeline} shows the pipeline of our shape decomposition method.




First, to achieve the controllability, we propose a part-level cues extraction module that uses bounding boxes as prompts to indicate part locations and scales, instead of directly using segmentation results as input. Compared with fine-grained and point-level segmentation cues, bounding boxes provide a coarser form of guidance, which mitigates overfitting to the input. Besides, the bounding box provides additional volume scale information for the partially visible part, benefiting the generation and controllability.

\begin{figure*}[!t]
  \centering
  \includegraphics[width=1\linewidth]{./figures/part/xpart/pipeline_v3.jpg}
  \caption{Pipeline of our shape decomposition.}
  \label{fig:xpart-pipeline}
\end{figure*}

Second, despite inaccuracies in the segmentation results, we notice that the high-dimension point-wise semantic feature is free from the information compression caused by the cluster algorithm or prediction head used in~\cite{partfield2025}, resulting in more accurate semantic representations. Therefore, we carefully introduce the semantic features into our framework with delicately designed feature perturbation, which benefits the meaningful part decomposition.

Third, we integrate $\mathcal{X}$-Part into a bounding box based part editing pipeline. It supports local editing, such as merging a small number of parts within an object and adjusting their scales, to facilitate interactive part generation.
To prove the effectiveness of $\mathcal{X}$-Part, we conducted extensive experiments on various benchmarks. Our results show that $\mathcal{X}$-Part achieves state-of-the-art performance in part-level decomposition and generation.

For more details of $\mathcal{X}$-Part, please refer to the paper~\cite{X-part}.





\textbf{Comparison with SOTA.}
We evaluate our method on 200 samples from the ObjaversePart-Tiny dataset, each comprising rendered images and corresponding ground-truth part geometries. To assess geometric quality, we employ Chamfer Distance (CD) and F-Score. The F-Score is computed at two different thresholds $[0.1, 0.5]$ to capture both coarse-level and fine-level geometric alignment. Prior to metric computation, each object is normalized to the range $[-1, 1]$. To ensure pose-agnostic evaluation, we rotate each object by $[0, 90, 180, 270]$ degrees and report the best score among these orientations as the final metric.
As shown in Table \ref{tab:xpart-tabel} and Figure \ref{fig:xpart-parts} our method outperforms all baselines.



\begin{table}[!b]
\centering
\label{tab:performance_comparison_3Dfront}
\begin{tabular}{lccccc}
\toprule
\textbf{Method} & CD↓ & Fscore-0.1↑ & Fscore-0.5↑ \\
\midrule
SAMPart3D  & 0. &  & 0. \\
PartField  & 0.17 & 0.68 & 0.57 \\
HoloPart  & 0.26 & 0.59 & 0.43  \\
OmniPart  & 0.23 & 0.63 & 0.46 \\
Ours      & \textbf{0.11} & \textbf{0.80} & \textbf{0.71}  \\
\bottomrule
\end{tabular}
\caption{Shape Decomposition Results}
\label{tab:xpart-tabel}
\end{table}