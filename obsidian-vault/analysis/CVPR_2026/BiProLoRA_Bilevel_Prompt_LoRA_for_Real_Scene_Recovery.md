---
title: "BiProLoRA: Bilevel Prompt LoRA for Real Scene Recovery"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/BiProLoRA_Bilevel_Prompt_LoRA_for_Real_Scene_Recovery.pdf
project_link: null
code_link: "https://github.com/Defender0527/BiProLoRA"
aliases:
- BBPL
- BiProLoRA
tags:
- CVPR_2026
- topic/other_unclear
- topic/other_unclear/general
core_operator: 通过自监督分布保真度学习（DFL）在潜在空间中对齐真实退化分布，再以双层超参数优化框架将提示嵌入（退化感知调节器）与LoRA（结构恢复能力）解耦并实现相互促进，从而达成合成到真实的鲁棒适应。
primary_logic: LoRA提供可复用的结构恢复能力，提示嵌入作为轻量退化感知调制器在不改变核心权重的前提下引导该能力的发挥，二者通过双层优化实现协同——下层在合成数据上训练LoRA以保留结构先验，上层在真实数据上优化提示以调控适应行为。
claims:
- 双层优化框架（Eq. 1）将结构学习与退化适应分离，上层在真实数据上优化提示θ，下层在合成数据上优化LoRA ω，实现了合成到真实的有效迁移。
- 消融实验证实仅用提示嵌入（无LoRA）时NIQE恶化至6.321，而完整BiProLoRA达到2.971，验证了LoRA结构恢复与提示退化调节的互补必要性（Table 4）。
- 移除DFL导致定量性能下降且视觉质量变差，证实了在去噪前校准真实分布一致性的必要。
- 双层联合建模（HO）策略优于朴素联合训练（Naive），在NIQE、LIQE、DE三项指标上均有显著提升。
---

# BiProLoRA: Bilevel Prompt LoRA for Real Scene Recovery

> [!tip] 核心洞察
> LoRA提供可复用的结构恢复能力，提示嵌入作为轻量退化感知调制器在不改变核心权重的前提下引导该能力的发挥，二者通过双层优化实现协同——下层在合成数据上训练LoRA以保留结构先验，上层在真实数据上优化提示以调控适应行为。

| 字段 | 内容 |
|------|------|
| 中文题名 | BiProLoRA：面向真实场景恢复的双层提示低秩适配 |
| 英文题名 | BiProLoRA: Bilevel Prompt LoRA for Real Scene Recovery |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/An_BiProLoRA_Bilevel_Prompt_LoRA_for_Real_Scene_Recovery_CVPR_2026_paper.html) · [Code](https://github.com/Defender0527/BiProLoRA) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | BiProLoRA (Bilevel Prompt LoRA) |
| Dataset | DARKFACE, ExDark, RTTS, URPC |

> [!tip] 效果简介
> - DARKFACE (seen real low-light) 上，NIQE↓ 2.971 vs 3.030 (Zero-IG) (-0.059)；LIQE↑ 2.585 vs 2.135 (SCI++) (+0.450)。
> - ExDark (unseen real low-light) 上，NIQE↓ 3.806 vs 3.920 (Zero-IG) (-0.114)。
> - RTTS (real hazy scene) 上，NIQE↓ 3.972 vs 4.059 (PHAT) (-0.087)。

## 概要

真实场景图像恢复面临一个根本性瓶颈：预训练扩散模型的自编码路径未针对真实退化分布进行校准，导致恢复结果出现纹理失真；同时，去噪器的结构恢复能力与退化处理能力被耦合在单一参数空间中，难以适应未见过的复杂退化。BiProLoRA 针对这一问题，提出了一种双层提示低秩适配（Bilevel Prompt LoRA）学习范式，核心思路是将 LoRA 提供的可复用结构恢复能力与提示嵌入（Prompt）提供的轻量退化感知调制能力解耦，并通过双层超参数优化框架实现二者的相互促进，从而达成从合成数据到真实场景的鲁棒迁移。

方法上，BiProLoRA 包含两个关键阶段。第一阶段为自监督分布保真度学习（DFL），通过在 VAE 编码器与解码器之间插入轻量双层零卷积适配器，直接在真实退化数据上以 L1 损失进行训练，将任务无关的真实退化分布编码到潜在表示中，为后续去噪提供纹理保真度保障。第二阶段为双层联合建模：下层在合成配对数据上优化 LoRA 权重以保留结构恢复先验，上层在无参考的真实数据上通过 CLIP 对比损失优化提示嵌入以实现退化适应，二者通过惩罚式单层重构实现高效协同训练。

实验层面，BiProLoRA 在三个真实退化场景（低光、雾霾、水下）上进行了全面评估。在 DARKFACE 真实低光数据集上，BiProLoRA 取得了 NIQE 2.971 和 LIQE 2.585 的最优结果，分别优于对比基线 Zero-IG（NIQE 3.030）和 SCI++（LIQE 2.135）；在未见过的 ExDark 数据集上，NIQE 降至 3.806，领先 Zero-IG 的 3.920。在真实雾霾（RTTS）和水下（URPC）场景中，BiProLoRA 同样以 NIQE 3.972 和 3.514 取得最优。在夜间目标检测下游任务上，mAP 达到 40.9，比 Baseline 提升 3.4 个百分点。值得注意的是，所有训练仅使用约 50 张真实图像（约为合成数据的 10%），验证了方法在极端数据不平衡下的有效性。

消融实验进一步揭示了各组件的因果贡献：移除 DFL 导致 NIQE 从 2.971 恶化至 4.074，证实了分布校准的必要性；仅使用提示嵌入（无 LoRA）时 NIQE 恶化至 6.321，验证了 LoRA 结构恢复与提示退化调节的互补性；双层联合建模（HO）策略在 NIQE、LIQE、DE 三项指标上均优于朴素联合训练，证实了超参数优化视角下解耦设计的有效性。

真实场景下的图像恢复（如低光增强、去雾、水下清晰化）是计算机视觉中的长期挑战。与合成退化不同，真实退化分布复杂、多样且缺乏成对参考真值，使得基于全监督学习的传统方法难以有效泛化。近年来，预训练扩散模型（如 **SD-Turbo**，Sauer et al., ECCV 2024）凭借其强大的生成先验，在图像恢复任务中展现出显著潜力。然而，将这些模型从合成数据适配到真实场景时，仍面临两个核心瓶颈。

**瓶颈一：自编码路径的分布失配。** 预训练扩散模型的VAE编码器-解码器仅在合成数据上训练，其潜在空间并未针对真实退化分布进行校准。当直接处理真实退化图像时，编码产生的潜在表示会偏离模型预期的分布，导致纹理失真和细节丢失。这一问题的本质在于，去噪过程的上游——自编码路径——缺乏对真实数据分布的一致性学习，使得后续的结构恢复建立在不可靠的表示之上。

**瓶颈二：结构恢复与退化适应的参数耦合。** 现有适配方案通常采用全模型微调或单一参数空间的学习策略（如 **LoRA**，Hu et al., ICLR 2022），将结构恢复能力与退化处理能力耦合在同一组权重中。这种耦合带来两个问题：其一，在真实数据稀缺且无参考信号的条件下，耦合的参数空间难以稳定地学习到有效的退化适应策略；其二，适配后的权重紧密绑定于训练分布，面对未见过的退化类型时泛化能力不足。

上述瓶颈揭示了一个关键的因果机制：**结构恢复需要稳定、可复用的映射能力，而退化适应则需要轻量、灵活的调控机制，二者本质上是可解耦的**。现有方法将二者混为一谈，导致在真实场景中顾此失彼——要么牺牲结构保真度以换取退化处理，要么在退化适应上妥协以维持结构先验。

基于这一洞察，本文提出 **BiProLoRA（Bilevel Prompt LoRA）**，一种面向真实场景恢复的双层提示低秩适配学习范式。其核心思想是：将LoRA作为可复用的结构恢复能力载体，将可学习提示嵌入作为轻量退化感知调制器，通过双层超参数优化框架实现二者的解耦与协同——下层在合成数据上训练LoRA以保留结构先验，上层在真实数据上优化提示以调控适应行为，从而在合成到真实的迁移中达成鲁棒的平衡。

## 核心方法与创新机理

BiProLoRA 的核心创新在于通过**双层超参数优化框架**将预训练扩散模型的适配过程解耦为两个互补的维度，并辅以**自监督分布保真度学习**在去噪前校准潜在空间，从而系统性地解决了合成到真实场景迁移中的两个关键瓶颈。

### 瓶颈诊断：耦合与失配

预训练扩散模型（如 **SD-Turbo**，Sauer et al., ECCV 2024）在真实场景恢复中面临双重困境：

1.  **自编码路径失配**：标准 VAE 编码器/解码器仅在合成数据上预训练，其潜在空间未针对真实退化分布进行校准，导致纹理细节在编码-解码过程中失真。
2.  **参数空间耦合**：去噪 UNet 的结构恢复能力与退化处理能力被耦合在单一参数空间中。全模型微调不仅成本高昂，更使得适配后的权重紧密绑定于训练分布，难以泛化至未见过的复杂退化。

BiProLoRA 的设计直指这两大瓶颈，通过两个阶段实现解耦与校准。

### 创新一：自监督分布保真度学习（DFL）

在去噪过程之前，DFL 模块承担起校准自编码路径的任务。其核心操作是：暂时分离 UNet，在 VAE 编码器与解码器之间插入轻量的**双层零卷积适配器** $A_\pi$，直接在真实退化数据 $\mathcal{D}_{\mathrm{real}}$ 上以 L1 损失进行训练。该训练同时在特征层和像素层施加约束，迫使适配器将任务无关的真实退化分布编码到潜在表示中，从而在源头上保证了纹理保真度。消融实验证实，移除 DFL 会导致 NIQE 显著恶化（从 2.971 升至 4.074），且视觉质量明显下降，验证了在去噪前对齐分布一致性的必要性。

### 创新二：提示-LoRA 双层联合建模

在完成分布校准后，BiProLoRA 通过双层超参数优化框架，将适配过程解耦为两种互补机制：

- **LoRA 低秩适配**（Hu et al., ICLR 2022）：仅对 UNet 选定层施加低秩更新，提供可复用的结构恢复能力。其核心使命是在合成配对数据 $\mathcal{D}_{\mathrm{syn}}$ 上学习稳健的结构恢复映射，优化成本低且不破坏预训练先验。
- **可学习提示嵌入** $P_\theta$：作为轻量退化感知调节器，通过条件接口引导模型。提示嵌入在不改变核心结构先验权重的前提下，调控 LoRA 所提供能力的发挥方式，使模型能够灵活适应未见过的退化类型。

二者的关系被形式化为双层优化问题：

$$
\min_{\theta} \ell_{\mathrm{real}}(\theta, \omega^*(\theta); \mathcal{D}_{\mathrm{real}}), \quad \mathrm{s.t.} \ \omega^*(\theta) \in \arg\min_{\omega} \ell_{\mathrm{syn}}(\omega, \theta; \mathcal{D}_{\mathrm{syn}})
$$

其中**上层**在真实数据上优化提示 $\theta$ 以实现退化适应，**下层**在合成数据上优化 LoRA $\omega$ 以保持结构恢复能力。这一设计的核心洞察在于：LoRA 与提示嵌入存在天然的互补性——LoRA 负责“能恢复什么”，提示嵌入负责“如何调控这种能力”。

### 创新三：惩罚式高效训练策略

为高效求解上述双层问题，BiProLoRA 将其重构为带惩罚项的单层优化，并通过 **Mirror LoRA 内循环**机制近似下层值函数。具体而言，在每次外层更新前，先对 LoRA 副本 $\tilde{\omega}$ 在合成数据上执行 $T$ 步快速优化，获得当前提示引导下的理想结构恢复参考 $\tilde{\omega}_T$。随后，Primary LoRA 的梯度更新由真实数据弱引导和合成数据正则化共同组成：

$$
g_{\omega} = \nabla_{\omega} \ell_{\mathrm{real}}(\theta, \omega) + \lambda \nabla_{\omega} \ell_{\mathrm{syn}}(\theta, \omega)
$$

提示嵌入的梯度则主要由真实场景目标驱动，惩罚项 $\nabla_{\theta} \ell_{\mathrm{syn}}(\theta, \tilde{\omega}_T)$ 防止提示选择严重损害 LoRA 合成最优结构的配置：

$$
g_{\theta} = \nabla_{\theta} \ell_{\mathrm{real}}(\theta, \omega) + \lambda \big( \nabla_{\theta} \ell_{\mathrm{syn}}(\theta, \omega) - \nabla_{\theta} \ell_{\mathrm{syn}}(\theta, \tilde{\omega}_T) \big)
$$

消融实验强有力地验证了这一设计的有效性：仅使用提示嵌入（无 LoRA）时 NIQE 恶化至 6.321，而完整 BiProLoRA 达到 2.971，证实了 LoRA 结构恢复与提示退化调节的互补必要性；双层联合建模（HO）策略在 NIQE、LIQE、DE 三项指标上均显著优于朴素联合训练（Naive），证明了从超参数优化视角进行联合建模的优越性。

### 与基线方法的范式对比

| 适配维度 | 基线方案 | BiProLoRA 方案 |
|---------|---------|---------------|
| 自编码路径 | 标准 VAE，未针对真实退化校准 | DFL：在真实数据上以 L1 损失训练轻量适配器，对齐退化分布 |
| 权重适配 | 全模型微调，结构恢复与退化处理耦合 | LoRA 低秩适配：解耦结构恢复映射，降低优化成本 |
| 条件调制 | 标准文本条件或无提示调优 | 可学习提示嵌入：退化感知调节器，不改变核心权重 |
| 优化框架 | 合成数据上的单层优化 | 双层超参数优化：上层（真实数据）优化提示，下层（合成数据）优化 LoRA |

值得注意的是，整个训练仅使用 50 张真实图像（约为合成数据的 10%），在这种极度不平衡的数据设置下，BiProLoRA 在 DARKFACE、ExDark、RTTS、URPC 等多个真实退化基准上均取得了最优的无参考指标表现，并展现出对未见场景的强大泛化能力。

BiProLoRA 的整体学习范式遵循“先校准分布，再解耦适配”的两阶段流水线，如图2所示。其核心设计动机源于一个关键瓶颈：预训练扩散模型（以 **SD-Turbo** (Sauer et al., ECCV 2024) 为基础）的自编码路径未针对真实退化分布进行校准，导致纹理失真；同时，去噪器的结构恢复能力与退化处理能力被单一参数空间耦合，难以泛化至未见过的复杂退化。为解开这一耦合，BiProLoRA 将适配过程分解为两个在功能与数据层面相互解耦的阶段。

**第一阶段：分布保真度学习（DFL）**。该阶段在去噪之前独立执行，目标是让 VAE 的自编码路径“认识”真实世界的退化分布。具体而言，在冻结的 VAE 编码器与解码器之间插入轻量的双层零卷积适配器 $A_\pi$，直接在无配对的真实退化数据 $\mathcal{D}_{\text{real}}$ 上以自监督方式训练，损失函数同时约束特征层与像素层的 L1 重建误差。这一设计将任务无关的真实退化特征显式编码到潜在表示中，为后续的任务特定适配提供纹理保真度保障。DFL 训练收敛后，适配器参数 $\pi$ 被冻结，不再参与后续优化。

**第二阶段：双层提示低秩适配（BiProLoRA）**。该阶段从超参数优化的视角，将结构恢复与退化适应分别交由 LoRA 权重 $\omega$ 与可学习提示嵌入 $\theta$ 承担，并通过双层优化实现二者的相互促进。其因果机制可概括为：LoRA 提供可复用的结构恢复能力，提示嵌入作为轻量退化感知调制器，在不改变核心权重的前提下引导该能力的发挥。流水线的数据流与模块关系如下：

1. **输入**：真实退化图像与合成配对退化图像分别构成上层与下层优化的数据源。
2. **Mirror LoRA 内循环**：在下层，以当前提示 $\theta$ 为条件，在合成数据 $\mathcal{D}_{\text{syn}}$ 上对 LoRA 副本 $\tilde{\omega}$ 执行 $T$ 步快速梯度更新，获得理想的结构恢复参考 $\tilde{\omega}_T$。这一步本质上是在回答“给定当前的退化调控策略，最优的结构恢复应该是什么样的”。
3. **Primary LoRA 更新**：核心 LoRA 权重 $\omega$ 的梯度由两部分组成——真实数据的弱引导项 $\nabla_{\omega} \ell_{\text{real}}$ 与合成数据的正则化项 $\lambda \nabla_{\omega} \ell_{\text{syn}}$，确保适应真实退化时不遗忘结构恢复的核心使命。
4. **Prompt 嵌入更新**：提示 $\theta$ 的更新主要由真实场景目标驱动，惩罚项 $\lambda (\nabla_{\theta} \ell_{\text{syn}}(\theta, \omega) - \nabla_{\theta} \ell_{\text{syn}}(\theta, \tilde{\omega}_T))$ 则防止提示选择严重偏离合成最优结构的配置。
5. **损失函数**：下层合成损失 $\ell_{\text{syn}}$ 由 L2 损失与 LPIPS 感知损失组合而成；上层真实损失 $\ell_{\text{real}}$ 采用基于 CLIP 的对比损失，通过最大化恢复结果与正提示文本的余弦相似度，在无参考设定下提供训练信号。
6. **输出**：经适配的扩散模型可直接对真实退化图像进行端到端恢复，输出增强后的干净图像。

整个框架的关键特性在于**数据效率**与**模块解耦**：DFL 与 BiProLoRA 的训练仅需约 50 张真实图像（约为合成数据的 10%），且各模块职责明确——DFL 负责分布对齐，LoRA 负责结构恢复，提示嵌入负责退化调制，三者通过双层优化的梯度流实现协同而非耦合。

### 2.1 整体架构概览

BiProLoRA 的学习范式由两个顺序阶段构成（Figure 2）：首先通过**分布保真度学习（DFL）**在去噪前校准自编码路径的真实退化分布，随后通过**双层联合建模**实现 LoRA 结构恢复能力与提示嵌入退化感知调制之间的相互促进。以下逐一展开各核心模块及其关键公式。

---

### 2.2 分布保真度学习（DFL）

预训练扩散模型（如 **SD-Turbo**，Sauer et al., ECCV 2024）的 VAE 编码器/解码器仅在合成数据上训练，其潜在表示未针对真实退化分布进行校准，导致纹理失真。DFL 模块在去噪 UNet 介入之前，直接在真实退化数据 $\mathcal{D}_{\mathrm{real}}$ 上训练轻量适配器 $A_\pi$，将任务无关的真实退化分布编码到潜在空间中。

具体而言，DFL 暂时分离 UNet $U$，在 VAE 编码器 $\mathcal{E}$ 与解码器 $\mathcal{D}$ 之间插入可学习的双层零卷积适配器 $A_\pi$（参数 $\pi$），以 $\ell_1$ 损失在特征层和像素层同时约束重建：

$$\pi_{n+1} \leftarrow \pi_n - \delta \nabla_{\pi} \ell_1(\pi_n)$$

其中 $\delta$ 为学习率。该阶段完成后，适配器参数被冻结，后续去噪过程在已校准的潜在空间中进行。消融实验证实，移除 DFL 会导致 NIQE 从 2.971 恶化至 4.074（Table 4），验证了分布一致性学习对纹理保真度的必要性。

---

### 2.3 双层联合建模：LoRA 与提示嵌入的协同

#### 2.3.1 互补性分析

**LoRA**（Hu et al., ICLR 2022）通过对 UNet 选定层施加低秩更新 $\Delta W = BA$，提供可复用的结构恢复能力，但其将任务特定的真实退化学习耦合在单一参数空间中，难以泛化至未见退化。**可学习提示嵌入** $P_\theta$ 作为轻量退化感知调制器，通过条件接口引导模型，在不改变核心权重的前提下调控预训练能力。二者的自然互补性构成双层建模的动机：LoRA 提供稳健的结构恢复基底，提示嵌入充当退化感知调节器。

#### 2.3.2 双层优化问题形式化

将提示嵌入 $\theta$ 视为上层超参数，LoRA 权重 $\omega$ 视为下层优化变量，构建如下双层优化问题：

$$\min_{\theta} \ell_{\mathrm{real}}(\theta, \omega^*(\theta); \mathcal{D}_{\mathrm{real}}), \quad \mathrm{s.t.} \ \omega^*(\theta) \in \arg\min_{\omega} \ell_{\mathrm{syn}}(\omega, \theta; \mathcal{D}_{\mathrm{syn}}) \tag{1}$$

- **上层**：在真实退化数据 $\mathcal{D}_{\mathrm{real}}$ 上优化提示 $\theta$，目标是最小化真实域损失 $\ell_{\mathrm{real}}$；
- **下层**：在合成配对数据 $\mathcal{D}_{\mathrm{syn}}$ 上优化 LoRA $\omega$，目标是保持结构恢复能力，$\omega^*(\theta)$ 表示给定 $\theta$ 时下层的最优 LoRA 配置。

该形式化将结构学习（下层）与退化适应（上层）解耦，使合成到真实的迁移通过超参数优化视角实现。

#### 2.3.3 惩罚式单层重构与高效训练

直接求解双层优化计算代价高昂。BiProLoRA 将其重构为带惩罚项的单层优化问题：

$$\min_{\theta,\omega} \big[ \ell_{\mathrm{real}}(\theta,\omega) + \lambda \big( \ell_{\mathrm{syn}}(\theta,\omega) - v(\theta) \big) \big] \tag{2}$$

其中 $v(\theta) = \min_{\omega} \ell_{\mathrm{syn}}(\theta, \omega)$ 为下层值函数，$\lambda$ 为惩罚系数（默认 $\lambda=0.2$，在真实适应与合成结构保持之间取得最佳平衡）。

为高效估计 $v(\theta)$，引入 **Mirror LoRA 内循环**：在合成数据上快速优化 LoRA 副本 $\tilde{\omega}$ 共 $T$ 步，获得当前提示 $\theta$ 引导下的理想结构恢复参考：

$$\tilde{\omega}_{t+1} \leftarrow \tilde{\omega}_t - \alpha \nabla_{\tilde{\omega}} \ell_{\mathrm{syn}}(\tilde{\omega}_t, \theta), \quad t = 0, \ldots, T-1 \tag{3}$$

基于 $\tilde{\omega}_T$ 近似 $v(\theta)$ 的梯度，分别推导 Primary LoRA 和提示嵌入的更新规则。

**Primary LoRA 梯度**：由真实数据弱引导和合成数据正则化共同组成，确保适应真实退化时不遗忘核心结构恢复能力：

$$g_{\omega} = \nabla_{\omega} \ell_{\mathrm{real}}(\theta, \omega) + \lambda \nabla_{\omega} \ell_{\mathrm{syn}}(\theta, \omega) \tag{4}$$

**提示嵌入梯度**：主要由真实场景目标驱动，惩罚项 $\nabla_{\theta} \ell_{\mathrm{syn}}(\theta, \tilde{\omega}_T)$ 防止提示选择严重损害 LoRA 合成最优结构的配置：

$$g_{\theta} = \nabla_{\theta} \ell_{\mathrm{real}}(\theta, \omega) + \lambda \big( \nabla_{\theta} \ell_{\mathrm{syn}}(\theta, \omega) - \nabla_{\theta} \ell_{\mathrm{syn}}(\theta, \tilde{\omega}_T) \big) \tag{5}$$

消融实验（Table 4）证实：仅用提示嵌入（无 LoRA）时 NIQE 恶化至 6.321，而完整 BiProLoRA 达到 2.971，验证了 LoRA 结构恢复与提示退化调节的互补必要性；双层联合建模（HO）策略在 NIQE、LIQE、DE 三项指标上均优于朴素联合训练（Naive）。

---

### 2.4 损失函数设计

#### 2.4.1 合成域损失

下层结构恢复训练在合成配对数据上进行，采用 L2 损失与感知 LPIPS 损失的组合：

$$\ell_{\mathrm{syn}} = \ell_2 + \ell_{\mathrm{lpips}} \tag{6}$$

#### 2.4.2 真实域 CLIP 对比损失

真实域缺乏参考真值，因此采用无参考的 CLIP 对比损失。利用预训练 CLIP 模型编码恢复结果与正/负提示文本，通过最大化文本-图像余弦相似度实现语义对齐：

$$\ell_{\mathrm{real}} = \frac{e^{\cos(\mathcal{G}_{\mathrm{image}}(\mathbf{z}_{\mathcal{D}}), \mathcal{G}_{\mathrm{text}}(\mathbf{t}_{\mathcal{D}}))}}{\sum_{i \in \{\mathcal{D}, \mathcal{C}\}} e^{\cos(\mathcal{G}_{\mathrm{image}}(\mathbf{z}_{\mathcal{D}}), \mathcal{G}_{\mathrm{text}}(\mathbf{t}_i))}} \tag{7}$$

其中 $\mathbf{z}_{\mathcal{D}}$ 为恢复结果的 CLIP 图像嵌入，$\mathbf{t}_{\mathcal{D}}$ 和 $\mathbf{t}_{\mathcal{C}}$ 分别为正提示（如"a clean, high-quality image"）和负提示（如"a degraded, low-quality image"）的文本嵌入。该损失在无参考条件下为真实域提供有效训练信号。

---

### 2.5 整体算法流程

完整算法流程如 Algorithm 1 所示：

1. **DFL 预训练**（行 2–6）：在 $\mathcal{D}_{\mathrm{real}}$ 上训练适配器 $A_\pi$，冻结后进入去噪阶段；
2. **BiProLoRA 双层优化**（行 7–20）：每轮迭代中，先执行 Mirror LoRA 内循环（式 3）获得 $\tilde{\omega}_T$，再分别按式 (4) 和式 (5) 更新 Primary LoRA $\omega$ 和提示嵌入 $\theta$。

## 实验与关键发现

### 一、主实验结果

BiProLoRA 在三个真实退化场景（低光、雾霾、水下）以及夜间目标检测下游任务上进行了全面评估。所有定量对比均采用五种无参考指标（NIQE↓、LIQE↑、DE↓、MUSIQ↑、ARNIQ↑），因为真实场景缺乏参考真值，这保证了与所有基线方法的公平对比。训练仅使用 50 张真实图像（约为合成数据的 10%），在这种极度不平衡的数据设置下评估方法的有效性和泛化能力。

**真实低光场景。** 在 DARKFACE（已知真实低光）和 ExDark（未知真实低光）两个基准上，BiProLoRA 在五项无参考指标上系统性地超越现有方法。如 Table 1 所示，在 DARKFACE 上，BiProLoRA 取得 NIQE 2.971（较 **Zero-IG** (Shi et al., CVPR 2024) 的 3.030 降低 0.059）和 LIQE 2.585（较 SCI++ 的 2.135 提升 0.450）的最优结果。在 ExDark 上，NIQE 达到 3.806（较 Zero-IG 的 3.920 降低 0.114），展现出对未知退化分布的强泛化能力。Figure 3 的视觉对比进一步验证：BiProLoRA 的恢复结果在亮度适宜性、纹理清晰度和色彩还原度上均优于对比方法。

**真实雾霾与水下场景。** 如 Table 2 所示，在 RTTS（真实雾霾）上 BiProLoRA 取得 NIQE 3.972（较 **PHAT** 的 4.059 降低 0.087）；在 URPC（真实水下）上取得 NIQE 3.514（较 **WF-Diff** 的 3.735 降低 0.221）。跨场景的稳定优势表明，双层提示 LoRA 框架的退化适应机制对不同物理退化类型具有通用性。Figure 4 的视觉结果佐证了定量发现。

**夜间目标检测。** 在 ExDark 数据集上评估恢复结果对下游检测任务的增益（Table 3）。BiProLoRA 恢复图像上的检测 mAP 达到 40.9，较 Baseline（直接使用原始暗光图像）的 37.5 提升 3.4 个百分点，验证了恢复质量对高层视觉任务的有效支撑。

### 二、消融分析

Table 4 系统拆解了 BiProLoRA 各组件的贡献，所有实验在 DARKFACE 上进行。

![[assets/figures/papers/paper_list_l2376_https_openaccess_thecvf_com_content_CVPR2026_html_An_BiProLoRA_Bilevel_P/figures/010_Table_4.jpg]]
*Table 4: Quantitative results of algorithmic analyses*

**DFL 的必要性。** 移除 DFL（即仅使用标准 VAE 自编码路径，配置 S_i）导致 NIQE 从 2.971 恶化至 4.074，视觉质量也明显下降（Figure 6）。这证实了在去噪前通过自监督分布保真度学习校准真实退化分布，对纹理保真度具有决定性作用。DFL 适配器的预训练（Pretrain）方式优于微调（Finetune）方式，无需在 BiProLoRA 阶段同时训练适配器即可获得最佳效果。

**LoRA 与提示嵌入的互补性。** 仅使用提示嵌入而无 LoRA（配置 S_f，DFL+Prompt only）时，NIQE 急剧恶化至 6.321，远差于完整模型。这验证了核心洞察：LoRA 提供可复用的结构恢复能力，提示嵌入作为轻量退化感知调制器在不改变核心权重的前提下引导该能力的发挥，二者缺一不可。

**双层联合建模（HO）的优势。** 将双层优化替换为朴素联合训练（配置 S_g，Naive joint training）后，NIQE、LIQE、DE 三项指标均出现显著退化。双层联合建模通过将结构学习与退化适应分离——下层在合成数据上优化 LoRA 以保留结构先验，上层在真实数据上优化提示以调控适应行为——实现了合成到真实的有效迁移，而朴素联合训练无法解耦这两种相互制约的学习目标。

**惩罚系数 λ。** 参数分析（Figure 8）表明 λ=0.2 在真实适应与合成结构保持之间取得了最佳平衡。过大的 λ 会过度约束提示的退化适应能力，过小的 λ 则可能导致合成学到的结构完整性被破坏。

### 三、失败模式与局限性

**复合退化处理能力不足。** 当前方法主要针对单一退化场景（低光、雾霾或水下）进行适配。如 Figure 9 所示，在 LOL-Blur 数据集上，当低光场景同时伴随设备引入的运动模糊时，BiProLoRA 的恢复能力明显受限。这是因为 DFL 阶段仅针对单一退化分布进行校准，而双层优化框架的提示嵌入也仅学习单一退化类型的调控策略。

**跨任务统一恢复尚未探索。** 不同退化场景的训练目前是独立进行的，尚未验证跨任务的混合数据训练能否产生可迁移的元表示，以实现单一模型的多场景恢复。这是一个值得进一步研究的方向。

**提示初始化的语义先验缺失。** DFL 阶段使用的提示为随机初始化，未充分利用预训练语言模型中的语义先验，可能在极端退化条件下限制了调控精度。引入视觉提示或多模态提示来增强退化感知能力，是潜在的改进路径。

![[assets/figures/papers/paper_list_l2376_https_openaccess_thecvf_com_content_CVPR2026_html_An_BiProLoRA_Bilevel_P/figures/003_Table_1.jpg]]
*Table 1: Quantitative comparisons on three real low-light datasets*

![[assets/figures/papers/paper_list_l2376_https_openaccess_thecvf_com_content_CVPR2026_html_An_BiProLoRA_Bilevel_P/figures/005_Table_2.jpg]]
*Table 2: Quantitative comparisons for real hazy and underwater scene recovery*

![[assets/figures/papers/paper_list_l2376_https_openaccess_thecvf_com_content_CVPR2026_html_An_BiProLoRA_Bilevel_P/figures/008_Table_3.jpg]]
*Table 3: Quantitative results on nighttime object detection*

![[assets/figures/papers/paper_list_l2376_https_openaccess_thecvf_com_content_CVPR2026_html_An_BiProLoRA_Bilevel_P/figures/007_Figure_5.jpg]]
*Figure 5: Qualitative comparisons corresponding to Table 3*

![[assets/figures/papers/paper_list_l2376_https_openaccess_thecvf_com_content_CVPR2026_html_An_BiProLoRA_Bilevel_P/figures/004_Figure_3.jpg]]
*Figure 3: Qualitative comparisons on real low-light scene corresponding to*

## 定位与知识库关联

### 1. 与基线方法的关系

BiProLoRA 建立在预训练扩散模型与参数高效微调两条技术路线的交叉点上，其核心创新在于通过双层优化框架将结构恢复能力与退化感知调制解耦，从而克服了现有方法在合成到真实迁移中的根本性瓶颈。

**与预训练扩散模型的关系。** BiProLoRA 以 **SD-Turbo**（Sauer et al., ECCV 2024）作为基础生成先验。SD-Turbo 提供的快速扩散采样能力赋予了方法实用的推理效率，但其自编码路径在合成数据上预训练，未针对真实退化分布进行校准——这正是 BiProLoRA 引入 DFL 模块的根本动机。与 **ReDDiT**（Lan et al., CVPR 2025）等同样基于扩散模型的低光增强方法不同，BiProLoRA 不直接在像素空间进行条件控制，而是将适配操作分解为潜在空间分布校准（DFL）与去噪器权重调制（LoRA+Prompt）两个阶段，从而在保留预训练先验的同时获得更强的真实场景泛化能力。

**与参数高效微调方法的关系。** **LoRA**（Hu et al., ICLR 2022）提供了低秩权重更新的基础机制，使 BiProLoRA 能够以极低的参数量（仅对 UNet 选定层施加低秩更新）学习结构恢复映射。然而，BiProLoRA 的关键洞察在于：LoRA 虽然能有效捕获合成数据上的结构恢复能力，但其权重空间与退化适应耦合，导致在未见真实退化上的泛化受限。为此，BiProLoRA 引入了可学习提示嵌入作为轻量退化感知调制器，在不改变核心权重的前提下调控 LoRA 能力的发挥——这一设计在理念上与提示调优（prompt tuning）一脉相承，但将其首次应用于双层优化的上下文中，实现了 LoRA 与 Prompt 的相互促进。

**与真实场景恢复方法的对比定位。** 在真实低光增强任务上，BiProLoRA 与 **Zero-IG**（Shi et al., CVPR 2024）形成直接对比：Zero-IG 依赖零样本扩散引导，而 BiProLoRA 通过少量真实数据（仅 50 张图像，约合成数据的 10%）进行适配，在 DARKFACE 上取得了更优的 NIQE（2.971 vs 3.030）。与 **QuadPrior**（Wang et al., CVPR 2024）利用 VAE 分支进行真实自适应的方法相比，BiProLoRA 的 DFL 模块同样在自编码路径上操作，但采用了更轻量的双层零卷积适配器设计，且直接在真实退化数据上以自监督方式训练，避免了额外的合成数据依赖。

### 2. 适用边界

BiProLoRA 的适用边界由其设计假设和方法结构共同决定：

**退化类型的边界。** 方法当前主要针对单一退化场景进行适配，包括低光增强（DARKFACE、ExDark、NOD 数据集）、雾霾去除（RTTS 数据集）和水下恢复（URPC 数据集）。在这三类场景上，BiProLoRA 均取得了最优或次优的无参考指标结果。然而，当退化类型超出训练分布时，方法的有效性受到限制——Figure 9 展示的 LOL-Blur 数据集案例表明，对于设备引入的运动模糊与低光构成的复合退化，BiProLoRA 的恢复能力不足。这一局限源于 DFL 模块和提示嵌入均为单一退化场景独立训练，尚未建立跨退化类型的统一表示。

**数据效率的边界。** BiProLoRA 在极度不平衡的数据设置下展示了有效性——仅使用 50 张真实图像（约合成数据的 10%）即可实现显著的性能提升。这一数据效率得益于双层优化框架的解耦设计：下层在充足的合成数据上学习可复用的结构恢复能力，上层仅在少量真实数据上优化轻量提示嵌入。然而，当真实数据量进一步减少或真实退化与合成退化之间的分布偏移过大时，DFL 的分布校准能力和提示嵌入的调制精度可能不足。

**任务类型边界。** 除图像恢复外，BiProLoRA 在下游任务上也展示了迁移能力——在 ExDark 夜间目标检测任务上，以 BiProLoRA 恢复结果作为输入的检测器取得了 40.9 mAP，较基线提升 3.4 个百分点。这表明方法恢复的图像质量对高层视觉任务具有正向迁移作用，但该方法本身不涉及检测器的联合优化，其迁移效果受限于恢复质量与检测器之间的适配程度。

### 3. 局限与开放问题

**已知局限。** 论文明确指出了三个层面的局限：（1）**复合退化处理能力不足**——当前方法针对单一退化场景独立训练，对低光+运动模糊等多因素耦合退化（如 LOL-Blur 数据集）的恢复效果有限（Figure 9）；（2）**跨任务训练尚未探索**——不同退化场景的适配是独立进行的，未验证混合数据训练能否产生可迁移的元表示以实现统一恢复；（3）**提示初始化未充分利用语义先验**——DFL 阶段使用的提示为随机初始化，未利用预训练语言模型中的语义知识，可能限制了在极端退化下的调控精度。

**开放问题。** 从方法结构出发，以下问题值得进一步探索：（1）BiProLoRA 的双层优化框架是否可扩展到复合退化场景——例如，通过多组提示嵌入分别对应不同退化因素，并在惩罚项中引入退化间的交互约束；（2）跨多个退化任务的混合数据训练能否产生可迁移的元表示，使单一模型具备多场景恢复能力——这需要重新设计 DFL 的分布校准策略和提示嵌入的共享机制；（3）提示嵌入的初始化和结构设计是否可以进一步优化——例如，引入视觉提示或多模态提示来增强退化感知能力，或利用预训练语言模型的语义先验进行初始化；（4）双层优化的内循环步数 T 和惩罚系数 λ 在不同退化类型间的最优配置是否存在统一规律——当前 λ=0.2 的选择基于低光场景的消融实验，其在雾霾和水下场景上的最优性需要进一步验证。

### 4. 在知识库中的定位

BiProLoRA 在真实场景恢复的知识谱系中占据了一个独特的位置：它既不是纯粹的零样本方法（如 Zero-IG），也不是完全依赖合成配对数据的有监督方法，而是通过**双层超参数优化**实现了合成监督与真实自监督的协同。其核心贡献在于揭示了 LoRA 与提示嵌入之间的**互补性机制**——LoRA 提供可复用的结构恢复能力，提示嵌入作为轻量退化感知调制器在不改变核心权重的前提下引导该能力的发挥——并通过双层优化的数学框架将这一互补性形式化。

从更宏观的视角看，BiProLoRA 代表了一类新兴的方法范式：**将预训练生成模型的适配问题建模为超参数优化问题**。在这一范式下，预训练权重（通过 LoRA 调制）扮演了“基础模型”的角色，而提示嵌入则扮演了“任务特定超参数”的角色，双层优化自然地分离了通用能力保持与任务特定适应两个目标。这一范式具有较强的可扩展性——理论上，下层的 LoRA 可以替换为其他参数高效微调方案，上层的提示嵌入也可以扩展为更复杂的条件调制机制，这使得 BiProLoRA 的框架思想有望迁移到更广泛的生成模型适配任务中。

## 原文 PDF

![[paperPDFs/CVPR_2026/BiProLoRA_Bilevel_Prompt_LoRA_for_Real_Scene_Recovery.pdf]]
