---
title: "MSJoE: Jointly Evolving MLLM and Sampler for Efficient Long-Form Video Understanding"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/MSJoE_Jointly_Evolving_MLLM_and_Sampler_for_Efficient_Long_Form_Video_Understanding.pdf
project_link: null
code_link: null
aliases:
- MSJEM
- MSJoE
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 将问题分解为多个视觉导向的查询，并利用可训练采样器从 CLIP 相似度矩阵中学习选择关键帧，同时通过联合强化学习实现 MLLM 与采样器的双向适应。
primary_logic: 通过联合强化学习（GRPO+REINFORCE）同时进化 MLLM 和轻量级 1D U-Net 采样器，使 MLLM 能够生成引导关键帧选择的推理查询，并适应稀疏关键帧分布，从而在极低帧预算下显著提升长视频理解精度。
claims:
- MSJoE 在四个长视频基准上比基础 MLLM 平均提升 8.0 个百分点（64 帧）
- 消融实验证明，冻结 MLLM 或移除联合训练均会导致性能显著下降，联合进化是必要的
- MSJoE 生成的查询能定位到多个有意义的事件区域，超越了问题本身的视觉线索
- 在 32 帧预算下，MSJoE 即可超越均匀采样的 64 帧，验证了关键帧选择的有效性
---

# MSJoE: Jointly Evolving MLLM and Sampler for Efficient Long-Form Video Understanding

> [!tip] 核心洞察
> 通过联合强化学习（GRPO+REINFORCE）同时进化 MLLM 和轻量级 1D U-Net 采样器，使 MLLM 能够生成引导关键帧选择的推理查询，并适应稀疏关键帧分布，从而在极低帧预算下显著提升长视频理解精度。

| 字段 | 内容 |
|------|------|
| 中文题名 | MSJoE：联合进化多模态大语言模型与采样器以高效理解长视频 |
| 英文题名 | MSJoE: Jointly Evolving MLLM and Sampler for Efficient Long-Form Video Understanding |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2602.22932) |
| Topic | #topic/vision_multimodal_applications #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | MLLM-Sampler Joint Evolution (MSJoE) |
| Dataset | MLVU, LVBench, Video-MME Long, LongVideoBench |

> [!tip] 效果简介
> - MLVU (64 frames) 上，accuracy (%) 75.1 vs Uniform Sampling 65.3 (+9.8)。
> - LVBench (64 frames) 上，accuracy (%) 51.1 vs Uniform Sampling 39.2 (+11.9)。
> - Video-MME Long (64 frames) 上，accuracy (%) 57.4 vs Uniform Sampling 52.2 (+5.2)。

## 概要

### 问题背景

长视频理解的核心瓶颈在于**密集均匀采样难以高效捕捉稀疏分布的关键事件**。长视频中与问题相关的视觉线索往往只出现在少数几个片段，而均匀采样在固定帧预算下要么遗漏这些稀疏线索，要么浪费大量计算资源在冗余帧上。现有的关键帧采样方法（如基于启发式规则的 **Q-Frame**、**BOLT**，或基于可训练采样器的 **TSPO**）虽然试图缓解这一问题，但它们要么依赖固定的相似度匹配策略，要么将采样器与多模态大语言模型（MLLM）分离训练，导致**采样器无法感知 MLLM 的推理需求，MLLM 也无法适应稀疏关键帧的分布偏移**。

### 核心方法

**MSJoE**（MLLM-Sampler Joint Evolution）提出了一种**联合进化**框架，将问题分解为两个协同优化的子任务：

1. **推理引导的查询生成**：MLLM 根据稀疏预览帧生成多个视觉导向的推理查询，这些查询描述了与问题相关的多样化视觉视角，而非简单复述问题文本。
2. **可学习的关键帧采样**：轻量级 1D U-Net 采样器从 CLIP 相似度矩阵中学习选择关键帧，将查询-帧匹配转化为概率采样问题。

整个框架通过**端到端联合强化学习**进行优化——MLLM 采用 **GRPO** 更新查询生成策略，采样器采用 **REINFORCE** 更新帧选择策略，二者共享同一个奖励信号（准确性奖励 + 格式奖励 + 信息性奖励），从而实现**双向适应**：MLLM 学会生成更有利于关键帧检索的查询，采样器学会适应 MLLM 的推理偏好。

### 核心结论

在四个长视频理解基准（MLVU、LVBench、Video-MME Long、LongVideoBench）上，MSJoE 以 **Qwen2.5-VL-7B** 为基础 MLLM，在 64 帧预算下相比均匀采样**平均提升 8.0 个百分点**，且**超越最强基线方法 TSPO 平均 1.1 个百分点**。在 32 帧预算下，MSJoE 的准确率即可**超越均匀采样的 64 帧**，验证了关键帧选择的有效性。消融实验进一步证明，**冻结 MLLM 或移除联合训练均会导致性能显著下降**，联合进化是必要的。

### 方法谱系与知识库定位

MSJoE 处于**长视频理解 × 强化学习驱动采样**的交叉点：

- **相对于静态采样方法**（Q-Frame、BOLT）：MSJoE 将固定的相似度匹配替换为可训练的采样器，并通过 MLLM 生成推理查询替代直接使用问题文本，显著提升了帧选择的针对性和鲁棒性。
- **相对于可训练采样器方法**（TSPO）：MSJoE 的关键突破在于**联合进化**——TSPO 使用固定查询且 MLLM 保持冻结，而 MSJoE 让 MLLM 与采样器在 RL 下同步更新，使查询生成与帧选择形成闭环优化。
- **相对于通用长视频 MLLM**（LongVU、NVILA、VideoMind-7B）：MSJoE 是一种**即插即用的采样增强框架**，可与不同基础 MLLM 结合，在保持模型规模不变的前提下提升长视频理解效率。
- **相对于闭源大模型**（GPT-4o、Gemini-1.5-pro）：MSJoE 以 7B 开源模型为基础，在 64 帧预算下实现了有竞争力的性能，展示了联合进化策略在资源受限场景下的价值。

### 证据强度与注意事项

本文的核心结论由多基准实验和系统消融支持，证据强度较高（置信度 0.9–0.95）。主要局限在于：方法重度依赖固定的 CLIP 视觉-语言对齐，可能在某些领域或语言中泛化不足；仅在多项选择问答任务上验证，对开放式视频问答或生成任务的有效性尚未检验；联合 RL 训练需要保持多轨迹采样，增加了训练计算开销。

### 长视频理解的瓶颈：密集采样与稀疏事件的矛盾

长视频理解任务的核心挑战在于，视频时长动辄数十分钟甚至数小时，而多模态大语言模型（MLLM）受限于上下文窗口和计算资源，只能处理有限数量的视频帧。当前的主流范式是**均匀采样**——以固定时间间隔从视频中抽取帧送入 MLLM。然而，这种策略存在根本性缺陷：视频中的关键事件往往是稀疏且非均匀分布的，均匀采样极易在大量冗余帧上浪费计算资源，同时遗漏那些对回答问题至关重要的短暂视觉线索。

这一矛盾在多项选择问答（MQA）基准上表现尤为突出。以 Qwen2.5-VL-7B 为基础 MLLM，均匀采样 64 帧在 MLVU 上仅取得 65.3% 的准确率，在 LVBench 上更是低至 39.2%（Table 1）。这表明，**密集均匀采样并不能有效捕捉长视频中的关键信息**，亟需更智能的帧选择策略。

### 现有方法的缺口：从启发式到可训练采样器

为缓解上述问题，研究者提出了多种关键帧采样方法。**启发式方法**如 Q-Frame 和 BOLT 基于预定义规则（如问题-帧相似度）选择帧，但缺乏对 MLLM 实际需求的适应能力。**可训练采样器**如 TSPO 引入轻量级网络来学习帧选择，但其查询构建通常依赖固定的问题文本，无法根据视频内容动态调整检索焦点。

这些方法的共同局限在于：**MLLM 与采样器之间缺乏双向适应**。采样器独立于 MLLM 训练，MLLM 也未被优化以理解采样器选出的稀疏帧分布。当采样器选出非均匀分布的关键帧时，未经过适配的 MLLM 可能无法有效利用这些帧中的信息，导致性能提升受限。此外，仅使用问题文本作为查询难以捕捉复杂推理需求——一个问题可能涉及多个视觉概念，而这些概念在视频中的分布往往是分散且动态变化的。

### 本文动机：联合进化 MLLM 与采样器

针对上述缺口，本文提出核心假设：**MLLM 与采样器应当协同进化**。具体而言，MLLM 应具备生成视觉推理查询的能力，以引导采样器定位关键帧；同时，MLLM 本身也应适应采样器输出的稀疏帧分布，从而在极低帧预算下维持高精度理解。这一假设将帧选择问题重新定义为 MLLM 与采样器的**联合优化问题**，而非两个独立模块的简单串联。

为实现这一目标，MSJoE 框架将问题分解为多个视觉导向的查询，利用可训练的 1D U-Net 采样器从 CLIP 相似度矩阵中学习选择关键帧，并通过联合强化学习（GRPO + REINFORCE）实现 MLLM 与采样器的端到端协同训练。实验表明，该框架在四个长视频基准上平均提升 8.0 个百分点（64 帧），且在 32 帧预算下即可超越均匀采样的 64 帧性能（Figure 4），验证了关键帧选择的有效性与联合进化的必要性。

## 核心方法与创新机理

MSJoE 的核心创新在于将长视频关键帧选择从“静态检索”或“独立训练采样器”的范式，推进为 **MLLM 与采样器的双向协同进化**。具体而言，该方法在三个关键维度上改变了 baseline 的设计。

### 1. 从问题文本到多视角推理查询

传统方法（如 Q-Frame、BOLT）直接使用问题文本与视频帧进行 CLIP 相似度匹配，但单一问题文本往往无法覆盖答案所需的多重视觉线索。MSJoE 引入了 **MLLM 引导的查询生成**：给定问题和稀疏预览帧 $\mathcal{F}_{\mathrm{init}}$，MLLM 生成一组视觉推理查询 $\{q^j\}_{j=1}^{N_q}$，每个查询描述与问题相关的不同视觉视角。这一设计使得帧选择不再受限于问题的字面表述，而是能够主动定位多个有意义的事件区域（Figure 6 的对比分布验证了多查询相比单一问题查询能发现更丰富的帧候选）。

### 2. 从启发式采样到可学习的关键帧选择

Baseline 方法依赖均匀采样或基于相似度分数的 top-k 启发式选择，缺乏对“哪些帧对 MLLM 理解最有益”的学习能力。MSJoE 采用一个轻量级 **1D U-Net 采样器**，将 CLIP 相似度矩阵映射为帧级采样概率，从而端到端地学习关键帧选择策略。该采样器通过 REINFORCE 算法进行预训练和联合优化，使得帧选择直接以最终答案质量为导向，而非依赖手工设计的中间准则。

### 3. 从分离训练到联合强化学习进化

此前的可训练采样器方法（如 TSPO）使用固定查询且与 MLLM 分离训练，导致采样器无法适应 MLLM 的理解偏好，MLLM 也难以适应稀疏关键帧的分布。MSJoE 通过 **联合强化学习** 打破了这一隔离：MLLM 通过 GRPO 优化查询生成和答案推理，采样器通过 REINFORCE 优化帧选择，两者共享同一个答案质量奖励信号。消融实验（Table 2）表明，冻结 MLLM 或移除联合训练均会导致性能显著下降，证实了双向适应的必要性——MLLM 学会生成更利于帧检索的查询，同时适应稀疏关键帧输入；采样器则学会选择更契合 MLLM 理解需求的帧。

这一联合进化框架使得 MSJoE 在 32 帧预算下即可超越均匀采样的 64 帧性能（Figure 4），在四个长视频基准上平均提升 8.0 个百分点（Table 1），验证了“让采样器理解模型，让模型适应采样器”这一核心洞察的有效性。

MSJoE 的核心思路是将长视频理解分解为“推理引导的查询生成 → 跨模态帧匹配 → 可学习关键帧采样 → 答案生成”四个协同步骤，并通过端到端强化学习实现 MLLM 与采样器的联合进化。整体流程如 Figure 3 所示。

![[assets/figures/papers/paper_list_l769_https_arxiv_org_abs_2602_22932/figures/003_Figure_3.jpg]]
*Figure 3: The proposed MSJoE framework. Given a video and question, MSJoE generates reasoning-based queries from a sparse preview, matches them against dense frames via CLIP to create a similarity matrix, and uses a lightweight U-Sampler to select informative frames. The MLLM then processes these key frames at high resolution for answer generation. The entire framework is jointly optimized through end-to-end reinforcement learning*

### 推理流程

给定一段包含 $T$ 帧的长视频 $\mathcal{V}$ 和一个问题 $q$，目标是从中选出 $K$ 个信息量最大的关键帧（$K \ll T$），在保持答案精度的同时控制计算开销。MSJoE 的推理管线包含四个步骤：

**步骤一：MLLM 引导的查询生成。** MLLM 首先接收问题 $q$ 和一组稀疏预览帧 $\mathcal{F}_{\mathrm{init}}$（数量为 $N_{\mathrm{init}}$，默认取 $K/2$），生成 $N_q$ 个视觉推理查询 $\{q^j\}_{j=1}^{N_q}$。这些查询并非简单复述问题，而是从不同视觉角度描述与问题相关的场景线索，例如“人物是否在厨房中移动”“画面中是否出现红色车辆”等。形式上：

$$\{ q^{j} \}_{j=1}^{N_q} = \mathbf{MLLM}(q, \mathcal{F}_{\mathrm{init}}; \theta_{\mathbf{MLLM}})$$

**步骤二：CLIP 相似度计算。** 将生成的查询 $\{q^j\}$ 与所有 $T$ 帧密集采样帧 $\{f_i\}_{i=1}^{T}$ 分别送入冻结的 CLIP 文本编码器和图像编码器，计算余弦相似度矩阵 $\mathbf{S} \in \mathbb{R}^{N_q \times T}$：

$$s_{ji} = \mathrm{sim}(\mathrm{CLIP}_{\mathrm{text}}(q^j), \mathrm{CLIP}_{\mathrm{image}}(f_i))$$

该矩阵的每一行 $j$ 表示第 $j$ 个查询与所有帧的语义相关性分布。

**步骤三：可学习关键帧采样。** 轻量级 1D U-Net 采样器将相似度矩阵 $\mathbf{S}$ 作为输入，输出每帧被选中的概率分布 $\mathbf{p} \in [0,1]^T$，并据此采样出 $K$ 个关键帧 $\mathcal{F}_{\mathrm{selected}}$。U-Net 的跳跃连接结构使其能够同时捕捉局部峰值和全局上下文，从而在多个查询之间进行权衡。

**步骤四：答案生成。** MLLM 接收选中的关键帧 $\mathcal{F}_{\mathrm{selected}}$ 和原始问题 $q$，生成最终答案 $a$：

$$a = \mathbf{MLLM}(q, \mathcal{F}_{\mathrm{selected}}; \theta_{\mathbf{MLLM}})$$

### 训练范式

MSJoE 采用两阶段训练策略，使 MLLM 和采样器在联合强化学习框架下双向适应。

**阶段一：采样器预训练。** 在联合训练之前，先对采样器进行 REINFORCE 预训练，使用难度感知奖励（Difficulty-aware Reward）。对于难度为 $c \in (0,1)$ 的样本，正确采样获得奖励 $A_{\mathrm{sampler}} = 1/c$，错误采样获得惩罚 $A_{\mathrm{sampler}} = -1/(1-c)$。该设计使采样器优先从高难度样本中学习关键帧选择策略，为后续联合训练提供稳定初始化。预训练数据来自作者构建的 LongVideoQA-ALL 数据集。

**阶段二：联合强化学习。** MLLM 与采样器端到端联合优化。MLLM 采用 GRPO（Group Relative Policy Optimization），采样器采用 REINFORCE。总奖励 $r$ 由三部分组成：

- **准确性奖励 $r_{\mathrm{acc}}$**：答案与标准答案的匹配程度；
- **格式奖励 $r_{\mathrm{format}}$**：输出格式的规范性；
- **信息性奖励 $r_{\mathrm{info}}$**：鼓励生成的查询具有清晰的注意力峰值，定义为：

$$r_{\mathrm{info}} = 0.1 \cdot \frac{ \sum_j \mathbb{I}\left[ \frac{\max_i s_{ji}}{\min_i s_{ji}} > \tau_{\mathrm{info}} \right] }{N_q}$$

其中 $\tau_{\mathrm{info}} = 10$。该奖励推动 MLLM 生成能精准定位特定帧区域的查询，而非产生模糊的均匀相似度分布。

MLLM 的 GRPO 目标为：

$$\mathcal{T}_{\mathrm{G}}(\theta) = \mathbb{E}_{o_1,\dots,o_G\sim\pi_{\theta_{\mathrm{old}}}, q\sim Q} \left[ \frac{1}{G} \sum_{i=1}^{G} \left( \min\left( s_i A_i, \mathrm{clip}(s_i, 1-\epsilon, 1+\epsilon) A_i \right) \right) \right]$$

其中 $s_i = \frac{\pi_{\theta}(o_i|q)}{\pi_{\theta_{\mathrm{old}}}(o_i|q)}$ 为重要性采样比率，$A_i = \frac{r_i - \mathrm{mean}(r_1, \dots, r_G)}{\mathrm{std}(r_1, \dots, r_G)}$ 为组内相对优势。采样器的 REINFORCE 目标为：

$$\mathcal{I}_{\mathrm{R}}(\phi) = \mathbb{E}_{x_1,\dots,x_K\sim\mathbf{p}} \left[ A_{\mathrm{sampler}} \cdot \sum_{k=1}^{K} \nabla_{\phi} \log \mathbf{p}(x_k) \right]$$

### 关键设计决策

MSJoE 区别于现有方法的核心在于 **MLLM 与采样器的双向协同进化**：MLLM 不仅被动回答，还主动生成引导帧选择的推理查询；采样器不仅筛选帧，其选择结果又通过 RL 信号反向塑造 MLLM 的查询生成策略。这种闭环设计使 MLLM 逐步适应稀疏关键帧分布，而采样器则学会解读 MLLM 的推理意图。

**与基线的本质差异**：静态关键帧采样（如均匀采样、Q-Frame、BOLT）使用固定规则，无法根据问题动态调整；可训练采样器（如 TSPO）虽能学习帧选择，但使用固定查询且 MLLM 保持冻结，缺乏查询-帧选择的协同优化。MSJoE 通过联合 RL 打破了这一单向依赖，使两个模块在训练中相互塑造（Figure 1 对比了三种范式的差异）。

![[assets/figures/papers/paper_list_l769_https_arxiv_org_abs_2602_22932/figures/001_Figure_1.jpg]]
*Figure 1: A direct comparison among static key-frame sampling algorithms, trainable key-frame sampler, and our proposed MLLM-Sampler Joint Evolution framework (MSJoE)*

MSJoE 的推理流水线由四个核心模块串联构成，形成“查询生成—相似度计算—关键帧采样—答案生成”的闭环。整个框架在端到端强化学习下联合优化，使 MLLM 与采样器双向适应。

### 1. MLLM 引导的查询生成

给定长视频问题 $q$ 和一小组稀疏预览帧 $\mathcal{F}_{\mathrm{init}}$，MLLM 首先生成 $N_q$ 个视觉推理查询，每个查询描述与问题相关的不同视觉视角：

$$\{ q^{j} \}_{j=1}^{N_q} = \mathbf{MLLM}(q, \mathcal{F}_{\mathrm{init}}; \theta_{\mathbf{MLLM}})$$

其中 $\theta_{\mathbf{MLLM}}$ 为 MLLM 的可训练参数，$\mathcal{F}_{\mathrm{init}}$ 由 $N_{\mathrm{init}} = K / 2$ 帧均匀采样的预览帧构成（$K$ 为总帧预算）。这一步将原始问题扩展为多个面向视觉检索的子查询，使采样器能够定位到问题文本本身无法直接命中的关键事件区域（参见 Figure 6 的对比分布）。

### 2. CLIP 相似度矩阵计算

将生成的文本查询 $\{q^j\}$ 与密集采样的全部 $T$ 帧 $\{f_i\}_{i=1}^T$ 分别通过冻结的 CLIP 文本编码器和图像编码器，计算余弦相似度矩阵 $\mathbf{S} \in \mathbb{R}^{N_q \times T}$：

$$s_{ji} = \mathrm{sim}(\mathrm{CLIP}_{\mathrm{text}}(q^j), \mathrm{CLIP}_{\mathrm{image}}(f_i))$$

该矩阵的每一行 $s_{j:}$ 编码了第 $j$ 个查询与各帧的语义关联强度。使用冻结 CLIP（Clip-ViT-Large-Patch14）保证了视觉-语言对齐的稳定性，同时避免了端到端训练中编码器偏移带来的不稳定性。

### 3. 1D U-Net 关键帧采样器

相似度矩阵 $\mathbf{S}$ 被送入一个轻量级 1D U-Net 采样器，其输出为各帧被选中的概率分布 $\mathbf{p} \in [0,1]^T$。采样器从该分布中无放回地采样 $K$ 帧作为关键帧集 $\mathcal{F}_{\mathrm{selected}}$。U-Net 的 1D 卷积结构天然适合建模视频帧序列的局部时间依赖，且参数量远小于 MLLM，使联合训练的计算开销可控。

### 4. 答案生成

MLLM 基于选中的关键帧 $\mathcal{F}_{\mathrm{selected}}$ 和原始问题 $q$ 生成最终答案：

$$a = \mathbf{MLLM}(q, \mathcal{F}_{\mathrm{selected}}; \theta_{\mathbf{MLLM}})$$

注意此阶段仅输入采样器选出的关键帧，稀疏预览帧 $\mathcal{F}_{\mathrm{init}}$ 被屏蔽，以保证与非推理基线方法比较的公平性。

### 5. 联合强化学习目标

MSJoE 的总奖励由三部分组成：

$$r = r_{\mathrm{acc}} + r_{\mathrm{format}} + r_{\mathrm{info}}$$

其中 $r_{\mathrm{acc}}$ 为答案正确性奖励（多项选择匹配则 $r_{\mathrm{acc}} = 1$，否则为 $0$），$r_{\mathrm{format}}$ 为格式遵循奖励，$r_{\mathrm{info}}$ 为信息性奖励，鼓励查询产生具有清晰高注意力区域的相似度分布：

$$r_{\mathrm{info}} = 0.1 \cdot \frac{ \sum_j \mathbb{I}\left[ \frac{\max_i s_{ji}}{\min_i s_{ji}} > \tau_{\mathrm{info}} \right] }{N_q}$$

其中 $\tau_{\mathrm{info}} = 10$ 为峰值比阈值。该奖励推动 MLLM 生成能精准定位特定帧的查询，而非产生均匀分布的模糊匹配。

MLLM 通过 **GRPO**（Group Relative Policy Optimization）优化。对于每个问题 $q$，从旧策略 $\pi_{\theta_{\mathrm{old}}}$ 采样 $G$ 个输出 $\{o_i\}$，计算重要性采样比率 $s_i = \frac{\pi_{\theta}(o_i|q)}{\pi_{\theta_{\mathrm{old}}}(o_i|q)}$ 和组内相对优势 $A_i = \frac{r_i - \mathrm{mean}(r_1,\dots,r_G)}{\mathrm{std}(r_1,\dots,r_G)}$，目标函数为：

$$\mathcal{T}_{\mathrm{G}}(\theta) = \mathbb{E}_{o_1,\dots,o_G\sim\pi_{\theta_{\mathrm{old}}}, q\sim Q} \left[ \frac{1}{G} \sum_{i=1}^{G} \min\left( s_i A_i, \mathrm{clip}(s_i, 1-\epsilon, 1+\epsilon) A_i \right) \right]$$

采样器则通过 **REINFORCE** 优化，使用总奖励 $r$ 作为采样器的优势信号 $A_{\mathrm{sampler}}$：

$$\mathcal{I}_{\mathrm{R}}(\phi) = \mathbb{E}_{x_1,\dots,x_K\sim\mathbf{p}} \left[ A_{\mathrm{sampler}} \cdot \sum_{k=1}^{K} \nabla_{\phi} \log \mathbf{p}(x_k) \right]$$

在采样器预训练阶段，$A_{\mathrm{sampler}}$ 进一步引入难度感知加权：对于难度 $c \in (0,1)$ 的样本，正确时 $A_{\mathrm{sampler}} = 1/c$，错误时 $A_{\mathrm{sampler}} = -1/(1-c)$，使采样器在困难样本上获得更强的学习信号。消融实验（Table 3）表明，移除该难度感知奖励使平均准确率下降 3.9 个百分点，验证了其关键作用。

## 实验与关键发现

### 主实验结果

MSJoE 在四个长视频理解基准上均显著超越基础 MLLM 的均匀采样基线。表 1 汇总了主要对比结果。

在 64 帧预算下，MSJoE 相较均匀采样（Uniform Sampling）的平均提升达 8.0 个百分点。具体到各基准：
- **MLVU**：75.1% vs. 65.3%，提升 +9.8 个百分点；
- **LVBench**：51.1% vs. 39.2%，提升 +11.9 个百分点；
- **Video-MME Long**：57.4% vs. 52.2%，提升 +5.2 个百分点；
- **LongVideoBench**：62.2% vs. 57.3%，提升 +4.9 个百分点。

与现有最强基线方法 TSPO 相比，MSJoE 在四个基准上平均领先 1.1 个百分点。值得注意的是，MSJoE 在仅使用 32 帧时，其平均准确率已超越均匀采样的 64 帧结果，验证了关键帧选择策略的有效性。

在与其他通用长视频 MLLM（LongVU、NVILA）和基于推理的方法（VideoMind-7B）的对比中，MSJoE 同样保持了领先优势。与闭源模型 GPT-4o 和 Gemini-1.5-pro 的对比则表明，MSJoE 在开放模型上实现了具有竞争力的性能。

### 消融实验分析

#### MLLM 与采样器模块消融

表 2 在 32 帧固定预算下，对 MLLM 和采样器的训练状态进行了系统性消融。核心发现如下：

- **联合进化的必要性**：设置 iii（PT-T*）和 iv 中冻结 MLLM，仅使用预训练采样器或联合训练采样器，性能均显著低于完整 MSJoE。这表明 MLLM 必须与采样器协同进化，才能生成适应稀疏关键帧分布的推理查询。
- **多查询 vs. 单查询**：仅使用问题文本作为单一查询（设置 vi，F*）虽优于均匀采样，但仍远不如多查询方案。同时，未经训练的多查询采样（设置 v）性能较差，强调了采样器训练的必要性。
- **采样器预训练的作用**：设置 ii（T-PT）中采样器仅预训练而 MLLM 联合训练，性能接近完整方案，说明采样器预训练为联合 RL 提供了良好的初始化基础。

#### 奖励函数消融

表 3 展示了信息性奖励（Informativeness Reward, IR）和难度感知奖励（Difficulty-aware Reward, DR）的消融结果：

- **难度感知奖励**：取消采样器预训练中的难度感知奖励，使平均准确率下降 3.9 个百分点。该奖励根据问题难度对正确/错误答案赋予不同权重，有效引导采样器关注更具挑战性的样本。
- **信息性奖励**：移除联合 RL 中的信息性奖励导致轻微性能退化。该奖励鼓励 MLLM 生成具有清晰高注意力区域的查询（即相似度矩阵中 max/min 比值超过阈值 $\tau_{\text{info}}=10$），使采样器更容易定位关键帧。

#### 帧预算与采样策略

图 4 展示了不同输入帧数（8～64）下的性能变化。MSJoE 在各种帧预算下始终优于均匀采样，且性能随帧数增加稳定提升。相比之下，Top-k 采样策略在低帧预算下表现不稳定，进一步验证了可学习采样器的鲁棒性。

#### 预览帧数量影响

图 7 显示，预览帧数量从 0 增加至 16 时，平均准确率大幅提升。这表明为 MLLM 提供稀疏预览帧作为视觉上下文，对于生成有效的推理查询至关重要。预览帧数量设置为总帧预算的一半（$N_{\text{init}} = K // 2$）是实验验证的较优配置。

### 推理效率分析

表 4 报告了 MSJoE 在 1000 个样本上的平均推理时间。四个步骤的时间开销分别为：
- MLLM 引导的查询生成
- CLIP 相似度计算
- U-Net 采样器帧选择
- MLLM 答案生成

由于查询生成和相似度计算的结果可跨样本缓存，QA 阶段的整体延迟得到有效控制。在 64 帧预算下，MSJoE 以可接受的额外计算成本换取了显著的精度提升。

### 定性分析

图 5 展示了不同采样策略生成的帧集定性对比。对于问题“是什么促使她改变饮食习惯？”，均匀采样遗漏了关键线索帧，而 MSJoE 选中的帧集中包含了与糖尿病诊断相关的画面，直接指向正确答案。

图 6 进一步揭示了 MSJoE 的查询机制优势。左侧显示问题-帧相似度分布（Top-k 方法），右侧显示 MSJoE 的查询-帧相似度分布。蓝色标记表示各方法选中的帧。MSJoE 生成的多个查询能够定位到多个有意义的事件区域，超越了问题本身直接提供的视觉线索，从而实现了更全面的关键帧覆盖。

### 训练稳定性

图 8 展示了不同训练配置下的平滑奖励曲线。完整的 MSJoE 训练配置（包含信息性奖励和难度感知奖励）展现出最稳定的收敛趋势，而移除任一奖励组件均导致奖励曲线的波动增大或收敛速度放缓，从训练动力学角度验证了各奖励组件的互补作用。

![[assets/figures/papers/paper_list_l769_https_arxiv_org_abs_2602_22932/figures/004_Table_1.jpg]]
*Table 1: Comparison of MLLMs and baseline methods against our method MSJoE on four benchmarks. We bold the best results and highlight performance gain over the base-MLLM. The performance of baseline methods are reported according to published papers*

![[assets/figures/papers/paper_list_l769_https_arxiv_org_abs_2602_22932/figures/005_Figure_4.jpg]]
*Figure 4: Ablation studies on varying input frames (x-axis). Four methods are evaluated: MSJoE in light violet, Top-k in red, and Uniform Sampling uniform sampling in gray*

![[assets/figures/papers/paper_list_l769_https_arxiv_org_abs_2602_22932/figures/006_Table_2.jpg]]
*Table 2: Ablation studies on the MLLM (M) and Sampler (S) module with a fixed input budget of 32 frames. The module settings T, PT, and F denote Training, Pre-Trained, Frozen respectively. Setting iii (PT-T*) denotes we feed the same frames (reasoned and sampled) as Ours to a frozen MLLM. Setting vi (F*) denotes using a Frozen MLLM w/ question-as-query. LoVi, VLong, and LVB denote the benchmarks LongVideoBench, VideoMME-Long, and LVBench, respectively*

![[assets/figures/papers/paper_list_l769_https_arxiv_org_abs_2602_22932/figures/009_Table_3.jpg]]
*Table 3: Ablation studies on the Informativeness Reward (IR) and Difficulty-aware Reward (DR) with a fixed input budget of 32 frames. LoVi, VLong, and LVB denote the benchmarks LongVideoBench, VideoMME-Long, and LVBench, respectively*

## 定位与知识库关联

### 关键帧采样方法的演进与 MSJoE 的定位

长视频理解中的帧选择策略可划分为三个代际。**第一代静态采样方法**以均匀采样为代表，按固定时间间隔抽取帧序列，完全不考虑问题语义。其优势在于实现简单、无需训练，但核心瓶颈在于密集均匀采样难以高效捕捉稀疏分布的关键事件，导致计算资源浪费且易遗漏对回答问题至关重要的短暂视觉线索。启发式关键帧方法如 **Q-Frame** 和 **BOLT** 尝试引入问题引导，利用 CLIP 相似度等信号进行 top-k 选择，但问题文本本身往往缺乏足够的视觉描述力，难以覆盖视频中多个分散的事件区域。

**第二代可训练采样器方法**以 **TSPO** 为代表，引入可学习参数来优化帧选择过程，但仍使用固定的问题文本作为查询，未能根据视频内容动态调整检索策略。MSJoE 在此基础上实现了关键突破，将问题分解为多个视觉导向的推理查询，使采样器能够从 CLIP 相似度矩阵中学习选择覆盖不同事件区域的关键帧。

**第三代联合进化框架**即 MSJoE 的核心创新：通过联合强化学习同时进化 MLLM 和轻量级 1D U-Net 采样器，使 MLLM 能够生成引导关键帧选择的推理查询，并适应稀疏关键帧分布。这一双向适应机制是 MSJoE 区别于所有先前工作的本质特征——消融实验（Table 2）明确证明，冻结 MLLM 或移除联合训练均会导致性能显著下降，验证了联合进化的必要性。

### 与通用长视频 MLLM 的关系

在通用长视频 MLLM 谱系中，**LongVU** 和 **NVILA** 通过改进的架构设计或训练策略提升长视频理解能力，**VideoMind-7B** 则引入推理机制增强时间理解。MSJoE 与这些工作的关系是互补而非替代：MSJoE 的核心贡献在于帧选择策略的优化，理论上可作为插件式模块与上述 MLLM 结合。实验结果显示，基于相同的基础 MLLM（Qwen2.5-VL-7B-Instruct），MSJoE 在四个长视频基准上平均提升 8.0 个百分点（64 帧），且在 32 帧预算下即可超越均匀采样的 64 帧性能（Figure 4），验证了关键帧选择相对于单纯增加帧数的效率优势。与闭源大型模型 **GPT-4o** 和 **Gemini-1.5-pro** 的对比进一步表明，通过智能帧选择，开源模型可在特定长视频任务上缩小与闭源模型的差距。

### 适用边界与局限

尽管 MSJoE 在多项选择问答（MQA）任务上展现了显著优势，其适用边界存在明确限制。**模态依赖性**方面，该方法重度依赖固定的 CLIP 视觉-语言对齐进行相似度计算，在 CLIP 训练数据覆盖不足的领域或低资源语言中可能泛化不足。**任务泛化性**方面，当前验证仅限于多项选择问答任务，对开放式视频问答、视频摘要生成或需要长时序因果推理的任务，其有效性尚未检验。**数据依赖性**方面，联合 RL 训练需要大量带难度标签的长期视频问答数据，收集和标注成本较高，限制了方法向新领域的快速迁移。**计算开销**方面，联合 RL 训练需保持多轨迹采样（GRPO 的组采样机制），增加了训练阶段的计算负担，尽管推理阶段的额外步骤（查询生成、相似度计算、采样器前向）因缓存机制而部分抵消（Table 4）。

### 开放问题与未来方向

MSJoE 框架开启了若干值得探索的研究方向。**多模态扩展**方面，当前框架仅利用视觉模态进行帧选择，能否将音频、字幕等模态纳入查询-帧匹配过程，以进一步增强对需要跨模态线索的长视频理解，是一个自然且具有应用价值的问题。**细粒度任务适配**方面，该框架能否适用于更细粒度的视频任务，例如时刻检索（moment retrieval）或时间动作定位（temporal action localization），需要重新设计奖励函数和采样目标。**时间动态建模**方面，CLIP 相似度矩阵本质上逐帧独立计算，是否能充分捕捉帧间的时间动态和事件演化关系，还是需要引入 3D 特征或显式的时间建模模块（如时序 Transformer），是提升采样质量的关键技术问题。**训练效率优化**方面，如何降低联合 RL 训练的计算开销，例如通过离线预训练轨迹复用或更高效的策略梯度估计方法，是推动该方法走向实际应用的重要工程挑战。

## 原文 PDF

![[paperPDFs/CVPR_2026/MSJoE_Jointly_Evolving_MLLM_and_Sampler_for_Efficient_Long_Form_Video_Understanding.pdf]]
