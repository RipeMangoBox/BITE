---
title: "Diffusion Negative Preference Optimization Made Simple"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Diffusion_Negative_Preference_Optimization_Made_Simple.pdf
openreview_forum_id: CU5EHe1KUt
aliases:
- DSDSNPO
- DNPOMS
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: "将偏好信号分配到单个扩散网络的已有双分支（条件分支学习正偏好，无条件分支学习负偏好），同时引入 Bounded DPO 以阻止失败样本对数似然主导损失，防止胜者似然坍塌。"
primary_logic: "利用 CFG 固有的条件/无条件双分支，以单网络实现正负偏好联合学习，并用混合分布下界约束负样本贡献，消除模糊伪影并保持稳定优化。"
claims:
- "Naive Diff-SNPO 产生逐步模糊的输出，而 Diff-SNPO 保持清晰且胜者概率持续提升。"
- "Diff-SNPO 在 Pick-a-Pic v2 和 HPDv2 上大多超越 Diff-NPO 与 CHATS，且训练速度 2×、推理吞吐提升。"
- "Diff-SNPO 的负偏好隐式准确率（57.45%）和损失（0.668）均优于合并后的 Diff-NPO（52.34%/0.703）。"
- "Pick-a-Pic v2 (SD1.5) 上 HPSv2 ↑ = 27.23 ± 0.07"
---

# Diffusion Negative Preference Optimization Made Simple

> [!tip] 核心洞察
> 利用 CFG 固有的条件/无条件双分支，以单网络实现正负偏好联合学习，并用混合分布下界约束负样本贡献，消除模糊伪影并保持稳定优化。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 扩散负偏好优化简化方法 |
| 英文题名 | Diffusion Negative Preference Optimization Made Simple |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=CU5EHe1KUt); [GitHub](https://github.com/JoshuaTTJ/DiffSNPO) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Diff-SNPO (Diffusion Simple Negative Preference Optimization) |
| Dataset | Pick-a-Pic v2 (SD1.5), Pick-a-Pic v2 (SDXL), HPDv2 (SD1.5) |

> [!tip] 效果简介
> - Pick-a-Pic v2 (SD1.5) 上，HPSv2 ↑ 为 27.23 ± 0.07，对比 Diff-NPO 27.08 ± 0.10，变化 +0.15。
> - Pick-a-Pic v2 (SD1.5) 上，Image Reward ↑ 为 0.6936 ± 0.17，对比 Diff-NPO 0.3786 ± 0.20，变化 +0.315。
> - Pick-a-Pic v2 (SDXL) 上，Pick Score ↑ 为 22.86 ± 0.03，对比 Diff-NPO 22.62 ± 0.09，变化 +0.24。

## 概述

扩散模型的对齐方法正从“仅优化正偏好”向“同时利用负偏好”演进。现有负偏好优化方法（Diff-NPO、CHATS）依赖双模型架构——分别训练正模型 θ⁺ 与负模型 θ⁻，导致训练和推理的计算/内存开销加倍。推理时虽可通过权重合并缓解资源压力，但合并过程会稀释负向对齐信号，造成保真度与负向对齐之间的根本性权衡（Figure 1）。

本文提出 **Diff-SNPO**（Diffusion Simple Negative Preference Optimization），核心思路是将偏好信号分配到单个扩散网络已有的双分支结构中：**条件分支**学习正偏好（胜者样本），**无条件分支**学习负偏好（败者样本）。这一设计利用 CFG 固有的条件/无条件双分支，以单网络实现正负偏好联合学习，彻底消除双模型开销与权重合并需求。

为防止败者样本的对数似然主导损失函数，Diff-SNPO 引入 **Bounded DPO** 机制，用混合分布 π_mix = λπ_θ + (1-λ)π_ref 约束负样本贡献，从而避免胜者似然坍塌和逐步模糊伪影（Figure 2, Figure 3）。

在 Pick-a-Pic v2 和 HPDv2 基准上，Diff-SNPO 在 SD1.5 和 SDXL backbone 上大多超越 Diff-NPO 与 CHATS，且训练速度提升 2×、推理吞吐达 0.48 img/s（对比 Diff-NPO 的 0.27 img/s）。负偏好隐式准确率（57.45%）和损失（0.668）均优于合并后的 Diff-NPO（52.34%/0.703），验证了单网络双分支设计对负向对齐的有效性。

## 背景与动机

### 扩散模型偏好对齐的进展与瓶颈

文本到图像扩散模型在图像保真度上取得了显著进步，但生成结果与人类偏好之间的对齐仍存在差距。为弥合这一差距，研究者将直接偏好优化（DPO）引入扩散模型，形成了 Diff-DPO 等方法。Diff-DPO 通过成对的胜者-败者比较数据训练模型，使其生成更符合人类偏好的图像。然而，Diff-DPO 仅利用正偏好信号——即只告诉模型“什么是好的”，却未显式建模“什么是坏的”。

这一局限催生了负偏好优化方法。Diff-NPO 和 CHATS 是两个代表性工作，它们同时利用正偏好（胜者样本）和负偏好（败者样本）进行训练。其核心设计是**双模型架构**：维护两个独立的扩散网络 θ⁺ 和 θ⁻，分别学习正偏好和负偏好。Table 1 总结了各方法的架构差异：Diff-DPO 为单模型且无负偏好建模，而 Diff-NPO 与 CHATS 均为双模型并依赖权重合并策略。

### 双模型架构的代价：计算开销与对齐权衡

双模型设计带来了两个严重问题。

**第一，训练与推理成本加倍。** 维护两个完整扩散网络意味着显存占用、计算量和训练时间均翻倍。如 Table 4 所示，Diff-NPO 在 8×A6000 GPU 上训练时显存占用达 88.4 GB，单步耗时 13.75 秒；而单模型方法仅需 44.2 GB 和 12.25 秒。对于 SDXL 等大 backbone，这一开销严重限制了方法的可扩展性。

**第二，推理时的权重合并造成负向对齐信号稀释。** 由于双模型在推理时需同时使用，Diff-NPO 和 CHATS 采用权重合并策略，将 θ⁺ 和 θ⁻ 的参数按比例融合为单一推理模型。然而，如 Figure 1 所示，合并操作会偏向正模型，削弱负模型的影响。这导致一个根本性权衡：合并系数越偏向正模型，生成质量（HPSv2）越高，但负向隐式准确率越低——模型对“什么是坏的”的判断能力下降。换言之，**保真度与负向对齐之间存在不可调和的冲突**。

### 核心动机：单网络双分支联合学习

上述分析揭示了现有方法的瓶颈：**双模型架构是计算开销与对齐权衡的共同根源**。一个自然的问题是：能否在单个扩散网络中同时实现正偏好与负偏好的学习？

本文的动机正源于此。扩散模型本身通过无分类器引导（CFG）在推理时同时使用条件分支和无条件分支，这一双分支结构天然提供了两个可分配的信号通路。关键洞察是：**将正偏好信号分配给条件分支，将负偏好信号分配给无条件分支，从而在单网络内实现正负偏好的联合学习**。这不仅消除了双模型的计算冗余，还避免了权重合并带来的负向信号稀释问题。

然而，直接将偏好信号分配到两个分支的朴素方法会导致训练不稳定——胜者似然在训练过程中持续下降，生成图像出现逐步模糊的伪影（Figure 3）。因此，需要设计一种**有界的偏好优化目标**，防止败者样本主导损失函数。这正是 Diff-SNPO 方法的核心贡献所在。

## 核心创新

### 瓶颈定位：双模型负偏好优化的结构性代价

现有负偏好优化方法（Diff-NPO、CHATS）依赖两个独立扩散模型分别处理正偏好（θ⁺）与负偏好（θ⁻），带来三重结构性代价：

1. **计算与内存加倍**：训练需同时维护两个完整扩散网络，内存占用和每步训练时间翻倍（Table 4 显示 Diff-NPO 内存 88.4 GB vs Diff-SNPO 44.2 GB）。
2. **推理强制合并**：推理时须通过权重合并（Eq.12-13）将 θ⁺ 与 θ⁻ 融合为单一参数，但合并系数偏向正模型，稀释负向对齐信号。Figure 1 揭示这一权衡——合并后 HPSv2 提升，但负偏好隐式准确率同步下降。
3. **保真度-对齐权衡**：合并策略本质是在生成质量与负向约束之间折中，无法同时满足两者。

### 核心洞察：CFG 双分支的天然解耦

Diff-SNPO 的关键创新在于**将偏好信号分配到 CFG 固有的条件/无条件双分支**，以单网络实现正负偏好联合学习：

- **条件分支**（接受文本条件 c）：学习正偏好，对应胜者样本 xʷ。
- **无条件分支**（接受空条件 ∅）：学习负偏好，处理标签翻转后的败者样本 xˡ。

这一设计将双模型架构的冗余计算压缩到单个网络内部，消除了独立 θ⁻ 的需求，推理时直接使用标准 CFG 公式（Eq.14），无需任何权重合并。Table 1 清晰对比了各方法的架构差异：Diff-SNPO 是唯一同时具备负对齐能力、单模型、无需合并的方案。

### 关键保障：Bounded DPO 防止胜者似然坍塌

直接将偏好信号分配到 CFG 双分支（Naive Diff-SNPO）会导致训练不稳定：败者样本的对数似然主导损失函数，引发胜者似然持续下降。Figure 2 显示 Naive-SNPO 的胜者概率比随训练下降，Figure 3 则展示其输出逐步出现模糊伪影。

Diff-SNPO 引入 **Diff-BDPO-UB**（Bounded DPO 的扩散适配）解决此问题。核心机制是将败者样本的参考分布替换为混合分布：

$$\pi_{\mathrm{mix}}(y|x) = \lambda \pi_\theta(y|x) + (1-\lambda) \pi_{\mathrm{ref}}(y|x), \quad \lambda \in (0,1)$$

该混合分布作为败者似然的下界约束，防止其无限降低并主导损失。最终损失函数（Eq.22）中，胜者使用标准 margin，败者使用混合 margin：

$$m_{\mathrm{mix}}(x_t,c) = -\log\Bigl( \lambda e^{-d_\theta(x_t,\epsilon,t,c)} + (1-\lambda) e^{-d_{\mathrm{ref}}(x_t,\epsilon,t,c)} \Bigr) - d_{\mathrm{ref}}(x_t,\epsilon,t,c)$$

其中 $d_\theta$ 与 $d_{\mathrm{ref}}$ 分别为当前模型与参考模型的加权去噪误差（Eq.37-38）。当 λ < 1 时，败者似然被限制在参考模型附近，避免损失被败者项支配。Figure 4 的消融证实 λ=1.0（即 Naive-SNPO）导致 HPSv2 和 Aesthetic Score 显著下降，而 λ=0.9 保持稳定优化。

### Changed Slots 总结

| 维度 | 基线（Diff-NPO/CHATS） | Diff-SNPO |
|------|----------------------|-----------|
| 模型架构 | 两个独立模型 θ⁺ 与 θ⁻ | 单个 CFG 网络，条件分支处理正偏好，无条件分支处理负偏好 |
| 损失函数 | 标准 Diff-DPO 损失（胜者/败者均与参考模型比较） | Diff-BDPO-UB：败者项替换为混合分布下界，防止败者主导 |
| 推理策略 | CFG 使用 θ⁺ 和合并后的 θ⁻，需权重合并 | 标准 CFG，仅使用单网络的条件/无条件分支，无需合并 |

这三个 changed slots 共同实现了训练速度 2× 提升（Table 4）、推理吞吐 0.48 img/s（Diff-NPO 0.27 img/s，Table 10），以及更优的负偏好隐式准确率 57.45%（Diff-NPO 合并后 52.34%，Table 5）。

## 整体框架

![[assets/figures/papers/iclr26_0011_CU5EHe1KUt_Diffusion_Negative_Preference_Optimization_Made/figures/001_Table_1.jpg]]
*Table 1: Comparison of methods by alignment type, model setup, and use of merging strategy*

![[assets/figures/papers/iclr26_0011_CU5EHe1KUt_Diffusion_Negative_Preference_Optimization_Made/figures/003_Figure_1.jpg]]
*Figure 1: Negative implicit accuracy (left) and HPSv2 (right) on SD1.5. Weight merging lowers implicit accuracy while increasing reward, revealing a trade-off*

Diff-SNPO 的核心设计是将负偏好优化从现有方法的双模型架构压缩为**单个扩散网络**，利用分类器自由引导（CFG）固有的双分支结构，将正负偏好信号分配到同一网络的不同分支中，从而消除冗余计算并规避权重合并带来的负向信号稀释。整体 pipeline 由三个关键模块构成：条件分支、无条件分支和 Diff-BDPO-UB 损失。

**输入**：给定一个偏好对 $(\mathbf{x}^w, \mathbf{x}^l, c)$，其中 $\mathbf{x}^w$ 为胜者样本，$\mathbf{x}^l$ 为败者样本，$c$ 为文本条件。训练时随机采样一个二元指示变量 $Y \in \{+1, -1\}$，用于决定当前 batch 中正负偏好的路由方向。

**条件分支（正偏好学习）**：当 $Y = +1$ 时，胜者样本 $\mathbf{x}^w$ 与文本条件 $c$ 配对，送入扩散网络的条件分支 $\epsilon_\theta(\cdot, c)$。该分支学习提升胜者样本的似然，与标准 Diff-DPO 中正偏好对的作用一致。

**无条件分支（负偏好学习）**：当 $Y = -1$ 时，败者样本 $\mathbf{x}^l$ 与空条件 $\varnothing$ 配对，送入无条件分支 $\epsilon_\theta(\cdot, \varnothing)$。此处通过标签翻转机制——将败者样本的偏好标签反转为“胜者”——使无条件分支学习远离败者分布，从而实现负偏好对齐。这一设计将原本需要独立负模型 $\theta^-$ 完成的任务迁移到 CFG 的 null-condition 通路，无需额外模型参数。

**Diff-BDPO-UB 损失**：直接在上述双分支上应用标准 Diff-DPO 损失（称为 Naive Diff-SNPO）会导致败者项主导优化，产生胜者似然坍塌和渐进模糊伪影（Figure 3）。为解决这一问题，Diff-SNPO 引入 Bounded DPO 的扩散版本。具体而言，败者样本的对数似然不再直接与参考模型比较，而是与一个**混合分布** $\pi_{\text{mix}} = \lambda \pi_\theta + (1-\lambda) \pi_{\text{ref}}$ 比较（$\lambda \in (0,1)$，默认 0.9）。该混合分布构成败者似然的下界，防止败者概率被过度压低。通过 Jensen 不等式和 Hölder 不等式推导，混合对数似然可转化为逐时间步的可计算形式：

$$m_{\text{mix}}(x_t, c) = -\log\left(\lambda e^{-d_\theta(x_t, \epsilon, t, c)} + (1-\lambda) e^{-d_{\text{ref}}(x_t, \epsilon, t, c)}\right) - d_{\text{ref}}(x_t, \epsilon, t, c)$$

其中 $d_\theta$ 和 $d_{\text{ref}}$ 分别为当前模型和参考模型的加权去噪误差。最终损失函数为：

$$\mathcal{L}_{\text{SNPO}}(\theta) = -\mathbb{E}_{(\mathbf{x}^w, \mathbf{x}^l, c) \sim \mathcal{D}, t \sim p(t), Y} \left[ \log \sigma \left( \beta \left( m(\tilde{x}^w(Y), \tilde{c}(Y)) - m_{\text{mix}}(\tilde{x}^l(Y), \tilde{c}(Y)) \right) \right) \right]$$

其中 $m(\cdot)$ 为标准 per-step margin（$m = d_\theta - d_{\text{ref}}$），$\tilde{x}^{w/l}(Y)$ 和 $\tilde{c}(Y)$ 根据 $Y$ 的符号在条件/无条件分支间切换。

**推理**：推理时使用标准 CFG，仅需单次前向传播——条件分支 $\epsilon_\theta(\cdot, c)$ 提供条件预测，无条件分支 $\epsilon_\theta(\cdot, \varnothing)$ 提供无条件预测，二者按 CFG 强度加权组合。无需像 Diff-NPO 或 CHATS 那样进行模型合并或条件嵌入扰动，彻底消除了推理阶段的额外开销。

**模块关系总结**：条件分支与无条件分支共享同一网络参数，通过 $Y$ 的随机采样实现正负偏好的交替训练。Diff-BDPO-UB 损失在败者分支引入混合下界约束，将负样本对损失的贡献限制在可控范围内，从而使单网络双分支设计能够稳定收敛。Table 1 对比了各方法的架构差异：Diff-SNPO 是唯一同时具备负偏好对齐能力、单模型设计且无需权重合并的方法。

## 核心模块与公式推导

Diff-SNPO 的核心设计在于将正负偏好信号分配到单个扩散网络的已有双分支结构中，并用有界偏好目标防止训练坍塌。以下按模块拆解其关键公式与变量含义。

### 单网络双分支偏好分配

传统 CFG 推理时，条件分支（接受文本条件 $c$）与无条件分支（接受空条件 $\varnothing$）共同工作。Diff-SNPO 将这一结构复用于偏好学习：条件分支学习正偏好（胜者样本），无条件分支学习负偏好（败者样本，标签翻转）。

具体而言，对于每个偏好对 $(\mathbf{x}^w, \mathbf{x}^l, c)$，引入 Bernoulli 变量 $Y \sim \text{Uniform}(\{+1, -1\})$ 决定当前批次的分支分配：

- 当 $Y = +1$：条件分支处理胜者 $\mathbf{x}^w$，无条件分支处理败者 $\mathbf{x}^l$
- 当 $Y = -1$：条件分支处理败者 $\mathbf{x}^l$，无条件分支处理胜者 $\mathbf{x}^w$

这一分配策略使单网络能够同时接收正偏好与负偏好信号，无需维护两个独立模型。

### Naive Diff-SNPO 损失及其失效

若直接沿用标准 Diff-DPO 损失到上述单网络框架，得到 Naive Diff-SNPO 损失：

$$\mathcal{L}_{\text{Naive Diff-SNPO}}(\theta) = -\mathbb{E}_{(x_0^w, x_0^l)\sim\mathcal{D}, t, Y} \left[ \log \sigma \left( Y T \omega(t) \beta \left( \Delta_t^w(\tilde{c}(Y)) - \Delta_t^l(\tilde{c}(Y)) \right) \right) \right]$$

其中 $\Delta_t(\cdot)$ 表示去噪误差项，$\tilde{c}(Y)$ 根据 $Y$ 的符号选择条件或空条件。

**关键失效模式**：如 Figure 3 和 Figure 2 所示，Naive Diff-SNPO 在训练过程中胜者概率比持续下降，生成图像逐步出现模糊伪影。其根源在于败者样本的对数似然 $\log \pi_\theta(\mathbf{x}^l|c)$ 在优化中不断降低，最终主导损失函数，导致胜者似然坍塌。

### Bounded DPO 与混合分布下界

为解决败者项主导问题，Diff-SNPO 引入 Bounded DPO（BDPO）的核心思想：将败者样本的对数似然替换为混合分布的对数似然，限制其对损失的贡献。

混合分布定义为当前策略 $\pi_\theta$ 与参考策略 $\pi_{\text{ref}}$ 的凸组合：

$$\pi_{\text{mix}}(y|x) = \lambda \pi_\theta(y|x) + (1-\lambda) \pi_{\text{ref}}(y|x), \quad \lambda \in (0,1)$$

BDPO 损失函数为：

$$\mathcal{L}_{\text{BDPO}}(\pi_\theta; \pi_{\text{ref}}) = -\mathbb{E}_{(x_0^w, x_0^l, c)\sim\mathcal{D}} \left[ \log \sigma \left( \beta \left[ \log \frac{\pi_\theta(x_0^w|c)}{\pi_{\text{ref}}(x_0^w|c)} - \log \frac{\pi_{\text{mix}}(x_0^l|c)}{\pi_{\text{ref}}(x_0^l|c)} \right] \right) \right]$$

这里胜者项保持标准形式，败者项使用 $\pi_{\text{mix}}$ 替代 $\pi_\theta$。由于 $\pi_{\text{mix}}$ 始终包含 $\pi_{\text{ref}}$ 分量，即使 $\pi_\theta$ 对败者赋予极低概率，混合分布的对数似然也不会发散，从而防止败者项主导损失。

### 扩散模型上的 BDPO 上界（Diff-BDPO-UB）

将 BDPO 适配到扩散模型需要处理轨迹级似然 $\log p_\theta(\mathbf{x}_{0:T}|c)$。通过 Hölder 不等式（取均匀指数 $p_t = T$）可导出逐时间步的可处理上界。

定义每步去噪误差：

$$d_\theta(x_t, \epsilon, t, c) = T \omega(t) \|\epsilon - \epsilon_\theta(x_t, t, c)\|_2^2$$

$$d_{\text{ref}}(x_t, \epsilon, t, c) = T \omega(t) \|\epsilon - \epsilon_{\text{ref}}(x_t, t, c)\|_2^2$$

定义每步 margin（模型与参考模型的去噪误差之差）：

$$m(x_t, c) = d_\theta(x_t, \epsilon, t, c) - d_{\text{ref}}(x_t, \epsilon, t, c)$$

混合 margin 为基于混合分布的对数似然下界：

$$m_{\text{mix}}(x_t, c) = -\log \left( \lambda e^{-d_\theta(x_t, \epsilon, t, c)} + (1-\lambda) e^{-d_{\text{ref}}(x_t, \epsilon, t, c)} \right) - d_{\text{ref}}(x_t, \epsilon, t, c)$$

经 Jensen 不等式收紧后，得到最终可计算的 Diff-BDPO-UB 损失：

$$\mathcal{L}_{\text{Diff-BDPO-UB}}(\theta) = -\mathbb{E}_{(x_0^w, x_0^l, c)\sim\mathcal{D}, t\sim\mathcal{U}[1,T]} \left[ \log \sigma \left( -\beta \left( m(x_t^w, c) - m_{\text{mix}}(x_t^l, c) \right) \right) \right]$$

### Diff-SNPO 最终损失

将单网络双分支分配策略与 Diff-BDPO-UB 结合，得到 Diff-SNPO 完整损失：

$$\mathcal{L}_{\text{SNPO}}(\theta) = -\mathbb{E}_{(\mathbf{x}^w,\mathbf{x}^l,c)\sim\mathcal{D}, t\sim p(t), Y} \left[ \log \sigma \left( \beta \left( m(\tilde{x}^w(Y), \tilde{c}(Y)) - m_{\text{mix}}(\tilde{x}^l(Y), \tilde{c}(Y)) \right) \right) \right]$$

其中 $\tilde{x}^w(Y)$ 与 $\tilde{x}^l(Y)$ 根据 $Y$ 的符号在胜者/败者间切换，$\tilde{c}(Y)$ 相应选择条件或空条件。胜者使用标准 margin $m(\cdot)$，败者使用混合 margin $m_{\text{mix}}(\cdot)$。

**消融验证**：Figure 4 表明，当 $\lambda=1.0$（即混合分布退化为 $\pi_\theta$，等价于 Naive-SNPO）时，HPSv2 和 Aesthetic Score 均显著下降；$\lambda<1$（论文默认 $\lambda=0.9$）是防止性能坍塌的关键。$\beta$ 在 $1000$–$3000$ 范围内对指标影响有限（Table 3），表明方法对超参数选择鲁棒。

### 推理策略

Diff-SNPO 推理时使用标准 CFG，无需权重合并：

$$\tilde{\epsilon}_\theta(x_t, t, c) = \epsilon_\theta(x_t, t, \varnothing) + s \cdot \left( \epsilon_\theta(x_t, t, c) - \epsilon_\theta(x_t, t, \varnothing) \right)$$

其中条件分支 $\epsilon_\theta(\cdot, c)$ 已学习正偏好，无条件分支 $\epsilon_\theta(\cdot, \varnothing)$ 已学习负偏好。这避免了 Diff-NPO 中权重合并带来的负向对齐信号稀释问题（Figure 1 揭示了合并后负向隐式准确率下降与 HPSv2 提升之间的权衡）。

## 实验与分析

### 核心瓶颈与动机验证

现有负偏好优化方法（Diff-NPO、CHATS）依赖双模型架构，训练与推理的计算/内存开销加倍。推理时虽可通过权重合并缓解正负模型不相关的问题，但合并会稀释负向对齐信号，导致保真度与负向对齐之间的固有权衡。Figure 1 清晰展示了这一现象：随着合并权重向正模型倾斜，负向隐式准确率持续下降，而 HPSv2 奖励分数上升，二者无法兼得。

Diff-SNPO 从架构层面消除了这一瓶颈：利用 CFG 固有的条件/无条件双分支，将正偏好信号分配给条件分支，负偏好信号分配给无条件分支，实现单网络正负偏好联合学习。Table 1 系统对比了各方法的对齐类型、模型架构与合并策略，Diff-SNPO 是唯一同时具备负偏好对齐能力且无需双模型、无需合并的方案。

### 主实验结果

**Pick-a-Pic v2 基准。** Table 2 报告了 SD1.5 和 SDXL 两个 backbone 上的全面对比。在 SD1.5 上，Diff-SNPO 在 HPSv2 上达到 27.23 ± 0.07，略优于 Diff-NPO 的 27.08 ± 0.10；在 Image Reward 上优势更为显著（0.6936 vs 0.3786，提升 0.315），表明单网络设计不仅未损害正偏好对齐，反而在部分指标上实现了更优的人类偏好匹配。在 SDXL 上，Diff-SNPO 的 Pick Score 达到 22.86 ± 0.03，超越 Diff-NPO 的 22.62 ± 0.09，但在 HPSv2 上二者接近（28.33 vs 28.37），优势有所收窄——这可能源于 SDXL backbone 自身能力较强，以及数据集中偏好样本的偏差与更强模型的交互作用。

![[assets/figures/papers/iclr26_0011_CU5EHe1KUt_Diffusion_Negative_Preference_Optimization_Made/figures/006_Table_2.jpg]]
*Table 2: Comparison of Diff-SNPO with baseline methods on SD1.5 and SDXL backbones using Pick-a-Pic v2. All values are reported as mean ± 95% confidence interval over 4 random seeds. Diff-SNPO consistently achieves the highest scores across most human preference metrics, reflecting improved alignment and visual quality. For clarity, the best-performing method in each metric is shown in bold, and the second-best is underlined*

**HPDv2 基准。** Table 6 展示了在 HPDv2 上的跨 backbone 评估。SD1.5 上 Diff-SNPO 的 Image Reward 达到 0.8093，远超 Diff-NPO 的 0.4761（提升 0.3332），HPSv2 亦以 22.86 领先。SDXL 上 Diff-SNPO 与 Diff-NPO 表现接近（HPSv2 28.01 vs 28.00，Image Reward 0.8781 vs 0.8684），进一步印证了在更强 backbone 上优势缩小的趋势。

### 消融实验：Bounded DPO 的关键作用

**混合系数 λ 的消融。** Figure 4 揭示了 λ 对性能的决定性影响。当 λ=1.0（即 Naive-SNPO，败者项完全由当前策略建模）时，HPSv2 和 Aesthetic Score 均出现显著下降。λ<1 时引入参考策略的混合分布约束，有效防止败者似然主导损失，避免了性能坍塌。论文默认使用 λ=0.9。

**训练动态对比。** Figure 2 和 Figure 3 从定量与定性两个维度展示了 Bounded DPO 的稳定化效果。Figure 2 显示 Naive-SNPO 的胜者概率比在训练过程中持续下降，而 Diff-SNPO 稳步提升。Figure 3 的定性样本更直观：Naive-SNPO 随训练迭代逐步产生模糊伪影，输出对比度持续降低；Diff-SNPO 则保持图像清晰度，且生成质量随训练逐步改善。这一现象的根本原因在于：无约束时败者样本的对数似然项主导损失函数，迫使模型同时降低胜者似然，导致“胜者似然坍塌”，在扩散模型中表现为去噪过程的信息丢失和模糊化。

![[assets/figures/papers/iclr26_0011_CU5EHe1KUt_Diffusion_Negative_Preference_Optimization_Made/figures/005_Figure_2.jpg]]
*Figure 2: Win probability ratio over training. Naive-SNPO’s win probability decreases during training, whereas Diff-SNPO’s improves steadily*

**β 的鲁棒性。** Table 3 显示 β 在 1000–3000 范围内对指标影响有限（HPSv2 27.23–27.30，Aesthetic 5.59–5.67），表明方法对温度参数不敏感，无需精细调参。

**ODE solver 的无关性。** Table 7 表明不同采样器（DDIM、Euler、UniPC、DPM）几乎不影响性能，Diff-SNPO 的推理质量对采样策略鲁棒。

### 负向对齐的定量验证

Table 5 从负偏好隐式分类准确率和损失两个维度直接评估负向对齐质量。Diff-SNPO 的负向隐式准确率达到 57.45%，显著优于合并后的 Diff-NPO（52.34%）；负偏好损失 0.668 也低于 Diff-NPO 的 0.703。这证实了单网络双分支设计在负向信号保留上优于双模型加权重合并的方案：合并操作不可避免地稀释了负模型学到的拒绝信号，而 Diff-SNPO 通过将负偏好直接编码进无条件分支，在推理时无需任何妥协即可完整保留负向对齐能力。

![[assets/figures/papers/iclr26_0011_CU5EHe1KUt_Diffusion_Negative_Preference_Optimization_Made/figures/011_Table_5.jpg]]
*Table 5: Negative preference implicit classification accuracy and loss. Parentheses denote Diff-NPO without weight merging. Diff-SNPO achieves higher negative implicit accuracy and lower negative preference loss than Diff-NPO, improving its negative alignment*

### 计算效率

Table 4 和 Table 10 分别量化了训练与推理的效率优势。训练方面，Diff-SNPO 单步耗时 12.25s，相对 Diff-NPO 实现 2× 加速，显存占用仅 44.2 GB（Diff-NPO 为 88.4 GB）。推理方面，Diff-SNPO 吞吐达到 0.48 img/s，显著高于 Diff-NPO 的 0.27 img/s。效率提升的根源在于：双模型方法在训练时需维护两套参数并分别计算前向/反向传播，推理时需执行权重合并或双模型推理；Diff-SNPO 的单网络设计彻底消除了这些冗余。

![[assets/figures/papers/iclr26_0011_CU5EHe1KUt_Diffusion_Negative_Preference_Optimization_Made/figures/010_Table_4.jpg]]
*Table 4: Training cost comparison. Experiments were conducted on 8×A6000 GPUs with a total batch size of 512. Dual-model approaches require substantially more memory and incur slower training throughput. The best result in each column is shown in bold*

### 安全性补充说明

在专用安全数据集 CoProv2 上微调后（Table 8），Diff-SNPO 的 IP 降至 0.11，优于 Diff-DPO 和 Diff-NPO，表明单网络双分支设计不会损害安全性微调的兼容性，甚至可能因架构简洁而更易于适配安全约束。

### 局限与待验证点

1. **SDXL 上优势缩小**：在更强 backbone 上 Diff-SNPO 相对 Diff-NPO 的增益减小，可能与数据集中偏好样本的偏差分布及 backbone 自身生成能力有关，需在更大规模、更多样化的偏好数据上进一步验证。
2. **λ 固定为 0.9**：未探索动态调整 λ 的可能性，样本难度自适应的混合系数可能进一步提升性能。
3. **任务范围受限**：当前仅在固定 T2I 基准上评估，未测试图像编辑或视频生成等任务上的泛化性。
4. **负属性建模能力上限**：将负偏好信号全部分配给无条件分支，可能限制对复杂、细粒度负属性的建模能力，这一假设需要更多消融验证。

## 方法谱系与知识库定位

### 与基线方法的关系

Diff-SNPO 直接回应了现有负偏好优化方法的两个结构性瓶颈：**双模型架构的计算冗余**与**权重合并带来的信号稀释**。

**Diff-DPO（单模型正偏好基线）** 仅利用胜者样本进行偏好对齐，完全忽略负偏好信号。Diff-SNPO 在其基础上将偏好信号分配到 CFG 的两个已有分支，在不增加模型参数的前提下引入负偏好学习，从而在多个人类偏好指标上实现一致提升（Table 2：SD1.5 上 HPSv2 从 Diff-DPO 的 26.97 提升至 27.23）。

**Diff-NPO（双模型负偏好基线）** 通过维护两个独立网络 θ⁺ 和 θ⁻ 分别学习正负偏好，但训练时内存占用加倍（Table 4：Diff-NPO 88.4 GB vs Diff-SNPO 44.2 GB），推理时必须通过权重合并将 θ⁻ 融入 θ⁺（Eq.12-13）。这一合并策略存在根本性权衡：Figure 1 显示，合并系数增大虽提升 HPSv2 奖励，却导致负向隐式准确率持续下降——正模型主导合并结果，负向对齐信号被稀释。Diff-SNPO 通过单网络双分支设计彻底消除合并需求，Table 5 表明其负向隐式准确率（57.45%）和负偏好损失（0.668）均优于合并后的 Diff-NPO（52.34%/0.703）。

**CHATS（条件嵌入扰动基线）** 同样采用双模型架构，通过扰动条件嵌入实现负偏好建模，但仍面临与 Diff-NPO 相同的计算开销问题。Diff-SNPO 在 Pick-a-Pic v2 和 HPDv2 上大多超越 CHATS（Table 2, Table 6），同时训练速度提升约 2×（Table 4）。

### 核心设计选择与适用边界

Diff-SNPO 的有效性依赖于两个关键设计选择，它们同时定义了方法的适用边界：

1. **CFG 双分支的语义分配**：将负偏好信号分配给无条件分支（空条件 ∅）利用了 CFG 推理时条件/无条件输出的差分机制。这一设计的隐含前提是负偏好属性可以通过“去条件化”来表征——即败者样本的特征与无条件生成分布有足够的重叠。当负属性高度依赖特定条件语义（如复杂组合概念中的错误绑定）时，无条件分支的表达能力可能受限，这是该方法的一个潜在边界。

2. **Bounded DPO 的混合下界**：Diff-BDPO-UB 损失（Eq.22）通过混合分布 $\\pi_{\\mathrm{mix}} = \\lambda \\pi_\\theta + (1-\\lambda) \\pi_{\\mathrm{ref}}$ 约束败者项对损失的贡献（Eq.16-17）。消融实验（Figure 4）表明，λ=1.0（即 Naive-SNPO，混合退化为纯当前策略）导致 HPSv2 和 Aesthetic Score 显著下降，生成样本出现逐步模糊的伪影（Figure 3）；λ<1 是防止性能坍塌的必要条件。当前 λ 固定为 0.9，未根据样本难度自适应调整，这限制了模型对不同质量败者样本的差异化处理能力。

### 局限与开放问题

**Backbone 依赖性**：在更强 backbone（SDXL）上，Diff-SNPO 相对于 Diff-NPO 的优势缩小（Table 2：SDXL 上 HPSv2 的 Δ 从 SD1.5 的 +0.15 降至 +0.04）。这一现象可能与 Pick-a-Pic v2 数据集的偏好偏差有关——当 backbone 自身生成能力较强时，数据集中“胜者”样本的偏好信号减弱，负偏好优化的边际收益相应降低。该点需要手动验证：论文未提供 SDXL 上不同数据集的系统性对比。

**任务泛化未验证**：当前评估仅覆盖固定 T2I 生成基准（Pick-a-Pic v2, HPDv2），未测试图像编辑、视频生成、或可控生成等任务。将负偏好信号分配到无条件分支的策略是否适用于需要精细条件控制的任务（如局部编辑保持背景不变）仍是开放问题。

**λ 与 β 的调参空间**：λ 固定为 0.9，β 在 1000-3000 范围内对指标影响有限（Table 3），但未探索极端值（β→0 或 β→∞）下的行为。λ 的自适应调整（如基于败者样本难度的动态插值）可能进一步提升负向对齐的精细度。

**安全对齐的整合**：论文在 CoProv2 安全数据集上微调后，Diff-SNPO 的 IP 降至 0.11（Table 8），表明单网络设计可以与显式安全过滤结合。但当前方法仅依赖隐式负偏好（从人类偏好数据中学习），是否可以将显式负反馈（如安全分类器输出）直接注入无条件分支，形成统一的隐式-显式负向控制框架，是值得探索的方向。

**理论收敛性**：Diff-BDPO-UB 通过 Hölder 不等式和 Jensen 不等式导出可处理的上界（Eq.34-36），但该上界的紧致性未经验证。宽松的上界可能导致优化目标与真实偏好优化目标之间存在不可忽略的偏差，在大规模多模态扩散模型上的稳定性有待进一步检验。

## 原文 PDF

![[paperPDFs/ICLR_2026/Diffusion_Negative_Preference_Optimization_Made_Simple.pdf]]
