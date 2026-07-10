<!-- part 2/5 chars 6324-13456 -->

the input images.


We introduce MaterialMVP, a one-stage model designed to generate PBR textures for 3D meshes. Our model produces multi-view, high-quality PBR textures, including albedo, metallic, and roughness maps. These textures not only highly follow the input reference images but also ensure precise alignment between different texture maps.

To be specific, we employ a Multiview Diffusion Model framework designed to generate multiple view-consistent PBR maps from image prompts. To simultaneously produce albedo, metallic, and roughness maps, we introduce a Dual-Channel Material Generation framework, which extends the original diffusion model by adding an extra channel to generate metallic-roughness (MR) alongside the existing albedo channel. For the input reference image, we utilize Reference Attention, leveraging a reference branch to extract detailed information from the input. This ensures the generated textures retain fine details and remain faithful to the reference. To address issues such as unwanted lighting artifacts in diffusion-generated outputs and improve the model’s robustness to input viewpoint perturbations, we introduce Consistency-Regularized Training. This strategy trains the model on pairs of reference images with subtle variations in camera pose and lighting but requires the model to produce identical, lighting-invariant results. This forces the model to learn lighting-invariant and accurate PBR maps across diverse conditions. Additionally, to tackle the misalignment problem in PBR material generation tasks, we design a Multi-Channel Aligned Attention module to synchronize information between the albedo and MR channels, ensuring the output materials are well-aligned and do not produce unexpected shadows or artifacts on textured meshes. At the same time, we incorporate Learnable Material Embeddings for each channel, providing additional context to help each channel learn its unique distribution, resulting in artifact-free and coherent textures.

In summary, our contributions are as follows. 1) We propose MaterialMVP, an end-to-end multi-view PBR material generation model that produces high-quality, multi-channel-aligned, and view-consistent textures. 2) We introduce Consistency-Regularized Training to improve model robustness to viewpoint perturbations and effectively disentangle lighting effects from material properties, producing lighting-invariant and accurate PBR maps. 3) We develop a Dual-Channel Material Generation framework, which processes albedo and metallic-roughness maps in separate channels. Leveraging Multi-Channel Aligned Attention and enhanced by Learnable Material Embeddings, it produces high-quality, coherent, and artifact-free textures.
\section{Related Work}
\label{sec:formatting}

\begin{figure*}[t]
    \centering
    \includegraphics[width=0.9\linewidth]{./fig/overview.pdf}
    \vspace{-3.5mm}
    \caption{Overview of MaterialMVP, which takes a 3D mesh and a reference image as input and generates high-quality PBR textures through multi-view PBR diffusion. The albedo and MR channels are aligned via MCAA, effectively reducing artifacts. And Consistency-Regularized Training effectively eliminates illumination and addresses material inconsistency across multi-view PBR textures. }
    \label{fig:pipeline}
    \vspace{-3.5mm}
\end{figure*}


\noindent\textbf{Texture Generation.}
The development of 3D generation has significantly advanced the creation of high-quality textures for 3D meshes \cite{yu2023texture,richardson2023texture,cao2023texfusion,chen2023text2tex,le2023euclidreamer,tang2024intex,chen2024scenetex,zeng2024paint3d,zhang2024repaint123,bensadoun2024meta,lu2024direct2,zhao2025hunyuan3d,xiang2024make,yu2024texgen}. Extending text-to-image diffusion models\cite{ho2020denoising,song2020denoising,rombach2022high,podell2023sdxl,li2024hunyuan} provides a foundation for generating detailed and semantically coherent textures from textual descriptions \cite{richardson2023texture, cao2023texfusion, chen2023text2tex, le2023euclidreamer, tang2024intex, chen2024scenetex, liu2024text, zhang2024texpainter, bensadoun2024meta, lu2024direct2}. Building upon this, using image prompts as input enables textures to closely align with specific visual references \cite{zeng2024paint3d,
zhang2024repaint123, zhao2025hunyuan3d, zhang2024clay,yu2024texgen}. Advancing further, 3D priors, such as depth maps \cite{le2023euclidreamer, tang2024intex, zhang2024repaint123, xiang2024make}, normal maps \cite{bensadoun2024meta, lu2024direct2, zhao2025hunyuan3d}, and position maps \cite{bensadoun2024meta, zhao2025hunyuan3d, zeng2024paint3d}, ensures that the textures are not only visually realistic but also geometrically consistent with the underlying 3D structure.

\noindent\textbf{PBR Generation.}
PBR simulates light-surface interactions with physically accurate material properties, driving extensive research into PBR information estimation \cite{chen2023fantasia3d, zhang2024dreammat, wu2023hyperdreamer, xu2023matlaber, yeh2024texturedreamer, vainer2024collaborative, sartor2023matfusion, vecchio2024matfuse, xiang2024make, youwang2024paint, liu2024unidream, chen2024intrinsicanything, zhang2024mapa, fang2024make, xiong2024texgaussian} for high-quality 3D texture generation. Generation-based approaches \cite{vainer2024collaborative, sartor2023matfusion, vecchio2024matfuse, chen2024intrinsicanything, zeng2024rgb} leverage diffusion models to learn material priors and recover PBR properties through physical rendering; retrieval-based techniques \cite{zhang2024mapa, fang2024make} adapt pre-built material graphs from libraries to ensure visual consistency and editability; optimization-based methods \cite{chen2023fantasia3d, zhang2024dreammat, wu2023hyperdreamer, xu2023matlaber, yeh2024texturedreamer, youwang2024paint, liu2024unidream} first generate initial textures and then refine them through techniques like Score-Distillation Sampling \cite{poole2022dreamfusion}.





\noindent\textbf{Multi-view Generation.}
Multi-view generation \cite{wang2023imagedream, liu2024oneA, liu2024oneB, hu2024mvd, ding2024text, tang2024mvdiffusion++, wen2024ouroboros3d, woo2024harmonyview, long2024wonder3d, yang2024hunyuan3d, shi2023zero123++, shi2023mvdream, li2024era3d, li2025multi, li2025cmd, li2024pshuman} has been adopted in texture generation \cite{liu2024text, zhang2024texpainter, bensadoun2024meta, lu2024direct2, zhao2025hunyuan3d, deng2024flashtex, zhang2024clay} to address issues such as blurring or artifacts.
Some methods integrate viewpoint information or 3D priors \cite{chen2024cascade, jeong2024nvs, liu2023syncdreamer, yang2024consistnet, yang2024viewfusion, hollein2024viewdiff}.
Other approaches utilize epipolar geometry to improve consistency between views or reduce memory overhead \cite{li2024era3d, huang2024epidiff, kant2024spad}, while another technique tiles multiple view images into a single layer, treating them as a unified input during the diffusion model’s denoising process \cite{shi2023zero123++, shi2023mvdream, wu2024unique3d, li2023instant3d}.




\section{Method}
\label{sec:method}