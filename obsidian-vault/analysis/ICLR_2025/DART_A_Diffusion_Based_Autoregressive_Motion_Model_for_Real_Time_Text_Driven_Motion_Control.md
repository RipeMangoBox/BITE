---
title: "DART: A Diffusion-Based Autoregressive Motion Model for Real-Time Text-Driven Motion Control"
type: paper
paper_level: A
venue: ICLR
year: 2025
pdf_ref: paperPDFs/ICLR_2025/DART_A_Diffusion_Based_Autoregressive_Motion_Model_for_Real_Time_Text_Driven_Motion_Control.pdf
aliases:
- DD
- DART
tags:
- ICLR_2025
- topic/motion_animation
- topic/motion_animation/human_motion_generation
core_operator: "采用基于运动原语的自回归表示（H=2历史帧，F=8未来帧）和潜在扩散模型（VAE+denoiser），在紧凑的潜在空间内进行文本条件的运动原语生成；通过潜在噪声优化或强化学习在该潜在空间内实现精确的空间控制。"
primary_logic: "将长期运动分解为短运动原语，进行潜在空间的自回归生成，使模型能实时响应文本提示，并通过在潜在噪声空间中优化或学习策略，灵活实现文本语义与空间约束的统一。"
claims:
- "DART在文本条件时间运动组合任务中取得了最佳的FID，并在人类偏好研究中在运动真实性和语义对齐两方面均优于所有基线（包括FlowMDM）。"
- "DART的生成速度超过300帧/秒，延迟0.02秒，比FlowMDM快约10倍，且内存占用更少。"
- "消融实验证实：去除VAE会导致运动抖动（PJ和AUJ）显著增加；去除调度训练会导致R-Prec和FID急剧恶化。"
- "在文本条件目标到达任务中，DART的成功率达到100%，在成功率和到达时间上均优于GAMMA基线。"
---

# DART: A Diffusion-Based Autoregressive Motion Model for Real-Time Text-Driven Motion Control

> [!tip] 核心洞察
> 将长期运动分解为短运动原语，进行潜在空间的自回归生成，使模型能实时响应文本提示，并通过在潜在噪声空间中优化或学习策略，灵活实现文本语义与空间约束的统一。

| 字段 | 内容 |
|------|------|
| 中文题名 | DART：面向实时文本驱动运动控制的基于扩散的自回归运动模型 |
| 英文题名 | DART: A Diffusion-Based Autoregressive Motion Model for Real-Time Text-Driven Motion Control |
| 会议/期刊 | ICLR 2025 |
| Links | [paper](https://arxiv.org/abs/2412.01976) · [Project](https://zkf1997.github.io/DART/) |
| Topic | #topic/motion_animation #topic/motion_animation/human_motion_generation |
| Method | DART (DartControl) |
| Dataset | Text-conditioned temporal motion composition (human preference), Text-conditioned goal-reaching (walk) |

> [!tip] 效果简介
> - Text-conditioned temporal motion composition (human preference) 上，Realism preference (%) 为 53.3，对比 46.7 (FlowMDM)，变化 +6.6。
> - Text-conditioned temporal motion composition (human preference) 上，Semantic alignment preference (%) 为 51.3，对比 48.7 (FlowMDM)，变化 +2.6。
> - Text-conditioned goal-reaching (walk) 上，Success rate 为 1.0 ± 0.0，对比 0.95 ± 0.03 (GAMMA)，变化 +0.05。

## 概述

文本驱动的3D人体运动生成在实时在线场景中面临根本性瓶颈：现有方法多为离线批量生成孤立的短运动片段，无法根据连续变化的自然语言指令自回归地生成长期连续运动，同时对空间约束（如目标位置、场景几何）缺乏精确控制能力。DART（DartControl）针对这一瓶颈，提出了基于运动原语的自回归生成范式，将长期运动分解为短运动原语（历史帧H=2，未来帧F=8），在VAE压缩的紧凑潜在空间内通过扩散模型实现文本条件的实时运动生成，速度超过300帧/秒，延迟仅0.02秒，比离线基线FlowMDM（Barquero et al., 2024）快约10倍且内存占用更少。

在文本条件时间运动组合任务中，DART取得了最佳的FID指标，并在人类偏好研究中于运动真实性和语义对齐两方面均优于所有基线（包括FlowMDM），其中真实性偏好率达53.3%，语义对齐偏好率达51.3%。在文本条件目标到达任务中，DART的成功率达到100%，优于GAMMA基线（Zhang & Tang, 2022）的95%，且到达时间缩短约45%。消融实验进一步证实：去除VAE会导致运动抖动（峰值急动度PJ从0.06升至0.20），去除调度训练则使R-Prec从0.62骤降至0.39、FID从3.79升至8.08，验证了各模块的关键作用。

DART的核心洞察在于：将长期运动分解为短原语进行潜在空间自回归生成，使模型能实时响应文本提示；同时通过在潜在噪声空间中优化或使用强化学习（PPO）训练策略，灵活实现文本语义与空间约束的统一。该方法在方法谱系上位于扩散生成模型、运动原语表示与潜在空间控制的交叉点，为实时文本驱动运动控制提供了新的技术路线。

## 背景与动机

### 文本驱动人体运动生成的需求转变

文本驱动的人体运动生成旨在根据自然语言描述合成逼真的3D人体动作序列，在动画制作、游戏开发、虚拟现实和人机交互等领域具有广泛应用。近年来，该领域的研究重点正从**离线、孤立的短运动生成**向**在线、实时的长序列运动控制**转变。实际应用场景——如交互式角色动画、实时人机协作——要求模型能够根据连续输入的文本指令，自回归地生成长期连贯的运动，并能精确响应空间约束（如目标位置、场景几何）。

### 现有方法的瓶颈

当前主流的文本驱动运动生成方法存在三个核心瓶颈：

**离线生成范式限制。** 大多数现有方法将运动生成视为离线任务，一次性生成整段孤立运动序列。这种范式无法支持在线场景下根据流式文本输入实时调整运动的需求。即使是支持时间运动组合的方法，如 **FlowMDM** (Barquero et al., 2024)，也仅能在离线设定下将多段运动拼接，缺乏真正的实时自回归生成能力。

**空间控制能力缺失。** 现有方法多聚焦于文本语义到运动的映射，忽视了空间约束的精确控制。在真实应用中，生成的运动不仅需要符合文本描述（如“走向桌子”），还需满足目标位置、场景避碰等空间条件。基于扩散噪声优化的方法如 **DNO** (Karunratanakul et al., 2024) 虽能实现一定程度的控制，但其在原始运动空间中进行优化的范式计算开销大且难以扩展到实时场景。

**长序列生成的稳定性不足。** 自回归生成长序列时，模型容易遭遇分布外的历史-文本组合，导致运动质量随序列增长而急剧退化。现有方法缺乏有效的训练策略来保证长程生成的一致性和可控性。

### DART的动机与核心思路

针对上述瓶颈，DART提出了一种**基于运动原语的自回归潜在扩散模型**，其核心动机可归纳为三点：

1. **实时在线生成**：将长期运动分解为短运动原语（历史帧 $H=2$，未来帧 $F=8$），通过自回归方式逐段生成，使模型能以超过300帧/秒的速度实时响应文本提示。

2. **潜在空间的高效控制**：利用VAE将运动原语压缩到紧凑的潜在空间，在该空间内进行扩散生成和噪声优化。潜在空间的低维性和平滑性使得空间控制（目标到达、运动内插、人-场景交互）更加高效和稳定。

3. **调度训练保障长程稳定性**：通过调度训练策略，使模型在训练阶段就接触多样化的历史-文本组合，从而在推理时能有效应对分布外输入，保证长序列生成的质量和文本可控性。

DART的目标是统一文本语义理解和空间约束控制，在一个框架内实现实时、可控的长期运动生成，为交互式角色动画等应用提供实用解决方案。

## 核心创新

DART 的核心创新在于将**长期连续运动生成**重新定义为**短运动原语的自回归潜在扩散**问题，从而在实时在线场景下同时实现文本语义响应与精确空间控制。相对于现有离线生成方法，DART 在三个关键维度上做出了根本性改变。

### 1. 运动表示：从全序列到运动原语

现有文本驱动运动生成方法（如 **FlowMDM**，Barquero et al., 2024）通常将整段运动作为单一序列进行离线批量生成，无法在实时场景中根据连续变化的文本输入自回归地产生长期运动。DART 将运动建模为**运动原语的序列组合**，每个原语 $\mathbf{P}^i = [\mathbf{H}^i, \mathbf{X}^i]$ 包含 $H=2$ 帧历史运动与 $F=8$ 帧未来运动（见 Section 3.1）。这种重叠的短片段表示使模型能够以自回归方式逐步生成运动，每次仅需预测未来 8 帧，从而将生成延迟压缩至 0.02 秒，生成速度超过 300 帧/秒（RTX 4090）。

这一改变的因果机制在于：运动原语将长期生成的分布外推问题分解为局部条件生成问题，大幅降低了单步生成的难度。消融实验证实，若将原语缩减为单帧预测（$H=1, F=1$），模型几乎无法响应文本提示，且 FID 从 3.79 急剧恶化至 10.31（Table 5），验证了多帧原语表示对文本可控性的关键作用。

### 2. 生成范式：从离线批量到在线自回归

FlowMDM 等离线方法需要预先获取完整的文本序列，生成整个运动后再输出，无法适应实时交互场景。DART 采用**在线自回归生成范式**：给定种子历史运动 $\bar{\mathbf{H}}_{seed}$ 和在线文本序列 $C$，模型通过算法 Alg. 1 逐原语生成未来帧，最终拼接为完整运动 $\mathbf{M} = [\bar{\mathbf{H}}_{seed}, \mathbf{X}^1, ..., \mathbf{X}^N]$。

这一范式的核心瓶颈在于自回归过程中的误差累积与分布偏移。DART 通过**调度训练**策略解决此问题：在训练时随机采样历史-未来原语对，使模型学习从任意中间状态继续生成的能力。消融实验表明，去除调度训练会导致分段 R-Prec 从 0.62 骤降至 0.39，FID 从 3.79 升至 8.08（Table 5），证明调度训练对分布式外推和文本可控性至关重要。

### 3. 运动空间：从原始运动到 VAE 压缩的潜在空间

直接在原始运动空间进行扩散生成面临维度高、噪声大的问题。DART 引入**变分自编码器**将运动原语压缩到紧凑的潜在空间，潜在扩散模型仅需在该低维空间中进行去噪生成。VAE 编码器以历史帧 $\mathbf{H}$ 为条件将未来帧 $\mathbf{X}$ 编码为潜在变量 $\mathbf{z}$，解码器则从 $\mathbf{z}$ 和 $\mathbf{H}$ 重建 $\mathbf{X}$（Figure 1）。

这一改变的因果机制是双重的：**运动平滑性**与**控制可优化性**。VAE 的正则化效应有效滤除了运动噪声——消融实验显示，去除 VAE 会导致峰值急动度 PJ 从 0.06 升至 0.20，急动度积分 AUJ 从 0.21 升至 0.96（Table 5），表明 VAE 显著抑制了运动抖动。更重要的是，紧凑的潜在空间使得空间控制目标可以直接重参数化为对初始噪声 $\mathbf{Z}_T$ 的优化问题：

$$\mathbf{Z}_{T}^{*} = \operatorname{argmin}_{\mathbf{Z}_{T}} \mathcal{F}(\Pi(\mathrm{ROLLOUT}(\mathbf{Z}_{T}, \mathbf{H}_{seed}, C)), g) + cons(\mathrm{ROLLOUT}(\mathbf{Z}_{T}, \mathbf{H}_{seed}, C))$$

这一重参数化使得梯度下降或强化学习策略可以高效地在潜在空间中搜索满足空间约束的噪声变量，而无需在原始高维运动空间中进行昂贵的优化。在文本条件目标到达任务中，DART 的成功率达到 100%，到达时间仅 17.08 秒，显著优于 **GAMMA**（Zhang & Tang, 2022）的 95% 成功率和 31.44 秒到达时间（Table 4）。

### 创新总结

DART 的三项核心改变形成了一条因果链路：**运动原语表示**使自回归在线生成成为可能，**VAE 潜在空间**在保证运动质量的同时为空间控制提供了可优化的低维流形，**调度训练**则确保了自回归长序列生成的稳定性。这一组合使 DART 成为首个在实时条件下同时实现文本语义对齐与精确空间控制的运动生成方法——比 FlowMDM 快约 10 倍，且在人类偏好研究中在运动真实性和语义对齐两方面均优于所有基线（Table 2）。

## 整体框架

DART 的整体 pipeline 围绕“运动原语的自回归潜在扩散”展开，将长期运动生成分解为短原语的在线组合，并在紧凑的潜在空间中完成文本条件生成与空间控制。系统由五个核心模块构成，形成“编码—扩散—自回归—控制”的闭环。

### 1. 运动原语表示与自回归分解

DART 将长期人体运动建模为运动原语的序列组合。每个运动原语 $\mathbf{P}^i = [\mathbf{H}^i, \mathbf{X}^i]$ 包含 $H$ 帧历史运动 $\mathbf{H}^i$ 和 $F$ 帧未来运动 $\mathbf{X}^i$，相邻原语之间通过重叠的历史帧实现时序衔接。完整运动序列由种子历史帧和所有未来原语拼接而成：$\mathbf{M} = [\bar{\mathbf{H}}_{seed}, \mathbf{X}^1, ..., \mathbf{X}^N]$。实验设定 $H=2$，$F=8$，该参数在消融实验中证实了其有效性——若退化为单帧预测（$H=1, F=1$），模型几乎无法响应文本提示，且 FID 从 3.79 飙升至 10.31。

### 2. 运动原语 VAE：潜在空间压缩

运动原语 VAE 是整个 pipeline 的“压缩层”。编码器以历史帧 $\mathbf{H}$ 为条件，将未来帧 $\mathbf{X}$ 压缩为紧凑的潜在变量 $\mathbf{z}$；解码器则根据同一历史条件和潜在变量重建未来帧。这一设计的关键因果作用是滤除运动噪声：消融实验显示，去除 VAE 会导致峰值急动度从 0.06 升至 0.20，急动度积分从 0.21 升至 0.96，表明 VAE 有效抑制了帧间抖动。

### 3. 潜在扩散去噪模型：文本条件生成核心

去噪模型 $\mathcal{G}$ 在潜在空间中执行文本条件生成。其输入包括噪声潜在变量 $\mathbf{z}_t$、扩散时间步 $t$、历史帧 $\mathbf{H}$ 和文本提示 $c$，输出为预测的干净潜在变量 $\hat{\mathbf{z}}_0$。时间步通过小型 MLP 嵌入，文本提示使用 CLIP 文本编码器编码。反向过程均值由预测的干净潜在变量推导：

$$\pmb{\mu}_t = \frac{\sqrt{\bar{\alpha}_{t-1}}\beta_t}{1-\bar{\alpha}_t}\mathcal{G}(\mathbf{z}_t,t,\mathbf{H},c) + \frac{\sqrt{\alpha_t}(1-\bar{\alpha}_{t-1})}{1-\bar{\alpha}_t}\mathbf{z}_t$$

训练时，VAE 的编码器和解码器权重保持固定，仅训练去噪模型，采用 DDPM 风格的简单去噪损失 $L_{\text{simple}}$。采样时引入分类器自由引导，调节文本条件强度：

$$\mathcal{G}_w(\mathbf{z}_t,t,\mathbf{H},c) = \mathcal{G}(\mathbf{z}_t,t,\mathbf{H},\emptyset) + w\cdot(\mathcal{G}(\mathbf{z}_t,t,\mathbf{H},c) - \mathcal{G}(\mathbf{z}_t,t,\mathbf{H},\emptyset))$$

### 4. 自回归 Rollout：在线运动生成

给定种子历史帧 $\mathbf{H}_{seed}$ 和在线文本提示序列 $C$，自回归 Rollout 算法（Algorithm 1）逐原语生成长期运动：每步以当前历史帧和文本提示为条件，通过去噪模型采样潜在变量，经解码器重建未来帧，再将最新帧滚动为下一原语的历史条件。这一设计使 DART 的生成速度超过 300 帧/秒（单张 RTX 4090），延迟仅 0.02 秒，比离线基线 FlowMDM 快约 10 倍，且内存占用显著更低。

### 5. 空间控制：潜在噪声优化与强化学习策略

DART 在潜在空间内实现精确的空间控制，提供两种互补机制：

- **潜在噪声优化**：将运动控制目标 $\mathbf{M}^{*} = \operatorname{argmin}_{\mathbf{M}} \mathcal{F}(\Pi(\mathbf{M}), g) + cons(\mathbf{M})$ 重参数化到潜在噪声空间，通过梯度下降优化初始噪声 $\mathbf{Z}_T$，使 Rollout 生成的运动满足空间目标 $g$ 和场景约束。
- **强化学习控制策略**：采用 Actor-Critic 架构和 PPO 算法训练策略模型，在潜在动作空间中直接输出控制信号。预训练的 DART 去噪器和解码器将潜在动作转化为运动帧，末帧经规范化后作为下一时间步的历史条件反馈给策略模型（Figure 2）。

### 输入输出流总结

系统接收**在线文本提示序列**、**种子历史帧**和**可选的空间目标**作为输入，输出为**长期连续运动序列**。数据流路径为：文本 + 历史 → 去噪模型（潜在空间）→ 解码器（运动空间）→ 历史更新 → 下一原语生成，形成闭环自回归推理。当需要空间控制时，控制信号通过潜在噪声优化或 RL 策略注入到去噪模型的初始噪声或潜在动作中。

### 补充图表

![[assets/figures/papers/paper_list_l13_DART_A_Diffusion_Based_Autoregressive_Motion_Model_for_Real_Time_Text_Dr/figures/010_Figure_5.jpg]]
*Figure 5: (a) Crawling sequence generated by DART (b) Physics-based motion tracking result Figure 5: We demonstrate an example of integrating DART with the physics-based motion tracking method PHC (Luo et al., 2023) to achieve more physically plausible motions. The left image illustrates a crawling sequence generated by DART, exhibiting artifacts such as hand-floor penetration. The right image displays the physics-based motion tracking outcome applied to the raw generated sequence, which enhances joint-floor contact and resolves the hand-floor penetration issue*

![[assets/figures/papers/paper_list_l13_DART_A_Diffusion_Based_Autoregressive_Motion_Model_for_Real_Time_Text_Dr/figures/001_Figure_1.jpg]]
*Figure 1: Architecture illustration of DART. The encoder network compresses the future frames $\mathbf { X }$ = [ $\mathbf { x } ^ { 1 }$ , . . . , $\mathbf { x } ^ { F }$ ] into a latent variable, conditioned on the history frames $\mathbf { H }$ = [ $\mathbf { h } ^ { 1 }$ , . . . , $\mathbf { h } ^ { H }$ ] The decoder network reconstructs the future frames conditioned on the history frames and the latent sample. The denoiser network predicts the clean latent sample $\hat { \mathbf { z } } _ { 0 }$ conditioned on the noising step, text prompt, history frames, and noised latent sample $\mathbf { z } _ { t }$ . During the denoiser training, the encoder and decoder network weights remain fixed

## 核心模块与公式推导

DART 的核心架构由三个紧密协作的模块构成：**运动原语 VAE**、**潜在扩散去噪模型** 和**自回归 Rollout 算法**，三者共同支撑在线文本条件运动生成与控制。

### 运动原语表示

DART 将长期人体运动建模为运动原语（motion primitives）的序列组合。每个运动原语 $\mathbf{P}^i = [\mathbf{H}^i, \mathbf{X}^i]$ 包含 $H$ 帧历史运动 $\mathbf{H}^i$ 和 $F$ 帧未来运动 $\mathbf{X}^i$。实验设定 $H=2$、$F=8$，相邻原语之间通过重叠的历史帧实现时序衔接。给定种子历史 $\bar{\mathbf{H}}_{seed}$ 和 $N$ 个未来原语，完整运动序列通过拼接得到：

$$\mathbf{M} = [\bar{\mathbf{H}}_{seed}, \mathbf{X}^1, ..., \mathbf{X}^N]$$

这种表示将长期生成分解为短原语的在线预测，是实现自回归实时生成的结构基础。

### 运动原语 VAE

VAE 模块负责将运动原语压缩到紧凑的潜在空间，并在生成阶段将潜在变量解码回运动帧。编码器以历史帧 $\mathbf{H}$ 为条件，将未来帧 $\mathbf{X}$ 编码为潜在变量；解码器则以历史帧 $\mathbf{H}$ 和潜在样本为条件重建未来帧。VAE 的核心作用在于滤除运动噪声——消融实验证实，去除 VAE（DART-VAE）会导致峰值急动度（PJ）从 0.06 升至 0.20，急动度积分（AUJ）从 0.21 升至 0.96，表明 VAE 有效压缩了高频抖动成分。

### 潜在扩散去噪模型

去噪模型 $\mathcal{G}$ 以扩散步 $t$、文本提示 $c$、历史帧 $\mathbf{H}$ 和加噪潜在变量 $\mathbf{z}_t$ 为条件，预测干净潜在变量 $\hat{\mathbf{z}}_0$：

$$\hat{\mathbf{z}}_0 = \mathcal{G}(\mathbf{z}_t, t, \mathbf{H}, c)$$

扩散步 $t$ 通过小型 MLP 嵌入，文本提示 $c$ 使用 CLIP 文本编码器编码。训练阶段编码器和解码器权重固定，仅优化去噪模型。训练采用 DDPM 风格的简单去噪损失：

$$L_{\mathrm{simple}} = \mathbb{E}_{(\mathbf{z}_0,c)\sim q(\mathbf{z}_0,c), t\sim[1,T], \epsilon\sim\mathcal{N}(\mathbf{0},\mathbf{I})} \mathcal{F}(\mathcal{G}(\mathbf{z}_t, t, \mathbf{H}, c), \mathbf{z}_0)$$

采样时，从预测的干净潜在变量推导反向过程均值 $\pmb{\mu}_t$：

$$\pmb{\mu}_t = \frac{\sqrt{\bar{\alpha}_{t-1}}\beta_t}{1-\bar{\alpha}_t}\mathcal{G}(\mathbf{z}_t,t,\mathbf{H},c) + \frac{\sqrt{\alpha_t}(1-\bar{\alpha}_{t-1})}{1-\bar{\alpha}_t}\mathbf{z}_t$$

为增强文本条件控制强度，采样时采用分类器自由引导（classifier-free guidance）：

$$\mathcal{G}_w(\mathbf{z}_t,t,\mathbf{H},c) = \mathcal{G}(\mathbf{z}_t,t,\mathbf{H},\emptyset) + w\cdot(\mathcal{G}(\mathbf{z}_t,t,\mathbf{H},c) - \mathcal{G}(\mathbf{z}_t,t,\mathbf{H},\emptyset))$$

其中 $w$ 为引导尺度，调节文本条件的控制力度。

### 自回归 Rollout 算法

给定种子历史 $\mathbf{H}_{seed}$ 和在线文本提示序列 $C$，DART 通过自回归方式逐原语生成长期运动：每一步将上一原语的最后 $H$ 帧作为当前步的历史条件，结合当前文本提示，通过去噪采样生成新的未来帧 $\mathbf{X}^i$，然后滑动窗口进入下一步。该算法使 DART 能够在文本序列驱动下实时生成连续运动，生成速度超过 300 帧/秒（单张 RTX 4090 GPU），延迟仅约 0.02 秒。

### 空间控制模块

DART 提供两种在潜在空间内实现精确空间控制的方式：

**潜在噪声优化**：将运动控制形式化为最小化与空间目标 $g$ 距离的优化问题，并通过 DDIM 确定性采样重参数化到潜在噪声空间：

$$\mathbf{Z}_{T}^{*} = \operatorname{argmin}_{\mathbf{Z}_{T}} \mathcal{F}(\Pi(\mathrm{ROLLOUT}(\mathbf{Z}_{T}, \mathbf{H}_{seed}, C)), g) + cons(\mathrm{ROLLOUT}(\mathbf{Z}_{T}, \mathbf{H}_{seed}, C))$$

其中 $\mathcal{F}$ 为距离准则函数，$cons$ 为场景/物理约束项。通过梯度下降直接优化初始噪声 $\mathbf{Z}_T$，即可生成满足空间约束的运动。

**强化学习控制策略**：采用 Actor-Critic 架构，使用 PPO 算法在潜在动作空间中训练策略模型。预训练的 DART 去噪器和解码器将潜在动作转化为运动帧，最后一帧经规范化后作为下一步的历史条件反馈给策略模型，形成闭环控制。该策略在文本条件目标到达任务中实现了 100% 的成功率。

## 实验与分析

### 评估基准与设置

DART 在 BABEL 数据集上进行训练与评估，所有方法使用相同的训练/测试分割和运动持续时长，确保公平对比。评估涵盖三个核心任务：**文本条件时间运动组合**（text-conditioned temporal motion composition）、**文本条件运动内插**（text-conditioned motion in-between）和**文本条件目标到达**（text-conditioned goal-reaching）。定量指标包括 FID（Frechet Inception Distance）、R-Precision（R-Prec）、峰值急动度（Peak Jitter, PJ）、急动度积分（Area Under Jitter, AUJ）等。人类偏好研究通过 Amazon Mechanical Turk 进行，每个对比由 3 位独立参与者投票，共 256 组，分别评估运动真实性和文本语义对齐。

### 主实验结果

#### 文本条件时间运动组合

Table 1 展示了 DART 与多个基线的定量对比。DART 在分段评估（segment evaluation）和过渡评估（transition evaluation）中均取得了**最优的 FID**，表明其生成的运动分布与真实数据最为接近。在 R-Precision 指标上，DART 同样表现优异，验证了其对文本语义的响应能力。

![[assets/figures/papers/paper_list_l13_DART_A_Diffusion_Based_Autoregressive_Motion_Model_for_Real_Time_Text_Dr/figures/003_Table_1.jpg]]
*Table 1: Quantitative evaluation results on text-conditioned temporal motion composition. The first row includes the metrics of the dataset for reference. Symbol ‘→’ denotes that closer to the dataset reference is better and $\cdot _ { \pm }$ , indicates the 95% confidence interval. Bold and blue texts indicate the best and second best results excluding the dataset, respectively

Table 2 报告了人类偏好研究结果。在运动真实性方面，DART 以 **53.3%** 的偏好率优于 FlowMDM（46.7%）；在语义对齐方面，DART 以 **51.3%** 的偏好率领先。值得注意的是，FlowMDM 是离线时间运动组合的强基线，DART 在在线自回归设定下仍能超越，证明了运动原语表示与潜在扩散架构的有效性。

![[assets/figures/papers/paper_list_l13_DART_A_Diffusion_Based_Autoregressive_Motion_Model_for_Real_Time_Text_Dr/figures/004_Table_2.jpg]]
*Table 2: Human preference study results comparing our method against baselines in generation realism and motion-text semantic alignment on text-conditioned temporal motion composition. We report the percentage of each method being voted better than the other (Ours vs. Baselines)*

#### 文本条件运动内插

Table 3 展示了运动内插任务的定量结果。DART 在目标误差（Goal error）上仅为 **0.59 ± 0.01 cm**，在所有对比方法中表现最优。该任务要求模型根据给定的起始帧、结束帧和文本提示生成中间运动，DART 通过潜在噪声优化实现了精确的空间约束满足。

![[assets/figures/papers/paper_list_l13_DART_A_Diffusion_Based_Autoregressive_Motion_Model_for_Real_Time_Text_Dr/figures/005_Table_3.jpg]]
*Table 3: Quantitative evaluation of text-conditioned motion in-between. The best results excluding the dataset are in bold and ‘±’ indicates the 95% confidence interval*

#### 文本条件目标到达

Table 4 报告了目标到达控制的结果。在“walk”动作类别上，DART 的成功率达到 **100%**（1.0 ± 0.0），优于 GAMMA 基线的 95%（0.95 ± 0.03）。更关键的是，DART 的平均到达时间仅为 **17.08 ± 0.05 秒**，而 GAMMA 需要 31.44 ± 2.58 秒，效率提升约 45.7%。这一结果验证了基于 PPO 强化学习的控制策略在潜在动作空间中的决策效率显著优于传统方法。

![[assets/figures/papers/paper_list_l13_DART_A_Diffusion_Based_Autoregressive_Motion_Model_for_Real_Time_Text_Dr/figures/007_Table_4.jpg]]
*Table 4: Quantitative evaluation of text-conditioned goal-reaching controller. The best results are in bold and ‘±’ indicates the 95% confidence interval*

### 推理效率

DART 在单张 RTX 4090 GPU 上实现了**超过 300 帧/秒**的生成速度，延迟仅约 0.02 秒。与离线基线 FlowMDM 相比，DART 的生成速度约快 10 倍，且内存占用显著降低。这一效率优势源于运动原语的自回归生成范式——每次仅需预测 8 帧未来运动，而非一次性生成整段序列。

### 消融实验

Table 5 系统性地验证了 DART 各设计组件的贡献：

![[assets/figures/papers/paper_list_l13_DART_A_Diffusion_Based_Autoregressive_Motion_Model_for_Real_Time_Text_Dr/figures/009_Table_5.jpg]]
*Table 5: Ablation studies results on text-conditioned temporal motion composition. The first row includes the metrics of the dataset for reference. Symbol ‘→’ denotes that closer to the dataset reference is better and ‘±’ indicates the 95% confidence interval*

**VAE 的作用。** 去除 VAE（DART-VAE 变体）直接在原始运动空间进行扩散生成，导致 PJ 从 0.06 急剧上升至 **0.20**，AUJ 从 0.21 上升至 **0.96**。这证实了 VAE 的潜在空间压缩有效滤除了运动噪声，是生成平滑运动的关键。

**调度训练的作用。** 去除调度训练（DART-schedule 变体）后，分段 R-Prec 从 0.62 暴跌至 **0.39**，FID 从 3.79 恶化至 **8.08**。这表明调度训练对于模型在自回归外推过程中保持文本可控性和分布稳定性至关重要。

**运动原语表示的作用。** 采用单帧预测（H=1, F=1）的变体几乎无法响应文本提示，R-Prec 仅为 0.29，FID 高达 10.31。这证明了 H=2、F=8 的运动原语设计是模型理解文本语义并生成连贯运动的基础。

**扩散步数的影响。** 将扩散步数从 100 步减少至 10 步以内对性能影响不显著，但极端减少至 2 步会导致 FID 明显升高。因此 DART 采用 10 步扩散采样，在生成质量与推理速度之间取得平衡。

### 失败模式与局限性

尽管 DART 在定量和定性评估中表现优异，但仍存在以下局限：

1. **动作词汇受限。** DART 的动作类别受限于 BABEL 数据集的标注范围，无法有效泛化到开放词汇的文本描述。这是当前文本驱动运动生成领域的共性问题。
2. **物理合理性不足。** 作为纯运动学方法，DART 可能产生滑步、浮空、穿透等物理不合理的运动。Figure 5 展示了将 DART 生成的爬行序列输入物理模拟追踪方法 PHC 后，能够修复手部穿地等伪影，表明结合物理模拟是可行的后处理方案。
3. **长序列稳定性。** 自回归生成长序列时，尽管调度训练提升了稳定性，模型仍可能遇到分布外的历史-文本组合，导致动作质量逐渐下降。这一问题的根本解决需要更强大的数据增强或在线适应机制。

### 补充图表

![[assets/figures/papers/paper_list_l13_DART_A_Diffusion_Based_Autoregressive_Motion_Model_for_Real_Time_Text_Dr/figures/006_Figure_3.jpg]]
*Figure 3: Illustrations of human-scene interaction generation given text prompts and goal pelvis joint location (visualized as a red sphere). Best viewed in the supplementary video*

## 方法谱系与知识库定位

### 1. 与现有方法的关系与定位

DART 的核心贡献在于将**离线、孤立的文本驱动运动生成**范式转变为**在线、自回归的实时运动控制**框架。这一转变通过三个关键设计实现：运动原语表示、潜在扩散生成和潜在空间控制策略。

**与离线文本-运动生成基线的关系。** 现有主流方法（如 MDM、MLD、MotionDiffuse）将运动建模为固定长度的完整序列，一次生成整段运动。FlowMDM（Barquero et al., 2024）通过时间运动组合实现了长序列生成，但仍是离线批处理模式。DART 采用运动原语表示（历史帧 H=2，未来帧 F=8），将长期运动分解为重叠的短片段，以自回归方式逐原语生成。这一设计使 DART 能够实时响应连续文本输入，生成速度超过 300 帧/秒，延迟仅 0.02 秒，比 FlowMDM 快约 10 倍且内存占用显著降低。在人类偏好研究中，DART 在运动真实性和语义对齐两方面均优于 FlowMDM（真实性偏好 53.3% vs 46.7%，语义对齐偏好 51.3% vs 48.7%）。

**与扩散噪声优化控制方法的关系。** DNO（Karunratanakul et al., 2024）通过在扩散噪声空间进行梯度优化实现运动控制，但操作于原始运动空间。DART 将控制问题重参数化到紧凑的潜在噪声空间（通过 VAE 压缩），在该空间内执行潜在噪声优化或强化学习策略，实现了更高效的空间约束控制。在文本条件目标到达任务中，DART 的成功率达 100%（行走动作），优于 GAMMA 基线（Zhang & Tang, 2022）的 95%，且到达时间显著缩短（17.08s vs 31.44s）。

**与运动原语方法的关系。** DART 的运动原语表示借鉴了 GAMMA（Zhang & Tang, 2022）的框架，但将其从目标条件到达任务扩展为通用的文本条件生成任务。关键区别在于：GAMMA 使用原语进行目标驱动的策略学习，而 DART 在原语空间上构建了文本条件的扩散生成模型，使原语表示成为连接文本语义与运动控制的统一接口。

### 2. 方法适用边界

**数据依赖性。** DART 的动作词汇受限于训练数据（BABEL 数据集）的动作类别。BABEL 涵盖约 40 种动作类型，DART 无法有效泛化到开放词汇的文本描述。对于训练数据中未见的动作类别或复合语义，模型可能产生语义错位或质量下降的运动。

**物理合理性。** 作为纯运动学方法，DART 不显式建模物理约束（如接触力、地面反作用力）。生成的运动可能出现滑步、浮空、肢体穿透等物理不合理现象。论文展示了通过物理模拟追踪方法 PHC（Luo et al., 2023）对 DART 输出进行后处理的可行性（如修复爬行动作中的手-地面穿透），但这属于外部补救而非框架内解决。

**自回归稳定性。** 尽管调度训练提升了分布式外推能力，但在长序列生成中，DART 仍可能遇到分布外的历史-文本组合，导致动作质量逐渐下降。消融实验表明，去除调度训练会导致 R-Prec 从 0.62 骤降至 0.39，FID 从 3.79 升至 8.08，说明调度训练对稳定性至关重要但并非完全消除退化风险。

**空间控制的精度-效率权衡。** 潜在噪声优化控制（基于梯度下降）提供精确的空间约束满足，但每次优化需多步迭代；强化学习控制策略（基于 PPO）在推理时更高效，但策略训练需要额外的环境交互。两种方案适用于不同的实时性要求场景。

### 3. 局限性

1. **动作词汇封闭性。** DART 的文本条件能力受 BABEL 数据集动作类别限制，无法处理开放词汇的文本描述。这是当前文本-运动生成领域的共性瓶颈，源于高质量 3D 运动数据的稀缺。

2. **物理不合理性。** 运动学生成框架不保证物理约束满足，可能产生不符合生物力学规律的运动。论文仅展示了与 PHC 物理模拟的后处理集成，未提供端到端的物理感知生成方案。

3. **长序列退化风险。** 自回归框架的误差累积效应在极端长序列中可能放大，调度训练虽缓解但未根除该问题。

4. **粗粒度文本标注的语义错位。** BABEL 数据集使用句子级文本标签标注多动作序列，可能导致文本与具体运动帧之间的语义错位，影响模型的细粒度文本-运动对齐能力。

### 4. 开放性研究问题

1. **开放词汇运动生成。** 如何利用互联网视频或生成模型（如视频扩散模型）扩展 3D 人体运动数据，实现开放词汇的文本条件运动生成？这需要解决从 2D 视频估计 3D 运动、文本-运动自动标注等子问题。

2. **自动化运动标注。** 能否利用视觉语言模型（VLM）自动为大规模运动数据提供帧对齐的精细文本标注？当前 BABEL 的句子级标注粒度限制了模型对原子动作的语义理解，分层标注可能同时捕获细粒度原子语义和全局序列语义。

3. **分层潜在空间设计。** 当前 DART 的潜在空间仅编码单个运动原语。分层潜在空间是否能同时有效捕获细粒度的原子语义（帧级）和全局序列级语义（动作过渡、意图），以提升长序列生成的一致性和可控性？

4. **物理感知的端到端生成。** 能否将物理约束（如接触力、动量守恒）直接嵌入扩散生成过程或潜在空间，实现物理合理运动的内生生成，而非依赖后处理物理模拟？

5. **多模态空间控制的统一。** 当前 DART 的空间控制主要针对目标位置（如骨盆关节位置）。如何统一处理更复杂的空间约束类型（如场景几何避碰、多目标路径规划、人际交互空间），并在统一框架内保持实时性？

## 原文 PDF

![[paperPDFs/ICLR_2025/DART_A_Diffusion_Based_Autoregressive_Motion_Model_for_Real_Time_Text_Driven_Motion_Control.pdf]]
