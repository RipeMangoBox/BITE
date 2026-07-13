---
title: "NoRD: A Data-Efficient Vision-Language-Action Model that Drives without Reasoning"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/NoRD_A_Data_Efficient_Vision_Language_Action_Model_that_Drives_without_Reasoning.pdf
project_link: null
code_link: "https://waymo.com/open/challenges/2025/e2e-driving/"
aliases:
- NNRD
- NoRD
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 移除GRPO优势估计中的组内标准差归一化项，直接使用均值中心化优势，消除对高方差样本的惩罚偏差。
primary_logic: 通过使用Dr. GRPO去除优势函数中的标准差归一化，并结合不对称裁剪与无KL散度正则化，RL后训练能够对弱SFT策略产生的全部样本（包括高方差困难场景）施加有效的梯度信号，从而在无推理标注和仅使用少量驾驶数据（<60%）的条件下，将PDM得分提升11.68%，达到与需要推理标注和大规模数据的方法可比的性能。
claims:
- GRPO后训练在NORD-BASE上仅带来0.67%的PDM得分提升，表明其几乎无法从弱SFT策略中学习。
- Dr. GRPO替换GRPO后，NORD-BASE的PDM得分从76.66提升至85.62，相对提升11.68%。
- GRPO主要优化低组内方差（难度低）的样本，而Dr. GRPO成功优化了中、高方差样本。
- Dr. GRPO在所有子指标上几乎一致优于GRPO，仅在Ego Progress上略逊。
---

# NoRD: A Data-Efficient Vision-Language-Action Model that Drives without Reasoning

> [!tip] 核心洞察
> 通过使用Dr. GRPO去除优势函数中的标准差归一化，并结合不对称裁剪与无KL散度正则化，RL后训练能够对弱SFT策略产生的全部样本（包括高方差困难场景）施加有效的梯度信号，从而在无推理标注和仅使用少量驾驶数据（<60%）的条件下，将PDM得分提升11.68%，达到与需要推理标注和大规模数据的方法可比的性能。

| 字段 | 内容 |
|------|------|
| 中文题名 | NoRD：一种无需推理的数据高效视觉-语言-动作模型 |
| 英文题名 | NoRD: A Data-Efficient Vision-Language-Action Model that Drives without Reasoning |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2602.21172) · [Code](https://waymo.com/open/challenges/2025/e2e-driving/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | NoRD (No Reasoning for Driving) |
| Dataset | NAVSIM, WaymoE2E, NAVSIM (navtest) RL提升分析 |

> [!tip] 效果简介
> - NAVSIM (navtest) 上，PDM Score ↑ 85.62 (NoRD) vs 89.1 (AutoVLA) (-3.48)。
> - NAVSIM (navtest, Best-of-6) 上，PDM Score ↑ 92.4 (NoRD-BoN) vs 92.1 (AutoVLA-BoN) (+0.3)。
> - WaymoE2E 上，Rated Feedback Score (RFS) ↑ 7.709 (NoRD) vs 7.556 (AutoVLA) (+0.153)。

## 概要

自动驾驶的视觉-语言-动作（VLA）模型近期取得了显著进展，但主流方法普遍依赖两个高成本要素：大规模驾驶数据与稠密的推理链（Chain-of-Thought）标注。这种范式不仅推高了数据获取与标注成本，还导致模型在推理时产生大量冗余token，限制了实时部署效率。一个核心问题随之浮现：**能否在不使用推理标注和大量数据的条件下，训练出具有竞争力的VLA模型？**

NoRD（No Reasoning for Driving）给出了肯定的回答。该方法仅使用不足60%的驾驶数据，且完全摒弃推理标注，直接在Qwen-2.5VL-3B-Instruct多模态基座上通过监督微调（SFT）与强化学习后训练（RL）构建驾驶策略。然而，初步实验揭示了一个关键瓶颈：标准的组相对策略优化（GRPO）在弱SFT策略上几乎失效，仅带来微乎其微的性能提升（PDM得分+0.67%）。

深入分析表明，**失效根源于一种“难度偏差”**：弱SFT策略产生的轨迹奖励在组内呈极化分布——低难度场景方差小、易优化，而占据多数的中高难度场景方差大。GRPO的优势估计中包含除以组内标准差的归一化操作，这会对高方差样本的梯度信号产生强烈衰减，导致RL后训练几乎只提升低方差样本，对整体性能改善极其有限。

针对这一发现，NoRD引入**Dr. GRPO**作为替代优化算法。其核心改动简洁而关键：**移除GRPO优势估计中的组内标准差归一化项，直接使用均值中心化优势**，从而消除对高方差样本的惩罚偏差。配合不对称裁剪与无KL散度正则化的设计，Dr. GRPO能够对弱SFT策略产生的全部样本施加有效的梯度信号。

这一改进带来了决定性的性能跃升：在NAVSIM基准上，NoRD-BASE经Dr. GRPO后训练后，PDM得分从76.66提升至85.62，相对提升**11.68%**；在WaymoE2E端到端驾驶基准上，NoRD以远少于基线模型的数据量取得排名第三的Rated Feedback Score，并拥有最低的平均位移误差（ADE@3s = 1.2504）。在Best-of-6设置下，NoRD的PDM得分（92.4）甚至超越了需要推理标注和大规模数据的AutoVLA（92.1），证明了数据高效、无推理VLA范式的可行性。



### 端到端自动驾驶的VLA范式与数据瓶颈

视觉-语言-动作（Vision-Language-Action, VLA）模型已成为端到端自动驾驶领域的前沿范式。这类模型将多视图图像、车辆状态和驾驶指令作为输入，通过大规模预训练的语言模型骨干直接生成未来轨迹，从而将感知、决策和规划统一在一个自回归框架中。然而，当前主流的VLA训练流程存在两个核心瓶颈：

1. **对大规模推理标注的强依赖**：现有方法（如 **AutoVLA**，Zhou et al., NeurIPS 2025）通常需要为驾驶数据生成稠密的思维链（Chain-of-Thought）推理标注，以引导模型学习“如何驾驶”的显式推理过程。这一过程不仅标注成本极高，还使模型在推理时产生大量冗余token，降低了实时性。
2. **数据效率低下**：即便使用了海量驾驶数据，标准强化学习后训练方法（如GRPO）在弱监督微调（SFT）策略上的性能提升仍然极其有限。实验表明，在NoRD-BASE上应用GRPO后训练仅带来**+0.67%**的PDM得分提升（Table 1），远不足以弥补与需要推理标注方法的性能差距（>12分）。

### GRPO失效的根本原因：难度偏差

为什么GRPO在弱SFT策略上几乎失效？本文通过分析NoRD-BASE的组内奖励分布，揭示了一个关键机制——**难度偏差（Difficulty Bias）**。

弱SFT策略产生的轨迹奖励在组内呈现**极化分布**：低难度场景（如直道巡航）的奖励方差小、易于优化；而中高难度场景（如复杂路口、急转弯）的奖励方差大，且占据样本的绝大多数（Figure 2）。标准GRPO在计算优势函数时，对组内奖励进行均值中心化后**除以标准差**进行归一化：

$$ \hat{A}_{i,t}^{\mathrm{GRPO}} = \frac{r_i - \mu_{\text{group}}}{\sigma_{\text{group}}} $$

这一归一化操作对高方差样本的梯度信号产生**强烈衰减**——高方差样本的优势估计被标准差大幅压缩，导致RL后训练几乎只对低方差样本施加有效更新，而对占多数的中高难度场景无能为力（Figure 3a）。这种“只优化简单场景”的偏差，使得GRPO后训练对整体驾驶性能的改善近乎停滞。

### 本文动机：无推理、数据高效的VLA训练

上述分析揭示了一个核心矛盾：**VLA模型的能力瓶颈并非来自是否具备显式推理，而是来自RL后训练能否有效利用弱SFT策略产生的全部信号**。这引出了本文的核心动机：

- **能否在不依赖推理标注和大规模数据的前提下，训练出具有竞争力的VLA模型？**
- **能否设计一种新的RL后训练方法，消除GRPO中的难度偏差，使弱SFT策略也能从高方差困难场景中有效学习？**

为此，本文提出**NoRD（No Reasoning for Driving）**——一种数据高效、无需推理的VLA模型，并配套设计**Dr. GRPO**强化学习算法作为GRPO的直接替代。NoRD仅使用不到60%的驾驶数据，完全去除推理标注，直接预测轨迹token（Figure 1b）；而Dr. GRPO通过移除优势估计中的标准差归一化，从根本上消除对高方差样本的惩罚偏差，使RL后训练能够对全部难度层级的样本施加有效的梯度信号。



## 核心方法与创新机理

NoRD 的核心创新在于**系统性地证明了“无推理”VLA 模型在数据高效场景下的可行性，并针对性地解决了弱监督策略在 RL 后训练中遭遇的“难度偏差”问题**。该工作并非提出全新的模型架构，而是通过精准的诊断与算法层面的轻量级改造，使一个仅在小规模驾驶数据（<60%）上微调、且完全不含推理链标注的基础模型，能够通过强化学习获得显著的性能提升。

### 1. 关键瓶颈诊断：GRPO 的“难度偏差”

NoRD 首先构建了一个弱监督的基线模型 **NoRD-BASE**（基于 Qwen-2.5VL-3B-Instruct，仅用 80,000 个 NAVSIM 样本进行 SFT，无推理标注）。当对 NoRD-BASE 应用标准的 **GRPO** 进行 RL 后训练时，发现其性能提升微乎其微（PDM 得分仅提升 +0.67%）。

通过分析奖励分布，研究揭示了根本原因：NoRD-BASE 生成的轨迹奖励在组内呈现**极化分布**（Figure 2）。低难度场景的轨迹奖励方差小，易于优化；而中高难度场景的轨迹奖励方差大，且占样本的大多数。标准 GRPO 的优势估计进行了组内标准差归一化（即 $\hat{A} = (r_i - \mu) / \sigma$），这导致对高方差样本的梯度信号产生了**强烈的衰减效应**。因此，GRPO 的优化过程几乎只作用于低方差样本，而对大量中高难度的关键场景束手无策，形成了“难度偏差”，限制了整体性能的提升。

### 2. 核心算法创新：Dr. GRPO

为解决上述瓶颈，NoRD 引入了 **Dr. GRPO** 作为标准 GRPO 的替代品。其核心改动在于**修改了优势估计中的关键控制旋钮**，并配套了稳定弱策略训练的优化策略。

#### 2.1 移除标准差归一化

Dr. GRPO 的核心操作是**直接移除了 GRPO 优势估计中的组内标准差归一化项**，改为仅使用均值中心化的优势函数。该改动精准地消除了对高方差样本的惩罚偏差，使所有样本——无论其组内方差高低——都能接收到有效的梯度信号。

具体而言，Dr. GRPO 的优势函数定义为：

$$
\hat{A}_{i,t}^{\mathrm{DrGRPO}} = r(o_i \mid x) - \frac{1}{G} \sum_{j=1}^{G} r(o_j \mid x)
$$

其中 $r(o_i \mid x)$ 是第 $i$ 个输出 $o_i$ 的奖励，$G$ 是组大小。与标准 GRPO 相比，该公式不再除以组内标准差 $\sigma$，从而避免了难度偏差。

#### 2.2 不对称裁剪与无 KL 正则化

为在弱 SFT 策略上实现稳定的 RL 后训练，Dr. GRPO 还引入了两项配套优化：

-   **不对称裁剪**：采用 DAPO 风格的不对称裁剪策略（低裁剪 -0.2，高裁剪 0.1），以替代标准 PPO 的对称裁剪。这有助于在策略更新幅度较大时提供更灵活的保护。
-   **移除 KL 散度正则化**：完全移除了 RL 损失函数中的 KL 散度惩罚项，仅依靠裁剪机制来保证策略更新的稳定性，避免了 KL 惩罚可能对弱策略探索能力的过度限制。

最终的 Dr. GRPO 损失函数为：

$$
\mathcal{L}_{\mathrm{DrGRPO}} = \sum_{t=1}^{|o_i|} \operatorname{min} \left( \frac{\pi_\theta(o_{i,t}|q,o_{i,<t})}{\pi_{\theta_{\mathrm{old}}}(o_{i,t}|q,o_{i,<t})} \hat{A}_{i,t}^{\mathrm{DrGRPO}} , \operatorname{clip} \left( \frac{\pi_\theta(o_{i,t}|q,o_{i,<t})}{\pi_{\theta_{\mathrm{old}}}(o_{i,t}|q,o_{i,<t})} , 1-\epsilon_1, 1+\epsilon_{\mathrm{h}} \right) \hat{A}_{i,t}^{\mathrm{DrGRPO}} \right)
$$

### 3. 数据与表征层面的高效设计

除了 RL 后训练算法的创新，NoRD 在数据与表征层面也做出了关键改变，共同构成了其“无推理、数据高效”的特性。

-   **训练数据类型**：与依赖大规模数据集和稠密推理链（Chain-of-Thought）标注的基线方法（如 **AutoVLA** (Zhou et al., NeurIPS 2025)）不同，NoRD **仅使用缩小的驾驶数据（<60%），且完全无推理标注**。模型直接学习从感知输入到轨迹 token 的映射。
-   **轨迹表征方式**：NoRD 采用 **k-disc tokenization** 方法，将连续的未来轨迹段聚类为 2048 个离散 token，并加入模型的词汇表。这使得模型能够以自回归的方式直接生成代表未来轨迹的 token 序列，如 `TRAJ 0242`，避免了复杂的坐标回归，简化了学习目标。

### 4. 创新效果验证

这些创新带来了显著的性能提升。**Table 1** 的结果直接证明了 Dr. GRPO 的有效性：在 NoRD-BASE 上应用 Dr. GRPO 进行 RL 后训练，PDM 得分从 76.66 跃升至 85.62，**相对提升高达 11.68%**，与 GRPO 的无效优化形成鲜明对比。

训练动态分析（Figure 3）进一步揭示了因果机制：GRPO 的改进主要集中在低方差样本，而 **Dr. GRPO 成功逆转了这一趋势，有效地优化了中、高方差样本**，从而带来了整体性能的大幅增长。定性结果（Figure 4）也显示，Dr. GRPO 使模型学会了复杂转弯等机动，而 GRPO 则失败并导致碰撞。

最终，这种无推理、数据高效的范式使 NoRD 在 **WaymoE2E** 基准上，以远少于基线模型的数据量，在不使用推理标注和模型集成的前提下，取得了排名第三的 RFS 分数，并拥有最低的 ADE（Table 2），证明了其在性能与效率上的双重竞争力。



NoRD 的整体设计围绕一个核心原则展开：**在不依赖任何推理标注的前提下，用尽可能少的驾驶数据训练出高性能的视觉-语言-动作（VLA）模型**。图 5 给出了完整的前向推理流程——多视图图像与自车状态进入视觉编码器，经语言模型主干直接自回归地输出代表未来轨迹的离散 token，再由解码器恢复为可执行的轨迹点序列。整个过程没有生成任何自然语言推理链，因此模型的 token 产出量和推理延迟均显著低于需要 CoT 的 VLA 方案（图 9）。

### 输入与感知模块

模型接收三类输入：
1. **多视图图像**：前、前左、前右三帧 RGB 图像（仅 3 个相机，无 LiDAR），由 **Qwen-2.5VL** 的视觉编码器（Bai et al., arXiv 2025）提取视觉特征。
2. **自车历史状态**：过去 1.5 秒的轨迹 token、当前速度、加速度，以及高层驾驶指令（如左转、直行等）。
3. **任务提示**：结构化的文本提示，告知模型当前驾驶上下文。

视觉特征与历史状态被拼接后送入语言模型主干，构成统一的多模态上下文。

### 语言模型主干与动作生成

NoRD 的语言模型主干为 **Qwen-2.5VL-3B-Instruct**（Bai et al., arXiv 2025）。与现有 VLA 方法的关键区别在于，该主干不生成任何推理文本，而是直接自回归地预测代表未来轨迹的离散 token 序列。轨迹的离散化采用 **k-disc tokenization**：将轨迹段聚类为 2048 个离散 token（如 `TRAJ 0242`），并将其加入词汇表。这使得轨迹预测与语言模型的标准自回归生成完全兼容，无需额外的回归头或坐标解码器。

### 轨迹解码与后处理

生成的离散轨迹 token 经解码器映射回 10 Hz 的轨迹点序列 `[x, y, yaw]`，直接作为下游规划器的输入。整个流程从像素到轨迹点端到端可微，且推理阶段仅需一次前向传播。

### 强化学习后训练：Dr. GRPO

NoRD 的训练分为两个阶段：
1. **弱监督微调（Weak SFT）**：仅使用约 80,000 个 NAVSIM 训练样本（不足全量数据的 60%），完全不包含推理标注。此阶段得到的 **NoRD-BASE** 策略性能显著低于需要推理标注的基线方法（PDM 得分差距超过 12 分）。
2. **Dr. GRPO 强化学习后训练**：针对弱 SFT 策略的奖励分布特性，采用移除标准差归一化的组相对策略优化。具体而言，Dr. GRPO 的优势函数直接使用奖励与组均值的差值（$\hat{A}_{i,t}^{\mathrm{DrGRPO}} = r(o_i \mid x) - \frac{1}{G} \sum_{j=1}^{G} r(o_j \mid x)$），而非标准 GRPO 的均值中心化后再除以组内标准差。损失函数采用 DAPO 风格的不对称裁剪（低裁剪 -0.2，高裁剪 0.1），并完全移除 KL 散度正则化，仅通过裁剪保证策略更新稳定。

这一后训练流程使 NoRD-BASE 的 PDM 得分从 76.66 提升至 85.62（相对提升 11.68%），而标准 GRPO 在同样条件下仅带来 0.67% 的微弱提升（Table 1）。

### 数据流总结

```
多视图RGB (3帧) ──→ 视觉编码器 ──┐
                                  ├──→ 语言模型主干 ──→ 轨迹token序列 ──→ 解码器 ──→ [x,y,yaw]轨迹
自车状态 + 驾驶指令 ─────────────┘       (Qwen-2.5VL-3B)    (k-disc, 2048词表)
```

整个 pipeline 的设计使得 NoRD 在 NAVSIM 上成为唯一同时处于高性能区和高数据效率区的 VLA 模型（Figure 6a），并在 WaymoE2E 上以远少于基线模型的数据量取得排名第三的 RFS，同时拥有最低的 ADE（Table 2）。

### 补充图表

![[assets/figures/papers/paper_list_l2238_https_arxiv_org_abs_2602_21172/figures/008_Figure_5.jpg]]
*Figure 5: Model architecture of NORD. NORD directly predicts action tokens without requiring reasoning traces, enabling a significantly more efficient training and inference pipeline*



### 3.1 弱SFT策略的难度偏差：问题根源

NoRD的核心发现源于对弱监督微调（SFT）后策略行为的深入分析。当使用仅80,000个NAVSIM样本且无推理标注的数据对**Qwen-2.5VL-3B-Instruct**进行SFT后，得到的NoRD-BASE模型在组内奖励分布上呈现出显著的极化现象（**Figure 2**）：

![[assets/figures/papers/paper_list_l2238_https_arxiv_org_abs_2602_21172/figures/002_Figure_2.jpg]]
*Figure 2: Reward distribution in the weak SFT model. The group-mean PDM score is shown with band representing the mean of the corresponding group standard deviation for NORD-BASE. GRPO struggles to optimize high-variance regions (the majority) and is effective only in low-variance regions (the trajectories in green and red are for ground truth and NORD-BASE prediction)*

- **低难度场景**：组内方差小，PDM得分集中在高分段，优化空间有限
- **中高难度场景**：组内方差大，PDM得分分布在[0.2, 0.65]区间，占据样本多数

标准GRPO的优势估计公式为 $\hat{A}_{i,t} = \frac{r_i - \mu}{\sigma}$，其中除以组内标准差 $\sigma$ 的归一化操作对高方差样本产生强烈的梯度信号衰减。这导致RL后训练几乎只提升低方差样本，而对占据多数的中高难度场景几乎无效——NoRD-BASE经GRPO后训练仅获得+0.67%的PDM得分提升（**Table 1**）。

### 3.2 Dr. GRPO：去除标准差归一化的优势估计

为解决上述难度偏差，NoRD采用Dr. GRPO作为RL后训练算法。其核心改动仅涉及一个因果调节变量：**移除GRPO优势估计中的组内标准差归一化项**。

**Dr. GRPO优势函数**（Equation 1）：

$$\hat{A}_{i,t}^{\mathrm{DrGRPO}} = r(o_i \mid x) - \frac{1}{G} \sum_{j=1}^{G} r(o_j \mid x)$$

其中：
- $r(o_i \mid x)$：第 $i$ 条轨迹在输入 $x$ 下的奖励值
- $G$：组内采样轨迹数量
- $\frac{1}{G} \sum_{j=1}^{G} r(o_j \mid x)$：组内奖励均值 $\mu$

与标准GRPO的 $\hat{A} = (r_i - \mu)/\sigma$ 相比，Dr. GRPO直接使用均值中心化优势 $r_i - \mu$，消除了 $\sigma$ 对高方差样本的惩罚性衰减。这一简单改动使得RL训练能够对弱SFT策略产生的全部样本（包括高方差困难场景）施加有效的梯度信号。

### 3.3 不对称裁剪与无KL正则化的损失设计

为稳定弱SFT策略的RL后训练，Dr. GRPO引入了两项配套设计：

**Dr. GRPO损失函数**（Equation 2）：

$$\mathcal{L}_{\mathrm{DrGRPO}} = \sum_{t=1}^{|o_i|} \min \left( \frac{\pi_\theta(o_{i,t}|q,o_{i,<t})}{\pi_{\theta_{\mathrm{old}}}(o_{i,t}|q,o_{i,<t})} \hat{A}_{i,t}^{\mathrm{DrGRPO}}, \operatorname{clip} \left( \frac{\pi_\theta(o_{i,t}|q,o_{i,<t})}{\pi_{\theta_{\mathrm{old}}}(o_{i,t}|q,o_{i,<t})}, 1-\epsilon_1, 1+\epsilon_{\mathrm{h}} \right) \hat{A}_{i,t}^{\mathrm{DrGRPO}} \right)$$

其中：
- $\pi_\theta$：当前策略，$\pi_{\theta_{\mathrm{old}}}$：旧策略
- $\frac{\pi_\theta}{\pi_{\theta_{\mathrm{old}}}}$：重要性采样比率
- $\epsilon_1 = 0.2$（低裁剪），$\epsilon_{\mathrm{h}} = 0.1$（高裁剪）：**DAPO风格的不对称裁剪**，对策略更新幅度进行非对称约束
- 完全**移除KL散度正则化项**，仅通过裁剪保证更新稳定性，避免策略熵崩溃

### 3.4 轨迹表征：k-disc离散化

NoRD将连续轨迹转化为离散token序列以适配语言模型的自回归生成范式。具体采用**k-disc tokenization**：

- 将轨迹段通过聚类算法映射到大小为**2048**的离散词汇表
- 每个token形如 `TRAJ 0242`，直接加入语言模型的词汇表
- 解码时将离散token序列恢复为10Hz的轨迹点序列 $[x, y, yaw]$

消融实验（**Table 5**）表明，将词汇量从2048降至512会导致PDM得分从85.62下降至83.07，证明足够的token粒度对表达复杂机动（如急转弯、变道）至关重要。

### 3.5 奖励函数设计

针对不同基准，NoRD采用数据集专用奖励：

- **NAVSIM**：直接使用PDM评分作为奖励
  $$\mathrm{PDM Score} = \mathrm{NC} \times \mathrm{DAC} \times \frac{5 \cdot \mathrm{TTC} + 2 \cdot \mathrm{C} + 5 \cdot \mathrm{EP}}{12}$$
  综合安全性（无碰撞NC、可行驶区域合规DAC）、舒适性（舒适度C）和进展（自车进度EP、碰撞时间TTC）

- **WaymoE2E**：使用归一化RFS评分
  $$\mathrm{Normalized \ RFS} = \frac{\max(\max_r(s_r), 4) - 4}{6}$$
  将原始评分线性映射到 $[0,1]$ 区间

最终RL奖励由三项加权合并：
$$r = \frac{r_f + r_l + r_d}{1.5}$$
其中 $r_f$ 为格式奖励，$r_l$ 为长度奖励，$r_d$ 为数据集专用奖励。

### 补充图表

![[assets/figures/papers/paper_list_l2238_https_arxiv_org_abs_2602_21172/figures/006_Figure_3.jpg]]
*Figure 3: Evolution of group-mean PDM score during RL fine-tuning. (a) GRPO struggles to optimize samples with high group variance during training, particularly in the range [0.2–0.65]. (b) Dr. GRPO effectively optimizes high-variance samples during training, resulting in significant overall performance gains*



## 实验与关键发现

### 1. 核心瓶颈：GRPO 后训练为何失效？

NoRD 的实验起点是一个令人困惑的现象：对弱监督微调（SFT）策略 **NoRD-BASE** 施加标准的 **GRPO**（Group Relative Policy Optimization）强化学习后训练，几乎无法带来性能提升。在 NAVSIM 的 navtest 子集上，GRPO 后训练仅将 PDM 得分从 76.66 提升至 77.18，相对提升仅 **+0.67%**（Table 1）。这与现有 VLA 方法中 RL 后训练通常能带来显著增益的认知严重矛盾。

![[assets/figures/papers/paper_list_l2238_https_arxiv_org_abs_2602_21172/figures/003_Table_1.jpg]]
*Table 1: Comparison of RL fine-tuning (RLFT) on NORD-BASE with GRPO and Dr. GRPO on NAVSIM test set. While GRPO fails to improve NORD-BASE, we get significant gains with Dr. GRPO*

论文通过分析弱 SFT 策略的组内奖励分布，揭示了这一失效的深层原因——**难度偏差（Difficulty Bias）**。如 Figure 2 所示，NoRD-BASE 策略产生的轨迹奖励在组内呈高度极化分布：
- **低难度场景**：组内奖励方差小，PDM 得分集中在高位（如 0.8–1.0），易于优化。
- **中高难度场景**：组内奖励方差大，PDM 得分分散在 0.2–0.65 区间，占据训练样本的绝大多数。

标准 GRPO 的优势估计公式为 $\hat{A}_i = (r_i - \mu) / \sigma$，其中除以组内标准差 $\sigma$ 的归一化操作，对高方差样本的梯度信号产生了强烈的衰减效应。这使得 GRPO 的优化信号几乎完全集中在低方差（低难度）样本上，而对占据多数的中高方差样本几乎不起作用。**Figure 3(a)** 清晰地展示了这一趋势：在 GRPO 训练过程中，高方差区域（[0.2, 0.65]）的组均值 PDM 得分密度几乎保持不变，仅低方差区域出现明显改善。

**结论**：标准 GRPO 中的标准差归一化，在弱 SFT 策略的极化奖励分布下，系统性地抑制了对困难样本的优化，导致 RL 后训练的整体收益微乎其微。

### 2. 关键改进：Dr. GRPO 的设计与验证

针对上述瓶颈，NoRD 采用 **Dr. GRPO** 作为 GRPO 的直接替代方案。其核心修改是移除优势估计中的标准差归一化，直接使用均值中心化的优势函数：

$$\hat{A}_{i,t}^{\mathrm{DrGRPO}} = r(o_i \mid x) - \frac{1}{G} \sum_{j=1}^{G} r(o_j \mid x)$$

配合 **DAPO 风格的不对称裁剪**（低裁剪 -0.2，高裁剪 0.1）和 **完全移除 KL 散度正则化**，Dr. GRPO 消除了对高方差样本的梯度惩罚，使 RL 后训练能够对所有难度级别的样本施加有效的优化信号。

**Table 1** 的主结果验证了这一设计的有效性：使用 Dr. GRPO 后训练后，NoRD 的 PDM 得分从 76.66 跃升至 **85.62**，相对提升 **+11.68%**（绝对提升 +8.96 PDM Score）。这一增益与 GRPO 的 +0.67% 形成鲜明对比。

**Figure 3(b)** 从训练动态角度提供了更细粒度的证据：Dr. GRPO 成功地将优化信号传递到了中、高方差样本区域，在整个训练过程中，高方差区域的组均值 PDM 得分密度持续上升。**Figure 10** 进一步量化了这一差异：GRPO 的改进几乎完全集中在初始得分 [0.8, 1.0] 的低方差样本（panel a），而 Dr. GRPO 在中方差（panel b）和高方差（panel c）样本上均表现出显著优于 GRPO 的改进密度，大量样本分布在 y=x 线之上。

**Table 4** 的消融对比显示，Dr. GRPO 在 NAVSIM 的几乎全部子指标上均优于 GRPO，仅在 Ego Progress 上略逊。这进一步证实移除标准差归一化是一个普遍有益的改进，而非仅在特定指标上有效。

### 3. 主基准测试结果

#### 3.1 NAVSIM 基准测试

**Table 3** 展示了 NoRD 在 NAVSIM navtest 子集上的完整测试结果。NoRD 仅使用 **3 帧 RGB 图像**（前、前左、前右），无 LiDAR 数据，无推理标注，取得了 **85.62** 的 PDM 得分。这一结果在 BEV 和 VLA 方法中均具有竞争力。特别地，使用 Best-of-6（BoN）策略后，NoRD 的 PDM 得分进一步提升至 **92.4**，略超需要推理标注和大规模数据的 **AutoVLA**（Zhou et al., NeurIPS 2025）的 92.1。

**Figure 6(a)** 的帕累托前沿分析将 NoRD 的数据效率优势可视化：在 NAVSIM 上，NoRD 是唯一一个在“高性能–高数据效率”区域运行的 VLA 模型，仅使用 RGB 输入即达到了与需要 LiDAR 或多帧密集输入的方法可比的性能。

#### 3.2 WaymoE2E 基准测试

**Table 2** 展示了 NoRD 在 Waymo 视觉端到端驾驶基准上的测试结果。NoRD 以 **7.709** 的 Rated Feedback Score（RFS）排名所有 VLA 方法的第三位，且拥有最低的 Average Displacement Error @3s（**ADE@3 = 1.2504**），优于 AutoVLA 的 1.3507。值得注意的是，NoRD 是唯一一个在不使用推理标注、不使用模型集成的前提下取得该排名的模型。对比方法如 Poutine、HMVLM 可能使用了多数据集混合或集成策略，NoRD 在严格公平的效率条件下展现了竞争力。

**Figure 6(b)** 的帕累托前沿分析显示，NoRD 在 WaymoE2E 上仅使用少量训练数据即达到了有竞争力的 RFS，无需集成或推理监督。

### 4. 消融实验与设计选择

#### 4.1 轨迹 Token 化粒度

NoRD 采用 **k-disc tokenization**，将轨迹段聚类为 2048 个离散 token 并加入词汇表进行自回归预测。**Table 5** 的消融实验表明，将词汇量从 2048 降至 512 后，PDM 得分下降至 **83.07**（-2.55）。这证明足够的 token 粒度对于表达复杂机动（如急转弯、换道）至关重要，过小的词汇量会导致轨迹表达能力的显著损失。

![[assets/figures/papers/paper_list_l2238_https_arxiv_org_abs_2602_21172/figures/018_Table_5.jpg]]
*Table 5: Effect of k-disc vocabulary size on the performance of NORD on navtest*

#### 4.2 不对称裁剪与 KL 正则化

Dr. GRPO 采用了不对称裁剪策略（低裁剪 -0.2，高裁剪 0.1），并完全移除了 KL 散度正则化。论文指出，这一设计选择对于稳定弱 SFT 策略的 RL 训练至关重要，避免了策略熵崩溃（详见补充材料 Section 11.2）。**Figure 11** 的训练和验证奖励曲线显示，Dr. GRPO 在整个训练过程中持续且显著地优于 GRPO，验证了该训练配置的稳定性。

![[assets/figures/papers/paper_list_l2238_https_arxiv_org_abs_2602_21172/figures/019_Figure_11.jpg]]
*Figure 11: Training and validation curves for RL fine-tuning with GRPO and Dr.GRPO. Dr.GRPO (in red) consistently outperforms GRPO (in blue) on the (a) training and (b) validation sets by a significant margin*

### 5. 失败模式与残留偏差

尽管 Dr. GRPO 显著缓解了难度偏差，但论文坦诚地指出了其局限性：**难度偏差并未被完全消除**。**Figure 13** 展示了 NoRD 的失败案例，在极端困难场景（如复杂交叉口、施工区域）中，模型仍可能出现不安全行为（如碰撞或违规）。这表明移除标准差归一化虽然大幅改善了中高难度样本的优化，但对于奖励分布极端离散的“最困难”样本，梯度信号可能仍然不足。

论文将此列为开放问题：未来工作可探索针对驾驶任务难度的自适应重加权或动态课程学习，以完全克服难度偏差。

### 6. 效率分析

**Figure 9** 对比了 NoRD 与其他 VLA 方法在 Token 数和推理时间上的效率。由于无需生成推理链，NoRD 的 Token 生成量和推理时间均为所有对比 VLA 中最优，实现了约 **3 倍的 Token 效率**提升。这一效率优势源于 NoRD 直接预测动作 token 的架构设计（Figure 5），省去了现有方法中冗长的 Chain-of-Thought 推理过程。

### 7. 实验设置摘要

- **SFT 阶段**：基于 Qwen-2.5VL-3B-Instruct，在 80,000 个 NAVSIM 训练样本上进行监督微调，无推理标注。
- **RL 后训练阶段**：使用 verl 框架配合 FSDP 和 vLLM 进行 rollout 生成。NAVSIM 上以 PDM 得分作为主奖励，WaymoE2E 上使用归一化 RFS 得分。最终奖励由格式奖励、长度奖励和数据集专用奖励加权合并：$r = \frac{r_f + r_l + r_d}{1.5}$。
- **评估协议**：NAVSIM 使用 PDM Score 综合指标（$\mathrm{PDM Score} = \mathrm{NC} \times \mathrm{DAC} \times \frac{5 \cdot \mathrm{TTC} + 2 \cdot \mathrm{C} + 5 \cdot \mathrm{EP}}{12}$）；WaymoE2E 使用 RFS 和 ADE@3s。BoN 结果基于 6 次不同随机种子的输出取每样本最优得分平均。

### 补充图表

![[assets/figures/papers/paper_list_l2238_https_arxiv_org_abs_2602_21172/figures/009_Table_2.jpg]]
*Table 2: Test results on the Waymo Vision-based End-to-End Driving Benchmark. NORD achieves competitive performance, without reasoning or ensembling*

![[assets/figures/papers/paper_list_l2238_https_arxiv_org_abs_2602_21172/figures/010_Table_3.jpg]]
*Table 3: Test results on NAVSIM benchmark (navtest subset). NORD achieves competitive performance (w/o R: Without reasoning data, w/o L: without LiDAR data, and C: Number of RGB frames; * BoN refers to the average over best score per sample out of 6 outputs with different random seeds)*

![[assets/figures/papers/paper_list_l2238_https_arxiv_org_abs_2602_21172/figures/017_Table_4.jpg]]
*Table 4: Detailed comparison of RL-fine-tuning of NORD-BASE with GRPO and Dr. GRPO. Dr. GRPO based RL fine-tuning is almost always better than GRPO*

![[assets/figures/papers/paper_list_l2238_https_arxiv_org_abs_2602_21172/figures/012_Figure_6.jpg]]
*Figure 6: Pareto-optimal curves on two driving benchmarks. (a) NORD is the only VLA in NAVSIM operating in the high-performance, high–data-efficiency region using only RGB inputs. (b) NORD achieves competitive RFS on WaymoE2E with a fraction of the training data, without ensembling or reasoning supervision. Shaded regions provide a qualitative categorization of model efficiency and performance for ease of visualization*

![[assets/figures/papers/paper_list_l2238_https_arxiv_org_abs_2602_21172/figures/007_Figure_4.jpg]]
*Figure 4: Qualitative comparison of RL fine-tuning (RLFT) on the weak SFT model using GRPO and Dr. GRPO. With Dr. GRPO, NORD successfully learns complex maneuvers such as sharp turns and lane changes without collisions, whereas GRPO fails to optimize the weak SFT model (NORD-BASE) and collides (in red)*

![[assets/figures/papers/paper_list_l2238_https_arxiv_org_abs_2602_21172/figures/015_Figure_9.jpg]]
*Figure 9: Comparison of token and runtime efficiency. NORD is the most (a) token and (b) runtime efficient VLA*



## 定位与知识库关联

### 1. 与基线方法的关系

**NoRD** 的核心方法论建立在两个关键基线的对比与改进之上：**GRPO**（Group Relative Policy Optimization）和 **AutoVLA**（Zhou et al., NeurIPS 2025）。

#### 1.1 与 GRPO 的关系：从失败中诊断，从诊断中改进

GRPO 是当前 VLA 模型 RL 后训练阶段的主流优化算法。NoRD 的研究起点正是一个反直觉的观察：当将标准 GRPO 应用于数据高效、无推理的弱 SFT 策略（NoRD-BASE）时，**RL 后训练几乎失效**——PDM 得分仅提升 +0.67%（Table 1）。这一结果并非源于 GRPO 算法本身的缺陷，而是源于其优势估计机制与弱 SFT 策略奖励分布之间的结构性失配。

NoRD 的诊断揭示了这一失配的精确机制：
- **难度偏差（Difficulty Bias）**：弱 SFT 策略产生的轨迹奖励在组内呈极化分布——低难度场景方差小、易优化，而中高难度场景方差大、占据多数样本。标准 GRPO 的优势归一化（除以组内标准差 $\sigma$）对高方差样本的梯度信号产生强烈衰减，导致 RL 后训练几乎只提升低方差样本，对整体性能改善极其有限。
- **因果旋钮**：Dr. GRPO 通过移除 GRPO 优势估计中的组内标准差归一化项，直接使用均值中心化优势 $\hat{A}_{i,t}^{\mathrm{DrGRPO}} = r(o_i \mid x) - \frac{1}{G} \sum_{j=1}^{G} r(o_j \mid x)$，消除了对高方差样本的惩罚偏差。

这一改进的实质是：**Dr. GRPO 并非否定 GRPO，而是针对弱 SFT 策略这一特定场景，修正了 GRPO 中一个在强策略下无害、在弱策略下致命的归一化操作**。从方法谱系看，Dr. GRPO 可视为 GRPO 的“弱策略适配变体”，其贡献在于揭示了 RL 后训练中难度偏差的存在，并提供了一个极简的修复方案。

#### 1.2 与 AutoVLA 的关系：推理标注的“去冗余化”

**AutoVLA**（Zhou et al., NeurIPS 2025）代表了 VLA 模型的另一条技术路线：通过自适应推理（adaptive reasoning）和稠密的推理链（Chain-of-Thought）标注，结合大规模数据训练，在 NAVSIM 和 WaymoE2E 上取得领先性能（PDM Score 89.1, RFS 7.556）。

NoRD 与 AutoVLA 的核心差异在于对“推理”角色的根本性不同判断：
- AutoVLA 将推理视为提升驾驶性能的关键中间表征，需要额外的推理标注数据。
- NoRD 证明：**在数据高效设定下，推理标注并非必需**。通过直接预测轨迹 token（k-disc tokenization）并结合 Dr. GRPO 后训练，NoRD 在仅使用 <60% 的数据量、无任何推理标注的条件下，在 WaymoE2E 上取得 RFS 7.709（超越 AutoVLA 的 7.556），在 NAVSIM 上取得 PDM Score 85.62（略低于 AutoVLA 的 89.1，但在 Best-of-6 设定下以 92.4 反超 92.1）。

这一对比揭示了 VLA 模型的一个关键知识库定位：**推理标注的价值高度依赖于数据规模**。在大数据场景下，推理链可能提供有用的归纳偏置；但在数据高效场景下，推理标注的生成成本与模型性能提升之间的边际效益可能为负——NoRD 用更少的 token（3× fewer tokens）和更低的推理成本（Figure 9）达到了可比甚至更优的性能。

#### 1.3 与其他 VLA 方法的谱系定位

在更广泛的 VLA 方法谱系中，NoRD 占据了一个独特位置：
- **数据效率维度**：NoRD 是唯一在 NAVSIM 帕累托前沿（Figure 6a）中同时占据高性能和高数据效率区域的纯视觉 VLA 模型，其训练数据量远少于 Poutine、HMVLM 等需要多数据集混合或模型集成的方法。
- **推理需求维度**：NoRD 明确放弃了推理链，与 EMMA、DriveVLM 等依赖显式推理的 VLA 形成对比。这一选择带来了显著的 token 效率和推理速度优势（Figure 9），但代价是模型行为缺乏可解释的中间步骤。
- **传感器效率维度**：NoRD 仅使用 3 帧 RGB 图像（前、前左、前右），不使用 LiDAR，在传感器配置上属于最轻量级的一类 VLA。

### 2. 适用边界与局限

#### 2.1 难度偏差的残留

尽管 Dr. GRPO 显著缓解了难度偏差，但**未能完全消除**。Figure 13 的失败案例分析显示，在极端困难场景（如复杂交叉口、施工区）中，NoRD 仍可能出现不安全行为。这表明：
- Dr. GRPO 的均值中心化优势虽然避免了对高方差样本的过度惩罚，但并未主动提升对这些样本的优化强度。
- 对于奖励分布中方差极大的“长尾困难样本”，仅靠移除归一化不足以提供足够的梯度信号。

#### 2.2 轨迹表征的粒度依赖

NoRD 的 k-disc tokenization 将轨迹聚类为 2048 个离散 token。Table 5 的消融实验显示，将词汇量降至 512 会导致 PDM 得分下降至 83.07（-2.55 分）。这表明：
- **足够的 token 粒度对表达复杂机动至关重要**。2048 的词汇量在 NAVSIM 和 WaymoE2E 上足够，但在更复杂的城市路况或需要更精细轨迹控制的场景中可能需要进一步扩展。
- k-disc tokenization 本身是一种有损压缩，其聚类质量依赖于训练数据的覆盖度。在 OOD 场景下，离散 token 可能无法精确表达所需的轨迹形状。

#### 2.3 跨平台泛化未验证

当前验证仅限于 NAVSIM 和 WaymoE2E 两个仿真基准。虽然这两个基准覆盖了多种驾驶场景（Table 6 展示了 WaymoE2E 各场景的详细评分），但：
- 仿真环境与真实世界的分布差异可能导致性能退化。
- Dr. GRPO 的难度偏差诊断基于这两个数据集的奖励分布特征，在其他平台或奖励函数设计下，偏差的表现形式可能不同。

#### 2.4 可解释性的固有缺失

由于完全无推理，NoRD 的决策过程是一个从多视图图像到轨迹 token 的黑箱映射（Figure 5, Figure 12）。在安全性要求极高的场景中，这一设计可能面临以下挑战：
- 无法追溯模型的“思考过程”，难以进行针对性的错误归因。
- 在需要向监管机构或用户解释驾驶决策的场景中缺乏透明性。

### 3. 开放问题

基于上述分析，NoRD 开启或留待解决的开放问题包括：

1. **难度偏差的完全消除**：能否设计针对驾驶任务难度的自适应重加权或动态课程机制，使 RL 后训练能够完全克服难度偏差？例如，基于组内方差的动态优势缩放，或在训练过程中主动采样困难样本。

2. **无推理 VLA 的极限边界**：数据高效的无推理 VLA 是否可以拓展到更复杂的城市路况和长尾场景，而无需海量数据？NoRD 在 <60% 数据下的成功提示了一个可能的方向，但该比例的下限在哪里？

3. **“潜在推理”的可能性**：是否可能在保持无推理优势（token 效率、推理速度）的同时，融入轻量级的“潜在推理”或可选的推理片断，以在极端情况下提升安全性？这需要在效率与可解释性之间寻找新的平衡点。

4. **Dr. GRPO 的跨领域迁移**：Dr. GRPO 的核心洞察——弱 SFT 策略的奖励分布极化导致标准 GRPO 失效——是否在具身智能或机器人操作等其他领域的弱 SFT 策略优化中同样成立？这一问题的回答将决定 Dr. GRPO 是驾驶特定的技巧，还是 RL 后训练的一个通用改进。

5. **k-disc tokenization 的理论基础**：当前词汇量 2048 的选择基于经验消融（Table 5），缺乏对最优词汇量与轨迹复杂度之间关系的理论分析。如何根据场景的机动复杂度自适应调整 token 粒度，是一个值得探索的方向。

---

**小结**：NoRD 在 VLA 方法谱系中定位为“数据高效、无推理”路线的代表性工作。它通过 Dr. GRPO 修正了标准 GRPO 在弱 SFT 策略下的难度偏差，证明在放弃推理标注和减少数据量的条件下仍可达到竞争性能。但其适用边界受限于难度偏差的残留、token 粒度的依赖和可解释性的缺失，这些限制也为后续研究指明了方向。



## 原文 PDF

![[paperPDFs/CVPR_2026/NoRD_A_Data_Efficient_Vision_Language_Action_Model_that_Drives_without_Reasoning.pdf]]
