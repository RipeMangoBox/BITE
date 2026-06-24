---
title: "HumanTOMATO: Text-Aligned Whole-Body Motion Generation"
type: paper
paper_level: A
venue: ICML
year: 2024
pdf_ref: paperPDFs/ICML_2024/HumanTOMATO_Text_Aligned_Whole_Body_Motion_Generation.pdf
aliases:
- HumanTOMATO
tags:
- ICML_2024
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 引入整体层次向量量化（H2VQ）对身体和手部动作进行分层离散编码，并采用预训练的文本-动作检索模型（TMR）提供运动感知的语言先验和显式的序列级对齐监督。
primary_logic: 通过将全身动作解耦为身体、手和面部，分别进行层次化离散表示学习，并利用运动感知的文本嵌入和对比对齐损失，可以在极低比特率下实现高质量且文本一致的全身动作生成。
claims:
- H2VQ在Motion-X上的MPJPE为92.97，显著优于Vanilla VQ (140.66) 和RVQ (110.94)。
- 引入TMR语言先验和对齐监督后，HumanTOMATO在Motion-X上FID降至1.174，TMR-R-Precision(256) Top1提升至0.416。
- 使用H2VQ的T2M-GPT相比不使用H2VQ，FID从1.366降至1.086，TMR-R-Precision Top1从0.368升至0.405。
- 预训练的TMR文本编码器替换CLIP文本编码器能更好地理解运动方向性和动态。
---

# HumanTOMATO: Text-Aligned Whole-Body Motion Generation

> [!tip] 核心洞察
> 通过将全身动作解耦为身体、手和面部，分别进行层次化离散表示学习，并利用运动感知的文本嵌入和对比对齐损失，可以在极低比特率下实现高质量且文本一致的全身动作生成。

| 字段 | 内容 |
|------|------|
| 中文题名 | HumanTOMATO：基于文本对齐的全身动作生成 |
| 英文题名 | HumanTOMATO: Text-Aligned Whole-Body Motion Generation |
| 会议/期刊 | ICML 2024 |
| Links | [paper](https://arxiv.org/abs/2310.12978) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | HumanTOMATO |
| Dataset | Motion-X |

> [!tip] 效果简介
> - Motion-X 上，FID↓ 1.174 vs 1.366 (T2M-GPT) (-0.192)；TMR-R-Precision(256) Top1↑ 0.416 vs 0.368 (T2M-GPT) (+0.048)；R-Precision(32) Top1↑ 0.399 vs 0.310 (T2M-GPT) (+0.089)。

## 概述

### 问题瓶颈

文本驱动的全身动作生成面临两个核心瓶颈。其一，现有方法（如 **T2M-GPT** (Zhang et al., 2023)、**MDM** (Tevet et al., 2023)）仅生成身体动作，忽略手部和面部细节，导致生成的全身动作缺乏生动性。其二，文本-动作对齐局限于帧级别，缺少序列级语义理解，使得生成的动作与文本描述之间存在对齐偏差。

### 核心方法

针对上述问题，本文提出 **HumanTOMATO**，其核心思路是通过解耦-分层表示-运动感知对齐三条路径实现全身动作生成：

1.  **整体层次向量量化（H2VQ）**：将全身动作解耦为身体和手部两个层次，分别使用独立编码器和码本进行离散表示学习。H2VQ 通过层次化结构关系，在极低比特率下保持高保真重建。
2.  **层次化自回归生成（Hierarchical-GPT）**：先预测身体令牌序列，再基于身体令牌和文本条件预测手部令牌序列，实现身体-手部的层次化生成。
3.  **运动感知语言先验与对齐监督**：引入预训练的文本-动作检索模型（TMR）提供运动感知的文本嵌入，替代传统 CLIP 嵌入；同时通过显式的对比对齐损失，在序列级别监督生成动作与文本的语义一致性。
4.  **面部条件 VAE**：独立的面部条件 VAE 根据表情文本生成面部运动，与身体、手部动作组合为完整的全身动作。

### 核心结论与证据强度

在 Motion-X 数据集上，HumanTOMATO 取得了显著提升：

-   **生成质量**：FID 降至 1.174，较 T2M-GPT 基线（1.366）降低 0.192（Table 1，置信度 0.99）。
-   **文本-动作对齐**：TMR-R-Precision(256) Top1 提升至 0.416，较基线（0.368）提升 0.048；传统 R-Precision(32) Top1 提升至 0.399（基线 0.310），提升 0.089（Table 1，置信度 0.99）。
-   **重建精度**：H2VQ 在 Motion-X 上的 MPJPE 为 92.97 mm，显著优于 Vanilla VQ（140.66 mm）和 RVQ（110.94 mm），验证了分层量化的有效性（Table 10，置信度 0.95）。

消融实验进一步证实：H2VQ 使 T2M-GPT 的 FID 从 1.366 降至 1.086，TMR-R-Precision Top1 从 0.368 升至 0.405（Table 13，置信度 0.95）；同时使用 TMR 嵌入和对齐监督时，HumanML3D 上的 FID 低至 0.312（Table 14，置信度 0.95）。

### 方法谱系与知识库定位

HumanTOMATO 属于**离散潜空间生成**范式的文本驱动动作生成方法，其技术路线可定位于以下谱系：

| 方法 | 动作表示 | 生成架构 | 语言先验 | 全身覆盖 |
| :--- | :--- | :--- | :--- | :--- |
| **T2M-GPT** (Zhang et al., 2023) | 单一 VQ-VAE | 单级 GPT 自回归 | CLIP 嵌入 | 仅身体 |
| **MDM** (Tevet et al., 2023) | 连续潜空间 | 扩散模型 | CLIP 嵌入 | 仅身体 |
| **MLD** (Chen et al., 2023b) | 连续潜空间 | 潜空间扩散 | CLIP 嵌入 | 仅身体 |
| **HumanTOMATO** (本文) | **H2VQ（身体+手部分层离散码本）** | **Hierarchical-GPT（层次自回归）** | **TMR 运动感知嵌入 + 对比对齐损失** | **身体+手部+面部** |

本文的核心贡献在于将**分层离散表示**与**运动感知的序列级对齐**引入全身动作生成，填补了现有方法在手部、面部生成及语义对齐方面的空白。

### 局限与待验证点

-   当前仅使用序列级整体文本描述，缺乏帧级或细粒度身体部位描述，限制了复杂动作的生成能力。
-   面部动作采用简单的条件 VAE，尚未与身体-手部生成统一为端到端框架。
-   模型尚未在大规模多源文本-运动数据上训练，泛化能力有待验证。
-   面部表情质量的客观评估指标缺失，该点需要手动验证。

## 背景与动机

### 问题背景

文本驱动的动作生成旨在根据自然语言描述合成逼真的人体运动序列，在虚拟人动画、人机交互和游戏影视等领域具有广泛应用。近年来，基于离散令牌的自回归模型（如 **T2M-GPT**，Zhang et al., 2023）和基于扩散模型的连续生成方法（如 **MDM**，Tevet et al., 2023；**MLD**，Chen et al., 2023b）在身体动作生成上取得了显著进展。然而，一个完整的人体运动不仅包含躯干和四肢的动作，还需要协调的手部手势和面部表情，才能真正传递出文本所描述的语义和情感。

### 现有方法缺口

当前文本驱动动作生成方法存在两个核心瓶颈：

**1. 全身动作建模不完整。** 现有方法几乎全部聚焦于身体动作生成，忽略了手部和面部细节。手部动作对于表达“挥手”“指向”等语义至关重要，面部表情则承载着“微笑”“恐惧”等情感信息。缺乏这些细节的生成结果虽然身体运动合理，但整体表现力不足，显得“不生动”。

**2. 文本-动作对齐粒度不足。** 主流方法引入语言先验的方式存在固有局限：基于 CLIP 文本编码器的方法（如 MLD）仅提供图像-文本对齐的语义嵌入，缺乏对运动方向性、动态特性的理解；基于大语言模型（LLMs）的方法则仅有纯文本先验，同样无法捕捉运动特有的时空模式。此外，现有对齐监督仅停留在帧级别或隐式层面，缺少序列级别的显式语义对齐约束，导致生成动作与文本描述之间的对应关系不够精确。

### 本文动机

针对上述问题，本文提出 **HumanTOMATO**，核心动机包括：

- **构建全身动作生成框架**：将动作解耦为身体、手部和面部三个组成部分，分别建模并最终融合，实现文本驱动的高质量全身动作生成。
- **设计层次化离散表示（H2VQ）**：通过整体层次向量量化，对身体和手部动作进行分层离散编码，在极低比特率下保留细粒度运动信息，同时建立身体与手部之间的层次结构关系。
- **引入运动感知的语言先验与显式对齐**：采用预训练的文本-动作检索模型（TMR）提供运动感知的文本嵌入，并通过对比对齐损失实现序列级的显式文本-动作对齐监督，从根本上提升生成动作与文本语义的一致性。

## 核心创新

HumanTOMATO 围绕“文本对齐的全身动作生成”这一目标，针对现有方法的两大瓶颈——**忽略手部/面部细节**与**缺乏序列级文本-动作对齐**——进行了三项关键创新。这些创新构成了从动作表示、生成架构到语言先验的完整技术链条。

### 1. 整体层次向量量化（H²VQ）：解耦身体与手部的离散表示

现有方法（如 T2M-GPT、MDM）通常使用单一 VQ-VAE 对整个身体动作进行编码，手部细节在压缩过程中容易被淹没，导致重建精度不足。HumanTOMATO 提出 **H²VQ（Holistic Hierarchical Vector Quantization）**，将全身动作显式解耦为身体与手部两个层次，分别使用独立的编码器和码本进行离散表示学习。

- **Changed Slot**：动作表示与量化从“单一 VQ-VAE 编码全身动作”变为“H²VQ 分离身体/手部编码器，层次量化，代码组合空间 $O(K^2)$”（Section 2.2, Figure 2(a)）。
- **因果机制**：身体码本捕获全局姿态与位移的粗粒度模式，手部码本专注于手指关节的精细运动。两个码本的组合索引在推理时形成 $K_B \times K_H$ 的联合离散空间，使模型在极低比特率下仍能保留手部细节。
- **决定性证据**：在 Motion-X 上，H²VQ 的 MPJPE 为 **92.97 mm**，相比 Vanilla VQ (512) 的 140.66 mm 降低 **47.69 mm**，相比 RVQ 的 110.94 mm 降低 **17.97 mm**（Table 10）。在 T2M-GPT 框架中引入 H²VQ 后，FID 从 1.366 降至 **1.086**，TMR-R-Precision Top1 从 0.368 升至 **0.405**（Table 13），证明层次化离散表示对生成质量与对齐度的双重增益。

### 2. Hierarchical-GPT：层次化自回归生成架构

传统方法（如 T2M-GPT）采用单级 GPT 自回归预测所有运动令牌，未区分身体与手部的结构层级关系。HumanTOMATO 设计 **Hierarchical-GPT**，按“先身体后手部”的层次顺序进行自回归预测。

- **Changed Slot**：生成架构从“单级 GPT 预测所有运动令牌”变为“Hierarchical-GPT 先预测身体令牌，再预测手部令牌”（Section 2.3, Equation 2）。
- **因果机制**：每个时间步先预测身体代码索引 $\mathbf{I}_s^{B}$，再以该身体索引为条件预测对应的手部代码索引 $\mathbf{I}_s^{H}$。这种条件依赖显式建模了身体运动对手部姿态的因果约束（如“走路时手部自然摆动”），避免了身体与手部运动的不协调。
- **公式表达**：
  $$P(\mathbf{I}_{1,2,\cdots,L/r}^{B,H} \mid \mathbf{t}) = \prod_{s=1}^{L/r} P(\mathbf{I}_s^{B} \mid \mathbf{I}_{<s}^{B,H}, \mathbf{t}) \cdot P(\mathbf{I}_s^{H} \mid \mathbf{I}_s^{B}, \mathbf{I}_{<s}^{B,H}, \mathbf{t})$$
- **配套模块**：面部动作通过独立的 **Facial cVAE** 基于表情文本生成（Figure 2(c)），与身体-手部生成解耦，使全身动作（身体+手+面部）完整且协调。

### 3. 运动感知的语言先验与显式对齐监督

现有方法普遍使用 CLIP 文本编码器嵌入作为条件（Figure 3），但 CLIP 训练于图像-文本对，缺乏对运动方向性、动态性的理解能力。HumanTOMATO 引入预训练的 **文本-动作检索模型 TMR** 作为语言先验，并添加显式的**对比对齐损失**进行序列级监督。

- **Changed Slot**：语言先验从“CLIP 文本嵌入”变为“预训练 TMR 文本编码器提供运动感知嵌入 + 显式文本-动作对比对齐损失”（Section 2.4, Figure 3）。
- **因果机制**：TMR 文本编码器在训练中学习将文本映射到与动作嵌入对齐的语义空间，天然理解“旋转”“跳跃”等运动相关语义。在此基础上，HumanTOMATO 在生成器输出端添加对比对齐模块，强制生成的动作序列与输入文本在 TMR 嵌入空间中保持高相似度，实现序列级（而非仅帧级）的对齐监督。
- **决定性证据**：在 Motion-X 上，同时使用 TMR 嵌入与对齐监督时，HumanTOMATO 的 FID 降至 **1.174**，TMR-R-Precision (256) Top1 达到 **0.416**，显著优于 T2M-GPT（FID 1.366, Top1 0.368）和仅使用 TMR 嵌入无监督的变体（Table 1, Table 3）。论文明确指出，CLIP 嵌入无法理解运动方向性，而 TMR 嵌入有效弥补了这一缺陷（Section 2.4）。

### 创新之间的协同关系

三项创新并非孤立设计，而是形成因果闭环：**H²VQ** 提供高质量的身体-手部分层离散表示，为 **Hierarchical-GPT** 的层次预测提供结构化令牌序列；**TMR 语言先验与对齐监督** 则驱动 Hierarchical-GPT 生成与文本语义高度一致的令牌序列。三者叠加使得 HumanTOMATO 在极低比特率下实现了高质量且文本对齐的全身动作生成。

## 整体框架

HumanTOMATO 的总体 pipeline 围绕一个核心洞察展开：**将全身动作解耦为身体、手部和面部三个异质组分，分别采用层次化离散表示与生成策略，并引入运动感知的语言先验进行显式的序列级对齐监督**。这一设计解决了现有方法仅生成身体动作、忽略手部和面部细节，以及文本-动作对齐仅停留在帧级别的瓶颈问题。

整体框架由四个关键模块串联构成，形成“表示学习 → 层次生成 → 面部补全 → 对齐监督”的完整链路：

### 1. H2VQ-VAE：整体层次向量量化

第一阶段的核心是 **Holistic Hierarchical Vector Quantization (H²VQ)**（Figure 2(a)），负责将身体和手部动作压缩为两个具有层次结构关系的离散码本。与传统的单一 VQ-VAE 对整个身体动作编码不同，H²VQ 设计了两套独立的编码器与码本：

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2310_12978/figures/002_Figure_2.jpg]]
*Figure 2: The framework overview of the proposed text-driven whole-body motion generation. (a) Holistic Hierarchical Vector Quantization $\mathrm { ( H ^ { 2 } V Q ) }$ to compress fine-grained body-hand motion into two discrete codebooks with hierarchical structure relations. (b) Hierarchical-GPT using motionaware textual embedding as the input to hierarchically generate body-hand motions. (c) Facial textconditional VAE (cVAE) to generate the corresponding facial motions. The outputs of body, hand, and face motions comprise a vivid and text-aligned whole-body motion*

- **身体编码器**与**身体码本** $\mathcal{C}^B$：编码躯干、四肢等主体运动
- **手部编码器**与**手部码本** $\mathcal{C}^H$：编码精细的手指动作

两个码本之间存在层次依赖关系——手部代码的预测以对应时间步的身体代码为条件。这种设计使代码组合空间从单一码本的 $O(K)$ 扩展为 $O(K^2)$，在相同码本容量的前提下显著提升了表示精度。训练损失在标准 VQ-VAE 的重建损失和 commitment 损失基础上，同时优化两个码本：

$$
\mathcal{L} = \| \mathbf{m} - \mathrm{Dec}(\mathcal{Q}^{H}(\mathbf{z}^{H};\mathcal{C}^{H}), \mathcal{Q}^{B}(\mathbf{z}^{B};\mathcal{C}^{B})) \|_2^2 + \alpha (\| \mathbf{z}^{H} - \mathrm{sg}(\hat{\mathbf{z}}^{H}) \|_2^2 + \| \mathbf{z}^{B} - \mathrm{sg}(\hat{\mathbf{z}}^{B}) \|_2^2)
$$

### 2. Hierarchical-GPT：层次自回归生成

第二阶段采用 **Hierarchical-GPT**（Figure 2(b)），以运动感知的文本嵌入为条件，自回归地预测身体和手部的离散令牌序列。其核心是层次化的预测范式——在每个时间步 $s$，先预测身体代码索引 $\mathbf{I}_s^B$，再基于已预测的身体代码预测手部代码索引 $\mathbf{I}_s^H$：

$$
P(\mathbf{I}_{1,2,\cdots,L/r}^{B,H} \mid \mathbf{t}) = \prod_{s=1}^{L/r} P(\mathbf{I}_s^{B} \mid \mathbf{I}_{<s}^{B,H}, \mathbf{t}) \cdot P(\mathbf{I}_s^{H} \mid \mathbf{I}_s^{B}, \mathbf{I}_{<s}^{B,H}, \mathbf{t})
$$

这一设计显式建模了身体运动对手部运动的因果约束，使生成的手部动作与身体动作保持物理一致性。

### 3. Facial cVAE：面部条件生成

面部动作通过独立的 **Facial conditional VAE (cVAE)** 生成（Figure 2(c)）。该模块由面部编码器、文本编码器和面部解码器组成，以表情相关的文本描述为条件，生成对应的面部运动序列。当前设计采用分离式架构，主要是因为面部运动与身体-手部运动的数据分布和时序特性差异较大；作者也指出，当更多面部运动数据可用时，需要更先进的统一设计。

### 4. 运动感知的语言先验与对齐监督

区别于现有方法直接使用 CLIP 文本编码器嵌入作为条件（Figure 3），HumanTOMATO 引入了**预训练的文本-动作检索模型 TMR** 提供运动感知的文本嵌入，并在此基础上添加显式的**文本-动作对比对齐损失**。这一监督信号作用于序列级别，强制生成的动作与文本描述在共享嵌入空间中保持高度一致，弥补了传统方法仅依赖帧级对齐的不足。

### 输入输出流总结

- **输入**：自然语言文本描述 $\mathbf{t}$
- **文本编码**：TMR 文本编码器 → 运动感知的文本嵌入
- **身体-手部生成**：Hierarchical-GPT 自回归预测 H²VQ 码本索引 → H²VQ 解码器重建身体和手部动作
- **面部生成**：Facial cVAE 基于表情文本生成面部运动
- **输出**：融合身体、手部、面部三者的全身动作序列 $\mathbf{m}$
- **监督信号**：生成动作与文本之间的对比对齐损失，确保序列级语义一致性

## 核心模块与公式推导

### 整体层次向量量化（H²VQ）

HumanTOMATO 的核心创新在于将全身动作分解为身体、手部和面部三个独立通道，并针对身体与手部动作设计了一种**层次化离散表示学习**方案。该方法的关键瓶颈在于：现有 VQ-VAE 对整个身体动作进行单一码本量化，无法捕捉身体与手部在运动粒度上的层次差异，导致重建精度不足且生成质量受限。

**H²VQ 模块**由以下组件构成（Figure 2(a)）：

1. **分离编码器**：身体编码器 $E^B$ 和手部编码器 $E^H$ 分别将身体运动序列和手部运动序列映射到各自的潜空间 $\mathbf{z}^B$ 和 $\mathbf{z}^H$。
2. **双码本量化**：两个独立的码本 $\mathcal{C}^B = \{\mathbf{e}_k^B\}_{k=1}^{K}$ 和 $\mathcal{C}^H = \{\mathbf{e}_k^H\}_{k=1}^{K}$ 分别对身体和手部潜向量进行离散化。量化操作遵循最近邻搜索：

$$\hat{\mathbf{z}} = \mathcal{Q}(\mathbf{z}; \mathcal{C}) = \underset{\mathbf{e}_k}{\arg\min} \lVert \mathbf{z} - \mathbf{e}_k \rVert_2^2$$

3. **层次结构关系**：身体码本索引 $\mathbf{I}^B$ 与手部码本索引 $\mathbf{I}^H$ 之间存在显式的条件依赖——手部动作的离散编码以对应时刻的身体动作为条件，形成“身体先行、手部后验”的层次结构。这种设计使得代码组合空间从单一码本的 $O(K)$ 扩展为 $O(K^2)$，在相同码本容量下显著提升了表示能力。

**训练损失函数**（Equation 3）同时优化两个码本的重建误差和 commitment 损失：

$$\mathcal{L} = \| \mathbf{m} - \mathrm{Dec}(\mathcal{Q}^H(\mathbf{z}^H;\mathcal{C}^H), \mathcal{Q}^B(\mathbf{z}^B;\mathcal{C}^B)) \|_2^2 + \alpha (\| \mathbf{z}^H - \mathrm{sg}(\hat{\mathbf{z}}^H) \|_2^2 + \| \mathbf{z}^B - \mathrm{sg}(\hat{\mathbf{z}}^B) \|_2^2)$$

其中 $\mathrm{sg}(\cdot)$ 表示停止梯度算子，$\alpha$ 为 commitment 损失权重。与标准 VQ-VAE（Equation 1）相比，H²VQ 将单一重建项和 commitment 项扩展为身体与手部的联合优化。

**决定性证据**：Table 10 显示，在 Motion-X 数据集上，H²VQ 的 MPJPE 为 92.97 mm，显著优于 Vanilla VQ（140.66 mm，码本大小 512）和 RVQ（110.94 mm），证明了层次化解耦量化的有效性。

---

### 层次化 GPT 生成器（Hierarchical-GPT）

在获得离散表示后，HumanTOMATO 采用**层次化自回归生成**策略来预测运动令牌序列。与基线方法 T2M-GPT（Zhang et al., 2023）的单级自回归预测不同，Hierarchical-GPT 将身体和手部代码索引的联合概率分解为层次化条件概率（Equation 2）：

$$P(\mathbf{I}_{1,2,\cdots,L/r}^{B,H} \mid \mathbf{t}) = \prod_{s=1}^{L/r} P(\mathbf{I}_s^{B} \mid \mathbf{I}_{<s}^{B,H}, \mathbf{t}) \cdot P(\mathbf{I}_s^{H} \mid \mathbf{I}_s^{B}, \mathbf{I}_{<s}^{B,H}, \mathbf{t})$$

**变量含义**：
- $\mathbf{t}$：文本条件嵌入
- $\mathbf{I}_s^B$：第 $s$ 个时间步的身体码本索引
- $\mathbf{I}_s^H$：第 $s$ 个时间步的手部码本索引
- $\mathbf{I}_{<s}^{B,H}$：前 $s-1$ 个时间步的所有身体和手部索引
- $L/r$：下采样后的序列长度

**因果机制**：在每个时间步，模型首先基于历史令牌和文本条件预测身体令牌 $P(\mathbf{I}_s^B \mid \mathbf{I}_{<s}^{B,H}, \mathbf{t})$，随后以当前身体令牌为附加条件预测手部令牌 $P(\mathbf{I}_s^H \mid \mathbf{I}_s^B, \mathbf{I}_{<s}^{B,H}, \mathbf{t})$。这种“先身体后手部”的生成顺序强制模型学习身体运动对手部运动的因果约束，避免了独立生成导致的手部动作与身体姿态不一致。

**消融证据**：Table 13 显示，在 T2M-GPT 框架中引入 H²VQ 层次化表示后，FID 从 1.366 降至 1.086，TMR-R-Precision Top1 从 0.368 升至 0.405，证实层次化生成策略对质量和文本对齐的双重提升。

---

### 运动感知语言先验与对齐监督

HumanTOMATO 的语言先验引入方式与现有方法存在本质差异（Figure 3）。基线方法通常使用 CLIP 文本编码器将文本映射到图像-文本对齐空间，但该空间缺乏对运动方向性、动态性和时序结构的理解。HumanTOMATO 采用**预训练的文本-动作检索模型 TMR** 作为文本编码器，其嵌入空间天然具备运动感知能力。

**对齐监督模块**在生成器输出端引入显式的对比损失：将生成的全身动作序列与输入文本在 TMR 的联合嵌入空间中进行对比对齐，直接优化序列级的文本-动作匹配度。这一设计与仅依赖条件生成的隐式对齐形成互补。

**决定性证据**：Table 1 显示，引入 TMR 语言先验和对齐监督后，HumanTOMATO 在 Motion-X 上的 FID 降至 1.174，TMR-R-Precision(256) Top1 提升至 0.416，显著优于 T2M-GPT（FID 1.366，Top1 0.368）。Table 3 的消融进一步表明，同时使用 TMR 嵌入和对齐监督时，各项指标均优于仅使用 TMR 嵌入无监督的配置。

---

### 面部条件 VAE（Facial cVAE）

面部动作生成采用独立的条件 VAE 模块（Figure 2(c)），由面部编码器、文本编码器和面部解码器组成。该模块以表情文本描述为条件，生成与身体-手部运动时间对齐的面部表情序列。当前设计为分离式架构，尚未与 H²VQ 和 Hierarchical-GPT 统一为端到端框架，这一局限在论文的 open questions 中被明确指认为未来改进方向。

## 实验与分析

### 主实验结果

HumanTOMATO 在 Motion‑X 全身动作生成基准上全面优于现有方法。Table 1 报告了核心指标：HumanTOMATO 的 FID 降至 **1.174**，显著低于 T2M‑GPT 的 1.366、MDM 的 3.800 和 MLD 的 3.407，表明生成分布与真实分布高度一致。在文本‑动作对齐方面，采用更准确的 TMR‑R‑Precision(256) 指标，HumanTOMATO 的 Top‑1 召回率达到 **0.416**，而 T2M‑GPT、MLD、MDM 分别为 0.368、0.385、0.352；传统 R‑Precision(32) Top‑1 也由 0.310（T2M‑GPT）提升至 **0.399**。Matching‑Score 和 MModality 同样保持优势，说明模型在保证对齐精度的同时维持了合理的生成多样性。定性对比（Figure 4）进一步显示，HumanTOMATO 是唯一能同时生成面部表情的方法，手部动作质量和对齐度明显优于 MLD 和 T2M‑GPT。

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2310_12978/figures/004_Table_1.jpg]]
*Table 1: Main results of motion generation on Motion-X dataset*

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2310_12978/figures/005_Figure_4.jpg]]
*Figure 4: (b) Text: a person walks forwards, then suddenly, as if bumping into something, starts walking backwards, fearfully. Figure 4: Qualitative comparison with baselines. HumanTOMATO supports face motion generation and outperforms MLD and T2M-GPT on hand motion generation and text-motion alignment*

### 分层向量量化的重建能力

H²VQ 是生成质量提升的根基。Table 2 对比了不同量化方法在 Motion‑X、GRAB、HumanML3D 三个数据集上的 MPJPE（mm）。在 Motion‑X 上，H²VQ 的总体 MPJPE 仅为 **92.97**，相比 Vanilla VQ（512 码本）的 140.66 降低 47.69 mm，相比残差 VQ（RVQ）的 110.94 降低 17.97 mm；身体和手部分别评估时，H²VQ 同样一致最优。Table 10 的扩展消融进一步验证了分层结构的必要性：若将身体和手部合并为单一码本但保持分层解码，MPJPE 回升至 103.85；若完全取消分层（Vanilla VQ‑1024），则升至 130.42。这表明分离编码器与分层码本设计以极低比特率（码本尺寸仅 512×2）实现了高保真运动重建，为后续生成提供了干净、紧凑的离散令牌空间。

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2310_12978/figures/006_Table_2.jpg]]
*Table 2: Comparison of the motion reconstruction errors (MPJPE in mm) of different quantization methods on Motion-X, GRAB, and HumanML3D. Our $\mathrm { H } ^ { 2 } \mathrm { V }$ Q shows significant improvements

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2310_12978/figures/021_Table_10.jpg]]
*Table 10: Different vector quantization methods on Motion-X*

### 语言先验与对齐监督的因果作用

Table 3 系统消融了预训练文本‑动作对齐模型（TMR）作为语言先验的影响。基线使用 CLIP 文本嵌入的 T2M‑GPT 在 Motion‑X 上 FID 为 1.366，TMR‑R‑Precision(256) Top‑1 为 0.368。仅将 CLIP 替换为 TMR 文本嵌入，FID 降至 1.211，Top‑1 升至 0.403；进一步加入显式的文本‑动作对比对齐损失（即 HumanTOMATO 完整方案），FID 进一步降至 **1.174**，Top‑1 达到 **0.416**。这表明 TMR 提供的运动感知嵌入本身已能改善生成质量，而序列级对齐监督则在此基础上强化了语义一致性，两者协同作用显著。

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2310_12978/figures/007_Table_3.jpg]]
*Table 3: Abaltion on a pre-trained text-motion-aligned model for motion generation on Motion-X. Both TMR embedding and text-motion alignment supervision help generate text-aligned motions*

### H²VQ 对生成模型的增益

H²VQ 不仅提升重建质量，还直接惠及下游生成。Table 13 显示，在 T2M‑GPT 框架下，使用 H²VQ 令牌替代原始连续表示或 Vanilla VQ 令牌后，FID 从 1.366 降至 **1.086**，TMR‑R‑Precision(256) Top‑1 从 0.368 升至 **0.405**。这说明层次化离散表示有效降低了生成模型的建模难度，使其更容易学习文本到运动令牌的映射。

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2310_12978/figures/024_Table_13.jpg]]
*Table 13: The ablation on how can $\mathrm { H } ^ { 2 } \mathrm { V }$ Q help the whole-body motion generation on T2M-GPT

### 面部生成与整体协调

面部运动由独立的 Facial cVAE 基于表情文本生成。Table 9 报告了面部生成在 Motion‑X 上的定量结果，验证了该模块能够产生与文本描述匹配的面部表情运动。配合 H²VQ 和 Hierarchical‑GPT 生成的身体与手部动作，三者组合构成了协调的全身运动序列（Figure 1 定性示例）。不过，面部模块目前独立于主干框架，缺乏端到端的联合优化，这是当前设计的已知局限。

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2310_12978/figures/016_Table_9.jpg]]
*Table 9: Facial motion generation results on Motion-X dataset*

### 评估指标的可靠性

本文指出传统 R‑Precision(32) 和 Matching‑Score 在全身动作场景下区分度不足。Figure 5 对比了新旧指标在 Motion‑X 上的检索能力：TMR‑R‑Precision(256) 和 TMR‑Matching‑Score 在文本‑动作和动作‑文本双向检索中均表现出更高的 Recall@K，能更准确反映语义对齐质量。Table 5 和 Table 6 分别报告了 Motion‑X 和 HumanML3D 上真实动作与文本的 Recall@K，为指标的可信度提供了上限参考。

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2310_12978/figures/008_Figure_5.jpg]]
*Figure 5: Comparison with existing metrics on Motion-X. Existing evaluation metrics (Guo et al., 2022) are illustrated in red, and ours are in green. The B = 3 2 and B = 2 5 6 settings for retrieval are denoted as $\sp { 6 6 } - \bullet - \sp { 5 5 }$ and $\twoheadleftarrow$ respectively

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2310_12978/figures/011_Table_5.jpg]]
*Table 5: Recall@K (T2M and M2T) of GT motions and texts on the Motion-X dataset*

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2310_12978/figures/012_Table_6.jpg]]
*Table 6: Recall@K (T2M and M2T) of GT motions and texts on the HumanML3D dataset*

### 失败模式与局限

尽管整体性能领先，HumanTOMATO 仍存在以下可观测或作者指出的失败模式：
- **细粒度控制缺失**：当前仅使用序列级整体文本描述，无法指定帧级或左右手等细粒度动作，导致复杂交互动作的生成不可控。
- **面部生成独立性**：Facial cVAE 与身体‑手部生成管道分离，缺乏统一的全身生成框架，在面部数据更丰富时可能成为瓶颈。
- **泛化边界未充分测试**：模型仅在 Motion‑X 等现有数据集上验证，尚未在更大规模、多源文本‑运动配对数据上训练，跨域泛化能力待考证。
- **评估维度不完整**：面部表情质量和对齐度缺乏客观量化指标，当前主要依赖定性观察，该点需读者注意。

### 补充图表

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2310_12978/figures/003_Figure_3.jpg]]
*Figure 3: (a) Learning image-text aligned prior explicitly. (b) Learning image-text aligned prior implicitly. (c) Learning motion-text alignment explicitly(Ours). Figure 3: Technical comparisons on introducing language priors of existing methods*

## 方法谱系与知识库定位

### 1. 问题瓶颈与核心思路

现有文本驱动动作生成方法面临两个关键瓶颈：**（1）生成范围局限**——主流方法如 **T2M-GPT**（Zhang et al., 2023）、**MDM**（Tevet et al., 2023）和 **MLD**（Chen et al., 2023b）仅生成身体动作，忽略手部和面部细节，导致全身动作不生动；**（2）对齐粒度粗糙**——文本-动作对齐仅限于帧级别，缺乏序列级语义理解，生成的动作与文本描述匹配不准确。

HumanTOMATO 通过三个核心设计解决上述问题：
- **H²VQ（Holistic Hierarchical VQ-VAE）**：将全身动作解耦为身体和手部，分别进行层次化离散编码，代码组合空间达 $O(K^2)$，在极低比特率下实现高保真重建；
- **Hierarchical-GPT**：基于运动感知的文本嵌入，先预测身体令牌序列，再预测手部令牌序列，建立层次化自回归生成范式；
- **序列级对齐监督**：引入预训练的文本-动作检索模型 **TMR** 提供运动感知的语言先验，并通过对比损失显式监督生成动作与文本的序列级对齐。

### 2. 与基线方法的技术对比

| 方法维度        | 基线方法                                             | HumanTOMATO                             | 变化性质    |
| ----------- | ------------------------------------------------ | --------------------------------------- | ------- |
| **动作表示与量化** | 单一 VQ-VAE 对整个身体编码（T2M-GPT）                       | H²VQ：分离身体/手部编码器，层次量化                    | 架构级重构   |
| **生成架构**    | 单级 GPT 自回归预测所有运动令牌                               | Hierarchical-GPT：先身体后手部的层次预测            | 范式升级    |
| **语言先验**    | CLIP 文本编码器嵌入作为条件                                 | 预训练 TMR 文本编码器 + 显式对比对齐损失                | 先验替换与增强 |
| **面部生成**    | 忽略或未专门处理                                         | 独立面部条件 VAE，基于表情文本生成                     | 功能新增    |
| **评估指标**    | R-Precision(32)、Matching-Score（Guo et al., 2022） | TMR-R-Precision(256)、TMR-Matching-Score | 评估体系升级  |

**关键差异解析**：

1. **从单一量化到层次量化**：T2M-GPT 使用标准 VQ-VAE 对整个身体动作进行统一编码，而 H²VQ 设计独立的身体和手部编码器与码本，通过层次结构关系捕捉身体-手部的解剖学依赖。Table 10 显示，H²VQ 在 Motion-X 上的 MPJPE 为 92.97 mm，显著优于 Vanilla VQ（140.66 mm）和 RVQ（110.94 mm）。

2. **从 CLIP 到运动感知语言先验**：现有方法普遍使用 CLIP 文本编码器，其训练目标为图像-文本对齐，缺乏对运动方向性和动态的理解。HumanTOMATO 采用在运动-文本对上预训练的 TMR 文本编码器，能更好地捕捉“走”、“跑”、“挥手”等动作语义的方向性和时序特征（见 Section 2.4）。

3. **从隐式对齐到显式监督**：Figure 3 对比了三种语言先验引入方式：（a）显式学习图像-文本对齐先验、（b）隐式学习图像-文本对齐先验、（c）显式学习运动-文本对齐（HumanTOMATO）。前两种依赖图像模态作为中介，而 HumanTOMATO 直接在运动-文本空间进行对比对齐，消除了模态鸿沟。

### 3. 适用边界与局限

**适用场景**：
- 文本驱动的全身动作生成，特别是需要手部和面部细节的场景（如虚拟人交互、动画制作）；
- 序列级文本描述驱动，支持身体、手部、面部的协调生成。

**已知局限**（论文明确指出的）：
1. **文本粒度受限**：当前仅使用序列级整体文本描述，缺乏帧级别或细粒度的身体部位描述（如“左手挥手，右手叉腰”），限制了复杂动作的精确控制；
2. **面部生成模块独立**：面部动作采用简单的条件 VAE 生成，缺乏与身体-手部生成模块的统一框架，当更多面部运动数据可用时需要更先进的设计；
3. **数据规模有限**：模型尚未在更大规模的多源文本-运动配对数据上训练，泛化能力有待验证。

### 4. 开放问题与未来方向

基于论文讨论和方法局限性，以下问题值得进一步探索：

1. **细粒度文本整合**：如何将帧级或部位级文本描述（如具体到左右手动作）有效整合到层次化生成框架中？这需要设计新的文本编码机制和条件注入策略。

2. **统一端到端框架**：当前身体、手部、面部由三个分离模块生成，能否设计一个统一的端到端框架同时高质量生成所有部位？这涉及多模态动作空间的联合建模和协调优化。

3. **大规模预训练的潜力**：在更大规模、更多样化的数据集上预训练文本-运动对齐模型（如 TMR 的扩展版本）是否会进一步增强生成性能？这需要构造或收集更丰富的全身运动-文本配对数据。

4. **面部生成评估**：如何客观评估全身动作生成中的面部表情质量和对齐度？现有指标（FID、R-Precision）主要针对身体动作，缺乏面部表情的专门评估指标。

5. **层次化结构的泛化性**：H²VQ 的身体-手部层次分解策略是否可以推广到其他多部位运动生成任务（如四足动物、多智能体协作）？这需要验证层次化离散表示在不同运动结构上的适应性。

## 原文 PDF

![[paperPDFs/ICML_2024/HumanTOMATO_Text_Aligned_Whole_Body_Motion_Generation.pdf]]
