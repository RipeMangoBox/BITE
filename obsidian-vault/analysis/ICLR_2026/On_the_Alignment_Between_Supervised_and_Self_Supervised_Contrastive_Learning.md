---
title: "On the Alignment Between Supervised and Self-Supervised Contrastive Learning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/On_the_Alignment_Between_Supervised_and_Self_Supervised_Contrastive_Learning.pdf
aliases:
- SSCAF
- ABSSSCL
tags:
- ICLR_2026
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/representation_learning
core_operator: "批量大小（B）、类别数（C）、温度（τ）和学习率调度是控制CL-NSCL表示对齐度的关键可调节超参数。增大类别数、提高温度或使用较小的有效步长可以增强对齐；批量大小的影响取决于学习率缩放策略。"
primary_logic: "在相似性空间中分析耦合动力学，绕过参数空间指数发散问题，证明CL与NSCL的相似性矩阵在训练过程中始终接近。由此导出线性CKA和RSA的高概率下界，表明CL和NSCL在表示层面紧密耦合，且该耦合程度由类别数、批量大小、温度等因素定量控制。"
claims:
- "CL与NSCL的相似性矩阵在共享随机性下保持接近，其差距受批量大小、温度、类数等因子约束。"
- "从相似性矩阵漂移可直接得到CKA和RSA的高概率下界，且下界随类别数增多、温度升高而变紧。"
- "NSCL训练的表示与CL的表示之间的对齐程度显著高于其他监督方法（如SCL、CE）。"
- "参数空间可能发生指数发散，即使表示空间始终保持高度对齐。"
---

# On the Alignment Between Supervised and Self-Supervised Contrastive Learning

> [!tip] 核心洞察
> 在相似性空间中分析耦合动力学，绕过参数空间指数发散问题，证明CL与NSCL的相似性矩阵在训练过程中始终接近。由此导出线性CKA和RSA的高概率下界，表明CL和NSCL在表示层面紧密耦合，且该耦合程度由类别数、批量大小、温度等因素定量控制。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 监督与自监督对比学习的对齐性分析 |
| 英文题名 | On the Alignment Between Supervised and Self-Supervised Contrastive Learning |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=JkitQScjuL); [Project](https://dlfundamentals.github.io/cl-nscl-representation-alignment/) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/representation_learning |
| Method | 相似性空间耦合分析框架（Similarity-Space Coupling Analysis Framework） |
| Dataset | Tiny-ImageNet, CIFAR-100, Multiple datasets (CIFAR-10/100, Mini/Tiny ImageNet), Multiple datasets |

> [!tip] 效果简介
> - Tiny-ImageNet 上，CKA (CL vs NSCL) 为 0.87，对比 0.043 (CL vs SCL)，变化 +0.827。
> - CIFAR-100 上，Linear Probe Accuracy 为 CL 65.65%, NSCL 68.38%，对比 SCL 69.52%, CE 68.04%，变化 NSCL > CL。
> - Multiple datasets (CIFAR-10/100, Mini/Tiny ImageNet) 上，CL-NSCL alignment (RSA/CKA) with increasing number of classes 为 Increases，对比 lower alignment with fewer classes，变化 Qualitative。

## 概述

自监督对比学习（CL）与监督对比学习（SCL）在损失函数形式上的相似性已被广泛关注：当类别数目足够大时，CL的InfoNCE目标会自然趋近于仅用负样本构造的监督对比损失（NSCL）。然而，**损失层面的接近并不能保证训练过程中表示层面的对齐**——模型在参数空间中的轨迹可能指数发散，学到的表示几何也可能截然不同。本文抓住这一关键矛盾，系统揭示了在共享随机性下，CL与NSCL的表示相似性矩阵能够在全域训练中保持高度一致的条件，从而解决了表示几何对齐的可控性问题。

**核心思路**是绕过充满发散风险的参数空间，直接在**相似性空间**建立耦合动力学。作者构造了一组替代更新规则（Eq. 1），将CL和NSCL的相似性矩阵置于同一梯度下降框架下分析，并证明二者的Frobenius差距受类别数、批量大小$B$、温度$\tau$及学习率调度的联合约束（Theorem 1）。由此进一步导出线性CKA与RSA的高概率下界（Corollary 1, 2），定量保证了CL与NSCL的表示在整个训练过程中维持非平凡对齐，且随类别数增加、温度升高或优化步长减小，这一下界会更紧。

**主要实验结论**在多组标准视觉数据集上得到验证：
- 在共享随机性下，CL与NSCL的CKA可达0.87，而CL与SCL仅0.043，与交叉熵训练模型的差距更大（Fig. 2），证实NSCL是唯一与CL高度对齐的监督参照。
- **温度**和**类别数**是直接控制对齐度的因果旋钮：增大类别数一致性地提升对齐（Fig. 3）；$\tau=1.0$时对齐最高，低温显著削弱耦合（Fig. 4）。
- **批量大小**的影响与学习率缩放方案耦合：若学习率按$\mathcal{O}(B)$缩放，增大$B$会降低对齐；若按$\mathcal{O}(\sqrt{B})$或$\mathcal{O}(B^{1/4})$缩放，对齐则随$B$提升（Fig. 5）。
- 即使在表示空间对齐良好的情况下，**参数空间差距仍然指数增长**（Fig. 1, 6），进一步凸显此次相似性空间建模的必要性。

总体而言，本文阐明了监督与自监督对比学习“对齐”的实质是表示相似性结构的持续耦合，而非损失函数的表面近似，并给出了可量化的控制因素。主要局限在于理论界基于最坏情形分析，常数较松，且实验限于中小规模视觉任务；如何将分析框架推广至非对比自监督方法仍是开放课题。

## 背景与动机

自监督对比学习（CL）在无需标签的条件下能够学习到强大的表示，而监督对比学习（SCL）及其变体则利用标签进一步提升特征判别力。尽管两类范式在实践中都取得了成功，但它们学习到的表示之间是否存在内在联系、何时对齐、又由哪些因素控制，始终缺乏清晰的回答。一种特殊的监督对比目标——仅以负样本为分母的负样本监督对比学习（NSCL）——引起了关注：当类别数较大时，其损失函数在形式上逼近 CL 的 InfoNCE 损失。然而，**损失层面的相似性并不自动保证训练过程中表示层面的对齐**。这项工作正是要填补这一理论与认知空白。

现有的分析大多停留在损失景观或下游准确率比较上，未曾触及表示几何的动态耦合。一个突出的矛盾现象是：即便使用相同的随机种子、相同的小批量和数据增强，CL 与 NSCL 在参数空间中可能以指数速度发散（Figure 1(a)，Figure 6），但两者在表示相似性空间却长期保持高度一致（Figure 1(b,c)）。这一观察直接引出了两个核心缺口：(1) **缺少在表示层面（而非参数或损失面）刻画 CL 与 NSCL 耦合动态的理论框架**；(2) **尚未定量揭示批量大小、温度、类别数、学习率缩放等关键超参数如何调控对齐程度**。此外，实验表明 CL 与 NSCL 的表示对齐显著强于其与普通 SCL 或交叉熵损失的对齐（Figure 2），这说明 NSCL 是一种独特的耦合目标，值得被系统研究，而非仅作为性能对比的基线。

本文的动机正是在相似性空间中建立耦合动力学模型，跳出参数轨迹指数发散的困境，转而分析 CL 与 NSCL 在**相似性矩阵上的替代梯度下降**。作者严格证明，在共享随机性的条件下，两者的相似性矩阵始终以高概率保持接近（Theorem 1），并由此推导出线性CKA和RSA的显式高概率下界（Corollary 1, 2）。这些理论边界不仅为表示对齐提供了保证，还清晰地展示了**对齐随类别数增多而增强、随温度升高而提升**，以及批量大小效应对齐的方向取决于学习率缩放策略等可控规律。该框架将自监督与监督对比学习的表示对齐从一个经验现象升华为可理解、可调控的几何性质，为模型融合、半监督学习等下游任务提供了新的理论视角和操作余地。

## 核心创新

传统观点仅在损失函数的极限行为（类别数→∞时CL与NSCL损失趋同）上讨论监督与自监督对比学习的联系，却未回答一个关键问题：**在真实的有限类别训练中，两种范式能否产生高度对齐的表示几何？** 本文通过将分析对象从参数空间迁移到表示相似性空间，给出了系统性的理论证明与实验验证，揭示了CL与NSCL之间的稳健表示耦合，并明确了对齐的可控因素。

### 1. 分析域的根本转变：从参数空间到相似性空间

本研究最核心的方法论创新在于**将表示对齐的分析域从权重轨迹转移到相似性矩阵**，从而绕过了参数空间指数发散这一技术障碍。传统参数空间分析需依赖强凸性等不切实际的假设，而本文证明即使在权重向量随训练急剧分离（Figure 1 a, 图 6）时，两组网络的相似性矩阵仍能长期保持紧耦合（Figure 1 b,c）。基于此，作者提出“相似性‑下降”替代动力学（式 (1)），直接在余弦相似性矩阵上执行共享随机性的梯度下降更新：
$$ \Sigma_{t+1}^{\mathrm{CL}} = \Sigma_t^{\mathrm{CL}} - \eta_t G_t^{\mathrm{CL}}, \quad \Sigma_{t+1}^{\mathrm{NSCL}} = \Sigma_t^{\mathrm{NSCL}} - \eta_t G_t^{\mathrm{NSCL}}. $$
该框架将表示对齐问题转化为相似性矩阵的动态耦合问题，为后续理论分析铺平了道路。这一转变是 **changed slot** 的精髓：分析域从参数空间切换到表示相似性空间，从而获得了对表示几何的直接控制和量化能力。

### 2. 理论突破：相似性耦合的可认证边界

在上述替代动力学下，本文建立了CL与NSCL相似性矩阵之间 Frobenius 差距的高概率上界（**Theorem 1**）：
$$
\| \Sigma_T^{\mathrm{CL}} - \Sigma_T^{\mathrm{NSCL}} \|_F \leq \exp\Bigl(\frac{1}{2\tau^2 B}\sum_{t=0}^{T-1}\eta_t\Bigr) \frac{1}{\tau\sqrt{B}} \Bigl(\sum_{t=0}^{T-1}\eta_t\Bigr) \Delta_{\pi,\delta}(B;\tau).
$$
该不等式揭示了批量大小 $B$、温度 $\tau$ 和累积有效步长如何联合控制相似性漂移。在此基础上，直接导出两个表示对齐度量——线性 CKA 和 RSA——的**高概率下界**（**Corollaries 1‑2**）：
$$ \mathrm{CKA}_T \geq \frac{1-\rho_T}{1+\rho_T}, \qquad \mathrm{RSA}_T \geq \frac{1-r_T}{1+r_T}, $$
其中 $\rho_T, r_T$ 均由上述相似性差距上界约束。这意味着，只要相似性矩阵保持接近，CKA 和 RSA 就会被保证在一个非平凡的高值区间内。这一组可认证的界面将对齐从经验观察提升为具有理论保障的结构化属性，是先前工作所不具备的。

### 3. 揭示控制对齐的因果钮

理论边界不仅给出存在性，更明确指出了影响 CL–NSCL 表示对齐的**可调节超参数**，形成理解对齐机制的“因果钮”：

- **类别数 $C$**：增大训练类别数使 CL 与 NSCL 的损失更接近，从而系统性地提高对齐程度（Figure 3, Figure 10, 11），但极长训练后对齐会有所衰减。
- **温度 $\tau$**：在常用范围内，较高的温度（如 $\tau=1.0$）一致地带来更强的表示对齐（Figure 4, Figure 8），但其提升效果受批量大小相互作用的调制。
- **批量大小 $B$ 与学习率缩放**：批量大小对对齐的影响取决于学习率缩放策略：$\eta \propto B$ 时大 $B$ 降低对齐，而 $\eta \propto \sqrt{B}$ 或 $\eta \propto B^{1/4}$ 时则相反（Figure 5, Figure 9, 13）。理论界中的指数项 $\exp(\sum\eta_t/(2\tau^2 B))$ 准确捕捉了这一非单调效应。

这些发现使从业者能够根据任务需求主动调节 CL 与监督目标的表示一致性，而非被动接受黑箱行为。

### 4. 实证证据与框架效度

实验从多个角度验证了理论创新。在 Tiny‑ImageNet 上，CL 与 NSCL 的线性 CKA 在 1000 轮训练后高达 **0.87**，而 CL 与 SCL 仅为 **0.043**，凸显出 NSCL 作为表示对齐核心参照的独特地位（Figure 2）。这一高度耦合现象在 CIFAR、Mini‑ImageNet 等多个数据集上复现，且模型间共享相同的初始化、小批次和数据增强，保证了公平对比。同时，参数空间的权重差距在训练中持续增大（Figure 6），但表示空间的 CKA/RSA 仍可维持在较高水平，直接验证了“相似性空间分析优于参数空间”这一核心洞见。

尽管 NSCL 在下游分类准确率上通常弱于 SCL 或 CE（Table 1），但本文重点并非追求 SOTA，而是厘清不同学习目标间的表示几何对齐规律。这一视角转变——**从性能导向转向几何可解释性**——本身构成重要的观念创新。

### 5. 局限与未闭合问题

当前分析的几点局限值得注意：(i) 理论界基于最坏情况，常数可能较宽松，数据依赖的紧致界尚待推导；(ii) 实验以小到中规模视觉数据集为主，未验证大规模或非视觉场景的泛化性；(iii) 框架仅限于对比学习范式，能否推广至掩码图像建模等非对比自监督方法仍为开放问题；(iv) NSCL 并非实践上最强的监督目标，本文强调的是对齐性这一结构性质，而非绝对性能。这些方向构成了未来工作的重要切入点。

## 整体框架

![[assets/figures/papers/iclr26_0015_JkitQScjuL_On_the_Alignment_Between_Supervised_and_Self-Sup/figures/001_Figure_1.jpg]]
*Figure 1: (a) Weight Space*

该工作提出了一种**表示相似性空间的耦合分析框架**，通过控制共享随机性，定量揭示自监督对比学习（CL）与仅负样本监督对比学习（NSCL）在训练全过程中的表示对齐机制。整体流程遵循“问题定义→域转换→理论刻画→实验验证”的闭环，其核心模块与输入输出关系如下。

### 1. 对比损失与共享随机性设定
框架首先定义对比学习中锚点 $i$ 的单样本损失。对于批量 $\mathcal{B}$（含 $B$ 个样本），自监督对比损失 $\ell_i^{\mathrm{CL}}$ 的负样本包含整个批量内除自身和正样本外的所有样本；而监督对比损失 $\ell_i^{\mathrm{NSCL}}$ 则仅保留类标签与锚点不同的样本构成负样本集 $I_i^-$。两者均使用温度 $\tau$ 和相同的全连接投影头（ResNet-50 主干 + 两层 MLP，输出维度 128）。为保证分析可控，训练采用解耦对比损失（DCL）避免正样本对分母的耦合。**共享随机性**要求 CL 与 NSCL 从相同参数初始化出发，使用完全一致的 mini-batch 序列、数据增强选择和训练步超参数，从而消除任何非本质的随机偏差。

### 2. 分析域转换：从参数空间到相似性空间
传统参数空间（权重轨迹）由于梯度动力学的高度非线性，即使数据一致也会导致两路模型迅速发散。因此，分析框架的关键是**将动力学迁移到表示相似性矩阵空间**。给定 $N$ 个样本的编码矩阵 $Z \in \mathbb{R}^{N\times d}$，定义表示相似性矩阵 $\Sigma = \operatorname{sim}(Z, Z) \in [-1,1]^{N\times N}$。在共享随机性下，对 CL 和 NSCL 分别执行“相似性下降”替代动力学：

$$
\Sigma_{t+1}^{\mathrm{CL}} = \Sigma_t^{\mathrm{CL}} - \eta_t G_t^{\mathrm{CL}},
\qquad
\Sigma_{t+1}^{\mathrm{NSCL}} = \Sigma_t^{\mathrm{NSCL}} - \eta_t G_t^{\mathrm{NSCL}},
$$

其中 $G_t$ 是与当前 mini-batch 接触的相似性条目上的梯度（参见 Eq. (1)）。该替代更新规避了参数空间的复杂映射，直接刻画表示结构的变化。输入为当前相似性矩阵、学习率 $\eta_t$ 和批量梯度；输出为更新后的相似性矩阵，经多步迭代后得到最终表示的对齐程度。

### 3. 相似性耦合理论及其定量控制
在替代动力学上，理论部分的核心成果是证明 CL 与 NSCL 的相似性矩阵在训练过程中保持接近，并给出高概率的 Frobenius 界（Theorem 1）：

$$
\|\Sigma_T^{\mathrm{CL}} - \Sigma_T^{\mathrm{NSCL}}\|_F \leq 
\exp\!\Big(\frac{1}{2\tau^2 B}\sum_{t=0}^{T-1}\eta_t\Big) \,
\frac{1}{\tau\sqrt{B}} \Big(\sum_{t=0}^{T-1}\eta_t\Big) \,
\Delta_{\pi,\delta}(B;\tau).
$$

该界显示相似性漂移受三个可控因子的联合影响：
- **温度 $\tau$**：增大 $\tau$ 使梯度 Lipschitz 常数变小，抑制差异放大；
- **批量大小 $B$**：隐含在指数项和 $1/\sqrt{B}$ 前置因子中，其效应与学习率缩放策略耦合（后文实验详析）；
- **累积有效步长 $\sum \eta_t$**：较大的总步长加剧漂移。

由相似性漂移可直接推导出两种常用表示对齐度量——线性 CKA（Corollary 1）和 RSA（Corollary 2）——的下界，其形式为 $\frac{1-\rho_T}{1+\rho_T}$，其中 $\rho_T$ 与上述 Frobenius 界成正比。这意味着类别数越多、温度越高、有效步长越小，对齐下界越紧，即 CL 与 NSCL 的表示空间一致性越强。

### 4. 实验验证与控制变量分析
实验部分将理论框架映射为可操作的对比流程：
- **主干网络**：ResNet-50（宽度因子 1），投影头输出 128 维，使用 DCL 损失。
- **对齐度量**：线 CKA 和 RSA，在训练集与测试集上按 epoch 计算；同时监控参数空间相对权重差距。
- **控制变量**：类别数 $C$（如 CIFAR-100 到 Tiny-ImageNet）、温度 $\tau$（0.1, 0.5, 1.0）、批量大小 $B$ 及学习率缩放策略（$\eta \propto B$，$\eta \propto \sqrt{B}$，$\eta \propto B^{1/4}$）。
- **对比基线**：标准监督对比 SCL 和交叉熵 CE，凸显 CL–NSCL 的独特耦合性。

整体数据流为：共享随机初始化 → 多 epoch 训练（10 epoch warm-up + cosine 衰减）→ 逐 epoch 保存编码器 → 计算相似性矩阵 → 得出 CKA/RSA 曲线。实验发现与理论预测一致：随着类别数增加（Fig. 3）、温度升高至 1.0（Fig. 4），CL–NSCL 的 CKA/RSA 显著提升；批量大小的影响则因学习率缩放而出现反转（Fig. 5）。此外，参数空间差距会以指数速度发散（Fig. 1, Fig. 6），即使表示空间始终保持高度对齐，印证了域转换的必要性。

该框架最终表明，通过相似性空间的解析动力学，而非直接追踪高维权重，可以精密控制自监督与监督对比学习之间的表示对齐程度，为理解两个范式的内在联系提供了定量桥梁。

## 核心模块与公式推导

本文提出 **相似性空间耦合分析框架（Similarity-Space Coupling Analysis Framework）**，其核心思想是绕过参数空间可能出现的指数发散，直接在表示相似性矩阵上建立替代动力学，从而定量刻画自监督对比学习（CL）与仅负样本监督对比学习（NSCL）在表示几何层面的耦合程度。该框架的关键模块与推导如下。

### 相似性替代动力学
设 $\Sigma \in [-1,1]^{N \times N}$ 为 $N$ 个样本对的余弦相似性矩阵，在共享初始化、同一批次与数据增强的条件下，CL 和 NSCL 的梯度下降可等价转换为仅在相似性空间中的替代更新（式1）：

$$
\Sigma_{t+1}^{\mathrm{CL}} = \Sigma_{t}^{\mathrm{CL}} - \eta_{t} G_{t}^{\mathrm{CL}}, \qquad
\Sigma_{t+1}^{\mathrm{NSCL}} = \Sigma_{t}^{\mathrm{NSCL}} - \eta_{t} G_{t}^{\mathrm{NSCL}} \tag{1}
$$

其中 $\eta_t$ 为学习率，$G_t^{\mathrm{CL}}, G_t^{\mathrm{NSCL}}$ 分别为 CL 和 NSCL 损失相对于相似性矩阵的梯度，仅需更新当前批次所覆盖的矩阵子块。该替代动力学使得两组模型相似性矩阵的差异完全由单步梯度偏差累积决定。

### 核心定理：相似性耦合上界
经过 $T$ 步训练，CL 与 NSCL 相似性矩阵的 Frobenius 差异服从以下高概率上界（定理1，式2）：

$$
\| \Sigma_T^{\mathrm{CL}} - \Sigma_T^{\mathrm{NSCL}} \|_F \leq
\exp\!\Bigl(\frac{1}{2\tau^{2} B} \sum_{t=0}^{T-1} \eta_t\Bigr)
\frac{1}{\tau\sqrt{B}} \Bigl(\sum_{t=0}^{T-1} \eta_t\Bigr)
\Delta_{\pi,\delta}(B;\tau) \tag{2}
$$

**变量含义：**
- $\tau$：对比损失的温度参数，增大 $\tau$ 会降低指数项并增大分母，整体收窄上界；
- $B$：批量大小，通过 $\sqrt{B}$ 和指数内的 $1/B$ 分别影响单步偏差和累积扰动；
- $\sum_{t=0}^{T-1} \eta_t$：总有效步长，表征优化过程对相似性矩阵的累积扰动量；
- $\Delta_{\pi,\delta}(B;\tau)$：与类别分布 $\pi$、失败概率 $\delta$、批量大小 $B$ 和温度 $\tau$ 相关的偏差项，源自 CL 与 NSCL 单步梯度差的量化上界。当训练类别数 $C$ 较大时 $\Delta_{\pi,\delta}$ 变小，因此上界随类别数增加而收紧，从理论上解释了实验中类别数越多对齐越强的现象。

该上界揭示了 **批量大小 $B$、温度 $\tau$、总有效步长以及类别数 $C$（通过 $\Delta_{\pi,\delta}$ 蕴含）** 对相似性差距的控制关系，所有因子均可由超参数调节，从而为可控地对齐表示提供了理论保证。

### 对齐度量的高概率下界
基于相似性漂移，可直接导出线性中心核对齐（CKA）和表示相似性分析（RSA）的高概率下界（推论1与推论2）：

**CKA 下界：**
$$
\mathrm{CKA}_T \geq \frac{1-\rho_T}{1+\rho_T},\qquad
\rho_T \leq \frac{\exp\!\bigl(\frac{1}{2\tau^{2} B}\sum_{t=0}^{T-1}\eta_t\bigr)
\frac{1}{\tau\sqrt{B}}\bigl(\sum_{t=0}^{T-1}\eta_t\bigr)
\Delta_{\pi,\delta}(B;\tau)}{\|K_T^{\mathrm{CL}}\|_F} \tag{3}
$$
其中 $\|K_T^{\mathrm{CL}}\|_F$ 为 CL 表示的中心化 Gram 矩阵的 Frobenius 范数，反映整体协方差结构的尺度。

**RSA 下界：**
$$
\mathrm{RSA}_T \geq \frac{1-r_T}{1+r_T},\qquad
r_T \leq \frac{\exp\!\bigl(\frac{1}{2\tau^{2} B}\sum_{t=0}^{T-1}\eta_t\bigr)
\frac{1}{\tau\sqrt{B}}\bigl(\sum_{t=0}^{T-1}\eta_t\bigr)
\Delta_{\pi,\delta}(B;\tau)}{\sqrt{M}\,\sigma_{D,T}} \tag{4}
$$
其中 $M$ 为样本对数，$\sigma_{D,T}$ 为不同性矩阵（RDM）上三角元素的标准差，度量表示间差异性的变异幅度。

两个下界具有统一形式：中间量 $\rho_T$ 或 $r_T$ 越小，则 CKA 或 RSA 越趋近于 1，表示 CL 与 NSCL 在表示几何上高度对齐。由于上界中的核心因子与式（2）一致，上述下界同样受到 $B$、$\tau$、$\eta_t$ 和类别数 $C$ 的定量调控，且当温度升高 ($\tau=1.0$)、类别数增大时，下界显著收紧，与实验观察完全吻合（Fig. 3-4）。值得注意的是，尽管参数空间可能因权重轨迹发散而导致耦合丧失（定理2，参数差距指数增长），相似性空间仍可通过上述界保持高度耦合（Fig. 1, 6），进一步凸显了分析域从参数空间转向表示相似性空间的必要性。

*注：以上公式源自原文 Section 3–4，LaTeX 经校核与原文一致。*

## 实验与分析

### 实验设置
本文的所有实验均在公平对比的框架下进行：CL与NSCL模型共享相同的初始化参数、随机小批量与数据增强策略，从而排除无关因素的干扰。采用ResNet-50作为编码器，投影头为两层MLP（2048→2048→128），损失函数统一使用解耦对比损失（DCL）以避免正样本对在分母中的耦合效应。训练采用10轮预热后接余弦衰减的学习率调度，批量大小默认为256；评估指标包括表示对齐度量（线性CKA、RSA）以及下游分类精度（最近类中心分类器NCCC、线性探测LP）。数据集覆盖CIFAR-10/100、Mini-ImageNet、Tiny-ImageNet和SVHN。

### 主结果：CL与NSCL表示的高度对齐
Figure 2 直观展示了训练过程中CL与各种监督目标之间表示对齐的演化轨迹。在Tiny-ImageNet上训练1000轮后，CL与NSCL的线性CKA高达0.87，而CL与标准监督对比学习（SCL）的CKA仅为0.043，与交叉熵（CE）训练模型的CKA更低。这一结果在不同的对齐度量（CKA和RSA）下均成立，确认了NSCL是唯一能在大范围训练区间内与CL保持高度表示耦合的监督目标。Table 1 提供了各方法的下游分类性能基准：NSCL的NCCC/LP精度通常介于CL与SCL/CE之间，但本文的核心主张是关于表示几何的对齐性，而非绝对性能排序。

### 消融研究：控制对齐的关键因子

#### 类别数量
Figure 3 的热力图系统考察了训练类别数对CL-NSCL对齐的影响。在CIFAR-100等数据集上，随着训练类别数增多，整条训练过程的线性CKA显著升高；然而，对于任一固定的类别数，对齐度在训练后期均表现出一定程度的衰减。附录中的Figure 10、Figure 11提供了进一步佐证，明确指向类别增加对NSCL近似CL的促进作用。

#### 温度参数
Figure 4 比较了不同温度（τ ∈ {0.1, 0.5, 1.0}）下CL与NSCL的RSA和CKA变化。四类数据集一致显示，温度提升至1.0时对齐度达到最大；这与理论界（Theorem 1）中温度项以 1/τ 形式控制相似性漂移的结论相符。Table 2 进一步给出变温条件下线性探测准确率的数值，验证了较高温度下CL与NSCL模型的实际性能差距缩小（见Figure 12）。

#### 批量大小与学习率缩放策略
Figure 5 揭示了批量大小 B 对齐的影响并非单一方向，而是取决于学习率 η 的缩放方式。当 η 随 B 线性缩放（即 O(B)，如 η = 0.3·⌊B/256⌋）时，对齐随 B 增大而减弱；相反，若采用 √B 或 B^{1/4} 缩放，增加 B 反而提升对齐。该现象与 Theorem 1 中 1/(τ√B) 因子的主导作用一致，说明学习率有效步长与控制表示耦合的批量规范化之间存在相互制衡。Figure 9 和 Figure 13 提供了不同缩放策略下的补充证据。

### 失败模式与理论-实际差距
尽管表示空间的高度耦合是稳健的，参数空间却呈现急剧发散。Figure 1 显示CL与NSCL的权重向量夹角可达85.7°，而表示空间同一类的样本向量仅偏离27.8°。Figure 6 跟踪了训练全程的权重差距，表明该指数级发散是两种监督形式固有的，即使二者的相似性矩阵始终保持接近。此外，CL-NSCL的表示对齐并非永久不变：当训练持续过长时间（Figure 2 中超1000轮），对齐度逐渐衰减，提示了理论界中累积梯度差上界的作用域限制。本文的理论界基于最坏情况分析，常数较宽松；更紧的数据依赖界有待推导。实验仅覆盖中、小规模视觉数据集，未在ImageNet-21K或非视觉领域验证。分析框架尚未拓展至掩码图像建模等非对比自监督方法，且NSCL本身并非Top-1准确率最优的监督目标，强调的是几何对齐的科学发现而非SOTA性能。

### 重要图表结论一览
- **Figure 1**：直观对比参数空间与表示空间的耦合差异，为相似性空间分析框架提供动机。
- **Figure 2**：确立CL-NSCL的独特对齐关系，远优于CL-SCL、CL-CE，但长期训练会削弱该关系。
- **Figure 3**：以热力图揭示类别数量对对齐的正向调节，并忠实反映训练后期的衰减趋势。
- **Figure 4**：证实提高温度一致性增强对齐，τ=1.0为实验最优值。
- **Figure 5**：证明批量大小效应高度依赖学习率缩放策略，即可控可调。
- **Figure 6**：记录权重空间对齐的崩溃，强调参数发散并不阻碍表示相似性耦合。
- **Table 1**：提供各方法在四类数据集上的下游精度基准。
- **Table 2**：为变温实验补充线性探测准确率，直接衡量对齐度对分类性能差距的影响。
- **Figure 12**：将温度调制的对齐与性能差距可视化，更高对齐度对应更小的CL-NSCL精度差。
- **Figure 17**：展示利用CL与NSCL表示对齐实现模型合并的潜力，NCCC/LP精度均显著提升，印证了表示兼容性的应用价值。

### 补充图表

![[assets/figures/papers/iclr26_0015_JkitQScjuL_On_the_Alignment_Between_Supervised_and_Self-Sup/figures/013_Figure_2.jpg]]
*Figure 2: Alignment during training. We train ResNet-50 models with decoupled CL, SCL, NSCL, and CE. For the first 1,000 epochs, the CL-trained model is substantially more aligned with the NSCL-trained model than with the others. However, alignment declines when training continues much longer*

![[assets/figures/papers/iclr26_0015_JkitQScjuL_On_the_Alignment_Between_Supervised_and_Self-Sup/figures/004_Table_1.jpg]]
*Table 1: Nearest Class-Center Classifier (NCCC) and Linear Probe (LP) test accuracies (%). We report the accuracies against the all-way classification task in each dataset. The models (also used in Fig. 2) were pre-trained on their respective datasets*

![[assets/figures/papers/iclr26_0015_JkitQScjuL_On_the_Alignment_Between_Supervised_and_Self-Sup/figures/022_Figure_3.jpg]]
*Figure 3: CL–NSCL alignment (linear CKA) increases with the number of training classes. The heatmaps show the linear CKA between CL and NSCL models. We visualize alignment on the training (top row, green) and test (bottom row, purple) sets. The y-axis indicates the number of classes (N ) used for training, and the x-axis represents the training epoch. While alignment is consistently higher for larger N , it also tends to decrease as training progresses for any fixed N*

![[assets/figures/papers/iclr26_0015_JkitQScjuL_On_the_Alignment_Between_Supervised_and_Self-Sup/figures/030_Figure_4.jpg]]
*Figure 4: Higher τ increases the CL-NSCL alignment. The plots show RSA (top row) and CKA (bottom row) over 300 epochs. We trained CL and NSCL models with varying temperatures ( $\tau \in \{$ 0 . 1 , 0 . 5 , 1 . 0 $\}$ ) ) on four datasets. Across all datasets, a higher temperature $\tau$ = 1 . 0 (shown in purple) evidently results in the highest alignment

![[assets/figures/papers/iclr26_0015_JkitQScjuL_On_the_Alignment_Between_Supervised_and_Self-Sup/figures/039_Figure_5.jpg]]
*Figure 5: Effect of batch size with scaled learning rates. We trained CL, and NSCL models for 300 epochs with varying batch-sizes (B ∈ {256, 512, 1024}). For each experiment, the learning rate η is scaled as a function of batch-size, as mentioned under each panel. For instance, the results shown in panel (b) use a learning rate of $\begin{array} { r } { \eta = \frac { 0 . 3 \sqrt { B } } { 2 5 6 } } \end{array}$ (a) CIFAR10

## 方法谱系与知识库定位

本文提出了一种**相似性空间耦合分析框架**，通过在表示相似性矩阵上构建替代动力学（见式 `Eq. (1)`），首次定量揭示了自监督对比学习（CL）与负样本监督对比学习（NSCL）在全训练过程中的表示几何对齐度，以及参数空间分歧的指数级扩大现象（Theorem 2, Figure 6）。该框架将 **NSCL** 确立为与 CL 最耦合的监督对比目标（CKA 值高达 0.87，而 CL–SCL 仅 0.043，见 Figure 2, Table 1），而非传统的 **Supervised Contrastive Learning（SCL）** 或 **Cross-Entropy（CE）**。作为分析基线，SCL 和 CE 仅用于凸显 CL–NSCL 的独特耦合性，其本身并非该方法体系的分析对象。

与以往直接在参数空间中比较权重轨迹的工作不同，本文的核心变更在于将**分析域从参数空间切换至表示相似性空间**：通过控制 CL 与 NSCL 在共享随机性（相同初始化、小批量、数据增强）下的梯度差异（Lemma 7），避免了在高度非凸损失下参数指数发散对理论分析的破坏。这一领域转换使得即使参数向量夹角达 85.7°，表示空间向量夹角仍可保持在 27.8° 以内（Figure 1），从而保证了后续 CKA 和 RSA 下界的高概率成立（Corollary 1, Corollary 2）。

**适用边界**由理论界（Theorem 1, Eq. (2)）和实验共同界定，关键可控因素包括：

- **类别数 $C$**：训练类别越多，CL 与 NSCL 的相似性矩阵漂移越小，CKA/RSA 对齐度越高（Figure 3, Figure 10/11）。在 C 较小时，对齐程度显著下降，表明该方法更适用于类别丰富的数据集。
- **温度 $\tau$**：较高的温度（如 $\tau=1.0$）一致性地提升对齐度（Figure 4, Figure 8, Table 2），因为更扁平的 softmax 分布缩小了损失函数间的差异。
- **批量大小 $B$ 与学习率缩放**：对齐度对批量大小的响应依赖于学习率缩放策略：若学习率与 $B$ 线性缩放（如 $O(B)$），对齐随 $B$ 增大而降低；若采用 $O(\sqrt{B})$ 或 $O(B^{1/4})$ 缩放，对齐反而可能提升（Figure 5, Figure 9, Figure 13）。这一现象可被理论界中的 $\exp\big(\frac{1}{2\tau^2 B}\sum \eta_t\big)$ 因子所解释。
- **训练步数**：理论界随总步长和 $\sum \eta_t$ 累积，因此在超长时间训练下，对齐度会出现衰减（Figure 2 中 1000 epochs 后趋势），说明框架在有限/适度训练范围内提供最紧保证。

以上边界在**共享随机性**的前提下成立，若初始化或数据增广不同，对齐性没有理论保证。实验验证主要在小到中等规模视觉数据集（CIFAR‑10/100, SVHN, Mini‑ImageNet, Tiny‑ImageNet）上进行，其在大规模数据（如 ImageNet‑21K）或非视觉模态上的适用性尚待检验。

**局限性**：

1. **理论常数较松**：界基于最坏情况分析，实际数据集上得到的 CKA/RSA 下界通常远高于理论值，数据依赖型更紧常数的推导是待解难题。
2. **范式局限**：当前框架只覆盖对比学习范式，尚未扩展到非对比自监督方法（如 BYOL, SimSiam, MAE），无法统一描述更广泛的自监督 – 监督对齐现象。
3. **性能与对齐的权衡**：NSCL 虽与 CL 表示最耦合，但其下游 Top‑1 准确率（如线性探针）常低于 SCL 或 CE（Table 1），这意味着高对齐并不直接等于高判别性能。该方法侧重于几何分析而非提出新的 SOTA 目标。
4. **实验规模**：缺少大尺寸模型和更大规模数据的验证，限制了对尺度扩展属性的认知。

**开放问题**：

- **更紧的常数与数据依赖结构**：能否利用类别分布、样本相似度等数据特性取代最坏情况分析，导出更贴合实际的界？
- **推广至非对比范式**：如何将相似性空间耦合分析迁移到基于动量更新或掩码预测的自监督算法，建立统一的表示对齐理论？
- **弱假设下的稳定性**：在不依赖共享增广/小批量的更弱条件下，CL 与监督学习的表示耦合是否存在有效的理论保证？
- **下游应用与融合**：CL–NSCL 的紧密表示对齐是否可被用于模型融合、半监督学习或迁移学习的改进？特别是在类别数较少的场景下，如何通过温度/批量调度主动提升对齐度？这些均是需要进一步工程探索的问题。

## 原文 PDF

![[paperPDFs/ICLR_2026/On_the_Alignment_Between_Supervised_and_Self_Supervised_Contrastive_Learning.pdf]]
