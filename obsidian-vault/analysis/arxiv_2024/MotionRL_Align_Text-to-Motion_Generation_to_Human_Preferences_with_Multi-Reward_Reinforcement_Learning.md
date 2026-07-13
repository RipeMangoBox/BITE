---
title: "MotionRL: Align Text-to-Motion Generation to Human Preferences with Multi-Reward Reinforcement Learning"
type: paper
paper_level: A
venue: arXiv
year: 2024
pdf_ref: "paperPDFs/arxiv_2024/MotionRL:_Align_Text-to-Motion_Generation_to_Human_Preferences_with_Multi-Reward_Reinforcement_Learning.pdf"
project_link: null
code_link: null
aliases:
- MotionRL
tags:
- arxiv_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 引入多奖励强化学习，利用预训练人类感知模型提供奖励，通过帕累托最优采样在文本一致性、运动质量和人类偏好之间寻求平衡，从而使生成器输出更符合人类判断。
primary_logic: 将人类感知建模为可计算的奖励，并借助逐批帕累托最优选择与特定奖励令牌，在无需人工调整权重的情况下自动学习多目标折中，同时保持文本-运动对齐和运动质量。
claims:
- MotionRL在HumanML3D测试集上的FID（0.066）和R-Precision Top-1（0.531）均显著优于T2M-GPT、InstructMotion等基线。
- 使用预训练感知模型评估，MotionRL生成的运动的感知分数明显高于其他方法。
- 用户研究显示，志愿者在文本一致性、运动质量和自然度方面更偏好MotionRL生成的运动。
- HumanML3D测试集 上 R-Precision Top-1 = 0.531 (MotionRL)
---

# MotionRL: Align Text-to-Motion Generation to Human Preferences with Multi-Reward Reinforcement Learning

> [!tip] 核心洞察
> 将人类感知建模为可计算的奖励，并借助逐批帕累托最优选择与特定奖励令牌，在无需人工调整权重的情况下自动学习多目标折中，同时保持文本-运动对齐和运动质量。

| 字段 | 内容 |
|------|------|
| 中文题名 | MotionRL：通过多奖励强化学习使文本到运动生成与人类偏好对齐 |
| 英文题名 | MotionRL: Align Text-to-Motion Generation to Human Preferences with Multi-Reward Reinforcement Learning |
| 会议/期刊 | arXiv 2024 |
| Links | [paper](https://arxiv.org/abs/2410.06513) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | MotionRL |
| Dataset | HumanML3D测试集 |

> [!tip] 效果简介
> - HumanML3D测试集 上，R-Precision Top-1 0.531 (MotionRL) vs 低于MotionRL的具体值参见Table 1 (显著提升)；FID 0.066 (MotionRL) vs 多数基线FID更高，详见Table 1 (更优)。
> - HumanML3D测试集（感知模型评估） 上，Perceptual Score 高于其他所有比较方法 (MotionRL) vs 较低分数 (其他方法) (定性更优)。
> - 用户研究 上，人类偏好胜率 MotionRL 生成的运动更受志愿者青睐 vs 其他对比方法 (定性更优)。

## 概要

**背景瓶颈**：现有文本到运动生成方法过度拟合数据集和传统误差指标（如FID），导致生成的运动缺乏真实感，无法捕捉视觉伪影、脚步滑动等人类细致感知的关键质量维度，与人类判断严重脱节。

**核心方法**：MotionRL 提出多奖励强化学习框架，将人类感知建模为可计算的奖励信号，通过逐批帕累托最优选择在文本一致性、运动质量和人类偏好三个目标之间自动寻求折中，无需人工调整权重。

**主要发现**：
- 在 HumanML3D 测试集上，MotionRL 的 FID 达到 **0.066**，R-Precision Top-1 达到 **0.531**，均显著优于 T2M-GPT、InstructMotion 等基线（Table 1）。
- 使用预训练感知模型评估，MotionRL 生成的运动的感知分数明显高于其他方法（Figure 3a）。
- 用户研究表明，志愿者在文本一致性、运动质量和自然度方面更偏好 MotionRL 生成的运动（Figure 3b）。

**方法定位**：MotionRL 以 InstructMotion 为基干模型进行 RL 微调，属于“预训练生成器 + 人类偏好对齐”范式，在方法谱系中与基于 GPT 式自回归生成（**T2M-GPT**, Zhang et al., CVPR 2023）和掩码建模生成（**MoMask**, Guo et al., 2023）形成互补——前者提供生成基础，MotionRL 在此基础上注入人类感知先验以提升生成质量。

文本到运动生成（Text-to-Motion Generation）旨在根据自然语言描述合成逼真的人体运动序列，在动画制作、虚拟现实和人机交互等领域具有广泛应用。近年来，基于自回归Transformer和向量量化变分自编码器（VQ-VAE）的方法在该任务上取得了显著进展。然而，现有方法面临一个根本性瓶颈：**过度拟合数据集和传统误差指标（如FID），导致生成的运动缺乏真实感，且与人类细致感知严重脱节**。

具体而言，现有范式存在两个关键缺口。第一，训练目标与人类判断之间存在错位。主流方法依赖交叉熵损失和文本-运动对齐损失进行监督学习，优化方向由数据集分布决定，无法捕捉视觉伪影、脚步滑动、物理合理性等人类高度敏感的质量维度。第二，多目标权衡缺乏有效机制。文本一致性、运动质量和人类偏好之间存在天然张力，现有方法通常不显式建模这些目标之间的关系，导致生成结果在某一维度上表现尚可，但综合质量难以令人满意。

针对上述问题，MotionRL提出了一种新的思路：**将人类感知建模为可计算的奖励信号，并通过多奖励强化学习使生成器直接与人类偏好对齐**。该方法的核心洞察在于，预训练的人类感知模型可以提供关于运动质量的细粒度反馈，而强化学习的探索-利用机制天然适合在多个奖励之间寻找折中。在此基础上，MotionRL进一步引入逐批帕累托最优选择与奖励特定令牌，在无需人工调整权重的情况下自动学习多目标折中策略，同时保持文本-运动对齐和运动质量。

## 核心方法与创新机理

MotionRL 的核心创新在于将文本到运动生成从传统的监督学习范式迁移至**多奖励强化学习（Multi-Reward RL）框架**，通过引入可计算的人类感知先验，使生成器输出与人类判断对齐。相较于现有方法，其关键改变体现在以下三个维度。

### 训练目标：从交叉熵损失到多奖励强化学习

现有文本到运动生成方法（如 **T2M-GPT**（Zhang et al., CVPR 2023）、**InstructMotion**）采用交叉熵损失与文本-运动对齐损失的纯监督学习范式。这种方式使模型过度拟合训练数据分布和传统评估指标（如 FID），却忽略了人类感知中的关键质量维度——例如视觉伪影、脚步滑动等细粒度缺陷。

MotionRL 将训练目标替换为基于 PPO 的多奖励强化学习，定义了三种奖励信号：
- **文本一致性奖励** $r_t$：基于预训练文本-运动匹配编码器，计算文本特征与生成运动特征之间的负距离（Equation 3）。
- **运动质量奖励** $r_m$：计算生成运动与真实运动在特征空间中的负距离（Equation 4）。
- **人类偏好奖励** $r_p$：利用预训练人类感知模型 $\mathcal{C}$ 对生成运动进行评分（Equation 6），其中感知模型通过成对比较数据训练（Equation 5），能够捕捉人类对运动自然度和真实感的细致判断。

这一改变的本质是将人类感知建模为可优化的奖励信号，使生成器不再仅仅拟合数据分布，而是主动向人类偏好方向优化。

### 人类感知引入方式：从隐式依赖到显式对齐

基线方法未显式引入人类感知，仅依赖数据集层面的统计指标进行评估，导致生成运动与人类细致感知严重脱节。MotionRL 通过以下机制实现显式对齐：

1. **预训练感知模型作为奖励源**：使用 Wang et al. (2024) 的预训练人类感知模型，该模型在人工标注的成对比较数据上训练，能够输出与人类判断高度相关的感知分数。
2. **关节到 SMPL 的快速转换**：由于感知模型需要 SMPL 格式输入，MotionRL 引入一个轻量转换网络（Conv1D + LSTM），将关节数据实时转换为 SMPL 格式（Figure 6），使感知模型能够无缝接入 RL 训练流程。
3. **RL 驱动的对齐优化**：通过 PPO 算法，生成器在训练过程中持续接收感知模型的反馈，逐步调整生成策略以提升人类偏好评分。

### 多目标权衡策略：从固定权重到帕累托最优选择

现有方法在面对多个优化目标时通常采用加权求和将其合并为单一目标，但权重选择高度依赖人工调参，且无法适应不同场景下的偏好变化。

MotionRL 提出**逐批帕累托最优选择**机制（Algorithm 1），核心设计包括：

- **批次内非支配排序**：对于每个文本输入的 $N$ 个候选生成运动，在三种奖励维度上进行帕累托支配关系判断，筛选出非支配的帕累托集合 $\mathcal{P}$。
- **仅在帕累托集合内更新**：PPO 的策略梯度更新仅使用帕累托集合中的样本（Equation 7），确保优化方向始终朝向多目标均衡改进，避免单一奖励主导训练。

$$
\mathcal{T}_r(\pi_\theta) = \sum_{k=1}^K \frac{1}{n(\mathcal{P})} \sum_{i=1, m_i \in \mathcal{P}}^N \sum_{t=1}^T \left[ r(t_k, m_k) - \beta \log \frac{\pi_\theta(m_k \mid t_k)}{\pi_{\mathrm{ref}}(m_k \mid t_k)} \right]
$$

- **奖励特定令牌**：引入可学习的奖励特定令牌（$t_k$），在推理时通过选择不同令牌控制优化方向，实现无需重新训练的目标偏好切换。为缓解新令牌对原始文本特征的干扰，采用特征加权混合（Equation 11）：

$$
\hat{\mathbf{f}}_{t_k} = (1 - \alpha) \mathbf{f}_t + \alpha \mathbf{f}_{t_k}
$$

消融实验（Table 2, Figure 5）证实：同时使用三种奖励相比单一或两种奖励在 R-Precision 和 FID 上取得最佳效果；帕累托选择相比简单加权求和在总体奖励值上表现显著更优；奖励特定令牌有效实现了推理时的可控权衡。

### 创新总结

MotionRL 的三项 changed slots 构成一个完整的创新链条：多奖励 RL 提供了与人类偏好对齐的优化框架，预训练感知模型将人类判断量化为可计算信号，帕累托最优选择则在无需人工调权的前提下自动学习多目标折中。这一设计使生成器在文本一致性（R-Precision Top-1: 0.531）、运动质量（FID: 0.066）和人类偏好（Figure 3）三个维度上均取得显著提升。

MotionRL 的整体流程围绕一个核心思想展开：**将人类感知建模为可计算的多维奖励，并通过强化学习使运动生成器在文本一致性、运动质量和人类偏好之间自动寻求帕累托最优折中**。其 pipeline 如 Figure 2 所示，由以下关键模块串联构成。

![[assets/figures/papers/paper_list_l3309_https_arxiv_org_abs_2410_06513/figures/002_Figure_2.jpg]]
*Figure 2: The overall pipeline of MotionRL. Given a text input, the Transformer serves as a motion generator, first producing multiple motions as a batch. Various rewards are then computed for these motions. Within this batch of motions, the Pareto set is identified. Finally, using the rewards from the Pareto set, along with the outputs of the critic model and the prediction logits, the motion generator is optimized using the PPO algorithm (note that the critic model is omitted in the diagram)*

### 输入与离散化：VQ‑VAE 编码

原始连续运动序列首先经过一个预训练的 **VQ‑VAE 编码器**，被映射为离散的码本索引序列 $S = \{s_1, s_2, \dots, s_{|S|}\}$。这一离散化步骤将运动生成转化为自回归令牌预测问题，为后续 Transformer 生成器提供统一的 token 空间。

### 文本条件自回归生成（Actor）

给定文本条件 $c$，**文本‑运动 Transformer 生成器**（Actor）以自回归方式逐令牌预测运动序列，其概率分解为：

$$p(S \mid c) = \prod_{i=1}^{|S|} p(s_i \mid c, S_{<i})$$

在实际推理中，Actor 对每条文本 **生成一批候选运动**（而非单个样本），这批候选运动是后续多目标评估与帕累托选择的基础。基干模型选用 **InstructMotion**，Transformer 配置为 18 层、隐藏维度 1024、16 个注意力头。

### 多目标奖励计算

对批次中的每条生成运动，**多目标奖励计算模块** 分别输出三个维度的奖励信号：

- **文本一致性奖励** $r_t$：基于预训练文本‑运动匹配编码器，计算文本特征 $\mathbf{f}_t$ 与生成运动特征 $\mathbf{f}_{m_{\mathrm{pred}}}$ 之间加权距离的负值（Equation 3）。
- **运动质量奖励** $r_m$：类似地计算生成运动特征与真实运动特征 $\mathbf{f}_{m_{\mathrm{gt}}}$ 的距离负值（Equation 4）。
- **人类偏好奖励** $r_p$：通过一个预训练的 **人类感知模型** $\mathcal{C}$ 直接对运动评分（Equation 6）。由于感知模型需要 SMPL 格式输入，pipeline 中嵌入了一个轻量 **联合‑SMPL 快速转换网络**（Conv1D + LSTM），将关节数据实时转换为 SMPL 格式（Figure 6）。

三种奖励在计算前均经过 **扩展最小‑最大归一化**（Equation 12），统一到可比尺度。

### 帕累托最优选择

传统多目标 RL 通常通过加权求和将多个奖励合并为单一标量，但这需要人工设定权重且难以捕捉目标间的 trade‑off。MotionRL 采用 **逐批帕累托最优选择**：在每批生成的运动中，识别出在所有奖励维度上均不被其他样本支配的 **帕累托集合** $\mathcal{P}$（Algorithm 1）。只有帕累托集合中的样本才会参与后续的策略优化，从而在无需手动调权的情况下自动逼近多目标帕累托前沿。

### PPO 策略优化（Actor‑Critic）

利用帕累托集合中的样本，**基于 PPO 的策略优化模块** 对生成器参数进行更新。优化目标包含多奖励项与 KL 散度正则项：

$$\mathcal{T}_r(\pi_\theta) = \sum_{k=1}^K \frac{1}{n(\mathcal{P})} \sum_{i=1, m_i \in \mathcal{P}}^N \sum_{t=1}^T \left[ r(t_k, m_k) - \beta \log \frac{\pi_\theta(m_k \mid t_k)}{\pi_{\mathrm{ref}}(m_k \mid t_k)} \right]$$

其中 $\pi_{\mathrm{ref}}$ 为参考策略，$\beta$ 控制 KL 惩罚强度。Critic 模型输出状态价值 $V_\phi(s_t)$，用于计算优势函数 $A_t = G_t - V_\phi(s_t)$（Equation 8），指导 Actor 的梯度更新。

### 奖励特定令牌与特征混合

为在推理时灵活控制优化方向，MotionRL 在文本条件中引入了 **奖励特定令牌**（如 `[R_t]`、`[R_m]`、`[R_p]`），分别对应三种奖励维度。然而直接引入新令牌会导致初始训练阶段性能下降——因为预训练生成器从未见过这些令牌。为此，pipeline 中增加了 **特征加权引导模块**，将原始文本特征 $\mathbf{f}_t$ 与奖励令牌特征 $\mathbf{f}_{t_k}$ 按权重 $\alpha$ 混合：

$$\hat{\mathbf{f}}_{t_k} = (1 - \alpha) \mathbf{f}_t + \alpha \mathbf{f}_{t_k}$$

这一设计有效缓解了新令牌引入的干扰，使模型在保持文本‑运动对齐能力的同时获得奖励维度的可控性（见 Appendix B 及 Figure 5 右子图）。

### 数据流总结

整体数据流为：**文本 → Transformer 生成器（批量输出运动 token）→ VQ‑VAE 解码为连续运动 → 多奖励计算（文本一致性、运动质量、人类偏好）→ 帕累托集合筛选 → PPO 更新 Actor/Critic**。其中人类偏好奖励分支额外经过关节‑SMPL 转换网络，而推理时可通过奖励特定令牌与特征混合实现偏好可控生成。

MotionRL 的核心设计围绕三个关键模块展开：**多目标奖励计算**、**逐批帕累托最优选择**，以及**基于 PPO 的策略优化**。这些模块协同工作，使文本到运动生成器能够在无需人工设定权重的情况下，自动在文本一致性、运动质量和人类偏好之间寻求折中。

### 多目标奖励计算

系统定义了三种奖励信号，分别对应三个优化维度：

**文本一致性奖励** 衡量生成运动与输入文本的语义对齐程度：
$$r_{t} = -\sum^{i} \lambda_{i} \lVert \mathbf{f}_{t,i} - \mathbf{f}_{m_{\mathrm{pred}},i} \rVert^{2}$$
其中 $\mathbf{f}_{t,i}$ 和 $\mathbf{f}_{m_{\mathrm{pred}},i}$ 分别表示文本特征和生成运动特征，$\lambda_{i}$ 为各编码器的权重系数。该奖励通过预训练的文本-运动匹配编码器计算，编码器采用对比损失 $\mathcal{L}_{CL}$（Guo et al.）和 InfoNCE 损失 $\mathcal{L}_{InfoNCE}$（Lu et al.）进行训练。

**运动质量奖励** 评估生成运动与真实运动的分布相似性：
$$r_{m} = -\sum^{i} \lambda_{i} \lVert \mathbf{f}_{m_{\mathrm{gt}},i} - \mathbf{f}_{m_{\mathrm{pred}},i} \rVert^{2}$$
$\mathbf{f}_{m_{\mathrm{gt}},i}$ 为真实运动的特征表示。该奖励本质上是运动重建质量的度量。

**人类偏好奖励** 利用预训练感知模型直接建模人类对运动质量的判断：
$$r_{p} = \mathcal{C}(g(m_{\mathrm{pred}}))$$
其中 $g(\cdot)$ 为格式转换函数，将关节数据转为 SMPL 格式；$\mathcal{C}(\cdot)$ 为感知模型，其训练目标为：
$$\mathcal{L}_{perception} = -\mathbb{E}_{(m^{(h)}, m^{(l)}) \sim \mathcal{D}} [\log \sigma(\mathcal{C}(m^{(h)}), \mathcal{C}(m^{(l)}))]$$
该损失通过成对比较数据 $\mathcal{D}$ 训练，使模型能够区分高质量运动 $m^{(h)}$ 和低质量运动 $m^{(l)}$。

### 逐批帕累托最优选择

为避免传统加权求和中权重难以设定的问题，MotionRL 在每个批次内执行帕累托最优选择。给定一批候选运动及其对应的三个奖励值，筛选出非支配解构成帕累托集合 $\mathcal{P}$。只有在帕累托集合中的样本才会被用于策略更新，从而引导生成器向多目标前沿面演进。

为统一不同奖励的尺度，采用扩展的最小-最大归一化：
$$r_{k, \mathrm{normalized}} = \begin{cases} \frac{r_k - \mathrm{min.val}_k}{\mathrm{max.val}_k - \mathrm{min.val}_k}, & \mathrm{if~min.val}_k \leq r_k \leq \mathrm{max.val}_k \\ \frac{r_k - \mathrm{min.val}_k}{\mathrm{max.val}_k - \mathrm{min.val}_k}, & \mathrm{if~} r_k < \mathrm{min.val}_k \\ \frac{r_k - \mathrm{max.val}_k}{\mathrm{max.val}_k - \mathrm{min.val}_k} + 1, & \mathrm{if~} r_k > \mathrm{max.val}_k \end{cases}$$
其中 $\mathrm{min.val}_k$ 和 $\mathrm{max.val}_k$ 为各奖励类型的估计边界值，超出范围时仍可平滑处理。

### 基于 PPO 的策略优化

生成器（Actor）以自回归方式建模运动令牌序列 $S$ 的条件概率：
$$p(S | c) = \prod_{i=1}^{|S|} p(s_{i} | c, S_{<i})$$
其中 $c$ 为文本条件，$S_{<i}$ 为已生成的前缀令牌。

策略优化采用 PPO 算法，目标函数为：
$$\mathcal{T}_r(\pi_\theta) = \sum_{k=1}^K \frac{1}{n(\mathcal{P})} \sum_{i=1, m_i \in \mathcal{P}}^N \sum_{t=1}^T \left[ r(t_k, m_k) - \beta \log \frac{\pi_\theta(m_k \mid t_k)}{\pi_{\mathrm{ref}}(m_k \mid t_k)} \right]$$
其中 $\pi_\theta$ 为当前策略，$\pi_{\mathrm{ref}}$ 为参考策略，$\beta$ 控制 KL 散度正则项的强度。优势函数定义为：
$$A_t = G_t - V_\phi(s_t)$$
$G_t$ 为累积奖励，$V_\phi(s_t)$ 为 Critic 网络对状态 $s_t$ 的价值估计。

### 奖励特定令牌与特征混合

为在推理时实现可控的偏好调节，系统引入奖励特定令牌。不同令牌对应不同的优化方向，通过将其嵌入与原始文本特征进行加权混合来缓解新令牌引入导致的性能下降：
$$\hat{\mathbf{f}}_{t_k} = (1 - \alpha) \mathbf{f}_t + \alpha \mathbf{f}_{t_k}$$
其中 $\mathbf{f}_t$ 为原始文本特征，$\mathbf{f}_{t_k}$ 为奖励特定令牌的特征，$\alpha$ 为混合权重。

> **待验证**：特征混合权重 $\alpha$ 的具体取值以及各奖励类型估计边界值 $\mathrm{min.val}_k$、$\mathrm{max.val}_k$ 的获取方式，原文未明确给出，需查阅补充材料或进行手动验证。

### 补充图表

![[assets/figures/papers/paper_list_l3309_https_arxiv_org_abs_2410_06513/figures/009_Figure_6.jpg]]
*Figure 6: Visualization of motions in different formats (a) Original joint-based motion (b) SMPLbased motion after conversion using our trained model*

## 实验与关键发现

### 核心实验设置

**基干模型与架构**。MotionRL 选用 **InstructMotion** 作为强化学习微调的基干模型。文本-运动 Transformer 生成器（Actor）由 18 层组成，每层隐藏维度为 1024，配备 16 个注意力头。评估在 HumanML3D 测试集上进行，指标计算遵循 Guo et al. (2022b) 的协议。

**奖励模型来源**。文本一致性奖励和运动质量奖励分别基于 Guo et al. 和 Lu et al. 提出的预训练文本-运动匹配编码器计算特征距离；人类偏好奖励则使用 Wang et al. (2024) 的预训练感知模型，通过一个轻量级转换网络（Conv1D+LSTM）将关节数据转为 SMPL 格式后输入感知模型获得评分。

---

### 主实验结果

**定量对比（Table 1）**。MotionRL 在 HumanML3D 测试集上取得了 **R-Precision Top-1 为 0.531**，显著优于 T2M-GPT（Zhang et al., CVPR 2023）、InstructMotion 等基线方法；**FID 降至 0.066**，同样优于多数对比方法。这表明通过多奖励 RL 微调，生成运动在文本-运动对齐和整体分布质量两个维度均获得了实质性提升。

**人类偏好评估（Figure 3）**。该评估从两个角度验证了方法有效性：
- **感知模型评分（Figure 3a）**：使用 Wang et al. 的预训练感知模型对测试集生成结果打分，MotionRL 的感知分数明显高于其他所有对比方法，说明模型输出与人类感知判断更为一致。
- **用户研究（Figure 3b）**：志愿者在文本一致性、运动质量和自然度三个维度上进行偏好选择，MotionRL 生成的运动胜率显著优于对比方法，直接验证了人类偏好对齐的有效性。

**定性对比（Figure 4）**。与 MoMask（Guo et al., 2023）等 top-performing 方法的可视化对比显示，MotionRL 在动作准确性和文本语义匹配方面表现更好——当文本描述特定动作时，MotionRL 能生成与之对齐的运动，而其他方法则可能出现动作偏差或语义丢失。

---

### 消融实验

**奖励组合消融（Table 2）**。消融实验系统考察了三种奖励（人类偏好 R_p、运动质量 R_m、文本一致性 R_t）的不同组合效果。结果表明，同时使用全部三种奖励时，模型在 R-Precision Top-1（0.531）、FID（0.064）和感知分数（0.494）上均达到最优。仅使用单一奖励或任意两种奖励的组合均会导致至少一个维度的性能下降，说明三类奖励之间存在互补关系，共同驱动生成器向人类偏好方向优化。

**帕累托最优选择的有效性（Figure 5）**。与传统加权求和将多目标合并为单一奖励不同，MotionRL 在每个批次内进行帕累托最优选择。Figure 5 显示，帕累托选择策略在总体奖励值上明显优于简单加权求和，验证了逐批近似帕累托最优性在多目标权衡中的优势——它避免了人工设定权重的困难，同时自动找到了文本一致性、运动质量和人类偏好之间的有效折中。

**奖励特定令牌与特征混合（Figure 5 右子图，Appendix B）**。引入奖励特定令牌（reward-specific tokens）允许在推理时通过选择不同令牌来控制优化方向。然而，新令牌的引入会导致初始训练阶段性能下降。为此，MotionRL 采用特征加权混合策略，将原始文本特征与奖励特定令牌特征按权重 α 混合（Equation 11），有效缓解了这一问题。消融结果证实该混合策略对稳定训练和最终性能均有正面贡献。

---

### 失败模式与局限性

**感知模型依赖**。MotionRL 的人类偏好奖励完全依赖预训练感知模型的质量。若感知模型本身存在偏差或无法准确捕捉某些运动质量维度（如细微的物理不合理性），则 RL 优化方向可能偏离真实人类偏好。论文未在训练前引入额外的人工标注来校准感知模型，这构成了方法的潜在脆弱点。

**奖励归一化的粗糙性**。不同奖励的尺度差异通过扩展最小-最大归一化（Equation 12）处理，但归一化所需的 min.val_k 和 max.val_k 仅为粗略估计值。虽然实验表明该策略足以稳定训练，但缺乏细粒度校准可能导致奖励尺度失真的风险，尤其在奖励分布发生偏移时。

**格式转换的透明性不足**。人类偏好奖励需要将关节数据转换为 SMPL 格式，但该转换网络的具体结构、训练数据和训练细节未在正文中充分展开（仅置于 Appendix A），其转换精度对最终感知评分的潜在影响需要读者自行验证。

### 补充图表

![[assets/figures/papers/paper_list_l3309_https_arxiv_org_abs_2410_06513/figures/003_Table_1.jpg]]
*Table 1: Quantitative comparison on HumanML3D test set. The evaluation metrics are computed following Guo et al. (2022b). § indicates reliance on ground-truth sequence length for generation. Underline indicates the second best*

![[assets/figures/papers/paper_list_l3309_https_arxiv_org_abs_2410_06513/figures/005_Figure_3.jpg]]
*Figure 3: Human Preferences Evaluation. (a) Perceptual scores on the test set using the pretrained perception model from Wang et al. (2024). The results show that our method aligns more closely with human perception compared to other approaches. (b) Comparison of human evaluations between our method and others. The results demonstrate that our method generates motions that are more consistent with human preferences*

![[assets/figures/papers/paper_list_l3309_https_arxiv_org_abs_2410_06513/figures/007_Table_2.jpg]]
*Table 2: Ablation of Reward Design*

![[assets/figures/papers/paper_list_l3309_https_arxiv_org_abs_2410_06513/figures/001_Figure_1.jpg]]
*Figure 1: Examples generated by MoMask and Ours. Our method significantly outperforms the previous state-of-the-art MoMask in text adherence, motion quality and human preferences*

## 定位与知识库关联

### 与基线方法的关系

MotionRL 直接建立在 **InstructMotion** 之上，将其作为强化学习微调的基干模型。InstructMotion 本身采用纯监督学习范式，训练目标为交叉熵损失与文本-运动对齐损失的组合，未显式引入人类感知信号。MotionRL 保留了该基干的 VQ-VAE 编码器与文本-运动 Transformer 生成器（Actor）架构，但在训练目标层面进行了根本性替换：将监督损失替换为基于 PPO 的多奖励强化学习目标，从而将生成器的优化方向从“拟合数据集分布”转向“最大化人类感知相关的奖励信号”。

在比较基线中，**T2M-GPT**（Zhang et al., CVPR 2023）是 GPT 式自回归文本-运动生成的代表性方法，**MoMask**（Guo et al., 2023）则是基于掩码建模的最优方法，被用于定性对比。Table 1 显示，MotionRL 在 HumanML3D 测试集上的 FID（0.066）和 R-Precision Top-1（0.531）均显著优于上述基线，表明多奖励 RL 微调在传统自动指标上同样带来了增益，而非仅在感知维度上有效。

### 方法适用边界

MotionRL 的核心机制——利用预训练人类感知模型提供奖励并通过帕累托最优选择进行多目标折中——决定了其适用边界高度依赖以下前提条件：

1. **感知模型的质量与覆盖范围**：人类偏好奖励 $r_p = \mathcal{C}(g(m_{\mathrm{pred}}))$ 直接依赖预训练感知模型 $\mathcal{C}$ 的评分可靠性。若感知模型未覆盖某些关键质量维度（如特定运动类型的物理合理性、细粒度手部交互），RL 优化将无法感知这些维度的缺陷，甚至可能被误导。论文明确指出该方法“高度依赖预训练感知模型的质量”，且未在训练前引入额外的人工标注成本来校准或补充感知模型。

2. **数据格式转换的保真度**：为使用感知模型，需要将关节数据通过轻量神经网络（Conv1D + LSTM）转换为 SMPL 格式（见 Figure 6）。这一转换环节引入了额外的近似误差，若转换质量不足，感知模型的评分将偏离真实运动质量。

3. **多目标冲突的不可消解性**：帕累托最优选择在批次内寻找非支配解，但文本一致性、运动质量和人类偏好之间可能存在根本性冲突（例如，高度写实的运动可能偏离文本的精确语义）。该方法通过奖励特定令牌（reward-specific tokens）允许推理时控制偏好方向，但并未从根本上消除目标间的张力。

### 局限与开放问题

**已确认的局限：**

- 奖励归一化采用扩展最小-最大归一化（Equation 12），但仅使用粗略的估计最小/最大值 $\mathrm{min.val}_k$ 和 $\mathrm{max.val}_k$。虽能稳定训练，但未进行细粒度校准，可能导致不同奖励类型的尺度对齐不够精确。
- 方法效果高度依赖预训练感知模型，若感知模型存在系统性偏差，RL 优化将放大该偏差。
- 引入奖励特定令牌后，初始训练阶段会出现性能下降，需通过特征加权混合 $\hat{\mathbf{f}}_{t_k} = (1 - \alpha) \mathbf{f}_t + \alpha \mathbf{f}_{t_k}$ 缓解（Appendix B）。

**需人工验证的开放问题：**

- 每种奖励类型的估计最小/最大值（$\mathrm{min.val}_k$, $\mathrm{max.val}_k$）的具体获取方式未在可用材料中明确说明，需要查阅完整论文或代码。
- 特征混合权重 $\alpha$ 的具体取值未在可用部分中披露。
- 关节到 SMPL 的转换网络的训练细节（损失函数、数据配对标定方式）透明度不足，影响对整体管线可靠性的判断。

### 在知识库中的定位

MotionRL 在文本-运动生成领域引入了“人类感知驱动的 RL 对齐”这一新范式，其核心贡献在于将多目标权衡问题形式化为批次内帕累托最优选择，避免了传统加权求和中权重调参的工程负担。相较于 InstructMotion 等纯监督方法，MotionRL 将优化目标从“拟合数据分布”升级为“逼近人类偏好”，在方法论层面与 LLM 对齐领域的 RLHF 思路形成呼应，但在运动生成这一连续-离散混合空间中实现了多奖励帕累托优化的独特设计。其后续工作可能沿两个方向展开：（1）引入在线人类反馈以克服静态感知模型的局限；（2）将帕累托选择机制推广至其他多模态生成任务。

## 原文 PDF

![[paperPDFs/arxiv_2024/MotionRL:_Align_Text-to-Motion_Generation_to_Human_Preferences_with_Multi-Reward_Reinforcement_Learning.pdf]]
