---
title: Resolving the Identity Crisis in Text-to-Image Generation
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Resolving_the_Identity_Crisis_in_Text_to_Image_Generation.pdf
project_link: "https://qualcomm-ai-research.github.io/disco/"
code_link: null
aliases:
- DRDC
- RICTIG
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过 GRPO 强化学习框架，使用组合奖励（图像内多样性、群体间多样性、计数准确性和 HPS 质量）以及单阶段课程学习，直接优化身份多样性，从根本上消除身份崩溃。
primary_logic: 在强化学习微调中同时施加图像内和跨样本的身份多样性约束，并引入计数和质量控制以防止奖励黑客，可显著提升多人场景中的身份独特性，同时保持图像质量。
claims:
- DISCO(Flux) 在 DiverseHumans-TestPrompts 上达到 98.6% Unique Face Accuracy 和 98.3% Global Identity Spread，远超基线模型。
- 消融研究证明，单独使用图像内多样性奖励会改善 UFA 但导致 GIS 崩溃，而加入群体多样性奖励可恢复全局多样性。
- 人类偏好研究证实，UFA 指标与人类对身份多样性的判断相关性达到 1.0。
- DiverseHumans-TestPrompts (2-7 People) 上 Count Accuracy = 92.4
---

# Resolving the Identity Crisis in Text-to-Image Generation

> [!tip] 核心洞察
> 在强化学习微调中同时施加图像内和跨样本的身份多样性约束，并引入计数和质量控制以防止奖励黑客，可显著提升多人场景中的身份独特性，同时保持图像质量。

| 字段 | 内容 |
|------|------|
| 中文题名 | 解决文本到图像生成中的身份危机 |
| 英文题名 | Resolving the Identity Crisis in Text-to-Image Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2510.01399) · [Project](https://qualcomm-ai-research.github.io/disco/) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | DISCO (Reinforcement with DiverSity Constraints) |
| Dataset | DiverseHumans-TestPrompts, MultiHuman-TestBench |

> [!tip] 效果简介
> - DiverseHumans-TestPrompts (2-7 People) 上，Count Accuracy 92.4 vs 70.8 (Flux-Dev) (+21.6)；Unique Face Accuracy (UFA) 98.6 vs 48.2 (Flux-Dev) (+50.4)；Global Identity Spread (GIS) 98.3 vs 50.5 (Flux-Dev) (+47.8)。
> - MultiHuman-TestBench (1-5 People) 上，Count Accuracy 86.6 vs 61.8 (Flux-Dev) (+24.8)；Unique Face Accuracy (UFA) 94.3 vs 56.5 (Flux-Dev) (+37.8)。

## 概要

文本到图像生成模型在单人场景下已取得令人瞩目的视觉质量，但在生成包含多人的图像时，普遍存在**身份重复**与**计数错误**的问题——同一张图像内的人脸高度相似，不同样本之间身份被复制，甚至生成的人数与提示不符。论文将这一现象称为“身份危机”（Identity Crisis），并指出其根源在于现有模型缺乏对身份多样性的显式建模：仅优化图像内部的多样性，无法解决跨样本的全局身份多样性崩溃。

针对上述瓶颈，论文提出 **DISCO（Reinforcement with DiverSity Constraints）**，一种基于强化学习的微调框架。DISCO 的核心思路是：在流匹配模型的 GRPO（Group-Relative Policy Optimization）训练中，引入一个**组合奖励函数**，同时约束图像内人脸多样性、跨样本身份多样性、计数准确性和图像质量，从而从根本上消除身份崩溃。该方法无需真实身份数据，仅使用合成提示即可完成训练。

实验结果显示，DISCO 在 DiverseHumans-TestPrompts 基准上将基线模型 FLUX-Dev 的**唯一人脸准确率（UFA）**从 48.2% 提升至 98.6%，**全局身份多样性（GIS）**从 50.5% 提升至 98.3%，计数准确率也提高了 21.6 个百分点。消融研究证实，图像内多样性奖励可改善 UFA 但会导致 GIS 崩溃，而加入群体多样性奖励后全局多样性得以恢复。人类偏好研究进一步验证了 UFA 指标与人类对身份多样性判断的完美相关性（1.0）。



文本到图像生成领域近年来取得了显著进展，模型在单人物肖像生成上已能产出高度逼真的结果。然而，当提示词要求生成**多人场景**时，现有方法普遍面临严重的“身份危机”（Identity Crisis）——生成图像中的人脸出现重复、身份合并、计数错误等问题。图 1 直观展示了这一现象：初看之下图像质量尚可，但仔细观察即可发现多张人脸实为同一身份的复制品。

这一问题的根源在于，当前主流文本到图像模型（如 **FLUX-Dev**、**SD3.5** 等）在训练过程中**缺乏对身份多样性的显式建模**。模型仅通过扩散或流匹配损失学习图像分布，并未被要求区分不同个体的面部特征。因此，当提示词中未明确指定每个人的具体属性时，模型倾向于生成高度相似甚至完全相同的人脸，导致图像内人脸重复（intra-image duplication）和跨样本身份复制（cross-sample identity repetition）。

更值得关注的是，仅优化图像内多样性无法解决全局身份多样性崩溃的问题。消融实验表明（见 Table 2），单独使用图像内多样性奖励虽然能提升单张图像内的唯一人脸准确率（UFA），但会导致全局身份多样性指标（GIS）急剧下降——模型学会了为每张图像生成不同的人脸，却在不同图像之间反复使用同一组身份。这说明**身份多样性必须在图像内和跨样本两个层面同时施加约束**。

此外，多人场景还面临**计数准确性**的挑战。模型常常无法精确控制生成的人脸数量，导致实际人数与提示词要求不符。这一问题在人数超过 3-4 人时尤为突出（Figure 5），现有模型在 4 人阈值处出现显著的性能断崖。

DISCO 的核心动机正是针对上述三个相互关联的瓶颈：**图像内身份重复、跨样本身份复制、以及计数错误**。通过引入基于强化学习的微调框架，DISCO 在生成过程中同时施加图像内多样性约束、群体间多样性约束和计数准确性约束，从根本上消除身份崩溃，同时保持图像感知质量。



## 核心方法与创新机理

DISCO 的核心创新在于将多人文本到图像生成的身份多样性问题，重新定义为强化学习微调中的**组合奖励优化**问题。现有方法（如 FLUX-Dev、SD3.5 等流匹配/扩散模型）在标准训练范式下缺乏对身份多样性的显式建模，导致同一图像内人脸重复、跨样本身份复制及计数错误等“身份危机”（Figure 1）。DISCO 通过三个关键层面的创新，从根本上改变了这一局面。

### 1. 训练框架创新：从标准生成到 GRPO 强化学习微调

不同于标准扩散/流匹配模型的直接微调，DISCO 采用 **Group-Relative Policy Optimization (GRPO)** 框架对预训练流匹配模型进行微调。GRPO 通过组内归一化优势函数 $\tilde{A}_i = \frac{r(\tau_i, c) - \mu_c}{\sigma_c}$ 进行策略优化，目标函数为：

$$\max_{\theta} \mathbb{E}_c \left[ \frac{1}{M} \sum_{i=1}^M \tilde{A}_i \log \pi_{\theta}(\tau_i \mid c) \right] - \beta_{KL} \mathbb{E}_c \left[ \mathrm{KL}(\pi_{\theta}(\cdot \mid c) \| \pi_{\theta_{\mathrm{ref}}}(\cdot \mid c)) \right]$$

这一框架的关键优势在于：组内相对比较机制天然适合捕捉跨样本的身份多样性信号，而 KL 散度惩罚项则防止模型偏离原始生成能力过远。训练时使用较少的去噪步数（$K_{\mathrm{train}} \ll K_{\mathrm{test}}$）以提高效率，测试时恢复完整去噪调度（Section 3.1）。

### 2. 多样性优化创新：从无约束到双重多样性奖励

现有模型仅依赖文本提示隐式引导多样性，缺乏显式约束。DISCO 引入了**两层互补的多样性奖励**：

**图像内多样性奖励**（Intra-Image Diversity Reward）直接惩罚同一图像中面部的最大余弦相似度：

$$r_{\mathrm{img}}^d(x_i) = \begin{cases} 1 - \max_{j \neq k} s(f_{i,j}, f_{i,k}) & \text{if } m_i \geq 2 \\ 0.5 & \text{if } m_i < 2 \end{cases}$$

其中 $f_{i,j}$ 为通过 ArcFace 提取的面部嵌入，$s(\cdot, \cdot)$ 为余弦相似度。该奖励迫使模型在同一图像内生成彼此不同的面部特征。

**群体多样性奖励**（Group-wise Diversity Reward）是 DISCO 最具原创性的设计。它基于反事实推理，衡量某张图像 $x_i$ 从生成组 $G$ 中移除后，组内身份相似度的变化：

$$r_{\mathrm{grp}}^d(x_i, G) = \sigma(-\lambda \Delta_i), \quad \sigma(u) = \frac{1}{1 + e^{-u}}, \lambda = 5$$

其中 $\Delta_i$ 为移除 $x_i$ 后群体相似度的变化量。这一设计的精妙之处在于：它利用了 GRPO 天然的分组生成机制，无需额外数据即可构建跨样本的反事实信号，直接抑制跨样本身份重复。消融实验（Table 2）证实，单独使用图像内多样性奖励会改善 UFA 但导致 GIS 崩溃，而加入群体多样性奖励可恢复全局多样性。

### 3. 训练策略创新：从标准微调到课程学习

DISCO 采用**单阶段课程学习**策略，从简单分布逐步过渡到均匀分布：

$$p_t(n) = \begin{cases} p_{\mathrm{ann}}(n,t) & \text{if } t \le t_{\mathrm{curriculum}} \\ p_{\mathrm{uni}}(n) & \text{if } t > t_{\mathrm{curriculum}} \end{cases}$$

训练初期优先采样人数较少（2-4 人）的简单场景，随着训练步数增加逐渐退火到全范围（2-$N_{\max}$ 人）的均匀采样。这一策略稳定了训练过程，使模型能够先掌握基本多样性约束，再泛化到更复杂的多人场景。对于专家模型，简单集边界为 2-4 的课程学习在 UFA 和 GIS 之间取得最佳平衡（Table E.5）。

### 创新效果验证

DISCO 的组合奖励设计产生了显著效果：在 DiverseHumans-TestPrompts 基准上，DISCO(Flux) 的 Unique Face Accuracy 从基线 Flux-Dev 的 48.2% 跃升至 98.6%，Global Identity Spread 从 50.5% 提升至 98.3%，Count Accuracy 从 70.8% 提升至 92.4%（Table 1）。人类偏好研究进一步证实，UFA 指标与人类对身份多样性的判断相关性达到 1.0（Appendix E.1.6），验证了指标设计的有效性。



DISCO 的整体训练流程围绕 **Flow-GRPO（流匹配组相对策略优化）** 构建，通过对预训练文本到图像模型进行强化学习微调，直接优化多人场景中的身份多样性。如图 3 所示，系统由四个核心模块串联构成闭环。

**输入**：一个描述多人场景的文本提示 $c$，以及从课程学习调度器中采样的人数分布 $p_t(n)$。

**生成与采样**：基础模型（如 FLUX-Dev 或 Krea-Dev）在给定提示 $c$ 下生成一组 $M$ 张图像 $\{x_1, \dots, x_M\}$。训练时使用较少的去噪步数 $K_{\mathrm{train}} \ll K_{\mathrm{test}}$ 以提高效率，测试时恢复完整步数。

**奖励计算**：每张图像 $x_i$ 和整个图像组 $G$ 经过四条并行的评估管线：
1. **面部检测与嵌入**：RetinaFace 检测人脸，ArcFace 提取面部嵌入向量 $f_{i,j}$。
2. **图像内多样性奖励** $r_{\mathrm{img}}^d$：惩罚同一图像内人脸嵌入的最大余弦相似度（Eq. 4）。
3. **群体多样性奖励** $r_{\mathrm{grp}}^d$：基于反事实贡献——计算移除图像 $i$ 后群体身份相似度的变化 $\Delta_i$，经 sigmoid 映射为奖励信号（Eq. 6）。
4. **计数准确性奖励** $r_{\mathrm{img}}^c$：检测人脸数 $m_i$ 与提示中目标人数 $N_{\mathrm{target}}$ 相等时给予 1，否则为 0（Eq. 7）。
5. **HPS 质量奖励** $r_{\mathrm{img}}^q$：将 HPSv3 分数线性归一化到 $[0,1]$，保持图像质量和提示遵循能力（Eq. 8）。

四条奖励按权重 $\alpha, \beta, \gamma, \zeta$ 组合为标量奖励 $r(\tau_i, c, G)$（Eq. 3）。

**策略优化**：在组内计算归一化优势 $\tilde{A}_i$，通过 GRPO 目标函数最大化期望优势加权对数概率，同时施加与参考策略 $\pi_{\theta_{\mathrm{ref}}}$ 的 KL 散度惩罚以防止策略崩溃（Eq. 1–2）。

**课程学习调度**：训练初期从简单分布（2–4 人）采样提示，逐步退火至均匀分布（2–$N_{\max}$ 人），稳定训练过程并逐步提升难度（Eq. 9–10）。

整个框架的核心机制在于：**图像内多样性奖励解决单张图像中的人脸重复问题，群体多样性奖励通过跨样本反事实约束防止全局身份崩溃，计数和质量奖励则防止模型通过减少人脸数或降低质量来“奖励黑客”**。消融实验（Table 2）证实，逐步添加这四个组件可持续提升 Count Accuracy、UFA 和 GIS，缺一不可。

### 补充图表

![[assets/figures/papers/paper_list_l2340_https_arxiv_org_abs_2510_01399/figures/003_Figure_3.jpg]]
*Figure 3: DISCO training overview. Our method fine-tunes text-to-image models using Flow-GRPO with a compositional reward. Given a prompt, the model generates a group of images evaluated by four components: (1) Intra-Image Diversity penalizes duplicate identities within images, (2) Group-wise Diversity promotes variation across the group, (3) Count Accuracy enforces correct person count, and (4) HPS Quality ensures prompt alignment and quality. The combined reward guides GRPO updates to improve identity diversity*

![[assets/figures/papers/paper_list_l2340_https_arxiv_org_abs_2510_01399/figures/002_Figure_2.jpg]]
*Figure 2: DISCO enables better multi-human generation. (a) SOTA methods often produce duplicate or inconsistent faces, while (b) DISCO generates distinct, diverse identities. (c) Quantitative results show clear gains in Count Accuracy, Unique Face Accuracy, Identity Spread, and Overall quality(HPSv2 score)*



DISCO 的核心架构围绕**Flow-GRPO 微调框架**展开，通过组合奖励函数引导流匹配模型学习身份多样性。整个训练管线包含四个关键模块，如 Figure 3 所示。

### 3.1 组相对策略优化（GRPO）

DISCO 采用 GRPO 作为训练框架。对于每个提示 $c$，模型从当前策略 $\pi_\theta$ 中采样一组 $M$ 条轨迹 $\{\tau_i\}_{i=1}^M$，每条轨迹对应一张生成图像。组归一化优势函数为：

$$\tilde{A}_i = \frac{r(\tau_i, c) - \mu_c}{\sigma_c}$$

其中 $\mu_c$ 和 $\sigma_c$ 为该组内奖励的均值和标准差。GRPO 优化目标为：

$$\max_{\theta} \mathbb{E}_c \left[ \frac{1}{M} \sum_{i=1}^M \tilde{A}_i \log \pi_{\theta}(\tau_i \mid c) \right] - \beta_{KL} \mathbb{E}_c \left[ \mathrm{KL}(\pi_{\theta}(\cdot \mid c) \| \pi_{\theta_{\mathrm{ref}}}(\cdot \mid c)) \right]$$

该目标最大化期望优势加权对数概率，同时通过 KL 散度惩罚项约束当前策略不偏离参考策略 $\pi_{\theta_{\mathrm{ref}}}$ 过远。为提升效率，训练时使用较少的去噪步数 $K_{\mathrm{train}} \ll K_{\mathrm{test}}$，测试时恢复完整调度。

### 3.2 组合奖励函数

总奖励由四个组件加权求和构成：

$$r(\tau_i, c, G) = \alpha r_{\mathrm{img}}^d(x_i) + \beta r_{\mathrm{grp}}^d(x_i, G) + \gamma r_{\mathrm{img}}^c(x_i) + \zeta r_{\mathrm{img}}^q(x_i)$$

其中 $x_i$ 为轨迹 $\tau_i$ 对应的生成图像，$G$ 为同提示下的图像组，$\alpha, \beta, \gamma, \zeta$ 为各奖励权重。

#### 图像内多样性奖励（Intra-Image Diversity）

该奖励惩罚同一图像内人脸的高相似度。首先使用 **RetinaFace** 检测人脸，再用 **ArcFace** 提取面部嵌入 $\{f_{i,j}\}$，计算任意两脸的余弦相似度 $s(\cdot,\cdot)$：

$$r_{\mathrm{img}}^d(x_i) = \begin{cases} 1 - \max_{j \neq k} s(f_{i,j}, f_{i,k}) & \text{if } m_i \geq 2 \\ 0.5 & \text{if } m_i < 2 \end{cases}$$

其中 $m_i$ 为检测到的人脸数。当人脸数不足 2 时给予中性奖励 0.5。消融实验表明，使用 $\max$ 聚合的效果优于 $\mathrm{mean}$ 和 $\min$ 聚合（Table E.3）。

#### 群体多样性奖励（Group-wise Diversity）

这是 DISCO 的关键创新——**基于反事实贡献的跨样本多样性约束**。定义图像 $x_i$ 移除后群体内最大人脸相似度的变化：

$$\Delta_i = \max_{j \neq k} s(f_{i,j}, f_{i,k}) - \max_{j \neq k, j,k \neq i} s(f_{j}, f_{k})$$

群体多样性奖励为：

$$r_{\mathrm{grp}}^d(x_i, G) = \sigma(-\lambda \Delta_i), \quad \sigma(u) = \frac{1}{1 + e^{-u}}, \lambda = 5$$

当移除某图像后群体相似度下降（$\Delta_i > 0$），说明该图像贡献了多样性，获得高奖励；反之则受惩罚。该机制直接抑制跨样本身份复制，是解决全局身份多样性崩溃的核心因果杠杆。

#### 计数准确性奖励（Count Accuracy）

$$r_{\mathrm{img}}^c(x_i) = \begin{cases} 1 & \text{if } m_i = N_{\mathrm{target}} \\ 0 & \text{otherwise} \end{cases}$$

其中 $N_{\mathrm{target}}$ 为提示中指定的目标人数。该二元奖励强制模型生成正确数量的人脸，防止奖励黑客（如通过减少人脸数来降低相似度）。

#### HPS 质量奖励（HPS Quality）

为保持图像感知质量和提示遵循能力，引入 HPSv3 分数的归一化奖励：

$$\tilde{q}(x_i) = \frac{\mathrm{HPSv3}(x_i) - q_{\mathrm{min}}}{q_{\mathrm{max}} - q_{\mathrm{min}}}$$

其中 $q_{\mathrm{min}}=0, q_{\mathrm{max}}=10$。该组件同时保留并改善了基础模型的组合式指令遵循能力。

### 3.3 课程学习调度

为稳定训练，DISCO 采用单阶段课程学习策略。训练初期从简单分布（2-4 人场景）采样提示，逐步退火至全范围均匀分布：

$$p_t(n) = \begin{cases} p_{\mathrm{ann}}(n,t) & \text{if } t \le t_{\mathrm{curriculum}} \\ p_{\mathrm{uni}}(n) & \text{if } t > t_{\mathrm{curriculum}} \end{cases}$$

其中 $p_{\mathrm{ann}}(n,t)$ 为退火分布，$p_{\mathrm{uni}}(n)$ 为 $[2, N_{\max}]$ 上的均匀分布。消融实验证实课程学习对专家模型（Krea-Dev）尤其有效，简单集边界为 2-4 时在 UFA 和 GIS 之间取得最佳平衡（Table E.5）。

### 补充图表

![[assets/figures/papers/paper_list_l2340_https_arxiv_org_abs_2510_01399/figures/010_Table.jpg]]
*Table: E.3. Comparison of aggregation functions for intra-image diversity reward computation. Results show performance on Flux-Krea baseline. Blue represents the selected aggregation function*

![[assets/figures/papers/paper_list_l2340_https_arxiv_org_abs_2510_01399/figures/013_Table.jpg]]
*Table: E.5. Ablation on curriculum simple-set bounds on Flux-Krea baseline. Blue row is the selected configuration*



## 实验与关键发现

### 核心瓶颈与评估体系

现有多人文本到图像模型在生成“一群人”时普遍陷入**身份危机**：同一图像内的人脸高度重复，跨样本间身份复制严重，且人数计数频繁出错。其根本原因在于，这些模型在训练或微调过程中缺乏对身份多样性的显式建模——仅靠扩散/流匹配的去噪目标无法自然约束人脸嵌入空间的分布。因此，**仅优化图像内多样性无法解决全局身份多样性崩溃**，必须同时引入跨样本的多样性约束。

为系统量化这一瓶颈，本文构建了三个核心指标（详见附录C）：

- **Count Accuracy**：检测人脸数与提示中目标人数相等的图像占比；
- **Unique Face Accuracy (UFA)**：不存在重复人脸的图像占比；
- **Global Identity Spread (GIS)**：数据集中唯一身份簇数量与总请求人数之比。

其中，UFA 与人类对身份多样性的判断相关性达到 **1.0**（附录 E.1.6，图 E.2），表明该指标可作为可靠的自动评估代理。

### 主实验结果

**Table 1** 给出了 DISCO 在 DiverseHumans-TestPrompts（2-7人）和 MultiHuman-TestBench（1-5人）两个基准上的全面对比。DISCO(Flux) 在所有指标上均大幅超越基线模型 FLUX-Dev：

| 基准 | 指标 | DISCO(Flux) | FLUX-Dev | 提升 |
|------|------|-------------|----------|------|
| DiverseHumans-TestPrompts | Count Accuracy | **92.4** | 70.8 | +21.6 |
| DiverseHumans-TestPrompts | UFA | **98.6** | 48.2 | +50.4 |
| DiverseHumans-TestPrompts | GIS | **98.3** | 50.5 | +47.8 |
| MultiHuman-TestBench | Count Accuracy | **86.6** | 61.8 | +24.8 |
| MultiHuman-TestBench | UFA | **94.3** | 56.5 | +37.8 |

DISCO(Flux) 的 **98.6% UFA** 和 **98.3% GIS** 表明，经过 GRPO 微调后，模型几乎完全消除了图像内和跨样本的身份重复问题。值得注意的是，DISCO 甚至超越了闭源商业模型 GPT-Image-1（UFA 85.1%，GIS 89.8%），同时保持了与基线相当的 HPSv2 感知质量分数。

在专家模型 FLUX-Krea 上应用 DISCO 同样取得显著提升，验证了方法对基础模型选择的鲁棒性。Figure 4 的视觉对比进一步显示，DISCO 生成的多人图像中人脸特征各异，且能准确遵循提示中的计数要求，而基线模型则频繁出现“同一张脸复制多次”的现象。

![[assets/figures/papers/paper_list_l2340_https_arxiv_org_abs_2510_01399/figures/005_Figure_4.jpg]]
*Figure 4: DISCO vs. Related Work DISCO finetuning improves performance over current SOTA methods to consistently generate accurate number of people without overlapping identity. It also maintains high perceptual quality while accurately following input prompts*

### 消融研究：组件贡献的因果链

**Table 2** 的渐进式消融揭示了各奖励组件的因果贡献。以 FLUX-Krea 为基线逐步添加 DISCO 组件：

1. **仅图像内多样性奖励**：UFA 显著改善，但 GIS 急剧崩溃——模型学会了在单张图像内生成不同人脸，却将同一组“多样性面孔”复制到所有样本中。这验证了核心洞察：**单独的图像内多样性约束不足以解决全局身份多样性问题**。

2. **加入群体多样性奖励**：GIS 大幅恢复，证明跨样本的反事实惩罚是打破“全局身份模板化”的关键控制旋钮。

3. **加入计数准确性奖励**：Count Accuracy 提升至接近上限，说明显式的计数监督有效防止了模型在追求多样性时“偷懒”生成错误人数。

4. **加入 HPS 质量奖励**：在保持身份多样性的同时，维持甚至提升了图像的感知质量和提示遵循能力，防止了奖励黑客行为（如生成模糊但“多样”的人脸）。

关于聚合函数的消融（Table E.3）表明，图像内多样性奖励使用 **max()** 聚合（惩罚最大余弦相似度）的效果优于 mean() 和 min()，因为 max() 直接针对最相似的人脸对施加压力，驱动力更强。

### 课程学习与训练策略

课程学习策略对专家模型的稳定性至关重要。Table E.5 的消融显示，将简单集边界设为 **2-4 人**时，UFA 和 GIS 达到最佳平衡。课程学习通过从简单分布退火到均匀分布（Eq. 9-10），使模型先掌握少人场景的多样性生成，再逐步泛化到更复杂的多人场景，避免了训练初期的奖励稀疏问题。

此外，DISCO 的 GRPO 框架在收敛速度和最终性能上均优于在线 SFT（Table E.4）：DISCO 仅需 **13 小时**达到最优，而 SFT 需要 33 小时，且 UFA 和 GIS 均显著更高。这表明，相对策略优化的探索机制比监督微调更适合多样性目标的优化。

### 失败模式与局限性

尽管 DISCO 在主要基准上表现优异，仍需注意以下边界条件：

- **检测管线依赖性**：方法依赖 RetinaFace 人脸检测和 ArcFace 嵌入相似度，在严重遮挡、极端姿态或小人脸（如远距离场景）下性能可能下降。这是当前管线的固有局限，而非奖励设计的缺陷。
- **非人脸属性的未覆盖**：DISCO 未显式训练人物属性（如服装、体型）的多样性控制，但 HPSv3 奖励可部分保留基础模型的提示遵循能力，间接维持这些属性的合理分布。
- **非个性化方法**：DISCO 仅适用于通用多人文本到图像生成，不涉及特定身份保持；个性化扩展见并发工作 Ar2Can。

### 公平性与泛化

DISCO 的训练仅使用合成提示，未使用任何真实身份数据，训练数据覆盖多种族、多场景，有助于生成更包容的视觉内容。附录 Table E.1 进一步显示，DISCO 在不同多样性标签条件下（无标签、“多样化面孔”、单一种族、个体属性分配）均保持一致的性能优势，表明方法对不同多样性规格具有良好的泛化能力。

### 补充图表

![[assets/figures/papers/paper_list_l2340_https_arxiv_org_abs_2510_01399/figures/004_Table_1.jpg]]
*Table 1: Multi-Human Generation Evaluation. Results with * are possibly misleading, as the same MLLM is being probed to perform Generation and act as a judge. Green scores indicate the highest results and Red scores indicate the lowest results*

![[assets/figures/papers/paper_list_l2340_https_arxiv_org_abs_2510_01399/figures/007_Table_2.jpg]]
*Table 2: Ablation Study: Progressive Addition of DISCO Components on Flux-Krea baseline*

![[assets/figures/papers/paper_list_l2340_https_arxiv_org_abs_2510_01399/figures/006_Figure.jpg]]
*Figure: b) Count Accuracy*

![[assets/figures/papers/paper_list_l2340_https_arxiv_org_abs_2510_01399/figures/012_Table.jpg]]
*Table: E.4. RL vs. online SFT on Flux-Dev. DISCO outperforms the SFT baseline on identity diversity and perceptual quality, while converging significantly faster*

![[assets/figures/papers/paper_list_l2340_https_arxiv_org_abs_2510_01399/figures/015_Figure.jpg]]
*Figure: E.2. User preference study results. Each point represents one image from a pair, plotted by its mean and max pairwise cosine face similarity. Green points are the images humans collectively judged as more diverse (lower similarity); red points are the images they judged as less diverse. The two clusters separate naturally in the 2D metric space, confirming that mean and max cosine similarity jointly align with human perception of identity diversity*

![[assets/figures/papers/paper_list_l2340_https_arxiv_org_abs_2510_01399/figures/008_Table.jpg]]
*Table: E.1. Performance across diversity tags (D=1: No tag, D=2: ”Diverse faces”, D=3: Single ethnicity, D=4: Individual assignments). DisCo shows consistent improvements across all diversity specifications. Green scores indicate the highest results and Red scores indicate the lowest results*

![[assets/figures/papers/paper_list_l2340_https_arxiv_org_abs_2510_01399/figures/009_Table.jpg]]
*Table: E.2. Ablation study on reward weight parameters. Results are for DisCo(Flux-Dev). Each row shows the effect of different weight configurations on overall performance metrics. Our selected hyperparameter configuration is represented in the Blue row*



## 定位与知识库关联

### 问题定位：身份危机的本质

现有文本到图像模型在多人生成中普遍存在“身份危机”（Identity Crisis），表现为三类典型失败模式：**同一图像内人脸重复**（身份合并）、**跨样本身份复制**（生成多样性崩溃）以及**计数错误**（生成人数与提示不符）。这一问题的根本瓶颈在于，当前扩散/流匹配模型缺乏对身份多样性的显式建模——即使通过提示工程（如添加“diverse faces”标签）或后处理手段优化图像内多样性，也无法解决跨样本的全局身份多样性崩溃。

DISCO 将这一问题重新定义为强化学习框架下的**约束优化问题**：在微调过程中同时施加图像内和跨样本的身份多样性约束，并引入计数和质量控制以防止奖励黑客（reward hacking）。

### 方法谱系

#### 基线模型

DISCO 的微调起点包括三类文本到图像模型：
- **FLUX-Dev**：开源流匹配模型，作为通用基线；
- **Krea-Dev**：在 FLUX-Dev 基础上针对多人场景微调的专家模型；
- **SD3.5**：开源扩散模型，用于验证方法跨架构的泛化性。

这些基线模型在 DiverseHumans-TestPrompts 上的 Unique Face Accuracy (UFA) 仅为 48.2%（FLUX-Dev），Global Identity Spread (GIS) 为 50.5%，计数准确率 70.8%，反映了现有方法在身份多样性上的系统性缺陷。

#### 与现有工作的关系

DISCO 的方法论定位可从以下几个维度理解：

**1. 与提示工程方法的区别。** 现有工作通常依赖提示中显式指定多样性标签（如“diverse faces”、“different ethnicities”）来缓解身份重复。实验表明（Table E.1），这类方法虽能带来边际改善，但无法从根本上解决跨样本的身份复制问题——GIS 指标在添加“diverse faces”标签后提升有限，且高度依赖提示设计的质量。

**2. 与个性化生成方法的边界。** DISCO 明确区别于个性化文本到图像生成（如 DreamBooth、IP-Adapter 等），后者旨在保持特定身份的一致性，而 DISCO 追求的是**身份多样性最大化**。论文指出，将 DISCO 扩展到个性化场景的并发工作为 Ar2Can，但 DISCO 本身不涉及任何真实身份数据训练。

**3. 与强化学习微调方法的关联。** DISCO 采用 Group-Relative Policy Optimization（GRPO）作为训练框架，这一选择与近期在语言模型中广泛应用的组相对策略优化方法一脉相承。GRPO 的核心优势在于利用组内奖励归一化消除绝对奖励尺度的影响，使得跨提示的训练信号更加稳定。

**4. 与多样性优化方法的差异。** 传统多样性优化通常聚焦于图像内的特征分散度（如通过最大均值差异或余弦相似度惩罚）。DISCO 的关键创新在于引入了**群体多样性奖励**（group-wise diversity reward）——一种基于反事实贡献的跨样本多样性约束：对于每张生成图像，计算将其从批次中移除后全局相似度的变化量，以此作为该图像对群体多样性贡献的代理信号。这一设计使得模型不仅学会在同一图像内生成不同身份，还学会在整个生成批次中避免身份重复。

### 适用边界与局限

**技术依赖边界。** DISCO 的奖励计算依赖 RetinaFace 进行人脸检测、ArcFace 提取面部嵌入。在严重遮挡、极端姿态或小人脸（如远距离场景）下，检测和嵌入质量可能显著下降，导致奖励信号噪声增加。论文未对此类边缘场景进行系统性评估。

**属性覆盖范围。** DISCO 当前仅针对**面部身份**多样性进行优化，未显式控制人物属性（如服装、体型、发型）。虽然 HPSv3 质量奖励可间接保留基础模型的提示遵循能力，但无法保证非面部属性的多样性。论文在 4.2.3 节展示了将奖励框架推广到其他视觉属性的初步结果，但这一方向仍处于探索阶段。

**任务范围限制。** DISCO 仅适用于文本到图像生成任务，不涉及视频生成中的时空一致性、3D 生成中的多视角一致性等扩展场景。

**公平性考量。** 论文强调 DISCO 仅使用合成提示训练，未使用任何真实身份数据，且训练数据覆盖多种族、多场景。然而，多样性优化可能因基础模型本身的偏见而产生新的分布偏移——例如，基础模型对特定种族面部特征的表征能力差异可能被奖励信号放大。论文未对此进行深入分析。

### 开放问题

1. **属性泛化。** 如何将身份多样性优化框架扩展到全身外观提示（服装、体型、姿态）的显式控制，同时避免不同属性维度间的冲突？

2. **时空扩展。** 在视频生成中，身份多样性需与时序一致性联合优化——如何定义和平衡帧内多样性与帧间一致性约束？

3. **鲁棒性边界。** 在极端遮挡、极小脸部（如人群远景）或非正面姿态下，当前检测/嵌入管线的性能退化对最终生成质量的影响程度如何？是否存在替代的人脸表征方案（如基于 CLIP 的全局面部特征）？

4. **公平性与偏见。** 如何引入更显式的公平性约束（如人口统计平衡目标）以防止多样性优化过程中产生新的表征偏见？基础模型在不同种族、性别、年龄群体上的先验差异如何影响 DISCO 的优化结果？

5. **效率与规模化。** 群体多样性奖励的计算复杂度随批次大小线性增长，在更大规模训练中如何保持计算效率？课程学习策略的退火参数是否需要在不同基础模型间重新调优？



## 原文 PDF

![[paperPDFs/CVPR_2026/Resolving_the_Identity_Crisis_in_Text_to_Image_Generation.pdf]]
