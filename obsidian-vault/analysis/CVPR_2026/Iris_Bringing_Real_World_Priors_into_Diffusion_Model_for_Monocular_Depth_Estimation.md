---
title: "Iris: Bringing Real-World Priors into Diffusion Model for Monocular Depth Estimation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Iris_Bringing_Real_World_Priors_into_Diffusion_Model_for_Monocular_Depth_Estimation.pdf
project_link: null
code_link: "https://github.com/NUST-Machine-Intelligence-Laboratory/Iris"
aliases:
- Iris
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 通过两阶段确定性扩散框架，在高时间步（低SNR）用频谱门控蒸馏引入真实世界低频先验，在低时间步（高SNR）用合成数据细化高频几何，并利用频谱门控一致性跨阶段传递高频细节。
primary_logic: 分离扩散时间步上的先验注入与几何细化，利用傅里叶域可学习门控选择性蒸馏可靠低频信息并保留高频细节的自由度，从而在有限数据下实现域泛化强、细节丰富的深度估计。
claims:
- Iris achieves the best overall performance among all 16 methods, ranking first in both All Avg Ranking and Group Avg Ranking.
- Two-stage PGD fully exploits real-world priors and validates the necessity of stage decoupling, with SGC further improving performance.
- Iris delivers stronger cross-domain generalization and consistent gains on real-image benchmarks compared to prior diffusion methods, while matching or surpassing DAv2 on several...
- KITTI 上 AbsRel↓ / δ1↑ = 7.2 / 94.5
---

# Iris: Bringing Real-World Priors into Diffusion Model for Monocular Depth Estimation

> [!tip] 核心洞察
> 分离扩散时间步上的先验注入与几何细化，利用傅里叶域可学习门控选择性蒸馏可靠低频信息并保留高频细节的自由度，从而在有限数据下实现域泛化强、细节丰富的深度估计。

| 字段 | 内容 |
|------|------|
| 中文题名 | Iris：将真实世界先验引入扩散模型用于单目深度估计 |
| 英文题名 | Iris: Bringing Real-World Priors into Diffusion Model for Monocular Depth Estimation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.16340) · [Code](https://github.com/NUST-Machine-Intelligence-Laboratory/Iris) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | Iris |
| Dataset | KITTI, NYUv2, ETH3D, ScanNet |

> [!tip] 效果简介
> - KITTI 上，AbsRel↓ / δ1↑ 7.2 / 94.5 vs Depth Anything V2: 7.4 / 94.6 (-0.2)。
> - NYUv2 上，AbsRel↓ / δ1↑ 4.9 / 97.4 vs Depth Anything V2: 4.5 / 97.9 (+0.4)。
> - ETH3D 上，AbsRel↓ / δ1↑ 5.5 / 97.6 vs Lotus-D: 6.1 / 97.0 (-0.6)。

## 概要

单目深度估计（MDE）长期面临一个核心瓶颈：传统前馈方法依赖海量训练数据但细节模糊，而扩散方法虽有生成先验却在合成到真实的域迁移中泛化不足。更隐蔽的问题是频率-可靠性不匹配——真实伪标签低频可信、高频不可信，与合成真值的高频精确形成冲突，单阶段训练难以调和。

Iris 通过一个**两阶段确定性扩散框架**解开这一死结。其核心洞察是：将先验注入与几何细化沿扩散时间步分离——在高时间步（低 SNR）用频谱门控蒸馏引入真实世界低频先验，在低时间步（高 SNR）用合成数据细化高频几何，并利用频谱门控一致性跨阶段传递高频细节。

**方法定位**：Iris 属于基于扩散的确定性深度估计方法，与 **Marigold**（Ke et al., CVPR 2024）的多步随机扩散和 **Lotus-D** 的单阶段确定性扩散形成对比。它同时吸收了 **Depth Anything V2**（Yang et al., NeurIPS 2024）在大规模真实数据上的先验优势，但仅使用 59K 合成图像与 100K 真实图像（SA-1B 伪标签）进行训练，数据效率显著更高。

**主要结果**：在零样本仿射不变深度估计的 16 种方法比较中，Iris 取得最优综合排名（All Avg Ranking 和 Group Avg Ranking 均列第一）。在 KITTI 上与 Depth Anything V2 持平（AbsRel 7.2 vs 7.4），在 ETH3D 和 ScanNet 上显著超越 Lotus-D，并展现出更强的跨域泛化能力和细节保真度。推理效率方面，在 NVIDIA A100 上 1536² 分辨率下单次推理速度优于 Depth Anything V2，远快于迭代扩散方法。

单目深度估计（Monocular Depth Estimation, MDE）是计算机视觉中的基础任务，旨在从单张RGB图像恢复逐像素的深度信息。近年来，该领域沿着两条主线演进：**前馈判别式方法**与**扩散生成式方法**，二者呈现出明显的互补特性。

**前馈方法的瓶颈**：以 **Depth Anything V2**（Yang et al., NeurIPS 2024）为代表的大规模前馈方法，通过在数千万级真实图像上训练，获得了准确的全局布局和尺度估计能力。然而，这类方法受限于监督信号的模糊性——真实场景的伪标签往往在低频结构上可靠，但在高频细节和物体边界处趋于平滑，导致预测结果缺乏精细的几何纹理（见 Figure 1b）。

**扩散方法的困境**：基于预训练Stable Diffusion的扩散方法（如 **Marigold**（Ke et al., CVPR 2024）、**Lotus-D**、**GenPercept**（Xu et al., ICLR 2025））虽能借助生成先验保留丰富的细节和锐利边界（见 Figure 1d），却面临**合成到真实的域迁移**（synthetic-to-real domain gap）问题——这些方法通常在合成数据集上训练，其学到的先验难以泛化到真实世界的复杂场景中。

**核心矛盾：频率-可靠性不匹配**。上述困境的根源在于一种深层的频率-可靠性不匹配：真实世界的伪标签在低频分量（全局布局、尺度关系）上较为可靠，但在高频分量（边界、纹理细节）上噪声较大；相反，合成数据的真值在高频几何上精确，却缺乏真实场景的多样性。单阶段训练无法有效调和这一矛盾——若同时监督高低频，模型要么被真实伪标签的高频噪声污染，要么被合成数据的有限多样性束缚。

**Iris的动机**：本文观察到前馈方法与扩散方法在频谱上的互补性（Figure 1），提出核心假设——**将真实世界先验的注入与几何细节的细化在扩散时间步上解耦**，可以系统性地解决上述矛盾。具体而言，在高时间步（低SNR）引入真实数据的低频先验以建立正确的全局结构，在低时间步（高SNR）利用合成数据细化高频几何，并通过傅里叶域的可学习门控机制选择性传递可靠信息。这一思路催生了Iris的两阶段先验到几何确定性（Priors-to-Geometry Deterministic, PGD）框架。

## 核心方法与创新机理

Iris的核心创新在于通过**两阶段确定性扩散框架**与**频谱门控机制**，系统性地解决了扩散模型在单目深度估计中“合成到真实域迁移”与“频率-可靠性不匹配”两大瓶颈。

### 瓶颈分析：两类方法的互补性与频率鸿沟

传统前馈方法（如 **Depth Anything V2**，Yang et al., NeurIPS 2024）依赖海量真实数据训练，能提供准确的全局布局与尺度，但输出细节趋于平滑。扩散方法（如 **Marigold**，Ke et al., CVPR 2024；**Lotus-D**）得益于生成先验，能保留锐利边界和丰富纹理，却因合成数据训练导致真实场景泛化不足。Figure 1直观展示了这种互补特性：DAv2的深度图边界模糊，而扩散方法边界清晰但存在域迁移误差。

更深层的矛盾在于**频率-可靠性不匹配**：真实图像伪标签的低频分量（布局、尺度）相对可信，高频分量（纹理细节）则充满噪声；合成真值恰好相反，高频几何精确但缺乏真实场景的布局多样性。单阶段训练无法调和这一矛盾——同时监督会导致高频伪影污染细节，或低频先验注入不足。

### 关键创新一：先验到几何的两阶段确定性框架（PGD）

Iris提出**Priori-to-Geometry Deterministic (PGD)** 框架，将扩散过程沿时间步解耦为两个阶段：

- **先验阶段（Prior Stage）**：在高时间步 $t_{\mathrm{high}}=1000$（低SNR状态）下运行，此时扩散模型的潜变量主要编码全局结构信息。该阶段通过真实图像伪标签注入低频先验，生成初始深度潜变量 $\hat{z}_{\mathrm{prior}}^{y}$，捕获场景布局与尺度。
- **几何阶段（Geometry Stage）**：以先验阶段输出为输入，在低时间步 $t_{\mathrm{low}}=500$（高SNR状态）下利用合成数据真值监督，细化高频几何细节，输出最终潜变量 $\hat{z}_{\mathrm{geo}}^{y}$。

两阶段共享同一UNet权重，但通过不同扩散状态实现先验注入与几何细化的功能分离。消融实验（Table 3）证实：两阶段PGD相比单阶段同时监督有显著提升，验证了阶段解耦的必要性。

### 关键创新二：频谱门控蒸馏（SGD）

先验阶段引入**Spectral-Gated Distillation (SGD)**，通过可学习的傅里叶低通门 $\mathcal{G}_{\phi}^{\mathrm{low}}$ 选择性对齐师生模型：

$$\mathcal{L}_{\mathrm{sgd}} = \mathbb{E}_{x \sim \mathcal{D}_{\mathrm{real}}} \| \mathcal{G}_{\phi}^{\mathrm{low}}(\hat{z}_{\mathrm{prior}}^{y}(x)) - \mathcal{G}_{\phi}^{\mathrm{low}}(z_{\mathrm{teach}}^{y}(x)) \|_2^2$$

低通门参数化截止频率与斜率，仅蒸馏可靠的布局与尺度信息，同时抑制教师伪标签的高频伪影。未被约束的高频分量则保留自由度，交由几何阶段处理。Figure 4可视化显示，SGD使师生在低频带高度一致，高频带则保持差异，防止噪声污染。

### 关键创新三：频谱门控一致性（SGC）

一个反直觉的发现是：先验阶段虽仅接受低频蒸馏，其输出却天然包含锐利边界和丰富纹理（Figure 2）。为利用这些“自发生成”的高频线索，Iris设计**Spectral-Gated Consistency (SGC)**，通过可学习高通门 $\mathcal{G}_{\psi}^{\mathrm{high}}$ 使几何阶段继承先验阶段的高频细节：

$$\mathcal{L}_{\mathrm{sgc}} = \mathbb{E}_{x \sim \mathcal{D}_{\mathrm{real}}} \| \mathcal{G}_{\psi}^{\mathrm{high}}(\hat{z}_{\mathrm{geo}}^{y}(x)) - \mathrm{sg}[\mathcal{G}_{\psi}^{\mathrm{high}}(\hat{z}_{\mathrm{prior}}^{y}(x))] \|_2^2$$

其中 $\mathrm{sg}[\cdot]$ 为停止梯度操作，防止阶段2的梯度反向传播破坏阶段1的先验学习。此外，SGC引入过激活约束以稳定训练。Table 3消融显示，去除SGC或过激活约束均导致精度下降，验证了该设计的有效性。

### 创新总结：从单阶段到频谱感知的两阶段范式

| 维度 | 基线方法 | Iris |
|------|----------|------|
| 训练策略 | 单阶段确定性扩散，仅合成数据监督 | 两阶段PGD：高时间步真实先验对齐 + 低时间步合成几何细化 |
| 频率处理 | 无显式频率分离 | SGD选择性蒸馏低频先验；SGC跨阶段传递高频细节 |
| 数据使用 | 仅合成数据集 | 59K合成图像 + 100K真实图像（DAv2伪标签） |

这三项创新协同作用：PGD提供时间步维度的任务解耦，SGD在频率维度过滤伪标签噪声，SGC在频率维度传递内部高频线索。最终损失函数为：

$$\mathcal{L} = \underbrace{\mathbb{E}_{x \sim \mathcal{D}_{\mathrm{syn}}} \| \hat{z}_{\mathrm{geo}}^{y} - z^{y} \|_2^2}_{\text{合成几何监督}} + \alpha \mathcal{L}_{\mathrm{sgd}} + \beta \mathcal{L}_{\mathrm{sgc}} + \gamma \mathcal{L}_{\mathrm{recon}}$$

其中 $\mathcal{L}_{\mathrm{recon}}$ 为图像重建辅助损失，用于保留Stable Diffusion骨干的细节建模能力。超参数消融（Table 4）确定最优设置为 $\alpha=1.0, \beta=0.1, \gamma=1.0$。

Iris 提出了一种名为 **先验到几何确定性（Priors-to-Geometry Deterministic, PGD）** 的两阶段扩散框架，用于单目深度估计。其核心设计理念是将真实世界先验的注入与高频几何细节的细化在扩散时间步上进行解耦，从而解决传统方法中合成到真实域迁移导致的泛化不足以及频率-可靠性不匹配问题。

### 两阶段确定性扩散流程

框架整体基于预训练的 Stable Diffusion 骨干网络，采用共享权重的 U-Net 作为深度预测器 $f_\theta$，在两个不同的扩散时间步上执行确定性推理：

1. **先验阶段（Prior Stage）**：在高时间步 $t_{\text{high}}=1000$（低信噪比状态）下，以带噪的 RGB 潜变量 $z^x$ 为输入，预测深度潜变量 $\hat{z}_{\text{prior}}^y = f_\theta(z^x, t_{\text{high}})$。该阶段通过频谱门控蒸馏（SGD）从冻结教师模型（DAv2）生成的伪标签中提取可靠的**低频布局先验**，捕获全局结构、尺度和场景布局。

2. **几何阶段（Geometry Stage）**：以先验阶段的输出 $\hat{z}_{\text{prior}}^y$ 作为输入，在低时间步 $t_{\text{low}}=500$（高信噪比状态）下预测精细化深度 $\hat{z}_{\text{geo}}^y = f_\theta(\hat{z}_{\text{prior}}^y, t_{\text{low}})$。该阶段利用合成数据的精确真值进行监督，恢复**高频几何细节**，同时通过频谱门控一致性（SGC）继承阶段一产生的高频边界和纹理信息。

两个阶段共享同一 U-Net 权重，形成端到端的确定性推理链路，无需迭代去噪，保证了推理效率。

### 频谱门控机制

为协调真实伪标签“低频可信、高频不可信”与合成真值“高频精确”之间的频率-可靠性不匹配，Iris 引入了两个可学习的傅里叶域门控模块：

- **频谱门控蒸馏（Spectral-Gated Distillation, SGD）**：部署于先验阶段，通过可学习低通门 $\mathcal{G}_\phi^{\text{low}}$ 选择性对齐师生模型在低频带的输出，抑制高频伪影向模型迁移。其损失函数为 $\mathcal{L}_{\text{sgd}} = \mathbb{E}_{x \sim \mathcal{D}_{\text{real}}} \| \mathcal{G}_\phi^{\text{low}}(\hat{z}_{\text{prior}}^y(x)) - \mathcal{G}_\phi^{\text{low}}(z_{\text{teach}}^y(x)) \|_2^2$。

- **频谱门控一致性（Spectral-Gated Consistency, SGC）**：部署于几何阶段，通过可学习高通门 $\mathcal{G}_\psi^{\text{high}}$ 强制阶段二的输出在**高频带**与阶段一保持一致，从而使阶段一的清晰边界和纹理细节传递至最终预测。该损失使用停止梯度操作以保证训练稳定性：$\mathcal{L}_{\text{sgc}} = \mathbb{E}_{x \sim \mathcal{D}_{\text{real}}} \| \mathcal{G}_\psi^{\text{high}}(\hat{z}_{\text{geo}}^y(x)) - \text{sg}[\mathcal{G}_\psi^{\text{high}}(\hat{z}_{\text{prior}}^y(x))] \|_2^2$。

### 训练数据流与损失函数

训练数据由两部分构成：59K 合成图像（Hypersim、Virtual KITTI 等）提供精确几何监督，100K 真实图像（SA-1B 子集，伪标签由 DAv2 教师生成）提供真实世界先验。综合损失函数为：

$$\mathcal{L} = \underbrace{\mathbb{E}_{x \sim \mathcal{D}_{\text{syn}}} \| \hat{z}_{\text{geo}}^y - z^y \|_2^2 + \alpha \mathcal{L}_{\text{sgd}} + \beta \mathcal{L}_{\text{sgc}}}_{\mathcal{L}_{\text{depth}}} + \gamma \mathcal{L}_{\text{recon}}$$

其中 $\mathcal{L}_{\text{recon}}$ 为图像重建辅助损失，用于保持 T2I 骨干的细节建模能力。超参数设置为 $\alpha=1.0$、$\beta=0.1$、$\gamma=1.0$（经消融验证为最优配置）。

### 关键设计动机

框架设计的两个关键观察来自初步实验（Figure 1 与 Figure 2）：
- DAv2 等前馈方法提供准确的全局布局和尺度，但细节平滑；扩散方法（如 Lotus-D）保留精细细节和锐利边界，但跨域泛化不足。两者在频率域呈现互补特性。
- 出乎意料的是，在高时间步仅接受低频先验对齐的阶段一，其直接输出反而包含丰富的高频边界和纹理信息，而经合成数据细化的阶段二输出则边界更平滑、几何更稳定。这一发现直接催生了 SGC 的设计——将阶段一作为阶段二的“高频教师”。

![[assets/figures/papers/paper_list_l2525_https_arxiv_org_abs_2603_16340/figures/003_Figure_3.jpg]]
*Figure 3: Iris overview. Iris introduces a two-stage diffusion-based Priors-to-Geometry Deterministic framework that effectively injects real-world priors into the diffusion model. First prior stage injects real-world priors from a frozen teacher under a high-timestep state, while the second geometry stage refines metrically faithful predictions on synthetic supervision at a low-timestep state. In the prior stage, Spectral-Gated Distillation (§3.2) uses a lightweight low-pass gate to filter noisy teacher predictions into stable low-frequency layout priors, whereas in the geometry stage, Spectral-Gated Consistency (§3.3) applies a lightweight high-pass gate to transfer sharp boundaries and fine detail...*

### 问题形式化与扩散背景

Iris 将单目深度估计建模为条件潜变量预测问题。给定输入图像 $\pmb{x}$ 及其在 VAE 潜空间中的编码 $\pmb{z}^x$，目标是预测深度潜变量 $\pmb{z}^y$。方法基于预训练的 Stable Diffusion 骨干，其前向扩散过程定义为：

$$\pmb{x}_t = \sqrt{\bar{\alpha}_t} \pmb{x}_0 + \sqrt{1 - \bar{\alpha}_t} \pmb{\epsilon}$$

其中 $\bar{\alpha}_t$ 控制噪声调度，$t$ 越大信噪比（SNR）越低。Iris 的核心洞察在于：**不同扩散时间步的信息特性与深度估计中频率-可靠性不匹配之间存在结构性对应**——高时间步（低 SNR）适合注入全局布局先验，低时间步（高 SNR）适合细化高频几何细节。

### 两阶段先验到几何确定性框架（PGD）

Iris 的核心框架由两个共享权重的确定性预测阶段构成，在推理时仅需单步前向传播。

**阶段一：先验阶段（Prior Stage）** 在高时间步 $t_{\text{high}} = 1000$ 下运行，此时扩散状态对应低 SNR 区域。模型从噪声潜变量出发，预测初始深度潜变量：

$$\hat{z}_{\text{prior}}^{y} = f_{\theta}(z^{x}, t_{\text{high}}) \tag{4}$$

这一阶段的目标是利用真实图像伪标签注入可靠的**低频先验**——包括场景布局、尺度关系和整体结构。由于高时间步下模型对高频细节的敏感度较低，自然形成对低频信息的偏好。

**阶段二：几何阶段（Geometry Stage）** 以阶段一的输出 $\hat{z}_{\text{prior}}^{y}$ 作为输入，在低时间步 $t_{\text{low}} = 500$ 下运行：

$$\hat{z}_{\text{geo}}^{y} = f_{\theta}(\hat{z}_{\text{prior}}^{y}, t_{\text{low}}) \tag{5}$$

低时间步对应高 SNR 区域，模型在此状态下利用合成数据的精确真值监督，对深度潜变量进行**高频几何细化**，恢复锐利边界和精细纹理。

两阶段解耦的关键在于：真实伪标签的低频分量可信而高频分量不可靠，合成真值则高频精确。单阶段同时监督会导致频率冲突，而 PGD 通过时间步分离实现了**先验注入与几何细化的解耦**。

### 频谱门控蒸馏（Spectral-Gated Distillation, SGD）

在阶段一中，Iris 使用冻结的 Depth Anything V2 教师模型生成真实图像的伪标签 $z_{\text{teach}}^{y}$。为避免教师伪标签中的高频伪影污染模型，SGD 引入可学习的傅里叶低通门：

$$\mathcal{G}_{\phi}^{\text{low}}(z) = z + s(\mathcal{F}^{-1}(M_{\phi} \odot \mathcal{F}(z)) - z) \tag{6}$$

其中 $\mathcal{F}$ 和 $\mathcal{F}^{-1}$ 分别表示傅里叶变换与逆变换，$M_{\phi}$ 为可学习的频域掩码，$s$ 为缩放因子。该门控机制**参数化地控制截止频率与过渡斜率**，选择性保留低频分量。

SGD 损失仅对齐师生在低频带的输出：

$$\mathcal{L}_{\text{sgd}} = \mathbb{E}_{x \sim \mathcal{D}_{\text{real}}} \left\| \mathcal{G}_{\phi}^{\text{low}}(\hat{z}_{\text{prior}}^{y}(x)) - \mathcal{G}_{\phi}^{\text{low}}(z_{\text{teach}}^{y}(x)) \right\|_2^2 \tag{7}$$

这确保了阶段一仅从真实数据中蒸馏可靠的布局与尺度先验，而高频分量保持自由，留待阶段二处理。

### 频谱门控一致性（Spectral-Gated Consistency, SGC）

实验发现，阶段一在高时间步下意外地产生了清晰的边界和丰富的高频纹理（见 Figure 2）。为将这些**内部高频线索**从阶段一传递到阶段二，SGC 引入可学习的高通门 $\mathcal{G}_{\psi}^{\text{high}}$，强制两阶段在高频带保持一致：

![[assets/figures/papers/paper_list_l2525_https_arxiv_org_abs_2603_16340/figures/002_Figure_2.jpg]]
*Figure 2: Comparison of direct stage-1 and stage-2 outputs. (a) Input. (b) Unexpectedly, stage-1 operating at a high timestep with low-pass prior alignment produces crisp boundaries and richer textures. (d) The low-timestep stage-2 refined with synthetic ground truth yields smoother boundaries and more stable geometry. (c) Cumulative spectrum shows that stage-1 carries stronger highfrequency energy. These observations motivate using stage-1 as a high-frequency teacher via Spectral-Gated Consistency (§3.3)*

$$\mathcal{L}_{\text{sgc}} = \mathbb{E}_{x \sim \mathcal{D}_{\text{real}}} \left\| \mathcal{G}_{\psi}^{\text{high}}(\hat{z}_{\text{geo}}^{y}(x)) - \text{sg}\left[ \mathcal{G}_{\psi}^{\text{high}}(\hat{z}_{\text{prior}}^{y}(x)) \right] \right\|_2^2 \tag{9}$$

其中 $\text{sg}[\cdot]$ 为停止梯度算子，防止梯度回传至阶段一，确保阶段一作为固定的高频教师。此外，SGC 引入**过激活约束**以稳定训练，防止高通门过度放大噪声。

### 综合训练损失

深度估计的总损失结合合成数据监督、低频先验蒸馏和高频一致性传递：

$$\mathcal{L}_{\text{depth}} = \mathbb{E}_{x \sim \mathcal{D}_{\text{syn}}} \left\| \hat{z}_{\text{geo}}^{y} - z^{y} \right\|_2^2 + \alpha \mathcal{L}_{\text{sgd}} + \beta \mathcal{L}_{\text{sgc}} \tag{10}$$

为进一步保留 T2I 骨干的细节建模能力，加入图像重建辅助损失 $\mathcal{L}_{\text{recon}}$，仅在阶段二对合成和真实图像进行潜变量重建：

$$\mathcal{L} = \mathcal{L}_{\text{depth}} + \gamma \mathcal{L}_{\text{recon}} \tag{12}$$

消融实验确定最佳超参数为 $\alpha = 1.0$、$\beta = 0.1$、$\gamma = 1.0$（Table 4）。

### 关键设计总结

| 模块 | 作用阶段 | 频域操作 | 核心功能 |
|------|---------|---------|---------|
| PGD 两阶段 | 阶段一 $t=1000$ / 阶段二 $t=500$ | — | 解耦先验注入与几何细化 |
| SGD | 阶段一 | 可学习低通门 | 选择性蒸馏真实低频先验，抑制高频伪影 |
| SGC | 阶段二 | 可学习高通门 + 停止梯度 | 继承阶段一的高频细节，稳定训练 |

![[assets/figures/papers/paper_list_l2525_https_arxiv_org_abs_2603_16340/figures/001_Figure_1.jpg]]
*Figure 1: Comparison of DAv2 and diffusion-based method. (a) Input. (b) DAv2 [46] yields accurate global layout and scale but smoother details. (d) The diffusion-based method (i.e., Lotus [14]) preserves fine details and sharper boundaries. This complementarity motivates our Priors-to-Geometry Deterministic (§3.1) framework; spectral disparity further motivates Spectral-Gated Distillation (§3.2), which transfers reliable low-frequency real-image priors while deferring high-frequency details*

![[assets/figures/papers/paper_list_l2525_https_arxiv_org_abs_2603_16340/figures/005_Figure_4.jpg]]
*Figure 4: Visualization of Spectral-Gated Distillation. SGD aligns teacher and student in the low-frequency band, injecting real-world priors for layout and scale, suppressing high-frequency artifacts, and leaving high-frequency components unconstrained for next-stage refinement. See §3.2 for more details*

![[assets/figures/papers/paper_list_l2525_https_arxiv_org_abs_2603_16340/figures/004_Figure_5.jpg]]
*Figure 5: Visualization of Spectral-Gated Consistency. Stage-1 naturally yields crisp detail and boundary cues. To leverage these internal cues, SGC encourages agreement between stages in the high-frequency band. See §3.3 for more details*

## 实验与关键发现

### 零样本仿射不变深度估计主结果

Iris在零样本仿射不变深度估计任务上与16种方法进行了全面比较，涵盖传统判别式方法和基于扩散的方法。Table 1展示了在KITTI、NYUv2、ETH3D、ScanNet、DIODE等五个基准数据集上的定量结果。

从综合排名来看，Iris在All Avg Ranking和Group Avg Ranking两项指标上均位列第一，整体性能最优。具体而言：

- **KITTI**: Iris取得AbsRel 7.2、δ1 94.5，与**Depth Anything V2**（Yang et al., NeurIPS 2024）的7.4/94.6基本持平。
- **NYUv2**: Iris的AbsRel 4.9、δ1 97.4，略低于DAv2的4.5/97.9，但显著优于其他扩散方法。
- **ETH3D**: Iris取得AbsRel 5.5、δ1 97.6，较**Lotus-D**的6.1/97.0有明显提升（AbsRel降低0.6）。
- **ScanNet**: Iris的AbsRel 5.0、δ1 97.1，同样优于Lotus-D的5.5/96.5。
- **DIODE**: Iris的AbsRel 24.3、δ1 74.3，在该困难场景上略逊于Lotus-D的22.8/73.8。
- **DA-2K**（补充材料Table S1）: Iris的Acc达94.5%，虽低于DAv2的97.1%，但显著优于所有其他扩散方法。

**关键结论**: Iris在训练数据规模远小于DAv2（59K合成+100K真实 vs 62.6M）的条件下，取得了具有竞争力的平均性能，验证了PGD框架在数据效率上的显著优势。相较于先前的扩散方法（**Marigold**、**GenPercept**等），Iris在所有数据集上均实现了一致且可观的性能增益，充分证明了真实世界先验注入的有效性。

### 推理效率分析

Table 2展示了各方法在NVIDIA A100 GPU上以1536²分辨率进行推理的时间对比。Iris的推理时间为1.3秒，显著快于DAv2的2.1秒，且远快于需要多步迭代的随机扩散方法（如Marigold需要数十秒）。这得益于Iris的确定性两阶段设计——仅需两次前向传播即可完成从先验注入到几何细化的全过程。

### 消融实验

Table 3系统消融了Iris各核心组件的贡献：

1. **确定性单步基线**（Deterministic alone）：仅使用单步确定性网络，无真实数据先验，性能最低。
2. **单阶段+SGD**（Deterministic + SGD）：在单阶段中同时监督合成真值和真实伪标签的低频对齐，性能有所提升，但受限于频率-可靠性不匹配，提升有限。
3. **两阶段PGD**（Deterministic + two-stage）：将先验注入与几何细化解耦到不同时间步，性能显著跃升，验证了阶段解耦的必要性。
4. **两阶段+SGD**：在阶段1引入频谱门控蒸馏选择性对齐低频先验，进一步改善全局布局与尺度精度。
5. **两阶段+SGD+SGC（完整Iris）**：加入频谱门控一致性后，阶段2继承阶段1的高频细节，边界清晰度和纹理保真度进一步提升，达到最优性能。

Table 4进一步消融了超参数α（SGD权重）、β（SGC权重）、γ（重建损失权重）的影响，最佳设置为α=1.0、β=0.1、γ=1.0。去除SGC中的过激活约束（条目h）会导致精度下降，验证了稳定训练机制的必要性。

Figure 7通过可视化对比了单阶段+SGD与两阶段PGD的定性差异：单阶段方法仅能部分吸收真实先验，而两阶段方法在全局布局和局部细节上均有明显改善。

### 定性分析

Figure 6展示了Iris在多种场景下的定性比较结果。Iris在室内外场景中均展现出稳定的跨域泛化能力和精确的细节建模——在保持清晰物体边界和丰富纹理的同时，避免了扩散方法常见的伪影问题。与DAv2相比，Iris在细节保真度上具有优势；与Lotus-D相比，Iris在全局布局和尺度准确性上更优。

### 失败模式与局限性

尽管Iris在多数基准上表现优异，仍存在以下局限：

1. **室内场景提升有限**: Iris在NYUv2上的提升较小（AbsRel 4.9 vs DAv2 4.5），主要原因是用于蒸馏的SA-1B子集以室外场景为主，缺乏足够的室内真实图像来校正室内布局先验。这揭示了方法对真实数据分布覆盖度的敏感性。
2. **DIODE性能波动**: 在DIODE数据集上Iris略逊于Lotus-D，可能与该数据集中存在大量极端光照和复杂几何场景有关，高频一致性传递在这些情况下可能引入不稳定性。
3. **安全关键应用风险**: 深度估计在安全关键应用中仍可能出现罕见但较大的误差，且数据分布偏差可能影响特定场景的决策可靠性。

![[assets/figures/papers/paper_list_l2525_https_arxiv_org_abs_2603_16340/figures/010_Table_4.jpg]]
*Table 4: Ablation studies of hyperparameters. α, β, and γ control the relative strengths of SGD, SGC, and the reconstruction loss, respectively. See §4.4 for details*

## 定位与知识库关联

### 1. 基线谱系与定位

Iris 处于单目深度估计（MDE）中“扩散先验+确定性推理”这一新兴交叉点。其核心基线可归为两条主线：

**（1）前馈判别式方法。** 以 **Depth Anything V2**（Yang et al., NeurIPS 2024）为代表，该类方法依赖超大规模真实图像语料（DAv2 训练数据达 62.6M 张）进行训练，在全局布局和尺度估计上表现优异，但输出深度图细节趋于平滑。Iris 的训练数据规模仅为 59K 合成图像 + 100K 真实图像（伪标签由 DAv2 教师生成），在数据效率上具有显著优势，同时在零样本仿射不变深度估计的多数据集综合排名上超越或持平 DAv2（Table 1）。

**（2）扩散式生成方法。** 可进一步分为两类：
- **多步随机扩散方法**，如 **Marigold**（Ke et al., CVPR 2024），利用 Stable Diffusion 的生成先验进行多次去噪迭代，细节保留较好但推理耗时长、域泛化受限于合成到真实的迁移鸿沟。
- **确定性扩散方法**，如 **Lotus-D** 和 **GenPercept**（Xu et al., ICLR 2025），将扩散模型改造为单步确定性预测器，在保持细节能力的同时大幅提升推理效率。Iris 在此基础上进一步引入**两阶段先验到几何确定性（PGD）框架**，解耦先验注入与几何细化，在 KITTI、ETH3D、ScanNet 等数据集上相较 Lotus-D 取得一致且显著的性能提升（AbsRel 分别降低 0.2、0.6、0.5 个百分点，Table 1）。

Iris 的方法定位可概括为：**以确定性扩散为骨架，通过频谱门控蒸馏（SGD）和频谱门控一致性（SGC）实现真实世界先验与合成几何监督的频率解耦融合**，在数据效率、域泛化能力和细节保真度三个维度上同时取得突破。

### 2. 适用边界

**有效场景。** Iris 在室外场景（KITTI、ETH3D）和跨域泛化任务上表现尤为突出，这得益于 SGD 机制从 SA-1B 真实图像子集中提取的低频布局先验。推理效率方面，在 NVIDIA A100 GPU 上以 1536² 分辨率运行时仅需 1.3 秒，显著快于 DAv2（Table 2），且远优于多步迭代扩散方法。

**弱效场景。** Iris 在室内数据集（如 NYUv2）上的提升幅度较小——AbsRel 为 4.9，略逊于 DAv2 的 4.5（Table 1）。分析指出，这是因为用于蒸馏的 SA-1B 子集以室外场景为主，缺乏足够的室内真实图像来校正室内布局先验。在 DIODE 数据集上，Iris 的 AbsRel（24.3）也略高于 Lotus-D（22.8），表明在某些室内外混合场景下仍有改进空间。

**数据依赖边界。** Iris 的性能依赖于 DAv2 教师模型提供的伪标签质量。若教师模型在特定域上存在系统性偏差，该偏差可能通过 SGD 的低频对齐传递至学生模型。此外，两阶段训练要求同时具备合成真值（用于几何监督）和真实图像伪标签（用于先验蒸馏），在缺乏其中任一数据源的场景下框架需做适配。

### 3. 局限与开放问题

**已知局限。**
1. **室内场景先验不足。** 如适用边界所述，真实图像蒸馏集以室外场景为主，导致室内布局先验校正不充分，NYUv2 上的提升有限。这是数据分布偏差的直接后果，而非方法本身的架构缺陷。
2. **安全关键场景的可靠性。** 论文明确指出，深度估计在安全关键应用中仍可能出现罕见但较大的误差，且数据分布偏差可能影响特定场景的决策。Iris 目前未针对此类极端情况做专门的鲁棒性设计。

**开放问题。**
1. **室内数据高效融入。** 如何在不显著增加训练成本的前提下，高效融入更多室内真实数据以提升室内场景的泛化能力，是直接且紧迫的工程问题。
2. **框架的任务泛化性。** 两阶段 PGD 框架是否可推广到其他密集预测任务（如法线估计、语义分割），并保持同等的性能增益？频谱门控机制对非深度模态的频率特性是否同样有效，尚待验证。
3. **降低教师依赖。** 当前框架依赖 DAv2 作为冻结教师提供伪标签。是否可以通过更轻量级的教师模型或自蒸馏策略进一步降低对大规模预训练教师的依赖，是提升方法实用性的重要方向。

## 原文 PDF

![[paperPDFs/CVPR_2026/Iris_Bringing_Real_World_Priors_into_Diffusion_Model_for_Monocular_Depth_Estimation.pdf]]
