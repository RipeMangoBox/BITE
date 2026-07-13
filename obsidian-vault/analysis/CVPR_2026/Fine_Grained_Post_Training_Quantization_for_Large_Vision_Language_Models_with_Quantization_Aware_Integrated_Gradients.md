---
title: Fine-Grained Post-Training Quantization for Large Vision Language Models with Quantization-Aware Integrated Gradients
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Fine_Grained_Post_Training_Quantization_for_Large_Vision_Language_Models_with_Quantization_Aware_Integrated_Gradients.pdf
project_link: null
code_link: "https://github.com/ucas-xiang/QIG"
aliases:
- QQAIG
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 引入基于量化感知集成梯度的令牌级敏感性评分（QIG），将每个令牌对量化误差的贡献量化为重要性系数λ_i，并用于重新加权重建误差，实现细粒度优化。
primary_logic: 集成梯度对量化前后输出差异的归因能力，能够将误差分解为每个输入令牌的贡献，从而提供直接且细粒度的令牌重要性信号，指导训练后量化。
claims:
- 在VizWiz基准上，令牌级敏感性（扰动方法）准确率达57.72%，显著高于模态级方法的56.81%（Table 1）。
- 在LLaVA-onevision-7B W3A16设置下，QIG的平均准确率比MBQ高1.60%，将性能差距缩小到全精度模型的1.33%（Table 2）。
- 消融实验中，使用量化基线x^q和误差目标f(x)−f(x^q)的QIG配置在ChartQA和VizWiz上取得最佳性能，验证了专门针对量化误差的归因设计（Table 4）。
- LLaVA-onevision-7B W3A16 (平均) 上 平均准确率 = 72.04%
---

# Fine-Grained Post-Training Quantization for Large Vision Language Models with Quantization-Aware Integrated Gradients

> [!tip] 核心洞察
> 集成梯度对量化前后输出差异的归因能力，能够将误差分解为每个输入令牌的贡献，从而提供直接且细粒度的令牌重要性信号，指导训练后量化。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于量化感知集成梯度的大视觉语言模型细粒度训练后量化 |
| 英文题名 | Fine-Grained Post-Training Quantization for Large Vision Language Models with Quantization-Aware Integrated Gradients |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.17809) · [Code](https://github.com/ucas-xiang/QIG) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | QIG (Quantization-aware Integrated Gradients) |
| Dataset | LLaVA-onevision-7B W3A16, VizWiz, ChartQA |

> [!tip] 效果简介
> - LLaVA-onevision-7B W3A16 (平均) 上，平均准确率 72.04% vs MBQ 70.44% (+1.60%)。
> - VizWiz (InternVL2-8B W4A8) 上，准确率 58.33% vs MBQ 57.36% (+0.97%)。
> - ChartQA (InternVL2-26B W4A8) 上，准确率 85.24% vs MBQ 84.44% (+0.80%)。

## 概要

大视觉语言模型（LVLM）的训练后量化（PTQ）面临一个被忽视的瓶颈：现有方法仅在**模态层面**分配敏感性权重（如视觉 vs. 文本），却忽略了同一模态内不同令牌之间的显著异质性。这种粗粒度假设导致量化误差分配不均，性能次优。

本文提出 **QIG（Quantization-aware Integrated Gradients）**，一种细粒度的令牌级量化策略。其核心洞察在于：集成梯度（Integrated Gradients）能够将量化前后模型的输出差异归因到每个输入令牌，从而提供直接且细粒度的令牌重要性信号。QIG 以量化后的输入为基线、全精度输入为目标，计算每个令牌对量化误差的贡献，经 IQR 剪裁与归一化后得到令牌重要性系数 λᵢ，并将其融入通道均衡（CWE）目标函数中，实现对不同令牌重建误差的差异化加权。

实验表明，在 LLaVA-onevision-7B 的 W3A16 设置下，QIG 的平均准确率比模态平衡基线 MBQ 高出 **1.60%**，将性能差距缩小到全精度模型的仅 **1.33%**；在 InternVL2-8B 和 InternVL2-26B 上同样取得一致提升。该方法计算开销可忽略，且与 GPTQ 等权重量化方法正交兼容。

### 大视觉语言模型的量化挑战

大视觉语言模型（Large Vision-Language Models, LVLMs）通过融合视觉编码器与大语言模型，在多模态理解任务上取得了显著进展。然而，其庞大的参数量与计算开销严重制约了实际部署。训练后量化（Post-Training Quantization, PTQ）作为一种高效的模型压缩手段，通过将浮点权重和激活值映射到低位宽整数表示，能够大幅降低推理成本。在LVLM中，权重-激活（WA）量化通常采用通道均衡（Channel-wise Equalization, CWE）框架，其核心目标是最小化每个Transformer块内量化输出与原始输出的均方误差：

$$\mathbf{E}^{*} = \underset{\mathbf{E}}{\arg\min} \left\| Q_{W}(\mathbf{W} * \mathbf{E}) Q_{\mathcal{X}}(\mathbf{E}^{-1} * \mathbf{X}) - \mathbf{W}\mathbf{X} \right\|_{2}^{2}$$

然而，该目标函数对所有输入令牌的重建误差施加了同等权重，隐式假设了各令牌对输出质量具有相同的重要性。这一假设在多模态场景下是否成立，构成了本文的核心问题。

### 模态级敏感性的局限性

现有LVLM量化方法，如模态平衡量化（**MBQ**），已经认识到视觉令牌与文本令牌对量化误差的敏感性存在差异，并在模态层面上分配不同的敏感性权重。然而，本文通过对InternVL2-8B在校准过程中的激活分布进行系统可视化（Figure 2），揭示了四个反复出现的现象：**大规模激活（massive activations）、层异质性（layer heterogeneity）、子层分歧（sub-layer divergence）以及令牌变异性（token variability）**。这些观察表明，即使在同一模态内部，不同令牌位置的激活模式也存在显著差异，模态级的粗粒度敏感性建模不足以捕捉这种细粒度结构。

进一步的量化敏感性分析（Figure 1）证实了这一判断：利用本文提出的量化感知集成梯度（QIG）对跨层令牌敏感性进行测量，热力图和曲线均显示，不仅视觉与文本令牌之间存在敏感性差异，同一模态内的不同令牌（如特殊令牌、不同位置的视觉令牌）也呈现出高度异质的量化敏感性。这一发现构成了本文的核心动机：**量化敏感性不仅依赖于模态，更高度依赖于令牌**。

### 现有令牌级方法的不足

为验证令牌级敏感性建模的必要性，本文在VizWiz基准上（InternVL2-8B, W4A8）系统比较了多种敏感性估计策略（Table 1）。实验结果表明，直观的令牌级方法并不一定优于模态级方法：基于梯度的令牌级加权仅达到55.78%准确率，显著低于模态级方法的57.36%；基于注意力权重的令牌级方法虽有提升（57.12%），但增益有限且不稳定。这一反直觉现象揭示了一个关键瓶颈：**缺乏专门针对量化误差设计的令牌级归因机制**，导致简单的令牌级敏感性估计无法有效指导量化优化。

### 本文动机

综上，现有LVLM量化方法面临的核心缺口在于：敏感性建模的粒度受限于模态层面，而缺乏一种能够直接量化每个输入令牌对量化误差贡献的细粒度机制。本文的动机正是填补这一空白——通过引入公理化归因（axiomatic attribution）的思想，开发一种量化专用的令牌级敏感性估计方法，将量化误差精确分解到每个输入令牌，从而实现从“模态级”到“令牌级”的细粒度量化优化。

## 核心方法与创新机理

### 从模态级到令牌级：敏感性粒度的根本转变

现有LVLM训练后量化方法——包括朴素四舍五入（RTN）、基于二阶近似的GPTQ、激活感知的AWQ，以及专门面向多模态的模态平衡量化MBQ——在分配敏感性权重时，均停留在模态层面。它们隐式地假设同一模态内所有令牌对量化误差的贡献相等，仅区分视觉令牌与文本令牌的整体重要性差异。

然而，本文通过激活分布可视化（Figure 2）和量化敏感性热力图（Figure 1）揭示了一个关键事实：**量化敏感性不仅具有模态依赖性，更展现出强烈的令牌异质性**。在同一模态内部，不同令牌对量化误差的敏感程度差异显著，且这种差异随层深、子层类型和架构变化而动态演变。MBQ等模态级方法无法捕捉这种细粒度差异，导致量化误差分配失当，性能次优。

QIG的核心创新在于**将敏感性估计的粒度从模态级推进到令牌级**，通过量化感知集成梯度为每个令牌计算独立的重要性系数。这一转变直接对应方法谱系中的核心changed slot：

| 维度 | 基线方法（MBQ等） | QIG方法 |
|------|-------------------|---------|
| 敏感性估计粒度 | 模态级：统一或梯度加权的模态权重 | 令牌级：每个令牌独立的λᵢ系数 |
| 误差加权策略 | 模态内令牌等权重建 | 令牌级加权，优先保护高敏感令牌 |
| 敏感性信号来源 | 输出梯度（间接） | 量化误差归因（直接） |

### 量化感知集成梯度：专门面向量化误差的归因机制

QIG的第二个关键创新在于**归因目标的设计**。标准集成梯度（IG）衡量的是从基线输入到实际输入对模型输出的累计贡献，其归因对象是输出值本身。然而，量化任务的核心关注点并非输出的绝对值，而是**量化前后输出的差异**。

QIG将归因目标重新定义为量化误差函数 `f(x) − f(x^q)`，并以量化模型输出 `x^q` 作为基线路径起点，构建专用于量化场景的归因公式：

$$QIG(x) = (x - x^{q}) \int_{0}^{1} \frac{\partial (f(x_{\alpha}, w) - f(x_{\alpha}, w^{q}))}{\partial x_{\alpha}} d\alpha$$

这一设计使QIG能够直接回答“每个令牌对量化误差贡献了多少”这一核心问题，而非间接推断。消融实验（Table 4）证实了这一设计的必要性：以全精度输出 `f(x)` 为归因目标或使用零基线 `x'=0` 的变体，在ChartQA和VizWiz上性能均不及QIG的量化误差目标配置。这验证了**专门针对量化误差的归因设计**是性能提升的关键因素。

### IQR剪裁稳定化：抑制异常值的实用机制

令牌级敏感性估计面临一个实际挑战：部分令牌的QIG值可能极端偏离分布，直接使用会导致优化不稳定。QIG引入**基于四分位距（IQR）的剪裁策略**作为第二个changed slot，通过剪裁超出 `[Q₁−1.5·IQR, Q₃+1.5·IQR]` 范围的异常值，再归一化得到稳定的令牌重要性系数λᵢ。

消融实验（Table A1）表明，IQR剪裁在LLaVA-OneVision-7B W4A8的多个基准上一致优于无剪裁、Top5零化、Top5均值替代等变体策略。这一机制使令牌级敏感性既能捕捉细粒度差异，又避免了异常值对优化过程的干扰。

### 方法正交性与可组合性

QIG的令牌级敏感性加权机制与现有量化方法是正交的。Table 5显示，将QIG的细粒度令牌敏感性与GPTQ的二阶近似框架结合后，在LLaVA-onevision-7B W3A16上VizWiz准确率额外提升2.08%。这表明**令牌级敏感性可以作为一种通用增强模块**，叠加于不同的量化重建框架之上。

QIG 方法构建了一套从令牌级量化误差归因到细粒度通道均衡的完整训练后量化管线，其核心流程由三个顺序耦合的模块构成。

### 管线总览

整个框架以校准数据集中的多模态序列为输入，最终输出优化后的通道缩放因子 **E**，用于指导权重与激活的量化。管线的工作流如下：

1. **QIG 计算**：对量化前后的模型输出差异执行集成梯度归因，为序列中每个令牌生成一个标量化的敏感性评分。
2. **IQR 剪裁与归一化**：对原始 QIG 值进行四分位距剪裁以抑制异常值，随后归一化得到令牌重要性系数 λ_i。
3. **令牌加权通道均衡**：将 λ_i 融入通道均衡的目标函数，在优化缩放因子时使高敏感令牌的重建误差获得更大惩罚权重。

Figure 3 直观对比了模态级均衡（如 MBQ）与本文细粒度均衡的差异：前者对同一模态内所有令牌赋予统一权重，后者则通过 QIG 为每个令牌分配独立的重要性系数。

![[assets/figures/papers/paper_list_l751_https_arxiv_org_abs_2603_17809/figures/003_Figure_3.jpg]]
*Figure 3: Comparison between modality-balanced quantization and our fine-grained quantization. Different colors indicate token types. Unlike MBQ, which assigns modality-level sensitivity, our method computes token-level sensitivity via Quantization-aware y Integrated Gradients (QIG) during calibration, enabling more effective quantization*

### 模块间关系与数据流

三个模块之间存在严格的前馈依赖关系，上游模块的输出直接构成下游模块的输入约束。

**模块 1 → 模块 2**：QIG 计算模块输出每个令牌的原始归因向量 QIG(x)，该向量维度与令牌数 T 相同。由于原始 QIG 值存在极端离群点，直接使用会导致优化不稳定，因此送入 IQR 剪裁模块进行稳定化处理。

**模块 2 → 模块 3**：IQR 模块输出归一化后的令牌重要性系数 λ_i（满足 Σλ_i = 1），这些系数作为加权因子嵌入通道均衡的目标函数。具体而言，对于权重-激活量化场景，加权目标函数为：

$$ \mathbf{E}^{*} = \arg\min_{\mathbf{E}} \sum_{i=1}^{T} \lambda_i \left\| Q_{W}(\mathbf{W} * \mathbf{E}) Q_{X}(\mathbf{E}^{-1} * \mathbf{X}_i) - \mathbf{W}\mathbf{X}_i \right\|_{2}^{2} $$

对于仅权重量化场景，目标函数简化为：

$$ \mathbf{E}^{*} = \arg\min_{\mathbf{E}} \sum_{i=1}^{T} \lambda_i \left\| Q_{W}(\mathbf{W} * \mathbf{E}) (\mathbf{E}^{-1} * \mathbf{X}_i) - \mathbf{W}\mathbf{X}_i \right\|_{2}^{2} $$

### 关键设计决策

框架中两个关键设计直接决定了细粒度敏感性的有效性：

- **归因目标的选择**：QIG 以量化前后输出差异 f(x) − f(x^q) 作为归因目标，而非直接对输出值归因。消融实验（Table 4）证实，这一专门针对量化误差的设计在 ChartQA 和 VizWiz 上均优于使用全精度输出作为目标的 IG 变体。
- **敏感性稳定化策略**：IQR 剪裁（基于 Q_1 − 1.5·IQR 和 Q_3 + 1.5·IQR 的边界）在多个基准上一致优于无剪裁、Top-5 zeroing 和 Top-5 averaging 等替代方案（Table A1），表明鲁棒的异常值抑制对令牌级加权至关重要。

### 计算开销

整个管线在校准阶段引入的额外计算开销极小。据 Table 6 报告，在单张 A800 80GB GPU 上，细粒度量化的总耗时与 MBQ 等基线方法相比几乎无增加，这得益于 QIG 计算仅需沿插值路径采样有限步数（默认 32 步）即可完成归因估计。

### 3.1 通道均衡基础：CWE目标

权重-激活量化的通道均衡（Channel-wise Equalization, CWE）通过优化通道缩放因子 $\mathbf{E}$ 来最小化量化输出与原始输出之间的均方误差。其基础目标函数为：

$$\mathbf{E}^{*} = \underset{\mathbf{E}}{\arg\min} \left\| Q_{W}(\mathbf{W} * \mathbf{E}) Q_{\mathcal{X}}(\mathbf{E}^{-1} * \mathbf{X}) - \mathbf{W}\mathbf{X} \right\|_{2}^{2}$$

其中 $\mathbf{W}$ 为权重矩阵，$\mathbf{X}$ 为输入激活，$Q_W(\cdot)$ 和 $Q_{\mathcal{X}}(\cdot)$ 分别为权重和激活的量化函数。该目标在块级别上搜索最优的通道缩放因子，以平衡权重和激活的量化误差。

### 3.2 量化感知集成梯度：QIG

标准集成梯度（Integrated Gradients）衡量输入从基线到实际值的累积贡献：

$$IG(x) = (x - x') \int_{0}^{1} \frac{\partial f(x_{\alpha}, w)}{\partial x_{\alpha}} d\alpha$$

本文提出**量化感知集成梯度（Quantization-aware Integrated Gradients, QIG）**，将归因目标从模型输出本身改为量化前后输出的差异。具体而言，QIG以量化后的输入 $x^q$ 作为基线，以原始输入 $x$ 作为目标，计算每个令牌对量化误差 $f(x) - f(x^q)$ 的贡献：

$$QIG(x) = (x - x^{q}) \int_{0}^{1} \frac{\partial \left( f(x_{\alpha}, w) - f(x_{\alpha}, w^{q}) \right)}{\partial x_{\alpha}} d\alpha$$

其中 $w$ 为全精度权重，$w^q$ 为量化权重。该公式的核心设计在于：归因目标 $f(x) - f(x^q)$ 直接捕获了量化引入的输出差异，使得QIG向量能够逐令牌量化“恢复该令牌对缩小量化误差的贡献”。

### 3.3 令牌重要性系数：IQR剪裁与归一化

原始QIG值存在极端异常值，直接使用会引入噪声。本文采用**四分位距（IQR）剪裁**进行稳定化：

$$C(QIG_i) = \mathrm{clip}(QIG_i, Q_1 - 1.5 \cdot IQR, Q_3 + 1.5 \cdot IQR)$$

其中 $Q_1$、$Q_3$ 分别为第一、第三四分位数，$IQR = Q_3 - Q_1$。剪裁后的值经归一化得到令牌重要性系数 $\lambda_i$：

$$\lambda_i = \frac{C(QIG_i)}{\sum_{j=1}^{T} C(QIG_j)}$$

$\lambda_i$ 满足 $\sum_i \lambda_i = 1$，直接作为后续优化中每个令牌的重建误差权重。

### 3.4 令牌加权通道均衡：Token-weighted CWE

将令牌重要性系数 $\lambda_i$ 嵌入CWE目标，得到**令牌加权通道均衡**。对于权重-激活量化（WA quantization）：

$$\mathbf{E}^{*} = \arg\min_{\mathbf{E}} \sum_{i=1}^{T} \lambda_i \left\| Q_{W}(\mathbf{W} * \mathbf{E}) Q_{X}(\mathbf{E}^{-1} * \mathbf{X}_i) - \mathbf{W}\mathbf{X}_i \right\|_{2}^{2}$$

对于仅权重量化（weight-only quantization），激活不参与量化，目标简化为：

$$\mathbf{E}^{*} = \arg\min_{\mathbf{E}} \sum_{i=1}^{T} \lambda_i \left\| Q_{W}(\mathbf{W} * \mathbf{E}) (\mathbf{E}^{-1} * \mathbf{X}_i) - \mathbf{W}\mathbf{X}_i \right\|_{2}^{2}$$

在这两个目标中，$\lambda_i$ 使得优化过程对高敏感性令牌的重建误差施加更大惩罚，从而在通道缩放因子的搜索中优先保护关键令牌的量化精度。这一机制将敏感性建模的粒度从模态级别细化到令牌级别。

![[assets/figures/papers/paper_list_l751_https_arxiv_org_abs_2603_17809/figures/002_Figure_2.jpg]]
*Figure 2: Visualization of activation distributions in InternVL2-8B during calibration. We visualize two representative layers and four linear sub-layers. In each panel, the horizontal axis denotes token positions in the multimodal sequence and the vertical axis indexes hidden channels; color encodes the average activation magnitude per token–channel pair over the calibration set. The plots reveal four recurring phenomena: massive activations, layer heterogeneity, sub-layer divergence, and token variability. These patterns indicate that coarse modality-level sensitivity modeling is insufficient, motivating our token-level sensitivity weighting*

## 实验与关键发现

### 核心发现：令牌级敏感性归因的有效性

实验首先验证了细粒度令牌级敏感性估计策略相较于传统模态级方法的优势。在InternVL2-8B的W4A8量化设置下，于VizWiz基准上系统比较了多种敏感性估计策略（Table 1）。结果表明，基于扰动的令牌级敏感性方法（Perturbation-based）取得了57.72%的最高准确率，显著优于模态级梯度加权方法的57.36%。值得注意的是，直接使用梯度幅值作为令牌级权重（Token-level Gradient-based）反而导致性能下降至55.78%，说明简单的梯度范数无法准确反映量化误差对每个令牌的差异化影响。基于注意力分数的方法（Attention-based）虽有一定提升（57.12%），但增益有限且不稳定。这一对比直接验证了核心瓶颈：**现有LVLM量化方法仅在模态层面分配敏感性权重，忽略了同一模态内不同令牌的异质性**，而QIG通过量化感知的集成梯度归因，能够精确捕获这种令牌级差异。

![[assets/figures/papers/paper_list_l751_https_arxiv_org_abs_2603_17809/figures/004_Table_1.jpg]]
*Table 1: Comparison of modality-level and token-level sensitivity estimation strategies on VizWiz (W4A8, InternVL2-8B)*

### 主实验结果：跨模型与跨比特位宽的全面优势

在三个代表性LVLM（LLaVA-onevision-7B、Qwen2-VL-7B、InternVL2-8B）上，QIG在W3A16（仅权重量化）和W4A8（权重-激活量化）两种设置下均取得最优平均准确率（Table 2）。以LLaVA-onevision-7B的W3A16设置为例，QIG的平均准确率达到72.04%，比最强的模态平衡基线MBQ（70.44%）提升**1.60个百分点**，将量化模型与全精度模型（73.37%）的性能差距缩小至仅**1.33%**。在Qwen2-VL-7B上，QIG同样以72.31%的平均准确率领先MBQ（71.08%）。在InternVL2-8B的W4A8设置下，QIG在VizWiz上取得58.33%，较MBQ提升0.97个百分点。

![[assets/figures/papers/paper_list_l751_https_arxiv_org_abs_2603_17809/figures/005_Table_2.jpg]]
*Table 2: Overall comparison of full-precision and post-training quantization methods on three representative LVLMs under W3A16 and W4A8. RTN and SQ are naive PTQ baselines, MBQ is the modality-balanced baseline, and QIG is the proposed fine-grained quantization method. Bold numbers indicate the best performance, and underlined numbers indicate the second best in each column*

为验证方法的可扩展性，进一步在更大规模的InternVL2-26B上进行实验（Table 3）。在W4A8设置下，QIG在ChartQA上达到85.24%，较MBQ提升0.80个百分点，表明令牌级敏感性加权策略能够有效迁移至更大模型，且性能增益保持稳定。

![[assets/figures/papers/paper_list_l751_https_arxiv_org_abs_2603_17809/figures/006_Table_3.jpg]]
*Table 3: Quantization on InternVL2-26B: MBQ vs. Ours under W3A16/W4A8*

### 消融实验：QIG配置与稳定性策略的关键作用

**QIG归因目标的选择**对最终性能至关重要（Table 4）。实验比较了不同基线输入和归因目标函数的组合。使用量化输入$x^q$作为基线、以量化误差$f(x) - f(x^q)$为归因目标的配置，在ChartQA和VizWiz上均取得最佳性能。这一结果验证了核心设计直觉：**QIG专门针对量化误差进行归因，而非泛化地归因模型输出**，使得令牌重要性系数$\lambda_i$能够直接反映每个令牌对量化退化的贡献程度。

**IQR剪裁策略**是稳定敏感性估计的关键环节（Table A1）。在LLaVA-OneVision-7B的W4A8量化下，比较了无剪裁、Top5置零、Top5取均值等变体，IQR剪裁在多个基准上取得一致最优。该策略利用四分位距（$Q_1 - 1.5 \cdot IQR$至$Q_3 + 1.5 \cdot IQR$）抑制极端QIG值，有效防止少数离群令牌主导误差加权，从而保证了跨层和跨令牌的均衡优化。

### 正交性与效率分析

QIG的令牌级敏感性加权策略与现有量化方法是正交的，可叠加使用（Table 5）。将细粒度令牌敏感性与GPTQ结合后，在LLaVA-onevision-7B的W3A16设置下，VizWiz准确率进一步提升2.08%，证明该方法可以作为插件式模块增强现有量化框架。

在计算效率方面（Table 6），QIG的量化时间开销与MBQ等基线方法相当，在单张A800 80GB GPU上仅增加可忽略的额外耗时。这得益于QIG计算仅在校准阶段执行一次，且集成梯度的数值积分步长（默认32步）已在精度与效率之间取得平衡。

### 失败模式与局限分析

尽管QIG在多数场景下表现优异，但实验也揭示了若干值得关注的边界情况。在部分文本密集的基准（如DocVQA）上，令牌级加权带来的增益相对较小，可能原因在于文本令牌间的敏感性差异不如视觉令牌显著。此外，当校准数据分布与测试场景存在较大偏移时（如附录Table A3所示的OCR特定校准实验），QIG的鲁棒性虽优于MBQ，但仍存在一定性能波动，提示**校准数据的选择对令牌敏感性的泛化能力有直接影响**。当前方法尚未探索自适应校准策略，这构成了一个开放问题。

综合来看，QIG通过将量化误差归因细化为令牌级粒度，有效解决了模态级方法的关键瓶颈，在多个LVLM和量化配置下取得一致且显著的性能提升，同时保持了计算效率。

![[assets/figures/papers/paper_list_l751_https_arxiv_org_abs_2603_17809/figures/007_Table_4.jpg]]
*Table 4: Ablation of the integrated-gradients configuration for token-wise sensitivities, varying the reference baseline*

## 定位与知识库关联

### 1. 基线谱系与差异化定位

本文提出的QIG方法根植于**训练后量化（PTQ）** 技术栈，其核心贡献在于将敏感性建模的粒度从模态级推进至令牌级。为清晰定位其创新边界，我们将相关基线分为三个层次：

**第一层：通用PTQ基线。** 最朴素的**RTN**（Round-to-Nearest）直接对权重进行四舍五入取整，完全不考虑任何敏感性差异。**GPTQ**引入基于Hessian矩阵的二阶近似来逐层优化权重量化，但仅适用于仅权重量化场景，且未考虑多模态输入的异质性。**AWQ**通过观察激活值中的显著通道来保护关键权重，但其敏感性信号仍基于激活幅值的启发式统计。**SmoothQuant（SQ）** 通过数学上等价的通道级缩放变换，将激活量化难度向权重迁移，解决了权重-激活联合量化的范围不匹配问题，但其缩放因子搜索同样对所有令牌一视同仁。这些方法在设计时均以纯文本LLM为目标，缺乏对多模态序列中令牌异质性的显式建模。

**第二层：模态感知LVLM量化基线。** **MBQ**（Modality-Balanced Quantization）是目前最具代表性的LVLM专用PTQ方法。它首次识别出视觉令牌与文本令牌在量化敏感性上的模态级差异，并通过梯度幅度对两类模态的重建误差施加不同权重。然而，MBQ的敏感性建模止步于模态层面——它隐含地假设同一模态内的所有令牌具有相等的量化敏感性。本文通过Figure 1和Figure 2的系统性可视化，揭示了这一假设的脆弱性：即使在视觉令牌内部，不同空间位置的令牌敏感性也存在数量级差异；文本令牌中，承载问题核心语义的令牌远比其他填充令牌敏感。**QIG正是在MBQ的模态平衡框架之上，将敏感性权重从模态级（两类权重）推进至令牌级（每个令牌一个权重），实现了细粒度的误差分配。**

**第三层：归因方法的引入。** 将归因技术引入量化领域是本文的方法论创新。传统敏感性估计依赖梯度幅值（Gradient-based）或注意力权重（Attention-based），但Table 1的消融实验表明，直接使用梯度加权甚至劣于模态级方法（55.78% vs. 57.36%），注意力加权仅带来微弱且不稳定的增益（57.12% vs. 56.43%）。这揭示了一个关键洞察：**量化误差的令牌级贡献不能简单用前向传播中的激活或梯度大小来近似，而需要专门针对“量化前后输出差异”进行归因。** QIG通过将集成梯度的基线设为量化输入$x^q$、目标函数设为全精度与量化模型输出之差$f(x)-f(x^q)$，构建了一个直接回答“恢复每个令牌对缩小量化误差有多大贡献”的归因信号。这种**量化感知**的归因设计，是其区别于通用可解释性工具的核心所在。

### 2. 方法适用边界

QIG的设计使其在以下条件下表现最优，但也存在明确的适用边界：

- **模型架构兼容性。** 方法在LLaVA-onevision-7B、Qwen2-VL-7B、InternVL2-8B和InternVL2-26B四个代表性LVLM上验证有效，覆盖了不同的视觉编码器（ViT、InternViT）和语言解码器架构。这表明QIG对主流LVLM架构具有良好的泛化性，但其对非Transformer视觉骨干（如CNN-based）或多模态早期融合架构的适用性尚未验证。

- **量化比特宽度。** 实验覆盖了W3A16（3-bit仅权重）和W4A8（4-bit权重/8-bit激活）两种配置。在W3A16的极限压缩下，QIG将LLaVA-onevision-7B与全精度模型的平均准确率差距缩小至1.33%，展现出在低比特场景下的显著价值。然而，更低比特（如2-bit）的量化场景尚未探索，此时量化误差的非线性急剧增加可能使令牌敏感性估计本身变得不稳定。

- **校准数据依赖性。** QIG的令牌敏感性评分依赖于校准数据集上的集成梯度计算。论文未深入探讨校准数据分布对敏感性估计泛化性的影响——若校准时域与推理时域存在显著分布偏移，令牌重要性的排序是否保持稳定，这是一个待验证的开放问题。

- **计算开销可控。** Table 6显示，QIG的量化时间开销与MBQ等基线方法相比几乎可忽略（在单张A800 80GB GPU上），这得益于集成梯度计算仅在校准阶段执行一次。但集成梯度的步长（默认32步）是精度-效率的权衡参数，其动态调整策略尚未被探索。

### 3. 局限性与开放问题

尽管QIG在多个基准上取得了显著提升，但以下问题值得进一步研究：

1. **极低比特量化的稳定性。** 当量化比特降至2-bit或更低时，量化误差的量级和分布会发生质变。QIG的令牌敏感性评分是否仍能保持对误差贡献的准确排序，IQR剪裁策略是否足以抑制极端值，需要专门的实验验证。

2. **校准策略的自适应化。** 当前方法固定使用一组校准数据计算全局令牌重要性。是否存在一种自适应策略，根据输入样本动态调整令牌权重，从而在分布外场景下保持鲁棒性？

3. **长序列与视频扩展。** 论文聚焦于静态图像-文本多模态任务。当序列长度急剧增加（如视频理解中的数百帧）时，集成梯度的计算开销和归因质量是否会退化，令牌敏感性的稀疏化策略是否必要？

4. **归因步长的动态调节。** 集成梯度的近似精度与步数正相关。是否可以根据每层量化误差的幅度动态分配步数，在保持归因质量的同时进一步降低校准开销？

5. **与量化训练的融合潜力。** QIG当前定位于训练后量化。其令牌级敏感性信号是否可以作为量化感知训练（QAT）中的正则化项或权重，引导训练过程更精细地保护关键令牌的表示能力，是一个值得探索的方向。

## 原文 PDF

![[paperPDFs/CVPR_2026/Fine_Grained_Post_Training_Quantization_for_Large_Vision_Language_Models_with_Quantization_Aware_Integrated_Gradients.pdf]]
