---
title: "PosterOmni: Generalized Artistic Poster Creation via Task Distillation and Unified Reward Feedback"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/PosterOmni_Generalized_Artistic_Poster_Creation_via_Task_Distillation_and_Unified_Reward_Feedback.pdf
project_link: "https://ephemeral182.github.io/PosterOmni/"
code_link: "https://github.com/PaddlePaddle/PaddleDetection"
aliases:
- PosterOmni
tags:
- CVPR_2026
- topic/other_unclear
- topic/other_unclear/general
core_operator: 通过对局部编辑与全局生成任务进行分解，采用专家知识蒸馏（Task Distillation）和统一奖励反馈（Unified PosterOmni Reward Feedback）驱动的强化学习，将两类能力整合到一个统一模型中。
primary_logic: 将海报生成任务显式建模为局部编辑与全局创作两个互补子空间，利用教师-学生蒸馏避免任务干扰，并通过统一奖励模型同时注入美学偏好与任务精度信号，实现精细化编辑与全局美学对齐的协同优化。
claims:
- PosterOmni significantly enhances reference adherence, global composition quality, and aesthetic harmony, outperforming all open-source baselines and even surpassing several propr...
- PosterOmni outperforms Qwen-Image-Edit baseline on local editing tasks with gains from +0.48 to +0.98, and on layout-driven and style-driven tasks shows substantial advantages (+0...
- Task distillation (PosterOmni-SFT) achieves 4.43/3.89 (L/G) on expert integration, outperforming joint training (4.18/3.52) and linear LoRA merge (4.27/3.71).
- Full R_omni reward model achieves 4.76/4.20 (L/G), while removing negative pairs drops to 4.64/4.03 and removing image-to-poster prompt drops to 4.67/4.09, demonstrating the effec...
---

# PosterOmni: Generalized Artistic Poster Creation via Task Distillation and Unified Reward Feedback

> [!tip] 核心洞察
> 将海报生成任务显式建模为局部编辑与全局创作两个互补子空间，利用教师-学生蒸馏避免任务干扰，并通过统一奖励模型同时注入美学偏好与任务精度信号，实现精细化编辑与全局美学对齐的协同优化。

| 字段 | 内容 |
|------|------|
| 中文题名 | PosterOmni：通过任务蒸馏和统一奖励反馈的广义艺术海报创作 |
| 英文题名 | PosterOmni: Generalized Artistic Poster Creation via Task Distillation and Unified Reward Feedback |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2602.12127) · [Project](https://ephemeral182.github.io/PosterOmni/) · [Code](https://github.com/PaddlePaddle/PaddleDetection) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | PosterOmni |
| Dataset | PosterOmni-Bench-en |

> [!tip] 效果简介
> - PosterOmni-Bench-en 上，Overall Score 4.37 vs Qwen-Image-Edit: 3.51 (+0.86)；Layout-driven Score 4.20 vs Qwen-Image-Edit: 3.44 (+0.76)；Style-driven Score 4.31 vs Qwen-Image-Edit: 2.91 (+1.40)。

## 概要

**PosterOmni** 面向图像到海报（image-to-poster）的广义创作任务，将局部编辑（如实体保留、区域填充、空间一致性）与全局创作（如布局、风格、美学和谐）统一到单一框架中。现有开源图像编辑模型难以同时兼顾这两类能力：局部编辑精度不足会导致布局错位与文本失真，而全局创作理解缺失则使海报缺乏整体美学质量。PosterOmni 的核心思路是将海报生成显式建模为局部与全局两个互补子空间，通过 **任务蒸馏（Task Distillation）** 将专家知识整合到统一模型中，并引入 **统一奖励反馈（Unified PosterOmni Reward Feedback）** 驱动的强化学习，同时注入美学偏好与任务精度信号，实现精细化编辑与全局美学对齐的协同优化。

在方法层面，PosterOmni 构建了一条自动化数据生成管线，覆盖六大任务类型（扩展、填充、缩放、身份驱动、布局驱动、风格驱动），形成 PosterOmni-200K 训练集与 PosterOmni-Bench 评测基准。训练流程分为四阶段：任务特定 SFT 分别训练局部与全局专家、任务蒸馏将专家知识融合为单一学生模型、训练统一奖励模型 $R_{\text{omni}}$、以及基于 DiffusionNFT 的 Omni-Edit RL 对齐优化。相比直接联合训练或线性 LoRA 合并，任务蒸馏在局部/全局任务上分别取得 **4.43/3.89** 分，显著优于联合训练（4.18/3.52）和线性合并（4.27/3.71）。完整的 $R_{\text{omni}}$ 奖励模型配合 RL 后进一步提升至 **4.76/4.20**，消融实验证实移除负样本对或图像到海报提示均会导致性能下降。

在 PosterOmni-Bench 上，PosterOmni 的总体得分达到 **4.37**，较基线模型 Qwen-Image-Edit（3.51）提升 **+0.86**；在布局驱动任务上领先 **+0.76**，在风格驱动任务上领先 **+1.40**，在所有开源基线中取得最优，并在人类偏好研究中与商业系统 Seedream-4.0 表现持平。该方法在方法谱系上属于**任务蒸馏 + 统一奖励强化学习**的扩散模型对齐范式，为多任务图像编辑与生成提供了一条可复现的整合路径。

### 图像到海报生成的双重困境

海报创作是一项高度复合的视觉设计任务，要求系统同时具备两类截然不同的能力：**局部编辑精度**（如实体保留、空间一致性、文本渲染准确性）与**全局创作理解**（如布局规划、风格迁移、美学和谐）。现有开源图像编辑模型——包括 **ICEdit**（Zhang et al., arXiv 2025）、**Step1X-Edit**（Liu et al., arXiv 2025）、**FLUX.1 Kontext**（Batifol et al., arXiv 2025）以及 **Qwen-Image-Edit**（Chenfei Wu et al., arXiv 2025）——虽然在单一编辑任务上取得了进展，但在面对多任务图像到海报生成时，普遍存在布局错位、文本失真和美学质量下降等问题。其根本瓶颈在于：这些模型的设计范式未能将局部编辑与全局创作视为两个需要协同优化的互补子空间，导致任务干扰和能力割裂。

与此同时，商业系统如 **Seedream-4.0**（Seedream Team, arXiv 2025）虽在海报生成的整体质量上表现突出，但其技术细节和训练数据均未公开，难以复现或进行学术研究。开源社区亟需一个能够统一局部编辑与全局创作的端到端框架。

### 现有方法缺口

从方法学角度审视，现有工作的缺口集中在三个层面：

1. **训练策略的单一性**：主流方法采用标准多任务联合监督微调（joint SFT），将所有任务的数据混合训练。这种方式忽略了局部编辑与全局创作在特征空间中的分布差异，导致模型在学习过程中产生任务间干扰，无法同时精通两类能力。

2. **奖励信号的缺失**：图像编辑模型的训练通常仅依赖像素级或速度场回归损失，缺乏对整体美学质量和任务完成度的显式反馈信号。即便部分工作引入了通用图像偏好奖励，也未能针对海报生成的多任务特性提供差异化的精度评估。

3. **强化学习对齐的空白**：在图像编辑领域，基于人类偏好或自动评估指标的强化学习对齐方法尚未被系统性地引入，导致模型输出与人类审美标准之间存在显著差距。

### 本文动机

针对上述瓶颈，本文提出 **PosterOmni**——一个通过**任务蒸馏（Task Distillation）**和**统一奖励反馈（Unified PosterOmni Reward Feedback）**驱动的广义艺术海报创作框架。核心动机可概括为三个递进目标：

- **任务解耦与专家化**：将海报生成显式分解为局部编辑（扩展、填充、缩放、身份驱动）和全局创作（布局驱动、风格驱动）两类子任务，分别训练专家模型，避免任务间干扰。
- **知识蒸馏整合**：通过教师-学生蒸馏框架，将局部与全局专家的互补能力注入单一统一模型，实现精细化编辑与全局美学对齐的协同优化。
- **统一奖励对齐**：构建覆盖多任务的统一奖励模型，同时注入美学偏好与任务精度信号，并通过基于 DiffusionNFT 的强化学习方法将奖励反馈融入前向扩散目标，使模型输出与人类偏好对齐。

通过这一数据–蒸馏–奖励流水线，PosterOmni 旨在成为首个统一局部编辑与全局创作的开源图像到海报生成系统，在参考一致性、全局构图质量和美学和谐性上全面超越现有开源基线，并与商业系统形成竞争力。

## 核心方法与创新机理

PosterOmni 的核心创新并非提出全新的生成架构，而是在现有流匹配（Flow Matching）图像编辑基座之上，通过**任务蒸馏（Task Distillation）**与**统一奖励反馈（Unified Reward Feedback）**两个关键机制，系统性地解决了“局部编辑精度”与“全局创作美学”难以在同一模型中兼得的瓶颈。其创新点可凝练为三个相互耦合的 changed slots：

### 1. 训练策略：从多任务联合 SFT 到任务蒸馏

传统多任务微调通常采用**联合训练（Joint Training）**，即将所有任务的混合数据一次性送入模型进行监督微调。然而，局部编辑（如实体保留、空间一致性）与全局创作（如布局、风格、美学和谐）在特征空间上存在显著差异，直接混合训练容易引发**任务干扰**，导致布局错位、文本失真和美学质量下降。

PosterOmni 将这一过程重构为两阶段：
- **阶段一：任务特定 SFT**。分别微调**局部编辑专家**（覆盖 Rescaling、Filling、Extending、ID-driven 四个任务）和**全局创作专家**（覆盖 Style-driven、Layout-driven 两个任务），使每个专家在其子空间内达到最优。
- **阶段二：任务蒸馏**。以局部和全局专家为教师，通过教师-学生蒸馏将两类能力注入一个统一的学生模型（PosterOmni-SFT）。蒸馏损失在标准流匹配损失之上增加了专家速度场对齐项（见 Eq. (15)），强制学生同时逼近两个教师的行为。

消融实验（Table 2）量化了这一设计的优势：PosterOmni-SFT 在局部/全局任务上分别取得 **4.43 / 3.89** 分，优于联合训练（4.18 / 3.52）和线性 LoRA 合并（4.27 / 3.71）。这表明，显式的任务分解与蒸馏能有效规避任务干扰，是统一模型能力的关键。

### 2. 奖励信号：从无/通用偏好奖励到统一任务反馈

现有开源编辑模型通常缺乏精细的奖励信号，或仅依赖通用图像偏好奖励（如 PickScore、HPSv2），无法感知不同海报任务对精度和美学的差异化要求。

PosterOmni 提出了**统一 PosterOmni 奖励模型 $R_{\text{omni}}$**，其核心设计在于：
- **偏好数据构建**：从 SFT 模型的输出中采样成对结果，经 Gemini-2.5-Pro 过滤后由人类标注者选择优胜者，形成覆盖多任务的偏好数据集。
- **任务特定反馈**：$R_{\text{omni}}$ 同时注入**通用美学偏好**和**任务特定精度信号**（如文本准确性、实体一致性），通过 Bradley-Terry 偏好损失（Eq. (16)）进行训练。

消融实验（Table 5）揭示了统一奖励的贡献：完整 $R_{\text{omni}}$ 在局部/全局任务上达到 **4.76 / 4.20**；移除负样本对后降至 4.64 / 4.03；移除 image-to-poster 提示后降至 4.67 / 4.09。这表明，**多任务统一的奖励反馈**是 RL 对齐阶段性能提升的核心驱动力。

### 3. RL 微调方法：从无 RL 到 DiffusionNFT 驱动的 Omni-Edit RL

在获得统一奖励模型后，PosterOmni 进一步引入基于 **DiffusionNFT** 的强化学习策略（Omni-Edit RL），将奖励信号注入前向扩散目标。其核心思想是：通过构造正/负速度场策略（Eq. (18)），以对比式策略损失（Eq. (17)）引导模型在扩散轨迹上向高奖励方向偏移，同时避免传统策略梯度方法中的似然近似和训练不稳定问题。

这一设计使得 RL 阶段能够直接利用 $R_{\text{omni}}$ 的细粒度反馈，在 SFT 基础上进一步对齐人类偏好，最终在 PosterOmni-Bench 上实现对开源基线的全面超越（Overall Score 4.37 vs. Qwen-Image-Edit 3.51），并在布局驱动（+0.76）和风格驱动（+1.40）任务上展现出显著优势。

---

**综上**，PosterOmni 的创新本质是**任务分解-蒸馏整合-统一奖励对齐**的三阶段协同：任务蒸馏解决了多任务能力融合中的干扰问题，统一奖励模型提供了覆盖精度与美学的细粒度反馈，Omni-Edit RL 则将该反馈高效地注入生成过程。三者共同构成了从数据到模型的对齐闭环。

PosterOmni 构建了一个**数据–蒸馏–奖励**三阶段闭环，将图像到海报的生成统一为局部编辑与全局创作的协同优化问题。整个框架围绕一个核心洞察展开：海报生成任务天然存在两个互补的子空间——局部编辑（实体保留、空间一致性）和全局创作（布局、风格、美学和谐），现有开源模型难以同时兼顾二者，导致布局错位、文本失真和美学质量下降。PosterOmni 通过显式分解任务、专家知识蒸馏和统一奖励反馈，将这两类能力整合到一个统一模型中。

### 任务分解与数据流

框架首先将图像到海报生成显式建模为六大代表性任务，分为两组：

- **局部编辑**：扩展（Extending）、填充（Filling）、缩放（Rescaling）、身份驱动（Identity-driven）
- **全局创作**：布局驱动（Layout-driven）、风格驱动（Style-driven）

数据流始于一个**全自动数据构建管道**（Figure 2），该管道整合了提示生成、图像生成和多模态过滤三个环节，针对产品、食品、活动/旅行、自然、教育、娱乐六大主题场景，构建任务特定的输入-输出对，最终形成 **PosterOmni-200K** 训练集和 **PosterOmni-Bench** 评测基准。

![[assets/figures/papers/paper_list_l2290_https_arxiv_org_abs_2602_12127/figures/003_Figure_2.jpg]]
*Figure 2: We decompose image-to-poster generation into local editing and global creation, including extending, filling, rescaling, identity-driven, layout-driven, and style-driven generation. Our overall pipeline integrates prompt generation, image generation, multimodal filtering, and task-specific construction into a unified framework for large-scale, imageto-poster data generation. We then propose PosterOmni-200K and PosterOmni-Bench, which encompass six major poster themes and multi-image input scenarios*

### 四阶段训练流程

模型训练遵循四阶段递进式工作流（Figure 4）：

1. **任务特定 SFT（Task-specific SFT）**：分别微调局部编辑专家和全局创作专家，各自在对应任务数据上使用流匹配损失进行监督训练：
   $$\mathcal{L}_{\mathrm{SFT}} = \mathbb{E}_{\boldsymbol{x}_t, \boldsymbol{v}_t \sim \boldsymbol{q}(\boldsymbol{x}_t, \boldsymbol{v}_t)} \left[ \| \boldsymbol{v}_t - \boldsymbol{v}_{\boldsymbol{\theta}}(\boldsymbol{x}_t, t, \boldsymbol{c}_t) \|_2^2 \right]$$

2. **任务蒸馏（Task Distillation）**：通过教师-学生蒸馏将局部与全局专家的知识整合到统一的 **PosterOmni-SFT** 模型中，联合优化辅助文本渲染损失和专家蒸馏损失：
   $$\mathcal{L}_{\mathrm{total}} = \underbrace{\mathbb{E}_{\boldsymbol{x}_t, \boldsymbol{v}_t \sim \boldsymbol{q}(\boldsymbol{x}_t, \boldsymbol{v}_t)} \left[ \| \boldsymbol{v}_t - \boldsymbol{v}_{\theta}(\boldsymbol{x}_t, t, c_t) \|_2^2 \right]}_{\mathrm{Auxiliary~(Text~Rendering)~Loss}} + \underbrace{\lambda_{\mathrm{E}} \mathbb{E}_{\boldsymbol{x}_t, \boldsymbol{v}_t \sim \boldsymbol{q}(\boldsymbol{x}_t, \boldsymbol{v}_t)} \left[ \| \boldsymbol{v}_{\theta}(\boldsymbol{x}_t, t, c_t) - \boldsymbol{v}_{\mathrm{E}}(\boldsymbol{x}_t, t, c_t) \|_2^2 \right]}_{\mathrm{Task~Distillation~Loss}}$$

3. **统一奖励训练（PosterOmni Reward Training）**：构建偏好数据集（由 SFT 模型生成候选、Gemini-2.5-Pro 过滤、人工标注选择），基于 Bradley-Terry 模型训练统一的 **PosterOmni 奖励模型** $R_{\mathrm{omni}}$，同时注入通用美学偏好和任务特定精度信号：
   $$\mathcal{L}_{\mathrm{BT}} = -\mathbb{E}_{(I_{\mathrm{chosen}}, I_{\mathrm{rejected}})} \Big[ \log \sigma \big( r_{\theta}(I_{\mathrm{chosen}}) - r_{\theta}(I_{\mathrm{rejected}}) \big) \Big]$$

4. **Omni-Edit 强化学习（Omni-Edit RL）**：基于 DiffusionNFT 的对比式策略优化，将 $R_{\mathrm{omni}}$ 的奖励信号注入前向扩散目标，通过正/负速度场策略进行对齐优化：
   $$\mathcal{L}_{\mathrm{RL}} = \mathbb{E}_{c, t} \Big[ r \, \| v_{\theta}^{+}(x_t, c, t) - v \|_2^2 + (1 - r) \, \| v_{\theta}^{-}(x_t, c, t) - v \|_2^2 \Big]$$
   其中正/负速度场通过超参数 $\beta$ 控制更新强度：
   $$v_{\theta}^{+}(x_t, c, t) = (1 - \beta) v_{\mathrm{old}}(x_t, c, t) + \beta v_{\theta}(x_t, c, t)$$
   $$v_{\theta}^{-}(x_t, c, t) = (1 + \beta) v_{\mathrm{old}}(x_t, c, t) - \beta v_{\theta}(x_t, c, t)$$

### 因果机制与效果验证

整个框架的关键因果旋钮在于：**任务蒸馏避免了多任务联合训练中的任务间干扰**，而**统一奖励模型同时提供了美学偏好与任务精度的双重信号**。消融实验证实了这一设计的有效性：

- 任务蒸馏（PosterOmni-SFT）在局部/全局任务上取得 4.43/3.89，显著优于联合训练（4.18/3.52）和线性 LoRA 合并（4.27/3.71）（Table 2）。
- 完整的 $R_{\mathrm{omni}}$ 奖励模型配合 Omni-Edit RL 达到 4.76/4.20，移除负样本对后降至 4.64/4.03，移除图像到海报提示后降至 4.67/4.09，验证了统一奖励反馈的必要性（Table 5）。

最终，PosterOmni 在 PosterOmni-Bench 上取得 4.37 的总体评分，相较基线 **Qwen-Image-Edit**（Chenfei Wu et al., arXiv 2025）的 3.51 提升 +0.86，在布局驱动和风格驱动任务上分别提升 +0.76 和 +1.40（Table 1），并在人类偏好研究中与商业系统 **Seedream-4.0**（Seedream Team, arXiv 2025）表现相当（Figure 9）。

![[assets/figures/papers/paper_list_l2290_https_arxiv_org_abs_2602_12127/figures/002_Figure_1.jpg]]
*Figure 1: PosterOmni unifies local editing and global creation within a single image-to-poster generation framework. It covers six representative tasks—extending, filling, rescaling, identity-driven, layout-driven, and style-driven poster generation—enabling the model to achieve both fine-grained visual editing and holistic aesthetic composition*

PosterOmni 的训练流程由四个关键模块串联构成（Figure 4），其核心思想是将图像到海报生成任务显式分解为局部编辑与全局创作两个子空间，通过任务蒸馏（Task Distillation）和统一奖励反馈（Unified Reward Feedback）驱动强化学习，将两类能力整合到一个统一模型中。

### 任务特定监督微调

首先，将六类代表性任务划分为局部编辑和全局创作两个集合：

$$ \mathcal{T} = \underbrace{\{ \mathrm{Rescaling, Filling, Extending, ID} \}}_{\mathrm{Local\ Editing}} \cup \underbrace{\{ \mathrm{Style, Layout} \}}_{\mathrm{Global\ Creation}} $$

基于流匹配（Flow Matching）框架，对每个任务分别微调专家模型。流匹配训练目标为：

$$ \mathcal{L}_{\mathrm{FM}}(\theta) = \mathbb{E}_{t, x_0, x_1} \left[ \| v - v_{\theta}(x_t, t, c) \|_2^2 \right] $$

其中 $x_t = \alpha_t x_0 + \sigma_t \epsilon$ 为扩散轨迹，$v = \dot{\alpha}_t x_0 + \dot{\sigma}_t \epsilon$ 为瞬时速度场，模型学习预测该速度场。任务特定 SFT 的损失函数为：

$$ \mathcal{L}_{\mathrm{SFT}} = \mathbb{E}_{\boldsymbol{x}_t, \boldsymbol{v}_t \sim \boldsymbol{q}(\boldsymbol{x}_t, \boldsymbol{v}_t)} \left[ \| \boldsymbol{v}_t - \boldsymbol{v}_{\boldsymbol{\theta}}(\boldsymbol{x}_t, t, \boldsymbol{c}_t) \|_2^2 \right] $$

此阶段产出局部编辑专家和全局创作专家两个模型，各自精通其子任务域。

### 任务蒸馏

为避免多任务联合训练中的任务干扰，PosterOmni 采用教师-学生蒸馏策略，将两个专家的知识整合到统一的学生模型中。蒸馏损失联合了辅助文本渲染损失和专家蒸馏损失：

$$ \mathcal{L}_{\mathrm{total}} = \underbrace{\mathbb{E}_{{x}_t, {v}_t \sim {q}({x}_t, {v}_t)} \left[ \| {v}_t - {v}_{\theta}({x}_t, t, c_t) \|_2^2 \right]}_{\mathrm{Auxiliary\ (Text\ Rendering)\ Loss}} + \underbrace{\lambda_{\mathrm{E}} \mathbb{E}_{{x}_t, {v}_t \sim {q}({x}_t, {v}_t)} \left[ \| {v}_{\theta}({x}_t, {t}, {c}_t) - {v}_{\mathrm{E}}({x}_t, {t}, {c}_t) \|_2^2 \right]}_{\mathrm{Task\ Distillation\ Loss}} $$

其中 $v_{\mathrm{E}}$ 为对应任务专家的速度场输出，$v_{\theta}$ 为学生模型输出，$\lambda_{\mathrm{E}}$ 控制蒸馏强度。消融实验（Table 2）证实，蒸馏策略（Local/Global 得分 4.43/3.89）显著优于联合训练（4.18/3.52）和线性 LoRA 合并（4.27/3.71）。

### 统一奖励模型

为同时注入美学偏好与任务精度信号，PosterOmni 构建了统一奖励模型 $R_{\mathrm{omni}}$。训练数据来自 SFT 模型的多任务输出，经 Gemini-2.5-Pro 过滤后由人工标注偏好对。采用 Bradley-Terry 偏好损失：

$$ \mathcal{L}_{\mathrm{BT}} = -\mathbb{E}_{(I_{\mathrm{chosen}}, I_{\mathrm{rejected}})} \Big[ \log \sigma \big( r_{\theta}(I_{\mathrm{chosen}}) - r_{\theta}(I_{\mathrm{rejected}}) \big) \Big] $$

该损失将成对比较转化为可微目标，使奖励模型能够同时评估局部编辑精度和全局美学质量。

### Omni-Edit 强化学习

最后阶段，PosterOmni 采用基于 DiffusionNFT 的 Omni-Edit RL，将 $R_{\mathrm{omni}}$ 的奖励信号注入前向扩散目标。核心是对比式策略损失：

$$ \mathcal{L}_{\mathrm{RL}} = \mathbb{E}_{c, t} \Big[ r \cdot \| v_{\theta}^{+}(x_t, c, t) - v \|_2^2 + (1 - r) \cdot \| v_{\theta}^{-}(x_t, c, t) - v \|_2^2 \Big] $$

其中 $r$ 为归一化奖励值（clamp 至 $[-1, 1]$），正/负速度场策略定义为：

$$ v_{\theta}^{+}(x_t, c, t) = (1 - \beta) v_{\mathrm{old}}(x_t, c, t) + \beta v_{\theta}(x_t, c, t) $$

$$ v_{\theta}^{-}(x_t, c, t) = (1 + \beta) v_{\mathrm{old}}(x_t, c, t) - \beta v_{\theta}(x_t, c, t) $$

$\beta$ 控制更新强度：当奖励为正时，模型向当前策略方向更新；奖励为负时则反向远离。与策略梯度类 RL 方法不同，DiffusionNFT 保持了前向扩散的一致性，隐式地将强化信号融入速度场，避免了似然近似，实现了简单且稳定的对齐优化。消融实验（Table 3）表明，完整的 $R_{\mathrm{omni}}$ 配合 Omni-Edit RL 达到 4.76/4.20（Local/Global），移除负样本对或图像到海报提示分别降至 4.64/4.03 和 4.67/4.09，验证了统一奖励反馈中多维度信号的必要性。

## 实验与关键发现

PosterOmni 的实验体系围绕自建基准 PosterOmni-Bench 展开，通过自动评估与人类偏好研究双重验证，系统性地回答了三个核心问题：统一模型能否同时胜任局部编辑与全局创作、任务蒸馏是否优于其他专家集成策略、以及统一奖励反馈能否带来进一步的性能增益。

### 整体性能：开源模型中的全面领先

Table 1 报告了在 PosterOmni-Bench-en 上的主结果。PosterOmni 以 **4.37** 的总分显著超越最强开源基线 **Qwen-Image-Edit**（3.51），相对提升 **+0.86**。这一优势在六类子任务上普遍存在：局部编辑任务（扩展、填充、缩放、身份驱动）的增益在 +0.48 至 +0.98 之间；全局创作任务中，布局驱动得分 4.20（基线 3.44，+0.76），风格驱动得分 4.31（基线 2.91，+1.40），后者的大幅差距表明全局美学理解是现有编辑模型的核心短板。值得注意的是，PosterOmni 甚至超越了部分商业系统，在开源模型阵营中确立了新的性能上界。

![[assets/figures/papers/paper_list_l2290_https_arxiv_org_abs_2602_12127/figures/007_Table_1.jpg]]
*Table 1: Quantitative comparison results on proposed PosterOmni-Bench. We use Gemini-2.5-Pro [33] for evaluation poster creation results. Bold indicates the best performance. We highlight the best and second metrics. The numbers before and after “/” correspond to the PosterOmni-Bench-en and PosterOmni-Bench-cn, respectively*

评估采用 Gemini-2.5-Pro 作为自动打分器，这一选择虽然保证了评分的一致性和可复现性，但单一评估器可能引入视觉-语言模型的固有偏好。为此，Figure 9 提供了人类偏好研究的对冲证据：在审美价值、任务对齐、文本准确度和综合偏好四个维度上，PosterOmni 显著优于所有开源竞争系统，并与最先进的商业系统 Seedream-4.0 表现持平，验证了自动评估结论的可靠性。

![[assets/figures/papers/paper_list_l2290_https_arxiv_org_abs_2602_12127/figures/014_Figure_9.jpg]]
*Figure 9: Human preference study for image-to-poster generation. We compare PosterOmni with six competing systems (Seedream-4.0 [30], Seedream-3.0 [9], UniWorld-V2–Qwen-Image-Edit [18], Qwen-Image-Edit [2509] [36], FLUX.1 Kontext [dev] [2], and BAGEL [7]) under four criteria: Aesthetic Value, Task (Prompt) Alignment, Text Accuracy, and Overall Preference. For each pairwise comparison, bars report the fraction of cases in which PosterOmni is preferred (light purple), tied (gray), or worse (red) than the competing model. The vertical dashed line at 0.5 denotes parity; bars extending to the right indicate that PosterOmni is more often favored than the corresponding baseline. Overall, PosterOmni signific...*

### 任务蒸馏：避免多任务干扰的关键设计

Table 2/6 的消融实验直接比较了三种专家集成策略。任务蒸馏（PosterOmni-SFT）在局部（L=4.43）和全局（G=3.89）任务上均取得最优，而联合训练（joint training）仅得 4.18/3.52，线性 LoRA 合并（linear LoRA merge）得 4.27/3.71。联合训练的退化揭示了局部编辑与全局创作之间存在显著的任务干扰——两类任务对特征空间的诉求可能相互冲突，简单混合训练导致模型在两个方向上都无法达到专家水平。线性 LoRA 合并虽优于联合训练，但仍不及蒸馏，说明权重空间的线性插值无法有效整合异构能力。Figure 10 的定性对比进一步佐证：线性合并和 ZipLoRA 合并在布局驱动和风格驱动任务上出现了明显的布局错位和风格不一致，而蒸馏模型则保持了与参考图像的空间对齐和美学连贯性。

![[assets/figures/papers/paper_list_l2290_https_arxiv_org_abs_2602_12127/figures/008_Table_2.jpg]]
*Table 2: Ablation study of our task distillation. Scores are averaged on the selected local (extend) and global (layout) tasks*

蒸馏损失的设计（Eq. 15）包含两个关键组分：辅助文本渲染损失保证基础编辑能力不退化，专家蒸馏损失通过速度场对齐将局部和全局专家的知识迁移至学生模型。这种“先专后统”的策略本质上是一种能力解耦与重组——让专家各自在子空间内达到局部最优，再通过蒸馏寻找统一参数空间中的帕累托前沿。

### 统一奖励反馈：美学与精度的双重对齐

Table 5 的消融揭示了统一奖励模型 R_omni 的增益来源。完整 R_omni 配合 Omni-Edit RL 后，局部和全局得分分别达到 4.76/4.20。移除负样本对（negative pairs）后降至 4.64/4.03，表明对比式偏好信号对于模型区分优劣生成至关重要；移除图像到海报的专用提示（image-to-poster prompt）后降至 4.67/4.09，说明任务特定的条件信息是奖励模型准确判断精度的前提。这两项消融共同验证了统一奖励反馈的核心价值：它不仅注入通用的美学偏好，更通过任务感知的条件编码提供了细粒度的精度信号。

![[assets/figures/papers/paper_list_l2290_https_arxiv_org_abs_2602_12127/figures/015_Table_5.jpg]]
*Table 5: Ablation study of PosterOmni Reward Model design. Scores are averaged on a local task (extend, L) and a global task (layout-driven, G)*

Omni-Edit RL 基于 DiffusionNFT 框架（Eq. 17-18），其核心机制是将归一化后的奖励 r 作为权重，对正向速度策略 v⁺_θ 和负向速度策略 v⁻_θ 进行对比式优化。与策略梯度类方法不同，DiffusionNFT 直接在速度场上施加约束，避免了似然估计的不稳定性，使得 RL 微调能够在流匹配框架下简洁而稳定地收敛。

### 失败模式与局限性

尽管整体性能优异，PosterOmni 仍存在若干结构性局限。首先，当前框架仅覆盖六种预定义任务，无法处理动态元素、交互组件等更复杂的海报设计需求，任务边界的外推能力未经验证。其次，评估体系对 Gemini-2.5-Pro 的强依赖意味着评分标准可能偏向该模型的审美偏好，大规模人工标注基准的缺失使得绝对性能的校准存在不确定性。此外，框架在幻灯片、网页横幅、多页宣传册等非海报图形设计任务上的泛化能力尚未测试，任务蒸馏的跨域迁移特性仍是开放问题。最后，模型不支持多轮交互式共创或序列化海报的一致性控制，限制了其在真实协作场景中的适用性。

## 定位与知识库关联

### 任务定位：从单任务编辑到统一图像到海报生成

PosterOmni 瞄准的是一个现有开源模型尚未充分覆盖的交叉地带——**多任务图像到海报生成**。该任务同时要求局部编辑精度（实体保留、空间一致性）和全局创作理解（布局、风格、美学和谐），而现有工作大多只覆盖其中一侧。

在局部编辑侧，**ICEdit**（Zhang et al., arXiv 2025）、**Step1X-Edit**（Liu et al., arXiv 2025）等开源图像编辑模型在单任务编辑上表现良好，但缺乏对全局构图和风格迁移的理解。在全局生成侧，**FLUX.1 Kontext**（Batifol et al., arXiv 2025）作为流匹配上下文编辑器、**OmniGen2**（Chenyuan Wu et al., arXiv 2025）作为多模态生成模型，以及商业系统 **Seedream-3.0/4.0**（Gao et al. / Seedream Team, arXiv 2025）在文生图质量上表现突出，但难以精确控制局部编辑的引用一致性和文本保真度。

PosterOmni 的核心贡献在于**将这两个子空间显式建模为互补任务，并通过任务蒸馏和统一奖励反馈将它们整合到一个单一模型中**。其直接基线 **Qwen-Image-Edit**（Chenfei Wu et al., arXiv 2025）在 PosterOmni-Bench-en 上的 Overall Score 为 3.51，而 PosterOmni 达到 4.37（+0.86，Table 1），这一差距在 Style-driven 任务上尤为显著（2.91 vs 4.31，+1.40），说明全局创作能力是拉开差距的关键维度。

### 技术谱系：流匹配、知识蒸馏与扩散强化学习的交汇

从技术栈来看，PosterOmni 处于三条技术线的交汇点：

**（1）流匹配生成建模。** PosterOmni 基于流匹配（Flow Matching）框架构建，其训练目标为 $\mathcal{L}_{\mathrm{FM}}(\theta) = \mathbb{E}_{t, x_0, x_1}[\|v - v_\theta(x_t, t, c)\|_2^2]$（Eq. 6）。这一选择与 **FLUX**（Black Forest Labs, 2024）等前沿工作一致，相比传统扩散模型在采样效率和生成质量上具有优势。

**（2）知识蒸馏与多专家融合。** 在多任务学习中，联合训练（joint training）常因任务间梯度冲突导致性能下降。PosterOmni 采用教师-学生蒸馏策略：先分别训练局部编辑专家和全局创建专家，再通过蒸馏损失 $\mathcal{L}_{\mathrm{total}}$（Eq. 15）将两类知识迁移到统一学生模型中。消融实验（Table 2）证实了这一设计的必要性——任务蒸馏（PosterOmni-SFT）在局部/全局任务上分别达到 4.43/3.89，显著优于联合训练（4.18/3.52）和线性 LoRA 合并（4.27/3.71）。这与多任务学习中常见的“任务干扰”现象一致：局部编辑需要保留像素级引用一致性，而全局创建需要大胆重构布局和风格，二者的梯度方向天然冲突。

**（3）扩散强化学习与偏好对齐。** PosterOmni 引入基于 DiffusionNFT 的 Omni-Edit RL，将奖励信号注入前向扩散目标。其策略损失为 $\mathcal{L}_{\mathrm{RL}} = \mathbb{E}_{c,t}[r \cdot \|v_\theta^+(x_t, c, t) - v\|_2^2 + (1-r) \cdot \|v_\theta^-(x_t, c, t) - v\|_2^2]$（Eq. 17），通过正/负速度场策略（Eq. 18）实现对比优化。与策略梯度类方法不同，DiffusionNFT 保持了前向一致性，避免了似然近似带来的不稳定性。这一设计在思想上与 **UniWorld-V2-Qwen-Image-Edit**（Li et al., arXiv 2025）的 RL 增强编辑方向相近，但 PosterOmni 的统一奖励模型 $R_{\mathrm{omni}}$ 同时覆盖通用美学偏好和任务特定精度信号，消融实验（Table 5）显示移除负样本对或图像到海报提示都会导致性能下降，验证了统一反馈的必要性。

### 适用边界与局限

**任务覆盖范围。** PosterOmni 当前仅覆盖六种预定义任务（extending、filling、rescaling、identity-driven、layout-driven、style-driven），这些任务虽然具有代表性，但尚未涉及动态元素（如动画效果）、交互组件（如可点击按钮）或多页宣传册等更复杂的海报设计场景。论文未验证框架在非海报图形设计任务（如幻灯片、网页横幅、Logo 生成、UI 布局）上的泛化能力。

**评估可靠性。** 主要评估依赖 Gemini-2.5-Pro 自动评分，虽然人类偏好研究（Figure 9）验证了排序一致性，但单一自动评估器可能引入视觉-语言模型的系统性偏好偏差。目前缺乏大规模人工标注基准的独立验证。

**交互与序列化控制。** 当前框架为单轮生成，不支持多轮交互式共创（如用户点击、拖拽调整布局后迭代优化），也不支持序列化海报的一致性控制（如系列海报的品牌色和字体统一）。

**模型压缩与部署。** 论文未讨论在资源受限设备上的模型压缩方案，训练流程涉及四阶段（任务特定 SFT → 任务蒸馏 → 奖励训练 → Omni-Edit RL），计算开销较大。

### 开放问题

1. **跨任务泛化。** 统一奖励模型 $R_{\mathrm{omni}}$ 与任务蒸馏框架能否直接适配其他视觉设计任务（如 Logo 生成、信息图表、UI 布局）？这需要验证任务分解策略和奖励信号的可迁移性。

2. **灾难性遗忘。** 任务蒸馏过程中，学生模型在学习全局创建能力时是否会遗忘基础编辑能力？论文未报告蒸馏前后单任务性能的逐项对比，引入抗遗忘正则（如 EWC、LwF）可能是进一步优化的方向。

3. **个性化协同创作。** 如何将用户交互信号（点击、拖拽、自然语言反馈）注入 RL 奖励模型，实现个性化海报的迭代共创？这需要将人类反馈从静态偏好扩展到动态交互序列。

4. **奖励模型的鲁棒性。** $R_{\mathrm{omni}}$ 的训练依赖 Gemini-2.5-Pro 过滤和人工标注构建偏好对，这一过程是否引入了标注者的文化偏见（如对特定美学风格的偏好）？跨文化场景下的公平性需要进一步验证。

5. **效率优化。** 四阶段训练流程的计算开销是否可以通过联合优化（如端到端可微蒸馏 + RL）或模型剪枝来降低？这在工业部署场景下尤为重要。

## 原文 PDF

![[paperPDFs/CVPR_2026/PosterOmni_Generalized_Artistic_Poster_Creation_via_Task_Distillation_and_Unified_Reward_Feedback.pdf]]
