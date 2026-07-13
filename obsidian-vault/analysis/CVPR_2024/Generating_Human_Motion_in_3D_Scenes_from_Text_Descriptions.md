---
title: Generating Human Motion in 3D Scenes from Text Descriptions
type: paper
paper_level: A
venue: CVPR
year: 2024
pdf_ref: paperPDFs/CVPR_2024/Generating_Human_Motion_in_3D_Scenes_from_Text_Descriptions.pdf
code_link: null
project_link: https://zju3dv.github.io/text_scene_motion
aliases:
- LGTSGOCD
- GHM3SFTD
tags:
- CVPR_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 将复杂的多模态问题分解为目标物体的显式语言定位（利用大语言模型进行3D视觉基础）和以物体为中心的运动生成两个子问题，显著降低了学习难度并提高了生成质量。
primary_logic: 通过将3D场景转换为文本表示并利用ChatGPT的常识推理能力，可以精确识别与文本描述匹配的目标物体，然后围绕该物体构建轻量的体积传感器表示，指导扩散模型生成轨迹和局部姿态，使模型专注于相关场景部分，实现准确的交互和自然的运动。
claims:
- 我们的方法将问题分解为目标定位和以物体为中心的运动生成两个子问题。
- 我们利用ChatGPT进行语言基础的3D目标定位，通过将场景图转换为文本提示并采用两阶段提问实现。
- 对象中心表示使用体积传感器（环境传感器和目标传感器）代替原始场景点云，从而降低复杂度并提高运动质量。
- 定量实验（表1）表明，我们的方法在目标距离、场景评分、动作识别精度和FID上均优于基线HUMANISE及GMD变体。
---

# Generating Human Motion in 3D Scenes from Text Descriptions

> [!tip] 核心洞察
> 通过将3D场景转换为文本表示并利用ChatGPT的常识推理能力，可以精确识别与文本描述匹配的目标物体，然后围绕该物体构建轻量的体积传感器表示，指导扩散模型生成轨迹和局部姿态，使模型专注于相关场景部分，实现准确的交互和自然的运动。

| 字段 | 内容 |
|------|------|
| 中文题名 | 根据文本描述生成3D场景中的人体运动 |
| 英文题名 | Generating Human Motion in 3D Scenes from Text Descriptions |
| 会议/期刊 | CVPR 2024 |
| Links |  [Project](https://zju3dv.github.io/text_scene_motion)|
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | LLM-guided two-stage generation with object-centric diffusion |
| Dataset | HUMANISE test set, HUMANISE |

> [!tip] 效果简介
> - HUMANISE test set (predicted detection) 上，Target localization accuracy (%) 75.6 (ChatGPT) vs 72.4 (Mistral) (+3.2)。
> - HUMANISE 上，goal distance 0.384 vs 0.385 (w/o two-stage) (-0.001)；scene score, accuracy, FID, quality score outperforms baselines vs HUMANISE, GMD∗, GMDHC (superior)。

## 概要

**核心问题**：给定一段文本描述（如“一个人坐在沙发上”），在三维场景中生成与之匹配的、包含精确人-物交互的人体运动序列，是一个具有挑战性的多模态生成任务。现有方法（如 **HUMANISE**，Wang et al., NeurIPS 2022）对整个三维场景点云进行编码，并采用隐式的视觉定位来推断交互目标。然而，这种全局编码策略导致生成器难以聚焦于与动作真正相关的目标物体，使得运动交互的准确性和运动质量受限——这正是本工作所要解决的关键瓶颈。

**核心思路**：本文提出将这一复杂问题**分解为两个更易管理的子问题**：目标物体的显式语言定位（language grounding）与以物体为中心的运动生成（object-centric motion generation）。其核心洞察在于：利用大语言模型（ChatGPT）的常识推理能力，先将三维场景转化为文本表示，通过问答方式精确识别文本描述所指向的目标物体；随后，围绕该目标物体构建轻量的体积传感器表示，指导扩散模型分阶段生成人体轨迹和局部姿态，使模型能够专注于场景中与交互相关的部分。

**方法定位**：该方法在生成范式上属于**LLM引导的两阶段扩散生成**。与 HUMANISE 的单阶段 cVAE + 全局点云编码方案相比，本文在四个关键维度上做出了改变：

- **目标定位策略**：从隐式回归目标中心 → **显式的两阶段 ChatGPT 提示**，将语言基础问题转化为问答推理。
- **场景表示**：从全景点云编码 → **以目标物体为中心的体积传感器**（环境传感器与目标传感器），大幅降低表示复杂度。
- **生成架构**：从 cVAE → **条件扩散模型**，提升生成质量与多样性。
- **生成结构**：从单阶段联合生成 → **轨迹生成 + 运动补全的两阶段流水线**，使粗粒度规划与细粒度姿态生成各司其职。

**主要结果**：在 HUMANISE 数据集上的定量实验（Table 1）表明，该方法在目标距离、场景评分、动作识别精度和 FID 等指标上均优于 HUMANISE 及 GMD 变体基线。消融实验（Table 2）进一步验证了语言定位模块、物体中心表示、两阶段生成结构以及扩散模型选择各自对最终性能的贡献。此外，该方法在未做微调的情况下可泛化至 PROX 数据集（Figure 6），展现了一定的场景迁移能力。

**局限性**：当前方法假设场景为静态，无法处理动态物体或多人交互；文本描述限于模板化语言；目标定位依赖预训练三维检测器，检测错误会向下游传播。

生成逼真的人体运动是计算机视觉和图形学中的核心问题，其在虚拟现实、机器人仿真、游戏角色动画等领域具有广泛的应用前景。近年来，随着生成模型的快速发展，从文本描述生成人体运动取得了显著进展。然而，当任务从空旷空间拓展到包含复杂物体布局的3D场景时，生成与场景中特定物体进行精确交互的运动仍然是一个极具挑战性的问题。

这一挑战的根源在于多模态信息融合的复杂性。模型需要同时理解文本指令的语义意图、识别3D场景中与指令相关的目标物体，并生成能够精确接触或操作该物体的自然人体运动序列。现有的代表性方法如**HUMANISE**（Wang et al., NeurIPS 2022）尝试端到端地解决这一问题：它将整个3D场景的点云输入点云Transformer进行编码，通过隐式回归来定位交互目标，然后利用条件变分自编码器（cVAE）直接生成运动序列。

然而，这种端到端的隐式定位策略存在一个关键瓶颈：**生成器难以从整个场景的密集点云中聚焦于与动作真正相关的目标物体**。场景中大量无关的几何信息（如墙壁、地板、其他家具）淹没了与交互目标直接相关的局部特征，导致模型在定位精度和运动交互质量上均受到限制。具体表现为生成的肢体末端无法准确到达目标物体表面，或交互姿态缺乏物理合理性。

本文的核心动机在于：**将这一复杂的多模态生成问题分解为两个更可管理的子问题，以降低学习难度并提升生成质量**。这一思路的因果操纵点是：如果能够先显式地定位出文本所指的目标物体，那么后续的运动生成就可以围绕该物体展开，从而将注意力集中在场景的局部相关区域，而非处理整个场景的冗余信息。基于此，本文提出了一种LLM引导的两阶段生成框架，利用大语言模型的常识推理能力实现显式的3D视觉基础，并围绕定位到的目标物体构建轻量的物体中心场景表示，指导扩散模型生成轨迹和局部姿态。

## 核心方法与创新机理

本方法针对现有文本驱动场景感知运动生成方法（如 **HUMANISE**，Wang et al., NeurIPS 2022）的核心瓶颈——直接对整个3D场景点云编码并进行隐式视觉定位，导致生成器难以聚焦于与动作相关的目标物体——提出了系统性的解决方案。其关键创新在于将复杂的多模态生成问题**显式分解**为两个更易管理的子问题：目标物体的语言定位（language grounding）和以物体为中心的运动生成（object-centric motion generation）。

这一分解策略带来了以下四个核心 changed slots，构成了方法相对于基线的主要创新点：

### 1. 目标定位策略：从隐式回归到显式语言基础

**基线方法（HUMANISE）** 采用隐式回归目标物体中心的方式，直接从场景点云中学习定位，缺乏对物体语义和空间关系的显式推理。本方法引入了基于大语言模型（ChatGPT）的两阶段显式定位策略（Fig. 3, Sec. 4.1）：
- 将3D场景转换为场景图及其文本描述，利用ChatGPT的常识推理能力进行目标物体推断；
- 第一阶段提示ChatGPT识别目标物体和锚定物体的类别，第二阶段结合简化后的场景图和物体关系推断具体目标物体；
- 这一设计将定位问题转化为问答任务，显著降低了对视觉特征学习的依赖，并提高了定位的可解释性和准确性。

### 2. 场景表示：从全景点云到以物体为中心的体积传感器

**基线方法（HUMANISE）** 使用Point Transformer对整个场景点云进行编码，信息密度高但缺乏对交互区域的聚焦。本方法提出以物体为中心的场景表示（Sec. 4.2, Fig. 4）：
- 围绕定位到的目标物体构建两类轻量体积传感器：**环境传感器（Environment Sensor）** 提供目标周围4m×4m×4m范围的粗糙空间信息，**目标传感器（Target Sensor）** 提供目标物体本身的精细几何信息；
- 这一表示大幅降低了输入复杂度，使生成模型能够专注于与交互直接相关的场景部分，从而提升运动交互的准确性和自然度。

### 3. 生成模型架构：从cVAE到条件扩散模型

**基线方法（HUMANISE）** 基于cVAE和Transformer VAE架构进行运动生成。本方法全面转向条件扩散模型（Sec. 4.2, 4.3）：
- 轨迹生成和运动补全均采用扩散模型，训练目标为条件去噪损失（Eq. (2)）；
- 扩散模型的迭代去噪特性有助于生成更自然、多样化的运动序列，消融实验（Table 2, “w/o diffusion”）证实替换为cVAE会导致生成质量下降。

### 4. 生成结构：从单阶段联合生成到两阶段级联生成

**基线方法（HUMANISE）** 采用单阶段联合生成人体轨迹和局部姿态。本方法将生成过程解耦为两阶段（Fig. 2）：
- **第一阶段**：给定以物体为中心的场景表示和文本条件，生成粗略的人体轨迹（trajectory generation）；
- **第二阶段**：基于生成的轨迹、场景表示和文本条件，补全详细的局部姿态（motion completion）；
- 两阶段设计使模型能够先规划全局运动路径，再细化局部交互细节，消融实验（Table 2, “w/o two-stage”）表明单阶段生成会导致运动立即坍缩至目标物体，缺乏自然过渡。

### 创新总结

上述四个 changed slots 围绕“分解复杂问题、聚焦交互核心”这一核心洞察展开：通过将3D场景转换为文本表示并利用LLM进行显式语言定位，再围绕定位结果构建轻量体积传感器表示，最后以两阶段扩散模型生成轨迹和运动，本方法系统性地解决了基线方法中“场景信息过载导致交互不准”的瓶颈问题。

本文提出了一种基于大语言模型引导的两阶段生成框架，将“根据文本描述在3D场景中生成人体运动”这一复杂多模态问题，显式分解为**目标物体的语言定位**与**以物体为中心的运动生成**两个子问题。这一分解策略的核心动机在于：现有方法（如HUMANISE）直接对整个场景点云进行隐式编码与定位，导致生成器难以聚焦于与动作语义真正相关的目标物体，从而限制了交互精度与运动质量。

整体流程如Figure 2所示，包含以下串联模块：

1.  **场景图构建与文本化描述**：将输入的3D场景转换为结构化的场景图，并生成对应的文本描述，作为后续大语言模型推理的基础。
2.  **基于ChatGPT的目标物体定位**：采用两阶段提示策略，引导ChatGPT从文本描述与场景图中，识别出与输入文本指令匹配的目标物体，实现显式的语言基础定位。
3.  **以物体为中心的场景表示**：围绕已定位的目标物体，构建轻量级的体积传感器表示（环境传感器与目标传感器），替代原始的全景点云，大幅降低场景表示的复杂度。
4.  **两阶段运动生成**：
    *   **第一阶段：轨迹生成**。以文本特征、环境传感器和目标传感器为条件，利用条件扩散模型生成粗略的人体运动轨迹。
    *   **第二阶段：运动补全**。在已生成轨迹的基础上，进一步结合文本特征、环境传感器、目标传感器以及逐帧的轨迹传感器，通过第二个条件扩散模型生成精细的局部姿态序列。
5.  **运动重建**：将扩散模型输出的运动参数转换为最终的SMPL-X人体网格序列。

该框架的关键优势在于**问题分解带来的专注性**：ChatGPT的常识推理能力使得目标物体定位更精确，而后续的物体中心表示与两阶段生成则让模型能够完全聚焦于相关的场景局部，从而在降低学习难度的同时，显著提升了人-物交互的准确性和运动生成的整体质量。

![[assets/figures/papers/paper_list_l1713_Generating_Human_Motion_in_3D_Scenes_from_Text_Descriptions/figures/002_Figure_2.jpg]]
*Figure 2: Overview of our two-stage pipeline. In the first stage, given an input scene and a text description (a), we use ChatGPT to locate the target object (b). In the second stage, human motions are synthesized by first producing human trajectories (c) and then generating local poses (d)*

本方法的核心架构由三个关键模块串联而成：基于大语言模型的目标物体显式定位、以物体为中心的体积传感器场景表示，以及两阶段条件扩散生成模型。以下逐一剖析其设计机理与数学基础。

### 3.1 基于ChatGPT的目标物体显式定位

现有方法（如**HUMANISE**，Wang et al., NeurIPS 2022）直接对整个3D场景点云进行编码，并通过隐式回归预测目标物体中心。这种端到端的黑箱定位方式使生成器难以聚焦于与动作语义真正相关的物体，成为交互准确性的瓶颈。

本方法将定位问题转化为一个基于常识推理的问答任务，利用大语言模型（ChatGPT）的世界知识来桥接文本描述与3D场景之间的语义鸿沟。具体实现采用两阶段提示策略（见图3）：

- **第一阶段：目标类别与锚点物体识别。** 将输入文本描述与场景中所有已检测物体的包围盒信息（类别、中心坐标、尺寸）构造为文本提示，要求ChatGPT推断出目标物体的类别以及可作为空间参照的锚点物体类别。基于此响应，原始场景图被简化为仅包含相关物体的子图。
- **第二阶段：目标物体推理。** 将第一阶段的结果（目标类别、锚点类别）与从简化场景图中提取的物体间空间关系（如“在...上方”、“靠近...”）组合为第二个提示，要求ChatGPT推理出具体的目标物体包围盒。

这种显式定位策略的核心优势在于将视觉定位的复杂感知问题转化为LLM擅长的语义推理问题，避免了从高维点云中直接回归坐标的困难。消融实验表明，移除定位模块（`w/o localization`）会显著降低交互精度（Table 2）。

### 3.2 以物体为中心的体积传感器表示

一旦目标物体被精确定位，场景表示便可从全局点云压缩为围绕该物体的轻量体积传感器，从根本上降低条件空间的复杂度。本方法设计了三种互补的体积传感器（见图4）：

**环境传感器（Environment Sensor）** 以目标物体中心 $c_o = (c_x, c_y, c_z)$ 为中心，覆盖 $4 \times 4 \times 4 \text{ m}^3$ 的立方体空间，划分为 $8 \times 8 \times 8$ 个体素。每个体素存储三个通道的信息：占用率、体素中心坐标和法向量。占用率 $o_s$ 由体素到场景网格的有符号距离 $d_s$ 和体素边长 $a_s$ 定义：

$$o_s = \begin{cases} 
1 & \text{if } d_s < 0, \\
0 & \text{if } d_s > a_s, \\
1 - \frac{d_s}{a_s} & \text{otherwise}.
\end{cases}$$

环境传感器提供目标物体周围的粗粒度空间上下文，使模型理解可行动区域和障碍物分布。

**目标传感器（Target Sensor）** 紧密包围目标物体，提供其精细几何信息。该传感器的体素分辨率与环境传感器相同，但覆盖范围仅为目标物体包围盒的尺寸，因此能捕捉物体的精确形状和表面细节，对生成准确的接触交互至关重要。

**轨迹传感器（Trajectory Sensor）** 在运动生成阶段动态构建，以人体当前帧位置为中心，提供人体周围的局部环境信息。其结构与目标传感器类似，但中心随人体移动而变化。

这种以物体为中心的表示方法将输入维度从整个场景点云（通常包含数万点）压缩为数百个体素的特征，同时保留了与交互直接相关的几何信息。消融实验证实，移除该表示（`w/o object-centric`）并在场景坐标系中直接预测运动会导致性能下降（Table 2）。

### 3.3 两阶段条件扩散生成模型

生成过程被分解为轨迹生成和运动补全两个阶段，均采用条件扩散模型实现。扩散模型的正向过程按照标准定义逐步向数据添加高斯噪声：

$$q(\mathbf{x}_t \mid \mathbf{x}_0) = \mathcal{N}(\mathbf{x}_t; \sqrt{\bar{\alpha}_t} \mathbf{x}_0, (1 - \bar{\alpha}_t) \mathbf{I})$$

其中 $\mathbf{x}_0$ 为原始数据（轨迹或运动序列），$\bar{\alpha}_t$ 为累积噪声调度参数。逆向过程通过一个条件生成器 $G$ 从噪声 $\mathbf{x}_t$ 预测原始数据 $\mathbf{x}_0$，训练损失为：

$$\mathcal{L} = \mathbb{E}_{t \in [1,T], \mathbf{x}_0 \sim q(\mathbf{x}_0)} \left[ \left\| \mathbf{x}_0 - G(\mathbf{x}_t, t, \mathbf{C}) \right\| \right]$$

其中 $\mathbf{C}$ 为条件信号，$T$ 为扩散总步数。

**第一阶段：轨迹生成。** 轨迹扩散模型的条件 $\mathbf{C}_t$ 由三部分组成：

$$\mathbf{C}_t = \{L, E, T\}$$

其中 $L$ 为文本描述的CLIP特征，$E$ 为环境传感器编码，$T$ 为目标传感器编码。模型从纯噪声出发，在条件引导下逐步去噪，生成人体在场景中的粗粒度运动轨迹（根节点位置序列）。

**第二阶段：运动补全。** 运动扩散模型的条件 $\mathbf{C}_m$ 在轨迹条件基础上增加了逐帧的轨迹传感器信息：

$$\mathbf{C}_m = \{L, E, T, O_1, ..., O_N\}$$

其中 $O_i$ 为第 $i$ 帧的轨迹传感器，$N$ 为序列总帧数。模型以第一阶段生成的轨迹为骨架，在局部坐标系中补全每帧的精细姿态参数（关节旋转），最终通过SMPL-X模型重建完整的人体网格序列。

两阶段分解的关键优势在于降低了单次生成的复杂度：轨迹生成只需关注宏观的空间规划，运动补全则专注于局部的姿态自然性。消融实验表明，将轨迹和运动合并为单阶段生成（`w/o two-stage`）会导致运动质量下降，人体倾向于“瞬间坍缩”到目标位置而非产生自然的趋近过程（Table 2）。此外，将扩散模型替换为cVAE（`w/o diffusion`）也会降低生成质量，验证了扩散模型在该任务中的优势。

![[assets/figures/papers/paper_list_l1713_Generating_Human_Motion_in_3D_Scenes_from_Text_Descriptions/figures/003_Figure_3.jpg]]
*Figure 3: Pipeline of localizing the target object. In stage 1, given the input text description and detected object bounding boxes (bbx), we construct the first prompt asking ChatGPT the categories of target objects and anchor objects. Based on the response, the scene graph can be simplified. In stage 2, we construct the second prompt with inputs and results from stage 1, including object relations derived from the simplified scene graph. The second prompt is designed for asking ChatGPT to infer the target object. Finally, we can get the target object bounding box from the response of ChatGPT*

![[assets/figures/papers/paper_list_l1713_Generating_Human_Motion_in_3D_Scenes_from_Text_Descriptions/figures/005_Figure_4.jpg]]
*Figure 4: The visualization of the environment sensor, target sensor, and trajectory sensor. The target sensor (b) gives detailed geometry of the target object. The environment sensor (c) gives coarse spatial information around the target object. The trajectory sensor (d) is located around the human*

## 实验与关键发现

### 5.1 实验设置

本文在HUMANISE数据集上进行训练和测试。运动生成模型先在AMASS上预训练200个epoch，再在HUMANISE上微调200个epoch。训练使用AdamW优化器，学习率0.0001，批大小128，在单张RTX 3090上完成。评估指标包括目标距离（goal distance）、场景评分（scene score）、动作识别精度（accuracy）、FID、质量评分（quality score）、多样性（diversity）和多模态性（multimodality），其中场景评分和质量评分通过感知研究获得。

### 5.2 主要结果

表1展示了在HUMANISE数据集上的定量对比。本文方法与**HUMANISE**（Wang et al., NeurIPS 2022）及GMD∗、GMDHC等基线进行对比。GMDHC使用HUMANISE预测的目标中心来引导GMD∗的运动生成。

**表1 核心结论**

| 指标 | 本文方法 | HUMANISE | GMD∗ | GMDHC | 真实数据 |
|------|----------|----------|------|-------|----------|
| goal distance ↓ | **0.384** | 0.385 | — | — | — |
| scene score ↑ | **最优** | 次优 | — | — | — |
| accuracy ↑ | **最优** | — | — | — | — |
| FID ↓ | **最优** | — | — | — | — |
| quality score ↑ | **最优** | — | — | — | — |
| diversity | 4.78 | — | — | — | — |

本文方法在目标距离、场景评分、动作识别精度和FID上均优于基线，同时在多样性和多模态性上取得有竞争力的结果。图5的定性对比显示，给定相同文本描述，本文方法生成的运动会与目标物体进行精确交互，与真实数据一致，而基线方法（HUMANISE、GMD∗、GMDHC）则无法实现准确的物体交互。

### 5.3 消融实验

表2系统消融了各核心组件的贡献：

- **w/o localization**：移除ChatGPT定位模块，直接使用场景点云生成轨迹和运动，交互精度显著下降。
- **w/o object-centric**：移除物体中心表示，在场景坐标系中预测运动，性能受损。
- **w/o two-stage**：将轨迹和运动合并为一阶段生成，导致运动真实感降低，人体会立即“坍缩”到目标物体位置。
- **w/o diffusion**：用cVAE替换扩散模型，生成质量下降。
- **w/o pretrain**：跳过AMASS预训练，结果明显退化。

表3进一步分析了目标定位模块的设计选择。ChatGPT在目标定位准确率上达到75.6%，优于Mistral的72.4%。值得注意的是，HUMANISE直接回归目标中心坐标，不依赖真实检测框，因此在预测检测条件下不计算准确率。

### 5.4 跨场景泛化

图6展示了本文方法在PROX数据集上的定性结果。模型无需在PROX上微调即可直接泛化到未见过的场景和物体类别，生成合理的人体运动序列。

### 5.5 失败模式与局限性

1. **静态场景假设**：方法假设场景物体保持静止，无法处理移动物体或动态环境变化。
2. **文本描述受限**：当前仅支持模板化语言输入，对复杂、自由形式的文本描述支持不足。
3. **运动时长限制**：生成的运动时长受训练数据约束，生成长序列运动仍具挑战。
4. **检测误差传播**：目标物体定位依赖预训练的3D检测器，检测错误会级联传播到后续运动生成阶段，导致交互失败。

![[assets/figures/papers/paper_list_l1713_Generating_Human_Motion_in_3D_Scenes_from_Text_Descriptions/figures/006_Table_1.jpg]]
*Table 1: Quantitative results on the HUMANISE dataset. We compare our method with four baselines (please refer to Sec. 5.2) and the real data. GMDHC means using HUMANISE’s predicted center to guide motion generation in GMD∗. Among the metrics, scene score and quality score are perceptual studies. ↑ means higher is better and ↓ means lower is better. → means closer to the real data is better. Bold indicates the best results. Underline indicates the second best*

![[assets/figures/papers/paper_list_l1713_Generating_Human_Motion_in_3D_Scenes_from_Text_Descriptions/figures/008_Table_2.jpg]]
*Table 2: Ablation of main components. We compare our method with five variants (please refer to Sec. 5.3). Among them, mm indicates multimodality. Bold indicates the best results. Underline indicates the second best*

![[assets/figures/papers/paper_list_l1713_Generating_Human_Motion_in_3D_Scenes_from_Text_Descriptions/figures/007_Figure_5.jpg]]
*Figure 5: Qualitative results. We compare our method with groundtruth and four baselines (please refer to Sec. 5.2) given the same text descriptions. Our method synthesizes motions that interact with the object precisely as the groundtruth data while the baselines fail*

## 定位与知识库关联

### 问题瓶颈与核心洞察

现有文本驱动的场景感知人体运动生成方法（以 **HUMANISE** (Wang et al., NeurIPS 2022) 为代表）面临一个关键瓶颈：它们直接对整个3D场景点云进行编码，并采用隐式回归方式定位交互目标。这种“全局编码+隐式定位”的策略使生成器难以聚焦于与动作描述真正相关的目标物体，导致交互精度不足和运动质量受限。

本文的核心洞察在于将复杂的多模态生成问题拆解为两个更可控的子问题：**目标物体的显式语言定位**与**以物体为中心的运动生成**。这一拆解的关键在于利用大语言模型（ChatGPT）的常识推理能力，将3D场景转换为文本表示后进行精确的目标基础（grounding），然后围绕定位到的目标构建轻量级体积传感器，使后续扩散模型能够专注于场景中与交互最相关的局部区域。

### 与基线方法的关系与差异

本文方法在问题设定上与 **HUMANISE** 直接可比，但在多个关键设计槽位上做出了根本性改变：

| 设计槽位 | HUMANISE (基线) | 本文方法 |
|:---|:---|:---|
| 目标定位策略 | 点云编码器隐式回归目标中心坐标 | ChatGPT两阶段提示实现显式文本基础 |
| 场景表示 | 完整点云经Point Transformer编码 | 以目标物体为中心的体积传感器（环境传感器+目标传感器） |
| 生成模型架构 | cVAE + Transformer VAE | 条件扩散模型（两阶段：轨迹生成+运动补全） |
| 生成结构 | 单阶段联合生成 | 两阶段级联：先轨迹后局部姿态 |

实验还引入了两个额外基线进行消融对比：**GMD\***（去除了场景感知能力的运动生成变体）和 **GMDHC**（使用HUMANISE预测的目标中心来引导GMD\*的运动生成）。定量结果表明（Table 1），本文方法在目标距离（goal distance）、场景评分（scene score）、动作识别精度（accuracy）和FID上均优于所有基线。

### 方法适用边界

1. **静态场景假设**：方法假定3D场景是静态的，无法处理包含移动物体或动态环境变化的场景。
2. **模板化文本输入**：文本描述限于HUMANISE数据集中的模板化语言，对复杂、自由形式的自然语言描述支持不足。
3. **运动时长限制**：生成的动作时长受限于训练数据分布，生成更长序列仍具挑战。
4. **检测器依赖**：目标物体定位依赖预训练的3D检测器，检测错误会传播至后续运动生成阶段，影响最终交互质量。

### 局限与开放问题

**已知局限：**
- 目标定位模块的精度受限于ChatGPT对场景文本描述的理解能力，在物体类别模糊或多候选目标场景中可能出现定位错误（Table 3中定位准确率为75.6%）。
- 体积传感器的空间分辨率（环境传感器4×4×4 m³，8×8×8体素）限制了精细几何信息的捕捉能力。
- 方法在HUMANISE数据集上训练和测试，尽管展示了向PROX数据集的零样本泛化能力（Figure 6），但跨场景泛化的鲁棒性尚未充分验证。

**开放问题：**
- 如何将方法拓展到动态物体交互和多人协作场景？
- 是否可以利用更大的LLM或多模态视觉-语言模型直接处理点云，取消文本中间表示，实现端到端的3D视觉基础？
- 能否将方法应用于户外场景或更大规模环境，突破当前室内场景的局限？
- 如何增强模型对自由形式、非模板化文本描述的理解和泛化能力？

## 原文 PDF

![[paperPDFs/CVPR_2024/Generating_Human_Motion_in_3D_Scenes_from_Text_Descriptions.pdf]]
