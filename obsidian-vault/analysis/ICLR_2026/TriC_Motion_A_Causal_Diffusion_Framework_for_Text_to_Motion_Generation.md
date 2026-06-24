---
title: "TRIC-MOTION: TRI-DOMAIN CAUSAL MODELING GROUNDED TEXT-TO-MOTION GENERATION"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/TriC_Motion_A_Causal_Diffusion_Framework_for_Text_to_Motion_Generation.pdf
aliases:
- TM
- TRIC-MOTION
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 因果干预模块（CCMD）通过事实/反事实特征解缠，显式去除与运动无关的混淆特征，保留对动作生成有利的因果特征，从而稳定去噪过程并提升关键运动特征的建模能力。
primary_logic: 在扩散去噪框架中并行集成时间（TME）、空间（STM）和混合频率（HFA，DWT+FFT）建模，再通过得分指导的三域融合（S-Fus）进行信息整合，并在此基础上引入因果反事实运动解缠模块（CCMD），消去多域噪声，使生成动作同时具备时序一致性、骨骼拓扑合理性、全局运动趋势和细节动态，大幅提升语义对齐与逼真度。
claims:
- TriC-Motion 在 HumanML3D 上取得 R@1 0.612，显著优于第二名 SALAD 的 0.581。
- 去除混合频率分析（HFA）后，FID 从 0.347 恶化至 0.593。
- 去除因果干预模块（w/o CCMD）后，R@1 下降至 0.568，FID 上升至 0.561。
- 在 SnapMoGen 数据集上，TriC-Motion 的 R@1 达到 0.907，超越所有比较方法。
---

# TRIC-MOTION: TRI-DOMAIN CAUSAL MODELING GROUNDED TEXT-TO-MOTION GENERATION

> [!tip] 核心洞察
> 在扩散去噪框架中并行集成时间（TME）、空间（STM）和混合频率（HFA，DWT+FFT）建模，再通过得分指导的三域融合（S-Fus）进行信息整合，并在此基础上引入因果反事实运动解缠模块（CCMD），消去多域噪声，使生成动作同时具备时序一致性、骨骼拓扑合理性、全局运动趋势和细节动态，大幅提升语义对齐与逼真度。

| 字段 | 内容 |
|------|------|
| 中文题名 | TriC-Motion：基于三域因果建模的文本到动作生成 |
| 英文题名 | TRIC-MOTION: TRI-DOMAIN CAUSAL MODELING GROUNDED TEXT-TO-MOTION GENERATION |
| 会议/期刊 | ICLR 2026 |
| Links |  |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | TriC-Motion |
| Dataset | HumanML3D, SnapMoGen |

> [!tip] 效果简介
> - HumanML3D 上，R-Precision Top1 (R@1) 0.612（large） vs 0.581（SALAD） (+0.031)；FID 0.347（base） vs 0.032（LaMP） (+0.315（较 LaMP 高，但非最优；TriC-Motion 主要提升语义对齐指标）)；MM-Dist 2.463（base） vs 2.649（SALAD） (-0.186)。
> - SnapMoGen 上，R-Precision Top1 (R@1) 0.907 vs 0.802（MoMask++） (+0.105)；CLIP Score 0.675 vs 0.685（MoMask++） (-0.010)。

## 概述

### 问题瓶颈

文本到运动生成任务的核心挑战在于从自然语言描述中合成高质量、语义对齐的三维人体动作序列。现有方法大多聚焦于时间建模或空-时联合建模，但普遍存在一个深层瓶颈：缺乏对**空间、时间和频率三域的统一联合优化**。具体而言，纯时序模型（如基于Transformer的架构）难以显式维护骨骼拓扑的合理性；空-时联合方法虽然兼顾了关节空间关系，却忽略了运动信号在不同频率尺度上的差异化特征——全局运动趋势与局部细节动态往往被混为一谈。更关键的是，多域特征中混杂了大量**与运动语义无关的噪声和混淆信息**，这些无关特征在去噪过程中持续干扰生成质量，阻碍了语义对齐度和逼真度的进一步提升。

### 核心方法

TriC-Motion 针对上述瓶颈提出了两个层次的解决方案：

1. **三域并行建模与得分指导融合**：在扩散去噪框架内部，同时部署**时间运动编码（TME）**、**空间拓扑建模（STM）** 和**混合频率分析（HFA）** 三个并行的域专用模块。TME 通过 Transformer 捕捉时序依赖，STM 利用图卷积网络（GCN）维护关节拓扑合理性，HFA 则结合离散小波变换（DWT）与快速傅里叶变换（FFT）分别增强低频全局趋势和高频细节动态。三域特征通过**得分指导的三域融合模块（S-Fus）** 进行自适应加权整合，使生成动作同时具备时序一致性、骨骼拓扑合理性、准确的全局运动趋势和精细的局部动态。

2. **因果反事实运动解缠**：TriC-Motion 首次将因果干预引入运动生成，设计了**因果反事实运动解缠模块（CCMD）**。该模块从各域特征中分别提取因果贡献特征（事实特征）和混淆特征（反事实特征），通过有监督的因果干预 $do(\cdot)$ 显式消除与运动无关的噪声，保留对动作生成有利的因果信息。CCMD 仅在训练阶段使用，不增加推理开销。

### 主要结果

在主流基准 HumanML3D 上，TriC-Motion 取得了 **R-Precision Top-1 达到 0.612** 的新 state-of-the-art 结果，显著超越此前最优方法 SALAD（0.581），同时 MM-Dist 降至 2.463。在 SnapMoGen 数据集上，R@1 更是达到 0.907，以大幅优势领先所有对比方法。使用独立评估器 CLaM 进行跨空间验证时，TriC-Motion 依然保持领先，证明性能增益不依赖于特定评估特征空间。

消融实验进一步验证了各组件的关键作用：移除混合频率分析后 FID 从 0.347 恶化至 0.593；去除因果干预模块后 R@1 下降至 0.568、FID 上升至 0.561。值得注意的是，即使移除感知损失，模型仍以 R@1 0.585 超越 SALAD，表明核心增益来自三域建模与因果干预的架构设计本身，而非与评估器的耦合。

### 方法谱系与知识库定位

TriC-Motion 建立在扩散生成框架之上，以 **MDM**（Tevet et al., 2022）为基础去噪架构，但在建模域和特征处理机制上进行了根本性扩展。与仅依赖时序 Transformer 的 MDM 不同，TriC-Motion 引入了空间 GCN 和混合频率分析，形成三域并行架构。相较于近期强基线 **SALAD**（Hong et al., 2025）、**MoMask**（Guo et al., 2024）和 **StableMoFusion**（Huang et al., 2024a），TriC-Motion 的独特贡献在于**因果解缠机制的引入**——这是该领域首次将因果干预用于消除多域特征中的运动无关噪声。在频率建模方面，TriC-Motion 的 HFA 模块通过 DWT+FFT 的混合分解策略，区别于 **LaMP**（Li et al., 2024c）等仅关注单一频率维度的方法，实现了对低频全局趋势和高频局部细节的并行增强。总体而言，TriC-Motion 在三域联合建模与因果特征净化的交叉点上确立了新的技术路线。

## 背景与动机

### 问题背景

文本到动作生成（Text-to-Motion Generation）旨在根据自然语言描述合成逼真的三维人体运动序列，在动画制作、虚拟现实、游戏开发和人机交互等领域具有广泛应用。该任务的核心挑战在于：文本描述通常具有高度的语义抽象性，而人体运动则涉及复杂的时空动态、骨骼拓扑约束和多尺度运动模式，如何在两者之间建立精确的对齐是一个开放难题。

近年来，扩散模型在该领域取得了显著进展。以 **MDM**（Tevet et al., 2022）为代表的方法将运动生成建模为条件扩散去噪过程，通过 Transformer 架构捕捉运动序列的时间依赖关系。随后的一系列工作，如 **MoMask**（Guo et al., 2024）、**StableMoFusion**（Huang et al., 2024a）、**LaMP**（Li et al., 2024c）、**MotionPCM**（Jiang et al., 2025）以及 **SALAD**（Hong et al., 2025），分别在离散表示、稳定扩散、频率建模和融合先验等方面推动了性能边界的提升。

### 现有方法的瓶颈

尽管已有方法取得了可观进展，但深入审视可以发现一个根本性的建模盲区：**现有工作大多将注意力集中在时间建模或空-时联合建模上，缺乏对空间、时间和频率三个域的统一联合优化**。具体而言：

- **时间域**：以 Transformer 为核心的时序编码器能有效捕捉运动序列的长程依赖，但难以显式建模人体骨骼关节之间的空间拓扑关系。
- **空间域**：部分方法（如基于图卷积网络的工作）关注了关节层面的空间结构，但往往忽视了运动在不同时间尺度上的频率特性。
- **频率域**：人体运动天然包含不同频率成分——低频分量对应整体运动趋势和大尺度姿态变化，高频分量对应精细的局部动态和快速切换。现有方法要么完全忽略频率信息，要么仅对单一频段进行独立分析，未能实现高低频的协同增强。

更为关键的是，在多域特征建模过程中，**各域提取的特征中不可避免地混杂了与运动语义无关的噪声和混淆信息**。这些混淆特征可能来源于数据采集偏差、个体运动风格差异或文本描述中的非运动相关线索。现有方法缺乏显式的机制来分离这些运动无关特征，导致去噪过程受到干扰，生成的运动在语义对齐度和视觉逼真度上均受到制约。

### 本文动机

针对上述瓶颈，本文提出 **TriC-Motion**——一个基于三域因果建模的文本到动作生成框架。其核心动机体现在两个层面：

1. **三域统一建模**：在扩散去噪框架中并行集成时间建模（Temporal Motion Encoding, TME）、空间拓扑建模（Spatial Topology Modeling, STM）和混合频率分析（Hybrid Frequency Analysis, HFA），通过得分指导的三域融合机制（Score-guided Tri-domain Fusion, S-Fus）实现信息的自适应整合，使生成动作同时具备时序一致性、骨骼拓扑合理性、全局运动趋势和细节动态。

2. **因果反事实解缠**：首次将因果干预引入运动生成领域，设计因果反事实运动解缠模块（Causality-based Counterfactual Motion Disentangler, CCMD），通过事实/反事实特征提取和有监督因果干预，显式消除各域特征中与运动无关的混淆成分，保留对动作生成有利的因果特征，从而稳定去噪过程并提升关键运动特征的建模能力。

通过在 HumanML3D 和 SnapMoGen 两个基准数据集上的系统验证，TriC-Motion 在语义对齐核心指标 R-Precision Top1 上取得了 0.612（HumanML3D）和 0.907（SnapMoGen）的领先结果，证明了多域因果建模策略的有效性。

## 核心创新

TriC-Motion 针对现有文本到动作生成方法的核心瓶颈——多域特征中混杂运动无关噪声、缺乏空间-时间-频率三域统一优化——提出了两项关键创新：**三域并行建模与得分指导融合**，以及**因果反事实运动解缠**。

### 1. 三域并行建模与得分指导融合

现有方法多局限于单一时间建模（如 **MDM**（Tevet et al., 2022）的纯 Transformer）或空-时联合建模，忽略了频率域中蕴含的全局运动趋势与局部细节动态。TriC-Motion 首次在扩散去噪框架内并行集成三个互补的建模域：

- **时序运动编码（Temporal Motion Encoding, TME）**：沿时间维度应用标准 TransformerEncoderLayer，捕捉短程与长程时序依赖。
- **空间拓扑建模（Spatial Topology Modeling, STM）**：利用 3 层图卷积网络（GCN）在关节维度建模，保持骨骼拓扑合理性。
- **混合频率分析（Hybrid Frequency Analysis, HFA）**：结合离散小波变换（DWT）与快速傅里叶变换（FFT），先通过 DWT 分解出低频子带与高频子带，再对低频子带进行 FFT 获取全局频谱；低频分支采用空间-时间自适应注意力增强关键运动模式，高频分支则通过轻量级深度可分离卷积保留精细动态细节。

三域特征通过**得分指导的三域融合模块（Score-guided Tri-domain Fusion, S-Fus）**进行自适应整合。S-Fus 同时计算运动评分与语义评分，生成各域的注意力权重，加权融合后送入文本信息注入模块（TIJ），确保生成动作同时具备时序一致性、骨骼拓扑合理性、准确的全局运动趋势与细粒度动态。

消融实验表明，逐步添加 STM、HFA 和 S-Fus 持续提升各项指标，完整三域融合在 HumanML3D 上取得 R@1 0.607（Table 3）。其中 HFA 的低频与高频分支缺一不可——去除高频分支使 FID 从 0.347 恶化至 0.504，去除低频或关节内频率分支同样显著损害性能（Table 3）。

### 2. 因果反事实运动解缠

这是 TriC-Motion 最具区分度的创新：首次将因果干预引入运动生成。其核心动机在于，多域特征中混杂了与运动无关的混淆特征（如骨骼长度偏差、静态姿态偏好），这些噪声阻碍高质量动作的生成。

**因果反事实运动解缠模块（Causality-based Counterfactual Motion Disentangler, CCMD）**通过轻量级对称架构，从各域特征 $F_j^i$ 中分别提取因果贡献 $E_j^i$ 与混淆特征 $C_j^i$，随后执行有监督因果干预：

$$\tilde{F}_j^i = W_{do} E_j^i - W_{do} C_j^i$$

即从因果特征中显式减去反事实混淆特征，消除运动无关噪声。CCMD 仅用于训练阶段，通过逐层的事实/反事实损失 $\mathcal{L}_{fcf}$ 约束其输出逼近真实运动，迫使模块去除混淆信息。

消融实验验证了 CCMD 的关键作用：去除 CCMD 后，R@1 从 0.607 下降至 0.568，FID 从 0.347 上升至 0.561（Table 4）。进一步分析表明，CCMD 同时作用于时空频三域并应用于 S-Fus 之后效果最优；仅在时域或空-时域施加因果干预均不及全三域（Table 4）。t-SNE 可视化（Figure A1）也证实，因果解缠后的特征 $F_{tde}$ 在语义空间中具有更清晰的可分性。

值得注意的是，移除感知损失后，TriC-Motion 仍以 R@1 0.585 超越先前 SOTA **SALAD**（Hong et al., 2025）的 0.581（Table A4），说明核心增益来自三域建模与因果干预，而非与特定评估器的耦合。使用独立评估器 CLaM 的跨空间验证进一步确认了这一结论（Table A5）。

### 创新总结

相对于以 MDM 为代表的纯时序建模基线和以 SALAD、MoMask 为代表的近期强方法，TriC-Motion 的 changed slots 清晰聚焦于两点：**建模域从单一/双域扩展至时间-空间-频率三域并行**，以及**引入因果反事实机制主动消除多域混淆噪声**。这两项设计相互增强——三域建模提供了更丰富的特征空间，而 CCMD 确保这些特征中仅保留对运动生成有益的因果成分，从而在 HumanML3D 上取得 R@1 0.612（large）的 SOTA 性能，并在 SnapMoGen 上以 R@1 0.907 大幅超越所有对比方法（Table 2）。

## 整体框架

TriC-Motion 的整体框架围绕一个核心设计展开：在扩散去噪过程中，对运动序列同时进行**时间、空间、频率**三个域的并行建模，并通过**因果干预**显式消除多域特征中混杂的运动无关噪声。整个系统由堆叠的 TriC-Motion 去噪块构成，每个块内依次完成域内建模、三域融合、文本注入和因果解缠，最终输出干净的运动序列。

### 推理流程

如图 3(a) 所示，推理过程从随机噪声开始，经过 $T$ 步迭代去噪。每一步将当前带噪运动特征 $X_j$ 送入一个 TriC-Motion 去噪块，该块内部执行以下操作（式 1）：

1. **三域并行建模**：$X_j$ 同时被送入时间运动编码（TME）、空间拓扑建模（STM）和混合频率分析（HFA）三个模块，分别提取时间域特征 $F_j^{temp}$、空间域特征 $F_j^{spa}$ 和频率域特征 $F_j^{freq}$。
2. **得分指导三域融合（S-Fus）**：三域特征通过运动评分和语义评分机制计算注意力权重，自适应融合为统一的运动表示。
3. **文本信息注入（TIJ）**：融合后的特征通过交叉注意力与文本词级特征 $\tau$ 交互，增强语义一致性。
4. **因果反事实运动解缠（CCMD）**：仅在训练阶段，CCMD 模块从各域特征中提取因果贡献和混淆特征，通过有监督干预消除运动无关噪声，优化去噪过程。

经过 $J$ 层（默认 $J=4$）去噪块处理后，最终输出预测的干净运动序列 $\hat{X}$。

### 训练流程

训练时，TriC-Motion 采用扩散预测范式，直接回归干净运动 $x_0$（式 9）。总损失函数（式 11）由三部分组成：

- **简单扩散损失 $\mathcal{L}_{\text{simple}}$**：约束去噪输出逼近真实运动。
- **因果干预损失 $\mathcal{L}_{fcf}$**：逐层约束 CCMD 的因果解缠输出逼近真实运动，迫使模块消除混淆信息（式 10），层次权重设为 $\{0.1, 0.2, 0.3, 0.4\}$。
- **感知损失 $\mathcal{L}_p$**：利用预训练运动编码器提取特征，提升生成运动的感知质量。

权重设置为 $\lambda_{fcf}=1$，$\lambda_p=10$。

### 模块间数据流

各模块间的连接关系如下（图 3(b)、图 4）：

- **TME** 使用标准 TransformerEncoderLayer 沿时间维度建模，捕捉短程和长程时序依赖。
- **STM** 使用 3 层图卷积网络（GCN）沿关节维度建模，保持骨骼拓扑合理性。
- **HFA** 先用离散小波变换（DWT）分解出低频子带和高频子带，再对低频子带进行快速傅里叶变换（FFT）获取全局频谱；低频分支通过自适应注意力增强全局运动趋势，高频分支通过深度可分离卷积增强局部细节动态。
- **S-Fus** 以 TME、STM、HFA 的输出和 CLS token 为输入，通过运动评分分支 $f_{mot}$ 和语义评分分支 $f_{sem}$ 生成三域注意力权重 $\alpha_i$，加权融合后与原始输入 $X_j$ 拼接并线性投影（式 7）。
- **TIJ** 在 S-Fus 之后，通过交叉注意力将文本特征注入运动表示。
- **CCMD** 作用于 S-Fus 之后、TIJ 之前，从各域特征中通过对称的事实/反事实模块分别提取因果贡献 $E_j^i$ 和混淆特征 $C_j^i$，执行 $W_{do}E_j^i - W_{do}C_j^i$ 的因果干预，仅在训练时使用。消融实验证实，将 CCMD 置于 S-Fus 之后（post）优于置于其前（pre），且同时作用于时间、空间、频率三域效果最优（Table 4）。

### 设计动机

现有运动生成方法多关注时间或空-时联合建模，缺乏对空间、时间和频率三域的统一联合优化。更关键的是，多域特征中混杂了与运动无关的噪声（如骨骼拓扑偏差、频率域伪影），这些混淆特征阻碍了高质量动作的生成。TriC-Motion 通过三域并行建模 + 得分指导融合 + 因果反事实解缠的组合策略，使生成动作同时具备时序一致性、骨骼拓扑合理性、全局运动趋势和细节动态，在语义对齐指标上取得显著提升。

### 补充图表

![[assets/figures/papers/paper_list_l1907_TriC_Motion_A_Causal_Diffusion_Framework_for_Text_to_Motion_Generation/figures/003_Figure_3.jpg]]
*Figure 3: Overview of TriC-Motion. (a) Sampling process with stacked TriC-Motion Denoiser Blocks. (b) Overall architecture of the TriC-Motion framework*

## 核心模块与公式推导

### 整体框架与三域去噪块

TriC-Motion 的去噪器由 $J$ 层结构相同的 TriC-Motion Denoiser Block 堆叠而成。在第 $j$ 层、时间步 $t$，运动特征 $X_j$ 被并行送入三个域专用建模模块——时间运动编码（TME）、空间拓扑建模（STM）和混合频率分析（HFA），分别提取时域、空域和频域的特征 $F_j^{temp}$、$F_j^{spa}$ 和 $F_j^{freq}$。随后，得分指导的三域融合模块（S-Fus）将三域特征自适应整合，再通过文本信息注入（TIJ）以交叉注意力将文本词级特征 $\tau$ 注入融合后的运动特征。完整的 $J$ 层计算流程定义为：

$$
\left\{ \begin{array}{ll} \mathrm{TIJ}(X_j, \tau) = \mathrm{CrossAttention}(X_j, \tau, \tau) \\ \hat{X} = [ \mathrm{TIJ}( \mathrm{S\text{-}Fus}( \mathrm{TME}(X_j), \mathrm{STM}(X_j), \mathrm{HFA}(X_j), CLS ), \tau ) ] ||_{j=1}^{J} \end{array} \right.
$$

其中 $CLS$ 为文本全局语义标记，$||$ 表示逐层串联。这一并行三域架构确保了时序一致性、骨骼拓扑合理性、整体运动趋势与细节动态的联合建模（见 Figure 3）。

### 时间运动编码（TME）

TME 沿时间维度对运动帧序列施加标准的 TransformerEncoderLayer，捕捉短程和长程时序依赖：

$$
F_{j}^{temp} = \mathrm{TransformerEncoderLayer}(X_{j})
$$

该模块直接继承自 MDM（Tevet et al., 2022）的时序建模思想，但在 TriC-Motion 中仅作为三域之一，与空间和频率分支协同工作。

### 空间拓扑建模（STM）

STM 在关节维度上利用 3 层图卷积网络（GCN）保持骨骼拓扑的合理性，并引入残差连接以稳定训练：

$$
F_{j}^{spa} = X_{j} + [\mathbf{LN}(\mathbf{GELU}(\mathbf{GCN}(X_{j})))] ||^{3}
$$

其中 $\mathbf{LN}$ 为 LayerNorm，$\mathbf{GELU}$ 为激活函数，$||^{3}$ 表示 3 层级联。GCN 的邻接矩阵基于人体骨骼的自然连接关系构建，使模型显式感知关节间的空间约束。

### 混合频率分析（HFA）

HFA 是 TriC-Motion 的核心创新之一，结合离散小波变换（DWT）和快速傅里叶变换（FFT）实现混合频率建模。首先利用 DWT 将运动特征分解为低频子带 $\hat{S}_{LF}$ 和高频子带 $S_{HF}$，再对低频子带进行 FFT 以获取全局频谱：

$$
(\hat{S}_{LF}, S_{HF}) = \mathrm{DWT}(X_j), \quad S_{LF} = \mathrm{FFT}(\hat{S}_{LF})
$$

**低频分支**：在频域中利用空间-时间自适应注意力增强关键运动模式。通过可学习的时间权重 $\bar{w}_{t}$ 和空间权重 $w_{s}$ 对频谱 $S_{LF}$ 进行加权调制，再经线性变换和残差连接得到增强后的低频特征：

$$
\dot{S}_{LF}^{\prime} = \dot{S}_{LF} + \mathrm{Linear}(S_{LF} \otimes (\bar{w}_{t} \otimes w_{s}))
$$

其中 $\otimes$ 表示逐元素乘法，$\dot{S}_{LF}$ 为 FFT 后的复频谱表示。该分支负责捕捉整体运动趋势和全局节奏。

**高频分支**：通过轻量级深度可分离卷积增强高频细节，保持关节级精细动态：

$$
S_{HF}^{\prime} = S_{HF} + \mathrm{GELU}(\mathrm{GN}(f^{p}(f^{d}(S_{HF}))))
$$

其中 $f^{d}$ 为深度卷积，$f^{p}$ 为逐点卷积，$\mathrm{GN}$ 为 GroupNorm。高频分支确保局部快速运动和细微姿态变化不被丢失。

HFA 的详细架构见 Figure 4(a-c)。消融实验（Table 3）表明，低频和高频分支缺一不可：去除高频分支使 FID 从 0.347 恶化至 0.504，去除低频分支同样显著损害性能。

![[assets/figures/papers/paper_list_l1907_TriC_Motion_A_Causal_Diffusion_Framework_for_Text_to_Motion_Generation/figures/004_Figure_4.jpg]]
*Figure 4: Detailed architectures of TriC-Motion main components. (a) HFA with DWT/FFT decomposition; (b) Low-frequency branch network in HFA; (c) High-frequency branch network in HFA; (d) S-Fus with motion and semantic scoring; (e) Details of CCMD*

### 得分指导的三域融合（S-Fus）

S-Fus 通过双分支评分机制自适应地整合三域特征。对于每个域 $i \in \{temp, spa, freq\}$，运动评分分支 $f_{mot}$ 基于三域特征的拼接 $F_j^{tri}$ 计算运动层面的重要性，语义评分分支 $f_{sem}$ 则结合域特征与全局文本标记 $CLS$ 计算语义对齐程度。两者相加后经 Softmax 得到注意力权重 $\alpha_i$，最终加权融合并投影：

$$
\begin{array}{l} logits_{mot}^i = f_{mot}(F_j^{tri}), \; logits_{sem}^i = f_{sem}(\mathrm{CAT}(F_j^i, CLS)) \\ \alpha_i = \mathrm{Softmax}(logits_{mot}^i + logits_{sem}^i) \\ Y_j = \mathrm{Linear}(\mathrm{CAT}(X_j, \sum_i \alpha_i F_j^i)) \end{array}
$$

其中 $F_j^{tri} = \mathrm{CAT}(F_j^{temp}, F_j^{spa}, F_j^{freq})$。S-Fus 的结构见 Figure 4(d)。

### 因果反事实运动解缠模块（CCMD）

CCMD 是 TriC-Motion 首次引入运动生成的因果干预机制（Figure 2 给出了结构因果模型）。其核心思想是：域特征 $F_j^i$ 中既包含对运动生成有益的因果贡献 $E_j^i$，也混杂了与运动无关的混淆特征 $C_j^i$。CCMD 通过事实模块（Factual Module）和反事实模块（Counterfactual Module）分别提取二者，再通过有监督干预消除混淆噪声。

![[assets/figures/papers/paper_list_l1907_TriC_Motion_A_Causal_Diffusion_Framework_for_Text_to_Motion_Generation/figures/002_Figure_2.jpg]]
*Figure 2: Structured Casual Model in TriC-Motion*

**事实模块**采用通道门控机制，通过全局平均池化、两层线性变换和 Sigmoid 激活生成通道级权重 $\omega$，进而提取因果贡献：

$$
\omega = \mathrm{Sigmoid}(\mathrm{Linear}(\mathrm{ReLU}(\mathrm{Linear}(\mathrm{Pool}(F_j^i))))) \in \mathbb{R}^{1 \times 1 \times D}
$$

$$
E_j^i = \omega \odot F_j^i
$$

反事实模块与事实模块共享相同的轻量对称架构，但通过独立的参数学习提取混淆特征 $C_j^i$。最终的因果解缠特征通过减去反事实混淆得到：

$$
\tilde{F}_j^i = W_{do} E_j^i - W_{do} C_j^i
$$

其中 $W_{do}$ 为可学习的干预投影矩阵，$\tilde{F}_j^i$ 为因果解缠后的域特征，用于后续融合和生成。CCMD 仅在训练阶段使用，推理时直接利用解缠后的特征空间，不增加额外计算开销。

### 训练损失函数

TriC-Motion 采用组合损失进行端到端训练。

**简单扩散损失**：直接回归干净运动序列 $x_0$，而非预测噪声：

$$
\mathcal{L}_{\mathrm{simple}} = \mathbb{E}_{x_0 \sim q(x_0|c), t \sim [1,T]} \left[ \| x_0 - f(x_t, t, c) \|^2 \right]
$$

**事实-反事实损失**：逐层约束 CCMD 的输出逼近真实运动，迫使模块去除混淆信息。设 $TDE_j$ 为第 $j$ 层 CCMD 输出的三域解缠特征经融合后的去噪预测，$w_j$ 为层次权重：

$$
\mathcal{L}_{fcf} = \sum_{j=1}^{J} w_j \mathcal{L}_{fcf,j} = \sum_{j=1}^{J} w_j \mathcal{L}_{MSE}(TDE_j, x_0)
$$

**感知损失**：利用预训练运动编码器 $E$ 提取特征表示，约束生成运动与真实运动在感知空间的一致性：

$$
\mathcal{L}_{p} = \|E(\hat{x}_0) - E(x_0)\|_2^2
$$

**总损失**：

$$
\mathcal{L} = \mathcal{L}_{\mathrm{simple}} + \lambda_{fcf} \mathcal{L}_{fcf} + \lambda_{p} \mathcal{L}_{p}
$$

默认设置 $\lambda_{fcf}=1$，$\lambda_{p}=10$。消融实验（Table 4）表明层次权重 $\{0.1, 0.2, 0.3, 0.4\}$ 取得最优结果，验证了深层施加更高权重的合理性。敏感性分析（Table A3）进一步证明损失权重在较大范围变化时性能保持稳定，模型优化具有鲁棒性。

## 实验与分析

### 主实验：HumanML3D 与 SnapMoGen 双基准定量评估

TriC-Motion 在两个主流文本-动作生成基准上进行了全面评估。在 **HumanML3D** 数据集上（Table 1），TriC-Motion (large) 以 **R@1 0.612** 取得最优文本-动作语义对齐性能，显著超越先前 SOTA 方法 **SALAD**（Hong et al., 2025）的 0.581（Δ=+0.031）。在 base 配置下，R@1 亦达到 0.607，R@2 和 R@3 分别为 0.800 和 0.878，均处于领先水平。MM-Dist 降至 2.463，优于 SALAD 的 2.649，进一步验证了语义匹配的精准性。

![[assets/figures/papers/paper_list_l1907_TriC_Motion_A_Causal_Diffusion_Framework_for_Text_to_Motion_Generation/figures/005_Table_1.jpg]]
*Table 1: Quantitative results on HumanML3D. The right arrow → means the closer to real motion the better. Each experiment is repeated 20 times, with average results and 95% confidence intervals (±) reported. The best result is highlighted in bold, and the second-best is underlined*

在分布质量指标 FID 上，TriC-Motion (base) 取得 0.347，虽未超越 **LaMP**（Li et al., 2024c）的 0.032，但需注意 FID 并非 TriC-Motion 的核心优化目标——该方法主要通过三域因果建模提升语义对齐，而非单纯追求分布匹配。Diversity 指标上，TriC-Motion 的 9.652 与真实数据的 9.503 最为接近，表明生成动作的多样性未因强语义约束而坍缩。

在 **SnapMoGen** 数据集上（Table 2），TriC-Motion 展现出更强的跨数据集泛化能力：**R@1 达到 0.907**，大幅超越第二名 **MoMask++**（Guo et al., 2024）的 0.802（Δ=+0.105），R@2 和 R@3 分别达 0.964 和 0.980。CLIP Score 为 0.675，与 MoMask++ 的 0.685 基本持平，说明模型在文本-视觉对齐上保持竞争力。

![[assets/figures/papers/paper_list_l1907_TriC_Motion_A_Causal_Diffusion_Framework_for_Text_to_Motion_Generation/figures/006_Table_2.jpg]]
*Table 2: Quantitative results on SnapMoGen test dataset*

**跨评估器验证（Table A5）**：为避免 HumanML3D 评估器与训练的潜在耦合，TriC-Motion 在独立评估器 **CLaM** 下进行测试，依然以大幅优势超越 SALAD 等强基线，证明性能增益来源于模型本身的三域因果建模能力，而非评估特征空间的过拟合。

**用户调研（Table 5）**：在整体质量和文本-动作对齐性的人工评估中，TriC-Motion 均获得最优评价，进一步佐证了定量指标的可靠性。

### 消融实验：三域建模与因果干预的贡献解耦

消融实验从模块贡献、频率分支设计、因果干预配置三个维度系统验证了 TriC-Motion 各组件的有效性。

**模块逐步叠加消融（Table 3 上半部分）**：以纯时间建模（TME only）为基线，逐步添加空间拓扑建模（STM）、混合频率分析（HFA）和得分指导融合（S-Fus）。结果表明，每增加一个域均带来 R-Precision 和 FID 的持续改善。完整三域融合（TME+STM+HFA+S-Fus）达到 **R@1 0.607**，较纯时间建模的 0.569 提升 3.8 个百分点，FID 从 0.593 降至 0.347，降幅达 41.5%。这一趋势验证了空间、时间和频率三域信息互补的核心假设。

**HFA 内部设计消融（Table 3 下半部分）**：HFA 的低频分支和高频分支缺一不可。去除高频分支后，FID 从 0.347 急剧恶化至 0.504，表明高频细节对动作逼真度至关重要；去除低频分支同样导致性能下降。此外，去除关节内频率分支（仅保留时间频率）亦损害性能，说明关节维度的频谱建模对骨骼拓扑合理性有独立贡献。

**CCMD 因果干预消融（Table 4 上半部分）**：去除 CCMD 后，R@1 从 0.607 降至 0.568，FID 从 0.347 升至 0.561，降幅显著。进一步分析表明，CCMD 同时作用于时-空-频三域并应用于 S-Fus 之后效果最优；仅在时域或空-时域施加因果干预均不及全三域配置。将因果干预置于 S-Fus 之前（“pre”）同样劣于后置（“post”）方案，说明在融合后去除跨域混淆噪声更为有效。

**层次损失权重消融（Table 4 下半部分）**：对于 4 层去噪块，权重配置 {0.1, 0.2, 0.3, 0.4}（深层权重更高）取得最佳结果，验证了深层特征对因果解缠更敏感的假设。

**感知损失与因果损失敏感性分析（Table A3）**：感知损失权重 α 和因果损失权重 β 在较大范围内变化时，模型性能保持稳定，表明优化过程对超参数不敏感，训练鲁棒性强。此外，完全移除感知损失后（Table A4），TriC-Motion 仍以 R@1 0.585 超越 SALAD 的 0.581，说明核心增益来自三域建模和因果干预，而非与评估器的感知特征耦合。

### 失败模式与局限性

尽管 TriC-Motion 在语义对齐上取得显著突破，仍存在以下局限：

1. **推理效率瓶颈**：扩散模型在原始运动空间进行多步去噪，平均推理时间（AIT）为 3.8s，计算量 388.45 GFLOPs（Table A1），虽参数量仅 13.86M（Table A2），但推理速度仍远高于基于离散空间或潜在空间的快速方法（如 **MoMask** 的 0.4s）。尚未整合 DPM-Solver、UniPC 等先进采样器，加速潜力未释放。

![[assets/figures/papers/paper_list_l1907_TriC_Motion_A_Causal_Diffusion_Framework_for_Text_to_Motion_Generation/figures/012_Table.jpg]]
*Table: A1: FLOPs and average inference time (AIT) comparison across various methods*

2. **FID 非最优**：在分布匹配指标 FID 上，TriC-Motion 未在所有设置下达到最优（LaMP 等方法 FID 更低），表明生成动作的分布与真实分布之间仍存在差距，可能与扩散模型的固有特性或训练目标中 FID 未直接优化有关。

3. **频率分支计算负担**：HFA 中的 DWT/FFT 分解及双分支增强增加了网络复杂度，在极低计算预算场景下可能成为瓶颈，尽管整体参数规模较小。

4. **长时运动与多样化动作类型**：当前实验主要在 HumanML3D 和 SnapMoGen 的常规动作类型上验证，对于更长时序的运动生成和舞蹈、体育等复杂动作类型，三域因果建模的收益边界尚不明确，需进一步探索。

### 补充图表

![[assets/figures/papers/paper_list_l1907_TriC_Motion_A_Causal_Diffusion_Framework_for_Text_to_Motion_Generation/figures/008_Table_3.jpg]]
*Table 3: Ablation study of the proposed modules in TriC-Motion on HumanML3D test dataset, as well as the analysis of HFA. “2D rep” denotes the spatio-temporal 2D motion representation with dimensions*

![[assets/figures/papers/paper_list_l1907_TriC_Motion_A_Causal_Diffusion_Framework_for_Text_to_Motion_Generation/figures/009_Table_4.jpg]]
*Table 4: Ablation experiment of CCMD (upper half) and the layer-wise loss weights of*

![[assets/figures/papers/paper_list_l1907_TriC_Motion_A_Causal_Diffusion_Framework_for_Text_to_Motion_Generation/figures/010_Table_5.jpg]]
*Table 5: User study results*

![[assets/figures/papers/paper_list_l1907_TriC_Motion_A_Causal_Diffusion_Framework_for_Text_to_Motion_Generation/figures/011_Figure.jpg]]
*Figure: A1: t-SNE Visualization of the the three feature types in TriC-Motion: motion-relevant features $F _ { f }$ , motion-irrelevant (confounding) features $F _ { c f }$ , and the final causally disentangled features $F _ { t d e }$ used for generation. The six text inputs are taken from the HumanML3D test set*

![[assets/figures/papers/paper_list_l1907_TriC_Motion_A_Causal_Diffusion_Framework_for_Text_to_Motion_Generation/figures/015_Table.jpg]]
*Table: A4: The performance comparison on HumanML3D dataset between our TriC-Motion without ${ \mathcal { L } }$ _ { p } and the previous state-of-the-art method, SALAD (Hong et al., 2025). Table A5: Performance comparison on HumanML3D dataset under the CLaM evaluator*

![[assets/figures/papers/paper_list_l1907_TriC_Motion_A_Causal_Diffusion_Framework_for_Text_to_Motion_Generation/figures/014_Table.jpg]]
*Table: A3: Sensitivity analysis of the perceptual loss ${ \mathcal { L } }$ _ { p } (upper part) and causal loss $\mathcal { L }$ _ { f c f } (lower part). Here, α and β denote the weights of ${ \mathcal { L } }$ _ { p } and $\mathcal { L }$ _ { f c f } , respectively. The default setting (Ours) corresponds to $\alpha = 1$ . $0 , \beta = 1$ 0*

## 方法谱系与知识库定位

### 1. 与基线方法的继承与突破

TriC-Motion 建立在扩散式文本到动作生成的主线上，其直接架构基座是 **MDM**（Tevet et al., 2022）所确立的“原始运动空间扩散预测”范式——在运动序列上直接执行多步去噪，以 $x_0$ 预测替代噪声预测。TriC-Motion 继承了 MDM 的简单去噪损失 $\mathcal{L}_{\mathrm{simple}}$（Eq. 9），但对其核心的“单域建模”瓶颈进行了根本性重构：MDM 仅使用一个纯 Transformer 沿时间维度处理运动序列，缺乏对空间骨骼拓扑和频率特性的显式建模，导致生成动作在关节合理性和全局运动趋势上存在不足。

TriC-Motion 的突破在于将建模域从单一时间域扩展至**时间-空间-频率三域并行**，并通过得分指导融合（S-Fus）进行信息整合。这一设计与以下近期强基线形成明确对比：

- **SALAD**（Hong et al., 2025）作为先前的 SOTA 之一，在 HumanML3D 上取得 R@1 0.581。TriC-Motion 以 0.612 超越 SALAD（+0.031），核心增益来自三域联合建模和因果解缠，而非简单的网络缩放。
- **MoMask**（Guo et al., 2024）和 **StableMoFusion**（Huang et al., 2024a）分别代表离散表示和潜在空间扩散路线，它们在推理速度上具有优势（MoMask 推理仅 0.4s），但在语义对齐指标上弱于 TriC-Motion。
- **LaMP**（Li et al., 2024c）是频率建模方向的先行者，在 FID 指标上表现突出（0.032），但 TriC-Motion 的混合频率分析（HFA）采用了 DWT+FFT 的双重分解策略，同时捕捉低频全局趋势和高频局部细节，在保持竞争力的 FID（0.347）的同时大幅提升了语义对齐（R@1）。
- **MotionPCM**（Jiang et al., 2025）和 **GMMotion** 等近期工作分别在融合先验和生成模型设计上有所贡献，但均未涉及因果干预机制。

TriC-Motion 的独特定位在于：**首次将因果干预引入运动生成领域**，通过 CCMD 模块显式消解多域特征中的运动无关混淆噪声。这一设计在方法谱系中填补了“多域建模 + 因果解缠”的空白，与仅依赖统计关联的现有方法形成本质差异。

### 2. 三域建模的知识库贡献

TriC-Motion 的三个核心模块各自对应运动生成中不同维度的知识需求：

| 模块 | 建模域 | 知识贡献 | 与已有工作的关系 |
|------|--------|----------|------------------|
| **TME** | 时间 | TransformerEncoderLayer 捕捉短程和长程时序依赖 | 继承 MDM 的时间建模思路，但作为三域并行分支之一而非唯一建模手段 |
| **STM** | 空间 | 3 层 GCN 在关节维度建模，保持骨骼拓扑合理性 | 类似 STG-Diff 的图卷积思路，但集成于扩散去噪块内而非独立编码器 |
| **HFA** | 混合频率 | DWT 分解高低频子带 + FFT 获取全局频谱，自适应注意力增强低频，深度可分离卷积增强高频 | 超越 LaMP 的单频段分析，实现高低频互补增强 |

消融实验（Table 3）验证了各模块的独立贡献：逐步添加 STM、HFA 和 S-Fus 持续提升各项指标，完整三域融合达最优（R@1 0.607）。特别地，去除 HFA 后 FID 从 0.347 恶化至 0.593，去除高频分支使 FID 升至 0.504，表明混合频率分析对分布匹配质量具有决定性作用。

### 3. 因果干预的适用边界

CCMD 模块的核心机制是通过事实/反事实特征提取和有监督因果干预（$W_{do} E_j^i - W_{do} C_j^i$），显式消除与运动无关的混淆特征。消融实验（Table 4）揭示了其适用边界：

- **作用位置**：CCMD 应用于 S-Fus 之后（“post”）优于应用于融合之前（“pre”），说明在三域信息整合后再进行因果解缠更为有效。
- **作用域**：同时作用于时空频三域（“tri-domain”）效果最优；仅在时域（“temp”）或空时域（“temp+spa”）施加因果干预均不及全三域，验证了混淆噪声存在于所有建模域中。
- **层次权重**：$\mathcal{L}_{fcf}$ 的层次损失权重 $\{0.1, 0.2, 0.3, 0.4\}$ 取得最佳结果，深层施加更高权重的设计符合直觉——越靠近输出的特征层越需要纯净的因果特征。

值得注意的是，移除感知损失后，模型仍以 R@1 0.585 超越 SALAD 的 0.581（Table A4），证明核心增益来自三域建模和因果干预，而非与评估器的耦合。跨评估器验证（Table A5，使用独立 CLaM 评估器）进一步确认了性能提升的鲁棒性。

### 4. 局限与开放问题

**推理效率瓶颈**：TriC-Motion 在原始运动空间进行多步去噪，推理时间（AIT 3.8s）和计算量（388.45 GFLOPs）仍高于基于离散空间或潜在空间的快速方法（如 MoMask 0.4s）。尚未整合先进采样器（如 DPM-Solver、UniPC），加速潜力未完全释放。

**FID 指标的可改进空间**：尽管语义对齐指标（R@1、MM-Dist）达到 SOTA，FID（0.347）未在所有设置下达到最优（LaMP 的 0.032 更低），说明分布匹配可能有进一步改进空间。

**频率建模的计算负担**：HFA 的 DWT+FFT 双重分解和双分支增强增加了网络复杂度，虽然整体参数规模较小（13.86M），但在极低计算预算场景下可能仍是负担。

**开放方向**：
1. 能否将 TriC-Motion 迁移到潜在空间扩散框架中，以大幅降低推理成本并进一步提高 FID？
2. 因果干预模块的设计思想是否可推广到其他生成任务（如视频生成、音频合成），以抑制多域混淆噪声？
3. 如何动态调整三域融合的权重，或引入更复杂的注意力机制，使模型能根据文本复杂度自适应地侧重不同域的信息？
4. 在更长时运动生成和更多样化的运动类型（如舞蹈、体育动作）上，三域因果建模是否有进一步的收益？

## 原文 PDF

![[paperPDFs/ICLR_2026/TriC_Motion_A_Causal_Diffusion_Framework_for_Text_to_Motion_Generation.pdf]]