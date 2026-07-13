---
title: "When Robots Obey the Patch: Universal Transferable Patch Attacks on Vision-Language-Action Models"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/When_Robots_Obey_the_Patch_Universal_Transferable_Patch_Attacks_on_Vision_Language_Action_Models.pdf
project_link: null
code_link: "https://github.com/yuyi-sd/UPA-RFAS"
aliases:
- URUPARFAS
- WROPUTPAVLAM
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/representation_self_supervised_transfer
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过共享特征空间内的ℓ₁偏差与排斥性对比学习迫使代理模型产生高迁移性位移，结合鲁棒性增强的双层优化与跨模态注意力劫持+语义错位损失，使补丁在多个VLA模型间稳定迁移。
primary_logic: VLA模型视觉特征处于同一低维线性子空间（高CCA、高R²），因此最大化代理侧ℓ₁偏差并沿高CCA方向排斥对比，再叠加注意力劫持与指令语义错位，可学到跨越模型、任务与环境的通用物理补丁。
claims:
- 代理与目标VLA特征空间具有强线性对齐（R²≈0.654，top-k CCA接近1），表明存在共享低维子空间。
- 最大化ℓ₁代理偏差在目标侧必然引起非平凡偏差（命题1及推论1），保证迁移性。
- 鲁棒性增强双层优化（内部PGD扰动+外部补丁更新）显著提升迁移强度（Table 8，ϵ=4/255时平均成功率降至58.00%）。
- 消融实验：移除联合特征损失（w/o J_tr）导致攻击效果断崖式下降（平均成功率从61.50%反弹至85.75%），验证特征空间目标是迁移关键。
---

# When Robots Obey the Patch: Universal Transferable Patch Attacks on Vision-Language-Action Models

> [!tip] 核心洞察
> VLA模型视觉特征处于同一低维线性子空间（高CCA、高R²），因此最大化代理侧ℓ₁偏差并沿高CCA方向排斥对比，再叠加注意力劫持与指令语义错位，可学到跨越模型、任务与环境的通用物理补丁。

| 字段 | 内容 |
|------|------|
| 中文题名 | 当机器人服从补丁：面向视觉-语言-动作模型的通用可迁移补丁攻击 |
| 英文题名 | When Robots Obey the Patch: Universal Transferable Patch Attacks on Vision-Language-Action Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2511.21192) · [Code](https://github.com/yuyi-sd/UPA-RFAS) |
| Topic | #topic/vision_multimodal_applications #topic/representation_self_supervised_transfer #topic/vision_multimodal_applications/image_and_video_generation |
| Method | UPA-RFAS (Universal Patch Attack via Robust Feature, Attention, and Semantics) |
| Dataset | LIBERO |

> [!tip] 效果简介
> - LIBERO 上，Task Success Rate (%) 5.75 (OpenVLA-oft-w, 仿真) vs 76.5 (良性) (-70.75 pp)；Task Success Rate (%) 40.25 (OpenVLA-oft-w, 物理) vs 76.5 (良性) (-36.25 pp)；Task Success Rate (%) 86.0 (π₀, 仿真) vs 92.0 (良性) (-6.0 pp)。
> - LIBERO (白盒) 上，Task Success Rate (%) 0.5 (仿真平均) vs 76.5 (良性) (-76.0 pp)；Task Success Rate (%) 2.75 (物理平均) vs 76.5 (良性) (-73.75 pp)。

## 概要

视觉‑语言‑动作（VLA）模型正在成为机器人操控的核心范式，但其对抗鲁棒性——尤其是面对物理世界可部署的补丁攻击时——仍未被充分审视。现有针对VLA的补丁攻击严重过拟合单一代理模型，在黑盒条件（未知架构、微调变体、sim‑to‑real漂移）下迁移性极差，缺乏一个通用、可迁移的攻击框架来系统性地暴露这一脆弱性。

本文提出 **UPA‑RFAS**（*Universal Patch Attack via Robust Feature, Attention, and Semantics*），首个面向VLA机器人的通用可迁移补丁攻击框架。其核心洞察在于：不同VLA模型的视觉特征处于同一低维线性子空间（代理与目标特征间 R² ≈ 0.654，top‑k 典型相关系数接近1），这意味着在代理模型上最大化特征偏差必然在目标模型上引起非平凡位移。基于这一发现，UPA‑RFAS 通过三条互补路径构建可迁移攻击：

1. **特征空间目标**：以 ℓ₁ 偏差与排斥性 InfoNCE 对比损失迫使代理特征沿高 CCA 方向一致偏移，保证跨模型迁移。
2. **鲁棒性增强双层优化**：内部 PGD 学习样本级不可见扰动以硬化代理特征空间，外部 AdamW 优化单一通用物理补丁，使补丁在扰动邻域内仍保持强攻击力。
3. **跨模态注意力劫持与语义错位**：Patch Attention Dominance（PAD）损失劫持文本→视觉注意力，使动作相关查询聚焦补丁区域；Patch Semantic Misalignment（PSM）损失将补丁语义拉向动作/方向锚点并推离指令嵌入，从高层语义层面破坏任务执行。

在黑盒迁移攻击下，仅使用 5% 画面面积（50×50 像素于 224×224 观测）的单一补丁，UPA‑RFAS 在 LIBERO 仿真基准上将受害者 **OpenVLA‑oft‑w** 的任务成功率从 76.5% 降至 **5.75%**，物理场景降至 **40.25%**，大幅超越 UMA、UADA、TMA 等现有基线。消融实验证实，移除联合特征损失（w/o J_tr）导致攻击断崖式退化（平均成功率反弹至 85.75%），而 RUPA 内部扰动 ϵ = 4/255 时获得最强迁移（58.00%），验证了特征空间目标与鲁棒性增强是迁移性的双重关键。

**方法定位**：UPA‑RFAS 属于对抗攻击中的**通用物理补丁攻击**范畴，区别于传统白盒单模型攻击，它强调**跨模型、跨任务、跨域（sim‑to‑real）的可迁移性**。在方法谱系上，其核心贡献在于首次将特征空间线性对齐理论、鲁棒性增强 min‑max 优化与 VLA 特有的跨模态注意力/语义操控整合为一个统一框架，填补了 VLA 领域通用可迁移攻击的空白。

### 机器人基础模型的安全脆弱性

视觉‑语言‑动作（VLA）模型正迅速成为机器人操作的核心范式。这类模型将视觉观测与自然语言指令融合，通过大规模预训练的视觉编码器和语言模型骨干直接输出连续动作指令，在跨任务泛化、零样本指令跟随等方面展现出显著优势。然而，随着VLA模型从实验室走向真实部署，其安全性问题日益凸显——尤其是对抗性物理补丁攻击的威胁。

物理补丁攻击仅需在场景中放置一个视觉上有限的图案（如打印的贴纸），即可在不接触模型参数的前提下误导机器人策略。这类攻击具有极低的实施门槛和极高的现实危害性：攻击者无需访问模型内部，只需将补丁贴在操作场景中的任意位置，就可能使机器人执行危险动作或完全丧失任务能力。

### 现有攻击的致命瓶颈：迁移性缺失

尽管已有工作探索了针对VLA模型的补丁攻击，但它们存在一个根本性缺陷——**严重过拟合单一代理模型**。现有方法（如UMA、UADA等）在白盒条件下（已知代理模型架构与参数）表现尚可，但一旦切换到黑盒受害者（不同架构、微调变体、甚至sim-to-real环境漂移），攻击效果急剧退化。这一瓶颈源于：

1. **任务/动作损失的模型特异性**：现有攻击直接优化代理模型的任务成功率或动作损失，这些损失函数高度依赖模型内部的决策边界，缺乏跨模型不变性。
2. **缺乏对共享表征结构的利用**：不同VLA模型虽架构各异，但其视觉编码器（多为DINOv2、SigLIP等大规模预训练模型）共享相似的底层特征空间。现有方法未能系统性地利用这一共享子空间来保证迁移性。
3. **训练范式的脆弱性**：单环梯度上升训练出的补丁对代理模型的小幅扰动极为敏感，缺乏对抗局部扰动的鲁棒性，导致其在未知受害者上的泛化能力薄弱。

### 核心洞察与本文动机

本工作的核心洞察在于：**不同VLA模型的视觉特征空间存在高度线性对齐**。实验分析表明，代理模型与受害者模型的视觉嵌入之间存在显著的高正则相关系数（top-k CCA接近1）和线性回归拟合度（R² ≈ 0.654），表明它们处于同一低维线性子空间中。这意味着，若能在代理模型的特征空间中制造足够大的ℓ₁偏差，并沿高CCA方向引导特征位移，该偏差将以高概率传递到受害者模型。

基于此洞察，本文提出**UPA-RFAS**——首个面向VLA机器人的通用、可迁移物理补丁攻击框架。其核心动机是：**通过特征空间内的结构化扰动、鲁棒性增强的双层优化、以及跨模态注意力劫持与语义错位，迫使代理模型产生沿共享子空间方向的特征位移，从而实现跨模型、跨任务、跨环境的稳定迁移**。

## 核心方法与创新机理

### 问题瓶颈：现有VLA补丁攻击为何无法迁移？

现有针对视觉-语言-动作（VLA）模型的补丁攻击方法（如UMA、UADA、TMA等）存在一个根本性缺陷：**严重过拟合单一代理模型**。这些方法直接在代理模型上优化任务级或动作级损失，所生成的补丁高度特化于该模型的决策边界。当面对黑盒条件——未知架构、微调变体、sim-to-real分布漂移——时，补丁的迁移性急剧退化，攻击成功率断崖式下跌。换言之，攻击者只要换一个受害者模型，现有的补丁就几乎失效。

这一瓶颈的本质在于：**缺乏一个通用、可迁移的补丁攻击体系**，使得在单一代理模型上训练的物理补丁能够稳定地跨越模型、任务与环境边界。

### 核心洞察：共享低维子空间与特征级操控

本工作提出了一个关键发现：**不同VLA模型的视觉特征处于同一低维线性子空间内**。实验证据表明，代理模型与目标模型之间的特征空间具有强线性对齐——决定系数R²≈0.654，top-k典型相关系数（CCA）接近1。这意味着，尽管模型架构和训练细节各异，它们的视觉编码器输出之间存在着可被线性映射捕获的共享结构。

基于这一洞察，攻击策略发生了根本性转变：**从优化任务/动作损失转向操控共享特征空间内的表示位移**。如果在代理侧的特征空间中制造一个足够大的、沿高CCA方向集中的偏差，那么根据线性对齐假设（命题1及推论1），该偏差在目标侧必然引起非平凡的位移，从而保证迁移性。

### 方法谱系与知识库定位

下表将UPA-RFAS与现有VLA攻击方法在关键设计维度上进行对比，清晰呈现其创新所在：

| 设计维度 | 现有方法（UMA/UADA/TMA等） | UPA-RFAS（本工作） |
|---------|--------------------------|-------------------|
| **攻击优化目标** | 任务/动作损失（如RoboticAttack） | 特征空间ℓ₁偏差 + 排斥性InfoNCE对比损失 + PAD + PSM |
| **训练范式** | 单环梯度上升（直接优化补丁） | 鲁棒性增强双层优化：内部PGD + 外部AdamW |
| **跨模态注意力操控** | 无专门机制 | Patch Attention Dominance (PAD) 劫持文本→视觉注意力 |
| **语义错位** | 无 | Patch Semantic Misalignment (PSM) 主动错位指令语义 |
| **迁移性理论保证** | 无 | 基于线性对齐假设的偏差下界（命题1） |
| **代理模型依赖性** | 高（需针对每个受害者调整） | 低（单代理模型OpenVLA-7B即可跨模型迁移） |

### 四大创新槽位详解

#### 槽位一：特征空间联合损失（ℓ₁ + 排斥性InfoNCE）

传统方法直接最大化任务损失，导致补丁过拟合代理模型的特定决策边界。UPA-RFAS将攻击目标重新定义为**在代理特征空间中最大化表示偏差**，具体由两项组成：

- **ℓ₁偏差损失**：最大化代理侧干净特征与补丁特征之间的ℓ₁距离。选择ℓ₁而非ℓ₂的原因是ℓ₁对高维特征中的稀疏大偏差更敏感，能更有效地驱动特征沿共享子空间的关键维度位移。
- **排斥性对比损失（InfoNCE）**：将补丁特征推离其对应的干净锚点，同时沿批次内一致的高CCA方向集中变化。这一设计迫使补丁引起的特征位移不仅幅度大，而且方向与共享子空间的对齐方向一致，从而保证迁移性。

联合损失 $\mathcal{J}_{\mathrm{tr}} = \mathcal{L}_{1} + \lambda_{\mathrm{con}} \mathcal{L}_{\mathrm{con}}$ 是迁移能力的核心引擎。消融实验提供了强有力的证据：**移除联合特征损失后，攻击效果断崖式下降**——平均成功率从61.50%反弹至85.75%（物理场景，OpenVLA-oft-w受害者），验证了特征空间目标对迁移性的决定性作用。

#### 槽位二：鲁棒性增强双层优化

传统方法在固定代理模型上优化补丁，忽略了模型本身的脆弱性差异对迁移性的影响。UPA-RFAS引入**鲁棒性增强双层优化（RUPA）**，将训练过程重构为min-max博弈：

- **内部最小化**：冻结补丁，通过PGD学习样本级微小扰动σ（ϵ=4/255时效果最优），模拟局部对抗训练以“硬化”代理模型的特征空间。
- **外部最大化**：冻结σ，通过AdamW优化通用物理补丁δ，使其在硬化后的代理模型上仍能最大化组合转移损失。

这一设计的直觉是：如果补丁能在一个经过对抗性硬化的代理模型上仍然有效，那么它学到的攻击模式更可能具有本质性和可迁移性。消融实验证实：去除RUPA后平均成功率升至62.25%，而ϵ=4/255时获得最强迁移（58.00%），过大或过小的扰动均导致退化。这表明RUPA起到了“局部对抗训练循环”的作用，适度噪声水平产生最强迁移。

#### 槽位三：Patch Attention Dominance (PAD) — 跨模态注意力劫持

VLA模型的核心机制是文本指令通过交叉注意力引导视觉特征的聚合。现有方法未利用这一结构。UPA-RFAS提出**PAD损失**，主动劫持文本→视觉的注意力流：

$$\mathcal{L}_{\mathrm{PAD}} = \mathbb{E}[d_{\mathrm{patch}}] - \lambda \mathbb{E}[\mathrm{ReLU}(d_{\mathrm{non}})] - \mathbb{E}[\mathrm{ReLU}(m - (d_{\mathrm{patch}} - \mathrm{non.top}))]$$

其中 $d_{\mathrm{patch}}$ 和 $d_{\mathrm{non}}$ 分别衡量补丁区域和非补丁区域的注意力增量，$\mathrm{non.top}$ 为最强非补丁增量的上界。PAD的三项分别实现：最大化补丁注意力增量、惩罚非补丁增量、强制补丁增量超出最强非补丁增量至少m的边距。

这一设计确保动作相关的文本查询（如“移动”“抓取”）将注意力过度集中在补丁区域，从而污染下游的动作预测。消融显示去除PAD后成功率升至62.50%，证明注意力劫持是攻击链的关键环节。

#### 槽位四：Patch Semantic Misalignment (PSM) — 语义错位

PAD劫持了注意力流向，但补丁区域的视觉语义仍可能与正确指令一致。PSM损失进一步**主动控制补丁的语义内容**：

$$\mathcal{L}_{\mathrm{PSM}} = \alpha \left[ \log \sum_{k=1}^{K} \exp \left( \frac{\hat{\mathbf{v}}_{\mathrm{patch}}^{\top} \hat{\mathbf{p}}_k}{\tau} \right) \right] - \beta \hat{\mathbf{v}}_{\mathrm{patch}}^{\top} \hat{\mathbf{t}}$$

其中 $\hat{\mathbf{v}}_{\mathrm{patch}}$ 为补丁视觉特征，$\hat{\mathbf{p}}_k$ 为跨模型稳定的动作/方向探针原型（如“向左移动”“向下抓取”），$\hat{\mathbf{t}}$ 为当前指令嵌入。第一项将补丁语义拉向动作探针原型，第二项将其推离正确指令嵌入。两者共同作用使补丁在语义空间中“说错话”——即使注意力正确聚焦，模型读到的也是错误的动作意图。消融显示去除PSM后成功率升至63.50%，验证了语义错位的独立贡献。

### 创新总结

UPA-RFAS的四项创新构成了一个**分层递进的攻击体系**：特征空间联合损失提供迁移性的理论基础和主要驱动力；鲁棒性增强双层优化硬化代理模型以提升迁移强度；PAD劫持注意力流向确保攻击信息进入决策路径；PSM错位语义内容确保进入的信息是错误的。四者协同，使单一代理模型上训练的5%面积补丁能在黑盒条件下将受害者VLA策略的成功率从76.5%压低至5.75%（仿真）和40.25%（物理），大幅超越所有现有基线。

UPA‑RFAS 的总体设计遵循**“共享特征空间内的鲁棒通用补丁生成”**这一核心思想，整个 pipeline 围绕一个两阶段双层优化框架展开，如图 1 所示。攻击者仅需访问单个代理 VLA 模型（本文采用 OpenVLA‑7B），即可训练出一个面积受限（默认 5%）的通用物理补丁，该补丁可迁移至多种未知受害者策略、不同任务甚至物理环境。

### 输入与预处理

给定一段机器人操作演示视频，每帧观测图像 $\mathbf{x}_t$ 首先经过**补丁渲染模块**处理：

$$\tilde{\mathbf{x}}_t = \mathcal{P}(\mathbf{x}_t, \delta, T_t) = (\mathbf{1} - \mathbf{M}_{T_t}) \odot \mathbf{x}_t + \mathbf{M}_{T_t} \odot \mathcal{R}(\delta; T_t) \quad \mathrm{s.t.} \quad \mathcal{S}(\delta) < \rho$$

其中 $\delta$ 为待优化的通用补丁，$T_t$ 为随机采样的几何变换（平移、缩放、旋转等），$\mathcal{R}(\delta; T_t)$ 将补丁按变换参数渲染，$\mathbf{M}_{T_t}$ 为对应的二值掩码，$\mathcal{S}(\delta) < \rho$ 约束补丁面积不超过阈值。这一随机化渲染策略迫使补丁学会对空间位置和几何形变不敏感，是保证物理鲁棒性与跨场景迁移的基础。

### 视觉编码与特征提取

渲染后的帧 $\tilde{\mathbf{x}}_t$ 被送入代理模型的**视觉编码器** $f_v$，该编码器融合了 DINOv2 和 SigLIP 两种预训练视觉 backbone 的多粒度特征。随后，**视觉投影器** $f_{\mathrm{prj}}$ 将这些视觉嵌入对齐到大语言模型（LLM）的令牌空间，形成视觉令牌序列。同时，任务指令经文本分词后嵌入为文本令牌。视觉令牌与文本令牌拼接后送入 **LLM 主干** $f_{\mathrm{llm}}$ 进行跨模态融合，最终由**动作头** $f_{\mathrm{act}}$ 解码出连续动作指令。

### 两阶段双层优化

UPA‑RFAS 的核心优化采用**鲁棒性增强的双层 min‑max 结构**，分为内部最小化与外部最大化两个交替执行的阶段：

**Phase 1 — 内部最小化（RUPA Inner Loop）**：固定通用补丁 $\delta$，对每帧观测引入一个微小的、不可见的样本级扰动 $\sigma$，通过投影梯度下降（PGD）在 $\ell_\infty$ 约束下最小化特征空间目标 $\mathcal{J}_{\mathrm{tr}}$：

$$\boldsymbol{\sigma}^{(i+1)} = \Pi_{\|\cdot\|_\infty \leq \epsilon_\sigma} \left( \boldsymbol{\sigma}^{(i)} - \eta_\sigma \nabla_{\boldsymbol{\sigma}} \mathcal{I}_{\mathrm{in}} \left( \mathcal{P}(\mathbf{x} + \boldsymbol{\sigma}^{(i)}, \boldsymbol{\delta}, T_t); \hat{\pi} \right) \right)$$

该阶段的本质是对代理模型进行**局部对抗训练**，硬化其特征空间，使得后续外部优化产生的补丁具有更强的迁移鲁棒性。消融实验证实，$\epsilon=4/255$ 时迁移效果最优（平均成功率降至 58.00%），过大或过小均导致性能退化。

**Phase 2 — 外部最大化（UPA‑RFAS Outer Loop）**：冻结样本级扰动 $\sigma$，通过 AdamW 优化器更新通用补丁 $\delta$，最大化组合损失 $\mathcal{I}_{\mathrm{out}}$：

$$\mathcal{I}_{\mathrm{out}} = \mathcal{L}_{1} + \lambda_{\mathrm{con}} \mathcal{L}_{\mathrm{con}} + \lambda_{\mathrm{PAD}} \mathcal{L}_{\mathrm{PAD}} + \lambda_{\mathrm{PSM}} \mathcal{L}_{\mathrm{PSM}}$$

该组合损失由四个模块级联构成，分别从特征空间、注意力机制和语义空间三个层面协同攻击 VLA 策略。

### 四大攻击损失模块

**（1）特征空间目标 $\mathcal{J}_{\mathrm{tr}}$**：由 $\ell_1$ 特征偏差损失与排斥性对比损失加权组成：

$$\mathcal{J}_{\mathrm{tr}} = \mathcal{L}_{1} + \lambda_{\mathrm{con}} \mathcal{L}_{\mathrm{con}}$$

其中 $\mathcal{L}_1$ 最大化代理模型特征空间中干净帧与补丁帧之间的 $\ell_1$ 距离，利用代理与目标 VLA 特征空间的高度线性对齐（$\mathrm{R}^2 \approx 0.654$，top‑k CCA 接近 1）保证目标侧必然产生非平凡偏差。$\mathcal{L}_{\mathrm{con}}$ 为排斥性 InfoNCE 损失，将补丁特征推离干净锚点并沿批次一致的高 CCA 方向集中变化：

$$\mathcal{L}_{\mathrm{con}} = -\frac{1}{N}\sum_{i=1}^{N}\log\frac{\exp(\mathrm{sim}(\mathbf{z}_i, \tilde{\mathbf{z}}_i)/\tau)}{\sum_{j=1}^{N}\exp(\mathrm{sim}(\mathbf{z}_i, \tilde{\mathbf{z}}_j)/\tau)}$$

消融实验表明，移除 $\mathcal{J}_{\mathrm{tr}}$ 后攻击效果断崖式下降，平均成功率从 61.50% 反弹至 85.75%，验证了特征空间目标是迁移性的关键瓶颈。

**（2）Patch Attention Dominance（PAD）损失**：劫持文本→视觉的跨模态注意力，使动作相关查询（如“move forward”）的注意力增量集中到补丁区域：

$$\mathcal{L}_{\mathrm{PAD}} = \mathbb{E}[d_{\mathrm{patch}}] - \lambda \mathbb{E}[\mathrm{ReLU}(d_{\mathrm{non}})] - \mathbb{E}[\mathrm{ReLU}(m - (d_{\mathrm{patch}} - \mathrm{non.top}))]$$

其中 $d_{\mathrm{patch}}$ 和 $d_{\mathrm{non}}$ 分别度量补丁区域与非补丁区域的注意力增量，第三项强制补丁增量超出最强非补丁增量至少 $m$ 的裕度。

**（3）Patch Semantic Misalignment（PSM）损失**：将补丁的视觉语义拉向一组跨模型稳定的动作/方向探针原型，同时推离当前指令嵌入，造成指令‑视觉语义错位：

$$\mathcal{L}_{\mathrm{PSM}} = \alpha \left[ \log \sum_{k=1}^{K} \exp \left( \frac{\hat{\mathbf{v}}_{\mathrm{patch}}^{\top} \hat{\mathbf{p}}_k}{\tau} \right) \right] - \beta \hat{\mathbf{v}}_{\mathrm{patch}}^{\top} \hat{\mathbf{t}}$$

消融实验显示，去除 PAD 后平均成功率升至 62.50%，去除 PSM 后升至 63.50%，两者均为攻击强度的关键贡献因子。

### 输出与评估

训练完成后，UPA‑RFAS 输出单一通用物理补丁 $\delta^\star$。在推理阶段，该补丁被打印并粘贴于机器人操作场景中的固定位置（如桌面），受害者 VLA 策略在不知情的情况下通过其视觉观测感知到补丁，从而被诱导产生错误动作。评估指标为任务成功率（Task Success Rate），越低表示攻击越强。白盒场景下仿真平均成功率仅 0.5%，物理场景仅 2.75%；黑盒迁移至微调变体 OpenVLA‑oft‑w 时，仿真成功率降至 5.75%，物理场景降至 40.25%，显著优于 UMA、UADA、TMA 等基线方法。

![[assets/figures/papers/paper_list_l2431_https_arxiv_org_abs_2511_21192/figures/001_Figure_1.jpg]]
*Figure 1: Overall transferable patch attack (UPA-RFAS) for VLA robotics. The framework operates in two coordinated stages within a shared feature-space objective. Phase 1 – Inner minimization learns a small, invisible, sample-wise perturbation σ via PGD that minimizes the feature objective Jin (§ 3.3) with the patch frozen (§ 3.4). Phase 2 – Outer maximization freezes σ and optimizes a single physical patch δ to maximize Jout (§ 3.7), which combines an*

### 3.1 问题形式化与补丁渲染

给定一帧观测图像 $\mathbf{x}_t$、一个通用物理补丁 $\delta$ 和一个随机仿射变换 $T_t$，补丁渲染算子 $\mathcal{P}$ 将变换后的补丁叠加到图像上：

$$\tilde{\mathbf{x}}_t = \mathcal{P}(\mathbf{x}_t, \delta, T_t) = (\mathbf{1} - \mathbf{M}_{T_t}) \odot \mathbf{x}_t + \mathbf{M}_{T_t} \odot \mathcal{R}(\delta; T_t) \quad \mathrm{s.t.} \quad \mathcal{S}(\delta) < \rho$$

其中 $\mathbf{M}_{T_t}$ 是变换后的二值掩码，$\mathcal{R}(\delta; T_t)$ 对补丁施加几何变换（旋转、缩放、透视），$\mathcal{S}(\delta) < \rho$ 约束补丁面积不超过预算 $\rho$。这一形式化确保了补丁在物理部署中能适应视角变化和空间扰动。

### 3.2 威胁模型与可迁移攻击目标

攻击者仅拥有单个代理模型 $\hat{\pi}$ 的梯度访问权，目标是学习一个通用补丁 $\delta_s$，使其在未见过的受害者策略族 $\Pi_{\mathrm{tgt}}$ 上最大化任务失败率。形式化目标为：

$$\underset{\pmb{\delta}_s}{\operatorname{max}} \ \mathbb{E}_{\pi \sim \Pi_{\mathbf{tgt}}} \mathbb{E}_{\mathbf{x} \sim p(\mathbf{x})} \left[ \mathcal{I}_{\mathrm{eval}} \left( \mathcal{P}(\mathbf{x}, \pmb{\delta}_s, T); \pi \right) \right]$$

由于目标策略不可访问，补丁在代理特征空间内通过可微分的迁移目标 $\mathcal{I}_{\mathrm{tr}}$ 优化：

$$\delta_s \in \arg \underset{\pmb{\delta}}{\operatorname{max}} \ \mathbb{E}_{\mathbf{x} \sim p(\mathbf{x})} \left[ \mathcal{I}_{\mathrm{tr}} \left( \mathcal{P}(\mathbf{x}, \pmb{\delta}, T); \hat{\pi} \right) \right]$$

核心挑战在于设计 $\mathcal{I}_{\mathrm{tr}}$，使其在代理模型上的最大化能可靠地转化为目标模型上的评估损失 $\mathcal{I}_{\mathrm{eval}}$ 最大化。

### 3.3 特征空间可迁移性：线性对齐假设与联合目标

**线性对齐假设** 是方法可迁移性的理论基石。实证分析表明，代理模型与目标模型的视觉特征处于同一低维线性子空间（$R^2 \approx 0.654$，top-k 典型相关系数接近 1）。基于此，提出：

**假设 1（有界残差线性对齐）**：存在矩阵 $A^{\star}$，使得目标编码器输出可表示为代理编码器输出的线性变换加有界残差：

$$f_{\pi}(\mathbf{x}) = f_{\hat{\pi}}(\mathbf{x}) A^{\star} + e(\mathbf{x}), \quad \|e(\tilde{\mathbf{x}}) - e(\mathbf{x})\|_2 \leq \varepsilon_E$$

在该假设下，目标侧特征偏差由代理侧偏差下界约束：

$$\|\Delta \mathbf{g}_i\|_2 \geq \sigma_{\min}(A^{\star}) \|\Delta \mathbf{z}_i\|_2 - \varepsilon_E$$

其中 $\sigma_{\min}(A^{\star})$ 是 $A^{\star}$ 的最小奇异值。这意味着**最大化代理侧特征偏差可在目标侧引发不可忽略的偏差**，为可迁移攻击提供理论保证。

基于此，设计**联合特征空间目标** $\mathcal{J}_{\mathrm{tr}}$，由两项构成：

$$\mathcal{J}_{\mathrm{tr}} = \mathcal{L}_{1} + \lambda_{\mathrm{con}} \mathcal{L}_{\mathrm{con}}$$

- **$\mathcal{L}_1$（ℓ₁ 偏差损失）**：最大化干净特征 $\mathbf{z}_i$ 与补丁污染特征 $\tilde{\mathbf{z}}_i$ 之间的 ℓ₁ 距离。选择 ℓ₁ 而非 ℓ₂ 是因为 ℓ₁ 对异常维度更敏感，能沿高 CCA 方向产生更集中的位移，避免能量分散到与目标模型无关的维度。

- **$\mathcal{L}_{\mathrm{con}}$（排斥性对比损失）**：采用 InfoNCE 形式，将补丁特征推离对应的干净锚点，同时沿批次内一致的高 CCA 方向集中变化：

$$\mathcal{L}_{\mathrm{con}} = -\frac{1}{N}\sum_{i=1}^{N}\log\frac{\exp(\mathrm{sim}(\mathbf{z}_i, \tilde{\mathbf{z}}_i)/\tau)}{\sum_{j=1}^{N}\exp(\mathrm{sim}(\mathbf{z}_i, \tilde{\mathbf{z}}_j)/\tau)}$$

其中 $\mathrm{sim}(\cdot,\cdot)$ 为余弦相似度，$\tau$ 为温度系数。该损失迫使补丁引起的特征位移沿共享子空间的主方向对齐，抑制模型特异性扰动，从而提升跨模型迁移性。

### 3.4 鲁棒性增强双层优化（RUPA）

为模拟目标模型的局部鲁棒性差异，UPA-RFAS 采用**双层 min-max 优化**，在不重新训练 VLA 的前提下硬化代理模型：

$$\pmb{\delta}^{\star} \in \arg \underset{\mathcal{S}(\pmb{\delta}) < \rho}{\operatorname{max}} \ \mathbb{E}_{\mathbf{x} \sim p(\mathbf{x})} \ \mathcal{I}_{\mathrm{tr}} \left( \mathcal{P}(\mathbf{x} + \pmb{\sigma}^{\star}(\pmb{\delta}), \pmb{\delta}, T); \hat{\pi} \right)$$

$$\text{s.t.} \quad \pmb{\sigma}^{\star}(\pmb{\delta}) = \arg \underset{\|\pmb{\sigma}\|_{\infty} \leq \epsilon_{\sigma}}{\operatorname{min}} \ \mathcal{I}_{\mathrm{in}} \left( \mathcal{P}(\mathbf{x} + \pmb{\sigma}, \pmb{\delta}, T); \hat{\pi} \right)$$

- **内部最小化（Inner Loop）**：冻结补丁 $\delta$，通过 PGD 学习样本级微小扰动 $\sigma$，最小化特征空间目标 $\mathcal{I}_{\mathrm{in}}$。这模拟了目标模型可能具备的局部对抗鲁棒性，迫使外部补丁学会在“硬化”的代理邻域内仍有效。内部 PGD 更新公式为：

$$\boldsymbol{\sigma}^{(i+1)} = \Pi_{\|\cdot\|_{\infty} \leq \epsilon_{\sigma}} \left( \boldsymbol{\sigma}^{(i)} - \eta_{\sigma} \nabla_{\boldsymbol{\sigma}} \mathcal{I}_{\mathrm{in}} \left( \mathcal{P}(\mathbf{x} + \boldsymbol{\sigma}^{(i)}, \boldsymbol{\delta}, T_t); \hat{\pi} \right) \right)$$

- **外部最大化（Outer Loop）**：冻结 $\sigma$，通过 AdamW 优化单一通用补丁 $\delta$，最大化组合损失 $\mathcal{I}_{\mathrm{out}}$：

$$\mathcal{I}_{\mathrm{out}} = \mathcal{L}_{1} + \lambda_{\mathrm{con}} \mathcal{L}_{\mathrm{con}} + \lambda_{\mathrm{PAD}} \mathcal{L}_{\mathrm{PAD}} + \lambda_{\mathrm{PSM}} \mathcal{L}_{\mathrm{PSM}}$$

消融实验（Table 8）验证了双层优化的关键作用：内部扰动界限 $\epsilon = 4/255$ 时获得最强迁移性（平均成功率 58.00%），过大或过小均导致退化——这表明适度噪声水平模拟了“局部对抗训练”效应，产生最强迁移强度。

### 3.5 跨模态注意力劫持：Patch Attention Dominance (PAD)

VLA 模型中，文本指令通过交叉注意力引导视觉特征提取。PAD 损失旨在**劫持文本→视觉的注意力流**，使动作相关的文本查询将注意力集中于补丁区域，从而污染下游动作预测。

具体地，定义补丁令牌与非补丁令牌的注意力增量：

$$d_{\mathrm{patch}} = \langle \tilde{\Delta}, \mathbf{M}_z \rangle_p, \quad d_{\mathrm{non}} = \langle \tilde{\Delta}, \mathbf{1} - \mathbf{M}_z \rangle_p, \quad \mathrm{non.top} = \max_p \big( \tilde{\Delta} \odot (\mathbf{1} - \mathbf{M}_z) \big)$$

其中 $\tilde{\Delta}$ 为补丁污染前后动作相关文本查询对视觉令牌的注意力差异，$\mathbf{M}_z$ 为视觉令牌空间中的补丁掩码，$\langle \cdot, \cdot \rangle_p$ 表示按位置聚合。

PAD 损失由三项组成：

$$\mathcal{L}_{\mathrm{PAD}} = \mathbb{E}[d_{\mathrm{patch}}] - \lambda \mathbb{E}[\mathrm{ReLU}(d_{\mathrm{non}})] - \mathbb{E}[\mathrm{ReLU}(m - (d_{\mathrm{patch}} - \mathrm{non.top}))]$$

- **第一项**：最大化补丁区域的注意力增量，将文本查询“吸引”到补丁。
- **第二项**：惩罚非补丁区域的注意力增量，抑制正常视觉信息的利用。
- **第三项**：强制补丁增量超出最强非补丁增量至少 $m$（margin），确保补丁在注意力竞争中占据主导地位。

### 3.6 语义错位：Patch Semantic Misalignment (PSM)

PSM 损失在**语义空间**中操控补丁的视觉表征，使其与当前指令语义错位，从而诱导错误的动作输出。具体策略是将补丁特征拉向一组跨模型稳定的**动作/方向探针原型**（如 "move left", "rotate gripper"），同时推离当前指令的整体嵌入：

$$\mathcal{L}_{\mathrm{PSM}} = \alpha \left[ \log \sum_{k=1}^{K} \exp \left( \frac{\hat{\mathbf{v}}_{\mathrm{patch}}^{\top} \hat{\mathbf{p}}_k}{\tau} \right) \right] - \beta \ \hat{\mathbf{v}}_{\mathrm{patch}}^{\top} \hat{\mathbf{t}}$$

其中：
- $\hat{\mathbf{v}}_{\mathrm{patch}}$ 为归一化的补丁视觉特征；
- $\{\hat{\mathbf{p}}_k\}_{k=1}^{K}$ 为归一化的探针原型嵌入（预定义的对抗性动作/方向短语）；
- $\hat{\mathbf{t}}$ 为归一化的当前指令嵌入；
- $\alpha, \beta$ 控制吸引与排斥的强度；
- LogSumExp 形式鼓励补丁特征靠近任意一个探针原型，而非单一原型，增强泛化性。

消融实验（Table 3）表明，探针短语的具体措辞对攻击效果有影响，但方法对措辞变化不极端敏感，验证了语义错位机制的鲁棒性。

### 3.7 训练流程总览

UPA-RFAS 的两阶段训练流程（Figure 1）可总结为：

1. **Phase 1 – 内部最小化**：冻结补丁 $\delta$，对每帧通过 PGD 学习样本级扰动 $\sigma$，最小化特征空间目标 $\mathcal{I}_{\mathrm{in}}$（§3.3），硬化代理模型的特征邻域。
2. **Phase 2 – 外部最大化**：冻结 $\sigma$，通过 AdamW 优化通用补丁 $\delta$，最大化组合损失 $\mathcal{I}_{\mathrm{out}}$（Eq. 20），融合 ℓ₁ 偏差、排斥对比、注意力劫持（PAD）和语义错位（PSM）四项目标。

整个流程仅需单个代理模型（如 OpenVLA-7B）的梯度访问，无需接触受害者模型，契合真实黑盒威胁模型。消融实验（Table 2）逐一验证了各模块的关键贡献：移除联合特征损失 $\mathcal{J}_{\mathrm{tr}}$ 导致成功率从 61.50% 反弹至 85.75%；去除 RUPA 升至 62.25%；去除 PAD 或 PSM 分别升至 62.50% 和 63.50%，证实四者协同是实现强可迁移性的必要条件。

## 实验与关键发现

### 核心假设验证

UPA-RFAS 的迁移能力建立在代理模型与受害者模型特征空间线性对齐的前提之上。分析表明，代理模型 OpenVLA-7B 与目标模型（如 OpenVLA-oft-w）的视觉特征处于同一低维线性子空间：回归决定系数 $R^2 \approx 0.654$，且 top-k 典型相关系数接近 1。基于这一实证观察，论文提出**假设1**——存在有界残差的线性对齐矩阵 $A^\star$ 使得 $f_{\pi}(\mathbf{x}) = f_{\hat{\pi}}(\mathbf{x}) A^{\star} + e(\mathbf{x})$，其中 $\|e(\tilde{\mathbf{x}}) - e(\mathbf{x})\|_2 \leq \varepsilon_E$。在此假设下，**命题1及其推论1**保证了代理侧最大化 $\ell_1$ 偏差在目标侧必然引起非平凡位移，其 $\ell_2$ 下界为 $\sigma_{\min}(A^{\star}) \|\Delta \mathbf{z}_i\|_2 - \varepsilon_E$。这一理论保证构成了后续所有迁移实验的基石。

### 实验设置

攻击仅需单一代理模型 **OpenVLA-7B**（微调变体 openvla-oft），无需访问受害者网络内部参数。通用物理补丁面积固定为 $50 \times 50$ 像素（占 $224 \times 224$ 观测帧的约 5%），在训练过程中经历随机几何变换（缩放、旋转、平移、透视）以模拟物理部署中的视角变化。实验覆盖**仿真**（LIBERO 基准的渲染观测）和**物理**（真实机器人采集的含杂波、运动模糊的图像）两种设定，受害者模型包括 OpenVLA-oft-w、OpenVLA-oft 及 $\pi_0$ 等不同架构与微调变体。

### 黑盒迁移攻击主结果

Table 1 展示了从代理 OpenVLA-7B 向不同受害者模型迁移时的任务成功率。UPA-RFAS 在所有受害者上均取得最低成功率，验证了其跨模型通用性。

![[assets/figures/papers/paper_list_l2431_https_arxiv_org_abs_2511_21192/figures/002_Table_1.jpg]]
*Table 1: Task success rate (%) when transferring from the surrogate OpenVLA-7B to different victim models on LIBERO*

- **仿真设定**：良性策略成功率为 76.5%，UPA-RFAS 将受害者 OpenVLA-oft-w 的成功率降至仅 **5.75%**（降幅 70.75 个百分点），对 OpenVLA-oft 降至 11.25%。相比之下，最强基线 UADA1-3 仅能将成功率压至 17.00%（OpenVLA-oft-w）和 22.50%（OpenVLA-oft），TMA 则为 27.75% 和 34.00%。值得注意的是，UPA-RFAS 在攻击 $\pi_0$（与代理模型架构差异最大的受害者）时仍将成功率从 92.0% 降至 86.0%，虽降幅有限（6 个百分点），但已超越所有基线（UADA1-3 为 89.5%，TMA 为 90.0%），体现了特征空间目标的部分跨架构迁移能力。

- **物理设定**：真实世界杂波、运动模糊和透视畸变显著增加了攻击难度。良性策略成功率仍为 76.5%，UPA-RFAS 将 OpenVLA-oft-w 成功率降至 **40.25%**（降幅 36.25 个百分点），OpenVLA-oft 降至 42.50%。相比之下，UADA1-3 分别为 51.75% 和 52.75%，TMA 为 62.75% 和 66.00%。物理场景下攻击未能使策略完全失效，这与 sim-to-real 漂移及机械臂冗余自由度对错误动作的缓冲效应有关，但 UPA-RFAS 仍以显著优势领先所有基线。

### 白盒攻击结果

在代理模型自身（白盒设定）上，UPA-RFAS 几乎完全瘫痪策略：仿真设定下平均成功率仅 **0.5%**（良性 76.5%），物理设定下平均 **2.75%**（Table 4）。即使将补丁应用于与训练域不同的 LIBERO 子数据集（△标记），成功率仍保持在极低水平（仿真 1.25%，物理 3.50%），表明补丁对任务分布变化具有鲁棒性。

![[assets/figures/papers/paper_list_l2431_https_arxiv_org_abs_2511_21192/figures/006_Table_4.jpg]]
*Table 4: We report the success rate (SR) on LIBERO simulation in a white-box setup. ∗ marks an in-domain dataset matching the patchtraining data, and*

### 跨模型迁移：OpenVLA-7B → $\pi_0$

Table 5 单独报告了从 OpenVLA-7B 到 $\pi_0$ 的迁移结果。在仿真设定下，UPA-RFAS 将 $\pi_0$ 成功率从 92.0% 降至 86.0%（降幅 6 个百分点），优于 UADA1-3（89.5%）和 TMA（90.0%）。物理设定下降幅更小（从 92.0% 降至 88.5%），但仍是唯一在 $\pi_0$ 上产生非平凡降幅的方法。这一结果揭示了一个关键瓶颈：当代理与受害者视觉编码器架构差异极大（DINOv2+SigLIP 融合 vs. $\pi_0$ 专用编码器）时，共享低维子空间的假设部分失效，迁移强度显著衰减。

### 消融实验

Table 2 系统拆解了 UPA-RFAS 各组件对物理场景下向 OpenVLA-oft 迁移的贡献。

![[assets/figures/papers/paper_list_l2431_https_arxiv_org_abs_2511_21192/figures/004_Table_2.jpg]]
*Table 2: Ablation for transfer to openvla-oft under physical setting*

| 消融变体 | 平均成功率 (%) | 关键发现 |
|---------|--------------|---------|
| 完整 UPA-RFAS | **61.50** | 所有组件协同工作的基线 |
| w/o $\mathcal{J}_{\mathrm{tr}}$（移除联合特征损失） | 85.75 | 攻击几乎完全失效，$\ell_1$+InfoNCE 是迁移的核心驱动力 |
| w/o RUPA（去除鲁棒性增强） | 62.25 | 双层优化对迁移性有显著贡献 |
| w/o PAD（去除注意力劫持） | 62.50 | 跨模态注意力操控独立增强攻击 |
| w/o PSM（去除语义错位） | 63.50 | 语义控制提供额外增益 |

**特征空间目标的决定性作用**：移除联合特征损失 $\mathcal{J}_{\mathrm{tr}}$（即仅保留 PAD 和 PSM 而无 $\ell_1$ 偏差与 InfoNCE）导致平均成功率从 61.50% 反弹至 85.75%，接近良性水平。这直接验证了核心洞察——代理与目标共享低维子空间，因此最大化代理侧 $\ell_1$ 偏差并沿高 CCA 方向排斥对比是迁移性的必要条件。

**鲁棒性增强的精细调控**：RUPA 内部扰动界限 $\epsilon$ 的影响呈 U 形曲线（Table 8）。当 $\epsilon$ 从 1/255 增至 4/255 时，平均成功率从 63.25% 持续降至 **58.00%**（最强迁移点）；进一步增大 $\epsilon$ 至 8/255 和 16/255 时，成功率反而回升至 60.25% 和 62.75%。这表明适度的内部对抗扰动（$\epsilon=4/255$）在硬化代理特征空间与保持可优化性之间取得最佳平衡，过大扰动破坏了特征空间的可用结构。

**注意力与语义模块的独立增益**：单独移除 PAD 或 PSM 分别使成功率升至 62.50% 和 63.50%，证明两者均提供不可替代的攻击增量。PAD 通过劫持文本→视觉注意力使动作相关查询聚焦补丁区域，PSM 则将补丁语义拉向“向下移动”“向左旋转”等动作探针原型并推离当前指令嵌入，两者从不同维度瓦解 VLA 的跨模态对齐。

**补丁面积的影响**：Table 6 显示补丁面积从 5% 增至 10% 可使平均成功率进一步降至 20.75%，但 5% 已提供良好的攻防权衡。面积减小至 3% 和 1% 时，成功率分别回升至 68.50% 和 74.50%，表明物理攻击需要足够的像素预算来维持特征空间扰动强度。

**超参数敏感性**：$\lambda_{\mathrm{con}}$ 在 1–10 区间内攻击强度单调增强（63.75% → 61.50%），在 5–10 区间趋于平台（Table 7），表明方法对该超参数不敏感，便于实际调优。

### 语义探针措辞的影响

Table 3 研究了 PSM 中文本探针措辞对攻击效果的影响。使用动作导向探针（“move down”“rotate left”等）取得最优效果（61.50%），而使用方向描述（“downward”“leftward”）或抽象概念（“failure”“error”）时攻击强度分别降至 63.25% 和 64.00%。这表明与机器人动作空间直接对齐的语义锚点能最有效地错位补丁特征与指令嵌入。

![[assets/figures/papers/paper_list_l2431_https_arxiv_org_abs_2511_21192/figures/005_Table_3.jpg]]
*Table 3: Ablation on text-probe phrasing for transfer to openvlaoft in the physical setting*

### 失败模式与局限性

1. **物理场景残余成功率**：即使在最强配置下，物理场景中受害者成功率仍有 40.25%。真实世界的严重杂波、运动模糊和透视畸变使补丁特征在投影后部分退化，且机械臂的冗余自由度可缓冲部分错误动作指令。sim-to-real 迁移仍是开放挑战。

2. **跨架构迁移衰减**：向 $\pi_0$ 的迁移降幅仅 6 个百分点（仿真），远低于向 OpenVLA 变体的 70+ 个百分点。当代理与受害者视觉编码器架构差异极大时，线性对齐假设的残差 $\varepsilon_E$ 增大，$\ell_2$ 下界松弛，迁移效率显著下降。

3. **隐蔽性与攻击力的权衡**：补丁面积需达 5% 才能保证强攻击力，更小的隐蔽补丁（1%–3%）攻击效果大幅削弱。实际部署中需根据场景容忍度调整面积。

4. **单模态攻击局限**：方法仅操纵视觉模态，未涉及语言指令或动作空间的联合扰动。在多传感器融合的机器人系统中，其他模态可能提供冗余信息缓冲攻击影响。

![[assets/figures/papers/paper_list_l2431_https_arxiv_org_abs_2511_21192/figures/011_Figure_3.jpg]]
*Figure 3: Qualitative real-world results. The top row displays benign executions, while the bottom row shows their adversarial counterparts*

## 定位与知识库关联

### 1. 问题定位：从白盒过拟合到通用可迁移攻击

现有针对视觉‑语言‑动作（VLA）模型的物理补丁攻击面临一个核心瓶颈：**严重过拟合单一代理模型，在黑盒条件下迁移性极差**。以 **UMA** 和 **UADA** 系列为代表的现有方法，其攻击优化目标直接锚定于任务级动作损失（如 RoboticAttack），这使得补丁在训练代理模型上表现良好，但一旦面对未知架构、微调变体或 sim‑to‑real 分布漂移，攻击效果便急剧退化。这种“白盒强、黑盒弱”的模式在真实机器人安全评估中几乎不构成威胁——攻击者通常无法获取受害者模型的梯度信息。

UPA‑RFAS 的出发点正是将攻击范式从**模型特定**转向**特征空间通用**。其核心假设（经实验验证）是：不同 VLA 模型的视觉编码器输出处于同一低维线性子空间，表现为代理与目标特征之间的高线性决定系数（R² ≈ 0.654）和接近 1 的 top‑k 典型相关系数（CCA）。基于这一共享子空间的存在，攻击者仅需在单个代理模型的特征空间中最大化 ℓ₁ 偏差，即可在目标侧产生非平凡的特征位移（命题 1 及推论 1 给出线性下界保证），从而实现跨模型迁移。

### 2. 与现有攻击范式的关键差异

| 维度 | 现有方法（UMA/UADA/TMA/DOF） | UPA‑RFAS |
|------|------------------------------|----------|
| **优化目标** | 任务/动作损失（单环梯度上升） | 特征空间 ℓ₁ 偏差 + 排斥性 InfoNCE 对比损失 + PAD + PSM |
| **训练范式** | 直接优化补丁像素 | 鲁棒性增强双层优化（内部 PGD 硬化 + 外部 AdamW 优化） |
| **跨模态操控** | 无专门注意力劫持 | PAD 损失劫持文本→视觉注意力，使动作查询聚焦补丁区域 |
| **语义控制** | 无 | PSM 损失将补丁语义拉向动作/方向探针原型，推离指令嵌入 |
| **迁移机制** | 依赖像素级模式过拟合 | 基于共享低维子空间的 ℓ₁ 偏差最大化 + 排斥对比对齐 |

具体而言，**UMA** 系列直接在动作损失上做梯度上升，补丁学到的是代理模型特定的决策边界扰动，缺乏跨模型泛化能力。**UADA** 引入注意力机制但仅作用于白盒场景，未涉及跨模态注意力劫持或语义错位。**TMA** 聚焦任务级动作攻击，**DOF1/DOF7** 在单自由度或七自由度动作空间上操作，均未触及特征空间迁移的本质。UPA‑RFAS 通过四个协同模块（特征空间目标、鲁棒双层优化、PAD、PSM）首次构建了完整的通用可迁移补丁攻击体系。

### 3. 方法适用边界

**有效域**：
- 受害者模型与代理模型共享足够的低维线性子空间（如 OpenVLA‑7B → OpenVLA‑oft‑w、π₀ 等基于类似视觉骨干的 VLA）；
- 攻击仅需单代理模型梯度访问，无需受害者网络内部信息，契合真实黑盒威胁模型；
- 补丁面积 ≥ 5%（50×50 像素于 224×224 观测）时攻击力显著，面积增至 10% 可进一步将平均成功率压至 20.75%。

**退化域**：
- 若代理与受害者特征空间差异极大（如架构完全不同且无投影器对齐），共享子空间假设可能不成立，迁移性受限；
- 物理场景下 sim‑to‑real 漂移（严重杂波、运动模糊、透视畸变）使攻击未能完全失效——受害者 OpenVLA‑oft‑w 在物理场景下成功率仍为 40.25%，相比仿真场景的 5.75% 有显著回升；
- 补丁面积过小（< 5%）时攻击效果急剧下降，隐蔽性与攻击力之间存在权衡；
- 仅针对视觉模态，未涉及语言或动作模态的联合扰动。

### 4. 局限性与待验证假设

**已识别的局限**：
1. **物理鲁棒性不足**：真实世界中的机械冗余（如柔性夹爪的被动顺应性）和感知噪声对补丁攻击形成缓冲，导致物理场景下策略未完全失效。
2. **补丁尺寸依赖**：攻击强度与补丁面积正相关，更隐蔽的小面积补丁攻击力显著下降，限制了隐蔽部署场景。
3. **模态单一**：仅攻击视觉模态，未利用语言指令或动作序列的联合脆弱性。
4. **代理‑目标对齐假设**：方法依赖代理与受害者共享低维线性子空间，该假设在高度异构模型间可能不成立。

**需手动验证的声明**：
- 文中未提供对完全异构 VLA 架构（如基于不同 LLM 骨干、不同视觉编码器组合）的跨模型迁移实验，共享子空间假设的泛化边界需进一步验证。
- 物理实验仅在有限场景和机器人平台上进行，跨平台（如移动底盘、无人机）和长期任务的攻击有效性尚未验证。

### 5. 开放问题与后续方向

1. **防御机制设计**：如何针对此类通用特征空间攻击构建高效防御？可能的路径包括补丁检测器、鲁棒视觉编码器（对抗训练或特征去噪）、以及基于注意力的异常检测。

2. **多模态扩展**：结合视觉以外的模态（深度、触觉、力反馈）是否会进一步增强攻击的物理鲁棒性？多模态联合扰动可能突破单一视觉模态的退化边界。

3. **跨形态泛化**：攻击能否扩展至更多机器人形态（移动底盘、无人机、双臂协作）及更复杂的长期任务（如“整理房间”等多步骤任务）？

4. **多代理协作攻击**：在多代理协作场景下，单个通用补丁能否同时误导多个 VLA 策略？这涉及共享特征空间在多代理系统中的存在性验证。

5. **攻击‑防御博弈**：若防御方已知 UPA‑RFAS 的攻击机理，能否通过微调视觉投影器或引入特征空间正则化来破坏共享子空间假设，从而阻断迁移通道？

## 原文 PDF

![[paperPDFs/CVPR_2026/When_Robots_Obey_the_Patch_Universal_Transferable_Patch_Attacks_on_Vision_Language_Action_Models.pdf]]
