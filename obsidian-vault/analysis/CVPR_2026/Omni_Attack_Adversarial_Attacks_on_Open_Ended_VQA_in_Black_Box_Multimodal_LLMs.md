---
title: "Omni-Attack: Adversarial Attacks on Open-Ended VQA in Black-Box Multimodal LLMs"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Omni_Attack_Adversarial_Attacks_on_Open_Ended_VQA_in_Black_Box_Multimodal_LLMs.pdf
project_link: null
code_link: "https://github.com/hukkai/transferable_mllm_attack"
aliases:
- OA
- Omni-Attack
tags:
- CVPR_2026
- topic/other_unclear
- topic/other_unclear/general
core_operator: 通过LLM推理生成问题条件的文本和视觉目标，以及针对OCR的位置感知局部扰动，为对抗优化提供更强的监督信号。
primary_logic: 利用多模态LLM的推理能力将问题转化为具体的想象图像描述，并通过文本到图像模型生成视觉目标，配合多目标集成和位置感知，可以大幅提升黑盒对抗攻击的迁移性。
claims:
- Omni-Attack在GPT-4.1上达到71.8%的定向攻击成功率（ε=8/255），显著优于先前方法。
- 目标构造消融实验显示问题条件的文本和视觉目标显著提升性能，且多目标集成优于单一目标。
- DropPath和扰动EMA正则化对提升Claude系列的鲁棒性攻击至关重要。
- AdvRobustBench (MMBench split) 上 ASR (%) = 71.8
---

# Omni-Attack: Adversarial Attacks on Open-Ended VQA in Black-Box Multimodal LLMs

> [!tip] 核心洞察
> 利用多模态LLM的推理能力将问题转化为具体的想象图像描述，并通过文本到图像模型生成视觉目标，配合多目标集成和位置感知，可以大幅提升黑盒对抗攻击的迁移性。

| 字段 | 内容 |
|------|------|
| 中文题名 | Omni-Attack：面向开放域视觉问答的黑盒多模态大模型对抗攻击 |
| 英文题名 | Omni-Attack: Adversarial Attacks on Open-Ended VQA in Black-Box Multimodal LLMs |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Hu_Omni-Attack_Adversarial_Attacks_on_Open-Ended_VQA_in_Black-Box_Multimodal_LLMs_CVPR_2026_paper.html) · [Code](https://github.com/hukkai/transferable_mllm_attack) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | Omni-Attack |
| Dataset | AdvRobustBench, NIPS2017 Split |

> [!tip] 效果简介
> - AdvRobustBench (MMBench split) 上，ASR (%) 71.8；ASR (%) 80.1。
> - AdvRobustBench (OCRBench-v2 split) 上，ASR (%) 25.3。
> - NIPS2017 Split 上，Targeted Success Rate (%) 81.2。

## 概要

多模态大模型（MLLMs）在开放域视觉问答（VQA）中展现出强大能力，但其安全性尚未充分评估。现有黑盒对抗攻击方法在开放域问答场景下面临两个核心瓶颈：其一，缺乏有效的问题条件目标信号，导致复杂推理任务的攻击成功率低下；其二，OCR任务需要细粒度空间控制，而全局扰动方法难以精准影响文本识别区域。

Omni-Attack 针对上述瓶颈提出了一套系统的解决方案。其核心洞察在于：利用多模态LLM的推理能力将攻击目标问题转化为具体的“想象图像”描述，再通过文本到图像模型生成视觉目标，从而为对抗优化提供更强的监督信号。方法上，Omni-Attack 引入三个关键改进：**目标构造流水线**——使用LLM生成问题条件的文本目标，配合文本到图像模型生成视觉目标，并通过循环验证和多目标集成提升目标质量；**位置感知OCR流水线**——利用PaddleOCR检测文本区域，将OCR攻击简化为局部VQA攻击；**迁移性增强正则化**——采用DropPath、PatchDrop、扰动EMA和随机JPEG压缩等技巧，显著提升对抗样本在黑盒模型间的迁移性。

实验结果表明，Omni-Attack 在 AdvRobustBench 基准上达到 71.8% 的定向攻击成功率（GPT-4.1，ε=8/255），在 ε=16/255 时进一步提升至 80.1%，显著优于先前方法。消融实验证实，问题条件的文本与视觉目标、多目标集成、循环验证以及正则化策略各自对性能均有显著贡献，其中 DropPath 和扰动 EMA 对攻击 Claude 系列模型至关重要。

多模态大语言模型（MLLM）在视觉问答（VQA）等任务上展现出强大的能力，但其对抗鲁棒性正成为安全部署的关键瓶颈。针对MLLM的黑盒对抗攻击中，**基于迁移的攻击**因无需访问目标模型内部参数而具有实际威胁——攻击者利用白盒代理模型生成对抗样本，再将其迁移至黑盒受害者模型。然而，现有工作在开放域问答场景下面临两个根本性缺口：

**缺口一：缺乏问题条件的优化目标。** 现有方法通常直接使用目标选项文本（如**Attack-VLM**，Zhao et al., NeurIPS 2023）或随机选取的图像（如**M-Attack**，Li et al., arXiv 2025）作为攻击目标。这种与问题语义脱节的目标信号导致优化方向模糊，尤其在需要复杂推理的任务上，攻击成功率显著受限。

**缺口二：OCR任务缺乏空间感知。** 文本识别类VQA需要对图像中的文字区域进行精确操控，但现有方法对整个图像施加全局扰动，无法针对性地干扰与问题相关的文本区域，导致OCR攻击效果薄弱。

**核心洞察**在于：多模态LLM本身具备强大的推理与生成能力，可以被反向利用来构造更有效的攻击目标。具体而言，利用LLM将问题转化为具体的“想象图像”文本描述，再通过文本到图像模型生成视觉目标，配合多目标集成优化，能够为对抗优化提供远强于传统方法的监督信号。同时，针对OCR任务引入位置感知的局部扰动，可将OCR攻击简化为局部VQA攻击。

基于上述洞察，本文提出**Omni-Attack**，一种面向开放域VQA的黑盒迁移攻击方法，通过问题条件的目标构造、位置感知的OCR攻击和迁移性增强正则化，系统性地提升了复杂推理与文本识别场景下的攻击成功率。在GPT-4.1上，Omni-Attack在ε=8/255的扰动预算下达到71.8%的定向攻击成功率，显著优于先前方法。

## 核心方法与创新机理

Omni-Attack 的核心突破在于**为黑盒迁移攻击注入了问题条件的语义监督信号**，从而解决了开放域 VQA 场景下目标信号缺失的根本瓶颈。与先前方法直接使用目标选项文本或随机图像作为攻击目标不同，Omni-Attack 通过三个相互协同的创新模块，实现了攻击效能的跨越式提升。

### 问题条件的多模态目标构造

传统迁移攻击（如 **Attack-VLM** (Zhao et al., NeurIPS 2023) 使用 CLIP 相似度作为目标、**AnyAttack** (Zhang et al., arXiv 2024) 使用大规模生成器产生目标文本）在开放域 VQA 场景下存在致命缺陷：**攻击目标与具体问题脱节**，导致优化信号缺乏针对性。Omni-Attack 提出了一套完整的目标构造流水线，将多模态 LLM 的推理能力转化为攻击监督信号：

1. **文本目标生成**：利用 LLM 根据问题和目标选项进行反向推理——"想象如果目标选项是正确答案，图像应该是什么样的"——生成问题条件的图像描述文本 $x_{\mathrm{T}}$。
2. **视觉目标生成**：通过文本到图像模型（Qwen-Image）将文本目标转化为对应的视觉目标 $x_{\mathrm{V}}$，为 CLIP 代理模型提供视觉空间的监督锚点。
3. **循环验证与多目标集成**：引入循环验证机制滤除次优目标，并通过多目标集成（约 5 个目标达到收益饱和）将对抗优化目标扩展为：

$$\delta^{*} = \underset{\|\delta\|_{p} \leq \epsilon}{\mathrm{argmin}} -\sum_{i=1}^{n} \sum_{j=1}^{M} \log\big(p_{i}^{(j)}\big)$$

其中 $p_{i}^{(j)}$ 为对抗图像与第 $j$ 个目标文本的 softmax 归一化相似度，鼓励对抗样本同时向多个语义一致的目标靠拢。消融实验表明，**融合文本和视觉监督可进一步提升攻击成功率**，且循环验证带来一致性增益。

### 位置感知的 OCR 对抗攻击

OCR 任务对扰动空间位置高度敏感，全局扰动会破坏文本区域的细粒度特征。Omni-Attack 创新性地将 OCR 攻击**简化为局部 VQA 问题**：

- 使用 PaddleOCR 检测图像中的文本区域边界框。
- 根据问题定位相关边界框，**仅优化问题相关区域的对抗扰动**。
- 将局部 OCR 问题转化为该区域上的通用 VQA 攻击，复用目标构造流水线。

这一设计使 Omni-Attack 在 OCRBench-v2 分割上对 Qwen3-VL30B 达到 25.3% 的 ASR（$\epsilon=8/255$），突破了先前方法在文本识别任务上的瓶颈。

### 迁移性增强正则化体系

针对黑盒迁移场景中的代理模型过拟合问题，Omni-Attack 引入了一套专门适配对抗优化的正则化技术：

- **DropPath**：在优化过程中按深度比例随机跳过残差块，减少对特定代理模型架构的过拟合：

$$x_{i+1} = \begin{cases} \operatorname{block}_i(x_i), & \text{if } \operatorname{Uniform}(0,1) > (i/L)p, \\ x_i, & \text{otherwise}. \end{cases}$$

- **扰动 EMA**：对扰动进行指数移动平均 $\delta^{\mathrm{EMA}} \gets 0.99 \delta^{\mathrm{EMA}} + 0.01 \delta$，产生更平滑、迁移性更强的扰动。
- **随机 JPEG 压缩**：在优化过程中以随机质量进行可微 JPEG 压缩，使对抗样本与真实世界的图像处理分布对齐。

正则化分解实验揭示了这些技术的**非对称重要性**：对于 Claude 系列模型，移除 DropPath 或扰动 EMA 后 ASR 骤降至 11.1%（Table 5），证明这些正则化是突破高鲁棒性模型的关键。相比之下，代理模型数量的增加（从 3 个 CLIP 模型扩展到 6 个）并未带来显著收益，表明**正则化策略比代理模型规模更重要**。

### 创新点的协同效应

三个创新模块并非孤立运作。目标构造流水线提供了问题语义层面的监督信号，位置感知机制确保了 OCR 场景下的空间精度，而正则化体系则保障了这些信号在黑盒迁移过程中的有效性。这种**语义监督-空间控制-迁移保障**的三层协同，使 Omni-Attack 在 GPT-4.1 上达到 71.8% 的定向攻击成功率（$\epsilon=8/255$），显著超越先前方法。

Omni-Attack 围绕一个核心洞察构建：现有黑盒对抗攻击在开放域 VQA 场景下缺乏有效的问题条件目标信号，导致复杂推理和文本识别任务上的攻击成功率低。为此，Omni-Attack 将攻击过程组织为三个协同模块，形成从目标构造到扰动优化再到迁移性增强的完整流水线。

### 输入输出流

攻击的输入包括：一张干净图像 $x$、一个开放域问题 $Q$ 及其选项集合，以及一个选定的错误目标选项。输出为对抗图像 $x_{\delta} = x + \delta$，满足 $\|\delta\|_p \leq \epsilon$ 的扰动预算约束，使得黑盒受害多模态大模型在给定 $x_{\delta}$ 和 $Q$ 时输出目标选项。

### 三阶段流水线

**第一阶段：目标构造流水线**（Section 4.1）。该模块将问题条件转化为具体的优化监督信号。给定问题 $Q$ 和目标选项，Omni-Attack 首先调用 LLM 推理“如果目标选项是正确答案，图像应该是什么样”，生成问题条件的文本描述 $x_{\mathrm{T}}$。随后通过文本到图像模型（Qwen-Image）将文本描述转化为视觉目标图像 $x_{\mathrm{G}}$。为滤除次优目标，引入循环验证机制：将生成的视觉目标图像反馈给 MLLM 重新回答原问题，仅保留能正确导向目标选项的样本。最终通过多目标集成，生成 $M$ 组 $x_{\mathrm{T}}^{(j)}$ 与 $x_{\mathrm{G}}^{(j)}$，为后续优化提供丰富的监督信号。

**第二阶段：位置感知 OCR 流水线**（Section 4.2）。针对 OCR 任务中文本区域需要细粒度空间控制的挑战，Omni-Attack 使用 PaddleOCR 检测图像中的文本边界框，并定位与问题相关的区域。通过将对抗扰动优化限制在这些局部边界框内，该方法将原本需要精确操纵文本的 OCR 攻击简化为局部区域的通用 VQA 攻击，从而复用目标构造流水线生成的监督信号。

**第三阶段：迁移性增强正则化**（Section 4.3）。在对抗优化过程中，Omni-Attack 采用代理模型集成策略——默认使用三个 CLIP 家族模型——并引入多项正则化技巧以提升对抗样本在黑盒模型间的迁移性。具体包括：
- **DropPath**：按深度比例随机跳过残差块，减少对特定代理模型架构的过拟合；
- **PatchDrop**：随机丢弃图像块，增强扰动的空间泛化性；
- **扰动 EMA**：对扰动进行指数移动平均，产生更平滑的扰动模式；
- **随机 JPEG 压缩**：在优化过程中以随机质量进行可微 JPEG 压缩，使对抗样本与真实传输场景的退化分布对齐。

### 优化目标

整个流水线的优化目标可表述为多目标集成下的最小化问题。令 $S_i(\cdot, \cdot)$ 表示第 $i$ 个代理模型的相似度函数，对抗扰动 $\delta$ 的优化目标为：

$$\delta^{*} = \underset{\|\delta\|_{p} \leq \epsilon}{\mathrm{argmin}} -\sum_{i=1}^{n} \sum_{j=1}^{M} \log\big(p_{i}^{(j)}\big)$$

其中 $p_{i}^{(j)}$ 是第 $i$ 个代理模型下对抗图像与第 $j$ 个目标文本的 softmax 归一化相似度：

$$p_{i}^{(j)} = \frac{\exp\bigl(\mathrm{S}_{i}(x_{\delta}, x_{\mathrm{T}}^{(j)})\bigr)}{\sum_{k=1}^{M} \bigl[ \exp\bigl(\mathrm{S}_{i}(x_{\delta}, x_{\mathrm{T}}^{(k)})\bigr) + \exp\bigl(\mathrm{S}_{i}(x_{\delta}, x_{\mathrm{G}}^{(k)})\bigr) \bigr]}$$

该目标鼓励对抗图像对每个目标文本的相对相似度最大化，同时抑制与真实表示的相似度，从而驱动受害模型在推理时偏向目标选项。

### 模块间关系

三个模块形成级联依赖：目标构造流水线为优化提供监督信号，位置感知 OCR 流水线决定扰动的空间作用范围，迁移性增强正则化则贯穿整个优化过程以保障黑盒迁移能力。消融实验表明，移除去噪正则化（DropPath 或扰动 EMA）后，Claude 3.7 上的 ASR 从 15.5% 骤降至 11.1%（Table 5），验证了正则化模块对突破高鲁棒性模型的必要性。

### 问题形式化与缩放成功率

Omni-Attack 面向开放域视觉问答的黑盒定向攻击。给定干净图像 $x$、问题 $q$ 和选项集 $\mathcal{O}$，攻击者选择一个非真实选项作为目标答案 $y_t$，在 $L_p$ 范数约束 $\|\delta\|_p \leq \epsilon$ 下优化对抗扰动 $\delta$，使对抗图像 $x_\delta = x + \delta$ 输入目标多模态大模型后输出 $y_t$。

为公平评估，论文采用**缩放攻击成功率**（Scaled ASR），仅统计在干净图像上能正确回答的样本：

$$
\mathrm{ASR} = \frac{\sum_{i=1}^{N} x_i y_i}{\sum_{i=1}^{N} x_i}
$$

其中 $x_i \in \{0,1\}$ 表示第 $i$ 个样本在干净图像上是否被正确回答，$y_i \in \{0,1\}$ 表示对抗样本是否成功诱导目标输出。该指标排除了模型自身能力不足带来的混淆。

### 核心优化目标

Omni-Attack 在代理模型集合 $\{\mathrm{S}_i\}_{i=1}^n$（CLIP 家族模型）上进行迁移攻击，基础优化目标为：

$$
\delta^{*} = \underset{\|\delta\|_{p} \leq \epsilon}{\mathrm{argmin}} \sum_{i=1}^{n} \Big[ \mathrm{S}_{i}(\boldsymbol{x}_{\delta}, \boldsymbol{x}_{\mathrm{G}}) - \mathrm{S}_{i}(\boldsymbol{x}_{\delta}, \boldsymbol{x}_{\mathrm{T}}) \Big]
$$

其中 $\mathrm{S}_i(\cdot,\cdot)$ 为第 $i$ 个代理模型的相似度函数，$\boldsymbol{x}_{\mathrm{G}}$ 为真实答案的文本表示，$\boldsymbol{x}_{\mathrm{T}}$ 为目标答案的文本表示。该目标同时最小化对抗图像与真实表示的相似度、最大化与目标表示的相似度。

### 多目标集成优化

为缓解单一目标表示的不稳定性，Omni-Attack 引入多目标集成。对第 $j$ 个目标文本 $\boldsymbol{x}_{\mathrm{T}}^{(j)}$，定义 softmax 归一化得分：

$$
p_{i}^{(j)} = \frac{\exp\bigl(\mathrm{S}_{i}(x_{\delta}, x_{\mathrm{T}}^{(j)})\bigr)}{\sum_{k=1}^{M} \bigl[ \exp\bigl(\mathrm{S}_{i}(x_{\delta}, x_{\mathrm{T}}^{(k)})\bigr) + \exp\bigl(\mathrm{S}_{i}(x_{\delta}, x_{\mathrm{G}}^{(k)})\bigr) \bigr]}
$$

其中 $M$ 为目标数量，分母同时包含所有目标文本和真实文本候选。最终多目标集成优化目标为：

$$
\delta^{*} = \underset{\|\delta\|_{p} \leq \epsilon}{\mathrm{argmin}} -\sum_{i=1}^{n} \sum_{j=1}^{M} \log\big(p_{i}^{(j)}\big)
$$

该目标鼓励对抗图像对每个目标文本的相对相似度最大化，消融实验表明增加目标数量可稳步提升性能，但在约 5 个目标后收益饱和。

### 迁移性增强正则化

**DropPath 随机跳跃**：在优化过程中按深度比例随机跳过残差块，减少对特定代理模型结构的过拟合：

$$
x_{i+1} = \begin{cases} \operatorname{block}_i(x_i), & \text{if } \operatorname{Uniform}(0,1) > (i/L)p, \\ x_i, & \text{otherwise}. \end{cases}
$$

其中 $i$ 为层索引，$L$ 为总层数，$p$ 为控制跳跃概率的超参数。

**扰动指数移动平均（EMA）**：对每次迭代的扰动进行平滑，产生迁移性更强的扰动：

$$
\delta^{\mathrm{EMA}} \gets 0.99 \delta^{\mathrm{EMA}} + 0.01 \delta
$$

**随机 JPEG 压缩**：在优化过程中以随机质量进行可微 JPEG 压缩，使对抗样本对常见图像处理具有鲁棒性：

$$
x \leftarrow \operatorname{DiffJPEG}(x; \mathrm{quality} \sim \operatorname{Uniform}[0.5, 1.0])
$$

消融实验（Table 5）表明，DropPath 和扰动 EMA 对攻击 Claude 系列模型至关重要——移除后 Claude 3.7 的 ASR 骤降至 11.1%。

## 实验与关键发现

### 主实验结果

Omni-Attack 在 AdvRobustBench 基准上对多种黑盒多模态大模型进行了定向攻击评估，采用缩放攻击成功率（Scaled ASR）作为核心指标，仅统计干净图像上能正确回答的样本，排除了模型本身能力不足带来的混淆。表 1 汇总了最佳实践配置下的主结果。

在 L∞ 扰动预算 ε = 8/255 下，Omni-Attack 对 GPT-4.1 实现了 71.8% 的定向 ASR；当预算放宽至 16/255 时，该指标进一步提升至 80.1%。Gemini 2.0 和 Gemini 2.5 在 ε = 8/255 下分别达到 65.8% 和 43.3%，表明攻击对 Google 系列模型同样具有较强迁移性。值得注意的是，Claude 系列模型表现出显著更强的鲁棒性：Claude 3.5 和 Claude 3.7 在 ε = 8/255 下的 ASR 仅为 13.9% 和 15.5%，即便在 16/255 预算下也仅提升至 44.7% 和 38.1%，这揭示了 Claude 家族在对抗防御机制上的独特性，也是当前方法的主要瓶颈之一。

在 OCR 任务（OCRBench-v2 子集）上，攻击难度整体较高。Qwen3-VL30B 在 ε = 8/255 下取得 25.3% 的 ASR，为所有模型中最高；GPT-4.1 和 Gemini 2.0 的 OCR ASR 则明显低于其 VQA 表现，说明文本区域的细粒度对抗扰动仍是开放挑战。

### 与先前工作的对比

在 MMBench 子集上，Omni-Attack 与 **Attack-VLM**（Zhao et al., NeurIPS 2023）、**AnyAttack**（Zhang et al., arXiv 2024）、**M-Attack**（Li et al., arXiv 2025）、**ScalingAttack**（Liu et al., arXiv 2024）和 **SSA-CWA**（Dong et al., 2024）等方法进行了系统对比。Omni-Attack 在所有评估模型上均显著优于先前方法。以 GPT-4.1 为例，Omni-Attack 在 ε = 8/255 下达到 71.8% ASR，而表现最好的先前方法远低于此水平。这一优势在 Gemini 2.0 和 Qwen3-VL30B 上同样保持，验证了问题条件目标构造和多目标集成策略的有效性。

在 NIPS2017 数据集上，Omni-Attack 对 GPT-4.1 实现了 81.2% 的定向成功率（ε = 8/255），进一步证明了方法在不同数据分布下的泛化能力。

### 消融实验

#### 目标构造策略

目标构造流水线的消融揭示了几个关键发现。首先，**循环验证机制**能够有效滤除次优目标，在所有配置下均带来一致性增益——移除循环验证后，ASR 出现明显下降。其次，**目标数量**对性能的影响呈边际递减趋势：从单一目标增加到 5 个目标时，ASR 稳步提升，但超过 5 个后收益趋于饱和。这一饱和现象在视觉和文本特征上均被观察到，表明 5 个目标已能提供足够多样化的优化信号。最后，**融合视觉与文本监督**相比仅使用单一模态目标能进一步提升攻击成功率，验证了多模态目标互补设计的必要性。

#### 代理模型选择

代理模型消融表明，非 CLIP 模型和低分辨率 CLIP 变体不适合作为迁移攻击的代理。使用 6 个 CLIP 模型与默认的 3 个 CLIP 模型相比，ASR 几乎持平（GPT-4.1 上分别为 71.9% 和 71.8%），说明代理模型数量在达到一定阈值后不再带来明显提升。这一发现对计算效率优化具有实际指导意义——3 个精心选择的 CLIP 模型即可达到接近最优的迁移效果。

#### 正则化技术分解

正则化效果的分解实验揭示了不同技术对攻击迁移性的差异化贡献，尤其是针对 Claude 系列模型。**DropPath** 和**扰动 EMA** 被证明是最关键的两个正则化组件：当两者同时移除时，Claude 3.7 上的 ASR 从 15.5% 骤降至 11.1%。PatchDrop 和随机 JPEG 压缩也各自贡献了正向增益，但影响程度相对较小。这些结果表明，DropPath 通过随机跳过残差块减少了代理模型过拟合，而扰动 EMA 通过平滑扰动更新提升了跨模型迁移性，两者在应对 Claude 的鲁棒防御时尤为关键。

### 失败模式与局限性

尽管 Omni-Attack 在多数模型上取得了领先性能，但仍存在明确的失败模式：

1. **Claude 鲁棒性瓶颈**：Claude 3.5/3.7 在 ε = 8/255 下的 ASR 仅约 15%，远低于其他商用模型。即便引入全套正则化技术，提升幅度仍然有限，表明 Claude 可能采用了独特的对抗防御或安全对齐机制，现有基于 CLIP 代理的迁移策略对其穿透力不足。

2. **OCR 任务低成功率**：OCR 子集上的 ASR 普遍偏低，即使表现最好的 Qwen3-VL30B 也仅达 25.3%。位置感知流水线虽将 OCR 攻击简化为局部 VQA 问题，但文本区域的细粒度扰动仍难以在保持语义一致性的同时有效欺骗 OCR 能力较强的模型。

3. **目标质量依赖性**：目标构造流水线的效果受限于底层 LLM 和文本到图像模型的生成能力，可能引入与问题语义不完全对齐的次优目标，影响攻击稳定性。

4. **代理模型生态局限**：攻击迁移性主要集中在 CLIP 家族模型上，对非 CLIP 架构的代理模型迁移效果有限，限制了方法的通用性。

### 评估公平性保障

实验设计采用了多项措施确保评估的公平性与可靠性：

- **缩放 ASR 指标**：仅计算干净样本上能正确回答的案例，避免将模型本身的能力缺陷误判为攻击成功，使不同方法间的比较更加公平。
- **OCR 评估验证**：OCR 任务采用 LLM-as-judge 进行自动评判，并经过人工验证，精确率达 99%、召回率 97.5%，确保了评估结果的可靠性。
- **多次运行取平均**：每个对抗样本在三次独立运行中评估，对结果取平均，以处理多模态 LLM 输出的非确定性。

![[assets/figures/papers/paper_list_l770_https_openaccess_thecvf_com_content_CVPR2026_html_Hu_Omni_Attack_Adversa/figures/003_Table_1.jpg]]
*Table 1: Performance of Omni-Attack best practices in ASR (%) on AdvRobustBench. Attack performed in a black-box targeted manner. Test examples that the victim LLM cannot resolve correctly with clean images are excluded in the computation of ASR*

![[assets/figures/papers/paper_list_l770_https_openaccess_thecvf_com_content_CVPR2026_html_Hu_Omni_Attack_Adversa/figures/004_Table_2.jpg]]
*Table 2: Comparison with prior work on the MMBench split*

![[assets/figures/papers/paper_list_l770_https_openaccess_thecvf_com_content_CVPR2026_html_Hu_Omni_Attack_Adversa/figures/006_Table_6.jpg]]
*Table 6: Comparison with prior work on the NIPS2017 Split*

![[assets/figures/papers/paper_list_l770_https_openaccess_thecvf_com_content_CVPR2026_html_Hu_Omni_Attack_Adversa/figures/007_Table_4.jpg]]
*Table 4: ASR (%) under different target constructions at*

![[assets/figures/papers/paper_list_l770_https_openaccess_thecvf_com_content_CVPR2026_html_Hu_Omni_Attack_Adversa/figures/009_Table_5.jpg]]
*Table 5: Breakdown of regularization effects at*

![[assets/figures/papers/paper_list_l770_https_openaccess_thecvf_com_content_CVPR2026_html_Hu_Omni_Attack_Adversa/figures/008_Table_7.jpg]]
*Table 7: Comparison on non-CLIP models*

## 定位与知识库关联

### 1. 与现有方法的逻辑关系

Omni-Attack 属于**基于迁移的黑盒对抗攻击**范式，其核心改进围绕三个瓶颈展开：目标信号的语义条件化、OCR 任务的空间精细化、以及对抗样本的跨模型迁移性。以下从这三个维度梳理其与基线工作的关系。

**目标表示维度。** 早期方法如 **Attack-VLM** (Zhao et al., NeurIPS 2023) 直接使用 CLIP 相似度作为优化目标，**M-Attack** (Li et al., arXiv 2025) 则采用随机图像作为目标并结合关键词匹配。这些方法的目标信号与具体问题脱节，缺乏语义条件化，导致在开放域 VQA 的复杂推理场景中攻击成功率受限。**AnyAttack** (Zhang et al., arXiv 2024) 虽然引入了大规模生成器产生目标文本，但其目标构造未针对问题进行条件化。Omni-Attack 的关键推进在于：利用多模态 LLM 的推理能力，将问题转化为“想象图像”的描述，再通过文本到图像模型生成对应的视觉目标，从而建立**问题条件的文本-视觉双重监督**。这一设计使得对抗优化不再盲目地向任意错误答案靠拢，而是向一个与问题语义一致的、具体的错误表征收敛。

**OCR 攻击维度。** 现有方法通常对整个图像施加均匀扰动，忽略了 OCR 任务中文本区域的空间局部性。Omni-Attack 引入 PaddleOCR 检测文本区域，并仅优化与问题相关的局部边界框，将 OCR 对抗攻击**简化为局部 VQA 攻击**。这一策略在方法论上将 OCR 任务从全局扰动范式中解耦，是当前黑盒攻击文献中较少被明确建模的设计。

**迁移性增强维度。** 标准对抗优化（如 PGD）在代理模型上容易过拟合，导致黑盒迁移性不足。**ScalingAttack** (Liu et al., arXiv 2024) 从缩放法则角度研究对抗攻击，**SSA-CWA** (Dong et al., 2024) 则基于目标提及进行攻击。Omni-Attack 的独特贡献在于将 DropPath、PatchDrop、扰动 EMA 和随机 JPEG 压缩等正则化技术系统性地引入对抗优化流程，形成一套**迁移性增强正则化组合**。消融实验（Table 5）表明，DropPath 和扰动 EMA 对攻击 Claude 系列模型至关重要——移除后 Claude 3.7 的 ASR 从 15.5% 骤降至 11.1%，验证了这些正则化在突破强鲁棒模型时的因果作用。

### 2. 方法谱系定位

Omni-Attack 在对抗攻击研究谱系中的定位可以概括为：**将多模态生成能力注入迁移攻击的优化目标构造环节**。其技术路线沿以下脉络展开：

- **上游依赖**：方法假设存在可用的 CLIP 家族代理模型（默认使用 3 个 CLIP 变体）和一个强大的多模态 LLM 用于目标文本生成，以及一个文本到图像模型（Qwen-Image）用于视觉目标生成。这一依赖决定了其适用边界——在无法访问 CLIP 类模型的场景下，攻击迁移性会显著下降（Table 7 显示非 CLIP 模型上的 ASR 较低）。

- **核心创新层**：目标构造流水线（LLM 推理 → 文本目标 → 循环验证 → 多目标集成 → 视觉目标生成）是方法的核心差异化模块。该流水线将“攻击什么”的问题从启发式选择提升为语义推理驱动的自动生成。

- **下游泛化**：方法在 AdvRobustBench（整合 MMBench、MMStar、OCRBench-v2）和 NIPS2017 Split 上进行了全面验证，覆盖 GPT-4.1、Claude 3.5/3.7、Gemini 2.0 等主流商业 MLLM，以及 Qwen3-VL 等开源模型，体现了较强的模型泛化性。

### 3. 适用边界

**有效边界**：
- 攻击目标为多选 VQA 任务，且问题-选项结构明确，便于 LLM 生成条件化的目标描述。
- 代理模型限定于 CLIP 家族（ViT-B/32、ViT-B/16、ViT-L/14 等），在这些模型上优化的扰动对基于视觉编码器的 MLLM 具有较强迁移性。
- 扰动预算在 L∞ 范数下为 8/255 或 16/255，属于中等强度的不可感知扰动范围。
- OCR 任务中，文本区域可被 PaddleOCR 可靠检测，且问题与特定文本区域存在明确的空间对应关系。

**失效或弱效边界**：
- **Claude 系列模型的强鲁棒性**：即使在 ε=8/255 下，Claude 3.5 和 3.7 的 ASR 仅为 13.9% 和 15.5%，远低于 GPT-4.1 的 71.8%。这表明 Claude 可能采用了不同的视觉编码架构或更强的对抗防御机制，Omni-Attack 的迁移策略在此处遭遇瓶颈。
- **非 CLIP 代理模型**：当代理模型不属于 CLIP 家族时，攻击迁移性显著下降（Table 7），说明方法的迁移性高度依赖 CLIP 特征空间的共性。
- **OCR 任务的低位 ASR**：在 OCRBench-v2 上，Qwen3-VL30B 的 ASR 仅为 25.3%（ε=8/255），远低于通用 VQA 任务，表明复杂文本区域的对抗扰动仍需更强的空间控制策略。
- **目标数量饱和**：消融显示多目标集成的收益在约 5 个目标后达到平台期，进一步增加目标无法带来显著提升，说明该方法在目标多样性方面的边际收益有限。

### 4. 局限与开放问题

**已识别的局限**（来自分析验证）：
1. Claude 系列模型表现出显著鲁棒性，Omni-Attack 对其攻击成功率较低，仍需突破该防御。
2. OCR 任务上的攻击成功率仍然处于低位，复杂文本区域的对抗扰动有待加强。
3. 生成的目标质量依赖 LLM 和文本到图像模型的能力，可能引入偏差，影响攻击稳定性。
4. 多目标集成的收益在约 5 个目标后达到饱和。
5. 攻击方法在非 CLIP 模型上的迁移性有限，代理模型选择主要局限于 CLIP 家族。

**开放问题**：
1. 如何进一步提升针对 Claude 等高度鲁棒模型的对抗样本迁移性？这是当前最紧迫的实际挑战，可能需要探索新的代理模型选择策略或针对 Claude 架构特性的定制化正则化。
2. 能否设计不依赖 CLIP 代理的通用黑盒攻击方法？当前方法对 CLIP 特征空间的强依赖限制了其在更广泛模型生态中的适用性。
3. 目标构造流水线能否实现自动化，摆脱对 LLM 循环验证的依赖？循环验证虽然有效，但增加了计算开销和流程复杂性。
4. 对抗扰动是否可能触发多模态 LLM 的安全对齐防御，从而限制攻击效果？随着模型安全机制的增强，攻击与防御的博弈将更加复杂。
5. 在真实场景（如图像压缩、传输）下，攻击的鲁棒性如何？随机 JPEG 压缩正则化虽然提升了迁移性，但实际部署中的多重失真可能进一步削弱攻击效果。

> **注意**：关于 Claude 系列鲁棒性的具体成因（如是否采用对抗训练、不同的视觉编码器架构等），原文未提供详细分析，需结合 Claude 技术文档进行进一步验证。

## 原文 PDF

![[paperPDFs/CVPR_2026/Omni_Attack_Adversarial_Attacks_on_Open_Ended_VQA_in_Black_Box_Multimodal_LLMs.pdf]]
