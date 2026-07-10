<!-- part 3/5 chars 13106-20480 -->

views or reduce memory overhead \cite{li2024era3d, huang2024epidiff, kant2024spad}, while another technique tiles multiple view images into a single layer, treating them as a unified input during the diffusion model’s denoising process \cite{shi2023zero123++, shi2023mvdream, wu2024unique3d, li2023instant3d}.




\section{Method}
\label{sec:method}


As shown in~\cref{fig:pipeline}, our MaterialMVP generates PBR textures conditioned on a 3D mesh and an image prompt. The 3D mesh is input in the form of normal maps and position maps, which are encoded into latent space and concatenated channel-wise with noise latent as U-Net input. The generated albedo map is expected to be free from lighting information, while the metallic and roughness maps should be both accurate and precisely aligned. In this section, we first review the multi-view image generation diffusion model and the principles of PBR-based material modeling, which form the foundation of our approach. Then, we introduce the Consistency-Regularized Training method, designed to disentangle residual lighting information from the albedo map while improving robustness against input variations. Finally, we present our dual-channel material generation framework, which ensures the precise alignment and fidelity of the generated texture maps.





\subsection{Preliminary}
\label{subsec:pre}
\noindent\textbf{Multi-view Diffusion.}
The Latent Diffusion Model (LDM)~\cite{rombach2022high} is a generative framework that operates in a compressed latent space, combining the principles of diffusion processes with VAEs to generate high-quality images efficiently.
Building upon LDM, existing methods~\cite{long2024wonder3d, wang2023imagedream, tang2024mvdiffusion++} propose multi-view diffusion models that extends the latent space $z$ to multi-view representations $Z=\left \{z_{1},\dots ,z_{n} \right \}$ via multi-view attention as
\begin{equation}
    z_i^{new} = {\sum_{j=1}^{n}} \text{Softmax}(\frac{ Q_i K_j^T}{\sqrt{d}}) \cdot V_j,
    \label{eq:mvattn}
\end{equation}
where $Q$, $K$, and $V$ are the projected features of Query, Key, and Value, enabling synchronized denoising of geometrically consistent multi-view outputs.

\noindent\textbf{PBR Material.}
Our material representation employs the Disney Principled Bidirectional Reflectance Distribution Function (BRDF) framework~\cite{burley2012physically}, defining surfaces through three parameters: albedo, metallic, and roughness. These parameters are stored in two separate textures: a combined MR map storing metallic and roughness data, while albedo remains in an RGB texture map.

\subsection{Consistency-Regularized Training}
\label{subsec:CRTrain}
We observe two key limitations in multi-view PBR synthesis with image prompts: (1) \textbf{view sensitivity}, where slight perturbations in camera pose can lead to dramatically different material outputs, and (2) \textbf{illumination entanglement}, where lighting from the reference images is incorrectly baked into the output, or the pretrained diffusion model generates unintended lighting effects.

To address these issues, we propose a consistency-regularized training strategy that trains the model on pairs of reference images rather than individual samples. At each training step, the diffusion model is jointly conditioned on two reference images. This dual-prompt mechanism introduces implicit geometric consistency constraints to stabilize multi-view generation while encouraging the model to disentangle lighting variations from material features.


\begin{figure}[t]
    \centering
    \includegraphics[width=0.8\linewidth]{./fig/ref_img_pair3.png}
    \vspace{-3.5mm}
    \caption{\textbf{Reference Image Pair Selection.} The selected image pair exhibits perturbations in camera pose and/or lighting. The solid box indicates the chosen reference image, and the dashed box indicates the perturbed reference image.}
    \label{fig:img_pair}
    \vspace{-5.5mm}
\end{figure}


\subsubsection{Reference Pair Selection}
\label{subsubsec: RefPair}

For each object, we construct a candidate set $\mathcal{I}$ of 312 images rendered in various camera poses and lighting conditions at elevation angles $\theta_{c} \in\left\{-20^{\circ}, 0^{\circ}, 20^{\circ}, \text { random}\right\}$, with 24 azimuth angles $\phi_{c}$ uniformly sampled per elevation. For $\theta_{c} \in\left\{-20^{\circ}, 0^{\circ}, 20^{\circ}\right\}$, each pose is rendered under three random HDR lighting conditions; for $\theta_{c}=\text{random}$, each pose is rendered under a single point light with random light elevation $\theta_{l} \in\left\{-30^{\circ}, 0^{\circ}, 30^{\circ}\right\}$ and light azimuth $\phi_{l} \in\left\{-45^{\circ}, 0^{\circ}, 45^{\circ}\right\}$.
As shown in \cref{fig:img_pair}, to select a reference pair $(I_1,I_2)$, we first choose $I_1$ from $\mathcal{I}$ with probability $p$ favoring point light images (in practice, we set $p=0.4$), and then select $I_2$ from the subset $\mathcal{S}(I_1)$ defined as
\begin{equation}
\mathcal{S}\left(I_{1}\right)=\left\{I \in \mathcal{I} \mid \phi_{c}(I) \in\left\{\phi_{c}\left(I_{1}\right), \phi_{c}\left(I_{1}\right)\pm15^{\circ}\right\}\right\},\nonumber
\end{equation}
where $\phi_{c}(I)$ denotes the camera azimuth angle of image $I$. The selection process can be compactly expressed as
\begin{equation}
(I_1, I_2) = \left( \text{Sample}(\mathcal{I}, p), \text{Sample}(\mathcal{S}(I_1)) \right),\nonumber
\end{equation}
where $\text{Sample}(\mathcal{I}, p)$ samples $I_1$ with probability $p$ for point light images, and $\text{Sample}(\mathcal{S}(I_1))$ uniformly selects $I_2$ from $\mathcal{S}(I_1)$. In this way, we obtain a reference image pair with subtle differences in viewpoint and lighting.


\begin{table*}[t]
\centering
\caption{Quantitative comparison with state-of-the-art methods. We compare with two classes of methods, one conditioned on text only, and the other one based on image. Our method achieves the best performance compared with both classes.}
\vspace{-3.5mm}
\setlength{\tabcolsep}{5pt}\small
\begin{tabular}{ccccccc}
\toprule
Method   & Condition     & {CLIP-FID$\downarrow$} & {FID$\downarrow$} & {CMMD$\downarrow$} & {CLIP-I$\uparrow$} & {LPIPS$\downarrow$}  \\ \midrule
Text2Tex \cite{chen2023text2tex} \textcolor{blue}{\textsubscript{ICCV'23}}  & Text          & 31.83    & 187.7      & 2.738 & -      & 0.1448 \\
SyncMVD \cite{liu2024text} \textcolor{blue}{\textsubscript{SIGGRAPH Asia'24}}   & Text          & 29.93    & 189.2      & 2.584 & -      & 0.1411 \\
Paint-it \cite{youwang2024paint} \textcolor{blue}{\textsubscript{CVPR'24}} & Text          & 33.54    & 179.1      & 2.629 & -      & 0.1538       \\
Paint3D \cite{zeng2024paint3d} \textcolor{blue}{\textsubscript{CVPR'24}} & Text          & 30.17    & 185.7      & 2.755 & -      & 0.1388 \\
\hline
Paint3D \cite{zeng2024paint3d} \textcolor{blue}{\textsubscript{CVPR'24}}& Image          & 26.86    & 176.9      & 2.400 & 0.8871      & 0.1261       \\
TexGen \cite{yu2024texgen} \textcolor{blue}{\textsubscript{TOG'24}}  & Text + Image & 28.23    & 178.6      & 2.447 & 0.8818 & 0.1331       \\
Ours     & Image         & \textbf{24.78}    & \textbf{168.5}      & \textbf{2.191} & \textbf{0.9207} & \textbf{0.1211}       \\ \bottomrule
\end{tabular}
\label{tab: comparisons}
\vspace{-5.5mm}
\end{table*}


\subsubsection{Training Strategy}