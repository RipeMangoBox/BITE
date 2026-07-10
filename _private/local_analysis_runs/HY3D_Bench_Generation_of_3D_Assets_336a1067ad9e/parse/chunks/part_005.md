<!-- part 5/9 chars 27795-35673 -->

0213d} provide datasets with part-level annotations. While these methods present impressive performance in the 3D generation task, they usually rely on high-quality data processing in terms of the part-aware mesh and watertight mesh. In this paper, we open-source large-scale processed data that can be used to train 3D VAE and diffusion directly.




\subsection{3D Datasets}
The advancement of 3D generation models is inherently tied to the availability of high-quality benchmark datasets, which provide the foundational data support for model training, validation, and evaluation. Early 3D benchmark datasets~\cite{zhou2016thingi10k,fu20213d,downs2022google,wu2023omniobject3d}, such as ShapeNet~\cite{chang2015shapenet}, laid the initial groundwork for the development of 3D generation research. However, these datasets suffer from limitations such as a limited number of categories, simple geometry, and small quantities, which severely constrain the generalization capabilities of trained 3D generation models. This bottleneck has long restricted the further advancement of 3D generation technology towards more practical and versatile scenarios. The emergence of large-scale 3D datasets with complex geometric structures has broken this deadlock, among which Objaverse stands out as a pivotal milestone. As the large-scale, diverse 3D object dataset, Objaverse~\cite{objaverse} and Objaver-XL~\cite{objaverseXL} contain millions of 3D models spanning a wide range of categories, including complex geometric structures such as articulated objects, organic shapes, and detailed industrial parts. The release of Objaverse has significantly empowered the development of 3D generation technology, particularly fostering the advent of a new generation of large-scale 3D generation models.


However, a critical challenge persists in the current 3D generation research landscape: mainstream 3D generation models typically require extensive preprocessing of raw 3D data to generate task-specific representations, such as rendered images, watertight meshes, and corresponding Signed Distance Function (SDF) fields. This preprocessing step not only increases the entry barrier for researchers new to 3D generation, requiring proficiency in specialized data processing techniques, but also imposes substantial computational burdens. Although open-source data processing scripts have been developed to alleviate some of these difficulties by automating certain preprocessing workflows, processing large-scale training datasets (often involving millions of 3D models) demands enormous GPU and CPU computational resources. This resource-intensive preprocessing requirement remains a significant bottleneck for the broader research community, hindering the rapid iteration and widespread adoption of 3D generation models.

To address this critical challenge, in this paper, we directly provide a high-quality dataset of 200k samples specifically tailored for training 3D Variational Autoencoders (3D VAE) and 3D diffusion models. The data samples are curated from two large-scale 3D repositories, Objaverse and Objaverse-XL, ensuring rich category diversity and complex geometric characteristics. Notably, we process the 3D meshes to obtain watertight meshes at a resolution of 512, which effectively preserves a large number of fine-grained details from the original meshes. By offering this preprocessed, high-resolution 3D dataset, we aim to reduce the computational and technical burdens on researchers, lower the entry barrier for 3D generation research, and further facilitate the advancement of the field.


\section{Methods}



{\bf VAE}. Given an input point cloud $P \in R^{N \times (3 + C)}$ sampled from the mesh surface, where $C$ denotes surface normals, 3D VAE first extract point features and then obtain the corresponding latent vector set $Z \in R^{L \times d}$ via resampling from estimated distribution, where $L$ and $d$ indicate the length and dimension of latent VecSet, respectively. Subsequently, a decoder is applied to reconstruct the signed distance function (SDF) field $F_{sdf}$, in which we can leverage the iso-surface extraction to obtain explicit mesh output. The procedure of VAE can be formulated as follows:
\begin{align}
Z = \mathcal{E}(P), F_{sdf} = \mathcal{D}(Z)
\end{align}


{\bf Diffusion}. Given an image and its latent set representation $Z$ of a shape, the 3D diffusion model aims to model the denoising process, thereby achieving conditional generation from an arbitrary image. It first leverages an image encoder, such as DINO-v2~\cite{}, to capture image embeddings $c_i$ and then exploits the multi layers of DiT to predict the added noise or velocity. For a flow matching model used in Hunyuan3D 2.1~\cite{}, its training objective is to transform a simple noise distribution $x_0 \sim \mathcal{N}(0, I)$ into a complex data distribution $x_1 \sim D$ conditioned on image embeddings $c_i$, which can be formulated as follows:
\begin{equation}
\mathbb{E}_{t, {x}_0, {x_1}, c}\vert\vert{v}_\theta({x}, t, c)-(x_1-x_0)\vert\vert_2^2
\end{equation}






\section{Hunyuan Objarverse}





The currently open-source Objaverse series datasets~\cite{objaverse,objaverseXL} contain a vast collection of raw 3D assets available for access and download. However, these raw assets suffer from numerous critical issues that urgently need to be addressed, rendering them unsuitable for direct application in downstream tasks such as 3D generation.

First, from a technical specification perspective, various types of 3D assets produced by different 3D modeling software (such as Blender, Maya, 3ds Max, etc.) exhibit significant format discrepancies and lack of standardization. Specifically: (1) Inconsistent coordinate system definitions: Different software packages adopt varying coordinate system conventions (e.g., left-handed vs. right-handed systems, Y-up vs. Z-up, etc.), resulting in orientation errors or mirror flipping when assets are loaded in different environments; (2) Complex and diverse asset construction methods: Many assets employ multi-level node hierarchies, contain parent-child node scale inheritance relationships, and include hidden transformation matrices, which greatly increase the complexity of data processing.

Second, from a data quality perspective, the quality of various 3D assets is highly inconsistent, exhibiting significant heterogeneity. The main issues include: (1) Poor geometric quality: A large number of assets have overly simplified meshes with insufficient polygon counts, failing to accurately represent the detailed features of objects. Additionally, severe topological defects exist, such as non-manifold edges, self-intersecting faces, and isolated vertices. These problems render the assets unsuitable for tasks requiring watertight meshes (such as physical simulation, 3D printing, etc.); (2) Texture mapping errors: Some assets have serious UV unwrapping problems, with incorrect texture-to-geometry mapping, excessively low texture resolution, or missing textures, which compromise rendering quality.

Finally, from a data ecosystem perspective, existing datasets also suffer from the following systemic deficiencies: (1) Severely imbalanced category distribution: The datasets exhibit pronounced long-tail distribution characteristics, with abundant assets in common categories (such as chairs and tables), while assets in many rare categories that are important for real-world applications are extremely scarce, limiting the generalization capability of models; (2) Lack of structured information: The vast majority of assets are holistic, monolithic meshes, lacking hierarchical part decomposition and assembly relationship descriptions, which severely constrains the development of advanced applications such as fine-grained understanding, editable generation, and robotic manipulation.