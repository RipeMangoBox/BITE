---
title: "Attend Before Attention: Efficient and Scalable Video Understanding via Autoregressive Gazing"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Attend_Before_Attention_Efficient_and_Scalable_Video_Understanding_via_Autoregressive_Gazing.pdf
project_link: "https://autogaze.github.io/"
code_link: null
aliases:
- ABAESVUAG
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 在ViT前通过AutoGaze自回归选择最小化的多尺度补丁集合（凝视比例），直接控制输入ViT的视觉token数量，从而实质性地减少计算开销并实现扩展。
primary_logic: 利用视频中的时空冗余，通过自回归凝视机制以重建误差为引导选择最优的最小补丁子集，在保持信息的同时大幅减少视觉token；并通过下一token预测(NTP)预训练与强化学习(RL)后训练学习最优凝视策略，使模型能够自动决定何时停止凝视。
claims:
- AutoGaze reduces visual tokens by 4×-100× and accelerates ViTs and MLLMs by up to 19× and 10× respectively.
- Scaling an MLLM to 1K frames and 4K resolution via AutoGaze improves HLVid accuracy from 42.5% to 52.6%, outperforming the previous best MLLM by 4.5%.
- With 6.25% visual tokens, AutoGaze achieves ViT latency of 0.55s and LLM latency of 0.10s, reducing ViT latency by 4× while maintaining VideoMME accuracy (52.3 vs. 53.4 baseline).
- VideoMME (w/o sub) 上 accuracy = 67.0
---

# Attend Before Attention: Efficient and Scalable Video Understanding via Autoregressive Gazing

> [!tip] 核心洞察
> 利用视频中的时空冗余，通过自回归凝视机制以重建误差为引导选择最优的最小补丁子集，在保持信息的同时大幅减少视觉token；并通过下一token预测(NTP)预训练与强化学习(RL)后训练学习最优凝视策略，使模型能够自动决定何时停止凝视。

| 字段 | 内容 |
|------|------|
| 中文题名 | 先注视再关注：通过自回归凝视的高效可扩展视频理解 |
| 英文题名 | Attend Before Attention: Efficient and Scalable Video Understanding via Autoregressive Gazing |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.12254) · [Project](https://autogaze.github.io/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | AutoGaze |
| Dataset | VideoMME, HLVid, LongVideoBench, ViT Latency |

> [!tip] 效果简介
> - VideoMME (w/o sub) 上，accuracy 67.0 vs 64.2 (+2.8)。
> - VideoMME (w/ sub) 上，accuracy 71.8 vs 70.0 (+1.8)。
> - HLVid (test) 上，accuracy 52.6 vs 42.5 (+10.1)。

## 概要

### 问题背景

当前多模态大语言模型（MLLM）在视频理解任务中面临一个根本性的计算瓶颈：视觉Transformer（ViT）必须处理视频的**全部像素**，这严重限制了模型向长视频和高分辨率视频的扩展能力。已有方法（如VideoChat-Flash）仅在LLM端进行token剪枝，但ViT仍需处理完整帧的所有补丁，计算开销并未实质性降低。

### 核心方法：AutoGaze

本文提出**AutoGaze**——一个仅3M参数的轻量级凝视模块，在ViT之前通过自回归方式选择最优的**最小多尺度补丁集合**，从而直接削减输入ViT的视觉token数量。其核心思想是利用视频中的时空冗余，以重建误差为引导信号，通过自回归凝视机制决定每帧需要保留哪些补丁及何时停止凝视，在保持信息完整性的同时大幅压缩计算量。

AutoGaze采用两阶段训练策略：先通过下一token预测（NTP）预训练学习基本的凝视行为，再通过强化学习（GRPO）后训练以重建奖励优化凝视策略，使模型能够自动发现更低重建损失的凝视序列。

### 主要结果

- **效率提升**：AutoGaze可将视觉token减少4×–100×，ViT加速最高达19×，MLLM加速最高达10×。在仅使用6.25%视觉token的条件下，ViT延迟从2.20秒降至0.55秒（4×加速），LLM延迟从1.42秒降至0.10秒（14.2×加速）。
- **性能表现**：在VideoMME（w/o sub）上达到67.0%，超过基础MLLM 2.8个百分点；在HLVid长视频高分辨率基准上，将基线MLLM从42.5%提升至52.6%（+10.1%），超越此前最佳MLLM 4.5个百分点。
- **扩展能力**：AutoGaze使MLLM能够扩展至1K帧、4K分辨率视频，而基线方法在超过256帧时即因显存不足而无法运行。

### 方法定位

AutoGaze区别于现有token缩减方法的关键在于**在ViT之前**而非之后进行补丁选择。现有方法（如VideoChat-Flash）仅在LLM端剪枝token，ViT仍需处理全量像素，因此ViT延迟不变。AutoGaze通过前置凝视模块直接控制ViT输入规模，同时加速ViT和LLM两端，实现了从视觉编码到语言推理的全链路效率提升。

### 视频理解的效率瓶颈：从LLM剪枝到ViT前移

多模态大语言模型（MLLM）在视频理解任务中展现出强大能力，但其计算效率始终是制约实际部署与规模扩展的核心障碍。现有MLLM的典型架构采用“视觉Transformer（ViT）编码 + 大语言模型（LLM）推理”的串行管线：ViT首先将视频帧切分为固定网格补丁并全量编码为视觉token，随后LLM在这些token上进行跨模态推理。

这一管线存在一个被长期忽视的结构性瓶颈：**ViT必须处理所有像素**。即使LLM端可以通过token剪枝大幅减少待处理token数量，ViT仍需对完整视频帧进行前向计算，其计算量随帧率和分辨率线性增长。例如，处理一段30 FPS的4K视频时，ViT每秒需编码的数百万个补丁构成了不可逾越的计算壁垒。

此前的高效视频理解方法，如**VideoChat-Flash**等，将优化重心放在LLM端的token剪枝上——在ViT完成全量编码后，再通过空间、时间或时空维度的剪枝策略减少输入LLM的视觉token。这类方法虽然降低了LLM的推理延迟，却未能触及真正的计算瓶颈：**ViT的计算开销并未减少**。当视频长度和分辨率持续增长时，ViT的编码时间将主导整体延迟，使LLM端的加速效果被稀释。

### 核心洞察：利用时空冗余进行“先注视再关注”

AutoGaze的核心动机源于一个朴素但关键的观察：**视频中存在大量时空冗余**。相邻帧之间、单帧内部的大部分区域承载的视觉信息高度重复，无需全部送入ViT进行精细编码。人类视觉系统正是通过选择性注视（gaze）机制，仅对场景中的关键区域进行高分辨率感知，从而在有限的计算资源下实现高效理解。

基于这一洞察，AutoGaze提出了一种范式转换：**将补丁选择从ViT之后前移至ViT之前**。具体而言，AutoGaze在ViT编码前引入一个轻量级的“凝视”模块，自回归地选择每帧中最具信息量的最小多尺度补丁子集，仅将选中的补丁送入ViT。这一设计从根源上削减了ViT的输入规模，使ViT的计算量与视频的信息密度而非像素总量挂钩。

### 技术挑战与设计目标

实现上述范式转换面临三重挑战：

1. **最优补丁子集的选择**：如何在给定凝视长度下，选出能最大化保留视频信息的补丁组合？这本质上是一个组合优化问题，穷举搜索不可行。
2. **凝视长度的自动决策**：不同视频的信息密度差异巨大——一段静态演讲视频所需的凝视比例远低于一段快速运动的体育视频。凝视模型需要自动判断何时已“看够”，而非依赖人工预设固定比例。
3. **凝视策略的可学习性**：启发式规则（如基于光流或随机选择）难以捕捉任务相关的语义重要性。凝视策略需要从数据中学习，使其能够根据下游MLLM的需求自适应调整。

AutoGaze通过三项关键设计应对这些挑战：以**重建误差为引导信号**定义补丁子集的信息保真度；在解码每一步**预测当前帧的重建损失**，当损失低于用户指定阈值时自动停止凝视；采用**下一token预测（NTP）预训练 + 强化学习（RL）后训练**的两阶段管线，使凝视策略从专家轨迹中学习基础行为，再通过RL探索更低重建损失的凝视序列。

### 预期收益与验证路径

AutoGaze的设计预期带来三个层面的收益：

- **ViT加速**：通过大幅减少ViT的输入token数量，直接降低ViT编码延迟。实验表明，AutoGaze可将视觉token减少4×至100×，ViT加速最高达19×。
- **MLLM整体加速**：ViT输出token的减少进一步降低了LLM的推理开销，使MLLM端到端加速最高达10×。
- **规模扩展能力**：效率的提升使MLLM能够处理此前因内存和计算限制而无法企及的超长、超高分辨率视频。例如，将MLLM扩展至1K帧、4K分辨率后，在HLVid基准上准确率从42.5%提升至52.6%，超越此前最优MLLM 4.5个百分点。

这些收益通过多个维度的实验进行验证：在VideoMME、LongVideoBench等通用与长视频基准上与SOTA MLLM对比精度；在统一硬件条件下测量ViT和LLM的延迟；通过消融实验验证各设计选择的贡献；并通过可视化分析揭示凝视行为的内在规律。

## 核心方法与创新机理

AutoGaze 的核心创新在于**将视觉token的选择时机从LLM端提前到ViT之前**，并引入一套自回归凝视机制来自动决定“看哪里”和“看多少”。这一设计直接切入了现有视频MLLM的根本计算瓶颈：ViT必须处理全部像素。

### 关键改变：从“全量处理”到“先凝视、再编码”

传统视频MLLM的管线是 ViT → 投影层 → LLM，其中ViT对每一帧的所有补丁进行无差别的全量编码。此前的token缩减方法（如VideoChat-Flash等）仅在LLM端做剪枝，ViT仍需处理全部视觉信息，因此ViT的计算开销并未减少。AutoGaze 将这一范式改为：

1. **AutoGaze凝视** → 2. **ViT编码（仅处理选定补丁）** → 3. **LLM推理**

这一时序上的前置（changed slot: “视觉token选择方式”）使得ViT的输入量被直接控制，从而实现了ViT和LLM的联合加速。

### 自回归多尺度凝视：自动决定“看哪里”

AutoGaze 是一个仅3M参数的轻量模块，由**卷积编码器**和**自回归Transformer解码器**组成。对于每一帧，解码器基于当前帧特征和历史凝视信息，自回归地解码出应选择的补丁索引。其核心机制包含两个层面的创新：

**多尺度补丁选择（changed slot: “ViT输入结构”）**。传统ViT接受单尺度固定网格的补丁嵌入，而AutoGaze允许ViT接受混合尺度的token序列——对每帧按不同尺度插值并分别嵌入，解码器在多个尺度上选择补丁。消融实验表明，多尺度凝视使凝视比例从0.220降至0.094（降低2.3×），延迟降低2.4×。其背后的直觉是：运动剧烈的区域用粗尺度捕获全局上下文，细节丰富的区域用细尺度保留纹理信息（Figure 4、Figure 5的统计分析支持这一行为）。

**自动停止凝视**。解码器每一步额外预测当前帧的重建损失。当预测损失低于用户指定的阈值时，AutoGaze自动停止对该帧的凝视——这意味着模型自行决定了最小的凝视长度$N^t$，无需人工预设每帧选择多少补丁。这一设计使得凝视比例可以随视频内容自适应变化：高FPS、高分辨率视频的时空冗余更高，仅需约1%的补丁即可达到重建损失0.7（Figure 7）。

### 学习最优凝视策略：NTP预训练 + RL后训练

AutoGaze的凝视策略并非启发式规则，而是通过两阶段训练习得：

- **NTP预训练**：使用贪心搜索从25万视频中收集近似最小化重建损失的凝视序列，然后通过下一token预测交叉熵损失 $\boldsymbol{L}_{NTP}$ 预训练AutoGaze，使其模仿这些“伪最优”凝视轨迹。
- **RL后训练**：以重建损失为奖励信号，使用简化版GRPO算法 $\mathcal{L}_{GRPO}$ 进行在线策略优化，使模型自主发现比贪心搜索更优的凝视序列。消融实验（Table 3）表明，完整的NTP+RL管线将凝视比例降至0.094，而仅预训练为0.102、仅RL为0.209、随机选择为0.263——两者缺一不可。

### 与启发式方法的本质区别

AutoGaze 的学习型凝视与随机选择、光流引导等启发式基线有本质差异。Figure 10显示，AutoGaze以5%的补丁达到重建损失1.0，而Random Gaze需要15%——效率提升3×。更关键的是，启发式方法（如光流凝视）仅依赖局部运动信息，无法建模全局重建质量；AutoGaze通过VideoMAE重建模型的反传信号，学习的是“哪些补丁对重建整个视频是不可或缺的”，这是一种全局信息量驱动的选择。

AutoGaze 的整体设计遵循“先注视再关注”（Attend Before Attention）的核心思想：在 ViT 处理视频帧之前，通过一个轻量级的自回归凝视模块预先筛选出最小化的多尺度补丁集合，仅将选中的补丁送入下游 ViT 和 MLLM，从而从源头上削减视觉 token 数量。其 pipeline 由四个关键模块串联构成，形成“编码—解码—预测—重建监督”的闭环。

### 输入输出流

给定一段 $T$ 帧的视频 $\boldsymbol{X}^{1:T}$，AutoGaze 将其映射为每帧选中补丁的索引序列：

$$
\mathtt{AutoGaze:} \boldsymbol{X}^{1:T} \to p_{1:N^1}^1, \dots, p_{1:N^T}^T
$$

其中 $N^t$ 为第 $t$ 帧的凝视长度（即选中补丁的数量）。该映射的目标是在给定凝视长度下最小化原始视频与从选中补丁重建的视频之间的损失：

$$
\min_{p_1^1,\ldots,p_{N^T}^T} L(\boldsymbol{X}^{1:T}, \mathrm{Recon}(\boldsymbol{X}^1[p_1^1],\ldots,\boldsymbol{X}^T[p_{N^T}^T]))
$$

### 模块串联关系

如图 3 所示，AutoGaze 的 pipeline 由以下模块依次构成：

1. **卷积编码器**：将每一帧编码为时空特征表示，作为后续自回归解码的条件信息。该编码器由一个空间核尺寸为 16 的 2D 卷积层和一个 3D 卷积层组成，参数极为轻量。

2. **自回归 Transformer 解码器**：基于当前帧的编码特征以及先前帧的凝视历史，自回归地逐 token 解码当前帧的多尺度补丁索引。每个解码步输出一个补丁索引 $p_k^t$，指示应在哪个尺度和空间位置提取补丁。

3. **重建损失预测头**：附加在解码器之上的预测头，在解码每个 $p_k^t$ 时同步预测当前帧的重建损失。一旦预测损失降至用户指定的阈值以下，AutoGaze 即自动停止对该帧的凝视——这意味着模型能够根据视频内容的复杂程度自适应地决定凝视长度 $N^t$，无需人工设定。

4. **VideoMAE 重建模型**：一个定制化的 VideoMAE（采用块因果注意力），根据 AutoGaze 选中的补丁集合重建完整视频，并计算重建损失。该重建损失在训练阶段作为监督信号，引导凝视策略学习选择最具信息量的补丁子集。

### 多尺度补丁机制

与现有 MLLM 中 ViT 仅接受单尺度固定网格补丁嵌入不同，AutoGaze 引入了多尺度补丁输入：对每帧按不同尺度进行插值并分别嵌入位置编码，ViT 随后接受混合尺度的 token 序列。这一设计使凝视策略能够根据区域的信息密度灵活选择尺度——高运动区域用粗尺度捕获全局上下文，高细节区域用细尺度保留纹理信息。

### 训练管线

AutoGaze 的训练分为两个阶段（图 3）：

- **阶段一：NTP 预训练**。通过贪婪搜索在 250K 视频上收集近似最小化重建损失的凝视序列 $\tilde{p}_{1:N^t}^t$，然后使用下一 token 预测（NTP）交叉熵损失预训练 AutoGaze：

  $$
  \boldsymbol{L}_{NTP} = -\sum_{t=1}^T\sum_{k=1}^{N^t} \log \pi_{\boldsymbol{\theta}}(\tilde{p}_k^t \mid \boldsymbol{X}^{1:t}, \tilde{p}_{1:N^1}^1,\dots,\tilde{p}_{1:k-1}^t)
  $$

- **阶段二：GRPO 强化学习后训练**。以重建奖励为优势信号，使用简化版 GRPO 算法对凝视策略进行在线微调，使其能够发现比贪婪搜索更优的凝视序列：

  $$
  \mathcal{L}_{GRPO} = -\sum_{t=1}^T\sum_{k=1}^{N^t} \frac{\pi_\theta(p_k^t)}{\pi_{\theta_{\text{detached}}}(p_k^t)} \mathcal{A}_k^t
  $$

消融实验表明，两个阶段缺一不可：完整管线达到凝视比例 0.094，仅预训练为 0.102，仅后训练为 0.209，随机基线则为 0.263（Table 3）。

### 下游使用

AutoGaze 本身是一个仅 3M 参数的轻量模块，独立于下游 ViT 和 MLLM。推理时，它处理任意分辨率和时长的视频：将视频切分为 $16 \times 224 \times 224$ 的时空块（tile），在每个 tile 上独立运行 AutoGaze，最后将各 tile 的凝视位置合并，提取对应补丁送入 ViT。这种 tile-wise 设计使其能够无缝扩展至 1K 帧、4K 分辨率的超长高清视频，而无需重新训练。

![[assets/figures/papers/paper_list_l837_https_arxiv_org_abs_2603_12254/figures/001_Figure_1.jpg]]
*Figure 1: We propose AutoGaze, which reduces the computational cost of video understanding to scale MLLMs to long, highresolution videos. (Left) Existing MLLMs either process all pixels which is inefficient, or prune tokens only in their LLMs, leaving ViTs the computational bottleneck. In contrast, AutoGaze eliminates redundant patches by up to 100× before ViTs, accelerating ViTs and MLLMs by up to 19×. (Right) This efficiency enables MLLMs with AutoGaze to scale to 1K-frame, 4K-resolution videos and achieve superior performance on HLVid, our new long, high-resolution video benchmark, surpassing prior MLLMs limited to short or low-resolution videos*

![[assets/figures/papers/paper_list_l837_https_arxiv_org_abs_2603_12254/figures/003_Figure_3.jpg]]
*Figure 3: Architecture and training pipeline of AutoGaze. (Left & Middle) Given a video, AutoGaze processes each frame and autoregressively decodes indices of multi-scale patches based on the history of frames and selected patches. Once it believes the previouslygazed patches are sufficient to reconstruct the current frame, it automatically stops gazing and moves to the next frame. (Right) AutoGaze is trained in two stages: next-token-prediction pre-training on collected gazing sequences, and RL post-training with reconstruction reward*

### 问题形式化：凝视作为补丁选择

AutoGaze 将视频理解中的视觉 token 选择形式化为一个自回归凝视（gazing）问题。给定一段 $T$ 帧视频 $\boldsymbol{X}^{1:T}$，AutoGaze 将其映射为每帧选中补丁的索引序列：

$$ \mathtt{AutoGaze:} X^{1:T} \to p_{1:N^1}^1, \dots, p_{1:N^T}^T $$

其中 $N^t$ 为第 $t$ 帧的凝视长度（即选中补丁数量）。凝视的目标是在给定凝视长度下，使原始视频与仅从选中补丁重建的视频之间的重建损失最小：

$$ \min_{p_1^1,\ldots,p_{N^T}^T} L(\boldsymbol{X}^{1:T}, \mathrm{Recon}(\boldsymbol{X}^1[p_1^1],\ldots,\boldsymbol{X}^T[p_{N^T}^T])) $$

这里 $\mathrm{Recon}(\cdot)$ 是一个定制的 VideoMAE 重建模型，采用块因果注意力（block-causal attention），根据所选补丁重建完整视频并计算重建损失。这一形式化的核心洞察在于：视频中存在显著的时空冗余，只需极少量的关键补丁即可在可容忍的损失范围内重建视频，从而大幅减少后续 ViT 和 LLM 需要处理的视觉 token 数量。

### 轻量架构：编码器-解码器设计

AutoGaze 是一个仅 3M 参数的轻量模块，由两个核心组件构成（Figure 3）：

**卷积编码器**负责将视频帧编码为紧凑的时空特征表示。具体实现包含一个空间卷积层（kernel size 16）和一个 3D 卷积层，将原始像素压缩为低维特征，供解码器使用。

**自回归 Transformer 解码器**基于当前帧特征和历史凝视信息，逐步解码当前帧的多尺度补丁索引。在每一步 $k$，解码器根据已选择的补丁序列 $\tilde{p}_{1:k-1}^t$ 和帧上下文预测下一个补丁位置 $p_k^t$。这一自回归设计使凝视过程能够动态适应视频内容，而非一次性做出全部选择。

### 自动停止机制：重建损失预测头

AutoGaze 的一个关键创新是自动决定每帧需要凝视多少补丁。为此，在解码器上附加一个预测头：在解码每个 $p_k^t$ 时，该头预测若仅使用前 $k$ 个补丁重建第 $t$ 帧的重建损失。一旦预测损失低于用户指定的阈值，该帧的凝视过程即自动停止。这使得模型能够根据视频内容的复杂程度自适应地调整凝视比例——简单场景只需少量补丁，复杂场景则凝视更多。

### 多尺度补丁嵌入

与标准 ViT 的单尺度固定网格补丁不同，AutoGaze 支持多尺度补丁选择。具体而言，对每帧按不同尺度进行插值，并相应调整位置嵌入，使 ViT 能够接受混合尺度的 token 序列。这一设计使凝视机制可以用粗粒度补丁覆盖大范围运动区域，用细粒度补丁捕捉局部细节，从而在相同凝视比例下获得更优的重建质量（消融实验表明多尺度凝视将凝视比例降低了 2.3×）。

### 训练管线：NTP 预训练 + GRPO 后训练

AutoGaze 采用两阶段训练策略学习最优凝视策略。

**第一阶段：NTP 预训练。** 首先通过贪心搜索在 250K 视频上收集近似最小化重建损失的凝视序列，然后以这些序列作为监督信号，用下一 token 预测交叉熵损失预训练 AutoGaze：

$$ \boldsymbol{L}_{NTP} = -\sum_{t=1}^T\sum_{k=1}^{N^t} \log \pi_{\boldsymbol{\theta}}(\tilde{p}_k^t \mid \boldsymbol{X}^{1:t}, \tilde{p}_{1:N^1}^1,\dots,\tilde{p}_{1:k-1}^t) $$

其中 $\pi_{\boldsymbol{\theta}}$ 为 AutoGaze 策略，$\tilde{p}$ 为贪心搜索得到的参考凝视序列。

**第二阶段：GRPO 强化学习后训练。** 预训练策略仅模仿贪心搜索的结果，但贪心搜索本身并非全局最优。为此，使用简化的 GRPO（Group Relative Policy Optimization）算法以重建奖励为优势函数进行后训练，使策略能够探索并发现重建损失更低的凝视序列：

$$ \mathcal{L}_{GRPO} = -\sum_{t=1}^T\sum_{k=1}^{N^t} \frac{\pi_\theta(p_k^t)}{\pi_{\theta_{detached}}(p_k^t)} \mathcal{A}_k^t $$

消融实验证实两个阶段缺一不可：完整管线达到凝视比例 0.094，仅预训练为 0.102，仅后训练为 0.209，随机选择则为 0.263（Table 3）。

### 下游使用：时空分块处理

为使 AutoGaze 能够处理任意分辨率和时长的视频，推理时将视频分割为 $16 \times 224 \times 224$ 的时空块（tile），在每个块上独立运行 AutoGaze，最后将各块的凝视位置合并。这一分块策略保证了 AutoGaze 的计算开销与视频规模呈线性关系，且不受单块 GPU 内存限制。

## 实验与关键发现

### 1. 与SOTA MLLM的综合性能对比

AutoGaze以**NVILA-8B-Video**为基础MLLM，在通用、长视频和高分辨率视频基准上与当前SOTA进行了系统比较（Table 1）。核心发现是：AutoGaze使同一基础模型能够扩展到**1K帧、4K分辨率**的视频输入，而此前方法受限于ViT的计算瓶颈无法实现这种扩展。

![[assets/figures/papers/paper_list_l837_https_arxiv_org_abs_2603_12254/figures/010_Table_1.jpg]]
*Table 1: Comparison to state-of-the-art MLLMs. NVILA-8B-Video with AutoGaze is scaled to 1K-frame, 4K-resolution videos, achieving competitive performance on general and long video benchmarks and state-of-the-art result on HLVid*

在通用视频理解基准**VideoMME**上，启用AutoGaze的NVILA-8B-Video取得67.0%（w/o sub）和71.8%（w/ sub），较未使用AutoGaze的基础模型分别提升+2.8和+1.8个百分点，并超越了开源SOTA **Qwen2.5-VL-7B**（63.3%/69.0%）和商业闭源模型**GPT-4o**（71.9%/77.2%，但其参数量和训练数据远大于8B规模）。在长视频基准**LongVideoBench**上，AutoGaze版本达到61.0%，较基线提升+3.3个百分点。

最显著的性能跃升出现在本文提出的长时高分辨率基准**HLVid**上：基础NVILA-8B-Video仅取得42.5%，而启用AutoGaze扩展至1K帧4K分辨率后飙升至**52.6%，提升+10.1个百分点**，超越此前最佳MLLM达4.5个百分点。这一结果直接验证了核心主张：AutoGaze通过大幅降低ViT的计算开销，使MLLM能够处理此前无法企及的视频规模和分辨率，从而解锁了显著的性能增益。

### 2. 与Token缩减方法的效率-精度权衡

Table 2将AutoGaze与现有MLLM token缩减方法进行了严格对比，所有方法统一使用**SigLIP2-SO400M**作为ViT、**NVILA-8B-Video**作为LLM，且均选择**6.25%的视觉token**以保证公平性。对比方法包括空间/时间/时空（S-/T-/ST-）维度的prompt-agnostic（PA）和prompt-dependent（PD）剪枝策略，以及**VideoChat-Flash**等领先方法。

关键发现：AutoGaze是**唯一同时加速ViT和LLM**的方法。在128帧视频上，AutoGaze将ViT延迟从2.20s降至**0.55s（4×加速）**，LLM延迟从1.42s降至**0.10s（14.2×加速）**。相比之下，所有其他token缩减方法仅在LLM端剪枝，ViT延迟保持不变（仍为2.20s），因为ViT仍需处理全部视频帧。这表明AutoGaze填补了现有方法的盲区——**在ViT之前消除冗余**，而非仅在LLM端做后处理。

在精度方面，AutoGaze在VideoMME（w/o sub）上达到52.3%，虽略低于使用全部token的基线（53.4%），但显著优于其他token缩减方法（例如VideoChat-Flash的49.1%）。这证明了AutoGaze在极低token比例（6.25%）下仍能保持高信息保真度。

### 3. 训练管线的消融分析

Table 3揭示了AutoGaze两阶段训练的必要性。仅使用**NTP预训练**（从贪心搜索收集的凝视序列学习）可将凝视比例降至0.102；仅使用**RL后训练**（以重建损失为奖励）的凝视比例为0.209；而**完整的NTP+RL管线**将凝视比例进一步压缩至**0.094**。随机凝视基线的比例为0.263，表明AutoGaze学习到的凝视策略比随机选择高效约2.8倍。

这一消融揭示了因果机制：NTP预训练提供了良好的初始策略（模仿近似最优的贪心搜索轨迹），而RL后训练在此基础上通过探索发现更优的凝视序列，进一步降低重建损失。两者缺一不可。

### 4. 模型设计选择的消融

Table 4评估了AutoGaze的关键设计选择：

- **多尺度凝视 vs 单尺度凝视**：多尺度凝视将凝视比例从0.220降至0.094（**2.3×降低**），延迟从0.464s降至0.193s（**2.4×加速**）。这验证了多尺度机制允许模型以粗粒度尺度覆盖大面积静态区域，仅对细节丰富区域使用细粒度尺度，从而大幅减少所需补丁数量。
- **每步解码token数**：解码10个token/步提供最佳的延迟-凝视权衡（0.193s延迟，0.094凝视比例）。解码更少token增加自回归步数从而增加延迟；解码更多token则降低凝视精度。
- **多token预测**：预测多个未来token可略微降低凝视比例（0.094→0.092），但提升有限，表明标准的下一token预测已足够有效。

### 5. 重建损失阈值的可容忍性

Table 5回答了关键工程问题：**多大的重建损失对下游MLLM性能是可接受的？** 实验表明，当重建损失阈值设为**0.7**时，VideoMME精度仅下降不到0.5%，而凝视比例可大幅降低。这为实际部署提供了操作点：用户可根据延迟需求调整阈值，在精度和效率间灵活权衡。

### 6. 扩展能力与效率增益

Figure 9展示了AutoGaze的扩展能力：基础模型在超过256帧时即耗尽内存（OOM），而AutoGaze版本可顺利扩展至1K帧甚至更多。在HLVid上，随着视频token数增加，性能持续提升，验证了AutoGaze使MLLM首次能够从长时高分辨率视频中有效提取信息。

Figure 8量化了效率增益：对于30FPS、4K视频，AutoGaze仅需约**1%的补丁**即可达到重建损失0.7，ViT加速最高达**19×**，MLLM加速最高达**10×**。延迟随FPS和分辨率呈亚线性增长，而基线呈线性甚至超线性增长，凸显了AutoGaze在处理高信息密度视频时的优势。

### 7. 凝视行为的可解释性分析

Figure 4和Figure 5对AutoGaze学到的凝视策略进行了统计分析：

- **运动感知**：AutoGaze更频繁地选择具有高光流的补丁（Figure 4），且使用更粗的尺度来覆盖高运动区域，说明模型学会了用粗粒度尺度捕获运动信息。
- **细节感知**：更精细的尺度与补丁细节度（以拉普拉斯方差度量）呈正相关（ρ=0.12，p<0.001；Figure 5），表明模型在细节丰富区域自动切换到细粒度凝视。

这些涌现行为并非显式编程，而是通过最小化重建损失自然习得的，体现了AutoGaze对视频时空冗余的有效利用。

### 8. 局限性与失败模式

尽管AutoGaze在效率和扩展性上表现突出，但存在两个已知局限：

1. **相机平移运动盲区**：当场景整体平移时，AutoGaze继续选择补丁，但无法识别平移后的区域与先前帧存在大量像素重叠（仅发生位移）。这导致选择的补丁集合包含冗余信息，凝视效率未达理论最优。该问题需要引入运动补偿或全局运动估计来解决。
2. **缺乏物理直觉**：VideoMAE重建模型是因果的但未注入物理知识，无法根据物体的物理运动规律（如抛物轨迹）预测未来帧的合理外观。这限制了凝视决策的前瞻性——模型仅基于当前和过去帧的重建损失做决策，无法预判哪些区域即将变得重要。

这些局限性提示未来工作方向：将运动模型或物理先验融入凝视决策，以进一步提升效率和对动态场景的适应性。

![[assets/figures/papers/paper_list_l837_https_arxiv_org_abs_2603_12254/figures/011_Table_3.jpg]]
*Table 3: Ablation on AutoGaze training pipeline. Both NTP pre-training and RL post-training helps with the performance*

![[assets/figures/papers/paper_list_l837_https_arxiv_org_abs_2603_12254/figures/013_Table_4.jpg]]
*Table 4: Ablations of AutoGaze model designs*

![[assets/figures/papers/paper_list_l837_https_arxiv_org_abs_2603_12254/figures/008_Figure_8.jpg]]
*Figure 8: Efficiency gain on ViTs and MLLMs with AutoGaze. We benchmark the ViT and MLLM latency of encoding one second of video with varying FPS and resolution. AutoGaze can select different numbers of patches to vary latency depending on user needs. When using the gazing ratio required for a reconstruction loss of 0.7, AutoGaze reduces the ViT and MLLM latency by up to 19× and 10×*

## 定位与知识库关联

### 核心问题定位：视觉Token冗余是视频MLLM扩展的真正瓶颈

现有视频多模态大语言模型（MLLM）面临一个被长期忽视的计算瓶颈：**视觉Transformer（ViT）对完整视频帧的全量处理**。此前的主流token缩减方法——如**VideoChat-Flash**等——仅在LLM端进行token剪枝，ViT仍需处理所有像素，导致ViT的计算开销成为限制视频MLLM向长视频、高分辨率扩展的真正障碍。AutoGaze的核心洞察在于：**在ViT之前**就通过自回归凝视机制选择最小化的多尺度补丁集合，从而直接控制输入ViT的视觉token数量，从根源上消除冗余。

### 方法谱系中的位置

AutoGaze处于**视觉前端token选择**这一新兴技术路线，与现有方法形成以下对比关系：

| 方法类别 | 代表工作 | Token缩减位置 | ViT是否加速 | 选择策略 |
|---------|---------|-------------|-----------|---------|
| LLM端剪枝 | VideoChat-Flash等 | LLM输入侧 | 否 | 启发式/可学习 |
| 视觉前端选择 | **AutoGaze** | ViT输入前 | 是（最高19×） | 自回归+重建引导+RL |
| 启发式凝视 | Random Gaze, Optical-Flow Gaze | ViT输入前 | 是 | 随机/光流启发式 |

AutoGaze与启发式凝视基线（Random Gaze、Optical-Flow Gaze）的关键区别在于：AutoGaze通过**重建损失引导的自回归选择**学习最优凝视策略，而非依赖手工设计的启发式规则。实验表明，AutoGaze在达到重建损失1.0时仅需5%的补丁，而Random Gaze需要15%，效率提升达3倍。

### 适用边界

**有效场景：**
- 长视频理解（至1K帧）：AutoGaze使MLLM能够处理远超基线内存上限的帧数，基线在256帧后即耗尽内存，而AutoGaze可扩展至1K帧
- 高分辨率视频（至4K）：通过多尺度补丁选择，仅需约1%的补丁即可在30-FPS、4K视频上达到重建损失0.7
- 通用视频基准：在VideoMME、LongVideoBench等基准上保持竞争力，同时在HLVid长高分辨率基准上取得10.1%的显著提升

**已知局限：**
1. **相机平移运动未建模**：当场景整体平移时，AutoGaze会继续选择补丁但无法识别平移后的区域与之前帧存在重复，导致选择的补丁并非最优。这需要手动验证是否在特定场景（如无人机航拍、监控视频平移）下性能退化。
2. **缺乏物理直觉**：VideoMAE重建模型是因果的但未训练物理知识，无法根据物体的物理运动（如抛物线轨迹）预测未来帧的合理外观，限制了凝视决策的前瞻性。
3. **OOD泛化**：AutoGaze在分布外视频（CCTV、机器人抓取演示、物体交换视频）上表现出鲁棒跟踪能力（Figure 6），但这一结论基于定性展示，缺乏大规模OOD基准的定量验证。

### 知识库定位：与相关工作的关系

**与MLLM Token缩减方法的区别：**
AutoGaze与现有的空间/时间/时空token缩减方法（Table 2）的核心区别在于**作用位置**：前者在ViT之前操作，后者在LLM端操作。这导致AutoGaze同时加速ViT和LLM（ViT延迟降低4×，LLM延迟降低14.2×），而LLM端方法仅加速LLM，ViT延迟不变。在相同6.25%视觉token选择比例下，AutoGaze的ViT延迟为0.55s，而其他方法仍需2.20s。

**与可学习凝视/注意力机制的关联：**
AutoGaze的自回归凝视机制与视觉注意力中的可学习稀疏注意力（如deformable attention）有概念上的亲缘性，但AutoGaze将选择过程外置为独立的轻量模块（3M参数），不修改ViT内部结构，使其可与任意预训练ViT和MLLM即插即用。

**训练范式的贡献：**
AutoGaze采用**下一token预测（NTP）预训练 + 强化学习（RL）后训练**的两阶段策略学习凝视策略。消融实验（Table 3）表明两者缺一不可：完整管线达到凝视比例0.094，仅预训练为0.102，仅后训练为0.209，随机基线为0.263。RL后训练使模型学会自动决定何时停止凝视——当预测重建损失低于用户指定阈值时停止，这一机制为凝视策略提供了可调节的效率-精度权衡。

### 开放问题

1. **物理建模的集成**：如何将物理先验（物体运动规律、遮挡推理）融入VideoMAE重建模型，使凝视决策具备前瞻性？
2. **相机运动补偿**：能否在AutoGaze中引入全局运动估计模块，识别并补偿相机平移，避免重复选择平移后的冗余区域？
3. **OOD鲁棒性的量化**：当前OOD分析仅为定性展示，需要在标准OOD视频基准上进行系统评估。
4. **凝视策略的可解释性**：虽然Figure 4和Figure 5揭示了AutoGaze偏好高光流区域和细节丰富区域，但凝视决策的因果机制仍需更深入的分析。

## 原文 PDF

![[paperPDFs/CVPR_2026/Attend_Before_Attention_Efficient_and_Scalable_Video_Understanding_via_Autoregressive_Gazing.pdf]]
