---
title: "MoDiPO: text-to-motion alignment via AI-feedback-driven Direct Preference Optimization"
type: paper
paper_level: A
venue: arXiv
year: 2024
pdf_ref: "paperPDFs/arxiv_2024/MoDiPO:_text-to-motion_alignment_via_AI-feedback-driven_Direct_Preference_Optimization.pdf"
project_link: null
code_link: null
aliases:
- MoDiPO
tags:
- arxiv_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/representation_self_supervised_transfer
core_operator: 通过Direct Preference Optimization (DPO)在扩散路径上直接优化模型，利用AI反馈构建的偏好数据集（Pick-a-Move）引导生成远离低质量区域，朝向高文本对齐且真实的运动分布。
primary_logic: 用检索模型的文本-运动匹配得分作为AI反馈，替代昂贵的人类偏好标注，构建大规模偏好对数据集；采用随机赢家-输家选择策略，结合DPO目标对去噪过程进行监督，在保持多模态性的同时显著提升运动真实性和文本对齐度。
claims:
- MoDiPO是首个将DPO应用于文本到运动生成对齐的框架。
- 使用AI反馈（检索模型）自动标注偏好，避免人工标注的昂贵和耗时。
- 随机选择赢家-输家对策略优于简单的边缘选择，更有效地保持生成多样性。
- MoDiPO在HumanML3D上将FID从0.459降至0.281（约39%改善），同时保持RPrecision和Multi-Modality不降。
---

# MoDiPO: text-to-motion alignment via AI-feedback-driven Direct Preference Optimization

> [!tip] 核心洞察
> 用检索模型的文本-运动匹配得分作为AI反馈，替代昂贵的人类偏好标注，构建大规模偏好对数据集；采用随机赢家-输家选择策略，结合DPO目标对去噪过程进行监督，在保持多模态性的同时显著提升运动真实性和文本对齐度。

| 字段 | 内容 |
|------|------|
| 中文题名 | MoDiPO：通过AI反馈驱动的直接偏好优化实现文本到运动对齐 |
| 英文题名 | MoDiPO: text-to-motion alignment via AI-feedback-driven Direct Preference Optimization |
| 会议/期刊 | arXiv 2024 |
| Links | [paper](https://arxiv.org/abs/2405.03803) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/representation_self_supervised_transfer |
| Method | MoDiPO |
| Dataset | HumanML3D |

> [!tip] 效果简介
> - HumanML3D 上，FID↓ 0.281 ±0.007 vs 0.459 ±0.011 (-0.178 (-38.8%))；RPrecision Top3↑ 0.758 ±0.002 vs 0.755 ±0.003 (+0.003)；MMDist↓ 3.267 ±0.010 vs 3.292 ±0.010 (-0.025)。

## 概要

文本到运动（Text-to-Motion）扩散模型因其内在的随机采样机制，常生成偏离文本描述或缺乏物理真实感的运动序列。现有方法在控制生成多样性与文本对齐/真实感之间的平衡上存在明显短板，而依赖人类反馈的对齐方案又面临标注成本高昂的瓶颈。

MoDiPO（Motion Diffusion DPO）首次将Direct Preference Optimization引入文本到运动生成的对齐任务。其核心思路是：**用检索模型的文本-运动匹配得分作为AI反馈，替代昂贵的人类偏好标注，构建大规模合成偏好数据集Pick-a-Move（PaM）；在此基础上，采用随机赢家-输家选择策略，通过Diffusion DPO损失在完整扩散路径上优化模型，使生成分布远离低质量区域，朝向高文本对齐且真实的运动分布收敛。**

实验表明，MoDiPO在对齐**MLD**（Chen et al., CVPR 2023）和**MDM**（Tevet et al., ICLR 2023）两种主流扩散架构后，HumanML3D上的FID最高降低约39%（从0.459降至0.281），同时RPrecision和Multi-Modality基本保持不变，验证了该方法在显著提升运动真实性的同时能够保留生成多样性。赢家-输家分析进一步揭示，MoDiPO有效抑制了低质量生成，大幅缩小了同一提示下最优与最差样本之间的FID差距。

### 文本到运动生成的核心瓶颈

文本到运动（Text-to-Motion）生成旨在根据自然语言描述合成逼真的三维人体运动序列，在动画制作、游戏开发和虚拟人交互等领域具有广泛应用。近年来，扩散模型在该任务上取得了显著进展，代表性工作包括基于原始运动空间的 **MDM**（Tevet et al., ICLR 2023）和基于潜在扩散的 **MLD**（Chen et al., CVPR 2023）。这些模型通过逐步去噪的方式从文本条件中采样运动，能够产生多样化的生成结果。

然而，扩散模型的内在随机性带来了一个关键问题：**生成多样性、运动真实感与文本对齐度之间存在难以调和的张力**。具体而言，同一文本提示下的多次采样可能产生质量参差不齐的运动——部分生成可能偏离文本描述、包含不自然的姿态或陷入异常运动区域。现有方法主要通过改进网络架构或训练策略来提升整体生成质量，但**缺乏对生成分布中低质量区域的显式抑制机制**，无法在保持多样性的同时系统性地引导模型远离不真实或不对齐的运动。

### 偏好对齐的机遇与挑战

在大语言模型领域，**Direct Preference Optimization (DPO)** 已被证明是一种有效的对齐方法，能够直接利用偏好数据优化模型，使其生成更符合人类期望。将这一思路迁移到文本到运动生成中，理论上可以通过偏好学习引导扩散模型朝向高文本对齐且真实的运动分布。但这一迁移面临两个核心障碍：

1. **偏好数据匮乏**：文本到运动领域缺乏大规模的人工偏好标注数据集。与文本或图像不同，运动数据的偏好判断需要专业标注者逐对比较运动序列的文本对齐度和自然度，成本极高且难以规模化。

2. **扩散路径上的优化适配**：DPO最初针对自回归语言模型设计，需要将其适配到扩散模型的去噪轨迹上。扩散DPO（Diffusion-DPO）为这一适配提供了理论基础，但其在文本到运动任务上的有效性尚未被验证。

### 本文动机

针对上述瓶颈，本文提出 **MoDiPO（Motion Diffusion DPO）**，核心动机在于：

- **用AI反馈替代人工偏好标注**：利用检索模型自动评估文本-运动对的匹配程度，构建大规模合成偏好数据集（Pick-a-Move），从而绕过昂贵的人工标注流程。
- **在扩散路径上直接优化**：将Diffusion-DPO目标应用于文本到运动扩散模型，通过赢家-输家对的对比学习，显式地拉近高质量生成、推远低质量生成，在不牺牲多样性的前提下提升运动真实性和文本对齐度。
- **验证偏好学习在该模态的有效性**：首次系统性地探索DPO在文本到运动生成对齐中的作用，为后续研究提供基准和方法论参考。

## 核心方法与创新机理

MoDiPO的核心创新在于将**Direct Preference Optimization (DPO)** 首次引入文本到运动生成的对齐任务，并通过**AI反馈驱动的合成偏好数据集**替代昂贵的人类标注，在保持生成多样性的同时显著提升运动真实性和文本对齐度。

### 1. 从人类偏好到AI反馈的闭环

传统DPO依赖人工标注偏好对，成本高昂且难以规模化。MoDiPO的关键突破是用**检索模型的文本-运动匹配得分作为AI反馈**，自动构建大规模偏好数据集 **Pick-a-Move (PaM)**。具体流程为：冻结的参考模型为每个文本提示生成 $K$ 个候选运动，由检索模型（如 **TMR** 或 **Guo** 模型）根据文本对齐度打分排序，再从中采样赢家-输家对用于DPO训练。这一设计将偏好标注从“人工劳动”变为“模型自动生成”，使得DPO在运动生成领域的大规模应用成为可能。

### 2. 扩散路径上的直接偏好优化

MoDiPO采用**Diffusion DPO损失**，在完整去噪路径 $x_{0:T}$ 上直接优化目标模型：

$$L_{\mathrm{DDPO}}(\theta) = -\mathbb{E}_{x_{0}^{w}, x_{0}^{l}} \log \sigma\Big( \beta \mathbb{E}_{x_{1:T}^{w}\sim p_{\theta}(x_{1:T}^{w}\mid x_{0}^{w})} \big[ \log \frac{p_{\theta}(x_{0:T}^{w})}{p_{\mathrm{ref}}(x_{0:T}^{w})} - \log \frac{p_{\theta}(x_{0:T}^{l})}{p_{\mathrm{ref}}(x_{0:T}^{l})} \big] \Big)$$

该损失的核心机制是：**提高赢家运动的去噪似然，同时压低输家运动的去噪似然**，从而引导模型远离低质量区域，朝向高文本对齐且真实的运动分布。与标准的DDPM均方误差损失相比，这一目标直接建模了“好运动”与“差运动”之间的相对偏好，而非简单的逐像素重建。

### 3. 随机赢家-输家选择策略

在偏好对构建上，MoDiPO提出**随机选择策略**：将排序列表划分为前半（赢家候选）和后半（输家候选），再从中随机采样组成训练对。消融实验表明，该策略在FID和多样性指标上**优于仅取首尾极端对的边缘选择策略**。原因在于随机采样保留了适度的排序噪声，避免模型过度拟合极端偏好而损害生成多样性。

### 4. 针对性参数微调

MoDiPO仅对模型的部分参数进行微调：对于基于潜在扩散的**MLD**（Chen et al., CVPR 2023），仅更新denoiser参数；对于**MDM**（Tevet et al., ICLR 2023），仅微调最后几层。参考模型完全冻结，确保对齐过程中不会偏离原始生成能力过远。此外，以低概率（0.25/0.5）用真实运动替换赢家，提供额外的监督信号，可在FID和Multi-Modality上获得进一步改善，但会轻微损害R-Precision，需根据应用场景权衡。

### 5. 关键证据强度

- **FID改善显著且一致**：在HumanML3D上，MLD经MoDiPO对齐后FID从0.459降至0.281（约39%改善），同时RPrecision和Multi-Modality基本持平，证明对齐未牺牲文本匹配与多样性。
- **低质量生成有效抑制**：赢家-输家分析显示，对齐后输家运动的FID大幅改善，赢家与输家之间的FID差距显著缩小（HumanML3D上从0.711降至0.604，KIT-ML上从0.172降至0.006），表明模型有效抑制了低质量生成。
- **消融实验充分**：随机选择策略、GT监督概率、在线对齐及PaM+等设计选择均有量化验证，结论可靠。

> 需注意：AI反馈的排序模型可能引入与人类偏好不完全一致的偏差，且当前仅在HumanML3D和KIT-ML两个数据集上验证，对其他运动域的泛化性尚待确认。

MoDiPO 的整体流程围绕“生成—排序—配对—优化”四个阶段构建，将 Direct Preference Optimization (DPO) 引入文本到运动扩散模型的对齐训练。其核心思路是：利用冻结的预训练扩散模型（参考模型）为每个文本提示生成多个候选运动，再通过检索模型给出的文本-运动匹配得分自动构建赢家-输家偏好对，最终以 Diffusion DPO 损失对目标模型进行微调，使其在保持生成多样性的同时远离低质量运动区域。

### 模块关系与数据流

框架由四个关键模块串联而成：

**1. 参考模型（Reference Model）**
一个完全冻结的预训练文本到运动扩散模型（实验中采用 **MLD** (Chen et al., CVPR 2023) 或 **MDM** (Tevet et al., ICLR 2023)）。对于给定文本提示 $c$，参考模型生成 $K$ 个候选运动 $\{m_1, m_2, \dots, m_K\}$。这些候选构成后续偏好排序的原始素材。

**2. AI 排序器（Ranker / Scorer）**
采用基于检索的预训练模型对每个候选运动与提示文本的匹配程度进行打分。论文使用了两种排序器：**TMR** 和 **Guo 模型**。排序器输出每个候选运动的得分 $s_i$，据此将候选列表 $\mathbf{m}$ 排序为 $\mathbf{m}^*$（得分从高到低）。

**3. 偏好对构建（Pair Construction）**
从排序后的候选列表中采样形成赢家-输家对。论文设计了两种策略：
- **边缘选择（edge selection）**：直接取排序列表的首尾作为赢家和输家。
- **随机选择（stochastic selection）**：将排序列表平分为前后两部分，前半部分为赢家候选池，后半部分为输家候选池，从中随机采样组成训练对。实验表明，随机选择策略在 FID 和多样性指标上均优于边缘选择，因为它避免了模型仅学习排斥极端劣质样本而忽略中间分布的问题。

此外，为了提供额外的监督信号，框架以较低概率（$p=0.25$ 或 $0.5$）将真实运动替换为赢家，使目标模型在优化过程中也能接触到 ground truth 的分布特征。

**4. DPO 训练循环（DPO Training）**
利用构建好的赢家-输家对 $(x_0^w, x_0^l)$，以 Diffusion DPO 损失对目标模型进行微调。目标模型与参考模型共享架构，但仅更新部分参数：对于 MLD 仅微调解码器（denoiser），对于 MDM 仅微调最后几层。损失函数在完整扩散路径 $x_{0:T}$ 上比较赢家与输家序列的对数概率比：

$$L_{\mathrm{DDPO}}(\theta) = -\mathbb{E}_{x_0^w, x_0^l} \log \sigma\Big( \beta \mathbb{E}_{x_{1:T}^w \sim p_\theta(x_{1:T}^w \mid x_0^w)} \big[ \log \frac{p_\theta(x_{0:T}^w)}{p_{\mathrm{ref}}(x_{0:T}^w)} - \log \frac{p_\theta(x_{0:T}^l)}{p_{\mathrm{ref}}(x_{0:T}^l)} \big] \Big)$$

该损失引导目标模型提高赢家运动的去噪似然、降低输家运动的去噪似然，从而在扩散采样过程中系统性地抑制低质量生成。

### 偏好数据集 Pick-a-Move

为支撑上述流程，论文构建了合成偏好数据集 **Pick-a-Move (PaM)**。该数据集使用 MLD 和 MDM 两个基础模型，对 HumanML3D 和 KIT-ML 的训练集文本提示各生成 $K$ 个候选运动，经 AI 排序器打分排序后存储。PaM 的构建完全自动化，避免了人工偏好标注的高昂成本，使 DPO 在大规模文本-运动对齐任务上可行。

整个框架的输入为文本提示和 PaM 中的偏好对，输出为经过对齐微调的扩散模型。该模型在推理时与原始模型保持相同的采样流程，无需额外组件，因此不增加推理开销。

![[assets/figures/papers/paper_list_l3308_https_arxiv_org_abs_2405_03803/figures/002_Figure_2.jpg]]
*Figure 2: MoDiPO Schematics: Starting with the input prompt, we generate a winnerloser pair, which constitutes a sample in our preferential dataset. To do so, the reference model produces K generations based on the same input prompt. These generations are then ranked by the ranker model according to their relevance with the textual input. From these rankings, we select both a set of winners and a set of losers. Finally, we sample from these sets to determine the final pair. This pair is then used to refine the unfrozen target model using DPO*

MoDiPO 的核心在于将 Direct Preference Optimization（DPO）引入扩散模型的去噪路径，利用 AI 反馈自动构建偏好对，从而在不依赖人类标注的情况下实现文本到运动生成的对齐。整个框架由四个关键模块串联而成。

### 参考模型：偏好数据的生成器

参考模型是一个完全冻结的预训练文本到运动扩散模型（如 **MLD** (Chen et al., CVPR 2023) 或 **MDM** (Tevet et al., ICLR 2023)）。对于给定文本提示 $c$，参考模型生成 $K$ 个候选运动 $\{m_1, m_2, \dots, m_K\}$，构成后续偏好排序的原料池。该模型在 DPO 训练期间参数完全冻结，仅作为生成分布的上限参考。

### AI 排序器：替代人类反馈的自动评分

为避免昂贵的人工偏好标注，MoDiPO 采用基于检索的模型作为 AI 排序器，对文本-运动对进行对齐度评分。具体而言，使用 **TMR** 或 **Guo 模型** 计算文本 $c$ 与每个生成运动 $m_i$ 之间的匹配得分 $s(c, m_i)$。根据这些得分将 $K$ 个候选运动排序为有序列表 $m^*$，得分高者文本对齐度更优。

### 偏好对构建：随机赢家-输家选择策略

从排序列表中构建赢家-输家对是 MoDiPO 的关键设计选择。与直接选取首尾极端对（edge selection）不同，MoDiPO 采用**随机选择策略**：

1. 将排序后的列表 $m^*$ 划分为前半部分（高分区）和后半部分（低分区）。
2. 从前半部分随机采样一个运动作为赢家 $x_0^w$，从后半部分随机采样一个运动作为输家 $x_0^l$。
3. 以低概率（0.25 或 0.5）用真实运动替换赢家，为模型提供额外的监督信号。

消融实验表明，这种随机划分策略在 FID 和生成多样性上均优于仅取首尾极端对的边缘选择策略，因为它避免了模型过度聚焦于极端样本而损害多模态性。

### DPO 训练循环：扩散路径上的偏好优化

MoDiPO 的训练目标建立在扩散 DPO 损失之上，其推导从带 KL 正则化的奖励最大化目标出发：

$$\max_{p_{\theta}} \mathbb{E}_{c\sim\mathcal{D}_{c}, x_{0}\sim p_{\theta}(x_{0}\mid c)} \big[ r(c, x_{0}) \big] - \beta \mathrm{KL}\big[ p_{\theta}(x_{0}\mid c) \| p_{\mathrm{ref}}(x_{0}\mid c) \big]$$

该目标在最大化预期奖励的同时，约束优化后的分布 $p_\theta$ 不过度偏离参考分布 $p_{\mathrm{ref}}$，超参数 $\beta$ 控制约束强度。通过推导，奖励函数可被隐式表达为对数概率比的形式，从而将问题转化为直接在偏好对上优化条件分布，无需显式训练奖励模型。

将 DPO 目标特化到扩散模型，损失函数定义在整个去噪路径 $x_{0:T}$ 上：

$$L_{\mathrm{DDPO}}(\theta) = -\mathbb{E}_{x_{0}^{w}, x_{0}^{l}} \log \sigma\Big( \beta \mathbb{E}_{x_{1:T}^{w}\sim p_{\theta}(x_{1:T}^{w}\mid x_{0}^{w})} \big[ \log \frac{p_{\theta}(x_{0:T}^{w})}{p_{\mathrm{ref}}(x_{0:T}^{w})} - \log \frac{p_{\theta}(x_{0:T}^{l})}{p_{\mathrm{ref}}(x_{0:T}^{l})} \big] \Big)$$

其中各符号含义：
- $x_0^w, x_0^l$：赢家与输家运动样本。
- $x_{1:T}^w$：赢家运动对应的完整扩散前向路径。
- $p_\theta(x_{0:T})$：目标模型在扩散路径上的联合概率。
- $p_{\mathrm{ref}}(x_{0:T})$：冻结参考模型在扩散路径上的联合概率。
- $\sigma(\cdot)$：sigmoid 函数，将对数几率比映射为概率。
- $\beta$：控制 DPO 更新强度的温度系数。

该损失的核心机制是：当赢家序列在目标模型下的对数概率比高于输家序列时，损失降低；反之则惩罚模型。通过在整个扩散路径上比较对数概率比，模型被引导去提升高质量运动（赢家）的去噪似然，同时抑制低质量运动（输家）的生成概率。

在模型更新范围上，MoDiPO 仅微调目标模型的部分参数：对于基于潜在扩散的 **MLD**，只更新 denoiser 参数；对于 **MDM**，仅微调最后几层。参考模型完全冻结，确保优化不会偏离预训练分布过远。

## 实验与关键发现

### 1. 主实验结果

MoDiPO在HumanML3D和KIT-ML两个标准基准上对MLD和MDM两种基线模型进行了对齐实验。表1和表2分别展示了两个数据集上的完整对比结果。所有指标均基于20次随机种子运行报告均值与置信区间，确保比较的统计可靠性。

**HumanML3D上的表现（Table 1）**：MLD-GUO配置（使用Guo评分器）取得对齐模型中最优的FID（0.281），相比未对齐MLD的0.459降低了约38.8%；MLD-TMR配置则在RPrecision Top3上取得对齐模型中最优值（0.758），略高于未对齐MLD的0.755。MDM模型同样受益于MoDiPO对齐，FID从0.544降至0.399（约26.7%改善），同时RPrecision Top3从0.611提升至0.656。两项Multi-Modality指标在两种基线上均保持不降甚至略有提升，表明DPO对齐未以牺牲生成为代价换取质量。

**KIT-ML上的表现（Table 2）**：MoDiPO对齐后的MLD模型FID从0.404降至0.296，MDM模型从0.497降至0.404，趋势与HumanML3D一致。值得注意的是，KIT-ML上的MLD模型是作者从头训练的（因原始模型未公开），可能引入细微差异，但MoDiPO对齐后仍展现出显著的跨数据集一致改善。表中斜体表示所有方法中的全局最优，粗体表示预训练模型与MoDiPO对齐模型中的最优，读者可据此定位各指标的最佳方案。

**赢家-输家质量差距分析（Table 3）**：每提示生成8条运动后，取评分最高者为赢家、最低者为输家。未对齐MLD在HumanML3D上赢家与输家FID差距为0.711，对齐后降至0.604，差距缩小15.05%；在KIT-ML上，差距从0.172降至0.006，缩小幅度高达96.51%。这一结果表明MoDiPO有效抑制了低质量生成，使模型输出分布整体向高质量区域收缩，而非仅仅提升平均表现。

### 2. 消融实验

消融实验以MLD为基模型、HumanML3D为主数据集，系统评估了偏好对构建策略、真实运动监督、数据来源及在线对齐方式的影响（Table 4）。

![[assets/figures/papers/paper_list_l3308_https_arxiv_org_abs_2405_03803/figures/016_Table_4.jpg]]
*Table 4: Ablation study with MLD model on HumanML3D dataset [8]. Stoch stands for stochastic selection of pairs, default is edge selection*

**随机选择策略 vs. 边缘选择策略**：默认的边缘选择策略直接取排序列表的首尾作为赢家-输家对；随机选择策略则将排序列表分为前后两半，前半作为赢家候选集、后半作为输家候选集，从中随机采样构成对。实验表明，随机选择策略在FID上优于边缘选择（0.281 vs. 0.303），同时Multi-Modality更高（2.736 vs. 2.600），说明该策略在提升质量的同时更有效地保持了生成多样性。这一发现与DPO理论预期一致——极端对可能导致模型过度拟合评分器的偏好边界，而随机采样引入了更丰富的比较信号。

**真实运动监督概率（GT_p）**：以一定概率（0.25或0.5）用真实运动替换赢家，可进一步降低FID（GT_p=0.5时FID降至0.271）并提升Multi-Modality，但RPrecision Top3从0.758降至0.746。这表明真实运动提供了额外的正向监督信号，但可能使模型偏向真实分布而略微牺牲文本对齐精度，需根据应用场景权衡。

**完整Pick-a-Move数据集（PaM+）**：PaM+同时包含MLD和MDM生成的候选运动，旨在增加数据多样性。然而实验表明，使用PaM+并未带来预期提升，性能甚至略低于仅用同模型生成数据的配置。作者推测跨模型数据分布差异可能引入了噪声信号，此点需手动验证具体原因。

**在线对齐**：在线对齐方式在每步训练时实时生成并排序候选运动，初步结果显示FID有所降低，但RPrecision同步下降。作者指出这体现了质量-对齐的权衡，可能需要更多训练迭代才能使目标模型有效排斥低质量运动。这一方向仍处于探索阶段，结论强度有限。

### 3. 失败模式与局限

尽管MoDiPO在整体指标上表现优异，但分析揭示了若干值得关注的边界情况：

- **RPrecision的潜在退化**：当引入真实运动监督或采用在线对齐时，RPrecision出现可观测的下降。这表明AI评分器（TMR/Guo）的偏好与文本-运动检索评估指标之间存在偏差，过度优化评分器信号可能导致模型在检索式评估上表现受损。这是AI反馈对齐方法的固有风险，需手动验证评分器偏差的具体方向。

- **跨模型数据混合失效**：PaM+实验的负面结果表明，简单地混合不同生成模型的输出并不能增强偏好数据集的有效性。可能的解释是MLD和MDM的失败模式不同，混合后引入了不一致的比较信号，但原始论文未深入分析此现象，此论断需谨慎对待。

- **在线对齐的不稳定性**：在线对齐的RPrecision下降提示当前迭代次数不足以让模型充分学习排斥低质量运动。这暗示扩散DPO在在线设置下可能需要更长的训练周期或改进的负样本利用策略。

### 4. 关键图表结论

- **Table 1 & Table 2**：MoDiPO对齐在两种基线和两个数据集上一致降低FID，同时保持或提升RPrecision与Multi-Modality，验证了方法的通用性和鲁棒性。
- **Table 3**：赢家-输家FID差距的大幅缩小直接证明了MoDiPO抑制低质量生成的核心机制有效，而非仅通过提升平均表现掩盖方差。
- **Table 4**：随机选择策略优于边缘选择、适度真实运动监督可进一步改善FID、跨模型数据混合未带来增益，这些消融发现为偏好数据集构建提供了明确的设计指南。

![[assets/figures/papers/paper_list_l3308_https_arxiv_org_abs_2405_03803/figures/003_Table_1.jpg]]
*Table 1: Results for HumanML3D [8]. Each group results corresponds to vanilla models, aligned models and current SOTA backed by a RAG framework. Italic is for best results overall, while bold represents best results among pretrained models and MoDiPO aligned ones*

![[assets/figures/papers/paper_list_l3308_https_arxiv_org_abs_2405_03803/figures/004_Table_2.jpg]]
*Table 2: Results for KIT-ML [22]. Each group results corresponds to vanilla models, aligned models and current SOTA backed by a RAG framework. Italic is for best results overall, while bold represents best results among pretrained models and MoDiPO aligned ones*

![[assets/figures/papers/paper_list_l3308_https_arxiv_org_abs_2405_03803/figures/005_Table_3.jpg]]
*Table 3: Performances of Winner (W) and Loser (L) among the 8 generations perprompt of vanilla MLD (MLD) and MLD aligned with MoDiPO (Ours) for HumanML3D and KIT-ML. The typical evaluation method calculation is used in the case of MLD and Ours (aligned model)*

## 定位与知识库关联

### 与基线方法的关系

MoDiPO 并非一个独立的文本到运动生成模型，而是一种**模型无关的对齐框架**，可施加于现有扩散式生成器之上。论文选择了两类代表性基线进行对齐实验：

- **MLD**（Chen et al., CVPR 2023）：基于潜在扩散的文本到运动模型，将运动编码到 VAE 潜在空间后执行去噪。MoDiPO 对齐时仅微调其 denoiser 参数，VAE 编码器/解码器保持冻结。
- **MDM**（Tevet et al., ICLR 2023）：在原始运动表示上直接执行扩散去噪。MoDiPO 对齐时仅微调最后几层，参考模型完全冻结。

这种“轻量微调”策略使 MoDiPO 区别于需要重新训练或引入额外模块的对齐方法。与基于 RAG 的 SOTA 方法（如 ReMoDiffuse）相比，MoDiPO 在 HumanML3D 上以 **0.281 的 FID 显著优于后者的 0.363**（Table 1），同时保持 RPrecision Top3 为 0.758，说明 DPO 对齐在运动真实性上的增益不依赖于检索增强的外部知识库。

### 与 DPO 家族的关系

MoDiPO 直接继承自 **Diffusion-DPO**（Wallace et al., 2023）在文本到图像对齐中的公式化工作，将其首次迁移至文本到运动域。其核心改动在于：

1. **AI 反馈替代人类偏好**：用检索模型（TMR 或 Guo 模型）的文本-运动匹配得分构建偏好对，绕过了 RLHF/DPO 管线中昂贵的人类标注环节。
2. **随机赢家-输家选择策略**：不同于取排序列表首尾极端对的简单做法，MoDiPO 将排序列表划分为前半（赢家候选）和后半（输家候选），再从中随机采样组成对。消融实验（Table 4）证实该策略在 FID 和多样性指标上均优于边缘选择。
3. **真实运动注入机制**：以低概率（0.25 或 0.5）用 ground-truth 运动替换赢家，提供额外的监督信号。该操作能进一步降低 FID 并提升 Multi-Modality，但会损害 R-Precision，形成可控的权衡旋钮。

与标准的 RLHF 相比，MoDiPO 避免了显式训练奖励模型和在线策略优化的复杂性，直接在扩散路径上通过对数几率比对比赢家与输家序列：

$$L_{\mathrm{DDPO}}(\theta) = -\mathbb{E}_{x_{0}^{w}, x_{0}^{l}} \log \sigma\Big( \beta \mathbb{E}_{x_{1:T}^{w}\sim p_{\theta}(x_{1:T}^{w}\mid x_{0}^{w})} \big[ \log \frac{p_{\theta}(x_{0:T}^{w})}{p_{\mathrm{ref}}(x_{0:T}^{w})} - \log \frac{p_{\theta}(x_{0:T}^{l})}{p_{\mathrm{ref}}(x_{0:T}^{l})} \big] \Big)$$

该损失在完整去噪路径 $x_{0:T}$ 上比较赢家与输家序列的对数概率比，使目标模型提高赢家运动的去噪似然、降低输家运动的去噪似然。

### 适用边界

**有效边界**：
- 适用于基于扩散的文本到运动生成模型（MLD、MDM 已验证），理论上可推广至其他扩散式生成器。
- 在 HumanML3D 和 KIT-ML 两个标准基准上均有效，FID 改善幅度达 39%，同时 RPrecision 和 Multi-Modality 不降。
- 赢家-输家 FID 差距显著缩小（HumanML3D 上从 0.711 降至 0.604，KIT-ML 上从 0.172 降至 0.006），表明模型有效抑制了低质量生成。

**已知局限**：
- **微调范围的保守性**：目前仅更新 MLD 的 denoiser 或 MDM 的最后几层，可能未充分释放模型潜力。论文明确建议未来尝试 LoRA 等参数高效微调。
- **在线对齐的不成熟**：实时生成并排序的在线对齐方式虽能降低 FID，但 R-Precision 同步下降，表明需要更多迭代才能有效排斥低质量运动。
- **AI 反馈的偏差**：排序模型（TMR/Guo）的文本-运动匹配得分可能与人类偏好存在系统性偏差，该偏差会直接传导至 DPO 训练。
- **数据集泛化性未验证**：仅在 HumanML3D 和 KIT-ML 上测试，对其他运动域（如舞蹈、体育动作）或文本风格的泛化性未知。
- **跨模型数据混合的失效**：同时使用 MLD 和 MDM 生成数据构建的 PaM+ 数据集未带来预期提升，性能甚至略低于仅用同模型生成的数据（Table 4），说明偏好数据的分布一致性对 DPO 训练至关重要。

### 开放问题

1. **在线对齐的收敛条件**：需要多少迭代才能实现“降低 FID 同时保持 R-Precision”的理想均衡？是否需要引入负样本重采样或课程学习策略？
2. **参数高效微调的上限**：LoRA 等方案能否在 MDM 上取得比“仅微调最后几层”更好的对齐效果，同时保持训练效率？
3. **AI 反馈模型的校准**：是否可以通过微调排序模型或集成多个人工反馈代理来提升其对人类偏好的拟合能力？
4. **跨架构迁移**：MoDiPO 框架能否直接应用于自回归式文本到运动模型（如 T2M-GPT）或其他生成模态（如文本到音乐、文本到视频）？
5. **FID-RPrecision 权衡的自动化**：能否设计自适应机制，根据下游任务需求自动调节真实运动注入概率 $p_{GT}$ 或 DPO 正则化系数 $\beta$？
6. **偏好对构建的最优策略**：随机划分排序列表的策略虽优于边缘选择，但是否存在更优的采样分布（如基于得分的加权采样）？

## 原文 PDF

![[paperPDFs/arxiv_2024/MoDiPO:_text-to-motion_alignment_via_AI-feedback-driven_Direct_Preference_Optimization.pdf]]
