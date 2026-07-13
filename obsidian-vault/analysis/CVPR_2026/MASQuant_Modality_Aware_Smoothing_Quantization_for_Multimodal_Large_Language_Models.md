---
title: "MASQuant: Modality-Aware Smoothing Quantization for Multimodal Large Language Models"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/MASQuant_Modality_Aware_Smoothing_Quantization_for_Multimodal_Large_Language_Models.pdf
project_link: null
code_link: "https://github.com/alibaba/EfficientAI"
aliases:
- MMASQ
- MASQuant
tags:
- CVPR_2026
- topic/other_unclear
- topic/other_unclear/general
core_operator: 为每个模态独立学习的平滑因子（modality-aware smoothing factors）是控制量化质量的关键因果变量。通过为各模态优化专属的平滑矩阵，可以消除平滑错位，但会破坏计算不变性（需要多个量化权重），因此进一步引入低秩补偿来维持单一权重。
primary_logic: 核心洞见：跨模态的平滑后激活差异具有低秩特性。首先通过 Modal-Aware Smoothing (MAS) 为每个模态学习独立的平滑因子以消除错位；然后利用 SVD 白化将不同模态的权重差转化为低秩形式，并通过 Cross-Modal Compensation (CMC) 对文本基础量化权重进行低秩补偿，从而在推理时仅需一套量化权重即可实现模态专属适应，同时保持计算不变性。
claims:
- 统一平滑因子由主导模态决定，导致非主导模态的 SQNR 显著下降。在 Qwen2.5-Omni-3B 上，多模态输入下各层 SQNR 均低于单模态最优。
- MASQuant 在双模态（VL）和三模态（Omni）MLLM 的多个基准上，量化精度均优于现有 PTQ 方法（SmoothQuant, AWQ, MBQ 等），并在 W8A8 下匹配 FP16 性能。
- Cross-Modal Compensation 通过 SVD 白化显著降低权重残差的有效秩，使补偿所需秩减少 4 倍，仅需很少额外参数即可接近模态专属量化的 SQNR。
- MMMU 上 Accuracy = 46.6
---

# MASQuant: Modality-Aware Smoothing Quantization for Multimodal Large Language Models

> [!tip] 核心洞察
> 核心洞见：跨模态的平滑后激活差异具有低秩特性。首先通过 Modal-Aware Smoothing (MAS) 为每个模态学习独立的平滑因子以消除错位；然后利用 SVD 白化将不同模态的权重差转化为低秩形式，并通过 Cross-Modal Compensation (CMC) 对文本基础量化权重进行低秩补偿，从而在推理时仅需一套量化权重即可实现模态专属适应，同时保持计算不变性。

| 字段 | 内容 |
|------|------|
| 中文题名 | MASQuant：面向多模态大语言模型的模态感知平滑量化 |
| 英文题名 | MASQuant: Modality-Aware Smoothing Quantization for Multimodal Large Language Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.04800) · [Code](https://github.com/alibaba/EfficientAI) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | MASQuant (Modality-Aware Smoothing Quantization) |
| Dataset | MMMU, LibriSpeech, Qwen2.5-VL-7B Prefill Speed |

> [!tip] 效果简介
> - MMMU 上，Accuracy 46.6 vs 46.6 (FP16) (0 (matches FP16))。
> - LibriSpeech 上，WER (%) 3.8 vs 77.4 (Uniform smoothing) (-73.6)。
> - Qwen2.5-VL-7B Prefill Speed 上，Speedup vs FP16 2.5x vs 1x (FP16) (+1.5x)。

## 概要

多模态大语言模型（MLLM）在推理过程中，不同模态（文本、视觉、音频）的激活分布差异极大——视觉 token 的激活幅值可达文本 token 的 10 至 100 倍。这种异质性导致现有的通道级平滑量化方法（如 **SmoothQuant**，Xiao et al., ICML 2023）产生**平滑错位**（smoothing misalignment）：统一的平滑因子由主导模态决定，非主导模态被过度平滑，量化信噪比（SQNR）严重下降，最终造成显著的量化误差（Figure 2）。

针对这一问题，本文提出 **MASQuant**（Modality-Aware Smoothing Quantization），核心洞见在于：跨模态的平滑后激活差异具有**低秩特性**。方法包含两个关键模块：

1. **模态感知平滑（Modality-Aware Smoothing, MAS）**：为每种模态独立学习专属的对角平滑矩阵，直接优化量化重建的 MAE 损失，从根源上消除平滑错位。
2. **跨模态补偿（Cross-Modal Compensation, CMC）**：利用 SVD 白化将不同模态的平滑后权重差转化为低秩形式，并通过截断 SVD 得到低秩补偿矩阵。推理时以文本模态的量化权重为基础，其他模态叠加轻量的低秩修正项，从而在仅维护一套量化权重的条件下实现模态专属适应，保持计算不变性。

实验表明，MASQuant 在双模态（视觉-语言）和三模态（全模态）MLLM 的多个基准上均优于现有 PTQ 方法（SmoothQuant、**AWQ**（Lin et al., MLSys 2024）、**MBQ**（Li et al., CVPR 2025）等）。在 W8A8 设置下，MASQuant 的精度可匹配 FP16 基线；在 W4A8 下，LibriSpeech 的词错误率（WER）从统一平滑的 77.4% 降至 3.8%。端到端测试中，Qwen2.5-VL-7B 在 W4A4 设置下实现 2.5 倍预填充加速，且延迟开销极小。

### 多模态大语言模型的量化困境

多模态大语言模型（MLLM）通过同时处理文本、视觉和音频等多种模态信息，在视觉问答、语音识别等任务中展现出强大的能力。然而，这类模型庞大的参数量和计算开销严重阻碍了其在资源受限设备上的部署。训练后量化（PTQ）作为一种关键的模型压缩技术，通过将高精度浮点权重和激活值映射到低比特整数表示，能够显著降低模型的内存占用和推理延迟。

在众多 PTQ 方法中，通道级平滑量化（channel-wise smoothing quantization）因其能够有效缓解激活值中的离群值（outlier）问题而成为主流范式。其核心思想是引入一个平滑因子矩阵 $\mathbf{S}$，将原始线性层 $\mathbf{Y} = \mathbf{X}\mathbf{W}$ 等价变换为：

$$\mathbf{Y} = (\mathbf{X} \mathbf{S}^{-1}) \cdot (\mathbf{S} \mathbf{W})$$

通过将量化难度从激活值 $\mathbf{X}$ 迁移到权重 $\mathbf{W}$，使得激活值分布更加平坦，从而降低量化误差。**SmoothQuant**（Xiao et al., ICML 2023）是这一范式的代表性工作，其统一平滑因子由激活值和权重的最大绝对值共同决定。

### 平滑错位：多模态场景下的根本瓶颈

然而，当上述通道级平滑量化方法被直接应用于多模态大语言模型时，一个根本性的问题浮现出来——**平滑错位（smoothing misalignment）**。如图 1(a) 所示，在 MLLM 的多模态推理过程中，不同 Transformer 层乃至同一层内的不同组件，其激活值的主导模态可能截然不同：某些层以文本模态为主，而另一些层则以视觉或音频模态为主。这种模态主导权的动态变化，源于不同模态输入在特征空间中的统计特性存在巨大差异——视觉 token 的激活幅值可达文本 token 的 10 到 100 倍。

现有的统一平滑策略在计算平滑因子 $\mathbf{s}^{\text{uni}}$ 时，将所有模态的激活值混合在一起取最大值：

$$\mathbf{s}_i^{\text{uni}} = \frac{(\max_{m,t} |\mathbf{x}^{m}_{t,i}|)^{\beta}}{(\max_j |w_{j,i}|)^{1-\beta}} \propto \mathbf{R}_i^{m^*}$$

这意味着平滑因子实际上由激活范围最大的**主导模态** $m^*$ 决定。如图 4 所示，在 Qwen2.5-Omni 和 Qwen2.5-VL 系列模型中，SmoothQuant 的统一平滑因子在不同层中分别被视觉、音频或文本模态主导，非主导模态的平滑因子严重偏离其理想值。

这种偏离造成的后果是灾难性的。理论分析（Eq. 17）表明，当使用由主导模态 $m'$ 决定的统一平滑因子去量化非主导模态 $m$ 时，其信号量化噪声比（SQNR）将遭受如下衰减：

$$\text{SQNR}(\mathbf{s}^{\text{uni}}, \mathbf{x}_t^{m'}) = \text{SQNR}(\mathbf{s}^{m'}, \mathbf{x}_t^{m'}) - 10\log_{10}\left(\frac{d(\min_i (\alpha_i^{m,m'})^2)}{\sum_{i=1}^{d} \frac{1}{(\alpha_i^{m,m'})^2}}\right)$$

其中 $\alpha_i^{m,m'}$ 表示两模态在各通道上的幅度比。衰减程度取决于这些比值在通道间的非均匀性——差异越大，量化质量恶化越严重。图 2 在 Qwen2.5-Omni-3B 上验证了这一理论：在多模态输入条件下，各层的平均 SQNR 始终低于任意单一模态的最优 SQNR，证实了平滑错位是普遍存在的系统性问题。

### 计算不变性的两难困境

解决平滑错位最直接的方式是为每种模态独立学习专属的平滑矩阵 $\mathbf{S}_m$。然而，这会破坏量化中的**计算不变性（computational invariance）**——由于不同模态的平滑后权重 $\mathbf{S}_m\mathbf{W}$ 各不相同，推理时需要为每个模态存储一套独立的量化权重，导致内存开销随模态数量线性增长，完全抵消了量化带来的存储优势。

现有的模态平衡量化方法如 **MBQ**（Li et al., CVPR 2025）试图通过模态平衡重建损失来优化统一的平滑因子，但这本质上是在不同模态之间寻求折中，无法从根本上消除平滑错位，在模态差异极大的场景（如音频与文本）下仍然面临显著的性能退化。

### MASQuant 的核心动机

上述分析揭示了多模态大语言模型量化面临的核心矛盾：**模态感知的平滑因子是消除平滑错位的必要条件，但直接使用多套量化权重又会丧失计算不变性带来的存储和推理效率优势。**

MASQuant 的设计动机正是要打破这一困境。其核心洞见在于：跨模态的平滑后激活差异具有低秩特性。这意味着可以在推理时仅维护一套文本模态的基础量化权重，同时通过轻量的低秩修正矩阵来补偿其他模态与文本模态之间的差异，从而同时实现模态专属的量化精度和单一权重的计算效率。这一思路为多模态大语言模型的高效部署开辟了新的技术路径。

## 核心方法与创新机理

### 问题根源：模态间的平滑错位（Smoothing Misalignment）

多模态大语言模型（MLLM）在推理过程中，不同模态的激活分布存在巨大差异。视觉 token 的激活幅值可达文本 token 的 10–100 倍，且不同模态在模型的各组件中交替占据主导地位（Figure 1a）。现有的通道级平滑量化方法（如 **SmoothQuant** (Xiao et al., ICML 2023)）在计算统一平滑因子时，仅从混合模态的激活中提取最大幅值来决定缩放方向，导致平滑因子由主导模态决定（Figure 4），而非主导模态被过度平滑，产生严重的量化误差。理论分析（Theorem 1）表明，这种平滑错位会使非主导模态的 SQNR 显著衰减，衰减程度取决于各通道幅度比 α_i 的非均匀性：

$$ \mathrm { S Q N R } ( \mathbf { s } ^ { \mathrm { u n i } } , \mathbf { x } _ { t } ^ { m ^ { \prime } } ) = \mathrm { S Q N R } ( \mathbf { s } ^ { m ^ { \prime } } , \mathbf { x } _ { t } ^ { m ^ { \prime } } ) - 1 0 \log _ { 1 0 } \left( \frac { d ( \operatorname* { m i n } _ { i } ( \alpha _ { i } ^ { m , m ^ { \prime } } ) ^ { 2 } ) } { \sum _ { i = 1 } ^ { d } \frac { 1 } { ( \alpha _ { i } ^ { m , m ^ { \prime } } ) ^ { 2 } } } \right) $$

实验证实，在 Qwen2.5-Omni-3B 的多模态输入下，各层 SQNR 均低于单模态最优（Figure 2），音频模态在低比特量化下更是出现灾难性崩溃（Table 2，LibriSpeech WER 达 77.4）。

### Changed Slot 1：从统一平滑到模态感知平滑（MAS）

**Baseline 做法**：SmoothQuant 等现有方法为所有模态计算单一的统一平滑因子 s_i^uni，该因子由混合模态激活的最大幅值决定（Eq.11），无法适应不同模态的分布特性。

**MASQuant 创新**：提出 **Modality-Aware Smoothing (MAS)**，为每种模态独立维护专属的对角平滑矩阵 S_m。每个通道的平滑因子初始化为该模态激活最大绝对值与权重最大绝对值之比的平方根：

$$ s_i^m = \sqrt{ \frac{ \max_t |x_{t,i}^m| }{ \max_j |w_{j,i}| } } $$

随后，通过直接优化各模态的量化重建 MAE 损失来学习最优的 S_m，而非像 SmoothQuant 那样在 β 参数空间搜索：

$$ \{ \mathbf { S } _ { m } ^ { * } \} = \underset { \{ \mathbf { S } _ { m } \} } { \arg \operatorname* { m i n } } \sum _ { m \in \mathcal { M } } ( \lambda _ { m } \cdot \mathcal { L } _ { \mathrm { M A E } } ( \mathbf { S } _ { m } , \mathbf { X } _ { m } , \mathbf { W } ) ) $$

这一设计从根源上消除了平滑错位：每个模态的平滑因子完全由自身激活分布决定，不受其他模态干扰。消融实验（Table 3）表明，仅将统一平滑替换为 MAS，LibriSpeech 的 WER 便从 77.4 骤降至 3.8，平均精度提升至 61.2，充分验证了消除平滑错位的必要性。

### Changed Slot 2：从多套量化权重到低秩跨模态补偿（CMC）

**MAS 带来的新问题**：模态专属平滑虽消除了错位，但破坏了 SmoothQuant 的计算不变性——不同模态需要不同的量化权重 Q(S_m W)，导致存储和计算开销随模态数线性增长。

**核心洞见**：跨模态的平滑后激活差异具有低秩特性。MASQuant 发现，不同模态平滑后权重的残差 ΔW = S_m W - S_t W 在经过 SVD 白化后，其有效秩显著降低（Figure 5a），这意味着可以用极少的参数来补偿模态差异。

**CMC 设计**：**Cross-Modal Compensation (CMC)** 以文本模态的平滑权重 S_t W 为基准，仅存储一套文本基量化权重 Q(S_t W)。对于其他模态，通过白化后的截断 SVD 将权重残差转化为低秩校正矩阵：

$$ \Delta \mathbf { W } \approx \mathbf { L } _ { 1 } \mathbf { L } _ { 2 } , \quad \mathbf { L } _ { 1 } = \mathbf { T } ^ { - 1 } \mathbf { U } _ { r } , \; \mathbf { L } _ { 2 } = \Sigma _ { r } \mathbf { V } _ { r } ^ { \top } $$

推理时，文本模态直接使用基量化权重；非文本模态在基权重计算结果上叠加对应的低秩修正项，实现模态专属适应：

$$ \mathbf { Y } = \left\{ \begin{array} { r } { \mathrm { Q } ( \mathbf { X } _ { m } \mathbf { S } _ { m } ^ { - 1 } ) \cdot \mathrm { Q } ( \mathbf { S } _ { t } \mathbf { W } ) , \, m = \text{text} } \\ { \mathrm { Q } ( \mathbf { X } _ { m } \mathbf { S } _ { m } ^ { - 1 } ) \cdot \mathrm { Q } ( \mathbf { S } _ { t } \mathbf { W } ) + \mathbf { X } _ { m } \mathbf { S } _ { m } ^ { - 1 } \cdot \mathbf { L } _ { 1 } ^ { m } \mathbf { L } _ { 2 } ^ { m } , \, m \neq \text{text} } \end{array} \right. $$

SVD 白化使补偿所需秩减少 4 倍：在秩比仅 0.08 时，CMC 的 SQNR 即超越单独使用 MAS（Figure 6），且额外的低秩矩阵参数量极小（Table 6），实现了“一套量化权重服务所有模态”的计算不变性。

### 创新总结

MASQuant 的两个 changed slot 构成了“先解耦，后补偿”的完整方案：MAS 通过模态专属平滑因子消除平滑错位，将各模态推向量化最优；CMC 则利用跨模态差异的低秩特性，以极少的额外参数恢复计算不变性。这一设计使得 MASQuant 在 W8A8 下即可匹配 FP16 精度（Table 1, MMMU 46.6），并在 W4A4 极端量化下实现 2.5 倍推理加速（Table 7），同时将音频模态从崩溃边缘（WER 77.4）拉回可用水平（WER 3.8）。

MASQuant 框架由两个级联的核心模块构成：**模态感知平滑（Modality-Aware Smoothing, MAS）** 和 **跨模态补偿（Cross-Modal Compensation, CMC）**。其设计目标是在多模态大语言模型的训练后量化（PTQ）中，同时解决平滑错位与跨模态计算不变性两大瓶颈。

### 问题根源与设计动机

在多模态推理过程中，不同模态的激活分布差异巨大——视觉 token 的激活幅值可达文本 token 的 10–100 倍。现有的通道级平滑量化方法（如 **SmoothQuant**（Xiao et al., ICML 2023））通过从混合模态激活中计算统一平滑因子来迁移量化难度，但这一统一因子实际上由激活范围最大的“主导模态”决定（Figure 4）。其后果是：非主导模态被施加了与其自身统计特性严重偏离的平滑因子，产生**平滑错位**，导致该模态的量化信噪比（SQNR）大幅衰减（Figure 2）。

### Pipeline 总览

MASQuant 的完整流程分为校准阶段与推理阶段，如 Figure 3 所示：

![[assets/figures/papers/paper_list_l763_https_arxiv_org_abs_2603_04800/figures/003_Figure_3.jpg]]
*Figure 3: The illustrated case demonstrates a text-vision dualmodal setting. (a) Schematic workflow of MAS and CMC with calibration data, (b) Illustration of how low-rank matrices L1 and L2 in CMC are utilized in MASQuant, exemplified with an MLP block*

1. **校准阶段（Calibration）**：
   - **MAS**：为每种模态独立初始化对角平滑矩阵 $\mathbf{S}_m$，并通过最小化模态专属的量化重建 MAE 损失，直接优化各模态的平滑因子，从而从根本上消除平滑错位。
   - **CMC**：在 MAS 得到各模态平滑因子后，以文本模态的平滑后权重 $\mathbf{S}_t \mathbf{W}$ 为基，计算其他模态平滑后权重与基权重的残差 $\Delta\mathbf{W}$。利用 SVD 白化将 $\Delta\mathbf{W}$ 转化为低秩形式，再通过截断 SVD 得到低秩补偿矩阵 $\mathbf{L}_1^m, \mathbf{L}_2^m$，以极少的额外参数补偿模态差异。

2. **推理阶段（Inference）**：
   - 文本模态直接使用文本平滑的量化权重：$\mathrm{Q}(\mathbf{X}_t \mathbf{S}_t^{-1}) \cdot \mathrm{Q}(\mathbf{S}_t \mathbf{W})$。
   - 非文本模态在基权重计算的基础上，叠加对应的低秩修正项：$\mathrm{Q}(\mathbf{X}_m \mathbf{S}_m^{-1}) \cdot \mathrm{Q}(\mathbf{S}_t \mathbf{W}) + \mathbf{X}_m \mathbf{S}_m^{-1} \cdot \mathbf{L}_1^m \mathbf{L}_2^m$。

这一设计使得推理时仅需存储**一套文本基量化权重**，其他模态通过轻量低秩矩阵实现模态专属适应，在保持计算不变性的同时消除了平滑错位。

### 问题形式化：平滑错位的量化分析

多模态大语言模型（MLLM）中，不同模态的激活幅度差异巨大——视觉 token 的幅值可达文本 token 的 10–100 倍。当采用通道级平滑量化（如 **SmoothQuant** (Xiao et al., ICML 2023)）时，统一平滑因子 $\mathbf{s}^{\mathrm{uni}}$ 由主导模态（通常为视觉）的激活范围决定：

$$
\mathbf { s } _ { i } ^ { \mathrm { u n i } } = \frac { ( \operatorname* { m a x } _ { m , t } | \mathbf { x } ^ { \mathrm { m } } _ { t , i } | ) ^ { \beta } } { ( \operatorname* { m a x } _ { j } | w _ { j , i } | ) ^ { 1 - \beta } } \propto \mathbf { R } _ { i } ^ { m ^ { * } }
$$

这导致非主导模态的平滑因子严重偏离其理想值，产生**平滑错位**（smoothing misalignment）。定量地，非主导模态 $m'$ 在统一平滑下的 SQNR 衰减可表示为：

$$
\mathrm { S Q N R } ( \mathbf { s } ^ { \mathrm { u n i } } , \mathbf { x } _ { t } ^ { m ^ { \prime } } ) = \mathrm { S Q N R } ( \mathbf { s } ^ { m ^ { \prime } } , \mathbf { x } _ { t } ^ { m ^ { \prime } } ) - 1 0 \log _ { 1 0 } \left( \frac { d ( \operatorname* { m i n } _ { i } ( \alpha _ { i } ^ { m , m ^ { \prime } } ) ^ { 2 } ) } { \sum _ { i = 1 } ^ { d } \frac { 1 } { ( \alpha _ { i } ^ { m , m ^ { \prime } } ) ^ { 2 } } } \right)
$$

其中 $\alpha_i^{m,m'}$ 为两模态在第 $i$ 通道的幅度比。衰减程度取决于各通道幅度比的非均匀性——幅度差异越大，SQNR 损失越严重。Figure 2 在 Qwen2.5-Omni-3B 上验证了这一理论：多模态输入下各层平均 SQNR 均显著低于单模态最优水平。

### 模块一：Modality-Aware Smoothing (MAS)

MAS 的核心思想是**为每种模态独立学习平滑因子**，从根本上消除平滑错位。对于模态 $m \in \mathcal{M}$，定义对角平滑矩阵 $\mathbf{S}_m = \operatorname{diag}(s_1^m, \dots, s_d^m)$，其初始值由该模态自身的激活-权重幅值比决定：

$$
s_i^m = \sqrt{ \frac{ \max_t |x_{t,i}^m| }{ \max_j |w_{j,i}| } }
$$

随后通过直接优化 $\mathbf{S}_m$ 来最小化模态专属的量化重建 MAE 损失：

$$
\{ \mathbf { S } _ { m } ^ { * } \} = \underset { \{ \mathbf { S } _ { m } \} } { \arg \operatorname* { m i n } } \sum _ { m \in \mathcal { M } } ( \lambda _ { m } \cdot \mathcal { L } _ { \mathrm { M A E } } ( \mathbf { S } _ { m } , \mathbf { X } _ { m } , \mathbf { W } ) )
$$

其中 $\lambda_m$ 为模态损失权重（消融实验表明等权重 $\lambda_t = \lambda_v$ 最优），$\mathcal{L}_{\mathrm{MAE}}$ 衡量量化前后输出的平均绝对误差。与 SmoothQuant 通过搜索单一 $\beta$ 的间接方式不同，MAS 将平滑因子作为自由参数直接优化，从而将通道级平滑推向优化极限。

MAS 推理时的前向过程为：

$$
\mathbf{Y} = \operatorname{Q}(\mathbf{X}_m \mathbf{S}_m^{-1}) \cdot \operatorname{Q}(\mathbf{S}_m \mathbf{W}), \quad m \in \mathcal{M}
$$

但这一形式破坏了计算不变性：每种模态需要独立的量化权重 $\operatorname{Q}(\mathbf{S}_m \mathbf{W})$，导致存储和计算开销随模态数线性增长。

### 模块二：Cross-Modal Compensation (CMC)

CMC 解决的核心矛盾是：如何在保持单一量化权重的条件下，实现模态专属的适应能力。其关键洞见在于**跨模态的平滑后权重差具有低秩特性**。

以文本模态为参考基，定义视觉模态的权重残差：

$$
\Delta \mathbf{W} = \mathbf{S}_v \mathbf{W} - \mathbf{S}_t \mathbf{W}
$$

直接对 $\Delta \mathbf{W}$ 做低秩分解效率不高。CMC 引入 **SVD 白化**（SVD-based Whitening）来降低残差的有效秩：先计算文本平滑权重的协方差矩阵 $\mathbf{C} = (\mathbf{S}_t \mathbf{W})(\mathbf{S}_t \mathbf{W})^\top$，通过 Cholesky 分解得到白化矩阵 $\mathbf{T}$，使得 $\mathbf{T}(\mathbf{S}_t \mathbf{W})$ 的各行不相关。对白化后的残差进行截断 SVD，再反白化得到低秩补偿矩阵：

$$
\Delta \mathbf { W } \approx \mathbf { L } _ { 1 } \mathbf { L } _ { 2 } , \quad \mathbf { L } _ { 1 } = \mathbf { T } ^ { - 1 } \mathbf { U } _ { r } , \; \mathbf { L } _ { 2 } = \Sigma _ { r } \mathbf { V } _ { r } ^ { \top }
$$

其中 $\mathbf{U}_r, \Sigma_r, \mathbf{V}_r$ 为白化残差的秩-$r$ 截断 SVD 结果。Figure 5 证实，白化后 $\Delta \mathbf{W}$ 的有效秩在各层均大幅下降；Figure 6 进一步表明，CMC 仅需非白化基线 1/4 的秩即可达到同等补偿效果，SQNR 在秩比 0.08 时即超越单独使用 MAS。

最终推理时，文本模态直接使用文本平滑的量化权重；其他模态在基权重计算后叠加对应的低秩修正项：

$$
\mathbf { Y } = \left\{ \begin{array} { r } { \mathrm { Q } ( \mathbf { X } _ { m } \mathbf { S } _ { m } ^ { - 1 } ) \cdot \mathrm { Q } ( \mathbf { S } _ { t } \mathbf { W } ) , \, m = \text{text} } \\ { \mathrm { Q } ( \mathbf { X } _ { m } \mathbf { S } _ { m } ^ { - 1 } ) \cdot \mathrm { Q } ( \mathbf { S } _ { t } \mathbf { W } ) + \mathbf { X } _ { m } \mathbf { S } _ { m } ^ { - 1 } \cdot \mathbf { L } _ { 1 } ^ { m } \mathbf { L } _ { 2 } ^ { m } , \, m \neq \text{text} } \end{array} \right.
$$

这一设计使推理时仅需存储一套文本基量化权重 $\operatorname{Q}(\mathbf{S}_t \mathbf{W})$，非文本模态通过轻量的低秩矩阵 $\mathbf{L}_1^m, \mathbf{L}_2^m$ 进行补偿，额外参数开销为 $O(2dr)$，其中 $r \ll d$。Table 6 定量展示了 CMC 在解码阶段的计算成本与内存占用优势。

### 方法谱系与知识库定位

MASQuant 继承并扩展了通道级平滑量化的技术路线。**SmoothQuant** (Xiao et al., ICML 2023) 开创了通过数学等价的平滑变换将激活异常值迁移至权重的范式，但其统一平滑因子在多模态场景下产生错位。**AWQ** (Lin et al., MLSys 2024) 引入激活感知的权重保护，但仅针对权重进行量化。**MBQ** (Li et al., CVPR 2025) 首次关注多模态量化中的模态平衡问题，通过统一平滑因子的模态平衡重建来缓解偏差，但未从根本上消除平滑错位。MASQuant 的 MAS 模块通过模态专属平滑因子的直接优化，将错位问题从“缓解”推向“消除”；CMC 模块则通过 SVD 白化与低秩补偿，在保持计算不变性的前提下实现了模态专属适应，这是此前方法均未解决的系统性难题。

## 实验与关键发现

### 核心实验设置

MASQuant 在两个多模态大语言模型系列上进行了全面评估：双模态的 **Qwen2.5-VL-3B/7B**（文本-视觉）和三模态的 **Qwen2.5-Omni-3B/7B**（文本-视觉-音频）。对比基线包括当前主流的训练后量化方法：**SmoothQuant**（Xiao et al., ICML 2023）、**AWQ**（Lin et al., MLSys 2024）、**OmniQuant**（Shao et al., arXiv 2023）以及专门针对多模态的 **MBQ**（Li et al., CVPR 2025）。评估覆盖权重量化与激活量化的多种组合（W4A16, W4A8, W4A6, W4A4），并在多模态基准上全面测试。

### 主要结果

#### 视觉-语言任务上的量化精度

在 Qwen2.5-VL-3B 和 7B 上，MASQuant 在多个精度级别下均取得最优平均精度（Table 1）。

![[assets/figures/papers/paper_list_l763_https_arxiv_org_abs_2603_04800/figures/004_Table_1.jpg]]
*Table 1: Comparison of MASQuant with existing quantization methods on multimodal benchmarks. OCR: OCRBench. Viz: Vizwiz. S-QA: ScienceQA. T-VQA: TextVQA. SQ: SmoothQuant. The best results are highlighted in bold*

- **W4A16 设置**：Qwen2.5-VL-3B 上 MASQuant 平均精度达 69.9，超越 SmoothQuant（68.9）和 AWQ（69.3），且与 MBQ（69.6）相比仍有提升；Qwen2.5-VL-7B 上平均精度 74.2，同样领先所有基线。
- **W4A8 设置**：MASQuant 在 Qwen2.5-VL-7B 上达到 73.2 的平均精度，与 FP16 的 74.3 差距仅 1.1 个百分点，而 SmoothQuant 已降至 71.8。
- **W8A8 设置**：MASQuant 在 MMMU 上达到 46.6，精确匹配 FP16 性能（46.6），证明高比特下可完全恢复原始精度。

关键趋势：随着量化比特降低，SmoothQuant 等统一平滑方法性能急剧下降，而 MASQuant 的精度衰减显著更平缓，验证了模态感知平滑对低比特鲁棒性的关键作用。

#### 全模态任务上的量化精度

在三模态 Qwen2.5-Omni-3B/7B 上，MASQuant 在视觉、音频和文本任务上均展现出显著优势（Table 2）。

- **音频模态的灾难性崩溃被消除**：在 LibriSpeech 基准上，统一平滑方法在 W4A8 下 WER 飙升至 77.4（基本失效），而 MASQuant 将 WER 压至 3.8，接近 FP16 的 3.2。这直接验证了平滑错位在非主导模态上造成严重量化误差的核心论断。
- **视觉任务**：MMMU 上 MASQuant 在 W4A8 下达到 43.7，优于 SmoothQuant（41.2）和 MBQ（42.8）。
- **文本任务**：MMLU 上 MASQuant 在 W4A8 下保持 69.1，与 FP16（69.8）差距微小。

#### 推理效率

在 RTX 4090 上对 Qwen2.5-VL-7B 的端到端预填充阶段测试（Table 7），MASQuant 在 W4A4 设置下实现 **2.5 倍加速**（batch size 1），且随着 batch size 增大加速比保持稳定。CMC 引入的低秩补偿矩阵带来的额外计算开销极小：解码阶段每 token 额外 FLOPs 为 $2drm$（Table 6），其中 $d$ 为隐藏维度，$r$ 为秩，$m$ 为额外模态数，在典型设置下占比不到 1%。

![[assets/figures/papers/paper_list_l763_https_arxiv_org_abs_2603_04800/figures/012_Table_7.jpg]]
*Table 7: End-to-end prefill-stage performance of Qwen2.5-VL-7B on Desktop RTX 4090 with fused GPU kernels (sequence length = 2048) under W4A4 setting. MAS: MASQuant. BS: Batch Size*

### 消融实验

#### 模态感知平滑（MAS）的核心作用

Table 3 对比了统一平滑与 MAS 在 W4A8 下的性能差异。在 LibriSpeech 上，统一平滑的 WER 高达 77.4，而 MAS 直接降至 3.8，降幅达 73.6 个百分点。同时，MAS 将平均精度从 57.8 提升至 61.2。这直接证明了消除平滑错位是多模态 PTQ 的核心瓶颈。

![[assets/figures/papers/paper_list_l763_https_arxiv_org_abs_2603_04800/figures/009_Table_3.jpg]]
*Table 3: Effects of Modality-Aware Smoothing (W4A8)*

Table 5 展示了 MAS 训练的收敛性：第 2 epoch 时平均精度达到峰值 61.2，之后趋于稳定，表明模态感知平滑因子的优化快速且稳定。

![[assets/figures/papers/paper_list_l763_https_arxiv_org_abs_2603_04800/figures/011_Table_5.jpg]]
*Table 5: Effects of Modality-Aware Smoothing (W4A8)*

#### 模态损失权重的敏感性

Table 4 研究了不同模态损失权重组合的影响。当仅偏重文本模态（$\lambda_t=1, \lambda_v=0$）时，视觉任务精度显著下降；仅偏重视觉模态（$\lambda_t=0, \lambda_v=1$）则导致文本 PPL 上升。**等权重策略**（$\lambda_t=\lambda_v$）在所有指标上获得最佳整体性能，证明多模态均衡优化对量化质量至关重要。

![[assets/figures/papers/paper_list_l763_https_arxiv_org_abs_2603_04800/figures/010_Table_4.jpg]]
*Table 4: Effects of Modality Loss Weight (W4A8)*

#### 跨模态补偿（CMC）的有效性与效率

Figure 5 揭示了 CMC 的核心机理：SVD 白化后跨模态权重残差 $\Delta\mathbf{W}$ 的有效秩在各层显著下降，使得低秩近似成为可能。Figure 6 在 W4A6 设置下量化了补偿效率：CMC 在秩比仅 0.08 时 SQNR 即超越单独使用 MAS，且 SQNR 随秩比增加快速接近模态专属量化的理论上限。**CMC 仅需非白化基线 1/4 的秩即可达到 MBQ 相当的补偿效果**，验证了白化策略对压缩补偿参数的关键作用。

### 失败模式与局限分析

1. **极低比特下的性能衰减**：虽然 MASQuant 在 W4A4 下仍优于所有基线，但与 FP16 的差距有所扩大。这源于极低比特下量化误差本身的非线性增长，模态感知平滑虽能消除错位，但无法完全补偿量化网格的粗糙度。

2. **模态数量扩展的边际成本**：CMC 为每个额外模态引入独立的低秩补偿矩阵，参数开销与模态数线性增长（Table 6 中内存开销为 $2dr \times m$）。当模态数较多时，需要在补偿精度与存储开销间权衡。

3. **校准数据依赖性**：MAS 的平滑因子优化依赖模态特定的校准数据，若校准数据分布与实际推理分布存在偏移，可能导致次优平滑。论文未提供跨分布泛化性的系统分析，该点需在实际部署中手动验证。

## 定位与知识库关联

### 问题定位：多模态量化中的平滑错位

多模态大语言模型（MLLM）中，不同模态的激活幅度存在数量级的差异——视觉 token 的幅值可达文本 token 的 10–100 倍。这一现象导致现有的通道级平滑量化方法（如 **SmoothQuant** (Xiao et al., ICML 2023)）在 MLLM 场景下出现根本性失效：统一平滑因子由幅值最大的主导模态决定（Figure 4 证实了这一点），非主导模态被迫接受与其激活统计特性严重不匹配的平滑尺度，造成平滑错位（smoothing misalignment），进而引发量化信噪比（SQNR）的灾难性下降（Figure 2, Theorem 1）。

### 方法谱系中的位置

MASQuant 处于“多模态大语言模型后训练量化（PTQ）”这一细分赛道，其核心贡献在于首次系统性地识别并解决了跨模态平滑错位问题，同时通过低秩补偿维持了计算不变性。在方法谱系中，其与相关工作的关系如下：

| 方法 | 核心机制 | 与 MASQuant 的关系 |
|------|----------|-------------------|
| **SmoothQuant** (Xiao et al., ICML 2023) | 通道级平滑量化，将激活离群值迁移到权重 | 基石方法，但统一平滑因子在 MLLM 中失效；MAS 将其泛化为模态感知版本 |
| **AWQ** (Lin et al., MLSys 2024) | 基于激活幅值的逐通道权重缩放 | 同属平滑量化家族，通过搜索 β 优化平滑因子；MAS 直接优化平滑矩阵，自由度更高 |
| **OmniQuant** (Shao et al., arXiv 2023) | 可学习的权重裁剪与平滑 | 引入可学习范式，但未考虑模态异质性；MASQuant 将可学习思想扩展到模态维度 |
| **MBQ** (Li et al., CVPR 2025) | 模态均衡重建损失，统一平滑因子 | 最直接的前置工作，通过均衡损失缓解模态偏置，但仍使用单一平滑因子；MASQuant 从根本上为各模态分配独立平滑因子 |

MASQuant 的方法学贡献可概括为“解耦—补偿”两步范式：**Modality-Aware Smoothing (MAS)** 通过为每种模态独立学习对角平滑矩阵 $\mathbf{S}_m$，将平滑因子的优化从搜索单一 β 提升为直接优化自由参数（Eq. 12-14），消除平滑错位；**Cross-Modal Compensation (CMC)** 则利用跨模态权重差经过 SVD 白化后的低秩特性（Figure 5 显示有效秩显著下降），以极少的低秩参数 $\mathbf{L}_1^m, \mathbf{L}_2^m$ 补偿非文本模态与文本基量化权重的差异（Eq. 22-25），从而在推理时仅需存储一套量化权重 $\mathrm{Q}(\mathbf{S}_t \mathbf{W})$。

### 适用边界与局限

**适用场景**：MASQuant 的设计前提是多模态输入下激活幅度的跨模态异质性。当 MLLM 的视觉编码器输出 token 幅值远超文本 token 时，该方法的收益最为显著。实验覆盖了双模态（Qwen2.5-VL 系列）和三模态（Qwen2.5-Omni 系列，含音频）MLLM，在 W4A8、W4A6、W4A4 等多种精度设置下均验证了有效性（Table 1, Table 2）。

**已知局限**：
- CMC 引入的额外计算开销与模态数量 $m$ 和补偿秩 $r$ 成正比（Table 6），当模态数量较多或秩需求较高时，低秩修正项的推理开销会相应增加。不过，实验表明 SVD 白化使所需秩减少约 4 倍（Figure 5），在秩比 0.08 时即超越单独 MAS 的 SQNR，实际开销可控。
- 论文未报告在超过三种模态（如触觉、点云等）的 MLLM 上的验证，三模态以上的泛化性需要手动验证。
- 校准过程需要为每种模态准备校准数据，且 MAS 的优化需要 2 个 epoch 达到峰值性能（Table 5），校准成本高于单模态 PTQ 方法。

### 与 Follow-up 工作的潜在关联

MASQuant 的“模态感知平滑 + 低秩补偿”范式为后续研究打开了几个方向：
1. **动态模态路由**：CMC 的低秩补偿矩阵 $\mathbf{L}_1^m, \mathbf{L}_2^m$ 本质上是一种模态适配器，可与 MoE（混合专家）架构中的专家路由机制结合，实现更细粒度的模态感知计算。
2. **量化感知的模态融合**：当前 MAS 独立优化各模态的平滑因子，模态间的交互仅在 CMC 的残差补偿中隐式体现。未来工作可探索在平滑因子优化中引入跨模态约束，进一步提升量化鲁棒性。
3. **训练后量化的训练阶段协同**：MASQuant 的平滑因子学习范式（直接优化 $\mathbf{S}_m$ 而非搜索 β）可反向指导量化感知训练（QAT）中平滑矩阵的初始化策略。

### 开放问题

1. **音频模态的极端敏感性**：Table 2 显示，在 W4A4 设置下，SmoothQuant 和 MBQ 在 LibriSpeech 上的 WER 分别飙升至 77.4 和 85.5，而 MASQuant 将其降至 3.8。音频模态为何对量化误差如此敏感？其激活分布是否存在特殊的尖峰结构？论文未对此给出机理解释。
2. **SVD 白化的理论基础**：CMC 的 SVD 白化步骤被证明能有效降低 $\Delta\mathbf{W}$ 的有效秩，但论文未严格证明为何跨模态权重差在白化后呈现低秩——这一性质可能与 MLLM 中跨模态共享的语义子空间有关，需要进一步的理论分析。
3. **与 KV-Cache 量化的协同**：MLLM 推理中 KV-Cache 的内存瓶颈同样显著。MASQuant 的模态感知思想是否可迁移到 KV-Cache 量化中，实现模态自适应的缓存压缩，是值得探索的开放方向。

## 原文 PDF

![[paperPDFs/CVPR_2026/MASQuant_Modality_Aware_Smoothing_Quantization_for_Multimodal_Large_Language_Models.pdf]]
