<!-- part 8/9 chars 50153-57806 -->

m watertight processing on each independent part mesh separately, ensuring that each part is a topologically closed geometric entity. This step is crucial because many parts may have open boundaries at connection points after decomposition, and watertight processing can complete these boundaries, making each part an independent, complete 3D object.

Through the above complete processing pipeline, we ultimately obtain a high-quality part-level 3D dataset, with each sample containing: a reasonable number of semantically consistent parts, multi-view RGB images and part masks, and watertight holistic and part meshes. This rich data lays a solid foundation for training powerful part generation models, fine-grained 3D understanding or editing models, and simulation environments supporting complex robotic manipulation.

\subsection{Synthetic Data Generation}

\begin{figure}[h]
    \centering
    \includegraphics[width=0.8\linewidth]{figures/data_processing_pipeline_generated.png}
    \caption{Synthetic Data Generating Pipeline.}
    \label{fig:synthetic_data_pipeline}
\end{figure}

We leverage the powerful priors of generative models to synthesize data, aiming to bridge the significant gap in sample counts across object categories that exists in real-world datasets. To achieve this goal, our data synthesis pipeline consists of three main steps: text expansion, image generation, and 3D generation. The overall pipeline is illustrated in the Figure~\ref{fig:synthetic_data_pipeline}.

\textbf{Text Expansion}. We first collected and organized a complete e-commerce product category system from mainstream e-commerce platforms and product databases, constructing a category hierarchy that comprehensively covers real-world products. After excluding service-oriented virtual products (such as insurance, membership services.), we ultimately retained 1,252 specific physical product categories.

Using these product categories as semantic conditions, we employ an LLM model to generate detailed and diverse product descriptions. Our prompt design is centered around the following three points: (1) Ensuring basic rationality and authenticity, generating physically and logically reasonable descriptions around the category; (2) Providing rich visual details, including key attributes such as the object's shape, material, color, and size proportions; (3) Expanding diversity, imaginatively expanding the product's form, materials, and other content within a reasonable range, setting aside limitations of actual craftsmanship, cost, and other factors.


\textbf{Image Generation}. We select Qwen-Image to transform text descriptions into images. Although this model performs excellently in text understanding and image quality, as a general-purpose text-to-image model, it often generates images containing complex backgrounds, or viewpoints unsuitable for 3D generation. To ensure that the generated images are suitable for subsequent 3D generation step, we customize the model behavior through LoRA fine-tuning.

Specifically, our fine-tuning objective is to enable the model to generate images that meet the following quality standards: (1) Clean background: Solid color or simple gradient backgrounds with no complex scene elements, facilitating the separation of foreground objects; (2) Complete object: Ensuring that the overall geometric features can be accurately captured; (3) Appropriate position: The object is located at the image center, occupying a suitable proportion of the frame, avoiding being too large or too small; (4) Reasonable view point: Adopting three-quarter views or other information-rich observation angles that can simultaneously display multiple faces of the object, providing sufficient geometric cues for 3D generation; (5) Information-rich: Clearly displaying the object's key structural features, material properties, and detail elements.


\textbf{3D Generation}. We select the industry-leading HY3D-3.0 model~\cite{hunyuan3d_online} as our 3D generation engine. Leveraging the powerful capabilities of the HY3D-3.0 model, we are able to obtain high-quality 3D assets with the following characteristics: (1) Fine geometry: The generated meshes possess rich geometric details, accurately reconstructing the object's shape features, including complex structures such as edges, bumps, and holes; (2) Clear textures: Accurate texture mapping, with visual attributes such as color, material, and surface details highly consistent with the input image.


\subsection{Data Distribution and Visualization}





{\bf Full-level Data}. Using Objaverse and Objaverse-XL as base data sources, we conducted rigorous quality filtering and data processing workflows, ultimately curating 252,676 high-quality 3D assets for in-depth processing. These assets have undergone the complete data processing pipeline described above, ensuring that each asset meets training-ready standards.

To support model training and scientific evaluation, we perform a split of the dataset: 252,000 samples are allocated to the training set for comprehensive model learning; 276 samples are allocated to the validation set for hyperparameter tuning and model selection during training; and 400 samples are allocated to the test set for final model performance evaluation and benchmarking.

In terms of category coverage, the entire dataset spans 19 top-level categories, further subdivided into 74 mid-level subcategories, and ultimately contains 389 fine-grained classifications, such as Animal-Virtual/Extinct Animals-Anthropomorphic Animals, Weapon-Firearms-Guns.

\begin{figure}[h]
    \centering
    \includegraphics[width=0.9\linewidth]{figures/full_static1.png}
    \caption{The Top-level Category Distribution of Full-level Data.}
    \label{fig:top_level_distribution_full_data}
\end{figure}

\begin{figure}[h]
    \centering
    \includegraphics[width=0.82\linewidth]{figures/full_data_vis.png}
    \caption{Visualization of the full-level dataset, including sharp edge point clouds, random surface point clouds, watertight meshes, and rendered images.}
    \label{fig:full_data_vis}
\end{figure}



{\bf Part-level Data}. The part-level dataset comprises 240,524 samples in total, with a mean component count of 14.13 and a median of 11, exhibiting a diverse distribution of component complexity. Specifically, 24.63\% of samples contain 2-5 components, representing relatively simple object structures; 24.83\% of samples contain 6-10 components, covering objects with moderate structural complexity; 27.00\% of samples contain 11-20 components, encompassing more intricate assemblies; and the remaining samples contain 21-50 components, representing highly complex multi-part objects. The detailed statistical distribution of component counts is illustrated in Fig.~\ref{fig:component_distribution_part_data}.

\begin{figure}[h]
    \centering
    \includegraphics[width=0.95\linewidth]{figures/part_static.png}
    \caption{The Component Distribution of Part-level Data.The prominent peaks at 16, 34, and 35 primarily stem from humanoid models that share identical geometric structures but differ in texture. Considering that various research scenarios and application needs may require such texture variant data, we chose to retain this portion of the data without deduplication.}
    \label{fig:component_distribution_part_data}
\end{figure}

\begin{figure}[h]
    \centering
    \includegraphics[width=0.95\linewidth]{figures/part_data_vis1.png}
    \caption{Part-level dataset visualization, showing individual components and the assembled model color-coded by component ID.}
    \label{fig:full_data_vis}
\end{figure}