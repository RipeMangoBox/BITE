---
title: Principled Steering via Null-space Projection for Jailbreak Defense in Vision-Language Models
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Principled_Steering_via_Null_space_Projection_for_Jailbreak_Defense_in_Vision_Language_Models.pdf
project_link: null
code_link: null
aliases:
- PSNSPJDVLM
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 良性激活零空间上的投影矩阵 P（确保更新只作用于与良性激活正交的方向）
primary_logic: 将激活转向变换完全约束在良性激活的零空间内，可以使良性提示的不变性得到理论保证，同时对有害激活产生定向的拒绝转向，从而在实现安全增强的同时保持模型的通用性能。
claims:
- 在 MiniGPT-4 的无约束攻击下，NullSteer 将毒性得分降至 2.89%，ASR 降至 7.32%，显著优于 ASTRA（4.48% / 9.09%）
- 在良性基准 MM-Vet、MMBench 和 XSTest 上，NullSteer 保持与未防御模型相当甚至更好的性能，避免过拒绝
- 在域外泛化实验中，NullSteer 在结构化、扰动和纯文本攻击上均取得最低 ASR，显示转向方向具有可迁移性
- Toxicity (MiniGPT-4, unconstrained attack) 上 Toxicity Score (%) = 2.89
---

# Principled Steering via Null-space Projection for Jailbreak Defense in Vision-Language Models

> [!tip] 核心洞察
> 将激活转向变换完全约束在良性激活的零空间内，可以使良性提示的不变性得到理论保证，同时对有害激活产生定向的拒绝转向，从而在实现安全增强的同时保持模型的通用性能。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于零空间投影的原则性激活转向：视觉语言模型越狱防御 |
| 英文题名 | Principled Steering via Null-space Projection for Jailbreak Defense in Vision-Language Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.22094) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | NullSteer |
| Dataset | Toxicity, Jailbreak, MM-Vet, XSTest |

> [!tip] 效果简介
> - Toxicity (MiniGPT-4, unconstrained attack) 上，Toxicity Score (%) 2.89 vs 4.48 (ASTRA) (-1.59)。
> - Jailbreak (MiniGPT-4, unconstrained attack) 上，ASR (%) 7.32 vs 9.09 (ASTRA) (-1.77)。
> - Toxicity (Qwen2-VL, ε=32/255) 上，Toxicity Score (%) 3.51 vs 5.45 (ASTRA) (-1.94)。

## 概要

视觉语言模型（VLMs）在安全对齐后仍易受越狱攻击——攻击者通过在图像中注入不可见扰动或构造对抗性文本，诱导模型生成有害内容。现有的激活转向（activation steering）防御方法在推理时向隐藏状态注入固定的“拒绝方向”向量，虽能抑制有害输出，却缺乏对良性查询的理论保证：拒绝向量对所有输入施加无差别偏移，导致良性查询也被错误拒绝（过拒绝），严重损害模型的通用能力（Figure 1）。这一瓶颈源于转向方向的选择缺乏原则性约束——它无法区分有害激活与良性激活，因而无法在安全增强与效用保持之间取得平衡。

本文提出 **NullSteer**，一种基于零空间投影的原则性激活转向框架。其核心洞见是：**将激活转向变换完全约束在良性激活的零空间内**，使转向更新仅作用于与良性表示正交的方向。这一设计从理论上保证了良性提示的激活不变性（$ \Delta \mathbf{H}_b = \mathbf{0} $），同时对有害激活产生定向的拒绝转向。NullSteer 首先从良性多模态输入的隐藏状态中建模良性子空间，通过 SVD 提取其零空间并构造投影矩阵 $\mathbf{P}$；随后，在零空间约束下，通过闭式优化目标同时对齐拒绝语义并抑制有害方向，求解出转向变换矩阵 $\tilde{\Delta}^\star$；推理时仅需应用 $\mathbf{h}' = \mathbf{h} + \lambda \tilde{\Delta}^\star \mathbf{P} \mathbf{h}$，即可实现对有害输入的精准干预。

实验结果表明，NullSteer 在安全性和通用性上均显著优于现有方法。在 MiniGPT-4 的无约束攻击下，NullSteer 将毒性得分降至 2.89%，越狱成功率（ASR）降至 7.32%，优于 ASTRA（4.48% / 9.09%）等强基线（Table 1）。在良性基准 MM-Vet、MMBench 和 XSTest 上，NullSteer 保持与未防御模型相当甚至更好的性能，避免了过拒绝问题（Table 2）。域外泛化实验中，NullSteer 在结构化攻击、扰动攻击和纯文本攻击上均取得最低 ASR，验证了其转向方向的可迁移性（Table E）。消融实验进一步证实，零空间约束、拒绝对齐和有害抑制三者的协同是实现安全-效用最优平衡的关键。

视觉语言模型（VLM）在图像理解与文本生成任务中展现了强大的能力，但其对多模态输入的开放性也使其易受越狱攻击——攻击者通过构造恶意图像或文本提示，诱导模型生成有害内容。这一问题严重制约了 VLM 在安全敏感场景中的部署。

现有的 VLM 安全防御方法大致分为三类：（1）**系统提示方法**，如 **Self-Reminder**（Xie et al., Nat. Mach. Intell., 2023），通过在输入中加入安全提示约束模型行为，但容易被精心设计的越狱提示绕过；（2）**输入扰动检测方法**，如 **JailGuard**（Zhang et al., arXiv 2023），试图在输入端识别恶意扰动，但面对自适应攻击时检测能力有限；（3）**激活转向方法**，如 **ASTRA**（Wang et al., CVPR 2025）和 **Refusal Pairs**（Rimsky et al., ACL 2024），在推理时直接修改模型的隐藏层激活，将输出导向拒绝方向。

激活转向方法因其无需重新训练、推理时开销低的优势，近年来受到广泛关注。其核心思想是在解码器的隐藏状态上注入一个缩放的拒绝方向向量：

$$ \mathbf{h}^{(l)'} = \mathbf{h}^{(l)} + \lambda \mathbf{r}^{(l)} $$

其中 $\mathbf{r}^{(l)}$ 通常由拒绝样本与服从样本的隐藏状态均值差估计得到。然而，该方法存在一个关键瓶颈：**固定的拒绝向量对所有输入施加无差别的偏向**，导致良性查询的隐藏表示也被偏移，引发“过拒绝”（over-refusal）问题——模型错误地拒绝回答安全的用户请求，显著损害通用能力。Figure 1 直观展示了这一困境：注入拒绝向量虽然能缓解有害输出，但也会使良性查询被错误拒绝。

这一问题的本质在于，现有方法缺乏对“何时转向、向何处转向”的原则性约束。转向向量的选择和注入缺乏理论解释性，使得安全增强与通用能力保持之间难以取得平衡。具体而言，若能将转向变换完全约束在“不影响良性表示”的方向上，则可以在理论上保证良性提示的不变性，同时仅对有害激活产生定向的拒绝转向。

这一洞察驱动了本文的核心动机：**利用良性激活的零空间作为转向的可行域**，构建一个有理论保证的激活转向框架，在实现安全防御的同时保持模型的通用性能。

## 核心方法与创新机理

NullSteer 的核心创新在于将激活转向（activation steering）从“全局偏移”重新定义为“零空间约束下的定向变换”，从根本上解决了现有方法中安全性与通用能力不可兼得的瓶颈。

### 1. 从无约束转向到零空间投影

传统的激活转向防御方法（如 **Refusal Pairs** (Rimsky et al., ACL 2024)、**ASTRA** (Wang et al., CVPR 2025)）在推理时直接向隐藏状态注入固定的拒绝方向向量：

$$ \mathbf { h } ^ { ( l ) ^ { \prime } } = \mathbf { h } ^ { ( l ) } + \lambda \mathbf { r } ^ { ( l ) } $$

其中拒绝方向 $\mathbf{r}^{(l)}$ 通常由拒绝样本与服从样本的均值差估计（Eq. 3）。这一操作对所有输入施加无差别的偏向，导致良性查询的隐藏表示也被推向拒绝区域，引发严重的过拒绝（overrefusal）问题（Figure 1）。

NullSteer 的关键改变在于引入**良性激活零空间投影矩阵 $\mathbf{P}$**，将转向变换约束为：

$$ \mathbf { h } ^ { ( l ) ^ { \prime } } = \mathbf { h } ^ { ( l ) } + \lambda \tilde { \Delta } ^ { \star ( l ) } \mathbf { P } ^ { ( l ) } \mathbf { h } ^ { ( l ) } $$

这一形式保证了 $\Delta \mathbf{H}_b = \mathbf{0}$：任何落在良性激活子空间内的表示，其转向更新恒为零（Eq. 4, Section 3.2）。因此，**良性提示的隐藏状态获得理论不变性保证**，从根本上消除了过拒绝的成因。

### 2. 从启发式方向估计到闭式优化求解

传统方法的拒绝方向 $\mathbf{r}$ 是启发式估计的单一向量，缺乏对有害语义方向的显式建模，且方向选择缺乏理论依据。NullSteer 将转向变换 $\tilde{\Delta}$ 的构造转化为一个**闭式优化问题**：

$$ \tilde { \mathbf { A } } ^ { \star } = ( \mathbf { R } + \beta \mathbf { V } ) \mathbf { H } _ { m } ^ { \top } \mathbf { P } ^ { \top } \big ( \mathbf { P } \mathbf { H } _ { m } \mathbf { H } _ { m } ^ { \top } \mathbf { P } ^ { \top } + ( \alpha + \beta ) \mathbf { P } \mathbf { P } ^ { \top } \big ) ^ { + } $$

该目标函数（Eq. 14）同时包含三个组件：
- **拒绝对齐项**：使恶意激活 $\mathbf{H}_m$ 经变换后逼近目标拒绝激活 $\mathbf{R}$；
- **有害抑制项**：通过遮罩视觉显著区域提取的有害方向 $\mathbf{V}$ 被显式抑制；
- **平滑正则项**：控制变换矩阵的 Frobenius 范数，防止过拟合。

消融实验（Table 3）证实，三者缺一不可：仅保留拒绝对齐项时毒性得分和越狱成功率显著上升，同时加入有害抑制和平滑正则才能达到最优的安全-效用平衡。

### 3. changed slots 总结

| 设计维度 | 基线方法 | NullSteer | 关键公式 |
|---------|---------|-----------|---------|
| 转向变换形式 | $\mathbf{h}' = \mathbf{h} + \lambda \mathbf{r}$ | $\mathbf{h}' = \mathbf{h} + \lambda \tilde{\Delta} \mathbf{P} \mathbf{h}$ | Eq. (2) vs Eq. (16) |
| 转向方向构造 | 拒绝/服从均值差估计 | 闭式优化同时对齐拒绝语义并抑制有害方向 | Eq. (3) vs Eq. (15) |
| 对良性输入的影响 | 全局偏移，导致过拒绝 | $\Delta \mathbf{P} \mathbf{h}_b = 0$，理论保证不变性 | Eq. (4), Section 3.2 |

### 4. 创新带来的实证收益

这一原则性设计在实验中转化为显著的性能优势。在 MiniGPT-4 的无约束攻击下，NullSteer 将毒性得分降至 **2.89%**，越狱成功率降至 **7.32%**，均优于最强的基线 ASTRA（4.48% / 9.09%）（Table 1）。更重要的是，在 MM-Vet、MMBench 和 XSTest 等良性基准上，NullSteer 保持了与未防御模型相当甚至更好的性能（Table 2），验证了零空间约束对通用能力的保护效果。域外泛化实验（Table E）进一步表明，这一约束下学到的转向方向具有跨攻击类型的可迁移性。

NullSteer 的整体设计围绕一个核心约束展开：**将激活转向变换完全限制在良性激活的零空间内**。这一约束从理论上保证了良性提示的隐藏状态在推理时保持不变，从而从根本上解决了现有激活转向方法（如 ASTRA、Refusal Pairs）中普遍存在的过拒绝问题。

### Pipeline 总览

NullSteer 的工作流分为四个阶段，如图 Figure 2 所示：

![[assets/figures/papers/paper_list_l775_https_arxiv_org_abs_2603_22094/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the proposed NullSteer framework. Given multimodal inputs, image and text embeddings are encoded and fed into the large language model. During inference, NullSteer applies activation steering within the null space of benign representations, ensuring that harmful activations are redirected toward refusal semantics while preserving benign behaviors*

1. **良性子空间建模（离线）**  
   收集一组良性多模态输入的隐藏状态，计算其协方差矩阵，通过奇异值分解（SVD）提取零空间，并构造投影矩阵 $P$。该矩阵满足 $P H_b = 0$，即任何落在良性激活张成子空间内的向量经 $P$ 投影后为零。

2. **拒绝方向与有害方向提取（离线）**  
   利用恶意输入（如对抗扰动图像 + 有害文本）获取目标拒绝激活 $R$；同时通过遮罩视觉显著区域，从恶意激活中分离出纯粹的有害方向 $V$，用于后续优化中的抑制项。

3. **稀疏优化求解转向矩阵 $\tilde{\Delta}$（离线）**  
   在零空间约束下，将转向变换参数化为 $\Delta = \tilde{\Delta} P$，并通过最小化一个加权目标函数——包含拒绝对齐项、有害抑制项和平滑正则项——得到闭式解 $\tilde{\Delta}^\star$。该解在所有满足约束的变换中具有最小 Frobenius 范数。

4. **推理时转向（在线）**  
   对每一层解码器的隐藏状态应用更新：
   $$h^{(l)'} = h^{(l)} + \lambda \tilde{\Delta}^{\star(l)} P^{(l)} h^{(l)}$$
   由于 $P^{(l)} h_b^{(l)} = 0$，良性输入的更新量为零；只有当输入包含有害特征、其激活在零空间中有非零分量时，转向才会生效。

### 与基线方法的本质差异

| 设计维度 | 基线激活转向（ASTRA / Refusal Pairs） | NullSteer |
|---------|--------------------------------------|-----------|
| 转向变换形式 | $h' = h + \lambda r$，其中 $r$ 为固定拒绝方向向量 | $h' = h + \lambda \tilde{\Delta} P h$，$\tilde{\Delta}$ 通过优化求解 |
| 转向方向构造 | 拒绝与服从样本的均值差估计（Eq. 3） | 闭式优化目标同时对齐拒绝语义 $R$ 并抑制有害方向 $V$，受 $P$ 约束（Eq. 14-15） |
| 对良性输入的影响 | $\lambda r$ 对所有输入施加偏向，导致良性表示偏移 | $\Delta P h_b = 0$，良性激活理论上完全不变（Eq. 4） |

这一设计使得 NullSteer 在实现安全增强的同时，在 MM-Vet、MMBench 和 XSTest 等良性基准上保持了与未防御模型相当甚至更好的性能（Table 2），从根本上避免了过拒绝。

### 3.1 激活转向的数学形式与过拒绝问题

视觉语言模型（VLM）的自回归生成过程可形式化为：

$$y _ { t } \sim \pi _ { \theta } ( \cdot \mid [ \mathbf { Z } , \mathbf { X } ] , y _ { < t } ) , \quad t = 1 , \ldots , T$$

其中 $\mathbf{Z}$ 为视觉嵌入，$\mathbf{X}$ 为文本嵌入，$y_{<t}$ 为已生成的 token 序列。

现有激活转向防御（如 **Refusal Pairs** (Rimsky et al., ACL 2024)、**ASTRA** (Wang et al., CVPR 2025)）在推理时对第 $l$ 层解码器隐藏状态施加加性偏移：

$$\mathbf { h } ^ { ( l ) ^ { \prime } } = \mathbf { h } ^ { ( l ) } + \lambda \mathbf { r } ^ { ( l ) }$$

其中 $\mathbf{r}^{(l)}$ 为拒绝方向向量，通常由拒绝样本与服从样本的均值差估计：

$$\mathbf { r } ^ { ( l ) } = \frac { 1 } { \vert \mathcal { D } _ { r } \vert } \sum _ { \mathbf { h } ^ { ( l ) } \in \mathcal { D } _ { r } } \mathbf { h } ^ { ( l ) } - \frac { 1 } { \vert \mathcal { D } _ { c } \vert } \sum _ { \mathbf { h } ^ { ( l ) } \in \mathcal { D } _ { c } } \mathbf { h } ^ { ( l ) }$$

**核心瓶颈**：该方案对*所有*输入施加相同的 $\lambda\mathbf{r}^{(l)}$ 偏移，导致良性查询的隐藏表示也被推向拒绝方向，引发过拒绝（Figure 1 示意），显著损害模型的通用能力。

### 3.2 良性不变性约束与零空间投影

NullSteer 的核心洞察是将转向变换 $\Delta$ 完全约束在良性激活的零空间内。设 $\mathbf{H}_b \in \mathbb{R}^{d \times N_b}$ 为 $N_b$ 个良性多模态输入的隐藏状态矩阵，则良性不变性约束为：

$$\Delta \mathbf { H } _ { b } = \mathbf { 0 }$$

这意味着 $\Delta$ 的行向量必须位于 $\mathbf{H}_b$ 行空间的正交补中，即 $\mathbf{H}_b$ 的零空间：

$$\mathrm { N u l l } ( \mathbf { H } _ { b } ) = \{ \mathbf { x } \in \mathbb { R } ^ { d } \mid \mathbf { x } ^ { \top } \mathbf { H } _ { b } = \mathbf { 0 } \}$$

为参数化该约束，将 $\Delta$ 分解为可学习矩阵与零空间投影的乘积：

$$\Delta = \tilde { \Delta } \mathbf { P }$$

其中投影矩阵 $\mathbf{P}$ 通过以下步骤构造：
1. 收集良性激活 $\mathbf{H}_b$，计算协方差矩阵 $\mathbf{H}_b\mathbf{H}_b^\top$；
2. 通过 SVD 提取零空间奇异向量 $\hat{\mathbf{U}}$（对应零奇异值）；
3. 构造投影矩阵：

$$\mathbf { P } = { \hat { \mathbf { U } } } { \hat { \mathbf { U } } } ^ { \top }$$

该构造保证 $\mathbf{P}\mathbf{H}_b = \mathbf{0}$，从而 $\Delta\mathbf{H}_b = \tilde{\Delta}\mathbf{P}\mathbf{H}_b = \mathbf{0}$，使良性激活严格不变。

### 3.3 转向方向的闭式优化求解

在零空间约束下，转向方向 $\tilde{\Delta}$ 需同时满足三个目标：

1. **拒绝对齐**：将恶意激活 $\mathbf{H}_m$ 映射到目标拒绝激活 $\mathbf{R}$；
2. **有害抑制**：抑制有害方向 $\mathbf{V}$（通过遮罩视觉显著区域提取）；
3. **平滑正则**：约束 $\tilde{\Delta}$ 的 Frobenius 范数，防止过拟合。

综合优化目标为：

$$\tilde{\pmb{\Delta}}^{\star} = \arg \min_{\tilde{\pmb{\Delta}}} \Big( \| \tilde{\pmb{\Delta}} \mathbf{P} \mathbf{H}_m - \mathbf{R} \|_F^2 + \beta \| \tilde{\pmb{\Delta}} \mathbf{P} \mathbf{V} \|_F^2 + \alpha \| \tilde{\pmb{\Delta}} \mathbf{P} \|_F^2 \Big)$$

该问题具有闭式最小范数解：

$$\tilde { \mathbf { A } } ^ { \star } = ( \mathbf { R } + \beta \mathbf { V } ) \mathbf { H } _ { m } ^ { \top } \mathbf { P } ^ { \top } \big ( \mathbf { P } \mathbf { H } _ { m } \mathbf { H } _ { m } ^ { \top } \mathbf { P } ^ { \top } + ( \alpha + \beta ) \mathbf { P } \mathbf { P } ^ { \top } \big ) ^ { + }$$

其中 $(\cdot)^+$ 表示 Moore-Penrose 伪逆，$\alpha$、$\beta$ 为平衡超参数。

### 3.4 推理时转向

推理时，对每层解码器隐藏状态应用约束后的更新：

$$\mathbf { h } ^ { ( l ) ^ { \prime } } = \mathbf { h } ^ { ( l ) } + \lambda \tilde { \Delta } ^ { \star ( l ) } \mathbf { P } ^ { ( l ) } \mathbf { h } ^ { ( l ) }$$

**关键性质**：当输入为良性时，$\mathbf{P}^{(l)}\mathbf{h}^{(l)}$ 落在良性子空间内，投影后为零，更新项消失；当输入包含有害特征时，$\mathbf{P}^{(l)}\mathbf{h}^{(l)}$ 的非零分量经 $\tilde{\Delta}^{\star(l)}$ 变换后产生定向拒绝偏移。这一机制从理论上保证了安全增强与通用性能的兼容。

### 3.5 方法谱系与知识库定位

NullSteer 在激活转向防御谱系中引入了**零空间约束**这一新维度：

| 方法 | 转向变换形式 | 转向方向构造 | 对良性输入的影响 |
|------|-------------|-------------|-----------------|
| Refusal Pairs / ASTRA | $\mathbf{h}' = \mathbf{h} + \lambda\mathbf{r}$ | 拒绝-服从均值差估计 | $\lambda\mathbf{r}$ 对所有输入施加偏向 |
| **NullSteer** | $\mathbf{h}' = \mathbf{h} + \lambda\tilde{\Delta}\mathbf{P}\mathbf{h}$ | 闭式优化，联合对齐拒绝语义并抑制有害方向 | $\Delta\mathbf{P}\mathbf{h}_b = \mathbf{0}$，良性激活不变 |

与 **Self-Reminder** (Xie et al., Nat. Mach. Intell., 2023) 的系统提示方法、**JailGuard** (Zhang et al., arXiv 2023) 的输入扰动检测方法相比，NullSteer 属于**表示层干预**范式，无需修改输入或微调模型参数，且通过理论保证避免了过拒绝问题。

## 实验与关键发现

### 核心防御效果

NullSteer 在多种视觉语言模型和攻击强度下均展现出显著的安全对齐能力。Table 1 汇总了不同防御方法在扰动攻击下的毒性得分（Toxicity Score）与越狱成功率（ASR）对比。在 MiniGPT-4 的无约束攻击设定下，NullSteer 将毒性得分降至 **2.89%**，ASR 降至 **7.32%**，相比最强的激活转向基线 ASTRA（4.48% / 9.09%）分别降低了 1.59 和 1.77 个百分点。在 Qwen2-VL 模型上，当对抗扰动强度 ε=32/255 时，NullSteer 的毒性得分为 3.51%，ASR 为 4.55%，同样优于 ASTRA 的 5.45% 和 5.00%。

![[assets/figures/papers/paper_list_l775_https_arxiv_org_abs_2603_22094/figures/003_Table_1.jpg]]
*Table 1: Defense comparisons across different VLMs. Lower values (↓) indicate stronger robustness. Steering vectors for each ϵ are derived from adversarial examples generated under the same perturbation level. The best results are highlighted in bold*

上述结果的核心机理在于零空间投影的约束：传统激活转向方法（如 Refusal Pairs 和 ASTRA）对所有输入施加固定的拒绝方向偏移，导致良性查询的隐藏表示被污染，而 NullSteer 的转向更新 $\tilde{\Delta} \mathbf{P} \mathbf{h}$ 仅在良性激活的零空间内生效，对良性输入天然满足 $\Delta \mathbf{H}_b = \mathbf{0}$，从而在拒绝有害内容的同时不损害正常功能。

### 域内迁移与自适应攻击鲁棒性

Figure 3 展示了 NullSteer 在域内（ID）条件下的迁移性能。当转向向量在某一扰动强度 ε 下学习后，直接应用于其他 ε 下的对抗样本时，NullSteer 仍能维持较低的毒性得分和越狱率，表明学到的转向方向具有跨扰动强度的泛化能力。

![[assets/figures/papers/paper_list_l775_https_arxiv_org_abs_2603_22094/figures/004_Figure_3.jpg]]
*Figure 3: Transferability performance under ID conditions*

在更严苛的自适应攻击场景下（Figure 4），攻击者可以针对防御机制优化对抗样本。即使在此白盒设定下，NullSteer 依然将 MiniGPT-4 的越狱 ASR 从无防御时的 49.1% 降至 19.3%（ε=64/255），在所有 ε 取值下均取得最低的越狱率。这一鲁棒性源于 NullSteer 的转向方向由闭式优化求解得到，而非简单的均值差估计，使其对攻击者的适应性扰动具有更强的抵抗力。

### 效用保持与过拒绝避免

Table 2 报告了各方法在良性基准上的效用表现。在 MM-Vet 综合视觉理解评测上，NullSteer 得分为 21.05，略高于未防御的原始模型（19.40），表明零空间约束不仅避免了效用损失，还带来了轻微的正向收益。在专门评估过拒绝的 XSTest 基准上，NullSteer 得分为 87.80，与原始模型（87.60）几乎持平，证明其不会将正常的边界指令误判为有害请求。

![[assets/figures/papers/paper_list_l775_https_arxiv_org_abs_2603_22094/figures/006_Table_2.jpg]]
*Table 2: Utility performance in benign and adversarial scenarios*

相比之下，ASTRA 和 Refusal Pairs 等方法在 MM-Vet 上的得分分别为 15.24 和 16.33，均显著低于原始模型，验证了固定拒绝方向注入会导致严重的过拒绝问题。NullSteer 通过将转向完全约束在良性激活零空间内，从理论上保证了 $\mathbf{P} \mathbf{h}_b = \mathbf{0}$，从而在安全增强与效用保持之间取得了原则性平衡。

### 消融实验

Table 3 的消融实验揭示了目标函数各组件的作用。完整的 NullSteer 目标包含三个关键项：拒绝对齐项 $\|\tilde{\Delta} \mathbf{P} \mathbf{H}_m - \mathbf{R}\|_F^2$、有害抑制项（通过有害方向矩阵 $\mathbf{V}$ 加权）和平滑正则项 $\|\tilde{\Delta} \mathbf{P}\|_F^2$。移除任意一项均会导致毒性得分或越狱率上升。仅使用拒绝对齐项时，MiniGPT-4 上的毒性得分升至 4.12%，ASR 升至 10.45%；加入有害抑制后，毒性降至 3.45%，ASR 降至 8.76%；同时加入平滑正则后达到最优的 2.89% 和 7.32%。这表明三者协同作用：拒绝对齐确保转向目标语义正确，有害抑制防止转向方向被恶意利用，平滑正则避免过拟合到少量恶意样本。

![[assets/figures/papers/paper_list_l775_https_arxiv_org_abs_2603_22094/figures/010_Table_3.jpg]]
*Table 3: Ablation study of different objective components on Minigpt-4*

### 参数敏感性分析

Figure 5 展示了良性激活数量 $N_b$ 对效用的影响。随着 $N_b$ 增加，模型在 MM-Vet 上的效用逐步提升，在 $N_b \approx 8$ 时趋于饱和，说明仅需少量代表性良性样本即可构建有效的零空间投影矩阵。

Figure 6 分析了恶意激活数量 $N_m$ 对安全性的影响。防御效果随 $N_m$ 增加而提升，但即使仅使用少量恶意样本（如 $N_m=4$），NullSteer 仍能显著降低毒性得分，显示出对恶意样本数量的低敏感性。

Figure 7 考察了转向强度 $\lambda$ 的影响。在 ε=16/255 扰动设定下，增大 $\lambda$ 可持续降低毒性得分和越狱 ASR，而 MM-Vet 上的效用得分保持稳定。这一安全-效用解耦特性是零空间约束的直接结果：$\lambda$ 仅放大零空间内的转向分量，不会侵入良性子空间。

### 域外泛化

Table E 报告了域外（OOD）泛化实验的结果。使用 Jailbreak 攻击样本（ε=16/255）学到的转向向量，直接应用于未见过的攻击类型——包括 MM-SafetyBench 的结构化攻击、PGD 扰动变体攻击和纯文本攻击——NullSteer 在所有场景下均取得最低的 ASR。这表明通过零空间约束和闭式优化得到的转向方向具有跨攻击类型的可迁移性，并非对特定训练分布的过拟合。

### 推理效率

Table 4 比较了各方法的每 token 推理时间。NullSteer 的推理时计算仅涉及矩阵-向量乘法 $\tilde{\Delta}^{\star(l)} \mathbf{P}^{(l)} \mathbf{h}^{(l)}$，额外开销极小，与无防御的原始模型相比几乎无延迟增加，适合实时部署场景。

![[assets/figures/papers/paper_list_l775_https_arxiv_org_abs_2603_22094/figures/012_Table_4.jpg]]
*Table 4: Inference time per token (ms). Average decoding latency is computed and normalized by the number of generated tokens. Reporting time per token enables a fair comparison of inference efficiency across models with varying output lengths. Lower values indicate faster decoding*

### 失败模式与局限性

尽管 NullSteer 在多数场景下表现优异，仍需注意以下局限。首先，零空间构建依赖少量代表性良性样本；若实际部署中良性输入分布极为多样，当前 $N_b \approx 8$ 的设定可能不足以完全覆盖，需手动验证是否需要增加样本量。其次，对于高逼真度的文本嵌入图像的结构化越狱攻击，虽然 Table E 显示 NullSteer 仍优于基线，但绝对 ASR 仍有降低空间。最后，所有实验在 MiniGPT-4、LLaVA-v1.5 和 Qwen2-VL 上进行，在更大规模或最新架构 VLM 上的表现需进一步验证。

## 定位与知识库关联

### 1. 问题定位：激活转向防御的瓶颈

视觉语言模型（VLM）在安全对齐后仍易受多模态越狱攻击，尤其是基于对抗扰动的视觉越狱。在此背景下，激活转向（activation steering）成为一类轻量级推理时防御范式，其核心思路是在解码器的隐藏状态上注入一个固定的“拒绝方向向量” $\mathbf{r}$，将模型输出导向安全拒绝行为。该范式的基本形式为：

$$\mathbf{h}^{(l)'} = \mathbf{h}^{(l)} + \lambda \mathbf{r}^{(l)}$$

其中 $\mathbf{r}$ 通常由拒绝样本与服从样本的隐藏状态均值差估计（Eq. 3）。此类方法的代表包括 **Refusal Pairs**（Rimsky et al., ACL 2024）和 **ASTRA**（Wang et al., CVPR 2025）等。

然而，这一范式存在一个核心瓶颈：**固定的拒绝向量对所有输入施加无差别的偏向**。当良性查询进入模型时，$\lambda \mathbf{r}$ 同样会偏移其隐藏表示，导致模型对正常指令也产生拒绝行为——即“过拒绝”（overrefusal）。这不仅损害模型的通用能力，也暴露了现有方法在理论上的脆弱性：**转向向量的选择缺乏对良性表示不变性的形式化保证**。

### 2. 核心机制突破：零空间约束下的原则性转向

NullSteer 的核心洞察在于将激活转向变换完全约束在良性激活的零空间内，从而在机制层面解决了过拒绝问题。具体而言，该方法引入了一个关键的结构性组件——**良性激活零空间上的投影矩阵 $\mathbf{P}$**，确保转向更新只作用于与良性激活正交的方向：

$$\Delta = \tilde{\Delta} \mathbf{P}, \quad \text{其中 } \mathbf{P} \mathbf{H}_b = \mathbf{0}$$

这一约束带来了两个根本性变化：

| 设计维度 | 基线方法（ASTRA / Refusal Pairs） | NullSteer |
|---------|--------------------------------|-----------|
| **转向变换形式** | $\mathbf{h}' = \mathbf{h} + \lambda \mathbf{r}$，$\mathbf{r}$ 为固定向量 | $\mathbf{h}' = \mathbf{h} + \lambda \tilde{\Delta} \mathbf{P} \mathbf{h}$，$\tilde{\Delta}$ 通过闭式优化求解（Eq. 16） |
| **转向方向构造** | 由拒绝/服从样本的均值差估计（Eq. 3），单一方向 | 在 $\mathbf{P}$ 约束下同时对齐拒绝语义 $\mathbf{R}$ 并抑制有害方向 $\mathbf{V}$，通过多目标闭式优化得到（Eq. 14-15） |
| **对良性输入的影响** | $\lambda \mathbf{r}$ 对所有输入施加偏向，良性表示发生偏移 | $\Delta \mathbf{P} \mathbf{h}_b = \mathbf{0}$，良性激活理论上不变（Eq. 4） |

这种设计的理论优势在于：**良性提示的不变性得到保证**（转向更新在良性子空间上的投影为零），同时**对有害激活产生定向的拒绝转向**（有害激活在零空间上的分量被有效调制）。这使得 NullSteer 在安全增强与通用性能保持之间取得了可证明的平衡，而非依赖经验调参。

### 3. 与相关防御路线的对比

在 VLM 越狱防御的知识谱系中，NullSteer 与以下几类方法形成对照：

- **系统提示方法**：如 **Self-Reminder**（Xie et al., Nat. Mach. Intell., 2023），通过在输入中注入安全提示引导模型行为。此类方法实现简单，但容易被越狱模板绕过，且对视觉对抗扰动缺乏鲁棒性。

- **输入扰动检测方法**：如 **JailGuard**（Zhang et al., arXiv 2023），通过检测输入中的异常模式来拦截攻击。这类方法属于“检测-拒绝”范式，面临检测器本身被攻破的风险。

- **视觉到文本安全映射**：如 **ECSO**，通过将视觉内容转换为文本后进行安全检查。该方法引入了额外的模态转换开销，且可能丢失细粒度的视觉安全信息。

- **自适应激活转向**：如 **ASTRA**（Wang et al., CVPR 2025），在推理时动态调整转向方向和强度。这是与 NullSteer 最接近的基线，但 ASTRA 仍缺乏对良性表示不变性的形式化保证，其转向向量可能侵入良性激活空间。

NullSteer 的关键区分点在于：**它是首个将激活转向约束在良性零空间内的方法**，从而在理论上保证了安全干预不会以牺牲通用能力为代价。这一设计原则使其在方法谱系中占据了“原则性安全干预”的定位。

### 4. 适用边界与局限

尽管 NullSteer 在多个 VLM 和攻击场景下展现了优越性，其适用边界和局限值得关注：

- **模型覆盖范围有限**：当前验证仅在 MiniGPT-4-13B、LLaVA-v1.5-13B 和 Qwen2-VL-7B 上完成。尚未在更大规模（如 70B+）或最新架构的 VLM 上测试，其在更强基础模型上的表现需要进一步验证。

- **零空间构建对良性样本的依赖**：投影矩阵 $\mathbf{P}$ 的质量依赖于所收集的良性多模态激活的代表性。实验表明，随着良性激活数量 $N_b$ 增加，模型效用提升并在 $N_b \approx 8$ 时趋于饱和（Figure 5），说明少量代表性样本即可覆盖主要良性子空间。但若实际部署中良性分布极为多样（如开放域对话），可能需要更多样本或在线更新策略。

- **对复杂结构化越狱的防御仍有提升空间**：在域外泛化实验中（Table E），NullSteer 对结构化攻击、扰动变体和纯文本攻击均取得最低 ASR，显示出转向方向的可迁移性。但对于高逼真度文本嵌入图像的复杂越狱，其防御效果可能受限于视觉编码器对恶意文本的表示能力。

- **推理开销可控但非零**：每层解码器需执行一次矩阵-向量乘法 $\tilde{\Delta} \mathbf{P} \mathbf{h}$。Table 4 报告了每 token 推理时间的对比，NullSteer 的额外开销在可接受范围内，但对于实时应用场景，仍需考虑投影矩阵的存储和计算优化。

### 5. 开放问题与未来方向

NullSteer 的提出开启了若干值得探索的方向：

- **跨模态泛化**：零空间投影的核心思想——将安全干预约束在与良性表示正交的子空间内——是否可推广到其他模态（如音频、视频）的安全对齐任务？这需要定义相应模态的“良性子空间”并验证不变性约束的有效性。

- **投影矩阵的压缩与加速**：当前 $\mathbf{P}$ 的维度与隐藏状态维度相同，对于大模型可能存在内存瓶颈。是否可以通过低秩近似或稀疏化进一步压缩投影矩阵，使其适应边缘设备或实时应用？

- **自适应攻击下的鲁棒性边界**：Figure 4 显示，在白盒自适应攻击（攻击者同时优化扰动以绕过防御）下，NullSteer 仍保持最低的越狱率，在 $\epsilon = 64/255$ 时将 ASR 从 49.1% 降至 19.3%。但若攻击者同时扰动图像和文本模态，NullSteer 的鲁棒性边界在哪里？

- **转向强度 $\lambda$ 的自动化选择**：Figure 7 表明，增大 $\lambda$ 可持续降低不安全生成，而 MM-Vet 上的效用保持稳定，显示出良好的安全-效用平衡。但当前 $\lambda$ 仍需手动设定，能否设计自适应的 $\lambda$ 选择策略（如基于输入的有害特征强度动态调整）以进一步优化这一平衡？

## 原文 PDF

![[paperPDFs/CVPR_2026/Principled_Steering_via_Null_space_Projection_for_Jailbreak_Defense_in_Vision_Language_Models.pdf]]
