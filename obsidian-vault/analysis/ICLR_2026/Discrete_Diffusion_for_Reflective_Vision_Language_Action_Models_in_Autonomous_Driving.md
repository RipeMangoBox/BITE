---
title: "Discrete Diffusion for Reflective Vision-Language-Action Models in Autonomous Driving"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Discrete_Diffusion_for_Reflective_Vision_Language_Action_Models_in_Autonomous_Driving.pdf
openreview_forum_id: XJxXSMLDoZ
aliases:
- DDRVLAMAD
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/robotics
core_operator: "将连续驾驶空间离散化为动作码本，利用离散扩散模型的修复能力，在推理时通过目标条件生成与安全引导再生（反射机制）以无梯度方式注入硬性安全约束。"
primary_logic: "离散令牌化使安全约束可通过高效的局部搜索、掩码与修复技术无缝集成到扩散生成过程中，同时扩散模型的双向修复能力能够重建全局连贯轨迹，实现安全且符合物理的规划。"
claims:
- "引入安全引导再生后，DAC指标从95.4提升至99.3，NC从96.9提升至97.7，EP从79.0升至86.9，PDMS从84.8升至91.1。"
- "使用真实环境代理状态时，ReflectDrive†在NAVSIM上达到PDMS 94.7，接近人类水平94.8。"
- "反射机制无需梯度计算，通过离散令牌空间内的局部搜索和修复实现安全约束注入。"
- "离散扩散VLA在大规模开环数据集（10亿样本）上以更低的FDE超越连续扩散基线。"
---

# Discrete Diffusion for Reflective Vision-Language-Action Models in Autonomous Driving

> [!tip] 核心洞察
> 离散令牌化使安全约束可通过高效的局部搜索、掩码与修复技术无缝集成到扩散生成过程中，同时扩散模型的双向修复能力能够重建全局连贯轨迹，实现安全且符合物理的规划。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 基于离散扩散的反思式视觉-语言-动作自动驾驶模型 |
| 英文题名 | Discrete Diffusion for Reflective Vision-Language-Action Models in Autonomous Driving |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=XJxXSMLDoZ) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/robotics |
| Method | ReflectDrive |
| Dataset | NAVSIM (closed-loop), NAVSIM, NAVSIM (oracle upper bound) |

> [!tip] 效果简介
> - NAVSIM (closed-loop) 上，PDMS 为 91.1 (ReflectDrive)，对比 89.1 (AutoVLA)，变化 +2.0。
> - NAVSIM 上，PDMS 为 91.1，对比 83.4 (UniAD)，变化 +7.7。
> - NAVSIM 上，DAC 为 99.3，对比 95.4 (ReflectDrive w/o R.I.)，变化 +3.9。

## 概述

基于模仿学习的端到端自动驾驶规划方法面临一个根本性瓶颈：模型仅从专家示范中学习行为克隆，无法内化碰撞避免、可行驶区域合规等物理安全约束，导致生成轨迹在安全关键场景下容易违反硬性规则。ReflectDrive 的核心洞察在于，将连续驾驶空间离散化为动作码本后，安全约束可通过高效的局部搜索、掩码与修复技术无缝集成到扩散生成过程中，而离散扩散模型的双向修复能力能够重建全局连贯轨迹，实现安全且符合物理的规划。

方法上，ReflectDrive 提出“反射推理”框架，包含两个阶段：目标条件生成（Goal-Conditioned Generation）利用终端航点分布采样多样化的全局轨迹提案；安全引导再生（Safety-Guided Regeneration）则通过无梯度的迭代局部搜索识别不安全航点，寻找安全锚令牌后以修复方式重建轨迹。整个过程无需梯度计算，将外部安全验证与离散令牌操作深度耦合。

在 NAVSIM 闭环基准上，ReflectDrive 达到 PDMS 91.1，较此前最优 VLA 方法 AutoVLA（89.1）提升 2.0 点，较基础端到端规划器 UniAD（83.4）提升 7.7 点。消融实验表明，完整反射推理相比无反射基线 PDMS 提升 6.3 点（84.8→91.1），其中安全引导再生单独将无责碰撞指标 DAC 从 95.4 提升至 99.3。使用真值代理状态作为安全前置时，ReflectDrive† 达到 PDMS 94.7，接近人类水平 94.8。在大规模开环数据集（10 亿样本）上，离散扩散 VLA 以更低的终点位移误差（Min FDE 1.06 vs. 1.44）超越连续扩散基线，验证了离散表示的规模化优势。

当前方法存在若干局限：仅使用单帧三视图输入，无法捕获周围车辆速度信息；可行驶空间受限时轨迹易在边界违规与碰撞避免间振荡；推理延迟较高（约 8.92 秒），缺乏工程优化。后续方向包括融合历史帧信息以建模交互、将规则奖励替换为可学习安全评估模型以降低推理成本，以及在更大规模真实数据上探索离散扩散规划的可扩展性上限。

## 背景与动机

端到端（E2E）自动驾驶规划旨在直接从传感器输入映射到驾驶动作，近年来以模仿学习为核心的范式取得了显著进展。然而，该范式存在一个根本性瓶颈：**基于行为克隆的规划方法无法内化物理安全约束**。具体而言，模型仅从专家示范中学习统计相关性，缺乏对碰撞避免、可行驶区域合规等硬性安全规则的显式建模能力，导致生成的轨迹在安全关键场景下可能违反这些不可妥协的物理约束。

现有方法在应对这一瓶颈时呈现出两条主要路径。一类是以 **UniAD**（Hu et al., 2023）、**PARA-Drive**（Weng et al., 2024）为代表的基座式端到端规划器，它们通过模块化设计将感知、预测、规划耦合，但本质上仍依赖模仿学习，无法在推理时主动修正不安全输出。另一类是增强型规划器，如 **DiffusionDrive**（Liao et al., 2024）和 **GoalFlow**（Xing et al., 2025），它们引入扩散模型以提升轨迹的多样性与质量，但其扩散过程在连续空间中运行，安全引导往往依赖梯度计算，不仅计算开销大，且难以精确注入离散化的硬性安全约束。

与此同时，视觉-语言-动作（VLA）模型在自动驾驶中展现出规模化训练的潜力，如 **AutoVLA**（Zhou et al., 2025）将规划任务统一为序列生成。然而，现有VLA规划方法仍以连续坐标表示轨迹，未能从根本上解决安全约束的内化问题。

上述缺口指向一个核心矛盾：**连续轨迹表示与硬性安全约束的离散化检查之间存在天然的不匹配**。连续空间中的安全边界模糊，局部修正缺乏高效的搜索机制，而梯度引导又引入了额外的计算负担与不稳定性。这促使我们探索一种新的技术路径——将离散扩散模型引入端到端规划，利用离散令牌化空间的结构优势，在推理时以无梯度方式实现安全约束的精确注入与轨迹的全局修复。

## 核心创新

ReflectDrive 的核心创新在于将**连续驾驶空间离散化**与**离散扩散模型的推理时修复能力**相结合，构建了一套无需梯度的安全约束注入机制。其关键设计围绕三个与基线方法的本质差异展开。

### 离散动作码本替代连续坐标表示

传统端到端规划器（如 UniAD、PARA-Drive）直接输出连续浮点坐标，而 ReflectDrive 将二维驾驶空间以网格分辨率 $\Delta g = 0.3\text{m}$ 量化为离散动作码本，每个航点 $(x, y)$ 被独立映射为两个一维令牌。这一变化（**轨迹表示** slot）是后续所有推理机制的基础：离散令牌空间使安全约束可通过高效的局部搜索、掩码与修复技术无缝集成到扩散生成过程中，而连续空间中的约束注入通常依赖梯度引导或后处理修正。

### 离散掩码扩散替代连续扩散过程

现有增强型规划器（如 DiffusionDrive 的伪扩散、GoalFlow 的连续扩散）在连续潜空间中进行去噪，ReflectDrive 则采用基于 MDLM 框架的**离散掩码扩散**（**扩散过程** slot）。模型从预训练扩散语言模型初始化，通过监督微调学习在场景上下文条件下预测被掩码位置的原始令牌。离散扩散的双向修复能力——同时考虑前后文信息重建缺失令牌——是后续安全引导再生的生成基础。

### 无梯度反射推理替代行为克隆与梯度引导

这是 ReflectDrive 最关键的创新（**推理时安全引导** slot）。基线方法在推理时仅执行行为克隆，或依赖基于梯度的引导实现约束满足。ReflectDrive 提出**反射推理**框架，分两阶段以无梯度方式注入硬性安全约束：

1. **目标条件生成**：从终端航点分布中通过 TopK 与非极大值抑制选取 $K$ 个空间多样的目标候选 $\mathcal{G}$，以目标点为条件生成多条全局轨迹提案，捕获多模态驾驶行为。

2. **安全引导再生**：对选出的最优轨迹 $\tau^*$，通过外部安全验证器识别不安全航点，在离散令牌空间的局部曼哈顿邻域 $\mathcal{N}_\delta$ 内搜索最大化局部安全评分的令牌对作为安全锚，再利用扩散模型的修复能力重建全局连贯轨迹。该过程迭代执行，大多数安全违规在 1–3 轮内解决。

这一机制的核心优势在于：安全约束通过离散令牌空间内的局部搜索直接注入，无需梯度计算；同时扩散模型的全局修复能力确保修正后的轨迹保持物理合理性和整体连贯性。消融实验证实，完整反射推理相较无反射基线提升 PDMS 6.3 点（84.8 → 91.1），其中安全引导再生单独贡献 DAC 从 95.4 升至 98.9、NC 从 96.9 升至 98.1，目标条件生成则将 EP 从 79.0 提升至 83.8。

## 整体框架

![[assets/figures/papers/paper_list_l35_https_openreview_net_forum_id_XJxXSMLDoZ/figures/002_Figure_1.jpg]]
*Figure 1: ReflectDrive Framework Overview*

![[assets/figures/papers/paper_list_l35_https_openreview_net_forum_id_XJxXSMLDoZ/figures/003_Figure_2.jpg]]
*Figure 2: Safety-Guided Regeneration Pipeline*

ReflectDrive 的整体架构围绕**离散扩散生成 + 推理时安全反射**两条主线构建，形成“生成—验证—修复”的闭环推理流水线。其核心设计逻辑是：将连续驾驶空间离散化为动作码本，使安全约束可通过高效的局部搜索、掩码与修复技术无缝注入扩散生成过程，同时利用扩散模型的双向修复能力重建全局连贯轨迹。

### 输入输出规范

**输入**：当前帧的三视图图像（前视、左前、右前），不依赖历史帧信息或 LiDAR 点云。

**输出**：未来 $N$ 个时间步的规划航点序列 $\tau = \{(\mathbf{y}_{t,x}, \mathbf{y}_{t,y})\}_{t=1}^N$，每个航点由离散令牌对表示。

### 模块构成与数据流

ReflectDrive 由四个核心模块串联构成，数据流严格遵循“离散化→条件生成→安全验证→局部修复”的单向闭环路径：

#### 1. 轨迹离散化模块 (Trajectory Discretization)

**功能**：将连续二维航点坐标映射为离散令牌序列。

**机制**：以均匀网格分辨率 $\Delta g = 0.3\text{m}$ 构建一维码本，对每个航点的 $x$ 和 $y$ 坐标独立量化，映射到码本中最近邻令牌。该离散化表示使得后续的安全搜索与修复操作可在有限、可枚举的令牌空间内高效执行。

**数据流**：连续轨迹 → 离散令牌序列 $\mathbf{y} = (\mathbf{y}_1, \dots, \mathbf{y}_N)$。

#### 2. 离散扩散 VLA 模型 (Discrete Diffusion VLA)

**功能**：在场景上下文条件下生成或修复轨迹令牌序列。

**机制**：基于预训练的 Diffusion Language Model（You et al., 2025; Nie et al., 2025）初始化，采用掩码扩散框架（MDLM）。训练时，以负对数似然为目标函数：

$$\mathcal{L}(\boldsymbol{\theta}) = \mathbb{E}_{\mathbf{y}, c, s, \mathbf{m}^{(s)}} \left[ - \sum_{i : m_i^{(s)} = 1} \log p_{\boldsymbol{\theta}} \big( \mathbf{y}_i \big| \tilde{\mathbf{y}}^{(s)}, c, s \big) \right]$$

模型学习在给定未掩码令牌 $\tilde{\mathbf{y}}^{(s)}$、扩散时间步 $s$ 和场景上下文 $c$ 的条件下，预测被掩码位置的原始令牌。

**数据流**：场景上下文 $c$ + 带掩码的令牌序列 → 预测的完整令牌序列。

#### 3. 目标条件生成模块 (Goal-Conditioned Generation)

**功能**：生成多样化的全局轨迹提案，捕获多模态驾驶行为。

**机制**：推理时从模型预测的终端航点分布 $p_{\theta}(\mathbf{y}_N \mid c, s)$ 中，通过 TopK 和非极大值抑制（NMS）筛选 $K$ 个空间多样的目标候选：

$$\mathcal{G} = \mathbf{NMS}\left(\mathrm{TopK}_{K'}\left(p_{\theta}(\mathbf{y}_N \mid c, s)\right), d_{\mathrm{NMS}}, K\right)$$

以每个目标点为条件生成完整轨迹，并通过全局评分函数 $S(\tau)$ 选取最优轨迹：

$$\tau^{*} = \operatorname*{argmax}_{\tau_k, k=1,\dots,K} S(\tau_k)$$

其中 $S(\tau)$ 由硬安全合规项 $H(\tau)$ 和性能质量项 $Q(\tau)$ 构成：$H(\tau) = m_{\mathrm{NC}}(\tau) \cdot m_{\mathrm{DAC}}(\tau)$ 确保任何无责碰撞或可行驶区域违规将直接归零评分；$Q(\tau)$ 为进度、碰撞时距、舒适度的归一化加权和。

**数据流**：扩散生成分布 → $K$ 个目标候选 → $K$ 条完整轨迹 → 最高分轨迹 $\tau^*$。

#### 4. 安全引导再生模块 (Safety-Guided Regeneration)

**功能**：迭代识别不安全航点，通过局部搜索寻找安全锚并修复轨迹。

**机制**：该模块构成一个**无梯度**的“生成模型↔安全预言机”对话循环：
- **安全验证**：外部安全预言机检测 $\tau^*$ 中违反碰撞避免或可行驶区域约束的航点。
- **局部安全锚搜索**：对每个不安全航点 $\mathbf{y}_t$，在其曼哈顿邻域 $\mathcal{N}_{\delta}$（$\delta \leq 10$）内搜索最大化局部安全评分的令牌对：

$$(\mathbf{y}_{t,x}', \mathbf{y}_{t,y}') = \underset{(a_x, a_y) \in \mathcal{N}_{\delta}(\mathbf{y}_{t,x}, \mathbf{y}_{t,y})}{\arg\max} S_{\mathrm{local}}(a_x, a_y)$$

- **轨迹修复**：将安全锚令牌作为条件，利用扩散模型的掩码修复（inpainting）能力重建全局连贯轨迹。

该过程迭代执行，论文报告大多数安全违规在 1–3 轮反射内得到解决。

**数据流**：$\tau^*$ → 安全验证 → 不安全航点集合 → 局部搜索 → 安全锚令牌 → 掩码修复 → 更新轨迹 → 循环直至收敛。

### 推理流水线总览

完整的推理流程为：**离散化场景编码 → 目标条件生成 $K$ 条提案 → 全局评分选优 → 安全引导再生迭代优化 → 输出安全轨迹**。两个推理阶段形成互补：目标条件生成主要提升自车进度（EP），安全引导再生则显著改善碰撞避免（DAC）、无责碰撞（NC）和碰撞时距（TTC）等安全指标。

## 核心模块与公式推导

### 4.1 轨迹离散化与离散扩散VLA

ReflectDrive的核心技术路线是将连续驾驶空间转化为离散令牌空间，从而利用离散扩散模型的掩码-修复能力实现安全约束的注入。该方法包含两个基础模块：

**轨迹离散化模块 (Trajectory Discretization)**。将连续的二维航点坐标 $(x, y)$ 映射为离散令牌序列。具体而言，对 $x$ 和 $y$ 坐标分别建立独立的一维码本，以网格分辨率 $\Delta g = 0.3\text{m}$ 进行均匀量化，每个连续值被映射到最近邻的离散令牌。这一离散化策略使轨迹成为可被语言模型直接处理的令牌序列，同时保留了空间结构的可操作性（Section 4.1）。

**离散扩散VLA模型 (Discrete Diffusion VLA)**。模型从预训练的扩散语言模型（Diffusion Language Model）初始化，以场景上下文 $c$ 为条件，在自动驾驶规划数据集上进行监督微调。其核心学习任务遵循掩码扩散框架（MDLM）：在前向过程中按时间步 $s$ 随机掩码部分令牌，模型 $p_{\boldsymbol{\theta}}$ 学习从被掩码版本 $\tilde{\mathbf{y}}^{(s)}$ 中预测原始令牌。

训练目标为负对数似然损失：

$$
\mathcal{L}(\boldsymbol{\theta}) = \mathbb{E}_{\mathbf{y}, c, s, \mathbf{m}^{(s)}} \left[ - \sum_{i : m_i^{(s)} = 1} \log p_{\boldsymbol{\theta}} \big( \mathbf{y}_i \big| \tilde{\mathbf{y}}^{(s)}, c, s \big) \right] \tag{1}
$$

其中 $\mathbf{m}^{(s)}$ 为时间步 $s$ 的掩码指示向量（$m_i^{(s)}=1$ 表示位置 $i$ 被掩码），模型仅对被掩码位置的原始令牌进行预测。该目标使模型获得双向上下文建模能力，为后续推理时的修复（inpainting）操作奠定基础（Section 3.2, 4.1）。

### 4.2 反射推理机制

反射推理（Reflective Inference）是ReflectDrive的核心创新，包含两个阶段：目标条件生成与安全引导再生。整个过程无需梯度计算，完全在离散令牌空间内通过局部搜索和条件生成实现。

**阶段一：目标条件生成 (Goal-Conditioned Generation)**。首先从模型的终端航点分布中采样多样化的目标候选。利用TopK和非极大值抑制（NMS）选取 $K$ 个空间多样的目标点：

$$
\mathcal{G} = \mathbf{NMS}\left(\mathrm{TopK}_{K'}\left(p_{\theta}(\mathbf{y}_N \mid c, s)\right), d_{\mathrm{NMS}}, K\right) \tag{2}
$$

其中 $\mathbf{y}_N$ 为轨迹末端航点的令牌表示，$d_{\mathrm{NMS}}$ 控制候选目标之间的最小空间距离。以每个目标点为条件，通过离散扩散的修复过程生成完整轨迹 $\tau_k$，最终选择全局评分最高的方案：

$$
\tau^{*} = \operatorname*{argmax}_{\tau_k, k=1,\dots,K} S(\tau_k) \tag{3}
$$

**阶段二：安全引导再生 (Safety-Guided Regeneration)**。对阶段一选出的最优轨迹 $\tau^{*}$，利用外部安全评估器（safety oracle）逐航点检测违规（如碰撞、越界）。对于每个不安全航点 $(\mathbf{y}_{t,x}, \mathbf{y}_{t,y})$，在其局部曼哈顿邻域 $\mathcal{N}_{\delta}$（$\delta \leq 10$）内搜索最大化局部安全评分的替代令牌对：

$$
(\mathbf{y}_{t,x}', \mathbf{y}_{t,y}') = \underset{(a_x, a_y) \in \mathcal{N}_{\delta}(\mathbf{y}_{t,x}, \mathbf{y}_{t,y})}{\arg\max} S_{\mathrm{local}}(a_x, a_y) \tag{4}
$$

找到的安全令牌作为“锚点”，模型以修复方式重新生成周围航点，从而在保持全局轨迹连贯性的同时消除局部违规。该过程迭代执行，实验表明大多数安全违规在1-3次反射迭代内即可解决（Section 4.2）。

### 4.3 评分函数设计

反射机制依赖评分函数 $S(\tau)$ 评估轨迹质量，其设计包含硬安全合规项与性能质量项（附录E）。

**硬安全合规项**确保任何关键安全规则违反将导致轨迹被拒绝：

$$
H(\tau) = m_{\mathrm{NC}}(\tau) \cdot m_{\mathrm{DAC}}(\tau) \tag{5}
$$

其中 $m_{\mathrm{NC}}$ 为无责碰撞指标，$m_{\mathrm{DAC}}$ 为可行驶区域合规指标。两者均为二元值（合规为1，违规为0），乘积形式保证了任一违规即归零的硬约束特性。

**性能质量项**在通过安全检查后衡量轨迹的综合质量：

$$
Q(\tau) = \frac{w_{\mathrm{EP}} \cdot m_{\mathrm{EP}}(\tau) + w_{\mathrm{TTC}} \cdot m_{\mathrm{TTC}}(\tau) + w_{\mathrm{C}} \cdot m_{\mathrm{C}}(\tau)}{w_{\mathrm{EP}} + w_{\mathrm{TTC}} + w_{\mathrm{C}}} \tag{6}
$$

其中 $m_{\mathrm{EP}}$、$m_{\mathrm{TTC}}$、$m_{\mathrm{C}}$ 分别衡量自车进度、碰撞时距和舒适度，$w$ 为对应权重。消融实验表明，评分函数权重对最终性能影响较小（PDMS在90.9-91.2范围内波动），方法对超参数具有良好鲁棒性（Table 7）。

### 关键设计决策

离散化粒度 $\Delta g$ 是影响性能的核心超参数。Table 6显示，$\Delta g = 0.2\text{m}$ 时PDMS达到最优91.3，但默认设置 $\Delta g = 0.3\text{m}$ 在精度（PDMS 91.1）与码本大小之间取得了平衡——过细的离散化（0.1m）导致码本过大、训练困难，过粗（0.4m以上）则损失空间精度。局部搜索的邻域范围 $\delta \leq 10$ 保证了搜索效率，使无梯度反射推理的计算开销可控。

## 实验与分析

### 核心实验结果

ReflectDrive在NAVSIM闭环基准上取得PDMS 91.1，显著超越同属VLA范式的AutoVLA（89.1）以及基础端到端规划器UniAD（83.4）。在仅使用三视图相机输入的条件下，该方法已逼近使用LiDAR的增强型方法Hydra-MDP（91.0）和GoalFlow（91.5）。当使用真值代理状态作为安全前置时，ReflectDrive†达到PDMS 94.7，与人类基线94.8仅差0.1点，表明反射机制的上限接近人类驾驶水平（Table 1）。

![[assets/figures/papers/paper_list_l35_https_openreview_net_forum_id_XJxXSMLDoZ/figures/004_Table_1.jpg]]
*Table 1: NAVSIM Closed-Loop Results. Methods are grouped by their core architectural paradigm. The † symbol denotes our method using a privileged ground-truth oracle for reflection, serving as an analytical upper bound. Best result per column is in bold (higher is better)*

反射推理带来的安全增益尤为突出：相比无反射推理基线（ReflectDrive w/o R.I.），完整模型将DAC从95.4提升至99.3（+3.9），NC从96.9提升至97.7（+0.8），TTC从92.7提升至94.0（+1.3）。EP从79.0大幅提升至86.9（+7.9），说明安全引导再生不仅增强安全性，还通过修复不安全航点间接提升了通行效率（Table 1）。

### 反射推理消融

Table 2系统解耦了反射推理两阶段的贡献。无任何反射的基线模型PDMS为84.8。单独引入目标条件生成（G.C.G.）将EP从79.0提升至83.8，PDMS升至87.4，但NC和TTC略有下降——更多样的目标提案增加了探索能力，却也引入了不安全候选的风险。单独引入安全引导再生（S.G.R.）则将DAC从95.4提升至98.9，NC从96.9升至98.1，PDMS达90.8，证明局部搜索与修复机制能有效纠正安全违规。两阶段联合使用取得最优PDMS 91.1，验证了二者的互补性：目标条件生成提供多样化全局提案，安全引导再生在局部进行安全精炼。

![[assets/figures/papers/paper_list_l35_https_openreview_net_forum_id_XJxXSMLDoZ/figures/010_Table_2.jpg]]
*Table 2: Ablation for Reflective Inference. The ablation study results of goal-conditioned generation and safety-guided regeneration to demonstrate the effectiveness of reflective inference*

### 离散化粒度与超参数敏感性

离散化粒度Δg对性能有显著影响（Table 6）。Δg=0.2m时PDMS最优（91.3），但码本大小|A|随之增大，增加计算开销。默认设置Δg=0.3m在精度与效率间取得平衡（PDMS 91.1）。过细的离散化（Δg=0.1m）反而导致性能下降（PDMS 90.7），可能因码本过大增加了学习难度；过粗的离散化（Δg=0.4m）则因分辨率不足而损害精度（PDMS 90.4）。

![[assets/figures/papers/paper_list_l35_https_openreview_net_forum_id_XJxXSMLDoZ/figures/016_Table_6.jpg]]
*Table 6: Ablation on Discretization Granularity ( $\Delta$ g )*

评分函数权重对最终性能影响较小（Table 7）：在w_EP、w_TTC、w_C的不同组合下，PDMS在90.9至91.2范围内波动，表明方法对超参数设置具有鲁棒性。TTC阈值从0.5s变化至1.5s时，PDMS波动幅度同样有限。

### 推理效率与扩展性

ReflectDrive的推理延迟分解（Table 5）显示，单NVIDIA H20上总延迟约8.92秒。其中目标条件生成阶段占6.82秒（目标提案0.62秒，轨迹修复6.06秒，评分筛选0.15秒），安全引导再生阶段占2.10秒。当前为研究原型，缺乏KV缓存等工程优化，延迟仍有较大压缩空间。

在大规模开环评估中（Table 9，10亿样本内部数据集），离散扩散VLA以更低的FDE超越连续扩散基线，验证了离散表示在大规模训练中的扩展性优势。

### 定性分析与失败模式

Figure 3展示了安全引导再生的迭代优化过程。在大角度转弯场景中，初始轨迹存在越界风险，经过S.G.R.逐步迭代后收敛至安全可行区域；在强交互场景中，初始轨迹可能与其他车辆或行人发生碰撞，S.G.R.通过迭代优化使轨迹学会避让或减速让行。

![[assets/figures/papers/paper_list_l35_https_openreview_net_forum_id_XJxXSMLDoZ/figures/006_Figure_3.jpg]]
*Figure 3: Safety-Guided Regeneration (S.G.R) Visualization. The first row illustrates three scenarios where large-angle turns are prone to boundary violations. The initial trajectories (lightest color) carry the risk of exceeding the boundaries. Using S.G.R, the trajectory is gradually optimized toward the safe region (with its color darkening progressively), ultimately resulting in a feasible trajectory. The second row depicts three scenarios involving intense interactions. Initial trajectories may pose collision risks with other vehicles or pedestrians. Through the iterative optimization of S.G.R., the trajectories learn to avoid conflicts or decelerate to yield, achieving much higher safety*

Figure 6揭示了三种典型失败模式：**边界振荡**——在可行驶空间受限场景下，轨迹在边界违规与碰撞避免之间反复振荡，需在奖励函数中引入中心线距离等约束；**目标点选择偏差**——部分场景下目标候选选择不佳，限制了搜索范围内的修正能力；**导航偏差**——奖励函数未包含导航正确性，可能导致错误修正方向。这些失败模式指向了未来改进方向：融合历史帧信息以建模交互动态、引入可学习的安全评估模型替代规则奖励、优化搜索策略以彻底超越人类驾驶性能。

## 方法谱系与知识库定位

### 1. 核心瓶颈与设计动机

当前基于模仿学习的端到端自动驾驶规划方法面临一个根本性瓶颈：**无法内化物理安全约束**（如碰撞避免、可行驶区域合规）。行为克隆范式下，模型仅学习从感知到轨迹的统计映射，导致生成的轨迹可能违反关键安全规则——这一问题在NAVSIM闭环评估中尤为突出，无约束模型在DAC（可行驶区域合规）和NC（无责碰撞）等安全指标上存在显著短板。

ReflectDrive的核心洞察在于：**将连续驾驶空间离散化为动作码本，使安全约束可通过高效的局部搜索、掩码与修复技术无缝集成到扩散生成过程中**。离散扩散模型的双向修复能力能够重建全局连贯轨迹，实现安全且符合物理的规划。

### 2. 在方法谱系中的定位

ReflectDrive位于端到端自动驾驶规划的**VLA（视觉-语言-动作）范式**与**扩散生成方法**的交汇点。下表梳理其与相关工作的关键差异：

| 方法范式 | 代表工作 | 轨迹表示 | 扩散过程 | 推理时安全引导 |
|---------|---------|---------|---------|-------------|
| Base E2E Planner | **UniAD** (Hu et al., 2023) | 连续坐标 | 无扩散 | 无 |
| Base E2E Planner | **PARA-Drive** (Weng et al., 2024) | 连续坐标 | 无扩散 | 无 |
| Base E2E Planner | **Transfuser** (Chitta et al., 2023) | 连续坐标 | 无扩散 | 无 |
| Augmented E2E Planner | **Hydra-MDP** (Li et al., 2024) | 连续坐标 | 无扩散 | 无（仅行为克隆） |
| Augmented E2E Planner | **DiffusionDrive** (Liao et al., 2024) | 连续坐标 | 连续伪扩散 | 无 |
| Augmented E2E Planner | **GoalFlow** (Xing et al., 2025) | 连续坐标 | 连续扩散 | 无 |
| VLA Planner | **AutoVLA** (Zhou et al., 2025) | 连续坐标 | 无扩散 | 无 |
| **VLA Planner (Ours)** | **ReflectDrive** | **离散动作码本** (Δg=0.3m) | **离散掩码扩散** (MDLM框架) | **无梯度反射推理** |

**关键差异总结**：

- **离散化表示**：ReflectDrive将连续航点映射为离散令牌序列，使安全约束验证转化为离散令牌空间内的局部搜索问题，无需梯度计算。这一设计从根本上区别于DiffusionDrive的连续伪扩散和GoalFlow的连续扩散。

- **反射推理机制**：现有方法在推理时缺乏显式的安全约束注入。ReflectDrive提出两阶段反射框架——目标条件生成（捕获多模态行为）+ 安全引导再生（迭代识别不安全航点，通过局部搜索寻找安全锚并修复轨迹），以无梯度方式实现硬性安全约束的注入。

- **模型初始化**：ReflectDrive的离散扩散模块从预训练扩散语言模型初始化，利用大规模语言预训练的先验知识，区别于从零训练的连续扩散规划器。

### 3. 适用边界

**输入模态边界**：ReflectDrive当前仅使用三视图相机输入，未融合LiDAR或历史帧信息。这一设计使其在传感器配置上与Hydra-MDP、DiffusionDrive、GoalFlow等使用LiDAR的增强型方法存在信息不对称——后者可获取更精确的3D几何信息，而ReflectDrive需要在纯视觉条件下推断空间关系。

**安全约束的硬性边界**：反射机制通过硬安全合规项 $H(\tau) = m_{\mathrm{NC}}(\tau) \cdot m_{\mathrm{DAC}}(\tau)$ 实现约束注入，任何规则违反将导致该项归零。这种硬性约束在多数场景下有效，但在可行驶空间受限场景下可能引发**边界振荡**——轨迹在边界违规与碰撞避免之间反复跳变，难以收敛到同时满足所有约束的解。

**目标点选择的依赖**：反射机制的有效性依赖于目标条件生成阶段提供的目标候选质量。当目标点选择出现偏差时（如导航方向错误），安全引导再生仅能在局部邻域内修正，无法纠正全局导航偏差。

**计算延迟边界**：当前研究原型的推理延迟较高（平均约8.92秒，单NVIDIA H20），其中目标条件生成占6.82秒，安全引导再生占2.10秒。缺乏KV缓存等工程优化，使其暂时无法满足实时部署需求。

### 4. 已知局限与失败模式

根据论文提供的失败案例分析（Figure 6），ReflectDrive存在三类典型失败模式：

1. **边界振荡**：在可行驶空间受限场景下，轨迹在边界违规与碰撞避免之间反复振荡。论文指出需要在奖励函数中增加中心线距离等项来缓解此问题。

2. **目标点选择偏差**：目标候选筛选（TopK + NMS）在某些场景下未能覆盖正确的导航目标，导致后续再生无法修正到正确方向。

3. **导航偏差**：即使轨迹在安全约束下可行，其导航方向可能与预期路线偏离——当前评分函数未包含导航正确性项。

此外，仅使用当前帧图像作为输入，模型无法捕获周围车辆的速度信息，限制了交互建模能力。在密集交互场景（如无保护左转、行人横穿）中，这一限制可能导致对动态障碍物意图的误判。

### 5. 开放问题

1. **历史信息融合**：如何高效融合历史帧信息以建模车辆交互与速度估计，同时不显著增加推理延迟？这对提升密集交互场景下的安全性至关重要。

2. **可学习安全评估**：当前反射机制依赖基于规则的安全评分函数（硬安全合规项 + 性能质量项）。能否将基于规则的奖励替换为可学习的安全评估模型，并内化反射过程以减少推理成本？这可能是将反射机制从研究原型推向实用系统的关键一步。

3. **超越人类性能的路径**：ReflectDrive†在使用真值代理状态时达到PDMS 94.7，接近人类水平94.8。如何进一步优化局部搜索与修复策略以彻底超越人类驾驶性能？论文指出推理扩展（inference scaling）的上限可能取决于所采用的策略，暗示存在进一步优化的空间。

4. **离散扩散的可扩展性上限**：论文在10亿样本的大规模开环数据集上验证了离散扩散VLA以更低FDE超越连续扩散基线（Table 9）。但在更大规模真实数据上，离散扩散规划的可扩展性上限如何？码本大小、离散化粒度与模型容量之间的关系需要更系统的研究。

5. **多模态感知融合**：当前纯视觉输入在3D几何理解上存在固有局限。如何在保持反射机制无梯度优势的前提下，有效融合LiDAR等多模态信息，是一个尚未探索的方向。

---

**证据强度说明**：上述分析中，方法定位与核心差异基于Table 1的系统对比（置信度0.95），失败模式基于Figure 6的定性分析（置信度0.85-0.90），开放问题基于论文讨论与消融实验的推断（置信度0.75-0.85）。计算延迟数据来自Table 5（置信度0.95）。

## 原文 PDF

![[paperPDFs/ICLR_2026/Discrete_Diffusion_for_Reflective_Vision_Language_Action_Models_in_Autonomous_Driving.pdf]]
