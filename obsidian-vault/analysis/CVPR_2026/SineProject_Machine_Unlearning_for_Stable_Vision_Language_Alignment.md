---
title: "SineProject: Machine Unlearning for Stable Vision-Language Alignment"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/SineProject_Machine_Unlearning_for_Stable_Vision_Language_Alignment.pdf
project_link: null
code_link: null
aliases:
- SineProject
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/representation_self_supervised_transfer
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: "对投影权重施加正弦变换的有界参数扰动（冻结预训练权重 W，仅优化 ΔW 并通过 W + sin(ΔW) 约束于 [-1, 1]），稳定投影网络的雅可比谱，从而避免对齐破坏。"
primary_logic: 通过正弦变换的固有谱正则化效应，将投影层参数更新限制在紧致范围内，显著降低雅可比条件数，维持视觉与语言嵌入间的几何一致性，在彻底遗忘目标知识的同时大幅度减少不当拒绝。
claims:
- 遗忘过程中投影层雅可比条件数上升3-4个数量级，是视觉-语言对齐漂移的直接原因。
- "SINEPROJECT 将投影网络条件数维持于 <10^3，比 SafeEraser 低 3-4 个数量级，同时模态整合率（MIR）收敛在最优区间 [2.5, 3.0]。"
- 在 SafeEraser 基准上，SINEPROJECT 在 LLaVA-7B 上 SARR 降低 15%（30.3% → 25.8%），LLaVA-13B 上降低 8%（27.3% → 25.1%），且保持 100% 的拒绝率。
- SafeEraser (LLaVA-7B) 上 SARR (%) = 25.8
---

# SineProject: Machine Unlearning for Stable Vision-Language Alignment

> [!tip] 核心洞察
> 通过正弦变换的固有谱正则化效应，将投影层参数更新限制在紧致范围内，显著降低雅可比条件数，维持视觉与语言嵌入间的几何一致性，在彻底遗忘目标知识的同时大幅度减少不当拒绝。

| 字段 | 内容 |
|------|------|
| 中文题名 | SineProject: 面向稳定视觉-语言对齐的机器遗忘方法 |
| 英文题名 | SineProject: Machine Unlearning for Stable Vision-Language Alignment |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2511.18444) |
| Topic | #topic/vision_multimodal_applications #topic/representation_self_supervised_transfer #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | SINEPROJECT |
| Dataset | SafeEraser, MLLMU-Bench, Geometric Stability |

> [!tip] 效果简介
> - SafeEraser (LLaVA-7B) 上，SARR (%) 25.8 vs 30.3 (SafeEraser PO+PD) (-15% （相对降低）)；ROUGE 65.8 vs 65.4 (SafeEraser PO+PD) (+0.4)。
> - SafeEraser (LLaVA-13B) 上，SARR (%) 25.1 vs 27.3 (SafeEraser PO+PD) (-8% （相对降低）)。
> - MLLMU-Bench (5% 删除率, LLaVA-7B) 上，Forget Cls (↓) 43.28 vs 45.61 (NPO) (-2.33)。

## 概要

### 问题：视觉-语言对齐漂移是机器遗忘的隐性瓶颈

在多模态大语言模型（MLLM）的安全遗忘任务中，一个被忽视但关键的瓶颈是**投影网络的雅可比条件数急剧恶化**。当模型试图遗忘特定危险知识时，投影层（将视觉特征映射到语言嵌入空间的两层 MLP）的雅可比矩阵条件数会上升 **3–4 个数量级**，导致优化过程数值不稳定，跨模态嵌入发生系统性漂移。这种漂移直接破坏了视觉与语言之间的几何对齐关系——原本匹配的图像-文本对在嵌入空间中的余弦相似度显著降低，模型对无害查询产生大量不当拒绝（过遗忘），严重损害了模型的通用效用。

### 核心方法：正弦投影器（SINEPROJECT）

SINEPROJECT 提出了一种简洁而有效的几何稳定策略：**冻结预训练的投影权重 W，仅优化增量参数 ΔW，并通过正弦变换 W + sin(ΔW) 将扰动约束在 [-1, 1] 的紧致范围内**。这一设计的核心洞察在于正弦函数的固有谱正则化效应——通过将参数更新限制在有界区间，显著降低投影层的雅可比条件数（从 >10⁶ 降至 <10³），从而在遗忘过程中维持视觉与语言嵌入间的几何一致性，避免对齐退化。

### 主要发现与结果

在 SafeEraser 和 MLLMU-Bench 两个主流多模态遗忘基准上，SINEPROJECT 取得了一致的改进：

- **不当拒绝大幅减少**：在 LLaVA-7B 上，安全不当拒绝率（SARR）从 30.3% 降至 25.8%（相对降低 15%）；在 LLaVA-13B 上从 27.3% 降至 25.1%（相对降低 8%），同时保持 100% 的目标遗忘拒绝率。
- **几何稳定性显著提升**：投影层雅可比条件数维持在 <10³，比当前最优方法 SafeEraser 低 3–4 个数量级；模态整合率（MIR）收敛于最优区间 [2.5, 3.0]。
- **方法无关性**：正弦投影器对损失函数不敏感，在梯度上升、KL 散度、偏好优化三种遗忘目标下均一致降低 SARR 0.8–4.5%。
- **持续遗忘韧性**：在多轮连续遗忘场景中，SINEPROJECT 将可行的遗忘轮次扩展约一倍（5 轮 vs. NPO 的 2–3 轮），累积效用损失仅为 6.9%（NPO 为 12.2%）。

### 方法谱系与知识库定位

SINEPROJECT 属于**参数高效微调 + 几何正则化**的技术路线，与以下工作形成对比：

| 方法 | 核心策略 | 局限性 |
|------|----------|--------|
| SafeEraser (PO+PD) | 偏好优化 + 提示解耦 | 投影层条件数失控，对齐退化 |
| GA/KL/GD + PD | 梯度上升/散度/下降 + 提示解耦 | 缺乏几何约束，过遗忘严重 |
| NPO | 隐私遗忘优化 | 高删除率下性能骤降，多轮遗忘知识复活 |
| 显式正则化（谱范数、权重裁剪、LoRA） | 直接约束权重范数或秩 | 无法有效控制雅可比条件数，SARR 达 34.1% |
| 其他有界函数（tanh、sigmoid） | 替代有界变换 | 谱正则化效果弱于正弦，条件数高 2 个数量级 |

SINEPROJECT 的关键创新在于**将正弦变换引入投影器参数化，利用其固有谱特性实现隐式正则化**，而非依赖显式约束。该方法在 LLaVA 架构的 MLP 和注意力投影器上均验证有效，计算开销低于 1%，但尚未在 Flamingo 等深度交叉注意融合模型上实验。

### 局限与开放问题

尽管 SINEPROJECT 显著缓解了过遗忘问题，仍存在若干局限：当遗忘比例超过 25% 时，遗忘质量与保留性能仍会下降；正弦投影器无法解决深度纠缠的语义概念解耦问题（如遗忘一个人物时，其关联作品的知识也可能受损）；在约 24% 的双方均拒绝的案例中，模型仍不当拒绝良性查询。开放问题包括：如何将几何稳定策略与认证防御机制结合以获得形式化遗忘保证，如何扩展到深度融合架构，以及如何在持续遗忘场景中进一步延长可行遗忘窗口。

### 多模态大语言模型的安全遗忘需求

多模态大语言模型（MLLM）通过视觉编码器、投影网络和语言模型主干的级联架构，将视觉感知与语言理解深度融合。然而，这种强大的多模态能力也带来了显著的安全隐患：模型可能记住并复现有害、隐私敏感或受版权保护的多模态内容。传统的安全对齐方法（如 RLHF）虽能在训练阶段抑制部分有害输出，但无法应对部署后新发现的安全漏洞，而全量重训的成本过高。机器遗忘（machine unlearning）作为一种事后修复机制，旨在从已训练模型中定向擦除特定知识，同时保留模型在其他任务上的通用能力，成为解决这一问题的关键路径。

### 视觉-语言对齐退化：被忽视的核心瓶颈

在多模态遗忘的现有研究中，**SafeEraser** 等方法通过偏好优化（PO）结合提示解耦（PD）取得了当前最优的遗忘质量。然而，这些方法在追求彻底擦除目标知识的过程中，普遍遭遇一个严重但未被系统诊断的问题：**遗忘后的模型对无害查询产生过度拒绝（over-forgetting）**。在 SafeEraser 基准上，即使是最强的 SafeEraser (PO+PD) 方法，其安全拒绝率（SARR）仍高达 30.3%（LLaVA-7B），意味着近三分之一的良性请求被错误拒绝。

本文首次揭示了这一现象的深层机制：**投影网络的雅可比条件数在遗忘过程中急剧增大 3–4 个数量级**。投影网络（通常为二层 MLP）负责将视觉特征映射至语言嵌入空间，是视觉-语言对齐的几何枢纽。当雅可比矩阵的最大奇异值与最小奇异值之比（条件数）从正常水平飙升至 $>10^6$ 时，投影映射变得极度病态，导致跨模态嵌入的几何一致性被破坏——即视觉-语言对齐退化。这种退化使得模型无法正确判断查询的语义安全性，从而对无害输入产生过度拒绝。

### 现有方法的局限

现有缓解策略存在根本性缺陷：
- **直接正则化**（谱范数约束、权重裁剪）缺乏对雅可比谱动态的精细控制，无法有效抑制条件数的指数级增长。
- **低秩适配**（LoRA）虽限制了参数更新规模，但未从几何角度约束投影映射的条件数，仍会出现显著的谱漂移。
- **有界激活函数**（tanh、sigmoid）可限制权重范围，但其梯度饱和特性会阻碍遗忘优化过程，导致遗忘质量下降。

这些方法均未能针对投影网络的条件数恶化这一根本原因进行干预，因此无法在遗忘质量与对齐稳定性之间取得有效平衡。

### 本文动机：通过谱正则化实现稳定遗忘

本文的核心动机源于一个关键洞察：**如果能将投影网络的参数更新约束在一个紧致且数值良态的范围内，就能从根本上抑制雅可比条件数的爆炸，从而在彻底遗忘目标知识的同时维持视觉-语言对齐的几何稳定性**。这需要一个既能严格限制权重扰动幅度、又不会阻碍梯度传播的参数化策略——正弦变换恰好满足这些要求：$\sin(\Delta W)$ 天然将输出限制在 $[-1, 1]$，且其导数 $\cos(\Delta W)$ 在零点附近接近 1，保证了优化初期的有效梯度流。

基于此，本文提出 **SINEPROJECT**，通过冻结预训练的投影权重 $W$，仅优化可训练的扰动参数 $\Delta W$，并以 $W + \sin(\Delta W)$ 的形式施加有界调制，从而在不引入额外计算开销的前提下，实现投影网络雅可比谱的稳定控制，大幅减少过度拒绝。

## 核心方法与创新机理

### 问题诊断：投影层雅可比条件数崩溃

在多模态大语言模型（MLLM）的机器遗忘过程中，现有方法面临一个此前未被揭示的根本性瓶颈：**投影网络（projector）的雅可比矩阵条件数在遗忘训练中急剧增大 3–4 个数量级**。这一数值不稳定直接导致跨模态嵌入空间的几何结构发生漂移——视觉特征与语言嵌入之间的余弦相似性矩阵从强对角结构退化为噪声分布——进而引发视觉-语言对齐的退化。对齐退化在行为层面的表现是模型对无害查询产生过度拒绝（over-forgetting），即 SafeEraser 基准中 SARR 指标接近 100% 的灾难性遗忘现象。

### 核心机制：正弦变换的谱正则化

SINEPROJECT 的核心创新在于**将投影层权重更新约束在一个紧致有界范围内，从而稳定遗忘过程中的雅可比谱**。具体而言，方法冻结预训练的投影 MLP 权重矩阵 $W_1$、$W_2$，引入可训练的扰动矩阵 $\Delta W_1$、$\Delta W_2$，并通过正弦变换构造实际前向传播权重：

$$\text{Sine-projector weights} = W + \sin(\Delta W)$$

完整的二层正弦投影器前向传播为：

$$(W_2 + \sin(\Delta W_2)) \phi((W_1 + \sin(\Delta W_1)) x + b_1) + b_2$$

这一设计的因果机制在于：正弦函数将 $\Delta W$ 的任意实值更新映射到 $[-1, 1]$ 区间，从而对投影权重的扰动施加硬边界。这并非简单的权重裁剪或范数正则化，而是通过正弦变换的**固有谱正则化效应**——在数学上，有界权重直接约束了雅可比矩阵的最大奇异值 $\sigma_{\max}$ 的增长，同时保持最小奇异值 $\sigma_{\min}$ 不坍塌，从而将条件数 $\frac{\sigma_{\max}}{\sigma_{\min}}$ 维持在稳定范围内。

### 与现有方法的 changed slots 对比

| 方法组件 | 基线做法（SafeEraser 等） | SINEPROJECT 做法 | 机制差异 |
|---------|------------------------|-----------------|---------|
| **投影权重参数化** | 直接优化投影 MLP 的权重矩阵 $W_1$、$W_2$ | 冻结预训练 $W_1$、$W_2$；新增可训练 $\Delta W_1$、$\Delta W_2$，通过 $W + \sin(\Delta W)$ 施加有界扰动 | 将无约束优化转化为有界扰动学习，从根本上防止权重幅值发散 |
| **雅可比稳定性** | 条件数随遗忘轮次飙升至 $>10^6$ | 条件数始终控制在 $<10^3$，改善 3–4 个数量级 | 谱正则化是正弦变换的数学后果，无需额外损失项或超参数 |
| **模态对齐保持** | 余弦相似性矩阵退化为弱对角结构 | 维持强对角结构，模态整合率（MIR）收敛于最优区间 $[2.5, 3.0]$ | 几何一致性通过权重有界性自然保持，而非通过显式对齐损失 |

### 消融验证的关键发现

消融实验（Table 6）证实，正弦调制 $\sin(\Delta W)$ 在 SARR 和雅可比条件数上**显著优于**其他正则化策略和有界函数：
- **谱范数正则化**、**权重裁剪**、**LoRA** 等显式正则化方法均无法达到同等稳定性（SARR 34.1% vs 25.8%，条件数 $1.15\times10^5$ vs $5.40\times10^2$，$p<0.05$）
- **tanh** 和 **sigmoid** 等其他有界函数的效果也明显弱于正弦变换，表明正弦函数的周期性和梯度特性对谱调节具有独特优势

此外，正弦投影器对损失函数**不敏感**（Table 8）：在 GD、KL、PO 三种遗忘目标下均一致降低 SARR 0.8–4.5%，同时保持拒绝率 >99%。这表明几何稳定机制是独立于具体优化目标的通用正则化策略。

### 创新边界

SINEPROJECT 的创新聚焦于投影层的参数化方式，**不改变遗忘损失函数的形式**、**不修改视觉编码器或语言模型主干的架构**、**不引入额外的对齐约束或蒸馏损失**。其有效性源于对遗忘过程中数值不稳定根源的精确干预——通过正弦变换的谱正则化效应，在参数层面而非损失层面解决了对齐漂移问题。

SINEPROJECT 的整体框架围绕一个核心发现构建：在多模态大语言模型（MLLM）的机器遗忘过程中，视觉-语言投影网络的雅可比矩阵条件数会急剧增大 3–4 个数量级，导致跨模态嵌入发生显著漂移，进而引发灾难性的“过遗忘”——模型对无害查询产生过度拒绝。针对这一瓶颈，SINEPROJECT 提出了一种轻量级的几何稳定策略，在不改变原有 MLLM 架构主干的前提下，仅对投影层施加正弦变换的有界参数扰动，从而稳定雅可比谱，维持视觉与语言嵌入空间的几何一致性。

### 模块构成与数据流

框架由三个核心模块组成，形成“视觉编码 → 投影映射 → 语言生成”的级联管线：

1. **视觉编码器（冻结）**：采用 CLIP ViT-L/14 作为视觉特征提取器。在整个遗忘过程中，该模块保持冻结，不参与任何参数更新，以确保视觉表征空间的稳定性不受遗忘目标的干扰。

2. **正弦投影器（可训练）**：这是 SINEPROJECT 的核心创新所在。投影器实现为一个二层 MLP，标准形式为：
   $$F(x) = W_2 \phi(W_1 x + b_1) + b_2$$
   其中 $W_1, W_2$ 为权重矩阵，$\phi$ 为非线性激活函数。该模块负责将视觉编码器输出的视觉特征映射至语言模型的嵌入空间。在 SINEPROJECT 中，预训练的 $W_1, W_2$ 被冻结，新引入可训练的扰动矩阵 $\Delta W_1, \Delta W_2$，并通过正弦变换约束其有效范围：
   $$\text{Sine-projector weights} = W + \sin(\Delta W)$$
   完整的二层正弦投影器前向传播为：
   $$(W_2 + \sin(\Delta W_2)) \phi((W_1 + \sin(\Delta W_1)) x + b_1) + b_2$$
   这一设计将权重扰动严格限制在 $[-1, 1]$ 的有界区间内，从根本上抑制了投影层雅可比条件数的发散。

3. **语言模型主干（LoRA 微调）**：使用 Vicuna-7B 或 Vicuna-13B 作为文本生成主干。遗忘训练期间，仅通过秩为 32 的 LoRA 适配器进行低秩微调，视觉编码器和正弦投影器中的冻结权重均保持不变。

### 遗忘优化流程

机器遗忘的目标函数形式为：
$$\theta^* = \arg\min_\theta \mathcal{L}_{\mathrm{forget}}(\theta; \mathcal{D}_f) + \lambda \mathcal{L}_{\mathrm{retain}}(\theta; \mathcal{D}_r)$$
其中 $\mathcal{D}_f$ 为待遗忘数据集，$\mathcal{D}_r$ 为需保留的数据集，$\lambda$ 平衡遗忘质量与模型效用。在训练过程中，梯度仅流向 $\Delta W_1, \Delta W_2$ 和 LoRA 适配器，而冻结的预训练权重 $W_1, W_2$ 以及视觉编码器完全不参与更新。

### 关键机制：几何稳定性的因果链路

框架有效性的因果链路可概括为：正弦变换 → 雅可比条件数受控（$<10^3$）→ 模态整合率（MIR）收敛于最优区间 $[2.5, 3.0]$ → 视觉-语言对齐得以保持 → 过遗忘（SARR）显著降低。消融实验证实，正弦调制（$\sin(\Delta W)$）在雅可比条件数控制上优于谱范数正则化、权重裁剪、LoRA 等替代策略，且优于 tanh、sigmoid 等其他有界函数，实现了最低的条件数（$5.40 \times 10^2$）和最优的 SARR（25.8%）。同时调制投影器两层（$W_1$ 和 $W_2$）是获得最优稳定性的必要条件——仅调制 $W_2$ 会导致 SARR 上升至 26.5%。

### 与提示解耦的协同

框架还集成了提示解耦策略，将纯文本样本与多模态样本分别处理，以不同的损失目标进行优化。消融实验表明，提示解耦是避免灾难性过遗忘的关键组件：不使用提示解耦时，所有遗忘方法的 SARR 均接近 100%；引入提示解耦后 SARR 降至约 30%，再结合 SINEPROJECT 进一步降至 25.8%。这一协同效应说明，几何稳定与损失解耦分别从参数空间和优化目标两个维度共同抑制了过遗忘行为。

### 损失函数无关性

值得注意的设计特性是正弦投影器对损失函数选择的鲁棒性。在梯度下降（GD）、KL 散度最小化（KL）和偏好优化（PO）三种不同的遗忘目标下，SINEPROJECT 均一致地将 SARR 降低 0.8–4.5 个百分点，同时保持拒绝率（RR）超过 99%。这表明几何稳定机制与具体的遗忘损失解耦，可作为通用插件嵌入各类机器遗忘范式。

### 投影网络架构

多模态大语言模型（MLLM）中，视觉-语言对齐的核心组件是**投影网络**（Projector），其功能是将视觉编码器（如 CLIP ViT-L/14）提取的视觉特征映射至语言模型的嵌入空间。遵循 LLaVA 的设计范式，投影器实现为一个两层多层感知机（MLP）：

$$F(x) = W_2 \phi(W_1 x + b_1) + b_2 \quad \text{(Eq. 1)}$$

其中，$x$ 为视觉编码器输出的视觉特征，$W_1, W_2$ 为投影层的权重矩阵，$b_1, b_2$ 为偏置项，$\phi(\cdot)$ 为激活函数（如 GELU）。

### 机器遗忘的形式化目标

机器遗忘的目标是在消除模型对特定遗忘数据 $\mathcal{D}_f$ 的知识的同时，保持对保留数据 $\mathcal{D}_r$ 的效用。该优化问题可形式化为：

$$\theta^* = \arg\min_\theta \mathcal{L}_{\mathrm{forget}}(\theta; \mathcal{D}_f) + \lambda \mathcal{L}_{\mathrm{retain}}(\theta; \mathcal{D}_r) \quad \text{(Eq. 2)}$$

其中，$\mathcal{L}_{\mathrm{forget}}$ 为遗忘损失（如梯度上升、偏好优化等），$\mathcal{L}_{\mathrm{retain}}$ 为保留损失，$\lambda$ 为平衡超参数。

### 核心瓶颈：雅可比条件数的爆炸

在遗忘过程中，投影网络的雅可比矩阵条件数急剧增大 **3–4 个数量级**（Section 1），这是导致视觉-语言对齐漂移的直接原因。雅可比条件数定义为矩阵最大奇异值与最小奇异值的比值：

$$\frac{\sigma_{\max}(A)}{\sigma_{\min}(A)} \quad \text{(Section 3.1)}$$

条件数的爆炸意味着投影映射对输入扰动极度敏感，导致视觉嵌入在语言空间中的几何位置发生不可控偏移，进而引发模型对无害查询的**过度拒绝**（SARR 接近 100%）。

### SINEPROJECT 核心机制：正弦参数化

SINEPROJECT 的核心创新在于对投影权重施加**正弦变换的有界参数扰动**，以稳定雅可比谱。具体而言：

1. **冻结预训练权重** $W_1, W_2$，保持原始对齐知识。
2. **引入可训练的扰动参数** $\Delta W_1, \Delta W_2$。
3. **通过正弦函数约束扰动范围**，使有效权重始终处于紧致区间内：

$$\text{Sine-projector weights} = W + \sin(\Delta W) \quad \text{(Eq. 9)}$$

完整的二层正弦投影器前向传播为：

$$(W_2 + \sin(\Delta W_2)) \phi((W_1 + \sin(\Delta W_1)) x + b_1) + b_2 \quad \text{(Eq. 10)}$$

### 正弦变换的谱正则化效应

正弦函数 $\sin(\cdot) \in [-1, 1]$ 的固有有界性赋予了投影层天然的谱正则化效果。理论分析（Theorem C.2）预测，正弦调制通过约束 $\sigma_{\max}$ 的增长并维持 $\sigma_{\min}$ 的稳定，从根本上防止了条件数的恶化。实验证实：

- SINEPROJECT 将第二投影层的雅可比条件数维持在 **$<10^3$**，而基线方法 SafeEraser 超过 **$10^6$**，改善达 3–4 个数量级（Figure 2b）。
- 同时，模态整合率（MIR）收敛于最优区间 **[2.5, 3.0]**（约 2.7），较最强基线降低 1.7 倍（Section 4.3）。

### 训练配置

在实际训练中，视觉编码器完全冻结，仅优化正弦投影器的扰动参数 $\Delta W_1, \Delta W_2$ 以及语言模型主干的 LoRA 适配器（秩 32）。这一设计确保了遗忘过程的计算开销低于 1%（Table 9），同时保持了对齐的几何稳定性。

## 实验与关键发现

### 核心发现：SINEPROJECT 在遗忘-保留权衡上的突破

SINEPROJECT 在 SafeEraser 和 MLLMU-Bench 两大基准上均实现了当前最优的遗忘-保留平衡。其核心优势在于：在保持 100% 目标拒绝率（RR）的同时，将无害查询的不当拒绝率（SARR）大幅压低。

**SafeEraser 基准**（Table 1）上，以当前最强的 **SafeEraser (PO+PD)** 为直接对比对象：
- **LLaVA-7B**：SARR 从 30.3% 降至 **25.8%**（相对降低 15%），ROUGE 保持 65.8（vs. 65.4）；
- **LLaVA-13B**：SARR 从 27.3% 降至 **25.1%**（相对降低 8%），同时保持 100% RR。

**MLLMU-Bench 基准**（Table 2）上，在 5% 删除率下，SINEPROJECT 的 Forget Cls 降至 **43.28**，优于 NPO 的 45.61；综合平均分 62.1 为所有方法最高。在 10% 和 15% 删除率下，SINEPROJECT 同样保持一致的遗忘-保留优势。

### 几何稳定性：从条件数崩溃到谱正则化

SINEPROJECT 性能提升的根本原因在于其对投影网络几何结构的稳定化作用。

**关键证据**（Figure 2b）：在遗忘过程中，SafeEraser 的第二投影层雅可比条件数飙升至 **>10⁶** 量级，而 SINEPROJECT 将该条件数稳定控制在 **<10³**，改善幅度达 **3–4 个数量级**。这一条件数崩溃正是视觉-语言对齐漂移的直接数学表征——当投影矩阵变得病态时，微小的输入扰动即导致跨模态嵌入的大幅偏移，进而触发模型对无害查询的过度拒绝。

**模态整合率（MIR）** 的收敛行为（Figure 2）进一步验证了这一机制：SINEPROJECT 的 MIR 收敛至约 **2.7**，恰好落在最优区间 [2.5, 3.0] 内，且比最强基线低 1.7 倍。这表明正弦调制维持了视觉与语言嵌入间的适度耦合强度，既不过度融合（导致遗忘失败），也不过度解耦（导致对齐崩溃）。

**谱动态分析**（Figure 3）揭示，SINEPROJECT 同时约束了最大奇异值（σ_max）的膨胀和最小奇异值（σ_min）的坍缩，从谱的两端共同维持了条件数的稳定，与理论分析（Theorem C.2）的预测一致。

### 消融实验：设计选择的因果验证

#### 1. 提示解耦（PD）是防止灾难性过遗忘的必要条件

Table 4 的消融结果给出了明确的因果链：
- **无 PD**：所有遗忘方法（GD、KL、PO）的 SARR 均接近 **100%**，即模型几乎拒绝所有无害查询；
- **引入 PD**：SARR 骤降至 28–30% 区间；
- **PD + SINEPROJECT**：进一步降至 **25.8%**。

这确立了“提示解耦处理跨模态遗忘信号 → 正弦投影器稳定几何结构”的两阶段防御体系。

#### 2. 正弦调制优于所有替代正则化策略

Table 6 对比了多种参数约束方案（均使用 PO+PD，LLaVA-7B）：
- **谱范数正则化**：SARR 34.1%，条件数 1.15×10⁵；
- **权重裁剪**：SARR 29.3%；
- **LoRA 低秩适配**：SARR 28.7%；
- **tanh 有界函数**：SARR 27.1%；
- **sigmoid 有界函数**：SARR 26.8%；
- **sin(ΔW)（SINEPROJECT）**：SARR **25.8%**，条件数 **5.40×10²**（p<0.05）。

![[assets/figures/papers/paper_list_l783_https_arxiv_org_abs_2511_18444/figures/009_Table_6.jpg]]
*Table 6: Ablation on regularization strategies and bounded modulation. Results of SafeEraser using LLaVA-7B with PO+PD. SINEPRO-JECT outperformed explicit regularization (spectral norm, clipping, LoRA), and alternative bounded functions. Modulating biases provides no benefit, confirming weight matrices dominate geometric instability*

正弦变换的优势不仅在于有界性，更在于其固有的谱正则化效应——sin 函数在零点附近的线性区域允许有效学习，而在边界处的饱和特性自然抑制了参数的过度增长。

#### 3. 两层联合调制是必要的

Table 7 显示，仅调制第二投影层（W2）时 SARR 为 26.5%，而同时调制两层（W1 + W2）达到最优的 **25.8%**。这表明第一投影层的条件数稳定同样对整体对齐有贡献，尽管其退化程度（Figure 2a）较第二层温和。

![[assets/figures/papers/paper_list_l783_https_arxiv_org_abs_2511_18444/figures/010_Table_7.jpg]]
*Table 7: Ablation on layer-specific application of sinusoidal modulation within the two-layer projector. Results on SafeEraser using LLaVA-7B with PO+PD. While modulating*

#### 4. 损失函数无关性

Table 8 验证了 SINEPROJECT 的通用性：在 GD、KL、PO 三种遗忘目标下，正弦投影器均一致降低 SARR **0.8–4.5%**，同时保持 RR >99%。这说明几何稳定是一种与优化目标正交的正则化机制。

![[assets/figures/papers/paper_list_l783_https_arxiv_org_abs_2511_18444/figures/011_Table_8.jpg]]
*Table 8: Ablation on loss function interaction with SINEPROJECT. Results on SafeEraser using LLaVA-7B across three base unlearning objectives (GD, KL, PO) with and without Prompt Decoupling. SINEPROJECT consistently improved geometric stability across all configurations, demonstrating loss-agnostic benefits. The combination SINEPROJECT(PO+PD) achieved optimal performance, used as our primary configuration throughout the paper*

### 失败模式与局限性

尽管 SINEPROJECT 显著改善了遗忘稳定性，论文识别了以下边界条件：

1. **高删除率退化**（Table 14）：当遗忘比例超过 25% 时，即使几何结构稳定，遗忘质量与保留性能仍出现可观测的下降，受限于模型容量本身。

2. **语义纠缠无法解耦**：正弦投影器解决的是几何稳定性问题，而非语义解耦问题。遗忘某个人物时，其关联作品的知识可能连带受损——这是训练数据中的深度语义纠缠所致，非参数正则化所能解决。

3. **残余不当拒绝**：在人类评估中（Figure 7–8），24% 的双方均拒绝案例中，SINEPROJECT 仍错误地拒绝了良性查询。几何稳定无法完全补偿有偏的训练信号。

![[assets/figures/papers/paper_list_l783_https_arxiv_org_abs_2511_18444/figures/017_Figure_7.jpg]]
*Figure 7: Human evaluation examples (Part 1/3) featuring real-world images from the SafeEraser benchmark. ✗ denotes inappropriate refusal (over-forgetting), while ✓ signifies correct behavior. Examples 1 and 2 illustrate SafeEraser’s keyword-triggered refusals on benign queries, wherein SINEPROJECT maintains semantic discrimination. Example 3 demonstrates that both methods preserve safety on genuinely harmful queries*

4. **架构覆盖有限**：当前验证限于 LLaVA 架构的 MLP 和注意力投影器（Table 11），未在 Flamingo 等深度交叉注意融合模型上实验。

![[assets/figures/papers/paper_list_l783_https_arxiv_org_abs_2511_18444/figures/016_Table_11.jpg]]
*Table 11: Validation of Multi-Architecture on SafeEraser (PO+PD). The SINEPROJECT consistently enhances geometric stability across both MLP- and attention-based projectors. While attention architectures exhibit a higher baseline SARR, they also demonstrate proportional improvements*

### 计算效率与可扩展性

Table 9 显示，SINEPROJECT 引入的计算开销低于 1%（SafeEraser，LLaVA-7B，4× A6000 GPU），因为正弦变换仅作用于投影层的可训练参数 ΔW，不改变前向传播的计算图结构。Table 13 的可扩展性分析进一步验证了该方法在不同视觉编码器、语言模型规模和投影器深度下的鲁棒性。

![[assets/figures/papers/paper_list_l783_https_arxiv_org_abs_2511_18444/figures/020_Table_13.jpg]]
*Table 13: Comprehensive scalability analysis across vision encoders, language models, and projector architectures on SafeEraser (PO+PD). SINEPROJECT maintains consistent benefits (14-19% SARR reduction, 3-4 orders of magnitude better conditioning) across all configurations. Gray rows indicate baseline LLaVA-7B+ViT-L+2-layer setup*

## 定位与知识库关联

### 问题定位：多模态遗忘中的视觉-语言对齐退化

SINEPROJECT 针对的是多模态大语言模型（MLLM）机器遗忘中一个此前未被充分诊断的核心瓶颈：**投影网络的条件数崩溃导致跨模态对齐退化**。在标准遗忘流程中，投影层（通常为二层 MLP）的雅可比条件数会上升 3–4 个数量级，使得视觉特征到语言空间的映射变得数值不稳定，进而引发对无害查询的过度拒绝（SARR 接近 100%）。这一发现将 MLLM 遗忘的失败模式从“损失函数设计不当”重新定位为“几何结构破坏”，构成了该方法与现有工作的根本分野。

### 与现有遗忘范式的对比

当前多模态机器遗忘方法主要沿两条技术路线展开：

**损失函数设计路线**以 SafeEraser 系列为代表。其核心策略包括偏好优化（PO）、梯度上升（GA）、KL 散度最小化等遗忘目标，配合提示解耦（Prompt Decoupling, PD）将纯文本样本与多模态样本分别处理，以缓解跨模态干扰。SafeEraser (PO+PD) 在 LLaVA-7B 上实现了 30.3% 的 SARR，是此前的最优方法。然而，这些方法未对投影层的参数更新施加任何结构约束，导致条件数随遗忘轮次急剧恶化——SafeEraser 的第二投影层条件数超过 10⁶，成为过遗忘的直接诱因。

**隐私遗忘路线**以 MLLMU-Bench 上的 NPO 方法为代表，侧重于在隐私保护场景下擦除特定实体知识，但其评估体系主要关注遗忘质量与保留能力的权衡，未涉及对齐稳定性问题。

SINEPROJECT 的独特贡献在于**将遗忘稳定性问题从损失函数层面提升到参数几何层面**：它不改变遗忘目标本身（可兼容 GD、KL、PO 等多种损失），而是通过正弦变换对投影权重施加有界参数扰动，从根源上抑制条件数爆炸。这一设计哲学与上述两类方法正交——事实上，SINEPROJECT 与 PO+PD 结合后，在 SafeEraser 基准上将 SARR 进一步降低至 25.8%（7B）和 25.1%（13B），验证了“几何稳定 + 损失优化”的互补性。

### 技术谱系中的位置：谱正则化与有界参数化

从更广的技术谱系看，SINEPROJECT 的正弦调制策略可追溯至两类方法传统：

**谱正则化方法**（如谱范数正则化、权重裁剪、LoRA 低秩适配）试图通过显式约束权重矩阵的谱特性来提升训练稳定性。消融实验表明，这些方法在遗忘场景下效果有限：谱范数正则化仅将 SARR 降至 34.1%，权重裁剪为 32.8%，而 SINEPROJECT 的 sin(ΔW) 实现了 25.8% 的 SARR，且第二投影层的雅可比条件数仅为 5.40×10²（对比谱范数正则化的 1.15×10⁵，p<0.05）。这揭示了一个关键差异：显式正则化作用于权重范数，而正弦变换通过限制参数空间的有界性间接约束了雅可比谱，产生了更强的条件数抑制效果。

**有界激活函数方法**（如 tanh、sigmoid）同样将参数限制在紧致范围内，但消融显示其效果显著弱于正弦：tanh(ΔW) 和 sigmoid(ΔW) 均无法有效控制条件数，导致 SARR 分别高达 29.8% 和 31.2%。正弦函数的独特优势在于其梯度特性——在零点附近近似线性（利于优化），在远离零点时自然饱和（提供有界性），且导数 cos(ΔW) 在 [-1,1] 内保持正值，避免了梯度消失对训练的阻碍。

### 适用边界与架构依赖

SINEPROJECT 的适用性由以下边界条件界定：

1. **投影器架构依赖**：当前方法在 LLaVA 架构的 MLP 投影器和注意力投影器（Attention Projector）上均得到验证，但尚未在 Flamingo 等采用分层门控交叉注意力的深度融合架构上实验。正弦调制的有效性依赖于投影层作为视觉-语言之间的唯一（或主要）信息瓶颈——当存在多条并行的跨模态通路时，单一瓶颈的谱稳定可能不足以全局约束对齐漂移。

2. **遗忘比例上限**：实验表明，当遗忘比例超过 25% 时，即使几何稳定性得以维持，遗忘质量与保留性能仍会同步下降。这是因为正弦投影器无法解决深度语义纠缠问题——遗忘一个实体时，其关联概念（如遗忘某位人物时，其参演作品的知识）可能连带受损，这是参数化知识存储的结构性限制，而非优化稳定性问题。

3. **训练信号偏差**：在 24% 的双方均拒绝的案例中，SINEPROJECT 仍不当地拒绝了良性查询。这表明几何稳定可以防止条件数崩溃导致的“无差别拒绝”，但无法完全补偿遗忘训练信号本身引入的判别边界偏移。

### 局限性与开放问题

**已识别的核心局限**：

- **语义解耦缺失**：正弦投影器是纯几何层面的稳定策略，不具备语义解耦能力。当遗忘目标与保留知识在嵌入空间中深度纠缠时（如同一人物的不同属性、关联作品），方法无法实现精细化的选择性遗忘。Table 14 的失败模式分析证实了这一局限。
- **架构泛化未验证**：仅在 LLaVA 系列（Vicuna 主干 + MLP/注意力投影器）上验证，未覆盖 Qwen-VL、InternVL 等采用不同融合策略的架构，也未在 Flamingo 式深度交叉注意力模型上测试。
- **多轮遗忘退化**：Table 15 的多轮连续遗忘实验（5 轮 × 5% 删除率）显示，尽管 SINEPROJECT 延缓了退化速度，但累积效应仍不可避免，超过五轮后的可行遗忘窗口尚待扩展。
- **基准敏感性**：SafeEraser 基准存在提示敏感性，多提示评估协议尚未标准化，可能影响 SARR 等指标的跨方法可比性。

**值得追踪的开放方向**：

1. 如何将正弦投影器的几何稳定策略与认证遗忘机制（如差分隐私保证、形式化遗忘边界）结合，获得可证明的遗忘质量保证？
2. 在遗忘比例超过 25% 的高负载场景下，是否需要引入稀疏化、记忆编辑或模型扩展等补充策略来维持遗忘-保留平衡？
3. 能否将正弦调制推广到深度融合架构的交叉注意力层，通过约束注意力权重的谱特性来稳定多模态交互？
4. 是否可以通过设计新的遗忘损失函数或数据增强策略（如对比解耦、反事实样本生成），从训练信号层面减轻语义纠缠，与几何稳定形成双层防护？
5. 在持续遗忘场景中，能否引入弹性权重巩固（EWC）或渐进式网络扩展等持续学习策略，进一步延长可行遗忘窗口？

## 原文 PDF

![[paperPDFs/CVPR_2026/SineProject_Machine_Unlearning_for_Stable_Vision_Language_Alignment.pdf]]
