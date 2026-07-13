---
title: Efficient Unrolled Networks for Large-Scale 3D Inverse Problems
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Efficient_Unrolled_Networks_for_Large_Scale_3D_Inverse_Problems.pdf
project_link: null
code_link: null
aliases:
- EUNDPNOA
- EUNLS3IP
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 通过域分割将全量问题在训练时分解为小尺寸随机补丁，使得展开网络可以在每个子问题上局部处理；同时利用对角‑循环矩阵乘积近似正则算子AᵀA，通过FFT快速计算数据一致性更新，从而将内存与计算约束降至可承受范围。
primary_logic: 线性前向算子的线性性质允许人为将信号空间正交分解为感兴趣的补丁与已知的上下文，进而将全局逆问题转化为多个补丁级子问题；结合用对角掩膜与傅里叶域调制对正则算子的低秩结构逼近，可以在不牺牲端到端展开训练优势的前提下支持任意大规模三维重建。
claims:
- Fig. 1 展示网络步骤内存消耗远高于数据一致性步骤，成为大规模三维展开的瓶颈。
- 域分割策略允许展开网络在训练时只用小补丁，测试时通过两步（全局粗估+补丁细化）完成推理。
- 正则算子近似 H = diag(m) F⁻¹ diag(λ) F 能高效计算数据一致性更新，且参数可通过高斯随机向量拟合，无需问题相关数据。
- Walnut-CBCT (50 views) 上 PSNR (dB) = 34.21
---

# Efficient Unrolled Networks for Large-Scale 3D Inverse Problems

> [!tip] 核心洞察
> 线性前向算子的线性性质允许人为将信号空间正交分解为感兴趣的补丁与已知的上下文，进而将全局逆问题转化为多个补丁级子问题；结合用对角掩膜与傅里叶域调制对正则算子的低秩结构逼近，可以在不牺牲端到端展开训练优势的前提下支持任意大规模三维重建。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向大规模三维逆问题的高效展开网络 |
| 英文题名 | Efficient Unrolled Networks for Large-Scale 3D Inverse Problems |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2601.02141) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Efficient Unrolled Networks with Domain Partitioning and Normal Operator Approximation |
| Dataset | Walnut-CBCT, Calgary-Campinas MC-MRI |

> [!tip] 效果简介
> - Walnut-CBCT (50 views) 上，PSNR (dB) 34.21。
> - Calgary-Campinas MC-MRI (R=5) 上，PSNR (dB) 37.36。

## 概要

三维逆问题（如锥束CT重建和多线圈加速MRI）在医学成像中至关重要，其目标是从带噪线性测量 $\pmb{y} = \pmb{A} \pmb{x}^* + \pmb{\varepsilon}$ 中恢复未知信号 $\pmb{x}^*$。近年来，基于展开（unrolling）的端到端学习方法将物理模型与深度先验紧密结合，在各类成像任务中取得了领先的重建质量。然而，**标准展开网络在训练时需要对全局前向算子 $\pmb{A}$ 进行反向传播，其网络步骤（如3D DRUNet）的内存消耗随体积尺寸快速增长，远超数据一致性步骤**（见Figure 1），使得在单GPU上处理大规模三维问题（例如 $501^3$ 体素的CBCT）变得不可行。

本文针对这一瓶颈提出了两项互补技术，使得展开网络能够以单GPU资源高效训练并推理任意大规模三维重建任务：

1. **域分割（Domain Partitioning）**：利用线性前向算子的线性性质，将全量信号空间正交分解为感兴趣的补丁与已知的上下文，从而将全局逆问题转化为多个小尺寸补丁级子问题。训练时仅需随机提取的小尺寸补丁（如 $8 \times 384^2$），测试时通过“全量粗估 + 逐补丁细化”两步流程完成推理。
2. **正则算子近似（Normal Operator Approximation）**：将数据一致性步骤中出现的 $\pmb{A}^\top \pmb{A}$ 近似为对角‑循环矩阵乘积 $\pmb{H} = \mathrm{diag}(\pmb{m}) \pmb{F}^{-1} \mathrm{diag}(\pmb{\lambda}) \pmb{F}$，从而通过FFT快速计算梯度更新，避免显式存储和计算完整正则算子。

在方法谱系上，本文工作处于**端到端展开重建**与**即插即用（PnP）先验**的交汇点。与标准展开（在完整体积上训练3D DRUNet）相比，域分割将训练从不可行降至约44.7 GB显存，PSNR仅下降约0.38 dB；进一步结合正则算子近似，训练时间缩短约30%。与经典非学习方法（FDK、零填充RSS、TV最小化）和纯后处理/即插即用方法（2D/3D DRUNet后处理、PnP-αPGD、DPIR[RAM]）相比，所提方法在Walnut-CBCT（50视图）上达到34.21 dB PSNR，在Calgary-Campinas MC-MRI（加速倍率R=5）上达到37.36 dB PSNR，均取得最优或竞争性能（见Table 1和Table 2）。与基于隐式神经表示（INR）的逐样本优化方法相比，展开网络在推理时无需迭代优化，速度优势显著。

**核心结论**：通过域分割与正则算子近似的协同设计，展开网络首次在单GPU上实现了对 $501^3$ 级三维逆问题的端到端训练与推理，且性能与资源受限的标准展开相当或更优。该方法不依赖特定前向算子的坐标友好分解，适用于CBCT和MC-MRI等不同成像模态，展现了良好的通用性。



### 大规模三维逆问题与计算瓶颈

三维医学成像中广泛存在线性逆问题，其数学形式为

$$\pmb{y} = \pmb{A} \pmb{x}^* + \pmb{\varepsilon},$$

其中 $\pmb{A}$ 为线性前向算子（如锥束CT的X射线投影或并行MRI的多线圈傅里叶欠采样），$\pmb{x}^*$ 为未知的真实体积，$\pmb{\varepsilon}$ 为测量噪声。此类问题的标准求解路径是变分重建：

$$\hat{\pmb{x}} \in \arg\min_{\pmb{x}} d(\pmb{A x}, \pmb{y}) + \lambda g(\pmb{x}), \quad \lambda > 0,$$

其中 $d$ 为数据保真项，$g$ 为正则项。近年来，**展开网络**（unrolled networks）将上述优化过程展开为固定步数的迭代，用可学习的去噪先验 $\mathrm{D}_\phi$ 替代近端算子，形成端到端可训练的映射 $\mathrm{R}_\phi(\pmb{y}, \pmb{A})$。其一步更新为

$$\pmb{x}_{k+1} = \mathrm{D}_\phi\big(\pmb{x}_k - \eta \nabla_{\pmb{x}_k} d(\pmb{A x}_k, \pmb{y})\big), \quad \eta > 0,$$

训练损失为

$$\mathcal{L}_\mathrm{UNR}(\phi) = \mathbb{E}_{\pmb{x}^*, \pmb{y}} \parallel \mathrm{R}_\phi(\pmb{y}, \pmb{A}) - \pmb{x}^* \parallel_2^2.$$

然而，当问题规模上升到三维（如 $501^3$ 体素的CBCT或 $256\times218\times170$ 的多线圈MRI），标准展开网络的训练面临一个根本性瓶颈：**网络步骤（3D DRUNet）的内存消耗随体积尺寸快速增长，远超过数据一致性步骤**。Figure 1 明确展示了这一现象——网络步骤的峰值显存和执行时间在体积增大时急剧膨胀，而数据一致性步骤即使在高分辨率下仍可管理。这意味着，在单GPU上训练端到端展开网络处理大规模三维问题几乎不可行。

### 现有方法的缺口

现有三维重建方法各有局限：

- **经典非学习方法**（如CBCT的FDK算法、MC-MRI的零填充RSS重建）计算高效但重建质量不足。
- **变分方法**（如TV最小化配合FISTA）依赖手工设计的正则项，表达能力有限。
- **后处理网络**（如2D/3D DRUNet，Zhang et al., TPAMI 2022）仅对初始重建做单次映射，未充分利用前向算子的物理信息。
- **即插即用方法**（PnP-αPGD、DPIR[RAM]）将去噪器嵌入迭代框架，但每次迭代需完整评估前向/伴随算子，训练时仍需处理完整体积。
- **隐式神经表示**（INR，如instant-NGP，Müller et al., SIGGRAPH 2022）逐样本优化，推理耗时且无法利用大规模数据集的统计先验。

**核心缺口在于**：端到端展开网络虽然理论上能学习最优重建映射，但其训练内存需求使其无法直接应用于大规模三维问题。现有工作要么放弃端到端训练（转而使用后处理或PnP），要么限制在可承受的小规模问题上，缺乏一种能够将展开网络的表达能力扩展到任意大规模三维逆问题的通用策略。

### 本文动机与核心洞察

本文的核心洞察是：**线性前向算子的线性性质允许将信号空间正交分解为感兴趣的补丁与已知的上下文**。如 Figure 2 所示，即使前向算子 $\pmb{A}$ 以非平凡方式混合信号，仍可通过域分割将全量问题分解为两个正交子空间——固定上下文 $\pmb{x}_\mathrm{context}$ 后，仅需在较小的补丁 $\pmb{x}_\mathrm{patch}$ 上求解子问题。这一性质使得展开网络可以在训练时仅处理小尺寸随机补丁，从而将内存约束降至可承受范围。

同时，数据一致性步骤中的正则算子 $\pmb{A}^\top\pmb{A}$ 可通过**对角-循环矩阵乘积**高效逼近：

$$\pmb{A}^\top \pmb{A} \approx \mathrm{diag}(\pmb{m}) \pmb{F}^{-1} \mathrm{diag}(\pmb{\lambda}) \pmb{F},$$

其中 $\pmb{F}$ 为傅里叶变换，$\pmb{m}$ 为空间掩膜，$\pmb{\lambda}$ 为频域调制参数。该近似可通过高斯随机向量拟合，无需问题相关数据，且能借助FFT快速计算，进一步降低数据一致性更新的计算开销。

基于以上两条技术路线——**域分割**与**正则算子近似**——本文提出了一种通用框架，使得展开网络能够在不牺牲端到端训练优势的前提下，在单GPU上处理任意大规模三维重建问题，并在CBCT和MC-MRI两个代表性任务上验证其有效性。



## 核心方法与创新机理

### 瓶颈识别：网络步骤而非数据一致性步骤构成大规模三维展开的内存壁垒

标准展开网络在训练时需对全局前向算子进行反向传播，其内存消耗分布极不均衡。**Figure 1** 明确揭示了这一瓶颈：3D DRUNet 网络步骤的峰值显存和执行时间随体积尺寸快速增长，而数据一致性步骤即便在高分辨率下仍保持在可控范围。以 501³ 体素的 CBCT 重建为例，仅网络步骤的反向传播就已超出单 GPU 显存上限，使得端到端展开训练在物理上不可行。这一发现直接指向了本文的核心因果旋钮——**必须降低网络步骤所处理的信号维度，而非单纯优化数据一致性计算**。

### Changed Slot 1：域分割训练——将全局逆问题分解为补丁级子问题

本文的关键创新在于利用线性前向算子的线性性质，将信号空间正交分解为“感兴趣补丁”与“已知上下文”两部分。如 **Figure 2** 所示，对于任意线性算子 $\pmb{A}$，可将全量信号 $\pmb{x}^*$ 写作：

$$\pmb{x}^* = \pmb{S}^\top \pmb{x}_{\mathrm{patch}} + \pmb{S}_\perp^\top \pmb{x}_{\mathrm{context}}$$

其中 $\pmb{S}$ 为补丁提取矩阵。通过固定上下文 $\pmb{x}_{\mathrm{context}}$，原问题被转化为仅关于小尺寸 $\pmb{x}_{\mathrm{patch}}$ 的子问题，其有效前向算子变为 $\tilde{\pmb{A}} = \pmb{A}\pmb{S}^\top$，观测残差为 $\tilde{\pmb{y}} = \pmb{y} - \pmb{A}\pmb{S}_\perp^\top \pmb{x}_{\mathrm{context}}$。

**这一 changed slot 的直接效果**：训练时仅需对随机抽取的小尺寸立方体补丁（CBCT 为 8×384²，MC-MRI 为 8×128²）进行展开，而非完整体积（501³ 或 256×218×170）。消融实验（**Table 3**）表明，仅引入域分割即可将 CBCT 训练从“不可行”降至约 44.7 GB 显存，且 PSNR 仅比标准全量展开低约 0.38 dB，验证了该分解策略在保持重建质量的同时大幅降低资源需求。

### Changed Slot 2：正则算子 FFT 近似——用对角‑循环矩阵乘积加速数据一致性

数据一致性步骤的核心计算为 $\pmb{A}^\top\pmb{A}\pmb{x}$，即正则算子作用于当前估计。本文提出用结构化矩阵逼近这一算子：

$$\pmb{A}^\top\pmb{A} \approx H(\pmb{m}, \pmb{\lambda}) = \mathrm{diag}(\pmb{m}) \pmb{F}^{-1} \mathrm{diag}(\pmb{\lambda}) \pmb{F}$$

其中 $\pmb{m}$ 为空域掩膜，$\pmb{\lambda}$ 为傅里叶域调制系数。该形式的计算可通过 FFT 在 $\mathcal{O}(n\log n)$ 内完成，远低于精确矩阵乘法的 $\mathcal{O}(n^2)$。

**关键的实现细节**：参数 $\pmb{m}$ 和 $\pmb{\lambda}$ 的拟合不依赖任何问题相关数据，而是通过最小化 Frobenius 范数完成：

$$\mathscr{L}(\pmb{m}, \pmb{\lambda}) = \mathbb{E}_{\mathbf{x}\sim\mathcal{N}(0,I)} \| \pmb{A}^\top\pmb{A}\mathbf{x} - H(\pmb{m}, \pmb{\lambda})\mathbf{x} \|_2^2 = \| \pmb{A}^\top\pmb{A} - H(\pmb{m}, \pmb{\lambda}) \|_F^2$$

该损失等价于在高斯随机向量上评估近似误差，可在训练前一次性完成拟合。**Figure 9** 和 **Figure 10** 分别展示了 CBCT 和 MC-MRI 上近似算子与精确算子的对比，误差主要集中在高频区域，对重建质量的影响有限。

**组合效果**：同时使用域分割与正则算子近似（**Table 3**），在 Walnut-CBCT 上达到 34.15 dB PSNR，训练时间进一步缩短约 30%，且显存占用保持在单 GPU 可承受范围。值得注意的是，在 MC-MRI 上单独使用正则算子近似会略微降低性能（PSNR 35.12），但仍为第二优方案，说明该近似的适用性与前向算子的结构密切相关。

### Changed Slot 3：两步测试推理——从全局粗估到补丁细化

训练时的域分割策略需要配套的测试推理流程（**Algorithm 1**）。本文设计了两步过程：

1. **全量展开**：使用域分割训练的网络对完整体积进行初步重建，得到全局粗估计 $\tilde{\pmb{x}}$；
2. **逐补丁细化**：以 $\tilde{\pmb{x}}$ 为上下文，对每个补丁独立执行展开推理，最终通过加权融合聚合为最终重建。

这一设计解决了训练时仅见补丁、测试时需处理全量体积的“分布偏移”问题。对于 CBCT 这类前向算子高度混合的场景，细化步骤是必要的；而对于 MC-MRI，由于子问题本身已表现良好，细化带来的增益可忽略，这也暴露了该策略的**任务依赖性**——需要根据前向算子的混合程度判断是否需要第二步。

### 方法谱系与知识库定位

本文的方法创新处于**展开网络（unrolled networks）** 与**即插即用（Plug-and-Play）** 方法的交叉地带。与标准展开网络（如使用 3D DRUNet 的端到端 PGD 展开）相比，核心差异在于训练时的信号维度：标准展开要求全量体积参与反向传播，而本文通过域分割将训练限制在补丁级别。与 PnP-αPGD 和 DPIR[RAM] 等即插即用方法相比，本文保留了端到端训练的优势（可学习步长、共享先验参数），但通过算子近似避免了全量数据一致性步骤的高昂开销。与后处理方法（2D/3D DRUNet 直接映射）相比，本文通过展开迭代引入了前向算子的物理约束，在稀疏采集场景下具有显著优势。



本文提出了一套**可扩展的展开网络训练与推理框架**，旨在将端到端展开重建从中小规模问题推广到任意大规模三维逆问题。整个框架围绕两个核心机制构建：**域分割（Domain Partitioning）** 和 **正则算子近似（Normal Operator Approximation）**。二者协同工作，分别解决展开网络中“网络步骤”的内存爆炸瓶颈和“数据一致性步骤”在大规模下的计算效率问题。

### 问题形式化

框架处理的是线性逆问题的标准形式：

$$ \pmb{y} = \pmb{A} \pmb{x}^* + \pmb{\varepsilon} $$

其中 $\pmb{x}^* \in \mathbb{R}^n$ 为未知的真实信号，$\pmb{A} \in \mathbb{R}^{m \times n}$ 为已知的线性前向算子，$\pmb{y}$ 为含噪观测，$\pmb{\varepsilon}$ 为噪声。重建目标通过变分形式表达：

$$ \hat{\pmb{x}} \in \arg\min_{\pmb{x}} d(\pmb{A x}, \pmb{y}) + \lambda g(\pmb{x}), \ \lambda > 0 $$

### 展开PGD作为骨干架构

框架采用展开近端梯度下降（Unrolled PGD）作为基础迭代结构。每一迭代步执行数据一致性更新后接可学习的去噪先验：

$$ \pmb{x}_{k+1} = \mathrm{D}_\phi\big(\pmb{x}_k - \eta \nabla_{\pmb{x}_k} d(\pmb{A x}_k, \pmb{y})\big), \ \eta > 0 $$

其中 $\mathrm{D}_\phi$ 为参数化的去噪网络（本文使用2D/3D DRUNet，权重在所有迭代步间共享），$\eta$ 为步长。端到端训练损失为：

$$ \mathcal{L}_\mathrm{UNR}(\phi) = \mathbb{E}_{\pmb{x}^*, \pmb{y}} \parallel \mathrm{R}_\phi(\pmb{y}, \pmb{A}) - \pmb{x}^* \parallel_2^2 $$

### 核心瓶颈：网络步骤 vs. 数据一致性步骤

**Figure 1** 明确揭示了展开网络在大规模三维问题上的根本瓶颈：网络步骤（3D DRUNet）的峰值显存和执行时间随体积尺寸急剧增长，而数据一致性步骤（梯度下降）即使在高分辨率下仍可管理。以 $501^3$ 体素为例，仅网络步骤的反向传播就已超出单GPU显存容量，使得标准展开网络在CBCT等应用上完全不可行。

### 两模块协同的Pipeline

框架通过以下两个模块化解上述瓶颈：

**模块一：域分割训练与两步推理。** 利用线性前向算子的线性性质，将全量信号空间 $\mathbb{R}^n$ 正交分解为感兴趣的补丁子空间 $\mathbb{R}^p$ 和已知的上下文子空间 $\mathbb{R}^q$（$q = n - p$）。训练时，随机提取小尺寸补丁（如 $8 \times 384^2$ 用于CBCT，$8 \times 128^2$ 用于MC-MRI），将全局逆问题转化为多个补丁级子问题：

$$ \mathcal{L}_\mathrm{PART}(\phi) = \mathbb{E}_{\mathbf{S}} \mathbb{E}_{\pmb{x}^*, \pmb{y}} \parallel \mathrm{R}_\phi(\tilde{\pmb{y}}, \tilde{\pmb{A}}) - \mathbf{S}\pmb{x}^* \parallel_2^2 $$

其中 $\tilde{\pmb{A}} = \pmb{A} \pmb{S}^\top$，$\tilde{\pmb{y}} = \pmb{y} - \pmb{A} \pmb{S}_\perp^\top \pmb{x}_\mathrm{context}$。**Figure 2** 示意了这一分解原理。测试时采用两步流程（Algorithm 1）：先在全量体积上执行展开得到粗估计 $\tilde{\pmb{x}}$，再逐补丁细化并聚合。

![[assets/figures/papers/paper_list_l2056_https_arxiv_org_abs_2601_02141/figures/002_Figure_2.jpg]]
*Figure 2: Domain partitioning strategy: in case of a forward operator A that mixes the signal x in a non-trivial manner, we can still decompose the full domain*

**模块二：FFT加速的正则算子近似。** 数据一致性步骤中的梯度计算涉及 $\pmb{A}^\top\pmb{A}$，直接计算在大规模下同样昂贵。框架将其近似为对角‑循环矩阵乘积结构：

$$ \pmb{A}^\top \pmb{A} \approx \mathrm{diag}(\pmb{m}) \pmb{F}^{-1} \mathrm{diag}(\pmb{\lambda}) \pmb{F} $$

其中 $\pmb{m}$ 为空间掩膜，$\pmb{\lambda}$ 为傅里叶域调制参数，二者通过最小化Frobenius范数在随机高斯向量上拟合得到，无需问题相关数据：

$$ \mathscr{L}(m, \lambda) = \| \pmb{A}^\top\pmb{A} - H(m,\lambda) \|_F^2 $$

该近似使得数据一致性更新可通过FFT高效计算，且可直接嵌入补丁级运算中。

### 输入输出流

- **训练阶段**：输入为全量测量 $\pmb{y}$ 和真实信号 $\pmb{x}^*$，通过随机补丁提取和上下文补偿生成子问题 $(\tilde{\pmb{y}}, \tilde{\pmb{A}})$，送入展开网络进行端到端优化。梯度累积用于匹配有效批量大小。
- **推理阶段**：输入为测量 $\pmb{y}$ 和前向算子 $\pmb{A}$，经全量展开粗估后，逐补丁细化并融合输出最终重建 $\hat{\pmb{x}}$。

### 补充图表

![[assets/figures/papers/paper_list_l2056_https_arxiv_org_abs_2601_02141/figures/001_Figure_1.jpg]]
*Figure 1: Peak video memory complexity (dashed lines) and global execution times (dotted lines) of isolated components used in unrolling. We show the cost of evaluating and back-propagating through a standard 3D data consistency step (using gradient descent) and a standard 3D network step (using a 3D DRUNet [72]). We see here that the bottleneck lies in the network step, which grows rapidly with the volume size, while the data-consistency step remains manageable even at high resolutions*



### 问题形式化与展开PGD框架

本工作针对的**线性逆问题**具有统一形式：

$$\pmb{y} = \pmb{A} \pmb{x}^* + \pmb{\varepsilon} \tag{1}$$

其中 $\pmb{y}$ 为观测到的带噪测量，$\pmb{A}$ 为线性前向算子，$\pmb{x}^*$ 为未知真实信号，$\pmb{\varepsilon}$ 为加性噪声。对应的**变分重建目标**为：

$$\hat{\pmb{x}} \in \arg\min_{\pmb{x}} d(\pmb{A x}, \pmb{y}) + \lambda g(\pmb{x}), \ \lambda > 0 \tag{2}$$

其中 $d(\cdot,\cdot)$ 为数据保真项，$g(\cdot)$ 为正则项。

**展开近端梯度下降（Unrolled PGD）** 将迭代优化展开为固定步数的可学习网络。每一步用可学习去噪器 $\mathrm{D}_\phi$ 替代近端算子：

$$\pmb{x}_{k+1} = \mathrm{D}_\phi\big(\pmb{x}_k - \eta \nabla_{\pmb{x}_k} d(\pmb{A x}_k, \pmb{y})\big), \ \eta > 0 \tag{4}$$

端到端训练损失直接最小化重建结果与真实信号之间的 $\ell_2$ 距离：

$$\mathcal{L}_\mathrm{UNR}(\phi) = \mathbb{E}_{\pmb{x}^*, \pmb{y}} \parallel \mathrm{R}_\phi(\pmb{y}, \pmb{A}) - \pmb{x}^* \parallel_2^2 \tag{5}$$

### 瓶颈分析：网络步骤的内存爆炸

**Figure 1** 揭示了标准展开网络的致命瓶颈：**网络步骤（3D DRUNet）的显存消耗随体积尺寸急剧增长，远超数据一致性步骤**。在 $501^3$ 体素的 CBCT 场景下，仅网络步骤的反向传播就已超出单 GPU 显存上限，而数据一致性步骤即使在高分辨率下仍可管理。这意味着，若不解决网络步骤的内存问题，端到端展开训练在大规模三维问题上完全不可行。

### 核心模块一：域分割训练

域分割的核心思想是**利用线性前向算子的线性性质，将全局逆问题分解为多个补丁级子问题**。将全空间 $\mathbb{R}^n$ 正交分解为感兴趣的补丁空间 $\mathbb{R}^p$ 与已知的上下文空间 $\mathbb{R}^q$（$q = n-p$）：

$$\mathbb{R}^n = \mathbb{R}^p \oplus \mathbb{R}^q \quad \text{with } q = n-p \tag{10}$$

通过提取矩阵 $\pmb{S}$ 和 $\pmb{S}_\perp$ 分别提取补丁和上下文：

$$\pmb{x}^* = \pmb{S}^\top \pmb{x}_\mathrm{patch} + \pmb{S}_\perp^\top \pmb{x}_\mathrm{context} \tag{11}$$

利用线性性质，可将测量 $\pmb{y}$ 中上下文的贡献扣除，得到仅与补丁相关的残差测量：

$$\tilde{\pmb{y}} = \pmb{y} - \pmb{A} \pmb{S}_\perp^\top \pmb{x}_\mathrm{context}, \quad \tilde{\pmb{A}} = \pmb{A} \pmb{S}^\top \tag{12}$$

由此得到**域分割训练损失**，仅需对小尺寸补丁进行展开重建：

$$\mathcal{L}_\mathrm{PART}(\phi) = \mathbb{E}_{\mathbf{S}} \mathbb{E}_{\pmb{x}^*, \pmb{y}} \parallel \mathrm{R}_\phi(\tilde{\pmb{y}}, \tilde{\pmb{A}}) - \mathbf{S}\pmb{x}^* \parallel_2^2 \tag{13}$$

**Figure 2** 直观展示了这一策略：即使前向算子 $\pmb{A}$ 以非平凡方式混合信号，仍可将全域分解为正交子空间，固定已知上下文（蓝色）后仅求解未知补丁（红色）。

### 核心模块二：正则算子FFT近似

数据一致性步骤中的梯度计算涉及正则算子 $\pmb{A}^\top\pmb{A}$。在大规模问题上，精确计算 $\pmb{A}^\top\pmb{A}$ 代价极高。本工作提出用**对角-循环矩阵乘积**进行高效近似：

$$\pmb{A}^\top \pmb{A} \approx \mathrm{diag}(\pmb{m}) \pmb{F}^{-1} \mathrm{diag}(\pmb{\lambda}) \pmb{F} \tag{16}$$

其中 $\pmb{m}$ 为空间域的对角掩膜，$\pmb{\lambda}$ 为傅里叶域的对角调制参数，$\pmb{F}$ 为傅里叶变换矩阵。这一结构允许通过 FFT 快速计算数据一致性更新。

近似参数 $(\pmb{m}, \pmb{\lambda})$ 通过最小化 Frobenius 范数拟合，且**无需问题相关数据**，仅需高斯随机向量：

$$\mathscr{L}(m, \lambda) = \mathbb{E}_{\mathbf{x} \sim \mathcal{N}(0,I)} \| \mathcal{A}^\top \mathcal{A} \mathbf{x} - H(m, \lambda) \mathbf{x} \|_2^2 = \| \pmb{A}^\top\pmb{A} - H(m,\lambda) \|_F^2 \tag{17-18}$$

在补丁级别应用时，该近似可进一步简化为受限卷积核（大小为 $k=2p$）：

$$\mathbf{S} \mathrm{diag}(\pmb{m}) \mathbf{F}^{-1} \mathrm{diag}(\pmb{\lambda}) \mathbf{F} \mathbf{S}^\top \mathbf{x}_\mathrm{patch} = \mathrm{diag}(\mathbf{S}\pmb{m}) \mathbf{F}_k^{-1} \mathrm{diag}(\pmb{\lambda}_k) \mathbf{F}_k \mathbf{x}_\mathrm{patch}$$

### 测试时两步推理流程

测试时采用 **Algorithm 1** 所述的两步流程：

1. **全局粗估**：在全量体积上执行展开推理，其中去噪器以顺序方式逐补丁应用（利用域分割避免整网前向的内存爆炸）；
2. **补丁细化**：对每个补丁再次执行展开，使用第一步的全局估计作为上下文 $\tilde{\pmb{x}}$，计算残差 $\tilde{\pmb{y}} = \pmb{y} - \pmb{A} \pmb{S}_\perp^\top \pmb{S}_\perp \tilde{\pmb{x}}$，然后聚合所有补丁结果得到最终重建。

### 因果机制总结

两个核心模块分别解决了展开网络在大规模三维逆问题中的不同瓶颈：

- **域分割**通过将训练限制在小补丁上，直接削减了网络步骤的内存消耗（从不可行降至约 44.7 GB，消融实验证实）；
- **正则算子近似**通过 FFT 结构加速数据一致性步骤，进一步缩短训练时间约 30%。

两者的组合使得在单 GPU 上训练处理 $501^3$ 体素的端到端展开网络成为可能，且性能损失可控（约 0.38 dB PSNR 下降）。

### 补充图表

![[assets/figures/papers/paper_list_l2056_https_arxiv_org_abs_2601_02141/figures/012_Figure_9.jpg]]
*Figure 9: Illustrations of the normal operator approximation on Walnut-CBCT. (top row) Original volume slice x, exact normal operator evaluation*

![[assets/figures/papers/paper_list_l2056_https_arxiv_org_abs_2601_02141/figures/013_Figure_10.jpg]]
*Figure 10: Illustrations of the normal operator approximation on Calgary-Campinas. (top row) Original volume slice*



## 实验与关键发现

### 核心瓶颈验证：网络步骤是内存灾难

在深入定量结果之前，必须首先确认本文的核心动机——标准展开网络在大规模三维问题上的内存瓶颈是否真实存在。**Figure 1** 提供了决定性证据：该图对比了展开迭代中两个核心组件——数据一致性步骤（梯度下降）和网络步骤（3D DRUNet）——在评估与反向传播时的峰值显存消耗和全局执行时间。结果显示，数据一致性步骤即使在 501³ 体素的高分辨率下仍保持在可控范围，而网络步骤的显存消耗随体积尺寸急剧膨胀，迅速占据主导地位。这一观测直接界定了问题的因果把手：**不是前向算子的复杂性，而是去噪网络的端到端训练本身，使得大规模三维展开在单 GPU 上不可行。**

### 主要定量结果

#### Walnut-CBCT 稀疏视图重建

**Table 1** 汇总了 Walnut-CBCT 数据集上各方法在 50 视图配置下的重建性能。本文提出的 Unrolled 3D（域分割 + 正则算子近似）达到 **34.21 dB** 的 PSNR，在所有对比方法中排名第一。作为参照，经典 FDK 算法、TV 最小化（FISTA）、后处理 3D DRUNet、PnP-αPGD（3D DRUNet）、DPIR[RAM] 以及 INR（instant-NGP）均未能达到同等水平。更重要的是，标准展开网络（Standard unrolled, K=5）在该数据集上**无法训练**——全量 501³ 体积的显存需求远超单 GPU 容量，这从反面验证了域分割策略的必要性。

**Figure 3** 提供了 30 个投影角度下的轴向和垂直切片视觉对比。本文方法的切片 PSNR 最高，重建结果在细节保留和伪影抑制方面均优于其他方法，尤其在与 INR 和 PnP 方法的对比中，边缘清晰度和纹理一致性优势明显。

#### Calgary-Campinas 多线圈加速 MRI

**Table 2** 报告了 Calgary-Campinas 数据集上加速倍率 R=5 的结果。本文 Unrolled 3D 达到 **37.36 dB** PSNR，与标准展开网络（37.74 dB）差距仅约 0.38 dB，但标准展开在此处可以训练，因为 MC-MRI 的体积尺寸（256×218×170）相对较小。本文方法显著优于后处理 2D/3D DRUNet、PnP-αPGD 和 DPIR[RAM]，且与 INR 相比具有明显优势。值得注意的是，标准展开网络虽然在 PSNR 上略高，但其训练需要全量体积加载，无法推广到 CBCT 规模的问题。

**Figure 4** 展示了 R=5 时轴向和冠状切片的视觉对比。本文方法在抑制欠采样伪影和恢复细微解剖结构方面表现与标准展开网络接近，明显优于 PnP 和 DPIR 方法。

### 消融研究：域分割与正则算子近似的独立贡献

**Table 3** 在两个数据集上系统拆解了域分割（Domain Partitioning）和正则算子近似（Normal Operator Approximation）的各自贡献。

- **仅域分割**：在 MC-MRI 上，仅使用域分割（不使用正则算子近似）将训练峰值显存从标准展开的约 44.7 GB 降至可承受范围，PSNR 仅下降约 **0.38 dB**。这证明域分割策略本身是解决内存瓶颈的核心机制，性能代价很小。
- **仅正则算子近似**：在 MC-MRI 上单独使用正则算子近似会略微降低性能（PSNR 35.12 dB），但仍为第二优。在 Walnut-CBCT 上，单独使用该近似同样有效，但域分割的组合效果最佳。
- **域分割 + 正则算子近似**：组合使用两者在 Walnut-CBCT 上达到 **34.15 dB** PSNR，同时将训练时间缩短约 **30%**。在 MC-MRI 上，组合方案在保持高 PSNR 的同时显著降低了显存和时间开销。

**因果解释**：域分割通过将全局逆问题分解为小尺寸随机补丁，从根本上切断了网络步骤显存与全量体积尺寸的耦合；正则算子近似则将数据一致性更新从精确矩阵乘法转化为 FFT 加速的对角-循环矩阵乘积，进一步压缩了计算开销。两者的协同使得在单 GPU 上训练任意规模三维展开网络成为可能。

### 补丁尺寸的权衡分析

**Figure 7**（Walnut-CBCT）和 **Figure 8**（Calgary-Campinas MC-MRI）展示了训练补丁尺寸对 PSNR、训练时间和峰值显存的三元权衡。两个数据集上均呈现一致趋势：更大的补丁带来更高的 PSNR，但以更高的显存消耗为代价。这一曲线为实际部署提供了显存预算与性能之间的可操作调节旋钮——用户可根据可用 GPU 显存选择合适的补丁尺寸，在资源约束下最大化重建质量。

### 正则算子近似的可视化验证

**Figure 9**（Walnut-CBCT）和 **Figure 10**（Calgary-Campinas）直观展示了正则算子近似的质量。每张图的顶行对比了原始切片 x、精确正则算子评估 AᵀAx 和近似结果 H(m,λ)x；底行展示了学习到的傅里叶域滤波器 λ、空间掩膜 m 以及平方近似误差。在 CBCT 上，近似误差集中在高频边缘区域，但整体结构保真度很高；在 MC-MRI 上，近似同样捕捉了正则算子的主要能量分布。这些可视化表明，**H = diag(m) F⁻¹ diag(λ) F** 的低秩结构逼近在实际三维问题上具有足够的表达能力。

### 失败模式与局限性

1. **性能上限的微小损失**：域分割训练使用小补丁，相较于在全量体积上训练的标准展开网络存在约 0.38 dB 的 PSNR 差距（Table 3）。这是内存效率与重建精度之间的固有权衡。
2. **正则算子近似的适用范围**：H 的近似形式假设前向算子 AᵀA 可被对角-循环结构良好逼近。对于多线圈 MRI 等更复杂的算子，可能需要额外的空间调制项才能获得足够好的近似（文中提及但未展开），这增加了调优复杂性。
3. **测试时推理开销**：两步推理流程（全局粗估 + 补丁细化）在 CBCT 上是必要的，但对于 MC-MRI 这种子问题已表现良好的场景，细化步骤带来的增益可忽略，却增加了不必要的计算开销。这提示测试策略需要根据问题特性自适应选择。
4. **单 GPU 限制**：当前补丁尺寸和训练策略仅针对单 GPU 环境设计，未探索多 GPU 分布式训练下的最优并行策略，这在高维（4D）或更大规模场景下可能成为新的瓶颈。

![[assets/figures/papers/paper_list_l2056_https_arxiv_org_abs_2601_02141/figures/007_Table_3.jpg]]
*Table 3: Ablation study on the Calgary-Campinas dataset and the Walnut-CBCT dataset. For each line we report the PSNR averaged on the different subsampling configurations, as well as the peak video memory usage in GB and training speed. Best and second-best results highlighted*

### 公平性保障说明

所有学习方法均基于相同的骨干网络 DRUNet（3D 版本约 96.5M 参数），采用统一的训练超参数（Adam 优化器、余弦退火学习率调度、10⁵ 训练步数）。域分割方法使用批量大小 1 并累积 4 步梯度，以匹配其他方法的有效批量大小 4。评估均在相同测试数据上以幅度图像的 PSNR 和 SSIM 进行，确保了对比的公平性。

### 补充图表

![[assets/figures/papers/paper_list_l2056_https_arxiv_org_abs_2601_02141/figures/003_Table.jpg]]
*Table: CBCT is a typical example of a 3D inverse problem that does not admit a coordinate-friendly partitioning of the forward operator, thus making it impossible to train unrolled networks on patches without our proposed domain partitioning strategy*

![[assets/figures/papers/paper_list_l2056_https_arxiv_org_abs_2601_02141/figures/005_Table_2.jpg]]
*Table 2: Reconstruction performances on the Calgary-Campinas dataset. PSNR and SSIM are measured on amplitude images. Best and second-best results highlighted*

![[assets/figures/papers/paper_list_l2056_https_arxiv_org_abs_2601_02141/figures/011_Figure_7.jpg]]
*Figure 7: Walnut-CBCT - Average PSNR and time complexity against peak memory consumption during training. We vary the VRAM budget by changing the patch size used during domain partitioning. Larger patches lead to better performance at the cost of higher memory consumption. We do not show the complexity of standard unrolling (without partitioning) as a single H100 GPU is not sufficient for training it*

![[assets/figures/papers/paper_list_l2056_https_arxiv_org_abs_2601_02141/figures/010_Figure_8.jpg]]
*Figure 8: Calgary-Campinas MC-MRI - Average PSNR and time complexity against peak memory consumption during training. We vary the VRAM budget by changing the patch size used during domain partitioning. Larger patches lead to better performance at the cost of higher memory consumption*

![[assets/figures/papers/paper_list_l2056_https_arxiv_org_abs_2601_02141/figures/004_Figure_3.jpg]]
*Figure 3: Illustrations of sparse view reconstructions with [30/1200] projections on the Walnut-CBCT [10] dataset using the methods compared in Tab. 1. First row axial slices, second row vertical slices from the same sample. PSNR is computed per slice*

![[assets/figures/papers/paper_list_l2056_https_arxiv_org_abs_2601_02141/figures/006_Figure_4.jpg]]
*Figure 4: Illustrations of MC-MRI reconstructions with acceleration rate of 5 on the Calgary-Campinas dataset [52] for the methods compared in Tab. 2. First row: axial slice, second row: coronal slice from the same sample. PSNR is computed per slice*



## 定位与知识库关联

### 1. 方法谱系：从即插即用到端到端展开

本文方法处于**学习型三维逆问题重建**的交叉点上，其直接技术谱系可沿两条主线追溯：**即插即用（Plug-and-Play, PnP）框架**与**展开网络（Unrolled Networks）**。

在PnP方向上，**PnP-αPGD**（使用2D/3D DRUNet先验）和**DPIR[RAM]**代表了将预训练去噪器嵌入迭代优化器的经典范式。这些方法在每次迭代中调用去噪网络作为隐式正则项，但其去噪器是独立于前向算子训练的，缺乏端到端的数据一致性感知。本文的展开网络直接沿袭了**Standard unrolled (3D DRUNet, K=5)** 的架构——将可学习去噪先验 $D_\phi$ 嵌入梯度下降步骤中：

$$\pmb{x}_{k+1} = \mathrm{D}_\phi\big(\pmb{x}_k - \eta \nabla_{\pmb{x}_k} d(\pmb{A x}_k, \pmb{y})\big)$$

并通过端到端损失 $\mathcal{L}_\mathrm{UNR}(\phi)$ 联合优化所有展开步骤。这一设计继承自展开优化的核心思想：将迭代算法的每个步骤参数化，使网络能够学习针对特定前向算子的最优重建策略。

在非学习基线方面，**Feldkamp-Davis-Kress (FDK) 算法**（CBCT）和**Zero-filled RSS重建**（MC-MRI）代表了经典的解析重建方法，而**Total Variation (TV) minimization**（使用FISTA求解）则是标准的变分正则化方法。这些方法无需训练数据，但重建质量受限于手工设计的先验假设。

### 2. 关键差异：域分割与正则算子近似

本文方法的核心创新在于**训练机制的改变**，而非网络架构本身。所有学习方法均共享相同的DRUNet骨干网络（3D版本约96.5M参数），差异体现在训练和推理的计算策略上：

| 方法 | 训练域 | 数据一致性计算 | 推理方式 |
|------|--------|----------------|----------|
| Standard unrolled | 完整体积 | 精确梯度下降 | 单次全量展开 |
| Post-processing (DRUNet) | 补丁级 | 无（仅后处理） | 补丁聚合 |
| PnP-αPGD / DPIR | 无需训练 | 精确梯度下降 | 迭代优化 |
| **本文方法** | **补丁级（域分割）** | **FFT近似（正则算子逼近）** | **两步：全量粗估+补丁细化** |

**域分割策略**的核心在于利用线性前向算子的线性性质，将全量问题在训练时分解为小尺寸随机补丁子问题。具体而言，通过正交分解 $\mathbb{R}^n = \mathbb{R}^p \oplus \mathbb{R}^q$ 和上下文补偿 $\tilde{\pmb{y}} = \pmb{y} - \pmb{A} \pmb{S}_\perp^\top \pmb{x}_\mathrm{context}$，将全局逆问题转化为多个补丁级子问题。这使得训练内存从完整体积（如CBCT的501³体素）降至可控范围（如8×384²的补丁）。

**正则算子近似** $H = \mathrm{diag}(\pmb{m}) \pmb{F}^{-1} \mathrm{diag}(\pmb{\lambda}) \pmb{F}$ 则通过空间掩膜和对角化傅里叶域调制，将 $\pmb{A}^\top\pmb{A}$ 的计算复杂度从显式矩阵乘法降至FFT加速的卷积形式。其参数 $(\pmb{m}, \pmb{\lambda})$ 通过Frobenius范数损失在高斯随机向量上拟合得到：

$$\mathscr{L}(m, \lambda) = \mathbb{E}_{\mathbf{x} \sim \mathcal{N}(0,I)} \| \mathcal{A}^\top \mathcal{A} \mathbf{x} - H(m, \lambda) \mathbf{x} \|_2^2 = \| \pmb{A}^\top\pmb{A} - H(m,\lambda) \|_F^2$$

这一设计的关键优势在于**无需问题相关数据即可拟合近似参数**，显著降低了调优成本。

### 3. 与隐式神经表示（INR）的关系

本文还与基于坐标的隐式神经表示方法形成对比。**INR (instant-NGP/grid-based)**（Müller et al., SIGGRAPH 2022）通过逐样本优化隐式函数来重建三维体积，其优势在于内存效率极高，但推理时需要针对每个新样本重新优化，计算开销较大。本文的展开网络则在训练阶段一次性学习重建映射，推理时仅需前向传播，更适合需要快速重建的应用场景。两者在内存-计算权衡曲线上占据不同的位置：INR偏向极低训练内存、高推理成本；本文方法则通过域分割在训练内存和推理速度之间取得平衡。

### 4. 适用边界与局限

**适用条件**：本文方法的核心假设是前向算子为线性算子，这是域分割策略（利用线性叠加原理）和正则算子近似（利用循环矩阵结构）的基础。对于非线性前向算子，这两个关键组件均无法直接适用。

**性能权衡**：
- 域分割训练使用较小补丁尺寸，相较于完整体积上的标准展开网络存在约0.38 dB的PSNR轻微下降（Tab. 3, MC-MRI数据集）。这是内存效率与重建精度之间的直接权衡。
- 正则算子近似 $H = \mathrm{diag}(\pmb{m}) \pmb{F}^{-1} \mathrm{diag}(\pmb{\lambda}) \pmb{F}$ 并非对所有前向算子都精确。对于多线圈MRI，需要通过略微变化的分解（如增加额外的空间调制项）才能获得良好近似，这增加了调优的复杂性。在MC-MRI上单独使用正则算子近似会导致性能下降（Tab. 3, PSNR 35.12 vs. 最优37.36），表明该近似在特定前向算子结构下存在精度损失。

**推理开销**：测试时的两步推理流程（全量粗估 + 补丁细化）增加了计算量。对于CBCT，细化步骤是必要的；但对于MC-MRI这类子问题已表现良好的场景，细化带来的增益可忽略，却引入了不必要的开销。这表明两步策略的收益因前向算子的混合特性而异。

**硬件限制**：当前的补丁尺寸和训练策略仅针对单GPU环境设计，未探索多GPU分布式训练或更大规模下的最优并行策略。在需要处理更大体积或更高维度数据时，单GPU的内存限制可能再次成为瓶颈。

### 5. 开放问题

1. **自适应补丁选择**：如何根据数据特性和前向算子结构自动选择最优的补丁尺寸与形状？当前补丁尺寸依赖人工调优（Fig. 7, Fig. 8展示了补丁大小对PSNR-内存权衡的影响），缺乏自动化机制。

2. **非线性前向算子的推广**：域分割和正则算子逼近能否推广到更一般的非线性或时变前向算子？这需要重新设计分解策略和近似结构，可能涉及局部线性化或可逆网络技术。

3. **与内存优化技术的结合**：域分割方法是否可以与可逆网络或梯度检查点技术结合，以进一步降低训练内存并加快收敛？这些技术在深度学习训练中已被证明有效，但尚未在展开网络的上下文中与域分割联合优化。

4. **补丁间相关性的利用**：在测试时，是否可以利用补丁间空间相关性设计更高效的融合策略，以减少两步推理中的冗余计算？当前的补丁聚合策略相对简单，可能存在信息利用不充分的问题。

5. **高维扩展性**：该方法在更高维（4D动态成像或更高）或稀疏数据采集场景下的可扩展性和性能表现如何？随着维度增加，补丁分解的组合复杂度和正则算子近似的精度需求可能发生质变。



## 原文 PDF

![[paperPDFs/CVPR_2026/Efficient_Unrolled_Networks_for_Large_Scale_3D_Inverse_Problems.pdf]]
