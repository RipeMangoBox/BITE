---
title: "Joint-Aligned Latent Action: Towards Scalable VLA Pretraining in the Wild"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Joint_Aligned_Latent_Action_Towards_Scalable_VLA_Pretraining_in_the_Wild.pdf
project_link: "https://research.beingbeyond.com/jala"
code_link: null
aliases:
- JJALA
- JALATSVPW
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 联合对齐机制：将VLA产生的预测嵌入与逆动力学模型导出的潜在动作直接对齐，构建一个行为中心的统一潜在动作空间，从而同时从有标签和无标签人类视频中学习。
primary_logic: 舍弃像素重建，通过对齐预测表征与视觉动态隐式捕获的运动信息，以更高效且可控的方式扩展VLA预训练，减少对精细人工标注的依赖。
claims:
- JALA replaces reconstruction-driven pipelines with joint alignment between predictive embeddings and latent actions from IDM.
- JALA constructs a unified latent action space that supports learning from both lab-annotated and in-the-wild videos.
- The VLA predicts action tokens from mask tokens while aligning intermediate hidden states with latent actions from IDM.
- Predictive embeddings fed into a flow-matching head enable efficient transfer to robot tasks.
---

# Joint-Aligned Latent Action: Towards Scalable VLA Pretraining in the Wild

> [!tip] 核心洞察
> 舍弃像素重建，通过对齐预测表征与视觉动态隐式捕获的运动信息，以更高效且可控的方式扩展VLA预训练，减少对精细人工标注的依赖。

| 字段 | 内容 |
|------|------|
| 中文题名 | 联合对齐潜在动作：迈向可扩展的野外VLA预训练 |
| 英文题名 | Joint-Aligned Latent Action: Towards Scalable VLA Pretraining in the Wild |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2602.21736) · [Project](https://research.beingbeyond.com/jala) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | JALA (Joint-Aligned Latent Actions) |
| Dataset | Hand Motion Generation, GR1 Tabletop Tasks, LIBERO Two-View, Real-World Multi-Step |

> [!tip] 效果简介
> - Hand Motion Generation (Lab / Wild) 上，MPJPE↓ 7.16 (Lab) / 11.02 (Wild) (JALA-dino) vs 7.61 (Lab) / 16.91 (Wild) (Being-H0) (-0.45 (Lab) / -5.89 (Wild))。
> - GR1 Tabletop Tasks 上，Success Rate (%) 26.33 (JALA-dino) vs 12.91 (Being-H0) (+13.42)。
> - LIBERO Two-View 上，Average Success Rate (%) 96.9 (JALA-dino) vs 87.6 (JALA w/o align) (+9.3)。

## 概要

视觉‑语言‑动作模型（VLA）的规模化预训练长期受限于机器人动作标注数据的高度稀缺。大规模野外人类操作视频天然包含丰富的运动先验，但现有潜在动作方法依赖**重建驱动管线**——通过正向动力学模型从视频中重建未来帧来约束潜在动作，这一过程引入噪声、效率低下，且难以有效桥接有标签与无标签数据。**JALA**（Joint‑Aligned Latent Actions）针对这一瓶颈提出**联合对齐机制**：将VLA在掩码块预测中产生的预测嵌入直接与逆动力学模型（IDM）从边界帧导出的潜在动作进行L1对齐，从而构建一个行为中心的统一潜在动作空间。该空间同时兼容有动作标签的实验室数据与无标签的野外视频，使VLA能够从更大规模、更多样的人类操作数据中学习，而无需像素重建或伪标签生成。

核心方法论上，JALA引入**Latent Action Perceiver（LAP）**从视频块的首尾帧提取潜在动作，同时以**Latent State Perceiver（LSP）**将VLA上下文映射至同一空间，二者通过解耦EMA更新保持训练稳定。预训练后，预测嵌入直接馈入**流匹配头**生成机器人动作，形成从大规模人类视频预训练到机器人任务迁移的高效通路。为支撑该范式，作者构建了**UniHand‑Mix**数据集，在现有UniHand基础上扩展250万野外人类操作样本。

实验表明，联合对齐机制带来显著增益：在手部运动生成任务上，JALA在野外分割的MPJPE从16.91降至11.02（降幅34.8%）；在LIBERO双视图操作基准上，JALA‑dino平均成功率达96.9%，较去除对齐的变体提升9.3个百分点；在真实世界多步操作任务中，子任务完成率提升12.0个百分点。消融研究进一步确认，解耦EMA更新对稳定性至关重要（去除后成功率从96.9%骤降至56.6%），且下游性能随预训练野外数据比例增加而单调提升。JALA在同等规模模型中表现领先，在部分基准上甚至与更大规模模型竞争，同时保持仅使用人类数据预训练的高效性。

### 具身智能中的数据瓶颈

视觉-语言-动作模型（VLA）旨在赋予机器人理解和执行自然语言指令的能力，其核心在于学习从感知到动作的映射。当前VLA预训练面临一个根本性瓶颈：**高质量机器人操作数据极度稀缺**。与互联网规模的图文数据不同，机器人数据需要真实的物理交互和精确的动作标注，采集成本高昂。与此同时，互联网上存在海量的**野外人类操作视频**——烹饪、维修、装配等场景中蕴含着丰富的操作知识与运动模式，但这些视频几乎完全不包含动作标签，无法直接用于VLA的监督训练。

### 重建驱动范式的局限

为了利用这些无标签视频，近期工作尝试通过**潜在动作**（latent actions）作为桥梁。其典型范式是**重建驱动**：先训练一个逆动力学模型（IDM）或正向动力学模型，从视频帧中提取一个紧凑的潜在动作表示，然后要求该表示能够重建未来的视觉观测。最具代表性的工作是 **LAPA**（Ye et al., IJCV 2025），它通过多阶段管线，利用动力学重建从人类视频中提取潜在动作作为伪标签，再供VLA学习。

然而，这一范式存在两个关键缺陷：

1. **噪声引入**：像素级重建目标迫使潜在动作编码大量与任务无关的视觉细节（光照、纹理、背景），这些噪声信号会污染动作表征，削弱其行为中心性。
2. **效率低下**：多阶段训练管线（先训练动力学模型，再生成伪标签，最后训练VLA）计算开销大，且各阶段之间的误差会逐级累积。

### 本文动机：从重建到对齐

本文提出一个核心洞察：**VLA真正需要的是隐式捕获于视觉动态中的运动信息，而非像素重建本身**。如果能将VLA的预测表征直接与从视频中导出的运动信号对齐，就可以绕过重建环节，以更高效且可控的方式扩展预训练。这一思路引出了两个关键问题：

- **如何定义“运动信号”？** 逆动力学模型从视频边界帧中提取的潜在动作天然编码了状态转移信息，是理想的对齐目标。
- **如何实现统一学习？** 需要构建一个统一的潜在动作空间，使得有标签的实验室数据和无标签的野外视频能够在此空间中共同训练。

基于上述动机，本文提出了 **JALA（Joint-Aligned Latent Actions）**——一种联合对齐潜在动作范式，其核心是将VLA产生的预测嵌入与逆动力学模型导出的潜在动作直接对齐，从而同时从有标签和无标签人类视频中学习，迈向可扩展的野外VLA预训练。

## 核心方法与创新机理

JALA的核心创新在于**用联合对齐替代重建驱动**，构建了一个统一的潜在动作空间，使VLA能够同时从有标签实验室数据和无标签野外人类视频中高效学习。这一范式转换体现在四个关键的“changed slots”上。

### 从重建驱动到联合对齐

现有方法（如**LAPA**, Ye et al., IJCV 2025）依赖多阶段重建管线：先通过逆动力学模型从视频中提取潜在动作，再训练正向动力学模型以重建未来帧来约束这些潜在动作，最终将潜在动作作为伪标签供VLA学习。这一范式存在两个根本性瓶颈：**像素重建引入与任务无关的噪声**，且**多阶段管线效率低下、误差累积**。

JALA彻底舍弃了像素重建目标。其核心机制是：将VLA在掩码块预测过程中产生的预测嵌入 $h$ 与逆动力学模型（IDM）直接从边界帧导出的潜在动作 $z$ 进行**直接L1对齐**：

$$\mathcal{L}_{\mathrm{Align}} = \sum_{i=1}^{N} \sum_{k=1}^{K} \| h_{i,k} - z_{i,k} \|_1$$

这一设计的关键洞察在于：逆动力学模型已经通过视觉动态隐式捕获了帧间运动信息，无需通过重建来二次验证。直接对齐不仅消除了重建噪声，还使得预训练管线从多阶段简化为端到端的单阶段联合优化。

### 统一潜在动作空间：混合数据学习

重建驱动方法的另一局限是**无法有效利用无标签野外视频**——这些视频缺乏动作标注，而生成伪标签的质量又受限于重建精度。JALA通过联合对齐机制自然解决了这一问题：无论数据是否带有动作标签，逆动力学模型都能从边界帧中提取潜在动作作为监督信号。

具体而言，JALA的混合训练目标为：

$$\mathcal{L} = \mathbf{1}_{\mathrm{labeled}} \cdot \mathcal{L}_{\mathrm{MCP}} + \lambda \mathcal{L}_{\mathrm{Align}}$$

其中 $\mathcal{L}_{\mathrm{MCP}}$ 仅在数据带有动作标签时激活，而 $\mathcal{L}_{\mathrm{Align}}$ 始终活跃。这使得VLA能够在统一的潜在动作空间中同时从两类数据中学习：有标签数据提供精确的动作令牌监督，无标签野外数据则通过潜在动作对齐扩展行为多样性。t-SNE可视化（Figure 4）证实，预测嵌入与潜在动作在空间中紧密聚集，且野外样本大幅扩展了实验室数据的行为流形。

### 解耦EMA更新：稳定对齐架构

为支持联合对齐，JALA引入了一对对称但非对称更新的感知器模块：

- **Latent Action Perceiver (LAP)**：从边界帧 $(v_t, v_{t+\delta})$ 提取潜在动作 $z$，作为对齐目标。
- **Latent State Perceiver (LSP)**：将VLA预测上下文映射到同一潜在空间，产生预测嵌入 $h$。

二者通过解耦的指数移动平均（EMA）保持稳定：

$$\theta_b^{\mathrm{LAP}} \leftarrow \alpha \theta_b^{\mathrm{LAP}} + (1 - \alpha) \theta_b^{\mathrm{LSP}}$$
$$\theta_q^{\mathrm{LSP}} \leftarrow \alpha \theta_q^{\mathrm{LSP}} + (1 - \alpha) \theta_q^{\mathrm{LAP}}$$

其中LAP的骨干网络由LSP骨干缓慢更新，而LSP的查询向量则由LAP查询缓慢注入动作先验。消融实验表明，移除这一解耦更新机制会导致LIBERO成功率从96.9%骤降至56.6%，验证了其对训练稳定性的关键作用。

### 流匹配下游接口：从预测嵌入到机器人动作

传统VLA在下游任务中通常直接使用行为克隆令牌或扩散策略。JALA则利用预训练阶段产生的**预测嵌入**作为中间表征，配合流匹配头生成精确的机器人动作序列：

$$\mathcal{L}_{\mathrm{FM}} = \mathbb{E}_{\tau, \epsilon, A_t} \left[ \| V_{\theta}( \{h_{i,k}\}, A_t^{\tau}, q_t) - (\epsilon - A_t) \|_2^2 \right]$$

这一设计使得预训练阶段学到的行为表征能够高效迁移到机器人控制任务，无需重新训练整个VLA骨干。消融研究（Figure 6右）表明，使用第19层的预测嵌入作为流匹配输入可获得最佳迁移性能。

JALA 的核心理念是舍弃重建驱动的潜在动作范式，转而构建一个**联合对齐的潜在动作空间**。该空间由 VLA 产生的预测嵌入和逆动力学模型（IDM）导出的潜在动作共同定义，二者通过直接对齐形成统一表征，使模型能同时从有标签实验室数据和无标签野外人类视频中学习。

### 预训练阶段

预训练阶段由三个关键模块协同构成：

**Masked Chunk Prediction (MCP)** 负责在带标签数据上学习运动令牌分布。对于每个运动块，所有运动令牌被替换为 `[MASK]` 占位符，模型在块内使用双向注意力进行预测。其损失函数为：

$$\mathcal{L}_{\mathrm{MCP}} = -\sum_{i=1}^{N}\sum_{k=1}^{K}\log p_{\Theta}(a_{i,k} \mid A_{<i}, v, x)$$

**Latent Action Perceiver (LAP)** 是逆动力学模块的核心。对于每个运动块，LAP 接收起始帧和结束帧 $(v_t, v_{t+\delta})$，通过一组固定的可学习查询向量产生 $K$ 个潜在动作向量 $\{z_{i,1}, \dotsc, z_{i,K}\}$。这些潜在动作隐式编码了视觉动态中的运动信息，无需任何动作标签即可为无标签视频提供监督信号。

**Latent State Perceiver (LSP)** 与 LAP 参数共享，负责将 VLA 的预测上下文映射到同一潜在动作空间。LSP 注入初始帧上下文，其产生的预测嵌入 $h_{i,k}$ 与 LAP 的潜在动作 $z_{i,k}$ 通过 L1 损失直接对齐：

$$\mathcal{L}_{\mathrm{Align}} = \sum_{i=1}^{N}\sum_{k=1}^{K}\|h_{i,k} - z_{i,k}\|_{1}$$

为保持训练稳定性，LAP 和 LSP 之间采用**解耦 EMA 更新**机制：LAP 骨干权重由 LSP 骨干权重的指数移动平均更新（$\theta_b^{\mathrm{LAP}} \leftarrow \alpha\theta_b^{\mathrm{LAP}} + (1-\alpha)\theta_b^{\mathrm{LSP}}$），而 LSP 查询权重则由 LAP 查询权重的指数移动平均更新（$\theta_q^{\mathrm{LSP}} \leftarrow \alpha\theta_q^{\mathrm{LSP}} + (1-\alpha)\theta_q^{\mathrm{LAP}}$）。这种非对称更新使 LSP 逐步获得动作基础，同时避免对齐过程中的表示坍塌。

混合训练的总损失为：

$$\mathcal{L} = \mathbf{1}_{\mathrm{labeled}} \cdot \mathcal{L}_{\mathrm{MCP}} + \lambda\mathcal{L}_{\mathrm{Align}}$$

其中 $\lambda=0.5$，指示函数在有标签数据上激活 MCP 损失，而对齐损失在所有数据上始终活跃。这种设计使模型能够混合使用有标签实验室数据和大量无标签野外视频，无需为后者生成伪标签。

### 后训练阶段

预训练完成后，VLA 中间层产生的预测嵌入 $\{h_{i,k}\}$ 被馈入一个**流匹配头（Flow-Matching Head）**，用于下游机器人任务的动作生成。流匹配损失从预测嵌入和机器人状态学习去噪向量场：

$$\mathcal{L}_{\mathrm{FM}} = \mathbb{E}_{\tau,\epsilon,A_t}\left[\|V_{\theta}(\{h_{i,k}\}, A_t^{\tau}, q_t) - (\epsilon - A_t)\|_{2}^{2}\right]$$

### 数据流与模块关系

整体数据流可概括为：视觉输入经固定编码器（DINOv3 或 V-JEPA2）提取特征后，与指令令牌和运动令牌一同送入基于 InternVL3-2B 的 Transformer 骨干。在预训练中，掩码运动块的隐藏状态作为预测嵌入，与 LAP 从边界帧提取的潜在动作对齐；在后训练中，这些预测嵌入直接驱动流匹配头生成机器人动作序列。LAP-LSP 的解耦 EMA 更新贯穿整个预训练过程，确保潜在动作空间的一致性和稳定性。

![[assets/figures/papers/paper_list_l2259_https_arxiv_org_abs_2602_21736/figures/002_Figure_2.jpg]]
*Figure 2: The JALA framework. Pre-training (left): Hidden states of masked motion chunks serve as predictive embeddings to align with latent actions from boundary frames. The Latent Action Perceiver (LAP) maps boundary frames to latent action space, providing supervision without action labels. A parameter-shared Latent State Perceiver (LSP) injects initial frame context, with LAP and LSP linked via decoupled EMA update for stability. Post-training (right): The predictive embeddings are fed into a flow-matching head for robot task transfer*

### 3.1 基础VLA训练目标

JALA构建在基于Transformer的视觉-语言模型之上，该模型同时处理视觉令牌、指令令牌和运动令牌。其基础训练目标为最大化给定视觉-文本上下文下运动令牌序列的似然：

$$
\operatorname* { m a x } _ { \Theta } \sum _ { i = 1 } ^ { N } \log p ( A _ { i } \mid A _ { < i } , v _ { 1 } , x ; \Theta )
$$

其中 $A_i$ 表示第 $i$ 个运动块的动作令牌序列，$A_{<i}$ 为前序动作令牌，$v_1$ 为初始帧视觉输入，$x$ 为指令文本。

### 3.2 掩码块预测（Masked Chunk Prediction, MCP）

在预训练阶段，对于有标签数据，JALA采用块级掩码策略：将整个运动块中的所有动作令牌替换为 `[MASK]` 占位符，并在块内使用双向注意力。MCP损失定义为：

$$
\mathcal { L } _ { \mathrm { M C P } } = - \sum _ { i = 1 } ^ { N } \sum _ { k = 1 } ^ { K } \log p _ { \Theta } \big ( a _ { i , k } \mid A _ { < i } , v , x \big )
$$

其中 $a_{i,k}$ 为第 $i$ 个块中第 $k$ 个运动令牌，$K$ 为每块令牌总数（128个：手腕运动64令牌+手指运动64令牌）。该损失仅在带动作标签的数据上激活。

### 3.3 联合对齐损失（Joint Alignment Loss）

JALA的核心创新在于用联合对齐替代重建驱动范式。对于每个运动块，VLA在掩码位置产生的隐藏状态作为预测嵌入 $h_{i,k}$，而逆动力学模型（Latent Action Perceiver, LAP）从边界帧 $(v_t, v_{t+\delta})$ 提取潜在动作 $z_{i,k}$。两者通过L1损失直接对齐：

$$
\mathcal { L } _ { \mathrm { A l i g n } } = \sum _ { i = 1 } ^ { N } \sum _ { k = 1 } ^ { K } \| h _ { i , k } - z _ { i , k } \| _ { 1 }
$$

该损失始终激活，无论数据是否带有动作标签，从而统一有标签实验室数据和无标签野外视频的学习。

### 3.4 解耦EMA更新机制

为保持潜在动作空间的一致性，JALA引入Latent State Perceiver（LSP）与LAP配对，并通过解耦的指数移动平均（EMA）更新维持稳定性。

**LAP骨干权重更新**（用LSP骨干权重平滑LAP骨干）：

$$
\theta _ { b } ^ { \mathrm { L A P } } \leftarrow \alpha \theta _ { b } ^ { \mathrm { L A P } } + ( 1 - \alpha ) \theta _ { b } ^ { \mathrm { L S P } }
$$

**LSP查询权重更新**（用LAP查询权重注入动作先验到LSP）：

$$
\theta _ { q } ^ { \mathrm { L S P } } \leftarrow \alpha \theta _ { q } ^ { \mathrm { L S P } } + ( 1 - \alpha ) \theta _ { q } ^ { \mathrm { L A P } }
$$

其中 $\alpha$ 为EMA衰减系数。此非对称设计使LSP逐步获得动作基础，同时LAP骨干保持与预测上下文的一致性。消融实验证实，去除该解耦更新导致LIBERO成功率从96.9%骤降至56.6%，验证其稳定性必要性。

### 3.5 混合训练目标

预训练阶段的总体损失为MCP损失与对齐损失的加权组合：

$$
\mathcal { L } = \mathbf { 1 } _ { \mathrm { l a b e l e d } } \cdot \mathcal { L } _ { \mathrm { M C P } } + \lambda \mathcal { L } _ { \mathrm { A l i g n } }
$$

其中 $\mathbf{1}_{\mathrm{labeled}}$ 为指示函数（有标签时为1），$\lambda = 0.5$ 为对齐损失权重。此设计确保有标签数据同时受动作令牌监督和潜在动作对齐，无标签数据仅通过对齐损失学习。

### 3.6 后训练流匹配目标

在下游机器人任务迁移阶段，预训练的预测嵌入 $\{h_{i,k}\}$ 被馈入流匹配头（flow-matching head），从噪声分布学习去噪向量场以生成精确动作序列：

$$
\mathcal { L } _ { \mathrm { F M } } = \mathbb { E } _ { \tau , \epsilon , A _ { t } } \left[ \| V _ { \theta } ( \{ h _ { i , k } \} , A _ { t } ^ { \tau } , q _ { t } ) - ( \epsilon - A _ { t } ) \| _ { 2 } ^ { 2 } \right]
$$

其中 $\tau$ 为扩散时间步，$\epsilon \sim \mathcal{N}(0,I)$ 为噪声，$A_t^\tau$ 为加噪后的动作序列，$q_t$ 为机器人状态，$V_\theta$ 为预测的向量场。该模块仅在少量机器人数据上进行微调，实现从人手运动表征到机器人动作的高效迁移。

## 实验与关键发现

### 核心实验设置

JALA基于**InternVL3-2B**作为视觉语言骨干（28层注意力），视觉编码器可选**DINOv3**或**V-JEPA2**。运动块被分解为腕部与手指运动，分别量化为64个token，每块共128个token。预训练混合损失权重$\lambda=0.5$，优化器为AdamW（$\beta=(0.9,0.95)$）。

### 手部运动生成：联合对齐的预训练效果

Table 1展示了手部运动生成与预测任务在Lab和Wild两个分割上的性能。核心发现是**联合对齐机制在野外数据上带来了显著增益**：

- **JALA-dino**在Lab分割上MPJPE为7.16，Wild分割为11.02；对比仅用有标签数据的**Being-H0**（Lab: 7.61, Wild: 16.91），Wild上的提升达-5.89。
- **JALA-vjepa**同样表现一致（Lab: 7.05, Wild: 11.54），验证了方法的编码器无关性。

关键洞察：Being-H0在Wild分割上性能急剧退化（16.91），说明缺乏动作标签的野外数据无法被传统范式有效利用。JALA通过联合对齐，将Wild性能拉近至Lab水平，证明统一潜在动作空间成功吸收了无标签视频中的运动信息。

### 机器人操作：跨体现迁移的实证

**LIBERO双视图基准**（Table 2）上，JALA-dino以96.9%的平均成功率显著超越无对齐变体（87.6%，+9.3%）。值得注意的是，**LAPA†**（重建驱动方法，使用JALA骨干重新训练）仅达90.2%，低于JALA的联合对齐方案，直接验证了“对齐优于重建”的核心主张。

**LIBERO单视图**（Table 3）将JALA置于更广泛的方法谱系中。在≤3B参数级别，JALA-dino（91.4%）和JALA-vjepa（90.5%）均优于同尺寸模型。即便与>3B的大模型对比，JALA仍保持竞争力——这一结果尤为值得关注，因为JALA仅使用人类视频预训练，而**UniVLA-full††**额外引入了Bridge-V2机器人数据。

**RoboCasa与GR1桌面任务**（Table 4）进一步验证跨场景迁移能力。JALA-dino在GR1上达26.33%，对比Being-H0的12.91%，提升超过一倍（+13.42%）。这表明联合对齐学到的行为表征比单纯的动作令牌预测更具泛化性。

### 真实世界多步操作

真实机器人实验（Table 5）设置了三项多步任务：**Put-Three-Obj**（开抽屉→取放三个水果→关抽屉）、**Wipe-Board**（抓布→擦拭标记区域→清除墨迹）、**Water-Plant**（抓喷壶→转向植物→按压扳机）。每项任务包含可见与未见变体（Figure 8），未见变体引入桌布纹理、马克笔颜色等视觉偏移。

![[assets/figures/papers/paper_list_l2259_https_arxiv_org_abs_2602_21736/figures/013_Table_5.jpg]]
*Table 5: Real-world robot performance measured by average subtask completion rate (%) on three multi-step manipulation tasks. Each policy is evaluated over 10 rollouts per task*

JALA-dino在Put-Three-Obj可见设置下子任务完成率达60.0%，无对齐变体为48.0%（+12.0%）。Figure 10展示了未见设置下的鲁棒执行：Put-Three-Obj任务中策略纠正了初始空间错位，Wipe-Board任务中策略自适应地回访残留墨迹区域。

### 消融研究：关键设计选择

**解耦EMA更新的必要性**（Table 2）：去除解耦EMA更新（JALA w/o dec.）导致LIBERO成功率从96.9%骤降至56.6%，降幅达40.3个百分点。这一极端退化验证了LAP-LSP间的非对称EMA更新对训练稳定性的关键作用——没有解耦更新，对齐目标与预测上下文之间的分布偏移会破坏学习过程。

**潜在动作 vs 伪标签**（Table 1）：使用伪标签替代潜在动作的变体（JALA w/o latent）在Wild分割上性能显著低于无对齐变体（JALA w/o align），说明显式伪标签引入的噪声比完全不使用野外数据更有害。联合对齐通过隐式表征空间的对齐规避了伪标签的误差累积问题。

**野外数据比例**（Figure 6左）：下游LIBERO成功率随预训练中野外数据比例从0%到100%单调提升，证实了野外数据的增量价值——更多样化的人类操作视频持续改善机器人任务迁移。

**预测嵌入层选择**（Figure 6右）：使用第19层隐藏状态作为流匹配输入获得最佳迁移性能，而更浅（14层）或更深（24、28层）均导致性能下降。这表明中间层在行为表征的抽象程度与任务相关性之间达到了最优平衡。

### 失败模式分析

真实机器人实验揭示了JALA的三类典型失败（Figure 11）：

![[assets/figures/papers/paper_list_l2259_https_arxiv_org_abs_2602_21736/figures/016_Figure_11.jpg]]
*Figure 11: Failure cases across real-robot tasks. Put-Three-Obj: spatial misalignment, incomplete contact, and unstable grasp. Wipe-Board: insufficient planar contact and persistent residual ink. Water-Plant: incorrect affordance reasoning leading to wrong bottle orientation*

1. **空间错位与不完整抓取**（Put-Three-Obj）：策略未能精确定位目标物体，导致抓取接触不充分或物体滑落。这暴露了潜在动作空间在精细空间推理上的局限。
2. **连续接触维持失败**（Wipe-Board）：擦拭过程中平面接触不足，或未能完全清除标记墨迹。说明模型对持续力控和视觉反馈闭环的理解不足。
3. **功能推理错误**（Water-Plant）：策略错误地定向喷壶，将喷嘴对准非目标方向。这涉及对工具功能语义的推理，超出了当前预训练数据的覆盖范围。

这些失败模式指向一个共同瓶颈：**联合对齐学到的是运动层面的行为表征，而非任务级的物理交互推理**。在需要精确空间对齐、持续接触维持和工具功能理解的场景中，仅靠运动先验不足以产生鲁棒策略。

### 方法谱系与知识库定位

JALA在VLA预训练方法谱系中占据独特位置：

- 相对于**Being-H0**（Luo et al., arXiv 2025）：JALA突破了“仅使用有标签实验室数据”的限制，通过联合对齐将无标签野外视频纳入预训练，在Wild分割上实现-5.89 MPJPE的增益。
- 相对于**LAPA**（Ye et al., IJCV 2025）：JALA舍弃了重建驱动的多阶段管线，以端到端的对齐机制替代正向动力学重建，在LIBERO上以96.9% vs 90.2%的优势验证了对齐范式的效率优势。
- 相对于**UniVLA**（UniVLA Team, arXiv 2024）：JALA在仅使用人类视频预训练的条件下，以更小的模型规模（≤3B）达到与引入机器人数据的大模型（>3B）相当的性能，展示了数据效率的优势。

JALA的核心贡献在于**将VLA预训练从“需要动作标签”的约束中解放出来**，构建了一个行为中心的统一潜在动作空间。这一范式转换使大规模野外人类视频成为VLA预训练的有效数据源，为数据稀缺的机器人学习开辟了可扩展的路径。

![[assets/figures/papers/paper_list_l2259_https_arxiv_org_abs_2602_21736/figures/004_Table_1.jpg]]
*Table 1: Comparison of hand motion generation and prediction tasks on both Lab and Wild splits*

![[assets/figures/papers/paper_list_l2259_https_arxiv_org_abs_2602_21736/figures/006_Figure_5.jpg]]
*Figure 5: Qualitative hand-motion generation on lab (left column) and wild (right column) scenes. Colored overlays denote generated hand poses*

![[assets/figures/papers/paper_list_l2259_https_arxiv_org_abs_2602_21736/figures/010_Figure_6.jpg]]
*Figure 6: Ablation studies on JALA-dino evaluated on LIBERO. Left: performance across various the proportion of in-the-wild data used during pretraining (0%, 25%, 50%, 100%). Right: performance when feeding hidden states from different backbone layers (14, 19, 24, 28) into the flow-matching head during adaptation*

## 定位与知识库关联

### 1. 方法谱系：从重建驱动到联合对齐

JALA 的核心贡献在于重新定义了 VLA 预训练中潜在动作的获取方式。此前，以 **LAPA**（Ye et al., IJCV 2025）为代表的重建驱动范式占据主流：先通过逆动力学模型从视频中提取潜在动作，再训练正向动力学模型以重建未来帧来约束潜在动作质量，最终将潜在动作作为伪标签用于 VLA 训练。这一多阶段管线存在两个瓶颈：（1）重建目标引入的噪声与任务无关，效率低下；（2）伪标签生成与 VLA 训练解耦，误差逐级累积。

JALA 直接舍弃像素重建，转而采用**联合对齐**：在 VLA 预测上下文的同时，将中间隐藏状态（预测嵌入 $h$）与逆动力学模型（IDM）导出的潜在动作 $z$ 进行 L1 对齐。这一设计将潜在动作的获取与 VLA 的预测过程耦合为单一优化目标，无需伪标签，也无需多阶段训练。

与 **Being-H0**（Luo et al., arXiv 2025）相比，Being-H0 仅使用带动作标签的实验室数据进行预训练，无法利用大规模无标签野外视频。JALA 通过统一的潜在动作空间，使有标签实验室数据和无标签野外视频能够混合训练——有标签时启用掩码块预测损失 $\mathcal{L}_{\mathrm{MCP}}$，无标签时仅使用对齐损失 $\mathcal{L}_{\mathrm{Align}}$，两者共享同一 Transformer 骨干。

在模型规模与架构上，JALA 与 **UniVLA**（UniVLA Team, arXiv 2024）同属 Transformer-based VLA 路线，但 UniVLA 依赖显式动作标签或伪标签进行跨 embodiment 迁移，而 JALA 的对齐机制天然支持无标签数据，在数据效率上具有本质优势。Table 3 显示，JALA-dino（≤3B 参数）在单视图 LIBERO 上达到 96.9% 的平均成功率，与更大模型（>3B）相比仍具竞争力。

### 2. 关键设计决策与适用边界

**解耦 EMA 更新的必要性。** JALA 引入 Latent Action Perceiver（LAP）和 Latent State Perceiver（LSP）两个模块，通过非对称指数移动平均（EMA）保持对齐稳定性：LAP 骨干权重由 LSP 骨干权重更新（$\theta_b^{\mathrm{LAP}} \leftarrow \alpha\theta_b^{\mathrm{LAP}} + (1-\alpha)\theta_b^{\mathrm{LSP}}$），LSP 查询权重由 LAP 查询权重更新（$\theta_q^{\mathrm{LSP}} \leftarrow \alpha\theta_q^{\mathrm{LSP}} + (1-\alpha)\theta_q^{\mathrm{LAP}}$）。消融实验表明，去除解耦 EMA 后 LIBERO 成功率从 96.9% 骤降至 56.6%，验证了这一设计的必要性。这意味着 JALA 的对齐效果高度依赖 LAP/LSP 之间的动量耦合，在需要频繁切换视觉域的场景中，EMA 系数的选择可能成为敏感超参数。

**预测嵌入层选择的任务依赖性。** Figure 6 右显示，使用第 19 层的隐藏状态作为流匹配输入可获得最佳迁移性能，而非最深层（第 28 层）。这暗示中间层保留了更具迁移性的运动表征，而深层特征可能过度拟合预训练任务。对于与预训练域差异较大的下游任务，最优层选择可能需要重新校准。

**视觉编码器的敏感性。** JALA-dino（使用 DINOv3）和 JALA-vjepa（使用 V-JEPA2）在野外分割上的 MPJPE 分别为 11.02 和 11.54（Table 1），差异虽小但存在。方法依赖固定视觉编码器提取边界帧特征，对视觉特征质量和域差异可能敏感——当野外视频的视觉分布与编码器训练分布偏差较大时，IDM 提取的潜在动作质量可能下降，进而影响对齐效果。

### 3. 适用边界与局限

**已知失败模式。** 真实世界实验中，JALA 在以下场景仍出现失败（Figure 11）：
- **空间错位与不完整抓取**（Put-Three-Obj）：需要精细空间对齐的任务中，策略可能产生错误的抓取位置或无法维持稳定接触。
- **连续接触维持不足**（Wipe-Board）：擦拭任务中，策略可能无法保持足够的平面接触力，导致残留墨迹。
- **错误功能推理**（Water-Plant）：喷壶任务中，策略可能以错误方向握持瓶子，表明对工具 affordance 的理解不足。

这些失败指向一个共同瓶颈：JALA 从人手视频中学习的潜在动作空间，在需要精确工具使用和持续物理接触的任务上泛化能力有限。当前预训练数据（UniHand-Mix）虽包含 2.5M 野外样本，但可能仍不足以覆盖极端多样性的操作场景。

**数据覆盖的隐性假设。** JALA 假设野外人手视频与机器人操作之间存在可迁移的运动模式。当目标机器人任务涉及人手视频中罕见的动作类型（如精确力控、工具铰接操作）时，对齐机制可能无法提供有效监督。这一假设的边界尚未被系统验证。

### 4. 开放问题

1. **跨视角泛化。** 当前 UniHand-Mix 以第一人称人手视频为主。联合对齐机制能否推广到第三人称或固定视角的人类活动视频，是扩展数据来源的关键问题。

2. **完全无标签的自监督扩展。** JALA 仍依赖部分有标签实验室数据来训练 MCP 损失。能否在完全无标签的视频上，通过自监督方式进一步提升潜在动作的表征质量（例如引入对比学习或掩码自编码器），值得探索。

3. **移动操作与双手协调。** 当前实验集中在桌面操作和单手机器人任务。JALA 的对齐框架是否适用于移动操作或高自由度双手协调任务，需要验证。

4. **自适应超参数选择。** 预测嵌入层选择（Figure 6 右）和 EMA 系数对下游性能影响显著。如何自动确定最优配置以适应不同下游任务，是一个工程上重要但尚未解决的问题。

5. **与更大模型的 scaling 行为。** Table 3 显示 JALA 在 ≤3B 规模下已具竞争力，但其性能随模型规模增长的 scaling 行为尚未被系统研究——特别是联合对齐机制在大模型下是否仍能保持稳定。

## 原文 PDF

![[paperPDFs/CVPR_2026/Joint_Aligned_Latent_Action_Towards_Scalable_VLA_Pretraining_in_the_Wild.pdf]]
