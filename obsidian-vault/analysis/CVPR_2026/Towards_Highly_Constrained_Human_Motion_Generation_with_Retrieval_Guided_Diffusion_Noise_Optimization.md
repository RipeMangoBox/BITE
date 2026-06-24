---
title: Towards Highly-Constrained Human Motion Generation with Retrieval-Guided Diffusion Noise Optimization
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Towards_Highly_Constrained_Human_Motion_Generation_with_Retrieval_Guided_Diffusion_Noise_Optimization.pdf
paper_link: https://openaccess.thecvf.com/content/CVPR2026/html/Liu_Towards_Highly-Constrained_Human_Motion_Generation_with_Retrieval-Guided_Diffusion_Noise_Optimization_CVPR_2026_paper.html
project_link: https://hanchaoliu.github.io/RetrievalGuidedDNO/
code_link: null
aliases:
- RGDNORD
- THCHMGRGDNO
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 通过关系任务解析识别出任务中最困难的约束，据此从现有大规模运动数据集中检索相关运动技能，将检索到的运动反演为扩散噪声，再通过蒙版优化将检索噪声与随机噪声智能结合，为扩散模型提供更优的初始噪声。
primary_logic: 扩散模型早期噪声的选取对最终生成质量至关重要；利用现有运动数据集作为外部知识库，通过检索-蒙版组合的方式注入先验技能，可将高度约束任务分解为可解的子问题，从而突破单纯随机优化在困难约束下的能力边界。
claims:
- 在要求精确步数或通过狭窄障碍物的高度约束任务中，现有DNO方法产生高约束误差和运动伪影，而RG-DNO显著降低约束误差并提高运动自然度。
- 关系任务解析能准确识别困难约束并指导检索，仅对整个任务进行检索效果不佳，证明任务解析的必要性。
- 蒙版优化结合奖励函数可以滤除不合理的噪声组合，避免简单线性组合导致的过度平滑和运动质量下降。
- Task-1 (very narrow gap) 上 Constraint Error (C.Error) = 0.0050
---

# Towards Highly-Constrained Human Motion Generation with Retrieval-Guided Diffusion Noise Optimization

> [!tip] 核心洞察
> 扩散模型早期噪声的选取对最终生成质量至关重要；利用现有运动数据集作为外部知识库，通过检索-蒙版组合的方式注入先验技能，可将高度约束任务分解为可解的子问题，从而突破单纯随机优化在困难约束下的能力边界。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向高约束人体运动生成的检索引导扩散噪声优化 |
| 英文题名 | Towards Highly-Constrained Human Motion Generation with Retrieval-Guided Diffusion Noise Optimization |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Liu_Towards_Highly-Constrained_Human_Motion_Generation_with_Retrieval-Guided_Diffusion_Noise_Optimization_CVPR_2026_paper.html) · [Project](https://hanchaoliu.github.io/RetrievalGuidedDNO/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | Retrieval-Guided Diffusion Noise Optimization (RG-DNO) |
| Dataset | Task-1, Task-2, Task-3, Task HSI-2 |

> [!tip] 效果简介
> - Task-1 (very narrow gap) 上，Constraint Error (C.Error) 0.0050 vs 未提供具体数值（显著高于RG-DNO） (显著降低)。
> - Task-2 (very low overhead barrier) 上，Constraint Error (C.Error) 0.000049 vs 未提供具体数值（显著高于RG-DNO） (显著降低)。
> - Task-3 (precise steps & distance) 上，Constraint Error (C.Error) 0.0003 vs 未提供具体数值 (降低)。

## 概述

**问题瓶颈**：现有训练无关的扩散噪声优化（DNO）方法在处理高度挑战的时空约束（如通过非常狭窄的间隙）和精确数值控制（如指定步数）时，会遭遇高约束误差与运动伪影。其根本原因在于，DNO仅从随机高斯噪声出发进行优化，缺乏满足困难约束所需的特定运动技能和结构化知识，导致优化过程陷入次优解。

**核心思路**：本文提出 **检索引导的扩散噪声优化（RG-DNO）** 框架。其核心洞见是，扩散模型早期噪声的选取对最终生成质量至关重要——利用现有大规模运动数据集作为外部知识库，通过检索相关运动技能并将其反演为扩散噪声，再经蒙版优化与随机噪声智能结合，可为扩散模型提供更优的初始噪声，从而将高度约束任务分解为可解的子问题。

**方法定位**：RG-DNO 在 **ProgMoGen**（Liu et al., CVPR 2024）的运动编程框架和 **DNO**（Karunratanakul et al., CVPR 2024）的噪声优化范式基础上，引入了三个关键创新：（1）关系任务解析，将约束集按困难程度和依赖关系拆分为可检索子集与可优化子集；（2）基于约束的运动检索与反演，从外部数据集中提取结构化运动先验；（3）蒙版噪声优化与奖励引导的蒙版选择，在时空维度上智能融合检索噪声与随机噪声，同时通过运动质量奖励函数滤除不合理组合。

**主要结果**：在通过狭窄间隙（Task-1）、极低头顶障碍（Task-2）和精确步数控制（Task-3）等高度约束任务上，RG-DNO 显著降低了约束误差并提高了运动自然度。例如，在 Task-2 上约束误差降至 0.000049，Task-3 的成功率达到 0.594，均明显优于现有 DNO 基线。消融实验证实，关系任务解析、蒙版优化和奖励函数三个组件对性能提升均有决定性贡献。

## 背景与动机

### 扩散噪声优化：训练无关的运动控制新范式

基于扩散模型的人体运动生成近年来取得了显著进展，其核心是将运动序列建模为逐步去噪的过程。在扩散模型的标准推理中，生成结果完全由初始高斯噪声 $z \sim \mathcal{N}(0, I)$ 决定：给定一个初始噪声 $z_T$，通过确定性DDIM去噪步（Eq. 1）逐步还原为运动序列，整个过程不依赖额外的训练或微调。

扩散噪声优化（Diffusion Noise Optimization, DNO）**（Karunratanakul et al., CVPR 2024）** 进一步将这一特性转化为一个通用的训练无关控制框架：通过直接优化初始噪声 $z$ 来最小化生成运动在约束函数 $F$ 下的误差，即 $\min_z F(G(z, \mathcal{C}))$。在此基础上，**ProgMoGen**（Liu et al., CVPR 2024）提出了基于运动编程的组合约束框架，允许用户通过组合多种约束函数来定义复杂的生成任务，并在随机噪声空间中通过多轮搜索寻找满足约束的最优解。

这一范式的核心优势在于**训练无关性**：无需针对新任务重新训练或微调模型，仅需调整优化目标即可适应不同的约束组合，极大地降低了运动生成系统的部署成本。

### 高度约束场景下的根本瓶颈

然而，当任务约束变得极具挑战性时，现有DNO方法的性能会急剧恶化。典型的高度约束场景包括：

- **挑战性时空约束**：要求角色通过非常狭窄的间隙（如Task-1中的极窄竖直通道）或极低的头顶障碍物（如Task-2中仅略高于身体高度的横杆），这些约束要求运动在特定时刻达到高度精确的空间位置。
- **精确数值控制**：要求角色在指定距离内完成精确的步数（如Task-3中在固定行走距离内恰好迈出N步），这需要运动生成系统同时满足高层语义和低层数值的双重约束。

在这些任务中，现有DNO方法暴露出两个根本性缺陷：**高约束误差**和**运动伪影**（Figure 1）。从优化机制来看，问题的根源在于DNO始终从完全随机的标准高斯噪声出发进行优化。随机噪声本身不携带任何与任务相关的结构化知识或运动技能——它仅依赖扩散模型的隐式先验，通过约束函数的梯度信号来“摸索”可行解。

当约束条件变得苛刻时，这种“从零开始”的优化策略面临双重困境：一方面，约束函数的梯度信号在高度非凸的噪声空间中可能极其稀疏，导致优化陷入局部最优；另一方面，即使最终满足约束，由于缺乏对运动自然度的显式建模，生成结果往往出现关节抖动、脚部滑动等伪影。Figure 5进一步揭示了这一困境的系统性：随着障碍物高度降低或步数要求偏离自然步态，DNO的性能呈持续下降趋势。

### 核心洞察：外部知识驱动的噪声初始化

本文的核心洞察源于对扩散模型生成机制的一个关键观察：**扩散模型的早期噪声选取对最终生成质量具有决定性影响**。DDIM的确定性去噪过程意味着，初始噪声 $z_T$ 的微小变化会通过去噪链传播并放大，最终导致生成结果的显著差异。因此，如果能为优化过程提供一个“更聪明”的初始噪声——一个已经蕴含了任务所需运动技能的起点——那么后续的约束优化将变得更容易收敛，且生成质量更高。

这一洞察引出了一个自然的问题：**这些“运动技能”从何而来？** 本文的答案是：从现有的大规模运动数据集中检索。现实世界中已积累了丰富的运动捕捉数据，这些数据天然包含了各种运动技能的结构化知识——弯腰通过低矮障碍物的姿态、特定步数的行走节奏、跨越狭窄间隙的步态调整等。如果能将这些知识以适当的形式注入到扩散噪声空间中，就可以将高度约束的生成任务分解为“检索相关技能+局部优化适配”的两阶段问题，从而突破单纯随机优化的能力边界。

基于这一思路，本文提出了**检索引导的扩散噪声优化（Retrieval-Guided Diffusion Noise Optimization, RG-DNO）**框架，其核心机制包括三个层次：

1. **关系任务解析**：识别约束集中最困难的部分，避免对整个任务进行盲目检索；
2. **约束引导的检索与反演**：从数据集中找到最匹配困难约束的运动样本，并将其反演为扩散噪声；
3. **蒙版噪声优化**：通过可学习的线性蒙版智能组合检索噪声与随机噪声，在保留检索技能的同时保持运动的多样性与自然度。

这一框架的独特之处在于，它将外部数据集视为一个**可查询的运动技能知识库**，而非传统意义上的训练数据。通过检索-反演-组合的管线，RG-DNO在不修改扩散模型权重、不增加额外训练的前提下，显著扩展了训练无关运动生成的能力边界。

## 核心创新

### 问题瓶颈：随机噪声优化的能力边界

现有训练无关的扩散噪声优化（DNO）方法——如 **ProgMoGen**（Liu et al., CVPR 2024）和通用 **DNO**（Karunratanakul et al., CVPR 2024）——在处理高度约束的运动生成任务时暴露出根本性缺陷。这些方法从标准高斯随机噪声 $z \sim \mathcal{N}(0, I)$ 出发，通过梯度下降直接优化初始噪声以最小化约束函数：

$$\min_z F(G(z, \mathcal{C}))$$

当面对**挑战性时空约束**（如穿越极狭窄间隙、蹲行通过极低障碍物）或**精确数值控制**（如指定步数完成固定距离行走）时，随机噪声的优化空间缺乏满足这些困难约束所需的特定运动技能和结构化先验知识，导致高约束误差和运动伪影（Figure 1, Table 1, Table 2）。

### 核心洞察：检索作为先验注入机制

本文的关键突破在于认识到：**扩散模型的早期噪声选取对最终生成质量具有决定性影响**，而现有大规模运动数据集可以作为外部知识库，为困难约束提供“可复用的运动技能片段”。通过将检索到的相关运动反演为扩散噪声，并与随机噪声进行智能组合，可以将高度约束任务分解为可解的子问题，从而突破单纯随机优化在困难约束下的能力边界。

### 方法框架：RG-DNO 的四个关键 changed slots

基于上述洞察，**Retrieval-Guided Diffusion Noise Optimization（RG-DNO）** 在以下四个维度对标准 DNO 进行了根本性改造：

#### 1. 约束处理策略：从无差别优化到关系任务解析

**Baseline**：针对完整约束集 $\mathcal{C}$ 进行单一阶段的无差别优化。

**RG-DNO**：引入**关系任务解析（Relational Task Parsing）**，根据约束的困难程度和相互依赖关系，将原始约束集分解为三个子集：
- $\mathcal{C}_R$：最困难的约束子集，用于指导检索
- $\mathcal{C}_1$：可由随机噪声处理的约束
- $\mathcal{C}_2$：可由检索噪声处理的约束

$$\mathcal{C} = \mathcal{C}_1 \oplus \mathcal{C}_2, \quad \mathcal{C}_R \subseteq \mathcal{C}_2$$

这一分解使得框架能够识别出真正需要外部知识注入的瓶颈约束，而非盲目地对整个任务进行检索（消融实验证实，对整个任务检索效果不佳，Table 4）。

#### 2. 初始噪声来源：从纯随机噪声到检索-蒙版组合噪声

**Baseline**：标准高斯随机噪声 $z \sim \mathcal{N}(0, I)$。

**RG-DNO**：通过蒙版 $M$ 组合的噪声 $z' = M z_1 + (1-M) z_2$，其中：
- $z_1$：从随机噪声出发，针对 $\mathcal{C}_1$ 优化得到
- $z_2$：从检索运动反演噪声 $z_R$ 出发，针对 $\mathcal{C}_2$ 优化得到

检索噪声 $z_R$ 通过以下流程获取：在外部运动数据集 $\mathcal{D}$ 中，通过最小化 $\mathcal{C}_R$ 约束误差寻找合适的参考运动 $x_R$，并允许水平面刚性变换 $\mathcal{H}$ 以进一步降低误差：

$$x, \mathcal{H} = \arg\min_{x, \mathcal{H}} F_{\mathcal{C}_R}(\mathcal{H} x)$$

随后将变换后的样本反演为扩散初始噪声：

$$z_R = G^{-1}(\mathcal{H} x_R, C_0)$$

#### 3. 优化管线：从单轮优化到多阶段协同优化

**Baseline**：单轮优化 $\min_z F_{\mathcal{C}}(G(z, C_0))$，直接对随机初始噪声优化至收敛。

**RG-DNO**：采用三阶段优化管线：
1. **分路优化**：分别优化 $z_1$ 和 $z_2$ 以满足 $\mathcal{C}_1$ 和 $\mathcal{C}_2$
2. **蒙版优化**：在运动质量奖励 $\mathcal{R}$ 监督下优化蒙版 $M$，组合中间噪声：
   $$\min_M F_{\mathcal{C}}(G(z')) + \mathcal{R}(G(z'))$$
3. **最终微调**：以 $z'$ 为新起点执行最后一轮完整的约束优化：
   $$\min_{\delta z} F_{\mathcal{C}}(G(z' + \delta z))$$

#### 4. 运动质量保证：从无保真度约束到奖励引导的蒙版选择

**Baseline**：优化目标仅包含约束函数，无专门的保真度项。

**RG-DNO**：引入由四项指标构成的综合奖励函数 $\mathcal{R}$，用于在蒙版选择阶段过滤低质量组合：

$$\mathcal{R}(G(z'), z') = \lambda_1 \mathcal{L}_{\text{jitter}} + \lambda_2 \mathcal{L}_{\text{footskate}} + \lambda_3 \mathcal{L}_{\text{decorr}} + \lambda_4 \mathcal{L}_{\text{semantic}}$$

其中 $\mathcal{L}_{\text{jitter}}$ 惩罚关节抖动，$\mathcal{L}_{\text{footskate}}$ 惩罚脚滑动，$\mathcal{L}_{\text{decorr}}$ 鼓励噪声去相关以避免过度平滑，$\mathcal{L}_{\text{semantic}}$ 保证语义对齐。蒙版选择采用启发式策略，从预设的候选蒙版集合 $\mathcal{M}$（时间或空间切分）中选择最优者：

$$M = \arg\min_{M \in \mathcal{M}} F_{\mathcal{C}}(G(z')) + \mathcal{R}(G(z'))$$

消融实验证实，移除奖励函数后蒙版优化难以滤除不合理的时空组合，整体运动质量显著下降（Sec. 5.5）。

### 创新总结

RG-DNO 的本质创新在于将“检索外部知识→反演为扩散噪声→蒙版智能组合→奖励引导筛选”这一完整链路引入扩散噪声优化框架，使得原本受限于随机初始化的 DNO 方法获得了处理高度约束任务的能力。这一思路的核心价值在于：**不修改扩散模型本身，不增加训练成本，仅通过优化初始噪声的构造方式，就显著扩展了训练无关运动生成的能力边界**。

## 整体框架

RG-DNO 的核心思想是将高度约束的运动生成任务分解为可解的子问题，并通过检索外部运动数据集中的相关技能来引导扩散噪声优化过程。其整体管线包含五个顺序模块，形成一条从任务解析到最终运动生成的完整推理链。

**输入**：一个由组合约束函数 $F_C$ 定义的运动生成任务，可选地附带文本条件 $C_0$。约束函数可包含多种时空约束（如通过狭窄间隙、跨越低障碍物）和精确数值约束（如指定步数、移动距离）。

**关系任务解析**首先对约束集进行难度排序和依赖关系分析，将原始约束 $C$ 拆分为三个子集：检索目标集 $C_R$（最困难的约束子集，用于指导检索）、随机噪声适配集 $C_1$（可由随机噪声优化处理的约束）和检索噪声适配集 $C_2$（可由检索噪声优化处理的约束）。解析可通过人工规则或 LLM 推理完成。

**基于约束的检索**模块以 $C_R$ 为查询目标，在大规模运动数据集 $\mathcal{D}$ 中搜索使 $C_R$ 误差最小的运动样本 $x_R$，并同时优化水平面刚性变换 $\mathcal{H}$ 以进一步降低约束误差。检索到的样本经时序调整和语义一致性检查后，通过扩散模型的反演过程 $z_R = G^{-1}(\mathcal{H} x_R, C_0)$ 转换为检索噪声 $z_R$。

**蒙版噪声优化**分两阶段进行。第一阶段，分别以随机噪声和检索噪声 $z_R$ 为起点，优化两个噪声变量 $z_1$ 和 $z_2$，使其各自满足约束子集 $C_1$ 和 $C_2$。第二阶段，优化一个线性蒙版 $M$，将两个噪声组合为 $z' = M z_1 + (1 - M) z_2$，优化目标同时包含全约束误差 $F_C(G(z'))$ 和运动质量奖励 $\mathcal{R}(G(z'))$。

**奖励引导的蒙版选择**通过构建时间或空间维度的二值候选蒙版集合 $\mathcal{M}$，从中选择使组合目标最优的蒙版，以降低连续优化的难度并保证运动质量。奖励函数 $\mathcal{R}$ 由抖动惩罚、脚滑动惩罚、噪声去相关损失和语义对齐损失四项加权组成，默认权重 $\lambda_k = 1.0$。

**最终扩散噪声优化**以组合噪声 $z'$ 作为更优初始化，执行最后一轮标准 DNO 微调 $\min_{\delta z} F_C(G(z' + \delta z))$，得到满足全部约束的最终运动序列。

**输出**：一段满足高度时空与数值约束、同时保持自然运动质量的人体运动序列。

整个管线中，信息流从约束解析到检索、再到噪声组合与最终优化的递进关系清晰：关系解析将复杂问题结构化，检索注入外部先验技能，蒙版优化智能融合多源噪声，最终微调确保约束精确满足。这一设计使得 RG-DNO 能够在标准 DNO 失败的困难约束场景下（如通过极窄间隙或精确控制步数）显著降低约束误差并提高运动自然度。

### 补充图表

![[assets/figures/papers/paper_list_l11_https_openaccess_thecvf_com_content_CVPR2026_html_Liu_Towards_Highly_Con/figures/002_Figure_2.jpg]]
*Figure 2: Overview of Retrieval-Guided Diffusion Noise Optimization. Given a motion generation task represented by a combined constraint function*

## 核心模块与公式推导

### 3.1 问题形式化：高约束运动生成

给定一个预训练的运动扩散模型 $G$（基于 MDM 架构）和可选的文本条件 $C_0$，高约束运动生成任务被定义为一个约束优化问题：

$$\min_z \sum_i F_{C_i}(G(z, C_0)) \tag{3}$$

其中 $z \sim \mathcal{N}(0, I)$ 为初始噪声，$F_{C_i}$ 为第 $i$ 个约束子函数（如关节位置约束、步数约束等）。扩散模型 $G$ 通过 DDIM 确定性去噪过程从 $z$ 生成运动序列：

$$z_{t-1} = \sqrt{\frac{\alpha_{t-1}}{\alpha_t}} (z_t - \sqrt{1-\alpha_t} \epsilon_{\theta}(z_t)) + \sqrt{1-\alpha_{t-1}} \epsilon_{\theta}(z_t) \tag{1}$$

现有扩散噪声优化（DNO）方法直接对随机高斯噪声 $z$ 执行梯度优化 $\min_z F(G(z, \mathcal{C}))$，但在高度约束场景下，随机初始化缺乏满足困难约束所需的结构化运动技能，导致优化陷入局部极小。

### 3.2 关系任务解析（Relational Task Parsing）

关系任务解析是 RG-DNO 的第一个核心模块，其目标是将原始约束集 $C$ 智能分解为可分别处理的子集：

$$C = C_1 \oplus C_2, \quad C_R \subseteq C_2 \tag{4}$$

其中：
- **$C_R$**：检索目标约束集，包含任务中最困难的约束子集，用于指导从外部数据集中检索相关运动技能。
- **$C_1$**：可由随机噪声 $z_1$ 处理的一般约束子集。
- **$C_2$**：需要借助检索噪声 $z_2$ 处理的约束子集（$C_R$ 为其子集）。

解析过程基于约束的困难程度排序和相互依赖关系进行。对于“通过极低障碍物”任务，关系解析会识别出“身体高度约束”为困难约束 $C_R$，而“行走方向”“步态自然度”等约束则分配到 $C_1$ 或 $C_2$。解析可通过人工规则或 LLM 推理完成。

### 3.3 基于约束的检索（Constraint-based Retrieval）

该模块从现有大规模运动数据集 $\mathcal{D}$ 中检索满足 $C_R$ 的运动样本。检索目标为：

$$x = \arg\min_{x \in \mathcal{D}} F_{C_R}(x) \tag{5}$$

为进一步降低约束误差，引入水平面刚性变换 $\mathcal{H}$（旋转+平移）进行空间对齐：

$$x, \mathcal{H} = \arg\min_{x, \mathcal{H}} F_{C_R}(\mathcal{H} x) \tag{6}$$

检索到的样本 $x_R$ 经过时序调整和语义一致性检查后，通过扩散反演得到检索噪声：

$$z_R = G^{-1}(\mathcal{H} x_R, C_0) \tag{7}$$

其中 $G^{-1}$ 表示将运动序列映射回扩散初始噪声空间的反演过程。

### 3.4 蒙版噪声优化（Masked Noise Optimization）

这是 RG-DNO 的核心创新模块，通过蒙版机制智能组合随机噪声和检索噪声。具体分三步执行：

**第一步：分路优化。** 分别优化随机噪声 $z_1$（针对 $C_1$）和检索噪声 $z_2$（针对 $C_2$）：
- $z_1$ 从标准高斯噪声初始化，优化目标为 $\min_{z_1} F_{C_1}(G(z_1, C_0))$
- $z_2$ 从检索噪声 $z_R$ 初始化，优化目标为 $\min_{z_2} F_{C_2}(G(z_2, C_0))$

**第二步：蒙版组合。** 通过线性蒙版 $M$（取值在 $[0,1]$ 之间的矩阵）组合两个噪声：

$$z' = M z_1 + (1 - M) z_2 \tag{10}$$

蒙版 $M$ 的优化目标同时考虑约束满足和运动质量：

$$\min_M F_C(G(z')) + \mathcal{R}(G(z')) \tag{11}$$

其中 $\mathcal{R}$ 为运动质量奖励函数（见 3.5 节）。

**第三步：最终微调。** 以组合噪声 $z'$ 作为更优初始化，执行最后一轮标准约束优化：

$$\min_{\delta z} F_C(G(z' + \delta z)) \tag{12}$$

### 3.5 奖励引导的蒙版选择（Reward-Guided Mask Selection）

为降低蒙版 $M$ 的优化难度，RG-DNO 采用启发式候选蒙版集合 $\mathcal{M}$（时间切分或空间切分），从中选择最优者：

$$M = \arg\min_{M \in \mathcal{M}} F_C(G(z')) + \mathcal{R}(G(z')) \tag{13}$$

运动质量奖励函数 $\mathcal{R}$ 由四项组成：

$$\mathcal{R}(G(z'), z') = \lambda_1 \mathcal{L}_{\mathrm{jitter}} + \lambda_2 \mathcal{L}_{\mathrm{footskate}} + \lambda_3 \mathcal{L}_{\mathrm{decorr}} + \lambda_4 \mathcal{L}_{\mathrm{semantic}} \tag{14}$$

其中：
- $\mathcal{L}_{\mathrm{jitter}}$：关节抖动惩罚，约束相邻帧关节加速度的突变。
- $\mathcal{L}_{\mathrm{footskate}}$：脚滑动惩罚，检测足部接地时的滑动距离。
- $\mathcal{L}_{\mathrm{decorr}}$：噪声去相关损失，防止组合噪声 $z'$ 偏离扩散模型的高概率区域。
- $\mathcal{L}_{\mathrm{semantic}}$：语义对齐损失，确保生成运动与文本条件 $C_0$ 的一致性。

所有权重 $\lambda_k$ 默认设为 1.0，可根据具体任务手动调整。蒙版选择过程计算开销小，因为各候选蒙版的约束误差和奖励计算可并行执行。

### 3.6 模块间因果机制

RG-DNO 各模块形成级联因果链：**关系任务解析**识别瓶颈约束 $C_R$ → **约束检索**从外部知识库获取相关运动技能并反演为 $z_R$ → **蒙版优化**将检索先验与随机探索能力智能融合为 $z'$ → **最终微调**在优质初始化基础上精调。这一设计将高度约束任务分解为可解的子问题，突破了纯随机优化在困难约束下的能力边界。消融实验（Table 4）证实：跳过关系解析直接对全任务检索、用固定权重 $M=0.5$ 替代蒙版优化、或移除奖励函数 $\mathcal{R}$，均会导致约束误差上升或运动质量显著下降。

### 补充图表

![[assets/figures/papers/paper_list_l11_https_openaccess_thecvf_com_content_CVPR2026_html_Liu_Towards_Highly_Con/figures/001_Figure.jpg]]
*Figure: Ours (Retrieval-Guided Diffusion Noise Optimization)*

![[assets/figures/papers/paper_list_l11_https_openaccess_thecvf_com_content_CVPR2026_html_Liu_Towards_Highly_Con/figures/008_Figure.jpg]]
*Figure: (a) ProgMoGen+DNO (b) Retrieval only (c) with Mask Optim*

![[assets/figures/papers/paper_list_l11_https_openaccess_thecvf_com_content_CVPR2026_html_Liu_Towards_Highly_Con/figures/009_Figure_4.jpg]]
*Figure 4: Qualitative comparison. (a) ProgMoGen+DNO produces unsatisfactory motion for difficult constraints. For Task-2: (b) Using retrieved noise only produces implausible motion when fitting the entire task. (c) We generate plausible motion by combining retrieved noise and random noise with mask optimization*

## 实验与分析

### 主实验结果

RG-DNO 在涉及挑战性时空约束和精确数值控制的高度约束任务上，相较于现有训练无关的扩散噪声优化方法取得了显著提升。

**挑战性时空约束任务**（Task-1 极窄间隙通过、Task-2 极低障碍跨越）：如 Table 1 所示，RG-DNO 将约束误差（C.Error）分别降至 **0.0050** 和 **0.000049**，显著低于 **ProgMoGen+DNO**（Karunratanakul et al., CVPR 2024）基线。同时，关节抖动（Jitter）大幅降低，脚滑动（Foot Skate）保持在相当水平，表明运动自然度未因约束满足而牺牲。需注意，Table 1 中 ProgMoGen+DNO 采用 N_S=5 的随机噪声搜索设置。

**精确数值控制任务**（Task-3 指定步数与距离）：如 Table 2 所示，RG-DNO 将约束误差降至 **0.0003**，成功率（Succ. Rate）达到 **0.594**，明显优于 ProgMoGen+DNO 基线。这验证了检索引导的噪声初始化在处理精确数值约束时的有效性——检索到的运动技能为扩散模型提供了更接近目标步态模式的初始噪声，使后续优化能快速收敛到满足精确步数要求的解。

**基于关节的场景交互任务**（Task HSI-2）：如 Table 3 所示，RG-DNO 的约束误差降至 **0.000**，低于 **MaskControl**（Pinyoanuntapong et al., ICCV 2025）等基线。需注意公平性：MaskControl 使用 MoMask 作为基模型，而本文方法基于 MDM，模型容量存在差异。

**任务难度分析**（Figure 5）：在不同障碍高度和不同步数要求下，RG-DNO 的性能衰减明显缓于 DNO。当障碍高度极低或步数要求极端时，DNO 的约束误差急剧上升，而 RG-DNO 通过检索相关技能保持了相对稳定的表现，证明其方法在困难边界下的鲁棒性。

**LLM 文本引导的增益**（Table 5）：在 Task-2 中引入 LLM 文本引导后，RG-DNO 的约束误差进一步降至 **0.000027**，表明语言模型提供的语义先验能与检索机制形成互补，提升约束满足精度。

### 消融实验

Table 4 系统消融了 RG-DNO 各核心组件在 Task-2 上的贡献，红色背景表示该方法在该指标上失败。

![[assets/figures/papers/paper_list_l11_https_openaccess_thecvf_com_content_CVPR2026_html_Liu_Towards_Highly_Con/figures/007_Table_4.jpg]]
*Table 4: Ablation study of the proposed method on Task-2. The red background indicates that the method fails in this metric*

**关系任务解析的必要性**：仅对整个任务进行检索（不做关系任务解析，即不识别困难约束子集 C_R）效果不佳。原因是全任务检索无法精准定位所需运动技能，检索到的样本可能仅满足简单约束，对困难约束的指导作用有限。这证明了识别并仅检索困难约束子集的必要性。

**蒙版优化的关键作用**：直接使用简单线性权重组合（如 M=0.5）替代蒙版优化，导致局部运动质量显著下降，产生过度平滑现象。原因在于，随机噪声和检索噪声各自优化的运动片段在时空交界处缺乏一致性，简单加权平均无法保证过渡自然。蒙版优化通过约束误差和奖励函数的联合监督，能自动筛选出合理的时空切分方案。

**奖励函数的过滤作用**：移除奖励函数 R 后，蒙版优化难以滤除不合理的时空组合。具体而言，缺少抖动惩罚、脚滑动惩罚和噪声去相关损失后，优化过程可能选择看似满足约束但运动质量低劣的蒙版，导致整体运动质量指标变差。

**仅用检索噪声的局限**：仅使用检索噪声（不结合随机噪声）拟合完整任务时，局部脚滑动（Local FS）高达 **0.180**，产生不符合物理的姿势。这表明检索噪声虽包含有用技能，但缺乏适应完整约束集的灵活性；随机噪声的引入为模型保留了探索空间，使最终运动在满足约束的同时保持物理合理性。

### 失败模式与局限

尽管 RG-DNO 在高度约束任务上表现优异，仍存在以下失败模式：

1. **检索覆盖不足**：当任务约束极为罕见（如非人类的极端运动模式）时，现有运动数据集中无法找到合适的参考样本，检索机制失效，方法退化为标准 DNO。该点需在极端约束场景下手动验证。

2. **任务解析鲁棒性**：关系任务解析依赖人工规则或 LLM 推理。当约束间的依赖关系复杂且隐含时，解析可能错误地将困难约束分配到随机噪声处理子集 C1，导致该阶段优化无法收敛，最终影响整体性能。

3. **计算开销**：相比标准 DNO，RG-DNO 因额外增加检索、反演和蒙版优化步骤，单次生成耗时约增加 300 个优化步，实时性不足。奖励函数权重（λ_k）默认设为 1.0，需针对不同任务手动调整以达到最优平衡，自动化调参仍是开放问题。

### 补充图表

![[assets/figures/papers/paper_list_l11_https_openaccess_thecvf_com_content_CVPR2026_html_Liu_Towards_Highly_Con/figures/003_Table_1.jpg]]
*Table 1: Quantitative comparison on the highly-constrained motion generation tasks involving challenging spatiotemporal constraints*

![[assets/figures/papers/paper_list_l11_https_openaccess_thecvf_com_content_CVPR2026_html_Liu_Towards_Highly_Con/figures/004_Table_2.jpg]]
*Table 2: Quantitative comparison on the highly-constrained motion generation task involving challenging numerical constraints*

![[assets/figures/papers/paper_list_l11_https_openaccess_thecvf_com_content_CVPR2026_html_Liu_Towards_Highly_Con/figures/005_Table_3.jpg]]
*Table 3: Quantitative comparison on Task HSI-2 with joint-based constraints. MaskControl uses MoMask as its base model*

![[assets/figures/papers/paper_list_l11_https_openaccess_thecvf_com_content_CVPR2026_html_Liu_Towards_Highly_Con/figures/010_Figure_5.jpg]]
*Figure 5: Performance on different levels of task difficulty. (a) Different heights of the overhead barrier. (b) Different numbers of steps for the same walking distance*

![[assets/figures/papers/paper_list_l11_https_openaccess_thecvf_com_content_CVPR2026_html_Liu_Towards_Highly_Con/figures/006_Figure_3.jpg]]
*Figure 3: Qualitative examples for various highly-constrained generation tasks. The relational task parsing results are obtained via LLM. Details of each constraint function are provided in the supplementary material*

![[assets/figures/papers/paper_list_l11_https_openaccess_thecvf_com_content_CVPR2026_html_Liu_Towards_Highly_Con/figures/011_Table_5.jpg]]
*Table 5: Performance on incorporating with text guidance via large language models for Task-2 very low barrier. Our method can further improve performance with the help of text guidance*

## 方法谱系与知识库定位

### 1. 方法谱系：从扩散噪声优化到检索增强生成

本文提出的 **RG-DNO** 位于**训练无关的扩散模型可控生成**与**基于检索的运动合成**两条技术路线的交汇点。其直接技术前驱是两类方法：

- **扩散噪声优化 (DNO)**：以 **DNO** (Karunratanakul et al., CVPR 2024) 为代表，核心思想是将扩散模型的初始噪声 $z$ 视为可优化变量，通过最小化约束函数 $\min_z F(G(z, \mathcal{C}))$ 实现训练无关的运动编辑与细化。该方法引入了梯度归一化和学习率衰减策略，但始终从标准高斯噪声 $\mathcal{N}(0, I)$ 出发，缺乏对困难约束的结构化先验。

- **基于运动编程的约束框架**：以 **ProgMoGen** (Liu et al., CVPR 2024) 为代表，将运动生成任务形式化为组合约束函数的优化问题，支持开集时空约束的定义与组合。ProgMoGen 本身不涉及检索，其约束求解依赖随机噪声的多轮搜索（如 $N_S = 5$ 次初始噪声采样）。

RG-DNO 在继承上述框架的基础上，引入了**外部运动数据集作为知识库**的关键创新：通过检索-反演-蒙版组合的管线，将困难约束的求解从“纯优化”转化为“检索引导的优化”，实质上是用数据驱动的运动技能先验替代了随机探索。

### 2. 与相关工作的边界与差异

#### 2.1 与基于掩模的约束控制方法的区别

**MaskControl** (Pinyoanuntapong et al., ICCV 2025) 同样处理时空约束下的运动生成，但其核心机制是在扩散去噪过程中对特定关节或时间步施加掩模控制，且基于 **MoMask** 作为基模型。RG-DNO 与之有本质区别：

| 维度 | MaskControl | RG-DNO |
|------|-------------|--------|
| 约束处理层面 | 去噪过程内部的特征掩模 | 初始噪声层面的检索增强 |
| 基模型 | MoMask | MDM |
| 外部数据利用 | 无 | 检索大规模运动数据集 |
| 训练需求 | 需训练掩模控制模块 | 完全训练无关 |

在 Table 3 的 HSI-2 任务对比中，RG-DNO 取得了 $0.000$ 的约束误差，但需注意两者基模型容量存在差异，直接比较需谨慎。

#### 2.2 与通用检索增强生成的关系

RG-DNO 的检索-增强范式与语言模型领域的 RAG (Retrieval-Augmented Generation) 共享相似的动机——利用外部知识弥补模型先验的不足。但 RG-DNO 面临独特的挑战：

- **连续运动空间的检索**：不同于文本的离散 token 匹配，运动检索需要在连续姿态序列空间中定义相似度，本文通过最小化约束函数 $F_{C_R}$ 实现任务驱动的检索（Eq. 5-6）。
- **噪声空间的融合**：检索到的运动不能直接拼接，需反演为扩散噪声 $z_R = G^{-1}(\mathcal{H} x_R, C_0)$（Eq. 7），再通过蒙版优化与随机噪声组合（Eq. 10），这是运动扩散模型特有的技术要求。

### 3. 适用边界

RG-DNO 的有效性建立在以下前提之上：

1. **检索库覆盖假设**：外部运动数据集需包含与目标困难约束相关的运动技能。对于极端罕见或超出数据集分布的约束（如非人形运动、超常规物理交互），检索可能失效，此时方法退化为标准 DNO。

2. **约束可分解性假设**：关系任务解析能将全约束集 $C$ 有效拆分为 $C_1 \oplus C_2$，且存在子集 $C_R \subseteq C_2$ 可通过检索解决。若约束高度纠缠无法分解，解析质量将直接影响最终性能。

3. **扩散模型反演精度**：DDIM 反演 $G^{-1}$ 的精度决定了检索运动能否在噪声空间中被准确表征。反演误差会传播至后续蒙版优化阶段。

4. **计算预算**：相比标准 DNO，RG-DNO 单次生成额外增加约 300 个优化步（检索、反演、蒙版优化），不适用于实时或低延迟场景。

### 4. 局限性与开放问题

#### 4.1 已识别的局限性

- **检索库依赖**：检索效果受限于现有运动数据集的覆盖范围和多样性。对于极端罕见的约束（如非人类运动模式），可能无法找到合适的参考样本。
- **任务解析鲁棒性**：关系任务解析仍依赖人工规则或 LLM 推理，解析质量在不同任务间可能存在波动，缺乏自动化的质量验证机制。
- **奖励权重敏感性**：运动质量奖励函数 $\mathcal{R}$ 的权重 $\lambda_k$ 默认设为 $1.0$，但针对不同任务可能需要手动调整以达到最优平衡，缺乏自适应调权策略。
- **实时性不足**：额外的检索、反演和蒙版优化步骤导致生成耗时显著增加，限制了在交互式应用中的部署。

#### 4.2 开放研究问题

1. **LLM 深层推理的利用**：当前 LLM 仅用于辅助约束解析，如何利用其深层推理能力自动设计约束分解策略，甚至生成针对性的检索查询，是提升自动化程度的关键方向。

2. **检索与优化效率的平衡**：能否通过检索缓存、近似反演或蒸馏技术降低计算开销，使检索引导的噪声优化接近实时应用需求？

3. **跨模态泛化**：检索引导的噪声优化思路能否推广到其他生成任务（如图像、视频生成）？在图像扩散模型中，检索到的图像片段能否通过类似的反演-蒙版机制注入初始噪声？

4. **与其他训练范式的结合**：RG-DNO 目前是完全训练无关的，能否与 RLHF、偏好优化等训练框架结合，利用人类反馈进一步优化蒙版选择策略和奖励函数权重？

5. **动态多阶段约束**：在约束条件动态变化的多阶段任务中，如何进行在线检索与噪声调整，使生成运动能平滑适应约束的时序变化？

## 原文 PDF

![[paperPDFs/CVPR_2026/Towards_Highly_Constrained_Human_Motion_Generation_with_Retrieval_Guided_Diffusion_Noise_Optimization.pdf]]