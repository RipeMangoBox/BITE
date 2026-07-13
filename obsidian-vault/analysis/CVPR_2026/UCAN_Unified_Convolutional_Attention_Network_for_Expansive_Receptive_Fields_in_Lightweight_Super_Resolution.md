---
title: "UCAN: Unified Convolutional Attention Network for Expansive Receptive Fields in Lightweight Super-Resolution"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/UCAN_Unified_Convolutional_Attention_Network_for_Expansive_Receptive_Fields_in_Lightweight_Super_Resolution.pdf
project_link: null
code_link: "https://github.com/hokiyoshi/UCAN"
aliases:
- UUCAN
- UCAN
tags:
- CVPR_2026
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/representation_learning
core_operator: 通过Hedgehog特征图提升线性注意力的特征秩以突破秩瓶颈，同时采用Flash Attention实现高效大窗口注意力，并利用半共享参数架构与蒸馏大核卷积降低计算开销。
primary_logic: 使用可学习的对称指数对特征映射（Hedgehog Feature Map），以低秩线性时间重建softmax注意力的高秩和判别性，同时配合Flash Attention和蒸馏大核卷积，在轻量模型中实现广泛有效感受野。
claims:
- Hedgehog特征图将线性注意力的输出矩阵秩恢复至46，远超ReLU和ELU+1的基线
- 在Manga109（×4）上，UCAN相对于MambaIRV2提升0.26 dB PSNR，同时参数减少11%
- Set5 上 PSNR/SSIM (×2) = 38.34 / 0.9618 (UCAN)
- Urban100 上 PSNR/SSIM (×2) = 33.22 / 0.9379 (UCAN)
---

# UCAN: Unified Convolutional Attention Network for Expansive Receptive Fields in Lightweight Super-Resolution

> [!tip] 核心洞察
> 使用可学习的对称指数对特征映射（Hedgehog Feature Map），以低秩线性时间重建softmax注意力的高秩和判别性，同时配合Flash Attention和蒸馏大核卷积，在轻量模型中实现广泛有效感受野。

| 字段 | 内容 |
|------|------|
| 中文题名 | UCAN：面向轻量超分辨率的统一卷积注意力网络 |
| 英文题名 | UCAN: Unified Convolutional Attention Network for Expansive Receptive Fields in Lightweight Super-Resolution |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.11680) · [Code](https://github.com/hokiyoshi/UCAN) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/representation_learning |
| Method | UCAN (Unified Convolutional Attention Network) |
| Dataset | Set5, Urban100, Manga109, BSDS100 |

> [!tip] 效果简介
> - Set5 上，PSNR/SSIM (×2) 38.34 / 0.9618 (UCAN) vs 38.22 / 0.9613 (OmniSR) (+0.12 dB)。
> - Urban100 上，PSNR/SSIM (×2) 33.22 / 0.9379 (UCAN) vs 33.05 / 0.9363 (OmniSR) (+0.17 dB)。
> - Manga109 上，PSNR (×4) 31.63 (UCAN-L) vs 31.24 (MambaIRV2-light) (+0.39 dB)。

## 概要

轻量级图像超分辨率（SR）在移动设备和边缘计算场景中需求迫切，但现有方法在扩大感受野时面临**计算成本与特征多样性的根本矛盾**：标准线性注意力因特征图秩崩塌导致表征能力不足，而大窗口注意力计算量过高，难以在资源受限条件下实现高保真重建。

针对这一瓶颈，本文提出 **UCAN（Unified Convolutional Attention Network）**，通过三个关键机制实现突破：

1. **Hedgehog 特征图（HFM）**：采用可学习的对称指数对映射，将线性注意力的输出矩阵秩从 ReLU/ELU+1 的极低水平恢复至 **46**，以 $O(N)$ 线性复杂度逼近 softmax 注意力的高秩判别性。
2. **Flash Attention 大窗口注意力**：在 32×32 窗口内使用 Flash Attention 实现精确注意力计算，大幅降低内存占用与延迟。
3. **半共享混合注意力与蒸馏大核卷积**：Sharing Block 与 Receiving Block 共享注意力成分以压缩计算量，同时通过通道分离的蒸馏式大核模块高效保留高频结构。

实验表明，UCAN 在多个基准上以更少参数取得领先性能：在 **Manga109（×4）** 上，UCAN-L 达到 **31.63 dB** PSNR，仅需 48.4G MACs；在 **Urban100（×2）** 上达到 **33.22 dB**，较 OmniSR 提升 0.17 dB。消融实验证实，移除 HPA 模块导致 Urban100 性能下降 0.32 dB，验证了大窗口注意力的关键作用。

该方法为轻量 SR 提供了一条“低秩线性时间 + 高秩判别性”的新路径，但尚未在视频 SR、复杂退化及极端资源设备上验证其泛化能力。

图像超分辨率（SR）旨在从低分辨率输入重建高保真高分辨率图像，是底层视觉领域的基础任务。近年来，基于深度学习的SR方法取得了显著进展，但在资源受限设备（如移动端、IoT终端）上的部署仍面临严峻挑战：模型必须在极低的参数量和计算量约束下，同时保持足够的表征能力以恢复高频细节。

**核心矛盾：感受野扩展与计算效率的冲突。** 现有轻量SR方法在扩大有效感受野（ERF）时，普遍陷入两难困境。一方面，标准Softmax注意力机制具备强大的全局建模能力，但其计算复杂度为 $O(N^2)$，难以直接应用于高分辨率特征图。另一方面，线性注意力通过特征映射 $\phi$ 将复杂度降至 $O(N)$，成为轻量模型的自然选择：

$$o_i^{\mathrm{L}} = \frac{\phi(\pmb{q}_i)^\top \big(\sum_{j} \phi(\pmb{k}_j) \pmb{v}_j^\top\big)}{\phi(\pmb{q}_i)^\top \big(\sum_{j} \phi(\pmb{k}_j)\big)}$$

然而，现有线性注意力方法使用ReLU或ELU+1等简单特征映射，存在严重的**秩崩塌（rank collapse）**问题——输出矩阵的秩远低于理论满秩，导致特征多样性不足、判别能力下降。如Figure 2所示，ReLU和ELU+1特征映射的输出秩显著偏低，而UCAN采用的Hedgehog特征映射将秩恢复至46，远超基线方法。此外，Figure 7进一步揭示了线性注意力缺乏归一化机制导致的注意力分数幅度异常问题。

**现有方法的局限性。** 当前轻量SR方法可大致分为三类：CNN方法（如**ESC**）计算高效但感受野受限；Transformer方法（如**SwinIR-light**）通过窗口注意力平衡效率与性能，但窗口大小固定，难以捕获长程依赖；状态空间模型（如**MambaIRV2-light**）虽在长序列建模上展现潜力，但在复杂纹理重建上的ERF覆盖仍不充分（见Figure 5的ERF可视化对比）。这些方法均未从根本上解决秩崩塌与大窗口注意力计算开销之间的矛盾。

**本文动机。** 针对上述瓶颈，UCAN提出了一种统一卷积注意力网络，核心思路是双管齐下：在全局建模层面，引入可学习的**Hedgehog特征映射**以突破线性注意力的秩瓶颈，在 $O(N)$ 复杂度下逼近Softmax注意力的高秩判别性；在局部建模层面，采用**Flash Attention**实现高效的大窗口（32×32）精确注意力计算，配合**蒸馏式大核卷积**以可控成本扩展空间感受野。通过半共享注意力架构进一步压缩跨层计算冗余，UCAN在轻量参数预算内实现了广泛的有效感受野和高保真重建能力。

## 核心方法与创新机理

UCAN 的核心创新在于通过**四个关键设计槽位**的协同替换，系统性地解决了轻量超分辨率模型在扩大感受野时面临的“计算成本-特征多样性”矛盾。这些创新并非孤立存在，而是围绕一个统一的因果链条：提升线性注意力的特征秩、降低大窗口注意力的实现成本、压缩跨层注意力的冗余计算、以及用蒸馏策略保留高频结构。

### 因果瓶颈与调控旋钮

现有轻量 SR 方法在扩展感受野时陷入两难：标准线性注意力（如 ReLU 或 ELU+1 特征映射）因**输出矩阵秩崩塌**导致表征判别力不足，无法有效捕捉长距离依赖；而大窗口 softmax 注意力虽然保秩能力强，但 $O(N^2)$ 的计算复杂度使其在资源受限设备上不可行。UCAN 的调控旋钮是**用 Hedgehog 特征图提升线性注意力的特征秩以突破秩瓶颈**，同时**采用 Flash Attention 实现高效大窗口注意力**，并**通过半共享参数架构与蒸馏大核卷积降低整体计算开销**。

### 四个关键槽位创新

**槽位一：线性注意力的特征图 — 从 ReLU/ELU+1 到 Hedgehog Feature Map**

线性注意力通过特征映射 $\phi$ 将复杂度从 $O(N^2)$ 降至 $O(N)$，但其表征质量高度依赖 $\phi$ 的输出矩阵秩。ReLU 和 ELU+1 映射产生的特征矩阵秩严重不足，导致注意力分数分布退化（Figure 7 显示 ReLU 和 ELU+1 的线性注意力存在高幅度伪影，缺乏归一化）。UCAN 引入 **Hedgehog Feature Map (HFM)**，其形式为 $m$ 对可学习的对称指数特征：

$$\phi_{\mathrm{H}}(\boldsymbol{X}) = [\exp(\boldsymbol{W}^{\top}\boldsymbol{X} + b_1), \dots, \exp(\boldsymbol{W}^{\top}\boldsymbol{X} + b_m), \exp(-\boldsymbol{W}^{\top}\boldsymbol{X} - b_1), \dots, \exp(-\boldsymbol{W}^{\top}\boldsymbol{X} - b_m)]$$

其中 $\boldsymbol{W}$ 为共享投影矩阵，$b_i$ 为可学习偏置。这一设计的核心优势在于：对称指数对天然形成互补模式，使得输出矩阵的列空间更加丰富。实验证据显示（Figure 2），在 $N=256$、$d=48$ 的设置下，Hedgehog 注意力将输出矩阵秩恢复至 **46**，远超 ReLU 和 ELU+1 的基线水平，接近满秩 64。同时，Figure 8 的排序一致性分析表明 Hedgehog 在注意力分数排序上与标准 softmax 注意力的一致性显著优于 Symmetric ReLU 等替代方案。

**槽位二：大窗口注意力实现 — 从标准 Softmax 注意力到 Flash Attention**

大窗口（32×32）注意力能提供更广泛的局部上下文，但标准 softmax 注意力的 $O(N^2)$ 内存开销使其在轻量模型中不可行。UCAN 采用 **Flash Attention** 实现精确的大窗口注意力计算，在保持数学等价性的前提下将内存占用降至 $O(N)$ 级别，执行速度显著提升。Table 2 的延迟对比显示，Flash Attention 相比 Naive Self-Attention 在参数量不变的情况下大幅降低了推理延迟，使得 32×32 大窗口注意力能够实际部署于轻量模型。

**槽位三：跨层注意力计算 — 从独立计算到半共享机制**

传统设计中每层注意力独立计算 Q、K、V 并生成注意力图，存在大量冗余。UCAN 提出 **半共享机制**（Semi-Sharing Mechanism）：在 Broad Effective Receptive Field Group (BERFG) 中，Sharing Block 通过 Shared Hybrid Attention (SHA) 计算完整的注意力分量（注意力图 $A_{map}$ 和查询-键成分 $A_{qk}$），而 Receiving Block 的 Received Hybrid Attention (RHA) 直接复用这些分量：

$$F_{2,a+1}, A_{map}^{(a)}, A_{qk}^{(a)} = f_{SHA}^{(a)}(F_{2,a})$$

$$F_{2,a+1}' = f_{RHA}^{(a)}(F_{2,a}', A_{map}^{(a)}, A_{qk}^{(a)})$$

这一设计使得 Receiving Block 无需重新计算注意力图，在保持表征质量的同时显著降低计算量。消融实验（Table 3）间接验证了该机制的有效性：混合块深度从 3 降至 1 时，Urban100 PSNR 从 33.05 dB 降至 32.71 dB（−0.34 dB），说明多层半共享结构对性能有实质贡献。

**槽位四：大核卷积设计 — 从标准大核卷积到蒸馏式大核模块**

大核卷积能有效扩大感受野并保留高频结构，但直接使用会带来沉重计算负担。UCAN 的 **Large Kernel Distillation (LKD)** 模块采用通道分离策略：将特征通道分为细粒度子集 $F_{fg}$（$C_{fg}=\max(C/4,16)$）和粗粒度子集 $F_{cg}$，仅对细粒度通道执行三支特征提取——大核空间分支（使用扩张卷积和深度可分离卷积）、通道分支和小核局部分支，粗粒度通道则通过恒等映射保留。这种“蒸馏”设计使得大核卷积的计算成本集中在信息最丰富的少数通道上，在保持高频结构保真度的同时大幅降低开销。消融实验（Table 5）显示，LKD 内核尺寸从 5 增大到 65 时，Urban100 PSNR 从 33.12 dB 提升至 33.19 dB（+0.07 dB），验证了大核带来的感受野增益；而移除 LKD 模块（Table 3）导致 Urban100 PSNR 从 33.22 dB 降至 32.90 dB（−0.32 dB），证明该模块对整体性能不可或缺。

### 创新的协同效应

四个槽位创新形成闭环：Hedgehog 特征图保证线性注意力的全局建模质量，Flash Attention 使大窗口局部注意力在轻量约束下可行，半共享机制压缩跨层冗余计算，蒸馏大核卷积以低成本保留高频细节。这一协同设计使得 UCAN 在 Manga109（×4）上以比 MambaIRV2 少 11% 的参数实现 0.26 dB PSNR 提升，在 Urban100（×2）上以 33.22 dB 超越 OmniSR 的 33.05 dB，验证了创新组合的有效性。

UCAN 的整体管线遵循“浅层特征提取 → 核心编码器 → 重建”的标准超分辨率范式，其关键创新在于核心编码器中同时整合了**大窗口空间注意力**、**Hedgehog 线性全局注意力**和**蒸馏式大核卷积**，从而在轻量参数预算下获得广泛的有效感受野。

### 输入到浅层特征

低分辨率输入图像 $I_{LR}$ 首先通过一个 $3 \times 3$ 卷积映射为浅层特征嵌入 $F_0$（Shallow Feature Extractor）。这一步与大多数轻量 SR 方法一致，负责将 RGB 图像转换为高维特征空间。

### 核心编码器：Broad Effective Receptive Field Group (BERFG)

浅层特征 $F_0$ 随后进入 **Broad Effective Receptive Field Group (BERFG)**，这是 UCAN 的核心编码器。BERFG 采用**双块配对架构**，由 Sharing Block (SB) 和 Receiving Block (RB) 交替堆叠构成：

1. **Sharing Block (SB)**：接收前一层的特征，通过 Shared Hybrid Attention (SHA) 模块计算窗口多头自注意力，并输出三样东西——增强后的特征 $F_{2,a+1}$、共享注意力图 $A_{map}^{(a)}$ 和共享查询-键成分 $A_{qk}^{(a)}$：
   $$F_{2,a+1}, A_{map}^{(a)}, A_{qk}^{(a)} = f_{SHA}^{(a)}(F_{2,a})$$

2. **Receiving Block (RB)**：接收 Sharing Block 输出的共享注意力分量，直接复用以计算自身的 Received Hybrid Attention (RHA)，避免重复计算：
   $$F_{2,a+1}' = f_{RHA}^{(a)}(F_{2,a}', A_{map}^{(a)}, A_{qk}^{(a)})$$

这种**半共享机制**是 UCAN 实现轻量化的关键策略——SB 承担完整的注意力计算开销，RB 则通过复用中间结果大幅降低计算量，同时保持特征质量。

### 核心模块构成

BERFG 内部的每个 Hybrid Attention 模块由以下关键组件构成：

- **High Performance Attention (HPA)**：包含 ConvMLP 和 Flash Attention 大窗口注意力。ConvMLP 先提取局部上下文 $\mathcal{F}_{mlp}$，随后 Flash Attention 在 $32 \times 32$ 大窗口上执行精确注意力计算，以 $O(N)$ 级内存开销替代标准注意力的 $O(N^2)$：
  $$\mathcal{F}_{mlp} = f_{\mathrm{ConvMLP}}(f_{\mathrm{LN}}(\boldsymbol{X})), \quad \mathcal{F}_1 = f_{\mathrm{FWA}}(f_{\mathrm{LN}}(\boldsymbol{F}_{mlp}))$$

- **Hedgehog Attention**：采用可学习的对称指数对特征映射（Hedgehog Feature Map, HFM），将线性注意力的输出矩阵秩恢复至 46（远超 ReLU 和 ELU+1 基线的低秩表现），从而缓解线性注意力的秩崩塌问题，在 $O(N)$ 复杂度下逼近 softmax 注意力的判别性：
  $$\phi_{\mathrm{H}}(\boldsymbol{X}) = [\exp(\boldsymbol{W}^\top \boldsymbol{X} + b_1), \dots, \exp(\boldsymbol{W}^\top \boldsymbol{X} + b_m), \exp(-\boldsymbol{W}^\top \boldsymbol{X} - b_1), \dots, \exp(-\boldsymbol{W}^\top \boldsymbol{X} - b_m)]$$

- **Large Kernel Distillation (LKD)**：采用通道分离策略，将特征通道划分为细粒度子集 $F_{fg}$（$C_{fg} = \max(C/4, 16)$）和粗粒度子集 $F_{cg}$，仅对细粒度通道执行三支特征提取（大核空间分支、通道分支、小核局部分支），以蒸馏方式保留高频结构信息，避免大核卷积对全部通道施加的沉重计算负担。

### 重建模块

BERFG 输出的深层特征经过一个重建模块，由 $3 \times 3$ 卷积和 Pixel Shuffle 上采样组成，将特征映射回 RGB 空间，得到最终的高分辨率输出 $I_{SR}$。

### 整体数据流总结

$$I_{LR} \xrightarrow{3\times3 \text{ Conv}} F_0 \xrightarrow{\text{BERFG (SB/RB pairs)}} F_{deep} \xrightarrow{\text{Conv + Pixel Shuffle}} I_{SR}$$

BERFG 内部，Sharing Block 和 Receiving Block 交替执行，前者通过 HPA（ConvMLP + Flash Attention 大窗口）和 Hedgehog Attention 捕获局部纹理与全局长程依赖，后者通过半共享机制复用注意力分量降低开销；LKD 模块则进一步蒸馏大核卷积的高频保持能力。三者协同，使 UCAN 在轻量参数预算下获得广泛的有效感受野（图 5 的 ERF 可视化证实了这一点）。

![[assets/figures/papers/paper_list_l948_https_arxiv_org_abs_2603_11680/figures/003_Figure_3.jpg]]
*Figure 3: Detailed architecture of (a) Shared and Received Hybrid Attention (SHA and RHA) and (b) Large Kernel Distillation (LKD). LKD contains a Triple Feature Extraction block with three branches, which are the Large Kernel Spatial Branch, the Channel Branch, and the Small Kernel Spatial Branch. SHA and RHA employ Shared and Received Window Multi Head Self Attention (Shared WMHSA and Received WMHSA) to capture local information, and include a Shared Dual Fusion Layer (SDFL) and a Dual Fusion Receiver Layer (DFRL) to aggregate global context. The Dual Fusion Layer comprises two sub branches, which are Hedgehog Attention*

### 线性注意力的秩瓶颈与Hedgehog特征图

标准Softmax注意力通过指数归一化获得高秩判别性，但计算复杂度为$O(N^2)$，难以用于大窗口高分辨率特征。线性注意力通过特征映射$\phi$将复杂度降至$O(N)$：

$$o_i^{\mathrm{L}} = \frac{\phi(\pmb{q}_i)^\top \big(\sum_{j} \phi(\pmb{k}_j) \pmb{v}_j^\top\big)}{\phi(\pmb{q}_i)^\top \big(\sum_{j} \phi(\pmb{k}_j)\big)}$$

然而，常用特征映射（如ReLU、ELU+1）会导致注意力输出矩阵秩严重崩塌，表征多样性不足。图2的实验证据表明，ReLU和ELU+1下的线性注意力输出矩阵秩远低于满秩64，而**Hedgehog Feature Map（HFM）**可将秩恢复至46，显著缓解秩瓶颈。

HFM通过可学习的对称指数对构造特征映射：

$$\phi_{\mathrm{H}}(\boldsymbol{X}) = [\exp(\boldsymbol{W}^\top \boldsymbol{X} + b_1), \dots, \exp(\boldsymbol{W}^\top \boldsymbol{X} + b_m), \exp(-\boldsymbol{W}^\top \boldsymbol{X} - b_1), \dots, \exp(-\boldsymbol{W}^\top \boldsymbol{X} - b_m)]$$

其中$\boldsymbol{W}$为共享投影矩阵，$b_1,\dots,b_m$为可学习偏置，$m$为特征对数量。对称指数对的设计使得正负方向的特征同时被激活，从而在低秩线性时间内重建softmax注意力的高秩判别性。

---

### 高表现力注意力模块（HPA）

HPA模块解决大窗口注意力的计算效率问题。其结构为ConvMLP与Flash Attention的级联：

$$\mathcal{F}_{mlp} = f_{\mathrm{ConvMLP}}(f_{\mathrm{LN}}(\boldsymbol{X})), \quad \mathcal{F}_1 = f_{\mathrm{FWA}}(f_{\mathrm{LN}}(\boldsymbol{F}_{mlp}))$$

- **ConvMLP**：先通过LayerNorm归一化，再经卷积MLP提取局部上下文。
- **Flash Window Attention（FWA）**：在32×32大窗口上执行精确注意力计算，利用Flash Attention将内存占用降至$O(N)$级别，避免标准自注意力的$O(N^2)$内存瓶颈。Table 2显示，Flash Attention相比朴素自注意力在延迟和参数量上均有显著优势。

---

### 半共享混合注意力机制（SHA/RHA）

为降低跨层注意力计算开销，UCAN在Broad Effective Receptive Field Group（BERFG）中引入半共享机制。BERFG由**Sharing Block（SB）**和**Receiving Block（RB）**成对构成。

**共享混合注意力（SHA）**输出特征及两个共享注意力分量：

$$F_{2,a+1}, A_{map}^{(a)}, A_{qk}^{(a)} = f_{SHA}^{(a)}(F_{2,a})$$

**接收混合注意力（RHA）**复用SHA产出的注意力图$A_{map}$和查询-键成分$A_{qk}$，仅重新计算值投影与融合：

$$F_{2,a+1}' = f_{RHA}^{(a)}(F_{2,a}', A_{map}^{(a)}, A_{qk}^{(a)})$$

SHA内部包含Shared Window Multi Head Attention和Shared Dual Fusion Layer；RHA对应包含Received WMHA和Dual Fusion Receiver Layer（Fig. 3a）。QKV投影将通道维度减半（$C/2$），空间分支输出结合HFM线性注意力与深度可分离卷积：

$$\pmb{F_{sb}} = \phi(\pmb{Q}) ((\phi(\pmb{K})^T \pmb{V}) + \pmb{W_d} \pmb{V})$$

其中$\phi$为Hedgehog特征映射，$\pmb{W_d}$为深度卷积权重。

---

### 蒸馏式大核模块（LKD）

大核卷积能有效扩大感受野，但标准实现计算量高。LKD通过**通道分离+三支特征提取**实现轻量化：

- **通道分离**：将特征通道分为细粒度子集$F_{fg}$（$C_{fg}=\max(C/4, 16)$）和粗粒度子集$F_{cg}$，仅对细粒度通道执行昂贵的大核操作。
- **三支并行提取**（Fig. 3b）：
  1. **大核空间分支**：利用扩张卷积和深度可分离分解高效扩大感受野。
  2. **通道分支**：捕获通道间依赖。
  3. **小核局部分支**：保留细粒度局部纹理。

三支输出融合后与粗粒度通道拼接，在保持高频结构的同时大幅降低计算开销。消融实验（Table 5）显示，LKD核尺寸从5增至65时Urban100 PSNR从33.12 dB提升至33.19 dB（+0.07 dB），验证了大核感受野的收益。

![[assets/figures/papers/paper_list_l948_https_arxiv_org_abs_2603_11680/figures/010_Figure_7.jpg]]
*Figure 7: Visualization of attention maps for Linear Attention using ReLU and ELU + 1 (computed with sequence length*

## 实验与关键发现

### 主实验结果

UCAN 在五个标准基准上与轻量级超分辨率方法进行全面对比，包括 CNN 类（**ESC**）、Transformer 类（**SwinIR-light**、**OmniSR**）和状态空间模型类（**MambaIRV2-light**）。Table 1 和 Table 6 汇总了定量结果。

![[assets/figures/papers/paper_list_l948_https_arxiv_org_abs_2603_11680/figures/005_Table_1.jpg]]
*Table 1: Quantitative comparison on lightweight image super-resolution with state-of-the-art methods. The best and second-best results are shown in bold and underlined, respectively*

在 ×2 放大尺度上，UCAN 在 Set5 上达到 38.34 dB PSNR，超越 OmniSR 的 38.22 dB（+0.12 dB）；在 Urban100 上达到 33.22 dB，超越 OmniSR 的 33.05 dB（+0.17 dB）。在 ×4 放大尺度上，UCAN 在 BSDS100 上达到 27.79 dB，超越 SwinIR-light 的 27.69 dB（+0.10 dB）；在 Set14 上达到 34.27 dB，超越 PFT-light 的 34.19 dB（+0.08 dB）。

UCAN-L 变体在 Manga109（×4）上达到 31.63 dB PSNR，相比 MambaIRV2-light 提升 0.39 dB，同时参数减少 11%（见 Abstract 和 Section 1）。UCAN-L 在五个基准中的四个上超越 ESC，参数量却少 7%。Figure 1 展示了 Manga109（×4）上 PSNR 与参数量的权衡关系：UCAN（红色菱形）位于 Pareto 前沿的右上角，以更低参数量实现更高 PSNR，显著区别于 CNN（绿色三角）、Transformer（黄色方块）和 SSM（蓝色圆点）方法簇。

![[assets/figures/papers/paper_list_l948_https_arxiv_org_abs_2603_11680/figures/001_Figure_1.jpg]]
*Figure 1: Performance comparison of PSNR versus model parameters on the Manga109 (×4) dataset. Our method is evaluated alongside state-of-the-art super-resolution approaches. Green triangles represent CNN-based methods, yellow squares denote Transformerbased methods, blue circles indicate SSM-based methods, and red diamonds show our proposed approach*

视觉效果方面，Figure 4 和 Figure 9-18 显示 UCAN 在 Urban100、Set5、Set14、BSDS100 和 Manga109 上恢复了更精细的纹理和结构细节。

![[assets/figures/papers/paper_list_l948_https_arxiv_org_abs_2603_11680/figures/004_Figure_4.jpg]]
*Figure 4: Visual comparison between ground truth and different methods on Urban100*

### 消融实验

**核心模块消融**（Table 3）：在 DIV2K 上训练 400K 迭代，测试于 Set5 和 Urban100（×2）。移除 High Performance Attention（HPA）后，Urban100 PSNR 从 33.22 dB 降至 32.90 dB（−0.32 dB），验证了大窗口 Flash Attention 对感受野扩展的关键作用。移除 Dual Fusion Layer（DFL）和 Large Kernel Distillation（LKD）同样导致性能下降，证实了通道融合与高频结构保持模块的必要性。

**结构超参数消融**（Table 5）：混合块（Hybrid Block）深度从 3 降至 1 时，Urban100 PSNR 从 33.05 dB 降至 32.71 dB（−0.34 dB），表明多级半共享注意力堆叠对特征质量至关重要。LKD 内核尺寸从 5 增大到 65 时，Urban100 PSNR 从 33.12 dB 提升至 33.19 dB（+0.07 dB），验证了蒸馏大核模块通过增大有效感受野带来的增益。

**注意力机制效率**（Table 2）：对比朴素自注意力、Flash Attention 和 Dual Fusion Layer 的延迟与参数量。Flash Attention 在 32×32 大窗口下实现精确注意力计算，同时显著降低内存占用和推理延迟。

### 秩分析与感受野验证

Figure 2 揭示了 Hedgehog Feature Map（HFM）的核心机理：在 N=256、d=48、满秩 64 的设置下，ReLU 和 ELU+1 特征图的输出矩阵秩严重崩塌，而 HFM 将秩恢复至 46，远超其他方法。Figure 7 进一步显示 ReLU 和 ELU+1 因缺乏归一化而产生高幅度伪影，HFM 则避免了此问题。Figure 8 的排序一致性分析表明，Hedgehog 特征图在注意力分数排序上最接近标准 Softmax 注意力，优于对称 ReLU 等替代方案。

Figure 5 的有效感受野（ERF）可视化显示，UCAN 相比 MambaIR 和 MambaIRv2 拥有更广泛、更均匀的 ERF 分布。Figure 6 的局部归因图（LAM）对比进一步证实 UCAN 在 ×4 尺度下能利用更广范围的输入像素进行重建。

### 局限性与失效模式

尽管整体参数量低，Hedgehog 特征图引入的额外 MLP 在极低资源 MCU 或 IoT 设备上可能仍构成负担。当前实验仅在双三次下采样退化下进行，未验证对噪声、模糊等复杂退化的鲁棒性。此外，Hedgehog 注意力在视频超分辨率、动态场景或更高放大倍数（×8）上的有效性尚未探索。上述结论需在实际部署中进一步验证。

![[assets/figures/papers/paper_list_l948_https_arxiv_org_abs_2603_11680/figures/008_Table_3.jpg]]
*Table 3: Ablation study. We train all models on DIV2K for 400K iterations, and test on Set5 and Urban100 (×2). The final result is shown in the last row*

## 定位与知识库关联

### 1. 方法定位与谱系

UCAN 处于**轻量图像超分辨率（Lightweight SR）** 的交叉地带，其设计同时吸收了卷积网络（CNN）、视觉Transformer（ViT）和状态空间模型（SSM）三条技术路线的思想，并针对资源受限场景进行了系统性重构。

**与CNN轻量SR的关系**：UCAN继承了CNN在局部特征提取上的高效性，体现在浅层特征提取器（3×3卷积）和蒸馏式大核模块（LKD）上。LKD通过通道分离与三支特征提取（大核空间分支、通道分支、小核局部分支），在控制计算量的前提下扩张感受野，这一定位与**ESC**等高效CNN方法形成直接竞争——UCAN-L在参数量少7%的情况下，在五个基准数据集中的四个上超越ESC。

**与Transformer轻量SR的关系**：UCAN的核心创新在于对线性注意力机制的秩瓶颈突破。标准线性注意力因特征图秩崩塌导致表征能力不足，而大窗口Softmax注意力计算量过高。UCAN引入**Hedgehog Feature Map（HFM）**——一种可学习的对称指数对特征映射——将线性注意力的输出矩阵秩恢复至46，远超ReLU和ELU+1基线。这与**SwinIR-light**和**OmniSR**等基于窗口注意力的轻量Transformer形成差异化：前者依赖标准Softmax注意力或网格注意力，UCAN则以线性时间复杂度的Hedgehog注意力实现全局信息建模。

**与SSM轻量SR的关系**：UCAN在有效感受野（ERF）上直接对标**MambaIRV2-light**等状态空间模型方法。Figure 5的ERF可视化表明，UCAN的注意力机制比MambaIR系列具有更广泛的空间覆盖。定量上，UCAN在Manga109（×4）上相对于MambaIRV2提升0.26 dB PSNR，同时参数减少11%。

### 2. 核心机制的知识贡献

UCAN的知识增量集中在三个相互耦合的机制上：

- **Hedgehog注意力与秩恢复**：线性注意力的根本缺陷在于特征映射后的矩阵秩坍缩，导致注意力分数缺乏判别性。HFM通过拼接$m$对对称指数特征$[\exp(\boldsymbol{W}^\top \boldsymbol{X} + b_i), \exp(-\boldsymbol{W}^\top \boldsymbol{X} - b_i)]$，在保持$O(N)$复杂度的前提下，将输出秩从ReLU的不足10提升至46（Figure 2）。这一发现为线性注意力在低层视觉任务中的应用提供了理论依据。

- **Flash Attention大窗口聚合**：为弥补线性注意力在局部精细建模上的不足，UCAN在HPA模块中采用Flash Attention实现32×32大窗口的精确Softmax注意力计算，以$O(N)$级内存开销替代标准实现的$O(N^2)$。Table 2显示，Flash Attention相比Naive Self-Attention在延迟和参数量上均有显著优势。

- **半共享混合注意力架构**：BERFG中的Sharing Block计算完整的注意力图$A_{map}$和查询-键成分$A_{qk}$，Receiving Block直接复用这些分量，仅执行轻量的Received WMHA和Dual Fusion Receiver Layer。这种半共享机制在保持表征能力的同时大幅降低跨层冗余计算。

### 3. 适用边界与局限

**已知适用场景**：
- 常规双三次下采样退化下的×2/×3/×4超分辨率重建
- 资源受限设备（参数量约1M量级，MACs约50G级别）
- 需要广泛有效感受野的纹理恢复任务（如Urban100中的规则纹理、Manga109中的线条结构）

**明确局限**（论文已指出）：
1. **退化鲁棒性未验证**：训练与测试均在双三次下采样退化下进行，对噪声、模糊、压缩伪影等复杂退化的泛化能力未知。
2. **高倍放大未探索**：未验证在×8等更高放大倍数下的有效性。
3. **动态场景未覆盖**：Hedgehog注意力在视频超分辨率或动态场景中的表现尚未评估。
4. **极低资源部署风险**：尽管整体参数量低，HFM引入的额外MLP投影在MCU或IoT级别的微控制器上可能仍构成计算负担。

### 4. 开放问题

1. **跨任务泛化**：Hedgehog特征图的秩恢复机制能否推广到其他基于Transformer的低层视觉任务（如去雾、去雨、去模糊）？其有效性是否依赖于超分辨率特有的高频重建需求？

2. **半共享机制的压缩极限**：当前共享$A_{map}$和$A_{qk}$两个分量，是否可进一步压缩为仅共享QK而独立计算注意力图？压缩对性能的边际影响如何？

3. **自适应窗口策略**：Flash Attention的32×32大窗口与Hedgehog注意力的全局建模如何根据输入分辨率或内容复杂度自适应调整？是否存在最优的窗口拆分策略？

4. **推理效率优化**：蒸馏大核卷积（LKD）与结构重参数化技术的结合能否进一步降低推理延迟？Table 5中LKD内核尺寸从5增至65仅带来0.07 dB提升，表明大核收益递减，更高效的卷积设计值得探索。

5. **HFM的理论分析**：HFM恢复秩的机制目前以实验验证为主（Figure 2, Figure 8的排序一致性分析），缺乏严格的理论界——$m$的取值与输出秩之间的定量关系、对称指数对的最优数量等问题仍待形式化分析。

## 原文 PDF

![[paperPDFs/CVPR_2026/UCAN_Unified_Convolutional_Attention_Network_for_Expansive_Receptive_Fields_in_Lightweight_Super_Resolution.pdf]]
