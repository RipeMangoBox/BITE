---
title: DisCoRD Discrete Tokens to Continuous Motion via Rectified Flow Decoding
type: paper
paper_level: A
venue: ICCV
year: 2025
pdf_ref: paperPDFs/ICCV_2025/DisCoRD_Discrete_Tokens_to_Continuous_Motion_via_Rectified_Flow_Decoding.pdf
project_link: https://whwjdqls.github.io/discord-motion/
code_link: null
aliases:
- DDTCMRFD
tags:
- ICCV_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 将离散令牌的解码方式从确定性的一步前馈解码器（feedforward decoder）替换为在连续原始运动空间中运行的条件整流流（rectified flow）迭代解码器，以离散令牌作为条件信号，在连续空间中逐步优化动作序列。
primary_logic: 离散令牌解码本质上可被视为一个条件生成问题：利用离散令牌中编码的语义与结构信息作为条件，通过整流流模型在连续运动空间中执行迭代去噪/传输，逐步恢复具有丰富动态和高度平滑性的自然动作，从而在不牺牲对控制信号忠实度的前提下大幅提升自然度。
claims:
- DisCoRD 解码器相对于原始前馈解码器在动作重建中显著降低 FID 和 sJPE：MoMask 基线 FID 0.019 → 0.011 (+42%)，sJPE 0.512 → 0.385 (+25%)
- 在文本到动作生成任务中，DisCoRD 在提升自然度（FID）的同时保持了忠实度（R-Precision）：MoMask+DisCoRD 在 HumanML3D 上 FID 0.032，R-Precision Top-1 0.524，与基线 MoMask (0.521) 几乎持平
- sJPE 对帧级高斯噪声高度敏感，而 FID 几乎不响应，证明 sJPE 能有效捕获传统 FID 无法反映的自然度缺陷
- 在共语音手势生成和音乐驱动舞蹈生成任务上，DisCoRD 同样大幅降低 sJPE（例如 TalkSHOW 基线 sJPE 0.284 → 0.077），验证了方法的跨任务通用性
---

# DisCoRD Discrete Tokens to Continuous Motion via Rectified Flow Decoding

> [!tip] 核心洞察
> 离散令牌解码本质上可被视为一个条件生成问题：利用离散令牌中编码的语义与结构信息作为条件，通过整流流模型在连续运动空间中执行迭代去噪/传输，逐步恢复具有丰富动态和高度平滑性的自然动作，从而在不牺牲对控制信号忠实度的前提下大幅提升自然度。

| 字段 | 内容 |
|------|------|
| 中文题名 | DisCoRD：通过整流流解码将离散令牌转换为连续运动 |
| 英文题名 | DisCoRD Discrete Tokens to Continuous Motion via Rectified Flow Decoding |
| 会议/期刊 | ICCV 2025 |
| Links | [Project](https://whwjdqls.github.io/discord-motion/) · [paper](https://arxiv.org/abs/2411.19527) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | DisCoRD |
| Dataset | HumanML3D Reconstruction, HumanML3D Generation, SHOW Co-speech Gesture |

> [!tip] 效果简介
> - HumanML3D Reconstruction 上，FID 0.011 (MoMask+DisCoRD) vs 0.019 (MoMask) (+42% (lower is better))；sJPE 0.385 (MoMask+DisCoRD) vs 0.512 (MoMask) (+25% (lower is better))。
> - HumanML3D Generation 上，FID 0.032 (MoMask+DisCoRD) vs 0.045 (MoMask) (+29% (lower is better))；R Precision Top-1 0.524 (MoMask+DisCoRD) vs 0.521 (MoMask) (+0.6% (faithfulness preserved))。
> - SHOW Co-speech Gesture 上，sJPE 0.077 (TalkSHOW+DisCoRD) vs 0.284 (TalkSHOW) (-73% (lower is better))。

## 概要

### 问题背景

基于离散令牌的运动生成方法（如 VQ-VAE 结合自回归模型）在文本到动作、共语音手势等任务中展现了高控制忠实度，但其解码机制存在一个被忽视的瓶颈：**前馈解码器（feedforward decoder）将离散令牌一步映射为动作序列，导致离散化误差直接传播到连续运动空间**。其后果表现为两类自然度缺陷——（1）**欠重构**：动态细节丢失，动作缺乏表现力；（2）**帧级噪声**：解码动作出现高频抖动，破坏运动平滑性。传统评估指标 FID 对这两类缺陷均不敏感，使得问题长期被掩盖。

### 核心方法

DisCoRD 将离散令牌解码重新定义为**条件生成问题**：以预训练 VQ-VAE 产生的离散令牌作为条件信号，在连续原始运动空间中运行**整流流（rectified flow）迭代解码器**，从高斯噪声逐步传输到目标动作。这一设计保留了离散令牌对控制信号的忠实度，同时通过连续空间中的迭代优化恢复运动的固有平滑性与动态丰富度。具体而言，DisCoRD 通过**条件投影**将离散令牌转换为帧级连续特征，与带噪运动拼接后训练向量场 $v_\theta$，推理时从噪声出发沿学得的 ODE 轨迹生成最终动作。

### 方法定位

DisCoRD 是一种**解码器替换方案**，不改变预训练的量化器和令牌预测模型。它桥接了离散方法的控制忠实度优势与连续方法的自然度优势，可即插即用地部署到现有离散运动生成管线（如 **MoMask**、**T2M-GPT**、**BAMM** 等）中。

### 主要结果

- **运动重建**（HumanML3D）：MoMask + DisCoRD 相比原始 MoMask，FID 从 0.019 降至 0.011（提升 42%），sJPE 从 0.512 降至 0.385（提升 25%），验证了迭代连续解码对欠重构和帧级噪声的显著抑制。
- **文本到动作生成**（HumanML3D）：MoMask + DisCoRD 在 FID 上达到 0.032（基线 0.045），同时 R-Precision Top-1 保持在 0.524（基线 0.521），证明自然度大幅提升且忠实度无损。
- **跨任务泛化**：在共语音手势生成（TalkSHOW + DisCoRD，sJPE 从 0.284 降至 0.077）和音乐驱动舞蹈生成任务上同样取得一致改善，验证了方法的通用性。
- **指标验证**：提出的 **sJPE**（对称 Jerk 百分比误差）对帧级高斯噪声高度敏感，而 FID 几乎无响应，证明 sJPE 能有效捕获传统分布度量无法反映的自然度缺陷。



人体动作生成是计算机视觉与图形学中的核心问题，其目标是根据文本、语音或音乐等控制信号合成逼真的三维人体运动序列。近年来，基于离散表示的方法逐渐成为主流范式。这类方法通常采用两阶段流程：首先训练一个基于 VQ-VAE 的量化器，将连续运动序列编码为离散令牌；然后训练一个自回归或掩码令牌预测模型，根据控制信号生成令牌序列；最后通过一个确定性前馈解码器将离散令牌一步映射回运动空间。代表性工作包括 **T2M-GPT**、**MoMask**、**BAMM** 和 **MMM** 等。

这种离散化策略带来了显著优势：离散令牌能够有效压缩运动数据中的高层语义与结构信息，使得令牌预测模型能够以高忠实度响应控制信号。然而，这一范式存在一个被长期忽视的根本性瓶颈：**离散令牌解码过程中的信息损失**。VQ-VAE 将连续运动映射到有限码本的过程本身引入了不可逆的离散化误差，而现有方法采用的前馈解码器以一步式、确定性的方式直接从离散令牌重建运动，无法弥补这一误差。其后果表现为两类典型缺陷：

- **欠重构**：解码出的动作缺乏丰富的动态细节，动作显得僵硬、不生动，丢失了真实运动中细微的速度变化和关节协调模式。
- **帧级噪声**：解码结果中出现高频抖动，运动轨迹不平滑，破坏视觉自然度。

相比之下，连续空间中的生成方法（如基于扩散模型的 **MLD**）虽然能产生平滑的运动，却往往在忠实度上有所妥协——生成的语义内容与控制信号之间的一致性不足。

DisCoRD 的动机正是弥合这一鸿沟：**在保留离散令牌高忠实度优势的前提下，消除其自然度缺陷**。核心洞察在于，离散令牌解码本质上可以被重新定义为一个条件生成问题——以离散令牌中编码的语义与结构信息作为条件，在连续原始运动空间中执行迭代优化，逐步恢复被离散化过程丢失的动态细节与平滑性。这一思路将解码从“一步映射”转变为“条件连续生成”，从而在不牺牲对控制信号忠实度的前提下，大幅提升生成动作的自然度。



## 核心方法与创新机理

DisCoRD 的核心创新在于将离散运动令牌的解码方式从**确定性一步前馈映射**替换为**在连续原始运动空间中运行的条件整流流迭代解码器**。这一改变直接针对现有离散运动生成方法（如 T2M-GPT、MoMask、BAMM、MMM）的瓶颈：前馈解码器将离散化误差直接传播到输出动作序列，导致两个相互关联的自然度缺陷——**欠重构**（动态细节丢失，动作呆板）与**帧级噪声**（高频抖动破坏运动平滑性）。

### 关键洞察：解码即条件生成

DisCoRD 的核心洞察在于重新定义离散令牌解码的本质：**令牌解码不是简单的映射，而是一个条件生成问题**。离散令牌中编码了运动的结构与语义信息，这些信息应作为条件信号，引导一个生成模型在连续空间中逐步恢复具有丰富动态和高平滑度的自然动作。这一视角转变使得解码过程从“一步到位”变为“逐步优化”，从而在不牺牲对控制信号忠实度的前提下大幅提升生成动作的自然度。

### Changed Slot：解码器替换

DisCoRD 对现有离散运动生成流水线的唯一修改点在于解码器模块：

| 模块 | 基线方法 | DisCoRD 方法 |
|------|----------|--------------|
| **解码器** | 前馈解码器 D（从离散令牌一步映射到动作序列） | 条件整流流解码器，包含条件投影与迭代 ODE 求解 |

其余组件（预训练 VQ-VAE 量化器、令牌预测模型）均保持冻结，确保公平对比。

### 条件投影：令牌到帧级特征的桥接

为实现离散令牌对连续解码过程的有效条件化，DisCoRD 设计了**条件投影**（Condition Projection）模块。该模块将每个离散令牌 $z_t$ 通过重复、堆叠、线性投影和解堆叠操作，转换为与原始运动帧一一对应的帧级条件特征 $\mathbf{C} = [c_1, \dots, c_T]$，保持了时序对应关系。消融实验证实，这种 Stack & Unstack 投影方式在生成 FID（0.032）上优于简单的上卷积投影（0.039）和重复+线性投影（0.038），表明其更强的泛化能力。

### 整流流解码：连续空间中的迭代传输

解码器采用**整流流**（Rectified Flow）框架，在连续原始运动空间中求解条件常微分方程：

$$d \mathbf{X}_t = v(\mathbf{X}_t, t, \mathbf{C}) dt$$

训练时，模型学习一个向量场 $v$，使其逼近从高斯噪声 $\mathbf{X}_0$ 到真实运动 $\mathbf{X}_1$ 的传输方向，条件为帧级特征 $\mathbf{C}$：

$$\min_v \int_0^1 \mathbb{E}\left[\|(\mathbf{X}_1 - \mathbf{X}_0) - v(\mathbf{X}_t, t, \mathbf{C})\|^2\right] dt, \quad \mathbf{X}_t = t\mathbf{X}_1 + (1-t)\mathbf{X}_0$$

推理时，从高斯噪声出发，通过学得的向量场迭代求解 ODE，逐步生成与离散令牌条件一致的自然运动。相比扩散模型，整流流提供了更直接的传输映射，推理步骤更少。

### 创新效果验证

MoMask+DisCoRD 在 HumanML3D 重建任务上，FID 从 0.019 降至 0.011（+42%），sJPE 从 0.512 降至 0.385（+25%）；在生成任务上，FID 从 0.045 降至 0.032（+29%），同时 R-Precision Top-1 保持几乎持平（0.524 vs 0.521），验证了“自然度提升而不牺牲忠实度”的核心主张。跨任务迁移至共语音手势生成（TalkSHOW+DisCoRD sJPE 从 0.284 降至 0.077）进一步证明了方法的通用性。



DisCoRD 的整体 pipeline 围绕一个核心设计展开：**将离散运动令牌的解码重新定义为一个条件生成问题**，在连续原始运动空间中通过迭代优化恢复自然动作。该框架由四个模块串联构成，形成训练与推理两条路径。

### 模块构成与数据流

**1. 预训练量化器（VQ-VAE）**
该模块将原始运动序列编码为离散令牌，并提供码本嵌入。在 DisCoRD 训练和推理阶段，量化器保持冻结状态，仅作为令牌提取器使用。其输出为离散令牌序列 $z_1, \dots, z_T$，每个令牌对应一段运动片段。

**2. 条件投影（Condition Projection）**
这是 DisCoRD 的关键连接模块，负责将离散令牌转化为帧级连续条件特征 $\mathbf{C}$。具体流程为：
- 将每个离散令牌 $z_t$ 沿时间维度重复，使其与对应运动片段的帧数对齐；
- 将所有重复后的令牌特征堆叠（stack），通过线性投影映射到连续特征空间；
- 再解堆叠（unstack），得到帧级条件特征序列 $\mathbf{C} = [c_1, \dots, c_T]$。

这一设计保持了离散令牌与运动帧之间的时间对应关系，消融实验表明，该投影方法在生成 FID（0.032）上优于简单的上卷积投影（0.039）和重复+线性投影（0.038），泛化能力更强（Table 6）。

**3. 整流流解码器（Rectified Flow Decoder）**
解码器以高斯噪声 $\mathbf{X}_0 \sim \mathcal{N}(0, \mathbf{I})$ 为起点，在条件特征 $\mathbf{C}$ 的引导下，通过求解条件常微分方程迭代生成运动序列 $\hat{\mathbf{X}}_1$。训练目标为：

$$\min_v \int_0^1 \mathbb{E}\left[\|(\mathbf{X}_1 - \mathbf{X}_0) - v(\mathbf{X}_t, t, \mathbf{C})\|^2\right] dt, \quad \mathbf{X}_t = t\mathbf{X}_1 + (1-t)\mathbf{X}_0$$

其中向量场 $v$ 学习从噪声到真实运动 $\mathbf{X}_1$ 的直接传输方向。条件特征 $\mathbf{C}$ 沿通道维度与噪声运动 $\mathbf{X}_t$ 拼接后输入向量场网络。训练采用滑动窗口策略（windowed segments）而非全序列，消融显示这使生成 FID 从 0.038 降至 0.032，且加入注意力机制反而损害性能（Table 6）。

**4. 预训练令牌预测模型**
该模块在推理阶段使用，根据控制信号（如文本描述）生成离散令牌序列，作为条件投影的输入。DisCoRD 仅替换解码器部分，令牌预测模型保持原样，确保公平比较。

### 训练与推理流程

**训练阶段**（Figure 3）：
1. 冻结的量化器将真实运动编码为离散令牌；
2. 条件投影将令牌转化为帧级连续特征 $\mathbf{C}$；
3. 从真实运动 $\mathbf{X}_1$ 和高斯噪声 $\mathbf{X}_0$ 构造线性插值路径 $\mathbf{X}_t$；
4. 将 $\mathbf{X}_t$ 与 $\mathbf{C}$ 拼接，训练向量场 $v_\theta$ 逼近真实传输方向 $\mathbf{X}_1 - \mathbf{X}_0$。

**推理阶段**（Figure 3）：
1. 令牌预测模型根据控制信号生成离散令牌；
2. 条件投影将生成令牌转化为连续特征 $\hat{\mathbf{C}}$；
3. 从高斯噪声 $\mathbf{X}_0$ 出发，通过训练好的向量场 $v_\theta$ 迭代求解 ODE $d\mathbf{X}_t = v_\theta(\mathbf{X}_t, t, \hat{\mathbf{C}}) dt$，逐步解码为运动序列 $\hat{\mathbf{X}}_1$。

### 与基线方法的架构差异

传统离散方法（如 **MoMask**、**T2M-GPT**、**BAMM**、**MMM**）使用确定性的一步前馈解码器直接将离散令牌映射为动作序列。DisCoRD 将这一解码器替换为在连续空间中运行的整流流迭代解码器，其余组件（量化器、令牌预测模型）完全复用。这一替换是 DisCoRD 性能提升的唯一架构变更，消融实验中整流流解码器（RF）相比前馈解码器（FF）在生成任务上 FID 从 0.064 降至 0.032，重建 sJPE 从 0.512 降至 0.385（Table 6）。

### 补充图表

![[assets/figures/papers/paper_list_l1885_DisCoRD_Discrete_Tokens_to_Continuous_Motion_via_Rectified_Flow_Decoding/figures/003_Figure_3.jpg]]
*Figure 3: An overview of DisCoRD. During the Training stage, we leverage a pretrained quantizer to first obtain discrete representations (tokens) of motion. These tokens are then projected into continuous features C, which are concatenated with noisy motion*



### 3.1 预备知识：整流流（Rectified Flow）

DisCoRD 的解码器建立在整流流框架之上。整流流将样本生成建模为一个传输问题：通过一个常微分方程（ODE）定义从源分布（高斯噪声）到目标分布（真实运动）的直接传输路径。

**核心 ODE：**
$$d x_t = v(x_t, t) dt$$
其中 $v$ 是待学习的向量场，$t \in [0, 1]$ 为时间参数。

**前向扩散过程**通过源样本 $x_0$ 与目标样本 $x_1$ 之间的线性插值构建：
$$x_t = t x_1 + (1-t) x_0$$

**训练目标**为最小二乘回归，使向量场 $v$ 逼近真实的传输方向 $x_1 - x_0$：
$$\min_v \int_0^1 \mathbb{E}\left[ \|(x_1 - x_0) - v(x_t, t)\|^2 \right] dt$$

该框架为后续的条件解码提供了基础：一旦向量场 $v$ 学习完成，即可通过从 $t=0$ 到 $t=1$ 求解 ODE，将高斯噪声逐步传输为目标运动样本。

### 3.2 DisCoRD 解码器架构

DisCoRD 将离散令牌解码重新定义为条件生成任务，其核心由两个模块组成：**条件投影（Condition Projection）** 和 **条件整流流解码器（Conditional Rectified Flow Decoder）**。

#### 3.2.1 条件投影

该模块将预训练 VQ-VAE 量化器产生的离散令牌序列 $\{z_t\}_{t=1}^{T}$ 转换为与原始运动帧一一对应的连续条件特征 $\mathbf{C} = [c_1, \dots, c_T]$。具体流程为：

1. **重复（Repeat）**：将每个离散令牌 $z_t$ 沿时间维度重复 $r$ 次（$r$ 为量化器的下采样率），使令牌序列长度与运动帧数匹配。
2. **堆叠（Stack）**：将重复后的令牌序列堆叠为张量形式。
3. **线性投影（Linear Projection）**：通过可学习的线性层将离散令牌嵌入映射到连续特征空间。
4. **解堆叠（Unstack）**：恢复为逐帧的条件特征序列 $\mathbf{C}$。

该设计的核心优势在于：保持了离散令牌与运动帧之间的时间对应关系，使得整流流解码器能够在每一帧获得精确的语义条件信号。

#### 3.2.2 条件整流流解码器

解码器在连续原始运动空间中运行，以条件特征 $\mathbf{C}$ 为引导，从高斯噪声 $\mathbf{X}_0 \sim \mathcal{N}(0, I)$ 逐步生成目标运动 $\mathbf{X}_1$。

**条件向量场训练目标**为：
$$\min_v \int_0^1 \mathbb{E}\left[\|(\mathbf{X}_1 - \mathbf{X}_0) - v(\mathbf{X}_t, t, \mathbf{C})\|^2\right] dt, \quad \mathbf{X}_t = t\mathbf{X}_1 + (1-t)\mathbf{X}_0$$

具体实现中，条件特征 $\mathbf{C}$ 沿通道维度与带噪运动 $\mathbf{X}_t$ 拼接后输入向量场网络 $v_\theta$。推理时，利用预训练的令牌预测模型（如 T2M-GPT、MoMask）从控制信号生成离散令牌序列，经条件投影得到 $\hat{\mathbf{C}}$，再通过求解条件 ODE 从高斯噪声迭代解码为最终运动 $\hat{\mathbf{X}}_1$。

### 3.3 自然度评估指标：sJPE

为量化解码器输出中“欠重构”（动态细节丢失）和“帧级噪声”（高频抖动）两类自然度缺陷，DisCoRD 提出了**对称 Jerk 百分比误差（Symmetric Jerk Percentage Error, sJPE）**。

Jerk 定义为位置的三阶导数，反映运动的平滑性变化。sJPE 计算预测运动与真实运动在 jerk 上的对称平均绝对百分比误差：
$$\mathrm{sJPE} = \frac{1}{n} \sum_{t=1}^{n} \frac{|J_{\mathrm{pred},t} - J_{\mathrm{true},t}|}{|J_{\mathrm{true},t}| + |J_{\mathrm{pred},t}|}$$

为进一步诊断误差来源，sJPE 可分解为两个互补分量：

**噪声分量（Noise sJPE）**——捕获因预测 jerk 过高（帧级噪声）产生的误差：
$$\mathrm{Noise\ sJPE} = \frac{1}{n} \sum_{t=1}^{n} \frac{\max(0, J_{\mathrm{pred},t} - J_{\mathrm{true},t})}{|J_{\mathrm{true},t}| + |J_{\mathrm{pred},t}|}$$

**静态分量（Static sJPE）**——捕获因预测 jerk 过低（欠重构，缺乏动态）产生的误差：
$$\mathrm{Static\ sJPE} = \frac{1}{n} \sum_{t=1}^{n} \frac{\max(0, J_{\mathrm{true},t} - J_{\mathrm{pred},t})}{|J_{\mathrm{true},t}| + |J_{\mathrm{pred},t}|}$$

实验验证（Figure 4）表明，在真实运动上叠加帧级高斯噪声时，Noise sJPE 高度敏感，而 Static sJPE 保持低位；相比之下，FID 对同样的噪声几乎无响应。这证明 sJPE 能有效捕获传统分布度量（FID）无法反映的自然度缺陷。

![[assets/figures/papers/paper_list_l1885_DisCoRD_Discrete_Tokens_to_Continuous_Motion_via_Rectified_Flow_Decoding/figures/004_Figure_4.jpg]]
*Figure 4: sJPE and FID response to frame-wise gaussian noise. We introduce Gaussian noise with varying standard deviations (x-axis) to ground-truth motion data and evaluate its effect on sJPE and FID. Noise sJPE is highly sensitive to subtle frame-wise perturbations, whereas Static sJPE remains low. FID is highly insensitive to frame-wise noise. Note that FID scale (y-axis, right) is very small compared to sJPE scale (y-axis, left)*

### 3.4 模块间数据流

整体推理流程的数据依赖关系如 Figure 3 所示：

1. **预训练量化器**（冻结）：将原始运动编码为离散令牌，提供码本嵌入。
2. **令牌预测模型**（冻结）：根据控制信号（文本、语音、音乐）生成离散令牌序列。
3. **条件投影**（可训练）：将离散令牌转换为逐帧连续条件特征 $\mathbf{C}$。
4. **整流流解码器**（可训练）：以 $\mathbf{C}$ 为条件，从高斯噪声 $\mathbf{X}_0$ 迭代求解 ODE 至 $\mathbf{X}_1$，输出最终运动。

训练阶段仅优化条件投影和整流流解码器的参数，量化器与令牌预测模型保持冻结，确保与现有离散运动生成框架的兼容性。

### 补充图表

![[assets/figures/papers/paper_list_l1885_DisCoRD_Discrete_Tokens_to_Continuous_Motion_via_Rectified_Flow_Decoding/figures/002_Figure_2.jpg]]
*Figure 2: Concept of DisCoRD. Discrete quantization methods encode multiple motions into a single quantized representation. While existing methods directly decode from this quantized representation, DisCoRD iteratively decodes the discrete latent in a continuous space to recover the inherent continuity and dynamism of motion. To assess the gap between reconstructed and real motion, prior work primarily used FID as the metric. Here, we additionally propose symmetric Jerk Percentage Error (sJPE) to evaluate the differences in naturalness between reconstructed and real motion*



## 实验与关键发现

### 核心瓶颈与因果机制

DisCoRD 旨在解决离散运动生成方法中一个被长期忽视的本质缺陷：**前馈解码器的一步式映射会忠实地传播离散化误差**。具体而言，基于 VQ-VAE 的离散方法（如 **T2M-GPT**、**MoMask**、**BAMM**、**MMM**）使用确定性前馈网络直接将离散令牌映射为动作序列。这种解码方式导致两个相互关联的自然度退化问题：

1. **欠重构**：动态细节丢失，动作缺乏表现力，表现为 jerk 的欠估计；
2. **帧级噪声**：解码动作出现高频抖动，破坏运动平滑性，表现为 jerk 的过估计。

DisCoRD 的因果干预是将解码器从确定性一步前馈替换为**在连续原始运动空间中运行的条件整流流迭代解码器**。离散令牌不再直接映射为动作，而是通过条件投影转化为逐帧条件特征，引导整流流模型从高斯噪声中逐步传输到目标运动。这一设计将令牌解码重新框定为条件生成问题，使模型在连续空间中迭代优化，从而恢复丰富的动态细节和高度平滑性，同时保持对控制信号的忠实度。

### 主实验结果

#### 运动重建：自然度大幅提升

Table 1 报告了 HumanML3D 和 KIT-ML 数据集上的运动重建结果。DisCoRD 作为离散基线的即插即用解码器，在所有模型上一致地降低了 FID 和 sJPE：

![[assets/figures/papers/paper_list_l1885_DisCoRD_Discrete_Tokens_to_Continuous_Motion_via_Rectified_Flow_Decoding/figures/006_Table_1.jpg]]
*Table 1: Quantitative results on motion reconstruction. Dis-CoRD enhances naturalness as a decoder for discrete models, shown by improvements over base models on FID and sJPE (blue). H-ML3D stands for HumanML3D and cont. for continuous*

- **MoMask + DisCoRD** 在 HumanML3D 上 FID 从 0.019 降至 0.011（相对提升 42%），sJPE 从 0.512 降至 0.385（相对提升 25%）；
- **T2M-GPT + DisCoRD** 在 KIT-ML 上 FID 从 0.711 降至 0.284（相对提升 40%），sJPE 从 0.573 降至 0.422（相对提升 26%）；
- 在 HumanML3D 上，MoMask + DisCoRD 的 FID（0.011）甚至优于连续方法 **MLD**（0.021），说明迭代连续解码能够弥合离散方法与连续方法在自然度上的差距。

#### 文本到动作生成：自然度与忠实度的双赢

Table 2 展示了 HumanML3D 和 KIT-ML 上的文本到动作生成结果。DisCoRD 在显著提升自然度（FID）的同时，保持了与基线几乎持平的忠实度（R-Precision）：

![[assets/figures/papers/paper_list_l1885_DisCoRD_Discrete_Tokens_to_Continuous_Motion_via_Rectified_Flow_Decoding/figures/007_Table_2.jpg]]
*Table 2: Quantitative results on motion generation. ± indicates a 95% confidence interval. +DisCoRD indicates that the baseline model’s decoder is replaced with DisCoRD. Bold indicates the best result, while underscore refers the second best. DisCoRD improves naturalness, as evidenced by FID improvements shown in blue, while preserving faithfulness, demonstrated by R-Precision*

- **MoMask + DisCoRD** 在 HumanML3D 上 FID 为 0.032（MoMask 基线 0.045，提升 29%），R-Precision Top-1 为 0.524（MoMask 基线 0.521，仅下降 0.6%，在置信区间内可视为持平）；
- **BAMM + DisCoRD** 在 HumanML3D 上 FID 从 0.055 降至 0.041（提升 25%）；
- **T2M-GPT + DisCoRD** 在 HumanML3D 上 FID 从 0.116 降至 0.095（提升 18%）。

这一结果表明，DisCoRD 成功打破了连续方法（自然度高但忠实度低）与离散方法（忠实度高但自然度低）之间的固有权衡（Figure 1 定性展示）。

![[assets/figures/papers/paper_list_l1885_DisCoRD_Discrete_Tokens_to_Continuous_Motion_via_Rectified_Flow_Decoding/figures/001_Figure_1.jpg]]
*Figure 1: Continuous methods generate smooth motions, but lack faithfulness (red text) to conditioning signals. In contrast, discrete methods demonstrate high faithfulness (blue words) but often produce less natural results such as unexpressive motion and frame-wise noise (red box). We present a novel discrete token decoding method, DisCoRD, that generates smooth, dynamic motion (blue box) while faithfully adhering to the conditioning signal. The plotted lines represent left-hand trajectories of generated motions for visual comparison*

#### 跨任务泛化

DisCoRD 的迭代连续解码策略在共语音手势生成和音乐驱动舞蹈生成任务上也展现出强泛化能力：

- **共语音手势生成**（Table 3）：**TalkSHOW + DisCoRD** 在 SHOW 测试集上 sJPE 从 0.284 降至 0.077（降低 73%），FGD 也有改善；
- **音乐驱动舞蹈生成**（Table 4）：DisCoRD 在 AIST++ 测试集上显著降低 sJPE、Dist_k 和 Dist_g，但 FID_k 和 FID_g 出现退化。作者指出这两个分布度量在该数据集上已知不可靠，而 Beat Align Score 有所改善，表明动作与音乐节拍的对齐质量提升。

![[assets/figures/papers/paper_list_l1885_DisCoRD_Discrete_Tokens_to_Continuous_Motion_via_Rectified_Flow_Decoding/figures/008_Table_3.jpg]]
*Table 3: Quantitative results on each method’s SHOW test set. DisCoRD outperforms baseline models on sJPE and FGD*

![[assets/figures/papers/paper_list_l1885_DisCoRD_Discrete_Tokens_to_Continuous_Motion_via_Rectified_Flow_Decoding/figures/009_Table_4.jpg]]
*Table 4: Quantitative results on the AIST++ test set. DisCoRD outperforms baseline model on sJPE, Distk and*

### 消融实验

Table 6 系统性地验证了 DisCoRD 各设计选择的贡献：

![[assets/figures/papers/paper_list_l1885_DisCoRD_Discrete_Tokens_to_Continuous_Motion_via_Rectified_Flow_Decoding/figures/011_Table_6.jpg]]
*Table 6: Ablation studies. Evaluation on the HumanML3D test set assessing the impact of decoding strategies, projection methods, and training strategies. FF and RF denote feedforward and rectified flow model, respectively*

1. **解码策略**：整流流解码器（RF）相比前馈解码器（FF）在生成任务上 FID 从 0.064 降至 0.032，重建 sJPE 从 0.512 降至 0.385，验证了迭代连续解码的核心优势。

2. **条件投影方法**：提出的 Stack & Unstack 投影在生成 FID（0.032）上优于简单的上卷积投影（0.039）和重复+线性投影（0.038），尽管后两者在重建指标上类似。这表明 Stack & Unstack 方法通过保持时序对应关系，使条件特征具有更强的泛化能力。

3. **训练策略**：使用滑动窗口片段训练（windowed segments）比使用全序列训练（full sequences）的生成 FID 更低（0.032 vs 0.038），且加入注意力机制会损害性能。这说明局部运动片段训练有助于模型学习细粒度动态，避免对全局序列模式的过拟合，从而提升第二阶段生成时的泛化能力。

### 评估指标的灵敏度验证

Figure 4 通过向真实运动注入不同标准差的高斯噪声，系统性地验证了 sJPE 和 FID 对帧级噪声的响应特性：

- **Noise sJPE** 对微小帧级扰动高度敏感，随噪声标准差线性增长；
- **Static sJPE** 始终保持在低水平，不受纯加性噪声影响；
- **FID** 对帧级噪声几乎不响应（注意 FID 的 y 轴尺度远小于 sJPE）。

这一分析证明 sJPE 能有效捕获传统 FID 无法反映的自然度缺陷——帧级噪声和欠重构。Figure 5 进一步通过运动轨迹和 jerk 图可视化展示了 DisCoRD 如何减少蓝色区域（噪声 sJPE）和红色区域（静态 sJPE），生成更平滑且更富动态的动作。

![[assets/figures/papers/paper_list_l1885_DisCoRD_Discrete_Tokens_to_Continuous_Motion_via_Rectified_Flow_Decoding/figures/005_Figure_5.jpg]]
*Figure 5: Under-reconstruction and frame-wise noise. We visualize fine-grained motion trajectories (top), and corresponding jerk graphs (bottom), where blue and red regions indicate noise and static sJPE, respectively. Compared to other methods, DisCoRD significantly reduces sJPE, resulting in smoother motion (fewer blue regions) and greater dynamism (fewer red regions), as highlighted in green boxes*

### 失败模式与局限性

1. **音乐到舞蹈生成的指标退化**：在 AIST++ 上 FID_k 和 FID_g 出现退化。作者归因于这些指标在该数据集上已知不可靠，但这一现象表明 DisCoRD 在特定领域的评估可能需要专门的度量标准。Beat Align Score 的改善提供了部分正面证据，但该任务上的整体性能需要更多定性评估支持。

2. **对预训练组件的依赖**：DisCoRD 的性能上限受预训练 VQ-VAE 量化器和令牌预测模型的质量约束。若量化器引入严重离散化误差，解码器无法完全纠正。当前实验均在固定预训练模型上进行，未探索端到端联合训练的可能性。

3. **计算开销**：单个 RTX 4090 Ti 训练需 35 小时。Figure 6 显示 DisCoRD 的解码时间与基线方法可比（批量解码 32 个序列的平均耗时相近），但迭代解码的推理步骤数是一个可调节的效率-质量权衡参数。

![[assets/figures/papers/paper_list_l1885_DisCoRD_Discrete_Tokens_to_Continuous_Motion_via_Rectified_Flow_Decoding/figures/012_Figure_6.jpg]]
*Figure 6: Decoding efficiency comparison. We report the average decoding time for a batch of 32 token sequences on an NVIDIA RTX 4090 Ti, averaged over 20 trials on the HumanML3D test set. DisCoRD achieves more better performance on motion naturalness at a comparable decoding speed to MoMask and can even decode significantly faster while maintaining superior performance*

4. **sJPE 的适用边界**：sJPE 计算依赖真实运动 jerk，在无真值的开放生成场景中无法直接应用，需依赖参考动作或模型级代理指标。

### 补充图表

![[assets/figures/papers/paper_list_l1885_DisCoRD_Discrete_Tokens_to_Continuous_Motion_via_Rectified_Flow_Decoding/figures/010_Figure.jpg]]



## 定位与知识库关联

### 1. 核心问题定位：离散运动生成的解码瓶颈

DisCoRD 瞄准的是当前离散运动生成范式中的一个结构性缺陷。以 **T2M-GPT**、**MoMask**、**BAMM**、**MMM** 等为代表的离散方法，其标准流程是：先用 VQ-VAE 将连续运动序列量化为离散令牌（tokens），再用一个确定性前馈解码器（feedforward decoder）将令牌一步映射回动作序列。这种一步式解码存在两个传播性缺陷：

- **欠重构（under-reconstruction）**：离散化过程丢失了原始运动的精细动态细节，前馈解码器无法在解码阶段恢复这些信息，导致生成的动作缺乏生动性。
- **帧级噪声（frame-wise noise）**：解码出的动作在相邻帧之间出现高频抖动，破坏运动平滑性，这是离散化误差在时域上的直接表现。

这两个问题共同导致生成动作的“自然度”严重下降，而传统评估指标 FID 对此类缺陷并不敏感（Figure 4 的灵敏度分析提供了关键证据）。

### 2. 方法定位：离散令牌的条件连续解码

DisCoRD 的方法论定位清晰而精确：**它不改变离散令牌的生成方式，而是重新定义令牌到动作的解码方式**。具体而言，DisCoRD 将解码过程从确定性的一步前馈映射，替换为在连续原始运动空间中运行的条件整流流（rectified flow）迭代解码器。

这一设计的核心洞察在于：离散令牌解码本质上是一个条件生成问题——令牌中编码了动作的语义与结构信息，可以将其作为条件信号，通过整流流模型在连续空间中执行迭代传输，逐步从高斯噪声中恢复具有丰富动态和高度平滑性的自然动作。

从方法谱系上看，DisCoRD 处于以下三条技术路线的交汇点：

1. **离散运动生成（VQ-VAE + 自回归/掩码令牌预测）**：继承了 **T2M-GPT**、**MoMask** 等工作的离散令牌化优势（高忠实度、强可控性），但抛弃了其一步式前馈解码的局限。

2. **连续空间生成模型（扩散/流匹配）**：借鉴了 **MLD** 等连续方法在原始运动空间中进行迭代去噪以获得平滑动作的思路，但保留了离散令牌作为条件信号，从而维持了对控制信号的忠实度。

3. **整流流（Rectified Flow）**：采用整流流而非标准扩散模型作为解码器的骨干，利用其直接传输映射的特性（$d x_t = v(x_t, t) dt$，线性插值前向过程 $x_t = t x_1 + (1-t) x_0$），在训练效率和采样速度上具有优势。

### 3. 与基线方法的关系

DisCoRD 在实验中作为解码器的即插即用替换件，与以下离散基线进行了系统对比：

- **MoMask**：当前离散运动生成的强基线之一。DisCoRD 替换其前馈解码器后，在 HumanML3D 重建任务上 FID 从 0.019 降至 0.011（+42%），sJPE 从 0.512 降至 0.385（+25%）（Table 1）；在文本到动作生成任务上，FID 从 0.045 降至 0.032（+29%），同时 R-Precision Top-1 保持在 0.524（基线 0.521），忠实度几乎无损（Table 2）。

- **T2M-GPT**：早期离散方法的代表。+DisCoRD 后在 KIT-ML 重建上 FID 提升 40%，在 HumanML3D 生成上 FID 提升 18%（Table 1, Table 2）。

- **BAMM**：+DisCoRD 后在 HumanML3D 生成上 FID 提升 25%（Table 2）。

- **MMM**：+DisCoRD 后同样在自然度指标上获得显著改善。

- **MLD**：作为连续方法的代表，在 Table 1 中作为重建参考出现。DisCoRD 在自然度（FID）上显著超越 MLD，同时维持了离散方法固有的高忠实度优势。

跨任务泛化方面，DisCoRD 在共语音手势生成（TalkSHOW+DisCoRD，sJPE 从 0.284 降至 0.077，降幅 73%，Table 3）和音乐驱动舞蹈生成（Table 4）上同样验证了其有效性，表明整流流解码的思想不局限于特定运动模态。

### 4. 适用边界与局限

尽管 DisCoRD 在主流基准上表现出色，其适用边界和局限同样值得关注：

**依赖性约束**：
- DisCoRD 的性能上限受预训练 VQ-VAE 量化器和令牌预测模型的质量约束。若量化器引入严重离散化误差，整流流解码器无法完全纠正——它只能在连续空间中优化解码过程，但无法修复已丢失的语义信息。
- 目前仅支持固定帧率和预定义的动作表示（基于标准骨架），尚未验证对任意骨架拓扑或可变帧率的泛化能力。

**特定领域的退化**：
- 在音乐到舞蹈生成任务（AIST++）上，传统的分布度量 FID_k 和 FID_g 显示 DisCoRD 出现退化。作者指出这些指标在该数据集上已知不可靠（Beat Align Score 有所改善），但这提示在特定领域可能需要专门的评估方法，DisCoRD 的优势并非在所有指标上无条件成立。

**计算成本**：
- 模型训练需要较高计算资源（单个 RTX 4090 Ti 训练 35 小时），相比一步式前馈解码器，推理时的迭代采样也会增加延迟。

**评估指标的局限**：
- 提出的 sJPE 指标虽然对自然度缺陷高度敏感，但其计算依赖真实运动 jerk 值。在无真值的开放生成场景中无法直接应用，需依赖参考动作或模型级指标。

### 5. 消融实验的关键发现

Table 6 的消融实验揭示了 DisCoRD 设计的几个关键决策点：

- **解码策略**：整流流解码器（RF）相比前馈解码器（FF）在生成任务上 FID 显著更低（0.032 vs 0.064），同时重建 sJPE 也更低（0.385 vs 0.512），直接验证了迭代连续解码相对于一步式解码的优势。

- **条件投影方法**：提出的 Stack & Unstack 投影在生成 FID（0.032）上优于简单的上卷积投影（0.039）和重复+线性投影（0.038），尽管后两者在重建指标上表现类似。这表明 Stack & Unstack 方法具有更强的泛化能力，可能得益于其更好地保持了帧级时间对应关系。

- **训练策略**：使用滑动窗口（windowed segments）训练比使用全序列（full sequences）的生成 FID 更低（0.032 vs 0.038），且加入注意力机制反而损害性能。这一反直觉发现表明，局部运动片段训练有助于提高第二阶段（令牌预测→解码）的泛化能力，而全局注意力可能引入了对训练分布的有害过拟合。

### 6. 开放问题与未来方向

DisCoRD 开辟了若干值得探索的方向：

1. **解码器与量化器的联合训练**：当前 DisCoRD 将量化器冻结，仅训练解码器。若将整流流解码器与 VQ-VAE 量化器端到端联合训练，可能进一步减少量化误差并提升重建质量。

2. **扩展到全身运动生成**：DisCoRD 目前处理的是身体动作，能否扩展到离散化的面部表情或手部动作生成，从而实现全身一致的自然动作生成，是一个自然的延伸方向。

3. **物理约束的整合**：整流流解码器在连续空间中运行，理论上可以方便地引入物理约束（如足部接触、平衡条件），进一步提升动作的真实性和物理合理性。

4. **sJPE 的无参考推广**：当前 sJPE 需要真实运动 jerk 作为参考。能否将其推广为一种无需参考动作的生成质量评估指标，用于实时反馈或强化学习奖励，是一个有实际价值的开放问题。

5. **更大规模数据上的验证**：在 AMASS 等更大规模、更多样化的混合运动数据集上，DisCoRD 是否仍能保持优势，有待进一步验证。



## 原文 PDF

![[paperPDFs/ICCV_2025/DisCoRD_Discrete_Tokens_to_Continuous_Motion_via_Rectified_Flow_Decoding.pdf]]
