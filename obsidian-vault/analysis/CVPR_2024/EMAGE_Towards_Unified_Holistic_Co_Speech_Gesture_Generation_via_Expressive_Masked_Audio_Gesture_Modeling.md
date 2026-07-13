---
title: "EMAGE: Towards Unified Holistic Co-Speech Gesture Generation via Expressive Masked Audio Gesture Modeling"
type: paper
paper_level: A
venue: CVPR
year: 2024
pdf_ref: paperPDFs/CVPR_2024/EMAGE_Towards_Unified_Holistic_Co_Speech_Gesture_Generation_via_Expressive_Masked_Audio_Gesture_Modeling.pdf
code_link: null
project_link: https://pantomatrix.github.io/EMAGE
aliases:
- EMAGE
tags:
- CVPR_2024
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 在训练中联合优化掩码姿态重建（MG2G）与音频条件生成（A2G），并通过掩码姿态提示（body hints）自适应融合音频节奏与内容特征，从而提升推理时的生成质量。
primary_logic: 将全身手势分解为四个独立的 VQ-VAE 隐空间进行建模，并设计可切换的交叉注意力机制，使模型能利用部分掩码姿态和音频信息生成连贯的全身动作。
claims:
- EMAGE 在 BEATv2 上显著降低 FGD（5.512 vs. 6.209 TalkSHOW），提升生成手势的真实性。
- 用户偏好度调查显示，EMAGE 在整体、身体和面部手势上分别获得 52.7%、44.7% 和 56.0% 的胜率，显著优于基线方法。
- 消融实验证明，组合式 VQ-VAE、内容-节奏注意力（CRA）和掩码姿态提示均能持续提升 FGD 和 BC。
- 多数据集训练（Trinity、AMASS）进一步降低了 FGD，验证了模型的扩展性。
---

# EMAGE: Towards Unified Holistic Co-Speech Gesture Generation via Expressive Masked Audio Gesture Modeling

> [!tip] 核心洞察
> 将全身手势分解为四个独立的 VQ-VAE 隐空间进行建模，并设计可切换的交叉注意力机制，使模型能利用部分掩码姿态和音频信息生成连贯的全身动作。

| 字段 | 内容 |
|------|------|
| 中文题名 | EMAGE：面向统一整体协同语音手势生成的表达性掩码音频手势建模 |
| 英文题名 | EMAGE: Towards Unified Holistic Co-Speech Gesture Generation via Expressive Masked Audio Gesture Modeling |
| 会议/期刊 | CVPR 2024 |
| Links |  [Project](https://pantomatrix.github.io/EMAGE)|
| Topic | #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation #topic/generative_models_diffusion/diffusion_image_video |
| Method | EMAGE |
| Dataset | BEATv2, User Study |

> [!tip] 效果简介
> - BEATv2 上，FGD (↓) 5.512 vs 6.209 (TalkSHOW) (-0.697)；BC (↑) 7.724 vs 6.947 (TalkSHOW) (+0.777)；Diversity (↑) 13.06 vs 13.47 (TalkSHOW) (-0.41)。
> - User Study 上，Holistic Preference Win Rate 52.7% vs 22.7% (Habibie et al.) (+30.0%)；Face Preference Win Rate 56.0% vs 33.0% (TalkSHOW) (+23.0%)。

## 概要

协同语音手势生成旨在从语音音频中合成与说话人节奏、语义相协调的身体与面部动作。该领域的核心瓶颈在于：现有方法要么仅处理面部或身体等局部运动，要么依赖单一 VQ-VAE 编码全身，无法在统一的网格层级上同时生成面部、身体、手部及全身运动，且难以结合用户指定的部分预定义姿态进行灵活生成。

针对上述问题，**EMAGE** 提出了一种基于表达性掩码音频手势建模的统一框架。其核心思路是将全身手势分解为四个独立的 VQ-VAE 隐空间（面部、上身、手部、下身）进行组合式建模，并通过**掩码姿态重建（MG2G）**与**音频条件生成（A2G）**的联合训练，使模型在推理时能利用任意关节与帧的掩码姿态提示（body hints），自适应融合音频节奏与内容特征，生成连贯的全身动作。

在方法论层面，EMAGE 首次将部分时空掩码姿态作为显式条件引入协同语音手势生成，并设计了可切换的交叉注意力机制与内容-节奏自注意力（CRA）模块，实现了音频特征与身体提示的有效解耦与融合。同时，EMAGE 配套发布了 **BEAT2**（BEAT-SMPLX-FLAME）数据集，这是目前最大的动作捕捉级、网格层级、整体协同语音手势数据集，包含 60 小时数据，为统一建模提供了数据基础。

实验结果表明，EMAGE 在 BEATv2 基准上全面超越现有方法：与最强基线 **TalkSHOW** 相比，FGD 从 6.209 降至 5.512，BC 从 6.947 提升至 7.724。用户偏好度调查进一步验证了其主观优越性——在整体、身体和面部手势上分别获得 52.7%、44.7% 和 56.0% 的胜率。消融实验证实，组合式 VQ-VAE、CRA 模块和掩码姿态提示均对性能有持续贡献，且模型在多数据集（Trinity、AMASS）训练下展现出良好的扩展性。

协同语音手势生成（Co-Speech Gesture Generation）旨在根据语音信号自动合成与说话内容、节奏和情感同步的身体动作与面部表情，是构建逼真虚拟人交互的核心技术。近年来，随着大规模数据集（如 BEAT）和深度学习方法的出现，该领域取得了显著进展。然而，现有方法仍面临三个根本性瓶颈，制约着整体手势生成的真实性与可控性。

**瓶颈一：缺乏统一的整体手势生成能力。** 现有方法通常将面部动画、身体姿态和手部动作视为独立任务分别建模。例如，**FaceFormer** 和 **CodeTalker** 专注于面部动画生成，**S2G** 和 **DisCo** 则仅处理身体手势。少数尝试整体生成的方法（如 **Habibie et al.** 的多解码器方案、**TalkSHOW** 的自回归全身生成）虽然整合了多个身体部位，但缺乏统一的网格级数据集支撑，且无法在统一的框架内灵活处理面部、身体、手部和下身的协同运动。Table 2 的系统对比表明，EMAGE 是首个接受音频与部分或完全掩码姿态输入、生成全身音频同步结果的方法。

**瓶颈二：缺乏高质量的网格级整体手势数据集。** 现有数据集（如 Trinity、AMASS）或仅覆盖局部身体，或依赖伪真值（Pseudo Ground Truth），在数据规模和标注精度上均存在不足。Table 1 的对比显示，此前最大的动捕数据集仅约 30 小时，且未同时提供 SMPL-X 身体参数和 FLAME 面部参数的网格级标注。这直接限制了整体手势生成模型的训练质量。

**瓶颈三：无法结合部分预定义姿态进行可控生成。** 实际应用（如虚拟人动画、游戏角色控制）中，用户往往希望提供部分关键姿态（如特定手势、站姿）作为约束，同时让模型自动补全其余动作并保持与音频的同步。然而，现有方法要么仅接受完整姿态序列进行自回归预测，要么仅依赖音频条件生成，缺乏对部分时空掩码姿态（任意关节与帧）的灵活融合能力。

针对上述瓶颈，EMAGE 提出了一套系统性的解决方案：首先构建了 BEAT2（BEAT-SMPLX-FLAME）数据集，提供 60 小时动捕级别的整体网格标注；其次设计了组合式 VQ-VAE 将全身手势分解为四个独立的隐空间进行建模；最后通过掩码音频手势 Transformer 联合训练掩码姿态重建（MG2G）与音频条件生成（A2G）两条路径，使模型在推理时能利用少量种子姿态（仅需 4 帧）生成连贯的全身动作。

## 核心方法与创新机理

EMAGE 的核心创新在于将“掩码姿态重建”作为训练约束，与“音频条件生成”联合优化，从而在推理时仅需极少的种子姿态（如 4 帧）即可生成连贯的全身协同语音手势。这一思想通过四个关键设计实现，直接改变了现有方法的多个技术槽位。

### 1. 组合式离散先验：从单一体素到四体解耦

现有全身手势生成方法（如 **TalkSHOW**）通常使用单个 VQ-VAE 编码整个身体的运动，导致不同部位（面部、手部、身体）的异质运动模式相互干扰。EMAGE 将全身手势分解为四个独立的 VQ-VAE 隐空间：**面部、上身、手部和下身**，分别进行量化与重建（Figure 4 右）。每个 VQ-VAE 的损失函数包含重建、速度、加速度和承诺损失：

$$\mathcal{L}_{\mathrm{VQ-VAE}} = \mathcal{L}_{rec}(\mathbf{g}, \hat{\mathbf{g}}) + \mathcal{L}_{\mathrm{vel}}(\mathbf{g}', \hat{\mathbf{g}}') + \mathcal{L}_{\mathrm{acc}}(\mathbf{g}'', \hat{\mathbf{g}}'') + \| \mathrm{sg}[\mathbf{z}] - \mathbf{q} \|^2 + \| \mathbf{z} - \mathrm{sg}[\mathbf{q}] \|^2$$

消融实验（Table 6）表明，组合式 VQ-VAE 相比单一 VQ-VAE 将 FGD 从 13.080 降至 7.397，降幅达 43.4%，证实了解耦量化对生成质量的因果性提升。

### 2. 掩码姿态提示：从纯音频条件到部分姿态引导

传统方法仅以音频为输入（如 **S2G**、**Trimodal**），或采用自回归方式依赖完整历史姿态（如 **TalkSHOW**）。EMAGE 首次接受**部分时空掩码的姿态**作为输入——任意关节、任意帧均可被掩码，掩码比例在训练中从 0 线性增长至 95%。掩码姿态通过空间卷积编码器（SC）和时间自注意力（TSA）生成“身体提示” $\mathbf{h}$：

$$\mathbf{h} = \mathcal{TSA}(\mathcal{SC}(\overline{\mathbf{g}}) + \mathbf{p}_t)$$

这一设计使模型在推理时既能利用可见姿态进行可控生成，又能在完全掩码时退化为纯音频生成。消融实验（Table 6）显示，引入掩码姿态提示将 FGD 从 6.833 进一步降至 5.423，BC 从 7.092 升至 7.568，证明身体提示对生成质量和节拍同步性的双重增益。

### 3. 内容-节奏自适应注意力：从简单相加到学习融合

现有方法通常将音频的节奏特征（onset、amplitude）与内容特征（文本词嵌入）简单相加。EMAGE 设计了**内容-节奏自注意力（CRA）**模块，通过学习注意力权重 $\boldsymbol{\alpha}$ 自适应融合两类特征：

$$\mathbf{f}_{1:T} = \boldsymbol{\alpha} \times \mathbf{r}_{1:T} + (1 - \boldsymbol{\alpha}) \times \mathbf{c}_{1:T}, \quad \boldsymbol{\alpha} = \mathrm{Softmax}(\boldsymbol{A}T(\mathbf{r}_{1:T}, \mathbf{c}_{1:T}))$$

这使得模型在不同帧能动态偏好节奏或语义信息，例如在重音时刻关注节奏，在叙述性语句中关注内容。消融实验（Table 6）表明，CRA 模块将 FGD 从 7.397 降至 6.833，验证了自适应融合优于简单相加。

### 4. 可切换交叉注意力与双路径训练：从单任务到联合掩码建模

EMAGE 的训练包含两条路径（Figure 3）：
- **MG2G（掩码姿态到姿态）**：纯姿态重建，通过交叉注意力解码器从身体提示 $\mathbf{h}$ 重建姿态隐变量 $\hat{\mathbf{q}}_{\mathrm{mg2g}} = \mathcal{TCAT}(\mathbf{h} + \mathbf{p}_t)$。
- **A2G（音频到姿态）**：融合音频特征与身体提示后重建姿态隐变量 $\hat{\mathbf{q}}_{\mathrm{a2g}} = \mathcal{TCAT}(\mathcal{TCA}(\mathbf{h} + \mathbf{p}_t, \mathbf{f}_{\mathrm{body}}), \overline{\mathbf{g}} + \mathbf{p}_t)$。

两条路径共享同一个**可切换交叉注意力**模块，在训练时根据路径选择不同的注意力源，在推理时则融合两者。这一设计与传统的纯音频条件生成形成根本差异：MG2G 路径迫使编码器学习鲁棒的身体运动先验，即使 95% 的姿态被掩码，仍能通过身体提示恢复合理的运动结构；A2G 路径则利用这些先验指导音频到姿态的映射。

此外，面部解码采用**直接拼接**而非交叉注意力：$\hat{\mathbf{q}}_{\mathrm{f}} = \mathcal{TCAT}(\mathbf{f}_{\mathrm{face}} \oplus \mathbf{h}, \mathbf{p}_t)$，避免了身体提示与面部音频特征在注意力空间中的不自然耦合，这一设计选择在 Figure 5 的架构对比中得到验证。

### 创新总结

| 技术槽位 | 基线方法 | EMAGE 创新 | 证据 |
|---------|---------|-----------|------|
| 量化解码空间 | 单一 VQ-VAE（TalkSHOW） | 四体组合式 VQ-VAE | FGD 13.080→7.397 |
| 输入姿态类型 | 无姿态或完整序列 | 部分时空掩码姿态 | FGD 6.833→5.423 |
| 音频特征融合 | 节奏与内容相加 | CRA 自适应注意力 | FGD 7.397→6.833 |
| 训练任务 | 仅音频条件生成 | 联合 MG2G + A2G | 整体框架消融 |
| 面部解码设计 | 共享交叉注意力 | 直接拼接后解码 | 架构对比验证 |

这些创新共同构成了 EMAGE 的因果性优势：掩码姿态建模提供了强健的运动先验，组合式 VQ-VAE 解耦了异质运动模式，CRA 实现了细粒度的音频-语义对齐，而双路径训练则将这些能力统一在一个端到端框架中。

EMAGE 的整体框架围绕一个核心设计展开：**在训练阶段联合优化掩码姿态重建（MG2G）与音频条件手势生成（A2G）两条路径，使模型在推理时能利用部分掩码姿态提示（body hints）显著提升生成质量**。该框架由四个关键阶段构成：组合式 VQ-VAE 隐空间建模、音频特征自适应融合、掩码音频手势 Transformer 主干网络，以及全局运动预测与解码。

### 组合式离散先验编码

与以往使用单一 VQ-VAE 编码全身运动的方法（如 TalkSHOW）不同，EMAGE 将全身手势显式分解为**面部、上身、手部和下身**四个独立部分，分别训练四个组合式 VQ-VAE（Figure 4 右）。每个 VQ-VAE 将对应部位的连续运动序列 $\mathbf{g}$ 编码为离散隐变量 $\mathbf{q}$，并通过以下损失联合优化：

$$\mathcal{L}_{\mathrm{VQ-VAE}} = \mathcal{L}_{rec}(\mathbf{g}, \hat{\mathbf{g}}) + \mathcal{L}_{\mathrm{vel}}(\mathbf{g}', \hat{\mathbf{g}}') + \mathcal{L}_{\mathrm{acc}}(\mathbf{g}'', \hat{\mathbf{g}}'') + \| \mathrm{sg}[\mathbf{z}] - \mathbf{q} \|^2 + \| \mathbf{z} - \mathrm{sg}[\mathbf{q}] \|^2$$

其中重建损失、速度损失和加速度损失共同约束运动学一致性，承诺损失（最后两项）确保编码器输出 $\mathbf{z}$ 与码本 $\mathbf{q}$ 的对齐。这种分解设计的动机在于：不同身体部位的运动与音频的关联程度存在本质差异——手势和唇动与语音高度耦合，而下身运动主要受物理平衡约束，与音频几乎无关。分离建模使每个 VQ-VAE 能专注于本部位的分布特性，避免跨部位信息混淆。

### 音频特征的自适应融合

音频特征提取分为两条并行支路：**语音节律特征**（onset 与 amplitude）和**语义内容特征**（预训练词嵌入）。EMAGE 设计了 Content-Rhythm Self-Attention（CRA）模块来自适应融合这两类特征（Figure 4 左）：

$$\mathbf{f}_{1:T} = \boldsymbol{\alpha} \times \mathbf{r}_{1:T} + (1 - \boldsymbol{\alpha}) \times \mathbf{c}_{1:T}, \quad \boldsymbol{\alpha} = \mathrm{Softmax}(\boldsymbol{A}T(\mathbf{r}_{1:T}, \mathbf{c}_{1:T}))$$

其中 $\boldsymbol{\alpha}$ 是通过节律特征 $\mathbf{r}$ 和内容特征 $\mathbf{c}$ 的交叉注意力学习到的帧级融合权重。这一设计的因果机制在于：**不同时刻的手势对音频的依赖维度不同**——节拍时刻需要更强的节律对齐，而语义手势（如指向、比喻动作）则更依赖内容特征。CRA 通过学习自适应权重，使模型能在帧级别动态调整融合比例。

### 掩码音频手势 Transformer 主干

主干网络 **Masked Audio Gesture Transformer** 包含三条处理流（Figure 3）：

1. **空间-时间编码器**：对输入的部分掩码姿态 $\overline{\mathbf{g}}$ 进行空间卷积编码（Spatial Convolutional Encoder, SC）和时间自注意力提炼（Temporal Self-Attention, TSA），生成身体提示特征 $\mathbf{h}$：
   $$\mathbf{h} = \mathcal{TSA}(\mathcal{SC}(\overline{\mathbf{g}}) + \mathbf{p}_t)$$

2. **MG2G 路径（掩码姿态重建）**：纯姿态到姿态的隐变量重建，通过时间交叉注意力 Transformer 解码器（TCAT）从身体提示直接预测目标隐变量：
   $$\hat{\mathbf{q}}_{\mathrm{mg2g}} = \mathcal{TCAT}(\mathbf{h} + \mathbf{p}_t)$$

3. **A2G 路径（音频条件生成）**：通过**可切换交叉注意力**（Switchable Cross-Attention）融合身体提示与音频特征后重建姿态隐变量：
   $$\hat{\mathbf{q}}_{\mathrm{a2g}} = \mathcal{TCAT}(\mathcal{TCA}(\mathbf{h} + \mathbf{p}_t, \mathbf{f}_{\mathrm{body}}), \overline{\mathbf{g}} + \mathbf{p}_t)$$

训练期间，掩码比例从 0 线性增长至 95%，迫使模型在极度稀疏的观测下学习鲁棒的身体提示编码。推理时，用户可提供任意关节、任意帧的部分姿态作为提示，模型通过 MG2G 路径编码身体提示，再通过 A2G 路径融合音频生成连贯的全身动作。

### 面部解码与全局运动预测

面部隐变量的解码采用**直接拼接策略**而非交叉注意力：将面部音频特征 $\mathbf{f}_{\mathrm{face}}$ 与身体提示 $\mathbf{h}$ 直接拼接后解码：
$$\hat{\mathbf{q}}_{\mathrm{f}} = \mathcal{TCAT}(\mathbf{f}_{\mathrm{face}} \oplus \mathbf{h}, \mathbf{p}_t)$$

这一设计选择（Figure 5 的架构对比）避免了交叉注意力可能导致的面部动作与身体提示的不自然耦合。此外，**Global Motion Predictor** 从下身局部运动 $\tilde{\mathbf{g}}_l$ 预测全局平移 $\tilde{\mathbf{t}}$，以减少足部滑动伪影：
$$\tilde{\mathbf{t}} = \mathcal{G}(\tilde{\mathbf{g}}_l)$$

### 框架设计的因果逻辑

EMAGE 整体框架的因果链条可概括为：**组合式 VQ-VAE 提供解耦的离散运动先验 → CRA 实现帧级自适应的音频特征融合 → 掩码姿态提示通过双路径训练赋予模型利用部分观测的能力 → 可切换交叉注意力与直接拼接解码在融合灵活性与部位独立性之间取得平衡**。这一设计使得 EMAGE 成为首个能接受音频与部分/完全掩码姿态、统一生成全身音频同步手势的框架（Table 2）。

### 组合式离散身体与面部先验

EMAGE 将全身手势显式解耦为四个独立部分——面部、上身、手部和下身——并为每个部分预训练独立的 VQ‑VAE，构成组合式量化先验。每个 VQ‑VAE 的编码器将对应身体部位的局部姿态序列 $\mathbf{g}$ 映射为连续隐变量 $\mathbf{z}$，随后通过最近邻查找将其量化为码本向量 $\mathbf{q}$：

$$q_i = \underset{q_i \in \mathbf{q}}{\arg\min} \| z_j - q_i \|^2$$

解码器从量化后的隐变量重建原始姿态。VQ‑VAE 的总损失由重建项、速度项、加速度项和承诺损失共同构成：

$$\mathcal{L}_{\mathrm{VQ\text{-}VAE}} = \mathcal{L}_{rec}(\mathbf{g}, \hat{\mathbf{g}}) + \mathcal{L}_{\mathrm{vel}}(\mathbf{g}', \hat{\mathbf{g}}') + \mathcal{L}_{\mathrm{acc}}(\mathbf{g}'', \hat{\mathbf{g}}'') + \| \mathrm{sg}[\mathbf{z}] - \mathbf{q} \|^2 + \| \mathbf{z} - \mathrm{sg}[\mathbf{q}] \|^2$$

其中 $\mathrm{sg}[\cdot]$ 表示停止梯度算子。速度损失 $\mathcal{L}_{\mathrm{vel}}$ 和加速度损失 $\mathcal{L}_{\mathrm{acc}}$ 分别约束相邻帧的一阶和二阶差分，迫使解码器输出平滑的运动序列。这种组合式设计的核心优势在于：各部位的量化空间相互独立，能够显式解耦与音频无关的本体运动模式，从而避免单一 VQ‑VAE 编码全身时不同部位运动统计特性相互干扰的问题。消融实验证实，组合式 VQ‑VAE 将 FGD 从单一 VQ‑VAE 的 13.080 大幅降至 7.397（Table 6）。

### 内容‑节奏自适应注意力

音频特征融合是协同语音手势生成的关键瓶颈。EMAGE 设计了内容‑节奏自注意力模块（Content‑Rhythm Self‑Attention, CRA），以自适应方式融合语音的节律特征 $\mathbf{r}_{1:T}$ 和语义内容特征 $\mathbf{c}_{1:T}$。节律特征提取自音频起始包络和幅度包络，内容特征则来自预训练的词嵌入。CRA 通过计算两种特征之间的交叉注意力权重矩阵 $\boldsymbol{A}$，生成逐帧的自适应融合系数 $\boldsymbol{\alpha}$：

$$\mathbf{f}_{1:T} = \boldsymbol{\alpha} \times \mathbf{r}_{1:T} + (1 - \boldsymbol{\alpha}) \times \mathbf{c}_{1:T}, \quad \boldsymbol{\alpha} = \mathrm{Softmax}(\boldsymbol{A}^T(\mathbf{r}_{1:T}, \mathbf{c}_{1:T}))$$

该机制使模型能够在不同时间步动态偏好节律或内容信息：在音频节拍点附近，$\boldsymbol{\alpha}$ 倾向于赋予节律特征更高权重，以驱动节拍对齐的手势；在语义关键词出现时，内容特征权重上升，引导生成语义感知的手势。消融实验表明，引入 CRA 模块可将 FGD 从 7.397 进一步降至 6.833（Table 6），验证了自适应融合相较于简单相加或拼接的显著增益。

### 掩码音频手势 Transformer 主干网络

EMAGE 的核心生成器是掩码音频手势 Transformer，其包含两条训练路径：掩码姿态重建（MG2G）和音频条件生成（A2G）。两条路径共享同一个主干网络，但通过可切换的交叉注意力层实现功能分化。

**身体提示编码。** 给定时空掩码后的姿态 $\overline{\mathbf{g}}$，模型首先用可学习的掩码嵌入替换被遮蔽的关节和帧，随后通过空间卷积编码器 $\mathcal{SC}$ 汇总各关节的空间特征，再经时间自注意力 $\mathcal{TSA}$ 提炼时序信息，并与位置编码 $\mathbf{p}_t$ 相加，生成身体提示 $\mathbf{h}$：

$$\mathbf{h} = \mathcal{TSA}(\mathcal{SC}(\overline{\mathbf{g}}) + \mathbf{p}_t)$$

身体提示 $\mathbf{h}$ 是 MG2G 和 A2G 路径的核心桥梁，它编码了可见姿态的结构和时序上下文，为后续生成提供强先验。

**MG2G 路径。** 在纯姿态重建任务中，掩码姿态的隐变量 $\hat{\mathbf{q}}_{\mathrm{mg2g}}$ 仅由身体提示经时间交叉注意力 Transformer 解码器 $\mathcal{TCAT}$ 重建：

$$\hat{\mathbf{q}}_{\mathrm{mg2g}} = \mathcal{TCAT}(\mathbf{h} + \mathbf{p}_t)$$

该路径迫使主干网络从部分观测中学习鲁棒的身体运动先验，即使在高掩码率（训练中线性增长至 95%）下也能恢复连贯的全身姿态。

**A2G 路径。** 在音频条件生成任务中，身体提示 $\mathbf{h}$ 首先与身体音频特征 $\mathbf{f}_{\mathrm{body}}$ 通过交叉注意力融合，再与掩码姿态的可见部分进行第二次交叉注意力，最终重建姿态隐变量 $\hat{\mathbf{q}}_{\mathrm{a2g}}$：

$$\hat{\mathbf{q}}_{\mathrm{a2g}} = \mathcal{TCAT}(\mathcal{TCA}(\mathbf{h} + \mathbf{p}_t, \mathbf{f}_{\mathrm{body}}), \overline{\mathbf{g}} + \mathbf{p}_t)$$

其中 $\mathcal{TCA}$ 表示时间交叉注意力层。这一设计的关键在于：身体提示 $\mathbf{h}$ 作为音频特征与姿态空间之间的中介，使音频信息能够以姿态感知的方式注入生成过程，而非简单地将音频特征与姿态特征拼接。Figure 5 的架构对比证实，这种选择性融合设计在自回归推理场景下显著优于直接融合和自注意力解码器方案。

![[assets/figures/papers/paper_list_l1847_EMAGE_Towards_Unified_Holistic_Co_Speech_Gesture_Generation_via_Expressi/figures/008_Figure_5.jpg]]
*Figure 5: Comparison of Forward Path Designs. Straightforward fusion module (a) merges audio features without refined body features and recombines audio features based only on position embedding. The Self-Attention decoder module (b), adopted in previous MLM models [17, 31], is limited for tasks requiring auto-regressive inference. Our design (c) considers effective audio feature fusion and auto-regressive decoding*

**面部解码。** 面部隐变量的解码采用直接拼接策略，将面部音频特征 $\mathbf{f}_{\mathrm{face}}$ 与身体提示 $\mathbf{h}$ 拼接后送入时间交叉注意力 Transformer：

$$\hat{\mathbf{q}}_{\mathrm{f}} = \mathcal{TCAT}(\mathbf{f}_{\mathrm{face}} \oplus \mathbf{h}, \mathbf{p}_t)$$

这种设计与身体部位的解码路径不同：面部动作与语音内容的耦合更为紧密，因此将音频特征与身体提示直接拼接，而非通过交叉注意力融合，有助于保留更丰富的语音‑面部关联信息。

### 全局运动预测器

从 VQ‑VAE 解码器获得局部身体姿态后，EMAGE 通过一个预训练的全局运动预测器 $\mathcal{G}$ 从下身局部运动 $\tilde{\mathbf{g}}_l$ 预测全局平移 $\tilde{\mathbf{t}}$：

$$\tilde{\mathbf{t}} = \mathcal{G}(\tilde{\mathbf{g}}_l)$$

该模块直接作用于下身关节的局部运动序列，输出对应的全局位移向量，从而有效减少生成结果中的滑步伪影。预测器独立于主干网络预训练，不参与 MG2G/A2G 的联合优化。

### 训练策略

训练过程中，时空掩码比例从 0 线性增长至 95%，迫使模型逐步适应从极稀疏观测中重建完整姿态。两条路径联合优化，MG2G 路径确保身体提示 $\mathbf{h}$ 编码足够丰富的姿态上下文，A2G 路径则利用这些提示引导音频条件生成。推理时，用户可提供任意关节和帧的部分掩码姿态作为身体提示，模型通过 A2G 路径生成与音频同步且与提示姿态一致的全身动作。

## 实验与关键发现

### 核心实验设置与公平性保障

为了公平评估 EMAGE 的性能，所有基线方法均在 BEAT2 数据集上进行了复现，并统一采用非自回归训练策略以获得最佳的 FLAME 参数表现。为消除对抗训练带来的抖动问题，基线的对抗训练组件被省略，且增加速度损失权重被证明无效。针对 **TalkSHOW**，额外为其添加了下身 VQ-VAE 以支持全身动作的比较。所有面部指标（MSE, LVD）均在 BEATv2 的相同顶点集上计算。

### 整体定量结果

在 BEATv2 基准上，EMAGE 在身体手势生成的核心指标上显著超越了现有方法。如 Table 4 所示，EMAGE 的 Fréchet Gesture Distance (FGD) 降至 **5.512**，相比 **TalkSHOW** 的 6.209 降低了 0.697，表明生成分布与真实分布更为接近。节拍一致性（BC）达到 **7.724**，比 TalkSHOW 的 6.947 提升了 0.777，证明其与音频节奏的同步性更强。在多样性指标上，EMAGE 为 13.06，略低于 TalkSHOW 的 13.47，但结合 FGD 来看，这种适度的多样性下降通常意味着生成结果更可控、更符合真实手势的分布模式。

![[assets/figures/papers/paper_list_l1847_EMAGE_Towards_Unified_Holistic_Co_Speech_Gesture_Generation_via_Expressi/figures/010_Table_4.jpg]]
*Table 4: Quantitative evaluation on BEATv2. We report FGD*

![[assets/figures/papers/paper_list_l1847_EMAGE_Towards_Unified_Holistic_Co_Speech_Gesture_Generation_via_Expressi/figures/012_Figure_7.jpg]]
*Figure 7: Comparison of Generated Facial Movements. Compared with previous state-of-the-art talking face generation methods FaceFormer [19] and CodeTalker [61] as well as holistic gesture generation methods Habibie et al. [28] and TalkSHOW [65]. Note that CodeTalker has higher MSE than EMAGE on BEATv2 (Table 4, lower is better) but is subjectively realistic. EMAGE gets good lip motions by leveraging both the face model and masked body hints*

在面部动作生成上，EMAGE 的 MSE 与 LVD 分别为 **7.680** 和 **7.556**，均优于 TalkSHOW 的 7.784 和 7.771，但需注意专用面部动画方法 **CodeTalker** 在 MSE 上仍具有优势。这一现象在 Table 7 的面部对比中也有体现——EMAGE 的面部生成受益于身体提示的融合，但在纯面部精度上尚未完全超越专用模型。

![[assets/figures/papers/paper_list_l1847_EMAGE_Towards_Unified_Holistic_Co_Speech_Gesture_Generation_via_Expressi/figures/014_Table_7.jpg]]
*Table 7: Training EMAGE on Multiple Datasets. EMAGE demonstrates flexibility by training on multiple datasets, even when only a subset of holistic gestures is available. This approach further improves the objective metrics on the BEATv1.3 test set*

### 用户偏好研究

主观评估（Table 5）进一步验证了 EMAGE 的感知优势。在整体手势偏好上，EMAGE 获得了 **52.7%** 的胜率，远超 **Habibie et al.** 的 22.7%。在身体手势上，EMAGE 以 **44.7%** 的胜率领先于 TalkSHOW 的 30.7%；在面部手势上，EMAGE 的胜率高达 **56.0%**，而 TalkSHOW 仅为 33.0%。这表明用户更倾向于认为 EMAGE 生成的动作更自然、更可信。

### 消融实验：组件贡献分解

Table 6 的消融分析系统性地揭示了各模块的因果贡献。基线模型使用单一 VQ-VAE 编码全身时，FGD 高达 13.080；替换为**组合式 VQ-VAE**（分别编码面部、上身、手部、下身）后，FGD 骤降至 7.397，降幅达 43.5%。这验证了将全身运动分解到独立隐空间进行建模是解决多部位运动耦合问题的关键。

![[assets/figures/papers/paper_list_l1847_EMAGE_Towards_Unified_Holistic_Co_Speech_Gesture_Generation_via_Expressi/figures/013_Table_6.jpg]]
*Table 6: Abliation Analysis on BEATv1.3*

在此基础上引入**内容-节奏注意力（CRA）**模块，FGD 进一步从 7.397 降至 6.833。CRA 通过学习自适应权重 $\boldsymbol{\alpha}$ 融合语音节律特征（onset/amplitude）与语义内容特征（预训练词嵌入），使模型能在不同帧动态调整对节奏或内容的偏好，从而生成更具语义感知能力的手势。

最后，加入**掩码姿态提示（Masked Hints）**——即在推理时提供部分可见的身体姿态作为条件——将 FGD 从 6.833 推至 **5.423**。这一结果表明，MG2G（掩码姿态重建）与 A2G（音频条件生成）的联合训练使模型学会了从稀疏姿态线索中提取鲁棒的身体提示 $\mathbf{h}$，并有效融合音频特征进行补全。

### 多数据集扩展与泛化性

Table 7 展示了 EMAGE 在多数据集上的灵活性。当仅使用 BEAT 数据训练时，FGD 为 5.423；引入 Trinity 数据集后降至 5.319；进一步加入 AMASS 后达到 **5.174**。值得注意的是，即使 Trinity 和 AMASS 仅包含身体运动而不含面部数据，模型仍能从中受益，证明了组合式 VQ-VAE 架构允许不同部位独立利用异构数据源进行训练。

### 数据集质量对比

BEAT2 数据集本身的质量优势在 Table 3 的用户偏好中得到了验证。在身体动作上，BEAT2 以 43.6% 的胜率显著优于 TalkSHOW 数据集的 14.4%，与 AMASS 动作捕捉数据（42.0%）持平。在面部动作上，BEAT2 以 35.7% 优于 TalkSHOW 的 26.1%。Table 8 进一步显示，BEAT2 在局部多样性和节拍同步性上均优于 TalkSHOW 数据集。

![[assets/figures/papers/paper_list_l1847_EMAGE_Towards_Unified_Holistic_Co_Speech_Gesture_Generation_via_Expressi/figures/015_Table_8.jpg]]
*Table 8: Diversity and BC Comparisons. The local and global diversity refers to the variance in joint positions with and without global translations, respectively*

### 失败模式与局限性

尽管整体性能领先，EMAGE 仍存在若干已知局限：

1. **面部精度瓶颈**：如 Table 4 所示，EMAGE 的面部 MSE 虽优于 TalkSHOW，但仍不及专用面部模型 **CodeTalker**。身体提示与面部音频特征的直接拼接（Equation 10）在某些情况下可能导致面部动作与身体姿态的不自然耦合。

2. **头部运动噪声**：BEAT2 数据集虽经过 MoSh++ 优化和硬编码物理规则精炼，但原始头盔标记仍可能引入头部运动噪声，需要大量人工约束进行修正。

3. **动态全局位移**：全局运动预测器 $\mathcal{G}$ 仅基于下身局部运动 $\tilde{\mathbf{g}}_l$ 预测全局平移，可能在高度动态场景（如跑步、快速转向）下产生滑步或预测偏差。

4. **场景泛化未验证**：当前模型仅针对单人独白语音场景训练，在多说话人对话、交互场景下的性能尚需进一步验证。

5. **掩码冲突处理**：当提供的掩码姿态提示与音频语义发生冲突时（例如音频表达“举手”而掩码姿态显示手部下垂），选择性融合机制的具体平衡策略尚不明确，可能导致生成结果出现语义不一致。

## 定位与知识库关联

### 1. 核心问题与瓶颈突破

现有协同语音手势生成方法长期面临三个结构性瓶颈：**（1）身体部位割裂**——面部、身体、手部运动通常由独立模型分别生成，缺乏统一的全身网格级建模；**（2）数据集缺失**——尚无同时提供高质量 SMPL-X 身体参数与 FLAME 面部参数的动捕级协同语音数据集；**（3）可控性不足**——主流方法仅接受音频输入，无法利用部分预定义姿态（如特定手势、朝向）引导生成。EMAGE 通过三项设计突破这些瓶颈：构建 BEAT2 数据集（60 小时动捕数据，经 MoSh++ 优化与手工物理规则精炼），将全身手势分解为四个组合式 VQ-VAE 隐空间（面部、上身、手部、下身），以及设计可切换交叉注意力机制实现掩码姿态提示与音频特征的自适应融合。

### 2. 与基线方法的关系定位

EMAGE 在输入模态、解码架构和训练范式上均与现有方法形成系统差异（Table 2）：

**（1）输入模态扩展**
- **FaceFormer** 与 **CodeTalker** 仅处理面部动画生成，输入仅有音频；EMAGE 同时接受音频与任意时空掩码的姿态提示（部分关节、部分帧），首次实现统一全身生成。
- **Habibie et al.** 采用多解码器架构分别生成身体和手部，但无面部输出；**TalkSHOW** 虽支持全身自回归生成，但仅依赖音频输入，缺乏姿态可控性。
- **CaMN**、**DiffStyleGesture**、**Trimodal**、**HA2G**、**DisCo**、**S2G** 等方法均聚焦于身体手势生成，未涉及面部或手部运动，且不接受掩码姿态作为条件。

**（2）解码架构差异**
- TalkSHOW 使用单一 VQ-VAE 编码全身运动，导致不同身体部位的耦合干扰；EMAGE 采用四个独立的组合式 VQ-VAE，分别量化解码面部、上身、手部和下身运动，显式解耦音频无关的姿态先验（Figure 4）。
- Habibie et al. 的多解码器设计虽支持不同部位，但各解码器独立训练，缺乏统一的跨部位特征融合机制。

**（3）训练范式创新**
- 现有方法普遍仅训练音频条件生成（A2G）任务；EMAGE 联合优化掩码姿态重建（MG2G）与音频条件生成（A2G）两条路径（Figure 3），使模型在训练阶段学习从部分姿态推断全身运动的鲁棒身体提示（body hints），推理时即使仅提供 4 帧种子姿态也能显著提升生成质量。

**（4）音频融合策略**
- 基线方法通常将语音节奏特征与内容特征简单相加；EMAGE 设计内容-节奏自注意力机制（CRA），通过学习的注意力权重自适应融合两者，使模型在特定帧能偏向语义感知手势或节奏同步动作。

### 3. 适用边界与限制

**（1）数据层面**
- BEAT2 数据集虽为目前最大的动捕级协同语音全身数据集（60 小时），但头部运动仍可能因头盔标记引入噪声，需大量人工物理约束进行修正（Section 3.2）。这限制了数据质量的完全自动化扩展。
- 数据集仅覆盖单人演讲场景，缺乏对话交互、多说话人场景的手势数据，模型在这类场景下的泛化能力尚未验证。

**（2）模型层面**
- 面部生成性能仍低于专用纯面部动画方法：CodeTalker 在 MSE 指标上优于 EMAGE（Table 4），表明身体提示与面部音频特征的融合可能导致面部动作的不自然耦合，尤其在唇动精度上仍有差距。
- 全局运动预测器仅基于下身局部运动预测全局平移，可能无法处理高度动态的全局位移（如跑步、跳跃），在需要大幅空间移动的场景中存在局限。
- 掩码比例在训练中线性增加至 95%，极高掩码率对生成多样性与重建保真度的长期影响尚不明确（消融实验仅在 BEATv1.3 上验证，Table 6）。

**（3）推理效率**
- 模型包含四个 VQ-VAE 解码器、空间-时间 Transformer 主干网络及全局运动预测器，实时应用场景下的推理速度与生成质量的平衡尚未系统评估。

### 4. 开放问题

1. **冲突融合机制**：当掩码身体提示与音频语义冲突时（例如掩码姿态指示静止，但音频语义要求挥手），可切换交叉注意力如何具体平衡两者权重？当前论文未提供冲突场景的定量分析。

2. **掩码策略的边界效应**：95% 的极高掩码比例在训练中是否会导致模型过度依赖身体提示，削弱纯音频条件生成（A2G）路径的独立能力？消融实验（Table 6）仅展示掩码提示的增益，未反向验证其对 A2G 路径的潜在抑制。

3. **模态扩展性**：当前框架假设身体提示来自掩码姿态，但能否无缝扩展至仅手部或仅面部的部分姿态输入？组合式 VQ-VAE 的设计是否支持任意子集的条件组合？

4. **多说话人泛化**：模型在单人演讲数据上训练，对话场景中的轮流发言、手势交互（如指向对方、共同节奏）等复杂动态是否可通过现有架构处理？

5. **实时部署权衡**：四个 VQ-VAE 解码器与 Transformer 主干网络的计算开销在实时应用中是否可接受？是否存在模型压缩或级联推理策略的空间？

### 5. 知识库定位

EMAGE 处于**协同语音手势生成**与**掩码建模**的交叉点，其方法论贡献可映射至以下知识节点：

- **离散运动先验**：继承自 CodeTalker 等方法的 VQ-VAE 运动量化思路，但将其从单一面部或身体扩展至组合式全身隐空间。
- **掩码自编码器（MAE）范式**：借鉴计算机视觉中 MAE 的掩码重建思想，将其适配至时序姿态数据，并通过联合训练将掩码重建能力迁移至条件生成任务。
- **音频-运动跨模态融合**：在 CaMN、DisCo 等方法的音频特征编码基础上，引入内容-节奏自适应注意力，提升语义感知手势的生成质量。
- **全身网格级建模**：整合 SMPL-X 身体模型与 FLAME 面部模型，填补了此前数据集（如 BEAT 仅提供骨架，TalkSHOW 使用伪真值）在网格级全身表示上的空白。

该方法为后续研究提供了两个可扩展方向：**（1）** 组合式 VQ-VAE 架构可作为多部位运动解耦的通用模板，支持更细粒度的部位分解（如左右手独立建模）；**（2）** 掩码姿态提示机制为交互式手势编辑、风格迁移和少样本自适应提供了统一的接口。

## 原文 PDF

![[paperPDFs/CVPR_2024/EMAGE_Towards_Unified_Holistic_Co_Speech_Gesture_Generation_via_Expressive_Masked_Audio_Gesture_Modeling.pdf]]
