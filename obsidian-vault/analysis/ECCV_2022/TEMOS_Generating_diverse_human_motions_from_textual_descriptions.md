---
title: "TEMOS: Generating diverse human motions from textual descriptions"
type: paper
paper_level: A
venue: ECCV
year: 2022
pdf_ref: paperPDFs/ECCV_2022/TEMOS_Generating_diverse_human_motions_from_textual_descriptions.pdf
project_link: https://mathis.petrovich.fr/temos/
code_link: null
aliases:
- TEMOS
tags:
- ECCV_2022
- topic/generative_models_diffusion
- topic/generative_models_diffusion/generative_models_and_autoencoders
core_operator: "通过非自回归的Transformer解码器一次性生成完整运动序列，并结合VAE在共享的文本-运动潜在空间中进行随机采样，从而实现多样化且连贯的运动生成。"
primary_logic: "将序列整体建模为单个潜在向量并通过Transformer一次性解码，有效缓解了长期依赖与漂移问题；在跨模态潜在空间内施加变分约束，使解码器能够为同一文本生成多个符合描述的运动变体。"
claims:
- "与GRU等循环架构相比，Transformer架构带来了最显著的性能提升"
- "变分模型通过采样10个生成中最佳的一个，将根关节APE从1.175降至0.784"
- "冻结DistilBERT优于微调，在APE均值全局上从1.414降至0.976"
- "在用户感知研究中，TEMOS在语义匹配和真实感上均显著优于先前最先进方法，甚至部分情况下优于真实数据"
---

# TEMOS: Generating diverse human motions from textual descriptions

> [!tip] 核心洞察
> 将序列整体建模为单个潜在向量并通过Transformer一次性解码，有效缓解了长期依赖与漂移问题；在跨模态潜在空间内施加变分约束，使解码器能够为同一文本生成多个符合描述的运动变体。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | TEMOS：通过文本描述生成多样化的人体运动 |
| 英文题名 | TEMOS: Generating diverse human motions from textual descriptions |
| 会议/期刊 | ECCV 2022 |
| Links | [paper](https://arxiv.org/abs/2204.14109) · [Project](https://mathis.petrovich.fr/temos/) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/generative_models_and_autoencoders |
| Method | TEMOS |
| Dataset | KIT Motion-Language |

> [!tip] 效果简介
> - KIT Motion-Language 上，APE root joint (m) 为 0.963，对比 1.291 (Ghosh et al.)，变化 -0.328。
> - KIT Motion-Language 上，AVE root joint (m) 为 0.445，对比 0.564 (Ghosh et al.)，变化 -0.119。
> - KIT Motion-Language 上，APE global trajectory (m) 为 0.955，对比 1.242 (Ghosh et al.)，变化 -0.287。

## 概要

### 问题瓶颈

文本到人体运动生成任务面临两个核心挑战。其一，文本描述天然具有模糊性——同一句话可以对应多种合理的运动表现——但现有方法普遍采用确定性映射，只能为每个输入文本产生单一输出。其二，主流的自回归逐帧解码策略容易在长序列上累积误差，导致生成的运动出现长期漂移甚至陷入静止姿态。

### 核心方法

TEMOS通过两个关键设计同时解决上述问题。在解码策略上，它采用**非自回归的Transformer解码器**，从单个潜在向量一次性生成完整运动序列，从根本上消除逐帧误差累积。在生成模式上，它引入**变分自编码器（VAE）框架**，在共享的文本-运动潜在空间中施加变分约束，使模型能够通过随机采样为同一文本生成多样化的运动变体。文本侧使用冻结的DistilBERT提取词嵌入，运动侧和文本侧分别通过对称的Transformer编码器映射到联合潜在空间，训练时以重建损失、KL散度损失和跨模态嵌入相似性损失的加权和作为优化目标。

### 方法定位

在方法谱系中，TEMOS属于**跨模态变分生成模型**，其关键改进可归纳为三个维度：

| 设计维度 | 先前方法 | TEMOS |
|---------|---------|-------|
| 序列解码 | 自回归逐帧生成（如Ghosh et al.） | 非自回归一次性全序列生成 |
| 生成模式 | 确定性单输出 | 基于VAE的随机多样化生成 |
| 文本编码 | 微调的BERT或word2vec | 冻结的DistilBERT |

与同期工作相比，TEMOS在架构选择上做出了明确取舍：用Transformer替换循环网络（GRU）带来的性能增益远大于损失函数的精细调节，而冻结语言模型反而优于端到端微调。

### 主要结果

在KIT Motion-Language数据集上，TEMOS在多项指标上显著超越先前方法。以根关节平均位置误差（APE root joint）为例，TEMOS达到0.963 m，相比Ghosh et al.的1.291 m降低了约25%。变分模型的采样机制进一步放大了这一优势：从10次随机生成中选取最佳样本时，根关节APE可进一步降至0.784 m。

用户感知研究提供了更强的证据：在语义匹配度比较中，TEMOS的生成结果被用户偏好的比例显著高于Lin et al.、JL2P和Ghosh et al.等先前方法；在真实感评估中，TEMOS甚至有15.5%的情况下被认为优于真实运动数据，而Ghosh et al.仅为8.5%。

### 局限与开放问题

TEMOS的性能受限于KIT数据集的规模和词汇丰富度，对未见描述和复杂动作的泛化能力有限。模型未显式建模脚-地面接触与物理约束，可能导致脚步滑动等伪影。此外，Transformer的二次复杂度使其难以直接扩展到数分钟级别的长序列运动。这些局限指向若干开放方向：显式物理约束的整合、运动时长的自动估计、长序列场景下的效率优化，以及更能反映人类感知的多样化评价指标设计。

从自然语言描述生成人体运动序列，是连接视觉感知与语言理解的重要交叉问题，在动画制作、虚拟角色控制和人机交互等场景中有广泛应用。该任务的核心挑战在于，自然语言天然具有模糊性和多义性——同一句描述（如“一个人走向桌子”）可以对应多种合理的运动实现，而人类观察者能够接受这些变体。

然而，现有方法在处理这种“一对多”映射时存在两个根本性瓶颈。**第一，确定性映射导致输出单一**。以 **JL2P**（Ahuja & Morency, 2019）和 **Ghosh et al.**（2021）为代表的先前工作，将文本到运动的生成建模为确定性函数：给定文本输入，模型输出唯一确定的运动序列。这种设计无法捕捉语言描述内在的歧义性，用户无法获得多个合理候选来满足不同场景需求。**第二，自回归逐帧解码造成长期漂移**。主流方法采用循环神经网络（RNN）或自回归Transformer逐帧预测未来姿态，每一帧的误差会在序列中累积传播，导致生成的运动在长时间跨度上偏离合理分布，甚至陷入静止姿态（“冻结”现象）。

上述两个瓶颈的叠加效应尤为严重：确定性模型缺乏对运动分布的整体建模，而逐帧解码又使局部误差无法被全局上下文校正。这导致生成的运动在**语义一致性**（是否符合文本描述）和**物理真实感**（是否自然流畅）两个维度上均难以令人满意。

TEMOS的提出正是针对这两大缺陷。其核心动机在于：**将序列整体建模为单个潜在向量，并通过非自回归的Transformer解码器一次性生成完整运动，从而同时解决多样性与长期连贯性问题**。具体而言，该方法引入变分自编码器（VAE）框架，在文本与运动的共享潜在空间中施加概率分布约束，使解码器能够通过随机采样为同一文本生成多个语义一致但细节不同的运动变体。这一设计从因果机制上切断了逐帧误差累积的路径，并将“一对多”映射显式地编码进模型结构。

## 核心方法与创新机理

TEMOS 的核心创新在于通过**非自回归的 Transformer 解码器一次性生成完整运动序列**，并结合**VAE 在共享的文本-运动潜在空间中进行随机采样**，系统性解决了文本条件人体运动生成中的两大瓶颈：确定性映射导致的单一输出，以及自回归逐帧解码引发的长期漂移与静止姿态。

### 关键 changed slots

**1. 序列解码方式：自回归逐帧生成 → 非自回归全序列一次性生成**

先前方法（如 **Ghosh et al.** 和 **JL2P**）普遍采用自回归架构，逐帧预测下一帧姿态。这种方式容易累积误差，导致长时间序列出现漂移或陷入静止姿态。TEMOS 改用 Transformer 解码器，将整个运动序列建模为单个潜在向量 $z$ 的一次性解码输出，从机制上切断了逐帧误差传播路径。消融实验（Table 3）提供了决定性证据：将 Transformer 替换为 GRU 后，APE 均值全局从 0.976 骤增至 1.451，表明 Transformer 架构是性能提升的最关键组件。此外，一次性解码使训练时间从自回归方式的约 15 小时缩短至 4.5 小时，效率提升一个数量级。

**2. 生成模式：确定性单输出 → 基于 VAE 的随机多样化生成**

语言描述天然具有模糊性（如“一个人走路”可能对应多种步态风格），确定性模型只能输出单一结果，无法捕捉这种多样性。TEMOS 在跨模态潜在空间上施加变分约束，使文本编码器和运动编码器分别输出高斯分布参数 $\mu$ 和 $\Sigma$，通过重参数化技巧采样潜在向量 $z$，从而为同一文本生成多个符合描述的运动变体。Table 2 的消融实验量化了这一收益：变分模型生成 10 个样本并选择最佳者，根关节 APE 从确定性模型的 1.175 降至 0.784。用户感知研究（Figure 3）进一步验证，TEMOS 在语义匹配和真实感上均显著优于先前方法，甚至在 15.5% 的情况下被用户认为优于真实数据。

**3. 文本编码器：微调的 BERT/word2vec → 冻结的 DistilBERT**

先前工作通常对语言模型进行端到端微调，但这在跨模态小数据集上容易过拟合。TEMOS 采用冻结的预训练 DistilBERT 提取词嵌入，仅训练其上的 Transformer 文本编码器。Table 4 的消融表明，冻结策略将 APE 均值全局从微调的 1.414 降至 0.976，同时减少了可训练参数量和训练开销。这一发现与直觉相悖——通常微调被认为能更好地适配下游任务——但在此场景下，冻结预训练权重反而保留了更鲁棒的语义表示，避免了对小规模运动-语言数据的过拟合。

### 架构设计的因果机制

上述三个 changed slots 并非孤立改进，而是通过统一的架构设计形成因果闭环：**冻结 DistilBERT 提供稳定的文本语义表示**，**Transformer 编码器将其映射到变分潜在空间**，**非自回归解码器从采样的潜在向量一次性生成完整序列**。其中，Transformer 的全局自注意力机制是解决长期依赖的核心，VAE 的随机采样是赋予多样性的关键，而冻结语言模型则是保证跨模态泛化的稳定锚点。三者缺一不可——消融实验表明，移除任一组件（如去掉 KL 损失项或运动编码器分支）都会导致性能退化，尽管退化幅度远小于将 Transformer 降级为 GRU。

![[assets/figures/papers/paper_list_l19_https_arxiv_org_abs_2204_14109/figures/002_Figure_2.jpg]]
*Figure 2: Method overview: During training, we encode both the motion and text through their respective Transformer encoders, together with modal-specific learnable distribution tokens. The encoder outputs corresponding to these tokens provide Gaussian distribution parameters on which the KL losses are applied and a latent vector z is sampled. Reconstruction losses on the motion decoder outputs further provide supervision for both motion and text branches. In practice, our word embedding consists of a variational encoder that takes input from a pre-trained and frozen DistilBERT [48] model. Trainable layers are denoted in green, the inputs/outputs in brown. At test time, we only use the right branch,...*

TEMOS 的整体框架围绕一个核心设计展开：在**文本与运动两个模态之间构建共享的变分潜在空间**，并通过非自回归的 Transformer 解码器一次性生成完整运动序列。这一设计直接回应了现有方法的两个瓶颈——确定性映射导致输出单一、自回归逐帧解码引发长期漂移和静止姿态。

### 训练流程：双分支对称编码

训练时，文本和运动分别通过各自的 Transformer 编码器进入潜在空间，形成两条对称分支（Figure 2）：

1. **文本分支**：输入文本首先经过**冻结的 DistilBERT** 提取词嵌入 $W_{1:N}$，随后送入**文本 Transformer 编码器**。编码器输出对应一个可学习的“分布令牌”（distribution token），由此得到高斯分布的均值 $\mu^T$ 和协方差 $\Sigma^T$，记为 $\phi^T = \mathcal{N}(\mu^T, \Sigma^T)$。
2. **运动分支**：运动序列 $H_{1:F}$ 经过**运动 Transformer 编码器**，同样通过分布令牌输出运动侧的分布参数 $\phi^M = \mathcal{N}(\mu^M, \Sigma^M)$。

两个分支从各自分布中通过重参数化技巧采样潜在向量 $z^T$ 和 $z^M$，随后共享同一个**运动 Transformer 解码器**，分别重建运动序列 $\hat{H}_{1:F}^T$ 和 $\hat{H}_{1:F}^M$。这种“文本→运动”和“运动→运动”的双支路设计使得模型在缺乏成对数据时仍能从纯运动数据中学习运动先验。

### 潜在空间约束：三重损失驱动对齐

跨模态潜在空间的对齐由三项损失共同约束：

- **重建损失** $\mathcal{L}_{\mathrm{R}}$：对两个分支的重建结果分别施加平滑 L1 损失，确保解码器能从潜在向量准确恢复原始运动：
  $$\mathcal{L}_{\mathrm{R}} = \mathcal{L}_1(H_{1:F}, \hat{H}_{1:F}^M) + \mathcal{L}_1(H_{1:F}, \hat{H}_{1:F}^T)$$

- **KL 散度损失** $\mathcal{L}_{\mathrm{KL}}$：包含四组 KL 散度——文本分布与运动分布之间的双向 KL、以及两者各自与标准正态先验 $\psi = \mathcal{N}(0, I)$ 之间的 KL：
  $$\mathcal{L}_{\mathrm{KL}} = \mathrm{KL}(\phi^T, \phi^M) + \mathrm{KL}(\phi^M, \phi^T) + \mathrm{KL}(\phi^T, \psi) + \mathrm{KL}(\phi^M, \psi)$$
  这既将潜在空间正则化到高斯先验附近，又显式拉近了文本与运动两个模态的分布。

- **嵌入相似性损失** $\mathcal{L}_{\mathrm{E}}$：对采样得到的 $z^T$ 和 $z^M$ 施加 L1 损失，进一步强化跨模态潜在向量的一致性：
  $$\mathcal{L}_{\mathrm{E}} = \mathcal{L}_1(z^T, z^M)$$

总损失为三项的加权和：$\mathcal{L} = \mathcal{L}_{\mathrm{R}} + \lambda_{\mathrm{KL}}\mathcal{L}_{\mathrm{KL}} + \lambda_{\mathrm{E}}\mathcal{L}_{\mathrm{E}}$。

### 推理流程：从文本到多样化运动

推理时仅使用文本分支（Figure 2 右半部分）。给定文本描述，DistilBERT 和文本 Transformer 编码器输出分布 $\phi^T$，从中随机采样潜在向量 $z^T$，运动 Transformer 解码器结合位置编码一次性生成 $F$ 帧的完整运动序列 $\hat{H}_{1:F}$。运动时长由位置编码的数量 $F$ 显式控制。由于 $z^T$ 是随机采样的，同一文本可生成多个符合描述但姿态细节各异的运动变体，这正是 TEMOS 实现多样化的机制。

### 关键设计决策的证据支撑

消融实验为上述设计提供了清晰的因果链：

- **非自回归 Transformer 是最关键的组件**：将 Transformer 替换为 GRU 后，APE 均值全局从 0.976 升至 1.451（Table 3），表明一次性全序列解码相比自回归方式在缓解长期漂移上具有决定性优势。
- **冻结 DistilBERT 优于微调**：冻结语言模型参数时 APE 均值全局为 0.976，微调后升至 1.414（Table 4），说明在数据有限的 KIT 数据集上，保留预训练语言模型的通用语义能力比适配特定领域更有效。
- **变分采样带来显著的多样化增益**：确定性模型 APE 根关节为 1.175，而变分模型生成 10 个样本并选取最佳者可将该指标降至 0.784（Table 2），验证了在共享潜在空间中随机采样能够有效探索符合文本约束的多个合理运动假设。

### 局限性与开放问题

框架存在若干已知局限：KIT 数据集规模有限且词汇不丰富，限制了模型对未见描述的泛化能力；Transformer 的二次复杂度使得直接扩展到数分钟的长序列运动成本过高；未显式建模脚-地面接触，可能导致脚步滑动。这些指向后续工作可探索的方向，包括显式物理约束的整合、运动时长的自动估计，以及面向长序列的架构优化。

### 流水线模块

TEMOS 的架构围绕一个跨模态变分自编码器（VAE）展开，核心由四个模块构成（Figure 2）：

1. **DistilBERT 文本编码器**：接收自然语言描述 $W_{1:N}$，提取冻结的词嵌入。权重在训练中不更新（Table 4 表明冻结优于微调，APE 均值全局从 1.414 降至 0.976）。

2. **文本 Transformer 编码器**：处理词嵌入序列，通过一个可学习的分布 token 输出文本潜在空间的均值 $\mu^T$ 和对角协方差 $\Sigma^T$，定义高斯分布 $\phi^T = \mathcal{N}(\mu^T, \Sigma^T)$。

3. **运动 Transformer 编码器**：与文本编码器对称设计，输入运动序列 $H_{1:F}$，通过另一个分布 token 输出运动潜在空间的分布参数 $\phi^M = \mathcal{N}(\mu^M, \Sigma^M)$。

4. **运动 Transformer 解码器**：从潜在向量 $z \in \mathbb{R}^d$ 和 $F$ 个位置编码出发，非自回归地一次性生成完整运动序列 $\hat{H}_{1:F}$。这是区别于先前自回归逐帧生成方法（如 Ghosh et al.、JL2P）的关键设计。

训练时，文本分支和运动分支共享同一个运动解码器，形成 text-to-motion 和 motion-to-motion 两条重建路径。推理时仅使用文本分支，从 $\phi^T$ 采样 $z$ 即可生成多样化运动。

### 关键公式

**重建损失**（Section 3.3, Equation 1）：
$$\mathcal{L}_{\mathrm{R}} = \mathcal{L}_1(H_{1:F}, \hat{H}_{1:F}^M) + \mathcal{L}_1(H_{1:F}, \hat{H}_{1:F}^T)$$

其中 $\mathcal{L}_1$ 为平滑 L1 损失，$\hat{H}_{1:F}^M$ 和 $\hat{H}_{1:F}^T$ 分别是从运动编码和文本编码经解码器重建的运动序列。两项之和确保两个模态的潜在表示都能准确重建原始运动。

**KL 散度损失**（Section 3.3, Equation 2）：
$$\mathcal{L}_{\mathrm{KL}} = \mathrm{KL}(\phi^T, \phi^M) + \mathrm{KL}(\phi^M, \phi^T) + \mathrm{KL}(\phi^T, \psi) + \mathrm{KL}(\phi^M, \psi)$$

其中 $\psi = \mathcal{N}(0, I)$ 为标准正态先验。前两项拉近文本与运动分布，后两项将各模态分布正则化到先验，共同构建共享的跨模态潜在空间。

**嵌入相似性损失**（Section 3.3, Equation 3）：
$$\mathcal{L}_{\mathrm{E}} = \mathcal{L}_1(z^T, z^M)$$

$z^T \sim \phi^T$ 和 $z^M \sim \phi^M$ 通过重参数化技巧采样得到，该损失直接约束两个模态的采样向量在潜在空间中接近。

**总损失**：
$$\mathcal{L} = \mathcal{L}_{\mathrm{R}} + \lambda_{\mathrm{KL}}\mathcal{L}_{\mathrm{KL}} + \lambda_{\mathrm{E}}\mathcal{L}_{\mathrm{E}}$$

消融实验（Table 3）表明，Transformer 架构本身是最关键的组件（替换为 GRU 后 APE 均值全局从 0.976 升至 1.451），而 KL 损失和嵌入损失的额外贡献相对较小但仍有帮助。

### 评价指标公式

**平均位置误差**（Appendix C, Equation 4）：
$$\mathrm{APE}[j] = \frac{1}{NF} \sum_{n \in N} \sum_{f \in F} \| H_f[j] - \hat{H}_f[j] \|_2$$

衡量生成关节 $j$ 的位置与真值之间的平均 L2 距离，$N$ 为样本数，$F$ 为帧数。

**平均方差误差**（Appendix C, Equation 5）：
$$\mathrm{AVE}[j] = \frac{1}{N} \sum_{n \in N} \| \sigma[j] - \hat{\sigma}[j] \|_2$$

衡量生成运动方差与真实运动方差之间的差异，反映模型是否捕捉到了动作的动态变化范围。

## 实验与关键发现

### 主要定量结果

TEMOS 在 KIT Motion-Language 数据集上与三个先前最先进方法进行了系统比较：**Lin et al. [30]**（序列到序列模型）、**JL2P**（Language2Pose [2]，跨模态嵌入方法）和 **Ghosh et al. [14]**（基于 BERT 的自回归模型）。如表 1 所示，TEMOS 在大多数指标上取得了显著改进，即使仅对每个文本描述随机采样一个运动进行评测。

![[assets/figures/papers/paper_list_l19_https_arxiv_org_abs_2204_14109/figures/003_Table_1.jpg]]
*Table 1: State-of-the-art comparison: We compare our method with recent works [30,2,14], on the KIT Motion-Language dataset [43] and obtain significant improvements on most metrics (values in meters) even if we are sampling a random motion per text conditioning for our model*

具体而言，TEMOS 将根关节平均位置误差（APE root joint）从 Ghosh et al. 的 1.291 m 降至 **0.963 m**（降低 0.328 m），根关节平均方差误差（AVE root joint）从 0.564 m 降至 **0.445 m**，全局轨迹 APE 从 1.242 m 降至 **0.955 m**。值得注意的是，TEMOS 在局部关节的 APE 指标上未表现出明显优势，这表明模型的主要改进集中在全局运动轨迹和根关节的建模精度上。

### 用户感知研究

论文通过两项用户研究（Figure 3）评估了生成运动的语义匹配度和真实感。在语义对应性研究中，用户被要求判断两个生成样本中哪一个更符合输入文本描述，结果显示 TEMOS 相比 Lin et al. 获得 **90.5%** 的偏好率，相比 JL2P 和 Ghosh et al. 也均显著领先。在真实感研究中（不展示文本描述），TEMOS 同样优于所有先前方法。

更引人注目的是，在与真实数据（GT）的直接比较中，TEMOS 的生成结果在 **15.5%** 的情况下被认为语义匹配度优于真实数据，在 **38.5%** 的情况下被认为真实感优于真实数据；而 Ghosh et al. 的对应比例仅为 8.5% 和 5.5%。这一结果说明 TEMOS 的生成质量在感知层面已达到甚至部分超越真实运动数据的水平。

### 消融实验

#### 变分模型与确定性模型

Table 2 对比了确定性版本和变分版本的性能。确定性模型（去除采样机制，直接从学习到的嵌入 token 获得潜在向量）的根关节 APE 为 **1.175 m**。引入 VAE 变分采样后，单次随机采样的 APE 为 0.963 m，而生成 10 个候选并选择最佳者可将 APE 进一步降至 **0.784 m**。这表明变分建模不仅赋予了模型生成多样性的能力，还通过多采样策略显著提升了生成精度——语言描述的模糊性使得“一对多”映射成为必要，而 VAE 恰好提供了从同一文本分布中采样多个合理运动假设的机制。

![[assets/figures/papers/paper_list_l19_https_arxiv_org_abs_2204_14109/figures/006_Table_2.jpg]]
*Table 2: Variational vs deterministic models: We first provide the performance of the deterministic version of our model. We then report results with several settings using our variational model: (i) generating a single motion per text to compare against the ground truth (either randomly or using a zero-vector representing the mean of the Gaussian latent space), and (ii) generating 10 motions per text, each compared against the ground truth separately (either averaging the metrics or taking the motion with the best metric). As expected, TEMOS is able to produce multiple hypotheses where the best candidates improve the metrics*

#### 架构与损失函数

Table 3 的消融实验揭示了各组件的相对重要性。最关键的发现是：将 Transformer 架构替换为 GRU 后，APE 均值全局从 **0.976 m** 飙升至 **1.451 m**，性能退化幅度远超移除任何其他组件。这一证据直接支持了论文的核心设计选择——非自回归的 Transformer 解码器是解决长期漂移和静止姿态问题的决定性因素。相比之下，四项 KL 散度损失项、运动编码器分支和嵌入相似性损失的移除虽然也会导致性能轻微下降，但影响相对有限，属于锦上添花的辅助约束。

![[assets/figures/papers/paper_list_l19_https_arxiv_org_abs_2204_14109/figures/007_Table_3.jpg]]
*Table 3: Architectural and loss study: We conclude that the most critical component is the Transformer architecture, as opposed to a recurrent one (i.e., GRU). While the additional losses are helpful, they bring relatively minor improvements*

#### 语言模型微调

Table 4 显示，冻结预训练的 DistilBERT 参数优于端到端微调：微调后的 APE 均值全局为 **1.414 m**，而冻结状态为 **0.976 m**。这一反直觉的结果可能源于 KIT 数据集规模有限（仅 1784 个训练样本），微调容易导致语言模型的过拟合和灾难性遗忘，而冻结策略保留了大规模预训练学到的鲁棒语义表征。此外，冻结还带来了效率优势——训练时间从 15 小时降至 **4.5 小时**（Appendix D），速度提升约一个数量级。

![[assets/figures/papers/paper_list_l19_https_arxiv_org_abs_2204_14109/figures/008_Table_4.jpg]]
*Table 4: Language model finetuning: We experiment with finetuning the language model (LM) parameters (i.e., DistilBERT [48]) end-to-end with our motion-language cross-modal framework, and do not observe improvements. Here ‘Frozen’ refers to not updating the LM parameters*

#### 其他消融

附录中的补充实验进一步验证了方法的鲁棒性：批次大小在 8 到 32 之间性能最佳（Table A.1）；损失权重中嵌入相似性损失 $\lambda_{\mathrm{E}}$ 对结果的影响大于 KL 损失权重 $\lambda_{\mathrm{KL}}$（Table A.2）；Transformer 的层数和头数在一定范围内对性能不敏感（Table A.3）；更大的语言模型（BERT、RoBERTa）并未带来显著提升（Table A.5）。

### 定性分析

Figure 4 的定性比较展示了 TEMOS 相对于先前方法的视觉质量优势。Lin et al. 的生成运动趋于过度平滑，JL2P 存在明显的脚步滑动问题，Ghosh et al. 则表现出夸张的脚部接触。TEMOS 在这些方面均有改善，生成的运动在语义匹配度和物理合理性上更接近真实数据。Figure 5 展示了同一文本描述的两个不同生成结果，验证了模型在保持语义一致性的前提下能够产生可感知的多样性。

### 失败模式与局限性

尽管 TEMOS 在定量和定性评估中表现优异，论文明确指出了若干局限性：

1. **数据依赖性**：KIT 数据集规模有限且词汇不丰富，模型对未见描述和复杂动作的泛化能力受限于训练分布。
2. **文本鲁棒性不足**：模型无法处理输入文本中的拼写错误或不常见表述，缺乏对噪声输入的容错机制。
3. **长序列扩展困难**：由于 Transformer 的二次复杂度，方法难以直接扩展到数分钟级别的长运动序列，限制了其在长时间交互场景中的应用。
4. **物理约束缺失**：未显式建模脚与地面的接触，可能导致脚步滑动；缺乏物理约束的整合，生成的运动在某些情况下可能违背物理规律。
5. **时长依赖人工指定**：模型需要外部给定运动时长参数 $F$，无法自动估计适宜的运动持续时间。

![[assets/figures/papers/paper_list_l19_https_arxiv_org_abs_2204_14109/figures/016_Table.jpg]]
*Table: A.6: Correspondence between the SMPL-H joints and the MMM framework joints*

## 定位与知识库关联

### 任务定位与基线关系

TEMOS 解决的是**文本到三维人体运动生成**（text-to-motion）任务。在 TEMOS 提出之前，该领域的主流方法存在两个核心瓶颈：一是确定性映射导致单一输出，无法应对自然语言描述的固有模糊性；二是自回归逐帧解码容易出现长期漂移和静止姿态退化。

TEMOS 的直接对比基线包括三类代表性工作：

- **Lin et al. [30]**：基于序列到序列（seq2seq）模型，生成结果存在过度平滑的问题，运动细节丢失严重。
- **JL2P (Language2Pose) [2]**：采用跨模态嵌入方法，将文本和运动映射到共享空间，但生成的运动常出现脚步滑动（foot sliding）。
- **Ghosh et al. [14]**：基于 BERT 和自回归模型，在语义匹配上有所改进，但存在夸张的脚部接触（exaggerated foot contacts）问题，且自回归架构导致训练效率低下。

TEMOS 在上述基线的基础上做出了三个关键改变：

| 设计维度 | 基线做法 | TEMOS 做法 | 证据锚点 |
|---------|---------|-----------|---------|
| 序列解码方式 | 自回归逐帧生成 | 非自回归一次性全序列生成 | Section 1 |
| 生成模式 | 确定性单输出 | 基于 VAE 的随机多样化生成 | Section 3.2 |
| 文本编码器 | 微调的 BERT 或 word2vec | 冻结的 DistilBERT | Table 4 |

这三个改变之间存在因果耦合：**非自回归解码**解决了长期漂移问题，使训练速度提升一个数量级（4.5 小时对比 15 小时，见 Appendix D）；**VAE 变分采样**使得同一文本可生成多个符合语义的运动变体，并通过采样 10 个候选取最佳的方式将根关节 APE 从 1.175 降至 0.784（Table 2）；**冻结 DistilBERT** 则避免了微调带来的过拟合，将 APE 均值全局从 1.414 降至 0.976（Table 4）。消融实验进一步表明，Transformer 架构本身是最关键的组件——将其替换为 GRU 后，APE 从 0.976 飙升至 1.451（Table 3），而 KL 散度损失和嵌入相似性损失虽有益处，但贡献相对次要。

### 适用边界与局限

TEMOS 的设计决策决定了其适用范围和固有局限：

1. **数据规模与词汇覆盖**：模型在 KIT Motion-Language 数据集上训练，该数据集仅包含 3911 个运动序列和 6353 条文本描述，词汇丰富度有限。这导致模型对未见描述和复杂动作的泛化能力受限，无法处理输入文本中的拼写错误或不常见表述。

2. **序列长度限制**：Transformer 解码器的二次复杂度使得模型难以直接扩展到非常长的运动序列（如数分钟的运动）。当前方案依赖人为指定生成时长，缺乏自动估计适宜运动时长的机制。

3. **物理真实感缺失**：模型未显式建模脚与地面的接触约束，导致生成的运动中可能出现脚步滑动；缺乏物理约束的整合，运动可能在某些情况下违背物理规律。这与 Ghosh et al. [14] 中出现的夸张脚部接触问题是同一类底层缺陷——纯数据驱动方法难以隐式学到物理约束。

4. **文本编码器的冻结策略**：虽然冻结 DistilBERT 在 KIT 数据集上表现更好，但这也意味着模型无法利用运动数据反向优化文本表示，可能限制了在更大规模、更多样化文本上的适应能力。

### 开放问题

TEMOS 留下了一系列有待后续工作探索的问题：

- **物理与接触建模**：如何显式地建模人与环境的接触和物理约束，以提高运动真实感？这涉及将物理模拟或接触损失函数集成到生成框架中。
- **时长自适应**：能否自动估计生成运动的适宜时长，而不是依赖人为指定？这需要模型学会从文本语义中推断动作的持续范围。
- **长序列扩展**：在处理长序列运动时，如何克服 Transformer 的二次复杂度，使其适用于实时交互场景？可能的路径包括稀疏注意力机制或分层生成策略。
- **语言理解深化**：如何将方法扩展到更丰富的语言输入（如长时间指令、多句描述）并保持生成质量？这要求模型具备更强的时序语义解析能力。
- **评估指标改进**：如何量化多样性与真实感，并设计更能反映人类感知的评价指标？当前的 APE/AVE 指标主要衡量与单一 ground truth 的偏差，无法充分评估生成多样性。用户感知研究（Figure 3）虽然提供了有价值的补充，但成本高昂且难以标准化。

需要指出的是，TEMOS 在用户感知研究中甚至在某些情况下被评价为优于真实数据（15.5% 的语义匹配偏好和 38.5% 的真实感偏好，见 Figure 3），这一反直觉结果可能源于 KIT 数据集中真实运动本身存在噪声或不够自然，而非 TEMOS 真的超越了物理真实——该点需要结合数据集质量进行审慎解读。

## 原文 PDF

![[paperPDFs/ECCV_2022/TEMOS_Generating_diverse_human_motions_from_textual_descriptions.pdf]]
