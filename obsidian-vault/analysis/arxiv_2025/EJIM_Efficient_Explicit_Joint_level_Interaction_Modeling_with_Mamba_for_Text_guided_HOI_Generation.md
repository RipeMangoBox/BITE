---
title: EJIM Efficient Explicit Joint level Interaction Modeling with Mamba for Text guided HOI Generation
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: paperPDFs/arxiv_2025/EJIM_Efficient_Explicit_Joint_level_Interaction_Modeling_with_Mamba_for_Text_guided_HOI_Generation.pdf
project_link: null
code_link: null
aliases:
- EEEJLIM
- EEEJLIMMTGHG
tags:
- arxiv_2025
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 利用Mamba的线性复杂度对关节级序列进行高效时空建模，并通过肢体引导扫描、双分支条件注入和渐进式掩码机制实现精确交互。
primary_logic: 显式关节级交互建模是生成逼真HOI的关键，结合Mamba的效率优势与肢体结构先验（肢体引导扫描）以及动态注意力掩码，可在不牺牲推理速度的前提下大幅提升交互质量。
claims:
- EJIM在BEHAVE和OMOMO数据集上以仅5%的推理时间大幅超越现有方法，FID提升21%以上。
- 移除双分支设计（DHM/DCI）导致FID从0.124升至0.151，CD从0.107升至0.117，验证了双分支的必要性。
- 肢体引导扫描相比普通扫描显著提升FID和CD，证明肢体结构先验对空间建模至关重要。
- 渐进式掩码机制（k=3）达到最佳FID 0.124，关闭掩码（k=0）导致性能全面下降。
---

# EJIM Efficient Explicit Joint level Interaction Modeling with Mamba for Text guided HOI Generation

> [!tip] 核心洞察
> 显式关节级交互建模是生成逼真HOI的关键，结合Mamba的效率优势与肢体结构先验（肢体引导扫描）以及动态注意力掩码，可在不牺牲推理速度的前提下大幅提升交互质量。

| 字段 | 内容 |
|------|------|
| 中文题名 | EJIM：基于Mamba的高效显式关节级交互建模用于文本引导的人-物交互生成 |
| 英文题名 | EJIM Efficient Explicit Joint level Interaction Modeling with Mamba for Text guided HOI Generation |
| 会议/期刊 | arXiv 2025 |
| Links |  |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | EJIM (Efficient Explicit Joint-level Interaction Model) |
| Dataset | BEHAVE, OMOMO |

> [!tip] 效果简介
> - BEHAVE 上，FID↓ 0.124 vs 0.157 (CHOIS*) (-0.033)；R-Precision Top1↑ 0.403 vs 0.312 (HOI-Diff) (+0.091)；Contact Distance (CD)↓ 0.107 vs 0.117 (HOI-Diff) (-0.010)。
> - OMOMO 上，FID↓ 0.127 vs 0.164 (MDMfinetuned) (-0.037)；R-Precision Top1↑ 0.194 vs 0.147 (PriorMDM*) (+0.047)。

## 概要

**EJIM** 面向文本引导的三维人-物交互（HOI）生成任务，核心挑战在于：现有方法将人体压缩为单一token，丢失了关节级细粒度交互信息；而若将每个关节独立建模，计算量又会膨胀约400倍。EJIM的关键洞察是——**显式关节级交互建模是生成逼真HOI的瓶颈，而Mamba的线性复杂度恰好能以极低代价支撑这一细粒度建模**。

为此，EJIM提出了一套以Mamba为骨架的高效关节级交互框架，包含三个核心设计：**双分支HOI Mamba（DHM）** 对人和物体运动分别进行时空建模，其中人体分支引入肢体引导扫描以注入结构先验；**双分支条件注入器（DCI）** 将文本语义、物体几何与扩散时间步注入运动流；**动态交互块（DIB）** 配合渐进式掩码机制，逐模块过滤低注意力关节，使交互建模逐步聚焦于真正相关的关节对。

在BEHAVE和OMOMO两个基准上，EJIM以仅约5%的推理时间大幅超越现有方法——FID提升超过21%，接触距离（CD）和足部滑动率（FSR）均显著下降。消融实验系统验证了双分支设计、肢体引导扫描、渐进式掩码（k=3）以及物体损失与光滑损失各自的关键贡献。用户研究进一步表明，EJIM在语义匹配度和交互合理性上均优于对比方法。



**任务定义与挑战** 文本引导的三维人-物交互（Human-Object Interaction, HOI）生成旨在根据自然语言描述和物体几何信息，合成逼真且语义一致的人体与物体协同运动序列。该任务的核心挑战在于：人体运动与物体运动之间存在细粒度的空间-时间耦合关系，生成结果必须同时满足语义匹配、物理合理性（如避免穿透、保持合理接触距离）和运动自然度等多重约束。

**现有方法的瓶颈** 当前主流方法在人体表示上存在根本性局限——它们通常将整个人体压缩为单一特征token，然后利用Transformer架构进行全局时空建模。这种粗粒度表示虽然计算高效，却从根本上丧失了关节级别的交互细节捕捉能力。若反过来对每个关节独立建模，则会导致序列长度膨胀约400倍，使得基于自注意力的Transformer面临$O(n^2)$的计算灾难。这一“粒度-效率”悖论构成了该领域长期悬而未决的结构性瓶颈。

**Mamba带来的转机** 状态空间模型（State Space Models, SSM）的线性复杂度特性为打破上述僵局提供了新的可能。Mamba作为SSM的最新演进，通过输入依赖的选择性扫描机制，在保持序列长度线性复杂度的同时实现了对长程依赖的有效建模。然而，直接将Mamba应用于HOI生成仍面临两个关键缺口：其一，标准的序列扫描方式忽略了人体固有的肢体结构先验，无法有效捕捉同一肢体内部关节的强相关性；其二，人与物体之间的交互并非全局均匀的——不同交互动作中，仅有部分关节与物体发生实质性接触，需要一种动态的、逐步聚焦的交互建模机制。

**本文动机** 针对上述问题，本文提出EJIM（Efficient Explicit Joint-level Interaction Model），核心动机是实现“显式关节级交互建模”与“高效推理”的统一。具体而言，EJIM利用Mamba的线性复杂度对23个关节级token进行高效时空建模，同时引入三个关键设计：肢体引导扫描（Limb-guided Scan）将人体结构先验注入空间扫描顺序、双分支条件注入器（Dual-branch Condition Injector, DCI）实现文本语义与物体几何的精细化条件融合、以及渐进式动态交互掩码（Progressive Dynamic Interaction Mask）使模型从全局交互逐步收敛到关键关节的精准交互。这一设计使得EJIM能够在仅消耗现有方法约5%推理时间的前提下，大幅提升交互生成的逼真度和语义准确性。



## 核心方法与创新机理

EJIM的核心创新在于将人-物交互（HOI）生成从粗粒度的全身表示推进到**显式关节级交互建模**，并利用Mamba的线性复杂度解决随之而来的计算瓶颈。与现有方法将人体压缩为单一token不同，EJIM将人体表示为23个关节级token（含虚拟足部接触关节），使模型能够精确捕捉手部、肘部等关键部位与物体的细粒度交互。这一表示粒度的提升带来了约400倍的计算量增长风险，而EJIM通过以下三个紧密耦合的设计实现了高效且精准的交互生成。

### 1. 双分支HOI Mamba与肢体引导空间扫描

传统Transformer的自注意力机制复杂度为 $O(n^2)$，在关节级序列上难以承受。EJIM采用**双分支HOI Mamba（DHM）**，将人体和物体运动分别送入独立的Mamba分支进行时空建模，充分利用Mamba的线性复杂度优势。更为关键的是，人体分支引入了**肢体引导空间扫描**策略：先将23个关节按肢体结构（左右臂、左右腿、躯干等）分组，在各组之间插入可学习的虚拟分隔token，再按分组顺序扫描。这一设计将人体运动的肢体结构先验注入Mamba的序列建模过程，使空间上相邻的关节在扫描序列中也保持邻近，从而更有效地捕捉关节间的空间依赖关系。消融实验证实，用普通扫描替代肢体引导扫描后，FID从0.124升至0.143，CD从0.107升至0.123，验证了肢体结构先验对空间建模的决定性作用。

### 2. 双分支条件注入器（DCI）

现有方法通常通过简单拼接或交叉注意力注入条件信息，难以在关节级粒度上实现精细的条件控制。EJIM的**双分支条件注入器（DCI）**将文本语义（由CLIP提取）、扩散时间步和物体几何特征（由PointNet提取）分别注入人体和物体运动流。其核心操作是将条件token $\mathbf{c}$ 与运动token $\mathbf{m}$ 拼接后送入Mamba处理，仅保留运动token输出：

$$\hat{\mathbf{m}} = \mathbf{Mamba}(\mathbf{Concat}([\mathbf{c}, \mathbf{m}]))$$

双分支设计使人体和物体能够独立接收各自相关的条件信号，避免了单分支设计中信息混淆的问题。消融表明，单分支配置导致FID升至0.159，R-Precision Top1降至0.307，证实了双分支条件注入的必要性。

### 3. 动态交互块与渐进式掩码机制

为实现显式的关节-物体交互建模，EJIM在每个Joint-level Interaction Module中嵌入两个**动态交互块（DIB）**。DIB通过带掩码的注意力机制直接建模人体关节与物体之间的交互：

$$\hat{\mathbf{y}}_l = \mathrm{softmax}\left(\frac{\mathbf{Q}\mathbf{K}^T}{\sqrt{D}} + \mathbf{M}_l^i\right)\mathbf{V}$$

其中交互掩码 $\mathbf{M}_l^i$ 控制哪些关节参与交互计算。EJIM进一步提出了**渐进式掩码机制**：初始时所有关节均可见，在每个模块中根据注意力得分过滤掉 $k$ 个最不相关的关节（$k=3$ 时达到最佳FID 0.124），使后续模块的交互建模逐步聚焦于真正参与交互的关键关节。这一机制有效抑制了无关关节的噪声干扰，同时避免了过早过滤导致的交互信息丢失。消融显示，完全关闭掩码（$k=0$）导致FID升至0.154，而移除整个DIB模块则使FID飙升至0.190、CD升至0.150，充分证明了显式交互建模和渐进式掩码的核心作用。

### 创新总结

EJIM的三项创新形成了从“表示粒度提升”到“高效时空建模”再到“精准交互聚焦”的完整因果链：关节级表示提供了交互建模的细粒度基础，肢体引导Mamba和双分支条件注入保障了计算效率与条件控制精度，而渐进式掩码机制则确保交互建模始终聚焦于真正相关的关节。这一设计使EJIM在BEHAVE和OMOMO数据集上以仅约5%的推理时间大幅超越HOI-Diff等现有方法，FID提升超过21%。



EJIM是一种基于扩散模型的文本驱动HOI生成框架，核心瓶颈在于**显式关节级交互建模**——现有方法将人体压缩为单一token，丢失了细粒度的关节-物体接触信息，而将每个关节独立处理又导致计算量激增。EJIM通过Mamba的线性复杂度特性，在保持高效推理的同时实现了关节级时空建模。

### 输入输出与数据流

框架的输入输出流程如下：

1. **输入**：带噪的HOI序列 $\mathbf{x}_t = \{\mathbf{x}_t^o, \mathbf{x}_t^h\}$，其中 $\mathbf{x}_t^o$ 为物体运动，$\mathbf{x}_t^h$ 为人体运动（表示为23个关节级token，含虚拟足地接触关节）。条件信号包括文本描述（经预训练CLIP编码）和物体几何（经PointNet编码）。

2. **编码阶段**：人体和物体运动分别通过线性投影器 $E_H$ 和 $E_O$ 映射到统一隐空间。

3. **核心处理**：隐空间特征经过 $N$ 个相同的**Joint-level Interaction Module**串联处理，每个模块包含三个关键子模块：
   - **Dual-branch HOI Mamba (DHM)**：双分支分别对人体和物体进行时空建模，人体分支采用肢体引导空间扫描
   - **Dual-branch Condition Injector (DCI)**：将文本语义、扩散时间步、物体几何条件注入人体和物体运动流
   - **Dynamic Interaction Block (DIB)** ×2：基于动态交互掩码的注意力机制，显式建模人体关节与物体的交互

4. **解码阶段**：处理后的隐空间特征经线性投影器 $D_H$ 和 $D_O$ 解码回原始运动空间，得到去噪后的HOI序列 $\mathbf{x}_{t-1}$。

### 核心设计逻辑

EJIM的设计围绕三个因果调节变量展开：

- **关节级表示**：将人体从单一token扩展为23个关节token，使模型能够区分不同关节与物体的接触关系（如“手推椅子”vs“脚踢椅子”），这是生成逼真交互的前提。
- **Mamba线性复杂度**：相比Transformer的 $O(n^2)$ 复杂度，Mamba的线性复杂度使得处理关节级序列（序列长度约为全身token的23倍）成为可能，推理时间仅需HOI-Diff的4.5%。
- **肢体结构先验**：通过肢体引导扫描将人体关节按肢体分组排列，并插入可学习分隔token，使Mamba能够感知肢体结构，从而更准确地建模关节间的空间关系。

### 渐进式掩码机制

DIB中的动态交互掩码 $\mathbf{M}_l^i$ 实现了从粗到细的交互建模：初始时所有关节均可见，每个Joint-level Interaction Module根据注意力分数过滤掉 $k$ 个最不相关的关节（$k=3$ 时性能最优），使后续模块专注于真正参与交互的关键关节。这一机制有效抑制了无关关节对交互建模的干扰。

### 补充图表

![[assets/figures/papers/paper_list_l1679_EJIM_Efficient_Explicit_Joint_level_Interaction_Modeling_with_Mamba_for/figures/002_Figure_2.jpg]]
*Figure 2: Overview of our EJIM. Our EJIM takes a noisy HOI sequence*



EJIM 的核心由 $N$ 个结构相同的 **Joint-level Interaction Module** 堆叠而成，每个模块包含三个关键子块：**Dual-branch HOI Mamba (DHM)**、**Dual-branch Condition Injector (DCI)** 和 **Dynamic Interaction Block (DIB)**。其设计瓶颈在于：将人体表示为 23 个关节级 token 后，若采用 Transformer 的全局自注意力将导致 $O(n^2)$ 的计算爆炸（约 400 倍增长），而 Mamba 的线性复杂度状态空间模型恰好解决了这一矛盾。

### 连续状态空间模型（SSM）基础

Mamba 的核心建立在连续时间状态空间模型之上，其数学形式为：

$$h'(t) = \mathbf{A} h(t) + \mathbf{B} x(t), \quad y(t) = \mathbf{C} h(t) + D x(t)$$

其中 $x(t)$ 为输入信号，$h(t)$ 为隐状态，$y(t)$ 为输出。通过离散化后，该模型可高效地对长序列进行建模，复杂度为 $O(n)$，这是 EJIM 能够在关节级粒度上进行时空建模而推理时间仅需 0.27 秒的根本原因。

### 前向扩散过程

EJIM 基于扩散模型框架，给定干净的运动序列 $\mathbf{x}_0$，前向过程按噪声调度 $\beta_t$ 逐步添加高斯噪声：

$$q(\mathbf{x}_t | \mathbf{x}_{t-1}) = \mathcal{N}(\mathbf{x}_t; \sqrt{1 - \beta_t} \mathbf{x}_{t-1}, \beta_t I)$$

模型学习逆向过程，从噪声 $\mathbf{x}_t$ 预测去噪后的 $\mathbf{x}_{t-1}$。关键设计在于：人体运动 $\mathbf{x}_t^h$ 被编码为 23 个关节级 token（含一个虚拟脚-地接触关节），物体运动 $\mathbf{x}_t^o$ 保持为单一 token，二者通过线性投影 $E_H$、$E_O$ 映射到隐空间后分别进入双分支处理。

### Dual-branch HOI Mamba (DHM)

DHM 包含人体分支和物体分支，均基于 Mamba 块实现。人体分支的核心创新是 **肢体引导空间扫描（Limb-guided Spatial Mamba）**：将 23 个关节按肢体分组（左右臂、左右腿、躯干等）重新排序，并在各组之间插入可学习分隔 token，使 Mamba 在扫描时天然具备肢体结构先验。虚拟脚-地接触关节被复制并同时分配给双腿，以缓解脚步滑动问题。消融实验表明，用普通扫描替代肢体引导扫描，FID 从 0.124 升至 0.143，CD 从 0.107 升至 0.123；移除可学习分隔 token 或用固定 token 替代，CD 从 0.107 恶化至 0.188，证实了肢体结构先验对空间建模的关键作用。

### Dual-branch Condition Injector (DCI)

DCI 负责将文本语义、扩散时间步和物体几何条件注入运动流。其核心操作为：

$$\hat{\mathbf{m}} = \mathbf{Mamba}(\mathbf{Concat}([\mathbf{c}, \mathbf{m}]))$$

其中 $\mathbf{c}$ 为条件 token（通过预训练 CLIP 提取文本特征，PointNet 提取物体几何特征），$\mathbf{m}$ 为运动 token。二者拼接后送入 Mamba，仅保留运动 token 部分作为输出。双分支设计意味着人体和物体分别拥有独立的 DCI，消融实验显示单分支合并设计导致 FID 升至 0.159，R-Top1 降至 0.307，验证了双分支的必要性。

### Dynamic Interaction Block (DIB) 与渐进式掩码

DIB 通过带动态掩码的注意力机制显式建模人体关节与物体的交互：

$$\hat{\mathbf{y}}_l = \mathrm{softmax}\left(\frac{\mathbf{Q}\mathbf{K}^T}{\sqrt{D}} + \mathbf{M}_l^i\right)\mathbf{V}$$

其中 $\mathbf{M}_l^i$ 为动态交互掩码，可见关节对应 0，被掩码关节对应 $-\infty$。**渐进式掩码机制**是 DIB 的核心创新：初始时所有关节均可见，每经过一个 Joint-level Interaction Module，根据注意力分数过滤掉 $k$ 个最不相关的关节。当 $k=3$ 时达到最佳 FID 0.124，关闭掩码（$k=0$）导致 FID 升至 0.154。移除整个 DIB 模块后 FID 从 0.124 升至 0.190，CD 从 0.107 升至 0.150，证明显式交互建模不可或缺。

### 训练损失函数

总损失由三项加权组合：

$$\mathcal{L} = \lambda_1 ||\mathbf{x} - \hat{\mathbf{x}}||_2 + \lambda_2 ||\mathbf{x}^o - \hat{\mathbf{x}}^o||_2 + \lambda_3 \sum_{l=1}^{L-1} ||\mathbf{x}_l - \mathbf{x}_{l+1}||_2$$

其中第一项为扩散重建损失，第二项为物体运动损失（权重 $\lambda_2=1$），第三项为光滑性损失（权重 $\lambda_3=0.5$），用于抑制帧间抖动。消融显示去掉物体损失使 CD 升至 0.154，去掉光滑损失使 FSR 升至 0.098，表明两项辅助损失对交互质量和运动平滑性至关重要。

### 补充图表

![[assets/figures/papers/paper_list_l1679_EJIM_Efficient_Explicit_Joint_level_Interaction_Modeling_with_Mamba_for/figures/003_Figure_3.jpg]]
*Figure 3: (a) Illustration of human joints. (b) Our limb division scheme. Here, the virtual foot-ground contact joint is duplicated and assigned to both lower limbs to mitigate foot skating. (c) The Limb-guided scan in our Spatial Mamba reorders joints by limb groupings and inserts learnable tokens to define distinct limbs. (d) The vanilla scan approach for comparison*

![[assets/figures/papers/paper_list_l1679_EJIM_Efficient_Explicit_Joint_level_Interaction_Modeling_with_Mamba_for/figures/004_Figure_4.jpg]]
*Figure 4: Our progressive masking mechanism. Initially, all joints are visible. At each Joint-level Interaction Module, we filter out k joints with the lowest attention scores, leading to more accurate interaction modeling*



## 实验与关键发现

### 定量对比：BEHAVE与OMOMO数据集

EJIM在两个标准HOI生成基准上均以显著优势超越现有方法，同时仅需约5%的推理时间。Table I（及附录Table VI）报告了BEHAVE和OMOMO测试集上的完整结果，所有评估重复20次并给出95%置信区间。

**BEHAVE数据集**上，EJIM在生成质量与交互质量两个维度均取得最优：

- **FID**降至0.124，较第二优方法CHOIS\*（Li et al., ECCV 2024）的0.157降低21.0%，较HOI-Diff（Peng et al., arXiv 2023）的0.179降低30.7%。
- **R-Precision Top1**达到0.403，较HOI-Diff的0.312提升29.2%，表明文本-运动语义对齐能力大幅领先。
- **Contact Distance (CD)**降至0.107，优于HOI-Diff的0.117和PriorMDM\*的0.122，验证了关节级显式交互建模对接触精度的关键作用。
- **Foot Skating Rate (FSR)**为0.057，低于PriorMDM\*的0.066，得益于虚拟足地接触关节与肢体引导扫描设计。
- **平均推理时间 (AIT)**仅0.27秒，而HOI-Diff需5.97秒——EJIM仅用其4.5%的推理时间，效率提升超过20倍。这一优势源于Mamba的线性复杂度（$O(n)$）替代Transformer的二次复杂度（$O(n^2)$）。

**OMOMO数据集**上，EJIM同样全面领先：

- FID 0.127，较MDMfinetuned的0.164降低22.6%；R-Precision Top1 0.194，较PriorMDM\*的0.147提升32.0%。
- 该数据集包含更复杂的物体几何与交互类型，EJIM的鲁棒表现进一步验证了显式关节级建模的泛化能力。

**关键结论**：EJIM与先前方法之间的巨大性能差距（FID提升超21%，R-Top1提升超29%）直接证明了显式关节级交互建模对生成逼真HOI的决定性作用。同时，仅4.5%的推理时间成本使得该方法具备实际部署潜力。

### 用户研究

55名参与者对EJIM与InterDiff（Xu et al., ICCV 2023）、CHOIS\*、HOI-Diff进行盲评，从语义匹配（生成动作是否与文本描述一致）和交互合理性（是否存在穿透、悬空等物理异常）两个维度投票（Table II）：

- 语义匹配：EJIM分别以56.4% vs 43.6%（vs InterDiff）、52.7% vs 47.3%（vs CHOIS\*）、60.0% vs 40.0%（vs HOI-Diff）胜出。
- 交互合理性：EJIM以58.2% vs 41.8%（vs InterDiff）、54.5% vs 45.5%（vs CHOIS\*）、63.6% vs 36.4%（vs HOI-Diff）大幅领先。

用户主观评价与客观指标高度一致，尤其在交互合理性维度优势更明显，印证了动态交互块（DIB）与渐进式掩码机制对减少穿透、改善接触的有效性。

### 主要模块消融

Table III在BEHAVE数据集上验证了EJIM各核心模块的必要性：

- **移除DIB**：FID从0.124飙升至0.190（+53.2%），CD从0.107升至0.150（+40.2%），证明显式交互建模模块是性能基石。
- **移除双分支设计（合并人体与物体为单分支）**：FID升至0.159，R-Top1降至0.307，CD升至0.126。双分支设计允许人体与物体各自保持独立的时空建模路径，合并后信息混杂导致交互质量显著下降。
- **移除DCI**（条件注入器）：FID升至0.151，CD升至0.117，说明文本语义与物体几何的条件注入对引导生成至关重要。

### DHM消融：肢体引导扫描与可学习分隔token

Table IV针对双分支HOI Mamba（DHM）进行深入消融：

- **肢体引导扫描 vs 普通扫描**：使用普通扫描（vanilla scan）替代肢体引导空间扫描后，FID从0.124升至0.143，CD从0.107升至0.123。肢体结构先验（将关节按肢体分组扫描并插入可学习分隔token）对空间关系建模具有不可替代的作用。
- **可学习分隔token vs 固定token vs 无token**：可学习token方案CD为0.107，固定token方案CD恶化至0.188，无token方案CD为0.132。可学习分隔token能自适应地编码肢体边界信息，固定token则破坏了关节间的语义连续性。

### DIB消融：渐进式掩码机制

Table V探索了每模块过滤关节数k的影响：

- **k=3**（每模块掩码3个注意力得分最低的关节）达到最佳综合性能：FID 0.124，CD 0.107。
- **k=0**（关闭渐进式掩码，所有关节始终可见）：FID升至0.154，CD升至0.128，R-Top1降至0.370。说明逐步过滤无关关节能有效减少噪声干扰，使模型聚焦于真正参与交互的关键关节。
- **k值过大**（如k=5）：CD升至0.130，可能因过度掩码丢失了必要的上下文信息。

### 损失函数与超参数消融

**损失权重**（Table VII）：移除物体运动损失（$\lambda_2=0$）导致CD从0.107升至0.154；移除光滑性损失（$\lambda_3=0$）导致FSR从0.057升至0.098。两项辅助损失分别对接触精度和运动平滑性起关键约束作用。

**引导尺度**（Table VIII）：引导尺度2达到最佳平衡（FID 0.124，CD 0.107）。过大尺度虽提升R-Top1至0.419，但CD恶化至0.119，表明过度强调文本对齐可能损害物理合理性。

**物体几何条件**（Table IX）：移除PointNet提取的物体几何特征后，FID升至0.139，CD升至0.159，验证了物体几何先验对空间交互建模的指导价值。

**推理步数**（Table X）：50步在性能与效率间取得平衡（FID 0.124，AIT 0.27s）。20步FID略升至0.127但AIT降至0.11s；100步FID仅微降至0.121但AIT翻倍至0.54s。

**模块数量**（Table XI）：6个Joint-level Interaction Module性能最优。增至8个时CD反而从0.107升至0.115，可能因过深网络引入优化困难。

### 定性分析

Figure 5展示了BEHAVE数据集上的定性对比。先前方法（InterDiff、CHOIS\*、HOI-Diff）在复杂交互场景中频繁出现网格穿透（红色框标注）、接触距离过大或文本不一致问题。EJIM生成的交互在接触精度、时序连贯性和文本语义匹配方面均表现更优，尤其在手部抓取物体、身体倚靠等细粒度交互场景中优势明显。

### 失败模式与局限性

尽管EJIM在单物体交互场景中表现优异，但存在以下局限：

1. **多物体交互不支持**：当前框架假设场景中仅存在单一交互物体，无法处理同时与多个物体交互的场景（如双手各持一物），可能生成不完整或物理矛盾的动画。
2. **非刚体物体不适用**：框架缺少对变形物体的建模先验（如头发、衣物、烟雾），且相关标注数据匮乏，限制了对非刚体交互场景的泛化。

这些失败模式指向未来工作方向：扩展渐进式掩码机制以支持多物体注意力分配，以及引入物理先验（如接触力约束）进一步减少穿透和滑动。

### 补充图表

![[assets/figures/papers/paper_list_l1679_EJIM_Efficient_Explicit_Joint_level_Interaction_Modeling_with_Mamba_for/figures/005_Table.jpg]]
*Table: I QUANTITATIVE RESULTS ON THE BEHAVE AND OMOMO TEST SETS. EACH EVALUATION WAS CONDUCTED 20 TIMES TO COMPUTE AVERAGE RESULTS WITH A 95% CONFIDENCE INTERVAL (DENOTED AS ±). THE BEST PERFORMANCE IS IN BOLD, AND THE SECOND-BEST IS UNDERLINED. AVERAGE INFERENCE TIME (AIT), CALCULATED ONLY ON THE BEHAVE DATASET, DENOTES THE MEAN OVER 100 SAMPLES ON AN RTX 3090. TABLE II USER STUDY RESULTS. BOLD VALUES INDICATE BETTER PERFORMANCE. TABLE III TABLE IV ABLATION STUDY OF THE DHM ON THE BEHAVE DATASET. ABLATION STUDY OF THE MAIN MODULES ON THE BEHAVE DATASET*

![[assets/figures/papers/paper_list_l1679_EJIM_Efficient_Explicit_Joint_level_Interaction_Modeling_with_Mamba_for/figures/007_Table.jpg]]
*Table: V ABLATION STUDY OF THE NUMBER OF MASKED JOINTS (K) IN THE DIB’S PROGRESSIVE MASKING MECHANISM*

![[assets/figures/papers/paper_list_l1679_EJIM_Efficient_Explicit_Joint_level_Interaction_Modeling_with_Mamba_for/figures/008_Table.jpg]]
*Table: VI QUANTITATIVE EVALUATION OF THE BEHAVE AND OMOMO TEST SETS. WE REPEATED EVALUATION 20 TIMES TO CALCULATE THE AVERAGE RESULTS WITH A 95% CONFIDENCE INTERVAL (DENOTED BY ±). THE BEST RESULT IS IN BOLD, AND THE SECOND BEST IS UNDERLINED*

![[assets/figures/papers/paper_list_l1679_EJIM_Efficient_Explicit_Joint_level_Interaction_Modeling_with_Mamba_for/figures/009_Table.jpg]]
*Table: VII IMPACT OF WEIGHTS ON THE TRAINING LOSS. THE GRAY LINE INDICATES THE CONFIGURATION ADOPTED IN OUR EJIM. TABLE VIII TABLE IX ABLATION STUDY OF THE OBJECT GEOMETRY ON THE BEHAVE DATASET TABLE X*

![[assets/figures/papers/paper_list_l1679_EJIM_Efficient_Explicit_Joint_level_Interaction_Modeling_with_Mamba_for/figures/010_Table.jpg]]
*Table: IMPACT OF THE NUMBER OF INFERENCE STEPS. THE GRAY LINE REPRESENTS THE CONFIGURATION USED IN OUR EJIM. THE AVERAGE INFERENCE TIME (AIT) IS THE MEAN OVER 100 SAMPLES ON AN RTX 3090TI*

![[assets/figures/papers/paper_list_l1679_EJIM_Efficient_Explicit_Joint_level_Interaction_Modeling_with_Mamba_for/figures/011_Table.jpg]]
*Table: IMPACT OF THE GUIDANCE SCALE. THE GRAY LINE REPRESENTS THE CONFIGURATION USED IN OUR EJIM*

![[assets/figures/papers/paper_list_l1679_EJIM_Efficient_Explicit_Joint_level_Interaction_Modeling_with_Mamba_for/figures/012_Table.jpg]]
*Table: XI IMPACT OF THE NUMBER OF BLOCKS. THE GRAY LINE REPRESENTS THE CONFIGURATION USED IN OUR EJIM*

![[assets/figures/papers/paper_list_l1679_EJIM_Efficient_Explicit_Joint_level_Interaction_Modeling_with_Mamba_for/figures/001_Figure_1.jpg]]
*Figure 1: Our EJIM can generate realistic 3D human-object interactions guided by text descriptions and object geometry, with colors transitioning from lighter to darker to represent the passage of time*

![[assets/figures/papers/paper_list_l1679_EJIM_Efficient_Explicit_Joint_level_Interaction_Modeling_with_Mamba_for/figures/006_Figure.jpg]]
*Figure: Someone is applying force to the tablesquare by pulling it on the ground*



## 定位与知识库关联

### 1. 与现有方法的谱系关系

EJIM 处于**文本驱动的3D人-物交互（HOI）运动生成**这一任务线上，其核心突破在于首次将**显式关节级交互建模**与**Mamba的高效线性复杂度**相结合。此前的方法可大致分为两条技术路线：

**（1）基于Transformer的隐式全身建模路线**

- **MDM**（Tevet et al., ICCV 2023）及其适配版 **MDM\*** 将人体运动表示为单一token，通过Transformer进行时空建模。这一设计虽然简洁，但将整个人体压缩为单一表示，**天然丢失了关节间的细粒度空间关系**，无法显式建模“手触碰物体”这类精确交互。
- **PriorMDM\***（Shafir et al., ICCV 2024）将双人运动框架迁移至HOI场景，但仍沿用全局token表示，交互建模依赖于Transformer的全局注意力，缺乏对交互关节的显式聚焦。
- **InterDiff**（Xu et al., ICCV 2023）引入物理引导，但本质上仍采用隐式交互建模，且原文未包含文本条件（本文为其添加文本条件后纳入对比）。

这些方法的共同瓶颈在于：**人体表示粒度过粗**（单一全身token），且Transformer的 $O(n^2)$ 复杂度使得直接对每个关节独立建模的计算代价过高（约400倍增长），迫使研究者不得不妥协于粗粒度表示。

**（2）基于扩散模型的HOI专用路线**

- **HOI-Diff**（Peng et al., arXiv 2023）是首个专门针对文本驱动HOI生成的扩散模型，但其人体表示仍为整体token，交互建模依赖全局注意力。
- **CHOIS\***（Li et al., ECCV 2024）原本依赖路径点条件，本文移除路径点后将其纳入文本驱动对比。该方法在交互质量上有所改进，但推理效率仍受限于Transformer架构。

EJIM 在谱系中的定位是：**保留了扩散模型的生成框架，但将人体表示从单一token升级为23个关节级token，并用Mamba替代Transformer作为核心建模器**。这一“细粒度表示 + 线性复杂度建模器”的组合，使得显式关节级交互建模在计算上首次变得可行。

### 2. 方法适用边界

**明确支持的能力：**

- 文本描述驱动的人-物交互运动生成，输入为文本 + 物体几何（PointNet提取），输出为人体与物体的同步运动序列。
- 单一刚体物体场景（如椅子、桌子、箱子等BEHAVE和OMOMO数据集中的物体类别）。
- 支持多种交互类型（坐、搬、推、拉等），在BEHAVE和OMOMO两个数据集上验证。

**明确不支持/未验证的场景：**

- **多物体交互**：论文明确将“不支持多物体场景”列为局限性，当前框架无法处理人同时与多个物体交互的情况，可能生成不完整或不准确的动画。
- **非刚体物体**：无法处理头发、烟雾、布料等可变形物体，因为框架缺少变形先验，且相关训练数据不足。
- **实时交互应用**：虽然推理速度已大幅提升（0.27s/样本），但论文未验证在VR/AR等实时场景中的部署可行性。
- **长时序生成**：论文未验证在超出BEHAVE/OMOMO数据集时序范围（约数秒级别）的长序列生成上的表现。

### 3. 关键局限与失败模式分析

**（1）渐进式掩码的过过滤风险**

DIB中的渐进式掩码机制每层过滤 $k$ 个注意力得分最低的关节。当 $k$ 设置过大时，可能导致**交互关键关节被过早排除**。论文消融实验（TABLE V）显示 $k=3$ 为最优，但未分析不同交互类型对 $k$ 值的敏感性——某些交互（如“用手指轻触”）可能仅涉及1-2个关节，而过早过滤可能误伤关键关节。

**（2）肢体划分先验的泛化性**

肢体引导扫描（Limb-guided Scan）将人体关节按五组肢体划分（图3b），这一先验在标准人体骨骼上有效，但**对非标准骨骼（如动物、机器人）或缺失关节的情况可能失效**。论文仅在标准SMPL-H骨骼上验证，未讨论骨骼拓扑变化的适应性。

**（3）物体几何条件的依赖性**

消融实验（TABLE IX）显示移除物体几何条件导致CD从0.107升至0.159，表明模型对物体几何输入的强依赖。这意味着**当物体几何表示不准确或噪声较大时，交互质量可能显著下降**。论文未测试对几何噪声的鲁棒性。

**（4）双分支设计的计算冗余**

虽然Mamba本身是线性的，但双分支DHM + 双分支DCI + 两个DIB的模块堆叠（共 $N=6$ 个Joint-level Interaction Module）引入了可观的参数和计算量。论文未与更轻量的单分支变体在参数效率上进行系统对比（仅报告了单分支的性能下降，未分析参数量的差异）。

### 4. 开放问题

1. **多物体交互扩展**：如何将渐进式掩码机制从“人-单物”推广到“人-多物”场景？是否需要对每个物体独立维护一个交互掩码，还是共享统一的注意力空间？

2. **物理先验的融入**：当前方法依赖数据驱动学习交互约束，但接触距离（CD）和穿透率（PS）仍有优化空间。引入显式物理先验（如接触力、穿透惩罚）是否能进一步减少伪影？这会与扩散模型的去噪目标如何协调？

3. **实时部署可行性**：0.27秒的推理时间（RTX 3090）距离实时交互（>30fps）仍有差距。通过模型蒸馏、量化或更少的推理步数（TABLE X显示20步FID仅升至0.127），是否有望达到实时性能？

4. **肢体引导扫描的通用性**：这一扫描策略本质上是将空间结构先验编码为序列顺序，该思路是否适用于其他基于Mamba的序列建模任务（如蛋白质结构预测、分子动力学模拟）？

5. **关节级交互的可解释性**：渐进式掩码机制提供了“哪些关节参与交互”的自然解释，但论文未对此进行深入分析。掩码模式是否与人类直觉一致？能否用于交互质量的事前诊断？



## 原文 PDF

![[paperPDFs/arxiv_2025/EJIM_Efficient_Explicit_Joint_level_Interaction_Modeling_with_Mamba_for_Text_guided_HOI_Generation.pdf]]
