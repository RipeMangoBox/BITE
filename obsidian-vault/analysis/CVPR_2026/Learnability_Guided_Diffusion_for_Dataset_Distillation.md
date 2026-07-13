---
title: Learnability-Guided Diffusion for Dataset Distillation
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Learnability_Guided_Diffusion_for_Dataset_Distillation.pdf
project_link: null
code_link: null
aliases:
- LGDL
- LGDDD
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 将蒸馏过程建模为增量式序列学习：以当前模型的可学习性为条件，引导扩散模型生成能填补模型知识缺口的互补样本，从而构建自适应的课程学习。
primary_logic: 通过将合成过程与学习者不断演变的状态对齐，每个增量批次都能提供非冗余、最大化边际学习收益的训练信号，从根本上减少冗余并显著提升样本效率。
claims:
- 对50 IPC蒸馏数据集按10 IPC增量划分，DiT和IGD的增量间交叉验证准确率高达98%和约80%，表明信息重叠严重；LGD的增量之间交叉准确率仅17%，证实互补性。
- 跨增量热力图显示，LGD的非对角线准确率显著低于DiT和IGD，增量间互补性更强。
- 与DiT相比，LGD将冗余降低了39.1%。
- LGD在ImageNet-1K (60.1%)、ImageNette (87.2%)、ImageWoof (72.9%)上取得最优或具有竞争力的结果。
---

# Learnability-Guided Diffusion for Dataset Distillation

> [!tip] 核心洞察
> 通过将合成过程与学习者不断演变的状态对齐，每个增量批次都能提供非冗余、最大化边际学习收益的训练信号，从根本上减少冗余并显著提升样本效率。

| 字段 | 内容 |
|------|------|
| 中文题名 | 可学习性引导的扩散模型用于数据集蒸馏 |
| 英文题名 | Learnability-Guided Diffusion for Dataset Distillation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Chan-Santiago_Learnability-Guided_Diffusion_for_Dataset_Distillation_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Learnability-Guided Diffusion (LGD) |
| Dataset | ImageNette, ImageWoof, ImageNet-1K |

> [!tip] 效果简介
> - ImageNette 上，Accuracy (ConvNet-6, IPC 100) 87.2±0.7 vs IGD: 84.5±0.7, DiT: 78.2±0.3 (+2.7 over IGD, +9.0 over DiT)。
> - ImageWoof 上，Accuracy (ResNet-18, IPC 100) 72.9±0.6 vs IGD: 70.6±1.8, DiT: 62.3±0.5 (+2.3 over IGD, +10.6 over DiT)。
> - ImageNet-1K 上，Top-1 Accuracy (ResNet-18, IPC 50) 60.1±0.1 vs IGD: 59.7±0.3 (reported in part_005) (+0.4 over IGD)。

## 概要

数据集蒸馏旨在将大规模数据集压缩为极少量高信息密度的合成样本，使下游模型仅用这些样本训练即可达到与全数据训练相近的性能。然而，当前主流蒸馏方法存在一个被忽视的根本瓶颈：**合成样本之间存在严重的信息冗余**。实验表明，将蒸馏数据集按10 IPC（每类图像数）划分为不相交的增量子集后，现有方法（如DiT、IGD）中，用前一个增量训练的模型对后一个增量评估的交叉验证准确率高达80–98%，这意味着不同增量传递了大量重叠的训练信号，多个样本在教模型同样的东西（见 Figure 1、Figure 2）。这种冗余源于现有范式在生成时仅追求视觉多样性或匹配平均训练轨迹，而忽视了不同样本间训练信号的互补性。

针对上述瓶颈，本文提出 **可学习性引导的扩散模型（Learnability-Guided Diffusion, LGD）**，核心思路是将数据集蒸馏重新建模为**增量式序列学习问题**：以当前模型的可学习性为条件，引导扩散模型生成能够填补模型知识缺口的互补样本，从而构建自适应的课程学习。具体而言，LGD 通过一个增量蒸馏循环（Figure 3），在每一阶段训练模型、评估其对候选样本的“可学习性分数”（当前模型损失与参考模型损失的差值），并以该分数的梯度调制扩散噪声，使生成过程偏向高可学习性区域，同时通过偏离引导增强类内多样性。这一机制使每个新增量都能提供非冗余、最大化边际学习收益的训练信号，从根本上减少冗余并提升样本效率。

实验验证了 LGD 的有效性：与 DiT 相比，LGD 将冗余降低了 **39.1%**；在 ImageNet-1K 上取得 **60.1%** 的 Top-1 准确率（ResNet-18, IPC 50），在 ImageNette 和 ImageWoof 上分别达到 **87.2%** 和 **72.9%**（ConvNet-6/ResNet-18, IPC 100），均达到最优或具有竞争力的水平（Table 1、Table 2）。增量训练动态分析（Figure 4）进一步证实，LGD 的每个增量都能持续带来显著的损失尖峰和准确率增益，而基线方法的增益随阶段增加迅速衰减，从实证层面验证了互补性机制的有效性。

### 数据集蒸馏的核心目标

现代深度学习依赖海量标注数据，但存储、传输和训练这些数据成本高昂。数据集蒸馏（Dataset Distillation）试图将大规模数据集压缩为极少量合成样本，使在此合成集上训练的模型，其性能能逼近在全量数据上训练的结果。其核心优化目标可形式化为：

$$ \underset { \mathcal { D } } { \mathop { \operatorname* { m i n } } } \left| \left| \mathbb { E } _ { \boldsymbol { x } \sim P _ { \mathrm { d a t a } } } \big [ \ell ( \theta _ { \mathcal { T } } ( \boldsymbol { x } ) , \boldsymbol { y } ) \big ] - \mathbb { E } _ { \boldsymbol { x } \sim P _ { \mathrm { d a t a } } } \big [ \ell ( \theta _ { \mathcal { D } } ( \boldsymbol { x } ) , \boldsymbol { y } ) \big ] \right| \right| $$

即最小化在全数据集 $\mathcal{T}$ 与蒸馏数据集 $\mathcal{D}$ 上分别训练所得模型之间的期望损失差异。理想情况下，每张合成样本应承载独特且非冗余的训练信号，使得在极低 IPC（Images Per Class）预算下也能实现高效学习。

### 现有方法的隐性冗余困境

近年来，基于扩散模型的蒸馏方法取得了显著进展。**DiT**（Peebles & Xie, ICCV 2023）利用预训练扩散模型统一采样生成合成数据；**IGD**（Chen et al., ICLR 2025）通过匹配训练梯度引导扩散过程；**MGD³**（Chan-Santiago et al., ICML 2025）在特征空间进行模式引导；**Minimax Diffusion**（Gu et al., CVPR 2024）则试图平衡多样性与代表性。这些方法在多个基准上不断刷新记录，但它们的共同盲点在于：**生成过程忽视不同样本间训练信号的互补性**。

本文通过增量式信息重叠分析揭示了一个关键事实：将现有方法蒸馏得到的 50 IPC 数据集按 10 IPC 划分为不相交的增量后，**不相交的子集之间竟能捕获 80–90% 的重叠训练信号**。例如，在 DiT 蒸馏的数据集上，用第一个增量（$\mathcal{I}_0$）训练的模型对第二个增量（$\mathcal{T}_1$）的分类准确率高达 98.0%，这意味着 $\mathcal{T}_1$ 几乎没有引入任何新信息——模型早已“学会”了这些样本所承载的内容。类似地，IGD 的跨增量交叉验证准确率也维持在约 80% 的高位。

这揭示出当前范式的深层瓶颈：**现有工作追求视觉多样性或匹配平均训练轨迹，却未能从“模型当前知道什么、还不知道什么”的角度来规划合成内容**，导致多个样本传递重复信息，严重稀释了有限 IPC 预算的信息密度。

### 本文动机：从冗余到互补

上述发现指向一个根本性的范式转换：数据集蒸馏不应是一次性的静态生成，而应是一个**与学习者状态协同演化的增量过程**。本文提出 **Learnability-Guided Diffusion（LGD）**，核心思路是将蒸馏建模为增量式序列学习——以当前模型的可学习性为条件，引导扩散模型生成能填补模型知识缺口的互补样本，从而构建自适应的课程学习。

在 LGD 框架下，同样的增量划分实验中，用 $\mathcal{I}_0$ 训练的模型对 $\mathcal{T}_1$ 的准确率骤降至仅 17.0%，证实了增量间的高度互补性。通过将合成过程与学习者不断演变的状态对齐，每个增量批次都能提供非冗余、最大化边际学习收益的训练信号，从根本上减少冗余并显著提升样本效率。

## 核心方法与创新机理

### 从冗余到互补：范式转换

现有数据集蒸馏方法存在一个被忽视的结构性缺陷——**合成样本之间存在严重的训练信号冗余**。实验揭示，将 DiT 蒸馏的 50 IPC 数据集划分为 5 个 10 IPC 的增量，用第一个增量训练的模型评估第二个增量时，交叉验证准确率竟高达 **98.0%**（Figure 1），这意味着后一个增量几乎没有提供新的学习信号。IGD 的情况稍好但仍达约 80%。这一发现直指当前范式的根本问题：无论是追求视觉多样性还是匹配平均训练轨迹，都无法保证不同样本传递的训练信号是互补的。

**LGD** 的核心创新在于将数据集蒸馏从“一次性生成”转变为 **“增量式互补构建”**——以模型当前的知识状态为条件，引导生成过程填补模型的“可学习缺口”，使每个新加入的增量批次都能带来非冗余、最大化的边际学习收益。

### 三个关键机制（Changed Slots）

#### 1. 合成范式：从一次性生成到增量式课程学习

**Baseline**：一次性生成所有合成样本，或独立生成各增量，不考虑模型训练过程中的状态演变。

**LGD**：将蒸馏建模为增量式序列学习问题。设第 $i$ 阶段的累积数据集为 $\mathcal{D}_i = \bigcup_{k=1}^{i} \mathcal{T}_k$，在 $\mathcal{D}_{i-1}$ 上训练得到模型 $\theta_{i-1}$ 后，以 $\theta_{i-1}$ 的状态为条件生成下一个增量 $\mathcal{T}_i$。这一设计使得每个增量都能“感知”模型已经学会了什么，从而有针对性地补充知识缺口。实验表明，LGD 的增量间交叉准确率仅 **17.0%**（Figure 1），证实了互补性；跨增量热力图（Figure 2）进一步显示 LGD 的非对角线得分显著低于 DiT 和 IGD，增量间信息重叠最小。

#### 2. 生成引导信号：从分类器引导到可学习性引导

**Baseline**：分类器引导（classifier guidance）或影响力引导，基于全数据集的平均梯度，无法区分样本对当前模型的信息价值。

**LGD**：引入**可学习性分数（Learnability Score）**作为生成引导信号：

$$\mathcal{S}(x, y) = \mathcal{L}(\theta_{i-1}, x, y) - \omega \cdot \mathcal{L}(\theta^*, x, y)$$

其中 $\theta_{i-1}$ 是当前阶段模型，$\theta^*$ 是在全数据集上预训练的参考模型。第一项 $\mathcal{L}(\theta_{i-1}, x, y)$ 衡量样本对当前模型的难度——损失越高，说明模型越不会；第二项 $\mathcal{L}(\theta^*, x, y)$ 作为正则化项，惩罚参考模型也难以分类的样本，防止生成过程漂移到分布外区域。两者之差精准定位了“当前模型不会、但参考模型会”的可学习区域。

该分数通过梯度调制扩散模型的噪声预测过程：

$$\tilde{\epsilon}_{\phi}(x_t, t, y) = \epsilon_{\phi}(x_t, t, y) + \lambda \cdot \rho_t \cdot \nabla_{x_t} \mathcal{S}(x_t, y)$$

其中 $\rho_t = \sqrt{1 - \bar{\alpha}_t} \frac{\|\epsilon_{\phi}(x_t, t, y)\|}{\|\nabla_{x_t} \mathcal{S}(x_t, y)\|}$ 是时间步依赖的缩放因子，用于保持梯度幅度与噪声水平一致。消融实验（Figure 6）证实，移除正则化项 $\mathcal{L}(\theta^*, x, y)$ 会导致生成低置信度的分布外样本，而完整 LGD 产生的是分布内的困难样本。

#### 3. 多样性机制：从无显式约束到偏离引导

**Baseline**：无显式类内多样性约束，合成样本容易聚集在相似模式上。

**LGD**：引入**偏离引导（Deviation Guidance）**，利用记忆缓冲区中最近样本的余弦相似度推动生成远离已有样本：

$$\mathcal{G}_D(\boldsymbol{x}) = \frac{\boldsymbol{x} \cdot \tilde{\boldsymbol{x}}^*}{\|\boldsymbol{x}\| \|\tilde{\boldsymbol{x}}^*\|}$$

在逆扩散过程中，从预测噪声中减去 $\gamma \nabla_{x_t} \mathcal{G}_D(x_t)$，使生成过程主动避开已存在的样本模式。这一机制与可学习性引导形成互补：前者保证每个样本的信息价值，后者保证样本之间的多样性。

### 创新效果：冗余的量化削减

增量训练动态（Figure 4）直观展示了 LGD 的优势：每个新加入的增量都能带来显著的损失尖峰和持续的准确率增益（+12.0%, +3.2%, +5.4%, +6.4%），而 DiT 的增益随阶段快速衰减（+7.2%, +4.8%, +2.2%, +0.4%）。整体上，LGD 将冗余降低了 **39.1%**，并在 ImageNet-1K（60.1%）、ImageNette（87.2%）、ImageWoof（72.9%）上取得最优或具有竞争力的结果。

LGD 将数据集蒸馏重新定义为**增量式序列学习问题**，其核心 pipeline 由四个模块构成一个闭环迭代过程，如 Figure 3 所示。

![[assets/figures/papers/paper_list_l2689_https_openaccess_thecvf_com_content_CVPR2026_html_Chan_Santiago_Learnabi/figures/003_Figure_3.jpg]]
*Figure 3: Overview of our learnability-guided iterative generation framework. (Top) Incremental distillation loop: we iteratively train model*

### 增量蒸馏循环

整个框架围绕一个外层循环展开：在第 i 个阶段，模型 θᵢ₋₁ 在累积数据集 𝒟ᵢ₋₁ 上完成训练后，系统进入生成-选择-扩充的迭代。累积数据集按公式 (4) 定义：

$$\mathcal{D}_i = \bigcup_{k=1}^{i} \mathcal{T}_k$$

即每个阶段将前 i 个增量合并。循环的驱动力来自一个关键洞察：当前模型的可学习性状态决定了下一步需要什么样的训练信号。因此，每个增量 𝒯ᵢ 的生成都以 θᵢ₋₁ 为条件，目标是最大化模型从该增量中获得的边际学习收益。

### 模块关系与数据流

**① 数据种子初始化**：循环需要一个起点。LGD 默认使用 **IGD**（Chen et al., ICLR 2025）预先蒸馏的 10 IPC 图像作为初始数据集 𝒟₀，以加速收敛。消融实验（见补充材料）表明方法对不同种子选择具有鲁棒性。

**② 可学习性引导扩散采样**：这是框架的核心生成模块。给定当前模型 θᵢ₋₁ 和参考模型 θ*（在全数据集上预训练），对每个目标类别 y，扩散模型从随机噪声 x_T 开始逐步去噪。在每个去噪步 t，计算可学习性分数：

$$\mathcal{S}(x_t, y) = \mathcal{L}(\theta_{i-1}, x_t, y) - \omega \cdot \mathcal{L}(\theta^*, x_t, y)$$

该分数度量样本对当前模型的"信息缺口"：高 S 意味着当前模型难以分类（高 ℒ(θᵢ₋₁)），但参考模型能够识别（低 ℒ(θ*)），即样本处于可学习间隙内。随后，用该分数的梯度调制扩散噪声预测：

$$\tilde{\epsilon}_{\phi}(x_t, t, y) = \epsilon_{\phi}(x_t, t, y) + \lambda \cdot \rho_t \cdot \nabla_{x_t} S(x_t, y)$$

其中 $\rho_t = \sqrt{1 - \bar{\alpha}_t} \frac{\|\epsilon_{\phi}(x_t, t, y)\|}{\|\nabla_{x_t} S(x_t, y)\|}$ 是时间步依赖的缩放因子，用于保持梯度幅度与当前噪声水平一致。这一引导机制将生成过程推向高可学习性区域，如 Figure 3（Bottom）所示，生成样本落在当前模型边界与参考模型边界之间的可学习间隙。

同时，为增强类内多样性，LGD 引入**偏离引导**：维护一个记忆缓冲区存储最近生成的样本，对当前生成样本计算与缓冲区中最相近样本的余弦相似度：

$$\mathcal{G}_D(\boldsymbol{x}) = \frac{\boldsymbol{x} \cdot \tilde{\boldsymbol{x}}^*}{\|\boldsymbol{x}\| \|\tilde{\boldsymbol{x}}^*\|}$$

并从预测噪声中减去 $\gamma \nabla_{x_t} \mathcal{G}_D(x_t)$，推动生成远离已有样本。

**③ 可学习性样本选择**：对每个数据集位置，生成 κ 个候选样本，按公式 (7) 的可学习性分数排序，保留最高分候选加入记忆缓冲区。这一筛选机制确保只有真正填补知识缺口的样本被纳入数据集。

**④ 数据集扩充与模型更新**：新选出的样本构成增量 𝒯ᵢ，合并入累积数据集 𝒟ᵢ = 𝒟ᵢ₋₁ ∪ 𝒯ᵢ。随后在 𝒟ᵢ 上训练模型得到 θᵢ，进入下一轮迭代。

### 输入输出流总结

- **输入**：预训练扩散模型（DiT）、全数据集上预训练的参考模型 θ*、初始种子数据集（默认 IGD 10 IPC）
- **每阶段输出**：增量 𝒯ᵢ（包含该阶段新合成的样本）、更新后的累积数据集 𝒟ᵢ、更新后的模型 θᵢ
- **最终输出**：完整蒸馏数据集 𝒟_K（含 K 个增量），可直接用于下游模型训练

整个框架的关键设计在于**以学习者状态为条件的自适应生成**，使得每个增量批次都能提供非冗余的训练信号。Figure 4 的训练动态验证了这一机制的有效性：LGD 的每个增量加入时都产生显著的损失尖峰和持续的准确率增益，而 DiT 的增益随阶段快速衰减。

### 问题建模：增量式数据集蒸馏

传统数据集蒸馏的目标是最小化全数据集与蒸馏数据集训练模型之间的期望损失差异：

$$
\underset{\mathcal{D}}{\operatorname{min}} \left| \left| \mathbb{E}_{\boldsymbol{x} \sim P_{\mathrm{data}}} \big[ \ell(\theta_{\mathcal{T}}(\boldsymbol{x}), \boldsymbol{y}) \big] - \mathbb{E}_{\boldsymbol{x} \sim P_{\mathrm{data}}} \big[ \ell(\theta_{\mathcal{D}}(\boldsymbol{x}), \boldsymbol{y}) \big] \right| \right|
$$

其中 $\theta_{\mathcal{T}}$ 和 $\theta_{\mathcal{D}}$ 分别表示在全数据集 $\mathcal{T}$ 和蒸馏数据集 $\mathcal{D}$ 上训练的模型参数。

LGD 将蒸馏过程重新建模为**增量式序列学习问题**：将蒸馏数据集 $\mathcal{D}_S$ 划分为 $K$ 个不相交的增量 $\{\mathcal{T}_1, \mathcal{T}_2, \ldots, \mathcal{T}_K\}$，第 $i$ 阶段的累积数据集为：

$$
\mathcal{D}_i = \bigcup_{k=1}^{i} \mathcal{T}_k
$$

在每个阶段，先在 $\mathcal{D}_{i-1}$ 上训练得到模型 $\theta_{i-1}$，然后以 $\theta_{i-1}$ 的状态为条件生成下一个增量 $\mathcal{T}_i$。核心直觉在于：$\mathcal{T}_i$ 应最大化当前模型的可学习信号，即选择使 $\theta_{i-1}$ 损失最大的样本：

$$
\mathcal{T}_i^{\ast} = \arg \max_{\mathcal{T}} \mathcal{L}(\theta_{i-1}, \mathcal{T})
$$

然而，单纯最大化损失会导致生成分布外（out-of-distribution）样本。为此，引入参考模型 $\theta^{\ast}$（在全数据集上预训练）作为正则项，约束样本必须语义有效：

$$
\mathcal{T}_i^{\ast} = \arg \max_{\mathcal{T}} \big[ \mathcal{L}(\theta_{i-1}, \mathcal{T}) - \mathcal{L}(\theta^{\ast}, \mathcal{T}) \big]
$$

该目标函数同时追求两个目标：当前模型难以分类（高 $\mathcal{L}(\theta_{i-1})$），但参考模型能够正确识别（低 $\mathcal{L}(\theta^{\ast})$），从而确保生成的样本位于“可学习间隙”内。

### 核心模块一：可学习性引导扩散采样

LGD 的核心创新在于将上述增量优化目标嵌入扩散模型的生成过程。扩散模型的逆过程通过预测噪声 $\epsilon_{\phi}(x_t, t)$ 来逐步去噪：

$$
\mu_{\phi}(x_t) = \frac{1}{\sqrt{1 - \beta_t}} \left( x_t - \frac{\beta_t}{\sqrt{1 - \bar{\alpha}_t}} \epsilon_{\phi}(x_t, t) \right)
$$

传统分类器引导通过类别梯度调制噪声：

$$
\tilde{\epsilon}_{\phi}(x_t, t, c) = \epsilon_{\phi}(x_t, t, c) + \lambda \nabla_{x_t} \log p(c | x_t)
$$

LGD 将其中的类别梯度替换为**可学习性分数**的梯度。对于样本 $(x, y)$，可学习性分数定义为：

$$
\mathcal{S}(x, y) = \mathcal{L}(\theta_{i-1}, x, y) - \omega \cdot \mathcal{L}(\theta^*, x, y)
$$

其中 $\omega$ 是平衡当前模型损失与参考模型损失的超参数。高 $\mathcal{S}$ 值表示该样本对当前模型具有高信息量且语义正确。将可学习性梯度注入扩散噪声预测：

$$
\tilde{\epsilon}_{\phi}(x_t, t, y) = \epsilon_{\phi}(x_t, t, y) + \lambda \cdot \rho_t \cdot \nabla_{x_t} \mathcal{S}(x_t, y)
$$

其中 $\lambda$ 为引导强度，$\rho_t$ 为时间步依赖的缩放因子，用于保持梯度幅度与当前噪声水平一致：

$$
\rho_t = \sqrt{1 - \bar{\alpha}_t} \frac{\|\epsilon_{\phi}(x_t, t, y)\|}{\|\nabla_{x_t} \mathcal{S}(x_t, y)\|}
$$

这一机制使得扩散过程被动态引导至高可学习性区域，每个生成步骤都朝着填补当前模型知识缺口的方向推进。

### 核心模块二：偏离引导

为增强类内多样性，LGD 引入**偏离引导**机制。维护一个记忆缓冲区，存储当前增量中已生成样本。对于正在生成的样本 $x_t$，计算其与缓冲区中最相近样本 $\tilde{\boldsymbol{x}}^*$ 的余弦相似度：

$$
\mathcal{G}_D(\boldsymbol{x}) = \frac{\boldsymbol{x} \cdot \tilde{\boldsymbol{x}}^*}{\|\boldsymbol{x}\| \|\tilde{\boldsymbol{x}}^*\|}
$$

在逆扩散过程中，从预测噪声中减去该相似度的梯度，推动生成远离已有样本：

$$
\tilde{\epsilon}_{\phi} \leftarrow \tilde{\epsilon}_{\phi} - \gamma \nabla_{x_t} \mathcal{G}_D(x_t)
$$

其中 $\gamma$ 控制偏离强度。该模块与可学习性引导协同工作：前者保证样本的信息增益，后者防止样本在特征空间聚集。

### 核心模块三：增量蒸馏循环

整体流程（Figure 3）由以下步骤循环构成：

1. **数据种子初始化**：默认使用 IGD（Chen et al., ICLR 2025）预蒸馏的 10 IPC 图像作为初始数据集 $\mathcal{D}_0$，加速收敛。
2. **模型训练**：在累积数据集 $\mathcal{D}_{i-1}$ 上训练模型 $\theta_{i-1}$。
3. **可学习性引导生成**：以 $\theta_{i-1}$ 和参考模型 $\theta^*$ 为条件，通过可学习性引导扩散采样生成候选样本。
4. **可学习性样本选择**：为每个目标位置生成 $\kappa$ 个候选样本，按 $\mathcal{S}(x, y)$ 排序，保留最高分样本加入增量 $\mathcal{T}_i$，同时更新记忆缓冲区。
5. **数据集扩充**：$\mathcal{D}_i = \mathcal{D}_{i-1} \cup \mathcal{T}_i$，进入下一轮迭代。

### 关键设计要点

- **参考模型的正则化作用**：消融实验（Figure 6）证实，移除 $\mathcal{L}(\theta^*, x, y)$ 项（即仅使用 DiT+Loss）会导致生成低置信度、分布外样本。该正则项确保生成的困难样本仍属于原始数据分布。
- **增量间的互补性**：跨增量验证实验（Figure 2）显示，LGD 的非对角线准确率显著低于 DiT 和 IGD，表明各增量传递的训练信号高度互补，而非简单重复。
- **初始化鲁棒性**：消融实验（见补充材料）表明，不同种子数据集（如随机种子或其他蒸馏方法）对最终性能影响有限，方法对初始化具有鲁棒性。

![[assets/figures/papers/paper_list_l2689_https_openaccess_thecvf_com_content_CVPR2026_html_Chan_Santiago_Learnabi/figures/002_Figure_2.jpg]]
*Figure 2: Cross-validation across distilled data increments*

## 实验与关键发现

### 核心实验设置

实验在三个基准上评估 LGD：**ImageNette**（10 类）、**ImageWoof**（10 类）和 **ImageNet-1K**（1000 类）。默认设置下，LGD 以 **IGD**（Chen et al., ICLR 2025）在 10 IPC 下预蒸馏的图像作为数据种子，随后通过增量蒸馏循环逐步将每类样本数扩展至目标 IPC。扩散骨干网络采用预训练的 **DiT**（Peebles & Xie, ICCV 2023），参考模型为在全数据集上训练的 ConvNet-6。主要评估协议包括：在同架构（ConvNet-6、ResNetAP-10、ResNet-18）上训练与测试，以及跨架构泛化测试。所有结果均报告均值±标准差。

### 主对比结果

**ImageNette 与 ImageWoof。** Table 1 给出了不同 IPC 预算和网络架构下的准确率对比。在 ImageNette 上，LGD 在 ConvNet-6 架构下以 100 IPC 达到 **87.2±0.7%**，较 IGD（84.5±0.7%）提升 2.7 个百分点，较 DiT（78.2±0.3%）提升 9.0 个百分点。在 ResNetAP-10 架构下，50 IPC 时 LGD 达到 84.3±0.5%，同样显著优于 IGD（82.5±0.5%）和 DiT（73.6±0.5%）。在 ImageWoof 上，LGD 在 ResNet-18 架构下以 100 IPC 达到 **72.9±0.6%**，较 IGD（70.6±1.8%）提升 2.3 个百分点，较 DiT（62.3±0.5%）提升 10.6 个百分点。值得注意的是，LGD 在所有 IPC 级别和架构组合下均保持最优或次优，尤其在低 IPC 场景下优势更为突出。

**ImageNet-1K。** Table 2 展示了在 ImageNet-1K 上使用 ResNet-18 的 Top-1 准确率。LGD 在 50 IPC 下达到 **60.1±0.1%**，略优于 IGD（59.7±0.3%），且显著超越其他非扩散蒸馏方法（如 DM、IDC-1 等）。这一结果表明，可学习性引导策略在大规模类别场景下仍能有效运作，尽管增益幅度相比小规模子集有所收窄。

### 冗余性分析：核心瓶颈验证

LGD 的核心动机在于现有蒸馏方法存在严重信息冗余。为量化这一现象，实验将 50 IPC 的蒸馏数据集划分为 5 个互不相交的 10 IPC 增量，并执行交叉验证：在一个增量上训练模型，在另一个增量上评估。

**Figure 1（底部）** 的对比极具说服力：在 DiT 框架下，使用增量 $\mathcal{I}_0$ 训练的模型在增量 $\mathcal{T}_1$ 上达到 **98.0%** 的准确率，表明 $\mathcal{T}_1$ 几乎未引入任何新信息。相比之下，LGD 生成的 $\mathcal{T}_1$ 在同一先验模型下仅获得 **17.0%** 的准确率，证实其包含了大量互补性知识。

**Figure 2** 的热力图进一步揭示了跨增量的信息重叠模式。DiT 和 IGD 的非对角线准确率普遍较高（热力图中呈现大面积暖色区域），说明不同增量间传递了大量重复信号。LGD 的非对角线得分显著降低，热力图呈现更清晰的块对角结构，表明各增量间互补性更强。定量而言，论文报告 LGD 将冗余降低了 **39.1%**（相对于 DiT）。

### 增量训练动态

**Figure 4** 追踪了逐增量加入时的训练损失和验证准确率变化。DiT 的损失曲线显示，随着增量增加，每个新阶段带来的损失尖峰逐渐衰减（+7.2%, +4.8%, +2.2%, +0.4%），表明后期增量提供的边际学习信号递减。LGD 则持续产生显著的损失尖峰和准确的准确率增益（+12.0%, +3.2%, +5.4%, +6.4%），验证了可学习性引导能持续生成填补模型知识缺口的样本。

**Table 4** 从 IPC 累加角度展示了准确率演进。在 ImageNette 上，从 10 IPC 累加到 100 IPC 的过程中，LGD 在每个 IPC 级别均保持对 IGD 和 DiT 的领先，最终达到 89.1±0.7%（100 IPC），而 IGD 为 84.5±0.7%，DiT 仅为 78.2±0.3%。

### 学习动态可视化

**Figure 5** 将每个样本在 50 轮训练过程中的真实类别概率均值（μ）和标准差（σ²）绘制为散点图。左上角为简单样本（高 μ、低 σ²），左下角为困难样本，中间偏右区域为信息量丰富的样本。LGD 合成的样本分布更接近原始数据的学习动态特征，其信息量（16.2%）和难度（2.6%）分别约为 IGD 的 3 倍和 2 倍，且与原始数据分布的 Jensen-Shannon 散度最低。

### 消融实验

**可学习性正则项的关键作用。** **Figure 6** 以参考模型置信度为 x 轴、训练难度为 y 轴，分析了各方法合成样本的分布内程度。DiT 集中于高置信度的简单样本；DiT+IGD 略有向中等难度区域扩展；移除可学习性正则项 $\mathcal{L}(\theta^*, x, y)$ 后的变体（DiT+Loss）覆盖了更广的难度范围，但同时引入了多个低置信度（低 x 值）的分布外样本。完整的 LGD（DiT+Ours）在保持与分布内区域紧密对齐的同时，成功捕获了信息量丰富的中等和困难样本。这一消融证实了正则项 $\mathcal{L}(\theta^*, x, y)$ 是防止生成过程漂移出分布的关键机制。

**偏离引导的贡献。** 偏离引导（deviation guidance）通过惩罚与记忆缓冲区中已有样本的余弦相似度，推动生成多样性。论文报告该机制进一步降低了类内冗余，但具体定量消融数据置于补充材料中，需要手动验证。

**种子数据集的鲁棒性。** 论文声称对不同种子选择（如随机种子或其他蒸馏方法）进行了消融实验，结果表明方法对初始化具有鲁棒性，但具体数据同样置于补充材料，需要手动验证。

### 跨架构泛化

**Table 3** 展示了在 ImageNette 上的跨架构评估结果。使用一种代理架构蒸馏的数据集，在多种目标架构（ConvNet-6、ResNetAP-10、ResNet-18、VGG-11、AlexNet）上进行评估。LGD 在所有代理-目标组合下均表现优异，表明可学习性引导生成的样本具有良好的架构泛化能力，不会过度拟合特定代理模型的归纳偏置。

### 失败模式与局限性

1. **计算开销。** LGD 依赖预训练扩散模型和全数据集训练的参考模型，且增量式训练过程为串行执行，计算成本高于一次性生成方法。
2. **大规模扩展性未验证。** 实验主要集中于 10 类子集和 ImageNet-1K，未在更多类别或更高分辨率场景（如 ImageNet-21K）上进行验证。
3. **代理分类器域差异。** 可学习性引导依赖代理分类器的梯度信号，若代理分类器与扩散模型存在域差异，可能影响生成质量。论文未对此进行系统分析。
4. **超参数敏感性缺失。** 关键超参数（如可学习性权重 ω、引导强度 λ、偏离引导强度 γ）的敏感性分析置于补充材料，公开版本中缺少可直接引用的定量结论。

### 补充图表

![[assets/figures/papers/paper_list_l2689_https_openaccess_thecvf_com_content_CVPR2026_html_Chan_Santiago_Learnabi/figures/004_Table_1.jpg]]
*Table 1: Comparison across distilled IPC budgets on Nette and Woof evaluated on different network architectures. Mean±std accuracy; best per row in bold. IGD, MGD3, and LGD used a pretrained DiT as the diffusion backbone*

![[assets/figures/papers/paper_list_l2689_https_openaccess_thecvf_com_content_CVPR2026_html_Chan_Santiago_Learnabi/figures/007_Table_2.jpg]]
*Table 2: ImageNet-1K: Performance comparison over ResNet-18 with state-of-the-art dataset distillation methods*

![[assets/figures/papers/paper_list_l2689_https_openaccess_thecvf_com_content_CVPR2026_html_Chan_Santiago_Learnabi/figures/005_Figure_4.jpg]]
*Figure 4: Incremental training dynamics of DiT and our method. (a-b) show the training loss across successive data increments*

![[assets/figures/papers/paper_list_l2689_https_openaccess_thecvf_com_content_CVPR2026_html_Chan_Santiago_Learnabi/figures/008_Table_3.jpg]]
*Table 3: Cross-Architecture Evaluation on ImageNette*

![[assets/figures/papers/paper_list_l2689_https_openaccess_thecvf_com_content_CVPR2026_html_Chan_Santiago_Learnabi/figures/006_Figure_5.jpg]]
*Figure 5: Learning-dynamics visualization of original and distilled samples. Each point shows a sample’s mean and standard deviation of ground-truth class probability across training (50 epochs). Top-left points are easy (high*

![[assets/figures/papers/paper_list_l2689_https_openaccess_thecvf_com_content_CVPR2026_html_Chan_Santiago_Learnabi/figures/010_Figure_6.jpg]]
*Figure 6: In-distribution and learning-dynamics analysis of distilled datasets. Each point represents a sample described by its groundtruth (GT) class probability from the reference model (x-axis, measuring in-distribution likelihood*

## 定位与知识库关联

### 问题脉络：从分布匹配到可学习性引导

数据集蒸馏（Dataset Distillation）的核心目标是将大规模真实数据集压缩为极小规模的合成数据集，使在其上训练的模型能逼近在全数据集上训练的性能。该领域的演进大致可划分为三个阶段：

**第一阶段：基于优化的蒸馏。** 早期工作如 **DM**（Zhao & Bilen, WACV 2023）通过最小化真实数据与合成数据在模型特征空间中的分布差异来优化合成样本；**IDC-1**（Kim et al., ICML 2022）则将合成数据参数化，通过元学习框架直接优化其训练效果。这些方法在小规模数据集上有效，但面对高分辨率、多类别场景时优化困难且生成质量受限。

**第二阶段：基于扩散模型的蒸馏。** 随着扩散生成模型的成熟，研究者开始利用预训练扩散模型作为强先验来合成高质量蒸馏样本。**DiT**（Peebles & Xie, ICCV 2023）首次将扩散模型引入数据集蒸馏，通过类别条件引导统一采样生成样本；**Minimax Diffusion**（Gu et al., CVPR 2024）进一步在微调过程中平衡样本的多样性与代表性；**MGD³**（Chan-Santiago et al., ICML 2025）则通过特征空间模式引导提升生成样本的判别性；**IGD**（Chen et al., ICLR 2025）以匹配训练梯度为引导信号，取得了当时的最优性能。

**第三阶段：LGD的增量可学习性范式。** 上述方法均存在一个被忽视的根本问题——**合成样本的严重冗余**。LGD的核心发现是：将现有方法蒸馏的50 IPC数据集按10 IPC增量划分后，DiT的增量间交叉验证准确率高达98%，IGD也达到约80%（Figure 1）。这意味着不相交的子集捕获了80-90%的重叠训练信号，多个样本传递的是重复信息，而非互补知识。

### 关键设计差异：增量条件生成替代独立合成

LGD与现有扩散蒸馏方法的本质差异在于**合成范式的转变**：

| 设计维度 | 现有扩散蒸馏方法（DiT/IGD/MGD³） | LGD |
|---------|-------------------------------|-----|
| **合成范式** | 一次性生成所有样本，各增量独立 | 增量式构建，每一步以当前模型状态为条件 |
| **引导信号** | 分类器引导或全数据集平均梯度 | 可学习性分数：当前模型损失与参考模型损失之差 |
| **多样性机制** | 无显式类内多样性约束 | 偏离引导：基于记忆缓冲区的余弦相似度排斥 |

**增量条件生成**是LGD方法论的基石。具体而言，LGD将蒸馏过程建模为序列决策问题：在第 $i$ 个阶段，给定已累积的数据集 $\mathcal{D}_{i-1}$ 和在其上训练的模型 $\theta_{i-1}$，目标不是独立生成一组新样本，而是生成能最大化当前模型学习信号的互补样本。这一思想通过可学习性分数 $\mathcal{S}(x, y) = \mathcal{L}(\theta_{i-1}, x, y) - \omega \cdot \mathcal{L}(\theta^*, x, y)$ 实现——高 $\mathcal{S}$ 意味着样本对当前模型困难（高 $\mathcal{L}(\theta_{i-1})$）但对参考模型可识别（低 $\mathcal{L}(\theta^*)$），恰好落在模型的“可学习间隙”中。

这种设计的直接效果是**自适应课程构建**：早期增量生成基础样本填补主要知识缺口，后期增量自动转向更精细的判别边界样本。Figure 4的增量训练动态清晰展示了这一机制——LGD每个新增量都能引发显著的损失尖峰和持续的准确率增益（+12.0%, +3.2%, +5.4%, +6.4%），而DiT的增益随阶段快速衰减（+7.2%, +4.8%, +2.2%, +0.4%），说明其后期增量几乎不提供新信息。

### 适用边界与局限

**适用场景。** LGD在以下条件下表现最优：（1）存在高质量预训练扩散模型作为生成骨干（论文使用DiT）；（2）可获得在全数据集上训练的参考模型用于可学习性校准；（3）目标IPC在10-100范围内，此时增量式课程的优势最为显著。实验表明，LGD在ImageNet-1K（60.1%）、ImageNette（87.2%）、ImageWoof（72.9%）上均取得最优或极具竞争力的结果，且跨架构泛化能力优于IGD和DiT（Table 3）。

**已知局限。** 论文明确指出的局限包括：

1. **计算开销较高**：方法依赖预训练扩散模型的反向采样过程，且增量式训练是串行的——每个阶段需要生成候选样本、训练模型、评估可学习性，循环多次。这比一次性生成的DiT或IGD更耗时。

2. **参考模型依赖**：可学习性分数中的 $\mathcal{L}(\theta^*)$ 项依赖于在全数据集上训练的参考模型。若参考模型本身存在偏差（如对某些子类识别能力弱），可能导致生成的课程引入系统性错误。论文未对此进行敏感性分析。

3. **扩展性未充分验证**：实验主要集中在类数较少的子集（ImageNette 10类、ImageWoof 10类）和ImageNet-1K（1000类），未验证在更多类别（如ImageNet-21K）或更高分辨率场景下的表现。在极高IPC（如IPC 500）下，增量式方法是否仍能有效减少冗余，还是会出现性能饱和，目前缺乏实验证据。

4. **超参数敏感性分析缺失**：论文将部分消融实验置于补充材料，正文中缺少对关键超参数（如可学习性权重 $\omega$、引导强度 $\lambda$、偏离引导强度 $\gamma$）的系统敏感性分析。这些参数如何影响生成质量与冗余度的权衡，需要进一步验证。

5. **代理分类器域差异**：可学习性引导依赖于对扩散模型中间表示 $x_t$ 计算分类损失的梯度。但扩散过程的噪声样本与自然图像存在分布差异，代理分类器在此域上的梯度质量可能影响引导效果。论文未讨论这一潜在问题。

### 开放问题

1. **生成骨干的泛化性**：LGD的可学习性引导机制是否必须依赖扩散模型的反向过程？能否推广到其他生成模型（如GAN、变分自编码器、流模型）？扩散模型提供的逐时间步梯度信息在多大程度上是该方法的关键要素，还是可以被其他形式的可学习性信号替代？

2. **参考模型的自举可能性**：当前方法需要一个在全数据集上预训练的参考模型，这在实际应用中可能不可得。能否通过自举方式——如使用前一轮蒸馏数据集训练的模型作为下一轮的参考模型——来消除这一依赖？这会将方法推向完全自监督的蒸馏范式。

3. **与高效采样策略的结合**：扩散模型的反向采样是计算瓶颈之一。能否将可学习性引导与一致性模型、蒸馏采样等加速策略结合，在保持互补性优势的同时大幅降低生成成本？

4. **可学习性度量的理论分析**：当前可学习性分数的设计基于直觉——当前模型损失高而参考模型损失低的样本具有高信息量。是否存在更优的可学习性度量？例如，是否应纳入模型不确定性、样本在训练动态中的遗忘事件等信息？对此缺乏理论分析和系统比较。

5. **冗余度的根本成因**：LGD揭示了现有方法的严重冗余，但未深入分析冗余产生的根本机制。是扩散模型的采样随机性不足？是引导信号本身缺乏互补性约束？还是优化目标（如分布匹配）天然鼓励样本聚集？回答这些问题可能催生更根本的解决方案。

## 原文 PDF

![[paperPDFs/CVPR_2026/Learnability_Guided_Diffusion_for_Dataset_Distillation.pdf]]
