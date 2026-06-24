---
title: "VLM-PTQ: Efficient Post-Training Quantization for Large Vision-Language Models"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/VLM_PTQ_Efficient_Post_Training_Quantization_for_Large_Vision_Language_Models.pdf
project_link: null
code_link: null
aliases:
- VP
- VLM-PTQ
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 输出残差r与逆Hessian列共同决定了对原始权重的校正偏移量δ；视觉和语言Hessian对角线的模态融合系数μ通过最小化重构误差调节通道重要性。
primary_logic: 通过推导闭式校正项，将量化目标显式地从原始权重移向同时考虑输出残差与逆Hessian的连续最优解；引入模态感知的通道重要性权重，使量化器能区分视觉和语言标记，从而在不对称校准下实现更好的局部最优。
claims:
- Round-to-nearest (RTN) 量化在不对称校准目标下不是最优策略，理论最优值是 w_q + δ
- 闭式校正项 C 可以使离散最优解对准加权后的权重，从而最小化每通道损失 L_q
- 模态感知重要性向量 M^μ 通过融合视觉和语言 Hessian 对角线并在校准集上搜索最优融合系数 μ，显著提升量化性能
- 在 3‑bit / 2‑bit 以及 W2A8KV8 设置下，VLM‑PTQ 在所有测试的 VLM（1B–72B）上均优于基线 GPTQ 和 GPTAQ
---

# VLM-PTQ: Efficient Post-Training Quantization for Large Vision-Language Models

> [!tip] 核心洞察
> 通过推导闭式校正项，将量化目标显式地从原始权重移向同时考虑输出残差与逆Hessian的连续最优解；引入模态感知的通道重要性权重，使量化器能区分视觉和语言标记，从而在不对称校准下实现更好的局部最优。

| 字段 | 内容 |
|------|------|
| 中文题名 | VLM-PTQ：面向大型视觉语言模型的高效训练后量化 |
| 英文题名 | VLM-PTQ: Efficient Post-Training Quantization for Large Vision-Language Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Deng_VLM-PTQ_Efficient_Post-Training_Quantization_for_Large_Vision-Language_Models_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | VLM-PTQ |
| Dataset | Eight VLM Benchmark Avg |

> [!tip] 效果简介
> - Eight VLM Benchmark Avg 上，Average Accuracy (%) 71.3 vs 65.0 (GPTQ) (+6.3)；Average Accuracy (%) 48.4 vs 43.1 (GPTQ) (+5.3)；Average Accuracy (%) 44.6 vs ≈39.0 (GPTQ estimate) (≈+5.6)。

## 概述

大型视觉语言模型（VLM）在图文理解与推理任务上展现出强大的能力，但其庞大的参数量——从 1B 到 72B 不等——使得部署成本极高。训练后量化（PTQ）是降低推理开销的主流手段，然而直接将面向纯语言模型设计的 PTQ 方法迁移到 VLM 上时，性能退化远超预期。

**核心瓶颈** 来自两个被忽视的因素。第一，当前主流的权重补偿方法（如 **GPTQ**（Frantar et al., arXiv 2022）和 **GPTAQ**（Li et al., arXiv 2025））在量化目标的选择上仍沿用 Round-to-Nearest（RTN）策略，但该策略在不对称校准目标下并非最优——输出残差与逆 Hessian 列共同决定了理论最优的量化点位置，而 RTN 会系统性地偏离该位置。第二，VLM 的输入通道同时承载视觉和语言两种模态的 token，其信息密度差异显著；标准量化器使用统一的 Hessian 对角线作为通道重要性分数，导致量化参数被统计占优的模态所主导，损害另一模态的精度。

**方法与定位**：VLM-PTQ 从上述两个瓶颈出发，在不增加推理开销的前提下对 PTQ 流程进行两处关键改造：

1. **闭式校正项**：推导出一个预计算的每通道校正系数 $C_q$，将量化目标从原始权重 $w_q$ 显式偏移至 $w_q + \delta$（其中 $\delta = r X^\top H_{:,q}^{-1}$），使得离散取整操作对准加权后的连续最优解，从而在不对称校准下获得更低的通道级量化损失 $L_q$。
2. **模态感知重要性向量**：在校准阶段，根据视觉掩码分别计算视觉 Hessian $H_v$ 和语言 Hessian $H_l$，并通过可调融合系数 $\mu$ 构造通道重要性 $M^\mu = \mu \cdot H_v^{\mathrm{diag}} + (1-\mu) \cdot H_l^{\mathrm{diag}}$。随后在校准集上以最小化输出重构误差为目标，通过轻量网格搜索确定每层最优的 $\mu^*$，使量化器能自适应地平衡两种模态。

该方法在方法谱系上属于 **权重补偿 + 通道重要性加权** 的 PTQ 范式，其独特之处在于将补偿过程从“先量化再补偿”扩展为“先校正目标再量化”，并将通道重要性从单模态 Hessian 推广为模态感知的融合形式。

**主要结果**：在 Qwen2.5-VL-7B 的 W3A16 设置下，VLM-PTQ 在 8 个 VLM 基准上的平均准确率达到 71.3%，较 GPTQ 的 65.0% 提升 **+6.3 个百分点**；在更极端的 W2A16 设置下，平均准确率为 48.4%，较 GPTQ 的 43.1% 提升 **+5.3 个百分点**。在 W2A8KV8 的极限压缩场景下，VLM-PTQ 同样在所有测试模型（1B–72B）上一致优于基线。消融实验表明，闭式校正项 $C$ 独立贡献约 +1.2 个百分点，模态感知重要性 $M$ 独立贡献约 +5.4 个百分点，二者联合使用达到最优。方法在校准时间上仅比 GPTAQ 增加约 10%（921s → 1020s），保持实用友好。

## 背景与动机

### 大型视觉语言模型的部署瓶颈

大型视觉语言模型（VLM）将视觉编码器与大型语言模型（LLM）深度融合，在图文理解、文档分析、多模态推理等任务上展现出卓越能力。然而，这类模型通常包含数十亿参数，推理时需要同时处理视觉和语言两种模态的高维特征，导致显存占用和计算开销远超纯文本LLM。以 Qwen2.5-VL-7B 为例，FP16 精度下仅 LLM 部分即需约 14 GB 显存，严重制约了 VLM 在资源受限设备上的部署。

训练后量化（Post-Training Quantization, PTQ）作为一种无需重训练的高效压缩手段，已在纯文本 LLM 上取得显著进展。其核心思想是用少量校准数据，通过逐层重构误差最小化，将浮点权重映射到低位宽定点表示。然而，将现有 PTQ 方法直接迁移至 VLM 面临两个根本性挑战。

### 不对称校准目标下的量化次优性

标准权重补偿方法（如 **GPTQ**，Frantar et al., arXiv 2022）采用逐列量化的贪心策略：每量化一列权重后，将产生的输出误差通过 Hessian 逆矩阵传播至剩余未量化列进行补偿。这一框架隐含假设量化目标是对称的——即 Round-to-Nearest（RTN）策略能够使补偿后的权重落在离散最优解附近。

然而，VLM 的校准过程引入了不对称性。**GPTAQ**（Li et al., arXiv 2025）指出，当层间存在残差传播时，量化某一列造成的输出残差 $r$ 会与输入激活 $X$ 和逆 Hessian 列 $H_{:,q}^{-1}$ 共同作用，使得连续域上的最优权重偏离原始权重 $w_q$。具体而言，连续最优解为：

$$\hat{\mathbf{w}}_q^* = \mathbf{w}_q + \mathbf{r} \mathbf{X}^{\top} \mathbf{H}_{:,q}^{-1}$$

但 GPTAQ 虽然在补偿阶段传播了残差，量化阶段仍对原始权重 $w_q$ 执行 RTN，而非对校正后的 $w_q + \delta$ 取整。这一“补偿-量化”分离策略导致量化点偏离理论最优位置，在低位宽下尤为致命。

### 模态信息密度差异与通道重要性失衡

VLM 的第二个独特挑战在于视觉和语言模态的信息密度存在显著差异。如图 3 所示，视觉 token 和语言 token 在 LLM 各层的 Hessian 对角线幅度可相差数个数量级。由于标准量化器使用统一的 Hessian 对角线作为通道重要性分数，统计上占优的模态会主导量化参数的确定，使量化器“偏向”该模态而忽视另一模态的关键通道。

Figure 3 的可视化揭示了这一失衡：在多数层中，语言 Hessian 的幅度远大于视觉 Hessian，导致标准量化器在优化重构误差时过度关注语言 token 的保真度，牺牲了视觉特征的量化精度。这种模态间的隐性竞争是纯文本 LLM 量化中不存在的结构性问题。

### 本文动机与核心思路

针对上述两个缺口，本文提出 **VLM-PTQ**，核心思路包含两个互补的技术组件：

1. **闭式校正项**：从不对称校准目标出发，推导出每通道的校正系数 $C_q$，将量化目标显式地从 $w_q$ 移向 $w_q + \delta$。该校正项同时编码了输出残差和逆 Hessian 列的信息，使得离散量化点能够对准连续最优解，从而在每通道上最小化量化损失 $L_q$（见 Figure 2）。

2. **模态感知重要性向量**：将 Hessian 分解为视觉 Hessian $H_v$ 和语言 Hessian $H_l$，引入可调融合系数 $\mu$，生成模态感知的通道重要性向量：

$$\mathbf{M}^{\mu} = \mu \cdot \mathbf{H}_v^{\mathrm{diag}} + (1 - \mu) \cdot \mathbf{H}_l^{\mathrm{diag}}$$

通过在校准集上最小化输出重构误差搜索最优 $\mu^*$，使量化器能够根据不同层的模态敏感度自适应地平衡视觉和语言通道的重要性（见 Figure 4）。

这两个组件均集成于 GPTQ 的逐列量化框架中，无需额外训练，仅在校准阶段增加少量搜索开销，即可在 3-bit / 2-bit 权重量化及 W2A8KV8 极端设置下实现一致的性能提升。

## 核心创新

VLM‑PTQ 针对现有权重补偿量化方法（GPTQ / GPTAQ）在视觉语言模型上的两个结构性缺陷，提出了两项互补的关键改进：**非对称量化校正**与**模态感知重要性加权**。这两项改进分别从“量化目标选择”和“通道重要性加权”两个维度，将标准量化管线重构为更适合 VLM 多模态特性的形式。

### 1. 非对称量化校正：从 RTN 到校正后的最优量化点

**问题根源。** 标准权重补偿方法（如 GPTQ）采用 Round‑to‑Nearest（RTN）策略，直接对原始权重 $\mathbf{w}_q$ 取整。然而，当引入输出残差传播（如 GPTAQ）后，量化目标变为非对称校准目标，RTN 不再是理论最优策略。此时，使每通道量化损失 $L_q$ 最小化的连续最优解是：

$$\hat{\mathbf{w}}_q^* = \mathbf{w}_q + \mathbf{r} \mathbf{X}^{\top} \mathbf{H}_{:,q}^{-1} \quad \text{(Eq. 14)}$$

即，最优权重点应从原始权重 $\mathbf{w}_q$ 偏移一个由输出残差 $\mathbf{r}$ 和逆 Hessian 列共同决定的量。

**核心机制。** VLM‑PTQ 推导了一个**闭式校正项** $\mathbf{C}$，将上述偏移显式地集成到量化步骤中。校正后的量化点为：

$$\hat{\mathbf{W}}_{:, q} = \operatorname{RTN}\left(\mathbf{W}_{:, q} \cdot (1 + \mathbf{C}_{q})\right) \quad \text{(Eq. 19)}$$

其中校正系数 $\mathbf{C}_q$ 通过预计算获得：

$$\mathbf{C} = \mathrm{diag}(\Delta\mathbf{X}\mathbf{X}^{\top}\mathbf{H}^{-T}) \odot \mathrm{diag}(\mathbf{H}^{-T}) \quad \text{(Eq. 18)}$$

这一设计的本质在于：**将离散量化操作从原始权重空间“搬移”到由残差和逆 Hessian 共同确定的连续最优解附近**，从而在不改变量化器本身的前提下，获得比 RTN 更优的局部最优。Figure 2 展示了校正项 $\mathbf{C}_q$ 与通道级量化损失 $L_q$ 的关系，验证了该偏移对损失降低的直接贡献。

### 2. 模态感知重要性加权：解耦视觉与语言通道

**问题根源。** 在 VLM 中，视觉标记和语言标记的信息密度存在显著差异（Figure 3 展示了视觉与语言 Hessian 在幅度上的显著差异）。然而，传统量化器使用统一的 Hessian 对角线作为所有输入通道的重要性分数，导致量化参数被统计占优的模态所主导，忽视了另一模态的关键通道。

**核心机制。** VLM‑PTQ 提出**模态感知重要性向量** $\mathbf{M}^{\mu}$，通过可调系数 $\mu$ 融合视觉和语言的 Hessian 对角线：

$$\mathbf{M}^{\mu} = \mu \cdot \mathbf{H}_v^{\mathrm{diag}} + (1 - \mu) \cdot \mathbf{H}_l^{\mathrm{diag}} \quad \text{(Eq. 22)}$$

其中 $\mathbf{H}_v$ 和 $\mathbf{H}_l$ 分别由视觉和语言标记的激活矩阵计算得到（Eq. 20），利用视觉掩码 $\mathbf{v}$ 实现解耦。最优融合系数 $\boldsymbol{\mu}^*$ 通过在校准集上最小化输出重构误差搜索得到：

$$\boldsymbol{\mu}^* = \arg\min_{\boldsymbol{\mu}} \| \mathbf{W} \tilde{\mathbf{X}} - \hat{\mathbf{W}}^{\mu} \mathbf{X} \|_2^2 \quad \text{(Eq. 25)}$$

这一设计使量化器能够**区分视觉和语言标记对每通道的重要性贡献**，避免单一模态主导量化参数的选择。Figure 4 进一步表明，不同层对两种模态的敏感度差异显著，逐层搜索 $\mu$ 是必要的。

### 3. 两项创新的协同效应

消融实验（Table 3）揭示了校正项 $\mathbf{C}$ 与模态感知重要性 $\mathbf{M}$ 的协同关系：在 W3A16 设置下，单独添加 $\mathbf{C}$ 使 Qwen2.5‑VL‑7B 在 8 个 VLM 基准上的平均准确率从 65.0% 提升至 66.2%（+1.2 pp）；单独添加 $\mathbf{M}$ 则大幅提升至 70.4%（+5.4 pp）；二者结合（完整 VLM‑PTQ）达到 71.3%（+6.3 pp）。这表明：**校正项提供了更优的局部优化起点，而模态感知重要性则从根本上解决了多模态场景下的通道优先级错配**，两者在因果链条上互补而非冗余。

### 4. 方法谱系与知识库定位

VLM‑PTQ 位于训练后权重量化（PTQ）的方法谱系中，直接对标两类基线：

- **GPTQ**（Frantar et al., arXiv 2022）：对称权重补偿的经典方法，使用 RTN 和 Hessian 驱动的逐列更新，但未考虑输出残差传播和模态差异。
- **GPTAQ**（Li et al., arXiv 2025）：在 GPTQ 基础上引入非对称校准，传播输出残差进行权重补偿，但仍采用 RTN 量化，未解决量化目标偏移问题。

VLM‑PTQ 的核心贡献在于：**在 GPTAQ 的非对称校准框架下，识别并修正了 RTN 策略的次优性，同时引入模态感知机制填补了多模态 PTQ 的空白**。该方法仅量化语言模型部分（视觉编码器与适配器保持全精度），与上述基线保持一致的实验设置，确保公平比较。

## 整体框架

VLM‑PTQ 的整体流程围绕两个核心模块构建：**非对称量化校正**与**模态感知量化**。这两个模块嵌入到标准的逐列权重量化框架中，在不改变视觉编码器和适配器（保持全精度）的前提下，仅对语言模型（LLM）部分的线性层权重进行低位宽压缩。

### 输入与预处理

给定一个图文对，视觉编码器 $\mathcal{V}$ 从输入图像 $\mathbf{I}$ 中提取视觉特征 $\mathbf{Z}_v \in \mathbb{R}^{n_v \times d_v}$，随后适配器 $\mathcal{A}$ 将其投影至与语言模型相同的维度 $d$，得到 $\mathbf{H}_v \in \mathbb{R}^{n_v \times d}$；文本标记通过分词器 $\mathcal{T}$ 映射为 $\mathbf{H}_t \in \mathbb{R}^{n_t \times d}$。两类嵌入按照视觉掩码 $\mathbf{v} \in \{0,1\}^{n_v+n_t}$ 进行交错拼接，形成该层的输入激活矩阵 $\mathbf{X} \in \mathbb{R}^{(n_v+n_t) \times d}$。校准集从 ShareGPT4V 改进的 COCO Caption 数据集中随机抽取 128 个图文对，所有对比方法共享同一校准集以保证公平性。

### 逐列量化主循环

量化过程沿权重矩阵 $\mathbf{W}$ 的列维度逐列进行，每列 $q$ 的处理包含以下步骤：

1. **残差传播与校正向量计算**  
   从上一列累积的输出残差 $\mathbf{r}$ 出发，结合当前列对应的逆 Hessian 列 $\mathbf{H}_{:,q}^{-1}$，计算连续最优权重：
   $$\hat{\mathbf{w}}_q^* = \mathbf{w}_q + \mathbf{r} \mathbf{X}^{\top} \mathbf{H}_{:,q}^{-1}$$
   进一步预计算每通道的闭式校正系数：
   $$\mathbf{C} = \mathrm{diag}(\Delta\mathbf{X}\mathbf{X}^{\top}\mathbf{H}^{-T}) \odot \mathrm{diag}(\mathbf{H}^{-T})$$
   该校正项显式地将量化目标从原始权重 $\mathbf{w}_q$ 偏移至同时考虑输出残差与逆 Hessian 的最优位置，解决了标准 RTN 在非对称校准目标下的次优性问题。

2. **模态感知重要性融合**  
   利用视觉掩码 $\mathbf{v}$ 分别计算视觉 Hessian $\mathbf{H}_v = \mathbf{X}_{:,v} \mathbf{X}_{:,v}^\top$ 和语言 Hessian $\mathbf{H}_l = \mathbf{X}_{:,\neg v} \mathbf{X}_{:,\neg v}^\top$，提取其对角线并融合为模态感知重要性向量：
   $$\mathbf{M}^{\mu} = \mu \cdot \mathbf{H}_v^{\mathrm{diag}} + (1 - \mu) \cdot \mathbf{H}_l^{\mathrm{diag}}$$
   其中融合系数 $\mu$ 通过在校准集上最小化输出重构误差进行逐层网格搜索确定：
   $$\boldsymbol{\mu}^* = \arg\min_{\boldsymbol{\mu}} \| \mathbf{W} \tilde{\mathbf{X}} - \hat{\mathbf{W}}^{\mu} \mathbf{X} \|_2^2$$
   这一机制使量化器能够区分视觉和语言标记的信息密度差异，避免被统计占优的模态主导量化参数选择。

3. **量化执行与权重更新**  
   将校正项 $\mathbf{C}$ 和模态感知重要性 $\mathbf{M}$ 同时作用于当前列，执行量化：
   $$\hat{\mathbf{W}}_{:, q} = \operatorname{RTN}\big(\mathbf{W}_{:, q} \cdot (1 + \mathbf{C}_{q}); \mathbf{S}^{*}, \mathbf{Z}^{*}\big)$$
   其中 $\mathbf{S}^{*}$ 和 $\mathbf{Z}^{*}$ 是基于 $\mathbf{M}^{\mu}$ 计算的缩放因子和零点。量化完成后，根据量化误差更新输出残差 $\mathbf{r}$，并传播至下一列。

### 模块关系与数据流

两个核心模块在功能上互补：**校正项 C** 提供通道级的离散最优解偏移，解决了非对称校准下的理论次优性问题；**模态感知重要性 M** 提供跨模态的通道重要性区分，解决了视觉和语言信息密度不均衡的问题。消融实验（Table 3）验证了这一互补性：单独添加 C 使 8 基准平均准确率从 65.0% 提升至 66.2%，单独添加 M 使其达到 70.4%，二者联合使用（完整 VLM‑PTQ）则进一步提升至 71.3%。

### 计算开销

相比基线 GPTQ/GPTAQ，VLM‑PTQ 额外引入了两项计算：模态感知 Hessian 分解和逐层 $\mu$ 的网格搜索。前者仅需在校准阶段执行一次，后者使校准时间增加约 10%、内存开销增加约 30%。推理阶段不引入任何额外延迟，因为量化后的权重矩阵与标准量化模型完全一致。

## 核心模块与公式推导

VLM-PTQ 的核心由两个互补模块构成：**非对称量化校正**与**模态感知量化**。前者解决权重补偿方法中 RTN 策略在非对称目标下的次优性问题，后者解决视觉与语言模态间信息密度差异导致的通道重要性偏差。

---

### 模块一：非对称量化校正

#### 问题建模

给定一层权重矩阵 $\mathbf{W} \in \mathbb{R}^{d_{\text{out}} \times d_{\text{in}}}$ 和输入激活 $\mathbf{X}$，GPTAQ 通过拉格朗日乘子法求解约束优化问题，得到权重补偿更新：

$$\Delta\mathbf{w} = \frac{(\hat{\mathbf{w}}_q - \mathbf{w}_q)}{\mathbf{H}_{qq}^{-1}} \cdot (\mathbf{H}_{q,:}^{-1}) + \mathbf{r}\mathbf{X}^{\top}\mathbf{H}^{-1}$$

其中 $\mathbf{r}$ 为输出残差，$\mathbf{H} = \mathbf{X}\mathbf{X}^{\top}$ 为 Hessian 矩阵。该补偿量在更新剩余权重时传播了残差信息，但量化目标 $\hat{\mathbf{w}}_q$ 仍通过 RTN 直接作用于原始权重 $\mathbf{w}_q$。

#### 核心洞察

论文指出，在非对称校准目标下，连续最优解并非原始权重，而是：

$$\hat{\mathbf{w}}_q^* = \mathbf{w}_q + \mathbf{r}\mathbf{X}^{\top}\mathbf{H}_{:,q}^{-1} \quad \text{(Eq. 14)}$$

这意味着量化点应沿 $\mathbf{r}\mathbf{X}^{\top}\mathbf{H}_{:,q}^{-1}$ 方向偏移。直接对 $\mathbf{w}_q$ 使用 RTN 会系统性地偏离该最优位置。

#### 闭式校正项

为将偏移量集成到量化步骤中，定义校正系数向量 $\mathbf{C}$：

$$\mathbf{C} = \mathrm{diag}(\Delta\mathbf{X}\mathbf{X}^{\top}\mathbf{H}^{-T}) \odot \mathrm{diag}(\mathbf{H}^{-T}) \quad \text{(Eq. 18)}$$

其中 $\Delta\mathbf{X}$ 为量化引入的输入扰动。校正后的量化点变为：

$$\hat{\mathbf{W}}_{:,q} = \operatorname{RTN}\big(\mathbf{W}_{:,q} \cdot (1 + \mathbf{C}_{q})\big) \quad \text{(Eq. 19)}$$

**变量含义**：
- $\mathbf{C}_q$：第 $q$ 个输入通道的校正系数，联合编码了输出残差与逆 Hessian 列的影响
- $\mathbf{H}_{:,q}^{-1}$：逆 Hessian 的第 $q$ 列，反映该通道与其他通道的相关性结构
- $\mathbf{r}$：当前层量化前的累积输出残差

Figure 2 展示了在 W3A16 Qwen2.5-VL-7B 的最后一个下投影层中，通道级量化损失 $L_q$ 与校正项 $\mathbf{C}_q$ 的关系——校正项有效降低了高损失通道的量化误差。

![[assets/figures/papers/paper_list_l809_https_openaccess_thecvf_com_content_CVPR2026_html_Deng_VLM_PTQ_Efficient/figures/002_Figure_2.jpg]]
*Figure 2: Channel-wise quantization loss*

---

### 模块二：模态感知量化

#### 动机

标准量化器使用统一的 Hessian 对角线 $\mathrm{diag}(\mathbf{H})$ 作为通道重要性权重。但在 VLM 中，输入 $\mathbf{X}$ 由视觉和语言 token 交织而成：

$$\mathbf{X} = \mathrm{Interleave}(\mathbf{H}_v, \mathbf{H}_t, \mathbf{v}) \in \mathbb{R}^{(n_v+n_t) \times d}$$

其中 $\mathbf{v} \in \{0,1\}^{n_v+n_t}$ 为视觉掩码。Figure 3 揭示，视觉和语言 Hessian 在不同层的幅度存在显著差异，标准量化器会被统计占优的模态主导，忽视另一模态的关键通道。

![[assets/figures/papers/paper_list_l809_https_openaccess_thecvf_com_content_CVPR2026_html_Deng_VLM_PTQ_Efficient/figures/003_Figure_3.jpg]]
*Figure 3: Magnitude disparity between vision and language Hessians across layers in the original 7B VLM, where the standard quantizer is biased toward the modality with the larger Hessian*

#### 模态解耦与融合

利用视觉掩码 $\mathbf{v}$ 分别计算两个模态的 Hessian：

$$\mathbf{H}_v = \mathbf{X}_{:,\mathbf{v}}\mathbf{X}_{:,\mathbf{v}}^{\top}, \quad \mathbf{H}_l = \mathbf{X}_{:,\neg\mathbf{v}}\mathbf{X}_{:,\neg\mathbf{v}}^{\top} \quad \text{(Eq. 20)}$$

提取对角线后，通过可调系数 $\mu$ 融合为模态感知重要性向量：

$$\mathbf{M}^{\mu} = \mu \cdot \mathbf{H}_v^{\mathrm{diag}} + (1 - \mu) \cdot \mathbf{H}_l^{\mathrm{diag}} \quad \text{(Eq. 22)}$$

**变量含义**：
- $\mathbf{H}_v^{\mathrm{diag}}, \mathbf{H}_l^{\mathrm{diag}}$：视觉/语言 Hessian 的对角线，反映各自模态的通道敏感度
- $\mu \in [0,1]$：模态融合系数，$\mu \to 1$ 偏向视觉，$\mu \to 0$ 偏向语言

#### 最优系数搜索

$\mu$ 通过在校准集上最小化输出重构误差逐层确定：

$$\mu^* = \arg\min_{\mu} \|\mathbf{W}\tilde{\mathbf{X}} - \hat{\mathbf{W}}^{\mu}\mathbf{X}\|_2^2 \quad \text{(Eq. 25)}$$

其中 $\hat{\mathbf{W}}^{\mu}$ 为使用 $\mathbf{M}^{\mu}$ 作为重要性权重量化后的权重。Figure 4 展示了不同输入层的最优 $\mu$ 变化，表明模态敏感度具有显著的层间差异——浅层更依赖视觉信息，深层则趋于均衡。

![[assets/figures/papers/paper_list_l809_https_openaccess_thecvf_com_content_CVPR2026_html_Deng_VLM_PTQ_Efficient/figures/004_Figure_4.jpg]]
*Figure 4: Visualization of awareness coefficient µ in input layers of W3A16 Qwen2.5-VL-7B-Instruct, which shows the varying modality sensitivities across different layers*

---

### 统一量化流程

两个模块协同工作，最终量化步骤为：

$$\hat{\mathbf{W}}_{:,q} = \operatorname{RTN}\big(\mathbf{W}_{:,q} \cdot (1 + \mathbf{C}_{q}); \mathbf{S}^{*}, \mathbf{Z}^{*}\big)$$

其中 $\mathbf{S}^{*}, \mathbf{Z}^{*}$ 为基于模态感知重要性 $\mathbf{M}^{\mu^*}$ 计算的量化参数（缩放因子与零点）。校正项 $\mathbf{C}$ 偏移量化目标，模态感知重要性 $\mathbf{M}^{\mu}$ 调节通道权重，二者共同决定最终的离散量化点。

## 实验与分析

### 主实验结果

VLM-PTQ 在 3‑bit 和 2‑bit 纯权重量化（W3A16 / W2A16）以及 W2A8KV8 极端量化设置下，对 1B 至 72B 参数规模的 VLM 进行了系统评估。所有实验仅量化语言模型部分，视觉编码器与适配器保持全精度，校准集统一使用从 ShareGPT4V 改进的 COCO Caption 数据集中随机抽取的 128 个图文对，确保与基线 **GPTQ**（Frantar et al., arXiv 2022）和 **GPTAQ**（Li et al., arXiv 2025）的公平比较。

#### 3‑bit 与 2‑bit 纯权重量化

Table 1 汇总了 8 个 VLM 基准上的平均准确率。在 W3A16 设置下，VLM-PTQ 在所有模型规模上一致优于 GPTQ 和 GPTAQ。以 Qwen2.5-VL-7B 为例，VLM-PTQ 的平均准确率达到 **71.3%**，相比 GPTQ 的 65.0% 提升 **+6.3 个百分点**，相比 GPTAQ 的 66.6% 提升 +4.7 个百分点。在更大规模的 InternVL3-38B 和 Qwen2.5-VL-72B 上，VLM-PTQ 分别达到 78.2% 和 76.9%，同样保持领先。

![[assets/figures/papers/paper_list_l809_https_openaccess_thecvf_com_content_CVPR2026_html_Deng_VLM_PTQ_Efficient/figures/005_Table_1.jpg]]
*Table 1: Performance of 3-bit and 2-bit weight-only quantization on eight benchmarks: ChartQA, DocVQA (Validation set), MME-RealWorld (English), MME-RealWorld (Chinese), OCRBench, ScienceQA, SeedBench 2 Plus, and TextVQA (Validation set)*

在更激进的 W2A16 设置下，性能差距进一步拉大。Qwen2.5-VL-7B 上 VLM-PTQ 达到 **48.4%**，而 GPTQ 仅为 43.1%（**+5.3 个百分点**），GPTAQ 为 43.4%。InternVL3-14B 上 VLM-PTQ 达到 62.7%，InternVL3-38B 达到 69.4%，表明闭式校正项和模态感知重要性在极端低位宽下对信息保留尤为关键。

#### W2A8KV8 极端量化

Table 2 报告了 W2A8KV8（2‑bit 权重、8‑bit 激活和 KV 缓存）下的多模型性能。VLM-PTQ 在所有测试模型上继续优于 GPTQ 和 GPTAQ。Qwen2.5-VL-7B 上 VLM-PTQ 平均准确率达到约 **44.6%**，相比 GPTQ 估计值约 39.0% 提升约 **+5.6 个百分点**。这一结果验证了方法在同时压缩权重、激活和 KV 缓存的联合量化场景下的有效性。

![[assets/figures/papers/paper_list_l809_https_openaccess_thecvf_com_content_CVPR2026_html_Deng_VLM_PTQ_Efficient/figures/006_Table_2.jpg]]
*Table 2: Performance of W2A8KV8 quantization on eight benchmarks: ChartQA, DocVQA (Validation set), MME-RealWorld (English), MME-RealWorld (Chinese), OCRBench, ScienceQA, SeedBench 2 Plus, and TextVQA (Validation set)*

### 消融实验

Table 3 通过消融实验量化了闭式校正项 **C** 和模态感知重要性向量 **M** 各自对 W3A16 量化的贡献，评估基准为 MME-RealWorld（English）和 8 个基准的平均准确率。

![[assets/figures/papers/paper_list_l809_https_openaccess_thecvf_com_content_CVPR2026_html_Deng_VLM_PTQ_Efficient/figures/007_Table_3.jpg]]
*Table 3: Ablation study on the effectiveness of closed-form correction term C and modality-aware importance vector M under W3A16 quantization. We evaluate on MME-RealWorld (English) and average accuracy across eight VLM benchmarks*

以 Qwen2.5-VL-7B 为例：
- **仅添加 C**：平均准确率从 GPTQ 基线的 65.0% 提升至 **66.2%**（+1.2 个百分点），验证了将量化目标从原始权重偏移至连续最优解的有效性。
- **仅添加 M**：平均准确率达到 **70.4%**（+5.4 个百分点），表明模态感知的通道重要性加权对性能提升贡献更大——这与 Figure 3 揭示的视觉和语言 Hessian 幅度差异现象一致：标准量化器被统计占优的模态主导，导致另一模态的信息损失。
- **完整 VLM-PTQ（C + M）**：达到 **71.3%**（+6.3 个百分点），两个组件产生正向叠加效应。

消融结果表明，模态感知重要性是性能提升的主要驱动因素，而闭式校正项提供了额外但稳定的增益，两者协同实现了最优量化效果。

### 关键图表分析

**Figure 1** 从四个维度可视化了 W3A16 量化的影响：(a) 逐层输出激活 MAE 显示深层累积误差显著；(b) 8 个基准上的相对精度曲线表明 VLM-PTQ 在所有基准上均更接近全精度模型；(c) 不同参数规模模型的相对平均精度对比进一步验证方法的跨规模泛化性；(d) 输出分布与 MAE 分布揭示了量化误差的模态依赖性。

**Figure 2** 展示了闭式校正项对通道级量化损失 $L_q$ 的影响。在 Qwen2.5-VL-7B 的最后一个下投影层中，校正项 $C_q$ 与 $L_q$ 呈现明显的负相关关系：校正幅度较大的通道，其量化损失显著降低，直接验证了 Eq. 19 中偏移量化目标的理论有效性。

**Figure 3** 揭示了视觉和语言 Hessian 在不同层之间的幅度差异。在某些层中，语言 Hessian 的幅值远大于视觉 Hessian，导致标准量化器偏向语言模态。这为模态感知重要性向量的设计提供了直接的实证动机。

**Figure 4** 可视化了 W3A16 量化下各层最优模态敏感系数 $\mu$ 的变化。不同输入层的最优 $\mu$ 值差异显著，表明各层对视觉和语言模态的敏感度不同，验证了逐层独立搜索 $\mu$ 的必要性。

### 失败模式与局限性

1. **模态敏感系数的搜索开销**：逐层网格搜索 $\mu$ 增加了约 10% 的校准时间和约 30% 的内存开销。在极端大规模 VLM（如 72B 以上）上，这一开销可能成为部署瓶颈。论文未探索可微学习或在线自适应策略来替代网格搜索。

2. **仅量化语言模型部分**：视觉编码器和适配器保持全精度，未探索全模型量化。当视觉编码器参数量占比显著时（如某些轻量级 LLM 搭配大型视觉骨干），整体压缩率受限。

3. **低位宽激活未验证**：实验主要关注 INT3/INT2 权重量化和 W2A8KV8 设置，未验证 8‑bit 以下激活位宽的组合。在 INT2 激活等更极端设置下，残差传播和 Hessian 近似的稳定性需要进一步验证。

4. **模态感知的泛化边界**：方法依赖视觉掩码 $\mathbf{v}$ 区分模态，对于更复杂的多模态交织（如多图像、视频帧、交错图文）场景，二元掩码的扩展性尚不明确。

### 补充图表

![[assets/figures/papers/paper_list_l809_https_openaccess_thecvf_com_content_CVPR2026_html_Deng_VLM_PTQ_Efficient/figures/001_Figure_1.jpg]]
*Figure 1: Visualization of (a) per-layer output activation MAE of W3A16 Qwen2.5-VL-7B-Instruct, (b) relative accuracy on 8 benchmarks compared with the original 7B model, (c) relative average accuracy compared with 6 models with different parameters, (d) W3A16 model output and its MAE distributions*

## 方法谱系与知识库定位

### 1. 与基线方法的关系

VLM‑PTQ 直接建立在两类权重补偿量化方法的谱系之上，通过修正其核心假设实现性能跃迁。

**GPTQ** (Frantar et al., arXiv 2022) 是逐层权重量化的代表性基线。它将最优脑量化（OBQ）扩展为并行化框架，利用 Cholesky 分解稳定地计算逆 Hessian 矩阵，通过最小化层输出重构误差来补偿量化引入的权重扰动。然而，GPTQ 的目标函数是对称的——它假设量化前后的输出差异仅来自权重量化误差本身，忽略了前序层已量化权重传播过来的输出残差。这一假设在仅量化单层时成立，但在逐层顺序量化中不再精确。

**GPTAQ** (Li et al., arXiv 2025) 识别了上述不对称性，将输出残差 r 显式纳入补偿目标，通过拉格朗日乘子法推导出结合残差传播的权重更新公式。但 GPTAQ 在量化步骤上仍沿用 RTN（Round‑to‑Nearest）策略，直接对原始权重 w_q 取整。VLM‑PTQ 的核心发现是：在 GPTAQ 已经偏移了补偿目标的情况下，RTN 对准原始权重并非最优——理论最优的离散化目标应当是经过校正后的权重 w_q + δ，其中 δ 由输出残差与逆 Hessian 列共同决定。

换言之，VLM‑PTQ 将 GPTAQ 的“补偿‑量化”两步解耦推进为“目标校正‑量化”的一体化方案：先通过闭式校正项 C 将量化目标从 w_q 显式移向连续最优解 \hat{w}_q^*，再对校正后的权重执行 RTN。这一定位使得 VLM‑PTQ 在方法谱系中处于 GPTQ → GPTAQ → VLM‑PTQ 的递进关系，每代方法修正了前一代的一个关键近似。

### 2. 新增的知识贡献

VLM‑PTQ 为 VLM 量化领域贡献了两个可迁移的知识模块：

**闭式校正项 C** 是独立于模态的通用工具。它仅依赖当前层的输入激活 X 和逆 Hessian H^{-1}，不涉及视觉/语言的区分。因此，该校正项理论上可嵌入任何基于 Hessian 的逐层量化框架（包括纯 LLM 量化），作为对 RTN 策略的普适性增强。消融实验表明，单独添加 C 即可将 W3A16 Qwen2.5‑VL‑7B 的八基准平均准确率从 65.0% 提升至 66.2%——这是一个纯算法改进，不引入任何模态假设。

**模态感知重要性向量 M^μ** 是 VLM 特有的知识贡献。它揭示了一个此前被忽视的现象：视觉和语言 token 在 Hessian 矩阵中的贡献幅度存在显著差异（见图 3），标准量化器会天然偏向 Hessian 幅度更大的模态，导致另一模态的信息损失加剧。M^μ 通过引入可学习的融合系数 μ，将通道重要性从单一 Hessian 对角线解耦为视觉 Hessian 对角线和语言 Hessian 对角线的加权组合。这一设计将模态不平衡问题转化为一个可优化的连续参数搜索问题，为多模态模型的量化提供了新的调控维度。

### 3. 适用边界与限制

VLM‑PTQ 的适用边界由以下设计选择划定：

**量化范围限制**：方法仅量化语言模型（LLM）部分的权重，视觉编码器和跨模态适配器保持全精度。这一选择保证了公平比较（所有基线方法均采用相同设置），但也意味着 VLM‑PTQ 尚未解决视觉编码器内部特征的量化问题。对于视觉编码器占模型参数比例较大的轻量级 VLM，这一限制可能导致整体压缩率受限。

**校准开销**：模态感知系数 μ 通过逐层网格搜索确定，相比 GPTQ/GPTAQ 增加了约 10% 的校准时间和约 30% 的内存开销。对于 72B 级别的模型，这一开销仍在可接受范围内，但在资源更受限的边缘部署场景中可能成为瓶颈。当前方法未探索可微学习 μ 或跨层共享 μ 的替代策略。

**位宽验证范围**：实验覆盖了 INT3/INT2 权重量化（W3A16, W2A16）和 W2A8KV8 设置。对于更低权重位宽（如 INT2 激活）或混合精度方案，校正项 C 的数值稳定性和模态感知重要性的有效性尚未验证。特别地，在极端低位宽下，Hessian 近似的精度可能下降，残差传播的累积误差也可能放大。

**动态场景未覆盖**：μ 的搜索依赖固定的校准集，一旦校准完成便固定不变。对于输入分布剧烈变化的在线场景（如长视频理解或多轮对话），静态 μ 可能无法适应模态重要性的动态变化。

### 4. 开放问题

1. **可微 μ 学习**：当前 μ 通过网格搜索获得，是否可以通过将量化重构误差作为损失函数，以可微方式直接在反向传播中学习 μ 参数？这将显著降低校准开销，并可能发现更精细的逐 token 或逐层 μ 分配策略。

2. **校正项 C 的推广**：C 的推导依赖于逐层 Hessian 近似，在激活量化或混合精度量化场景下，Hessian 的结构会发生变化。C 的形式是否需要调整？能否推广为统一的“量化目标偏移”框架？

3. **视觉编码器量化**：当前方法仅量化 LLM 部分。视觉编码器的特征图具有空间局部性和通道冗余性，其 Hessian 结构与语言模型显著不同。校正项 C 和模态感知重要性 M 的设计范式能否直接迁移到视觉编码器的量化中？

4. **极端位宽下的稳定性**：在 INT2 激活或 W1A8 等极端设置下，残差传播的累积误差是否会破坏校正项 C 的理论保证？是否需要引入二阶校正或迭代精炼机制？

5. **动态模态感知**：是否可以在推理时根据输入动态调整 μ，例如根据视觉 token 占比或图像复杂度自适应选择融合系数？这将使方法在分布外数据上具有更强的鲁棒性。

## 原文 PDF

![[paperPDFs/CVPR_2026/VLM_PTQ_Efficient_Post_Training_Quantization_for_Large_Vision_Language_Models.pdf]]
