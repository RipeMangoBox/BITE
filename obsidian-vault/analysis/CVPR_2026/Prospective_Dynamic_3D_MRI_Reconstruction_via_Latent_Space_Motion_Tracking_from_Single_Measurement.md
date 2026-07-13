---
title: Prospective Dynamic 3D MRI Reconstruction via Latent-Space Motion Tracking from Single Measurement
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Prospective_Dynamic_3D_MRI_Reconstruction_via_Latent_Space_Motion_Tracking_from_Single_Measurement.pdf
project_link: null
code_link: null
aliases:
- PD3MRLSMTFSM
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 学习一个低维、连续的潜在运动流形，从而将在线运动估计简化为低维潜在向量的快速优化。
primary_logic: 通过离线学习患者特异的三平面几何感知映射网络，将运动状态嵌入紧凑的潜在空间；在线阶段仅需几步优化即可从单次测量中恢复出非线性变形场，保持重建保真度和时间一致性。
claims:
- PDMR是首个利用非线性流形变形表征进行前瞻MRI重建的框架。
- PDMR仅需优化低维潜在向量，即可在几次迭代内恢复运动状态。
- 在院内腹部数据上，PDMR比SOTA方法MR-MOTUS的PSNR提高约2 dB。
- XCAT phantom (Immediate prospective) 上 PSNR (dB) = 26.28
---

# Prospective Dynamic 3D MRI Reconstruction via Latent-Space Motion Tracking from Single Measurement

> [!tip] 核心洞察
> 通过离线学习患者特异的三平面几何感知映射网络，将运动状态嵌入紧凑的潜在空间；在线阶段仅需几步优化即可从单次测量中恢复出非线性变形场，保持重建保真度和时间一致性。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于潜在空间运动追踪的前瞻性动态三维MRI重建 |
| 英文题名 | Prospective Dynamic 3D MRI Reconstruction via Latent-Space Motion Tracking from Single Measurement |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Chen_Prospective_Dynamic_3D_MRI_Reconstruction_via_Latent-Space_Motion_Tracking_from_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | PDMR |
| Dataset | XCAT phantom, In-house abdomen |

> [!tip] 效果简介
> - XCAT phantom (Immediate prospective) 上，PSNR (dB) 26.28 (outperforms all baselines)；SSIM 0.958 (outperforms all baselines)。
> - In-house abdomen (Immediate prospective) 上，PSNR (dB) 46.32 ± 4.06 vs MR-MOTUS (approximate) (~2 dB gain over MR-MOTUS)；SSIM 0.994 ± 0.003 (outperforms MR-MOTUS)。
> - XCAT phantom (Retrospective learning) 上，PSNR (dB) 26.63。

## 概要

动态三维MRI在腹部成像中面临一个核心矛盾：高时空分辨率与采集速度之间的根本性权衡。传统回顾式重建方法（如**GRASP-Pro** (Feng et al., Mag. Reson. Med. 2020)、**Deep Image Prior**）需要积累多帧k空间数据才能重建，无法满足实时引导干预（如放射治疗射束门控）对低延迟前瞻重建的需求。而现有在线前瞻方法——无论是基于线性变形场模型的**MR-MOTUS** (Huttinga et al., IEEE TMI 2022) 和**DREME-MR** (Shao et al., Phys. Med. Biol. 2025)，还是基于离散先验搜索的**Prior-INR** (Liu et al., Med. Phys. 2024)——均难以在超稀疏单次k空间测量下高效且准确地估计非线性、高维的3D变形场，限制了重建保真度和实时性。

针对这一瓶颈，本文提出**PDMR**（Prospective Dynamic MRI Reconstruction），据我们所知，这是首个利用非线性流形变形表征进行前瞻MRI重建的框架。其核心调控机制在于：通过离线学习一个低维、连续的潜在运动流形，将复杂的在线运动估计问题简化为低维潜在向量的快速优化——仅需几步迭代即可从单次测量中恢复当前运动状态，从而在保持重建保真度的同时实现低延迟。

PDMR的核心洞察是：离线阶段利用预扫描数据联合优化患者特异的三平面几何感知映射网络与潜在码，将运动状态嵌入紧凑的潜在空间；在线阶段冻结网络参数，仅优化潜在向量以匹配瞬时k空间测量。在XCAT数字体模和院内腹部DCE-MRI数据上的实验表明，PDMR在前瞻重建场景下显著优于现有方法，比SOTA方法MR-MOTUS的PSNR提高约2 dB（院内数据：46.32 ± 4.06 dB），且潜在向量的第一主成分与参考呼吸运动信号高度相关，验证了其运动可解释性。

动态磁共振成像（Dynamic MRI）通过连续采集时间序列图像，为临床诊断与治疗引导提供关键的运动信息，在腹部成像、心脏成像及放射治疗等场景中具有不可替代的价值。然而，MRI 固有的物理约束——较长的扫描时间与有限的采样速率——使得高时空分辨率动态成像始终面临严峻挑战。传统方法通常采用回顾式（retrospective）重建策略，即先完整采集所有时间帧的 k 空间数据，再通过后处理算法恢复图像序列。这类方法虽然能够利用全时序信息进行高质量重建，但其“先采集后重建”的范式天然存在一个致命缺陷：**无法在数据采集的同时实时输出重建结果**。

这一缺陷在需要即时反馈的临床应用中尤为突出。以 MRI 引导的放射治疗（MR-guided radiotherapy）为例，系统必须在毫秒级延迟内获取当前解剖结构的位置信息，才能精准调整辐射束以避开危及器官。回顾式方法因需要等待完整数据采集完成，其固有延迟动辄数秒甚至数十秒，完全无法满足此类**前瞻式（prospective）重建**的实时性要求。

前瞻式重建的核心困境在于信息与时间的双重约束：系统在每个时刻仅能获取**单次超稀疏 k 空间测量**（例如单根径向辐条），却必须从中估计出完整的三维动态图像。这本质上是一个极度欠定的逆问题。现有方法主要沿着两条技术路线展开：

- **线性变形场模型**：以 **MR-MOTUS**（Huttinga et al., IEEE TMI 2022）和 **DREME-MR**（Shao et al., Phys. Med. Biol. 2025）为代表，将三维变形场（Deformation Vector Field, DVF）表示为若干空间基函数的线性组合，在线阶段仅需估计少量基系数。这类方法的优势在于优化变量少、计算速度快，但其线性假设严重限制了模型对复杂非线性运动（如呼吸引起的器官滑动与形变）的表征能力。

- **离散先验搜索**：以 **Prior-INR**（Liu et al., Med. Phys. 2024）为代表，从预先构建的运动状态字典中检索最匹配的帧。该方法依赖离散的、有限数量的运动模板，无法捕捉连续运动轨迹中的细微变化，且字典的构建与存储成本随运动复杂度呈指数增长。

上述方法的共同瓶颈可归结为：**在超稀疏单次测量条件下，现有变形场表征方式要么过于刚性（线性假设），要么过于离散（字典搜索），均无法高效且准确地估计非线性、高维的三维变形场**。这一瓶颈直接限制了前瞻重建的保真度与时间一致性——当运动模式偏离训练分布时，重建图像会出现严重的伪影与解剖结构失真（见 Figure 1）。

一个自然的思路是：能否利用回顾式重建中已经积累的丰富运动先验，来赋能前瞻式重建？回顾式方法（如 **GRASP-Pro**, Feng et al., Mag. Reson. Med. 2020）虽然无法直接用于在线场景，但它们在离线阶段能够从完整时序数据中学习到高质量的运动模式。问题在于，如何将这些“回顾式先验”压缩为一种紧凑、连续且可快速查询的表示，使其在前瞻重建的严格延迟约束下仍能发挥作用。

本文提出的 **PDMR（Prospective Dynamic MRI Reconstruction）** 框架正是沿着这一思路展开。其核心洞见是：**通过离线学习一个患者特异的、低维连续的运动流形，将在线运动估计从高维变形场的直接优化转化为低维潜在向量的快速搜索**。具体而言，PDMR 在离线阶段利用预扫描的 k 空间数据，联合学习一个紧凑的潜在空间与一个几何感知的映射网络，将低维潜在向量（维度 r=12）非线性地映射为完整的三维变形场；在线阶段则冻结映射网络，仅需几步梯度下降即可从单次测量中恢复当前运动状态，从而实现高保真、低延迟的前瞻重建。

## 核心方法与创新机理

PDMR 的核心创新在于**将动态 MRI 前瞻重建中的高维变形场（DVF）估计问题，转化为在低维潜在流形上的快速优化问题**，从而在超稀疏单次 k 空间测量条件下实现高效、准确的非线性运动追踪。

### 关键改变点

| 设计维度 | 已有方法 | PDMR 方法 |
|---------|---------|----------|
| **变形场表示方式** | 线性组合空间基（MR-MOTUS, DREME-MR）或离散先验搜索（Prior-INR） | 连续非线性潜在流形：从低维潜在向量 $z \in \mathbb{R}^r$ 到 3D DVF 的非线性映射 |
| **在线优化变量** | 完整的 3D DVF 或空间基系数 | 仅优化低维潜在向量（$r=12$），冻结映射网络 |
| **运动映射网络** | 线性映射或无特定几何结构 | 几何感知的三平面生成器与轻量 MLP 解码器 |

**MR-MOTUS**（Huttinga et al., IEEE TMI 2022）和 **DREME-MR**（Shao et al., Phys. Med. Biol. 2025）均采用线性 DVF 模型，将变形场表示为空间基的线性组合。这种线性假设限制了其对复杂非线性运动（如呼吸引起的器官滑动、形变）的建模能力。**Prior-INR**（Liu et al., Med. Phys. 2024）虽引入先验搜索，但本质上仍是离散状态匹配，缺乏对连续运动流形的表达。

PDMR 的关键突破在于引入**流形 DVF 表征**（Eq. 4）：

$$\pmb{f} : \pmb{z} \in \mathbb{R}^{r} \mapsto \pmb{u} \in \mathbb{R}^{m \times 3}$$

这一映射将高维变形场（$m$ 个体素 × 3 个位移分量）压缩为低维潜在向量 $z$（$r=12$）。该映射由**几何感知的三平面网络**实现：潜在向量首先通过三平面生成器分解为三个正交特征平面（$xy$、$xz$、$yz$），随后对任意空间坐标 $\pmb{p}$ 拼接三平面特征（Eq. 5）：

$$\pmb{F}(\pmb{p}) = \pmb{F}_{xy}(x,y) \oplus \pmb{F}_{xz}(x,z) \oplus \pmb{F}_{yz}(y,z)$$

轻量 MLP 解码器接收该几何感知特征，预测该体素的位移向量。这种设计使网络显式地捕捉 3D 空间结构，从而生成更精确的非线性变形场。

### 两阶段范式：离线学习 + 在线优化

PDMR 采用“离线学习运动流形，在线优化潜在向量”的两阶段范式，这是实现低延迟前瞻重建的关键架构创新：

1. **离线流形学习**（Section 4.2）：利用预扫描动态数据，联合优化所有时间帧的潜在码 $\pmb{Z}$ 和映射网络参数 $(\psi, \theta)$，目标函数为测量一致性损失与 DVF 正则项的组合（Eq. 9）。该阶段学习出患者特异的、时间可泛化的连续运动流形。

2. **在线前瞻重建**（Section 4.3）：冻结映射网络参数 $(\psi^*, \theta^*)$，每帧仅优化潜在向量 $z_{t'}$ 以匹配瞬时 k 空间测量（Eq. 10）：

$$z_{t'} = \arg\min_{z} \left\| A_{t'} \mathbf{x}_{t'} - \mathbf{y}_{t'} \right\|_2^2$$

优化后的潜在向量通过映射网络生成当前 DVF，再扭曲静态模板得到重建图像（Eq. 11）。由于优化变量维度极低（$r=12$），仅需几次迭代即可收敛，大幅降低了在线计算延迟。

### 创新价值

这一设计从根源上解决了现有前瞻方法的瓶颈：线性模型无法准确表达复杂 3D 运动，而直接优化完整 DVF 又计算代价过高。PDMR 通过学习低维潜在流形，将在线运动估计简化为低维优化，在保持非线性建模能力的同时实现了高效推理。实验表明，该设计使 PDMR 在院内腹部数据上比 SOTA 方法 **MR-MOTUS** 的 PSNR 提高约 2 dB（Table 1），并展现出对未见运动偏移的强鲁棒性（Table 3）。

PDMR 的整体框架由**离线流形学习**与**在线前瞻重建**两个阶段构成，二者共享一个几何感知的变形场映射网络，形成“离线学习低维运动流形—在线快速潜变量优化”的闭环。

### 离线流形学习阶段

该阶段的目标是从预扫描的动态 k 空间数据中，学习一个患者特异的、连续的、可时序泛化的运动流形。其核心模块包括：

1. **三平面生成器（Tri-plane Generator）**：将低维潜在向量 $\mathbf{z} \in \mathbb{R}^r$（$r=12$）映射为三个正交特征平面 $\mathbf{F}_{xy}, \mathbf{F}_{xz}, \mathbf{F}_{yz}$，每个平面包含 32 个特征通道。
2. **MLP 解码器**：对于空间坐标 $\mathbf{p}$，从三个平面中采样并拼接特征 $\mathbf{F}(\mathbf{p}) = \mathbf{F}_{xy}(x,y) \oplus \mathbf{F}_{xz}(x,z) \oplus \mathbf{F}_{yz}(y,z)$，然后通过轻量级 MLP 预测该体素的三维位移，从而得到完整的变形场 $\mathbf{u} = \{ \mathbf{f}_{\psi,\theta}(\mathbf{z}, \mathbf{p}) \}_{\mathbf{p} \in \Omega}$。
3. **联合优化**：同时优化所有时间帧的潜在码 $\mathbf{Z}$ 和映射网络参数 $(\psi, \theta)$，目标函数为测量一致性损失与 DVF 时序平滑正则项的组合：
   $$\mathbf{Z}^*, \psi^*, \theta^* = \arg\min_{\mathbf{Z},\psi,\theta} \|\hat{\mathbf{Y}} - \mathbf{Y}\|_2^2 + \lambda \mathcal{R}(\mathbf{U})$$

### 在线前瞻重建阶段

当新一帧 k 空间测量 $\mathbf{y}_{t'}$ 到达时，冻结映射网络参数 $(\psi^*, \theta^*)$，**仅优化当前帧对应的潜在向量** $\mathbf{z}_{t'}$：
$$\mathbf{z}_{t'} = \arg\min_{\mathbf{z}} \|\mathbf{A}_{t'} \mathbf{x}_{t'} - \mathbf{y}_{t'}\|_2^2$$
其中 $\mathbf{x}_{t'} = \mathcal{W}(\mathbf{m}, \mathbf{f}_{\psi^*,\theta^*}(\mathbf{z}))$，即用当前潜在向量生成的 DVF 扭曲静态模板图像 $\mathbf{m}$。优化仅需几次迭代即可收敛，随后通过图像变形得到最终重建帧 $\hat{\mathbf{x}}_{t'} = \mathcal{W}(\mathbf{m}, \hat{\mathbf{u}}_{t'})$。

### 输入输出流

- **离线阶段输入**：预扫描动态 k 空间数据、静态模板图像 $\mathbf{m}$。
- **离线阶段输出**：优化后的潜在码 $\mathbf{Z}^*$、冻结的三平面生成器与 MLP 解码器参数。
- **在线阶段输入**：单次 k 空间测量 $\mathbf{y}_{t'}$、采样模式 $\mathbf{P}_{t'}$、静态模板 $\mathbf{m}$。
- **在线阶段输出**：当前帧重建图像 $\hat{\mathbf{x}}_{t'}$ 及对应的变形场 $\hat{\mathbf{u}}_{t'}$。

整个 pipeline 的架构概览如 **Figure 2** 所示。

![[assets/figures/papers/paper_list_l2576_https_openaccess_thecvf_com_content_CVPR2026_html_Chen_Prospective_Dynam/figures/002_Figure_2.jpg]]
*Figure 2: Overview of proposed PDMR. A. PDMR performs offline manifold learning, where the patient-specific motion manifold and DVF mapping network*

### 3.1 动态MRI前向模型与运动补偿分解

PDMR的核心问题建立在动态MRI的前向模型之上。对于时间帧 $t$，k空间测量 $\mathbf{y}_t$ 可表示为：

$$\mathbf{y}_t = \mathbf{P}_t \mathcal{T} \mathbf{x}_t + \mathbf{n}_t$$

其中 $\mathbf{x}_t$ 为待重建的动态图像，$\mathcal{T}$ 表示傅里叶变换，$\mathbf{P}_t$ 为当前帧的k空间采样掩码，$\mathbf{n}_t$ 为测量噪声。在超稀疏单次测量场景下，直接从 $\mathbf{y}_t$ 恢复 $\mathbf{x}_t$ 是高度病态的。

为降低问题维度，PDMR采用运动补偿分解，将动态图像表达为静态模板 $\mathbf{m}$ 经变形场 $\mathbf{u}_t$ 扭曲的结果：

$$\mathbf{x}_t = \mathcal{W}(\mathbf{m}, \mathbf{u}_t)$$

这一分解将重建问题转化为运动估计问题——只需从瞬时k空间测量中恢复变形场 $\mathbf{u}_t$，即可通过扭曲模板得到当前帧图像。然而，直接优化高维3D变形场（$m \times 3$ 维）在在线场景下仍然计算代价高昂且容易陷入局部最优。

### 4.1 流形变形场表征

PDMR的核心创新在于引入**非线性流形变形场表征**，将高维变形场压缩到低维潜在流形上。具体而言，变形场 $\mathbf{u} \in \mathbb{R}^{m \times 3}$ 被建模为低维潜在向量 $\mathbf{z} \in \mathbb{R}^r$ 的非线性映射：

$$\mathbf{f}: \mathbf{z} \in \mathbb{R}^r \mapsto \mathbf{u} \in \mathbb{R}^{m \times 3}$$

其中 $r \ll m \times 3$（实验中 $r=12$）。该映射函数 $\mathbf{f}$ 由**几何感知的三平面映射网络**实现，包含两个关键组件：

**三平面生成器**：将潜在向量 $\mathbf{z}$ 映射为三个正交特征平面 $\mathbf{F}_{xy}$、$\mathbf{F}_{xz}$、$\mathbf{F}_{yz}$。对于任意空间坐标 $\mathbf{p} = (x, y, z)$，通过双线性插值从三个平面提取特征并拼接：

$$\mathbf{F}(\mathbf{p}) = \mathbf{F}_{xy}(x, y) \oplus \mathbf{F}_{xz}(x, z) \oplus \mathbf{F}_{yz}(y, z)$$

**MLP解码器**：接收拼接后的几何感知特征 $\mathbf{F}(\mathbf{p})$，预测该空间位置的3D位移向量。遍历所有体素坐标 $\mathbf{p} \in \Omega$，即可获得完整变形场：

$$\mathbf{u} = \left\{ \mathbf{f}_{\psi, \theta}(z, \mathbf{p}) \right\}_{\mathbf{p} \in \Omega}$$

其中 $\psi$ 为三平面生成器参数，$\theta$ 为MLP解码器参数。三平面结构显式编码了空间几何关系，使得网络能够高效学习非线性的解剖运动模式。

### 4.2 离线流形学习

在离线阶段，PDMR利用预扫描动态数据联合学习潜在码 $\mathbf{Z} = \{\mathbf{z}_t\}$ 和映射网络参数 $(\psi, \theta)$。优化目标为测量一致性损失与变形场正则化的组合：

$$\mathbf{Z}^*, \psi^*, \theta^* = \arg\min_{\mathbf{Z}, \psi, \theta} \|\hat{\mathbf{Y}} - \mathbf{Y}\|_2^2 + \lambda \mathcal{R}(\mathbf{U})$$

其中 $\hat{\mathbf{Y}}$ 为根据估计变形场生成的k空间数据，$\mathbf{Y}$ 为实际采集数据，$\mathcal{R}(\mathbf{U})$ 为施加在变形场序列 $\mathbf{U}$ 上的时序平滑正则项（如总变分约束），$\lambda$ 控制正则化强度。该阶段不依赖外部标注，完全以自监督方式学习患者特异的连续运动流形。

### 4.3 在线潜在优化

在线前瞻重建阶段，映射网络参数 $(\psi^*, \theta^*)$ 被冻结，每帧仅需优化低维潜在向量 $\mathbf{z}_{t'}$ 以匹配瞬时k空间测量：

$$\mathbf{z}_{t'} = \arg\min_{\mathbf{z}} \|\mathbf{A}_{t'} \mathbf{x}_{t'} - \mathbf{y}_{t'}\|_2^2$$

其中 $\mathbf{x}_{t'} = \mathcal{W}(\mathbf{m}, \mathbf{f}_{\psi^*, \theta^*}(\mathbf{z}))$，$\mathbf{A}_{t'}$ 为包含采样掩码和傅里叶变换的前向算子。由于优化变量维度从完整变形场的 $m \times 3$ 维骤降至 $r=12$ 维，仅需几步梯度迭代即可收敛，满足在线重建的低延迟需求。最终，利用最优潜在向量生成的变形场扭曲静态模板，得到当前帧重建图像：

$$\hat{\mathbf{x}}_{t'} = \mathcal{W}(\mathbf{m}, \hat{\mathbf{u}}_{t'})$$

这一设计将计算瓶颈从在线优化转移至离线学习，实现了高质量前瞻重建与实时性之间的关键平衡。

## 实验与关键发现

### 实验设置与评估协议

PDMR在两类数据集上进行了验证：**XCAT数字体模**和**院内腹部DCE-MRI数据**。XCAT数据模拟呼吸运动，时间分辨率为每帧170 ms；院内数据采集自6名受试者，使用黄金角径向采样，共3500根辐条，每根辐条170 ms。实验分为两种重建场景：

- **前瞻重建（Prospective Reconstruction）**：模拟真实在线环境，分为“即时前瞻”（immediate prospective）和“2分钟延迟前瞻”（2-minute delayed prospective）两种设定，后者用于评估方法对运动漂移的鲁棒性。
- **回顾性学习（Retrospective Learning）**：利用预扫描数据离线学习运动流形，评估各方法在已知数据上的重建质量。

对比方法涵盖三类基线：在线前瞻方法**MR-MOTUS**（Huttinga et al., IEEE TMI 2022）、**DREME-MR**（Shao et al., Phys. Med. Biol. 2025）和**Prior-INR**（Liu et al., Med. Phys. 2024）；回顾性重建方法**GRASP-Pro**（Feng et al., Mag. Reson. Med. 2020）和**Deep Image Prior (DIP)**。所有基线使用原始论文默认配置及推荐超参数。评价指标为PSNR（dB）和SSIM。

> 需注意：比较在模拟放疗场景下进行，尚未在真实在线临床环境中验证实时性。

### 前瞻重建主结果

Table 1汇总了各方法在前瞻重建设定下的定量结果。PDMR在所有场景下均显著优于全部基线方法：

- **XCAT体模（即时前瞻）**：PDMR取得26.28 dB PSNR和0.958 SSIM，大幅领先所有对比方法。相比之下，线性DVF模型（MR-MOTUS、DREME-MR）和离散先验搜索方法（Prior-INR）在处理非线性、高维3D变形时均出现明显退化。
- **院内腹部数据（即时前瞻）**：PDMR取得46.32 ± 4.06 dB PSNR和0.994 ± 0.003 SSIM，相比当前SOTA在线方法**MR-MOTUS**提升约2 dB PSNR。这一增益源于PDMR的非线性流形表征能力——仅需优化低维潜在向量（r=12）即可从单次k空间测量中恢复出精细的3D变形场，而线性基方法受限于表达能力，难以捕捉复杂的呼吸运动模式。
- **2分钟延迟前瞻**：PDMR在院内数据上仍保持44.62 dB PSNR，表明其对运动漂移具有良好的时序泛化性。

Figure 3的定性比较进一步验证了上述结论：PDMR重建的图像在z-t剖面线上与参考图像高度一致，误差图显著低于其他方法，尤其在膈肌等大位移区域表现出明显优势。

### 变形场估计质量

Figure 4可视化了前瞻重建过程中估计的变形向量场（DVF）。PDMR估计的DVF在冠状面和矢状面上均呈现出平滑、生理合理的运动模式，与呼吸周期中的器官位移规律一致。相比之下，线性模型方法估计的DVF存在明显的空间不连续性，尤其在运动幅度较大的区域出现失真。这表明三平面几何感知映射网络有效捕捉了3D运动的非线性结构，使得从低维潜在向量解码出的DVF保持了空间平滑性和解剖一致性。

### 回顾性学习结果

Table 2报告了回顾性学习阶段的定量比较。PDMR在院内数据上取得47.60 ± 3.44 dB PSNR和0.995 ± 0.002 SSIM，在XCAT体模上取得26.63 dB PSNR和0.959 SSIM，均优于所有对比方法。回顾性学习的高质量重建为后续在线前瞻重建提供了可靠的运动流形先验，是PDMR整体性能的基础保障。

### 潜在空间分析与运动泛化

**潜在空间连续性与可解释性**：Figure 5展示了在两个潜在向量（分别对应吸气和呼气状态）之间进行线性插值生成的图像和DVF。插值结果呈现出平滑、自然的运动过渡，验证了所学流形的连续性和物理合理性。Figure 6进一步表明，潜在向量的第一主成分与参考膈肌运动信号高度相关（需人工核实相关系数），证实潜在码有效捕捉了呼吸运动的主要变化模式。

**未见运动的鲁棒性**：Table 3展示了PDMR在3 mm额外运动偏移下的鲁棒性量化结果。即使面对训练分布之外的偏移，PDMR仍可实现38.80 dB PSNR，表明其具有较强的运动泛化能力。然而，需注意该测试仅在3 mm偏移范围内进行，更大或更复杂的运动模式仍需进一步验证。

### 失败模式与局限性

1. **患者特异性限制**：PDMR的离线流形学习需针对每位患者定制，不同患者之间无法共享模型，限制了其在大规模临床部署中的通用性。
2. **采样轨迹依赖**：离线流形学习依赖于黄金角径向采集的预扫描数据。对于其他k空间采样轨迹，方法需重新训练，缺乏即插即用能力。
3. **运动偏移范围有限**：对未见运动的鲁棒性仅在3 mm偏移范围内验证，更大幅度的运动漂移或非周期性运动（如咳嗽、体位变化）可能导致性能下降。
4. **临床验证不足**：实验仅使用XCAT体模和6名受试者的院内数据，缺乏多中心、大规模临床真实数据测试，且未在真实在线环境中验证毫秒级延迟的可行性。
5. **流形维度敏感性**：流形维度r的选择对性能的影响尚未系统研究——r过低可能欠拟合运动多样性，r过高则增加在线优化负担和过拟合风险。

### 开放问题

- 如何利用历史回顾性数据加速流形学习，减少预扫描时间？
- 如何将该框架扩展至自适应采样，使采样模式根据当前运动状态动态调整？
- 流形维度r的最优选择策略是什么？是否存在自适应确定r的机制？
- 在真实在线环境中，如何实现毫秒级延迟以满足临床实时性要求？

![[assets/figures/papers/paper_list_l2576_https_openaccess_thecvf_com_content_CVPR2026_html_Chen_Prospective_Dynam/figures/005_Table_1.jpg]]
*Table 1: Quantitative results (PSNR (dB)/SSIM) of compared methods on the XCAT phantom and in-house datasets under immediate and 2-minute delayed prospective reconstruction settings. The best results are highlighted in bold*

![[assets/figures/papers/paper_list_l2576_https_openaccess_thecvf_com_content_CVPR2026_html_Chen_Prospective_Dynam/figures/003_Figure_3.jpg]]
*Figure 3: Qualitative comparisons of prospective reconstruction results on the in-house dataset (top row) and the XCAT dataset (bottom row). We display the reconstructed images, the over-time profile lines in the z–t plane, and the corresponding error maps. The selected z-axis location is marked by an orange dashed line, and zoom-in boxes highlight regions of interest at the end-inhale and end-exhale motion states for improved visualization of motion capture. Red arrows indicate noticeable small-motion capture failures in the baselines*

![[assets/figures/papers/paper_list_l2576_https_openaccess_thecvf_com_content_CVPR2026_html_Chen_Prospective_Dynam/figures/004_Figure_4.jpg]]
*Figure 4: Visualization of the estimated DVFs during prospective reconstruction on the in-house dataset (coronal view) and the XCAT dataset (sagittal view)*

![[assets/figures/papers/paper_list_l2576_https_openaccess_thecvf_com_content_CVPR2026_html_Chen_Prospective_Dynam/figures/006_Table_2.jpg]]
*Table 2: Quantitative results (PSNR (dB)/SSIM) of compared methods on the XCAT phantom and in-house datasets during retrospective learning. The best results are highlighted in bold*

![[assets/figures/papers/paper_list_l2576_https_openaccess_thecvf_com_content_CVPR2026_html_Chen_Prospective_Dynam/figures/007_Figure_5.jpg]]
*Figure 5: Visualization of reconstructed MR images and corresponding DVFs obtained from interpolating between two latent vectors, where*

## 定位与知识库关联

### 与基线方法的关系

**PDMR** 的核心贡献在于将动态 MRI 前瞻重建中的变形场（DVF）表征从线性空间或离散先验搜索推进到**连续非线性潜在流形**，从而在超稀疏单次 k 空间测量下实现高效、高保真的运动追踪。下面从变形场表征方式和在线优化策略两个维度，梳理 PDMR 与现有工作的关系。

**1. 线性 DVF 模型基线**

**MR-MOTUS** (Huttinga et al., IEEE TMI 2022) 和 **DREME-MR** (Shao et al., Phys. Med. Biol. 2025) 是当前在线前瞻重建的代表性方法，均采用线性组合空间基来表征变形场。这类方法将 3D DVF 表示为若干空间基函数的线性叠加，在线阶段优化基系数以匹配瞬时 k 空间测量。其优势在于计算效率高，但线性基的表达能力有限，难以捕捉呼吸运动中的非线性、高维变形模式——这正是 PDMR 试图突破的瓶颈。

PDMR 将 DVF 表征替换为从低维潜在向量 $\mathbf{z} \in \mathbb{R}^r$ 到高维变形场 $\mathbf{u} \in \mathbb{R}^{m \times 3}$ 的非线性映射 $\mathbf{f}$（Eq. 4），使运动状态嵌入一个紧凑的连续流形。在线阶段仅需优化 $r=12$ 的潜在向量，而非完整的 3D DVF 或空间基系数。在院内腹部数据上，PDMR 的 PSNR 比 MR-MOTUS 提高约 2 dB（Table 1），验证了非线性流形表征在前瞻重建中的优势。

**2. 离散先验搜索基线**

**Prior-INR** (Liu et al., Med. Phys. 2024) 采用另一种策略：从预扫描数据中构建离散的运动先验库，在线阶段通过搜索匹配当前测量。这种方法本质上仍受限于先验库的离散性和覆盖范围，无法泛化到未见运动模式。

相比之下，PDMR 学习的是一个**连续流形**，潜在空间中的插值可直接生成物理上有意义的中间运动状态（Figure 5 展示了从吸气到呼气状态的平滑过渡），从而具备更好的运动泛化能力。Table 3 显示，即使面对 3 mm 的未见运动偏移，PDMR 仍可实现 38.80 dB PSNR。

**3. 回顾性重建基线**

**GRASP-Pro** (Feng et al., Mag. Reson. Med. 2020) 和 **Deep Image Prior (DIP)** 是典型的回顾性重建方法，它们利用全部测量数据（包括未来帧）进行离线重建，无法满足前瞻场景的实时性要求。Figure 1 说明了回顾性方法在前瞻重建中面临的挑战：无法访问未来数据，且需在极低延迟下完成重建。PDMR 通过离线流形学习将计算负担前移，在线阶段仅需几步优化即可恢复运动状态，从而弥合了回顾性高质量重建与前瞻实时性需求之间的鸿沟。

### 适用边界

PDMR 的设计基于以下关键假设和条件，超出这些边界时性能可能下降或方法不再适用：

- **采集轨迹依赖**：离线流形学习依赖于黄金角径向采集（golden-angle radial acquisition）的预扫描数据，以确保 k 空间采样的准均匀性和时间一致性。若更换为其他采样轨迹（如笛卡尔采样），需重新训练映射网络，方法无法直接迁移。
- **患者特异性**：映射网络和潜在流形是针对每位患者单独学习的，不同患者之间无法共享模型。这限制了方法的通用性和部署效率。
- **运动模式范围**：对未见运动的鲁棒性仅在 3 mm 偏移范围内得到验证（Table 3）。更大振幅或更复杂的运动模式（如咳嗽、突发体动）可能需要额外的机制来保证重建质量。
- **数据规模**：验证仅在 XCAT 数字体模和包含 6 名受试者的院内腹部 DCE-MRI 数据集上进行，缺乏多中心、大规模临床真实数据的测试。

### 局限与开放问题

**已知局限**

1. **患者定制化的代价**：每个患者需单独进行离线流形学习，增加了临床工作流程的复杂性和准备时间。如何利用历史回顾性数据加速流形学习，是降低部署成本的关键方向。
2. **采样轨迹的刚性依赖**：方法假设预扫描和在线扫描使用相同的黄金角径向轨迹，限制了其在多样化采集协议中的适用性。
3. **运动泛化边界未充分探索**：对未见运动的鲁棒性仅在有限偏移范围内测试，更大或更复杂的运动模式仍需验证。
4. **实时性未在真实环境中验证**：虽然理论上在线优化仅需几步迭代，但所有实验均在模拟放疗场景下进行，未在真实在线临床环境中验证毫秒级延迟的可行性。

**开放问题**

- 如何将该框架扩展至**自适应采样**（adaptive sampling），使 k 空间采集策略根据当前运动状态动态调整？
- 流形维度 $r$ 的选择对运动表征能力和在线优化效率的 trade-off 如何定量分析？
- 在真实在线环境中，如何实现端到端的毫秒级延迟，包括数据采集、潜在优化和图像重建？
- 是否可以将患者特异性流形学习替换为群体水平的预训练模型，再通过少量在线数据快速微调？

## 原文 PDF

![[paperPDFs/CVPR_2026/Prospective_Dynamic_3D_MRI_Reconstruction_via_Latent_Space_Motion_Tracking_from_Single_Measurement.pdf]]
