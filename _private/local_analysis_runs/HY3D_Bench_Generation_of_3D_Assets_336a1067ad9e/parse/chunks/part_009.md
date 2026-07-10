<!-- part 9/9 chars 57456-65094 -->

tion.}
    \label{fig:component_distribution_part_data}
\end{figure}

\begin{figure}[h]
    \centering
    \includegraphics[width=0.95\linewidth]{figures/part_data_vis1.png}
    \caption{Part-level dataset visualization, showing individual components and the assembled model color-coded by component ID.}
    \label{fig:full_data_vis}
\end{figure}




{\bf Synthetic Data}. The Synthetic Data contains more than 125k samples. The category system design of this dataset fully considers the needs of real-world applications, ultimately encompassing 20 top-level categories, 130 mid-level subcategories, and 1,252 fine-grained classifications of product data. The breadth and depth of this category system far exceed existing real datasets, with coverage ranging from daily necessities and consumer electronics to professional industrial products.

\begin{figure}[h]
    \centering
    \includegraphics[width=0.95\linewidth]{figures/gen_static.png}
    \caption{The Top-level Category Distribution of Synthetic Data.}
    \label{fig:component_distribution_gen_data}
\end{figure}

\begin{figure}[h]
    \centering
    \includegraphics[width=0.95\linewidth]{figures/gen_data_vis.png}
    \caption{Synthetic dataset visualization, showing diverse samples from 5 fine-grained categories.}
    \label{fig:full_data_vis}
\end{figure}





\section{Evaluation}

\subsection{Implementation Details}
To validate the effectiveness of Full-level Data in 3D generation tasks, we use Hunyuan3D-2.1 as our baseline. While maintaining the core architectural design principles, we appropriately scale down the model to reduce training costs and train a lightweight Hunyuan3D-2.1-Small model. For evaluation, we use ULIP~\cite{xue2023ulip} and Uni3D~\cite{zhou2023uni3d} to measure the consistency between images and generated meshes.

\textbf{Model Architecture Adjustments}. Compared to the original Hunyuan3D-2.1 model, our Small model incorporates the following key architectural modifications to balance model capacity with training efficiency: (1) Channel dimension reduction: We reduce the base channel dimension from 2048 to 1536. (2) Architecture simplification: We remove the Mixture of Experts (MoE) structure and adopt a fully Dense architecture instead. After these adjustments, our Hunyuan3D-2.1-Small model contains 832M parameters.

\textbf{Progressive Training Strategy}. Drawing on the successful experience of Hunyuan3D-2.1, we employ a progressive token resolution training strategy, starting from 512 tokens and gradually increasing the token count to improve representation fidelity, ultimately reaching 4096 tokens. Detailed training configurations are provided in Table~\ref{tab:full_level_data_train}.

\begin{table}[h]
    \centering
    \begin{tabular}{c||c|c|c|c}
    \hline
         Tokens &  Batch size & Image Size & Learning rate & Traning steps \\
    \hline
         512 & 512 & 224 & 1.e-4 & 800k \\
         2048 & 256 & 224 & 5.e-5 & 400k \\
         2048 & 256 & 518 & 5.e-5 & 200k \\
         4096 & 128 & 518 & 1.e-5 & 400k \\
    \hline
    \end{tabular}
    \caption{Hunyuan3D-2.1-Small Training Strategy.}
    \label{tab:full_level_data_train}
\end{table}

\subsection{Experimental Results}

To comprehensively evaluate the effectiveness of our full-level dataset, we conducted comparative experiments with several representative state-of-the-art open-source methods, including Michelangelo~\cite{zhao2024michelangelo}, Craftsman~\cite{li2024craftsman}, Trellis~\cite{xiang2024structured}, and Hunyuan3D 2.1~\cite{hunyuan3d2025hunyuan3d}. These baseline methods have all demonstrated outstanding performance in the field of 3D generation. As shown in Table~\ref{tab:full_level_data_eval} and Figure~\ref{fig:full_level_data_eval}, despite having significantly fewer parameters than Trellis and Hunyuan3D 2.1, our model achieves comparable generation quality when trained on our open-sourced dataset, while outperforming the similarly-sized Craftsman. This experimental result fully demonstrates the high-quality characteristics of our open-sourced dataset. Meanwhile, this also indicates that data quality plays a crucial role in 3D generation tasks. The dataset we have constructed can provide the community with an efficient training resource, enabling researchers to focus more on algorithm innovation and model optimization rather than tedious data processing and preparation work.

\begin{table}[h]
    \centering
    \begin{tabular}{c|c|c|c|c}
    \hline
         Methods &  Token length & Model Size (M) & Uni3D-I $\uparrow$ & ULIP-I $\uparrow$ \\
    \hline
         Michelangelo~\cite{zhao2024michelangelo} & 257 & 105 & 0.3169 & 0.2186 \\
         CraftsMan~\cite{li2024craftsman} & 2048 & 852 & 0.3351 & 0.2264 \\
         Trellis~\cite{xiang2024structured} & 10000* & 1156 & 0.3641 & 0.2454 \\
         Hunyuan3D 2.1~\cite{hunyuan3d2025hunyuan3d} & 4096 & 1238 & 0.3636 & 0.2446 \\
         Ours  & 4096 & 832 & 0.3606 & 0.2424 \\
    \hline
    \end{tabular}
    \caption{The quantitative comparison for image-to-3D generation on our test dataset.``*'' denotes the average token length for active voxel.}
    \label{tab:full_level_data_eval}
\end{table}

\begin{figure}[h]
    \centering
    \includegraphics[width=0.95\linewidth]{figures/eval_full.png}
    \caption{The qualitative comparison for image-to-3D generation on our test dataset.}
    \label{fig:full_level_data_eval}
\end{figure}


\section{Conclusion}
In this work, we present HY3D-Bench, an open-source ecosystem designed to surmount the data processing bottlenecks currently constraining 3D generative models. We establish a unified foundation through three key contributions. First, we curate a high-fidelity library of 252k 3D objects derived from large-scale repositories such as Objaverse and Objaverse-XL. We employ a rigorous, multi-stage pipeline to ensure training readiness, producing essential artifacts such as watertight meshes and multi-view renderings. Second, we introduce 240k structured part-level decomposition, providing the granularity essential for advancing fine-grained perception, part-aware generation, and controllable 3D editing. Third, to mitigate real-world data distribution gaps, we develop a scalable AIGC-driven synthesis pipeline, contributing 125k synthetic assets to enrich diversity within long-tail categories. Empirical validation using the Hunyuan3D-2.1-Small model confirms the practical utility of our dataset. By democratizing access to these resources, HY3D-Bench aims to catalyze innovation across 3D perception, robotics, and digital content creation. Future efforts will focus on extending this framework to include dynamic assets and broader tasks.



\clearpage


\section{Contributors}
\large{Authors are listed \textbf{alphabetically by the first name}.}
\definecolor{tencentblue}{RGB}{38,54,221}
\large{
\color{tencentblue}
\begin{multicols}{2}
\raggedcolumns
Bowen Zhang\\
Chunchao Guo\\
Dongyuan Guo\\
Haolin Liu\\
Hongyu Yan\\
Huiwen Shi\\
Jiaao Yu\\
Jiachen Xu\\
Jingwei Huang\\
Kunhong Li\\
Lifu Wang\\
Linus\\
Penghao Wang\\
Qingxiang Lin\\
Ruining Tang\\
Xianghui Yang\\
Yang Li\\
Yunfei Zhao\\
Yunhan Yang\\
Zeqiang Lai\\
Zhihao Liang\\
Zibo Zhao\\
\end{multicols}}

\large{Other contributors are listed \textbf{alphabetically by the first name}.}
\definecolor{tencentblue}{RGB}{38,54,221}
\large{
\color{tencentblue}
\begin{multicols}{2}
\raggedcolumns
Chao Zhang\\
Edwarrd Wang\\
Hao Zhang\\
Jiaxin Lin\\
Peng He\\
Yirui Guan\\
Yonghao Tan\\
Zheng Ye\\
\end{multicols}}

\clearpage

\bibliography{colm2024_conference}
\bibliographystyle{colm2024_conference}


\end{document}