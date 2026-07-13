---
title: "When Safety Collides: Resolving Multi-Category Harmful Conflicts in Text-to-Image Diffusion via Adaptive Safety Guidance"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/When_Safety_Collides_Resolving_Multi_Category_Harmful_Conflicts_in_Text_to_Image_Diffusion_via_Adaptive_Safety_Guidance.pdf
project_link: null
code_link: "https://github.com/tmllab/2026_CVPR_CASG"
aliases:
- CAASGC
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 安全引导方向是否与当前生成过程中的真实有害类别对齐。
primary_logic: 在去噪过程中动态识别与提示引导方向最一致的有害类别，并仅沿该类别施加安全纠正，能够避免多类别聚合带来的方向干扰和衰减。
claims:
- 错误的有害类别方向会导致有害率大幅上升，甚至超过未引导基线（如hate方向用于sexual提示时有害率达72.4%，而correct sexual方向仅为3.2%）。
- 组合多个有害类别会削弱单类别安全方向的效果，使有害率高于单类别引导（如sexual+hate达5.8%，而单独sexual为3.2%）。
- CASG在多个基准上显著降低有害率，CASG+SLD在I2P上仅10.2%（SDv1.5为42.2%），且图像质量保持与基线相当。
- I2P 上 Harmful Rate % = 10.2 (CASG+SLD)
---

# When Safety Collides: Resolving Multi-Category Harmful Conflicts in Text-to-Image Diffusion via Adaptive Safety Guidance

> [!tip] 核心洞察
> 在去噪过程中动态识别与提示引导方向最一致的有害类别，并仅沿该类别施加安全纠正，能够避免多类别聚合带来的方向干扰和衰减。

| 字段 | 内容 |
|------|------|
| 中文题名 | 当安全性碰撞：基于自适应安全引导的文本到图像扩散模型多类别有害冲突消解 |
| 英文题名 | When Safety Collides: Resolving Multi-Category Harmful Conflicts in Text-to-Image Diffusion via Adaptive Safety Guidance |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2602.20880) · [Code](https://github.com/tmllab/2026_CVPR_CASG) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Conflict-aware Adaptive Safety Guidance (CASG) |
| Dataset | I2P, CoProv2, COCO |

> [!tip] 效果简介
> - I2P 上，Harmful Rate % 10.2 (CASG+SLD) vs 42.2 (SD-v1.5) (-32.0)；Harmful Rate % 18.9 (CASG+SAFREE) vs 20.0 (SAFREE) (-1.1)。
> - CoProv2 上，Harmful Rate % 3.9 (CASG+SLD) vs 28.2 (SD-v1.5) (-24.3)。
> - COCO 上，CLIP Score ↑ 29.4 (CASG+SLD) vs 29.2 (SLD) (+0.2)。

## 概要

文本到图像扩散模型虽被广泛部署，但在面对可能诱发有害内容（如暴力、仇恨或性内容）的用户提示时，其安全性仍是一个核心挑战。现有安全引导方法——无论是潜在空间引导（如 **SLD**）还是文本空间引导（如 **SAFREE**）——通常通过拼接多个预定义有害类别的关键词来生成安全纠正方向。然而，本文揭示了一个此前被忽视的关键瓶颈：**不同有害类别的安全方向在生成过程中并非相互一致，而是存在交叉、抵消甚至反向的“有害冲突”**。简单聚合多类别关键词会导致安全方向的衰减与干扰，反而削弱整体安全性能，甚至在某些情形下使有害率超过未引导的基线模型。

针对这一瓶颈，本文提出 **Conflict-aware Adaptive Safety Guidance (CASG)**，一个免训练的即插即用框架。CASG 的核心洞察在于：**在去噪的每个时间步，动态识别与当前提示引导方向最一致的主导有害类别，并仅沿该单一类别施加安全纠正**，从而避免多类别聚合带来的方向干扰。该方法由两个组件构成：**Conflict-aware Category Identification (CaCI)** 负责自适应识别主导有害类别；**Conflict-resolving Guidance Application (CrGA)** 负责仅沿识别出的类别施加安全引导。CASG 可无缝嵌入潜在空间和文本空间的现有安全引导机制。

实验表明，CASG 在多个基准上显著降低有害率：CASG+SLD 在 I2P 基准上将有害率从 SDv1.5 的 42.2% 降至 10.2%，在 CoProv2 上从 28.2% 降至 3.9%，同时保持与基线相当的图像质量（COCO 上 CLIP Score 29.4 vs. SLD 29.2）。消融实验进一步证实，静态类别分类器无法适应动态冲突，而 CASG 的动态选择机制是性能提升的关键。该方法在性内容和非法活动等强冲突类别上尤为有效，且对预定义关键词的变体具有鲁棒性。

文本到图像（T2I）扩散模型的快速发展带来了严重的安全隐患——恶意用户可通过精心设计的提示词生成暴力、色情、仇恨言论等有害内容。为应对这一挑战，现有安全机制主要分为三类：模型编辑方法（如 **ESD**、**UCE**、**RECE**）通过修改模型参数擦除有害概念，但对训练资源要求高且可能损害生成质量；对齐式方法（如 **SafetyDPO**）通过偏好优化调整模型行为，但泛化能力有限；安全引导方法（如 **SLD**、**SAFREE**）在推理阶段施加安全约束，无需重新训练，成为当前最灵活的主流范式。

然而，现有安全引导方法存在一个被忽视的关键瓶颈：**多类别有害冲突**。这些方法通常将多个有害类别的关键词简单拼接，生成一个聚合的安全方向。但如图2所示，不同类别的安全方向在潜在空间中并不一致——它们相互交叉甚至对立，且这种关系在去噪过程中动态变化。当聚合方向与当前生成内容的真实有害类别不匹配时，安全引导不仅失效，还可能将生成过程推向其他有害区域。

Figure 1和Table 1量化了这一现象的严重性：对于性内容提示，使用正确的“sexual”安全方向可将有害率从67.2%降至3.2%；但若错误地施加“hate”方向，有害率反而飙升至72.4%，甚至超过无引导基线。更关键的是，当同时使用“sexual”和“hate”两个类别时，有害率回升至5.8%，表明多类别聚合会削弱单类别安全方向的效果——这一现象被称为**方向衰减**。图3进一步揭示了这种衰减的动态特性：不同类别在不同去噪时间步的主导程度波动显著，静态聚合无法适应这种变化。

上述发现揭示了一个因果调控点：**安全引导方向是否与当前生成过程中的真实有害类别对齐**。现有方法的核心缺陷在于缺乏动态类别识别机制，导致安全信号被无关类别的噪声所淹没。本文由此提出核心洞察：在去噪过程中动态识别与提示引导方向最一致的有害类别，并仅沿该类别施加安全纠正，能够避免多类别聚合带来的方向干扰和衰减。基于这一洞察，我们设计了**冲突感知自适应安全引导框架（CASG）**，通过即插即用的方式解决现有多类别安全机制中的有害冲突问题。

## 核心方法与创新机理

CASG 的核心创新在于将多类别安全引导从“静态聚合”转变为“动态对齐”，从而解决现有方法中普遍存在但未被系统研究的有害冲突问题。其关键设计体现在两个 changed slots 上。

### 从静态聚合到动态对齐的安全方向合成

现有基于安全引导的方法（如 **SLD** 和 **SAFREE**）在处理多个有害类别时，采用直接拼接预定义关键词的方式生成一个聚合的安全方向。这种静态聚合策略隐含假设不同类别的安全方向是一致的，然而实证分析表明，不同有害类别在潜在空间和文本空间中的安全方向往往相互交叉甚至对立，且这种关系随去噪时间步动态演化（Figure 2）。直接聚合会导致类别间方向相互抵消，使单类别安全方向的有效性被大幅削弱——例如，单独使用 sexual 方向时有害率为 3.2%，而同时叠加 sexual 和 hate 方向后有害率反而上升至 5.8%（Table 1）。

CASG 将安全方向合成方式从“静态拼接所有类别”改为“在每个时间步动态选择与当前生成状态最一致的有害类别，仅沿该单一类别施加安全纠正”。这一改变的核心因果机制在于：安全引导的有效性取决于引导方向是否与当前生成过程中实际激活的有害语义对齐。当引导方向与提示的实际有害类别匹配时，有害率可从无引导的 67.2% 骤降至 3.2%；而当引导方向错误（如用 hate 方向处理 sexual 提示）时，有害率反而飙升至 72.4%，甚至超过无引导基线（Table 1）。因此，动态识别并仅施加对齐的单一类别方向，从根本上避免了多类别聚合带来的方向干扰和衰减。

### 自适应有害类别识别机制

与静态拼接相对应的，是 CASG 引入了自适应有害类别识别机制，取代了基线方法中无类别选择的静态关键词拼接。这一机制通过两个关键模块实现：

- **Conflict-aware Category Identification (CaCI)**：在每个去噪时间步，动态识别与当前生成状态最一致的有害类别。在潜在空间中，CaCI 通过计算有害引导向量 $g_i$ 与提示引导向量 $g_p$ 之间的余弦相似度 $\cos\theta_i = \frac{g_i \cdot g_p}{\|g_i\| \|g_p\|}$（Eq. 4）来衡量方向一致性，并选择相似度最大的类别作为主导类别 $h^* = h_{\arg\max_i \cos\theta_i}$（Eq. 5）。在文本空间中，CaCI 则通过计算提示嵌入经有害子空间正交投影后的残差范数 $\|p_{h_i}^{\perp}\|$（Eq. 6），选择残差最小的类别 $h^* = h_{\arg\min_i \|p_{h_i}^{\perp}\|}$（Eq. 7），即提示嵌入与有害子空间最对齐的类别。

- **Conflict-resolving Guidance Application (CrGA)**：在 CaCI 识别出主导类别后，CrGA 仅沿该单一类别施加安全纠正，而非聚合所有类别的信号。这确保了安全引导始终与当前生成状态中的实际有害语义对齐，避免了多类别信号间的相互干扰。

### 与 LLM 辅助方法的本质区别

消融实验进一步验证了 CASG 动态识别机制的必要性。与使用 GPT-4o 或 QwenGuard 等外部 LLM 对提示进行静态有害分类后再施加 SLD 的替代方案相比，CASG+SLD 在 I2P 上的有害率仅为 10.2%，显著优于 GPT-4o 辅助 SLD 的 11.6% 和 QwenGuard 辅助 SLD 的 14.0%（Table 3）。这一差距表明，静态文本分类器无法感知去噪过程中动态演化的语义状态，而 CaCI 在潜在空间或文本空间中的动态对齐机制能够适应这种动态性，从而更准确地识别当前真正需要抑制的有害类别。

### 方法定位

CASG 是一个 training-free、即插即用的框架，无需模型微调或参数更新，可直接嵌入现有的潜在空间安全引导方法（如 SLD）和文本空间安全引导方法（如 SAFREE）中。这一设计使其区别于 **ESD**、**UCE**、**RECE** 等需要模型编辑的基线方法，以及 **SafetyDPO** 等需要对齐训练的方法，在保持轻量级部署的同时实现了显著的安全性提升。

CASG 是一个即插即用的训练无关框架，旨在解决现有多类别安全引导中的“有害冲突”问题。其核心思想是：在去噪过程的每个时间步，动态识别与当前生成状态最对齐的单一有害类别，并仅沿该类别施加安全纠正，从而避免多类别信号聚合带来的方向干扰和衰减。

框架由两个关键模块串联构成：

1. **Conflict-aware Category Identification (CaCI)**：在每一时间步，根据当前生成状态自适应地识别主导有害类别。具体而言，在潜在空间中，CaCI 计算各有害类别的安全引导向量与提示引导向量之间的余弦相似度（Eq. 4），选择相似度最大的类别作为主导类别（Eq. 5）；在文本空间中，CaCI 计算提示嵌入经过各有害子空间正交投影后的残差范数（Eq. 6），选择残差最小的类别（Eq. 7），即提示嵌入与该有害子空间最对齐的类别。

2. **Conflict-resolving Guidance Application (CrGA)**：获得主导有害类别后，CrGA 仅沿该单一类别施加安全纠正信号，而非聚合所有预定义类别的安全方向。在潜在空间方法（如 SLD）中，CrGA 将识别出的主导有害方向用于噪声预测的调整；在文本空间方法（如 SAFREE）中，CrGA 仅对提示嵌入执行针对该主导类别的正交投影，移除相应的有害成分。

整体流程如下：给定用户提示和预定义的有害类别集合 $H = (h_1, \ldots, h_k)$，在每个去噪时间步 $t$，CaCI 首先从当前潜在状态 $z_t$ 或提示嵌入中提取信号，识别主导有害类别 $h^*$；随后 CrGA 将 $h^*$ 对应的安全方向应用于基础安全引导机制，生成经过冲突消解的安全噪声预测或安全提示嵌入，最终引导扩散模型远离该特定有害区域。

CASG 作为一个轻量级修正器，可无缝嵌入现有的潜在空间安全引导方法（如 SLD）和文本空间安全引导方法（如 SAFREE），分别形成 CASG+SLD 和 CASG+SAFREE。框架的整体结构如图 4 所示，伪代码见 Algorithm 1。

### 问题形式化

现有安全引导方法在处理多类别有害内容时存在一个根本性瓶颈：简单拼接多个有害类别的关键词会生成方向不一致甚至相互抵消的安全引导信号，导致“有害冲突”。具体而言，给定一组预定义的有害类别 $H = (h_1, \ldots, h_k)$，每个类别 $h_i$ 产生一个安全引导方向 $g_i$，这些方向并非相互一致——部分方向在潜在空间中部分重叠，另一些则指向相反方向（Figure 2）。当多个类别被聚合使用时，类别层面的安全影响会被显著衰减（Figure 3），最终削弱整体安全性能。

![[assets/figures/papers/paper_list_l2364_https_arxiv_org_abs_2602_20880/figures/002_Figure_2.jpg]]
*Figure 2: Cross-Category Directional Conflict in latent space. Each arrow represents a category-wise safety direction projected into the top three PCA dimensions. Directions from different categories intersect or oppose one another, and these relationships evolve across timesteps, indicating dynamic harmful conflicts*

### CASG 框架总览

本文提出的 **Conflict-aware Adaptive Safety Guidance (CASG)** 是一个免训练、即插即用的框架，通过在现有安全引导机制中插入轻量级修正器来解决有害冲突。CASG 由两个核心模块组成：

- **Conflict-aware Category Identification (CaCI)**：在去噪过程中动态识别与当前生成状态最对齐的有害类别。
- **Conflict-resolving Guidance Application (CrGA)**：仅沿识别出的主导类别施加安全纠正，避免多类别信号干扰。

CASG 可同时集成到潜在空间方法（如 **SLD**）和文本空间方法（如 **SAFREE**）中，形成 CASG+SLD 和 CASG+SAFREE 两种变体。

### CASG+SLD：潜在空间中的冲突感知安全引导

**步骤 1：计算类别层面的有害引导与提示引导。** 对于每个预定义有害类别 $h_i$，在时间步 $t$ 计算其有害噪声估计：

$$\hat{\epsilon}_i = \epsilon_\theta(z_t, c_{h_i})$$

其中 $\epsilon_\theta$ 为扩散模型的噪声预测网络，$z_t$ 为当前潜在表示，$c_{h_i}$ 为有害类别 $h_i$ 的文本条件。有害引导向量 $g_i$ 由有害噪声与无条件噪声之差得到：

$$g_i = \hat{\epsilon}_i - \epsilon_\theta(z_t)$$

同时计算提示引导向量 $g_p$：

$$g_p = \epsilon_\theta(z_t, c_p) - \epsilon_\theta(z_t)$$

其中 $c_p$ 为用户提示的文本条件。

**步骤 2：CaCI — 通过方向一致性识别主导有害类别。** 有害引导 $g_i$ 与提示引导 $g_p$ 之间的余弦相似度衡量了二者的方向一致性：

$$\cos\theta_i = \frac{g_i \cdot g_p}{\|g_i\| \|g_p\|}$$

选择余弦相似度最大的类别作为主导有害类别：

$$h^* = h_{\arg\max_i \cos\theta_i}$$

这一设计的因果直觉是：当前生成过程中，与提示引导方向最一致的有害类别才是最需要被纠正的目标。错误的类别方向不仅无效，甚至会将生成推向其他有害区域（例如，对性内容提示施加仇恨类别引导时，有害率从 67.2% 飙升至 72.4%，远超未引导基线；Table 1）。

**步骤 3：CrGA — 沿主导类别施加安全引导。** 仅使用识别出的主导类别 $h^*$ 的安全方向进行噪声修正，替代原始 SLD 中聚合多类别关键词的做法，从而消除方向干扰和衰减。

### CASG+SAFREE：文本空间中的冲突感知正交投影

**步骤 1：计算投影残差。** 对于提示嵌入 $p$，在每个有害类别 $h_i$ 对应的有害子空间上进行正交投影，得到残差：

$$p_{h_i}^{\perp} = (I - P_{h_i}) p$$

其中 $P_{h_i}$ 为向有害子空间的投影矩阵，$I$ 为单位矩阵。残差 $p_{h_i}^{\perp}$ 表示去除该类别有害成分后的提示嵌入。

**步骤 2：CaCI — 通过残差幅值识别主导有害类别。** 残差范数 $\|p_{h_i}^{\perp}\|$ 越小，说明提示嵌入与该有害子空间越对齐，即该类别对当前提示的主导性越强。因此选择残差范数最小的类别：

$$h^* = h_{\arg\min_i \|p_{h_i}^{\perp}\|}$$

**步骤 3：CrGA — 仅对主导类别进行正交投影。** 仅使用主导类别 $h^*$ 对应的投影残差 $p_{h^*}^{\perp}$ 作为安全提示嵌入，替代原始 SAFREE 中对所有类别子空间的联合投影，避免多类别投影带来的语义过度偏移。

### 关键设计选择

CASG 的核心创新在于将“安全方向合成方式”从**静态拼接所有预定义关键词**改为**在每个时间步动态选择与提示引导最一致的有害类别**。这一设计解决了两个层面的冲突：
1. **跨类别方向冲突**：不同类别的安全方向在潜在空间和文本空间中均存在不一致甚至对立（Figure 2, Figure 6, Figure 7）。
2. **聚合衰减**：多类别聚合会显著削弱单类别安全方向的有效性，例如单独使用 sexual 方向时有害率为 3.2%，而 sexual+hate 组合上升至 5.8%（Table 1）。

![[assets/figures/papers/paper_list_l2364_https_arxiv_org_abs_2602_20880/figures/009_Figure_6.jpg]]
*Figure 6: Cross-Category Directional Conflict in latent space under sexual and hate prompts. Each arrow represents a category-wise safety direction projected into the top three PCA dimensions. Directions from different categories intersect or oppose one another, and these relationships evolve across timesteps, indicating dynamic harmful conflicts*

CASG 的类别识别机制不依赖外部文本分类器，而是直接从扩散模型的内部状态（潜在空间中的噪声预测方向或文本空间中的投影残差）中推断，因此能够适应生成过程中语义的动态演变。

## 实验与关键发现

### 核心发现：CASG 在多个安全基准上一致且显著地降低有害率

Table 2 汇总了 CASG 与现有安全防护方法在四个有害内容基准上的对比。CASG 分别与潜在空间安全引导方法 **SLD** 和文本空间安全引导方法 **SAFREE** 集成，形成 CASG+SLD 与 CASG+SAFREE 两个变体。

![[assets/figures/papers/paper_list_l2364_https_arxiv_org_abs_2602_20880/figures/006_Table_2.jpg]]
*Table 2: Comparison of text-to-image safeguard methods. Harmful rates (↓, lower is better; brackets show change relative to SDv1.5) are evaluated on four benchmarks. Image quality on COCO is measured by FID (↓, lower is better) and CLIP score (↑, higher is better). Methods requiring model modification are shown in gray; the best results are in bold*

在 I2P 基准上，CASG+SLD 将有害率从 SDv1.5 的 42.2% 降至 **10.2%**（降幅 32.0 个百分点），CASG+SAFREE 则从 SAFREE 的 20.0% 降至 **18.9%**。在 CoProv2 上，CASG+SLD 达到 **3.9%**（SDv1.5 为 28.2%），降幅达 24.3 个百分点。在 T2VSafetyBench 和 Unsafe-Diffusion 上，CASG+SLD 分别取得 **9.8%** 和 **9.8%** 的有害率。这些结果表明，CASG 的冲突消解机制在潜在空间安全引导上带来的增益尤为突出——因为潜在空间中的跨类别方向冲突比文本空间更为剧烈。

与需要模型修改的方法（表中灰色行）相比，CASG 作为免训练框架，在安全性上达到甚至超越了 **ESD**、**UCE**、**RECE** 等概念擦除方法，同时保持了与原始模型相当的图像生成质量。在 COCO 良性提示上，CASG+SLD 的 FID 为 19.3（SLD 为 18.9），CLIP Score 为 29.4（SLD 为 29.2），表明安全引导几乎不损害正常生成能力。

### 消融实验：动态类别选择是性能提升的关键

**与 LLM 辅助方法的对比。** Table 3 将 CASG+SLD 与两种基于外部语言模型的 SLD 变体进行对比：GPT-4o 辅助 SLD 和 QwenGuard 辅助 SLD，二者均使用 LLM 对提示进行有害类别分类后再施加对应安全引导。在 I2P 上，CASG+SLD 的有害率为 10.2%，优于 GPT-4o 辅助 SLD 的 11.6% 和 QwenGuard 辅助 SLD 的 14.0%。这一差距揭示了静态文本分类器的根本局限：提示的文本类别标签无法反映去噪过程中动态变化的语义状态，而 CASG 在潜在空间中的实时方向一致性检测能够更准确地捕捉当前生成状态下的主导有害类别。

**关键词变体的鲁棒性。** Table 8 测试了 CASG 在四种预定义有害关键词设置下的稳定性：默认关键词、同义词、抽象描述和详细描述。在 T2VSafetyBench 上，CASG+SLD 在所有设置下均一致降低了 ASR，且降幅稳定，表明 CaCI 模块的方向匹配机制对关键词的具体措辞不敏感——只要关键词的语义方向与有害类别大致对齐，CASG 即可正确识别主导类别。

**类别层面分析。** Table 9 给出了 I2P 数据集中各有害类别的详细降幅。CASG+SLD 在性内容（sexual）类别上实现了 -61.2% 的最大降幅，在非法活动（illegal activity）上降幅为 -26.7%。这两个类别正是多类别聚合中方向冲突最严重的类别（如 Figure 2 所示，sexual 方向与其他类别方向接近正交甚至反向），CASG 通过排除干扰方向，释放了被聚合衰减的单类别安全引导能力。

**推理效率。** Table 10 报告了 CASG 的推理时间开销。CASG+SLD 的延迟随有害类别数 k 线性增长，当 k=7 时，推理时间为原始 SLD 的 2.58 倍。这一开销来自 CaCI 模块在每个时间步对 k 个类别的方向评估，但仍属于轻量级，无需额外模型加载或参数更新。

### 定性分析：CASG 在强冲突场景下保持语义一致性

Figure 5 展示了不同安全方法在暴力和不当内容提示上的生成对比。CASG+SLD 在抑制有害视觉元素的同时，较好地保留了提示的非有害语义成分（如场景构图、人物姿态等），而直接聚合多类别关键词的 SLD 变体往往导致过度修正，使图像内容偏离原始提示意图。这与 CASG 仅沿单一主导类别施加安全引导的设计一致：避免多方向拉扯造成的语义漂移。

![[assets/figures/papers/paper_list_l2364_https_arxiv_org_abs_2602_20880/figures/008_Figure_5.jpg]]
*Figure 5: Comparison of T2I safety methods across different categories of harmful content. The rows show generation results for prompts related to violence and inappropriate content. Methods marked with * require parameter tuning or model modifications*

### 失败模式与局限

CASG 的性能边界主要体现在以下方面：

1. **预定义类别依赖。** CASG 的有害类别集合是预先定义的，对于不在集合中的新颖有害概念（如训练后新出现的敏感话题），CaCI 无法识别对应方向，安全引导可能失效。Table 8 的鲁棒性测试仅限于同义变体，未覆盖开放集有害概念。

![[assets/figures/papers/paper_list_l2364_https_arxiv_org_abs_2602_20880/figures/017_Table_8.jpg]]
*Table 8: ASR (%) under different predefined harmful keyword variants on T2VSafetyBench. Values in brackets denote the change relative to the base safeguard*

2. **推理延迟与类别数线性相关。** 当需要覆盖大量有害类别时，CASG+SLD 的延迟将成倍增长。Table 10 显示 k=7 时已为原始 SLD 的 2.58 倍，在实际部署中需要在安全覆盖范围与推理效率之间权衡。

![[assets/figures/papers/paper_list_l2364_https_arxiv_org_abs_2602_20880/figures/021_Table_10.jpg]]
*Table 10: Inference Efficiency Comparison. k denotes the number of predefined harmful categories. Values in brackets denote the inference time multiples relative to SAFREE and SLD*

3. **恶意输入上的语义偏移。** 对于明确有害的提示，CASG 为了安全引导会主动偏离原始语义，这种偏移在安全优先的场景中可接受，但在需要精确上下文保真度的应用中可能成为问题。该偏移的程度和可控性在论文中未做定量分析，需要进一步验证。

## 定位与知识库关联

### 安全生成方法的谱系

CASG 定位于文本到图像扩散模型的安全生成方法谱系中，属于**训练无关的推理时安全引导**分支。现有方法可根据干预机制分为三类：

**模型编辑方法**直接修改模型参数以擦除有害概念，包括 **ESD**、**UCE** 和 **RECE**。这类方法需要参数微调，干预后不可逆，且可能影响模型的通用生成能力。

**对齐式方法**如 **SafetyDPO**，通过对齐训练调整模型的行为偏好，但同样需要额外的训练过程。

**安全引导方法**在推理时通过调整去噪过程来抑制有害内容，无需修改模型参数。其中：
- **潜在空间引导**的代表 **SLD** 通过计算有害条件噪声与无条件噪声之差得到安全方向，在潜在空间中引导生成远离有害区域。
- **文本空间引导**的代表 **SAFREE** 将提示嵌入投影到有害子空间的正交补上，从文本层面移除有害成分。

CASG 属于安全引导方法的增强框架，以即插即用的方式嵌入现有引导机制，不引入额外训练开销。

### 核心改进：从静态聚合到动态对齐

现有安全引导方法在处理多类别有害内容时采用**静态关键词拼接**策略：将所有预定义有害类别的关键词合并为一个聚合条件，生成单一的安全方向。这种策略的根本缺陷在于：

1. **方向不一致**：不同类别的安全方向在潜在空间和文本空间中并非相互一致。PCA 可视化（Figure 2）显示，部分类别的方向相互交叉甚至反向，且这种关系随去噪时间步动态变化。
2. **方向衰减**：聚合多个类别会显著削弱单类别安全方向的有效性。定量分析（Figure 3）表明，性内容类别的安全方向在聚合后保留率明显降低，导致对该类别的抑制能力下降。
3. **错误引导风险**：当聚合方向与实际有害类别不匹配时，安全引导可能将生成过程推向其他有害区域。实验证据（Table 1）显示，对性内容提示施加仇恨类别的安全方向，有害率从基线的 67.2% 飙升至 72.4%，远高于使用正确性内容方向时的 3.2%。

CASG 的核心改进在于将**安全方向合成方式**从静态聚合转变为动态对齐：在每个去噪时间步，通过 Conflict-aware Category Identification (CaCI) 模块识别与当前生成状态最一致的有害类别，然后通过 Conflict-resolving Guidance Application (CrGA) 模块仅沿该单一类别施加安全纠正。这种设计的因果机制在于：安全引导方向是否与当前生成过程中的真实有害类别对齐，直接决定了安全干预的有效性。

### 适用边界与局限

CASG 的有效性建立在以下前提之上：

1. **预定义类别依赖**：CASG 需要预定义的有害关键词集合。对于不在集合中的新颖有害概念，CaCI 无法识别对应类别，安全引导可能失效。这是方法的核心局限，也是未来向开放集有害概念扩展的关键挑战。

2. **推理效率与类别数的权衡**：CASG+SLD 的推理时间随有害类别数 $k$ 线性增长。当 $k=7$ 时，延迟为原始 SLD 的 2.58 倍（Table 10）。虽然仍属轻量级，但在大规模部署中需要在覆盖类别数与推理开销之间做出权衡。

3. **恶意输入上的语义偏移**：CASG 在恶意输入上会引起一定的语义偏移以确保安全。在安全优先的部署场景中，这种偏移是可接受的，但可能影响上下文保真度。这与模型编辑方法面临的保真度-安全性权衡类似，但 CASG 的偏移发生在推理时，可通过调整引导强度灵活控制。

4. **对抗鲁棒性未验证**：动态类别选择机制基于余弦相似度或投影残差幅值，是否可能被精心设计的对抗性提示所欺骗，从而选择错误的安全方向，目前尚无实验验证。

### 开放问题

1. **开放集有害概念扩展**：CASG 能否摆脱对预定义类别标签的依赖，通过在线有害概念发现或零样本有害识别来覆盖未见过的新型有害内容？

2. **跨模态泛化**：该方法的核心思想——动态识别主导有害类别并施加对齐的安全引导——是否可推广到视频生成模型、音频生成模型或其他生成模态？不同模态的安全方向定义和冲突模式可能存在本质差异。

3. **对抗鲁棒性**：CaCI 的类别选择机制是否对对抗性提示具有鲁棒性？攻击者可能构造在文本空间与特定有害类别高度对齐但实际语义不同的提示，诱导错误的安全方向选择。

4. **最优类别粒度**：预定义有害类别的粒度和数量如何影响 CASG 的性能？过粗的粒度可能导致类别内冲突，过细的粒度则会增加推理开销。是否存在最优的类别划分策略？

## 原文 PDF

![[paperPDFs/CVPR_2026/When_Safety_Collides_Resolving_Multi_Category_Harmful_Conflicts_in_Text_to_Image_Diffusion_via_Adaptive_Safety_Guidance.pdf]]
