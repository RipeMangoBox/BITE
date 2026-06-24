---
title: "PhysGen: Physically Grounded 3D Shape Generation for Industrial Design"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/PhysGen_Physically_Grounded_3D_Shape_Generation_for_Industrial_Design.pdf
project_link: null
code_link: "https://github.com/kasvii/PhysGen"
aliases:
- PhysGen
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 在流匹配（flow matching）生成过程中交替进行速度更新与物理精炼，并利用阻力系数的梯度进行物理正则化，将物理约束融入潜在空间更新，确保生成过程不脱离形状流形。
primary_logic: 将形状与物理（压力和阻力）联合编码到统一潜在空间（SP‑VAE），通过流匹配保持形状先验的同时，利用物理梯度进行交替迭代优化，可以在不牺牲几何合理性的前提下提升物理性能。
claims:
- 统一生成框架相比后优化方法大幅提升形状准确度，F‑score 从 74.03 提高到 89.65。
- 给定目标阻力系数可显著提高形状生成精度，F‑score 提升 21.09%，倒角距离降低 22.68%。
- 物理引导能缓解单视图深度歧义，生成形状的前视宽度更一致，倒角距离从 20.98 降至 2.38。
- 交替更新策略既能恢复几何合理性又能改善物理性能，避免单一物理优化造成的几何畸变。
---

# PhysGen: Physically Grounded 3D Shape Generation for Industrial Design

> [!tip] 核心洞察
> 将形状与物理（压力和阻力）联合编码到统一潜在空间（SP‑VAE），通过流匹配保持形状先验的同时，利用物理梯度进行交替迭代优化，可以在不牺牲几何合理性的前提下提升物理性能。

| 字段 | 内容 |
|------|------|
| 中文题名 | PhysGen：面向工业设计的物理约束三维形状生成 |
| 英文题名 | PhysGen: Physically Grounded 3D Shape Generation for Industrial Design |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.00422) · [Code](https://github.com/kasvii/PhysGen) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | PhysGen |
| Dataset | DrivAerNet++, ShapeNet / DrivAerNet++ |

> [!tip] 效果简介
> - DrivAerNet++ (无条件生成) 上，F-score (0.01) ×100 ↑ 89.65 vs 74.03 (w/o phys.) (+21.09%)。
> - DrivAerNet++ (形状重建) 上，Overall Accuracy (O-Acc.) ↑ 96.73 vs 95.31 (Dora fine-tuned) (+1.42)。
> - DrivAerNet++ (阻力系数估计) 上，MSE ×10^{-5} ↓ 4.0 vs 9.1 (TripNet) (-5.1)。

## 概述

3D 生成模型在视觉质量上取得了显著进展，但现有方法普遍缺乏物理知识，导致生成的形状在物理上不可行——例如车轮与车身相交、座椅结构不稳定、气动外形产生宽大湍流尾迹——无法满足工业设计的实际需求。这一瓶颈的根源在于生成过程完全依赖几何或图像先验，而忽略了形状在真实物理环境中的功能约束。

PhysGen 提出了一个统一的物理感知 3D 形状生成框架，其核心思想是将形状与物理属性（表面压力和阻力系数）联合编码到统一潜在空间，并在流匹配（flow matching）生成过程中交替进行速度更新与物理精炼，从而将物理约束融入生成轨迹而不脱离形状流形。该方法的关键因果机制在于：阻力系数的梯度作为物理正则化项，在每一步去噪后软性地引导潜在码向物理可行区域移动；随后通过方向感知的物理精炼进一步优化压力分布与力平衡。

实验表明，这一统一生成策略相比传统的后优化方法显著提升了形状精度：在 DrivAerNet++ 数据集上，F‑score 从 74.03 提高到 89.65（+21.09%），倒角距离降低 22.68%。给定目标阻力系数进行物理引导时，生成形状与真实几何的对齐度大幅改善。在单视图真实图像场景中，物理引导有效缓解了深度歧义，倒角距离从 20.98 降至 2.38（降低 88.7%）。此外，交替迭代策略在保持几何合理性的同时改善了压力分布均匀性，避免了单一物理优化造成的几何畸变。

在方法谱系上，PhysGen 以 Dora 的形状 VAE 和流匹配生成管线为基础，将占用场表征替换为有符号距离函数（SDF）以捕获更精细的几何细节，并引入 SP‑VAE 实现形状与物理的联合编码。与 TripOptimizer 等后优化基线相比，PhysGen 将物理引导内嵌于生成过程，避免了后优化易产生不可逆畸变的缺陷。在知识库定位上，该方法属于物理信息驱动的生成模型范畴，其交替迭代策略为将 PDE 约束融入扩散/流匹配生成提供了可泛化的范式。

**主要结果速览**：

- **无条件生成**：F‑score 89.65（vs. 无物理引导 74.03），提升 21.09%（Table 2）
- **形状重建**：Overall Accuracy 96.73，优于 Dora fine‑tuned 的 95.31（Table 4）
- **阻力系数估计**：MSE 4.0×10⁻⁵，优于 TripNet 的 9.1×10⁻⁵（Table 5）
- **单视图真实图像**：物理引导使 CD 降低 88.7%（Table 3, Figure 5）
- **阻力最小化**：平均阻力系数在 DrivAerNet++ 无条件生成中降低 15.5%（Table A）

**局限与开放问题**：当前验证集中在汽车气动设计，训练依赖昂贵的 CFD 仿真数据，交替迭代策略导致推理时间较长（单次约 210 秒）。未来方向包括推广至热传导、电磁场等非气动物理场，处理多目标物理优化的权衡，以及在缺乏高保真仿真数据时利用物理先验实现弱监督生成。

## 背景与动机

三维形状生成技术近年来取得了显著进展，但在工业设计这一高要求领域，现有方法暴露出一个根本性缺陷：**缺乏物理知识**。主流生成模型能够产出视觉上合理的几何形状，却无法保证其在物理世界中的可行性——生成的车轮可能与车身相交，座椅腿可能断裂或不稳定，气动外形可能产生宽大的湍流尾迹，导致极低的气动效率（Figure 1）。这种“形似而神不似”的生成结果，使得模型难以直接服务于对功能性和安全性有严格要求的工业设计流程。

造成这一瓶颈的深层原因在于，现有三维生成范式将形状建模为纯粹的几何问题。无论是基于占用场（Occupancy Field）的隐式表征，还是以图像为条件的流匹配（flow matching）生成，其优化目标都局限于几何保真度，完全忽略了形状在物理环境中承受的力、产生的压力场以及由此决定的功能性能。当生成结果需要满足气动阻力、结构稳定性等物理约束时，这些方法天然地力不从心。

一种朴素的补救思路是“先生成、后优化”：先用生成模型产出形状，再通过物理仿真进行后优化调整。然而，这种两阶段策略存在不可逆的几何畸变风险——物理优化可能将形状推离数据流形，产生扭曲的表面，且无法通过后续的生成步骤恢复（Figure 3）。这揭示了物理约束与形状先验之间的深层张力：**单独施加物理优化会破坏几何合理性，而纯粹的生成模型又无视物理可行性**。

PhysGen 的动机正是弥合这一裂隙。其核心洞察在于：**将形状与物理信息联合编码到统一潜在空间，并在生成过程中交替进行流匹配更新与物理精炼，可以在不牺牲几何合理性的前提下显著提升物理性能**。这一思路将物理知识从外挂约束升级为生成过程的内在引导，为工业级三维形状生成开辟了新的技术路径。

## 核心创新

PhysGen 的核心创新在于将**物理感知**系统性地嵌入 3D 形状生成的完整流程，而非将其作为后处理步骤。这通过三个紧密耦合的“changed slots”实现：统一的形状-物理表征空间、物理正则化的生成动力学、以及交替迭代的生成范式。

### 从形状表征到形状-物理联合表征

现有 3D 生成模型（如 **Dora**、**3DShape2VecSet**）仅编码几何信息，缺乏对物理属性的显式建模。PhysGen 提出 **SP‑VAE（Shape-and-Physics Variational Autoencoder）**，将形状与物理（表面压力场、全局阻力系数）联合编码到统一潜在空间。这一设计的关键机制是：共享的潜在码 $z$ 同时驱动三个解码器——形状解码器（预测 SDF 场）、压力解码器（预测表面压力 $p = \mathcal{D}_p(\mathbf{x}, \mathbf{z})$）和阻力解码器（预测全局 $C_d$）。联合微调策略（Table 7）使几何重建与物理估计形成相互增强：O-Acc. 从独立训练的 95.31 提升至 96.73，阻力估计 MSE 也同步改善。

与基线采用占用场（Occupancy Field）不同，PhysGen 改用**有符号距离函数（SDF）**表征形状，以捕获更精细的几何细节。这一选择为后续物理精炼中通过 Marching Cubes 提取高质量网格奠定了基础。

### 从无条件生成到物理正则化的流匹配

传统流匹配模型的去噪过程仅由数据分布驱动：
$$ \mathbf{z}_{t_{n+1}}' = \mathbf{z}_{t_n} - (t_{n+1} - t_n) \hat{\mathbf{u}}(\mathbf{z}_{t_n}, t_n, \mathbf{c}) $$

PhysGen 在每一步速度更新后注入**物理正则化项**，利用阻力解码器作为物理感知估计器，沿目标阻力偏差的梯度调整潜在码：
$$ \mathbf{z}_{t_{n+1}} = \mathbf{z}_{t_{n+1}}' - \lambda_d \nabla_{\mathbf{z}_{t_n}} \big\| \mathcal{D}_d(\mathbf{z}_{t_n}) - d_{\mathrm{tar}} \big\|_2^2 $$

这一机制“软引导”生成轨迹偏向物理可行的流形区域，而非硬性约束。其因果效应在 Table 2 中量化：给定目标阻力系数使 F-score 提升 21.09%（从 74.03 到 89.65），倒角距离降低 22.68%。

### 从一步生成到交替迭代的物理-几何协同优化

这是 PhysGen 最关键的流程创新。传统方法要么仅做无条件生成（忽略物理），要么采用两阶段“生成-后优化”（如 **TripOptimizer**），但后优化容易使形状脱离数据流形，产生不可逆的几何畸变（Figure 3）。

PhysGen 提出**交替进行速度更新与物理精炼**的迭代范式：每轮先执行 25 步流匹配速度更新（保持形状先验），再执行 20 步物理精炼（利用方向力梯度优化潜在码）。物理精炼阶段基于表面压力计算方向力：
$$ F_s = \sum_{i=1}^{V} p_i \mathbf{n}_{s,i} A_i, \quad s \in \{x, y, z\} $$
并通过分方向损失函数（最小化阻力 $\mathcal{L}_x$、对称化侧向力 $\mathcal{L}_y$、约束负升力 $\mathcal{L}_z$）反向传播梯度。

Figure 6 的消融实验揭示了这一交替策略的因果瓶颈：纯物理优化改善气动性能但引入网格畸变；纯流匹配恢复几何却导致压力分布不均；唯有交替执行两者，才能在保持几何合理性的同时获得均匀的压力分布。Table 1 的量化对比证实，统一生成框架的 F-score（89.65）显著优于后优化方法（74.03），且后者即使使用更强的优化设置（500 步、学习率 $10^{-3}$）仍无法恢复形状品质。

### 物理引导缓解单视图歧义

一个意料之外的创新收益是物理信息对深度歧义的缓解。从单张真实图像生成 3D 形状时，不同随机噪声会产生前视宽度不一致的形状（Figure 5 中红色与橙色车辆）。引入物理引导后，不同初始化生成的形状（蓝色与绿色）收敛到一致的前视宽度，倒角距离从 20.98 降至 2.38（Table 3）。这表明阻力系数约束充当了隐式的跨视角正则化器，迫使生成形状在不可见维度上满足物理一致性。

## 整体框架

PhysGen 的整体框架围绕一个核心矛盾展开：**如何在保持形状流形合理性的前提下，将物理约束注入生成过程**。现有方案通常将生成与物理优化割裂为两阶段（先生成、后优化），这种串行范式极易在物理精炼阶段破坏几何结构且无法恢复（见 Table 1 和 Figure 3）。PhysGen 的解决方案是将物理知识内化到生成动力学中，构建一个统一的、交替迭代的物理引导生成管线。

### 核心流水线

Figure 2 给出了系统的全局视图，整体可分为两大功能模块：

![[assets/figures/papers/paper_list_l2566_https_arxiv_org_abs_2512_00422/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the proposed framework. (a) The proposed SP-VAE learns a unified latent representation that jointly encodes geometric structure and physical properties. From this shared representation, three decoders reconstruct the 3D shape, surface pressure field, and drag coefficient, respectively. (b) The physics-guided shape generation iteratively bridges flow-matching updates and physical refinements, optionally conditioned on an image, such as a sketch. This alternating strategy updates the latent code to align with the desired 3D shape and physical properties, ensuring both visual plausibility and physical validity*

**（a）形状-物理联合变分自编码器（SP‑VAE）**  
该模块负责学习一个统一的潜在空间，将三维几何结构与物理属性（表面压力场、阻力系数）联合编码。具体而言，编码器接收点云输入，通过双向交叉注意力融合均匀采样点与显著表面点，输出一个紧凑的潜在向量 $z$。这一潜在向量同时驱动三个解码器：形状解码器预测有符号距离函数（SDF）场并通过 Marching Cubes 重建网格；压力解码器预测逐点表面压力 $p = \mathcal{D}_p(\mathbf{x}, \mathbf{z})$；阻力解码器预测全局阻力系数 $C_d$。三个解码器共享同一潜在表征，使得几何与物理之间的内在相关性在训练中被隐式捕获。

**（b）物理引导的流匹配生成**  
该模块在 SP‑VAE 的潜在空间上执行生成过程，核心创新在于**交替迭代策略**。每一步迭代包含两个子步骤：

1. **速度更新与物理正则化**：采用整流流（rectified flow）框架，在潜在空间中从噪声 $\epsilon$ 向数据 $\mathbf{z}_1$ 线性插值。每个时间步 $t_n$，扩散变换器（DiT）预测速度场 $\hat{\mathbf{u}}(\mathbf{z}_{t_n}, t_n, \mathbf{c})$，执行一步反向更新得到中间潜在码 $\mathbf{z}_{t_{n+1}}'$。随后，利用阻力解码器作为物理感知估计器，沿目标阻力偏差的梯度方向对潜在码施加正则化：

$$\mathbf{z}_{t_{n+1}} = \mathbf{z}_{t_{n+1}}' - \lambda_d \nabla_{\mathbf{z}_{t_n}} \big\| \mathcal{D}_d(\mathbf{z}_{t_n}) - d_{\mathrm{tar}} \big\|_2^2$$

这一软约束将生成轨迹柔和地导向物理可行区域，而不强制脱离形状流形。

2. **物理精炼**：在速度更新之后，对潜在码执行 $M$ 步方向感知的物理梯度下降。利用压力解码器预测的表面压力场，计算阻力（$x$）、侧向力（$y$）和升力（$z$）方向的分力：

$$F_s = \sum_{i=1}^{V} p_i \mathbf{n}_{s,i} A_i, \quad s \in \{x, y, z\}$$

并构建分方向物理损失——最小化阻力 $\|F_x\|_2$、鼓励侧向力对称 $\|F_y\|_2$、约束负升力 $\mathrm{ReLU}(F_z)$ 以增加抓地力。梯度通过压力解码器反向传播至潜在码，直接优化物理性能。

交替执行上述两个子步骤 $K$ 次（默认 $K=20$），每次包含 25 步速度更新和 20 步物理精炼。这种设计使得物理优化始终处于流匹配的“引力场”中——物理精炼改善气动性能，流匹配更新则修复物理优化可能引入的几何畸变，二者相互制衡、协同收敛。Figure 6 的消融可视化清晰展示了这一动态：纯物理优化产生扭曲表面，纯流匹配更新导致压力分布不均匀，而交替策略同时实现了精细几何与均匀压力场。

### 条件注入与输入输出

生成过程支持可选的图像条件（如草图或单视图真实照片），通过 DINO 特征提取后经交叉注意力注入 DiT 的每个 Transformer 块（见 Figure B）。无条件生成则直接从随机噪声出发。最终输出为符合目标物理属性（如指定阻力系数 $d_{\mathrm{tar}}$）的三维网格，以及对应的表面压力分布。

## 核心模块与公式推导

PhysGen 的核心架构由两个紧密耦合的模块构成：**形状-物理联合变分自编码器（SP‑VAE）** 与 **物理引导的交替生成流程**。前者将几何与物理属性压缩到统一潜在空间，后者在此空间中通过流匹配与物理精炼的交替迭代，生成既符合形状先验又满足物理约束的三维模型。

### SP‑VAE：统一形状-物理潜在空间

SP‑VAE 的设计目标是学习一个能够同时表达几何结构与物理属性的统一潜在表示。其编码器通过双向交叉注意力机制融合均匀采样点与显著表面点，输出潜在码 $\mathbf{z}$。从该潜在码出发，三个并行的解码器分别负责不同的预测任务：

- **形状解码器** $\mathcal{D}_s$：对查询点 $\mathbf{x}$ 预测有符号距离函数值 $s = \mathcal{D}_s(\mathbf{x}, \mathbf{z})$，随后通过 Marching Cubes 提取网格。相比占用场，SDF 表示能捕捉更精细的几何细节。
- **压力解码器** $\mathcal{D}_p$：预测表面压力场 $p = \mathcal{D}_p(\mathbf{x}, \mathbf{z})$，为后续物理精炼提供逐点的气动信息。
- **阻力解码器** $\mathcal{D}_d$：预测全局阻力系数 $C_d$，作为生成过程中物理正则化的梯度信号源。

训练采用两阶段策略：首先对各模块独立预训练，再进行联合微调。联合微调的损失函数为：

$$\mathcal{L}_{\mathrm{shape}} = \lambda_{\mathrm{sdf}} \mathcal{L}_{\mathrm{sdf}} + \lambda_{\mathrm{KL}} \mathcal{L}_{\mathrm{KL}}$$

其中 SDF 损失为预测值与真实值之间的均方误差：

$$\mathcal{L}_{\mathrm{sdf}} = \| s - \hat{s} \|_2^2$$

联合微调使几何表示与物理表示相互促进——消融实验表明，该策略将形状重建的整体准确率（O-Acc.）从 95.31 提升至 96.73，同时在阻力估计和压力预测上均获得增益（Table 7）。

### 物理引导的流匹配生成

生成过程在 SP‑VAE 的潜在空间中执行，采用整流流（rectified flow）框架。前向扩散过程定义为从噪声 $\boldsymbol{\epsilon}$ 到数据 $\mathbf{z}_1$ 的线性插值：

$$\mathbf{z}_{t_n} = t_n \mathbf{z}_1 + (1 - t_n) \boldsymbol{\epsilon}$$

对应的常速度场为：

$$\mathbf{u}_{t_n} = \frac{d\mathbf{z}_{t_n}}{dt_n} = \mathbf{z}_1 - \boldsymbol{\epsilon}$$

反向去噪时，利用扩散变换器（DiT）预测的速度场 $\hat{\mathbf{u}}$ 进行一步更新：

$$\mathbf{z}_{t_{n+1}}' = \mathbf{z}_{t_n} - (t_{n+1} - t_n) \hat{\mathbf{u}}(\mathbf{z}_{t_n}, t_n, \mathbf{c})$$

**物理正则化**在此步骤之后介入。利用阻力解码器作为物理感知估计器，沿目标阻力偏差的梯度方向调整潜在码，使生成轨迹偏向物理可行区域：

$$\mathbf{z}_{t_{n+1}} = \mathbf{z}_{t_{n+1}}' - \lambda_d \nabla_{\mathbf{z}_{t_n}} \big\| \mathcal{D}_d(\mathbf{z}_{t_n}) - d_{\mathrm{tar}} \big\|_2^2$$

这一机制的关键优势在于：它不改变流匹配学习到的形状流形，而是通过软约束引导采样过程，避免后优化方法中常见的几何畸变。

### 物理精炼：方向感知的力优化

在交替生成范式中，物理精炼阶段利用压力解码器预测的表面压力场，计算三个方向的分力：

$$F_s = \sum_{i=1}^{V} p_i \mathbf{n}_{s,i} A_i, \quad s \in \{x, y, z\}$$

其中 $p_i$、$\mathbf{n}_{s,i}$、$A_i$ 分别为第 $i$ 个面元的压力、法向分量和面积。基于此定义方向感知的物理损失：

$$\mathcal{L}_x = \|F_x\|_2, \quad \mathcal{L}_y = \|F_y\|_2, \quad \mathcal{L}_z = \mathrm{ReLU}(F_z)$$

- $\mathcal{L}_x$：最小化阻力方向的分力，降低气动阻力。
- $\mathcal{L}_y$：惩罚侧向力，鼓励左右对称。
- $\mathcal{L}_z$：约束负升力（增加下压力），提升行驶稳定性。

总物理损失为加权和：

$$\mathcal{L} = \lambda_x \mathcal{L}_x + \lambda_y \mathcal{L}_y + \lambda_z \mathcal{L}_z$$

物理精炼通过反向传播该损失，对潜在码执行 $M$ 步梯度更新。随后流匹配更新恢复几何合理性，二者交替迭代 $K$ 次。消融实验（Fig. 6）证实：纯物理优化虽改善气动性能但引入表面畸变，纯流匹配更新虽保持形状品质但压力分布不均匀，唯有交替策略能同时获得精细几何与平滑压力分布。

![[assets/figures/papers/paper_list_l2566_https_arxiv_org_abs_2512_00422/figures/015_Figure_6.jpg]]
*Figure 6: Visualization of generation with physical refinement and flow-matching updates, shown in terms of mesh geometry and surface pressure. Starting from a physically imperfect initialization (a), physical refinement improves physical objectives but introduces distortions (b). Adding flow-matching updates restore geometric plausibility but lead to non-uniform pressure (c). Alternating the two produces refined geometry and more uniform pressure, improving both visual quality and aerodynamic performance (d)*

### 补充图表

![[assets/figures/papers/paper_list_l2566_https_arxiv_org_abs_2512_00422/figures/018_Figure.jpg]]
*Figure: A. Overview of the SP-VAE shape encoder-decoder. The encoder fuses uniform and salient surface points via bidirectional cross-attention and self-attention to produce a latent code. The decoder predicts an SDF field from query points using crossattention and reconstructs the mesh via marching cubes*

![[assets/figures/papers/paper_list_l2566_https_arxiv_org_abs_2512_00422/figures/019_Figure.jpg]]
*Figure: B. Diffusion Transformer (DiT) architecture. Noised latent and timestep embeddings form the input token sequence, while optional DINO-based conditioning is injected via cross-attention in each block. Each DiT block applies self-attention, cross-attention, and an MLP to produce the final velocity prediction*

![[assets/figures/papers/paper_list_l2566_https_arxiv_org_abs_2512_00422/figures/004_Figure_3.jpg]]
*Figure 3: Qualitative comparison of post-optimization and our unified generation. SP-VAE + TripOptimizer produces distorted shapes and fails to recover them, whereas our alternating method restores plausible surfaces closer to the ground truth*

## 实验与分析

### 核心实验设置

PhysGen 的实验围绕 **DrivAerNet++** 数据集展开，该数据集包含丰富的汽车几何变体及对应的 CFD 仿真物理场（表面压力、阻力系数）。评估维度覆盖形状精度、物理估计准确性和物理引导生成效果。形状精度采用 **F-score（阈值 0.01）**、**Chamfer Distance (CD)** 和 **Overall Accuracy (O-Acc.)** 等指标；物理估计采用 **MSE**；气动性能通过 **OpenFOAM** 仿真得到的平均阻力系数衡量。

---

### 统一生成 vs. 后优化：交替策略的决定性优势

现有方法通常将物理优化作为后处理步骤，即在生成形状后再进行物理精炼。PhysGen 的核心主张是将物理引导嵌入生成过程本身，形成统一的交替迭代框架。

**Table 1** 给出了统一生成与后优化方法的定量对比。后优化基线采用 **TripOptimizer**，在 SP‑VAE 生成的形状上进行物理精炼。即使使用更强的优化设置（500 步，学习率 $10^{-3}$），后优化方法的 F-score 仅为 74.03，而 PhysGen 的交替策略达到 **89.65**，提升超过 15 个百分点。倒角距离（CD）同样大幅降低（20.99 vs. 32.00）。这表明后优化容易使形状偏离原始流形、产生不可逆畸变，而交替更新在改善物理性能的同时保持了形状的几何合理性。

**Figure 3** 的定性对比直观展示了这一差异：SP‑VAE + TripOptimizer 生成的形状出现明显畸变且无法恢复，而 PhysGen 的交替方法能够恢复接近真实几何的合理表面。

**关键结论**：物理引导必须与生成过程交替进行，而非事后修补。后优化破坏了潜在空间中的形状先验，导致不可逆的质量退化。

---

### 物理信息对生成精度的因果作用

#### 目标阻力系数引导

PhysGen 允许用户指定目标阻力系数 $d_{\text{tar}}$ 来引导生成。**Table 2** 量化了这一引导的效果：

![[assets/figures/papers/paper_list_l2566_https_arxiv_org_abs_2512_00422/figures/006_Table_2.jpg]]
*Table 2: Shape accuracy under target drag coefficient*

- **F-score** 从无物理引导的 74.03 提升至 **89.65**（+21.09%）
- **Chamfer Distance** 从 27.08 降至 **20.99**（−22.68%）

**Figure 4** 从几何层面揭示了因果机制：无物理引导的生成形状（灰色）与真实形状（红色）存在偏差，而向目标阻力系数精炼后（蓝色），形状明显向真实几何收敛。这说明阻力系数作为全局物理特征，对形状的宏观几何具有强约束力，能有效纠正生成过程中的几何偏差。

#### 缓解单视图深度歧义

单视图 3D 生成存在固有的深度歧义问题——同一张图像可以对应不同深度分布的形状。**Table 3** 和 **Figure 5** 展示了物理引导对这一问题的缓解效果。

![[assets/figures/papers/paper_list_l2566_https_arxiv_org_abs_2512_00422/figures/007_Table_3.jpg]]
*Table 3: Comparison of shapes from a real image without (w/o phys.) and with (w/ phys.) physical guidance*

在真实单视图图像条件下，无物理引导时不同随机噪声生成的形状前视宽度差异显著，Chamfer Distance 高达 20.98（×10⁴）；加入物理引导后，CD 骤降至 **2.38**（−88.7%），且不同噪声生成的前视宽度趋于一致。物理信息在此充当了隐式的深度正则化器，约束了视觉歧义空间中的可行解范围。

**关键结论**：物理信息（阻力系数）作为全局形状描述符，能够有效约束生成空间，同时提升形状精度和跨样本一致性。

---

### 形状重建与物理估计性能

PhysGen 的 SP‑VAE 不仅服务于生成，其本身也是一个强大的联合编码器。**Table 4** 对比了形状重建性能。在 DrivAerNet++ 上微调后，PhysGen 在所有指标上均优于主流 VAE 基线：

![[assets/figures/papers/paper_list_l2566_https_arxiv_org_abs_2512_00422/figures/008_Table_4.jpg]]
*Table 4: Comparison on shape reconstruction. “†” indicates finetuning on the DrivAerNet++ [11] dataset. “O-”, “S-”, and “C-” denote overall, sharp, and coarse, respectively*

- **O-Acc.** 达到 **96.73**，超过 **Dora**（95.31）、**3DShape2VecSet**（94.82）、**Hunyuan3D 2.1**（93.47）和 **Hi3DGen**（92.62）
- 在 S-IoU、C-IoU 等细分指标上同样保持领先

在物理估计方面，**Table 5** 显示 PhysGen 的阻力系数估计 MSE 为 **4.0 × 10⁻⁵**，显著优于专用预测模型 **TripNet**（9.1 × 10⁻⁵）。**Table 6** 的压力场预测中，PhysGen 的 MSE 为 **4.55 × 10⁻²**，优于 **FigConvNet**（4.99 × 10⁻²）等专用模型。

![[assets/figures/papers/paper_list_l2566_https_arxiv_org_abs_2512_00422/figures/010_Table_5.jpg]]
*Table 5: Performance comparison on drag coefficient estimation*

![[assets/figures/papers/paper_list_l2566_https_arxiv_org_abs_2512_00422/figures/011_Table_6.jpg]]
*Table 6: Performance comparison on pressure field prediction*

这些结果表明，联合编码形状与物理信息不仅没有造成任务冲突，反而通过多任务学习实现了相互促进。

---

### 消融实验：关键设计选择验证

#### 训练策略：联合微调的必要性

**Table 7** 对比了 SP‑VAE 的两种训练策略：独立训练（各模块分别预训练后固定）与联合微调。联合微调在所有指标上均有提升：

- 形状重建 O-Acc. 从 95.31 提升至 **96.73**
- 阻力估计 MSE 从 6.6 × 10⁻⁵ 降至 **4.0 × 10⁻⁵**
- 压力预测 MSE 从 5.17 × 10⁻² 降至 **4.55 × 10⁻²**

这验证了形状与物理表征之间存在内在相关性，联合优化能够促进两者的相互增强。

#### 交替策略的有效性

**Figure 6** 通过可视化对比了四种策略的效果：
1. **初始形状**（a）：物理上不完美
2. **仅物理精炼**（b）：改善了物理目标，但引入几何畸变
3. **仅流匹配更新**（c）：恢复了几何合理性，但压力分布不均匀
4. **交替更新**（d）：同时获得精炼的几何和更均匀的压力分布

这一定性结果直接支持了论文的核心设计理念：物理精炼和流匹配更新具有互补性，单独使用任一种都会导致质量退化，交替迭代才能同时满足几何和物理约束。

#### 全压力场引导 vs. 仅阻力引导

**Figure 7** 进一步对比了仅用阻力系数引导和利用完整压力场引导的效果差异。全压力场引导能够更精细地抑制局部高压区域，使表面压力分布更加平滑。这表明阻力系数提供了有效的全局约束，而压力场则补充了局部细节的物理合理性。

#### 物理解码器架构

**Table 8** 消融了物理解码器的组件设计。同时使用自注意力、通道分支和 MLP 分支的完整配置达到最低的 MSE 和 MAE，验证了多维度特征融合对物理场预测的有效性。

---

### 阻力最小化：跨数据集的泛化验证

**Table A** 展示了在不同数据集和条件下主动最小化阻力系数的结果。通过 OpenFOAM 仿真验证：

- **DrivAerNet++ 无条件生成**：平均阻力系数从 0.324 降至 **0.274**（−15.5%）
- **DrivAerNet++ 条件生成**：从 0.334 降至 **0.312**（−6.5%）
- **ShapeNet 无条件生成**：从 0.393 降至 **0.304**（−22.7%）

条件生成下的降幅较小，因为图像条件本身已对形状施加了强约束，物理优化的空间受限。ShapeNet 上的显著降幅表明，PhysGen 的物理引导机制具有一定的跨域泛化能力，即使面对分布外几何也能有效优化气动性能。

---

### 失败模式与局限性

尽管 PhysGen 在多个维度上表现优异，但分析揭示了以下局限：

1. **推理效率**：交替迭代策略（K=20 次，每次 25 步速度更新 + 20 步物理精炼）导致单次生成约需 210 秒，远高于单步生成方法，不适合实时应用场景。

2. **物理解码器依赖性**：物理精炼的效果高度依赖压力解码器的预测精度。在分布外几何上，解码器误差可能被迭代放大，导致物理引导失效或产生非预期形变。Figure 6(b) 中仅物理精炼产生的畸变即反映了这一问题。

3. **数据获取成本**：SP‑VAE 的训练需要配对的 CFD 仿真数据（阻力系数、压力场），这些数据的获取成本高昂，限制了向新工业领域的快速扩展。

4. **领域聚焦**：当前验证集中在汽车气动设计，向飞机、船舶等领域的推广需要额外的数据收集和验证实验。

### 补充图表

![[assets/figures/papers/paper_list_l2566_https_arxiv_org_abs_2512_00422/figures/003_Table_1.jpg]]
*Table 1: Unified generation vs. post-optimization*

![[assets/figures/papers/paper_list_l2566_https_arxiv_org_abs_2512_00422/figures/012_Table_7.jpg]]
*Table 7: Ablation study on the training strategy of SP-VAE*

## 方法谱系与知识库定位

### 1. 在生成范式中的位置

PhysGen 属于**物理感知的条件生成模型**，其核心定位是在流匹配（flow matching）框架中嵌入显式物理约束，区别于两类主流方法：

- **纯几何生成模型**：如 **Dora**、**3DShape2VecSet**、**Hunyuan3D 2.1**、**Hi3DGen** 等，仅以视觉或几何保真度为目标，缺乏对物理可行性（如气动效率、结构稳定性）的显式建模。PhysGen 在保留此类模型形状先验的基础上，引入了物理正则化。
- **后优化方法**：如 **TripOptimizer**，在生成完成后施加物理优化。Table 1 的对比表明，后优化即使采用更强的优化设置（500 步, 学习率 $10^{-3}$），F‑score 仅达 74.03，而 PhysGen 的统一交替框架达到 89.65。Figure 3 进一步揭示后优化易产生不可逆的几何畸变，而交替策略能恢复合理表面——这构成了 PhysGen 区别于后优化范式的关键因果证据。

PhysGen 的生成流程可抽象为：**流匹配速度更新 → 阻力梯度正则化 → 方向感知物理精炼** 的 K 次循环。这种“生成-精炼交替”机制在概念上与强化学习中 actor-critic 的交替优化有相似之处，但 PhysGen 的“critic”是预训练的可微物理解码器（压力解码器 $\mathcal{D}_p$、阻力解码器 $\mathcal{D}_d$），而非价值网络。

### 2. 表征学习谱系

PhysGen 的 SP‑VAE 将形状（SDF）与物理场（压力、阻力）联合编码到统一潜在空间。这一设计可追溯至两类工作：

- **3D 形状 VAE**：如 **3DShape2VecSet** 和 **Dora**，使用占用场（occupancy field）作为形状表征。PhysGen 将表征切换为 SDF（证据锚点：“we adopt an SDF representation to capture finer geometric details”），以获得更精细的几何细节，这一选择在 Table 4 中体现为 O‑Acc. 96.73 vs. Dora 的 95.31。
- **物理场预测模型**：如 **TripNet**（阻力估计，MSE $9.1 \times 10^{-5}$）和 **FigConvNet**（压力预测，MSE $4.99 \times 10^{-2}$）。PhysGen 的物理解码器在联合训练后分别达到 $4.0 \times 10^{-5}$ 和 $4.55 \times 10^{-2}$（Table 5、Table 6），表明联合编码产生了形状与物理之间的互信息增益——Table 7 的消融证实了联合微调相比独立训练的一致提升。

### 3. 适用边界

**已验证的有效域**：
- 汽车气动外形生成（DrivAerNet++ 数据集），包括无条件生成、图像条件生成、目标阻力引导生成。
- 单视图真实图像的 3D 重建（物理引导将倒角距离从 $20.98 \times 10^4$ 降至 $2.38 \times 10^4$，Table 3）。
- 阻力最小化任务（OpenFOAM 仿真验证，Table A：DrivAerNet++ 无条件生成平均 $C_d$ 从 0.324 降至 0.274，降幅 15.5%）。
- 初步的结构优化（Figure C 展示外部载荷下的柔度降低）。

**已知局限与未验证边界**：
- **领域泛化**：当前验证集中于汽车气动设计，扩展到飞机、船舶等需要额外的 CFD 数据和实验验证。
- **物理场类型**：仅验证了气动压力场和阻力系数，未涉及热传导、电磁场等其他物理模态。
- **多目标权衡**：物理精炼使用加权总损失 $\mathcal{L} = \lambda_x \mathcal{L}_x + \lambda_y \mathcal{L}_y + \lambda_z \mathcal{L}_z$（Eq. 13），但权重 $\lambda$ 的选取策略及其对多目标帕累托前沿的影响未系统研究。
- **数据依赖**：训练 SP‑VAE 依赖高保真 CFD 仿真数据（阻力系数、表面压力场），限制了数据规模的快速扩展。在缺乏仿真数据的场景下，能否利用 PDE 先验实现弱监督或自监督的物理感知生成，仍为开放问题。

### 4. 计算与推理效率边界

交替迭代策略（K=20 次循环，每次 25 步速度更新 + 20 步物理精炼）使单次生成约需 210 秒，不适合实时应用。物理精炼的效果依赖压力解码器在分布外几何上的预测精度——当生成形状偏离训练分布时，物理梯度可能指向不可靠的方向。

### 5. 开放问题

1. **跨物理模态泛化**：SP‑VAE 的联合编码框架能否直接扩展到热、电磁等多物理场，构建通用物理感知生成模型？
2. **多目标帕累托优化**：如何在阻力最小化与下压力最大化等冲突目标间进行可控权衡？当前加权损失方案缺乏对帕累托前沿的显式探索。
3. **潜在空间偏差**：形状与物理的联合编码是否会在潜在空间中引入隐式偏差，导致某些物理合理但几何罕见的样本难以生成？
4. **弱监督扩展**：在缺乏高保真 CFD 数据时，能否利用物理先验（如 Navier‑Stokes 方程的弱形式）实现自监督或物理信息网络（PINN）风格的训练？

## 原文 PDF

![[paperPDFs/CVPR_2026/PhysGen_Physically_Grounded_3D_Shape_Generation_for_Industrial_Design.pdf]]