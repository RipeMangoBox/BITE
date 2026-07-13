---
title: "MoEActok: A MoE-based Action Tokenizer for Vision-Language-Action Models"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/MoEActok_A_MoE_based_Action_Tokenizer_for_Vision_Language_Action_Models.pdf
project_link: null
code_link: "https://github.com/cpaaax/MoEActok"
aliases:
- MoEActok
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 引入基于聚类的混合专家（MoE）VQ-VAE架构，将动作片段分组为技能簇，并为每个技能分配专用量化器，辅以适配器实现共享与技能专属空间的对齐。
primary_logic: 机器人操作动作在运动学空间内天然形成可分技能簇（见Figure 1）；通过强制每个专家学习一个技能簇，可消除跨技能表示冲突，提升重建保真度，并借助技能感知训练使VLA模型显式推理技能类别与动作标记。
claims:
- RoboTwin 12项模拟任务中，MoEActok-VLA平均成功率0.56，显著超越Uniform Binning、FAST、VQ-BET、VQ-VLA等基线。
- Simpler-Env 4项模拟任务中，MoEActok-VLA平均成功率0.38，同样领先所有对比方法。
- 消融实验表明，移除适配器或技能感知训练会导致RoboTwin成功率分别降至0.45和0.47，验证了关键组件的必要性。
- 在三个真实世界任务上零样本迁移，MoEActok-VLA平均成功率0.37，远超VQ-VLA（0.28）和Binning（0.10）。
---

# MoEActok: A MoE-based Action Tokenizer for Vision-Language-Action Models

> [!tip] 核心洞察
> 机器人操作动作在运动学空间内天然形成可分技能簇（见Figure 1）；通过强制每个专家学习一个技能簇，可消除跨技能表示冲突，提升重建保真度，并借助技能感知训练使VLA模型显式推理技能类别与动作标记。

| 字段 | 内容 |
|------|------|
| 中文题名 | MoEActok：基于混合专家的视觉-语言-动作模型动作分词器 |
| 英文题名 | MoEActok: A MoE-based Action Tokenizer for Vision-Language-Action Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Xu_MoEActok_A_MoE-based_Action_Tokenizer_for_Vision-Language-Action_Models_CVPR_2026_paper.html) · [Code](https://github.com/cpaaax/MoEActok) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | MoEActok |
| Dataset | RoboTwin, Simpler-Env, Real-world |

> [!tip] 效果简介
> - RoboTwin (12 tasks) 上，Average Success Rate 0.56 vs best prior method (e.g., VQ-VLA; exact values not extracted in part analyses) (substantially outperforms all baselines)。
> - Simpler-Env (4 tasks) 上，Average Success Rate 0.38 vs best prior method (e.g., VQ-VLA; exact values not extracted) (substantially outperforms all baselines)。
> - Real-world (3 tasks: Click Bell, Place Container on Plate, Pick Diverse Bottles) 上，Average Success Rate 0.37 vs 0.28 (VQ-VLA) / 0.10 (Binning) (+0.09 over VQ-VLA, +0.27 over Binning)。

## 概要

**问题瓶颈：** 现有面向视觉-语言-动作（VLA）模型的动作分词器通常采用单一量化器处理完整操作轨迹。然而，机器人操作轨迹天然包含多种异质技能（如全局移动与精细夹取），单一量化器难以同时覆盖这些差异显著的技能模式，导致表示冲突和优化权衡，限制了VLA模型的技能接地与泛化能力。

**核心方法：** MoEActok 提出一种基于聚类的混合专家（MoE）VQ-VAE动作分词器。其核心思路是：首先通过k-means聚类将动作片段划分为技能簇，随后为每个技能簇分配一个专用VQ量化器（专家），并辅以前/后适配器实现共享表示空间与技能专属空间的对齐。基于该分词器，进一步引入技能感知VLA训练范式，使模型显式预测技能类别并条件化生成动作标记，实现粗到细的技能感知动作生成。

**关键结论：**
- 在 RoboTwin 12项模拟任务中，MoEActok-VLA 平均成功率 **0.56**，显著优于 Uniform Binning、FAST、VQ-BET、VQ-VLA 等基线方法（Table 1）。
- 在 Simpler-Env 4项模拟任务中，平均成功率 **0.38**，同样全面领先（Table 2）。
- 三个真实世界任务上的零样本迁移平均成功率 **0.37**，远超 VQ-VLA（0.28）和 Binning（0.10）（Table 5）。
- 消融实验证实：移除适配器使成功率降至 0.45，移除技能感知训练降至 0.47，验证了各组件的必要性（Table 3/4）。
- 专家数量从 1 增至 4 时，RoboTwin 性能从 0.50 提升至 0.56，Simpler-Env 从 0.26 提升至 0.38（Figure 4/5），表明多专家技能解耦对性能提升起关键作用。



视觉-语言-动作（VLA）模型通过将机器人操作建模为序列预测问题，在多种操作任务中展现出强大的泛化能力。这类模型通常将连续的机器人动作转换为离散标记，以便与视觉和语言标记统一输入自回归Transformer进行训练。动作分词器（action tokenizer）因此成为VLA模型的关键上游组件，其编码质量直接影响下游策略的性能。

当前主流的动作标记方案可归为两类。一类是朴素的按维度分箱（Uniform Binning），将每个动作维度独立离散化，完全忽略动作维度间的关联结构。另一类是基于VQ-VAE的学习式分词器，如**VQ-BET**（Lee et al., ICML 2024）采用残差VQ-VAE进行行为生成，**VQ-VLA**（Wang et al., ArXiv 2025）则专门为VLA流水线设计了卷积残差VQ-VAE。这些方法共享一个根本性局限：它们使用**单一量化器**覆盖整个操作轨迹中的所有动作。

然而，机器人操作轨迹天然包含异质技能片段。如Figure 1所示，在BridgeData V2数据集上对动作片段进行聚类后，可以清晰观察到运动学空间内存在多个可分簇——例如大范围移动（涉及x, y, z的大幅度变化）与精细夹取（主要表现为gripper维度的开关）形成截然不同的分布模式。当单一量化器被迫同时编码这些异质技能时，会产生**表示冲突**：码本向量需要在差异巨大的动作模式之间妥协，导致重建保真度下降，并限制VLA模型对细粒度技能的接地能力。

这一瓶颈的因果机制在于：单一量化器的码本空间是全局共享的，无法为不同技能分配专属的表示子空间。由此带来的优化权衡使得模型在技能边界处产生高重建误差，进而影响下游VLA对动作标记的预测精度。

针对上述问题，本文提出**MoEActok**，一个基于混合专家（Mixture-of-Experts）的动作分词器。其核心洞见是：既然操作动作在运动学空间内天然形成技能簇，那么应当为每个技能簇分配专用量化器，从而消除跨技能表示冲突。具体而言，MoEActok首先通过K-means聚类将动作片段分组为技能簇，再构建K个专家VQ量化器，每个专家专门负责一个技能簇的编码与重建。此外，引入技能适配器实现共享表示空间与技能专属空间之间的映射，并通过技能感知训练使下游VLA模型显式推理技能类别与动作标记，形成从粗粒度技能识别到细粒度动作生成的级联预测范式。



## 核心方法与创新机理

MoEActok 的核心创新在于将传统 VLA 动作分词器中的**单一全局量化器**替换为**技能感知的混合专家（MoE）量化架构**，从根本上解决了异质操作轨迹中跨技能表示冲突导致的优化权衡问题。

### 技能解耦：从动作聚类到专家分工

传统动作分词器（如 VQ-VLA、VQ-BET）对完整轨迹的所有动作片段使用同一个 VQ 量化器，忽略了操作任务中天然存在的技能异质性——例如“移动到目标”与“精细夹取”在运动学空间中分布截然不同。MoEActok 的关键洞察是：**机器人操作动作在七维运动学空间内天然形成可分的技能簇**（见 Figure 1），强制单一量化器覆盖所有技能簇必然产生表示冲突。

基于此，MoEActok 引入**动作技能解耦策略**：首先对动作片段提取全局表示，然后使用 k-means 聚类将其划分为 K 个技能簇，并为每个片段分配技能标签 h。这一无监督聚类过程无需人工标注，自动将语义相似的动作片段归入同一技能类别。

### 混合专家量化器：技能专属码本

在技能解耦的基础上，MoEActok 部署 K 个独立的 VQ 量化器 $\{VQ_1, VQ_2, ..., VQ_K\}$，每个专家维护自己的码本，专门负责某一技能簇的动作量化。给定技能标签 h，量化过程选择对应专家：

$$z_q, q = \arg \min_{c \in VQ_h} ||z - c||_2$$

这种设计使每个专家只需学习单一技能簇的表示，消除了跨技能优化冲突。与 VQ-VLA 的单量化器相比，**changed slot** 在于量化器架构从“全局共享”变为“技能专属分工”。

### 技能适配器：共享与专属空间的桥梁

直接为每个专家配备独立编码器/解码器会导致参数冗余和技能间知识隔离。MoEActok 采用**共享编码器-解码器 + 技能适配器**的折中设计：

- **预量化适配器** $A_h^{pre}$ 将共享编码器输出 z 映射到技能 h 专属的潜在空间：$z' = A_h^{pre}(z) = W_1(\sigma_1(W_2(z) * W_3(z)) + \sigma_2(W_4(z)))$
- **后量化适配器** $A_h^{post}$ 将量化嵌入 $z_q$ 映射回统一潜在空间：$z_q' = A_h^{post}(z_q)$

这一 **changed slot** 替代了 VQ-VLA 中“直接量化共用编码器输出”的衔接方式。适配器以轻量参数代价实现了共享知识与技能专属表示的灵活对齐，消融实验证实移除适配器会导致 RoboTwin 成功率从 0.56 降至 0.45。

### 技能感知 VLA 训练：粗到细的动作生成

MoEActok 不仅改进了分词器架构，还提出了配套的**技能感知 VLA 训练范式**。传统 VLA 训练仅以自回归交叉熵预测动作标记，而 MoEActok 将技能标签 h 作为显式预测目标：

$$\mathcal{L}_{\mathrm{VLA}} = -\log P(h \mid o_t, s_t, l) - \sum_{r=1}^{R} \log P(q_r \mid q_{<r}, o_t, s_t, l, h)$$

这一 **changed slot** 将动作生成分解为“先识别技能类别，再条件生成动作标记”的粗到细流程。技能分类损失迫使 VLA 学会从视觉-语言上下文中推理当前应执行的技能类型，而条件动作标记预测则利用技能先验缩小生成空间。消融实验表明，移除技能感知训练会使 RoboTwin 成功率从 0.56 降至 0.47，验证了该组件的关键作用。

### 创新总结

MoEActok 的四个 changed slots 形成了一条完整的因果链：**技能解耦**发现动作空间的内在结构 → **专家量化器**消除跨技能表示冲突 → **技能适配器**平衡共享与专属 → **技能感知训练**将技能知识注入 VLA 推理。这一设计使 MoEActok-VLA 在 RoboTwin（12 任务平均 0.56）、Simpler-Env（4 任务平均 0.38）和真实世界（3 任务平均 0.37）上均显著超越 Uniform Binning、FAST、VQ-BET、VQ-VLA 等基线方法。



MoEActok 提出了一套“技能解耦动作分词 + 技能感知 VLA 训练”的端到端流水线，核心目标是将异质操作轨迹中的动作离散化从单一量化器扩展为混合专家（MoE）范式，从而消除跨技能表示冲突，并赋予 VLA 模型显式的技能推理能力。

### 流水线总览

整个框架由两个协同阶段构成（见图 Figure 2）：

![[assets/figures/papers/paper_list_l2172_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_MoEActok_A_MoE_base/figures/002_Figure_2.jpg]]
*Figure 2: Overview of MoEActok action tokenizer (top) and the MoEActok-based VLA model (bottom)*

1. **动作分词器训练阶段**（Figure 2 上）：基于离线操作数据集，先通过无监督聚类将动作片段划分为 K 个技能簇，再训练一个 MoE VQ-VAE 分词器，使每个专家量化器专精于一个技能簇。该阶段输出冻结的动作分词器与技能标签。
2. **技能感知 VLA 训练阶段**（Figure 2 下）：在冻结分词器与视觉编码器的前提下，VLA 模型同时预测技能类别与条件动作标记，实现粗到细的技能感知动作生成。

### 模块关系与数据流

#### 阶段一：动作技能解耦与 MoE 分词器训练

1. **动作技能解耦（Action-Skill Decoupling）**  
   从数据集中提取固定时间窗口的动作片段 $a_{t:t+k-1}$，通过共享编码器提取全局表示，再对全局表示应用 k-means 聚类，得到 K 个技能簇及每个片段的技能标签 $h$。这一步将动作空间在运动学层面天然形成的技能模式（见 Figure 1）显式化为离散技能类别。

2. **共享编码器（Shared Encoder）**  
   采用 CNN + Transformer 混合架构，将原始动作片段压缩为潜在表示 $z$。所有技能共享此编码器，以保留跨技能的通用运动基元。

3. **技能适配器（Skill Adapters）**  
   - **预量化适配器 $A_h^{\text{pre}}$**：将共享潜在表示 $z$ 映射到技能 $h$ 专属的潜在空间 $z'$，公式为：
     
$$
z' = A_h^{\text{pre}}(z) = W_1(\sigma_1(W_2(z) * W_3(z)) + \sigma_2(W_4(z)))
$$

   - **后量化适配器 $A_h^{\text{post}}$**：将量化嵌入 $z_q$ 映射回统一潜在空间 $z_q'$，供共享解码器重建。

4. **专家量化器组（Mixture-of-Experts Quantizers）**  
   K 个独立的 VQ 量化器 $\{VQ_1, ..., VQ_K\}$，每个维护专属码本。根据技能标签 $h$ 选择对应专家，对 $z'$ 执行最近邻量化：
   
$$
z_q, q = \arg\min_{c \in VQ_h} \|z' - c\|_2
$$

5. **共享解码器（Shared Decoder）**  
   从 $z_q'$ 重建动作片段 $\hat{a}_{t:t+k-1}$，训练损失为：
   
$$
\mathcal{L}_{\text{rec}} = \|\hat{a}_{t:t+k-1} - a_{t:t+k-1}\|_2^2
$$

   总标记器损失结合重建损失、码本优化损失 $\mathcal{L}_{\text{emb}}$ 和编码器承诺损失 $\mathcal{L}_{\text{com}}$：
   
$$
\mathcal{L}_{\text{total}} = \mathcal{L}_{\text{rec}} + \alpha\mathcal{L}_{\text{emb}} + \beta\mathcal{L}_{\text{com}}
$$

#### 阶段二：技能感知 VLA 训练

在分词器与视觉编码器冻结后，VLA 骨干（LLM + MLP 投影层）接收视觉观测 $o_t$、机器人状态 $s_t$ 和语言指令 $l$，自回归生成两个目标序列：

1. **技能分类**：预测技能标签 $h$。
2. **条件动作标记生成**：在已知 $h$ 的条件下，逐残差生成 $R$ 个动作标记 $q_1, ..., q_R$。

训练损失为粗到细分解：

$$
\mathcal{L}_{\mathrm{VLA}} = -\log P(h \mid o_t, s_t, l) - \sum_{r=1}^{R} \log P(q_r \mid q_{<r}, o_t, s_t, l, h)
$$

### 关键设计决策与因果机制

- **技能簇先验的引入**：k-means 聚类在动作片段层面而非单帧动作层面进行，捕获了时间上下文中的技能模式，为专家分工提供了结构化的归纳偏置。
- **适配器的双向映射**：预/后量化适配器实现了共享空间与技能专属空间的对齐，避免了完全独立的编码器-解码器带来的参数膨胀，同时保留了技能专属量化的精度优势。消融实验（Table 3/Table 4）表明，移除适配器导致 RoboTwin 平均成功率从 0.56 降至 0.45，验证了该模块的必要性。
- **技能感知训练的粗到细生成**：VLA 先预测高层技能意图，再在该意图约束下生成精细动作标记，显式解耦了“做什么技能”与“如何执行”两个决策层次。消融实验显示，移除技能感知训练后成功率降至 0.47，证实其关键作用。

### 输入输出规范

| 阶段 | 输入 | 输出 |
|------|------|------|
| 动作分词器训练 | 动作片段 $a_{t:t+k-1} \in \mathbb{R}^{k \times 7}$ | 技能标签 $h$、离散动作标记序列 $\{q_1, ..., q_R\}$、重建动作 $\hat{a}$ |
| VLA 推理 | 视觉观测 $o_t$、状态 $s_t$、语言指令 $l$ | 预测技能 $\hat{h}$、动作标记序列，经解码器恢复为连续动作 |



### 3.1 动作片段与技能解耦

机器人操作轨迹中的动作定义为 7 维向量 $a_t \in \mathbb{R}^7$，前六维为末端执行器的位置 $(x, y, z)$ 与姿态 $(roll, pitch, yaw)$，最后一维为夹爪动作（1 表示张开，0 表示闭合）。MoEActok 将连续动作序列切分为长度为 $k$ 的动作片段 $a_{t:t+k-1}$，作为分词器的基本处理单元。

动作技能解耦（Action-Skill Decoupling）是 MoEActok 的前置步骤。对于数据集中所有动作片段，首先通过共享编码器提取全局片段表示，随后应用 k-means 聚类将这些表示划分为 $K$ 个技能簇，并为每个片段分配技能标签 $h \in \{1, 2, \dots, K\}$。如 Figure 1 所示，末端执行器动作在运动学空间内天然形成可分的技能簇，这为后续的专家量化提供了结构基础。

![[assets/figures/papers/paper_list_l2172_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_MoEActok_A_MoE_base/figures/001_Figure_1.jpg]]
*Figure 1: Clustering results of actions on BridgeData V2. The seven dimensions (0-6) represent the robot end-effector actions: x, y, z coordinates for position, roll, pitch, yaw for orientation, and gripper action*

### 3.2 混合专家量化架构

MoEActok 的核心是一个基于混合专家（Mixture-of-Experts）的 VQ-VAE 架构，由以下模块组成：

**共享编码器（Shared Encoder）**：采用 CNN + Transformer 混合架构，将动作片段 $a_{t:t+k-1}$ 压缩为统一潜在表示 $z$。

**技能适配器（Skill Adapters）**：为解决共享表示与技能专属量化空间之间的对齐问题，MoEActok 引入预量化和后量化两组适配器。预量化适配器 $A_h^{pre}$ 将共享编码器输出 $z$ 映射到技能 $h$ 专属的潜在空间：

$$z' = A_h^{pre}(z) = W_1(\sigma_1(W_2(z) * W_3(z)) + \sigma_2(W_4(z)))$$

其中 $W_1$ 至 $W_4$ 为可学习权重矩阵，$\sigma_1$、$\sigma_2$ 为激活函数，$*$ 表示逐元素乘法。该设计通过门控机制实现技能特定的特征变换。

**专家量化器组（Mixture-of-Experts Quantizers）**：部署 $K$ 个独立向量量化器 $\{VQ_1, VQ_2, \dots, VQ_K\}$，每个量化器维护专属码本。根据技能标签 $h$ 选择对应专家进行量化：

$$z_q, q = \arg \min_{c \in VQ_h} \|z' - c\|_2$$

该公式表示在专家 $VQ_h$ 的码本中搜索与适配后表示 $z'$ 欧氏距离最近的码向量，返回量化嵌入 $z_q$ 及对应码本索引 $q$。

**后量化适配器（Post-Quantization Adapter）**：将量化嵌入 $z_q$ 映射回统一潜在空间，以供共享解码器重建：

$$z_q' = A_h^{post}(z_q)$$

**共享解码器（Shared Decoder）**：从 $z_q'$ 重建原始动作片段 $\hat{a}_{t:t+k-1}$。

### 3.3 训练目标

**分词器训练损失**：MoEActok 分词器的总损失由三项加权组成：

$$\mathcal{L}_{total} = \mathcal{L}_{rec} + \alpha \mathcal{L}_{emb} + \beta \mathcal{L}_{com}$$

其中重建损失为原始动作片段与解码输出之间的均方误差：

$$\mathcal{L}_{rec} = \|\hat{a}_{t:t+k-1} - a_{t:t+k-1}\|_2^2$$

$\mathcal{L}_{emb}$ 为码本优化损失，推动码本向量向适配后的编码器输出靠拢（对编码器施加 stop-gradient）；$\mathcal{L}_{com}$ 为编码器承诺损失，约束编码器输出不过度偏离所选码向量。$\alpha$ 和 $\beta$ 为平衡超参数。

**技能感知 VLA 训练损失**：在 VLA 模型微调阶段，MoEActok 引入粗到细的技能感知动作生成范式。VLA 损失由技能分类损失和条件动作标记预测损失组成：

$$\mathcal{L}_{\mathrm{VLA}} = -\log P(h \mid o_t, s_t, l) - \sum_{r=1}^{R} \log P(q_r \mid q_{<r}, o_t, s_t, l, h)$$

第一项为给定观测 $o_t$、状态 $s_t$ 和语言指令 $l$ 时预测技能标签 $h$ 的交叉熵损失；第二项为以技能 $h$ 为条件的自回归动作标记 $q_1, \dots, q_R$ 预测损失。该设计迫使 VLA 模型显式推理技能类别，再在技能约束下生成细粒度动作标记，从而提升动作生成的语义一致性和泛化能力。



## 实验与关键发现

### 模拟器主结果

MoEActok-VLA在RoboTwin（12项任务）和Simpler-Env（4项任务）两个模拟器基准上均取得领先成功率。**Table 1**给出了RoboTwin上不同VLA模型的成功率对比：MoEActok-VLA平均成功率达到0.56，显著超越Uniform Binning、FAST（Pertsch et al., 2025）、VQ-BET（Lee et al., ICML 2024）以及VQ-VLA（Wang et al., ArXiv 2025）等基线方法。**Table 2**的Simpler-Env结果呈现一致趋势，MoEActok-VLA平均成功率为0.38，同样领先所有对比方法。这一跨基准的稳定优势表明，MoE架构驱动的技能解耦量化并非针对单一环境的过拟合，而是有效缓解了异质动作轨迹中的表示冲突。

![[assets/figures/papers/paper_list_l2172_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_MoEActok_A_MoE_base/figures/003_Table_1.jpg]]
*Table 1: Success rates of different VLAs across RoboTwin simulation 12 tasks*

![[assets/figures/papers/paper_list_l2172_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_MoEActok_A_MoE_base/figures/004_Table_2.jpg]]
*Table 2: Success rates of different VLAs across Simpler-Env simulation 4 tasks*

### 消融实验

消融实验系统验证了MoEActok两个核心设计的必要性。**Table 3**（RoboTwin）与**Table 4**（Simpler-Env）显示：
- **移除技能适配器**（adapters）：RoboTwin平均成功率从0.56降至0.45，Simpler-Env相应下降。适配器承担共享空间与技能专属空间之间的映射，其缺失导致专家量化器无法有效利用技能特异性表示，重建质量与下游策略性能同步恶化。
- **移除技能感知训练**（skill-aware training）：RoboTwin成功率从0.56降至0.47，Simpler-Env亦出现明显退化。这表明显式建模技能类别作为中间预测目标，对VLA模型的粗到细动作生成具有关键作用——仅靠隐式条件不足以充分利用技能划分带来的结构先验。

![[assets/figures/papers/paper_list_l2172_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_MoEActok_A_MoE_base/figures/006_Figure_3.jpg]]
*Figure 3: Real-world manipulation visualizations for “Click Bell” and “Place Container Plate” tasks*

![[assets/figures/papers/paper_list_l2172_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_MoEActok_A_MoE_base/figures/007_Table_4.jpg]]
*Table 4: Results of ablation study on Simpler-Env benchmark*

### 专家数量影响

**Figure 4**（RoboTwin）和**Figure 5**（Simpler-Env）展示了专家数量K从1递增至4时的性能变化。当K=1时，模型退化为单一VQ-VAE，RoboTwin成功率为0.50，Simpler-Env为0.26；随着K增至4，两项基准分别提升至0.56和0.38。性能在K=4处趋于饱和，这与动作片段经k-means聚类后自然形成的技能簇数量相吻合，进一步印证了“每个专家学习一个技能簇”的设计合理性。

### 真实世界零样本迁移

**Table 5**报告了三个真实世界任务（Click Bell、Place Container on Plate、Pick Diverse Bottles）上的零样本迁移结果。MoEActok-VLA平均成功率为0.37，较VQ-VLA（0.28）提升0.09，较Uniform Binning（0.10）提升0.27。**Figure 3**可视化了Click Bell与Place Container Plate任务的操作序列，直观展示了模型在真实环境中的策略执行过程。零样本设置下仍保持对强基线的优势，说明技能感知的离散动作表示具备跨域泛化能力——技能簇结构捕获的是运动学层面的行为模式，而非特定场景的统计相关性。

### 推理效率

MoEActok-VLA在单张RTX 4090上的推理吞吐约为10 Hz；借助vLLM加速框架可进一步提升至54 Hz。这一吞吐量满足大多数操作任务的实时性要求，表明MoE架构引入的多专家量化并未带来显著的推理开销瓶颈。

### 补充图表

![[assets/figures/papers/paper_list_l2172_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_MoEActok_A_MoE_base/figures/010_Table_5.jpg]]
*Table 5: Real-world results*

![[assets/figures/papers/paper_list_l2172_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_MoEActok_A_MoE_base/figures/008_Figure_4.jpg]]
*Figure 4: The influence of the number of experts on the performance of RoboTwin*

![[assets/figures/papers/paper_list_l2172_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_MoEActok_A_MoE_base/figures/009_Figure_5.jpg]]
*Figure 5: The influence of the number of experts on the performance of Simper-Env*



## 定位与知识库关联

### 动作分词器的演进脉络

机器人视觉-语言-动作（VLA）模型的动作分词器设计，核心矛盾在于如何将连续、高维、多模态的末端执行器轨迹压缩为离散标记序列，同时保留技能语义。现有方案可沿两条轴线定位：

**朴素离散化。** 最直接的策略是对每个动作维度独立分箱（Uniform Binning），将7维动作向量 $a_t \in \mathbb{R}^7$ 的各分量等距划分。该方法完全忽略维度间相关性和时序结构，技能信息在分箱过程中被彻底破坏，真实世界零样本迁移成功率仅0.10（Table 5），构成性能下界。

**统一量化范式。** 为捕获动作的连续性与上下文依赖，一系列工作引入VQ-VAE架构。**VQ-BET**（Lee et al., ICML 2024）采用残差VQ-VAE进行行为生成，但设计初衷并非服务于VLA的视觉-语言条件生成。**VQ-VLA**（Wang et al., ArXiv 2025）专为VLA设计卷积残差VQ-VAE，使用单一量化器覆盖全部轨迹动作，在RoboTwin上取得0.50的平均成功率（Table 1），代表统一量化范式的当前最强水平。**FAST**（Pertsch et al., 2025）另辟蹊径，将动作信号变换至频域后应用字节对编码（BPE），利用频域能量集中特性提升压缩效率，但其离散化过程同样不区分技能边界。

上述方法的共同瓶颈在于：**单一量化器被迫同时编码异质技能（如全局移动与精细夹取），码本向量的表示空间被不同技能簇的样本拉扯，导致优化权衡与表示冲突**。这一瓶颈在Figure 1的聚类可视化中得到直观印证——BridgeData V2的动作片段在运动学空间内天然形成可分的技能簇，但统一量化器无法为每个簇分配专用表示容量。

### MoEActok的方法定位

MoEActok的核心创新在于将“技能解耦”作为动作分词器的设计原语，其方法定位可从三个层次理解：

**架构层面：混合专家量化。** MoEActok将单一VQ-VAE量化器替换为 $K$ 个专家量化器 $\{VQ_1, VQ_2, ..., VQ_K\}$，每个专家维护独立码本，仅负责编码特定技能簇的动作片段。技能分配通过k-means聚类自动完成，无需人工标注。这一设计直接缓解了统一量化器的表示冲突问题——每个专家的码本向量只需拟合单一技能簇的分布，重建保真度因此提升。

**衔接层面：技能适配器。** 共享编码器输出 $z$ 需先经技能特定适配器 $A_h^{pre}$ 映射到对应专家的潜在空间（Equation 2），量化嵌入 $z_q$ 再经 $A_h^{post}$ 映射回统一空间供共享解码器重建（Equation 3）。适配器的存在使得共享编码器/解码器可复用跨技能的低级运动基元，同时为每个专家保留专属的表示子空间，避免码本污染。

**训练层面：技能感知VLA。** MoEActok不仅改进分词器本身，还提出技能感知VLA训练范式（Equation 9）：将技能标签 $h$ 作为显式预测目标，与动作标记 $q_r$ 联合自回归建模。这使VLA模型在推理时先进行粗粒度的技能识别，再在技能约束下生成细粒度动作标记，形成“粗到细”的层次化动作预测。

### 与相关工作的关系边界

**与VQ-VLA的关系。** VQ-VLA是MoEActok最直接的对比基线。当MoEActok的专家数量 $K=1$ 时，架构退化为类似VQ-VLA的单一量化器方案（此时适配器退化为恒等映射），RoboTwin成功率为0.50（Figure 4），与VQ-VLA的0.50持平（Table 1），验证了两者在统一量化范式下的等价性。MoEActok的增益完全来自 $K>1$ 时的技能解耦效应。

**与FAST的关系。** FAST在频域操作，MoEActok在时域运动学空间操作，两者在变换域选择上正交。FAST的BPE机制本质上是数据驱动的码本构建，而MoEActok的技能聚类是语义驱动的专家分配，两者可潜在互补，但论文未进行组合实验。

**与VQ-BET的关系。** VQ-BET的残差VQ设计旨在增加码本容量，MoEActok的MoE设计旨在解耦技能表示。残差VQ通过多层量化逐步逼近目标，每层量化器仍覆盖全部技能；MoEActok通过路由机制将不同技能分配给不同专家，两者解决的是不同维度的问题。

### 适用边界与局限

**技能聚类质量的依赖。** MoEActok的性能高度依赖k-means聚类能否形成有意义的技能簇。论文在BridgeData V2上验证了聚类的有效性（Figure 1），但未讨论当数据集技能分布高度重叠或技能边界模糊时聚类质量的退化风险。若聚类结果与真实技能边界不匹配，专家分配将引入噪声而非信息增益。

**专家数量的敏感性。** Figure 4和Figure 5显示，RoboTwin上 $K$ 从1增至4时成功率从0.50升至0.56，Simpler-Env上从0.26升至0.38，但论文未探索 $K>4$ 时的性能饱和或退化趋势。过大的 $K$ 可能导致每个专家的训练样本不足，码本欠拟合。

**零样本迁移的泛化边界。** 真实世界零样本迁移（Table 5）的三项任务（Click Bell、Place Container on Plate、Pick Diverse Bottles）均为桌面级操作，未覆盖移动操作、双手协调、动态交互等更复杂的技能类型。MoEActok在这些场景下的技能聚类与专家泛化能力尚待验证。

**推理效率的权衡。** 论文报告MoEActok推理吞吐约10 Hz（单RTX 4090），利用vLLM加速可达54 Hz（Section 4.3）。但未分析MoE路由机制引入的额外延迟开销，以及专家数量增加对吞吐的影响。

### 开放问题

1. **技能簇数量的自动化选择。** 当前 $K$ 需人工设定，能否基于聚类紧密度指标（如轮廓系数）自动确定最优专家数量？
2. **跨具身迁移。** 不同机器人的运动学空间差异显著，在一个机器人数据上训练的MoEActok分词器能否迁移到其他具身形态？适配器是否需要重新训练？
3. **技能标签的语言对齐。** 当前技能标签 $h$ 是纯数值索引，若将其对齐到自然语言描述（如“抓取”“移动”“放置”），能否进一步提升VLA的语言指令跟随能力？
4. **动态技能路由。** 当前技能分配在分词器训练阶段固定，是否可以在VLA推理时根据视觉观测动态调整技能路由，以适应技能边界的模糊性？



## 原文 PDF

![[paperPDFs/CVPR_2026/MoEActok_A_MoE_based_Action_Tokenizer_for_Vision_Language_Action_Models.pdf]]
