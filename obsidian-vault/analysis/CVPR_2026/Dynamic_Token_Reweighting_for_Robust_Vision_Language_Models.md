---
title: Dynamic Token Reweighting for Robust Vision-Language Models
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Dynamic_Token_Reweighting_for_Robust_Vision_Language_Models.pdf
project_link: null
code_link: "https://github.com/TanqiuJiang/DTR"
huggingface_link: "https://huggingface.co/datasets/Open-Orca/FLAN"
aliases:
- DDTR
- DTRRVLM
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过优化视觉token在KV缓存中的权重，调整模型在拒绝方向上的激活，从而抵消由视觉输入引入的安全相关偏移，恢复模型的安全对齐行为。
primary_logic: 提出逆安全相关偏移（RSS）概念，无需图像到文本转换即可量化视觉token对安全偏移的贡献；利用该信号动态重加权视觉token以最小化安全偏移，同时通过激活保持项保留模型对良性查询的性能，实现了高效且可解释的防御。
claims:
- 越狱查询的RSS值显著高于良性查询，且随着优化步数增加差距扩大（Figure 3）
- 在HADES的S+T+A攻击下，DTR将llava-llama2-7b的ASR从56.9%降至15.9%（Table 1）
- 在MM-Vet上DTR几乎完全保留了基线的视觉语言能力，甚至在空间感知上略有提升（Table 2）
- DTR的平均推理时间仅为4.01秒，远低于其他防御如ShiftDC的10.66秒（Table 3）
---

# Dynamic Token Reweighting for Robust Vision-Language Models

> [!tip] 核心洞察
> 提出逆安全相关偏移（RSS）概念，无需图像到文本转换即可量化视觉token对安全偏移的贡献；利用该信号动态重加权视觉token以最小化安全偏移，同时通过激活保持项保留模型对良性查询的性能，实现了高效且可解释的防御。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向鲁棒视觉语言模型的动态令牌重加权 |
| 英文题名 | Dynamic Token Reweighting for Robust Vision-Language Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2505.17132) · [Code](https://github.com/TanqiuJiang/DTR) · [HuggingFace](https://huggingface.co/datasets/Open-Orca/FLAN) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | DTR (Dynamic Token Reweighting) |
| Dataset | HADES, MM-SafetyBench, JailBreakV-28K, MM-Vet |

> [!tip] 效果简介
> - HADES (S+T+A) 上，ASR 15.9% vs 56.9% (-41.0%)。
> - MM-SafetyBench (S) 上，ASR 3.6% vs 70.0% (-66.4%)。
> - JailBreakV-28K (Blank) 上，ASR 3.6% vs 27.7% (-24.1%)。

## 概要

视觉语言模型（VLM）在多模态任务中展现出强大能力，但其安全对齐机制在面对视觉输入时存在根本性脆弱性：**视觉模态会引入安全相关的分布偏移（safety-relevant distributional shift），削弱模型区分安全与不安全请求的能力**，使其更容易被多模态越狱攻击攻破。现有防御方法或依赖图像到文本的转换（带来信息损失与计算开销），或在微调/推理阶段修改中间激活或解码logits，均难以在安全性与任务性能之间取得高效平衡。

针对这一瓶颈，本文提出 **DTR（Dynamic Token Reweighting，动态令牌重加权）**，一种新颖的推理时防御方法。DTR的核心思想是：**通过优化视觉token在KV缓存中的权重，调整模型在拒绝方向上的激活，从而抵消视觉输入引入的安全相关偏移，恢复模型的安全对齐行为**。该方法的关键创新在于引入**逆安全相关偏移（Reversal Safety-Relevant Shift, RSS）**概念——无需图像到文本转换即可量化视觉token对安全偏移的贡献，并利用该信号动态重加权视觉token以最小化安全偏移，同时通过激活保持项保留模型对良性查询的性能。

DTR在方法谱系中定位为**推理时KV缓存优化防御**，与现有方法形成显著差异：它不依赖图像转文本（区别于ShiftDC、ECSO），不修改解码logits（区别于CoCA），也不使用迭代提示过滤（区别于AdaShield、JailGuard），而是直接在KV缓存层面对视觉token的重要性进行逐token动态调节，并可选择性淘汰低重要性token以进一步提升效率。

主要实验结果验证了DTR的有效性与效率：

- **攻击防御力显著**：在HADES的S+T+A组合攻击下，DTR将LLaVA-Llama2-7B的攻击成功率（ASR）从56.9%降至15.9%；在MM-SafetyBench上ASR从70.0%降至3.6%（Table 1）。
- **良性任务性能几乎无损**：在MM-Vet基准上，DTR完全保留了基线的视觉语言能力（识别得分均为50.3），甚至在空间感知上略有提升（36.8→39.1）（Table 2）。
- **推理效率优异**：DTR的平均推理时间仅为4.01秒，接近未防御基线的3.65秒，远低于ShiftDC的10.66秒（Table 3）。
- **鲁棒性根源**：DTR使攻击者面临双重困境——绕过安全护栏需要增加RSS，而这会被DTR检测到；最小化RSS以逃避检测则会削弱攻击效果，从而形成内在的防御优势（Sec B.7）。

DTR仅需32个参考样本即可达到稳定的防御效果，且优化步数少（m=4即可大幅降低ASR），展现出良好的数据效率与实用性。该方法在LLaVA、MiniGPT、InternVL、Llama-4-Scout等多种VLM架构上均验证了通用性。

### 多模态越狱攻击：视觉输入引发的安全退化

视觉语言模型（VLM）在整合视觉与语言能力的同时，也暴露了一个关键脆弱性：**视觉模态会引入安全相关的分布偏移（safety-relevant distributional shift）**，削弱模型区分安全与不安全请求的能力。攻击者通过在图像中嵌入对抗性扰动、排版文本或利用生成模型构造恶意视觉内容，可以绕过模型内置的安全对齐机制，诱导其产生有害响应。这种多模态越狱攻击在多个基准上展现出极高的攻击成功率——例如，在HADES的S+T+A组合攻击下，未防御的llava-llama2-7b模型的攻击成功率（ASR）高达56.9%。

问题的本质在于：VLM的安全对齐主要基于文本模态的训练，而视觉输入的加入使得模型在拒绝方向上的激活发生偏移，使其更容易被“推离”安全区域。因此，**如何在不损害视觉理解能力的前提下，抵消视觉模态引入的安全相关偏移**，成为多模态安全防御的核心挑战。

### 现有防御方法的缺口

当前针对多模态越狱攻击的防御方法大致可分为三类，但各自存在明显局限：

- **基于提示的防御**（如AdaShield、JailGuard）：通过迭代生成防御提示或提示变异来检测越狱攻击。这类方法依赖额外的推理调用，计算开销大，且防御效果受限于提示工程的质量。
- **基于激活或解码修改的防御**（如ShiftDC、CoCA）：在推理时修改中间层激活或解码logits来偏移安全相关偏移。其中ShiftDC需要通过图像到文本的转换来估计安全偏移，这一过程不仅引入信息损失，还导致推理时间增加2倍以上（例如ShiftDC的平均推理时间为10.66秒，而未防御模型仅需3.65秒）。
- **基于微调的防御**：在训练阶段强化安全对齐，但无法应对推理时出现的新型攻击，且重新训练成本高昂。

上述方法的共同缺口在于：**缺乏一种无需图像到文本转换、在推理时高效运行、且能精确量化视觉token对安全偏移贡献的机制**。这正是本文工作试图填补的空白。

### 本文动机：从KV缓存优化到动态令牌重加权

本文的核心洞察是：**视觉token在KV缓存中的重要性并非均匀分布——某些token是导致安全偏移的关键因素，而其他token则承载着良性视觉理解所需的信息**。基于此，本文提出**DTR（Dynamic Token Reweighting）**，一种全新的推理时防御框架。

DTR的动机源于三个关键观察：

1. **拒绝方向的可计算性**：通过少量（默认32个）有害和无害文本提示，可以预计算出模型在特定层的拒绝方向向量$\mathbf{d}_{\mathrm{ref}}$，该方向刻画了从有害到安全行为的激活差异。
2. **逆安全相关偏移（RSS）的量化**：引入RSS概念，直接量化视觉token在逆拒绝方向上可达到的最大偏移量，无需参考图像或文本转换即可估计视觉输入的安全风险——越狱查询的RSS值显著高于良性查询，且这一差距随优化步数增加而扩大（Figure 3）。
3. **逐token动态重加权的可行性**：通过在推理时优化视觉token的缩放因子$\boldsymbol{\alpha}$，可以最小化模型在拒绝方向上的投影（降低安全风险），同时约束激活与原始输入的L2距离（保留良性性能）。这种机制天然具有可解释性——缩放向量$\boldsymbol{\alpha}$的热力图可以直观地区分越狱查询中的对抗性token和特征token（Figure 4）。

与现有方法相比，DTR的独特优势在于：它首次将KV缓存优化引入多模态越狱防御，避免了图像到文本转换的信息损失和计算开销，同时通过早停和token淘汰策略实现了极低的推理额外开销（平均推理时间仅4.01秒，相比未防御模型的3.65秒仅增加0.36秒）。

## 核心方法与创新机理

DTR 的核心创新在于**首次将 KV 缓存优化引入多模态越狱防御**，并围绕“逆安全相关偏移”（Reversal Safety-Relevant Shift, RSS）构建了一套无需图像到文本转换、可解释且高效的推理时防御框架。其相对于现有防御方法的关键改进体现在以下三个维度。

### 1. 安全相关偏移的估计：从“参考依赖”到“自优化量化”

现有防御方法在估计视觉模态引入的安全退化时，普遍依赖外部参考或图像到文本的转换。例如，**ShiftDC** 与 **ECSO** 需要将图像转为文本描述，再与纯文本输入比较以计算安全偏移，这一过程不仅引入信息损失，还带来显著的计算开销。**CoCA** 则通过修改解码 logits 来偏移安全方向，但其偏移量的估计仍缺乏对视觉 token 粒度的精细建模。

DTR 提出了**逆安全相关偏移（RSS）**这一全新概念，彻底绕开了对参考图像或文本转换的依赖。其核心思想是：给定一个预计算的拒绝方向 $\mathbf{d}_{\mathrm{ref}}$，RSS 定义为通过优化视觉 token 的缩放因子 $\boldsymbol{\alpha} \in [0,1]^n$ 所能达到的最大逆偏移量：

$$
\Delta_{\mathrm{safe}}^{*}(\mathbf{x}) = \operatorname*{max}_{\boldsymbol{\alpha} \in [0,1]^n} {\frac{(f(\mathbf{x}) - f(\mathbf{x}(\boldsymbol{\alpha}))) \cdot \mathbf{d}_{\mathrm{ref}}}{\|\mathbf{d}_{\mathrm{ref}}\|}}
$$

其中 $\mathbf{x}(\boldsymbol{\alpha})$ 表示将缩放因子应用于视觉 token 后的多模态输入。RSS 直接量化了视觉 token 对安全偏移的贡献上限——越狱查询的 RSS 值显著高于良性查询，且随着优化步数增加，这一差距持续扩大（Figure 3）。这一信号不仅为防御提供了可靠的检测依据，还赋予了方法内在的**可解释性**：缩放向量 $\boldsymbol{\alpha}$ 的热力图可以直观地区分越狱查询中的对抗性 token 与正常特征 token（Figure 4）。

### 2. 防御机制：从“激活/Logit 干预”到“KV 缓存级动态重加权”

在防御的发生阶段与机制上，现有方法大致分为三类：微调阶段强化对齐、推理时修改中间激活（如 ShiftDC）、推理时修改解码 logits（如 CoCA），或通过迭代提示过滤（如 AdaShield、JailGuard）。这些方法要么需要额外的模型调用，要么在固定层上进行全局干预，缺乏对视觉 token 的细粒度控制。

DTR 的防御机制直接作用于模型的 **KV 缓存**，通过优化视觉 token 的逐 token 缩放因子 $\boldsymbol{\alpha}^{*}$ 来动态调节每个视觉 token 对模型推理的影响。优化目标由两项构成：

$$
\mathcal{L}(\boldsymbol{\alpha}) = \frac{f(\mathbf{x}(\boldsymbol{\alpha})) \cdot \mathbf{d}_{\mathrm{ref}}}{\|\mathbf{d}_{\mathrm{ref}}\|} + \lambda \| \mathbf{f}(\mathbf{x}) - \mathbf{f}(\mathbf{x}(\boldsymbol{\alpha})) \|_2
$$

第一项最小化激活在拒绝方向上的投影，直接压制安全风险；第二项约束缩放后激活与原始激活的 L2 距离，保留模型对良性查询的视觉理解能力。这一设计实现了**安全与效用的精细平衡**——均匀缩放所有视觉 token 无法同时达成两者，而 DTR 的逐 token 动态重加权能够选择性压制对抗性 token 同时保留视觉理解所需的关键特征（Table 14, Figure 7）。

此外，DTR 支持**选择性 token 淘汰**：将缩放因子低于阈值 $\beta$ 的视觉 token 从 KV 缓存中移除，进一步降低推理开销。消融实验表明，淘汰 20% 的视觉 token 即可良好平衡推理效率、ASR 降低和任务性能（Figure 5d）。

### 3. 推理效率：从“2 倍以上开销”到“近乎零额外延迟”

图像到文本转换不仅损失信息，还导致显著的推理延迟。例如，ShiftDC 的平均推理时间（AIT）为 10.66 秒，是未防御基线（3.65 秒）的近 3 倍。DTR 通过两项策略将额外开销压缩至极小：

- **早停策略**：优化步数 $m=4$ 即可大幅降低 ASR，继续增加对视觉语言能力影响不大（Figure 5b），因此可在有限步数内终止优化。
- **token 淘汰**：移除低重要性 token 减少 KV 缓存规模，加速后续推理。

最终，DTR 的平均推理时间仅为 4.01 秒，相比基线仅增加 0.36 秒（Table 3），远低于其他防御方法。

### 4. 鲁棒性的双重困境机制

DTR 的防御鲁棒性源于其给攻击者制造的**双重困境**（Appendix B.7）：攻击者要绕过 VLM 的安全护栏，需要将嵌入引导远离拒绝区域，这不可避免地增加 RSS，使输入被 DTR 检测到；反之，若攻击者试图最小化 RSS 以逃避检测，则会限制其诱导安全相关偏移的能力，从而削弱攻击效果。即使在针对 DTR 的自适应攻击（PGD 最小化 RSS）下，DTR 仍能将 ASR 限制在 18%，而未防御模型高达 68%（Table 13），验证了这一机制的有效性。

DTR（Dynamic Token Reweighting）是一种**推理时防御方法**，其核心设计目标是在不修改模型参数的前提下，通过动态调节视觉令牌（visual tokens）在KV缓存中的重要性，抵消由多模态输入引入的安全相关分布偏移（safety-relevant distributional shift），从而恢复VLM内置的安全对齐行为。该方法首次将KV缓存优化引入多模态越狱防御领域。

### 方法概览与输入输出流

DTR的整体流程如图1所示，由三个顺序执行的模块组成，形成一条从安全方向预计算到令牌重加权再到最终推理的完整管线。

**输入**：多模态查询 $\mathbf{x} = \mathbf{x}_{\mathrm{txt}} \parallel \mathbf{x}_{\mathrm{img}}$，其中 $\mathbf{x}_{\mathrm{txt}}$ 为文本令牌序列，$\mathbf{x}_{\mathrm{img}}$ 为视觉编码器输出的 $n$ 个视觉令牌。

**输出**：经过安全对齐的模型响应，由重加权后的视觉令牌参与解码生成。

**核心机制**：DTR通过优化一个可学习的缩放向量 $\boldsymbol{\alpha} \in [0,1]^n$，对每个视觉令牌的重要性进行逐令牌调整，使得模型在拒绝方向（refusal direction）上的激活被抑制，同时通过保真项约束保持对良性查询的响应质量。

### 三大管线模块

#### 模块一：拒绝方向预计算

该模块在防御启动前离线完成，为后续优化提供安全参考方向。具体而言，从AdvBench中随机采样少量有害文本提示（默认32条），从AlpacaEval中采样等量无害文本提示，分别计算模型在选定层 $\ell$ 的最后令牌激活均值：

$$
\boldsymbol{\mu}_{\mathrm{harmful}}^{(\ell)} = \frac{1}{|\mathcal{D}_{\mathrm{harmful}}|} \sum_{\mathbf{x} \in \mathcal{D}_{\mathrm{harmful}}} f^{(\ell)}(\mathbf{x}), \quad
\boldsymbol{\mu}_{\mathrm{harmless}}^{(\ell)} = \frac{1}{|\mathcal{D}_{\mathrm{harmless}}|} \sum_{\mathbf{x} \in \mathcal{D}_{\mathrm{harmless}}} f^{(\ell)}(\mathbf{x})
$$

拒绝方向向量即二者的差值：

$$
\mathbf{d}_{\mathrm{ref}}^{(\ell)} = \boldsymbol{\mu}_{\mathrm{harmless}}^{(\ell)} - \boldsymbol{\mu}_{\mathrm{harmful}}^{(\ell)}
$$

该方向捕捉了模型在安全与不安全输入之间的激活差异，是后续优化的核心参照。消融实验表明，仅需32个参考样本即可达到稳定的防御效果，更多样本收益递减（Figure 5a）。

#### 模块二：逆安全相关偏移优化

该模块是DTR的核心创新。传统方法（如ShiftDC、ECSO）需通过图像到文本转换或额外VLM来估计安全偏移，引入信息损失和计算开销。DTR提出**逆安全相关偏移（Reversal Safety-Relevant Shift, RSS）**概念，直接在视觉令牌空间内优化缩放向量 $\boldsymbol{\alpha}$，无需任何参考图像或文本转换。

RSS定义为通过调整 $\boldsymbol{\alpha}$ 可达到的沿逆拒绝方向的最大偏移量：

$$
\Delta_{\mathrm{safe}}^{*}(\mathbf{x}) = \operatorname*{max}_{\boldsymbol{\alpha} \in [0,1]^n} \frac{(f(\mathbf{x}) - f(\mathbf{x}(\boldsymbol{\alpha}))) \cdot \mathbf{d}_{\mathrm{ref}}}{\|\mathbf{d}_{\mathrm{ref}}\|}
$$

其中 $\mathbf{x}(\boldsymbol{\alpha}) = \mathbf{x}_{\mathrm{txt}} \parallel (\boldsymbol{\alpha} \odot \mathbf{x}_{\mathrm{img}})$ 表示将缩放向量逐元素作用于视觉令牌后的查询。

实验验证了RSS作为安全风险指标的有效性：越狱查询的RSS值显著高于良性查询，且随着优化步数增加，这一差距持续扩大（Figure 3）。这表明越狱攻击本质上会迫使模型激活偏离安全区域，而DTR正是利用这一信号进行防御。

在此基础上，DTR通过AdamW优化器最小化如下目标函数，得到最优缩放向量 $\boldsymbol{\alpha}^{*}$：

$$
\boldsymbol{\alpha}^{*} = \arg\min_{\boldsymbol{\alpha} \in [0,1]^n} \mathcal{L}(\boldsymbol{\alpha}), \quad \mathcal{L}(\boldsymbol{\alpha}) = \frac{f(\mathbf{x}(\boldsymbol{\alpha})) \cdot \mathbf{d}_{\mathrm{ref}}}{\|\mathbf{d}_{\mathrm{ref}}\|} + \lambda \| \mathbf{f}(\mathbf{x}) - \mathbf{f}(\mathbf{x}(\boldsymbol{\alpha})) \|_2
$$

损失函数由两项构成：
- **安全项**（第一项）：最小化重加权后激活在拒绝方向上的投影，将模型推向安全响应区域；
- **保真项**（第二项）：约束重加权后的激活与原始激活的L2距离，保留模型对良性内容的感知能力。

超参数 $\lambda$ 控制安全与效用的平衡，消融实验确定 $\lambda=0.1$ 时达到最优（ASR 9.21%，平均VLC 38.5，Table 15）。

#### 模块三：动态令牌重加权与推理

优化完成后，将 $\boldsymbol{\alpha}^{*}$ 应用于视觉令牌，并可选择性淘汰缩放因子低于阈值 $\beta$ 的令牌，进一步降低计算开销。随后，模型使用重加权后的视觉令牌执行标准解码，生成最终响应。

DTR通过两项策略保障推理效率：
1. **早停机制**：优化步数 $m$ 可提前终止，消融表明 $m=4$ 即可大幅降低ASR，继续增加对视觉语言能力影响甚微（Figure 5b）；
2. **令牌淘汰**：淘汰20%视觉令牌可在推理效率、ASR降低和任务性能之间取得良好平衡（Figure 5d）。

在MM-Vet基准上，DTR的平均推理时间仅为4.01秒，接近未防御基线的3.65秒，远低于ShiftDC的10.66秒（Table 3）。

### 模块间的数据依赖关系

三个模块形成清晰的串行依赖：模块一为模块二提供拒绝方向 $\mathbf{d}_{\mathrm{ref}}$；模块二利用该方向优化得到缩放向量 $\boldsymbol{\alpha}^{*}$；模块三消费 $\boldsymbol{\alpha}^{*}$ 完成令牌重加权和响应生成。模块一可离线预计算并跨查询复用，模块二和模块三在推理时对每个查询独立执行，整体流程无需访问外部模型或进行图像转文本操作，保证了方法的自包含性和高效性。

### 问题形式化

VLM 在给定文本输入 $\mathbf{x}_{\mathrm{txt}}$ 和视觉输入 $\mathbf{x}_{\mathrm{img}}$ 后，通过迭代采样生成响应：

$$y_i \sim P(\cdot \mid \mathbf{x}_{\mathrm{txt}}, \mathbf{x}_{\mathrm{img}}, y_1, \dots, y_{i-1})$$

多模态越狱攻击的核心瓶颈在于：视觉模态引入**安全相关的分布偏移**（safety-relevant distributional shift），削弱了 VLM 区分安全与不安全请求的能力。DTR 的核心思路是通过优化 KV 缓存中视觉 token 的权重，调整模型在拒绝方向上的激活，从而抵消该偏移。

### 模块一：拒绝方向预计算

DTR 首先需要获取模型的**拒绝方向**（refusal direction），该方向编码了模型从“安全响应”到“拒绝响应”的激活变化。具体做法是：从 AdvBench 中随机采样 32 个有害文本提示，从 AlpacaEval 中随机采样 32 个无害文本提示，分别计算模型在给定层 $\ell$ 上的最后 token 激活均值：

$$\pmb{\mu}_{\mathrm{harmful}}^{(\ell)} = \frac{1}{|\mathcal{D}_{\mathrm{harmful}}|} \sum_{\mathbf{x} \in \mathcal{D}_{\mathrm{harmful}}} f^{(\ell)}(\mathbf{x})$$

$$\pmb{\mu}_{\mathrm{harmless}}^{(\ell)} = \frac{1}{|\mathcal{D}_{\mathrm{harmless}}|} \sum_{\mathbf{x} \in \mathcal{D}_{\mathrm{harmless}}} f^{(\ell)}(\mathbf{x})$$

拒绝方向即为两者的差值向量：

$$\mathbf{d}_{\mathrm{ref}}^{(\ell)} = \pmb{\mu}_{\mathrm{harmless}}^{(\ell)} - \pmb{\mu}_{\mathrm{harmful}}^{(\ell)}$$

该方向捕捉了从有害到无害的激活偏移，后续所有安全相关偏移的估计都基于此方向进行投影。消融实验表明，仅需 32 个参考样本即可达到稳定的防御效果，更多样本收益递减（Figure 5a）。

### 模块二：逆安全相关偏移（RSS）的估计

传统方法（如 ShiftDC）需要将图像转换为文本来估计安全偏移，存在信息损失和计算开销。DTR 提出了**逆安全相关偏移**（Reversal Safety-Relevant Shift, RSS）的概念，无需参考图像或文本转换即可量化视觉 token 对安全偏移的贡献。

首先定义缩放后的查询：将视觉 token 的嵌入乘以缩放向量 $\alpha \in [0,1]^n$（$n$ 为视觉 token 数量），即：

$$\mathbf{x}(\alpha) = \mathbf{x}_{\mathrm{txt}} \,\|\, \alpha \cdot \mathbf{x}_{\mathrm{img}}$$

其中 $\|$ 表示拼接。安全相关偏移定义为多模态输入与纯文本输入的激活差在拒绝方向上的投影：

$$\Delta_{\mathrm{safe}}(\mathbf{x}) = \frac{(f(\mathbf{x}) - f(\tilde{\mathbf{x}})) \cdot \mathbf{d}_{\mathrm{ref}}}{\|\mathbf{d}_{\mathrm{ref}}\|}$$

在此基础上，RSS 定义为通过优化缩放因子 $\alpha$ 所能达到的最大逆偏移量——即最小化安全偏移的方向：

$$\Delta_{\mathrm{safe}}^{*}(\mathbf{x}) = \max_{\alpha \in [0,1]^n} \frac{(f(\mathbf{x}) - f(\mathbf{x}(\alpha))) \cdot \mathbf{d}_{\mathrm{ref}}}{\|\mathbf{d}_{\mathrm{ref}}\|}$$

实验验证了 RSS 的有效性：越狱查询的 RSS 值显著高于良性查询，且随着优化步数增加，两者差距逐渐扩大（Figure 3）。这表明越狱查询更容易沿着逆拒绝方向被优化，RSS 能够作为可靠的安全偏移信号。

### 模块三：动态 Token 重加权优化

基于 RSS 信号，DTR 通过优化视觉 token 的缩放因子 $\alpha$ 来实现防御。优化目标包含两项：

$$\alpha^{*} = \arg\min_{\alpha \in [0,1]^n} \mathcal{L}(\alpha), \quad \mathcal{L}(\alpha) = \frac{f(\mathbf{x}(\alpha)) \cdot \mathbf{d}_{\mathrm{ref}}}{\|\mathbf{d}_{\mathrm{ref}}\|} + \lambda \| \mathbf{f}(\mathbf{x}) - \mathbf{f}(\mathbf{x}(\alpha)) \|_2$$

- **第一项（安全项）**：最小化缩放后激活在拒绝方向上的投影值，即推动模型向拒绝方向移动，降低安全风险。
- **第二项（保真项）**：约束缩放后激活与原始激活的 L2 距离，保留模型对良性查询的性能。超参数 $\lambda$ 控制安全与效用的平衡（$\lambda=0.1$ 时达到最优，Table 15）。

优化使用 AdamW 优化器，并采用早停策略：仅需 $m=4$ 步即可大幅降低 ASR，继续增加步数对视觉语言能力影响不大（Figure 5b）。

### 模块四：Token 淘汰与推理效率

得到最优缩放向量 $\alpha^{*}$ 后，DTR 将其应用于视觉 token。为进一步提升效率，DTR 支持**token 淘汰**（token eviction）：将缩放因子低于预设阈值 $\beta$ 的视觉 token 直接移除。消融实验表明，淘汰 20% 的视觉 token 可良好平衡推理效率、ASR 降低和任务性能（Figure 5d）。

在推理效率方面，DTR 的平均推理时间仅为 4.01 秒，与未防御基线的 3.65 秒相比仅增加 0.36 秒，远低于 ShiftDC 的 10.66 秒（Table 3）。这得益于早停和 token 淘汰等优化策略。

![[assets/figures/papers/paper_list_l746_https_arxiv_org_abs_2505_17132/figures/020_Figure_7.jpg]]
*Figure 7: Comparison of α heatmaps under uniform reweighting (left) and DTR’s optimized reweighting (right). Uniform scaling applies a constant value across all visual tokens, whereas DTR selectively adjusts per-token weights based on their safety relevance*

## 实验与关键发现

### 核心防御性能

DTR在多个主流多模态越狱基准上展现出显著的防御能力。在最具挑战性的HADES（S+T+A联合攻击）下，DTR将**llava-llama2-7b**的攻击成功率（ASR）从56.9%降至15.9%，降幅达41个百分点（Table 1）。在MM-SafetyBench的SD生成攻击（S）下，ASR从70.0%骤降至3.6%，降幅达66.4个百分点。对于JailBreakV-28K的Blank攻击，DTR将**llava-1.5-vicuna-7b**的ASR从47.3%降至7.3%（Table 1），展现出跨模型架构的鲁棒性。

![[assets/figures/papers/paper_list_l746_https_arxiv_org_abs_2505_17132/figures/004_Table_1.jpg]]
*Table 1: Robustness of DTR and baselines against multimodal jailbreak attacks on various benchmarks (A – adversarial perturbation, S – stable diffusion, and T – typography)*

与现有防御方法相比，DTR的优势尤为突出。**ShiftDC**虽能降低ASR，但其图像转文本机制导致信息损失，在HADES（S+T+A）上ASR仍高达30.3%；**AdaShield**的迭代防御提示策略在MM-SafetyBench（S）上仅将ASR降至42.7%，远逊于DTR的3.6%。在VLGuard基准上，DTR将LLM判定的有害性（ASR-G）从66.5%降至7.4%（安全图像+有害文本设置），而拒绝启发式ASR（ASR-R）从58.5%降至2.0%（Table 9），表明防御不仅触发拒绝响应，更实质性降低了生成内容的有害程度。

![[assets/figures/papers/paper_list_l746_https_arxiv_org_abs_2505_17132/figures/013_Table_9.jpg]]
*Table 9: VLGuard results on LLaVA-Llama2-7B. ASR-G: LLMjudged harmfulness; ASR-R: refusal-heuristic ASR (success if no refusal cue is detected). Lower is better*

### 良性任务性能保留

DTR在MM-Vet基准上几乎完全保留了基线的视觉语言能力（Table 2）。在识别（Recognition）任务上，DTR得分50.3，与未防御基线持平；在OCR、数学、知识、语言生成等维度上，性能折损可忽略不计。值得注意的是，DTR在空间感知（Spatial Awareness）上得分39.1，较基线的36.8提升了2.3分，暗示动态token重加权可能抑制了部分干扰性视觉token，反而强化了空间推理相关特征。相比之下，ShiftDC在MM-Vet的多项能力上出现明显退化（如OCR从30.6降至27.1），CoCA在知识维度上从40.7降至35.5，验证了DTR的保真项设计（Eq. 8中λ约束）在维持模型效用方面的关键作用。

![[assets/figures/papers/paper_list_l746_https_arxiv_org_abs_2505_17132/figures/005_Table_2.jpg]]
*Table 2: Task performance of llava-llama2-7b defended by various methods on MM-Vet*

在MME基准上（Table 12），**LLaVA-v1.5-7b + DTR**与基线模型的得分差异极小，进一步证实防御不会引入针对特定能力的系统性偏差。

### 推理效率

DTR的推理开销极为有限（Table 3）。在MM-Vet上，DTR的平均推理时间（AIT）仅为4.01秒，较未防御基线的3.65秒仅增加0.36秒（约10%）。这得益于早停策略（优化步数m=4即可收敛）和token淘汰机制。相比之下，ShiftDC因图像转文本流程导致AIT高达10.66秒，为基线的2.9倍；AdaShield的迭代提示生成也将AIT推至8.21秒。DTR在安全性与效率之间实现了当前最优的平衡。

### 消融分析

**参考样本数量**（Figure 5a）：仅需32个参考样本（16有害+16无害）即可稳定估计拒绝方向，更多样本（如64或128）带来的ASR降低微乎其微，证明DTR的数据效率极高。

**优化步数**（Figure 5b）：优化步数m=4时ASR已大幅降低，继续增加步数对VLC影响不大，验证早停策略的有效性。这源于RSS信号本身对越狱查询的强区分能力（Figure 3），少量迭代即可将缩放向量α推向有效区域。

**超参数λ**（Figure 5c，Table 15）：λ=0.1时达到最佳安全-效用平衡（ASR 9.21%，平均VLC 38.5）。过小的λ（如0.01）虽进一步降低ASR至6.76%，但VLC降至37.2；过大的λ（如0.5）则ASR回升至12.31%，表明保真项对维持良性性能不可或缺。

**Token淘汰比例**（Figure 5d）：淘汰20%的视觉token可良好平衡推理效率、ASR降低和任务性能。更激进的淘汰（如50%）虽加速推理，但开始侵蚀视觉理解能力。

**防御层选择**（Table 7）：在LLaVA-Llama2上，第14层应用DTR时ASR最低（15.9%），浅层或深层效果均下降，表明安全相关偏移主要集中在中后期Transformer层。

**学习率灵敏度**（Table 8）：学习率η=0.01时ASR最低，过大（0.1）或过小（0.001）均影响收敛质量，需针对具体模型微调。

### 架构通用性

DTR在多种VLM架构上展现出一致的防御能力。在**InternVL-2.5-26b**上，DTR将HADES（S+T+A）的ASR从61.2%降至18.5%；在**MiniGPT-v2**上，从43.8%降至11.2%（Table 5）。在最新的**Llama-4-Scout-17B**上，DTR同样将HADES各攻击类型的ASR控制在20%以下（Table 6），证明方法不依赖特定模型架构或对齐方式。

![[assets/figures/papers/paper_list_l746_https_arxiv_org_abs_2505_17132/figures/011_Table_5.jpg]]
*Table 5: Attack robustness of DTR on InternVL-2.5-26b and MiniGPT-v2 (A – adversarial perturbation, S – stable diffusion, T – typography)*

![[assets/figures/papers/paper_list_l746_https_arxiv_org_abs_2505_17132/figures/012_Table_6.jpg]]
*Table 6: Attack robustness of DTR on Llama-4-Scout-17B on HADES (A – adversarial perturbation, S – stable diffusion, T – typography)*

### 可解释性

DTR的缩放向量α提供了直观的可解释性（Figure 4，Figure 12-13）。在越狱查询中，对抗性视觉token（如拼接的恶意文字区域）被赋予极低的缩放因子（接近0），而承载正常视觉特征的token保持较高权重。这种选择性压制使模型在拒绝有害请求的同时，仍能正确描述良性图像内容。均匀缩放所有视觉token则无法实现这种精细控制——要么全面压制导致良性性能崩溃，要么压制不足无法触发拒绝（Table 14，Figure 7）。

### 自适应攻击下的鲁棒性

为评估DTR面对自适应攻击的鲁棒性，研究者设计了PGD攻击以最小化RSS值，试图逃避检测。结果表明（Table 13，Figure 6），攻击者面临固有困境：绕过安全护栏需将嵌入推离拒绝区域，这会增加RSS使输入被DTR检测；而最小化RSS以逃避检测则会约束攻击者诱导安全偏移的能力。在此自适应攻击下，DTR仍将ASR限制在18%，而未防御模型高达68%，验证了防御机制的理论优势。

## 定位与知识库关联

### 问题定位：视觉模态引入的安全偏移

多模态视觉语言模型（VLM）面临的越狱攻击根源于一个关键瓶颈：**视觉模态引入了安全相关的分布偏移（safety-relevant distributional shift）**，削弱了模型区分安全与不安全请求的能力。纯文本语言模型通过安全对齐（如RLHF）习得的拒绝行为，在视觉输入加入后可能被绕过，使攻击者更容易通过多模态越狱攻击攻破模型。DTR的核心洞察在于，这种偏移可以通过**逆安全相关偏移（Reversal Safety-Relevant Shift, RSS）** 来量化——即视觉token沿拒绝方向反向优化可达到的最大偏移量，而无需进行图像到文本的转换。

### 方法谱系中的位置

DTR在多模态越狱防御方法谱系中占据独特位置，其与现有基线的关系可从以下几个维度定位：

**1. 推理时防御 vs. 训练时防御**

DTR属于**推理时防御**（inference-time defense），不修改模型参数，仅通过优化KV缓存中的视觉token权重来恢复安全对齐。与之相对的训练时防御（如安全微调）需要重新训练模型，成本高昂且可能损害通用能力。DTR的推理时特性使其具有即插即用的部署优势。

**2. 激活层干预 vs. 解码时干预**

现有的推理时防御可按干预阶段划分为两类：

- **激活层干预方法**：**ShiftDC** 通过修改中间激活层来偏移安全相关偏移，但需要图像到文本转换来估计偏移量，引入信息损失和约2倍推理时间增加（AIT 10.66s vs Base 3.65s）。**ECSO** 类似地依赖文本转换获取安全参考。
- **解码时干预方法**：**CoCA** 通过修改解码logits来偏移安全相关偏移，同样面临估计精度与效率的权衡。
- **提示层防御方法**：**AdaShield** 迭代生成防御提示以检查图像安全性，**JailGuard** 通过提示变异检测越狱攻击，这些方法依赖额外的推理轮次，效率较低。

DTR在**防御发生阶段与机制**上实现了关键突破：直接在KV缓存层面优化视觉token的缩放因子，无需参考图像或文本转换，避免了信息损失。其防御机制通过最小化包含安全项和保真项的损失函数（Eq. 8）实现：

$$
\mathbf{\boldsymbol{\alpha}}^{*} = \arg\underset{\boldsymbol{\alpha} \in [0,1]^n}{\operatorname*{min}} \mathcal{L}(\boldsymbol{\alpha}), \; \mathcal{L}(\boldsymbol{\alpha}) = \frac{f(\mathbf{x}(\boldsymbol{\alpha})) \cdot \mathbf{d}_{\mathrm{ref}}}{\|\mathbf{d}_{\mathrm{ref}}\|} + \lambda \| \mathbf{f}(\mathbf{x}) - \mathbf{f}(\mathbf{x}(\boldsymbol{\alpha})) \|_2
$$

第一项最小化投影到拒绝方向的值以降低安全风险，第二项约束激活与原始输入的L2距离以保留模型性能。

**3. 偏移估计方式的创新**

DTR的**安全相关偏移估计方式**从根本上区别于现有方法：

- 基线方法（ShiftDC、ECSO）需要图像到文本转换或额外的VLM来获取安全参考，导致信息损失和高计算开销。
- DTR利用拒绝方向和逆安全相关偏移（RSS）直接优化视觉token权重，无需参考图像或文本转换。RSS定义为：

$$
\Delta_{\mathrm{safe}}^{*}(\mathbf{x}) = \operatorname*{max}_{\alpha \in [0,1]^n} {\frac{(f(\mathbf{x}) - f(\mathbf{x}(\alpha))) \cdot \mathbf{d}_{\mathrm{ref}}}{\|\mathbf{d}_{\mathrm{ref}}\|}}
$$

拒绝方向 $\mathbf{d}_{\mathrm{ref}}^{(\ell)}$ 通过少量（默认32）有害和无害文本提示的激活差异预计算得到：

$$
\mathbf{d}_{\mathrm{ref}}^{(\ell)} = \pmb{\mu}_{\mathrm{harmless}}^{(\ell)} - \pmb{\mu}_{\mathrm{harmful}}^{(\ell)}
$$

这一设计使DTR成为**首个将KV缓存优化用于多模态越狱防御的工作**。

**4. 推理效率的优势**

DTR通过早停策略（优化步数m=4即可大幅降低ASR）和token淘汰机制（淘汰缩放因子低于阈值β的视觉token），实现了极低的额外开销。其平均推理时间仅为4.01秒，接近未防御基线的3.65秒，远优于ShiftDC的10.66秒。

### 适用边界与条件

DTR的适用性受以下条件约束：

1. **架构依赖**：DTR依赖VLM中视觉token与文本token在KV缓存中的分离表示。实验在LLaVA、MiniGPT、InternVL、Llama-4-Scout等架构上验证了通用性，但尚未在统一处理视觉和文本的最新大模型（如GPT-4o）上验证。

2. **层选择敏感性**：DTR需要手动选择应用层。在LLaVA-Llama2上，第14层表现最佳（ASR 15.9%），但不同VLM可能需要重新校准，缺乏自动化的层选择机制。

3. **攻击类型覆盖**：DTR主要针对视觉模态引入的越狱攻击（对抗扰动、Stable Diffusion生成、排版攻击等）。对于完全由文本驱动的越狱攻击，其防护作用间接依赖视觉-语言交互，效果可能有限。

4. **超参数校准**：超参数λ控制安全-效用平衡（λ=0.1时ASR 9.21%，平均VLC 38.5），学习率η=0.01时ASR最低。这些参数在不同VLM上可能需要重新调优。

### 局限与开放问题

**已知局限：**

1. **手动校准需求**：DTR依赖手动选择的层和超参数，在不同VLM上可能需要重新校准以达到最优效果。虽然仅需32个参考样本即可达到稳定防御效果，但层选择和λ调优仍需人工介入。

2. **微小推理开销**：优化步骤虽少（m=4），但仍对极低延迟应用产生约0.36秒的额外开销。对于实时交互场景，这一开销需纳入考量。

3. **对抗空间存在**：尽管自适应攻击评估（PGD最小化RSS）显示DTR仍将ASR限制在18%（未防御模型为68%），但对手可能开发更复杂的攻击来绕过RSS检测，防御仍存在理论上的对抗空间。

4. **纯文本越狱覆盖有限**：DTR的核心机制依赖于视觉token的重加权，对于完全由文本驱动的越狱攻击，防护效果可能不直接。

**开放问题：**

1. **自适应攻击的对抗鲁棒性边界**：DTR如何应对专门针对特定有害任务进行优化的自适应攻击？攻击者能否通过联合优化视觉和文本模态来绕过RSS检测？

2. **防御框架的协同效应**：能否将DTR与其他防御框架（如解码时防御CoCA）结合，在激活层和解码层同时施加约束，产生协同效应？

3. **纯文本语言模型的迁移**：DTR的核心机制——通过KV缓存优化调整拒绝方向上的激活——是否适用于仅文本的语言模型，以防御纯文本越狱攻击？这需要重新定义“视觉token”在文本上下文中的对应物。

4. **多轮对话与多图像场景**：在多轮对话或多图像输入场景下，DTR的动态重加权策略如何调整？是否需要维护跨轮次的token重要性状态？

5. **自动化层与超参数选择**：如何自动化选择最优的防御层和超参数，并适应模型更新？可能的路径包括基于验证集的启发式搜索或元学习。

6. **最新统一多模态大模型的扩展**：DTR在GPT-4o等统一处理视觉和文本的模型上的适用性待验证，这类模型可能不显式区分视觉和文本token的KV缓存。

### 防御机制的双重困境优势

DTR的鲁棒性部分源于其给攻击者制造的**双重困境**：绕过VLM安全护栏需要将嵌入引导远离拒绝区域，这会增加RSS并使输入被DTR检测到；反过来，最小化RSS以逃避DTR检测会限制攻击者诱导足够安全相关偏移的能力。这一内在张力使DTR在面对自适应攻击时仍保持有效，ASR-R与ASR-G的相反变化关系（Figure 6）验证了这一机制。

## 原文 PDF

![[paperPDFs/CVPR_2026/Dynamic_Token_Reweighting_for_Robust_Vision_Language_Models.pdf]]
