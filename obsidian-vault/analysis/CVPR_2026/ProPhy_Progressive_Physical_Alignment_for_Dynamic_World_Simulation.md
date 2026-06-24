---
title: "ProPhy: Progressive Physical Alignment for Dynamic World Simulation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/ProPhy_Progressive_Physical_Alignment_for_Dynamic_World_Simulation.pdf
project_link: "https://zijunwa.github.io/prophy/"
code_link: null
aliases:
- ProPhy
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/representation_self_supervised_transfer
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 渐进式物理对齐框架中的双层物理专家混合机制（语义专家块与细化专家块）及基于视觉语言模型（VLM）的细粒度物理空间对齐策略。
primary_logic: 通过语义路由器从文本中提取全局物理语义，并利用细化路由器与 VLM 注意力图进行 token 级空间对齐，使生成模型能够对不同空间区域施加各向异性的物理约束，从而实现动态、物理一致的视频生成。
claims:
- 提出的两阶段 MoPE 机制显式提取分层物理先验（语义级和 token 级），克服了以往方法全局、隐式的物理建模。
- 利用 VLM 的细粒度空间定位能力，通过物理对齐策略将 VLM 的空间分布迁移到细化路由器，实现了 token 级别的物理现象定位。
- 在 VideoPhy2 基准上，ProPhy 显著优于所有对比方法，尤其在 Joint（物理一致性综合）指标上对 CogVideoX 带来 +19.7% 的相对提升。
- 消融实验证明，物理分支（SEB+PB+REB）比简单的 LoRA 微调带来更大增益，且完整的损失组合（语义对齐+细粒度对齐+负载均衡）达到最优性能。
---

# ProPhy: Progressive Physical Alignment for Dynamic World Simulation

> [!tip] 核心洞察
> 通过语义路由器从文本中提取全局物理语义，并利用细化路由器与 VLM 注意力图进行 token 级空间对齐，使生成模型能够对不同空间区域施加各向异性的物理约束，从而实现动态、物理一致的视频生成。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向动态世界模拟的渐进式物理对齐框架 |
| 英文题名 | ProPhy: Progressive Physical Alignment for Dynamic World Simulation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.05564) · [Project](https://zijunwa.github.io/prophy/) |
| Topic | #topic/vision_multimodal_applications #topic/representation_self_supervised_transfer #topic/vision_multimodal_applications/image_and_video_generation |
| Method | ProPhy |
| Dataset | VideoPhy2, VBench |

> [!tip] 效果简介
> - VideoPhy2 (ALL set) 上，Physical Correctness (PC) / Semantic Alignment (SA) / Joint 65.0 / 32.0 / 26.5 (Wan2.1‑1.3B + ProPhy) vs 57.8 / 30.0 / 24.8 (Wan2.1‑1.3B) (+7.2 / +2.0 / +1.7)；Joint (相对提升) CogVideoX‑5B + ProPhy vs CogVideoX‑5B (+19.7% 相对提升)。
> - VBench 上，Quality Score 81.0 (CogVideoX‑5B + ProPhy) vs 76.8 (CogVideoX‑5B) (+4.2)。

## 概述

视频生成模型在模拟真实世界动态场景时面临一个核心瓶颈：**现有方法缺乏显式物理引导与细粒度空间对齐**。主流扩散模型依赖隐式学习来捕捉物理规律，导致生成结果对物理提示产生“同质响应”——模型无法精确识别文本中不同空间区域对应的物理现象（如“刚体碰撞”与“流体飞溅”），因而频繁出现物理一致性错误。近期一些物理感知方法尝试引入视频级物理先验，但仍停留在粗粒度路由层面，将整段视频分配给单一专家，未能实现 token 级别的各向异性物理约束。

针对上述问题，本文提出 **ProPhy**——一个面向动态世界模拟的渐进式物理对齐框架。其核心洞察在于：**通过语义路由器从文本中提取全局物理语义，并借助细化路由器与视觉语言模型（VLM）注意力图进行 token 级空间对齐，使生成模型能够对不同空间区域施加差异化的物理约束**，从而实现物理一致的视频生成。

ProPhy 的关键技术定位体现在三个层面：

1. **双层物理专家混合（MoPE）机制**：框架包含语义专家块（Semantic Expert Block, SEB）和细化专家块（Refinement Expert Block, REB）。SEB 在视频层面从文本提示中推断物理原理，通过语义路由器动态激活可学习物理基图，生成视频级物理增强潜变量；REB 则在 token 层面操作，通过细化路由器预测每个 token 的物理属性，使用 top‑k 专家机制注入细粒度物理先验。

2. **基于 VLM 的细粒度物理空间对齐**：利用 VLM 的跨模态定位能力，构建 token 级物理属性标签，并通过物理对齐策略将 VLM 的空间分布迁移到细化路由器，使生成模型首次具备 token 级别的物理现象定位能力。

3. **多目标物理对齐训练**：在标准扩散损失之外，引入语义对齐损失（$\mathcal{L}_{\text{coarse}}$）、细粒度对齐损失（$\mathcal{L}_{\text{fine-align}}$）和负载均衡损失（$\mathcal{L}_{\text{fine-balance}}$），形成端到端的物理感知优化目标。

实验结果表明，ProPhy 在物理相关视频生成基准上显著优于现有方法。在 **VideoPhy2** 基准上，ProPhy 对 CogVideoX‑5B 骨干网络在 Joint（物理一致性综合）指标上带来 **+19.7% 的相对提升**；对 Wan2.1‑1.3B 骨干网络，物理正确性（PC）从 57.8 提升至 65.0，语义对齐（SA）从 30.0 提升至 32.0。在 **VBench** 质量评估中，ProPhy 将 CogVideoX‑5B 的质量分数从 76.8 提升至 81.0。消融实验进一步证实，物理分支（SEB + PB + REB）相比简单 LoRA 微调带来显著增益，且完整的损失组合（语义对齐 + 细粒度对齐 + 负载均衡）达到最优性能。

## 背景与动机

### 视频生成中的物理一致性瓶颈

近年来，基于扩散模型的视频生成取得了显著进展，涌现出 **Wan2.1** (Team Wan et al., arXiv 2025)、**CogVideoX** (Yang et al., ICLR 2024)、**HunyuanVideo** (Kong et al., arXiv 2025) 等大规模骨干模型。然而，这些模型在生成涉及复杂物理交互的场景时，普遍暴露出一个关键瓶颈：**缺乏显式的物理引导与细粒度的空间对齐能力**。

具体而言，现有视频生成模型存在以下结构性缺陷：

1.  **同质化物理响应**：模型对文本中的物理线索（如“刚性碰撞”、“流体流动”）产生全局一致的响应，无法区分视频中不同空间区域应当遵循的不同物理规律。例如，一个场景中同时包含刚性物体和柔性布料，现有方法往往对整个视频施加单一、模糊的物理先验，导致局部物理行为失真。
2.  **隐式物理建模的局限性**：主流方法依赖扩散模型从大规模数据中隐式学习物理规律，缺乏可解释的物理先验注入机制。部分物理感知方法（如 **VideoREPA** (Zhang et al., NeurIPS 2025) 采用蒸馏策略，**WISA** (Wang et al., NeurIPS 2025) 使用混合物理专家）虽尝试引入物理引导，但多停留在视频级别的粗粒度路由，未能实现 token 级别的精细物理推理。
3.  **空间对齐缺失**：现有方法未建立文本物理语义与视频空间区域之间的显式对应关系，导致生成结果对物理提示呈各向同性响应，无法精确响应局部物理线索。

### 核心洞察：从全局隐式到局部显式的范式转变

针对上述瓶颈，ProPhy 提出了一个关键洞察：**物理一致的视频生成需要从“全局隐式建模”转向“局部显式对齐”**。具体而言，模型应当能够：

- 从文本中提取分层物理先验：既包括视频级别的全局物理语义（如“这是一个碰撞场景”），也包括 token 级别的局部物理属性（如“该像素区域正在发生弹性形变”）。
- 利用视觉语言模型（VLM）的细粒度空间定位能力，将物理现象的语义理解精确映射到生成过程中的空间区域，从而实现各向异性的物理约束。

这一洞察直接催生了 ProPhy 的**渐进式物理对齐框架**，其核心在于通过两阶段物理专家混合机制（MoPE）和基于 VLM 的空间对齐策略，使生成模型能够对不同空间区域施加差异化的物理约束，最终实现动态、物理一致的视频生成。

## 核心创新

ProPhy 的核心创新在于将**显式、分层的物理先验**注入视频扩散模型，并首次实现了 **token 级别的细粒度物理空间对齐**，从而解决了现有方法对物理提示产生全局同质响应、无法精确定位物理现象的根本瓶颈。其创新体系可归结为三个紧密耦合的 changed slots。

### 从隐式学习到显式两阶段物理专家混合

现有视频生成模型（如 **CogVideoX** (Yang et al., ICLR 2024)、**Wan2.1** (Team Wan et al., arXiv 2025)）或物理感知方法（如 **WISA** (Wang et al., NeurIPS 2025)）要么完全依赖扩散模型的隐式物理学习，要么仅在视频级别分配粗粒度物理专家，缺乏对物理原理的显式建模和细粒度推理能力。

ProPhy 提出了**两阶段物理专家混合机制（MoPE）**，由语义专家块（SEB）和细化专家块（REB）构成，分别在视频级和 token 级注入物理先验：

- **语义专家块（SEB）**：在视频级别操作。它包含一组可学习的物理基图 $\boldsymbol{B}_e$，通过语义路由器从文本提示中推断全局物理语义，动态激活相关基图并加权求和，生成视频级物理增强潜变量：

$$\tilde{\boldsymbol{X}} = \boldsymbol{X} + \sum_{e=1}^{E_s} \rho_p^e \boldsymbol{B}_e$$

- **细化专家块（REB）**：在 token 级别操作。对每个 token，细化路由器预测其所属的物理规律，通过 top‑k 专家选择机制施加各向异性的物理约束：

$$\tilde{\pmb{x}}' = \sum_{i \in \mathrm{argtop}_k \pmb{\rho}_r} \pmb{\rho}_r^i \mathbf{e}_\theta^i(\tilde{\pmb{x}})$$

这种分层设计使得模型能够同时捕捉场景的全局物理语义（如“这是一个弹性碰撞场景”）和局部物理属性（如“碰撞接触点附近 token 应遵循动量守恒”），从根本上克服了以往方法“一个视频一个物理标签”的粗糙建模。

### 基于 VLM 的 token 级物理空间对齐

这是 ProPhy 最具差异化的创新。此前没有任何方法在视频扩散模型的潜空间中建立 token 级别的物理属性监督。ProPhy 的关键洞察是：**视觉语言模型（VLM）具有比视频扩散模型（VDM）更强的物理现象空间定位能力**（见 Figure 4），可以将这种能力迁移到生成过程中。

具体策略包含两个层面：

1. **构建 token 级物理属性标签**：利用 VLM 提取物理现象的高显著性注意力区域，减去背景注意力图后获得 token 级别的物理属性标注（见 Figure 3）。这为细粒度对齐提供了监督信号。

2. **多目标物理对齐训练**：在标准扩散损失 $\mathcal{L}_{\mathrm{diffusion}}$ 之上，引入三个物理对齐损失：

   - **语义对齐损失 $\mathcal{L}_{\mathrm{coarse}}$**：通过最小化批量内样本的语义路由权重余弦相似度矩阵 $P_s^{i,j}$ 与 WISA‑80K 标注的物理类别标签相似度矩阵 $Q_s^{i,j}$ 之间的 L2 距离，使同类物理现象的样本具有相近的路由分布：
   
   $$\mathcal{L}_{\mathrm{coarse}} = \sum_{1 \leq i < j \leq B} \| P_s^{i,j} - Q_s^{i,j} \|_2$$

   - **细粒度对齐损失 $\mathcal{L}_{\mathrm{fine-align}}$**：在 VLM 提取的高显著性区域 $M$ 上，最小化细化路由器输出投影与 token 级物理属性标签的 L2 距离，迫使细化路由器学会定位物理事件发生的空间位置。

   - **负载均衡损失 $\mathcal{L}_{\mathrm{fine-balance}}$**：防止细化专家退化到少数专家被过度激活的模式。

总训练损失为：

$$\mathcal{L} = \mathcal{L}_{\mathrm{diffusion}} + \lambda_1 \mathcal{L}_{\mathrm{coarse}} + \lambda_2 \mathcal{L}_{\mathrm{fine-align}} + \lambda_3 \mathcal{L}_{\mathrm{fine-balance}}$$

### 渐进式物理分支架构

ProPhy 的物理分支（Physical Branch）并非简单地叠加在骨干网络上，而是采用了**渐进式注入**设计：多个物理块（Physical Blocks, PB）穿插在扩散 Transformer 的各层之间，将 SEB 输出的物理先验逐层融合到视频潜变量中。每个 PB 采用与对应 Transformer Block 相同的架构并初始化其权重，确保物理信息的注入不会破坏原有的生成能力。消融实验（Table 3）证实，这一物理分支设计相比仅在骨干网络上进行 LoRA 微调，在物理正确性（PC）和综合指标（Joint）上均带来显著增益。

**证据强度**：上述三个 changed slots 均有充分的实验支撑——Table 1 显示 ProPhy 在 VideoPhy2 基准上对 CogVideoX‑5B 带来 +19.7% 的 Joint 相对提升；Table 3 和 Table 4 的消融实验验证了物理分支和完整损失组合的必要性；Figure 7 的细化路由器专家激活地图直观展示了 token 级物理定位的有效性。

## 整体框架

ProPhy 提出了一种**渐进式物理对齐**范式，将可学习的物理先验显式注入预训练视频扩散模型，并通过从视频级到 token 级的递进路由，实现对不同空间区域施加各向异性的物理约束。其核心设计动机源于一个关键瓶颈：现有视频生成模型缺乏显式物理引导和细粒度空间对齐，导致生成结果对物理提示产生同质响应，无法精确响应局部物理线索。

### 框架总览

ProPhy 建立在潜空间视频扩散骨干（如 **Wan2.1** 和 **CogVideoX**）之上，引入一个专用的 **物理分支（Physical Branch）**，与原始扩散 Transformer Block 并行工作。该物理分支包含三个核心模块：

1. **语义专家块（Semantic Expert Block, SEB）**：在视频级别操作，从文本提示中推断语义级物理原理，生成视频级物理增强潜变量。
2. **物理块（Physical Blocks, PB）**：采用与对应 Transformer Block 相同的架构并初始化其权重，渐进式地将 SEB 输出的物理先验融合到视频潜变量中。
3. **细化专家块（Refinement Expert Block, REB）**：在 token 级别操作，通过细化路由器预测每个 token 的物理属性，使用 top‑k 专家机制施加细粒度物理先验。

三个模块形成从粗到细的递进管线：SEB 先提取全局物理语义，PB 将其逐层注入潜空间，REB 再对每个 token 进行精细化物理属性分配。

### 推理流程

在推理阶段，模型端到端运行。给定文本提示，SEB 中的语义路由器首先根据提示中隐含的物理线索，动态激活一组可学习的物理基图，产生视频级物理增强潜变量 $\tilde{\boldsymbol{X}}$；该增强潜变量经 PB 注入骨干网络后，进入 REB，由细化路由器为每个 token 选择 top‑k 物理专家并加权聚合其输出，最终生成物理一致的视频。整个过程无需额外的推理时标注或外部模型干预。

### 训练目标

ProPhy 的训练目标在标准扩散损失 $\mathcal{L}_{\mathrm{diffusion}}$ 基础上，叠加三个物理对齐损失，形成多目标联合优化：

$$
\mathcal{L} = \mathcal{L}_{\mathrm{diffusion}} + \lambda_1 \mathcal{L}_{\mathrm{coarse}} + \lambda_2 \mathcal{L}_{\mathrm{fine-align}} + \lambda_3 \mathcal{L}_{\mathrm{fine-balance}}
$$

其中：
- $\mathcal{L}_{\mathrm{coarse}}$ 为**语义对齐损失**，通过最小化批量内样本语义路由权重的余弦相似度矩阵与物理类别标签矩阵之间的 L2 距离，使同类物理现象的样本具有相近的路由分布；
- $\mathcal{L}_{\mathrm{fine-align}}$ 为**细粒度对齐损失**，在 VLM 提取的高显著性区域上，最小化细化路由器输出与 token 级物理属性标签的 L2 距离，将 VLM 的细粒度物理定位能力迁移到生成过程；
- $\mathcal{L}_{\mathrm{fine-balance}}$ 为**负载均衡损失**，作用于细化路由器的输出，防止专家利用不均。

### 关键设计决策

与以往方法的核心区别在于两点：一是**两阶段 MoPE 机制**显式提取分层物理先验（语义级和 token 级），克服了以往全局、隐式的物理建模；二是**基于 VLM 的细粒度空间对齐策略**，利用 VLM 注意力图构建 token 级物理属性标签，使细化路由器能够准确定位物理现象发生的空间区域，实现各向异性的物理响应。消融实验证实，这一完整物理分支（PB+SEB+REB）相比仅在骨干网络上进行 LoRA 微调，在物理正确性、语义对齐和综合指标上均带来显著增益。

### 补充图表

![[assets/figures/papers/paper_list_l2135_https_arxiv_org_abs_2512_05564/figures/002_Figure_2.jpg]]
*Figure 2: Overview of our proposed ProPhy framework. ProPhy uses a progressive physical alignment design, consisting of the Semantic Expert Block and the Refinement Expert Block. During inference, the model runs end-to-end and aligns physics categories through our proposed blocks*

## 核心模块与公式推导

ProPhy 的核心在于一个**渐进式物理对齐框架**，其关键模块由**物理分支（Physical Branch）**承载，该分支并行于基础视频扩散模型的 Transformer Block，包含三个紧密协作的子模块：**语义专家块（Semantic Expert Block, SEB）**、**物理块（Physical Blocks, PB）**和**细化专家块（Refinement Expert Block, REB）**。整个框架的推理流程如 Figure 2 所示，模型端到端运行，通过上述模块实现从视频级语义到 token 级空间的物理类别对齐。

### 语义专家块（SEB）：视频级物理先验提取

SEB 在视频级别操作，负责从文本提示中推断全局物理语义。它包含一组可学习的物理基图 $\boldsymbol{B}_e \in \mathbb{R}^{C \times T \times H \times W}$，每个基图编码一种特定的物理知识维度。给定输入潜变量 $\boldsymbol{X}$，SEB 首先通过一个**语义路由器**（semantic router）从文本编码中预测每个物理基图的激活权重 $\rho_p^e$，然后通过加权求和的方式将物理先验注入潜变量，得到**视频级物理增强潜变量**：

$$ \tilde{\boldsymbol{X}} = \boldsymbol{X} + \sum_{e=1}^{E_s} \rho_p^e \boldsymbol{B}_e \tag{1} $$

其中 $E_s$ 为语义专家（即可学习物理基图）的数量，$\rho_p^e$ 为第 $e$ 个基图的软路由权重。这一设计使模型能够根据文本中隐含的物理线索（如“弹性碰撞”“流体飞溅”）动态激活不同的物理知识基元，而非对所有视频施加同质的物理约束。

### 物理块（PB）：渐进式物理信息注入

PB 采用与对应 Transformer Block 相同的架构并初始化其权重，其输出被顺序注入到视频潜变量中。这种渐进式设计使模型能够逐层累积物理信息，避免一次性注入带来的信息过载或与生成主干的冲突。PB 的存在是消融实验中物理分支显著优于简单 LoRA 微调的关键因素之一（Table 3）。

### 细化专家块（REB）：Token 级物理先验注入

REB 在 token 级别操作，实现对物理现象的细粒度空间定位。对于每个 token 的潜变量 $\tilde{\pmb{x}}$，REB 通过一个**细化路由器**（refinement router）预测该 token 所遵循的物理规律分布 $\pmb{\rho}_r$，然后选择 top‑$k$ 个最相关的细化专家，按其路由权重聚合输出：

$$ \tilde{\pmb{x}}' = \sum_{i \in \mathrm{argtop}_k \pmb{\rho}_r} \pmb{\rho}_r^i \, \mathbf{e}_\theta^i(\tilde{\pmb{x}}) \tag{2} $$

其中 $\mathbf{e}_\theta^i$ 为第 $i$ 个细化专家（由轻量 MLP 实现），$\mathrm{argtop}_k$ 选取路由权重最高的 $k$ 个专家。这一机制使不同空间位置的 token 可以受到不同物理规律（如刚性、流体、弹性）的约束，从而实现**各向异性**的物理响应——这正是 ProPhy 区别于以往全局物理建模方法的核心突破。

### 物理对齐目标：从语义到空间的层级监督

为使上述模块学到有意义的物理表征，ProPhy 引入了三个互补的对齐损失函数。

**语义对齐损失** $\mathcal{L}_{\mathrm{coarse}}$ 作用于 SEB 的语义路由器。对于批量大小为 $B$ 的样本，首先计算任意两个样本 $i$ 和 $j$ 的语义路由权重向量之间的余弦相似度，构建预测相似度矩阵 $P_s$：

$$ P_s^{i,j} = \frac{\pmb{\rho}_s^{(i)} \cdot \pmb{\rho}_s^{(j)}}{\lVert \pmb{\rho}_s^{(i)} \rVert \, \lVert \pmb{\rho}_s^{(j)} \rVert} \tag{3} $$

然后利用 WISA‑80K 数据集中每个视频的物理类别标注向量构建标签相似度矩阵 $Q_s$，通过最小化两者的 L2 距离，使具有相同物理现象的视频获得相近的路由分布：

$$ \mathcal{L}_{\mathrm{coarse}} = \sum_{1 \leq i < j \leq B} \| P_s^{i,j} - Q_s^{i,j} \|_2 \tag{4} $$

消融实验表明，将此相对距离损失替换为 BCE 损失会提升语义对齐（SA）但削弱物理正确性（PC）和综合指标（Joint），验证了相对距离公式的有效性。

**细粒度对齐损失** $\mathcal{L}_{\mathrm{fine-align}}$ 作用于 REB 的细化路由器。ProPhy 利用 VLM 的注意力图提取 token 级物理属性标签 $\mathcal{Q}_r$（标注流水线见 Figure 3），并在 VLM 识别的高显著性区域 $M$ 上，最小化细化路由器输出投影 $\mathcal{P}'_r$ 与标签的 L2 距离：

$$ \mathcal{L}_{\mathrm{fine-align}} = \sum_{M^{i,e}=1} \| {\mathcal{P}'}_r^{i,e} - \mathcal{Q}_r^{i,e} \|_2 \tag{5} $$

这一策略将 VLM 的细粒度物理定位能力迁移到生成过程中——Figure 4 的对比显示，VLM 的注意力图在定位物理现象区域方面显著优于 VDM 自身的交叉注意力图。

![[assets/figures/papers/paper_list_l2135_https_arxiv_org_abs_2512_05564/figures/004_Figure_4.jpg]]
*Figure 4: Study of the attention localization capabilities of VDM and VLM. The VDM cross-attention maps are obtained by adding 10% noise and then denoising. As shown, despite minor imperfections, the VLM-based approach more accurately identifies the locations of the corresponding physical phenomena*

**负载均衡损失** $\mathcal{L}_{\mathrm{fine-balance}}$ 为标准辅助损失，施加于细化路由器的输出，防止少数专家被过度激活而其余专家退化。消融实验（Table 4）表明，仅使用绝对对齐损失而无负载均衡会导致性能退化，仅使用负载均衡损失虽提升 SA 但削弱 PC，完整损失组合达到最优。

### 总训练目标

最终优化目标将标准扩散损失与上述三个对齐损失结合：

$$ \mathcal{L} = \mathcal{L}_{\mathrm{diffusion}} + \lambda_1 \mathcal{L}_{\mathrm{coarse}} + \lambda_2 \mathcal{L}_{\mathrm{fine-align}} + \lambda_3 \mathcal{L}_{\mathrm{fine-balance}} \tag{6} $$

其中 $\lambda_1$、$\lambda_2$、$\lambda_3$ 为平衡各损失项权重的超参数。这一多目标训练框架使 ProPhy 在保持生成质量的同时，实现了从全局语义到局部 token 的双层物理对齐。

### 补充图表

![[assets/figures/papers/paper_list_l2135_https_arxiv_org_abs_2512_05564/figures/003_Figure_3.jpg]]
*Figure 3: Pipeline for annotating token-level physical attributes using a VLM*

![[assets/figures/papers/paper_list_l2135_https_arxiv_org_abs_2512_05564/figures/008_Figure_7.jpg]]
*Figure 7: Refinement router expert maps. High-activation regions accurately localize where corresponding physical events occur, demonstrating the REB’s fine-grained physical alignment*

## 实验与分析

### 主实验结果

ProPhy 在两个核心基准上均展现出显著的物理一致性提升，同时保持了基础模型的生成质量。

**VideoPhy2 基准。** 该基准从物理正确性（Physical Correctness, PC）、语义对齐（Semantic Alignment, SA）及二者的综合得分（Joint）三个维度评估视频生成的物理合理性。Table 1 报告了主要对比结果。以 CogVideoX-5B 为骨干网络时，ProPhy 在 Joint 指标上带来 **+19.7% 的相对提升**，在所有对比方法中取得最优或次优成绩。以 Wan2.1-1.3B 为骨干网络时，ProPhy 将 PC 从 57.8 提升至 65.0（+7.2），SA 从 30.0 提升至 32.0（+2.0），Joint 从 24.8 提升至 26.5（+1.7）。值得注意的是，ProPhy 在 Wan2.1-1.3B 上的 Joint 得分（26.5）已超越更大规模的基线模型 HunyuanVideo（13B 参数，Joint 26.3），表明物理先验的显式注入比单纯增大模型规模更有效地提升了物理一致性。

**VBench 质量基准。** Table 2 表明 ProPhy 在增强物理一致性的同时并未牺牲生成质量。CogVideoX-5B + ProPhy 的 Quality Score 达到 81.0，相比原始 CogVideoX-5B（76.8）提升 +4.2。其中，Dynamic Degree 维度的改善尤为突出，这与 ProPhy 通过细化专家块实现 token 级物理约束的设计目标一致——模型能够在不同空间区域施加各向异性的物理响应，从而生成更丰富的动态变化。

与现有物理感知方法的对比进一步验证了 ProPhy 的优势。在 VideoPhy2 上，ProPhy 在 PC 和 Joint 指标上均优于基于蒸馏策略的 **VideoREPA**（Zhang et al., NeurIPS 2025）、基于混合物理专家的 **WISA**（Wang et al., NeurIPS 2025）以及基于分层偏好优化的 **PhysHPO**（Chen et al., NeurIPS 2025）。这些方法或采用视频级物理路由，或依赖隐式物理对齐，而 ProPhy 的两阶段 MoPE 机制能够在语义级和 token 级两个粒度上显式建模物理先验，是其性能优势的关键来源。

### 消融实验

消融实验以 Wan2.1-1.3B 为骨干网络，系统验证了各组件和损失函数的贡献（Table 3 与 Table 4）。

![[assets/figures/papers/paper_list_l2135_https_arxiv_org_abs_2512_05564/figures/009_Table_3.jpg]]
*Table 3: Ablation study results on ProPhy with Wan2.1-1.3B as the base model. LoRA indicates that the Physical Branch is removed, and LoRA is applied to the backbone*

![[assets/figures/papers/paper_list_l2135_https_arxiv_org_abs_2512_05564/figures/011_Table_4.jpg]]
*Table 4: Ablation study on the roles of relative loss and absolute loss during training*

**物理分支的贡献。** 将完整的物理分支（PB + SEB + REB）与仅在骨干网络上进行 LoRA 微调（无物理分支）进行对比。结果显示，LoRA 微调仅带来微弱增益（PC 57.8 → 58.2），而引入物理分支后 PC 跃升至 65.0，SA 和 Joint 也同步提升。这证明物理一致性的改善并非来自简单的参数适配，而是源于显式物理先验的注入与对齐。

**损失函数的作用。** 在 SEB 中，将基于余弦相似度的相对距离损失（L_coarse）替换为 BCE 损失后，SA 略有上升但 PC 和 Joint 均下降，表明相对距离公式通过批量内样本间的语义关系约束，比逐样本分类损失更有效地引导语义物理先验的学习。在 REB 中，仅使用绝对对齐损失（L_fine-align）而移除负载均衡损失（L_fine-balance）会导致性能退化；仅使用负载均衡损失虽能提升 SA，但削弱了 PC。完整的损失组合（L_diffusion + λ₁L_coarse + λ₂L_fine-align + λ₃L_fine-balance）在 PC、SA 和 Joint 三个指标上均达到最优，验证了多目标训练设计的必要性。

### 关键图表分析

**Figure 5 定性对比。** 在涉及复杂物理交互的场景中（如物体碰撞、流体运动、柔性体形变），CogVideoX 和 Wan2.1 生成的视频常出现物理定律违反（如物体穿透、不合理的运动轨迹），而 ProPhy 生成的视频在物理合理性和运动连续性上均有明显改善。这与定量结果中 PC 指标的大幅提升相互印证。

**Figure 7 细化路由器专家激活图。** 该图可视化了 REB 中不同物理专家的 token 级激活分布。高激活区域与视频中物理现象发生的空间位置高度吻合——例如，“碰撞”专家在物体接触区域激活最强，“流体”专家在液体流动区域激活最强。这直接验证了基于 VLM 注意力图的细粒度对齐策略成功地将物理现象的定位能力迁移到了生成模型的 token 级路由中，使模型能够对不同空间区域施加差异化的物理约束。

**Figure 8 物理属性迁移实验。** 通过反转语义路由器的 logits（将“刚性”专家的权重与“柔性”专家的权重互换），原本应保持刚性的汽车车门在生成视频中出现了不合理的飘动。这一“专家反转”实验揭示了不同物理专家确实编码了可分离的、各向异性的物理先验，进一步佐证了 MoPE 机制的有效性和可解释性。

### 公平性说明

所有对比实验均在统一的训练数据（WISA-80K 子集）和评估协议下进行，针对不同骨干网络（Wan2.1、CogVideoX）进行了独立实验。然而，大模型（如 CogVideoX-5B）天然可能获得更高的绝对分数，论文未对模型参数量差异引入额外正则化，在跨模型规模比较时需注意这一因素。

### 失败模式与局限

尽管 ProPhy 在物理一致性上取得了显著提升，论文也明确指出以下局限：首先，用于物理现象标注的 VLM 注意力区域不可避免地包含噪声，且当前基于区域的物理分类仅能捕捉粗粒度的表层模式，可能限制更精细的物理推理能力。其次，框架尚未集成物理微分方程，物理知识注入的可解释性和原则性仍有提升空间。在极端物理场景（如多物体同时碰撞、复杂流体-固体耦合）中，ProPhy 的生成结果仍可能出现物理不一致，这与此类场景在训练数据中的稀疏性以及 VLM 标注精度的局限性有关。

### 补充图表

![[assets/figures/papers/paper_list_l2135_https_arxiv_org_abs_2512_05564/figures/005_Table_1.jpg]]
*Table 1: Results on VideoPhy2 benchmark. The best results are highlighted in bold, and the second-best results are underlined*

![[assets/figures/papers/paper_list_l2135_https_arxiv_org_abs_2512_05564/figures/006_Table_2.jpg]]
*Table 2: Results on VBench quality score. For each method, the best performance relative to its base model is highlighted in bold*

![[assets/figures/papers/paper_list_l2135_https_arxiv_org_abs_2512_05564/figures/007_Figure_5.jpg]]
*Figure 5: Qualitative comparison among ProPhy, CogVideoX, Wan2.1, and existing physics-aware methods*

![[assets/figures/papers/paper_list_l2135_https_arxiv_org_abs_2512_05564/figures/010_Figure_8.jpg]]
*Figure 8: Physical attribute transfer via expert inversion. Flipping semantic-router logits injects incorrect physical cues, causing implausible behaviors (e.g., a rigid car door fluttering), revealing that different experts encode distinct physical priors*

![[assets/figures/papers/paper_list_l2135_https_arxiv_org_abs_2512_05564/figures/012_Figure_6.jpg]]
*Figure 6: Analysis of the semantic router. r represents the Pearson correlation coefficient calculated between different distributions*

## 方法谱系与知识库定位

### 物理感知视频生成的演进脉络

ProPhy 所解决的问题根植于一个日益明确的共识：**现有视频生成模型缺乏显式物理引导和细粒度空间对齐**，导致生成结果对物理提示产生同质响应，无法精确响应局部物理线索。围绕这一瓶颈，近年来的工作从不同角度尝试将物理知识注入生成过程，形成了若干技术路线。

**隐式物理学习与蒸馏路线**。早期方法依赖扩散模型在训练数据中隐式习得物理规律，未引入显式物理先验。**VideoREPA**（Zhang et al., NeurIPS 2025）采用蒸馏策略，从预训练物理编码器中提取视频级物理表征来引导生成，但仍停留在全局物理约束层面。**PhysMaster**（Ji et al., arXiv 2025）则通过强化学习优化物理评分，以奖励信号间接塑造生成行为，其物理反馈的粒度和可解释性受限于奖励函数的设计。

**混合专家与分层偏好路线**。**WISA**（Wang et al., NeurIPS 2025）率先将 Mixture-of-Experts 思想引入物理感知生成，但其路由机制在视频级别分配专家，每个视频被整体指派到粗粒度物理类别，无法处理同一视频内不同空间区域存在不同物理现象的场景。**PhysHPO**（Chen et al., NeurIPS 2025）提出分层偏好优化，通过多级偏好对进行对齐，但仍缺乏 token 级的空间定位能力。**PISA**（Li et al., 2025）采用后训练策略注入物理知识，同样受限于全局物理建模的范式。

**ProPhy 的定位突破**。ProPhy 在上述谱系中首次实现了**从视频级物理语义到 token 级物理属性的分层显式建模**。其核心创新在于两阶段 MoPE 机制——语义专家块（SEB）提取全局物理原理，细化专家块（REB）通过 top‑k 路由对每个 token 施加各向异性的物理约束——以及基于 VLM 注意力图的细粒度空间对齐策略，将 VLM 的物理定位能力迁移到生成过程。这一设计使得 ProPhy 在 VideoPhy2 基准上对 CogVideoX-5B 带来 **+19.7% 的 Joint 指标相对提升**（Table 1），并在 VBench 质量分数上从 76.8 提升至 81.0（Table 2），同时保持了生成质量与物理一致性的双重优势。

### 适用边界与能力范围

ProPhy 的物理对齐能力建立在以下前提之上：**文本提示中包含可被语义路由器识别的物理线索**，且目标物理现象在 VLM 的视觉理解能力范围内。在 WISA-80K 所覆盖的物理类别（如刚性、重力、碰撞、流体等）上，框架表现出了稳定的物理一致性增益。然而，当物理现象超出标注数据分布或 VLM 的感知粒度时——例如涉及微观尺度的分子动力学或需要数值求解的连续介质力学场景——当前框架的物理注入仍停留在**表层模式匹配**层面，尚未集成支配性的物理微分方程。

此外，ProPhy 作为即插即用的物理分支设计，理论上可适配多种潜空间视频扩散骨干网络（已验证 **Wan2.1**（Team Wan et al., arXiv 2025）和 **CogVideoX**（Yang et al., ICLR 2024）），但其增益幅度与骨干模型的基座能力正相关：更大规模的骨干模型（如 CogVideoX-5B）天然具备更高的绝对分数上限，ProPhy 在其基础上带来的相对提升更为显著。

### 已知局限与开放问题

**标注噪声与粒度瓶颈**。当前用于物理现象标注的视频区域不可避免地包含噪声，且简单的区域级物理分类仅捕捉粗粒度表层模式。这限制了细化专家块对更精细物理推理的支持——例如，同一区域内同时发生的多物理场耦合（如流体-结构交互）难以被单一 token 级标签充分描述。

**物理可解释性的缺失**。框架虽通过专家激活图（Figure 7）展示了 token 级物理定位的可视化证据，但物理知识注入的形式仍是数据驱动的路由权重与可学习基图，缺乏与支配性物理定律（如 Navier-Stokes 方程、胡克定律）的显式关联。这引出了一个关键开放问题：**如何将对齐后的物理区域与物理偏微分方程相结合，以注入更具解释性和原则性的物理知识？**

**专家反转的泛化性**。Figure 8 展示了通过翻转语义路由器 logits 实现物理属性迁移（如将刚性车门变为柔性飘动），验证了不同专家确实编码了可区分的物理先验。但这一技术目前仅在“刚性”属性上得到验证，其能否泛化到流体、柔性体、断裂等其他物理属性，以及能否扩展到交互式编辑场景，仍是待探索的方向。

**与大规模物理世界模拟器的关系**。**Cosmos**（NVIDIA et al., arXiv 2025）等大规模物理世界模拟基线采用不同的技术路线（如基于物理引擎的合成数据训练），ProPhy 的数据驱动物理对齐策略与之形成互补而非替代关系。未来将 ProPhy 的细粒度对齐能力与物理引擎的精确约束相结合，可能是提升生成物理真实性的一条有前景的路径。

## 原文 PDF

![[paperPDFs/CVPR_2026/ProPhy_Progressive_Physical_Alignment_for_Dynamic_World_Simulation.pdf]]
