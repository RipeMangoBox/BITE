---
title: "MotionCritic: Aligning Human Motion Generation with Human Perceptions"
type: paper
paper_level: A
venue: ICLR
year: 2025
pdf_ref: paperPDFs/ICLR_2025/MotionCritic_Aligning_Human_Motion_Generation_with_Human_Perceptions.pdf
aliases:
- MotionCritic
tags:
- ICLR_2025
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "基于大规模人工偏好比较数据训练的数据驱动运动质量评价模型。"
primary_logic: "利用数万组成对的人类偏好标注数据训练一个“评价器”模型，该模型可以学会与人类感知一致的隐式质量标准，从而不仅提供更准确的自动评价指标，还能作为轻量级微调信号直接提升生成器输出的质量。"
claims:
- "在感知评价测试集上，MotionCritic 的准确率显著优于所有基线指标，在 MDM 子集上达到 85.07%，而最佳启发式指标仅为 71.78%。"
- "MotionCritic 具有良好的跨域泛化能力，在未见过的 FLAME 生成数据上的准确率仍高达 81.43%。"
- "将评价器分数作为微调监督信号后，用户研究中生成运动的 Elo 评分随微调步数持续上升，表明运动质量的主观提升。"
- "在真实 GT 运动分布上，评价器分数与人类 Elo 评分高度单调一致，而 FID 指标则无法反映这种偏好。"
---

# MotionCritic: Aligning Human Motion Generation with Human Perceptions

> [!tip] 核心洞察
> 利用数万组成对的人类偏好标注数据训练一个“评价器”模型，该模型可以学会与人类感知一致的隐式质量标准，从而不仅提供更准确的自动评价指标，还能作为轻量级微调信号直接提升生成器输出的质量。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | MotionCritic: 将人体运动生成与人类感知对齐 |
| 英文题名 | MotionCritic: Aligning Human Motion Generation with Human Perceptions |
| 会议/期刊 | ICLR 2025 |
| Links | [paper](https://arxiv.org/pdf/2407.02272); [Project](https://motioncritic.github.io/) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | MotionCritic |
| Dataset | MotionPercept (MDM 子集), MotionPercept (FLAME 子集, 跨域), HumanAct12 GT test set (主观一致性) |

> [!tip] 效果简介
> - MotionPercept (MDM 子集) 上，Accuracy (%) 为 85.07，对比 71.78 (Person-Ground Contact)，变化 +13.29。
> - MotionPercept (FLAME 子集, 跨域) 上，Accuracy (%) 为 81.43，对比 69.82 (Person-Ground Contact)，变化 +11.61。
> - HumanAct12 GT test set (主观一致性) 上，Elo 评分与分数的单调性 为 与人类 Elo 评分高度正相关，对比 FID 指标与人类评分几乎无关，变化 显著提升。

## 概述

### 问题瓶颈

现有的人体运动生成评估指标与人类感知之间存在显著脱节。无论是基于真值配对的直接距离度量（如 Root AVE、Joint AE）、基于运动平滑性的启发式规则（如 Jerk、Acceleration），还是基于脚步触地/穿地规则的物理约束（如 Person-Ground Contact、PFC），都依赖预定义的评价标准，无法在实例级别可靠地反映生成运动的质量。分布距离指标（如 FID）虽然被广泛使用，但实验表明其与人类主观评分几乎无关（Figure 4(B)）。此前基于学习的小规模评价器 MoBERT（Voas et al., 2023）仅使用了约 1.4K 的人工评分，数据规模限制了其泛化能力。这些指标的共同缺陷导致生成模型的优化目标与人类感知质量之间缺乏有效对齐。

### 核心思路

MotionCritic 的核心洞察是：利用大规模人类偏好比较数据训练一个数据驱动的运动质量评价器，使其学会与人类感知一致的隐式质量标准。该评价器不仅可作为更准确的自动评价指标，还能作为轻量级微调信号直接提升生成器输出的主观质量。

具体而言，方法包含三个关键环节：

1. **MotionPercept 数据集构建**：利用多种生成模型产生运动候选，通过人工多项选择偏好标注，收集了包含 52,563 对偏好的大规模数据集，数据规模远超此前工作。
2. **MotionCritic 评价器训练**：以 DSTformer 为骨干网络，将 SMPL 运动序列映射为标量分数，通过基于 Bradley-Terry 模型的成对对数损失 $\mathcal{L}_{\mathrm{Percept}} = - \mathbb{E}[\log \sigma(\mathcal{C}(\mathbf{x}^{(h)}) - \mathcal{C}(\mathbf{x}^{(l)}))]$ 学习人类感知偏好。
3. **评价器监督的生成微调**：在 MDM 扩散模型的去噪过程中，通过评价器对预测运动打分，结合 KL 散度正则项 $\mathcal{L}_{\mathrm{FT}} = \mathcal{L}_{\mathrm{MDM}} + \lambda \mathcal{L}_{\mathrm{Critic}} + \mu \mathcal{L}_{\mathrm{KL}}$，以极低的计算开销提升生成运动的主观质量。

### 方法定位

在方法谱系中，MotionCritic 将运动质量评估从“预定义规则驱动”范式转变为“数据驱动的人类感知对齐”范式。与依赖配对真值的距离度量、基于物理先验的启发式规则、以及衡量分布相似度的 FID 等传统方法不同，MotionCritic 直接从人类偏好比较中学习隐式的质量评价函数。在知识库定位上，该方法桥接了运动生成、感知评价和偏好学习三个领域，借鉴了 Bradley-Terry 偏好建模框架，并将其应用于人体运动的感知质量评估这一新场景。

### 主要结果

在 MotionPercept 测试集上，MotionCritic 的感知评价准确率达到 85.07%（MDM 子集），显著优于最佳启发式指标 Person-Ground Contact 的 71.78%（Table 1）。在跨域泛化测试中，评价器在未见过的 FLAME 生成数据上仍达到 81.43% 的准确率。在真实 GT 运动分布上，评价器分数与人类 Elo 评分高度单调一致，而 FID 指标无法反映这种偏好（Figure 4(B)）。将评价器作为微调监督信号后，用户研究中生成运动的 Elo 评分随微调步数持续上升，验证了该方法对生成质量的主观提升效果（Figure 5）。

### 局限与开放问题

当前方法存在若干局限：评价器仅支持固定 60 帧运动输入，对不同序列长度需插值或截断，鲁棒性有待提升；学习到的评价函数表现出非光滑的能量景观，给基于梯度的优化带来挑战；评价器只能给出全局质量分数，缺乏关节级、时间级的细粒度反馈。开放问题包括：如何设计更细粒度的感知评价方法以获得更丰富的训练信号，如何将生物力学约束显式融入评价模型，以及如何借鉴强化学习的优化策略来应对非平滑评价器景观下的生成优化。

## 背景与动机

### 问题背景

人体运动生成是计算机视觉与图形学中的核心任务，广泛应用于动画制作、虚拟人交互和机器人仿真等领域。近年来，基于扩散模型（如 **MDM**，Tevet et al., 2023）和自回归模型等生成范式的发展，使得合成运动的多样性和流畅性得到了显著提升。然而，生成运动的质量评估始终是一个悬而未决的瓶颈问题。

### 现有评估方法的根本缺陷

当前主流的运动质量评估手段可归为三类，但均与人类的主观感知存在系统性脱节：

1.  **基于真值配对的直接距离度量**：如 Root AVE / Root AE、Joint AVE / Joint AE 等指标，要求生成运动与真实运动逐帧对齐。这不仅在多数生成场景中缺乏可用的真值参照，而且距离误差本身无法反映运动的物理合理性或风格优劣。

2.  **基于启发式规则的指标**：如 Jerk / Acceleration（平滑性）、Person-Ground Contact / Foot-Floor Penetration（脚步触地/穿地规则，Rempe et al., 2021）以及 Physical Foot Contact（PFC，Tseng et al., 2023）。这些规则只能捕捉有限的、预定义的物理约束，难以覆盖人类感知中复杂的质量维度（如动作的自然度、协调性、风格一致性）。

3.  **基于分布距离的指标**：如 FID（Fréchet Inception Distance），在整体分布层面比较生成运动与真实运动的差异，但无法在实例级别提供可靠的质量判断。实验表明，FID 与人类通过 Elo 评分表达的主观偏好几乎无关（Figure 4(B)），这意味着一个 FID 更低的模型未必能生成人类认为更好的运动。

此前虽有基于学习的小规模评价器尝试（如 **MoBERT**，Voas et al., 2023），但其训练数据仅包含约 1.4K 的人类评分，规模不足，难以泛化到多样化的生成场景。

### 核心动机

上述缺陷揭示了一个根本性的因果瓶颈：**缺乏一个在实例级别与人类感知对齐的自动评价信号，既无法可靠地衡量生成质量，也无法直接作为监督信号反馈给生成模型以提升其输出。**

这一瓶颈催生了两个核心动机：

-   **构建大规模人类感知偏好数据集**：需要一个覆盖多种生成范式、动作类别和退化模式的大规模人工标注数据集，为学习感知对齐的评价模型提供充分的训练信号。
-   **训练数据驱动的运动评价器并用于生成优化**：利用该数据集训练一个神经网络评价器，使其学会隐式编码人类感知的质量标准，并进一步将该评价器作为轻量级微调信号，直接提升现有生成器的输出质量。

### 本文的解决思路

针对上述动机，本文提出了 **MotionCritic** 框架，其核心思路包含三个递进的模块：

1.  **MotionPercept 数据集**：利用 MDM 和 FLAME 等生成模型产生运动候选，通过人工多项选择偏好标注，构建包含 52,563 对偏好的大规模数据集，规模较 MoBERT 提升数十倍。
2.  **MotionCritic 评价器**：以 DSTformer 为骨干网络，将 SMPL 运动序列映射为标量质量分数，通过 Bradley-Terry 模型的成对对数损失学习人类偏好。
3.  **评价器监督的生成微调**：在 MDM 扩散模型的去噪过程中，引入评价器对预测运动的打分作为监督信号，结合 KL 散度正则项，以极低的计算开销提升生成运动的主观质量。

## 核心创新

MotionCritic 的核心创新在于**将人体运动质量的评估从“规则定义”范式切换为“数据驱动的感知对齐”范式**，并进一步将这种对齐后的评价能力转化为生成模型的直接监督信号。具体体现在以下三个关键维度的改变：

### 1. 评价范式：从启发式规则到大规模感知偏好学习

现有运动评价指标依赖两类路径：一是基于真值配对的距离度量（如 Root AVE、NPSS、NDMS），它们隐含假设“越接近真值越好”，但无法捕捉运动的主观自然度；二是基于物理或运动学的启发式规则（如 Jerk、Person-Ground Contact、PFC），这些规则只能检测有限的、预定义的缺陷类型。

MotionCritic 的核心改变在于：**直接学习人类对运动质量的隐式判断标准**。作者构建了 MotionPercept 数据集，包含 52563 组成对的人类偏好标注——这一规模远超此前唯一的同类工作 MoBERT（Voas et al., 2023）的 1.4K 标注。基于 Bradley-Terry 模型，评价器通过成对对数损失进行训练：

$$\mathcal{L}_{\mathrm{Percept}} = - \mathbb{E}_{(\mathbf{x}^{(h)},\mathbf{x}^{(l)})\sim\mathcal{D}} \left[ \log \sigma \left( \mathcal{C}(\mathbf{x}^{(h)}) - \mathcal{C}(\mathbf{x}^{(l)}) \right) \right]$$

该损失鼓励高质量样本的标量分数严格高于低质量样本，使评价器学会一个与人类感知单调一致的评分函数。这种范式转变的因果效应是：评价器不再需要预定义“什么是好的运动”，而是从数万次人类比较中隐式地归纳出质量标准。

### 2. 监督信号：从分布匹配到实例级质量反馈

传统生成模型训练依赖于扩散损失 $\mathcal{L}_{\mathrm{MDM}}$，其目标是最大化数据似然，但这一目标与人类感知质量之间并无直接关联。MotionCritic 的创新在于**将评价器分数作为实例级监督信号注入生成过程**：

$$\mathcal{L}_{\mathrm{FT}} = \mathcal{L}_{\mathrm{MDM}} + \lambda \mathcal{L}_{\mathrm{Critic}} + \mu \mathcal{L}_{\mathrm{KL}}$$

其中评价器监督损失 $\mathcal{L}_{\mathrm{Critic}}$ 对预测去噪运动 $\mathbf{x}_0'$ 的质量进行打分，并通过 $\phi(s) = -\sigma(\tau - s)$ 映射为损失信号——当分数高于阈值 $\tau$ 时损失趋于零，避免过度优化。KL 正则项 $\mathcal{L}_{\mathrm{KL}}$ 则约束当前迭代结果不偏离上一轮过远，保持生成多样性。

这一设计的精巧之处在于：**只需极少的微调步数（数百步），就能在用户研究中持续提升 Elo 评分**，而 FID 等分布距离指标在此过程中几乎不变，再次印证了分布匹配与感知质量之间的脱节。

### 3. 评价器能力的证据强度

评价器学习到的质量标准在多个维度展现出强因果效力：

- **感知对齐准确率**：在 MotionPercept 的 MDM 子集上达到 85.07%，显著优于最佳启发式指标 Person-Ground Contact 的 71.78%（Table 1）；在跨域 FLAME 子集上仍保持 81.43%，证明其泛化能力。
- **与人类偏好的单调一致性**：在真实 GT 运动分布上，评价器分数与人类 Elo 评分高度正相关，而 FID 则完全无法反映这种偏好排序（Figure 4(B)）。
- **信息完备性**：消融实验表明，移除 MotionCritic 特征后 SVM 分类准确率从 82.49% 骤降至 66.52%（Table 14）；集成学习中仅使用评价器分数即可达到 84.96%，加入其他启发式特征提升微乎其微（Table 12-13），说明评价器已捕捉了主要的感知知识。

这些证据共同表明：MotionCritic 不仅是一个更准确的评价指标，更是一个**可迁移的感知质量模型**，其学到的隐式标准超越了任何单一启发式规则的表达能力。

## 整体框架

MotionCritic 的整体框架围绕一个核心发现展开：现有运动生成评估指标与人类感知之间存在系统性的脱节。无论是基于真值配对的距离误差（如 Root AE、Joint AVE）、运动平滑性启发式规则（Jerk、Acceleration），还是分布距离（FID），都无法在实例级别可靠地反映生成运动的主观质量。MotionCritic 通过三个紧密耦合的模块来解决这一问题。

**模块一：MotionPercept 数据集构建。** 框架的第一步是获取大规模的人类感知偏好数据。研究者利用预训练的运动生成模型（MDM 和 FLAME）产生多样化的运动候选，通过多项选择题的方式收集人工标注——受试者从 6 个生成运动选项中选出质量最佳的一个。最终构建的 MotionPercept 数据集包含 52,563 对偏好标注，规模是此前类似工作 MoBERT（Voas et al., 2023，约 1.4K 标注）的数十倍。感知一致性实验表明，82.37% 的问题中 10 名受试者达成完全一致，所有受试者之间的成对一致性高达 90%，这为后续训练提供了可靠的监督信号。

**模块二：MotionCritic 评价器训练。** 框架的核心是一个将运动序列映射为标量质量分数的神经网络评价器 $\mathcal{C}$。以 DSTformer 为骨干网络（3 层、8 个注意力头），输入为 SMPL 运动参数序列，输出为单一标量分数 $s$。训练目标基于 Bradley-Terry 模型：给定一对人类标注的偏好数据 $(\mathbf{x}^{(h)}, \mathbf{x}^{(l)})$，其中 $\mathbf{x}^{(h)}$ 是人类偏好的高质量运动，$\mathbf{x}^{(l)}$ 是低质量运动，评价器通过成对对数损失学习使 $\mathbf{x}^{(h)}$ 的分数高于 $\mathbf{x}^{(l)}$：

$$\mathcal{L}_{\mathrm{Percept}} = - \mathbb{E}_{(\mathbf{x}^{(h)},\mathbf{x}^{(l)})\sim\mathcal{D}} \left[ \log \sigma \left( \mathcal{C}(\mathbf{x}^{(h)}) - \mathcal{C}(\mathbf{x}^{(l)}) \right) \right]$$

这一设计使评价器从大规模比较数据中隐式地学习与人类感知一致的复杂质量标准，而非依赖任何预定义的启发式规则。

**模块三：评价器监督的生成微调。** 训练好的 MotionCritic 不仅可作为离线评估指标，还能直接嵌入生成模型的训练循环。以预训练的 MDM 扩散模型为基线，在去噪过程的随机时间步 $t$ 处截取单步预测去噪运动 $\mathbf{x}_0'$，将其输入评价器获得监督信号：

$$\mathcal{L}_{\mathrm{Critic}} = \mathbb{E}_{y_i\sim y} \left[ \phi(\mathcal{C}(\mathbf{x}_0')) \right], \quad \phi(s) = -\sigma(\tau - s)$$

其中 $\tau$ 为分数阈值（设为 12.0），当评价器分数超过该阈值时损失趋于零，避免模型单纯追求极端高分。同时引入 KL 散度正则项 $\mathcal{L}_{\mathrm{KL}}$，约束当前迭代的去噪结果不偏离上一轮结果过远，以保持与原任务的一致性。最终微调损失为三者加权组合：

$$\mathcal{L}_{\mathrm{FT}} = \mathcal{L}_{\mathrm{MDM}} + \lambda \mathcal{L}_{\mathrm{Critic}} + \mu \mathcal{L}_{\mathrm{KL}}$$

这一微调方案的计算开销极低，仅需数百步即可显著提升生成运动的主观质量。

三个模块之间的因果链路清晰：MotionPercept 提供人类感知的“金标准”训练数据，MotionCritic 将这种感知知识压缩为可微分的标量评价函数，而微调模块则利用该函数的梯度信号直接优化生成器，使输出运动与人类偏好的对齐程度持续提升。

## 核心模块与公式推导

MotionCritic 的核心由两个关键模块构成：一个基于成对偏好学习的运动评价器，以及一个将评价器作为监督信号的生成器微调框架。以下分别阐述其设计逻辑与数学形式。

### 运动评价器：从人类偏好到标量分数

评价器的目标是学习一个映射 $\mathcal{C}(\mathbf{x}) \rightarrow s$，将高维运动参数 $\mathbf{x}$ 压缩为一个与人类感知对齐的标量质量分数 $s$。其核心挑战在于，人类对运动质量的判断本质上是相对的、比较性的，而非绝对的数值评分——这正是传统指标（如距离误差、FID）与人类感知脱节的根源。

为此，MotionCritic 采用 **Bradley-Terry 偏好模型** 作为训练框架。给定一对运动样本 $(\mathbf{x}^{(i)}, \mathbf{x}^{(j)})$，假设人类感知模型 $\mathcal{H}$ 更偏好 $\mathbf{x}^{(i)}$，则评价器 $\mathcal{C}$ 应给出 $\mathcal{C}(\mathbf{x}^{(i)}) > \mathcal{C}(\mathbf{x}^{(j)})$。训练目标为最大化评价器与人类判断一致的联合概率：

$$
\arg \max_{\mathcal{C}} \mathbb{E}_{(\mathbf{x}^{(i)},\mathbf{x}^{(j)})\sim\mathcal{D}} \left[ \log \sigma \left( (\mathcal{C}(\mathbf{x}^{(i)})-\mathcal{C}(\mathbf{x}^{(j)})) \cdot (\mathcal{H}(\mathbf{x}^{(i)})-\mathcal{H}(\mathbf{x}^{(j)})) \right) \right] \tag{1}
$$

其中 $\sigma$ 为 sigmoid 函数，$\mathcal{H}(\mathbf{x}^{(i)})-\mathcal{H}(\mathbf{x}^{(j)})$ 取值为 $+1$ 或 $-1$，表示人类偏好的方向。在实际实现中，数据集 $\mathcal{D}$ 直接提供“更好”样本 $\mathbf{x}^{(h)}$ 与“更差”样本 $\mathbf{x}^{(l)}$ 的配对，因此训练损失简化为成对对数损失：

$$
\mathcal{L}_{\mathrm{Percept}} = - \mathbb{E}_{(\mathbf{x}^{(h)},\mathbf{x}^{(l)})\sim\mathcal{D}} \left[ \log \sigma \left( \mathcal{C}(\mathbf{x}^{(h)}) - \mathcal{C}(\mathbf{x}^{(l)}) \right) \right] \tag{2}
$$

该损失的核心机制是：当 $\mathcal{C}(\mathbf{x}^{(h)}) \gg \mathcal{C}(\mathbf{x}^{(l)})$ 时，$\sigma$ 趋近于 1，损失趋近于 0；当分数关系颠倒时，损失急剧增大。这使得评价器无需显式定义“好运动”的规则，而是从数万对人工标注中隐式习得感知标准。

评价器骨干网络采用 **DSTformer**（Zhu et al., 2023），配置为 3 层、8 个注意力头，以 SMPL 姿态参数序列为输入，输出单一标量分数。

### 评价器监督的生成微调

将评价器用于提升生成质量时，直接最大化 $\mathcal{C}(\mathbf{x})$ 会导致模型“作弊”——生成评价器认为高分但实际失真或偏离文本条件的运动。MotionCritic 通过两个关键设计解决这一问题。

**评价器监督损失** 采用带阈值的映射函数，避免对已足够好的运动继续施加优化压力：

$$
\mathcal{L}_{\mathrm{Critic}} = \mathbb{E}_{y_i\sim y} \left[ \phi(\mathcal{C}(\mathbf{x}_0')) \right], \quad \phi(s) = -\sigma(\tau - s) \tag{4}
$$

其中 $\mathbf{x}_0'$ 是扩散模型在随机时间步 $t$ 的单步去噪预测结果，$\tau$ 为分数阈值（设为 12.0）。当 $\mathcal{C}(\mathbf{x}_0') \gg \tau$ 时，$\phi(s) \to 0$，损失消失；当分数低于阈值时，损失产生梯度信号推动生成器改进。这种“软饱和”设计是维持微调稳定性的关键——消融实验表明，不加裁剪会导致模型单纯追求高分而造成性能退化。

**KL 散度正则项** 约束当前迭代的去噪结果不偏离上一轮过远，防止微调破坏原始生成能力：

$$
\mathcal{L}_{\mathrm{KL}} = \mathbb{E}_{y_i\sim\mathcal{V}} \left[ D_{\mathrm{KL}}\left( p(\mathbf{x}_0') \| p(\widetilde{\mathbf{x}_0'}) \right) \right] \tag{5}
$$

其中 $\widetilde{\mathbf{x}_0'}$ 为上一微调步骤中相同时间步的去噪预测，$\mathcal{V}$ 为验证集。该正则项确保生成器在追求更高感知质量的同时，保持与原始任务（文本到运动）的一致性。

**微调总损失** 将上述组件与原始扩散损失组合：

$$
\mathcal{L}_{\mathrm{FT}} = \mathcal{L}_{\mathrm{MDM}} + \lambda \mathcal{L}_{\mathrm{Critic}} + \mu \mathcal{L}_{\mathrm{KL}} \tag{6}
$$

其中 $\mathcal{L}_{\mathrm{MDM}}$ 为预训练 MDM（Tevet et al., 2023）的标准扩散损失，$\lambda$ 和 $\mu$ 为平衡系数。前向扩散过程遵循标准马尔可夫加噪：

$$
q(\mathbf{x}_t | \mathbf{x}_{t-1}) = \mathcal{N}(\sqrt{\alpha_t}\mathbf{x}_{t-1}, (1-\alpha_t)I) \tag{3}
$$

该微调框架的计算开销极低——仅需在随机采样的去噪时间步插入一次评价器前向传播，即可在数百步内显著提升生成运动的主观质量。

## 实验与分析

### 主实验：感知评价准确率

MotionCritic 的核心验证是在 MotionPercept 测试集上直接衡量其与人类偏好的对齐程度。评价指标为二选一成对比较的准确率（Accuracy）和对数损失（Log Loss）。Table 1 汇总了与 11 种基线指标的定量对比，结果如下：

![[assets/figures/papers/paper_list_l42_https_arxiv_org_pdf_2407_02272/figures/004_Table_1.jpg]]
*Table 1: Quantitative comparison of motion evaluation metrics on MDM and FLAME testsets of MotionPercept*

- **MDM 子集（域内）**：MotionCritic 达到 **85.07%** 的准确率，而最佳启发式指标 Person-Ground Contact 仅为 71.78%，提升幅度达 **+13.29%**。对数损失方面，MotionCritic 取得 0.5486，远低于第二名 PFC 的 0.7061。
- **FLAME 子集（跨域泛化）**：在未见过的 FLAME 生成数据上，MotionCritic 准确率仍保持在 **81.43%**，领先最佳基线（Person-Ground Contact 的 69.82%）**+11.61%**，对数损失为 0.5758。
- **细粒度动作类别**：在 HumanAct12 的 12 个动作类别上，MotionCritic 在绝大多数类别中均保持领先，整体准确率 85.07%，而其他指标在不同类别上波动剧烈（Table 5, Table 6）。

这些结果表明，基于大规模人类偏好数据训练的神经评价器能够捕捉到传统距离度量、启发式规则和分布距离所无法反映的感知维度。

### 与人类偏好的单调一致性

为了验证评价器分数是否真正与人类主观感受保持单调关系，研究者在 HumanAct12 真实运动（GT）上进行了用户研究。首先依据 MotionCritic 分数将 GT 测试集从高到低分为五个子集（GT-I 至 GT-V），然后通过用户研究计算每个子集的 Elo 评分。

Figure 4(B) 揭示了关键发现：**MotionCritic 的平均分数与人类 Elo 评分高度正相关**，而广泛使用的 FID 指标则与人类偏好几乎无关——FID 在不同 GT 子集间几乎保持不变。这直接证明了 FID 等分布距离指标在实例级别的质量评价上存在根本性缺陷，而 MotionCritic 则有效填补了这一空白。

### 生成器微调实验

MotionCritic 的另一项核心功能是作为生成器的监督信号。研究者以预训练的 **MDM**（Tevet et al., 2023）为基线，使用公式

$$\mathcal{L}_{\mathrm{FT}} = \mathcal{L}_{\mathrm{MDM}} + \lambda \mathcal{L}_{\mathrm{Critic}} + \mu \mathcal{L}_{\mathrm{KL}}$$

进行轻量微调。关键实验结果如下：

- **用户研究**：Figure 5(A) 的胜率矩阵和 Figure 5(B) 的 Elo 评分曲线均显示，随着微调步数增加（0 → 200 → 400 → 600），生成运动的主观质量持续上升。600 步微调后的模型在用户研究中显著优于未微调基线。
- **自动指标**：Table 2 显示，微调至 600 步时，生成运动的 Accuracy 提升至 0.98，Diversity 为 6.68，Multimodality 为 2.42，表明质量提升并未以牺牲多样性为代价。
- **直观对比**：Figure 6 展示了不同微调步数下的生成结果，可见随着微调进行，运动中的伪影（如脚部滑动、不自然姿态）逐渐减少。

![[assets/figures/papers/paper_list_l42_https_arxiv_org_pdf_2407_02272/figures/008_Figure_6.jpg]]
*Figure 6: Motion generation results from different fine-tuning steps*

![[assets/figures/papers/paper_list_l42_https_arxiv_org_pdf_2407_02272/figures/009_Table_2.jpg]]
*Table 2: Comparison of motion generation metrics at different fine-tuning steps*

值得注意的是，FID 在微调过程中并未呈现单调改善趋势（Figure 5(B)），再次印证了 FID 与人类感知之间的脱节。

### 消融与诊断分析

**评价器分数的信息量**。在 SVM 分类实验中，当仅使用 MotionCritic 分数作为特征时，准确率为 82.49%；移除该特征后，准确率骤降至 66.52%（Table 13, Table 14）。这说明评价器分数包含了远超其他启发式特征的感知信息。

**集成学习的边际收益**。仅使用 MotionCritic 分数的 MLP 集成模型即可达到 84.96% 的准确率，加入其他启发式特征后仅微升至 85.17%（Table 12）。这一微小增益表明，MotionCritic 已经捕捉了人类感知评价所需的主要知识，其他特征提供的增量信息极为有限。

**分数裁剪的必要性**。在微调过程中，对评价器分数进行裁剪（阈值 τ=12.0）至关重要。不加裁剪会导致模型单纯追求极端高分，反而造成生成质量退化。这一机制通过损失函数中的 φ(s) = −σ(τ − s) 实现：当分数超过 τ 时，损失趋于零，防止过度优化。

**评价器能量景观的非光滑性**。通过对评价器输入施加不同尺度的高斯噪声扰动，研究者发现：随着噪声增大，评价准确率平滑下降，但评价器函数的“非光滑”（bumpy）特性可能给基于梯度的优化带来挑战（Figure 11）。这意味着直接使用评价器梯度指导生成时，优化过程可能陷入局部最优，需要配合 KL 正则项等措施来稳定训练。

![[assets/figures/papers/paper_list_l42_https_arxiv_org_pdf_2407_02272/figures/021_Figure_11.jpg]]
*Figure 11: Sensitivity analysis results. (A) Accuracy vs noise-scale curve. (B) Average and standard deviation of critic scores vs noise-scale*

### 失败模式与局限性

1. **序列长度敏感性**：评价器在标准 60 帧运动上表现最佳；对于非标准长度运动，需进行插值或截断预处理，性能会有所下降（Figure 13）。模型在不同序列长度上的鲁棒性仍有提升空间。

![[assets/figures/papers/paper_list_l42_https_arxiv_org_pdf_2407_02272/figures/026_Figure_13.jpg]]
*Figure 13: Performance of the Critic model across different motion lengths and interpolations. For shorter motions, two pre-processing approaches were evaluated*

2. **粒度不足**：当前评价器仅输出全局标量分数，无法提供时间维度或关节维度的细粒度反馈。这意味着它能够判断“哪段运动更好”，但难以精确诊断“哪个时刻、哪个关节出现了问题”。

3. **泛化边界未充分验证**：训练数据仅覆盖有限的动作类别和生成方式（MDM、FLAME），对极端罕见动作或全新生成范式的泛化性尚需进一步检验。

4. **物理合理性未显式建模**：评价器通过人类偏好数据隐式学习质量标准，但未显式融入生物力学约束（如关节角度限制、力矩平衡）。在某些情况下，高评价器分数的运动仍可能违反物理规律。

### 补充图表

![[assets/figures/papers/paper_list_l42_https_arxiv_org_pdf_2407_02272/figures/002_Figure_2.jpg]]
*Figure 2: We conduct a perceptual consensus experiment with 10 subjects on 312 multiple-choice questions, each with 6 options. (A): The distribution of the number of supporters for the most chosen option in each question. (B): Distribution of the number of options chosen by all subjects for each question. (C): Pairwise agreement ratio of all subjects*

![[assets/figures/papers/paper_list_l42_https_arxiv_org_pdf_2407_02272/figures/032_Figure_14.jpg]]
*Figure 14: Metrics’ venn fiagram and SHAP values*

![[assets/figures/papers/paper_list_l42_https_arxiv_org_pdf_2407_02272/figures/033_Figure_15.jpg]]
*Figure 15: Fine-tuning process. (A): Critic score in 1000-step denoising process. (B): Critic output in 800-step fine-tuning process. (C): Full finetuning process of our strategy based on ReFL (Xu et al., 2024) and 1-step back-propagation based on DRaFT-LV (Clark et al., 2024)*

![[assets/figures/papers/paper_list_l42_https_arxiv_org_pdf_2407_02272/figures/034_Figure_16.jpg]]
*Figure 16: Visualization of critic scores on fine-tuning experiments. (A): Fine-tuning 400 steps with and without MotionCritic supervision compared. (B): Fine-tuning with 400 and 800 steps compared*

![[assets/figures/papers/paper_list_l42_https_arxiv_org_pdf_2407_02272/figures/035_Figure_17.jpg]]
*Figure 17: Results from fine-tuning process. (A): Elo ratings and Critic scores. (B): FID, PFC(Tseng et al., 2023), Multimodality and Critic scores*

![[assets/figures/papers/paper_list_l42_https_arxiv_org_pdf_2407_02272/figures/010_Table_3.jpg]]
*Table 3: 12 action labels from HumanAct12 (Guo et al., 2020)*

![[assets/figures/papers/paper_list_l42_https_arxiv_org_pdf_2407_02272/figures/011_Table_4.jpg]]
*Table 4: 40 action labels from UESTC (Ji et al., 2018)*

## 方法谱系与知识库定位

### 核心瓶颈与因果机制

现有运动生成评估体系存在一个根本性脱节：主流指标——无论是基于真值配对的距离误差（Root AVE / Root AE / Joint AVE / Joint AE）、基于物理启发式的规则（Jerk、Acceleration、Person-Ground Contact、Foot-Floor Penetration），还是分布层面的度量（FID）——均无法在实例级别可靠地反映人类对运动质量的主观感知。这一瓶颈的实质在于，人类对“自然运动”的判断依赖难以显式参数化的隐式标准（如协调性、意图合理性），而预定义的规则和距离度量无法捕捉这些维度。

MotionCritic 的核心因果机制是：**利用大规模成对偏好数据训练一个数据驱动的评价器，将人类感知隐式编码为标量分数，从而将“与人类感知对齐”这一抽象目标转化为可优化的学习问题**。具体而言，该方法通过 Bradley-Terry 模型将成对比较转化为排序学习任务，使评价器学会输出与人类偏好一致的分数；随后，该分数可作为轻量级微调信号直接注入生成器的去噪过程，在极低计算开销下提升生成运动的主观质量。

### 方法演进与基线关系

MotionCritic 在运动评价方法谱系中处于从“规则驱动”向“数据驱动感知评价”跃迁的关键节点：

- **启发式规则基线**：Person-Ground Contact（Rempe et al., 2021）和 Physical Foot Contact（Tseng et al., 2023）代表了基于物理原理的脚部接触建模，在 MDM 子集上达到 71.78% 的准确率，是传统方法中最强的基线。然而，这些方法仅关注脚-地交互这一维度，无法评价整体运动质量。

- **学习型距离度量**：PoseNDF（Tiwari et al., 2022）通过学习姿态空间的隐式距离来度量运动相似性，但其训练目标与人类感知偏好无直接关联。NPSS（Gopalakrishnan et al., 2019）和 NDMS（Tanke et al., 2021）则分别从频域和方向相似性角度度量运动，同样缺乏感知对齐机制。

- **小规模感知评价尝试**：MoBERT（Voas et al., 2023）是此前唯一基于学习的人类评分运动评价器，但其训练数据仅约 1.4K 个评分，规模限制了其泛化能力。MotionCritic 将数据规模扩大至 52,563 对偏好标注（约 37 倍），从根本上改变了评价器可学习的感知知识广度。

- **生成器基线**：微调实验基于预训练的 MDM（Tevet et al., 2023）运动扩散生成器。MDM 本身仅使用扩散损失进行训练，缺乏对生成质量的主观感知约束。

### 关键改进槽位

| 改进维度 | 基线方案 | MotionCritic 方案 | 证据锚点 |
|---------|---------|------------------|---------|
| 运动质量评估范式 | 预定义距离、启发式规则或分布距离（FID） | 大规模人类偏好数据训练的神经网络评价器，输出与感知对齐的标量分数 | Table 1, Section 4.2 |
| 评价器训练目标 | 无（或小规模绝对评分学习） | Bradley-Terry 成对偏好对数损失：$\mathcal{L}_{\mathrm{Percept}} = -\mathbb{E}[\log \sigma(\mathcal{C}(\mathbf{x}^{(h)}) - \mathcal{C}(\mathbf{x}^{(l)}))]$ | Equation (2), Section 4.1 |
| 生成器微调损失 | 仅原始 MDM 扩散损失 | 扩散损失 + 评价器监督 + KL 正则：$\mathcal{L}_{\mathrm{FT}} = \mathcal{L}_{\mathrm{MDM}} + \lambda \mathcal{L}_{\mathrm{Critic}} + \mu \mathcal{L}_{\mathrm{KL}}$ | Equation (6), Section 4.3 |

### 适用边界

MotionCritic 的有效性在以下条件下得到验证：

1. **运动表征格式**：基于 SMPL 参数的运动序列，帧长为 60 帧。对于非 60 帧运动需要插值或截断处理，性能会有所下降（Figure 13 显示不同序列长度下存在性能衰减）。

2. **动作类别覆盖**：训练数据覆盖 HumanAct12 的 12 个动作类别和 UESTC 的 40 个动作类别。在 MDM 子集（85.07%）和跨域的 FLAME 子集（81.43%）上表现良好，但对极端罕见动作或全新生成范式的泛化性尚未充分验证。

3. **评价粒度**：评价器仅输出全局质量分数，无法提供时间维度或关节级别的细粒度反馈，难以精确诊断运动缺陷的具体位置和类型。

4. **优化可行性**：评价器函数表现出非光滑（“bumpy”）的能量景观（Figure 11 噪声扰动实验证实），这使得基于梯度的微调可能陷入局部最优，需要通过分数裁剪（$\tau=12.0$）和 KL 正则来维持训练稳定性。

### 局限与开放问题

**已确认的局限**：

- 评价器对运动长度的敏感性：非 60 帧运动需插值/截断，性能下降（Appendix 相关实验）。
- 评价函数的非光滑性：噪声扰动实验表明准确率随噪声增大平滑下降，能量景观的“颠簸”特性给梯度优化带来挑战（Figure 11, Appendix B.3）。
- 全局评分的局限性：无法提供时空细粒度的质量反馈，限制了诊断能力和监督信号的丰富度。
- 数据覆盖范围：训练数据仅覆盖有限的动作类别和生成方式，对极端罕见动作或全新生成范式（如物理仿真生成、文本到运动的新架构）的泛化性未经验证。

**开放问题**：

1. **细粒度感知评价**：如何设计时间/关节级别的偏好反馈机制，使评价器能输出更丰富的训练信号？这需要重新设计标注协议和模型架构。

2. **物理合理性显式融合**：当前评价器隐式学习物理合理性（如脚-地接触），但未显式融入生物力学约束。将物理先验与感知偏好联合建模可能进一步提升评估可靠性。

3. **非光滑景观的优化策略**：面对评价器的非光滑能量景观，可否借鉴强化学习中的策略梯度方法（而非依赖评价器梯度的直接反向传播）来更稳健地指导生成？

4. **数据集扩展**：如何扩展 MotionPercept 以包含更多样的运动风格（如舞蹈、体育动作）和更复杂的场景交互（如人与物体交互），使评价器具备更广泛的感知能力？

## 原文 PDF

![[paperPDFs/ICLR_2025/MotionCritic_Aligning_Human_Motion_Generation_with_Human_Perceptions.pdf]]
