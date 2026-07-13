---
title: "RealisVSR: Detail-enhanced Diffusion for Real-World 4K Video Super-Resolution"
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: paperPDFs/arxiv_2025/RealisVSR_Detail-enhanced_Diffusion_for_Real-World_4K_Video_Super-Resolution.pdf
project_link: "https://zws98.github.io/RealisVSR-project/"
code_link: null
aliases:
- RealisVSR
tags:
- arxiv_2025
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
core_operator: 三个关键因果调节因素：1) 采用Wan2.1视频扩散模型作为基础先验，因其具有优越的时空一致性；2) 提出一致性保留控制网络（CPC），移除条件分支中的噪声潜变量注入以抑制伪影；3) 提出高频校正损失（HR-Loss），通过小波分解和HOG特征显式增强高频分量。
primary_logic: 将先进的视频扩散先验（Wan2.1）与无噪声条件注入和频域感知损失相结合，可以在大幅减少训练数据的同时，恢复真实世界4K视频中的高频细节并保持时序一致性。
claims:
- 在SPMCS上，PSNR达到27.36 dB，显著优于最佳基线RealViformer（25.60 dB）
- 在VideoLQ真实视频集上，DOVER得分51.96，超越所有基线（如STAR 51.28）
- 时间一致性指标E_warp在SPMCS上为0.81，比STAR（2.00）降低60%
- 仅需50K训练视频对，约为STAR训练数据量的25%，且推理速度在720P单次模型上快于SeedVR
---

# RealisVSR: Detail-enhanced Diffusion for Real-World 4K Video Super-Resolution

> [!tip] 核心洞察
> 将先进的视频扩散先验（Wan2.1）与无噪声条件注入和频域感知损失相结合，可以在大幅减少训练数据的同时，恢复真实世界4K视频中的高频细节并保持时序一致性。

| 字段 | 内容 |
|------|------|
| 中文题名 | RealisVSR：面向真实世界4K视频超分的细节增强扩散模型 |
| 英文题名 | RealisVSR: Detail-enhanced Diffusion for Real-World 4K Video Super-Resolution |
| 会议/期刊 | arXiv 2025 |
| Links | [paper](https://arxiv.org/abs/2507.19138) · [Project](https://zws98.github.io/RealisVSR-project/) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion |
| Method | RealisVSR |
| Dataset | SPMCS, REDS30, VideoLQ, RealisVideo-4K |

> [!tip] 效果简介
> - SPMCS (合成) 上，PSNR ↑ 27.36 vs 25.60 (RealViformer) (+1.76)。
> - REDS30 (合成) 上，PSNR ↑ 26.56 vs 25.49 (SeedVR) (+1.07)。
> - VideoLQ (真实) 上，DOVER ↑ 51.96 vs 51.28 (STAR) (+0.68)。

## 概要

真实世界4K视频超分辨率（VSR）面临的核心瓶颈并非简单的分辨率不足，而是**时序一致性建模不稳定**与**高频细节恢复能力薄弱**的双重困境。现有基于扩散模型的方法（如STAR、SeedVR）虽然在一定程度上推进了生成质量，但仍受限于三个根本问题：基础模型的时间动态建模不一致导致时序伪影和运动模糊；主流损失函数（如整流流损失）偏向低频结构保真，对真实世界复杂退化下的高频纹理恢复不足；缺乏面向4K高细节场景的基准数据集，评估体系过度依赖无参考指标，无法准确衡量细节增强的真实能力。

RealisVSR通过三个关键因果调节因素破解上述瓶颈：**（1）** 采用Wan2.1视频扩散模型作为基础先验，凭借其优越的时空一致性建模能力，从根本上改善运动平滑性与时序稳定性；**（2）** 提出一致性保留控制网络（Consistency Preserved ControlNet, CPC），在条件注入阶段移除噪声潜变量，仅保留条件信号以抑制伪影产生；**（3）** 设计高频校正损失（HR-Loss），通过Haar小波分解与梯度方向直方图（HOG）特征约束，显式增强高频分量的恢复精度。三者协同使得模型仅需约5–25%的对比方法训练数据量（约50K视频对），即可在合成与真实场景下实现领先性能。

在方法谱系上，RealisVSR属于**基于视频扩散先验的条件生成式超分**路线，区别于基于GAN的RealViformer（Zhang & Yao, ECCV 2024）和基于整流流的STAR（Xie et al., ICCV 2025）等方案。其核心创新在于将“无噪声条件注入”与“频域感知损失”引入扩散框架，形成了从架构设计到训练目标的闭环优化。

主要实验结果验证了该路线的有效性：在合成基准SPMCS上，PSNR达到**27.36 dB**，显著超越最佳基线RealViformer（25.60 dB），提升幅度达1.76 dB；在真实视频集VideoLQ上，DOVER得分**51.96**，优于STAR（51.28）；时间一致性指标$E_{warp}$在SPMCS上降至**0.81**，相比STAR（2.00）改善约60%。消融实验进一步证实，CPC模块与HR-Loss各自独立贡献显著增益，二者组合后达到最优——基准模型PSNR为26.54 dB，全模型提升至27.36 dB，SSIM达0.8169。

值得注意的是，该方法仍存在若干局限：训练数据为自收集的50K 4K视频对，可能引入场景分布偏差；依赖Wan2.1预训练模型（约1.6B参数），对部署硬件要求较高；退化管道为两阶合成退化，尚未完整覆盖真实世界中传感器噪声、非均匀模糊等复杂退化组合。这些方面需在后续研究中进一步验证与改进。

### 真实世界视频超分的核心矛盾

视频超分辨率（VSR）旨在从低质量视频中恢复高分辨率细节，在安防监控、影视修复、移动摄影等领域具有广泛需求。然而，当目标分辨率提升至4K级别时，现有方法面临一个根本性矛盾：**高频细节恢复与时空一致性之间的权衡**。传统GAN方法通常能生成锐利纹理，但容易引入时序闪烁和伪影；而基于扩散模型的新范式虽然具有更强的生成能力，却在真实世界复杂退化场景下暴露出三个关键瓶颈。

### 现有扩散基VSR方法的三重瓶颈

**瓶颈一：基础模型的时间动态建模不一致。** 当前多数扩散基VSR方法（如Upscale-A-Video, Zhou et al., CVPR 2024；VEnhancer, He et al., Arxiv 2024）基于图像扩散先验（如Stable Diffusion）或早期视频扩散模型（如CogVideoX），这些模型对长程运动的理解能力有限，导致超分结果出现运动模糊和时序伪影。尽管SeedVR（Wang et al., CVPR 2025）和STAR（Xie et al., ICCV 2025）尝试引入视频扩散先验，但时空一致性仍远未达到实用水平——例如STAR在SPMCS数据集上的帧间扭曲误差高达2.00，表明存在明显的时序抖动。

**瓶颈二：损失函数偏向低频保真，高频细节恢复不足。** 扩散模型的训练通常采用整流流损失（Rectified Flow Loss），其本质是最小化预测速度与真实速度之间的均方误差。该损失函数天然偏向于重建低频结构（如平滑区域、大尺度轮廓），对高频纹理（如毛发、织物纹理、文字边缘）的约束力极弱。在真实世界退化场景中，低质量输入本身已丢失大量高频信息，仅靠整流流损失难以从噪声分布中恢复出可信的细节。

**瓶颈三：缺乏4K高细节基准数据集。** 现有VSR评估主要依赖合成退化数据集（如REDS、SPMCS）或无参考质量指标（如DOVER）。合成退化无法完整模拟真实世界中传感器噪声、压缩伪影、非均匀模糊等复杂退化组合；而无参考指标有时会被伪影“欺骗”而给出虚高评分，无法准确衡量细节增强的真实能力。这一评估体系的缺陷使得方法间的细节恢复能力难以公平比较。

### 本文动机与核心思路

针对上述瓶颈，RealisVSR提出三个因果调节因素来系统性地解决问题：

1. **采用Wan2.1视频扩散模型作为基础先验**，利用其更强的时空一致性建模能力来抑制运动伪影；
2. **设计一致性保留控制网络（CPC）**，通过移除条件分支中的噪声潜变量注入来消除伪影源头；
3. **提出高频校正损失（HR-Loss）**，结合小波分解和HOG特征显式增强高频分量的恢复。

这一组合策略的核心洞察在于：**将先进的视频扩散先验与无噪声条件注入和频域感知损失相结合，可以在大幅减少训练数据（仅需STAR的25%）的同时，恢复真实世界4K视频中的高频细节并保持时序一致性。**

## 核心方法与创新机理

RealisVSR 的核心创新并非单一模块的堆砌，而是围绕**扩散模型在真实世界4K视频超分中的三大瓶颈**——时序不一致、高频细节丢失、数据效率低下——进行的系统性改造。其技术路线可归结为三个相互耦合的 changed slot：**基础先验的升级**、**条件注入范式的重构**，以及**频域感知训练目标的引入**。

### 从图像先验到视频先验：Wan2.1 基础模型

现有扩散基 VSR 方法多构建于图像扩散模型（如 Stable Diffusion）或时序建模能力有限的视频扩散模型之上，导致生成结果在运动区域出现闪烁、伪影等时序不一致问题。RealisVSR 直接将基础先验替换为 **Wan2.1 视频扩散模型**，该模型内置 3D Causal VAE、DiT 块和 umT5 文本编码器（Figure 2），具备更强的时空一致性建模能力。这一选择并非简单的“换底座”——Wan2.1 的运动先验使得后续的条件注入和损失函数设计能够在一个更稳定的时序基底上发挥作用，从而避免了先验本身成为瓶颈。

### 无噪声条件注入：一致性保留控制网络（CPC）

标准 ControlNet 的条件注入范式同时将噪声潜变量 $z_t$ 和条件信号注入可训练副本，即 $x_{\text{comb}} = \mathcal{T}(z_t) + \mathcal{T}(\text{cond})$。RealisVSR 的关键洞察在于：**丢弃 $z_t$ 的注入，仅保留条件信号**，即 $x_{\text{CPC}} = \mathcal{T}_{\theta_{\text{cond}}}(c_t)$。这一设计的因果机制是：$z_t$ 携带的噪声分量在条件分支中会被放大并传播至主网络，成为伪影的来源；移除后，CPC 模块仅负责将低质量视频的结构信息通过深度自适应残差连接（可学习缩放因子 $\gamma$）融合至主网络各层：

$$\mathbf{X}_{i}^{\text{main}} = \mathbf{X}_{i}^{\text{main}} + \gamma \cdot \mathbf{F}_{\lfloor i / r \rfloor}^{\mathbf{CPC}}$$

消融实验（Table 3）证实了这一设计的决定性作用：基准模型（无 CPC，仅整流流损失）在 SPMCS 上 PSNR 为 26.54 dB，加入 CPC 后跃升至 27.24 dB 以上，说明条件注入范式的重构是性能提升的首要驱动因素。

### 频域感知的高频校正损失（HR-Loss）

传统整流流损失 $\mathcal{L}_{\text{REC}} = \mathbb{E}[\| v_{\Theta}(z_t, t) - (\epsilon - x_0) \|^2]$ 偏向低频结构保真，对高频纹理的约束不足。RealisVSR 引入 **HR-Loss**，通过两个互补的频域约束显式增强高频分量：

- **小波损失 $\mathcal{L}_{\text{WLF}}$**：基于 Haar 小波将预测速度与目标速度分解为 LL、LH、HL、HH 四个子带，对高频子带（LH、HL、HH）赋予更高权重（最佳配置为 $\{1.0, 2.0, 2.0, 2.0\}$，Table 5），迫使模型在训练中优先恢复边缘和纹理信息。
- **HOG 损失 $\mathcal{L}_{\text{HOG}}$**：在预测速度与目标速度上分别计算梯度方向直方图（9 个方向 bin），约束两者在纹理方向分布上的一致性，从而抑制方向性伪影。

总损失为三者的直接求和：$\mathcal{L}_{\text{HR}} = \mathcal{L}_{\text{WLF}} + \mathcal{L}_{\text{HOG}} + \mathcal{L}_{\text{REC}}$。消融实验（Table 3）表明，单独添加 HOG 损失即可将 PSNR 从 CPC 基线的 27.24 提升至 27.33，组合小波损失后达到最优 27.36 dB / SSIM 0.8169，证明两个频域约束存在互补增益。

### 创新的协同效应

三个 changed slot 并非孤立生效。Wan2.1 的视频先验为 CPC 的无噪声注入提供了稳定的时序基底，使条件信号不会被运动不一致性污染；CPC 抑制伪影后，HR-Loss 对高频分量的显式约束才能真正转化为纹理细节的增强，而非被伪影所消耗。这一协同效应的直接证据是：仅需 50K 训练视频对（约为 STAR 的 25%），RealisVSR 即在 SPMCS 上以 PSNR 27.36 dB 显著超越最佳基线 RealViformer（25.60 dB），同时在时间一致性指标 $E_{\text{warp}}$ 上达到 0.81，较 STAR（2.00）降低 60%。

RealisVSR 的整体流程围绕三个核心设计展开：**强大的视频扩散先验**、**无噪声条件注入**和**频域感知的损失函数**。给定一段低质量（LQ）视频，系统首先通过基础模型将其压缩到潜空间，再利用一致性保留控制网络（CPC）将退化视频的条件信息注入去噪过程，最终解码为高细节的4K超分输出。

### 输入输出与数据流

- **输入**：一段低分辨率/低质量视频，以及可选的文本描述（用于引导扩散过程）。
- **基础模型**：采用 **Wan2.1** 视频扩散模型作为先验骨干，包含三个子模块：
  - **3D Causal VAE**：将视频压缩到时空潜空间，实现高效表示；
  - **DiT Blocks**：基于 Diffusion Transformer 的去噪主干网络；
  - **umT5 Text Encoder**：对文本条件进行编码，提供语义引导。
- **条件注入**：CPC 模块接收 LQ 视频作为条件信号，通过深度自适应残差连接将特征融合到主网络的 DiT 块中。与标准 ControlNet 不同，CPC **丢弃了噪声潜变量 $z_t$ 的注入**，仅使用条件信号 $c_t$：
  
  $$\mathbf{X}_{i}^{\mathrm{main}} = \mathbf{X}_{i}^{\mathrm{main}} + \gamma \cdot \mathbf{F}_{\lfloor i / r \rfloor}^{\mathbf{CPC}}$$
  
  其中 $\gamma$ 为可学习的缩放因子，$r$ 为 CPC 块与主网络块的对应比率。这一设计的关键因果效应是**抑制了噪声注入引入的伪影和时序不一致性**，消融实验证实该模块将基准模型 PSNR 从 26.54 dB 提升至 27.24 dB 以上（Table 3）。

- **去噪与解码**：在 CPC 条件引导下，DiT 块执行反向扩散过程，预测速度场 $v_\Theta(z_t, t)$。去噪后的潜变量经 3D Causal VAE 解码器重建为高分辨率视频帧。

### 训练目标

RealisVSR 的优化目标为**高频校正损失（HR-Loss）**，由三个分量组成：

$$\mathcal{L}_{\mathrm{HR}} = \mathcal{L}_{\mathrm{WLF}} + \mathcal{L}_{\mathrm{HOG}} + \mathcal{L}_{\mathrm{REC}}$$

- **$\mathcal{L}_{\mathrm{REC}}$**：标准整流流损失，保留全局结构保真度；
- **$\mathcal{L}_{\mathrm{WLF}}$**：基于 Haar 小波分解的多尺度子带损失，高频子带（LH, HL, HH）赋予更高权重（设置为 2.0），显式增强边缘和纹理；
- **$\mathcal{L}_{\mathrm{HOG}}$**：基于梯度方向直方图（HOG）的纹理一致性约束，使用 9 个方向 bin 对齐预测与目标的局部梯度分布。

消融实验表明，单独添加 HOG 损失即可将 PSNR 提升至 27.33 dB，而组合小波和 HOG 损失的全模型达到最优 27.36 dB（Table 3），验证了频域感知损失对高频细节恢复的因果作用。

### 推理配置

推理阶段提供两种配置以权衡速度与质量：
- **Ours-720P**：单次前向直接生成 720P 输出，49 帧推理耗时约 86 秒；
- **Ours-480P**：在 480P 分辨率下推理后通过多次拼接生成 720P 输出，耗时约 216 秒，但可在更低显存占用下运行。

> **注意**：整体架构图见 **Figure 2**，该图展示了基础模型、CPC 模块和损失函数的完整关系。

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2507_19138/figures/002_Figure_2.jpg]]
*Figure 2: The framework of the proposed RealisVSR*

RealisVSR 的核心架构由三个关键模块协同构成：**Wan2.1 视频扩散先验**、**一致性保留控制网络（CPC）** 和 **高频校正损失（HR-Loss）**。三者分别解决时序一致性、条件注入伪影和高频细节恢复三大瓶颈。

### 2.1 Wan2.1 基础模型

RealisVSR 构建于 Wan2.1 视频扩散模型之上，利用其优越的时空一致性作为生成先验。基础模型包含三个子组件：

- **3D Causal VAE**：将视频压缩至潜空间，同时保留时序因果性，避免未来帧信息泄露；
- **DiT Blocks**：基于 Diffusion Transformer 的去噪主干网络，负责从噪声潜变量逐步恢复视频内容；
- **umT5 Text Encoder**：对文本描述进行编码，提供语义条件引导。

### 2.2 一致性保留控制网络（CPC）

标准 ControlNet 在条件注入时同时将噪声潜变量 $z_t$ 和条件信号拼接送入条件分支，即 $\mathbf{x}_{\text{comb}} = \mathcal{T}(z_t) + \mathcal{T}(\text{cond})$。作者发现这种噪声注入会引入额外的随机扰动，在视频超分任务中表现为时序伪影和纹理失真。

CPC 的核心创新在于**丢弃输入阶段的噪声潜变量**，仅使用条件信号 $c_t$ 作为条件分支的输入：

$$\mathbf{x}_{\text{CPC}} = \mathcal{T}_{\theta_{\text{cond}}}(c_t)$$

CPC 的输出特征通过深度自适应残差连接融合至主网络各 DiT Block：

$$\mathbf{X}_{i}^{\text{main}} = \mathbf{X}_{i}^{\text{main}} + \gamma \cdot \mathbf{F}_{\lfloor i / r \rfloor}^{\text{CPC}} \tag{1}$$

其中 $\mathbf{F}_{\lfloor i / r \rfloor}^{\text{CPC}}$ 为 CPC 模块在第 $\lfloor i / r \rfloor$ 层的输出特征，$\gamma$ 为可学习的缩放因子，$r$ 为 CPC 层与主网络层的间隔比例。这一设计有效抑制了噪声注入带来的伪影，同时保持了条件信息的高效传递。

### 2.3 高频校正损失（HR-Loss）

现有扩散模型的整流流损失偏向低频结构保真，对高频纹理恢复不足。HR-Loss 通过三个分量显式增强高频细节：

**整流流损失（$\mathcal{L}_{\text{REC}}$）** 保留全局结构保真度。给定前向扩散过程 $z_{t} = \alpha_{t} \cdot x_{0} + \sigma_{t} \cdot \epsilon$，模型预测速度 $v_{\Theta}(z_t, t)$：

$$\mathcal{L}_{\text{REC}} = \mathbb{E}\left[ \| v_{\Theta}(z_{t}, t) - (\epsilon - x_{0}) \|^{2} \right] \tag{3}$$

**小波损失（$\mathcal{L}_{\text{WLF}}$）** 基于 Haar 小波分解，将预测速度与目标速度分别分解为低频子带（LL）和高频子带（LH, HL, HH），并对各子带施加加权约束：

$$\mathcal{L}_{\text{WLF}} = \mathbb{E}\left[ \sum_{k_{i} \in \mathbb{S}} w_{k_{i}} \left\| f_{k_{i}}(v_{\Theta}(z_{t}, t)) - f_{k_{i}}(\epsilon - x_{0}) \right\|^{2} \right] \tag{4}$$

其中 $\mathbb{S} = \{\text{LL}, \text{LH}, \text{HL}, \text{HH}\}$，$f_{k_i}$ 为对应子带的小波系数提取函数。高频子带权重设为 2.0，低频子带权重设为 1.0，以此显式增强高频分量。

**HOG 损失（$\mathcal{L}_{\text{HOG}}$）** 通过梯度方向直方图约束纹理一致性。对预测速度与目标速度分别计算 9 个方向 bin 的梯度方向直方图，并最小化二者差异：

$$\mathcal{L}_{\text{HOG}} = \mathbb{E}\left[ \left\| \nabla_{\theta, m}(\boldsymbol{v}_{\Theta}(z_{t}, t)) - \nabla_{\theta, m}(\epsilon - \boldsymbol{x}_{0}) \right\|^{2} \right] \tag{5}$$

其中 $\nabla_{\theta, m}$ 表示在方向 $\theta$ 和尺度 $m$ 上的 HOG 特征提取操作。

**总损失** 为三个分量的直接求和：

$$\mathcal{L}_{\text{HR}} = \mathcal{L}_{\text{WLF}} + \mathcal{L}_{\text{HOG}} + \mathcal{L}_{\text{REC}} \tag{6}$$

消融实验（Table 3）表明，CPC 模块将基准 PSNR 从 26.54 提升至 27.24 以上；单独加入 HOG 损失（CPC+HOG）进一步提升至 27.33；组合小波与 HOG 损失的全模型达到最优 PSNR 27.36、SSIM 0.8169。Table 5 进一步验证了小波高频权重 $\{1.0, 2.0, 2.0, 2.0\}$ 为最优配置，权重过高反而导致质量下降。

## 实验与关键发现

### 核心结果：多基准定量对比

RealisVSR在合成退化与真实世界退化两大类基准上均取得领先性能。Table 1汇总了在六个数据集上的全参考/无参考指标对比，覆盖720P与4K分辨率。

**合成基准（全参考指标）**。在SPMCS上，RealisVSR的PSNR达到27.36 dB，比最佳基线**RealViformer**（Zhang and Yao, ECCV 2024）的25.60 dB高出1.76 dB；SSIM为0.8169，LPIPS降至0.1388。在REDS30上，PSNR为26.56 dB，超越**SeedVR**（Wang et al., CVPR 2025）的25.49 dB。在UDM10和YouTube-HQ上同样保持最优。这些合成基准上的全参考指标提升，直接归因于CPC模块对伪影的抑制和HR-Loss对高频纹理的增强——消融实验（Table 3）表明，仅加入CPC就将基准模型PSNR从26.54提升至27.24以上。

**真实世界基准（无参考指标）**。在VideoLQ真实视频集上，DOVER得分51.96，超越**STAR**（Xie et al., ICCV 2025）的51.28。在细节最丰富的RealisVideo-4K数据集上，LPIPS降至0.0939，优于所有基线。需要注意的是，DOVER等无参考指标可能对伪影敏感，部分对比需结合全参考指标综合判断。

**时间一致性**。Table 2展示了帧间扭曲误差$E_{warp}$的对比。在SPMCS上，RealisVSR的$E_{warp}$仅为0.81，比STAR的2.00降低约60%；在UDM10上为1.72，比**VEnhancer**（He et al., Arxiv 2024）的2.47降低约30%。这一优势源于Wan2.1基础模型的强时空一致性先验与CPC的无噪声条件注入策略——标准ControlNet同时注入噪声潜变量$z_t$和条件信号会引入时序伪影，而CPC丢弃$z_t$仅使用条件信号$c_t$，从而在去噪过程中保持帧间连贯性。

### 消融实验：CPC与HR-Loss的贡献分解

Table 3在SPMCS上系统拆解了各组件的作用。基准模型（无CPC，仅整流流损失$\mathcal{L}_{\text{REC}}$）的PSNR为26.54 dB。加入CPC后，PSNR跃升至27.24以上，验证了无噪声条件注入对伪影抑制的关键作用。在CPC基础上，单独添加HOG损失（$\mathcal{L}_{\text{HOG}}$）将PSNR提升至27.33，表明基于梯度方向直方图的纹理约束有效增强了细节恢复。组合小波损失（$\mathcal{L}_{\text{WLF}}$）和HOG损失的全模型达到最优PSNR 27.36、SSIM 0.8169，证明两种频域感知损失具有互补性——小波分解在多尺度子带上显式约束高频分量，HOG特征则在梯度方向上保持纹理一致性。

Table 5进一步消融了小波损失的高频权重配置。当四子带权重$\{w_{LL}, w_{LH}, w_{HL}, w_{HH}\}$设为$\{1.0, 2.0, 2.0, 2.0\}$时取得最佳PSNR 27.24；权重过高（如$\{1.0, 3.0, 3.0, 3.0\}$）反而导致质量下降，说明过度强调高频会破坏全局结构的保真度平衡。这一发现为频域损失的超参数选择提供了经验指导。

### 资源效率与推理开销

Table 4对比了扩散基方法的资源消耗。RealisVSR仅需50K训练视频对，约为STAR训练数据量的25%，却取得了更优性能。推理方面，Ours-720P模型单次前向推理86秒即可生成720P输出，快于SeedVR的108秒；但Ours-480P模型需多次前向拼接，推理时间延长至216秒（49帧）。这一权衡提示：在部署时需根据目标分辨率和时延要求选择合适的模型变体。

### 失败模式与局限

尽管整体性能领先，以下场景仍需关注：

1. **极端退化泛化性**：退化管道为两阶合成退化，未能完整覆盖真实世界中的传感器噪声、非均匀运动模糊等复杂组合。在未见过的退化类型上，细节恢复质量可能下降，需更广泛验证。

2. **高频权重敏感性**：小波损失的高频权重需谨慎调节，过高会引入伪影、损害结构保真度。当前最优权重$\{1.0, 2.0, 2.0, 2.0\}$来自SPMCS上的网格搜索，在其他数据分布下可能需要重新校准。

3. **无参考指标的可靠性**：DOVER等指标有时会被伪影提升，因此在VideoLQ等真实数据集上的优势需结合定性视觉检查确认。更鲁棒的纹理保真度度量仍是开放问题。

4. **计算开销**：依赖Wan2.1基础模型（约1.6B参数），相比GAN方法对硬件要求更高，资源受限环境下的部署存在挑战。

### 图表结论摘要

- **Table 1**：RealisVSR在合成和真实基准上全面超越现有方法，PSNR/SSIM/LPIPS/DOVER均达到最优或次优。
- **Table 2**：时间一致性指标$E_{warp}$大幅领先，验证了CPC和Wan2.1先验对时序伪影的抑制效果。
- **Table 3**：CPC和HR-Loss各自贡献显著，组合后达到最优，证明无噪声条件注入与频域感知损失的协同作用。
- **Table 4**：训练数据效率（仅需STAR的25%）和推理速度（720P单次86秒）具有实用优势。
- **Table 5**：小波高频权重存在最优区间，过高会损害质量，为损失函数调参提供了定量依据。

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2507_19138/figures/003_Table_1.jpg]]
*Table 1: Quantitative comparisons on VSR benchmarks from diverse scenarios, i.e., synthetic (SPMCS, UDM10, REDS, YouTube-HQ), and real (VideoLQ) datasets. The best and second performances are marked in bold and underlined, respectively. The RealisVideo-720P is resized from RealisVideo-4K, including the richest details among 720P datasets*

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2507_19138/figures/005_Table_2.jpg]]
*Table 2: Temporal consistency comparison with SOTA methods on warping error*

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2507_19138/figures/007_Table_3.jpg]]
*Table 3: Ablation study of Consistency Preserved Control-Net (CPC), the proposed wavelet-based and hog-based highfrequency losses (Wavelet, HOG). The experiments are conducted on SPMCS dataset*

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2507_19138/figures/009_Table_4.jpg]]
*Table 4: Resource consumption comparison with other diffusion-based methods, including dataset, size, resolution and inference time of 720P output*

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2507_19138/figures/008_Table_5.jpg]]
*Table 5: The effect of weights*

## 定位与知识库关联

### 在视频超分辨率方法谱系中的位置

RealisVSR 处于**基于扩散模型的真实世界视频超分辨率**这一前沿分支，其方法学定位可从三个维度刻画。

**相对于GAN-based方法**：传统VSR方法（如 **RealViformer** (Zhang and Yao, ECCV 2024)）依赖生成对抗网络，在合成退化上表现稳健，但对真实场景中复杂退化的高频细节恢复能力有限。RealisVSR通过引入视频扩散先验，在SPMCS上将PSNR从25.60 dB提升至27.36 dB（+1.76 dB），在真实视频集VideoLQ上DOVER从51.28提升至51.96，表明扩散模型在细节生成质量上具有本质优势。

**相对于同类扩散VSR方法**：现有扩散VSR方法面临三个瓶颈：基础模型时序建模不一致（如基于图像扩散的 **Upscale-A-Video** (Zhou et al., CVPR 2024)）、损失函数偏向低频保真（如标准整流流损失）、训练数据需求大（如 **STAR** (Xie et al., ICCV 2025) 需约200K视频对）。RealisVSR通过三个因果调节因素突破这些瓶颈：

1. **基础先验升级**：采用Wan2.1视频扩散模型替代CogVideoX或Stable Diffusion，利用其3D Causal VAE和DiT blocks实现更强的时空一致性建模。
2. **条件注入范式革新**：提出一致性保留控制网络（CPC），将标准ControlNet的条件注入方式从 $x_{comb} = T(z_t) + T(cond)$ 改为 $x_{CPC} = T(c_t)$，移除噪声潜变量$z_t$的直接注入以抑制伪影。这一设计是RealisVSR在时间一致性上取得突破的关键——在SPMCS上$E_{warp}$仅0.81，相比STAR的2.00降低60%。
3. **损失函数频域重构**：将训练目标从单一的整流流损失$\mathcal{L}_{REC}$扩展为高频校正损失$\mathcal{L}_{HR} = \mathcal{L}_{WLF} + \mathcal{L}_{HOG} + \mathcal{L}_{REC}$，通过Haar小波分解和HOG特征显式约束高频子带和纹理梯度方向。

**数据效率的独特优势**：RealisVSR仅需50K训练视频对（约为STAR的25%），却实现了更优的性能，证明强大的视频扩散先验与无噪声条件注入的组合可以大幅降低对训练数据规模的依赖。这一特性使其在数据稀缺的真实世界场景中具有实用价值。

### 适用边界与局限

尽管RealisVSR在多个基准上表现领先，其适用边界和局限性需要明确认知：

**退化覆盖的局限**。训练退化管道仍为两阶合成退化，未能完整覆盖真实世界中传感器噪声、非均匀运动模糊、压缩伪影等复杂退化组合。在极端退化类型上的泛化性有待更广泛验证，当前证据主要来自SPMCS、REDS30等标准基准。

**计算资源门槛**。RealisVSR依赖Wan2.1基础模型（约1.6B参数），相比GAN方法（如RealViformer）对硬件要求更高。虽然Ours-720P单次推理仅86秒（快于SeedVR的108秒），但Ours-480P模型需多次前向拼接生成720P输出，推理时间达216秒/49帧，在实时应用场景中仍存在瓶颈。

**评估指标的可靠性缺口**。4K细节评估仍部分依赖无参考指标（如DOVER），而这些指标有时会被伪影提升。例如，DOVER在VideoLQ上Ours为51.96仅略高于STAR的51.28（+0.68），但时间一致性$E_{warp}$的改善幅度（60%）远超DOVER的区分度，提示需要更鲁棒的纹理保真度度量。

**训练数据偏差**。自行收集的4K视频集（50K对）可能引入场景分布偏差，对特定内容类型（如暗光场景、快速运动）的性能需要进一步验证。

### 开放问题与后续方向

1. **跨任务泛化性**：CPC移除噪声潜变量的策略和HR-Loss的频域约束能否泛化到其他视频恢复任务（如去模糊、去噪）或其他扩散基模型？这一问题的回答将决定该方法的技术辐射范围。

2. **推理效率优化**：能否通过模型蒸馏、步数压缩或级联推理策略进一步缩短推理时间，实现4K视频的实时处理？当前86秒的720P推理时间仍需权衡。

3. **自适应损失权重**：高频校正损失中小波子带权重$\{w_{LL}, w_{LH}, w_{HL}, w_{HH}\}$当前固定为$\{1.0, 2.0, 2.0, 2.0\}$（消融实验显示权重过高反而降低质量），能否根据输入视频的退化程度和内容特性自适应调整？

4. **评估基准建设**：RealVideo-4K数据集的发布能否推动更真实的4K超分研究？需要设计更准确的无参考/全参考指标，以更好反映超分结果的纹理保真度和真实感，弥补当前DOVER等指标对伪影不敏感的缺陷。

5. **CPC机制的理论分析**：移除噪声潜变量注入为何能抑制伪影？这一现象在其他条件生成任务（如视频修复、编辑）中是否同样有效，其理论原因是否需要从扩散模型的条件引导理论角度进行更深入的分析？

## 原文 PDF

![[paperPDFs/arxiv_2025/RealisVSR_Detail-enhanced_Diffusion_for_Real-World_4K_Video_Super-Resolution.pdf]]
