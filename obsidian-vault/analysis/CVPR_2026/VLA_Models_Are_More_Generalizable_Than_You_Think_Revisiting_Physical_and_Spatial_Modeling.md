---
title: "VLA Models Are More Generalizable Than You Think: Revisiting Physical and Spatial Modeling"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/VLA_Models_Are_More_Generalizable_Than_You_Think_Revisiting_Physical_and_Spatial_Modeling.pdf
project_link: null
code_link: null
aliases:
- FTMFFLAF
- VMAMGTYTRPSM
tags:
- CVPR_2026
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/representation_learning
core_operator: 视觉嵌入空间与下游策略模块的协调一致性——通过轻量级视觉特征调整（仿射变换或低秩适配）即可校准该一致性。
primary_logic: 预训练的VLA模型内部蕴含着潜在的鲁棒性，只需对视觉通路进行极小规模的单次适配，即可激活这些不变性，恢复视点泛化能力，而无需大规模重训或额外数据。
claims:
- 视觉扰动导致的嵌入空间系统性漂移是性能下降的主因，适配视觉模块本身即可恢复协调性。
- 仅4K参数的FTM便将LIBERO视点准确率从48.5%提升至87.1%，证明局部仿射调制足矣。
- FLA以4.7M参数达到90.8%成功率，超越467M参数的LoRA全模型微调，表明视觉层的低秩更新效率极高。
- LIBERO (novel camera viewpoints, average across suites) 上 平均成功率（SR%） = FTM 87.1%; FLA 90.8%
---

# VLA Models Are More Generalizable Than You Think: Revisiting Physical and Spatial Modeling

> [!tip] 核心洞察
> 预训练的VLA模型内部蕴含着潜在的鲁棒性，只需对视觉通路进行极小规模的单次适配，即可激活这些不变性，恢复视点泛化能力，而无需大规模重训或额外数据。

| 字段 | 内容 |
|------|------|
| 中文题名 | VLA模型比你想象的更具泛化性：重新审视物理与空间建模 |
| 英文题名 | VLA Models Are More Generalizable Than You Think: Revisiting Physical and Spatial Modeling |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.02902) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/representation_learning |
| Method | Feature Token Modulation (FTM) and Feature Linear Adaptation (FLA) |
| Dataset | LIBERO, LIBERO-V, LIBERO Novel View across perturbation scales |

> [!tip] 效果简介
> - LIBERO (novel camera viewpoints, average across suites) 上，平均成功率（SR%） FTM 87.1%; FLA 90.8% vs π0.5 Zero-Shot 48.5%; π0.5 LoRA 90.3% (vs Zero-Shot: +38.6% (FTM) / +42.3% (FLA); vs LoRA: -3.2% (FTM) / +0.5% (FLA) 但...)。
> - LIBERO-V (visual perturbations overall) 上，平均成功率（SR%） FTM 90.5%; FLA 94.8% vs π0.5 Zero-Shot 83.6%; π0.5 LoRA 94.6% (vs Zero-Shot: +6.9% (FTM) / +11.2% (FLA); vs LoRA: -4.1% (FTM) / +0.2% (FLA), 且...)。
> - LIBERO Novel View across perturbation scales (Small→Medium→Large) 上，平均成功率（SR%） FLA 94.6 / 90.0 / 87.9 (Small/Medium/Large) vs π0.5 LoRA 94.8 / 90.5 / 85.6 (在大幅度扰动下FLA (+2.3%) 表现出更稳定的适应性)。

## 概要

视觉-语言-行动（VLA）模型在机器人操作中展现出强大潜力，但其对视觉扰动——尤其是相机视点变化——的鲁棒性仍是一个关键瓶颈。本文通过系统性分析揭示了一个反直觉的核心发现：**视点变化下VLA性能下降的主要原因并非物理建模（Physical Modeling）能力不足，而是空间建模（Spatial Modeling）中视觉嵌入空间的系统性漂移**——这种漂移破坏了视觉编码器与下游VLM解码器之间的协调一致性，而非暴露视觉运动能力的根本缺陷。

基于这一洞察，本文提出了一个统一的**单次（One-Shot）鲁棒性适配框架**，仅需一次人类演示即可完成适配，包含两种轻量级方法：

- **Feature Token Modulation (FTM)**：对视觉token嵌入施加全局仿射变换 $\hat{F} = (1 + \gamma) \odot F + \beta$，仅引入约4K可训练参数。
- **Feature Linear Adaptation (FLA)**：在SigLIP ViT编码器的线性层中注入低秩适配（LoRA），以 $W' = W + BA$ 的形式进行内部特征调整。

两种方法均**仅适配视觉通路**，冻结VLM骨干和Action Expert的全部参数，从而以极小代价恢复视点泛化能力。

在LIBERO新视点基准上，FTM仅凭4K参数将零样本成功率从48.5%提升至87.1%；FLA以4.7M参数达到90.8%，超越使用467M参数的LoRA全模型微调基线（90.3%）。在涵盖视点、光照、背景纹理和噪声四类扰动的LIBERO-V基准上，FLA进一步达到94.8%的平均成功率。真实世界实验亦验证了该方法在Franka Emika Panda平台上的有效性。

这些结果表明，预训练VLA模型内部蕴含着潜在的鲁棒性，仅需对视觉通路进行极小规模的单次适配即可激活这些不变性，无需大规模重训或额外数据。

### 视觉-语言-动作模型的空间泛化困境

视觉-语言-动作（VLA）模型通过大规模预训练，在机器人操作任务中展现出令人瞩目的通用性。然而，当部署环境中的相机视点发生偏移——哪怕只是轻微的拍摄角度变化——模型性能往往出现断崖式下跌。这一现象暴露了一个核心矛盾：VLA模型在语义理解和动作生成层面具有强大的能力储备，却在**空间建模**这一基础维度上异常脆弱。

问题的本质并非模型缺乏视觉运动能力。视觉扰动引发的性能退化，根源在于**视觉编码器与下游多模态解码器之间的协调性断裂**。具体而言，视点变化导致视觉嵌入空间发生系统性漂移，使得原本在源域中习得的“视觉-动作”映射关系在目标域中失效。这一发现重塑了对VLA泛化瓶颈的认知：瓶颈不在物理建模，而在空间建模中的**嵌入分布失配**。

### 现有适配方案的效率困境

面对视点泛化问题，当前主流方案存在明显的效率与效果矛盾：

- **全模型微调**：对VLA全部参数进行适配，虽然能恢复性能，但参数量巨大（如π0.5的LoRA全模型微调需467M参数），且每次面对新视点都需重复这一昂贵过程。
- **视觉骨干替换**：如GeoAware-VLA将视觉编码器替换为几何感知的VGGT，并从头训练策略。这种方式破坏了预训练模型的完整性，且需要大量领域数据。
- **提示学习**：在输入序列中插入可学习提示token，冻结骨干仅优化提示参数。该方法参数效率高，但在空间建模上的适配能力有限。

这些方案的共同盲点是：它们或过度调整了本已具备鲁棒性的高层语义模块，或完全抛弃了预训练视觉编码器中蕴含的丰富先验。一个更根本的问题是——**是否真的需要扰动整个模型，还是仅需校准视觉通路中的分布偏移？**

### 核心动机：激活预训练模型的内在鲁棒性

本文的核心假设是：预训练的VLA模型内部已经蕴含着应对视点变化的潜在不变性，只是这些不变性被视觉嵌入的分布漂移所“掩盖”。因此，适配的目标不是重新学习视觉运动策略，而是通过**极轻量的视觉特征校准**，恢复视觉编码器与解码器之间的协调关系。

这一动机催生了两个关键设计原则：

1. **适配范围最小化**：仅作用于视觉通路，冻结VLM解码器和动作专家（Action Expert），保留预训练模型的高层推理与运动生成能力。
2. **参数效率极致化**：通过全局仿射调制或低秩更新实现校准，参数量控制在4K至4.7M量级，使得**单次演示即可完成适配**（One-Shot Adaptation）。

### 问题定位与本文贡献

综上，本文聚焦于VLA模型在视点变化下的空间建模瓶颈，提出一个统一的单次鲁棒性适配框架。该框架包含两种互补的轻量级机制——**Feature Token Modulation（FTM）**和**Feature Linear Adaptation（FLA）**——分别从视觉token的全局分布校准和ViT编码器的内部特征调整两个层面，恢复嵌入空间的跨域对齐。这一框架不仅以不到全模型微调1%的参数量达到甚至超越其性能，更揭示了VLA模型泛化性的本质：**鲁棒性早已存在，只需找到正确的钥匙将其激活**。

## 核心方法与创新机理

### 瓶颈重定义：从物理建模到空间建模

现有VLA（Vision-Language-Action）模型在视点变化下的性能退化，通常被归因于物理建模（Physical Modeling）能力的不足。本文通过系统分析揭示了一个被忽视的核心瓶颈：**视觉扰动主要导致视觉嵌入空间的系统性漂移，破坏了视觉编码器与VLM解码器之间的协调一致性，而非暴露视觉运动能力的根本缺陷**。这一发现将问题从“模型能力不足”重新定义为“嵌入空间失配”，为极轻量级的适配策略提供了理论依据。

### 方法谱系与知识库定位

当前VLA模型的视点泛化方案可归为三类：

- **视觉骨干替换**：如**GeoAware-VLA**，将视觉编码器替换为几何感知的VGGT编码器并从头训练策略。该路线引入新的视觉骨干，计算与数据成本高昂。
- **全模型微调**：如**π0.5 One-Shot LoRA**，同时对VLM和Action Expert的注意力与FFN层施加低秩适配（467M参数）。该方法更新范围过大，参数效率低且存在过拟合风险。
- **提示学习**：在输入序列中插入可学习提示token，冻结骨干仅优化提示。该方法未直接干预视觉特征空间，对齐能力有限。

本文提出的两条轻量级适配路径——**Feature Token Modulation (FTM)** 和 **Feature Linear Adaptation (FLA)**——位于上述谱系的极端参数高效端：仅适配视觉通路，完全冻结VLM解码器与Action Expert。

### 关键创新槽位

| 创新维度 | 基线方法 | 本文方法 | 证据锚点 |
|---------|---------|---------|---------|
| **适配范围** | 全局微调VLA全部参数或替换视觉骨干 | 仅适配视觉通路（视觉token全局仿射调制 或 ViT线性层低秩更新） | “adapting only the visual module through lightweight mechanisms—either token modulation or a LoRA-based update—instead of globally finetuning the VLA.” |
| **FTM机制** | 无（视觉token直接传入解码器） | 对视觉token施加全局仿射变换 $\hat{F} = (1 + \gamma) \odot F + \beta$ | Eq. (4)；仅4K参数将LIBERO视点准确率从48.5%提升至87.1% |
| **FLA机制** | 冻结ViT线性层（无适配） | 对SigLIP ViT的线性层注入LoRA适配器 $W' = W + BA$ | Eq. (5)；4.7M参数达90.8%成功率，超越467M参数的LoRA全模型微调 |

### 因果机制解析

两类方法的核心差异在于干预层级：

- **FTM** 在视觉编码器输出端施加全局仿射变换，本质上是对嵌入空间进行**平移与缩放校准**。其假设是视点变化引起的嵌入偏移具有全局系统性，仅需两个可学习向量（$\gamma, \beta \in \mathbb{R}^{D_{\text{ViT}}}$，$D_{\text{ViT}}=2048$）即可重对齐分布。该设计的极端参数效率（4K参数）强有力地验证了“嵌入空间漂移是主因”的核心论断。

- **FLA** 进一步深入ViT编码器内部，对线性层注入低秩更新。这允许对特征提取过程进行更精细的调整，同时通过低秩约束（秩$r \ll \min(d_{\text{in}}, d_{\text{out}})$）保持参数效率。FLA在秩16时以4.7M参数超越LoRA的467M参数，且在大幅度视点扰动下（Large scale）表现出更稳定的适应性（FLA 87.9% vs LoRA 85.6%），表明视觉层内部的低秩更新比全局微调更能捕捉视点不变性。

### 训练稳定性优势

与LoRA和全微调相比，FLA展现出显著优越的训练稳定性。在LIBERO新视点任务的训练过程中，FLA收敛后无过拟合现象，而LoRA基线在训练后期出现性能波动（见Figure 12）。这一特性源于FLA仅干预视觉编码器的线性层，保留了预训练VLM解码器的完整推理能力，避免了全模型微调中多模块联合优化引入的不稳定性。

### 方法普适性

FLA的适配范式在不同VLA基础模型上均表现出有效性：在OpenVLA-OFT上以秩8达到89.0%，在π0上达到82.8%，在π0.5上达到91.05%（见Table 8）。这表明“视觉通路轻量适配”的策略并非特定于π0.5架构，而是VLA模型视点泛化的通用解决方案。

### 局限性提示

FTM依赖全局仿射假设——当嵌入偏移具有高度非线性和局部性时，仅凭仿射调制可能不足以完全恢复性能。FLA虽通过低秩更新部分缓解此问题，但在极端非线性扰动下的理论上限仍需进一步验证。此外，当前实验主要在静态扰动类型（视点、光照、纹理、噪声）下评估，动态场景中快速移动障碍物或交互式力反馈等复杂物理扰动下的表现尚待探索。

### 核心瓶颈

视点变化下VLA模型性能下降的主要瓶颈在于**空间建模中的视觉嵌入分布偏移**，而非物理建模部分的能力不足。具体而言，视觉扰动引发的嵌入空间系统性漂移破坏了视觉编码器与VLM头之间的协调一致性，使得冻结的策略模块无法正确解释来自新视点的视觉token。

### 设计思路

基于上述诊断，本文提出了一套**统一的单次鲁棒性适配框架**，其核心思想是：**仅适配视觉通路**，通过轻量级机制校准视觉嵌入空间与下游策略模块的协调关系，从而激活预训练模型内部蕴含的视点不变性。

具体包含两种互补的适配方法：

- **Feature Token Modulation (FTM)**：在视觉token输出端施加全局仿射变换，以极低成本重对齐嵌入分布。
- **Feature Linear Adaptation (FLA)**：在ViT编码器内部注入低秩适配器，从特征提取源头调整视觉表示。

两种方法均保持VLM骨干和Action Expert完全冻结，仅需**一次人类演示**即可完成适配，无需大规模重训或额外数据。

### 整体Pipeline

下图展示了适配框架的完整流程：

1. **视觉编码器 $f_v$**：将输入图像映射为视觉token嵌入序列。在FLA方案中，编码器内部的线性层被注入LoRA适配器以调整特征提取。
2. **语言编码器 $f_\ell$**：将任务语言指令映射为文本嵌入。
3. **特征适配模块 $\mathcal{A}_\phi$**：对视觉token施加轻量级变换——FTM通过全局仿射调制 $\hat{F} = (1 + \gamma) \odot F + \beta$ 校准嵌入分布；FLA则通过低秩更新 $W' = W + BA$ 从内部调整ViT的线性层。
4. **多模态Transformer解码器 $g$**：基于适配后的视觉嵌入与语言嵌入，自回归预测离散动作token：$\hat{a}_t \sim g(a_{<t}; [\mathcal{A}_\phi(f_v(v)); \ell])$。
5. **Action Expert $\pi_\theta(a|\cdot)$**：基于条件流匹配生成连续动作序列，由当前观测和高层语义条件控制。

### 关键公式

适配后的预测分布可统一表示为：

$$P_{\theta,\phi}(a_t \mid a_{<t}, o_{\le t}) = g(a_{<t}; [\mathcal{A}_{\phi}(f_v(v)); \ell])$$

其中 $\mathcal{A}_\phi$ 为FTM或FLA所定义的视觉特征适配变换，$\theta$ 为冻结的预训练参数，$\phi$ 为仅有的可学习适配参数。

![[assets/figures/papers/paper_list_l2653_https_arxiv_org_abs_2512_02902/figures/011_Figure_6.jpg]]
*Figure 6: Real-World Experimental Setup. (a) Our hardware environment features a Franka Emika Panda robot teleoperated via the GELLO framework, equipped with both a third-person static camera and a wrist-mounted camera. (b) The Novel Camera Viewpoint used for one-shot adaptation. This viewpoint introduces a significant spatial shift compared to the standard pre-training distribution, serving as the testbed for our Feature Linear Adaptation (FLA) method*

### 3.1 问题建模：VLA策略的视点泛化瓶颈

预训练的VLA模型通常将动作生成建模为自回归过程。给定观测序列 $o_{1:T}$，原始π0.5策略的动作分布为：

$$P_{\theta}(a_{1:T} \mid o_{1:T}) = \prod_{t=1}^{T} P_{\theta}(a_t \mid a_{<t}, o_{\leq t})$$

在解码阶段，Multimodal Transformer解码器 $g$ 基于视觉嵌入 $\mathbf{z}$ 和语言嵌入 $\ell$ 预测动作token：

$$\hat{a}_t \sim g(a_{<t}; [\mathbf{z}; \ell])$$

其中视觉嵌入由冻结的视觉编码器 $f_v$ 产生：$\mathbf{z} = f_v(v)$。

**核心瓶颈**：当相机视点发生变化时，视觉扰动主要导致视觉嵌入空间的系统性漂移，破坏了视觉编码器与VLM解码器之间的协调一致性，而非暴露视觉运动能力的根本性不足。因此，适配目标并非重新训练整个VLA，而是校准视觉嵌入分布以恢复原有的空间-语义对齐。

### 3.2 统一适配框架

本文提出统一的单次鲁棒性适配框架，将适配后的预测分布表述为：

$$P_{\theta,\phi}(a_t \mid a_{<t}, o_{\le t}) = g(a_{<t}; [\mathcal{A}_{\phi}(f_v(v)); \ell])$$

其中 $\mathcal{A}_{\phi}$ 是作用于视觉token的轻量级适配变换，$\phi$ 为可学习参数。该框架的核心设计原则是：**冻结VLM骨干网络和Action Expert，仅适配视觉通路**，从而以极小参数量恢复视点泛化能力。

### 3.3 Feature Token Modulation (FTM)

FTM对视觉编码器输出的token嵌入 $F \in \mathbb{R}^{N \times D_{\text{ViT}}}$ 施加全局仿射变换：

$$\hat{F} = (1 + \gamma) \odot F + \beta$$

其中 $\gamma, \beta \in \mathbb{R}^{D_{\text{ViT}}}$ 为可学习的逐通道缩放因子和偏置向量，$\odot$ 表示逐元素乘法。该设计仅引入 $2 \times D_{\text{ViT}}$ 个可训练参数（对于SigLIP ViT，$D_{\text{ViT}}=2048$，总计约4K参数），通过全局仿射调制即可校准嵌入分布的系统性漂移。训练时通过辅助损失监督调制效果，推理时直接应用学习到的变换。

**设计直觉**：视觉扰动引起的嵌入偏移在通道维度上呈现一定的全局一致性，因此逐通道的仿射变换足以部分恢复与解码器的对齐，而无需更新ViT内部权重。

### 3.4 Feature Linear Adaptation (FLA)

FLA将低秩适配（LoRA）注入SigLIP ViT编码器的线性层，实现更精细的内部特征调整。对于预训练的线性权重矩阵 $W \in \mathbb{R}^{d_{\text{out}} \times d_{\text{in}}}$，FLA引入低秩更新：

$$W' = W + \Delta W, \quad \Delta W = B A$$

其中 $A \in \mathbb{R}^{r \times d_{\text{in}}}$，$B \in \mathbb{R}^{d_{\text{out}} \times r}$，秩 $r \ll \min(d_{\text{in}}, d_{\text{out}})$。在秩 $r=16$ 的默认配置下，FLA仅引入约4.7M可训练参数，不足全模型LoRA微调（467M参数）的1%。

**与FTM的关系**：FTM在嵌入输出端进行全局校准，假设偏移具有通道级一致性；FLA则在ViT内部进行层级低秩调整，能够捕捉更复杂的非线性特征偏移。两者构成从粗到细的适配谱系。

### 3.5 Action Expert的条件流匹配

VLA策略被分解为高层VLM骨干和低层Action Expert的层次推断：

$$\pi_{\theta}(a_{t:t+H}, \hat{l} | o_t, l) = \pi_{\theta}(a_{t:t+H} | o_t, \hat{l}) \cdot \pi_{\theta}(\hat{l} | o_t, l)$$

Action Expert基于条件流匹配生成连续动作序列。流匹配采用线性插值路径连接噪声 $\omega$ 和动作数据 $a$：

$$a^{\tau} = \tau a_{t:t+H} + (1 - \tau) \omega$$

时间步 $\tau$ 通过正弦编码和MLP注入AdaRMSNorm层以调节特征：

$$\text{AdaRMSNorm}(x, \tau) = y \cdot (1 + \gamma(\tau)) + \beta(\tau), \quad y = \frac{x}{\|x\|_2}$$

在FTM/FLA适配过程中，Action Expert始终保持冻结，仅依赖校准后的视觉嵌入来恢复精确控制信号的生成。

## 实验与关键发现

### 核心瓶颈验证：空间建模中的视觉嵌入漂移

实验设计的起点是对“视点变化下VLA失效根源”的因果诊断。本文的核心假设是：视觉扰动主要引发视觉嵌入空间的系统性漂移，破坏视觉编码器与VLM解码器之间的协调性，而非暴露视觉运动能力的根本不足。这一假设通过以下关键实验得到验证：

- **零样本性能的急剧下降**：预训练的π0.5模型在LIBERO标准视点下表现良好，但在新视点下零样本成功率骤降至48.5%（Table 1），表明模型内部存在可恢复的潜在能力，而非完全缺乏视点泛化能力。
- **轻量适配的显著恢复**：仅对视觉token施加全局仿射变换（FTM，4K参数）即可将成功率提升至87.1%；对ViT线性层注入低秩更新（FLA，4.7M参数）更达到90.8%（Table 1）。这种“极小干预、极大恢复”的现象直接证明瓶颈在于视觉嵌入的分布对齐，而非策略网络的容量不足。
- **嵌入空间可视化证据**：t-SNE可视化（Figure 10）显示，适配前源域与目标域的视觉token嵌入存在显著的域间隙，而FLA适配后目标域嵌入被投影至源域流形上，恢复了特征空间的连通性，使得冻结的策略网络能够正常工作。

![[assets/figures/papers/paper_list_l2653_https_arxiv_org_abs_2512_02902/figures/015_Figure_10.jpg]]
*Figure 10: Visualization of Visual Token Embeddings via t-SNE. (a) Before Adaptation: A significant domain gap is observed between the source (blue) and target (red) embeddings, indicating severe spatial misalignment caused by viewpoint shifts. (b) After FLA: Our method projects the target embeddings (green) to align with the source manifold. This manifold alignment restores the connectivity of the feature space, allowing the frozen policy to function correctly without requiring the distributions to perfectly overlap*

### 主实验结果

#### LIBERO新视点基准（Table 1, Figure 5）

![[assets/figures/papers/paper_list_l2653_https_arxiv_org_abs_2512_02902/figures/007_Figure_5.jpg]]
*Figure 5: Success rates before and after adaptation on the LIBERO benchmark under novel camera viewpoints. We report Success Rate (SR) across all unseen viewpoints [31] in the LIBERO suites [21]. “Before” corresponds to the zero-shot performance of pretrained policies without any adaptation*

在LIBERO四个子套件（LIBERO-Spatial, LIBERO-Object, LIBERO-Goal, LIBERO-100）的新视点设定下，FTM和FLA均展现出极强的视点泛化能力：

- **FTM**：平均成功率87.1%，较零样本π0.5（48.5%）提升38.6个百分点，仅使用4K可训练参数。
- **FLA**：平均成功率90.8%，较零样本提升42.3个百分点，甚至超越了一发LoRA全模型微调（90.3%，467M参数），而参数量仅为其1%（4.7M vs 467M）。

这一结果具有双重意义：一方面，FLA以极低的参数代价超越了传统的全模型微调范式；另一方面，它证明了对视觉编码器内部特征提取过程的低秩调整，比全局仿射调制（FTM）能更精细地处理视点变化带来的非线性嵌入偏移。

与其他基线的对比同样关键：
- **GeoAware-VLA**：虽替换视觉骨干为几何感知的VGGT编码器并从头训练，但平均成功率仅为72.8%，远低于FTM/FLA。这从反面说明，预训练VLA模型内部蕴含的视觉运动知识远强于从头训练的几何感知模型，关键在于如何激活这些潜在能力。
- **OpenVLA-OFT**：零样本性能仅34.3%，而在LIBERO-Plus多视角数据上微调后的OpenVLA-OFT-m也仅达82.0%，仍低于FTM的87.1%。这表明大规模多视角数据的暴力微调效率远不如针对视觉通路的精准适配。

#### 视点扰动幅度分析（Table 2, Figure 11）

LIBERO新视点基准进一步将相机偏移按幅度分为Small、Medium、Large三个等级。FLA在不同幅度下均保持高成功率：
- Small: 94.6%（vs π0.5 LoRA 94.8%）
- Medium: 90.0%（vs π0.5 LoRA 90.5%）
- Large: 87.9%（vs π0.5 LoRA 85.6%）

值得注意的是，在大幅度视点偏移下，FLA反而以2.3个百分点的优势超越LoRA全模型微调。这说明当视觉分布偏移加剧时，仅适配视觉模块的策略比全局微调更稳定——全局微调可能因过度调整VLM或Action Expert的参数而破坏预训练知识的泛化结构。

#### LIBERO-V视觉鲁棒性基准（Table 3, Table 4）

![[assets/figures/papers/paper_list_l2653_https_arxiv_org_abs_2512_02902/figures/008_Table_3.jpg]]
*Table 3: Success rates on the LIBERO-V (Visual) benchmark. The benchmark evaluates robustness across four visual perturbations: camera viewpoint, lighting, background texture, and noise. Results marked with ∗ are taken from [8]*

![[assets/figures/papers/paper_list_l2653_https_arxiv_org_abs_2512_02902/figures/009_Table_4.jpg]]
*Table 4: Parameter count and accuracy on the LIBERO-V (Visual) benchmark*

LIBERO-V基准综合评估了四种视觉扰动类型：相机视点、光照变化、背景纹理替换和图像噪声。FTM和FLA在所有扰动类型上均表现出色：
- FLA总体准确率94.8%，超越π0.5 LoRA（94.6%），且参数量减少99%。
- FTM以0.004M参数达到90.5%的总体准确率，充分证明全局仿射假设在多种视觉扰动下的普适性。

### 消融实验

#### FLA秩的敏感性分析（Table 5）

![[assets/figures/papers/paper_list_l2653_https_arxiv_org_abs_2512_02902/figures/010_Table_5.jpg]]
*Table 5: Efficiency of our FLA adaptation. FLA (rank = 16) achieves a 90.8% success rate using only 4.7M parameters, compared to LoRA’s 467M parameters at 90.3%*

FLA的核心超参数是LoRA的秩$r$。实验表明：
- 秩从16增至32时，LIBERO成功率从90.8%微升至91.2%，提升仅0.4个百分点。
- 这表明适度的容量增加略有裨益，但并非必需——秩16已足以捕获视点变化带来的特征偏移模式。

#### 跨VLA模型的泛化性验证（Table 8）

为验证方法的模型无关性，FLA被应用于三种不同的VLA基础模型：OpenVLA-OFT、π0和π0.5。仅需秩8的极低秩适配，所有模型在新视点下的成功率均突破80%：
- OpenVLA-OFT: 89.0%
- π0: 82.8%
- π0.5: 91.05%

这一跨架构的普适性强烈暗示：视觉嵌入漂移是当前VLA模型的共性瓶颈，而轻量视觉适配是解决该瓶颈的通用方案。

#### 训练稳定性（Figure 12）

与LoRA和全微调相比，FLA在训练过程中表现出卓越的稳定性：收敛后成功率保持平稳，无过拟合迹象。而LoRA和全微调均出现不同程度的性能波动或过拟合。这归因于FLA仅调整视觉编码器的线性层，保留了VLM和Action Expert的完整预训练知识，避免了在少量适配数据上的灾难性遗忘。

### 真实世界验证（Figure 6, Figure 7）

在Franka Emika Panda机器人平台上，FLA经过一次人类演示适配后，成功完成了五项操作任务：抓取红色方块、将红色方块堆叠到绿色方块上、关闭微波炉门、按下绿色按钮、拉出顶层抽屉。尽管新视点与预训练分布存在显著的空间偏移，适配后的策略仍能恢复空间定位能力，以闭环方式执行精确操作。

此外，FLA在面对动态对象干扰（Figure 8）和非完美演示（Figure 9）时，仍保持高成功率和实时轨迹调整能力，展现出良好的鲁棒性和实用性。

### 失败模式与局限性

1. **高度非线性嵌入偏移**：FTM依赖全局仿射假设，当视点变化引发的嵌入偏移具有强非线性或局部性时，仅凭仿射调制可能不足以完全恢复性能。此时需使用FLA进行更精细的内部特征调整。

2. **动态物理扰动未覆盖**：当前实验主要在静态视觉扰动（视点、光照、纹理、噪声）下评估，未涉及动态场景中的快速移动障碍物或交互式力反馈等复杂物理扰动。在这些场景下，仅适配视觉通路可能不足。

3. **真实世界规模有限**：真实世界验证仅包含五项操作任务和单一机器人平台（Franka Emika Panda），更大规模、更多样化场景下的性能尚待进一步验证。

4. **单次适配的持久性**：当任务分布持续变化时（如终身学习场景），如何动态更新这些极轻量的适配参数而不引起灾难性遗忘，是尚待解决的开放问题。

## 定位与知识库关联

### 1. 核心问题定位：空间建模与物理建模的解耦

本工作将VLA（Vision-Language-Action）模型的泛化性问题分解为两个正交维度：**物理建模（Physical Modeling）**与**空间建模（Spatial Modeling）**。物理建模指模型理解物体交互、动力学和任务语义的能力；空间建模则指模型将视觉观测映射到与下游策略模块协调一致的嵌入空间的能力。

核心发现是：视点变化下VLA性能下降的主要瓶颈在于**空间建模中的视觉嵌入分布偏移**，而非物理建模能力的不足。具体而言，视觉扰动导致视觉嵌入空间发生系统性漂移，破坏了视觉编码器与VLM解码头之间的协调一致性（coordination），而非暴露了视觉运动能力的根本缺陷。这一诊断将问题从“模型容量不足”重新定义为“特征空间失配”，为轻量级适配方案提供了理论前提。

### 2. 方法谱系：从全局微调到视觉通路定向校准

#### 2.1 现有基线方法及其局限

在VLA模型的视觉鲁棒性适配领域，现有方案可归纳为三条技术路线：

**路线一：视觉骨干替换与从头训练。** **GeoAware-VLA** 将视觉骨干替换为几何感知的VGGT编码器，并从头训练策略。此路线引入了显著的架构变更和训练成本，且无法复用预训练VLA的已有能力。

**路线二：全模型微调。** 以 **π0/π0.5 One-Shot LoRA** 为代表，使用LoRA同时对VLM和Action Expert的注意力层与前馈层进行适配，秩为16/32，可训参数达467M。该方法虽能达到90.3%的LIBERO新视点成功率，但参数效率极低，且需更新VLM解码器和动作专家两个模块，违背了“瓶颈仅在视觉通路”的诊断。

**路线三：提示学习（Prompt Learning）。** 在输入序列中插入可学习提示token，冻结骨干仅优化提示。该方法未直接针对视觉嵌入的分布偏移进行校准，属于间接适配策略。

此外，**OpenVLA-OFT**（零样本）和 **OpenVLA-OFT-m**（在LIBERO-Plus多视角数据上微调）作为参照基线，后者利用大规模多视角数据获得性能提升，但数据需求远高于本工作的单次人类演示适配设定。

#### 2.2 本工作的方法定位：视觉通路的极轻量单次适配

本工作提出的统一框架包含两个递进的适配机制，均**仅作用于视觉通路**，冻结VLM解码器和Action Expert：

- **Feature Token Modulation (FTM)**：在视觉编码器输出的视觉token嵌入上施加全局仿射变换 $\hat{F} = (1 + \gamma) \odot F + \beta$，其中 $\gamma, \beta \in \mathbb{R}^{D_{\text{ViT}}}$（$D_{\text{ViT}}=2048$），可训参数仅4K。该方法假设嵌入偏移具有全局平移-缩放性质，通过两个参数向量即可重对齐嵌入空间。

- **Feature Linear Adaptation (FLA)**：将LoRA低秩更新 $W' = W + \Delta W, \Delta W = BA$ 注入SigLIP ViT编码器的线性层，实现内部特征提取的自适应调整。在秩为16时，可训参数仅4.7M，不足LoRA全模型微调的1%。

二者的关键设计选择在于**适配范围严格限定于视觉模块**——FTM作用于编码器输出端，FLA作用于编码器内部线性层——而完全不触及VLM解码器或Action Expert的权重。这一设计直接源于对瓶颈的诊断：既然问题出在视觉嵌入空间的系统性漂移，那么校准视觉通路本身即可恢复与下游模块的协调性。

### 3. 与知识库中相关工作的关系

#### 3.1 与参数高效微调（PEFT）谱系的关系

本工作的方法论可视为参数高效微调（PEFT）技术在具身智能领域的定向应用，但其独特贡献在于**将适配范围的选择本身作为核心设计变量**。传统PEFT方法（如LoRA、Adapter、Prompt Tuning）通常将适配器均匀或启发式地注入模型各层，而本工作通过因果诊断明确识别出视觉通路为唯一的适配靶点，从而在参数效率上获得数量级优势。

FTM可视为一种极简的“特征空间校准层”，类似于Feature-wise Transformation在域自适应中的应用，但将其简化为仅两个参数向量的全局仿射变换。FLA则是将LoRA的适用范围从“全模型”收缩至“ViT编码器线性层”，实现了适配容量与任务需求的精确匹配。

#### 3.2 与VLA模型鲁棒性研究的关系

在VLA鲁棒性研究的知识脉络中，本工作填补了“轻量级空间建模适配”这一空白。现有工作或依赖大规模多视角数据（如OpenVLA-OFT-m的LIBERO-Plus微调），或诉诸架构级修改（如GeoAware-VLA的VGGT骨干替换），而本工作证明了：**预训练VLA模型内部蕴含着潜在的鲁棒性，仅需对视觉通路进行极小规模的单次适配即可激活这些不变性**。这一发现将研究重心从“获取更多数据或更强骨干”转向“挖掘预训练模型已有的泛化能力”。

### 4. 适用边界与局限

#### 4.1 已验证的适用条件

- **扰动类型**：实验覆盖了静态视觉扰动（视点变化、光照变化、背景纹理替换、图像噪声），在LIBERO和LIBERO-V基准上验证了有效性。
- **模型架构**：方法在三种VLA基础模型（OpenVLA-OFT、π0、π0.5）上均表现出普适性，仅需秩8的FLA即可将零样本性能提升至80%以上。
- **数据效率**：所有实验均基于单次人类演示（one-shot）完成适配，无需大规模多视角数据。

#### 4.2 已知局限

1. **动态物理扰动的未覆盖**：实验主要在静态扰动类型下评估，未涉及动态场景中快速移动的障碍物或交互式力反馈等复杂物理扰动。当嵌入偏移同时涉及时间维度的动态变化时，静态仿射或低秩假设可能不足。

2. **FTM的全局仿射假设限制**：FTM假设嵌入偏移具有全局平移-缩放性质。当偏移呈现高度非线性和局部性时（例如局部遮挡或非均匀光照），仅凭两个参数向量的全局调制可能不足以完全恢复性能。FLA通过ViT内部低秩更新部分缓解了此问题，但仍受限于低秩假设的表达能力。

3. **真实世界验证的规模有限**：真实世界实验仅包含5个操作任务和单一Franka Emika Panda机器人平台，更大规模、更多样化场景下的性能尚待进一步验证。

4. **单次适配的静态性**：当前方法假设适配目标域是固定的。在持续学习或终身任务流中，如何动态更新这些极轻量适配参数而不引起灾难性遗忘，仍是未解决的问题。

### 5. 开放问题

1. **跨模型泛化**：FTM/FLA的适配范式能否直接推广到其他具身基础模型（如RT-2、Octo）而不需要结构修改？当前验证限于基于SigLIP ViT的VLA架构，对其他视觉骨干的适用性尚待检验。

2. **持续适配与灾难性遗忘**：在任务序列中，如何为新视点增量添加适配参数，同时保持对先前视点的性能？FTM的4K参数规模为每个域维护独立参数提供了可能，但域间的干扰与共享机制需进一步研究。

3. **多模态联合适配**：能否将提示学习（Prompt Learning）与FTM/FLA相结合，形成文本-视觉联合的跨扰动适配策略？当前方法仅适配视觉通路，语言编码器保持冻结，但语言指令与视觉观测的联合分布偏移可能蕴含更丰富的校准信号。

4. **瓶颈诊断的跨任务普适性**：在纯语言或纯视觉任务上，类似的空间建模瓶颈（即嵌入空间的系统性漂移而非能力缺失）是否同样存在，且能否用类似方法缓解？这关系到该诊断框架能否从具身智能推广至更广泛的视觉-语言模型鲁棒性研究。

5. **非线性偏移的建模**：当嵌入偏移超出仿射或低秩假设的表达范围时，需要何种更灵活但同样参数高效的适配机制？可能的扩展方向包括逐token的条件调制或轻量级注意力重校准。

## 原文 PDF

![[paperPDFs/CVPR_2026/VLA_Models_Are_More_Generalizable_Than_You_Think_Revisiting_Physical_and_Spatial_Modeling.pdf]]
