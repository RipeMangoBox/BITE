---
title: Towards Reasoning-Preserving Unlearning in Multimodal Large Language Models
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Towards_Reasoning_Preserving_Unlearning_in_Multimodal_Large_Language_Models.pdf
project_link: null
code_link: null
aliases:
- RM
- TRPUMLLM
tags:
- CVPR_2026
- topic/other_unclear
- topic/other_unclear/general
core_operator: 推理时通过激活引导，构建同时针对答案和思维链的遗忘方向，并将其正交投影到推理保留子空间之外，从而在遗忘过程中解耦敏感信息与通用推理。
primary_logic: 将遗忘方向构造为答案和推理轨迹的混合跨度对比信号，并在推理保留子空间的正交补空间中进行自适应强度引导，可在有效遗忘敏感信息的同时最大程度保护通用推理能力。
claims:
- 在LLaVA-1.5-7B上15%遗忘率下，R-MUSE将遗忘集分类准确率从Vanilla的51.87%降至21.80%，推理泄漏从79.50%降至39.20%，同时保留集准确率保持较高(45.85%)。
- 在Qwen-2.5-VL-7B上，R-MUSE实现深度遗忘（Fgt Acc 33.80% vs Vanilla 60.50%）而保留集效用几乎无损（Ret Acc 53.60% vs Vanilla 53.80%），显著优于所有基线。
- 消融实验显示，移除RRS后保留集分类准确率从54.1%骤降至34.0%，验证了正交投影保护机制的必要性。
- PCA可视化显示，R-MUSE引导的隐藏状态在遗忘集上发生显著的方向性偏移和拉伸，而在保留集上结构与原模型高度重叠，表明遗忘被定向而不破坏保留能力。
---

# Towards Reasoning-Preserving Unlearning in Multimodal Large Language Models

> [!tip] 核心洞察
> 将遗忘方向构造为答案和推理轨迹的混合跨度对比信号，并在推理保留子空间的正交补空间中进行自适应强度引导，可在有效遗忘敏感信息的同时最大程度保护通用推理能力。

| 字段 | 内容 |
|------|------|
| 中文题名 | 推理保留的多模态大语言模型遗忘方法 |
| 英文题名 | Towards Reasoning-Preserving Unlearning in Multimodal Large Language Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.17911) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | R-MUSE |
| Dataset | RMLLMU-Bench |

> [!tip] 效果简介
> - RMLLMU-Bench (LLaVA-1.5-7B, 15% Forget Rate) 上，Classification Accuracy Fgt↓ 21.80 vs 51.87 (Vanilla) (-30.07)；Reasoning Leakage Fgt↓ 39.20 vs 79.50 (Vanilla) (-40.30)。
> - RMLLMU-Bench (Qwen-2.5-VL-7B, 15% Forget Rate) 上，Classification Accuracy Fgt↓ 33.80 vs 60.50 (Vanilla) (-26.70)；Classification Accuracy Ret↑ 53.60 vs 53.80 (Vanilla) (-0.20)。

## 概要

**核心问题**：现有多模态大语言模型（MLLM）与推理大语言模型（LRM）的遗忘方法存在根本性困境——若仅遗忘最终答案，思维链中的中间推理步骤仍会泄漏敏感信息；若强行抑制推理链，则导致模型推理能力崩溃，输出不连贯的重复内容。现有方法无法同时实现深度遗忘与推理保留。

**核心方法**：本文提出 **R-MUSE**（Reasoning-Preserving Unlearning via Activation Steering），一个无需训练的推理时激活引导框架。其核心思路是：在推理阶段，通过对比“拒绝回答”与“原始回忆”的生成轨迹，构建同时覆盖答案跨度和思维链跨度的混合遗忘方向；再将该方向正交投影到推理保留子空间（Reasoning Retain Subspace, RRS）的正交补空间中，从而在遗忘敏感信息的同时显式保护通用推理能力。引导强度通过基于最优运输距离的自适应校准（Adaptive Calibration Steering, ACS）动态确定，无需手动调节超参数。

**方法定位**：R-MUSE 属于推理时干预方法，区别于基于梯度更新或微调的参数修改范式（如 GA、NPO、MMUnlearner、MANU 等）。其关键创新在于将遗忘目标从单一答案扩展至推理轨迹，并通过正交投影机制解耦遗忘与推理保护。

**主要结果**：在 RMLLMU-Bench 基准上，R-MUSE 在 LLaVA-1.5-7B 和 Qwen-2.5-VL-7B 两个骨干网络上均显著优于所有基线。以 15% 遗忘率为例，R-MUSE 在 LLaVA-1.5-7B 上将遗忘集分类准确率从 Vanilla 模型的 51.87% 降至 21.80%，推理泄漏从 79.50% 降至 39.20%，同时保留集准确率维持在 45.85%；在 Qwen-2.5-VL-7B 上实现遗忘集准确率 33.80%（Vanilla 为 60.50%），而保留集准确率几乎无损（53.60% vs 53.80%）。消融实验证实，移除 RRS 后保留集准确率从 54.1% 骤降至 34.0%，验证了正交投影保护机制的核心作用。PCA 可视化进一步表明，R-MUSE 引导的隐藏状态在遗忘集上发生显著方向性偏移，而在保留集上与原始模型高度重叠，实现了定向遗忘而不破坏保留能力。

### 推理型多模态大语言模型的遗忘困境

多模态大语言模型（MLLMs）在视觉问答、跨模态推理等任务中展现出强大能力，但其训练数据中不可避免地包含敏感或受版权保护的信息。当法律法规（如GDPR的“被遗忘权”）要求删除特定知识时，模型需要具备“遗忘”能力——即在不重新训练的前提下，使模型对特定查询不再生成包含目标信息的回答。

现有的MLLM遗忘方法主要沿两条技术路线展开：一类方法通过梯度上升（GA）、负偏好优化（NPO）、KL散度最小化等参数微调策略，直接修改模型权重以抑制对遗忘目标的记忆；另一类方法则探索模态感知的神经元剪枝（如**MANU**）或多模态联合遗忘（如**MMUnlearner**）。然而，这些方法面临一个共同的核心瓶颈：**它们无法同时抑制推理链中的信息泄漏和保持总体推理能力**。

### 推理泄漏：被忽视的关键挑战

Figure 1 清晰地揭示了这一困境。当遗忘方法仅针对最终答案进行干预时，模型虽然可能输出“拒绝回答”或错误答案，但其内部的思维链（Chain-of-Thought）仍然完整地重构了被遗忘的事实——这种现象被称为**推理泄漏（Reasoning Leakage）**。例如，模型在被问及某位被遗忘人物的生平时，可能最终回答“我不知道”，但中间推理步骤却明确写出了该人物的出生年份和主要成就。

反之，如果遗忘方法试图抑制推理过程以避免泄漏，又容易导致模型陷入语无伦次、重复循环的推理崩溃，严重损害其在保留任务上的通用推理能力。这种“遗忘-推理”的二律背反，构成了推理型多模态大语言模型遗忘的核心挑战。

### 现有方法的系统性缺口

从方法学角度审视，现有遗忘范式存在三个结构性缺陷：

1. **遗忘目标单一化**：大多数方法仅针对最终答案令牌进行遗忘信号设计，忽略了中间推理步骤同样承载敏感信息。这导致即使答案被改写，推理链仍可作为信息泄漏的“后门”。

2. **推理保护缺失**：现有方法或完全无推理保护机制，或仅通过损失函数中的正则化项进行隐式平衡（如**R²MU**），缺乏对通用推理能力的显式、结构性保护。在遗忘压力下，模型的推理能力往往成为“附带损伤”。

3. **训练依赖与灵活性不足**：基于微调的方法需要针对每个遗忘请求重新训练，计算成本高昂，且超参数（如遗忘强度系数λ）需手动调节，难以适应动态变化的遗忘需求。

### 本文动机与核心思路

针对上述缺口，本文提出**R-MUSE**（Reasoning-Preserving Multimodal Unlearning via Activation Steering），一个无需训练、在推理时通过激活引导实现遗忘的框架。其核心洞察在于：**将遗忘方向构造为答案和推理轨迹的混合跨度对比信号，并在推理保留子空间的正交补空间中进行自适应强度引导，可在有效遗忘敏感信息的同时最大程度保护通用推理能力**。

具体而言，R-MUSE通过三个关键设计实现这一目标：（1）构建覆盖答案和思维链的混合跨度遗忘方向，从根本上抑制推理泄漏；（2）学习推理保留子空间（RRS），并将遗忘引导投影到其正交补空间，实现遗忘与推理的结构化解耦；（3）引入基于最优运输距离的自适应校准机制，无需手动超参数即可动态确定引导强度。

## 核心方法与创新机理

R-MUSE 的核心创新在于将多模态大语言模型（MLLM）的遗忘问题从传统的参数修改范式迁移到**无需训练的推理时激活引导**框架，并通过三个协同设计的机制解决了一个此前被忽视的关键瓶颈：**如何在遗忘敏感信息的同时，既不泄漏推理链中的知识，又不损害模型的通用推理能力**。

### 从参数修改到推理时激活引导

现有遗忘方法（如 GA、KL_Min、NPO、MMUnlearner、MANU）均依赖对模型参数的微调或梯度更新来实现遗忘。这种范式面临两难困境：针对最终答案的遗忘无法阻断推理链中的信息泄漏，而针对推理链的遗忘则容易导致推理能力的全面崩溃（参见 Figure 1）。R-MUSE 通过**推理时激活引导**彻底绕开了这一困境——模型参数保持不变，仅在推理过程中对特定层的隐藏状态施加定向干预。这一设计不仅避免了昂贵的重训练成本，更关键的是，它使得遗忘行为可以在推理时根据查询内容动态决策，而非被固化为模型权重的全局性改变。

### 混合跨度遗忘方向：同时覆盖答案与推理链

传统遗忘方法通常仅以最终答案为目标，忽略了多模态推理模型中思维链（chain-of-thought）所承载的大量敏感信息。R-MUSE 构建遗忘方向的方式发生了根本性变化：它不再依赖单一令牌的表示差异，而是通过**跨度池化**（span pooling）分别提取答案跨度 $S_{\mathrm{ans}}$ 和思维链跨度 $S_{\mathrm{cot}}$ 的隐藏状态，对比“拒绝引导”与“原始输出”之间的差分信号：

$$\Delta_{\ell}(i) = \mathrm{ZScore}\big(\Delta_{\ell}^{\mathrm{ans}}(i)\big) + \mathrm{ZScore}\big(\Delta_{\ell}^{\mathrm{cot}}(i)\big)$$

其中，$\Delta_{\ell}^{\mathrm{ans}}$ 和 $\Delta_{\ell}^{\mathrm{cot}}$ 分别为答案和思维链跨度的表示差分。通过对各自维度进行 Z-score 标准化后求和，该方法确保了两个跨度的信号在量级上被公平对待，避免了某一跨度主导遗忘方向。随后，通过 SVD 提取累积能量比 ≥ 0.8 的主成分作为遗忘子空间 $\mathbf{P}_{\ell}^{\mathrm{un}}$。消融实验证实，移除推理跨度（w/o Reasoning Span）会导致遗忘效果显著下降、推理泄漏上升，验证了混合跨度设计对抑制推理泄漏的必要性。

### 推理保留子空间（RRS）：正交投影保护通用推理

这是 R-MUSE 最具区分度的创新。现有方法要么缺乏专门的推理保护机制，要么仅通过损失函数中的隐式平衡来维持推理能力，效果有限。R-MUSE 显式地构建了一个**推理保留子空间（Reasoning Retain Subspace, RRS）**：在保留集上，对比“显式步骤推理”与“直接答案”的激活差异，通过 SVD 提取主方向 $\mathbf{P}_{\ell}^{\mathrm{rrs}}$，捕捉支持通用推理的表示方向。

在推理时，遗忘引导并非直接施加于原始隐藏状态，而是被投影到 RRS 的**正交补空间**：

$$\mathsf{Upd}_{\ell}\big(\mathbf{q}; \mathbf{h}_{\ell}\big) = g(\mathbf{q})\left(\mathbf{I} - \mathbf{P}_{\ell}^{\mathrm{rrs}}\right)\left(\mathbf{v}_{\ell}^{\mathrm{un}}\mathbf{v}_{\ell}^{\mathrm{un}\top}\right)\mathbf{h}_{\ell}$$

这一操作的本质是**解耦**：遗忘方向 $\mathbf{v}_{\ell}^{\mathrm{un}}$ 中与通用推理共线的分量被显式剔除，仅保留正交分量用于引导。消融实验提供了强有力的因果证据：移除 RRS 后，保留集分类准确率从 54.1% 骤降至 34.0%，验证了正交投影保护机制的核心作用。PCA 可视化（Figure 4）进一步从几何角度印证了这一机制：R-MUSE 引导后的隐藏状态在遗忘集上发生显著的方向性偏移和拉伸，而在保留集上与原始模型的结构高度重叠，表明遗忘被精准定向而不破坏保留能力。

### 门控机制：选择性激活遗忘引导

并非所有查询都需要遗忘干预。R-MUSE 引入了基于 RRS 对齐分数的**门控机制**：计算查询隐藏状态在 RRS 上的归一化投影长度 $s_{\mathrm{gate}}(\mathbf{q})$，仅当该分数低于阈值 $\tau$ 时才激活遗忘引导。这一设计确保与通用推理高度一致的查询免受干扰，实现了遗忘行为的查询级选择性。实验表明，门控阈值在 0.6–0.9 范围内性能稳定，但当 $\tau \geq 0.95$ 时遗忘失效，验证了门控对选择性引导的关键作用。

### 自适应校准引导（ACS）：无需手动调参的强度控制

传统激活引导方法依赖固定超参数（如系数 $\lambda$）来调节引导强度，这在实际部署中需要大量手动调优，且难以适应不同查询的异质性。R-MUSE 将引导过程形式化为**最优运输问题**：根据当前隐藏状态到安全流形的最小测地距离，自适应确定引导强度 $\lambda = \min\{1, \theta_{\mathrm{tar}} / \theta_{\mathrm{dir}}\}$，并通过球面线性插值实现范数保持的激活更新。消融实验表明，用固定强度替代 ACS（w/o ACS）会导致遗忘-保留平衡显著变差，证实了自适应校准可有效避免欠引导或过引导。

R-MUSE 是一种**无需训练的推理时激活引导框架**，其核心目标是在遗忘敏感信息的同时保护通用多模态推理能力。该框架通过离线构建两个正交子空间——遗忘子空间与推理保留子空间——并在推理时通过门控机制和自适应校准实现定向干预。

### 框架总览

整个 pipeline 由四个模块级联构成，按执行时序可分为**离线构建阶段**和**在线推理阶段**：

**离线构建阶段：**

1. **Span Hybrid Unlearning Subspace（跨度混合遗忘子空间）**：在遗忘集上，对比“拒绝引导生成”与“原始生成”的隐藏状态差异，同时提取答案跨度（$S_{\mathrm{ans}}$）和思维链跨度（$S_{\mathrm{cot}}$）的差分信号。二者经批次 Z-score 标准化后求和，再通过 SVD 提取累积能量比 ≥ 0.8 的主成分，构成遗忘子空间的投影矩阵 $\mathbf{P}_{\ell}^{\mathrm{un}}$。

2. **Reasoning Retain Subspace（推理保留子空间，RRS）**：在保留集上，采用与遗忘子空间相同的跨度差分管线，但对比的是“显式步骤推理”与“直接答案”的激活差异。通过 SVD 提取主方向，构建 RRS 投影矩阵 $\mathbf{P}_{\ell}^{\mathrm{rrs}}$，用于保护通用推理方向。

**在线推理阶段：**

3. **Gating Mechanism（门控机制）**：对于每个输入查询 $\mathbf{q}$，计算其在 RRS 上的归一化投影长度 $s_{\mathrm{gate}}(\mathbf{q})$。若 $s_{\mathrm{gate}}$ 低于阈值 $\tau$，则判定该查询与保留推理方向不一致，激活遗忘引导；否则跳过干预，避免对无关查询的误伤。

4. **Adaptive Calibration Steering（自适应校准引导，ACS）**：当门控激活时，将引导过程形式化为最优运输问题，根据当前隐藏状态到安全流形的最小测地距离自适应确定引导强度 $\lambda$。最终通过球面线性插值（Slerp）更新隐藏状态，实现范数保持的定向偏移。

### 输入输出流

- **输入**：多模态查询 $\mathbf{q}$（图像 + 文本）以及可选的引导前缀 $\mathbf{g}$。
- **离线构造输入**：遗忘集样本对（原始生成 vs. 拒绝引导生成）、保留集样本对（显式推理 vs. 直接答案）。
- **在线推理输出**：经激活引导后的隐藏状态序列，其最终生成的回答在遗忘敏感信息的同时保持推理连贯性。
- **关键约束**：遗忘引导方向 $\mathbf{v}_{\ell}^{\mathrm{un}}$ 被显式投影到 RRS 的正交补空间 $(\mathbf{I} - \mathbf{P}_{\ell}^{\mathrm{rrs}})$ 中，确保干预不破坏通用推理能力。

### 模块间关系

遗忘子空间与 RRS 在设计上形成**正交解耦**：前者捕获需要抑制的敏感信息方向，后者锚定需要保护的通用推理方向。门控机制作为二者的调度器，决定何时激活遗忘引导；ACS 则作为强度控制器，避免固定超参数带来的欠引导或过引导问题。这种“检测-定向-校准”的三段式架构使得 R-MUSE 能够在不修改模型参数的前提下，实现细粒度的推理保留遗忘。

R-MUSE 是一个无需训练的推理时激活引导框架，其核心由四个模块级联构成，分别解决遗忘方向构建、推理保护、选择性干预和自适应强度校准问题。

### 4.1 跨度混合遗忘子空间

传统遗忘方法仅针对最终答案标记构建差分信号，忽略了思维链中可能泄漏的敏感信息。R-MUSE 通过**跨度混合差分**同时捕获答案和推理轨迹中的遗忘方向。

首先，对遗忘集样本构造正负样本对：正样本 $\mathbf{x}_i^+$ 将问题与拒绝风格前缀 $\mathbf{g}$ 和理想拒绝答案拼接，引导模型生成拒绝行为；负样本 $\mathbf{x}_i^{-}$ 则保留原始答案。对每层 $\ell$ 的隐藏状态 $\mathbf{h}_{\ell,t}$，定义跨度池化操作：

$$\phi_{\ell}(\mathbf{x}; S) = \frac{1}{|S|} \sum_{t \in S} \mathbf{h}_{\ell,t}(\mathbf{x})$$

分别对答案跨度 $S_{\mathrm{ans}}$ 和思维链跨度 $S_{\mathrm{cot}}$ 计算差分：

$$\Delta_{\ell}^{\mathrm{ans}}(i) = \phi_{\ell}(\mathbf{x}_i^{+}; S_{\mathrm{ans}}) - \phi_{\ell}(\mathbf{x}_i^{\mathrm{ans},-}; S_{\mathrm{ans}})$$

$$\Delta_{\ell}^{\mathrm{cot}}(i) = \phi_{\ell}(\mathbf{x}_i^{+}; S_{\mathrm{cot}}) - \phi_{\ell}(\mathbf{x}_i^{\mathrm{cot},-}; S_{\mathrm{cot}})$$

为避免某一跨度的量级主导遗忘方向，对两类差分分别进行批归一化 Z-score 处理后再求和：

$$\Delta_{\ell}(i) = \mathrm{ZScore}\big(\Delta_{\ell}^{\mathrm{ans}}(i)\big) + \mathrm{ZScore}\big(\Delta_{\ell}^{\mathrm{cot}}(i)\big)$$

将所有样本的 $\Delta_{\ell}(i)$ 堆叠为矩阵，通过 SVD 提取满足累积能量比 $\ge 0.8$ 的前 $k$ 个左奇异向量，构造遗忘投影矩阵：

$$\mathbf{P}_{\ell}^{\mathrm{un}} = \mathbf{U}_{\ell}^{\mathrm{un}} \mathbf{U}_{\ell}^{\mathrm{un}\top}$$

该投影矩阵张成的子空间即为遗忘方向的主成分空间。

### 4.2 推理保留子空间与门控机制

为保护通用推理能力，R-MUSE 在保留集 $\mathcal{R}$ 上构建**推理保留子空间（RRS）**。对每个保留样本，构造正负对：正样本 $\mathbf{x}_i^+ = (\mathbf{g} \oplus \mathbf{q}_i) \oplus \mathbf{r}_i$ 包含显式推理步骤 $\mathbf{r}_i$，负样本 $\mathbf{x}_i^- = (\mathbf{g} \oplus \mathbf{q}_i) \oplus \mathbf{d}_i$ 仅含直接答案 $\mathbf{d}_i$。采用与遗忘子空间相同的跨度池化和 SVD 流程，提取推理保留投影矩阵：

$$\mathbf{P}_{\ell}^{\mathrm{rrs}} = \mathbf{U}_{\ell}^{\mathrm{rrs}}[:, 1:r] \big( \mathbf{U}_{\ell}^{\mathrm{rrs}}[:, 1:r] \big)^{\top}$$

其中秩 $r$ 同样由能量阈值确定。

推理时，通过**门控机制**决定是否对当前查询施加遗忘引导。计算查询 $\mathbf{q}$ 的末端隐藏状态在 RRS 上的归一化投影长度作为门控分数：

$$s_{\mathrm{gate}}(\mathbf{q}) = \frac{\|\mathbf{P}_{\ell^{*}}^{\mathrm{rrs}} \mathbf{h}_{\ell^{*}}^{\mathrm{end}}(\mathbf{g} \oplus \mathbf{q})\|_2}{\|\mathbf{h}_{\ell^{*}}^{\mathrm{end}}(\mathbf{g} \oplus \mathbf{q})\|_2}$$

当 $s_{\mathrm{gate}} < \tau$ 时，门控激活 $g(\mathbf{q}) = 1$，表示该查询与保留推理方向不一致，需要遗忘干预；否则 $g(\mathbf{q}) = 0$，跳过干预。这一设计确保仅对敏感查询进行定向引导，避免对保留集样本的误伤。

门控激活后的引导更新算子为：

$$\mathsf{Upd}_{\ell}(\mathbf{q}; \mathbf{h}_{\ell}) = g(\mathbf{q}) \left( \mathbf{I} - \mathbf{P}_{\ell}^{\mathrm{rrs}} \right) \left( \mathbf{v}_{\ell}^{\mathrm{un}} \mathbf{v}_{\ell}^{\mathrm{un}\top} \right) \mathbf{h}_{\ell}$$

其中 $\mathbf{v}_{\ell}^{\mathrm{un}}$ 为遗忘子空间的主方向向量，$\mathbf{I} - \mathbf{P}_{\ell}^{\mathrm{rrs}}$ 将引导方向投影到 RRS 的正交补空间，实现遗忘与推理的解耦。

### 4.3 自适应校准引导

传统激活引导使用固定强度系数 $\lambda$ 进行干预，缺乏对查询难度的自适应能力。R-MUSE 将引导过程形式化为**最优运输问题**，根据当前隐藏状态到安全流形的测地距离自适应确定引导强度。

定义目标分布与当前方向之间的角度 $\theta_{\mathrm{tar}}$，以及当前方向可用的最大角度 $\theta_{\mathrm{dir}}$，自适应校准权重为：

$$\lambda = \min\{1, \, \theta_{\mathrm{tar}} / \theta_{\mathrm{dir}}\}$$

该权重无需手动调节超参数，当目标距离较小时自动降低引导强度，避免过度干预。

最终通过球面线性插值（Slerp）实现范数保持的激活更新：

$$\tilde{\mathbf{h}} = r \frac{\mathbf{h} + \alpha \hat{\mathbf{v}}}{\|\mathbf{h} + \alpha \hat{\mathbf{v}}\|_2}$$

其中 $\alpha$ 由 $\lambda$ 控制，$\hat{\mathbf{v}}$ 为归一化引导方向，$r$ 为原始范数。该更新确保隐藏状态在球面上平滑移动，避免范数爆炸或坍塌。

### 关键公式汇总

| 公式 | 含义 | 锚点 |
|------|------|------|
| $\phi_{\ell}(\mathbf{x}; S)$ | 跨度池化：对令牌跨 $S$ 的隐藏状态取平均 | Eq. (4.1) |
| $\Delta_{\ell}(i)$ | Z-score 标准化后的混合差分，融合答案和思维链信号 | Eq. (4.2) |
| $\mathbf{P}_{\ell}^{\mathrm{un}}$ | 遗忘投影矩阵，由 SVD 提取主成分 | Eq. (4.4) |
| $\mathbf{P}_{\ell}^{\mathrm{rrs}}$ | 推理保留投影矩阵，保护通用推理方向 | Eq. (4.6) |
| $s_{\mathrm{gate}}(\mathbf{q})$ | 门控分数：查询在 RRS 上的归一化投影长度 | Eq. (4.7) |
| $\mathsf{Upd}_{\ell}$ | 正交投影引导更新算子 | Eq. (4.10) |
| $\lambda$ | 自适应校准权重，由 OT 距离比确定 | Eq. (4.16) |
| $\tilde{\mathbf{h}}$ | Slerp 更新后的隐藏状态 | Eq. (4.18) |

## 实验与关键发现

### 核心瓶颈验证：推理泄漏与能力坍塌的双重困境

现有MLLM遗忘方法面临一个根本性瓶颈：无法同时抑制推理链中的信息泄漏和保持总体推理能力。如Figure 1所示，传统MLLM遗忘方法虽然能改变最终答案，但其思维链（Chain-of-Thought）仍会重建已记忆的敏感事实，造成**推理泄漏**；而直接对LRM进行遗忘处理虽然避免了泄漏，却导致推理过程崩溃为不连贯、重复的输出，严重损害通用推理能力。

R-MUSE的核心洞察在于：遗忘方向可以构造为答案和推理轨迹的**混合跨度对比信号**，并在推理保留子空间（RRS）的正交补空间中进行自适应强度引导。这一机制在推理时通过激活引导实现，无需任何训练或参数更新。

### 主实验结果：遗忘-保留的帕累托前沿

Table 1和Table 3分别报告了5%、10%和15%遗忘率下的综合性能。在最具挑战性的15%遗忘率设置下，R-MUSE在两个主流骨干网络上均展现出显著优势：

**LLaVA-1.5-7B（15%遗忘率，Table 3）**：
- 遗忘集分类准确率从Vanilla模型的51.87%降至**21.80%**（降幅30.07个百分点），实现了深度遗忘
- 推理泄漏（RIL）从79.50%降至**39.20%**（降幅40.30个百分点），验证了混合跨度遗忘方向对抑制推理泄漏的有效性
- 保留集准确率保持45.85%，显著优于所有参数更新类基线方法

**Qwen-2.5-VL-7B（15%遗忘率，Table 3）**：
- 遗忘集准确率降至**33.80%**（Vanilla为60.50%，降幅26.70个百分点）
- 保留集准确率几乎无损（**53.60%** vs Vanilla 53.80%，仅下降0.20个百分点）
- 在遗忘-保留权衡上达到帕累托最优，显著优于GA、KL_Min、NPO、MMUnlearner、MANU等基线

Figure 5的遗忘-效用权衡分析进一步可视化这一优势：R-MUSE（红色星标）始终位于左上角理想区域（低遗忘准确率、高保留准确率），在两个骨干网络上均显著超越所有基线方法。相比之下，基于梯度更新的方法（如GA、NPO）往往在遗忘和保留之间做出非此即彼的牺牲，无法同时逼近帕累托前沿。

### 消融实验：三大核心组件的因果贡献

Table 2在Qwen-2.5-VL-7B上以5%遗忘率进行了系统性消融，揭示了各组件的因果机制：

**RRS正交投影（w/o RRS）**：移除RRS后，保留集分类准确率从54.1%骤降至**34.0%**（下降20.1个百分点），而遗忘集准确率仅从37.3%微降至35.9%。这一不对称效应表明：RRS的核心作用并非增强遗忘，而是**定向保护**通用推理能力——遗忘方向本身已足够有效，但缺乏正交约束会严重误伤保留集。这验证了“在正交补空间中引导”这一设计原则的必要性。

**混合跨度遗忘（w/o Reasoning Span）**：仅使用答案跨度构建遗忘方向时，遗忘集准确率从37.3%上升至42.1%，推理泄漏指标恶化。这说明思维链跨度包含的敏感信息无法仅通过答案层面对比消除，混合跨度信号对抑制推理泄漏**必不可少**。

**自适应校准（w/o ACS）**：用固定强度替代ACS后，遗忘-保留平衡整体变差。ACS将引导过程形式化为最优运输问题，根据当前隐藏状态到安全流形的最小测地距离自适应确定引导强度（见公式$\lambda = \operatorname* { m i n }\{ 1 , \: \theta _ { \mathrm { t a r } } / \theta _ { \mathrm { d i r } } \: \}$），避免了固定强度导致的欠引导（遗忘不足）或过引导（保留受损）。

**门控机制敏感性**：Figure 3显示，门控阈值τ在0.6–0.9范围内性能稳定；当τ≥0.95时遗忘几乎失效，验证了RRS门控对选择性干预的关键作用——门控通过计算查询与RRS的对齐分数$s _ { \mathrm { g a t e } } ( \mathbf { q } )$，确保仅对需要遗忘的查询激活引导，避免对无关输入的干扰。

### 推理能力保留：RCR指标的独立验证

Figure 2展示了推理能力保留（RCR）的对比结果。R-MUSE在Qwen-2.5-VL-7B上实现了最高的RCR分数，表明其遗忘过程不仅保护了分类准确率，更保护了**结构化推理能力**——模型在遗忘敏感知识后仍能生成有效、有证据支撑的推理步骤。这与RRS的设计目标一致：通过对比显式步骤推理与直接答案的激活差异，提取并保护支持通用推理的隐藏方向。

### 激活动态可视化：定向遗忘的几何证据

Figure 4通过PCA可视化提供了R-MUSE作用机制的几何证据。在LLaVA-1.5-7B和Qwen-2.5-VL-7B两个模型上：
- **保留集（蓝色）**：R-MUSE引导后的隐藏状态分布与Vanilla模型高度重叠，结构几乎不变
- **遗忘集（红色）**：R-MUSE引导后的隐藏状态发生显著的方向性偏移和拉伸，表明遗忘被定向到特定子空间

这一可视化直接印证了RRS正交投影机制的效果：遗忘方向的主成分被限制在RRS的正交补空间中，从而在不扰动保留集表示结构的前提下，对遗忘集施加定向干预。

### 数据集与评估公平性

所有实验均在RMLLMU-Bench的相同数据划分下进行（Table 4提供了数据集统计），包括遗忘集、保留集、测试集和名人集四个子集，确保数据分布和任务组成与基础基准严格对齐。评估采用统一指标：分类准确率（Fgt/Ret/Test/Cele）、Rouge分数、Cloze准确率、推理泄漏RIL和推理能力保留RCR。基线方法的超参数按原始论文建议或针对公平比较进行调优，实验覆盖LLaVA-1.5-7B和Qwen-2.5-VL-7B两个异构骨干网络。

### 待验证边界与开放问题

尽管R-MUSE在基准测试中表现优异，以下问题仍需进一步验证：
- **真实多模态隐私数据上的鲁棒性**：当前实验基于RMLLMU-Bench构造的遗忘场景，在真实部署中的推理泄漏抑制效果是否依然稳健尚待检验
- **遗忘方向构建的数据依赖**：遗忘方向与安全流形的构建依赖于高质量的正负样本对（拒绝引导vs原始输出），这一依赖对实际部署中样本获取成本的影响需要评估
- **跨架构可迁移性**：RRS和遗忘子空间在不同MLLM架构间的可迁移性尚未探索，这关系到方法的规模化应用
- **大规模遗忘集的扩展性**：当遗忘集规模显著增大时，正交保护机制是否仍能维持推理保留需要进一步验证

![[assets/figures/papers/paper_list_l790_https_arxiv_org_abs_2512_17911/figures/008_Table_3.jpg]]
*Table 3: Unlearning performance on RMLLMU-Bench with a 15% Forget Rate. Results are evaluated on the forget set (Fgt), test set (Test), retain set (Ret), and celebrity set (Cele). ↓ indicates lower is better, and ↑ indicates higher is better*

![[assets/figures/papers/paper_list_l790_https_arxiv_org_abs_2512_17911/figures/003_Table_2.jpg]]
*Table 2: Ablation study on RMLLMU-Bench (5% Forget) using Qwen-2.5-VL-7B-Instruct. ↓ lower is better, ↑ higher is better*

![[assets/figures/papers/paper_list_l790_https_arxiv_org_abs_2512_17911/figures/006_Figure_4.jpg]]
*Figure 4: PCA Visualization of Activation Dynamics. We compare the hidden state distributions of the Vanilla model (light colors) and the R-MUSE Steered model (dark colors) on LLaVA-1.5-7B (a) and Qwen-2.5-VL-7B (b). Left (Blue): The Retain Set shows high structural overlap, demonstrating that general reasoning capabilities are preserved, though slight deviations (dragging) are visible due to global steering effects. Right (Red): The Forget Set exhibits a significant directional shift and elongation, indicating that the sensitive reasoning paths are effectively re-oriented towards the refusal subspace*

![[assets/figures/papers/paper_list_l790_https_arxiv_org_abs_2512_17911/figures/007_Figure_5.jpg]]
*Figure 5: Forgetting-Utility Trade-off Analysis. We plot the Retain Set Accuracy vs. Forget Set Accuracy for LLaVA-1.5-7B (a) and Qwen-2.5-VL-7B (b). The ideal performance is located in the top-left corner (Low Forget Acc, High Retain Acc). R-MUSE (Red Star) significantly outperforms all baselines, achieving deep unlearning while maintaining utility comparable to the Vanilla model (Grey Diamond). In contrast, optimization-based baselines (Circles) suffer from utility collapse (dropping low on y-axis), while other SOTA methods (Squares) fail to unlearn effectively (staying right on x-axis)*

![[assets/figures/papers/paper_list_l790_https_arxiv_org_abs_2512_17911/figures/002_Table_1.jpg]]
*Table 1: Unlearning performance on MLLMU-Bench (5% and 10% Forget Rate,15% in Appendix E). Results are evaluated on the forget set (Fgt), test set (Test), retain set (Ret), and celebrity set (Cele). ↓ indicates lower is better, and ↑ indicates higher is better*

![[assets/figures/papers/paper_list_l790_https_arxiv_org_abs_2512_17911/figures/009_Table_4.jpg]]
*Table 4: Key statistics of the RMLLMU-Bench. The dataset maintains strict alignment in data distribution and task composition with the foundational benchmark*

## 定位与知识库关联

### 问题定位：推理泄漏与能力坍塌的双重困境

多模态大语言模型（MLLM）和推理增强大语言模型（LRM）的遗忘（unlearning）面临一个此前未被充分认识的核心矛盾：**仅针对最终答案的遗忘会在推理链中残留敏感信息，而针对推理链的遗忘则容易导致推理能力的全面崩溃**。Figure 1 直观展示了这一困境——左侧的 MLLM 遗忘方法虽然改变了最终答案，但思维链（chain-of-thought）仍完整重构了被遗忘的事实，造成“推理泄漏”（reasoning leakage）；右侧的 LRM 遗忘方法虽避免了泄漏，却陷入不连贯、重复的推理模式，破坏了通用推理能力。

这一矛盾源于现有遗忘方法的两个根本性设计缺陷：（1）遗忘目标仅覆盖最终答案的表示，未触及推理过程中逐步展开的中间状态；（2）缺乏将敏感信息遗忘与通用推理保护进行显式解耦的机制。

### 现有方法谱系与 R-MUSE 的定位

当前 MLLM/LRM 遗忘方法可沿两个维度进行归类：**干预方式**（训练时微调 vs. 推理时引导）与**遗忘粒度**（答案级 vs. 推理级）。

**训练时微调范式**构成了当前的主流基线。**GA（Gradient Ascent）** 直接在遗忘样本上最大化损失，是最朴素的遗忘策略；**KL_Min** 通过最小化遗忘模型与原始模型在保留集上的 KL 散度来维持效用；**NPO（Negative Preference Optimization）** 将遗忘形式化为负偏好优化问题，在拒绝遗忘样本的同时保持对保留样本的正常响应。这些方法均共享一个关键局限：遗忘信号仅通过损失函数作用于参数更新，缺乏对推理过程中间状态的显式控制。**MMUnlearner** 和 **MANU（Modality-Aware Neuron Unlearning）** 进一步引入了多模态感知机制，前者针对视觉-语言跨模态关联进行遗忘，后者通过定位模态特异性神经元实现选择性参数修改，但它们仍然在训练时参数空间中操作，遗忘-保留的平衡依赖于超参数调优，缺乏对推理链泄漏的结构性抑制。

**推理时引导范式**的代表是 **R²MU**，该方法通过推理时的激活引导实现遗忘，避免了对模型参数的永久修改。然而，R²MU 的引导方向主要针对最终答案的表示，且缺乏对通用推理方向的显式保护机制，因此在抑制推理泄漏方面效果有限。

**R-MUSE 在上述谱系中的定位**是：**推理时引导范式下，首个同时覆盖答案与推理链、并显式构建推理保留子空间的方法**。其关键差异体现在四个维度：

| 维度 | 训练时微调方法 | R²MU | R-MUSE |
|------|---------------|------|--------|
| 干预方式 | 参数更新 | 推理时引导 | 推理时引导 |
| 遗忘目标 | 最终答案 | 最终答案 | 答案 + 推理链混合跨度 |
| 推理保护 | 隐式（损失平衡） | 无 | 显式（RRS 正交投影） |
| 引导强度 | 固定超参数 | 固定超参数 | 自适应（ACS，基于最优运输） |

### 核心机制的知识贡献

R-MUSE 的三个核心模块各自对应一个方法学贡献，可被后续工作独立复用或组合改进：

**（1）Span Hybrid Unlearning Subspace（混合跨度遗忘子空间）**：通过对比“拒绝引导生成”与“原始召回生成”在答案跨度（$S_{\text{ans}}$）和思维链跨度（$S_{\text{cot}}$）上的激活差异，构建遗忘方向。关键设计在于对两类差分分别进行 Z-score 标准化后求和（$\Delta_{\ell}(i) = \text{ZScore}(\Delta_{\ell}^{\text{ans}}(i)) + \text{ZScore}(\Delta_{\ell}^{\text{cot}}(i))$），避免某一跨度的量级主导遗忘方向。经 SVD 取累积能量比 ≥ 0.8 的主成分作为遗忘子空间。这一设计的洞察在于：推理泄漏的本质是模型在生成过程中逐步“回忆”被遗忘事实，仅抑制最终答案的表示无法阻断这一过程。

**（2）Reasoning Retain Subspace（RRS，推理保留子空间）**：在保留集上通过对比“显式步骤推理”与“直接答案”的激活差异，提取支持通用推理的主方向，并构建投影矩阵 $\mathbf{P}_{\ell}^{\text{rrs}}$。推理时，遗忘引导被投影到 RRS 的正交补空间 $(\mathbf{I} - \mathbf{P}_{\ell}^{\text{rrs}})$ 中执行，从而在几何上将遗忘方向与推理方向解耦。消融实验（Table 2）显示，移除 RRS 使保留集分类准确率从 54.1% 骤降至 34.0%，验证了这一正交保护机制的必要性。

**（3）Adaptive Calibration Steering（ACS，自适应校准引导）**：将引导过程形式化为最优运输问题，根据当前隐藏状态到“安全流形”的最小测地距离自适应确定引导强度 $\lambda = \min\{1, \theta_{\text{tar}} / \theta_{\text{dir}}\}$，无需手动设置超参数。通过球面线性插值（Slerp）实现范数保持的激活更新。这一设计解决了传统激活引导中固定强度导致的欠引导（遗忘不充分）或过引导（推理崩溃）问题。

### 适用边界与局限

**适用前提**：R-MUSE 的有效性依赖于以下条件：（1）存在可获取的拒绝引导模板池 $\mathcal{G}$，用于构造遗忘方向的正样本；（2）保留集 $\mathcal{R}$ 能够覆盖目标通用推理模式的多样性，以构建有效的 RRS；（3）遗忘集与保留集在特征空间中具有足够的可分离性，使得正交投影能够有效解耦。

**已知局限**：论文未报告在真实多模态隐私数据（如人脸、医疗图像）上的评估结果，RMLLMU-Bench 的评估集中在结构化知识（如名人识别）场景。此外，遗忘方向与安全流形的构建依赖于高质量的正负样本对，当遗忘请求涉及复杂、模糊的语义边界时，对比信号的可靠性可能下降。

**架构依赖性**：RRS 和遗忘子空间的构建基于特定层的隐藏状态表示，其有效性可能受 MLLM 架构（如视觉编码器类型、跨模态融合机制）的影响。论文在 LLaVA-1.5-7B 和 Qwen-2.5-VL-7B 上验证了方法，但向其他架构（如基于 Q-Former 的 BLIP-2 系列或更大规模模型）的迁移性尚待验证。

### 开放问题与后续方向

1. **遗忘子空间的可迁移性**：RRS 和遗忘子空间在不同 MLLM 架构间是否可迁移？若能构建架构无关的遗忘/推理方向表示，将大幅降低部署成本。

2. **大规模遗忘的扩展性**：当遗忘集规模增大时，正交保护机制是否仍能维持推理保留？遗忘方向的信噪比可能随样本增多而下降，需要研究子空间聚合策略。

3. **动态遗忘请求的适应性**：ACS 中的最优运输目标分布目前是静态构建的，能否动态扩展以处理增量式、序列化的遗忘请求（continual unlearning）？

4. **评估体系的完善**：当前 RMLLMU-Bench 的推理泄漏评估（RIL）依赖 LLM 评判器，其对隐式泄漏的检测灵敏度有待进一步标定。更严格的对抗性评估（如通过 probing classifier 检测隐藏状态中的残留信息）将是对 R-MUSE 遗忘彻底性的重要补充验证。

5. **与训练时方法的融合**：R-MUSE 作为推理时方法，可与训练时遗忘方法形成互补——后者负责粗粒度的参数级遗忘，前者负责细粒度的推理时泄漏抑制。这种“训练-推理”联合遗忘框架的设计空间值得探索。

## 原文 PDF

![[paperPDFs/CVPR_2026/Towards_Reasoning_Preserving_Unlearning_in_Multimodal_Large_Language_Models.pdf]]
