---
title: "Talk2Move: Reinforcement Learning for Text-Instructed Object-Level Geometric Transformation in Scenes"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Talk2Move_Reinforcement_Learning_for_Text_Instructed_Object_Level_Geometric_Transformation_in_Scenes.pdf
project_link: null
code_link: null
aliases:
- Talk2Move
tags:
- CVPR_2026
- topic/benchmarks_datasets_evaluation
- topic/benchmarks_datasets_evaluation/benchmarking
core_operator: 采用组相对策略优化（GRPO）框架，通过注入随机噪声生成多样化的扩散轨迹，并结合空间感知奖励模型直接评估物体位移、旋转和缩放行为，从而在不依赖成对数据的情况下学习精确的几何变换。
primary_logic: 将扩散去噪过程建模为马尔可夫决策过程（MDP），利用GRPO的组内优势估计更新策略，并通过专门的空间奖励（分割、深度估计、方向估计）提供可解释的几何反馈，使模型能够遵循文本指令进行精确的空间操作。
claims:
- GRPO通过从输入图像和轻量文本变体中生成多样滚动路径，探索几何动作，无需昂贵的成对数据
- 空间奖励模型直接评估位移、旋转和缩放行为，实现可解释且连贯的变换
- 离策略步进评估和主动步进采样将训练效率提高2倍，同时保持奖励鲁棒性
- Curated Synthetic Test Benchmark (Translation) 上 Translation Accuracy = 76.67%
---

# Talk2Move: Reinforcement Learning for Text-Instructed Object-Level Geometric Transformation in Scenes

> [!tip] 核心洞察
> 将扩散去噪过程建模为马尔可夫决策过程（MDP），利用GRPO的组内优势估计更新策略，并通过专门的空间奖励（分割、深度估计、方向估计）提供可解释的几何反馈，使模型能够遵循文本指令进行精确的空间操作。

| 字段 | 内容 |
|------|------|
| 中文题名 | Talk2Move：基于强化学习的文本指令物体级几何变换场景编辑 |
| 英文题名 | Talk2Move: Reinforcement Learning for Text-Instructed Object-Level Geometric Transformation in Scenes |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2601.02356) |
| Topic | #topic/benchmarks_datasets_evaluation #topic/benchmarks_datasets_evaluation/benchmarking |
| Method | TALK2MOVE |
| Dataset | Curated Synthetic Test Benchmark, User Study |

> [!tip] 效果简介
> - Curated Synthetic Test Benchmark (Translation) 上，Translation Accuracy 76.67%。
> - Curated Synthetic Test Benchmark (Rotation) 上，Rotation Accuracy 29.55%。
> - Curated Synthetic Test Benchmark (Resize) 上，Resize Accuracy 9.17%。

## 概要

### 1. 问题与瓶颈

现有文本引导的图像编辑方法主要擅长调整图像的外观、风格或纹理，但难以执行**物体级的几何变换**（平移、旋转、缩放）。其根本瓶颈在于：这类精确的空间操作缺乏大规模的成对标注数据，而传统的像素级监督微调（SFT）范式无法有效捕捉物体在场景中的位置、朝向和尺度变化。因此，当前的编辑模型在面对“将杯子向右移动”或“顺时针旋转书本”这类指令时，往往产生不准确或场景不一致的结果。

### 2. 核心方法定位

Talk2Move 首次将**强化学习（RL）**引入文本引导的物体级几何变换任务，核心思路是将扩散模型的去噪过程建模为马尔可夫决策过程（MDP），并利用**组相对策略优化（GRPO）**框架进行策略梯度更新。该方法的关键创新体现在三个层面：

- **探索机制**：在每个扩散步骤注入随机噪声，生成多样化的采样轨迹，从而在不依赖成对数据的前提下探索几何动作空间。
- **空间感知奖励**：设计了一套物体中心的空间奖励模型，利用现成的分割、深度估计和方向估计模型，直接评估物体的位移、旋转和缩放行为，提供可解释的几何反馈。
- **效率优化**：引入离策略步进评估与主动步进采样，识别信息量最大的去噪步骤并跳过冗余步骤，将训练效率提升约 **2 倍**。

与依赖像素级 MSE 损失的监督微调方法（如 **QwenImageEdit**，Wu et al., arXiv 2025；**Flux.1 Kontext**，Black Forest Labs, 2025）不同，Talk2Move 的 RL 范式无需昂贵的成对真值数据，仅需输入图像和文本指令即可学习精确的空间变换。

### 3. 主要结果概览

在作者构建的合成测试基准上，Talk2Move 在物体平移任务上取得了 **76.67%** 的编辑准确率，旋转任务为 **29.55%**，缩放任务为 **9.17%**。用户研究表明，该方法在平移和旋转任务上的胜率分别达到 **57.50%** 和 **68.75%**，显著优于现有 SOTA 图像编辑模型。消融实验进一步证实：空间奖励模型在旋转任务中相比通用 VLM 奖励将误差从 0.3294 降至 **0.2861**，准确率从 11.63% 提升至 29.55%；主动步进采样相比完整采样减少了 **49%** 的迭代时间，同时保持了更高的编辑正确性。

值得注意的是，旋转和缩放任务的绝对准确率仍然较低，表明复杂的几何变换仍是开放挑战。此外，当前方法仅在有限的任务类型和标准化模板上验证，向更复杂的组合变换和开放词汇指令的泛化有待进一步探索。



文本引导的图像编辑近年来取得了显著进展，现有方法能够根据自然语言指令调整图像的风格、颜色和局部纹理。然而，当任务从“外观编辑”转向“空间编辑”时，这些方法暴露出根本性的能力缺口：**它们难以执行物体级的几何变换**——即根据文本指令精确地平移、旋转或缩放场景中的特定物体。

这一瓶颈的根源在于两个相互交织的困难。第一，**监督信号的缺失**。传统的图像编辑模型依赖像素级均方误差（MSE）损失进行监督微调（SFT），这要求成对的“编辑前-编辑后”图像作为训练数据。对于外观编辑，这类配对数据相对容易获取；但对于物体级的空间位移，构建大规模、高质量且多样化的成对标注数据成本极高，甚至不可行。第二，**像素优化的局限性**。即使获得少量配对数据，直接优化像素差异也难以教会模型理解“将物体向左移动”这类抽象的空间语义——模型容易陷入对训练模板的记忆，而非学习可泛化的几何推理能力。

因此，现有主流文本编辑模型（如基于流匹配的 **Flux.1 Kontext**（Black Forest Labs, 2025）、统一多模态框架 **Bagel**（Deng et al., arXiv 2025）以及商业模型 **GPT-image-1**（OpenAI, 2024））在面对物体平移、旋转和缩放指令时，往往无法产生空间上准确且场景连贯的结果。它们要么忽略空间指令仅做外观变化，要么在移动物体的同时破坏背景一致性。

**Talk2Move** 的动机正是填补这一空白。其核心洞见是：将扩散模型的去噪过程形式化为马尔可夫决策过程（MDP），并引入**组相对策略优化（GRPO）** 框架。通过向去噪轨迹注入随机噪声生成多样化的采样路径，模型可以在无需成对监督的条件下探索几何动作空间。同时，专门设计的**空间感知奖励模型**——利用分割、深度估计和方向估计等专家模型——直接评估物体级的位移、旋转和缩放行为，提供可解释的几何反馈信号。这一范式将几何变换的学习从“模仿成对数据”转变为“最大化空间奖励”，从而绕开了对昂贵标注的依赖，使精确的文本驱动空间编辑成为可能。



## 核心方法与创新机理

TALK2MOVE 的核心创新在于将文本引导的物体级几何变换问题从监督微调范式迁移至强化学习范式，并通过三个**changed slots** 实现突破。

### 1. 训练范式：从 SFT 到 GRPO 强化学习

现有文本引导图像编辑方法（如 **QwenImageEdit** (Wu et al., arXiv 2025)、**Flux.1 Kontext** (Black Forest Labs, 2025)）主要依赖监督微调（SFT）和像素级 MSE 损失，这要求大量成对标注数据，而几何变换的精确成对数据获取成本极高。TALK2MOVE 将扩散去噪过程建模为马尔可夫决策过程（MDP），采用**组相对策略优化（GRPO）** 框架进行训练，**无需成对数据**即可学习精确的几何变换。

GRPO 的核心机制是：在每个扩散步骤注入随机噪声，从输入图像和轻量文本变体中生成多样化的采样轨迹（diverse rollouts），然后通过组内优势估计进行策略梯度更新。具体而言，GRPO 的概率比定义为：

$$r_{t}^{i}(\theta)=\frac{p_{\theta}(\mathbf{x}_{t-1}|\mathbf{x}_{t},\mathbf{c})}{p_{\mathrm{old}}(\mathbf{x}_{t-1}|\mathbf{x}_{t},\mathbf{c})}$$

目标函数采用概率比剪切机制：

$$\mathcal{J}_{\mathrm{GRPO}}(\theta) = \mathbb{E}\left[\frac{1}{G T}\sum_{i,t}\min\left(r_{t}^{i}(\theta)\hat{A}_{t}^{i},\operatorname{clip}(r_{t}^{i}(\theta),1-\epsilon,1+\epsilon)\hat{A}_{t}^{i}\right)\right]$$

这种设计使模型能够通过探索不同几何动作并接收空间奖励反馈来学习，而非依赖昂贵的成对真值监督。

### 2. 奖励模型：从通用 VLM 奖励到物体中心空间奖励

现有方法通常使用图像级美学评分、CLIP 对齐或通用 VLM 奖励来引导编辑，但这些奖励缺乏对物体级几何变化的精确感知。TALK2MOVE 设计了**物体中心的空间奖励模型**，利用现成的专家模型直接评估几何变换：

- **平移**：通过文本驱动分割模型分离目标物体，计算其相对位移。
- **旋转**：利用方向估计模型（Orient-Anything）评估物体朝向变化。
- **缩放**：比较归一化尺寸比例以评估缩放行为。

消融实验证实了空间奖励的优越性：在旋转任务中，空间奖励模型的误差为 0.2861，准确率达 29.55%，而基于 VLM 的奖励误差为 0.3294，准确率仅 11.63%（见 **Figure 4c**）。这种可解释的几何反馈是模型能够遵循文本指令进行精确空间操作的关键。

### 3. 训练效率：离策略步进评估与主动步进采样

标准 GRPO 需要对完整去噪轨迹的所有步骤进行采样和优化，计算成本高昂。TALK2MOVE 引入了**离策略步进评估（Off-policy Step Evaluation）** 和**主动步进采样（Active Step Sampling）** 机制：通过评估各去噪步骤的奖励方差，识别信息量最大的步骤作为提前退出点 $K$，并利用 ODE 捷径跳过冗余步骤，将总计算复杂度从 $T$ 步线性缩减至：

$$K(t_{\text{sample}}+t_{\text{optim}})$$

实验表明，该方法相比滑动窗口基线减少 14% 的迭代时间，相比完整采样减少 49% 的时间，同时编辑正确性更高（见 **Table 4**）。每个子任务训练约需 160 GPU 小时（16 H200），效率提升约 2 倍。

### 辅助设计：SFT 冷启动

为增强 GRPO 训练的稳定性，TALK2MOVE 采用 SFT 冷启动策略：使用少量高质量成对数据（平移 800 对，旋转 43 对）进行 LoRA 微调（rank-64，3000 次迭代，学习率 1e-4），为扩散骨干网络嵌入基本空间编辑先验。消融实验表明，在仅 80 对标注数据的极限条件下，SFT 无法获得有意义增益，而基于小数据 SFT 检查点的 RL 仍能达到与全数据设置相当的性能，验证了 RL 范式在低数据场景下的鲁棒性。



TALK2MOVE 提出了一种基于强化学习的文本引导图像编辑框架，专门解决物体级几何变换（平移、旋转、缩放）问题。其核心设计思路是将扩散去噪过程建模为马尔可夫决策过程（MDP），利用组相对策略优化（GRPO）在不依赖成对标注数据的情况下学习精确的空间操作。

### 流水线总览

框架的整体流水线（见 Figure 2）由四个关键模块串联构成，形成从冷启动到高效策略优化的完整闭环：

![[assets/figures/papers/paper_list_l2726_https_arxiv_org_abs_2601_02356/figures/003_Figure_2.jpg]]
*Figure 2: The pipeline of TALK2MOVE. TALK2MOVE streamlines a GRPO-style reinforcement learning pipeline tailored for flow-based image editing. Starting from an initial noise sample, stochastic perturbations are injected at each diffusion step to generate diverse sampling trajectories. Spatially grounded rewards from specialist models, which explicitly evaluate object-level geometric changes, are then used to compute group-relative advantages for policy gradient updates*

1. **SFT 冷启动（Cold Start）**：使用少量高质量成对数据对扩散骨干网络进行低秩适配（LoRA）微调，为模型注入基本的空间编辑先验。这一步骤并非训练的主体，而是为后续 GRPO 训练提供稳定的初始策略，避免强化学习在完全随机初始化下的探索困难。实验表明，即使在仅 80 对标注的极小数据量下，基于该冷启动检查点的 RL 训练仍能达到与全数据设置相当的性能，而纯 SFT 在此数据规模下完全失效。

2. **GRPO 探索轨迹生成器**：在冷启动策略基础上，框架从初始噪声样本出发，在每个扩散步骤注入随机扰动，将确定性 ODE 去噪转化为类随机微分方程（SDE）的采样过程。这种随机化生成一组多样化的去噪轨迹（rollouts），使模型能够在几何变换空间中充分探索不同的位移、旋转和缩放行为。

3. **空间奖励模型（Spatially Grounded Rewards）**：区别于依赖通用 VLM 或图像级美学评分的现有方法，TALK2MOVE 设计了物体中心的空间奖励机制。该模块利用现成的专家模型（文本驱动分割、深度估计、方向估计）将目标物体从场景中显式分离，直接评估物体级的几何变化：对于平移，计算物体中心在图像空间中的相对位移；对于旋转，使用方向估计模型量化角度变化；对于缩放，比较归一化后的尺寸比例。这些奖励信号为 GRPO 提供了可解释的几何反馈。

4. **离策略步进评估与主动步进采样**：为提高训练效率，框架通过评估各去噪步骤的奖励方差，识别信息量最大的“关键步骤”作为提前退出点（exit step $K$），并利用 ODE 捷径跳过冗余步骤。这一设计将总计算复杂度从 $T$ 步线性缩减至约 $K(t_{\text{sample}} + t_{\text{optim}})$，相比完整采样减少 49% 的迭代时间，同时编辑正确性更高。

### 输入输出与优化目标

框架的输入输出映射定义为 $f_{\theta} : (I, T) \to I'$，其中 $I$ 为输入场景图像，$T$ 为描述几何变换的文本指令，$I'$ 为编辑后的输出图像。GRPO 训练仅需要输入样本（参考图像与文本提示），无需成对标注数据。

优化过程中，GRPO 目标函数采用概率比剪切与组内优势估计：

$$\mathcal{J}_{\mathrm{GRPO}}(\theta) = \mathbb{E}\left[\frac{1}{G T}\sum_{i,t}\min\left(r_{t}^{i}(\theta)\hat{A}_{t}^{i},\operatorname{clip}(r_{t}^{i}(\theta),1-\epsilon,1+\epsilon)\hat{A}_{t}^{i}\right)\right]$$

其中 $r_{t}^{i}(\theta) = \frac{p_{\theta}(\mathbf{x}_{t-1}|\mathbf{x}_{t},\mathbf{c})}{p_{\mathrm{old}}(\mathbf{x}_{t-1}|\mathbf{x}_{t},\mathbf{c})}$ 为新旧策略在条件 $\mathbf{c}$ 下的去噪转移概率比，$G$ 为每组随机轨迹数量，$T$ 为去噪步数，$\hat{A}_{t}^{i}$ 为基于空间奖励计算的组内优势估计。

### 模块间的因果机制

整个流水线的因果链路可概括为：冷启动提供基础空间编辑能力 → GRPO 随机探索生成多样变换候选 → 空间奖励模型提供精确的几何反馈信号 → 策略梯度更新使模型逐步学会遵循文本指令进行精确空间操作 → 主动步进采样在关键步骤集中优化，降低计算开销。这一设计使得框架能够在不依赖昂贵成对数据的情况下，实现可解释且连贯的物体级几何变换。

**证据强度说明**：上述流水线描述基于论文 Section 3-5 及 Figure 2 的明确阐述，置信度在 0.9-0.95 之间。各模块的具体实现细节和消融验证将在后续章节展开。

### 补充图表

![[assets/figures/papers/paper_list_l2726_https_arxiv_org_abs_2601_02356/figures/001_Figure_1.jpg]]
*Figure 1: We introduce TALK2MOVE, a text-guided scene editing model for object-level geometric transformation, focusing on object translation, rotation and resizing, achieving superior results over current SOTA image editing models*



### 问题形式化

TALK2MOVE 将文本引导的物体级几何变换建模为一个映射函数：

$$f_{\theta} : (I, T) \to I'$$

其中 $I$ 为输入场景图像，$T$ 为描述几何变换的自然语言指令（如“将杯子向右移动”），$I'$ 为编辑后的输出图像。该映射的核心挑战在于：模型必须在缺乏成对监督信号的条件下，学会精确控制物体的平移、旋转和缩放。

### 核心模块一：SFT 冷启动（Cold Start）

在进入强化学习阶段之前，TALK2MOVE 首先进行轻量级的监督微调冷启动。该模块使用少量高质量成对数据（平移任务约 800 对，旋转任务仅 43 对）对扩散骨干网络进行 LoRA 微调，为模型植入基本的空间编辑先验。这一设计的因果逻辑在于：纯 RL 从零开始探索几何动作空间时，奖励信号过于稀疏，冷启动提供的初始策略能够显著提升 GRPO 训练的稳定性和收敛速度。训练配置为 rank-64 LoRA、3,000 次迭代、学习率 1e-4。

### 核心模块二：GRPO 探索轨迹生成器

TALK2MOVE 的核心训练范式是组相对策略优化（GRPO）。与依赖像素级 MSE 损失的监督微调不同，GRPO 将扩散去噪过程建模为马尔可夫决策过程（MDP），通过在每个扩散步骤注入随机噪声来生成一组多样化的采样轨迹，从而探索不同的几何变换行为。

具体而言，给定输入图像 $I$ 和文本指令 $T$ 构成的条件 $\mathbf{c}$，模型从初始噪声样本出发，在每个去噪步骤 $t$ 注入随机扰动，将原本确定性的 ODE 求解转化为类随机微分方程（SDE）的采样过程。对于每个条件 $\mathbf{c}$，模型生成 $G$ 条随机 rollout 轨迹，形成一组候选编辑结果。

新策略与旧策略在给定条件 $\mathbf{c}$ 下的去噪转移概率比定义为：

$$r_{t}^{i}(\theta) = \frac{p_{\theta}(\mathbf{x}_{t-1}|\mathbf{x}_{t},\mathbf{c})}{p_{\mathrm{old}}(\mathbf{x}_{t-1}|\mathbf{x}_{t},\mathbf{c})}$$

其中 $\mathbf{x}_t$ 为第 $t$ 步的隐变量，$p_{\theta}$ 和 $p_{\mathrm{old}}$ 分别为新策略和旧策略的转移概率。GRPO 通过组内相对优势估计来更新策略，其目标函数为：

$$\mathcal{J}_{\mathrm{GRPO}}(\theta) = \mathbb{E}\left[\frac{1}{G T}\sum_{i,t}\min\left(r_{t}^{i}(\theta)\hat{A}_{t}^{i},\operatorname{clip}(r_{t}^{i}(\theta),1-\epsilon,1+\epsilon)\hat{A}_{t}^{i}\right)\right]$$

其中 $\hat{A}_{t}^{i}$ 为第 $i$ 条轨迹在第 $t$ 步的组内相对优势估计，$\epsilon$ 为概率比剪切范围（本文设为 $2\times10^{-4}$）。该目标函数通过剪切机制防止策略更新过大，保证训练稳定性。

### 核心模块三：空间奖励模型（Spatially Grounded Rewards）

TALK2MOVE 的关键创新在于设计了物体中心的空间奖励模型，直接评估几何变换的精确性，而非依赖通用的图像级美学或 CLIP 对齐奖励。该模块利用现成的专家模型将目标物体从场景中显式分离，并分别评估三类几何变换：

- **平移评估**：利用文本驱动的分割模型定位目标物体，计算编辑前后物体中心的相对位移，与指令中的移动方向和距离进行比对。
- **旋转评估**：使用 Orient-Anything 模型估计物体朝向，计算旋转角度与指令的一致性。
- **缩放评估**：比较编辑前后物体的归一化尺寸比率，评估缩放操作的准确性。

这些空间奖励信号为 GRPO 提供了可解释的几何反馈，使模型能够学习精确的空间操作，而无需昂贵的成对标注数据。

### 核心模块四：离策略步进评估与主动步进采样

为提升训练效率，TALK2MOVE 引入了离策略步进评估和主动步进采样机制。其核心洞察是：并非所有去噪步骤对几何变换的贡献相等，部分步骤的奖励方差显著更高，包含更多信息量。

该模块首先通过轻量级的离策略奖励评估，计算各去噪步骤的奖励方差分布，确定信息量最大的步骤 $K$ 作为“提前退出点”。随后，模型直接从此退出步骤去噪至最终步骤 $T$，通过 ODE 捷径跳过冗余步骤。这一设计将总计算复杂度从 $T$ 步线性缩减至：

$$K(t_{\text{sample}} + t_{\text{optim}})$$

其中 $t_{\text{sample}}$ 和 $t_{\text{optim}}$ 分别为单步采样和优化时间。实验表明，该策略相比滑动窗口基线减少 14% 的迭代时间，相比完整采样减少 49% 的时间，同时在编辑正确性上表现更优。

### 补充图表

![[assets/figures/papers/paper_list_l2726_https_arxiv_org_abs_2601_02356/figures/004_Figure_3.jpg]]
*Figure 3: Three types of step sampling: (a) is the full sampling and optimizing GRPO [21, 40]; subsequent methods [14, 17] as in (b), use a sliding window (yellow) to reduce the optimizing steps per iteration; (c) our work introduces step-wise active sampling that select the informative steps (red) and use shortcuts to bypass the rest of the steps, reducing both the sampling and optimizing time*



## 实验与关键发现

### 实验设置

为评估TALK2MOVE的物体级几何变换能力，作者构建了一个合成测试基准，涵盖平移、旋转和缩放三类任务。评估指标包括编辑准确率（Editing Accuracy）、平均平移距离（Average Translation Distance）和编辑误差（Editing Errors）。此外，还从OpenImages-V6中筛选真实图像进行定量比较，并通过用户研究获取人类偏好胜率（Win Rate）。

训练配置分为两个阶段。冷启动阶段使用Qwen-Image-Edit（Wu et al., arXiv 2025）作为backbone，通过rank-64的LoRA层进行3000次迭代的监督微调，学习率为1e-4。GRPO训练阶段基于FlowGRPO框架，采样噪声水平为1.0，裁剪范围（clip range）为2e-4，在16块H200 GPU上进行，每个子任务约需160 GPU小时。

### 主实验结果

**合成基准测试。** 如Table 1所示，TALK2MOVE在平移任务上取得了76.67%的编辑准确率，显著优于所有开源基线模型。在旋转任务上，准确率达到29.55%，虽然绝对数值不高，但已远超对比方法。缩放任务的准确率为9.17%，反映出该任务本身的极高难度——模型需要在保持物体语义身份的同时精确控制尺寸变化。

**真实图像测试。** 在OpenImages-V6真实图像上的定量结果（Table 2）进一步验证了方法的泛化能力。TALK2MOVE在平移距离和编辑准确率上均保持领先，表明基于RL的训练策略有效弥合了合成数据与真实场景之间的分布差异。

**用户研究。** 人类评估结果显示，TALK2MOVE在平移任务上的胜率为57.50%，在旋转任务上的胜率高达68.75%，以明显优势超越其他方法。值得注意的是，作者指出胜率指标不反映第二偏好或接近平局的倾向，因此可能低估了GPT-based模型等产生有竞争力但视觉显著性稍弱结果的方法。

### 消融研究

**SFT与RL的协同效应。** Table 3的消融实验揭示了几个关键发现。首先，在SFT检查点之上应用RL进一步提高了平均平移距离和最终准确率，验证了RL阶段对SFT先验的有效增强。更重要的是，在极端数据稀缺场景下（仅80对标注数据），纯SFT无法获得有意义的性能提升，而基于小数据SFT检查点启动的RL训练仍能达到与全数据设置相当的性能。这一结果直接证明了GRPO框架对标注数据量的鲁棒性——这正是该方法的核心优势之一。

**奖励模型设计的影响。** Figure 4c展示了空间奖励模型与VLM-based奖励的对比。在旋转任务上，空间奖励模型的误差为0.2861，准确率为29.55%；而VLM-based奖励的误差高达0.3294，准确率仅为11.63%。这一显著差距表明，通用的视觉语言模型难以提供精确的几何变换反馈，而专门设计的空间感知奖励（通过分割、深度估计和方向估计直接评估物体级变化）是实现可解释、连贯几何操作的关键。

**主动步进采样效率。** Table 4报告了不同采样策略的时间开销。与滑动窗口基线相比，主动步进采样将整体迭代时间减少了14%；与完整采样相比，减少了49%。更重要的是，尽管使用的采样步数更少，捷径策略（shortcut strategy）在平移距离和准确率上反而实现了更高的编辑正确性。这验证了“并非所有去噪步进同等重要”的核心假设——通过离策略步进评估识别信息量最大的步进并提前退出，可以在不牺牲甚至提升性能的前提下大幅降低计算成本。

### 背景一致性分析

Table 5报告了背景ID一致性的评估结果，使用图像级CLIP和L1距离作为度量。TALK2MOVE在所有三项变换任务上均取得了最优或次优的背景保持效果。这表明空间奖励模型通过显式分离目标物体与场景，有效避免了编辑过程中的背景漂移问题——这是许多端到端编辑方法常见的失败模式。

### 定性结果与失败模式

Figure 5展示了TALK2MOVE在平移、旋转和缩放任务上的定性编辑结果，每项任务分别包含一张真实图像和一张合成图像的示例。从视觉质量来看，模型能够在保持物体身份和场景光照一致性的前提下，执行符合文本指令的几何变换。

然而，实验也暴露了明显的局限性。旋转准确率（29.55%）和缩放准确率（9.17%）仍然较低，表明这些复杂几何变换任务存在根本性挑战。可能的原因包括：旋转涉及更精细的空间推理，要求模型理解物体的朝向变化；缩放则需要在改变尺寸的同时保持物体的结构完整性，这对扩散模型的像素级生成能力提出了极高要求。此外，当前数据集规模有限（平移仅800张独特图像，旋转和缩放分别仅43对和110对标注数据），数据覆盖不足可能是性能瓶颈之一。

### 关键图表结论

- **Table 1 & Table 2**：TALK2MOVE在合成和真实图像上均取得最优编辑准确率和最大平移距离，验证了GRPO+空间奖励范式的有效性。
- **Table 3**：RL在小数据场景下展现出远超SFT的鲁棒性，证明该方法降低了对成对标注数据的依赖。
- **Figure 4c**：空间奖励模型在旋转任务上的准确率是VLM-based奖励的近3倍，凸显了专用几何反馈的不可替代性。
- **Table 4**：主动步进采样在减少49%时间的同时提升编辑正确性，验证了信息量感知采样的设计合理性。
- **Table 5**：TALK2MOVE在所有变换任务上保持最优背景一致性，证明空间奖励模型有效抑制了背景漂移。

![[assets/figures/papers/paper_list_l2726_https_arxiv_org_abs_2601_02356/figures/005_Table_1.jpg]]
*Table 1: Quantitative comparison of object transformation tasks on our curated synthetic test benchmark in terms of editing accuracy, average translation distance and editing errors. We also report human evaluation results in terms of winning rate. We note that win rate does not capture second-best or near-tie preferences, and thus may underestimate methods that produce competitive but less visually salient results, such as GPT-based models*

![[assets/figures/papers/paper_list_l2726_https_arxiv_org_abs_2601_02356/figures/006_Table_2.jpg]]
*Table 2: Quantitative comparison of object transformation tasks on curated real images from OpenImages-V6 [11] in terms of editing accuracy, average translation distance and editing errors*

![[assets/figures/papers/paper_list_l2726_https_arxiv_org_abs_2601_02356/figures/007_Table_3.jpg]]
*Table 3: Ablation study on SFT and RL under object translation task in terms of translation distance, editing accuracy and image L1 distance*

![[assets/figures/papers/paper_list_l2726_https_arxiv_org_abs_2601_02356/figures/009_Table_4.jpg]]
*Table 4: Ablation on active step sampling under translation task, efficiency measured in seconds(s)*

### 补充图表

![[assets/figures/papers/paper_list_l2726_https_arxiv_org_abs_2601_02356/figures/008_Figure_4.jpg]]
*Figure 4: Reward behavior across tasks: (a) reward variance distribution, (b) GRPO sampling strategies, and (c) reward model ablations*

![[assets/figures/papers/paper_list_l2726_https_arxiv_org_abs_2601_02356/figures/011_Figure_5.jpg]]
*Figure 5: Qualitative results on object translation, rotation and resize over state-of-the-art image editing models. For each task, we provide one real image editing result (source from OpenImagesV6 [11]) and one synthetic image editing result to showcase the generalization ability of TALK2MOVE*



## 定位与知识库关联

### 任务定位与核心差异

TALK2MOVE 聚焦于文本指令驱动的物体级几何变换（平移、旋转、缩放），这与现有文本引导图像编辑方法形成明确的任务边界。当前主流方法——无论是基于扩散模型的 **QwenImageEdit**（Wu et al., arXiv 2025）、流匹配框架 **Flux.1 Kontext**（Black Forest Labs, 2025），还是统一多模态框架 **Bagel**（Deng et al., arXiv 2025）——主要调整图像的外观、风格或语义属性，缺乏对物体空间位置和几何形态的精确操控能力。商业模型 **GPT-image-1**（OpenAI, 2024）虽具备一定的编辑灵活性，但在几何变换精度上同样受限。

这一差异的根源在于训练范式的根本不同：上述基线方法依赖监督微调（SFT）使用像素级 MSE 损失，需要成对的编辑前后图像作为监督信号。然而，物体级几何变换的成对标注数据获取成本极高且难以规模化，导致这些方法无法有效学习空间操作。TALK2MOVE 通过引入组相对策略优化（GRPO）框架，将扩散去噪过程建模为马尔可夫决策过程（MDP），利用空间感知奖励模型直接评估物体位移、旋转和缩放行为，从而在不依赖成对数据的情况下学习精确的几何变换。

### 训练范式谱系：从 SFT 到 RL 的迁移

TALK2MOVE 在训练范式上的核心创新在于将图像编辑从“模仿学习”迁移到“探索-利用”的强化学习框架。具体而言：

- **监督微调（SFT）阶段**：作为冷启动策略，仅使用少量高质量成对数据（平移任务 800 对，旋转任务 43 对）进行 rank-64 LoRA 微调，为扩散 backbone 嵌入基本的空间编辑先验。这一阶段的目标不是达到最终性能，而是为后续 RL 训练提供稳定的策略初始化。

- **GRPO 强化学习阶段**：在 SFT 检查点之上，通过在每个扩散步骤注入随机噪声（噪声水平 1.0）生成多样化的采样轨迹，利用组内优势估计进行策略梯度更新。空间奖励模型由现成的专家模型组成——文本驱动分割模型用于提取目标物体掩码，深度估计模型提供空间定位信息，方向估计模型（Orient-Anything）评估旋转角度——这些模型共同构成可解释的几何反馈信号。

消融研究（Table 3）提供了关键证据：在有限数据条件下（仅 80 对标注），SFT 无法获得有意义的性能提升，而基于小数据 SFT 的 RL 仍能达到与全数据设置相当的性能。这表明 RL 框架对标注数据量的依赖显著低于 SFT 范式。

### 效率优化机制：离策略步进评估与主动步进采样

TALK2MOVE 针对 GRPO 在扩散模型中的计算瓶颈提出了效率优化方案。传统 GRPO 需要对完整的 T 步去噪轨迹进行采样和优化，计算成本高昂。TALK2MOVE 引入两个关键机制：

- **离策略步进评估**：通过评估各去噪步骤的奖励方差，确定信息量最大的步进（即“提前退出点”K），使得模型可以在 K 步后直接通过 ODE 捷径跳至最终步 T，将总计算复杂度从 $T(t_{\text{sample}} + t_{\text{optim}})$ 缩减为 $K(t_{\text{sample}} + t_{\text{optim}})$。

- **主动步进采样**：自适应选择信息量丰富的去噪步骤，跳过冗余步骤。

消融实验（Table 4）表明，该策略相比滑动窗口基线减少了 14% 的迭代时间，相比完整采样减少了 49% 的时间，同时编辑正确性更高。每个子任务仍需约 160 GPU 小时（16 张 H200），表明效率虽有显著提升，但 RL 训练的计算门槛仍然较高。

### 适用边界与局限

TALK2MOVE 的适用性受以下因素约束：

1. **数据规模与任务覆盖**：当前数据集仅包含 3200 个样本（800 张独特图像用于平移），旋转和缩放任务的成对数据更少（43 对和 110 对）。这限制了模型在开放场景中的泛化能力，尤其对于复杂背景或罕见物体类别。

2. **旋转与缩放精度不足**：旋转准确率仅 29.55%，缩放准确率仅 9.17%，表明这些任务仍远未解决。空间奖励模型在旋转任务上虽优于 VLM 奖励（误差 0.2861 vs. 0.3294），但绝对性能仍然较低。

3. **任务范式受限**：方法仅在标准化模板（“将物体向左移动”、“将物体旋转 45 度”等）上进行验证，未探索组合变换（如同时平移和旋转）或开放词汇空间指令。

4. **用户研究偏差**：Table 1 注释指出，胜率（win rate）不反映第二选择或接近平局的偏好，可能低估了产生有竞争力结果的方法（如 GPT 模型）。

### 开放问题

- **跨模态扩展**：该方法是否可以推广到视频中的物体变换，利用时序一致性约束提升几何变换的稳定性？

- **数据规模化**：能否通过更大的合成数据生成管线进一步降低对真实配对数据的依赖，同时提高模型在真实场景中的鲁棒性？

- **多对象交互**：如何支持更复杂的多对象交互式空间编辑，例如相对位置关系的改变（“将 A 放在 B 的左侧”）？

- **框架泛化**：该 RL 范式是否可以推广到其他生成式框架（如自回归模型），用于可验证的可控视觉生成任务？



## 原文 PDF

![[paperPDFs/CVPR_2026/Talk2Move_Reinforcement_Learning_for_Text_Instructed_Object_Level_Geometric_Transformation_in_Scenes.pdf]]
