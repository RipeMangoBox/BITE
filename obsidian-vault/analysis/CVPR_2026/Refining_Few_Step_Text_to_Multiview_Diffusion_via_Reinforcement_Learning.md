---
title: Refining Few-Step Text-to-Multiview Diffusion via Reinforcement Learning
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Refining_Few_Step_Text_to_Multiview_Diffusion_via_Reinforcement_Learning.pdf
project_link: null
code_link: "https://github.com/ZiyiZhang27/MVC-ZigAL"
aliases:
- MZ
- RFSTMDRL
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 引入多视图联合MDP建模所有视图，通过自反思zigzag采样构造结构化优势信号，并利用拉格朗日对偶约束优化自动平衡单视图保真度与跨视图一致性。
primary_logic: 利用自反思采样（ZMV-Sampling）产生的自改进轨迹作为参考，学习其相对优势而非绝对奖励，能够在少步条件下获得更强的梯度信号；同时将单视图奖励作为主目标、多视图奖励作为约束，通过自适应原-对偶更新与自定节奏阈值课程动态协调两者。
claims:
- MV-ZigAL在HyperScore所有子指标及PickScore上均超越MV-PG、MV-DPO、MV-RDL等多视图基线。
- 在MATE-3D分布外基准上，MVC-ZigAL以极低NFE（4/8）显著超过SPAD、MV-Adapter等SOTA方法，且ImageReward从-0.846跃升至0.865。
- 消融实验证实first-step zigzag调度、自适应阈值和自适应步长均对最终性能有独立贡献。
- 动物提示集 (45 prompts, 8 steps, 6 views) 上 HyperScore Overall = 9.17
---

# Refining Few-Step Text-to-Multiview Diffusion via Reinforcement Learning

> [!tip] 核心洞察
> 利用自反思采样（ZMV-Sampling）产生的自改进轨迹作为参考，学习其相对优势而非绝对奖励，能够在少步条件下获得更强的梯度信号；同时将单视图奖励作为主目标、多视图奖励作为约束，通过自适应原-对偶更新与自定节奏阈值课程动态协调两者。

| 字段 | 内容 |
|------|------|
| 中文题名 | 通过强化学习精炼少步文本到多视图扩散 |
| 英文题名 | Refining Few-Step Text-to-Multiview Diffusion via Reinforcement Learning |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2505.20107) · [Code](https://github.com/ZiyiZhang27/MVC-ZigAL) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | MVC-ZigAL |
| Dataset | MATE-3D |

> [!tip] 效果简介
> - 动物提示集 (45 prompts, 8 steps, 6 views) 上，HyperScore Overall 9.17 vs 7.23 (+1.94)。
> - MATE-3D (NFE=8) 上，HyperScore Overall 7.04 vs 6.67 (+0.37)。
> - MATE-3D (NFE=8, large-scale) 上，ImageReward 0.865 vs -0.846 (+1.711)。

## 概述

**问题瓶颈**：现有的强化学习微调方法专为单图像扩散模型设计，将其直接迁移到文本到多视图（Text-to-Multiview, T2MV）生成时，面临两个根本性困难。其一，这些方法将每个视图视为独立的去噪过程，忽略了多视图之间必须保持的跨视角一致性；其二，在少步推理（如4步或8步）条件下，奖励分布高度集中，导致策略梯度信号极其微弱，难以驱动有效的策略改进。

**核心方法**：本文提出 **MVC-ZigAL**，一个专为少步T2MV扩散模型设计的强化学习微调框架。其核心创新由三个相互协同的机制构成：

1. **多视图联合MDP建模**：将所有视图的生成过程统一建模为一个多视图马尔可夫决策过程，使用联合视图奖励函数评估整体生成质量，从根本上解决视图间协调问题。
2. **自反思zigzag优势学习**：引入ZMV-Sampling（zigzag多视图采样），通过在首步交替使用高引导去噪和低引导反转，生成高质量的自反思参考轨迹。模型学习的是参考轨迹与标准采样轨迹之间的相对优势，而非绝对奖励值，从而在少步条件下获得更强的梯度信号。
3. **多视图约束优化**：将单视图保真度作为主优化目标，将联合视图一致性作为约束条件，通过拉格朗日对偶框架将二者统一。配合自适应步长的原-对偶更新和自定节奏阈值课程学习，实现单视图质量与跨视图一致性之间的自动平衡。

**主要结果**：在训练提示集上，MVC-ZigAL的HyperScore Overall达到9.17，较基线模型（7.23）提升1.94；在MATE-3D分布外基准上，以仅8次函数评估（NFE）的极低推理成本，HyperScore Overall达到7.04，超越MV-Adapter等SOTA方法，且ImageReward从-0.846跃升至0.865，实现了从负到正的根本性质变。消融实验进一步证实，首步zigzag调度、自适应阈值课程和自适应步长原-对偶更新均对最终性能有独立且显著的贡献。

## 背景与动机

### 问题背景：少步文本到多视图生成的效率与质量矛盾

文本到多视图（Text-to-Multiview, T2MV）生成旨在从单一文本描述同时合成多个一致视角的图像，是3D内容创建的关键前置技术。扩散模型在此任务上展现出强大的生成能力，但其多步迭代去噪过程导致推理成本高昂。少步扩散模型（如基于LCM-SDXL的MV-Adapter）通过将采样步数压缩至4-8步，大幅提升了推理效率，然而步数的急剧减少也带来了生成质量下降——多视图一致性受损、单视图保真度不足等问题在少步设置下尤为突出。

### 现有方法缺口：强化学习微调在多视图场景下的三重局限

为弥补少步模型的质量损失，近期工作将强化学习（RL）引入扩散模型微调，通过奖励信号直接优化生成策略。然而，现有RL微调方法存在三个关键瓶颈：

**第一，MDP建模忽略多视图协调性。** 现有方法将每个视图视为独立单图像生成任务，其MDP状态仅包含单个视图的潜变量和相机条件，奖励函数也仅评估单视图质量。这种建模方式完全忽略了多视图之间必须保持的跨视角一致性——例如，物体在不同视角下的几何结构、纹理和光照应当协调统一。当各视图独立优化时，极易出现“多脸”（Janus）等跨视图冲突问题。

**第二，少步条件下学习信号微弱。** 在少步推理（如8步）下，策略的探索空间被压缩，不同采样轨迹获得的奖励值分布高度集中，导致绝对奖励或两条标准轨迹间的奖励差异难以提供有效的梯度信号。无论是策略梯度（MV-PG）还是直接偏好优化（MV-DPO），都依赖足够强的奖励对比度来驱动策略更新，而少步设置恰恰削弱了这一前提。

**第三，单视图保真度与跨视图一致性的目标冲突。** 若仅优化联合视图奖励（如HyperScore），模型倾向于牺牲单视图质量以换取视图间一致性；反之，若仅优化单视图奖励之和，则跨视图协调性被忽略。简单的固定权重加权和无法动态平衡这对矛盾，因为两者的相对重要性随训练进程和提示难度而变化。

### 本文动机：通过约束强化学习实现协调优化

针对上述局限，本文提出**MVC-ZigAL**框架，核心动机在于：

1. **联合建模多视图决策过程**：将所有视图的状态、动作和奖励统一纳入一个多视图MDP，使策略更新时能够感知跨视图的全局质量，从建模层面消除视图间的不协调。

2. **构造自反思优势信号**：利用ZMV-Sampling（自反思zigzag采样）生成高质量参考轨迹，以其与标准采样轨迹的奖励差值作为优势函数。这种自改进轨迹提供的相对信号在少步条件下比绝对奖励具有更强的梯度区分度。

3. **约束优化范式协调双目标**：将单视图保真度作为优化主目标，跨视图一致性作为约束条件，通过拉格朗日对偶求解实现自适应平衡。配合自定节奏阈值课程和自适应步长原-对偶更新，使约束强度随策略改善动态收紧，避免早期过度约束或后期约束松弛。

## 核心创新

MVC-ZigAL 的核心创新在于针对少步文本到多视图（T2MV）扩散模型，设计了一套完整的强化学习微调框架，从三个层面系统性地解决了现有方法的局限：**多视图联合建模**、**自反思优势学习**和**多视图约束优化**。

### 1. 多视图联合 MDP 建模

现有 RL 微调方法（如 DDPO、DPOK）专为单图像扩散设计，将每个视图独立建模为单图像 MDP，忽略了多视图间的协调性。MVC-ZigAL 提出**多视图感知的 MDP 公式化**，将所有视图联合建模为统一的状态、动作和策略空间：

- **状态** $s_t$ 包含所有 $V$ 个视图的噪声隐变量及对应相机嵌入；
- **动作** $a_t$ 为所有视图的下一步去噪结果；
- **策略** $\pi(a_t \mid s_t)$ 定义为所有视图的联合条件分布；
- **奖励** 仅在最终步 $t=0$ 由联合视图奖励函数 $\mathcal{R}_{\mathrm{mv}}$ 评估整体多视图质量。

这一建模使得策略能够感知跨视图的全局一致性，为后续的约束优化奠定基础。

### 2. 自反思 Zigzag 采样与优势学习

少步推理下，标准采样轨迹的奖励分布高度集中，导致绝对奖励或两条标准轨迹间的奖励差异作为学习信号时梯度微弱。MVC-ZigAL 引入 **ZMV-Sampling**——一种基于自反思机制的 zigzag 采样技术：

- 以**高引导尺度** $\omega_{\mathrm{high}}$ 执行去噪步，增强文本和视角条件的约束力；
- 以**低引导尺度** $\omega_{\mathrm{low}}$ 执行近似反转步，重新注入噪声并弱化条件影响；
- 交替执行上述两步（zigzag pass），在首步即注入结构先验，生成高质量的自改进轨迹。

消融实验表明，**首步 zigzag 调度**在 HyperScore 上优于全步 zigzag，且计算成本更低。基于此，MVC-ZigAL 定义**自反思优势函数**：

$$\mathcal{A}_{\mathrm{mv}} \triangleq \mathcal{R}_{\mathrm{mv}}(\{\mathbf{x}_0^{z,v}\}, \mathbf{c}) - \mathcal{R}_{\mathrm{mv}}(\{\mathbf{x}_0^{s,v}\}, \mathbf{c})$$

即 zigzag 轨迹与标准采样轨迹的联合视图奖励差值。通过最小化策略对数似然比差异与该优势值之间的平方误差（MV-ZigAL 损失），模型学习自改进轨迹的相对优势而非绝对奖励，在少步条件下获得更强的梯度信号。

### 3. 多视图约束优化与自适应原-对偶更新

仅优化联合视图奖励会牺牲单视图保真度，而仅优化单视图奖励则可能导致多脸、视图不一致等问题。MVC-ZigAL 提出**多视图约束策略优化**框架，将单视图奖励作为主目标、联合视图奖励作为约束：

$$\max_{\theta} \mathbb{E}\left[\sum_{v=1}^{V} R(\mathbf{x}_0^v, \mathbf{c})\right] \quad \text{s.t.} \quad \mathbb{E}[\mathcal{R}_{\mathrm{mv}}] \geq \tau$$

通过拉格朗日对偶将约束合并为统一目标，定义**多视图约束奖励**：

$$\mathcal{R}_{\mathrm{mvc}}(\mathbf{x}_0^v, \mathbf{c}) = \frac{R(\mathbf{x}_0^v, \mathbf{c}) + \lambda \mathcal{R}_{\mathrm{mv}}(\{\mathbf{x}_0^v\}, \mathbf{c})}{1 + \lambda}$$

其中拉格朗日乘子 $\lambda$ 通过**自适应步长原-对偶更新**动态调整：

$$\lambda_{k+1} = \max(\lambda_k + \alpha^{\pm}(\tau - \bar{\mathcal{R}}_{\mathrm{mv}}), 0)$$

约束满足时采用较小步长 $\alpha^{-}$，违反时采用较大步长 $\alpha^{+}$，实现响应迅速且稳定的约束执行。同时引入**自定节奏阈值课程**：

$$\tau_{k+1} \leftarrow \beta_{\tau} \tau_k + (1 - \beta_{\tau}) \bar{\mathcal{R}}_{\mathrm{mv}}$$

通过指数移动平均动态调整约束阈值，早期鼓励探索，后期随策略改善逐步收紧约束。消融实验证实，自适应阈值和自适应步长分别带来更稳定且更高的奖励曲线，并减少拉格朗日乘子震荡。

### 4. 与基线的关键差异总结

| 设计维度 | 现有方法（MV-PG/MV-DPO/MV-RDL） | MVC-ZigAL |
|---------|-------------------------------|-----------|
| **MDP 建模** | 每视图独立建模 | 所有视图联合建模 |
| **学习信号** | 绝对奖励或两条标准轨迹奖励差 | 自反思 zigzag 轨迹与标准轨迹的结构化优势 |
| **优化目标** | 单目标（仅单视图或仅联合视图） | 约束优化：最大化单视图奖励，约束联合视图奖励 |
| **约束执行** | 无约束或固定权重加权和 | 自适应步长原-对偶更新 + 自定节奏阈值课程 |

这些创新协同作用，使 MVC-ZigAL 在训练提示集上 HyperScore Overall 达到 9.17（基线 7.23），在 MATE-3D 分布外基准上以极低 NFE（4/8）显著超越 SPAD、MV-Adapter 等 SOTA 方法，ImageReward 从 -0.846 跃升至 0.865。

## 整体框架

MVC-ZigAL 是一个面向少步文本到多视图（T2MV）扩散模型的强化学习微调框架。其核心设计围绕三个相互协作的模块展开：**多视图联合 MDP 建模**、**自反思 zigzag 采样（ZMV-Sampling）** 以及**多视图约束策略优化**。整体流程如下：

1. **基础模型**：以 **MV-Adapter (LCM-SDXL)** 作为少步 T2MV 骨干，该模型能够在极少的函数评估次数（NFE，如 8 步）下，根据文本提示 $\mathbf{c}$ 和相机嵌入 $\{\mathbf{e}_v\}_{v=1}^V$ 生成 $V$ 个视图的图像 $\{\mathbf{x}_0^v\}_{v=1}^V$。

2. **多视图 MDP 建模**：将 T2MV 的去噪过程重新形式化为一个多视图感知的马尔可夫决策过程（MDP），其中状态 $s_t$ 联合编码所有 $V$ 个视图的噪声潜变量与相机嵌入，动作 $a_t$ 为所有视图的下一步去噪结果，策略 $\pi(a_t|s_t)$ 即为扩散模型的多视图联合去噪分布。奖励函数 $\mathcal{R}_{\mathrm{mv}}$ 在最终步 $t=0$ 时评估所有视图的整体质量（基于 HyperScore 等多维评估器），而非仅评估单个视图。

3. **自反思采样（ZMV-Sampling）**：在微调过程中，对每个提示并行执行两条轨迹——
   - **标准采样轨迹**：以常规引导尺度进行少步去噪，生成标准多视图图像 $\{\mathbf{x}_0^{s,v}\}$。
   - **zigzag 参考轨迹**：采用 first-step zigzag 调度，仅在首步执行高引导去噪（$\omega_{\mathrm{high}}$）→ 低引导反转（$\omega_{\mathrm{low}}$）→ 高引导去噪的 zigzag pass，后续步正常采样，生成自反思增强的多视图图像 $\{\mathbf{x}_0^{z,v}\}$。该设计在极低计算开销下为参考轨迹注入更强的结构先验。

4. **优势信号构造**：计算 zigzag 轨迹与标准轨迹之间的联合视图奖励差值，形成自反思优势 $\mathcal{A}_{\mathrm{mv}} = \mathcal{R}_{\mathrm{mv}}(\{\mathbf{x}_0^{z,v}\}) - \mathcal{R}_{\mathrm{mv}}(\{\mathbf{x}_0^{s,v}\})$。相比直接使用绝对奖励或两条普通轨迹的奖励差，这种结构化优势在少步条件下提供更强的梯度信号。

5. **多视图约束优化**：将单视图保真度与跨视图一致性协调建模为约束优化问题——
   - **主目标**：最大化所有视图的单视图奖励之和 $\sum_{v=1}^V R(\mathbf{x}_0^v, \mathbf{c})$。
   - **约束**：期望联合视图奖励不低于自适应阈值 $\tau$，即 $\mathbb{E}[\mathcal{R}_{\mathrm{mv}}] \geq \tau$。
   - 通过拉格朗日对偶将约束转化为多视图约束奖励 $\mathcal{R}_{\mathrm{mvc}}$，以拉格朗日乘子 $\lambda$ 动态平衡单视图与联合视图目标。

6. **策略更新**：将多视图约束优势 $\mathcal{A}_{\mathrm{mvc}}$（zigzag 与标准轨迹在 $\mathcal{R}_{\mathrm{mvc}}$ 下的差值）作为学习目标，最小化策略对数似然比差异与 $\mathcal{A}_{\mathrm{mvc}}$ 之间的平方误差（MVC-ZigAL 损失，Eq. 16），实现优势内化。

7. **自适应约束执行**：采用原-对偶更新机制——
   - **自适应步长**：根据约束满足或违反情况使用不同学习率 $\alpha^{\pm}$ 更新 $\lambda$，响应迅速且避免震荡。
   - **自定节奏阈值课程**：通过指数移动平均 $\tau_{k+1} = \beta_\tau \tau_k + (1-\beta_\tau)\bar{\mathcal{R}}_{\mathrm{mv}}$ 动态调整约束阈值，早期鼓励探索，后期随策略改善逐步收紧约束。

**输入**：文本提示 $\mathbf{c}$、相机嵌入 $\{\mathbf{e}_v\}_{v=1}^V$、随机噪声。  
**输出**：经 RL 微调后的策略 $p_\theta$，在少步采样下生成高保真且跨视图一致的多视图图像。

## 核心模块与公式推导

### 多视图感知的MDP建模

现有RL微调方法将多视图生成中的每个视图视为独立单图像MDP，忽略了视图间的协调性。MVC-ZigAL将全部视图联合建模为一个多视图感知的MDP，使策略能够感知跨视图的全局质量信号。

**状态**定义为当前时间步所有视图的噪声潜变量、相机嵌入及文本条件的集合：

$$s _ { t } \triangleq \left( \{ \mathbf { x } _ { t } ^ { v } , \mathbf { e } _ { v } \} _ { v = 1 } ^ { V } , \mathbf { c } \right)$$

**动作**为所有视图的去噪结果：

$$a _ { t } \triangleq \{ \mathbf { x } _ { t - 1 } ^ { v } \} _ { v = 1 } ^ { V }$$

**策略**在所有视图上联合定义：

$$\pi ( a _ { t } \mid s _ { t } ) \triangleq p _ { \theta } \left( \{ \mathbf { x } _ { t - 1 } ^ { v } \} _ { v = 1 } ^ { V } \mid \{ \mathbf { x } _ { t } ^ { v } , \mathbf { e } _ { v } \} _ { v = 1 } ^ { V } , \mathbf { c } \right)$$

**奖励**仅在最终时间步由联合视图奖励函数 $\mathcal{R}_{\mathrm{mv}}$ 给出：

$$r ( s _ { t } , a _ { t } ) \triangleq \left\{ \begin{array} { l l } { \mathcal { R } _ { \mathrm { m v } } \left( \{ \mathbf { x } _ { 0 } ^ { v } \} _ { v = 1 } ^ { V } , \mathbf { c } \right) } & { \mathrm { i f ~ } t = 0 } \\ { 0 } & { \mathrm { o t h e r w i s e } } \end{array} \right.$$

该MDP的目标是最大化期望联合视图奖励：

$$\operatorname* { m a x } _ { \theta } \mathbb { E } _ { \mathbf { c } \sim p ( \mathbf { c } ) } \mathbb { E } _ { \{ \mathbf { x } _ { 0 } ^ { v } \} _ { v = 1 } ^ { V } \sim p _ { \theta } ( \cdot \vert \{ \mathbf { e } _ { v } \} _ { v = 1 } ^ { V } , \mathbf { c } ) } [ \mathcal { R } _ { \mathrm { m v } } ( \{ \mathbf { x } _ { 0 } ^ { v } \} _ { v = 1 } ^ { V } , \mathbf { c } ) ]$$

---

### 自反思Zigzag采样（ZMV-Sampling）

少步推理下标准采样与奖励模型评估的轨迹之间奖励分布集中，导致学习信号微弱。ZMV-Sampling通过自反思机制构造高质量参考轨迹，为优势学习提供结构化信号。

ZMV-Sampling在首步去噪中执行zigzag交替：高引导尺度去噪步强化文本与视角条件，低引导尺度近似反转步重新注入噪声并弱化条件影响。其核心操作如下：

**高引导去噪步**（$\omega_{\mathrm{high}}$ 为高引导尺度）：

$$\{ \mathbf { x } _ { t - 1 } ^ { v } \} _ { v = 1 } ^ { V } \sim p _ { \theta } \left( \cdot \mid \{ \mathbf { x } _ { t } ^ { v } , \mathbf { e } _ { v } \} _ { v = 1 } ^ { V } , \mathbf { c } ; \omega _ { \mathrm { h i g h } } \right)$$

**低引导反转步**（$\omega_{\mathrm{low}}$ 为低引导尺度）：

$$\{ \tilde { \mathbf { x } } _ { t } ^ { v } \} _ { v = 1 } ^ { V } \sim q _ { \theta } \left( \cdot \mid \{ \mathbf { x } _ { t - 1 } ^ { v } , \mathbf { e } _ { v } \} _ { v = 1 } ^ { V } , \mathbf { c } ; \omega _ { \mathrm { l o w } } \right)$$

在首步去噪中交替执行上述两步后，后续步骤以标准方式完成，得到自反思轨迹 $\{ \mathbf { x } _ { 0 } ^ { z , v } \}$。该轨迹通常比标准采样轨迹 $\{ \mathbf { x } _ { 0 } ^ { s , v } \}$ 获得更高的联合视图奖励，其差值构成zigzag优势：

$$\mathcal { A } _ { \mathrm { m v } } \triangleq \mathcal { R } _ { \mathrm { m v } } \left( \{ \mathbf { x } _ { 0 } ^ { z , v } \} _ { v = 1 } ^ { V } , \mathbf { c } \right) - \mathcal { R } _ { \mathrm { m v } } \left( \{ \mathbf { x } _ { 0 } ^ { s , v } \} _ { v = 1 } ^ { V } , \mathbf { c } \right)$$

消融实验证实，仅首步zigzag即可在HyperScore上超越全步zigzag，且计算成本更低（Table 2, First-Step vs Full-Step Zigzag）。

---

### 多视图约束优化

纯粹最大化联合视图奖励会牺牲单视图保真度（如多脸、纹理退化），而仅优化单视图奖励则破坏跨视图一致性。MVC-ZigAL将两者统一为约束优化问题：

$$\begin{array} { r l } { \operatorname* { m a x } _ { \theta } } & { \mathbb { E } [ \sum _ { v = 1 } ^ { V } R ( \mathbf { x } _ { 0 } ^ { v } , \mathbf { c } ) ] } \\ { \mathrm { s . t . } } & { \mathbb { E } [ \mathcal { R } _ { \mathrm { m v } } ] \geq \tau } \end{array}$$

即最大化单视图奖励之和，同时约束期望联合视图奖励不低于阈值 $\tau$。通过拉格朗日对偶转化为无约束min-max问题：

$$\operatorname* { m i n } _ { \lambda \geq 0 } \operatorname* { m a x } _ { \theta } \mathbb { E } \left[ \sum _ { v = 1 } ^ { V } R ( \mathbf { x } _ { 0 } ^ { v } , \mathbf { c } ) + \lambda \left( \mathcal { R } _ { \mathrm { m v } } - \tau \right) \right]$$

由此定义**多视图约束奖励**，将单视图奖励与拉格朗日乘子加权的联合视图奖励归一化组合：

$$\mathcal { R } _ { \mathrm { m v c } } ( \mathbf { x } _ { 0 } ^ { v } , \mathbf { c } ) = \frac { R ( \mathbf { x } _ { 0 } ^ { v } , \mathbf { c } ) + \lambda \mathcal { R } _ { \mathrm { m v } } \left( \{ \mathbf { x } _ { 0 } ^ { v } \} _ { v = 1 } ^ { V } , \mathbf { c } \right) } { 1 + \lambda }$$

对应的**多视图约束优势**为自反思轨迹与标准轨迹的约束奖励差值：

$$\mathcal { A } _ { \mathrm { m v c } } ( \mathbf { x } _ { 0 } ^ { z , v } , \mathbf { x } _ { 0 } ^ { s , v } , \mathbf { c } ) = \mathcal { R } _ { \mathrm { m v c } } ( \mathbf { x } _ { 0 } ^ { z , v } , \mathbf { c } ) - \mathcal { R } _ { \mathrm { m v c } } ( \mathbf { x } _ { 0 } ^ { s , v } , \mathbf { c } )$$

---

### MVC-ZigAL最终损失

将多视图约束优势代入优势学习框架，MVC-ZigAL最小化轨迹对的对数似然比差异与约束优势之间的平方误差：

$$\mathbb { E } \Bigg [ \sum _ { t = 1 } ^ { T } \sum _ { v = 1 } ^ { V } \left( \frac { 1 } { \eta } \left( \log \frac { p _ { \theta } ( \mathbf { x } _ { t - 1 } ^ { z , v } \mid \mathbf { x } _ { t } ^ { z , v } , \mathbf { e } _ { v } , \mathbf { c } ) } { p _ { \theta ^ { \prime } } ( \mathbf { x } _ { t - 1 } ^ { z , v } \mid \mathbf { x } _ { t } ^ { z , v } , \mathbf { e } _ { v } , \mathbf { c } ) } - \log \frac { p _ { \theta } ( \mathbf { x } _ { t - 1 } ^ { s , v } \mid \mathbf { x } _ { t } ^ { s , v } , \mathbf { e } _ { v } , \mathbf { c } ) } { p _ { \theta ^ { \prime } } ( \mathbf { x } _ { t - 1 } ^ { s , v } \mid \mathbf { x } _ { t } ^ { s , v } , \mathbf { e } _ { v } , \mathbf { c } ) } \right) - \mathcal { A } _ { \mathrm { m v c } } \right) ^ { 2 } \Bigg ]$$

其中 $\eta$ 为温度系数，$\theta^\prime$ 为冻结的参考策略参数。该损失使策略内化自反思轨迹相对于标准轨迹的结构化优势，在少步条件下获得更强的梯度信号。

---

### 自适应原-对偶更新与自定节奏阈值课程

拉格朗日乘子 $\lambda$ 的更新直接影响单视图保真度与跨视图一致性的平衡。MVC-ZigAL采用**自适应步长原-对偶更新**：

$$\lambda _ { k + 1 } = \operatorname* { m a x } ( \lambda _ { k } + \alpha ^ { \pm } ( \tau - \bar { \mathcal { R } } _ { \mathrm { m v } } ) , 0 )$$

其中 $\bar{\mathcal{R}}_{\mathrm{mv}}$ 为当前批次的平均联合视图奖励。当约束满足（$\bar{\mathcal{R}}_{\mathrm{mv}} \geq \tau$）时使用较小步长 $\alpha^-$，违反时使用较大步长 $\alpha^+$，实现响应迅速且稳定的约束执行。

约束阈值 $\tau$ 通过**自定节奏阈值课程**动态调整，跟随策略改善逐步收紧：

$$\tau _ { k + 1 } \gets \beta _ { \tau } \tau _ { k } + ( 1 - \beta _ { \tau } ) \bar { \mathcal { R } } _ { \mathrm { m v } }$$

其中 $\beta_\tau$ 为指数移动平均的衰减系数。早期训练阶段阈值较低，鼓励策略探索；随着策略改善，阈值自动上升，逐步收紧跨视图一致性约束。消融实验证实，自适应阈值和自适应步长分别带来更稳定且更高的奖励曲线，并减少拉格朗日乘子震荡（Figure 5, Figure 6）。

### 补充图表

![[assets/figures/papers/paper_list_l2699_https_arxiv_org_abs_2505_20107/figures/002_Figure_2.jpg]]
*Figure 2: Comparison of full-step and first-step zigzag schedules for ZMV-Sampling using the non-finetuned MV-Adapter*

![[assets/figures/papers/paper_list_l2699_https_arxiv_org_abs_2505_20107/figures/003_Figure_3.jpg]]
*Figure 3: Qualitative comparison of reward optimization with joint-view or single-view rewards only versus our multiview-constrained approach. Joint-view optimization emphasizes view consistency but under-optimizes image fidelity; single-view optimization targets image fidelity but compromises view consistency, causing the “multi-face” problem. In contrast, our approach balances both aspects effectively*

## 实验与分析

### 1. 核心定量结果

MVC-ZigAL在训练提示集和分布外基准上均展现出对多视图RL基线的显著优势。Table 1报告了在45个动物提示、8步采样、6视图配置下的主结果：MVC-ZigAL取得**HyperScore Overall 9.17**，较基础模型MV-Adapter (LCM-SDXL)的7.23提升**+1.94**（相对提升26.8%），同时PickScore从0.196提升至0.205。相比之下，MV-PG（9.14）、MV-DPO（9.07）、MV-RDL（9.04）均未能超越MVC-ZigAL，验证了多视图约束优化与自反思优势学习的协同增益。

在MATE-3D分布外基准上（Table 4），MVC-ZigAL以极低NFE（4/8步）取得**HyperScore Overall 7.04**，超过MV-Adapter的6.67及SPAD、MVDream等SOTA方法。更值得关注的是，大规模微调后ImageReward从**-0.846跃升至0.865**（提升+1.711），表明RL微调有效修复了LCM-SDXL骨干在图像保真度上的严重退化。

![[assets/figures/papers/paper_list_l2699_https_arxiv_org_abs_2505_20107/figures/010_Table_4.jpg]]
*Table 4: Out-of-distribution evaluation on the MATE-3D benchmark. The number of function evaluations (NFE) indicates the total number of diffusion model passes required per inference. Our MVC-ZigAL consistently outperforms the SOTA T2MV diffusion baselines (SPAD [17] and MV-Adapter [15]) and all SOTA methods listed in the MATE-3D benchmark across all metrics at low NFEs. Results of SOTA methods are directly taken from the MATE-3D benchmark*

### 2. 消融分析

**自反思优势学习策略**：Table 2显示MVC-ZigAL在所有HyperScore子指标上超越MV-ZigPG（策略梯度变体），证实学习zigzag轨迹的相对优势优于直接优化绝对奖励。Figure 4（Left）进一步揭示，随着微调进行，标准采样与ZMV-Sampling之间的奖励差距持续收敛，说明模型逐步内化了自反思轨迹的质量优势。

**zigzag调度设计**：Table 2对比了first-step zigzag与full-step zigzag。前者在HyperScore上表现更优且计算成本更低——仅需在首步执行高-低引导交替，而非全链去噪。Figure 2的定性结果显示，first-step zigzag已能有效注入结构先验，全步调度带来的额外增益有限。

**多视图约束优化的必要性**：Figure 3和Table 2联合揭示了关键权衡。仅优化联合视图奖励（Joint-View Only）虽提升跨视图一致性，但单视图保真度受损；仅优化单视图奖励（Single-View Only）则导致多脸等一致性问题。MVC-ZigAL通过约束优化框架，在Figure 4（Middle & Right）的权衡曲线上同时取得更高的单视图和联合视图奖励，验证了拉格朗日对偶求解的有效性。

**自适应机制**：Figure 5表明，固定阈值下奖励曲线波动较大，而自适应阈值课程使训练更稳定且最终奖励更高。Figure 6显示自适应步长有效抑制了拉格朗日乘子的震荡，使约束执行响应更迅速。Table 2的消融进一步确认，移除自适应阈值（w/o Adaptive τ）或自适应步长（w/o Adaptive α）均导致性能下降。

### 3. 关键图表解读

- **Figure 1**：定性展示MV-Adapter (SDXL)、MV-Adapter (LCM-SDXL)与MVC-ZigAL的多视图生成对比。MVC-ZigAL在保持跨视图几何一致性的同时，显著改善了LCM-SDXL骨干的纹理细节和图像保真度。
- **Figure 4（Left）**：奖励差距收敛曲线直接验证了自反思优势学习机制——模型通过模仿ZMV-Sampling的高质量轨迹，逐步缩小与参考轨迹的性能差距。
- **Figure 7**：MVC-ZigAL对SDXL骨干进行RL微调时，奖励曲线持续上升，表明方法对不同骨干具有泛化性。

![[assets/figures/papers/paper_list_l2699_https_arxiv_org_abs_2505_20107/figures/005_Figure_4.jpg]]
*Figure 4: (Left) Reward gap in HyperScore between standard sampling and ZMV-Sampling over MVC-ZigAL finetuning. (Middle & Right) Trade-off between per-view rewards (PickScore/HPSv2) and joint-view rewards (HyperScore) under different RL paradigms*

![[assets/figures/papers/paper_list_l2699_https_arxiv_org_abs_2505_20107/figures/011_Figure_7.jpg]]
*Figure 7: Reward curves of our MVC-ZigAL during RL finetuning of MV-Adapter (SDXL)*

### 4. 失败模式与局限性

论文未明确报告失败案例，但可从实验设计中推断以下潜在边界：

1. **极端少步设置**：当前实验最低NFE为4步（Table 4），在2步甚至1步下的表现未经验证。ZMV-Sampling的自反思机制依赖首步zigzag调度，当总步数过少时，单步去噪可能无法充分承载结构先验。
2. **奖励模型依赖性**：HyperScore和PickScore均面向3D/多视图质量评估设计，若替换为其他奖励模型（如CLIP-based评分），多视图约束优化的效果需要重新验证。
3. **训练提示分布**：主实验仅使用45个动物名称作为训练提示，大规模微调扩展至MATE-3D提示集后ImageReward大幅提升，暗示训练提示的多样性与覆盖度对最终性能有显著影响。

### 5. 公平性说明

所有对比实验统一使用8步采样和6视图配置，训练提示集固定为45个动物名称，OOD评估采用MATE-3D基准。定性比较固定随机种子42。Table 3汇总了标准微调、大规模微调和SDXL骨干微调三组超参数，确保了实验设置的可复现性。

### 补充图表

![[assets/figures/papers/paper_list_l2699_https_arxiv_org_abs_2505_20107/figures/004_Table_1.jpg]]
*Table 1: Quantitative comparison of T2MV policy optimization methods using HyperScore and PickScore. All reward scores are evaluated with 8 sampling steps and 6 views per trajectory*

![[assets/figures/papers/paper_list_l2699_https_arxiv_org_abs_2505_20107/figures/006_Table_2.jpg]]
*Table 2: Quantitative comparison of MVC-ZigAL variants and ablations. All reward scores are evaluated on unseen prompts from the MATE-3D benchmark using 8 sampling steps and 6 views per trajectory, with models checkpointed at the 70th training epoch*

![[assets/figures/papers/paper_list_l2699_https_arxiv_org_abs_2505_20107/figures/007_Figure_5.jpg]]
*Figure 5: Comparison of reward curves (left & middle) and Lagrange multiplier dynamics (right) during training of MVC-ZigAL variants with either adaptive or fixed constraint thresholds*

![[assets/figures/papers/paper_list_l2699_https_arxiv_org_abs_2505_20107/figures/008_Figure_6.jpg]]
*Figure 6: Comparison of reward curves (left & middle) and Lagrange multiplier dynamics (right) during training of MVC-ZigAL variants using either adaptive or fixed step sizes for Lagrange multiplier updates*

![[assets/figures/papers/paper_list_l2699_https_arxiv_org_abs_2505_20107/figures/015_Figure_12.jpg]]
*Figure 12: Additional qualitative comparison on unseen prompts between MV-Adapter and our MVC-ZigAL finetuned model*

![[assets/figures/papers/paper_list_l2699_https_arxiv_org_abs_2505_20107/figures/016_Figure_13.jpg]]
*Figure 13: Additional qualitative comparison on unseen prompts between MV-Adapter and our MVC-ZigAL finetuned model*

![[assets/figures/papers/paper_list_l2699_https_arxiv_org_abs_2505_20107/figures/017_Figure_14.jpg]]
*Figure 14: Additional qualitative comparison on unseen prompts between MV-Adapter and our MVC-ZigAL finetuned model*

## 方法谱系与知识库定位

### 基础模型与基线关系

MVC-ZigAL 构建在 **MV-Adapter**（集成 LCM-SDXL 的少步文本到多视图扩散模型）之上，将其作为 RL 微调的初始策略。论文系统性地将三类现有 RL 微调范式扩展到多视图场景作为基线：

- **MV-PG**：将单图像策略梯度估计器直接推广到多视图，对所有视图的对数似然梯度求和，以联合视图奖励作为权重。该方法继承了 REINFORCE 类算法方差高、梯度效率低的问题，在少步条件下尤为严重。
- **MV-DPO**：将直接偏好优化推广到多视图，聚合所有视图的对数似然比差异。其核心局限在于依赖两条标准采样轨迹的奖励对比，当奖励分布集中时（少步推理的典型特征），正负样本对之间的区分度微弱，导致学习信号不足。
- **MV-RDL**：将奖励差异学习推广到多视图，最小化对数似然比差异与联合奖励差异之间的平方误差。MVC-ZigAL 的损失函数形式直接继承自 MV-RDL，但将其中的绝对奖励差异替换为自反思优势信号，从根本上改变了优化目标的质量。

### 核心创新与因果机制

MVC-ZigAL 的因果链条由三个相互耦合的设计决策构成：

1. **自反思优势学习（ZMV-Sampling → MV-ZigAL 损失）**：现有方法（MV-PG、MV-DPO、MV-RDL）均依赖标准采样轨迹之间的奖励对比，当少步推理导致奖励分布高度集中时，这些对比信号近乎噪声。MVC-ZigAL 的关键洞察在于：利用 ZMV-Sampling 在推理时通过高-低引导交替的 zigzag pass 产生自改进轨迹，这些轨迹天然具有更高的结构质量和跨视图一致性。学习自反思轨迹相对于标准轨迹的**结构化优势**，而非两条标准轨迹之间的微弱差异，能够在少步条件下提供显著更强的梯度信号。Figure 4（Left）显示，随着微调进行，标准采样与 ZMV-Sampling 之间的 HyperScore 奖励差距持续缩小，验证了策略确实内化了自反思能力。

2. **多视图约束优化（单视图主目标 + 联合视图约束）**：直接最大化联合视图奖励（如 MV-PG）会过度强调跨视图一致性，牺牲单视图保真度；仅优化单视图奖励则忽略视图间协调，导致多脸等结构性问题（见 Figure 3）。MVC-ZigAL 将问题形式化为约束优化——最大化单视图奖励之和，同时约束期望联合视图奖励不低于自适应阈值。通过拉格朗日对偶将约束合并为统一的多视图约束奖励函数 $\mathcal{R}_{\mathrm{mvc}}$，实现了两者在梯度层面的自动平衡。

3. **自适应原-对偶更新与自定节奏阈值课程**：约束优化的实际效果高度依赖拉格朗日乘子 $\lambda$ 的更新策略和阈值 $\tau$ 的设置。MVC-ZigAL 引入两个自适应机制：
   - **自适应步长**：当约束满足时使用较小步长 $\alpha^-$ 缓慢放松乘子，约束违反时使用较大步长 $\alpha^+$ 快速收紧，避免乘子震荡（Figure 6 证实该设计带来更稳定的奖励曲线）。
   - **自定节奏阈值课程**：通过指数移动平均 $\tau_{k+1} \gets \beta_\tau \tau_k + (1-\beta_\tau)\bar{\mathcal{R}}_{\mathrm{mv}}$ 动态调整阈值，使其跟随策略改善逐步收紧，早期鼓励探索，后期强制执行一致性约束（Figure 5 显示固定阈值会导致乘子持续增长或奖励停滞）。

### 适用边界与局限

MVC-ZigAL 的设计假设和潜在局限包括：

- **奖励模型依赖性**：框架依赖 HyperScore 作为联合视图奖励函数，该模型专为文本到 3D 生成设计，其对多视图一致性评估的泛化能力尚未在其他奖励模型（如 CLIP-based 评分）上验证。若奖励模型对特定结构缺陷不敏感，约束优化的效果将打折扣。
- **ZMV-Sampling 的少步极限**：实验验证了 8 步和 4 步设置下的有效性，但 zigzag pass 本身需要额外的去噪-反转循环。在极端少步设置（如 2 步）下，自反思轨迹是否仍能提供有效优势信号尚待验证。
- **训练提示集规模**：标准 RL 微调仅使用 45 个动物名称作为训练提示，虽然 OOD 评估（MATE-3D 基准）显示泛化能力显著，但提示多样性对最终策略质量的上限影响未充分消融。
- **对后续 3D 重建的增益未量化**：论文聚焦于 T2MV 生成质量本身，RL 微调后的多视图一致性提升对下游任务（如 Gaussian Splatting 重建）的实际增益尚未通过实验验证。

### 开放问题

1. MVC-ZigAL 能否无缝适配除 HyperScore 和 PickScore 之外的其他奖励模型？不同奖励模型对约束优化中 $\lambda$ 动态的影响是否鲁棒？
2. ZMV-Sampling 的自反思机制在 2 步甚至 1 步的极端少步设置下是否仍能提供有效优势信号？zigzag pass 的额外计算开销与性能增益的权衡曲线如何？
3. RL 微调后的 T2MV 模型对后续 3D 重建任务（如通过 3D Gaussian Splatting 或 NeRF）的实际增益有多大？多视图一致性的提升是否线性转化为重建质量的提升？
4. 自定节奏阈值课程和自适应步长原-对偶更新是否对其他约束 RL 问题（如安全 RL、多目标 RL）具有通用性？这些机制的理论收敛性质尚待分析。

## 原文 PDF

![[paperPDFs/CVPR_2026/Refining_Few_Step_Text_to_Multiview_Diffusion_via_Reinforcement_Learning.pdf]]