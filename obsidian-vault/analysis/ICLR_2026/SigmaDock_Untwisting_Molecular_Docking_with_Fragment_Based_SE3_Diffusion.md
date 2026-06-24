---
title: "SigmaDock: Untwisting Molecular Docking with Fragment-Based SE(3) Diffusion"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/SigmaDock_Untwisting_Molecular_Docking_with_Fragment_Based_SE3_Diffusion.pdf
openreview_forum_id: Vgm77U4ojX
aliases:
- SigmaDock
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/chemistry_and_drug_discovery
core_operator: "将配体分解为刚体片段，在乘积空间 SE(3)^m 上进行独立扩散，消除几何纠缠，使扩散过程可分解且易于学习。"
primary_logic: "利用结构化学中构象流形的性质，将分子对接转化为预测各刚体片段的 SE(3) 变换；在 SE(3)^m 上定义扩散具有分解的乘积 Haar 测度，避免了扭角扩散的纠缠，并通过三角边约束和片段归并（FR3D）保持化学合理性并降低自由度。"
claims:
- "SIGMADOCK 在 PoseBusters 集上达到 79.9% 的 Top-1 成功率 (RMSD < 2 & PB-valid)，远超先前深度学习方法（12.7–32.8%）"
- "移除三角化约束使 PB-validity 下降 12.8%（消融实验）"
- "扭角参数化产生非乘积基测度，而片段参数化产生乘积 Haar 测度，使学习问题更简单"
- "SIGMADOCK 在未见蛋白上泛化良好，在大多数序列相似度区间匹配或超越 AlphaFold3，且训练数据仅为其 1/20"
---

# SigmaDock: Untwisting Molecular Docking with Fragment-Based SE(3) Diffusion

> [!tip] 核心洞察
> 利用结构化学中构象流形的性质，将分子对接转化为预测各刚体片段的 SE(3) 变换；在 SE(3)^m 上定义扩散具有分解的乘积 Haar 测度，避免了扭角扩散的纠缠，并通过三角边约束和片段归并（FR3D）保持化学合理性并降低自由度。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | SigmaDock: 基于片段的SE(3)扩散模型解析分子对接 |
| 英文题名 | SigmaDock: Untwisting Molecular Docking with Fragment-Based SE(3) Diffusion |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=Vgm77U4ojX) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/chemistry_and_drug_discovery |
| Method | SIGMADOCK |
| Dataset | PoseBusters, PoseBusters (sequence similarity split) |

> [!tip] 效果简介
> - PoseBusters 上，Top-1 (RMSD < 2 & PB-valid) 为 79.9%，对比 12.7%–32.8% (reported by recent deep learning approaches, e.g. DiffDock)，变化 +67.1% absolute improvement。
> - PoseBusters (sequence similarity split) 上，Top-1 (PB-valid) across similarity bins 为 [0,30): 72%; [30,95): 79%; [95,100]: 87%，对比 AlphaFold3 reported: [0,30): 87%; [30,95): 82%; [95,100]: 78% (with different train-test leakage)，变化 SIGMADOCK outperforms AF3 on [95,100] and is competitive overall despite far less data。

## 概述

分子对接——预测配体在蛋白质结合口袋中的三维结合姿态——是结构药物设计的核心任务。传统物理对接工具受限于评分函数的精度，而近期深度学习方法（如基于扭角扩散的 DiffDock）虽然在部分场景取得进展，却面临一个根本性瓶颈：**扭角参数化在笛卡尔空间中诱导出高度非线性、非局部的几何耦合，导致学习目标复杂、采样不稳定**。具体而言，从扭角空间到笛卡尔坐标的映射使得诱导测度不再具有乘积结构，扩散过程难以分解，评分网络需要隐式地学习复杂的几何纠缠关系。

SIGMADOCK 的核心思路是**从根本上消除这种几何纠缠**：将配体沿可旋转键分解为若干刚体片段，在乘积空间 $\mathrm{SE}(3)^m$ 上对每个片段独立地进行扩散。这一参数化将生成任务转化为预测各片段的刚体变换，避免了扭角的显式建模，同时利用乘积 Haar 测度的因子分解性质使扩散过程天然可分解。为了保持化学合理性，方法引入**三角化距离约束**固定相邻键角和扭键长度，同时不限制二面角的变化；并通过**片段归并算法（FR3D）**随机搜索合并相邻片段，降低自由度并消除冗余虚拟原子。

在 PoseBusters 基准上，SIGMADOCK 取得了 **79.9% 的 Top-1 成功率**（RMSD < 2 Å 且通过物理化学有效性检查），远超先前深度学习方法报告的 12.7%–32.8%，并匹配或超越了传统对接工具。消融实验证实了各设计组件的关键作用：移除三角化约束使有效性下降 12.8%，移除蛋白质-配体交互边使 RMSD 指标崩溃至 10.3%，而片段归并和评分策略均有显著贡献。在按序列相似度分层的泛化分析中，SIGMADOCK 在未见蛋白上表现稳健，在高相似度区间（[95,100]）甚至超越 AlphaFold3，且训练数据仅为其约 1/20。

**方法定位**：SIGMADOCK 是一种基于片段的 SE(3) 扩散模型，通过结构化学先验将分子对接重新表述为乘积空间上的可分解生成问题，绕开了扭角扩散的固有困难。其核心贡献在于**利用构象流形的几何性质设计扩散空间**，而非仅仅改进网络架构或评分函数。

## 背景与动机

### 分子对接的核心挑战

分子对接是计算药物发现中的核心任务，其目标是预测小分子配体在蛋白质结合口袋中的三维结合姿态。从物理化学角度看，对接问题的本质是搜索配体构象空间中的低能态——配体的结合构象遵循 Boltzmann 分布，概率质量集中在由键长、键角等完整约束所定义的构象流形 $\mathcal{M}_c$ 上：

$$\mathcal{M}_c = \{ \mathbf{x}_c \in \mathbb{R}^{|\mathcal{G}_{\mathrm{ligand}}|\times 3} : g(\mathbf{x}_c) \approx 0 \}$$

该流形编码了局域守恒的几何先验，包括固定的键长 $d_{AB} = d_0$ 和键角 $\tau_{ABC} = \tau_0$，但明确排除了可自由旋转的二面角（可旋转键）。这意味着配体构象变化的主要来源是绕可旋转键的二面角变化（图2），而各刚性片段内部的几何结构基本固定。

### 现有深度学习方法的关键瓶颈

近年来，基于扩散模型的深度学习方法在分子对接领域展现出潜力，其中最具代表性的是扭角扩散模型。这类方法将配体姿态参数化为全局 SE(3) 位姿与 $k$ 个二面角的组合，在乘积空间 $\mathrm{SE}(3) \times \mathbb{T}^k$ 上定义扩散过程。

然而，这种参数化存在根本性的几何缺陷：**从扭角空间到笛卡尔坐标的映射是高度非线性且非局部的**。具体而言，改变一个二面角会导致配体远端原子的大幅位移，使得不同扭角之间产生复杂的几何纠缠。这种纠缠在测度层面表现为诱导测度的非乘积结构——扭角空间上的乘积分布映射到笛卡尔空间后，其 Gram 行列式无法分解为各自由度独立因子的乘积。这导致两个严重后果：

1. **学习目标复杂化**：评分网络需要隐式学习这种非线性耦合关系，训练动力学不佳；
2. **采样不稳定**：反向扩散过程中，各自由度无法独立去噪，采样效率低下。

实证结果印证了这一问题：以 DiffDock 为代表的扭角扩散模型在 PoseBusters 基准上的 Top-1 成功率（RMSD < 2Å 且通过物理化学有效性检查）仅为 12.7%–32.8%，与传统对接工具（如 Vina、Gold）相比并无明显优势。

### 本文的核心动机与洞察

本文的核心洞察源于结构化学中的一个基本观察：**配体的构象变化主要由可旋转键处的二面角旋转驱动，而各刚性片段内部的键长、键角几乎不变**。这一事实在实验上得到验证——对 Astex 多样集 85 个配体的分析表明，结合构象与最近构象异构体之间的对齐 RMSD 中位数仅为 0.11 Å，远低于 2 Å 的成功判定阈值。

基于此，本文提出一个根本性的范式转换：**放弃在纠缠的扭角空间建模，转而将配体分解为刚体片段，在乘积空间 $\mathrm{SE}(3)^m$ 上进行独立扩散**。这一转换的数学优势在于：

- **乘积 Haar 测度**：$\mathrm{SE}(3)^m$ 上的基测度自然分解为各片段 Haar 测度的乘积，避免了扭角参数化中诱导测度的非乘积结构，使学习问题显著简化；
- **独立扰动**：前向扩散过程中可对各片段独立施加平移和旋转噪声，反向采样时各片段的评分也可独立预测，消除了几何纠缠。

简言之，SIGMADOCK 通过将分子对接重新定义为“预测各刚体片段的 SE(3) 变换”，以结构化学先验换取了扩散模型的简洁性与可学习性，从而在根本上突破了扭角扩散模型的瓶颈。

## 核心创新

SIGMADOCK 的核心创新在于**将分子对接从扭角空间彻底迁移到片段的 SE(3) 乘积空间**，从而消除了扭角扩散模型中固有的几何纠缠与学习困难。这一迁移并非简单的参数化替换，而是通过三个紧密耦合的设计实现：**片段分解与归并**、**乘积空间上的独立扩散**、以及**三角化几何约束**。

### 从扭角纠缠到乘积 Haar 测度

传统扭角扩散模型（如 DiffDock）在 $SE(3) \times \mathbb{T}^k$ 上定义扩散过程。其根本瓶颈在于：从扭角到笛卡尔坐标的映射是高度非线性、非局部的——单个扭角的变化会通过分子骨架传播，引发远端原子的全局位移。这种几何耦合导致诱导测度呈现**非乘积结构**，使得扩散过程的学习目标复杂化，采样也容易不稳定。

SIGMADOCK 的解决方案是**将配体沿可旋转键切断，分解为 $m$ 个刚体片段**，在乘积空间 $SE(3)^m$ 上定义扩散过程。由于每个片段独立承载一个 SE(3) 变换，扩散的基测度自然因子分解为乘积 Haar 测度，从根本上避免了扭角参数化带来的几何纠缠。正如 Theorem 1 所证明的：扭角空间诱导的笛卡尔密度通常不是乘积分布，而片段空间则天然具有因子分解性质——这使得学习问题显著简化。

### 片段归并（FR3D）：在自由度与化学合理性间平衡

朴素地切断所有 $k$ 个可旋转键会产生 $k+1$ 个片段，自由度过高且引入了大量虚拟原子。FR3D（Fragment Reduction for 3D）通过**随机搜索递归合并相邻片段**，将片段数从 $\hat{m} = k+1$ 压缩至不可约的 $m$。合并过程中，被消去的扭角键上的虚拟原子被移除，避免了过度约束二面角变化。经验上，FR3D 能将片段数压缩至约 $\frac{2}{3}\hat{m}$，有效自由度满足 $k+6 \leq \text{DoF} \leq 6m$。

### 三角化约束：软几何先验而非硬限制

片段独立扩散后如何保证化学合理性？SIGMADOCK 引入**三角化距离约束**作为条件信号，而非硬性限制。Lemma 1 证明：通过固定相邻片段间的跨片段距离（三角边），可以唯一确定键长和键角，同时**不限制二面角的变化**。这一设计巧妙地在“保持局部化学结构”与“允许构象柔性”之间取得平衡。消融实验证实，移除三角化约束条件使 PB-validity 从 79.9% 骤降至 67.1%（下降 12.8 个百分点），验证了该约束的关键作用。

### 架构与评分的协同适配

为适配片段级扩散，SIGMADOCK 对 EquiformerV2 骨干网络进行了针对性改造：添加虚拟节点与边构建分层拓扑，以 SO(3)-等变方式预测每个原子的力和扭矩，再通过牛顿-欧拉方程聚合为片段的平移和旋转评分。在评分排序阶段，SIGMADOCK 摒弃了需要单独训练的置信度网络，转而采用**伪结合能（Vinardo）+ PoseBusters 物理化学检查**的简单启发式策略，在保持高效的同时取得了优异的排序效果。

## 整体框架

![[assets/figures/papers/iclr26_0011_Vgm77U4ojX_SigmaDock_Untwisting_Molecular_Docking_with_Frag/figures/001_Figure_1.jpg]]
*Figure 1: Illustration of SIGMADOCK using PDB 1V4S and ligand MRK. We create an initial conformation of a query ligand where we define our m rigid body fragments (colour coded). The corresponding forward diffusion process operates in $\mathrm { S E }$ ( 3 )$^ { \overline { { { m } } } }$ via independent roto-translations

![[assets/figures/papers/iclr26_0011_Vgm77U4ojX_SigmaDock_Untwisting_Molecular_Docking_with_Frag/figures/003_Figure_3.jpg]]
*Figure 3: Illustrative example of how FR3D reduces the number of fragments (colour coded) required to represent rigid bodies on ligand TNK into irreducible form. A: Defining fragments by snapping all torsional bonds (ribbons); B: FR3D recursively attempts to reduce the k torsional bonds and removes over-constrained dummies in the process (denoted by the coloured rings), which otherwise define a dihedral across the merged fragment; C; Over-constrained dummies removed and triangulation edges displayed under a different stochastic reduction (equiprobable to solution b)*

SIGMADOCK 的整体 pipeline 围绕一个核心思想展开：**将配体分解为刚体片段，在乘积空间 SE(3)^m 上定义独立扩散过程，从而消除传统扭角扩散模型中因扭角到笛卡尔坐标映射产生的非线性几何纠缠**。整个流程可归纳为以下几个串联模块：

### 输入与预处理

给定一个蛋白质-配体对，系统首先从配体的分子图中识别所有可旋转键，将其切断得到初始的 $k+1$ 个无扭角片段。随后，**FR3D（Fragment Reduction in 3D）** 模块对相邻片段进行随机搜索式归并，将片段数从 $k+1$ 压缩至不可约的 $m$ 个（平均约降至初始数量的 2/3），同时建立跨片段的三角化距离约束。这些约束通过余弦定理固定相邻键角和扭键长度，但**不限制二面角的变化**（Lemma 1），从而在保持化学合理性的前提下降低有效自由度——从无约束的 $6m$ 降至 $k+6$ 到 $6m$ 之间。

蛋白质侧则通过一个以配体原子为中心、半径随机扰动的口袋定义来截取结合位点残基（$d_r := d_0 + \mathcal{N}(0, \sigma_r)$，默认 $d_0=5$ Å，$\sigma_r=1$ Å），以减轻口袋中心先验偏差。

### 扩散过程

核心生成过程定义在 **SE(3)^m 乘积空间**上：每个片段拥有独立的平移 $p_i \in \mathbb{R}^3$ 和旋转 $R_i \in \mathrm{SO}(3)$，整体位姿为 $\mathbf{Z} = (p_1, R_1, \ldots, p_m, R_m)$。正向扩散通过 SDE 对各片段独立施加平移噪声和 SO(3) 上的旋转噪声：

$$d\mathbf{Z}^{(t)} = \left[ -\frac{1}{2}\mathbf{p}^{(t)}, 0 \right] dt + \left[ d\mathbf{B}_{\mathbb{R}^{m\times 3}}^{(t)}, d\mathbf{B}_{\mathrm{SO}(3)^m}^{(t)} \right]$$

由于 SE(3)^m 上的基测度为乘积 Haar 测度，该扩散过程具有因子分解性质，**避免了扭角模型中诱导测度的非乘积结构**（Theorem 1），使评分函数的学习目标显著简化。

反向采样则依赖条件评分函数 $\nabla \log p_{T-t}(\overleftarrow{\mathbf{Z}}^{(t)}|\mathcal{G}_{\mathrm{dock}})$ 驱动去噪 SDE，从先验分布逐步恢复结合构象。

### 评分网络架构

评分网络以改造的 **EquiformerV2** 为骨干，通过添加虚拟节点和边构建分层拓扑，以 SO(3)-等变方式处理蛋白质-配体交互。网络输出每个原子的力预测，再通过牛顿-欧拉方程聚合为片段的平移力 $\mathbf{F}_F$ 和扭矩 $\pmb{\tau}_F$，最终转换为平移评分 $\mathbf{s}_{\theta}^p$ 和旋转评分 $\mathbf{s}_{\theta}^R$：

$$\mathbf{s}_{\theta}^p = \frac{1}{\sqrt{1-\alpha_t}} \cdot \frac{1}{|\mathcal{G}_F|} \mathbf{F}_F$$

$$\mathbf{s}_{\theta}^R = - \frac{\partial_\omega f_0(\omega, \sigma(t))}{\omega f_0(\omega, \sigma(t))} [\mathbf{I}_F^{-1} \pmb{\tau}_F] \times R_F$$

训练目标为标准的去噪评分匹配损失，在 SE(3)^m 的黎曼度量下优化。

### 后处理与排序

采样完成后，三角化约束中引入的虚拟原子被丢弃，扭键通过锚点重建。生成的候选构象不依赖单独训练的置信度网络，而是通过**简单的伪结合能（Vinardo 评分函数）与 PoseBusters 物理化学有效性检查**进行排序，选出 Top-1 预测。消融实验表明，移除能量评分使 RMSD<2 从 80.5% 降至 76.1%，移除 PoseBusters 评分使 PB-validity 从 79.9% 降至 74.9%，验证了该排序策略的有效性。

### 模块间数据流总结

1. **配体分子图** → 可旋转键识别 → 初始 $k+1$ 片段
2. **FR3D 归并** → $m$ 个不可约片段 + 三角化距离约束
3. **蛋白质口袋截取** → 结合位点残基子图
4. **EquiformerV2 评分网络** → 原子力预测 → 片段平移/旋转评分
5. **反向 SDE 采样** → SE(3)^m 上的候选位姿集合
6. **虚拟原子丢弃 + 扭键重建** → 完整配体构象
7. **Vinardo 能量 + PoseBusters 检查** → 排序 → Top-1 预测

## 核心模块与公式推导

### 2.1 构象流形与扭角模型的困境

配体的局部几何构象空间服从 Boltzmann 分布，概率质量集中在一个满足完整约束的流形 $\mathcal{M}_c$ 上：

$$\mathcal{M}_c = \{ \mathbf{x}_c \in \mathbb{R}^{|\mathcal{G}_{\mathrm{ligand}}|\times 3} : g(\mathbf{x}_c) \approx 0 \}$$

这些完整约束编码了局部守恒的几何先验，包括键长（$d_{AB} = d_0$）和键角（$\tau_{ABC} = \tau_0$），但**不包含二面角/扭角**。因此，配体构象变化的主要自由度来自可旋转键上的扭角变化（Figure 2C 展示了 SKF、CEL、IH5 配体的构象系综，最显著的结构变化确实源于可旋转键的扭转）。

传统扭角扩散模型在 $\mathrm{SE}(3) \times \mathbb{T}^k$ 上定义生成过程，其核心瓶颈在于：**从扭角到笛卡尔坐标的映射 $\Psi(p, R, \phi) = (p, R) \cdot \psi(\phi)$ 具有高度非线性和非局部的几何耦合**，导致诱导测度在笛卡尔空间中并非乘积结构，学习目标复杂且采样不稳定（Theorem 1 及附录 C.2 提供了形式化证明）。

### 2.2 片段分解与 FR3D 归并

SIGMADOCK 的核心操作是将配体沿所有可旋转键断裂，分解为 $k+1$ 个刚体片段（$k$ 为可旋转键数）。生成任务由此退化为**预测每个片段的 $\mathrm{SE}(3)$ 刚体变换**，显式避免了扭角建模。

直接断裂产生 $\hat{m} = k+1$ 个片段，自由度过高。FR3D（Fragment Reduction in 3D）通过**随机搜索递归合并相邻片段**，将片段数降至不可约的 $m$（$1 \leq m \leq k+1$）。合并条件由三角化约束保证：仅当合并不引入过约束时才允许。经验上，$\bar{m} \approx \frac{2}{3}\hat{m}$，有效自由度满足 $k+6 \leq \mathrm{DoF} \leq 6m$（Figure 3 以配体 TNK 为例展示了归并过程）。

### 2.3 三角化约束（Lemma 1）

片段化后，相邻片段通过扭键连接。SIGMADOCK 引入**软三角化距离约束**来维持片段间的化学合理性：

**Lemma 1**：给定片段 $\mathcal{A}$ 上的原子 $A_p$、扭键原子 $B_A$（属于 $\mathcal{A}$）和 $C_{\mathcal{D}}$（属于相邻片段 $\mathcal{D}$），若跨片段距离 $\|A_p - C_{\mathcal{D}}\|$ 被约束至参考值，则键角 $\angle(A_p, B_A, C_{\mathcal{D}})$ 被唯一确定，而**二面角的变化不受限制**：

$$\cos \angle (A_p, B_A, C_{\mathcal{D}}) = \frac{\| A_p - B_A \|^2 + \| B_A - C_{\mathcal{D}} \|^2 - \| A_p - C_{\mathcal{D}} \|^2}{2 \| A_p - B_A \| \| B_A - C_{\mathcal{D}} \|}$$

该公式直接由余弦定理导出（证明见附录 D.2）。其关键性质是：**固定键长和跨片段距离即固定键角，但不约束二面角**，从而在保持局部化学合理性的同时保留了构象灵活性。消融实验证实，移除三角化约束使 PB-validity 从 79.9% 骤降至 67.1%（Table 1, Config A）。

### 2.4 $\mathrm{SE}(3)^m$ 上的扩散过程

片段位姿定义在乘积空间 $\mathrm{SE}(3)^m$ 上，参数化为 $\mathbf{Z} = (\mathbf{p}, \mathbf{R})$，其中 $\mathbf{p} \in \mathbb{R}^{m \times 3}$ 为各片段质心平移，$\mathbf{R} \in \mathrm{SO}(3)^m$ 为各片段旋转矩阵。该空间具有**因子分解的乘积 Haar 测度**，使得扩散过程可独立作用于每个片段的平移和旋转分量。

**前向扩散 SDE**（VP 型）：

$$d\mathbf{Z}^{(t)} = \left[ -\frac{1}{2}\mathbf{p}^{(t)}, 0 \right] dt + \left[ d\mathbf{B}_{\mathbb{R}^{m\times 3}}^{(t)}, d\mathbf{B}_{\mathrm{SO}(3)^m}^{(t)} \right]$$

平移分量经历 Ornstein-Uhlenbeck 过程，旋转分量在 $\mathrm{SO}(3)$ 上进行各向同性扩散。

**反向采样 SDE**：

$$d\overleftarrow{\mathbf{Z}}^{(t)} = \left[ \frac{1}{2}\overleftarrow{\mathbf{p}}^{(t)} + \nabla_p \log p_{T-t}, \nabla_R \log p_{T-t} \right] dt + \left[ d\mathbf{B}_{\mathbb{R}^{m\times 3}}^{(t)}, d\mathbf{B}_{\mathrm{SO}(3)^m}^{(t)} \right]$$

其中 $\nabla_p \log p_{T-t}$ 和 $\nabla_R \log p_{T-t}$ 分别为平移和旋转的条件评分函数，由评分网络 $s_{\boldsymbol{\theta}}$ 预测。

**评分匹配损失**：

$$\mathcal{L}(\boldsymbol{\theta}) = \mathbb{E}_{p(t), p_{\mathrm{data}}, p_{t|0}} \left[ \left\| s_{\boldsymbol{\theta}}(\mathbf{Z}^{(t)}, t, \mathcal{G}_{\mathrm{dock}}) - \nabla_z \log p_{t|0}(\mathbf{Z}^{(t)}|\mathbf{Z}^{(0)}) \right\|_{\mathrm{SE}(3)^m}^2 \right]$$

其中 $\mathcal{G}_{\mathrm{dock}}$ 为包含蛋白质-配体交互图和三角化约束的对接图。

### 2.5 评分预测：从原子力到片段评分

SIGMADOCK 使用改造的 EquiformerV2 作为骨干网络（$\mathrm{SO}(3)$-等变），在蛋白质-配体交互图上预测每个原子的力和扭矩。评分预测头通过牛顿-欧拉方程将原子级预测聚合为片段级评分：

**平移评分**（由片段总力 $\mathbf{F}_F$ 驱动）：

$$\mathbf{s}_{\theta}^p = \frac{1}{\sqrt{1-\alpha_t}} \cdot \frac{1}{|\mathcal{G}_F|} \mathbf{F}_F$$

**旋转评分**（由扭矩 $\boldsymbol{\tau}_F$ 和惯性矩阵 $\mathbf{I}_F$ 驱动）：

$$\mathbf{s}_{\theta}^R = - \frac{\partial_\omega f_0(\omega, \sigma(t))}{\omega f_0(\omega, \sigma(t))} [\mathbf{I}_F^{-1} \boldsymbol{\tau}_F] \times R_F$$

其中 $f_0$ 为 $\mathrm{SO}(3)$ 上的各向同性扩散核，$\sigma(t)$ 为噪声尺度，系数项确保评分形式与扩散路径的条件评分一致（推导见附录 G.4）。

### 2.6 采样后处理与排序

采样完成后，哑原子（用于三角化约束的辅助原子）被丢弃，扭键通过锚点重建。SIGMADOCK **不需要单独训练的置信度网络**，而是采用简单的启发式排序策略：结合 Vinardo 伪结合能评分和 PoseBusters 物理化学有效性检查（包括键长、键角、手性中心、平面性、碰撞等判据）对生成样本进行排序。消融实验表明，移除能量评分使 RMSD<2 从 80.5% 降至 76.1%，移除 PoseBusters 评分使 PB-validity 从 79.9% 降至 74.9%（Table 1, Config D, E）。

## 实验与分析

### 核心性能对比

SIGMADOCK 在 PoseBusters 基准上实现了 **79.9% 的 Top-1 成功率**（RMSD < 2Å 且通过 PB-valid 物理化学检查），相比此前深度学习方法报告的 12.7%–32.8%，绝对提升超过 67 个百分点。在 Astex 多样集上同样取得领先性能（Figure 4 左）。


![[assets/figures/papers/iclr26_0011_Vgm77U4ojX_SigmaDock_Untwisting_Molecular_Docking_with_Frag/figures/005_Figure_4.jpg]]
*Figure 4: Performance benchmarks. Left: Comparative performance of SIGMADOCK on the PB and AX diverse sets against prior methods. Extracted from Abramson et al. (2024); Buttenschoen et al. (2024). (*) Denotes classical docking; (**) Are not open-sourced. Right: Performance breakdown across sequence similarity splits in the PB set*

与传统对接工具相比：Vina 和 Gold 在 PoseBusters 上的 PB-valid 率远低于 SIGMADOCK。值得注意的是，SIGMADOCK 是首个在 PoseBusters 预期训练-测试划分（PDBBind v2020）上训练、且在该基准上超越经典对接工具的生成式方法。

**关键指标拆解**（Table 1 默认配置）：

![[assets/figures/papers/iclr26_0011_Vgm77U4ojX_SigmaDock_Untwisting_Molecular_Docking_with_Frag/figures/006_Table_1.jpg]]
*Table 1: Ablation results (Top-1 accuracy (%) across the PB set) for different configurations. A-C are re-trained from scratch; (*): default*

- RMSD < 2Å：80.5%
- PB-valid：79.9%
- RMSD < 2Å 且 PB-valid：79.9%

这表明模型生成的位姿在几何精度和化学合理性上高度一致——几乎不存在“几何正确但化学违规”的样本。

### 泛化能力与序列相似度分析

Figure 4 右半部分按蛋白序列相似度分层展示了 SIGMADOCK 的性能：
- [0, 30) 低相似度区间：72% PB-valid
- [30, 95) 中等相似度区间：79% PB-valid  
- [95, 100] 高相似度区间：87% PB-valid

与 AlphaFold3 的对比（Table 5）需要谨慎解读。AF3 的训练-测试划分与 PDBBind 不同：AF3 在低相似度区间（[0, 30)）仅有 2 个样本，而 SIGMADOCK 有 21 个；AF3 报告的平均值（84.4%）与按相似度分层计算的平均值（80.2%）存在不一致。在样本更均衡的中高相似度区间，SIGMADOCK 匹配或超越 AF3（[95, 100]：87% vs 78%），且训练数据量仅为 AF3 的约 1/20。


![[assets/figures/papers/iclr26_0011_Vgm77U4ojX_SigmaDock_Untwisting_Molecular_Docking_with_Frag/figures/021_Table_5.jpg]]
*Table 5: Stratification of the original PDBbind(v2020) vs. AF3 train-test splits on PoseBusters(v2). Sequence similarity split values extracted from AF3 Extended Data Fig. 4c (Abramson et al., 2024). (*) We observe a mismatch between the averaged sequence similarity results (80.2%) vs the reported average performance in AF3’s Extended Data Fig. 4e (84.4%)*

### 消融实验

Table 1 展示了五项消融实验的核心发现：

**1. 三角化约束（Config A）**：移除三角化距离条件后，PB-valid 从 79.9% 骤降至 **67.1%**（降幅 12.8%）。这直接验证了 Lemma 1 的理论论断——三角化约束在不限制二面角变化的前提下，通过固定相邻键长和键角来维持局部化学合理性。缺少该约束，生成片段间的几何关系失去锚定，导致大量化学违规。

**2. 蛋白质-配体交互边（Config B）**：移除蛋白质-配体交互边后，RMSD < 2Å 暴跌至 **10.3%**。这表明模型几乎完全依赖蛋白-配体交互信息来引导片段进入正确结合位姿，仅靠配体内几何约束无法实现有效对接。

**3. 片段归并 FR3D（Config C）**：用朴素 (k+1) 片段切割替代 FR3D 归并后，PB-valid 降至 **73.2%**。FR3D 通过随机搜索合并相邻片段，将片段数从 $\hat{m} = k+1$ 降至约 $\bar{m} \approx \frac{2}{3}\hat{m}$，有效降低了自由度（从 $6(k+1)$ 降至 $6m$），同时保留了关键的构象灵活性。

**4. 伪结合能评分（Config D）**：移除 Vinardo 伪结合能评分后，RMSD < 2Å 从 80.5% 降至 **76.1%**，PB-valid 降至 **73.4%**。该评分作为简单的物理启发式排序手段，在不依赖单独训练的置信度网络的情况下，有效筛选高质量位姿。

**5. PoseBusters 评分项（Config E）**：移除 PoseBusters 理化检查后，PB-valid 从 79.9% 降至 **74.9%**，但 RMSD < 2Å 反而升至 82.1%。这说明纯几何精度与化学合理性之间存在 trade-off——部分高 RMSD 精度的位姿存在化学违规，PoseBusters 检查有效过滤了这些样本。

### 失败模式分析

**1. 辅因子场景（Table 2）**：当结合口袋中存在辅因子（辅酶、离子、结晶助剂等）时，性能显著下降。无辅因子子集（n=165）的 Top-1 为 84.2%，而含天然配体子集（n=17）仅为 58.8%，且样本失败率高达 41.2%。模型当前不显式处理辅因子，导致其在拥挤口袋中的位姿预测能力受限。

**2. RMSD 指标的局限性（Figure 11）**：多个高 RMSD（4.2–10.2Å）的生成位姿实际上化学合理，仅是结合模式与晶体结构不同。例如 7FRX-O88（10.2Å RMSD）和 7KZ9-XN7（4.7Å RMSD）的生成位姿展示了可替代的结合构象。这说明 RMSD 作为单一指标可能低估实际对接质量。

**3. 口袋定义的敏感性（Table 3）**：SIGMADOCK 依赖用户指定的口袋中心。当口袋半径 $d_0$ 从 4Å 变化到 7Å 时，性能相对稳定（PB-valid 在 74.3%–79.9% 间波动），但训练时使用的随机化策略（$d_r := d_0 + \mathcal{N}(0, \sigma_r)$，默认 $\sigma_r = 1$Å）对鲁棒性至关重要。

**4. 手性中心翻转**：片段化过程可能导致手性中心翻转，当前依赖后过滤丢弃不良立体异构体，而非在生成过程中显式约束。

### 采样效率

Figure 12 展示了 Top-k 成功率随种子数 $N_{\text{seeds}}$ 的变化。Top-1（40 种子）为 79.9%，而 Oracle 上限（取所有种子中的最优）接近 90%。这表明排序策略仍有约 10 个百分点的提升空间——约 10% 的复合物在所有 40 个采样中至少存在一个高质量位姿，但当前评分函数未能将其排到 Top-1。理想伯努利线表明采样间独立性较好，增加种子数可稳定提升 Top-k 性能。


![[assets/figures/papers/iclr26_0011_Vgm77U4ojX_SigmaDock_Untwisting_Molecular_Docking_with_Frag/figures/020_Figure_12.jpg]]
*Figure 12: Top-k success rate as a function of the pool sample size $N _ { \mathrm { s e e d s } }$ . . Solid Top-k lines represent the mean success rates across ( 4 0 - $N _ { \mathrm { s e e d s } }$ ) permutations, with shaded areas representing the standard deviation. The Oracle reflects the empirical maximum success rate attainable across the $N _ { \mathrm { s e e d s } }$ samples, equivalent to $\mathrm { T o p } { \cdot } N _ { \mathrm { s e e d s } }$ . The ideal Bernoulli line represents the empirical optimal, assuming independent sampling probability

### 公平性说明

与先前工作的比较需注意以下因素：
1. **训练-测试泄漏控制**：SIGMADOCK 严格使用 PDBBind v2020 的 PoseBusters 训练-测试划分，而部分先前工作存在不同程度的泄漏。
2. **口袋先验**：许多深度学习方法使用基于配体位置的 bounding box 定义口袋，可能引入不可在实际部署中获得的先验信息。SIGMADOCK 通过随机化口袋半径和中心噪声来减轻该偏差。
3. **无后处理最小化**：SIGMADOCK 直接报告扩散生成结果，不使用能量最小化后处理，避免了因后处理带来的不公平比较。

## 方法谱系与知识库定位

### 1. 在分子对接方法谱系中的位置

SIGMADOCK 处于**深度学习生成式对接**与**结构化学先验**的交叉点。其直接前驱是扭角扩散模型（以 DiffDock 为代表），后者将配体构象参数化为 SE(3) 位姿与 $k$ 个可旋转键的二面角，在乘积空间 $\mathrm{SE}(3) \times \mathbb{T}^k$ 上进行扩散。SIGMADOCK 的**核心突破**在于识别出该参数化方式的结构性缺陷：从扭角到笛卡尔坐标的映射高度非线性且非局部，导致诱导测度非乘积结构，学习目标复杂、采样不稳定。通过将配体分解为刚体片段并在 $\mathrm{SE}(3)^m$ 上独立扩散，SIGMADOCK 消除了这种几何纠缠，使扩散过程可分解且易于学习——这一洞察有严格的理论支撑（Theorem 1 及附录 C.2 的形式化证明）。

与 AlphaFold3 等共折叠模型的关系更为微妙。AF3 并非严格的重对接方法，而是从序列出发联合预测结构，其训练-测试划分存在更高的序列泄漏。SIGMADOCK 在意图使用的 PDBBind(v2020) 训练-测试划分下训练，泄漏更少，训练数据仅约为 AF3 的 1/20，却在 PoseBusters 集上取得总体可比的表现（79.9% vs. 80.2%），并在高序列相似度区间 [95,100] 上超越 AF3（87% vs. 78%）。这表明**基于片段的 SE(3) 扩散在数据效率上具有显著优势**。

与传统物理对接工具（Vina、Gold）相比，SIGMADOCK 是首个在 PoseBusters 重对接任务上超越经典方法的生成式模型，标志着深度学习对接从“接近传统方法”到“实质性超越”的转折。

### 2. 适用边界与约束条件

SIGMADOCK 的设计隐含以下适用前提，超出这些边界时性能可能显著下降：

- **重对接协议**：所有评估均在已知结合位姿的晶体结构上进行重对接（re-docking）。模型未在交叉对接（cross-docking）或 apo 结构对接场景下测试，这些场景中结合口袋的构象变化可能破坏片段假设。
- **口袋中心依赖**：推理需要用户指定口袋中心。口袋定义的质量直接影响搜索区域的有效性。模型通过随机化口袋半径（$d_r := d_0 + \mathcal{N}(0, \sigma_r)$，默认 $d_0=5$Å、$\sigma_r=1$Å）来减轻对精确中心的过拟合，但若中心指定严重偏差，性能仍可能下降。
- **辅因子盲区**：当前模型不处理辅因子（辅酶、离子、结晶助剂等）。表 2 显示，存在天然配体辅因子时 Top-1 成功率降至 58.8%（失败率 41.2%），而纯净口袋中为 84.2%。这是最显著的性能瓶颈。
- **手性中心风险**：片段化过程可能导致手性中心翻转。当前依赖后过滤丢弃不良立体异构体，而非在生成过程中显式保持手性。
- **训练数据规模**：仅使用 PDBBind v2020（约 19k 复合物）训练，限制了分布外泛化能力。更大规模、更多样化的训练数据可能进一步提升性能。

### 3. 已知局限与失败模式

消融实验揭示了各组件的贡献边界和失败模式：

| 消融配置 | PB-validity | 关键发现 |
|---------|-------------|---------|
| 默认（Config I*） | 79.9% | 完整模型 |
| 移除三角化约束（Config A） | 67.1% | 下降 12.8%，证明跨片段距离约束对化学合理性至关重要 |
| 移除蛋白-配体交互边（Config B） | RMSD<2 仅 10.3% | 蛋白上下文是精确对接的核心驱动，纯配体内约束远不足 |
| 移除片段归并（Config C） | 73.2% | 朴素 $(k+1)$ 片段切割引入过多自由度，FR3D 归并有效降低复杂度 |
| 移除伪结合能评分（Config D） | 73.4% | 能量排序对筛选近原生构象有实质性贡献 |
| 移除 PoseBusters 评分（Config E） | 74.9% | 物理化学检查补充了能量评分的盲区 |

此外，RMSD 指标本身存在局限性。图 11 展示了多个高 RMSD（4.2–10.2Å）但化学上合理的生成样例，说明 RMSD 无法完全捕捉对接质量——这在对称配体或替代结合模式中尤为突出。

Oracle 分析（图 12）显示，当采样种子数增加时，Oracle 上限接近 90%，而实际 Top-1 约为 80%。这约 10% 的差距表明**排序/重评分策略是当前最主要的性能瓶颈**，而非生成能力本身。

### 4. 开放问题与未来方向

基于上述分析，以下问题构成该方向的核心研究议程：

1. **排序策略优化**：如何缩小 Oracle 上限（~90%）与实际 Top-1（~80%）之间的差距？是否需要更精细的能量函数、学习型排序器，或更好的采样策略？

2. **辅因子处理**：如何将辅因子纳入片段框架？一种自然扩展是将辅因子视为额外的刚体片段，但这需要处理辅因子-蛋白和辅因子-配体的双重交互。

3. **柔性受体对接**：将部分蛋白侧链视为额外可动片段是方法上的自然延伸。这直接触及诱导契合效应的建模。

4. **交叉对接与 apo 结构**：在结合口袋构象未知的真实虚拟筛选场景中，SIGMADOCK 的鲁棒性尚未验证。这可能需要对口袋定义和采样策略进行适应性调整。

5. **数据规模化与迁移学习**：在更大规模数据集上训练，或利用预训练的蛋白质表征，能否进一步提升泛化性，特别是在低序列相似度区间（当前 [0,30) 区间为 72%，低于 AF3 的 87%）？

6. **高通量筛选适配**：基于片段的 SE(3) 扩散是否在速度上适用于大规模虚拟筛选？当前 40 种子的采样策略可能需要针对吞吐量进行优化。

## 原文 PDF

![[paperPDFs/ICLR_2026/SigmaDock_Untwisting_Molecular_Docking_with_Fragment_Based_SE3_Diffusion.pdf]]
