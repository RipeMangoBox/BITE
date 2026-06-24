---
title: "GrOCE : Graph-Guided Online Concept Erasure for Text-to-Image Diffusion Models"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/GrOCE_Graph_Guided_Online_Concept_Erasure_for_Text_to_Image_Diffusion_Models.pdf
project_link: null
code_link: null
aliases:
- GrOCE
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 通过构建动态语义图来显式建模概念间的相似性、层次关联和共现模式，将概念擦除转化为图上的连通性切断问题，从而精准抑制目标簇对文本提示的影响。
primary_logic: 在语义图上通过扩散过程识别与目标概念紧密纠缠的节点簇，仅移除这些簇在文本嵌入上的投影分量，即可实现上下文感知的精确擦除，同时保留全局句子结构和不相关语义。
claims:
- 在单/多/风格概念擦除任务上，GrOCE均取得最低的概念相似度（CS）和完美的非目标FID（0），验证了精准擦除与极致保留。
- 移除IDENTIFY模块后，虽然目标CS略降至14.51，但非目标FID暴增至426.74，证明该模块有效防止了过度擦除和不相关内容的损坏。
- GrOCE的图结构直接揭示了文本Token与视觉特征之间的固有关联，使切断操作可以精确针对目标概念，无需训练或手工设定阈值。
- 在高并发（10个概念）擦除场景下，GrOCE仅需1.73秒，比训练方法快一个数量级，使在线大规模概念清理成为可能。
---

# GrOCE : Graph-Guided Online Concept Erasure for Text-to-Image Diffusion Models

> [!tip] 核心洞察
> 在语义图上通过扩散过程识别与目标概念紧密纠缠的节点簇，仅移除这些簇在文本嵌入上的投影分量，即可实现上下文感知的精确擦除，同时保留全局句子结构和不相关语义。

| 字段 | 内容 |
|------|------|
| 中文题名 | GrOCE：面向文生图扩散模型的图引导在线概念擦除 |
| 英文题名 | GrOCE : Graph-Guided Online Concept Erasure for Text-to-Image Diffusion Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Han_GrOCE__Graph-Guided_Online_Concept_Erasure_for_Text-to-Image_Diffusion_Models_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | GrOCE |
| Dataset | Single-concept erasure, Dual-concept erasure (Snoopy) – Snoopy CS, Dual-concept erasure (Mickey) – Mickey CS, Triple-concept erasure (Spongebob) – Spongebob CS |

> [!tip] 效果简介
> - Single-concept erasure (Snoopy) 上，CS 16.92 (Lowest CS among compared methods)；FID 0 (FID=0, perfect preservation of non-target concepts)。
> - Dual-concept erasure (Snoopy) – Snoopy CS 上，CS 16.92 (Lowest CS)。
> - Dual-concept erasure (Mickey) – Mickey CS 上，CS 18.37 (Lowest CS)。

## 概述

文生图扩散模型虽然能根据文本描述生成高质量图像，但也带来了生成侵权、有害或不适宜内容的风险。概念擦除（concept erasure）旨在从模型中移除特定概念的生成能力，但现有方法面临两个核心瓶颈：**需要模型微调**，部署成本高且难以应对动态变化的概念集合；**将概念视为孤立实体**，采用粗粒度的语义分离，忽略了概念之间复杂的语义拓扑关系，导致擦除目标时损害邻近概念。

GrOCE 提出了一种**图引导的在线概念擦除**范式，将概念擦除转化为推理时的语义图连通性切断问题。其核心洞察是：通过在文本嵌入空间构建动态语义图，显式建模概念间的相似性、层次关联和共现模式，利用扩散过程识别与目标概念紧密纠缠的节点簇，仅移除这些簇在提示嵌入上的投影分量，即可实现上下文感知的精确擦除，同时保留全局句子结构和不相关语义。

GrOCE 由三个协同组件构成：**CONSTRUCT** 动态构建加权语义图，**IDENTIFY** 自适应识别目标概念簇，**SEVER** 选择性切断目标语义影响。该方法完全免训练，在 Stable Diffusion v1.4、SDXL 和 FLUX 三种架构上均展现出即插即用的通用性。

在单概念、多概念及艺术风格擦除任务上，GrOCE 均取得最低的概念相似度（CS），且非目标概念的 FID 保持为 0，实现了精准擦除与极致保留的平衡。消融实验表明，IDENTIFY 模块是防止过度擦除的关键——移除后非目标 FID 从 0 骤升至 426.74。在效率方面，GrOCE 擦除 10 个概念仅需 1.73 秒，比训练方法快一个数量级，使在线大规模概念清理成为可能。

## 背景与动机

文本到图像（T2I）扩散模型的快速发展使高质量图像生成变得触手可及，但同时也带来了生成不安全、侵权或不当内容的隐患。概念擦除（concept erasure）作为一种关键的缓解策略，旨在从生成过程中移除特定概念（如受版权保护的卡通形象、特定艺术风格或敏感视觉元素），同时尽可能保留模型的其余生成能力。然而，当前的主流方法面临两个核心瓶颈。

**现有方法的缺口**。一方面，以 **ESD**（Gandikota et al., ICCV 2023）、**UCE**（Gandikota et al., WACV 2024）、**CA**（Kumari et al., ICCV 2023）、**SPM**（Lyu et al., CVPR 2024）和 **MACE**（Lu et al., CVPR 2024）为代表的方法依赖模型微调或权重修改，不仅计算代价高昂，且难以灵活适应动态变化的概念擦除需求。近期出现的训练自由方法如 **SPEED**（Li et al., ICLR 2026）和 **AdaVD**（Wang et al., CVPR 2025），虽在推理效率上有所突破，却仍将概念视为语义空间中的孤立实体，采用粗粒度的语义分离策略，忽略了概念之间固有的语义拓扑关系。

**语义纠缠的挑战**。扩散模型的文本嵌入空间中，概念并非独立分布，而是通过相似性、层次关联和共现模式形成复杂的语义结构。直接抑制目标概念往往会不可避免地波及与其语义相邻的非目标概念——例如，擦除“Snoopy”时可能损害“卡通狗”或“漫画风格”等邻近概念，导致生成质量下降或非目标内容意外丢失。这种“误伤”源于现有方法缺乏对概念间语义依赖关系的显式建模能力。

**在线适应性的缺失**。实际部署中，需要擦除的概念集合往往是动态演化的——新的不当概念持续涌现，旧概念的威胁评估也可能随时变化。基于微调的方法每次更新都需要重新训练，难以实现实时响应；而现有的训练自由方法则依赖固定的概念列表，无法在线增量处理新增概念。如 Figure 1(b) 所示，GrOCE 在 10 概念并发擦除场景下仅需 1.73 秒，比基于训练的 ConAbl 等方法快一个数量级，凸显了在线大规模概念清理的实用价值。

**本文动机**。针对上述缺口，GrOCE 提出了一种根本性的思路转变：将概念擦除重新定义为语义图上的连通性切断问题。通过动态构建概念间的语义图，显式捕获相似性、层次和共现关系，再借助图上的扩散过程精准识别与目标概念紧密纠缠的节点簇，最终仅移除这些簇在文本提示嵌入上的投影分量。这一范式实现了上下文感知的精确擦除，既能在语义层面精准打击目标，又能最大限度地保留全局句子结构和不相关语义——如 Figure 1(a) 所示，在抑制目标概念的同时，其语义邻近的非目标概念得以完好保留。

## 核心创新

GrOCE 的核心创新在于将概念擦除从“参数修改”或“孤立语义抑制”转变为**图引导的在线语义切断**。与现有方法相比，GrOCE 在四个关键维度上实现了根本性的突破。

### 1. 从模型修改到推理时语义操作

现有主流方法普遍依赖模型微调或权重优化来实现概念擦除：**ESD** (Gandikota et al., ICCV 2023)、**UCE** (Gandikota et al., WACV 2024) 和 **CA** (Kumari et al., ICCV 2023) 需要针对每个目标概念进行参数更新；**SPM** (Lyu et al., CVPR 2024) 和 **MACE** (Lu et al., CVPR 2024) 虽然效率有所提升，但仍需训练适配器或进行多步优化。即使是最新的训练自由方法 **AdaVD** (Wang et al., CVPR 2025) 和 **SPEED** (Li et al., ICLR 2026)，也主要在值空间或注意力层进行修改，缺乏对语义结构的显式建模。

GrOCE 完全摒弃了训练环节，将擦除操作上移至**文本嵌入层**，通过选择性过滤提示中的 Token 来实现概念抑制。这一设计不仅消除了模型修改的成本和风险，还使得擦除过程可以在推理时动态执行，无需任何预计算或离线准备。

### 2. 从孤立概念到语义拓扑感知

现有方法将待擦除概念视为独立实体，忽略了概念之间复杂的语义关系。这种“粗略语义分离”策略的致命缺陷在于：当目标概念与邻近概念在语义空间中高度纠缠时，抑制目标会不可避免地损害邻近概念。

GrOCE 通过**动态语义图**显式建模概念间的相似性、层次关联和共现模式。图中的节点为词汇嵌入，边权重由余弦相似度和局部自适应阈值共同决定：

$$w_{ij} = \begin{cases} \exp\left(-\frac{\tau_i - \langle x_i, x_j \rangle}{\sigma}\right), & \text{if } \langle x_i, x_j \rangle > \tau_i; \\ 0, & \text{otherwise}. \end{cases}$$

这种图结构直接揭示了文本 Token 与视觉特征之间的固有关联（见 Section 5.2 定性分析），使擦除操作可以精确针对目标概念簇，而非盲目抑制单个节点。

### 3. 从手工阈值到自适应簇识别

传统方法通常依赖手工设定的阈值或固定的概念列表来决定擦除范围。GrOCE 的 **IDENTIFY** 模块通过锚点初始化、语义扩散和 Top-K 选择，自动识别与目标概念紧密纠缠的概念簇：

$$s = \exp(-\varphi \mathcal{L}_{sub}) Y$$

该扩散过程在局部子图上模拟信息传播，从目标概念节点出发，沿加权边扩散至相邻节点，量化每个节点与目标概念的语义关联强度。随后通过 Top-K 选择提取影响最大的节点，形成精确的擦除簇。这一过程无需任何手工调参或领域知识。

### 4. 从静态概念集到在线增量适应

现有方法依赖固定的概念列表，难以应对动态出现的新增概念。当需要擦除新概念时，基于训练的方法必须重新微调模型，耗时巨大。

GrOCE 支持**在线增量图构建**：新概念可以即时添加为图节点，仅需计算其与现有节点的边权重即可完成图更新。在高并发场景下（10个概念同时擦除），GrOCE 仅需 **1.73 秒**，比训练方法快一个数量级（Table 4），使在线大规模概念清理成为可能。

### 决定性证据

消融实验（Table 3）为 GrOCE 的核心创新提供了强有力的因果验证：移除 IDENTIFY 模块后，虽然目标概念相似度（CS）仅从 16.92 略微降至 14.51，但非目标 FID 从完美的 0 暴增至 **426.74**。这一巨大反差证明，IDENTIFY 模块的自适应簇识别能力是防止过度擦除和保留非目标语义的关键机制——这正是 GrOCE 区别于所有现有方法的核心优势。

## 整体框架

GrOCE 提出了一种**完全无训练、纯推理时**的概念擦除框架，其核心思想是将概念擦除转化为在**动态语义图**上识别并切断目标概念簇对文本提示影响的过程。如图2所示，整个pipeline由三个协同组件构成：**CONSTRUCT（动态语义图构建）**、**IDENTIFY（自适应目标簇识别）** 和 **SEVER（选择性语义切断）**。

### Pipeline 总览

给定一个文本提示 $t$ 和一个指定的目标概念 $c_t$（例如 “bear”），GrOCE 按以下流程执行推理时概念擦除：

1. **语义图构建**：CONSTRUCT 模块以词汇表中的概念为节点，基于 CLIP 文本编码器提取的嵌入向量计算节点间的余弦相似度，动态构建一个加权语义图 $\mathcal{G} = (\mathcal{V}, \mathcal{E})$。边的权重通过指数衰减函数定义，仅当两节点相似度超过局部自适应阈值 $\tau_i$ 时才建立连接（见公式 (2)-(4)）。该图支持增量更新，可适应演化中的概念集合。
2. **目标簇识别**：IDENTIFY 模块以目标概念节点为锚点，在局部 $n$ 跳子图上模拟语义扩散过程（公式 (5)-(7)），计算每个节点受目标概念影响的扩散分数，并通过 Top-$K$ 选择提取与目标概念**语义紧密纠缠的概念簇** $\mathcal{V}_c$。
3. **选择性切断**：SEVER 模块遍历提示中的每个 Token 嵌入 $t_i$，计算目标簇 $\mathcal{V}_c$ 中所有节点对其的加权投影贡献 $\alpha_i$（公式 (8)），并仅保留那些投影总范数 $\|\alpha_i\|$ 低于阈值 $\delta$ 的 Token（公式 (9)），从而在文本嵌入层精确抑制目标概念的影响，同时保留全局句子结构和不相关语义。

修改后的提示 $t'$ 被重新编码后送入扩散模型生成图像，整个过程无需修改模型权重或进行任何优化。

### 模块间关系与数据流

三个组件之间存在严格的**串行依赖与功能分工**：

- **CONSTRUCT → IDENTIFY**：CONSTRUCT 输出的语义图 $\mathcal{G}$ 是 IDENTIFY 执行语义扩散和簇提取的空间基础。图的边权重直接决定了扩散过程中概念间影响传播的强度与范围。
- **IDENTIFY → SEVER**：IDENTIFY 输出的目标概念簇 $\mathcal{V}_c$ 定义了 SEVER 需要抑制的语义子空间。若跳过 IDENTIFY 直接执行 SEVER，消融实验（Table 3）表明：虽然目标概念相似度（CS）仅从 16.92 微降至 14.51，但非目标 FID 从 0 暴增至 426.74，证明 IDENTIFY 在**防止过度擦除和保护非目标语义**方面不可或缺。
- **SEVER → 扩散生成**：SEVER 输出的过滤后提示 $t'$ 直接替代原始提示进入扩散模型的文本编码与去噪流程，完成最终的图像生成。

### 输入输出规范

| 阶段 | 输入 | 输出 |
|------|------|------|
| CONSTRUCT | 词汇表概念嵌入 $\{x_i\}$ | 加权语义图 $\mathcal{G}$ |
| IDENTIFY | 语义图 $\mathcal{G}$，目标概念 $c_t$ | 目标概念簇 $\mathcal{V}_c$ |
| SEVER | 提示 Token 嵌入 $\{t_i\}$，目标簇 $\mathcal{V}_c$ | 过滤后提示 $t'$ |

### 关键设计理念

与现有方法将概念视为孤立实体不同，GrOCE 通过语义图**显式建模概念间的相似性、层次关联和共现模式**。图结构直接揭示了文本 Token 与视觉特征之间的固有关联（Section 5.2 定性分析），使得切断操作可以精确针对目标概念，无需训练或手工设定阈值。这一设计同时赋予了框架**在线适应性**：当新概念出现时，仅需在图中增量添加节点并更新相关边权重，即可动态扩展擦除能力。在高并发场景（10 个概念同时擦除）下，GrOCE 仅需 1.73 秒（Table 4），比训练方法快一个数量级，使在线大规模概念清理成为可能。

### 补充图表

![[assets/figures/papers/paper_list_l2315_https_openaccess_thecvf_com_content_CVPR2026_html_Han_GrOCE_Graph_Guided/figures/002_Figure_2.jpg]]
*Figure 2: The GrOCE pipeline for online concept erasure. Given a text prompt and a specified target concept (e.g., “bear”), GrOCE performs inference-time concept erasure through three synergistic components: (1) Dynamic Semantic Graph Construction builds a semantic graph with vocabulary tokens as nodes and cosine-weighted edges, supporting incremental updates for evolving concept sets.(2) Adaptive Cluster Identification performs multi-hop traversal with similarity decay to identify semantically entangled concepts (e.g., “grizzly,” “panda”) around the target. (3) Selective Severing removes the semantic components associated with the identified cluster, editing the text prompt prior to diffusion to sup...*

## 核心模块与公式推导

GrOCE 是一种**完全无训练**的推理时概念擦除框架，将概念擦除建模为在动态语义图上执行的在线推理过程。其核心由三个协同组件构成：**CONSTRUCT**（动态语义图构建）、**IDENTIFY**（自适应目标簇识别）和 **SEVER**（选择性语义切断），整体流程如 Figure 2 所示。

### 4.1 CONSTRUCT：动态语义图构建

给定文本提示，首先通过 CLIP 文本编码器获取词汇表中所有 Token 的上下文嵌入。CONSTRUCT 模块基于这些嵌入构建一个加权无向图 $\mathcal{G} = (\mathcal{V}, \mathcal{E})$，其中节点为概念嵌入，边权重反映语义亲和度。

**边权重定义**（Eq. (2)）：

$$w_{ij} = \begin{cases} \exp\left(-\frac{\tau_i - \langle x_i, x_j \rangle}{\sigma}\right), & \text{if } \langle x_i, x_j \rangle > \tau_i; \\ 0, & \text{otherwise}. \end{cases}$$

其中 $\langle x_i, x_j \rangle$ 为节点 $i$ 与 $j$ 嵌入的余弦相似度，$\tau_i$ 为节点 $i$ 的局部自适应阈值，$\sigma$ 控制衰减速率。当相似度低于阈值时边权重为零，实现稀疏化；高于阈值时通过指数衰减赋予软连接权重，使高度相似的概念间保持强连接。

**局部自适应阈值**（Eq. (3)）：

$$\tau_i = \tau_0 + \lambda \cdot \sqrt{\frac{1}{|\mathcal{N}_i|} \sum_{j \in \mathcal{N}_i} \left( \langle x_i, x_j \rangle - \mu_i \right)^2}$$

该阈值由基础阈值 $\tau_0$ 和局部相似度标准差加权构成，$\lambda$ 为缩放因子。这种设计使阈值能根据节点 $i$ 邻域 $\mathcal{N}_i$ 内相似度的离散程度自适应调整：在语义密集区域阈值更高，在稀疏区域阈值更低，从而更精准地捕获局部语义结构。

### 4.2 IDENTIFY：自适应目标簇识别

IDENTIFY 模块在构建好的语义图上识别与目标概念 $c_t$ 紧密纠缠的概念簇，防止后续切断操作误伤邻近语义。

**步骤一：局部子图构建**（Eq. (5)）。以目标概念 $c_t$ 为锚点，提取其 $n$ 跳邻域内的所有节点构成局部子图 $\mathcal{G}_{\text{sub}} = (\mathcal{V}_{\text{sub}}, \mathcal{E}_{\text{sub}})$：

$$\mathcal{V}_{\text{sub}} = \{ v_i \in \mathcal{V} \mid d(v_i, c_t) \leq n \}$$

其中 $d(v_i, c_t)$ 为图上最短路径距离，$n$ 为跳数超参数。这一约束将语义扩散限制在锚点的局部邻域，避免全局计算开销。

**步骤二：语义扩散**（Eq. (6)）。在局部子图上模拟扩散过程，从锚点向邻域传播语义影响：

$$s = \exp(-\varphi \mathcal{L}_{\text{sub}}) Y$$

其中 $\mathcal{L}_{\text{sub}}$ 为子图的归一化拉普拉斯矩阵，$Y$ 为锚点的独热指示向量，$\varphi$ 为扩散尺度参数。矩阵指数 $\exp(-\varphi \mathcal{L}_{\text{sub}})$ 实现了图上多跳平滑扩散，使与锚点通过强边连接且路径短的节点获得更高影响分数 $s$。

**步骤三：Top-K 簇选择**（Eq. (7)）。根据扩散分数 $s$ 选取前 $K$ 个最高分节点，构成目标概念簇 $\mathcal{V}_c$。该簇包含了与目标概念语义高度纠缠的邻近概念（如擦除 “bear” 时可能包含 “grizzly”、“panda” 等），为后续精确切断提供上下文感知的抑制范围。

### 4.3 SEVER：选择性语义切断

SEVER 模块在文本嵌入层执行概念擦除：对提示中的每个 Token 嵌入 $t_i$，计算目标概念簇 $\mathcal{V}_c$ 对其的投影影响，并过滤高影响 Token。

**Token 影响分数**（Eq. (8)）：

$$\alpha_i = \sum_{c'_t \in \mathcal{V}_c} \exp(-\gamma d(t_i, c'_t)) \langle f_i, x_j \rangle x_j$$

该公式聚合了目标簇中所有节点对当前 Token 的加权投影贡献。其中 $\langle f_i, x_j \rangle$ 为 Token 特征 $f_i$ 与簇节点嵌入 $x_j$ 的余弦相似度，$x_j$ 为投影方向；$\exp(-\gamma d(t_i, c'_t))$ 为图上最短路径衰减因子，$\gamma$ 控制衰减速率，使得与目标概念图上距离越远的 Token 受影响越小。最终 $\alpha_i$ 是一个向量，其范数 $\|\alpha_i\|$ 量化了目标簇对该 Token 的总体语义影响程度。

**Token 保留条件**（Eq. (9)）：

$$t' = \{ t_i \in t \mid \mathbb{I}(\|\alpha_i\| \leq \delta) \}$$

只保留影响范数不超过阈值 $\delta$ 的 Token，其余 Token 被视为与目标概念高度相关而被移除。修改后的提示 $t'$ 重新编码后送入扩散模型生成图像，从而在源头抑制目标概念的视觉表达。

**关键设计动机**：SEVER 仅作用于文本嵌入层，且切断粒度精确到 Token 级别——这与 IDENTIFY 识别的概念簇形成闭环：簇内概念被系统性抑制，簇外语义（包括句子结构和无关内容）得以完整保留。消融实验（Table 3）证实，移除 IDENTIFY 后非目标 FID 从 0 暴增至 426.74，验证了该模块在防止过度擦除中的关键作用。

### 补充图表

![[assets/figures/papers/paper_list_l2315_https_openaccess_thecvf_com_content_CVPR2026_html_Han_GrOCE_Graph_Guided/figures/001_Figure_1.jpg]]
*Figure 1: Two key aspects of concept erasure. (a) Concept erasure in text-to-image diffusion models involves both explicit and implicit semantic structure in the latent space. Our method leverages adjacency in semantic space to suppress a target concept while better preserving its neighboring, non-target concepts. (b) Runtime comparison with the training-based ConAbl [16] and the recent training-free AdaVD [37]. Our method achieves an order-of-magnitude speedup, making online large-scale concept removal practical*

## 实验与分析

### 核心定量结果

GrOCE在单一、多目标及艺术风格概念擦除任务上均取得最优性能，验证了其精确擦除与极致保留的双重能力。表1汇总了单概念（Snoopy）、双概念（Snoopy & Mickey）及三概念（Snoopy, Mickey & Spongebob）擦除的定量对比。在单概念擦除中，GrOCE取得最低的概念相似度（CS=16.92），同时非目标概念的FID为0，表明擦除目标时完全未损害其他概念的生成质量。双概念擦除下，Snoopy和Mickey的CS分别降至16.92和18.37，非目标FID仍保持0。三概念擦除中，Spongebob的CS为16.45，非目标FID继续为0。在所有场景中，GrOCE的CS值均低于基于微调的方法（ESD、UCE、CA、SPM、MACE）和推理时方法（SPEED、AdaVD），且FID=0的完美保留记录在对比方法中极为罕见。

艺术风格擦除任务的结果进一步证实了方法的泛化能力。如表2所示，在擦除梵高风格时，GrOCE取得最低CS（23.28），同时对毕加索和莫奈风格的FID均为0。这一结果说明语义图结构能有效区分不同艺术风格的嵌入簇，切断操作精准针对目标风格而保留相邻风格。

### 消融实验：IDENTIFY模块的关键作用

表3的消融实验揭示了GrOCE三个组件中IDENTIFY模块的核心地位。当移除IDENTIFY模块、仅保留CONSTRUCT和SEVER时，目标概念Snoopy的CS从16.92略微下降至14.51，但非目标FID从0暴增至426.74。这一显著恶化表明：缺少自适应目标簇识别，SEVER的切断操作会过度抑制与目标概念无关的语义Token，导致生成内容大面积损坏。IDENTIFY通过语义扩散和Top-K选择，将切断范围精确限定在与目标概念紧密纠缠的概念簇内，是防止过度擦除的关键机制。

### 推理效率：在线大规模擦除的可行性

表4对比了不同方法擦除10个概念的总耗时。GrOCE仅需1.73秒，比训练方法快一个数量级，也显著优于其他推理时方法。这一效率优势源于三个因素：图构建仅依赖预计算的CLIP嵌入相似度；语义扩散限制在n-hop局部子图内；切断操作仅为Token嵌入的投影过滤。Figure 1(b)的延时对比直观展示了GrOCE相对于ConAbl（训练方法）和AdaVD（训练自由方法）的速度优势，使在线大规模概念清理成为可能。

### 跨模型泛化验证

Figure 5展示了GrOCE在三种不同主干扩散模型（Stable Diffusion v1.4、SDXL b1.0、FLUX.1-schnell）上的擦除性能。结果表明，GrOCE在不同架构上均能保持均衡的擦除与保留能力，验证了其即插即用的部署潜力。这一泛化性源于方法仅作用于文本嵌入层，不依赖特定模型的内部权重结构。

### 失败模式与局限性分析

尽管GrOCE在主要基准上表现优异，分析揭示了以下边界情况：

1. **语义图覆盖盲区**：语义图的构建依赖CLIP文本编码器的预训练知识，对于纯视觉概念（如特定构图风格、复杂光照交互）可能无法充分捕获。当目标概念缺乏明确的文本对应Token时，图中锚点初始化可能不准确，导致簇识别偏差。

2. **高密度语义邻域的边界模糊**：当目标概念与大量语义相近概念高度重叠时（如擦除“狗”而需保留数百种犬类品种），图中的簇边界可能模糊。此时IDENTIFY的Top-K选择可能遗漏部分关联节点或纳入不应切断的邻近概念，导致擦除不彻底或轻微误伤。

3. **超参数敏感性**：方法性能对多个超参数（τ₀、λ、K、δ等）敏感。论文在实验部分固定了参数值（τ₀=0.3, λ=0.1, n=2, φ=3, K=8, γ=0.8, δ=10），但在完全不同的概念域上可能需要重新调优。Table 3的消融已证明IDENTIFY移除后的剧烈退化，暗示参数选择对结果影响显著。

4. **嵌入层切断的深度局限**：选择性切断仅作用于文本嵌入层，无法抑制扩散模型内部更深层的概念依赖（如UNet跨注意力层中可能隐含的跨模态联系）。这意味着对于某些深度编码的概念，仅修改输入嵌入可能无法完全阻断其视觉生成。

### 重要图表结论

- **Table 1 & Table 2**：GrOCE在所有擦除场景下取得最低CS和完美非目标FID（0），证明精确擦除与极致保留的双重优势。
- **Table 3**：IDENTIFY模块的移除导致非目标FID暴增至426.74，验证了自适应簇识别在防止过度擦除中的关键作用。
- **Table 4**：GrOCE在10概念擦除中仅需1.73秒，比训练方法快一个数量级，支持在线大规模概念清理。
- **Figure 5**：在SDv1.4、SDXL、FLUX三种架构上均表现稳定，验证了方法的即插即用泛化能力。

![[assets/figures/papers/paper_list_l2315_https_openaccess_thecvf_com_content_CVPR2026_html_Han_GrOCE_Graph_Guided/figures/005_Table_1.jpg]]
*Table 1: Quantitative comparison of single- and multi-concept erasure*

![[assets/figures/papers/paper_list_l2315_https_openaccess_thecvf_com_content_CVPR2026_html_Han_GrOCE_Graph_Guided/figures/004_Table_2.jpg]]
*Table 2: Quantitative comparison of artistic style erasure*

![[assets/figures/papers/paper_list_l2315_https_openaccess_thecvf_com_content_CVPR2026_html_Han_GrOCE_Graph_Guided/figures/008_Table_3.jpg]]
*Table 3: Ablation studies on proposed components of GrOCE in erasing Snoopy*

![[assets/figures/papers/paper_list_l2315_https_openaccess_thecvf_com_content_CVPR2026_html_Han_GrOCE_Graph_Guided/figures/009_Table_4.jpg]]
*Table 4: Time consumption for 10-concept erasure*

![[assets/figures/papers/paper_list_l2315_https_openaccess_thecvf_com_content_CVPR2026_html_Han_GrOCE_Graph_Guided/figures/007_Figure_5.jpg]]
*Figure 5: Erasure Performance Validation Experiment under Multi-Diffusion Models*

### 补充图表

![[assets/figures/papers/paper_list_l2315_https_openaccess_thecvf_com_content_CVPR2026_html_Han_GrOCE_Graph_Guided/figures/003_Figure_3.jpg]]
*Figure 3: From the visualization results, our method demonstrates excellent erasure and retention capabilities, whether it is erasing Snoopy, Snoopy and Mickey, or Snoopy, Mickey and Spongebob. It can not only accurately accomplish target erasure but also stably retain prior knowledge in the process, thus achieving a balance between effectiveness and information retention*

![[assets/figures/papers/paper_list_l2315_https_openaccess_thecvf_com_content_CVPR2026_html_Han_GrOCE_Graph_Guided/figures/006_Figure_4.jpg]]
*Figure 4: Regarding Van Gogh-related content, we can not only accurately and efficiently erase the Van Gogh style, but also retain the ability to generate styles of Picasso and Monet, achieving an excellent balance between targeted removal and retention of key information*

## 方法谱系与知识库定位

### 核心差异：从“孤立擦除”到“图引导的上下文感知切断”

GrOCE 的根本创新在于将概念擦除从“孤立实体”的范式迁移到“语义拓扑”范式。现有方法要么通过微调模型权重来抑制目标概念，如 **ESD**（Gandikota et al., ICCV 2023）、**UCE**（Gandikota et al., WACV 2024）和 **CA**（Kumari et al., ICCV 2023），要么在推理时直接修改注意力图或激活值，如 **SPEED**（Li et al., ICLR 2026）和 **AdaVD**（Wang et al., CVPR 2025）。这些方法的共同瓶颈在于：它们将每个概念视为独立的擦除目标，忽略了概念之间固有的语义邻近性、层次关联和共现模式。这导致一个两难困境——擦除力度不足则目标残留，擦除力度过强则“误伤”邻近概念（例如擦除“Snoopy”时损坏“Mickey”的生成能力）。

GrOCE 通过三个协同组件改变了这一局面：
1. **CONSTRUCT**：在文本嵌入空间动态构建加权语义图，节点为词汇概念嵌入，边权重由余弦相似度与局部自适应阈值的差值经指数衰减定义（Eq. (2)-(3)），显式捕获概念间的软连接关系。
2. **IDENTIFY**：在图上以目标概念为锚点，通过语义扩散过程（Eq. (6)）识别与目标紧密纠缠的概念簇，将擦除问题转化为图上的连通性切断问题。
3. **SEVER**：对提示中的每个Token计算目标簇的加权投影影响分数（Eq. (8)），仅过滤掉投影范数超过阈值的Token（Eq. (9)），实现选择性切断。

这种设计使GrOCE成为**完全无训练、纯推理时操作**的方法，与需要模型优化的ESD、UCE、CA、**SPM**（Lyu et al., CVPR 2024）和**MACE**（Lu et al., CVPR 2024）形成鲜明对比。同时，GrOCE的图结构可在线增量更新，支持动态出现的概念擦除，而现有方法依赖固定的概念列表。

### 证据强度与关键验证

**决定性证据**来自消融实验（Table 3）：移除IDENTIFY模块后，虽然目标概念CS从16.92略微降至14.51，但非目标FID从0暴增至426.74。这直接证明了IDENTIFY在防止过度擦除和保留非目标语义方面的关键作用——没有图引导的簇识别，SEVER会盲目切断大量不相关的语义成分，导致全局图像质量崩溃。

**跨架构泛化性**在三种扩散模型上得到验证（Figure 5）：Stable Diffusion v1.4、SDXL b1.0和FLUX.1-schnell均展示了均衡的擦除与保留能力，证明GrOCE的即插即用特性不依赖特定模型架构。

**效率优势**在Table 4中得到量化：在10个概念并发擦除场景下，GrOCE仅需1.73秒，比训练方法快一个数量级，使在线大规模概念清理成为可能。

### 适用边界与局限

尽管GrOCE在单/多/风格概念擦除任务上取得了最低CS和完美非目标FID（Table 1, Table 2），其适用边界受以下因素制约：

1. **语义图的知识依赖**：图构建依赖CLIP文本编码器的预训练知识，可能无法充分捕获细粒度或纯视觉概念（如特定的构图风格、复杂光照交互）。当目标概念在CLIP空间中的表征不够精确时，图中的簇边界可能模糊。

2. **超参数敏感性**：性能对基阈值τ₀、扩散尺度φ、簇大小K、投影阈值δ等超参数敏感。论文在标准概念集上进行了调优（τ₀=0.3, λ=0.1, n=2, φ=3, K=8, γ=0.8, δ=10），但在完全不同的概念域上仍需重新调优，缺乏自适应机制。

3. **擦除深度的局限**：选择性切断仅作用于文本嵌入层，无法抑制扩散模型内部更深层的概念依赖（如UNet中可能隐含的跨模态联系）。当目标概念与大量语义相近概念高度重叠时，图中的簇边界可能模糊，导致擦除不彻底或轻微误伤。

4. **动态概念集的持续演化**：虽然GrOCE支持在线增量构建图，但在概念集合持续演化（增量添加新概念或弃用旧概念）时的图更新策略尚未被系统研究。

### 开放问题与未来方向

1. **多模态语义图扩展**：如何融合外部视觉知识库（如视觉概念图谱）以增强对纯视觉概念的捕获能力，是提升擦除精度的关键方向。

2. **混合擦除策略**：能否将图引导的在线擦除与部分参数微调相结合，在必要场景下实现更深层和更持久的擦除效果？这需要在效率与彻底性之间寻找新的平衡点。

3. **动态图更新策略**：当概念集合持续演化时，如何设计高效的图增量更新和过期概念剔除机制，使GrOCE适应真实世界的动态安全需求？

4. **跨任务迁移**：GrOCE的图结构分析能力能否延伸至其他扩散模型安全任务，如概念诅咒防御、受限内容编辑或生成过程中的实时安全控制？这需要验证语义图在不同安全目标下的通用性。

## 原文 PDF

![[paperPDFs/CVPR_2026/GrOCE_Graph_Guided_Online_Concept_Erasure_for_Text_to_Image_Diffusion_Models.pdf]]