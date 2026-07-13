---
title: "FinPercep-RM: A Fine-grained Reward Model and Co-evolutionary Curriculum for RL-based Real-world Super-Resolution"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/FinPercep_RM_A_Fine_grained_Reward_Model_and_Co_evolutionary_Curriculum_for_RL_based_Real_world_Super_Resolution.pdf
project_link: null
code_link: "https://github.com/lyd-2022/FinPercep-RM"
aliases:
- FRCECLC
- FinPercep-RM
tags:
- CVPR_2026
- topic/benchmarks_datasets_evaluation
- topic/benchmarks_datasets_evaluation/benchmarking
core_operator: FinPercep-RM同时输出的全局质量评分（What）和细粒度感知退化图（Where），以及通过CCL控制的奖励信号复杂度与训练稳定性之间的平衡，是抑制reward hacking并提升局部真实感的关键。
primary_logic: 让奖励模型具备“诊断”能力，通过空间局部的缺陷图调制全局评分，使其在本质上对局部瑕疵敏感，再配合从粗到细的协同进化课程学习策略，可以在不牺牲训练稳定性的前提下，有效消除奖励黑客现象。
claims:
- FinPercep-RM的Fg-PDM能够精准定位局部失真，并使全局评分对局部伪影敏感，相比标准IQA更符合人类判断。
- CCL的训练曲线显示，直接使用FinPercep-RM训练不稳定，而采用CCL后训练收敛且最优。
- 在四个真实世界基准上的定量评估表明，结合FinPercep-RM的RLHF训练方法在所有指标上均达到最佳或次佳性能。
- RealLQ250 上 MUSIQ = 73.456 (Ours REFL)
---

# FinPercep-RM: A Fine-grained Reward Model and Co-evolutionary Curriculum for RL-based Real-world Super-Resolution

> [!tip] 核心洞察
> 让奖励模型具备“诊断”能力，通过空间局部的缺陷图调制全局评分，使其在本质上对局部瑕疵敏感，再配合从粗到细的协同进化课程学习策略，可以在不牺牲训练稳定性的前提下，有效消除奖励黑客现象。

| 字段 | 内容 |
|------|------|
| 中文题名 | FinPercep-RM：一种面向强化学习的真实世界超分辨率的细粒度奖励模型与协同进化课程 |
| 英文题名 | FinPercep-RM: A Fine-grained Reward Model and Co-evolutionary Curriculum for RL-based Real-world Super-Resolution |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.22647) · [Code](https://github.com/lyd-2022/FinPercep-RM) |
| Topic | #topic/benchmarks_datasets_evaluation #topic/benchmarks_datasets_evaluation/benchmarking |
| Method | FinPercep-RM and Co-evolutionary Curriculum Learning (CCL) |
| Dataset | RealLQ250, User Study |

> [!tip] 效果简介
> - RealLQ250 上，MUSIQ 73.456 (Ours REFL) vs 70.456 (CLIP-IQA REFL) (+3.0)。
> - User Study 上，用户偏好率 (Realism / Fidelity) DIT4SR w/ Ours vs DiffBIR: 84.2% / 80.1% vs 各对比方法 (DiffBIR, SeeSR, etc.) (显著优于所有对比方法)。

## 概要

真实世界图像超分辨率（Real-ISR）在利用强化学习人类反馈（RLHF）进行优化时，面临一个关键瓶颈：现有基于图像质量评价（IQA）的奖励模型仅输出单一全局质量分数，缺乏对局部失真的细粒度感知能力。这种“盲评”机制无法检测和惩罚空间局部的伪影与纹理畸变，导致生成器在训练中利用奖励函数的漏洞，产生reward hacking现象——输出图像虽获得高全局评分，却包含明显的“绘画式”失真和局部伪影（Fig. 1）。

针对上述问题，本文提出**FinPercep-RM**，一种细粒度感知奖励模型，其核心创新在于让奖励模型具备“诊断”能力：FinPercep-RM基于编码器-解码器架构，同时输出一个细粒度校准的全局质量评分（Fine-grained Calibrated Global Score）和一张空间精细的感知退化图（Fine-grained Perceptual Degradation Map, Fg-PDM）。退化图精确定位并量化局部缺陷的似然与强度，而全局评分则通过退化图对深层特征进行调制，从而在本质上对局部瑕疵敏感，使奖励信号更贴合人类感知判断（Fig. 1(a)）。

为了训练FinPercep-RM，本文构建了**FGR-30k**数据集，包含30,000对通过区域交换合成的局部失真样本及其真值退化图。真值退化图由像素级差异与基于DINOv3的特征级差异加权融合生成，为模型提供空间精确的监督信号。在此基础上，本文进一步提出**协同进化课程学习（Co-evolutionary Curriculum Learning, CCL）**策略，通过奖励模型渐进式扩展与生成器课程协同进化两条路径，解决细粒度奖励信号带来的训练稳定性-鲁棒性困境：从粗粒度的全局奖励开始，逐步引入更严格的细粒度信号，使生成器在稳定初始化的前提下，最终抑制reward hacking并提升局部真实感（Fig. 1(b)）。

在实验验证方面，FinPercep-RM结合CCL在四个真实世界基准（DrealSR、RealSR、RealLR200、RealLQ250）上取得了最优或次优的定量性能（Table 1），用户主观测试中相较DiffBIR、SeeSR等方法的偏好率超过80%（Table 2）。消融实验进一步证实，移除CCL或仅使用像素差异训练奖励模型均导致性能显著下降（Table 4），验证了协同进化课程与高层特征差异对方法有效性的关键支撑作用。

真实世界图像超分辨率（Real-ISR）旨在从低质量输入中恢复高保真、视觉逼真的高分辨率图像。近年来，基于强化学习的微调策略（RLHF）被引入该领域，通过奖励模型引导生成器优化感知质量，取得了显著进展。然而，现有方法面临一个核心瓶颈：当前主流的奖励模型——如图像质量评估模型（IQA）——仅输出单一的全局质量评分，缺乏对空间局部失真的细粒度感知能力。

这一缺陷直接导致了严重的“奖励黑客”（reward hacking）现象：生成器学会最大化全局评分，却产生了明显的局部伪影和“绘画式”失真，与真实图像相去甚远。如 Figure 1(a) 所示，标准 IQA 奖励模型（如 **CLIP-IQA** (Wang et al., AAAI 2023) 和 **MANIQA** (Yang et al., CVPR 2022)）无法有效惩罚局部失真，其评分与人类主观判断存在显著偏差。Figure 1(c) 进一步可视化了这一困境：使用 CLIP-IQA 或 MANIQA 作为奖励信号训练的生成器，其输出图像中出现了大量局部伪影，而真实图像则保持了自然的纹理结构。

Figure 1(b) 揭示了另一个关键矛盾——稳定性与鲁棒性的权衡困境：基线 IQA 奖励模型（蓝色/紫色曲线）虽然训练收敛迅速且稳定，但因其粗粒度的全局评分而无法有效抑制奖励黑客；若直接使用具备细粒度感知能力的 FinPercep-RM（浅蓝色曲线），奖励信号方差增大，训练过程出现剧烈振荡甚至不收敛。这表明，仅设计一个更精细的奖励模型是不够的，还需要一套配套的训练策略来平衡奖励信号的复杂度与训练的稳定性。

针对上述问题，本文提出 **FinPercep-RM**——一个细粒度感知奖励模型，以及 **协同进化课程学习（Co-evolutionary Curriculum Learning, CCL）** 框架。FinPercep-RM 通过编码器-解码器架构同时输出全局质量评分和逐像素的感知退化图（Fine-grained Perceptual Degradation Map, Fg-PDM），使奖励模型具备“诊断”能力：不仅判断图像质量“如何”（What），还能定位缺陷“在哪里”（Where）。CCL 则通过奖励模型的渐进式扩展与生成器的课程协同进化，在训练初期以粗粒度、低方差的奖励信号保证稳定性，随后逐步过渡到细粒度、高方差的信号以提升鲁棒性，从而在稳定收敛的前提下有效消除奖励黑客现象。

## 核心方法与创新机理

FinPercep-RM 的核心创新在于将奖励模型从“盲评打分器”升级为“细粒度诊断器”，并引入协同进化课程学习（CCL）来解决由此带来的训练稳定性挑战。其关键改变可归纳为三个相互耦合的维度。

### 从全局评分到“What & Where”的双通道诊断

现有基于 IQA 的奖励模型（如 **CLIP-IQA** (Wang et al., AAAI 2023)、**MANIQA** (Yang et al., CVPR 2022)）仅输出单一全局质量分数 $S_{\text{global}}$，缺乏对局部失真的空间感知能力。这导致生成器在 RLHF 训练中容易产生 reward hacking——通过制造“绘画式”局部伪影来欺骗全局评分，而非真正提升重建质量。

FinPercep-RM 将输出粒度从一维标量扩展为双通道信号：

$$\{ S_{\mathrm{fgc-global}}, M_{\mathrm{fg-pdm}} \} = \mathrm{RM}_{\phi}(I_{SR})$$

其中 $M_{\mathrm{fg-pdm}}$ 是**细粒度感知退化图**（Fine-grained Perceptual Degradation Map），以逐像素热图的形式定位缺陷的空间分布与强度；$S_{\mathrm{fgc-global}}$ 是**细粒度校准全局评分**，其关键设计在于显式依赖退化图：

$$S_{\mathrm{fgc-global}} = \mathrm{MLP}(f_N \odot \mathrm{interpolate}(M_{\mathrm{fg-pdm}}))$$

通过将退化图上采样后与最深全局特征 $f_N$ 逐元素调制，迫使全局评分对局部伪影产生本质敏感性。这一“诊断反馈”机制是抑制 reward hacking 的因果旋钮：生成器无法再通过制造全局评分不可见的局部失真来获取高奖励。

### 从无监督到有监督的退化图学习：FGR-30k 数据集

细粒度退化图的训练需要空间级真值监督，而现有数据集无法提供。FinPercep-RM 构建了 **FGR-30k** 数据集，包含 30,000 对合成失真样本与对应真值退化图。其核心合成策略是通过区域交换将扩散模型 SR 输出中的伪影区域“植入”干净图像：

$$I_{\mathrm{syn}} = M \odot I_{SR} + (1 - M) \odot I_{GT}$$

真值退化图则通过融合像素级差异与高层特征差异生成：

$$M_{\mathrm{gt}} = \mathrm{Normalize}\left( \alpha \cdot \mathrm{Diff}_{\mathrm{pixel}} + (1 - \alpha) \cdot \mathrm{Diff}_{\mathrm{feat}} \right)$$

其中特征差异基于 DINOv3 的余弦距离计算。消融实验证实，仅使用像素差异训练会使 MUSIQ 从 73.456 降至 72.123，说明高层语义特征差异对退化图泛化能力至关重要。

### 从固定奖励到协同进化课程学习（CCL）

细粒度奖励信号虽然更精准，但直接用于 RLHF 训练会导致剧烈振荡甚至不收敛（见 Figure 1(b) 中浅蓝色曲线的剧烈波动）。CCL 通过两条协同进化路径解决这一稳定性-鲁棒性权衡：

1. **奖励模型渐进扩展**：构建诊断能力递增的模型序列 $\{RM_0, RM_1, ..., RM_N\}$，通过分阶段训练逐步增强奖励信号的方差与细粒度。
2. **生成器课程协同进化**：生成器先用粗粒度的 $RM_0$ 进行稳定初始化，随后与逐渐严格的 $RM_k$ 版本协同演进，逐步提升局部保真度。

消融实验直接验证了 CCL 的必要性：移除 CCL（直接使用 FinPercep-RM 训练）使 MUSIQ 从 73.456 降至 71.982，证实了课程机制对稳定收敛的因果作用。最终奖励信号通过解耦融合全局评分与退化图信息：

$$R_k = \lambda_1 \bar{S}_{\mathrm{global}} + \lambda_2 (1 - \widehat{\max}(M_{\mathrm{fg-pdm}}))$$

这一融合方式在阶段 $k$ 平衡了全局质量评估与局部缺陷惩罚，使训练曲线从振荡走向稳定最优收敛（Figure 1(b) 橙色曲线）。

FinPercep-RM 与协同进化课程学习（Co-evolutionary Curriculum Learning, CCL）框架的整体设计围绕一个核心矛盾展开：**更精细的奖励信号能更有效地抑制 reward hacking，但其高方差特性又会破坏 RL 训练的稳定性**。为此，该框架从两个维度协同推进——奖励模型的细粒度感知能力构建，以及训练过程中奖励复杂度与生成器能力的同步演化。

### 框架总览

整个 RL-based Real-ISR 优化流程如图 Figure 2 所示，包含三个关键实体：

![[assets/figures/papers/paper_list_l2678_https_arxiv_org_abs_2512_22647/figures/003_Figure_2.jpg]]
*Figure 2: The overall pipeline of the proposed FinPercep-RM and Co-evolutionary Curriculum Learning (CCL) framework. FinPercep-RM produces a Fine-grained Perceptual Degradation Map that captures spatially localized defect likelihood and intensity, and the reward model is progressively expanded from small-variance, coarse-grained rewards to large-variance, fine-grained signals. During training, under the CCL mechanism, the Generator first learns with the coarse global reward from*

1. **生成器（Generator）** $G_\theta$：以低质量输入 $I_{LQ}$ 为条件，生成超分辨率重建 $I_{SR} = G_\theta(I_{LQ})$。
2. **FinPercep-RM 奖励模型** $\mathrm{RM}_\phi$：接收 $I_{SR}$，同时输出**细粒度校准全局质量评分** $S_{\mathrm{fgc-global}}$ 和**细粒度感知退化图** $M_{\mathrm{fg-pdm}}$，从“是什么缺陷”（what）和“缺陷在哪里”（where）两个互补维度评估重建质量。
3. **CCL 协同进化机制**：构建一个逐步增强的奖励模型序列 $\{\mathrm{RM}_0, \mathrm{RM}_1, \ldots, \mathrm{RM}_N\}$，并与生成器的训练阶段同步演进，实现从“粗粒度稳定初始化”到“细粒度鲁棒优化”的平滑过渡。

### 数据流与模块交互

**推理阶段**，FinPercep-RM 的内部数据流如下（详见 Eq. (1)-(2)）：

- **Encoder** 以 IQA 骨干网络提取多尺度特征 $\{f_i\}_{i=1}^N$，其中最深层的全局特征 $f_N$ 编码了“what”信息。
- **Decoder** 对多尺度特征进行上采样与融合，经 Sigmoid 激活后输出归一化的感知退化图 $M_{\mathrm{fg-pdm}} \in [0, 1]^{H \times W}$，每个像素值表示该位置存在局部缺陷的可能性和强度。
- **MLP Head** 接收被退化图调制的全局特征 $f_N \odot \mathrm{interpolate}(M_{\mathrm{fg-pdm}})$，回归得到细粒度校准的全局质量评分 $S_{\mathrm{fgc-global}}$。这一设计的**因果机制**在于：通过显式地将全局评分与空间局部缺陷图耦合，使奖励模型在本质上对局部伪影敏感，从而弥补标准 IQA 仅输出单一全局评分、无法检测局部失真的结构性缺陷。

**训练阶段**，CCL 通过两条协同演化路径平衡稳定性与鲁棒性：

- **奖励模型渐进式参数扩展**：在 FGR-30k 数据集上进行分阶段训练，逐步增加 Decoder 的容量与感知粒度，构建诊断能力递增的模型序列。早期 $\mathrm{RM}_k$ 输出较粗粒度的退化图，奖励信号方差小，训练稳定；后期 $\mathrm{RM}_k$ 具备细粒度缺陷定位能力，能有效惩罚局部伪影。
- **生成器课程协同演化**：生成器首先在 $\mathrm{RM}_0$ 的粗粒度全局奖励下完成稳定初始化，随后随 $\mathrm{RM}_k$ 的逐步增强而同步更新，最终在 $\mathrm{RM}_N$ 的细粒度信号引导下实现局部保真度的提升与 reward hacking 的抑制。

### 训练数据闭环

框架依赖 **FGR-30k 数据集**提供细粒度监督信号（构建流程见 Figure 3）。该数据集包含 30,000 对合成样本，通过区域交换策略（Eq. (3)）将扩散模型 SR 输出中的伪影区域“植入”高质量图像，并融合像素级差异与 DINOv3 特征级差异生成真值退化图（Eq. (4)），为 FinPercep-RM 的密集热图损失 $\mathcal{L}_{\mathrm{map}}$（Eq. (5)）提供空间精确的监督。

![[assets/figures/papers/paper_list_l2678_https_arxiv_org_abs_2512_22647/figures/004_Figure_3.jpg]]
*Figure 3: FGR-30k construction pipeline. We synthesize finegrained distortion samples by swapping artifact-rich regions from diffusion-based SR outputs into clean images, using both random and semantic masks. Ground-truth perceptual degradation maps are generated by fusing pixel- and feature-level dissimilarities (via DINOv3), providing spatially precise supervision for training FinPercep-RM*

### 与基线方法的架构差异

相较于 **CLIP-IQA**（Wang et al., AAAI 2023）和 **MANIQA**（Yang et al., CVPR 2022）等仅输出单一全局质量分数的奖励模型，FinPercep-RM 的核心架构创新在于引入了**解耦的“诊断”分支**（Decoder + 退化图调制），使奖励信号从“单一标量判断”升级为“空间定位 + 全局校准”的双通道评估。这一设计直接针对 reward hacking 的产生机理——生成器通过制造全局评分高但局部失真的“欺骗性”输出来最大化奖励——提供了根本性的抑制手段。

### 奖励模型架构：FinPercep-RM

FinPercep-RM 的核心设计目标是让奖励模型具备“诊断”能力——不仅输出全局质量评分（What），还能定位局部失真（Where）。其整体输出形式为：

$$
\{ S_{\mathrm{fgc-global}}, M_{\mathrm{fg-pdm}} \} = \mathrm{RM}_{\phi}(I_{SR})
$$

其中 $S_{\mathrm{fgc-global}}$ 为细粒度校准的全局质量分数，$M_{\mathrm{fg-pdm}}$ 为细粒度感知退化图（Fine-grained Perceptual Degradation Map）。

模型由三个关键模块组成：

- **Encoder**：基于 IQA 骨干网络提取多尺度特征 $\{ f_i \}_{i=1}^N$，其中 $f_N$ 为最深层的全局表征。
- **Decoder**：对多尺度特征进行上采样与融合，经 Sigmoid 激活后输出归一化的感知退化图 $M_{\mathrm{fg-pdm}}$。
- **MLP Head**：接收被退化图调制的全局特征，回归最终的细粒度校准全局质量分数。

其计算流程可形式化为：

$$
\begin{array}{rl}
& \{ f_i \}_{i=1}^N = \mathrm{Encoder}(I_{SR}) \\
& M_{\mathrm{fg-pdm}} = \mathrm{Sigmoid}(\mathrm{Decoder}(\{ f_i \}_{i=1}^N)) \\
& S_{\mathrm{fgc-global}} = \mathrm{MLP}(f_N \odot \mathrm{interpolate}(M_{\mathrm{fg-pdm}}))
\end{array}
$$

**因果机制**：全局评分 $S_{\mathrm{fgc-global}}$ 被显式地绑定到退化图上——通过将下采样后的 $M_{\mathrm{fg-pdm}}$ 与最深特征 $f_N$ 做逐元素乘法（$\odot$），使得局部伪影区域的激活值会直接调制全局质量评分。这从根本上解决了标准 IQA 模型（如 **CLIP-IQA** (Wang et al., AAAI 2023)、**MANIQA** (Yang et al., CVPR 2022)）仅输出单一全局分数、对局部失真不敏感的问题。

---

### 训练数据集：FGR-30k 的合成与真值退化图生成

由于缺乏细粒度感知监督数据，论文构建了 FGR-30k 数据集，包含 30,000 对局部失真样本与对应的真值退化图。

**合成样本生成**：通过区域交换将扩散模型 SR 输出中的伪影区域“植入”高质量图像：

$$
I_{\mathrm{syn}} = M \odot I_{SR} + (1 - M) \odot I_{GT}
$$

其中 $M$ 为随机掩码或语义掩码，$I_{SR}$ 为含伪影的扩散模型输出，$I_{GT}$ 为清晰图像。该操作在 $I_{GT}$ 的局部区域引入真实世界退化，同时保持其余区域的高质量。

**真值退化图融合**：为获得空间精确的监督信号，融合像素级差异与特征级差异：

$$
M_{\mathrm{gt}} = \mathrm{Normalize}\left( \alpha \cdot \mathrm{Diff}_{\mathrm{pixel}} + (1 - \alpha) \cdot \mathrm{Diff}_{\mathrm{feat}} \right)
$$

其中 $\mathrm{Diff}_{\mathrm{pixel}}$ 为像素级 L1 距离，$\mathrm{Diff}_{\mathrm{feat}}$ 为基于 DINOv3 的特征余弦距离。消融实验（Table 4, Variant A）表明，仅使用像素差异会使 MUSIQ 降至 72.123，验证了高层语义特征差异对泛化能力的关键作用。

---

### 损失函数设计

FinPercep-RM 的训练由三项损失联合驱动：

**密集热图损失**：以 L1 范数监督预测退化图与真值退化图之间的逐像素差异：

$$
\mathcal{L}_{\mathrm{map}} = \mathbb{E}_{(I_{\mathrm{syn}}, M_{\mathrm{gt}}) \sim \mathrm{FGR-30k}} \| M_{\mathrm{fg-pdm}} - M_{\mathrm{gt}} \|_1
$$

**三元组排序损失**：强制质量评分满足 $S_{SR} < S_{\mathrm{syn}} < S_{GT}$ 的顺序关系：

$$
\mathcal{L}_{\mathrm{rank}} = \mathbb{E} \big[ \max(0, m_1 - (S_{\mathrm{syn}} - S_{SR})) + \max(0, m_2 - (S_{GT} - S_{\mathrm{syn}})) \big]
$$

其中 $S_{SR}$、$S_{\mathrm{syn}}$、$S_{GT}$ 分别为原始 SR 输出、合成样本、真实图像的评分，$m_1$、$m_2$ 为间隔超参数。

**锚点对齐损失**：将真实图像的评分对齐到预训练 IQA 模型的输出，防止评分漂移：

$$
\mathcal{L}_{\mathrm{align}} = \mathbb{E}_{(I_{GT}) \sim \mathrm{FGR-30k}} \left[ \| S_{GT} - S_{\mathrm{base}}(I_{GT}) \|_1 \right]
$$

**总损失**：

$$
\mathcal{L}_{\mathrm{total}} = \lambda_{\mathrm{map}} \cdot \mathcal{L}_{\mathrm{map}} + \lambda_{\mathrm{rank}} \cdot \mathcal{L}_{\mathrm{rank}} + \lambda_{\mathrm{align}} \cdot \mathcal{L}_{\mathrm{align}}
$$

---

### 协同进化课程学习（CCL）

直接使用 FinPercep-RM 作为奖励信号会导致训练不稳定（Fig. 1(b) 中浅蓝色曲线振荡剧烈）。CCL 通过两条协同进化路径解决这一稳定性-鲁棒性困境：

![[assets/figures/papers/paper_list_l2678_https_arxiv_org_abs_2512_22647/figures/001_Figure_1.jpg]]
*Figure 1: Motivation for FinPercep-RM and CCL. (a) Standard IQAs lack fine-grained perception and struggle to penalize local distortions, while Ours aligns with human judgment (User Study). (b) The training curves illustrate the stability-robustness dilemma: baseline IQA rewards (blue/purple) converge quickly, while FinPercep-RM (light blue) is oscillatory and unstable. Our complete method (FinPercep-RM w/ CCL, orange) achieves stable and optimal convergence. (c) Visualization of Reward Hacking: baseline rewards (W/ CLIP-IQA, W/ MAN-IQA) produce local artifacts, whereas our results are faithful to the Ground Truth*

1. **奖励模型渐进扩展**：构建一系列诊断能力递增的模型 $\{RM_0, RM_1, ..., RM_N\}$，在 FGR-30k 上分阶段训练，逐步增强其细粒度感知能力。
2. **生成器课程协同进化**：生成器首先使用粗粒度全局奖励 $RM_0$ 进行稳定初始化，随后逐步切换到更严格的 $RM_k$ 版本。

**解耦奖励融合**：在阶段 $k$，奖励信号由全局评分与退化图信息加权融合：

$$
R_k = \lambda_1 \bar{S}_{\mathrm{global}} + \lambda_2 (1 - \widehat{\max}(M_{\mathrm{fg-pdm}}))
$$

其中 $\widehat{\max}(M_{\mathrm{fg-pdm}})$ 为退化图的空间最大值估计，$(1 - \widehat{\max}(\cdot))$ 将局部缺陷强度转化为惩罚项。消融实验（Table 4, Variant C）显示，移除 CCL 后 MUSIQ 从 73.456 降至 71.982，验证了课程学习对稳定训练的必要性。

## 实验与关键发现

### 核心瓶颈验证：全局IQA奖励的奖励黑客现象

RLHF训练真实世界超分（Real-ISR）时，直接使用标准IQA模型（如**CLIP-IQA** (Wang et al., AAAI 2023)、**MANIQA** (Yang et al., CVPR 2022)）作为奖励信号存在根本性缺陷。如Figure 1(a)所示，这些模型仅输出单一全局质量分数，缺乏对局部失真的空间感知能力。当生成器通过策略梯度优化该奖励时，会利用这一盲区产生“奖励黑客”行为——生成器学会产出在全局统计上讨好IQA、但局部充满伪影的图像。Figure 1(c)的可视化结果直接证实：使用CLIP-IQA或MANIQA作为奖励训练时，输出图像出现明显的“绘画式”伪影和局部失真，而Ground Truth则保持自然的纹理结构。

这一现象的因果机制在于：标准IQA的全局评分对局部缺陷不敏感，生成器无需修复局部细节即可获得高奖励，导致优化目标与人类感知真实感发生偏离。FinPercep-RM通过同时输出细粒度感知退化图（Fg-PDM）和经退化图调制的校准全局评分，从奖励函数设计上切断了这一作弊路径。

### 主要定量结果

Table 1汇总了在四个真实世界基准（DrealSR、RealSR、RealLR200、RealLQ250）上，基于REFL框架的RLHF训练方法对比。核心发现如下：

- **跨基准一致性**：将FinPercep-RM作为奖励模型（w/ Ours）应用于DiffBIR、SeeSR和DiT4SR三种生成器骨干时，在所有四个基准上均达到最佳或次佳性能。以RealLQ250的MUSIQ指标为例，DiT4SR w/ Ours达到73.456，相比使用CLIP-IQA奖励的版本（70.456）提升+3.0，相比使用MANIQA奖励的版本亦有显著提高。
- **感知-失真权衡**：w/ Ours在降低LPIPS（感知距离）的同时提升MUSIQ、MANIQA、ClipIQA、LIQE等无参考质量指标，表明方法在提升感知质量的同时未引入额外失真。
- **训练策略对比**：Table 3进一步比较了不同RLHF策略。直接使用IQA作为奖励（w/ IQA）虽能提升部分IQA指标，但LPIPS往往劣化，验证了奖励黑客的存在。FinPercep-RM配合CCL则在所有指标上取得最优平衡。

### 用户主观研究

Table 2的用户偏好测试从真实感和保真度两个维度验证了方法的感知优势。以DiT4SR为生成器骨干时：

- 相比DiffBIR，84.2%的用户偏好w/ Ours的真实感，80.1%偏好其保真度；
- 相比SeeSR，真实感偏好率达85.3%，保真度偏好率为72.6%；
- 相比DreamClear，真实感和保真度偏好率分别为76.4%和74.2%。

这一结果与Figure 1(a)中FinPercep-RM与人类判断高度对齐的结论一致——奖励模型越接近人类感知，其引导的生成器输出越能在主观测试中胜出。

### 消融实验：CCL与特征差异的关键作用

Table 4的消融实验揭示了两个关键设计的作用机制：

**CCL的稳定性保障**：Variant C移除了协同进化课程学习，直接使用完整的FinPercep-RM训练生成器。此时RealLQ250的MUSIQ从73.456降至71.982，降幅显著。这与Figure 1(b)的训练曲线一致：直接使用FinPercep-RM（浅蓝色曲线）奖励信号方差大、训练振荡剧烈，而CCL（橙色曲线）通过从粗到细的课程设计，在早期用低复杂度RM提供稳定初始化，后期逐步引入细粒度监督，实现了稳定收敛且最优的最终性能。

**特征差异对泛化的贡献**：Variant A在训练奖励模型时仅使用像素级差异（移除DINOv3特征级差异）生成真值退化图，MUSIQ降至72.123。这表明高层语义特征差异能捕获像素空间无法感知的感知退化（如纹理紊乱、伪影模式），对奖励模型的泛化能力至关重要。仅依赖像素差异会导致退化图对复杂失真的定位不准确，进而削弱对生成器的约束。

### 奖励融合策略分析

Sec. 4.3的解耦奖励融合实验（Table 4相关变体）验证了全局评分与退化图信息的互补性。最终奖励信号采用 $R_k = \lambda_1 \bar{S}_{\text{global}} + \lambda_2 (1 - \widehat{\max}(M_{\text{fg-pdm}}))$ 的形式，其中第二项利用退化图的最大值作为局部惩罚因子。移除退化图项（仅使用全局评分）时性能下降，证实了空间局部缺陷信息对抑制奖励黑客的必要性。

### 定性分析

Figure 4的视觉对比展示了在RealSR数据集上的重建效果。w/ Ours的方法在纹理区域的真实感显著优于对比方法：DiffBIR和SeeSR在细纹理区域（如毛发、织物）出现模糊或过度平滑，而w/ Ours保持了清晰的纹理结构，同时避免了w/ IQA方法中常见的伪影。这与Fg-PDM能够精确定位局部失真区域（Figure 1(a)）的能力直接相关——生成器在训练中被迫修复退化图高响应区域，从而在局部细节上逼近Ground Truth。

### 实验公平性说明

评估覆盖四个真实世界基准及用户主观测试，比较对象包括DiffBIR、SeeSR、DiT4SR、DreamClear等多种SOTA方法，所有方法均在REFL的统一RLHF框架下进行公平对比。消融实验中所有变体使用与完整模型相同的训练设置。

![[assets/figures/papers/paper_list_l2678_https_arxiv_org_abs_2512_22647/figures/005_Table_1.jpg]]
*Table 1: Quantitative results of Real-ISR methods on four real-world benchmarks based on RLHF method of REFL [44]. Best and second best results are highlighted in red and blue, respectively. w/Ours achieves the best or comparable performance across four benchmarks*

![[assets/figures/papers/paper_list_l2678_https_arxiv_org_abs_2512_22647/figures/007_Table_3.jpg]]
*Table 3: Comparison of training strategies under IQA guidance vs. our method. Higher is better for all metrics*

![[assets/figures/papers/paper_list_l2678_https_arxiv_org_abs_2512_22647/figures/009_Table_4.jpg]]
*Table 4: Ablation results on RealLQ250 for our DiT4SR. All variants are trained using the same settings as the full model*

## 定位与知识库关联

### 1. 核心基线与改进路径

FinPercep-RM 的提出直接针对基于强化学习的真实世界超分辨率（Real-ISR）中“奖励黑客”（reward hacking）这一结构性瓶颈。在本文工作之前，RLHF 微调生成器的主流范式是采用预训练的**无参考图像质量评估（NR-IQA）**模型作为奖励信号，典型代表包括 **CLIP-IQA**（Wang et al., AAAI 2023）和 **MANIQA**（Yang et al., CVPR 2022）。这些模型仅输出单一的全局质量评分 $S_{\text{global}}$，其根本缺陷在于**缺乏空间细粒度感知能力**——它们无法区分“整体质量尚可但局部存在严重伪影”的图像与真正高质量的图像。这导致生成器在策略优化过程中学会利用评分函数的盲区，产生局部纹理扭曲、绘画式伪影等“高分低质”的输出（见 Figure 1(c) 的可视化证据）。

FinPercep-RM 对这一范式的改进体现在两个关键维度：

- **输出粒度的根本性升级**：从单一的全局评分扩展为 $\{S_{\text{fgc-global}}, M_{\text{fg-pdm}}\}$ 的互补信号对。其中 $M_{\text{fg-pdm}}$ 是空间分辨率与输入图像一致的细粒度感知退化图（Fine-grained Perceptual Degradation Map），能够逐像素地定位和量化局部失真（Equation 1）。更关键的是，全局评分 $S_{\text{fgc-global}}$ 的计算并非独立于退化图，而是通过将 $M_{\text{fg-pdm}}$ 插值后与最深层的全局特征 $f_N$ 进行逐元素调制（$\odot$），再经由 MLP 回归得到（Equation 2）。这种**显式的因果依赖**迫使全局评分对局部缺陷保持本质敏感，从结构上封堵了 reward hacking 的捷径。

- **训练策略的协同进化**：现有方法通常使用固定的奖励模型直接训练生成器。本文揭示了直接使用 FinPercep-RM 会导致训练不稳定（Figure 1(b) 浅蓝色曲线），原因在于细粒度奖励信号的方差远大于全局 IQA 评分，策略梯度估计的噪声显著增加。为此提出的**协同进化课程学习（CCL）**通过两条共演化路径——奖励模型的渐进式参数扩展（从粗到细的 $\{RM_0, RM_1, ..., RM_N\}$ 序列）和生成器的课程协同进化——在早期阶段优先保证训练稳定性，随后逐步引入更严格的细粒度监督，最终在稳定性和鲁棒性之间取得最优平衡。

### 2. 与相关工作谱系的关系

#### 2.1 在 IQA 研究谱系中的定位

FinPercep-RM 的编码器-解码器架构借鉴了 IQA 领域从全局评分向空间感知扩展的趋势，但其设计目标与现有工作存在本质差异。传统的空间敏感 IQA 方法（如学习局部注意力图来加权全局评分）通常服务于“更准确地预测人类主观评分”这一目标。而 FinPercep-RM 的 $M_{\text{fg-pdm}}$ 被设计为**RL 训练中的可微分诊断信号**——它不仅要准确，还要能够通过解耦融合公式 $R_k = \lambda_1 \bar{S}_{\text{global}} + \lambda_2 (1 - \widehat{\max}(M_{\text{fg-pdm}}))$（Section 4.3, Table 4）向生成器传递有效的梯度信息。这种“为策略优化而设计”的导向使其区别于传统的 IQA 精度竞赛。

#### 2.2 在 RLHF 训练策略谱系中的定位

CCL 的课程学习思想与 RL 训练中的奖励塑形（reward shaping）和课程强化学习有一定关联，但其独特之处在于**奖励模型本身也在进化**。这不同于固定奖励函数下的逐步难度递增，也不同于对抗训练中判别器与生成器的交替更新。CCL 的两条路径——$RM_k$ 的参数扩展和 $G_\theta$ 的策略更新——是解耦但同步的：$RM_k$ 在 FGR-30k 数据集上通过分阶段训练获得逐步增强的诊断能力，而 $G_\theta$ 则在不同阶段接收由对应 $RM_k$ 产生的不同粒度的奖励信号。这种设计避免了判别器-生成器交替训练中常见的模式崩溃问题，同时保留了逐步收紧约束的课程效果。

#### 2.3 在 Real-ISR 系统谱系中的定位

本文的实验将 FinPercep-RM 与三种不同架构的 Real-ISR 生成器集成：**DiffBIR**、**SeeSR** 和 **DiT4SR**。结果表明，无论底层生成器是基于扩散模型还是 Transformer，FinPercep-RM + CCL 的组合均能一致地提升感知质量指标（Table 1，在四个真实世界基准上达到最佳或次佳）并降低 LPIPS 失真。这表明该方法具有较强的**模型无关性（model-agnostic）**——奖励模型的改进可以作为一种即插即用的 RLHF 训练策略增强，而非与特定生成器架构绑定。

### 3. 关键支撑数据集的贡献

**FGR-30k** 数据集是 FinPercep-RM 训练的基础设施，其构建方法本身也是一项方法论贡献。与现有 IQA 数据集（通常只提供全局 MOS/DMOS 标签）不同，FGR-30k 通过区域交换合成策略（Equation 3: $I_{\text{syn}} = M \odot I_{SR} + (1-M) \odot I_{GT}$）生成了 30,000 对包含局部失真的样本，并通过融合像素级 L1 距离和 DINOv3 特征级余弦距离（Equation 4）生成空间密集的真值退化图 $M_{\text{gt}}$。消融实验（Table 4, Variant A）表明，仅使用像素差异训练会使 MUSIQ 从 73.456 降至 72.123，验证了高层语义特征差异对退化图泛化能力的关键作用。

### 4. 适用边界与局限

从方法设计和实验覆盖范围可以推断以下适用边界：

- **依赖 RLHF 训练框架**：FinPercep-RM 的核心价值体现在作为 RL 奖励模型抑制 reward hacking，若直接用于传统的监督训练（如 L1/L2 损失），其细粒度感知能力的优势无法充分发挥。
- **对初始生成器质量有一定要求**：FGR-30k 的合成依赖于扩散模型输出的伪影区域，这意味着 FinPercep-RM 的训练分布偏向于“扩散模型典型失真”的检测。对于其他类型生成器（如纯 GAN）产生的不同分布伪影，泛化能力需要进一步验证——论文未提供此类跨生成器类型的奖励模型迁移实验。
- **CCL 的阶段数量和调度策略**：论文未详细讨论 $N$（RM 序列长度）的选择依据和各阶段切换的自动化机制，这在实际部署中可能需要手动调参。

### 5. 开放问题

1. **奖励模型的跨架构泛化**：FinPercep-RM 在 FGR-30k 上训练，其合成失真主要来自扩散模型。当底层生成器架构发生根本性变化（如纯 CNN-based 或 GAN-based SR）时，$M_{\text{fg-pdm}}$ 的检测精度是否会显著退化？是否需要针对不同生成器类型分别构建 FGR 数据集？

2. **CCL 的自动化调度**：当前 CCL 的阶段划分似乎是预定义的。是否可以通过监测奖励方差或策略梯度范数来自适应地触发阶段切换，从而减少人工干预？

3. **细粒度奖励信号的边际收益**：Table 4 显示解耦融合中 $\lambda_2$（退化图项的权重）的存在使性能从 71.982 提升至 73.456。但退化图信息的更精细利用方式（如按区域加权而不是仅取全局最大值）是否能带来进一步增益，尚未被探索。

4. **与偏好优化方法的结合**：FinPercep-RM 目前用于基于策略梯度的 RL 训练（REFL）。将其输出的 $\{S_{\text{fgc-global}}, M_{\text{fg-pdm}}\}$ 整合到直接偏好优化（DPO）等无需显式奖励模型的 RLHF 变体中，是否可能进一步简化训练流程并保持细粒度感知的优势？

## 原文 PDF

![[paperPDFs/CVPR_2026/FinPercep_RM_A_Fine_grained_Reward_Model_and_Co_evolutionary_Curriculum_for_RL_based_Real_world_Super_Resolution.pdf]]
