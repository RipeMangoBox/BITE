---
title: Transition Matching Distillation for Fast Video Generation
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Transition_Matching_Distillation_for_Fast_Video_Generation.pdf
project_link: "https://research.nvidia.com/labs/genair/tmd"
code_link: null
aliases:
- TMDT
- TMDFVG
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/generative_models_diffusion
core_operator: 通过将多步去噪轨迹近似为紧凑的少步概率转移过程，并采用解耦架构（语义主干网络 + 可迭代的轻量流头），在每步转移内进行内流展开与细粒度优化，从而在保持生成质量的同时大幅减少采样步数。
primary_logic: 将预训练教师模型分解为主要负责语义特征提取的主干网络和仅含少数层、可循环调用的流头，利用转移匹配蒸馏与流头展开，使学生模型能够用少量外步和灵活的内步完成从噪声到数据的转移，同时通过分布匹配蒸馏弥合训练与推理的差距，实现速度‑质量的可精细调节。
claims:
- TMD-N2H5 (有效NFE=2.33) 在Wan2.1 1.3B蒸馏中取得总评84.68，超过所有其他蒸馏模型（包括4步rCM的84.43）。
- TMD-N4H5 (有效NFE=1.38) 在Wan2.1 14B蒸馏中取得总评84.24，比一步rCM高出+1.22。
- 用户偏好研究表明，在一步和两步生成设置下，TMD在视觉质量和prompt对齐上均持续优于DMD2-v。
- 蒸馏过程中进行flow head rollout能闭合训练‑推理差距，带来更快的收敛和更高的性能。
---

# Transition Matching Distillation for Fast Video Generation

> [!tip] 核心洞察
> 将预训练教师模型分解为主要负责语义特征提取的主干网络和仅含少数层、可循环调用的流头，利用转移匹配蒸馏与流头展开，使学生模型能够用少量外步和灵活的内步完成从噪声到数据的转移，同时通过分布匹配蒸馏弥合训练与推理的差距，实现速度‑质量的可精细调节。

| 字段 | 内容 |
|------|------|
| 中文题名 | 过渡匹配蒸馏用于快速视频生成 |
| 英文题名 | Transition Matching Distillation for Fast Video Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2601.09881) · [Project](https://research.nvidia.com/labs/genair/tmd) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/generative_models_diffusion |
| Method | Transition Matching Distillation (TMD) |
| Dataset | VBench |

> [!tip] 效果简介
> - VBench (Wan2.1 1.3B 蒸馏) 上，Overall score 84.68 (TMD-N2H5, NFE=2.33) vs 84.43 (rCM, NFE=4) (+0.25)；Overall score 83.80 (TMD-N2H5, NFE=1.17) vs 83.24 (DMD2-v, NFE=1) (+0.56)。
> - VBench (Wan2.1 14B 蒸馏) 上，Overall score 84.24 (TMD-N4H5, NFE=1.38) vs 83.02 (rCM, NFE=1) (+1.22)；Overall score 84.62 (TMD-N4H5, NFE=2.75) vs 84.52 (DMD2-v, NFE=4) (+0.10)。

## 概要

**问题瓶颈**：大型视频扩散模型（如 Wan2.1 系列）的多步采样过程推理代价高、延迟大，难以用于实时交互式应用。现有蒸馏方法（rCM、DMD2、APT、T2V-Turbo-v2、DOLLAR 等）在保留全局运动一致性和细粒度空间细节方面存在困难，且通常将网络视为整体映射，忽略了层级化结构和语义递进。

**核心思路**：本文提出 **过渡匹配蒸馏（Transition Matching Distillation, TMD）**，将多步去噪轨迹近似为紧凑的少步概率转移过程。其关键在于将预训练教师模型**解耦**为两部分——负责提取语义特征的**主主干网络**（大部分层）和仅含少数层、可循环调用的**轻量流头**（最后 H 层）。在每个外步转移内，流头进行 N 步内流展开与细粒度优化，从而在保持生成质量的同时大幅减少采样步数。

**方法定位**：TMD 采用两阶段训练策略。第一阶段 **TM-MF（Transition Matching MeanFlow）** 预训练流头，将其转化为条件流映射；第二阶段基于改进的 **DMD2-v**（引入 Conv3D 判别器、时间步平移等）进行分布匹配蒸馏，并在蒸馏过程中展开流头以闭合训练‑推理差距。推理时按照 M 步外步时间离散化执行转移，每步调用流头 N 次完成内流优化。

**主要结果**：在 Wan2.1 1.3B 蒸馏中，TMD-N2H5（有效 NFE=2.33）取得 VBench 总评 **84.68**，超过所有其他蒸馏模型（包括 4 步 rCM 的 84.43）；在 Wan2.1 14B 蒸馏中，TMD-N4H5（有效 NFE=1.38）取得总评 **84.24**，比一步 rCM 高出 +1.22。用户偏好研究表明，在一步和两步生成设置下，TMD 在视觉质量和 prompt 对齐上均持续优于 DMD2-v。消融实验证实，流头展开、循环迭代、TM-MF 预训练、Conv3D 判别器头和时间步平移等设计均对最终性能有显著贡献。

**局限与展望**：当前两阶段训练流程较复杂，蒸馏依赖教师模型生成的合成数据集（500k 文本‑视频对），尚未在真实视频数据集上验证泛化能力；TMD 未与系统级优化（高效注意力、特征缓存等）结合，实际推理加速潜力可能尚未完全发挥；对其他主流视频扩散模型的蒸馏效果有待验证。未来可探索统一单阶段训练、结合系统优化，以及将该框架推广至其他模态与架构。

### 视频扩散模型的推理瓶颈

基于扩散的视频生成模型近年来取得了显著进展，但其推理过程依赖多步迭代采样——典型设置下需要50步甚至更多次模型前向计算——导致生成一段视频的延迟极高。这种计算代价使得大型视频扩散模型难以部署于实时交互式应用场景，成为制约其实际落地的核心瓶颈。

### 现有蒸馏方法的局限

为缓解上述问题，研究者提出了多种蒸馏策略，试图将教师模型的多步采样轨迹压缩至少量步骤的学生模型。然而，现有方法普遍面临两个关键困难：

1. **全局运动一致性与细粒度空间细节的权衡**：少步生成容易导致时间维度上的闪烁、抖动或运动不连贯，同时空间细节也趋于模糊。现有蒸馏范式通常将整个网络视为单一映射函数进行压缩，忽略了扩散模型内在的层级化结构——浅层主要负责语义特征提取，深层则逐步细化空间与时间细节。这种“整体蒸馏”的思路难以在保持语义一致性的同时保留精细的时空信息。

2. **训练与推理的分布差距**：蒸馏训练时学生模型通常仅执行单步预测，而推理时则需要将前一步的输出作为下一步的输入进行链式调用。这种训练-推理的不一致会导致误差累积，尤其在极低步数（如1-2步）设置下表现尤为明显。

### 本文动机

针对上述问题，本文提出**过渡匹配蒸馏（Transition Matching Distillation, TMD）**，其核心动机源于以下观察：

- 扩散模型的去噪轨迹可以理解为从噪声分布到数据分布的一系列概率转移。与其让学生模型模仿教师的每一步去噪操作，不如直接学习跨越较大噪声区间的紧凑概率转移过程，从而用极少数外步完成生成。

- 教师模型的不同层承担着不同的功能角色：早期层提取高层语义特征，后期层进行细节细化。将这一层级化结构显式建模为解耦架构——**语义主干网络 + 轻量可迭代流头**——有望在保持语义质量的同时，通过流头的循环调用来灵活控制细节细化程度。

- 若能在蒸馏训练阶段就模拟推理时的多步链式调用（即展开流头的内流轨迹并让梯度反向传播通过整个展开序列），则可以有效弥合训练与推理之间的分布差距，提升少步生成的质量上限。

基于上述动机，TMD将多步去噪轨迹蒸馏为紧凑的少步概率转移过程，并通过解耦架构与流头展开机制，实现了速度与生成质量之间可精细调节的权衡。

## 核心方法与创新机理

TMD 的核心创新并非单一算法改进，而是围绕**层级化解耦蒸馏**这一核心理念，对模型架构、生成过程与训练策略三个维度进行了系统性重构，从而在保持生成质量的前提下将视频扩散模型的采样步数从数十步压缩至 1–2 步。

### 1. 从整体蒸馏到解耦架构

传统蒸馏方法（如 DMD2、rCM）将教师模型视为一个整体的“黑箱”映射，直接学习从噪声到数据的端到端变换。TMD 的关键洞察在于：预训练视频扩散模型的不同层承担着不同粒度的功能——浅层和中层主要负责提取高层语义特征，而最后若干层则负责将这些特征转化为精细的时空细节。基于这一观察，TMD 将教师模型**解耦为两个功能模块**（Figure 2a）：

- **主主干网络 (Main Backbone)**：继承教师模型的大部分早期层，负责在每一外步提取语义特征 $\mathbf{m} = m_\theta(\mathbf{x}_{t_i}, t_i)$，为后续的精细生成提供条件信息。
- **流头 (Flow Head)**：仅包含教师模型的最后 $H$ 个 DiT 块，是一个轻量的、可循环调用的模块。流头接收主干特征并通过门控融合机制（时间条件门控）将其与自身输入整合，迭代预测内流更新。

这一解耦架构带来了两个直接优势：（1）流头参数量远小于完整模型，其循环调用（内步 $N > 1$）的计算开销可控；（2）主干网络与流头的功能分离使得蒸馏可以分层进行，主干专注于语义保持，流头专注于细节精化。

### 2. 从多步去噪到少步概率转移

传统扩散模型需要沿连续时间轨迹执行数十步去噪操作。TMD 将这一过程重新定义为**少步概率转移过程**（Figure 2b）：仅用 $M$ 个外步（如 $M=2$）覆盖从噪声到数据的完整变换，每一步跨越较大的噪声水平区间。在每个外步内部，流头执行 $N$ 次内流展开（inner flow rollout），以较小的步长逐步精化样本，从而在极少的外步数下仍能保持生成质量。

这一设计的因果机制在于：外步负责粗粒度的分布迁移，内步负责细粒度的轨迹修正。通过调节 $M$、$N$ 和 $H$，TMD 实现了**速度‑质量的可精细调节**——用户可以在有效 NFE 从约 1.17 到 3.00 的范围内按需选择配置（Table 1）。

### 3. 从直接蒸馏到两阶段训练

TMD 的训练策略同样体现了层级化思想，分为两个阶段：

- **第一阶段：TM-MF 预训练**。传统的流匹配（Flow Matching）直接学习瞬时速度，但 TMD 的流头需要学习的是跨越大时间区间的条件内流映射。为此，TMD 提出了 **MeanFlow 目标**，利用恒等式 $\mathbf{u}(\mathbf{y}_s, s, r) + (s-r)\frac{d}{ds}\mathbf{u}(\mathbf{y}_s, s, r) = \mathbf{v}(\mathbf{y}_s, s)$ 关联平均速度与瞬时速度，使流头能够在不展开的情况下学习到与教师外流对齐的平均速度场。消融实验证实，TM-MF 预训练显著优于直接使用普通流匹配（TM）进行第一阶段训练（Table 6）。

- **第二阶段：DMD2-v 分布匹配蒸馏 + 流头展开**。在预训练流头的基础上，TMD 采用改进的 DMD2-v 进行分布匹配蒸馏。DMD2-v 相比原始 DMD2 引入了三项关键改进：Conv3D 判别器头（捕捉局部时空特征，优于 Conv1D-2D 和基于 Attention 的头，Table 3）、时间步平移（防止模式崩塌，Table 5 和 Figure 9）、以及仅对一步蒸馏有益的 KD 预热（对两步蒸馏会引入不可消除的粗粒度伪影，Table 4 和 Figure 10）。**最关键的是**，在此阶段 TMD 对每个外步展开流头的全部 $N$ 步内流迭代，将展开后的架构作为学生生成器 $\mathbf{g}_\theta$，使 VSD 损失的梯度能够自然回传通过所有内流步骤。这一设计**闭合了训练与推理之间的差距**——训练时流头看到的是自身多步迭代的输出分布，而非单步预测的分布。消融实验表明，展开流头可带来更快的收敛和更高的最终 VBench 得分（Figure 7）。

### 4. 内流目标的设计选择

TMD 的流头采用 **DTM 目标** $\mathbf{y} = \mathbf{x}_1 - \mathbf{x}$（即噪声与数据之差），而非直接预测样本 $\mathbf{x}$ 或速度 $\mathbf{v}$。消融实验证实 DTM 目标优于其他目标类型（Table 10）。这一选择的合理性在于：在整流流框架下，$\mathbf{y}$ 与瞬时速度 $\mathbf{v}$ 直接相关（$\mathbf{v}(\mathbf{x}, t) = \mathbb{E}[\mathbf{x}_1 - \mathbf{x} \mid \mathbf{x}]$），但作为预测目标更为稳定，且与 MeanFlow 预训练中的平均速度参数化 $\mathbf{u}_\theta(\mathbf{y}_s, s, r; \mathbf{m}) := \mathbf{y}_1 - \mathrm{head}_\theta(\mathbf{y}_s, s, r; \mathbf{m})$ 自然衔接。

### 创新点总结

| 创新维度 | 基线做法 | TMD 做法 | 因果作用 |
|---------|---------|---------|---------|
| 模型架构 | 整体 DiT 蒸馏 | 解耦为主干网络 + 可循环流头 | 层级化功能分离，支持灵活的内步精化 |
| 生成过程 | 多步去噪/流匹配 | 少步概率转移 + 内流展开 | 大幅减少外步数，保持轨迹精度 |
| 训练策略 | 单阶段蒸馏 | TM-MF 预训练 + DMD2-v 展开蒸馏 | 闭合训练‑推理差距，加速收敛 |
| 流头目标 | $\mathbf{x}$ 预测或其他 | DTM 目标 $\mathbf{y} = \mathbf{x}_1 - \mathbf{x}$ | 与整流流框架对齐，提升稳定性 |
| 特征融合 | — | 时间条件门控融合 | 稳定地将主干特征注入流头迭代过程 |

TMD 的核心思路是将多步去噪轨迹蒸馏为一个紧凑的少步概率转移过程，并通过解耦架构实现速度与质量的可精细调节。整体框架由三个关键设计构成：**解耦的学生模型架构**、**两阶段蒸馏训练流程**、以及**带内流展开的推理过程**。

### 解耦架构

TMD 学生模型将预训练的教师视频扩散模型（如 Wan2.1）拆分为两个功能互补的组件（Figure 2a）：

- **主主干网络（Main Backbone）**：继承教师模型的前 $L-H$ 层 DiT 块，负责从噪声输入 $\mathbf{x}_{t_i}$ 和时间步 $t_i$ 中提取高层语义特征 $\mathbf{m} = \mathbf{m}_\theta(\mathbf{x}_{t_i}, t_i)$。主干网络在每个外步转移中仅调用一次，提供稳定的语义锚点。
- **轻量流头（Flow Head）**：由教师模型最后 $H$ 个 DiT 块构成，可循环调用。流头以主干特征 $\mathbf{m}$ 为条件，迭代预测内流更新，完成从当前时间 $s$ 到目标时间 $r$ 的精细转移。

主干特征与流头输入之间通过**时间条件门控融合**（gated fusion）机制进行整合，使流头能够自适应地利用不同噪声水平下的语义信息。

### 两阶段训练流程

TMD 的训练分为两个阶段（Algorithm 2），逐步构建学生的少步生成能力：

**第一阶段：TM‑MF 预训练（Transition Matching MeanFlow）**。该阶段的目标是将流头初始化为一个条件内流映射，使其能够在给定主干特征的条件下，预测从任意中间时间 $s$ 到 $r$ 的平均速度。具体而言，流头采用 DTM 目标 $\mathbf{y} = \mathbf{x}_1 - \mathbf{x}$（即噪声与数据之差），并通过 MeanFlow 损失进行训练——该损失利用平均速度 $\mathbf{u}$ 与瞬时速度 $\mathbf{v}$ 之间的恒等关系 $\mathbf{u}(\mathbf{y}_s, s, r) + (s-r)\frac{d}{ds}\mathbf{u}(\mathbf{y}_s, s, r) = \mathbf{v}(\mathbf{y}_s, s)$ 来构造监督信号，避免直接回归瞬时速度时的不稳定性。

**第二阶段：DMD2‑v 分布匹配蒸馏（含流头展开）**。在预训练流头的基础上，将整个学生模型视为一个少步生成器。在每个外步转移 $t_i \to t_{i-1}$ 中，流头被展开 $N$ 次进行内流迭代，展开后的学生输出为：

$$g_\theta(\mathbf{x}_{t_i}, t_i; \mathbf{y}_1) := \mathbf{x}_1 - \mathrm{INNERFLOW}(\mathbf{m}_\theta(\mathbf{x}_{t_i}, t_i))$$

随后对该展开输出施加改进的 DMD2‑v 损失（包含 Conv3D 判别器、时间步平移等），梯度通过所有内流步反向传播，从而闭合训练与推理之间的差距。

### 推理流程

推理时（Algorithm 1），学生模型按照预设的外步时间离散化 $\{t_i\}_{i=0}^M$ 执行 $M$ 步转移。在每一步转移中，主干网络提取一次特征 $\mathbf{m}$，流头循环 $N$ 次完成内流优化，最终从纯噪声 $\mathbf{x}_1$ 逐步转移至数据 $\mathbf{x}_0$。整体计算量以有效 NFE 衡量：

$$\mathrm{Effective\ NFE} := M\left(1 + \frac{(N-1)H}{L}\right)$$

其中 $L$ 为教师模型总层数，$H$ 为流头层数。通过调节外步数 $M$、内步数 $N$ 和流头深度 $H$，可在推理速度与生成质量之间实现精细的权衡控制。

### 输入输出流

- **输入**：标准高斯噪声 $\mathbf{x}_1 \sim \mathcal{N}(\mathbf{0}, \mathbf{I})$ 和文本提示（通过文本编码器注入主干网络）。
- **输出**：生成的视频数据 $\hat{\mathbf{x}}_0$，经过 $M$ 步外转移和每步 $N$ 次内流迭代得到。
- **中间表示**：主干网络输出语义特征 $\mathbf{m}$，流头在各内步中维护并更新 DTM 变量 $\mathbf{y}_s$，最终通过 $\hat{\mathbf{x}} = \mathbf{x}_1 - \hat{\mathbf{y}}_0$ 恢复视频样本。

### 3.1 解耦架构与转移匹配框架

TMD 的核心洞察在于将预训练的教师视频扩散模型分解为两个功能互补的组件，并利用转移匹配蒸馏将多步去噪轨迹压缩为紧凑的少步概率转移过程。

**主主干网络 (Main Backbone)** 由教师模型的前 $L-H$ 层构成，负责提取高层语义特征。给定带噪输入 $\mathbf{x}_{t_i}$ 和时间步 $t_i$，主干网络输出特征：

$$\mathbf{m}_{\theta}(\mathbf{x}_{t_i}, t_i)$$

其中 $t_i$ 为外步时间离散化点。主干网络保留了教师模型的大部分容量，确保语义信息的完整性。

**流头 (Flow Head)** 由教师模型的最后 $H$ 个 DiT 块组成，是一个轻量级可循环调用的模块。流头基于主干特征 $\mathbf{m}$ 迭代预测内流更新，其核心是条件内流映射：

$$\mathbf{f}_{\theta}(\mathbf{y}_s, s, r; \mathbf{m}) := \mathbf{y}_s + (s - r) \mathbf{u}_{\theta}(\mathbf{y}_s, s, r; \mathbf{m}) \tag{13}$$

其中 $\mathbf{y}_s$ 为当前内流状态，$s$ 和 $r$ 分别为内流的起始和终止时间步，$\mathbf{u}_{\theta}$ 为参数化的平均速度场。该映射将状态从时间 $s$ 推进到时间 $r$。

**平均速度参数化** 采用 DTM (Difference of Transition Matching) 形式，使流头输出与教师的外流预测对齐：

$$\mathbf{u}_{\theta}(\mathbf{y}_s, s, r; \mathbf{m}) := \mathbf{y}_1 - \mathrm{head}_{\theta}(\mathbf{y}_s, s, r; \mathbf{m}) \tag{14}$$

其中 $\mathbf{y}_1$ 为目标噪声（标准高斯），$\mathrm{head}_{\theta}$ 为流头网络输出。这一参数化使得当 $r \to s$ 时，$\mathbf{u}_{\theta}$ 趋近于教师的瞬时速度，有利于预训练阶段的收敛。

**特征融合** 采用时间条件门控机制 (gated fusion)，将主干特征 $\mathbf{m}_{t_i}$ 与带噪流头目标 $\mathbf{y}_{s_j}$ 进行动态融合，作为流头的输入。消融实验表明，门控融合相比通道拼接在收敛稳定性上更优 (Table 9, Figure 13)。

### 3.2 两阶段训练流程

TMD 的训练分为两个阶段，对应 Algorithm 2 中的两条分支。

**第一阶段：TM-MF 预训练 (Transition Matching with MeanFlow)**

该阶段的目标是将流头预训练为条件内流映射。核心训练目标基于 MeanFlow 恒等式，该恒等式将平均速度 $\mathbf{u}$ 与瞬时速度 $\mathbf{v}$ 关联：

$$\mathbf{u}(\mathbf{y}_s, s, r) + (s - r) \frac{d}{ds} \mathbf{u}(\mathbf{y}_s, s, r) = \mathbf{v}(\mathbf{y}_s, s) \tag{8}$$

利用教师模型提供的瞬时速度 $\mathbf{v}$ 作为监督信号，通过该恒等式构造 MeanFlow 损失，使流头学会在给定主干特征的条件下执行内流转移。消融实验证实，TM-MF 预训练优于直接使用普通流匹配 (TM) 进行第一阶段预训练 (Table 6)。

由于直接计算全导数 $\frac{d}{ds} \mathbf{u}_{\theta}$ 可能与 flash attention 等高效实现不兼容，TMD 采用中心差分近似：

$$\frac{d}{ds} \mathbf{u}_{\theta}(\mathbf{y}_s, s, r) \approx \frac{\mathbf{u}_{\theta}(\mathbf{y}_{s+\delta}, s+\delta, r) - \mathbf{u}_{\theta}(\mathbf{y}_{s-\delta}, s-\delta, r)}{2\delta}$$

**第二阶段：DMD2-v 分布匹配蒸馏**

第二阶段在每步外转移中展开流头（flow head rollout），将解耦架构视为样本生成器，应用改进的 DMD2-v 损失进行分布匹配蒸馏。展开后的学生生成器输出为：

$$g_{\theta}(\mathbf{x}_{t_i}, t_i; \mathbf{y}_1) := \mathbf{x}_1 - \mathrm{INNERFLOW}(\mathbf{m}_{\theta}(\mathbf{x}_{t_i}, t_i)) \tag{15}$$

其中 $\mathrm{INNERFLOW}$ 表示 $N$ 步内流迭代的完整展开过程。将 VSD 损失应用于展开后的输出，梯度自然通过所有内流步反向传播，从而闭合训练与推理之间的差距。消融实验表明，流头展开带来更快的收敛和更高的最终 VBench 得分 (Figure 7)。

![[assets/figures/papers/paper_list_l946_https_arxiv_org_abs_2601_09881/figures/012_Figure_7.jpg]]
*Figure 7: | Convergence and rollout ablation. We compare the overall VBench score over iterations for the second-stage TMD training with and without flow head rollout. While TMD generally converges within a only few thousand iterations, we observe faster convergence and improved performance when using rollouts*

DMD2-v 相对于原始 DMD2 引入了三项关键改进：
- **Conv3D 判别器**：利用局部时空特征提升 GAN 损失的有效性 (Table 3)；
- **KD 预热**：仅对一步蒸馏有益，两步蒸馏会引入不可消除的粗粒度伪影 (Table 4, Figure 10)；
- **时间步平移**：对 $t_{\text{dmd}}$ 和 $t_{\text{student}}$ 施加非线性平移函数 $t = \frac{\gamma t'}{(\gamma - 1) t' + 1}$ ($\gamma \geq 1$)，有效提升性能并防止模式崩塌 (Table 5, Figure 9)。

### 3.3 推理过程与效率度量

推理时，TMD 按照外步时间离散化执行 $M$ 步转移，每步调用流头 $N$ 次完成内流优化 (Algorithm 1)。为公平比较计算量，定义有效 NFE：

$$\mathrm{Effective\ NFE} := M \big( 1 + \frac{(N - 1) H}{L} \big) \tag{16}$$

其中 $L$ 为教师模型总层数，$H$ 为流头层数。该公式将流头的循环调用折算为等效的全模型前向传播次数，确保 TMD 与基线在类似推理成本下进行公平对比。

## 实验与关键发现

### 核心瓶颈与蒸馏目标

大型视频扩散模型（如 Wan2.1）的多步采样过程推理代价高、延迟大，难以用于实时交互式应用。现有蒸馏方法（如 rCM、DMD2、APT 等）在保留全局运动一致性和细粒度空间细节方面存在困难，且通常将网络视为整体映射，忽略了层级化结构和语义递进。TMD 的核心思路是将多步去噪轨迹近似为紧凑的少步概率转移过程，并采用解耦架构（语义主干网络 + 可迭代的轻量流头），在每步转移内进行内流展开与细粒度优化，从而在保持生成质量的同时大幅减少采样步数。

### 主实验结果

#### Wan2.1 1.3B 蒸馏结果

Table 1 展示了在 Wan2.1 1.3B 教师模型上的蒸馏对比。TMD-N2H5（有效 NFE=2.33）取得 VBench 总评 **84.68**，超过所有其他蒸馏模型，包括 4 步 rCM 的 84.43。在更低计算量设置下，TMD-N2H5（有效 NFE=1.17）取得 83.80，比一步 DMD2-v 高出 +0.56。TMD-N4H5（有效 NFE=3.00）进一步达到 84.67，展现了内步数 N 对质量的提升作用。

#### Wan2.1 14B 蒸馏结果

Table 2 展示了在 Wan2.1 14B 教师模型上的蒸馏对比。TMD-N4H5（有效 NFE=1.38）取得总评 **84.24**，比一步 rCM 高出 +1.22，显著优于所有其他一步蒸馏方法。在两步设置下，TMD-N4H5（有效 NFE=2.75）取得 84.62，超过 DMD2-v（NFE=4）的 84.52，以更低的计算量实现了更优的质量。

#### 用户偏好研究

Figure 5 展示了双盲 2AFC 用户偏好研究结果。在一步和两步生成设置下，TMD-N4H5 在视觉质量和 prompt 对齐上均持续优于 DMD2-v。用户偏好百分比显著高于 50% 的随机基线，验证了 TMD 在主观感知质量上的优势。

![[assets/figures/papers/paper_list_l946_https_arxiv_org_abs_2601_09881/figures/010_Figure_5.jpg]]
*Figure 5: | User preference study results. Comparison of TMD-N4H5 (ours) against DMD2-v under one-step (?? = 1) and two-step (?? = 2) distillation regimes. Values indicate the percentage of times users preferred our method over the baseline DMD2-v and the dashed line at 50% represents parity*

### 关键消融分析

#### 流头展开（Flow Head Rollout）

Figure 7 展示了蒸馏阶段是否展开流头对收敛和最终性能的影响。展开流头可闭合训练‑推理差距，带来更快的收敛和更高的最终 VBench 得分。不展开流头时，训练过程中的架构与推理时不一致，导致性能下降。这一消融验证了“在蒸馏过程中将流头展开为样本生成器”策略的必要性。

#### 流头循环迭代（Inner Steps N）

Figure 14 展示了流头循环迭代对生成质量的影响。N1H5（无循环）生成的视频存在明显伪影和模糊，而 N4H5（4 步内流迭代）质量显著更高。这表明循环迭代（N>1）对于生成高质量视频至关重要，流头需要多步内流优化才能有效捕获细节。

![[assets/figures/papers/paper_list_l946_https_arxiv_org_abs_2601_09881/figures/025_Figure_14.jpg]]
*Figure 14: | Impact of flow head recurrence. We show the impact of recurrence in the flow head by setting the number of flow head steps to 1 only at inference (i.e., N1H5) when distilling Wan2.1 1.3B with ?? = 2 and the N4H5 setting for flow head (i.e., 4 denoising steps and 5 DiT blocks in flow head). We observe that the videos generated without recurrence (marked by N1H5) are of much lower quality (e.g., more artifacts and blurriness) than ones with recurrence (marked by N4H5), implying the importance of the fine-grained iterative refinement on our method*

#### DMD2-v 关键改进因素

Table 3、Table 4、Table 5 分别消融了 DMD2-v 中的三项关键改进：

![[assets/figures/papers/paper_list_l946_https_arxiv_org_abs_2601_09881/figures/008_Table_4.jpg]]
*Table 4: | Impact of the KD warm-up, where we distill Wan2.1 1.3B into a one-step or two-step student, respectively. For KD warm-up, we use teacher model to generate 10k noise-data pairs*

![[assets/figures/papers/paper_list_l946_https_arxiv_org_abs_2601_09881/figures/009_Table_5.jpg]]
*Table 5: | Impact of the timestep shifting for*

- **Conv3D 判别器头**（Table 3）：使用 Conv3D 判别器头优于 Conv1D-2D 和基于 Attention 的头，验证了局部时空特征对 GAN loss 的重要性。
- **KD 预热**（Table 4）：KD 预热仅对一步蒸馏有益；对两步蒸馏会引入粗粒度伪影，且这些伪影无法被后续 DMD2 训练消除（见 Figure 10）。
- **时间步平移**（Table 5）：对 t_dmd 和 t_student 施加时间步平移可有效提升性能并防止模式崩塌。Figure 9 展示了无时间步平移时出现的典型模式崩塌现象——生成视频中主要角色始终出现在画面左侧。

![[assets/figures/papers/paper_list_l946_https_arxiv_org_abs_2601_09881/figures/017_Figure_9.jpg]]
*Figure 9: | Mode collapse without time-shifting. We show videos generated by the one-step student distilled from DMD2 in the setting*

#### TM-MF 预训练

Table 6 对比了第一阶段预训练方法。TM-MF（基于 MeanFlow 目标）比直接使用普通流匹配（TM）能取得更好的最终蒸馏性能，验证了 MeanFlow 损失在预训练流头中的有效性。

#### 融合策略与目标类型

Table 9 和 Figure 13 比较了门控融合与通道拼接融合。两种融合方式均可取得强性能，但门控融合在收敛稳定性上更优。Table 10 验证了采用 DTM 目标 y = x₁ - x 优于直接预测 x 作为内流目标。

### 性能‑效率权衡

Figure 6 展示了 TMD 在不同内步数 N 和流头层数 H 下的性能‑效率权衡曲线。TMD 在相同有效 NFE 下持续优于 2 步和 3 步 DMD2-v，且通过调节 N 和 H 可实现速度‑质量的可精细调节。Figure 11 将这一分析扩展到 M=1 的设置，进一步验证了 TMD 在不同外步数下的鲁棒性。

### 失败模式与局限

1. **KD 预热在两步蒸馏中的负面影响**：KD 预热引入的粗粒度伪影在后续 DMD2 训练中无法消除（Figure 10），表明两步蒸馏应直接从分布匹配开始训练。
2. **无时间步平移导致模式崩塌**：Figure 9 展示了典型失败案例，生成多样性严重受限。
3. **两阶段训练流程复杂**：当前需要先进行 TM-MF 预训练再进行 DMD2-v 蒸馏，流程较为繁琐。
4. **蒸馏数据依赖**：当前蒸馏依赖教师模型生成的 500k 合成文本‑视频对，尚未验证在真实视频数据集上的泛化能力。
5. **未结合系统级优化**：TMD 未与高效注意力、特征缓存等系统级优化结合，实际推理加速潜力可能尚未完全发挥。

### 公平性说明

所有实验使用有效 NFE（Effective NFE = M(1 + (N-1)H/L)）作为统一的计算量衡量指标，确保 TMD 与基线在类似推理成本下公平比较。基线 DMD2-v 是原始 DMD2 针对视频生成的改进版本（包含 Conv3D 判别器、时间步平移等），确保对比为各自最优配置。用户偏好研究采用双盲 2AFC 设计，从 VBench 中随机采样 60 个具有挑战性的提示，对视觉质量和提示对齐进行独立评分。

## 定位与知识库关联

### 蒸馏范式定位：从轨迹回归到转移匹配

TMD 处于视频扩散模型加速蒸馏的方法谱系中，其核心区别于现有工作的关键点在于**将多步去噪轨迹重新表述为紧凑的概率转移过程**，而非直接回归教师轨迹或进行单步分布匹配。

在现有蒸馏方法中，**rCM**和 **APT**等一致性模型变体通过强制相邻时间步输出一致来压缩轨迹，但通常将整个网络视为黑箱映射，忽略了扩散模型内部层级化的语义递进结构。**DMD2**及其变体采用分布匹配范式，通过 GAN 判别器直接拉近学生生成分布与教师分布，但在视频生成中面临模式崩塌和细粒度时空细节丢失的问题。**T2V-Turbo-v2**和 **DOLLAR**等方法针对视频生成进行了适配，但同样受限于整体映射的蒸馏策略。

TMD 的关键创新在于**解耦蒸馏**：将教师模型分解为语义主干网络和轻量流头两个功能模块。这一设计与现有工作形成鲜明对比——传统蒸馏方法将整个 DiT 网络作为单一映射函数进行压缩，而 TMD 识别出教师模型的不同层承担不同角色：早期层负责提取高层语义特征，最后若干层（H 层）负责将语义特征转化为精细的去噪/流更新。通过将后者独立为可循环调用的流头模块，TMD 实现了**层级化蒸馏**，使外步转移（M 步）处理大尺度语义演进，内流展开（N 步）处理细粒度细节优化。

### 与 DMD2-v 的关系：改进基线而非替代

值得注意的是，TMD 的第二阶段训练直接建立在**本文改进的 DMD2-v** 之上。DMD2-v 本身是原始 DMD2针对视频生成的重要改进版本，包含三个关键增强：

1. **Conv3D 判别器头**：替代原始 DMD2 的 Conv1D-2D 或 Attention 判别器，验证了局部时空特征对视频 GAN loss 的重要性（Table 3）。
2. **时间步平移**：对 $t_\text{dmd}$ 和 $t_\text{student}$ 施加非线性平移函数 $t = \frac{\gamma t'}{(\gamma - 1) t' + 1}$，有效防止模式崩塌并提升性能（Table 5, Figure 9）。
3. **KD 预热**：仅对一步蒸馏有益，对两步蒸馏会引入不可消除的粗粒度伪影（Table 4, Figure 10）。

TMD 在 DMD2-v 基础上的核心增量在于**解耦架构 + 流头展开 + TM-MF 预训练**的三阶段设计。消融实验证实，单独使用 DMD2-v（即不展开流头、不进行 TM-MF 预训练）的性能显著低于完整 TMD：在 Wan2.1 1.3B 蒸馏中，TMD-N2H5（有效 NFE=2.33）总评 84.68 超过 DMD2-v（NFE=1）的 83.24（+0.56）；在 Wan2.1 14B 蒸馏中，TMD-N4H5（有效 NFE=1.38）总评 84.24 超过 rCM（NFE=1）的 83.02（+1.22）。这表明 TMD 的贡献并非来自更强的判别器或训练技巧，而是来自架构解耦和内流展开带来的训练-推理一致性。

### 适用边界与约束条件

TMD 的设计和验证存在以下适用边界：

**教师模型架构依赖**：当前验证仅针对 **Wan2.1**（1.3B / 14B）系列模型，该模型采用标准 DiT 架构。TMD 的解耦策略假设教师模型的层级结构具有明确的语义递进性——早期层提取高层语义，后期层进行细节优化。对于其他主流视频扩散模型（如 HunyuanVideo 的 MMDiT 架构、Cosmos 的 U-Net 变体），这一假设的适用性尚未验证。特别是 MMDiT 架构中文本和视频 token 的交叉注意力机制可能改变层级功能的分布，流头划分策略需要重新设计。

**训练数据依赖**：蒸馏过程依赖教师模型生成的 500k 文本-视频合成数据对，而非真实视频数据集。这意味着 TMD 的蒸馏质量上限受限于教师模型的生成能力，且无法保证在真实视频分布上的泛化性能。对于教师模型本身存在系统性缺陷（如特定运动模式的崩塌）的场景，TMD 可能放大而非修正这些缺陷。

**计算量公平比较**：TMD 使用有效 NFE（Effective NFE）作为统一计算量指标，公式为 $M(1 + \frac{(N-1)H}{L})$。这一指标合理地将流头的轻量计算（H 层 vs 教师总 L 层）折算为等效全模型评估次数。然而，该指标假设流头层与主干层的计算成本呈线性比例，忽略了注意力操作中序列长度对计算量的非线性影响。在长视频生成场景下，有效 NFE 可能低估实际推理成本。

**两阶段训练复杂性**：TMD 的两阶段训练流程（TM-MF 预训练 + DMD2-v 分布匹配蒸馏）增加了工程复杂度。第一阶段需要额外的 MeanFlow 损失实现和中心差分 JVP 近似（用于避免与 flash attention 的不兼容），第二阶段需要在每步转移中展开流头并反向传播梯度通过所有内步。这种复杂性可能阻碍 TMD 在其他模型上的快速复现和部署。

### 局限与开放问题

**训练流程统一化**：当前两阶段设计是 TMD 最明显的工程局限。TM-MF 预训练将流头初始化为条件流映射，为后续分布匹配蒸馏提供良好起点；DMD2-v 阶段则通过 GAN loss 弥合分布差距。理论上，MeanFlow 目标和 VSD loss 可以联合优化，但消融实验（Table 6）表明直接使用普通流匹配（TM）替代 MeanFlow 会降低最终性能，说明两阶段设计在当前形式下是必要的。如何设计统一的单阶段训练目标，同时保留 MeanFlow 的轨迹对齐能力和 DMD2-v 的分布匹配能力，是一个开放问题。

**系统级优化潜力未释放**：TMD 当前仅从算法层面减少采样步数，未结合系统级优化技术。将 TMD 与高效注意力机制（如 flash attention 3、稀疏注意力）、特征缓存（如跨步特征复用）、或专用推理引擎（如 TensorRT）结合，可能进一步压缩实际推理延迟。特别是流头的循环调用特性天然适合特征缓存——同一外步内的多次内流迭代共享主干特征 $m_\theta(x_{t_i}, t_i)$，当前实现每次内步都重新计算融合特征，存在明显冗余。

**跨模态与跨架构泛化**：TMD 的解耦蒸馏框架在概念上不限于视频生成。对于图像生成（如 Stable Diffusion 3）、3D 生成（如 Gaussian Splatting 的扩散先验）、乃至音频生成，层级化解耦策略可能同样有效。但具体到不同架构，流头划分的层数 H、内步数 N、以及门控融合的设计都需要重新调优。特别是对于 U-Net 架构，其跳跃连接结构使得"早期层"和"后期层"的语义分工不如 DiT 清晰，解耦策略需要适配。

**内流速度的精确建模**：当前 TM-MF 预训练使用平均速度参数化 $u_\theta(y_s, s, r; m) := y_1 - \text{head}_\theta(y_s, s, r; m)$，其理论依据是 MeanFlow 恒等式将平均速度与瞬时速度关联。然而，该参数化假设教师速度场在 $[r, s]$ 区间内近似线性，对于 Wan2.1 轨迹中观测到的近 $t=1$ 处的大曲率区域（Figure 12），这一假设可能引入近似误差。利用教师速度的高阶导数信息（如通过更高阶的 JVP 或连续时间 Neural ODE 求解器）推导更精确的内流速度，可能进一步提升转移匹配预训练的质量。

**长视频生成的扩展性**：当前实验验证集中在 5 秒 480p 视频生成。对于更长时长（如 30 秒以上）或更高分辨率（如 1080p）的视频生成，外步数 M 和内步数 N 的最优配置可能发生变化。直觉上，长视频涉及更复杂的时序依赖，可能需要更多的外步来捕捉大尺度运动演进；而高分辨率视频的细粒度细节更丰富，可能需要更多的内步或更深的流头。TMD 的 M/N/H 参数空间在不同视频规格下的扩展规律尚未被系统研究。

## 原文 PDF

![[paperPDFs/CVPR_2026/Transition_Matching_Distillation_for_Fast_Video_Generation.pdf]]
