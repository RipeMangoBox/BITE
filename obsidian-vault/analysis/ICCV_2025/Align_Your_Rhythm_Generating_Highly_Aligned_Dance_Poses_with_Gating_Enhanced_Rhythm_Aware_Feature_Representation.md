---
title: Align Your Rhythm Generating Highly Aligned Dance Poses with Gating Enhanced Rhythm Aware Feature Representation
type: paper
paper_level: A
venue: ICCV
year: 2025
pdf_ref: paperPDFs/ICCV_2025/Align_Your_Rhythm_Generating_Highly_Aligned_Dance_Poses_with_Gating_Enhanced_Rhythm_Aware_Feature_Representation.pdf
project_link: https://danceba.github.io/
code_link: null
aliases:
- Align_Your_Rhyth
tags:
- ICCV_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/representation_self_supervised_transfer
core_operator: 通过三个创新设计干预瓶颈：①基于相位的节奏特征提取（PRE）显式解耦并增强节奏信息；②时间门控因果注意（TGCA）通过门控机制强化全局节奏注意力；③并行Mamba运动建模（PMMM）分离建模上身和下身运动，提升多样性。
primary_logic: 音乐STFT相位角天然编码周期性节奏特征，将其显式提取并与门控增强的交叉条件注意力融合，再结合并行Mamba的分离式序列建模，能够在保持高节拍对齐的同时显著提升运动多样性，打破了以往方法中节奏精度与多样性的权衡。
claims:
- 在AIST++测试集上，Danceba在节拍对齐（BAS 0.2714）和运动质量（FID_k 11.67）上均大幅领先现有最佳方法Bailando++（BAS 0.2423, FID_k 22.74），FID_k改善幅度达48.68%。
- 消融实验显示，去除PRE模块后FID_k恶化41.91%，Div_k下降14.86%，BAS下降10.96%，证明相位节奏提取是捕获节奏信息的关键。
- 去除TGCA同样引起FID_k和BAS显著退化，表明门控增强的全局注意力对节拍-舞蹈对齐必不可少。
- 采用单流Mamba替代并行Mamba导致FID_k上升67.02，FID_g上升60.40，验证了分离建模上下身对提升生成质量的必要性。
---

# Align Your Rhythm Generating Highly Aligned Dance Poses with Gating Enhanced Rhythm Aware Feature Representation

> [!tip] 核心洞察
> 音乐STFT相位角天然编码周期性节奏特征，将其显式提取并与门控增强的交叉条件注意力融合，再结合并行Mamba的分离式序列建模，能够在保持高节拍对齐的同时显著提升运动多样性，打破了以往方法中节奏精度与多样性的权衡。

| 字段 | 内容 |
|------|------|
| 中文题名 | 对齐节奏：门控增强节奏感知特征生成高度对齐舞蹈姿势 |
| 英文题名 | Align Your Rhythm Generating Highly Aligned Dance Poses with Gating Enhanced Rhythm Aware Feature Representation |
| 会议/期刊 | ICCV 2025 |
| Links | [Project](https://danceba.github.io/) · [paper](https://arxiv.org/abs/2503.17340) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/representation_self_supervised_transfer |
| Method | Danceba |
| Dataset | AIST++ |

> [!tip] 效果简介
> - AIST++ 上，FID_k ↓ 11.67 vs 22.74 (Bailando++) (-11.07 (-48.68%))；Div_k ↑ 8.52 vs 7.96 (Bailando++) (+0.56 (+7.0%))；Div_g ↑ 7.55 vs 6.49 (Bailando++) (+1.06 (+16.3%))。

## 概要

音乐驱动舞蹈生成的核心挑战在于实现舞蹈动作与音乐节拍的高度对齐，同时保持动作的自然性与多样性。现有方法普遍面临三个瓶颈：音乐节奏特征与语义特征高度耦合，缺乏显式节奏建模；交叉条件因果注意力仅捕捉局部对应，无法有效利用全局节奏结构；运动建模将上身和下身视为整体，忽视了上下身运动动态的独立性。

针对上述问题，本文提出 **Danceba** 框架，通过三个创新设计实现干预：① **基于相位的节奏特征提取（PRE）**——利用 STFT 相位角显式解耦并增强节奏信息；② **时间门控因果注意（TGCA）**——通过 SiLU 门控机制强化全局节奏注意力；③ **并行 Mamba 运动建模（PMMM）**——分离建模上身和下身运动，提升多样性。

核心洞察在于：音乐 STFT 相位角天然编码周期性节奏特征，将其显式提取并与门控增强的交叉条件注意力融合，再结合并行 Mamba 的分离式序列建模，能够在保持高节拍对齐的同时显著提升运动多样性，打破了以往方法中节奏精度与多样性之间的权衡。

在 AIST++ 测试集上，Danceba 在节拍对齐（BAS 0.2714）和运动质量（FID_k 11.67）上均大幅领先现有最佳方法 Bailando++（BAS 0.2423，FID_k 22.74），FID_k 改善幅度达 48.68%。消融实验进一步证实：移除 PRE 后 FID_k 恶化 41.91%、BAS 下降 10.96%；移除 TGCA 同样引起 FID_k 和 BAS 显著退化；采用单流 Mamba 替代并行 Mamba 导致 FID_k 上升 67.02。这些结果表明，节奏解耦、门控全局注意力和分离式运动建模三者协同作用，是实现高精度节拍对齐与高多样性舞蹈生成的关键。

音乐驱动的舞蹈生成旨在为给定的音乐片段自动合成逼真且富有表现力的3D舞蹈动作序列，是计算机视觉与图形学交叉领域的前沿课题，在虚拟人动画、游戏开发、影视制作及人机交互中具有广泛的应用前景。近年来，基于深度学习的生成模型在该任务上取得了显著进展，主流方法通常采用自回归Transformer架构，将舞蹈生成建模为给定音乐条件下的序列预测问题。

然而，现有方法在三个核心维度上存在系统性瓶颈，制约了生成舞蹈的艺术表现力与实用性。

**瓶颈一：节奏特征与语义特征的深度耦合。** 音乐信号同时承载着语义内容（如旋律、和声、乐器）和周期性节奏线索（如节拍、速度），二者在原始音频表征中高度纠缠。现有方法大多直接使用通用音频特征（如librosa提取的mel频谱或预训练音频模型的隐层表示）作为条件输入，缺乏对节奏信息的显式解耦与增强。如**Figure 2**所示，原始音乐特征中仅有少量成分包含有意义的音乐信息，呈现“节奏贫乏”特性；而经过短时傅里叶变换（STFT）后提取的相位特征，每个时间token均蕴含丰富的周期性结构，构成“节奏丰富”特征。这一观察揭示了显式节奏建模的必要性，但现有方法普遍忽视了相位域所编码的节拍先验。

**瓶颈二：交叉条件注意力仅捕捉局部对应，缺乏全局节奏约束。** 以**Bailando**（Siyao et al., CVPR 2022）及其增强版**Bailando++**（Siyao et al., TPAMI 2023）为代表的先进方法，采用交叉条件因果注意力（C3Attention）在音乐与舞蹈序列间建立条件依赖。然而，如**Figure 3(a)**的注意力热图所示，C3Attention主要聚焦于局部时间邻域的对应关系，无法为下一预测token提供清晰的全局控制信号，导致舞蹈动作趋于随机，节拍对齐精度受限。

**瓶颈三：运动建模将上下身视为整体，忽视部位动态的独立性。** 人体舞蹈中，上半身与下半身承载着截然不同的运动语义——下半身主导步态与位移，与节拍强相关；上半身则负责手势与姿态表达，自由度更高。现有方法将上下身特征拼接后输入统一的Transformer自注意力层，迫使模型在同一表征空间中同时处理两类异质动态，限制了生成舞蹈的自然性与多样性。

上述瓶颈共同导致了一个根本性的权衡困境：追求高节拍对齐往往以牺牲运动多样性为代价，反之亦然。**Danceba**正是在这一背景下提出，旨在通过相位节奏提取、门控全局注意力与并行部位建模三个维度的协同创新，打破节奏精度与运动多样性之间的固有张力。

## 核心方法与创新机理

Danceba 围绕“显式节奏解耦—门控全局对齐—分离式运动建模”三条主线，对现有音乐驱动舞蹈生成框架进行了系统性重构。其核心创新可归结为三个紧密协同的 changed slots，分别对应节奏特征提取、注意力机制和运动序列建模骨干的升级。

### 2.1 从耦合特征到显式节奏解耦：基于相位的节奏特征提取（PRE）

现有方法（如 **Bailando** (Siyao et al., CVPR 2022) 及 **Bailando++** (Siyao et al., TPAMI 2023)）直接使用原始音乐特征（如 librosa 提取的声谱图），音乐节奏信息与语义信息高度耦合，缺乏对节拍结构的显式建模。Danceba 提出 **Phase-Based Rhythm Extraction (PRE)** 模块，利用短时傅里叶变换（STFT）的相位角天然编码周期性节奏特征的特性，将节奏信息从音乐语义中解耦出来。

具体而言，PRE 对输入音乐特征 $\mathbf{m}$ 执行 STFT，提取相位角 $\varphi' = \mathrm{Angle}(\mathrm{STFT}(\mathbf{m}))$，经中心裁剪对齐时间维度后，通过线性变换、批归一化和 ReLU 激活得到节奏增强嵌入 $\mathbf{X}_\varphi$。这一设计的关键洞察在于：原始音乐特征中仅有少量 token 携带有效的音乐信息（节奏贫乏特征），而 STFT 相位角为每个 token 赋予了丰富的周期性节奏线索（节奏丰富特征），如 **Figure 2** 所示。消融实验提供了强因果证据：移除 PRE 后，FID_k 恶化 41.91%，Div_k 下降 14.86%，Beat Align Score 下降 10.96%（**Table 2**），证实相位节奏提取是捕获节拍信息的关键瓶颈干预点。

### 2.2 从局部因果注意到门控全局节奏对齐：时间门控因果注意（TGCA）

基线方法 **Bailando** 采用的交叉条件因果注意力（C3Attention）仅能捕捉音乐与舞蹈之间的局部对应关系，缺乏对全局节奏结构的有效利用，导致节拍对齐不佳。Danceba 将 C3Attention 升级为 **Temporal-Gated Causal Attention (TGCA)**，通过引入门控机制强化全局节奏注意力。

TGCA 的核心操作是将 C3Attention 的输出与一个 SiLU 门控信号逐元素相乘：

$$\mathrm{TGCA}(\mathbf{X}) = \mathrm{C}^3\mathrm{Attention}(\mathbf{X}) \odot \mathrm{SiLU}(\mathrm{Linear}(\mathbf{X}))$$

门控信号由特征自身的线性投影经 SiLU 激活产生，起到自适应筛选和增强节奏敏感特征的作用。注意力热图可视化（**Figure 3**）直观展示了这一改进的效果：原始 C3Attention 的热图缺乏清晰的全局控制信号，导致舞蹈动作趋于随机；而 TGCA 为下一预测 token 提供了明确的全局控制信号，使舞蹈动作与音乐节拍高度对齐。消融实验进一步验证：移除 TGCA 后 FID_k 和 BAS 均显著退化（**Table 2**），表明门控增强的全局注意力对节拍-舞蹈对齐不可或缺。

### 2.3 从整体建模到分离式并行运动生成：并行 Mamba 运动建模（PMMM）

现有方法通常将上身和下身运动特征拼接后统一送入自注意力层处理，忽视了上下身运动动态的独立性，限制了生成舞蹈的自然性和多样性。Danceba 引入 **Parallel Mamba Motion Modeling (PMMM)**，用两个并行的 Mamba 流分别独立建模上身和下身运动序列。

每个并行流由 Mamba 选择性状态空间块和 GateMlp 组成：

$$\mathbf{X}_{mb}' = \mathbf{Mamba}(\mathrm{RMSNorm}(\mathbf{X}_{attn})) + \mathbf{X}_{attn}$$
$$\mathbf{X}_{mb} = \mathbf{GateMlp}(\mathrm{RMSNorm}(\mathbf{X}_{mb}')) + \mathbf{X}_{mb}'$$

这一设计的因果逻辑在于：上身运动（如手臂摆动）和下身运动（如脚步移动）具有不同的节奏响应模式和运动自由度，分离建模使每个部位能独立学习其与音乐节奏的对应关系。消融实验提供了决定性证据：将并行 Mamba 替换为原始 Transformer 层导致性能大幅下降（**Table 2**）；采用单一 Mamba 架构（Danceba-Single）处理拼接后的上下身特征，相比并行版本 FID_k 上升 67.02，FID_g 上升 60.40（**Table 3**），充分验证了分离建模上下身对提升生成质量的必要性。

### 2.4 创新点协同机制

三个创新点并非孤立运作，而是形成了一条因果链路：**PRE** 从音乐中提取纯净的节奏信号，为后续模块提供精确的节拍约束；**TGCA** 利用门控机制将这一节奏信号转化为全局注意力控制，确保舞蹈动作与音乐节拍在时序上高度对齐；**PMMM** 在节奏对齐的约束下，通过分离式序列建模释放上下身运动的多样性潜力。这一设计打破了以往方法中“节奏精度-运动多样性”的固有权衡——在 Beat Align Score 提升 12.0% 的同时，Div_k 和 Div_g 分别提升 7.0% 和 16.3%（**Table 1**）。

Danceba 的整体设计遵循“节奏解耦—门控增强—分离建模”的三阶段流水线，其数据流与模块关系如 **Figure 1** 所示。系统输入为原始音乐波形与历史舞蹈姿势序列，输出为下一时刻的上身与下身姿势预测，最终通过预训练的 Pose VQ‑VAE 解码器恢复为连续 3D 舞蹈动作。

![[assets/figures/papers/paper_list_l1883_Align_Your_Rhythm_Generating_Highly_Aligned_Dance_Poses_with_Gating_Enha/figures/001_Figure_1.jpg]]
*Figure 1: The overall framework of Danceba consists of three core modules: Phase-based Rhythm Extraction (PRE), Temporal-Gated Causal Attention (TGCA), and Parallel Mamba Motion Modeling (PMMM). PRE precisely extracts rhythm-aware features from musical phase information, providing accurate rhythmic signals. These rhythm-enhanced music features are fused with pose embeddings (upperbody and lower-body poses) and processed through the TGCA module, which utilizes gating mechanism to reinforce rhythmic sensitivity and align dance movements accurately with music beats. Parallel Mamba Motion Modeling separately models upper and lower body motion sequences, effectively capturing distinct dance dynamics align...*

**输入与预处理。** 音乐端，原始波形经短时傅里叶变换（STFT）提取相位角，送入 **Phase‑Based Rhythm Extraction（PRE）** 模块，得到节奏增强的特征表示 $X_\varphi$。姿态端，历史舞蹈序列被两个独立的 Pose VQ‑VAE 编码器分别量化为上身姿势码 $p^u$ 和下身姿势码 $p^l$，再经线性嵌入映射至统一维度。

**节奏特征注入。** PRE 输出的 $X_\varphi$ 被复制三份，分别与原始音乐特征、上身嵌入、下身嵌入逐元素相加，形成节奏增强的音乐、上身、下身三支特征流。这一设计使得后续所有注意力与运动建模模块均在统一的节奏感知空间中运行，从源头解耦节奏与语义信息。

**门控增强的交叉条件注意力。** 三支节奏增强特征首先进入 **Temporal‑Gated Causal Attention（TGCA）** 的第一阶段。TGCA 在传统交叉条件因果注意力（C³Attention）的基础上，引入 SiLU 激活的门控机制，将注意力输出与门控信号逐元素相乘：
$$ \mathrm{TGCA}(\mathbf{X}) = \mathrm{C}^3\mathrm{Attention}(\mathbf{X}) \odot \mathrm{SiLU}(\mathrm{Linear}(\mathbf{X})). $$
门控信号为下一预测 token 提供清晰的全局节奏控制，有效抑制了原始 C³Attention 中因局部注意力导致的舞蹈动作随机化问题（参见 **Figure 3** 的热力图对比）。

**并行 Mamba 运动建模。** 经过第一阶段 TGCA 的特征被分流为上身和下身两条通路，分别进入 **Parallel Mamba Motion Modeling（PMMM）** 模块。每条通路包含一个 Mamba 选择性状态空间块与一个 GateMlp 块，二者均带有 RMSNorm 与残差连接：
$$ \mathbf{X}_{mb}' = \mathrm{Mamba}(\mathrm{RMSNorm}(\mathbf{X}_{attn})) + \mathbf{X}_{attn}, $$
$$ \mathbf{X}_{mb} = \mathrm{GateMlp}(\mathrm{RMSNorm}(\mathbf{X}_{mb}')) + \mathbf{X}_{mb}'. $$
并行 Mamba 独立建模上身与下身的运动动态，避免了传统单流 Transformer 将两者混为一谈所导致的信息耦合，从而显著提升动作的自然性与多样性。

**二次门控与预测头。** PMMM 输出的上身和下身特征再次汇合，经过 **TGCA 的第二阶段**进一步强化节拍‑舞蹈对齐。最终，两个独立的线性预测头将特征投影为姿势码的概率分布，通过 Softmax 选取最高概率的码字作为下一时刻的预测：
$$ \hat{p}_t^u = \arg\max_k \mathbb{P}(\mathbf{z}_k^u \mid \mathbf{m}_{1\ldots t}, p_{0\ldots t-1}^u, p_{0\ldots t-1}^l), $$
$$ \hat{p}_t^l = \arg\max_k \mathbb{P}(\mathbf{z}_k^l \mid \mathbf{m}_{1\ldots t}, p_{0\ldots t-1}^u, p_{0\ldots t-1}^l). $$
整个框架以交叉熵损失端到端训练：
$$ \mathcal{L}_{CE} = \frac{1}{T'} \sum_{t=0}^{T'-1} \sum_{h=u,l} \mathrm{CrossEntropy}(a_t^h, p_{t+1}^h). $$

**流水线总结。** Danceba 的完整前向过程可概括为：音乐相位提取 → 节奏特征注入 → 第一阶段 TGCA 全局节奏约束 → 并行 Mamba 分离建模上下身 → 第二阶段 TGCA 精炼对齐 → 双头预测下一姿态。三个核心模块 PRE、TGCA、PMMM 分别对应节奏解耦、全局注意力增强和分离式序列建模三个因果干预点，共同打破了既有方法中节拍对齐精度与运动多样性之间的权衡。

### 总体框架

Danceba 框架由三个核心模块构成：**基于相位的节奏特征提取（Phase-Based Rhythm Extraction, PRE）**、**时间门控因果注意（Temporal-Gated Causal Attention, TGCA）** 和 **并行 Mamba 运动建模（Parallel Mamba Motion Modeling, PMMM）**。PRE 从音乐相位信息中精确提取节奏感知特征，提供准确的节奏信号；节奏增强的音乐特征与上下身姿势嵌入融合后，经 TGCA 模块利用门控机制强化节奏敏感性，实现舞蹈动作与音乐节拍的精确对齐；PMMM 分别建模上身和下身运动序列，有效捕捉与节奏感知音乐特征对齐的差异化舞蹈动态，从而显著提升生成舞蹈的自然性、多样性和时间连贯性。

### 预备：姿势 VQ-VAE 编码与自回归生成

给定原始舞蹈姿势序列 $\mathbf{P}$，使用两个预训练的 Pose VQ-VAE 分别编码上身和下身运动：

$$
\mathbf{p}^u = \mathcal{F}_{VAE}^u(\mathbf{P}), \quad \mathbf{p}^l = \mathcal{F}_{VAE}^l(\mathbf{P}) \tag{1}
$$

其中 $\mathbf{p}^u, \mathbf{p}^l$ 分别为上身和下身的离散姿势码序列。在自回归生成阶段，模型在给定音乐特征 $\mathbf{m}_{1\ldots t}$ 和历史上下身姿势码的条件下，分别预测下一时刻的上身和下身姿势码：

$$
\hat{p}_t^u = \arg\max_k \mathbb{P}(\mathbf{z}_k^u \mid \mathbf{m}_{1\ldots t}, p_{0\ldots t-1}^u, p_{0\ldots t-1}^l) \tag{2}
$$

$$
\hat{p}_t^l = \arg\max_k \mathbb{P}(\mathbf{z}_k^l \mid \mathbf{m}_{1\ldots t}, p_{0\ldots t-1}^u, p_{0\ldots t-1}^l) \tag{3}
$$

自回归 Transformer $\mathcal{F}_{AR}$ 输出的概率分布为：

$$
\mathbf{a}^h = \operatorname{Softmax}(\operatorname{Linear}(\mathcal{F}_{AR}(\mathbf{X}_i))) \tag{4}
$$

训练采用上下身平均的交叉熵损失：

$$
\mathcal{L}_{CE} = \frac{1}{T'} \sum_{t=0}^{T'-1} \sum_{h=u,l} \mathrm{CrossEntropy}(\mathrm{a}_t^h, p_{t+1}^h) \tag{5}
$$

### 核心模块一：基于相位的节奏特征提取（PRE）

PRE 的核心洞察在于：音乐 STFT 的相位角天然编码了周期性节奏结构，而原始音乐特征中仅包含少量有意义的音乐信息（节奏贫乏特征）。PRE 通过解耦节奏与语义信息，显式提取节奏丰富的特征。

具体流程如下：

1. **STFT 相位提取**：对输入音乐特征 $\mathbf{m}$ 进行短时傅里叶变换，提取相位角：

   $$
   \mathbf{S}_m = \mathrm{STFT}(\mathbf{m}), \quad \varphi' = \mathrm{Angle}(\mathbf{S}_m) \tag{6}
   $$

2. **中心裁剪**：将相位时间维度裁剪至与目标序列长度 $T'$ 对齐：

   $$
   \varphi = \mathrm{CenterCrop}(\varphi') \tag{7}
   $$

3. **特征嵌入**：通过线性变换、批归一化和 ReLU 激活得到节奏嵌入 $\mathbf{X}_\varphi$：

   $$
   \mathbf{X}_\varphi = \mathrm{ReLU}(\mathrm{BN}(\mathrm{Linear}(\varphi))) \tag{8}
   $$

4. **节奏特征融合**：将 $\mathbf{X}_\varphi$ 复制后分别与原始音乐特征、上身特征、下身特征逐元素相加，得到节奏增强的特征表示。

### 核心模块二：时间门控因果注意（TGCA）

TGCA 旨在解决原始交叉条件因果注意（C3Attention）仅捕捉局部对应、无法有效利用全局节奏结构的问题。其关键设计是通过门控机制强化全局节奏注意力。

门控信号由 SiLU 激活的线性投影产生：

$$
\mathrm{Gating}(\mathbf{X}) = \mathrm{SiLU}(\mathrm{Linear}(\mathbf{X})) \tag{9}
$$

TGCA 的输出为 C3Attention 与门控信号的逐元素乘积：

$$
\mathbf{X}_{attn} = \mathrm{TGCA}(\mathbf{X}) = \mathrm{C}^3\mathrm{Attention}(\mathbf{X}) \odot \mathrm{Gating}(\mathbf{X}) \tag{10}
$$

注意力热图可视化（Figure 3）表明，TGCA 为下一预测 token 提供了清晰的全局控制信号，而原始 C3Attention 缺乏该信号，导致舞蹈动作随机。Danceba 在框架中两次应用 TGCA：首次在节奏特征融合后，第二次在 PMMM 处理后，以进一步强化节拍对齐。

### 核心模块三：并行 Mamba 运动建模（PMMM）

PMMM 的核心创新在于将上身和下身运动视为两个独立动态系统，分别用并行的 Mamba 流进行序列建模，打破了以往方法将上下身拼接后统一处理的局限。

每个 Mamba 流包含两个子层：

1. **Mamba 块**（带 RMSNorm 和残差连接）：

   $$
   \mathbf{X}_{mb}' = \mathbf{Mamba}(\mathbf{RMSNorm}(\mathbf{X}_{attn})) + \mathbf{X}_{attn} \tag{11}
   $$

2. **GateMlp**（门控 MLP 精炼）：

   $$
   \mathbf{X}_{mb} = \mathbf{GateMlp}(\mathbf{RMSNorm}(\mathbf{X}_{mb}')) + \mathbf{X}_{mb}' \tag{12}
   $$

上身和下身特征分别经过上述并行 Mamba 流处理后，再次通过 TGCA 增强节奏对齐，最终由预测头输出上下身姿势码的概率分布。

## 实验与关键发现

### 主实验结果

Danceba 在 AIST++ 测试集上与现有最佳方法进行了全面定量对比，结果如 Table 1 所示。在运动质量指标 FID_k 上，Danceba 达到 **11.67**，较最佳基线 Bailando++（22.74）**大幅降低 48.68%**，表明生成舞蹈的逼真度显著提升。在运动多样性方面，Danceba 的 Div_k 达到 **8.52**（提升 7.0%），Div_g 达到 **7.55**（提升 16.3%），打破了以往方法在质量与多样性之间的固有权衡。更为关键的是，在节拍对齐指标 Beat Align Score (BAS) 上，Danceba 取得 **0.2714**，较 Bailando++ 的 0.2423 **提升 12.0%**，证明了节奏感知特征表示对音乐-舞蹈精确对齐的核心作用。同时，FID_g 为 11.90，较 Bailando++ 降低 16.0%，保持了竞争力的整体运动质量。

![[assets/figures/papers/paper_list_l1883_Align_Your_Rhythm_Generating_Highly_Aligned_Dance_Poses_with_Gating_Enha/figures/004_Table_1.jpg]]
*Table 1: Comparison with state-of-the-art methods on the AIST++ dataset. Underlining indicates the best performance among existing methods. Blue indicates results that surpass the best existing method. ↓ indicates that lower values are better, while ↑ indicates that higher values are better*

对比的基线方法涵盖多种技术路线：基于交叉条件因果注意的 **Bailando** (Siyao et al., CVPR 2022) 及其增强版 **Bailando++** (Siyao et al., TPAMI 2023)、采用 MERT 预训练音频特征的 **Enhancing-Bailando** (Huang et al., ICASSP 2024)、显式节拍同步方法 **Beat-It** (Zheng et al., ECCV 2024)、扩散模型级联 **DiffDance** (Qi et al., ACMMM 2023)、粗到细扩散网络 **Lodge** (Li et al., CVPR 2024) 等。Danceba 在所有核心指标上均实现一致且显著的超越，验证了其设计有效性。

### 消融实验

为系统评估三个核心模块的贡献，进行了模块移除消融实验（Table 2）。

![[assets/figures/papers/paper_list_l1883_Align_Your_Rhythm_Generating_Highly_Aligned_Dance_Poses_with_Gating_Enha/figures/009_Table_2.jpg]]
*Table 2: Ablation study of three key modules (i.e., PRE, TGCA, and PMMM), and*

**去除 PRE 模块**（w/o PRE）导致 FID_k 恶化 41.91%，Div_k 下降 14.86%，BAS 下降 10.96%。这一结果表明，基于 STFT 相位角的节奏特征显式提取是捕获音乐周期性节拍信息的关键——仅依赖原始音乐特征无法提供足够的节奏约束，导致生成舞蹈的节拍对齐和运动多样性同时受损。

**去除 TGCA 模块**（w/o TGCA）同样引起 FID_k 和 BAS 的显著退化。这验证了门控增强的全局注意力机制对节奏-舞蹈对齐不可或缺：原始 C3Attention 仅捕捉局部对应关系，缺乏对全局节奏结构的有效利用，而 TGCA 通过 SiLU 门控与因果注意力的逐元素相乘，为下一预测 token 提供了清晰的全局控制信号（如 Figure 3 注意力热图所示），避免了舞蹈动作的随机漂移。

**去除 PMMM 模块**（w/o PMMM，替换为原始 Transformer 层）导致性能大幅下降，证实在运动序列建模中 Mamba 选择性状态空间模型相较于传统 Transformer 自注意力具有优势。

进一步地，Table 3 对比了并行 Mamba 架构（Danceba）与单一 Mamba 架构（Danceba-Single）。采用单流 Mamba 替代并行 Mamba 后，FID_k 上升 67.02，FID_g 上升 60.40。这一显著差距直接证明了分离建模上身和下身运动的必要性：上下身运动动态具有本质差异——下身主要承载节奏性步伐位移，上身则负责表现性姿态变化——统一建模会混淆两类运动模式，限制生成的自然性和多样性。

![[assets/figures/papers/paper_list_l1883_Align_Your_Rhythm_Generating_Highly_Aligned_Dance_Poses_with_Gating_Enha/figures/008_Table_3.jpg]]
*Table 3: Ablation study on parallel Mamba motion modeling, where Danceba-Single denotes our method using single Mamba architecture*

### 定性分析

Figure 3 的注意力热图对比直观揭示了 TGCA 的作用机制：原始 C3Attention 的热图分布较为均匀分散，缺乏明确的时序控制焦点；而 TGCA 的热图在下一预测 token 位置呈现高亮集中，表明门控机制有效强化了节奏关键时刻的注意力权重，为舞蹈生成提供了清晰的全局时序引导。

Figure 6 的节拍对齐可视化进一步量化了 Danceba 的优势：对比 Danceba 与 Bailando++ 在相同音乐片段上的运动节拍与音乐节拍距离，Danceba 生成的舞蹈动作节拍偏移明显更小，与音乐节奏的同步精度更高。

![[assets/figures/papers/paper_list_l1883_Align_Your_Rhythm_Generating_Highly_Aligned_Dance_Poses_with_Gating_Enha/figures/007_Figure_6.jpg]]
*Figure 6: Beats alignment visualization, where the horizontal axis shows frame indices of beat events. Comparing Danceba with Bailando++ [31], we can find that the distance between motion beats and music beats generated by our method is smaller. This indicating that Danceba performs better in terms of rhythmic alignment*

Figure 5 展示了与 Bailando 的定性对比，Danceba 生成的舞蹈在运动幅度和动作多样性上均有可见提升，与定量指标相互印证。

![[assets/figures/papers/paper_list_l1883_Align_Your_Rhythm_Generating_Highly_Aligned_Dance_Poses_with_Gating_Enha/figures/006_Figure_5.jpg]]
*Figure 5: Comparison with the state-of-the-art method Bailando [30]. Visual comparisons with Bailando can be found in the supplementary video*

### 失败模式与局限性

尽管 Danceba 在多个指标上取得领先，仍存在以下局限：

1. **音乐特征编码容量有限**：当前仅使用简单线性层对音乐特征进行编码，未采用预训练音频模型（如 Jukebox、MERT），可能无法充分捕捉细微的音乐结构和表现力线索，在复杂音乐片段上节奏-运动同步仍有提升空间。
2. **量化瓶颈**：姿势量化沿用 Bailando 的 Pose VQ-VAE 框架，离散码本空间有限，可能约束运动多样性的上限；量化效率与细粒度运动细节保留之间存在权衡，对于高表现力舞蹈风格，现有码本可能不足以覆盖全部运动模式。

以上局限指向进一步优化的方向：集成预训练音频编码器以增强音乐理解深度，探索层次化量化或自适应码本学习以突破运动表现力瓶颈。

## 定位与知识库关联

### 1. 与现有基线的继承与突破

Danceba 建立在音乐驱动舞蹈生成领域两条核心路线的交叉点上：**自回归离散姿态生成**与**节奏感知建模**。

**继承自 Bailando 系列的自回归框架。** Danceba 直接继承了 **Bailando**（Siyao et al., CVPR 2022）和 **Bailando++**（Siyao et al., TPAMI 2023）的核心架构：使用预训练的 Pose VQ-VAE 将舞蹈姿态离散化为上下半身码本，并通过自回归 Transformer 在音乐条件下逐帧预测下一姿态码。这一框架奠定了“离散码本+交叉条件注意力”的范式，但 Bailando 的交叉条件因果注意力（C3Attention）仅能捕捉局部音乐-运动对应，缺乏对全局节奏结构的显式建模，导致节拍对齐不足且运动多样性受限。

**节奏感知的深化：从隐式到显式解耦。** 在节奏建模方面，**Beat-It**（Zheng et al., ECCV 2024）尝试显式节拍同步，但 Danceba 更进一步，通过基于相位的节奏特征提取（PRE）将节奏信息从音乐语义中彻底解耦。PRE 利用 STFT 的相位角天然编码周期性节奏特征的特性（见 Figure 2 的可视化对比），将“节奏贫乏”的原始音乐特征转化为“节奏丰富”的相位特征，再通过中心裁剪和线性嵌入注入到音乐与姿态特征中。这一设计使得节奏信号成为独立可控的调制源，而非隐含在语义特征中的附属信息。

**注意力机制的改造：门控增强全局节奏感知。** Danceba 将 Bailando 的 C3Attention 改造为时间门控因果注意（TGCA），核心变化是在注意力输出上逐元素乘以 SiLU 门控信号。Figure 3 的热力图对比揭示了这一改造的本质效果：C3Attention 的注意力分布分散且缺乏清晰的全局控制信号，而 TGCA 为下一预测 token 提供了明确的全局节奏约束，避免了舞蹈动作的随机漂移。

**运动建模的分离：从统一到并行。** 现有方法（包括 Bailando、FACT、EDGE 等）普遍将上下半身特征拼接后统一处理，忽视了上下半身运动动态的根本差异。Danceba 的并行 Mamba 运动建模（PMMM）首次将上下半身分别交由两个独立的 Mamba 流处理，每个流包含 Mamba 选择性状态空间层和 GateMlp。这一设计使得上身（如手臂摆动）和下身（如脚步节奏）能够保持各自的时间动态特性，同时通过共享的音乐条件保持协调。

### 2. 在知识库中的定位

Danceba 处于**自回归离散姿态生成**与**状态空间序列建模**的交叉地带，其核心贡献在于通过三个协同设计的模块打破了节奏精度与运动多样性之间的既有权衡。

从技术谱系看，Danceba 的贡献可定位为：
- **相对于 Bailando/Bailando++**：继承其 VQ-VAE 离散化框架，但在节奏特征提取（PRE）、注意力机制（TGCA）和运动建模骨干（PMMM）三个关键槽位上进行了系统性改造。
- **相对于 Mamba 系列应用**：将 Mamba 的选择性状态空间建模引入舞蹈生成，并创新性地采用并行双流架构处理上下半身，这不同于标准的单流 Mamba 序列建模。
- **相对于扩散模型方法**（如 EDGE、DiffDance、Lodge）：Danceba 保持了自回归框架的推理效率优势，同时通过显式节奏建模在节拍对齐上实现了超越。

### 3. 适用边界与局限

**适用边界。** Danceba 的设计假设音乐具有明确的节拍结构，其 PRE 模块依赖 STFT 相位角的周期性特征。对于无节拍或节拍模糊的音乐（如环境音、自由节奏音乐），PRE 的有效性可能显著下降。此外，框架目前仅支持无条件音乐驱动生成，未引入风格标签或情感条件，限制了可控创作场景的应用。

**已知局限。**
1. **音乐特征编码的浅层性**：音乐特征仅通过简单线性层映射，未采用预训练音频模型（如 Jukebox、MERT、CLAP）。这可能导致细微音乐结构（如旋律轮廓、和声进行）的捕捉不充分，影响节奏-运动同步的细粒度表现。论文本身也指出这是未来改进方向。
2. **量化空间的表达力瓶颈**：姿态量化沿用 Bailando 的 Pose VQ-VAE 框架，编码空间有限。量化效率与表现力之间的权衡可能阻碍细粒度运动细节（如手指动作、面部朝向微调）的保留。消融实验（Table 2）显示，即使完整 Danceba 模型，在极端节拍场景下仍可能存在对齐偏差。
3. **长序列一致性未验证**：论文仅在 AIST++ 的短片段（约 10-15 秒）上评估，未测试长序列（如完整舞蹈编排）中的风格一致性和运动连贯性。GTN-Bailando 等方法专门针对长序列风格一致性设计，Danceba 在该场景下的表现尚待验证。

### 4. 开放问题

1. **预训练音频编码器的集成**：将 MERT、CLAP 等预训练音频模型作为音乐编码器，是否能进一步提升节奏-运动同步精度和运动表现力？这涉及预训练特征与相位特征的融合策略设计。
2. **层次化量化的探索**：采用层次化 VQ-VAE 或自适应码本学习，是否能在不牺牲推理效率的前提下扩大运动表示空间，提升运动质量和多样性？
3. **风格条件扩展**：如何将 Danceba 的节奏感知框架扩展到风格条件舞蹈生成？这需要在 PRE-TGCA-PMMM 管线中引入风格调制机制，同时保持节奏对齐能力不被稀释。
4. **跨数据集泛化**：Danceba 在 AIST++（专业舞者表演）上的优异表现能否泛化到更自由的舞蹈风格数据集（如 TikTok 舞蹈、社交舞）？不同数据分布下 PRE 的节奏提取鲁棒性需要进一步验证。
5. **实时交互生成**：当前框架为离线自回归生成，是否可以通过 Mamba 的高效推理特性实现实时音乐驱动舞蹈生成，支持现场表演或交互式应用？

## 原文 PDF

![[paperPDFs/ICCV_2025/Align_Your_Rhythm_Generating_Highly_Aligned_Dance_Poses_with_Gating_Enhanced_Rhythm_Aware_Feature_Representation.pdf]]
