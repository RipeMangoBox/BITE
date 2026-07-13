---
title: "SERQ: Saliency-Aware Low-Rank Error Reconstruction for LLM Quantization"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/SERQ_Saliency_Aware_Low_Rank_Error_Reconstruction_for_LLM_Quantization.pdf
project_link: null
code_link: https://github.com/acalabys/SERQ
openreview_forum_id: nFjj8NEBqv
aliases:
- SERQ
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "通过将激活显著性融入权重矩阵并仅对最显著的权重行进行误差重建，使用单个低秩矩阵同时补偿激活离群值与权重显著性的量化误差，并完全离线处理展平与置换。"
primary_logic: "激活离群值的危害可以通过静态展平转嫁到权重上，而权重的显著性分布恰可指导低秩误差重建集中在少数关键行，从而用一个量化后的低秩残差矩阵即可恢复精度，且无需在线变换或顺序分支。"
claims:
- "SERQ 仅使用单个低秩矩阵重构显著行的量化误差，避免双因子带来的在线量化和顺序计算。"
- "在所有W4A4与W4A8配置下，SERQ 的困惑度和零样本推理精度均显著优于 L2QER、LLM.int4() 以及基于旋转的 QuaRot/SpinQuant。"
- "静态激活展平与离线权重置换合并到权重参数中，推理时零额外延迟开销。"
- "端到端GPU推理中，SERQ-MXFP4 实现超过2倍的整体加速，同时相对于FP16降低峰值内存占用约2.48倍。"
---

# SERQ: Saliency-Aware Low-Rank Error Reconstruction for LLM Quantization

> [!tip] 核心洞察
> 激活离群值的危害可以通过静态展平转嫁到权重上，而权重的显著性分布恰可指导低秩误差重建集中在少数关键行，从而用一个量化后的低秩残差矩阵即可恢复精度，且无需在线变换或顺序分支。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | SERQ：面向LLM量化的显著性感知低秩误差重建 |
| 英文题名 | SERQ: Saliency-Aware Low-Rank Error Reconstruction for LLM Quantization |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=nFjj8NEBqv) · [GitHub](https://github.com/acalabys/SERQ) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | SERQ |
| Dataset | WikiText-2 (LLaMA-2 7B, W4A4), WikiText-2 (LLaMA-2 70B, W4A8), 0-shot Common Sense Reasoning (LLaMA-3 8B, W4A4) vs. 旋转方法 |

> [!tip] 效果简介
> - WikiText-2 (LLaMA-2 7B, W4A4) 上，PPL 为 5.97 (SERQ GPTQ)，对比 7.37 (L2QER)，变化 -1.40。
> - WikiText-2 (LLaMA-2 70B, W4A8) 上，PPL 为 3.43 (SERQ GPTQ)，对比 3.55 (L2QER)，变化 -0.12。
> - 0-shot Common Sense Reasoning (LLaMA-3 8B, W4A4) 上，平均准确率 (↑) 为 62.41 (SERQ GPTQ)，对比 55.44 (L2QER)，变化 +6.97。

## 概要

**核心问题：** 将大语言模型（LLM）权重量化至4位时，激活中存在的离群值会严重破坏低精度矩阵乘法的精度。现有低秩误差重建方法（如 **L2QER**，Zhang et al., NeurIPS 2024）虽然通过双因子分解补偿量化误差，但在W4A4极端低精度设置下精度退化严重，且依赖两个顺序低秩因子，导致推理时需要在线量化和多个窄矩阵乘法，无法实现纯4位高效矩阵乘。

**核心思路：** 本文提出 **SERQ**（Saliency-Aware Low-Rank Error Reconstruction），其关键洞察在于：激活离群值的危害可以通过静态展平转嫁到权重上，而权重的显著性分布恰可指导低秩误差重建集中在少数关键行，从而用一个量化后的低秩残差矩阵即可恢复精度，且无需在线变换或顺序分支。

**方法定位：** SERQ 属于训练无关（training-free）的W4A4量化方法，与基于矩阵分解的误差重建方法（LLM.int4()、L2QER）和基于旋转的分布展平方法（QuaRot、SpinQuant）形成对比。其核心创新在于将 **静态激活展平**、**显著性感知误差重建** 和 **离线权重置换** 三个模块整合为统一的纯4位推理路径，所有预处理均在离线阶段完成，推理时零额外延迟开销。

**主要结果：**
- 在WikiText-2困惑度上，SERQ（W4A4）在LLaMA-2 7B上达到5.97，显著优于L2QER（7.37）和QuaRot（6.15）。
- 在零样本常识推理和MMLU上，SERQ在LLaMA-3 8B W4A4下分别达到62.41和53.80，较L2QER提升约7个和15个百分点。
- 端到端GPU推理中，SERQ-MXFP4实现超过2倍的整体加速，峰值内存占用相对FP16降低约2.48倍。
- 消融实验表明，仅对显著行进行误差重建相较于覆盖全矩阵，在相同秩预算下可提升1–4%精度；方法对校准数据规模和领域鲁棒。

### 大规模语言模型部署的效率瓶颈

大规模语言模型（LLM）的推理成本已成为实际部署的核心约束。模型量化通过将浮点权重和激活映射到低位宽整数表示，能够显著压缩模型体积并加速推理。给定一个 $n$ 位量化方案，张量 $\pmb{X}$ 的量化过程可表述为：

$$\pmb{X}_q = \mathrm{clip}(\lceil \pmb{X} / \pmb{s} \rfloor), \quad \pmb{s} = \mathrm{max}(|\pmb{X}|) / (2^{n-1} - 1), \quad \hat{\pmb{X}} = \pmb{s} \cdot \pmb{X}_q$$

在此基础上，一个线性层的量化近似计算为：

$$\pmb{y} \approx \pmb{s}_W (\pmb{W}_q \pmb{X}_q) \pmb{s}_X$$

然而，当量化位宽降至4位时，精度退化问题变得极为严峻。**核心瓶颈**在于：权重和激活的联合4位量化（W4A4）会引入显著的量化误差，而现有方法在精度保持和推理效率之间难以兼顾。

### 现有方法的缺口

当前应对低比特量化的方法大致分为三条技术路线，但各自存在关键缺陷：

**矩阵分解方法**以 **LLM.int4()**（Dettmers et al., NeurIPS 2022）和 **L2QER**（Zhang et al., NeurIPS 2024）为代表。LLM.int4() 采用混合精度方案，为离群值和常规值分配不同的计算路径（INT8 与 FP16），这导致推理时存在异构计算开销。L2QER 则通过对量化误差矩阵进行低秩分解来补偿精度损失：

$$\hat{\pmb{W}} = \mathrm{Q}(\pmb{W}) + \pmb{L}_1 \pmb{L}_2, \quad \pmb{L}_1 \pmb{L}_2 \approx \pmb{W} - \mathrm{Q}(\pmb{W})$$

这一方法在 W4A8 设置下表现尚可，但**在 W4A4 设置下精度严重退化**。更关键的是，双因子结构 $\pmb{L}_1\pmb{L}_2$ 引入了两个顺序低秩分支，推理时需要在线量化和多个窄矩阵乘法，无法实现纯4位高效矩阵乘。

**分布展平方法**以 **SmoothQuant**（Xiao et al., ICML 2024）、**QuaRot**（Ashkboos et al., 2024）和 **SpinQuant**（Liu et al., 2025）为代表。SmoothQuant 通过将激活离群值迁移到权重侧来平滑分布，但需要在线计算缩放因子。QuaRot 和 SpinQuant 分别采用随机 Hadamard 旋转和学习旋转矩阵来均匀化激活分布，但旋转操作本身引入了在线变换开销，且校准过程复杂。

**权重量化优化方法**以 **GPTQ**（Frantar et al., ICML 2023）为代表，专注于逐层权重最优量化，但未系统解决激活离群值问题。

### 本文动机与核心洞察

上述方法暴露了一个共同的结构性矛盾：**精度恢复所需的补偿计算与纯低位推理的效率目标之间存在根本冲突**。双因子低秩重建需要在线量化和顺序乘法，旋转方法需要运行时变换，混合精度方法则需要维护多条计算路径。

SERQ 的核心洞察在于将这一矛盾转化为可离线解决的设计问题：**激活离群值的危害可以通过静态展平转嫁到权重上，而权重的显著性分布恰可指导低秩误差重建集中在少数关键行**。具体而言，通过 SmoothQuant 式的静态激活展平，将激活缩放因子离线融入权重矩阵，消除在线变换需求；随后，利用激活显著性识别最关键的权重行，仅对这些显著行的量化误差进行低秩重建，并使用单个量化后的低秩矩阵 $\pmb{R}$ 同时补偿激活离群值与权重显著性的量化误差。这一设计使得推理时仅需一个纯4位残差分支，无需在线变换或顺序计算。

SERQ 在三个维度上区别于现有工作：（1）用**单个低秩矩阵**替代双因子结构，消除在线量化步骤；（2）将**显著性感知**引入误差重建，使有限的秩预算集中于关键行；（3）通过**离线权重置换**将行列重排传播至相邻层，完全消除推理时的动态重排序开销。这些设计使得 SERQ 能够在 W4A4 和 W4A8 设置下，以极低的延迟开销实现与 FP16 基线接近的精度。

## 核心方法与创新机理

SERQ 的核心创新在于将**激活离群值抑制**与**权重显著性引导的低秩误差重建**统一到一个纯4位推理路径中，从根本上消除了现有低秩分解方法在 W4A4 场景下的精度退化与推理延迟瓶颈。

### 从双因子到单低秩残差：消除在线量化与顺序计算

现有低秩误差重建方法（如 **L2QER**，Zhang et al., NeurIPS 2024）通过对量化误差矩阵做 SVD 分解，得到两个低秩因子 $L_1 L_2$，并将其加回量化权重：

$$
\hat{\pmb{W}} = \mathrm{Q}(\pmb{W}) + \pmb{L}_1 \pmb{L}_2
$$

这一设计的根本缺陷在于：两个因子中至少一个必须保持较高精度，导致推理时需要对中间结果进行**在线量化**，且残差路径形成**顺序分支**，无法实现端到端的纯4位矩阵乘。在 W4A4 设置下，这一结构带来的精度退化尤为严重——LLaMA-3 8B 的 MMLU 准确率从 FP16 的 62.6 骤降至 38.33（Table 1）。

SERQ 的解决方案是将误差重建压缩为**单个量化后的低秩矩阵 $R$**，仅作用于最显著的权重行：

$$
\pmb{R} = \widetilde{\pmb{W}}_s - \mathrm{Q}(\widetilde{\pmb{W}}_s)
$$

推理时的线性层计算变为：

$$
\mathrm{Q}(\widehat{\pmb{X}}) \cdot \mathrm{Q}(\widehat{\pmb{W}}) \approx \widehat{\pmb{X}}_q \cdot \widehat{\pmb{W}}_q + \widetilde{\pmb{X}}_{s,q} \cdot \mathrm{Q}(\pmb{R})
$$

其中主路径与残差路径**均使用4位精度**，无需任何在线量化或精度转换。这一结构将 L2QER 的顺序双分支替换为可并行的单残差路径，每层延迟开销降至约 18.7%，远低于旋转类方法（Table 2）。

### 激活离群值的静态转嫁：将分布展平融入权重

激活离群值是 W4A4 量化的核心障碍。旋转类方法（**QuaRot**、**SpinQuant**）通过在线 Hadamard 变换或学习旋转矩阵来展平激活分布，但这引入了推理时的额外矩阵乘和重排序开销。

SERQ 采用**静态激活展平**（Static Activation Flattening），借鉴 SmoothQuant（Xiao et al., ICML 2024）的思想，通过逐通道缩放因子将激活离群值抑制到权重侧：

$$
\pmb{Y} = \pmb{X} \pmb{W} = (\pmb{X} \cdot \mathrm{diag}(\pmb{s}^{-1})) (\mathrm{diag}(\pmb{s}) \cdot \pmb{W}) = \widetilde{\pmb{X}} \widetilde{\pmb{W}}
$$

关键差异在于：缩放因子 $\pmb{s}$ 被**离线融入权重矩阵** $\widetilde{\pmb{W}}$，并进一步传播至相邻层，推理时完全无需在线展平或动态重排。这一设计使得 SERQ 在消除激活离群值的同时，实现了零额外延迟开销。

### 显著性感知的误差分配：用秩预算换取关键行精度

激活展平后的权重矩阵 $\widetilde{\pmb{W}}$ 中，缩放因子大的行对应原始激活的离群通道，其量化误差对输出的影响远大于普通行。SERQ 利用这一性质，按显著性对权重行进行排序：

$$
\widehat{\pmb{W}} = \pmb{P} \cdot \mathrm{diag}(\pmb{s}) \cdot \pmb{W} = [\widetilde{\pmb{W}}_s ; \widetilde{\pmb{W}}_r]
$$

仅对显著行 $\widetilde{\pmb{W}}_s$ 提取量化残差 $R$，而非对全矩阵做低秩分解。消融实验（Figure 4）表明，在相同秩预算下，仅覆盖显著行的误差重建相比覆盖全矩阵可实现 1-4% 的精度提升。这意味着 SERQ 用更少的秩预算达到了更高的精度——秩预算被集中分配到真正关键的权重区域。

### 离线置换传播：消除推理时重排序

显著性排序需要对权重行进行置换，但直接置换会破坏激活通道的顺序对齐。SERQ 通过在相邻层之间**传播列置换**来解决这一问题：当前层的行置换 $P$ 同时作为前一层的列置换，使得所有线性层的权重矩阵在离线阶段完成重排，推理时激活通道自然对齐，无需任何在线重排序操作。

### 创新总结

SERQ 相对于基线的关键变化可归纳为四个维度：

| 设计维度 | 基线方案 | SERQ 方案 |
|---------|---------|----------|
| 误差重建结构 | 双低秩因子，需在线量化 | 单低秩矩阵 $R$，纯4位路径 |
| 激活离群值处理 | 在线旋转或混合精度 | 离线静态展平，融入权重 |
| 推理路径 | 顺序低秩分支 | 单残差路径，仅作用于显著通道 |
| 权重置换 | 无或推理时动态重排 | 离线行列置换，传播至相邻层 |

这些创新共同实现了 SERQ 的核心承诺：在 W4A4 设置下，以单个量化低秩矩阵同时补偿激活离群值与权重显著性的量化误差，且所有展平与置换操作均在离线完成，推理时无额外延迟。端到端 GPU 实测中，SERQ-MXFP4 实现超过 2 倍的整体加速，峰值内存占用相对 FP16 降低约 2.48 倍（Table 3）。

SERQ 的整体流程围绕一个核心设计原则展开：**将激活离群值的危害通过静态展平转嫁到权重侧，再利用权重显著性分布指导低秩误差重建，最终用一个量化后的单残差矩阵恢复精度，且所有变换均在离线完成**。该框架包含三个顺序执行的模块，分别解决激活分布不均、量化误差补偿以及推理时重排开销三个瓶颈。

### Pipeline 总览

1. **Static Activation Flattening（静态激活展平）**  
   离线计算逐通道的平滑缩放因子 $s$，将激活的离群值幅度抑制并迁移到权重矩阵中。缩放因子直接融入权重参数，使推理时无需任何在线变换。该步骤借鉴 **SmoothQuant**（Xiao et al., ICML 2024）的思想，但将其完全离线化。

2. **Saliency-Aware Error Reconstruction（显著性感知误差重建）**  
   展平后的权重矩阵 $\widetilde{W}$ 按行显著性排序，仅提取最显著的 $r$ 行的量化误差构成单个低秩残差矩阵 $R$。$R$ 本身也被量化（INT4 或 MXFP4），从而形成一条纯 4 位精度的残差补偿路径。这与 **L2QER**（Zhang et al., NeurIPS 2024）使用两个低秩因子且需在线量化中间结果的方式截然不同。

3. **Offline Weight Permutation（离线权重置换）**  
   根据显著性顺序对权重行进行重排，并通过列置换将排列信息传播至前一层权重，确保激活通道顺序自然对齐。所有置换均在离线阶段完成，推理时完全消除动态重排序开销。

### 模块关系与数据流

三个模块的衔接关系如下：

- **输入**：原始 FP16 权重 $W$ 与少量校准数据。
- **Step 1 → Step 2**：SAF 输出的展平权重 $\widetilde{W}$ 直接作为显著性排序和误差重建的输入。激活缩放因子 $s$ 的大小天然反映了各行的显著性，因此无需额外计算显著性指标。
- **Step 2 → Step 3**：显著性排序确定的行置换矩阵 $P$ 同时应用于权重和残差矩阵，确保残差路径与主路径的通道对应关系一致。
- **推理时**：主路径执行量化后的矩阵乘 $Q(\widehat{X}) \cdot Q(\widehat{W})$，残差路径仅在显著通道上计算 $Q(\widetilde{X}_s) \cdot Q(R)$，两条路径结果相加得到最终输出。整个计算链路均为 4 位精度，无混合精度分支。

### 关键设计决策

| 设计维度 | 传统做法 | SERQ 选择 |
|---------|---------|----------|
| 激活离群值处理 | 在线旋转（QuaRot/SpinQuant）或混合精度路径（LLM.int4()） | 离线静态展平融入权重 |
| 误差重建结构 | 双低秩因子 $L_1 L_2$，需在线量化 | 单低秩矩阵 $R$，预量化 |
| 推理路径 | 顺序低秩分支带来额外延迟 | 单残差路径仅作用于显著行 |
| 权重置换 | 无或推理时动态重排 | 离线行列置换并传播至相邻层 |

这一框架使得 SERQ 在 W4A4 设置下首次实现了与旋转方法相当甚至更优的精度，同时将每层延迟开销控制在约 18.7%，显著低于双因子重建方案。

### 基础量化与线性层

SERQ 的量化基础采用最大缩放整数量化。对于任意浮点张量 $\pmb{X}$，其 $n$ 位整数量化形式为：

$$\pmb{X}_q = \mathrm{clip}(\lceil \pmb{X} / \pmb{s} \rfloor), \quad \pmb{s} = \mathrm{max}(|\pmb{X}|) / (2^{n-1} - 1), \quad \hat{\pmb{X}} = \pmb{s} \cdot \pmb{X}_q$$

其中 $\pmb{s}$ 为缩放因子，由张量绝对值的最大值与目标位宽共同决定。当权重和激活均被量化时，线性层的近似计算为：

$$\pmb{y} \approx \pmb{s}_W (\pmb{W}_q \pmb{X}_q) \pmb{s}_X$$

### 模块一：静态激活展平 (Static Activation Flattening)

激活离群值是低精度量化的核心瓶颈。SERQ 借鉴 SmoothQuant 的思路，将激活分布的展平操作完全离线化。通过引入逐通道缩放因子 $\pmb{s}$，将激活的离群值抑制转嫁到权重侧：

$$\pmb{Y} = \pmb{X} \pmb{W} = (\pmb{X} \cdot \mathrm{diag}(\pmb{s}^{-1})) (\mathrm{diag}(\pmb{s}) \cdot \pmb{W}) = \widetilde{\pmb{X}} \widetilde{\pmb{W}}$$

缩放因子 $\mathrm{diag}(\pmb{s})$ 被直接融入权重矩阵 $\widetilde{\pmb{W}}$ 中，并在相邻层间传播合并，推理时零额外开销。这一步骤同时揭示了权重行的显著性——缩放因子越大的通道，其对应的权重行对输出贡献越大。

### 模块二：显著性感知误差重建 (Saliency-Aware Error Reconstruction)

传统低秩误差重建方法（如 L2QER）对量化误差矩阵 $\pmb{W} - \mathrm{Q}(\pmb{W})$ 做 SVD 分解，用两个低秩因子 $\pmb{L}_1 \pmb{L}_2$ 进行补偿：

$$\hat{\pmb{W}} = \mathrm{Q}(\pmb{W}) + \pmb{L}_1 \pmb{L}_2, \quad \pmb{L}_1 \pmb{L}_2 \approx \pmb{W} - \mathrm{Q}(\pmb{W})$$

但该方案需要在线量化中间结果，且双因子带来顺序计算开销。SERQ 的核心创新在于：仅对最显著的权重行进行误差重建，并使用单个低秩矩阵。

具体而言，经静态展平后的权重矩阵 $\widetilde{\pmb{W}}$ 按行显著性排序并置换，分割为显著行 $\widetilde{\pmb{W}}_s$ 和其余行 $\widetilde{\pmb{W}}_r$：

$$\widehat{\pmb{W}} = \pmb{P} \cdot \mathrm{diag}(\pmb{s}) \cdot \pmb{W} = [\widetilde{\pmb{W}}_s ; \widetilde{\pmb{W}}_r]$$

仅提取显著行的量化残差构成单低秩矩阵 $\pmb{R}$：

$$\pmb{R} = \widetilde{\pmb{W}}_s - \mathrm{Q}(\widetilde{\pmb{W}}_s)$$

$\pmb{R}$ 自身也被量化，从而形成纯低精度的残差分支。推理时的计算为：

$$\mathrm{Q}(\widehat{\pmb{X}}) \cdot \mathrm{Q}(\widehat{\pmb{W}}) \approx \widehat{\pmb{X}}_q \cdot \widehat{\pmb{W}}_q + \widetilde{\pmb{X}}_{s,q} \cdot \mathrm{Q}(\pmb{R})$$

主路径使用量化后的权重-激活矩阵乘，附加路径仅在显著通道上乘以量化后的残差 $\mathrm{Q}(\pmb{R})$，全程无需在线量化或混合精度切换。

### 模块三：离线权重置换 (Offline Weight Permutation)

为使显著行在推理时自然对齐，SERQ 在离线阶段完成行列置换。权重行按显著性重排，对应的列置换传播至前一层（如下投影层的行置换传播至上一层门控/上投影层的列），确保激活通道顺序与置换后的权重行匹配。所有线性层均避免推理时的动态重排序，完全消除在线开销。

## 实验与关键发现

### 核心瓶颈验证：SERQ 为何能在 W4A4 下显著优于双因子误差重建

现有低秩误差重建方法的根本瓶颈在于其双因子结构（$\mathbf{L}_1\mathbf{L}_2$）在 W4A4 设置下精度严重退化。以 **L2QER**（Zhang et al., NeurIPS 2024）为例，该方法对量化误差矩阵进行 SVD 分解后，需在推理时对中间结果执行在线量化，并引入两个顺序窄矩阵乘法，导致无法实现纯 4 位高效矩阵乘。SERQ 通过将激活显著性融入权重矩阵，仅对最显著的权重行提取量化误差构成**单个低秩矩阵 $\mathbf{R}$**，并将 $\mathbf{R}$ 本身也量化（Eq. 7），从而在残差路径上实现与主路径一致的纯 4 位计算。

这一结构性差异在 W4A4 设置下产生了决定性精度差距。**Table 1** 显示，在 LLaMA-2 7B 上，SERQ (GPTQ) 的 WikiText-2 困惑度仅为 5.97，而 L2QER 高达 7.37（差距 -1.40）；在 LLaMA-3 8B 上，SERQ 的 0-shot 常识推理平均准确率达到 62.41，L2QER 仅为 55.44（差距 +6.97），MMLU 准确率差距更达 +15.47（53.80 vs 38.33）。即使在 W4A8 的较宽松设置下，SERQ 在 LLaMA-2 70B 上仍以 3.43 的困惑度优于 L2QER 的 3.55。这些结果表明，双因子结构在极低位宽下的精度退化并非模型规模或校准数据的次要效应，而是结构性的瓶颈。

![[assets/figures/papers/paper_list_l37_https_openreview_net_forum_id_nFjj8NEBqv/figures/003_Table_1.jpg]]
*Table 1: Comparison with matrix decomposition methods. We compare perplexity scores, average zero-shot common sense reasoning accuracy, and average MMLU accuracy. Results under different precision settings are obtained by modifying their publicly released codebase (See Appendix A.7)*

### 与旋转量化方法的精度-效率权衡

**Table 2** 将 SERQ 与当前 SOTA 的 W4A4 旋转量化方法 **QuaRot**（Ashkboos et al., 2024）和 **SpinQuant**（Liu et al., 2025）进行了系统对比。在 LLaMA-2 7B 上，SERQ (GPTQ) 以 5.97 的困惑度优于 QuaRot 的 6.15 和 SpinQuant 的 6.0，同时在 0-shot 和 MMLU 准确率上均保持优势。更关键的是效率维度：SERQ 的每层延迟开销仅为 18.7%，低于旋转方法的额外开销。这一优势源于 SERQ 将所有展平与置换操作完全离线处理——缩放因子融入相邻层权重，行列置换在标定阶段预计算并传播至前一层（Figure 2b），推理时无需任何在线重排序或在线量化。

**Table 9**（附录）进一步揭示了校准效率的显著差异：SERQ 的标定时间远低于需要学习旋转矩阵的 SpinQuant，同时保持精度优势。这一结果确立了 SERQ 作为训练无关 W4A4 方案中精度-效率 Pareto 前沿的地位。

### 端到端 GPU 推理：2 倍加速与 2.48 倍内存压缩

**Table 3** 报告了 LLaMA-3 8B 在 2k 输入序列长度下的端到端 GPU 推理性能。SERQ-MXFP4 在所有批次大小（1/8/16/32）下均实现超过 2 倍的 TTFT（Time to First Token）加速，峰值内存占用相对 FP16 基线降低最多 2.48 倍。值得注意的是，在 batch size=1 的极小批量下，SERQ-MXFP4 的 TPOT（Time per Output Token）略高于纯 MXFP4 方案，这是单残差路径在极低计算密度场景下的固有开销，但总体加速比仍保持在 2.09 倍。

**Figure 3** 的 GPU 延迟分析进一步表明，SERQ 的残差路径在较大行尺寸矩阵上尤为高效——这是因为单矩阵乘法相比双因子的顺序窄矩阵乘更好地利用了 GPU 的并行计算能力。SERQ 的延迟开销比 L2QER 的 LoRA 路径降低最多 4.5 倍，这在附录 **Table 10** 的线性层延迟测量中得到了定量验证。

![[assets/figures/papers/paper_list_l37_https_openreview_net_forum_id_nFjj8NEBqv/figures/009_Figure_3.jpg]]
*Figure 3: GPU performance comparison. We report latency overhead analysis across various matrix sizes (batch size is 1 and token length is 4k). SERQ is particularly effective for larger row-sized matrices. (See Appendix A.6)*

### 消融实验：秩、校准数据与静态激活展平

**秩大小的影响（Table 4）**：增大低秩矩阵的秩 $r$ 可单调降低困惑度，但提升在 $r \geq 128$ 后趋于饱和。这一饱和现象验证了 SERQ 的核心假设——量化误差主要集中在少数显著行上，过度增加秩预算对非显著行的重建边际收益递减。

![[assets/figures/papers/paper_list_l37_https_openreview_net_forum_id_nFjj8NEBqv/figures/011_Table_4.jpg]]
*Table 4: Effect of rank size on perplexity*

**显著性感知重建的有效性（Figure 4）**：仅对最显著的权重行进行误差重建，相较于将相同秩预算均匀覆盖全矩阵，可实现 1-4% 的精度提升。这一消融直接证明了“将低秩预算集中于显著行”策略的有效性，而非低秩分解本身带来的增益。

![[assets/figures/papers/paper_list_l37_https_openreview_net_forum_id_nFjj8NEBqv/figures/015_Figure_4.jpg]]
*Figure 4: The trade-off between loss from rank reduction and the coverage of error reconstruction. The figure shows that higher accuracy is achieved by reconstructing errors for salient rows with smaller ranks, rather than covering a larger portion of the weight matrix*

**校准数据的鲁棒性（Table 5）**：SERQ 对校准数据集的大小（512/128/32 样本）和领域（WikiText/Pile）表现出高度鲁棒性，困惑度变化极小。这表明显著性行的识别主要依赖于激活分布的统计特性，而非特定领域的语义内容。

**静态激活展平（SAF）的贡献（Table 7）**：在小模型上，SAF 的效果尤为显著——Qwen-2.5 3B 在 W4A4 设置下，SAF 将困惑度从 10.83 降至 9.57。这是因为小模型的激活离群值相对更集中，展平操作将离群值的危害从激活侧转嫁到权重侧后，显著行的误差重建能更有效地补偿精度损失。

![[assets/figures/papers/paper_list_l37_https_openreview_net_forum_id_nFjj8NEBqv/figures/014_Table_7.jpg]]
*Table 7: Effect of static activation flattening (SAF) on perplexity*

### 生成任务评估

**Table 6** 展示了 SERQ 在 GSM8K（数学推理）和 LongBench（长文本理解）上的生成质量。在 W4A8 和 W4A4 设置下，SERQ 全面超过 L2QER 与 LLM.int4()，且 W4A8 下的表现已接近 FP16 基线。这验证了 SERQ 的精度恢复不仅限于困惑度指标，在需要连贯推理和长程依赖的下游任务中同样有效。

### 量化信号质量分析

**Table 8** 的 QSNR（Quantization Signal-to-Noise Ratio）对比显示，SERQ 的显著性感知重建相比传统 SVD 分解获得了更高的信噪比。这从信号保真度角度解释了 SERQ 精度优势的物理根源——通过将重建预算集中在信息密度最高的权重行上，SERQ 在相同秩约束下保留了更多对模型输出有决定性影响的信息。

![[assets/figures/papers/paper_list_l37_https_openreview_net_forum_id_nFjj8NEBqv/figures/016_Table_8.jpg]]
*Table 8: Comparison of Quantization Signal-to-Noise Ratio (QSNR) between SERQ and SVD*

### 已知局限

1. **极小批量下的 TPOT 开销**：Table 3 显示 batch size=1 时 SERQ-MXFP4 的 TPOT 略高于纯 MXFP4，单残差路径在极低计算密度下的延迟优势有限。
2. **领域偏移鲁棒性未验证**：显著性行的确定依赖于校准数据集的激活统计，极端领域偏移下显著性分布可能发生变化，该场景的鲁棒性在文中未讨论。
3. **非线形层适用性**：当前方法聚焦于线性层的量化误差重建，对注意力机制中 softmax 等非线性算子的推广尚未探索。

## 定位与知识库关联

### 1. 与低秩误差重建方法的继承与突破

SERQ 的直接技术前驱是 **L2QER**（Zhang et al., NeurIPS 2024），后者率先将量化误差的低秩分解引入LLM压缩。L2QER 通过SVD提取双低秩因子 $\mathbf{L}_1\mathbf{L}_2$ 来补偿量化损失，其核心瓶颈在于：双因子结构要求推理时对中间结果进行在线量化，且两个窄矩阵乘法构成顺序依赖，无法实现纯4位矩阵乘。在W4A4设置下，该方法的精度退化尤为严重——例如LLaMA-2 7B的困惑度从FP16的5.47飙升至7.37。

SERQ 的突破点在于将“双因子顺序补偿”重构为“单矩阵显著性补偿”。具体而言：
- **结构简化**：仅使用一个低秩矩阵 $\mathbf{R}$ 直接补偿显著行的量化误差，消除了在线量化环节，使残差路径与主路径统一为纯4位计算。
- **补偿聚焦**：不再对全矩阵误差做无差别低秩近似，而是依据激活显著性仅重建最关键权重行的误差。消融实验（Figure 4）表明，在相同秩预算下，仅覆盖显著行比覆盖全矩阵可获得1-4%的精度提升。

这一设计使SERQ在W4A4下将LLaMA-2 7B的困惑度从L2QER的7.37压至5.97，同时将每层延迟开销降低至约18.7%，而L2QER的双分支路径在同等设置下延迟开销显著更高。

### 2. 与混合精度分解方法的对比

**LLM.int4()**（Dettmers et al., NeurIPS 2022）是混合精度矩阵分解的代表性基线，其将离群值通道分配至FP16路径，非离群值通道使用INT4。该方案的问题在于双精度路径导致硬件利用率不均，且有效位宽高于纯4位。

SERQ 通过静态激活展平（SAF）将离群值抑制到权重侧，再以量化后的单低秩残差统一补偿，从而在纯4位路径上实现更高精度。Table 1显示，SERQ在所有W4A4和W4A8配置下的困惑度和零样本推理精度均系统性地优于LLM.int4()，同时有效位宽更低。

### 3. 与分布展平/旋转方法的对比

SERQ 的静态激活展平模块继承自 **SmoothQuant**（Xiao et al., ICML 2024）的逐通道缩放思想，但关键差异在于：SmoothQuant 的缩放因子需在推理时在线应用，而SERQ将其离线融入权重矩阵，并进一步通过行列置换传播至相邻层，完全消除运行时开销。

与基于旋转的W4A4方法相比：
- **QuaRot**（Ashkboos et al., 2024）使用随机Hadamard旋转矩阵展平激活分布，但旋转操作本身在推理时引入额外矩阵乘。
- **SpinQuant**（Liu et al., 2025）通过学习旋转矩阵提升精度，但校准成本显著增加。

Table 2的对比表明，SERQ在LLaMA-2 7B上以5.97的困惑度优于QuaRot（6.15）和SpinQuant（6.0），且每层延迟开销（18.7%）低于旋转方法的在线变换成本。Table 9进一步显示SERQ的校准时间远低于SpinQuant等学习式旋转方法。

### 4. 与权重量化优化器的兼容性

SERQ 本身不限定权重量化算法，与 **GPTQ**（Frantar et al., ICML 2023）完全兼容。实验中使用GPTQ作为权重优化器时，SERQ的精度进一步提升（例如LLaMA-3 8B W4A4零样本准确率从RTN的62.41提至GPTQ的更高值）。这种兼容性使SERQ可受益于未来权重量化算法的进步。

### 5. 适用边界与局限

**适用场景**：
- SERQ 专为线性层的权重-激活量化设计，覆盖LLM中占主导计算量的前馈网络和投影层。
- 在W4A4和W4A8配置下均有效，尤其适合大矩阵行维度场景（Figure 3显示SERQ对较大行尺寸的矩阵加速效果更显著）。
- 端到端GPU推理中，SERQ-MXFP4在LLaMA-3 8B上实现超过2倍的整体加速，峰值内存占用相对FP16降低约2.48倍（Table 3）。

**已知局限**：
- 在极小批量（batch size=1）下，TPOT（每输出token时间）可能略高于纯MXFP4方案，因残差路径的额外计算在单样本时无法被有效摊销。
- 方法依赖校准数据集确定显著性行，极端领域偏移下的鲁棒性未经系统验证。Table 5表明SERQ在Wiki和Pile校准数据间困惑度变化很小，但更剧烈的分布偏移（如代码到自然语言）的影响尚不明确。

### 6. 开放问题

1. **算子泛化性**：SERQ当前仅应用于线性层，是否可直接推广至注意力机制中的QKV投影或注意力分数计算，仍需验证。
2. **更大规模模型**：实验覆盖至LLaMA-2 70B，但在超大规模模型（>70B）或多模态LLM中，单低秩残差路径的秩预算是否足够，以及显著性行识别策略是否需要调整，尚无定论。
3. **训练后量化的极限**：SERQ在W4A4下已接近FP16基线的生成质量（Table 6中GSM8K和LongBench结果），但进一步提升至W3A3或更低精度时，仅靠低秩误差重建是否仍有效，仍需探索。

## 原文 PDF

![[paperPDFs/ICLR_2026/SERQ_Saliency_Aware_Low_Rank_Error_Reconstruction_for_LLM_Quantization.pdf]]
