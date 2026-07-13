---
title: "SATO: Stable Text-to-Motion Framework"
type: paper
paper_level: A
venue: ACM MM
year: 2024
pdf_ref: paperPDFs/ACM_MM_2024/SATO_Stable_Text_to_Motion_Framework.pdf
project_link: null
code_link: "https://github.com/sato-team/Stable-Text-to-Motion-Framework"
aliases:
- SSTMF
- SATO
tags:
- ACM_MM_2024
- topic/motion_animation
- topic/motion_animation/human_motion_generation
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/benchmarks_datasets_evaluation
core_operator: 通过强制约束扰动前后注意力向量的top‑k重叠（稳定注意力），并结合PGD/RSR扰动与冻结教师模型，稳定预测分布，从而在保持准确性的同时提升鲁棒性。
primary_logic: 将稳定性形式化为三个数学约束：注意力top‑k鲁棒性、预测分布鲁棒性及与原模型预测的接近性，并提出可微分的替代损失L_Topk以端到端优化。
claims:
- SATO由三个模块组成：扰动模块、稳定注意力模块和预训练教师模块，分别负责稳定注意力、稳定预测和平衡准确性与鲁棒性。
- 在HumanML3D基准上，SATO（基于T2M‑GPT）的扰动文本FID_P从1.754降至0.155，且原始文本FID仅从0.141微升至0.157。
- SATO显著降低了CLIP编码器在扰动前后的注意力Jensen‑Shannon散度，表明稳定注意力模块有效。
- 消融实验显示，同时使用稳定注意力损失（L2）和扰动损失（L3）可获得最优稳定性（FID_P 0.155, FID_D 0.010）。
---

# SATO: Stable Text-to-Motion Framework

> [!tip] 核心洞察
> 将稳定性形式化为三个数学约束：注意力top‑k鲁棒性、预测分布鲁棒性及与原模型预测的接近性，并提出可微分的替代损失L_Topk以端到端优化。

| 字段 | 内容 |
|------|------|
| 中文题名 | SATO：稳定的文本到运动生成框架 |
| 英文题名 | SATO: Stable Text-to-Motion Framework |
| 会议/期刊 | ACM MM 2024 |
| Links | [paper](https://arxiv.org/abs/2405.01461) · [Code](https://github.com/sato-team/Stable-Text-to-Motion-Framework) |
| Topic | #topic/motion_animation #topic/motion_animation/human_motion_generation #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/benchmarks_datasets_evaluation |
| Method | SATO (Stable Text-to-Motion Framework) |
| Dataset | HumanML3D, KIT-ML, Human evaluation |

> [!tip] 效果简介
> - HumanML3D (original text) 上，FID↓ 0.157 vs 0.141 (+0.016)。
> - HumanML3D (perturbed text) 上，FID_P↓ 0.155 vs 1.754 (-1.599)。
> - HumanML3D (prediction discrepancy) 上，FID_D↓ 0.021 vs 1.443 (-1.422)。

## 概要

文本到运动生成（Text-to-Motion）模型近年来取得了显著进展，但在实际部署中暴露出一个关键瓶颈：**对输入文本的微小扰动极度敏感**。用户使用同义词替换（如将“walk”替换为“stroll”）或微调措辞时，现有模型往往生成完全不同的、甚至错误的运动序列。SATO论文通过系统分析揭示了这一现象的根源——预训练的CLIP文本编码器在扰动前后注意力模式不稳定，导致对关键运动描述词的关注发生偏移，进而引发运动生成误差的级联放大（见Figure 2的token修改示例）。

针对上述问题，SATO提出了一个**稳定的文本到运动框架**，其核心洞察是将稳定性形式化为三个数学约束：(1) 注意力top-k鲁棒性——扰动前后模型对关键token的注意力索引应保持一致；(2) 预测分布稳定性——扰动不应导致生成运动分布的剧烈变化；(3) 与原模型预测的接近性——在提升鲁棒性的同时，不能显著偏离原始模型的准确预测。基于这三个约束，SATO构建了包含**扰动模块、稳定注意力模块和预训练教师模块**的三组件架构（Figure 3），通过可微的替代损失函数 $\mathcal{L}_{\mathrm{Topk}}$ 实现端到端优化。

在**HumanML3D**基准上的实验结果表明，SATO在保持原始性能基本不变的前提下，大幅提升了模型稳定性：基于T2M-GPT的SATO将扰动文本的FID_P从1.754降至0.155（降幅达91.2%），而原始文本FID仅从0.141微升至0.157。在**KIT-ML**数据集和人类评估中，SATO同样表现出跨模型（MoMask）和跨数据集的泛化能力。消融实验进一步证实，稳定注意力损失与扰动损失协同作用是实现最优稳定性的关键。

SATO的方法定位属于**模型微调型鲁棒性增强框架**，区别于单纯的数据增强或对抗训练方法。其核心创新在于首次将注意力层面的稳定性约束引入文本到运动生成任务，并设计了一套可微分、可优化的损失体系来实现这一目标。该方法可适配于不同类型的基线模型（如基于VQ-VAE的T2M-GPT和基于掩码建模的MoMask），展现了良好的通用性。

文本到运动生成（Text-to-Motion）旨在从自然语言描述中合成三维人体动作序列，在动画制作、虚拟现实和人机交互等领域具有广泛应用。近年来，基于 VQ-VAE、扩散模型和生成式掩码建模的方法显著提升了生成质量，代表性工作包括 **T2M‑GPT**（Zhang et al., arXiv 2023）、**MoMask**（Guo et al., arXiv 2023）和 **MotionDiffuse**（Zhang et al., arXiv 2022）。

然而，现有模型存在一个被忽视的关键瓶颈：**对文本输入的微小扰动极度敏感**。当用户输入中出现同义词替换、语序调整等细微变化时，模型常常产生灾难性的错误预测。SATO 论文通过 token 修改实验揭示了这一现象的根源——预训练的 CLIP 文本编码器在处理扰动文本时，其注意力分布会发生显著偏移，导致模型不再关注关键的运动描述词，进而引发生成误差的级联放大。在 HumanML3D 基准上，基线模型 T2M‑GPT 在原始文本上 FID 低至 0.141，但在扰动文本上 FID_P 急剧恶化至 1.754，充分说明了稳定性问题的严重性。

现有工作的一个共同缺陷在于：它们普遍冻结 CLIP 文本编码器，未对文本表示的鲁棒性进行任何约束或优化。这导致模型在训练过程中从未见过扰动输入，也缺乏应对文本变化的机制。SATO 的核心洞察在于，一个稳定的文本到运动模型应当满足三个数学约束：**注意力机制的 top‑k 鲁棒性**、**预测分布的稳定性**，以及**与原模型预测的接近性**。基于此，SATO 提出了一个包含扰动模块、稳定注意力模块和预训练教师模块的三组件框架，通过解冻 CLIP 并引入可微替代损失 $\mathcal{L}_{\mathrm{Topk}}$ 进行端到端优化，在保持生成准确性的同时大幅提升对文本扰动的鲁棒性。

## 核心方法与创新机理

SATO的核心创新在于首次将文本到运动模型的稳定性形式化为三个可优化的数学约束，并通过“解冻CLIP + 注意力top‑k对齐 + 扰动一致性训练”的组合策略实现端到端优化。相较于现有方法普遍冻结CLIP文本编码器且缺乏对输入扰动的显式建模，SATO在以下四个关键维度上引入了结构性改变：

**1. CLIP文本编码器从冻结到可训练的转变**

现有文本到运动方法（如 **T2M‑GPT** (Zhang et al., 2023)、**MoMask** (Guo et al., 2023)）通常冻结预训练的CLIP文本编码器，仅将其作为固定的特征提取器。SATO首次解冻CLIP模块并引入稳定性损失进行微调，使其能够学习对同义词替换等微小文本扰动保持注意力模式稳定的表示。这一改变是后续所有稳定性约束得以实施的前提——冻结的编码器无法响应稳定性信号的梯度更新。

**2. 注意力top‑k稳定性约束（L_Topk损失）**

SATO提出了一种可微分的替代损失 $\mathcal{L}_{\mathrm{Topk}}$，直接约束扰动前后注意力向量的top‑k索引及其数值稳定性：

$$\mathcal{L}_{\mathrm{Topk}} = \frac{1}{2k} \big( \| \omega_{\zeta_{k}^{\omega}} - \tilde{\omega}_{\zeta_{k}^{\omega}} \| + \| \tilde{\omega}_{\zeta_{k}^{\tilde{\omega}}} - \omega_{\zeta_{k}^{\tilde{\omega}}} \| \big)$$

该损失的核心思想是：文本到运动模型的生成误差往往源于CLIP编码器在扰动后对关键运动描述词（如“walk”、“jump”）的注意力权重发生偏移，进而引发运动序列生成的级联错误。通过强制扰动前后top‑k注意力索引重叠，SATO迫使模型始终聚焦于相同的语义关键token，从注意力层面阻断误差传播链。这是现有基线方法完全缺失的机制。

**3. 扰动模块：从无扰动处理到显式对抗训练**

基线方法在训练和推理阶段均假设输入文本是干净的，对用户实际使用中的同义词替换、拼写变体等扰动毫无准备。SATO引入扰动模块，通过随机同义词替换（RSR）或投影梯度下降（PGD）在嵌入空间生成扰动文本，并在训练时显式约束扰动后的预测分布与原始预测保持一致（通过一致性损失 $\mathcal{L}_3$）。这一设计使模型在训练阶段即暴露于扰动分布，从而获得对推理阶段输入变化的鲁棒性。

**4. 冻结教师模块：准确性与鲁棒性的平衡机制**

SATO引入一个冻结的预训练T2M‑GPT作为教师模型，通过预测接近性损失 $\mathcal{L}_1$ 约束微调后的模型在未扰动文本上的预测分布不偏离原始模型太远。这一机制直接回应了稳定性训练中常见的“准确性‑鲁棒性权衡”问题：消融实验（Table 5）表明，仅使用扰动损失（$\mathcal{L}_3$）虽能提升鲁棒性，但会导致原始文本上的生成质量下降；加入教师模块的 $\mathcal{L}_1$ 后，原始文本FID仅从0.141微升至0.157，而扰动文本FID_P从1.754骤降至0.155，实现了准确性与鲁棒性的最优平衡。

**创新点的内在逻辑链条**

上述四个changed slot并非孤立存在，而是形成了一条因果闭环：解冻CLIP（slot 1）使注意力可优化 → $\mathcal{L}_{\mathrm{Topk}}$（slot 2）从注意力层面稳定特征提取 → 扰动模块（slot 3）从预测层面增强鲁棒性 → 教师模块（slot 4）防止稳定性训练损害原始性能。消融实验（Table 5）证实，同时启用 $\mathcal{L}_2$（稳定注意力）和 $\mathcal{L}_3$（扰动一致性）时达到最优稳定性（FID_P 0.155, FID_D 0.010），单独使用任一损失均无法达到同等效果，验证了该闭环设计的必要性。

SATO (Stable Text-to-Motion Framework) 是一个即插即用的文本到运动稳定性框架，可适配当前所有采用文本编码器与Transformer层的生成方法。其核心架构由三个模块串联构成：**扰动模块 (Perturbation Module)**、**稳定注意力模块 (Stable Attention Module)** 和**预训练教师模块 (Pretrained Teacher Module)**，如 Figure 3 所示。

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2405_01461/figures/003_Figure_3.jpg]]
*Figure 3: (a) Framework of our proposed Stable Text-to-Motion (SATO). It comprises three components: perturbation module, stable attention module, and pretrained teacher model. (b) The perturbation module encompasses two approaches for perturbation, namely Random Synonym Replacement (RSR) and Projected Gradient Descent (PGD). This module is utilized to emulate various perturbations encountered during user interactions. (c) The stable attention module aligns the top-k attention index weights before and after perturbation to stabilize the model’s attention distribution. Additionally, we incorporate a frozen teacher module, solely utilized during training, to stabilize the model’s motion generation capa...*

### 模块关系与数据流

给定原始文本输入 $x$，SATO 的推理流程如下：

1. **扰动模块**在训练阶段模拟用户输入中可能出现的文本扰动，生成扰动后的文本表示。该模块提供两种扰动策略：**随机同义词替换 (Random Synonym Replacement, RSR)** 和**投影梯度下降 (Projected Gradient Descent, PGD)**。RSR 通过人工构建的同义词词典随机替换文本中的词汇；PGD 则在嵌入空间中寻找最大扰动方向，以生成更具对抗性的扰动嵌入。扰动后的文本与原始文本一同送入后续模块。

2. **稳定注意力模块**接收原始文本与扰动文本，分别通过**解冻的 CLIP 文本编码器**提取注意力权重向量。该模块的核心操作是对齐扰动前后注意力向量的 top‑k 索引，迫使模型在文本发生微小变化时仍聚焦于关键的运动描述词。这一约束通过可微代理损失 $\mathcal{L}_{\mathrm{Topk}}$ 实现端到端优化。

3. **预训练教师模块**仅在训练阶段激活。它使用冻结的预训练模型（如 T2M‑GPT）作为教师，对原始文本生成参考运动预测。学生模型（即 SATO 微调后的模型）需在原始文本和扰动文本上的预测分别与教师预测保持接近，从而在提升鲁棒性的同时避免原始性能显著退化。

### 优化目标

SATO 将稳定性形式化为三个数学约束，并统一为一个最小‑最大优化问题：

- **预测鲁棒性 (Prediction Robustness)**：扰动后的预测分布与原始预测分布之间的距离应被约束在阈值 $\gamma_1$ 以内，对应损失 $\mathcal{L}_3$。
- **预测接近性 (Closeness of Prediction)**：SATO 在未扰动文本上的预测分布应与冻结教师模型的预测分布保持接近（阈值 $\gamma_2$），对应损失 $\mathcal{L}_1$。
- **Top‑k 注意力鲁棒性 (Top‑k Attention Robustness)**：扰动前后注意力向量的 top‑k 重叠比例应不低于 $\beta$，对应损失 $\mathcal{L}_2$（即 $\mathcal{L}_{\mathrm{Topk}}$）。

最终微调损失为原始 Transformer 损失与三个稳定性辅助损失的加权和：

$$\mathcal{L} = \mathcal{L}_{\mathrm{trans}} + \lambda_{1} \cdot \mathcal{L}_{1} + \lambda_{2} \cdot \mathcal{L}_{2} + \lambda_{3} \cdot \mathcal{L}_{3}$$

其中 $\mathcal{L}_1$ 约束预测接近性，$\mathcal{L}_2$ 约束注意力稳定性，$\mathcal{L}_3$ 约束扰动鲁棒性。消融实验 (Table 5) 证实，同时使用 $\mathcal{L}_2$ 和 $\mathcal{L}_3$ 可获得最优稳定性——扰动文本的 FID_P 降至 0.155，预测差异 FID_D 降至 0.010。

### 关键设计决策

与现有工作中普遍冻结 CLIP 文本编码器的做法不同，SATO **解冻 CLIP 模块**进行微调，使其能够学习更稳定的注意力模式。这一改变是稳定注意力约束得以生效的前提，但论文未对解冻可能引发的灾难性遗忘风险进行深入分析。此外，SATO 框架在 T2M‑GPT 和 MoMask 两种不同架构的基线上均得到验证，初步展示了其即插即用的通用性。

### 问题形式化与稳定性三约束

SATO将文本到运动模型的稳定性形式化为三个数学约束，分别对应注意力、预测分布和预测接近性三个维度的鲁棒性要求。

**约束1：预测鲁棒性（Prediction Robustness）**。对于原始文本嵌入 $x$ 及其扰动版本 $x'$，模型预测 $\tilde{y}(x, \tilde{\omega})$ 和 $\tilde{y}(x', \tilde{\omega}')$ 之间的距离应被限制在一个阈值 $\gamma_1$ 以内：

$$D_1(\tilde{y}(x, \tilde{\omega}), \tilde{y}(x', \tilde{\omega}')) \leq \gamma_1$$

**约束2：预测接近性（Closeness of Prediction）**。扰动后模型的预测 $\tilde{y}(x, \tilde{\omega})$ 应与原始冻结教师模型 $y(x, \omega)$ 的预测保持接近，以平衡准确性与鲁棒性：

$$D_2(\tilde{y}(x, \tilde{\omega}), y(x, \omega)) \leq \gamma_2$$

**约束3：Top‑k注意力鲁棒性（Top‑k Attention Robustness）**。扰动前后注意力向量的top‑k索引重叠比例 $V_k$ 应不低于阈值 $\beta$。首先定义top‑k分量集合：

$$T_k(\mathbf{x}) = \{ i : i \in [d] \text{ 且 } |\{ \mathbf{x}_j \geq \mathbf{x}_i : j \in [n] \}| \leq k \}$$

基于此定义top‑k重叠比例：

$$V_k(\mathbf{x}, \mathbf{x}') = \frac{1}{k} \cdot | T_k(\mathbf{x}) \cap T_k(\mathbf{x}') |$$

约束条件为 $V_k(\tilde{\omega}, \tilde{\omega}') \geq \beta$，其中 $\tilde{\omega}$ 和 $\tilde{\omega}'$ 分别为扰动前后的注意力权重向量。

---

### SATO优化目标

将上述三个约束整合为最小‑最大优化问题。记扰动 $\rho$ 作用于注意力向量，$D_1$ 和 $D_2$ 为预测分布之间的距离度量，则总体优化目标为：

$$\min_{\tilde{\mathcal{W}}} \mathbb{E}_x \Big[ \lambda_1 (D_2(\tilde{y}(x, \tilde{\omega}), y(x, \omega)) - \gamma_2) + \max_{\mathbb{H}^2} \lambda_2 (\beta - V_k(\tilde{\omega}, \tilde{\omega} + \rho)) + \lambda_3 (\max_{\|\rho\| \leq R} D_1(\tilde{y}(x, \tilde{\omega}), \tilde{y}(x, \tilde{\omega} + \rho)) - \gamma_1) \Big]$$

其中：
- $\tilde{\mathcal{W}}$ 为可训练的模型参数（包括解冻的CLIP编码器）；
- $\lambda_1, \lambda_2, \lambda_3$ 为各约束的权重系数；
- 内层最大化 $\max_{\|\rho\| \leq R}$ 通过投影梯度下降（PGD）寻找最坏情况扰动。

---

### 稳定注意力替代损失 $L_{\text{Topk}}$

由于 $V_k$ 涉及不可微的top‑k索引操作，SATO提出可微分的替代损失 $\mathcal{L}_{\text{Topk}}$。记 $\zeta_k^{\omega}$ 为原始注意力向量 $\omega$ 的top‑k索引集合，$\tilde{\omega}$ 为扰动后注意力向量，则损失定义为：

$$\mathcal{L}_{\text{Topk}} = \frac{1}{2k} \big( \| \omega_{\zeta_k^{\omega}} - \tilde{\omega}_{\zeta_k^{\omega}} \| + \| \tilde{\omega}_{\zeta_k^{\tilde{\omega}}} - \omega_{\zeta_k^{\tilde{\omega}}} \| \big)$$

**变量含义**：
- $\omega_{\zeta_k^{\omega}}$：原始注意力向量在自身top‑k索引上的取值；
- $\tilde{\omega}_{\zeta_k^{\omega}}$：扰动后注意力向量在原始top‑k索引上的取值；
- $\tilde{\omega}_{\zeta_k^{\tilde{\omega}}}$：扰动后注意力向量在自身top‑k索引上的取值；
- $\omega_{\zeta_k^{\tilde{\omega}}}$：原始注意力向量在扰动后top‑k索引上的取值。

该损失通过双向约束，确保扰动前后注意力向量的top‑k索引及其数值均保持稳定，从而强制CLIP编码器始终聚焦于关键运动描述词。

---

### 最终训练损失

SATO的总训练损失由原始Transformer生成损失与三个稳定性辅助损失加权求和构成：

$$\mathcal{L} = \mathcal{L}_{\text{trans}} + \lambda_1 \cdot \mathcal{L}_1 + \lambda_2 \cdot \mathcal{L}_2 + \lambda_3 \cdot \mathcal{L}_3$$

其中：
- $\mathcal{L}_{\text{trans}}$：基础文本到运动模型的原始损失（如T2M‑GPT的交叉熵损失）；
- $\mathcal{L}_1 = D_2(\tilde{y}(x, \tilde{\omega}), y(x, \omega))$：预测接近性损失，约束微调模型输出不偏离冻结教师模型；
- $\mathcal{L}_2 = \mathcal{L}_{\text{Topk}}(\tilde{\omega}, \tilde{\omega}')$：稳定注意力损失，对齐扰动前后的top‑k注意力分布；
- $\mathcal{L}_3 = D_1(\tilde{y}(x, \tilde{\omega}), \tilde{y}(x, \tilde{\omega}'))$：扰动一致性损失，约束扰动前后预测分布一致。

---

### 三个核心模块

**扰动模块（Perturbation Module）** 提供两种扰动生成方式：
- **随机同义词替换（RSR）**：基于人工构建的同义词词典，随机替换文本中的词汇；
- **投影梯度下降（PGD）**：在嵌入空间中沿梯度方向寻找最大扰动，约束 $\|\rho\| \leq R$。

**稳定注意力模块（Stable Attention Module）** 解冻CLIP文本编码器，通过 $\mathcal{L}_2$ 损失直接优化注意力向量的top‑k稳定性。这一设计改变了现有工作中冻结CLIP的常规做法（如 **T2M‑GPT** Zhang et al., arXiv 2023 和 **MoMask** Guo et al., arXiv 2023），使编码器能够主动适应稳定性需求。

**预训练教师模块（Pretrained Teacher Module）** 引入冻结的原始T2M‑GPT作为教师，仅通过 $\mathcal{L}_1$ 损失在训练时约束学生模型，不参与推理。该模块是平衡准确性与鲁棒性的关键——消融实验（Table 5）显示，同时使用 $\mathcal{L}_2$ 和 $\mathcal{L}_3$ 可将扰动文本FID_P降至0.155，预测差异FID_D降至0.010，达到最优稳定性。

## 实验与关键发现

### 主实验：扰动鲁棒性的定量评估

SATO的核心价值在于显著提升模型对文本扰动的鲁棒性，同时几乎不牺牲原始文本上的生成质量。在HumanML3D基准上，基于T2M-GPT构建的SATO将扰动文本的FID_P从1.754降至0.155，降幅达1.599（Table 1）。更关键的是，原始文本的FID仅从0.141微升至0.157，增幅仅0.016，表明鲁棒性提升并未以显著损害准确性为代价。预测差异度FID_D同样从1.443骤降至0.021，说明扰动前后模型输出高度一致。

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2405_01461/figures/006_Table_1.jpg]]
*Table 1: Quantitative evaluation on the HumanML3D. ± indicates a 95% confidence interval. SATO(T2M-GPT) refers to finetuning based on T2M-GPT to create SATO, and similarly, SATO(MoMask) refers to fine-tuning based on MoMask to create SATO. Red indicates the best result, while blue refers to the second best*

基于MoMask构建的SATO同样展现出鲁棒性增益：FID_P从0.206降至0.174，FID_D从0.414降至0.010，原始FID从0.057小幅升至0.066。这表明SATO框架对不同架构基线均具备适配能力。

在KIT-ML数据集上（Table 2），SATO（MoMask）在原始文本上的FID为0.204，扰动文本的FID_P为0.261，预测差异度FID_D为0.011。该结果进一步验证了跨数据集的鲁棒性迁移能力。

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2405_01461/figures/005_Table_2.jpg]]
*Table 2: Quantitative evaluation on the KIT-ML. ± indicates a 95% confidence interval. SATO (T2M-GPT) refers to fine-tuning based on T2M-GPT to create*

人类评估（Table 3）提供了感知层面的证据：在扰动文本条件下，SATO的生成准确率达到75.5%，显著优于基线模型。跨数据集评估中，模型在HumanML3D上训练、以KIT-ML文本测试时，SATO在扰动文本上的准确率为72.3%，原始文本为76.8%，展示了良好的泛化稳定性。

### 消融实验：三个损失函数的贡献

Table 5的消融实验揭示了三个稳定性损失各自的作用机制。仅使用稳定注意力损失$\mathcal{L}_2$时，FID_P为0.614，FID_D为0.034；仅使用扰动损失$\mathcal{L}_3$时，FID_P为0.187，FID_D为0.013。当两者联合使用时，达到最优稳定性：FID_P降至0.155，FID_D降至0.010。这一结果验证了注意力稳定与预测稳定之间存在协同效应——稳定注意力为稳定预测提供了基础，而扰动一致性约束则直接强化了输出鲁棒性。

值得注意的是，单独使用教师一致性损失$\mathcal{L}_1$时，FID_P为1.086，效果有限。这表明仅约束与原始模型的预测接近，不足以应对扰动带来的分布偏移，必须结合注意力层面的显式稳定。

### 扰动方式的比较

Table 6对比了两种扰动策略的效果。随机同义词替换（RSR）在稳定性指标上优于投影梯度下降（PGD）：RSR的FID_P为0.155，PGD为0.247。这一反直觉的结果可能源于RSR生成的扰动更贴近真实用户输入的同义词替换模式，而PGD在嵌入空间中找到的对抗性扰动可能与自然语言分布存在偏差，导致模型学到的鲁棒性泛化能力较弱。

### 注意力稳定性的直接证据

Figure 7和Table 7提供了注意力层面的定量验证。SATO将CLIP文本编码器在扰动前后的注意力Jensen-Shannon散度（JSD）从0.228降至0.188，降幅约17.5%。这一降低直接印证了稳定注意力模块的有效性——模型在文本受扰动后，仍能保持对关键运动描述词的注意力聚焦，从而阻断误差向后续生成阶段的级联传播。

定性可视化（Figure 4、Figure 6）进一步展示了这一机制：当输入文本中的运动关键词被替换时，基线模型的注意力分布发生剧烈偏移，导致生成的动作序列出现灾难性错误；而SATO的注意力权重保持相对稳定，生成的动作序列与原始文本输入高度一致。

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2405_01461/figures/004_Figure_4.jpg]]
*Figure 4: Visual results on user testing. SATO (T2M-GPT) refers to fine-tuning based on T2M-GPT to create SATO. Below each action sequence is the corresponding motion caption. The bold text represents the top-k attention weight words. It can be seen that the perturbation of the caption can lead to changes in the attention of the text, which can lead to catastrophic errors in the generative model. SATO has demonstrated superior stability to other models both in terms of attention and motion prediction*

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2405_01461/figures/012_Figure_6.jpg]]
*Figure 6: Visual comparison between SATO and state-of-the-art approaches. We compare SATO with T2M-GPT [38], MoMask [7], and MotionDiffuse [39]. We present two examples demonstrating predicted action sequences as outputs before and after perturbation. The underlined part is the part that scrambles the description. It can be observed that all models perform relatively accurately on the original text. However, only SATO predicts correctly on perturbed text*

### 与数据增强的对比

Table 7将SATO与单纯的数据增强方法进行了对比。数据增强虽能一定程度提升鲁棒性，但在原始文本上的准确性下降更为明显，且扰动文本上的稳定性增益远不及SATO。这验证了SATO的显式稳定性约束比隐式的数据增强更高效——前者直接针对注意力不稳定这一瓶颈进行优化，后者仅通过增加训练样本多样性间接缓解问题。

### 扰动程度的影响

Figure 5展示了不同扰动水平下的模型稳定性。在所有扰动强度下，SATO的稳定性指标均持续优于基线T2M-GPT。即使在显著扰动条件下，SATO仍保持较低的FID_P和FID_D，表明框架具备应对极端文本变化的鲁棒性。

### 损失权重的参数分析

Table 8分析了三个辅助损失权重$\lambda_1$、$\lambda_2$、$\lambda_3$的敏感性。结果表明，在合理的参数范围内，SATO的性能相对稳定，未出现对特定权重组合的过度依赖，这降低了实际部署时的调参难度。

### 局限性与失败模式

尽管SATO在鲁棒性上取得了显著提升，仍存在若干值得关注的局限：

1. **准确性-鲁棒性权衡**：原始文本上的FID略有上升（T2M-GPT从0.141到0.157），说明稳定性约束对模型在干净输入上的表达能力存在轻微抑制。

2. **训练开销增加**：引入冻结教师模块和扰动生成导致训练时间增加约7.4小时（100k次迭代），对于资源受限场景可能构成负担。

3. **扰动覆盖的局限**：RSR依赖人工构建的同义词替换词典，对未登录词或细粒度语义扰动的覆盖可能不足，在开放域文本输入下稳定性可能下降。

4. **CLIP解冻的风险**：解冻预训练的CLIP文本编码器进行微调，可能引入灾难性遗忘，论文未对此进行深入分析，需要手动验证在极端微调设置下的退化程度。

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2405_01461/figures/010_Table_5.jpg]]
*Table 5: Ablation study results of SATO stability component. We conducted six separate ablation studies on three different loss functions. Bold indicates the best results*

## 定位与知识库关联

### 基线关系与核心改进

SATO 作为一个即插即用的稳定性框架，其核心定位不是提出全新的生成架构，而是在现有文本到运动模型之上构建稳定性增强层。论文选择三类代表性基线进行验证：

- **T2M‑GPT**（Zhang et al., arXiv 2023）：基于 VQ‑VAE 和自回归 Transformer 的生成范式，是 SATO 的主要实验载体。
- **MoMask**（Guo et al., arXiv 2023）：基于生成式掩码建模的范式，SATO 同样在其上进行了适配验证。
- **MotionDiffuse**（Zhang et al., arXiv 2022）：基于扩散模型的范式，用于定性对比。

SATO 在方法层面的关键改进体现在四个维度：

| 改进维度 | 基线做法 | SATO 做法 | 证据强度 |
|---------|---------|----------|---------|
| CLIP 文本编码器 | 冻结（frozen） | 解冻并引入稳定性损失微调 | 强（Section 3.3 明确声明） |
| 注意力稳定性约束 | 无 | 基于 top‑k 重叠的可微分损失 $\mathcal{L}_{\mathrm{Topk}}$ | 强（式 3） |
| 扰动处理机制 | 无 | PGD 对抗扰动或 RSR 同义词替换，配合一致性损失 $\mathcal{L}_3$ | 强（Figure 3(b)） |
| 教师模块 | 无 | 冻结的预训练 T2M‑GPT 作为教师，通过 $\mathcal{L}_1$ 保持预测一致性 | 强（Section 3.3） |

SATO 的核心创新在于将“稳定性”形式化为三个数学约束——预测鲁棒性、预测接近性、top‑k 注意力鲁棒性——并通过最小‑最大优化框架（式 2）统一求解。这种将注意力层面的稳定性与预测层面的鲁棒性联合建模的思路，在文本到运动领域属于首次系统化尝试。

### 适用边界与推广性

SATO 的设计原则使其具备较强的模型迁移能力：论文明确将其定位为“适用于所有使用文本编码器和 Transformer 层的当前方法”的即插即用框架（Section 3.3）。在 HumanML3D 和 KIT‑ML 两个基准上，SATO 分别在 T2M‑GPT 和 MoMask 两种不同范式的基线上取得了显著的稳定性提升（FID_P 从 1.754 降至 0.155），初步验证了框架的通用性。

然而，推广到基于扩散模型的方法（如 MotionDiffuse）时，论文仅提供了定性视觉对比（Figure 6），缺乏定量稳定性指标。扩散模型在推理时涉及多步去噪过程，其注意力机制和预测分布的定义与自回归模型存在差异，SATO 的三个约束是否可直接迁移仍需进一步验证。

### 局限性与权衡

1. **准确性与鲁棒性的权衡**：在未扰动文本上，SATO 的 FID 从 0.141 微升至 0.157，表明稳定性增强以轻微的准确性损失为代价。这是对抗训练和一致性约束中常见的现象，但论文未深入分析该权衡的调节机制（如损失权重 $\lambda_1$、$\lambda_2$、$\lambda_3$ 的敏感性仅通过 Table 8 做了简要参数分析）。

2. **训练开销增加**：引入冻结教师模块和扰动生成导致训练时间增加约 7.4 小时（100k 次迭代），对于需要快速迭代的场景可能构成负担。

3. **扰动覆盖的局限性**：RSR 依赖人工构建的同义词替换词典，对未登录词、细粒度语义扰动（如否定词插入、语序调整）的覆盖能力有限。PGD 虽能探索更广泛的扰动空间，但消融实验（Table 6）显示其稳定性效果反而不如 RSR，该现象的原因未被充分解释。

4. **CLIP 解冻的潜在风险**：解冻预训练的 CLIP 文本编码器可能引入灾难性遗忘，即编码器在通用文本理解能力上的退化。论文未对此风险进行分析或提出缓解策略。

### 开放问题

1. **距离度量 $D_1$ 和 $D_2$ 的精确定义**：论文在式 2 中引入了两个预测分布距离度量，但未给出具体的函数形式。这直接影响约束的语义和优化行为，需要查阅附录或代码确认。

2. **PGD 与 RSR 的差异化效果机制**：Table 6 显示 RSR 的稳定性优于 PGD，但两种扰动方式在注意力向量上产生的具体差异（如扰动方向、幅度分布）未被分析。理解这一机制有助于设计更有效的扰动策略。

3. **FID 三种变体的输入差异**：论文使用了 FID、FID_P、FID_D 三个指标，分别对应原始文本、扰动文本和预测差异的评估。三者在计算时具体使用哪些生成样本和真实样本的配对关系，需要从附录 B 中进一步确认。

4. **框架在其他模态的迁移潜力**：SATO 的注意力稳定性和预测鲁棒性约束不依赖于运动生成的特定假设，理论上可迁移到其他文本到序列生成任务（如文本到语音、文本到视频）。但论文未讨论这一可能性，也未提供跨模态的初步实验证据。

## 原文 PDF

![[paperPDFs/ACM_MM_2024/SATO_Stable_Text_to_Motion_Framework.pdf]]
