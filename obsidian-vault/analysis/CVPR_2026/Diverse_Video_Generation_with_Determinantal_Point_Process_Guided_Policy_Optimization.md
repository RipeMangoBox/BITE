---
title: Diverse Video Generation with Determinantal Point Process-Guided Policy Optimization
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Diverse_Video_Generation_with_Determinantal_Point_Process_Guided_Policy_Optimization.pdf
project_link: "https://diverse-video.github.io"
code_link: null
aliases:
- DG
- DVGDPPGPO
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/generative_models_diffusion
core_operator: DPP（行列式点过程）边际增益奖励：通过衡量新候选相对于当前参考集的体积增量，显式奖励语义互补的样本，并对冗余变化施加递减收益，从而引导策略覆盖多样模式。
primary_logic: 将多样化视频生成建模为集合级别的策略优化问题：利用DPP对集合多样性的自然度量作为奖励信号，结合GRPO的组内相对反馈，在无需修改底层视频生成模型的前提下，训练一个可即插即用的提示策略，使模型能够生成既多样又语义忠实的视频集合。
claims:
- 在Wan2.1骨干上，DPP-GRPO将语义多样性指标TCE从19.76（原始提示）提升至31.95，增幅超过60%，并全面超越所有基线方法。
- 消融实验证实，DPP多样性项和相关性项的联合使用是实现最佳平衡的关键——仅用相关性项会导致模式坍塌，仅用多样性项会削弱语义保真度（Table 4）。
- 在人类评估中，DPP-GRPO在多样性（4.07/5）和文本对齐度（4.28/5）两项均获得最高分，显著优于所有对比方法。
- 该方法在Wan2.1、CogVideoX和黑盒模型VEO上均有效，且计算开销仅为0.67%，证明其即插即用和模型无关的特性。
---

# Diverse Video Generation with Determinantal Point Process-Guided Policy Optimization

> [!tip] 核心洞察
> 将多样化视频生成建模为集合级别的策略优化问题：利用DPP对集合多样性的自然度量作为奖励信号，结合GRPO的组内相对反馈，在无需修改底层视频生成模型的前提下，训练一个可即插即用的提示策略，使模型能够生成既多样又语义忠实的视频集合。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于行列式点过程引导策略优化的多样化视频生成 |
| 英文题名 | Diverse Video Generation with Determinantal Point Process-Guided Policy Optimization |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2511.20647) · [Project](https://diverse-video.github.io) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/generative_models_diffusion |
| Method | DPP-GRPO |
| Dataset | VBench |

> [!tip] 效果简介
> - VBench (Wan2.1骨干) 上，TCE (语义多样性) 31.95 vs 19.76 (原始提示) (+12.19 (+61.7%))。
> - 计算效率 (Wan2.1管道) 上，生成每个视频的平均时间（秒） +0.58s vs 原始Wan2.1推理时间 (+0.67%)。
> - 用户研究 (120名参与者) 上，多样性评分 (1-5) 4.07 vs 次优方法（评分未列出） (最高)。

## 概述

文本到视频生成模型在给定单一提示时，往往收敛于少数几种视觉模式，难以自动覆盖镜头运动、场景布局、主体外观等电影化要素的全部可能性。这一**模式坍塌**现象限制了生成内容的丰富度与实用性。本文将该问题形式化为**集合级别的策略优化**任务，并提出 **DPP-GRPO**（Determinantal Point Process-Guided Group Relative Policy Optimization）框架。

其核心思路是：利用**行列式点过程（DPP）** 对集合多样性的自然度量能力，将新候选样本相对于已有参考集的体积增量作为多样性奖励信号——首次出现的视觉选择获得高奖励，而冗余变体则因 DPP 的边际收益递减特性被惩罚。该奖励与语义相关性奖励联合，通过 **GRPO** 的组内相对反馈机制，训练一个轻量级提示策略网络。该策略以自回归方式迭代生成多样化提示，进而驱动底层视频生成模型产生丰富且语义忠实的视频集合。

该方法的关键优势在于**即插即用**：无需修改或微调任何底层视频扩散模型，仅作为外部提示优化器运行。在 Wan2.1 骨干上，DPP-GRPO 将语义多样性指标 TCE 从原始提示的 19.76 提升至 31.95，增幅超过 60%，同时计算开销仅增加 0.67%。人类评估中，该方法在多样性（4.07/5）和文本对齐度（4.28/5）两项均获得最高评分，并在 CogVideoX 及黑盒模型 VEO 上验证了其模型无关的泛化能力。

消融实验进一步揭示了方法成功的关键机制：DPP 多样性项与相关性项的联合使用是实现最佳平衡的必要条件——仅用相关性项会导致模式坍塌，仅用多样性项则会削弱语义保真度；参考集大小在 5–8 个示例时达到最优，符合 DPP 对数行列式的边际收益递减特性。

## 背景与动机

### 文本到视频生成的多样性瓶颈

文本到视频（Text-to-Video, T2V）扩散模型近年来取得了显著进展，以 **CogVideoX**（Yang et al., 2024）、**Wan2.1**（Team Wan et al., 2025）等为代表的模型已能生成高质量的视频片段。然而，这些模型存在一个被长期忽视的核心瓶颈：**当给定单个文本提示时，多次独立采样生成的视频往往收敛于少数几种视觉模式**，难以全面覆盖该提示所隐含的电影化要素空间。

具体而言，对于一个描述特定场景的提示，现有模型可能在镜头运动（如推拉摇移）、场景布局、主体外观、环境氛围等维度上表现出高度的一致性——例如，多次生成都倾向于使用固定的中景镜头和相似的构图方式。这种模式坍塌（mode collapse）现象导致用户无法通过简单的多次采样获得一组真正多样化的视频候选，限制了T2V模型在创意设计、影视预演等场景中的实用价值。

### 现有方法的局限性

当前提升生成多样性的尝试主要集中在以下几个方向，但各自存在明显不足：

1. **直接使用原始提示并随机采样种子**：这是最朴素的基线方法，但由于扩散模型的固有倾向性，不同种子下的生成结果在语义空间中往往高度聚集，多样性极为有限。

2. **基于大语言模型的提示扩展**（如 **GPT-5**）：利用LLM对原始提示进行改写或扩展，试图通过文本层面的变化引导视觉多样性。然而，LLM生成的变体往往停留在词汇替换层面，难以系统性地探索镜头运动、场景布局等电影化要素的组合空间，且缺乏对生成结果的反馈闭环。

3. **基于强化学习的提示优化**（如 **Promptist**、**Prompt-A-Video**）：这些方法通过奖励信号优化提示生成策略，但其奖励设计通常以单样本质量或对齐度为目标，**缺乏对集合级别多样性的显式建模**。它们优化的是“每个样本有多好”，而非“一组样本作为一个整体有多互补”。

4. **启发式种子搜索**：通过遍历不同随机种子来寻找多样化结果，计算开销大且缺乏理论保证，本质上是一种穷举策略。

上述方法的共同缺陷在于：它们将多样化视频生成视为**独立的单样本优化问题**，而忽视了**集合级别的多样性与互补性**这一核心需求。

### 核心动机与问题建模

本文的核心洞察是：**多样化视频生成本质上是一个集合级别的策略优化问题**。用户真正需要的不是一个“最好的”视频，而是一组能够从不同电影化维度（镜头运动、场景布局、主体外观等）覆盖提示语义空间的视频集合。这一目标要求我们：

- **显式奖励互补性**：当一个新生成的视频引入了与已有集合不同的视觉模式时，应给予正向奖励；
- **惩罚冗余**：当新视频与已有集合中的样本高度相似时，其边际贡献应递减，即引入**边际收益递减（diminishing returns）**机制。

行列式点过程（Determinantal Point Process, DPP）天然具备上述特性：其核心概率度量——对数行列式——恰好衡量了集合在语义嵌入空间中“体积”，而体积越大意味着元素之间的互补性越强、覆盖的语义维度越丰富。同时，DPP的行列式结构使得**新增元素的边际增益随集合增长而递减**，完美契合多样性优化的需求。

基于这一洞察，本文提出 **DPP-GRPO**，将DPP的集合多样性度量与组相对策略优化（Group Relative Policy Optimization, GRPO）相结合，在无需修改底层视频生成模型的前提下，训练一个即插即用的提示策略网络，使其能够为任意文本提示生成一组既多样化又语义忠实的视频。

## 核心创新

DPP-GRPO 的核心创新在于将多样化视频生成重新定义为**集合级别的策略优化问题**，并通过三个关键机制实现突破：

### 1. DPP 边际增益奖励：显式建模多样性的递减收益

现有文本到视频扩散模型在给定单个提示时，多次采样往往收敛于少数几种视觉模式，缺乏对镜头运动、场景布局等电影化要素的全面覆盖。DPP-GRPO 的核心突破在于引入**行列式点过程（DPP）**作为多样性的自然度量。

具体而言，方法利用 Sentence-BERT 嵌入构建核矩阵 $L$，通过对数行列式度量提示集合的体积：

$$\mathrm{Div}(p_{1:k}) = \log \det(L_{\phi}(p_{1:k}) + I)$$

在此基础上，定义**边际增益**作为新候选的多样性奖励：

$$\Delta(p_i \mid \mathcal{R}_q) = \log \operatorname*{det}(L_{\phi}(\mathcal{R}_q \cup \{p_i\})) - \log \operatorname*{det}(L_{\phi}(\mathcal{R}_q))$$

这一设计的精髓在于 DPP 的递减收益特性：当候选与参考集中已有样本语义相似时，其对行列式的贡献微乎其微，从而被自动抑制；反之，语义互补的候选则获得高额奖励。这从根本上解决了朴素随机采样中“首现模式获奖励、冗余变体无惩罚”的问题。

### 2. GRPO 组内相对反馈：无需价值网络的策略优化

DPP-GRPO 采用 **Group Relative Policy Optimization（GRPO）** 作为策略优化框架，其核心优势在于：

- **组内归一化优势**：对每组 $G$ 个候选，将每个样本的奖励减去组内均值后除以标准差，使得高质量样本获得正优势：

  $$A_i = \frac{r_i - \operatorname*{mean}(r_{1:G})}{\operatorname*{std}(r_{1:G})}$$

- **无需独立价值网络**：通过截断重要性采样和 KL 散度惩罚直接优化策略，大幅降低训练复杂度。

这一设计使策略模型能够从组内相对比较中学习，而非依赖绝对奖励阈值，从而更鲁棒地适应不同提示的多样性需求。

### 3. 复合奖励机制：多样性与语义保真度的动态平衡

DPP-GRPO 的最终奖励为多样性边际增益与相关性奖励的加权和：

$$R(p \mid q, g) = \lambda_{\mathrm{div}} \Delta(p_i \mid \mathcal{R}_q) + \lambda_{\mathrm{rel}} R_{\mathrm{rel}}$$

其中相关性奖励确保生成提示与用户查询及已有变体均保持语义关联：

$$R_{\mathrm{rel}} = \frac{1}{|\mathcal{R}_q|} \sum_{g \in \mathcal{R}_q} \cos(\phi(p_i), \phi(q)) \cdot \cos(\phi(p_i), \phi(g))$$

消融实验（Table 4）证实，仅用相关性项会导致模式坍塌，仅用多样性项会削弱语义保真度——二者的联合使用是实现最佳平衡的关键。权重消融（Table 6）进一步表明，$(\lambda_{\mathrm{div}}, \lambda_{\mathrm{rel}}) = (0.5, 0.5)$ 为最优折中点。

### 4. 即插即用与模型无关性

DPP-GRPO 的另一关键创新在于其**完全解耦于底层视频生成模型**。方法仅训练一个基于 Qwen2-7b-Instruct 的轻量级提示策略网络，在推理时自回归地生成多样化提示集合，无需修改视频扩散模型的权重或采样过程。实验表明，该方法在 **Wan2.1**、**CogVideoX**（Yang et al., 2024）和黑盒模型 **VEO3** 上均有效，且计算开销仅为 0.67%（Table 2），真正实现了即插即用。

### 与基线方法的核心差异

| 创新维度 | 基线方法 | DPP-GRPO |
|---------|---------|----------|
| **多样性奖励信号** | 无显式多样性目标，样本相互独立 | DPP 对数行列式边际增益，显式鼓励互补、惩罚冗余 |
| **策略优化框架** | 直接使用原始提示或启发式种子搜索 | GRPO 组内相对反馈，联合优化多样性与相关性 |
| **提示生成机制** | 一次性生成固定提示 | 自回归迭代生成，每步基于参考集计算边际增益 |

这种“集合级多样性度量 + 组内相对优化 + 提示策略解耦”的三位一体设计，使 DPP-GRPO 在不牺牲语义保真度的前提下，将语义多样性指标 TCE 从 19.76（原始提示）提升至 31.95，增幅超过 60%（Table 1）。

## 整体框架

DPP-GRPO 将多样化视频生成建模为集合级别的策略优化问题，其核心 pipeline 由三个关键模块构成闭环：**策略模型**负责生成候选提示，**DPP 多样性计算与边际增益评估**量化集合的语义覆盖度，**GRPO 训练循环**则利用组内相对反馈更新策略。整个框架无需修改底层视频生成模型，以即插即用的方式工作。

### Pipeline 总览

如 Figure 3 所示，系统接收一个用户查询 $q$ 后，按以下流程运行：

![[assets/figures/papers/paper_list_l2464_https_arxiv_org_abs_2511_20647/figures/003_Figure_3.jpg]]
*Figure 3: Framework Overview. The model generates a group of G candidates*

1. **候选生成**：策略模型 $\pi_\theta$（基于 Qwen2-7b-Instruct）接收 $q$ 和可选的参考集 $\mathcal{R}_q$，自回归地生成一组 $G$ 个候选提示 $\{p_1, \dots, p_G\}$。
2. **复合奖励计算**：每个候选 $p_i$ 被送入两个并行的奖励模块——
   - **DPP 边际增益** $\Delta(p_i \mid \mathcal{R}_q)$：衡量将 $p_i$ 加入当前参考集后，集合体积的对数行列式增量，显式奖励互补性并惩罚冗余。
   - **相关性奖励** $R_{\mathrm{rel}}$：计算 $p_i$ 与用户查询 $q$ 及参考集中已有样本的平均余弦相似度乘积，保证语义忠实。
   - 最终奖励为二者的加权和：$R(p \mid q, g) = \lambda_{\mathrm{div}} \Delta(p_i \mid \mathcal{R}_q) + \lambda_{\mathrm{rel}} R_{\mathrm{rel}}$（Equation 7）。
3. **组内归一化与策略更新**：对 $G$ 个候选的奖励进行组内归一化，得到优势 $A_i = \frac{r_i - \mathrm{mean}(r_{1:G})}{\mathrm{std}(r_{1:G})}$（Equation 2），然后通过截断重要性采样和 KL 散度惩罚更新策略 $\pi_\theta$（Equation 1）。
4. **推理时自回归扩展**：在推理阶段，策略每次生成一个新提示，将其加入参考集 $\mathcal{R}_q$，然后基于更新后的参考集计算下一个候选的边际增益，如此迭代直至生成所需数量 $K$ 的提示集合。这些提示分别送入底层视频生成模型，产生多样化的视频集合。

### 模块关系与数据流

| 模块 | 输入 | 输出 | 核心机制 |
|------|------|------|----------|
| 策略模型 (Policy Model) | 用户查询 $q$，参考集 $\mathcal{R}_q$ | $G$ 个候选提示 $\{p_i\}$ | 基于 Qwen2-7b-Instruct 的自回归生成 |
| DPP 多样性计算 | 提示嵌入 $\phi(p)$（Sentence-BERT） | 核矩阵 $L_\phi$ 及对数行列式 $\log\det(L_\phi + I)$ | Equation 3：$\mathrm{Div}(p_{1:k}) = \log \det(L_{\phi}(p_{1:k}) + I)$ |
| 边际增益评估 | 新候选 $p_i$，当前参考集 $\mathcal{R}_q$ | 多样性增量 $\Delta(p_i \mid \mathcal{R}_q)$ | Equation 4：体积增量 = $\log\det(L_\phi(\mathcal{R}_q \cup \{p_i\})) - \log\det(L_\phi(\mathcal{R}_q))$ |
| 相关性奖励模块 | $p_i$, $q$, $\mathcal{R}_q$ | $R_{\mathrm{rel}}$ | Equation 6：$\frac{1}{|\mathcal{R}_q|}\sum_{g \in \mathcal{R}_q} \cos(\phi(p_i), \phi(q)) \cdot \cos(\phi(p_i), \phi(g))$ |
| GRPO 训练循环 | 组内奖励 $\{r_i\}$，旧策略 $\pi_{\theta_{\mathrm{old}}}$ | 更新后的策略 $\pi_\theta$ | Equation 1-2：组归一化优势 + 截断重要性采样 + KL 处罚 |

### 训练流程

训练采用两阶段后训练策略（part_004 证据）：
- **第一阶段（监督微调）**：对策略模型进行 50 轮迭代的监督微调，学习率为 $2\times10^{-5}$，为后续强化学习提供良好的初始化。
- **第二阶段（GRPO 强化学习）**：进行约 1200 轮迭代的 GRPO 训练，学习率降至 $2\times10^{-7}$，利用复合奖励和组内相对反馈优化策略。

### 关键设计特性

**即插即用与模型无关**：DPP-GRPO 仅作用于提示层面，不侵入视频生成模型的内部推理过程。实验证实该方法在 **Wan2.1**（Team Wan et al., 2025）、**CogVideoX**（Yang et al., 2024）以及黑盒模型 **VEO** 上均有效（Figure 5），且计算开销仅为 $+0.67\%$（Table 2）。

**递减收益机制**：DPP 对数行列式的数学性质天然实现了“递减收益”——当参考集中已存在与候选相似的样本时，新候选带来的体积增量极小，从而自动抑制冗余变化。消融实验（Table 5）证实，参考集大小在 5-8 个示例时多样性达到峰值，超过 10 个后性能衰减，与 DPP 边际收益递减的理论预期一致。

**多样性与保真度的可调节平衡**：通过权重 $(\lambda_{\mathrm{div}}, \lambda_{\mathrm{rel}})$ 控制探索与利用的权衡。消融实验（Table 6）表明，$(0.5, 0.5)$ 为最佳折中点——单独提高多样性权重可提升 TCE/TIE 但降低 CLIP 对齐度，反之亦然。

### 补充图表

![[assets/figures/papers/paper_list_l2464_https_arxiv_org_abs_2511_20647/figures/017_Table_7.jpg]]
*Table 7: System Prompt*

## 核心模块与公式推导

DPP-GRPO 将多样化视频生成建模为集合级别的策略优化问题，其核心由三个模块构成：**DPP 多样性度量**、**复合奖励函数**和 **GRPO 策略优化**。这三个模块协同工作，在无需修改底层视频生成模型的前提下，训练一个可即插即用的提示策略网络。

### DPP 多样性度量

方法的核心创新在于利用行列式点过程（DPP）来量化提示集合的多样性。给定一组提示 $p_{1:k}$，首先通过 Sentence-BERT 嵌入 $\phi(\cdot)$ 构建核矩阵 $L_{\phi}(p_{1:k})$，然后以对数行列式度量集合覆盖的语义体积：

$$\mathrm{Div}(p_{1:k}) = \log \det(L_{\phi}(p_{1:k}) + I)$$

其中 $I$ 为单位矩阵，用于保证数值稳定性。该度量的直觉来自 DPP 的 L-ensemble 定义——子集 $S$ 的概率正比于 $\det(L_S)$，行列式越大表示子集元素间的语义互补性越强。对数行列式天然具备**边际收益递减**特性：当集合中已存在相似样本时，新增相似候选带来的体积增量极小，从而自动抑制冗余变化。

基于此，定义新候选 $p_i$ 相对于已有参考集 $\mathcal{R}_q$ 的**边际多样性增益**：

$$\Delta(p_i \mid \mathcal{R}_q) = \log \det(L_{\phi}(\mathcal{R}_q \cup \{p_i\})) - \log \det(L_{\phi}(\mathcal{R}_q))$$

该增益直接量化了 $p_i$ 为参考集带来的额外多样性：若 $p_i$ 与参考集中样本高度相似，增益趋近于零；若 $p_i$ 引入全新语义维度，增益显著为正。

### 复合奖励函数

为保证生成视频既多样又语义忠实，奖励函数联合优化多样性与相关性两个维度。**相关性奖励** $R_{\mathrm{rel}}$ 衡量生成提示 $p_i$ 与用户查询 $q$ 及参考集中已有样本的双向余弦相似度：

$$R_{\mathrm{rel}} = \frac{1}{|\mathcal{R}_q|} \sum_{g \in \mathcal{R}_q} \cos(\phi(p_i), \phi(q)) \cdot \cos(\phi(p_i), \phi(g))$$

该设计鼓励生成提示既忠于原始意图，又与已知变体保持语义关联，避免因过度追求多样性而偏离主题。

最终**复合奖励**为两项的加权和：

$$R(p \mid q, g) = \lambda_{\mathrm{div}} \Delta(p_i \mid \mathcal{R}_q) + \lambda_{\mathrm{rel}} R_{\mathrm{rel}}$$

其中 $\lambda_{\mathrm{div}}$ 和 $\lambda_{\mathrm{rel}}$ 为超参数，控制多样性与语义保真度的权衡。消融实验证实（Table 6），$(\lambda_{\mathrm{div}}, \lambda_{\mathrm{rel}}) = (0.5, 0.5)$ 为最佳折中点——仅用相关性项会导致模式坍塌，仅用多样性项会削弱语义对齐。

### GRPO 策略优化

策略模型基于 **Qwen2-7b-Instruct**，接收用户查询和可选参考集，自回归生成多样性提示。训练采用两阶段范式：先进行 50 轮监督微调（SFT，学习率 $2 \times 10^{-5}$）初始化策略，再通过 GRPO 进行约 1200 轮强化学习优化（学习率 $2 \times 10^{-7}$）。

GRPO 的核心优势在于无需单独的价值网络，而是通过**组内相对反馈**直接优化策略。对每组 $G$ 个候选，首先计算每个样本的奖励 $r_i$，然后进行组内归一化得到优势 $A_i$：

$$A_i = \frac{r_i - \mathrm{mean}(r_{1:G})}{\mathrm{std}(r_{1:G})}$$

奖励高于组内均值的样本获得正优势，反之获得负优势。策略更新遵循截断重要性采样与 KL 散度惩罚的目标函数：

$$\mathcal{I}_{\mathrm{GRPO}}(\theta) = \mathbb{E}_{a, \{o_i\}} \Bigg[ \frac{1}{G} \sum_{i=1}^{G} \min\left( \frac{\pi_{\theta}(o_i | q)}{\pi_{\theta_{\mathrm{old}}}(o_i | q)} A_i, \mathrm{clip}\left( \frac{\pi_{\theta}(o_i | q)}{\pi_{\theta_{\mathrm{old}}}(o_i | q)}, 1-\epsilon, 1+\epsilon \right) A_i \right) - \beta \mathbb{D}_{\mathrm{KL}}(\pi_{\theta} || \pi_{\mathrm{ref}}) \Bigg]$$

其中 $\pi_{\theta}$ 为当前策略，$\pi_{\theta_{\mathrm{old}}}$ 为旧策略，$\pi_{\mathrm{ref}}$ 为参考策略（SFT 初始化后的模型），$\epsilon$ 为截断阈值，$\beta$ 控制 KL 惩罚强度。截断机制防止策略更新幅度过大，KL 散度项约束策略不偏离参考模型过远，保证训练稳定性。

### 推理流程

推理时，策略模型以**自回归迭代**方式生成提示集合：首先生成第一个提示并加入参考集 $\mathcal{R}_q$，随后每一步基于当前 $\mathcal{R}_q$ 计算边际增益，指导下一次采样。这一设计使得后续生成的提示能够主动避开已覆盖的语义区域，逐步扩展集合的多样性边界。生成完成后，所有提示分别送入冻结的文本到视频扩散模型（如 **Wan2.1** 或 **CogVideoX**）进行视频生成，整个流程对底层模型完全透明。

## 实验与分析

### 核心实验结果

DPP-GRPO 在语义多样性、感知多样性与文本对齐度三个维度上均展现出显著且一致的提升。在 Wan2.1 骨干上，其语义多样性指标 TCE 从原始提示的 19.76 跃升至 31.95，增幅超过 60%（Table 1）。该优势在 CogVideoX 骨干上同样复现，证明方法具备模型无关的即插即用特性。在计算效率方面，DPP-GRPO 引入的额外开销仅为每视频 0.58 秒，占原始 Wan2.1 推理时间的 0.67%（Table 2），几乎可忽略不计。

![[assets/figures/papers/paper_list_l2464_https_arxiv_org_abs_2511_20647/figures/005_Table_1.jpg]]
*Table 1: Quantitative comparison of our framework with baseline T2V models under two model families (Wan2.1 and CogVideoX)*

![[assets/figures/papers/paper_list_l2464_https_arxiv_org_abs_2511_20647/figures/007_Table_2.jpg]]
*Table 2: Computational efficiency comparison. Time per video in seconds. Our method achieves minimal overhead (+0.67%)*

人类评估进一步验证了客观指标的可靠性：在 120 名参与者的双盲研究中，DPP-GRPO 在多样性（4.07/5）和文本对齐度（4.28/5）两项均获得最高评分，显著超越所有对比方法（Table 3）。值得注意的是，所有定量结果均以未挑选的原始生成顺序呈现，排除了后处理或人工挑选带来的偏差。

![[assets/figures/papers/paper_list_l2464_https_arxiv_org_abs_2511_20647/figures/009_Table_3.jpg]]
*Table 3: Our method achieves the highest ratings for both diversity and alignment in human evaluation*

### 消融研究

**奖励项消融**（Table 4）揭示了 DPP 多样性项与相关性项的协同必要性。仅使用相关性项（λ_rel=1, λ_div=0）会导致严重的模式坍塌，生成样本高度雷同；仅使用多样性项（λ_div=1, λ_rel=0）虽能提升 TCE/TIE，但 CLIP 对齐度明显下降。完整模型（两项联合）在多样性与保真度之间达到了最佳平衡，证实了复合奖励设计的不可分割性。

**参考集大小消融**（Table 5）表明，5–8 个示例的参考集在 TCE 和 TIE 上达到最优多样性水平。当参考集增至 10 个示例时性能开始衰减，这与 DPP 对数行列式的边际收益递减特性一致——过多的参考样本使新候选的边际增益趋近于零，策略优化的信号强度减弱。

**奖励权重消融**（Table 6）显示，将多样性权重 λ_div 提高至 0.9 可提升 TCE/TIE 但降低 CLIP 对齐度，将相关性权重 λ_rel 提高至 0.9 则产生相反效果。(0.5, 0.5) 被确认为最佳折中点，在语义多样性、感知多样性和文本保真度之间取得全局最优。

**CFG 值消融**（Figure 6）表明，在不同无分类器引导强度下，DPP-GRPO 始终比 Wan 基线取得更高的 TCE/TIE，同时在 CFG=6 时获得最高的 CLIP 对齐度。这证明方法的多样性增益对采样超参数具有鲁棒性。

**集合大小 K 消融**（Figure 7）进一步验证了方法的可扩展性：当生成集合从 2 增至 10 时，DPP-GRPO 的语义多样性（TCE）和感知多样性（TIE）持续优于基线，且平均 CLIP 对齐度始终更高。这表明 DPP 边际增益机制能够有效引导策略在更大集合中持续探索互补模式，而非重复已有变体。

### 失败模式分析

方法的效果受限于底层视频生成模型的基础能力。对于某些复杂场景（如高动态运动或精细时空细节），基础模型可能无法生成合理的运动或纹理，此时即使 DPP-GRPO 生成了多样化的提示，最终视频的多样性和质量提升也无法体现（Figure 8）。这表明该方法作为一种外部提示策略，不能弥补生成模型本身的根本性缺陷。此外，推理时的自回归生成方式在需要大量样本（K 很大）时，计算开销会线性增长，可能限制其在超大规模集合生成场景中的适用性。

![[assets/figures/papers/paper_list_l2464_https_arxiv_org_abs_2511_20647/figures/012_Figure_8.jpg]]
*Figure 8: An example failure case of our method where the temporal video quality depends on the base model’s ability*

### 补充图表

![[assets/figures/papers/paper_list_l2464_https_arxiv_org_abs_2511_20647/figures/013_Table_5.jpg]]
*Table 5: Ablation on reference set size*

![[assets/figures/papers/paper_list_l2464_https_arxiv_org_abs_2511_20647/figures/014_Table_6.jpg]]
*Table 6: Ablation on reward weights*

![[assets/figures/papers/paper_list_l2464_https_arxiv_org_abs_2511_20647/figures/008_Figure_6.jpg]]
*Figure 6: CFG ablation. Diversity (TCE/TIE) and fidelity (CLIP) across different CFG values for Wan and our DPP– GRPO model*

![[assets/figures/papers/paper_list_l2464_https_arxiv_org_abs_2511_20647/figures/011_Figure_7.jpg]]
*Figure 7: Impact of generation set size on diversity and alignment. The plots compare our DPP-GRPO method against the Wan baseline on (Left) Average CLIP alignment, (Middle) semantic diversity (TCE), and (Right) perceptual diversity (TIE). DPP-GRPO consistently outperforms the baseline in both alignment and diversity as the set grows*

![[assets/figures/papers/paper_list_l2464_https_arxiv_org_abs_2511_20647/figures/006_Figure_5.jpg]]
*Figure 5: Visual comparison of T2V generations from various base models, with and without our method. For each baseline (CogVideoX, Wan, VEO), we show two generated videos and their representative frames. Our method enhances the diversity and quality of the generated videos across integrated models*

![[assets/figures/papers/paper_list_l2464_https_arxiv_org_abs_2511_20647/figures/004_Figure_4.jpg]]
*Figure 4: Qualitative Comparison. DPP-GRPO diversifies several cinematic factors such as subject, scene, motion, and cameraview diversity while preserving the prompt alignment and achieves more diverse and semantically faithful videos compared to baselines. (a) For clarity, we provide the first frames of each video (b) Detailed frame-by-frame comparisons of the same videos are given (please kindly zoom-in for details). Please visit our SM for more comparisons and high-quality videos*

## 方法谱系与知识库定位

### 问题定位：从独立采样到集合级多样性优化

现有文本到视频（T2V）扩散模型在给定单个提示时，生成的多个样本往往收敛于少数几种视觉模式——例如重复出现相似的镜头运动、场景布局或主体外观——缺乏对电影化要素的全面覆盖。这一瓶颈的根源在于：传统生成流程将每个样本视为独立事件，没有显式的集合级多样性目标。DPP-GRPO 将问题重新建模为**集合级别的策略优化**：不修改底层视频生成模型本身，而是训练一个可即插即用的提示策略网络，使其能够为同一用户查询生成一组既多样又语义忠实的提示，从而引导基础模型产出覆盖多种视觉模式的视频集合。

### 方法谱系：与相关工作的关系

#### 提示优化方法

在提示优化方向上，**Promptist**（基于强化学习的提示优化）和 **Prompt-A-Video**（视频提示优化）均试图通过改写提示来改善生成质量，但它们的目标通常是单样本质量提升或风格控制，而非集合级多样性。**GPT-5** 等利用大语言模型直接扩展提示的方法，虽能引入一定变化，但缺乏对冗余的显式惩罚机制，容易在多次采样中重复相似语义方向。DPP-GRPO 与这些方法的本质区别在于引入了**行列式点过程（DPP）的边际增益奖励**：每生成一个新候选提示，系统计算其加入当前参考集后对数行列式的增量，仅当新候选在语义空间中拓展了集合的“体积”时才给予正向奖励，而对冗余变化施加递减收益。这一机制使得策略学会主动探索互补的语义方向，而非简单地随机扰动。

#### 强化学习与策略优化框架

在策略优化层面，DPP-GRPO 采用 **GRPO（Group Relative Policy Optimization）** 作为训练框架。与需要单独价值网络的 PPO 不同，GRPO 通过对每组 G 个候选进行组内奖励归一化来计算优势函数，公式为：

$$A_i = \frac{r_i - \operatorname{mean}(r_{1:G})}{\operatorname{std}(r_{1:G})}$$

这一设计使得奖励高的样本在组内获得正优势，奖励低的样本获得负优势，从而驱动策略向高奖励方向更新。GRPO 的目标函数结合了截断重要性采样和 KL 散度惩罚：

$$\mathcal{I}_{\mathrm{GRPO}}(\theta) = \mathbb{E}_{a,\{o_i\}} \Bigg[ \frac{1}{G} \sum_{i=1}^{G} \min\left( \frac{\pi_{\theta}(o_i|q)}{\pi_{\theta_{\mathrm{old}}}(o_i|q)} A_i, \mathrm{clip}\left( \frac{\pi_{\theta}(o_i|q)}{\pi_{\theta_{\mathrm{old}}}(o_i|q)}, 1-\epsilon, 1+\epsilon \right) A_i \right) - \beta \mathbb{D}_{\mathrm{KL}}(\pi_{\theta} || \pi_{\mathrm{ref}}) \Bigg]$$

#### 多样性度量方法

在多样性度量上，DPP 提供了自然的集合多样性形式化工具。在 L-ensemble DPP 下，子集 S 的概率正比于其核矩阵的主子式：

$$\mathrm{Pr}(\mathbf{Y}=S) \propto \operatorname{det}(L_S)$$

行列式越大，表示子集元素在特征空间中越“分散”，即多样性越高。DPP-GRPO 使用 Sentence-BERT 嵌入构建核矩阵 L，通过对数行列式度量提示集合的体积：

$$\mathrm{Div}(p_{1:k}) = \log \det(L_{\phi}(p_{1:k}) + I)$$

新候选的多样性贡献通过边际增益评估：

$$\Delta(p_i \mid \mathcal{R}_q) = \log \operatorname{det}(L_{\phi}(\mathcal{R}_q \cup \{p_i\})) - \log \operatorname{det}(L_{\phi}(\mathcal{R}_q))$$

#### 与基础视频生成模型的关系

DPP-GRPO 在 **Wan2.1**（Team Wan et al., 2025）、**CogVideoX**（Yang et al., 2024）和黑盒模型 **VEO3** 上均验证有效。其角色是作为这些基础模型上游的“提示策略插件”——策略模型（基于 Qwen2-7b-Instruct）接收用户查询和可选的参考集，自回归地生成多样化提示，然后交由底层 T2V 模型进行视频生成。由于不涉及对视频扩散模型的微调或内部采样过程的修改，该方法的计算开销仅为 0.67%（Table 2），且表现出模型无关的即插即用特性（Figure 5）。

### 适用边界与局限

1. **受限于底层模型能力**：DPP-GRPO 通过提示多样性间接引导视频多样性，无法弥补基础模型本身的生成缺陷。当基础模型对某些复杂场景无法生成合理的运动或细节时，多样性提升无法体现（参见 Figure 8 的失败案例）。

2. **间接控制粒度**：目前仅能通过生成多样化的提示来影响视频的宏观视觉模式（如镜头运动、场景布局、主体外观），无法直接控制视频内部的运动节奏、时序一致性或其他细粒度属性。

3. **推理时的线性扩展**：自回归生成方式在需要大量样本（K 很大）时，每步都需计算新候选相对于已有参考集的 DPP 边际增益，计算开销随集合大小线性增长。

4. **数据集覆盖范围**：训练和评估所使用的数据集聚焦于常见提示类别，可能无法完全覆盖所有视频生成场景。

### 开放问题

1. **深层多样性整合**：如何将多样性优化直接融入视频扩散模型的内部采样过程（例如在去噪步骤中引入 DPP 引导），而非仅依赖外部提示策略，从而实现更深层次、更细粒度的多样性控制？

2. **时序一致性保障**：在更复杂的摄像机动和场景变换下，如何确保生成的视频在追求多样性的同时不损害时序一致性？

3. **任务扩展**：该方法能否扩展至更长的视频生成或交互式视频生成任务，其中用户可能逐步指定偏好并期望系统自适应调整多样性策略？

4. **自适应权重调节**：当前需要手动设置 λ_div 和 λ_rel 来平衡多样性与保真度（Table 6 显示 (0.5, 0.5) 为最佳折中点）。能否设计内容自适应的权重调节机制，减少用户调参负担？

5. **更高效的多样性度量**：对数行列式计算在大规模生成时算力需求较高。是否存在更高效的集合多样性替代度量（如基于随机投影或近似核方法），以进一步降低计算开销？

## 原文 PDF

![[paperPDFs/CVPR_2026/Diverse_Video_Generation_with_Determinantal_Point_Process_Guided_Policy_Optimization.pdf]]