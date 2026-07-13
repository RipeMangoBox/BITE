---
title: "ATM: Enhanced Alignment for Text-to-Motion Generation"
type: paper
paper_level: A
venue: WACV
year: 2026
pdf_ref: "paperPDFs/WACV_2026/ATM:_Enhanced_Alignment_for_Text-to-Motion_Generation.pdf"
project_link: null
code_link: "https://github.com/ke-hanaca/ATM.git"
aliases:
- AATM
- ATM
tags:
- WACV_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
- topic/representation_self_supervised_transfer
core_operator: 引入语义感知的自适应监督：通过挖掘语义矛盾（inter-motion）和局部语义代理（intra-motion），对不同程度语义差异施加实例特定的对齐优化，从而校正全局和局部语义错位。
primary_logic: 在预训练的文本-动作对齐空间上，通过挖掘最小化生成距离与真实距离比值的负样本和局部代理，实现无需局部文本标注的无监督语义细化，同时自适应边界增强了模型学习结构化语义边界的能力。
claims:
- 添加L_inter和L_intra后，HumanML3D上R-Precision Top-1从0.425提升至0.519，FID从0.570降至0.320。
- 自适应margin在所有指标上均优于固定margin，R-Precision Top-1达到0.519，而固定margin最高仅0.420。
- L_inter在R-Precision Top-1上达到0.502，优于对比学习(0.473)和三元组损失(0.420)等。
- HumanML3D 上 R-Precision Top-1 = 0.519 (ATM)
---

# ATM: Enhanced Alignment for Text-to-Motion Generation

> [!tip] 核心洞察
> 在预训练的文本-动作对齐空间上，通过挖掘最小化生成距离与真实距离比值的负样本和局部代理，实现无需局部文本标注的无监督语义细化，同时自适应边界增强了模型学习结构化语义边界的能力。

| 字段 | 内容 |
|------|------|
| 中文题名 | ATM：增强的文本到动作生成对齐 |
| 英文题名 | ATM: Enhanced Alignment for Text-to-Motion Generation |
| 会议/期刊 | WACV 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/WACV2026/papers/Han_ATM_Enhanced_Alignment_for_Text-to-Motion_Generation_WACV_2026_paper.pdf) · [Code](https://github.com/ke-hanaca/ATM.git) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion #topic/representation_self_supervised_transfer |
| Method | ATM (Aligned Text-to-Motion) |
| Dataset | HumanML3D, KIT |

> [!tip] 效果简介
> - HumanML3D 上，R-Precision Top-1 0.519 (ATM) vs 0.425 (Baseline L_mse only) (+0.094)；FID 0.320 (ATM) vs 0.570 (Baseline) (-0.250)。
> - KIT 上，R-Precision Top-1 0.434 (ATM) vs 0.392 (Baseline) (+0.042)；FID 0.354 (ATM) vs 0.566 (Baseline) (-0.212)。

## 概要

文本到动作生成（Text-to-Motion, T2M）旨在根据自然语言描述合成逼真的三维人体动作序列。现有主流方法（如 **MDM** (Tevet et al., ICLR 2023)、**MoMask** (Guo et al., CVPR 2024)、**BAMM** (Pinyoanuntapong et al., ECCV 2024)）普遍依赖均方误差（MSE）损失监督骨骼关节位置精度，但缺乏显式的语义对齐机制。这导致两个层次的语义错位：**序列间错位**（inter-motion misalignment）——语义不同的文本生成过于相似的动作；**序列内错位**（intra-motion misalignment）——动作片段包含与文本不符的错误语义。Figure 1 展示了 MoMask 生成结果中的典型错位现象。

ATM（Aligned Text-to-Motion）的核心洞察是：在预训练的文本-动作对齐空间中，通过挖掘语义矛盾（最小化生成距离与真实距离比值的负样本）和局部语义代理，可以在无需局部文本标注的条件下实现无监督语义细化。ATM 引入两个关键模块：**Inter-motion Alignment** 通过自适应边界的三元组损失校正序列级全局语义错位；**Intra-motion Alignment** 通过正/负代理剪辑校正片段级局部语义错位。自适应边界根据真实语义距离动态调整优化强度，使模型能够学习结构化的语义边界。

实验表明，ATM 在 HumanML3D 和 KIT 两个基准上均取得显著提升。在 HumanML3D 上，将 ATM 应用于基线模型后，R-Precision Top-1 从 0.425 提升至 0.519（+0.094），FID 从 0.570 降至 0.320（-0.250）。消融实验验证了 inter-motion 和 intra-motion 损失的独立贡献及自适应边界相对于固定边界的优势。用户研究进一步证实 ATM 生成的动作在语义对齐性和真实感上均优于现有 SOTA 方法。



文本到动作生成（Text-to-Motion, T2M）旨在根据自然语言描述生成逼真的三维人体动作序列，在动画制作、虚拟现实和人机交互等领域具有广泛应用。近年来，基于扩散模型的方法如 **MDM**（Tevet et al., ICLR 2023）显著推进了这一领域的发展，而 **MoMask**（Guo et al., CVPR 2024）和 **BAMM**（Pinyoanuntapong et al., ECCV 2024）等后续工作进一步将生成质量推向新高。

然而，现有方法存在一个关键瓶颈：**它们普遍依赖回归损失（如均方误差 MSE）作为核心监督信号，缺乏显式的语义对齐机制**。MSE 损失仅约束生成动作与真实动作在骨骼位置层面的逐帧差异，却无法感知和纠正跨动作序列或动作内部的语义不一致。这导致两类典型的语义错位问题（见图 1）：

- **序列间错位（Inter-motion misalignment）**：语义上不同的文本描述生成了过于相似的动作序列。例如，“一个人向前走”和“一个人踱步”在骨骼结构上可能高度相似，但语义意图截然不同，MSE 损失无法区分这种差异。
- **序列内错位（Intra-motion misalignment）**：动作序列内部的局部片段未能准确反映文本中的特定语义。例如，“一个人坐下然后挥手”中，“挥手”的动作片段可能被错误地执行为其他手势。

这些语义错位问题的根源在于：**回归损失仅提供低层次的骨骼精度监督，而文本-动作对齐这一高层次的语义关系完全未被显式建模**。因此，模型难以学习到结构化语义边界——即哪些动作差异是语义相关的、哪些是不相关的。

针对上述缺口，本文提出 **ATM（Aligned Text-to-Motion）**，其核心动机是：**在预训练的文本-动作对齐空间中引入语义感知的自适应监督，在不依赖额外局部文本标注的前提下，系统性地校正全局和局部语义错位**。具体而言，ATM 通过两个互补的对齐模块实现这一目标——挖掘序列间语义矛盾的 Inter-motion Alignment 和利用局部语义代理的 Intra-motion Alignment——从而将语义对齐从隐式期望转化为显式优化目标。



## 核心方法与创新机理

ATM 的核心创新在于**将语义感知的自适应监督引入文本到动作（T2M）生成的训练过程**，从根本上改变了模型学习语义对齐的方式。

### 问题诊断：回归损失的语义盲区

现有扩散式 T2M 方法（如 **MDM**，Tevet et al., ICLR 2023）仅依赖均方误差损失 $\mathcal{L}_{mse} = \| \pmb{m}_i - \hat{\pmb{m}}_i \|_2^2$ 监督骨骼位置精度。这种纯回归范式存在根本性的语义盲区：它无法感知生成动作与文本描述之间的语义一致性，导致两类典型错位——

- **序列间错位（inter-motion misalignment）**：语义不同的文本描述生成了过于相似的动作序列；
- **序列内错位（intra-motion misalignment）**：单个动作序列中存在局部语义不准确的片段。

### 核心机制：双重自适应语义对齐

ATM 在预训练的文本-动作对齐嵌入空间上构建了两层自适应监督，分别对应上述两类错位：

**1. 序列间对齐（Inter-motion Alignment）**

通过挖掘语义矛盾样本实现全局语义校正。具体而言，对于每个生成动作 $\hat{\pmb{m}}_i$，在 mini-batch 中寻找使其生成距离与真实距离比值最小的样本作为错位示例：

$$\hat{\pmb{m}}_i^h = \hat{\pmb{m}}_{j^*}, \text{ where } j^* = \arg\min_{j \neq i} \frac{\mathcal{D}(\hat{\pmb{m}}_i, \hat{\pmb{m}}_j)}{\mathcal{D}(\pmb{m}_i, \pmb{m}_j)}$$

随后施加自适应边界的三元组损失：

$$\mathcal{L}_{inter} = \max\{0, \mathcal{D}(t_i, \hat{m}_i) - \mathcal{D}(t_i, \hat{m}_i^h) + \phi_{ter}\}$$

其中自适应边界 $\phi_{ter} = \mathcal{D}(t_i, m_i^h) - \mathcal{D}(t_i, m_i)$ 根据真实语义距离动态调整优化强度——语义差异越大，边界越宽，优化力度越强。

**2. 序列内对齐（Intra-motion Alignment）**

无需局部文本标注，通过语义代理实现无监督的局部语义细化。首先识别生成动作中最不对齐的局部剪辑 $\hat{c}$，然后在 mini-batch 中分别挖掘正代理 $\hat{c}_{pos}$（应相似但当前不相似）和负代理 $\hat{c}_{neg}$（应不相似但当前相似），施加剪辑级自适应三元组损失：

$$\mathcal{L}_{intra} = \max\{0, \mathcal{D}(\hat{c}, \hat{c}_{pos}) - \mathcal{D}(\hat{c}, \hat{c}_{neg}) + \phi_{tra}\}$$

该损失仅在生成与真实动作序列存在显著语义差异（$\cos(\hat{m}_i, m_i) < \gamma$）时激活，避免对已对齐序列的过度优化。

### 关键设计：自适应边界 vs. 固定边界

自适应边界是 ATM 区别于传统度量学习的关键设计。传统三元组损失使用固定 margin，无法适应不同程度的语义错位。ATM 的 $\phi_{ter}$ 和 $\phi_{tra}$ 直接从真实数据的语义距离中导出，使模型能够学习结构化的语义边界。消融实验（Table 4）证实：自适应 margin 在所有指标上均显著优于固定 margin（R-Precision Top-1 达到 0.519，而固定 margin 最高仅 0.420）。

### 与 Baseline 的 Changed Slots 总结

| 组件 | Baseline（纯回归） | ATM |
|------|-------------------|-----|
| 损失函数 | 仅 $\mathcal{L}_{mse}$ | $\mathcal{L}_{mse} + \lambda(\mathcal{L}_{inter} + \mathcal{L}_{intra})$ |
| 语义对齐策略 | 无显式语义监督 | 序列级 + 剪辑级自适应三元组损失 |
| 优化边界 | 不适用 | 基于真实语义距离的自适应 margin |

总体损失函数为 $\mathcal{L}_{all} = \mathcal{L}_{mse} + \lambda \cdot (\mathcal{L}_{inter} + \mathcal{L}_{intra})$，其中 $\mathcal{L}_{mse}$ 保持对骨骼精度的基础监督，两个对齐损失作为语义感知的补充信号，共同驱动生成动作向文本语义靠拢。



ATM（Aligned Text-to-Motion）在现有文本到动作生成模型的基础上，引入了一个预训练的文本-动作对齐嵌入空间，并在此空间内施加两类语义感知的自适应对齐损失，从而在不依赖局部文本标注的条件下，同时校正序列级和剪辑级的语义错位。

**核心瓶颈与解决思路。** 现有方法（如 **MDM** (Tevet et al., ICLR 2023)）仅依赖均方误差损失 $\mathcal{L}_{mse}$ 监督骨骼位置精度：

$$\mathcal { L } _ { m s e } = \| \pmb { m } _ { i } - \hat { \pmb { m } } _ { i } \| _ { 2 } ^ { 2 }$$

这种纯回归目标缺乏显式语义监督，导致两个典型问题：不同语义的文本生成出过于相似的动作（inter-motion misalignment），以及同一动作序列内部出现语义不准确的局部片段（intra-motion misalignment）。ATM 的核心洞察是：在预训练的文本-动作对齐空间上，通过挖掘生成距离与真实距离比值最小/最大的样本作为负样本或局部代理，可以无监督地细化语义对齐，而自适应边界则使模型能够根据语义差异程度灵活调整优化强度。

**Pipeline 模块与数据流。** ATM 的整体框架由以下模块串联构成：

1. **Text Encoder**：将输入文本描述编码为嵌入向量，作为后续对齐空间的查询锚点。
2. **Motion Generator**（如 MDM 等扩散模型）：从文本嵌入生成动作序列 $\hat{m}_i$。该模块保持原有架构不变，ATM 仅在其输出端施加额外损失。
3. **MSE Loss（$\mathcal{L}_{mse}$）**：基础回归损失，监督生成动作与真实动作 $m_i$ 之间的骨骼位置精度。
4. **Inter-motion Alignment Module**：在 mini-batch 内，对每个生成序列 $\hat{m}_i$，通过最小化生成距离与真实距离的比值 $\frac{\mathcal{D}(\hat{m}_i, \hat{m}_j)}{\mathcal{D}(m_i, m_j)}$ 挖掘语义矛盾最严重的序列对 $\hat{m}_i^h$，随后施加自适应边界的三元组损失 $\mathcal{L}_{inter}$，校正序列间全局语义错位。
5. **Intra-motion Alignment Module**：首先识别每个生成序列中最不对齐的局部剪辑 $\hat{c}$（即与对应真实剪辑距离最大的片段），然后在 mini-batch 中通过距离比值分别选取正代理 $\hat{c}_{pos}$（应相似但当前不相似）和负代理 $\hat{c}_{neg}$（应不相似但当前相似），施加自适应边界的剪辑级三元组损失 $\mathcal{L}_{intra}$。该损失仅在整段生成与真实动作余弦相似度低于阈值 $\gamma$ 时激活，以避免对已对齐序列的过度校正。

最终总损失为三者的加权组合：

$$\mathcal { L } _ { a l l } = \mathcal { L } _ { m s e } + \lambda \cdot ( \mathcal { L } _ { i n t e r } + \mathcal { L } _ { i n t r a } )$$

**与 SOTA 方法的集成。** ATM 作为即插即用的对齐模块，可直接附加于 **MDM** (Tevet et al., ICLR 2023)、**MoMask** (Guo et al., CVPR 2024)、**BAMM** (Pinyoanuntapong et al., ECCV 2024) 等主流生成器之上。实验表明（Table 1, Table 2），添加 ATM 后各基线在 HumanML3D 和 KIT 数据集上的 R-Precision 和 FID 均获得显著提升，验证了该框架的通用性。

**局限性。** 需注意，基于 VQ-VAE 的离散动作表示模型（如 MoMask）因 token 不可微，无法直接应用本对齐损失；此外，intra-motion alignment 依赖生成与真实运动间的时间对齐假设，时间错位可能影响剪辑相似度计算的准确性。

### 补充图表

![[assets/figures/papers/paper_list_l3314_https_openaccess_thecvf_com_content_WACV2026_papers_Han_ATM_Enhanced_Ali/figures/002_Figure_2.jpg]]
*Figure 2: (1) The Aligned Text-to-Motion (ATM) generation framework. In a pre-trained text-motion alignment space, ATM performs inter-motion alignment by correcting motion sequences that are structurally similar but semantically distinct, as illustrated in (2), and intramotion alignment by refining semantically inaccurate motion clips using positive and negative proxy clips, as shown in (3)*



### 问题定义与基线损失

文本到动作生成模型通常以文本描述为输入，输出对应的动作序列。基线方法（如 **MDM**，Tevet et al., ICLR 2023）仅使用均方误差损失监督骨骼位置的回归：

$$ \mathcal { L } _ { m s e } = \| \pmb { m } _ { i } - \hat { \pmb { m } } _ { i } \| _ { 2 } ^ { 2 } \tag{1} $$

其中 $\pmb{m}_i$ 为真实动作序列，$\hat{\pmb{m}}_i$ 为生成动作序列。该损失缺乏显式语义监督，导致两个关键问题：**序列间语义错位**（不同文本生成过于相似的动作）和**序列内语义错位**（局部动作剪辑与文本语义不一致）。

### 核心模块一：序列间对齐（Inter-motion Alignment）

序列间对齐模块的目标是校正语义不同但生成动作过于相似的全局错位。其核心机制分为两步：

**步骤一：挖掘语义矛盾对。** 对于生成动作 $\hat{\pmb{m}}_i$，在批次内寻找其语义矛盾样本 $\hat{\pmb{m}}_i^h$——即生成距离与真实距离比值最小的其他动作：

$$ \hat { \pmb { m } } _ { i } ^ { h } = \hat { \pmb { m } } _ { j ^ { * } } , \mathrm { w h e r e \ } j ^ { * } = \operatorname * { a r g m i n } _ { j \neq i } \frac { \mathcal { D } ( \hat { \pmb { m } } _ { i } , \hat { \pmb { m } } _ { j } ) } { \mathcal { D } ( \pmb { m } _ { i } , \pmb { m } _ { j } ) } \tag{2} $$

该比值越小，说明生成空间中两个动作过于接近，而真实空间中它们本应相距较远——这正是语义矛盾的信号。

**步骤二：自适应边界三元组损失。** 利用挖掘到的矛盾对，构建自适应边界的序列级三元组损失：

$$ \mathcal { L } _ { i n t e r } = \operatorname* { m a x } \{ 0 , \mathcal { D } ( t _ { i } , \hat { m } _ { i } ) - \mathcal { D } ( t _ { i } , \hat { m } _ { i } ^ { h } ) + \phi _ { i n t e r } \} \tag{3} $$

其中自适应边界 $\phi_{inter} = \mathcal{D}(t_i, m_i^h) - \mathcal{D}(t_i, m_i)$ 由真实语义距离决定。其关键洞察是：**语义差异越大，边界越大，优化力度越强**——这使得模型能够根据语义矛盾的程度灵活调整校正强度，而非对所有样本施加统一的惩罚。

### 核心模块二：序列内对齐（Intra-motion Alignment）

序列内对齐模块处理局部动作剪辑的语义错位，在无需局部文本标注的情况下实现无监督语义细化。

**步骤一：识别最不对齐剪辑。** 在生成动作 $\hat{\pmb{m}}_i$ 中，找到与对应真实剪辑距离最大的局部剪辑：

$$ \hat { c } = \hat { { m } } _ { i } ^ { k ^ { * } } , \quad c = m _ { i } ^ { k ^ { * } } , \mathrm { w h e r e } \quad k ^ { * } = \arg \operatorname* { m a x } _ { k } \mathcal { D } ( \hat { m } _ { i } ^ { k } , m _ { i } ^ { k } ) \tag{4} $$

**步骤二：选择语义代理。** 从批次中为错位剪辑 $\hat{c}$ 选择正代理 $\hat{c}_{pos}$ 和负代理 $\hat{c}_{neg}$：

$$ \hat { c } _ { p o s } = \hat { c } _ { k ^ { * } } , \quad k ^ { * } = \arg \operatorname* { m a x } _ { k } \frac { \mathcal { D } ( \hat { c } , \hat { c } _ { k } ) } { \mathcal { D } ( c , c _ { k } ) } \tag{5} $$

$$ \hat { c } _ { n e g } = \hat { c } _ { k ^ { * } } , \quad k ^ { * } = \arg \operatorname* { m i n } _ { k } \frac { \mathcal { D } ( \hat { c } , \hat { c } _ { k } ) } { \mathcal { D } ( c , c _ { k } ) } \tag{6} $$

正代理是那些本应相似（真实距离小）但当前生成空间中相距较远的剪辑；负代理则是本应不相似但当前过于接近的剪辑。这种选择策略与序列间对齐的语义矛盾挖掘思路一脉相承。

**步骤三：自适应边界剪辑级三元组损失：**

$$ \mathcal { L } _ { i n t r a } = \operatorname* { m a x } \{ 0 , \mathcal { D } ( \hat { c } , \hat { c } _ { p o s } ) - \mathcal { D } ( \hat { c } , \hat { c } _ { n e g } ) + \phi _ { i n t r a } \} \tag{7} $$

其中 $\phi_{intra} = \mathcal{D}(c, c_{neg}) - \mathcal{D}(c, c_{pos})$。该损失仅在生成与真实动作的余弦相似度低于阈值 $\gamma$ 时激活，避免对已对齐良好的序列进行不必要的干预。

### 总损失函数

ATM 的最终训练目标将回归损失与两个对齐损失结合：

$$ \mathcal { L } _ { a l l } = \mathcal { L } _ { m s e } + \lambda \cdot ( \mathcal { L } _ { i n t e r } + \mathcal { L } _ { i n t r a } ) \tag{8} $$

其中 $\lambda$ 为平衡系数。整个框架在预训练的文本-动作对齐嵌入空间上运行，无需额外训练对齐编码器。

### 关键设计决策

自适应边界 $\phi_{inter}$ 和 $\phi_{intra}$ 是 ATM 区别于固定边界度量学习的核心创新。固定边界对所有样本对施加相同的约束强度，无法区分轻微语义偏差与严重语义矛盾。自适应边界直接从真实语义距离中推导优化强度，使模型能够学习结构化的语义边界。消融实验证实，自适应边界在所有指标上均优于固定边界（R-Precision Top-1 达 0.519，而固定边界最高仅 0.420）。

**局限性说明**：序列内对齐依赖生成与真实运动间的时间对齐假设，时间上的错位可能影响剪辑相似度计算的准确性。此外，基于 VQ-VAE 的离散运动表示因 token 不可微，无法直接应用本对齐损失——这是方法泛化性的一个已知约束。

### 补充图表

![[assets/figures/papers/paper_list_l3314_https_openaccess_thecvf_com_content_WACV2026_papers_Han_ATM_Enhanced_Ali/figures/001_Figure_1.jpg]]
*Figure 1: Semantic misalignment generated by MoMask [9]. Inter-motion misalignment highlights instances where semantically different text descriptions lead to overly similar motions, while intra-motion misalignment refers to the presence of inaccurate semantics. Green, red, and yellow words represent correct, incorrect, and undesired motion semantics, respectively*



## 实验与关键发现

### 主实验结果

ATM 在两个主流文本到动作生成基准 HumanML3D 和 KIT 上均取得了显著提升。Table 1 和 Table 2 分别展示了在 HumanML3D 和 KIT 上的完整评估结果，指标涵盖 R-Precision Top-1、FID、MultiModal Distance 和 Diversity 等。

![[assets/figures/papers/paper_list_l3314_https_openaccess_thecvf_com_content_WACV2026_papers_Han_ATM_Enhanced_Ali/figures/003_Table_1.jpg]]
*Table 1: Results on HumanML3D [8]. “↑”, “↓” and “→” indicate that higher or lower values, or values closer to real motion are better, respectively. “+ATM” indicates incorporating ATM with corresponding models. The baseline is trained only with*

![[assets/figures/papers/paper_list_l3314_https_openaccess_thecvf_com_content_WACV2026_papers_Han_ATM_Enhanced_Ali/figures/004_Table_2.jpg]]
*Table 2: Results on the KIT [32] dataset, using the same notations as in Table 1*

在 HumanML3D 上，将 ATM 集成到基线 MDM（Tevet et al., ICLR 2023）后，R-Precision Top-1 从 0.425 提升至 0.519（+0.094），FID 从 0.570 降至 0.320（-0.250）。更值得关注的是，当 ATM 与当前 SOTA 方法 MoMask（Guo et al., CVPR 2024）结合时，FID 进一步降至 0.043，R-Precision Top-1 达到 0.528，在所有指标上均优于单独使用 MoMask 或 BAMM（Pinyoanuntapong et al., ECCV 2024）等强基线。KIT 数据集上趋势一致：ATM 将基线 R-Precision Top-1 从 0.392 提升至 0.434，FID 从 0.566 降至 0.354。

这些结果表明，ATM 的对齐损失对不同类型的生成器（扩散模型 MDM、掩码模型 MoMask）均具有即插即用的兼容性，且语义对齐的改善直接转化为生成质量与文本匹配度的双重提升。

### 消融实验

**损失组件消融。** Table 3 系统拆解了各损失项的贡献。仅使用 $L_{mse}$ 的基线在 HumanML3D 上 R-Precision Top-1 为 0.425，FID 为 0.570。单独添加 $L_{inter}$ 将 Top-1 提升至 0.502，FID 降至 0.383；单独添加 $L_{intra}$ 则将 Top-1 提升至 0.480，FID 降至 0.391。两者联合使用时达到最优：Top-1 0.519，FID 0.320。这验证了序列级（inter-motion）和剪辑级（intra-motion）语义对齐具有互补性，前者负责纠正跨序列的全局语义混淆，后者细化局部动作的语义准确性。

**自适应边界 vs. 固定边界。** Table 4 对比了自适应 margin $\phi_{ter}$ 与多个固定 margin 值的效果。固定 margin 在 0.1 到 0.5 范围内，R-Precision Top-1 最高仅达 0.420，而自适应 margin 达到 0.519。这一差距揭示了核心机制：固定 margin 对所有样本施加统一的优化强度，无法区分语义差异程度；自适应 margin 根据真实语义距离 $\mathcal{D}(t_i, m_i^h) - \mathcal{D}(t_i, m_i)$ 动态调整，对语义矛盾更严重的样本施加更强的校正信号，从而学习到更结构化的语义边界。

**$L_{inter}$ 与其他度量损失对比。** Table 5 将所提 $L_{inter}$ 与对比学习损失、三元组损失等常见度量学习目标进行了对比。$L_{inter}$ 在 R-Precision Top-1 上达到 0.502，显著优于对比学习（0.473）和标准三元组损失（0.420）。这得益于 $L_{inter}$ 的两个设计优势：一是通过最小化 $\frac{\mathcal{D}(\hat{m}_i, \hat{m}_j)}{\mathcal{D}(m_i, m_j)}$ 比值来挖掘语义矛盾样本，而非随机采样负样本；二是自适应边界使优化目标与实例特定的语义差距对齐。

### 失败模式与局限性

尽管 ATM 在连续运动表示上表现优异，但作者明确指出两个关键局限：

1. **离散表示的不可微性。** 基于 VQ-VAE 的 T2M 模型（如 MoMask 的离散 token 表示）因量化操作不可微，无法直接应用 $L_{inter}$ 和 $L_{intra}$。Table 1 中 MoMask+ATM 的结果是通过在连续潜空间施加对齐损失实现的，而非直接优化离散 token。这限制了 ATM 在离散运动生成范式中的直接部署。

2. **时间对齐假设。** Intra-motion alignment 依赖生成运动与真实运动在时间维度上对齐的假设，以准确计算剪辑间的语义相似度。当生成运动存在时间偏移或节奏差异时，剪辑匹配的准确性会下降，可能导致 $L_{intra}$ 的优化信号噪声增大。该问题在 KIT 数据集上的提升幅度（R-Precision Top-1 +0.042）小于 HumanML3D（+0.094）也侧面反映了时间对齐假设对数据特性的敏感性。

### 用户研究

Figure 4 展示了用户研究的设计与结果。研究从动作对齐度（Action Alignment Score）、序列对齐度（Sequence Alignment Score）和真实感质量（Realistic Quality）三个维度评估生成结果。ATM 在所有三个维度上均优于对比方法，尤其在动作对齐度上优势明显——该指标衡量生成动作中具体行为与文本描述的一致性，直接对应 intra-motion alignment 的设计目标。这一主观评价与 R-Precision、FID 等客观指标的趋势一致，增强了结论的可信度。

![[assets/figures/papers/paper_list_l3314_https_openaccess_thecvf_com_content_WACV2026_papers_Han_ATM_Enhanced_Ali/figures/008_Figure_4.jpg]]
*Figure 4: User study. In (1), A, B, C, D denote motion videos generated by different methods. In (2), the action alignment score is calculated as the ratio of users’ responses to Q2 relative to Q1. The sequence alignment score and realistic quality are derived from the statistical analysis of users’ answers to Q3 and Q4, respectively*

### 定性分析

Figure 3 展示了 SOTA 方法的生成示例对比。MoMask 生成的序列在“walk forward then sit down”等复合指令下出现语义遗漏（仅完成行走，未执行坐下），而 ATM 纠正了此类局部语义错位。Figure 5 进一步可视化了不同损失组件的贡献：仅使用 $L_{mse}$ 的基线生成的动作语义模糊，添加 $L_{inter}$ 后跨序列语义区分度提升，再叠加 $L_{intra}$ 后局部动作细节更准确。这与 Table 3 的量化消融结论一致。

![[assets/figures/papers/paper_list_l3314_https_openaccess_thecvf_com_content_WACV2026_papers_Han_ATM_Enhanced_Ali/figures/006_Table_3.jpg]]
*Table 3: Ablation study of loss functions on HumanML3D*

![[assets/figures/papers/paper_list_l3314_https_openaccess_thecvf_com_content_WACV2026_papers_Han_ATM_Enhanced_Ali/figures/007_Figure_3.jpg]]
*Figure 3: Examples generated by SOTA methods. In (1), the unchanged color indicates remaining in the same position, while in (2), the darkening color highlights position change. Green, red, and yellow words denote correct, incorrect, and undesired semantics, respectively*

![[assets/figures/papers/paper_list_l3314_https_openaccess_thecvf_com_content_WACV2026_papers_Han_ATM_Enhanced_Ali/figures/010_Figure_5.jpg]]
*Figure 5: Motion sequences generated by different components of our method. Darker colors indicate motion progression*

### 补充图表

![[assets/figures/papers/paper_list_l3314_https_openaccess_thecvf_com_content_WACV2026_papers_Han_ATM_Enhanced_Ali/figures/009_Table_4.jpg]]
*Table 4: Comparison between the adaptive margin and predefined margin values on HumanML3D*

![[assets/figures/papers/paper_list_l3314_https_openaccess_thecvf_com_content_WACV2026_papers_Han_ATM_Enhanced_Ali/figures/011_Table_5.jpg]]
*Table 5: Comparison between*



## 定位与知识库关联

### 1. 与基线方法的关系

ATM 并非一个独立的生成模型，而是一种**即插即用的语义对齐增强模块**，可叠加于现有扩散式文本到动作（T2M）生成器之上。论文以 **MDM**（Tevet et al., ICLR 2023）为主要基线，验证了 ATM 的有效性。MDM 仅使用 MSE 回归损失 $\mathcal{L}_{mse}$ 监督骨骼位置精度，缺乏显式的语义对齐机制，导致生成的动作序列在全局（inter-motion）和局部（intra-motion）层面出现严重的语义错位——语义不同的文本描述产生过于相似的动作，或动作内部包含与文本不符的片段。

ATM 的核心改动在于**损失函数**和**语义对齐策略**两个槽位：

| 改动槽位 | 基线值（MDM） | ATM 方案 |
|---------|-------------|---------|
| 损失函数 | 仅 $\mathcal{L}_{mse}$ | $\mathcal{L}_{mse}$ + 自适应 $\mathcal{L}_{inter}$ + 自适应 $\mathcal{L}_{intra}$ |
| 语义对齐策略 | 无显式语义对齐 | 基于语义矛盾挖掘的自适应三元组损失，分别在序列级和剪辑级施加 |

ATM 还将该对齐模块应用于 **MoMask**（Guo et al., CVPR 2024）和 **BAMM**（Pinyoanuntapong et al., ECCV 2024）等 SOTA 方法，在 HumanML3D 和 KIT 数据集上均取得一致提升，表明其具有较强的**模型无关性**。

### 2. 与度量学习范式的差异

ATM 的 $\mathcal{L}_{inter}$ 和 $\mathcal{L}_{intra}$ 形式上属于三元组损失族，但与标准对比学习和固定边界三元组损失存在本质区别：

- **负样本挖掘策略不同**：标准对比学习通常以同一批次中其他样本为负例，或基于随机采样。ATM 的 $\mathcal{L}_{inter}$ 通过最小化生成距离与真实距离的比值 $\frac{\mathcal{D}(\hat{\pmb{m}}_i, \hat{\pmb{m}}_j)}{\mathcal{D}(\pmb{m}_i, \pmb{m}_j)}$ 来挖掘最可能产生语义矛盾的序列对，这是一种**语义感知的硬负样本挖掘**，而非随机或均匀采样。
- **边界机制不同**：标准三元组损失使用固定 margin。ATM 引入**自适应边界** $\phi_{ter} = \mathcal{D}(t_i, m_i^h) - \mathcal{D}(t_i, m_i)$ 和 $\phi_{tra} = \mathcal{D}(c, c_{neg}) - \mathcal{D}(c, c_{pos})$，边界值由真实语义距离动态决定。消融实验（Table 4）证实，自适应 margin 在所有指标上均显著优于固定 margin（R-Precision Top-1 0.519 vs. 最高 0.420）。
- **监督粒度不同**：$\mathcal{L}_{intra}$ 在剪辑级别进行语义细化，通过正代理剪辑 $\hat{c}_{pos}$ 和负代理剪辑 $\hat{c}_{neg}$ 的挖掘，实现了**无需局部文本标注的无监督局部语义对齐**。这一设计在现有 T2M 方法中尚无直接对应。

### 3. 适用边界与局限性

**适用前提**：
- ATM 依赖预训练的文本-动作对齐嵌入空间来计算语义距离 $\mathcal{D}(\cdot, \cdot)$。该空间的质量直接影响负样本挖掘和自适应边界的可靠性。
- $\mathcal{L}_{intra}$ 假设生成动作与真实动作之间存在时间对齐关系，即对应时间步的剪辑应具有语义可比性。

**已知局限**（论文明确指出的 failure modes）：
1. **离散动作表示不兼容**：基于 VQ-VAE 的 T2M 模型（如 MoMask 的原始版本）因离散 token 的不可微性，无法直接应用 ATM 的对齐损失。论文中 MoMask+ATM 的结果是通过对连续潜变量施加损失实现的，但这一路径在纯离散框架下不可行。
2. **时间错位敏感**：Intra-motion alignment 依赖剪辑级的时间对齐假设。当生成动作与真实动作在时间维度上存在偏移（如动作节奏不同）时，剪辑相似度计算可能不准确，影响正/负代理选择的可靠性。

### 4. 开放问题

基于上述局限，论文留出了两个明确的后续研究方向：

- **离散表示的兼容性**：如何通过重参数化、Gumbel-Softmax 松弛或替代梯度估计等策略，使语义对齐损失兼容于 VQ-VAE 类离散运动表示模型，是一个待解决的技术问题。
- **时间对齐鲁棒性**：如何设计机制（如动态时间规整 DTW 的连续松弛、可学习的时序对齐模块）来确保运动剪辑间的时间对齐，以进一步提高 intra-motion alignment 在时序偏移场景下的鲁棒性。

此外，从方法谱系角度看，ATM 的自适应边界机制与度量学习中的**距离加权采样**和**软边界三元组损失**存在概念关联，但其在 T2M 任务中的具体形式（基于预训练对齐空间的语义距离比值）具有领域特异性。该方向是否可推广至其他跨模态生成任务（如文本到视频、文本到语音），需要进一步验证。



## 原文 PDF

![[paperPDFs/WACV_2026/ATM:_Enhanced_Alignment_for_Text-to-Motion_Generation.pdf]]
