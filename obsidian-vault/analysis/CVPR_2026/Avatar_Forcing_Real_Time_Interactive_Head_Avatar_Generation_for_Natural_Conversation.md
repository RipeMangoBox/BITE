---
title: "Avatar Forcing: Real-Time Interactive Head Avatar Generation for Natural Conversation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Avatar_Forcing_Real_Time_Interactive_Head_Avatar_Generation_for_Natural_Conversation.pdf
project_link: "https://taekyungki.github.io/AvatarForcing"
code_link: null
aliases:
- AF
- AFRTIHAGNC
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 核心因果开关是：（1）用因果扩散强制（causal diffusion forcing）取代双向生成，通过块级前瞻注意力掩码和滑动 KV 缓存实现逐块实时推理；（2）利用直接偏好优化（DPO）构造合成弱偏好样本（仅依赖化身音频的说话模型生成的动作），在无人工标注的情况下强化互动动作的表现力。
primary_logic: 将交互式头像生成视为运动潜在空间中的因果序列建模问题，并借助偏好优化对齐用户信号与化身反应，是同时实现低延迟实时响应与自然、生动交互的关键。
claims:
- Avatar Forcing 在 RealTalk 上实现约 0.5s 的用户输入延迟，比 INFP*（3.4s）快约 6.8 倍，满足实时交互要求。
- 人类偏好研究中，Avatar Forcing 在整体偏好上超过 80% 的支持率，显著优于 INFP*。
- 消融实验表明，加入用户运动并配合 DPO 微调后，反应性指标 rPCC‑Exp 从 0.042 降至 0.003，运动丰富度 SID 从 2.236 升至 2.442，且视觉效果和唇音同步保持竞争力。
- RealTalk 上 User Input Latency (s) ↓ = 0.5
---

# Avatar Forcing: Real-Time Interactive Head Avatar Generation for Natural Conversation

> [!tip] 核心洞察
> 将交互式头像生成视为运动潜在空间中的因果序列建模问题，并借助偏好优化对齐用户信号与化身反应，是同时实现低延迟实时响应与自然、生动交互的关键。

| 字段 | 内容 |
|------|------|
| 中文题名 | Avatar Forcing：面向自然对话的实时交互式头部化身生成 |
| 英文题名 | Avatar Forcing: Real-Time Interactive Head Avatar Generation for Natural Conversation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2601.00664) · [Project](https://taekyungki.github.io/AvatarForcing) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Avatar Forcing |
| Dataset | RealTalk, HDTF, ViCo, Human Preference |

> [!tip] 效果简介
> - RealTalk 上，User Input Latency (s) ↓ 0.5 vs 3.4 (INFP*) (-2.9)；rPCC-Exp ↓ (反应性) 0.003 vs 0.035 (INFP*) (-0.032)；SID ↑ (运动丰富度) 2.442 vs 2.343 (INFP*) (+0.099)。
> - HDTF 上，FID ↓ (图像质量) 20.332 vs 25.110 (FLOAT) (-4.778)。
> - ViCo 上，FD-Exp ↓ (表情分布距离) 16.64 vs 17.52 (INFP*) (-0.88)。

## 概要

交互式头部化身生成旨在根据用户的语音、面部动作等实时输入，驱动一个虚拟化身进行自然的对话回应。然而，现有方法面临两个核心瓶颈：**实时性不足**与**动作表现力低下**。一方面，以 INFP 为代表的双向模型需要完整的对话上下文才能生成化身动作，导致用户输入延迟高达 3.4 秒，无法满足真实对话场景的实时交互需求。另一方面，现有倾听数据集中化身动作的表现力较弱，模型学到的倾听行为往往被动、僵硬，缺乏主动的非语言互动。

针对上述问题，本文提出 **Avatar Forcing**，一种面向自然对话的实时交互式头部化身生成框架。其核心思路是将交互式化身生成建模为运动潜在空间中的因果序列建模问题，并通过两个关键设计实现低延迟实时响应与自然生动的交互：

1. **因果扩散强制（Causal Diffusion Forcing）**：用块级前瞻注意力掩码和滑动窗口 KV 缓存取代双向生成，使模型能够逐块因果推理，在保证块间平滑过渡的同时将用户输入延迟降至约 0.5 秒，相比 INFP* 加速约 6.8 倍。
2. **无接触标注的直接偏好优化（DPO）**：利用仅依赖化身音频的说话模型生成弱偏好样本，构造“真实动作 vs. 弱动作”的偏序对进行微调，在无需人工标注的条件下显著增强化身动作的反应性与表现力。

在 RealTalk 数据集上，Avatar Forcing 的用户输入延迟为 0.5 秒，反应性指标 rPCC‑Exp 降至 0.003，运动丰富度 SID 提升至 2.442。人类偏好研究中，该方法以超过 80% 的整体支持率显著优于 INFP*。消融实验进一步验证了用户运动输入和 DPO 微调对实时反应性与动作表现力的关键作用。

### 交互式头像生成的实时性瓶颈

实时交互式头像生成（Interactive Head Avatar Generation）旨在根据用户的多模态信号（音频、面部动作等）实时驱动虚拟化身的表情与头部运动，以支持自然对话场景。这一任务的核心挑战在于：化身不仅需要在自身说话时产生唇音同步的说话动作，更需要在倾听用户发言时，根据用户的非语言信号做出即时、自然的反应——如点头、微笑、挑眉等。

现有方法中，最具代表性的交互式生成模型是 **INFP**（基于双向 Transformer 的同时说话与倾听动作生成框架）。INFP 将交互对话建模为一个完整的时序窗口，通过双向注意力机制同时考虑过去和未来的上下文来生成化身动作。这一设计虽然保证了生成质量，却引入了根本性的实时性障碍：双向模型必须等待完整的对话上下文（包括未来帧）才能开始推理，导致用户输入延迟高达 **3.4 秒**（Table 1），远远无法满足实时对话对亚秒级响应的需求。

### 倾听动作的表现力缺失

除延迟问题外，现有方法的另一个关键缺陷在于倾听行为的表现力不足。在典型的对话数据集中（如 ViCo），倾听者的面部表情方差显著低于说话者（Figure 5），这意味着模型从数据中学到的倾听行为天然偏向被动和僵硬——化身往往只是保持静态的中性表情，缺乏主动的非语言互动信号（如微笑回应、惊讶挑眉等）。

这种表现力缺失的根源在于数据分布本身的偏差，而非模型架构的固有问题。然而，现有方法（包括 INFP、FLOAT、SadTalker 等）均未针对这一偏差进行专门处理，导致生成的倾听动作缺乏人类对话中常见的互动性和生动感。

### 核心动机：从双向到因果，从被动到主动

上述两大瓶颈——**高延迟的双向推理**与**低表现力的倾听行为**——构成了本文的核心动机。Avatar Forcing 从两个维度同时突破：

1. **因果生成替代双向生成**：将交互式头像生成重新定义为运动潜在空间中的因果序列建模问题。通过块级因果扩散强制（Causal Diffusion Forcing）和滑动窗口 KV 缓存，模型可以逐块预测化身动作，无需等待未来上下文，从而将用户输入延迟压缩至约 **0.5 秒**（约 6.8 倍加速）。

2. **偏好优化增强互动表现**：在无需人工标注的条件下，利用直接偏好优化（DPO）构造合成弱偏好样本——通过仅依赖化身音频的说话模型生成缺乏用户信号响应的动作，将其作为“负样本”与真实动作形成偏序对——从而显式地对齐化身反应与用户信号，大幅提升倾听动作的丰富度和反应性。

这两个技术路径共同指向一个目标：在保证实时响应的前提下，让虚拟化身展现出自然对话中应有的主动性和互动感。

## 核心方法与创新机理

Avatar Forcing 的核心创新在于通过两个“因果开关”同时解决了交互式头部化身生成中长期存在的**实时性**与**表现力**两大瓶颈。

### 瓶颈一：从双向依赖到因果实时推理

现有交互式化身生成方法（如双向 Transformer/DiT 架构）依赖完整的对话上下文进行运动生成，导致高达 3.4 秒的用户输入延迟，无法满足实时交互需求。Avatar Forcing 将问题重新定义为运动潜在空间中的**因果序列建模**，提出**因果扩散强制 Transformer（DFoT）**，其关键设计包括：

- **块级前瞻注意力掩码**：允许当前块关注有限数量的未来帧，在保持块间平滑过渡的同时，使模型无需等待完整未来上下文即可开始生成。
- **滑动窗口因果编码与 KV 缓存**：通过滑动窗口注意力沿时间轴进行时序平滑条件建模，并利用键值缓存高效复用历史信息，实现逐块实时推理。

这一架构转变将用户输入延迟从 INFP* 的 3.4 秒降至约 0.5 秒（Table 1），加速约 6.8 倍，首次实现了真正意义上的实时交互式化身生成。

### 瓶颈二：从被动倾听到主动互动

倾听数据集中动作表现力低下（Figure 5 展示了 ViCo 数据集中倾听者表情方差远低于说话者），导致模型学到的倾听行为被动、僵硬。Avatar Forcing 通过**无接触标注的直接偏好优化（DPO）** 解决此问题：

- **弱偏好样本合成**：利用仅依赖化身音频的说话模型生成“弱表现力”动作潜在向量，作为负样本。
- **偏好对构建**：将真实动作作为正样本，合成弱动作作为负样本，构造 (真实动作, 弱动作) 偏序对。
- **DPO 微调**：在扩散强制框架中引入 DPO 损失，与扩散强制损失加权组合（λ=0.1），强化化身对用户信号的主动响应能力。

消融实验（Table 5, Table 6）证实：加入用户运动输入后，反应性指标 rPCC-Exp 从 0.042 降至 0.003，运动丰富度 SID 从 2.236 升至 2.442；进一步配合 DPO 微调后，视觉质量指标（FID, FVD）同步提升，且人类偏好研究中整体偏好率超过 80%（Table 2）。

Avatar Forcing 的整体 pipeline 将交互式头像生成建模为**运动潜在空间中的因果序列生成问题**，其核心由四个模块串联构成，形成端到端的实时视频生成流。

### 输入输出流

系统接收四路输入信号：
- **用户视频帧**：提供用户的头部运动与表情信息
- **用户音频**：提供用户的语音信号
- **化身音频**：驱动化身说话动作的音频
- **化身参考图像**：提供化身的身份外观

输出为实时生成的化身视频帧，该视频在说话与倾听之间自然切换，并能对用户的非语言信号（如微笑）产生即时反应。

### 四大核心模块

**1. Motion Latent Auto-encoder（运动潜在自编码器）**
将输入图像编码为身份‑运动解耦的潜在向量 $z = z_S + m_S$，其中 $z_S$ 为身份成分，$m_S$ 为运动成分。该分解使得后续生成仅需操控低维运动潜在 $m_S$，大幅压缩了生成空间（Fig. 9）。

**2. Dual Motion Encoder（双路运动编码器）**
通过交叉注意力机制融合用户音频特征、用户运动潜在 $m_u$ 和化身音频特征，生成统一的条件表示 $c^i$。该模块将多模态用户信号与化身音频整合为生成器可消费的紧凑条件（Fig. 2, Fig. 3）。

![[assets/figures/papers/paper_list_l975_https_arxiv_org_abs_2601_00664/figures/002_Figure_2.jpg]]
*Figure 2: Overall architecture of Avatar Forcing. We encode the use motion and audio, as well as avatar audio into a unified condition by Dual Motion Encoder. Causal Motion Generator infer the motion latent block of the avatar, which are then decoded into an avatar video*

**3. Causal DFoT Motion Generator（因果扩散强制运动生成器）**
这是 pipeline 的核心生成引擎。它基于 **Diffusion Forcing Transformer（DFoT）**，采用块级前瞻因果注意力掩码（Eq. (5)）和滑动窗口 KV 缓存，以自回归方式逐块预测化身运动潜在块 $\mathbf{m}^i$：

$$p_{\theta}(\mathbf{m}^{1:N}) = \prod_{i=1}^{N} p_{\theta}(\mathbf{m}^{i} \mid \mathbf{m}^{<i}, \mathbf{c}^{\leq i})$$

其中 $c^i$ 为第 $i$ 块的条件三元组。因果结构使得推理时无需等待完整未来上下文，仅依赖已生成的历史信息即可实时产出下一块运动（Fig. 4）。

**4. Latent-to-Frame Decoder（潜在到帧解码器）**
将预测的运动潜在 $\mathbf{m}^i$ 与身份潜在 $z_S$ 组合，解码为最终的化身视频帧，完成从潜在空间到像素空间的映射。

### 因果推理与实时性保证

区别于 INFP 等双向模型需要访问完整时序窗口（引入高达 3.4s 延迟），Avatar Forcing 的块级因果 DFoT 在推理时通过 **KV 缓存** 复用历史帧的键值对，仅对当前块执行前向计算。结合 5 块划分策略（Tab. 7），用户输入延迟降至约 **0.5s**，实现了约 6.8 倍的加速，满足实时交互需求。

### 表现力增强的偏好优化回路

在基础扩散强制训练之外，pipeline 引入了一个**无需人工标注的 DPO 微调回路**（Sec. 4.2）：利用仅受化身音频驱动的说话模型生成“弱偏好”运动样本（缺乏用户信号引导，动作被动），将其与真实运动构成偏序对 $(\mathbf{m}^w, \mathbf{m}^l)$，通过联合损失 $\mathcal{L}_{ft}(\theta) = \mathcal{L}_{DF}(\theta) + \lambda \mathcal{L}_{DPO}(\theta)$ 微调生成器。该回路显著增强了化身对用户动作的反应性和运动丰富度（Fig. 8）。

Avatar Forcing 的推理管线由四个关键模块串联构成，其核心创新在于将交互式头像生成重新定义为运动潜在空间中的因果序列建模问题。

### 运动潜在自编码器（Motion Latent Auto-encoder）

该模块将输入图像 $S$ 编码为身份与运动可解耦的潜在向量。具体地，图像潜在 $z$ 被分解为身份成分 $z_S$ 和运动成分 $\mathbf{m}_S$：

$$z = z_S + \mathbf{m}_S$$

其中身份潜在 $z_S$ 在推理时固定，运动潜在 $\mathbf{m}_S$ 捕捉头部姿态、表情、唇动等动态信息。这种显式分解使得后续的因果生成器只需在低维运动空间（$d=512$）中操作，大幅降低了计算开销，是实现实时推理的基础。

### 双模态运动编码器（Dual Motion Encoder）

该编码器通过交叉注意力机制融合三类条件信号：用户音频、用户运动潜在 $\mathbf{m}_u$、以及化身音频，输出统一的条件表示 $\mathbf{c}^i$。其中 $\mathbf{m}_u$ 由同一运动潜在自编码器从用户视频帧中提取。用户运动信号的引入是化身能够实时镜像用户表情（如微笑、专注）的关键因果输入。

### 因果扩散强制运动生成器（Causal DFoT Motion Generator）

这是 Avatar Forcing 的核心推理引擎。与 INFP 等基线采用的双向 Transformer（需完整时序上下文，延迟高达 3.4 秒）不同，本模块基于扩散强制（Diffusion Forcing）框架，采用块级因果结构进行逐块自回归生成。

**自回归生成范式**：运动潜在块 $\mathbf{m}^i$ 的生成条件为过去运动轨迹 $\mathbf{m}^{<i}$ 和当前条件 $\mathbf{c}^{\leq i}$：

$$p_{\theta}(\mathbf{m}^{1:N}) = \prod_{i=1}^{N} p_{\theta}(\mathbf{m}^i \mid \mathbf{m}^{<i}, \mathbf{c}^{\leq i})$$

**块级前瞻注意力掩码**：为保证块间平滑过渡，注意力掩码允许当前块关注有限数量的未来帧（前瞻窗口 $l$）：

$$M_{i,j} = 1 \quad \text{if} \quad \lfloor j / B \rfloor \le \lfloor i / B \rfloor + l \quad \text{else} \quad 0$$

其中 $B$ 为块大小。配合滑动窗口因果编码和 KV 缓存机制，模型在推理时无需重新计算历史帧的键值对，实现了约 0.5 秒的用户输入延迟。

**训练目标**：在运动潜在空间中回归向量场 $v_{\theta}$ 到目标差异 $\mathbf{m}_1^n - \mathbf{m}_0^n$：

$$\mathcal{L}_{DF}(\theta) = \mathbb{E}_{n, t_n, \mathbf{m}_{t_n}^n} \left\| v_{\theta}(\mathbf{m}_{t_n}^n, t_n, \mathbf{c}^n) - (\mathbf{m}_1^n - \mathbf{m}_0^n) \right\|$$

### 潜在到帧解码器（Latent-to-Frame Decoder）

将生成的运动潜在 $\mathbf{m}_S$ 与固定的身份潜在 $z_S$ 相加后，解码为最终视频帧。

### 表现力增强：无接触 DPO 微调

针对倾听数据集中动作表现力低下的瓶颈，Avatar Forcing 引入直接偏好优化（DPO）进行微调，无需人工标注。其核心技巧是：利用仅受化身音频驱动的说话模型（即丢弃用户信号）生成弱表现力的运动潜在 $\mathbf{m}^l$，与真实运动 $\mathbf{m}^w$ 构成偏好对。微调采用混合损失：

$$\mathcal{L}_{ft}(\theta) = \mathcal{L}_{DF}(\theta) + \lambda \mathcal{L}_{DPO}(\theta)$$

其中 $\lambda = 0.1$，DPO 损失适配到扩散强制框架后，通过比较向量场回归误差来对齐偏好：

$$\mathcal{L}_{DPO}(\theta) = -\mathbb{E}_{n, t_n, \mathbf{c}^n, (\mathbf{m}^{w,n}, \mathbf{m}^{l,n})} \log \sigma \Big( -\beta \big[ \| v_{t_n}^{w,n} - v_{\theta}(\mathbf{m}_{t_n}^{w,n}, t_n, \mathbf{c}^n) \| - \| v_{t_n}^{w,n} - v_{\mathrm{ref}}(\mathbf{m}_{t_n}^{w,n}, t_n, \mathbf{c}^n) \| - ( \| v_{t_n}^{l,n} - v_{\theta}(\mathbf{m}_{t_n}^{l,n}, t_n, \mathbf{c}^n) \| - \| v_{t_n}^{l,n} - v_{\mathrm{ref}}(\mathbf{m}_{t_n}^{l,n}, t_n, \mathbf{c}^n) \| ) \big] \Big)$$

消融实验证实，DPO 微调使反应性指标 rPCC‑Exp 从 0.042 降至 0.003，运动丰富度 SID 从 2.236 提升至 2.442，同时视觉质量指标同步改善。

![[assets/figures/papers/paper_list_l975_https_arxiv_org_abs_2601_00664/figures/004_Figure_4.jpg]]
*Figure 4: Architectural comparison between bidirectional and causal structure. (a) Bidirectional DiT used in INFP [70] requires access to the entire temporal window for motion generation. (b) Our blockwise causal DFoT predicts the next block without using future context and supports KV caching*

## 实验与关键发现

### 核心定量结果

Avatar Forcing 在交互式头像生成任务上实现了实时响应与表现力的双重突破。在 RealTalk 数据集上，系统将用户输入延迟压缩至 **0.5 s**，仅为复现版 INFP\*（3.4 s）的约 1/7，满足实时交互要求（Table 1）。与此同时，反应性指标 **rPCC‑Exp** 从 INFP\* 的 0.035 降至 **0.003**，运动丰富度 **SID** 从 2.343 提升至 **2.442**，表明化身能够更敏锐地跟随用户表情变化并产生更丰富的非语言动作。

![[assets/figures/papers/paper_list_l975_https_arxiv_org_abs_2601_00664/figures/006_Table_1.jpg]]
*Table 1: Quantitative comparison results on RealTalk [17]. Best results highlighted in bold. ∗ denotes the reproduced version that is publicly unavailable. We also report the results from a non-interactive talking head model [28], shown in gray, for reference*

人类偏好研究进一步验证了上述量化优势：在整体偏好评估中，Avatar Forcing 获得 **超过 80%** 的支持率，显著优于 INFP\*（Table 2）。这一结果说明，低延迟与高表现力的结合在主观体验层面具有压倒性优势。

![[assets/figures/papers/paper_list_l975_https_arxiv_org_abs_2601_00664/figures/007_Table_2.jpg]]
*Table 2: Human preference study on interactive avatar generation models, comparing Avatar Forcing and INFP∗*

在传统说话头生成任务（HDTF 数据集）上，Avatar Forcing 同样展现出竞争力。其 FID 达到 **20.332**，优于 FLOAT 的 25.110，且 CSIM 保持 0.783 的高水平，证明因果生成架构并未牺牲身份保持能力（Table 3）。在倾听头像生成任务（ViCo 数据集）上，Avatar Forcing 的表情分布距离 **FD‑Exp** 为 **16.64**，低于 INFP\* 的 17.52，表明生成的表情更接近真实倾听者的表现力分布（Table 4）。

### 消融分析：因果架构与偏好优化的协同效应

消融实验揭示了 Avatar Forcing 中两个核心设计——用户运动输入与 DPO 微调——的独立贡献与协同效应。

**用户运动输入的关键性。** 移除用户运动输入后，模型退化为仅依赖音频的单向生成，反应性指标急剧恶化：rPCC‑Exp 从 0.003 飙升至 **0.042–0.052**，运动丰富度 SID 从 2.442 降至 **2.165–2.236**（Table 5）。视觉对比（Figure 7）直观展示了这一退化：当用户微笑时，无用户运动输入的化身保持静止，而完整模型则在用户微笑后产生相应的微笑反应，并在用户开始说话时切换为专注表情。

**DPO 微调的增强作用。** 在保留用户运动输入的基础上，加入 DPO 微调进一步将 rPCC‑Exp 从 0.042 降至 **0.003**，SID 从 2.236 提升至 **2.442**（Table 5）。值得注意的是，DPO 微调不仅改善了反应性和运动丰富度，还同步提升了视觉质量指标：FID 和 FVD 均有所下降（Table 6）。这表明通过合成弱偏好样本（仅依赖化身音频的说话模型生成的动作）进行偏好优化，能够在不依赖人工标注的前提下，有效对齐化身动作与用户信号，同时避免视觉质量的退化。

**块大小选举。** 运动块大小的消融实验（Table 7）表明，**5 个块**的设置（即 Avatar Forcing 的默认配置）在延迟与各项指标之间取得了最佳平衡：延迟为 0.5 s，rPCC‑Exp 为 0.003，FVD 为 170.87。更小的块数会降低反应性，更大的块数则增加延迟且性能提升有限。

### 失败模式与局限性

尽管 Avatar Forcing 在实时交互式头像生成上取得了显著进展，仍存在以下局限：

1. **肢体线索缺失。** 系统仅通过头部运动潜在空间建模交互对话，缺少对手势等肢体线索的支持。在自然对话中，手势是重要的非语言交流通道，当前模型无法捕捉或生成这类信号，限制了更丰富多模态交流的实现。

2. **曝光偏差未完全解决。** 虽然扩散强制对长时生成较为鲁棒（Figure 11 展示了其相对于自回归扩散的优势），但仍未完全消除曝光偏差问题。在极长序列生成场景下，误差累积可能导致动作逐渐偏离真实分布。这一问题需要进一步的理论或架构创新来解决。

3. **非语言信号的可控性有限。** 当前模型对特定非语言信号的显式可控性不足。例如，眼动注视方向、情绪强调程度等场景需要额外的控制信号，而现有框架缺乏对应的条件接口。如何在保持实时性的前提下引入细粒度控制，是一个开放挑战。

### 重要图表结论速览

- **Figure 4：** 双向 DiT（INFP 所用）与块级因果 DFoT 的架构对比。双向结构需访问完整时序窗口，导致高延迟；DFoT 通过块级前瞻注意力掩码和 KV 缓存实现逐块因果推理，是实时性的结构基础。
- **Figure 5：** ViCo 数据集中说话者与倾听者表情表达力的方差对比。倾听者的表情方差显著低于说话者，揭示了现有数据集中倾听动作表现力低下的瓶颈，直接支撑了 DPO 增强表现力的设计动机。
- **Figure 6：** 与 INFP\* 的定性对比。Avatar Forcing 生成的化身在用户微笑后产生更及时的表情反应（红色箭头），且在倾听状态下保持更丰富的微表情（红色方框）。
- **Figure 11：** 自回归扩散与扩散强制的长时生成对比。自回归扩散在长序列中出现明显的运动漂移（红色箭头），而扩散强制保持稳定的运动生成，验证了扩散强制框架对长时一致性的优势。

![[assets/figures/papers/paper_list_l975_https_arxiv_org_abs_2601_00664/figures/005_Figure_5.jpg]]
*Figure 5: Variance visualization of the L2-norm of 3DMM expressions [16] for the speaker and listener on ViCo [68] dataset. Higher variance indicates higher expressiveness*

![[assets/figures/papers/paper_list_l975_https_arxiv_org_abs_2601_00664/figures/012_Table_5.jpg]]
*Table 5: Ablation study on user motion and preference optimization*

## 定位与知识库关联

### 问题定位与核心瓶颈

交互式头部化身生成处于**说话头生成**、**倾听头像生成**与**双人对话动作生成**三个领域的交叉点。现有工作面临两大瓶颈：

1. **实时性瓶颈**：以 INFP 为代表的双向交互模型依赖完整对话上下文进行运动生成，其双向 Transformer（DiT）架构需要访问整个时序窗口，导致用户输入延迟高达 3.4 秒，无法满足实时对话需求（Fig. 4a, Table 1）。
2. **表现力瓶颈**：现有倾听数据集（如 ViCo）中，倾听者的表情方差远低于说话者（Fig. 5），模型学到的倾听行为被动、僵硬，缺乏主动的非语言互动能力。

Avatar Forcing 的核心洞察是：将交互式头像生成重新定义为**运动潜在空间中的因果序列建模问题**，并借助**偏好优化**对齐用户信号与化身反应，从而同时突破实时性与表现力两大瓶颈。

### 与基线工作的关系

#### 交互式头像生成基线

**INFP\***（复现版本）是本文最直接、最强的对比基线。INFP 采用双向 DiT 架构进行运动生成，需要完整时序上下文，导致约 3.4s 的延迟。Avatar Forcing 通过因果扩散强制 Transformer（DFoT）配合块级前瞻注意力掩码和滑动 KV 缓存，将延迟压缩至约 0.5s，实现约 6.8 倍加速（Table 1）。在反应性指标 rPCC-Exp 上，Avatar Forcing 达到 0.003，显著优于 INFP\* 的 0.035。

#### 非交互式说话头生成基线

- **FLOAT**：非交互式说话头生成模型，在 HDTF 数据集上 FID 为 25.110，Avatar Forcing 达到 20.332（Table 3）。
- **SadTalker**：基于 3DMM 的说话头生成方法，作为传统方法的代表参与对比。
- **Hallo3**：扩散模型实时说话头生成方法，代表扩散模型在该领域的应用。

这些非交互式模型仅依赖化身音频驱动，无法响应用户的非语言信号（表情、头部姿态等），因此在交互场景中天然处于劣势。Table 1 中以灰色标注的 FLOAT 结果仅为参考，不参与直接比较。

#### 倾听头像生成基线

- **RLHG** 和 **L2L**：倾听头像生成方法，在 ViCo 数据集上进行对比。
- **DIM**：双人对话动作生成模型，部分倾听头像生成结果继承自 DIM（Table 4 中以 † 标注）。

Avatar Forcing 在 ViCo 数据集上的 FD-Exp 达到 16.64，优于 INFP\* 的 17.52（Table 4），验证了 DPO 微调对倾听表现力的增强效果。

### 方法谱系中的技术定位

#### 序列建模范式的转变：从双向到因果

Avatar Forcing 的方法论贡献首先体现在**序列建模范式的根本转变**上。INFP 等双向模型可视为“离线”推理模式——必须等待完整对话窗口才能生成动作。Avatar Forcing 引入的因果扩散强制框架（Sec. 4.1）将运动生成转化为自回归过程：

$$
p_{\theta}(\mathbf{m}^{1:N}) = \prod_{i=1}^{N} p_{\theta}(\mathbf{m}^{i} \mid \mathbf{m}^{<i}, \mathbf{c}^{\leq i})
$$

通过块级前瞻注意力掩码（Eq. 5）和滑动窗口因果编码，模型在保证块间平滑过渡的同时，实现了逐块实时推理。Fig. 4 清晰对比了双向 DiT 与块级因果 DFoT 的架构差异：前者需要完整未来上下文，后者仅依赖过去信息并支持 KV 缓存复用。

#### 表现力增强的范式创新：无接触标注的偏好优化

传统方法依赖数据集监督，无法显式调整动作的表现力。Avatar Forcing 提出了一种**零额外标注成本**的偏好优化策略（Sec. 4.2）：利用仅受化身音频驱动的说话模型生成“弱偏好样本”（underexpressive motion latents），构造 (真实动作, 弱动作) 偏序对，通过 DPO 微调强化互动动作的表现力：

$$
\mathcal{L}_{ft}(\theta) = \mathcal{L}_{DF}(\theta) + \lambda \mathcal{L}_{DPO}(\theta)
$$

这一策略的核心巧妙之处在于：弱偏好样本的生成仅需“丢弃用户信号”即可自动合成，无需任何人工标注。消融实验（Table 5, Table 6）证实，DPO 微调使 rPCC-Exp 从 0.042 降至 0.003，运动丰富度 SID 从 2.236 升至 2.442，且视觉质量指标（FID, FVD）同步提升。

### 适用边界与局限

尽管 Avatar Forcing 在实时交互式头部化身生成上取得了显著进展，其适用边界和局限同样值得关注：

1. **模态覆盖范围**：系统仅通过头部运动潜在空间建模交互对话，缺少对手势等肢体线索的支持。在需要丰富多模态交流的场景（如虚拟会议、远程协作）中，单纯的头部动作可能不足以传达完整的非语言信息。

2. **长序列生成的曝光偏差**：虽然扩散强制（diffusion forcing）相比自回归扩散（autoregressive diffusion）在长时生成中更为鲁棒（Fig. 11），但仍未完全解决曝光偏差问题。在极长序列生成中，训练时的教师强制与推理时的自回归采样之间的分布偏移可能导致累积误差。

3. **非语言信号的显式可控性有限**：当前模型对眼动注视、情绪强调等细粒度非语言信号的显式控制能力有限。这些场景需要额外的控制信号输入，而现有框架的条件设计（化身音频、用户音频、用户运动）尚未覆盖此类需求。

4. **数据依赖性**：DPO 微调中弱偏好样本的合成依赖于“仅用化身音频驱动”的说话模型，该模型的生成质量直接影响偏好对的构造质量。若说话模型本身表现力不足，弱偏好样本与真实样本的差异可能不够显著，削弱 DPO 的对齐效果。

### 开放问题

基于上述局限，Avatar Forcing 框架引出了以下开放研究问题：

1. **多模态信号的融合与显式控制**：如何高效融合眼动追踪、情绪追踪等额外用户信号，以提升互动的显式可控性？这需要在 Dual Motion Encoder 中引入新的条件分支，同时保持实时推理的延迟约束。

2. **曝光偏差的根本性解决**：如何在运动潜在空间中彻底克服曝光偏差，实现无限长度的稳定生成？可能的路径包括对抗训练、滚动式训练策略或引入显式的长期一致性约束。

3. **复杂多人对话场景的扩展**：如何在不增加人工标注的条件下，进一步对齐复杂的多人对话互动模式（如多人轮流发言、交叉信号、群体反应等）？当前的 DPO 策略仅针对双人交互设计，扩展到多人场景需要重新定义偏好对的构造逻辑。

4. **偏好优化的理论边界**：DPO 微调中弱偏好样本的合成策略（丢弃用户信号）是否总是产生有效的偏好排序？在用户信号本身较弱或模糊的场景下，这种合成策略可能失效，需要更鲁棒的偏好构造方法。

## 原文 PDF

![[paperPDFs/CVPR_2026/Avatar_Forcing_Real_Time_Interactive_Head_Avatar_Generation_for_Natural_Conversation.pdf]]
