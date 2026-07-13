---
title: "MAMM: Motion Control via Metric-Aligning Motion Matching"
type: paper
paper_level: A
venue: SIGGRAPH
year: 2025
pdf_ref: paperPDFs/SIGGRAPH_2025/MAMM.pdf
project_link: https://ataga101.github.io/mamm-project-page/
code_link: null
aliases:
- MAMM
tags:
- SIGGRAPH_2025
- topic/motion_animation
- topic/motion_animation/human_motion_generation
core_operator: 通过最优传输框架优化域内距离结构对齐（Gromov-Wasserstein损失与Wasserstein损失的平衡），避免显式跨域映射，从根本上解决跨域对应问题。
primary_logic: 仅利用各域内部的距离（度量）即可实现跨域序列对齐，通过融合半非平衡Gromov-Wasserstein最优传输，在无监督下建立结构对应，从而支持多种控制模态。
claims:
- 本文方法仅考虑域内距离，无需手工定义映射或带标注数据进行训练。
- 使用融合半非平衡Gromov-Wasserstein（FSUGW）优化目标进行度量对齐。
- 该方法能在数秒内生成高质量对齐，无需大数据集和长时训练。
- 仅利用各域内部的距离（度量）即可实现跨域序列对齐，通过融合半非平衡Gromov-Wasserstein最优传输，在无监督下建立结构对应，从而支持多种控制模态。
---

# MAMM: Motion Control via Metric-Aligning Motion Matching

> [!tip] 核心洞察
> 仅利用各域内部的距离（度量）即可实现跨域序列对齐，通过融合半非平衡Gromov-Wasserstein最优传输，在无监督下建立结构对应，从而支持多种控制模态。

>[!思考] #ripe
>思考1：MAMM的training-free最优传输（FSUGW）能否用于motion rep，进行training-free或者learnable的multimodel (latent) mapping，从而获得更对齐的表征？这个过程，需要将整个dataset的motion进行单点轨迹化吗？目前的MAMM更像是基于选择好的motion sequence与control trajectory进行OPT，并没有在dataset层面进行matching（这也合理，因为control轨迹是任意的，而且training free，因此单个control 轨迹是能够对应复数的motion data的）
>`思考plus1`：MAMM如何扩展到dataset level的motion matching？如果不行，是否更合适的迁移是应用于retarget？只要两个subject的motion都能映射到同一个control trajectory/motion phase，自然就能做motion retarget。这个过程可以training-free，也可以构建learnable.
>
>思考2：motion phase本身就是种轨迹保证，不过偏向周期性。MAMM是否有机会将其扩充为非周期性？前提是找出motion phase路线在哪些任务上有巨大优势，才有价值继续研究。最好是一类或者多类任务，类似于MAMM能适配多种轨迹控制。

>[!TODO] #ripe
>从MoCapAnything v1 -> v2的优化过程，思考MAMM的优化，哪些部分能够换成learnable，然后能获得哪些新的能力，解决什么新问题？

| 字段      | 内容                                                                                                  |
| ------- | --------------------------------------------------------------------------------------------------- |
| 中文题名    | 基于度量对齐运动匹配的运动控制                                                                                     |
| 英文题名    | MAMM: Motion Control via Metric-Aligning Motion Matching                                            |
| 会议/期刊   | SIGGRAPH 2025                                                                                       |
| Links   | [paper](https://arxiv.org/abs/2505.19976) · [Project](https://ataga101.github.io/mamm-project-page/) |
| Topic   | #topic/motion_animation #topic/motion_animation/human_motion_generation                             |
| Method  | Metric-Aligning Motion Matching (MAMM)                                                              |
| Dataset | Mixamo/Adobe动画资产（运动序列）；手绘曲线、合成波形、音频、运动等控制序列（无需标准benchmark，单样本优化验证）                                  |

> [!tip] 效果简介
> 量化结果、消融证据与适用边界见“实验与关键发现”。

## 概要

**问题瓶颈**：传统运动控制方法依赖手工定义或学习得到的跨域映射，需要大规模配对数据集和耗时训练，难以处理任意控制序列对齐。

**核心洞察**：仅利用各域内部的距离（度量）即可实现跨域序列对齐。本文提出的 **Metric-Aligning Motion Matching (MAMM)** 通过融合半非平衡Gromov-Wasserstein（FSUGW）最优传输框架，在无监督下建立结构对应，无需显式跨域映射。

**方法定位**：MAMM 是一个统一的优化框架，接受草图、波形、标签、音频、运动等多种控制序列，仅需单个原始运动序列和控制序列即可在数秒内生成高质量对齐，无需任务特定训练或算法重新设计。其核心机制是通过最优传输优化域内距离结构对齐（Gromov-Wasserstein损失与Wasserstein损失的平衡），从根本上解决跨域对应问题。

**主要结果**：方法在多种控制模态下均能生成自然且结构一致的对齐运动，并通过消融实验验证了关键超参数（α、λ）对控制服从度与运动自然度的调节作用。

运动控制是计算机动画领域的核心挑战，其目标是根据给定的控制信号（如手绘曲线、音频、语义标签或另一段运动）驱动角色运动，使生成的运动既忠实于控制意图，又保持运动本身的自然性。这一任务在游戏、影视、虚拟人交互等场景中具有广泛需求。

### 问题本质：跨域序列对齐

运动控制的核心难点可归结为**跨域序列对齐问题**：给定一段原始运动序列 $X$ 和一个来自不同模态的控制序列 $Y$，需要生成一个新的运动序列 $X'$，使其在时间结构上与 $Y$ 对齐，同时保持 $X$ 的运动内容特征。这里的“域”可以是运动数据、音频特征、手绘轨迹、语义标签等任意模态，不同域之间的数据表示和距离度量存在本质差异。

### 现有方法的瓶颈

传统运动控制方法依赖**显式的跨域映射**，通常通过以下两种方式实现：

1. **手工定义映射规则**：针对特定控制模态设计特征对应关系（如音频节拍到运动节奏的映射），这类方法泛化能力差，每换一种控制模态就需要重新设计。
2. **学习跨域映射**：利用配对数据集训练神经网络（如音频到运动的回归模型），但获取大规模、高质量的配对标注数据成本极高，且训练耗时，难以快速适应新任务。

这两种路线的共同瓶颈在于：**它们都试图在原始域和控制域之间建立直接的对应关系**，而这种对应关系的建立要么依赖领域专家的手工设计，要么依赖大量标注样本的监督学习。当控制序列的类型发生变化（从音频变为草图，或从标签变为运动），整个映射机制需要推倒重来。

### 核心洞察：度量对齐的可能性

本文提出的关键洞察是：**仅利用各域内部的距离结构（度量），即可实现跨域序列对齐，而无需显式定义域间映射**。具体而言，如果控制序列 $Y$ 中两个时间点的特征相似，那么对齐后的运动 $X'$ 中对应时间点的姿态也应当相似——这种“结构保持”原则仅依赖于每个域内部的 pairwise 距离矩阵，不要求两个域之间存在任何预定义的对应关系。

这一思想将跨域对齐问题转化为**最优传输问题**：寻找一个传输计划 $T$，使得控制序列的内部距离结构与原始运动的内部距离结构尽可能一致。通过融合 Gromov-Wasserstein 损失（衡量结构对齐）与 Wasserstein 损失（保持运动内容），可以在无监督条件下建立结构对应，从而支持多种控制模态的统一处理。

### 本文动机与目标

基于上述洞察，本文提出 **Metric-Aligning Motion Matching (MAMM)**，一个统一的运动控制框架，其设计目标包括：

- **免训练、免标注**：仅需单个原始运动序列和控制序列，无需配对数据集或长时间训练，在数秒内生成对齐结果。
- **多模态统一**：支持草图、波形、标签、音频、运动等多种控制序列类型，无需针对不同任务重新设计算法。
- **用户可控**：通过软/硬关键帧机制，允许用户以直观方式指定对应关系或固定特定姿态。

这一框架从根本上绕开了传统方法对跨域映射的依赖，为运动控制提供了一种轻量、灵活且通用的解决方案。

## 核心方法与创新机理

MAMM的核心创新在于**从“学习跨域映射”转向“对齐域内度量”**，从而彻底规避了传统运动控制方法对配对数据和任务特定设计的依赖。这一转变通过三个关键changed slots实现：

---

### 1. 跨域对齐机制：从显式映射到度量对齐

传统方法（如基于学习的运动生成或音频驱动运动合成）通常需要**手工定义或从数据中学习跨域映射函数**，将控制信号显式地映射到运动空间。这种映射的建立依赖于大规模配对数据集和耗时的训练过程，且难以泛化到未见过的控制类型。

MAMM引入了**融合半非平衡Gromov-Wasserstein最优传输（FSUGW）**框架，仅利用各域内部的距离结构即可实现对齐。其核心思想是：通过优化传输计划 $T$，使得对齐后的运动块之间的成对距离矩阵与控制序列的成对距离矩阵相似，同时保持与原始运动的直接相似性。这一过程无需定义跨域映射，从根本上解决了跨域对应问题。

> *“our method uses metric alignment techniques based on the fused semi-unbalanced Gromov-Wasserstein (FSUGW) optimization objective”*

---

### 2. 控制序列类型支持：从任务特定到统一框架

现有方法的控制能力通常局限于特定目标域——例如运动到运动重定向、音频到舞蹈生成、或标签驱动运动合成——每种任务需要针对性地设计映射网络或优化目标。这种碎片化的设计使得系统难以扩展到新的控制模态。

MAMM提供了一个**统一的FSUGW优化框架**，支持**草图、波形、标签、音频、运动**等多种控制序列类型，无需针对不同任务重新设计算法。这一通用性的根本原因在于：FSUGW仅依赖控制序列内部的成对距离结构，而非控制信号的语义或模态特定特征。只要能为控制序列定义合适的域内距离函数（如草图的欧氏距离、音频的MFCC距离、运动关节距离），MAMM即可直接工作。

> *“a unified FSUGW-based optimization framework that aligns motions with a diverse range of control sequences without requiring task-specific training or algorithm redesign.”*

---

### 3. 数据需求：从大规模配对到单样本无监督

传统跨域运动控制方法依赖**大规模配对数据集**（如音频-运动对、文本-运动对）进行监督训练，或需要大量标注数据来学习映射关系。这一需求不仅增加了数据采集成本，也限制了方法在资源稀缺场景下的应用。

MAMM仅需**单个原始运动序列和单个控制序列**即可完成对齐，无需任何配对标注。其优化过程在数秒内完成，完全消除了对大规模数据集和长时间训练的依赖。这一能力的实现源于FSUGW的**无监督本质**：传输计划 $T$ 的优化仅基于域内距离结构的匹配，而非跨域监督信号。

> *“our method achieves high-quality alignments between a given motion and control sequence within seconds, eliminating the need for large datasets, extensive annotations, or prolonged training times”*

---

### 与最相关基线的差异

在概念上，MAMM与**GenMM**（Li et al., SIGGRAPH 2023）共享运动块（patch）操作的思想，但两者在任务定义和机制上有本质区别：GenMM通过双向相似度匹配在运动域内进行运动合成，而MAMM将任务推广至**任意控制序列与运动之间的跨域对齐**，并通过FSUGW框架实现了度量层面的结构对应，而非简单的相似度检索。

---

### 创新支撑的因果机制

这三个changed slots之间存在因果依赖关系：**FSUGW度量对齐机制**（slot 1）是核心使能技术，它天然地消除了对跨域映射和配对数据的需求，从而直接导致了**统一控制框架**（slot 2）和**单样本无监督能力**（slot 3）的实现。换言之，MAMM的通用性和数据效率并非独立设计，而是度量对齐范式的自然产物。

Metric-Aligning Motion Matching (MAMM) 是一个统一的优化框架，其核心思想在于：**仅利用原始运动域与控制序列域各自内部的距离（度量）结构，通过最优传输建立跨域对应，从而避免显式的跨域映射定义或配对训练数据**（Fig. 1）。给定任意原始运动序列 $X$ 和控制序列 $Y$，MAMM 输出对齐后的运动 $X'$，使 $X'$ 在保持原始运动内容的同时，其内部时序结构与 $Y$ 的结构相匹配（Fig. 2）。

![[assets/figures/papers/MAMM_Motion_Control_via_Metric-Aligning_Motion_Matching_234bebcdacd3/figures/002_Figure_2.jpg]]
*Figure 2: Intuitive concept of MAMM framework. Our framework optimizes transport plan ?? and aligned motion sequence $X ^ { \prime }$ , whose patch pairwise distance matrix is similar to that of control sequence $\boldsymbol { Y }$ , while resembling original motion ??

### 输入输出与数据表示

- **输入**：原始运动序列 $X$（由角色空间中的根位移 $\dot{V}_t$ 和关节旋转 $R_t$ 逐帧描述）以及控制序列 $Y$。控制序列可以是手绘曲线、一维波形、音频特征、语义标签或另一运动序列，无需针对不同模态重新设计框架。
- **输出**：对齐后的运动序列 $X'$，与 $X$ 具有相同的运动学表示格式，但帧间动态结构已与控制序列 $Y$ 对齐。

### 核心优化目标

框架将运动对齐问题形式化为**融合半非平衡 Gromov-Wasserstein（FSUGW）损失**的最小化（Fig. 3）：

$$L_{\mathrm{FSUGW}}(\tilde{X'}, \tilde{X}, \tilde{Y}, T) = \alpha \cdot L_{\mathrm{GW}}(\tilde{Y}, \tilde{X}, T) + (1-\alpha) \cdot L_{\mathrm{W}}(\tilde{X'}, \tilde{X}, T) + \lambda \cdot D_{\mathrm{KL}}(T^{\top} 1 \parallel b) - \epsilon \cdot H(T)$$

该目标函数由四项构成：
- **Wasserstein 损失 $L_W$**：通过传输计划 $T$ 约束对齐运动块 $\tilde{X'}$ 与原始运动块 $\tilde{X}$ 之间的直接距离，保持运动内容：
  $$L_W(\tilde{X'}, \tilde{X}, T) = \sum_{x_i' \in \tilde{X'}, x_k \in \tilde{X}} d_X(x_i', x_k) T_{i,k}$$
- **Gromov-Wasserstein 损失 $L_{GW}$**：比较控制序列块 $\tilde{Y}$ 与原始运动块 $\tilde{X}$ 的内部距离结构一致性，推动度量对齐：
  $$L_{GW}(\tilde{Y}, \tilde{X}, T) = \sum_{y_i,y_j \in \tilde{Y}, x_k,x_l \in \tilde{X}} |d_Y(y_i,y_j) - d_X(x_k,x_l)|^2 T_{i,k} T_{j,l}$$
- **边缘分布 KL 散度项**：以 $\lambda$ 为权重，软约束传输计划 $T$ 的边缘分布接近目标分布 $b$。
- **熵正则项**：以 $\epsilon$ 为系数，促进传输计划的平滑性。

参数 $\alpha$ 平衡对控制信号的服从度与运动自然度，$\lambda$ 控制运动块分布对原始运动的保真度。

### Pipeline 模块与交替优化

MAMM 的优化流程采用**由粗到精策略**与**FSUGW 块交替迭代**相结合的方式（Algorithm 1）：

1. **运动块提取（Motion Patch Extraction）**：将控制序列 $Y$、原始运动 $X$ 和对齐运动 $X'$ 以步长 1 帧分割为重叠的时间块，使优化在细粒度 patch 级别进行。
2. **由粗到精初始化**：从低分辨率开始，先仅最小化 $L_{GW}$ 项获得初始传输计划 $T$，再通过上采样逐级细化运动，为后续 FSUGW 优化提供良好起点。
3. **FSUGW 块交替优化**：在每一级分辨率上，交替执行以下步骤——
   - 固定 $X'$，优化传输计划 $T$；
   - 固定 $T$，通过混合操作更新 $X'$。
4. **软/硬关键帧约束**（可选）：用户可通过示例 patch 对指定对应关系（软关键帧），或固定特定帧段不变（硬关键帧），介入对齐细节。

### 方法定位

MAMM 在概念上与基于示例的运动合成方法 **GenMM**（Li et al., SIGGRAPH 2023）共享 patch 操作，但将任务从“运动到运动”的相似度匹配推广至**任意控制序列对齐**。其关键区别在于：GenMM 依赖双向相似度匹配，而 MAMM 通过 FSUGW 最优传输仅利用域内距离结构，无需手工定义跨域映射或大规模配对标注数据，可在数秒内完成高质量对齐。

### 问题形式化与运动表示

MAMM 将运动表示为角色空间中每一帧的根位移 $\Delta V_t$ 与关节旋转 $R_t$ 的组合 $[V_t, R_t]$（§3.1）。给定原始运动序列 $X$ 和控制序列 $Y$，目标是在不依赖跨域配对标注的前提下，生成与 $Y$ 结构对齐、同时保持 $X$ 运动内容的输出序列 $X'$。

核心思路是将该问题形式化为**融合半非平衡 Gromov-Wasserstein (FSUGW) 损失**的最小化（§3.2）。方法仅利用各域内部的成对距离（度量），无需手工定义跨域映射或进行有监督训练。

### 运动块提取 (Motion Patch Extraction)

为进行细粒度的结构对齐，MAMM 将 $X$、$X'$ 和 $Y$ 分别分割为步长为 1 帧的重叠时间块（patch），得到块集合 $\tilde{X}$、$\tilde{X'}$ 和 $\tilde{Y}$。原始运动的块大小设为 11 帧（30 fps 下约 0.37 秒），控制序列的块大小根据模态调整。

### Wasserstein 损失 ($L_W$)：保持运动内容

Wasserstein 损失通过传输计划 $T$ 建立对齐运动块 $\tilde{X'}$ 与原始运动块 $\tilde{X}$ 之间的直接对应，约束 $X'$ 在内容上接近 $X$：

$$L_W(\tilde{X'}, \tilde{X}, T) = \sum_{x_i' \in \tilde{X'}, x_k \in \tilde{X}} d_X(x_i', x_k) \, T_{i,k}$$

其中 $d_X(\cdot, \cdot)$ 是运动域内的距离度量，$T_{i,k}$ 表示块 $x_i'$ 传输到块 $x_k$ 的质量。该损失鼓励对齐后的运动块在原始运动块集合中找到近邻，从而保留运动的局部动态特征（§3.2.2）。

### Gromov-Wasserstein 损失 ($L_{GW}$)：驱动结构对齐

Gromov-Wasserstein 损失评估控制序列 $\tilde{Y}$ 与原始运动 $\tilde{X}$ 内部距离结构的一致性，是实现度量对齐的核心机制：

$$L_{GW}(\tilde{Y}, \tilde{X}, T) = \sum_{y_i,y_j \in \tilde{Y}, x_k,x_l \in \tilde{X}} \big| d_Y(y_i, y_j) - d_X(x_k, x_l) \big|^2 \, T_{i,k} \, T_{j,l}$$

该损失比较两个域内部的成对距离：若 $y_i$ 与 $y_j$ 在控制域中相距较远，则通过 $T$ 与之对应的运动块 $x_k$ 与 $x_l$ 在运动域中也应相距较远。通过最小化该损失，传输计划 $T$ 被推向“度量对齐”——即保持两个域内部距离结构的等距对应（§3.2.3）。这一设计使得 MAMM 无需定义跨域距离，从根本上规避了传统方法中手工设计映射或学习跨域对应的难题。

### FSUGW 统一优化目标

将 $L_W$ 与 $L_{GW}$ 融合，并加入边缘分布正则与熵正则，形成完整的 FSUGW 目标函数：

$$L_{\mathrm{FSUGW}}(\tilde{X'}, \tilde{X}, \tilde{Y}, T) = \alpha \cdot L_{GW}(\tilde{Y}, \tilde{X}, T) + (1-\alpha) \cdot L_{W}(\tilde{X'}, \tilde{X}, T) + \lambda \cdot D_{\mathrm{KL}}(T^{\top} \mathbf{1} \parallel b) - \epsilon \cdot H(T)$$

各组分含义如下（§3.2.4）：

- **$\alpha \in [0,1]$**：平衡结构对齐（$L_{GW}$）与内容保持（$L_W$）的权重。$\alpha$ 越大，对齐运动越忠实于控制序列的结构；$\alpha$ 过小（如 0.2）则运动自然但可能忽略控制输入，$\alpha=1.0$ 时可能导致运动段僵硬甚至静止。
- **$\lambda \cdot D_{\mathrm{KL}}(T^{\top} \mathbf{1} \parallel b)$**：软边缘分布约束，通过 KL 散度使传输计划 $T$ 的列和接近目标分布 $b$（原始运动块的分布）。$\lambda$ 控制该约束的强度：$\lambda=0$ 时运动可能包含不变姿态段，偏离原始动态；$\lambda \to \infty$ 时分布严格匹配原始运动，但可能牺牲对控制序列的响应。
- **$-\epsilon \cdot H(T)$**：熵正则项，促进传输计划的平滑性，避免过于稀疏的匹配。

### 交替优化与 FSUGW 块

FSUGW 目标的优化采用交替策略（Fig. 3），构成一个 **FSUGW 块**（§3.2.4）：

1. **提取块**：从当前 $X'$、$X$ 和 $Y$ 提取重叠 patch。
2. **优化 $T$**：固定 $X'$，通过投影梯度下降或 Sinkhorn 类算法优化传输计划。
3. **优化 $X'$**：固定 $T$，通过梯度下降更新对齐运动 $X'$，使其在满足传输计划的同时最小化 $L_W$ 项。

### 由粗到精优化 (Coarse-to-Fine Alignment)

为避免陷入局部最优，MAMM 采用由粗到精的多阶段优化策略（§3.2.5）。从低分辨率开始，初始传输计划 $T$ 仅通过最小化 $L_{GW}$ 项计算；随后逐级上采样，将上一阶段的输出 $X'^{k-1}$ 作为当前阶段的初始化，并应用 FSUGW 块进行细化。该策略在控制序列距离矩阵较复杂时（如运动到运动对齐场景）尤为关键，显著提升对齐质量。

### 软/硬关键帧约束 (Soft/Hard Keyframes)

MAMM 支持用户通过关键帧对对齐进行精细控制（§3.3.1）：

- **软关键帧**：用户指定示例 patch 对 $(X_{\mathrm{example}}, Y_{\mathrm{example}})$，方法将其追加到块分布中，并约束传输矩阵 $T$ 使示例 patch 的质量仅在其对应 patch 之间传输。这允许用户在正反两个方向上影响运动生成——靠近关键帧时生成对应姿态，远离时自动避开。
- **硬关键帧**：直接固定指定帧段的内容，强制对齐运动在特定时间位置完全匹配给定姿态。

![[assets/figures/papers/MAMM_Motion_Control_via_Metric-Aligning_Motion_Matching_234bebcdacd3/figures/001_Figure_1.jpg]]
*Figure 1: Overview of our method. Our method aligns given original motion to given control sequence. Our method can take arbitrary control sequences, such as sketches, labels, audio, and motions. Our method solely relies on within-domain distance in original and control, without needing manual definition of mapping or training with annotated data*

![[assets/figures/papers/MAMM_Motion_Control_via_Metric-Aligning_Motion_Matching_234bebcdacd3/figures/006_Figure_5.jpg]]
*Figure 5: Example of controlling aligned motion with soft keyframes. (a) Users can specify keyframe poses, such as "hands-up horse rider" and "hands-down horse rider," using our interface. For simplicity, users select poses from original sequence, although our method does not impose strict constraints on keyframe selection. (b) When motion curve approaches keyframe, algorithm ensures that corresponding poses in aligned motion closely match keyframe poses. (c) Conversely, when curve is distant from keyframe, algorithm selects alternative poses, such as "side-step" poses, which differ from keyframe poses. This illustrates how soft keyframes can influence motion in both positive and negative contexts. F...*

## 实验与关键发现

### 应用验证：多模态控制序列对齐

MAMM 的核心优势在于无需任务特定训练即可处理任意类型的控制序列。论文通过四类典型应用进行了定性验证：

**手绘曲线控制（Sketch-to-Motion）**：用户绘制二维曲线作为控制序列，角色运动自动跟随曲线的抽象结构（Fig. 4）。通过引入软关键帧机制，用户可在曲线上指定示例姿态对（如“举手骑马者”与“放手骑马者”），对齐后的运动在接近关键帧位置时生成对应姿态，远离时自动避开（Fig. 5）。这验证了 FSUGW 框架在连续空间信号与语义姿态约束联合驱动下的有效性。

**一维波形控制（Waveform-to-Motion）**：使用频率变化正弦波和中心交替正弦波分别控制舞蹈动作的频率与相位（Fig. 6）。运动自然跟随波形的周期性结构变化，证明度量对齐能够捕捉一维控制信号中的时序模式。

**音频驱动（Audio-to-Motion）**：在音乐控制舞蹈和语音控制手势（犬吠动作）两个场景中，运动与音频的强度、节拍及风格变化同步（Fig. 7）。音频数据以波形和 MFCC 特征表示，MAMM 仅利用域内距离即可建立结构对应，无需音频-运动配对数据集。

**运动到运动对齐（Motion-to-Motion）**：包括跨骨骼结构的步态对齐（不同骨架和风格的踏步序列匹配频率与相位）和非周期性战斗序列的时序同步（人与马的战斗动作对齐）（Fig. 8）。这是距离矩阵最复杂的场景，由粗到精优化策略在此尤为关键。

### 消融实验：超参数分析

MAMM 有两个关键超参数：α 平衡控制服从度与运动自然度，λ 控制运动块分布保真度。

**α 参数的影响**（Fig. 9）：固定 ε=0.05，λ=1.0。当 α 较小（如 0.2）时，$L_W$ 项占主导，生成的运动自然流畅，但偶尔忽略控制信号的风格变化；当 α 较大（如 1.0）时，$L_{GW}$ 项主导，部分运动段出现僵硬甚至静止现象。α 的实质作用是调节“保持原始运动内容”与“服从控制序列结构”之间的权衡。

**λ 参数的影响**（Fig. 10）：固定 α=0.8。当 λ 较小（如 0）时，对齐运动可能包含姿态不变的片段，偏离原始运动动态；当 λ 很大（如 →∞）时，对齐运动块的分布紧密匹配原始运动，但可能牺牲对控制序列的响应。λ 通过软边缘正则项 $D_{KL}(T^\top 1 \parallel b)$ 控制传输计划 T 的列和与目标分布 b 的接近程度。

**由粗到精优化的作用**：消融表明，当控制序列的距离矩阵较复杂（如运动到运动对齐）时，由粗到精策略对提高对齐质量尤为重要。从低分辨率开始提供良好初始化，通过逐级上采样细化运动，避免了直接在高维空间中优化陷入局部极值。

### 失败模式与局限性

1. **超参数手动调节**：α 和 λ 的最优值因任务而异，当前缺乏自动选择或自适应调整机制，用户需凭经验调试。

2. **距离矩阵缩放问题**：处理大规模多聚类数据时，缺乏通用的距离矩阵缩放策略，可能导致对齐失效。论文指出这是 FSUGW 框架在复杂数据结构上的已知挑战。

3. **可扩展性受限**：当前实现不适用于超过 10 万帧的数据集。面向大规模运动数据库时，需开发分层传输技术或 FSUGW 近似方法。

4. **实时性不足**：单次优化需数秒至数十秒，尚不能支持实时交互式控制。快速近似技术是未来实现实时 MAMM 的关键方向。

![[assets/figures/papers/MAMM_Motion_Control_via_Metric-Aligning_Motion_Matching_234bebcdacd3/figures/007_Figure_7.jpg]]
*Figure 7: (b) Gesture control by speech Fig. 7. Examples of motion controlled by audio data. We tested two scenarios: (a) dance movements controlled by music and (b) gestures (barking) controlled by speech. Here audio data is represented in both waveforms and MFCCs, but we only used MFCCs as input. Synchronization between motion and intensity, beat, or style of audio was observed. For more details, please refer to supplemental video*

*Figure 3: Explanation of the fused semi-unbalanced Gromov-Wasserstein (FSUGW) objective and algorithm to minimize it. ???? constrains $X ^ { \prime }$ to resemble ?? via transport plan ?? and ?????? encourages ?? to be metric-aligning, which leads to structural similarity between $X ^ { \prime }$ and ?? . We optimize FSUGW objective with alternating steps, where the first step optimizes ?? with $X ^ { \prime }$ fixed, and second step optimizes $X ^ { \prime }$ over fixed ??

![[assets/figures/papers/MAMM_Motion_Control_via_Metric-Aligning_Motion_Matching_234bebcdacd3/figures/008_Figure_8.jpg]]
*Figure 8: Examples of motion-to-motion alignment, where original motion is synchronized with control motion. First example aligns stepping motion to step with different skeletal structure and style, matching both frequency and phase. Second example aligns nonperiodic combat sequence involving human and horse, demonstrating synchronized timing of combat actions. Fig. 9. Aligned motions for various ?? values with ?? and ?? fixed to 0.05 and 1.0, respectively. Small ?? (e.g., 0.2) results in natural motion but occasionally ignores control inputs, such as style changes within the same segmentation label. Conversely, ?? value of 1.0 leads to aligned motions with segments that exhibit no movement*

![[assets/figures/papers/MAMM_Motion_Control_via_Metric-Aligning_Motion_Matching_234bebcdacd3/figures/009_Figure_10.jpg]]
*Figure 10: Aligned motions for various ?? values with ?? fixed at 0.8. When ?? is small (e.g., 0), aligned motion includes segments where poses remain unchanged, deviating from the overall dynamics of the original motion. By contrast, large ?? (e.g., ∞) ensures that distribution of aligned motion patches closely matches original motion, often at the expense of adhering to control sequence*

## 定位与知识库关联

**核心定位：无监督度量对齐范式**

MAMM 属于一类新兴的基于最优传输（Optimal Transport）的运动对齐与合成方法，其核心创新在于**完全回避跨域映射的学习或手工定义**，转而仅利用各域内部的距离结构（度量）实现对齐。这与传统运动控制方法形成根本性区别：

- **传统跨域映射范式**：依赖手工定义的特征对应规则，或需要大规模配对数据集训练神经网络来学习从控制域到运动域的映射函数。这类方法通常针对特定任务（如音频到舞蹈、文本到动作）设计，泛化到新控制模态时需重新设计架构或重新训练。
- **MAMM 的度量对齐范式**：通过融合半非平衡 Gromov-Wasserstein（FSUGW）最优传输框架，仅需单个原始运动序列和控制序列，在数秒内通过优化传输计划实现结构对齐，无需任何配对标注或训练。

**与 GenMM 的关系与推进**

MAMM 在概念上与 **GenMM**（Li et al., SIGGRAPH 2023）共享“运动块（patch）操作”的思想——两者都将运动序列分割为重叠时间块，并通过块级匹配实现运动合成。然而，两者的任务定位和技术路线存在本质差异：

| 维度 | GenMM | MAMM |
|------|-------|------|
| 任务定位 | 基于示例的运动合成（双向相似度匹配生成新运动） | 任意控制序列到运动的对齐 |
| 对齐机制 | 双向相似度匹配（Bidirectional Similarity） | FSUGW最优传输（Wasserstein + Gromov-Wasserstein联合优化） |
| 控制信号 | 无显式控制序列输入 | 支持草图、波形、标签、音频、运动等多种控制模态 |
| 数据需求 | 无需训练，但依赖示例运动 | 仅需单个原始运动和控制序列 |

MAMM 可视为将 GenMM 的块操作思想推广到更一般的跨域对齐问题，并通过引入最优传输理论提供了更系统的优化框架。

**适用边界与任务适配**

MAMM 的统一框架使其适用于多种控制模态，但需要针对不同任务设计合适的**域内距离函数** $d_X$ 和 $d_Y$：

- **草图到运动**：控制域距离 $d_Y$ 基于曲线几何特征（如曲率、弧长参数化），运动域距离 $d_X$ 基于关节旋转和根位移的欧氏距离。
- **波形到运动**：$d_Y$ 直接使用一维信号的绝对差值，适合控制周期性运动的频率和相位。
- **音频到运动**：$d_Y$ 可采用 MFCC 特征间的欧氏距离，捕捉音频的节拍、强度和风格变化。
- **运动到运动**：$d_X$ 和 $d_Y$ 均基于运动姿态的距离度量，可实现跨骨骼、跨风格的运动时序同步。

**关键局限与失效模式**

1. **超参数敏感性强**：参数 $\alpha$（平衡 $L_{GW}$ 和 $L_W$）和 $\lambda$（控制边缘分布保真度）需手动调节以适应不同任务。$\alpha$ 过小（如 0.2）时运动自然但可能忽略控制信号；$\alpha$ 过大（如 1.0）时运动段可能出现僵硬甚至静止。$\lambda$ 过小时对齐运动可能包含不变姿态段，偏离原始运动动态；$\lambda$ 过大时分布紧密匹配原始运动，但可能牺牲对控制序列的响应。缺乏自动选择机制限制了方法的易用性。

2. **大规模数据的可扩展性瓶颈**：当前实现不适用于超过 10 万帧的数据集。FSUGW 优化涉及传输计划 $T$ 的迭代求解，其计算复杂度随序列长度增长而显著增加。缺乏通用的距离矩阵缩放策略，处理大规模多聚类数据时可能失效。

3. **实时性不足**：优化过程需数秒至数十秒（取决于序列长度），尚不能支持实时交互式控制。这限制了其在需要即时反馈的应用场景（如现场表演、游戏实时操控）中的使用。

4. **距离函数设计依赖领域知识**：虽然方法本身是通用的，但不同控制模态需要人工设计合适的域内距离函数。对于某些抽象或高维控制信号，设计有效反映语义结构的距离度量可能具有挑战性。

**开放问题与未来方向**

1. **实时化与近似加速**：如何设计 FSUGW 的快速近似算法（如低秩分解、随机化方法、分层传输）以实现实时控制，是该方向最紧迫的工程挑战。

2. **自适应超参数与距离学习**：能否为不同数据域自动学习或自适应调整距离函数及超参数 $(\alpha, \lambda)$？将度量学习（Metric Learning）与最优传输结合是一个有前景的方向。

3. **大规模运动数据库扩展**：通过分层传输（Hierarchical Optimal Transport）或随机化方法将 MAMM 扩展到包含数十万帧的运动数据库，将使其能够从更大规模的原始运动中选择最合适的源运动。

4. **连续-离散混合控制**：如何将软关键帧概念推广到连续控制信号（如手绘曲线）与语义标签联合驱动的场景？这需要设计能够同时处理连续约束和离散约束的传输计划约束机制。

5. **理论收敛性分析**：FSUGW 交替优化算法的收敛性保证尚未在论文中严格讨论，理论分析可能揭示更优的优化策略或初始化方法。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2025/MAMM.pdf]]
