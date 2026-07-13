---
title: "OraPO: Oracle-educated Reinforcement Learning for Data-efficient and Factual Radiology Report Generation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/OraPO_Oracle_educated_Reinforcement_Learning_for_Data_efficient_and_Factual_Radiology_Report_Generation.pdf
project_link: null
code_link: null
aliases:
- OOEG
- OraPO
tags:
- CVPR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 引入基于零奖励率（ZRR）的自适应混合权重，当GRPO探索失败时，动态增加DPO损失权重，将失败生成作为负例、真实报告作为正例进行直接偏好优化，从而将无效rollout转化为有效监督信号。
primary_logic: 通过将GRPO的探索失败转化为DPO的偏好对，无需额外数据或模型，即可在极低数据预算（1K样本）下实现高效的RL训练，同时配合事实级奖励（FactS）确保临床准确性。
claims:
- OraPO大幅降低零奖励组比例，且对Pneumonia和Fracture等困难类别的F1提升更早、更高。
- 在CheXpert Plus上仅用1K训练样本达到SOTA F1=0.341，而最佳基线MambaXray-L使用1.27M样本仅得F1=0.335。
- 添加FactS奖励使F1从0.089提升至0.291（+227%），配合OraPO进一步达到0.341。
- 在MIMIC-CXR上同样以1K样本取得F1=0.357，优于使用完整223K样本的多个基线。
---

# OraPO: Oracle-educated Reinforcement Learning for Data-efficient and Factual Radiology Report Generation

> [!tip] 核心洞察
> 通过将GRPO的探索失败转化为DPO的偏好对，无需额外数据或模型，即可在极低数据预算（1K样本）下实现高效的RL训练，同时配合事实级奖励（FactS）确保临床准确性。

| 字段 | 内容 |
|------|------|
| 中文题名 | OraPO：面向数据高效与事实性放射学报告生成的Oracle指导强化学习 |
| 英文题名 | OraPO: Oracle-educated Reinforcement Learning for Data-efficient and Factual Radiology Report Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2509.18600) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | OraPO (Oracle-educated GRPO) |
| Dataset | CheXpert Plus, MIMIC-CXR, CheXpert validation set |

> [!tip] 效果简介
> - CheXpert Plus (macro-averaged over 14 labels) 上，Precision / Recall / F1 0.237 / 0.832 / 0.341 vs 0.377 / 0.319 / 0.335 (MambaXray-L, 1.27M samples) (Precision -0.140, Recall +0.513, F1 +0.006)。
> - MIMIC-CXR (macro-averaged over 14 labels) 上，Precision / Recall / F1 0.242 / 0.891 / 0.357 vs 0.275 / 0.248 / 0.260 (R2GenGPT, 223K samples) (Precision -0.033, Recall +0.643, F1 +0.097)。
> - CheXpert validation set (gold labels) 上，Precision / Recall / F1 0.234 / 0.641 / 0.288 vs 0.375 / 0.305 / 0.253 (GPT-4.1 with prompt engineering) (Precision -0.141, Recall +0.336, F1 +0.035)。

## 概要

放射学报告生成（RRG）旨在自动从胸部X光片生成描述性临床报告，其核心瓶颈在于视觉-语言模型（VLM）缺乏领域知识，导致强化学习（RL）训练中大量采样组获得全零奖励——在训练早期约30%的批次无法产生有效梯度信号，造成计算资源浪费与收敛缓慢。

**OraPO**（Oracle-educated GRPO）针对这一瓶颈提出了一个简洁而高效的解决方案：当GRPO的探索失败（即采样组内所有报告奖励均为零）时，动态触发轻量级DPO更新，将这些无效生成作为负例、真实报告作为正例进行直接偏好优化。其核心洞察在于——**将RL的探索失败转化为偏好学习的监督信号**，无需额外数据或模型即可实现高效的RL训练。

方法层面，OraPO引入了三个关键组件：

- **零奖励率（ZRR）自适应混合**：实时监测每个prompt的零奖励完成比例，通过EMA平滑后映射为动态混合权重$w_i^{(t)}$，在GRPO探索失败时自动增加DPO损失权重，实现从“教育”（DPO）到“探索”（GRPO）的自然过渡。
- **FactScore（FactS）稠密奖励**：从生成报告中提取原子临床事实，进行标签级蕴含验证，计算$F_\beta$分数作为稠密、可解释的句子级奖励，替代传统的标量准确率奖励，使临床有效性F1从0.089跃升至0.291（+227%）。
- **自适应损失混合**：$\mathcal{L}_{\text{OraPO}} = \frac{1}{B} \sum_i [(1-w_i)\mathcal{L}_{\text{GRPO}} + w_i\mathcal{L}_{\text{DPO}}]$，将GRPO的组归一化优势估计与DPO的偏好优化统一在单一目标中。

在数据效率方面，OraPO展现出显著优势：**仅使用1K训练样本**（不足最佳基线MambaXray-L所用1.27M样本的0.1%），在CheXpert Plus上取得F1=0.341的SOTA性能，召回率高达0.832（相对MambaXray-L提升160.8%）；在MIMIC-CXR上同样以1K样本取得F1=0.357，优于使用完整223K样本的R2GenGPT等基线。消融实验进一步表明，仅用400个训练样本时OraPO+FactS已取得F1=0.296，超过仅用FactS的1K样本结果（0.289），验证了其极低数据预算下的有效性。

**方法定位**：OraPO属于RL-based RRG方法，其核心贡献在于通过ZRR自适应混合机制将GRPO与DPO有机结合，配合事实级奖励设计，在数据高效与临床事实性两个维度上实现了突破。与依赖大规模监督微调（SFT）的传统方法（如R2GenGPT）和纯GRPO方法相比，OraPO在极低数据预算下展现出更强的探索效率与临床准确性。



### 放射学报告生成的任务困境

放射学报告生成（Radiology Report Generation, RRG）旨在从胸部X光片自动生成描述性诊断报告，其核心挑战在于临床事实的准确性——模型不仅需要生成流畅的自然语言，更必须正确识别并描述图像中的病理发现。然而，现有主流范式面临双重瓶颈：

**数据饥渴与计算密集。** 当前最优的RRG系统通常依赖大规模标注数据进行多阶段训练。例如，先前SOTA模型 **MambaXray-L**（Wang et al., CVPR 2025）使用了127万训练样本，而代表性监督微调（SFT）基线 **R2GenGPT** 也需要完整的223K样本才能在MIMIC-CXR上取得可用性能。这种数据依赖不仅限制了RRG在低资源场景下的部署，也使得模型迭代成本高昂。

**奖励信号稀疏与无效探索。** 将强化学习（特别是GRPO）引入RRG面临一个根本性困难：基础视觉语言模型（VLM）在训练初期缺乏足够的领域知识，导致大量采样组（group）获得全零奖励。论文数据显示，在训练早期，约30%的batch其组内平均奖励为零。这些零奖励组在标准GRPO框架下不产生有效梯度，造成计算资源浪费和收敛缓慢——模型在“盲目探索”中消耗了大量算力却无法获得有意义的监督信号。

### 现有方法的缺口

当前RRG的强化学习方案存在两个关键盲区：

1. **无效rollout的浪费。** 标准GRPO（naïve GRPO）仅依赖组内相对优势进行策略更新，当一组K个采样报告全部获得零奖励时，该组完全被丢弃，不贡献任何学习信号。这意味着模型从失败中无法学习——它不知道“错在哪里”，只能等待偶然采样到正向奖励的组。

2. **奖励信号的粗糙性。** 传统方案使用标量准确率或文本相似度（如CIDEr、BLEU）作为奖励，这类指标无法捕捉细粒度的临床事实正确性。一个报告可能因整体措辞与参考报告相似而获得高分，却在关键病理发现上出现假阳性或漏诊。

### 本文动机

针对上述缺口，本文提出 **OraPO（Oracle-educated GRPO）**，核心动机是将GRPO的探索失败转化为有效的监督信号，从而在极低数据预算下实现高效的RL训练。具体而言：

- **变废为宝：** 当GRPO采样组全零奖励时，OraPO触发轻量级DPO更新，将失败生成作为负例、真实报告作为正例构成偏好对，直接教导模型远离低质量生成。这一机制无需额外数据或模型，仅利用原本被丢弃的无效rollout。

- **事实级奖励：** 引入FactScore（FactS）奖励，通过提取原子临床事实并进行标签级蕴含验证，提供稠密、可解释的句子级奖励信号，确保优化目标与临床准确性对齐。

- **自适应混合：** 通过零奖励率（Zero-Reward Rate, ZRR）动态控制GRPO与DPO损失的混合权重，实现从“教育”（DPO主导）到“探索”（GRPO主导）的自然过渡——当模型频繁失败时加强DPO引导，当模型逐渐掌握领域知识后逐步让位于GRPO的自主探索。

这一设计使得OraPO仅需1K训练样本即可在CheXpert Plus上达到F1=0.341，超越使用1.27M样本的先前SOTA，同时将召回率从0.319提升至0.832（+160.8%），展示了在严格数据和计算预算下的显著优势。



## 核心方法与创新机理

OraPO 的核心创新在于识别并解决了原始 GRPO 在放射学报告生成（RRG）中的一个关键瓶颈：**基础 VLM 缺乏领域知识导致大量组奖励全为零，产生无效梯度，浪费计算资源且收敛缓慢**。针对此，OraPO 提出了三个紧密耦合的 changed slots，形成从“探索失败检测”到“失败信号转化”再到“事实级稠密奖励”的完整闭环。

### 1. 自适应混合学习目标：从纯探索到“教育-探索”协同

原始 GRPO 采用纯 GRPO 损失（仅含 KL 正则项），当组内所有采样报告均获零奖励时，该组对梯度无任何贡献，成为无效计算。OraPO 的核心机制是通过**零奖励率（Zero-Reward Rate, ZRR）**动态控制 GRPO 与 DPO 损失的混合权重：

$$z_i = \frac{1}{K} \sum_{j=1}^{K} \mathbf{1}[r_{i,j} = 0]$$

$$\tilde{z}_i^{(t)} = \alpha \tilde{z}_i^{(t-1)} + (1-\alpha) z_i^{(t)}$$

$$w_i^{(t)} = \mathrm{clip}\Big( w_{\mathrm{min}} + (w_{\mathrm{max}} - w_{\mathrm{min}}) \big[\tilde{z}_i^{(t)} \big]^\gamma, w_{\mathrm{min}}, w_{\mathrm{max}} \Big)$$

最终 OraPO 总损失为：

$$\mathcal{L}_{\mathrm{OraPO}} = \frac{1}{B} \sum_{i=1}^{B} \Big[ \big(1 - w_i^{(t)}\big) \mathcal{L}_{\mathrm{GRPO}}(x_i, p_i) + w_i^{(t)} \mathcal{L}_{\mathrm{DPO}}(x_i, p_i) \Big]$$

**关键机制**：当 GRPO 探索成功（ZRR 低）时，DPO 权重趋近于 $w_{\mathrm{min}}$，模型以自主探索为主；当 GRPO 频繁失败（ZRR 高，如训练早期约 30% 的组全为零奖励）时，DPO 权重自动升高，模型从“教育信号”中学习。Fig. 2（左）证实，OraPO 比 naïve GRPO 更快、更彻底地抑制了零奖励组比例，验证了该自适应策略的有效性。

### 2. 无效 Rollout 的价值转化：从丢弃到负例偏好学习

原始 GRPO 直接丢弃零奖励组，这些失败生成不产生任何梯度贡献。OraPO 将这些**零奖励 rollout 作为 DPO 的负例（dispreferred completion），与真实报告（正例）构成偏好对**，驱动策略远离低质量生成：

$$\mathcal{L}_{\mathrm{DPO}} = -\mathbb{E}\Big[\log \sigma\big( \tau (\Delta^+ - \Delta^-) \big)\Big]$$

其中 $\Delta^+ = \log \pi_\theta(y^+ \mid x, p) - \log \pi_{\mathrm{ref}}(y^+ \mid x, p)$，$\Delta^-$ 同理。这一设计无需额外数据或模型，将原本浪费的计算资源转化为有效的监督信号。消融实验（Table 4）提供了决定性证据：将 DPO 替换为 SFT（GRPO+SFT variant）导致性能崩溃——召回从 0.832 降至 0.176，F1 从 0.341 降至 0.106，证明 DPO 的偏好对比机制（而非简单的监督模仿）是 OraPO 成功的关键。

### 3. 事实级稠密奖励：从标量准确率到原子事实蕴含验证

原始 GRPO 使用标量准确率/相似度奖励，信号稀疏且无法区分部分正确的生成。OraPO 引入 **FactScore-based F-β 奖励（FactS）**，将生成报告分解为原子临床事实，进行标签级蕴含验证：

$$\mathcal{F}(\hat{y}_i) = \{ s_{i,k} \}_{k=1}^{K_i}$$

$$\hat{z}_{i,\ell} = \mathbf{1}[ \exists s \in \mathcal{F}(\hat{y}_i) \text{ s.t. } \mathrm{entails}(s, \ell) = \mathrm{true} ]$$

$$r(x_i, \hat{y}_i) = F_{\beta, i} = \frac{ (1+\beta^2) P_i R_i }{ \beta^2 P_i + R_i + \xi }$$

**因果效应**：Table 4 的消融实验显示，将 FactS 引入 vanilla GRPO 使 F1 从 0.089 提升至 0.291（+227%），召回从 0.162 升至 0.605（+274%）。在此基础上加入 DPO（即完整 OraPO）进一步将 F1 推至 0.341，召回至 0.832。这一递进关系表明，FactS 提供了必要的稠密学习信号，而 OraPO 的自适应 DPO 机制则将这些信号更高效地转化为策略改进。

### 创新协同效应

三个 changed slots 并非独立运作，而是形成因果链：FactS 提供细粒度奖励，使 ZRR 能更精确地反映探索质量；ZRR 驱动的自适应权重确保 DPO 在模型最需要指导时介入；DPO 的偏好学习则将 FactS 信号与失败经验共同转化为策略更新。这一协同使 OraPO 在仅 1K 训练样本下即达到 SOTA——CheXpert Plus 上 F1=0.341，超过使用 1.27M 样本的 **MambaXray-L**（Wang et al., CVPR 2025）的 0.335；MIMIC-CXR 上 F1=0.357，超过使用 223K 样本的多个基线。



OraPO（Oracle-educated GRPO）提出了一种面向放射学报告生成（RRG）的数据高效强化学习范式。其核心动机源于一个关键瓶颈：**原始GRPO在基础视觉语言模型（VLM）缺乏领域知识时，会产生大量全零奖励的采样组**——在训练早期约30%的组内所有rollout奖励均为零（Fig. 2左），导致无效梯度，浪费计算资源且收敛缓慢。

OraPO的整体pipeline由**四个核心模块**构成，形成“探索—检测—教育—评估”的闭环：

### 1. GRPO采样与组归一化优势计算（探索模块）

对于每个输入影像-提示对 $(x_i, p_i)$，模型采样 $K$ 个候选报告 $\{\hat{y}_{i,j}\}_{j=1}^K$，计算每个候选的标量奖励 $r_{i,j}$，并在组内进行归一化：

$$\bar{r} = \frac{1}{K} \sum_{j=1}^{K} r_j, \qquad \sigma = \sqrt{\frac{1}{K} \sum_{j=1}^{K} (r_j - \bar{r})^2 + \varepsilon}$$

$$A_j = \frac{r_j - \bar{r}}{\sigma}$$

基于组归一化优势 $A_j$，GRPO通过带裁剪的替代损失更新策略 $\pi_\theta$：

$$\mathcal{L}_{\mathrm{GRPO}} = -\mathbb{E}\Big[\min\left(\rho_j A_j, \mathrm{clip}(\rho_j, 1-\epsilon, 1+\epsilon) A_j\right)\Big] + \lambda_{\mathrm{KL}} \mathbb{E}\big[\mathrm{KL}\big(\pi_\theta(\cdot \mid x, p) \| \pi_{\mathrm{ref}}(\cdot \mid x, p)\big)\big]$$

该模块负责**探索**生成空间，但当基础VLM缺乏领域知识时，大量采样组内所有候选报告的奖励均为零，GRPO损失无法提供有效学习信号。

### 2. 零奖励率（ZRR）计算与EMA平滑（检测模块）

为检测GRPO的探索失败，OraPO引入**零奖励率（Zero-Reward Rate, ZRR）**指标：

$$z_i = \frac{1}{K} \sum_{j=1}^{K} \mathbf{1}[r_{i,j} = 0]$$

$z_i$ 量化单个prompt下零奖励完成的比例。为进一步平滑训练波动，对ZRR施加指数移动平均（EMA）：

$$\tilde{z}_i^{(t)} = \alpha \tilde{z}_i^{(t-1)} + (1-\alpha) z_i^{(t)}$$

平滑后的ZRR $\tilde{z}_i^{(t)}$ 作为**自适应混合权重的控制信号**，决定DPO“教育”模块的介入强度。

### 3. 自适应DPO更新（教育模块）

当ZRR较高（即GRPO探索大面积失败）时，OraPO触发轻量级DPO更新，将**零奖励rollout作为负例（dispreferred）、真实报告作为正例（preferred）**，构成偏好对进行直接偏好优化：

$$\mathcal{L}_{\mathrm{DPO}} = -\mathbb{E}\Big[\log \sigma\big(\tau (\Delta^+ - \Delta^-)\big)\Big]$$

其中 $\Delta^+ = \log \pi_\theta(y^+ \mid x, p) - \log \pi_{\mathrm{ref}}(y^+ \mid x, p)$，$\Delta^-$ 同理。该模块的核心作用是将GRPO的**无效探索转化为有效监督信号**，驱动策略远离低质量生成，无需额外数据或模型。

动态混合权重 $w_i^{(t)}$ 由平滑ZRR通过幂律映射得到：

$$w_i^{(t)} = \mathrm{clip}\Big( w_{\mathrm{min}} + (w_{\mathrm{max}} - w_{\mathrm{min}}) \big[\tilde{z}_i^{(t)} \big]^\gamma, w_{\mathrm{min}}, w_{\mathrm{max}} \Big)$$

$w_i^{(t)}$ 被限制在窄范围（如0.05–0.15），确保DPO始终作为辅助信号，不会压倒GRPO的探索。

### 4. FactScore奖励计算（评估模块）

为提供稠密、可解释的临床奖励，OraPO采用**FactScore-based F-β奖励（FactS）**。该模块首先从生成报告 $\hat{y}_i$ 中提取原子临床事实集合：

$$\mathcal{F}(\hat{y}_i) = \{ s_{i,k} \}_{k=1}^{K_i}$$

随后对每个病理标签 $\ell$ 进行蕴含验证，判断是否存在支持该标签的事实：

$$\hat{z}_{i,\ell} = \mathbf{1}[ \exists s \in \mathcal{F}(\hat{y}_i) \text{ s.t. } \mathrm{entails}(s, \ell) = \mathrm{true} ]$$

最终奖励为基于事实精度 $P_i$ 与召回率 $R_i$ 的F-β分数：

$$r(x_i, \hat{y}_i) = F_{\beta, i} = \frac{ (1+\beta^2) P_i R_i }{ \beta^2 P_i + R_i + \xi }$$

FactS奖励替代了传统GRPO中粗糙的标量准确率奖励，为第1模块的GRPO采样和第3模块的DPO偏好对提供**标签级细粒度监督**。

### 5. OraPO总损失混合

上述模块通过自适应混合权重整合为统一的优化目标：

$$\mathcal{L}_{\mathrm{OraPO}} = \frac{1}{B} \sum_{i=1}^{B} \Big[ \big(1 - w_i^{(t)}\big) \mathcal{L}_{\mathrm{GRPO}}(x_i, p_i) + w_i^{(t)} \mathcal{L}_{\mathrm{DPO}}(x_i, p_i) \Big]$$

当ZRR低时，$w_i^{(t)}$ 接近 $w_{\mathrm{min}}$，训练以GRPO探索为主；当ZRR高时，$w_i^{(t)}$ 增大，DPO“教育”信号增强，将失败生成转化为远离负例的梯度。这种**从教育到探索的自然过渡**是OraPO在极低数据预算（1K样本）下实现高效RL训练的核心机制。

### 输入输出流总结

- **输入**：胸部X光影像 $x_i$ + 任务提示 $p_i$（如“请描述影像中的临床发现”）
- **前向传播**：VLM $\pi_\theta$ 对每个输入采样 $K$ 个候选报告
- **奖励计算**：FactS模块提取原子事实、进行蕴含验证、计算F-β分数
- **ZRR检测**：统计组内零奖励比例，EMA平滑后计算混合权重
- **损失计算与反向传播**：$\mathcal{L}_{\mathrm{OraPO}}$ 混合GRPO与DPO信号，更新 $\pi_\theta$
- **输出**：训练后的VLM可直接生成包含临床发现的放射学报告

关键超参数设置见 **Table 6**，包括 $K=8$、$\beta=0.5$（F-β中偏向召回）、$w_{\mathrm{min}}=0.05$、$w_{\mathrm{max}}=0.15$、$\gamma=2.0$ 等。消融实验（Table 4）证实：用SFT替代DPO（GRPO+SFT变体）会导致性能崩溃（召回降至0.176，F1降至0.106），证明**DPO在OraPO中不可替代**——SFT的正向模仿无法提供DPO特有的“远离负例”梯度信号。

### 补充图表

![[assets/figures/papers/paper_list_l2289_https_arxiv_org_abs_2509_18600/figures/001_Figure_1.jpg]]
*Figure 1: Illustration of mainstream data/compute-intensive pipelines (upper-left) versus our data-efficient pipeline (upper-right). Bottom: on CheXpert Plus [8], our method achieves the SOTA performance for RRG with less than 0.1% of the training samples (vs. 1.27 M) used by best-performing baselines and a much smaller model, demonstrating strong performance under tight data and compute budgets*



### 3.1 基础GRPO：组归一化优势与策略优化

OraPO以Group Relative Policy Optimization（GRPO）为探索基础。GRPO的核心思想是用组内归一化优势替代传统RLHF中的价值函数（critic），从而消除对额外价值网络的依赖。对于每个输入提示（胸部X光图像和任务指令），GRPO采样$K$个候选报告，计算每个候选的奖励$r_j$，然后在组内进行归一化：

$$\bar{r} = \frac{1}{K} \sum_{j=1}^{K} r_j, \qquad \sigma = \sqrt{\frac{1}{K} \sum_{j=1}^{K} (r_j - \bar{r})^2 + \varepsilon}$$

$$A_j = \frac{r_j - \bar{r}}{\sigma}$$

其中$\bar{r}$为组内奖励均值，$\sigma$为组内标准差（含小常数$\varepsilon$防止除零），$A_j$为第$j$个候选报告的组归一化优势。GRPO的策略优化目标为带裁剪的代理损失加KL正则项：

$$\mathcal{L}_{\mathrm{GRPO}} = -\mathbb{E}\Big[\min\left(\rho_j A_j, \mathrm{clip}(\rho_j, 1-\epsilon, 1+\epsilon) A_j\right)\Big] + \lambda_{\mathrm{KL}} \mathbb{E}\big[\mathrm{KL}\big(\pi_\theta(\cdot \mid x, p) \| \pi_{\mathrm{ref}}(\cdot \mid x, p)\big)\big]$$

其中$\rho_j$为当前策略与旧策略的概率比，$\epsilon$控制裁剪范围，$\lambda_{\mathrm{KL}}$控制与参考策略$\pi_{\mathrm{ref}}$的偏离惩罚。

**瓶颈分析**：当基础VLM缺乏领域知识时，GRPO采样的$K$个报告可能全部获得零奖励，导致$\bar{r}=0$、$\sigma\approx\varepsilon$、所有$A_j\approx 0$。此时GRPO损失梯度趋于零，产生无效更新。实验表明，在训练前50步，约30%的组出现全零奖励（Fig. 2左），造成大量计算资源浪费和收敛缓慢。

### 3.2 OraPO核心：零奖励率驱动的自适应DPO教育

OraPO的关键创新在于将GRPO的探索失败转化为有效的监督信号。当一组采样全部获得零奖励时，这些失败生成被作为DPO的负例（dispreferred completion），真实报告作为正例（preferred completion），驱动策略远离低质量生成。

**零奖励率（Zero-Reward Rate, ZRR）**：对第$i$个提示，ZRR定义为该组内零奖励完成的比例：

$$z_i = \frac{1}{K} \sum_{j=1}^{K} \mathbf{1}[r_{i,j} = 0]$$

为稳定训练信号，ZRR通过指数移动平均（EMA）平滑：

$$\tilde{z}_i^{(t)} = \alpha \tilde{z}_i^{(t-1)} + (1-\alpha) z_i^{(t)}$$

**自适应混合权重**：平滑后的ZRR通过幂函数映射为DPO损失的混合权重：

$$w_i^{(t)} = \mathrm{clip}\Big( w_{\mathrm{min}} + (w_{\mathrm{max}} - w_{\mathrm{min}}) \big[\tilde{z}_i^{(t)} \big]^\gamma, w_{\mathrm{min}}, w_{\mathrm{max}} \Big)$$

其中$\gamma$控制映射曲线的陡峭度，$w_{\mathrm{min}}$和$w_{\mathrm{max}}$限定DPO权重的范围（实验中设为0.05和0.15）。当ZRR高时（GRPO探索频繁失败），$w_i^{(t)}$增大，DPO教育信号增强；当ZRR降低时，GRPO自主探索逐渐主导。

**DPO损失**：以真实报告$y^+$为正例、模型生成为负例$y^-$，DPO目标为最大化正负样本的对数概率差：

$$\mathcal{L}_{\mathrm{DPO}} = -\mathbb{E}\Big[\log \sigma\big( \tau (\Delta^+ - \Delta^-) \big)\Big]$$

其中$\Delta^+ = \log \pi_\theta(y^+ \mid x, p) - \log \pi_{\mathrm{ref}}(y^+ \mid x, p)$，$\Delta^- = \log \pi_\theta(y^- \mid x, p) - \log \pi_{\mathrm{ref}}(y^- \mid x, p)$，$\tau$为温度参数。

**OraPO总损失**：将GRPO探索与DPO教育通过ZRR导出的权重自适应混合：

$$\mathcal{L}_{\mathrm{OraPO}} = \frac{1}{B} \sum_{i=1}^{B} \Big[ \big(1 - w_i^{(t)}\big) \mathcal{L}_{\mathrm{GRPO}}(x_i, p_i) + w_i^{(t)} \mathcal{L}_{\mathrm{DPO}}(x_i, p_i) \Big]$$

这一设计实现了从“教育”（DPO主导）到“探索”（GRPO主导）的自然过渡：训练初期ZRR高，DPO权重接近$w_{\mathrm{max}}$，提供强监督信号纠正基础模型的领域无知；随着策略改善，ZRR下降，GRPO逐渐接管，进行细粒度的组内相对优化。

### 3.3 FactScore奖励：原子事实提取与标签级蕴含验证

为解决传统标量奖励（如准确率、相似度）无法提供稠密、可解释的临床反馈的问题，OraPO引入FactScore（FactS）奖励。

**原子事实提取**：从生成报告$\hat{y}_i$中使用GPT-4.1提取原子临床事实集合：

$$\mathcal{F}(\hat{y}_i) = \{ s_{i,k} \}_{k=1}^{K_i}$$

**标签级蕴含验证**：对每个病理标签$\ell$，检查是否存在至少一个原子事实蕴含该标签：

$$\hat{z}_{i,\ell} = \mathbf{1}[ \exists s \in \mathcal{F}(\hat{y}_i) \text{ s.t. } \mathrm{entails}(s, \ell) = \mathrm{true} ]$$

**F-β奖励**：基于事实级精度$P_i$和召回率$R_i$计算F-β分数作为稠密奖励：

$$r(x_i, \hat{y}_i) = F_{\beta, i} = \frac{ (1+\beta^2) P_i R_i }{ \beta^2 P_i + R_i + \xi }$$

其中$\beta$控制精度与召回的权衡（放射学报告生成中偏重召回，$\beta>1$），$\xi$为平滑常数。FactS奖励在句子级别提供可解释的反馈，直接对齐临床诊断证据。

### 3.4 模块协同与训练流程

OraPO的完整训练流程由五个模块协同完成：

1. **GRPO采样与组归一化优势计算**（Eq. 1-4）：每组采样$K$个报告，计算组内相对优势，作为探索信号。
2. **ZRR计算与EMA平滑**（Eq. 8-9）：检测GRPO探索失败程度，为混合权重提供动态信号。
3. **自适应DPO更新**（Eq. 7, 12）：当ZRR高时，以真实报告为正例、失败生成为负例进行偏好优化，将无效rollout转化为有效梯度。
4. **FactScore奖励计算**（Eq. 13-15）：提取原子事实，进行标签级蕴含验证，提供稠密、可解释的临床奖励。
5. **OraPO总损失混合**（Eq. 10-11）：通过ZRR导出的权重动态混合GRPO与DPO损失，实现从教育到探索的自然过渡。

**关键消融证据**：将DPO替换为SFT（即用真实报告做监督微调而非偏好优化）导致性能崩溃——召回率从0.832降至0.176，F1从0.341降至0.106（Table 4末行），证明DPO的对比偏好机制在OraPO中不可替代。SFT仅强化正例，无法有效利用失败生成的负向信号来“推开”策略远离低质量区域。



## 实验与关键发现

### 核心实验设置与对比框架

OraPO的训练仅使用**1K个样本**（从CheXpert Plus训练集中随机采样），在Qwen2.5-VL-3B-Instruct基础模型上进行RL微调。这一数据预算不到先前最佳方法MambaXray-L（使用1.27M样本）的0.1%。评测在三个基准上展开：CheXpert Plus（14个病理标签的macro-average）、MIMIC-CXR、以及CheXpert验证集的人工金标。对比基线涵盖任务专用RRG算法（Table 1）、不同LLM/VLM骨干（Table 2），以及代表性的SFT方法如**R2GenGPT**和**Token-Mixer**（Yang et al., IEEE TMI 2024）。

![[assets/figures/papers/paper_list_l2289_https_arxiv_org_abs_2509_18600/figures/003_Table_1.jpg]]
*Table 1: Experimental results on the CheXpert Plus dataset [8] using task-specific RRG algorithms. We report macro-averaged Precision, Recall, and F1 across 14 CheXpert pathologies. Train Size is the number of training samples. Some baselines train on multiple corpora and/or in multiple stages. Best and second best are in bold and underline, respectively*

![[assets/figures/papers/paper_list_l2289_https_arxiv_org_abs_2509_18600/figures/004_Table_2.jpg]]
*Table 2: Experimental results on the CheXpert Plus benchmark [8] across diverse LLMs/VLMs, all supervised fine-tuned with R2GenGPT [95] on CheXpert Plus. We report macro-averaged Precision, Recall, and F1 across 14 CheXpert pathologies. The Params listed denotes the parameters that need to be tuned in the training phase. FT-Size indicates the number of samples used for fine-tuning. Best and second best are in bold and underline, respectively*

### CheXpert Plus主结果：极致数据效率下的SOTA

Table 1展示了OraPO与任务专用RRG算法的对比。OraPO以**F1=0.341**取得最优，超过此前SOTA **MambaXray-L**（Wang et al., CVPR 2025）的F1=0.335。关键差异在于召回率的巨大提升：OraPO达到**Recall=0.832**，而MambaXray-L仅为0.319（**+160.8%**）。精确率方面OraPO为0.237，低于MambaXray-L的0.377，体现出OraPO倾向于高召回、低精确的临床保守策略——宁可误报也不漏报。

这一结果的震撼之处在于数据效率：OraPO仅用1K样本即超越使用1.27M样本训练的MambaXray-L。Table 2进一步显示，在不同VLM骨干上统一使用R2GenGPT进行SFT后，OraPO仍显著优于其他RL方法，验证了其骨干无关的通用性。

### MIMIC-CXR迁移结果：跨数据集的鲁棒性

Table 3报告了MIMIC-CXR上的结果。OraPO同样以1K样本取得**F1=0.357**，Recall高达**0.891**，显著优于使用完整223K样本训练的R2GenGPT（F1=0.260, Recall=0.248）。这证明OraPO的数据效率并非CheXpert Plus的特例，其自适应混合策略在不同数据分布下均能有效运作。

### 消融实验：FactS奖励与OraPO组件的独立贡献

Table 4的消融实验揭示了三个关键发现：

**（1）FactS奖励是性能跃升的第一推动力。** 基础Qwen2.5-VL-3B-Instruct未经微调时F1仅为0.034。引入naïve GRPO（以准确率为奖励）后F1升至0.089，提升有限。将奖励替换为FactS后，F1飙升至**0.291（+227%）**，Recall从0.162跃升至0.605（**+274%**）。这验证了FactS通过原子事实提取和标签级蕴含验证，提供了远比标量准确率更稠密、更具诊断导向的奖励信号。

**（2）OraPO在FactS基础上进一步释放潜力。** 在FactS+GRPO基础上加入DPO自适应混合（即完整OraPO），F1从0.291进一步提升至**0.341**，Recall从0.605升至0.832。这表明DPO组件有效将GRPO的探索失败转化为偏好学习的正向信号，而非简单丢弃。

**（3）OraPO的数据效率在极小样本下依然成立。** 仅用400个训练样本时，OraPO+FactS已取得F1=0.296，超过FactS-only在1K样本下的0.289。这展示了OraPO在极端数据稀缺场景下的实用价值。

**（4）DPO不可替代。** 将DPO替换为SFT（GRPO+SFT变体）导致性能崩溃：Recall降至0.176，F1降至0.106。这证明简单的监督微调无法替代DPO在OraPO中的角色——DPO通过对比正负例的偏好学习，精准地将策略推离低质量生成区域，而SFT的正向模仿缺乏这种排斥力。

### 人工金标验证：临床可信度

Table 5展示了在CheXpert验证集人工金标上的结果。OraPO取得F1=0.288，Recall=0.641，优于GPT-4.1的prompt engineering结果（F1=0.253, Recall=0.305）。尽管GPT-4.1的精确率更高（0.375 vs 0.234），OraPO在召回上的巨大优势（+0.336）使其综合F1更优。这验证了FactS奖励机制确实引导模型生成了更具临床事实支撑的报告，而非仅仅模仿表面语言模式。

### 训练动态分析：零奖励率抑制与困难类别学习

Figure 2的左图展示了OraPO与naïve GRPO在训练过程中零奖励批次比例的动态变化。在训练初期（前50步），naïve GRPO约有**30%的批次奖励全为零**，产生无效梯度。OraPO通过自适应DPO介入，显著更快地压制零奖励率，并收敛到更低的平台值。这直接验证了核心设计假设：当GRPO探索失败时，DPO以真实报告为正例、失败生成为负例进行偏好优化，有效将“废料”转化为教学信号。

Figure 2的中图和右图展示了两个临床困难且罕见的类别——**Pneumonia（发病率2.70%）**和**Fracture（4.05%）**——的F1随训练步数的变化曲线。OraPO在这两个类别上均**更早开始提升**，并在整个训练过程中**维持更高的F1**。这表明Oracle教育机制特别有利于长尾、困难病理的学习，因为零奖励组在这些类别上更频繁出现，而OraPO的DPO介入恰好提供了关键的梯度信号。

### 失败模式与局限性

尽管OraPO在召回率上表现卓越，其精确率（0.237）显著低于部分基线（如MambaXray-L的0.377）。这反映出模型倾向于过度报告阳性发现，可能产生临床假阳性。Figure 3的定性示例中，模型生成报告与真实报告之间的不匹配句被高亮标注，直观展示了这一现象。

此外，以下局限需在实际部署中关注：
- **FactS依赖GPT-4.1**进行事实提取和蕴含验证，引入额外的计算成本和API延迟，限制了实时应用场景。
- **仅1K训练样本**虽展示了极端数据效率，但对超罕见病理的覆盖必然不足，且未在不同人群/机构数据上进行泛化测试。
- **仅在小规模VLM（3B）上验证**，OraPO在更大模型（>7B）上的效果和计算效率有待确认。
- **DPO权重范围较窄（0.05-0.15）**，固定超参数可能在不同训练规模下需要重新调整。

### 开放问题

1. OraPO在其他医学影像模态（CT、MRI）的报告生成任务上是否同样有效？
2. 是否有更高效的原子事实提取方法（如开源轻量NLI模型），以减少对闭源大模型的依赖？
3. 如何在保持极高召回率的同时提升精确率，以降低假阳性风险？可能的路径包括引入精确率惩罚项或校准FactS的β参数。
4. OraPO结合更先进的长文本生成RL技术（如DR.GRPO、LN-DPO）是否能带来进一步增益？
5. 当训练数据量增大至数千或数万时，当前的自适应权重策略是否仍是最优解？

### 补充图表

![[assets/figures/papers/paper_list_l2289_https_arxiv_org_abs_2509_18600/figures/002_Figure_2.jpg]]
*Figure 2: Left: Cumulative proportion of zero-reward batches (reward batch mean = 0) vs. training step on CheXpert Plus [92]. OraPO suppresses zero-reward frequency faster than na¨ıve GRPO. Centre/Right: Class-level F1 on the CheXpert Plus validation set [92] across checkpoints for two clinically challenging and rare classes: Pneumonia (2.70%) and Fracture (4.05%). OraPO learns earlier and maintains higher F1 than na¨ıve GRPO*

![[assets/figures/papers/paper_list_l2289_https_arxiv_org_abs_2509_18600/figures/005_Table_3.jpg]]
*Table 3: Experimental results on the MIMIC-CXR dataset [8]. We report macro-averaged Precision, Recall, and F1 across 14 CheXpert pathologies. Train Size is the number of training samples. Some baselines train on multiple corpora and/or in multiple stages. Best are in bold*

![[assets/figures/papers/paper_list_l2289_https_arxiv_org_abs_2509_18600/figures/006_Table_4.jpg]]
*Table 4: Ablation on CheXpert Plus [8]: Impact of the FactS reward and OraPO. The first row indicates the base Qwen2.5-VL-3B-Instruct [4] direct test results, without any fine-tuning. The second row corresponds to a na¨ıve GRPO-based RLHF baseline using accuracy as the reward [29]. We report per-label Precision, Recall, and F1 across 14 findings. Best are in bold*

![[assets/figures/papers/paper_list_l2289_https_arxiv_org_abs_2509_18600/figures/007_Table_5.jpg]]
*Table 5: Experimental results on CheXpert validation set with gold labels from certified radiologists [36]*

![[assets/figures/papers/paper_list_l2289_https_arxiv_org_abs_2509_18600/figures/008_Table_6.jpg]]
*Table 6: Hyperparameter settings of the proposed method (selected in underline)*

![[assets/figures/papers/paper_list_l2289_https_arxiv_org_abs_2509_18600/figures/009_Table_7.jpg]]
*Table 7: Experimental results (micro averaging) on the MIMIC-CXR dataset [8]*

![[assets/figures/papers/paper_list_l2289_https_arxiv_org_abs_2509_18600/figures/010_Figure_3.jpg]]
*Figure 3: X-ray image and its corresponding ground-truth, along with the output of our model generation report on the ChexPert Plus dataset. The mismatch sentence in the reports are highlighted using different colors*



## 定位与知识库关联

### 1. 与基线方法的关系

OraPO 处于放射学报告生成（RRG）的强化学习微调谱系中，其直接对比的基线可分为三类：

**（1）纯 GRPO 基线**：OraPO 以 naïve GRPO（仅含准确率奖励与 KL 正则）为最直接的消融对比对象。核心差异在于 OraPO 引入由零奖励率（ZRR）驱动的自适应 DPO 损失混合（Eq. 11），将 GRPO 的探索失败转化为监督信号。实验表明，纯 GRPO 在早期约 30% 的组中奖励全为零（Fig. 2 左），产生无效梯度；OraPO 通过动态增加 DPO 权重，显著加速零奖励率下降，并在 Pneumonia 和 Fracture 等困难类别上更早、更高地提升 F1（Fig. 2 中/右）。

**（2）任务专用 SOTA 方法**：在 CheXpert Plus 上，OraPO 以仅 1K 训练样本取得 macro-F1 = 0.341，超过此前最佳方法 **MambaXray-L**（Wang et al., CVPR 2025）使用 1.27M 样本的 F1 = 0.335（Table 1）。在 MIMIC-CXR 上，OraPO 以 1K 样本取得 F1 = 0.357，优于使用完整 223K 样本的 **R2GenGPT**（F1 = 0.260）和 **Token-Mixer**（Yang et al., IEEE TMI 2024）等多个代表性基线（Table 3）。OraPO 在召回率上尤为突出（CheXpert Plus 上 +0.513 vs. MambaXray-L），但精确率存在差距（-0.140），反映出其偏好高召回的生成策略。

**（3）通用 VLM 微调基线**：Table 2 展示了不同 LLM/VLM 经 R2GenGPT 微调后的结果。OraPO 在此设定下同样以 1K 样本取得最优，验证了其方法在多种 backbone 上的有效性。

### 2. 方法适用边界

**适用场景**：
- **极低数据预算**：OraPO 在 1K 样本下即可达到或超越使用数十万样本的基线，适合标注成本高昂的医学影像领域。
- **领域知识匮乏的 VLM**：当基础模型在目标领域几乎无先验知识时（如 Qwen2.5-VL-3B 未微调时临床有效性 F1 仅 0.034，Table 4），OraPO 的“教育-探索”机制能有效引导模型从零开始学习。
- **需要高召回率的临床筛查**：FactScore 奖励的 F-β 设计倾向于召回，使 OraPO 在减少漏诊方面具有优势。

**不适用或需谨慎的场景**：
- **对精确率要求极高的场景**：OraPO 当前精确率低于部分基线（如 MambaXray-L 精确率 0.377 vs. OraPO 0.237），在假阳性代价高昂的任务中需额外约束。
- **大模型（>7B）**：实验仅在 Qwen2.5-VL-3B 上进行，OraPO 在更大模型上的效果和计算效率有待验证。
- **极端罕见病理**：1K 训练样本可能对发病率极低的疾病覆盖不足，论文未进行深入的公平性或亚组分析。

### 3. 关键局限与开放问题

**已识别的局限**：
1. **FactS 奖励的外部依赖**：FactScore 依赖 GPT-4.1 进行原子事实提取和蕴含验证，引入额外的计算成本、延迟和对闭源模型的依赖。
2. **DPO 权重范围固定**：混合权重 $w_i^{(t)}$ 被限制在 [0.05, 0.15] 的窄区间（Eq. 10），该超参数在不同数据规模或模型大小下可能需要重新调整。
3. **泛化未验证**：未在不同人群、机构或影像模态（CT、MRI）上进行测试。
4. **精确率-召回率权衡**：OraPO 以牺牲精确率为代价换取极高召回率，在需要平衡两者的场景中需额外机制。

**开放问题**：
1. OraPO 的自适应混合策略在数据量增至数千或数万时是否仍然最优？ZRR 的动态范围可能随模型能力提升而变化。
2. 是否有更高效的原子事实提取方法（如开源小模型或结构化知识库）以减少对 GPT-4.1 的依赖？
3. OraPO 与更先进的长文本生成 RL 技术（如 DR.GRPO、LN-DPO）结合是否能进一步提升性能？
4. 如何在保持高召回率的同时提升精确率，以完全消除假阳性？可能需要引入额外的精确率约束或负采样策略。
5. OraPO 在其他医学影像报告生成任务（如 CT、MRI）上的适用性如何？不同模态的事实提取和蕴含验证逻辑可能需要适配。



## 原文 PDF

![[paperPDFs/CVPR_2026/OraPO_Oracle_educated_Reinforcement_Learning_for_Data_efficient_and_Factual_Radiology_Report_Generation.pdf]]
