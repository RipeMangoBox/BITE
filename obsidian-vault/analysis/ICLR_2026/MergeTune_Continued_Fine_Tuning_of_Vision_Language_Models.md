---
title: "MergeTune: Continued Fine-Tuning of Vision-Language Models"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/MergeTune_Continued_Fine_Tuning_of_Vision_Language_Models.pdf
project_link: null
code_link: https://github.com/Surrey-UP-Lab/MERGETUNE
aliases:
- MergeTune
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/vision_models_multimodal
core_operator: "将零样本模型和下游微调模型作为两个端点，用持续微调优化线性模式连通性并以 L2 代理正则近似预训练任务约束。"
primary_logic: |
  MergeTune 在下游微调完成后初始化一个持续模型，使其同时靠近零样本模型和微调模型。
  它用 LMC 目标约束持续模型与微调端点之间的低损失插值路径，并用由二阶泰勒展开得到的 L2 正则项替代不可访问的预训练数据回放。
  训练后的模型隐式合并零样本知识与下游任务知识，从而缓解 VLM 微调后的灾难性遗忘。
claims:
- "持续微调可作为后置步骤恢复 VLM 微调过程中丢失的预训练知识。"
- "LMC 目标与 L2 代理正则项可以在无预训练数据回放的情况下实现有效模型合并。"
- "MERGETUNE 在基类-新类泛化、跨数据集泛化和鲁棒微调评估中稳定提升多种 VLM 微调基线。"
---

# MergeTune: Continued Fine-Tuning of Vision-Language Models

> [!tip] 核心洞察
> 核心洞察在于，通过将线性模式连通性（LMC）直接作为学习目标进行持续微调，可以有效地合并零样本模型和微调模型，从而恢复微调过程中丢失的预训练知识。该方法的关键创新在于：1）提出了“持续微调”（CFT）这一新范式，将知识恢复从微调过程中解耦出来，作为后置步骤；2）利用二阶泰勒展开推导出一个无需数据回放的代理正则项，解决了LMC约束需要预训练数据回放的实际难题；3）该方法与模型无关，可以即插即用地应用于任何已微调的VLM，无需修改架构。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | MergeTune：视觉语言模型的持续微调 |
| 英文题名 | MergeTune: Continued Fine-Tuning of Vision-Language Models |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=MAApSY32Z6) · [GitHub](https://github.com/Surrey-UP-Lab/MERGETUNE) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal |
| Method | MERGETUNE |
| Dataset | 基类-新类泛化 (11个数据集平均) |

> [!tip] 效果简介
> - 基类-新类泛化 (11个数据集平均) 上，调和平均数 (HM) 为 77.24 (CoOp + MERGETUNE)，对比 71.66 (CoOp)，变化 +5.58。
> - 基类-新类泛化 (11个数据集平均) 上，调和平均数 (HM) 为 77.98 (KgCoOp + MERGETUNE)，对比 77.01 (KgCoOp)，变化 +0.97。
> - 基类-新类泛化 (11个数据集平均) 上，调和平均数 (HM) 为 80.44 (MMA + MERGETUNE)，对比 79.87 (MMA)，变化 +0.57。

## 概要

本文提出 **MERGETUNE**，一种新颖的**持续微调（Continued Fine-Tuning, CFT）** 策略，旨在解决视觉语言模型（VLM）在下游任务微调后出现的**灾难性遗忘**问题。与现有在微调过程中缓解遗忘的方法不同，MERGETUNE 将知识恢复作为微调完成后的后置步骤，通过**线性模式连通性（Linear Mode Connectivity, LMC）** 作为学习目标，隐式地合并零样本模型（如 CLIP）与已微调模型的知识。该方法无需修改模型架构，可即插即用地应用于任何已微调的 VLM。实验表明，MERGETUNE 在基类-新类泛化任务中将 CoOp 的调和平均数（HM）提升了 +5.6%，在鲁棒微调评估中超越了集成基线，且推理成本更低。

现有的视觉语言模型（VLM）微调方法（如 CoOp、KgCoOp、MMA 等）在适应下游任务时，不可避免地会遗忘预训练知识（灾难性遗忘）。即使采用参数高效微调（PEFT）或集成方法，也无法完全保留预训练知识，导致模型在基类-新类泛化、跨数据集泛化和分布外泛化等场景下性能受限。例如，没有任何一种 PEFT 方法能在所有 11 个数据集上一致地优于 CLIP 零样本模型（Figure 1）。

![Figure 1](Figure 1)

此外，现有的无训练模型合并方法（如 TIES-Merging、DARE）在应用于 CLIP 微调方法时通常会降低性能（例如，CoOp + TIES 的 HM 下降 5.3%）。这是因为零样本模型与微调模型在权重空间中可能相距甚远，破坏了模式连通性，使得模型合并失效。

## 核心方法与创新机理

MERGETUNE 的核心创新在于：

1. **提出“持续微调”（CFT）新范式**：将知识恢复从微调过程中解耦出来，作为后置步骤，在微调完成后恢复遗忘的预训练知识。
2. **以线性模式连通性（LMC）作为学习目标**：通过优化目标函数，使得持续微调后的模型与零样本模型和微调模型之间都存在低损失的线性插值路径，从而隐式地合并两个模型的知识。
3. **无需数据回放的代理正则项**：利用二阶泰勒展开推导出一个代理正则项（L2 距离），近似零样本任务损失，解决了 LMC 约束需要预训练数据回放的实际难题。
4. **模型无关性**：该方法与模型无关，可以即插即用地应用于任何已微调的 VLM，无需修改架构。

MERGETUNE 的整体框架如 Figure 2 所示。给定一个零样本检查点 ŵ₁（如 CLIP）和一个下游微调检查点 ŵ₂（如 CoOp），MERGETUNE 通过持续微调搜索一个持续模型 w，使其与两个端点之间都存在低损失的线性插值路径。

![Figure 2](Figure 2)

框架包含三个核心模块：
- **零样本模型 (ŵ₁)**：提供预训练知识，作为 L2 代理正则项的目标。
- **微调模型 (ŵ₂)**：提供下游任务知识，作为 LMC 损失的目标。
- **持续微调目标函数**：包含下游任务损失、L2 代理正则项和 LMC 损失，用于优化持续模型 w。

### 1 线性模式连通性（LMC）

给定两个模型权重 ŵ₁ 和 ŵ₂，线性插值定义为：

$$w = \gamma(\alpha) = (1-\alpha)\hat{w}_1 + \alpha\hat{w}_2, \quad \alpha \in [0,1].$$

低损失条件要求沿插值路径的损失保持接近零：

$$\mathcal{L}(\gamma(\alpha)) \approx 0.$$

### 2 双任务模式连通性

MERGETUNE 的目标是找到一个持续模型 w，使其与两个端点之间都存在低损失路径。定义从每个端点到 w 的线性路径：

$$\gamma_1(\alpha) = \hat{w}_1 + \alpha(w - \hat{w}_1), \quad \gamma_2(\alpha) = \hat{w}_2 + \alpha(w - \hat{w}_2), \quad \alpha \in [0,1].$$

双任务模式连通性条件要求两条插值路径在其各自任务上均保持低损失：

$$\mathcal{L}_1(\gamma_1(\alpha)) \approx 0, \quad \mathcal{L}_2(\gamma_2(\alpha)) \approx 0.$$

### 3 MERGETUNE 目标函数

持续微调的目标函数强制与两个检查点保持线性模式连通性：

$$w = \underset{w}{\arg\min} \ \mathbb{E}_{\alpha \sim \mathcal{U}[0,1]} \Big[ \mathcal{L}_1(\hat{w}_1 + \alpha(w - \hat{w}_1)) + \mathcal{L}_2(\hat{w}_2 + \alpha(w - \hat{w}_2)) \Big].$$

### 4 无需数据回放的代理正则项

由于任务 1（预训练任务）的数据不可用，无法直接计算 $\mathcal{L}_1$。论文利用二阶泰勒展开进行近似：

$$\mathcal{L}_1(\hat{w}_1 + \alpha(w - \hat{w}_1)) \approx \mathcal{L}_1(\hat{w}_1) + \alpha \nabla \mathcal{L}_1(\hat{w}_1)^\top (w - \hat{w}_1) + \frac{\alpha^2}{2} (w - \hat{w}_1)^\top H_1 (w - \hat{w}_1).$$

在零梯度（ŵ₁ 是预训练任务的最优解）和各向同性 Hessian 假设下，简化为：

$$\mathcal{L}_1(\hat{w}_1 + \alpha(w - \hat{w}_1)) \approx \mathcal{L}_1(\hat{w}_1) + \frac{\mu \alpha^2}{2} \|w - \hat{w}_1\|^2.$$

由此得到任务 1 的代理正则项：

$$\mathcal{R}_{\mathrm{Task1}} = \lambda \|w - \hat{w}_1\|^2.$$

### 5 最终无回放目标函数

最终的持续微调损失结合了下游任务损失、与 ŵ₁ 的接近性以及与 ŵ₂ 的低损失连通性：

$$\mathcal{L}(w) = \mathcal{L}_2(w) + \lambda \|w - \hat{w}_1\|^2 + \beta \mathbb{E}_{\alpha \sim \mathcal{U}[0,1)} \mathcal{L}_2(\hat{w}_2 + \alpha(w - \hat{w}_2)).$$

其中，期望项通过评估少量均匀间隔的 α 值（如 5 个）来近似。

## 实验与关键发现

### 1 基类-新类泛化

Table 1 展示了 MERGETUNE 在 11 个数据集上的基类-新类泛化实验结果。MERGETUNE 在所有基线上均取得一致的性能提升。

![Table 1](Table 1)

关键结果：
- CoOp + MERGETUNE：HM 从 71.66 提升至 77.24（+5.58）
- KgCoOp + MERGETUNE：HM 从 77.01 提升至 77.98（+0.97）
- MMA + MERGETUNE：HM 从 79.87 提升至 80.44（+0.57）
- PromptKD + MERGETUNE：HM 从 83.73 提升至 84.09（+0.36）

相比之下，现有无训练合并方法（TIES, DARE）通常会降低性能（例如，CoOp + TIES 的 HM 下降 5.3%）。

### 2 跨数据集泛化

Table 2 展示了跨数据集泛化实验结果。模型在 ImageNet 上训练，直接在其他数据集上评估。

![Table 2](Table 2)

- CoOp + MERGETUNE：Avg-C 从 63.88 提升至 65.80（+1.92）
- KgCoOp + MERGETUNE：Avg-C 从 65.51 提升至 66.53（+1.02）

### 3 域泛化

Table 3 展示了域泛化实验结果。

![Table 3](Table 3)

- CoOp + MERGETUNE：Avg-D 从 59.28 提升至 60.15（+0.87）
- KgCoOp + MERGETUNE：Avg-D 从 60.11 提升至 60.46（+0.35）

### 4 ID-OOD 泛化（鲁棒微调）

Table 4 展示了鲁棒微调评估中的 ID-OOD 泛化准确率。

![Table 4](Table 4)

- E2E-FT + MERGETUNE：Avg-D 从 53.70 提升至 62.29（+8.59）
- E2E-FT + MERGETUNE + Weight ens.：Avg-D 达到 62.90（+9.20）

MERGETUNE 的 LMC 合并模型在推理成本更低的情况下超越了集成基线。

### 5 消融与分析

**超参数敏感性**（Figure 3）：MERGETUNE 对超参数选择鲁棒，HM 在不同 λ 和 β 组合下变化范围很小。最佳性能在 λ ∈ [8, 16] 和 β ∈ [0.1, 0.5] 时达到。

![Figure 3](Figure 3)

**初始化参数**（Table 8）：当持续模型的初始化参数 τ ∈ [0.3, 0.6]（平衡地混合零样本和微调模型权重）时，性能最优。

**插值点数**（Table 9）：LMC 近似中的插值点数 N_α 从 1 增加到 5 时性能稳步提升，之后饱和；N_α=5 是平衡性能和训练成本的选择。

**过合并分析**（Figure 5）：持续微调不会导致过合并，在 10 到 100 个 epoch 的训练中，所有 11 个数据集上的性能均未出现退化。

![Figure 5](Figure 5)

### 6 跨骨干网络泛化

Table 6 展示了在不同视觉语言模型（CLIP-L/14, Siglip2-B/16, Siglip2-L/16）上的基类-新类泛化实验。MERGETUNE 在所有模型架构上均取得一致的性能提升。

![Table 6](Table 6)

## 定位与知识库关联

MERGETUNE 定位于**模型合并**与**持续学习**的交叉领域。与现有方法相比，其核心差异在于：

| 维度 | 现有方法 | MERGETUNE |
|------|----------|-----------|
| 微调范式 | 在微调过程中缓解遗忘（如 PEFT、集成） | 在微调完成后，通过持续微调（CFT）恢复遗忘的知识 |
| 模型合并方法 | 无训练方法（如 TIES, DARE）或简单的权重平均 | 基于学习的合并方法，以 LMC 为目标进行持续微调 |
| LMC 约束的数据需求 | 需要回放预训练数据 | 通过二阶泰勒展开推导出代理正则项（L2 距离），无需数据回放 |
| 模型适用性 | 通常需要特定架构或训练过程 | 模型无关，可后置应用于任何已微调的 VLM，无需架构修改 |

**局限性**：
- 持续微调过程需要额外的训练步骤和计算成本（N_α=5 时训练成本约为基线的 3 倍）。
- 代理正则项（L2 距离）基于零梯度和各向同性 Hessian 的强假设，在复杂损失景观下可能不精确。
- 方法在基类-新类泛化上的提升幅度因基线方法而异（CoOp 提升大，PromptKD 提升小），可能依赖于基线方法的遗忘程度。
- 实验主要在 CLIP 和 SigLIP2 系列模型上进行，在其他 VLM 架构上的泛化性未验证。

**开放问题**：
- MERGETUNE 的代理正则项在更复杂的损失景观（如非凸、多模态）下是否仍然有效？
- MERGETUNE 能否应用于其他类型的预训练模型（如纯文本模型、多模态模型）？
- MERGETUNE 的持续微调过程是否可能引入新的过拟合风险，尤其是在小样本场景下？
- MERGETUNE 与更先进的模型合并方法（如 AdaMerging, Fisher Merging）相比性能如何？

### 整体框架

![[assets/figures/papers/iclr26_0001_MAApSY32Z6_MergeTune_Continued_Fine-Tuning_of_Vision-Langua/figures/001_Figure_1.jpg]]
*Figure 1: Cross-dataset generalisation shows no single PEFT method consistently outperforms CLIP across all 11 datasets, implying incomplete preservation of pretrained knowledge. Numbers in brackets (X/11) indicate X times a method underperforms CLIP.*

### 实验与分析

![[assets/figures/papers/iclr26_0001_MAApSY32Z6_MergeTune_Continued_Fine-Tuning_of_Vision-Langua/figures/003_Table_1.jpg]]
*Table 1: Base-to-novel generalisation experiments on 11 datasets. Our method achieves consistent average performance improvement over different baselines. †: Using large language model or teacher model’s knowledge.*

![[assets/figures/papers/iclr26_0001_MAApSY32Z6_MergeTune_Continued_Fine-Tuning_of_Vision-Langua/figures/004_Table_2.jpg]]
*Table 2: Cross-dataset generalisation results. Models are trained on ImageNet and directly evaluated on other datasets. Avg-C = average over all cross-dataset targets. *: Our reproduction. †: Using external knowledge.*

![[assets/figures/papers/iclr26_0001_MAApSY32Z6_MergeTune_Continued_Fine-Tuning_of_Vision-Langua/figures/005_Table_3.jpg]]
*Table 3: Domain generalisation results on ImageNet and four distribution shifts. Avg-D = average over domain-shifted datasets. MMA* is our reproduction.*

![[assets/figures/papers/iclr26_0001_MAApSY32Z6_MergeTune_Continued_Fine-Tuning_of_Vision-Langua/figures/006_Table_4.jpg]]
*Table 4: ID-OOD generaisation accuracy of various methods on ImageNet and distribution shifts for CLIP ViT-B/16 in the robust fine-tuning evaluation. Avg-D = average over domain-shifted datasets.*

![[assets/figures/papers/iclr26_0001_MAApSY32Z6_MergeTune_Continued_Fine-Tuning_of_Vision-Langua/figures/009_Table_5.jpg]]
*Table 5: ID-OOD generaisation accuracy of various methods on ImageNet and distribution shifts for CLIP ViT-B/32 in the robust fine-tuning evaluation. Avg-D = average over domain-shifted datasets.*

## 原文 PDF

![[paperPDFs/ICLR_2026/MergeTune_Continued_Fine_Tuning_of_Vision_Language_Models.pdf]]
