---
title: "VITA: Vision-to-Action Flow Matching Policy"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/VITA_Vision_to_Action_Flow_Matching_Policy.pdf
project_link: https://ucd-dare.github.io/VITA/
code_link: null
openreview_forum_id: BTe5VLBjPg
aliases:
- VITA
tags:
- ICLR_2026
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/representation_learning
core_operator: "VITA 直接从视觉潜在表示流向潜在动作，消除了噪声先验和条件化模块，从而减少复杂性和计算开销。"
primary_logic: "通过联合训练动作自编码器来创建一个与视觉潜在空间对齐的结构化潜在动作空间，并引入流潜在解码（FLD）损失在训练期间通过 ODE 求解步骤反向传播动作重建误差，从而弥合训练-推理差距并防止潜在空间塌缩。"
claims:
- "VITA 是一个无噪声、无条件化的流匹配策略，直接由视觉表示流向潜在动作"
- "VITA 比具有类似模型大小的传统流匹配基线快 1.5×-2×，内存减少 18.6%-28.7%"
- "没有 FLD 损失，模型由于潜在塌缩而完全无法学习"
- "Inference Latency (Vector-based) 上 Latency (ms/chunk, batch size 1) = 0.2215"
---

# VITA: Vision-to-Action Flow Matching Policy

> [!tip] 核心洞察
> 通过联合训练动作自编码器来创建一个与视觉潜在空间对齐的结构化潜在动作空间，并引入流潜在解码（FLD）损失在训练期间通过 ODE 求解步骤反向传播动作重建误差，从而弥合训练-推理差距并防止潜在空间塌缩。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | VITA：从视觉到动作的流匹配策略 |
| 英文题名 | VITA: Vision-to-Action Flow Matching Policy |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=BTe5VLBjPg) · [Project](https://ucd-dare.github.io/VITA/) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/representation_learning |
| Method | VITA |
| Dataset | Inference Latency (Vector-based), Inference Memory (Vector-based), Inference Latency (Grid-based), StoreDrawer OOD (4 unseen objects) |

> [!tip] 效果简介
> - Inference Latency (Vector-based) 上，Latency (ms/chunk, batch size 1) 为 0.2215，对比 0.3307 (FM Transformer + AdaLN)，变化 -33.0% (-0.1092 ms)。
> - Inference Memory (Vector-based) 上，Peak Memory (MiB) 为 333.86，对比 410.38 (FM Transformer + AdaLN)，变化 -18.6% (-76.52 MiB)。
> - Inference Latency (Grid-based) 上，Latency (ms/chunk, batch size 1) 为 0.2502，对比 0.5083 (FM Transformer + Cross-Attn)，变化 -50.8% (-0.2581 ms)。

## 概要

机器人操作策略学习面临一个关键的实时性瓶颈：传统流匹配与扩散策略在推理时，需从标准噪声分布开始采样，并通过交叉注意力、FiLM 或 AdaLN 等视觉条件化模块在**每一个去噪步骤**中重复注入观察信息。这种设计导致推理延迟高、内存开销大，严重制约了实时控制场景下的部署效率。

本文提出 **VITA**（VIsion-To-Action policy），一种**无噪声、无条件化**的流匹配策略学习框架。其核心思路是直接以视觉潜在表示作为流的起点，流向潜在动作空间，从而从根本上消除对噪声先验和重复条件化模块的依赖。这一思路建立在两个关键设计之上：

1. **结构化潜在动作空间**：通过联合训练动作自编码器，将原始动作映射到与视觉潜在空间对齐的高维结构化空间，使视觉-动作之间的流匹配成为可能。
2. **流潜在解码（Flow Latent Decoding, FLD）**：在训练期间通过 ODE 求解步骤反向传播动作重建误差，弥合训练-推理之间的分布差距，并有效防止潜在空间塌缩。

VITA 在 9 项仿真任务和 5 项真实世界任务上进行了评估，涵盖双手（AV-ALOHA）与单臂（ALOHA）操作场景。与同等模型规模的流匹配基线相比，VITA 的推理速度提升 **1.5×–2×**，内存占用降低 **18.6%–28.7%**，同时在 7/9 的仿真任务上取得了最高成功率。消融实验进一步表明，移除 FLD 损失将导致潜在空间完全塌缩，成功率骤降至 0%，验证了该设计的决定性作用。

机器人操作任务要求策略模型能够根据高维视觉观察实时生成精确的动作序列。近年来，扩散策略（**Diffusion Policy**，Chi et al., 2023）和流匹配策略（**Flow Matching Policy**，Zhang & Gienger, 2024）在这一领域取得了显著进展，其核心范式是：从标准高斯噪声分布 $\mathcal{N}(0, I)$ 采样初始状态，通过迭代去噪或流式变换逐步生成动作块，并在每一步通过视觉条件化模块（如交叉注意力、FiLM、AdaLN）注入观察信息。

然而，这一范式存在一个关键瓶颈：**视觉条件化模块需要在每一个去噪或流步骤中重复执行**。对于一个典型的 $N$ 步采样过程，条件化网络被调用 $N$ 次，导致推理延迟和 GPU 内存开销随步数线性增长。在需要毫秒级响应的实时机器人控制场景中，这种冗余计算成为限制策略部署的实质性障碍。实验测量表明，传统流匹配策略在向量表示下的单块推理延迟为 0.33 ms，峰值内存占用超过 410 MiB（Table 1），而扩散策略由于步数更多，开销更为严重。

从根本原因分析，这一瓶颈源于传统方法对**源分布**和**条件化机制**的双重依赖：
- **源分布约束**：标准高斯噪声作为流或扩散的起点，本身不携带任何任务相关信息，因此必须通过外部条件化将视觉信号“注入”生成过程。
- **重复条件化**：由于噪声初始状态与目标动作之间缺乏语义对齐，条件化模块需要在每一步重新编码视觉特征以引导生成方向，形成“噪声→条件化→去噪→条件化→…”的循环。

VITA 的动机正是打破这一循环。其核心洞察是：**如果流的源分布本身就来自视觉编码器，那么视觉信息已经内嵌于流的起点，条件化模块便不再必要**。这一思路将策略从“噪声到动作的条件化生成”重构为“视觉到动作的直接流动”，从而在架构层面消除了重复条件化带来的计算冗余。

## 核心方法与创新机理

VITA 的核心创新在于**从根本上消除了传统流匹配与扩散策略中两个紧密耦合的冗余设计**：标准噪声先验与逐步骤的视觉条件化模块。这一重构并非简单的模块替换，而是通过三个相互依赖的 changed slots 实现的系统性简化，其因果链条可概括为：**视觉潜在即流源 → 消除条件化 → 潜在动作对齐 → 训练-推理鸿沟弥合**。

### 从噪声先验到视觉原生流

传统流匹配策略（如 **Flow Matching Policy**, Zhang & Gienger, 2024）和扩散策略（如 **Diffusion Policy**, Chi et al., 2023）的采样过程遵循同一范式：从标准高斯分布 $\mathcal{N}(0, I)$ 采样噪声，再通过交叉注意力、FiLM 或 AdaLN 等模块在**每一个去噪步骤**注入视觉观察信息，将无意义的噪声逐步塑形为有意义的动作轨迹。

VITA 做了一个看似简单却影响深远的改变：**直接将视觉编码器的潜在表示 $z_0 = E_v(O)$ 作为流的起点**。这意味着流的源分布不再是人为指定的噪声，而是已经蕴含场景与任务信息的视觉特征。由于视觉信息天然存在于源潜在中，速度场网络 $v_\theta(z_t, t)$ 不再需要任何条件化模块——它学习的只是一个无条件化的速度场。这一改变的级联效应是显著的：

- **推理延迟大幅降低**：向量表示下 VITA 每动作块推理仅需 0.22 ms，比同架构的 Transformer + AdaLN 流匹配基线快 1.5 倍；网格表示下快 2 倍（Table 1）。
- **显存占用显著减少**：向量表示下峰值显存降低 18.6%（333.86 MiB vs. 410.38 MiB），网格表示下降低 28.7%（Table 1）。
- **架构选择更灵活**：由于不再需要处理交叉注意力的空间结构，VITA 在向量表示下可以直接使用纯 MLP 架构，而传统 FM 在 MLP 下表现不佳（Figure 11, Appendix B.6.1）。

### 结构化潜在动作空间：维度对齐与联合训练

直接将视觉潜在流向原始动作空间在维度上是不匹配的——视觉编码器输出的潜在维度通常远高于动作维度。VITA 引入了一个**动作自编码器**（Action Autoencoder），将原始动作块 $A \in \mathbb{R}^{T_{\text{pred}} \times D_{\text{action}}}$ 映射到与视觉潜在同维度的结构化潜在动作空间 $z_1 = E_a(A)$。

这一设计的精妙之处在于**联合训练**而非分阶段训练。消融实验表明，冻结预训练的动作自编码器会导致成功率急剧下降和动作 MSE 飙升（Figure 8），因为冻结的自编码器无法与流匹配网络协同演化出一个真正对齐的共享潜在空间。联合训练使得视觉编码器、动作自编码器和流匹配网络三方在端到端优化中相互适应，最终形成“以动作感知的视觉表示”（Figure 7b）——初始视觉潜在甚至可以直接解码出初步的动作轨迹，ODE 求解器只需进行平滑精炼。

### 流潜在解码：弥合训练-推理鸿沟

上述设计存在一个隐蔽但致命的训练-推理不一致问题：训练时，动作解码器 $D_a$ 接收的是编码器产生的“完美”潜在动作 $z_1$；推理时，它接收的却是 ODE 数值求解生成的近似潜在动作 $\hat{z}_1$。当两者分布出现偏差时，解码器会产生严重错误，甚至导致**潜在空间塌缩**——模型将所有输入映射到同一个无意义的潜在点。

VITA 的解决方案是**流潜在解码（Flow Latent Decoding, FLD）**：

$$\mathcal{L}_{\mathrm{FLD}} = \| \mathcal{D}_a(\hat{z}_1) - A \|$$

其中 $\hat{z}_1 = z_0 + \int_0^1 v_\theta(z_t, t) dt$ 是通过 6 步 Euler ODE 求解器生成的。该损失将动作重建误差通过 ODE 求解步骤反向传播，迫使流匹配网络学习的速度场在数值积分后能生成可被解码器正确还原的潜在动作。

FLD 的必要性是**二元**的：没有 FLD 时，模型完全无法学习，成功率降为 0%（Figure 6, Table 4）。即使使用更轻量的替代方案——流潜在一致性损失（FLC, $\mathcal{L}_{\mathrm{FLC}} = \|\hat{z}_1 - z_1\|$，直接在潜在空间对齐而不经过解码器），模型虽然可以学习但收敛更慢。FLD 与 FLC 的组合达到最佳性能，表明在原始动作空间的强监督信号和在潜在空间的一致性约束是互补的。

### 与基线方法的结构性差异总结

| 设计维度 | 传统 FM/DP | VITA |
|---------|-----------|------|
| 流源分布 | 标准高斯噪声 $\mathcal{N}(0, I)$ | 视觉潜在表示 $z_0 = E_v(O)$ |
| 视觉条件化 | 每步注入（交叉注意力/AdaLN/FiLM） | 无条件化（视觉信息已在源潜在中） |
| 动作目标 | 原始动作块 | 潜在动作（与视觉潜在同维度） |
| 训练-推理一致性 | 存在鸿沟（编码器潜在 vs. ODE 潜在） | FLD 损失通过 ODE 反向传播弥合鸿沟 |

这些 changed slots 并非孤立改进，而是构成了一条完整的因果链：**视觉原生流消除了条件化模块的计算开销，潜在动作空间解决了维度不匹配问题，FLD 则保障了这条简化管线在实际推理时的可靠性**。三者缺一不可——去除任何一个都会导致系统失效或性能严重退化。


VITA 的整体 pipeline 围绕一个核心设计展开：**将视觉潜在表示直接作为流匹配的源分布**，从而消除传统扩散/流匹配策略中必需的噪声先验和逐步骤视觉条件化模块。整个框架由三个主要组件构成，形成一个端到端可训练的视觉到动作映射系统。

### 数据流与模块关系

推理时的数据流遵循线性路径。首先，**视觉编码器** $E_v$ 接收原始观察 $O$（包含图像和本体感知信息），将其编码为源潜在表示 $\mathbf{z}_0 = E_v(O)$。该潜在向量直接作为流匹配 ODE 的初始状态，而非传统方法中的标准高斯噪声样本。

随后，**流匹配网络** $v_\theta$ 在无需任何视觉条件化输入的情况下，学习从 $\mathbf{z}_0$ 到目标潜在动作 $\mathbf{z}_1$ 的连续时间速度场。推理时通过求解 ODE 生成目标潜在动作：

$$\hat{\mathbf{z}}_1 = \mathbf{z}_0 + \int_0^1 v_\theta(\mathbf{z}_t, t) dt$$

其中 $\mathbf{z}_t = (1-t)\mathbf{z}_0 + t\mathbf{z}_1$ 为线性插值路径。论文使用基于最优传输的 OT-CFM 变体，并采用 6 步 Euler 求解器进行数值积分。

最后，**动作解码器** $D_a$ 将 ODE 生成的潜在动作 $\hat{\mathbf{z}}_1$ 解码为原始动作块 $A$，完成从视觉观察到可执行动作的端到端映射。

### 训练时的闭环设计

训练阶段引入额外的**动作编码器** $E_a$，将真实动作块编码为目标潜在动作 $\mathbf{z}_1 = E_a(A)$，为流匹配网络提供监督信号。训练损失由三项加权组成：

$$\mathcal{L}_{\mathrm{VITA}} = \lambda_{\mathrm{FM}} \mathcal{L}_{\mathrm{FM}} + \lambda_{\mathrm{FLD}} \mathcal{L}_{\mathrm{FLD}} + \lambda_{\mathrm{AE}} \mathcal{L}_{\mathrm{AE}}$$

其中 $\mathcal{L}_{\mathrm{FM}}$ 为标准的流匹配损失，训练速度场预测线性插值的真实速度。$\mathcal{L}_{\mathrm{AE}}$ 为动作自编码器的重建损失，使用编码器产生的 $\mathbf{z}_1$ 经解码器重建动作。关键在于 $\mathcal{L}_{\mathrm{FLD}}$（流潜在解码损失），它使用 ODE 求解器生成的 $\hat{\mathbf{z}}_1$ 而非编码器产生的 $\mathbf{z}_1$ 来计算动作重建误差：

$$\mathcal{L}_{\mathrm{FLD}} = \| D_a(\hat{z}_1) - A \|$$

这一设计弥合了训练-推理差距：训练时动作解码器必须学会从 ODE 生成的潜在动作中重建动作，而非仅依赖编码器提供的“完美”潜在表示。消融实验表明，**移除 FLD 损失会导致潜在空间塌缩，模型完全无法学习**（成功率降为 0%），验证了该模块的关键作用。

### 与传统方法的本质差异

传统流匹配/扩散策略的核心瓶颈在于：每个去噪步骤都需要通过交叉注意力、FiLM 或 AdaLN 等模块重新注入视觉条件信息（见 Figure 7a）。这导致推理延迟和内存开销与 ODE 求解步数线性增长。

VITA 通过将视觉信息直接编码为流的源分布 $\mathbf{z}_0$，从根本上切断了这一依赖（见 Figure 7b）。流匹配网络 $v_\theta(\mathbf{z}_t, t)$ 仅以当前潜在状态和时间步为输入，完全不需要额外的条件化模块。这使得 VITA 在向量表示下可采用纯 MLP 架构实现流匹配网络，在网格表示下虽仍需 Transformer 但可移除交叉注意力模块，从而实现 1.5×–2× 的推理加速和 18.6%–28.7% 的显存节省。

值得注意的是，端到端优化会促使视觉编码器学习以动作为中心的视觉表示，使其与潜在动作空间对齐。因此，初始视觉潜在向量甚至可以直接解码为初步的动作轨迹，ODE 求解器再对其进行平滑精炼，最终生成精确动作。

### 3.1 流匹配基础

VITA 基于连续归一化流（Continuous Normalizing Flow）框架。给定源分布样本 $\mathbf{z}_0$ 和目标分布样本 $\mathbf{z}_1$，定义线性插值路径：

$$\mathbf{z}_t = (1 - t)\mathbf{z}_0 + t\mathbf{z}_1, \quad t \in [0, 1]$$

该路径对应的真实速度场为 $(\mathbf{z}_1 - \mathbf{z}_0)$。流匹配网络 $v_{\theta}(\mathbf{z}_t, t)$ 通过最小化以下损失来学习该速度场：

$$\mathcal{L}_{\mathrm{FM}} = \mathbb{E}_{t, \mathbf{z}_0, \mathbf{z}_1} \left[ \left\| v_{\theta}(\mathbf{z}_t, t) - (\mathbf{z}_1 - \mathbf{z}_0) \right\|^2 \right]$$

训练完成后，推理时通过求解常微分方程（ODE）从源样本生成目标样本：

$$\hat{\mathbf{z}}_1 = \mathbf{z}_0 + \int_0^1 v_{\theta}(\mathbf{z}_t, t) \, dt$$

VITA 采用基于最优传输的 OT-CFM（Tong et al., 2023a），并使用 6 步线性插值时间步的 Euler 求解器进行数值积分。

### 3.2 核心架构模块

VITA 由三个核心组件构成（Figure 2），其关键创新在于**消除噪声先验和条件化模块**，直接从视觉潜在表示流向潜在动作。

#### 视觉编码器（Vision Encoder, $E_v$）

将原始观察 $O$（图像 + 本体感）编码为源潜在表示 $\mathbf{z}_0 = E_v(O)$，作为流匹配的起点。VITA 使用 ResNet-18 作为视觉编码器。与传统方法的关键区别在于：**$\mathbf{z}_0$ 直接作为流的源分布，而非从标准高斯噪声 $\mathcal{N}(0, I)$ 采样**，从而将视觉信息隐式注入流的初始状态，消除了每步重复注入视觉条件的需求。

#### 动作自编码器（Action Autoencoder）

动作自编码器由动作编码器 $E_a$ 和动作解码器 $D_a$ 组成，其核心作用是将原始动作块 $A \in \mathbb{R}^{T_{\text{pred}} \times D_{\text{action}}}$ 映射到与视觉潜在空间同维度的结构化潜在动作空间：

- **动作编码器** $E_a$：将真实动作块 $A$ 编码为目标潜在表示 $\mathbf{z}_1 = E_a(A)$，为流匹配训练提供目标
- **动作解码器** $D_a$：将潜在动作解码回原始动作空间 $\hat{A} = D_a(\hat{\mathbf{z}}_1)$

动作自编码器通过联合训练与流匹配网络协同优化，使潜在动作空间与视觉潜在空间对齐。消融实验表明，冻结预训练的自编码器会导致成功率显著下降和动作 MSE 升高（Figure 8），证明联合训练对于空间对齐至关重要。

#### 流匹配网络（Flow Matching Network, $v_{\theta}$）

流匹配网络学习无条件化的速度场 $v_{\theta}(\mathbf{z}_t, t)$，定义从 $\mathbf{z}_0$ 到 $\mathbf{z}_1$ 的连续时间流。与传统方法（如 **Flow Matching Policy**（Zhang & Gienger, 2024）使用 AdaLN 条件化、**Diffusion Policy**（Chi et al., 2023）使用 FiLM 条件化）不同，VITA 的速度场**不接收任何视觉条件输入**，因为视觉信息已包含在源潜在 $\mathbf{z}_0$ 中。这一设计消除了条件化模块的参数开销和每步计算成本。

在向量表示场景下，VITA 可使用纯 MLP 架构实现流匹配网络，而传统 FM 在 MLP 架构下性能不佳（Figure 11），进一步验证了无条件化设计的优势。

### 3.3 流潜在解码（Flow Latent Decoding, FLD）

训练-推理差距是 VITA 面临的核心挑战：训练时动作解码器 $D_a$ 接收编码器生成的 $\mathbf{z}_1$，而推理时接收 ODE 求解器生成的 $\hat{\mathbf{z}}_1$。若不加约束，模型会因潜在空间塌缩而完全无法学习（Figure 5, Figure 6）。

FLD 通过将动作重建误差沿 ODE 求解步骤反向传播来弥合这一差距：

$$\mathcal{L}_{\mathrm{FLD}} = \| D_a(\hat{\mathbf{z}}_1) - A \|$$

其中 $\hat{\mathbf{z}}_1 = \mathbf{z}_0 + \int_0^1 v_{\theta}(\mathbf{z}_t, t) \, dt$ 是通过 ODE 求解器生成的潜在动作。FLD 强制解码器在训练期间适应 ODE 生成的质量，从而锚定潜在生成过程。

作为 FLD 的轻量替代，VITA 还引入了**流潜在一致性（Flow Latent Consistency, FLC）**损失，直接在潜在空间对齐 ODE 生成和编码器生成的潜在表示：

$$\mathcal{L}_{\mathrm{FLC}} = \| \hat{\mathbf{z}}_1 - \bar{\mathbf{z}}_1 \|$$

其中 $\bar{\mathbf{z}}_1$ 表示停止梯度的编码器潜在表示。FLC 提供较弱的信号，收敛略慢于 FLD，但两者结合可取得最佳性能（Figure 6）。

### 3.4 总训练目标

VITA 的总训练损失为三个损失的加权和：

$$\mathcal{L}_{\mathrm{VITA}} = \lambda_{\mathrm{FM}} \mathcal{L}_{\mathrm{FM}} + \lambda_{\mathrm{FLD}} \mathcal{L}_{\mathrm{FLD}} + \lambda_{\mathrm{AE}} \mathcal{L}_{\mathrm{AE}}$$

其中 $\mathcal{L}_{\mathrm{AE}}$ 为标准动作自编码器重建损失 $\| D_a(\mathbf{z}_1) - A \|$，$\lambda_{\mathrm{FM}}$、$\lambda_{\mathrm{FLD}}$、$\lambda_{\mathrm{AE}}$ 为各损失项的权重系数。消融实验确认，移除 FLD 损失（即仅使用 $\mathcal{L}_{\mathrm{FM}} + \mathcal{L}_{\mathrm{AE}}$）会导致潜在空间塌缩，成功率为 0%（Table 4, Figure 6），证明 FLD 是 VITA 有效训练的必要条件。

## 实验与关键发现

### 核心瓶颈与设计动机

传统流匹配和扩散策略（如 **Flow Matching Policy** (Zhang & Gienger, 2024)、**Diffusion Policy** (Chi et al., 2023)）在推理时存在一个根本性瓶颈：它们必须从标准噪声分布开始采样，并在每一个去噪步骤中通过条件化模块（交叉注意力、FiLM、AdaLN）重复注入视觉观察信息。这些条件化模块在每一步都需要执行，导致较高的推理延迟和显存开销，严重限制了实时机器人控制的可行性。

VITA 的设计动机直指这一瓶颈：它直接从视觉潜在表示流向潜在动作，完全消除了噪声先验和条件化模块，从而在架构层面减少了复杂性和计算开销。这一设计选择的核心洞察在于——通过联合训练动作自编码器来创建一个与视觉潜在空间对齐的结构化潜在动作空间，并引入流潜在解码（FLD）损失在训练期间通过 ODE 求解步骤反向传播动作重建误差，从而弥合训练-推理差距并防止潜在空间塌缩。

### 推理效率：延迟与显存

Table 1 报告了 VITA 与流匹配基线在推理效率上的对比。在基于向量的视觉潜在表示下，VITA 的推理延迟为 0.2215 ms/chunk（batch size 1），而使用 Transformer + AdaLN 条件化的 FM 基线为 0.3307 ms/chunk，VITA 快了约 33%（1.5×）。在基于网格的表示下，VITA 的延迟为 0.2502 ms/chunk，而使用 Transformer + 交叉注意力的 FM 基线为 0.5083 ms/chunk，VITA 快了约 51%（2×）。

![[assets/figures/papers/paper_list_l47_https_openreview_net_forum_id_BTe5VLBjPg/figures/011_Table_1.jpg]]
*Table 1: Comparison of the time and space efficiency of VITA and flow-matching baselines, grouped by the type of visual latents used (“Vector” or “Grid” based). Metrics include: model size, inference latency (ms/chunk, batch size 1), and inference memory (MiB), (see Appendix B.7.2 for inference memory measurement details)*

在显存占用方面，VITA 同样展现出显著优势：基于向量的 VITA 峰值显存为 333.86 MiB，比 FM 基线（410.38 MiB）减少了 18.6%；基于网格的 VITA 峰值显存为 377.55 MiB，比 FM 基线减少了 28.7%。这些效率提升直接源于 VITA 消除了条件化模块——Table 5 显示 VITA 的条件化参数开销为零，而 FM 基线需要额外的条件化参数（向量表示下为 0.18M–0.22M，网格表示下为 0.16M–0.23M）。

![[assets/figures/papers/paper_list_l47_https_openreview_net_forum_id_BTe5VLBjPg/figures/030_Table_5.jpg]]
*Table 5: Comparison of the conditioning parameter overhead, training-time cost, and training-time memory usage of VITA and baselines, grouped by the type of visual latents used (“Vector” or “Grid” based). Metrics include (i) parameters introduced solely by conditioning modules, (ii) training time per chunk (ms), and (iii) peak GPU memory during training (MiB)*

值得注意的是，VITA 使用 MLP-only 架构即可在向量表示上取得有竞争力的性能（Figure 11），而 MLP-only 的 FM 在 PushT 任务上性能不佳，这表明 VITA 的架构选择降低了对复杂网络结构的依赖。

### 模拟任务成功率

Table 2 报告了 VITA 与 FM、Diffusion Policy（DP）和 Action Chunking Transformer（ACT）在 9 个模拟任务上的成功率对比。VITA 在 7/9 个任务上取得了最高或并列最高的成功率，具体表现为：

- **AV-ALOHA 任务**：在 CubeTransfer（100%）、SlotInsertion（95.33%）、HookPackage（96.67%）、PourTestTube（88.33%）和 ThreadNeedle（91.33%）上，VITA 均优于或持平 FM 和 DP。其中 ThreadNeedle 任务要求毫米级精度的穿针操作，VITA 的 91.33% 成功率显著高于 FM（85.33%）和 DP（78.67%）。
- **Robomimic 任务**：在 Square（100%）和 Can（100%）上，VITA 取得了满分，与 FM 持平，优于 DP 和 ACT。
- **PushT 和 CloseBox**：VITA 在 PushT 上取得 88.00%，略低于 FM（90.33%）；在 CloseBox 上取得 94.00%，与 FM（93.33%）基本持平。

需要指出的是，VITA 和 FM 训练 25K-50K 步，而 DP 训练 100K 步、ACT 训练 100K-200K 步，因为 VITA/FM 收敛更快。报告的是最佳验证成功率，这可能使比较偏向 VITA/FM，但反映了流匹配方法在样本效率上的优势。

### 真实世界任务成功率

Table 3 报告了 VITA 在三个真实世界单臂 ALOHA 任务上的成功率，并与 FM、DP 和 ACT 进行了对比。每个任务被分解为子任务：

![[assets/figures/papers/paper_list_l47_https_openreview_net_forum_id_BTe5VLBjPg/figures/013_Table_3.jpg]]
*Table 3: Comparison of SRs on three real-world single-arm ALOHA manipulation tasks. Each task is decomposed into subtasks, and SRs are reported per subtask*

- **PickBall**：VITA 在 Pick 子任务上取得 0.85，低于 DP（1.00）和 FM（1.00），但在 Place 子任务上取得 0.85，优于 DP（0.80）。VITA 在在线扰动下展现了实时调整能力（Figure 19），在抓取前多次移动球、抓取后多次移动盒子的情况下，机械臂仍能成功调整到正确位置。
- **StoreDrawer**：VITA 在 Pick 子任务上取得 1.00（与 DP 持平），在 Place 子任务上取得 0.90（与 DP 持平），在 Close 子任务上取得 0.85（略低于 DP 的 0.90）。
- **ToothBrush**：VITA 在 Pick 子任务上取得 0.85，低于 FM（1.00）和 DP（0.95）；在 Place 子任务上取得 0.85，与 DP 持平，低于 FM（1.00）。

Table 7 报告了 VITA 在两个真实世界双手 AV-ALOHA 任务（使用主动视觉）上的成功率。在 HiddenPick 任务中，VITA 在 Reveal 子任务上取得 0.85，在 Pick 和 Place 子任务上均取得 0.80。在 TransferFromBox 任务中，VITA 在 Reveal 和 Pick 子任务上均取得 1.00，但在 Place 子任务上仅取得 0.40，表明在精确放置方面仍有改进空间。

### OOD 泛化能力

Table 8 报告了在 StoreDrawer 任务上使用四个未见过的物体（包括三棱柱和星形块）进行 OOD 评估的结果。VITA 和 DP 在四个物体上均取得了 4/4 的成功率，FM 取得 3/4，ACT 取得 2/4。这表明 VITA 的视觉-动作流在分布外物体上保持了良好的泛化能力，与 DP 相当。

### 消融实验

#### 流潜在解码（FLD）的关键作用

FLD 是 VITA 训练中最为关键的组件。Figure 6 和 Table 4 显示，移除 FLD 后模型完全无法学习（成功率为 0%），原因是潜在空间塌缩——动作自编码器在没有 FLD 约束的情况下，会将不同的动作映射到相同的潜在表示，导致解码器无法区分。Figure 5 直观展示了这一现象：无 FLD 时重建的动作与真实动作完全不一致。

![[assets/figures/papers/paper_list_l47_https_openreview_net_forum_id_BTe5VLBjPg/figures/020_Table_4.jpg]]
*Table 4: Task SR (%) on ThreadNeedle with different action up-sampling strategies*

![[assets/figures/papers/paper_list_l47_https_openreview_net_forum_id_BTe5VLBjPg/figures/016_Figure_6.jpg]]
*Figure 6: Success rates using different objectives*

流潜在一致性（FLC）作为 FLD 的轻量替代方案，通过直接对齐 ODE 生成的潜在和编码器生成的潜在来提供训练信号。Figure 6 显示 FLC 可以学习但收敛速度略慢，将 FLD 和 FLC 结合使用可获得最佳性能。

从公式层面，FLD 定义为：

$$\mathcal{L}_{\mathrm{FLD}} = \| \mathcal{D}_a(\hat{z}_1) - A \|$$

其中 $\hat{z}_1$ 是通过 ODE 求解生成的潜在动作，$A$ 是真实动作。这一损失通过 ODE 求解步骤反向传播梯度，迫使流匹配网络学习生成可被解码器准确重建的潜在表示。

#### 联合训练 vs. 冻结动作自编码器

Figure 8 对比了端到端联合训练 VITA 与使用冻结预训练动作自编码器的 VITA 在 ThreadNeedle 任务上的表现。冻结 AE 导致成功率显著下降且动作 MSE 较高，表明动作自编码器需要与流匹配网络联合优化，才能在视觉潜在和动作潜在之间建立有效的对齐。

#### 对比损失的辅助作用

Figure 9 显示，单独使用对比损失不足以学习有效策略（性能远低于 FLD），但当对比损失与 FLD/FLC 结合时，可以带来额外的性能提升。这表明对比损失作为辅助信号有助于增强视觉-动作潜在空间的对齐，但不能替代 FLD 提供的精确重建约束。

#### MLP-only 架构的可行性

Figure 11 展示了在 PushT 任务上 MLP-only VITA 与 MLP-only FM 的对比。MLP-only VITA 取得了与 Transformer 实现相当的成功率，而 MLP-only FM 由于缺乏精度，在线性能不佳。这进一步验证了 VITA 的架构设计降低了对复杂网络结构的依赖——因为在 VITA 中，视觉信息已经包含在源潜在中，不需要复杂的条件化机制来融合多模态信息。

### 失败模式分析

1. **极端效率与精度的权衡**：一步生成方法（如 MeanFlow）在 PushT 上可将推理速度提升约 2 倍，但成功率从 88% 下降到 74%，表明在追求极致推理速度时需要接受一定的精度损失。

2. **精确放置的挑战**：在 TransferFromBox 真实世界任务中，VITA 在 Place 子任务上仅取得 0.40 的成功率（Table 7），说明在需要高精度放置的场景下，VITA 仍存在改进空间。类似地，DP 在 ThreadNeedle 任务上可能完成大部分子任务，但最终因毫米级误差而插入失败（Figure 14）。

3. **数据依赖性**：动作自编码器的训练依赖于一定规模的动作数据，在数据极度稀疏或动作结构不清晰时，学习可靠的潜在空间可能困难。当前实验主要在中等规模数据集上进行（Table 6），尚未在更大规模、更多样的机器人控制任务上全面验证。

![[assets/figures/papers/paper_list_l47_https_openreview_net_forum_id_BTe5VLBjPg/figures/038_Table_6.jpg]]
*Table 6: Comparison of dataset specifications*

### 效率-性能权衡总结

VITA 在推理效率上取得了显著优势（1.5×-2× 加速，18.6%-28.7% 显存节省），同时在大多数模拟和真实世界任务上保持了与最强基线相当或更优的成功率。这一效率-性能权衡的关键在于 VITA 从根本上消除了条件化模块的重复计算，同时通过 FLD 损失确保了潜在空间的结构化，防止了训练-推理差距导致的性能退化。

## 定位与知识库关联

### 1. 与流匹配和扩散策略的关系

VITA 直接建立在流匹配（flow matching）的连续归一化流框架之上，但其核心设计选择与现有工作形成了系统性差异。传统流匹配策略（如 **FM Policy**, Zhang & Gienger, 2024）和扩散策略（如 **Diffusion Policy**, Chi et al., 2023）共享一个基本范式：从标准高斯噪声 $\mathcal{N}(0, I)$ 开始采样，并在每一个去噪/积分步骤中通过条件化模块（交叉注意力、FiLM、AdaLN）注入视觉观察信息。这一范式带来了两个瓶颈：① 噪声先验与动作分布之间的结构性不匹配，导致需要更多的采样步骤和更深的网络来逐步“塑造”动作轨迹；② 每一步条件化模块的重复执行带来了显著的推理延迟和内存开销。

VITA 的突破在于切断了这两个瓶颈的根源——它直接用视觉编码器的潜在表示 $z_0 = E_v(O)$ 替代标准高斯噪声作为流的源分布，从而将视觉条件化的信息“折叠”进流的初始状态，消除了对每步条件化模块的需求。这一设计使得 VITA 学习的是一个无条件化的速度场 $v_\theta(z_t, t)$，而传统方法学习的是条件化速度场 $v_\theta(z_t, t, c)$，其中 $c$ 是视觉条件。从信息论角度看，VITA 将“视觉到动作”的映射问题重新表述为“视觉潜在到动作潜在”的传输问题，而非“噪声到动作”的条件生成问题。

在架构层面，这一差异带来了级联的简化：当使用向量化视觉表示时，VITA 的流匹配网络可以退化为纯 MLP 架构，而传统 FM 在相同架构下性能显著下降（Figure 11，附录 B.6.1）。这表明传统方法的条件化模块不仅是效率负担，也是架构表达力的结构性依赖——它们承担了将噪声逐步“翻译”为有意义动作轨迹的功能，而 VITA 通过改变源分布本身，将这一负担转移到了视觉编码器的表示学习上。

### 2. 与动作分块策略的关系

VITA 继承了 **Action Chunking Transformer** (ACT, Zhao et al., 2023) 的动作分块思想——预测未来 $T_{\text{pred}}$ 步的动作序列而非单步动作，以提升时间一致性和执行稳定性。但两者的生成机制有本质区别：ACT 基于 CVAE 框架，通过条件变分自编码器从视觉观察中采样潜在变量再解码为动作块；VITA 则通过流匹配的 ODE 求解过程，从视觉潜在确定性地流向动作潜在，再解码为动作块。这一差异意味着 VITA 避免了 CVAE 中常见的后验塌缩（posterior collapse）问题，同时保留了多步动作预测的时间平滑性优势。

值得注意的是，VITA 在训练步数上显著少于 ACT 和 Diffusion Policy（VITA/FM 训练 25K-50K 步 vs. DP 100K 步、ACT 100K-200K 步），但仍能在多数任务上取得相当或更优的成功率。这暗示流匹配框架本身比扩散模型和 CVAE 具有更高的样本效率，而 VITA 的无条件化设计进一步加速了这一收敛过程。

### 3. 核心创新：流潜在解码与训练-推理鸿沟的弥合

VITA 最具原创性的技术贡献是**流潜在解码（Flow Latent Decoding, FLD）**损失。这一设计的动机源于一个关键的训练-推理不一致问题：在训练时，动作解码器 $D_a$ 接收的是动作编码器产生的“干净”潜在 $z_1 = E_a(A)$；但在推理时，解码器接收的是 ODE 求解器生成的近似潜在 $\hat{z}_1$。如果仅在 $z_1$ 上训练解码器（标准 AE 损失），模型会在推理时遭遇分布偏移，导致潜在空间塌缩——解码器将所有输入映射到平凡解（如零动作或均值动作）。

FLD 通过在训练期间显式地执行 ODE 求解步骤，并将 $\hat{z}_1$ 的解码结果与真实动作 $A$ 之间的重建误差反向传播通过整个 ODE 求解链，强制模型学习一个“对 ODE 误差鲁棒”的潜在空间。消融实验（Figure 6, Table 4）提供了决定性证据：没有 FLD 时，模型成功率降为 0%，完全无法学习。这一定量结果与定性可视化（Figure 5）一致——无 FLD 时重建的动作轨迹完全塌缩。

FLD 的设计可以理解为一种“端到端对齐”策略：它不仅要求动作自编码器能重建动作（AE 损失），还要求流匹配网络生成的潜在能被解码器正确解释（FLD 损失），从而将视觉编码器、流匹配网络和动作解码器联合优化为一个一致的传输系统。与之对比，**流潜在一致性（Flow Latent Consistency, FLC）**损失仅要求在潜在空间中对齐 $\hat{z}_1$ 和 $z_1$，信号更弱，收敛更慢，但计算开销更小。两者结合可在收敛速度和最终性能之间取得最佳平衡。

### 4. 适用边界与局限

**适用场景**：VITA 特别适合对推理延迟和内存敏感的实时机器人控制场景，尤其是在边缘设备上部署时。其在向量化表示下可使用纯 MLP 架构的特性，进一步降低了硬件要求。实验覆盖了双手协调操作（AV-ALOHA）、单臂操作（ALOHA）、以及 Robomimic 等已建立的基准，表明其对不同操作模式和精度要求（如穿针任务需要毫米级精度）具有广泛的适用性。

**已知局限**：

1. **速度-精度权衡**：一步生成方法（如 MeanFlow）可将推理速度再提升约 2 倍，但在 PushT 任务上成功率从 88% 下降到 74%，表明极端效率与动作精度之间存在尚未解决的张力。

2. **动作自编码器的数据依赖**：联合训练动作自编码器依赖于一定规模和结构清晰的动作数据。消融实验（Figure 8）显示，冻结预训练自编码器会导致成功率和动作 MSE 显著恶化，说明视觉-动作潜在空间的对齐需要端到端联合优化，这可能限制其在数据稀疏场景下的直接迁移。

3. **模态覆盖范围**：当前 VITA 主要使用单视图或多视图 RGB 图像（AV-ALOHA 使用左眼图像，单臂任务使用手腕与俯视相机），尚未验证在触觉、深度、力觉等额外模态下的有效性。多模态融合是否会破坏潜在空间的结构化对齐，仍是开放问题。

4. **空间信息处理的架构依赖**：在需要保留空间结构的网格表示下，VITA 仍需使用 Transformer 架构（虽然消除了交叉注意力模块），无法完全退化为 MLP。这意味着对于高度依赖空间推理的任务（如复杂场景中的物体定位），VITA 的效率优势可能部分减弱。

5. **任务规模验证**：实验主要在 ALOHA 和 Robomimic 等中等规模任务上进行，尚未在更大规模、更多样的机器人控制任务（如灵巧手操作、全身控制、长时程任务）上全面验证。

### 5. 开放问题与未来方向

1. **跨具身与跨任务泛化**：VITA 的视觉-动作潜在空间对齐机制是否支持从人类演示中学习或跨机器人平台迁移？这需要验证视觉编码器是否能学习具身无关的表示，以及动作自编码器是否能适应不同形态的动作空间。

2. **与强化学习的结合**：当前 VITA 是纯模仿学习方法，如何将其与在线强化学习或自适应控制结合，以增强在分布外场景下的鲁棒性，是一个自然的研究方向。流匹配框架的概率特性可能为探索-利用权衡提供新的视角。

3. **一步生成的精度保持**：如何在保持 VITA 高精度的同时实现一步生成的最快推理，是效率优化的核心问题。可能需要探索新的蒸馏策略或特殊设计的 ODE 路径。

4. **更高维动作空间的扩展**：将 VITA 扩展到灵巧手操作或全身控制等高维动作空间时，动作自编码器的压缩率和重建精度之间的平衡需要重新审视，FLD 损失的梯度传播路径也可能需要调整。

5. **多模态融合的架构设计**：如何在保持无条件化流匹配优势的同时有效融合触觉、深度等额外模态，而不重新引入条件化模块的开销，是一个架构设计挑战。

## 原文 PDF

![[paperPDFs/ICLR_2026/VITA_Vision_to_Action_Flow_Matching_Policy.pdf]]
