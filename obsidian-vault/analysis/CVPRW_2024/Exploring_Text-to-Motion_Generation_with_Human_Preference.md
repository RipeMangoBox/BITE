---
title: Exploring Text-to-Motion Generation with Human Preference
type: paper
paper_level: A
venue: CVPRW
year: 2024
pdf_ref: paperPDFs/CVPRW_2024/Exploring_Text-to-Motion_Generation_with_Human_Preference.pdf
project_link: null
code_link: "https://github.com/THU-LYJ-Lab/InstructMotion"
aliases:
- ETMGHP
tags:
- CVPRW_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 利用非专家的人类偏好标注（比较两个生成动作的优劣）作为训练信号，绕过对运动捕捉数据的依赖。
primary_logic: 在数据稀缺的条件下，直接偏好优化（DPO）避免了奖励模型过拟合，并且偏好程度高的样本贡献了大部分性能增益；LoRA 正则化是稳定训练的关键。
claims:
- 标注者显著偏好经过偏好数据训练的 MotionGPT 输出，且该趋势在不同温度下均成立。
- DPO 在 R-precision 和 MM Dist 上优于 RLHF。
- 偏好程度为 “Much better” 和 “Better” 的样本贡献了大部分性能提升。
- LoRA 在 DPO 训练中起到关键的正则化作用，显著提升各项指标。
---

# Exploring Text-to-Motion Generation with Human Preference

> [!tip] 核心洞察
> 在数据稀缺的条件下，直接偏好优化（DPO）避免了奖励模型过拟合，并且偏好程度高的样本贡献了大部分性能增益；LoRA 正则化是稳定训练的关键。

| 字段 | 内容 |
|------|------|
| 中文题名 | 探索基于人类偏好的文本到动作生成 |
| 英文题名 | Exploring Text-to-Motion Generation with Human Preference |
| 会议/期刊 | CVPRW 2024 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2024W/HuMoGen/papers/Sheng_Exploring_Text-to-Motion_Generation_with_Human_Preference_CVPRW_2024_paper.pdf) · [Code](https://github.com/THU-LYJ-Lab/InstructMotion) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | InstructMotion |
| Dataset | HumanML3D |

> [!tip] 效果简介
> - HumanML3D (测试集) 上，R-precision Top-1 ↑ 0.426 (DPO) vs 0.415 (RLHF) (+0.011)；MM Dist ↓ 3.782 (DPO) vs 3.908 (RLHF) (-0.126)。
> - 人类评估 (未见过的描述) 上，偏好胜率 vs MotionGPT DPO vs MotionGPT (DPO 在温度 1.0-2.0 下显著胜出)。

## 概要

文本到动作生成任务面临一个根本瓶颈：高质量运动捕捉数据的采集成本极高，导致训练数据稀缺，模型在文本-动作对齐上表现不足。本文提出 **InstructMotion**，核心思路是绕过对昂贵运动捕捉数据的依赖，转而利用廉价的非专家人类偏好标注——即让标注者比较两个生成动作的优劣——作为训练信号，直接优化生成模型。

在偏好学习范式的选择上，论文对比了两种路径：基于奖励模型的强化学习（RLHF）和直接偏好优化（DPO）。关键洞察在于，仅 3,528 个偏好对的数据规模下，训练独立的奖励模型极易过拟合，导致 RLHF 训练不稳定且难以调参。DPO 通过隐式地将奖励表示为策略与参考模型的对数概率比，跳过了奖励模型训练环节，在数据稀缺条件下展现出显著优势。此外，LoRA 低秩适应被证明是 DPO 成功的关键正则化组件——移除 LoRA 后，Top-1 R-precision 从 0.426 降至 0.394，MM Dist 从 3.782 升至 4.097，FID 从 0.219 升至 0.276。

主要实验结论如下：
- **DPO 优于 RLHF**：在 HumanML3D 测试集上，DPO 的 Top-1 R-precision 达到 0.426（RLHF 为 0.415），MM Dist 降至 3.782（RLHF 为 3.908）。
- **人类偏好验证**：标注者在未见过的文本描述上显著偏好 DPO 微调后的 MotionGPT 输出，该趋势在不同采样温度下均成立。
- **数据效率**：仅使用约 700 对偏好数据（总量的 20%）即可获得大部分性能增益，继续增加数据收益递减。
- **偏好强度至关重要**：偏好程度为“Much better”和“Better”的样本贡献了绝大部分性能提升，加入“Slightly better”和“Negligibly better”样本仅略微改善对齐，反而降低生成质量。

值得注意的是，论文明确指出 FID 指标不能准确衡量运动质量，人类偏好评估才是更可靠的判断标准。该方法目前仅在 MotionGPT 单一自回归骨干上验证，且标注者均为计算机科学研究生，结论的泛化性有待在更多样化的模型架构和用户群体上进一步检验。

文本到动作生成（Text-to-Motion Generation）旨在根据自然语言描述合成逼真的三维人体运动序列，在动画制作、虚拟现实和人机交互等领域具有重要应用价值。然而，该领域面临一个根本性瓶颈：**训练数据的稀缺性**。高质量的运动数据依赖昂贵、专业化的运动捕捉（MoCap）设备采集，导致可用数据量远小于图像或文本领域，进而造成文本-动作对齐不足——模型生成的动作品质参差不齐，常出现与文本语义不符或不逼真的情况。

现有文本到动作生成模型，如 **MotionGPT**（Zhang et al., arXiv 2023），采用自回归 Transformer 架构，将连续运动序列通过 VQ-VAE 离散化为运动分词（motion tokens），再基于文本提示自回归生成。这类模型通常仅在标准的文本-动作对上以交叉熵损失进行监督训练，缺乏对生成质量与语义对齐的显式优化信号。

与此同时，在大语言模型领域，**基于人类偏好的学习**（Preference Learning）已展现出强大的对齐能力。RLHF（Ouyang et al., NeurIPS 2022）通过训练奖励模型并结合强化学习微调策略，使模型输出更符合人类期望。然而，RLHF 在数据稀缺场景下存在致命缺陷：**奖励模型容易过拟合**，导致强化学习训练不稳定且难以调参。DPO（Direct Preference Optimization）则绕过奖励模型，直接在偏好数据上进行监督式优化，避免了这一问题。

本文的核心洞察在于：**在文本到动作生成的数据稀缺条件下，利用非专家的人类偏好标注作为训练信号，可以绕过对运动捕捉数据的依赖**。具体而言，仅需标注者比较两个生成动作的优劣（而非提供专业动捕数据），即可为模型提供有效的对齐信号。这一思路将偏好学习从语言领域迁移到运动生成领域，同时通过 DPO 避免奖励模型过拟合、通过 LoRA 正则化稳定训练，形成了一套适用于稀缺数据场景的文本到动作对齐方案。

## 核心方法与创新机理

InstructMotion 的核心创新在于**将文本到动作生成问题重新表述为偏好学习问题**，从而绕过了对昂贵运动捕捉数据的依赖。传统的文本到动作模型（如 **MotionGPT**，Zhang et al., arXiv 2023）依赖稀缺的专业动捕数据进行监督训练，导致文本-动作对齐不足。InstructMotion 通过三个关键的 changed slots 实现了范式转变：

### 1. 训练数据：从文本-动作对到人类偏好比较

基线方法使用 HumanML3D 中的文本-动作对进行标准监督学习。InstructMotion 转而收集**3,528 个人类偏好标注对**——标注者仅需比较两个生成动作的优劣，无需专业动捕知识。这一设计使数据采集成本大幅降低，标注者间一致性达到 84%（42/50 样本），表明非专家也能提供可靠偏好信号。

### 2. 目标函数：从交叉熵损失到直接偏好优化

基线使用标准自回归交叉熵损失。InstructMotion 探索了两种偏好学习算法：RLHF（**Ouyang et al., NeurIPS 2022**）和 DPO。实验表明，**DPO 在有限偏好数据上显著优于 RLHF**（R-precision Top-1: 0.426 vs 0.415; MM Dist: 3.782 vs 3.908），根本原因在于稀缺数据导致奖励模型过拟合，使 RLHF 训练不稳定且难以调参。DPO 通过将奖励隐式表示为策略概率与参考模型概率比值的对数（Eq. 7），直接优化偏好数据，跳过了奖励模型训练环节：

$$\hat{r}_{\theta}(\mathbf{x},\mathbf{y}) = \beta \log \frac{\pi_{\theta}(\mathbf{y}\mid\mathbf{x})}{\pi_{\mathrm{ref}}(\mathbf{y}\mid\mathbf{x})} + \beta \log Z(\mathbf{x})$$

DPO 损失直接最大化优选与拒绝响应之间的奖励差距：

$$-\mathbb{E}_{(\mathbf{x},\mathbf{y}_w,\mathbf{y}_l)\sim\mathcal{D}} \left[ \log \sigma \left( \hat{r}_{\boldsymbol{\theta}}(\mathbf{x},\mathbf{y}_w) - \hat{r}_{\boldsymbol{\theta}}(\mathbf{x},\mathbf{y}_l) \right) \right]$$

### 3. 正则化技术：LoRA 是稳定训练的关键

基线除 dropout 外无显式正则化。InstructMotion 引入**低秩适应（LoRA）** 进行 DPO 微调，消融实验表明 LoRA 是决定性组件：移除 LoRA 后，Top-1 从 0.426 降至 0.394，MM Dist 从 3.782 升至 4.097，FID 从 0.219 升至 0.276。LoRA 通过参数高效的正则化防止了偏好数据上的训练不稳定。

### 创新深度分析

进一步消融揭示了偏好学习的几个关键特性：

- **偏好程度的重要性**：标注为“Much better”和“Better”的样本贡献了大部分性能增益，加入“Slightly better”等弱偏好样本仅略微改善对齐，甚至降低生成质量。这表明强偏好信号是驱动对齐提升的核心因素。
- **数据效率**：仅使用 20% 的偏好数据（约 700 对）即可获得大部分增益（Top-1: 0.422 vs 全量 0.426），收益呈递减趋势。
- **损失函数选择**：IPO 损失优于标准 DPO 和 KTO，因其缓解了 Bradley-Terry 模型在有限数据上的过拟合问题。
- **KL 惩罚鲁棒性**：模型对 KL 惩罚系数 β 在 0.05-0.20 范围内不敏感（β=0.10 最佳）。

需要注意的是，该创新仅在 MotionGPT 自回归骨干上验证，其在扩散模型等其他生成骨架上的泛化性尚待检验。

InstructMotion 的整体流程围绕一个核心瓶颈展开：**文本到动作生成模型依赖昂贵、专业化的运动捕捉数据，导致训练数据稀缺、文本-动作对齐不足**。为解决这一问题，该方法引入人类偏好作为训练信号，构建了一个包含数据采集、偏好学习和策略优化的完整管线。

### 管线概览

整个框架由五个关键模块串联而成，如图 1 所示：

1. **Motion Tokenizer（VQ-VAE）**：将连续运动序列离散化为运动分词（motion tokens），使动作生成问题可被自回归语言模型处理。
2. **Autoregressive MotionGPT**：以文本提示为条件，自回归地生成运动分词序列。该模型骨干为 **MotionGPT**（Zhang et al., arXiv 2023），其可处理的似然（tractable log-likelihood）是偏好学习方法得以应用的必要前提。
3. **Preference Data Collection**：通过 Gradio 界面收集人类标注者对生成动作对的偏好判断，共标注 3,528 个偏好对（标注者间一致性为 84%）。
4. **DPO Finetuning**：直接在偏好数据上优化策略，通过最大化优选响应与拒绝响应之间的隐式奖励差距来更新模型，无需显式训练奖励模型。
5. **RLHF（Reward Model + PPO）**：作为对比的替代路径——先训练奖励模型，再使用 PPO 对策略进行强化学习微调。

输入为文本描述 $\mathbf{x}$，输出为运动分词序列 $\mathbf{y}$，经 Motion Tokenizer 解码后得到连续运动序列。

### 两种偏好学习路径的核心差异

论文探索了两条实现偏好学习的技术路径，其根本区别在于**是否需要显式训练奖励模型**：

- **RLHF 路径**：先以交叉熵损失训练奖励模型 $r_\psi(\mathbf{x}, \mathbf{y})$，使其拟合 Bradley-Terry 偏好模型 $p^\star(\mathbf{y}\succ\mathbf{y}'\mid\mathbf{x}) = \sigma(r(\mathbf{x},\mathbf{y}) - r(\mathbf{x},\mathbf{y}'))$，再在 KL 正则化下最大化期望奖励。但实验发现，**在有限的偏好数据上训练会导致奖励模型过拟合，使 RLHF 训练不稳定且难以调参**。
- **DPO 路径**：跳过奖励模型，将奖励隐式表示为策略与参考模型的概率比值：$\hat{r}_{\theta}(\mathbf{x},\mathbf{y}) = \beta \log \frac{\pi_{\theta}(\mathbf{y}\mid\mathbf{x})}{\pi_{\mathrm{ref}}(\mathbf{y}\mid\mathbf{x})} + \beta \log Z(\mathbf{x})$，直接最大化 DPO 损失。实验表明 DPO 在 R-precision Top-1（0.426 vs 0.415）和 MM Dist（3.782 vs 3.908）上均优于 RLHF。

### 关键设计选择

框架中两个设计选择对最终性能至关重要：

- **LoRA 正则化**：在 DPO 训练中引入低秩适应（LoRA）起到关键正则化作用。移除 LoRA 后，Top-1 从 0.426 降至 0.394，MM Dist 从 3.782 升至 4.097，FID 从 0.219 升至 0.276，表明 LoRA 有效防止了训练不稳定。
- **偏好程度筛选**：偏好程度为“Much better”和“Better”的样本贡献了大部分性能增益；加入“Slightly better”和“Negligibly better”样本仅能略微改善对齐但会降低质量，说明高置信度偏好对是有效的学习信号。

> **注意**：FID 指标被论文明确指出不能准确衡量运动质量，人类偏好评估更为可靠。此外，标注者均为计算机科学研究生，可能引入人口偏见；1,312 对被标记为“跳过”的样本（双方生成动作均不真实）未用于训练，可能丢失了有价值的学习信号。

### 管道模块总览

InstructMotion 在 MotionGPT 自回归文本-动作生成框架之上，引入人类偏好学习，管道由五个核心模块构成：

1. **运动分词器（VQ‑VAE）**：将连续运动序列离散化为运动分词，类比语言模型中的文本分词。
2. **自回归 MotionGPT 骨干**：基于文本提示生成运动分词序列，具备可处理的对数似然。
3. **偏好数据收集**：通过 Gradio 标注平台收集人类对生成运动对的偏好比较，最终获得 3,528 个标注对。
4. **DPO 微调**：直接在偏好数据上优化策略，绕过奖励模型训练。
5. **RLHF（奖励模型 + PPO）**：作为对比方法，先训练奖励模型，再通过强化学习微调策略。

### 偏好学习目标函数

偏好学习的核心优化目标为：

$$J(\theta) = \mathbb{E}_{\mathbf{x}\sim\boldsymbol{\rho}} \left[ \boldsymbol{\Psi}(p^{\star}(\mathbf{y}\succ\mathbf{y}'\mid\mathbf{x})) \right] - \beta \mathbb{KL}(\pi_{\theta}||\pi_{\mathrm{ref}})$$

其中：
- $\mathbf{x}$ 为文本提示，$\mathbf{y}$ 为生成的运动序列；
- $p^{\star}(\mathbf{y}\succ\mathbf{y}'\mid\mathbf{x})$ 表示 $\mathbf{y}$ 优于 $\mathbf{y}'$ 的真实偏好概率；
- $\boldsymbol{\Psi}$ 是将偏好概率映射为实值的函数，不同算法对应不同映射；
- $\beta \mathbb{KL}(\pi_{\theta}||\pi_{\mathrm{ref}})$ 为 KL 散度正则项，约束当前策略 $\pi_{\theta}$ 不偏离参考策略 $\pi_{\mathrm{ref}}$ 过远。

KL 散度可进一步分解为交叉熵与熵之差：

$$\mathbb{KL}(\pi_{\theta} \| \pi_{\mathrm{ref}}) = \mathbb{H}[\pi_{\theta}, \pi_{\mathrm{ref}}] - \mathbb{H}[\pi_{\theta}]$$

### Bradley‑Terry 偏好模型

偏好概率通过 Bradley‑Terry 模型建模为潜在奖励值差异的 sigmoid 函数：

$$p^{\star}(\mathbf{y}\succ\mathbf{y}'\mid\mathbf{x}) = \sigma(r(\mathbf{x},\mathbf{y}) - r(\mathbf{x},\mathbf{y}'))$$

其中 $r(\mathbf{x},\mathbf{y})$ 为隐式的奖励函数，$\sigma$ 为 sigmoid 函数。

### RLHF 的两阶段优化

RLHF 采用双层优化：

**阶段一：奖励模型训练。** 以交叉熵损失拟合偏好分布：

$$-\mathbb{E}_{(\mathbf{x},\mathbf{y}_w,\mathbf{y}_l)\sim\mathcal{D}} \big[ \log \sigma( r_{\psi}(\mathbf{x},\mathbf{y}_w) - r_{\psi}(\mathbf{x},\mathbf{y}_l) ) \big]$$

其中 $\mathbf{y}_w$ 为优选运动，$\mathbf{y}_l$ 为被拒绝运动。

**阶段二：策略优化。** 最大化奖励期望并施加 KL 正则：

$$J(\theta) = \mathbb{E}_{\mathbf{x}\sim\rho, \mathbf{y}\sim\pi_{\theta}} \big[ r_{\psi}(\mathbf{x},\mathbf{y}) \big] - \beta \mathbb{KL}(\pi_{\theta}||\pi_{\mathrm{ref}})$$

### DPO 的核心公式

DPO 的关键洞察是将奖励函数隐式表示为策略与参考模型的概率比值：

$$\hat{r}_{\theta}(\mathbf{x},\mathbf{y}) = \beta \log \frac{\pi_{\theta}(\mathbf{y}\mid\mathbf{x})}{\pi_{\mathrm{ref}}(\mathbf{y}\mid\mathbf{x})} + \beta \log Z(\mathbf{x})$$

其中 $Z(\mathbf{x})$ 为与 $\mathbf{y}$ 无关的配分函数，在比较中可消去。由此得到 DPO 损失：

$$-\mathbb{E}_{(\mathbf{x},\mathbf{y}_w,\mathbf{y}_l)\sim\mathcal{D}} \left[ \log \sigma \left( \hat{r}_{\boldsymbol{\theta}}(\mathbf{x},\mathbf{y}_w) - \hat{r}_{\boldsymbol{\theta}}(\mathbf{x},\mathbf{y}_l) \right) \right]$$

该损失直接最大化优选响应与拒绝响应之间的隐式奖励差距，无需显式训练奖励模型。

### DPO 梯度与样本权重

DPO 的梯度更新可写为加权形式：

$$-\beta \mathbb{E}_{\mathcal{D}} \left[ w(\mathbf{x},\mathbf{y}_w,\mathbf{y}_l) \left[ \nabla_{\theta} \log \pi(\mathbf{y}_w\mid\mathbf{x}) - \nabla_{\theta} \log \pi(\mathbf{y}_l\mid\mathbf{x}) \right] \right]$$

其中每个样本的权重为：

$$w(\mathbf{x},\mathbf{y}_w,\mathbf{y}_l) = \sigma \big( \hat{r}_{\theta}(\mathbf{x},\mathbf{y}_l) - \hat{r}_{\theta}(\mathbf{x},\mathbf{y}_w) \big)$$

该权重衡量隐式奖励模型对当前偏好对的“错误程度”：当模型错误地给拒绝样本分配更高奖励时，权重增大，梯度更新力度加强。

### 瓶颈分析

论文揭示的核心瓶颈在于：**稀缺的偏好数据导致奖励模型过拟合，使得 RLHF 训练不稳定且难以调参**。DPO 通过绕过奖励模型直接优化策略，从根本上规避了这一问题。此外，**LoRA 低秩适应作为正则化手段对 DPO 的成功至关重要**——移除 LoRA 后，R‑precision Top‑1 从 0.426 降至 0.394，MM Dist 从 3.782 恶化至 4.097，FID 从 0.219 升至 0.276，表明无正则化时模型在偏好数据上严重过拟合。

## 实验与关键发现

### 核心发现：偏好学习有效提升文本-动作对齐

实验的核心结论是：在稀缺的偏好数据上训练，能够显著改善文本到动作生成模型的对齐质量，且直接偏好优化（DPO）优于基于强化学习的 RLHF 方案。

**主结果对比**（Table 1）显示，DPO 在关键对齐指标上全面领先：R-precision Top-1 达到 0.426，而 RLHF 为 0.415；MM Dist 降至 3.782（RLHF 为 3.908）。值得注意的是，论文明确指出 FID 指标并不能准确衡量运动质量——标注者在人类评估中显著偏好 DPO 的输出。这一偏好趋势在不同采样温度下均稳定成立（Figure 3），验证了偏好信号对生成质量的真实改善，而非自动指标的虚假提升。

RLHF 表现不佳的根本原因在于数据稀缺导致的奖励模型过拟合：仅 3,528 个偏好对不足以训练出可靠的奖励模型，使得后续的 PPO 强化学习阶段难以稳定调参。DPO 通过跳过奖励模型训练、直接在偏好数据上进行监督式优化，绕过了这一瓶颈。

### 消融分析：数据量、损失函数与正则化的关键作用

**偏好数据量的收益递减**（Table 2）：使用 20% 的数据（约 700 对）即可获得大部分性能增益——Top-1 从 0.422（20%）提升至 0.426（100%），MM Dist 从 3.775 降至 3.782，FID 从 0.252 降至 0.219。这表明 DPO 对数据量的需求不高，少量高质量偏好标注即可产生显著效果，但继续增加数据的边际收益递减。

**IPO 损失函数最优**（Table 3）：在 DPO 的多种变体中，IPO（Identity Preference Optimization）取得了最佳综合表现（Top-1 0.426, MM Dist 3.782, FID 0.219），优于标准 DPO 和 KTO。论文分析认为，IPO 的设计初衷是缓解 Bradley-Terry 偏好模型在小数据集上引起的过拟合，这与本任务的低数据场景高度契合。

**LoRA 正则化是关键使能技术**（Table 4）：移除 LoRA 后，DPO 的性能大幅下降——Top-1 从 0.426 跌至 0.394，MM Dist 从 3.782 升至 4.097，FID 从 0.219 升至 0.276。LoRA 的低秩约束在 DPO 训练中起到了关键的正则化作用，防止模型在有限的偏好数据上发生灾难性遗忘或过拟合。这一发现具有重要的实践指导意义：在数据稀缺条件下进行偏好微调时，参数高效的正则化手段不可或缺。

**偏好强度决定样本价值**（Figure 4）：仅使用偏好程度为“Much better”和“Better”的样本即可获得大部分性能增益。加入“Slightly better”和“Negligibly better/unsure”样本只能略微改善对齐指标，但会降低生成质量（FID 上升）。这说明强偏好信号是驱动对齐改善的主要因素，弱偏好样本的信噪比过低，甚至可能引入噪声。

**KL 惩罚系数 β 的鲁棒性**（Figure 5）：在 0.05 至 0.20 范围内调整 β 对对齐指标影响不大，β=0.10 表现最佳。这一鲁棒性降低了超参数调优的工程负担。

### 失败模式与评估陷阱

论文坦诚指出了若干关键限制：

1. **FID 指标失效**：FID 被明确认定为运动质量的不准确度量，与人类判断相关性弱。这意味着仅依赖自动指标评估文本到动作模型存在系统性偏差，人类偏好评估在当前阶段更为可靠。

2. **“跳过”样本的信息浪费**：标注过程中有 1,312 对样本因双方生成动作均不真实而被标注者跳过，这些样本未参与训练。它们可能蕴含有价值的负信号（例如可通过 unlikelihood 训练惩罚不真实动作），但论文未探索其利用方式。

3. **标注者群体单一**：所有标注者均为计算机科学研究生，可能引入特定的人口偏见，结论向普通用户群体的泛化性需进一步验证。

4. **模型骨架单一**：所有实验仅在 MotionGPT（自回归 Transformer）上进行，偏好学习方法在扩散模型等其他生成骨架上的有效性未知。

### 图表结论速览

| 图表 | 核心结论 |
|------|----------|
| Table 1 | DPO 在 R-precision 和 MM Dist 上全面优于 RLHF；FID 不可靠 |
| Figure 3 | 人类标注者在不同温度下均显著偏好 DPO 输出 |
| Table 2 | 20% 数据（~700 对）即可获得大部分增益，收益递减 |
| Table 3 | IPO 损失优于标准 DPO 和 KTO，缓解 Bradley-Terry 过拟合 |
| Table 4 | LoRA 是 DPO 成功的关键正则化组件 |
| Figure 4 | 仅“Much better”和“Better”样本贡献主要增益 |
| Figure 5 | β 在 0.05-0.20 范围内对性能影响不敏感 |

![[assets/figures/papers/paper_list_l3310_https_openaccess_thecvf_com_content_CVPR2024W_HuMoGen_papers_Sheng_Explo/figures/003_Table_1.jpg]]
*Table 1: Preference data improves alignment. We find that DPO performs better than RLHF. It is important to note that the FID metric is an inaccurate measure of the quality of the motion. In particular, our labelers prefer outputs from DPO over MotionGPT*

![[assets/figures/papers/paper_list_l3310_https_openaccess_thecvf_com_content_CVPR2024W_HuMoGen_papers_Sheng_Explo/figures/004_Figure_3.jpg]]
*Figure 3: Humans prefer DPO outputs over outputs from MotionGPT. MotionGPT trained on motion data with DPO (in green) has a higher win rate. The win rate is computed on prompts never seen by the model*

![[assets/figures/papers/paper_list_l3310_https_openaccess_thecvf_com_content_CVPR2024W_HuMoGen_papers_Sheng_Explo/figures/005_Table_2.jpg]]
*Table 2: More preference data helps. Our analysis reveals that an increased volume of preference data enhances performance in both alignment and quality metrics, although the impact diminishes with more data. Our results demonstrate that DPO does not need a significant amount of data to exhibit performance gains*

![[assets/figures/papers/paper_list_l3310_https_openaccess_thecvf_com_content_CVPR2024W_HuMoGen_papers_Sheng_Explo/figures/006_Table_3.jpg]]
*Table 3: IPO loss performs best. The IPO [3] variant of DPO is designed to alleviate overfitting due to the Bradley-Terry model*

![[assets/figures/papers/paper_list_l3310_https_openaccess_thecvf_com_content_CVPR2024W_HuMoGen_papers_Sheng_Explo/figures/007_Table_4.jpg]]
*Table 4: LoRA is an important component for preference learning. We find that LoRA significantly contributes to the success of DPO by regularizing the model’s training*

![[assets/figures/papers/paper_list_l3310_https_openaccess_thecvf_com_content_CVPR2024W_HuMoGen_papers_Sheng_Explo/figures/008_Figure_4.jpg]]
*Figure 4: Samples with preference degrees “Much better” and “Better” provide most of the performance gains. Adding in “Slightly better” and “Negligibly better/unsure” samples slightly improves alignment but decreases quality*

## 定位与知识库关联

**InstructMotion** 将偏好学习引入文本到动作生成，其直接前身是 **MotionGPT**（Zhang et al., arXiv 2023）——一种基于自回归 Transformer 和 VQ-VAE 运动分词器的文生动作模型。MotionGPT 采用标准交叉熵损失在 HumanML3D 的文本-动作对上训练，而 InstructMotion 在此基础上叠加了人类偏好信号，通过偏好对（而非额外的运动捕捉数据）来改善文本-动作对齐。

在偏好学习的技术路径上，本文同时探索了两条分支：**RLHF**（Ouyang et al., NeurIPS 2022）和 **DPO**（Rafailov et al., NeurIPS 2023）。RLHF 采用双层优化——先训练奖励模型，再通过 PPO 对策略进行强化学习；DPO 则跳过奖励模型，直接在偏好数据上做监督式最大似然估计。实验表明，在小规模偏好数据（3,528 对）下，RLHF 的奖励模型容易过拟合，导致训练不稳定且难以调参，而 DPO 在 R-precision Top-1（0.426 vs 0.415）和 MM Dist（3.782 vs 3.908）上均优于 RLHF。

### 关键技术决策与适用边界

InstructMotion 的几个关键设计选择直接定义了其适用边界：

1. **自回归骨干的必要性**：DPO 需要策略具有可处理的对数似然，因此本文选择了自回归 Transformer（MotionGPT），而非扩散模型等隐式生成模型。这限制了该方法向扩散式动作生成模型（如 MDM、MLD）的迁移。

2. **LoRA 正则化的核心作用**：消融实验（Table 4）表明，去掉 LoRA 后 DPO 性能大幅退化（Top-1 从 0.426 降至 0.394，FID 从 0.219 升至 0.276）。LoRA 在此充当了防止偏好训练中策略偏离参考模型过远的关键正则化手段，这一发现对低数据场景下的偏好学习具有普适意义。

3. **偏好程度的质量分层**：仅使用“Much better”和“Better”标签的样本即可获得大部分性能增益；加入“Slightly better”和“Negligibly better”样本仅略微改善对齐，却降低了生成质量（Figure 4）。这表明弱偏好信号可能引入噪声，偏好数据的质量比数量更重要。

4. **损失函数选择**：IPO 变体优于标准 DPO 和 KTO（Table 3），作者归因于 IPO 缓解了 Bradley-Terry 模型在小数据下的过拟合倾向。模型对 KL 惩罚系数 β 在 0.05-0.20 范围内不敏感（Figure 5），降低了超参调优负担。

### 局限与开放问题

**数据层面**：仅使用 3,528 个偏好对，且标注者均为计算机科学研究生，存在人口偏差。此外，1,312 对被标记为“跳过”（双方生成动作均不真实）的样本被直接丢弃，未探索其潜在学习信号——例如通过 unlikelihood 训练惩罚不真实动作。

**评估层面**：FID 被明确指为不可靠的运动质量指标，但论文未提出替代的自动评估方案。奖励模型本身是否可充当更好的自动评估器，是一个值得探索的方向。

**泛化性**：方法仅在 MotionGPT 单一骨干上验证，未在更大规模数据集（如 Motion-X）或扩散模型上测试。偏好学习能否在更丰富、更多样的动作生成场景中保持优势，仍是开放问题。

**细粒度偏好**：当前偏好标注仅给出整体优劣判断，未涉及动作特定属性（如速度、幅度、时序动态）的细粒度偏好信号。利用此类信号可能进一步提升对齐精度。

**混合训练策略**：DPO 的离线特性使其无法利用策略探索生成的新样本；将在线探索与离线 DPO 结合的混合方法是否更优，尚待研究。

## 原文 PDF

![[paperPDFs/CVPRW_2024/Exploring_Text-to-Motion_Generation_with_Human_Preference.pdf]]
