---
title: Let Your Image Move with Your Motion! -- Implicit Multi-Object Multi-Motion Transfer
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Let_Your_Image_Move_with_Your_Motion_Implicit_Multi_Object_Multi_Motion_Transfer.pdf
paper_link: https://openaccess.thecvf.com/content/CVPR2026/html/Li_Let_Your_Image_Move_with_Your_Motion_--_Implicit_Multi-Object_CVPR_2026_paper.html
project_link: https://ethan-li123.github.io/FlexiMMT_page/
code_link: null
aliases:
- LYIMYMIMOMMT
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/representation_self_supervised_transfer
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过物体特定掩码在注意力层中强制解耦动作与文本标记，实现精确的逐物体动作分配。
primary_logic: 利用扩散模型自注意力中的物体掩码，直接对文本、动作和视频标记的交互进行屏蔽，使得单一模型无需外部动作标注即可独立迁移多个物体的不同运动。
claims:
- MDMA 通过物体掩码将全局注意力解耦为逐物体交互，消除了跨物体运动泄漏。
- DMEM 和 RMPM 提供了从第一帧到后续帧的准确物体掩码，保证了多物体控制的稳定性。
- FlexiMMT 在轨迹保真度(TF)和光流保真度(FF)上显著优于所有基线，实现了 SOTA 性能。
- Custom evaluation set (200 video-image pairs) 上 Trajectory Fidelity (TF) ↑ = 0.577
---

# Let Your Image Move with Your Motion! -- Implicit Multi-Object Multi-Motion Transfer

> [!tip] 核心洞察
> 利用扩散模型自注意力中的物体掩码，直接对文本、动作和视频标记的交互进行屏蔽，使得单一模型无需外部动作标注即可独立迁移多个物体的不同运动。

| 字段 | 内容 |
|------|------|
| 中文题名 | 让你的图像随你的动作而动！——隐式多物体多动作迁移 |
| 英文题名 | Let Your Image Move with Your Motion! -- Implicit Multi-Object Multi-Motion Transfer |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Li_Let_Your_Image_Move_with_Your_Motion_--_Implicit_Multi-Object_CVPR_2026_paper.html) · [Project](https://ethan-li123.github.io/FlexiMMT_page/) |
| Topic | #topic/vision_multimodal_applications #topic/representation_self_supervised_transfer #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | FlexiMMT |
| Dataset | Custom evaluation set |

> [!tip] 效果简介
> - Custom evaluation set (200 video-image pairs) 上，Trajectory Fidelity (TF) ↑ 0.577 vs Best baseline (not specified) (N/A)；Flow Fidelity (FF) ↑ 0.723 vs Best baseline (not specified) (N/A)；Human Evaluation: Action Consistency (AC) % 76.750 vs Best baseline (not specified) (N/A)。

## 概要

**问题瓶颈**：现有隐式图像到视频（I2V）运动迁移方法在单图像多物体场景中存在**跨物体动作纠缠**——不同物体的运动信号在注意力层相互泄漏，导致无法独立控制每个物体的运动。

**核心思想**：FlexiMMT 通过**物体特定掩码**在扩散模型的自注意力中强制解耦动作与文本标记的交互，使得单一模型无需外部动作标注即可实现多物体、多动作的独立迁移。其关键机制是**运动解耦掩码注意力（MDMA）**，将全局注意力约束为逐物体的局部交互，从根本上消除跨物体运动泄漏。

**方法定位**：FlexiMMT 是首个隐式 I2V 多物体多动作迁移框架，以 CogVideoX-5B-I2V 为基础扩散模型，引入可训练的运动标记（motion tokens）和两级掩码提取机制——训练阶段通过 QK 乘法和硬阈值自动提取单物体掩码，推理阶段通过回归掩码传播机制（RMPM）将第一帧语义分割掩码动态传播至所有生成帧。

**主要结果**：在 200 个视频-图像对的评测集上，FlexiMMT 在轨迹保真度（TF=0.577）和光流保真度（FF=0.723）上显著优于所有基线方法，人工评测的动作一致性（76.75%）和运动保真度（89.48%）同样达到最优。消融实验证实，移除 M2X 掩码导致 TF 从 0.577 降至 0.381，移除 T2X 掩码使 TF 降至 0.461，验证了逐物体注意力解耦的决定性作用。

### 问题背景

视觉内容生成领域正经历从静态图像到动态视频的范式跃迁。在这一进程中，**动作迁移**（motion transfer）成为一个关键且极具挑战的子问题：给定一段包含特定动作的参考视频和一张目标图像，生成一段视频，使目标图像中的物体“继承”参考视频中的运动模式，同时保持物体外观和场景结构不变。这一能力在数字人驱动、影视特效、虚拟试穿、交互式内容创作等场景中具有广泛的应用前景。

根据动作表征方式的不同，现有动作迁移方法可分为两大范式：

- **显式动作迁移**：从参考视频中提取结构化中间表征（如骨架关键点、密集光流、3D网格、深度图），再将这些显式动作信号注入生成过程。这类方法（如基于DensePose或OpenPose的方案）虽然提供了可控的动作接口，但存在两个根本性局限：（1）中间表征的提取本身是有损的，难以完整保留参考视频中的细粒度运动细节（如衣物褶皱变化、非刚性形变）；（2）不同物体类型需要不同的显式表征，难以构建统一的动作迁移框架。
- **隐式动作迁移**：直接从参考视频的像素空间中学习运动模式，通过可学习的“动作标记”（motion tokens）将运动信息注入扩散模型的生成过程。这类方法（如**MotionClone**等）避免了显式中间表征的信息损失，能够更忠实地复现参考视频中的运动风格。然而，现有隐式方法均假设**单物体、单动作**场景——即参考视频和目标图像中均只包含一个主体物体。

### 核心瓶颈：跨物体动作纠缠

当场景从单物体扩展到多物体时，一个此前未被充分解决的核心瓶颈浮现：**跨物体动作纠缠**（cross-object motion entanglement）。

具体而言，在多物体场景中，不同物体需要执行不同的动作（例如：一只刺猬站立，同时一瓶啤酒鞠躬）。如果直接将多个参考视频的动作标记注入扩散模型，模型的自注意力机制会使不同物体的动作标记、文本标记和视频标记在全局范围内自由交互，导致：

1. **动作泄漏**（motion leakage）：物体A的动作标记错误地影响了物体B的视频区域，使得生成视频中物体B的动作混杂了物体A的运动特征。
2. **文本-动作错配**：描述物体A动作的文本标记可能关注到物体B的视频区域，进一步加剧动作分配的混乱。
3. **特征纠缠**：在隐空间中进行简单的QK乘法（query-key multiplication）提取物体掩码时，不同物体的特征高度纠缠，无法获得清晰的逐物体掩码（如Figure 3所示）。

这一瓶颈使得现有隐式动作迁移方法在多物体场景下完全失效——它们要么只能处理单物体，要么在多物体场景中产生严重的动作混淆。

### 方法缺口与本文动机

上述分析揭示了当前隐式动作迁移领域的两个关键缺口：

1. **缺少逐物体动作解耦机制**：现有方法依赖扩散模型的全注意力（full attention）机制，缺乏将动作信息精确分配到对应物体区域的约束手段。
2. **缺少推理时的物体掩码获取方案**：即使训练时能够获得物体掩码（通过外部标注或简单启发式方法），在推理阶段面对任意多物体图像时，如何稳定地获取每一帧的物体掩码仍是一个开放问题。

针对这些缺口，本文提出**FlexiMMT**——首个支持多物体、多动作的隐式图像到视频动作迁移框架。其核心动机在于：**通过物体特定的注意力掩码，在扩散模型的注意力层中强制执行逐物体的动作-文本-视频交互解耦，从而在不依赖外部动作标注的前提下，实现精确、灵活的多物体独立动作控制**。

## 核心方法与创新机理

FlexiMMT 的核心创新在于首次在隐式运动迁移框架中实现了**多物体、多动作的独立控制**，其关键突破是通过**物体特定掩码在注意力层中强制解耦动作与文本标记**，从而消除了跨物体运动泄漏这一根本瓶颈。以下从三个 changed slots 展开。

### 1. 运动解耦掩码注意力机制（MDMA）

标准扩散模型中的 3D 全注意力无法区分不同物体的运动，导致多物体场景中出现特征纠缠（Figure 3）。FlexiMMT 提出的 **MDMA** 通过构造物体特定的掩码矩阵 $\mathcal{M}$，直接对文本（Text）、运动（Motion）和视频（Video）标记之间的交互进行屏蔽，确保每个物体的运动标记和文本标记仅关注属于该物体的视频区域。

具体而言，MDMA 构建了两类核心子掩码：
- **Motion-to-Video 掩码**（$\mathcal{M}_{m,v}^k$）：仅当运动标记 $T_m[p]$ 和视频标记 $T_v[q]$ 属于同一物体 $k$ 时激活。
- **Text-to-Video 掩码**（$\mathcal{M}_{y,v}^k$）：仅当运动相关的文本标记 $T_y[p]$ 和视频标记 $T_v[q]$ 属于同一物体 $k$ 时激活。

这些子掩码被组合为完整的注意力掩码矩阵（Equation 11），在训练阶段仅激活 M2M、M2V 和 T2M 部分，推理阶段则激活全部子掩码以实现多物体解耦。**这一设计使得单一模型无需外部动作标注即可独立迁移多个物体的不同运动**，是 FlexiMMT 区别于所有隐式运动迁移基线的根本机制。

### 2. 区分式掩码提取与回归式掩码传播（DMEM & RMPM）

MDMA 的有效性依赖于准确的逐帧物体掩码。FlexiMMT 在训练和推理阶段分别采用不同策略获取掩码，构成了第二个关键创新：

- **训练阶段——区分式掩码提取机制（DMEM）**：由于训练视频仅包含单个物体，FlexiMMT 通过 QK 乘法和硬阈值从注意力激活中直接提取单物体掩码，无需外部标注。这一简单而有效的方法为模型学习运动传递提供了精确的物体定位信号。
- **推理阶段——回归式掩码传播机制（RMPM）**：面对多物体图像，FlexiMMT 首先使用外部语义分割模型（Grounded SAM）获取第一帧的初始掩码，随后通过计算当前帧特征与带掩码锚特征的归一化相关性 $\mathcal{C}_l^k$，将掩码逐步传播到所有生成帧。传播后的掩码通过均值阈值进行二值化，并通过局部时间窗口和早期停止准则（Dynamic RMPM）大幅加速推理。

DMEM 与 RMPM 的协同使得掩码在多帧生成过程中保持稳定，保证了多物体控制的时序一致性。

### 3. 可训练运动标记注入

FlexiMMT 在 CogVideoX-5B-I2V 的基础上引入了**可训练的运动标记**，将其插入文本和视频标记序列中。这些运动标记通过 2,000 步的 AdamW 优化（学习率 3e-3，batch size 1）从参考视频中学习运动模式，生成可注入的运动表示。与 MDMA 配合，运动标记被物体特定掩码约束，仅影响其对应物体的视频标记，从而实现了**从参考视频到目标图像的可组合运动迁移**。

### 创新总结

FlexiMMT 的三项 changed slots 形成了完整的因果链条：运动标记提供可迁移的运动表示，MDMA 通过物体特定掩码实现运动与文本的解耦，DMEM/RMPM 则保证了多帧掩码的准确性与稳定性。这一组合使得 FlexiMMT 成为首个能够在单张图像中独立控制多个物体不同运动的隐式 I2V 框架，在轨迹保真度（TF=0.577）和光流保真度（FF=0.723）上均达到 SOTA 性能。

FlexiMMT 的整体流程围绕一个核心矛盾展开：**如何在不依赖外部动作标注的条件下，将多个参考视频中的不同运动独立、精确地迁移到一幅图像中的多个物体上**。该框架将这一问题分解为三个相互协同的机制——运动标记学习、注意力解耦掩码和掩码提取与传播——形成一个从训练到推理的完整闭环。

### 训练阶段：单物体运动嵌入与掩码解耦

训练阶段的目标是让模型学会从单个参考视频中提取运动模式，并在注意力层面建立运动与物体的对应约束。如图 2(a) 所示，训练流程包含以下关键模块：

1. **运动标记注入**：在 CogVideoX-5B-I2V 的文本标记和视频标记序列中插入一组可训练的运动标记（motion tokens）。这些标记通过标准扩散噪声预测损失进行优化：
   $$\mathcal{L} = \mathbb{E}_{y,\mathbf{I}_0,\epsilon,t}\left[\|\epsilon_\theta(\mathbf{z}_t,y,t,\mathbf{I}_0)-\epsilon\|_2^2\right]$$
   运动标记通过与文本、视频标记的联合注意力交互来捕获参考视频中的运动模式：
   $$\mathcal{A} = \frac{[Q_c \oplus Q_m \oplus Q_v][K_c \oplus K_m \oplus K_v]^\top}{\sqrt{d}}$$

2. **差异化掩码提取机制**：由于训练时每个参考视频仅包含单个物体，FlexiMMT 采用一种简单的 QK 乘法方法从注意力激活中提取物体掩码。具体而言，通过计算 Query 和 Key 的相关性并施加硬阈值，即可获得该物体在潜空间中的二值掩码。然而，这一简单方法在存在多个物体时会因特征纠缠而失效——这正是推理阶段需要更复杂机制的原因。

3. **运动解耦掩码注意力**：在获得物体掩码后，MDMA 在注意力层中应用物体特定的掩码矩阵，确保运动标记和文本标记仅与属于同一物体的视频标记交互。训练时仅激活 M2M（运动到运动）、M2V（运动到视频）和 T2M（文本到运动）子掩码，其余注意力块保持不变。这一约束从根源上切断了跨物体的运动泄漏通道。

### 推理阶段：多物体掩码获取与动态传播

推理阶段的核心挑战在于：给定一幅包含多个物体的条件图像，如何为每个物体获取准确的时空掩码，以引导对应的运动标记。FlexiMMT 采用“外部初始化 + 内部传播”的策略：

1. **第一帧语义分割**：使用外部模型（如 Grounded SAM）对条件图像进行语义分割，获得每个物体的初始掩码。这是整个流程中唯一依赖外部模型的一步。

2. **回归式掩码传播机制**：将第一帧掩码作为锚点，逐步传播到后续所有生成帧。其核心操作是计算当前帧特征与带掩码的锚特征之间的相关性矩阵：
   $$\mathcal{C}_l^k = \operatorname{Norm}(\mathcal{F}_l) \cdot \operatorname{Norm}(\mathcal{F}_{\mathrm{anc}} \odot \widehat{\mathcal{M}}_{\mathrm{anc}}^k)^\top$$
   然后通过相似度传播和均值阈值生成当前帧的二值掩码：
   $$\mathcal{S}_l^k = \mathcal{M}_{\mathrm{anc}}^k \cdot \mathcal{C}_l^{k^\top}, \quad \widehat{\mathcal{M}}_l^k = \{1 \text{ if } S_l^k > \mathrm{mean}(S_l^k)\}$$
   锚点集合会随着去噪步的推进动态更新：每生成一帧，将其特征和掩码加入锚点集，并移除超出预设窗口大小的最旧帧。

3. **动态 RMPM 加速**：论文发现运动迁移在去噪早期阶段即可完成。基于这一观察，动态 RMPM 引入早期停止准则：当当前帧掩码与前一帧掩码的差异低于预设阈值 α 时，终止掩码更新，后续步骤直接复用最近的稳定掩码。这一策略在不牺牲性能的前提下显著减少了推理时间。

4. **掩码引导的注意力解耦**：获得各物体的时空掩码后，MDMA 在推理时激活完整的掩码矩阵：
   $$\mathcal{M} = \begin{bmatrix} \mathcal{M}_{y,y} & \mathcal{M}_{y,m} & \mathcal{M}_{y,v} \\ \mathcal{M}_{m,y} & \mathcal{M}_{m,m} & \mathcal{M}_{m,v} \\ \mathcal{M}_{v,y} & \mathcal{M}_{v,m} & \mathbf{I}_{d_v\times d_v} \end{bmatrix}$$
   其中每个子掩码精确控制文本、运动和视频标记之间的交互范围，实现“哪个物体执行哪种运动”的独立分配。

### 模块间的因果依赖

上述模块之间存在严格的因果链条：**运动标记提供可迁移的运动表征，MDMA 提供解耦的注意力空间，DMEM/RMPM 提供精确的物体时空定位**。消融实验验证了这一依赖关系——移除任一组件都会导致轨迹保真度（TF）和光流保真度（FF）的显著下降。例如，禁用推理阶段的掩码提取（w/o Infer）使 TF 从 0.577 骤降至 0.373，FF 从 0.723 降至 0.602，表明即使有正确的运动标记和解耦注意力，缺乏准确的物体掩码也会使多物体控制完全失效。

![[assets/figures/papers/paper_list_l7_https_openaccess_thecvf_com_content_CVPR2026_html_Li_Let_Your_Image_Move/figures/002_Figure_2.jpg]]
*Figure 2: Overview of FlexiMMT. (a) Training: Given one reference video, insert trainable motion tokens into text and video tokens. Get the object mask through a simple QK multiplication method, then mask out M2M, M2V and T2M parts in attention map. (b) Inference: Given a multi-object conditional image, we first segment each object’s mask with semantic segmentation model [35]. Concatenate pretrained motion tokens into text and video tokens for inference. Extract each object’s latent-space mask in subsequent frames via Dynamic Regressive Mask Propagation Mechanism (Dynamic RMPM), and apply it to Motion parts and Text parts in attention map*

### 3.1 运动标记注入与前向注意力

FlexiMMT 基于 CogVideoX-5B-I2V 图像到视频扩散模型构建，其训练目标为标准噪声预测损失：

$$ \mathcal{L} = \mathbb{E}_{y,\mathbf{I}_0,\epsilon,t}\left[\|\epsilon_\theta(\mathbf{z}_t,y,t,\mathbf{I}_0)-\epsilon\|_2^2\right] $$

其中 $y$ 为文本条件，$\mathbf{I}_0$ 为条件图像，$\mathbf{z}_t$ 为加噪后的视频潜变量。

为隐式编码参考视频中的运动模式，方法引入一组可训练的运动标记（motion tokens），将其分别插入文本标记序列和视频标记序列中。在注意力层，文本标记、运动标记和视频标记的 Query 与 Key 被拼接后计算注意力图：

$$ \mathcal{A} = \frac{[Q_c \oplus Q_m \oplus Q_v][K_c \oplus K_m \oplus K_v]^\top}{\sqrt{d}} $$

其中 $Q_c, Q_m, Q_v$ 分别表示文本、运动和视频标记的查询向量，$K_c, K_m, K_v$ 为对应的键向量，$d$ 为特征维度。这一拼接操作使得运动标记能够与文本和视频标记进行全局交互，但同时也引入了跨物体动作纠缠的风险——这正是后续 MDMA 模块所要解决的核心问题。

### 3.2 运动解耦掩码注意力机制

MDMA 的核心思想是通过物体特定掩码矩阵 $\mathcal{M}$，在注意力层中强制解耦不同物体间的动作与文本交互。对于第 $k$ 个物体，其运动标记到视频标记的掩码定义为：

$$ \mathcal{M}_{m,v}^k[p,q] = \begin{cases} 1, & \text{if } T_m[p]\in T_m^k \land T_v[q]\in T_v^k \\ 0, & \text{otherwise} \end{cases} $$

其中 $T_m^k$ 和 $T_v^k$ 分别表示属于第 $k$ 个物体的运动标记集合和视频标记集合。该掩码确保每个物体的运动标记仅关注属于同一物体的视频区域，从机制上阻断了跨物体的运动泄漏。

类似地，文本到视频掩码约束运动相关的文本标记与视频标记的交互：

$$ \mathcal{M}_{y,v}^k[p,q] = \begin{cases} 1, & \text{if } T_y[p]\in T_{y,mo}^k \land T_v[q]\in T_v^k \\ 0, & \text{otherwise} \end{cases} $$

其中 $T_{y,mo}^k$ 为与第 $k$ 个物体运动描述相关的文本标记子集。

将所有子掩码组合，得到完整的注意力掩码矩阵：

$$ \mathcal{M} = \begin{bmatrix} \mathcal{M}_{y,y} & \mathcal{M}_{y,m} & \mathcal{M}_{y,v} \\ \mathcal{M}_{m,y} & \mathcal{M}_{m,m} & \mathcal{M}_{m,v} \\ \mathcal{M}_{v,y} & \mathcal{M}_{v,m} & \mathbf{I}_{d_v\times d_v} \end{bmatrix} $$

其中视频自注意力块保持为单位矩阵 $\mathbf{I}$，不做掩码干预。训练阶段由于参考视频仅包含单个物体，仅激活 M2M、M2V 和 T2M 子掩码，其余块保持原始注意力值不变。推理阶段则根据多物体场景激活全部子掩码，实现逐物体独立控制。

### 3.3 掩码提取与传播机制

MDMA 的有效性依赖于准确的物体掩码。FlexiMMT 在训练和推理阶段采用不同的掩码获取策略。

**训练阶段——差异化掩码提取机制：** 由于训练视频仅含单一物体，可通过简单的 QK 乘法从注意力激活中提取掩码。具体而言，对运动标记与视频标记的注意力图进行硬阈值处理，获得该物体的二值空间掩码。然而，如图 Figure 3 所示，当视频包含多个物体时，特征纠缠导致这一简单方法失效——不同物体的特征在潜空间中高度耦合，无法通过单一阈值分离。这直接催生了推理阶段的 RMPM 设计。

**推理阶段——回归式掩码传播机制：** 推理时，首先使用外部语义分割模型（如 Grounded SAM）获取第一帧的多物体掩码。随后，RMPM 通过特征相关性将掩码从锚帧逐步传播到后续生成帧。对于第 $l$ 帧的第 $k$ 个物体，计算当前帧特征与带掩码锚特征之间的相关性矩阵：

$$ \mathcal{C}_l^k = \operatorname{Norm}(\mathcal{F}_l) \cdot \operatorname{Norm}(\mathcal{F}_{\mathrm{anc}} \odot \widehat{\mathcal{M}}_{\mathrm{anc}}^k)^\top $$

其中 $\mathcal{F}_l$ 为第 $l$ 帧的潜空间特征，$\mathcal{F}_{\mathrm{anc}}$ 为锚帧特征，$\widehat{\mathcal{M}}_{\mathrm{anc}}^k$ 为锚帧中第 $k$ 个物体的掩码，$\odot$ 表示逐元素乘法。随后通过相似度传播和均值阈值生成当前帧的二值掩码：

$$ \mathcal{S}_l^k = \mathcal{M}_{\mathrm{anc}}^k \cdot \mathcal{C}_l^{k^\top}, \quad \widehat{\mathcal{M}}_l^k = \{1 \text{ if } S_l^k > \mathrm{mean}(S_l^k)\} $$

RMPM 维护一个局部时间窗口内的锚帧集合，每完成一帧掩码提取后将其加入锚集，并移除最旧的锚帧。动态 RMPM 进一步引入早期停止准则：当连续帧间掩码差异低于预设阈值 $\alpha$ 时，终止掩码更新并复用最近的稳定掩码——这一设计源于 Figure 4 中的关键观察：动作迁移在去噪早期阶段即已完成，后续步骤的掩码变化极小。

![[assets/figures/papers/paper_list_l7_https_openaccess_thecvf_com_content_CVPR2026_html_Li_Let_Your_Image_Move/figures/004_Figure_4.jpg]]
*Figure 4: Illustration of the propagate feature and mask changes during denoising steps. We found that the transfer of motion can be completed in the early stage of denoising steps*

## 实验与关键发现

### 主结果

FlexiMMT 在 200 个视频-图像对的定制评估集上进行了系统验证。Table 1 报告了自动评估与人工评估的完整对比。在自动指标上，FlexiMMT 取得了最高的轨迹保真度（TF = 0.577）和光流保真度（FF = 0.723），表明生成视频中物体运动轨迹与参考运动高度一致，且帧间光流模式保真度最优。在人工评估的四个维度上，FlexiMMT 同样全面领先：动作一致性（AC）达 76.750%，文本一致性（TC）达 83.875%，文本相似度（TS）达 89.550%，运动保真度（MF）达 89.475%。这些结果表明，FlexiMMT 不仅在客观运动传递精度上实现 SOTA，在人类感知的语义一致性和运动自然度上也显著优于现有方法。

![[assets/figures/papers/paper_list_l7_https_openaccess_thecvf_com_content_CVPR2026_html_Li_Let_Your_Image_Move/figures/005_Table_1.jpg]]
*Table 1: Quantitative comparison. We compared the effectiveness of different methods with our method. There are five metrics for Automatic Evaluations and four for Human Evaluations, among which Human Evaluations score are in percentage*

定性对比（Figure 5）进一步印证了定量结论。在需要将不同参考视频中的运动独立迁移到同一图像中多个物体的场景下，基线方法普遍出现跨物体运动泄漏或语义混淆，而 FlexiMMT 能够为每个物体精确分配其对应的运动模式，生成的运动边界清晰、物体身份保持完整。

![[assets/figures/papers/paper_list_l7_https_openaccess_thecvf_com_content_CVPR2026_html_Li_Let_Your_Image_Move/figures/006_Figure_5.jpg]]
*Figure 5: Qualitative comparison. We compared the effects of different methods on transferring multi-object motions. The first row is the referenced motion, and the next six rows are the results of different methods*

### 消融实验

为验证各组件的独立贡献，论文进行了系统消融，核心发现如下。

**MDMA 中 M2X 与 T2X 掩码的作用（Table 2）**。移除所有 Motion-to-[X] 掩码（w/o M2X）后，TF 从 0.577 骤降至 0.381，FF 从 0.723 降至 0.618；移除所有 Text-to-[X] 掩码（w/o T2X）后，TF 降至 0.461，FF 降至 0.665。这一对比揭示了两条因果路径：M2X 掩码负责阻止动作标记向非目标物体的视频区域泄漏，是运动解耦的核心；T2X 掩码确保文本语义仅作用于对应物体区域，防止语义-运动绑定混乱。两者缺一不可，且 M2X 的性能影响更为剧烈。

**DMEM 与 RMPM 的贡献（Table 3）**。禁用训练阶段的掩码提取（w/o Train）使 TF 降至 0.440、FF 降至 0.656，说明训练时缺乏精确的物体定位会削弱模型学习有效运动传递的能力。禁用推理阶段的掩码提取（w/o Infer）导致更严重的性能退化（TF 0.373, FF 0.602），证实推理时的物体掩码对多物体控制不可或缺。移除 RMPM（w/o RMPM），即仅使用第一帧掩码而不进行传播，TF 降至 0.377、FF 降至 0.607，验证了逐帧掩码传播机制对于维持时序一致性的必要性。定性消融对比（Figure 6）直观展示了缺失各组件时的典型失败模式：运动漂移、物体混淆、边缘模糊等。

**动态 RMPM 的加速效果（Figure 7）**。动态 RMPM 通过早期停止策略，在不牺牲 TF/FF 性能的前提下显著减少推理时间。这一设计基于观察（Figure 4）：运动传递在去噪过程的早期阶段即可完成，后续步骤的掩码变化趋于稳定，因此可通过阈值 α 判断收敛并复用稳定掩码。

### 失败模式与局限性

尽管 FlexiMMT 在整体指标上表现优异，分析中仍可识别出若干边界条件和潜在失败模式：

1. **训练阶段的单物体限制**：训练时每个参考视频仅包含单个物体，模型未直接学习多物体共现的联合分布。当推理场景中物体间存在严重交互（如遮挡、接触）时，DMEM 提取的掩码可能出现边界模糊或归属错误，进而导致 MDMA 的注意力解耦失效。

2. **外部分割模型的依赖性**：推理阶段依赖 Grounded SAM 提供第一帧的语义分割掩码。若该模型在特定域（如非自然图像、极端光照）产生错误分割，误差将通过 RMPM 传播至后续所有帧，造成不可恢复的运动分配错误。

3. **动态 RMPM 的超参数敏感性**：阈值 α 和窗口大小 W 需要手动设定。α 过大可能导致掩码未收敛即停止更新，α 过小则加速效果有限。论文未提供这些超参数在不同场景下的调优策略或自适应机制。

4. **极端运动场景的鲁棒性未充分验证**：当参考运动包含大幅度的非刚体形变或快速旋转时，基于特征相关性的 RMPM 掩码传播是否仍能保持准确，目前缺乏定量证据支持。

![[assets/figures/papers/paper_list_l7_https_openaccess_thecvf_com_content_CVPR2026_html_Li_Let_Your_Image_Move/figures/009_Figure_6.jpg]]
*Figure 6: Qualitative comparison of each component in FlexiMMT. The caption for the generated videos is: “A beer bows head. A hedgehog stands up.”*

![[assets/figures/papers/paper_list_l7_https_openaccess_thecvf_com_content_CVPR2026_html_Li_Let_Your_Image_Move/figures/010_Figure_7.jpg]]
*Figure 7: Comparison of RMPM (w/o Dynamic) and Dynamic RMPM (w/ Dynamic). Dynamic RMPM substantially accelerates inference without compromising performance*

## 定位与知识库关联

### 问题定位：从单物体到多物体的隐式运动迁移

FlexiMMT 解决的核心瓶颈是**跨物体动作纠缠**——在单个图像中独立控制多个物体的运动时，现有方法难以将不同参考视频中的动作精确分配给各自对应的物体。此前的隐式运动迁移方法（如基于扩散模型的 I2V 框架）通常假设场景中只有一个运动主体，或者依赖外部运动标注（如光流、骨骼关键点）来驱动生成。当面对多物体场景时，这些方法要么产生运动泄漏（一个物体的动作影响到另一个），要么需要额外的显式运动信号，无法实现灵活的、组合式的多动作迁移。

FlexiMMT 首次在隐式运动迁移范式下实现了**多物体、多动作的独立控制**，其核心创新在于将物体掩码直接引入扩散模型的注意力机制，通过屏蔽文本、动作与视频标记之间的跨物体交互，在无需外部动作标注的条件下完成精确的逐物体动作分配。

### 方法谱系中的位置

从方法演变的角度，FlexiMMT 位于以下几条技术路线的交汇点：

1. **隐式运动迁移（Implicit Motion Transfer）**：这类方法从参考视频中学习运动模式，并将其迁移到条件图像上，而不显式提取光流或轨迹。FlexiMMT 延续了这一范式，但通过引入可训练的运动标记（motion tokens）和物体特定掩码，将适用范围从单物体扩展到多物体场景。与依赖显式运动信号的显式方法相比，FlexiMMT 保持了隐式方法的灵活性和泛化能力。

2. **扩散模型中的注意力控制**：FlexiMMT 的 Motion Decoupled Mask Attention（MDMA）机制本质上是一种**结构化注意力掩码策略**。与通用扩散模型中不加约束的全注意力不同，MDMA 通过物体特定的二值掩码矩阵 $\mathcal{M}$ 将全局注意力解耦为逐物体的局部交互。这一思路与可控生成中基于掩码的注意力引导方法有相似之处，但 FlexiMMT 的独特之处在于：（a）掩码直接作用于文本、动作和视频三类标记的交叉注意力，而非仅作用于空间特征；（b）掩码在训练和推理阶段通过不同的机制自动获取，无需人工标注。

3. **基于掩码的视频物体追踪**：FlexiMMT 的 Regressive Mask Propagation Mechanism（RMPM）从第一帧的语义分割掩码出发，通过特征相关性传播生成后续帧的物体掩码。这与视频物体分割（VOS）中的掩码传播方法有相似的思想，但 RMPM 工作在扩散模型的潜在空间而非像素空间，且利用去噪过程中早期步骤即可完成运动传递的观察（Figure 4），设计了动态早期停止策略以加速推理。

### 适用边界与依赖

FlexiMMT 的适用性受到以下边界的约束：

- **训练阶段的单物体假设**：训练时每个参考视频只能包含单个物体，模型通过 MDMA 学习到的解耦能力依赖于这一简化。对于包含多个运动物体的训练视频，当前的掩码提取机制（基于 QK 乘法的硬阈值方法）无法有效分离不同物体的特征（Figure 3 展示了特征纠缠问题）。这意味着模型对多物体场景的泛化能力是通过推理阶段的掩码组合实现的，而非直接从多物体训练数据中学习。

- **推理阶段的外部模型依赖**：推理时需要外部语义分割模型（论文提及使用 Grounded SAM）为第一帧提供物体掩码。这引入了额外的计算开销和外部模型的性能依赖——如果分割模型未能准确识别所有物体或边界不精确，初始掩码的误差会通过 RMPM 传播到后续帧。

- **掩码传播的鲁棒性边界**：RMPM 基于特征相关性进行掩码传播，在严重遮挡、快速运动或物体外观剧烈变化的场景下，相关性计算的可靠性可能下降。论文未提供针对这些极端情况的定量分析，该边界需要进一步验证。

- **超参数敏感性**：动态 RMPM 中的阈值 $\alpha$ 和局部时间窗口大小 $W$ 需要手动设置。虽然 Figure 7 展示了动态策略在不牺牲性能的前提下显著加速推理，但不同场景下这些超参数的最优值可能不同，实际部署时可能需要针对具体应用进行调优。

### 局限与开放问题

**已知局限**（论文中可验证）：

1. 训练阶段仅支持单物体参考视频，限制了对复杂多物体交互场景的直接建模能力。
2. 推理阶段依赖外部语义分割模型，未实现完全端到端的多物体运动迁移。
3. 动态掩码传播的超参数需要手动设定，缺乏自适应的参数选择机制。

**开放问题**（基于方法逻辑的延伸）：

1. **端到端的掩码获取**：能否将物体掩码的提取完全集成到扩散模型内部，从而消除对外部语义分割模型的依赖？一种可能的路径是利用扩散模型自身的交叉注意力图进行无监督的物体发现，但这需要解决多物体场景下的特征纠缠问题——这正是 Figure 3 所揭示的核心挑战。

2. **扩展到更多物体与更复杂场景**：当前实验主要展示两个物体的场景。当物体数量增加到三个或更多时，MDMA 的掩码矩阵规模线性增长，但注意力解耦的有效性是否能够保持？特别是当物体之间存在严重遮挡或空间重叠时，基于二值掩码的硬性解耦策略可能不足以处理边界区域的模糊归属问题。

3. **跨框架的可迁移性**：MDMA 的注意力解耦策略是否可应用于文本到视频（T2V）生成或其他视频扩散模型框架？这取决于目标框架是否具有与 CogVideoX 相似的文本-视频联合注意力结构，以及是否能够插入可训练的运动标记。

4. **与显式运动信号的结合**：FlexiMMT 目前完全依赖隐式运动学习。是否可以将显式运动信号（如稀疏轨迹或骨骼关键点）作为辅助条件引入，以提升运动控制的精确性和可编辑性？这需要在 MDMA 的掩码框架中为新的条件信号设计对应的注意力交互规则。

## 原文 PDF

![[paperPDFs/CVPR_2026/Let_Your_Image_Move_with_Your_Motion_Implicit_Multi_Object_Multi_Motion_Transfer.pdf]]
