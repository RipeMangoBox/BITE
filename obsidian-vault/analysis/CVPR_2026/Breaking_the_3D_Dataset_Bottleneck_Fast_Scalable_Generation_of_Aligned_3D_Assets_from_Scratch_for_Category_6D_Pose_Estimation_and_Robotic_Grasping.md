---
title: "Breaking the 3D Dataset Bottleneck: Fast Scalable Generation of Aligned 3D Assets from Scratch for Category 6D Pose Estimation and Robotic Grasping"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Breaking_the_3D_Dataset_Bottleneck_Fast_Scalable_Generation_of_Aligned_3D_Assets_from_Scratch_for_Category_6D_Pose_Estimation_and_Robotic_Grasping.pdf
project_link: "https://genomni3d.github.io/"
code_link: null
aliases:
- GP3
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
core_operator: 在文本到图像生成阶段引入深度条件（深度图作为ControlNet条件）显式控制物体朝向，从而将规范对齐能力内嵌于生成流水线的前端，摆脱了后续手动对齐的需求。
primary_logic: 深度条件图像生成能够同时保留物体的全局结构与空间姿态，而不过度约束局部几何与纹理变化，使得从单张图像重建的3D网格天然具有一致的规范朝向，彻底解决了从无到有大规模生成对齐3D资产的核心难题。
claims:
- 流水线能在每个对象不到3分钟的时间内生成高质量、对齐的3D网格，相比传统扫描加速5–20倍。
- 深度条件将NOCS类别的平均姿态一致性从57%提升至97%，并在153个Omni6Dpose类别上达到96%的网格姿态一致性。
- 生成的网格使抓取成功率提升至87.8%，大幅超越先前方法（CenterGrasp 82.7%，GIGA 63.8%）。
- NOCS REAL275 (zero-shot Sim2Real 6D pose) 上 平均6D姿态精度 (Avg 6D pose accuracy) = 34.75 (GenNOCS混合现实+阴影)
---

# Breaking the 3D Dataset Bottleneck: Fast Scalable Generation of Aligned 3D Assets from Scratch for Category 6D Pose Estimation and Robotic Grasping

> [!tip] 核心洞察
> 深度条件图像生成能够同时保留物体的全局结构与空间姿态，而不过度约束局部几何与纹理变化，使得从单张图像重建的3D网格天然具有一致的规范朝向，彻底解决了从无到有大规模生成对齐3D资产的核心难题。

| 字段 | 内容 |
|------|------|
| 中文题名 | 打破3D数据集瓶颈：从零快速规模化生成对齐3D资产，用于类别级6D姿态估计与机器人抓取 |
| 英文题名 | Breaking the 3D Dataset Bottleneck: Fast Scalable Generation of Aligned 3D Assets from Scratch for Category 6D Pose Estimation and Robotic Grasping |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Guillaume_Breaking_the_3D_Dataset_Bottleneck_Fast_Scalable_Generation_of_Aligned_CVPR_2026_paper.html) · [Project](https://genomni3d.github.io/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation |
| Method | GenOmni3D Pipeline（基于深度条件控制的文本到图像到3D生成流水线） |
| Dataset | NOCS REAL275, 自定义SAPIEN抓取仿真（NOCS类别）, NOCS合成验证集（in-domain） |

> [!tip] 效果简介
> - NOCS REAL275 (zero-shot Sim2Real 6D pose) 上，平均6D姿态精度 (Avg 6D pose accuracy) 34.75 (GenNOCS混合现实+阴影) vs 33.10 (纯合成Replica训练) (+1.65)。
> - 自定义SAPIEN抓取仿真（NOCS类别） 上，抓取成功率 (Grasp Success Rate %) 87.8 (Custom-CG on our meshes) vs 82.7 (CenterGrasp on OmniObject3D) (+5.1)。
> - NOCS合成验证集（in-domain） 上，平均6D姿态精度 (Avg 6D pose accuracy) 23.91 (GenNOCS meshes) vs 15.66 (original NOCS synthetic meshes) (+8.25)。

## 概述

类别级6D姿态估计与机器人抓取长期受困于一个根本性瓶颈：大规模、高质量且规范对齐的3D数据极度匮乏。现有数据集要么实例数与类别数有限，要么缺乏统一的规范朝向，要么依赖昂贵的人工扫描与艺术家建模，难以支撑稳健的视觉学习。本文提出的**GenOmni3D流水线**直指这一症结，首次实现了从文本类别描述到对齐3D资产的完全自动化生成，将单物体网格生成时间压缩至**3分钟以内**——相比传统扫描流程加速5–20倍。

流水线的核心创新在于**将规范对齐能力内嵌于生成前端**：在文本到图像生成阶段引入深度图作为ControlNet条件，显式控制物体朝向。这一设计使得生成图像在保留局部几何与纹理多样性的同时，天然具备一致的全局姿态，从而让后续3D重建无需任何手动对齐后处理。实验表明，深度条件将NOCS类别的平均姿态一致性从**57%** 提升至**97%**，在153个Omni6Dpose类别上达到**96%** 的网格姿态一致性。

在下游任务验证中，基于GenOmni3D生成数据训练的抓取模型在仿真环境中达到**87.8%** 的成功率，显著超越CenterGrasp（82.7%）和GIGA（63.8%）；在NOCS REAL275的零样本Sim2Real 6D姿态估计任务上，混合现实渲染策略使真实场景精度从30.83提升至**34.75**，验证了生成数据的实用迁移能力。

**方法定位**：GenOmni3D属于“文本→深度条件图像→3D网格”的生成式数据扩增范式，其核心调控变量是深度条件信号，区别于纯文本提示的生成方法（如GenVegeFruits3D）和纯合成渲染流水线（如Omni6D）。该方法在数据规模、对齐质量与生成效率三个维度上同时实现了突破，为类别级3D视觉任务提供了可规模化的数据基础。

## 背景与动机

类别级6D姿态估计旨在从单张RGB-D图像中预测物体实例的三维位置、朝向及尺寸，是机器人抓取、增强现实和场景理解等下游任务的关键感知能力。然而，该领域长期受困于一个根本性瓶颈：**大规模、高质量且规范对齐的3D数据极度匮乏**。与实例级任务不同，类别级方法需要覆盖同一类别内丰富的几何与纹理变化，这对训练数据的数量、多样性和一致性提出了极高要求。

现有3D数据集在三个维度上存在显著缺口。第一，**规模与类别覆盖不足**：真实扫描数据集（如NOCS）仅包含6个类别、每个类别数十个实例，难以支撑深度学习模型对类内变化的充分建模；艺术家手工创建的合成资产虽然质量可控，但制作成本高昂，难以规模化扩展。第二，**规范朝向缺失**：大多数现有3D网格缺乏统一的规范坐标系对齐——同一类别的不同实例可能具有任意的初始朝向，这使得从数据中学习一致的姿态表示变得极为困难。第三，**生成效率低下**：先前的生成式3D数据集方法（如**GenVegeFruits3D**，Duret et al., HAL 2025）仅适用于对称物体，且需要大量人工过滤筛除低质量生成结果（过滤比例超过15倍），无法支撑大规模、多类别的自动化数据生产。

上述数据瓶颈直接制约了下游任务性能的上限。在6D姿态估计中，基于纯合成渲染的流水线（如**Omni6D**，Zhang et al., ECCV 2024）虽然能够生成大规模标注数据，但其使用的3D资产仍依赖现有数据集，未能从根本上解决资产匮乏问题。在机器人抓取中，**CenterGrasp**（Chisari et al., IEEE RA-L 2024）和**GIGA**（Jiang et al., arXiv 2021）等方法高度依赖训练数据的3D几何质量，数据不足直接导致抓取成功率受限。

本文的核心动机源于一个关键观察：**文本到图像生成模型具备保留物体全局结构与空间姿态的能力，而深度图作为中间表示可以显式编码规范朝向信息**。这一洞察指向了一条从零自动化生成对齐3D资产的全新路径——通过在前端引入深度条件控制，将规范对齐能力内嵌于生成流水线，从而彻底摆脱对人工对齐或后处理过滤的依赖。基于此，本文提出GenOmni3D流水线，旨在以每个物体不到3分钟的速度、5–20倍于传统扫描的加速比，实现大规模、高质量、规范对齐的3D网格生成，为类别级6D姿态估计和机器人抓取提供前所未有的数据支撑。

## 核心创新

本工作的核心创新在于将**规范对齐能力内嵌于生成流水线的前端**，从而彻底绕过了传统方法中“先生成、后对齐”的低效范式。具体而言，GenOmni3D Pipeline 通过三个关键槽位的替换，实现了从文本描述到对齐3D资产的全自动规模化生成。

### 从文本到深度条件：对齐机制的根本性变革

此前基于文本到图像生成3D数据的方法（如 **GenVegeFruits3D**，Duret et al., HAL 2025）仅使用文本提示作为生成控制信号，其致命弱点在于无法约束物体的空间朝向。文本描述“一把朝左的椅子”对扩散模型而言缺乏几何约束力，导致生成的图像中物体姿态随机分布——这对于类别级6D姿态估计而言是灾难性的，因为规范姿态的一致性直接决定了NOCS坐标映射的可学习性。

GenOmni3D 的核心洞察在于：**深度图是连接语义控制与几何约束的最优信号载体**。深度图天然编码了物体的全局结构与空间姿态，却不过度约束局部几何变化和纹理细节。这一特性使其成为ControlNet条件的理想选择——它既能强制生成图像中的物体保持目标朝向，又为纹理多样性留出了充足的生成空间。

消融实验（Table 3）为这一设计提供了决定性证据：在NOCS的六个类别上，纯文本生成的平均姿态一致性仅为57%，其中复杂非对称物体（如相机、笔记本电脑）的一致性更是骤降至约20%。引入深度条件后，平均一致性跃升至**97%**，且在153个Omni6Dpose类别上达到了**96%的网格姿态一致性**。这一近40个百分点的提升并非渐进式改进，而是从“不可用”到“可规模化部署”的质变。

### 深度条件与纹理多样性的解耦设计

方法谱系中的一个关键创新在于**几何约束与纹理生成的解耦**。流水线首先通过LLM驱动的几何提示工程生成100张带有随机化形状描述的深度图，随后每张深度图作为ControlNet条件，结合LLM生成的纹理提示，产生10个纹理变体。这一设计实现了两个看似矛盾目标的统一：

- **姿态一致性**：同一深度图条件保证所有纹理变体共享相同的规范朝向；
- **纹理多样性**：不同的纹理提示确保生成的资产具有丰富的视觉外观，避免过拟合。

相比GenVegeFruits3D需要人工过滤超过15倍生成量的做法，GenOmni3D借助Hunyuan3D-v2.0的高质量重建能力，几乎消除了人工过滤环节，真正实现了从类别描述到1000个对齐网格的全自动生成。

### 方法谱系与知识库定位

从数据集构建范式来看，GenOmni3D填补了生成式3D资产与规范化6D姿态数据之间的空白。现有3D网格数据集（Table 1）可分为三类：真实扫描（R）、艺术家合成（S）和生成式AI资产（SAI）。前两类受限于采集成本和类别覆盖，而此前的SAI方法（如GenVegeFruits3D）仅适用于对称物体且缺乏对齐机制。GenOmni3D首次在SAI范式下实现了跨153个类别的**内置规范对齐**。

在6D姿态数据生成流水线方面，本工作继承并扩展了 **Omni6D**（Zhang et al., ECCV 2024）的合成渲染框架和 **Omni6DPose**（Zhang et al., ECCV 2024）的混合现实渲染策略，但将上游的3D资产来源从人工建模替换为全自动生成，使数据生产速度提升5–20倍（每对象不到3分钟）。下游实验中，用生成的GenNOCS网格替换原始NOCS合成物体后，域内6D姿态精度从15.66提升至23.91（+8.25），验证了生成资产的质量足以支撑高精度学习。

## 整体框架

GenOmni3D流水线旨在以全自动方式将类别描述转化为大规模、高质量且具有规范朝向一致性的3D网格资产。其核心设计逻辑在于：**将规范对齐能力内嵌于生成流水线的前端**——通过在文本到图像的生成阶段引入深度图作为显式空间控制信号，使后续3D重建天然继承一致的物体朝向，从而彻底摆脱对后期手动对齐的依赖。

### 流水线总览

整个流水线由四个顺序模块构成，如Figure 1所示：

1. **基于LLM的几何提示工程（LLM-based Geometry Prompt Engineering）**：利用大语言模型为每个目标类别生成带有随机化形状描述的文本提示，并通过自我验证机制确保描述的真实性与合理性。这一阶段为后续图像生成提供了丰富的几何多样性种子。

2. **图像生成与深度估计（Image Generation and Depth Estimation）**：使用扩散模型根据几何提示生成初始RGB图像，随后通过深度估计模型（DepthFM）提取对应的深度图。这些深度图作为后续纹理变体生成的空间条件信号。

3. **纹理变体生成（Texture Variation）**：以深度图作为ControlNet条件，结合LLM生成的纹理提示，为每张深度图生成10个纹理变体。这一设计实现了**姿态一致性与纹理多样性的解耦**：深度条件锁定物体的全局结构与空间姿态，而纹理提示则驱动外观的丰富变化。

4. **3D重建（3D Reconstruction）**：采用Hunyuan3D-v2.0将条件生成的RGB图像重建为纹理化的3D网格。该模型在大规模生成中展现出稳定的输出质量和较强的可靠性，几乎无需人工过滤——这与先前方法（如**GenVegeFruits3D**（Duret et al., HAL 2025）需过滤超过15倍的生成网格）形成鲜明对比。

### 核心控制机制：深度条件

流水线的关键创新在于**深度条件控制**。消融实验（Table 3）揭示：纯文本提示（text-only）生成方式在NOCS类别上的平均姿态一致性仅为57%，对于相机、笔记本电脑等复杂非对称物体甚至低至20%；而引入深度条件后，平均姿态一致性跃升至97%，在153个Omni6Dpose类别上达到96%的网格姿态一致性。

这一显著提升的根本原因在于：深度图能够捕获物体的全局结构与空间定位信息，同时不过度约束局部几何变化或纹理细节。这使得从单张条件生成图像重建的3D网格天然具备一致的规范朝向，无需任何后处理对齐步骤。

### 数据生成效率

从效率维度看，该流水线在每个物体不到3分钟的时间内即可生成高质量、对齐的3D网格，相比传统扫描方式加速5–20倍。以100张深度图作为输入，流水线可全自动生成每类别1000个对齐网格，为下游的6D姿态估计与机器人抓取任务提供了前所未有的数据规模与质量保障。

### 补充图表

![[assets/figures/papers/paper_list_l2202_https_openaccess_thecvf_com_content_CVPR2026_html_Guillaume_Breaking_the/figures/001_Figure_1.jpg]]
*Figure 1: Our text-to-image pipeline: (a) Category-based geometry prompt engineering and images generation; (b) Depth-conditioned image generation for texture variation and automatic alignment*

## 核心模块与公式推导

GenOmni3D流水线由四个顺序模块构成，其核心设计目标是：在保证生成网格规范对齐的前提下，最大化几何与纹理的类别内多样性。整个流水线可在单张消费级GPU上运行，每个物体生成时间少于3分钟。

### 模块一：基于LLM的几何提示工程

该模块负责为每个目标类别生成多样化的几何形状描述。具体流程为：

1. **类别级提示生成**：给定目标类别名称（如“mug”），大语言模型生成一组带有随机化形状描述的文本提示。例如，对于“mug”类别，模型可能生成“a tall cylindrical mug with a wide handle”或“a short tapered mug with a small ear-shaped handle”等变体。
2. **自我验证机制**：LLM对生成的提示进行自我验证，确保描述在物理上合理且符合该类别物体的真实形态分布。不合理的描述（如“a mug with two opposing handles”）会被自动筛除。
3. **规模化输出**：每个类别最终保留约100个通过验证的几何提示，作为后续图像生成阶段的条件输入。

该模块的因果作用在于：通过LLM的结构化探索能力，系统性地覆盖类别内几何形态空间，避免人工设计提示的覆盖盲区。

### 模块二：图像生成与深度估计

该模块将几何提示转化为可视化的深度图，是整个流水线实现规范对齐的关键环节。

1. **初始图像生成**：使用Stable Diffusion等扩散模型，根据几何提示生成物体的RGB图像。此时生成的图像在姿态上具有随机性。
2. **深度图提取**：使用预训练的DepthFM模型从生成的RGB图像中估计深度图。深度图天然编码了物体的三维表面几何和空间朝向信息。
3. **深度图筛选**：对提取的深度图进行质量筛选，剔除深度估计失效或物体结构严重残缺的样本。每个类别最终保留约100张高质量深度图。

深度图在此扮演**几何代理**的角色——它既保留了物体的全局结构信息，又剥离了纹理细节，为后续的纹理变体生成提供了姿态锚点。

### 模块三：纹理变体生成（深度条件控制）

这是流水线中最具创新性的模块，直接解决了“生成多样性”与“规范对齐”之间的矛盾。

**技术方案**：采用ControlNet架构，以模块二产出的深度图作为空间条件信号，引导扩散模型生成纹理化图像。具体而言：

- **控制信号**：深度图通过ControlNet的编码分支注入UNet的中间层特征，约束生成图像的物体轮廓和空间姿态与深度图保持一致。
- **纹理提示**：LLM额外生成纹理相关的文本提示（如“a ceramic mug with blue glaze”、“a matte black mug with speckled texture”），每张深度图搭配10个不同的纹理提示，生成10个纹理变体。
- **因果机制**：深度条件显式锁定了物体的全局朝向和三维结构，而纹理提示在局部纹理空间内引入变化。这种“全局约束-局部自由”的设计，使得同一深度图衍生的所有纹理变体共享一致的规范姿态，同时呈现丰富的视觉多样性。

**消融实验的关键证据**（Table 3）：仅使用文本提示（text-only）生成时，NOCS各类别的平均姿态一致性仅为57%，其中非对称物体（如laptop、camera）的姿态一致性低至20%。引入深度条件后，平均姿态一致性跃升至97%，在153个Omni6Dpose类别上达到96%的网格姿态一致性。这一跃升幅度（+40个百分点）直接验证了深度条件作为因果操控变量的决定性作用。

### 模块四：3D重建

该模块将模块三产出的纹理化图像转化为带纹理的3D网格。

**重建模型选择**：经过对比评估（Table 4），Hunyuan3D-v2.0在输出质量和可靠性上显著优于其他方案（如InstantMesh、Zero123++等）。其关键优势在于：

- **质量稳定性**：在大规模生成中几乎不需要人工过滤，而此前方法（如GenVegeFruits3D）需要筛除超过15倍的生成网格。
- **效率**：单次重建时间在可接受范围内，整体流水线控制在每物体3分钟以内。

**对齐保持**：由于输入图像已通过深度条件锁定了规范朝向，Hunyuan3D-v2.0重建的网格天然继承了这一对齐属性，无需后处理步骤。

### 公式推导

本文未提出新的理论公式。流水线的核心数学基础来自所引用的现有工作：

- **扩散模型**：模块二和三的生成过程基于标准扩散模型的去噪框架，其训练目标为噪声预测损失 $\mathcal{L} = \mathbb{E}_{x_0, \epsilon, t}\left[\|\epsilon - \epsilon_\theta(x_t, t, c)\|^2\right]$，其中条件 $c$ 在模块三中为深度图信号。
- **ControlNet**：模块三的空间控制通过ControlNet的可训练副本网络实现，其输出特征与原始UNet的对应层相加，形式为 $\mathbf{f}_\text{out} = \mathbf{f}_\text{UNet} + \mathcal{Z}(\mathbf{f}_\text{UNet}; \mathbf{d})$，其中 $\mathbf{d}$ 为深度条件。
- **3D重建**：模块四使用Hunyuan3D-v2.0的多视图重建管线，其核心为基于Transformer的稀疏视图到3D的映射，具体公式参见原论文。

若需深入理解上述组件的数学细节，建议直接查阅Stable Diffusion、ControlNet（Zhang et al., ICCV 2023）及Hunyuan3D-v2.0的原始论文。

### 补充图表

![[assets/figures/papers/paper_list_l2202_https_openaccess_thecvf_com_content_CVPR2026_html_Guillaume_Breaking_the/figures/004_Figure_3.jpg]]
*Figure 3: Qualitative examples of final textured images of the 6 categories in the NOCS dataset (on the left) and final resulting 3D textured meshes using Hunyuan3D-v2.0 model [26] (on the right)*

![[assets/figures/papers/paper_list_l2202_https_openaccess_thecvf_com_content_CVPR2026_html_Guillaume_Breaking_the/figures/006_Table.jpg]]

## 实验与分析

### 核心实验设定与公平性保障

所有6D姿态估计实验均采用相同的**DualPoseNet**网络架构与训练超参数，仅改变训练数据来源。抓取实验在统一的**SAPIEN**仿真环境中进行，使用相同的数据集划分与物体放置策略；基线方法均使用各自论文推荐的预训练模型。这一严格控制变量的设定，使得性能差异能够直接归因于训练数据的质量与多样性。

### 零样本Sim2Real 6D姿态估计

在**NOCS REAL275**真实场景测试集上的零样本迁移结果（Table 5）揭示了混合现实渲染策略的决定性作用。使用混合现实渲染且启用阴影模拟的训练数据（Mix_SAI with shadows）取得了**34.75**的平均6D姿态精度，显著优于纯合成Replica渲染的**33.10**。消融实验进一步表明，阴影模拟是零样本sim2real迁移的关键因素：禁用阴影后，真实场景平均精度从34.75下降至30.83。这一发现说明，混合现实渲染中的光照一致性（尤其是阴影线索）为模型提供了跨越合成-真实域间隔的关键桥接信号。

![[assets/figures/papers/paper_list_l2202_https_openaccess_thecvf_com_content_CVPR2026_html_Guillaume_Breaking_the/figures/013_Table_5.jpg]]
*Table 5: Comprehensive evaluation of DualPoseNet for Sim2Real transfer and in-domain performance. The top section reports zero-shot transfer to the real-world NOCS REAL275 test set. The middle section shows performance on synthetic validation splits. The bottom section provides the original NOCS supervised upper-bounds for reference. Metrics evaluate both 2D detection (IoU50/75) and 3D pose accuracy, where*

在合成域内验证集上，使用**GenNOCS**生成网格训练的平均6D姿态精度达到**23.91**，相较原始NOCS合成网格的**15.66**提升了**+8.25**。这一大幅提升验证了生成网格在几何质量与多样性上对原始合成资产的显著超越。

### 抓取与形状补全评估

在自定义SAPIEN抓取仿真中（Table 6），基于GenOmni3D网格训练的**Custom-CG**模型取得了**87.8%**的抓取成功率，大幅超越**CenterGrasp**（82.7%）和**GIGA**（63.8%）。形状补全指标同样呈现一致趋势：Custom-CG的IoU达到**0.475**，相较CenterGrasp的0.314提升超过51%。值得注意的是，当训练使用原生纹理而评估使用随机纹理时（Custom-CG-tex-val-rdom），性能仍然保持竞争力，表明模型学到的几何先验对纹理变化具有较强的鲁棒性。

### 深度条件消融：姿态一致性的因果证据

Table 3的消融实验直接验证了深度条件作为因果调节变量的核心作用。在仅使用文本提示的生成模式下，NOCS类别的平均姿态一致性仅为**57%**，其中复杂非对称物体（如相机、笔记本电脑）的姿态一致性甚至低至**20%**——这些物体几乎无法保持规范朝向。引入深度图作为ControlNet条件后，NOCS类别的平均姿态一致性跃升至**97%**，并在153个Omni6Dpose类别上达到**96%**的网格姿态一致性。这一接近饱和的提升幅度表明，深度条件在保留局部几何与纹理多样性的同时，有效锁定了物体的全局结构与空间朝向，从根本上解决了生成式3D资产的对齐难题。

### 3D重建方法对比与网格过滤效率

Table 4对比了多种3D网格生成方法。**Hunyuan3D-v2.0**在输出质量与可靠性上表现最优，在大规模生成中几乎无需人工过滤——这与先前工作形成鲜明对比：**GenVegeFruits3D**（Duret et al., HAL 2025）需要过滤超过15倍的生成网格才能获得可用资产。其他重建方法（如InstantMesh）虽然速度更快，但质量不稳定，难以支撑规模化数据生产。这一发现确立了Hunyuan3D-v2.0作为本流水线后端重建模块的最优选择。

### 真实机器人抓取验证

在真实机器人实验中（Table 7, Figure 10），基于GenOmni3D数据训练的模型在多种类别物体上展现了可靠的检测与抓取能力。各类别的检测与抓取成功率详见表7，可视化结果（Figure 10）展示了从RGB-D感知到抓取预测与热力图置信度的完整流程，验证了生成数据训练的模型在真实场景中的实用部署能力。

![[assets/figures/papers/paper_list_l2202_https_openaccess_thecvf_com_content_CVPR2026_html_Guillaume_Breaking_the/figures/016_Table_7.jpg]]
*Table 7: Detection and Grasping Success Rate Across Categories*

![[assets/figures/papers/paper_list_l2202_https_openaccess_thecvf_com_content_CVPR2026_html_Guillaume_Breaking_the/figures/015_Figure_10.jpg]]
*Figure 10: Robotic perception and grasping visualizations on can object of Centergrasp trained on our custom ”Can” dataset. Top: All 6 category objects used in real-world setup. Bottom (2×2 grid): top row—RGB image of a scene of cans and associated depth; bottom row—shape-based grasp prediction and heatmap indicating grasp confidence*

### 补充图表

![[assets/figures/papers/paper_list_l2202_https_openaccess_thecvf_com_content_CVPR2026_html_Guillaume_Breaking_the/figures/003_Table_1.jpg]]
*Table 1: Comparison of existing 3D mesh datasets, highlighting their number of instances by categories. R/S/SAI indicates whether the dataset consists of real-world scanned objects (R), synthetic assets created by artists (S), or assets from generative 3D models (SAI)*

![[assets/figures/papers/paper_list_l2202_https_openaccess_thecvf_com_content_CVPR2026_html_Guillaume_Breaking_the/figures/005_Table_2.jpg]]
*Table 2: Comparison of existing category-level 6D pose estimation methods, including quantitative metrics of 3D data usage. Rast: rasterization; RT: ray tracing; R: real data; MR: Mixed-reality*

![[assets/figures/papers/paper_list_l2202_https_openaccess_thecvf_com_content_CVPR2026_html_Guillaume_Breaking_the/figures/007_Table_4.jpg]]
*Table 4: Comparison of state-of-the-art 3D mesh generation methods. We have evaluated four approaches based on output quality (Qlty), generation time (Time), and visual results (Mesh)*

![[assets/figures/papers/paper_list_l2202_https_openaccess_thecvf_com_content_CVPR2026_html_Guillaume_Breaking_the/figures/008_Figure_4.jpg]]
*Figure 4: Images with random textures*

![[assets/figures/papers/paper_list_l2202_https_openaccess_thecvf_com_content_CVPR2026_html_Guillaume_Breaking_the/figures/010_Figure_5.jpg]]
*Figure 5: Images with object textures*

![[assets/figures/papers/paper_list_l2202_https_openaccess_thecvf_com_content_CVPR2026_html_Guillaume_Breaking_the/figures/012_Figure_9.jpg]]
*Figure 9: Real images of REAL275 [27]*

## 方法谱系与知识库定位

### 生成式3D数据：从扫描到合成的范式转移

类别级6D姿态估计长期依赖手工建模或实物扫描获取3D资产。**NOCS**（Wang et al., CVPR 2019）奠定了类别级姿态估计的基准，但其合成数据集仅覆盖6个类别、每类数十个实例，且网格质量参差不齐——这正是本文在表5中所揭示的：原始NOCS合成网格训练的姿态精度仅为15.66%，而替换为GenNOCS网格后提升至23.91%（+8.25）。**Omni6D**（Zhang et al., ECCV 2024）将覆盖范围扩展到153个类别，但依赖艺术家手工建模，扩展成本高昂。**GenVegeFruits3D**（Duret et al., HAL 2025）首次尝试用生成式模型产生产品级3D数据，却受限于仅处理对称物体，且需要过滤超过15倍生成网格以剔除不合格样本——这一瓶颈正是GenOmni3D通过Hunyuan3D-v2.0的高质量重建所消除的。

本文的核心突破在于将“规范对齐”这一关键约束从后处理阶段前移至生成条件中。传统方法（包括GenVegeFruits3D的text-only生成）产出的3D资产姿态随机，需大量人工对齐；GenOmni3D通过在文本到图像生成阶段注入深度图作为ControlNet条件，将NOCS类别的平均姿态一致性从57%提升至97%，并在153个Omni6Dpose类别上达到96%的网格姿态一致性（表3）。这一设计使得从100张深度图即可全自动生成1000个对齐网格，无需人工干预。

### 与下游任务的耦合深度

GenOmni3D并非孤立的数据生成工具，而是与6D姿态估计和机器人抓取形成闭环验证。在抓取任务上，使用GenOmni3D网格训练的Custom-CG模型达到87.8%的抓取成功率，显著超越**CenterGrasp**（Chisari et al., IEEE RA-L 2024）的82.7%和**GIGA**（Jiang et al., arXiv 2021）的63.8%（表6）。形状补全的IoU也从0.314提升至0.475。值得注意的是，混合现实渲染中的阴影模拟对零样本sim2real迁移至关重要——启用阴影将REAL275真实场景的平均精度从30.83提升至34.75（表5），这一发现直接继承了**Omni6DPose**（Zhang et al., ECCV 2024）的混合现实渲染思路并将其开源。

### 适用边界与局限

当前流水线的适用边界清晰：**适用于刚体、非铰接、具有明确规范朝向的物体类别**。深度条件控制依赖于物体存在可定义的规范坐标系——对于完全对称的球体或高度非对称但无共识朝向的物体（如自然石块），规范对齐的概念本身即模糊。此外，Hunyuan3D-v2.0虽然质量稳定，但单次重建仍需分钟级时间（表4），限制了实时或交互式应用场景。

论文未明确讨论的局限包括：生成的网格纹理是否在极端光照或传感器噪声下保持足够的视觉保真度以支撑鲁棒的特征匹配；深度条件是否对某些拓扑结构（如细长部件、薄壁结构）产生系统性偏差。这些问题在实验部分未被消融，需在实际部署中手动验证。

### 开放问题与未来方向

1. **铰接物体与复杂拓扑**：当前流水线能否推广到铰接物体（如剪刀、笔记本电脑开合状态）或具有复杂拓扑结构的类别？深度条件是否能编码部件间的相对运动约束？
2. **动态场景与视频域迁移**：该数据生成策略能否支撑动态场景下的6D姿态跟踪任务？生成数据的时间一致性尚未被探索。
3. **3D基础模型的训练数据**：GenOmni3D以每类1000个对齐网格的规模生成数据，这是否已足够训练真正的3D基础模型？规模化生成的数据质量与多样性是否存在边际效益递减？
4. **跨域鲁棒性**：生成的网格在不同光照条件、传感器噪声和遮挡程度下的鲁棒性需系统评估——当前仅在受控的SAPIEN仿真和有限的真实场景（REAL275）中验证。

### 知识库定位

GenOmni3D处于**生成式3D数据**与**类别级6D姿态估计**的交叉点。其上游依赖文本到图像扩散模型（ControlNet）和单视图3D重建模型（Hunyuan3D-v2.0），下游赋能6D姿态估计网络（DualPoseNet）和抓取策略（Custom-CG）。与纯合成渲染管线（Omni6D）和纯真实扫描管线（NOCS）不同，GenOmni3D开创了“深度条件生成→对齐3D重建→混合现实渲染”的第三条路径，以不到3分钟/物体的速度实现5–20倍的加速，同时保持与手工建模相当的网格质量和显著更优的姿态一致性。

## 原文 PDF

![[paperPDFs/CVPR_2026/Breaking_the_3D_Dataset_Bottleneck_Fast_Scalable_Generation_of_Aligned_3D_Assets_from_Scratch_for_Category_6D_Pose_Estimation_and_Robotic_Grasping.pdf]]