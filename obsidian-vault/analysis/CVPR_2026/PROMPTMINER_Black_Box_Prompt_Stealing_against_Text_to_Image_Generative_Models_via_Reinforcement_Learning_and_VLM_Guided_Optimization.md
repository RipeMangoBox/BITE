---
title: "PROMPTMINER: Black-Box Prompt Stealing against Text-to-Image Generative Models via Reinforcement Learning and VLM-Guided Optimization"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/PROMPTMINER_Black_Box_Prompt_Stealing_against_Text_to_Image_Generative_Models_via_Reinforcement_Learning_and_VLM_Guided_Optimization.pdf
project_link: null
code_link: "https://github.com/aaFrostnova/PromptMiner"
aliases:
- PROMPTMINER
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 将提示窃取解耦为两阶段：基于强化学习的主体反转和基于VLM引导的修饰语搜索。强化学习利用奖励塑造高效优化离散提示空间，VLM变异算子系统探索修饰语空间。
primary_logic: 核心思路是将提示窃取任务解耦为两个阶段：（i）基于强化学习的优化阶段，用于重建主要主体；（ii）VLM引导的搜索阶段，用于恢复风格修饰语。
claims:
- PROMPTMINER在CLIP相似度上达到0.958，超越所有基线。
- 在野图像中，PROMPTMINER比最强基线在CLIP相似度上提高7.5%。
- 常见后防御（噪声、拼图、水印）对PROMPTMINER的影响很小，说明其对低层视觉扰动具有内在鲁棒性。
- 强化学习中的奖励塑形加速收敛并保持策略最优性，消融实验证实其有效性。
---

# PROMPTMINER: Black-Box Prompt Stealing against Text-to-Image Generative Models via Reinforcement Learning and VLM-Guided Optimization

> [!tip] 核心洞察
> 核心思路是将提示窃取任务解耦为两个阶段：（i）基于强化学习的优化阶段，用于重建主要主体；（ii）VLM引导的搜索阶段，用于恢复风格修饰语。

| 字段 | 内容 |
|------|------|
| 中文题名 | PROMPTMINER：基于强化学习与VLM引导优化的黑盒提示窃取攻击文本到图像生成模型 |
| 英文题名 | PROMPTMINER: Black-Box Prompt Stealing against Text-to-Image Generative Models via Reinforcement Learning and VLM-Guided Optimization |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Li_PROMPTMINER_Black-Box_Prompt_Stealing_against_Text-to-Image_Generative_Models_via_Reinforcement_CVPR_2026_paper.html) · [Code](https://github.com/aaFrostnova/PromptMiner) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | PROMPTMINER |
| Dataset | MS COCO + FLUX.1 dev, MS COCO + SD 3.5 Medium, MS COCO + SDXL-Turbo, DiffusionDB |

> [!tip] 效果简介
> - MS COCO + FLUX.1 dev 上，CLIP相似度 0.958 vs 最强基线 (低于0.95) (超越所有基线)。
> - MS COCO + SD 3.5 Medium 上，SBERT 文本对齐 0.751 vs 0.718 (BLIP) (+0.033)。
> - MS COCO + SDXL-Turbo 上，CLIP相似度 0.934 vs 最强基线 (低于0.93) (超越所有基线)。

## 概要

文本到图像（T2I）生成模型的提示（prompt）是决定输出内容与风格的关键控制信号，其本身具有重要的知识产权价值。**提示窃取**（prompt stealing）攻击旨在仅凭目标图像恢复出能够生成高度相似图像的提示文本，这既是对模型安全的威胁，也可用于版权取证等正当场景。现有方法面临一个共同瓶颈：白盒方法依赖模型梯度，黑盒方法缺乏显式优化，监督方法则需要大规模标注数据，三者均难以在无梯度访问且无标注数据的条件下，同时恢复精确的主体和丰富的风格修饰语。

PROMPTMINER 提出一种**两阶段黑盒提示窃取框架**，将任务解耦为：
1. **基于强化学习的提示反转**（Phase I）：将提示生成建模为马尔可夫决策过程（MDP），利用势能奖励塑形（potential-based reward shaping）提供稠密监督，高效优化离散提示空间以捕获主要主体；
2. **VLM引导的修饰语搜索**（Phase II）：以视觉语言模型（VLM）作为变异算子，通过五种定向操作（主体改写/丰富、修饰语生成/描述/风格）系统探索修饰语空间，并采用 MCTS 引导的种子选择平衡探索与利用。

**核心结论**：PROMPTMINER 在 MS COCO 数据集上搭配 FLUX.1 dev 生成器时，CLIP 相似度达到 **0.958**，SBERT 文本对齐达到 **0.751**，超越所有基线方法。在 DiffusionDB 在野图像上，CLIP 相似度比最强基线提升 **7.5%**。常见后防御手段（噪声、拼图、水印）对其影响很小，表明该方法对低层视觉扰动具有内在鲁棒性。消融实验证实，两阶段设计各自贡献显著，奖励塑形则加速收敛并稳定训练。

**方法定位**：PROMPTMINER 属于**黑盒、无监督、两阶段优化**的提示窃取方法。与 BLIP（Li et al., ICML 2022）等图像描述基线相比，它引入了显式的目标优化；与 PromptStealer（Shen et al., USENIX Security 2024）等监督方法相比，它无需大规模标注数据；与 Prometheus（Zhao et al., arXiv 2025）等依赖提示库的方法相比，它通过 VLM 变异实现了灵活的修饰语探索。其核心创新在于将强化学习的序列决策能力与 VLM 的语义理解能力相结合，在离散提示空间中实现了高效的黑盒搜索。

### 问题背景：提示窃取攻击

文本到图像（T2I）生成模型（如Stable Diffusion、FLUX）的兴起使得高质量图像创作的门槛大幅降低。用户通过精心设计的文本提示（prompt）引导模型生成特定风格和内容的图像，这些提示本身已成为具有商业价值和知识产权的创作资产。然而，攻击者可以通过“提示窃取”（prompt stealing）攻击，仅凭目标图像反向推断出生成该图像所使用的提示，从而复制或盗用原创者的创作成果。这一威胁在模型服务以黑盒API形式部署时尤为突出——攻击者只能获得输入提示所生成的输出图像，无法访问模型内部参数或梯度。

### 现有方法的局限

当前提示窃取方法可大致分为三类，但各自存在根本性瓶颈：

- **白盒方法**依赖对生成模型的梯度访问，通过优化提示嵌入或直接反推潜在表示来恢复提示。这类方法在现实场景中几乎不可行，因为商业T2I服务不会暴露模型梯度。
- **黑盒方法**无需梯度，但现有方案缺乏显式的优化目标。例如，**BLIP**（Li et al., ICML 2022）仅使用图像描述模型直接生成描述作为提示，未针对目标生成器进行适配优化；**CLIP Interrogator**（Pharmapsychotic, 2025）从预定义的修饰语池中组合提示，缺乏对特定图像的针对性搜索；**Visually Guided Decoding (VGD)**（Kim et al., 2025）虽引入LLM和CLIP引导，但本质上仍是无梯度的贪婪或随机搜索，难以高效探索庞大的离散提示空间。
- **监督方法**如**PromptStealer**（Shen et al., USENIX Security 2024）需要大规模标注数据集来训练专用的反转模型和分类器，泛化性受限于训练数据的分布，且标注成本高昂。**Prometheus**（Zhao et al., arXiv 2025）则依赖预收集的提示库进行修饰语匹配，灵活性不足。

这些方法的共同缺陷在于：**无法在无梯度访问且无大规模标注数据的情况下，同时恢复精确的主体内容和丰富的风格修饰语**。主体捕获要求对图像语义的精确对齐，而修饰语恢复则需要在巨大的离散空间中高效搜索，两者对优化策略的需求截然不同，单一阶段的方案难以兼顾。

### 本文动机与核心思路

针对上述缺口，PROMPTMINER提出将提示窃取任务**解耦为两个阶段**，分别应对主体重建和修饰语搜索的差异化挑战：

1. **基于强化学习的主体反转（Phase I）**：将提示生成建模为马尔可夫决策过程（MDP），使用强化学习在离散提示空间中进行黑盒优化。通过引入基于势能的奖励塑形（potential-based reward shaping），为每个生成步骤提供稠密的中间监督信号，显著加速收敛同时保持策略最优性。这一阶段确保核心主体语义被精确捕获。

2. **VLM引导的修饰语搜索（Phase II）**：在RL阶段获得的主体提示基础上，利用视觉语言模型（VLM）作为变异算子，通过五种针对性操作（主体改写、主体丰富、修饰语生成、修饰语描述、修饰语风格）系统探索修饰语空间。采用基于MCTS的种子选择策略平衡探索与利用，在容量受限的精英种子池中高效搜索最优修饰语组合。

这一两阶段框架从根本上改变了提示窃取的优化范式：从单阶段的“盲搜”或“直接描述”转变为“先精确捕获主体，再系统丰富修饰语”的结构化搜索过程，从而在不依赖梯度和大规模标注数据的前提下，实现了对完整提示的高质量恢复。

## 核心方法与创新机理

PROMPTMINER 的核心创新在于将**黑盒提示窃取任务解耦为两个互补阶段**，分别攻克现有方法中相互纠缠的两大瓶颈：精确主体重建与丰富修饰语恢复。这一设计直接回应了当前基线的根本缺陷——白盒方法依赖梯度访问，监督方法依赖大规模标注数据，而现有黑盒方法缺乏显式优化机制，导致无法同时恢复主体语义和风格细节。

### 从单阶段到两阶段解耦

传统提示窃取方法将主体与修饰语视为整体进行单步描述或反转，导致优化目标混杂、搜索空间低效。PROMPTMINER 将任务分解为：

1. **Phase I — 基于强化学习的主体反转**：将提示生成建模为马尔可夫决策过程（MDP），在冻结的图像描述模型之上训练轻量 RL 适配器，通过奖励塑形提供稠密中间监督，高效锁定图像中的核心主体语义。
2. **Phase II — VLM 引导的修饰语搜索**：将 RL 阶段产出的提示作为精英种子，利用视觉语言模型（VLM）驱动的五种变异算子（主体改写、主体丰富、修饰语生成、修饰语描述、修饰语风格）系统探索修饰语空间，并通过 MCTS 算法平衡探索与利用。

这一解耦使得两个阶段各司其职：RL 优化聚焦于高维离散提示空间中的主体语义对齐，VLM 搜索则利用其视觉理解与语言生成能力补充风格修饰语。消融实验（Figure 4）证实，单独使用 Phase I 即可捕获主要主体，而 Phase II 在此基础上进一步提升了 CLIP 相似度，两者结合达到最优效果。

### 关键 changed slots 对比

| 创新维度 | 基线方法 | PROMPTMINER |
|---------|---------|-------------|
| **梯度需求** | 需要（白盒方法）或未显式优化（黑盒方法） | 无需梯度；采用基于 RL 的黑盒优化 |
| **修饰语恢复** | 无或使用预定义池（CLIP-IG, PromptStealer）或提示库（Prometheus） | VLM 引导的进化搜索，含五种变异算子 |
| **训练数据需求** | 需要大规模标注数据集（PromptStealer）或提示库（Prometheus） | 无需大规模标注数据；使用冻结的描述模型和 VLM |
| **优化目标** | 单阶段描述或直接反转，无显式优化 | 两阶段：RL 进行主体捕获，VLM 进行修饰语搜索，并使用势能奖励塑形提供稠密监督 |
| **搜索效率** | 随机或贪婪搜索 | 基于 MCTS 的种子选择平衡探索与利用，容量受限的精英种子池 |

### 奖励塑形：稠密监督的关键

在 Phase I 的 RL 优化中，若仅使用终端图像相似度作为稀疏奖励（见 Eq. (2)），训练将面临严重的信用分配问题。PROMPTMINER 引入基于势能的奖励塑形（Eq. (4)），将部分生成的提示与目标图像的 CLIP 文本-图像相似度作为势函数（Eq. (5)），在每一步提供稠密中间奖励。这一设计在理论上保持最优策略不变，同时在实践中显著加速收敛（Figure 5）。消融实验表明，移除奖励塑形后训练动态明显恶化，验证了该机制对稳定 RL 训练的关键作用。

### VLM 驱动的修饰语探索

Phase II 的创新在于将 VLM 作为“变异算子”而非直接生成器。五种针对性操作覆盖了修饰语空间的不同维度：主体改写和丰富操作增强语义表达的准确性与细节，修饰语生成、描述和风格操作则系统补充风格信息。配合 MCTS 引导的种子选择，该方法在有限查询预算下实现了比随机搜索更高效的修饰语空间探索。这一设计区别于 Prometheus 依赖预收集提示库的静态方式，也克服了 CLIP Interrogator 仅从固定修饰语池选择的局限性。

### 内在鲁棒性来源

PROMPTMINER 的两阶段设计使其对低层视觉扰动具有内在鲁棒性。Phase I 的 RL 适配器在冻结描述模型的语义空间中进行优化，而非直接拟合像素级特征；Phase II 的 VLM 变异器依赖高层语义理解生成修饰语。因此，常见后防御手段（随机噪声、拼图效果、文本水印）对攻击性能的影响很小（Table 3），这与依赖精确梯度或像素级特征的白盒方法形成鲜明对比。

PROMPTMINER 将黑盒提示窃取任务解耦为两个阶段，形成“粗捕获—精修饰”的级联流水线。整体框架如 Figure 2 所示，核心设计思想是：**主体与修饰语具有不同的语义粒度和搜索难度，分开处理能显著提升恢复精度与效率**。

![[assets/figures/papers/paper_list_l2195_https_openaccess_thecvf_com_content_CVPR2026_html_Li_PROMPTMINER_Black_B/figures/002_Figure_2.jpg]]
*Figure 2: Overview of PROMPTMINER. Our method comprises two phases: (I) a reinforcement learning–based optimization phase to reconstruct the primary subject, and (II) a VLM-Guided search phase to recover stylistic modifiers*

### 输入输出流

- **输入**：一张目标图像 $x$，以及对目标文本到图像生成模型的黑盒查询权限（即仅能输入提示词并获取生成图像，无法访问梯度或内部参数）。
- **输出**：一个自然语言提示词，使得目标生成器据此生成的图像 $\hat{x}$ 在语义和风格上与 $x$ 高度相似。

### 两阶段流水线

**Phase I：基于强化学习的提示反转（RL-Based Prompt Inversion）**

该阶段负责恢复图像中的**主要主体**（primary subject）。其核心是将提示生成形式化为一个马尔可夫决策过程（MDP），并在冻结的图像描述模型之上训练一个轻量级 RL 适配器（RL Adapter $\theta$）。适配器接收描述模型的隐藏状态，输出动作 logits 以自回归方式生成提示词。训练采用近端策略优化（PPO），并引入基于势能的奖励塑形（potential-based reward shaping），将稀疏的终端图像相似度奖励转化为稠密的中间监督信号，从而加速收敛并保持策略最优性不变。Phase I 输出的提示词已能捕获图像的核心语义内容，但通常缺乏风格和细节修饰。

**Phase II：VLM引导的提示优化（VLM-Guided Prompt Optimization）**

该阶段在 Phase I 的结果基础上，进一步恢复**风格修饰语**（stylistic modifiers）。它维护一个容量受限的精英种子池（seed pool），并利用视觉语言模型（VLM，如 Qwen2-VL）作为变异器，通过五种定向操作（主体改写、主体丰富、修饰语生成、修饰语描述、修饰语风格）系统性地探索修饰语空间。每次迭代中，采用基于蒙特卡洛树搜索（MCTS）的选择策略从种子池中挑选最有潜力的候选提示进行变异，生成的新提示经目标生成器合成图像后，由 CLIP 相似度评估并决定是否进入种子池。这种设计在探索与利用之间取得平衡，使修饰语搜索既高效又多样。

### 模块关系

两阶段之间存在明确的**顺序依赖**：Phase I 的输出作为 Phase II 种子池的初始种子，为修饰语搜索提供高质量的语义锚点。消融实验（Figure 4）证实，单独使用 Phase I 已能捕获主要主体，但 CLIP 相似度有限；加入 Phase II 后，修饰语的补充使相似度进一步提升，两者结合达到最佳效果。

### 两阶段框架总览

PROMPTMINER将提示窃取任务解耦为两个阶段（Figure 2）：

- **Phase I: RL-Based Prompt Inversion** — 基于强化学习的主体重建阶段，将提示反转形式化为马尔可夫决策过程（MDP），利用奖励塑形高效优化离散提示空间，恢复主要主体。
- **Phase II: VLM-Guided Prompt Optimization** — VLM引导的修饰语搜索阶段，使用视觉语言模型作为变异器，通过进化搜索恢复风格修饰语。

### 关键模块

| 模块 | 角色 | 证据锚点 |
|------|------|----------|
| 冻结的图像描述模型 (Frozen Captioner) | 生成初始文本表示并提供隐藏状态，作为策略网络的骨干 | Figure 2; Section 3.3 |
| RL适配器 (RL Adapter θ) | 可训练的策略网络，接收隐藏状态并输出动作logits，通过PPO优化 | Section 3.3, Eq. (6) |
| 价值头 (Value Head) | 估计状态价值，用于PPO中的优势计算 | Section 3.3 |
| VLM变异器 (VLM Mutator) | 使用VLM（如Qwen2-VL）通过五种操作生成提示变体：主体改写、主体丰富、修饰语生成、修饰语描述、修饰语风格 | Section 3.4 |
| 种子池与MCTS选择器 | 维持容量受限的精英种子池，利用MCTS算法平衡探索与利用 | Section 3.4 |
| CLIP图像与文本编码器 | 计算图像相似度奖励（Ψ）和势函数（Φ），提供奖励塑形和最终评价 | Eq. (3, 5) |

### 核心公式推导

**自回归描述概率** — 给定目标图像 $x$，生成完整提示 $p_{0:T}$ 的概率按自回归方式分解：

$$P(p_{0:T} \mid x) = \prod_{t=0}^{T} P(p_t \mid p_{<t}, x) \quad \text{(Eq. 1)}$$

**稀疏奖励** — 在生成过程中奖励为零，仅在终端时刻给出生成图像与目标图像的相似度：

$$r_t = \begin{cases} 0, & 0 \leq t < T, \\ \Psi(x, \hat{x}), & t = T \end{cases} \quad \text{(Eq. 2)}$$

其中 $\hat{x}$ 为根据生成提示合成的图像。

**图像相似度** — 使用CLIP图像编码器 $f_{\mathrm{img}}$ 计算余弦相似度：

$$\Psi(\hat{x}, x) = \frac{f_{\mathrm{img}}(\hat{x}) \cdot f_{\mathrm{img}}(x)}{\|f_{\mathrm{img}}(\hat{x})\| \|f_{\mathrm{img}}(x)\|} \quad \text{(Eq. 3)}$$

**势函数** — 部分生成的提示与目标图像的CLIP文本-图像相似度，乘以缩放系数 $\beta$ 作为势能：

$$\Phi(s_t) = \beta \cdot \frac{f_{\mathrm{text}}(p_{1:t}) \cdot f_{\mathrm{img}}(x)}{\|f_{\mathrm{text}}(p_{1:t})\| \|f_{\mathrm{img}}(x)\|} \quad \text{(Eq. 5)}$$

其中 $s_t$ 为当前状态（包含已生成的部分提示），$f_{\mathrm{text}}$ 为CLIP文本编码器。

**塑形奖励** — 基于势函数的奖励塑形，提供稠密中间奖励并保持最优策略不变：

$$r_t' = \begin{cases} \gamma \Phi(s_{t+1}) - \Phi(s_t), & 0 \leq t < T, \\ r_t - \Phi(s_t), & t = T \end{cases} \quad \text{(Eq. 4)}$$

其中 $\gamma$ 为折扣因子。该塑形将稀疏的终端奖励转化为每一步的稠密信号，显著加速收敛（消融实验证实，见Figure 5）。

**模仿学习损失** — 使用冻结的语言模型头对适配器进行预热训练，最小化下一词预测的交叉熵：

$$\mathcal{L}_{\mathrm{IL}} = -\frac{1}{N} \sum_{(h_t, y_{t+1})} \log P_{\mathrm{LM}}(y_{t+1} \mid \tilde{h}_t) \quad \text{(Eq. 7)}$$

其中 $h_t$ 为冻结骨干的隐藏状态，$\tilde{h}_t$ 为经适配器变换后的隐藏状态，$y_{t+1}$ 为真实下一词。该预热阶段仅更新适配器参数 $\theta$，为后续RL训练提供强语义初始化。

**PPO裁剪替代目标** — 通过裁剪重要性权重 $\rho_t(\theta)$ 防止策略更新过大：

$$\mathcal{L}_{\mathrm{PPO}} = \mathbb{E}_t \Big[ \min \big( \rho_t(\theta) A_t, \ \mathrm{clip}(\rho_t(\theta), 1-\epsilon, 1+\epsilon) A_t \big) \Big] \quad \text{(Eq. 8)}$$

其中 $A_t$ 为优势函数，$\epsilon$ 为裁剪阈值。该损失函数是Phase I策略优化的核心。

### 瓶颈与机制总结

现有方法的核心瓶颈在于：白盒方法依赖梯度访问，黑盒方法缺乏显式优化目标，监督方法需要大规模标注数据。PROMPTMINER通过以下机制突破这些限制：

1. **RL + 奖励塑形**：将离散提示搜索形式化为MDP，利用势能奖励塑形提供稠密监督，使策略在无梯度条件下高效收敛。
2. **VLM引导的进化搜索**：利用预训练VLM的语义理解能力，通过五种定向变异算子系统探索修饰语空间，无需预定义提示库或标注数据。
3. **MCTS种子选择**：在容量受限的精英种子池中，使用蒙特卡洛树搜索平衡探索与利用，提升搜索效率。

## 实验与关键发现

### 主要定量结果

PROMPTMINER 在多个基准数据集和目标生成模型上均一致地超越了所有基线方法。Table 1 报告了在 MS COCO 数据集上，针对三种主流文本到图像生成模型（FLUX.1 dev、SD 3.5 Medium、SDXL-Turbo）的图像相似度与文本对齐指标对比。

![[assets/figures/papers/paper_list_l2195_https_openaccess_thecvf_com_content_CVPR2026_html_Li_PROMPTMINER_Black_B/figures/003_Table_1.jpg]]
*Table 1: Image similarity and textual alignment comparison across datasets*

在图像相似度方面，PROMPTMINER 在 FLUX.1 dev 上达到 **CLIP 相似度 0.958**，超越所有基线；在 SDXL-Turbo 上达到 **0.934**，同样领先。在感知相似度指标 LPIPS 上，PROMPTMINER 在 SD 3.5 Medium 上取得最低值 **0.303**，表明其生成的图像在感知层面与目标图像最为接近。

在文本对齐方面，PROMPTMINER 在 SD 3.5 Medium 上达到 **SBERT 文本对齐 0.751**，显著优于最强基线 BLIP 的 0.718（+0.033），说明恢复的提示在语义层面更准确地描述了目标图像内容。

### 在野图像泛化能力

为评估方法的实际泛化能力，Table 2 报告了在 DiffusionDB 数据集（来源于未知生成器的在野图像）上的提示窃取性能。PROMPTMINER 取得 **CLIP 相似度 0.863**，比最强基线（约 0.803）相对提升 **7.5%**。这一结果表明，PROMPTMINER 的两阶段设计——RL 主体捕获与 VLM 修饰语搜索——即使在生成器未知、图像分布与训练数据差异较大的场景下，仍能有效恢复高质量的提示。

![[assets/figures/papers/paper_list_l2195_https_openaccess_thecvf_com_content_CVPR2026_html_Li_PROMPTMINER_Black_B/figures/006_Table_2.jpg]]
*Table 2: Prompt stealing performance on in-the-wild images*

### 消融实验

**两阶段贡献分析**（Figure 4）：消融实验考察了 Phase I（RL-Based Prompt Inversion）和 Phase II（VLM-Guided Prompt Optimization）在不同查询预算下对 CLIP 相似度的独立与联合贡献。结果表明，Phase I 的 RL 反转已能捕获主要主体并获得较高的基础相似度，而 Phase II 的 VLM 优化在此基础上进一步加入风格修饰语，持续提升 CLIP 相似度。两阶段结合在所有查询预算下均取得最优效果，验证了解耦设计的有效性。

**奖励塑形的作用**（Figure 5）：对比有无势能奖励塑形（potential-based reward shaping）的训练动态曲线。引入塑形奖励后，训练收敛速度显著加快，且最终性能更稳定。这得益于势函数 $\Phi(s_t)$ 在生成过程中提供稠密的中间监督信号（Eq. 4-5），缓解了稀疏奖励问题，同时保持了策略最优性不变。

**MCTS 种子选择的有效性**：在 Phase II 的 VLM 引导搜索中，基于 MCTS 的种子选择策略通过平衡探索与利用，相比随机选择能更高效地探索修饰语空间，在相同查询预算下获得更高的 CLIP 相似度提升。

### 用户研究

Figure 6 展示了用户研究结果，参与者在图像相似度和语义丰富性两个维度上对不同方法恢复的提示进行评分。PROMPTMINER 在两个维度上均获得最高评分，表明其恢复的提示不仅能生成与目标图像高度相似的图像，还包含了更丰富的语义修饰信息。

![[assets/figures/papers/paper_list_l2195_https_openaccess_thecvf_com_content_CVPR2026_html_Li_PROMPTMINER_Black_B/figures/007_Figure_6.jpg]]
*Figure 6: Ratings from the user study*

### 防御策略评估

Table 3 评估了三种常见的后处理防御策略对 PROMPTMINER 的影响：随机噪声、拼图效果（jigsaw）和文本水印。实验结果表明，这些低层视觉扰动对 PROMPTMINER 的 CLIP 相似度影响很小，攻击性能仅出现轻微下降。这说明 PROMPTMINER 对像素级扰动具有内在鲁棒性——其 RL 阶段通过高层语义相似度进行优化，VLM 阶段依赖语义理解而非像素匹配，因此简单的图像后处理难以构成有效防御。

![[assets/figures/papers/paper_list_l2195_https_openaccess_thecvf_com_content_CVPR2026_html_Li_PROMPTMINER_Black_B/figures/009_Table_3.jpg]]
*Table 3: Potential defenses against PROMPTMINER*

### 公平性保障

所有对比实验在相同的黑盒查询预算下进行，确保各方法在资源约束上的公平性。在野图像实验统一使用 DiffusionDB 数据源，所有基线处于相同的未知生成器条件下。防御评估仅对目标图像施加后处理变换，未修改生成器内部参数，保持攻击场景的一致性。

### 失败模式与局限性

尽管 PROMPTMINER 在多数场景下表现优异，仍存在以下局限：

1. **查询效率依赖**：方法依赖对目标 T2I 生成模型的黑盒查询，若查询次数受到严格限制，攻击效率会下降。当前实验在给定的查询预算下已展现高效性，但极端低预算场景仍需进一步验证。

2. **VLM 域外泛化**：VLM 引导的修饰语搜索依赖于预训练视觉语言模型（如 Qwen2-VL）的性能。对于域外或高度风格化的图像（如抽象艺术、非自然场景），VLM 可能无法生成恰当的修饰语描述，导致 Phase II 的优化增益有限。

3. **运行时间开销**：当前评估集中于图像质量和文本对齐指标，未充分考量两阶段优化（特别是 VLM 迭代搜索）带来的运行时间开销，实际部署时需权衡效率与效果。

![[assets/figures/papers/paper_list_l2195_https_openaccess_thecvf_com_content_CVPR2026_html_Li_PROMPTMINER_Black_B/figures/004_Figure_3.jpg]]
*Figure 3: Visualization of generated images compared with target image*

## 定位与知识库关联

### 核心瓶颈与设计动机

现有提示窃取方法面临一个根本性困境：**白盒方法**依赖目标生成器的梯度信息，在现实黑盒场景中不可行；**黑盒方法**则缺乏显式优化目标，仅通过描述模型或预定义池生成提示，无法同时恢复精确的主体语义和丰富的风格修饰语。具体而言：

- **BLIP**（Li et al., ICML 2022）直接使用图像描述模型生成提示，本质是“描述”而非“窃取”，输出的提示缺乏针对特定生成器的优化，难以复现目标图像的风格细节。
- **CLIP Interrogator**（Pharmapsychotic, 2025）从预定义的修饰语池中组合提示，虽然能覆盖部分风格词汇，但池的静态性限制了其对新图像或新风格的适应能力。
- **PromptStealer**（Shen et al., USENIX Security 2024）采用监督学习范式，需要大规模标注的提示-图像对训练反转模型和分类器，数据获取成本高，且泛化到未见生成器的能力有限。
- **Prometheus**（Zhao et al., arXiv 2025）依赖预收集的提示库进行修饰语搜索，灵活性受限于库的覆盖范围。
- **Visually Guided Decoding (VGD)**（Kim et al., 2025）是较近的黑盒硬提示反转方法，通过LLM+CLIP引导生成主体，但缺乏对修饰语空间的系统探索，恢复的提示在风格丰富性上不足。

PROMPTMINER的核心洞察在于将提示窃取任务**解耦为两个阶段**：主体捕获与修饰语搜索。这一解耦使得每个阶段可以采用最适合的优化策略——强化学习（RL）处理离散提示空间的序列决策，视觉语言模型（VLM）提供语义感知的变异操作——从而在无需梯度访问和无需大规模标注数据的约束下，同时提升主体精确度和修饰语丰富度。

### 方法谱系定位

从技术路线看，PROMPTMINER处于**黑盒优化**与**VLM辅助搜索**的交汇点，其设计融合了多个领域的成熟技术，但组合方式具有创新性：

| 技术组件 | 来源脉络 | PROMPTMINER的改进 |
|----------|----------|-------------------|
| 基于RL的文本生成 | 文本生成领域的策略梯度方法（PPO, Schulman et al., 2017） | 引入势能奖励塑形（potential-based reward shaping），将CLIP文本-图像相似度作为稠密中间奖励，加速收敛并保持策略最优性（Eq. 4-5） |
| 奖励塑形 | Ng et al., 1999的势能塑形理论 | 首次应用于提示窃取的RL训练中，消融实验（Figure 5）证实其显著加速收敛 |
| VLM引导的进化搜索 | 进化算法在提示优化中的应用 | 设计五种语义感知的变异算子（主体改写、主体丰富、修饰语生成、修饰语描述、修饰语风格），利用VLM的视觉理解能力进行定向探索，而非随机变异 |
| MCTS种子选择 | 蒙特卡洛树搜索在组合优化中的应用 | 在容量受限的精英种子池中平衡探索与利用，优于随机选择策略 |

### 适用边界

PROMPTMINER的有效性建立在以下前提之上：

1. **黑盒查询可用**：攻击者需要能够调用目标T2I生成模型并获取生成图像。若查询次数受限，RL训练和VLM搜索的效率会下降，但论文在有限查询预算（Figure 4）下已展现有效性。
2. **VLM的语义理解能力**：Phase II的修饰语搜索依赖VLM（如Qwen2-VL）对图像内容的理解。对于高度风格化、抽象或域外图像，VLM可能无法生成恰当的修饰语变异，导致搜索效率下降。
3. **CLIP编码器的语义对齐**：奖励函数（Eq. 3）和势函数（Eq. 5）均依赖CLIP的跨模态对齐质量。对于CLIP表征能力较弱的细粒度属性（如精确的纹理、排版、构图），优化信号可能不够精确。
4. **生成器的确定性或低随机性**：方法假设同一提示在目标生成器上产生一致或高度相似的输出。若生成器具有强随机性（如高噪声调度），基于图像相似度的奖励信号将变得嘈杂。

### 局限与开放问题

**已知局限**（论文承认或可从设计推断）：

- **查询依赖**：尽管在给定预算下高效，但攻击本质上需要多次黑盒查询，无法像某些监督方法那样单次推理完成。
- **VLM瓶颈**：修饰语搜索的质量上限受限于所用VLM的视觉理解和语言生成能力，对于超出VLM训练分布的图像类型可能退化。
- **知识产权风险**：方法可被滥用于窃取创作者精心设计的提示，带来版权和商业利益威胁。论文虽强调正当取证用途，但未提供技术性防护方案。
- **运行时间开销**：两阶段优化涉及RL训练和多轮VLM变异，论文未充分讨论时间成本，尽管附录可能提供查询次数分析。

**开放问题**：

1. **防御机制的设计空间**：Table 3评估的后防御（随机噪声、拼图效果、文本水印）对PROMPTMINER影响较小，说明其对低层视觉扰动具有内在鲁棒性。如何设计能有效抵抗基于RL和VLM的提示窃取、同时不显著损害生成图像质量的防御机制？可能的路径包括在生成器端引入对抗训练、差分隐私提示编码，或设计语义层面的扰动。

2. **跨模态泛化**：PROMPTMINER的两阶段框架（RL主体捕获 + VLM修饰语搜索）是否适用于其他生成模态？例如文本到视频、文本到3D等任务中，“提示”的语义结构类似，但时序或空间维度的引入会显著增加搜索空间和评估复杂度。

3. **动态生成器的鲁棒性**：若目标生成器的内部参数随时间变化（如在线更新的模型），或采用动态提示编码（如提示被映射到变化的嵌入空间），攻击的跨时间泛化能力如何？这需要评估方法对生成器分布偏移的敏感度。

4. **更严格的威胁模型**：当前假设攻击者可获得生成图像。若防御方对输出图像施加更强的语义扰动（如对抗性重绘、语义替换），或限制生成图像的分辨率/质量，攻击的有效性是否会显著下降？

5. **VLM变异算子的可扩展性**：当前五种变异算子覆盖了主体和修饰语的常见变换，但对于更复杂的提示结构（如多主体交互、空间布局指令、负面提示），是否需要设计新的变异算子？VLM能否可靠地执行这些更复杂的语义操作？

## 原文 PDF

![[paperPDFs/CVPR_2026/PROMPTMINER_Black_Box_Prompt_Stealing_against_Text_to_Image_Generative_Models_via_Reinforcement_Learning_and_VLM_Guided_Optimization.pdf]]
