---
title: "UniGen-1.5: Enhancing Image Generation and Editing through Reward Unification in RL"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/UniGen_1_5_Enhancing_Image_Generation_and_Editing_through_Reward_Unification_in_RL.pdf
project_link: null
code_link: null
aliases:
- U15
- U15EIGETRUR
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 将图像编辑任务重新表述为通用图像生成任务，使用共享的文本-图像对齐奖励模型，在统一强化学习框架下同时优化生成与编辑；并通过编辑指令对齐阶段显著增强模型对编辑意图的理解。
primary_logic: 通过将编辑目标图像的语义描述作为奖励信号，可以直接复用成熟的文本-图像生成奖励模型，从而简化奖励设计，实现生成与编辑的可扩展联合优化。
claims:
- GRPO训练使生成（GenEval 0.85→0.89, DPG-Bench 84.19→86.83）和编辑（ImgEdit 3.93→4.31）性能大幅提升，且联合训练优于单任务训练。
- 编辑指令对齐阶段在RL前即提升所有任务，并使RL编辑增益加倍（0.38 vs. 0.21）。
- 统一RL策略在ImgEdit上达到4.31综合分，大幅超越现有开源模型OmniGen2（3.44），逼近GPT-Image-1。
- ImgEdit 上 Overall score = 4.31
---

# UniGen-1.5: Enhancing Image Generation and Editing through Reward Unification in RL

> [!tip] 核心洞察
> 通过将编辑目标图像的语义描述作为奖励信号，可以直接复用成熟的文本-图像生成奖励模型，从而简化奖励设计，实现生成与编辑的可扩展联合优化。

| 字段 | 内容 |
|------|------|
| 中文题名 | UniGen-1.5：通过强化学习中的奖励统一增强图像生成与编辑 |
| 英文题名 | UniGen-1.5: Enhancing Image Generation and Editing through Reward Unification in RL |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Tian_UniGen-1.5_Enhancing_Image_Generation_and_Editing_through_Reward_Unification_in_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | UniGen-1.5 |
| Dataset | ImgEdit, GenEval, DPG-Bench |

> [!tip] 效果简介
> - ImgEdit 上，Overall score 4.31 vs 3.44 (OmniGen2) (+0.87)。
> - GenEval 上，Overall score 0.89 vs 0.85 (UniGen-1.5 w/o RL) (+0.04)。
> - DPG-Bench 上，Overall score 86.83 vs 84.19 (UniGen-1.5 w/o RL) (+2.64)。

## 概要

**核心问题**：当前统一多模态模型在监督微调（SFT）后仍存在显著的指令理解瓶颈——模型难以充分解析复杂的图像编辑指令，导致强化学习（RL）训练中候选图像的奖励方差过小、学习信号薄弱，阻碍了生成与编辑能力的联合提升。

**核心方法**：UniGen-1.5 提出**统一强化学习策略**与**编辑指令对齐**两个关键设计。前者将图像编辑重新表述为通用图像生成任务，复用文本-图像对齐的集成奖励模型（CLIP-H、HPSv2、Unified-Reward-7B、ORM），在 GRPO 框架下联合优化生成与编辑；后者作为轻量级后 SFT 阶段，借助外部模型生成编辑目标图像的语义描述，使模型显式学习编辑指令与目标语义之间的映射，显著增强指令理解能力。

**主要结果**：UniGen-1.5 在 ImgEdit 综合评测上达到 **4.31**，大幅超越现有开源模型 OmniGen2（3.44），逼近闭源模型 GPT-Image-1；在 GenEval 和 DPG-Bench 上分别取得 **0.89** 和 **86.83**，均优于 BAGEL、BLIP3-o 等同期方法。消融实验证实，统一 RL 联合训练优于单任务训练，且编辑指令对齐阶段使 RL 编辑增益加倍（+0.38 vs. +0.21）。

**方法定位**：UniGen-1.5 属于**统一多模态生成-编辑框架**，其方法谱系可追溯至 UniGen（Tian et al., arXiv 2025）的 LLM-based 生成架构，并在以下维度实现突破：引入编辑指令对齐解决 SFT 后指令理解不足的问题；通过统一 RL 实现生成与编辑的可扩展联合优化；以共享奖励模型替代任务特化奖励设计，简化训练管线。与扩散模型路线（如 FLUX.1 Kontext Pro）或纯编辑模型（如 OmniGen2）不同，UniGen-1.5 在单一自回归框架内同时覆盖图像理解、生成与编辑三个任务。



### 图像生成与编辑的统一化趋势

近年来，多模态大语言模型（MLLM）在统一视觉理解与生成方面取得了显著进展。以 **UniGen**（Tian et al., arXiv 2025）为代表的工作展示了单一自回归Transformer同时处理图像理解、文本到图像生成和图像编辑的潜力。然而，这类统一模型在监督微调（SFT）之后仍面临一个核心瓶颈：**模型无法充分理解复杂的编辑指令**，导致候选图像在奖励模型评估下差异极小，强化学习（RL）训练中学习信号微弱，难以同时提升生成与编辑能力。

### 现有方法的缺口

当前图像编辑方法主要分为两类。一类是基于扩散模型的专用编辑器（如 **FLUX.1 Kontext [Pro]**），它们在特定编辑任务上表现优异，但缺乏与理解和生成的统一性。另一类是基于MLLM的统一模型（如 **OmniGen2**, Wu et al., arXiv 2025），虽然架构统一，但在编辑性能上仍与专用模型存在差距——例如 OmniGen2 在 ImgEdit 基准上仅达到 3.44 的综合分。更关键的是，这些方法在 RL 对齐阶段通常仅针对文本到图像生成进行优化，**缺乏对图像编辑任务的统一奖励设计**，导致编辑能力无法通过 RL 获得实质性提升。

### 本文动机

针对上述缺口，UniGen-1.5 提出两个关键创新。首先，引入**编辑指令对齐（Edit Instruction Alignment）**作为轻量级后SFT阶段，通过外部模型生成目标图像的文本描述并训练模型预测该描述，从而显著增强模型对编辑意图的语义理解。其次，提出**统一强化学习策略**：将图像编辑重新表述为通用图像生成任务，直接复用成熟的文本-图像对齐奖励模型（CLIP-H、HPSv2、Unified-Reward-7B、ORM），在共享奖励框架下联合优化生成与编辑。这一设计从根本上解决了编辑任务奖励方差小、学习信号弱的问题，使得生成与编辑能力能够协同提升。



## 核心方法与创新机理

UniGen-1.5 的核心创新在于通过**奖励统一**将图像生成与图像编辑纳入同一个强化学习框架，并引入**编辑指令对齐**阶段以克服监督微调后模型对编辑指令理解不足的瓶颈。其相对于前代基线 UniGen（Tian et al., arXiv 2025）的关键改动槽位（changed slots）如下。

### 1. 奖励统一：将编辑重新表述为通用生成任务

监督微调后的模型在图像编辑任务上存在候选图像奖励方差小、学习信号弱的问题，导致强化学习难以有效提升编辑能力。UniGen-1.5 的解决方案是将编辑目标图像的语义描述作为奖励信号，从而直接复用成熟的文本-图像生成奖励模型。

具体而言，给定编辑后的输出图像 $\tilde{\mathcal{X}}_O^G$ 和描述其期望语义的文本 $T_O$，统一奖励函数 $R(\tilde{\mathcal{X}}_O^G, T_O)$ 同时评估生成与编辑任务。奖励集成（reward ensemble）包含四个互补的视觉专家模型：**CLIP-H**、**HPSv2**、**Unified-Reward-7B** 和 **ORM**。对于文本-图像生成，直接将生成图像与文本提示输入奖励模型；对于图像编辑，则先通过外部强大多模态模型（MLLMs 和 LLMs）估计编辑后图像的文本描述，再计算该描述与生成图像的语义对齐度（Figure 4）。

这一设计的核心洞察是：编辑任务本质上可被视为“根据条件图像和编辑指令生成目标图像”，其输出质量同样可以通过文本-图像对齐来度量，因此无需为编辑单独设计奖励模型，实现了生成与编辑的可扩展联合优化。

### 2. 编辑指令对齐：强化学习前的关键预备阶段

在进入统一强化学习之前，UniGen-1.5 增加了一个轻量的后 SFT 阶段——**编辑指令对齐**（Edit Instruction Alignment）。该阶段利用外部模型为编辑后的目标图像生成文本描述，然后优化模型基于条件图像和编辑指令预测该描述的能力（Figure 3）。其目标是增强模型对编辑意图的语义理解，而非直接生成图像。

消融实验（Table 5）表明，该阶段在强化学习前即可提升 GenEval、DPG-Bench 和 ImgEdit 三个基准的性能，并且使后续强化学习在编辑任务上的增益加倍（+0.38 vs. +0.21）。这验证了编辑指令对齐有效解决了监督微调后模型对复杂编辑指令理解不足的核心瓶颈。

### 3. 统一强化学习框架

UniGen-1.5 采用 **GRPO**（Group Relative Policy Optimization）进行策略优化，在训练中同时采样文本-图像生成和图像编辑的候选样本，通过组内标准化计算优势函数：

$$A_i = \frac{R_i - \mathrm{mean}(\{R_1,...,R_N\})}{\mathrm{std}(\{R_1,...,R_N\})}$$

策略更新目标为带有裁剪重要性采样比和 KL 散度惩罚的 PPO 风格目标：

$$\mathcal{L}(\theta) = \frac{1}{N}\sum_{i=1}^N \min\big(\rho_i A_i, \mathrm{clip}(\rho_i, 1-\epsilon, 1+\epsilon) A_i\big) - \beta D_{\mathrm{KL}}(\pi_\theta \| \pi_{\mathrm{ref}})$$

训练中移除了传统的比率裁剪，仅依赖显式 KL 惩罚来约束策略更新，共进行 1500 步，学习率 $3 \times 10^{-6}$，batch size 32，在 8 张 B200 GPU 上完成。

消融实验（Table 4）直接验证了联合训练的必要性：移除强化学习中的文本-图像生成任务会导致该任务性能显著下降（GenEval 0.85 vs. 0.89），移除图像编辑任务则导致编辑性能显著下降（ImgEdit 3.93 vs. 4.31），证明两个任务在统一奖励下相互促进。

### 4. 架构与推理的配套改进

为支撑统一框架，UniGen-1.5 在多个架构槽位进行了升级：

- **视觉理解编码器**：从 SigLIP（固定分辨率）升级为 **SigLIP2**，支持任意分辨率和宽高比的原生输入，提升对条件图像的语义提取能力。
- **生成标记器**：从 VQGAN / MAGViTv1 升级为 **MAGViTv2**，提供更高质量的离散令牌化与反令牌化。
- **图像编辑输入**：同时输入条件图像的连续语义特征（来自 SigLIP2）和离散低级特征（来自 MAGViTv2），通过掩码令牌预测生成目标图像，使模型能同时利用语义和纹理信息。
- **编辑推理引导**：引入对编辑指令（$s_T$）和条件图像（$s_I$）的独立无分类器引导尺度，推理时使用 $s_T=3$、$s_I=1.5$ 的设置，以平衡指令遵循与视觉一致性：

$$\mathcal{X}_O = \mathcal{P}_\theta(\emptyset,\emptyset,\emptyset) + s_I \cdot (\mathcal{P}_\theta(\mathcal{X}_C^U,\emptyset,\mathcal{X}_C^G) - \mathcal{P}_\theta(\emptyset,\emptyset,\emptyset)) + s_T \cdot (\mathcal{P}_\theta(\mathcal{X}_C^U,\mathcal{T}_C,\mathcal{X}_C^G) - \mathcal{P}_\theta(\mathcal{X}_C^U,\emptyset,\mathcal{X}_C^G))$$

### 创新总结

UniGen-1.5 的创新链条清晰：**编辑指令对齐**解决监督微调后指令理解不足的瓶颈 → **奖励统一**将编辑重新表述为通用生成任务，复用成熟奖励模型 → **统一强化学习**联合优化生成与编辑，两个任务相互促进。这一设计使模型在 ImgEdit 上达到 4.31 的综合分，大幅超越现有开源模型 OmniGen2（3.44），逼近闭源模型 GPT-Image-1，同时在 GenEval（0.89）和 DPG-Bench（86.83）上也取得领先。



UniGen-1.5 的核心设计动机源于一个被验证的关键瓶颈：模型在监督微调后仍无法充分理解复杂的编辑指令，导致强化学习训练中候选图像的奖励方差小、学习信号弱，阻碍生成与编辑能力的联合提升。为解决这一问题，UniGen-1.5 提出了一套统一的强化学习框架，将图像编辑重新表述为通用图像生成任务，通过共享的文本-图像对齐奖励模型同时优化生成与编辑，并引入**编辑指令对齐**阶段显著增强模型对编辑意图的理解。

### 多模态主干架构

UniGen-1.5 以预训练语言模型 **Qwen2.5-7B** 为核心，采用分离式编码器设计，分别处理视觉理解和视觉生成任务（Figure 2）：

![[assets/figures/papers/paper_list_l2709_https_openaccess_thecvf_com_content_CVPR2026_html_Tian_UniGen_1_5_Enhanc/figures/002_Figure_2.jpg]]
*Figure 2: Thearchitectureof UniGen-1.5jointlyoptimizedfor(a)imageunderstanding,(b)text-to-imagegenerationand(c)mage editing. See Sec.3.1 for more details*

- **视觉理解编码器**：使用 **SigLIP2**，支持任意分辨率和宽高比的原生图像输入，提取连续语义特征 $\mathcal{X}_C^U$。
- **视觉生成标记器**：使用 **MAGViTv2** 作为离散视觉标记器，将图像编码为离散令牌序列 $\mathcal{X}_C^G$ 用于生成，并通过解码器重建图像。
- **MLP 投影器**：对齐视觉特征与语言模型的文本嵌入空间，使多模态序列能够被 LLM 统一处理。

该架构支持三种任务模式（Figure 2）：
1. **图像理解**：SigLIP2 编码图像 → MLP 投影 → LLM 生成文本响应。
2. **文本到图像生成**：LLM 根据文本提示生成离散图像令牌序列 → MAGViTv2 解码器重建图像。
3. **图像编辑**：同时输入条件图像的语义特征（SigLIP2 连续特征）和低级特征（MAGViTv2 离散特征），LLM 通过掩码令牌预测生成目标图像。

### 训练管线

UniGen-1.5 的训练分为四个阶段（Figure 3）：

1. **预训练**：使用图像生成、图像理解和文本理解数据以 3:2:1 的比例混合训练，数据来源包括 ImageNet、CC-3M、CC-12M、SAM-11M 及少量 RefinedWeb 纯文本数据。
2. **监督微调（SFT）**：在高质量图像生成和编辑数据上进行指令微调。
3. **编辑指令对齐（Edit Instruction Alignment）**：这是一个轻量的后 SFT 阶段，核心思路是利用外部强模型（MLLMs 和 LLMs）为编辑目标图像生成文本描述，然后训练 UniGen-1.5 根据编辑指令和条件图像预测该描述。此阶段旨在增强模型对编辑指令语义的理解，为后续 RL 训练提供更强的学习信号。消融实验证实，该阶段在 RL 前即可提升所有基准性能，并使 RL 编辑增益加倍（+0.38 vs. +0.21）。
4. **统一强化学习（Unified RL）**：采用 GRPO 算法，将图像生成和编辑任务纳入统一的奖励框架。关键创新在于将编辑目标图像的语义描述作为奖励信号，从而直接复用成熟的文本-图像生成奖励模型。

### 统一强化学习的奖励设计

统一 RL 的核心洞察是：通过将编辑任务重新表述为“生成符合目标描述的图像”，可以共享生成任务的奖励模型，实现可扩展的联合优化（Figure 4）。具体而言：

- **生成任务**：直接将生成图像与文本提示输入奖励模型，获得对齐分数。
- **编辑任务**：先用外部 MLLM/LLM 根据条件图像和编辑指令生成目标图像描述 $\mathcal{T}_O$，再将编辑输出图像与该描述一起输入奖励模型，衡量编辑结果与目标语义的对齐程度。

奖励函数 $R(\cdot)$ 由四个视觉专家模型集成：**CLIP-H**、**HPSv2**、**Unified-Reward-7B** 和 **ORM**。GRPO 训练使用组归一化优势函数：

$$A_i = \frac{R_i - \mathrm{mean}(\{R_1,...,R_N\})}{\mathrm{std}(\{R_1,...,R_N\})}$$

策略更新目标采用带 KL 散度惩罚的裁剪目标：

$$\mathcal{L}(\theta) = \frac{1}{N}\sum_{i=1}^N \min\big(\rho_i A_i, \mathrm{clip}(\rho_i, 1-\epsilon, 1+\epsilon) A_i\big) - \beta D_{\mathrm{KL}}(\pi_\theta \| \pi_{\mathrm{ref}})$$

其中 $\rho_i$ 为重要性采样比，$\pi_{\mathrm{ref}}$ 为参考策略。训练使用 1500 步、学习率 $3\times10^{-6}$、批量大小 32，在 8 块 B200 GPU 上完成。

### 推理时的引导策略

在图像编辑推理阶段，UniGen-1.5 采用改进的无分类器引导（CFG），对编辑指令和条件图像使用独立的引导尺度：

$$\mathcal{X}_O = \mathcal{P}_\theta(\emptyset,\emptyset,\emptyset) + s_I \cdot (\mathcal{P}_\theta(\mathcal{X}_C^U,\emptyset,\mathcal{X}_C^G) - \mathcal{P}_\theta(\emptyset,\emptyset,\emptyset)) + s_T \cdot (\mathcal{P}_\theta(\mathcal{X}_C^U,\mathcal{T}_C,\mathcal{X}_C^G) - \mathcal{P}_\theta(\mathcal{X}_C^U,\emptyset,\mathcal{X}_C^G))$$

其中 $s_T$ 控制编辑指令的引导强度，$s_I$ 控制条件图像的引导强度。在 ImgEdit 基准评估中，分别设置为 $s_T=3$ 和 $s_I=1.5$。



### 多模态架构的三大功能模块

UniGen-1.5 基于预训练语言模型 **Qwen2.5-7B** 构建，通过独立的编码器分别处理图像理解与图像生成任务。其架构包含三个核心功能模块（Figure 2）：

- **图像理解模块**：使用 **SigLIP2** 编码器 $Enc^U$ 提取图像的连续语义特征。SigLIP2 支持任意分辨率和宽高比的输入，相比前代 UniGen 使用的固定分辨率 SigLIP，增强了对多样化图像条件的适应能力（Sec. 3.1）。

- **图像生成模块**：采用 **MAGViTv2** 作为离散视觉标记器（Tokenizer），负责将图像编码为离散令牌序列，并通过 LLM 自回归预测生成目标图像的令牌，最终由 MAGViTv2 解码器重建为像素空间图像。相比前代使用的 VQGAN/MAGViTv1，MAGViTv2 提供了更高质量的令牌化与重建能力（Sec. 3.1）。

- **图像编辑模块**：编辑任务同时利用上述两个编码器。给定条件图像 $\mathcal{X}_C$ 和编辑文本指令 $\mathcal{T}_C$，模型分别提取连续语义特征 $\mathcal{X}_C^U = Enc^U(\mathcal{X}_C)$ 和离散低级特征 $\mathcal{X}_C^G = Enc^G(\mathcal{X}_C)$，二者共同作为 LLM 的条件输入，通过掩码令牌预测生成编辑后的目标图像（Sec. 3.1, Figure 2(c)）。

此外，一个 **MLP Projector** 负责将视觉特征映射到与文本嵌入对齐的表示空间，确保多模态序列在 LLM 中的统一处理。

### 编辑指令对齐模块

在监督微调（SFT）之后、强化学习（RL）之前，UniGen-1.5 引入了一个轻量级的 **编辑指令对齐**（Edit Instruction Alignment）阶段（Figure 3）。该模块的核心机制是：利用外部强模型（MLLM 和 LLM）为编辑目标图像生成文本描述，然后优化 UniGen-1.5 自身预测该描述的能力。这一过程迫使模型在生成图像之前先“理解”编辑指令所期望的视觉语义，从而显著增强模型对复杂编辑意图的解析能力（Sec. 3.4）。

![[assets/figures/papers/paper_list_l2709_https_openaccess_thecvf_com_content_CVPR2026_html_Tian_UniGen_1_5_Enhanc/figures/003_Figure_3.jpg]]
*Figure 3: Ilustration of Edit Instruction Alignment in the entire training pipeline of UniGen-1.5*

### 统一强化学习框架中的奖励模型集成

UniGen-1.5 的核心创新在于将图像编辑重新表述为通用图像生成任务，使得两类任务可以共享同一套文本-图像对齐奖励模型。具体而言，奖励函数 $R(\cdot)$ 由四个互补的视觉专家模型集成（Sec. 3.5）：

- **CLIP-H** 和 **HPSv2**：评估图像与文本的语义对齐程度；
- **Unified-Reward-7B**：基于 MLLM 的统一奖励模型，提供更细粒度的质量判断；
- **ORM**（Object Reward Model）：检测生成图像中的对象与文本描述的一致性。

对于文本-图像生成任务，直接将生成图像与文本提示输入奖励模型获得奖励信号；对于图像编辑任务，则先通过外部模型估计编辑后目标图像的文本描述 $\tilde{\mathcal{T}}_O$，再将该描述与生成图像一同输入奖励模型计算对齐得分（Figure 4）。

![[assets/figures/papers/paper_list_l2709_https_openaccess_thecvf_com_content_CVPR2026_html_Tian_UniGen_1_5_Enhanc/figures/004_Figure_4.jpg]]
*Figure 4: Left:The pipelineof GRPOtraiingin UniGen-1.5.Weutilizesharedrewardmodelsforbothtext--image generationand imageediting.Forthfoer,wedirectlyiputthegeneratedimagewithtetextprompttoobtainrewards.Forthelaterwegetreward signals bymeasuringthealignmentbetweentheeditedimagedescriptionandthe generatedimage.Right: Thepipelineofeditedimage description estimation.We leverage powerful external MLLMs andLLMsto generate thedescriptionofdesired editedimages*

### 关键公式推导

**GRPO 优势函数**。UniGen-1.5 采用 Group Relative Policy Optimization（GRPO）进行策略更新。对于每组 $N$ 个候选样本，优势函数通过组内标准化计算：

$$A_i = \frac{R_i - \mathrm{mean}(\{R_1, R_2, ..., R_N\})}{\mathrm{std}(\{R_1, R_2, ..., R_N\})}$$

其中 $R_i$ 为第 $i$ 个候选样本的集成奖励得分。这种组内相对比较的设计使模型能够从同一指令下不同生成质量的样本中学习偏好排序（Sec. 3.5, Equation 1）。

**GRPO 训练目标**。策略参数 $\theta$ 的更新目标为：

$$\mathcal{L}(\theta) = \frac{1}{N}\sum_{i=1}^N \min\big(\rho_i A_i, \mathrm{clip}(\rho_i, 1-\epsilon, 1+\epsilon) A_i\big) - \beta D_{\mathrm{KL}}(\pi_\theta \| \pi_{\mathrm{ref}})$$

其中 $\rho_i$ 为重要性采样比，$\epsilon$ 为裁剪阈值，$\beta$ 为 KL 散度惩罚系数，$\pi_{\mathrm{ref}}$ 为参考策略。UniGen-1.5 遵循 T2I-R1 的做法，移除了传统 PPO 中的比例裁剪（ratio clipping），仅通过显式 KL 散度惩罚约束策略更新幅度（Sec. 3.5, Equation 2）。

**图像编辑的无分类器引导**。在推理阶段，UniGen-1.5 对编辑指令和条件图像分别使用独立的引导尺度：

$$\mathcal{X}_O = \mathcal{P}_\theta(\emptyset,\emptyset,\emptyset) + s_I \cdot (\mathcal{P}_\theta(\mathcal{X}_C^U,\emptyset,\mathcal{X}_C^G) - \mathcal{P}_\theta(\emptyset,\emptyset,\emptyset)) + s_T \cdot (\mathcal{P}_\theta(\mathcal{X}_C^U,\mathcal{T}_C,\mathcal{X}_C^G) - \mathcal{P}_\theta(\mathcal{X}_C^U,\emptyset,\mathcal{X}_C^G))$$

其中 $s_T$ 为编辑指令的引导尺度，$s_I$ 为条件图像的引导尺度。在 ImgEdit 基准评估中，$s_T$ 和 $s_I$ 分别设为 3 和 1.5（Sec. 4.1）。这种双重引导机制使模型能够分别控制对编辑指令的遵循程度和对条件图像视觉信息的保留程度。



## 实验与关键发现

### 核心结果与基准对比

UniGen-1.5 在图像编辑、文本-图像生成和图像理解三大类基准上均取得了领先或极具竞争力的结果。

**图像编辑**：在 ImgEdit 综合基准上，UniGen-1.5 以 **4.31** 的总分大幅超越现有开源模型 **OmniGen2**（3.44），领先幅度达 +0.87，并逼近专有模型 GPT-Image-1 的性能水平（Table 1）。这一结果验证了统一强化学习策略在编辑任务上的有效性。

**文本-图像生成**：在 GenEval 和 DPG-Bench 两个生成基准上，UniGen-1.5 分别取得了 **0.89** 和 **86.83** 的总分，显著优于 BAGEL、BLIP3-o 等近期方法（Table 2）。与未经过 RL 训练的 UniGen-1.5 基线（GenEval 0.85, DPG-Bench 84.19）相比，GRPO 训练分别带来了 +0.04 和 +2.64 的增益。

**图像理解**：UniGen-1.5 在图像理解基准上同样表现出色（Table 3），与 Show-o2 等专用模型相比具有竞争力，体现了统一架构在多模态任务上的泛化能力。

### 统一强化学习的消融分析

Table 4 系统消融了统一 RL 框架中不同任务组合的影响。实验在相同训练步数下进行，结论如下：

![[assets/figures/papers/paper_list_l2709_https_openaccess_thecvf_com_content_CVPR2026_html_Tian_UniGen_1_5_Enhanc/figures/008_Table_4.jpg]]
*Table 4: Ablation ofUnifiedRL.We train UniGen-1.5 with different tasks during RL for same steps.T2I stands for text-to-image generation and I-Edit represents image editing.We report the overall score for GenEval,DPG-Bench and ImgEdit benchmarks*

- **仅训练文本-图像生成（T2I）**：生成任务保持高性能（GenEval 0.89, DPG-Bench 86.83），但编辑性能显著退化（ImgEdit 3.93 vs. 联合训练的 4.31）。
- **仅训练图像编辑（I-Edit）**：编辑性能大幅下降至 3.93，同时生成任务也明显受损（GenEval 0.85 vs. 0.89）。
- **联合训练（T2I + I-Edit）**：在所有三个基准上均取得最优结果，证明了统一 RL 策略通过共享奖励模型实现了生成与编辑能力的协同提升。

这一消融直接支撑了核心洞察：将编辑任务重新表述为通用生成任务，复用文本-图像对齐奖励模型，能够提供更强的学习信号，避免单任务训练时的奖励方差不足问题。

### 编辑指令对齐的消融分析

Table 5 检验了编辑指令对齐（Edit Instruction Alignment）阶段的贡献：

![[assets/figures/papers/paper_list_l2709_https_openaccess_thecvf_com_content_CVPR2026_html_Tian_UniGen_1_5_Enhanc/figures/010_Table_5.jpg]]
*Table 5: Ablation of Edit Instruction Alignment. We report the overall score for GenEval,DPG-Bench and ImgEdit benchmarks*

- 在 RL 训练前，添加该阶段即可提升三个基准的性能，说明指令对齐本身已增强了模型对编辑意图的理解。
- 在 RL 阶段，经过指令对齐的模型获得了更大的编辑增益（+0.38 vs. 未对齐的 +0.21），编辑性能提升幅度接近翻倍。

这一结果证实了编辑指令对齐是 RL 训练的关键前置步骤——它通过外部强模型生成目标图像描述来优化模型对编辑指令的语义理解，从而在后续 RL 中放大了奖励信号的有效性。

### 推理策略与引导机制

UniGen-1.5 在图像编辑推理时引入了独立的无分类器引导（CFG）尺度：

$$
\begin{aligned}
\mathcal{X}_O = &\ \mathcal{P}_\theta(\emptyset,\emptyset,\emptyset) \\
&+ s_I \cdot (\mathcal{P}_\theta(\mathcal{X}_C^U,\emptyset,\mathcal{X}_C^G) - \mathcal{P}_\theta(\emptyset,\emptyset,\emptyset)) \\
&+ s_T \cdot (\mathcal{P}_\theta(\mathcal{X}_C^U,\mathcal{T}_C,\mathcal{X}_C^G) - \mathcal{P}_\theta(\mathcal{X}_C^U,\emptyset,\mathcal{X}_C^G))
\end{aligned}
$$

其中 $s_T$ 控制编辑指令的引导强度，$s_I$ 控制条件图像的引导强度。在 ImgEdit 评估中，设置 $s_T=3, s_I=1.5$。这种解耦设计允许模型在保持条件图像视觉一致性的同时，更精确地响应编辑指令。

### 定性效果与失败模式

Figure 5 展示了 GRPO 训练前后的定性对比：经过 RL 训练后，模型在复杂指令遵循、属性绑定和场景构成方面有明显改善。

![[assets/figures/papers/paper_list_l2709_https_openaccess_thecvf_com_content_CVPR2026_html_Tian_UniGen_1_5_Enhanc/figures/009_Figure_5.jpg]]
*Figure 5: Examples generated by UniGen-1.5, highlightingthecontribution of GRPO training*

然而，论文明确列出了若干已知局限：
1. **文本渲染能力不足**：模型无法准确生成图像中的文字，需要结合扩散组件改进。
2. **编辑视觉一致性欠佳**：在某些编辑场景下可能出现伪影或不合理的改变，缺乏专门的编辑一致性奖励模型。
3. **编辑指令对齐依赖外部模型**：目标描述由外部强模型生成，存在描述偏差风险，且增加了系统复杂度。
4. **离线奖励的局限性**：统一 RL 使用离线预计算奖励，可能未完全对齐人类偏好；在高编辑复杂度场景下，候选图像的奖励方差仍可能较小，削弱学习信号。

### 补充图表

![[assets/figures/papers/paper_list_l2709_https_openaccess_thecvf_com_content_CVPR2026_html_Tian_UniGen_1_5_Enhanc/figures/005_Table_1.jpg]]
*Table 1: Comparisonwithbaseline modelsonImgEditbenchmark.Thebestandsecond-bestresultsarehighlghtedinboldanduderlined, respectively. UniGen-1.5 achieves the best overall score against all the other models*

![[assets/figures/papers/paper_list_l2709_https_openaccess_thecvf_com_content_CVPR2026_html_Tian_UniGen_1_5_Enhanc/figures/006_Table_2.jpg]]
*Table 2: Comparisonwithstateof-te-artmodelsonGenEvalandDPG-Bench.Thebestandsecond-bestresultsarehighlightedinbold and underlined,respectively. UniGen-1.5 achieves the best performance on both benchmarks*

![[assets/figures/papers/paper_list_l2709_https_openaccess_thecvf_com_content_CVPR2026_html_Tian_UniGen_1_5_Enhanc/figures/001_Figure_1.jpg]]
*Figure 1: Examples of images generated by UniGen-1.5*

![[assets/figures/papers/paper_list_l2709_https_openaccess_thecvf_com_content_CVPR2026_html_Tian_UniGen_1_5_Enhanc/figures/007_Table_3.jpg]]
*Table 3: Comparisonwithstate-of-the-artmodelsonimageunderstandingbenchmarks.*denotesreproducedresults.Thebestandsecondbest results are highlighted in bold and underlined,respectively*



## 定位与知识库关联

### 1. 在图像生成与编辑统一模型谱系中的位置

UniGen-1.5 处于“统一多模态大语言模型（MLLM）同时处理图像理解、生成与编辑”这一技术路线的前沿。其直接前身 **UniGen**（Tian et al., arXiv 2025）已建立了基于 LLM 的统一架构，但缺乏专门的编辑支持与 RL 对齐阶段。UniGen-1.5 在此基础上引入三项关键升级，构成代际跃迁：

- **编码器升级**：视觉理解编码器从固定分辨率的 SigLIP 替换为支持原生分辨率和任意宽高比的 SigLIP2；生成标记器从 VQGAN/MAGViTv1 升级为 MAGViTv2，提升离散令牌的表示质量（Sec.3.1）。
- **编辑能力从无到有**：UniGen 不支持图像编辑；UniGen-1.5 通过同时输入条件图像的连续语义特征（SigLIP2 输出）和离散低级特征（MAGViTv2 令牌），以掩码令牌预测方式生成目标图像（Fig.2(c)），首次将编辑纳入统一架构。
- **后 SFT 对齐与统一 RL**：UniGen 无 RL 对齐阶段；UniGen-1.5 引入编辑指令对齐（Edit Instruction Alignment）和基于 GRPO 的统一强化学习，构成从监督微调到人类偏好对齐的完整训练管线。

在更广泛的方法谱系中，与 UniGen-1.5 可比的统一模型包括 **OmniGen2**（Wu et al., arXiv 2025）、**Show-o2**（Xie et al., arXiv 2025）和 **BAGEL**。在 ImgEdit 基准上，UniGen-1.5 以 4.31 的综合分大幅领先 OmniGen2（3.44），并逼近闭源模型 GPT-Image-1（Table 1）。在生成基准 GenEval 和 DPG-Bench 上，UniGen-1.5 分别达到 0.89 和 86.83，超越 BAGEL 与 BLIP3-o（Table 2）。这一性能优势的核心来源是统一 RL 策略——消融实验（Table 4）表明，若 RL 阶段移除任一任务（仅保留生成或仅保留编辑），对应任务的性能均显著下降，证实了联合优化的必要性。

### 2. 核心方法创新与因果机制

UniGen-1.5 的方法贡献可归结为一个核心洞察和两个关键设计：

**核心洞察**：将图像编辑重新表述为通用图像生成任务。具体而言，对于编辑指令 $T_C$ 和条件图像 $X_C$，模型并非直接学习“修改图像”的映射，而是生成目标图像 $X_O$，并以目标图像的文本描述 $T_O$ 作为奖励信号。这使得编辑任务可以直接复用成熟的文本-图像对齐奖励模型（CLIP-H、HPSv2、Unified-Reward-7B、ORM），无需为编辑单独设计奖励函数（Sec.3.5, Fig.4）。

**关键设计一：编辑指令对齐（Edit Instruction Alignment）**。在 SFT 之后、RL 之前插入一个轻量阶段：利用外部强 MLLM 和 LLM 为编辑样本生成目标图像的文本描述，然后训练模型根据编辑指令预测该描述（Sec.3.4, Fig.3）。这一阶段解决了监督微调后模型对复杂编辑指令理解不足的瓶颈——正是这种理解不足导致 RL 训练中候选图像奖励方差小、学习信号弱。消融实验（Table 5）表明，加入该阶段在 RL 前即提升所有基准性能，并使 RL 的编辑增益从 +0.21 翻倍至 +0.38。

**关键设计二：统一强化学习框架**。采用 GRPO（Group Relative Policy Optimization）算法，在组内标准化奖励后计算优势函数：

$$A_i = \frac{R_i - \mathrm{mean}(\{R_1,...,R_N\})}{\mathrm{std}(\{R_1,...,R_N\})}$$

策略更新目标为：

$$\mathcal{L}(\theta) = \frac{1}{N}\sum_{i=1}^N \min\big(\rho_i A_i, \mathrm{clip}(\rho_i, 1-\epsilon, 1+\epsilon) A_i\big) - \beta D_{\mathrm{KL}}(\pi_\theta \| \pi_{\mathrm{ref}})$$

其中 $\rho_i$ 为重要性采样比，$\beta$ 控制对参考策略 $\pi_{\mathrm{ref}}$ 的 KL 散度惩罚强度。生成与编辑任务共享同一套奖励模型集成，实现可扩展的联合优化。推理时，编辑采用独立引导尺度的无分类器引导（CFG），对编辑指令（$s_T$）和条件图像（$s_I$）分别控制引导强度，默认设为 $s_T=3, s_I=1.5$。

### 3. 适用边界与局限

尽管 UniGen-1.5 在生成与编辑基准上取得领先，其方法存在明确的适用边界：

1. **文本渲染能力不足**：模型无法准确生成图像中的文字，这是当前自回归视觉令牌预测方法的共性局限，需结合扩散组件改进。
2. **编辑视觉一致性欠佳**：在某些编辑场景下出现伪影或不合理的改变。根本原因在于统一 RL 使用的奖励模型（CLIP-H、HPSv2 等）主要衡量文本-图像语义对齐，缺乏对编辑前后视觉一致性的显式约束。需要设计专门的编辑一致性奖励模型。
3. **对外部强模型的依赖**：编辑指令对齐阶段依赖外部 MLLM/LLM 生成目标描述，存在描述偏差风险——若外部模型对编辑意图的理解有误，将直接污染对齐信号。
4. **离线奖励的局限性**：统一 RL 使用离线预计算奖励，可能未完全对齐人类偏好。在高编辑复杂度场景下，候选图像的奖励方差仍可能较小，导致 GRPO 的学习信号减弱。

### 4. 开放问题

1. **文本渲染的突破路径**：如何将扩散组件整合进自回归框架，以解决文本渲染这一长期瓶颈？
2. **编辑一致性奖励设计**：能否训练一个专门的奖励模型，在 RL 训练中同时优化文本-图像对齐和编辑前后视觉一致性？
3. **自监督编辑指令对齐**：如何减少或消除对外部强模型的依赖，实现自监督的编辑指令理解增强？
4. **规模化验证**：统一 RL 策略在更大规模、更多样化的编辑数据上能否保持泛化优势？当前实验主要在 ImgEdit 基准上验证，其覆盖的编辑类型和复杂度有限。
5. **与扩散模型的深度融合**：UniGen-1.5 目前是完全基于自回归令牌预测的框架；与扩散模型（如 FLUX.1 Kontext Pro）的混合架构是否能在保持统一性的同时突破各自局限？



## 原文 PDF

![[paperPDFs/CVPR_2026/UniGen_1_5_Enhancing_Image_Generation_and_Editing_through_Reward_Unification_in_RL.pdf]]
