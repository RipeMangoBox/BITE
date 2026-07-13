---
title: "MoCoDiff: A Controllable Autoregressive Diffusion Model for Expressive Motion Generation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/MoCoDiff_A_Controllable_Autoregressive_Diffusion_Model_for_Expressive_Motion_Generation.pdf
project_link: null
code_link: null
aliases:
- MoCoDiff
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 通过 Injection Modulation Controllers（IMC）将文本、风格和历史信号分离为独立的模态特定注入路径，利用轻量级线性交叉注意力模块实现解耦控制。同时，引入 Temporal IMC（TIMC）将历史作为时间步相关的校正信号注入扩散过程，将记忆less马尔可夫链转化为受控马尔可夫过程，从而主动抑制漂移并强制平滑过渡。
primary_logic: 将多条件运动生成重新定义为基于条件特定注入机制的时序调制问题，而非简单的特征拼接。通过在冻结的扩散骨干中独立注入语义、风格和历史调制，并利用受控自回归扩散动态，实现了模态解耦、长时稳定且风格一致的表达性运动合成。这种设计不仅提高了可控性和可解释性，还避免了繁琐的重新训练。
claims:
- IMC 通过分离的路径分别注入文本、风格和历史信号，避免了融合条件带来的模态纠缠。
- TIMC 将历史信息作为时间步相关的校正信号，将无记忆的马尔可夫链转化为有限历史的受控马尔可夫过程，从根本上改善了长时稳定性。
- MoCoDiff 在长序列风格化运动生成中取得了最高的 SRA（26.37）和最低的 AUJ（1.58），显著优于对比方法。
- 移除自回归扩散（ARDiffusion）导致过渡平滑度急剧下降，AUJ 从 1.58 升至 2.96，证明了受控自回归设计的必要性。
---

# MoCoDiff: A Controllable Autoregressive Diffusion Model for Expressive Motion Generation

> [!tip] 核心洞察
> 将多条件运动生成重新定义为基于条件特定注入机制的时序调制问题，而非简单的特征拼接。通过在冻结的扩散骨干中独立注入语义、风格和历史调制，并利用受控自回归扩散动态，实现了模态解耦、长时稳定且风格一致的表达性运动合成。这种设计不仅提高了可控性和可解释性，还避免了繁琐的重新训练。

| 字段 | 内容 |
|------|------|
| 中文题名 | MoCoDiff：一种用于表达性运动生成的可控自回归扩散模型 |
| 英文题名 | MoCoDiff: A Controllable Autoregressive Diffusion Model for Expressive Motion Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Song_MoCoDiff_A_Controllable_Autoregressive_Diffusion_Model_for_Expressive_Motion_Generation_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | MoCoDiff |
| Dataset | Long-sequence Stylized Motion Generation, Single Motion Generation, Time Efficiency, Ablation: AUJ |

> [!tip] 效果简介
> - Long-sequence Stylized Motion Generation 上，SRA (Style Recognition Accuracy) ↑ 26.37 vs ≤24.67 (best competing) (+≥1.70)；AUJ (Average Unbiased Jerk) ↓ 1.58 vs >2.0 (estimated best compete) (-≥0.42)。
> - Single Motion Generation (Style IMC only) 上，SRA ↑ 27.21 vs ≤26.37 (best compete) (+0.84)。
> - Time Efficiency 上，FPS (Frames Per Second) ↑ 136.89 vs ~28.5 (strongest baseline) (~4.8× faster)。

## 概要

### 问题背景

现有扩散运动生成方法普遍采用**融合条件范式**，将文本语义、运动风格和时间信号混合在单一通道中注入扩散模型。这种设计导致模态间相互干扰，严重削弱了长时一致性、细粒度风格控制和多条件组合的灵活性。同时，传统的自回归扩散缺乏对历史信息如何影响去噪过程的显式控制，在逐块生成长序列时容易出现**时间漂移**和过渡不一致——这是制约表达性运动生成走向实际应用的核心瓶颈。

### 核心方法

**MoCoDiff** 提出了一种可控的自回归扩散框架，核心创新在于将多条件运动生成重新定义为**基于条件特定注入机制的时序调制问题**。具体而言，通过两类关键设计实现突破：

1. **Injection Modulation Controllers (IMC)**：将文本、风格和历史信号分离为独立的模态特定注入路径，利用轻量级线性交叉注意力模块实现解耦控制。语义 IMC 注入低频内容调制以控制全局运动轨迹，风格 IMC 注入高频姿态级残差以捕捉节奏与身体曲线，时序 IMC 则引入历史依赖的校正信号。
2. **Controlled Autoregressive Diffusion**：通过 Temporal IMC (TIMC) 将历史信息作为时间步相关的校正项注入去噪过程，将无记忆的马尔可夫链转化为**有限历史的受控马尔可夫过程**，从而主动抑制漂移并强制平滑过渡。

整个框架保持扩散骨干冻结，仅训练轻量级 IMC 适配器，兼顾了可控性、可解释性与训练效率。

### 主要结果

在长序列风格化运动生成基准上，MoCoDiff 取得了最高的风格识别准确率（**SRA 26.37**）和最低的平均无偏急动度（**AUJ 1.58**），显著优于 AutoMDM+PersonaBooth、AutoMLD+SMooDi 等基线组合。消融实验证实：移除自回归扩散使 AUJ 从 1.58 升至 2.96，证明受控自回归机制对长时一致性的核心作用；用 ControlNet 替代 IMC 使 SRA 降至 15.38，验证了解耦多模态注入的不可替代优势。在效率方面，MoCoDiff 以 **136.89 FPS** 实现约 4.8 倍的生成加速。

### 方法定位

MoCoDiff 属于**可控运动扩散生成**方法，在条件注入机制上区别于融合式条件方法（如 **SMooDi** (Zhong et al., ECCV 2024) 的风格编码器拼接），在时序建模上区别于简单历史拼接的自回归扩散（如 **AutoMDM** 的逐块生成）。其解耦的 IMC 设计为多条件运动生成提供了可插拔、可解释的控制范式，冻结骨干的策略则降低了部署成本。当前局限在于固定大小的历史窗口（k=10）限制了对全局长程依赖的建模，极长序列下的误差累积仍是开放挑战。

### 运动生成中的多条件控制困境

人体运动生成是计算机视觉与图形学中的核心挑战之一，其目标是根据文本描述、风格参考等多模态信号合成逼真且可控的运动序列。近年来，扩散模型凭借其高质量的生成能力，已成为该领域的主流范式。然而，当任务从单条件扩展到多条件——尤其是同时要求语义对齐、风格保真和长时一致性时，现有方法暴露出根本性的结构缺陷。

当前扩散运动生成方法普遍采用**融合条件范式**：将文本语义、风格信号和时间上下文混合在单一通道中，通过 FiLM、AdaIN 或简单拼接等方式注入去噪网络。这一设计看似简洁，实则引入了严重的**模态间干扰**——不同条件信号在共享路径中相互竞争，导致语义与风格纠缠、长序列生成中出现时间漂移，以及多条件组合时灵活性的丧失。具体而言，融合条件范式在以下三个维度上存在系统性不足：

1. **语义-风格纠缠**：文本内容与运动风格通过同一注入路径混合，使得对某一条件的精细控制不可避免地影响另一条件，难以实现“保持语义、仅改风格”的独立操控。
2. **长时一致性缺失**：传统自回归扩散方法将去噪过程视为无记忆的马尔可夫链，缺乏对历史信息如何影响当前去噪动力学的显式控制，导致片段间过渡生硬、误差随序列增长而累积。
3. **条件组合灵活性受限**：融合范式要求所有条件在训练时即被固定绑定，难以在推理阶段动态组合或插值不同模态的控制信号，限制了生成系统的实用性与可解释性。

### 现有方法的局限与本文动机

针对上述困境，近期工作从不同角度进行了探索。**AutoMDM** 采用逐块自回归扩散策略，但缺乏对历史信息的结构化注入；**PersonaBooth**（Kim et al., CVPR 2025）实现了个性化文本到运动生成，却未解决多条件解耦问题；**SMooDi**（Zhong et al., ECCV 2024）和 **Motion Puzzle**（Jang et al., TOG 2022）分别专注于风格化扩散和任意风格迁移，但在长序列一致性上表现薄弱。这些方法的共同缺陷在于：**将多条件运动生成视为特征拼接问题，而非时序调制问题**。

本文的核心动机源于一个关键观察：运动生成中的语义、风格和历史信息具有本质不同的时间频率特性——语义控制全局轨迹（低频），风格刻画姿态细节（高频），历史提供过渡约束（时序依赖）。将它们强行融合在同一通道中，无异于用单一工具处理性质迥异的信号，必然导致控制精度与生成质量的折损。

基于此，我们提出 **MoCoDiff**，其核心思想是将多条件运动生成重新定义为**基于条件特定注入机制的时序调制问题**。通过引入 Injection Modulation Controllers（IMC），将文本、风格和历史信号分离为独立的模态特定注入路径，利用轻量级线性交叉注意力模块实现解耦控制。同时，Temporal IMC（TIMC）将历史信息作为时间步相关的校正信号注入扩散过程，将无记忆的马尔可夫链转化为受控马尔可夫过程，从根本上抑制漂移并强制平滑过渡。这一设计不仅实现了模态解耦与长时稳定，还通过冻结预训练扩散骨干、仅训练轻量适配器的方式，避免了繁琐的重新训练，为表达性运动生成提供了高效且可解释的解决方案。

## 核心方法与创新机理

MoCoDiff 的核心创新在于将多条件运动生成重新定义为**基于条件特定注入机制的时序调制问题**，而非简单的特征拼接。通过三个关键设计，该方法在冻结的扩散骨干上实现了模态解耦、长时稳定且风格一致的表达性运动合成。

### 1. 解耦的 Injection Modulation Controllers（IMC）

现有扩散运动生成方法普遍采用融合条件范式（FiLM/AdaIN/拼接），将语义、风格和时间信号混合在单一通道中，导致模态间相互干扰，严重削弱了细粒度风格控制和多条件组合的灵活性。MoCoDiff 引入 **Injection Modulation Controllers（IMC）**，将文本、风格和历史信号分离为独立的模态特定注入路径。

每个 IMC 实现为轻量级线性交叉注意力模块，核心公式为：

$$
X_t' = \mathcal{N}(X_t), \quad \mathrm{cond}' = \mathcal{N}(\mathrm{cond})
$$

$$
(Q, K, V) = \Phi(X_t', \mathrm{cond}') = \bigl( f_Q(X_t'), f_K(\mathrm{cond}'), f_V(\mathrm{cond}') \bigr)
$$

三个控制器分别承担不同的调制职责：
- **Semantic IMC（SIMC）**：注入低频、内容对齐的调制，控制全局运动轨迹；
- **Style IMC（STIMC）**：注入高频、姿态级残差，捕捉节奏、身体曲线等风格模式；
- **Temporal IMC（TIMC）**：引入历史依赖的校正信号，确保时序一致性。

最终，三种调制以残差形式叠加到扩散潜变量上：

$$
\hat{X}_t = X_t + O_{\mathrm{sem}}^{(t)} + O_{\mathrm{sty}}^{(t)} + \mathcal{M}_{\mathrm{hist}} \odot O_{\mathrm{hist}}^{(t)}
$$

消融实验证实了这一设计的不可替代性：**用 ControlNet 替代 IMC 使 SRA 从 26.37 骤降至 15.38，AUJ 从 1.58 升至 2.48**（Table 5），表明解耦的多模态注入远比单一控制网络更适合多条件运动生成。

### 2. 受控自回归扩散（Controlled Autoregressive Diffusion）

传统自回归扩散缺乏对历史信息如何影响去噪过程的显式控制，导致时间漂移和一致性差。MoCoDiff 通过 **Temporal IMC（TIMC）** 将历史作为时间步相关的校正信号注入扩散过程：

$$
x_{t-1} = f_\theta(x_t, t) + \mathscr{C}_t(h_{t-1})
$$

这一设计将无记忆的马尔可夫链转化为**有限历史的受控马尔可夫过程**，从根本上改善了长时稳定性。TIMC 修改的是扩散转移动力学本身，而非仅仅是条件特征，从而实现了真正基于反馈的采样控制。

在推理时，运动逐片段生成：

$$
C_i = \begin{cases} \mathcal{D}(T_1, S_1), & i=1, \\ \mathcal{D}(T_i, S_i, F_H), & i>1 \end{cases}
$$

训练阶段采用 **Progressive Rollout Curriculum**，逐步用模型自生成的历史替代真实历史，概率调度为：

$$
p_{\mathrm{rollout}}(\tau) = \frac{\tau - 0.3\mathcal{T}}{0.5\mathcal{T}}
$$

同时使用 EMA 模型更新历史缓冲区以稳定训练：

$$
\mathbf{h}^{(i+1)} = \left[ \mathbf{h}^{(i)}, \hat{\mathbf{m}}_{\mathrm{EMA}}^{(i)} \right]_{-k :}
$$

消融实验直接证明了这一机制的核心作用：**移除自回归扩散（w/o ARDiffusion）使过渡平滑度急剧下降，AUJ 从 1.58 升至 2.96**（Table 5）。误差累积诊断（Figure 7）进一步显示，随着运动长度增加，MoCoDiff 的漂移极小。

### 3. 冻结骨干 + 轻量级适配器策略

与从头训练或全微调扩散 U-Net 不同，MoCoDiff **冻结预训练扩散骨干**，仅训练轻量级 IMC 适配器。这一策略不仅避免了繁琐的重新训练，更重要的是保证了语义对齐的稳定性。消融实验显示：**解除骨干冻结（w/o freezeUnet）使 FID 升至 18.42，R-Top-3 降至 0.281**（Table 5），证实了冻结策略对稳定训练和保持语义对齐的关键作用。

### 核心创新总结

| 设计维度 | 基线方法 | MoCoDiff |
|---------|---------|----------|
| 条件注入机制 | 融合条件（FiLM/AdaIn/拼接），所有信号共享单一路径 | 解耦的 IMC，每类条件独立注入，通过线性交叉注意力实现模态特定调制 |
| 时序建模 | 静态条件或简单历史拼接，未显式控制去噪动力学 | 受控自回归扩散 + TIMC，将历史作为时间步相关的校正项注入去噪步骤 |
| 骨干网络策略 | 从头训练或全微调 | 冻结预训练扩散骨干，仅训练轻量级 IMC 适配器 |

这三个创新点协同作用，使得 MoCoDiff 在长序列风格化运动生成中取得了最高的 SRA（26.37）和最低的 AUJ（1.58），同时推理速度达到 136.89 FPS，约为最强基线的 4.8 倍。

MoCoDiff 的整体设计围绕一个核心思想展开：将多条件运动生成重新定义为**基于条件特定注入机制的时序调制问题**，而非传统的特征拼接或融合范式。如图3所示，系统由三个功能层构成——**多模态条件编码**、**解耦注入调制控制器（IMC）** 和**可控自回归扩散生成**，三者协同工作，在冻结的扩散骨干上实现模态解耦、长时稳定且风格一致的表达性运动合成。

### 多模态条件编码

框架接收三类异构条件信号，并通过独立的编码器将其映射到统一的特征空间：

- **文本编码器** $\mathcal{E}_{\text{text}}$（基于 CLIP）从文本提示 $T$ 中提取语义特征 $F_T$，用于控制运动的全局内容轨迹。
- **风格编码器** $\mathcal{E}_{\text{sty}}$（基于 MotionCLIP）从参考运动序列 $S_{1:L}$ 中提取风格特征 $F_S$，捕捉节奏、身体曲线和表现力等细粒度风格模式。
- **历史编码器** $\mathcal{E}_{\text{hist}}$ 是一个可学习的模块，将上一运动片段最后 $k$ 帧 $H_{1:k}$ 聚合为紧凑的时序状态 $F_H$：

$$F_T = \mathcal{E}_{\text{text}}(T), \quad F_S = \mathcal{E}_{\text{sty}}(S_{1:L}), \quad F_H = \mathcal{E}_{\text{hist}}(H_{1:k}) = \phi(W_h \operatorname{P}(H_{1:k}) + b_h)$$

这种分离式编码设计从源头上避免了不同模态信号在特征空间的纠缠，为后续的解耦注入奠定了基础。

### 解耦注入调制控制器（IMC）

IMC 是框架的核心创新模块，用于将编码后的条件信号注入扩散去噪过程。如图4所示，系统包含三个功能互补的控制器：

- **语义 IMC（SIMC）** 注入低频、内容对齐的调制信号，控制运动的全局轨迹和动作语义。
- **风格 IMC（STIMC）** 注入高频、姿态级残差，捕捉风格特有的节奏、身体曲线和表现力模式。
- **时序 IMC（TIMC）** 引入历史依赖的校正信号，将扩散过程从无记忆的马尔可夫链转变为**有限历史的受控马尔可夫过程**，从根本上改善长时一致性和过渡平滑度。

每个 IMC 均实现为轻量级线性交叉注意力模块。对于给定的含噪潜变量 $X_t$ 和条件信号 $\text{cond}$，首先分别进行归一化以稳定交互计算：

$$X_t' = \mathcal{N}(X_t), \quad \text{cond}' = \mathcal{N}(\text{cond})$$

随后通过投影算子 $\Phi$ 将二者映射到共享的查询-键-值空间：

$$(Q, K, V) = \Phi(X_t', \text{cond}') = \bigl( f_Q(X_t'), f_K(\text{cond}'), f_V(\text{cond}') \bigr)$$

最终，三个控制器的输出以残差形式叠加到扩散潜变量上，实现联合调控：

$$\hat{X}_t = X_t + O_{\text{sem}}^{(t)} + O_{\text{sty}}^{(t)} + \mathcal{M}_{\text{hist}} \odot O_{\text{hist}}^{(t)}$$

其中 $\mathcal{M}_{\text{hist}}$ 为历史掩码，用于控制历史调制的作用范围。这种设计的关键优势在于：**每类条件信号拥有独立的注入路径**，避免了传统融合条件（如 FiLM、AdaIN 或简单拼接）中模态间相互干扰的问题，同时保持了扩散骨干的冻结状态，仅需训练轻量级适配器即可实现多条件可控生成。

### 可控自回归扩散生成

长序列运动生成采用逐片段的自回归策略。设第 $i$ 个运动片段为 $C_i$，其生成过程为：

$$C_i = \begin{cases} \mathcal{D}(T_1, S_1), & i=1, \\ \mathcal{D}(T_i, S_i, F_H), & i>1 \end{cases}$$

首个片段仅由文本和风格条件生成，后续片段额外接收历史特征 $F_H$，保证运动在语义和风格上的连贯过渡。在每个片段的去噪过程中，TIMC 将历史状态 $h_{t-1}$ 导出的时变控制项 $\mathscr{C}_t(h_{t-1})$ 注入标准去噪步骤：

$$x_{t-1} = f_\theta(x_t, t) + \mathscr{C}_t(h_{t-1})$$

这一公式标志着从传统扩散到**受控扩散动力学**的本质转变：TIMC 修改的是扩散转移函数本身，而不仅仅是条件特征，从而实现了采样过程中基于反馈的主动漂移抑制。

### 渐进式 Rollout 训练

为弥合训练时的教师强制与推理时的自回归行为之间的差距，框架采用**渐进式 Rollout 课程训练**策略。训练过程中，模型以概率 $p_{\text{rollout}}$ 使用自身生成的历史替代真实历史：

$$p_{\text{rollout}}(\tau) = \frac{\tau - 0.3\mathcal{T}}{0.5\mathcal{T}}$$

其中 $\tau$ 为当前训练步数，$\mathcal{T}$ 为总训练步数。随着训练推进，$p_{\text{rollout}}$ 从 0 线性增长至 1，使模型逐步适应自回归推理模式。同时，历史缓冲区使用指数移动平均（EMA）模型的预测进行更新，以解耦历史生成与快速参数更新之间的不稳定性。总训练损失由重建损失、时序平滑损失和运动动态损失加权组成：

$$\mathcal{L} = \mathcal{L}_{\text{rec}} + \alpha \mathcal{L}_{\text{smooth}} + \beta \mathcal{L}_{\Delta}$$

整体而言，MoCoDiff 通过“分离编码—解耦注入—受控自回归”的三阶段设计，将多条件运动生成重新定义为条件特定的时序调制问题，实现了模态解耦、长时稳定且风格一致的表达性运动合成，同时避免了繁琐的从头训练或全微调。

![[assets/figures/papers/paper_list_l4_https_openaccess_thecvf_com_content_CVPR2026_html_Song_MoCoDiff_A_Contro/figures/003_Figure_3.jpg]]
*Figure 3: Method Overview. Content text, style motion, and historical context are encoded and injected into the diffusion backbone through Injection Modulation Controllers. Long-sequence generation is performed via Controlled Autoregressive Diffusion, which produces motion segment-by-segment and aligns each segment with prior history to maintain temporal coherence*

### 3.1 多模态条件编码

MoCoDiff 将生成过程所需的三类异质信号——文本语义、运动风格和历史上下文——分别映射为统一的特征表示，作为后续解耦注入的基础。编码阶段采用三个独立的编码器，公式化为：

$$F_T = \mathcal{E}_{\mathrm{text}}(T), \quad F_S = \mathcal{E}_{\mathrm{sty}}(S_{1:L}), \quad F_H = \mathcal{E}_{\mathrm{hist}}(H_{1:k}) = \phi(W_h \operatorname{P}(H_{1:k}) + b_h) \tag{1}$$

其中，$\mathcal{E}_{\mathrm{text}}$ 为基于 CLIP 的文本编码器，从文本提示 $T$ 中提取语义特征 $F_T$；$\mathcal{E}_{\mathrm{sty}}$ 为基于 MotionCLIP 的风格编码器，从参考运动序列 $S_{1:L}$ 中提取风格特征 $F_S$；$\mathcal{E}_{\mathrm{hist}}$ 为可学习的历史编码器，通过线性投影 $\phi$ 将上一运动片段最后 $k$ 帧的拼接姿态 $\operatorname{P}(H_{1:k})$ 压缩为紧凑的时序状态 $F_H$。这种分离的编码设计确保了三类条件在特征空间中保持模态特异性，为后续的独立注入路径奠定基础。

### 3.2 Injection Modulation Controllers（IMC）

IMC 是 MoCoDiff 的核心控制机制，其关键洞察在于：**将多条件运动生成重新定义为基于条件特定注入机制的时序调制问题，而非简单的特征拼接**。每个 IMC 被实现为轻量级线性交叉注意力模块，通过在冻结的扩散骨干中独立注入语义、风格和历史调制，实现模态解耦控制。

#### 3.2.1 交叉注意力注入机制

IMC 的运算流程分为归一化、投影和残差注入三步。首先对含噪潜变量 $X_t$ 和条件信号 $\mathrm{cond}$ 分别进行归一化，以稳定交叉注意力计算：

$$X_t' = \mathcal{N}(X_t), \quad \mathrm{cond}' = \mathcal{N}(\mathrm{cond}) \tag{2}$$

随后，通过投影算子 $\Phi$ 将归一化后的运动特征和条件特征映射到共享的查询-键-值空间：

$$(Q, K, V) = \Phi(X_t', \mathrm{cond}') = \bigl( f_Q(X_t'), f_K(\mathrm{cond}'), f_V(\mathrm{cond}') \bigr) \tag{3}$$

其中 $f_Q$ 为查询投影，$f_K$ 和 $f_V$ 分别为键和值的投影函数。该投影使运动特征（作为查询）能够主动检索条件信号（作为键-值对）中的相关信息，从而生成与当前扩散状态适配的调制信号。

#### 3.2.2 三类解耦控制器

三种 IMC 分别针对不同模态的调控需求设计，通过独立的键-值路径注入条件信息，最终以残差形式叠加到扩散潜变量上：

$$\hat{X}_t = X_t + O_{\mathrm{sem}}^{(t)} + O_{\mathrm{sty}}^{(t)} + \mathcal{M}_{\mathrm{hist}} \odot O_{\mathrm{hist}}^{(t)} \tag{4}$$

- **Semantic IMC（SIMC）**：提供低频、内容对齐的调制信号 $O_{\mathrm{sem}}^{(t)}$，控制全局运动轨迹。该控制器确保生成的运动在语义层面与文本描述保持一致，如“行走”与“跳跃”的动作区分。

- **Style IMC（STIMC）**：注入高频、姿态级残差 $O_{\mathrm{sty}}^{(t)}$，捕捉节奏、身体曲线和表现力等风格模式。与 SIMC 的低频调制形成频域互补，使风格特征能够在不干扰语义内容的前提下被精确注入。

- **Temporal IMC（TIMC）**：引入历史依赖的校正信号 $O_{\mathrm{hist}}^{(t)}$，通过掩码 $\mathcal{M}_{\mathrm{hist}}$ 控制其作用范围。TIMC 的核心创新在于**修改了扩散转移动力学本身**，而不仅仅是条件特征——它将标准去噪步骤从无记忆的马尔可夫链转化为有限历史的受控马尔可夫过程，从根本上抑制时序漂移。

### 3.3 受控自回归扩散

传统自回归扩散仅将历史信息作为附加条件拼接，未显式控制去噪动力学，导致长序列生成中出现时间漂移和一致性退化。MoCoDiff 通过 TIMC 将历史作为时间步相关的校正项直接注入去噪步骤，将生成过程建模为受控动力学系统：

$$x_{t-1} = f_\theta(x_t, t) + \mathscr{C}_t(h_{t-1}) \tag{5}$$

其中 $f_\theta(x_t, t)$ 为标准去噪转移函数，$\mathscr{C}_t(h_{t-1})$ 为由历史状态 $h_{t-1}$ 导出的时变控制项。这一设计使扩散过程从无记忆马尔可夫链转变为**受控马尔可夫过程**，主动抑制漂移并强制平滑过渡。

在推理阶段，运动序列以逐片段方式生成。首个运动块仅由文本和风格条件驱动，后续块额外接收历史特征 $F_H$：

$$C_i = \begin{cases} \mathcal{D}(T_1, S_1), & i=1, \\ \mathcal{D}(T_i, S_i, F_H), & i>1 \end{cases} \tag{6}$$

训练采用渐进式 Rollout 课程策略，逐步用模型自生成的历史替代真实历史，以平滑地从教师强制过渡到自回归推理。Rollout 概率随训练进度 $\tau$ 线性增长：

$$p_{\mathrm{rollout}}(\tau) = \frac{\tau - 0.3\mathcal{T}}{0.5\mathcal{T}} \tag{7}$$

其中 $\mathcal{T}$ 为总训练步数。为稳定训练，历史缓冲区使用指数移动平均（EMA）模型预测进行更新：

$$\mathbf{h}^{(i+1)} = \left[ \mathbf{h}^{(i)}, \hat{\mathbf{m}}_{\mathrm{EMA}}^{(i)} \right]_{-k:} \tag{8}$$

最终训练目标由重建损失、时序平滑损失和运动动态损失加权组成：

$$\mathcal{L} = \mathcal{L}_{\mathrm{rec}} + \alpha \mathcal{L}_{\mathrm{smooth}} + \beta \mathcal{L}_{\Delta} \tag{9}$$

其中 $\mathcal{L}_{\mathrm{rec}}$ 确保生成运动与真实数据的分布对齐，$\mathcal{L}_{\mathrm{smooth}}$ 惩罚相邻帧间的突变以增强过渡平滑性，$\mathcal{L}_{\Delta}$ 约束运动动态参数（如速度、加速度）的合理性。

![[assets/figures/papers/paper_list_l4_https_openaccess_thecvf_com_content_CVPR2026_html_Song_MoCoDiff_A_Contro/figures/004_Figure_4.jpg]]
*Figure 4: Architecture of IMCs. Each controller injects semantic, stylistic, or history-dependent modulation into the diffusion backbone, enabling disentangled and temporally consistent motion generation*

## 实验与关键发现

### 主要定量结果

**长序列风格化运动生成。** 表 1 报告了 MoCoDiff 与多种基线方法在长序列风格化运动生成任务上的全面对比。MoCoDiff 在风格准确度（SRA 26.37）和过渡平滑度（PJ 0.27，AUJ 1.58）上均取得最优结果，显著优于次优方法。具体而言，SRA 领先至少 1.70 个百分点，AUJ 则比估计的最佳竞争方法低 0.42 以上。这一优势的核心在于 **Temporal IMC（TIMC）** 将历史信息作为时间步相关的校正信号注入去噪过程，将无记忆的马尔可夫链转化为有限历史的受控马尔可夫过程，从而主动抑制时序漂移并强制平滑过渡。同时，**Style IMC（STIMC）** 通过独立的高频注入路径捕捉节奏、身体曲线等细粒度风格模式，在保持语义对齐（R-Top-3 0.564）的前提下实现了高保真风格迁移。

**单运动生成。** 在仅使用 Style IMC 的单运动生成评估中（表 2），MoCoDiff 取得 SRA 27.21，优于所有对比方法。这表明即使在无历史信息的条件下，解耦的风格注入机制本身已具备优于融合条件范式的风格控制能力。

**时间效率。** 表 3 显示 MoCoDiff 的生成帧率达到 136.89 FPS，约为最强基线（~28.5 FPS）的 4.8 倍。这种效率提升源于可控自回归扩散设计：通过逐片段生成而非逐帧生成，同时利用冻结的扩散骨干避免重复计算，在保证长时一致性的前提下大幅降低了推理延迟。

### 消融实验

表 5 的消融实验揭示了三个关键设计选择的因果作用：

1. **移除自回归扩散（w/o ARDiffusion）。** 过渡平滑度急剧恶化，AUJ 从 1.58 升至 2.96（+1.38）。这直接证明了 TIMC 驱动的受控自回归机制对长时一致性的核心贡献——缺少该机制时，模型退化为无记忆的逐片段生成，无法抑制片段间的漂移累积。

2. **用 ControlNet 替代 IMC。** 所有指标均显著下降，尤其是 SRA 降至 15.38，AUJ 升至 2.48。这表明单一控制网络无法有效处理多模态条件的解耦需求，而 IMC 通过分离的语义、风格和历史注入路径，在保持各模态独立可控性的同时实现了协同调制。

3. **解除骨干冻结（w/o freezeUnet）。** FID 升至 18.42，R-Top-3 降至 0.281。冻结预训练扩散骨干对于稳定训练和保持语义对齐至关重要——全微调会导致灾难性遗忘，破坏预训练模型已习得的运动先验。

### 关键超参数分析

**风格控制强度 λ。** 表 4 显示，λ=1.0 在运动真实感（FID 5.56）与风格保真度（SRA 27.21）之间取得最佳平衡。过低的 λ 导致风格注入不足，过高则引入伪影并损害运动自然度。

**历史帧长度 k。** 图 8 揭示了风格化能力（SRA）与过渡平滑度（AUJ）之间的权衡关系。k=10 帧被选为默认值，在此设置下模型在空间推理和时序稳定性之间达到最优折中。过短的历史窗口无法提供足够的时序上下文，而过长的窗口则引入冗余信息，干扰风格调制。

### 误差累积诊断

图 7 展示了随着运动序列长度增加，MoCoDiff 的漂移程度极小。这归功于 Progressive Rollout Curriculum 训练策略：训练中逐步用模型自生成的历史替代真实历史（公式 7），并利用 EMA 模型预测稳定历史缓冲区更新（公式 8），使模型在推理时能够鲁棒地处理自回归条件下的误差传播。

### 定性分析

图 5 的定性对比显示，MoCoDiff 在多个动作序列上实现了平滑过渡和忠实风格迁移，而基线方法（红框标注）出现明显的运动伪影和风格不一致。图 6 的消融可视化进一步证实：移除自回归扩散或 IMC 后，生成结果出现漂移和风格保真度丧失，与定量消融结论一致。

### 失败模式与局限

尽管 MoCoDiff 在长序列风格化运动生成上表现优异，仍存在以下局限：

- **极长序列的误差累积。** 在非常长的自回归滚动过程中，链式推理的稳定性仍有提升空间，误差可能逐步累积。
- **固定历史窗口的限制。** k=10 的固定大小窗口无法建模全局长程依赖关系，对于需要长时规划的运动序列可能不足。
- **冻结骨干的表达瓶颈。** 当遇到极端噪声或罕见运动模式时，冻结的扩散骨干表达能力可能受限，需要进一步验证。

### 公平性说明

所有方法均在相同数据集（HumanML3D + BABEL）上训练，使用 100Style 作为风格参考，评估采用统一的 SRA、FID、R-Top-3、PJ、AUJ 和 FPS 指标。对比方法涵盖 AutoMDM+PersonaBooth、AutoMLD+SMooDi 等最新基线组合，部分组合可能非原论文默认设置，但论文提供了公平的比较环境。

![[assets/figures/papers/paper_list_l4_https_openaccess_thecvf_com_content_CVPR2026_html_Song_MoCoDiff_A_Contro/figures/006_Table_1.jpg]]
*Table 1: Quantitative Evaluation. Symbols ↑, ↓, and → indicate that higher, lower, or closer-to-ground-truth (GT) values are better, respectively; The Bold text indicates the best performer, underlined text indicates the second best performer*

![[assets/figures/papers/paper_list_l4_https_openaccess_thecvf_com_content_CVPR2026_html_Song_MoCoDiff_A_Contro/figures/012_Table_5.jpg]]
*Table 5: Ablation Study. We present the visualization results of Three ablation experiments: without our ARDiffusion , without the IMC and without freezeUnet. The results showcase their importance*

![[assets/figures/papers/paper_list_l4_https_openaccess_thecvf_com_content_CVPR2026_html_Song_MoCoDiff_A_Contro/figures/005_Figure_5.jpg]]
*Figure 5: Qualitative Evaluation. MoCoDiff achieves smooth transitions and faithful style transfer across multiple actions, whereas prior methods show motion artifacts and style inconsistencies (red boxes)*

![[assets/figures/papers/paper_list_l4_https_openaccess_thecvf_com_content_CVPR2026_html_Song_MoCoDiff_A_Contro/figures/009_Figure_6.jpg]]
*Figure 6: Qualitative Of Ablation Study. Our method maintains smooth, style-consistent motion across multi-step text commands. Without autoregressive diffusion or IMC, results show drift and loss of stylistic fidelity. Long-horizonStyleRecognitionAccuracy(SRA) Long-horizonPhysical Stability (AUj)*

## 定位与知识库关联

### 一、与现有工作的关系与核心差异

MoCoDiff 处于**多条件运动生成**与**可控扩散模型**的交叉地带，其核心贡献在于将条件注入与自回归动力学重新定义为两个解耦的调控维度。与现有工作的关系可从三个维度展开：

**条件注入范式的演进。** 传统扩散运动生成方法普遍采用融合条件范式——将语义、风格和时序信号通过 FiLM、AdaIN 或简单拼接混合在单一通道中。MoCoDiff 的 Injection Modulation Controllers（IMC）打破了这一范式，通过三条独立的模态特定注入路径（语义 IMC、风格 IMC、时序 IMC）实现解耦控制。这一设计与 **ControlNet** 形成鲜明对比：消融实验显示，用 ControlNet 替代 IMC 导致 SRA 从 26.37 降至 15.38、AUJ 从 1.58 升至 2.48（Table 5），表明单一控制网络在多条件耦合场景下存在严重的模态间干扰。IMC 的解耦机制本质上将“多条件融合”重新定义为“多路径独立调制”，每条路径仅通过轻量级线性交叉注意力模块（Eq. 3）注入特定模态的校正信号，从而避免了特征空间的纠缠。

**自回归扩散的动力学重构。** 现有自回归运动扩散方法（如 **AutoMDM**）将历史信息作为静态条件拼接至输入，未显式控制去噪过程的动力学。MoCoDiff 的 Temporal IMC（TIMC）将这一关系倒置：历史信息不再是被动条件，而是作为时间步相关的**校正项**直接注入扩散转移函数（Eq. 5），将无记忆的马尔可夫链转化为有限历史的受控马尔可夫过程。这一设计从根本上改变了长序列生成中的误差传播机制——TIMC 在每一步去噪中主动抑制漂移，而非依赖模型隐式学习时序一致性。消融实验证实了这一设计的必要性：移除自回归扩散（w/o ARDiffusion）使 AUJ 从 1.58 急剧升至 2.96（Table 5），过渡平滑度严重受损。

**风格化运动生成的定位。** 在风格化运动生成领域，MoCoDiff 与 **SMooDi**（Zhong et al., ECCV 2024）、**Motion Puzzle**（Jang et al., TOG 2022）和 **PersonaBooth**（Kim et al., CVPR 2025）形成互补或超越关系。SMooDi 和 Motion Puzzle 专注于单段运动的风格迁移，缺乏长序列生成能力；PersonaBooth 通过个性化文本嵌入实现风格控制，但未涉及时序一致性建模。MoCoDiff 在长序列风格化运动生成中取得了 SRA 26.37 和 AUJ 1.58 的最优结果（Table 1），显著优于 AutoMDM+PersonaBooth 组合（SRA ≤24.67），证明了风格注入与时序控制联合建模的协同优势。

**骨干网络策略的分歧。** 与从头训练或全微调扩散 U-Net 的主流做法不同，MoCoDiff 采用**冻结预训练扩散骨干 + 轻量级 IMC 适配器**的策略。这一设计不仅降低了训练成本（单张 RTX 3090，8k 迭代），更重要的是保护了预训练模型中的运动先验。消融实验显示，解除骨干冻结（w/o freezeUnet）导致 FID 升至 18.42、R-Top-3 降至 0.281（Table 5），证实冻结策略对维持语义对齐和训练稳定性至关重要。

### 二、适用边界与能力边界

MoCoDiff 的能力边界由其设计选择所定义，理解这些边界对于正确使用和后续改进至关重要：

**长序列生成的上限。** 尽管 TIMC 将扩散过程转化为受控马尔可夫过程，但其控制能力受限于固定大小的历史窗口（k=10 帧）。这一设计在短至中等长度的序列中表现优异——误差累积诊断（Figure 7）显示，随着运动长度增加，MoCoDiff 的漂移极小——但在非常长的自回归滚动过程中，有限历史窗口无法捕获全局长程依赖关系，链式推理的稳定性仍有提升空间。

**冻结骨干的表达能力边界。** 冻结的预训练扩散骨干在常规运动模式下表现稳定，但当遇到极端噪声分布或罕见的运动模式（如高难度体操动作、非自然运动轨迹）时，其固定的参数化空间可能不足以提供充分的表达能力。此时 IMC 的调制能力受限于骨干的特征空间，无法从根本上扩展模型的生成边界。

**风格控制的分辨率。** Style IMC 通过注入高频、姿态级残差捕捉节奏和身体曲线等风格模式，但其调制粒度受限于交叉注意力机制的分辨率。对于需要逐关节精确控制的细粒度风格迁移任务（如特定舞种的脚步节奏），当前设计可能无法提供足够的控制精度。

**多条件组合的优先级。** IMC 的三条注入路径在潜变量空间中以残差叠加方式组合（Eq. 4），但各调制信号之间的相对权重和潜在冲突缺乏显式的协调机制。当语义、风格和历史信号指向相互矛盾的运动方向时，模型的仲裁策略是隐式的，可能导致不可预测的生成结果。

### 三、局限性与开放问题

基于上述分析，MoCoDiff 的局限性和开放问题可归纳如下：

**已验证的局限：**

1. **长程误差累积。** 在非常长的自回归滚动过程中仍可能累积误差，固定大小的历史窗口（k=10）限制了对全局长程依赖关系的建模能力。Figure 8 展示了历史帧长度在风格化（SRA）与过渡平滑度（AUJ）之间的权衡，10 帧是当前实验条件下的最优折中，但并非全局最优解。

2. **冻结骨干的表达瓶颈。** 冻结的扩散骨干在遇到极端噪声或罕见的运动模式时，其表达能力可能不足。Table 5 中 w/o freezeUnet 的 FID 急剧恶化（18.42 vs. 5.56）表明微调骨干会破坏预训练先验，但完全冻结又限制了模型对分布外样本的适应能力——这一矛盾尚未解决。

3. **物理合理性缺失。** 当前框架未引入任何物理先验（如足部接触约束、关节角度限制），生成的运动在极端情况下可能出现物理上不合理的姿态（如滑步、关节超伸）。Table 1 中 PJ 0.27 虽优于基线，但距离真实运动数据的平滑度仍有差距。

**开放问题：**

1. **物理先验的融合。** 如何为运动生成引入物理先验（如足部接触约束、动力学方程），以增强长序列的物理合理性？这可能需要将 IMC 框架扩展为可微分物理模拟器的接口，或引入基于物理的损失项。

2. **分层或全局规划策略。** 能否开发分层或全局规划的生成策略，以突破当前片段式自回归的长度限制？例如，先生成粗粒度的运动蓝图，再通过 IMC 注入细粒度细节——这种“先规划后细化”的范式可能从根本上解决长程依赖问题。

3. **自适应调制器。** 是否可以将 IMC 扩展为非线性或自适应的调制器，进一步提升对极端条件的泛化能力？当前线性交叉注意力设计简洁高效，但可能限制了调制函数的表达能力。引入门控机制或动态路由可能是一个方向。

4. **场景感知的运动合成。** 该框架如何适配到场景感知的运动合成任务中，例如结合环境上下文（障碍物、地形）？IMC 的模块化设计理论上允许插入新的注入路径，但环境上下文与运动风格的耦合方式需要重新设计。

5. **多条件冲突的显式仲裁。** 当语义、风格和历史信号指向矛盾的运动方向时，如何设计显式的仲裁机制以确保生成结果的可预测性？这可能需要引入条件优先级编码或基于注意力的动态加权策略。

### 四、知识库定位

MoCoDiff 在运动生成领域的知识谱系中占据以下位置：

- **方法类型：** 可控自回归扩散模型，属于扩散模型 + 自回归生成的混合范式。
- **核心创新：** 将多条件注入从“特征融合”升级为“动力学调制”，将自回归扩散从“条件拼接”升级为“受控马尔可夫过程”。
- **技术遗产：** 继承了扩散运动生成（MDM 系列）的去噪框架、CLIP/MotionCLIP 的多模态编码能力、以及自回归生成的序列建模范式，但在条件注入机制和时序动力学控制上做出了根本性改进。
- **下游影响：** 为多条件可控生成提供了“解耦注入 + 动力学控制”的通用设计模式，其 IMC 框架可潜在迁移至其他时序生成任务（如视频生成、音频合成）。

## 原文 PDF

![[paperPDFs/CVPR_2026/MoCoDiff_A_Controllable_Autoregressive_Diffusion_Model_for_Expressive_Motion_Generation.pdf]]
