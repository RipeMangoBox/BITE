---
title: "STAGE: Storyboard-Anchored Generation for Cinematic Multi-shot Narrative"
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: paperPDFs/arxiv_2025/STAGE_Storyboard_Anchored_Generation_for_Cinematic_Multi_shot_Narrative.pdf
project_link: null
code_link: null
aliases:
- SSAGS
- STAGE
tags:
- arxiv_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
core_operator: 将预测目标重构为每个镜头的起始-结束帧对（结构性故事板），为镜头内动态和镜头间过渡提供显式视觉锚点；同时引入双编码策略共享镜头内上下文、多镜头记忆包保持长程实体一致性，并通过两阶段训练（监督微调+偏好对齐）学习复杂的电影过渡语言。
primary_logic: 通过同时预测起始和结束帧，模型能隐式共享视觉上下文，确保镜头内时空连贯性；压缩的记忆机制使得跨镜头实体一致，偏好对齐则优化了电影语言的时序关系，从而生成具有专业叙事质量的视频。
claims:
- STAGE在所有八项定量指标和四项基于LLM的评估上均超越现有方法，取得最优性能。
- 移除多镜头记忆包（MMP）会导致跨镜头一致性指标（SC-E、BC-E、TVS）显著下降。
- 移除双编码策略（DES）会使整体质量（AQ）和对象一致性（OC）降低。
- 将两阶段训练替换为标准训练（W/ TTS）会降低过渡平滑度（TVS）和故事一致性（STS）。
---

# STAGE: Storyboard-Anchored Generation for Cinematic Multi-shot Narrative

> [!tip] 核心洞察
> 通过同时预测起始和结束帧，模型能隐式共享视觉上下文，确保镜头内时空连贯性；压缩的记忆机制使得跨镜头实体一致，偏好对齐则优化了电影语言的时序关系，从而生成具有专业叙事质量的视频。

| 字段 | 内容 |
|------|------|
| 中文题名 | STAGE：故事板锚定的电影化多镜头叙事生成 |
| 英文题名 | STAGE: Storyboard-Anchored Generation for Cinematic Multi-shot Narrative |
| 会议/期刊 | arXiv 2025 |
| Links | [paper](https://arxiv.org/abs/2512.12372) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation |
| Method | STAGE (Storyboard-Anchored Generation) with STEP² |
| Dataset | ConStoryBoard test set, Human evaluation |

> [!tip] 效果简介
> - ConStoryBoard test set 上，OVQ (Overall Quality) 0.8929；AQ (Aesthetic Quality) 0.7689；TVS (Transition Visual Smoothness) 0.2732。
> - Human evaluation 上，VQE (Visual Quality Evaluation) 57.6%；TAE (Text Alignment Evaluation) 53.2%；SCE (Shot Consistency Evaluation) 72.8%。

## 概要

现有基于关键帧的多镜头视频生成方法（如 **StoryDiffusion** (Zhou et al., NeurIPS 2024)、**MovieDreamer** (Zhao et al., arxiv 2024)、**Cineverse** (Phung et al., arxiv 2025) 等）通常仅预测稀疏的关键帧序列，缺少对镜头间过渡结构和电影语言（如镜头/反打镜头、变焦、移动）的显式建模，导致跨镜头动作断裂、外观突变，破坏叙事连贯性。

STAGE 将预测目标重构为每个镜头的**起始-结束帧对**（结构性故事板），为镜头内动态和镜头间过渡提供显式视觉锚点。核心组件 STEP² 模型通过**双编码策略**隐式共享镜头内视觉上下文以确保时空连贯性，通过**多镜头记忆包**将历史帧压缩为紧凑令牌以保持长程实体一致性，并采用**两阶段训练**（监督微调 + 偏好对齐 DPO）学习复杂的电影过渡语言。

在 ConStoryBoard 测试集上，STAGE 在所有八项定量指标和四项基于 LLM 的评估上均超越现有方法，取得最优性能（Table 1）。人类评估中，STAGE 在视觉质量、文本对齐、镜头一致性和镜头间过渡四项实验中均获得最高用户偏好（Table 2）。消融实验证实，移除多镜头记忆包会显著降低跨镜头一致性指标，移除双编码策略会损害整体质量与对象一致性，替换为单阶段标准训练则会削弱过渡平滑度与故事一致性。

视频生成领域正经历从单镜头向多镜头叙事的范式跃迁。用户期望通过一段故事描述即可获得具有电影级连贯性的多镜头视频，然而现有方法在这一目标上暴露出根本性瓶颈：**跨镜头过渡结构的缺失**。端到端生成方法（如扩散模型直接输出长视频）虽然架构简洁，但缺乏对镜头边界的显式建模，导致动作断裂与外观突变；基于关键帧的方法（如**StoryDiffusion** (Zhou et al., NeurIPS 2024)、**MovieDreamer** (Zhao et al., arxiv 2024)）通过预测稀疏关键帧序列来引导生成，却仅对每个镜头输出单个代表性帧，本质上将镜头间过渡视为黑箱——模型无法理解“镜头A如何演化到镜头B”这一电影语言的核心命题。

这一瓶颈的深层原因在于**预测目标与叙事需求之间的结构性错配**。电影叙事依赖精确的镜头内动态（如推拉摇移）和镜头间过渡（如正反打、跳切），而单帧关键帧既不能锚定镜头内部的时空演化轨迹，也无法为相邻镜头提供过渡约束。其直接后果是：生成的视频序列中，角色外观在镜头切换时发生突变，运动方向出现逻辑矛盾，叙事流被频繁打断。

STAGE 的动机正是从这一根本缺陷出发，将预测目标重构为**每个镜头的起始-结束帧对**——即结构性故事板。这一设计将镜头内动态显式编码为“从起始帧到结束帧的演化路径”，同时为镜头间过渡提供双向视觉锚点：前一镜头的结束帧与后一镜头的起始帧构成天然的过渡约束对。在此基础上，STAGE 引入三项机制来系统性解决连贯性问题：(1) **双编码策略**，通过联合编码起始-结束帧的潜变量来共享镜头内视觉上下文；(2) **多镜头记忆包**，将历史帧压缩为紧凑令牌以维持长程实体一致性；(3) **两阶段训练**（监督微调 + 偏好对齐），使模型显式学习符合人类偏好的电影过渡语言。这一方案从根本上将多镜头视频生成从“独立帧拼接”提升为“叙事结构驱动的连贯创作”。

## 核心方法与创新机理

STAGE 的核心创新在于将多镜头视频生成任务**重新定义为结构性故事板预测问题**，通过预测每个镜头的起始-结束帧对（而非稀疏关键帧），为镜头内动态和镜头间过渡提供显式视觉锚点。围绕这一目标重构，方法在四个关键维度上引入了差异化设计。

### 1. 预测目标重构：从稀疏关键帧到起始-结束帧对

现有基于关键帧的方法（如 **StoryDiffusion** (Zhou et al., NeurIPS 2024)、**MovieDreamer** (Zhao et al., 2024)）通常仅为每个镜头预测单个关键帧，缺少对镜头内部运动轨迹和镜头间过渡结构的建模，导致动作断裂和外观突变。STAGE 的核心洞察是：**同时预测起始帧和结束帧**，使模型隐式共享镜头内的视觉上下文，从而确保时空连贯性。这一重构使得后续的视频生成模型（如 WanX）能够以起始-结束帧为锚点，插值出连贯的镜头内运动。

### 2. 跨镜头记忆机制：多镜头记忆包

长序列生成中，如何保持实体（人物、物体、场景）的跨镜头一致性是核心瓶颈。STAGE 提出**多镜头记忆包（Multi-shot Memory Pack, MMP）**，将历史帧的潜在编码通过渐进空间平铺压缩为紧凑令牌：

$$M_i = \mathrm{SpatialTile}_{j \in \{1, ..., 2i-2\}} \big( \mathcal{P}(m_j', A_j) \big)$$

其中压缩率 $A_j = 1/2^j$，确保较早帧占用更少空间，总面积收敛。这种压缩机制使模型能够以固定大小的记忆令牌访问全部历史视觉上下文，而非完整存储所有帧或完全丢弃历史信息。消融实验证实，移除 MMP 后跨镜头一致性指标显著下降（SC-E 从 0.6917 降至 0.6088，BC-E 从 0.8207 降至 0.7311，TVS 从 0.2732 降至 0.2370）。

### 3. 镜头内连贯性建模：双编码策略

传统方法独立编码每个关键帧，忽略了同一镜头内起始与结束状态之间的因果关联。STAGE 引入**双编码策略（Dual-Encoding Strategy, DES）**，将起始帧和结束帧的潜在变量连接为一个联合张量，使扩散 Transformer 在去噪过程中共享视觉上下文。这一设计确保了镜头内部的逻辑相关性——例如，一个“角色走向门口”的镜头，其起始帧和结束帧中的角色外观、场景布局必须保持一致。消融实验表明，移除 DES 会导致整体美学质量（AQ 从 0.7689 降至 0.7217）和对象一致性（OC 从 0.2713 降至 0.2488）下降。

### 4. 电影语言过渡建模：两阶段训练与偏好对齐

电影叙事中的镜头过渡（如正反打、变焦、移动镜头）具有复杂的时序语义，单纯依赖监督微调难以捕捉这些微妙模式。STAGE 采用**两阶段训练策略**：首先通过流匹配损失进行监督微调（SFT），建立基础生成能力：

$$\mathcal{L}_{\mathrm{SFT}} = \mathbb{E}_{x_i^1, x_i^0, \mathcal{C}_i, t} \lVert v_{\theta}(x_i^t, t, \mathcal{C}_i) - v_t \rVert^2$$

其中 $v_t = x_i^1 - x_i^0$ 为恒定速度场。随后使用直接偏好优化（DPO）进行偏好对齐，最大化模型对人工优选样本的偏好概率：

$$\mathcal{L}_{\mathrm{DPO}} = - \mathbb{E}_{(y_w, y_l), \mathcal{C}_i, t} \left[ \log \sigma \left( \beta ( \mathrm{D}_{\theta} - \mathrm{D}_{\mathrm{ref}} ) \right) \right]$$

其中 $\mathbf{D}_k$ 计算策略模型和参考模型对正负样本的速度预测误差差。消融实验证实，替换为单阶段标准训练（W/ TTS）会损害过渡平滑度（TVS 从 0.2732 降至 0.2195）和故事一致性（STS 从 0.6255 降至 0.5111）。

### 创新总结

| 创新维度 | 基线做法 | STAGE 方案 | 因果机制 |
|---------|---------|-----------|---------|
| 预测目标 | 稀疏关键帧 | 起始-结束帧对 | 隐式共享视觉上下文，确保镜头内连贯 |
| 跨镜头记忆 | 无或完整历史 | 多镜头记忆包 | 压缩历史为紧凑令牌，保持长程实体一致 |
| 镜头内建模 | 独立编码 | 双编码策略 | 联合编码起始-结束帧，共享潜在空间 |
| 训练策略 | 标准微调 | SFT + DPO 两阶段 | 偏好对齐优化电影过渡语言 |

这四项创新构成互补体系：起始-结束帧对提供结构锚点，记忆包维持跨镜头实体，双编码保障镜头内逻辑，偏好对齐注入电影语言知识。三者共同解决了“叙事连贯性”这一核心瓶颈，使 STAGE 在所有定量指标和人类评估上取得最优性能。

STAGE 将多镜头视频生成重构为**故事板锚定的起始-结束帧对预测**流水线。其核心洞察是：现有方法仅预测稀疏关键帧，缺少对镜头间过渡结构和电影语言的显式建模，导致跨镜头动作断裂、外观突变。STAGE 通过在每个镜头中同时预测起始帧和结束帧（结构性故事板），为镜头内动态和镜头间过渡提供显式视觉锚点，从根本上提升叙事连贯性。

### 三阶段流水线

如 Figure 3 所示，STAGE 由三个顺序模块组成，形成从文本故事到多镜头视频的完整生成链路：

![[assets/figures/papers/paper_list_l91_https_arxiv_org_abs_2512_12372/figures/004_Figure_3.jpg]]
*Figure 3: Overview of our proposed STAGE workflow. The core component of STAGE is the Start-End frame-pair prediction model (STEP2), which iteratively generates start-end frame pairs for each shot. To ensure long-term consistency*

1. **Director Agent（导演代理）**：将用户提供的主题或故事描述扩展为结构化的文字故事板 $S = \mathrm{G}_{\mathrm{dir}}(T_{\mathrm{desc}})$（Equation 7），为后续视觉生成提供镜头级别的语义规划。

2. **STEP²（Start-End Frame-Pair Prediction）**：核心生成模块，迭代预测每个镜头的起始-结束帧对 $(F_i^{\mathrm{S}}, F_i^{\mathrm{E}}) = \mathrm{STEP^2}(S_i, \{(F_j^{\mathrm{S}}, F_j^{\mathrm{E}})\}_{j=1}^{i-1})$（Equation 8）。该模块内嵌三个关键机制：
   - **多模态理解与生成统一架构**：基于 MMDiT 块的扩散 Transformer，从多样化上下文进行鲁棒推理。
   - **多镜头记忆包（Multi-Shot Memory Pack）**：将先前所有镜头帧的潜在编码压缩为紧凑令牌 $M_i$（Equation 1），确保长程实体一致性。
   - **双编码策略（Dual-Encoding Strategy）**：将当前镜头的起始帧和结束帧潜变量拼接，隐式共享视觉上下文，保证镜头内时空连贯性。

3. **Refiner Agent + Video Generation（精炼代理与视频生成）**：利用已生成的起始-结束帧对，精炼代理生成包含视觉细节的增强提示 $R_i = G_{\mathrm{refine}}(D_i, F_i^{\mathrm{S}}, F_i^{\mathrm{E}})$（Equation 9），随后调用现成视频生成模型 $G_{\mathrm{video}}$ 合成最终视频片段 $V_i$（Equation 10）。

### 训练策略

STEP² 采用**两阶段训练**方案（Section 4.2）：

- **阶段一：监督微调（SFT）**——基于流匹配（Flow Matching）框架，使用 $\mathcal{L}_{\mathrm{SFT}}$ 损失（Equation 4）训练模型预测从噪声到干净帧对的速度场 $v_t = x_i^1 - x_i^0$，建立强生成基础。
- **阶段二：偏好对齐（DPO）**——通过直接偏好优化 $\mathcal{L}_{\mathrm{DPO}}$（Equation 5）对齐人类偏好，显式优化镜头间的电影语言过渡关系。训练配置：SFT 迭代 100K 步，DPO 迭代 20K 步，8 张 A800 GPU，Adam 优化器，学习率 $1 \times 10^{-4}$。

### 输入输出流

整个流水线的信息流为：**用户故事主题 → 文字故事板 → 每镜头起始-结束帧对 → 增强提示 → 视频片段 → 多镜头叙事视频**。其中，多镜头记忆包在 STEP² 的迭代生成中持续累积历史视觉上下文，形成跨越镜头的隐式记忆通道，这是保证长序列叙事一致性的关键数据流设计。

STAGE 的核心生成模型 **STEP²**（Start-End Frame-Pair Prediction）采用扩散 Transformer 架构，由多个 MMDiT 块构成。其设计围绕三个关键机制展开：多镜头记忆包、双编码策略和两阶段训练。

### 多镜头记忆包（Multi-Shot Memory Pack）

随着生成镜头数增加，历史帧的潜在编码数量线性增长，直接将其全部作为条件输入会带来不可承受的计算开销。STEP² 通过渐进空间平铺（progressive spatial tiling）将先前所有帧的潜在编码压缩为固定大小的紧凑记忆令牌。对于第 $i$ 个镜头，记忆包 $M_i$ 的构建方式为：

$$M_i = \mathrm{SpatialTile}_{j \in \{1, ..., 2i-2\}} \big( \mathcal{P}(m_j', A_j) \big)$$

其中 $m_j'$ 为按重要性排序后的先前帧潜在编码，压缩率 $A_j = 1/2^j$ 随帧索引递减，确保总面积收敛。该机制使得模型在生成当前镜头时能以固定计算成本访问压缩后的长程视觉上下文，是跨镜头实体一致性（如人物外观、场景元素）的核心保障。

### 双编码策略（Dual-Encoding Strategy）

传统关键帧方法独立编码每个镜头帧，导致镜头内起始帧与结束帧之间缺乏视觉上下文共享，容易出现逻辑断裂。STEP² 将当前镜头的起始帧和结束帧潜在变量沿通道维度拼接，形成联合镜头张量 $x_i$，使两者在生成过程中隐式共享视觉信息。生成过程通过流匹配（flow matching）框架实现：将干净的联合镜头张量 $x_i^1$ 与高斯噪声 $x_i^0$ 线性插值：

$$\boldsymbol{x}_i^t = t \cdot \boldsymbol{x}_i^1 + (1 - t) \cdot \boldsymbol{x}_i^0$$

随后求解常微分方程从 $t=0$ 到 $t=1$ 生成起始-结束帧对：

$$\mathrm{d} x_i^t / \mathrm{d} t = \mathscr{E}_{\mathrm{gen}} (U_i, t, x_i^t, M_i)$$

其中 $\mathscr{E}_{\mathrm{gen}}$ 为扩散 Transformer 生成模型，$U_i$ 为多模态理解编码器提取的文本条件，$M_i$ 为前述记忆包。双编码策略确保同镜头内起始帧与结束帧的时空连贯性。

### 两阶段训练

**第一阶段——监督微调（SFT）**：采用流匹配损失，使模型预测的速度场 $v_\theta$ 逼近恒定速度 $v_t = x_i^1 - x_i^0$：

$$\mathcal{L}_{\mathrm{SFT}} = \mathbb{E}_{x_i^1, x_i^0, \mathcal{C}_i, t} \lVert v_{\theta}(x_i^t, t, \mathcal{C}_i) - v_t \rVert^2$$

此阶段建立强生成基础，训练 100K 迭代，优化器为 Adam，学习率 $1 \times 10^{-4}$，使用 8 块 A800 GPU。

**第二阶段——偏好对齐（DPO）**：为显式优化镜头间过渡的电影语言质量，引入直接偏好优化。损失函数为：

$$\mathcal{L}_{\mathrm{DPO}} = - \mathbb{E}_{(y_w, y_l), \mathcal{C}_i, t} \left[ \log \sigma \left( \beta ( \mathrm{D}_{\theta} - \mathrm{D}_{\mathrm{ref}} ) \right) \right]$$

其中偏好差异 $\mathbf{D}_k$ 定义为策略模型和参考模型对负样本与正样本的速度预测误差差：

$$\mathbf{D}_k = \| v_k(\hat{x}_i^t, t, \mathcal{C}_i) - \hat{v}^t \|^2 - \| v_k(\check{x}_i^t, t, \mathcal{C}_i) - \check{v}^t \|^2$$

DPO 阶段训练 20K 迭代，使模型输出向人类偏好的电影过渡风格对齐。消融实验证实，将两阶段训练替换为标准单阶段训练（W/ TTS）会导致过渡平滑度（TVS: 0.2195）和故事一致性（STS: 0.5111）显著下降，验证了偏好对齐对电影语言建模的关键作用。

### 推理流水线中的公式衔接

在完整 STAGE 推理流水线中，上述模块按以下公式串联：导演代理根据故事描述 $T_{\mathrm{desc}}$ 生成结构化文字故事板 $S = \mathrm{G}_{\mathrm{dir}}(T_{\mathrm{desc}})$；STEP² 迭代预测第 $i$ 镜头的起始-结束帧对 $(F_i^{\mathrm{S}}, F_i^{\mathrm{E}}) = \mathrm{STEP^2}(S_i, \{(F_j^{\mathrm{S}}, F_j^{\mathrm{E}})\}_{j=1}^{i-1})$；精炼代理生成增强提示 $R_i = G_{\mathrm{refine}}(D_i, F_i^{\mathrm{S}}, F_i^{\mathrm{E}})$；最终视频生成模型合成片段 $V_i = G_{\mathrm{video}}(R_i, F_i^{\mathrm{S}}, F_i^{\mathrm{E}})$。

## 实验与关键发现

### 主实验结果

STAGE 在 ConStoryBoard 测试集上对所有基线方法实现了全面超越。Table 1 报告了八项定量指标和四项基于 LLM 的评估结果，STAGE 在全部维度上取得最优性能。具体而言，整体质量 OVQ 达到 0.8929，美学质量 AQ 为 0.7689，图像质量 IQ 为 0.7305。在跨镜头一致性方面，镜头一致性 SC 为 0.9695，背景一致性 BC 为 0.9685，镜头一致性评估 SC-E 为 0.6917，背景一致性评估 BC-E 为 0.8207，过渡视觉平滑度 TVS 为 0.2732。此外，对象一致性 OC 为 0.2713，视觉-文本一致性 VTC 为 0.6069，镜头间一致性 ISC 为 0.6985，故事一致性 STS 为 0.6255。

![[assets/figures/papers/paper_list_l91_https_arxiv_org_abs_2512_12372/figures/006_Table_1.jpg]]
*Table 1: Quantitative experiment results of comparison and ablation. ↑ (↓) means higher (lower) is better. Throughout the paper, the best performances are highlighted in bold*

对比的基线方法包括 **StoryDiffusion**（Zhou et al., NeurIPS 2024）、**MovieDreamer**（Zhao et al., arxiv 2024）、**Cineverse**（Phung et al., arxiv 2025）、**Seed-Story**（Yang et al., ICCV 2025）和 **Cut2next**（He et al., arxiv 2025）。这些方法在跨镜头过渡指标（如 TVS、SC-E、BC-E）上普遍表现较弱，反映了其缺少对镜头间过渡结构的显式建模这一根本瓶颈。Figure 4 的视觉质量对比进一步印证了定量结论：STAGE 生成的视频在镜头切换处保持了主体外观和运动轨迹的连贯性，而基线方法常出现动作断裂或外观突变。

![[assets/figures/papers/paper_list_l91_https_arxiv_org_abs_2512_12372/figures/005_Figure_4.jpg]]
*Figure 4: Visual quality comparisons with multi-shot video generation methods*

人类评估结果（Table 2）强化了自动指标的结论。在视觉质量评估（VQE）、文本对齐评估（TAE）、镜头一致性评估（SCE）和镜头间过渡评估（ITE）四项测试中，STAGE 分别获得 57.6%、53.2%、72.8% 和 69.6% 的用户偏好率，均显著高于对比方法。SCE 和 ITE 的高偏好率直接验证了结构性故事板锚定策略对叙事连贯性的提升效果。

![[assets/figures/papers/paper_list_l91_https_arxiv_org_abs_2512_12372/figures/009_Table_2.jpg]]
*Table 2: Percentage (%) of user ratings in the four experiments of human evaluation for the results*

### 消融实验

为验证各核心组件的贡献，作者进行了系统的消融实验（Table 1 下半部分，Figure 5）。

![[assets/figures/papers/paper_list_l91_https_arxiv_org_abs_2512_12372/figures/007_Figure_5.jpg]]
*Figure 5: Ablation study results with different variants of our STAGE framework*

**移除多镜头记忆包（W/o MMP）** 对跨镜头一致性造成了显著损害。SC-E 从完整模型的 0.6917 降至 0.6088，BC-E 从 0.8207 降至 0.7311，TVS 从 0.2732 降至 0.2370。这表明压缩历史帧为紧凑令牌的记忆机制是维持长程实体一致性的关键——缺少该机制时，模型无法有效利用先前镜头的视觉上下文，导致镜头间外观和背景发生漂移。

**移除双编码策略（W/o DES）** 主要影响整体质量和对象一致性。AQ 从 0.7689 降至 0.7217，OC 从 0.2713 降至 0.2488。这验证了连接起始-结束帧潜变量以共享视觉上下文的设计对于镜头内时空连贯性的必要性：独立编码时，起始帧和结束帧之间缺乏隐式信息交互，导致镜头内动作逻辑断裂。

**替换为单阶段标准训练（W/ TTS）** 削弱了过渡平滑度和故事一致性。TVS 从 0.2732 降至 0.2195，STS 从 0.6255 降至 0.5111。这证明了两阶段训练方案（监督微调 + DPO 偏好对齐）对学习电影语言过渡的独特价值——仅靠标准监督微调无法有效捕捉人类对镜头过渡的偏好模式。

Figure 5 的定性消融结果与定量趋势一致：W/o MMP 变体在跨镜头场景中出现明显的角色外观不一致，W/o DES 变体在镜头内动作连贯性上表现较差，W/ TTS 变体的镜头过渡显得生硬。

### 公平性讨论

需要指出的是，ConStoryBoard 数据集为本文任务专门构建，基线方法可能未在该数据分布上进行训练，因此性能对比存在一定优势偏差。此外，视频生成阶段依赖外部模型（如 WanX），不同版本的外部模型可能导致输出质量波动。自动评估指标（如基于 CLIP 的 SC-E、BC-E）虽能反映一定程度的语义一致性，但可能无法完全捕捉人类对电影叙事的细腻感知，人类评估结果（Table 2）在此起到重要补充作用。

### 长序列生成能力

Figure 6 展示了一个长程多镜头视频生成结果，STAGE 在多个连续镜头中保持了角色外观、场景背景和光照条件的高度一致性，验证了多镜头记忆包在长序列场景下的有效性。该结果说明，通过渐进空间平铺压缩机制（压缩率 $A_j = 1/2^j$），记忆令牌的总面积保持收敛，使得模型即使在数十个镜头的长序列中也能维持可控的上下文开销。

![[assets/figures/papers/paper_list_l91_https_arxiv_org_abs_2512_12372/figures/008_Figure_6.jpg]]
*Figure 6: A long-range multi-shot video generation result of our STAGE framework, demonstrating high cross-shot consistency*

### 失败模式与局限性

尽管 STAGE 在定量和定性评估中表现优异，论文指出了若干局限。第一，当前流水线依赖外部视频生成模型进行最终的视频片段合成，未进行端到端联合训练，因此无法保证所有中间帧的密集平滑过渡——起始-结束帧对提供了视觉锚点，但镜头内部的帧间过渡质量受限于外部模型的能力。第二，ConStoryBoard 数据集基于 Condensed Movies 构建，可能无法覆盖所有电影类型和叙事语言风格，模型在非电影领域的泛化性有待验证。第三，偏好对齐训练需要人工筛选优选样本，扩展成本较高，如何自动生成更细粒度的电影语言属性以减少人工标注依赖是一个开放问题。

## 定位与知识库关联

### 任务定位：从关键帧生成到结构性故事板预测

STAGE 的核心贡献在于将多镜头视频生成任务从“预测稀疏关键帧序列”重构为“预测每个镜头的起始-结束帧对（结构性故事板）”。这一重构直接回应了现有方法的瓶颈：**StoryDiffusion**（Zhou et al., NeurIPS 2024）、**MovieDreamer**（Zhao et al., arxiv 2024）、**Cineverse**（Phung et al., arxiv 2025）等方法通常仅预测逐镜头的单个关键帧，缺少对镜头内动态范围和镜头间过渡结构的显式建模，导致跨镜头动作断裂和外观突变。STAGE 通过同时预测起始帧 $F_i^{\mathrm{S}}$ 和结束帧 $F_i^{\mathrm{E}}$，为镜头内的时间演变和镜头间的视觉衔接提供了显式锚点，从而将问题从“生成孤立帧”提升为“生成具有电影语言结构的帧对序列”。

### 与基线方法的差异化对比

| 维度 | 现有方法 | STAGE (STEP²) |
|------|---------|---------------|
| 预测目标 | 稀疏关键帧（逐镜头单帧） | 起始-结束帧对（结构性故事板） |
| 镜头内连贯性 | 独立编码关键帧，无时序约束 | 双编码策略（DES）：连接起始-结束帧潜变量，共享视觉上下文 |
| 跨镜头记忆 | 无（或使用完整历史帧，计算代价高） | 多镜头记忆包（MMP）：压缩历史帧为紧凑令牌，总面积收敛 |
| 电影语言过渡 | 未显式建模 | 两阶段训练（SFT + DPO偏好对齐），显式优化镜头过渡 |
| 生成流程 | 端到端或关键帧合成 | 三阶段流水线：导演代理→STEP²预测→精炼代理+视频合成 |

具体而言：

- **StoryDiffusion** 依赖一致自注意力机制生成长序列图像，但未针对多镜头视频的过渡结构进行专门设计，其自注意力窗口无法显式建模镜头切换的电影语言（如镜头/反打镜头、变焦）。
- **MovieDreamer** 采用层次化生成策略，但其层次结构主要面向视觉序列的粗到细生成，而非镜头级的叙事结构。
- **Cut2next**（He et al., arxiv 2025）通过上下文微调生成下一镜头，与 STAGE 的目标最为接近，但其仅预测下一镜头的单个关键帧，缺少对镜头内起始-结束动态的建模。
- **Seed-Story**（Yang et al., ICCV 2025）面向多模态长故事生成，但其关键帧选择策略未引入结构性帧对约束。

### 方法谱系中的技术继承与创新

STAGE 的技术路线融合了多个研究脉络：

1. **流匹配生成范式**：STEP² 基于流匹配（Flow Matching）框架，将生成过程建模为从高斯噪声到干净帧对的常微分方程求解 $\mathrm{d} x_i^t / \mathrm{d} t = \mathscr{E}_{\mathrm{gen}}(U_i, t, x_i^t, M_i)$。这与当前扩散模型的主流趋势一致，但将其适配到联合帧对预测的场景。

2. **记忆压缩机制**：多镜头记忆包采用渐进空间平铺策略 $M_i = \mathrm{SpatialTile}_{j \in \{1, ..., 2i-2\}} \big( \mathcal{P}(m_j', A_j) \big)$，压缩率 $A_j = 1/2^j$ 确保总面积收敛。这一设计与长序列建模中的记忆压缩方法（如 Transformer-XL 的片段级循环）共享思想，但针对视觉帧的二维空间结构进行了定制。

3. **偏好对齐训练**：第二阶段采用直接偏好优化（DPO），损失函数为 $\mathcal{L}_{\mathrm{DPO}} = - \mathbb{E}_{(y_w, y_l), \mathcal{C}_i, t} \left[ \log \sigma \left( \beta ( \mathrm{D}_{\theta} - \mathrm{D}_{\mathrm{ref}} ) \right) \right]$，将电影语言过渡的偏好信号注入生成模型。这继承了 LLM 对齐领域的方法论，但将其应用于视觉生成的速度场预测任务。

4. **多模态理解与生成统一架构**：STEP² 采用 MMDiT 块（基于 DiT 架构）实现多模态条件注入，这与当前多模态生成模型的设计趋势一致。

### 适用边界与局限

**适用场景**：
- 需要明确镜头切换结构的多镜头叙事视频生成（如电影片段、故事可视化）
- 用户提供故事主题描述，系统自动生成结构化故事板和对应视频
- 对跨镜头实体一致性（人物、场景、物体）有较高要求的场景

**已知局限**（来自论文分析）：
1. **非端到端流水线**：当前 STAGE 依赖外部视频生成模型（如 WanX）将预测的起始-结束帧对合成为视频片段，STEP² 与视频生成器之间未进行联合训练。这意味着密集帧间的平滑过渡无法得到保证——模型仅锚定了起始和结束帧，中间帧的质量完全取决于外部视频模型的插值能力。
2. **数据集覆盖范围有限**：ConStoryBoard 数据集基于 Condensed Movies 构建，可能偏向特定电影类型和语言风格，对动画、纪录片等类型的泛化性有待验证。
3. **偏好对齐的扩展成本**：DPO 训练需要人工筛选偏好样本对（正样本 vs 负样本），随着镜头数量和过渡类型增多，标注成本呈线性增长。
4. **评估指标的局限性**：自动评估指标（如基于 CLIP 的 SC-E、BC-E）可能无法完全反映人类对电影叙事连贯性的感知，尤其是对镜头节奏、情绪递进等高层语义的判断。

### 开放问题

1. **端到端密集一致性**：如何将多镜头记忆包和结构性故事板无缝集成到端到端视频生成主干中，使模型不仅能锚定起始-结束帧，还能保证所有中间帧的密集时空一致性？这需要重新设计视频生成架构的记忆注入机制。

2. **电影语言属性的自动标注**：当前偏好对齐依赖人工标注的镜头过渡偏好，能否自动生成更细粒度的电影语言属性（如镜头类型、运动模式、节奏标签）以减少人工依赖？这可能需要借助大型多模态模型的电影理解能力。

3. **长序列的累积误差控制**：随着镜头数量增加，多镜头记忆包的压缩损失会累积，可能导致后期镜头的实体一致性退化。如何设计自适应压缩率或选择性记忆机制以缓解这一问题？

4. **与现有视频生成模型的深度耦合**：当前 STAGE 将外部视频模型视为黑盒调用，若能实现 STEP² 与视频生成器的特征级交互（如将起始-结束帧对的潜在表示作为视频扩散模型的条件注入），可能进一步提升过渡质量。

## 原文 PDF

![[paperPDFs/arxiv_2025/STAGE_Storyboard_Anchored_Generation_for_Cinematic_Multi_shot_Narrative.pdf]]
