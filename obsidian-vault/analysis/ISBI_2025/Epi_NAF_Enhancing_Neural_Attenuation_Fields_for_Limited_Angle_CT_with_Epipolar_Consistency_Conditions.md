---
title: "Epi-NAF: Enhancing Neural Attenuation Fields for Limited-Angle CT with Epipolar Consistency Conditions"
type: paper
paper_level: A
venue: ISBI
year: 2025
pdf_ref: paperPDFs/ISBI_2025/Epi_NAF_Enhancing_Neural_Attenuation_Fields_for_Limited_Angle_CT_with_Epipolar_Consistency_Conditions.pdf
aliases:
- Epi-NAF
tags:
- ISBI_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "引入基于极线一致性条件（ECC）的正则化损失 L_ECC，将输入投影的监督信息传播到全角度范围，约束未被直接观测的投影。"
primary_logic: "利用X射线成像中固有的极线一致性条件，在神经场训练时强制预测投影在对应极线上保持导数一致性，从而在无需额外监督的情况下实现对未观测角度的有效正则化。"
claims:
- "Epi-NAF通过L_ECC将有限角度输入视图的监督传播至全180°范围的预测投影，正则化未约束区域。"
- "在四个CT扫描数据集及多种有限角度配置下，Epi-NAF的PSNR/SSIM均一致优于vanilla NAF。"
- "定性结果中，Epi-NAF显著减少了vanilla NAF在低密度区域“幻觉”高密度结构的现象。"
- "Chest CT 60° 上 PSNR/SSIM = 21.57/.724"
---

# Epi-NAF: Enhancing Neural Attenuation Fields for Limited-Angle CT with Epipolar Consistency Conditions

> [!tip] 核心洞察
> 利用X射线成像中固有的极线一致性条件，在神经场训练时强制预测投影在对应极线上保持导数一致性，从而在无需额外监督的情况下实现对未观测角度的有效正则化。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Epi-NAF：利用极线一致性条件增强有限角度CT的神经衰减场 |
| 英文题名 | Epi-NAF: Enhancing Neural Attenuation Fields for Limited-Angle CT with Epipolar Consistency Conditions |
| 会议/期刊 | ISBI 2025 |
| Links | [paper](https://arxiv.org/abs/2411.06181v1) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Epi-NAF |
| Dataset | Chest CT 60°, Abdomen CT 60°, Chest CT 90° |

> [!tip] 效果简介
> - Chest CT 60° 上，PSNR/SSIM 为 21.57/.724，对比 20.4/.678，变化 +1.17/+0.046。
> - Abdomen CT 60° 上，PSNR/SSIM 为 26.1/.863，对比 25.75/.858，变化 +0.35/+0.005。
> - Chest CT 90° 上，PSNR/SSIM 为 25.73/.856，对比 24.78/.834，变化 +0.95/+0.022。

## 概述

有限角度CT（Limited-Angle CT, LACT）重建是计算成像中的一个核心挑战：当X射线投影仅能在受限的角度范围内采集时，重建问题变为严重欠定，导致传统解析方法（如FDK）和迭代方法（如SART、ASD-POCS）产生严重的条纹伪影和结构失真。近年来，基于神经衰减场（Neural Attenuation Field, NAF）的方法将CT重建转化为连续三维衰减系数场的优化问题，在稀疏视角和有限角度场景下展现出优于传统方法的潜力。然而，vanilla NAF在优化过程中仅依赖有限角度范围内的输入投影进行监督，未观测角度区域完全缺乏约束，导致重建结果出现模糊、细节丢失，甚至在低密度区域“幻觉”出高密度伪结构。

本文提出**Epi-NAF**，核心思想是将X射线成像中固有的**极线一致性条件（Epipolar Consistency Condition, ECC）**引入神经场训练框架。ECC描述了这样一个物理事实：在圆形锥束CT轨迹下，任意两个投影图像中对应极线上的余弦加权投影的Radon变换导数应当相等。Epi-NAF通过在训练时随机采样全180°范围内的投影角度对，计算预测投影在对应极线上的导数一致性损失 $\mathcal{L}_{\mathrm{ECC}}$，从而将有限角度输入视图的监督信息有效传播至未观测角度区域，实现对神经场优化的全角度正则化。总损失函数为 $\mathcal{L} = \mathcal{L}_{\mathrm{Recon}} + \lambda \mathcal{L}_{\mathrm{ECC}}$，其中 $\mathcal{L}_{\mathrm{Recon}}$ 为预测投影与输入投影之间的像素级L2损失。

在方法定位上，Epi-NAF属于**神经场CT重建 + 几何一致性正则化**的技术路线。其基线方法vanilla NAF（Zha et al., MICCAI 2022）仅使用重建损失；Epi-NAF在此基础上增加了一个即插即用的正则化项，不改变网络架构，也不依赖额外的训练数据或预训练模型。与基于全变分（TV）等传统先验的迭代方法相比，Epi-NAF利用的是锥束CT几何自身的一致性约束，具有明确的物理可解释性。

实验表明，在四个CT扫描数据集（胸部、腹部、足部、颌骨）及多种有限角度配置（45°、60°、90°、120°）下，Epi-NAF的PSNR和SSIM指标均一致优于vanilla NAF。以胸部CT 60°设定为例，PSNR从20.4提升至21.57，SSIM从0.678提升至0.724。定性结果中，Epi-NAF显著抑制了vanilla NAF在低密度区域产生的高密度伪影，重建图像更接近真实CT。该方法的主要局限在于：有限角度重建本质上仍为严重欠定问题，重建结果依然存在一定程度的模糊；正则化权重 $\lambda$ 和预热轮次等超参数仅给出经验设定，缺乏系统性敏感性分析；$\mathcal{L}_{\mathrm{ECC}}$ 在其他神经场CT框架上的即插即用特性尚未实验验证。

## 背景与动机

### 有限角度CT重建的核心困境

计算机断层成像（CT）在医学诊断与工业检测中不可或缺，但实际场景中常因扫描几何限制或辐射剂量约束，只能获取有限角度（Limited-Angle CT, LACT）的X射线投影数据。在此设定下，重建问题变为严重欠定：投影角度覆盖不完整导致傅里叶空间中存在缺失楔形区域，传统解析方法（如**FDK**, Feldkamp et al., JOSA A 1984）和迭代方法（如**SART**, Andersen et al., Ultrasonic Imaging 1984; **ASD-POCS**, Sidky et al., PMB 2008）的重建结果普遍存在严重的条纹伪影、方向性模糊和结构失真。

### 神经衰减场的潜力与缺口

近年来，神经辐射场（NeRF）启发的隐式神经表示被引入CT重建领域。其中，**神经衰减场（Neural Attenuation Field, NAF）**（Zha et al., MICCAI 2022）将3D衰减系数建模为多层感知机（MLP）的连续函数，并通过可微Beer-Lambert渲染与输入投影进行像素级$L_2$监督优化：

$$\hat{I}(\mathbf{r}) = I_0 \exp\left(-\sum_{i=1}^{N} \mu_i \delta_i\right)$$

$$\mathcal{L}_{\mathrm{recon}} = \frac{1}{|\Omega_{recon}|} \sum_{r \in \Omega_{recon}} \|\hat{I}(r) - I(r)\|_2^2$$

NAF利用神经场的隐式平滑先验在一定程度上缓解了有限角度问题，但其训练过程仅依赖有限角度范围内的输入投影进行监督。**核心瓶颈在于**：对于未被直接观测的投影角度，优化过程完全缺乏约束，导致神经场在这些区域自由“想象”，表现为重建切片中的模糊、细节丢失，以及在低密度区域“幻觉”出高密度结构的伪影（见Figure 3定性对比中vanilla NAF的典型失效模式）。

### 极线一致性条件的引入动机

X射线成像几何中存在一个固有的物理约束——**极线一致性条件（Epipolar Consistency Condition, ECC）**。如图1所示，两个不同源位置采集的投影图像中，由同一极平面定义的两条对应极线上，余弦加权投影的Radon变换导数应严格相等：

$$\frac{\partial}{\partial t} \mathcal{R}_{\tilde{P}_0}(\alpha_0, t_0) = \frac{\partial}{\partial t} \mathcal{R}_{\tilde{P}_1}(\alpha_1, t_1)$$

该条件源于X射线衰减的物理一致性：同一极平面上的线积分在几何上对应相同的3D空间信息。ECC此前主要用于投影几何标定，但本文的核心洞察在于：**这一几何一致性约束可被转化为神经场训练的损失函数，从而将有限角度输入投影的监督信号传播到全180°范围的预测投影上**。在每次训练迭代中，随机采样一对投影角度，计算其对应极线上的导数一致性损失$\mathcal{L}_{\mathrm{ECC}}$，即可在无需任何额外标注或真实投影数据的情况下，为未观测角度提供有效的正则化：

$$\mathcal{L}_{\mathrm{ECC}} = \| \sum_{j=1}^{N_s} \Delta_{0,j} \delta_0 - \Delta_{1,j} \delta_1 \|_2^2$$

$$\mathcal{L} = \mathcal{L}_{\mathrm{Recon}} + \lambda \mathcal{L}_{\mathrm{ECC}}$$

这一设计将几何先验无缝嵌入神经场优化框架，使监督信息从有限角度区域“流动”至全角度范围（Figure 2），从而显著抑制vanilla NAF在未约束区域的伪影生成。

## 核心创新

Epi-NAF 的核心创新在于将 **X 射线成像中固有的极线一致性条件（Epipolar Consistency Conditions, ECC）** 引入神经衰减场（Neural Attenuation Field, NAF）的优化框架，作为一项即插即用的正则化损失 $ \mathcal{L}_{\mathrm{ECC}} $，以解决有限角度 CT（Limited-Angle CT, LACT）重建中**未观测角度区域缺乏约束**这一根本瓶颈。

### 问题瓶颈与因果机制

在 LACT 设定下，vanilla NAF（Zha et al., MICCAI 2022）仅依赖有限角度范围内的输入投影进行监督（通过 $ \mathcal{L}_{\mathrm{recon}} $ 计算预测投影与输入投影的 L2 误差）。这使得神经场在未观测角度区域的衰减系数优化完全缺乏引导，导致重建结果出现**模糊、细节丢失，以及低密度区域“幻觉”高密度结构**的典型伪影。

Epi-NAF 的因果调控机制在于：利用 ECC 所揭示的几何约束——即两个不同源位置下对应极线上余弦加权投影的导数应相等——将有限角度输入视图的监督信号**传播至全 180° 范围的预测投影**。这使得原本不受直接监督的未观测角度投影也受到隐式正则化，从而在不引入额外数据或监督的条件下，显著缓解了欠定问题带来的重建退化。

### 关键改动槽位（Changed Slots）

相较于 vanilla NAF，Epi-NAF 在以下两个核心槽位上进行了改动：

| 槽位 | 基线方案（vanilla NAF） | Epi-NAF 方案 | 证据锚点 |
|------|------------------------|-------------|---------|
| **训练损失函数** | 仅使用重建损失 $ \mathcal{L}_{\mathrm{recon}} $（预测投影与输入投影的像素级 L2 误差） | 总损失扩展为 $ \mathcal{L} = \mathcal{L}_{\mathrm{Recon}} + \lambda \mathcal{L}_{\mathrm{ECC}} $，其中 $ \mathcal{L}_{\mathrm{ECC}} $ 强制对应极线上导数一致性 | Section 3, Eq. (5) |
| **投影角度采样与监督范围** | 训练时仅从有限角度的输入投影中采样射线进行监督 | 额外从整个 180° 范围随机采样投影角度对，计算 $ \mathcal{L}_{\mathrm{ECC}} $，将监督拓展至未观测角度 | Section 3 |

### $ \mathcal{L}_{\mathrm{ECC}} $ 的工作机理

ECC 损失的核心计算流程如下：

1. **随机采样投影角度对**：在每次训练迭代中，从完整的 180° 角度范围内随机采样一对投影角度，而非局限于输入投影的有限角度区间。

2. **极线采样与导数近似**：对于采样到的角度对，确定其对应的极线。在每条极线上，以微小偏移量 $ \epsilon $ 采样两条邻近线，通过中心差分近似投影值沿极线方向的导数。

3. **一致性约束**：强制两条对应极线上的导数近似积分相等，构建 L2 损失：

$$ \mathcal{L}_{\mathrm{ECC}} = \left\| \sum_{j=1}^{N_s} \Delta_{0,j} \delta_0 - \Delta_{1,j} \delta_1 \right\|_2^2 $$

其中 $ \Delta_{0,j} $ 和 $ \Delta_{1,j} $ 分别为两条对应极线上第 $ j $ 个采样点处的导数近似，$ \delta_0 $ 和 $ \delta_1 $ 为采样步长。

### 训练策略设计

为确保训练稳定性，Epi-NAF 采用了 **200 个 epoch 的预热阶段**（warm-up period），在此期间仅优化 $ \mathcal{L}_{\mathrm{Recon}} $，使神经场先收敛到一个合理的初始解，随后再引入 $ \mathcal{L}_{\mathrm{ECC}} $ 进行联合优化。正则化权重 $ \lambda $ 根据有限角度范围动态调整：角度范围低于 120° 时设为 $ 10^{-3} $，120° 时设为 $ 10^{-4} $，以适应不同程度的不适定性。

### 创新边界与局限

需要指出的是，ECC 本身并非本文首次提出，其在传统 CT 重建中已有理论基础。Epi-NAF 的贡献在于**首次将 ECC 作为可微分损失项集成到神经场 CT 重建框架中**，实现了端到端的隐式正则化。论文声称 $ \mathcal{L}_{\mathrm{ECC}} $ 可作为即插即用模块应用于任意基于神经场的 CT 框架，但这一泛化能力目前仅在与 NAF 的结合中得到了验证，其在其他架构（如 SNAF、IntraTomo 等）上的有效性仍有待实验证实。

## 整体框架

Epi-NAF 的整体训练流程在 vanilla NAF 的基础上引入了一条关键的正则化通路，将有限角度输入投影的监督信号传播至全角度范围。其核心架构由四个模块串联构成：

1. **神经衰减场（MLP）**：一个多层感知机 $\phi$ 将三维空间坐标映射为对应点的衰减系数 $\mu$，作为场景的隐式连续表示。该模块与 vanilla NAF 共享完全相同的网络结构。

2. **可微渲染（Beer-Lambert 积分）**：沿每条射线对衰减系数进行数值积分，得到预测的 X 射线投影强度：
   $$\hat{I}(\mathbf{r}) = I_0 \exp\left(-\sum_{i=1}^{N} \mu_i \delta_i\right)$$
   该模块使梯度能够从投影空间反向传播至衰减场参数。

3. **重建损失 $\mathcal{L}_{\mathrm{recon}}$**：在有限角度范围内的输入投影上计算预测值与真实测量值之间的像素级 L2 误差：
   $$\mathcal{L}_{\mathrm{recon}} = \frac{1}{|\Omega_{recon}|} \sum_{r \in \Omega_{recon}} \|\hat{I}(r) - I(r)\|_2^2$$
   这是唯一直接接收输入监督的损失项，仅覆盖被观测的角度区域。

4. **极线一致性损失 $\mathcal{L}_{\mathrm{ECC}}$**：这是 Epi-NAF 的核心创新模块。在每次训练迭代中，从整个 180° 范围随机采样一对投影角度，计算对应极线上余弦加权投影的导数一致性损失：
   $$\mathcal{L}_{\mathrm{ECC}} = \| \sum_{j=1}^{N_s} \Delta_{0,j} \delta_0 - \Delta_{1,j} \delta_1 \|_2^2$$
   该损失不依赖任何输入投影的真值，仅要求预测投影在几何对应的极线上满足导数相等条件，从而将正则化约束拓展至未被直接观测的角度区域。

最终训练损失为两者的加权和：
$$\mathcal{L} = \mathcal{L}_{\mathrm{Recon}} + \lambda \mathcal{L}_{\mathrm{ECC}}$$

**输入输出流**：系统输入为有限角度范围的锥束 CT 投影图像及对应的几何标定参数。训练时，射线批次从两部分来源采样——有限角度区域用于 $\mathcal{L}_{\mathrm{recon}}$，全角度随机采样用于 $\mathcal{L}_{\mathrm{ECC}}$。输出为优化后的神经衰减场，可在任意视角下渲染投影，或通过体素采样重建完整的三维 CT 体积。

**训练策略**：前 200 个 epoch 作为预热阶段，仅优化 $\mathcal{L}_{\mathrm{recon}}$，随后引入 $\mathcal{L}_{\mathrm{ECC}}$ 联合训练。正则化权重 $\lambda$ 根据角度范围调整：角度低于 120° 时设为 $10^{-3}$，120° 时设为 $10^{-4}$，以适应不同不适定程度下的正则化强度需求。

### 补充图表

![[assets/figures/papers/paper_list_l24_https_arxiv_org_abs_2411_06181v1/figures/002_Figure_2.jpg]]
*Figure 2: Epi-NAF Method Overview. On the left part of the figure, we mark the limited-angle region of the provided projections in green, and the unseen projections region in red. Epi-NAF comprises two loss terms: (1) ${ \mathcal { L } } _ { \mathrm { r e c o n } }$ . , based on the $L _ { 2 }$ difference between the predicted and ground-truth intensity values (green pixels), and (2) our novel $\mathcal { L } _ { \mathrm { E C C } }$ , which enforces consistency in the derivatives in the t direction of line integrals along corresponding epipolar lines (blue pixels). Crucially, projection (iii) receives direct supervision from the input, which is propagated to projections (i) and (ii) via the ECC loss. This...

## 核心模块与公式推导

### 方法总览

Epi-NAF 在 vanilla NAF 的神经衰减场框架上引入极线一致性正则化，其训练流程由四个核心模块构成：**神经衰减场（MLP）**、**可微渲染（Beer-Lambert积分）**、**重建损失（L_recon）** 和 **极线一致性损失（L_ECC）**。总体损失函数为两者的加权和：

$$\mathcal{L} = \mathcal{L}_{\mathrm{Recon}} + \lambda \mathcal{L}_{\mathrm{ECC}}$$

其中正则化权重 $\lambda$ 根据有限角度范围调整：角度低于 120° 时 $\lambda=10^{-3}$，120° 时 $\lambda=10^{-4}$。训练前 200 个 epoch 仅优化 $\mathcal{L}_{\mathrm{Recon}}$ 作为预热，以增强后续加入 $\mathcal{L}_{\mathrm{ECC}}$ 时的稳定性。

### 模块一：神经衰减场（MLP）

一个多层感知机 $\phi$ 将三维空间坐标映射为衰减系数 $\mu$，即 $\phi: \mathbb{R}^3 \to \mathbb{R}$。该 MLP 是 vanilla NAF 与 Epi-NAF 共享的基础表示网络，网络架构和训练配置在两种方法中保持一致。

### 模块二：可微渲染（Beer-Lambert 积分）

基于衰减系数场，沿射线 $\mathbf{r}$ 对衰减系数进行积分，得到预测的 X 射线强度：

$$\hat{I}(\mathbf{r}) = I_0 \exp\left(-\sum_{i=1}^{N} \mu_i \delta_i\right)$$

其中 $I_0$ 为入射 X 射线强度，$\mu_i$ 为射线上第 $i$ 个采样点的衰减系数，$\delta_i$ 为采样步长。该渲染过程完全可微，允许梯度从投影图像反向传播至 MLP 参数。

### 模块三：重建损失（L_recon）

在有限角度范围内的输入投影上计算像素级均方误差：

$$\mathcal{L}_{\mathrm{recon}} = \frac{1}{|\Omega_{recon}|} \sum_{r \in \Omega_{recon}} \|\hat{I}(r) - I(r)\|_2^2$$

其中 $\Omega_{recon}$ 为从有限角度输入投影中采样的训练射线批次，$\hat{I}(r)$ 为预测投影强度，$I(r)$ 为真实测量投影强度。该损失仅对有限角度范围内的观测投影提供直接监督，未观测角度区域缺乏约束。

### 模块四：极线一致性损失（L_ECC）

L_ECC 是 Epi-NAF 的核心创新，其理论基础是 X 射线成像中的极线一致性条件。考虑两个不同源位置的余弦加权投影图像 $\tilde{P}_0$ 和 $\tilde{P}_1$，对应极线由角度 $\alpha$ 和到原点的距离 $t$ 定义，一致性条件要求对应极线上 Radon 变换的导数相等：

$$\frac{\partial}{\partial t} \mathcal{R}_{\tilde{P}_0}(\alpha_0, t_0) = \frac{\partial}{\partial t} \mathcal{R}_{\tilde{P}_1}(\alpha_1, t_1)$$

在实际计算中，通过中心差分近似导数。对于每条极线 $l_i = P_i(\alpha_i, t_i)$，采样两条偏移线 $l_i^+ = P_i(\alpha_i, t_i + \epsilon)$ 和 $l_i^- = P_i(\alpha_i, t_i - \epsilon)$，其中 $\epsilon$ 为小偏移量。导数近似为 $(\hat{I}(l_i^+) - \hat{I}(l_i^-)) / (2\epsilon)$。极线一致性损失定义为两条对应极线上导数近似积分差值的平方 L2 范数：

$$\mathcal{L}_{\mathrm{ECC}} = \left\| \sum_{j=1}^{N_s} \Delta_{0,j} \delta_0 - \Delta_{1,j} \delta_1 \right\|_2^2$$

其中 $\Delta_{i,j}$ 为第 $i$ 条极线上第 $j$ 个采样点处的导数近似，$\delta_i$ 为采样步长，$N_s$ 为极线上的采样点数。

在每次训练迭代中，除从有限角度输入投影采样射线外，还从整个 180° 范围随机采样一对投影角度，计算 L_ECC。这一机制将输入投影的监督信息传播至全角度范围的预测投影，从而正则化未被直接观测的角度区域，缓解 vanilla NAF 在未观测角度缺乏约束导致的模糊和伪影问题。

## 实验与分析

### 定量评估

Epi-NAF 在四个 CT 扫描数据集（胸部、腹部、足部、下颌）及多种有限角度配置下进行了评估，与四个基线方法对比：**FDK**（Feldkamp et al., JOSA A, 1984）、**SART**（Andersen et al., Ultrasonic Imaging, 1984）、**ASD-POCS**（Sidky et al., PMB, 2008）以及 **vanilla NAF**（Zha et al., MICCAI 2022）。

从 Table 1 的主结果来看，Epi-NAF 在所有扫描和角度设定下均一致优于 vanilla NAF。以 60° 有限角度为例，胸部 CT 上 PSNR 从 20.4 提升至 21.57（+1.17 dB），SSIM 从 0.678 提升至 0.724（+0.046）；腹部 CT 上 PSNR 从 25.75 提升至 26.1（+0.35 dB），SSIM 从 0.858 提升至 0.863（+0.005）。在 90° 设定下，胸部 CT 的 PSNR 从 24.78 提升至 25.73（+0.95 dB），SSIM 从 0.834 提升至 0.856（+0.022）。在更极端的 45° 条件下，胸部 CT 的 PSNR 从 19.1 提升至 19.6（+0.5 dB），SSIM 从 0.591 提升至 0.606（+0.015）；足部 CT 的 PSNR 从 24.7 提升至 24.9（+0.2 dB），SSIM 从 0.835 提升至 0.849（+0.014）。

![[assets/figures/papers/paper_list_l24_https_arxiv_org_abs_2411_06181v1/figures/003_Table_1.jpg]]
*Table 1: PSNR/SSIM compared to ground-truth CT scans, of Epi-NAF and baselines. Best results are in bold*

这些结果表明，$L_{\mathrm{ECC}}$ 的引入在不同解剖部位和角度缺失程度下均能带来一致的性能增益，且在角度范围越受限（问题越不适定）时，正则化的作用越明显。但需注意，在部分设置下 PSNR/SSIM 的绝对提升幅度较小（如腹部 60° 仅 +0.35 dB），标准图像重建指标可能不足以完全反映临床意义上的改善。

### 定性分析

Figure 3 展示了 90° 有限角度下胸部与腹部 CT 的重建切片对比。Vanilla NAF 在低密度区域出现了明显的“幻觉”现象——即在应为低衰减系数的区域错误地重建出高密度结构。Epi-NAF 通过 $L_{\mathrm{ECC}}$ 正则化显著缓解了这一问题，重建结果中的伪影大幅减少，组织边界更加清晰，整体更接近真实 CT 图像。

### 消融与训练策略

Epi-NAF 的核心消融即与 vanilla NAF 的直接对比：后者仅使用重建损失 $L_{\mathrm{recon}}$，前者在此基础上加入 $L_{\mathrm{ECC}}$。Table 1 中 NAF 与 Epi-NAF 各行的对比构成了完整的消融证据，验证了极线一致性损失在有限角度 CT 重建中的有效性。

训练策略上，论文采用了两个关键设计：
1. **预热阶段**：前 200 个 epoch 仅优化 $L_{\mathrm{recon}}$，之后引入 $L_{\mathrm{ECC}}$。这一设计旨在让神经场先学习一个合理的初始衰减系数分布，避免早期训练中 ECC 损失在高度欠拟合的场上的不稳定梯度影响收敛。
2. **自适应正则化权重**：损失权重 $\lambda$ 根据角度范围动态调整——角度范围低于 120° 时设为 $10^{-3}$，120° 时设为 $10^{-4}$。这一策略反映了问题不适定程度对正则化强度的需求差异：角度范围越小，未观测区域越大，需要更强的 ECC 约束。

### 失败模式与局限性

尽管 Epi-NAF 在定性和定量上均展现出改进，但仍存在以下局限：

- **欠定问题的本质限制**：有限角度 CT 重建本质上是严重欠定的逆问题。即使在 $L_{\mathrm{ECC}}$ 正则化下，重建结果仍存在一定程度的模糊和细节丢失，尤其在极度有限角度（如 45°）下，部分精细结构无法恢复。
- **超参数敏感性未充分探索**：正则化权重 $\lambda$ 和预热轮次对性能有直接影响，但论文仅提供了经验设定，未进行系统性的超参数消融或敏感性分析。不同扫描协议和解剖部位下的最优配置可能不同，当前结论的泛化性需要进一步验证。
- **数值微分离散化的影响未知**：$L_{\mathrm{ECC}}$ 中用于近似导数的 $\epsilon$ 偏移量（通过采样 $l_i^+$ 和 $l_i^-$ 实现中心差分）对数值精度和最终重建质量的影响未被探讨。是否存在更稳健的离散化方案（如高阶差分或自动微分）仍是开放问题。
- **指标提升的临床意义存疑**：在部分设置下 PSNR/SSIM 的绝对提升较小（如腹部 60° 仅 +0.35 dB / +0.005），标准全参考指标可能无法捕捉临床诊断中关键的局部结构保真度改善。需要任务驱动的评估（如病灶检测率）来验证实际临床价值。
- **几何假设限制**：当前 ECC 损失依赖于圆形/半圆形锥束 CT 轨迹的极线几何关系，其在非理想几何标定或自由扫描轨迹（如 C 型臂）下的适用性尚未验证。实际噪声投影下的鲁棒性也需要进一步评估。

## 方法谱系与知识库定位

### 1. 方法谱系

Epi-NAF 直接建立在神经衰减场（Neural Attenuation Fields, NAF）框架之上。Vanilla NAF（Zha et al., MICCAI 2022）使用一个多层感知机（MLP）将三维空间坐标映射为衰减系数 $\mu$，并通过可微的 Beer-Lambert 积分渲染投影图像，训练时仅依赖有限角度输入投影上的 $L_2$ 重建损失。Epi-NAF 保留了 NAF 的完整架构与渲染管线，唯一的修改在于训练损失函数：在 $L_{\text{recon}}$ 之外引入了一个基于极线一致性条件（Epipolar Consistency Conditions, ECC）的正则化项 $L_{\text{ECC}}$，形成总损失 $\mathcal{L} = \mathcal{L}_{\text{Recon}} + \lambda \mathcal{L}_{\text{ECC}}$。这一修改使得原本仅作用于有限角度区域的监督信号，通过 ECC 的几何约束传播至全 180° 范围的预测投影，从而有效正则化未观测角度的重建。

在更广泛的有限角度 CT 重建方法谱系中，Epi-NAF 的定位如下：

| 方法 | 范式 | 核心机制 | 与 Epi-NAF 的关系 |
|------|------|----------|-------------------|
| **FDK**（Feldkamp et al., JOSA A, 1984） | 解析重建 | 锥束滤波反投影 | 经典解析基线，在有限角度下产生严重条纹伪影 |
| **SART**（Andersen et al., Ultrasonic Imaging, 1984） | 代数迭代重建 | 逐投影迭代更新 | 迭代优化基线，无显式先验约束 |
| **ASD-POCS**（Sidky et al., PMB, 2008） | 迭代重建 + 先验 | 全变分（TV）正则化 | 引入显式图像域先验，但非神经场方法 |
| **Vanilla NAF**（Zha et al., MICCAI 2022） | 神经场隐式重建 | MLP + 可微渲染 + $L_2$ 损失 | Epi-NAF 的直接基线，缺少未观测角度约束 |
| **Epi-NAF**（本文） | 神经场 + 几何正则化 | NAF + 极线一致性损失 | 在 NAF 基础上引入投影域几何一致性约束 |

Epi-NAF 的核心创新在于将经典 X 射线成像几何中的极线一致性条件（ECC）转化为神经场训练中的可微正则化损失，属于“几何先验驱动神经场优化”这一技术路线。与数据驱动先验（如扩散模型或生成对抗网络）不同，ECC 不依赖任何外部训练数据，而是利用 CBCT 成像几何的内在冗余性进行自监督正则化。论文明确指出 $L_{\text{ECC}}$ 具有即插即用特性，可服务于任何基于神经场的 CT 重建框架，这一推广性在后续工作中尚待验证。

### 2. 适用边界

Epi-NAF 的适用边界由以下条件界定：

- **成像几何假设**：ECC 损失依赖于圆形或半圆形锥束 CT（CBCT）轨迹下的极线几何关系。对于非标准源轨迹（如 C 型臂自由扫描）或扇束 CT 几何，当前的 $L_{\text{ECC}}$ 公式需要重新推导相应的极线参数化。
- **角度范围依赖**：正则化权重 $\lambda$ 需根据有限角度范围调整——角度低于 120° 时设为 $10^{-3}$，120° 时设为 $10^{-4}$。这表明方法的超参数与问题的欠定程度耦合，在不同角度配置下需要经验性调整。
- **训练稳定性需求**：需要 200 轮仅使用 $L_{\text{recon}}$ 的预热训练，以确保后续加入 $L_{\text{ECC}}$ 时优化稳定。这一设计暗示在训练早期直接施加几何约束可能导致收敛困难。
- **计算开销**：相较于 vanilla NAF，Epi-NAF 的计算开销增加至 1.5–3 倍，主要来源于每次迭代中额外采样的投影角度对及其极线渲染。

在实验覆盖范围内，方法在四种 CT 扫描（胸部、腹部、足部、颌骨）和多种有限角度配置（45°–120°）下均表现出一致的定量改善。然而，所有实验均在理想几何标定和无噪声投影条件下进行，实际临床场景中的噪声投影和非理想标定下的鲁棒性尚不明确。

### 3. 局限与开放问题

#### 3.1 已识别的局限

1. **重建质量的本质上限**：有限角度 CT 重建本质上是一个严重欠定逆问题。即使引入 ECC 正则化，重建结果仍存在一定程度的模糊和细节丢失。PSNR/SSIM 的绝对提升在某些设置下较为微小（如腹部 60° 下仅 +0.35 dB），标准图像重建指标可能不足以反映临床意义上的改进。

2. **超参数敏感性未系统分析**：正则化权重 $\lambda$ 和预热轮次仅提供了经验设定，论文未进行系统性的超参数消融或敏感性分析。不同扫描部位和角度范围下的最优超参数组合仍不明确。

3. **即插即用特性未验证**：尽管论文声称 $L_{\text{ECC}}$ 可作为即插即用模块用于任何神经场 CT 框架，但该声明仅在 NAF 上得到实验验证。在其他神经场方法（如 SNAF、IntraTomo）上的兼容性和有效性尚待实验证实。

4. **数值微分离散化方案单一**：$L_{\text{ECC}}$ 中极线上导数的近似采用中心差分，依赖一个偏移量 $\epsilon$。该偏移量的选择对数值精度和最终重建质量的影响未被讨论，是否存在更稳健的数值微分离散化方案也是一个开放问题。

#### 3.2 开放问题

1. **与数据驱动先验的融合**：ECC 作为一种几何先验，能否与数据驱动的先验（如扩散模型、生成对抗网络）协同工作，以在极度有限角度下恢复更丰富的纹理和结构信息？

2. **动态超参数策略**：200 轮预热期是否在所有场景下均为最优？能否通过动态调整 $\lambda$（如课程学习策略）在训练早期逐步引入几何约束，从而在保证稳定性的同时加速收敛？

3. **几何推广性**：如何将基于圆形锥束轨迹的 ECC 损失推广到更灵活的源轨迹（如 C 型臂自由扫描）或扇束 CT 几何？这需要重新推导对应几何下的极线参数化。

4. **鲁棒性验证**：在实际噪声投影和非理想几何标定条件下，极线一致性条件的鲁棒性如何？是否需要额外的校正模块（如几何标定网络或去噪预处理）来保证 $L_{\text{ECC}}$ 的有效性？

5. **临床相关性评估**：PSNR/SSIM 的提升在部分场景下幅度有限，需要任务驱动的评估（如病灶检测率、诊断准确率）来验证 ECC 正则化带来的改进是否具有临床意义。

## 原文 PDF

![[paperPDFs/ISBI_2025/Epi_NAF_Enhancing_Neural_Attenuation_Fields_for_Limited_Angle_CT_with_Epipolar_Consistency_Conditions.pdf]]
