---
title: "MotionGPT3: Human Motion as a Second Modality"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/MotionGPT3_Human_Motion_as_a_Second_Modality.pdf
project_link: null
code_link: https://github.com/OpenMotionLab/MotionGPT3
openreview_forum_id: Ha075JDMZR
aliases:
- MotionGPT3
tags:
- ICLR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/generative_models_and_autoencoders
core_operator: "采用连续VAE潜在空间替代离散码本，并引入双流Transformer架构分离模态特定路径，通过共享注意力进行受控交互。"
primary_logic: "为运动模态建立独立分支并通过共享注意力进行受控交互，可以避免量化损失和模态间干扰，从而提高生成质量和训练稳定性。"
claims:
- "在组件消融中，双流+VAE配置实现了最佳的T2M和M2T性能，显著优于单流或VQ变体。"
- "双流骨干使扩散损失的收敛速度提高约2倍，且在匹配损失下获得更高的R@3和更低的MMDist。"
- "连续VAE潜在空间在重建精度上全面优于VQ-VAE，并在生成和理解任务中带来更强的对齐性能。"
- "完整的三阶段训练计划（SI+SII+SIII）实现了生成与理解的最佳平衡，省略第一阶段会严重降低生成质量。"
---

# MotionGPT3: Human Motion as a Second Modality

> [!tip] 核心洞察
> 为运动模态建立独立分支并通过共享注意力进行受控交互，可以避免量化损失和模态间干扰，从而提高生成质量和训练稳定性。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | MotionGPT3：将人体运动作为第二模态 |
| 英文题名 | MotionGPT3: Human Motion as a Second Modality |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=Ha075JDMZR) · [GitHub](https://github.com/OpenMotionLab/MotionGPT3) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/generative_models_and_autoencoders |
| Method | MotionGPT3 |
| Dataset | HumanML3D, KIT-ML, HumanML3D (TMR evaluator) |

> [!tip] 效果简介
> - HumanML3D 上，R-Precision Top-3 (R@3) 为 0.837 (MotionGPT3 unified)，对比 0.733 (MotionGPT unified)，变化 +0.104。
> - HumanML3D 上，FID 为 0.208 (MotionGPT3 unified)，对比 0.232 (MotionGPT unified)，变化 -0.024。
> - KIT-ML 上，R@3 为 0.803 (MotionGPT3†)，对比 0.734 (MLD)，变化 +0.069。

## 概要

人体运动生成与理解是构建具身智能体的关键能力。现有统一框架普遍采用离散VQ-VAE将运动量化为令牌，并与文本在单流Transformer中联合建模。然而，这种范式面临两个根本瓶颈：**运动量化引入的近似误差**限制了生成运动的精细度，而**单流骨干中离散文本与连续运动信号的联合处理**引发了严重的跨模态干扰，导致训练不稳定和收敛缓慢。

MotionGPT3 的核心洞察在于：**将人体运动视为独立于文本的第二模态**，为其建立专属处理路径，仅通过受控的共享注意力机制与语言分支交互。这一设计从因果层面同时解决了量化损失和模态干扰问题。具体而言，该方法做出四项关键改变：

- **运动表示**：采用连续VAE潜在空间替代离散码本，消除量化瓶颈。
- **骨干架构**：构建双流Transformer，文本分支和运动分支各自维护独立的嵌入、前馈网络和归一化层，仅在共享自注意力层进行信息交换。
- **运动生成头**：在VAE潜在空间上附加轻量级扩散头，以运动分支的隐藏状态为条件进行去噪预测，取代传统的自回归令牌预测。
- **训练策略**：设计三阶段“生成-对齐-微调”流程——先冻结文本分支进行T2M预训练，再引入跨模态对齐任务，最后解冻全部参数联合微调。

实验证据有力地支撑了上述设计的有效性。在组件消融中，**双流+VAE配置**在HumanML3D上实现了最佳的文本到运动生成（R@3达0.826）和运动描述生成性能，显著优于单流或VQ变体（Table 4）。训练效率分析表明，双流骨干使扩散损失的收敛速度提高约2倍，且在匹配损失下获得更高的R@3和更低的MMDist（Figure 3）。连续VAE潜在空间在重建精度上全面优于VQ-VAE，并为生成与理解任务带来更强的对齐性能（Table 4, Table 5）。完整的三阶段训练计划实现了生成与理解的最佳平衡，省略第一阶段会严重降低生成质量（Table 5/Table 13）。

在标准基准上，MotionGPT3统一模型在HumanML3D上取得R@3为0.837、FID为0.208，较MotionGPT统一模型分别提升+0.104和-0.024（Table 1）；在KIT-ML上R@3达0.803，超越MLD等专用生成模型（Table 2）。基于TMR评估器的检索任务中，MotionGPT3在所有协议下均大幅领先先前方法，Text-Motion R@1达到9.60（Table 7）。

尽管如此，当前框架仍存在若干局限：验证范围限于HumanML3D和KIT-ML两个中小规模基准；三阶段训练策略需手动设计阶段划分，难以自动泛化至新模态；运动分支容量受限于语言模型规模，直接扩展会导致训练不稳定；跨模态对齐主要依赖配对数据，未能充分利用纯文本语料中的语言知识。这些方向为未来工作留下了明确的探索空间。



### 运动生成与理解的统一建模困境

人体运动生成与理解是具身智能领域的核心任务，涵盖文本到运动（Text-to-Motion, T2M）生成和运动到文本（Motion-to-Text, M2T）描述两个方向。近年来，研究者试图构建统一框架同时处理这两类任务，代表性工作包括 **TM2T**（Guo et al., ECCV 2022）、**MotionGPT**（Jiang et al., arXiv 2023）和 **MoTe**（Wu et al., arXiv 2024）。这些方法的共同范式是：将运动序列量化为离散token，然后与文本token一同输入单流Transformer骨干网络进行自回归建模。

然而，这一范式面临两个根本性瓶颈：

**瓶颈一：运动量化的近似误差。** 离散VQ-VAE编码将连续的人体运动压缩为有限码本索引，这一量化过程不可避免地引入信息损失。如组件消融实验（Table 4）所示，在相同架构下，连续VAE潜在空间在T2M任务上的R@3达到0.826，而VQ变体仅为0.800；在M2T任务上，VAE的MMDist为2.524，VQ则为2.775。量化误差直接限制了生成运动的精度和自然度。

**瓶颈二：单流架构的跨模态干扰。** 在单流Transformer中，文本和运动共享同一参数路径，两种模态的梯度在训练中相互干扰。Figure 3的训练曲线直观地揭示了这一问题：双流架构的扩散损失收敛速度约为单流的2倍，且在相同匹配损失下获得更高的R@3和更低的MMDist。这表明单流设计迫使模型在文本理解和运动生成之间做出表征妥协，既损害了生成质量，也降低了训练效率。

### 核心动机：运动作为“第二模态”

MotionGPT3的核心洞察在于重新审视运动模态在统一框架中的定位。此前方法将运动视为文本的“翻译目标”——通过量化将其强行纳入语言模型的token空间。这种设计忽略了运动模态自身的连续性和时空结构特性。

本文提出将人体运动作为与语言对等的**第二模态**（second modality），而非从属于语言的衍生表示。这一视角转变带来了三个关键设计原则：

1. **保留模态原生表示**：运动应以连续潜在向量而非离散token表示，避免量化带来的信息瓶颈。
2. **模态特定处理路径**：文本和运动应拥有独立的处理分支，仅在受控点进行跨模态交互，减少梯度干扰。
3. **模态适配的生成目标**：运动生成不应简单套用文本的自回归token预测范式，而应采用更适合连续信号的扩散建模。

### 现有方法的系统性缺口

从方法谱系来看，现有统一运动-语言模型存在以下结构性不足：

| 设计维度 | 现有方案 | 缺口 |
|---------|---------|------|
| 运动表示 | 离散VQ-VAE token（MotionGPT, TM2T, MoTe） | 量化损失限制生成精度上限 |
| 骨干架构 | 单流Transformer（MotionGPT, TM2T） | 模态间梯度干扰，收敛缓慢 |
| 运动生成头 | 自回归token预测（softmax over codebook） | 不适合连续运动信号的精细建模 |
| 训练策略 | 单阶段联合训练或直接多任务优化 | 缺乏对模态对齐的显式设计 |

值得注意的是，部分仅做生成的方法已探索了连续表示和扩散建模的优势，如 **MLD**（Xin et al., CVPR 2023）采用潜在扩散、**MoMask**（Guo et al., CVPR 2024）使用残差VQ，但这些方法不支持运动理解任务。**MG-MotionLLM**（Wu et al., arXiv 2025）虽尝试将运动token融入LLM，但仍沿用离散表示和单流范式。因此，如何在统一生成与理解的框架内同时解决量化误差和模态干扰，构成了本文的核心研究动机。



## 核心方法与创新机理

MotionGPT3 的核心创新可归结为三个相互关联的**changed slots**，分别指向运动表示、模型架构和训练策略的根本性重构，共同解决了先前统一运动-语言模型的两大瓶颈：运动量化带来的近似误差，以及单流骨干网络中跨模态表示的相互干扰。

### 1. 运动表示：从离散码本到连续 VAE 潜在空间

**Baseline 方案**（如 **MotionGPT** Jiang et al., 2023; **TM2T** Guo et al., ECCV 2022; **MoMask** Guo et al., CVPR 2024）普遍采用 VQ-VAE 将运动序列量化为离散码本索引，随后以自回归方式预测这些离散 token。这一范式将运动生成规约为标准的 next-token prediction，但其根本缺陷在于量化操作引入了不可逆的信息损失，直接限制了生成运动的质量上限。

**MotionGPT3 的替换**：采用连续 VAE 潜在空间替代离散码本。具体而言，运动序列 $m^{1:M}$ 通过编码器 $\mathcal{E}$ 映射为实值潜在向量 $z = \mathcal{E}(m^{1:M})$，解码器 $\mathcal{D}$ 再从 $z$ 重建运动序列 $\hat{m}^{1:L} = \mathcal{D}(z)$。VAE 的训练目标为重建损失与 KL 散度正则项的组合：

$$\mathcal{L} = \mathcal{L}_{\mathrm{rec}} + \lambda_{\mathrm{KL}} \mathcal{L}_{\mathrm{KL}}$$

其中 $\mathcal{L}_{\mathrm{rec}} = \frac{1}{T} \sum_{t=1}^{T} \| \boldsymbol{m}_t - \hat{\boldsymbol{m}}_t \|_2^2$ 为逐帧均方误差，$\mathcal{L}_{\mathrm{KL}} = D_{\mathrm{KL}}( \mathcal{N}(\mu, \mathrm{diag}(\sigma^2)) \| \mathcal{N}(0, I) )$ 约束潜在空间平滑。

**因果机制**：连续表示消除了量化瓶颈，保留了运动细节的完整信息流。组件消融实验（Table 4）直接验证了这一设计选择：在相同双流骨干下，VAE 变体在 T2M 任务上的 FID 为 0.239，显著优于 VQ 变体的 0.290；在 M2T 任务上，VAE 的 MMDist 为 2.524，同样优于 VQ 的 2.775。训练效率分析（Figure 3）进一步表明，VQ 潜在空间在验证指标上存在明显的质量天花板（R@3 约 0.5 即趋于饱和），而 VAE 连续空间则持续改善。

### 2. 骨干架构：从单流共享到双流分支

**Baseline 方案**（如 **MotionGPT** Jiang et al., 2023; **TM2T** Guo et al., ECCV 2022）采用单流 Transformer，文本和运动 token 共享同一组参数和前向路径。虽然这种设计简洁，但两种模态的表示学习在同一参数空间中相互竞争，产生严重的梯度干扰和表示折中。

**MotionGPT3 的替换**：引入双流 Transformer 架构，为文本和运动分别建立独立分支。文本分支 $\tau$ 基于冻结的预训练 GPT-2，保留语言先验；运动分支 $M$ 从零开始训练，捕捉运动特定的归纳偏置。两个分支各自维护独立的嵌入层、前馈网络和归一化模块，信息交换**仅**通过共享的自注意力层进行受控交互。此外，引入跨模态注意力（CMA）机制，仅在最后 $L$ 层启用，进一步限制模态间干扰的传播范围。

**因果机制**：模态解耦使得梯度信号不再相互污染。Figure 3 提供了直接的收敛证据：双流骨干使扩散损失的收敛速度约为单流的 2 倍，且在匹配损失（约 0.22）处，双流架构获得更高的 R@3 和更低的 MMDist。这一优势在不同 LLM 骨干（GPT-2、Flan-T5、Qwen2.5）上一致成立（Table 14），表明双流设计的增益具有架构无关的鲁棒性。CMA 层数的消融（Figure 4）揭示了非单调模式：性能随 $L$ 增加至 5 层持续改善，但 6 层时出现轻微退化，说明适度的跨模态交互是最优的，过度共享反而重新引入干扰。

### 3. 训练策略：从单阶段联合到三阶段渐进对齐

**Baseline 方案**（如 **MotionGPT** Jiang et al., 2023; **MoTe** Wu et al., 2024）通常采用单阶段联合训练或直接多任务优化，文本和运动分支从训练伊始即完全耦合。这种方式在统一生成与理解任务时面临困难：运动生成需要运动特定的特征学习，而语言理解需要保持预训练语言模型的语义能力，二者在同一优化目标下难以兼顾。

**MotionGPT3 的替换**：提出三阶段“生成-对齐-微调”训练计划：

- **Stage I (SI)：T2M 预训练**。冻结文本分支，仅训练运动分支和扩散头，使运动分支建立运动特定的表示基础。
- **Stage II (SII)：跨模态对齐**。引入运动理解任务（M2T），通过双向监督将运动分支与冻结的语言分支对齐。
- **Stage III (SIII)：联合微调**。解冻文本分支，所有模块联合优化，使两个模态在保持各自能力的同时实现深度融合。

**因果机制**：训练方案消融（Table 5 / Table 13）揭示了各阶段的因果贡献。省略 SI 直接进行 SII+SIII 会严重降低 T2M 质量（FID 从 0.215 升至更高值），表明运动特定的预训练是不可或缺的基础。仅执行 SI 已获得强生成能力（FID 0.239），但缺乏 M2T 能力；SII 在赋予理解能力的同时，进一步将 T2M 的 FID 降低 0.10、MMDist 降低约 0.2，表明跨模态对齐对生成任务本身也有正向溢出。完整三阶段方案实现了生成与理解的最佳平衡。

### 创新间的协同效应

三个 changed slots 并非孤立改进，而是形成因果链条：连续 VAE 潜在空间使运动表示摆脱量化约束，为扩散头（而非自回归 token 预测）提供了自然的连续目标空间；双流架构则为连续运动潜在向量和离散文本 token 提供了各自的处理路径，避免将异构表示强行塞入同一参数空间；三阶段训练策略进一步确保运动分支在不受语言分支干扰的前提下先建立运动先验，再逐步引入跨模态交互。Table 4 的组件消融直接验证了这一协同效应：Bimodal+VAE 配置在所有 T2M 和 M2T 指标上均显著优于 Unified+VQ、Unified+VAE 或 Bimodal+VQ 的任意组合，表明双流架构与连续表示的结合产生了超越各自独立贡献的增益。



![[assets/figures/papers/paper_list_l11_https_openreview_net_forum_id_Ha075JDMZR/figures/001_Figure_1.jpg]]
*Figure 1: Motion MotionFigure 1: MotionGPT3 introduces hybrid motion-language model that takes motion as a second Holdermodality and processes the data through a new branch, with cross-modal attention mechanism AdaLN Latentto communicate with text branch (Sec. 3.2). We leverage a VAE network for continuous motion representation (Sec. 3.1), and design separate training objective for each modality (Sec. 3.3)*

MotionGPT3 将人体运动视为与大语言模型（LLM）交互的**第二模态**，构建了一个双流运动-语言混合模型。其核心设计理念是：为运动模态建立独立分支，仅通过共享自注意力层与冻结的文本分支进行受控交互，从而避免传统单流架构中的模态间干扰和离散量化带来的信息损失。

### 三大核心组件

框架由三个松耦合的模块构成，形成“连续表示—双流交互—扩散生成”的流水线：

1.  **运动VAE（Motion VAE）**：负责将原始运动序列压缩为紧凑的连续潜在向量，并提供从潜在向量重建运动的能力。该模块独立预训练，为后续的双流模型提供一个**连续、低维且感知对齐**的运动表示，从根本上规避了离散码本（VQ-VAE）引入的量化误差。
2.  **双流运动-语言骨干网络（Dual-Stream Backbone）**：这是框架的核心。它由两个独立的Transformer分支组成：
    -   **文本分支**：基于冻结的预训练GPT-2，保持语言先验知识。
    -   **运动分支**：从零开始训练，捕捉运动特定的归纳偏置。
    
    两个分支仅在**共享的自注意力层**中进行信息交换，其余前馈网络和归一化层均保持独立。这种设计实现了模态特定路径的隔离，减少了梯度干扰。运动分支通过**运动理解头（MUH）**将连续潜在向量映射到Transformer的嵌入空间，支持运动理解任务（如运动描述生成）。
3.  **运动生成头（MGH / 扩散头）**：一个轻量级的扩散模块，接收运动分支的隐藏状态作为条件，通过去噪过程直接预测运动VAE的连续潜在向量，实现文本到运动（T2M）的生成。该设计将**潜在扩散模型**无缝集成到自回归骨干网络中，弥合了连续运动与离散文本表示之间的鸿沟。

### 输入输出与边界标记

模型的输入和输出通过特殊的**边界标记**进行组织，以触发不同的任务行为：
- **`<som>` 和 `<eom>`**：分别标记运动片段的开始和结束，用于在序列中插入运动模态。
- **`<motion_out>`**：作为运动生成的“占位符”，其对应的隐藏状态被送入扩散头以预测运动潜在向量。

在推理时，文本和运动分支各自处理其对应模态的数据。例如，对于文本到运动生成，文本分支处理输入描述，运动分支在 `<motion_out>` 标记处通过扩散头生成运动潜在向量，再由运动VAE解码器重建为运动序列。

### 三阶段训练策略

为了在生成和理解任务间取得平衡，模型采用一个精心设计的三阶段训练计划，逐步建立跨模态对齐：

- **第一阶段（SI）：T2M预训练**。仅训练运动分支和扩散头，文本分支冻结。此阶段专注于让运动分支学习运动特定的生成能力。
- **第二阶段（SII）：跨模态对齐**。引入运动理解任务，同时监督文本和运动两个模态的输出。此阶段赋予模型运动描述生成（M2T）能力，并进一步改善生成质量。
- **第三阶段（SIII）：联合微调**。解冻文本分支，对所有模块进行联合优化，以最大化生成与理解的整体性能。

消融实验证实，省略第一阶段（SI）会严重损害文本到运动的生成质量，表明运动特定的预训练对于最终性能至关重要（Table 5 / Table 13）。



### 运动VAE：连续潜在空间表示

MotionGPT3 摒弃了先前工作中普遍采用的离散 VQ-VAE 码本表示，转而使用连续 VAE 潜在空间来编码人体运动。其核心动机在于避免量化引入的近似误差——离散化过程不可避免地丢弃了运动序列中的细粒度信息，从而限制了生成运动的质量上限。

运动 VAE 采用基于 Transformer 的架构，编码器和解码器各由 9 层组成，配备 4 个注意力头，并通过跳跃连接保持信息流动。对于每个运动序列，编码器将其压缩为一个 $1 \times 1 \times 256$ 维的连续潜在向量 $z$，解码器则从该潜在向量重建原始运动：

$$\hat{m}^{1:L} = \mathcal{D}(\mathcal{E}(m^{1:M}))$$

其中 $m^{1:M}$ 表示长度为 $M$ 的原始运动序列，$\mathcal{E}$ 和 $\mathcal{D}$ 分别为编码器和解码器，$\hat{m}^{1:L}$ 为重建后的运动。

VAE 的总训练损失由重建损失和 KL 散度正则项构成：

$$\mathcal{L} = \mathcal{L}_{\mathrm{rec}} + \lambda_{\mathrm{KL}} \mathcal{L}_{\mathrm{KL}}$$

重建损失采用逐帧姿势的均方误差：

$$\mathcal{L}_{\mathrm{rec}} = \frac{1}{T} \sum_{t=1}^{T} \| \boldsymbol{m}_t - \hat{\boldsymbol{m}}_t \|_2^2$$

KL 散度项约束潜在空间向标准正态分布靠拢，保证潜在空间的平滑性和连续性：

$$\mathcal{L}_{\mathrm{KL}} = D_{\mathrm{KL}}\big( \mathcal{N}(\mu, \mathrm{diag}(\sigma^2)) \| \mathcal{N}(0, I) \big)$$

实验表明，连续 VAE 潜在空间在重建精度上全面优于 VQ-VAE，并在后续的生成和理解任务中带来更强的跨模态对齐性能（Table 4, Appendix C.1/C.2）。

### 双流Transformer骨干：模态分离与受控交互

MotionGPT3 的核心架构创新在于引入双流（Bimodal）Transformer，将文本和运动作为两个独立的模态分支处理。文本分支 $\tau$ 基于冻结的预训练 GPT-2，保持语言先验知识；运动分支 $M$ 从零开始训练，捕捉运动特定的归纳偏置。两个分支各自维护独立的嵌入层、前馈网络和归一化层，仅在共享自注意力层中进行信息交换。

这种设计的因果机制在于：单流架构中文本和运动共享同一参数路径，导致梯度在反向传播时相互干扰，迫使模型在两种模态的表示学习之间做出折中。双流架构通过解耦模态特定路径，使运动分支能够专注于学习运动语义，文本分支则保持其语言能力，从而缓解了跨模态干扰问题。

运动理解头（Motion Understanding Head, MUH）负责将连续的 VAE 潜在向量线性映射到 Transformer 的输入嵌入空间，使运动模态能够参与自回归语言建模。边界令牌 `<som>`、`<eom>` 和 `<motion_out>` 标记运动片段的起止位置，触发相应的生成或理解操作，并在训练中提供有限的交叉熵监督。

训练效率分析（Figure 3）提供了双流设计的关键证据：在 HumanML3D 数据集上，双流骨干使扩散损失的收敛速度约为单流架构的 2 倍。在匹配损失约为 0.22 的检查点上，双流架构获得了更高的 R@3 和更低的 MMDist，表明其不仅训练更快，而且收敛到更优的局部最优。消融实验进一步证实，双流+VAE 配置在 T2M 和 M2T 任务上均显著优于单流或 VQ 变体（Table 4）。

### 轻量级扩散头：桥接连续运动与自回归框架

运动生成头（Motion Generation Head, MGH）是连接连续运动潜在空间与自回归语言模型骨干的关键模块。其设计为一个轻量级的 3 层 MLP，采用 ResBlock 风格层，隐藏维度为 1024。扩散头以运动分支的隐藏状态 $h_m$ 为条件，在 VAE 潜在空间中执行去噪过程，预测目标运动潜在向量。

前向扩散过程对目标潜在向量 $z_0$ 施加高斯噪声扰动：

$$z_t = \sqrt{\bar{\alpha}_t} z_0 + \sqrt{1 - \bar{\alpha}_t} \epsilon, \quad \epsilon \sim \mathcal{N}(0, I)$$

其中 $\bar{\alpha}_t$ 为噪声调度参数，$t$ 为扩散时间步。扩散头 $\mathcal{H}$ 的训练目标是最小化噪声预测的均方误差：

$$\mathcal{L}_{\mathrm{diff}} = \mathbb{E}_{z_0, t, \epsilon} \Big[ \| \epsilon - \mathcal{H}(z_t, t, h_m) \|_2^2 \Big]$$

附录中给出了等价的 $\epsilon$ 预测变体形式：

$$L_{diff} = \mathcal{E}_{z_0, \epsilon, t} \lVert \epsilon - \hat{\epsilon}_{\theta} (\alpha_t z_0 + \sigma_t \epsilon, t, c) \rVert_2^2$$

消融实验（Table 11）表明，扩散头在生成质量上显著优于直接的 MSE 回归。此外，在将骨干隐藏状态映射到扩散条件时，多头注意力（MHA）池化模块优于简单的线性映射，进一步验证了扩散头设计的有效性。

### 三阶段训练策略

完整的训练方案分为三个阶段（Figure 2）：

- **阶段一（SI）：T2M 预训练**。文本分支冻结，仅监督运动输出，使运动分支学习运动特定的生成能力。
- **阶段二（SII）：跨模态对齐**。引入运动理解任务，同时监督文本和运动两个模态的输出，建立跨模态对齐。
- **阶段三（SIII）：联合微调**。解冻文本分支，对所有模块进行联合优化。

训练方案消融（Table 5 / Table 13）揭示了各阶段的因果作用：省略第一阶段会严重降低文本到运动的生成质量，表明运动特定的预训练不可或缺；第二阶段赋予了模型运动理解能力，并进一步改善了生成指标（FID 降低约 0.10，MMDist 降低约 0.2）；完整的三阶段方案实现了生成与理解的最佳平衡。

### 跨模态注意力层数

跨模态注意力（CMA）仅在 Transformer 的最后 $L$ 层启用。消融研究（Figure 4, Table 9）显示，随着 $L$ 从 1 增加到 5，T2M 性能持续改善；但当 $L=6$ 时出现轻微退化，呈现非单调模式。这表明适度的跨模态交互层数足以实现有效的信息流动，过多的共享层可能重新引入模态间干扰。



## 实验与关键发现

### 主实验结果

MotionGPT3 在 HumanML3D 和 KIT-ML 两个标准基准上进行了系统评估，涵盖文本驱动运动生成（T2M）和运动描述生成（M2T）两大任务。所有结果均基于 20 次重复评估并报告 95% 置信区间，与先前工作保持一致。

**HumanML3D 文本到运动生成。** 表 1（Table 1）汇总了主要对比结果。在仅生成（Gen. only）设置下，MotionGPT3† 在 R-Precision Top-1（0.533）和 Top-3（0.826）上均达到或接近最优水平，同时 FID 降至 0.239，MMDist 降至 2.797。在统一生成与理解（Gen. & Und.）设置下，MotionGPT3 进一步将 R@3 提升至 0.837，相比此前统一方法 MotionGPT（Jiang et al., 2023, arXiv）的 0.733 提升了 +0.104，FID 从 0.232 降至 0.208，验证了双流架构与连续潜在空间在统一框架中的显著优势。

![[assets/figures/papers/paper_list_l11_https_openreview_net_forum_id_Ha075JDMZR/figures/010_Table_1.jpg]]
*Table 1: Evaluation of text-guided motion generation on HumanML3D (Guo et al., 2022a). Rows are grouped by training tasks: Gen. only for generation-only and Gen. & Und. for both. Real is obtained by ground-truch motions, and → indicate values closer to Real are desirable. † marks our single-task model trained for 200 epochs, and MotionGPT3 is a three-stage model trained with unified tasks. Best and second-best results are highlighted in bold and underline*

**KIT-ML 文本到运动生成。** 表 2（Table 2）展示了 KIT-ML 上的结果。MotionGPT3† 的 R@3 达到 0.803，相比 MLD（Xin et al., CVPR 2023）的 0.734 提升了 +0.069，FID 降至 0.263，进一步证明了方法在不同数据集上的泛化能力。

![[assets/figures/papers/paper_list_l11_https_openreview_net_forum_id_Ha075JDMZR/figures/011_Table_2.jpg]]
*Table 2: Evaluation of text-guided motion generation on KIT-ML (Plappert et al., 2016)*

**运动描述生成（M2T）。** 表 3（Table 3）报告了 HumanML3D 上的运动描述生成结果。MotionGPT3†（单任务）和 MotionGPT3（统一模型）在 R@k 指标上均与近期最优方法持平，并在部分指标上超越了真实标注（GT）的指标水平。值得注意的是，统一模型在保持强生成能力的同时，也实现了高质量的运动理解，表明三阶段训练策略成功平衡了双向任务。

![[assets/figures/papers/paper_list_l11_https_openreview_net_forum_id_Ha075JDMZR/figures/012_Table_3.jpg]]
*Table 3: Comparison of motion captioning on HumanML3D (Guo et al., 2022a), evaluation follows (Guo et al., 2022c). MotionGPT3 † denotes our single-task captioning model trained for 100 epochs, and MotionGPT3 is an unified model trained on both tasks with the three-stage scheme (Sec. 3.4). Both variants achieve R@k on par with recent state of the art, and surpass the GT metrics*

**基于 TMR 评估器的检索性能。** 表 7（Table 7）展示了使用 TMR 评估器（Petrovich et al., 2023）的跨模态检索结果。在 All 协议下，MotionGPT3 的 Text-Motion R@1 达到 9.60，远超 TMR 的 5.68（+3.92）和 MotionGPT 的 6.71（+2.89），并在全部四个协议（All、All with threshold、Dissimilar subset、Small batches）中一致取得最优或次优的 R@k 和 MedR。这一结果说明连续潜在空间和双流架构产生的跨模态表征具有更强的语义对齐能力。

![[assets/figures/papers/paper_list_l11_https_openreview_net_forum_id_Ha075JDMZR/figures/024_Table_7.jpg]]
*Table 7: Retrieval on HumanML3D with the TMR evaluator (Petrovich et al., 2023). We report R@1/2/3/5/10 and MedR for text-motion retrieval under the four official protocols: (a) All, (b) All with threshold, (c) Dissimilar subset, and (d) Small batches (see Sec. C.2 for definitions). Results for TEMOS (Petrovich et al., 2022), T2M (Guo et al., 2022b), and TMR (Petrovich et al., 2023) are taken from the TMR paper. LaMP (Li et al., 2024b) is reported only for (d). MotionGPT and MotionGPT3 are evaluated with the released checkpoints using the official TMR code. MotionGPT3 attains strong performance across protocols*

---

### 训练效率分析

Figure 3 揭示了架构设计对训练效率的因果影响。在 HumanML3D 运动生成任务上，双流 + VAE 配置的扩散损失收敛速度约为单流 + VQ 配置的 2 倍。在匹配损失约 0.22 处（图中三角标记），双流架构实现了更高的 R@3 和更低的 MMDist，表明其在训练早期即可获得更优的生成质量。离散 VQ 潜在空间则在 R@3 约 0.5 处出现质量天花板，进一步验证了量化瓶颈是制约性能的关键因素。

![[assets/figures/papers/paper_list_l11_https_openreview_net_forum_id_Ha075JDMZR/figures/009_Figure_3.jpg]]
*Figure 3: Training loss and validation curves on motion generation on HumanML3D for architecture variants of dual-stream and single-stream and representation variants of VAE and VQ latents. The right figures illustrate validation metrics of R-Precision TOP 3 (R@3↑) and Multimodal Distance (MMDist↓). Triangle markers indicate matched-loss checkpoints (∼0.22). Our hybrid architecture with continuous motion representation helps accelerating convergence for about 2×, as well as achieves better quality especially in early training stage*

这一效率优势的机制在于：双流骨干使运动分支和文本分支各自专注于模态特定的优化目标，避免了单流模型中跨模态梯度干扰导致的表征妥协。连续 VAE 潜在空间则消除了离散码本的近似误差，使扩散头能够在平滑的连续空间中进行去噪。

---

### 消融实验

#### 组件消融：表示类型与架构设计

表 4（Table 4）系统消融了运动表示类型（VQ vs. VAE）和骨干架构（Unified 单流 vs. Bimodal 双流）对 T2M 和 M2T 性能的影响。所有变体使用相同的 GPT-2 风格分支和超参数，在相同协议下分别训练。

![[assets/figures/papers/paper_list_l11_https_openreview_net_forum_id_Ha075JDMZR/figures/013_Table_4.jpg]]
*Table 4: Component ablations on HumanML3D for representation choice and architecture design. Unified denotes a single-stream backbone, where one branch is shared by text and motion, as employed in Jiang et al. (2023), and Bimodal denotes a dual-stream backbone described in Sec. 3.2. VQ and VAE indicate discrete and continuous motion latents, respectively. For each configuration we train separate models for motion generation (T2M) and motion captioning (M2T) under the same protocol and report test-set metrics. All variants share the same GPT-2-style branch and hyperparameters. and training is run for 100 epochs on M2T and 200 epochs on T2M. Best and second-best results are highlighted in bold and und...*

![[assets/figures/papers/paper_list_l11_https_openreview_net_forum_id_Ha075JDMZR/figures/017_Table_4.jpg]]
*Table 4: Reconstruction performance of a continuous VAE (Xin et al., 2023) versus a discrete VQ-VAE (Jiang et al., 2023). The VQ-VAE shows consistently higher errors, consistent with information loss introduced by quantized encoding and decoding. Sec. D.3 presents the metric definitions*

- **T2M 任务**：Bimodal + VAE 配置在所有指标上均取得最优或次优结果（R@1 0.533, R@3 0.826, FID 0.239, MMDist 2.797）。相比之下，Unified + VQ 配置的 FID 为 0.297，MMDist 为 2.888，性能差距显著。
- **M2T 任务**：Bimodal + VAE 的 MMDist 降至 2.524，相比 Bimodal + VQ 的 2.775 降低了 0.251，表明连续潜在空间在运动理解任务中同样具有更强的对齐能力。

这一消融直接验证了核心洞察：将连续 VAE 潜在空间与双流架构结合，可以同时消除量化损失和模态间干扰，从而在生成和理解两个方向上均获得显著增益。

#### 训练方案消融

表 5（Table 5）和附录表 13（Table 13）消融了三阶段训练策略中不同阶段组合的效果。

![[assets/figures/papers/paper_list_l11_https_openreview_net_forum_id_Ha075JDMZR/figures/016_Table_5.jpg]]
*Table 5: Ablation on training-scheme. Enabled stages are marked with $\checkmark$ . , and colors encode the text branch updated or frozen. Best results are bold and second best are underlined*

![[assets/figures/papers/paper_list_l11_https_openreview_net_forum_id_Ha075JDMZR/figures/018_Table_5.jpg]]
*Table 5: Discrete (VQ) vs. continuous (VAE) motion representations under single-task training. We report both T2M on R@1, FID, MMDist, DIV and M2T on R@3, BLEU@1/4, ROUGE. With fewer training epochs, VAE-variants achieve stronger alignment and better quality. VQ requires extended training of 399 epochs while still remains behind on most alignment and language scores*

- **仅 SI（T2M 预训练）**：已能提供较强的运动生成能力（FID 0.239），验证了运动特定预训练的必要性。
- **SI + SII（增加跨模态对齐）**：在保持生成质量的同时，赋予了模型 M2T 能力，FID 进一步降至 0.215，MMDist 降低约 0.2。
- **SI + SII + SIII（联合微调）**：实现了生成与理解的最佳平衡。
- **省略 SI**：直接使用 SII + SIII 的两阶段方案导致 T2M 性能严重退化，FID 显著升高，表明第一阶段对学习运动特定特征不可或缺。

此外，表 13 揭示了文本分支冻结策略的关键作用：若从训练伊始就联合更新文本分支，虽然能在 SI 阶段略微改善早期 T2M，但最终会损害 SII 后的 T2M 质量，并显著降低 M2T 分数。这进一步支持了分阶段解耦训练的设计原则。

#### 跨模态注意力层数消融

Figure 4 展示了跨模态注意力（CMA）层数对 T2M 性能的影响。CMA 在最后 L 层启用，L 从 1 到 6 进行扫描。MMDist 随 L 增加持续下降，在 L=5 时达到最低点（约 2.82），但 L=6 时出现轻微退化。这一非单调模式表明，适度的跨模态交互足以实现有效对齐，过多的共享层可能重新引入模态间干扰。

![[assets/figures/papers/paper_list_l11_https_openreview_net_forum_id_Ha075JDMZR/figures/015_Figure_4.jpg]]
*Figure 4: Ablation on the number of cross-modal attention (CMA) layers for T2M on HumanML3D. CMA is enabled in the last L layers ( L $\in { 1 , \dots , 6 }$ ) . Performance improves as L increases up to 5 layers, then shows slight degradation at 6, indicating a non-monotonically pattern

#### 运动生成头消融

表 11（Table 11）消融了运动生成头的设计选择：

- **扩散头 vs. 直接 MSE 回归**：扩散头在生成质量上显著优于 MSE 回归，验证了在连续潜在空间中进行去噪建模的有效性。
- **MHA 池化 vs. 线性映射**：使用多头注意力（MHA）将骨干隐藏状态映射为扩散条件，优于简单的线性映射，表明运动生成需要更丰富的条件聚合机制。
- **Holder 数量**：运动输出 token `<motion_out>` 的数量对性能有影响，需要适当配置。
- **分类器自由引导（CFG）**：CFG 对生成质量有显著影响，但其最优强度需要针对不同模型重新搜索。

#### 运动分支容量消融

Figure 9 和表 10（Table 10）探索了运动分支容量对性能的影响。一个 124M 的文本分支配合约 51M 的运动参数即可实现与更大骨干（355M/774M）相竞争的性能（MMDist 约 2.6），表明运动分支不需要与文本分支等量齐观即可有效工作。但过大的未预训练运动分支容量可能导致训练不稳定，需要在容量与稳定性之间取得平衡。

#### 不同 LLM 骨干的泛化性

表 14（Table 14）验证了双流架构在不同 LLM 骨干（GPT-2、Flan-T5、Qwen2.5）上的一致优势。在所有骨干上，双流架构均优于单流架构，证明了该设计原则的通用性，而非特定于某一语言模型的偶然现象。

---

### 失败模式与局限性

尽管 MotionGPT3 在多个基准上取得了最优性能，分析中仍识别出以下局限：

1. **数据集规模限制**：当前验证主要在 HumanML3D 和 KIT-ML 两个中小规模基准上进行，尚未在大规模、更复杂的运动数据集上测试，方法的可扩展性有待进一步验证。
2. **训练策略的手动设计**：三阶段训练策略虽然有效，但阶段划分和冻结策略仍需人工设计，可能难以自动适应新模态或新任务。
3. **运动分支容量约束**：运动分支容量受限于当前语言模型规模，直接引入超大运动分支会导致训练不稳定，需要更大规模配对企业数据或额外预训练来支撑。
4. **CFG 超参数敏感性**：分类器自由引导对生成质量有显著影响，但其最优强度需要针对不同模型配置重新搜索，增加了实际部署的调参成本。
5. **纯文本语料利用不足**：跨模态对齐主要通过配对数据进行，未能充分挖掘纯文本语料中蕴含的语言知识，可能限制了语言分支在复杂语义理解上的潜力。

### 补充图表

![[assets/figures/papers/paper_list_l11_https_openreview_net_forum_id_Ha075JDMZR/figures/019_Table_6.jpg]]
*Table 6: Comprehensive comparison of text-to-motion generation on HumanML3D (Guo et al., 2022a). We report generation-only models (Gen. only) here, and visualize unified dual-task models (Gen. & Und.) in Fig. 8. Real denotes ground-truth statistics; arrows (→) indicate that values closer to Real are desirable. † marks our single-task model trained for 200 epochs, and MotionGPT3 is the unified three-stage model. Best and second-best results are bold and underlined*



## 定位与知识库关联

### 1. 在统一运动-语言模型谱系中的位置

MotionGPT3 处于将人体运动作为"第二模态"整合进语言模型的研究前沿。其直接前身是 **MotionGPT**（Jiang et al., arXiv 2023），后者首次尝试将运动与文本统一为离散令牌，通过单流Transformer进行自回归建模。然而，该范式存在两个根本性瓶颈：**运动量化引入的近似误差**限制了生成运动的保真度，而**单流骨干中离散文本与连续运动的联合处理**加剧了跨模态干扰。

MotionGPT3 通过两项关键设计突破了上述瓶颈：

- **连续VAE潜在空间替代离散码本**：与 **T2M-GPT**（Zhang et al., ICCV 2023）、**MoMask**（Guo et al., CVPR 2024）等仅生成方法采用的VQ-VAE路线不同，MotionGPT3 借鉴了 **MLD**（Xin et al., CVPR 2023）的连续潜在扩散思想，但将其从独立的生成模型迁移到统一的运动-语言框架中。这一转变消除了码本量化的信息损失，使得运动重建精度和跨模态对齐性能均显著提升（Table 4, Appendix C.1/C.2）。

- **双流Transformer架构**：不同于 **TM2T**（Guo et al., ECCV 2022）、**MoTe**（Wu et al., arXiv 2024）和 **MG-MotionLLM**（Wu et al., arXiv 2025）等延续单流范式的统一模型，MotionGPT3 引入独立的文本分支和运动分支，仅通过共享自注意力层进行受控交互。这一设计使得文本分支可以冻结预训练的GPT-2权重以保持语言先验，而运动分支从零开始学习运动特定的归纳偏置，从而有效缓解了模态间梯度干扰（Figure 3）。

### 2. 核心设计决策与因果机制

MotionGPT3 的四个关键设计槽位及其因果效应如下：

| 设计槽位 | 基线取值 | 本文取值 | 因果机制 |
|:---|:---|:---|:---|
| 运动表示 | 离散VQ-VAE令牌 | 连续VAE潜在向量 | 消除码本量化瓶颈，提升重建精度与对齐质量 |
| 骨干架构 | 单流Transformer | 双流Transformer | 解耦模态特定路径，减少梯度干扰，加速收敛约2倍 |
| 运动生成头 | 自回归token预测 | 轻量级扩散头 | 在连续潜在空间去噪，避免离散预测的累积误差 |
| 训练策略 | 单阶段联合训练 | 三阶段"生成-对齐-微调" | 分阶段引入跨模态对齐，平衡生成与理解能力 |

**决定性证据**来自组件消融实验（Table 4）：双流+VAE配置在T2M和M2T任务上均显著优于单流或VQ变体。具体而言，双流+VAE在T2M上的FID为0.239，而单流+VQ为0.305；在M2T上的MMDist为2.524，而双流+VQ为2.775。训练效率分析（Figure 3）进一步表明，双流骨干使扩散损失的收敛速度提高约2倍，且在匹配损失（~0.22）下获得更高的R@3和更低的MMDist。

### 3. 适用边界与局限

尽管MotionGPT3在HumanML3D和KIT-ML两个标准基准上取得了领先性能，其适用边界仍存在以下约束：

1. **数据规模限制**：当前验证集中在中小规模基准（HumanML3D约15k序列，KIT-ML约4k序列），尚未在大规模、高多样性的运动数据集上测试。运动分支的容量受限于语言模型规模，直接引入超大运动分支会导致训练不稳定（Figure 9, Table 10），需要更大规模配对企业数据或额外的运动预训练。

2. **训练策略的手动设计**：三阶段训练方案虽然有效，但阶段划分、迭代分配（SI: 100k, SII: 300k, SIII: 50k）和文本分支冻结策略均需手动设定。省略第一阶段（SI）会严重降低生成质量（Table 5/Table 13），表明运动特定的预训练不可或缺，但如何自动化这一过程仍是开放问题。

3. **跨模态注意力层数的非单调性**：CMA层数从1增加到5持续改善T2M性能，但6层时出现退化（Figure 4）。这表明模态交互的"最佳深度"需要针对不同骨干和数据集重新搜索，缺乏理论指导。

4. **分类器自由引导（CFG）的敏感性**：CFG对生成质量有显著影响（Table 11），但其最优强度依赖于具体模型配置，需要额外的超参数搜索。

5. **纯文本语料的利用不足**：跨模态对齐主要通过配对企业数据进行，未能充分挖掘纯文本语料中蕴含的语言知识，可能限制了语言分支在理解任务上的潜力。

### 4. 开放问题与未来方向

基于上述局限，以下研究方向值得关注：

- **更大规模验证与扩展**：当采用更强的基础语言模型（如LLaMA、Mistral）时，双流架构和三阶段训练是否仍然有效？需要何种规模的配对企业数据？Table 14已初步展示了在GPT-2、Flan-T5和Qwen2.5上双流一致优于单流，但更大规模模型的验证仍然缺失。

- **纯文本语料的整合**：如何将多样化的纯文本语料自然地整合到最终对齐阶段（SIII），以增强语言理解而不损害运动生成？这可能需要设计新的训练目标或数据增强策略。

- **可控与长序列生成**：如何在双流框架下开发具有局部语义对齐和分段控制的可控运动生成，面向长期复杂运动序列？当前框架主要处理单段运动生成，分段控制和时序组合能力尚未探索。

- **跨模态泛化**：连续潜在空间和扩散头的组合是否可推广到其他连续模态（如音频、视频），形成统一的生成框架？这需要验证VAE+扩散范式在不同模态特性下的鲁棒性。

- **自动化模态交互策略**：是否存在更自动化的模态交互策略，以取代当前需要手动设计CMA层数和冻结策略的方案？例如，基于可微分架构搜索或动态路由机制的自适应交互可能是一个有前景的方向。



## 原文 PDF

![[paperPDFs/ICLR_2026/MotionGPT3_Human_Motion_as_a_Second_Modality.pdf]]
