---
title: "GDRO: Group-level Reward Post-training Suitable for Diffusion Models"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/GDRO_Group_level_Reward_Post_training_Suitable_for_Diffusion_Models.pdf
project_link: null
code_link: null
aliases:
- GLDROG
- GDRO
tags:
- CVPR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 利用隐式奖励函数（implicit reward function）在任意扩散时间步可离线计算的特性，将组级奖励对齐转化为基于Plackett–Luce排名模型的交叉熵损失，从而完全绕过对在线采样和随机性的需求。
primary_logic: GDRO通过引入隐式奖励函数将组级显式奖励转化为可离线优化的排名导向交叉熵目标，使扩散模型在纯离线、采样器无关的方式下高效学习奖励排序，同时显著缓解奖励黑客问题，并且理论上当组大小k=2、温度τ→0时退化为DPO。
claims:
- GDRO supports full offline training and is diffusion-sampler-independent.
- GDRO achieves higher corrected OCR score (0.5701) at step 300 than Flow-GRPO (0.5482), DanceGRPO (0.5406), and DPO (0.5341).
- GDRO shows 2× (OCR) and 3.7× (GenEval) efficiency compared to Flow-GRPO in GPU hours.
- GDRO effectively mitigates reward hacking, preserving image quality and details compared to Flow-GRPO.
---

# GDRO: Group-level Reward Post-training Suitable for Diffusion Models

> [!tip] 核心洞察
> GDRO通过引入隐式奖励函数将组级显式奖励转化为可离线优化的排名导向交叉熵目标，使扩散模型在纯离线、采样器无关的方式下高效学习奖励排序，同时显著缓解奖励黑客问题，并且理论上当组大小k=2、温度τ→0时退化为DPO。

| 字段 | 内容 |
|------|------|
| 中文题名 | GDRO：适用于扩散模型的组级奖励后训练 |
| 英文题名 | GDRO: Group-level Reward Post-training Suitable for Diffusion Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2601.02036) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | Group-level Direct Reward Optimization (GDRO) |
| Dataset | OCR Task, GenEval Task |

> [!tip] 效果简介
> - OCR Task 上，OCR Reward / Corrected Score 0.8721 / 0.5701 vs FLUX.1: 0.5843 / 0.4486; Flow-GRPO: 0.8714 / 0.5482 (vs. FLUX.1 corrected +0.1215; vs. Flow-GRPO corrected +0.0219)；GPU Training Hours 29.60 vs Flow-GRPO: 149.07; DanceGRPO: 74.67 (2.0× faster than DanceGRPO; 5.0× faster than Flow-GRPO)。
> - GenEval Task 上，GenEval Reward / Corrected Score 0.8517 / 0.5148 vs FLUX.1: 0.6178 / 0.4646; Flow-GRPO: 0.8520 / 0.4757 (vs. FLUX.1 corrected +0.0502; vs. Flow-GRPO corrected +0.0391)；GPU Training Hours 68.4 vs Flow-GRPO: 340.00; DanceGRPO: 294.53 (3.7× faster than Flow-GRPO)。

## 概要

扩散模型的后训练对齐是实现高质量、高可控文本到图像生成的关键环节。当前主流方法——如基于在线强化学习的Flow‑GRPO和DanceGRPO——在应用于**rectified flow扩散模型**（如FLUX.1）时，面临三个相互交织的瓶颈：**训练效率低下**（每一步优化都需要完整的在线采样链，图像生成耗时主导训练）、**采样器依赖**（rectified flow是确定性模型，必须通过ODE‑to‑SDE近似引入随机性，由此产生分布外问题）、以及严重的**奖励黑客**现象（优化虽提高了奖励分数，却导致生成质量、细节和图文对齐显著退化）。

**GDRO（Group‑level Direct Reward Optimization）** 针对上述瓶颈提出了一种全新的后训练范式。其核心思想是：利用**隐式奖励函数**在任意扩散时间步可离线计算的特性，将组级显式奖励对齐转化为基于Plackett–Luce排名模型的交叉熵损失，从而**完全绕过对在线采样和随机性的需求**。这一设计使GDRO在纯离线、采样器无关的方式下高效学习奖励排序，同时显著缓解奖励黑客问题。理论上，当组大小k=2且温度τ→0时，GDRO自然退化为DPO（Diffusion‑DPO, Wallace et al., CVPR 2024），因此可视为DPO从成对偏好到组级显式奖励的广义扩展。

实验结果表明，GDRO在OCR和GenEval两个任务上均实现了有效的奖励对齐与质量保持。在OCR任务上，GDRO的**修正OCR分数达到0.5701**，优于Flow‑GRPO（0.5482）、DanceGRPO（0.5406）和DPO（0.5341）；在GenEval任务上，**修正分数为0.5148**，较Flow‑GRPO（0.4757）提升8.2%。训练效率方面，GDRO在OCR任务上仅需**29.60 GPU小时**，相比Flow‑GRPO（149.07小时）和DanceGRPO（74.67小时）分别实现5.0×和2.5×的加速；在GenEval任务上为68.4 GPU小时，较Flow‑GRPO（340.00小时）加速约5.0×。定性分析进一步表明，GDRO有效抑制了Flow‑GRPO中常见的“扁平化”、“文字异常放大”等奖励黑客退化，生成的图像保持了良好的视觉质量与属性正确性。

在方法谱系上，GDRO位于**离线奖励后训练**与**扩散模型偏好对齐**的交汇点：它继承了DPO的隐式奖励框架，但通过引入组级排名损失和显式奖励软目标，将适用范围从成对偏好拓展到任意大小的图像组，并实现了对rectified flow模型的采样器无关支持。

扩散模型在后训练阶段引入奖励对齐已成为提升文本到图像生成质量的关键路径。当前主流方案——在线强化学习微调（如 **Flow-GRPO**、**DanceGRPO** 等）——在通用扩散模型上取得了一定成效，但当将其应用于 **rectified flow 扩散模型**（如 **FLUX.1**，Black-Forest-Labs, 2024）时，暴露出三个相互关联的瓶颈。

**瓶颈一：训练效率低下。** 在线 RL 方法的每一步优化都需要完整的扩散采样链来生成 rollout 图像，图像生成耗时主导了训练过程。对于需要多步采样的 rectified flow 模型，这一开销尤为突出。

**瓶颈二：采样器依赖与分布外问题。** Rectified flow 模型本质上是确定性的，缺乏随机采样器。为获得在线 RL 所需的随机探索能力，现有方法不得不采用 ODE-to-SDE 近似来引入随机性，这不可避免地引入分布外（out-of-distribution）问题，损害生成质量。

**瓶颈三：奖励黑客（Reward Hacking）。** 在线 RL 虽然能有效提升评价奖励分数，但生成质量、细节保真度和图文对齐却严重退化。如 Figure 1 所示，Flow-GRPO 为追求高 OCR 评分，倾向于将文字放大、加粗并纠正倾斜，导致图像内容变得不自然，退化为类似平面插画的风格。这种“高分低质”的奖励黑客现象，使得单纯以评价奖励衡量模型性能变得不可靠。

上述瓶颈的根本原因在于：在线 RL 范式将奖励优化与扩散采样过程强耦合。这引出了一个核心问题——**能否在完全离线、采样器无关的条件下，实现扩散模型的组级奖励对齐？**

**GDRO** 的提出正是为了回答这一问题。其核心动机是利用隐式奖励函数（implicit reward function）在任意扩散时间步可离线计算的特性，将组级显式奖励转化为基于 Plackett–Luce 排名模型的交叉熵损失，从而完全绕过对在线采样和随机性的需求。这一思路将奖励对齐从“在线采样-奖励评估-策略更新”的闭环中解放出来，转变为纯粹的离线排名优化问题，为 rectified flow 扩散模型提供了一种高效、稳定且抗奖励黑客的后训练范式。

## 核心方法与创新机理

### 从在线强化学习到离线排名对齐：范式转换

现有扩散模型奖励后训练方法（如Flow-GRPO、DanceGRPO）依赖在线强化学习框架，其核心瓶颈在于每一步优化都需要完整的在线采样链——扩散模型的前向生成过程本身即构成训练的主要时间开销。对于rectified flow这类确定性模型，还需通过ODE-to-SDE近似来人为引入随机性，这不仅引入分布外问题，更在追求高奖励分数的过程中诱发严重的奖励黑客（reward hacking）现象：优化后的模型倾向于生成符合奖励函数偏好但质量退化、图文对齐丧失的图像（如将文字极端放大、图像退化为平面绘画风格）。

GDRO的核心创新在于**完全绕过在线采样和随机性需求**，将组级奖励对齐问题转化为一个纯离线的排名导向交叉熵优化问题。这一转换的关键杠杆是**隐式奖励函数（implicit reward function）**——该函数仅需对预生成图像在任意扩散时间步进行扰动和速度预测即可计算，无需完整的采样链，从而实现了训练与采样器的彻底解耦。

### 关键机制创新：从成对偏好到组级排名

与仅支持成对偏好优化的Diffusion-DPO（Wallace et al., CVPR 2024）相比，GDRO将优化目标从二元偏好扩展到**任意大小图像组的完整排名**。其损失函数基于Plackett-Luce排名模型，对组内每个位置计算剩余集合上的交叉熵损失：

$$\mathcal{L}_{\mathrm{GDRO}}(\theta) = \sum_{i=1}^{k-1} \left( \log \sum_{m=i}^{k} e^{s_\theta(x_m, t)} - \sum_{j=i}^{k} q_i(j, \tau) s_\theta(x_j, t) \right)$$

其中$q_i(j, \tau)$是由显式奖励经温度$\tau$缩放的软目标分布。这种设计使得GDRO在理论上将DPO作为特例包含：当组大小$k=2$且温度$\tau \to 0$时，GDRO退化为DPO。更大的组大小使模型能够学习更丰富的奖励排序结构，从而提升优化稳定性和最终性能。

### 奖励黑客抑制的双重机制

GDRO通过两个协同机制有效抑制奖励黑客：

1. **软目标分布**：温度参数$\tau$控制显式奖励到目标分布的映射强度。中等温度（如$\tau=0.05$）在奖励信号利用和优化稳定性之间取得平衡——过低的$\tau$会使目标分布过于尖锐，导致类似在线RL的崩溃问题；过高的$\tau$则使奖励信号过于平滑，优化不足。

2. **Top-1似然稳定化正则化**：引入正则项$\mathcal{L}_{\mathrm{reg}}(\theta) = M \circ ||v - v_\theta(x_t(c), t, c)||_2^2$，通过one-hot掩码$M$稳定组内最高奖励样本的似然，防止模型在追求排名对齐时牺牲生成质量。消融实验表明，移除该正则化（$\gamma=0$）会导致与过低$\beta$类似的优化崩溃。

### 训练效率的结构性优势

由于GDRO完全离线，其训练时间由预生成图像组的数量和质量决定，而非在线采样步数。在OCR任务上，GDRO仅需29.60 GPU小时即可达到0.5701的修正分数，而Flow-GRPO需要149.07 GPU小时（5倍差距）；在GenEval任务上，GDRO以68.4 GPU小时超越Flow-GRPO的340.00 GPU小时（3.7倍差距）。这一效率优势源于GDRO避免了扩散模型前向采样这一最耗时的环节，将计算资源集中于损失函数的优化本身。

GDRO 的整体设计围绕一个核心原则展开：**将组级显式奖励对齐转化为完全离线的排名导向交叉熵优化，从而彻底绕过在线采样与随机性依赖**。其 pipeline 由五个顺序模块构成，输入为预生成的同提示图像组及其显式奖励，输出为更新后的扩散模型参数。

### 1. 图像组预生成

训练开始前，对于每个文本提示 $c$，使用**参考模型**（如 FLUX.1）离线采样 $k$ 张图像，构成图像组 $\{x_1, x_2, \dots, x_k\}$，并为每张图像分配一个显式奖励分数 $\{r_1, r_2, \dots, r_k\}$（如 OCR 准确率或 GenEval 评分）。这一步骤完全离线完成，无需在训练循环中重复采样，是 GDRO 效率优势的根源。

### 2. 随机时间步扰动

对于图像组中的每张图像 $x_i$，随机采样一个扩散时间步 $t \in [0, T]$，并按照 rectified flow 的前向加噪过程对其施加噪声，得到扰动图像 $x_{t,i}$。这一操作为后续的隐式奖励计算提供了必要的噪声中间态，同时保持了完全离线特性——扰动仅依赖于预生成图像和噪声调度，不涉及任何采样器。

### 3. 速度预测与隐式奖励计算

将扰动图像 $x_{t,i}$ 分别送入**当前模型** $v_\theta$ 和**参考模型** $v_{\mathrm{ref}}$，预测对应的速度场。随后按以下公式计算隐式奖励：

$$s_\theta(x_i, t) = -\beta \, \mathbb{E}_{t, v}\big[ \|v - v_\theta(C)\|_2^2 - \|v - v_{\mathrm{ref}}(C)\|_2^2 \big]$$

其中 $\beta$ 为控制奖励尺度的超参数。该隐式奖励函数的核心性质在于：**它仅依赖扰动图像和两个模型的速度预测差异，可在任意扩散时间步离线计算，无需在线采样或随机采样器**。这正是 GDRO 实现“采样器无关”的理论基础。

### 4. 软目标分布构造

将组内的显式奖励 $\{r_i\}$ 通过温度参数 $\tau$ 进行 softmax 缩放，得到软目标分布 $Q$：

$$q(i, \tau) = \frac{e^{r_i / \tau}}{\sum_{j=1}^k e^{r_j / \tau}}$$

同时，对隐式奖励 $\{s_\theta(x_i, t)\}$ 做 softmax 得到模型的隐式奖励分布 $P_\theta$。温度 $\tau$ 控制显式奖励对排序的软化程度：$\tau \to 0$ 时 $Q$ 退化为 one-hot（仅最高奖励样本获得全部概率质量），$\tau \to \infty$ 时趋于均匀分布。

### 5. GDRO 损失优化

最终损失由两部分组成：

**GDRO 排名损失**（组级交叉熵）：基于 Plackett–Luce 排名模型，逐位置计算剩余集合的交叉熵，使隐式奖励分布 $P_\theta$ 对齐显式奖励分布 $Q$ 所蕴含的完整排序：

$$\mathcal{L}_{\mathrm{GDRO}}(\theta) = \sum_{i=1}^{k-1} \left( \log \sum_{m=i}^{k} e^{s_\theta(x_m, t)} - \sum_{j=i}^{k} q_i(j, \tau) s_\theta(x_j, t) \right)$$

其中 $q_i(j, \tau)$ 是在位置 $i$ 对剩余样本 $j$ 重新归一化后的目标分布。

**Top-1 稳定性正则化**：用 one-hot 掩码 $M$ 仅对组内显式奖励最高的样本施加速度预测 MSE 损失，防止优化过程中图像质量退化：

$$\mathcal{L}_{\mathrm{reg}}(\theta) = M \circ \|v - v_\theta(x_t(c), t, c)\|_2^2$$

**最终目标**为二者的加权组合：

$$\mathcal{L}_{\mathrm{final}}(\theta) = \mathcal{L}_{\mathrm{GDRO}}(\theta) + \gamma \mathcal{L}_{\mathrm{reg}}(\theta)$$

其中 $\gamma$ 控制正则化强度。反向传播仅更新当前模型 $v_\theta$，参考模型 $v_{\mathrm{ref}}$ 保持冻结。

### 关键设计决策与理论连接

GDRO 的 pipeline 体现了三个关键设计决策，直接回应了现有方法的瓶颈：

1. **离线扰动替代在线采样**：通过预生成图像组加随机时间步扰动，GDRO 完全消除了对扩散采样链的依赖，解决了效率瓶颈。实验表明，这一设计使 GDRO 在 OCR 任务上的 GPU 训练耗时仅为 Flow-GRPO 的约 1/5（29.60 vs. 149.07 GPU 小时）。

2. **隐式奖励替代显式奖励梯度**：利用 rectified flow 模型的速度预测误差差值构造隐式奖励，使优化目标仅依赖前向传播，无需可微奖励函数或随机采样器。这从根本上避免了 ODE-to-SDE 近似引入的分布外问题。

3. **组级排名对齐替代逐样本策略梯度**：基于 Plackett–Luce 模型的交叉熵损失利用组内完整排序信息，相比仅优化 top-1 的 DPO（当 $k=2, \tau \to 0$ 时 GDRO 退化为 DPO），组级设计提供了更丰富的学习信号和更强的稳定性。消融实验证实，组大小 $k=6$ 在 OCR 任务上获得最优表现，$k=2$ 则优化不足。

图 2 直观展示了上述模块的完整数据流：从预生成图像组出发，经扰动、速度预测、隐式奖励计算，最终通过 GDRO 损失与正则化项驱动模型更新。

![[assets/figures/papers/paper_list_l2680_https_arxiv_org_abs_2601_02036/figures/002_Figure_2.jpg]]
*Figure 2: Overview of our method. Given a pre-generated image group synthesized from the same prompt and their corresponding explicit rewards, we perturb the images with noise on different time steps, feed them to the diffusion model to predict the velocity, and calculate the implicit rewards accordingly to get the final loss*

### 3.1 隐式奖励函数的理论构造

GDRO 的核心理论起点是 RL 微调目标下的最优策略形式。给定显式奖励函数 $r(x_0, c)$，RL 微调的目标是在最大化期望奖励的同时约束当前策略 $\pi_\theta$ 与参考策略 $\pi_{\mathrm{ref}}$ 之间的 KL 散度：

$$
\operatorname*{max}_{\theta} \mathbb{E}_{c, x_0 \sim \pi_\theta} r(x_0, c) - \beta_{\mathrm{KL}} \mathbb{D}_{\mathrm{KL}}[\pi_\theta(x_0|c) || \pi_{\mathrm{ref}}(x_0|c)]
$$

该优化问题存在闭式最优解（Eq. (2)）：

$$
\pi_\theta^*(x_0|c) = \frac{\pi_{\mathrm{ref}}(x_0|c) e^{r(x_0,c)/\beta_{\mathrm{KL}}}}{Z(c)}
$$

其中 $Z(c)$ 为配分函数。对该闭式解取对数并移项，可导出**隐式奖励函数**（Eq. (3)）：

$$
s_\theta(x) = \beta_{\mathrm{KL}} \log \frac{\pi_\theta^*(x_0 \mid c)}{\pi_{\mathrm{ref}}(x_0 \mid c)} + \beta_{\mathrm{KL}} \log Z(c)
$$

常数项 $\beta_{\mathrm{KL}} \log Z(c)$ 在后续基于 softmax 的组级优化中会被自然消去，因此隐式奖励的核心信息完全由当前模型与参考模型的策略比率决定。

**关键瓶颈突破：** 上述推导表明，隐式奖励函数仅需扰动后的图像即可计算，无需任何在线采样或随机性。对于 rectified flow 扩散模型，GDRO 采用 Diffusion-DPO 的近似方式，通过速度预测误差差值的期望来估计隐式奖励（Eq. (5)）：

$$
s_\theta(x, t) = -\beta \mathbb{E}_{t, v}\left[\|v - v_\theta(C)\|_2^2 - \|v - v_{\mathrm{ref}}(C)\|_2^2\right]
$$

其中 $v_\theta(C)$ 和 $v_{\mathrm{ref}}(C)$ 分别为当前模型和参考模型在条件 $C$ 下的速度预测值。这一近似使 GDRO 成为**采样器无关**的方法——rectified flow 模型无需通过 ODE-to-SDE 近似获取随机性，从根本上规避了在线 RL 方法中分布外采样的风险。

### 3.2 从组级显式奖励到 GDRO 损失

GDRO 的核心创新在于将组级显式奖励转化为可离线优化的排名导向交叉熵目标。给定同一提示下预生成的图像组 $\{x_1, \dots, x_k\}$ 及其显式奖励 $\{r_1, \dots, r_k\}$，方法通过以下模块完成对齐：

**模块 1：图像扰动与隐式奖励计算。** 在不同扩散时间步对图像组加噪，将扰动图像送入当前模型与参考模型预测速度，按 Eq. (5) 计算每张图像的隐式奖励 $s_\theta(x_i, t)$。

**模块 2：软目标分布构造。** 对显式奖励做温度缩放的 softmax 得到目标分布 $Q$：

$$
Q = \mathrm{softmax}(r_i / \tau)
$$

同时对隐式奖励做 softmax 得到模型分布 $P_\theta$：

$$
p_\theta(i) = \mathrm{softmax}(s_\theta(x_i, t))
$$

**模块 3：Top-1 交叉熵损失。** 首先对齐 top-1 位置的显式奖励分布与隐式奖励分布（Eq. (6)）：

$$
\mathcal{L}_{\mathrm{top-1}}(\theta) = \log \sum_{j=1}^{k} \exp(s_\theta(x_j, t)) - \sum_{i=1}^{k} q(i, \tau) s_\theta(x_i, t)
$$

该损失使高奖励样本在模型隐式奖励空间中同样获得高分，从而增大其被采样的概率。

**模块 4：GDRO 全组排名损失。** 为捕获完整的组级排名信息，GDRO 在每个位置 $i$ 上对剩余集 $\{x_i, \dots, x_k\}$ 计算交叉熵并求和（Eq. (7)）：

$$
\mathcal{L}_{\mathrm{GDRO}}(\theta) = \sum_{i=1}^{k-1} \left( \log \sum_{m=i}^{k} e^{s_\theta(x_m, t)} - \sum_{j=i}^{k} q_i(j, \tau) s_\theta(x_j, t) \right)
$$

其中 $q_i(j, \tau)$ 是对剩余项显式奖励做温度缩放 softmax 后的归一化分布。这一逐位置求和结构等价于 Plackett-Luce 排名模型下的交叉熵损失，使模型学习到完整的组级奖励排序关系。

**模块 5：Top-1 稳定性正则化。** 为防止优化过程中图像质量退化，GDRO 引入 top-1 似然稳定化正则项（Eq. (8)）：

$$
\mathcal{L}_{\mathrm{reg}}(\theta) = M \circ \|v - v_\theta(x_t(c), t, c)\|_2^2
$$

其中 $M$ 为 one-hot 掩码，仅对组内显式奖励最高的样本施加速度预测均方误差约束，稳定其似然。

**最终目标函数**（Eq. (9)）：

$$
\mathcal{L}_{\mathrm{final}}(\theta) = \mathcal{L}_{\mathrm{GDRO}}(\theta) + \gamma \mathcal{L}_{\mathrm{reg}}(\theta)
$$

其中 $\gamma$ 控制正则化强度。消融实验表明，当 $\gamma = 0$（无正则化）时优化过程会出现类似低 $\beta$ 设置的崩溃问题；在 OCR 任务上 $\gamma = 0.5$、GenEval 任务上 $\gamma = 1.0$ 可有效防止质量退化。

### 3.3 与 DPO 的理论退化关系

GDRO 的一个重要理论性质是：当组大小 $k = 2$ 且温度 $\tau \to 0$ 时，GDRO 损失退化为 DPO 损失（Eq. (12) 不含显式奖励的排名损失形式）：

$$
\mathcal{L}_{\mathrm{rank}}(\theta) = \sum_{i=1}^{k-1} \left( \log \sum_{m=i}^{k} \exp(s_\theta(x_m, t)) - s_\theta(x_i, t) \right)
$$

此时 GDRO 仅依赖排序信息，与 DPO 的成对偏好优化等价。然而，当 $k > 2$ 时 GDRO 能够利用更丰富的组级排名结构，这是其相对于 DPO（仅支持成对偏好）的核心优势。消融实验证实 $k = 6$ 在 OCR 任务上获得最优原始分和修正分，$k = 4$ 次之，$k = 2$ 则优化不足，验证了组级信息的重要性。

## 实验与关键发现

### 实验设置与评价设计

GDRO的实验基于预训练的rectified flow文本到图像模型**FLUX.1**（Black-Forest-Labs, 2024）展开，在**OCR**和**GenEval**两个任务上进行奖励后训练与评测。训练采用完全离线模式：先为每个提示预生成一组图像并分配显式奖励，再通过GDRO损失进行优化，无需在线采样。

为应对奖励黑客问题，论文提出了**修正分数（corrected score）**：将评测奖励 $r$ 与**UnifiedReward**（衡量图文对齐、连贯性和风格的综合指标）结合，以更客观地反映真实生成质量。OCR任务的修正分数定义为 $r_{\mathrm{corrected}} = r(\hat{u} - 3) + 0.2$，其中 $\hat{u}$ 为UnifiedReward三项得分的均值。

### 主要定量结果

Table 3汇总了各方法在OCR和GenEval任务上的核心指标。

**OCR任务**：GDRO在训练步数300时达到评测奖励0.8721、修正分数**0.5701**，显著优于Flow-GRPO（0.5482）、DanceGRPO（0.5406）和DPO（0.5341）。相比FLUX.1基线的修正分0.4486，GDRO提升了**+0.1215**。在GPU训练时耗上，GDRO仅需**29.60小时**，而Flow-GRPO需要149.07小时（约**5.0×加速**），DanceGRPO需要74.67小时（约**2.5×加速**）。

**GenEval任务**：GDRO在训练步数700时达到评测奖励0.8517、修正分数**0.5148**，优于Flow-GRPO（0.4757）和DPO（0.4723）。GPU时耗方面，GDRO仅需**68.4小时**，相比Flow-GRPO的340.00小时实现**约5.0×加速**，相比DanceGRPO的294.53小时实现**约4.3×加速**。

### 奖励黑客的实证分析

论文从多个维度验证了GDRO对奖励黑客的缓解效果：

**人类偏好研究（Table 1）**：在OCR任务上，GDRO与FLUX.1基线的图文对齐和生成质量得分几乎持平，且均显著优于Flow-GRPO方法。这表明Flow-GRPO虽然获得了高评测奖励，但实际生成质量严重退化。

**UnifiedReward评估（Table 2）**：Flow-GRPO的所有检查点在三个UnifiedReward子指标上均出现严重退化，而GDRO保持了与FLUX.1基线相当的得分。这从自动化指标层面印证了Flow-GRPO的奖励黑客行为。

**定性对比（Figure 4）**：Flow-GRPO的生成图像倾向于将文字放大到不自然的程度，图像内容退化为平面绘画风格，细节和真实感严重丧失。相比之下，GDRO在保持高文字渲染精度的同时，维持了良好的视觉质量和图文对齐。

**训练曲线分析（Figure 5）**：修正分数曲线清晰揭示了Flow-GRPO的奖励黑客分界线——在修正分达到峰值后，评测奖励继续上升但修正分急剧下降。GDRO的修正分曲线则保持稳定上升趋势，未出现类似的退化拐点。

### 消融研究

**组大小 $k$ 的影响**：在OCR任务上，$k=6$ 获得最高原始分和修正分，$k=4$ 次之，$k=2$ 则优化不足。这表明较大的组规模能为排名学习提供更丰富的比较信号。

**$\beta$（隐式奖励缩放系数）的影响**：OCR任务中，$\beta=6$ 导致快速奖励黑客（修正分下降），$\beta=12$ 保持稳定；GenEval任务中，$\beta=6$ 优于 $\beta=12$，而 $\beta=4$ 则导致训练崩溃。这说明 $\beta$ 的选择具有任务敏感性，需在优化强度与稳定性之间权衡。

**温度 $\tau$ 的影响**：$\tau=0.05$ 在OCR任务上获得最优稳定性和最佳修正分；$\tau=0.5$ 优化不足；$\tau=0.025$ 不稳定且曲线崩溃；$\tau=0$（不使用显式奖励）的表现介于 $\tau=0.05$ 和 $0.025$ 之间。中等温度值能有效平衡显式奖励的引导强度与训练稳定性。

**top-1稳定性正则化的影响**：移除正则化（$\gamma=0$）会导致与低 $\beta$ 类似的崩溃问题。在OCR任务上 $\gamma=0.5$、GenEval任务上 $\gamma=1.0$ 能有效防止质量退化，验证了正则化项在维持生成质量中的关键作用。

### 失败模式与局限

尽管GDRO在离线场景下表现优异，但仍存在以下局限：

1. **缺乏在线探索能力**：GDRO是完全离线的后训练方法，无法主动探索新的生成空间。对于需要主动动作探索的奖励任务（如3D理解、复杂交互），性能可能受限。
2. **修正分数的局限性**：修正分数依赖UnifiedReward来反映奖励黑客趋势，但无法精确量化黑客程度。UnifiedReward本身也可能存在与人类偏好不完全对齐的问题。
3. **超参数敏感性**：$\beta$ 和 $\tau$ 的最优取值具有任务依赖性，需要针对不同任务进行调参。不当的超参数组合可能导致优化不足或训练崩溃（如 $\beta=4$ 时GenEval任务的崩溃）。

![[assets/figures/papers/paper_list_l2680_https_arxiv_org_abs_2601_02036/figures/008_Table_3.jpg]]
*Table 3: Quantitative results. We report the quantitative metrics on evaluation time rewards, UnifiedReward scores, and GPU hours*

![[assets/figures/papers/paper_list_l2680_https_arxiv_org_abs_2601_02036/figures/006_Figure_4.jpg]]
*Figure 4: Qualitative results on OCR and GenEval. Columns 1-4 show the OCR task, and Columns 5-8 display the GenEval task*

![[assets/figures/papers/paper_list_l2680_https_arxiv_org_abs_2601_02036/figures/009_Figure_6.jpg]]
*Figure 6: Curves of ablation studies. We plot the evaluation scores across optimization steps across different ablation studies*

![[assets/figures/papers/paper_list_l2680_https_arxiv_org_abs_2601_02036/figures/011_Figure.jpg]]
*Figure: viii. Ablation study on temperature. We provide the evaluation curves on different choices of the temperature τ*

![[assets/figures/papers/paper_list_l2680_https_arxiv_org_abs_2601_02036/figures/012_Figure.jpg]]
*Figure: FLUX.1(0.58) Flow-GRPO (0.87) Ours (0.87) Figure ix. More visualizations on OCR. We provide more comparisons between our method and Flow-GRPO when the evaluation reward is the same on the OCR task*

## 定位与知识库关联

### 与基线方法的关系

GDRO 处于扩散模型奖励后训练的谱系中，其设计直接回应了当前在线强化学习范式在 rectified flow 模型上的结构性缺陷。理解这一谱系需要从三个维度展开：训练模式、采样器依赖和损失函数设计。

**在线 RL 基线：Flow-GRPO 与 DanceGRPO。** 这两类方法继承自 LLM 对齐中成熟的 PPO/GRPO 策略梯度框架，将其迁移至扩散模型时面临根本性障碍。Rectified flow 模型本质上是确定性的，缺乏 DDPM 等随机扩散模型固有的采样噪声。为获取策略梯度所需的随机性，这些方法不得不引入 ODE-to-SDE 近似——在采样过程中注入额外噪声以模拟随机扩散。这一近似带来了双重代价：其一，近似分布与真实分布之间存在偏差，导致分布外（out-of-distribution）问题；其二，每一步优化都需完整的在线采样链，图像生成时间主导了训练开销。从 Table 3 的 GPU 时耗数据可见，Flow-GRPO 在 OCR 任务上消耗 149.07 GPU 小时，DanceGRPO 消耗 74.67 GPU 小时，而 GDRO 仅需 29.60 GPU 小时——效率差距分别达到 5.0× 和 2.5×。

**离线偏好优化基线：Diffusion-DPO。** DPO（**Wallace et al., CVPR 2024**）通过隐式奖励函数将偏好优化转化为离线分类任务，完全规避了在线采样。然而，DPO 的设计仅支持成对偏好（pairwise preference），无法利用更丰富的组级显式奖励信号。GDRO 在理论上将 DPO 作为特例包含：当组大小 $k=2$ 且温度 $\tau \to 0$ 时，GDRO 退化为 DPO。这一退化关系揭示了 GDRO 的核心创新——将 DPO 的成对排名模型推广到基于 Plackett-Luce 排名模型的组级交叉熵框架，从而能够利用任意大小的图像组及其显式奖励进行离线优化。

**预训练基座：FLUX.1。** 作为 rectified flow 模型的代表性基座（**Black-Forest-Labs, 2024**），FLUX.1 提供了未经奖励后训练的初始策略。Table 3 显示，FLUX.1 在 OCR 任务上的原始奖励仅为 0.5843，修正分数为 0.4486，这构成了所有后训练方法的优化起点。

### 适用边界与局限

GDRO 的设计选择同时定义了其适用边界。该方法的核心前提是**完全离线训练**，这意味着它依赖预生成的图像组及其显式奖励作为训练数据。这一设计在带来效率优势的同时，也划定了其适用边界：

**离线数据的静态性限制。** GDRO 不进行在线探索，其优化完全基于预生成的固定图像组。在奖励信号与生成策略之间存在强耦合的任务中——例如需要主动探索以获得高奖励的 3D 理解或复杂交互场景——这种静态性可能导致优化触及离线数据的性能上限。论文明确指出，缺乏在线探索能力是当前方法的主要局限，未来需要研究如何将在线探索机制融入 GDRO 框架。

**奖励黑客的缓解而非根除。** 尽管 GDRO 相比 Flow-GRPO 显著缓解了奖励黑客（见 Figure 4 定性对比：Flow-GRPO 图像退化为平面绘图风格，而 GDRO 保持视觉质量和细节），但消融实验揭示了其脆弱性窗口。Figure 6 的 $\beta$ 消融曲线表明，在 OCR 任务上 $\beta=6$ 会导致快速奖励黑客（修正分数下降），而 $\beta=12$ 保持稳定。类似地，温度 $\tau=0.025$ 会导致训练曲线不稳定甚至崩溃（Figure viii）。这些结果表明，GDRO 的稳定性依赖于超参数的谨慎选择，并非对奖励黑客完全免疫。

**评价指标的固有局限。** 论文提出的修正分数（corrected score）通过结合评价奖励 $r$ 和 UnifiedReward 来更客观地刻画奖励黑客，但其公式 $r_{\mathrm{corrected}} = r(\hat{u} - 3) + 0.2$ 本质上是一种启发式组合。论文承认，这一指标无法精确建模黑客程度，仅能反映趋势。在需要精细区分质量退化程度的场景中，修正分数可能不足以提供充分的可解释性。

### 开放问题

GDRO 的提出为扩散模型奖励后训练开辟了若干值得探索的方向：

1. **在线-离线混合训练。** 当前 GDRO 的完全离线特性既是效率优势的来源，也是探索能力的瓶颈。一个自然的问题是：能否在 GDRO 框架中引入受控的在线探索，例如周期性地用当前策略生成新图像组以更新训练数据，从而在保持大部分效率优势的同时突破离线数据的上限？这需要在探索收益与计算成本之间寻找平衡点。

2. **更精确的奖励黑客检测指标。** 修正分数对 UnifiedReward 的依赖使其受限于该奖励模型的判别能力。设计能够更精细捕捉奖励黑客细微退化的自动评价指标——例如利用对比学习嵌入空间中的分布偏移度量——将有助于更可靠地评估后训练方法的真实效果。

3. **跨生成式架构的泛化。** GDRO 的核心机制——通过隐式奖励函数将组级显式奖励转化为排名导向的交叉熵目标——在理论上不限于扩散模型。这一框架是否可扩展至自回归视觉生成模型（如基于 next-token prediction 的图像生成器）或其他生成式架构，是一个值得验证的开放问题。关键在于隐式奖励函数在这些架构中是否仍具有可计算的近似形式。

4. **组大小与奖励多样性的关系。** 消融实验表明组大小 $k=6$ 在 OCR 任务上获得最优表现（Figure 6），但这一结论是否依赖于奖励函数的具体特性？当奖励信号稀疏或存在多个局部最优时，更大的组是否必然带来更好的排名对齐？对组大小与奖励分布特性之间关系的理论分析可能指导自适应组大小策略的设计。

## 原文 PDF

![[paperPDFs/CVPR_2026/GDRO_Group_level_Reward_Post_training_Suitable_for_Diffusion_Models.pdf]]
