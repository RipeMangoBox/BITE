---
title: "DiverseGRPO: Mitigating Mode Collapse in Image Generation via Diversity-Aware GRPO"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/DiverseGRPO_Mitigating_Mode_Collapse_in_Image_Generation_via_Diversity_Aware_GRPO.pdf
project_link: null
code_link: null
aliases:
- DiverseGRPO
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 引入基于语义聚类的分布级创新奖励（小簇获得更高探索奖励）并将正则化集中施加于早期去噪步骤（结构感知Wasserstein约束），以重新平衡探索-利用并保护多样性关键期。
primary_logic: 模式坍缩并非奖励优化的必然结果，而是奖励设计（单样本评分缺乏分布视角）和正则化策略（忽略去噪动态的多样性预算失衡）失配的产物；通过将多样性建模为分布级奖励并根据去噪轨迹调整正则化预算，可以在不牺牲质量的条件下重建帕累托前沿。
claims:
- 早期去噪步骤对多样性影响最大：前三分之一去噪步骤贡献了约66%的多样性变化。
- 单样本奖励导致自强化收敛，复制动力学表明均衡时仅剩主导模式。
- 结合分布级创新奖励和结构感知正则化后，在多个骨干和奖励模型上实现13%～18%的语义多样性提升。
- 消融实验证实两个模块（SA-Reg + Creativity Reward）共同作用才能达到最优质量-多样性平衡。
---

# DiverseGRPO: Mitigating Mode Collapse in Image Generation via Diversity-Aware GRPO

> [!tip] 核心洞察
> 模式坍缩并非奖励优化的必然结果，而是奖励设计（单样本评分缺乏分布视角）和正则化策略（忽略去噪动态的多样性预算失衡）失配的产物；通过将多样性建模为分布级奖励并根据去噪轨迹调整正则化预算，可以在不牺牲质量的条件下重建帕累托前沿。

| 字段 | 内容 |
|------|------|
| 中文题名 | DiverseGRPO：通过多样性感知GRPO缓解图像生成中的模式坍缩 |
| 英文题名 | DiverseGRPO: Mitigating Mode Collapse in Image Generation via Diversity-Aware GRPO |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.21514) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | DiverseGRPO |
| Dataset | SD3.5-M / PickScore, Flux.1-dev / PickScore, SD3.5-M / HPSv3 |

> [!tip] 效果简介
> - SD3.5-M / PickScore 上，DreamSim ↑ 0.1517 vs 0.1278 (+18.8%)；FID ↓ 43.115 vs 56.206 (-23.3%)。
> - Flux.1-dev / PickScore 上，BeyondFID ↑ 0.1059 vs 0.0766 (+38.2%)。
> - SD3.5-M / HPSv3 上，DreamSim ↑ 0.1493 vs 0.1312 (+13.8%)。

## 概要

基于GRPO（Group Relative Policy Optimization）的奖励微调已成为提升文本到图像生成模型质量的主流范式。然而，标准GRPO存在一个关键瓶颈：**单一评分奖励与均匀KL正则化的组合导致模型过度收敛到高奖励模式，引发严重的模式坍缩**——模型倾向于生成高度相似的视觉内容（如相似的面部特征、构图和色彩），严重限制了其在创意场景中的适用性。

本文提出的**DiverseGRPO**方法，核心洞见在于：模式坍缩并非奖励优化的必然结果，而是奖励设计（单样本评分缺乏分布视角）与正则化策略（忽略去噪动态的多样性预算失衡）失配的产物。通过将多样性建模为分布级奖励并根据去噪轨迹调整正则化预算，可以在不牺牲质量的条件下重建帕累托前沿。

具体而言，DiverseGRPO引入两个关键机制：

- **分布级创意奖励（Distributional Creativity Bonus）**：通过对同一提示词生成的图像进行谱聚类，构建分布级语义表示，并为小簇图像分配更高的探索奖励，鼓励模型发现新颖的视觉模式。
- **结构感知正则化（Structure-Aware Regularization）**：仅在早期去噪步骤施加Wasserstein约束以保护多样性，后期释放正则化以专注奖励优化，从而合理分配多样性预算。

实验表明，DiverseGRPO在多个骨干模型（SD3.5-M、Flux.1-dev）和奖励模型（PickScore、HPSv3）上均取得显著提升：在匹配质量分数下，语义多样性提升13%～18%，FID指标降低约23%。消融实验证实，两个模块协同作用才能达到最优的质量-多样性平衡。



### 文本到图像生成中的奖励微调

以扩散模型和流匹配为基础的文本到图像生成模型在图像质量和文本对齐方面取得了显著进展。为进一步提升生成结果与人类偏好的契合度，研究者引入了基于人类反馈的强化学习（RLHF）和直接偏好优化（DPO）等对齐技术。其中，**Flow-GRPO**（Liu et al., arXiv 2025）将组相对策略优化（GRPO）适配到流匹配框架中，通过奖励模型对生成样本打分，利用组内标准化计算优势函数，并结合KL散度正则化约束策略更新，成为当前图像生成领域奖励微调的代表性基线方法。

### 模式坍缩：奖励优化的隐性代价

尽管GRPO类方法能有效提升生成图像的质量评分，但论文揭示了一个关键问题：**单一的质量奖励信号会驱动策略模型自强化收敛到少数高奖励模式，导致严重的模式坍缩**。具体而言，当仅使用PickScore等单样本质量评分作为奖励时，模型倾向于重复生成奖励最高的视觉模式（如相似的面部特征、相机角度、构图），而逐渐丧失生成多样样本的能力。

论文通过复制动力学（replicator dynamics）对这一现象进行了理论刻画。将条件生成分布分解为$K$个语义模式：

$$\tilde{\mu}_{\theta}(x \mid p) = \sum_{k=1}^{K} w_{k} \pi_{\theta}^{k}(x \mid p)$$

各模式权重的演化遵循：

$$\frac{d w_{k}}{d t} = w_{k} \left( \bar{r}_{k} - \mathbb{E}_{j} \left[ \bar{r}_{j} \right] \right)$$

其中$\bar{r}_{k} = \mathbb{E}_{x \sim \pi_{\theta}^{k}} [r(x, p)]$为模式$k$的平均奖励。该方程表明：高于平均奖励的模式权重持续增长，低于平均的模式权重指数衰减，**均衡状态下仅剩单一主导模式**——这正是模式坍缩的动力学本质。

### 正则化的多样性预算失配

另一个被忽视的关键因素是**标准KL正则化与去噪过程多样性动态之间的失配**。实验分析揭示了一个重要发现：**早期去噪步骤对生成多样性影响最大**——前三分之一的去噪步骤贡献了约66%的多样性变化（Fig. 2.b），而随着共享去噪步骤的增加，样本间的相似度急剧上升。然而，标准的Flow-GRPO将KL正则化均匀施加于所有去噪时间步，未考虑这一时间异质性。其后果是：在多样性最需要保护的早期阶段，正则化强度不足；而在后期对多样性影响微弱的阶段，正则化却消耗了同等的优化预算。这种**多样性预算的时空错配**进一步加速了模式灭绝。

### 核心洞察与动机

综上，模式坍缩并非奖励优化的必然结果，而是**奖励设计缺陷**（单样本评分缺乏分布级视角）与**正则化策略失配**（忽略去噪动态的多样性预算失衡）共同作用的产物。这引出了本文的核心动机：

- **从单点奖励到分布奖励**：需要构建能够感知生成分布整体结构的奖励信号，为探索新颖模式提供正向激励。
- **从均匀正则化到结构感知正则化**：需要根据去噪轨迹的多样性敏感度重新分配正则化预算，将约束集中施加于早期关键阶段。

基于这两点洞察，DiverseGRPO旨在通过分布级创新奖励和结构感知正则化的协同设计，在不牺牲生成质量的前提下重建质量-多样性的帕累托前沿。



## 核心方法与创新机理

DiverseGRPO 的核心创新在于识别并修复了标准 GRPO 训练中导致模式坍缩的两个结构性缺陷：**奖励信号的单样本短视**和**正则化策略的去噪动态失配**。方法通过两个相互协同的模块——分布级创新奖励（Distributional Creativity Bonus）和结构感知正则化（Structure-Aware Regularization）——在保持甚至提升图像质量的同时，将语义多样性提升了 13%～18%。

### 1. 从单样本奖励到分布级创新奖励

标准 GRPO（以 **Flow-GRPO**（Liu et al., arXiv 2025）为基线）仅使用单样本质量评分（如 PickScore）作为奖励信号。这种设计在复制动力学（replicator dynamics）框架下会导致自强化坍缩：高奖励模式不断扩张，低奖励模式被淘汰，最终生成分布退化为单一主导模式（见 Introduction 中的复制动力学方程）。其根本瓶颈在于，单样本奖励缺乏对**分布级多样性**的感知——模型不知道同一 prompt 下生成的图像是否覆盖了丰富的语义模式，只被驱动去最大化个体得分。

DiverseGRPO 将奖励信号从“单样本质量评分”替换为“质量评分 + 基于谱聚类的探索奖励”。具体而言，对于同一 prompt 生成的图像组，方法首先使用 DreamSim 感知距离构建高斯核亲和矩阵 $A_{ij} = \exp(-d_{ij}^2 / (2\sigma^2))$，通过谱聚类将图像划分为不同的语义簇。探索奖励 $E_i = \sqrt{N / n_k}$ 与图像所在簇的大小成反比：小簇（稀有的、新颖的视觉模式）获得更高的探索奖励，大簇（常见的、已被充分开发的模式）获得较低的奖励。最终奖励为 $R_i = Q_i + \beta \cdot E_i$，其中 $Q_i$ 为质量分数，$\beta$ 控制探索-利用的平衡。

这一设计的因果机制在于：通过将多样性建模为分布级的、反比于簇大小的奖励信号，模型被激励去发现和维护小众的视觉模式，而非仅仅追逐高奖励的常见模式。这从根本上改变了复制动力学的收敛方向，使得均衡状态下多个语义模式可以共存。

### 2. 从均匀正则化到结构感知正则化

标准 GRPO 对去噪过程的所有步骤施加均匀的 KL 散度正则化，以防止策略偏离参考模型过远。然而，DiverseGRPO 的关键洞察是：**早期去噪步骤对多样性影响最大**——实验表明，前三分之一去噪步骤贡献了约 66% 的多样性变化（Fig. 2.b），而标准正则化在此阶段恰恰最弱，导致多样性在训练早期即被不可逆地侵蚀。

DiverseGRPO 将正则化策略从“均匀 KL 散度施加于所有去噪步”替换为“结构感知 Wasserstein 约束仅施加于早期 K 步，后期完全移除”。具体而言，对于 $t \leq K$ 的步骤，施加 Wasserstein 距离约束 $\mathcal{L}_{\mathrm{reg}}(t) = \frac{\|\bar{\mathbf{x}}_{t+\Delta t,\theta} - \bar{\mathbf{x}}_{t+\Delta t,\mathrm{ref}}\|^2}{2}$；对于 $t > K$ 的步骤，正则化设为 0，使模型可以自由地优化奖励。

这一设计的因果机制在于：将有限的正则化预算集中投入到多样性保护的关键窗口期（早期去噪阶段），在结构形成时维持样本间的差异性；而在后期细节生成阶段释放约束，使奖励优化可以充分发挥作用。这种“前期保护、后期释放”的策略避免了均匀正则化“处处约束、处处不精”的困境，实现了质量-多样性帕累托前沿的重建。

### 3. 模块协同与证据强度

消融实验（Fig. 5(a)）证实，两个模块单独使用均无法达到最优效果：仅使用结构感知正则化可以减缓多样性下降但无法主动鼓励探索，仅使用创新奖励可以促进模式发现但缺乏对多样性关键期的保护。**SA-Reg + Creativity Reward 的组合**才能在质量和多样性两个维度上同时超越基线，实现帕累托改进。训练过程曲线（Fig. 6）进一步显示，DiverseGRPO 的多样性下降速度显著慢于基线，且质量保持相当，验证了方法在训练全程的稳定性。

**证据强度评估**：核心因果主张（早期步骤对多样性影响、复制动力学坍缩机制、双模块协同效果）均有实验锚点支撑（Fig. 2.b, Fig. 5(a), Fig. 6），置信度较高。超参数 $\beta$ 和 $K$ 的敏感性分析（Fig. 5(b-c)）显示边际收益在饱和后受限，但论文未提供自动化调参方案，这一点需要在实际应用中手动验证。

### 4. 方法谱系与知识库定位

DiverseGRPO 处于 **GRPO 微调图像生成模型** 的方法谱系中，与 Flow-GRPO（Liu et al., arXiv 2025）构成直接继承与改进关系。相较于其他缓解模式坍缩的方法（如增加噪声注入、温度调节、或使用多样性正则化项），DiverseGRPO 的独特之处在于：(1) 通过谱聚类将多样性显式建模为分布级奖励，而非隐式的正则化项；(2) 根据去噪轨迹动态调整正则化预算，而非静态施加约束。方法在多个骨干模型（SD3.5-M, Flux.1-dev）和奖励模型（PickScore, HPSv3）上验证了泛化性，但尚未扩展到文本或视频生成等多模态任务。



DiverseGRPO 在 Flow-GRPO（Liu et al., arXiv 2025）的基础上引入两个关键模块，构成一个两阶段的多样性保护训练流水线。其核心设计理念是：**模式坍缩并非奖励优化的必然结果，而是单样本奖励的分布盲区和均匀KL正则化对去噪动态的失配共同导致的**。因此，流水线从“奖励信号”和“正则化策略”两个维度同时介入，重新平衡探索-利用关系。

整体训练流程如下：

1. **采样与生成阶段**：对每个文本提示 $c$，从当前策略 $\pi_\theta$ 中采样一组 $G$ 张图像 $\{\mathbf{x}^i\}_{i=1}^G$。这些图像通过流匹配模型的多步去噪过程生成，早期去噪步（前三分之一步）贡献约 66% 的多样性变化（Fig. 2.b），是多样性保护的关键窗口。

2. **分布级创意奖励（Distributional Creativity Bonus）**：对同提示下的 $G$ 张图像计算感知距离矩阵，通过谱聚类将其划分为若干语义簇。每个图像的探索奖励与其所在簇的大小成反比——小簇（稀有的视觉模式）获得更高的奖励：$E_i = \sqrt{N / n_k}$。最终奖励由质量分数与加权探索奖励组合而成：$R_i = Q_i + \beta \cdot E_i$。这一设计将奖励信号从单样本质量视角提升到分布级多样性视角，打破高奖励模式的自强化循环（Figure 3.a, Section 3.2）。

3. **结构感知正则化（Structure-Aware Regularization, SA-Reg）**：针对早期去噪步对多样性影响最大这一发现，将正则化约束集中施加于前 $K$ 步。具体而言，前 $K$ 步使用 Wasserstein 距离约束 $\mathcal{L}_{\mathrm{reg}}(t) = \frac{\|\bar{\mathbf{x}}_{t+\Delta t,\theta} - \bar{\mathbf{x}}_{t+\Delta t,\mathrm{ref}}\|^2}{2}$ 保护多样性；后续步骤完全移除正则化，释放模型专注于奖励优化。这替代了标准 GRPO 中均匀施加于所有去噪步的 KL 散度正则化（Figure 3.b, Section 3.3）。

4. **策略更新**：基于组合奖励和阶段依赖的正则化损失，计算组级标准化优势函数，更新 LoRA 参数（rank $r=32$, $\alpha=64$, learning rate $3\times 10^{-4}$）。

两个模块的协同作用通过消融实验得到验证：单独使用任一模块均无法达到最优的质量-多样性帕累托前沿，只有 **SA-Reg + Creativity Reward** 的组合才能同时实现多样性提升和质量保持（Fig. 5(a)）。训练过程中，DiverseGRPO 的多样性下降速度显著慢于 Flow-GRPO 基线，且因探索奖励的存在，后期仍能持续生成稀有多样样本（Fig. 6, Fig. 7）。

### 补充图表

![[assets/figures/papers/paper_list_l2670_https_arxiv_org_abs_2512_21514/figures/001_Figure_1.jpg]]
*Figure 1: (a) Image generation models trained with GRPO suffer from mode collapse (similar faces, camera angles, etc.), which limits their applicability in creative scenarios. (b) The proposed DiverseGRPO method achieves higher diversity while maintaining comparable quality. (c) DiverseGRPO successfully maintains a healthier level of diversity across the entire duration of training, while the baseline method suffers from a premature collapse. (d) In the Inception feature space, DiverseGRPO generates images that cover a significantly broader range of semantic features, effectively mitigating mode collapse*



DiverseGRPO 在标准 Flow-GRPO 框架（Liu et al., arXiv 2025）的基础上，针对模式坍缩的两个根本原因——单样本奖励缺乏分布视角、均匀 KL 正则化忽视去噪动态——引入了两个关键模块：**分布级创新奖励（Distributional Creativity Bonus）** 和 **结构感知正则化（Structure-Aware Regularization）**。

### 3.1 Flow-GRPO 基础框架

在介绍核心模块之前，先回顾 Flow-GRPO 的策略优化目标。给定条件 $c \sim \mathcal{Q}$ 和从当前策略 $\pi_{\theta}$ 采样的 $G$ 个样本 $\{\mathbf{x}^{i}\}_{i=1}^{G}$，Flow-GRPO 的目标函数为：

$$\mathcal{T}_{\mathrm{Flow-GRPO}}(\theta) = \mathbb{E}_{c \sim \mathcal{Q}, \{\mathbf{x}^{i}\}_{i=1}^{G} \sim \pi_{\theta}} f(r, \hat{A}, \theta, \epsilon, \beta)$$

其中优势函数通过组级标准化计算：

$$\hat{A}_{t}^{i} = \frac{R(\mathbf{x}_{0}^{i}, c) - \mathrm{mean}(\{R(\mathbf{x}_{0}^{i}, c)\}_{i=1}^{G})}{\mathrm{std}(\{R(\mathbf{x}_{0}^{i}, c)\}_{i=1}^{G})}$$

**关键瓶颈**：该框架中奖励 $R$ 仅依赖单样本质量评分（如 PickScore），缺乏对同 prompt 下生成样本分布结构的考量。这直接导致复制动力学（replicator dynamics）下的模式灭绝——高奖励模式自我强化，低奖励模式被逐步淘汰：

$$\frac{d w_{k}}{d t} = w_{k} \left( \bar{r}_{k} - \mathbb{E}_{j} \left[ \bar{r}_{j} \right] \right)$$

其中 $w_k$ 为第 $k$ 个语义模式的权重，$\bar{r}_k = \mathbb{E}_{x \sim \pi_{\theta}^{k}} [r(x, p)]$ 为该模式的期望奖励。均衡时仅剩主导模式，多样性彻底丧失。

KL 散度在流匹配设定下的闭式解为：

$$D_{\mathrm{KL}}(\pi_{\theta} \| \pi_{\mathrm{ref}}) = \frac{\|\bar{\mathbf{x}}_{t+\Delta t,\theta} - \bar{\mathbf{x}}_{t+\Delta t,\mathrm{ref}}\|^{2}}{2\sigma_{t}^{2} \Delta t}$$

该正则化均匀施加于所有去噪步骤，但分析表明早期去噪阶段（前 1/3 步）贡献了约 66% 的多样性变化（Fig. 2.b），而标准正则化在此关键期最弱，无法有效保护多样性。

### 3.2 分布级创新奖励

该模块的核心思想是将奖励信号从单样本质量评分扩展为**质量评分 + 分布级探索奖励**，通过语义聚类识别新颖视觉模式并给予额外激励。

**步骤一：感知距离矩阵构建。** 对同一 prompt 生成的 $n$ 张图像，使用 DreamSim 计算两两感知距离，构建距离矩阵：

$$D = \begin{pmatrix} 0 & d_{12} & \cdots & d_{1n} \\ d_{21} & 0 & \cdots & d_{2n} \\ \vdots & \vdots & \ddots & \vdots \\ d_{n1} & d_{n2} & \cdots & 0 \end{pmatrix}$$

**步骤二：谱聚类。** 基于高斯核亲和矩阵进行谱聚类：

$$A_{ij} = \exp\left(-\frac{d_{ij}^{2}}{2\sigma^{2}}\right)$$

将 $n$ 张图像划分为若干语义簇，每个簇代表一种视觉模式。

**步骤三：探索奖励分配。** 探索奖励与图像所在簇的大小成反比——小簇（稀有模式）获得更高奖励，大簇（常见模式）获得较低奖励：

$$E_{i} = \sqrt{\frac{N}{n_{k}}}$$

其中 $N$ 为总样本数，$n_k$ 为图像 $i$ 所在簇的大小。最终奖励为质量分数与加权探索奖励之和：

$$R_{i} = Q_{i} + \beta \cdot E_{i}$$

其中 $Q_i$ 为原始质量评分（如 PickScore），$\beta$ 为创新奖励系数，控制探索-利用的平衡。消融实验表明 $\beta=3$ 时增益显著，$\beta=5$ 时边际收益趋于饱和（Fig. 5(b)）。

### 3.3 结构感知正则化（SA-Reg）

该模块针对均匀 KL 正则化在早期去噪阶段约束不足的问题，提出**分阶段正则化调度**：在多样性关键期施加更强约束，后期释放以专注奖励优化。

核心调度函数为：

$$\mathcal{L}_{\mathrm{reg}}(t) = \begin{cases} \frac{\|\bar{\mathbf{x}}_{t+\Delta t,\theta} - \bar{\mathbf{x}}_{t+\Delta t,\mathrm{ref}}\|^{2}}{2}, & t \leq K \\ 0, & t > K \end{cases}$$

其中 $K$ 为施加正则化的步数阈值。与标准 KL 散度正则化不同，SA-Reg 采用 Wasserstein 距离形式（直接 MSE 约束而非除以 $\sigma_t^2 \Delta t$），在早期去噪阶段提供更强的结构保持力。当 $t > K$ 时完全移除正则化，使模型在后期去噪步骤中自由优化奖励信号。

**设计依据**：Fig. 2.b 揭示早期去噪步骤对多样性影响最大——共享更多早期步骤会导致样本高度相似。SA-Reg 通过将正则化预算集中于此关键窗口，在保护多样性的同时避免后期过度约束损害质量优化。消融实验（Fig. 5(a)）证实，SA-Reg 与创新奖励共同作用才能达到最优质量-多样性帕累托前沿，单独使用任一模块均无法充分缓解模式坍缩。

### 模块协同机制

两个模块从不同维度解决模式坍缩问题：**创新奖励**通过分布级信号重新平衡探索-利用，防止模型过早收敛到少数高奖励模式；**SA-Reg** 通过时空调度保护多样性关键期，防止早期去噪阶段的模式灭绝。两者协同实现了在不牺牲质量前提下重建质量-多样性的帕累托前沿。

### 补充图表

![[assets/figures/papers/paper_list_l2670_https_arxiv_org_abs_2512_21514/figures/003_Figure_3.jpg]]
*Figure 3: DiverseGRPO employs two primary strategies to mitigate mode collapse: (a) A distributional creativity bonus mechanism based on semantic grouping. It begins by applying spectral clustering to images generated from the same caption, then assigns exploratory rewards according to cluster size to encourage the emergence of novel visual modes. (b) Structure-aware regularization imposes stronger constraints during the initial denoising stages to preserve sample diversity, while gradually relaxing the penalty in later stages to enhance the effectiveness of reward optimization*



## 实验与关键发现

### 主实验结果：跨骨干与奖励模型的多样性-质量协同提升

DiverseGRPO 的核心主张——在不牺牲生成质量的前提下显著缓解模式坍缩——在多个骨干模型和奖励函数组合下得到一致验证。Table 1 汇总了以 Flow-GRPO（Liu et al., arXiv 2025）为基线的定量对比结果。

![[assets/figures/papers/paper_list_l2670_https_arxiv_org_abs_2512_21514/figures/004_Table_1.jpg]]
*Table 1: Comparative evaluation of different backbone models and reward models. Higher values (↑) indicate better performance for DreamSim, BeyondFID(abbreviated as BFID), ImageReward(abbreviated as ImR), PickScore, and UnifiedReward(abbreviated as UniReward), while lower values (↓) are better for FID. The Improvement is calculated as*

**SD3.5-M + PickScore 配置下的表现：** 在语义多样性指标 DreamSim 上，DiverseGRPO 达到 0.1517，相较基线的 0.1278 提升 18.8%；同时，FID 从 56.206 降至 43.115，降幅达 23.3%，说明分布级多样性提升并未以保真度退化为代价。这一结果直接支持了核心洞察：模式坍缩并非奖励优化的必然产物，而是奖励设计失配的结果——当引入分布级创新奖励后，帕累托前沿得以重建。

**Flux.1-dev + PickScore 配置下的表现：** 在更大规模骨干模型上，DiverseGRPO 的优势更为突出。BeyondFID 从 0.0766 跃升至 0.1059（+38.2%），表明方法在更强基座模型上仍能有效拓展语义覆盖范围。值得注意的是，ImageReward 和 UnifiedReward 等质量指标也同步提升，验证了“探索奖励不会侵蚀质量”的设计假设。

**跨奖励模型的泛化性：** 当奖励模型从 PickScore 切换为 HPSv3 时，DiverseGRPO 在 SD3.5-M 上仍实现 DreamSim 13.8% 的提升（0.1312 → 0.1493），同时 ImageReward 从 0.5594 提升至 0.6445。这表明分布级创新奖励的设计不依赖于特定奖励函数的偏好结构，具有一定的通用性。

**公平性保障：** 所有实验采用相同的 LoRA 微调配置（rank r=32, α=64, lr=3×10⁻⁴）和奖励预算，排除了计算资源差异对结论的干扰。

### 消融实验：双模块协同是帕累托最优的必要条件

Figure 5(a) 的消融实验揭示了两个核心模块的独立贡献与协同效应：

![[assets/figures/papers/paper_list_l2670_https_arxiv_org_abs_2512_21514/figures/007_Figure_5.jpg]]
*Figure 5: Ablation study on the Pareto front of quality and diversity for different modules and parameters*

- **仅使用创造力奖励（Creativity Reward only）：** 多样性有所提升，但质量出现波动，因为缺乏对早期去噪阶段的约束保护，模型可能在探索过程中偏离合理生成空间。
- **仅使用结构感知正则化（SA-Reg only）：** 多样性得到一定保护，但缺乏主动探索激励，模型倾向于保守地停留在已有模式附近，多样性增益有限。
- **SA-Reg + Creativity Reward 联合使用：** 达到最优的质量-多样性平衡点，证实了两个模块的互补性——SA-Reg 在早期去噪阶段保护多样性“预算”，创造力奖励则为模型提供探索新颖模式的主动激励。这一发现与因果分析一致：正则化策略和奖励设计必须协同调整，才能纠正 GRPO 中多样性预算失衡的根本问题。

### 关键超参数分析

**创造力奖励系数 β（Figure 5b）：** β 增大可增强探索强度，但增益呈边际递减趋势。β=3 相比 β=1 带来显著的多样性提升，而 β=5 相比 β=3 的额外增益趋于饱和。这表明存在一个有效探索区间，过高的探索权重可能引入噪声而不再显著拓展语义覆盖。

**结构感知正则化步数 K（Figure 5c）：** 增加 SA-Reg 的施加步数 K 可提高多样性保护强度，但计算成本同步上升且边际收益递减。这一趋势与早期去噪阶段贡献约 66% 多样性变化的发现（Fig. 2.b）一致——在关键的前三分之一去噪步施加约束即可捕获大部分多样性保护效益，后续步的正则化贡献有限。

### 训练动态：多样性衰退的显著延缓

Figure 6 展示了训练过程中的质量与多样性演化轨迹。关键发现是：DiverseGRPO 在保持与基线相当的质量分数的同时，多样性下降速度显著更慢。基线方法的多样性在训练早期即出现快速衰退（“过早坍缩”），而 DiverseGRPO 在整个训练周期内维持了更健康的多样性水平。这一动态差异与复制动力学分析（Eq. 1）的预测一致：单样本奖励驱动下，高奖励模式的自强化增长会迅速压缩低奖励模式的生存空间；分布级创新奖励通过为小簇分配更高权重，有效减缓了这一灭绝过程。

![[assets/figures/papers/paper_list_l2670_https_arxiv_org_abs_2512_21514/figures/008_Figure_6.jpg]]
*Figure 6: During the training process, DiverseGRPO achieves quality scores comparable to baseline methods, but exhibits a significantly slower decline in diversity*

Figure 7 进一步提供了训练后期的样本可视化证据：由于创新奖励的存在，DiverseGRPO 在训练后期仍能生成稀有多样样本，而基线方法此时已难以挖掘出新颖视觉模式。

### 定性对比：模式坍缩的直观缓解

Figure 4 的定性对比展示了基线方法与 DiverseGRPO 在生成多样性上的直观差异。基线方法在主体特征（面部特征、姿态、字体颜色等）上出现明显的模式坍缩——同一提示下生成的图像高度相似。DiverseGRPO 则在保持图像质量与提示一致性的同时，实现了显著更高的主体多样性和创意变化。这一视觉证据与 DreamSim 和 BeyondFID 的定量提升相互印证。

![[assets/figures/papers/paper_list_l2670_https_arxiv_org_abs_2512_21514/figures/005_Figure_4.jpg]]
*Figure 4: Qualitative experiments on diversity, the baseline method exhibits mode collapse in the generation of main subjects (such as facial features, poses, font colors, etc.), whereas our method achieves greater diversity and creativity while maintaining image quality and consistency with the captions*

### 失败模式与局限性

尽管 DiverseGRPO 在实验范围内表现稳健，但以下局限值得注意：

1. **谱聚类计算开销：** 当每个提示的生成样本数较多时，亲和矩阵构建与谱聚类的计算成本不可忽视，可能影响大规模训练效率。论文未给出具体的额外时间开销数据，此点需在实际部署中验证。
2. **超参数敏感性：** β 和 K 需要针对具体骨干网络和奖励模型进行调整，且饱和后的边际收益受限。方法缺乏自动确定最优聚类簇数的机制，可能影响对不同提示复杂度的适应性。
3. **任务范围限制：** 当前验证仅限于图像生成的 GRPO 训练框架，尚未扩展到文本或视频等多模态生成任务。方法在更广泛生成场景中的有效性仍有待检验。

### 补充图表

![[assets/figures/papers/paper_list_l2670_https_arxiv_org_abs_2512_21514/figures/006_Figure.jpg]]
*Figure: (a) Contribution of each module (b) Creativity reward coefficient (c) Structure-aware regularization steps*

![[assets/figures/papers/paper_list_l2670_https_arxiv_org_abs_2512_21514/figures/002_Figure_2.jpg]]
*Figure 2: Analysis of the reasons for mode collapse: (Left) Policy model collapse into high-reward modes due to single sample reward modeling. (Right) Conventional regularization neglects the dominant role of early-stage denoising in preserving diversity*



## 定位与知识库关联

### 基线关系与差异化定位

DiverseGRPO 建立在 **Flow-GRPO**（Liu et al., arXiv 2025）的基础之上，后者是将 GRPO 应用于流匹配图像生成的开创性工作。Flow-GRPO 的核心框架包含两个关键组件：基于组级奖励标准化的优势函数计算（Eq. 3）和均匀施加于所有去噪步骤的 KL 散度正则化（Eq. 6）。该框架在质量优化上表现有效，但本文的分析揭示了其内在缺陷：单样本奖励建模导致复制动力学（Eq. 1）下低奖励模式被系统性淘汰，而均匀 KL 正则化在早期去噪阶段——多样性变化最剧烈的关键窗口（前三分之一步骤贡献约 66% 的多样性变化，Fig. 2.b）——约束力度不足，无法阻止模式灭绝。

DiverseGRPO 对 Flow-GRPO 的改造聚焦于两个可替换槽位：

**奖励信号槽位**：将 Flow-GRPO 的纯质量评分（如 PickScore）替换为“质量评分 + 探索奖励”的复合信号。探索奖励通过谱聚类对同 prompt 生成样本进行语义分组后，按簇大小的反比分配（$E_i = \sqrt{N/n_k}$，Eq. 11），使小簇获得更高奖励权重。这一设计在奖励层面引入了分布级视角，打破了单样本奖励的自强化循环。

**正则化策略槽位**：将 Flow-GRPO 的均匀 KL 散度约束替换为结构感知的 Wasserstein 约束（SA-Reg），仅在早期 $K$ 步施加 $\frac{\|\bar{\mathbf{x}}_{t+\Delta t,\theta} - \bar{\mathbf{x}}_{t+\Delta t,\mathrm{ref}}\|^2}{2}$，后期完全移除正则化（Eq. 14）。这一调度策略将有限的多样性预算集中投入于去噪轨迹中对多样性影响最大的阶段。

### 适用边界

DiverseGRPO 的验证范围覆盖了两种主流骨干模型（SD3.5-M 和 Flux.1-dev）以及两种不同偏好的奖励模型（PickScore 和 HPSv3），在多个多样性指标（DreamSim、BeyondFID、FID）上均表现出对 Flow-GRPO 的一致改善（Table 1）。实验采用统一的 LoRA 微调设置（rank $r=32$，scaling factor $\alpha=64$，学习率 $3\times10^{-4}$），确保了对比的公平性。

然而，该方法存在明确的适用边界：首先，谱聚类的计算开销在生成样本数较多时不可忽略，可能成为训练效率的瓶颈；其次，两个关键超参数——探索奖励系数 $\beta$ 和正则化步数 $K$——需要针对具体骨干网络和奖励模型进行调整，且消融实验（Fig. 5.b, Fig. 5.c）表明 $\beta$ 增大至 5 后增益趋于饱和，$K$ 增加也面临边际收益递减；最后，该方法目前仅在图像生成的 GRPO 训练框架下验证，尚未扩展到文本、视频等多模态生成任务。

### 局限与开放问题

**已知局限**：
1. 谱聚类的计算开销在批量生成较大时构成效率瓶颈，影响训练吞吐。
2. 超参数 $\beta$ 和 $K$ 缺乏自动确定机制，需针对不同骨干-奖励组合手动调整。
3. 方法仅在图像生成场景验证，跨模态泛化性未知。

**开放问题**：
1. 如何自动确定最优聚类簇数以适应不同提示的视觉模式数量？当前方法依赖预设参数，而不同 prompt 的语义模式数量天然存在差异。
2. 探索奖励能否与更精细的任务特定美学奖励（如风格一致性、构图质量）进一步集成，形成更全面的奖励信号？
3. 在大规模生产环境下，该方法对实时生成的延迟和资源消耗的实际影响如何？这决定了其从研究到部署的可迁移性。



## 原文 PDF

![[paperPDFs/CVPR_2026/DiverseGRPO_Mitigating_Mode_Collapse_in_Image_Generation_via_Diversity_Aware_GRPO.pdf]]
