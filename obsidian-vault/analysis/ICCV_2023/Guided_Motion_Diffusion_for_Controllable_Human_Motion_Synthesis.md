---
title: "Guided Motion Diffusion for Controllable Human Motion Synthesis"
type: paper
paper_level: A
venue: ICCV
year: 2023
pdf_ref: paperPDFs/ICCV_2023/Guided_Motion_Diffusion_for_Controllable_Human_Motion_Synthesis.pdf
aliases:
- GMDG
- GMDCHMS
tags:
- ICCV_2023
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/robotics
core_operator: "通过强调投影（Emphasis projection）利用随机矩阵放大轨迹部分在运动表示中的方差比重，以及密集信号传播（Dense signal propagation）利用扩散模型自身的去噪网络将稀疏关键帧梯度反向传播到所有帧，从而强制模型关注空间引导。"
primary_logic: "将空间引导问题转化为表示学习和引导信号密集化问题：通过线性随机投影重分配运动特征的方差分布，使空间信息与局部姿态的梯度耦合；并将扩散模型的去噪网络视为运动先验，通过反向传播将稀疏位置约束扩散为稠密引导，无需额外训练。"
claims:
- "强调投影（c=10）使运动在轨迹条件下的脚滑率大幅降低，且 FID 显著改善，优于仅扩大损失权重的方案。"
- "密集信号传播是模型能遵循稀疏关键帧定位的必要条件，缺乏该机制时扩散模型完全忽略目标位置。"
- "采用 ε 参数化的轨迹 DPM 可防止在去噪后期（t→0）模型偏置反向覆盖引导信号，而 x0 模型则会产生轨迹“收缩”行为。"
- "HumanML3D 上 FID (text-to-motion) = 0.212"
---

# Guided Motion Diffusion for Controllable Human Motion Synthesis

> [!tip] 核心洞察
> 将空间引导问题转化为表示学习和引导信号密集化问题：通过线性随机投影重分配运动特征的方差分布，使空间信息与局部姿态的梯度耦合；并将扩散模型的去噪网络视为运动先验，通过反向传播将稀疏位置约束扩散为稠密引导，无需额外训练。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 可控人体运动合成的引导运动扩散模型 |
| 英文题名 | Guided Motion Diffusion for Controllable Human Motion Synthesis |
| 会议/期刊 | ICCV 2023 |
| Links | [paper](https://arxiv.org/abs/2305.12577); [Project](https://korrawe.github.io/gmd-project/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/robotics |
| Method | Guided Motion Diffusion (GMD) |
| Dataset | HumanML3D, HumanML3D (keyframe-conditioned) |

> [!tip] 效果简介
> - HumanML3D 上，FID (text-to-motion) 为 0.212，对比 0.556 (MDM)，变化 -0.344。
> - HumanML3D (keyframe-conditioned) 上，Location error (τ=100) 为 两阶段轨迹模型使位置误差相比单阶段模型降低超过 50%，对比 单阶段模型 (τ=100)，变化 减少 >50%。

## 概述

扩散模型在文本到人体运动生成上取得了显著进展，然而当引入空间约束（如轨迹、关键帧位置、障碍物规避）时，现有方法普遍面临一个核心瓶颈：人体运动表示中全局空间信息仅占 4 维（骨盆旋转与地面位置），而局部姿态占据 259 维，这种极端的维度不平衡使扩散模型倾向于将稀疏的空间引导信号当作噪声丢弃，导致生成的运动出现脚滑、轨迹偏离等不一致现象。

针对这一问题，**Guided Motion Diffusion (GMD)** 提出了两个关键机制。**强调投影（Emphasis Projection）** 通过线性随机投影重分配运动特征的方差分布，迫使模型在训练和推理中将空间信息与局部姿态的梯度耦合，从而增强轨迹与运动之间的连贯性。**密集信号传播（Dense Signal Propagation）** 则利用扩散模型自身的去噪网络作为运动先验，将稀疏关键帧的梯度反向传播到整个序列，使引导信号覆盖所有帧，防止模型忽略目标位置约束。

GMD 采用两阶段生成管道：第一阶段使用 ε 参数化的轨迹扩散模型生成满足空间目标的全局轨迹；第二阶段以该轨迹和文本为条件，通过集成强调投影的 x0 参数化运动扩散模型合成完整运动序列。在 HumanML3D 数据集上，GMD 的文本到动作生成 FID 达到 0.212，相比基线 MDM 的 0.556 显著降低；在关键帧条件任务中，两阶段轨迹模型使位置误差相比单阶段模型降低超过 50%。消融实验进一步证实，强调投影（c=10）使脚滑率降至 0.128，而移除密集信号传播后模型完全忽略关键帧目标——这两项机制是 GMD 实现可控生成的必要条件。

## 背景与动机

### 问题定义

人体运动合成旨在根据给定的条件信号生成自然、多样的人体动作序列。近年来，扩散概率模型（Diffusion Probabilistic Models, DPMs）在文本到动作生成任务上取得了显著进展，其中 **MDM**（Motion Diffusion Model）作为代表性工作，通过 Transformer 架构实现了高质量的文本条件运动生成。然而，纯文本条件难以精确控制运动的空间属性——例如“走到门口然后坐下”这样的指令，文本可以描述意图，却无法指定行走路径、关键位置或与场景障碍物的空间关系。

空间可控运动生成的核心挑战在于：**如何在保持运动自然度和文本语义一致性的同时，使生成的运动精确遵循用户指定的空间约束**，如全局轨迹、关键帧位置和障碍物规避。

### 瓶颈分析：稀疏信号被扩散模型忽略

现有方法在空间控制上面临两个紧密关联的技术瓶颈，其根源在于人体运动表示的内在结构不平衡。

**表示层面的信号稀疏性。** 标准人体运动表示通常包含约 263 维特征，其中描述全局空间信息（骨盆旋转与地面位置）的维度仅占 4 维，其余 259 维描述局部关节姿态。这种极端的维度不平衡导致两个后果：

1. **训练阶段**：扩散模型倾向于将空间维度的变化视为噪声，因为它们在整体特征方差中的贡献微乎其微。具体而言，轨迹部分（骨盆旋转和 x/z 位置）的累积方差仅为 3，而整个运动表示的方差约为 263，轨迹的相对重要性不足 1.2%。
2. **推理阶段**：当通过分类器引导或插补（imputation）注入空间约束时，梯度信号仅作用于少数几个维度，模型缺乏动力去调整局部姿态以配合全局空间目标，导致运动不连贯——典型表现为脚滑（foot skating）和轨迹偏离。

**时间层面的信号稀疏性。** 在关键帧条件任务中，用户仅在少数时间步指定目标位置（例如 5 个关键帧），引导信号在时间轴上也极度稀疏。标准的分类器引导方法将梯度直接施加于对应帧的对应维度，但这些稀疏梯度在扩散模型的去噪过程中被大量其他帧的更新所淹没，模型最终完全忽略目标位置约束。

Figure 3 直观展示了这一问题：在标准方法下，引导仅更新运动表示中的少数值；而 GMD 通过强调投影使每帧的所有特征都接收引导梯度，通过密集信号传播使所有帧都受到关键帧约束的影响。

### 现有方法的缺口

已有的可控生成方法大致分为两类，但均未有效解决上述瓶颈：

- **插补方法**（如通用 inpainting）：在每次去噪步骤后用目标观测替换生成样本的对应区域。这种方法提供硬约束，但仅作用于被替换的维度，无法促使模型调整其余特征以保持运动连贯性。
- **分类器引导方法**：通过目标函数的梯度引导生成过程。但在稀疏信号场景下，梯度过于局部化，容易被扩散模型忽略。

此外，**轨迹 DPM 的参数化选择**也对可控性有深远影响。以 $\mathbf{x}_0$ 为预测目标的模型在去噪后期（$t \to 0$）会表现出对引导信号的“抵抗”——模型自身的先验偏置反向覆盖引导信号，导致生成的轨迹向模型均值“收缩”。Figure 4 展示了这一现象：$\mathbf{x}_0$ 模型的干净轨迹在去噪后期出现明显的收缩行为，而 $\epsilon$ 模型则稳定地遵循引导。

### 本文动机

基于以上分析，本文提出 **Guided Motion Diffusion (GMD)**，核心动机是将空间引导问题重新定义为两个子问题：

1. **表示学习问题**：如何重新分配运动特征的方差分布，使空间信息与局部姿态在梯度传播中有效耦合？
2. **引导信号密集化问题**：如何将稀疏的空间约束（时间稀疏的关键帧、维度稀疏的轨迹）转化为扩散模型能够感知和响应的稠密信号？

GMD 通过两个核心机制回应上述动机：**强调投影（Emphasis Projection）** 利用线性随机投影放大轨迹部分在运动表示中的方差比重，强制模型在训练和推理中关注空间信息；**密集信号传播（Dense Signal Propagation）** 将扩散模型的去噪网络视为运动先验，通过反向传播将稀疏关键帧梯度扩散为覆盖整个序列的稠密引导，无需额外训练。两阶段管道（轨迹 DPM + 运动 DPM）进一步将空间规划与姿态生成解耦，轨迹 DPM 采用 $\epsilon$ 参数化以消除引导后期的收缩偏置，运动 DPM 集成强调投影和掩码分类器引导以生成连贯的全身运动。

## 核心创新

GMD 的核心创新在于将空间引导问题重新定义为**表示学习**与**引导信号密集化**问题，而非简单地堆叠条件模块。其相对于基线（MDM，基于 Transformer 的文本到动作扩散模型）的关键改变可归纳为四个 changed slots，这些改变共同解决了扩散模型在接收稀疏空间约束时将其视为噪声而忽略的根本瓶颈。

### 1. 强调投影：重分配运动特征的方差结构

人体运动表示中，全局空间信息（骨盆旋转与地面位置）仅占 4 维，而局部姿态占 259 维。这种维度不对称导致扩散模型在训练和推理中将空间约束信号当作噪声丢弃，产生脚滑、轨迹偏离等不一致现象。

GMD 提出**强调投影**（Emphasis Projection），核心操作是引入一个随机矩阵 $A$ 对运动表示进行线性投影：

$$x^{\text{proj}} = A x$$

该投影的实质是**重分配运动特征的方差分布**，使轨迹部分的相对方差被放大。具体而言，$A$ 由对角缩放矩阵 $B$ 和正交矩阵 $A'$ 构成：$B$ 将轨迹维度的方差放大 $c$ 倍（$c$ 为超参数），$A'$ 则通过随机旋转将这种方差增强传播到所有维度，实现空间信息与局部姿态的**梯度耦合**。在投影空间中完成插补和去噪后，再通过 $A^{-1}$ 解投影回原始表示空间。

消融实验提供了决定性证据（Table 2）：$c=10$ 时，脚滑率降至 0.128，FID 显著改善；而仅扩大损失权重的方案无法达到同等连贯性。这表明**表示层面的方差重分配比损失层面的加权更根本地改变了模型对空间信号的响应模式**。

### 2. 密集信号传播：将稀疏引导转化为稠密梯度

时间维度的稀疏引导（如仅给定少数关键帧位置）面临类似困境：扩散模型在去噪过程中仅更新与关键帧直接对应的少数帧，其余帧不受引导影响，导致模型完全忽略目标位置。

GMD 的**密集信号传播**（Dense Signal Propagation）利用扩散模型自身的去噪网络 $f(x_t)$ 作为运动先验，将稀疏关键帧梯度反向传播到所有帧：

$$\nabla_{x_t} \log p(G_x(X_t)=0|x_t) \approx -\nabla_{x_t} G_z(P_x^z f(x_t))$$

其因果机制是：去噪网络 $f$ 在训练过程中学到了帧间运动的自然关联，当稀疏位置约束的梯度通过 $f$ 反向传播时，这些梯度会沿学到的运动依赖关系自动扩散到非关键帧，产生**稠密的分类器引导信号**。GMD 进一步通过掩码机制将插补（硬约束，仅在已知位置施加）与分类器引导（软约束，在其余位置施加）结合：

$$\mu_t^{\text{proj}} = \tilde{\mu}_t^{\text{proj}} + A (1 - M_z^x) \odot \Delta_\mu$$

其中 $\Delta_\mu = -s \Sigma_t A^{-1} \nabla_{x_t^{\text{proj}}} G_z(P_x^z A^{-1} f(x_t^{\text{proj}}))$。

决定性证据来自 Figure 6 和 Table 3：去除密集信号传播后，模型在关键帧任务中完全忽略目标位置；而两阶段轨迹模型（先以密集信号传播生成满足关键帧的轨迹，再以该轨迹为条件生成完整运动）使位置误差相比单阶段模型降低超过 50%。

### 3. ε 参数化轨迹 DPM：消除引导后期的轨迹收缩

MDM 原始架构预测 $x_0$，但在分类器引导下，$x_0$ 参数化存在根本问题：去噪后期（$t \to 0$），模型对采样均值的贡献占主导地位，产生强烈的**偏置反向覆盖引导信号**，表现为轨迹“收缩”行为（Figure 4）。

GMD 将轨迹 DPM 的参数化目标从 $x_0$ 改为 $\epsilon$ 预测。其因果逻辑是：在 Cosine $\beta$ 调度下，$\epsilon$ 模型对采样均值的影响在 $t=T$ 时最大，与分类器引导在早期需要强引导的直觉一致；而 $x_0$ 模型的影响在 $t \to 0$ 时急剧上升，与引导信号产生对抗。Figure 4 提供了决定性视觉证据：$\epsilon$ 模型消除了轨迹收缩现象，引导信号在全程保持有效。

### 4. 绝对根表示与 1D UNet 架构

GMD 将运动根表示从相对表示（逐帧增量）改为绝对表示（全局坐标）。消融实验（Table B.1）显示，这一改变使 GMD 的 FID 从 0.305 降至 0.212，尽管多样性轻微下降；值得注意的是，该改变对 MDM 基线反而有负面影响，说明绝对表示与强调投影、密集信号传播等机制存在**协同效应**——绝对坐标使空间插补和优化更直接，而这些引导机制恰好能补偿绝对表示可能引入的累积误差。

此外，GMD 将网络架构从 Transformer 替换为 1D UNet with AdaGN（Table D.1, Figure D.1），后者更适合 $\epsilon$ 预测和高维特征处理，且通过 Adaptive Group Normalization 将时间步和文本条件注入各层。

### 创新间的因果耦合关系

上述四个 changed slots 并非独立改进，而是构成一个**因果链条**：绝对根表示使空间约束可直接作用于全局坐标；强调投影确保这些约束在梯度更新中获得足够的方差权重；密集信号传播将稀疏约束沿时间轴扩散；ε 参数化则保证引导信号在去噪全程不被模型偏置覆盖。缺失任一环节，整个空间引导机制都会失效——这正是 MDM 等基线在空间约束任务上表现不佳的根本原因。

## 整体框架

![[assets/figures/papers/paper_list_l30_https_arxiv_org_abs_2305_12577/figures/007_Figure_5.jpg]]
*Figure 5: Generated motion, conditioned a given trajectory and text “walking forward”. MDM [54] exhibits motion incoherence where the model disregards the trajectory and generates an inconsistent motion. Our method, improved by emphasis projection, deals effectively with the conditioning*

![[assets/figures/papers/paper_list_l30_https_arxiv_org_abs_2305_12577/figures/003_Figure_3.jpg]]
*Figure 3: (a) Under standard motion representation and guiding method, only a few values in the motion representation are updated according to the guidance. (b) With Emphasis projection, all values in each frame describing the motion receives gradients w.r.t. the guidance, leading to better coherence between global orientation and local pose in each frame. (c) With dense gradient propagation, all frames are updated according to the guidance at the keyframes, making the guidance less likely to be ignored*

GMD 采用**两阶段扩散管道**，将空间约束运动生成解耦为轨迹生成与运动合成两个子问题，如 Algorithm 1 和图 2(a) 所示。

**第一阶段：轨迹 DPM（ε 参数化）**。该阶段以文本提示为条件，生成满足空间目标函数 $G_z(\cdot)$ 的全局轨迹 $\mathbf{z}$。轨迹 DPM 采用 ε 预测（而非 x₀ 预测），使去噪网络在 $t \to T$ 时对采样均值的影响最大，从而与分类器引导信号的强度随扩散进程对齐，避免后期出现轨迹“收缩”现象（Figure 4）。生成过程结合**密集信号传播**：将稀疏关键帧位置约束通过去噪网络 $f(\mathbf{x}_t)$ 反向传播，产生稠密梯度 $\nabla_{\mathbf{x}_t} G_z(P_x^z f(\mathbf{x}_t))$，使引导影响力覆盖整个序列而非仅作用于约束帧。同时，在已知轨迹片段上使用插补（Eq. 3）施加硬约束，其余部分由分类器引导（Eq. 2）进行软调整，两者通过掩码 $M_z^x$ 协调。

**第二阶段：运动 DPM（x₀ 参数化）**。以第一阶段生成的轨迹 $\mathbf{z}$ 和文本嵌入为联合条件，生成完整的人体运动序列 $\mathbf{x}$。运动 DPM 集成**强调投影**：在训练和推理中对运动表示施加线性随机投影 $\mathbf{x}^{\text{proj}} = A\mathbf{x}$，放大轨迹维度（骨盆旋转与地面位置，仅 4 维）在 263 维表示中的相对方差，使空间信息与局部姿态的梯度在去噪过程中充分耦合。插补操作需在投影空间中完成“解投影→插补→再投影”的循环（Eq. 6），以保持单位方差的同时增强空间约束。

**条件注入方式**：两阶段均使用 CLIP 文本编码器将文本提示映射为嵌入向量，并以无分类器引导（classifier-free guidance）的方式注入去噪网络。网络架构采用 1D UNet + AdaGN（Table D.1, Figure D.1），时间步通过正弦编码，文本嵌入经 MLP 投影后输入 Adaptive Group Normalization 层。

**输入输出流总结**：文本提示 → CLIP 编码器 → 文本嵌入；文本嵌入 + 空间约束（关键帧/障碍物）→ 轨迹 DPM → 轨迹 $\mathbf{z}$；轨迹 $\mathbf{z}$ + 文本嵌入 → 运动 DPM（含强调投影）→ 完整运动序列 $\mathbf{x}$。两阶段均通过插补与密集信号传播的组合机制实现空间约束的精确遵循。

## 核心模块与公式推导

GMD 的核心架构由两个扩散概率模型（DPM）串联构成：**轨迹 DPM（Trajectory DPM）** 和 **运动 DPM（Motion DPM）**，两者通过两个关键机制——**强调投影（Emphasis Projection）** 和 **密集信号传播（Dense Signal Propagation）**——实现对空间约束的有效响应。

### 两阶段生成管道

GMD 采用先轨迹后运动的级联策略（Algorithm 1）。第一阶段，轨迹 DPM 以文本嵌入为条件，结合分类器引导和插补（imputation），生成满足空间目标函数（如关键帧位置、避障）的全局轨迹 $\mathbf{z}$。第二阶段，运动 DPM 以生成的轨迹和文本为条件，生成完整的人体运动序列 $\mathbf{x}$。

这一设计的因果逻辑在于：轨迹仅占运动表示中极少的维度（骨盆旋转与地面位置共 4 维，而局部姿态占 259 维），若直接在完整运动空间中进行空间引导，稀疏信号会被扩散模型当作噪声丢弃。分离轨迹生成可将空间约束问题聚焦于低维子空间，降低引导难度。

### 强调投影（Emphasis Projection）

强调投影是作用于运动 DPM 训练与推理阶段的线性随机投影方法，旨在解决轨迹信号在运动表示中方差占比过低的问题。

**动机**：标准运动表示中，轨迹部分的相对方差远小于局部姿态部分。当扩散模型接收轨迹约束时，其梯度更新主要集中在高方差的姿态维度上，导致轨迹与姿态之间产生运动不一致（如脚滑、轨迹偏离）。

**机制**：引入随机矩阵 $A = A' B$，其中 $B$ 为随机正交矩阵，$A'$ 为缩放矩阵，将原始运动表示 $\mathbf{x}$ 投影为 $\mathbf{x}^{\mathrm{proj}} = A \mathbf{x}$。投影后各维度的方差被重新分配，轨迹部分的相对重要性（方差占比）被人为放大，迫使去噪网络在训练中学习轨迹与姿态的耦合关系。

**投影空间中的插补**：在投影空间中执行插补需要先解投影、再插补、最后重新投影，公式为：

$$\tilde{\mathbf{x}}_{0}^{\mathrm{proj}} = A \Bigl( (1 - M_{z}^{x}) \odot (A^{-1} \mathbf{x}_{0,\theta}^{\mathrm{proj}}) + M_{z}^{x} \odot P_{z}^{x} \mathbf{z}^{*} \Bigr)$$

其中 $M_{z}^{x}$ 为轨迹部分的二值掩码，$P_{z}^{x}$ 将轨迹 $\mathbf{z}^{*}$ 映射到运动表示空间，$\mathbf{x}_{0,\theta}^{\mathrm{proj}}$ 为去噪网络在投影空间中预测的干净样本。解投影—插补—再投影的操作保持了投影空间的单位方差特性，同时将轨迹硬约束注入生成过程。

### 密集信号传播（Dense Signal Propagation）

密集信号传播解决的是时间维度的稀疏引导问题。当空间约束仅施加于少数关键帧时，标准分类器引导的梯度仅更新这些帧，其他帧不受影响，导致模型忽略引导信号。

**核心思路**：将扩散模型自身的去噪网络 $f(\mathbf{x}_t) = \mathbf{x}_{0,\theta}(\mathbf{x}_t)$ 视为运动先验，通过反向传播将稀疏的目标函数梯度扩展为稠密的分类器引导信号：

$$\nabla_{\mathbf{x}_t} \log p(G_x(X_t)=0|\mathbf{x}_t) \approx -\nabla_{\mathbf{x}_t} G_z(P_x^z f(\mathbf{x}_t))$$

其中 $G_z$ 为定义在轨迹空间上的目标函数，$P_x^z$ 从运动表示中提取轨迹部分。梯度从目标函数出发，经过去噪网络 $f$ 反向传播至当前噪声样本 $\mathbf{x}_t$，使所有帧都接收到与空间约束相关的更新信号。

**与插补的融合**：在同时使用插补和分类器引导时，采用掩码策略——插补覆盖已知区域（$M_z^x = 1$），分类器引导作用于其余区域（$1 - M_z^x$）。在强调投影空间中，最终的分类器引导项为：

$$\Delta_\mu = -s \Sigma_t A^{-1} \nabla_{\mathbf{x}_t^{\mathrm{proj}}} G_z(P_x^z A^{-1} f(\mathbf{x}_t^{\mathrm{proj}}))$$

$$\mu_t^{\mathrm{proj}} = \tilde{\mu}_t^{\mathrm{proj}} + A (1 - M_z^x) \odot \Delta_\mu$$

其中 $\tilde{\mu}_t^{\mathrm{proj}}$ 为插补后的采样均值，$s$ 为引导强度，$\Sigma_t$ 为后验方差。梯度项 $\Delta_\mu$ 仅在非插补区域生效，避免覆盖已知约束。

### 轨迹 DPM 的 $\epsilon$ 参数化

轨迹 DPM 采用 $\epsilon$ 预测而非 $\mathbf{x}_0$ 预测，这是保证引导信号在去噪全过程中持续生效的关键设计。

**因果机制**：在 DDPM 的去噪均值公式中：

$$\mu_t = \frac{\sqrt{\alpha_{t-1}}\beta_t}{1-\alpha_t} \mathbf{x}_0 + \frac{\sqrt{1-\beta_t}(1-\alpha_{t-1})}{1-\alpha_t} \mathbf{x}_t$$

当 $t \to 0$ 时，$\mathbf{x}_0$ 项的系数趋近于 1，而 $\mathbf{x}_t$ 项的系数趋近于 0。若模型预测 $\mathbf{x}_0$，则去噪后期采样均值几乎完全由模型预测的干净样本决定，分类器引导的梯度调整被模型自身的强偏置反向覆盖，表现为轨迹“收缩”行为（Figure 4）。相反，$\epsilon$ 模型在 $t = T$ 时对采样均值的影响最大，且其影响力随去噪进程自然衰减，与引导信号的作用强度在时间上对齐，从而消除了后期偏置问题。

### 目标函数设计

针对不同空间约束任务，GMD 定义了统一形式的目标函数 $G_x(\mathbf{x})$，通过最小化该函数实现可控生成：

- **轨迹条件**：$G_{x}(\mathbf{x}) := \left\| \mathbf{z} - P_{x}^{z} \mathbf{x} \right\|_{p}$，最小化生成运动轨迹与给定轨迹 $\mathbf{z}$ 的距离。

- **关键帧条件**：$G_{x}(\mathbf{x}) := \sum_{i} \left\| M_{y}^{z} (P_{x}^{z} \mathbf{x} - \mathbf{y}) \right\|_{p}$，仅在指定时间步评估与目标关键帧 $\mathbf{y}$ 的位置误差，$M_{y}^{z}$ 为关键帧时间掩码。

- **障碍物规避**：结合导航目标函数 $G_x^{\mathrm{loc}}$ 和斥力目标函数 $G_x^{\mathrm{obs}} := \sum_{i} - \mathrm{clipmax}(\mathrm{SDF}((P_x^z \mathbf{x})^{(i)}), c)$，其中 SDF 为有符号距离函数，$c$ 为安全距离阈值，当人体模型越过障碍边界时产生斥力梯度。

## 实验与分析

### 文本到动作生成主结果

GMD 在 HumanML3D 基准上的无条件/文本条件生成质量显著超越基线。如表 1 所示，GMD 的 FID 达到 **0.212**，相比 MDM 的 0.556 降低了 0.344，降幅超过 60%。与此同时，R-Precision 和 Diversity 指标与 MDM 保持可比水平，表明生成质量提升并非以牺牲文本匹配度或多样性为代价。这一提升的核心驱动力来自两方面：一是将运动根表示从相对增量改为绝对全局坐标（Table B.1 消融显示该改动使 GMD 的 FID 从 0.305 降至 0.212），二是强调投影机制在训练中重新分配了空间信息与局部姿态的方差权重，使模型不会将稀疏的轨迹维度当作噪声忽略。

![[assets/figures/papers/paper_list_l30_https_arxiv_org_abs_2305_12577/figures/004_Table_1.jpg]]
*Table 1: Text-to-motion evaluation on the HumanML3D [15] dataset. The right arrow → means closer to real data is better*

### 轨迹条件生成与强调投影消融

在轨迹条件生成任务中，强调投影是保证运动与给定轨迹一致性的关键。Table 2 的消融对比了两种增强空间引导的策略：直接在损失函数中对轨迹部分施加更大权重（emphasis loss），与本文提出的强调投影（emphasis projection）。结果表明，强调投影在 c=10 时将脚滑率（foot skating ratio）降至 **0.128**，同时 FID 保持最优；而单纯扩大损失权重无法达到同等的运动连贯性，说明方差重分配比损失缩放更有效地将空间梯度耦合到局部姿态维度。Figure 5 的定性对比进一步佐证：MDM 在跟踪“walking forward”轨迹时产生明显的不一致运动，而 GMD 结合强调投影后能紧密跟随给定轨迹。

![[assets/figures/papers/paper_list_l30_https_arxiv_org_abs_2305_12577/figures/006_Table_2.jpg]]
*Table 2: Trajectory-conditioned motions evaluation. The ground truth trajectory is used for imputing after each diffusion step. Comparing the effect of an original x with emphasis loss functions to the emphasis projection $\mathbf { x } ^ { \mathrm { { p r o j } } }$ after imputing whole trajectories after each diffusion step

### 关键帧条件生成与密集信号传播

密集信号传播（Dense Signal Propagation）是模型能遵循稀疏关键帧位置约束的必要条件。Figure 6 显示，去除该机制后，扩散模型完全忽略目标关键帧位置，生成的运动轨迹与给定约束无关。Table 3 的定量结果进一步证实：两阶段轨迹模型配合密集信号传播，在关键帧数量 N=5 的设置下，位置误差相比单阶段模型降低超过 50%。两阶段策略的因果逻辑是：第一阶段用 ε 参数化的轨迹 DPM 生成满足关键帧约束的全局轨迹，第二阶段以该轨迹为条件生成完整运动——这避免了单阶段模型中稀疏时间信号直接被扩散过程淹没的问题。

![[assets/figures/papers/paper_list_l30_https_arxiv_org_abs_2305_12577/figures/009_Table_3.jpg]]
*Table 3: The effect of different conditioning strategies tested on keyframe-conditioning task. The keyframes ( N = 5 ) are sampled from the ground truth motion trajectories with the same text prompts in the HumanML3D [15] test set*

### ε 参数化对引导稳定性的影响

轨迹 DPM 的参数化目标选择直接影响分类器引导的有效性。Figure 4 揭示了关键现象：x0 预测模型在去噪后期（t→0）会产生轨迹“收缩”行为，即模型偏置反向覆盖引导信号，导致生成轨迹偏离目标；而 ε 预测模型在 t=T 时对采样均值的影响最大，与引导信号的强度时间曲线对齐，从而消除了收缩现象。这一发现解释了为何 GMD 在轨迹 DPM 中采用 ε 参数化（motion DPM 仍用 x0 参数化），并在 Appendix A 中通过 x0 与 ε 对采样均值贡献的时间曲线给出了理论支撑。

### 障碍物规避与目标函数设计

GMD 在障碍物规避任务中通过组合两个目标函数实现空间约束：导航目标函数 $G_x^{\text{loc}}$ 引导运动从起点到达终点，障碍物推离函数 $G_x^{\text{obs}}$ 利用符号距离函数（SDF）在人体模型跨越障碍边界时产生反向梯度，clipmax 截断确保安全距离 c 外的区域不受影响。Figure 7 的可视化结果显示，生成的运动能自然绕开红色标记的障碍区域，同时保持与文本提示的语义一致性。但该方法依赖手工设计的目标函数，难以泛化到涉及复杂物理接触（如抓取物体）的场景。

### 失败模式与局限性

综合实验与分析，GMD 存在以下已知失效场景：（1）当引导信号极端稀疏或噪声较大时，密集信号传播的效果受限于去噪网络本身的能力，可能仍不够稳定；（2）强调投影的超参数 c 需手动设定，在不同数据集或运动风格下可能需要重新调优；（3）两阶段管道增加了推理时间，不适用于实时交互应用；（4）轨迹 DPM 容易过拟合，训练轮次需精细控制，否则会产生对分类器引导的抵抗行为。这些局限性指向了未来的改进方向：可学习的 c 值自适应、更高效的端到端架构、以及面向物理交互的目标函数自动化设计。

### 补充图表

![[assets/figures/papers/paper_list_l30_https_arxiv_org_abs_2305_12577/figures/012_Table.jpg]]
*Table: B.1. Text-to-motion evaluation on the HumanML3D [15] dataset. Comparision between relative and absolute root representation. The right arrow → means closer to real data is better*

![[assets/figures/papers/paper_list_l30_https_arxiv_org_abs_2305_12577/figures/013_Table.jpg]]
*Table: D.1. Network architecture of our GMD’s models based on the proposed 1D UNET with AdaGN*

## 方法谱系与知识库定位

GMD 的起点是 **MDM**（Tevet et al.，2023）——一个基于 Transformer 的文本到动作扩散模型，其运动表示中全局空间信息（骨盆旋转与地面位置）仅占 4 维，远少于局部姿态的 259 维。这一结构性倾斜导致 MDM 在接收空间约束（如轨迹、关键帧位置）时，将这些稀疏信号当作噪声丢弃，表现为脚滑、轨迹偏离等运动不一致。

GMD 并未推翻 MDM 的扩散框架，而是在其上插入两个因果调节旋钮：**强调投影**与**密集信号传播**。前者通过随机矩阵放大轨迹部分在运动表示中的方差比重，迫使模型在训练和推理中关注空间信息；后者利用扩散模型的去噪网络本身作为运动先验，将稀疏关键帧的梯度反向传播到所有帧，实现“稀疏引导→稠密响应”的转化。这一思路与通用的分类器引导（Dhariwal & Nichol，NeurIPS 2021）和插补方法（Lugmayr et al.，ECCV 2022）一脉相承，但 GMD 的关键差异在于将空间引导问题重新表述为**表示学习与信号密集化**问题，而非简单增加损失权重或扩大引导尺度。

在架构层面，GMD 将 MDM 的 Transformer 替换为 1D UNet with AdaGN，并将轨迹 DPM 的参数化目标从 x₀ 预测改为 ε 预测。这一改动的因果逻辑是：ε 模型在去噪早期（t → T）对采样均值的贡献最大，此时引导信号也最强；而 x₀ 模型在去噪后期（t → 0）贡献增强，会反向覆盖引导信号，导致轨迹“收缩”现象（Figure 4）。因此，ε 参数化使引导强度与扩散过程自然对齐，是密集信号传播有效性的结构前提。

**适用边界与局限**：GMD 的空间引导能力依赖于手工设计的目标函数，这在涉及复杂物理接触（如抓取物体、与动态环境交互）时难以泛化。两阶段管道增加了推理时间，不适用于实时交互式应用。强调投影的超参数 c 需手动设定，在不同数据集或运动风格下可能需重新调整。密集信号传播的效果受限于 DPM 的去噪能力，在极端稀疏或噪声较大的引导下仍可能不稳定。此外，轨迹 DPM 容易过拟合，训练轮次需精细控制以避免抵抗分类器引导。

**开放问题**：如何为高维人体运动数据设计有效的 ε 预测模型，既能保证生成质量又能充分响应引导信号？能否将强调投影中的 c 值设计为可学习或自适应，避免对不同数据集的手动微调？GMD 框架是否可以扩展至多角色交互或与动态物体的物理接触场景，而不仅限于静态障碍物和关键帧？在更长的运动序列生成中，如何保持密集信号传播的计算效率和控制精度？

## 原文 PDF

![[paperPDFs/ICCV_2023/Guided_Motion_Diffusion_for_Controllable_Human_Motion_Synthesis.pdf]]
