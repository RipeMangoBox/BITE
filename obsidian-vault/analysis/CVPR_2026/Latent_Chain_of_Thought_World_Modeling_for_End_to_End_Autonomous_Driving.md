---
title: Latent Chain-of-Thought World Modeling for End-to-End Autonomous Driving
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Latent_Chain_of_Thought_World_Modeling_for_End_to_End_Autonomous_Driving.pdf
project_link: null
code_link: null
huggingface_link: "https://huggingface.co/datasets/nvidia/PhysicalAI-Autonomous-Vehicles"
aliases:
- LLCD
- LCTWMEEAD
tags:
- CVPR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 将推理表示从自然语言切换为与动作词汇对齐的潜在令牌，并交错进行动作提案与潜在世界模型预测，使推理过程与最终决策高度一致且计算高效。
primary_logic: 在潜在空间中构建动作对齐的链式思考：通过交替生成动作提案（与输出动作共享词表）和世界模型潜在状态预测，模拟反事实未来，从而在紧凑的推理序列中实现高质量轨迹规划。
claims:
- 与文本CoT相比，LCDrive在ADE和安全性指标上均更优，且实现1.8×推理加速。
- 潜在CoT*结合RL后ADE进一步从1.268降至1.197。
- 冷启动阶段使用冻结的非推理VLA生成动作提案作为监督，有效引导模型学习潜在推理格式。
- PhysicalAI-AV 上 ADE (m) = 1.626
---

# Latent Chain-of-Thought World Modeling for End-to-End Autonomous Driving

> [!tip] 核心洞察
> 在潜在空间中构建动作对齐的链式思考：通过交替生成动作提案（与输出动作共享词表）和世界模型潜在状态预测，模拟反事实未来，从而在紧凑的推理序列中实现高质量轨迹规划。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向端到端自动驾驶的潜在链式思考世界建模 |
| 英文题名 | Latent Chain-of-Thought World Modeling for End-to-End Autonomous Driving |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Tan_Latent_Chain-of-Thought_World_Modeling_for_End-to-End_Autonomous_Driving_CVPR_2026_paper.html) · [HuggingFace](https://huggingface.co/datasets/nvidia/PhysicalAI-Autonomous-Vehicles) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | LCDrive (Latent-CoT-Drive) |
| Dataset | PhysicalAI-AV |

> [!tip] 效果简介
> - PhysicalAI-AV 上，ADE (m) 1.626 vs 1.762 (Non-reasoning) (-0.136)；OffRoad2.5 1.219 vs 1.753 (Non-reasoning) (-0.534)；Coll5 0.836 vs 2.207 (Non-reasoning) (-1.371)。

## 概要

端到端（E2E）自动驾驶视觉‑语言‑动作（VLA）模型近期开始引入链式思考（Chain‑of‑Thought, CoT）推理以提升规划质量，但主流方案依赖**文本链式思考（Text CoT）**，面临三个结构性瓶颈：（1）自然语言难以精确表达时空几何与多智能体交互关系；（2）自回归生成长文本序列带来显著推理延迟；（3）语言推理与最终动作之间可能出现严重不一致——例如文字描述“左转”而输出轨迹实际右转。

针对上述问题，本文提出 **LCDrive（Latent‑CoT‑Drive）**，核心思想是将推理表示从自然语言**切换为与动作词汇对齐的潜在令牌**，并在潜在空间中构建**动作对齐的链式思考**：交替生成动作提案块与潜在世界模型（Latent World Model, LWM）状态预测，从而模拟反事实未来，在紧凑的推理序列中实现高质量轨迹规划。

在 **PhysicalAI‑AV** 数据集上的实验表明：与无推理基线相比，LCDrive 将平均位移误差（ADE）从 1.762 m 降至 1.626 m，碰撞率（Coll5）从 2.207 大幅降至 0.836；与 Text CoT 基线相比，LCDrive 在 ADE 和安全性指标上均更优，且实现 **1.8× 推理加速**。进一步结合强化学习后训练（GRPO），潜在 CoT* 变体的 ADE 从 1.268 进一步降至 1.197，验证了潜在推理表示与 RL 后训练的协同增效。

在方法谱系上，LCDrive 属于 **VLA 推理表示学习** 范畴，与以下工作形成对比：
- **Text CoT VLA**（Wang et al., arXiv 2025）：使用自然语言作为推理介质，存在上述表示‑动作脱节与延迟问题；
- **Non‑reasoning VLA**：直接预测轨迹，缺少显式推理环节；
- **MPGD**（He et al., CVPR 2023）等基于世界模型的规划方法：通常依赖显式未来预测与规划器，而 LCDrive 将世界模型压缩为潜在令牌并融入自回归推理序列，实现端到端可微。

端到端（E2E）自动驾驶的核心目标是将传感器输入直接映射为可执行的车辆轨迹。近年来，视觉-语言-动作（VLA）模型在驾驶场景中展现出强大的泛化潜力，其优势在于能够利用大规模预训练知识进行场景理解与决策。然而，当面对复杂交通场景时，直接预测轨迹往往难以捕捉多智能体交互的深层因果逻辑，因此研究者开始探索将**链式思考（Chain-of-Thought, CoT）**引入驾驶VLA模型，以期通过显式推理提升轨迹质量与安全性。

当前的推理增强方案普遍采用**文本链式思考（Text CoT）**，即让模型先生成自然语言描述（如“前方车辆正在减速，我将向左变道”），再基于该文本预测动作。尽管这一范式在语言和视觉问答任务中取得了显著成功，但在自动驾驶这一时空敏感的具身任务中暴露出三个根本性瓶颈：

1. **表征失配**：自然语言天然适合描述抽象语义，却难以精确刻画车辆运动学约束、相对位姿关系和多智能体交互的时空几何。文本中的“左转”无法传递转向曲率、避让时机等连续控制所需的细粒度信息。
2. **推理延迟**：自回归生成冗长的文本序列引入了显著的计算开销，对于实时性要求极高的车载系统而言难以接受。
3. **语言-动作脱节**：文本推理与最终动作预测之间缺乏强对齐约束。模型可能在文字中描述“左转”，但实际输出的轨迹却指向右侧——这种“说一套做一套”的现象严重侵蚀了推理的可信度与决策的可靠性。

上述问题的本质在于：**自然语言并非自动驾驶推理的最优表示媒介**。驾驶决策本质上是在高维向量空间中对自车与周围智能体的未来状态进行反事实推演，而这一过程更适合在连续或离散的潜在空间中完成。与此同时，世界模型（World Model）在基于模型的强化学习中已被证明能够有效模拟环境动态，但将其作为VLA推理的内部“想象引擎”仍属空白。

基于此，本文提出核心动机：**将链式思考的表示从自然语言切换为与动作词汇对齐的潜在令牌，并引入可学习的潜在世界模型（Latent World Model, LWM）作为推理的“模拟器”**。这一思路旨在同时解决表征效率、推理延迟和动作对齐三大问题——模型在紧凑的潜在空间中交替生成动作提案与反事实世界状态预测，以极低的推理预算完成高质量的时空推演，最终输出安全且平滑的驾驶轨迹。

## 核心方法与创新机理

### 从文本链式思考到潜在链式思考

端到端自动驾驶中的视觉-语言-动作（VLA）模型通常将推理表示为自然语言链式思考（Text CoT）。然而，文本CoT在驾驶场景中存在三个根本性瓶颈：

1. **表示不对齐**：自然语言难以精确描述时空几何关系与多智能体交互动态，导致推理内容与驾驶动作之间存在语义鸿沟。
2. **推理延迟高**：自回归生成长文本推理序列引入显著的计算开销，难以满足实时性要求。
3. **动作脱节**：语言推理与最终输出的动作轨迹可能严重不一致——例如推理文字描述“左转”，但生成的轨迹却指向右转。

LCDrive 的核心创新在于**将推理的表示空间从自然语言切换为与动作词汇对齐的潜在令牌**，从而在紧凑的推理序列中实现高质量轨迹规划。具体而言，该方法将推理过程 `REASON` 实例化为一个交替交织的潜在令牌序列，由两类关键令牌组成：

- **动作提案令牌**（action-proposal tokens）：与最终轨迹预测共享同一离散动作词表（1024码本），确保推理过程与输出动作在词汇层面严格对齐。
- **潜在世界模型令牌**（latent world-model tokens）：编码以自车为中心的潜在世界状态，用于预测反事实未来场景中智能体的运动演变。

### 推理机制：交替生成与反事实模拟

LCDrive 的推理过程通过多个并行的推理分支实现。每个推理分支 $R^{(i)}$ 的结构为动作提案块与潜在世界状态预测令牌的交替序列：

$$R^{(i)} = \big[ A_0^{(i)}, \mathrm{LWM}_1^{(i)}, A_1^{(i)}, \mathrm{LWM}_2^{(i)}, \dots, A_{K-1}^{(i)}, \mathrm{LWM}_K^{(i)} \big]$$

其中每个动作提案块 $A_t^{(i)}$ 包含 1.0 秒（10 步）的动作令牌，潜在世界模型预测令牌 $\mathrm{LWM}_t^{(i)}$ 则编码在该动作假设下未来场景的演变。这一交替机制本质上实现了**反事实推理**：模型先提出一个候选动作序列，再预测该动作将引发的场景变化，随后基于预测结果调整下一阶段的动作提案。通过 $B$ 条并行的推理分支，模型可以在推理时探索多种可能的未来轨迹，最终选择最优方案。

与文本 CoT 相比，潜在 CoT 的推理令牌序列长度大幅压缩，且所有令牌均处于与驾驶动作直接相关的向量空间中，从根本上消除了语言歧义和动作脱节问题。

### 训练策略创新：冷启动与强化学习的协同

LCDrive 的另一关键创新在于其三阶段训练策略，专门针对潜在推理模型的特性设计：

1. **阶段 0（无推理预训练）**：训练一个不包含推理模块的基础 VLA 模型，直接根据传感器输入预测轨迹。
2. **阶段 1（CoT 冷启动）**：利用冻结的阶段 0 模型生成动作提案作为监督信号，引导 LCDrive 学习潜在推理格式。该阶段联合优化令牌交叉熵损失和潜在世界模型预测的 MSE 损失：$\mathcal{L}_{\mathrm{stage-1}} = \mathcal{L}_{\mathrm{token}} + \lambda \mathcal{L}_{\mathrm{lwm}}$，其中 $\lambda = 0.1$ 平衡两类损失。
3. **阶段 2（强化学习后训练）**：采用 GRPO（Group Relative Policy Optimization）进行强化学习微调，目标函数为 $\mathcal{L}_{\mathrm{GRPO}} = -\frac{1}{G} \sum_{j=1}^G A^{(j)} \sum_t \log \pi_{\theta}(x_t^{(j)} \mid \mathrm{context}_t^{(j)})$，通过组内相对优势加权最大化生成令牌的对数概率。实验发现去除 KL 正则化项后 GRPO 效果最佳。

冷启动阶段解决了潜在推理格式缺乏自然监督的难题，而 RL 后训练则进一步激活模型的推理能力——实验表明，潜在 CoT* 结合 RL 后 ADE 从 1.268 降至 1.197，验证了该训练策略的有效性。

### 与基线方法的关键差异

| 设计维度 | 无推理 VLA | 文本 CoT (AR1) | **LCDrive (本文)** |
|---------|-----------|---------------|-------------------|
| 推理表示 | 无 | 自然语言令牌 | 与动作词汇对齐的潜在令牌 + 世界模型令牌 |
| 推理过程 | 直接预测 | 文本自回归生成 | 交替动作提案与反事实世界状态预测 |
| 训练策略 | 仅监督微调 | 仅监督微调 | 预训练 → CoT 冷启动 → GRPO 强化学习 |
| 推理延迟 | 低 | 高（长文本生成） | 低（紧凑潜在序列，1.8× 加速） |
| 动作对齐 | — | 弱（语义鸿沟） | 强（共享动作词表） |

这些创新共同构成了 LCDrive 的核心贡献：在潜在空间中构建动作对齐的链式思考，通过反事实世界模拟实现高效且一致的运动规划。

LCDrive 将端到端驾驶形式化为一个自回归序列建模问题，其核心创新在于用**与动作词汇对齐的潜在令牌序列**替代传统的自然语言链式思考。整体序列结构为：

$$[ o_{\mathrm{image}}, o_{\mathrm{ego}}, \mathrm{REASON}, \tau ]$$

其中 $o_{\mathrm{image}}$ 为多视角图像令牌，$o_{\mathrm{ego}}$ 为自车历史运动学令牌，$\mathrm{REASON}$ 为本文提出的潜在推理令牌，$\tau$ 为未来轨迹令牌（64 个位姿点，覆盖 6.4 秒 @ 10 Hz）。

### 输入编码层

系统接收两类传感器输入，分别通过专用 tokenizer 转换为统一令牌空间：

- **Vision Tokenizer**：基于 ViT 的编码器，对每一帧多视角图像独立编码为视觉令牌序列。
- **Egomotion Tokenizer**：将自车历史运动学状态（位置、速度、航向等）嵌入为紧凑的令牌集合。

### 潜在推理核心

推理模块是 LCDrive 区别于传统 VLA 的关键。$\mathrm{REASON}$ 被实例化为 $B$ 个并行的**推理分支**，每个分支 $R^{(i)}$ 由交替排列的动作提案块和潜在世界模型（LWM）预测令牌构成：

$$R^{(i)} = \big[ A_0^{(i)}, \mathrm{LWM}_1^{(i)}, A_1^{(i)}, \mathrm{LWM}_2^{(i)}, \dots, A_{K-1}^{(i)}, \mathrm{LWM}_K^{(i)} \big]$$

其中每个动作提案块 $A_t^{(i)}$ 包含 10 个步进式动作令牌（对应 1.0 秒），使用与最终轨迹预测 $\tau$ 相同的 1024 码本词汇表。该词汇表通过对训练数据中的 $\Delta$-pose 进行 k-means 聚类构建。

LWM 令牌由两个子模块协同产生：

- **LWM Encoder**：轻量 Transformer 模块，将感知到的周围智能体边界框编码为以自车为中心的潜在世界状态 $\mathrm{LWM}_t$。
- **LWM Predictor**：一个轻量 MLP $f_\phi$，根据当前上下文预测未来潜在世界状态令牌，使模型能够在推理过程中模拟**反事实未来**。

### 输出层

- **Action Proposal Head** 与轨迹预测头共享码表，在推理阶段生成动作提案块；最终轨迹 $\tau$ 由模型自回归解码输出 64 个位姿点 $(x^i, y^i, \theta_{\mathrm{yaw}}^i)$。

### 训练三阶段

LCDrive 采用渐进式训练策略（Figure 3）：

1. **Stage 0 — 预训练**：训练一个无推理的基线 VLA，仅建模 $[o_{\mathrm{image}}, o_{\mathrm{ego}}, \tau]$。
2. **Stage 1 — CoT 冷启动**：冻结 Stage 0 模型，利用其生成的动作提案作为监督信号，训练 LCDrive 学习潜在推理格式。损失函数为 $\mathcal{L}_{\mathrm{stage-1}} = \mathcal{L}_{\mathrm{token}} + \lambda \mathcal{L}_{\mathrm{lwm}}$，其中 $\lambda=0.1$ 平衡令牌交叉熵损失与 LWM 预测 MSE 损失。
3. **Stage 2 — 强化学习后训练**：采用 GRPO（Group Relative Policy Optimization）激活推理能力，目标函数为优势加权对数概率最大化。实验发现去除 KL 正则化项后 GRPO 效果最佳。

### 设计动机

该框架针对文本 CoT 在自动驾驶中的三个根本瓶颈设计：自然语言不适合表示时空几何与多智能体交互；自回归生成长文本引入高延迟；语言推理与最终动作可能严重脱节。通过将推理表示切换为与动作词汇对齐的潜在令牌，并交错进行动作提案与世界状态预测，LCDrive 在紧凑的推理序列中实现了推理-决策的高度一致性。

![[assets/figures/papers/paper_list_l2321_https_openaccess_thecvf_com_content_CVPR2026_html_Tan_Latent_Chain_of_Th/figures/002_Figure_2.jpg]]
*Figure 2: Architecture. Overview of our proposed latent reasoning framework*

### 3.1 问题形式化：端到端驾驶的自回归序列建模

LCDrive将端到端驾驶形式化为对自回归令牌序列的分布建模。序列拼接了输入信息、推理轨迹（可选）以及自车未来轨迹 $\tau$：

$$ \bigl[ o_{\mathrm{image}}, o_{\mathrm{ego}}, \mathrm{REASON}, \tau \bigr] $$

其中 $o_{\mathrm{image}}$ 为多视角图像帧经视觉分词器编码后的令牌，$o_{\mathrm{ego}}$ 为自车历史运动学状态经自运动分词器编码后的令牌。$\mathrm{REASON}$ 为可选的推理令牌序列，$\tau$ 为未来轨迹令牌。

未来轨迹 $\tau$ 参数化为64个位姿点（对应6.4秒、10Hz的未来时域）：

$$ \tau = \{ ( x^i, y^i, \theta_{\mathrm{yaw}}^i ) \}_{i=1}^{64} $$

轨迹通过一个1024码本的离散词表进行量化——对训练集中的 $\Delta$-位姿执行k-means聚类得到。

### 3.2 潜在链式思考：动作提案与潜在世界模型的交错推理

LCDrive的核心创新在于将 $\mathrm{REASON}$ 实例化为一个短小的交错潜在令牌序列，由两类令牌交替组成：**动作提案令牌**（action-proposal tokens）与**反事实潜在世界模型令牌**（counterfactual latent world-model tokens）。这一设计直接回应了文本链式思考的三大瓶颈：自然语言不适合表示时空几何与多智能体交互、自回归生成长文本引入高延迟、语言推理与最终动作可能严重脱节。

每个推理分支 $i$ 的令牌序列结构为：

$$ R^{(i)} = \big[ A_0^{(i)}, \mathrm{LWM}_1^{(i)}, A_1^{(i)}, \dots, A_{K-1}^{(i)}, \mathrm{LWM}_K^{(i)} \big] $$

其中 $K$ 为推理步数（默认 $K=5$），$B$ 为并行推理分支数（默认 $B=2$）。

**动作提案块 $A_t^{(i)}$** 定义为1.0秒内10个步进动作令牌的序列：

$$ A_t^{(i)} := \big( a_{10(t-1)+1}, \dots, a_{10t} \big) $$

关键设计在于：动作提案块与最终轨迹预测 $\tau$ **共享同一离散动作词表**（1024码本），这确保了推理过程中的动作提案与最终输出的动作在词汇空间上严格对齐，从根本上消除了文本CoT中“语言推理与动作脱节”的问题。

**潜在世界模型状态 $\mathrm{LWM}_t^{(i)}$** 由LWM编码器从感知到的智能体边界框编码得到，LWM预测器 $f_\phi$（一个轻量MLP）则根据当前上下文预测未来的潜在世界状态。这一机制使模型能够在推理过程中模拟反事实未来——对于每个动作提案，预测相应的世界状态演变，从而评估不同行动方案的后果。

### 3.3 三阶段训练策略

LCDrive的训练分为三个阶段（Figure 3）：

![[assets/figures/papers/paper_list_l2321_https_openaccess_thecvf_com_content_CVPR2026_html_Tan_Latent_Chain_of_Th/figures/003_Figure_3.jpg]]
*Figure 3: Training strategy. We first use a base non-reasoning VLA to create latent CoT data, and cold start LCDrive by supervised learning. Then, we conduct reinforcement learning to activate useful reasoning capacity of LCDrive*

**阶段0：无推理预训练。** 训练一个基础的非推理VLA模型，直接预测轨迹令牌，为后续阶段提供初始权重和动作提案监督。

**阶段1：CoT冷启动。** 这是连接无推理与潜在推理的关键桥梁。使用阶段0冻结的非推理VLA生成动作提案作为监督信号，构造潜在CoT的 $\mathrm{REASON}$ 令牌监督数据。阶段1的总损失联合优化令牌交叉熵损失和LWM预测MSE损失：

$$ \mathcal{L}_{\mathrm{stage-1}} = \mathcal{L}_{\mathrm{token}} + \lambda \mathcal{L}_{\mathrm{lwm}} $$

其中 $\lambda = 0.1$ 用于平衡两项损失。这一冷启动策略有效引导模型学习潜在推理格式，避免了从零开始学习推理结构的困难。

**阶段2：强化学习后训练。** 采用GRPO（Group Relative Policy Optimization）激活模型的推理能力。GRPO的目标函数为基于组相对优势的加权对数概率最大化：

$$ \mathcal{L}_{\mathrm{GRPO}} = -\frac{1}{G} \sum_{j=1}^G A^{(j)} \sum_t \log \pi_{\theta}(x_t^{(j)} \mid \mathrm{context}_t^{(j)}) $$

其中 $G$ 为每组生成的序列数，$A^{(j)}$ 为序列 $j$ 的相对优势。实验发现GRPO在去除KL正则化项后效果最佳，因此最终目标中省略了KL项。

### 3.4 关键模块汇总

| 模块 | 功能 | 关键设计 |
|------|------|----------|
| Vision Tokenizer | 将多视角图像帧编码为视觉令牌 | ViT-based编码器，逐帧独立处理 |
| Egomotion Tokenizer | 将自车历史运动学编码为令牌 | 紧凑令牌表示 |
| Trajectory Tokenizer | 将未来轨迹量化为离散动作令牌 | 1024码本，k-means聚类 |
| LWM Encoder | 将感知智能体边界框编码为潜在世界状态 | 轻量Transformer模块 |
| LWM Predictor | 根据上下文预测未来潜在世界状态 | 轻量MLP $f_\phi$ |
| Action Proposal Head | 生成动作提案块 | 与轨迹预测共享词表 |

### 3.5 推理预算与效率

潜在CoT的推理长度由 $K$（推理步数）和 $B$（并行分支数）控制。与文本CoT相比，潜在令牌序列更为紧凑——每个动作提案块仅10个离散令牌，每个LWM状态为固定维度的连续表示，远短于自然语言推理段落。Table 4的消融实验表明 $K=5, B=2$ 在性能与效率间取得了良好折衷，实现了1.8×的推理加速（相对于文本CoT基线）。

![[assets/figures/papers/paper_list_l2321_https_openaccess_thecvf_com_content_CVPR2026_html_Tan_Latent_Chain_of_Th/figures/001_Figure_1.jpg]]
*Figure 1: Latent Chain-of-Thought Reasoning. Compared to text-based CoT, our proposed Latent CoT provides more efficient and aligned reasoning traces for end-to-end driving VLA models*

## 实验与关键发现

### 4.1 实验设置

**数据集**。实验在 **PhysicalAI-AV** 数据集 上进行，该数据集包含 1700+ 小时的实车多相机驾驶日志。训练集包含 39,072 个片段（87 小时），验证集包含 23,758 个片段（53 小时）。如表 2 所示，子集经过场景平衡构建，覆盖标称场景与事件场景。

**评估指标**。主要指标包括：
- **ADE (m)**：平均位移误差，衡量预测轨迹与真值轨迹的整体偏差；
- **OffRoad2.5**：预测轨迹点偏离可行驶区域超过 2.5 m 的比例；
- **Coll5**：预测轨迹导致未来 5 秒内发生碰撞的场景比例。

**基线方法**。对比三类模型：
- **Non-reasoning VLA**：无推理模块，直接从传感器输入预测轨迹的基线 VLA 模型；
- **Text CoT (AR1)**：基于文本链式思考的 VLA 模型（Wang et al., arXiv 2025），在相同架构下将推理令牌替换为自然语言；
- **Latent CoT\***：使用真值世界模型状态的 LCDrive 变体，作为方法上界。

所有模型接收相同的传感器输入，非推理基线也可选择使用 LWM₀ 作为上下文，确保比较公平。推理延迟测试在相同硬件上进行。

### 4.2 主要结果

表 1 汇总了 PhysicalAI-AV 数据集上的主要评估结果。LCDrive 在所有指标上均显著优于非推理基线：

| 方法 | ADE (m) ↓ | OffRoad2.5 ↓ | Coll5 ↓ |
|------|-----------|--------------|---------|
| Non-reasoning VLA | 1.762 | 1.753 | 2.207 |
| Text CoT (AR1) | — | — | — |
| **LCDrive (Latent CoT)** | **1.626** | **1.219** | **0.836** |
| Latent CoT\* (Oracle) | 1.268 | — | — |
| Latent CoT\* + RL | **1.197** | — | — |

**关键发现**：

1. **轨迹质量全面提升**。LCDrive 相比非推理基线 ADE 降低 0.136 m（7.7%），OffRoad2.5 降低 0.534（30.4%），Coll5 降低 1.371（62.1%）。安全性指标的提升尤为显著，表明潜在推理有效改善了复杂场景下的决策质量。

2. **推理效率优势**。与文本 CoT 相比，LCDrive 实现 **1.8× 推理加速**。这源于潜在令牌序列远短于自然语言推理文本，且无需额外的文本解码开销。

3. **RL 后训练的叠加增益**。Latent CoT\* 结合 GRPO 强化学习后，ADE 从 1.268 进一步降至 1.197（降低 0.071 m），验证了潜在推理表示与 RL 训练的协同效应——紧凑的潜在空间使策略搜索更高效。

4. **与文本 CoT 的定性对比**。图 4 的定性结果表明，文本 CoT 容易产生与最终动作不一致的推理（如文字描述"左转"而轨迹偏右），而潜在 CoT 的推理令牌与动作词汇直接对齐，推理过程与输出轨迹高度一致。

### 4.3 按场景细分分析

表 2 按场景类型细分了 ADE 表现。Latent CoT\* 系列方法（使用真值 LWM）在不同场景下均保持最优，但 LCDrive（使用学习到的 LWM）在多数场景下仍显著优于非推理基线。值得注意的是，在需要复杂多智能体交互的场景中，LCDrive 的优势更加明显，这与潜在世界模型对时空几何和多智能体关系的隐式建模能力一致。

### 4.4 消融实验

**推理预算 (K, B)**。表 4 的消融实验表明，推理分支数 K=5 和每分支动作块数 B=2 在性能与效率间取得良好折衷。增大推理预算可小幅提升 ADE，但推理延迟线性增长；减小预算则导致推理不充分，ADE 回升。

**GRPO 中的 KL 正则化**。实验发现 GRPO **在去除 KL 正则化后效果最佳**，因此最终目标函数省略了 KL 项。这与潜在推理令牌空间本身具有良好结构有关，无需额外约束即可保持策略稳定。

**冷启动权重 λ**。Stage-1 CoT 冷启动中，式 (4) 的 LWM 损失权重设为 λ=0.1，有效平衡了令牌预测损失和世界模型预测损失。过大的 λ 会干扰动作令牌学习，过小则导致世界模型预测质量下降。

### 4.5 失败模式与局限性

尽管 LCDrive 展现了显著优势，分析揭示了以下局限：

1. **真值监督依赖**。潜在 CoT 训练需要真值监督（如智能体边界框用于 LWM 编码），大规模获取仍具挑战。当前依赖 PhysicalAI-AV 数据集提供的感知标注，限制了方法向无标注数据扩展的能力。

2. **可解释性缺失**。模型无法从潜在令牌中恢复人类可解释的推理过程。虽然推理质量更高，但调试和安全性验证时缺乏可读的中间表示。

3. **固定推理预算**。当前 K 和 B 为固定值，无法根据场景复杂度自适应调整。简单场景可能浪费计算，极端复杂场景则可能推理不足。

4. **LWM 质量瓶颈**。LCDrive 的性能受限于学习到的 LWM 精度。当 LWM 预测误差较大时，反事实推理的质量下降，影响最终轨迹规划。这一现象在 Latent CoT\*（使用真值 LWM）与 LCDrive 的性能差距中得到印证。

![[assets/figures/papers/paper_list_l2321_https_openaccess_thecvf_com_content_CVPR2026_html_Tan_Latent_Chain_of_Th/figures/004_Table_1.jpg]]
*Table 1: Main evaluation results on the PhysicalAI-AV dataset [24]. Lower is better for all metrics, bold is best*

![[assets/figures/papers/paper_list_l2321_https_openaccess_thecvf_com_content_CVPR2026_html_Tan_Latent_Chain_of_Th/figures/005_Table_2.jpg]]
*Table 2: ADE split by scenario. Columns are ordered with methods using GT LWM (marked with ∗) shown first. Bold is best*

![[assets/figures/papers/paper_list_l2321_https_openaccess_thecvf_com_content_CVPR2026_html_Tan_Latent_Chain_of_Th/figures/006_Figure_4.jpg]]
*Figure 4: Qualitative Results. Qualitative comparison of textual and latent reasoning in driving VLA models. Latent CoT captures fine-grained spatial relationships and multi-agent interactions while using a smaller inference budget, leading to more stable and accurate trajectory predictions. In each case, we highlight the main misalignment of the Text CoT reasoning with the final trajectory*

## 定位与知识库关联

### 1. 推理范式对比：从文本链式思考到潜在链式思考

LCDrive 的核心贡献在于重新定义了端到端自动驾驶 VLA 模型中的推理表示。与现有的文本链式思考（Text CoT）方法相比，LCDrive 在三个维度上实现了范式转变：

**表示对齐性**：文本 CoT 基线（Wang et al., arXiv 2025）使用自然语言令牌进行推理，但自然语言本质上不适合表示时空几何关系和多智能体交互。LCDrive 将推理实例化为与动作词汇对齐的潜在令牌序列，使推理过程与最终轨迹预测共享相同的离散动作空间。具体而言，动作提案块 $A_t^{(i)}$ 使用与最终轨迹预测 $\tau$ 相同的 1024 码本词汇表，从根本上消除了语言推理与驾驶动作之间的语义鸿沟。

**推理效率**：文本 CoT 需要自回归生成长序列的自然语言描述，引入显著推理延迟。LCDrive 通过紧凑的潜在令牌序列实现推理，实验表明推理速度相比文本 CoT 基线提升 1.8 倍。这一加速源于潜在令牌序列的短长度和与动作词汇的直接映射，避免了自然语言解码的计算开销。

**推理-决策一致性**：文本 CoT 存在典型的“言行不一”问题——语言推理可能描述“左转”但实际输出轨迹为右转。LCDrive 通过交替生成动作提案和潜在世界模型预测，确保推理过程每一步都与可执行的动作提案绑定，从而保证推理与最终决策的高度一致性。

### 2. 与无推理基线的架构关系

LCDrive 建立在非推理 VLA 基线之上，两者共享相同的传感器输入管道（Vision Tokenizer 和 Egomotion Tokenizer）和轨迹预测头。关键区别在于 LCDrive 在输入令牌和轨迹令牌之间插入了 REASON 序列：

$$
\bigl[ o_{\mathrm{image}}, o_{\mathrm{ego}}, \mathrm{REASON}, \tau \bigr]
$$

非推理基线直接建模 $[o_{\mathrm{image}}, o_{\mathrm{ego}}, \tau]$，而 LCDrive 通过 REASON 序列引入显式推理能力。值得注意的是，非推理 VLA 在 LCDrive 的训练中扮演双重角色：（1）作为 Stage 0 的预训练起点；（2）在 Stage 1 CoT 冷启动阶段，其冻结版本用于生成动作提案监督信号，引导 LCDrive 学习潜在推理格式。

### 3. 潜在世界模型的监督来源与适用边界

LCDrive 的潜在世界模型（LWM）需要真值监督进行训练。LWM Encoder 将感知到的智能体边界框编码为潜在世界状态令牌 $\mathrm{LWM}_t$，LWM Predictor 则学习预测未来的潜在世界状态。这种设计使模型能够模拟反事实未来，但引入了对边界框标注的依赖。

**适用边界**：
- **强依赖场景**：需要精确多智能体交互建模的复杂城市场景（如无保护左转、拥挤环岛），LWM 提供的反事实推理能力最为关键。Table 2 的场景细分结果显示，Latent CoT* 在交互密集场景中的 ADE 改进尤为显著。
- **弱依赖场景**：在简单高速公路巡航等场景中，LWM 的边际收益可能有限，非推理基线已能取得可接受性能。
- **数据约束**：当前方法依赖 PhysicalAI-AV 数据集提供的边界框标注，在大规模未标注数据上的泛化能力尚未验证。

### 4. 训练策略的独特设计

LCDrive 的三阶段训练策略区别于现有 VLA 模型的单阶段监督微调范式：

- **Stage 0（非推理预训练）**：建立基础的视觉-运动映射能力。
- **Stage 1（CoT 冷启动）**：利用冻结的非推理 VLA 生成动作提案作为监督，结合 LWM 预测损失（权重 $\lambda=0.1$）进行联合优化。这一阶段解决了潜在推理令牌缺乏直接监督的核心挑战。
- **Stage 2（GRPO 强化学习后训练）**：通过组相对优势优化激活推理能力。消融实验表明，GRPO 在去除 KL 正则化后效果最佳，这与 LLM 领域的常见做法形成对比。

### 5. 局限性与开放问题

**当前局限**：
1. **监督依赖性**：潜在 CoT 训练需要真值监督（智能体边界框），大规模获取仍具挑战，限制了方法向更大规模未标注数据的扩展。
2. **可解释性缺失**：模型无法从潜在令牌中恢复人类可解释的推理过程，这在安全关键应用中可能构成部署障碍。
3. **推理预算固定**：推理分支数 $K=5$ 和每分支动作提案块数 $B=2$ 在所有场景中保持固定，缺乏自适应调整机制。

**开放问题**：
1. 如何在大规模数据上有效获取潜在世界模型所需的真值监督？可能的路径包括自监督预训练或利用神经辐射场（NeRF）等隐式表示。
2. 如何从潜在 CoT 令牌中解码出人类可理解的推理过程？这可能需要设计专门的解码器或将潜在令牌与自然语言空间对齐。
3. 如何动态调整推理分支数 $K$ 和 $B$ 以适应不同场景复杂度？简单的场景分类器或基于不确定性的自适应机制可能是可行的方向。
4. 潜在 CoT 的推理能力是否可以通过更大规模的 RL 后训练进一步激发？当前实验仅在有限规模上进行 GRPO 训练，扩展 RL 训练的计算预算可能带来额外收益。

## 原文 PDF

![[paperPDFs/CVPR_2026/Latent_Chain_of_Thought_World_Modeling_for_End_to_End_Autonomous_Driving.pdf]]
