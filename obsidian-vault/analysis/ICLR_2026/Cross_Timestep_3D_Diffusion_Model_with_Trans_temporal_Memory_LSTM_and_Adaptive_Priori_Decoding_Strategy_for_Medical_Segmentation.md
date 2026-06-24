---
title: "Cross-Timestep: 3D Diffusion Model with Trans-temporal Memory LSTM and Adaptive Priori Decoding Strategy for Medical Segmentation"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Cross_Timestep_3D_Diffusion_Model_with_Trans_temporal_Memory_LSTM_and_Adaptive_Priori_Decoding_Strategy_for_Medical_Segmentation.pdf
openreview_forum_id: TE3asYO8PQ
aliases:
- CT
- Cross-Timestep
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/segmentation
core_operator: "引入时间衰减的结构先验（APDS）和跨时间步循环记忆单元（tLSTM），以在高噪阶段提供强指导并在后续步中积累和细化证据。"
primary_logic: "通过自适应先验解码策略（APDS）在早期提供强先验并随时间衰减，同时利用跨时间步记忆LSTM（tLSTM）保持状态，使去噪过程逐步细化而非重新发现结构，从而稳定3D扩散模型的分割。"
claims:
- "APDS防止了从随机噪声开始的反向扩散崩溃。"
- "tLSTM的跨时间步记忆显著提高了分割性能和时间一致性。"
- "Cross-Timestep在多个异构3D医学数据集上均取得优于现有方法的性能。"
- "消融实验验证了tLSTM的t-cell组件和APDS各自对性能的贡献。"
---

# Cross-Timestep: 3D Diffusion Model with Trans-temporal Memory LSTM and Adaptive Priori Decoding Strategy for Medical Segmentation

> [!tip] 核心洞察
> 通过自适应先验解码策略（APDS）在早期提供强先验并随时间衰减，同时利用跨时间步记忆LSTM（tLSTM）保持状态，使去噪过程逐步细化而非重新发现结构，从而稳定3D扩散模型的分割。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 跨时间步：具有跨时空记忆LSTM和自适应先验解码策略的3D扩散模型用于医学分割 |
| 英文题名 | Cross-Timestep: 3D Diffusion Model with Trans-temporal Memory LSTM and Adaptive Priori Decoding Strategy for Medical Segmentation |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=TE3asYO8PQ) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/segmentation |
| Method | Cross-Timestep |
| Dataset | LNCTVSeg, OASeg |

> [!tip] 效果简介
> - LNCTVSeg 上，Dice 为 83.7，对比 Diff-UNet (best prior method, exact value not provided)，变化 未知。
> - OASeg 上，Dice 为 72.8，对比 Diff-UNet (best prior method, exact value not provided)，变化 未知。

## 概述

**核心问题：3D扩散模型在高噪时间步的结构崩溃。** 现有的3D扩散分割模型在反向扩散的初始阶段（高噪声时间步，$t$接近$T$）会遭遇“初始阶段崩溃”（Initial-stage collapse）现象——当从纯随机噪声开始采样时，模型无法恢复目标结构，导致分割完全失败。其根本原因在于，高噪阶段缺乏有效的结构先验且各时间步独立去噪，无法积累跨步证据来逐步构建目标形态。

**核心方法：Cross-Timestep框架。** 针对上述瓶颈，本文提出了两个关键调控机制：(1) **自适应先验解码策略（APDS）**，通过一个独立于主去噪分支的先验解码器生成结构先验掩码，并以时间衰减权重$\omega_t$将其注入主分支，在高噪阶段提供强引导、在低噪阶段逐步退让；(2) **跨时间步记忆LSTM（tLSTM）**，将3D卷积和线性层集成到LSTM/GRU门控结构中，在编码器（FFT-tLSTM、SC-tLSTM）和解码器（SC-tLSTM）中显式维护并传递跨时间步的状态，实现证据的持续积累与细化。

**核心结论：** APDS使扩散模型能够从随机噪声正确启动反向采样，从根本上解决了初始阶段崩溃问题；tLSTM的跨时间步记忆显著提升了分割性能和时间一致性。在LNCTVSeg和OASeg两个异构3D医学分割数据集上，Cross-Timestep均取得了优于现有方法（包括TransBTS、SwinUNETR、Diff-UNet等）的Dice/IoU/HD95指标，消融实验进一步验证了t-cell组件、APDS、SC-tLSTM和FFT-tLSTM各自的独立贡献。

## 背景与动机

### 3D扩散模型在医学分割中的瓶颈

扩散模型在2D图像生成与分割中取得了显著进展，但其向3D医学图像的迁移面临一个根本性障碍：**初始阶段崩溃**（initial-stage collapse）。当反向扩散过程从纯噪声（高噪声时间步）启动时，模型缺乏任何结构先验来引导去噪方向，导致无法恢复目标解剖结构（Figure 1）。这一现象的本质在于，从完全随机的初始状态出发，去噪网络没有可依赖的跨步证据积累机制，每一步的预测都是独立的、缺乏连续性的尝试。

现有基于扩散的3D分割方法（如Diff-UNet）虽然通过条件图像提供了一定引导，但并未从根本上解决高噪阶段的崩溃问题——它们仅在中等或低噪声时间步才能正确采样，这意味着模型实际上无法充分利用扩散模型的完整生成能力。

### 现有方法的两个关键缺口

**缺口一：缺乏时间衰减的结构先验。** 标准扩散模型在反向过程的每一步平等地依赖条件信息，但高噪声阶段对结构引导的需求远强于低噪声阶段。固定强度的条件注入无法适应这种动态需求——要么在早期引导不足导致崩溃，要么在后期引导过强干扰精细结构的恢复。

**缺口二：各时间步独立去噪，缺乏跨步记忆。** 无论是DDPM还是DDIM框架，每个去噪步都是一个无状态的前向计算，隐状态不跨时间步传递。这意味着模型在每个时间步都需要“重新发现”目标结构，无法积累和细化前序步骤中已恢复的证据。对于3D医学数据的高维空间和复杂解剖结构，这种无记忆的去噪方式效率低下且不稳定。

### 本文动机与核心思路

针对上述缺口，本文提出**Cross-Timestep**框架，通过两个核心机制稳定3D扩散分割过程：

1. **自适应先验解码策略（APDS）**：在反向扩散的早期阶段注入强结构先验，并随时间步衰减引导强度，使模型在高噪阶段获得足够的方向性，在低噪阶段享有充分的细化自由度。该策略通过先验解码器（PD）从条件图像生成粗分割掩码，再经时间加权融合机制（RA）将其反向融入主去噪分支。

2. **跨时间步记忆LSTM（tLSTM）**：首次将循环状态记忆引入扩散模型的去噪过程，使隐藏状态和细胞状态显式地跨时间步传递。这一设计将去噪从一系列独立操作转变为一个连贯的证据积累过程——早期步骤恢复的粗粒度结构信息通过tLSTM状态传递给后续步骤，逐步细化为精确的分割结果。

通过这两个机制的协同，Cross-Timestep在多个异构3D医学数据集上展现出优于现有方法的性能，同时保持了可接受的计算开销。

## 核心创新

Cross-Timestep 的核心创新在于通过两个相互协同的机制——**自适应先验解码策略（APDS）**和**跨时间步记忆LSTM（tLSTM）**——从根本上解决了3D扩散模型在医学分割任务中的“初始阶段崩溃”问题。

### 问题根源：初始阶段崩溃

3D扩散模型的反向扩散过程从纯噪声开始。在高噪声时间步（$t$ 接近 $T$，如 $t > 700$），模型缺乏任何结构先验，且无法积累跨步证据，导致去噪轨迹发散，无法恢复目标解剖结构——这一现象被本文定义为“初始阶段崩溃”（Figure 1, Figure 7）。传统扩散模型（如 Diff-UNet）各时间步独立去噪，没有跨步状态传递，在高噪阶段完全依赖随机采样，因此容易崩溃。

### 创新一：APDS——时间衰减的结构先验注入

APDS 的核心思想是**在去噪早期提供强结构先验，并随时间步衰减**，从而稳定反向扩散的初始阶段。其实现包含两个关键组件：

- **先验解码器（Prior Decoder, PD）**：一个仅处理条件图像分支的解码器，生成先验分割掩码 $F_{prior}$。该掩码编码了目标结构的粗粒度空间信息，为高噪阶段的去噪提供“脚手架”。
- **反向加法（Reverse Addition, RA）与时间加权融合**：RA 首先通过 $F_{refined} = F_{main} \odot (1 - \sigma(F_{prior}))$ 抑制主分支中先验掩码活跃区域的特征，再通过时间加权融合：
  $$F_{fused} = (1 - \omega_t) \odot F_{refined} + \omega_t \odot F_{prior}$$
  其中权重 $\omega_t$ 在 $t$ 较大（高噪阶段）时接近最大值 $\alpha$，随 $t$ 减小而衰减至零（Appendix B 给出具体函数 $\omega_{t} = \alpha \cdot \exp(-5.0 \cdot (1 - t_{normalized})) \cdot (1 - \exp(-10.0 \cdot t_{normalized}))$）。这一设计确保早期强引导、后期逐步让位于主去噪网络，避免过度干扰。

**证据强度**：Figure 3 显示，仅使用 Diff 或 Diff+tLSTM 的模型在 $t=1000$ 起始时 Dice 崩溃至 0，而加入 APDS 后全程维持有效分割。Figure 4 进一步表明，APDS Out 的 Dice 在早期高于 Diff Out，随后被反超，验证了“先验引导—主网络接管”的预期行为。

### 创新二：tLSTM——跨时间步的状态记忆与证据积累

tLSTM 将循环神经网络的状态记忆机制引入扩散模型的去噪轨迹，使模型能够**显式维护并传递跨时间步的状态**，从而积累结构化证据。其核心创新包括：

- **Conv-tLSTM**：将标准 LSTM 的门控机制扩展为 3D 卷积操作，处理体积特征图。遗忘门 $f_t$ 和输入门 $i_t$ 共同更新记忆细胞 $\mathcal{C}_t = f_t \odot \mathcal{C}_{t-1} + i_t \odot \tilde{\mathcal{C}}_t$，实现跨步信息的保留与更新。
- **Linear-tGRU**：轻量级变体，用线性变换替代 3D 卷积，在保持循环记忆能力的同时降低计算开销。
- **t-cell 增强**：在标准 LSTM 基础上增强记忆细胞机制，进一步强化时间状态的保持能力。Table 1 消融实验表明，t-cell 组件使 LNCTVSeg Dice 从 82.5 提升至 83.7。

tLSTM 的跨步状态更新可形式化为 $\mathscr{S}_t = tLSTM(\mathscr{S}_{t+1}, \phi(x_t, X_c, t))$，其中状态从高噪步向低噪步传递，逐步积累目标结构的证据。

### 创新三：SC-tLSTM 与 FFT-tLSTM——时空与频域的双重增强

在 tLSTM 基础上，Cross-Timestep 进一步引入两个专用模块：

- **SC-tLSTM（Spatial-Channel tLSTM）**：将空间注意力和通道注意力机制改造为有状态、时间感知的形式。空间注意力分支沿 X/Y/Z 轴池化后通过 tLSTM 生成空间注意力图 $M_s$；通道注意力分支通过平均/最大池化聚合后由 tGRU 生成通道注意力图 $M_c$。两者串联细化特征：$F_{out} = M_s \odot (M_c \odot F)$。
- **FFT-tLSTM**：利用频域中结构信息与噪声成分更易分离的特性，将输入变换到频域 $\mathcal{F}_t = FFT(X_t)$，通过 tLSTM 滤波并在条件频谱 $\mathcal{F}_c$ 门控下调制：$\tilde{\mathcal{F}} = tLSTM(Filter(\mathcal{F}_t + \mathcal{F}_c)) \odot \mathcal{F}_c$，最后经 iFFT 变换回空间域并加残差连接。

**证据强度**：Table 3 消融实验显示，单独引入 SC 或 FFT 模块均能显著提升性能；全量配置（APDS + SC + FFT）在 LNCTVSeg 上达到 Dice 83.7、IoU 74.2、HD95 2.44 的最优结果。Figure 5 和 Figure 10 的热图可视化进一步证实，tLSTM 的记忆机制使注意力在去噪过程中逐步聚焦到目标结构。

### 创新协同：从崩溃到稳定

APDS 和 tLSTM 的协同体现在：APDS 在高噪阶段注入强先验，防止早期崩溃；tLSTM 在后续步中积累和细化证据，使去噪过程成为“逐步细化”而非“重新发现”结构。Figure 6 的可视化对比直观展示了这一协同效果——无 APDS 时反向扩散无法形成有效结构，加入 APDS 后目标结构从早期即开始显现并逐步精细化。

### 相对 Baseline 的 Changed Slots 总结

| 机制槽位 | Baseline（Diff-UNet） | Cross-Timestep |
|---------|----------------------|----------------|
| 先验指导 | 无 | APDS（PD + RA + 时间加权衰减） |
| 跨时间步记忆 | 各步独立去噪 | tLSTM（Conv-tLSTM / Linear-tGRU + t-cell） |
| 去噪器架构 | 标准 U-Net 编码器-解码器 | 编码器集成 FFT-tLSTM + SC-tLSTM，解码器集成 SC-tLSTM + APDS |

## 整体框架

![[assets/figures/papers/iclr26_0011_TE3asYO8PQ_Cross-Timestep_3D_Diffusion_Model_with_Trans-tem/figures/002_Figure_2.jpg]]
*Figure 2: (a) The framework of the Cross-Timestep, we propose APDS and tLSTM to construct a stable diffusion architecture. (b) Time-weighted control RA, using the prior mask obtained from the PD to guide the main branch. (c) Detailed design of Conv-tLSTM, using convolution to improve the gating mechanism of LSTM and enhance its memory cell to remember the temporal state. (d) Detailed design of Linear-tGRU, using Linear combined with GRU to reduce resource requirements, compared with Conv-tLSTM. (e) Structure of SC-tLSTM, improving the traditional SC attention to adapt to the diffusion model. (f) Structure of FFT-tLSTM, transforming the time domain into the frequency domain for denoising*

Cross-Timestep 的整体架构围绕一个核心问题展开：3D扩散模型在从纯噪声开始的反向扩散中，高噪声时间步（初始阶段）会因缺乏结构先验而崩溃，无法恢复目标解剖结构。为解决这一问题，框架在标准U-Net风格编码器-解码器的基础上，引入了两个关键机制——**自适应先验解码策略（APDS）** 和**跨时间步记忆LSTM（tLSTM）**，以稳定去噪轨迹并积累跨步证据。

### 架构总览

如图2(a)所示，Cross-Timestep 的推理网络可形式化为：

$$
\epsilon_{\theta} = \mathcal{D}_{SC,APDS}(\mathcal{E}_{SC,FFT}(x_t, t), X_c, t)
$$

其中 $x_t$ 为当前时间步的带噪输入，$X_c$ 为条件图像（原始医学影像），$t$ 为扩散时间步。编码器 $\mathcal{E}_{SC,FFT}$ 集成了频域去噪模块 **FFT-tLSTM** 和时空注意力模块 **SC-tLSTM**，负责在频域和空间-通道维度上提取并积累结构化证据。解码器 $\mathcal{D}_{SC,APDS}$ 则通过 **SC-tLSTM** 进行特征重构，并借助 **APDS** 提供的先验指导实现稳定输出。

### 核心模块与数据流

**先验解码器（PD）** 是APDS的入口，仅处理条件图像分支 $X_c$，生成先验分割掩码 $F_{prior}$。该掩码通过**反向加法（RA）** 机制以时间加权方式融入主分支：

1. **特征细化**：先验掩码抑制主分支特征中的活跃区域，避免过强干扰：
   $$F_{refined} = F_{main} \odot (1 - \sigma(F_{prior}))$$

2. **时间加权融合**：使用随 $t$ 衰减的权重 $\omega_t$ 融合细化特征与先验特征：
   $$F_{fused} = (1 - \omega_t) \odot F_{refined} + \omega_t \odot F_{prior}$$

权重函数 $\omega_t$ 在附录B中定义为：
$$\omega_{t} = \alpha \cdot \exp(-5.0 \cdot (1 - t_{normalized})) \cdot (1 - \exp(-10.0 \cdot t_{normalized}))$$

其设计逻辑是：在初始高噪声阶段（$t$ 接近 $T$）提供强先验指导，防止崩溃；随着去噪推进（$t$ 接近 $0$），先验影响衰减至零，让主去噪器接管精细分割。

**tLSTM** 作为跨时间步记忆单元，在编码器和解码器中维护并传递状态 $\mathscr{S}_t$，实现证据积累：
$$\mathscr{S}_t = tLSTM(\mathscr{S}_{t+1}, \phi(x_t, X_c, t))$$

框架内包含三种tLSTM实现：
- **Conv-tLSTM**：将标准LSTM的门控机制扩展为3D卷积操作，处理体积特征图。
- **Linear-tGRU**：轻量级变体，用线性变换替代3D卷积以降低计算开销。
- **SC-tLSTM**：在Conv-tLSTM基础上集成空间和通道注意力，增强对目标结构的聚焦能力。
- **FFT-tLSTM**：在频域进行去噪，利用FFT将输入变换到频域后通过tLSTM滤波，再经iFFT返回空间域并加残差连接。

### 训练与推理

前向扩散过程为标准DDPM马尔可夫链：
$$q(x_t | x_{t-1}) = \mathcal{N}(x_t; \sqrt{1-\beta_t} x_{t-1}, \beta_t \mathbf{I})$$

训练采用简化的噪声预测损失：
$$\mathcal{L}_{simple} = \mathbb{E}_{t, x_0, \epsilon} \left[ || \epsilon - \mathcal{M}_{\theta}(x_t, X_c, t) ||^2 \right]$$

推理时，从纯噪声 $x_T \sim \mathcal{N}(0, \mathbf{I})$ 出发，迭代执行DDPM采样步：
$$x_{t-1} = \frac{1}{\sqrt{\alpha_t}} \left( x_t - \frac{1-\alpha_t}{\sqrt{1-\bar{\alpha}_t}} \epsilon_{\theta} \right) + \sigma_t z$$

整个pipeline的因果链条可概括为：APDS在早期提供强结构先验防止崩溃 → tLSTM跨步积累证据 → 先验权重衰减后主去噪器接管 → 最终输出精细分割掩码。图1和图3分别定性和定量地展示了APDS对“初始阶段崩溃”的消除效果。

## 核心模块与公式推导

### 自适应先验解码策略（APDS）

APDS 是解决“初始阶段崩溃”的核心机制。在高噪声时间步（$t$ 较大时），反向扩散从纯噪声开始缺乏结构先验，导致去噪轨迹崩溃。APDS 通过两个子模块注入并衰减先验引导：

**先验解码器（Prior Decoder, PD）** 仅处理条件图像分支 $X_c$，生成先验分割掩码 $F_{prior}$，为去噪过程提供粗粒度解剖结构参考。

**反向加法（Reverse Addition, RA）** 将先验掩码反向融合到主分支。首先通过特征细化抑制先验活跃区域：

$$F_{refined} = F_{main} \odot (1 - \sigma(F_{prior}))$$

其中 $F_{main}$ 为主去噪分支特征，$\sigma$ 为 sigmoid 激活。随后以时间加权融合细化特征与先验特征：

$$F_{fused} = (1 - \omega_t) \odot F_{refined} + \omega_t \odot F_{prior}$$

权重 $\omega_t$ 在扩散早期（高噪声）取较大值，随时间步 $t$ 减小而衰减至零，使先验引导逐步让位于主去噪器自身预测。具体形式为：

$$\omega_{t} = \alpha \cdot \exp(-5.0 \cdot (1 - t_{normalized})) \cdot (1 - \exp(-10.0 \cdot t_{normalized}))$$

其中 $\alpha$ 为最大先验权重，$t_{normalized}$ 为归一化时间步。该函数在 $t_{normalized} \to 1$（高噪声）时趋近 $\alpha$，在 $t_{normalized} \to 0$（低噪声）时衰减至零。

### 跨时间步记忆 LSTM（tLSTM）

tLSTM 是维持去噪过程时间一致性的有状态循环单元，在反向扩散各步间显式传递隐藏状态 $h_t$ 和记忆细胞 $\mathcal{C}_t$。其核心变体包括：

**Conv-tLSTM** 将标准 LSTM 的门控结构扩展至 3D 体积数据，使用 3D 卷积替代矩阵乘法。其门控公式为：

输入门：$i_t = \sigma(W_{xi} * X_t + W_{hi} * h_t' + b_i)$

遗忘门：$f_t = \sigma(W_{xf} * X_t + W_{hf} * h_t' + b_f)$

输出门：$o_t = \sigma(W_{xo} * X_t + W_{ho} * h_t' + b_o)$

候选记忆：$\tilde{C}_t = \tanh(W_{xc} * X_t + W_{hc} * h_t' + b_c)$

其中 $*$ 表示 3D 卷积，$h_t'$ 为上一时间步隐藏状态。记忆细胞更新遵循：

$$\mathcal{C}_t = f_t \odot \mathcal{C}_{t-1} + i_t \odot \tilde{\mathcal{C}}_t$$

隐藏状态由输出门调制记忆细胞得到：

$$h_t = o_t \odot \tanh(\mathcal{C}_t)$$

**Linear-tGRU** 是轻量级变体，以线性变换替代 3D 卷积，降低计算开销。其门控公式为：

重置门：$r_t = \sigma(W_{xr} X_t + W_{hr} h_t' + b_r)$

更新门：$z_t = \sigma(W_{xz} X_t + W_{hz} h_t' + b_z)$

**t-cell 增强** 在 Conv-tLSTM 基础上强化记忆细胞机制，显式保留跨步状态，是消融实验中性能提升的关键组件（Table 1 证实 t-cell 使 LNCTVSeg Dice 从 82.5 提升至 83.7）。

### 空间-通道 tLSTM（SC-tLSTM）

SC-tLSTM 将传统空间-通道注意力改造为有状态、时间感知的循环注意力。其空间注意力分支沿 X/Y/Z 轴池化并拼接：

$$P_{xyz} = Concat(Pool_x(F), Pool_y(F), Pool_z(F)), \quad M_s = tLSTM(P_{xyz})$$

通道注意力分支通过平均池化和最大池化聚合空间信息：

$$P_{channel} = Concat(AvgPool(F), MaxPool(F)), \quad M_c = tGRU(P_{channel})$$

特征细化先应用通道注意力再应用空间注意力：

$$F' = M_c \odot F, \quad F_{out} = M_s \odot F'$$

### 频域 tLSTM（FFT-tLSTM）

FFT-tLSTM 在频域进行去噪，利用结构信息与噪声在频谱中的可分离性。首先将带噪输入和条件图像变换到频域：

$$\mathcal{F}_t = FFT(X_t), \quad \mathcal{F}_c = FFT(X_c)$$

频域特征通过 tLSTM 滤波并在条件频谱门控下调制：

$$\tilde{\mathcal{F}} = tLSTM(Filter(\mathcal{F}_t + \mathcal{F}_c)) \odot \mathcal{F}_c$$

最后逆变换回空间域并加残差连接：

$$X_{out} = iFFT(\tilde{\mathcal{F}}) + X_t$$

### 完整推理网络

推理时，编码器集成 FFT-tLSTM 和 SC-tLSTM，解码器集成 SC-tLSTM 和 APDS：

$$\epsilon_{\theta} = \mathcal{D}_{SC,APDS}(\mathcal{E}_{SC,FFT}(x_t, t), X_c, t)$$

跨时间步状态通过 tLSTM 持续更新，实现证据积累：

$$\mathscr{S}_t = tLSTM(\mathscr{S}_{t+1}, \phi(x_t, X_c, t))$$

训练目标为条件 DDPM 简化损失：

$$\mathcal{L}_{simple} = \mathbb{E}_{t, x_0, \epsilon} \left[ || \epsilon - \mathcal{M}_{\theta}(x_t, X_c, t) ||^2 \right]$$

反向采样步遵循标准 DDPM 更新：

$$x_{t-1} = \frac{1}{\sqrt{\alpha_t}} \left( x_t - \frac{1-\alpha_t}{\sqrt{1-\bar{\alpha}_t}} \epsilon_{\theta} \right) + \sigma_t z$$

## 实验与分析

### 核心瓶颈与实验动机

3D扩散模型在医学分割中面临一个关键失效模式——“初始阶段崩溃”（Initial-stage collapse）。当反向扩散从纯噪声（高噪声时间步，t≈1000）开始时，模型缺乏结构先验且无法积累跨步证据，导致无法恢复目标解剖结构（Figure 1, Figure 7）。本文的实验设计围绕该瓶颈展开，验证两个因果调控手段：自适应先验解码策略（APDS）在高噪阶段提供强结构指导，以及跨时间步记忆LSTM（tLSTM）在去噪轨迹中积累并传递结构化证据。

![[assets/figures/papers/iclr26_0011_TE3asYO8PQ_Cross-Timestep_3D_Diffusion_Model_with_Trans-tem/figures/001_Figure_1.jpg]]
*Figure 1: “Initial-stage collapse”. For 3D medical data, the diffusion model will crash when sampling starts from the high-noise stage (equivalent to random noise), but it can correctly sample from the middle and low time steps. Introducing APDS enables correct sampling starting from random noise*

---

### 主结果：与现有方法的全面比较

Table 2报告了Cross-Timestep与七种现有方法在LNCTVSeg（鼻咽癌淋巴结CTV）和OASeg（骨关节炎分割）两个异构数据集上的定量对比。指标包括Dice、IoU和HD95。

![[assets/figures/papers/iclr26_0011_TE3asYO8PQ_Cross-Timestep_3D_Diffusion_Model_with_Trans-tem/figures/009_Table_2.jpg]]
*Table 2: Comparison with state-of-the-art methods*

- **LNCTVSeg数据集**：Cross-Timestep取得Dice 83.7、IoU 74.2、HD95 2.44，在所有指标上均优于次优方法Diff-UNet（精确值未提供，但Table 2显示Diff-UNet为先前最佳）。基于变换器的模型（TransBTS、SwinUNETR、UNETR、nnFormer）和混合模型（3DUXNET）的Dice分布在约78-82区间，表明扩散框架本身的潜力，但仅有Cross-Timestep通过APDS和tLSTM的组合充分释放了该潜力。
- **OASeg数据集**：Cross-Timestep取得Dice 72.8、IoU 65.4、HD95 6.24，同样优于所有对比方法。该数据集的t-SNE可视化（Figure 9）显示三个中心之间存在显著的域偏移，模型在该条件下仍保持领先，初步验证了方法的鲁棒性。

**证据强度**：Table 2提供了多指标、多数据集的直接对比，置信度高。但需注意，原文未提供Diff-UNet的精确数值，仅标注“Ours”为最优，因此定量差距需手动核对。

---

### 消融研究：模块贡献的因果验证

#### tLSTM组件的消融（Table 1）

Table 1系统拆解了tLSTM模块的内部设计，对比了五种配置：

![[assets/figures/papers/iclr26_0011_TE3asYO8PQ_Cross-Timestep_3D_Diffusion_Model_with_Trans-tem/figures/007_Table_1.jpg]]
*Table 1: Ablation study on tLSTM components*

1. **基础LSTM**：无卷积适配，性能最低。
2. **Conv-LSTM**：引入3D卷积门控，性能提升。
3. **Linear-GRU**：轻量级GRU变体，以线性层替代3D卷积，在效率与性能间取得折中。
4. **Conv-LSTM + Linear-GRU**：两者结合，进一步改善。
5. **完整tLSTM（含t-cell）**：在配置4基础上加入增强记忆细胞机制（t-cell），LNCTVSeg Dice从82.5提升至83.7，OASeg Dice达到72.8，取得最佳IoU和HD95。

**因果解读**：t-cell组件是tLSTM的核心创新——它显式维护并传递跨时间步状态，使去噪过程从“每步重新发现结构”转变为“逐步积累并细化证据”。Table 1的递进式提升直接支持该机制的有效性。

#### APDS、SC-tLSTM和FFT-tLSTM的模块消融（Table 3）

Table 3以基线模型（含APDS以解决初始阶段崩溃）为起点，逐步添加SC-tLSTM和FFT-tLSTM：

![[assets/figures/papers/iclr26_0011_TE3asYO8PQ_Cross-Timestep_3D_Diffusion_Model_with_Trans-tem/figures/010_Table_3.jpg]]
*Table 3: Ablation study on APDS, SC, and FFT modules*

- **仅APDS**：LNCTVSeg Dice约80.2，OASeg Dice约68.5（从Table 3行1估算），验证了APDS单独即可防止高噪崩溃，但缺乏时间记忆限制了精度。
- **APDS + SC-tLSTM**：引入空间-通道跨时间步记忆，在两个数据集上均显著提升。
- **APDS + FFT-tLSTM**：引入频域去噪，同样带来独立增益。
- **APDS + SC-tLSTM + FFT-tLSTM**：全量配置取得LNCTVSeg Dice 83.7、OASeg Dice 72.8的最优结果。

**因果解读**：SC-tLSTM和FFT-tLSTM各自独立有效，分别从时空记忆和频域噪声鲁棒性两个互补维度增强去噪质量。两者叠加产生协同效应，验证了设计的多维性。

---

### 关键现象的可视化验证

#### APDS防止初始阶段崩溃（Figure 3, Figure 6）

Figure 3展示了从不同起始时间步执行反向扩散的平均Dice。当起始步t>700时，纯扩散模型（Diff）和仅加tLSTM的模型（Diff+tLSTM）的Dice骤降至接近零——即初始阶段崩溃。引入APDS后（Diff+tLSTM+APDS），即使在t=1000起步，Dice仍保持正值并稳定上升。Figure 6提供了反向扩散过程的可视化对比：无APDS时，去噪轨迹早期即发散为无意义噪声；有APDS时，粗粒度解剖结构在早期逐步浮现，后续去噪仅需细化。

![[assets/figures/papers/iclr26_0011_TE3asYO8PQ_Cross-Timestep_3D_Diffusion_Model_with_Trans-tem/figures/004_Figure_3.jpg]]
*Figure 3: The average dice value obtained by performing reverse diffusion starting from noisy images at different time steps*

**机制**：APDS通过先验解码器（PD）从条件图像生成先验掩码$F_{prior}$，并以时间加权函数$\omega_t$（见附录B公式）将其融合到主分支。$\omega_t$在高噪阶段取最大值$\alpha$，随标准化时间步$t_{normalized}$衰减至零，确保先验指导“功成身退”，不过度干扰后期精细化去噪。

#### APDS的支撑性而非替代性作用（Figure 4）

Figure 4比较了完整反向扩散过程中主去噪网络输出（Diff Out）和APDS先验输出（APDS Out）的Dice变化。早期阶段APDS Out提供较高的Dice基线，起到“脚手架”作用；随着去噪推进，Diff Out逐渐超越APDS Out，最终分割结果由主网络主导。该动态证明APDS提供的是可退出的引导而非硬约束，避免了先验偏差导致的过拟合。

#### tLSTM的渐进式注意力聚焦（Figure 5, Figure 10）

Figure 5和Figure 10展示了反向扩散过程中tLSTM特征热图的演变。早期时间步的热图分散且模糊；随着去噪推进，热图逐渐聚焦到目标解剖结构（淋巴结CTV或骨关节炎区域）。这直接可视化tLSTM如何利用跨时间步记忆逐步积累结构化证据，将注意力从全局搜索收敛到精确分割目标。

---

### 计算成本与扩散步数的权衡

#### 计算效率分析（Table 4）

Table 4比较了五种方法的计算开销。Cross-Timestep的训练时间为33.4小时，推理时间0.17秒/样本，GFLOPS和GPU显存占用处于中等水平。nnFormer推理最快（0.03秒），但分割精度低于Cross-Timestep。这表明tLSTM的状态维护和APDS的先验解码带来了可接受的计算代价，换取的是稳定性与精度的显著提升。

#### 扩散步数的影响（Table 5）

Table 5报告了不同扩散步数（300、500、1000）下LNCTVSeg的性能变化。Dice从300步的79.3提升至1000步的83.7，HD95从4.86降至2.44。性能随步数单调改善，说明tLSTM的跨步证据积累机制需要足够的轨迹长度才能充分发挥作用。**局限性**：1000步的推理延迟（0.17秒/样本）并非最快，在实时或高吞吐场景下可能成为瓶颈。

---

### 失败模式与局限性

1. **初始阶段崩溃的残余风险**：尽管APDS有效防止了从纯噪声起步的完全崩溃，但其引导完全依赖条件图像。在极端域偏移或严重采集伪影下，先验解码器生成的$F_{prior}$可能不可靠，导致早期引导偏差。Figure 8的t-SNE可视化证实LNCTVSeg数据集存在显著的多中心异质性，模型虽整体鲁棒，但极端离群样本的表现需进一步验证。

2. **扩散步数依赖**：Table 5显示300步时Dice仅79.3，与1000步的83.7差距明显。该方法尚未与DDIM等加速采样策略结合，在低步数场景下的性能衰减是实用化的关键障碍。

3. **解剖结构与模态泛化性未验证**：当前仅在鼻咽癌淋巴结CTV和骨关节炎两种任务上评估，对其他解剖部位、成像模态（如MRI、超声）及病变类型的适用性尚属未知。

4. **长轨迹稳定性**：tLSTM的状态记忆虽增强了时间一致性，但在超过1000步的更长扩散轨迹或更大体积输入上的稳定性和效率有待研究。

---

### 开放问题

- 能否将APDS框架扩展至无监督或半监督3D分割，减少对精确标注的依赖？
- tLSTM的状态记忆机制能否与DDIM、FP-Diffusion等加速采样方法结合，在保持分割质量的前提下大幅降低扩散步数？
- 该方法在数千例规模的异源多中心数据集上是否仍能维持鲁棒性和计算效率？

## 方法谱系与知识库定位

### 与 Baseline 的关系

Cross-Timestep 的核心改进建立在扩散分割模型 Diff-UNet 之上，后者本身在 Table 2 中已是次优方法。两者的分水岭在于对“初始阶段崩溃”的处理：Diff-UNet 遵循标准 DDPM 范式，从纯噪声开始反向扩散，在高噪声时间步（t > 700）缺乏结构先验，导致去噪轨迹崩溃（Figure 1, Figure 7）；Cross-Timestep 通过两个互补机制——APDS 提供时间衰减的结构先验，tLSTM 积累跨步证据——将扩散模型稳定化，使从随机噪声出发的正确采样成为可能。

与 TransBTS、SwinUNETR、UNETR、nnFormer、3DUXNET 等非扩散分割模型相比，Cross-Timestep 的根本差异在于将分割建模为条件生成过程而非直接映射。Table 2 显示该方法在 LNCTVSeg 和 OASeg 两个异构数据集上均取得最优 Dice/IoU/HD95，表明扩散范式在 3D 医学分割中的潜力。Perspective+ 作为多视角融合模型，其设计思路与 Cross-Timestep 的频域去噪（FFT-tLSTM）存在松散的类比关系——两者都试图从不同表示空间提取互补信息，但机制上并无直接继承。

### 适用边界

从验证范围看，该方法的适用边界目前清晰但有限：

1. **任务边界**：仅在鼻咽癌淋巴结节 CTV（LNCTVSeg）和骨关节炎原发性肿瘤 GTV（OASeg）两种 3D 分割任务上验证。两者均为单器官、单模态（CT/MR）的病灶分割，对多器官联合分割、多模态融合、或正常解剖结构分割的泛化性未经检验。

2. **数据规模边界**：Table 4 显示训练时间 33.4 小时，推理时间 0.17 秒/样本，GFLOPS 和 GPU 显存开销在对比方法中处于中等偏上水平。Table 5 进一步表明性能对扩散步数敏感——需要 1000 步才能达到最佳 Dice，减少步数会导致性能退化。这一特性限制了在实时或资源受限场景下的部署。

3. **先验可靠性边界**：APDS 的引导完全依赖条件图像分支（PD 仅处理 $X_c$），在极端域偏移（Figure 9 展示的 OASeg 跨中心分布差异）或采集伪影情况下，先验质量可能下降。方法本身未包含对先验可信度的自适应评估机制。

### 已知局限

1. **推理延迟与步数依赖**：1000 步扩散是性能最优的必要条件（Table 5），这导致推理时间（0.17 秒/样本）虽非最差，但显著慢于 nnFormer（0.03 秒/样本）等非扩散方法。该局限根植于扩散模型的采样范式本身，tLSTM 的状态记忆机制并未直接减少所需步数。

2. **任务与模态泛化未验证**：当前仅在两种特定病灶类型上验证，对脑肿瘤、肝脏病变、血管分割等常见 3D 医学分割任务的适用性未知。不同模态（如超声、PET）的噪声特性差异可能影响 FFT-tLSTM 频域去噪的有效性。

3. **先验解码器的独立性风险**：PD 与主去噪分支在训练中共享条件编码器，但在推理时 PD 的输出 $F_{prior}$ 完全由 $X_c$ 决定，不接收来自扩散过程的反馈校正。Figure 4 显示 APDS Out 的 Dice 在后期时间步被 Diff Out 超越，表明先验质量存在上限，在极端噪声或分布外样本上可能成为瓶颈。

4. **长轨迹稳定性未充分探索**：tLSTM 的跨时间步状态更新 $\mathscr{S}_t = tLSTM(\mathscr{S}_{t+1}, \phi(x_t, X_c, t))$ 理论上可支持任意长度轨迹，但实际验证仅限 1000 步。更长的扩散轨迹或更大体积输入下，循环状态是否会出现梯度消失/爆炸、记忆饱和等问题，缺乏消融或分析。

### 开放问题

1. **加速采样与 tLSTM 的兼容性**：能否将 tLSTM 的状态记忆机制与 DDIM、FP-Diffusion 等加速采样策略结合，在保持分割质量的前提下将所需步数压缩至 50-100 步？这需要研究跨步状态在跳跃式采样中的传递方式——当时间步非均匀采样时，$\mathscr{S}_{t}$ 的更新频率和衰减特性需要重新设计。

2. **先验引导的弱监督扩展**：APDS 框架是否可扩展至无监督或半监督场景，以降低对精确像素级标注的依赖？例如，能否用粗糙的边界框或涂鸦标注训练 PD，再由扩散过程细化？这涉及先验质量与去噪能力之间的权衡边界。

3. **多中心大规模验证**：Figure 8-9 的 t-SNE 可视化确认了数据集的多中心异质性，但当前实验规模有限。在数千例级别的真实多中心数据上，tLSTM 的状态记忆是否仍能有效积累跨域证据，还是会被域偏移干扰，是一个开放的工程和科学问题。

4. **频域去噪的理论理解**：FFT-tLSTM 在消融实验中表现出独立贡献（Table 3），但其有效性的理论解释尚停留在“频域中信噪更可分离”的经验直觉层面。不同解剖结构、不同噪声水平下的最优频域滤波策略是什么，缺乏系统分析。

## 原文 PDF

![[paperPDFs/ICLR_2026/Cross_Timestep_3D_Diffusion_Model_with_Trans_temporal_Memory_LSTM_and_Adaptive_Priori_Decoding_Strategy_for_Medical_Segmentation.pdf]]
