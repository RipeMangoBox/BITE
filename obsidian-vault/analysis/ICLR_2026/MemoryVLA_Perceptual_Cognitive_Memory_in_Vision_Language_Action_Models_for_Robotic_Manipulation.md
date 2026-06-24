---
title: "MemoryVLA: Perceptual-Cognitive Memory in Vision-Language-Action Models for Robotic Manipulation"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/MemoryVLA_Perceptual_Cognitive_Memory_in_Vision_Language_Action_Models_for_Robotic_Manipulation.pdf
openreview_forum_id: 54U3XHf7qq
aliases:
- MemoryVLA
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/vision_models_multimodal
core_operator: "引入感知-认知记忆库（PCMB），通过检索历史、门控融合当前表示、合并相邻冗余，为动作决策提供可追溯的时序上下文。"
primary_logic: "借鉴人类双重记忆理论，将工作记忆与长时记忆解耦为感知流和认知流，使模型既能利用细粒度视觉历史，又能利用高层语义历史进行时序推理。"
claims:
- "在真实世界长时域任务上，MemoryVLA的成功分数达83%，较CogACT大幅提升42%，充分证明记忆单元对时序决策的核心贡献。"
- "同时使用感知记忆和认知记忆（71.9%）显著优于仅使用单一记忆类型的变体（63.5%和64.6%），表明双流记忆存在互补作用。"
- "在仿真与真实场景下，模型成功检索并关注那些仅凭当前观测无法分辨的关键历史帧（如推按钮前后的相同画面），解决了非马尔可夫决策歧义。"
- "在SimplerEnv、LIBERO、Mikasa-Robo等多个基准上，MemoryVLA均超越无记忆的VLA基线（例如在Bridge上比CogACT高14.6个百分点），验证了记忆机制的通用性。"
---

# MemoryVLA: Perceptual-Cognitive Memory in Vision-Language-Action Models for Robotic Manipulation

> [!tip] 核心洞察
> 借鉴人类双重记忆理论，将工作记忆与长时记忆解耦为感知流和认知流，使模型既能利用细粒度视觉历史，又能利用高层语义历史进行时序推理。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | MemoryVLA：面向机器人操作视觉-语言-动作模型的感知-认知记忆 |
| 英文题名 | MemoryVLA: Perceptual-Cognitive Memory in Vision-Language-Action Models for Robotic Manipulation |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=54U3XHf7qq); [Project](https://shihao1895.github.io/MemoryVLA) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal |
| Method | MemoryVLA |
| Dataset | SimplerEnv-Bridge, SimplerEnv-Fractal, LIBERO, Mikasa-Robo |

> [!tip] 效果简介
> - SimplerEnv-Bridge 上，Average Success Rate (%) 为 71.9，对比 57.3 (CogACT-Large)，变化 +14.6。
> - SimplerEnv-Fractal 上，Overall Success Rate (%) 为 72.7，对比 68.1 (CogACT)，变化 +4.6。
> - LIBERO 上，Average Success Rate (%) 为 96.5，对比 93.2 (CogACT)，变化 +3.3。

## 概述

机器人操作任务本质上是非马尔可夫的——许多决策无法仅凭当前观测做出。例如，在“推按钮”任务中，按钮按下前后的画面几乎完全相同（Figure 1a），模型必须记住“是否已经推过”这一历史状态才能决定下一步动作。然而，当前主流的视觉-语言-动作（VLA）模型，如 **CogACT**（Li et al., 2024a）、**π₀**（Black et al., 2024）和 **OpenVLA**（Kim et al., 2024），仅以单帧观测为条件预测动作，完全缺乏对时序上下文的显式建模。这导致它们在长时域、时序依赖任务中频繁失败——这是本文识别的核心瓶颈。

MemoryVLA 的核心洞察来自人类认知的双重记忆理论：工作记忆支撑短期控制，情景记忆保存长期经验（Figure 1b）。据此，MemoryVLA 引入**感知-认知记忆库（Perceptual-Cognitive Memory Bank, PCMB）**，将历史信息解耦为两条互补的记忆流——感知流保留细粒度视觉细节，认知流保留高层语义——使模型能同时利用两类历史线索进行时序推理。

具体而言，MemoryVLA 是一个“认知-记忆-动作”框架：预训练的 7B VLM 将当前 RGB 观测和语言指令编码为感知令牌和认知令牌，构成工作记忆；工作记忆从 PCMB 中检索决策相关的历史条目，通过可学习门控自适应融合当前与历史表示，并在记忆库满时基于余弦相似度合并最冗余的相邻条目以维持紧凑性；最终，记忆增强的令牌条件化一个扩散 Transformer，生成未来多步 7-DoF 动作序列（Figure 2）。

实验验证覆盖 6 个基准、3 种机器人、150+ 任务（Figure 4），关键结果如下：

- **仿真基准**：在 SimplerEnv-Bridge 上，MemoryVLA 平均成功率达 71.9%，较 CogACT 提升 14.6 个百分点（Table 1）；在 LIBERO 五套件上达 96.5%（Table 3）；在专门测试记忆能力的 Mikasa-Robo 上达 41.2%，比 π₀ 高 11.8 个百分点（Table 4）。
- **真实世界**：在 12 个真实机器人任务中，MemoryVLA 在通用任务上成功分数达 85%（+9），在长时域时序任务上达 83%（+26），充分证明记忆单元对时序决策的核心贡献（Table 5）。
- **消融实验**：同时使用感知和认知记忆比仅用单一记忆类型高出 7–8 个百分点，验证双流设计的互补性；门控融合和基于相似度的记忆合并均显著优于简单替代方案（Tables 6–7）。

在方法谱系中，MemoryVLA 区别于仅拼接多帧的 **RoboVLMs**（Liu et al., 2025b）、通过视觉轨迹简化时序但丢弃语义细节的 **TraceVLA**（Zheng et al., 2024b），以及近期引入时序上下文的 **CronusVLA**（Li et al., 2025a），其核心差异在于将记忆解耦为感知与认知双流，并通过检索-门控融合-合并三阶段机制实现结构化、可追溯的时序推理。

## 背景与动机

### 非马尔可夫操作任务的时序决策困境

机器人操作任务本质上是序贯决策过程，但当前主流的视觉-语言-动作（VLA）模型在架构设计上普遍隐含了马尔可夫假设——策略仅基于当前观测帧预测动作序列。这一假设在长时域、时序依赖的任务中暴露出根本性缺陷：当环境状态仅凭当前RGB图像无法唯一确定下一步动作时，模型因缺乏历史上下文而频繁失败。

最具代表性的场景是“推按钮”任务（Push Buttons）：按钮按下前与按下后的视觉画面几乎完全相同，仅凭单帧观测无法判断按钮是否已被按下，因而无法决定是继续按压还是转向下一个按钮（Figure 1a）。更广泛地，任何涉及状态计数、顺序记忆或因果追溯的操作任务——如“清理桌子并计数物品”“猜测物品被放置的位置”“更换食物”等——均要求模型回溯先前步骤中发生的事件，而非仅依赖当前传感器读数（Figure 11, 12）。

### 现有VLA方法的时序建模缺口

当前VLA领域的主流方法在时序上下文利用上存在明显的结构空白：

- **单帧条件型VLA**（如 **OpenVLA** Kim et al., 2024、**CogACT** Li et al., 2024a、**π₀** Black et al., 2024）仅将当前RGB图像和语言指令作为输入，完全不具备显式的时序记忆能力。这些模型在SimplerEnv、LIBERO等标准基准上表现良好，但在需要历史追溯的真实世界长时域任务中成功率骤降（Table 5：CogACT在长时域任务上仅57%，而MemoryVLA达83%）。

- **视频帧间格式方法**（如 **RoboVLMs** Liu et al., 2025b）尝试通过拼接多帧或利用帧间注意力建模时序，但计算代价随帧数线性增长，难以在实时控制中扩展至长历史窗口。

- **视觉轨迹简化方法**（如 **TraceVLA** Zheng et al., 2024b）将历史压缩为视觉轨迹表示，虽降低了计算开销，却丢弃了高层语义细节，削弱了对复杂决策的支持。

- **近期时序上下文VLA**（如 **CronusVLA** Li et al., 2025a）开始引入历史上下文，但在Mikasa-Robo等记忆密集型基准上仍显著落后于MemoryVLA（Table 17c：CronusVLA 18.0% vs MemoryVLA 41.2%），表明其记忆机制的设计尚不充分。

### 人类双重记忆系统的启示

认知神经科学揭示，人类在操作任务中依赖一套双重记忆系统（Figure 1b）：**工作记忆**（working memory）由前额叶神经活动支撑，负责短时程的感觉运动控制；**情景记忆**（episodic memory）由海马体介导，保存长期经验以供回溯。二者协同使人类能够同时利用当前的细粒度感知和过去的高层语义知识进行决策。

这一机制为机器人操作提供了直接的计算启示：一个有效的时序决策系统应当将历史信息解耦为**感知流**（perceptual stream，保留细粒度视觉细节）和**认知流**（cognitive stream，承载高层语义理解），并通过检索、融合与压缩机制维持紧凑且可追溯的长期表示。

### 本文动机与核心思路

基于上述观察，MemoryVLA提出了一种**认知-记忆-动作**（Cognition-Memory-Action）框架，核心动机在于：将人类双重记忆的计算原理嵌入VLA架构，使模型在动作预测时能够显式地检索和利用历史上下文，从而突破当前VLA方法在非马尔可夫任务中的性能瓶颈。

具体而言，MemoryVLA引入**感知-认知记忆库**（Perceptual-Cognitive Memory Bank, PCMB），将VLM编码的感知令牌和认知令牌分别存储为长期记忆条目，通过时序位置编码引导的交叉注意力检索决策相关的历史特征，经可学习门控自适应融合当前与历史表示，并在记忆库容量满时基于相邻条目余弦相似度合并冗余（Figure 1c, Figure 2）。这一设计使模型在保持推理效率的前提下（Table 15：延迟仅增加0.007s），在多个仿真基准和真实世界长时域任务上均显著超越无记忆的VLA基线（Figure 1d：在SimplerEnv-Bridge上较CogACT提升14.6个百分点）。

## 核心创新

MemoryVLA 的核心创新在于引入**感知-认知记忆库（Perceptual-Cognitive Memory Bank, PCMB）**，将人类双重记忆理论（工作记忆与长时记忆）映射为视觉-语言-动作模型中的双流时序记忆机制。与仅依赖当前观测的主流VLA模型相比，MemoryVLA 在四个关键维度上实现了结构性改变：

### 1. 时序上下文建模：从单帧观测到双流结构化记忆

主流VLA方法（如 **CogACT** (Li et al., 2024a)、**OpenVLA** (Kim et al., 2024)、**π0** (Black et al., 2024)）仅以当前RGB帧为条件预测动作，在非马尔可夫任务中因缺乏历史上下文而频繁失败。MemoryVLA 将历史信息解耦为两条互补流：**感知流**保留细粒度视觉细节（256个感知令牌），**认知流**捕获高层语义（来自VLM的EOS位置输出），二者共同构成结构化的长期记忆库（Section 3.3, Figure 2）。

消融实验（Table 6）直接验证了这一设计的必要性：同时使用感知记忆和认知记忆在 SimplerEnv-Bridge 上达到 71.9% 的平均成功率，而仅使用认知记忆降至 63.5%，仅使用感知记忆降至 64.6%，证明双流记忆存在显著的互补效应。

### 2. 信息融合策略：从直接拼接转为自适应门控融合

基线方法通常直接将多帧拼接输入Transformer（如 **RoboVLMs** (Liu et al., 2025b)），或仅依赖当前观测。MemoryVLA 设计了可学习的**门控融合机制**，通过 MLP 生成融合权重，自适应地整合当前令牌与从记忆库中检索的历史特征：

$$
\tilde{x} = g^x \odot H^x + (1 - g^x) \odot x, \quad g^x = \sigma(\mathrm{MLP}([x, H^x]))
$$

其中 $H^x$ 为检索到的历史特征，$g^x$ 为门控向量（Section 3.3, Eq. 7-8）。这一设计使模型能够根据当前状态自动权衡历史信息的贡献。消融实验（Table 7）表明，门控融合（71.9%）显著优于直接相加融合（67.7%），验证了自适应门控对整合历史信息的关键作用。

### 3. 记忆管理：从无记忆到语义感知的冗余压缩

现有VLA方法缺乏记忆管理机制。MemoryVLA 在记忆库容量满时，通过**基于相似度的合并策略**压缩冗余：在每个流中计算相邻条目的余弦相似度，选取相似度最高的相邻对进行平均合并：

$$
i_x^* = \arg\max_{i=1,\ldots,L-1} \cos(\tilde{x}_i, \tilde{x}_{i+1}), \quad m_{i_x^*}^x \gets \frac{1}{2}(\tilde{x}_{i_x^*} + \tilde{x}_{i_x^*+1})
$$

（Section 3.3, Eq. 9）。这一策略优于简单的FIFO合并（71.9% vs 66.7%，Table 7），表明语义感知的压缩有利于保留决策相关信息，避免因机械丢弃而损失关键历史线索。

### 4. 动作预测条件：从单一认知条件到双流记忆条件

主流扩散型VLA的动作专家仅基于高层认知特征生成动作。MemoryVLA 的**记忆条件扩散动作专家**同时条件于融合记忆的认知令牌和感知令牌，使扩散Transformer在去噪过程中既能利用高层语义引导，又能补充细粒度视觉历史（Section 3.4）。这一设计使模型在真实世界长时域任务上达到 83% 的成功分数，较 CogACT 提升 26 个百分点（Table 5），充分证明了双流记忆条件对时序决策的核心贡献。

### 创新总结

MemoryVLA 的四个 changed slots 构成了一个完整的记忆增强决策闭环：双流记忆库提供结构化的历史表示，自适应门控实现上下文感知的信息融合，语义压缩维持紧凑的长期存储，双流条件使动作生成充分利用多粒度历史信息。这一设计在 6 个基准、150+ 任务上均超越无记忆基线，且推理延迟仅增加 0.007 秒（Table 15），实现了性能与效率的有效平衡。

## 整体框架

![[assets/figures/papers/paper_list_l50_https_openreview_net_forum_id_54U3XHf7qq/figures/002_Figure_2.jpg]]
*Figure 2: Overall architecture of MemoryVLA. RGB observation and language instruction are encoded by a 7B VLM into perceptual and cognitive tokens, forming short-term working memory. The working memory queries a perceptual-cognitive memory bank (PCMB) to retrieve relevant historical context, including high-level semantics and low-level visual details, adaptively fuses it with current tokens, and consolidates the PCMB by merging the most similar neighbors. The memoryaugmented tokens then condition a diffusion transformer to predict a sequence of future actions*

![[assets/figures/papers/paper_list_l50_https_openreview_net_forum_id_54U3XHf7qq/figures/003_Figure_3.jpg]]

MemoryVLA 是一种 **认知-记忆-动作（Cognition-Memory-Action）** 框架，核心目标是解决机器人操作中因非马尔可夫性导致的时序决策歧义。其整体 pipeline 由三个关键模块串联构成：**视觉-语言认知模块**负责将当前观测编码为工作记忆，**感知-认知记忆模块**负责检索、融合并维护历史上下文，**记忆条件扩散动作专家**则基于记忆增强的表示生成未来动作序列。

### 输入输出规范

给定当前第三人称 RGB 图像 $I$ 和语言指令 $L$，策略 $\pi$ 输出未来 $T$ 步动作序列：

$$\mathcal{A} = (a_1, \ldots, a_T) = \pi(I, L)$$

每个动作 $a_t$ 由 7 自由度组成，包含相对位移、相对欧拉角旋转和二值夹爪状态：

$$a_t = [\Delta x, \Delta y, \Delta z, \Delta \theta_x, \Delta \theta_y, \Delta \theta_z, g]^\top$$

### 模块间数据流

**1. 视觉-语言认知模块（Vision-Language Cognition Module）**

该模块以 7B Prismatic VLM 为骨干。RGB 图像 $I$ 首先经并行 DINOv2 与 SigLIP 视觉编码器提取特征，拼接后通过 SE-bottleneck 压缩为 256 个感知令牌 $p \in \mathbb{R}^{N_p \times d_p}$。语言指令 $L$ 与压缩视觉令牌一同输入 LLaMA-7B 语言模型，取 EOS 位置的输出向量作为认知令牌 $c \in \mathbb{R}^{1 \times d_c}$。二者共同构成短时工作记忆：

$$M_{wk} = \{ p \in \mathbb{R}^{N_p \times d_p}, c \in \mathbb{R}^{1 \times d_c} \}$$

**2. 感知-认知记忆模块（Perceptual-Cognitive Memory Module）**

工作记忆作为查询，从长期记忆库 $M_{pcmb}$ 中检索历史上下文。记忆库分离为感知流和认知流两个子库，各存储最多 $L$ 个历史条目：

$$M_{pcmb} = \{ m^x \mid x \in \{per, cog\} \}, \quad m^x = \{ m_i^x \}_{i=1}^L$$

检索操作通过带时序位置编码的交叉注意力实现，以当前令牌为查询、记忆库条目为键值对，提取决策相关的历史特征 $\hat{H}^x$：

$$\hat{H}^x = \mathrm{softmax}\left(\frac{q^x (K^x)^\top}{\sqrt{d_x}}\right) V^x$$

检索到的历史特征与当前令牌通过可学习门控自适应融合，门控值由当前表示与历史特征的拼接经 MLP 后 sigmoid 激活得到：

$$\tilde{x} = g^x \odot H^x + (1 - g^x) \odot x, \quad g^x = \sigma(\mathrm{MLP}([x, H^x]))$$

融合后的令牌更新至记忆库。当记忆库容量达到上限 $L$ 时，在每个流内计算相邻条目的余弦相似度，选取相似度最高的相邻对求平均以压缩冗余：

$$i_x^* = \arg\max_{i=1,\ldots,L-1} \cos(\tilde{x}_i, \tilde{x}_{i+1}), \quad m_{i_x^*}^x \gets \frac{1}{2}(\tilde{x}_{i_x^*} + \tilde{x}_{i_x^*+1})$$

**3. 记忆条件扩散动作专家（Memory-Conditioned Diffusion Action Expert）**

记忆增强后的认知令牌和感知令牌分别通过认知注意力层和感知注意力层条件化扩散 Transformer（DiT），采用 DDIM 以 10 步去噪生成未来 16 步动作序列。认知注意力提供高层语义引导，感知注意力补充细粒度视觉细节，使动作预测同时受益于两种记忆流。

### 框架设计动机

该双流记忆设计直接针对一个关键瓶颈：主流 VLA 模型（如 **CogACT**（Li et al., 2024a）、**π0**（Black et al., 2024）、**OpenVLA**（Kim et al., 2024））仅依赖当前观测，在推按钮等前后画面几乎一致的任务中无法分辨状态变化，导致决策歧义。MemoryVLA 借鉴人类工作记忆与情节记忆的双重记忆理论，将历史信息解耦为细粒度感知流和高层认知流，使模型既能回溯“看到了什么”，也能利用“理解了什么”进行时序推理。

整体架构如图 2 所示，实验设置涵盖 3 种机器人、6 个基准、150+ 任务及 500+ 变体（图 4），全面验证了记忆机制在不同场景下的通用性。

## 核心模块与公式推导

### 问题形式化

MemoryVLA将机器人操作建模为从感知到动作序列的映射。给定当前时刻的第三人称RGB图像 $I$ 和语言指令 $L$，策略 $\pi$ 输出未来 $T$ 步的动作序列：

$$\mathcal{A} = (a_1, \ldots, a_T) = \pi(I, L)$$

每个动作 $a_t$ 由7自由度末端执行器指令构成：

$$a_t = [\Delta x, \Delta y, \Delta z, \Delta \theta_x, \Delta \theta_y, \Delta \theta_z, g]^\top$$

其中 $\Delta x, \Delta y, \Delta z$ 为相对位移，$\Delta \theta_x, \Delta \theta_y, \Delta \theta_z$ 为相对欧拉角旋转，$g$ 为二值夹爪状态。该形式化明确了模型需从单帧观测和语言指令中预测多步未来动作，而传统VLA在此框架下缺乏对历史上下文的显式建模。

### 视觉-语言认知模块

该模块负责将原始感知输入转化为结构化的工作记忆表示。视觉编码采用并行的DINOv2和SigLIP双骨干网络处理当前RGB图像，拼接后的原始视觉令牌经感知压缩模块（SE-bottleneck）压缩为 $N_p=256$ 个感知令牌 $p \in \mathbb{R}^{N_p \times d_p}$。语言指令与压缩后的视觉令牌共同输入7B Prismatic VLM，取LLaMA-7B输出在句子结束（EOS）位置的隐向量作为认知令牌 $c \in \mathbb{R}^{1 \times d_c}$，以紧凑形式承载高层语义。由此构成短时工作记忆：

$$M_{wk} = \{ p \in \mathbb{R}^{N_p \times d_p}, c \in \mathbb{R}^{1 \times d_c} \}$$

### 感知-认知记忆模块

记忆模块是MemoryVLA的核心创新，包含三个子机制：检索、门控融合与合并。

**记忆库结构。** 长期记忆库 $M_{pcmb}$ 分别维护感知流和认知流两个独立存储空间：

$$M_{pcmb} = \{ m^x \mid x \in \{per, cog\} \}, \quad m^x = \{ m_i^x \}_{i=1}^L$$

每个流最多存储 $L$ 个历史条目，感知条目维度为 $\mathbb{R}^{N_p \times d_p}$，认知条目维度为 $\mathbb{R}^{1 \times d_c}$。

**记忆检索。** 以当前工作记忆令牌为查询，通过带有时序位置编码的缩放点积注意力从记忆库中检索相关历史特征：

$$\hat{H}^x = \mathrm{softmax}\left(\frac{q^x (K^x)^\top}{\sqrt{d_x}}\right) V^x$$

其中 $q^x$ 为当前令牌的查询向量，$K^x$ 和 $V^x$ 分别为记忆库中对应流的键和值。时序位置编码使模型能够区分记忆条目的先后顺序，从而在检索时利用时间线索定位决策关键帧。

**门控融合。** 检索到的历史特征 $\hat{H}^x$ 与当前表示 $x$ 通过可学习门控自适应融合：

$$g^x = \sigma(\mathrm{MLP}([x, \hat{H}^x]))$$

$$\tilde{x} = g^x \odot \hat{H}^x + (1 - g^x) \odot x$$

门控值 $g^x$ 由拼接后的特征经MLP和sigmoid激活得到，控制历史信息与当前信息的混合比例。消融实验表明，该门控机制（71.9%）显著优于直接相加融合（67.7%），验证了自适应整合对时序决策的重要性（Table 7）。

**记忆合并。** 当记忆库达到容量上限时，在每个流内计算相邻条目的余弦相似度，选取最相似的一对进行平均合并：

$$i_x^* = \arg\max_{i=1,\ldots,L-1} \cos(\tilde{x}_i, \tilde{x}_{i+1}), \quad m_{i_x^*}^x \gets \frac{1}{2}(\tilde{x}_{i_x^*} + \tilde{x}_{i_x^*+1})$$

该语义感知的压缩策略（71.9%）优于简单的FIFO替换（66.7%），表明基于相似度的冗余消除能更有效地保留决策相关信息（Table 7）。感知流和认知流独立执行合并操作，确保两个模态的关键信息均得到保留。

### 记忆条件扩散动作专家

动作预测采用基于扩散Transformer（DiT）的架构，使用DDIM以10步去噪生成未来16步动作序列。与标准扩散模型不同，该专家同时条件于记忆增强后的认知令牌和感知令牌：认知注意力层提供高层语义引导，感知注意力层补充细粒度视觉历史细节。这种双条件设计使动作预测既能利用紧凑的语义记忆进行时序推理，又能从感知记忆中获取精确的空间信息。推理效率测试显示，引入记忆模块仅增加0.007秒延迟（0.194s vs 0.187s）和0.8GB GPU内存占用，开销极小（Table 15）。

## 实验与分析

### 评估设置概览

MemoryVLA在6个基准、3种机器人平台、超过150个任务及500余个变体上进行了系统评估（Figure 4），覆盖仿真与真实世界两大场景。仿真基准包括SimplerEnv-Bridge（WidowX机器人）、SimplerEnv-Fractal（Google机器人）、LIBERO（Franka机器人）和Mikasa-Robo（Franka机器人）；真实世界评估则包含通用任务与长时域时序任务两类。所有方法统一使用第三方视角RGB图像和语言指令，不包含腕部相机或本体感知状态，确保比较公平。

### 仿真基准主结果

**SimplerEnv-Bridge**（Table 1）：MemoryVLA在四个操作任务上取得71.9%的平均成功率，较CogACT-Large（57.3%）提升14.6个百分点，较π0-Beta（59.3%）提升12.6个百分点。在“Stack Cube”和“Eggplant in Basket”等需要精细操作的任务上，MemoryVLA分别达到70.7%和68.0%，显著优于所有基线。

![[assets/figures/papers/paper_list_l50_https_openreview_net_forum_id_54U3XHf7qq/figures/007_Table_1.jpg]]
*Table 1: Performance comparison on SimplerEnv-Bridge (Li et al., 2024b) with WidowX robot. CogACT-Large is our re-evaluated baseline using official weight, and MemoryVLA achieves a +14.6 gain in average success. Entries marked with * are reproduced from open-pi-zero, which leverage additional proprioceptive state inputs; they also adopt Uniform/Beta timestep sampling*

**SimplerEnv-Fractal**（Table 2）：在Google机器人平台上，MemoryVLA取得72.7%的整体成功率，较CogACT（68.1%）提升4.6个百分点。在Visual Matching套件的“Open/Close Drawer”任务上，MemoryVLA达到84.7%，较CogACT提升12.9个百分点，表明记忆机制对需要追踪物体状态变化的任务尤为关键。

**LIBERO**（Table 3）：MemoryVLA在五个子套件上取得96.5%的平均成功率，较CogACT（93.2%）提升3.3个百分点，超越所有对比方法。值得注意的是，部分标注*的基线方法（如4D-VLA、RoboVLMs）额外使用了本体感知和腕部相机输入，但MemoryVLA仅凭RGB输入仍表现更优。在LIBERO-Long-90长时域子集上，MemoryVLA的优势进一步凸显，表明记忆库对长序列任务的持续上下文保持能力。

**Mikasa-Robo**（Table 4）：该基准专门评估时序记忆能力，MemoryVLA取得41.2%的平均成功率，较先前最优方法CronusVLA（29.4%）提升11.8个百分点。在最具挑战性的“ShellGame Touch”任务上，MemoryVLA达到88%的成功率，较CronusVLA提升41.0个百分点——该任务要求模型在杯子移动后识别目标杯的位置，仅凭当前观测无法完成，充分验证了感知-认知记忆库在解决非马尔可夫决策问题上的核心价值。

![[assets/figures/papers/paper_list_l50_https_openreview_net_forum_id_54U3XHf7qq/figures/010_Table_4.jpg]]
*Table 4: Performance comparison on Mikasa-Robo (Cherepanov et al., 2025) with Franka robot. Success rates (%) are reported. CronusVLA results are reproduced by us*

### 真实世界实验结果

真实世界实验涵盖Franka和WidowX两种机器人平台（Table 5）。在6个通用任务上，MemoryVLA取得85%的平均成功分数，较CogACT（76%）提升9个百分点；在6个长时域时序任务上，MemoryVLA取得83%的成功分数，较CogACT（57%）大幅提升26个百分点。长时域任务（如“Change Food”、“Clean Table & Count”）要求模型追踪多步历史操作，仅凭当前RGB帧无法判断下一步动作（Figure 11, Figure 12），MemoryVLA的记忆检索机制在这些场景中发挥了决定性作用。

![[assets/figures/papers/paper_list_l50_https_openreview_net_forum_id_54U3XHf7qq/figures/011_Table_5.jpg]]
*Table 5: Performance comparison on real-world experiments with Franka and WidowX robots. Success scores (%) are reported over six general tasks and six long-horizon temporal tasks. All methods are evaluated with only third-person RGB observation and language instruction*

### 记忆机制消融实验

消融实验在SimplerEnv-Bridge上进行，系统验证了各设计选择的有效性。

**双流记忆的必要性**（Table 6）：同时使用感知记忆和认知记忆达到71.9%的平均成功率，而仅使用认知记忆降至63.5%，仅使用感知记忆降至64.6%。双流设计存在互补作用：认知流提供高层语义线索（如“已放入篮子”），感知流保留细粒度视觉细节（如物体精确位置），二者共同支撑时序决策。

![[assets/figures/papers/paper_list_l50_https_openreview_net_forum_id_54U3XHf7qq/figures/012_Table_6.jpg]]
*Table 6: Ablation on memory type and length. We report average success rates (%) on SimplerEnv-Bridge tasks*

**记忆长度敏感性**（Table 6）：记忆长度设为16时性能最优（71.9%），过短（长度4，67.7%）无法保留足够的时序上下文，过长（长度64，67.7%）则可能引入噪声或冗余信息。但最优长度具有任务依赖性：在真实世界“Clean Table & Count”任务中，长度256表现更佳（Table 10），表明当前缺乏自动调整机制是一个实际局限。

**门控融合与记忆合并**（Table 7）：门控融合机制（71.9%）显著优于直接相加融合（67.7%），证明自适应门控对于区分当前观测与历史线索的贡献至关重要。基于相似度的Token-Merge记忆合并（71.9%）优于FIFO合并（66.7%），表明语义感知的压缩策略能更有效地保留决策相关信息，减少冗余。

**认知令牌数量**（Table 11）：将认知令牌数量从1增至4未带来性能提升（71.9% vs 69.8%），说明单个4096维EOS位置的语义向量已足够承载高层认知信息，增加令牌反而可能引入冗余。

### 推理效率

推理效率测试在RTX 4090和HGX H20 GPU上进行（Table 15）。MemoryVLA的推理延迟为0.194秒，较无记忆基线（0.187秒）仅增加0.007秒；GPU内存额外占用0.8GB。这一微小开销源于记忆检索和门控融合的轻量设计，使得MemoryVLA在保持实时性的同时获得显著的时序推理能力提升。

### 记忆检索案例分析

Figure 10展示了记忆检索注意力权重的可视化。在真实世界“Change Food”任务和仿真“ShellGame Touch”任务中，模型成功检索并关注那些仅凭当前观测无法分辨的关键历史帧。例如，在推按钮任务中，按钮按下前后的画面几乎完全相同（Figure 1a），模型通过检索历史帧中的按钮状态变化来消除决策歧义，直接验证了感知-认知记忆库在非马尔可夫场景下的因果作用。

### 鲁棒性与泛化

在真实世界OOD场景中（Figure 5），MemoryVLA在未见背景、干扰物、光照变化、新物体/容器及遮挡条件下仍保持较高成功率。仿真OOD评估（Figure 6, Figure 7）显示，模型对背景、纹理、光照等中等程度偏移泛化良好，但对未见相机视角的泛化能力有限——例如“Pick Coke Can”任务成功率从92.0%下降至42.0%，表明视角变化仍是鲁棒性的主要短板。

### 失败模式与局限性

基于实验结果，MemoryVLA的主要失败模式集中在以下方面：第一，仿真环境中对极端相机视角变化的泛化能力不足，视角偏移导致感知令牌分布漂移，记忆检索的匹配质量下降；第二，最优记忆长度依赖具体任务，当前缺乏自适应配置机制，在实际部署中需要针对不同任务手动调参；第三，虽然引入了长期记忆单元，但尚未实现跨场景、跨任务的知识积累（如记忆反思或终身记忆），限制了更大规模部署的可扩展性。

## 方法谱系与知识库定位

### 1. 方法谱系：从无记忆VLA到时序上下文建模

MemoryVLA 的提出源于对当前 VLA 模型**非马尔可夫决策能力缺失**这一瓶颈的回应。主流方法如 **CogACT**（Li et al., 2024a）、**π0**（Black et al., 2024）和 **OpenVLA**（Kim et al., 2024）仅以当前观测为条件预测动作，在长时域、时序依赖任务中因缺乏历史上下文而频繁失败（Table 5, Figure 10）。MemoryVLA 的核心贡献在于将**结构化记忆**引入 VLA 框架，其方法定位可以从以下三个维度理解：

**（1）与无记忆基线的根本差异：条件空间扩展。**
CogACT、π0 等扩散型 VLA 的动作预测条件仅包含当前帧的视觉-语言特征。MemoryVLA 通过感知-认知记忆库（PCMB）将条件空间扩展为 $\{I_t, L, M_{pcmb}\}$，使模型能够追溯历史状态以消解当前观测的歧义。这一扩展在 Push Buttons 等非马尔可夫任务中尤为关键——预推和推后画面几乎相同，仅凭当前帧无法判断下一步动作（Figure 1a）。

**（2）与视频帧拼接方法的区别：结构化双流记忆 vs. 原始帧序列。**
**RoboVLMs**（Liu et al., 2025b）通过视频帧间格式建模时序，但直接将多帧输入 Transformer 带来高昂的计算代价。MemoryVLA 将历史信息解耦为**感知流**（细粒度视觉细节）和**认知流**（高层语义），并通过检索机制仅提取决策相关的历史条目，而非处理完整帧序列。消融实验表明，双流设计（71.9%）显著优于单一记忆类型（感知 64.6%、认知 63.5%），验证了解耦的必要性（Table 6）。

**（3）与视觉轨迹简化方法的区别：保留语义 vs. 丢弃细节。**
**TraceVLA**（Zheng et al., 2024b）通过视觉轨迹简化时序建模，但丢弃了语义细节。MemoryVLA 的认知流以 VLM 的 EOS 位置输出作为紧凑的语义表示（$c \in \mathbb{R}^{1 \times d_c}$），在保留高层认知的同时维持计算效率。消融实验证实，单个 4096 维认知令牌已足以承载决策所需语义，增加至 4 个令牌未带来性能提升（69.8% vs 71.9%，Table 11）。

**（4）与同期时序上下文方法的对比。**
**CronusVLA**（Li et al., 2025a）是近期同样引入时序上下文的 VLA 方法。在 Mikasa-Robo、SimplerEnv 和 LIBERO 等多个基准上的全面对比显示，MemoryVLA 在所有测试场景中均优于 CronusVLA（Table 17），表明双流记忆与门控融合的设计在时序决策上具有更强的表达能力。

### 2. 适用边界

**（1）强时序依赖场景是核心增益区。**
MemoryVLA 的最大优势体现在需要追溯历史状态的任务上。在真实世界长时域任务中，MemoryVLA 的成功分数达 83%，较 CogACT 提升 26 个百分点（Table 5）；在 Mikasa-Robo 的 ShellGameTouch 任务上，提升幅度高达 41.0%（Table 4）。这些任务共同的特点是：当前观测无法唯一确定正确动作，必须回忆先前的操作序列。

**（2）通用操作任务同样受益，但增益幅度递减。**
在 LIBERO 基准上，MemoryVLA 的增益为 +3.3%（96.5% vs 93.2%，Table 3），在 SimplerEnv-Fractal 上为 +4.6%（72.7% vs 68.1%，Table 2）。这些任务的部分子任务（如抓取放置）对时序依赖较弱，记忆机制的边际贡献相应减小。

**（3）视角变化是当前鲁棒性的主要短板。**
在仿真 OOD 评估中，当相机视角发生显著变化时，MemoryVLA 的性能出现明显下降。例如 Pick Coke Can 任务在未见相机视角下成功率从 92.0% 降至 42.0%（Figure 6）。这表明模型的视觉编码和记忆检索对特定视角存在过拟合，跨视角泛化能力有待增强。

**（4）记忆长度需人工设定，缺乏任务自适应能力。**
消融实验显示，SimplerEnv-Bridge 任务的最优记忆长度为 16（71.9%），而过短（4，67.7%）或过长（64，67.7%）均导致性能下降（Table 6）。然而在真实世界 Clean Table & Count 任务中，长度 256 表现更佳。目前 PCMB 的容量是固定超参数，无法根据任务时序跨度自动调整。

### 3. 局限与开放问题

**局限一：缺少记忆反思机制。**
当前 PCMB 仅执行检索-融合-合并的循环，未对存储的历史表示进行更高层次的抽象或推理。模型无法像人类那样“反思”过去的经验，例如从失败尝试中提炼通用策略。将记忆条目对齐到 LLM 的输入空间以支持嵌入空间下的链式思维推理，是下一步的关键方向。

**局限二：未实现终身记忆。**
PCMB 的记忆容量固定为 $L$，当容量满时通过相似度合并来压缩冗余。然而，这种合并是局部的（仅合并相邻最相似条目），且被合并的条目永久丢失。缺乏生物启发的记忆巩固机制——将频繁重用的经验蒸馏为永久表示，从而支持跨场景、跨任务的知识积累。

**局限三：真实世界验证规模有限。**
当前真实世界评估覆盖 12 个任务和两种机器人平台（Franka, WidowX），在更多具身形态（如移动操作、双臂协作）和更大规模任务集上的泛化能力尚待验证。

**局限四：极端视角变化的鲁棒性不足。**
如适用边界所述，模型在未见相机视角下性能大幅下降。如何在保持记忆有效性的同时增强视觉编码的视角不变性，是一个亟待解决的问题。

**开放问题：**

1. **记忆反射**：能否设计机制将 PCMB 中的历史表示对齐到 VLM 的嵌入空间，使模型能够在嵌入层面进行“回忆-推理-决策”的链式过程，而非仅依赖注意力检索？
2. **终身记忆系统**：如何实现生物启发的记忆巩固，自动识别并蒸馏频繁重用的经验为永久表示，支持跨多任务和具身平台的可扩展泛化？
3. **自适应记忆配置**：PCMB 容量、认知令牌数量等超参数能否通过元学习或在线自适应方式根据任务时序特征自动配置？
4. **视角鲁棒性增强**：如何在训练或记忆检索阶段引入视角增强策略，使模型对相机位姿变化具有更强的鲁棒性，同时不损害记忆检索的精度？

## 原文 PDF

![[paperPDFs/ICLR_2026/MemoryVLA_Perceptual_Cognitive_Memory_in_Vision_Language_Action_Models_for_Robotic_Manipulation.pdf]]
