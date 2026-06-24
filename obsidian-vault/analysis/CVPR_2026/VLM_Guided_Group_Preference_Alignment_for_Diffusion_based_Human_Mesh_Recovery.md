---
title: VLM-Guided Group Preference Alignment for Diffusion-based Human Mesh Recovery
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/VLM_Guided_Group_Preference_Alignment_for_Diffusion_based_Human_Mesh_Recovery.pdf
project_link: null
code_link: null
aliases:
- VGGPADBH
- VGGPADBHMR
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
- topic/representation_self_supervised_transfer
core_operator: 引入基于VLM的双记忆自反思HMR评价智能体，为每组多个预测提供稳定、语义一致的群体质量评分；将群组相对优势信号注入扩散模型，通过群组偏好对齐损失引导模型生成更符合物理约束和图像一致性的网格。
primary_logic: 大型VLM已编码丰富的人体姿态语义、接触关系与空间一致性先验，通过双记忆机制（规则记忆与原型记忆）和自反思循环可在无微调下产生可靠的质量评分；将这些群体评分转化为优势信号，并设计兼容ODE采样的群组偏好损失，使扩散模型在无3D标注的情况下依然能有效学习生成更优的人体网格。
claims:
- VLM评价智能体结合双记忆和自反思，能够纠正HMR-Scorer的错误评分，输出更符合物理合理性且语义一致的质量分数。
- 群组偏好对齐在3DPW上相比ADHMR将MPJPE降低了8.2%（M=100），并通过消融实验证明优于DPO变体。
- 去除自反思模块导致评分预测性能大幅下降（SRCC从0.597降至0.534，PLCC从0.695降至0.610），验证了自我反思知识构建的有效性。
- 该方法无需3D真值标注即可在野外数据集上进行有效微调，Ours†在3DPW上达到PVE 57.7 / MPJPE 48.5。
---

# VLM-Guided Group Preference Alignment for Diffusion-based Human Mesh Recovery

> [!tip] 核心洞察
> 大型VLM已编码丰富的人体姿态语义、接触关系与空间一致性先验，通过双记忆机制（规则记忆与原型记忆）和自反思循环可在无微调下产生可靠的质量评分；将这些群体评分转化为优势信号，并设计兼容ODE采样的群组偏好损失，使扩散模型在无3D标注的情况下依然能有效学习生成更优的人体网格。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于VLM引导的群组偏好对齐的扩散式人体网格重建 |
| 英文题名 | VLM-Guided Group Preference Alignment for Diffusion-based Human Mesh Recovery |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2602.19180) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion #topic/representation_self_supervised_transfer |
| Method | VLM-Guided Group Preference Alignment for Diffusion-based HMR |
| Dataset | 3DPW, Human3.6M |

> [!tip] 效果简介
> - 3DPW 上，PVE↓ (M=200) 59.0 vs ADHMR (reported in Table 1)；MPJPE↓ (M=200) 51.0 vs ADHMR (Table 1)；PA-MPJPE↓ (M=200) 30.2 vs ADHMR (Table 1)。
> - 3DPW (Ours† w/ extra data) 上，PVE↓ / MPJPE↓ / PA-MPJPE↓ (M=200) 57.7 / 48.5 / 30.5 vs ADHMR (Table 1)。
> - Human3.6M 上，PVE↓ / MPJPE↓ / PA-MPJPE↓ (M=200) 42.4 / 34.0 / 23.2 vs ADHMR (Table 1)。

## 概述

**问题瓶颈：** 扩散式人体网格重建（HMR）的核心挑战在于从单张2D图像恢复3D人体姿态时的固有歧义。在遮挡、杂乱背景等野外场景中，现有扩散模型（如**ADHMR**，Shen et al., 2025）常生成与输入图像不一致或物理上不合理的人体网格。主流的质量评估方法——基于2D关键点重投影的**HMR-Scorer**——容易被轮廓对齐但违背人体运动学的预测误导；而pairwise DPO仅利用成对胜负关系，忽略了多个预测间的群体质量结构，无法提供稳定可靠的偏好信号。

**核心思路：** 本文提出**VLM引导的群组偏好对齐框架**，包含两个关键创新：（1）引入基于大型视觉语言模型（VLM）的**双记忆自反思HMR评价智能体**，为每组多个预测提供稳定、语义一致的群体质量评分；（2）设计**群组偏好对齐损失**，将群体相对优势信号注入扩散模型，引导其生成更符合物理约束和图像一致性的网格。该框架的核心洞察在于：大型VLM已编码丰富的人体姿态语义、接触关系与空间一致性先验，通过双记忆机制（规则记忆与原型记忆）和自反思循环，可在无需微调VLM本身的情况下产生可靠的质量评分。

**方法定位：** 本方法处于扩散式HMR与偏好对齐的交叉点。与**ADHMR**（Shen et al., 2025）的Diffusion-DPO相比，它将成对偏好扩展为群组偏好，并将不可靠的2D重投影评分器替换为语义感知的VLM评价智能体。与**ScoreHypo**（Xu et al., CVPR 2024）的外部选择机制不同，本方法通过偏好对齐直接在扩散过程中优化生成质量。更广泛地，该框架将LLM对齐中的GRPO思想适配到扩散模型的ODE采样范式下。

**主要结果：** 在3DPW基准上，本方法相比ADHMR在MPJPE上实现8.2%的提升（M=100时MPJPE为49.9 vs. 53.1）。消融实验证实：群组偏好对齐显著优于DPO变体；去除自反思模块导致评分预测的SRCC从0.597降至0.534，验证了自我反思知识构建的有效性。更重要的是，该方法**无需3D真值标注**即可在野外数据集（InstaVariety）上进行有效微调，Ours†在3DPW上达到PVE 57.7 / MPJPE 48.5的竞争性能。

## 背景与动机

### 人体网格重建的2D-3D歧义困境

从单目图像恢复三维人体网格（Human Mesh Recovery, HMR）是计算机视觉的核心任务，其根本挑战在于**2D到3D的固有歧义**：一张二维图像可能对应无限多种三维姿态和形状解释。这一歧义在野外场景中尤为突出——遮挡、杂乱背景、非典型姿态等因素使得模型极易生成与输入图像不一致或物理上不合理的人体网格。

近年来，扩散模型被引入HMR任务以建模多模态后验分布，代表性工作如**ScoreHypo**（Xu et al., CVPR 2024）和**ADHMR**（Shen et al., 2025），它们通过扩散去噪过程生成多个人体网格假设，一定程度上缓解了确定性回归方法（如**Hybrik** Li et al., CVPR 2021；**CameraHMR** Patel & Black, 3DV 2025）只能输出单一解的问题。然而，**如何从多个候选预测中筛选或偏好生成高质量网格**，仍是一个未充分解决的瓶颈。

### 现有质量评估与偏好对齐的缺陷

当前扩散式HMR方法的偏好优化主要依赖两类策略：

1. **基于2D重投影的评分器**：以ADHMR中的HMR-Scorer为代表，通过计算预测网格的2D关键点重投影误差来评估质量。这种方案存在根本性缺陷——它容易被**轮廓对齐但违背人体运动学的预测**所误导（例如，遮挡区域的重投影误差天然较小，但对应的3D姿态可能严重扭曲）。如Figure 4所示，HMR-Scorer的初始评分经常与物理合理性相悖。

2. **成对偏好优化（Pairwise DPO）**：ADHMR首次将Diffusion-DPO引入HMR，但仅利用两个预测间的胜负关系进行优化，**忽略了多个预测间的群体质量关系**。成对比较无法捕捉组内相对优势的细粒度信号，导致偏好信号不稳定且信息利用率低。

### 核心动机：VLM先验与群组偏好信号

大型视觉语言模型（VLM）已在海量数据中编码了丰富的人体姿态语义、接触关系与空间一致性先验。本文的核心洞察在于：**这些先验可以被激活为可靠的人体网格质量评估能力**，而无需针对HMR任务进行微调。

基于此，本文提出两个关键思路：

- **双记忆自反思评价智能体**：通过规则记忆（rule memory）与原型记忆（prototype memory）的协同，结合自反思循环，使VLM能够在无微调下输出稳定、语义一致的质量评分，从而纠正HMR-Scorer的系统性偏差。

- **群组偏好对齐框架**：将评价智能体对一组预测的群体评分转化为**优势信号（advantage）**，设计兼容ODE采样的群组偏好损失，引导扩散模型在无需3D真值标注的情况下，优先生成更符合物理约束和图像一致性的网格。

这一框架从根本上改变了扩散式HMR的优化范式：从依赖不可靠的2D代理信号或昂贵的人工标注，转向利用VLM的语义理解能力自动构建高质量偏好数据，实现**无3D标注的野外场景微调**。

## 核心创新

本文的核心创新在于将**大型视觉语言模型（VLM）的语义理解能力**引入扩散式人体网格重建（HMR）的偏好优化流程，通过两个关键的技术转变（changed slots）解决了现有方法的瓶颈。

**1. 从几何评分到语义感知的群组质量评估**

现有扩散式HMR方法（如**ADHMR**，Shen et al., 2025）依赖基于2D关键点重投影的评分器（HMR-Scorer）来提供偏好信号。这类评分器容易被“轮廓对齐但物理上不合理”的预测所误导，尤其在遮挡或杂乱背景下，且其成对评分方式忽略了多个预测之间的群体质量关系。

本文提出**基于VLM的双记忆自反思评价智能体**（VLM-guided HMR critique agent），直接对一组网格预测进行并发评分。其核心机制包括：
- **双记忆机制**：规则记忆存储可解释的评估规则，原型记忆存储典型评分案例，二者协同保证评分的稳定性与语义一致性。
- **自反思循环**：当评分与真值指标出现偏差时，VLM自动检查差异并挖掘新的评估规则，无需微调即可持续提升评分可靠性。

这一转变使得质量信号从“低层次的几何对齐”升级为“语义层面的物理合理性与图像一致性判断”。

**2. 从成对偏好到群组优势对齐**

现有方法采用Diffusion-DPO，仅利用预测之间的胜负关系进行成对优化，忽略了群体内的相对优势幅度。

本文设计**群组偏好对齐损失**（group preference alignment loss），将评价智能体给出的群组分数转化为归一化的优势值：

$$A_{i} = \frac{s_{i} - \operatorname{mean}(\{s_{i}\}_{i=1}^{G})}{\operatorname{std}(\{s_{i}\}_{i=1}^{G})}$$

利用该优势加权，引导扩散模型在去噪过程中偏好生成高分网格。该损失兼容ODE采样，无需轨迹级强化学习，且整个微调过程**不依赖任何3D真值标注**，仅凭VLM自动生成的偏好分数即可在野外数据上完成对齐训练。

**关键证据支撑**：
- 消融实验表明，群组偏好对齐在3DPW上相比使用相同评价智能体的DPO变体，MPJPE从53.1降至49.9（6.0%相对提升），验证了群组优势信号优于成对胜负信号。
- 去除自反思模块后，群组评分预测的SRCC从0.597降至0.534，PLCC从0.695降至0.610，证实了自反思知识构建对评价质量的关键作用。

## 整体框架

本文提出 **VLM引导的群组偏好对齐框架**，用于在无3D真值标注的条件下微调扩散式人体网格重建（HMR）模型。如图2所示，整个pipeline由四个核心模块串联构成：基础扩散HMR模型、VLM评价智能体、HMR群组偏好数据集构建、以及群组偏好对齐微调。

### 问题瓶颈与设计动机

扩散式HMR方法面临2D到3D的固有歧义——在遮挡、杂乱背景等野外场景中，模型常生成与输入图像不一致或物理上不合理的人体网格。现有的质量评估方式（如ADHMR使用的HMR-Scorer，基于2D关键点重投影）容易被轮廓对齐但违背人体运动学的预测误导，且pairwise DPO仅利用成对胜负关系，忽略了多个预测间的群体质量结构，无法提供稳定可靠的偏好信号。

### 核心调节杠杆

本框架的关键创新在于将**大型VLM的语义先验**注入偏好信号链路：VLM已编码丰富的人体姿态语义、接触关系与空间一致性先验，通过双记忆机制（规则记忆与原型记忆）和自反思循环，可在无微调下产生可靠的质量评分；进而将这些群体评分转化为优势信号，设计兼容ODE采样的群组偏好损失，使扩散模型在无3D标注的情况下依然能有效学习生成更优的人体网格。

### 模块关系与数据流

1. **基础扩散HMR模型（ε_ref）**：以预训练的扩散去噪模型为起点，以图像特征 $c$ 为条件，通过反向扩散过程生成多个人体网格假设。该模型作为参考策略，后续微调时保持冻结。

2. **VLM评价智能体**：双记忆增强的语义评分器。对每组 $G=20$ 个网格预测进行同步评估，输出一致的质量分数 $\{s^1,\dots,s^G\}$ 及评语。其内部包含：
   - **规则记忆**：存储从校准数据中挖掘的可测试评估规则，通过混合语义相关性与UCB探索项选择最有效的规则组合；
   - **原型记忆**：存储典型评分案例作为上下文参考；
   - **自反思循环**：通过比较评分排序与GT指标的Spearman秩相关系数，更新现有规则权重，并挖掘新规则。

3. **HMR群组偏好数据集（GHMR）**：利用评价智能体对大量无标注图像的网格预测组进行批量评分，构建包含（图像，网格组，分数组）的偏好数据集，无需人工标注。

4. **群组偏好对齐微调（ε_θ）**：基于GHMR数据，将评分转化为群内相对优势 $A_i = \frac{s_i - \mathrm{mean}(\{s_i\})}{\mathrm{std}(\{s_i\})}$，通过优势加权的群组偏好损失优化扩散模型，使其偏好生成高分网格。最终训练目标为：

$$\mathcal{L}(\boldsymbol{\theta}) = \mathbb{E}_{\mathbf{m}\sim\mathcal{G}_{\mathrm{HMR}}, t\sim\mathcal{U}(1,T), \boldsymbol{\epsilon}\sim\mathcal{N}(0,\mathbf{I})} \beta T \lambda_t \sum_{i=1}^{G} \Big[ A(\mathbf{m}^i) \big( L_{\mathrm{DM}}^{\theta}(\mathbf{x}_t^i, \boldsymbol{\epsilon}) - L_{\mathrm{DM}}^{\mathrm{ref}}(\mathbf{x}_t^i, \boldsymbol{\epsilon}) \big) \Big]$$

该损失鼓励高分样本的去噪损失低于参考模型，从而实现偏好引导的生成优化。超参数 $\beta$ 控制正则化强度。

### 关键设计优势

- **群组同步评分**：相比成对比较，群组评分捕获了预测间的相对质量结构，提供更丰富的偏好信号。
- **语义一致性**：VLM评价智能体通过双记忆和自反思，能够纠正HMR-Scorer的错误评分（如Figure 4所示），输出更符合物理合理性且语义一致的质量分数。
- **无3D标注微调**：整个对齐流程仅需偏好信号，可在野外数据（如InstaVariety）上进行有效微调，Ours†在3DPW上达到PVE 57.7 / MPJPE 48.5。

> **注意**：评价智能体的探索阶段需要一定量带有3D真值的校准数据用于规则更新和自反思，全新场景可能需要额外的探索成本。群组偏好对齐为离线方案，尚不支持在线策略提升。

### 补充图表

![[assets/figures/papers/paper_list_l956_https_arxiv_org_abs_2602_19180/figures/001_Figure_1.jpg]]
*Figure 1: We introduce a VLM-guided HMR critique agent equipped with a dual-memory mechanism that delivers stable and semantically grounded assessments for groups of estimated 3D meshes. Building on these group-wise signals, our group preference alignment framework steers diffusion-based HMR models towards more coherent and reliable mesh generation*

![[assets/figures/papers/paper_list_l956_https_arxiv_org_abs_2602_19180/figures/002_Figure_2.jpg]]
*Figure 2: Overview of our framework. Our purpose is to refine a diffusion-based HMR model that generates a group of human mesh predictions per input image. We propose a VLM-enhanced HMR critique agent that assigns a score for each human mesh prediction. This critique agent is equipped with a dual-memory mechanism to give stable assessments. Then, we use this critique agent to build a group-wise HMR preference dataset without the need for manual labeling. Finally, we employ this preference dataset to finetune the base model to preferentially generate predictions that are physically plausible and better aligned with the image cues*

## 核心模块与公式推导

### 问题形式化与扩散基础

本方法将人体网格重建建模为条件反向扩散过程。给定输入图像特征 $c$，扩散模型 $\epsilon_\theta$ 从纯噪声 $\mathbf{x}_T \sim \mathcal{N}(0, \mathbf{I})$ 逐步去噪，生成人体网格参数 $\mathbf{x}_0$（包含SMPL姿态、体型和相机参数）。反向过程每一步为：

$$p_{\theta}(\mathbf{x}_{t-1} \vert \mathbf{x}_{t}) = \mathcal{N}\big(\mathbf{x}_{t-1}; \mu_{\theta}(\mathbf{x}_{t}, t), \sigma_{t}^{2} \mathbf{I}\big)$$

基础扩散模型的训练目标是最小化噪声预测误差：

$$L_{\mathrm{DM}} = \mathbb{E}_{t, \mathbf{x}_{0}, \epsilon}\left[\lambda_{t} \left\| \epsilon - \epsilon_{\theta}(\mathbf{x}_{t}, t) \right\|_{2}^{2} \right]$$

其中 $\epsilon$ 为真实噪声，$\epsilon_{\theta}$ 为模型预测噪声，$\lambda_t$ 为时间步权重。

### 核心模块一：VLM评价智能体

评价智能体 $\mathcal{C}_{\mathrm{VLM}}$ 接收输入图像 $I$ 和一组 $G$ 个网格预测 $\{\mathbf{m}^1, \dots, \mathbf{m}^G\}$，同步输出质量分数：

$$\{s^{1}, \dotsc, s^{G}\} = \mathcal{C}_{\mathrm{VLM}}(I, \mathbf{m}^{1}, \dotsc, \mathbf{m}^{G})$$

智能体的核心创新在于**双记忆机制**与**自反思循环**：

**规则记忆（Rule Memory）** 存储可解释的评估规则，每条规则 $T_i$ 包含语义条件与评分逻辑。**原型记忆（Prototype Memory）** 缓存历史评估案例（图像-网格-分数三元组），用于检索相似场景的参考。

在每次评估中，智能体通过混合选择分数从规则记忆中检索最相关的规则：

$$\Psi_{i} = \mathrm{R}(T_{q}, T_{i}) + \mathrm{U}_{i}$$

其中 $\mathrm{R}(\cdot)$ 衡量查询与规则的语义相关性，$\mathrm{U}_{i}$ 为上置信界（UCB）探索项：

$$\mathrm{U}_{i} = \rho_{i} + C\sqrt{\frac{\log N_{\mathrm{total}}}{N_{i}^{u} + 1}}$$

$\rho_i$ 为规则的历史成功率，$N_i^u$ 为规则使用次数，$N_{\mathrm{total}}$ 为总评估次数，$C$ 平衡利用与探索。该机制确保高频有效规则被优先选用，同时低频规则获得尝试机会。

**自反思循环**是智能体的学习核心：当评分排序与真值指标（如MPJPE）的Spearman相关系数低于阈值 $\tau$ 时，智能体指示VLM分析输出与真值的差异，自动挖掘1-2条新规则加入记忆。这一闭环使智能体在无需微调VLM的前提下持续提升评分质量。

### 核心模块二：群组偏好数据集构建

利用评价智能体对基础扩散模型 $\epsilon_{\mathrm{ref}}$ 生成的预测组进行批量评分，构建群组偏好数据集 $\mathcal{G}_{\mathrm{HMR}}$。每组包含 $G=20$ 个预测，每个样本形式为 $(I, \{\mathbf{m}^i\}_{i=1}^G, \{s^i\}_{i=1}^G)$。该过程无需人工标注或3D真值，可直接应用于野外图像。

### 核心模块三：群组偏好对齐损失

群组偏好对齐的核心思想是引导扩散模型 $\epsilon_\theta$ 偏好生成评价分数更高的网格。首先将组内分数转化为相对优势：

$$A_{i} = \frac{s_{i} - \operatorname{mean}(\{s_{i}\}_{i=1}^{G})}{\mathrm{std}(\{s_{i}\}_{i=1}^{G})}$$

优势 $A_i$ 为正表示该预测优于组内平均水平，为负则反之。该归一化消除了VLM评分的绝对尺度偏差，仅保留组内相对质量信号。

对齐损失采用优势加权的负对数似然比形式：

$$\mathcal{L}(\theta) = -\mathbb{E}_{c, \{\mathbf{m}^{i}\}}\left[\sum_{i=1}^{G} A(\mathbf{m}^{i}) \log \frac{p_{\theta}(\mathbf{m}^{i} \mid c)}{p_{\mathrm{ref}}(\mathbf{m}^{i} \mid c)}\right]$$

其中 $p_{\theta}$ 和 $p_{\mathrm{ref}}$ 分别为当前模型和参考模型的似然。该损失使高分预测的似然比增大，低分预测的似然比减小。

### 最终训练目标

将上述损失展开为可微分的去噪损失差异形式，得到最终训练目标：

$$\mathcal{L}(\boldsymbol{\theta}) = \mathbb{E}_{\mathbf{m} \sim \mathcal{G}_{\mathrm{HMR}}, t \sim \mathcal{U}(1, T), \boldsymbol{\epsilon} \sim \mathcal{N}(0, \mathbf{I})} \beta T \lambda_{t} \sum_{i=1}^{G}\Big[A(\mathbf{m}^{i})\left(L_{\mathrm{DM}}^{\theta}(\mathbf{x}_{t}^{i}, \boldsymbol{\epsilon}) - L_{\mathrm{DM}}^{\mathrm{ref}}(\mathbf{x}_{t}^{i}, \boldsymbol{\epsilon})\right)\Big]$$

其中 $\beta$ 控制正则化强度，$L_{\mathrm{DM}}^{\theta}$ 和 $L_{\mathrm{DM}}^{\mathrm{ref}}$ 分别为当前模型和参考模型对样本 $\mathbf{m}^i$ 的去噪损失。该目标直接兼容扩散模型的ODE采样器，无需轨迹级强化学习。训练时，高分样本的去噪损失被压低，低分样本的去噪损失被抬高，从而将模型生成分布推向高质量区域。

### 与GRPO的形式联系

本损失可视为群组相对策略优化（Group Relative Policy Optimization, GRPO）在扩散模型上的实例化。GRPO的目标函数为：

$$\operatorname*{max}_{\theta}\ \mathbb{E}_{c, \{\mathbf{x}_{0}^{i}\}}\left[\sum_{i=1}^{G} \frac{p_{\theta}(\mathbf{x}_{0}^{i} | c)}{p_{\mathrm{ref}}(\mathbf{x}_{0}^{i} | c)} A(\mathbf{x}_{0}^{i})\right]$$

其中优势计算为：

$$A_{i} = \frac{r_{i} - \operatorname{mean}(\{r_{1}, r_{2}, \ldots, r_{G}\})}{\operatorname{std}(\{r_{1}, r_{2}, \ldots, r_{G}\})}$$

本方法以VLM评价分数替代外部奖励 $r_i$，并将似然比优化转化为去噪损失差异最小化，实现了无需3D标注的扩散模型偏好对齐。

## 实验与分析

### 核心性能验证

我们在两个标准基准上对方法进行了全面评估：**3DPW**（野外视频）和 **Human3.6M**（室内受控环境）。Table 1 展示了与当前主流方法的定量对比。

![[assets/figures/papers/paper_list_l956_https_arxiv_org_abs_2602_19180/figures/003_Table_1.jpg]]
*Table 1: Comparison with state-of-the-arts on the 3DPW [55] and Human3.6M [22] dataset. M is the number of predictions of probabilistic methods. Ours† is trained on an additional in-the-wild dataset InstaVariety [25], using only preference signals without 3D labels*

在 3DPW 数据集上，本方法（M=200）取得了 **PVE 59.0 / MPJPE 51.0 / PA-MPJPE 30.2** 的成绩，在所有概率式方法中表现最优。相较于基于扩散的基线 **ADHMR**（Shen et al., 2025），本方法在 MPJPE 上实现了 **8.2% 的相对提升**（M=100 条件下）。在 Human3.6M 上，本方法同样保持领先，达到 PVE 42.4 / MPJPE 34.0 / PA-MPJPE 23.2。

值得注意的是，**Ours†** 变体在额外使用野外数据集 InstaVariety 进行微调时，**完全不需要 3D 真值标注**，仅依赖 VLM 评价智能体自动生成的群组偏好信号。该变体在 3DPW 上进一步将 MPJPE 降至 **48.5**，PVE 降至 **57.7**，验证了框架在无监督野外适应场景下的有效性。

### 消融实验：群组偏好对齐的必要性

Table 2 在 3DPW 测试集上系统消融了各训练策略的贡献（所有模型均在 InstaVariety 上微调，M=100）：

![[assets/figures/papers/paper_list_l956_https_arxiv_org_abs_2602_19180/figures/007_Table_2.jpg]]
*Table 2: Ablation study on the 3DPW [55] test set. All models are finetuned on the InstaVariety [25] dataset. M = 100 for all*

- **Base model**（仅使用预训练扩散模型，不做任何微调）性能最差，验证了域适应的必要性。
- **Supervised finetuning**（标准监督微调）虽有一定提升，但仍弱于偏好对齐方案，说明在野外数据缺乏 3D 真值时，监督信号本身不足以引导模型生成物理合理的结果。
- **DPO w/ critique agent**（使用 VLM 评价智能体替代 HMR-Scorer 的成对偏好优化）将 MPJPE 降至 53.1，已优于 ADHMR 原版，但**仍显著弱于本方法的 49.9**（MPJPE 差距 3.2mm，约 6.0%）。这直接证明了群组偏好对齐损失优于成对 DPO——群组优势信号能更充分地利用多个预测间的相对质量关系，提供更稳定的优化方向。

### 评价智能体的组件消融

Table 3 和 Table 4 从评分预测的角度验证了 VLM 评价智能体各模块的有效性。在 GTA-Human II 数据集上，完整的评价智能体取得了 **SRCC 0.597 / KRCC 0.432** 的群组评分相关性，以及 **PLCC 0.695** 的点向评分相关性。

![[assets/figures/papers/paper_list_l956_https_arxiv_org_abs_2602_19180/figures/008_Table_3.jpg]]
*Table 3: Group-wise score prediction results. We report the SRCC and KRCC between the predicted scores and the ground-truth HMR metrics. Our method consistently outperforms all baselines and ablation variants*

![[assets/figures/papers/paper_list_l956_https_arxiv_org_abs_2602_19180/figures/009_Table_4.jpg]]
*Table 4: Point-wise score prediction results. We report the PLCC between the predicted scores and the ground-truth metrics*

关键消融发现：

- **去除自反思模块**（w/o self-reflection）导致性能全面崩塌：SRCC 从 0.597 降至 0.534，PLCC 从 0.695 降至 0.610，KRCC 也大幅下降。这验证了自反思循环在知识构建中的核心作用——通过反思挖掘新规则并更新现有规则，智能体能够持续提升评分质量。
- **去除规则记忆或原型记忆**均导致评分相关性下降，证明双记忆机制（规则记忆提供可解释的评估准则，原型记忆提供历史案例参照）对评分稳定性至关重要。
- **UCB 规则选择策略**的消融同样显示性能退化，验证了平衡探索与利用在选择评估规则时的必要性。

### 定性分析

Figure 3 展示了本方法与 ADHMR 在 3DPW 和互联网图像上的定性对比。在遮挡、杂乱背景和复杂姿态场景下，ADHMR 常生成与图像不一致或物理上不合理的网格（如肢体穿透、姿态扭曲），而本方法生成的网格在轮廓对齐和物理合理性上均有明显改善。

![[assets/figures/papers/paper_list_l956_https_arxiv_org_abs_2602_19180/figures/004_Figure_3.jpg]]
*Figure 3: Qualitative comparison between our method and the state-of-the-art probabilistic model ADHMR [50]. Examples (a) ∼ (e) are from the 3DPW [55] dataset, while (f) ∼ (h) are challenging internet images. Both overlay and side-view results are shown*

Figure 4 直观展示了 VLM 评价智能体的纠错能力：HMR-Scorer 基于 2D 重投影给出了误导性的高分，而评价智能体通过语义推理识别出网格与图像的不一致性，给出了更符合物理合理性的修正评分及详细评语。

### 失败模式与局限性

尽管整体性能优异，方法仍存在以下已知局限：

1. **VLM 计算开销**：使用 Qwen3-VL-32B 作为评价智能体，训练和推理过程中的 VLM 调用增加了显著的计算成本，可能限制在资源受限环境下的部署。
2. **离线偏好对齐的局限**：群组偏好对齐为离线方案，不支持在线探索或迭代式自我改进。在全新场景下，评价智能体的探索阶段需要一定量带有 3D 真值的校准数据用于规则更新和自反思。
3. **极端场景的误判风险**：偏好分数的质量完全由 VLM 决定，在极端遮挡或非典型人体姿态下，VLM 的内部偏差可能导致评分失准。
4. **架构依赖性**：方法基于特定的扩散 HMR 架构（ScoreHypo/ADHMR）和 VLM（Qwen3-VL-32B），对其他基座模型的泛化性尚未验证。

## 方法谱系与知识库定位

### 问题定位：扩散式HMR的评估困境与偏好优化瓶颈

人体网格重建（HMR）本质上是一个从2D图像恢复3D人体姿态与形状的歧义问题。扩散模型通过生成多样化的假设来应对这一歧义，但其输出质量高度依赖于可靠的评估信号。现有方法在此处面临双重困境：

**评估信号不可靠。** 以 **ADHMR**（Shen et al., 2025）为代表的扩散式HMR方法，采用基于2D关键点重投影的HMR-Scorer进行质量评分。然而，这类评分器容易被轮廓对齐但违背人体运动学的预测误导——在遮挡或杂乱背景下，一个“看起来投影正确”的网格可能在3D空间中存在穿模、关节反向等严重错误。VLM评价智能体的核心突破在于：大型视觉语言模型（如Qwen3-VL-32B）已编码丰富的人体姿态语义、接触关系与空间一致性先验，通过双记忆机制（规则记忆与原型记忆）和自反思循环，可在无微调下产生语义一致且物理合理的质量评分。

**偏好信号利用不充分。** **ADHMR**采用的Diffusion-DPO（成对偏好优化）仅利用两个预测间的胜负关系，忽略了群组内多个预测间的相对优势结构。本方法将群组相对优势信号注入扩散模型，设计兼容ODE采样的群组偏好对齐损失，使模型能够从群体质量关系中学习更精细的偏好梯度。

### 与现有方法的关系图谱

#### 确定性HMR：从回归到解析

**Hybrik**（Li et al., CVPR 2021）通过混合解析-神经网络逆运动学求解姿态，代表了确定性回归路线的早期探索。**CameraHMR**（Patel & Black, 3DV 2025）则直接回归SMPL参数，是当前确定性方法的前沿。这些方法输出单一预测，无法建模2D到3D的固有歧义，在遮挡场景中尤其脆弱。本方法继承了扩散式生成框架的多假设优势，同时通过群组偏好对齐有效筛选高质量预测。

#### 概率HMR：从采样到偏好引导

**ProHMR**（Kolotouros et al., ICCV 2021）建模后验分布以生成多种假设，是概率HMR的开创性工作。**ScoreHypo**（Xu et al., CVPR 2024）将扩散模型引入HMR，通过外部选择网络筛选最佳假设。**ADHMR**在此基础上引入Diffusion-DPO，首次尝试用偏好优化替代外部选择。本方法在ADHMR的扩散-DPO框架上做出两项关键改进：（1）用VLM评价智能体替代HMR-Scorer，解决评分信号的语义盲区；（2）用群组偏好对齐替代成对DPO，更充分地利用群体质量结构。

#### 偏好优化：从成对到群组

在RLHF/偏好对齐领域，DPO（Direct Preference Optimization）通过成对比较优化策略。本方法借鉴GRPO（Group Relative Policy Optimization）的思想，将群组内相对优势作为训练信号。消融实验（Table 2）直接验证了这一改进的有效性：在3DPW上，使用VLM评价智能体的DPO变体（DPO w/ critique agent）MPJPE为53.1，而群组偏好对齐降至49.9，相对提升6.0%。这表明即使评分器相同，群组级别的优势信号也比成对胜负关系包含更丰富的偏好信息。

### 适用边界与关键假设

**VLM能力边界。** 评价智能体的可靠性受限于底层VLM的视觉理解能力。主要实验基于Qwen3-VL-32B，在极端遮挡、非典型姿态或高度模糊场景下，VLM仍可能产生误判。偏好分数的质量直接决定了对齐效果的上限。

**探索阶段的数据依赖。** 双记忆机制中的规则更新和自反思需要一定量带有3D真值的校准数据（用于计算Spearman秩相关系数与GT指标）。在全新场景或数据分布显著偏移时，可能需要额外的探索成本来重建规则记忆。

**离线对齐的静态性。** 群组偏好对齐是离线方案，依赖固定的参考模型和预构建的偏好数据集，不支持在线探索或迭代式自我改进（如在线GRPO）。这意味着模型无法在微调过程中自适应地发现新的高质量区域。

**架构耦合度。** 方法基于特定的扩散HMR架构（ScoreHypo/ADHMR的扩散去噪框架），对确定性回归方法或其他生成范式（如GAN、VAE）的泛化性尚未验证。

### 局限与开放问题

**计算效率瓶颈。** 训练阶段每组图像需采样G=20个预测并调用VLM进行群组评分；推理阶段虽可减少采样数，但VLM调用仍增加额外开销。使用32B量级的VLM在资源受限环境下部署面临挑战。一个自然的后续方向是：通过知识蒸馏将VLM的评价能力压缩进轻量评分网络，以降低推理成本。

**VLM系列的可替代性。** 当前仅验证了Qwen3-VL-32B作为评价主干的性能。不同VLM系列（如GPT-4V、Gemini）在人体姿态理解上的偏差和一致性如何？更换VLM后，双记忆机制是否需要重新校准？这直接关系到方法的可复现性和生态兼容性。

**野外场景的鲁棒性边界。** 虽然Ours†在InstaVariety野外数据上展示了无需3D标签的微调能力（PVE 57.7 / MPJPE 48.5），但多人交互、快速运动模糊、极端光照等场景下的评价稳定性尚未充分验证。VLM在这些场景中的语义理解可能退化，导致偏好信号质量下降。

**记忆机制的长期演化。** 随着偏好数据集规模增长，规则记忆的检索效率和遗忘曲线如何？是否需要引入记忆淘汰策略来管理规则库的膨胀？原型记忆在面对新姿态分布时，其代表性是否会被稀释？

**从离线到在线的进化路径。** 群组偏好对齐框架能否扩展到在线强化学习范式（如在线GRPO）？在线探索将允许模型在微调过程中持续生成新样本、获取VLM反馈并更新策略，可能突破离线数据的覆盖限制，实现更高效的自训练循环。

## 原文 PDF

![[paperPDFs/CVPR_2026/VLM_Guided_Group_Preference_Alignment_for_Diffusion_based_Human_Mesh_Recovery.pdf]]