---
title: Synthetic Curriculum Reinforces Compositional Text-to-Image Generation
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Synthetic_Curriculum_Reinforces_Compositional_Text_to_Image_Generation.pdf
project_link: null
code_link: null
aliases:
- SCRCTIG
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过场景图结构量化组合难度并构建自适应合成课程，利用强化学习（GRPO）使模型在从易到难的训练过程中逐步掌握对象存在、属性绑定、关系理解与数量计数等组合子能力。课程调度策略（易到难、高斯采样）和细粒度组合奖励信号是驱动性能提升的关键因果杠杆。
primary_logic: 将组合复杂性分解为场景图的节点数、平均属性密度和平均关系连通性三个可量化因子，并以此为准则构建合成课程进行强化学习训练，使T2I模型无需依赖真实图像或修改架构即可系统提升组合生成性能。
claims:
- CompGen 在 Stable-Diffusion-1.5 和 SimpleAR 两个不同架构上均带来显著提升，五个基准平均提升分别达 11.72% 和 7.61%。
- 提出的难度度量（乘法形式）优于加性基线，平均分提高 4.56 个百分点。
- 自适应 MCMC 采样在成功率和图多样性上显著优于随机拒绝采样和贪婪采样，硬难度下成功率达 91.5%，节点类型多样性 130。
- 课程调度策略对 scaling 行为影响显著：易到难和高斯调度在训练步数增加时持续提升，而随机采样较早饱和。
---

# Synthetic Curriculum Reinforces Compositional Text-to-Image Generation

> [!tip] 核心洞察
> 将组合复杂性分解为场景图的节点数、平均属性密度和平均关系连通性三个可量化因子，并以此为准则构建合成课程进行强化学习训练，使T2I模型无需依赖真实图像或修改架构即可系统提升组合生成性能。

| 字段 | 内容 |
|------|------|
| 中文题名 | 合成课程强化组合文本到图像生成 |
| 英文题名 | Synthetic Curriculum Reinforces Compositional Text-to-Image Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2511.18378) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | CompGen |
| Dataset | GenEval / DPG / TIFA / T2I-CompBench / DSG, GenEval, DSG |

> [!tip] 效果简介
> - GenEval / DPG / TIFA / T2I-CompBench / DSG (平均) 上，Average Accuracy 66.62% (Stable-Diffusion-1.5 w/ ours) vs 54.90% (Stable-Diffusion-1.5) (+11.72%)；Average Accuracy 71.27% (SimpleAR w/ ours) vs 63.66% (SimpleAR-SFT) (+7.61%)。
> - GenEval 上，Accuracy 53.88% (SD-1.5 w/ ours) vs 42.08% (SD-1.5) (+11.80%)。
> - DSG 上，Accuracy 86.11% (SimpleAR w/ ours) vs 71.98% (SimpleAR-SFT) (+14.13%)。

## 概要

文本到图像（T2I）生成模型在组合生成（compositional generation）方面存在系统性弱点，具体表现为对象遗漏、属性绑定错误、空间/语义关系混乱以及数量计数不准确。这些缺陷源于训练过程中缺乏专门针对组合能力的训练信号与难度递进机制。

针对这一瓶颈，本文提出 **CompGen**，一种基于合成课程强化学习的组合生成框架。其核心洞察是：将组合复杂性分解为场景图的节点数、平均属性密度和平均关系连通性三个可量化因子，并以此为准则构建从易到难的合成课程，通过强化学习驱动 T2I 模型逐步掌握对象存在、属性绑定、关系理解与数量计数等组合子能力。该方法无需依赖真实图像或修改模型架构，即可系统提升组合生成性能。

主要实证结论如下：
- 在 **Stable-Diffusion-1.5** 上，CompGen 在 GenEval、DPG、TIFA、T2I-CompBench、DSG 五个基准上平均提升 **11.72%**（从 54.90% 到 66.62%）；在自回归架构 **SimpleAR** 上平均提升 **7.61%**（从 63.66% 到 71.27%），验证了方法的架构无关性（Table 1）。
- 所提出的乘法形式难度度量优于加性基线，平均得分高出 **4.56 个百分点**（Table 3）。
- 细粒度组合奖励（分解为对象、属性、关系、计数四类 VQA 平均分）比单一 VQAScore 带来 **5.2%** 的平均提升（Table 4）。
- 课程调度策略对 scaling 行为影响显著：易到难和高斯调度在训练步数增加时持续提升，而随机采样较早饱和（Figure 5）。

在方法谱系上，CompGen 属于数据驱动的组合生成增强方法，区别于基于注意力调控的 **DenseDiffusion** 和 **CONFORM** 等方法。其训练范式将标准扩散/自回归训练替换为基于合成课程的强化学习（C-GRPO），训练数据由自适应 MCMC 从场景图合成生成，奖励信号采用细粒度组合 VQA 评分，难度调度采用易到难或高斯采样策略。该方法与 Stable-Diffusion-1.5、SimpleAR-SFT 等基线模型以及 SDXL、Lumina-Next 等更大规模模型进行了系统对比。

值得注意的是，CompGen 的性能依赖于多模态奖励模型（如 LLaVA-v1.6-13B）的评估品质，且目前仅在 1B 参数以下的模型上验证；在更大规模模型上的 scaling 特性及合成数据生成的计算开销仍需进一步探索。

文本到图像（T2I）生成模型近年来取得了显著进展，但在**组合生成**（compositional generation）方面仍暴露出系统性弱点。具体表现为：对象遗漏（object omission）、属性错误绑定（attribute misbinding）、空间与语义关系混乱（relational confusion），以及数量计数不准确（counting errors）。这些缺陷并非偶然，而是源于现有训练范式缺乏专门针对组合能力的训练信号与难度递进机制。

现有方法大致分为三类，但均未能从根本上解决上述瓶颈：

1. **基于注意力的方法**（如 DenseDiffusion、CONFORM）通过操纵交叉注意力图来强化特定对象或属性的生成，但这类方法往往需要在推理阶段引入额外输入或计算，且对复杂组合场景的泛化能力有限。
2. **基于布局的方法**要求用户提供空间布局或分割掩码作为条件，虽然能改善空间关系生成，但增加了使用门槛，且难以覆盖属性绑定和计数等非空间组合维度。
3. **基于微调的方法**利用人工标注的组合性数据对模型进行监督微调，但高质量组合标注数据稀缺、成本高昂，且固定数据集难以覆盖组合空间的多样性。

上述方法的共同局限在于：**缺乏对组合难度的量化建模与自适应训练调度**。具体而言，现有工作既未系统定义“什么样的文本-图像对在组合意义上更难”，也未设计从易到难的课程学习机制来逐步强化模型的组合子能力（对象存在、属性绑定、关系理解、数量计数）。

本文的核心动机正是填补这一空白。我们提出 **CompGen**——一个基于合成课程的组合强化学习框架。其核心洞察在于：**将组合复杂性分解为场景图（scene graph）的结构化因子，并以此为准则构建自适应合成课程，使 T2I 模型无需依赖真实图像或修改架构即可系统提升组合生成性能**。具体而言，CompGen 通过场景图的节点数、平均属性密度和平均关系连通性三个可量化因子来定义组合难度，并利用强化学习（GRPO）在从易到难的课程调度下逐步掌握组合子能力。这一数据驱动、课程引导的范式为 T2I 组合生成问题提供了新的解决路径。

## 核心方法与创新机理

CompGen 的核心创新在于将组合生成能力不足这一系统性瓶颈归因于**缺乏专门针对组合能力的训练信号与难度递进机制**，并提出了一套无需真实图像、无需修改模型架构的数据驱动解决方案。其关键创新点可归纳为三个相互耦合的 changed slots：

### 1. 训练范式：从标准微调到课程化强化学习（C-GRPO）

现有 T2I 模型通常依赖标准扩散/自回归训练或监督微调，缺乏对组合生成能力的显式优化目标。CompGen 将训练重新定义为基于合成课程的强化学习问题，采用课程化组内相对策略优化（C-GRPO）。具体而言，模型在每组 $G$ 张图像内计算课程加权的优势函数：

$$A_i(t) = \frac{\widehat{r}^{(i)}(t) - \mathrm{Mean}(\{\widehat{r}^{(k)}(t)\}_{k=1}^G)}{\mathrm{Std}(\{\widehat{r}^{(k)}(t)\}_{k=1}^G)}$$

并以此驱动带剪辑和 KL 正则的策略更新：

$$\mathcal{J}_{\mathrm{C-GRPO}}(\theta) = \mathbb{E}_T \left[ \frac{1}{G} \sum_{i=1}^G \left( \min\left( \frac{\pi_\theta}{\pi_{\theta_{\mathrm{old}}}} A_i(t), \mathrm{clip}\left( \frac{\pi_\theta}{\pi_{\theta_{\mathrm{old}}}}, 1-\epsilon, 1+\epsilon \right) A_i(t) \right) - \beta \mathrm{KL}(p_\theta(\cdot|T) || p_{\mathrm{ref}}(\cdot|T)) \right) \right]$$

这一范式转变使得模型能够直接从组合奖励信号中学习，而非间接地从图文对齐中隐式获取组合能力。证据强度高：在 Stable-Diffusion-1.5 上平均提升 11.72%，在 SimpleAR 上提升 7.61%（Table 1）。

### 2. 训练数据来源：自适应 MCMC 合成场景图课程

传统方法依赖人工标注或预训练图文对，组合多样性受限且难度不可控。CompGen 通过自适应 MCMC 采样从场景图空间合成训练数据，核心在于：

- **难度量化**：将场景图 $\mathcal{G}$ 的组合难度定义为对象数量、平均属性密度和平均关系连通性三者的乘积：

$$\operatorname{Diff}(\mathcal{G}) = \|\mathcal{O}\| \cdot \max\left(1, \frac{\|A\|}{\|\mathcal{O}\|}\right) \cdot \max\left(1, \frac{\|\mathcal{R}\|}{\|\mathcal{O}\|}\right)$$

- **约束采样**：以目标难度区间 $[\mathrm{Diff}_{\min}, \mathrm{Diff}_{\max}]$ 为约束，通过 MCMC 采样生成多样化场景图，能量函数衡量图难度与目标区间的偏离程度：

$$\mathrm{Energy}(\mathcal{G}) := \mathrm{Dist}(\mathrm{Diff}(\mathcal{G}), [\mathrm{Diff}_{\min}, \mathrm{Diff}_{\max}])$$

- **图到文转换**：通过受约束的 LLM 生成（强制包含、结构验证、多阶段校验）将场景图转化为严格匹配其组成结构的自然语言描述。

该合成管道使训练数据在 1–10 难度级别上均匀分布，且无需任何真实图像。消融实验证实，均匀覆盖所有难度级别的数据分布显著优于仅使用简单样本（+25.77 pp）或困难样本（+24.24 pp）的偏斜分布（Table 5），而自适应 MCMC 在硬难度下成功率达 91.5%，节点类型多样性达 130（Table 6）。

### 3. 奖励信号：细粒度组合奖励解耦

现有方法多采用单一 VQAScore 或 CLIP 分数作为奖励，无法区分对象遗漏、属性绑定错误、关系混乱和计数不准等不同组合失败模式。CompGen 将奖励信号细粒度分解为四类二值问题的 VQA 平均分：对象存在、属性绑定、关系理解、数量计数。这些问题由场景图程序化自动生成，并由多模态奖励模型（LLaVA-v1.6-13B）计算“是”概率。

细粒度组合奖励相比单一 VQAScore 带来 5.2 个百分点的平均提升（Table 4），表明将奖励解耦为多个子维度能更有效地引导组合生成学习。这一设计直接对应了 T2I 模型组合失败的四个主要维度，使优化信号更具针对性和可解释性。

### 4. 难度调度：课程化采样策略

CompGen 引入了三种课程调度策略（随机、易到难、高斯采样），在训练过程中动态调整不同难度样本的采样概率。实验表明，易到难和高斯调度策略在训练步数增加时持续提升，而随机采样较早饱和（Figure 5），揭示了课程调度对模型 scaling 行为的关键影响——正确的难度递进顺序能够持续释放组合生成能力的增长潜力。

**总结**：CompGen 的四项 changed slots 构成了一个闭环系统：以场景图难度度量为准则合成可控课程数据，以细粒度组合奖励为优化信号，以课程化 GRPO 为训练范式，以难度调度策略控制学习进程。这一设计使 T2I 模型在不依赖真实图像、不修改架构的前提下，系统性地提升了组合生成性能。

CompGen 框架采用“合成课程构建 + 课程化强化学习训练”两阶段范式，在不依赖真实图像、不修改模型架构的条件下系统提升文本到图像模型的组合生成能力。其核心思路是：**利用场景图的结构化特性量化组合难度，并通过自适应采样生成难度可控的合成训练数据，进而以细粒度组合奖励信号驱动强化学习，使模型在从易到难的课程中逐步掌握对象存在、属性绑定、关系理解与数量计数等组合子能力**。

### 两阶段流水线

框架的整体运行流程（图略，参见原文 Figure 2）可概括为两个紧密衔接的阶段：

![[assets/figures/papers/paper_list_l2344_https_arxiv_org_abs_2511_18378/figures/002_Figure_2.jpg]]
*Figure 2: Overview of our CompGen framework, which is incentivized to construct a curriculum through end-to-end reinforcement learning without requiring ground-truth images*

**第一阶段：合成课程构建。** 该阶段以目标难度区间为输入，通过自适应 MCMC 采样器生成满足难度约束的多样化场景图，再经由 LLM 驱动的提示生成器将场景图转化为严格匹配其组成结构的自然语言描述，同时由程序化 QA 生成器基于场景图自动构建对象、属性、关系、计数四类二值问题。这一过程的输出是一组“文本提示—问题集”对，构成完整的合成训练课程。

**第二阶段：课程化 GRPO 训练。** 该阶段将第一阶段生成的文本提示送入待训练的 T2I 模型生成图像，利用多模态奖励模型（LLaVA-v1.6-13B）对每个问题计算“是”的概率，聚合为细粒度组合奖励。奖励信号经课程调度策略加权后，通过组内相对策略优化（C-GRPO）更新模型参数，使模型在训练过程中逐步适应更复杂的组合场景。

### 模块构成与数据流

CompGen 由以下五个核心模块串联构成，模块间的输入输出关系清晰：

1. **难控场景图生成器（Adaptive MCMC Sampler）**：接收目标难度区间 $[\text{Diff}_{\min}, \text{Diff}_{\max}]$ 作为输入，通过 MCMC 迭代采样生成满足难度约束且语义多样化的场景图 $\mathcal{G}$。该模块以能量函数 $\mathrm{Energy}(\mathcal{G}) := \mathrm{Dist}(\mathrm{Diff}(\mathcal{G}), [\mathrm{Diff}_{\min}, \mathrm{Diff}_{\max}])$ 衡量图状态与目标区间的偏离程度，并依据 Metropolis-Hastings 接受概率 $\operatorname{Acc}(\mathcal{G}' | \mathcal{G}) = \min\left(1, \frac{\pi(\mathcal{G}') q(\mathcal{G} | \mathcal{G}')}{\pi(\mathcal{G}) q(\mathcal{G}' | \mathcal{G})}\right)$ 决定是否接受提议的新图状态。实验表明，该自适应 MCMC 方法在硬难度下成功率达 91.5%，节点类型多样性（NTD）达 130，显著优于随机拒绝采样和贪婪采样（Table 6）。

2. **文本提示生成器（LLM-based Prompt Generator）**：将场景图 $\mathcal{G}$ 转化为自然语言描述 $T$。生成过程施加三类严格约束：（i）强制包含约束，确保所有对象、属性和关系均出现在描述中；（ii）结构验证，保证生成的文本与场景图的组成结构完全一致；（iii）多阶段验证，对生成结果进行逐项核对。这一设计避免了自由文本生成可能引入的语义漂移或信息遗漏。

3. **问题-答案对生成器（Programmatic QA Generator）**：基于场景图 $\mathcal{G}$ 自动构建对象存在、属性绑定、关系理解、数量计数四类二值问题，每个问题的正确答案由场景图的结构化信息直接确定。这种程序化方式保证了问题-答案对的精确性和可扩展性，无需人工标注。

4. **多模态奖励模型（MLLM Reward Model）**：对生成的图像 $I$ 计算每个问题 $j$ 的“是”概率 $r_j^{(i)}$，聚合为细粒度组合奖励。该模块采用 LLaVA-v1.6-13B 作为评估骨干，在奖励模型消融实验中取得了最优的平均得分（Table 2），且相较于单一 VQAScore，细粒度组合奖励带来了 5.2 个百分点的平均提升（Table 4）。

5. **课程化 GRPO 优化器（Curriculum-GRPO Trainer）**：将课程调度策略与组内相对策略优化相结合。在第 $t$ 训练步，首先按课程采样概率 $\widehat{p}(t, j')$ 对各难度等级的奖励进行加权求和，得到课程加权奖励 $\widehat{r}_j^{(i)}(t) = \sum_{j'} \widehat{p}(t, j') \cdot r_j^{(i)}$；随后在组内归一化得到优势函数 $A_i(t) = \frac{\widehat{r}^{(i)}(t) - \text{Mean}(\{\widehat{r}^{(k)}(t)\}_{k=1}^G)}{\text{Std}(\{\widehat{r}^{(k)}(t)\}_{k=1}^G)}$；最终通过带剪辑和 KL 正则的目标函数 $\mathcal{J}_{\mathrm{C-GRPO}}(\theta)$ 更新模型参数（Eq. 5）。课程调度策略（易到难、高斯采样）的选择对训练 scaling 行为有显著影响——相较于随机采样较早饱和，易到难和高斯调度在训练步数增加时持续提升（Figure 5）。

### 关键设计：难度度量与课程调度

整个框架的运转建立在场景图难度度量之上。CompGen 将组合难度定义为三个因子的乘积形式：

$$\operatorname{Diff}(\mathcal{G}) = \|\mathcal{O}\| \cdot \max\left(1, \frac{\|A\|}{\|\mathcal{O}\|}\right) \cdot \max\left(1, \frac{\|\mathcal{R}\|}{\|\mathcal{O}\|}\right)$$

其中 $\|\mathcal{O}\|$ 为对象节点数，$\frac{\|A\|}{\|\mathcal{O}\|}$ 为平均属性密度，$\frac{\|\mathcal{R}\|}{\|\mathcal{O}\|}$ 为平均关系连通性。该乘法形式在消融实验中一致优于加性基线，平均得分高出 4.56 个百分点（Table 3），表明三个因子的交互效应——而非简单叠加——更能刻画组合生成的认知复杂度。

在此基础上，课程调度策略决定了不同难度数据在训练过程中的呈现顺序。CompGen 支持随机采样（等概率）、易到难（分阶段切换）和高斯采样（以高斯核在难度轴上滑动）三种调度方式。实验表明，均匀覆盖所有难度级别的训练数据优于仅使用简单或困难样本的倾斜分布，分别高出 25.77 和 24.24 个百分点（Table 5），验证了完整课程覆盖对组合能力培养的必要性。

### 训练数据与适用范围

CompGen 框架在实验中构建了 10K 合成样本，均匀分布于难度等级 1 至 10，并成功应用于扩散架构 Stable-Diffusion-1.5 和自回归架构 SimpleAR-SFT 两种不同生成范式的 T2I 模型。在五个组合生成基准（GenEval、DPG、TIFA、T2I-CompBench、DSG）上，Stable-Diffusion-1.5 的平均准确率从 54.90% 提升至 66.62%（+11.72 pp），SimpleAR-SFT 从 63.66% 提升至 71.27%（+7.61 pp）（Table 1），验证了该框架的架构无关性和有效性。

CompGen 框架的核心技术路径由三个紧密耦合的模块构成：**难控场景图生成器**、**细粒度组合奖励模型**以及**课程化 GRPO 优化器**。这三个模块共同实现了“从场景图难度量化到合成课程构建，再到组合能力强化学习”的闭环。

### 场景图难度度量

CompGen 首先需要一种可量化的方式衡量文本提示的组合复杂度。论文提出基于场景图（Scene Graph）的难度准则，将组合生成的核心挑战分解为三个可独立量化的因子：

- **对象数量** $\|\mathcal{O}\|$：场景图中包含的实体节点总数，反映生成的“容量”需求。
- **平均属性密度** $\|\mathcal{A}\|/\|\mathcal{O}\|$：每个对象平均绑定的属性数量，反映属性绑定难度。
- **平均关系连通性** $\|\mathcal{R}\|/\|\mathcal{O}\|$：每对对象之间平均存在的关系数量，反映空间/语义关系理解难度。

场景图 $\mathcal{G}$ 的组合难度定义为上述三因子的乘积：

$$\operatorname{Diff}(\mathcal{G}) = \|\mathcal{O}\| \cdot \max\left(1, \frac{\|\mathcal{A}\|}{\|\mathcal{O}\|}\right) \cdot \max\left(1, \frac{\|\mathcal{R}\|}{\|\mathcal{O}\|}\right)$$

其中 $\max(1, \cdot)$ 确保当属性或关系密度低于 1 时不会削弱对象数量带来的基础难度。消融实验（Table 3）表明，该乘法形式比多种加性基线（如 $\|\mathcal{O}\|+\|\mathcal{A}\|+\|\mathcal{R}\|$）平均得分高出 4.56 个百分点，验证了因子间乘法交互对难度建模的必要性。

### 自适应 MCMC 场景图采样

为按需生成满足特定难度区间的多样化场景图，CompGen 将场景图生成形式化为马尔可夫链蒙特卡洛（MCMC）采样问题。核心设计包括：

**能量函数**：衡量候选图 $\mathcal{G}$ 的难度与目标区间 $[\mathrm{Diff}_{\min}, \mathrm{Diff}_{\max}]$ 的偏离程度：

$$\mathrm{Energy}(\mathcal{G}) := \mathrm{Dist}\big(\mathrm{Diff}(\mathcal{G}), [\mathrm{Diff}_{\min}, \mathrm{Diff}_{\max}]\big)$$

当 $\mathrm{Diff}(\mathcal{G})$ 落入目标区间时能量为零，否则为正值。由此定义目标分布 $\pi(\mathcal{G}) \propto \exp(-\mathrm{Energy}(\mathcal{G}))$，使难度符合约束的图获得更高概率。

**接受概率**：采用 Metropolis-Hastings 准则决定是否接受提议的新图状态 $\mathcal{G}'$：

$$\operatorname{Acc}(\mathcal{G}' | \mathcal{G}) = \min\left(1, \frac{\pi(\mathcal{G}') q(\mathcal{G} | \mathcal{G}')}{\pi(\mathcal{G}) q(\mathcal{G}' | \mathcal{G})}\right)$$

其中 $q$ 为对称的提议分布，通过添加/删除对象节点、属性边或关系边来扰动当前图结构。自适应 MCMC 的关键在于提议策略会根据当前图的难度偏差动态调整扰动幅度，从而在采样效率与图多样性之间取得平衡。实验（Table 6）显示，该方法在硬难度下成功率达 91.5%，节点类型多样性（NTD）达 130，全面优于随机拒绝采样与贪婪采样。

### 细粒度组合奖励模型

生成场景图并转化为自然语言提示后，CompGen 需要精确评估生成图像与提示的组合一致性。不同于使用单一 VQAScore 的常见做法，CompGen 构建了**程序化问答生成器**，基于场景图自动生成四类二值问题：

- **对象存在**：“图中是否有[对象]？”
- **属性绑定**：“[对象]是否是[属性]的？”
- **关系理解**：“[对象A]是否在[对象B]的[关系位置]？”
- **数量计数**：“图中是否有恰好[N]个[对象]？”

对每张生成图像，使用多模态大模型（LLaVA-v1.6-13B）计算对每个问题回答“是”的预测概率，然后取所有问题得分的平均值作为细粒度组合奖励。消融实验（Table 4）表明，该细粒度奖励相比单一 VQAScore 带来 5.2 个百分点的平均提升，证明将奖励解耦为多个组合子维度能更有效地引导模型学习。

### 课程化 GRPO 优化

CompGen 将课程学习与 Group Relative Policy Optimization（GRPO）结合，形成 C-GRPO 训练范式。其核心机制包括：

**课程加权奖励**：在训练步 $t$，对难度等级 $j$ 的问题 $r_j^{(i)}$ 按课程调度概率 $\widehat{p}(t, j)$ 加权：

$$\widehat{r}_j^{(i)}(t) = \sum_{j'=1}^{\|\mathrm{Diff}\|} \widehat{p}(t, j') \cdot r_j^{(i)}$$

图像 $i$ 的整体奖励为所有采样问题的加权平均：

$$\widehat{r}^{(i)}(t) = \frac{1}{M} \sum_{j=1}^{M} \widehat{r}_j^{(i)}(t)$$

**课程感知优势函数**：在每组 $G$ 张图像内对奖励进行归一化，得到优势函数：

$$A_i(t) = \frac{\widehat{r}^{(i)}(t) - \mathrm{Mean}\big(\{\widehat{r}^{(k)}(t)\}_{k=1}^G\big)}{\mathrm{Std}\big(\{\widehat{r}^{(k)}(t)\}_{k=1}^G\big)}$$

**C-GRPO 优化目标**：带裁剪和 KL 正则的策略梯度目标：

$$\mathcal{J}_{\mathrm{C-GRPO}}(\theta) = \mathbb{E}_T \left[ \frac{1}{G} \sum_{i=1}^G \left( \min\left( \frac{\pi_\theta}{\pi_{\theta_{\mathrm{old}}}} A_i(t), \mathrm{clip}\left( \frac{\pi_\theta}{\pi_{\theta_{\mathrm{old}}}}, 1-\epsilon, 1+\epsilon \right) A_i(t) \right) - \beta \mathrm{KL}\big(p_\theta(\cdot|T) \| p_{\mathrm{ref}}(\cdot|T)\big) \right) \right]$$

其中 $\pi_\theta$ 为当前策略，$\pi_{\theta_{\mathrm{old}}}$ 为旧策略，$\epsilon$ 控制裁剪范围，$\beta$ 调节与参考模型 $p_{\mathrm{ref}}$ 的 KL 散度正则强度。

**课程调度策略**：论文对比了三种调度方案（详见 Appendix C）：
- **随机调度**：$p_{\mathrm{random}}(t, j) = 1/M$，各难度等概率采样。
- **易到难调度**：$p_{\mathrm{E2H}}(t, j)$ 在预定义阶段 $\tau_j$ 内仅采样对应难度，逐步推进。
- **高斯调度**：以潜在位置 $x_t = (t/N_T)^\beta (M-1)$ 为中心，按高斯核计算各难度采样概率，实现平滑过渡。

实验（Figure 5）表明，易到难和高斯调度在训练步数增加时持续提升性能，而随机采样较早饱和，验证了课程递进对组合能力 scaling 的关键作用。

## 实验与关键发现

### 主实验结果

CompGen 在两个不同架构的 T2I 模型上均带来显著且一致的组合生成能力提升。在五个标准组合生成基准（GenEval、DPG、TIFA、T2I-CompBench、DSG）上，以 Stable-Diffusion-1.5 为基线的 CompGen 平均准确率达 66.62%，相比基线 54.90% 提升 **11.72 个百分点**；以自回归模型 SimpleAR-SFT 为基线的 CompGen 平均准确率达 71.27%，相比基线 63.66% 提升 **7.61 个百分点**（Table 1）。这一结果验证了合成课程强化学习框架在不同生成范式下的泛化能力。

![[assets/figures/papers/paper_list_l2344_https_arxiv_org_abs_2511_18378/figures/004_Table_1.jpg]]
*Table 1: Comparison of different T2I models on compositional generation benchmarks. Models with gray background are the baseline models that our method builds upon, while those with yellow background are our trained models. The best performance among all models are marked in red and the performance improvement of our trained models over the baseline models are marked in ↑green*

从各基准的细粒度表现来看，CompGen 在 GenEval 上将 SD-1.5 从 42.08% 提升至 53.88%（+11.80 pp），在 DSG 上将 SimpleAR 从 71.98% 提升至 86.11%（+14.13 pp），表明方法对对象存在、属性绑定、空间关系和数量计数等组合子能力均有系统性改善。在同参数量级模型中，CompGen 达到了最优性能（Figure 1），且无需依赖真实图像或修改模型架构。

![[assets/figures/papers/paper_list_l2344_https_arxiv_org_abs_2511_18378/figures/001_Figure_1.jpg]]
*Figure 1: Overall performance of our CompGen, indicating that CompGen achieves state-of-the-art performance among models of the same scale*

定性对比（Figure 4）进一步揭示了 CompGen 的优势模式：在包含多对象、复杂属性修饰和空间关系约束的提示词上，SD-1.5、SD-2.1、SDXL 和 Lumina-Next 等强基线模型频繁出现对象遗漏（蓝色标注错误）、属性绑定错误（棕色）、关系混淆（绿色）和计数偏差（紫色），而 CompGen 在这些维度上展现出更一致的忠实生成能力。

### 关键消融与因果分析

**难度度量公式的乘法设计是核心因果杠杆。** 论文提出的场景图难度度量采用乘法形式：

$$\operatorname{Diff}(\mathcal{G}) = \|\mathcal{O}\| \cdot \max\left(1, \frac{\|A\|}{\|\mathcal{O}\|}\right) \cdot \max\left(1, \frac{\|\mathcal{R}\|}{\|\mathcal{O}\|}\right)$$

消融实验（Table 3）对比了多种加性基线（如仅用对象数、对象数+属性密度、对象数+关系连通性等），乘法度量在所有基准上一致最优，平均得分 66.62%，比最强加性基线高出 **4.56 个百分点**。这表明组合难度并非各因子的简单叠加，而是对象数量与属性密度、关系连通性之间的乘法交互效应——当对象数增加时，属性绑定和关系理解的难度呈超线性增长。

![[assets/figures/papers/paper_list_l2344_https_arxiv_org_abs_2511_18378/figures/008_Table_3.jpg]]
*Table 3: Investigation on different difficulty measures using Stable-Diffusion-1.5 with 10K training data. Our proposed difficulty measure is marked with yellow background. The best performance for each benchmark is marked in red. ∥O∥ is the number of objects in the scene graph, ∥A∥ is the number of attributes and ∥R∥ is the number of relations*

**细粒度组合奖励是性能提升的关键信号源。** 将奖励信号解耦为对象存在、属性绑定、关系理解和数量计数四类 VQA 问题的平均分，相比使用单一 VQAScore 带来 **5.2 个百分点**的平均提升（Table 4）。这一结果说明，粗粒度的整体对齐分数无法有效区分不同类型的组合错误，而细粒度奖励能够为每种组合子能力提供针对性的学习信号。

**数据难度分布需均匀覆盖所有级别。** 仅使用简单样本（Skew-easy）或困难样本（Skew-difficult）训练均严重损害性能：均匀分布分别高出 25.77 pp 和 24.24 pp（Table 5）。这证实了组合生成能力的获取需要从易到难的系统性覆盖，单一难度级别的训练无法形成泛化的组合推理能力。

**课程调度策略决定 scaling 行为。** 三种调度策略的对比（Figure 5）显示，易到难（Easy-to-Hard）和高斯采样（Gaussian）调度在训练步数增加时持续提升性能，而随机采样较早达到性能饱和。这验证了结构化课程对于充分利用合成数据的必要性——随机采样下模型难以建立从简单到复杂的渐进式能力构建路径。

**自适应 MCMC 采样是高质量课程数据生成的保障。** 在场景图生成阶段，自适应 MCMC 方法在成功率和图多样性上全面领先随机拒绝采样和贪婪采样（Table 6）。在硬难度（Hard）模式下，自适应 MCMC 的成功率达 **91.5%**，节点类型多样性（NTD）达 **130**，而随机拒绝采样仅 2.9% 成功率和 49 NTD。最小初始化策略（少量随机对象节点）在成功率和多样性之间取得最佳平衡（Table 7）。

### 失败模式与局限

尽管 CompGen 取得了显著提升，分析揭示了若干值得关注的局限性：

1. **奖励模型依赖性。** 不同多模态奖励模型导致明显的性能差异（Table 2）：LLaVA-v1.6-13B 取得最优平均分，而 CLIP-FlanT5-XXL 和 InstructBLIP 等替代模型表现显著逊色。这意味着 CompGen 的训练效果与奖励信号的品质强耦合，在奖励模型能力不足的场景下可能退化。

2. **架构覆盖有限。** 当前验证仅覆盖 Stable-Diffusion-1.5 和 SimpleAR 两种架构（参数量均在 1B 以下），在更大规模模型（如 SDXL、Playground v2）上的表现尚待验证。论文中这些模型的基线性能已较高，CompGen 能否在其基础上继续带来显著增益需要额外实验确认。

3. **课程调度需手工设计。** 易到难调度依赖预定义的阶段划分，高斯调度需设定 σ 等超参数，缺乏根据模型实时性能自适应调整难度的机制。这可能在更复杂的训练设定中导致次优的难度递进节奏。

4. **合成数据生成的计算开销。** 训练阶段需要额外的 MCMC 采样与 LLM（如 DeepSeek-V3）调用以生成场景图和文本提示，计算成本较标准微调有所增加，尽管推理阶段不引入额外开销。

### 图表结论摘要

- **Figure 1 / Table 1**：CompGen 在同参数量级模型中达到最优组合生成性能，跨架构平均提升 7.61%–11.72%。
- **Table 3**：乘法难度度量在所有基准上一致优于加性基线，验证了组合难度的乘法交互本质。
- **Table 4**：细粒度组合奖励比单一 VQAScore 提升 5.2 pp，解耦奖励信号是有效的训练策略。
- **Table 5**：均匀难度分布训练至关重要，偏斜分布导致 24–26 pp 的性能损失。
- **Figure 5**：易到难和高斯调度展现持续 scaling 潜力，随机采样较早饱和。
- **Table 6 / Table 7**：自适应 MCMC 采样和最小初始化策略是高质量课程数据生成的关键设计选择。

![[assets/figures/papers/paper_list_l2344_https_arxiv_org_abs_2511_18378/figures/011_Table_6.jpg]]
*Table 6: Comparison of sampling efficiency and graph diversity using different sampling methods. The proposed method is marked with yellow background. The best performance is marked in red. SR denotes Success Rate, and NTD denotes Node Type Diversity*

![[assets/figures/papers/paper_list_l2344_https_arxiv_org_abs_2511_18378/figures/012_Table_5.jpg]]
*Table 5: Investigation on different data difficulty distributions using Stable-Diffusion-1.5 with 10K training data. The data distribution we adopted is marked with yellow background. The best performance for each benchmark is marked in red. “Skew-easy” means training on easier instances, “Skew-difficult” means harder ones, and “Uniform” means training on a balanced mix of difficulties*

## 定位与知识库关联

### 1. 问题定位：组合生成中的系统性瓶颈

当前文本到图像（T2I）生成模型在组合生成方面存在明确的系统性弱点——对象遗漏、属性绑定错误、空间/语义关系混乱以及数量计数不准确。这些缺陷并非源于模型架构的根本性限制，而是由于训练过程中缺乏专门针对组合能力的训练信号与难度递进机制。CompGen 的核心洞察在于：组合复杂性可以被分解为场景图的三个可量化因子——节点数、平均属性密度和平均关系连通性——并以此为准则构建合成课程进行强化学习训练，从而使 T2I 模型无需依赖真实图像或修改架构即可系统提升组合生成性能。

### 2. 方法谱系中的定位

**与基于注意力的组合方法的区别。** 已有工作如 **DenseDiffusion** 和 **CONFORM** 通过在推理阶段操纵交叉注意力图来改善属性绑定和对象存在性。这些方法属于推理时干预（inference-time intervention）范式，需要额外的注意力调控模块，且不改变模型参数，因此提升上限受限于基座模型本身的能力。CompGen 采取数据驱动的训练范式，通过合成课程与强化学习直接优化模型参数，从根源上增强模型的组合生成能力，且不增加推理成本。

**与基于真实数据的组合训练方法的区别。** 部分工作尝试利用真实图像-文本对或人工标注的组合性数据来微调 T2I 模型，但受限于数据规模、标注质量和难度分布的可控性。CompGen 通过自适应 MCMC 从场景图合成生成训练数据，实现了难度可控、分布均衡的课程构建，完全摆脱了对真实图像的依赖。

**与强化学习微调方法的联系与推进。** 将 RL 用于 T2I 模型的对齐训练（如基于 VQAScore 或 CLIP 分数的奖励优化）已有初步探索。CompGen 在此基础上做了三个关键推进：（1）将单一奖励信号解耦为对象存在、属性绑定、关系理解、数量计数四类细粒度组合奖励，消融实验表明这比单一 VQAScore 带来 5.2 个百分点的平均提升（Table 4）；（2）引入基于场景图难度的课程调度机制（易到难、高斯采样），使训练从简单组合逐步过渡到复杂组合，scaling 趋势显著优于随机采样（Figure 5）；（3）采用 Group Relative Policy Optimization（GRPO）作为策略优化器，结合课程加权奖励与组内优势归一化，实现稳定的组合能力渐进学习。

**与自回归 T2I 模型的适配性。** CompGen 在扩散架构（Stable-Diffusion-1.5）和自回归架构（SimpleAR-SFT）上均取得显著提升（平均分别 +11.72% 和 +7.61%，Table 1），表明该框架对生成范式具有较好的通用性。在自回归模型序列中，经过 CompGen 训练的 SimpleAR 平均得分 71.27%，显著优于同尺度的 **Emu3**（62.31%）和 **LlamaGen**（63.66%）。

### 3. 适用边界

CompGen 的有效性已在以下条件下得到验证：

- **模型架构：** 扩散模型（Stable-Diffusion-1.5，约 1B 参数）和自回归模型（SimpleAR-SFT，参数量级相当）。在更大规模模型（如 SDXL、Playground v2）上的适用性尚待验证。
- **训练数据规模：** 10K 合成样本，均匀分布于 10 个难度级别。数据规模与性能的 scaling 关系未做系统探索。
- **奖励模型：** 主要基于 LLaVA-v1.6-13B 计算细粒度 VQA 分数。Table 2 显示不同奖励模型（如 VQAScore、CLIP-FlanT5-XXL、InstructBLIP）会导致明显的性能差异，表明奖励信号的品质是框架有效性的重要前提。
- **场景图资产库：** 依赖 DeepSeek-V3 等 LLM 构建的对象、属性、关系库，虽然覆盖面较广，但可能遗漏长尾对象或罕见关系组合。

### 4. 局限与开放问题

**奖励信号的品质依赖性。** 所有评估和训练均依赖特定多模态奖励模型（LLaVA-v1.6-13B），奖励模型的偏差或盲区可能直接影响训练稳定性和性能上限。在缺乏高质量奖励模型的环境下，如何构建等效的组合能力训练信号仍是一个开放问题。

**课程调度的静态性。** 当前课程调度策略（易到难、高斯采样）需要手工设定阶段划分或超参数（如高斯 σ），缺乏对模型动态性能的自适应调节机制。一个值得探索的方向是设计能根据模型当前性能动态调整难度分布的自适应课程策略，以进一步提升数据效率与最终性能。

**难度度量的维度局限。** 当前难度度量仅考虑场景图的结构复杂度（对象数、属性密度、关系连通性），未纳入语义复杂度、视觉真实感要求、跨模态对齐难度等因素。构建更全面的组合难度模型可能进一步释放课程学习的潜力。

**规模扩展的未知性。** CompGen 仅在 1B 参数以下的模型上验证，其在更大规模扩散模型（如 SDXL、Flux）或其他生成任务（如文本到视频）上的 scaling 行为尚待研究。训练阶段额外的 MCMC 采样与 LLM 调用也带来较标准微调更高的计算开销。

**数据多样性的增强空间。** 当前合成课程仅利用场景图结构化信息，未来可引入真实世界图像统计分布或开放域知识图谱，进一步增强课程数据的多样性和真实性。

## 原文 PDF

![[paperPDFs/CVPR_2026/Synthetic_Curriculum_Reinforces_Compositional_Text_to_Image_Generation.pdf]]
