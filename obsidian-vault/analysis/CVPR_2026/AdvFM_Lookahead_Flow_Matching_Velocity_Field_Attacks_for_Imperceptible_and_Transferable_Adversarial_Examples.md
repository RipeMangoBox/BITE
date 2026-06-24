---
title: "AdvFM: Lookahead Flow-Matching Velocity-Field Attacks for Imperceptible and Transferable Adversarial Examples"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/AdvFM_Lookahead_Flow_Matching_Velocity_Field_Attacks_for_Imperceptible_and_Transferable_Adversarial_Examples.pdf
project_link: null
code_link: null
aliases:
- ALFMVFA
- AdvFM
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/representation_self_supervised_transfer
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 将攻击扰动从像素空间转移至流匹配的连续时间速度场，并引入前瞻双点优化以对齐概率流ODE轨迹。
primary_logic: 流匹配的确定性和平滑动态使噪声空间中的扰动具有低方差、近似线性传播特性，并将扰动集中于数据流形切向方向，从而增强跨模型共享梯度的对齐，提升黑盒迁移性和对净化、对抗训练防御的鲁棒性。
claims:
- 流匹配速度场攻击（FM）在相同扰动下的单步目标损失放大大于扩散攻击。
- FM攻击方向方差低于扩散攻击，导致与目标梯度对齐改善。
- FM扰动更集中于流形切向方向，与鲁棒梯度对齐更好，且抗净化能力强。
- 前瞻损失进一步降低梯度方差，提升黑盒迁移性。
---

# AdvFM: Lookahead Flow-Matching Velocity-Field Attacks for Imperceptible and Transferable Adversarial Examples

> [!tip] 核心洞察
> 流匹配的确定性和平滑动态使噪声空间中的扰动具有低方差、近似线性传播特性，并将扰动集中于数据流形切向方向，从而增强跨模型共享梯度的对齐，提升黑盒迁移性和对净化、对抗训练防御的鲁棒性。

| 字段 | 内容 |
|------|------|
| 中文题名 | AdvFM: 基于前瞻流匹配速度场的不可感知与可迁移对抗攻击 |
| 英文题名 | AdvFM: Lookahead Flow-Matching Velocity-Field Attacks for Imperceptible and Transferable Adversarial Examples |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Liu_AdvFM_Lookahead_Flow-Matching_Velocity-Field_Attacks_for_Imperceptible_and_Transferable_Adversarial_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/representation_self_supervised_transfer #topic/vision_multimodal_applications/image_and_video_generation |
| Method | AdvFM (Lookahead Flow-Matching Velocity-Field Attack) |
| Dataset | ImageNet, 对抗净化防御 NRP, 对抗净化防御 Smooth, 对抗净化防御 DiffPure |

> [!tip] 效果简介
> - ImageNet (VGG19 替代模型) 上，平均黑盒 ASR (%) 70.35 vs 65.86 (APA) (+4.49)。
> - ImageNet (ResNet50 替代模型) 上，平均黑盒 ASR (%) 72.05 vs 64.41 (APA) (+7.64)。
> - ImageNet (ViT-B/16 替代模型) 上，平均黑盒 ASR (%) 68.22 vs 65.04 (APA) (+3.18)。

## 概述

**问题瓶颈**：现有基于扩散模型的非限制攻击（如 AdvDiffuser、DiffPGD）在生成对抗样本时，依赖随机噪声耦合与逐步衰减的重加噪过程。这导致替代模型的攻击梯度方差高、与目标模型真实梯度的对齐差，且扰动易被基于扩散的净化防御（如 DiffPure）削弱。

**核心思路**：AdvFM 将攻击扰动从像素空间转移至流匹配（Flow Matching）的连续时间速度场，并引入前瞻双点优化以对齐概率流 ODE 轨迹。流匹配的确定性和平滑动态使噪声空间中的扰动具有低方差、近似线性传播特性，并将扰动集中于数据流形的切向方向，从而增强跨模型共享梯度的对齐。

**关键结论**：
- **理论保证**：流匹配速度场攻击在相同扰动下的单步目标损失放大比扩散攻击更大（Lemma 1），攻击方向方差更低，与目标梯度和鲁棒梯度的对齐均优于扩散攻击（Theorem 1–3）。
- **黑盒迁移性**：在 ImageNet 上以 VGG19、ResNet50、ViT‑B/16、Swin‑B 为替代模型时，AdvFM 的平均黑盒攻击成功率（ASR）分别达到 70.35%、72.05%、68.22%、64.88%，均优于最强基线 APA（Jiang et al., arXiv 2025），提升幅度为 +3.18 至 +7.64 个百分点（Table 1）。
- **防御鲁棒性**：面对 NRP 和 Smooth 净化防御，AdvFM 的 ASR 分别达 94.98% 和 81.35%，比 APA 高出 13.8 和 11.1 个百分点；在 DiffPure 净化上略低于 APA（61.33% vs. 64.14%），需进一步验证（Table 2）。
- **前瞻损失增益**：消融实验表明，引入前瞻双点损失后，黑盒平均 ASR 从 64.31% 提升至 72.05%，白盒 ASR 从 91.72% 提升至 94.45%（Figure 2）。

**方法定位**：AdvFM 属于基于生成模型的非限制对抗攻击，其方法论上从扩散模型范式切换至流匹配速度场范式，扰动注入位置从重建图像空间改为速度场空间，并通过前瞻损失实现沿概率流 ODE 轨迹的时域梯度对齐。

## 背景与动机

### 对抗攻击的生成模型范式

深度神经网络在图像分类等任务上对精心设计的对抗扰动高度脆弱，这一现象催生了大量攻击方法。传统攻击方法（如 PGD）直接在像素空间施加 $L_p$ 范数约束的扰动，但受限于扰动预算，其黑盒迁移性和对净化防御的鲁棒性往往不足。近年来，扩散模型被引入对抗攻击领域，形成了以 **AdvDiffuser**（Chen et al., ICCV 2023）、**DiffPGD**（Xue et al., NeurIPS 2023）、**DiffAttack**（Kang et al., NeurIPS 2023）、**AdvAD**（Li et al., NeurIPS 2024）和 **APA**（Jiang et al., arXiv 2025）为代表的无限制攻击范式。这些方法利用扩散模型的去噪过程生成对抗样本，在保持视觉质量的同时突破了像素空间约束的限制。

### 扩散攻击的内在瓶颈

尽管扩散模型攻击取得了显著进展，其核心机制存在一个根本性瓶颈：**随机噪声耦合与逐步衰减导致替代梯度方差高、与目标梯度对齐差，且扰动易被净化防御削弱**。具体而言，扩散攻击将对抗扰动注入去噪重建图像 $x_0'$，该重建通过以下公式获得：

$$x_0' = \frac{1}{\sqrt{\bar{\alpha}_t}} \Big( x_t - \sqrt{1 - \bar{\alpha}_t} \, \mu_\theta(x_t, t) \Big)$$

其中 $x_t = \sqrt{\bar{\alpha}_t} x_0 + \sqrt{1 - \bar{\alpha}_t} \epsilon$ 是噪声状态，$\bar{\alpha}_t$ 是累积噪声尺度。扰动在噪声空间中的有效传播受衰减因子 $\sqrt{\bar{\alpha}_t} < 1$ 支配，这意味着随着去噪过程的推进，扰动的影响被逐步压缩。这种衰减效应带来了三重后果：（1）单步攻击的损失放大有限，优化效率低下；（2）随机噪声的耦合使替代模型梯度方差高，与目标模型真实梯度的对齐度差，限制了黑盒迁移性；（3）扰动方向偏离数据流形的切向方向，容易被基于扩散的净化防御（如 DiffPure）滤除。

### 流匹配的机遇与本文动机

流匹配（Flow Matching）作为扩散模型的替代范式，通过学习连续时间速度场 $v_\theta(x_t, t)$ 直接参数化概率流 ODE 的向量场，具有确定性和平滑动态的特性。本文的核心洞察在于：**将攻击扰动从像素空间转移至流匹配的连续时间速度场，并引入前瞻双点优化以对齐概率流 ODE 轨迹**。这一设计有望从根本上解决扩散攻击的三重困境——流匹配的确定性传播降低梯度方差，速度场空间的扰动放大机制提升单步攻击效率，而流形切向的扰动偏置则增强对净化防御的鲁棒性。基于此，本文提出 **AdvFM**（Lookahead Flow-Matching Velocity-Field Attack），在保持对抗样本不可感知性的同时，系统性地提升黑盒迁移性和防御鲁棒性。

## 核心创新

AdvFM 的核心创新在于将对抗攻击的扰动注入空间从像素域迁移至**流匹配的连续时间速度场**，并通过**前瞻双点优化**对齐概率流 ODE 轨迹，从根本上解决了扩散模型攻击中随机噪声耦合导致的梯度方差高、目标梯度对齐差以及扰动易被净化防御削弱等瓶颈问题。

### 攻击范式的根本转变：从扩散去噪到流匹配速度场

现有扩散模型攻击（如 **AdvDiffuser** (Chen et al., ICCV 2023)、**DiffPGD** (Xue et al., NeurIPS 2023)）的核心范式是在扩散过程的去噪/重加噪循环中注入扰动。具体而言，它们在每个时间步通过去噪器 $\mu_\theta$ 重建近似干净图像 $x_0'$，在该重建上执行 PGD 攻击，再将扰动后的图像重新加噪回噪声空间。这一范式存在两个结构性缺陷：(1) 扰动在重加噪过程中被衰减因子 $\sqrt{\bar{\alpha}_t} < 1$ 压缩，有效步长被削弱；(2) 随机噪声的耦合使替代梯度方差增大，与目标模型梯度的对齐恶化。

AdvFM 将攻击范式彻底重构为**流匹配连续速度场**上的扰动注入。给定噪声状态 $x_t$，流匹配重建算子直接通过速度场预测流终点：

$$R_t(x_t) := x_t + (1 - t) v_\theta(x_t, t)$$

攻击在重建图像 $R_t(x_t)$ 上生成对抗扰动 $\delta$，随后将该像素空间扰动**转换为速度场扰动**：

$$\hat{v}_t = \frac{\hat{x}_1^t - x_t}{1-t} = v_\theta(x_t, t) + \frac{\delta}{1-t}$$

最后通过欧拉推进更新噪声状态：

$$x_{t+\Delta t} = x_t + \Delta t \hat{v}_t$$

这一转换带来了关键的结构性优势：扰动传播系数从扩散的衰减因子 $\sqrt{\bar{\alpha}_t}$ 变为放大因子 $\frac{\Delta t}{1-t} > 1$（对于典型时间调度），使得噪声空间中的有效步长被**放大而非压缩**。

### 五个关键 changed slots 的因果机制

AdvFM 相对于扩散攻击基线的创新可精确分解为五个 changed slots，每个 slot 的变更都直接对应一个因果瓶颈的突破：

| Slot | 基线值 | AdvFM 值 | 因果作用 |
|------|--------|----------|----------|
| 生成模型与攻击范式 | 扩散模型去噪/重加噪 | 流匹配连续速度场 | 消除随机噪声耦合，降低替代梯度方差 |
| 扰动注入位置 | 重建图像空间 ($x_0'$) | 速度场空间（转化为速度扰动） | 扰动在噪声空间中传播时被放大而非衰减 |
| 优化损失 | 当前重建损失（单点） | 前瞻双点损失 | 对齐概率流 ODE 轨迹的时域梯度，进一步降低方差 |
| 状态演化步 | 扩散重采样步 | 欧拉推进步 | 确定性动力学传播，避免重采样引入的随机性 |
| 扰动传播系数 | 衰减因子 $\sqrt{\bar{\alpha}_t} < 1$ | 放大因子 $\frac{\Delta t}{1-t} > 1$ | 单步目标损失放大比显著提升 |

其中，扰动传播系数的反转是最具决定性的因果杠杆。Lemma 1 证明，在相同扰动 $\delta$ 下，流匹配攻击与扩散攻击的单步目标损失放大比为：

$$\frac{\Delta \mathcal{L}_g^{\mathrm{FM}}}{\Delta \mathcal{L}_g^{\mathrm{Diff}}} = \frac{\Delta t}{(1-t)\sqrt{\bar{\alpha}_t}}$$

该比值在典型时间调度下始终大于 1，意味着流匹配攻击在每一步都能更有效地放大目标损失，为黑盒迁移性提供了更强的梯度信号。

### 前瞻双点优化：对齐概率流 ODE 轨迹

基础流匹配攻击虽然已优于扩散攻击，但其优化目标仅关注当前时间步的重建损失，忽略了速度场沿概率流 ODE 轨迹的时域连续性。AdvFM 引入**前瞻损失**，联合优化当前与未来重建：

$$\mathcal{L}_f^{\mathrm{LA}}(\delta; t) = w \mathcal{L}_f(x_1^t + \delta, y) + (1-w) \mathcal{L}_f(x_1^{t+\Delta t}(\delta), y)$$

其中 $x_1^{t+\Delta t}(\delta)$ 是通过扰动速度场推进后获得的未来重建。这一双点目标迫使攻击方向不仅在当前时间步有效，而且在沿 ODE 轨迹前向传播后仍然保持对抗性，从而**对齐时域梯度**，进一步降低替代梯度方差。消融实验证实，前瞻损失使黑盒平均 ASR 从 64.31% 提升至 72.05%，白盒 ASR 从 91.72% 提升至 94.45%（Figure 2）。

### 理论保证：梯度对齐与抗净化鲁棒性

AdvFM 的创新不仅体现在经验性能上，更有严格的理论支撑。Theorem 1 证明，流匹配攻击方向与目标模型真实梯度的期望余弦相似度严格大于扩散攻击：

$$\mathbb{E}[\cos\angle(\mathcal{G}_f^{\mathrm{FM}}(x), \mathcal{G}_g(x))] > \mathbb{E}[\cos\angle(\mathcal{G}_f^{\mathrm{Diff}}(x), \mathcal{G}_g(x))]$$

这一对齐优势源于流匹配的确定性和平滑动态使攻击方向方差更低（Lemma 3），且扰动更集中于数据流形的切向方向。Theorem 2 进一步证明，FM 攻击方向与鲁棒梯度 $\mathcal{G}_{\mathrm{rob}}(x)$ 的对齐也优于扩散攻击，解释了其对对抗训练防御的更强穿透力。Theorem 3 则从理论上保证了 FM 扰动经净化后保留更多有效能量：

$$\mathbb{E}\|P(x + \eta^{\mathrm{FM}}) - P(x)\|^2 > \mathbb{E}\|P(x + \eta^{\mathrm{Diff}}) - P(x)\|^2$$

这直接转化为对净化防御（NRP、Smooth）的显著 ASR 提升（+13.8% 和 +11.1%）。

## 整体框架

AdvFM 将无限制对抗攻击从扩散模型的随机去噪/重加噪范式迁移至流匹配（Flow Matching）的连续时间速度场，构成一条“噪声桥采样 → 速度场重建 → PGD 扰动注入 → 速度扰动转换 → 欧拉前向推进 → 前瞻双点评估”的闭环管线（参见 Algorithm 1）。

**管线概览。** 给定干净图像 $x$，首先通过噪声桥 $x_t = t x + (1-t) \epsilon$ 采样时间索引的噪声状态（$\epsilon \sim \mathcal{N}(0,I), t \in [0,1]$），将问题嵌入一个平滑的噪声景观。随后，流匹配重建算子 $R_t(x_t) := x_t + (1-t) v_\theta(x_t, t)$ 单步预测流终点 $\hat{x}_1^t$，作为攻击的起点。在 $\hat{x}_1^t$ 上执行投影梯度下降（PGD），注入对抗扰动 $\delta$，并计算分类损失。若启用前瞻模式，则额外沿概率流 ODE 推进一个时间步，评估未来重建 $\hat{x}_1^{t+\Delta t}$ 上的损失，形成联合双点损失 $\mathcal{L}_f^{\mathrm{LA}}$（式 12）。最后，将图像空间扰动 $\delta$ 转换为速度场扰动 $\hat{v}_t = v_\theta(x_t, t) + \frac{\delta}{1-t}$（式 8），并通过欧拉推进 $x_{t+\Delta t} = x_t + \Delta t \hat{v}_t$（式 9）更新噪声状态，进入下一轮迭代。

**模块关系与数据流。** 五个核心模块构成一个循环：

1. **噪声桥采样**：将干净图像映射到时间索引的噪声状态 $x_t$，提供平滑的替代损失景观。
2. **流匹配重建**：从 $x_t$ 通过速度场 $v_\theta$ 预测流终点 $\hat{x}_1^t$，作为攻击的决策边界评估点。
3. **PGD 攻击模块**：在 $\hat{x}_1^t$ 上执行多步投影梯度上升，注入扰动 $\delta$；可选用前瞻损失联合优化当前与未来重建。
4. **速度场扰动更新**：将 $\delta$ 转为速度扰动 $\hat{v}_t$，并沿概率流 ODE 执行欧拉前向步，推进至 $x_{t+\Delta t}$。
5. **前瞻评估**：滚动输出未来重建 $\hat{x}_1^{t+\Delta t}$，与当前重建联合计算双点损失，以对齐时域梯度、降低替代梯度方差。

**与扩散攻击的关键差异。** 传统扩散攻击（如 AdvDiffuser、DiffPGD）在重建图像空间注入扰动，并通过扩散重采样步更新状态，其扰动传播受衰减因子 $\sqrt{\bar{\alpha}_t} < 1$ 抑制。AdvFM 将扰动注入位置从像素空间转移至速度场空间，利用欧拉推进的放大因子 $\frac{\Delta t}{1-t} > 1$ 实现噪声空间中的有效步长放大（式 11 vs 式 4），从而在单步内获得更大的目标损失增益（Lemma 1, 式 17）。同时，流匹配的确定性动态消除了扩散攻击中随机噪声耦合引入的高方差，使替代梯度方向更稳定，与目标模型共享梯度子空间的对齐显著改善（Theorem 1, 式 23）。前瞻损失进一步降低了梯度方差（Figure 2, Sec. 5.4），并将扰动偏置到数据流形的切向方向，增强了对净化防御和对抗训练模型的鲁棒性（Theorem 2, Theorem 3）。

**输入输出规格。** 输入为干净图像 $x$、真实标签 $y$、替代模型 $f$ 及流匹配速度场 $v_\theta$；输出为对抗样本 $x_{\mathrm{adv}}$。管线从 $t=t_0$ 迭代至 $t=1$，每一步在流终点评估损失并反向传播梯度，最终在 $t=1$ 处输出对抗图像。

## 核心模块与公式推导

AdvFM 的攻击范式建立在**流匹配（Flow Matching）连续时间速度场**之上，核心思路是将对抗扰动从像素空间转移至速度场空间，并利用概率流 ODE 的确定性动态实现扰动放大与梯度方差降低。整个攻击管线由五个关键模块串联构成。

### 噪声桥采样

攻击的起点是将干净图像映射到带时间索引的噪声状态。AdvFM 采用线性插值形式的噪声桥，而非扩散模型中基于累积噪声系数的加噪过程：

$$x_t = t x + (1 - t) \epsilon, \quad \epsilon \sim \mathcal{N}(0, I), \quad t \in [0, 1]$$

其中 $x$ 为干净图像，$\epsilon$ 为标准高斯噪声，$t$ 为流时间参数。该采样的核心优势在于：噪声状态 $x_t$ 的分布构成了一条从纯噪声（$t=0$）到干净图像（$t=1$）的平滑路径，为后续速度场预测提供了梯度方差更低的优化景观。

### 流匹配重建算子

给定噪声状态 $x_t$，AdvFM 并不直接攻击 $x_t$，而是通过速度场 $v_\theta$ 单步预测流的终点作为攻击起点：

$$R_t(x_t) := x_t + (1 - t) v_\theta(x_t, t)$$

该重建算子 $R_t$ 输出的是对 $t=1$ 处干净图像的近似估计 $x_1^t$。在此重建图像上执行 PGD 攻击，注入对抗扰动 $\delta$，得到 $\hat{x}_1^t = x_1^t + \delta$。

### 速度场扰动转换

像素空间的扰动 $\delta$ 需要被转换为速度场空间的扰动，以驱动噪声状态的演化。转换关系由流匹配的线性结构直接给出：

$$\hat{v}_t = \frac{\hat{x}_1^t - x_t}{1 - t} = v_\theta(x_t, t) + \frac{\delta}{1 - t}$$

关键观察：扰动 $\delta$ 在速度场中被放大了 $1/(1-t)$ 倍。当 $t$ 接近 1 时，该放大效应极为显著，这是 AdvFM 攻击效能的第一个核心机制。

### 欧拉推进更新

得到扰动后的速度 $\hat{v}_t$ 后，AdvFM 沿概率流 ODE 执行欧拉前向步，将噪声状态推进到下一时间点：

$$x_{t + \Delta t} = x_t + \Delta t \hat{v}_t$$

由此产生的噪声空间有效步长为：

$$\Delta x_t^{\mathrm{FM}} = \frac{\Delta t}{1 - t} \delta$$

与之形成对比的是扩散模型攻击中的有效步长 $\Delta x_t^{\mathrm{Diff}} = \sqrt{\bar{\alpha}_t} \delta$，其中 $\sqrt{\bar{\alpha}_t} < 1$ 为衰减因子。AdvFM 的放大系数 $\Delta t/(1-t)$ 在典型调度下大于 1，意味着相同 $\delta$ 在噪声空间中产生更大的状态变化，这是其**单步损失放大比**优于扩散攻击的根本原因（Lemma 1）。

### 前瞻双点损失

基础流匹配攻击仅在当前时刻 $t$ 的重建图像上优化损失。AdvFM 进一步引入**前瞻（Lookahead）机制**，在欧拉推进后再次重建并评估损失，联合优化当前与未来两个时间点的目标：

$$\mathcal{L}_f^{\mathrm{LA}}(\delta; t) = w \mathcal{L}_f(x_1^t + \delta, y) + (1 - w) \mathcal{L}_f(x_1^{t+\Delta t}(\delta), y)$$

其中 $w \in [0, 1]$ 为权重系数，$x_1^{t+\Delta t}(\delta)$ 是扰动 $\delta$ 经速度场更新和欧拉推进后得到的未来重建。该双点损失沿概率流 ODE 轨迹对齐时域梯度，进一步降低了替代梯度方差（Theorem 4），是黑盒迁移性提升的第二个核心机制。消融实验表明，引入前瞻损失后，黑盒平均 ASR 从 64.31% 提升至 72.05%，白盒 ASR 从 91.72% 提升至 94.45%（Figure 2）。

![[assets/figures/papers/paper_list_l836_https_openaccess_thecvf_com_content_CVPR2026_html_Liu_AdvFM_Lookahead_Fl/figures/004_Figure_2.jpg]]
*Figure 2: Ablation of the lookahead objective on ImageNet with ResNet50 as the surrogate. We plot white-box ASR on the surrogate and the average black-box ASR on the remaining models along the reverse flow from t to 1*

## 实验与分析

### 主实验结果：黑盒迁移性

Table 1 报告了以四种不同架构的模型作为替代（VGG19、ResNet50、ViT‑B/16、Swin‑B）时，在 ImageNet 上对多种黑盒目标模型的攻击成功率（ASR）。AdvFM 在所有替代模型设置下均取得最高的平均黑盒 ASR，且相对于最强基线 **APA**（Jiang et al., arXiv 2025）的领先幅度在 3.18 – 7.64 个百分点之间。具体而言，以 ResNet50 为替代时 AdvFM 的平均黑盒 ASR 达到 72.05%，比 APA 高出 7.64 pp；以 VGG19 为替代时达到 70.35%（+4.49 pp）；以 ViT‑B/16 和 Swin‑B 为替代时分别为 68.22%（+3.18 pp）和 64.88%（+3.39 pp）。这一跨架构的稳定优势验证了理论分析的核心主张：流匹配速度场攻击产生的替代梯度与目标模型共享梯度子空间的对齐更好（Theorem 1），且攻击方向的方差更低（Lemma 3），从而在多种模型对之间均能实现更高的迁移性。

![[assets/figures/papers/paper_list_l836_https_openaccess_thecvf_com_content_CVPR2026_html_Liu_AdvFM_Lookahead_Fl/figures/001_Table_1.jpg]]
*Table 1: Black-box attack success rate (ASR, %) on ImageNet classifiers. Best results per column (within each source model block) are in bold, second-best are underlined. * represents white-box attack*

### 防御鲁棒性：净化与对抗训练

Table 2 展示了在三种典型的对抗净化防御（NRP、Smooth、DiffPure）以及对抗训练模型上的攻击成功率。AdvFM 在 NRP 和 Smooth 防御下分别取得 94.98%（+13.8 pp 超过 APA）和 81.35%（+11.1 pp），展现出对净化类防御的显著鲁棒性。这一结果与 Theorem 3 一致：流匹配扰动更集中于数据流形的切向方向，经净化操作后保留了更多的有效扰动能量（Eq. 28），从而在净化后仍能维持高攻击性。在 DiffPure 防御下，AdvFM 的 ASR 为 61.33%，略低于 APA 的 64.14%（‑2.81 pp），提示 DiffPure 的随机前向扩散与流匹配动态之间可能存在特定的交互效应，需要进一步验证。在对抗训练模型上，AdvFM 同样保持竞争力，这与 Theorem 2 的结论一致——流匹配攻击方向与鲁棒梯度 $\\mathcal{G}_{\\mathrm{rob}}$ 的对齐优于扩散攻击，使其能有效应对对抗训练引入的损失景观变化。

![[assets/figures/papers/paper_list_l836_https_openaccess_thecvf_com_content_CVPR2026_html_Liu_AdvFM_Lookahead_Fl/figures/003_Table_2.jpg]]
*Table 2: ASR (%) against purification and adversarially trained defenses on ImageNet. Best results per column are in bold, second-best are underlined*

### 前瞻损失的消融分析

Figure 2 展示了在 ResNet50 作为替代模型时，沿反向流从时间 $t$ 到 $1$ 的过程中，前瞻损失对白盒 ASR 和平均黑盒 ASR 的影响。消融结果表明，引入前瞻双点损失后，平均黑盒 ASR 从 64.31% 提升至 72.05%，白盒 ASR 从 91.72% 提升至 94.45%。这一增益源于前瞻损失联合优化当前重建 $x_1^t$ 与未来重建 $x_1^{t+\\Delta t}$ 的损失（Eq. 12），进一步降低了替代梯度在时域上的方差，使得攻击方向在概率流 ODE 轨迹上保持更一致的几何对齐（Theorem 4），从而在保持白盒强度的同时显著提升黑盒迁移性。

### 失败模式与边界条件

在 DiffPure 防御下 AdvFM 未能超越 APA，构成一个值得注意的边界条件。DiffPure 采用随机前向扩散与多步去噪的组合，其噪声注入机制可能部分抵消了流匹配扰动在流形切向方向上的集中优势。此外，当前实验均在 $\\ell_\\infty$ 约束下进行，未探索其他扰动范数下的行为。若实际部署中防御方采用更强的自适应净化策略（如动态调整扩散步数或噪声强度），AdvFM 的优势可能被削弱，这一点需要在实际应用中通过自适应评估进行验证。

### 补充图表

![[assets/figures/papers/paper_list_l836_https_openaccess_thecvf_com_content_CVPR2026_html_Liu_AdvFM_Lookahead_Fl/figures/002_Figure_1.jpg]]
*Figure 1: Qualitative comparison of adversarial examples on ImageNet under ResNet50*

## 方法谱系与知识库定位

### 1. 与扩散模型攻击范式的对比定位

AdvFM 的核心贡献在于将对抗攻击的扰动注入空间从扩散模型的像素重建域迁移至流匹配（Flow Matching）的连续时间速度场。这一范式转换直接回应了现有扩散攻击方法的结构性瓶颈：**随机噪声耦合导致替代梯度方差高，且逐步衰减因子削弱了攻击在噪声空间中的有效步长**。

与以下代表性扩散攻击基线相比，AdvFM 在四个关键维度上实现了系统性改进：

- **AdvDiffuser** (Chen et al., ICCV 2023) 和 **DiffPGD** (Xue et al., NeurIPS 2023) 均依赖扩散模型的反向去噪过程（Eq. 2–3），在重建图像 $x_0'$ 上执行 PGD 攻击。其核心缺陷在于：扩散重采样步引入的随机噪声 $\epsilon$ 使替代梯度 $\mathcal{G}_f^{\mathrm{Diff}}$ 具有高方差（Lemma 3），削弱了与目标模型梯度 $\mathcal{G}_g$ 的对齐。AdvFM 通过流匹配的确定性概率流 ODE 消除了这一随机源，使攻击方向的方差显著降低（Theorem 1, Eq. 23）。

- **DiffAttack** (Kang et al., NeurIPS 2023) 和 **AdvAD** (Li et al., NeurIPS 2024) 分别针对扩散净化防御设计了自适应攻击和非参数扰动策略，但其扰动传播仍受制于扩散过程的衰减因子 $\sqrt{\bar{\alpha}_t} < 1$（Eq. 4）。AdvFM 的速度场扰动更新（Eq. 8–9）将传播系数转换为放大因子 $\Delta t/(1-t) > 1$（Eq. 11），使得单步目标损失放大比显著大于扩散攻击（Lemma 1, Eq. 17），**这是黑盒迁移性提升的直接因果机制**。

- **APA** (Jiang et al., arXiv 2025) 作为最新的基于偏好对齐的扩散攻击方法，在 Table 1 中被用作最强基线。AdvFM 在四个替代模型（VGG19、ResNet50、ViT-B/16、Swin-B）上的平均黑盒 ASR 分别超出 APA 4.49、7.64、3.18 和 3.39 个百分点，验证了速度场攻击范式的跨架构优势。

### 2. 方法谱系中的关键创新节点

AdvFM 的方法设计可分解为三个递进的创新层次，每个层次对应一个明确的因果调控旋钮：

| 创新层次 | 基线状态 | AdvFM 方案 | 调控效应 |
|---------|---------|-----------|---------|
| **扰动注入空间** | 像素重建域（$x_0'$） | 速度场空间（$v_\theta$，Eq. 8） | 扰动传播从衰减变为放大（Eq. 11） |
| **状态演化动力学** | 扩散重采样（随机） | 欧拉推进（确定性，Eq. 9） | 消除随机噪声耦合，降低梯度方差（Lemma 3） |
| **优化目标** | 单点损失 | 前瞻双点损失（Eq. 12） | 沿概率流 ODE 对齐时域梯度，进一步降低方差（Theorem 4） |

其中，**前瞻损失（Lookahead Loss）** 是 AdvFM 在基础流匹配攻击之上的增量创新。通过联合优化当前时间步 $t$ 和前瞻时间步 $t+\Delta t$ 的重建损失（Eq. 12），该方法使攻击在沿 ODE 轨迹推进时保持梯度方向的一致性。Figure 2 的消融实验表明：引入前瞻损失后，黑盒平均 ASR 从 64.31% 提升至 72.05%，白盒 ASR 从 91.72% 提升至 94.45%，**证实了双点优化对梯度方差抑制的显著效果**。

### 3. 适用边界与防御鲁棒性分析

AdvFM 在以下防御场景中展现出差异化的鲁棒性，其适用边界可从理论分析中明确界定：

- **对抗净化防御（NRP、Smooth）**：AdvFM 表现优异。Theorem 3（Eq. 28）证明，流匹配扰动更集中于数据流形的切向方向，经净化算子 $P(\cdot)$ 处理后保留更多有效扰动能量。Table 2 中，AdvFM 在 NRP 防御上达到 94.98% ASR（超出 APA 13.8 个百分点），在 Smooth 防御上达到 81.35% ASR（超出 APA 11.1 个百分点），验证了这一理论优势。

- **DiffPure 扩散净化**：AdvFM 在此防御上出现性能下降（61.33% vs. APA 64.14%，差距 -2.81%）。**这一反直觉结果需要手动验证**：可能原因在于 DiffPure 本身使用扩散模型进行净化，其内部动力学与流匹配的速度场存在某种分布错配，削弱了切向扰动的保留优势。该点尚未在论文中获得理论解释，属于适用边界的明确限制。

- **对抗训练防御**：Theorem 2（Eq. 26）表明，流匹配攻击方向与鲁棒梯度 $\mathcal{G}_{\mathrm{rob}}$ 的对齐优于扩散攻击，这意味着 AdvFM 对对抗训练模型具有内在的迁移优势。Table 2 中对抗训练防御上的 ASR 提升（具体数值需查阅原表）与该理论预测一致。

### 4. 开放问题与后续工作方向

尽管 AdvFM 在理论和实验上均展现出显著优势，以下开放问题值得后续工作关注：

1. **DiffPure 防御的性能衰减机制**：流匹配扰动在 DiffPure 净化下的能量保留为何弱于预期？是否与速度场和扩散模型的分布假设冲突有关？该问题指向速度场攻击在混合防御场景下的理论边界。

2. **速度场模型的选择与泛化**：当前 AdvFM 使用预训练的流匹配模型 $v_\theta$，其质量直接影响攻击效果。不同流匹配架构（如 Rectified Flow、Conditional Flow Matching）对攻击迁移性的影响尚未被系统研究。

3. **前瞻损失的超参数敏感性**：Eq. 12 中的权重 $w$ 和前瞻步长 $\Delta t$ 的联合优化策略尚未被理论化，其在不同替代模型-目标模型组合下的最优配置可能具有任务依赖性。

4. **与基于分数的扩散模型的统一框架**：流匹配与分数匹配（Score Matching）在连续时间极限下具有等价性，AdvFM 的方法论是否可推广至基于分数的扩散攻击范式，形成统一的连续时间攻击框架，是值得探索的理论方向。

## 原文 PDF

![[paperPDFs/CVPR_2026/AdvFM_Lookahead_Flow_Matching_Velocity_Field_Attacks_for_Imperceptible_and_Transferable_Adversarial_Examples.pdf]]
