---
title: Mitigating The Distribution Shift of Diffusion-based Dataset Distillation
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Mitigating_The_Distribution_Shift_of_Diffusion_based_Dataset_Distillation.pdf
project_link: null
code_link: null
aliases:
- RC
- MDSDBDD
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过受限分数匹配（RSM）在训练时引入L1稀疏正则化，迫使扩散模型学习紧凑的语义稀疏流形；通过协同引导采样（CGS）在采样时将全部N个样本同步去噪，并施加行列式点过程（DPP）损失和分布匹配损失，将采样转变为面向整个合成集的全局联合优化。
primary_logic: 数据集蒸馏的理想目标不是精确复制原始数据分布，而是学习一种保留核心可迁移特征的简化流形；同时，低容量场景下必须放弃顺序独立采样，转为对整个合成集的全局协同优化，才能从根本上抑制多样性崩溃和分布漂移。
claims:
- 扩散模型在DD中的直接应用受到合成数据与理想蒸馏数据之间分布偏移的阻碍。
- DD的最优合成分布应该是真实数据分布的简化，而非复制其复杂性。
- RSM通过L1稀疏正则化迫使扩散模型学习语义稀疏流形，减少训练时分布偏移。
- CGS通过同步去噪和DPP与分布匹配损失解决采样时的多样性崩溃和分布漂移。
---

# Mitigating The Distribution Shift of Diffusion-based Dataset Distillation

> [!tip] 核心洞察
> 数据集蒸馏的理想目标不是精确复制原始数据分布，而是学习一种保留核心可迁移特征的简化流形；同时，低容量场景下必须放弃顺序独立采样，转为对整个合成集的全局协同优化，才能从根本上抑制多样性崩溃和分布漂移。

| 字段 | 内容 |
|------|------|
| 中文题名 | 缓解基于扩散的数据集蒸馏中的分布偏移 |
| 英文题名 | Mitigating The Distribution Shift of Diffusion-based Dataset Distillation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Xu_Mitigating_The_Distribution_Shift_of_Diffusion-based_Dataset_Distillation_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | RSM+CGS |
| Dataset | ImageNet-1K, ImageNette, ImageWoof |

> [!tip] 效果简介
> - ImageNet-1K 上，Top-1 Accuracy (IPC 10, ResNet-18) 46.7±0.5 vs previous best diffusion-based method (e.g., IGD) (~1% improvement)；Top-1 Accuracy (IPC 50, ResNet-18) 61.0±0.8 vs previous best diffusion-based method (e.g., IGD) (~1% improvement)。
> - ImageNette 上，Top-1 Accuracy (IPC 10, ConvNet-6) 65.5±0.7 vs previous best diffusion-based method (e.g., IGD 63.8) (+1.7 (outperforms SOTA))。
> - ImageWoof 上，Top-1 Accuracy (IPC 100, ResNet-18) 72.5±0.8 vs previous best diffusion-based method (outperforms SOTA)。

## 概要

**核心问题**：基于扩散模型的数据集蒸馏（Diffusion-based Dataset Distillation, DD）面临两类分布偏移——训练时扩散模型学习过于复杂的完整数据分布，未能提炼出任务感知的简化表示；采样时因合成集容量极小（IPC很小），独立采样导致合成集经验分布偏离目标分布，出现**多样性崩溃**和**分布漂移**。

**核心洞察**：DD的理想目标并非精确复制原始数据分布，而是学习一种保留核心可迁移特征的**简化流形**；同时，低容量场景下必须放弃顺序独立采样，转为对整个合成集的**全局协同优化**，才能从根本上抑制多样性崩溃和分布漂移。

**方法定位**：本文提出两阶段框架 **RSM+CGS**——
- **受限分数匹配（Restricted Score Matching, RSM）**：在真实数据集上微调扩散模型时，对预测的干净潜在变量 $\hat{x}_0$ 施加L1稀疏正则化，迫使模型学习紧凑的**语义稀疏流形**，缓解训练时的分布偏移。
- **协同引导采样（Collaborative Guided Sampling, CGS）**：同步初始化并去噪全部 $N$ 个合成样本，每一步施加**行列式点过程（DPP）损失**强制样本间相互排斥以维持多样性，同时施加**分布匹配损失**将合成集类均值对齐到真实数据的期望均值，纠正分布漂移。

**方法谱系与知识库定位**：该方法属于**基于扩散模型的数据集蒸馏**这一新兴方向，与现有扩散蒸馏方法（如 **Minimax** (Gu et al., CVPR 2024)、**IGD** (Chen et al., ICLR 2025)、**D4M** (Su et al., CVPR 2024)）形成直接对比，同时区别于传统的分布匹配方法（如 **DM** (Zhao & Bilen, WACV 2023)）。其独特贡献在于首次从**流形简化**和**全局协同采样**两个维度系统解决扩散蒸馏中的分布偏移问题。

**主要结果**：
- 在 ImageNet-1K 上，IPC=10 时达到 46.7% Top-1 准确率（ResNet-18），IPC=50 时达到 61.0%，均超越现有最优扩散蒸馏方法约 1%。
- 在 ImageNette 上，IPC=10 时达到 65.5%（ConvNet-6），较 IGD 的 63.8% 提升 1.7 个百分点。
- RSM 单独使用即可超越现有扩散采样优化方法并达到最优水平；CGS 在此基础上额外贡献 1–2% 的提升。
- 推理效率显著优于 IGD：每样本仅需 2.2 秒（IGD 为 8.2 秒），CGS 的额外开销每步 <10ms，可忽略不计。

**关键证据强度**：核心机制（RSM 的 L1 稀疏正则化、CGS 的 DPP 与分布匹配损失）均有消融实验和超参数敏感性分析支撑，置信度 ≥0.9。方法在多个数据集和架构上表现一致，泛化性得到初步验证。

> **注意**：当预训练域与目标域差异较大时效果可能受限；关键超参数 $\lambda$ 和 $\eta$ 需针对不同数据集分别调节，增加了实用中的调参负担。

### 数据集蒸馏的核心矛盾

数据集蒸馏（Dataset Distillation, DD）旨在将大规模真实数据集压缩为极小的合成集，使下游模型在合成集上训练后仍能保持与全量数据相近的泛化能力。这一任务的根本挑战在于：合成集的容量（以每类图像数 IPC 衡量）通常远小于真实数据集，即 $N \ll N_{\mathrm{real}}$。因此，蒸馏过程必须在信息极度受限的条件下，保留对下游任务最关键的可迁移特征。

### 扩散模型引入的分布偏移困境

近年来，扩散模型因其强大的生成能力被引入数据集蒸馏，催生了 **Minimax**（Gu et al., CVPR 2024）、**IGD**（Chen et al., ICLR 2025）、**D4M**（Su et al., CVPR 2024）等方法。然而，这些方法面临一个共同瓶颈：**合成数据与理想蒸馏数据之间存在显著的分布偏移（distribution shift）**，导致性能次优。该分布偏移源于两个阶段的双重失配：

1. **训练时偏移**：扩散模型在真实数据上训练时，学习的是完整数据分布的复杂流形，而非蒸馏任务所需的简化、任务感知的紧凑表示。模型过度拟合了原始数据中的冗余细节和类内变异，使得后续采样难以聚焦于核心可迁移特征。

2. **采样时偏移**：现有方法采用顺序独立同分布（i.i.d.）采样策略，逐个生成合成样本。当合成集容量极小（低 IPC）时，这种贪婪的独立采样方式造成两类严重问题：
   - **多样性崩溃（diversity collapse）**：独立采样缺乏全局协调机制，导致同类合成样本高度相似，无法覆盖类内语义多样性。
   - **分布漂移（distribution drift）**：少量独立样本的经验分布天然偏离目标分布，低容量条件下尤其严重。

### 核心洞察

本工作的核心洞察在于重新审视数据集蒸馏的目标本质：**最优合成分布应当是真实数据分布的简化，而非对其复杂性的复制**。这意味着扩散模型需要学习的是一个保留核心可迁移特征的稀疏语义流形，而非原始数据的高维完整分布。同时，在极低容量场景下，必须放弃顺序独立采样范式，转而将采样过程建模为面向整个合成集的全局联合优化问题，才能从根本上抑制多样性崩溃和分布漂移。

### 本文动机与方法概览

基于上述洞察，本文提出两阶段方法 **RSM+CGS**，分别针对训练时和采样时的分布偏移进行系统性干预：

- **受限分数匹配（Restricted Score Matching, RSM）**：在扩散模型微调阶段，对预测的干净潜在变量 $\hat{x}_0$ 施加 L1 稀疏正则化，迫使模型学习紧凑的语义稀疏流形，从源头减少训练时偏移。
- **协同引导采样（Collaborative Guided Sampling, CGS）**：在采样阶段，同步初始化并去噪全部 $N$ 个合成样本，通过行列式点过程（DPP）损失强制样本间互斥以保障多样性，同时通过分布匹配损失将合成集的经验分布拉向真实分布，纠正分布漂移。

这一设计将数据集蒸馏从“生成-挑选”范式转变为“全局联合优化”范式，为扩散模型在数据蒸馏中的可靠应用提供了新的理论视角和实践方案。

## 核心方法与创新机理

本文的核心贡献在于首次系统性地识别并缓解了扩散模型应用于数据集蒸馏时的两类分布偏移，并据此提出了**受限分数匹配（RSM）**与**协同引导采样（CGS）**的两阶段框架。其创新本质并非更换扩散模型架构，而是通过改变训练目标与采样范式，将扩散模型从“完整数据分布复制器”改造为“蒸馏感知的简化流形生成器”。

### 训练端创新：受限分数匹配（RSM）

现有扩散式数据集蒸馏方法（如 **Minimax** (Gu et al., CVPR 2024)、**IGD** (Chen et al., ICLR 2025)、**D4M** (Su et al., CVPR 2024)）直接沿用扩散模型的标准分数匹配损失，使其学习完整数据分布的复杂流形。然而，数据集蒸馏的最优合成分布应是真实分布的**简化**，而非精确复制。

RSM 在标准扩散训练损失的基础上，对预测的干净潜在变量 $\hat{x}_0$ 施加 L1 稀疏正则化：

$$\mathcal{L}_{RSM} = \mathbb{E}_{t, x_{0}, \epsilon} ||\epsilon - \epsilon_{\theta}(x_t, t; \theta)||_2^2 + \lambda \mathbb{E}_{t, x_{0}, \epsilon} ||\hat{x}_{0}(x_t, t; \theta)||_1$$

其核心机理在于：L1 正则化迫使扩散模型学习一个**语义稀疏流形**——在该流形上，样本的潜在表示具有更少的非零激活，从而剥离掉对下游任务无益的冗余细节，仅保留可迁移的核心特征。这一设计直接回应了“训练时分布偏移”的瓶颈：扩散模型不再试图拟合完整数据分布的复杂性，而是提炼出任务感知的简化表示空间。

### 采样端创新：协同引导采样（CGS）

传统扩散采样采用**顺序独立同分布（i.i.d.）生成**范式，逐个生成合成样本。在数据集蒸馏的低容量场景（IPC 极小，$N \ll N_{\mathrm{real}}$）下，这种贪婪策略无法保证合成集的整体质量，引发两类问题：**多样性崩溃**（样本趋同）与**分布漂移**（合成集经验分布偏离目标分布）。

CGS 从根本上改变了采样范式，包含两个关键机制：

**1. 同步去噪与全局联合优化。** CGS 放弃顺序采样，转而将全部 $N$ 个样本初始化为噪声，并在每个去噪步同步更新整个合成集。这使得采样过程从一个局部贪婪决策转变为**面向整个合成集的全局联合优化**，使模型能够显式地协调样本间的互补关系。

**2. 双分量协同引导梯度。** 在每一步去噪后，对合成集施加两项引导损失，并通过梯度更新修正潜在变量：

$$g_t^c = \eta_{dpp} \nabla_{\mathcal{Z}_t^c} \mathcal{L}_{dpp}(\mathcal{Z}_t^c) + \eta_{dm} \nabla_{\mathcal{Z}_t^c} \mathcal{L}_{dm}(\mathcal{Z}_t^c)$$

- **行列式点过程（DPP）损失** $\mathcal{L}_{dpp}$：通过最大化合成样本间余弦相似度核矩阵的行列式，强制样本在特征空间中尽可能正交（不相似），主动施加样本间斥力以防止多样性崩溃。
- **分布匹配损失** $\mathcal{L}_{dm}$：将合成集每类的均值与预先计算的真实数据干净潜在均值 $\mu_{\mathrm{real},0}^c$ 对齐，纠正低容量采样导致的分布漂移。

### 与 baseline 的关键差异总结

| 变更维度 | 现有扩散式 DD 方法 | 本文方法 (RSM+CGS) |
|---------|-------------------|-------------------|
| 扩散训练目标 | 标准 $\mathbb{E}\|\epsilon - \epsilon_\theta\|^2$ | 增加 $\lambda \mathbb{E}\|\hat{x}_0\|_1$ 稀疏正则化 |
| 采样策略 | 顺序 i.i.d. 生成 | 全部 $N$ 个样本同步去噪（联合优化） |
| 多样性机制 | 无（隐式依赖随机噪声） | DPP 损失主动施加样本间斥力 |
| 分布对齐 | 无或像素空间分布匹配 | 潜在空间均值对齐（分布匹配损失） |

消融实验证实了这两个模块的独立贡献：**RSM 单独使用即可超越现有扩散采样优化方法并达到最优性能**，而 CGS 在 RSM 基础上进一步提供 **1–2% 的额外提升**。这表明训练端的流形简化与采样端的全局协同优化是两个互补且各自有效的创新维度。

本文提出了一种两阶段扩散数据集蒸馏框架 **RSM+CGS**，旨在系统性地缓解扩散模型在数据集蒸馏中引入的两类分布偏移——训练时的流形过复杂化与采样时的多样性崩溃/分布漂移。整体流程如 **Algorithm 1** 所示，包含以下关键模块与数据流：

### 阶段一：受限分数匹配（Restricted Score Matching, RSM）

**输入**：真实数据集 $\mathcal{D}_{\text{real}}$ 与预训练扩散模型（本文采用 **DiT** (Peebles & Xie, ICCV 2023) 作为基础模型）。

**处理流程**：
1. 通过 **VAE 编码器** 将真实图像映射至潜在空间，获得干净潜在变量 $z_0$。
2. 在真实数据集上对扩散模型进行微调，训练目标为标准分数匹配损失与新增的 **L1 稀疏正则化项** 的加权和：

$$\mathcal{L}_{\text{RSM}} = \mathbb{E}_{t, x_0, \epsilon} \|\epsilon - \epsilon_\theta(x_t, t)\|_2^2 + \lambda \mathbb{E}_{t, x_0, \epsilon} \|\hat{x}_0(x_t, t)\|_1$$

其中 $\hat{x}_0$ 为从噪声状态 $x_t$ 反推出的干净数据估计（见 Eq. 3）。L1 正则化项迫使扩散模型学习一个 **语义稀疏流形**，抑制对原始数据复杂分布中非必要细节的建模。

**输出**：经过 RSM 微调的扩散模型，其生成流形已被简化为保留核心可迁移特征的紧凑表示。

### 阶段二：协同引导采样（Collaborative Guided Sampling, CGS）

**输入**：RSM 微调后的扩散模型、每类合成样本数 $N$（即 IPC）、预计算的每类真实数据干净潜在均值 $\boldsymbol{\mu}_{\text{real},0}^c$。

**处理流程**：
1. **同步初始化**：为每个类别 $c$ 同时初始化 $N$ 个纯噪声样本，构成合成潜在集合 $\mathcal{Z}_T^c$。
2. **协同去噪**：在每一步去噪 $t \to t-1$ 中，对全部 $N$ 个样本同步执行去噪更新，而非传统的独立顺序采样。
3. **引导梯度注入**：在每一步去噪后，对中间潜在变量集施加两类引导损失：
   - **DPP 多样性损失**（Eq. 5）：通过最大化余弦相似度核矩阵的行列式，强制 $N$ 个样本相互排斥，防止多样性崩溃。
   - **分布匹配损失**（Eq. 7）：将合成集的经验均值与真实数据在该去噪步的期望均值对齐，纠正低容量采样导致的分布漂移。

   总引导梯度为两者的加权和（Eq. 8）：
   $$g_t^c = \eta_{\text{dpp}} \nabla_{\mathcal{Z}_t^c} \mathcal{L}_{\text{dpp}}(\mathcal{Z}_t^c) + \eta_{\text{dm}} \nabla_{\mathcal{Z}_t^c} \mathcal{L}_{\text{dm}}(\mathcal{Z}_t^c)$$

4. **解码输出**：去噪完成后，通过 **VAE 解码器** 将最终潜在变量 $z_0$ 映射回图像空间，得到合成数据集。

**输出**：紧凑且多样化的合成数据集，可直接用于下游分类器的训练。

### 模块关系与设计逻辑

两个阶段分别针对分布偏移的不同来源，形成互补：

| 偏移类型 | 发生阶段 | 对应模块 | 核心机制 |
|---------|---------|---------|---------|
| 训练时分布偏移（流形过复杂） | 扩散模型微调 | RSM | L1 稀疏正则化 → 语义稀疏流形 |
| 采样时多样性崩溃 | 合成集生成 | CGS (DPP) | 行列式点过程 → 样本互斥 |
| 采样时分布漂移 | 合成集生成 | CGS (DM) | 一阶矩对齐 → 分布校正 |

RSM 单独使用已能超越现有扩散采样优化方法（如 **Minimax** (Gu et al., CVPR 2024)、**IGD** (Chen et al., ICLR 2025)），达到 SOTA 水平；CGS 在此基础上提供额外的 1-2% 性能增益。两阶段的设计使得训练阶段的流形简化与采样阶段的全局协同优化相互解耦又彼此增强，共同实现了对扩散数据集蒸馏中分布偏移问题的系统性缓解。

本方法由两个互补阶段构成：**受限分数匹配（Restricted Score Matching, RSM）** 在训练时重塑扩散模型的生成流形，**协同引导采样（Collaborative Guided Sampling, CGS）** 在采样时对全体合成样本进行联合优化。两阶段均以潜在扩散模型为基础，图像先经VAE编码器映射到潜在空间，蒸馏完成后再解码回图像空间。

### 受限分数匹配（RSM）

扩散模型在真实数据集 $D_{real}$ 上微调时，标准训练目标仅最小化噪声预测误差：

$$ \mathcal{L}_{diff} = \mathbb{E}_{t, x_{0}, \epsilon} \, || \epsilon - \epsilon_{\theta}(x_{t}, t) ||^{2} \tag{Eq. 2} $$

其中 $x_{t} = \sqrt{\bar{\alpha}_{t}} x_{0} + \sqrt{1 - \bar{\alpha}_{t}} \epsilon$ 为前向加噪后的样本（Eq. 1），$\epsilon_{\theta}$ 为扩散模型预测的噪声。

从噪声状态 $x_t$ 可反推出对原始清洁数据的估计：

$$ \hat{x}_{0}(x_{t}, t) = \frac{1}{\sqrt{\bar{\alpha}_{t}}} (x_{t} - \sqrt{1 - \bar{\alpha}_{t}} \, \epsilon_{\theta}(x_{t}, t)) \tag{Eq. 3} $$

标准训练会使扩散模型学习完整的数据分布，但这与数据集蒸馏（DD）对简化表示的需求相悖。RSM 的核心创新是在微调时对预测的清洁数据 $\hat{x}_0$ 施加 L1 稀疏正则化，迫使模型学习**语义稀疏流形**：

$$ \mathcal{L}_{RSM} = \mathbb{E}_{t, x_{0}, \epsilon} ||\epsilon - \epsilon_{\theta}(x_t, t; \theta)||_2^2 + \lambda \, \mathbb{E}_{t, x_{0}, \epsilon} ||\hat{x}_{0}(x_t, t; \theta)||_1 \tag{Eq. 4} $$

其中 $\lambda$ 控制稀疏正则化的强度。L1 范数鼓励 $\hat{x}_0$ 中大部分激活趋近于零，使扩散模型倾向于生成特征更紧凑、语义更集中的样本，从而减少训练时的分布偏移。

### 协同引导采样（CGS）

当合成集容量极小（IPC 很小）时，传统的顺序独立采样会导致**多样性崩溃**（生成样本高度相似）和**分布漂移**（合成集经验分布偏离目标分布）。CGS 放弃逐样本独立采样，改为初始化 $N$ 个噪声样本并**同步去噪**，在每一步去噪后施加两类引导损失。

**DPP 多样性损失**基于行列式点过程，强制同类合成样本相互排斥。对类别 $c$ 的潜在变量集 $\mathcal{Z}_t^c$，计算样本间余弦相似度核矩阵 $K_{\mathcal{Z}}$，最大化其行列式以促进正交性：

$$ \mathcal{L}_{dpp}(\mathcal{Z}_t^c) = -\log(\det(K_{\mathcal{Z}} + \epsilon I)) \tag{Eq. 5} $$

其中 $\epsilon I$ 保证数值稳定性。

**分布匹配损失**纠正分布漂移。预先计算每类真实数据在干净潜在空间中的均值 $\pmb{\mu}_{\mathrm{real}, 0}^{c}$，根据全期望公式，其在去噪步 $t$ 的期望均值为 $\sqrt{\bar{\alpha}_{t}} \cdot \pmb{\mu}_{\mathrm{real}, 0}^{c}$。将合成集的类均值与之对齐：

$$ \mathcal{L}_{dm}(\mathcal{Z}_t^c) = \left\| \left( \frac{1}{N} \sum_{i=1}^{N} z_{t}^{c, (i)} \right) - \sqrt{\bar{\alpha}_{t}} \, \pmb{\mu}_{\mathrm{real}, 0}^{c} \right\|_2^2 \tag{Eq. 7} $$

每一步的协同引导梯度为两者的加权和：

$$ g_t^c = \eta_{dpp} \nabla_{\mathcal{Z}_t^c} \mathcal{L}_{dpp}(\mathcal{Z}_t^c) + \eta_{dm} \nabla_{\mathcal{Z}_t^c} \mathcal{L}_{dm}(\mathcal{Z}_t^c) \tag{Eq. 8} $$

该梯度用于更新去噪后的潜在变量集，使全体样本在保持多样性的同时整体分布不偏离目标。

## 实验与关键发现

### 主实验：ImageNet 子集与全量 ImageNet-1K

**RSM+CGS 在多个基准上一致地超越现有基于扩散的数据集蒸馏方法。** Table 1 展示了在 ImageNette 和 ImageWoof 两个 ImageNet 子集上、使用不同评估架构（ConvNet-6、ResNet-10、ResNet-18）的性能对比。以 ImageNette IPC 10 + ConvNet-6 为例，RSM+CGS 达到 **65.5±0.7** 的 Top-1 准确率，比此前最佳的扩散方法（如 IGD 的 63.8）高出约 **1.7 个百分点**；在 IPC 100 设定下，RSM+CGS 达到 86.7±0.6，同样处于领先位置。ImageWoof 上 IPC 100 + ResNet-18 的结果为 **72.5±0.8**，进一步验证了方法在不同难度子集上的鲁棒性。

Table 2 报告了更具挑战性的 **ImageNet-1K 全量数据集**（ResNet-18 评估）上的结果。在 IPC 10 设定下，RSM+CGS 达到 **46.7±0.5**；在 IPC 50 设定下达到 **61.0±0.8**，均比此前最佳扩散方法（如 IGD）高出约 **1 个百分点**。值得注意的是，RSM+CGS 在计算效率上显著优于 IGD——推理时间仅为其 **25%**（每样本 2.2 秒 vs 8.2 秒），同时保持可比甚至更优的性能。

![[assets/figures/papers/paper_list_l2694_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_Mitigating_The_Dist/figures/002_Table_2.jpg]]
*Table 2: Comparison on ImageNet-1K with ResNet-18*

### 消融实验：RSM 与 CGS 的贡献解耦

消融实验揭示了两个核心发现：

**第一，RSM 单独使用即足以超越现有的扩散采样优化方法。** 在仅使用受限分数匹配（RSM）而不引入 CGS 的情况下，方法已取得当时最优水平（state-of-the-art）的性能。这验证了核心假设：在扩散模型训练阶段通过 L1 稀疏正则化学习语义稀疏流形，是缓解训练时分布偏移的关键瓶颈。

**第二，CGS 在 RSM 基础上提供额外的 1–2% 增益。** 协同引导采样（CGS）的引入进一步提升了性能，且这一增益在不同 IPC 设定下稳定存在。具体而言，DPP 多样性损失通过强制合成样本间相互排斥，主动防止了多样性崩溃；分布匹配损失则通过将合成集每类均值与真实数据潜在均值对齐，纠正了低容量采样导致的分布漂移。CGS 的额外计算开销极小——行列式和对数运算每步耗时不足 **10 ms**，相对于扩散去噪过程本身可忽略不计。

### 超参数敏感性分析

Figure 1 展示了关键超参数的消融结果（ImageNette，ResNet-18）：

![[assets/figures/papers/paper_list_l2694_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_Mitigating_The_Dist/figures/003_Figure_1.jpg]]
*Figure 1: Ablation of hyperparameters on ImageNette and ResNet-18. Left: RSM weight λ. Middle and right: CGS weight*

- **RSM 权重 λ**：最优区间为 **[0.002, 0.006]**。λ 过小时稀疏正则化效果不足，流形未能充分简化；λ 过大则过度约束生成能力，损害合成数据的表达能力。
- **CGS 引导权重 η_dpp 和 η_dm**：最优范围约为 **30–300**。两个损失项需要协同调节——DPP 损失过强可能导致样本过度分散而偏离真实流形，分布匹配损失过强则可能抑制多样性。

### 定性分析：合成样本质量与潜在空间结构

Figure 2 定性比较了不同扩散数据集蒸馏方法（DiT、IGD 与 RSM+CGS）生成的合成样本。RSM+CGS 生成的样本在视觉质量和类别内多样性上均表现出优势，避免了其他方法中常见的模式重复和多样性不足问题。

![[assets/figures/papers/paper_list_l2694_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_Mitigating_The_Dist/figures/004_Figure_2.jpg]]
*Figure 2: Examples of synthetic data samples of state-of-the-art diffusion-based dataset distillation algorithms*

Figure 3 通过 T-SNE 可视化进一步揭示了潜在空间的结构差异。使用 DiT 基线时，合成样本的潜在嵌入呈现明显的聚集和重叠；而 RSM+CGS 的合成样本展现出更清晰的类别分离度和更高的样本离散度（以 γ 指标衡量）。这从几何层面印证了 DPP 损失和分布匹配损失的有效性——前者强制样本在潜在空间中相互排斥，后者确保类级分布中心与真实数据对齐。

![[assets/figures/papers/paper_list_l2694_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_Mitigating_The_Dist/figures/005_Figure_3.jpg]]
*Figure 3: T-SNE visualization of latent embeddings of synthesized samples. We apply an offset to each class for clearer presentation*

### 失败模式与局限性

尽管 RSM+CGS 取得了显著的性能提升，仍存在以下值得关注的局限：

1. **预训练依赖**：方法假设有可用的预训练扩散模型并在目标数据集上进行微调。当预训练域与目标域差异较大时，RSM 的稀疏流形学习可能受到影响，需进一步验证跨域迁移场景下的鲁棒性。
2. **超参数调参负担**：关键超参数 λ 和 η 需要针对不同数据集分别调节。虽然最优区间相对稳定，但在实际部署中仍增加了调参成本。能否设计自动化的超参数调节策略（如基于少量验证数据的启发式算法）是一个有待探索的开放问题。
3. **DPP 损失的数值稳定性**：当涉及数百个类别或不同 IPC 场景时，余弦相似度核矩阵的行列式计算可能面临数值稳定性挑战，需要进一步研究其在大规模设定下的表现。

![[assets/figures/papers/paper_list_l2694_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_Mitigating_The_Dist/figures/001_Table_1.jpg]]
*Table 1: Comparison on ImageNet subsets (ImageNette & ImageWoof) with diverse architectures. Best results are in bold*

## 定位与知识库关联

### 1. 方法谱系：从分布匹配到扩散生成

数据集蒸馏（Dataset Distillation, DD）的核心目标是将大规模真实数据集压缩为极小规模的合成集，同时保持下游模型训练的性能。早期方法以**分布匹配**（Distribution Matching）为范式，代表性工作如 **DM**（Zhao & Bilen, WACV 2023），通过在像素空间直接对齐合成集与真实集的统计特征来优化合成样本。这类方法虽简单高效，但受限于像素空间的表达能力和合成容量的刚性约束。

随着扩散模型在图像生成领域的突破，研究者开始将扩散先验引入DD，试图利用其强大的生成能力提升合成数据的质量和多样性。代表性工作包括：

- **Minimax**（Gu et al., CVPR 2024）：将DD建模为极小极大优化问题，利用扩散模型作为生成先验。
- **D4M**（Su et al., CVPR 2024）：通过扩散模型进行数据增强和匹配。
- **IGD**（Chen et al., ICLR 2025）：引入指导机制改进扩散采样过程。

这些方法通常基于预训练扩散模型（如 **DiT**，Peebles & Xie, ICCV 2023），在目标数据集上进行微调后采样生成合成集。然而，本文指出，直接将扩散模型应用于DD会面临**两类分布偏移**的根本性问题，导致现有方法的性能仍存在瓶颈。

### 2. 核心贡献与差异化定位

本文的独特贡献在于**首次系统性地识别并分别解决扩散DD中的训练时和采样时分布偏移**，而非简单地将扩散模型视为黑箱生成器：

| 偏移类型 | 发生阶段 | 根本原因 | 本文解决方案 |
|---------|---------|---------|------------|
| **训练时偏移** | 扩散模型微调 | 模型学习过于复杂的完整数据分布，未能提炼任务感知的简化表示 | **受限分数匹配（RSM）**：通过L1稀疏正则化强制学习语义稀疏流形 |
| **采样时偏移** | 合成集生成 | 独立采样导致小容量合成集经验分布偏离目标分布，出现多样性崩溃 | **协同引导采样（CGS）**：同步去噪+DPP多样性损失+分布匹配损失 |

这一双阶段设计使得本文方法与现有工作形成了清晰的差异化：

- **相较于Minimax、D4M等**：它们未显式处理扩散模型训练阶段的分布偏移，仅依赖标准扩散损失微调，导致学习的生成流形过于复杂。
- **相较于IGD等采样优化方法**：它们虽改进了采样过程，但仍采用顺序独立采样范式，无法从根本上解决低容量场景下的多样性崩溃和分布漂移。本文的CGS通过将采样转变为**全局联合优化问题**，在机制层面实现了突破。
- **相较于传统DM**：本文在潜在空间而非像素空间进行分布匹配，利用扩散模型的语义表达能力获得更高质量的合成样本。

消融实验的关键证据支持这一差异化定位：**RSM单独使用即可超越现有扩散采样优化方法并达到SOTA性能**，而CGS在此基础上进一步提供**1-2%的额外提升**（ImageNette IPC 10场景下，RSM+CGS达到65.5±0.7，超越IGD的63.8）。

### 3. 方法适用边界

本文方法的有效性依赖于以下前提条件，这些条件界定了其适用边界：

1. **预训练扩散模型可用性**：方法假设存在在足够大规模数据上预训练的扩散模型（如DiT），并在目标数据集上进行微调。当预训练域与目标域差异显著时（例如从自然图像迁移到医学影像），扩散先验的迁移效果可能下降，需要进一步验证。

2. **类别条件生成框架**：CGS中的分布匹配损失依赖每类的真实潜在均值 $\pmb{\mu}_{\mathrm{real,0}}^{c}$ 作为对齐目标，因此方法天然适用于分类导向的DD场景。对于无类别标签的数据蒸馏任务，需要重新设计分布匹配策略。

3. **超参数敏感性**：RSM的稀疏正则化权重 $\lambda$ 和CGS的引导权重 $\eta_{dpp}$、$\eta_{dm}$ 需要针对不同数据集分别调节。实验表明，$\lambda$ 的最优区间为 $[0.002, 0.006]$，CGS引导权重的最优范围在 $30$ 到 $300$ 之间，偏离这些区间会导致性能显著下降。

4. **计算效率优势**：相较于IGD，本文方法具有显著的效率优势——推理时间仅为IGD的**25%**（每样本2.2秒 vs 8.2秒），CGS的额外计算开销（行列式和对数计算）每步耗时不到10ms，相对扩散过程本身可忽略不计。这使得方法在实际部署中更具可行性。

### 4. 局限性与开放问题

尽管取得了显著进展，本文方法仍存在若干局限，并由此衍生出值得探索的开放问题：

**方法局限性：**

- **跨域迁移不确定性**：方法在ImageNet及其子集上验证有效，但扩散模型的预训练数据（通常为LAION等大规模图文数据）与专业化领域（如遥感、病理）之间的分布差异可能削弱RSM学习到的语义稀疏流形的迁移质量。此点需要手动验证。
- **调参负担**：关键超参数 $\lambda$ 和 $\eta$ 依赖人工调节，缺乏自动化机制，在应用到新数据集时增加了实验成本。
- **DPP损失的数值稳定性**：当合成类别数或每类样本数 $N$ 增大时，余弦相似度核矩阵 $K_{\mathcal{Z}}$ 可能趋于奇异，行列式计算面临数值稳定性挑战。当前实验主要在IPC ≤ 100的设置下进行，更大规模场景的鲁棒性有待检验。

**开放问题：**

1. **稀疏正则化的推广性**：L1稀疏正则化是否可推广到其他类型的生成模型（如GAN、归一化流）以用于数据蒸馏？这涉及生成模型架构与蒸馏目标之间的本质适配性问题。

2. **自动化超参数调节**：能否设计基于少量验证数据的启发式算法或元学习策略，自动为不同数据集选择合适的 $\lambda$ 和 $\eta$，减少人工调参负担？

3. **DPP损失的扩展性**：在涉及数百个类别或极端IPC场景下，如何保持核矩阵行列式的数值稳定性？可能的方案包括低秩近似、分块计算或引入替代的多样性度量。

4. **协同采样与高效去噪的结合**：CGS的同步去噪过程能否与更高效的去噪步骤（如DDIM、DPM-Solver）结合，在保持合成质量的同时进一步加速合成过程？这需要在引导梯度与跳步去噪之间建立兼容机制。

5. **无类别标签场景的拓展**：当前分布匹配损失依赖类均值，如何将CGS框架拓展到无监督或自监督的数据蒸馏场景，是一个具有实际价值的开放方向。

## 原文 PDF

![[paperPDFs/CVPR_2026/Mitigating_The_Distribution_Shift_of_Diffusion_based_Dataset_Distillation.pdf]]
