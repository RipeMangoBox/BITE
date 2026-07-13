---
title: "Unleashing Guidance Without Classifiers for Human-Object Interaction Animation"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Unleashing_Guidance_Without_Classifiers_for_Human_Object_Interaction_Animation.pdf
project_link: http://ziyinwang1.github.io/LIGHT
code_link: null
openreview_forum_id: 7lgQernr2Z
aliases:
- LLIGHOI
- UGWCHOIA
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: "推理时为不同模态分配异步噪声水平（偏移δ），构建清洁/噪声对比，从数据分布中隐式诱导出接触感知的引导信号。"
primary_logic: "将表示分解为身体、手部和物体模态并分配独立噪声水平，使模型学习到节奏诱导的隐式引导，该引导在无需手工先验的情况下自动关注接触细节；结合保留接触语义的形状谱增强，显著提升对未见过物体的泛化能力。"
claims:
- "LIGHT的节奏诱导引导方向比纯文本CFG与穿透降低梯度更相关（余弦相似度更高），表明其能自动减少穿透伪影。"
- "启用节奏引导后FID从0.196降至0.148，交互F1从0.599升至0.627。"
- "分离手部令牌能减少抓取伪影，提升手部-物体对齐。"
- "形状谱增强显著改善未见物体下的交互度量，In-category Top-1 R-Precision从0.216提升至0.279。"
---

# Unleashing Guidance Without Classifiers for Human-Object Interaction Animation

> [!tip] 核心洞察
> 将表示分解为身体、手部和物体模态并分配独立噪声水平，使模型学习到节奏诱导的隐式引导，该引导在无需手工先验的情况下自动关注接触细节；结合保留接触语义的形状谱增强，显著提升对未见过物体的泛化能力。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 释放无需分类器的引导用于人机交互动画 |
| 英文题名 | Unleashing Guidance Without Classifiers for Human-Object Interaction Animation |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=7lgQernr2Z) · [Project](http://ziyinwang1.github.io/LIGHT) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | LIGHT (Learning Implicit Guidance for Human-object inTeraction) |
| Dataset | InterAct, OMOMO |

> [!tip] 效果简介
> - InterAct 上，FID 为 0.148 (LIGHT w/ guidance)，对比 0.215 (InterDiff)，变化 -0.067。
> - InterAct 上，Interaction C_F1 为 0.627，对比 0.584 (InterDiff)，变化 +0.043。
> - OMOMO 上，FID 为 0.099，对比 0.163 (InterDiff)，变化 -0.064。

## 概要

人机交互（HOI）动画生成的核心瓶颈在于：扩散模型难以在长时序生成中维持精细且持续的接触控制。现有方案或依赖手工设计的接触先验（如**HOI-Diff**，Peng et al., 2023），或借助外部分类器进行引导，泛化性与推理效率均受制约。

LIGHT 的核心洞察是**将表示分解为身体、手部与物体三个独立模态，并为每个模态分配异步的噪声水平**。这种设计使模型在推理时通过构造“清洁/噪声”对比，从数据分布中隐式诱导出接触感知的引导信号——无需任何手工接触先验或外部分类器。具体而言，LIGHT 的节奏诱导引导（pace-induced guidance）方向与穿透降低梯度之间的余弦相似度显著高于纯文本 CFG（Table 4），表明其能自动关注并减少穿透伪影。

在方法定位上，LIGHT 将 diffusion forcing 框架拓展为一种引导机制，区别于**CHOIS**（Li et al., 2023a）的多任务学习与**InterDiff**（Xu et al., 2023b）的运动学预测器迭代修正范式。其关键改动包括三项：模态令牌分离、节奏诱导引导、以及保留接触语义的形状谱增强。

实验结果表明，LIGHT 在 InterAct 数据集上取得 FID 0.148、交互 C_F1 0.627，较 InterDiff 分别改善 0.067 和 0.043（Table 1）。形状谱增强使未见物体的 In-category Top-1 R-Precision 从 0.216 提升至 0.279（Table 3），验证了跨物体泛化能力。主要局限在于仅支持单物体场景，且推理计算成本约为基线的 5 倍。



人机交互（Human-Object Interaction, HOI）动画生成是计算机视觉与图形学中的核心挑战，其目标是根据文本描述或物体几何信息，生成真实、物理合理的人体运动序列。近年来，扩散模型在人体运动生成领域取得了显著进展，但在涉及人与物体精细接触的场景中，现有方法仍面临根本性瓶颈。

**核心瓶颈**在于：扩散模型在生成HOI动画时缺乏精细且持续的接触控制。现有方案通常依赖两类策略来弥补这一缺陷——要么引入手工设计的接触先验（如预定义的接触图或可供性预测），要么在推理时借助外部分类器提供引导信号。这两类方案均存在明显的泛化性与效率问题：手工先验难以覆盖多样化的交互模式，而外部分类器引导（classifier guidance）需要额外训练判别模型，增加了系统复杂度与计算开销。

具体而言，当前代表性工作面临的局限包括：

- **HOI-Diff**（Peng et al., 2023）将扩散模型与辅助可供性预测模块结合，以显式引导接触生成，但可供性预测本身依赖于物体类别的先验知识，泛化到未见过物体时性能下降。
- **CHOIS**（Li et al., 2023a）采用多任务学习联合预测接触与物体运动，然而联合优化的耦合性限制了各模态的独立建模能力。
- **InterDiff**（Xu et al., 2023b）通过运动学预测器迭代修正接触偏差，属于后处理式修正而非从生成过程中根本解决接触质量问题。
- **Text2HOI**（Cha et al., 2024）直接从文本生成HOI序列，但在缺乏显式接触约束时，生成的交互动作常出现穿透伪影或抓取不准确。

上述方法的共同缺陷在于：它们将身体、手部与物体状态视为单一统一表示，未能充分利用各模态在交互中的差异化角色。这种“一刀切”的建模方式使得模型难以自动关注接触细节——手部动作的精细度、物体与人体表面的几何关系等关键信息在统一的噪声扰动与去噪过程中被稀释。

**本文的动机**正是突破这一瓶颈：能否在不依赖任何手工接触先验或外部分类器的前提下，从数据分布中隐式诱导出接触感知的引导信号？LIGHT（Learning Implicit Guidance for Human-object inTeraction）提出了一条新路径——通过将表示分解为身体、手部和物体三个独立模态，并在推理时为不同模态分配异步噪声水平，构建清洁/噪声对比，从而在不引入额外先验的条件下，自动产生关注接触细节的引导效果。



## 核心方法与创新机理

LIGHT的核心创新在于将扩散模型的去噪过程从“全体同步”转变为“模态异步”，从而在不引入任何外部分类器或手工接触先验的条件下，隐式地诱导出接触感知的引导信号。这一设计围绕三个相互关联的**changed slots**展开。

### 1. 模态令牌分离：从单一序列到独立模态

现有扩散式HOI生成方法（如**InterDiff** (Xu et al., 2023b)、**CHOIS** (Li et al., 2023a)）通常将身体、手部和物体的运动表示合并为单一令牌序列进行处理。LIGHT将其**拆分为独立的模态令牌**——身体、手部和物体各自拥有独立的噪声水平与去噪轨迹。

这一分离的因果效应直接体现在抓取质量上：当手部与身体共享同一令牌时，模型倾向于产生不真实的抓取伪影（如手指穿透物体或悬空）；分离后，手部令牌能够独立建模精细的手指运动，显著改善手部-物体对齐（**Figure 4**）。定量消融表明，完全分离方案（身体-手部分离 + 人-物体分离）在R-Precision和FID上均优于合并方案（**Table 2**）。

### 2. 节奏诱导引导：从文本CFG到清洁/噪声对比

标准扩散模型在推理时仅依赖文本条件的无分类器引导（CFG），缺乏对接触细节的显式约束。LIGHT引入**节奏诱导引导**，其机制如下：

- 推理时维护两条去噪路径：**统一调度**对所有模态同步去噪，**阶段调度**则对指定模态（如人体）分配更低的噪声水平（偏移 $\delta$），使其保持更“清洁”的状态。
- 将阶段调度中清洁模态的轨迹作为条件输入，与统一调度的噪声轨迹形成对比，产生引导方向：
  $$\tilde{\pmb{x}}_S = \mathcal{G}_{\theta}(x_S(\lambda), \lambda, d) + \omega_1 (\mathcal{G}_{\theta}(\ldots, \emptyset) - \ldots) + \omega_2 (\mathcal{G}_{\theta}(x_S', \lambda', d) - \mathcal{G}_{\theta}(x_S(\lambda), \lambda, d))$$
  其中 $\omega_2$ 控制节奏引导强度，$x_S'$ 和 $\lambda'$ 来自阶段调度中偏移后的清洁轨迹。

这一设计的**决定性证据**来自梯度方向分析（**Table 4**）：LIGHT的引导方向与穿透降低梯度的余弦相似度显著高于纯文本CFG，表明其能自动感知并减少穿透伪影，而无需显式的穿透损失函数。启用节奏引导后，FID从0.196降至0.148，交互F1从0.599升至0.627（**Table 1**）。

### 3. 接触感知的形状谱增强：从无增强到保留接触语义的重定向

为提升对未见过物体的泛化能力，LIGHT提出**形状谱增强**：将原始动作中的人体运动重定向到新颖物体上，同时通过优化保持原始人-物接触点的语义一致性。与无增强训练相比，该策略在未见物体上的In-category Top-1 R-Precision从0.216提升至0.279（**Table 3**），且增强数据的质量与真实标注接近（**Table A**）。

### 创新总结

三个changed slots形成递进关系：**令牌分离**为异步去噪提供结构基础，**节奏诱导引导**利用这一结构从数据分布中隐式提取接触信号，**形状谱增强**则弥补数据多样性不足的短板。三者的协同使得LIGHT在无需手工接触先验或外部分类器的前提下，实现了对接触细节的精细控制和对未见物体的鲁棒泛化。



![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_7lgQernr2Z/figures/002_Figure_2.jpg]]
*Figure 2: Overview of LIGHT. Left: Training. We form different modalities, e.g., body, hand, and object, each diffused with its own noise level. After adding modal-wise and frame-wise rotary positional encodings, the tokens are processed by a shared Transformer decoder and an MLP head to predict clean motion. Right: Inference. We compare a uniform schedule that denoises all modalities synchronously with a staged schedule that keeps one modality cleaner from the uniform run*

LIGHT（Learning Implicit Guidance for Human-object inTeraction）将人机交互动画生成形式化为一个条件扩散生成问题：给定文本提示与物体几何，合成一段包含人体运动与物体轨迹的3D交互动画序列。框架的核心设计围绕三个关键模块展开：**多模态令牌分解**、**异步扩散调度**与**节奏诱导引导**。

### 输入表示与令牌化

每帧的人机状态被分解为三个独立的模态令牌：

- **身体令牌** $\mathbf{x}_t^b$：编码人体关节位置与全局朝向；
- **手部令牌** $\Delta\mathbf{x}_t^h$：编码手部关节旋转角的残差变化；
- **物体令牌** $\Delta\mathbf{x}_t^o$：编码物体平移与6D旋转的残差变化。

每个令牌附加模态级位置编码与帧级旋转位置编码，使Transformer解码器能区分模态身份与时序位置。物体几何则通过Basis Point Set（BPS）描述符从1024点的点云编码，并与归一化BPS及物体原始尺度拼接，形成物体几何令牌，注入解码器的交叉注意力层。文本提示由冻结的DistilBert编码，同样通过交叉注意力融入模型。

### 训练：扩散强制与异步噪声

训练采用扩散强制（Diffusion Forcing）框架，其核心特点是允许为每个令牌分配独立的噪声水平 $\pmb{\lambda}$，而非全局统一的时间步。训练目标为最小化干净数据预测与真实值的重建误差：

$$\mathcal{L}_{\mathrm{DF}} = \mathbb{E}_{\pmb{x}(0),\pmb{\lambda}} \| \hat{\pmb{x}}(\mathbf{0}) - \mathcal{G}_{\theta}(\pmb{x}(\pmb{\lambda}), \pmb{\lambda}, \pmb{d}) \|^2$$

其中 $\mathcal{G}_{\theta}$ 为共享的Transformer解码器与MLP预测头，$\pmb{d}$ 为文本条件。总损失在此基础上叠加正则化项：

$$\mathcal{L}_{\mathrm{reg}} = \lambda_{\mathrm{fs}} L_{\mathrm{fs}} + \lambda_{\mathrm{v}} L_{\mathrm{v}} + \lambda_{\mathrm{cont}} L_{\mathrm{cont}}$$

分别惩罚脚滑动、速度偏差与接触不一致，促使生成的运动在物理上更合理。

### 推理：双路径去噪与节奏诱导引导

推理时，LIGHT采用双路径策略（见Algorithm 1）：

1. **统一路径（Uniform Schedule）**：所有模态以同步噪声水平去噪，产生基线预测 $\tilde{\pmb{x}}_U$，并结合标准文本CFG更新；
2. **阶段路径（Staged Schedule）**：将模态划分为两个不相交集合 $m_1$ 与 $m_2$（如 $m_1 = \{b, h\}$，$m_2 = \{o\}$），对 $m_1$ 施加偏移 $\pmb{\delta}$，使其以更清洁的状态作为 $m_2$ 的条件输入。

两条路径的对比产生**节奏诱导引导信号**，其更新规则为：

$$\tilde{\pmb{x}}_S = \mathcal{G}_{\theta}(x_S(\lambda), \lambda, d) + \omega_1 (\mathcal{G}_{\theta}(\ldots, \emptyset) - \ldots) + \omega_2 (\mathcal{G}_{\theta}(x_S', \lambda', d) - \mathcal{G}_{\theta}(x_S(\lambda), \lambda, d))$$

其中 $\omega_1$ 控制文本CFG强度，$\omega_2$ 控制节奏引导强度。这一引导信号无需手工设计的接触先验或外部分类器，而是从数据分布中隐式学习到接触感知的修正方向（Table 4证实其与穿透降低梯度的余弦相似度高于纯文本CFG）。

### 数据增强：接触感知的形状谱增强

为提升对未见过物体的泛化能力，LIGHT引入接触感知的形状谱增强：通过优化将原有人类动作重定向到新颖物体，同时保留原始人-物接触点的语义。增强数据在未见物体评估上将In-category Top-1 R-Precision从0.216提升至0.279（Table 3）。

### 模块关系总结

整个pipeline的数据流为：**文本+物体几何 → 多模态令牌化 → 共享Transformer解码器（含自注意力与交叉注意力）→ MLP预测头 → 去噪运动输出**。训练时各令牌接受独立噪声水平；推理时通过双路径对比产生隐式引导，最终输出物理合理、接触精细的HOI动画序列。



LIGHT 的核心架构由六个功能模块构成，其设计围绕一个关键洞察：将人机交互（HOI）表示分解为身体、手部和物体三种模态令牌，并赋予独立的扩散噪声水平，从而在推理时通过异步去噪调度隐式诱导出接触感知的引导信号。

### 模态令牌生成

在每一帧，系统将人体关节位置 $j^p \in \mathbb{R}^{T \times 52 \times 3}$、手部标量旋转角 $j^{r_h} \in \mathbb{R}^{T \times 30}$ 及物体平移与 6D 旋转轨迹分别编码为三个独立的运动令牌：身体令牌 $\mathbf{x}_t^b$、手部令牌 $\Delta\mathbf{x}_t^h$ 和物体令牌 $\Delta\mathbf{x}_t^o$。每个令牌附加模态位置编码和帧级旋转位置编码，使 Transformer 解码器能够区分不同模态来源和时间步长。这一分离策略是后续异步去噪的基础，消融实验表明，完全分离方案（身体-手部 + 人-物体）相比合并方案在 R-Precision 和 FID 上均取得最优结果（Table 2）。

### 噪声水平与时序编码

扩散强迫（Diffusion Forcing）框架允许为每个令牌分配独立的噪声水平 $\boldsymbol{\lambda}$，而非传统扩散模型中所有令牌共享同一噪声尺度。每个令牌同时嵌入其当前噪声水平编码和帧级时序编码，使模型在训练时学会从任意异步噪声状态中恢复干净信号。训练目标为最小化干净数据预测与真实值之间的重建误差：

$$\mathcal{L}_{\mathrm{DF}} = \mathbb{E}_{\pmb{x}(0),\pmb{\lambda}} \| \hat{\pmb{x}}(\mathbf{0}) - \mathcal{G}_{\theta}(\pmb{x}(\pmb{\lambda}), \pmb{\lambda}, \pmb{d}) \|^2$$

其中 $\mathcal{G}_{\theta}$ 为共享 Transformer 解码器，$\pmb{d}$ 为文本条件。

### 物体几何编码

物体形状通过点云 $\mathcal{P}$ 编码。具体地，将未归一化的基点点集（BPS）描述符与归一化 BPS 拼接，并附加物体最大半径作为额外标量，形成物体几何令牌。该令牌通过交叉注意力注入 Transformer 解码器，使模型感知物体形状信息。结合形状谱增强（将人类动作重定向到新颖物体并保留接触语义），模型对未见过物体的泛化能力显著提升——In-category Top-1 R-Precision 从 0.216 提升至 0.279（Table 3）。

### 文本编码

冻结的 DistilBert 将文本提示编码为条件向量 $\pmb{d}$，注入 Transformer 解码器的交叉注意力层，实现文本到运动的语义对齐。

### Transformer 解码器与预测头

多层 Transformer 解码器通过自注意力和交叉注意力融合所有模态令牌、噪声嵌入、时序编码、物体几何令牌和文本条件。输出经轻量 MLP 预测头映射为最终运动序列。

### 训练目标

总损失由扩散重建损失与正则化损失加权组合：

$$\mathcal{L}_{\mathrm{reg}} = \lambda_{\mathrm{fs}} L_{\mathrm{fs}} + \lambda_{\mathrm{v}} L_{\mathrm{v}} + \lambda_{\mathrm{cont}} L_{\mathrm{cont}}$$

其中脚滑动损失 $L_{\mathrm{fs}}$ 惩罚预测与真实脚部速度偏差：

$$\mathcal{L}_{\mathrm{fs}} = \sum_{t=1}^{T} \sum_{f=1}^{4} c_{t}^{f} \big\| (j_{t,f}^{p} - j_{t-1,f}^{p}) - (\hat{j}_{t,f}^{p} - \hat{j}_{t-1,f}^{p}) \big\|_{2}^{2}$$

接触损失 $L_{\mathrm{cont}}$ 强制预期接触时刻的关节-物体表面距离最小化：

$$L_{\mathrm{cont}} = \sum_{t=1}^{T}\sum_{j=1}^{J} \bigl( d( j_{t,j}^{p}, \hat{V}_{t}^{o} ) \hat{c}_{t}^{j} \bigr)^{2}$$

### 节奏诱导引导

推理时，LIGHT 的核心创新在于将统一去噪调度与阶段式异步调度结合，形成隐式引导信号。统一调度对所有模态同步去噪，并施加标准文本 CFG：

$$\tilde{\pmb{x}}_U = \mathcal{G}_{\theta}(\pmb{x}_U(\pmb{\lambda}), \pmb{\lambda}, \pmb{d}) + \omega_1 (\mathcal{G}_{\theta}(\pmb{x}_U(\pmb{\lambda}), \pmb{\lambda}, \pmb{d}) - \mathcal{G}_{\theta}(\pmb{x}_U(\pmb{\lambda}), \pmb{\lambda}, \emptyset))$$

阶段式调度则将模态划分为两个不相交集合 $m_1$ 和 $m_2$（如 $m_1 = \{\text{body}, \text{hand}\}$，$m_2 = \{\text{object}\}$），为 $m_1$ 分配偏移 $\boldsymbol{\delta}$ 使其更早去噪，构造清洁/噪声对比输入：

$$\pmb{x}_S' = (\pmb{x}_U^{m_1}(\pmb{\lambda}^{m_1} - \pmb{\delta}); \pmb{x}_S^{m_2}(\pmb{\lambda}^{m_2})), \quad \pmb{\lambda}' = ((\pmb{\lambda}^{m_1} - \pmb{\delta}); \pmb{\lambda}^{m_2})$$

最终引导更新融合文本 CFG 与节奏诱导项：

$$\tilde{\pmb{x}}_S = \mathcal{G}_{\theta}(x_S(\lambda), \lambda, d) + \omega_1 (\mathcal{G}_{\theta}(\ldots, \emptyset) - \ldots) + \omega_2 (\mathcal{G}_{\theta}(x_S', \lambda', d) - \mathcal{G}_{\theta}(x_S(\lambda), \lambda, d))$$

其中 $\omega_2$ 控制节奏引导强度，$\delta$ 控制去噪先行偏移。消融实验表明 $\omega_2=4$、$\delta=200$ 在 FID 和穿透之间取得最佳平衡（Figure 6）。梯度方向分析进一步证实，LIGHT 的引导方向与穿透降低梯度的余弦相似度比纯文本 CFG 更高（InterAct 上 +0.035，OMOMO 上 +0.032），表明其能自动减少穿透伪影（Table 4）。



## 实验与关键发现

### 主要结果

LIGHT 在 InterAct 数据集上与四种基线方法进行了全面对比：**HOI-Diff** (Peng et al., 2023)、**CHOIS** (Li et al., 2023a)、**InterDiff** (Xu et al., 2023b) 和 **Text2HOI** (Cha et al., 2024)。Table 1 报告了核心定量结果。


![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_7lgQernr2Z/figures/004_Table_1.jpg]]
*Table 1: Quantitative comparisons on the InterAct dataset (Xu et al., 2025a) between our method and baseline approaches. We report R-Precision with batch sizes 256. object, optimizing the placement so that the original human-object contact points are preserved – the new object’s corresponding points remain consistently matched to the same human contacts. The optimization objectives are detailed in Sec. A.2 of the Appendix*

启用节奏诱导引导后，LIGHT 在所有关键指标上均取得最优。FID 从 InterDiff 的 0.215 降至 **0.148**（降幅 31%），交互 F1 分数（Interaction C_F1）从 0.584 提升至 **0.627**。R-Precision Top-1 达到 0.421，表明文本-运动对齐质量显著优于先前方法。在 OMOMO 数据集上（Table D），LIGHT 同样表现最优：FID 为 0.099（InterDiff 为 0.163），Contact 指标为 0.194，更接近真实值 0.262。

定性对比（Figure 3）显示，LIGHT 生成的交互动作在接触真实性、穿透伪影减少、手指定位精度和文本-运动对齐方面均优于基线。这些改进的核心驱动力来自两个机制：令牌分离策略使手部运动获得独立建模能力，节奏诱导引导则在不依赖手工接触先验的情况下自动关注接触细节。

### 消融实验

**令牌分离策略**（Table 2, Figure 4）。完全分离方案（身体-手部分离 + 人体-物体分离）在所有指标上最优：R-Precision Top-1 为 0.421，FID 为 0.148。仅分离身体-手部而合并人体-物体的方案性能次之，完全不分离的方案最差。Figure 4 的定性对比揭示了关键差异：当身体和手部合并为单一令牌时，抓取动作出现明显伪影（红色虚线框标注），而分离令牌策略能生成更精确的抓取姿态和物体放置。


![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_7lgQernr2Z/figures/005_Table_2.jpg]]
*Table 2: Ablation study of token-separation strategies on the InterAct dataset (Xu et al., 2025a). We report R-Precision with batch size 256*

**节奏诱导引导**（Table 1, Figure 5, Figure 6）。对比 LIGHT 无引导版本与完整版本，引导的引入使 FID 从 0.196 降至 0.148，交互 F1 从 0.599 升至 0.627。Figure 5 的定性示例展示了引导对生成质量的显著提升：无引导时动作缺乏精细接触，完整方法则呈现清晰的接触动态。超参数消融（Figure 6）表明，引导权重 $\omega_2 = 4$ 和去噪偏移 $\delta = 200$ 在 FID 与穿透之间取得最佳平衡；过大的偏移会导致模态间过度发散和突兀融合。


![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_7lgQernr2Z/figures/011_Figure_6.jpg]]
*Figure 6: Ablation study on the schedule-based guidance weight ω2 and denoising preceding offset δ. Left: δ fixed at 200 while varying ω2. Right: $\omega _ { 2 }$ fixed at 4 while varying δ*

**形状谱增强**（Table 3）。数据增强对未见物体的泛化能力至关重要。在类别内未见物体上，增强使 Top-1 R-Precision 从 0.216 提升至 **0.279**（提升 29%），FID 从 0.169 降至 0.153。跨类别未见物体的提升同样一致。增强数据的质量验证（Table A）显示，增强样本的穿透和漂浮指标与真实标注接近，Chamfer 距离的 F1 分数保持较高水平，说明接触语义在重定向过程中得到有效保留。


![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_7lgQernr2Z/figures/009_Table_3.jpg]]
*Table 3: Ablation study. We compare models trained with and without data augmentation on the InterAct dataset (Xu et al., 2025a). Experiments on unseen objects include in-category and cross-category objects never observed during training. We report R-Precision with batch size 256*

### 引导方向分析

Table 4 揭示了 LIGHT 引导的内在机理。将 LIGHT 引导方向 $g_{\mathrm{LIGHT}}$ 与穿透降低梯度 $\nabla L_{\mathrm{pen}}$ 计算余弦相似度，在 InterAct 上为 **0.217+0.035**，在 OMOMO 上为 **0.239+0.032**，均显著高于纯文本 CFG 的 0.217 和 0.239。这表明节奏诱导引导能自动朝向减少穿透伪影的方向更新。同时，LIGHT 引导方向与真实分布方向的相似度（InterAct: 0.401+0.002）与文本 CFG（0.401）持平，说明引导在改善接触质量的同时未牺牲与真实分布的对齐。


![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_7lgQernr2Z/figures/012_Table_4.jpg]]
*Table 4: Comparison of the mean gradient similarity with penetration-descending direction, direction towards GT distribution. δ = 250 is used and mean gradient similarity is calculated on all the guiding steps. we define $\langle \mathbf { a } , \mathbf { b } \rangle$ ~ = ~ $\frac { \mathbf { a } } { \| \mathbf { a } \| } \cdot \frac { \mathbf { \bar { b } } } { \| \mathbf { b } \| }$

### 失败模式与局限

尽管 LIGHT 在主要指标上表现优异，仍存在若干局限。首先，框架仅处理单物体场景，尚未扩展至多物体交互。其次，未显式建模静态环境上下文或场景几何，生成动作的情境真实感可能受限。对于高动态或物理复杂的交互（如快速抛接），模型仍可能产生不合理的接触或穿透。最后，推理计算成本较高：两阶段去噪调度使推理速度比基线慢约 5 倍，难以满足实时部署需求。这些局限指向了未来的改进方向，包括多物体扩展、环境上下文整合以及推理效率优化。

### 补充图表

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_7lgQernr2Z/figures/013_Table_5.jpg]]
*Table 5: Table A: Quantitative evaluation of augmented data quality relative to ground truth annotations*

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_7lgQernr2Z/figures/015_Table_6.jpg]]
*Table 6: Table B: Quantitative evaluation of unconditional generation on the BEHAVE dataset (Bhatnagar et al., 2022). For R-Precision we adopt a batch size of 64. We don’t retrain our model for unconditional generation. (b) Guidance Effect*

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_7lgQernr2Z/figures/018_Table_7.jpg]]
*Table 7: Table C: Ablation of modality combinations m1, m2 on InterAct (Xu et al., 2025a), BEHAVE (Bhatnagar et al., 2022), and OMOMO (Li et al., 2023a) datasets. We report R-Precision with batch size 256. human shape to synthesize a complete HOI sequence without extra conditioning, and (ii) controllable HOI generation, where the model is conditioned on a richer set of inputs—including the full object motion sequence, object mesh, human shape, and a textual description—to generate the corresponding HOI sequence. For both settings, we reuse the model from the main paper without retraining. This is made possible by our independent noise scheduling, which allows the model to noised out unused condition...*

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_7lgQernr2Z/figures/019_Table_8.jpg]]
*Table 8: Table D: Quantitative comparisons on the OMOMO dataset (Li et al., 2023a) between our method and baseline approaches. We report R-Precision with batch size 256*

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_7lgQernr2Z/figures/020_Table_9.jpg]]

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_7lgQernr2Z/figures/021_Table_10.jpg]]
*Table 10: Table F: Ablation study of token-separation strategies on the BEHAVE dataset Xu et al. (2025a). We report R-Precision with batch size 256*




## 定位与知识库关联

### 与现有工作的关系

LIGHT 的核心贡献在于将扩散强制（diffusion forcing）框架扩展为一种**隐式引导机制**，从而在不依赖外部接触先验或分类器的情况下实现精细的人-物交互控制。这一思路与现有基线方法形成鲜明对比：

- **HOI-Diff**（Peng et al., 2023）通过辅助可供性预测网络来引导接触生成，本质上依赖显式的接触先验信号。LIGHT 则完全摒弃了这种手工设计的接触监督，转而从数据分布中隐式诱导接触感知的引导方向。实验表明，LIGHT 的节奏诱导引导方向与穿透降低梯度的余弦相似度比纯文本 CFG 更高（Table 4），这意味着它**自动**学会了减少穿透伪影，而无需显式建模物理约束。

- **CHOIS**（Li et al., 2023a）采用多任务学习联合预测接触与物体运动，但这一范式在面对未见过物体时泛化能力受限。LIGHT 通过**接触感知的形状谱增强**（将原有人类动作重定向到新颖物体并保留接触语义）显著缓解了这一问题：在 In-category 未见物体上，Top-1 R-Precision 从 0.216 提升至 0.279（Table 3）。

- **InterDiff**（Xu et al., 2023b）在扩散模型基础上引入运动学预测器进行迭代修正，属于后处理式的接触偏差校正。LIGHT 则将接触控制**内化到去噪过程本身**——通过为不同模态分配异步噪声水平（偏移 δ），构建清洁/噪声对比，使引导信号在推理时自然涌现。在 InterAct 数据集上，LIGHT 的 FID 从 InterDiff 的 0.215 降至 0.148，交互 C_F1 从 0.584 升至 0.627（Table 1）。

- **Text2HOI**（Cha et al., 2024）同样利用扩散模型从文本生成 HOI 序列，但仅依赖标准文本 CFG。LIGHT 在此基础上叠加了**节奏诱导引导**（pace-induced guidance），其核心机制在于：将身体、手部和物体分离为独立令牌，并为手部/物体模态保留更清洁的去噪轨迹作为条件输入，从而在无额外网络的情况下实现接触细节增强。

### 适用边界

LIGHT 的有效性建立在以下前提之上：

1. **模态可分解性**：方法假设人-物交互可以分解为身体、手部和物体三个独立模态，且各模态的运动模式具有不同的去噪节奏需求。当交互涉及不可分解的耦合运动时（如柔性物体变形），该假设可能不成立。

2. **单物体场景**：当前框架仅处理单物体交互，未扩展至多物体场景。多物体交互需要更复杂的模态划分和调度策略，且引导方向可能在不同物体间产生冲突。

3. **物体几何的静态编码**：物体形状通过 BPS 描述符编码并注入交叉注意力层，这意味着物体在交互过程中被视为刚性体。对于可变形物体或动态变化的物体形状，该方法需要额外的几何编码机制。

4. **文本条件的充分性**：引导方向的质量依赖于文本条件提供的语义锚定。当文本描述模糊或与训练分布偏差较大时，节奏诱导引导可能无法有效补偿语义缺失。

### 局限与开放问题

**已确认的局限**：

- **推理计算成本高**：LIGHT 的推理速度比基线方法慢约 5 倍，这源于两阶段去噪调度（uniform + staged）带来的额外前向传播。这一瓶颈限制了其在实时交互应用中的部署可行性。

- **未建模静态环境上下文**：当前框架仅关注人-物二元交互，未显式整合场景几何或环境约束。生成的动作可能与环境中的障碍物或其他静态结构产生冲突。

- **高动态交互的可靠性不足**：对于物理复杂的快速交互（如抛接、剧烈碰撞），节奏诱导引导可能无法充分捕捉瞬态接触动力学，导致穿透或接触丢失。

**开放问题**：

- **多物体交互扩展**：如何将模态分离和异步调度策略推广至多物体场景？可能的思路包括引入物体间注意力机制或层次化调度策略，但需要解决引导方向在多目标间的分配与平衡问题。

- **环境上下文整合**：如何有效融合场景几何信息以提升生成动作的情境真实感？可考虑将场景点云作为额外模态令牌，或通过场景感知的接触损失进行约束。

- **计算效率优化**：能否在保持引导质量的前提下降低推理开销？潜在方向包括：共享两阶段去噪的中间特征、设计自适应调度策略以减少冗余步骤、或通过知识蒸馏将引导信号压缩至单阶段模型。

- **引导机制的理论理解**：Table 4 表明 LIGHT 的引导方向与穿透降低梯度具有更高相关性，但这一相关性是训练过程中隐式涌现的，其理论根源尚不清晰。进一步分析噪声水平偏移 δ 与引导方向之间的关系，可能揭示扩散模型中条件控制的更深层原理。



## 原文 PDF

![[paperPDFs/ICLR_2026/Unleashing_Guidance_Without_Classifiers_for_Human_Object_Interaction_Animation.pdf]]
