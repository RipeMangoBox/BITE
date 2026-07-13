---
title: "GeoRK2: Geometry-Guided Runge-Kutta Integration for Diffusion Transformer Acceleration"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/GeoRK2_Geometry_Guided_Runge_Kutta_Integration_for_Diffusion_Transformer_Acceleration.pdf
project_link: null
code_link: "https://github.com/vipshop/cache-dit"
aliases:
- GeoRK2
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 利用中间层激活的协方差矩阵构建低秩黎曼度量，并基于该度量执行黎曼梯度流积分，使去噪轨迹保持在特征流形上。
primary_logic: 将扩散去噪重新定义为黎曼流形上的梯度流，通过低秩特征协方差诱导的度量引导二阶Runge-Kutta积分，可以在大步长下稳定特征演化并保持结构保真度。
claims:
- 对DiT-XL/2和FLUX.1-dev的激活进行主成分分析，前64个方向解释了超过99%的方差，证明特征动态集中在低维流形上。
- 去噪轨迹偏离欧几里得直线预测的相对位移高达12%，表明平坦空间求解器与学习到的本征几何不匹配。
- 在ImageNet-256 DiT-XL/2上，GeoRK2（N=8）实现FID 3.32和4.92×加速，相较于DDIM-50（FID 2.51），质量损失极小（∆FID ≈ 0.81），且SSIM从0.74提升至0.88。
- 消融实验中移除几何校正导致FID相对上升30.7%，移除RK2预测器导致上升24.2%，证实了流形感知集成的关键作用。
---

# GeoRK2: Geometry-Guided Runge-Kutta Integration for Diffusion Transformer Acceleration

> [!tip] 核心洞察
> 将扩散去噪重新定义为黎曼流形上的梯度流，通过低秩特征协方差诱导的度量引导二阶Runge-Kutta积分，可以在大步长下稳定特征演化并保持结构保真度。

| 字段 | 内容 |
|------|------|
| 中文题名 | GeoRK2：几何引导的龙格-库塔积分用于扩散变压器加速 |
| 英文题名 | GeoRK2: Geometry-Guided Runge-Kutta Integration for Diffusion Transformer Acceleration |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Sun_GeoRK2_Geometry-Guided_Runge-Kutta_Integration_for_Diffusion_Transformer_Acceleration_CVPR_2026_paper.html) · [Code](https://github.com/vipshop/cache-dit) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | GeoRK2 |
| Dataset | ImageNet-256 DiT-XL/2, FLUX.1-dev, HunyuanVideo |

> [!tip] 效果简介
> - ImageNet-256 DiT-XL/2 上，FID 2.41 (N=2) vs 2.51 (DDIM-50) (-0.10)；FID 3.32 (N=8) vs 2.51 (DDIM-50) (+0.81)；SSIM 0.96 (N=2) vs 0.74 (DDIM-50) (+0.22)。
> - FLUX.1-dev (DrawBench) 上，ImageReward 0.989 (N=5) vs 50-step reference (加速度3.52×)。
> - HunyuanVideo (VBench) 上，VBench Score 80.73 (N=8) vs 50-step baseline (加速4.66×)。

## 概要

扩散变压器（DiT）在高分辨率视觉生成中取得了显著成功，但其迭代去噪过程计算成本高昂。现有加速方法——无论是基于高效数值积分器（如 **DDIM**, Song et al., ICLR 2021; **DPM-Solver++**, Lu et al., arXiv 2022）还是基于特征缓存复用（如 **FORA**, Selvaraju et al., 2024; **TaylorSeer**, Liu et al., ICCV 2025; **ToCa**, Zou et al., 2025）——都隐含地在欧几里得空间中执行数值积分。这一设计忽略了一个关键事实：中间层激活实际上分布在弯曲的低维黎曼流形上。在大步长加速场景下，欧氏空间求解器会偏离这一本征几何结构，导致**流形漂移**（manifold drift）：特征轨迹脱离预训练模型所学习到的几何约束，累积误差并显著降低生成保真度。

GeoRK2 的核心洞察在于将扩散去噪重新定义为**黎曼流形上的梯度流**，并通过一个几何引导的二阶 Runge-Kutta 积分框架来保持特征演化始终贴合流形。具体而言，该方法利用中间层激活的协方差矩阵构建低秩黎曼度量，该度量编码了特征空间各向异性的几何信息；在此基础上，一个流形感知的 RK2 预测器在主子空间内进行中点外推，抑制偏离流形的分量，而一个低秩度量预条件校正器则利用 Woodbury 恒等式高效地对预测误差进行曲率补偿。自适应稳定模块通过方差触发回退和动量混合机制抑制大步长下的振荡。

GeoRK2 是一种即插即用、无需微调的加速框架。在 ImageNet-256 DiT-XL/2 上，GeoRK2 以 2 步采样（N=2）实现 FID 2.41 和 1.95× 加速，质量上甚至略优于 50 步 DDIM 的 FID 2.51；以 8 步采样（N=8）在 4.92× 加速下保持 FID 3.32，结构相似度 SSIM 从 0.74 提升至 0.88。在 FLUX.1-dev 和 HunyuanVideo 等更大规模模型上，该方法同样在 3.5–4.7× 加速下保持了与参考方法相当的视觉质量。消融实验进一步证实，移除几何校正组件会导致 FID 相对上升 30.7%，证实了流形感知集成对性能的关键贡献。

扩散模型已成为生成式建模的主流范式，而基于Transformer架构的扩散变压器（Diffusion Transformer, DiT）在大规模图像与视频生成中展现出卓越的保真度和多样性。然而，DiT的推理过程通常需要50至数百次模型前向传播，其高昂的计算成本严重制约了实际部署。现有加速方法主要分为两类：一类是面向采样轨迹的数值积分器（如**DDIM**（Song et al., ICLR 2021）和**DPM-Solver++**（Lu et al., 2022）），通过增大去噪步长减少函数评估次数；另一类是缓存复用方法（如**FORA**、**TaylorSeer**（Liu et al., ICCV 2025）、**∆-DiT**、**ToCa**、**SmoothCache**、**TeaCache**（Liu et al., CVPR 2025）），利用相邻时间步之间的特征相似性跳过冗余计算。

然而，上述方法均在一个关键假设下运作：去噪轨迹在欧几里得空间中演化，因此数值积分或缓存复用可以在平坦的向量空间中进行。本文通过实证分析揭示了这一假设的根本性缺陷。

### 特征流形与流形漂移

对DiT-XL/2和FLUX.1-dev中间层激活的主成分分析表明，前64个主方向解释了超过99%的方差（Figure 3），这意味着去噪过程中的特征动态高度集中在嵌入高维空间的一个低维流形上。进一步测量发现，实际去噪轨迹偏离欧几里得直线预测的相对位移高达12%，表明预训练模型学习到的本征几何是弯曲的黎曼流形，而非平坦的欧几里得空间。

当步长增大时，传统欧氏空间求解器忽略这一曲率结构，导致预测的特征向量脱离流形支撑集——即产生**流形漂移（manifold drift）**。漂移累积的误差在后续时间步中被放大，最终表现为生成图像的结构失真和伪影（Figure 1a）。在极端加速体制下，几何无感知的预测器迅速发散，而几何感知方法则保持稳定（Figure 1b）。

### 现有方法的缺口

现有加速范式在几何建模层面存在结构性空白：

- **数值积分器**（DDIM、DPM-Solver++）在欧氏空间中执行一步或多步更新，未考虑特征空间的各向异性曲率，大步长下预测精度急剧退化。
- **缓存复用方法**（FORA、TaylorSeer、∆-DiT等）通过特征相似性跳过Transformer块的计算，但其缓存替换策略同样基于欧氏距离度量，无法感知流形的弯曲结构，在高加速比下出现不同程度的图像质量退化（Figure 2）。
- **无训练约束**：上述方法均未引入对特征流形的显式建模，也未利用预训练模型激活中蕴含的几何信息来引导去噪轨迹。

这一缺口指向一个核心瓶颈：**如何在无需重新训练的前提下，将扩散去噪重新定义为黎曼流形上的梯度流，并设计相应的数值积分策略，使大步长更新始终保持在特征流形上。**

### 本文动机

针对上述问题，本文提出GeoRK2——一个训练无关的几何感知加速框架。核心动机源于以下观察：中间层激活的协方差矩阵天然编码了特征流形的局部度量结构，可以作为黎曼度量的经验估计。基于这一度量，可以将去噪目标的梯度流约束在流形上，并通过二阶Runge-Kutta积分实现大步长下的稳定外推。

GeoRK2的设计目标是在不修改预训练模型权重、不增加微调成本的前提下，将几何结构显式引入采样过程，从而在4–5倍加速比下将感知质量损失控制在极小范围内（∆FID ≈ 0.81），同时保持生成图像的结构保真度（SSIM从0.74提升至0.88）。

## 核心方法与创新机理

GeoRK2 的核心创新在于将扩散去噪过程从平坦的欧几里得空间重新定义到弯曲的黎曼流形上，并据此设计了一套几何感知的数值积分框架。该框架通过三个紧密耦合的“变更槽”（changed slots）实现了大步长下的稳定加速，从根本上解决了现有方法中普遍存在的**流形漂移**问题。

### 从欧氏积分到黎曼梯度流

现有加速采样器（如 **DDIM**（Song et al., ICLR 2021）和 **DPM-Solver++**（Lu et al., arXiv 2022））本质上在欧氏空间中执行一阶或高阶数值积分。它们隐式地假设特征轨迹在平坦空间中演化，忽略了扩散变压器中间层激活所固有的弯曲几何结构。GeoRK2 的核心洞察在于：去噪轨迹并非任意路径，而是被约束在由模型预训练知识塑造的低维特征流形上。实验证据表明，对 DiT-XL/2 和 FLUX.1-dev 的激活进行主成分分析，前 64 个主方向解释了超过 99% 的方差（Figure 3），这直接证实了特征动态高度集中于一个低维流形。当欧氏空间求解器以大步长外推时，预测轨迹会偏离该流形，产生高达 12% 的相对位移偏差（Section 3），导致误差累积和生成保真度下降。

GeoRK2 将这一问题重新定义为黎曼流形上的梯度流：
$$\dot{h}_{t} = -\Pi_{T_{h_{t}} \mathcal{M}} \big[ G_{\mathrm{eff}}(h_{t})^{-1} \nabla U(h_{t}) \big]$$
其中，度量张量 $G_{t}^{(\ell)}$ 由各层激活的协方差矩阵实时构建：
$$G_{t}^{(\ell)} = \frac{1}{B} H_{t}^{(\ell)} \big( H_{t}^{(\ell)} \big)^{\top} + \varepsilon I_{d\ell}, \quad \varepsilon = 10^{-6}$$
这一“特征协方差诱导度量”将特征空间的各向异性转化为对潜在空间更新步长的几何约束，是 GeoRK2 所有后续机制的基础。

### 三个关键变更槽

基于上述几何框架，GeoRK2 相对于传统采样器在三个关键维度上进行了系统性创新：

**1. 积分方法：从一步更新到流形感知 RK2 预测器**

传统 DDIM 或 DPM-Solver 在每一步仅使用当前点的梯度进行欧氏更新。GeoRK2 将其替换为一个二阶 Runge-Kutta 预测器，但关键区别在于，中点外推和全步预测均被限制在由当前度量定义的**主子空间**内：
$$h_{\mathrm{mid}} = U_{r,t} U_{r,t}^{\top} \big( h_{t} + \frac{\Delta t}{2} v_{t} \big)$$
$$h_{\mathrm{pred}} = U_{r,t} U_{r,t}^{\top} \big( h_{t} + \Delta t v_{\mathrm{mid}} \big)$$
其中 $U_{r,t}$ 是协方差矩阵前 $r$ 个主特征向量构成的基。这种子空间投影起到“几何滤波器”的作用，直接抑制了正交于流形的漂移分量，以 $O(d\ell r^2)$ 的低成本实现了二阶精度（Section 4.1）。消融实验证实，用一阶欧拉替代该 RK2 预测器会导致 FID 相对上升 24.2%（Table 4）。

**2. 校正步骤：从无校正到低秩度量预条件校正**

传统方法缺乏对预测误差的几何感知校正。GeoRK2 引入了一个基于度量逆矩阵的校正项，利用 Woodbury 恒等式高效求解：
$$\Delta h_{\mathrm{geo}} = -\lambda \bar{G}_{r,t}^{-1} \big( h_{\mathrm{pred}} - F(h_{\mathrm{pred}}) \big)$$
该校正项根据局部曲率对预测残差进行补偿，将偏离流形的特征“拉回”到正确的几何位置。移除该几何校正模块会使 FID 相对上升 30.7%（Table 4），是三个组件中影响最大的，凸显了曲率补偿对保真度的关键作用。

**3. 稳定性机制：从无保护到方差触发回退与动量混合**

大步长积分在噪声水平剧烈变化的区域（尤其是 timestep 200–400 附近）容易产生振荡。GeoRK2 引入了一个自适应的稳定性模块：当加速度方差超过阈值 $\alpha=1.5$ 时，触发保守回退，回落到更稳定的更新路径。同时，通过动量混合抑制振荡：
$$h_{\mathrm{out}} = \rho \big( h_{\mathrm{pred}} + \Delta h_{\mathrm{geo}} \big) + (1-\rho) h_{t}, \quad \rho = 0.85$$
该机制在 6–10% 的高速步中触发，仅增加不到 1% 的开销，但防止了约 0.3% 随机种子下的发散（Section 4.1）。完全移除所有几何组件（回退到纯欧氏基线）会使 FID 相对上升 47.6%（Table 4），证明了这一整套几何感知集成策略的整体有效性。

### 与现有加速范式的本质区别

GeoRK2 的创新并非孤立的算法改进，而是代表了一种范式转换：从“在欧氏空间中寻找更快的积分公式”转向“在正确的几何空间中进行积分”。与基于缓存的方法（如 **FORA**、**TeaCache**（Liu et al., CVPR 2025）、**∆-DiT**）或基于泰勒展开的多步预测方法（如 **TaylorSeer**（Liu et al., ICCV 2025））不同，GeoRK2 不依赖于跳过计算或近似模型输出，而是通过理解并利用特征空间的本征几何结构，使得即使在极低步数下，每一步的更新都保持在预训练模型所定义的“有效区域”内。这种训练无关、即插即用的特性，加上跨 DiT-XL/2、FLUX.1-dev 和 HunyuanVideo 三个不同规模模型的统一超参数设置（$r=64, \lambda=0.1, \rho=0.85$），进一步证明了该方法的普适性和鲁棒性。

GeoRK2 是一种无需训练的即插即用加速框架，其核心思想是将扩散去噪过程重新定义为黎曼流形上的梯度流，并在 Transformer 推理管线中嵌入几何感知的二阶数值积分。整体架构由三个协同模块构成：**流形感知 RK2 预测器**、**低秩度量预条件校正器**和**自适应稳定模块**，它们共同替代现有采样器（如 DDIM、DPM-Solver）中的欧氏一步更新，在保持生成保真度的前提下实现大步长稳定推理。

### Pipeline 总览

GeoRK2 的推理流程如 Algorithm 1 和 Figure 4 所示，可概括为以下阶段：

![[assets/figures/papers/paper_list_l2509_https_openaccess_thecvf_com_content_CVPR2026_html_Sun_GeoRK2_Geometry_Gu/figures/004_Figure_4.jpg]]
*Figure 4: GeoRK2 performs geometry-aware diffusion sampling by embedding Riemannian integration into the Transformer inference pipeline. (Left) The prediction stage extrapolates latent dynamics over large intervals using cached activations, while the correction stage refines trajectories on the locally constructed geometric manifold. (Right) Within each Transformer block, GeoRK2 introduces a lightweight Predict–Correct module that replaces the default numerical update of existing samplers (e.g., DDIM, DPM-Solver) with a curvature-aware second-order integration, achieving stable and accelerated generation without retraining*

1. **度量构建与子空间估计**：从中间层激活的协方差矩阵构造局部黎曼度量 $G_t^{(\ell)}$（Eq. 1），并通过截断 SVD 提取前 $r=64$ 个主方向，形成低秩子空间 $U_{r,t}$。该度量每 5 步更新一次，以平衡计算开销与几何精度。
2. **预测阶段（Predictor）**：在主子空间内执行投影中点外推。首先将当前隐藏状态 $h_t$ 与半步速度组合投影至低秩流形，得到几何滤波后的中点 $h_{\mathrm{mid}}$（Eq. 4）；随后基于中点速度进行全步预测，再次投影得到 $h_{\mathrm{pred}}$（Eq. 5）。该投影操作作为一阶收缩映射，抑制偏离流形的正交分量，防止漂移进入度量病态的低置信区域。
3. **校正阶段（Corrector）**：利用低秩度量近似逆矩阵对预测误差进行曲率补偿。通过 Woodbury 恒等式高效计算 $\bar{G}_{r,t}^{-1}$，将预测 $h_{\mathrm{pred}}$ 与去噪网络输出 $F(h_{\mathrm{pred}})$ 的残差映射为几何校正量 $\Delta h_{\mathrm{geo}}$（Eq. 6）。
4. **动量混合与稳定输出**：将校正后的预测与上一步隐藏状态进行动量混合，阻尼系数 $\rho=0.85$ 抑制大步长下的振荡（Eq. 7）。同时，方差触发回退机制监控加速度统计量：当滑动窗口内的方差超过阈值 $\alpha=1.5$ 时，自动回退至保守的 DDIM 更新，确保极端步长下的数值稳定性。

### 模块关系与数据流

三个模块以流水线方式串联，数据流如下：

```
h_t → [度量更新(每5步)] → [RK2预测器: 子空间投影中点外推] → h_pred
                                                                    ↓
h_out ← [动量混合 ρ=0.85] ← [低秩度量校正器: 曲率补偿] ← Δh_geo
                                                                    ↑
                          [方差监控 → 触发回退时替换为DDIM更新]
```

- **度量更新**为预测器和校正器提供共享的几何先验（主子空间 $U_{r,t}$ 和低难度量近似逆 $\bar{G}_{r,t}^{-1}$），是连接两个模块的纽带。
- **预测器**利用子空间投影实现几何滤波，输出初步预测 $h_{\mathrm{pred}}$；**校正器**在此基础上利用度量信息进行曲率补偿，二者形成“预测-校正”的二阶积分范式。
- **自适应稳定模块**作为外层保护机制，监控整个推理过程的动力学稳定性，在必要时介入并覆盖预测-校正输出。

### 关键设计选择

- **低秩近似**：截断秩 $r=64$ 在 DiT-XL/2 和 FLUX.1-dev 上均捕获了超过 99% 的激活方差（Figure 3），使得度量构建和求逆的计算复杂度从 $O(d_\ell^3)$ 降至 $O(d_\ell r^2)$，额外 FLOPs 仅约 5.1%。
- **前 4 步 DDIM 预热**：在推理初期使用标准 DDIM 更新，待激活统计稳定后再启用几何积分，避免冷启动阶段的度量估计偏差。
- **统一超参数**：$\lambda=0.1$（校正步长）、$\rho=0.85$（动量阻尼）、$\beta=0.9$（方差衰减）、$\alpha=1.5$（回退阈值）在所有模型和数据集上均未进行单独调优，体现了方法的鲁棒性。

GeoRK2 将扩散去噪重新定义为黎曼流形上的梯度流，并通过三个紧密耦合的模块——**流形感知 RK2 预测器**、**低秩度量预条件校正器**和**自适应稳定模块**——在 Transformer 推理管线中嵌入几何感知的二阶数值积分。以下分述各模块的核心公式与变量含义。

### 局部协方差度量

GeoRK2 的几何基础建立在由中间层激活构造的黎曼度量之上。对于第 $\ell$ 层的激活矩阵 $H_t^{(\ell)} \in \mathbb{R}^{B \times d_\ell}$（$B$ 为批量大小，$d_\ell$ 为特征维度），定义局部协方差度量：

$$G_{t}^{(\ell)} = \frac{1}{B} H_{t}^{(\ell)} \big( H_{t}^{(\ell)} \big)^{\top} + \varepsilon I_{d_\ell}, \quad \varepsilon = 10^{-6}$$

其中 $\varepsilon I_{d_\ell}$ 为正则化项，确保度量矩阵正定。该度量将特征空间各向异性转化为潜在空间中的步长调整依据——沿主方向（高方差）允许大步长，沿次方向（低方差）则收缩步长，从而将去噪轨迹约束在预训练模型所隐含的低维流形上。

### 黎曼梯度流

在构造的黎曼流形 $\mathcal{M}$ 上，去噪过程被建模为能量函数 $U(h_t)$ 的梯度流：

$$\dot{h}_{t} = -\Pi_{T_{h_{t}} \mathcal{M}} \big[ G_{\mathrm{eff}}(h_{t})^{-1} \nabla U(h_{t}) \big]$$

其中 $G_{\mathrm{eff}}$ 为有效度量（由各层度量聚合得到），$\Pi_{T_{h_t}\mathcal{M}}$ 表示到切空间 $T_{h_t}\mathcal{M}$ 的投影算子。该方程的核心意义在于：梯度 $\nabla U(h_t)$ 先经度量逆矩阵 $G_{\mathrm{eff}}^{-1}$ 进行曲率补偿（将欧氏梯度“拉回”到流形上），再通过切空间投影确保更新方向始终与流形相切，从根本上抑制流形漂移。

### 流形感知 RK2 预测器

预测器在 Transformer 块内部执行两步子空间投影外推，实现二阶精度。

**投影中点**（Algorithm 1, Eq. 4）：将当前隐藏状态 $h_t$ 沿速度方向 $v_t$ 外推半步，然后通过正交投影限制在由前 $r$ 个主成分张成的子空间内：

$$h_{\mathrm{mid}} = U_{r,t} U_{r,t}^{\top} \big( h_{t} + \frac{\Delta t}{2} v_{t} \big)$$

其中 $U_{r,t} \in \mathbb{R}^{d_\ell \times r}$ 为 $G_t^{(\ell)}$ 的前 $r$ 个特征向量构成的矩阵。该投影作为几何滤波器：与流形正交的分量被抑制，防止特征漂移到度量定义不良的低置信度区域。

**全步预测**（Algorithm 1, Eq. 5）：利用中点速度 $v_{\mathrm{mid}}$ 进行全步外推，同样经子空间投影：

$$h_{\mathrm{pred}} = U_{r,t} U_{r,t}^{\top} \big( h_{t} + \Delta t \, v_{\mathrm{mid}} \big)$$

该方法以 $O(d_\ell r^2)$ 的计算代价实现二阶精度，将正交投影视为一阶回缩（retraction），避免了显式黎曼指数映射的高昂开销。

### 低秩度量预条件校正器

预测步骤后，校正器利用低难度量逆矩阵对预测误差进行曲率补偿（Algorithm 1, Eq. 6）：

$$\Delta h_{\mathrm{geo}} = -\lambda \, \bar{G}_{r,t}^{-1} \big( h_{\mathrm{pred}} - F(h_{\mathrm{pred}}) \big)$$

其中 $F(\cdot)$ 为 Transformer 块的前向函数，$h_{\mathrm{pred}} - F(h_{\mathrm{pred}})$ 度量预测值与模型实际输出之间的残差；$\bar{G}_{r,t}^{-1}$ 为低秩近似度量的逆矩阵，通过 Woodbury 恒等式高效计算，避免了对完整 $d_\ell \times d_\ell$ 矩阵求逆。$\lambda$ 为校正步长（默认 0.1），控制曲率补偿的强度。

### 动量混合与自适应稳定

**动量混合输出**（Algorithm 1, Eq. 7）：将校正后的预测与上一步隐藏状态进行阻尼混合，抑制大步长下的振荡：

$$h_{\mathrm{out}} = \rho \big( h_{\mathrm{pred}} + \Delta h_{\mathrm{geo}} \big) + (1-\rho) h_{t}, \quad \rho = 0.85$$

阻尼系数 $\rho = 0.85$ 在推进速度与稳定性之间取得平衡：$\rho$ 越大，更新越激进但振荡风险增加；$\rho$ 越小，轨迹越平滑但收敛变慢。

**方差触发回退**（Algorithm 1, lines 9–18）：监控加速度序列的滑动方差。当方差超过阈值 $\alpha = 1.5$ 时，触发保守回退——放弃当前几何校正，改用小步长欧拉更新，并将度量更新周期临时缩短。该机制在 6–10% 的高速步中触发，主要集中于噪声水平剧烈转换的 timestep 200–400 区间，以不到 1% 的额外开销防止约 0.3% 随机种子下的发散。

## 实验与关键发现

### 主要结果

GeoRK2 在图像、文本到图像和视频生成三个模态上均实现了显著的加速与质量保持。在 ImageNet-256 的 DiT-XL/2 上，仅需 2 步推理（N=2）即达到 FID 2.41 和 SSIM 0.96，相较 DDIM-50 的 FID 2.51 和 SSIM 0.74，在 1.95× 加速的同时实现了感知质量和结构保真度的双重提升（Table 1）。当步数放宽至 8 步（N=8），加速比达到 4.92×，FID 仅略微上升至 3.32，SSIM 保持在 0.88，验证了该方法在大步长下的稳定性。

![[assets/figures/papers/paper_list_l2509_https_openaccess_thecvf_com_content_CVPR2026_html_Sun_GeoRK2_Geometry_Gu/figures/005_Table_1.jpg]]
*Table 1: Quantitative comparison on ImageNet-256 with DiT-XL/2. Results are means over 5 runs. Speed↑ is relative to DDIM-50*

在文本到图像生成任务中，GeoRK2 在 FLUX.1-dev 上的表现同样突出。N=5 时，ImageReward 达到 0.989 ± 0.021，CLIP Score 为 34.96 ± 0.18，加速比 3.52×（Table 2）。值得注意的是，该配置下的感知质量与 50 步参考结果几乎无法区分，说明几何引导的积分策略有效抑制了文本-图像对齐能力的退化。

![[assets/figures/papers/paper_list_l2509_https_openaccess_thecvf_com_content_CVPR2026_html_Sun_GeoRK2_Geometry_Gu/figures/006_Table_2.jpg]]
*Table 2: Comparison on FLUX.1-dev. Results are means over 5 runs. Speed↑ relative to 50-step reference*

视频生成场景进一步验证了方法的泛化性。在 HunyuanVideo 上，GeoRK2（N=8）以 4.66× 加速获得 VBench Score 80.73（Table 3），证明低秩黎曼度量构建策略可以无缝迁移至更大规模、更高维度的 Transformer 架构，无需针对模型单独调参。

![[assets/figures/papers/paper_list_l2509_https_openaccess_thecvf_com_content_CVPR2026_html_Sun_GeoRK2_Geometry_Gu/figures/007_Table_3.jpg]]
*Table 3: Comparison on VBench with HunyuanVideo. Results are means over 5 runs. Speed↑ relative to 50-step baseline*

### 消融实验

消融实验（Table 4，N=3，DiT-XL/2）系统拆解了 GeoRK2 各组件的贡献。完整 GeoRK2 的 FID 为 2.31，SSIM 为 0.94。移除几何校正模块（w/o GC）导致 FID 相对上升 30.7%，这是所有消融中退化最严重的配置，直接证实了基于低秩协方差度量的曲率补偿是抑制流形漂移的核心机制。将 RK2 预测器替换为一阶欧拉更新（w/o RK2）使 FID 相对上升 24.2%，表明二阶中点外推对于在大步长下保持轨迹精度至关重要。纯欧氏基线（无任何几何组件）的 FID 相对退化高达 47.6%，从反面印证了将扩散去噪重新定义为黎曼梯度流的必要性。

![[assets/figures/papers/paper_list_l2509_https_openaccess_thecvf_com_content_CVPR2026_html_Sun_GeoRK2_Geometry_Gu/figures/009_Table_4.jpg]]
*Table 4: Controlled ablation on DiT-XL/2 (N=3). %FID degradation shows relative increase vs full GeoRK2*

### 超参数敏感性

截断秩 $r$ 是控制低秩近似质量与计算开销之间权衡的关键参数。实验表明，$r$ 从 32 增至 64 时，FID 从 2.89 改善至 2.31；继续增大至 128 时 FID 为 2.28，收益明显递减。这一饱和行为与主成分分析中前 64 个方向解释超过 99% 方差的发现（Figure 3）高度一致，说明 $r=64$ 已充分捕获特征流形的主导几何结构。

阻尼系数 $\rho$ 在 $[0.6, 0.9]$ 范围内均能保持动力学稳定，校正步长 $\lambda$ 在 $[0.05, 0.15]$ 区间内性能不敏感，表明方法对超参数选择具有较好的鲁棒性。稳定性阈值 $\alpha=1.5$ 时，回退机制在 6–10% 的高速步中触发，主要集中于噪声水平转换区（timestep 200–400 附近），额外开销低于 1%，但有效防止了约 0.3% 随机种子下的发散。

### 失败模式与局限性

尽管 GeoRK2 在多数场景下表现稳定，但在剧烈的噪声水平切换阶段，回退机制仍需在 6–10% 的步中触发，表明完全消除不稳定性仍面临挑战。此外，该方法引入约 5.1% 的额外 FLOPs 和 3.8% 的墙上时间开销，在极端资源受限场景下存在进一步优化空间。当前设计针对 Transformer 架构（DiT）验证，对其他扩散模型（如 U-Net）的适用性尚未评估，在极高分辨率或超大模型上的度量构建策略也可能需要调整。

![[assets/figures/papers/paper_list_l2509_https_openaccess_thecvf_com_content_CVPR2026_html_Sun_GeoRK2_Geometry_Gu/figures/002_Figure_2.jpg]]
*Figure 2: Visualization of images generated by different methods for multiple prompts. At high acceleration ratios, methods such as FORA and TaylorSeer exhibit varying degrees of image quality degradation, while GeoRK2 maintains superior performance*

## 定位与知识库关联

### 与现有加速方法的关系

GeoRK2 的贡献在于将扩散变压器（DiT）的去噪过程从欧几里得数值积分迁移到黎曼流形上的几何积分，从而解决了现有方法在大步长下普遍存在的**流形漂移**问题。其与相关工作的关系可从以下几个维度梳理。

**传统采样器与高阶求解器。** **DDIM**（Song et al., ICLR 2021）和 **DPM-Solver++**（Lu et al., arXiv 2022）在欧氏空间中执行数值积分，忽略了中间层激活所张成的弯曲几何结构。GeoRK2 的实验表明，在 DiT-XL/2 上，去噪轨迹偏离欧氏直线预测的相对位移高达 12%，这直接证实了平坦空间求解器与学习到的本征几何之间的失配。GeoRK2 的核心创新在于用**流形感知的 RK2 预测器**替换了这些求解器的默认数值更新，通过子空间投影中点外推（Eq. 4）和低秩度量预条件校正（Eq. 6），使积分轨迹保持在特征流形上。

**缓存驱动的加速方法。** 近年来，基于特征缓存的加速策略在 DiT 推理中取得了显著进展。**FORA**（Selvaraju et al., 2024）、**∆-DiT**（Chen et al., 2024）、**ToCa**（Zou et al., 2025）和 **TaylorSeer**（Liu et al., ICCV 2025）等方法通过重用跨时间步的中间激活来减少计算量，但它们在预测阶段仍采用欧氏空间的外推或插值，忽略了特征流形的曲率。GeoRK2 与这些方法是**正交且可叠加的**——其流形感知积分模块可嵌入到任何缓存加速框架中，为缓存预测提供几何一致的校正。事实上，GeoRK2 的代码实现基于 **DBCache**（vipshop, GitHub 2025）混合缓存引擎，展示了该方法作为即插即用组件的灵活性。**SmoothCache**（Liu et al., 2025）和 **TeaCache**（Liu et al., CVPR 2025）等通用缓存方案同样可从 GeoRK2 的几何校正中受益，尽管原文未对此进行直接验证。

**训练无关的加速范式。** GeoRK2 属于训练无关（training-free）方法，无需微调预训练模型。这与 ∆-DiT 和 ToCa 等方法的理念一致，但 GeoRK2 通过引入基于激活协方差的低秩黎曼度量（Eq. 1），提供了一种**数据驱动的几何先验**，而非仅仅依赖启发式缓存策略。消融实验（Table 4）表明，纯欧氏基线（无任何几何组件）使 FID 相对完整 GeoRK2 上升 47.6%，而移除几何校正（w/o GC）使 FID 上升 30.7%，这强有力地证明了流形感知设计的关键作用。

### 适用边界与局限

尽管 GeoRK2 在多个基准上展示了显著的加速效果和保真度提升，其适用边界和局限性同样值得关注。

**架构适用范围。** 当前设计针对 Transformer 架构（DiT-XL/2、FLUX.1-dev、HunyuanVideo）进行了验证，其核心操作——基于中间层激活协方差构建低秩度量——依赖于 Transformer 块输出的特征表示。对于其他扩散模型架构（如基于 U-Net 的 SD 系列），特征的组织方式和几何结构可能不同，GeoRK2 的适用性尚未评估。这是一个需要手动验证的开放问题。

**计算开销。** GeoRK2 引入了约 5.1% 的额外 FLOPs 和 3.8% 的墙上时间开销。这主要来自协方差矩阵的周期性计算和截断 SVD（每 5 步更新一次）。对于极高分辨率或超大模型（如更高维度的特征空间），这些操作可能带来更大的内存和时间开销，尽管低秩近似（r=64）和 Woodbury 恒等式的使用已显著缓解了这一问题。未来工作中提到的基于超网络的度量学习（hypernetwork-based metrics）正是为了进一步降低在线计算开销。

**稳定性边界。** 自适应稳定模块中的回退机制在 6–10% 的高速步中触发，主要发生在噪声水平转换区（timestep 200–400 附近）。虽然这仅增加了不到 1% 的开销，并防止了 0.3% 随机种子中的发散，但表明在剧烈的噪声切换阶段完全消除不稳定性仍有挑战。阻尼系数 ρ 在 [0.6, 0.9] 范围内保持动力学稳定，校正步长 λ 在 [0.05, 0.15] 内性能不敏感，说明超参数具有良好的鲁棒性。

**度量构建策略的泛化性。** 截断秩 r 从 32 增至 64 时，FID 从 2.89 改善至 2.31；继续增大至 128 时 FID 为 2.28，收益递减。这表明当前基于协方差低秩近似的度量策略在 r=64 附近已达到饱和。在更大规模模型（如 FLUX Pro、Sora 类视频模型）上，特征流形的本征维度可能更高，是否需要调整度量构建策略（如自适应秩选择或分层度量）尚未验证。

### 开放问题与未来方向

GeoRK2 将扩散去噪重新定义为黎曼流形上的梯度流，这一视角为加速采样开辟了新的研究方向。

**跨范式扩展。** 该方法能否扩展到其他迭代推理过程（如能量基模型、流匹配等），尚待探索。黎曼梯度流的框架在理论上具有通用性，但需要针对具体模型的特征几何进行适配。

**度量学习的进化。** 当前度量完全基于激活协方差的低秩近似，是一种无参数的几何先验。未来工作包括基于超网络的度量学习，以数据驱动的方式学习更精确的流形结构，同时降低在线计算开销。这有望进一步提升大步长下的积分精度。

**与缓存策略的深度耦合。** 当前 GeoRK2 与缓存加速是松耦合的（即插即用）。探索几何校正如何指导缓存策略（例如，在流形曲率大的区域减少缓存复用，在平坦区域增加复用）可能带来更高效的混合加速方案。

**理论收敛性分析。** 原文提供了充分的经验证据，但缺乏对黎曼 RK2 积分在扩散采样中收敛性的理论分析。建立大步长下的误差界和收敛保证，将有助于指导超参数选择并拓展到更广泛的应用场景。

## 原文 PDF

![[paperPDFs/CVPR_2026/GeoRK2_Geometry_Guided_Runge_Kutta_Integration_for_Diffusion_Transformer_Acceleration.pdf]]
