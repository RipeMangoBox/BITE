---
title: "Motion Attribution for Video Generation"
type: paper
paper_level: A
venue: ICML
year: 2026
pdf_ref: paperPDFs/ICML_2026/Motion_Attribution_for_Video_Generation.pdf
aliases:
- MMAVG
- MAVG
tags:
- ICML_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/generative_models_and_autoencoders
core_operator: "运动感知的梯度加权（通过在损失空间应用逐位置运动幅度掩码）与帧长度归一化机制，使得归因信号聚焦于动态区域并校正视频长度偏差，从而影响训练子集的选择。"
primary_logic: "通过光流估计的运动幅度构造损失掩码，将梯度计算重新加权到动态区域，可以分离运动影响与外观影响，进而以可扩展的梯度相似度排序识别出对特定运动模式最具影响力的训练片段，实现仅用10%数据微调即可显著提升生成视频的运动平滑性和物理合理性。"
claims:
- "在VBench评估中，Motive在动态度（Dynamic Degree）上达到47.6%，显著优于随机选择（41.3%）和全视频归因（43.8%），并且以仅10%的数据量匹配或超过全数据集微调性能。"
- "人类评估显示，Motive引导选择的数据微调模型相对于预训练基模型获得74.1%的胜率，相对于全量微调模型获得53.1%的胜率。"
- "在更大规模的模型Wan2.2-TI2V-5B上也验证了泛化性，Motive在运动平滑度等指标上维持或超越基模型，证明方法不依赖于特定架构。"
- "帧长度归一化消除视频长度偏差，使排名与视频长度的相关性下降54.0%，从而避免长视频获得虚假的高影响分。"
---

# Motion Attribution for Video Generation

> [!tip] 核心洞察
> 通过光流估计的运动幅度构造损失掩码，将梯度计算重新加权到动态区域，可以分离运动影响与外观影响，进而以可扩展的梯度相似度排序识别出对特定运动模式最具影响力的训练片段，实现仅用10%数据微调即可显著提升生成视频的运动平滑性和物理合理性。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 视频生成中的运动归因 |
| 英文题名 | Motion Attribution for Video Generation |
| 会议/期刊 | ICML 2026 |
| Links | [paper](https://arxiv.org/abs/2601.08828); [Project](https://research.nvidia.com/labs/sil/projects/MOTIVE/) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/generative_models_and_autoencoders |
| Method | Motive (MOTIon attribution for Video gEneration) |
| Dataset | VBench, Human Evaluation, Wan2.2-TI2V-5B (VBench) |

> [!tip] 效果简介
> - VBench 上，Dynamic Degree 为 47.6%，对比 41.3% (Random) / 43.8% (Ours w/o MM)，变化 +6.3 pp / +3.8 pp。
> - Human Evaluation 上，Win rate vs Base 为 74.1%，对比 25.9%，变化 +48.2 pp。
> - Human Evaluation 上，Win rate vs Full FT 为 53.1%，对比 46.9%，变化 +6.2 pp。

## 概述

**核心问题**：现有扩散模型的数据归因方法仅适用于图像，无法区分视频中的动态运动与静态外观，且无法高效扩展到大规模视频生成模型，导致难以识别和选择对运动质量有积极影响的训练样本。

**方法定位**：本文提出 **Motive（MOTIon attribution for Video gEneration）**——一种运动感知的视频数据归因框架。其核心思路是通过光流估计的运动幅度构造损失掩码，将梯度计算重新加权到动态区域，从而分离运动影响与外观影响；再以可扩展的梯度相似度排序识别出对特定运动模式最具影响力的训练片段。

**关键结论**：
- 在 VBench 评估中，Motive 在动态度（Dynamic Degree）上达到 47.6%，显著优于随机选择（41.3%）和全视频归因（43.8%），且仅使用 10% 数据微调即可匹配或超越全数据集微调性能（Table 1）。
- 人类评估显示，Motive 引导选择的数据微调模型相对于预训练基模型获得 74.1% 的胜率，相对于全量微调模型获得 53.1% 的胜率（Table 2）。
- 方法在更大规模的模型 Wan2.2-TI2V-5B 上也验证了泛化性，运动平滑度等指标维持或超越基模型（Table 5）。
- 帧长度归一化消除了视频长度偏差，使排名与视频长度的相关性下降 54.0%（Figure 5）；投影维度 D'=512 时与完整梯度的 Spearman 相关系数达 74.7%，在牺牲极小的排名质量前提下实现存储和计算可行（Figure 4）。

## 背景与动机

视频生成模型在近年来取得了显著进展，能够根据文本描述合成逼真且时序连贯的视频内容。然而，一个关键问题尚未得到充分解答：**究竟是训练数据中的哪些视频片段影响了生成视频中的特定运动模式？** 这一问题不仅关乎模型行为的可解释性，更直接影响数据策展的效率——如果能识别出对目标运动质量有积极贡献的训练样本，就可以用极少的数据进行针对性微调，从而提升生成视频的运动平滑性和物理合理性。

现有工作主要围绕图像生成模型的数据归因展开。基于影响函数或其梯度近似的方法（如 **Diffusion-ReTrac** (Xie et al., 2024)）通过计算训练样本与测试样本在损失空间中的梯度相似度来量化影响，但这些方法在迁移到视频领域时面临三个根本性障碍。

**第一，运动与外观的信号纠缠。** 图像归因方法对像素空间的所有区域一视同仁，无法区分动态区域与静态背景。在视频中，一个“浮动”运动的查询视频可能与训练集中包含水波荡漾的片段共享相似的动态模式，但传统归因方法可能因为外观相似而错误地赋予静态水面图像更高的影响分数。这种运动信号被外观噪声淹没的现象，使得现有方法无法有效识别运动相关的训练样本。

**第二，视频长度的偏差效应。** 视频片段的帧数从数帧到数百帧不等，而扩散模型的损失函数天然地与时空维度规模相关——帧数越多的视频在梯度计算中产生的量级越大。这导致长视频在归因排名中获得虚假的高影响分，扭曲了真实的数据重要性排序。

**第三，计算可扩展性的瓶颈。** 现代视频扩散模型的参数量通常达到十亿级别（如 Wan2.1-T2V-1.3B 的梯度维度 D ≈ 1.4B），直接存储和比较所有训练样本的完整梯度在计算和存储上都不可行。这使得面向大规模视频数据集的归因分析成为一项工程挑战。

针对上述缺口，本文提出了 **Motive（MOTIon attribution for Video gEneration）**，一个运动感知的视频数据归因框架。其核心动机在于：**通过将归因信号聚焦于动态区域，分离运动影响与外观影响，从而以可扩展的方式识别出对特定运动模式最具影响力的训练片段。** 这一方法使得仅用 10% 的数据进行微调即可显著提升生成视频的运动质量，在 VBench 动态度指标上达到 47.6%，并在人类评估中获得相对于预训练基模型 74.1% 的胜率。

## 核心创新

Motive的核心创新在于将扩散模型的数据归因从静态图像域系统性地迁移到动态视频域，通过三个关键机制解决了视频生成中运动质量的可归因性问题。

### 1. 运动感知的梯度加权：从均匀损失到动态聚焦

传统扩散模型的归因方法对每个空间位置的损失赋予均等权重，无法区分运动区域与静态背景。Motive引入**运动幅度掩码**，在损失空间中对梯度计算进行逐位置重加权：

- **运动提取与掩码生成**：使用AllTracker从视频像素空间提取光流位移场，计算每帧每个像素的运动幅度 $M_f(h,w) = \|\mathbf{F}_f(h,w)\|_2$，并通过全局min-max归一化将权重映射到 $[0,1]$ 区间（Eq. 13），再双线性下采样到VAE潜在空间分辨率（Eq. 14）。
- **运动加权损失**：在潜在空间中，逐位置计算噪声预测误差，并以运动掩码加权平均，得到运动感知损失 $\mathcal{L}_{\mathrm{mot}}$（Eq. 16）。该损失对高运动区域的预测误差赋予更高权重，对静态背景区域则近乎忽略。
- **因果机制**：这一设计使得梯度信号 $\mathbf{g}_{\mathrm{mot}} = \nabla_\theta \mathcal{L}_{\mathrm{mot}}$ 聚焦于动态区域，从而在计算影响分数时，训练样本对查询视频运动模式的贡献被有效分离于外观贡献。

消融实验证实了该机制的因果效应：去除运动掩码后（Ours w/o MM），VBench动态度从47.6%下降至43.8%（Table 1），表明运动掩码是性能提升的核心驱动因素。

### 2. 帧长度归一化：消除视频时长偏差

视频数据天然存在帧数差异，导致长视频的梯度量级系统性偏大，在归因排序中获得虚假的高影响分。Motive通过**帧长度归一化**（Eq. 11）直接校正这一偏差：

$$\nabla_\theta \mathcal{L}_{\mathrm{diff}} \gets \frac{1}{F} \nabla_\theta \mathcal{L}_{\mathrm{diff}}$$

其中 $F$ 为视频帧数。该操作将梯度量级归一化到“每帧平均贡献”的尺度，确保不同长度的视频在影响排序中公平比较。

实验证据表明，应用帧长度归一化后，排名与视频长度的相关性下降**54.0%**（Figure 5）。定性对比显示，未归一化时排名靠前的样本缺乏一致的运动模式，而归一化后顶部样本均呈现与查询一致的浮动运动（波浪、漂浮物、冲浪等）。

### 3. 可扩展的梯度投影与方差控制

视频扩散模型的参数量通常达到数十亿级别，完整梯度的存储和比较在计算上不可行。Motive通过两项设计实现可扩展性：

- **Fastfood随机投影**：将高维梯度（$D \approx 1.4\text{B}$）通过结构化随机矩阵 $\mathbf{P}$ 压缩至 $D'=512$ 维（Eq. 8），并归一化到单位球（Eq. 10）。投影后梯度间的余弦相似度近似原始梯度相似度。消融显示 $D'=512$ 时与完整梯度的Spearman相关系数达**74.7%**（Figure 4），存储需求降低百万倍。
- **单样本方差控制**：固定单一时间步 $t_{\mathrm{fix}}=751$ 与共享噪声 $\epsilon_{\mathrm{fix}}$，对所有训练-查询对使用相同采样（Eq. 7），避免多样本平均带来的方差和计算开销。单步与多步平均的排名一致性达到Spearman $\rho=66\%$（§4.4, App. F.1），表明单步足以保持相对顺序。

### 4. 多查询多数投票聚合

针对实际应用中需要同时优化多种运动模式的需求，Motive引入**多数投票聚合**机制（Eq. 18）：对每个候选训练视频，统计其跨 $Q$ 个查询的影响分数超过阈值 $\tau$ 的次数，选择得票最多的Top-K样本。这一设计使得选出的子集能够同时覆盖多种运动模式，避免单查询选择的过拟合风险。

综上，Motive的创新本质在于：**通过运动掩码将梯度信号从“全图均匀”重构为“动态加权”，通过帧长度归一化消除视频域特有的时长偏差，并通过投影和方差控制使该方法在十亿参数规模上可行**。这三项changed slots共同构成了从“图像归因”到“视频运动归因”的方法论跨越。

## 整体框架

![[assets/figures/papers/paper_list_l20_https_arxiv_org_abs_2601_08828/figures/001_Figure_1.jpg]]
*Figure 1: Motive. Top. Motion-gradient computation (§3.4) has three steps: (1) detect motion with AllTracker; (2) compute motion-magnitude patches; (3) apply loss-space motion masks to focus gradients on dynamic regions. Bottom. Our method (§3.2) is made scalable via a single-sample variant with common randomness and a projection, computed for each pair of training and query data, aggregated (§3.5) for a final ranking, and eventually used to select fine-tuning subsets*

Motive 的整体框架围绕一个核心目标构建：**将训练数据对视频生成模型运动质量的影响，从静态外观的影响中解耦出来，并以可扩展的方式量化**。该框架包含两条正交但协同的技术路径——运动感知梯度计算与可扩展归因管道——最终输出一个训练样本的排序列表，用于指导数据筛选与微调。

### 运动感知梯度计算

运动感知梯度的计算是 Motive 区别于传统图像归因方法的关键创新。其流程分为三个紧密衔接的步骤（见 Figure 1 顶部）：

1. **运动提取**：使用 **AllTracker**（Harley et al., 2025）从原始视频像素空间提取逐帧的光流位移场 $D_f(h,w)$、可见性和置信度信息，输出张量 $A \in \mathbb{R}^{F \times H \times W \times 4}$。这一步为后续的运动幅度量化提供了精确的时空运动表征。

2. **运动幅度掩码生成**：基于光流位移计算每帧每个像素的运动幅度 $M_f(h,w) = \|D_f(h,w)\|_2$，随后进行**全局 min-max 归一化**（Eq. 13），将幅度值映射到 $[0,1]$ 区间，以消除绝对运动尺度的偏差并突出相对运动显著性。归一化后的权重通过双线性下采样（Eq. 14）对齐到 VAE 潜在空间的分辨率，得到逐位置的掩码权重 $\tilde{W}(f,\tilde{h},\tilde{w})$。

3. **损失空间运动加权**：在潜在空间计算每个位置的噪声预测误差 $\tilde{\mathcal{L}}_{\theta,\mathbf{v},\mathbf{c}}$，并用运动掩码进行逐位置加权平均，得到运动感知损失 $\mathcal{L}_{\mathrm{mot}}$（Eq. 16）。该损失函数的梯度 $\mathbf{g}_{\mathrm{mot}} = \nabla_{\theta} \mathcal{L}_{\mathrm{mot}}$ 天然聚焦于动态区域，而静态背景区域因掩码权重趋近于零被有效抑制。值得强调的是，该加权仅作用于归因阶段的梯度计算，**不改变模型的前向加噪与生成过程**，从而避免了运动加权与噪声注入之间的潜在交互。

### 可扩展归因管道

现代视频生成模型的参数量通常达到数十亿级别，直接存储和比较完整梯度（如本文使用的模型梯度维度 $D \approx 1.4\text{B}$）在计算和存储上均不可行。Motive 通过以下技术组合实现了可扩展性（见 Figure 1 底部）：

- **方差控制与单步采样**：固定单一时间步 $t_{\mathrm{fix}} = 751$ 和共享噪声 $\epsilon_{\mathrm{fix}}$，对所有训练样本和查询视频使用相同的采样配置。这一设计消除了多时间步平均带来的方差，同时大幅降低计算成本。消融实验证实，单步采样与多步平均的排名 Spearman 相关系数达到 $\rho = 66\%$，足以保持样本间的相对顺序。

- **帧长度归一化**：视频帧数 $F$ 的差异会导致梯度量级的系统性偏差——长视频天然获得更大的梯度范数，从而在归因排名中获得虚假的高影响分。Motive 对每个视频的扩散损失梯度乘以 $1/F$（Eq. 11），将梯度量级校正到“每帧平均”的尺度。消融实验表明，该操作使排名与视频长度的相关性下降 54.0%，有效消除了长视频偏差。

- **Fastfood 随机投影**：通过结构化随机投影矩阵 $\mathbf{P}$（Eq. 8）将高维梯度 $\nabla_{\theta}\mathcal{L}_{\mathrm{diff}}$ 压缩至 $D' = 512$ 维，并进一步归一化到单位球上（Eq. 9-10）。投影维度消融显示，$D' = 512$ 时与完整梯度的 Spearman 相关系数达 74.7%，在存储需求降低百万倍的前提下保持了排名质量。

### 影响分数计算与多查询聚合

对于任意一对训练视频 $\mathbf{v}_n$ 和查询视频 $\hat{\mathbf{v}}$，Motive 通过计算两者运动感知投影梯度 $\tilde{\mathbf{g}}_{\mathrm{mot}}$ 的内积来定义影响分数（Eq. 17）：
$$I_{\mathrm{mot}}(\mathbf{v}_n, \hat{\mathbf{v}}) = \tilde{\mathbf{g}}_{\mathrm{mot}}(\theta, \hat{\mathbf{v}})^{\top} \tilde{\mathbf{g}}_{\mathrm{mot}}(\theta, \mathbf{v}_n)$$

为进一步提升选择的鲁棒性，Motive 引入了**多数投票聚合机制**（Eq. 18）：给定 $Q$ 个查询视频，当候选训练样本对某个查询的影响分数超过阈值 $\tau$ 时，其计数器加 1。最终根据多数投票计数选出 Top-K 个最具共识的训练样本。这种聚合策略使得 Motive 能够从多个运动查询中提取一致的归因信号，而非依赖单一查询的噪声估计。

### 数据流与模块关系总结

从端到端视角，Motive 的输入输出流可概括为：

1. **输入**：训练视频集 $\{\mathbf{v}_n\}_{n=1}^{N}$ 和查询视频集 $\{\hat{\mathbf{v}}_q\}_{q=1}^{Q}$。
2. **运动提取模块**：对每个视频运行 AllTracker，生成光流与运动幅度。
3. **梯度计算模块**：对每个视频计算运动加权损失 $\mathcal{L}_{\mathrm{mot}}$，反向传播得到运动感知梯度，经帧长度归一化后通过 Fastfood 投影并归一化存储。
4. **影响计算模块**：计算所有训练-查询对的投影梯度内积，得到影响分数矩阵。
5. **聚合与排序模块**：通过多数投票聚合多查询影响，输出 Top-K 训练样本排序列表。
6. **下游应用**：使用选出的子集对预训练视频生成模型进行微调。

整个管道中，梯度计算成本（约 150 GPU 小时 / 10k 样本）可一次性摊销于后续任意数量的查询，且通过多 GPU 并行可进一步缩短墙钟时间。这种设计使得 Motive 在保持归因精度的同时，具备了面向大规模视频数据集的实用可扩展性。

## 核心模块与公式推导

Motive 的核心架构由三个紧密耦合的模块构成：**运动掩码生成**、**运动感知梯度计算**，以及支撑大规模部署的**高效梯度投影与归一化**。以下逐一展开其关键公式与设计机理。

### 运动掩码生成

该模块的目标是从原始视频中提取运动信息，并将其转化为损失空间中的逐位置权重，使梯度计算聚焦于动态区域而非静态外观。

首先，使用 AllTracker 在像素空间提取光流与可见性信息：

$$A = \mathcal{A}(\mathbf{v}) \in \mathbb{R}^{F \times H \times W \times 4}$$

其中前两个通道为位移向量 $\mathbf{D}_f(h,w) = (A_{f,h,w,0}, A_{f,h,w,1})$，后两个通道编码可见性与置信度。运动幅度定义为位移的 $L_2$ 范数：

$$M_f(h,w) = \|\mathbf{D}_f(h,w)\|_2$$

为消除绝对运动尺度的偏差，对全视频所有帧和像素进行 min-max 归一化，将权重压缩至 $[0,1]$：

$$\mathbf{W}(f,h,w) = \frac{M_f(h,w) - \min_{f',h',w'} M_{f'}(h',w')}{\max_{f',h',w'} M_{f'}(h',w') - \min_{f',h',w'} M_{f'}(h',w') + \zeta}$$

其中 $\zeta = 10^{-6}$ 防止除零。随后通过双线性下采样将运动权重对齐到 VAE 潜在空间分辨率：

$$\tilde{\mathbf{W}}(f,\tilde{h},\tilde{w}) = \text{Bilinear}\left(\mathbf{W}(\cdot,\cdot,\cdot), F, \frac{H}{s}, \frac{W}{s}\right)$$

其中 $s$ 为 VAE 下采样倍数。

### 运动感知损失与梯度

运动感知损失在潜在空间计算逐位置噪声预测误差，并以运动掩码加权平均：

$$\mathcal{L}_{\mathrm{mot}}(\theta; \mathbf{v}, \mathbf{c}) = \frac{1}{F_{\mathbf{v}}} \mathrm{mean}_{f,\tilde{h},\tilde{w}} \left[ \tilde{\mathbf{W}}_{\mathbf{v},\mathbf{c}}(f,\tilde{h},\tilde{w}) \cdot \tilde{\mathcal{L}}_{\theta,\mathbf{v},\mathbf{c}}(f,\tilde{h},\tilde{w}) \right]$$

其中 $\tilde{\mathcal{L}}_{\theta,\mathbf{v},\mathbf{c}}$ 是扩散模型在潜在空间每个位置的逐元素噪声预测误差，$F_{\mathbf{v}}$ 为视频帧数。该设计的核心洞察在于：**损失空间掩码仅重新加权归因信号，不改变前向加噪与生成过程**，从而避免运动加权与噪声注入之间的交互干扰。

运动感知梯度定义为该损失对模型参数的导数：

$$\mathbf{g}_{\mathrm{mot}} := \nabla_{\theta} \mathcal{L}_{\mathrm{mot}}$$

### 帧长度归一化

视频帧数的差异会导致梯度量级的系统性偏差——长视频天然累积更大的梯度范数，从而在影响排序中占据虚假优势。Motive 通过帧长度归一化消除此偏差：

$$\nabla_{\theta} \mathcal{L}_{\mathrm{diff}}(\theta; \mathbf{v}, t_{\mathrm{fix}}, \epsilon_{\mathrm{fix}}) \gets \frac{1}{F} \nabla_{\theta} \mathcal{L}_{\mathrm{diff}}(\theta; \mathbf{v}, t_{\mathrm{fix}}, \epsilon_{\mathrm{fix}})$$

消融实验证实，该归一化使排名与视频长度的相关性下降 54.0%，有效消除了长视频偏差。

### 高效梯度投影与影响得分

为将归因扩展至大规模视频生成模型（完整梯度维度 $D \approx 1.4\text{B}$），Motive 采用 Fastfood 随机投影将梯度压缩至 $D' = 512$ 维：

$$\mathbf{P} := \frac{1}{\xi \sqrt{D'}} \mathbf{S Q G \Pi Q B}$$

投影后的梯度经 $L_2$ 归一化至单位球面：

$$\tilde{\mathbf{g}}(\theta, \mathbf{x}) := \frac{\mathbf{P} \nabla_{\theta} \mathcal{L}_{\mathrm{diff}}(\theta, \mathbf{x}, t_{\mathrm{fix}}, \epsilon_{\mathrm{fix}})}{\|\mathbf{P} \nabla_{\theta} \mathcal{L}_{\mathrm{diff}}(\theta, \mathbf{x}, t_{\mathrm{fix}}, \epsilon_{\mathrm{fix}})\|}$$

为降低方差，Motive 固定单一时间步 $t_{\mathrm{fix}} = 751$ 与共享噪声 $\epsilon_{\mathrm{fix}}$，对所有训练-查询对使用相同采样。消融显示，该单步方案与多步平均的 Spearman 排名相关性达 $\rho = 66\%$，在保持相对顺序的前提下大幅降低计算开销。

运动感知影响得分定义为训练视频与查询视频的归一化投影梯度内积：

$$I_{\mathrm{mot}}(\mathbf{v}_n, \hat{\mathbf{v}}) = \tilde{\mathbf{g}}_{\mathrm{mot}}(\theta, \hat{\mathbf{v}})^{\top} \tilde{\mathbf{g}}_{\mathrm{mot}}(\theta, \mathbf{v}_n)$$

对于多查询场景，采用多数投票聚合以选择最具共识的训练样本：

$$\mathrm{MajVote}_n = \sum_{q=1}^{Q} \mathbb{I}\big[ \mathcal{I}_{\mathrm{mot}}(\mathbf{v}_n, \hat{\mathbf{v}}_q) > \tau \big]$$

其中 $\tau$ 为影响阈值，$Q$ 为查询数量。最终按 $\mathrm{MajVote}_n$ 降序排列，选取 Top-K 样本用于微调。

## 实验与分析

### 主结果：VBench 量化评估

Table 1 报告了在 VBench 基准上的全面对比。所有数据选择方法均使用 10% 的训练数据，Motive 采用跨运动查询的多数投票聚合（§3.5）。核心发现如下：

![[assets/figures/papers/paper_list_l20_https_arxiv_org_abs_2601_08828/figures/005_Table_1.jpg]]
*Table 1: VBench Evaluation. Performance comparison on VBench [Huang et al., 2024] across different baselines (all values in { \% } , higher is better). All selection methods use 10% of training data; our method uses majority vote aggregation (§3.5) across motion queries. MM: motion masking*

- **动态度（Dynamic Degree）**：Motive 达到 **47.6%**，显著优于随机选择（41.3%，+6.3 pp）和去除运动掩码的消融版本 Ours w/o MM（43.8%，+3.8 pp）。这一指标直接衡量生成视频的运动丰富程度，验证了运动感知归因的核心价值。
- **主体一致性（Subject Consistency）**：Motive 取得 **96.3%**，与全量微调（96.4%）持平，说明聚焦运动并未牺牲外观保持能力。
- **美学质量（Aesthetic Quality）**：Motive 达到 **46.0%**，略低于全量微调（47.4%），但优于随机选择（44.1%），表明运动导向的数据筛选对整体视觉质量无负面影响。
- **运动平滑度（Motion Smoothness）**：Motive 为 96.3%，与基模型（96.2%）和全量微调（96.5%）相当，证明仅用 10% 数据即可维持时序连贯性。

值得注意的是，Motive 在仅使用 10% 数据的情况下，在动态度上超越全量微调（47.6% vs. 46.8%），在其他维度上接近或匹配全量微调性能。这直接验证了核心主张：**通过运动感知归因筛选的高影响力子集，其训练效果可媲美甚至超越全数据集**。

### 主结果：人类评估

Table 2 展示了 50 个视频、17 名参与者（共 850 次成对比较）的人类偏好结果：

![[assets/figures/papers/paper_list_l20_https_arxiv_org_abs_2601_08828/figures/006_Table_2.jpg]]
*Table 2: Human evaluation. Pairwise comparisons across 50 videos with 17 participants (850 total). Win, tie, and loss rates show where our method is preferred, rated equal, or outperformed*

- **Motive vs. 基模型**：胜率 **74.1%**，平局 14.1%，负率 11.8%。这表明归因引导的数据选择带来了人类可感知的显著运动质量提升。
- **Motive vs. 全量微调**：胜率 **53.1%**，平局 17.6%，负率 29.4%。Motive 以 10% 数据量微调的模型在人类评判中略微优于全量微调模型，进一步印证了数据质量优于数据数量的论点。

人类评估与 VBench 自动指标形成交叉验证，增强了结论的可信度。

### 跨模型泛化性

Table 5（附录 C）将评估扩展至更大规模的 **Wan2.2-TI2V-5B** 模型。在相同设置下（10% 数据选择，多数投票聚合），Motive 在运动平滑度上维持 97.6（基模型 97.5），在动态度上达到 45.2%（随机选择 42.1%）。这表明运动感知归因方法不依赖于特定模型架构或规模，具备良好的泛化能力。

![[assets/figures/papers/paper_list_l20_https_arxiv_org_abs_2601_08828/figures/011_Table_5.jpg]]
*Table 5: VBench Evaluation on Additional Model. Following the same setting in §4, we extend the VBench [Huang et al., 2024] evaluation to Wan2.2-TI2V-5B, a larger-scale text-to-video model. Random selection and our Motive both select 10% of the training data, with our method using majority vote aggregation (§3.5) across all motion queries. Results demonstrate that Motive generalizes effectively to different models. MM: motion masking*

### 消融分析

#### 运动掩码的关键作用

Table 1 中 **Ours w/o MM**（去除运动掩码，使用全视频级别影响分数）的动态度降至 43.8%，与 Motive 的 47.6% 形成 3.8 pp 的差距。这直接证明：**在损失空间应用逐位置运动幅度掩码，将归因信号聚焦于动态区域，是区分运动影响与外观影响的关键机制**。若不加掩码，归因会混杂静态外观信号，导致筛选出的训练样本对运动质量的提升有限。

#### 投影维度的效率-精度权衡

Figure 4 展示了投影维度 $D'$ 与完整梯度（$D \approx 1.4\text{B}$）之间的 Spearman 秩相关系数曲线。当 $D' = 512$ 时，相关系数达到 **74.7%**，在不牺牲排名质量的前提下将存储需求降低约百万倍（从 1.4B 维降至 512 维）。继续增大 $D'$ 带来的相关性增益边际递减，因此 $D' = 512$ 被选为效率与精度的最优平衡点。这一消融验证了 Fastfood 随机投影在视频扩散模型梯度压缩中的有效性。

#### 帧长度归一化消除时长偏差

Figure 5 以浮动运动查询为例，对比了有无帧长度归一化的排序结果。应用归一化后，排名靠前的训练样本一致展示浮动运动（波浪、漂浮物、冲浪），而未归一化时排序被视频长度偏差主导，靠前样本无一致运动模式。定量上，**帧长度归一化使排名与视频长度的相关性下降 54.0%**，有效消除了长视频因梯度量级更大而获得虚假高影响分的系统性偏差。

#### 单时间步采样的充分性

消融实验（§4.4，附录 F.1）表明，使用单个固定时间步 $t_{\text{fix}} = 751$ 与多时间步平均的排名一致性达到 Spearman $\rho = 66\%$。这一中等偏高的相关性证实单步足以保持训练样本间的相对顺序，同时大幅降低计算开销（从多步平均的 $|T|$ 倍梯度计算降至单次）。

### 定性分析

Figure 2 展示了浮动和滚动两类运动查询的归因案例。高影响力正样本包含清晰、物理合理的动态场景（如漂浮的船只、滚动的球体），而负影响样本多为仅含摄像机运动或卡通风格、与目标运动冲突的内容。Figure 3 进一步对比了压缩、旋转、滑动、自由落体四种运动场景下基模型、随机选择和 Motive 的生成效果，Motive 微调模型在运动幅度和物理合理性上均有明显改善。

Figure 7 的跨运动类别影响重叠热力图揭示了不同运动之间的数据共享规律。例如，弹跳与浮动在 4DNEX 和 VIDGEN 两个数据集上均表现出高重叠（44.4%/46.3%），而自由落体与拉伸的重叠较低（12.8%/12.7%）。这种非对称重叠模式表明，影响模式反映了视频生成模型中运动表示的基本结构，而非数据集的偶然属性。

![[assets/figures/papers/paper_list_l20_https_arxiv_org_abs_2601_08828/figures/013_Figure_7.jpg]]
*Figure 7: Cross-motion influence overlap across datasets. Heatmaps showing the percentage overlap of top-100 influential training samples across motion categories for (a) 4DNEX and (b) VIDGEN datasets. Each cell ( i , j ) shows the percentage of motion category ??’s influential data (aggregated from 5 queries per category) that also appears in motion category $j ^ { \prime }$ s top-100 influential samples. The asymmetric nature of the matrices (e.g., bounce→float $\neq$ float→bounce) arises because different motion categories have different numbers of unique influential videos, leading to directional overlap percentages. Consistent high-overlap pairs (e.g., bounce-float: 44.4%/46.3%) and low-overlap pair...

### 失败模式与局限性

尽管 Motive 在主流指标上表现优异，但以下局限性需在解读结果时注意：

1. **计算开销**：10k 样本的梯度归因约需 150 GPU 小时。虽然该成本可摊销于后续任意数量的查询，且可通过多 GPU 并行缩短，但对于资源受限的场景仍是门槛。
2. **片段级粒度缺失**：当前方法以整个视频为单位计算影响，无法定位到具体发生目标运动的帧或事件片段，可能稀释关键帧的学习信号。
3. **相机运动混淆**：运动掩码可能过度强调摄像机运动。尽管通过空间均匀性检测可降低纯相机平移的权重，但未能真正解耦自运动与物体运动。
4. **CFG 推理偏差**：训练时的归因未考虑分类器自由引导（CFG）在推理阶段对运动的影响，使得训练与推理动态可能存在不一致。
5. **有偏微调风险**：针对特定运动进行有偏微调可能损害模型在其他方面的生成能力，需要在后续工作中建立平衡机制。

### 公平性说明

- 评估使用的查询视频由 Veo-3 合成生成，虽经人工筛选确保清晰度和物理合理性，但可能引入合成域与真实域的分布差异。
- 多数投票聚合时使用的百分位阈值 $\tau$ 未在论文中明确公开，可能影响完全可复现性。
- 所有对比基线均使用相同的 10% 数据预算和相同的微调超参数（分辨率 $480 \times 832$，学习率 $1 \times 10^{-5}$，仅更新 DiT 骨干），确保了比较的公平性。

### 补充图表

![[assets/figures/papers/paper_list_l20_https_arxiv_org_abs_2601_08828/figures/003_Figure.jpg]]
*Figure: Prompt: A rubber ball being compressed under a flat press, filmed with a stationary camera. Bright,shadow-free lighting and a clean background emphasize the deformation as it flattens. Prompt: A single coin spins quickly on a polished glass surface, close-up fixed camera,bright even lighting, plain backdrop; capture its precession and slow wobble as it settles*

![[assets/figures/papers/paper_list_l20_https_arxiv_org_abs_2601_08828/figures/004_Figure.jpg]]

![[assets/figures/papers/paper_list_l20_https_arxiv_org_abs_2601_08828/figures/012_Figure_6.jpg]]
*Figure 6: Motive is not simply selecting “motion-rich" clips. Our influence scores are computed via gradients, and training videos are considered influential only when they directly improve the model’s ability to generate the target motion dynamics, not because they contain more motion overall*

![[assets/figures/papers/paper_list_l20_https_arxiv_org_abs_2601_08828/figures/009_Table_3.jpg]]
*Table 3: Glossary and notation*

![[assets/figures/papers/paper_list_l20_https_arxiv_org_abs_2601_08828/figures/010_Table_4.jpg]]
*Table 4: Glossary and notation (continued)*

![[assets/figures/papers/paper_list_l20_https_arxiv_org_abs_2601_08828/figures/015_Figure_8.jpg]]
*Figure 8: Illustration of motion query set. We generate near-realistic video queries with Veo-3 across ten motion categories. Each category contains five query videos synthesized with controlled prompts and manually screened for clarity and physical plausibility. Table 6: Runtime Breakdown. Detailed computational complexity and runtime for each component of our motion attribution framework on 10k training samples with Wan2.1-T2V-1.3B model*

![[assets/figures/papers/paper_list_l20_https_arxiv_org_abs_2601_08828/figures/016_Table.jpg]]

## 方法谱系与知识库定位

### 1. 问题定位：从图像归因到视频运动归因的跨越

Motive 的核心贡献在于将扩散模型的数据归因方法从静态图像域首次系统性地拓展至视频运动域。现有扩散模型归因方法（如 **Diffusion-ReTrac** (Xie et al., 2024) 和 **TRAK** (Park et al., 2023)）虽然在图像生成中有效，但面临三个视频特有问题：(1) 无法区分动态运动与静态外观对梯度的贡献；(2) 视频帧数差异导致梯度量级偏差；(3) 高维梯度存储和计算开销使大规模视频模型不可行。Motive 通过运动感知梯度加权、帧长度归一化和随机投影压缩三个技术模块，将归因信号聚焦于动态区域，使视频运动质量的数据溯源成为可能。

### 2. 方法谱系中的定位

#### 2.1 与扩散模型数据归因方法的关系

Motive 继承并改造了扩散模型归因的基本范式——基于梯度相似度的影响估计。与 **Diffusion-ReTrac** 采用多时间步、多噪声样本平均的策略不同，Motive 证明了单固定时间步（$t_{\text{fix}}=751$）与共享噪声 $\epsilon_{\text{fix}}$ 足以保持排名一致性（Spearman $\rho=66\%$），这大幅降低了计算开销。此外，Motive 用 Fastfood 随机投影替代了完整 Hessian 逆矩阵的估计，将梯度维度从 $D \approx 1.4\text{B}$ 压缩至 $D'=512$，同时保持与完整梯度的 Spearman 相关系数达 74.7%。这种身份预条件子（identity preconditioner）加投影的策略在计算可行性与归因精度之间取得了实用平衡。

#### 2.2 与视频运动表征方法的关系

Motive 的运动感知机制依赖于光流估计。论文选用 **AllTracker** (Harley et al., 2025) 从像素空间提取光流位移、可见性和置信度，而非直接在潜在空间建模运动。这一设计选择将运动提取与生成模型解耦，使得运动掩码可独立计算并下采样到 VAE 潜在空间。与直接使用 **V-JEPA** (Assran et al., 2025) 等自监督时空嵌入进行数据选择的方法相比，Motive 的运动加权损失直接作用于梯度空间，而非仅依赖表征相似度，因此能更精确地识别对特定运动模式有因果影响的训练样本。

#### 2.3 在视频生成数据策展中的位置

Motive 属于**基于影响函数的数据选择**范式，与基于启发式规则（如平均运动幅度）或基于表征聚类（如 V-JEPA 嵌入）的方法形成对比。实验表明，仅基于运动幅度选择高动态视频（Motion magnitude baseline）无法有效提升运动质量，因为高幅度不一定对应目标运动模式的可迁移性。Motive 通过梯度空间的余弦相似度，识别的是那些能直接改善模型对特定运动生成能力的训练样本，而非仅仅"运动丰富"的样本。

### 3. 适用边界与局限

#### 3.1 计算开销与可扩展性

尽管 Motive 通过投影和单步采样大幅降低了存储和计算需求，其梯度计算成本仍然较高——10k 样本约需 150 GPU 小时。这一开销可摊销于后续任意数量的查询，且可通过多 GPU 并行加速，但对于超大规模数据集（百万级以上），前期资源投入仍然可观。论文未讨论在更大规模数据集上的计算可行性验证。

#### 3.2 运动粒度的局限

当前方法以整个视频为单位进行归因，无法定位到具体发生目标运动的片段或事件。对于包含多种运动模式的视频，其影响分数可能被不相关片段稀释。论文明确指出这一局限，并提出了片段级归因的开放方向。

#### 3.3 相机运动与物体运动的混淆

运动掩码基于光流幅度构建，无法区分相机自运动（如平移、旋转）与场景内物体运动。虽然论文通过空间均匀性检测对全局运动进行了降权，但未能真正解耦两种运动源。这可能导致相机运动主导的视频获得虚高的影响分数，而精细物体运动的贡献被低估。

#### 3.4 训练-推理分布偏移

Motive 在训练时未考虑分类器自由引导（CFG）对推理动态的影响。由于 CFG 在推理时放大条件信号，训练时的归因排序可能与实际推理行为存在偏差。这是扩散模型归因方法的共性问题，但在视频运动场景下尤为关键，因为 CFG 强度直接影响运动幅度和物理合理性。

#### 3.5 有偏微调的风险

针对特定运动类别进行数据选择和微调可能损害模型在其他方面的生成能力。论文在通用模型（generalist）实验中采用了跨类别多数投票聚合来缓解这一问题，但未系统评估运动专项微调对非目标运动类型、主体一致性或文本跟随能力的负面影响。

### 4. 开放问题与未来方向

1. **细粒度运动归因**：如何实现片段级或事件级归因，捕获运动轨迹中不同阶段（加速、匀速、减速）的学习信号？这需要将时间定位机制引入影响估计框架。

2. **相机运动解耦**：如何完全解耦相机自运动与物体运动？可能的路径包括利用 AllTracker 的置信度通道、引入相机运动估计模块，或在光流空间中显式建模运动层。

3. **CFG 一致性**：如何将分类器自由引导纳入影响估计，使训练时的归因排序与推理时的实际行为一致？这可能需要建模 CFG 对梯度方向的非线性调制效应。

4. **跨模态拓展**：Motive 的运动感知归因框架是否可扩展至世界模型（world models）中的物理交互学习、音频-视觉同步生成等场景？这需要定义模态特定的"运动"概念和相应的损失掩码。

5. **闭环数据策展**：如何利用自生成视频作为查询，自动诊断并追溯不良运动模式（如非物理动态、运动伪影）至训练数据中的特定样本？这需要建立从生成失败到数据溯源的逆向分析管道。

6. **能力保留与专项优化的平衡**：如何在强化目标运动特性的同时最大限度地保留模型的通用生成能力？可能的方向包括正则化微调、混合数据策略，或多任务梯度投影方法。

## 原文 PDF

![[paperPDFs/ICML_2026/Motion_Attribution_for_Video_Generation.pdf]]
