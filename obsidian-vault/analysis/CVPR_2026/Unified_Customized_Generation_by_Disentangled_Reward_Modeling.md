---
title: Unified Customized Generation by Disentangled Reward Modeling
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Unified_Customized_Generation_by_Disentangled_Reward_Modeling.pdf
project_link: null
code_link: "https://github.com/bytedance/USO"
aliases:
- UUSO
- UCGBDRM
tags:
- CVPR_2026
- topic/generative_models_diffusion
- topic/representation_self_supervised_transfer
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 跨任务协同解耦范式：通过构建循环数据-模型框架（主体为风格的数据整理管道和风格为主体的模型训练管道），在统一优化中互促共进。
primary_logic: 一个任务学会「包含」某类特征，恰恰能帮助互补任务更有效地「排除」这类特征，从而在跨任务协同中实现更精准的特征分离。
claims:
- USO 引入了一个循环数据-模型框架，连接主题与风格任务。
- 风格为主体模型训练管道引入辅助风格奖励，同时对齐风格与内容特征。
- 提出新型跨任务协同解耦范式，统一风格驱动与主题驱动生成并实现相互增强。
- 辅助风格奖励（ASR）虽然仅依赖风格奖励，却能有效增强身份一致性。
---

# Unified Customized Generation by Disentangled Reward Modeling

> [!tip] 核心洞察
> 一个任务学会「包含」某类特征，恰恰能帮助互补任务更有效地「排除」这类特征，从而在跨任务协同中实现更精准的特征分离。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于解耦奖励建模的统一定制生成 |
| 英文题名 | Unified Customized Generation by Disentangled Reward Modeling |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Wu_Unified_Customized_Generation_by_Disentangled_Reward_Modeling_CVPR_2026_paper.html) · [Code](https://github.com/bytedance/USO) |
| Topic | #topic/generative_models_diffusion #topic/representation_self_supervised_transfer #topic/generative_models_diffusion/diffusion_image_video |
| Method | USO (Unified Simultaneous Optimization) |
| Dataset | USO-Bench |

> [!tip] 效果简介
> - USO-Bench (Subject-driven) 上，CLIP-I 0.647 vs 0.605 (UNO) (+0.042)；CLIP-T 0.287 vs 0.264 (UNO) (+0.023)。
> - USO-Bench (Style-driven) 上，CSD 0.556 vs previous best (unspecified) (new SOTA)；CLIP-T 0.286 vs previous best (unspecified) (new SOTA)。
> - USO-Bench (Style-subject-driven) 上，CSD 0.492 vs 0.365 (OmniStyle) (+0.127)。

## 概要

现有扩散模型的定制生成方法通常将**风格驱动**与**主题驱动**视为两个独立任务，各自设计解耦策略，忽略了二者在特征“包含”与“排除”上的天然互补性，导致解耦不够彻底。针对这一瓶颈，本文提出 **USO（Unified Simultaneous Optimization）**，一种基于**跨任务协同解耦**的统一框架。其核心洞见在于：一个任务学会“包含”某类特征，恰恰能帮助互补任务更有效地“排除”这类特征，从而在统一优化中实现更精准的特征分离。

USO 通过**循环数据-模型框架**连接两个任务：一方面，以主体为风格的数据整理管道（subject-for-style data curation pipeline）生成高质量三元组数据；另一方面，以风格为主体的模型训练管道（style-for-subject model training pipeline）引入辅助风格奖励（Auxiliary Style Reward, ASR），在流匹配损失基础上同时对齐风格与内容特征。模型采用解耦条件编码器（SigLIP 语义编码器 + 轻量分层投影器）分别处理风格参考与内容参考，并通过随机条件丢弃训练保持单任务与多任务能力。

在实验层面，USO 在自建的 **USO-Bench** 上取得了全面领先：主题驱动任务中 CLIP-I 达 0.647，显著优于 UNO（0.605）；风格驱动任务中 CSD 达 0.556，CLIP-T 达 0.286，均为新 SOTA；风格-主题联合驱动任务中 CSD 达 0.492，较 OmniStyle（0.365）提升 0.127。消融实验证实，ASR 损失与解耦编码器对性能提升均有显著贡献——值得注意的是，ASR 虽仅依赖风格奖励，却能有效增强身份一致性（Figure 7）。

### 定制化生成的两类任务与共同瓶颈

图像定制化生成旨在根据用户提供的参考图像，生成保留特定视觉属性且符合文本描述的新图像。该领域长期沿着两条相对独立的路径发展：

- **主体驱动生成**：要求生成的图像保持参考主体（如特定人物、物体）的身份一致性。主流方法通常通过微调扩散模型或注入身份特征来实现，代表性工作包括 **RealCustom++**（Mao et al., 2024）、**UNO**（Wu et al., 2025）、**OmniGen2**（Wu et al., 2025）、**BAGEL**（Deng et al., 2025）以及 **FLUX.1 Kontext dev**（Black Forest Labs et al., 2025）等。
- **风格驱动生成**：要求生成的图像继承参考图像的艺术风格（如笔触、色调、纹理），同时保持内容与文本一致。代表性方法包括 **StyleStudio**（Lei et al., CVPR 2025）、**DEADiff**（Qi et al., CVPR 2024）、**InstantStyle**（Wang et al., 2024）等。

两类任务面临一个共同的核心瓶颈：**如何将参考图像的特定属性（主体身份或风格特征）与不相关内容（背景、布局等）有效解耦**。现有方法各自针对单一任务设计解耦策略——主体方法着力“包含”身份特征，风格方法着力“排除”内容泄漏——但忽略了二者在特征包含与排除上的天然互补性，导致解耦不够彻底。

### 现有方法的缺口：任务孤立与解耦不充分

尽管已有少数工作尝试同时处理主体与风格，如 **OmniStyle**（Wang et al., CVPR 2025）和 **StyleID**（Chung et al., CVPR 2024），但它们本质上仍将两类任务视为独立的并行分支，缺乏任务间的协同机制。这种孤立设计带来两个突出问题：

1. **数据层面**：训练数据通常面向单一任务手工构建，缺乏跨任务的结构化三元组（内容图像、风格图像、风格化内容），限制了模型学习解耦表征的能力。
2. **优化层面**：损失函数仅关注最终生成质量，未显式建模风格与内容特征的分离过程，导致风格迁移时容易出现内容泄漏，或主体保持时风格保真度不足。

### 本文动机：跨任务协同解耦范式

本文提出一个关键洞察：**一个任务学会“包含”某类特征，恰恰能帮助互补任务更有效地“排除”这类特征**。具体而言，主体驱动任务需要精确包含身份特征，这为风格驱动任务提供了“哪些特征不应被风格化”的强信号；反之，风格驱动任务需要排除内容泄漏，这为主体驱动任务提供了“哪些特征不应被保留”的约束。

基于这一洞察，论文提出 **USO（Unified Simultaneous Optimization）**，一种新型跨任务协同解耦范式，通过构建**循环数据-模型框架**——主体为风格的数据整理管道和风格为主体的模型训练管道——将风格驱动与主体驱动生成统一在相互增强的优化过程中。

## 核心方法与创新机理

USO 的核心创新在于提出了一种**跨任务协同解耦范式**，将原本各自独立的风格驱动生成与主题驱动生成统一到一个相互增强的框架中。其关键洞察是：一个任务学会“包含”某类特征，恰恰能帮助互补任务更有效地“排除”这类特征，从而在跨任务协同中实现更精准的特征分离。

围绕这一范式，USO 在四个关键维度上对现有方法进行了系统性改进：

### 1. 跨任务三元组数据整理框架

现有方法通常为单一任务手工或自动构建三元组（通常仅保留布局信息），USO 则构建了一个**循环数据-模型框架**来桥接主题与风格任务。该框架包含两个专家模型：基于 UNO-SFT 微调的 **Stylization Expert** 负责生成高风格相似度且无内容泄漏的风格化图像；冻结的 **FLUX.1 Kontext dev** 作为 **De-stylization Expert** 将风格图像反转为写实图像。通过这两个专家，框架系统性地生成**布局保留**与**布局偏移**两类三元组，为跨任务训练提供高质量监督信号。

### 2. 解耦条件编码器

不同于基线方法普遍采用的共享 VAE 或简单图像编码器，USO 为风格参考与内容参考分别设计编码通路：风格图像经 **SigLIP 语义编码器**提取多层嵌入后，由**轻量分层投影器（Hierarchical Projector）** 提取并拼接多尺度细节特征 $z_s$；内容图像则通过 VAE 编码。这种显式解耦使模型能够独立处理风格与身份信息，消融实验表明，将其替换为单共享 VAE 会导致几乎所有指标下降（CLIP-I 从 0.647 降至 0.594，CSD 从 0.556 降至 0.491）。

### 3. 辅助风格奖励（ASR）

USO 在流匹配损失 $\mathcal{L}_{\mathrm{Pre}}$ 的基础上引入辅助风格奖励损失 $\mathcal{L}_{\mathrm{ASR}}$，在线计算参考风格图像与生成图像之间的风格相似度奖励并反传梯度。最终训练目标为：

$$\mathcal{L} = \mathcal{L}_{\mathrm{Pre}} + \lambda \mathcal{L}_{\mathrm{ASR}}, \quad \lambda = 0 \text{ before step } S, \lambda = 1 \text{ thereafter.}$$

该设计在预训练阶段（前 $S$ 步）仅使用流匹配损失，之后激活 ASR。值得注意的是，ASR 虽然仅依赖风格奖励，却能有效增强身份一致性——消融实验中移除 ASR 导致 CSD 大幅下降（0.556 vs. 0.491），CLIP-I 与 CLIP-T 也有所降低。

### 4. 随机条件丢弃训练

为保持模型同时胜任主题驱动、风格驱动及联合风格-主题驱动任务的能力，USO 采用随机条件丢弃策略：以 $p=0.25$ 的概率随机丢弃风格参考或主题参考。这使单模型无需切换架构即可覆盖全部三个子任务。

上述四个改进维度相互协同：跨任务数据整理为解耦编码器提供高质量训练样本，解耦编码器为 ASR 提供独立的风格特征空间，ASR 通过风格奖励间接强化身份保持，而随机条件丢弃则保证模型在统一框架下的多任务泛化能力。

USO 提出了一个**跨任务协同解耦范式**，将主体驱动生成作为主任务、风格驱动生成作为辅助任务，在单一模型中统一优化。其核心在于构建一个**循环数据-模型框架**：通过“主体为风格”的数据整理管道生成高质量三元组，再通过“风格为主体”的模型训练管道实现双向增强。

### 数据整理管道

数据整理管道的目标是系统性地生成**布局保留**与**布局偏移**两类三元组（内容图像、风格图像、风格化内容图像），桥接主题与风格任务（Figure 2）。该管道依赖两个专家模型：

- **Stylization Expert**：基于 UNO-SFT 微调的风格化专家，能够生成高风格相似度且无内容泄漏的风格化图像。
- **De-stylization Expert**：利用冻结的 FLUX.1 Kontext dev 实现去风格化，将风格图像反转为写实图像，利用其强大的指令编辑能力。

通过这两个专家的协同，管道产出的三元组既保留了内容的结构信息，又引入了风格变化，为后续统一训练提供了跨任务监督信号。

### 模型训练框架

USO 的训练框架以单流匹配模型为基础，通过三个关键设计实现统一优化（Figure 3）：

![[assets/figures/papers/paper_list_l2708_https_openaccess_thecvf_com_content_CVPR2026_html_Wu_Unified_Customized/figures/003_Figure_3.jpg]]
*Figure 3: Ilustration of the training framework of USO*

1. **解耦条件编码器**：风格参考图像经 SigLIP 语义编码器提取嵌入后，送入轻量**分层投影器**提取多尺度细节特征，拼接为风格令牌序列 $z_s$；内容参考图像则通过 VAE 编码为内容令牌 $z_c$。两者显式解耦，最终与文本令牌 $c$、时间步令牌 $z_t$ 拼接为多模态输入序列：
   $$z_2 = \mathrm{Concatenate}(z_s, c, z_t, z_c)$$

2. **随机条件丢弃训练**：以概率 $p=0.25$ 随机丢弃风格参考或主体参考，使单一模型同时胜任主题驱动、风格驱动及风格-主体联合驱动三类任务，避免任务间干扰。

3. **辅助风格奖励**：在线计算生成图像与风格参考之间的风格相似度奖励，作为辅助损失反向传播梯度。该奖励虽仅依赖风格信号，却能间接增强身份一致性——这一现象源于跨任务协同解耦：风格任务学会“包含”风格特征的过程，恰好帮助主体任务更有效地“排除”风格干扰，从而更精准地保留身份特征。

### 训练目标

最终训练损失由流匹配损失与辅助风格奖励损失组合而成：
$$\mathcal{L} = \mathcal{L}_{\mathrm{Pre}} + \lambda \mathcal{L}_{\mathrm{ASR}}$$
其中 $\lambda$ 在预训练步骤 $S$ 前为 0，之后切换为 1。这种两阶段策略确保模型先建立稳定的生成能力，再引入风格奖励进行精细化对齐。

### 输入输出流

- **输入**：风格参考图像 $I_{\mathrm{ref}}^s$、主体参考图像 $I_{\mathrm{ref}}^c$（可缺省）、文本提示。
- **编码**：风格参考经 SigLIP + 分层投影器编码为 $z_s$，主体参考经 VAE 编码为 $z_c$，文本经 T5 编码为 $c$。
- **生成**：拼接后的多模态序列送入 DiT 主干，经流匹配 ODE 采样生成目标图像。
- **奖励反馈**：生成图像与风格参考通过预训练奖励模型计算风格相似度，梯度反传至 DiT 主干。

USO 的训练框架围绕“以主体驱动为主任务、风格驱动为辅助任务”的统一范式构建，其核心由四个关键模块协同构成：**跨任务三元组数据整理管道**、**解耦条件编码器**、**随机条件丢弃训练策略**以及**辅助风格奖励（ASR）损失**。

### 跨任务三元组数据整理管道

该管道是 USO 实现跨任务协同解耦的数据基础，通过两个专家模型桥接主题与风格任务：

- **Stylization Expert（风格化专家）**：基于 UNO-SFT 微调，将内容图像渲染为高风格相似度且无内容泄漏的风格化图像，用于生成保留布局的三元组。
- **De-stylization Expert（去风格化专家）**：利用冻结的 FLUX.1 Kontext dev 的指令编辑能力，将风格图像反转为写实图像，从而产生布局偏移的三元组。

两个专家协同工作，系统性地生成 **布局保留** 与 **布局偏移** 两类三元组数据，为主体驱动和风格驱动任务提供统一的训练信号。

### 解耦条件编码器

USO 对不同类型条件图像采用显式解耦的编码策略：

- **内容参考图像** 通过标准 VAE 编码，提取空间结构特征。
- **风格参考图像** 则经过 SigLIP 语义编码器提取多层嵌入 $\{c_i\}_{i=1}^N$，再通过轻量级 **Hierarchical Projector**（分层投影器）进行多尺度特征融合：

$$z_{s} = \mathrm{Concatenate}(\mathcal{M}_{\mathrm{Proj}}(\{c_i\}_{i=1}^{N}))$$

其中 $\mathcal{M}_{\mathrm{Proj}}$ 将 SigLIP 不同层的嵌入投影并拼接，得到富含细粒度视觉细节的风格令牌 $z_s$。

最终的多模态输入序列由风格令牌、文本令牌、时间步令牌和内容令牌拼接而成：

$$z_{2} = \mathrm{Concatenate}(z_{s}, c, z_{t}, z_{c})$$

这种显式解耦设计使得风格与内容特征在输入端即被分离，为后续的跨任务协同优化提供了结构基础。

### 随机条件丢弃训练策略

为使单一模型同时胜任主体驱动、风格驱动以及联合风格-主体驱动三种任务，USO 在训练时以概率 $p = 0.25$ 随机丢弃风格参考或主体参考。该策略迫使模型在部分条件缺失的情况下仍能保持生成能力，从而在推理时灵活应对不同任务需求。

### 辅助风格奖励损失

USO 的训练目标由两部分组成：基础的流匹配损失 $\mathcal{L}_{\mathrm{Pre}}$ 和辅助风格奖励损失 $\mathcal{L}_{\mathrm{ASR}}$。

**流匹配损失** 沿用了扩散模型的标准训练目标：

$$\mathcal{L}_{\mathrm{Pre}} = \mathbb{E}_{\pmb{x}_0, t, \epsilon} [w(t) \| \pmb{v}_{\theta} - \pmb{v}_t \|^2]$$

其中 $w(t)$ 为时间步权重函数，$\pmb{v}_{\theta}$ 为模型预测的速度场，$\pmb{v}_t$ 为真实速度场。

**辅助风格奖励损失** 是 USO 实现跨任务协同增强的关键机制。该损失在线计算生成图像 $\hat{I}_0$ 与风格参考图像 $I_{\mathrm{ref}}^s$ 之间的风格相似度奖励：

$$\mathcal{L}_{\mathrm{ASR}} = \mathbb{E}[\phi(\mathcal{M}_{\mathrm{RM}}(I_{\mathrm{ref}}^s, \hat{I}_0))]$$

其中 $\mathcal{M}_{\mathrm{RM}}$ 为风格奖励模型，$\phi$ 为奖励到损失的映射函数。尽管该损失仅显式优化风格相似度，但实验表明它同时能有效增强身份一致性——这正是跨任务协同解耦的核心体现：风格任务学会“包含”风格特征的过程，反过来帮助主体任务更有效地“排除”风格干扰。

最终组合训练损失为：

$$\mathcal{L} = \mathcal{L}_{\mathrm{Pre}} + \lambda \mathcal{L}_{\mathrm{ASR}}, \quad \lambda = 0 \text{ before step } S, \lambda = 1 \text{ thereafter.}$$

在训练的前 $S$ 步中 $\lambda = 0$，模型仅通过流匹配损失学习基础生成能力；之后 $\lambda$ 切换为 1，ASR 损失被激活，引导模型在保持内容一致性的同时提升风格保真度。这种分阶段训练策略避免了早期阶段风格奖励信号对生成质量的不稳定影响。

## 实验与关键发现

### 主实验结果

USO 在自建基准 USO-Bench 上对三类任务进行了统一评估，涵盖主题驱动、风格驱动以及风格-主题联合驱动。表 1 汇总了定量结果（详见 **Table 1**）。在主题驱动任务上，USO 的 CLIP-I 达到 0.647，CLIP-T 达到 0.287，分别超出此前 SOTA 方法 **UNO** (Wu et al., 2025) 约 0.042 和 0.023。在风格驱动任务上，USO 同时取得最高的 CSD（0.556）和 CLIP-T（0.286），确立新的 SOTA。在更具挑战的风格-主题联合驱动任务上，USO 的 CSD 达到 0.492，CLIP-T 达到 0.283，相比 **OmniStyle** (Wang et al., CVPR 2025) 分别大幅提升 0.127 和 0.054。值得注意的是，在 USO 整理的数据集上复现的 UNO* 和 OmniStyle* 亦获得部分提升，证明跨任务三元组数据管道的独立贡献。

![[assets/figures/papers/paper_list_l2708_https_openaccess_thecvf_com_content_CVPR2026_html_Wu_Unified_Customized/figures/008_Table_1.jpg]]
*Table 1: Quantitative results on USO-Bench. We highlight the best and second-best values for each metric*

### 消融研究

消融实验围绕两个核心组件展开：解耦条件编码器（DE）和辅助风格奖励（ASR），结果列于 **Table 2** 与 **Figure 7**。移除 ASR 后，CSD 从 0.556 骤降至 0.491，CLIP-I 和 CLIP-T 也同步下降，表明 ASR 虽仅依赖风格奖励，却对身份一致性产生正向溢出效应。将解耦编码器替换为单共享 VAE（w/o DE）后，几乎所有指标均出现退化（CLIP-I 0.594、CLIP-T 0.269、CSD 0.491），验证了风格与内容特征显式分离编码的必要性。**Figure 7** 的奖励曲线进一步揭示：ASR 在训练后期持续推高风格相似度，同时带动身份奖励同步上升，形成跨任务协同增强。

![[assets/figures/papers/paper_list_l2708_https_openaccess_thecvf_com_content_CVPR2026_html_Wu_Unified_Customized/figures/010_Figure_7.jpg]]
*Figure 7: Ablation study of ASR.ASR enhances identity consistency even though it relies solely on style reward*

### 关键图表结论

- **Table 1 / Table 3**：USO 在主题驱动、风格驱动及联合驱动三项任务上全面领先，跨任务协同解耦范式带来一致且显著的性能增益。
- **Table 2**：ASR 与解耦编码器均为关键组件，移除任一组件均导致 CSD、CLIP-I、CLIP-T 的明显衰退。
- **Figure 7**：ASR 的定性对比与奖励曲线证实，风格奖励信号可间接强化身份保持，是跨任务互促机制的直接证据。

![[assets/figures/papers/paper_list_l2708_https_openaccess_thecvf_com_content_CVPR2026_html_Wu_Unified_Customized/figures/011_Table_3.jpg]]
*Table 3: Quantitative results on USO-Bench.* denotes models reproduced on our USO dataset*

![[assets/figures/papers/paper_list_l2708_https_openaccess_thecvf_com_content_CVPR2026_html_Wu_Unified_Customized/figures/009_Figure.jpg]]
*Figure: (a) Qualitative comparison (b)Reward on identity similarity (subject-driven) (c)Reward on style similarity (style-driven)*

![[assets/figures/papers/paper_list_l2708_https_openaccess_thecvf_com_content_CVPR2026_html_Wu_Unified_Customized/figures/005_Figure_4.jpg]]
*Figure 4: Qualitative comparison with different methods on subject-driven generation*

## 定位与知识库关联

### 1. 任务定位与核心突破

USO 面向**主题驱动生成**（subject-driven generation）与**风格驱动生成**（style-driven generation）这两类长期独立演进的定制生成任务。现有方法各自围绕单一任务设计解耦策略：主题驱动方法（如 **RealCustom++** (Mao et al., 2024)、**UNO** (Wu et al., 2025)、**OmniGen2** (Wu et al., 2025)、**BAGEL** (Deng et al., 2025)、**FLUX.1 Kontext dev** (Black Forest Labs et al., 2025)）致力于从参考图像中提取并保留主体身份特征；风格驱动方法（如 **StyleStudio** (Lei et al., CVPR 2025)、**DreamO** (Mou et al., 2025)、**CSGO** (Xing et al., 2024)、**InstantStyle** (Wang et al., 2024)、**DEADiff** (Qi et al., CVPR 2024)）则专注于分离并迁移风格特征。少数工作如 **OmniStyle** (Wang et al., CVPR 2025) 和 **StyleID** (Chung et al., CVPR 2024) 尝试同时处理风格与主体，但本质上仍是两套独立机制的组合，未触及两类任务在特征解耦上的深层互补关系。

USO 的根本性突破在于识别并利用了这样一个事实：**一个任务学会“包含”某类特征，恰恰能帮助互补任务更有效地“排除”这类特征**。基于此，论文提出了**跨任务协同解耦范式**（cross-task co-disentanglement paradigm），将风格驱动与主题驱动生成统一于单一框架内，实现相互增强而非简单叠加。

### 2. 方法演进脉络中的关键变化点

相较于基线方法，USO 在以下四个关键维度上做出了实质性改变：

**（1）训练数据构建方式：从单任务三元组到跨任务协同整理**

传统方法依赖面向单个任务的手工或自动化三元组（通常仅保留布局信息）。USO 构建了一个**跨任务三元组整理框架**（cross-task triplet curation framework），通过两个专家模型桥接主题与风格任务：
- **Stylization Expert**：基于 UNO-SFT 微调的风格化专家，将内容图像转化为高风格相似度且无内容泄漏的风格化图像；
- **De-stylization Expert**：利用冻结的 FLUX.1 Kontext dev 实现去风格化，将风格图像反转为写实图像。

该框架系统性地生成两类三元组——布局保留（layout-preserved）与布局偏移（layout-shifted）——使模型同时学习风格迁移与身份保持。

**（2）风格编码器：从共享 VAE 到分层语义编码**

基线方法通常使用共享 VAE 或简单图像编码器处理风格参考。USO 引入 **SigLIP 语义编码器 + 轻量分层投影器（Hierarchical Projector）**，从 SigLIP 的多层嵌入中提取并连接多尺度细节特征：
$$z _ { s } = \mathrm { C o n c a t e n a t e } ( \mathcal { M } _ { \mathrm { P r o j } } ( \{ c _ { i } \} _ { i = 1 } ^ { N } ) )$$
消融实验表明，将该解耦编码器替换为单共享 VAE 会导致几乎所有指标下降（CLIP-I 降至 0.594，CSD 降至 0.491）。

**（3）多任务训练策略：随机条件丢弃**

USO 以概率 $p=0.25$ 随机丢弃风格或主题参考，使单一模型同时胜任主题驱动、风格驱动及联合风格-主题驱动三种任务模式。这种随机条件丢弃训练（Stochastic Conditioning Dropout）避免了为每种任务维护独立模型的需求。

**（4）损失函数：流匹配损失 + 辅助风格奖励**

在标准流匹配损失 $\mathcal{L}_{\mathrm{Pre}}$ 的基础上，USO 引入了**辅助风格奖励（Auxiliary Style Reward, ASR）**损失：
$$\mathcal{L} = \mathcal{L}_{\mathrm{Pre}} + \lambda \mathcal{L}_{\mathrm{ASR}}, \quad \lambda = 0 \text{ before step } S, \lambda = 1 \text{ thereafter.}$$
其中 $\lambda$ 在预训练步骤 $S$ 后由 0 切换为 1。ASR 基于参考风格图像与生成图像之间的风格相似度计算奖励期望，反传梯度以增强风格一致性。值得关注的是，ASR 虽仅依赖风格奖励，却能有效增强身份一致性——这一反直觉现象在消融实验中得到验证：移除 ASR 导致 CSD 从 0.556 骤降至 0.491，CLIP-I 与 CLIP-T 也同步下降。

### 3. 与现有工作的关系图谱

**直接对比基线（同一任务赛道）：**
- 主题驱动赛道：USO 在 USO-Bench 上的 CLIP-I（0.647）和 CLIP-T（0.287）均超越 UNO（0.605 / 0.264）及 RealGeneral、OmniGen2 等方法。
- 风格驱动赛道：USO 在 CSD（0.556）和 CLIP-T（0.286）上达到新的 SOTA。
- 风格-主题联合赛道：USO 在 CSD（0.492 vs. 0.365）和 CLIP-T（0.283 vs. 0.229）上显著超越 OmniStyle。

**数据层面的贡献验证：**
在 USO 整理数据集上重新训练 UNO 和 OmniStyle（记为 UNO\* 和 OmniStyle\*）可获得部分提升，证明跨任务三元组整理框架本身对性能有独立贡献，但提升幅度不及 USO 完整方案，说明模型架构与训练策略的改进同样关键。

### 4. 适用边界与局限

论文未明确讨论方法局限性，以下分析基于方法设计与实验设置推断：

- **评估基准的潜在偏向**：主要结果均在提出的 USO-Bench 上报告。新基准的构造可能引入风格或内容的分布偏向，影响结论的泛化性。论文虽提及在 DreamBench 上也有测试，但未展开详细对比。
- **专家模型的依赖性**：数据整理管道依赖 UNO-SFT 和 FLUX.1 Kontext dev 两个外部模型，其性能上限受这些预训练模型质量的约束。若风格化或去风格化专家在某些极端风格或罕见主体上失效，三元组质量将受影响。
- **两阶段训练的调参敏感性**：ASR 损失在步骤 $S$ 后才激活，$S$ 的选择以及 $p=0.25$ 的丢弃概率均为经验设定，对不同数据规模或任务组合的鲁棒性需进一步验证。
- **计算开销**：分层投影器引入多尺度特征提取，ASR 需要在线计算风格相似度奖励并反传梯度，相比单任务基线增加了训练复杂度。论文未报告推理效率对比。

### 5. 开放问题

- **跨任务协同解耦的理论基础**：论文通过实验证明了“包含帮助排除”的现象（ASR 增强身份一致性），但未从表示学习或信息论角度给出形式化解释。这种协同效应的边界条件是什么？是否存在任务冲突的场景？
- **更多任务的扩展性**：当前框架连接了主题与风格两类任务。跨任务协同解耦范式能否推广到其他视觉属性（如姿态、光照、材质）的定制生成？
- **评估体系的完备性**：USO-Bench 作为新提出的基准，其与 DreamBench 等社区标准基准的系统性偏差分析尚不充分。联合风格-主题驱动任务的评估指标（如 CSD + CLIP-I 的权衡）也缺乏统一的社区共识。

## 原文 PDF

![[paperPDFs/CVPR_2026/Unified_Customized_Generation_by_Disentangled_Reward_Modeling.pdf]]
