---
title: "Lance: Unified Multimodal Modeling by Multi-Task Synergy"
type: paper
paper_level: A
venue: arXiv
year: 2026
pdf_ref: "paperPDFs/arxiv_2026/Lance:_Unified_Multimodal_Modeling_by_Multi-Task_Synergy.pdf"
project_link: https://lance-project.github.io
code_link: https://github.com/bytedance/Lance
aliases:
- Lance
tags:
- arxiv_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
core_operator: 通过双流混合专家（MoE）架构将理解与生成的能力通路解耦，并结合模态感知旋转位置编码（MaPE）为异构视觉token分配明确的全局位置，从而缓解多任务间的干扰并提升跨任务对齐。
primary_logic: 多任务协同不仅是能力的简单叠加，更是一种促进跨模态-任务边界迁移的机制。通过共享的交错多模态序列实现统一上下文学习，同时保持理解与生成的解耦通路，可以在轻量级参数下高效平衡多模态理解与生成。
claims:
- Lance采用双流混合专家架构，在共享交错序列上联合建模，同时为理解和生成分配专用容量。
- 引入模态感知旋转位置编码（MaPE）缓解异构视觉token干扰，提升跨任务上下文对齐。
- Lance通过分阶段多任务训练范式与能力导向目标自适应数据调度，逐步增强语义理解与视觉生成。
- 删除MaPE后，生成、编辑和理解性能全面下降（如GEdit从6.86降至6.30）。
---

# Lance: Unified Multimodal Modeling by Multi-Task Synergy

> [!tip] 核心洞察
> 多任务协同不仅是能力的简单叠加，更是一种促进跨模态-任务边界迁移的机制。通过共享的交错多模态序列实现统一上下文学习，同时保持理解与生成的解耦通路，可以在轻量级参数下高效平衡多模态理解与生成。

| 字段      | 内容                                                                                                                                                               |
| ------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 中文题名    | Lance：通过多任务协同实现统一多模态建模                                                                                                                                           |
| 英文题名    | Lance: Unified Multimodal Modeling by Multi-Task Synergy                                                                                                         |
| 会议/期刊   | arXiv 2026                                                                                                                                                       |
| Links   | [paper](https://arxiv.org/abs/2605.18678) · [Project](https://lance-project.github.io) · [HuggingFace](https://huggingface.co/bytedance-research/Lance) · [Code](https://github.com/bytedance/Lance) |
| Topic   | #topic/vision_multimodal_applications #topic/generative_models_diffusion                                                                                         |
| Method  | Lance                                                                                                                                                            |
| Dataset | GenEval, DPG-Bench, VBench, GEdit-Bench                                                                                                                          |

> [!tip] 效果简介
> - GenEval 上，Overall score 0.90 vs Best among unified models (N/A)。
> - DPG-Bench 上，Overall 84.67 vs Best among unified models (N/A)。
> - VBench 上，Total Score 85.11 vs Best among unified models (N/A)。

## 概要

多模态模型的“统一”长期面临一个根本性张力：理解任务依赖高层语义抽象，而生成任务必须保留纹理、几何与运动等低层连续特征。现有统一模型大多仅覆盖文本-图像子集，或在单一共享骨干中强行融合两类需求，导致语义推理与生成质量难以兼得。

Lance 的核心主张是：**多任务协同不是能力的简单叠加，而是一种促进跨模态-任务边界迁移的机制**。为此，它做了一件此前统一模型未系统尝试的事——在共享交错多模态序列上实现统一上下文学习，同时通过双流混合专家（MoE）架构将理解与生成的能力通路解耦。理解专家（LLM_UND）负责自回归下一token预测，生成专家（LLM_GEN）负责流匹配速度预测，二者共享序列但分配专用容量。进一步引入的模态感知旋转位置编码（MaPE）为异构视觉token组分配明确的全局位置偏移，缓解了位置歧义对跨任务对齐的干扰。

在训练层面，Lance 采用四阶段多任务范式（预训练→持续训练→监督微调→强化学习），覆盖文本、图像、视频的理解与生成全任务族，并通过能力导向的数据调度逐步强化语义理解与视觉生成。这一设计使其在仅激活约3B参数的情况下，在图像生成（GenEval 0.90、DPG-Bench 84.67）、视频生成（VBench 85.11）、图像编辑（GEdit-Bench 7.30）和视频理解（MVBench 62.0）等基准上均显著超越现有开源统一模型。

消融实验进一步验证了关键设计：移除MaPE导致生成、编辑和理解性能全面下降（如GEdit从6.86降至6.30）；理解数据与多任务生成数据的合理混合（6:4）能带来最优的跨任务协同增益。



多模态大模型正处于从“单一任务专精”向“统一多任务协同”演进的关键节点。当前的主流范式呈现出两条清晰的路径：一是以扩散模型和流匹配为核心的专用生成模型，如**Stable Diffusion**、**FLUX**（Black Forest Labs, 2024）、**Sora**等，在图像/视频生成质量上不断刷新记录；二是以自回归语言模型为骨干的多模态理解模型，如**LLaVA**系列、**Qwen2.5-VL**等，在视觉问答、感知推理等任务上表现卓越。然而，这两类模型在架构设计、训练目标和表征需求上存在根本性分歧，导致“理解”与“生成”长期处于割裂状态。

### 核心瓶颈：视觉表征需求的根本性错位

现有统一多模态模型面临的核心瓶颈在于**视觉表征需求的根本性错位**。理解任务——包括视觉问答、图像描述、感知推理——天然依赖高层语义特征，这些特征需要经过充分的抽象和压缩，以捕捉场景的类别、关系和逻辑结构。而生成任务——包括文生图、文生视频、图像编辑——则必须保留低层的连续视觉细节，如纹理、几何结构、运动动态和时空一致性。将这两种需求强行塞入同一个视觉表征空间，必然导致语义推理能力与生成保真度之间的零和博弈。

### 现有统一模型的三个缺口

尽管近年来涌现了一批尝试统一多模态能力的模型，如**Chameleon**、**Emu3**、**Bagel**、**Show-o2**等原生统一模型，以及**InternVL-U**等非原生统一模型，但它们在三个关键维度上仍存在明显缺口：

1. **任务覆盖的系统性不足**：如Table 1所示，大多数统一模型仅覆盖文本-图像子集或部分任务类型。Chameleon和Emu3虽支持文本-图像生成和理解，但在视频生成、图像编辑、主题驱动生成等任务上缺乏显式支持。更少模型能同时覆盖X2T（任意模态到文本）、X2I（任意模态到图像）和X2V（任意模态到视频）三大任务族。

2. **架构层面的表征冲突**：现有统一模型通常采用单一共享骨干处理所有模态和任务，这意味着理解所需的高层语义特征和生成所需的低层连续特征必须在同一个参数空间中竞争容量。这种设计缺乏对两类任务根本性需求差异的架构级应对。

3. **多任务协同训练的缺失**：即使部分模型在推理时支持多任务，其训练过程往往缺乏系统性的多任务协同设计。理解数据能否促进生成质量？生成数据能否反向增强理解能力？不同任务间的数据混合比例如何影响跨任务迁移？这些问题在现有工作中缺乏系统的消融验证和机制分析。

### Lance的动机与核心思路

针对上述缺口，Lance提出了一条系统性的解决路径。其核心动机并非简单地“叠加”更多任务，而是探索**多任务协同是否能够成为一种促进跨模态-任务边界迁移的机制**——即通过精心设计的架构解耦和训练调度，让理解任务和生成任务在共享的上下文空间中相互增强，而非相互干扰。

这一动机在架构层面体现为**双流混合专家（MoE）设计**：Lance将骨干网络拆分为理解专家LLM_UND和生成专家LLM_GEN，两者共享交错多模态序列实现统一上下文学习，但各自拥有专用的参数容量。理解专家专注于自回归下一token预测，生成专家则专注于流匹配速度预测。这种“共享上下文、解耦通路”的设计，从根本上缓解了视觉表征需求的错位问题。

在位置编码层面，Lance进一步引入**模态感知旋转位置编码（MaPE）**，通过在时序维度上为异构视觉token组（如语义ViT token、干净VAE latent token、噪声VAE latent token）分配不同的位置偏移，显式区分其模态身份，减轻位置歧义对跨任务对齐的干扰。

在训练层面，Lance采用**四阶段多任务训练范式**（预训练PT→继续训练CT→监督微调SFT→强化学习RL），配合能力导向的目标函数和自适应数据调度，逐步构建从基础能力到高级协同的完整能力栈。



## 核心方法与创新机理

Lance的核心创新围绕一个根本性矛盾展开：多模态理解依赖高层语义表征，而视觉生成必须保留纹理、几何与时序的连续细节。现有统一模型通常采用单一骨干处理所有模态，导致两种需求在共享参数空间中相互干扰。Lance通过三个相互协同的机制设计——双流混合专家架构、模态感知旋转位置编码和分阶段多任务训练范式——将理解与生成的能力通路解耦，同时维持统一的上下文学习能力。

### 双流混合专家架构：解耦理解与生成的参数空间

Lance最关键的架构创新在于将传统统一模型的单一共享骨干替换为**双流混合专家（MoE）骨干**。具体而言，模型从Qwen2.5-VL初始化两个独立的专家网络：理解专家`LLM_UND`负责处理文本与语义视觉token，执行多模态推理与文本生成；生成专家`LLM_GEN`负责处理VAE latent token，执行流匹配生成。两者在**共享的交错多模态序列**上运行统一的3D因果注意力，但拥有独立的参数化路径。

这一设计直接改变了视觉表征的使用方式。与基线模型将统一视觉表征同时用于理解和生成不同，Lance保持语义ViT token与生成VAE latent token的**解耦**——它们被组织在同一个交错序列中，但分别路由到不同专家处理。序列结构由文本段、ViT语义token段、干净VAE latent段和噪声VAE latent段交替拼接而成，每类视觉段以`BOV`/`EOV`边界token包裹，文本段以`BOT`/`EOT`包裹：

$$\mathcal{S} = \cdots \oplus \mathcal{B}_{\mathrm{text}}(\mathbf{T}) \oplus \mathcal{B}_{\mathrm{vis}}(\mathbf{V}_{\mathrm{vit}}) \oplus \mathcal{B}_{\mathrm{vis}}(\mathbf{V}_{\mathrm{vae}}^{\mathrm{clean}}) \oplus \mathcal{B}_{\mathrm{vis}}(\mathbf{V}_{\mathrm{vae}}^{\mathrm{noisy}}) \oplus \mathcal{B}_{\mathrm{text}}(\mathbf{T}') \oplus \cdots$$

训练目标也相应分离：理解专家采用标准下一token预测损失$\mathcal{L}_{\mathrm{UND}}$，生成专家采用流匹配损失$\mathcal{L}_{\mathrm{GEN}}$，最终通过加权和$\mathcal{L} = \lambda_u \mathcal{L}_{\mathrm{UND}} + \lambda_g \mathcal{L}_{\mathrm{GEN}}$联合优化。这种解耦使得语义推理与视觉生成能在不互相牺牲的前提下各自获得专用容量，是Lance在生成质量上超越Chameleon、Emu3等原生统一模型的结构性原因。

### 模态感知旋转位置编码：消除异构视觉token的位置歧义

统一序列中同时存在ViT语义token、干净VAE latent和噪声VAE latent三种异构视觉token，它们在3D空间中的位置语义截然不同。标准3D-RoPE（如Qwen2.5-VL所采用）为所有视觉token分配统一的时空位置$\hat{\mathbf{p}}_{t,h,w}^{\mathrm{vis}} = D + [t, h, w]$，无法区分不同模态组的token，导致位置歧义和跨任务干扰。

Lance提出的**模态感知旋转位置编码（MaPE）**通过一个简洁的机制解决这一问题：为第$i$个模态token组在时序维度上添加固定的偏移量$i \cdot \Delta_t$：

$$\mathbf{p}_{t,h,w}^{(m_i)} = \hat{\mathbf{p}}_{t,h,w}^{(m_i)} + [i \cdot \Delta_t, 0, 0] = [\hat{t}_{t,h,w}^{(m_i)} + i \cdot \Delta_t, \hat{h}_{t,h,w}^{(m_i)}, \hat{w}_{t,h,w}^{(m_i)}]$$

这一设计使不同模态组的token在位置编码空间中自然分离，注意力机制能够隐式感知token的模态来源，从而减轻异构视觉信息之间的干扰。消融实验提供了直接证据：移除MaPE后，图像生成（GenEval）、图像编辑（GEdit从6.86降至6.30）、视频生成（VBench）和视频理解（MVBench）性能全面下降（Table 10），验证了模态感知位置编码对跨任务对齐的关键作用。

### 分阶段多任务训练与数据调度：从能力奠基到协同增强

Lance的训练范式从单阶段或任务覆盖不全的基线方案转变为**四阶段多任务训练**，每个阶段具有明确的能力导向目标：

- **预训练阶段（PT）**：冻结VAE/ViT编码器，训练双流骨干、QK-Norm及MLP连接器，建立基础图像/视频理解与生成能力。
- **持续训练阶段（CT）**：扩展任务空间，引入交错多任务数据与任务特定系统提示，促进跨任务迁移。
- **监督微调阶段（SFT）**：使用高质量精选数据优化指令跟随、视觉保真度和编辑精度。
- **强化学习阶段（RL）**：采用GRPO优化图像生成，提升文本渲染准确性和图文一致性。

这一分阶段策略的核心洞察在于**多任务协同不仅是能力的简单叠加，更是跨模态-任务边界的迁移机制**。消融实验（Table 9）揭示了协同效应的具体表现：添加理解数据能够提升图像生成性能（GenEval从81.65提升至82.06）和视频生成性能（VBench提升至83.05）；生成数据与多任务生成数据（编辑、主题驱动生成）以6:4比例混合时总体效果最佳。这表明理解任务的语义知识可以正向迁移到生成任务中，而多样化生成任务的联合训练进一步增强了模型的泛化能力。

### 创新点的系统协同

上述三个创新并非孤立设计，而是形成了系统性的协同关系：双流MoE提供了理解与生成解耦的**容量基础**，MaPE确保异构token在共享序列中的**位置无歧义**，分阶段多任务训练则通过数据调度最大化**跨任务迁移**。这种“解耦通路 + 统一上下文 + 协同训练”的组合策略，使得Lance仅以3B激活参数就在图像生成（GenEval 0.90、DPG-Bench 84.67）、视频生成（VBench 85.11）、图像编辑（GEdit-Bench 7.30）和视频理解（MVBench 62.0）等任务上全面超越现有开源统一模型。



Lance 的整体设计围绕一个核心矛盾展开：**多模态理解需要高层语义特征，而多模态生成需要保留纹理、几何与时序的低层连续特征**。为解决这一表征需求的根本性错位，Lance 采用“共享上下文 + 解耦通路”的架构策略——所有模态的 token 被组织进统一的交错序列以实现联合上下文学习，但理解与生成分别由独立的专家子网处理，从而避免任务间干扰。

### 统一多模态上下文序列

Lance 的输入序列 $\mathcal{S}$ 由文本段、ViT 语义视觉 token、干净 VAE latent token 和噪声 VAE latent token 交错拼接而成：

$$\mathcal{S} = \cdots \oplus \mathcal{B}_{\text{text}}(\mathbf{T}) \oplus \mathcal{B}_{\text{vis}}(\mathbf{V}_{\text{vit}}) \oplus \mathcal{B}_{\text{vis}}(\mathbf{V}_{\text{vae}}^{\text{clean}}) \oplus \mathcal{B}_{\text{vis}}(\mathbf{V}_{\text{vae}}^{\text{noisy}}) \oplus \mathcal{B}_{\text{text}}(\mathbf{T}') \oplus \cdots$$

每种模态段由起止边界 token 包裹，以显式标记模态边界：

$${\mathcal{B}}_{\text{text}}({\bf T}) = [{\tt BOT}, {\bf T}, {\tt EOT}], \quad {\mathcal{B}}_{\text{vis}}({\bf V}) = [{\tt BOV}, {\bf V}, {\tt EOV}]$$

这一设计的关键在于：**语义视觉 token（来自 ViT 编码器）与生成式 latent token（来自 VAE 编码器）在序列层面共享上下文，但在参数层面保持解耦**。文本 token 作为跨模态对齐的桥梁，同时参与理解与生成两条通路。

### 双流混合专家骨干

Lance 的骨干网络初始化为 Qwen2.5-VL，但被扩展为双专家架构：

- **理解专家 LLM_UND**：处理文本 token 与语义视觉 token（ViT），执行自回归下一 token 预测，负责多模态推理与文本生成。
- **生成专家 LLM_GEN**：处理 VAE latent token（干净/噪声），通过流匹配预测从噪声到干净隐变量的速度向量，负责图像/视频生成与编辑。

两个专家共享统一的 MaPE 增强上下文序列，通过广义 3D 因果注意力机制在共享序列上进行联合建模，但各自输出仅由对应专家解码——LLM_UND 的输出经 LM head 产生离散 token，LLM_GEN 的输出经 flow head 产生连续速度预测。

### 模态感知旋转位置编码（MaPE）

标准 3D-RoPE 为所有视觉 token 分配统一的时空位置，但 Lance 的序列中同时存在语义 ViT token 和生成式 VAE token，它们的空间语义不同，共享位置编码会导致位置歧义。MaPE 的核心操作是：**沿时序维度为不同模态 token 组施加固定偏移**：

$$\mathbf{p}_{t,h,w}^{(m_i)} = \hat{\mathbf{p}}_{t,h,w}^{(m_i)} + [i \cdot \Delta_t, 0, 0] = [\hat{t}_{t,h,w}^{(m_i)} + i \cdot \Delta_t, \hat{h}_{t,h,w}^{(m_i)}, \hat{w}_{t,h,w}^{(m_i)}]$$

其中 $\hat{\mathbf{p}}_{t,h,w}^{(m_i)}$ 是标准 3D-RoPE 分配的基准位置，$i$ 为模态组索引，$\Delta_t$ 为固定偏移步长。这使得不同模态组的 token 在位置空间中彼此分离，缓解了异构视觉 token 之间的干扰，同时保留了组内 token 的相对位置关系。消融实验（Table 10）表明，移除 MaPE 会导致生成、编辑和理解性能全面下降（如 GEdit 从 6.86 降至 6.30），验证了该设计的必要性。

### 整体信息流

1. **输入编码**：文本经 tokenizer 编码为离散 token；图像/视频经 ViT 编码为语义 token，经 VAE 编码为 latent token。
2. **序列构建**：所有 token 按任务需求组织成交错序列，并施加 MaPE 位置编码。
3. **双流前向**：统一序列经广义 3D 因果注意力后，理解与生成专家分别提取任务相关隐状态。
4. **任务解码**：理解任务输出经 LM head 解码为文本；生成任务输出经 flow head 预测速度向量，再通过 ODE 求解器恢复干净 latent，最终由 VAE decoder 重建为图像或视频。

### 训练目标

整体损失为理解损失与生成损失的加权和：

$$\mathcal{L} = \lambda_u \mathcal{L}_{\text{UND}} + \lambda_g \mathcal{L}_{\text{GEN}}$$

其中 $\mathcal{L}_{\text{UND}}$ 为标准下一 token 预测交叉熵损失，$\mathcal{L}_{\text{GEN}}$ 为流匹配损失，预测从噪声 $x_t$ 到干净隐变量 $x_1$ 的速度向量 $v_{\theta_{\text{GEN}}}(x_t, \mathcal{S}, t)$ 与真实速度 $(x_1 - x_0)$ 之间的 L2 距离。

> **注意**：$\lambda_u$ 和 $\lambda_g$ 的具体取值在提供的部分证据中未明确给出，需查阅完整论文的 Section 3.2 或训练配置部分进行确认。

### 补充图表

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2605_18678/figures/009_Figure_6.jpg]]
*Figure 6: Overview of Lance. Given multi-task inputs spanning X2T, X2I, and X2V, Lance encodes all input tokens into a unified MaPE-enhanced multimodal context sequence. The dual-expert backbone performs generalized 3D causal attention over the shared context and produces task-specific hidden states, which are further decoded by an LM head for autoregressive next-token prediction and by a flow head for velocity prediction in the visual latent space*

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2605_18678/figures/013_Figure_8.jpg]]
*Figure 8: System prompts for understanding tasks. Red placeholders denote user-provided text and visual inputs*

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2605_18678/figures/014_Figure_9.jpg]]
*Figure 9: System prompts for generation tasks. Red placeholders denote user-provided text and visual inputs*



Lance 的核心架构围绕三个关键设计展开：**统一多模态上下文序列**、**双流混合专家骨干**和**模态感知旋转位置编码**。以下逐一展开其公式化定义与变量含义。

### 统一多模态上下文序列

Lance 将异构输入组织为一条交错的统一序列 $\mathcal{S}$，其构造方式如式 (1) 所示：

$$\mathcal{S} = \cdots \oplus \mathcal{B}_{\mathrm{text}}(\mathbf{T}) \oplus \mathcal{B}_{\mathrm{vis}}(\mathbf{V}_{\mathrm{vit}}) \oplus \mathcal{B}_{\mathrm{vis}}(\mathbf{V}_{\mathrm{vae}}^{\mathrm{clean}}) \oplus \mathcal{B}_{\mathrm{vis}}(\mathbf{V}_{\mathrm{vae}}^{\mathrm{noisy}}) \oplus \mathcal{B}_{\mathrm{text}}(\mathbf{T}') \oplus \cdots$$

其中，$\mathbf{T}$ 为文本 token，$\mathbf{V}_{\mathrm{vit}}$ 为语义 ViT token，$\mathbf{V}_{\mathrm{vae}}^{\mathrm{clean}}$ 与 $\mathbf{V}_{\mathrm{vae}}^{\mathrm{noisy}}$ 分别为干净的 VAE 隐变量 token 和加噪后的 VAE 隐变量 token。每个模态段由特定的边界 token 包裹，如式 (2) 所示：

$${\mathcal{B}}_{\mathrm{text}}({\bf T}) = [{\tt BOT}, {\bf T}, {\tt EOT}], \quad {\mathcal{B}}_{\mathrm{vis}}({\bf V}) = [{\tt BOV}, {\bf V}, {\tt EOV}]$$

其中 BOT/EOT 标记文本段的起止，BOV/EOV 标记视觉段的起止。这一设计使得语义 token 与生成 latent token 在序列层面解耦，同时共享统一的上下文学习空间。

### 双流专家损失函数

Lance 采用双流混合专家骨干，理解专家 LLM_UND 处理语义推理任务，生成专家 LLM_GEN 处理视觉生成任务。二者共享上述统一序列，但参数化路径独立。

**理解损失**为标准自回归下一 token 预测的交叉熵：

$$\mathcal{L}_{\mathrm{UND}} = -\sum_i \log p_{\theta_{\mathrm{UND}}}(y_i \mid y_{<i}, \mathcal{S})$$

其中 $\theta_{\mathrm{UND}}$ 为理解专家参数，$y_i$ 为目标文本 token，$\mathcal{S}$ 为统一上下文序列。

**生成损失**采用流匹配目标，预测从噪声 $x_0$ 到干净隐变量 $x_1$ 的速度场：

$$\mathcal{L}_{\mathrm{GEN}} = \mathbb{E}_{x_0,x_1,t}\left[\left\| v_{\theta_{\mathrm{GEN}}}(x_t, \mathcal{S}, t) - (x_1 - x_0) \right\|_2^2 \right]$$

其中 $x_t = t x_1 + (1-t) x_0$ 为时间 $t$ 处的插值隐变量，$v_{\theta_{\mathrm{GEN}}}$ 为生成专家的速度预测网络，$(x_1 - x_0)$ 为真实速度方向。

**总体目标**为二者的加权和：

$$\mathcal{L} = \lambda_u \mathcal{L}_{\mathrm{UND}} + \lambda_g \mathcal{L}_{\mathrm{GEN}}$$

其中 $\lambda_u$ 和 $\lambda_g$ 为平衡系数。

### 模态感知旋转位置编码（MaPE）

Qwen2.5-VL 的标准 3D-RoPE 为视觉 token 分配统一的时空位置，如式 (6) 所示：

$$\hat{\mathbf{p}}_{t,h,w}^{\mathrm{vis}} = D + [t, h, w] = [D+t, D+h, D+w]$$

其中 $D$ 为文本序列长度偏移，$t, h, w$ 分别为时序、高度、宽度维度索引。然而，当序列中同时存在 ViT token 和 VAE latent token 等多组异构视觉 token 时，这种统一的位置分配会导致位置歧义——不同模态组的 token 可能被分配到相同的位置坐标。

MaPE 通过在时序维度上为每个模态组 $m_i$ 引入固定偏移来解决这一问题，如式 (7) 所示：

$$\mathbf{p}_{t,h,w}^{(m_i)} = \hat{\mathbf{p}}_{t,h,w}^{(m_i)} + [i \cdot \Delta_t, 0, 0] = [\hat{t}_{t,h,w}^{(m_i)} + i \cdot \Delta_t, \hat{h}_{t,h,w}^{(m_i)}, \hat{w}_{t,h,w}^{(m_i)}]$$

其中 $i$ 为模态组索引，$\Delta_t$ 为预定义的时序偏移步长。这一设计使得不同模态组的 token 在位置空间中彼此分离，从而缓解异构视觉 token 之间的干扰，提升跨任务上下文对齐。消融实验证实，移除 MaPE 会导致生成、编辑和理解性能全面下降（如 GEdit 从 6.86 降至 6.30，见 Table 10）。



## 实验与关键发现

### 主实验结果

Lance在图像生成、视频生成、图像编辑和视频理解四个核心任务族上均取得了统一模型中的领先性能，部分指标甚至超越专用模型。

**图像生成。** 在GenEval和DPG-Bench两个基准上，Lance分别达到0.90和84.67的总体得分，在所有统一模型中排名第一（Table 5）。值得注意的是，Lance在GenEval上超越了多个使用LLM改写器的专用方法（以†标注），表明其原生文本-图像对齐能力已达到强基线水平。

**视频生成。** 在VBench上，Lance以85.11的总分显著领先于所有统一模型（Table 6）。这一优势在需要时序一致性和动态自然度的子维度上尤为突出，验证了双流MoE架构对视频隐空间token的有效建模。

**图像编辑。** 在GEdit-Bench上，Lance取得7.30的平均得分（Table 7），在统一模型中表现最佳。该基准综合评估编辑精度、纹理保持和结构一致性，Lance的高分表明其共享交错序列设计能够有效保留源图像信息的同时执行精确修改。

**视频理解。** 在MVBench上，Lance达到62.0的平均准确率（Table 8），在统一模型中同样排名第一。这证明理解专家LLM_UND在承担生成任务负载的同时，并未牺牲语义推理能力。

### 消融实验

#### 跨任务数据协同效应

Table 9揭示了多任务训练中数据混合的关键规律：

- **理解数据促进生成。** 在基础生成数据之上添加理解数据，使GenEval从81.65提升至82.06，VBench提升至83.05。这表明高层语义理解能力通过共享序列向生成通路正向迁移。
- **多任务生成数据的最佳配比。** 将编辑、主题驱动生成等多任务生成数据与基础生成数据以6:4混合时，总体效果最优。过高比例的多任务数据会稀释基础生成能力，过低则无法充分激发跨任务泛化。
- **数据混合存在任务间权衡。** 不同混合比例对图像生成和视频生成的影响并非完全同步，需要在具体应用场景下进行微调。

#### 模态感知位置编码（MaPE）的关键作用

Table 10的消融结果直接验证了MaPE的设计必要性：

- 移除MaPE后，所有任务性能一致下降：图像生成（GenEval）、图像编辑（GEdit从6.86降至6.30）、视频生成（VBench）和视频理解（MVBench）均出现明显退化。
- 编辑任务对MaPE最为敏感，降幅达0.56点，说明异构视觉token（语义ViT token与VAE latent token）之间的位置歧义在需要精确空间对齐的编辑场景中危害最大。
- 这一结果从反面证实了MaPE通过时序维度偏移区分不同模态token组的有效性。

#### 训练可扩展性

Figure 13展示了图像和视频生成性能随训练token数增长的扩展曲线。两个任务在预训练早期（约0.5T tokens前）均呈现快速提升，随后增长速度减缓但未出现饱和迹象，表明Lance架构具备良好的可扩展性。Figure 14的定性对比进一步印证了这一趋势：随着训练预算从0.5T增加到1.5T，生成图像的细节丰富度和视频的运动自然度均逐步改善。

### 失败模式与局限性

论文明确指出，**文字特定的编辑（text-specific editing）** 仍是Lance需要改进的重要方向。这主要指在图像中精确渲染、修改或擦除文字内容的场景，可能源于VAE latent空间对细粒度字形信息的压缩损失，以及当前训练数据中此类任务的覆盖不足。此外，尽管Lance在统一模型中表现领先，但与专用生成模型（如Flux）在极端复杂提示下的图像生成质量仍有差距，这需要更大规模的生成专项训练来弥补。

### 关键图表结论汇总

- **Table 1**：Lance是当前任务覆盖最全面的原生统一模型，同时支持图像/视频的理解、生成与编辑。
- **Table 5-8**：Lance在四个核心基准上均取得统一模型最优，验证了双流MoE架构与多任务协同训练的有效性。
- **Table 9**：理解数据与多任务生成数据的适当混合可产生正向跨任务迁移，最佳配比约为6:4。
- **Table 10**：MaPE是Lance的关键组件，移除后所有任务性能一致下降，编辑任务受影响最大。
- **Figure 13**：Lance的图像和视频生成性能随训练规模持续提升，未出现明显瓶颈。

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2605_18678/figures/003_Table_1.jpg]]
*Table 1: Comparison of multimodal unified models by supported task categories. ✓ indicates explicit support; △ indicates description-only support without official code; blank cells indicate no explicit report. Cap., Per., Rea. indicate understanding ability on captioning, perception, and reasoning. The last column denotes whether the model exhibits emergent generalization on unseen tasks. Models are categorized as native or non-native unified models based on whether they are jointly pre-trained as a unified architecture or assembled from separately pre-trained components*

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2605_18678/figures/015_Table_5.jpg]]
*Table 5: Image generation results on DPG-Bench and GenEval. † refers to methods using LLM rewriters in GenEval. Bold: best results among unified models. Underline: second-best among unified models*

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2605_18678/figures/034_Table_10.jpg]]
*Table 10: Ablation on Modality-Aware Rotary Positional Encoding (MaPE). We report GenEval for image generation, GEdit for image editing, VBench for video generation, and MVBench for video understanding*

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2605_18678/figures/029_Figure_13.jpg]]
*Figure 13: Scaling behavior of image and video generation performance with increasing training tokens. We report DPG-Bench for image generation and VBench for video generation across different training token budgets*

### 补充图表

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2605_18678/figures/018_Table_6.jpg]]
*Table 6: Video generation results on VBench. † refers to methods using LLM rewriters. Bold: best results among unified models. Underline: second-best among unified models*

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2605_18678/figures/024_Table_7.jpg]]
*Table 7: Image editing results on GEdit-Bench. Bold: best results among unified models. Underline: second-best among unified models*

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2605_18678/figures/025_Table_8.jpg]]
*Table 8: Video understanding results on MVBench. Bold: best results among unified models. Underline: second-best among unified models*

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2605_18678/figures/017_Figure_10.jpg]]
*Figure 10: T2I qualitative comparison. Instructions that are correctly reflected in our results but missed or incorrectly rendered by some baseline models are highlighted in red*

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2605_18678/figures/023_Figure_11.jpg]]
*Figure 11: T2V qualitative comparison. Instructions that are correctly reflected in our results but missed or incorrectly rendered by some baseline models are highlighted in red*



## 定位与知识库关联

### 统一多模态模型谱系中的定位

Lance 将自己定位为 **原生统一多模态模型**（native unified model），即从预训练阶段就以统一架构联合建模，而非将分别预训练的组件组装在一起。Table 1 将现有统一模型分为两类：原生模型（如 **Chameleon**、**Emu3**、**Bagel**、**Show-o2**）与非原生模型（如 **InternVL-U**，其采用组装式架构）。Lance 在这张功能矩阵中覆盖了最完整的任务空间：文本理解与推理、图像/视频理解、文本到图像生成、文本到视频生成、图像/视频编辑，以及主题驱动生成，且所有任务均有显式支持（✓），而非仅描述性提及（△）。

与现有原生统一模型的根本差异在于架构选择。Chameleon、Emu3 等采用单一共享骨干处理所有模态和任务，这导致理解与生成对视觉表征的需求冲突——理解依赖高层语义，生成需要保留纹理、几何和时序的低层连续特征——在共享参数空间中难以同时满足。Lance 通过双流混合专家（MoE）架构将这一冲突显式化解：理解专家 LLM_UND 处理文本和语义 ViT token，生成专家 LLM_GEN 处理 VAE latent token，两者共享交错多模态序列但拥有独立的参数化通路。这种设计使模型能以仅 3B 激活参数在理解和生成任务间取得平衡。

### 方法谱系中的关键设计选择

**视觉表征的解耦策略**构成了 Lance 区别于同类工作的核心支点。大多数统一模型试图用单一视觉表征服务所有任务，而 Lance 保持语义 ViT token 与生成 VAE latent token 的解耦，仅在统一上下文序列层面组织它们。这一设计受以下观察驱动：语义 token 需捕获全局上下文以支持推理，而 latent token 需保留局部细节以支持高质量生成。解耦后，两类 token 通过共享的交错序列实现跨任务上下文学习，但分别路由到不同专家处理，避免了表征层面的相互干扰。

**模态感知旋转位置编码（MaPE）** 是另一个差异化设计。标准 3D-RoPE（如 Qwen2.5-VL 所用）为所有视觉 token 分配统一的时空位置，但当同一序列中混杂 ViT token、干净 VAE token 和噪声 VAE token 时，这些异构 token 组之间会产生位置歧义——模型无法从位置编码中区分 token 的模态来源。MaPE 通过为每个模态组在时序维度上添加固定偏移量 $i \cdot \Delta_t$，使不同组的 token 占据互不重叠的位置区间，从而在保持 3D 位置信息的同时注入模态感知。消融实验（Table 10）证实了这一设计的因果效应：移除 MaPE 后，图像生成（GenEval）、图像编辑（GEdit）、视频生成（VBench）和视频理解（MVBench）性能全面下降，其中 GEdit 从 6.86 降至 6.30。

**分阶段多任务训练范式**（PT→CT→SFT→RL）使 Lance 能够渐进式地扩展能力边界。预训练阶段（PT）建立基础理解与生成能力，冻结 VAE/ViT 编码器，训练骨干网络和连接器；持续训练阶段（CT）引入交错多任务数据与任务特定系统提示，促进跨任务迁移；监督微调阶段（SFT）使用高质量精选数据优化指令跟随和视觉保真度；强化学习阶段（RL）采用 GRPO 优化图像生成，提升文本渲染准确性和图文一致性。这一范式与单阶段训练的统一模型形成对比，后者往往难以在任务间取得平衡。

### 适用边界与局限

Lance 的设计在当前任务空间内表现出色，但存在明确的适用边界。论文明确指出，**文字特定的编辑**（text-specific editing）仍然是需要改进的重要方向，这表明模型在精确操控图像中文字内容的能力上存在不足。这一局限可能源于 VAE latent 空间对文字细节的表征能力有限，或训练数据中文字编辑样本的覆盖不足。

从架构角度看，双流 MoE 的解耦策略虽然有效，但引入了额外的参数和路由开销。与单一骨干的统一模型相比，Lance 需要在推理时同时维护两个专家路径，这可能增加显存占用和推理延迟。论文未提供与同参数规模单一骨干模型的效率对比，这一点需要读者自行评估。

此外，Lance 的训练数据混合调度（Table 3）显示视频生成数据占比最高（全局比例 64%），这可能使模型在视频生成任务上获得更强表现，但也意味着其他任务（如图像理解仅占 4%）可能在数据覆盖上相对不足。跨任务数据消融（Table 9）表明理解数据确实能提升生成性能，但最优混合比例可能因任务而异，当前调度是否普适仍需验证。

### 开放问题

MaPE 的消融实验证实了其有效性，但其作用机制仍有深入空间。具体而言，MaPE 如何具体减少异构视觉 token 组之间的位置歧义？偏移量 $\Delta_t$ 的选择是否存在最优值？不同模态组之间的偏移间隔是否影响跨任务对齐的质量？这些问题在论文中未得到充分探讨。

更广泛的开放问题是：多任务协同的收益是否可推广到当前任务空间之外？Lance 目前覆盖文本、图像、视频三种模态的理解与生成，但未涉及音频、3D、代码等模态。如果将这些模态纳入统一序列，现有的双流架构和 MaPE 设计是否仍能有效运作？跨模态协同的收益是否会随模态数量增加而递减或饱和？这需要后续工作在更丰富的模态组合上进行验证。

最后，Lance 的训练扩展性曲线（Figure 13）显示图像和视频生成性能在预训练早期快速提升后增速减缓，但论文未报告理解任务的扩展行为。理解与生成是否遵循相同的扩展规律？在更大训练预算下，双流架构是否会遇到某一通路的瓶颈？这些问题的答案将决定 Lance 架构范式的长期可扩展性。



## 原文 PDF

![[paperPDFs/arxiv_2026/Lance:_Unified_Multimodal_Modeling_by_Multi-Task_Synergy.pdf]]
