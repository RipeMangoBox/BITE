---
title: "JANUS: A Lightweight Framework for Jailbreaking Text-to-Image Models via Distribution Optimization"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/JANUS_A_Lightweight_Framework_for_Jailbreaking_Text_to_Image_Models_via_Distribution_Optimization.pdf
project_link: null
code_link: "https://github.com/dimshimmer/JANUS"
aliases:
- JANUS
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 将离散提示搜索转化为在低维语义锚定分布上的连续混合策略优化。通过构建有害与清洁两个语义锚定高斯分布的凸组合，并利用轻量级策略梯度直接最大化端到端黑盒奖励（绕过安全过滤器且生成高有害内容），从而在无白盒梯度、无大规模生成器的条件下精准控制提示的‘有害性’与‘语义保持’的平衡。
primary_logic: 越狱提示的语义结构与有害性是可解耦的。通过建模两个语义锚定分布的线性叠加（类比波的干涉），能使共享的核心语义形成‘建设性干涉’而保持稳定，同时仅通过调节一个标量混合系数α即可在低维空间中高效探索绕过与有害性的最优均衡。这种分布级优化范式既避免了代理损失的目标错位，又摆脱了对大容量生成器的依赖。
claims:
- JANUS将越狱攻击形式化为在T2I系统及安全过滤器的黑盒端到端奖励下优化结构化提示分布，取代大容量生成器为低维混合策略。
- 在Stable Diffusion 3.5 Large Turbo上，攻击成功率ASR-8从25.30%显著提升至43.15%，并同时获得更高的CLIP和NSFW分数。
- 双分布干扰（Unimodal消融）和动态奖励（Fix NSFW消融）对最终性能至关重要，完整框架在ASR和NSFW指标上均优于变体。
- 在计算效率上，JANUS相对于优化类基线（MMA、MMP）实现了约18倍和12倍的加速，且无需记忆密集型大语言模型。
---

# JANUS: A Lightweight Framework for Jailbreaking Text-to-Image Models via Distribution Optimization

> [!tip] 核心洞察
> 越狱提示的语义结构与有害性是可解耦的。通过建模两个语义锚定分布的线性叠加（类比波的干涉），能使共享的核心语义形成‘建设性干涉’而保持稳定，同时仅通过调节一个标量混合系数α即可在低维空间中高效探索绕过与有害性的最优均衡。这种分布级优化范式既避免了代理损失的目标错位，又摆脱了对大容量生成器的依赖。

| 字段 | 内容 |
|------|------|
| 中文题名 | JANUS：一种通过分布优化实现文本到图像模型越狱攻击的轻量级框架 |
| 英文题名 | JANUS: A Lightweight Framework for Jailbreaking Text-to-Image Models via Distribution Optimization |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.21208) · [Code](https://github.com/dimshimmer/JANUS) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | JANUS |
| Dataset | Stable Diffusion 3.5 Large Turbo, DALL·E3, Stable Diffusion XL, Midjourney |

> [!tip] 效果简介
> - Stable Diffusion 3.5 Large Turbo (SD3.5LT) 上，ASR-8 (攻击成功率@8次采样) 43.15% vs 25.30% (QFA) (+17.85%)；CLIP Score/N SFW Score 0.37 / 0.33 vs 0.31 / 0.28 (QFA) (+0.06 / +0.05)。
> - DALL·E3 上，ASR-8 3.39% vs 0.00% (SneakyPrompt) (+3.39%)。
> - Stable Diffusion XL (SDXL) 上，ASR-8 58.20% vs 36.40% (SneakyPrompt, best competitor) (+21.80%)。

## 概要

**问题背景**：文本到图像（T2I）生成模型在安全机制上存在脆弱性，攻击者可通过越狱提示（jailbreak prompts）诱导模型生成违规内容。现有越狱攻击方法面临两大根本矛盾：提示级优化依赖代理损失（如语义相似度约束）而非真实的“绕过+有害性”端到端目标，而生成器级优化则需要大规模语言模型（数十亿参数）的强化学习，计算代价高昂且普适性差。这导致在真实黑盒场景下，攻击成功率与效率难以兼顾。

**核心洞察**：越狱提示的语义结构与有害性是可解耦的。通过建模两个语义锚定分布的线性叠加（类比波的干涉），能使共享的核心语义形成“建设性干涉”而保持稳定，同时仅通过调节一个标量混合系数α即可在低维空间中高效探索绕过与有害性的最优均衡。

**提出方法**：**JANUS** 是一个轻量级、无需大语言模型的两阶段框架。它将离散提示搜索转化为在低维语义锚定分布上的连续混合策略优化——构建有害与清洁两个语义锚定高斯分布的凸组合，并利用轻量级策略梯度直接最大化端到端黑盒奖励（绕过安全过滤器且生成高有害内容），从而在无白盒梯度、无大规模生成器的条件下精准控制提示的“有害性”与“语义保持”的平衡。

**主要结果**：
- 在 Stable Diffusion 3.5 Large Turbo 上，攻击成功率 ASR-8 从 25.30% 显著提升至 **43.15%**，同时获得更高的 CLIP 和 NSFW 分数（Table 1）。
- 在 Stable Diffusion XL 上，ASR-8 达到 **58.20%**，较最佳基线提升 21.80 个百分点。
- 在商业闭源模型 DALL·E3 和 Midjourney 上也取得了正向攻击增益（ASR-8 分别为 3.39% 和 6.20%），表明方法对不同类型的商业安全过滤器具有一定穿透能力。
- 计算效率方面，JANUS 相对于优化类基线 MMA 和 MMP 分别实现了约 **18 倍和 12 倍的加速**，且无需记忆密集型大语言模型（Table 3）。

**方法定位**：JANUS 属于分布优化范式，区别于逐提示离散梯度优化（如 MMA、MMP）和大容量生成器强化学习（如 SneakyPrompt、PGJ）。其核心创新在于将越狱攻击形式化为结构化提示分布的端到端黑盒优化，通过双锚点分布的凸组合保证语义下界，同时以标量混合系数 α 作为唯一的策略参数，在极低维度上完成高效的策略梯度搜索。

### 文本到图像生成与安全过滤

文本到图像（T2I）系统将自然语言提示映射为视觉内容，其形式化定义为映射 $M : \mathcal{P} \to \mathcal{V}$，其中提示 $\mathbf{p} = [t_1, t_2, \ldots, t_L] \in \mathbb{N}^L$ 是长度为 $L$ 的令牌序列。为防止生成有害内容，主流部署通常集成多层安全过滤机制，包括文本级分类器和图像级安全检测器。安全过滤器可抽象为二值函数 $C(\mathbf{p}, M(\mathbf{p})) \to \{0, 1\}$，输出 $1$ 表示内容通过安全检查，$0$ 表示被拦截。

### 越狱攻击的核心矛盾

越狱攻击旨在构造对抗性提示 $\mathbf{p}_{\mathrm{adv}}$，使其同时满足三个条件：**绕过安全过滤器**（$C(\mathbf{p}_{\mathrm{adv}}, M(\mathbf{p}_{\mathrm{adv}})) = 1$）、**保持与原始有害提示的语义相似性**、以及**诱导模型生成实际有害内容**。现有方法在解决这一多目标优化问题时，面临两个根本性矛盾：

1. **提示级优化依赖代理损失**：基于离散梯度优化的方法（如 **MMA**，采用 GCG 风格搜索）和连续嵌入空间搜索方法（如 **MMP**）通过手工设计的语义相似度约束来引导搜索，而非直接优化“绕过+有害性”的端到端目标。这种代理损失与真实攻击目标之间存在目标错位（objective misalignment），导致优化过程难以精准收敛到高效越狱解。

2. **生成器级优化计算代价高昂**：基于强化学习的方法（如 **SneakyPrompt**）需要训练大容量语言模型（数十亿参数）作为提示生成器，通过 RL 微调来学习越狱策略。这不仅消耗大量计算资源，还因对特定模型和过滤器的过拟合而缺乏跨模型的普适性。

### 关键洞察：语义与有害性的可解耦性

上述困境的根源在于现有方法将语义保持和有害性探索耦合在同一个高维离散搜索空间中。JANUS 的核心洞察是：**越狱提示的语义结构与有害性是可以解耦的**。通过将离散提示松弛为两个语义锚定高斯分布的凸组合——一个锚定于有害语义（$N_t$），另一个锚定于清洁语义（$N_c$）——共享的核心语义可以形成“建设性干涉”而保持稳定，同时仅需调节一个标量混合系数 $\alpha \in [0,1]$ 即可在低维空间中高效探索绕过与有害性的最优均衡。这种分布级优化范式既避免了代理损失的目标错位，又摆脱了对大容量生成器的依赖。

### JANUS 的设计动机

基于上述洞察，JANUS 被设计为一个**轻量级、无大语言模型的两阶段框架**：第一阶段构建双锚点语义分布模型，结构性地保障语义相似度下界；第二阶段采用轻量级策略梯度优化器，在黑盒条件下直接最大化端到端奖励（绕过安全过滤器且生成高有害内容）。这种范式将离散搜索转化为可处理的连续优化问题，实现了攻击成功率与计算效率的双重突破——在 Stable Diffusion 3.5 Large Turbo 上，JANUS 将 ASR-8 从 25.30% 提升至 43.15%，同时相对于优化类基线实现了约 18 倍（对 MMA）和 12 倍（对 MMP）的加速，且无需任何大语言模型参与。

## 核心方法与创新机理

JANUS的核心创新在于将越狱攻击从“搜索单条最优提示”的离散优化范式，彻底重构为“学习一个结构化提示分布”的连续优化问题。这一范式转换通过三个紧密耦合的**changed slots**实现，系统性地解决了现有方法的根本瓶颈。

### 优化范式：从离散搜索到低维混合策略优化

现有越狱方法在优化范式上陷入两难困境：**MMA**（硬优化，基于GCG的离散提示搜索）和**MMP**（软优化，连续嵌入空间搜索）等提示级方法依赖代理损失（如语义相似度约束）而非真实的“绕过+有害性”端到端目标，导致目标错位；而**SneakyPrompt**等生成器级方法需要大规模语言模型（数十亿参数）的强化学习训练，计算代价高昂且普适性受限。

JANUS将这一困境解耦为两个正交子问题：**语义保持**与**对抗探索**。具体而言，JANUS用一个低维混合策略替代大容量生成器——仅需学习一个标量混合系数 $$$\alpha \in [0,1]$$$，即可在有害锚点分布 $N_t$ 与清洁锚点分布 $N_c$ 的凸组合上实现高效探索：

$$p_{\alpha} = \alpha N_t + (1-\alpha) N_c$$

这一设计使得优化空间从离散提示的指数级组合空间，压缩至一维连续空间，从根本上避免了离散搜索的组合爆炸问题。在计算效率上，JANUS相对于优化类基线实现了约**18倍**（vs. MMA）和**12倍**（vs. MMP）的加速（Table 3），且无需记忆密集型大语言模型。

### 语义保持机制：从代理损失到结构化语义下界

现有方法（如**QFA**的查询反馈优化、**PGJ**的提示级生成器优化）通常采用手工设计的代理损失（如语义相似度约束）来维持对抗提示与原始提示的语义一致性。然而，代理损失与真实越狱目标之间存在固有的目标错位——优化代理损失并不能保证实际绕过安全过滤器或生成高有害内容。

JANUS通过双锚点分布的线性叠加，结构性地保证了语义相似度的下界（Eq.(8)）：

$$\mathbb{E}_{\mathbf{p}\sim p_{\alpha}}[\mathcal{L}(e(\mathbf{p}),\mathbf{e_t})] \geq \min(\mathbb{E}_{\mathbf{p}\sim N_t}[\mathcal{L}(e(\mathbf{p}),\mathbf{e_t})], \mathbb{E}_{\mathbf{p}\sim N_c}[\mathcal{L}(e(\mathbf{p}),\mathbf{e_t})])$$

这一下界意味着：无论混合系数 $$$\alpha$$$ 如何变化，生成的对抗提示与目标提示的语义相似度，始终不低于两个基础分布中较弱者的期望相似度。这种“语义稳定性由设计保证”的机制，使得优化过程无需额外引入语义正则项，从根本上消除了代理损失带来的目标错位风险。

消融实验（Table 2）验证了这一设计的核心作用：移除双分布干扰（仅用单一分布Unimodal）导致ASR和NSFW分数大幅下降，证实语义锚定混合空间对越狱性能至关重要。

### 优化信号：从白盒梯度到黑盒端到端联合奖励

现有提示级优化方法依赖白盒梯度（如通过模型反向传播计算提示嵌入的梯度），这在实际黑盒商业模型（如DALL·E3、Midjourney）上完全不可行。生成器级方法虽不要求白盒访问，但需要大量查询反馈来训练生成器，效率极低。

JANUS采用纯黑盒端到端联合奖励信号，直接最大化越狱成功的真实目标。能量函数（Eq.(9)）将安全过滤器绕过状态 $C(\cdot)$ 与输出有害性评分 $S(\cdot)$ 结合为单一标量反馈：

$$E(\mathbf{p}) = -C(\mathbf{p}, M(\mathbf{p})) \cdot S(M(\mathbf{p}))$$

越成功的越狱提示（既绕过过滤器又生成高有害内容）获得更低的能量值。基于此，JANUS将自由能最小化转化为最大化期望奖励的强化学习目标（Eq.(10)）：

$$J(\alpha) = \mathbb{E}_{\mathbf{p}\sim p_{\alpha}}[R(\mathbf{p})], \quad R(\mathbf{p}) = -(E(\mathbf{p}) + \log p_{\alpha}(\mathbf{p}))$$

其中对数策略梯度（Eq.(11)）仅需两个基础分布的概率密度即可计算，完全无需白盒模型参数或梯度：

$$\nabla_{\alpha} \log p_{\alpha}(\mathbf{p}) = \frac{N_t(\mathbf{p}) - N_c(\mathbf{p})}{\alpha N_t(\mathbf{p}) + (1-\alpha)N_c(\mathbf{p})}$$

消融实验进一步揭示了动态奖励的关键性：使用固定NSFW奖励（Fix NSFW）替换动态奖励会显著降低最终NSFW分数（Table 2），而固定混合系数 $$$\alpha$$$（不进行策略学习）则在过滤逃避与有害性之间产生次优权衡（Figure 4）。只有RL学习的动态 $$$\alpha$$$ 策略能取得全面更优的越狱表现。

### 创新总结

JANUS的三个changed slots形成了紧密的因果链条：**低维混合策略**提供了高效的探索空间，**结构化语义下界**消除了对代理损失的依赖，**黑盒端到端奖励**则使优化目标与真实越狱成功直接对齐。这一设计使得JANUS在Stable Diffusion 3.5 Large Turbo上将ASR-8从25.30%显著提升至43.15%，同时获得更高的CLIP和NSFW分数（Table 1），并在SDXL（58.20% vs. 36.40%）和Midjourney（6.20% vs. 3.28%）等多样化模型上保持领先（Table 4），验证了范式转换的泛化能力。

JANUS 将越狱攻击从传统的离散提示搜索或大容量生成器强化学习，重新形式化为**在低维语义锚定分布上的连续混合策略优化**。其核心思想是将“语义保持”与“有害性探索”两个目标解耦，通过构造两个语义锚定高斯分布的凸组合来结构化地保障语义下界，再以轻量级策略梯度直接在黑盒端到端奖励信号下优化混合系数。整个框架由两个阶段级联构成，如图2所示。

### 输入与输出流

- **输入**：一个目标有害提示 $p_t$（如包含 NSFW 内容的原始文本）及其对应的“清洁”改写版本 $p_c$。
- **输出**：一个优化后的提示分布 $p_\alpha$，从中采样得到的提示能够以高概率绕过文本和图像层面的安全过滤器，同时诱导 T2I 模型生成与原始有害意图对齐的图像。

### 第一阶段：语义锚定分布建模

该阶段将离散的硬提示松弛为可训练的**令牌级概率分布**。具体而言，以目标提示 $p_t$ 和清洁提示 $p_c$ 为锚点，分别构造两个语义锚定的基础分布 $N_t$ 和 $N_c$。每个分布定义在提示的令牌序列空间上，其中每个位置的令牌选择服从以原始令牌为中心的高斯型软分配。随后，通过一个标量混合系数 $\alpha \in [0, 1]$ 将两者线性组合为混合分布：

$$p_{\alpha} = \alpha N_t + (1-\alpha) N_c$$

这一凸组合结构具有关键的**语义稳定性保证**：从 $p_\alpha$ 中采样得到的提示与目标提示的语义相似度期望，被两个基础分布中较弱者的期望所下界（Eq. 8），从而结构性地避免了优化过程中语义的灾难性漂移。

### 第二阶段：基于策略的黑盒优化

在第一阶段构建的参数化分布 $p_\alpha$ 之上，JANUS 将越狱攻击转化为一个强化学习问题。混合系数 $\alpha$ 作为策略参数，优化目标为最大化从 $p_\alpha$ 采样提示的端到端黑盒奖励：

$$J(\alpha) = \mathbb{E}_{p \sim p_\alpha}[R(p)], \quad R(p) = -(E(p) + \log p_\alpha(p))$$

其中能量函数 $E(p) = -C(p, M(p)) \cdot S(M(p))$ 联合评估安全过滤器的绕过状态 $C(\cdot)$ 和生成图像的 NSFW 有害性评分 $S(\cdot)$。越成功的越狱提示能量越低，奖励越高。

JANUS 采用 **REINFORCE 风格的策略梯度**更新 $\alpha$，其梯度形式仅需计算两个基础分布的概率密度比：

$$\nabla_{\alpha} \log p_{\alpha}(p) = \frac{N_t(p) - N_c(p)}{\alpha N_t(p) + (1-\alpha)N_c(p)}$$

这一设计使得整个优化过程**无需访问 T2I 模型的参数或梯度**，也无需大语言模型作为生成器，仅依赖黑盒查询反馈即可完成端到端学习。

### 模块间的协作关系

两个阶段形成“松弛—优化”的闭环：第一阶段提供语义结构化的搜索空间，将离散的组合爆炸问题压缩为单一连续参数 $\alpha$ 的优化；第二阶段以黑盒奖励为驱动，在保持语义下界的前提下动态调节 $\alpha$，在“绕过安全过滤器”与“生成高有害内容”之间寻找最优均衡。消融实验（Table 2）证实，移除双分布建模（Unimodal 变体）或使用固定 NSFW 奖励（Fix NSFW 变体）均会导致攻击成功率和有害性分数的显著下降，验证了两个模块的协同必要性。

![[assets/figures/papers/paper_list_l2220_https_arxiv_org_abs_2603_21208/figures/002_Figure_2.jpg]]
*Figure 2: Overall pipeline of our JANUS. Stage 1 builds two semantically anchored base distributions from the target prompt pt and its clean counterpart*

### 2.1 问题形式化：从离散搜索到分布优化

JANUS 的核心范式转换在于将越狱攻击从“寻找单个最优对抗提示”重新定义为“学习一个参数化的提示分布”。给定一个文本到图像（T2I）系统 $M: \mathcal{P} \to \mathcal{V}$ 及其安全过滤器 $C(\mathbf{p}, M(\mathbf{p})) \to \{0, 1\}$，传统方法致力于搜索满足绕过、语义相似和有害性三个条件的单一 $\mathbf{p}_{\mathrm{adv}}$。JANUS 则直接学习一个分布 $p_{\theta}(\mathbf{p})$，使其尽可能逼近理想的越狱分布 $q^{*}$。

这一目标通过最小化 KL 散度实现：

$$
\theta^{*} = \arg\min_{\theta} D_{KL}(p_{\theta} || q^{*}) \tag{1}
$$

将理想分布 $q^{*}$ 建模为玻尔兹曼分布后，上述 KL 散度最小化等价于最小化期望自由能：

$$
\arg\min_{\theta} D_{KL}(p_{\theta}||q^{*}) = \mathbb{E}_{\mathbf{p}\sim p_{\theta}}[E(\mathbf{p}) + \log p_{\theta}(\mathbf{p})] \tag{2}
$$

其中 $E(\mathbf{p})$ 是衡量提示 $\mathbf{p}$ 越狱效果的端到端能量函数。这一形式化将问题转化为：在保持分布熵（由 $\log p_{\theta}(\mathbf{p})$ 项控制）的同时，最小化期望能量。

### 2.2 第一阶段：语义锚定分布建模

直接在高维离散提示空间上参数化 $p_{\theta}$ 面临维度灾难。JANUS 的核心洞察是：**越狱提示的语义结构与有害性可解耦**。基于此，第一阶段将离散提示松弛为两个语义锚定高斯分布的凸组合。

**双锚点构建。** 给定目标有害提示 $\mathbf{p}_t$ 及其清洁版本 $\mathbf{p}_c$（通过内容过滤获得），分别构建两个语义锚定分布：
- **有害锚点** $N_t$：以 $\mathbf{p}_t$ 的语义嵌入为中心的高斯分布
- **清洁锚点** $N_c$：以 $\mathbf{p}_c$ 的语义嵌入为中心的高斯分布

**混合策略。** 引入标量混合系数 $\alpha \in [0, 1]$，将提示分布参数化为两个基础分布的凸组合：

$$
p_{\alpha} = \alpha N_t + (1 - \alpha) N_c \tag{7}
$$

这一设计的关键优势在于**结构化的语义下界保证**。对于任意语义相似度度量 $\mathcal{L}$ 和目标嵌入 $\mathbf{e}_t$，混合分布生成的提示与目标提示的期望语义相似度满足：

$$
\mathbb{E}_{\mathbf{p}\sim p_{\alpha}}[\mathcal{L}(e(\mathbf{p}), \mathbf{e}_t)] \geq \min\left(\mathbb{E}_{\mathbf{p}\sim N_t}[\mathcal{L}(e(\mathbf{p}), \mathbf{e}_t)], \mathbb{E}_{\mathbf{p}\sim N_c}[\mathcal{L}(e(\mathbf{p}), \mathbf{e}_t)]\right) \tag{8}
$$

该下界由两个基础分布中较弱者保证，从结构上维持了语义一致性，无需手设计代理损失。这类似于波的干涉原理：共享的核心语义形成“建设性干涉”而保持稳定，仅通过调节 $\alpha$ 即可在低维空间中高效探索绕过与有害性的均衡。

### 2.3 第二阶段：基于策略梯度的黑盒优化

第二阶段将混合系数 $\alpha$ 作为策略参数，使用 REINFORCE 风格的策略梯度最大化端到端黑盒奖励。

**端到端能量函数。** 奖励信号直接来自 T2I 系统及其安全过滤器的黑盒反馈：

$$
E(\mathbf{p}) = -C(\mathbf{p}, M(\mathbf{p})) \cdot S(M(\mathbf{p})) \tag{9}
$$

其中 $C(\cdot) \in \{0,1\}$ 指示是否绕过安全过滤器（1 表示绕过），$S(\cdot)$ 为输出图像的 NSFW 有害性评分。越成功的越狱提示能量越低。

**强化学习目标。** 将自由能最小化（式 2）转化为最大化期望奖励：

$$
J(\alpha) = \mathbb{E}_{\mathbf{p}\sim p_{\alpha}}[R(\mathbf{p})], \quad R(\mathbf{p}) = -(E(\mathbf{p}) + \log p_{\alpha}(\mathbf{p})) \tag{10}
$$

**对数策略梯度。** 关键优势在于 $p_{\alpha}$ 的混合结构使得梯度计算极为简洁，仅需两个基础分布的概率密度：

$$
\nabla_{\alpha} \log p_{\alpha}(\mathbf{p}) = \frac{N_t(\mathbf{p}) - N_c(\mathbf{p})}{\alpha N_t(\mathbf{p}) + (1 - \alpha) N_c(\mathbf{p})} \tag{11}
$$

这一梯度形式无需白盒模型参数，无需大规模语言模型作为生成器，仅通过轻量级策略梯度即可在单标量参数 $\alpha$ 上完成优化。整个流水线如 Figure 2 所示：第一阶段构建语义锚定混合分布，第二阶段通过黑盒反馈更新混合策略。

## 实验与关键发现

### 主实验结果

JANUS在开源与商业T2I模型上均展现出显著且一致的越狱性能优势。Table 1报告了在Stable Diffusion 3.5 Large Turbo (SD3.5LT) 和 DALL·E3上的全面对比。在SD3.5LT上，JANUS的ASR-8达到**43.15%**，较最强基线QFA的25.30%提升了**17.85个百分点**；同时，CLIP Score（0.37 vs. 0.31）和NSFW Score（0.33 vs. 0.28）也同步提升，表明JANUS在增强绕过能力的同时并未牺牲语义保持或有害内容诱导质量。在商业闭源模型DALL·E3上，所有基线方法的ASR-8均接近0%，而JANUS取得了**3.39%**的ASR-8，首次证明了分布级优化范式对严格商业安全过滤器的渗透能力。

**Table 1** 定量对比
*（此处插入 Table 1）*

在更广泛的模型覆盖测试中（Table 4），JANUS在SDXL上取得**58.20%**的ASR-8，领先最强基线SneakyPrompt的36.40%达**21.80个百分点**；在Midjourney上，JANUS的ASR-8为**6.20%**，超过最佳基线PGJ的3.28%。值得注意的是，Midjourney的ASR-1指标因模型强制每次查询生成至少4张图像而不可计算，但其ASR-8的提升验证了JANUS在极端黑盒商业系统上的有效性。

![[assets/figures/papers/paper_list_l2220_https_arxiv_org_abs_2603_21208/figures/008_Table_4.jpg]]
*Table 4: Quantitative comparison of existing jailbreak attacks on SDXL and Midjourney. Higher values indicate better performance (↑), and the best results in each column are highlighted in bold. Note that for Midjourney, IASR-1 and ASR-1 are omitted (-) as the model generates a minimum batch of 4 images per query*

**Table 4** 补充定量结果
*（此处插入 Table 4）*

### 消融实验

为验证JANUS各组件的独立贡献，Table 2报告了在SD3.5LT和DALL·E3上的组件消融结果。

**Table 2** 消融实验
*（此处插入 Table 2）*

**双分布干扰（Unimodal消融）**：移除双锚点混合机制，仅使用单一分布（Unimodal变体）搜索提示，在SD3.5LT上ASR-8从43.15%大幅下降，NSFW分数也同步降低。这验证了有害锚点与清洁锚点的线性叠加空间（Eq.(7)）提供了丰富的、语义锚定的搜索域，是高效探索绕过与有害性均衡的关键。

**动态奖励机制（Fix NSFW消融）**：将端到端能量函数中的动态NSFW评分替换为固定值（Fix NSFW变体），导致最终NSFW分数显著降低。这表明在优化过程中持续评估输出有害性并反馈至策略更新（Eq.(9)-(10)），对于引导搜索朝向真正有害的绕过方向至关重要，单纯的过滤逃避目标会产生奖励破解（reward hacking）。

**混合策略学习（固定α vs. RL动态α）**：Figure 4展示了混合系数α对越狱性能的影响。固定α至任意静态值均会在过滤逃避与有害性之间产生次优权衡——高α值倾向于绕过但有害性不足，低α值则反之。JANUS采用REINFORCE策略梯度在线学习动态α策略（“Fully Trained”），在两个指标上均取得全面更优表现，证明了轻量级策略优化在黑盒奖励信号下自主发现最优混合比例的能力。

**Figure 4** 混合策略影响
*（此处插入 Figure 4）*

### 计算效率分析

Table 3对比了各方法的平均每次成功越狱运行时间。JANUS相较于优化类基线实现了显著加速：比MMA快约**18倍**，比MMP快约**12倍**。与生成器类方法（PGJ、SneakyPrompt）相比，JANUS在保持竞争性运行时间的同时，完全无需加载数十亿参数的大语言模型，显存占用极低。这一效率优势源自JANUS将搜索空间压缩至标量α的低维策略优化，避免了逐token离散搜索或大容量生成器的推理开销。

**Table 3** 计算效率
*（此处插入 Table 3）*

### 失败模式与局限性

尽管JANUS在开源模型上表现强劲，其在商业模型上的绝对ASR仍较低（DALL·E3: 3.39%，Midjourney: 6.20%），表明商业安全过滤器对分布级攻击具备一定抵御能力。离散化误差与探索噪声σ正相关——过大的σ会增大优化目标与真实输出之间的偏差，实际部署需手动调参以平衡探索与保真度。此外，当前评估仅覆盖NSFW类有害概念，JANUS对暴力、仇恨言论等更广泛隐性有害概念的泛化能力尚未验证，需进一步实验确认。

### 关键图表结论

- **Table 1**：JANUS在SD3.5LT上ASR-8达43.15%，CLIP/NSFW分数同步最优，全面超越所有基线。
- **Table 2**：双分布建模和动态奖励是JANUS性能的两大支柱，任一组件的移除均导致显著性能退化。
- **Figure 4**：固定α产生次优权衡，RL学习的动态α策略是解锁全面越狱性能的关键机制。
- **Table 3**：JANUS以18倍/12倍加速超越优化类基线，且无需大语言模型，实现轻量高效的黑盒攻击。
- **Table 4**：JANUS在SDXL和Midjourney上持续领先，跨模型泛化能力得到验证。

![[assets/figures/papers/paper_list_l2220_https_arxiv_org_abs_2603_21208/figures/003_Table_1.jpg]]
*Table 1: Quantitative comparison of existing jailbreak attacks on SD3.5LT and DALL·E3. Higher values indicate better performance (↑), and the best results in each column are highlighted in bold*

![[assets/figures/papers/paper_list_l2220_https_arxiv_org_abs_2603_21208/figures/006_Table_2.jpg]]
*Table 2: Component-wise ablation of JANUS on SD3.5LT and DALL·E3. We compare the full framework (“Full Process”) against a Unimodal variant (single distribution) and a fixed-NSFW-reward variant. We report TASR, IASR, ASR and NSFW Score for N=8*

![[assets/figures/papers/paper_list_l2220_https_arxiv_org_abs_2603_21208/figures/007_Table_3.jpg]]
*Table 3: Computational efficiency comparison. We report the average runtime (in seconds) per successful jailbreak. JANUS achieves a significant speedup compared to optimization-based baselines (MMA, MMP) while maintaining a competitive runtime against generator-based methods (PGJ, SneakyPrompt) without requiring memory-intensive Large Language Models*

![[assets/figures/papers/paper_list_l2220_https_arxiv_org_abs_2603_21208/figures/001_Figure_1.jpg]]
*Figure 1: Qualitative results of JANUS on Stable Diffusion 3.5 Large Turbo (left) and DALL·E3 (right). JANUS rewrites unsafe target prompts into distributionally optimized, ostensibly benign queries that bypass both text- and image-level safety filters, yet still induce model outputs aligned with the original prohibited intent*

## 定位与知识库关联

### 1. 越狱攻击的范式演进

文本到图像（T2I）越狱攻击的研究可沿两条核心轴线进行梳理：**搜索空间的粒度**（离散提示 vs. 连续嵌入 vs. 分布）和**优化信号的来源**（白盒梯度 vs. 代理损失 vs. 黑盒端到端奖励）。JANUS 的定位正是在这两条轴线上同时实现了范式跃迁。

**离散提示优化**是早期攻击的主流范式。**MMA** 将 GCG 风格的贪婪坐标梯度搜索从大语言模型迁移至 T2I 场景，在离散 token 空间中逐位置替换以最大化绕过概率。**QFA** 则采用查询反馈机制，通过多次黑盒探测来筛选有效提示。这类方法的根本瓶颈在于：搜索空间是组合爆炸的离散格点，每一步优化都依赖高成本的模型查询，且缺乏对语义连续性的显式建模，导致优化效率低下且容易陷入局部最优。

**连续嵌入优化**试图通过松弛离散约束来提升搜索效率。**MMP** 在连续的文本嵌入空间中执行软优化，利用嵌入空间的几何结构进行梯度引导的搜索。这虽然加速了优化过程，但引入了一个新的困境：嵌入空间的扰动缺乏语义可解释性，必须依赖额外的语义相似度代理损失来约束搜索方向，而代理损失与真实的“绕过+有害性”目标之间存在天然的目标错位（objective misalignment）。

**生成器级优化**代表了另一种思路。**SneakyPrompt** 和 **PGJ** 通过强化学习训练一个专用的大容量语言模型作为提示生成器，使其学会将有害目标提示改写为可绕过的表面良性查询。这类方法的核心代价在于：需要维护和微调数十亿参数的大语言模型，计算开销巨大（训练和推理均需大量 GPU 内存），且训练得到的生成器往往过度适应特定 T2I 模型的安全过滤器分布，跨模型泛化能力有限。

JANUS 的范式创新在于将上述两条轴线同时打破。在搜索空间上，它从“逐提示优化”跃迁到“提示分布优化”——不再搜索单个最优提示，而是学习一个参数化的提示分布 $p_\alpha$。在优化信号上，它完全摒弃了白盒梯度和代理损失，直接使用 T2I 系统及其安全过滤器提供的黑盒端到端联合奖励（绕过状态 $\times$ NSFW 分数）。这一双重跃迁使得 JANUS 既避免了离散搜索的低效，又摆脱了代理损失的目标错位，同时无需任何大容量生成器。

### 2. 核心机制对比

从技术机制的角度，JANUS 与现有方法的关键差异体现在三个可替换模块上：

| 机制维度 | 离散优化（MMA, QFA） | 连续优化（MMP） | 生成器优化（SneakyPrompt, PGJ） | **JANUS** |
|---------|---------------------|----------------|-------------------------------|-----------|
| **优化范式** | 逐提示离散梯度/查询搜索 | 连续嵌入空间搜索 | 大容量生成器 RL 训练 | 低维语义锚定分布的凸组合 + 轻量策略梯度 |
| **语义保持** | 无显式机制 | 手设计代理损失（语义相似度约束） | 生成器隐式学习 | 双锚点分布线性叠加的结构化语义下界保证（Eq.8） |
| **优化信号** | 白盒梯度或代理损失 | 白盒梯度或代理损失 | RL 奖励（绕过信号） | 黑盒端到端联合奖励 $E(p) = -C(p, M(p)) \cdot S(M(p))$ |

**语义保持机制**的差异尤为关键。MMP 依赖显式的语义相似度损失项来约束优化方向，但这本质上是一个代理目标——语义相似度高并不等价于越狱效果好。JANUS 通过双锚点分布的凸组合 $p_\alpha = \alpha N_t + (1-\alpha) N_c$ 结构性地解决了这一问题：混合分布生成的提示与目标提示的语义相似度下界由两个基础分布中较弱者保证（Eq.8），无需任何额外的代理损失项。这意味着语义保持被“免费”编码在分布结构之中，优化器可以专注于最大化绕过与有害性的联合目标，而不会因代理损失而偏离真正有效的搜索方向。

**优化信号的差异**决定了攻击的实用边界。MMA 需要访问模型的内部表示（白盒假设），这在实际商业 T2I 系统（如 DALL·E3、Midjourney）上不可行。MMP 虽然可以在嵌入空间操作，但仍需梯度信号来引导搜索。SneakyPrompt 和 PGJ 虽然工作在黑盒设定下，但它们的 RL 训练过程本身需要大量交互样本，且训练得到的生成器是一个静态的映射函数，无法针对每个目标提示动态调整策略。JANUS 的策略梯度优化（REINFORCE 风格，Eq.10-13）仅需两个基础分布的概率密度即可计算梯度（Eq.11），无需白盒模型，且对每个目标提示独立学习最优混合系数 $\alpha$，实现了真正的按提示自适应优化。

### 3. 适用边界与局限

**开源模型的优势区间**。JANUS 在开源 T2I 模型上展现了显著优势：在 SD3.5LT 上 ASR-8 达到 43.15%（对比最强基线 QFA 的 25.30%），在 SDXL 上达到 58.20%（对比 SneakyPrompt 的 36.40%）。这验证了分布优化范式在安全过滤器相对可穿透的场景下的高效性。

**商业模型的抵抗能力**。在 DALL·E3 和 Midjourney 上，JANUS 的 ASR-8 分别仅为 3.39% 和 6.20%，虽然均超越了所有基线方法（包括此前最优的 SneakyPrompt 在 DALL·E3 上的 0.00%），但绝对成功率仍然较低。这表明商业闭源模型部署的多层次安全过滤器（文本级 + 图像级联合检测）对分布式攻击仍具有较强的抵御能力。值得注意的是，JANUS 在 Midjourney 上的提升（+2.92% 对比 PGJ）是在该平台最低批量生成 4 张图像的限制下取得的，这一约束本身增加了攻击难度。

**离散化误差与探索噪声的权衡**。JANUS 将连续分布采样结果离散化为具体提示 token 时，离散化误差与探索噪声 $\sigma$ 成正比。过大的 $\sigma$ 会导致优化目标与真实输出之间的偏差增加；过小的 $\sigma$ 则限制了搜索空间的覆盖范围。论文证明了 $\sigma$ 在理论上是可控的，但实际应用中需要针对不同 T2I 模型手动调参以平衡探索与保真度，这构成了方法实用性的一个工程瓶颈。

**概念覆盖的局限性**。现有实验仅在 NSFW（色情/裸露）这一单一有害概念类别上进行评估，使用的 200 个人工构造提示均来自 Civitai-8mprompts 数据集。JANUS 对更广泛的隐性有害概念（如暴力、仇恨言论、自残内容）的泛化能力尚未得到验证。不同有害概念在语义空间中的分布结构可能存在差异，双锚点建模的有效性需要进一步检验。

### 4. 开放问题与未来方向

**自适应探索噪声调节**。当前 $\sigma$ 依赖人工设定，能否设计一种自适应机制，在攻击过程中根据绕过成功率和 NSFW 分数的反馈动态调节探索噪声？例如，当检测到优化陷入局部最优时自动增大 $\sigma$ 以扩大搜索半径，当语义偏离过大时自动收缩以保持目标一致性。

**多模态扩展与联合防御对抗**。该分布优化框架能否从 T2I 扩展到文本到视频（T2V）等更复杂的生成模型？视频生成涉及时序一致性约束和更复杂的安全过滤器（帧级检测 + 时序异常检测），双锚点分布假设是否仍然成立？此外，防御方可能发展出分布感知式的检测机制——通过监控提示的统计特征来识别分布优化攻击，JANUS 面对此类动态防御的鲁棒性是一个重要的对抗性研究课题。

**多锚点复合分布**。当前双锚点设计（有害 + 清洁）的语义稳定性下界在极端语义分离情况下（$\mu_t$ 与 $\mu_c$ 距离过大）是否仍然有效？能否扩展到三个或更多锚点的复合成分布（例如增加一个“中性风格”锚点）以提升攻击的语义多样性和绕过路径的丰富性？这需要重新推导语义稳定性下界的理论保证。

**红队测试工具的伦理转化**。JANUS 的核心技术——分布级黑盒优化——具有天然的“红队测试”工具属性：它能在不访问模型内部参数的情况下自动化地探测安全漏洞。如何界定这一技术的伦理使用边界？是否可以通过限制优化目标（例如将 NSFW 分数替换为通用的安全违规指标）和输出控制（仅报告漏洞而不生成实际有害图像）来将其转化为合法的安全审计工具？这需要学术界、工业界和政策制定者的共同参与。

## 原文 PDF

![[paperPDFs/CVPR_2026/JANUS_A_Lightweight_Framework_for_Jailbreaking_Text_to_Image_Models_via_Distribution_Optimization.pdf]]
