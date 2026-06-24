---
title: "PaCo-RL: Advancing Reinforcement Learning for Consistent Image Generation with Pairwise Reward Modeling"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/PaCo_RL_Advancing_Reinforcement_Learning_for_Consistent_Image_Generation_with_Pairwise_Reward_Modeling.pdf
project_link: null
code_link: null
aliases:
- PRPRPG
- PaCo-RL
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 引入成对一致性奖励模型（PaCo-Reward）将一致性评估转化为生成式二分类任务，以及设计分辨率解耦训练与对数驯化多奖励聚合的强化学习策略（PaCo-GRPO），直接提升奖励信号的感知对齐度和训练效率/稳定性。
primary_logic: 将一致性评估重构为 VLM 的下一个 token 预测（Yes/No 概率），充分利用自回归特性，避免额外回归头导致的错位；同时，在 RL 阶段采用低分辨率采样并辅以基于奖励波动的对数压缩，可在不损害推理质量的前提下大幅降低计算成本并防止单一奖励主导优化。
claims:
- PaCo-Reward-7B 在 ConsistencyRank 上相对基座 Qwen2.5-VL-7B 准确率提升 10.5%（0.344→0.449），Spearman ρ 增加 0.150。
- 在 EditReward-Bench 上，PaCo-Reward-7B 的一致性准确率（0.709）显著超越所有开源基线，接近 GPT-5（0.669）。
- FLUX.1-dev + PaCo-Reward-7B 在 T2IS-Bench 的视觉一致性身份指标达到 0.508 / 0.837，远超无 RL 基线的 0.249 / 0.636。
- Qwen-Image-Edit + PaCo-Reward-7B 在 GEdit-Bench 的 EN-I 总体得分从 7.307 提升至 7.451，且各项子指标全面提升。
---

# PaCo-RL: Advancing Reinforcement Learning for Consistent Image Generation with Pairwise Reward Modeling

> [!tip] 核心洞察
> 将一致性评估重构为 VLM 的下一个 token 预测（Yes/No 概率），充分利用自回归特性，避免额外回归头导致的错位；同时，在 RL 阶段采用低分辨率采样并辅以基于奖励波动的对数压缩，可在不损害推理质量的前提下大幅降低计算成本并防止单一奖励主导优化。

| 字段 | 内容 |
|------|------|
| 中文题名 | PaCo-RL：利用成对奖励建模推进一致图像生成的强化学习 |
| 英文题名 | PaCo-RL: Advancing Reinforcement Learning for Consistent Image Generation with Pairwise Reward Modeling |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.04784) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | PaCo-RL (PaCo-Reward + PaCo-GRPO) |
| Dataset | ConsistencyRank, EditReward-Bench, T2IS-Bench, GEdit-Bench |

> [!tip] 效果简介
> - ConsistencyRank 上，Accuracy PaCo-Reward-7B: 0.449 vs Qwen2.5-VL-7B: 0.344 (+0.105)。
> - EditReward-Bench 上，Consistency Accuracy PaCo-Reward-7B: 0.709 vs EditScore-72B: 0.586 (+0.123)。
> - T2IS-Bench (Text-to-ImageSet) 上，Visual Consistency: Identity (Qwen2.5-VL-7B eval) FLUX.1-dev + PaCo-Reward-7B: 0.508 vs FLUX.1-dev (no RL): 0.249 (+0.259)。

## 概述

一致图像生成面临一个核心瓶颈：现有奖励模型主要关注美学质量或文本-图像对齐，缺乏专门捕捉**视觉一致性**的能力；同时，在多图像、高分辨率场景下引入强化学习（RL）优化时，计算开销极大，且多奖励信号容易相互支配，导致训练不稳定甚至崩溃。

针对上述问题，本文提出 **PaCo-RL**，其核心思路包含两个关键调控点：

1. **成对一致性奖励模型（PaCo-Reward）**：将一致性评估重构为视觉语言模型（VLM）的下一个 token 预测任务——通过预测 “Yes”/“No” 的概率来度量两幅图像之间的一致性，从而充分利用自回归特性的感知对齐能力，避免额外回归头导致的错位。
2. **强化学习策略（PaCo-GRPO）**：设计分辨率解耦训练（低分辨率采样、全分辨率推理）与基于奖励波动的对数驯化多奖励聚合，在保证推理质量的前提下大幅降低计算成本，并防止单一奖励主导优化过程。

实验结果表明，PaCo-Reward-7B 在 ConsistencyRank 上相对基座 Qwen2.5-VL-7B 准确率提升 10.5%（0.344→0.449），在 EditReward-Bench 上的一致性准确率（0.709）显著超越所有开源基线并接近闭源模型 GPT-5（0.669）。将 PaCo-Reward 集成到 PaCo-GRPO 后，FLUX.1-dev 在 T2IS-Bench 的视觉一致性身份指标从 0.249 跃升至 0.508，Qwen-Image-Edit 在 GEdit-Bench 的总体得分从 7.307 提升至 7.451。消融实验进一步验证，分辨率解耦训练在仅用一半时间（6 小时 vs. 12 小时）内取得了更优的性能，而对数驯化聚合成功将奖励比稳定在 1.8 以下，避免了标准加权聚合导致的训练退化。

## 背景与动机

### 一致图像生成的任务定义

一致图像生成（Consistent Image Generation）要求模型在多个图像之间维持视觉身份、风格和语义上下文的连贯性。论文聚焦两个代表性任务（Figure 1）：

- **图像编辑**：在修改特定属性的同时保留整体外观，例如改变人物表情但不改变其身份或背景。
- **文本到图像集生成**：根据统一描述生成多张连贯图像，这些图像需在身份、风格和场景语境上保持一致。

这两类任务的核心挑战在于，模型不仅要满足单张图像的提示对齐和美学质量，还必须确保跨图像的视觉一致性——这是一个被现有生成流程系统性忽视的维度。

### 现有方法的缺口

当前一致图像生成面临两个关键瓶颈：

**瓶颈一：缺乏专门捕捉视觉一致性的奖励模型。** 现有的图像奖励模型主要关注美学质量（如 LAION Aesthetics Predictor）或文本-图像对齐（如 CLIP Score、PickScore），几乎没有模型将跨图像视觉一致性作为独立评估维度。通用的视觉语言模型（VLM）如 **Qwen2.5-VL-7B**（Qwen team, 2025）和 **InternVL3.5-8B**（OpenGVLab, 2024）虽具备一定的多图像理解能力，但未针对一致性比较进行专门优化，其原始输出与人类偏好存在显著偏差（ConsistencyRank 准确率仅 0.344）。此外，传统奖励模型通常依赖额外的标量回归头输出奖励分数，这一设计与 VLM 的自回归预测过程存在结构错位。

**瓶颈二：强化学习优化在多图像/高分辨率场景下计算开销极大，且多奖励信号容易相互支配。** 将一致性奖励引入 RL 训练时，全分辨率（如 1024×1024）下的多次采样和奖励计算需要大量 GPU 资源；同时，当同时优化美学、提示对齐和视觉一致性等多个奖励信号时，不同奖励的波动幅度差异会导致某一奖励主导优化方向，引发训练不稳定甚至模式崩溃——例如模型为追求视觉一致性而生成近乎重复的低质量图像。

### 本文动机与核心思路

针对上述瓶颈，PaCo-RL 提出两个核心组件：

- **PaCo-Reward**：将一致性评估重构为 VLM 的生成式二分类任务——直接预测 “Yes”/“No” token 的概率作为一致性得分，利用自回归特性避免额外回归头导致的表示错位。该设计使奖励信号与 VLM 的 next-token prediction 过程天然对齐。
- **PaCo-GRPO**：在 RL 阶段引入分辨率解耦训练（低分辨率采样、全分辨率推理）和对数驯化多奖励聚合，在降低计算成本的同时防止单一奖励主导优化。

这种“感知对齐的奖励建模 + 训练高效的 RL 策略”的组合，构成了解决一致图像生成问题的完整闭环。

## 核心创新

PaCo-RL 的核心创新围绕两个“变更槽”（changed slots）展开，分别作用于奖励建模范式和强化学习优化策略，形成“感知对齐的奖励信号 + 高效稳定的策略优化”闭环。

### 1. 从标量回归到生成式二分类的奖励建模

传统一致性奖励模型（如 CLIP-I、DreamSim 等基于嵌入相似度的方法，以及 EditScore 等标量回归模型）在捕捉人类对视觉一致性的细粒度偏好时存在明显错位——它们要么依赖预训练视觉编码器的全局特征距离，要么通过额外的回归头输出连续分数，缺乏对“一致性”这一二元判断的显式建模。

**PaCo-Reward 将一致性评估重构为视觉语言模型（VLM）的下一个 token 预测任务**：给定一对图像，模型直接预测“Yes”或“No”的概率，并将其作为一致性得分。这一设计的核心洞察在于，自回归 VLM 的生成式先验天然适合处理需要细粒度视觉比较的判断任务，避免了额外回归头引入的表示错位。训练目标采用加权似然损失：

$$\mathcal{L}_{\mathrm{PaCo}} = -\left[ \alpha \log p(y_0 \mid I) + \frac{(1-\alpha)}{n-1} \sum_{i=1}^{n-1} \log p(y_i \mid I) \right]$$

其中 $y_0$ 为决策 token（Yes/No），$y_i$ 为推理链 token，$\alpha=0.1$ 时泛化最优——这一极小的决策 token 权重表明，模型主要从推理链中学习一致性判断的视觉依据，而非简单记忆答案。

**证据强度**：在 ConsistencyRank 基准上，基于 Qwen2.5-VL-7B 微调的 PaCo-Reward-7B 将准确率从 0.344 提升至 0.449（+10.5%），Spearman $\rho$ 增加 0.150（Table 2）。在 EditReward-Bench 上，一致性准确率达到 0.709，显著超越包括 EditScore-72B（0.586）在内的所有开源基线，并接近 GPT-5（0.669）的闭源水平（Table 1）。这验证了生成式二分类范式在一致性评估上的有效性。

### 2. 分辨率解耦训练与对数驯化多奖励聚合

在 RL 微调阶段，PaCo-GRPO 针对两个关键瓶颈提出了解决方案：

**瓶颈一：全分辨率训练的极高计算开销。** 一致图像生成（尤其是多图像场景）在高分辨率下进行 RL 训练时，奖励计算和梯度反传的显存与时间成本随像素数呈超线性增长。

**解决方案：分辨率解耦训练。** 训练时使用低分辨率（如 512×512，即 0.5x）图像进行奖励计算和优化，推理时仍保持全分辨率（1024×1024）。其可行性依赖于一个关键实证发现：在 0.5x 降分辨率下，各评价指标（美学、提示对齐、视觉一致性）的 Pearson 相关系数保持在 0.725–0.848，奖励信号的相对排序高度可靠（Figure 15）；而降至 0.25x 时相关性大幅衰减，尤其是美学和一致性指标，说明 0.5x 是当前保持信号保真度的下限。

**证据强度**：消融实验（Table 5）显示，PaCo-GRPO 在 0.5x 分辨率下训练 6 小时，美学（0.555）、提示对齐（0.728）、视觉一致性（0.493）全面优于移除分辨率解耦后全分辨率训练 12 小时的结果（0.542/0.698/0.452）。训练时间减半的同时性能反超，证实了该策略的效率与有效性。

**瓶颈二：多奖励信号的相互支配。** 当同时优化视觉一致性、美学质量和提示对齐等多个奖励时，不同奖励的数值波动幅度差异会导致某一奖励主导优化方向，造成训练不稳定甚至生成退化。

**解决方案：对数驯化聚合。** 引入奖励波动系数 $h^k$ 衡量第 $k$ 个奖励在所有样本上的变异系数：

$$h^k = \frac{\mathrm{std}_{i,j}(R^k(\pmb{x}_i^j, \pmb{c}_i))}{\mathrm{mean}_{i,j}(R^k(\pmb{x}_i^j, \pmb{c}_i))}$$

当 $h^k > \delta$ 时，对该奖励应用对数压缩：

$$\overline{R}^k(\pmb{x}_i^j, \pmb{c}_i) = \begin{cases} \log(1 + R^k(\pmb{x}_i^j, \pmb{c}_i)), & \text{if } h^k > \delta \\ R^k(\pmb{x}_i^j, \pmb{c}_i), & \text{otherwise} \end{cases}$$

这一变换在压缩波动幅度的同时保持奖励的相对排序，防止高波动奖励在加权求和中占据不成比例的权重。

**证据强度**：Figure 6 显示，对数驯化聚合将一致性/提示对齐奖励比稳定在 1.8 以下，而标准加权聚合在训练后期该比率超过 2.5，导致视觉一致性奖励主导优化。消融实验（Table 5）进一步证实，移除对数驯化后美学（0.471 vs 0.555）和提示对齐（0.616 vs 0.728）大幅下降，尽管视觉一致性分数虚高（0.557 vs 0.493），但实际生成质量严重退化，出现近乎重复的低质量图像。

### 创新边界与局限

上述两个变更槽构成了 PaCo-RL 相对于现有方法的核心差异化能力，但其有效性存在明确边界：（1）PaCo-Reward 的生成式二分类范式受限于基座 VLM 的能力上限，当前基于 Qwen2.5-VL-7B，更大规模 VLM 可能进一步释放潜力；（2）分辨率解耦训练在 0.5x 以下分辨率时信号可靠性急剧下降，0.5x 是当前已验证的下界；（3）对数驯化聚合中的阈值 $\delta$ 当前设为固定值 0.2，其跨任务通用性尚未在更广泛的奖励组合上验证。

## 整体框架

PaCo-RL 的整体 pipeline 由三个核心模块串联构成：**PaCo-Dataset 构建** → **PaCo-Reward 训练** → **PaCo-GRPO 强化学习微调**。其设计逻辑围绕一个核心洞察展开：将一致性评估重构为视觉语言模型（VLM）的下一个 token 预测（Yes/No 概率），充分利用自回归特性避免额外回归头导致的感知错位；同时在 RL 阶段采用低分辨率采样并辅以基于奖励波动的对数压缩，在不损害推理质量的前提下大幅降低计算成本并防止单一奖励主导优化。

### 模块一：PaCo-Dataset 构建

输入为原始图像对或子图配对，通过自动合成与人工标注相结合的流程，构建覆盖 6 大类 32 个子类的成对一致性数据集。数据集采用 2×2 网格排布，最终产出约 33,984 个唯一排序实例，用于训练和评估奖励模型。标注由六位训练有素的标注者独立完成，最终标签通过多数表决确定，平局被丢弃以保证清晰的二元偏好。

### 模块二：PaCo-Reward 训练

以 **Qwen2.5-VL-7B**（Qwen team, arXiv 2025）为基座，在 PaCo-Dataset 上进行微调。PaCo-Reward 将一致性评估重构为生成式二分类任务——直接预测 “Yes” 或 “No” 的概率作为一致性得分，而非依赖标量回归头。训练目标采用加权似然损失：

$$\mathcal{L}_{\mathrm{PaCo}} = -\left[ \alpha \log p(y_0 \mid I) + \frac{(1-\alpha)}{n-1} \sum_{i=1}^{n-1} \log p(y_i \mid I) \right]$$

其中 $y_0$ 为决策 token，$y_i$ 为推理序列 token，$\alpha=0.1$ 时泛化最佳。该模块输出一个可感知视觉一致性的成对奖励模型 PaCo-Reward-7B，为下游 RL 训练提供奖励信号。

### 模块三：PaCo-GRPO 强化学习微调

对图像生成模型（如 **FLUX.1-dev** 或 **Qwen-Image-Edit**）进行在线 GRPO 优化，集成了两项关键策略：

1. **分辨率解耦训练**：训练时生成低分辨率图像（如 512×512，即 0.5x），用于奖励计算和优化；推理时仍使用全分辨率（1024×1024）。这大幅降低了计算开销，且 0.5x 分辨率下所有评价指标的 Pearson 相关系数保持在 0.725–0.848，奖励排序可靠。

2. **对数驯化多奖励聚合**：当某一奖励的波动系数 $h^k$ 超过阈值 $\delta$ 时，对其应用对数压缩：

$$\overline{R}^k(\pmb{x}_i^j, \pmb{c}_i) = \begin{cases} \log(1 + R^k(\pmb{x}_i^j, \pmb{c}_i)), & \text{if } h^k > \delta \\ R^k(\pmb{x}_i^j, \pmb{c}_i), & \text{otherwise} \end{cases}$$

其中波动系数 $h^k = \frac{\mathrm{std}_{i,j}(R^k)}{\mathrm{mean}_{i,j}(R^k)}$，$\delta$ 默认为 0.2。该策略将一致性/提示对齐奖励比稳定在 1.8 以下，防止单一奖励主导优化导致生成退化。

RL 训练中关闭 KL 惩罚（$\beta=0$），沿用 FlowGRPO 的设置以获得更好性能；同时引入 SDE 采样更新为流匹配模型增加随机性，增强探索多样性。图像编辑任务仅依赖单一奖励信号（PaCo-Reward），未使用多奖励聚合，消除了多信号交互引入的潜在偏差。

### 输入输出流总结

- **PaCo-Dataset 构建**：原始图像对/子图配对 → 成对一致性标注数据集
- **PaCo-Reward 训练**：成对图像 + 一致性标签 → 生成式二分类奖励模型（Yes/No 概率）
- **PaCo-GRPO 微调**：文本提示 + 低分辨率采样 → 多奖励聚合（含对数驯化）→ GRPO 优化 → 全分辨率一致图像输出

### 补充图表

![[assets/figures/papers/paper_list_l2698_https_arxiv_org_abs_2512_04784/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the proposed PaCo-Reward framework*

![[assets/figures/papers/paper_list_l2698_https_arxiv_org_abs_2512_04784/figures/003_Figure_3.jpg]]
*Figure 3: Overview of our proposed PaCo-GRPO framework on Text-to-ImageSet generation task*

## 核心模块与公式推导

PaCo-RL 的核心架构由两个紧密协作的模块构成：**PaCo-Reward**（成对一致性奖励模型）与 **PaCo-GRPO**（面向一致图像生成的强化学习策略）。前者负责提供与人类感知对齐的一致性评估信号，后者则将该信号高效、稳定地注入图像生成模型的在线优化过程。

### 3.1 PaCo-Reward：生成式成对一致性评估

传统奖励模型通常依赖额外的标量回归头输出一致性分数，这种设计与其基座 VLM 的自回归预训练目标存在错位，限制了感知对齐能力。PaCo-Reward 的核心创新在于**将一致性评估重构为生成式二分类任务**——给定两张图像，直接预测 VLM 输出 “Yes” 或 “No” 的概率，以此作为一致性得分。这一设计充分利用了 VLM 的下一 token 预测机制，无需引入额外的回归头。

**训练目标**采用加权似然损失，同时监督决策 token 与推理序列：

$$\mathcal{L}_{\mathrm{PaCo}} = -\left[ \alpha \log p(y_0 \mid I) + \frac{(1-\alpha)}{n-1} \sum_{i=1}^{n-1} \log p(y_i \mid I) \right]$$

其中：
- $I$ 为输入图像对及任务指令的拼接；
- $y_0$ 为决策 token（即 “Yes” 或 “No”）；
- $y_i$（$i=1,\dots,n-1$）为推理序列中的其余 token；
- $\alpha$ 控制决策 token 与推理序列的监督权重平衡。

实验表明 $\alpha=0.1$ 时泛化性能最佳——这一非对称权重设计意味着模型主要从推理链中学习一致性判断能力，而决策 token 仅需少量直接监督即可校准。

PaCo-Reward 基于 **Qwen2.5-VL-7B**（Qwen team, arXiv 2025）微调，训练数据来自自动构建的 **PaCo-Dataset**，涵盖 6 大类 32 个子类的一致性场景，包含约 34,000 个唯一排序实例。在 **ConsistencyRank** 基准上，PaCo-Reward-7B 相对基座 Qwen2.5-VL-7B 准确率提升 10.5%（0.344→0.449），Spearman $\rho$ 增加 0.150；在 **EditReward-Bench** 上，一致性准确率达 0.709，显著超越所有开源基线（如 EditScore-72B 的 0.586），接近闭源模型 **GPT-5**（OpenAI, 2025）的 0.669。

### 3.2 PaCo-GRPO：分辨率解耦与对数驯化聚合

将 PaCo-Reward 作为奖励信号引入图像生成模型的 GRPO（Group Relative Policy Optimization）在线优化时，面临两个关键瓶颈：（1）高分辨率图像生成与奖励计算的计算开销极大；（2）多奖励信号（如美学、提示对齐、视觉一致性）的数值波动差异会导致单一奖励主导优化，引发训练崩溃。

**分辨率解耦训练**策略将训练与推理的分辨率分离：训练阶段生成低分辨率图像（如 $h/2 \times w/2$，即 512×512）用于奖励计算与梯度优化，推理阶段仍使用全分辨率（1024×1024）。其可靠性由奖励排序的相关性实验支撑——在 0.5× 降分辨率下，所有评价指标的 Pearson 相关系数介于 0.725–0.848，表明低分辨率下的奖励信号仍能可靠反映全分辨率的相对优劣。但 0.25× 时相关性大幅下降，说明 0.5× 是当前保持信号可靠性的下限。

**对数驯化多奖励聚合**针对奖励波动幅度差异设计。首先定义第 $k$ 个奖励的波动系数：

$$h^k = \frac{\mathrm{std}_{i,j}(R^k(\pmb{x}_i^j, \pmb{c}_i))}{\mathrm{mean}_{i,j}(R^k(\pmb{x}_i^j, \pmb{c}_i))}$$

即所有样本上该奖励的标准差与均值之比。当 $h^k$ 超过阈值 $\delta$ 时，对该奖励施加对数压缩：

$$\overline{R}^k(\pmb{x}_i^j, \pmb{c}_i) = \begin{cases} \log(1 + R^k(\pmb{x}_i^j, \pmb{c}_i)), & \text{if } h^k > \delta \\ R^k(\pmb{x}_i^j, \pmb{c}_i), & \text{otherwise} \end{cases}$$

对数变换在压缩波动幅度的同时保持奖励的相对顺序，从而防止高波动奖励（如视觉一致性）在加权求和中占据压倒性优势。实验显示，标准加权聚合下一致性/提示对齐奖励比在训练后期超过 2.5 并导致生成退化，而对数驯化聚合将该比值稳定在 1.8 以下。

**基础 GRPO 目标**沿用标准形式（实验中设 KL 惩罚系数 $\beta=0$ 以获得更好性能）：

$$J_\theta = J_{\mathrm{clip}} - \beta D_{\mathrm{KL}}(\pi_\theta \| \pi_{\mathrm{ref}})$$

为增强 RL 训练的探索多样性，采样过程引入 SDE 随机性：

$$\pmb{x}_{t+\Delta t} = \pmb{x}_t + \left[ \pmb{v}_\theta + \frac{\sigma_t^2}{2t} (\pmb{x}_t + (1-t)\pmb{v}_\theta) \right] \Delta t + \sigma_t \sqrt{\Delta t} \epsilon$$

消融实验验证了两个策略的因果效应：移除分辨率解耦训练后，即使训练时间加倍（12h vs 6h），美学（0.542 vs 0.555）、提示对齐（0.698 vs 0.728）和视觉一致性（0.452 vs 0.493）全面下降；移除对数驯化聚合则导致视觉一致性奖励占优，美学降至 0.471、提示对齐降至 0.616，生成图像趋于低质量重复。

### 补充图表

![[assets/figures/papers/paper_list_l2698_https_arxiv_org_abs_2512_04784/figures/001_Figure_1.jpg]]
*Figure 1: Two Representative Tasks in Consistent Image Generation. In the image editing task, the model needs to modify specific attributes while preserving the overall appearance. In the text-to-image set generation task, the goal is to generate multiple coherent images that remain consistent in identity, style, and context under a unified description*

![[assets/figures/papers/paper_list_l2698_https_arxiv_org_abs_2512_04784/figures/010_Figure_6.jpg]]
*Figure 6: Ablation of log-tamed aggregation on the reward ratio*

![[assets/figures/papers/paper_list_l2698_https_arxiv_org_abs_2512_04784/figures/020_Figure_15.jpg]]
*Figure 15: Pearson correlation of evaluation metrics across different training-to-inference resolution ratios. Strong correlations at 0.5x confirm that reward signals remain reliable under moderate resolution reduction*

## 实验与分析

### 核心实验设计

PaCo-RL 的实验验证围绕两条主线展开：首先独立评估 PaCo-Reward 作为一致性奖励模型的人类偏好对齐能力，然后将其嵌入 PaCo-GRPO 强化学习框架，验证其对图像生成模型一致性提升的实际效果。实验覆盖两个代表性任务——文本到图像集生成（Text-to-ImageSet）和图像编辑（Image Editing），并在多个基准上与开源和闭源方法进行系统对比。

**奖励模型评估**采用 EditReward-Bench 和 ConsistencyRank 两个基准。EditReward-Bench 衡量奖励模型在编辑场景下对提示遵循（PF）、一致性（Consistency）和综合质量（Overall）的判断准确率；ConsistencyRank 则专门评估模型对成对图像一致性排序的能力，包含 Accuracy、Kendall's τ、Spearman's ρ 和 Top-1/Bottom-1 一致性识别率（T1-B1）四项指标。

**生成模型评估**在 T2IS-Bench 和 GEdit-Bench 上进行。T2IS-Bench 评估文本到图像集生成的美学质量（Aesthetics）、提示对齐（Prompt Following）和视觉一致性（Visual Consistency），其中视觉一致性由 Qwen2.5-VL-7B 和 Gemma-3-4B 两个独立评估器交叉验证（表中以“/”分隔）。GEdit-Bench 覆盖中英文指令的编辑任务，评估图像保真度、指令遵循和整体质量。

### 奖励模型基准结果

PaCo-Reward-7B 在两个奖励模型基准上均显著超越所有开源基线，并在多个指标上接近或超越闭源模型。

**EditReward-Bench（Table 1）**：PaCo-Reward-7B 的一致性准确率达到 0.709，较最强的开源基线 EditScore-72B（0.586）提升 12.3 个百分点，甚至超越 GPT-5（0.669）。综合得分 0.751，仅次于 GPT-5 的 0.771，但显著高于所有其他开源模型。值得注意的是，PaCo-Reward-7B 仅使用 7B 参数，而 EditScore 系列模型参数量达 72B，效率优势明显。

**ConsistencyRank（Table 2）**：相比基座模型 Qwen2.5-VL-7B，PaCo-Reward-7B 在 Accuracy 上提升 10.5 个百分点（0.344→0.449），Spearman's ρ 增加 0.150（0.138→0.288），Kendall's τ 从 0.096 提升至 0.250。这些结果表明，PaCo-Reward 的生成式二分类训练范式有效增强了一致性排序能力，而非仅在绝对评分上拟合。T1-B1 指标达到 0.557，说明模型对极端一致性差异的判别尤为可靠。

### 生成模型主要结果

**文本到图像集生成（Table 3）**：FLUX.1-dev 经 PaCo-GRPO 微调后，视觉一致性身份指标从无 RL 基线的 0.249/0.636 跃升至 0.508/0.837（Qwen2.5-VL-7B/Gemma-3-4B 评估），提升幅度超过一倍。同时，美学质量（0.555 vs 0.527）和提示对齐（0.728 vs 0.703）也同步改善，表明一致性优化并未以牺牲其他维度为代价。与闭源系统对比，PaCo-GRPO 的视觉一致性（0.837）超越 GPT-4o（0.798）和 Gemini 2.0 Flash（0.762），在开源方案中达到最优。

**图像编辑（Table 4）**：Qwen-Image-Edit 经 PaCo-GRPO 微调后，在 GEdit-Bench 英文指令编辑（EN-I）上的总体得分从 7.307 提升至 7.451，且图像保真度和指令遵循子指标全面提升。值得关注的是，图像编辑任务仅使用单一一致性奖励信号（未启用多奖励聚合），这排除了多信号交互的干扰，直接验证了 PaCo-Reward 作为优化目标的独立有效性。

### 消融实验：PaCo-GRPO 组件分析

Table 5 的消融实验揭示了 PaCo-GRPO 两个核心组件的关键作用。

![[assets/figures/papers/paper_list_l2698_https_arxiv_org_abs_2512_04784/figures/019_Table_5.jpg]]
*Table 5: Ablation study on PaCo-GRPO components. Removing resolution-decoupled training leads to suboptimal performance even with doubled training time, while removing log-tamed aggregation causes reward collapse*

**分辨率解耦训练**：移除该策略后（W/O Res-Dec.），即使将训练时间加倍至 12 小时，所有指标均出现退化——美学从 0.555 降至 0.542，提示对齐从 0.728 降至 0.698，视觉一致性从 0.493 降至 0.452。这表明低分辨率训练不仅降低了计算开销，还通过某种正则化效应避免了全分辨率下的过拟合倾向。Figure 15 的 Pearson 相关性分析进一步验证：在 0.5× 降分辨率下，各评价指标的相关性保持在 0.725–0.848，奖励信号排序可靠；但降至 0.25× 时，美学和一致性指标的相关性大幅下降，说明 0.5× 是当前设置下的可靠下限。

**对数驯化聚合**：移除该策略后（W/O Log-Agg.），视觉一致性奖励出现支配性膨胀（V.C. 升至 0.557），但美学（0.471）和提示对齐（0.616）大幅下降。Figure 6 的奖励比曲线直观展示了这一现象：标准加权聚合下，一致性/提示对齐奖励比在训练后期突破 2.5，导致模型生成近乎重复的低质量图像；而对数驯化聚合将该比值稳定控制在 1.8 以下，维持了多目标优化的平衡。

### 训练过程可视化与定性分析

Figure 7 展示了固定随机种子下文本到图像集生成的渐进式改善：随着 PaCo-RL 训练推进，生成的人物身份、服饰细节和场景风格逐步趋向一致，从初始的随机变异收敛为连贯的视觉叙事。Figure 8 的图像编辑训练过程则显示，模型逐渐学会在修改目标属性（如发色、表情）的同时保持无关区域的高度保真。

![[assets/figures/papers/paper_list_l2698_https_arxiv_org_abs_2512_04784/figures/011_Figure_7.jpg]]
*Figure 7: Progressive improvement of images generated with a fixed seed during PaCo-RL training for Text-to-ImageSet generation*

![[assets/figures/papers/paper_list_l2698_https_arxiv_org_abs_2512_04784/figures/012_Figure_8.jpg]]
*Figure 8: Training progression visualization for Image Editing with different prompts*

Figure 12–14 的跨方法定性对比进一步佐证了定量结果：PaCo-GRPO 在多人物身份保持、跨视角风格统一和复杂场景编辑等挑战性场景下，均展现出比 Seedream 4.0、AutoT2IS 等方法更优的一致性表现。

### 失败模式与局限性

尽管整体表现优异，实验也揭示了若干边界条件。首先，0.25× 分辨率下奖励信号的可靠性显著下降（Figure 15），限制了进一步压缩计算开销的空间。其次，在极端属性编辑（如大幅姿态变换）场景下，模型偶尔出现身份泄露或背景扭曲，这源于 PaCo-Reward 对细粒度空间对应关系的感知局限——其基于全局 VLM 的评估机制难以精确定位局部不一致区域。此外，当前验证仅限于构造基准上的分布内评估，论文未报告在真实照片编辑等分布外场景上的泛化性能，该点需要后续工作验证。

### 补充图表

![[assets/figures/papers/paper_list_l2698_https_arxiv_org_abs_2512_04784/figures/004_Table_1.jpg]]
*Table 1: Benchmark results on EditReward-Bench*

![[assets/figures/papers/paper_list_l2698_https_arxiv_org_abs_2512_04784/figures/005_Table_2.jpg]]
*Table 2: Benchmark results on ConsistencyRank*

![[assets/figures/papers/paper_list_l2698_https_arxiv_org_abs_2512_04784/figures/006_Table_3.jpg]]
*Table 3: Comparisons with various Text-to-ImageSet generation methods on T2IS-Bench. Scores for Visual Consistency are evaluated by two independent evaluators, Qwen2.5-VL-7B and Gemma-3-4B (values before/after the slash), to ensure cross-model reliability*

![[assets/figures/papers/paper_list_l2698_https_arxiv_org_abs_2512_04784/figures/007_Table_4.jpg]]
*Table 4: Benchmark results on GEdit-Bench. EN-I and EN denote English instructions, while CN-I and CN denote Chinese instructions*

## 方法谱系与知识库定位

### 1. 与现有方法的谱系关系

PaCo-RL 的方法栈由两条主线交织而成：**一致性奖励建模** 与 **面向一致性的强化学习微调**。下文按这两条线索梳理其与前人工作的继承与突破关系。

#### 1.1 奖励建模：从标量回归到生成式二分类

在 PaCo-Reward 之前，视觉一致性的自动评估主要依赖两类方案：

- **视觉相似度度量**：**CLIP-I**（Radford et al., ICML 2021）与 **DreamSim**（Fu et al., arXiv 2023）通过嵌入空间的距离度量来评判图像间相似度。这类方法无需专门训练，但缺乏对高层语义一致性（如身份保持、风格连贯）的感知能力，与人类偏好的一致性有限。
- **标量回归奖励模型**：**EditScore-7B** 等模型在 VLM 之上附加回归头，输出连续一致性分数。这种设计存在固有错位——回归头独立于 VLM 的预训练目标（下一个 token 预测），导致奖励信号与 VLM 内部表征之间的语义鸿沟。

PaCo-Reward 的核心突破在于**将一致性评估重构为 VLM 自身的下一个 token 预测任务**：输入两张图像及对应指令，模型直接输出 "Yes" 或 "No" 的概率作为一致性得分。这一设计与基座 **Qwen2.5-VL-7B**（Qwen team, arXiv 2025）的自回归特性完全对齐，避免了额外回归头引入的表征错位。训练时采用加权似然目标，以 $\alpha=0.1$ 平衡决策 token 与推理序列的监督强度：

$$\mathcal{L}_{\mathrm{PaCo}} = -\left[ \alpha \log p(y_0 \mid I) + \frac{(1-\alpha)}{n-1} \sum_{i=1}^{n-1} \log p(y_i \mid I) \right]$$

在基准评测中，这一生成式范式带来了显著增益：PaCo-Reward-7B 在 **ConsistencyRank** 上相对基座 Qwen2.5-VL-7B 准确率提升 10.5%（0.344→0.449），Spearman ρ 增加 0.150（Table 2）；在 **EditReward-Bench** 上一致性准确率达到 0.709，显著超越所有开源基线（如 EditScore-72B 的 0.586），接近闭源模型 **GPT-5** 的 0.669（Table 1）。

#### 1.2 强化学习微调：从全分辨率训练到分辨率解耦

将奖励模型集成到图像生成模型的强化学习微调中并非 PaCo-RL 首创，但现有方案面临两个瓶颈：

- **计算开销**：全分辨率（如 1024×1024）下的在线采样与奖励计算成本极高，限制了训练规模和迭代速度。
- **多奖励支配**：在文本到图像集生成等任务中，需同时优化美学质量、提示对齐和视觉一致性等多个奖励信号。标准加权求和聚合下，波动幅度大的奖励（如视觉一致性）会主导梯度更新，导致其他维度退化。

PaCo-GRPO 针对性引入两项策略：

**分辨率解耦训练**：训练阶段生成低分辨率图像（如 512×512，即 0.5x）用于奖励计算和梯度优化，推理阶段仍保持全分辨率生成。这一设计的可行性建立在奖励信号在降分辨率下仍保持可靠排序的实证验证之上——在 0.5x 分辨率下，所有评价指标的 Pearson 相关系数保持在 0.725–0.848（Figure 15）。消融实验（Table 5）表明，分辨率解耦训练在 **6 小时**内（0.5x 分辨率）达到比全分辨率训练 12 小时更优的综合表现（美学 0.555 vs 0.542，提示对齐 0.728 vs 0.698，视觉一致性 0.493 vs 0.452）。

**对数驯化多奖励聚合**：引入奖励波动系数 $h^k$ 衡量第 $k$ 个奖励在所有样本上的变异系数：

$$h^k = \frac{\mathrm{std}_{i,j}(R^k(\pmb{x}_i^j, \pmb{c}_i))}{\mathrm{mean}_{i,j}(R^k(\pmb{x}_i^j, \pmb{c}_i))}$$

当 $h^k$ 超过阈值 $\delta$ 时，对该奖励施加对数压缩：

$$\overline{R}^k(\pmb{x}_i^j, \pmb{c}_i) = \begin{cases} \log(1 + R^k(\pmb{x}_i^j, \pmb{c}_i)), & \text{if } h^k > \delta \\ R^k(\pmb{x}_i^j, \pmb{c}_i), & \text{otherwise} \end{cases}$$

这一策略将一致性/提示对齐奖励比稳定在 1.8 以下，而标准加权聚合在训练后期超过 2.5 并导致生成退化（Figure 6）。移除对数驯化聚合后，视觉一致性奖励占优，模型生成低质量、近乎重复的图像，美学和提示对齐大幅下降（Table 5）。

#### 1.3 在图像生成模型谱系中的定位

PaCo-RL 在两个代表性任务上验证了其通用性：

- **文本到图像集生成**：以 **FLUX.1-dev**（Black Forest Labs, 2024）为基础模型，集成 PaCo-Reward-7B 进行 GRPO 微调后，在 T2IS-Bench 的视觉一致性身份指标上达到 0.508/0.837（Qwen2.5-VL-7B/Gemma-3-4B 评估），远超无 RL 基线的 0.249/0.636（Table 3）。与闭源方案 **GPT-4o**（OpenAI, 2025）和 **Gemini 2.0 Flash**（Google, 2025）相比，PaCo-RL 在一致性维度展现出竞争力，但需注意闭源模型的训练细节不可知，直接对比存在局限。
- **图像编辑**：以 **Qwen-Image-Edit**（Wu et al., 2025）为基础模型，在 GEdit-Bench 的 EN-I 总体得分从 7.307 提升至 7.451，且各项子指标全面提升（Table 4）。该任务仅依赖单一一致性奖励信号，未使用多奖励聚合，从而排除了多信号交互引入的潜在偏差。

### 2. 适用边界与关键局限

基于论文报告的证据与未覆盖场景，PaCo-RL 的适用边界可归纳如下：

1. **分辨率下限约束**：奖励信号的可靠性在 0.5x 分辨率下仍可保持（Pearson 相关系数 0.725–0.848），但在 0.25x 时显著下降，尤其是美学和一致性维度（Figure 15）。这意味着分辨率解耦训练的下限约为 0.5x，进一步压缩将损害优化信号质量。

2. **任务范围限制**：当前验证场景仅限于图像编辑和文本到图像集生成两类任务。论文未涉及视频一致性（时序上的身份、风格和逻辑连贯）、3D 多视角一致性等更复杂的跨帧/跨模态场景。PaCo-Reward 的成对比较范式在理论上可迁移，但缺乏实证支持。

3. **基座模型能力天花板**：PaCo-Reward 基于 Qwen2.5-VL-7B 微调，其一致性评估能力的上限受基座 VLM 的视觉理解和推理能力制约。更大规模的 VLM（如 InternVL3.5-8B 的更大变体）可能进一步提升奖励质量，但论文未对此进行实验验证。

4. **计算资源门槛**：RL 训练仍需 8 张 H100 GPU 和专门的 vLLM 奖励服务，尚未降低到消费级硬件可运行的规模。这限制了该方法在资源受限场景下的推广。

5. **分布外泛化未知**：所有评估均在构造的基准数据集上进行（T2IS-Bench、GEdit-Bench、EditReward-Bench、ConsistencyRank）。论文未报告在更广泛的分布外场景（如真实照片编辑、复杂场景组合生成）上的泛化性能，这是实际部署前需要补全的关键证据。

### 3. 开放问题

基于上述分析，以下开放问题值得后续工作关注：

- **跨模态迁移**：PaCo-RL 的成对奖励建模和分辨率解耦策略能否直接迁移到视频一致生成？视频场景下的时序一致性涉及更复杂的跨帧依赖，可能需要扩展为多帧比较或序列建模范式。
- **自适应阈值学习**：对数驯化聚合中的阈值 $\delta$ 当前采用固定值（0.2）或简单均值。能否设计完全自适应的阈值学习机制，使其在不同任务和奖励分布下自动调节压缩强度？
- **通用一致性评估器**：PaCo-Reward 的生成式二分类范式能否发展为通用的多图像一致性评估器，替代现有的多维人工评分？这需要在更广泛的一致性维度（如叙事连贯性、情感一致性）上进行验证。
- **效率优化**：能否结合量化、蒸馏或模型轻量化技术进一步降低 RL 训练对 GPU 资源的依赖？当前 8×H100 的门槛限制了学术研究和中小团队的复现能力。
- **开放式生成泛化**：在故事创作等开放式生成任务中，PaCo-Reward 能否泛化到未见过的远域一致性维度（如情节连贯性、角色发展一致性）？这需要构建相应的高质量成对偏好数据集。

## 原文 PDF

![[paperPDFs/CVPR_2026/PaCo_RL_Advancing_Reinforcement_Learning_for_Consistent_Image_Generation_with_Pairwise_Reward_Modeling.pdf]]
