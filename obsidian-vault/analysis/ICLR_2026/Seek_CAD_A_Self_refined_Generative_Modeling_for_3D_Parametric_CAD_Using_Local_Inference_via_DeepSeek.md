---
title: "Seek-CAD: A Self-refined Generative Modeling for 3D Parametric CAD Using Local Inference via DeepSeek"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Seek_CAD_A_Self_refined_Generative_Modeling_for_3D_Parametric_CAD_Using_Local_In_3b6e5b4dcc73.pdf
project_link: "https://ollama.com/"
code_link: "https://github.com/Sunny-Hack/Seek-CAD"
aliases:
- SC
- Seek-CAD
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
core_operator: 将DeepSeek-R1的CoT与逐步视觉反馈（SVF）对齐，并引入SSR设计范式，使模型可以自精炼生成的CAD代码。
primary_logic: 利用本地部署的推理大模型DeepSeek-R1，通过检索增强生成（RAG）和逐步视觉反馈（SVF）实现无需训练的CAD参数化模型生成，在保持高效率的同时显著提升几何保真度和语义对齐。
claims:
- Seek-CAD在CD、HD、IoGT、G-Score等指标上全面优于训练免费基线3D-PreMise和CADCodeVerify，例如CD从0.2164（CADCodeVerify）降至0.1979。
- 移除本地CAD语料库导致完全无法生成可编译的CAD命令，验证了RAG的必要性。
- SVF反馈策略的88.2%反馈被VLM判断为有帮助，且反馈后CD、IoGT显著提升。
- 消融实验表明逐步图像（inter-images）比单一最终图像提供更丰富的视觉信息，精炼效果更好。
---

# Seek-CAD: A Self-refined Generative Modeling for 3D Parametric CAD Using Local Inference via DeepSeek

> [!tip] 核心洞察
> 利用本地部署的推理大模型DeepSeek-R1，通过检索增强生成（RAG）和逐步视觉反馈（SVF）实现无需训练的CAD参数化模型生成，在保持高效率的同时显著提升几何保真度和语义对齐。

| 字段 | 内容 |
|------|------|
| 中文题名 | Seek-CAD：基于DeepSeek本地推理的3D参数化CAD自精炼生成模型 |
| 英文题名 | Seek-CAD: A Self-refined Generative Modeling for 3D Parametric CAD Using Local Inference via DeepSeek |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=PzIc2TxhwN) · [Code](https://github.com/Sunny-Hack/Seek-CAD) · [paper](https://arxiv.org/abs/2412.19663) · [Project](https://ollama.com/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation |
| Method | Seek-CAD |
| Dataset | SSR-based test set, DeepCAD dataset |

> [!tip] 效果简介
> - SSR-based test set (500 CAD models) 上，CD↓ 0.1979 vs 0.2164 (CADCodeVerify) (-0.0185 (-8.5%))；HD↓ 0.5566 vs 0.5917 (CADCodeVerify) (-0.0351 (-5.9%))；IoGT↑ 0.7226 vs 0.6562 (CADCodeVerify) (+0.0664 (+10.1%))。
> - DeepCAD dataset 上，CD↓ 0.1811 vs 0.2147 (CAD-Llama) (-0.0336 (-15.6%))；G-Score↑ 4.0604 vs 3.3385 (CAD-Llama) (+0.7219 (+21.6%))。

## 概要

**Seek-CAD** 是一个无需训练的3D参数化CAD生成框架，其核心思路是将本地部署的推理大模型DeepSeek-R1与检索增强生成（RAG）及逐步视觉反馈（SVF）相结合，实现CAD代码的自精炼生成。现有训练免费CAD生成方法缺乏链式思维（CoT）和逐步视觉反馈，导致复杂模型的几何精度与细节控制不足。Seek-CAD通过将DeepSeek-R1的CoT与逐步渲染图像对齐，并引入SSR（Sketch, Sketch-based feature, Refinements）三元组设计范式，在保持高效率的同时显著提升了几何保真度与语义对齐。

在500个CAD模型的测试集上，Seek-CAD在倒角距离（CD↓）、豪斯多夫距离（HD↓）、交并比IoGT↑和G-Score↑等指标上全面优于训练免费基线**CADCodeVerify**（Alrashedy et al., arXiv 2025）和**3D-PreMise**（Yuan et al., arXiv 2024），例如CD从0.2164降至0.1979，IoGT从0.6562提升至0.7226。在DeepCAD数据集上，Seek-CAD同样超越微调基线**CAD-Llama**（Li et al., AAAI 2025b），CD降低15.6%，G-Score提升21.6%。消融实验证实，移除本地CAD语料库将导致完全无法生成可编译命令，验证了RAG的必要性；SVF反馈在88.2%的情况下被VLM判定为有帮助，且逐步图像比单一最终图像提供更丰富的视觉信息。

方法上，Seek-CAD属于**训练免费的自精炼生成方法**，其关键创新在于：用本地部署的DeepSeek-R1-32B-Q4替代基于API的GPT-4作为推理主干，用SSR三元组范式扩展传统Sketch-Extrude范式，并通过混合搜索（向量+全文）的RAG和与CoT对齐的逐步视觉反馈实现自精炼。该方法不依赖任何微调，仅通过检索增强和知识约束即可生成可编译的类Python CAD代码，为资源受限场景下的高质量CAD生成提供了可行路径。



计算机辅助设计（CAD）是现代工业制造的基石，其参数化建模方式通过序列化命令构建几何形状，天然适合由语言模型生成。然而，现有的CAD生成方法面临一个核心瓶颈：**训练免费方法缺乏链式思维（CoT）和逐步视觉反馈，导致复杂模型的生成精度与细节控制严重不足**。以 **3D-PreMise**（Yuan et al., arXiv 2024）和 **CADCodeVerify**（Alrashedy et al., arXiv 2025）为代表的训练免费基线，虽然避免了微调成本，但其生成过程缺乏对中间建模步骤的感知与纠错能力，几何保真度和语义对齐均受限。另一方面，基于微调的方法如 **CAD-Llama**（Li et al., AAAI 2025b）虽然性能有所提升，却需要大量标注数据和训练资源，泛化到新设计模式时灵活性不足。

上述缺口源于两个关键因果环节的缺失。其一，现有方法将CAD生成视为一次性代码输出任务，未利用推理大模型的链式思维来显式建模从草图到三维特征的逐步构建逻辑。其二，视觉反馈仅依赖最终形状的单张图像（如3D-PreMise的做法），无法捕捉中间拓扑变化中累积的误差，导致精炼信号粗糙且滞后。

针对这些问题，Seek-CAD提出了一种根本性的解决思路：**将本地部署的推理大模型DeepSeek-R1的CoT与逐步视觉反馈（SVF）对齐，并引入SSR设计范式，使模型能够在无需训练的条件下自精炼生成的CAD代码**。其核心洞察在于，利用检索增强生成（RAG）从本地CAD语料库中注入领域知识，再通过逐步渲染的中间图像序列为VLM提供细粒度反馈，从而在保持高效率的同时显著提升几何保真度和语义对齐。这一设计直接回应了训练免费方法在复杂建模场景下的精度瓶颈，为参数化CAD生成开辟了“推理即精炼”的新路径。



## 核心方法与创新机理

Seek-CAD的核心创新并非单一技术的突破，而是通过**推理范式的重构**与**设计表示的重定义**，构建了一套无需训练即可实现高保真CAD生成的自精炼体系。其创新点可凝练为以下四个紧密耦合的维度。

### 1. 从云端黑盒到本地推理主干的迁移

现有训练免费的CAD生成方法（如**3D-PreMise** (Yuan et al., arXiv 2024) 与 **CADCodeVerify** (Alrashedy et al., arXiv 2025)）普遍依赖闭源的GPT-4作为推理引擎，这带来了成本、隐私与可复现性的多重制约。Seek-CAD首次将**本地部署的DeepSeek-R1-32B-Q4**引入CAD生成管线（Sec 3.1），其关键价值在于：

- **链式思维（Chain-of-Thought, CoT）的原生可用性**：DeepSeek-R1在推理过程中输出的逐步思考链条，为后续的视觉反馈模块提供了天然的对齐目标，使得“思考过程”与“建模过程”的语义一致性评估成为可能。
- **资源效率与可控性**：通过量化模型在本地GPU上完成推理，避免了云端API的调用延迟与成本，同时使整个生成过程完全可控。

### 2. 从单步渲染到逐步视觉反馈的对齐机制

传统方法（如3D-PreMise）仅使用最终形状的单张渲染图作为反馈依据，忽略了CAD建模内在的**过程性**。Seek-CAD提出的**逐步视觉反馈（Step-wise Visual Feedback, SVF）**机制（Sec 3.2）从根本上改变了反馈的粒度：

- **过程-思考对齐**：将生成的CAD代码按SSR三元组逐步渲染为中间图像序列 $\mathcal{M}_{I}$，并将该序列与DeepSeek-R1的CoT一同提交给VLM（Gemini）进行对齐性评估。VLM据此生成反馈 $F_{call}$，判断当前生成是否符合设计逻辑。
- **精炼效率的跃升**：消融实验证实，使用逐步中间图像（inter-images）比仅使用最终图像（ultimate-image）在所有几何指标上均获得更好性能（Table 3, Models C vs D），这表明过程性视觉信息对精炼至关重要。

### 3. 从SE范式到SSR三元组设计范式的重构

传统CAD生成方法多遵循简单的Sketch-Extrude（SE）范式，难以表达工业级零件中常见的精修操作（如倒角、抽壳、拔模）。Seek-CAD引入了**SSR（Sketch, Sketch-based feature, Refinements）三元组设计范式**（Sec 4），将每个建模步骤形式化为：

$$S = ( s , f , \langle r _ { 1 } , r _ { 2 } , \ldots , r _ { k } \rangle \mathrm{ or } \emptyset )$$

其中 $s$ 为二维草图，$f$ 为基于草图的特征（拉伸、旋转等），$\langle r_i \rangle$ 为可选的有序精修操作序列。完整CAD模型 $\mathcal{M}$ 则由多个SSR三元组通过布尔操作串联而成：

$$\mathcal{M} = \langle S_{1}, \, \mathsf{op}_{1}, \, S_{2}, \, \mathsf{op}_{2}, \, \dots , \, S_{n} \rangle$$

该范式同时配套了**CapType引用机制**（Figure 3），通过 $\phi( a , C ) \rightarrow b$ 的映射关系（$C \in \{\mathrm{START}, \mathrm{END}, \mathrm{SWEPT}\}$），解决了精修操作中草图基元与三维基元之间的拓扑引用难题。这一设计使Seek-CAD能够生成比SE范式更复杂的工业特征。

### 4. 从孤立生成到检索增强的知识注入

Seek-CAD通过**基于混合搜索的检索增强生成（RAG）**（Sec 3.1），将本地SSR语料库的知识注入生成过程。其检索相似度采用向量相似度与全文检索分数的加权融合：

$$g_{i}^{\mathrm{final}} = \lambda \cdot g_{i}^{\mathrm{vec}} + (1 - \lambda) \cdot g_{i}^{\mathrm{full}}, \quad \lambda \in [0, 1]$$

消融实验揭示了RAG的决定性作用：**移除本地CAD语料库后，模型完全无法生成可编译的CAD命令**（Table 3, Model A），这验证了知识检索对语法正确性的兜底价值。同时，混合搜索策略在IoGT和G-Score上显著优于单一的向量搜索或全文搜索（Table 3, Models E, F vs H），表明语义相似性与精确文本匹配的互补性。

---

**创新间的因果耦合**：上述四个维度并非孤立存在。DeepSeek-R1的CoT能力为SVF提供了对齐锚点；SSR范式为逐步渲染提供了结构化的分解依据；RAG则为初始代码生成提供了语法与格式约束。三者共同构成了“检索约束生成→逐步视觉诊断→CoT引导精炼”的闭环，使Seek-CAD在无需任何训练的前提下，在CD（0.1979 vs. 0.2164）、IoGT（0.7226 vs. 0.6562）等核心指标上全面超越训练免费基线（Table 1）。



Seek-CAD 是一个训练免费（training-free）的 CAD 生成框架，其核心思想是将本地部署的推理大模型 DeepSeek-R1 与逐步视觉反馈（Step-wise Visual Feedback, SVF）相结合，实现“生成-反馈-精炼”的闭环。整个流水线分为两大阶段：**初始 CAD 代码生成** 和 **CAD 代码精炼**，二者共享同一套知识约束（Knowledge Constraint），并通过检索增强生成（RAG）和 SSR 三元组设计范式串联起从文本到可执行 CAD 代码的完整通路。

### 流水线总览

框架的输入为描述目标几何体的自然语言文本，输出为符合 SSR 范式的 Python 风格 CAD 代码。流水线可概括为以下步骤：

1. **检索增强生成（RAG）**：输入文本经向量化后，与本地 SSR 语料库进行混合搜索（向量相似度 + 全文检索），检索出最相关的 `(描述, 代码)` 对，作为上下文注入 DeepSeek-R1 的推理过程。
2. **初始代码生成**：DeepSeek-R1 在知识约束（系统提示，包含功能描述、SSR 文档和示例）的引导下，结合检索到的参考代码，生成初始 CAD 代码 `I_0`。该代码需通过语法修正模块确保可编译性。
3. **逐步视觉反馈（SVF）**：将初始代码解析为 SSR 三元组序列，逐步渲染中间形状，形成中间图像序列 `M_I`。同时提取 DeepSeek-R1 的链式思维（CoT）。将逐步图像与 CoT 一并送入 Gemini VLM，由 VLM 判断生成结果是否与设计意图对齐，并输出反馈 `F_call`。
4. **自精炼循环**：若 VLM 判断反馈为正向（`L=1`），则保留当前代码；否则（`L=0`）将反馈回传给 DeepSeek-R1，触发重新生成。最大迭代次数设为 1（即最多一次精炼），精炼后再次进行语法修正，输出最终代码。

整个流程的模块关系与数据流如 Figure 1 所示。

![[assets/figures/papers/paper_list_l76_https_openreview_net_forum_id_PzIc2TxhwN/figures/001_Figure_1.jpg]]
*Figure 1: The overview of our Seek-CAD framework. The whole pipeline can be divided into two parts consisting of "Initial CAD Code Generation" and "CAD Code Refinement", which are both embedded with a knowledge constraint depicted in Sec. 3.1 to guide DeepSeek-R1 to generate CAD code following the SSR paradigm (Sec. 4). For the first part, a given query T is enhanced by conducting RAG on a local CAD corpus that consisting 10, 000 CAD models. Next, Top-3 retrieved candidates would be concatenated with T to trigger DeepSeek-R1 to generate an initial CAD code*

### 核心设计决策

Seek-CAD 与传统训练免费方法（如 **3D-PreMise**（Yuan et al., arXiv 2024）和 **CADCodeVerify**（Alrashedy et al., arXiv 2025））的关键差异体现在四个维度：

| 维度 | 基线方法 | Seek-CAD | 作用机制 |
|------|---------|----------|---------|
| 推理主干 | GPT-4（云端 API） | DeepSeek-R1-32B-Q4（本地部署） | 本地部署降低计算资源需求，同时利用 DeepSeek-R1 的 CoT 能力为视觉反馈提供对齐锚点 |
| 设计范式 | Sketch-Extrude（SE） | SSR 三元组（Sketch, Sketch-based feature, Refinements） | 将建模步骤标准化为“草图-特征-精修”三元组，支持更丰富的特征类型（如 shell、chamfer、fillet）和 CapType 拓扑引用 |
| 视觉反馈 | 仅最终形状单张图像 | 逐步图像 + CoT 对齐 | 逐步渲染展示建构过程，与推理链对齐后由 VLM 判断，反馈信息量显著提升 |
| 知识增强 | 无检索增强 | 混合搜索 RAG | 从本地语料库检索相关代码示例，保证生成代码的格式正确性和可编译性 |

### SSR 三元组范式

SSR 范式是 Seek-CAD 的建模基础。每个 CAD 模型 `M` 被表示为若干 SSR 三元组通过布尔操作串联而成的序列：

$$M = \langle S_{1}, \, \mathsf{op}_{1}, \, S_{2}, \, \mathsf{op}_{2}, \, \dots , \, S_{n} \rangle$$

其中每个三元组 `S = (s, f, ⟨r₁, r₂, …, rₖ⟩ or ∅)` 包含：二维草图 `s`、基于草图的特征 `f`（如 extrude、revolve）、以及可选的精修操作序列 `rᵢ`（如 fillet、chamfer、shell）。为处理精修操作中拓扑元素的引用问题，框架引入 CapType 引用机制：

$$\phi(a, C) \rightarrow b, \quad a \in \mathcal{A}, \, b \in \mathcal{B}, \, C \in \{\mathrm{START}, \mathrm{END}, \mathrm{SWEPT}\}$$

该机制将草图基元 `a` 按 CapType 类别（开始端/结束端/扫掠面）映射到三维基元 `b`，从而在建模过程中建立显式的拓扑引用关系。

### 反馈驱动的自精炼

SVF 模块的核心在于将逐步建构过程可视化，并与推理链对齐。逐步图像序列定义为：

$$\mathcal{M}_{I} = [ R(S_{1}), \, R(\bar{S}_{1} \oplus S_{2}), \, \dots , \, R(\bar{S}_{1} \oplus \bar{S}_{2} \oplus \dots \oplus S_{n}) ]$$

每一步渲染时，当前 SSR 实体被高亮显示，先前实体被隐藏，从而清晰展示逐步建构逻辑。VLM 根据提示 `G`、逐步图像 `M` 和推理链 `CoT` 生成反馈：

$$F_{call} \sim P( F_{call} \mid G, M, CoT )$$

消融实验表明，逐步图像比单一最终图像提供更丰富的视觉信息，精炼效果更优（Table 3, Models C vs D）。VLM 反馈在 88.2% 的情况下被判断为有帮助，精炼后 CD、IoGT 等指标在 Round 1 即有明显提升（Table 4 / Table 2）。

### 关键依赖与边界

框架的性能高度依赖本地 SSR 语料库的覆盖度——移除语料库后模型完全无法生成可编译的 CAD 命令（Table 3, Model A），验证了 RAG 的必要性。知识约束（系统提示）同样关键，移除后 Pass@1 从 0.68 降至 0.44（Table 3, Model B）。此外，VLM 反馈存在约 11.8% 的无法明确判断的情况，可能引入噪声；最大精炼迭代次数设为 1，可能不足以处理需要多次修正的复杂场景。



Seek-CAD 的核心架构由两个紧密协作的阶段构成：**本地推理流水线**与**逐步视觉反馈（SVF）自精炼循环**。两者共享一个统一的知识约束系统，并围绕作者提出的 **SSR 三元组设计范式** 展开，形成“生成—渲染—反馈—修正”的闭环。

### 3.1 本地推理流水线与 RAG

第一阶段的目标是生成符合 SSR 范式的初始 CAD 代码。系统将用户输入的文本描述 $T$ 作为查询，在本地 CAD 语料库上执行检索增强生成（RAG）。检索采用**混合相似度**对候选进行排序：

$$g_{i}^{\mathrm{final}} = \lambda \cdot g_{i}^{\mathrm{vec}} + (1 - \lambda) \cdot g_{i}^{\mathrm{full}}, \quad \lambda \in [0, 1]$$

其中 $g_{i}^{\mathrm{vec}}$ 为向量语义相似度，$g_{i}^{\mathrm{full}}$ 为全文检索分数，通过超参数 $\lambda$ 加权融合。检索到的 top-1 描述-代码对 $(d_j, c_j)$ 与输入文本拼接后，连同知识约束（系统提示）一起送入本地部署的 **DeepSeek-R1-32B-Q4** 进行推理，生成初始代码 $I_0$：

$$I_0 \sim \mathcal{P}(I_0 \mid T \oplus (d_j, c_j), Cons)$$

此处的知识约束 $Cons$ 包含 SSR 范式文档、PythonOCC API 说明及示例，是保证代码可编译性的关键——消融实验表明，移除该约束后 Pass@1 从 0.68 骤降至 0.44。

### 3.2 逐步视觉反馈与自精炼

第二阶段对初始代码 $I_0$ 进行语法修正后，将其解析为 SSR 三元组序列 $S_{seq}$，并依次渲染每一步的中间形状，生成**逐步中间图像序列**：

$$\mathcal{M}_{I} = [ R(S_{1}), \, R(\bar{S}_{1} \oplus S_{2}), \, \dots , \, R(\bar{S}_{1} \oplus \bar{S}_{2} \oplus \dots \oplus S_{n}) ]$$

其中 $R(\cdot)$ 为渲染函数，$\oplus$ 表示布尔操作，$\bar{S}_i$ 为当前步骤的实体。该序列突出每一步的增量建构过程，与 DeepSeek-R1 的链式思维（CoT）在时间维度上天然对齐。随后，逐步图像与 CoT 一同交由 Gemini VLM 进行评估，生成反馈：

$$F_{call} \sim P( F_{call} \mid G, M, CoT )$$

反馈 $F_{call}$ 包含一个二值标签 $L \in \{0, 1\}$（1 表示满意）和具体修改建议。若 $L=0$，则触发精炼循环：

$$I = \begin{cases} \{I_m\}_{m=0}^k & L=1 \\ I_k \sim \{P(I_k \mid I_{k-1}, F_{call}, Cons)\}_{k=1}^N & L=0 \end{cases}$$

系统最多执行 $N=2$ 次迭代，每次根据反馈调用 DeepSeek-R1 重新生成代码。实验表明，88.2% 的 VLM 反馈被判定为有帮助，且精炼后 CD、IoGT 等指标在 Round 1 即有显著提升。

### 4.1 SSR 三元组设计范式

为统一 CAD 建模的表示并解决中间拓扑元素的引用难题，Seek-CAD 提出了 **SSR（Sketch, Sketch-based feature, Refinements）三元组范式**。每个建模步骤表示为一个三元组：

$$S = ( s , f , \langle r _ { 1 } , r _ { 2 } , \ldots , r _ { k } \rangle \mathrm{ or } \emptyset )$$

其中 $s$ 为二维草图，$f$ 为基于草图的特征（如拉伸、旋转），$\langle r_1, \dots, r_k \rangle$ 为可选的有序精修操作序列（如抽壳、倒角、圆角）。完整 CAD 模型由多个三元组通过布尔操作串联而成：

$$\mathcal{M} = \langle S_{1}, \, \mathsf{op}_{1}, \, S_{2}, \, \mathsf{op}_{2}, \, \dots , \, S_{n} \rangle$$

### 4.2 CapType 引用机制

精修操作需要引用前序步骤产生的三维基元，但直接引用拓扑面/边极易因建模历史变化而失效。Seek-CAD 引入 **CapType 引用机制**，通过类别标签将草图基元映射到对应的三维基元：

$$\phi( a , C ) \rightarrow b , \quad a \in \mathcal{A}, \, b \in \mathcal{B}, \, C \in \{ \mathrm{START}, \mathrm{END}, \mathrm{SWEPT} \}$$

其中 $\mathcal{A}$ 为草图基元集合，$\mathcal{B}$ 为拉伸/旋转产生的三维基元集合，CapType $C$ 取值为起始端（START）、结束端（END）或扫掠面（SWEPT）。该映射在建模过程中自动追踪拓扑变化，为精修操作提供了稳定、可解释的引用锚点。

---

**瓶颈与因果机制小结**：现有训练免费方法（如 3D-PreMise）仅依赖最终形状的单张图像反馈，缺乏对逐步建构逻辑的感知，导致复杂模型的细节控制不足。Seek-CAD 通过将 DeepSeek-R1 的 CoT 与逐步渲染图像对齐，使 VLM 能够在每一步判断“当前操作是否符合设计意图”，从而生成精准的局部修正信号。RAG 与知识约束则从源头保证了代码的可编译性与 API 正确性，二者缺一不可——移除本地语料库后模型完全无法生成可编译命令。

### 补充图表

![[assets/figures/papers/paper_list_l76_https_openreview_net_forum_id_PzIc2TxhwN/figures/002_Figure_2.jpg]]
*Figure 2: The SSR Design Paradigm. Each CAD model is constructed as a sequence of SSR triplets, where each triplet consists of a sketch, a sketch-based feature (e.g., extrude, revolve), and optional refinement features (e.g., shell, chamfer, fillet). Topological primitives is traced using the CapType reference system (START, SWEPT, END) during modeling operations. Final shapes are formed by applying boolean operations (e.g., Union, Cut, Intersect) between the outputs of SSR triplets*

![[assets/figures/papers/paper_list_l76_https_openreview_net_forum_id_PzIc2TxhwN/figures/012_Figure_6.jpg]]
*Figure 6: The knowledge constraint adopted in Seek-CAD*



## 实验与关键发现

### 主实验结果

Seek-CAD 在包含 500 个 CAD 模型的 SSR 测试集上，与训练免费基线 **3D-PreMise**（Yuan et al., arXiv 2024）、**CADCodeVerify**（Alrashedy et al., arXiv 2025）以及基于微调的基线 **CAD-Llama**（Li et al., AAAI 2025b）进行了全面对比。Table 1 显示，Seek-CAD 在所有几何保真度指标上均取得最优结果：

![[assets/figures/papers/paper_list_l76_https_openreview_net_forum_id_PzIc2TxhwN/figures/004_Table_1.jpg]]
*Table 1: The quantitative results of generation ability tested on 500 CAD models*

- 相较于 CADCodeVerify，Chamfer Distance（CD↓）从 0.2164 降至 **0.1979**（-8.5%），Hausdorff Distance（HD↓）从 0.5917 降至 **0.5566**（-5.9%），IoGT↑ 从 0.6562 提升至 **0.7226**（+10.1%），G-Score↑ 从 3.3927 提升至 **3.5185**（+3.7%）。
- 相较于微调方法 CAD-Llama，Seek-CAD 同样表现出显著优势，尤其是在 G-Score 上，说明训练免费的本地推理范式在几何语义对齐方面已超越部分微调方案。

为进一步验证泛化性，在 DeepCAD 数据集上进行了额外测试（Table 6）。Seek-CAD 的 CD↓ 达到 **0.1811**，较 CAD-Llama 的 0.2147 降低 15.6%；G-Score↑ 达到 **4.0604**，较 CAD-Llama 的 3.3385 提升 21.6%。这一跨数据集的表现差异表明，SSR 设计范式与逐步视觉反馈的组合不仅适用于特定语料库，在更通用的 CAD 数据上也具有竞争力。

![[assets/figures/papers/paper_list_l76_https_openreview_net_forum_id_PzIc2TxhwN/figures/011_Table_6.jpg]]
*Table 6: The quantitative results of generation ability tested on the DeepCAD dataset*

### 精炼轮次消融

Table 2 展示了不同精炼轮次对性能的增量贡献。Round 0（无精炼）到 Round 1 的提升最为显著，CD 与 IoGT 均有明显改善；Round 2 带来的额外增益有限，部分指标甚至出现轻微回退。这与论文设定的最大迭代次数 N=2 一致：首轮精炼已能修正大部分几何偏差，过度迭代可能引入噪声。

![[assets/figures/papers/paper_list_l76_https_openreview_net_forum_id_PzIc2TxhwN/figures/006_Table_2.jpg]]
*Table 2: The quantitative results of comparing refinement rounds tested on 500 CAD models*

### 消融实验

在 200 个 CAD 模型上的消融实验（Table 3）揭示了各组件的因果作用：

![[assets/figures/papers/paper_list_l76_https_openreview_net_forum_id_PzIc2TxhwN/figures/007_Table_3.jpg]]
*Table 3: Ablation Studies on 200 CAD models*

- **本地 CAD 语料库（RAG）**：移除语料库后（Model A），模型完全无法生成可编译的 CAD 命令，Pass@1 失效。这验证了检索增强生成对于代码语法正确性的决定性作用。
- **知识约束（系统提示）**：移除知识约束（Model B）导致 Pass@1 从 0.68 骤降至 0.44，说明结构化的 SSR 文档与示例对约束 LLM 输出格式至关重要。
- **逐步图像 vs. 最终图像**：使用逐步中间图像（Model C）在所有指标上均优于仅使用最终渲染图像（Model D）。逐步图像提供的分步建构信息与 DeepSeek-R1 的链式思维更易对齐，使 VLM 能更精准地定位几何偏差。
- **混合搜索策略**：混合搜索（向量 + 全文，Model H）在 IoGT 和 G-Score 上显著优于纯向量搜索（Model E）或纯全文搜索（Model F），表明多模态检索信号对召回高质量 CAD 示例具有互补效应。

### VLM 反馈质量分析

Table 4 统计了 VLM 反馈的有效性：在 500 个测试样本上，**88.2%** 的反馈被判定为有帮助（Yes），仅约 11.8% 的反馈无法提供明确判断（Unsure 或 No）。结合 Table 1/Table 2 的精炼增益，可以确认 SVF 反馈在绝大多数情况下提供了有效的几何修正信号。但约 12% 的无效反馈仍是潜在的噪声源，可能限制进一步精炼的上限。

![[assets/figures/papers/paper_list_l76_https_openreview_net_forum_id_PzIc2TxhwN/figures/008_Table_4.jpg]]
*Table 4: The quantitative analysis of the VLM feedback on 500 CAD models*

### 复杂度分析与失败模式

Table 5 按 CAD 命令序列长度分层分析了模型性能。随着命令序列长度增加，各项指标呈下降趋势，表明 Seek-CAD 在处理高复杂度模型时仍面临挑战。这一退化可归因于两个瓶颈：一是长序列中链式思维的对齐难度增大，二是逐步渲染图像的信息密度随步骤增加而稀释，VLM 更难以从多张图像中提取精确的偏差信号。

### 定性结果

Figure 4 提供了生成结果的可视化对比与精炼案例。图 4(a) 显示 Seek-CAD 生成的 CAD 模型在几何细节和结构合理性上优于基线方法；图 4(b) 展示了 SVF 策略对初始生成结果的修正能力，例如修正了拉伸方向错误与倒角缺失等问题。Figure 5 进一步展示了 Seek-CAD 在相似生成、草图编辑和复杂模型生成等多种应用场景下的灵活性。

![[assets/figures/papers/paper_list_l76_https_openreview_net_forum_id_PzIc2TxhwN/figures/005_Figure_4.jpg]]
*Figure 4: (a) Visual illustrations of CAD generative comparison. (b) The visualizations of refinement capability through the SVF strategy (Recall Sec 3.2). Please enlarge to 225% to see the text clearly*

![[assets/figures/papers/paper_list_l76_https_openreview_net_forum_id_PzIc2TxhwN/figures/010_Figure_5.jpg]]
*Figure 5: Various Showcases by Seek-CAD. Please enlarge to 180% to see the text clearly*

![[assets/figures/papers/paper_list_l76_https_openreview_net_forum_id_PzIc2TxhwN/figures/017_Figure_10.jpg]]
*Figure 10: The enlarged version of showcases in Figure 5(c) of the main manuscript*

![[assets/figures/papers/paper_list_l76_https_openreview_net_forum_id_PzIc2TxhwN/figures/018_Figure_5.jpg]]
*Figure 5: (a) The extended showcases of Figure 5(a)Figure 11: The showcases of similar generations.iameter*



## 定位与知识库关联

### 与训练免费自精炼基线的继承与突破

Seek-CAD 直接继承了**训练免费自精炼CAD生成**这一研究路线的核心假设——无需针对CAD领域微调大语言模型，仅通过提示工程和外部反馈即可生成可用的参数化CAD代码。该路线上的代表性工作包括 **3D-PreMise**（Yuan et al., arXiv 2024）和 **CADCodeVerify**（Alrashedy et al., arXiv 2025），两者均依赖GPT-4作为推理主干，采用“生成-验证-修正”的循环范式。Seek-CAD 在此基础上做出了三个关键突破：

1. **推理主干的本地化部署**：将云端闭源模型GPT-4替换为本地部署的DeepSeek-R1-32B-Q4，消除了API调用延迟和成本约束，同时利用DeepSeek-R1原生的链式思维（CoT）推理能力，为后续逐步视觉反馈的引入提供了认知基础。

2. **设计范式的根本重构**：3D-PreMise和CADCodeVerify沿用传统的Sketch-Extrude（SE）范式，将建模过程简化为“草图-拉伸”的线性序列。Seek-CAD提出的**SSR三元组范式**（Sketch, Sketch-based feature, Refinements）将每个建模步骤扩展为包含可选精修操作的完整单元，并通过布尔操作串联多个三元组，显著提升了复杂模型（如含倒角、抽壳、圆角等精修特征）的表达能力。

3. **视觉反馈的粒度升级**：3D-PreMise仅使用最终形状的单张渲染图像进行反馈，丢失了建模过程的中间信息。Seek-CAD的**逐步视觉反馈（SVF）**机制将CAD代码按SSR三元组逐步渲染为中间图像序列，并与DeepSeek-R1的CoT对齐后交由Gemini VLM评估，实现了对每一步建模逻辑的细粒度验证。

### 与微调基线的范式差异

Seek-CAD 与基于微调的CAD生成方法（如 **CAD-Llama**，Li et al., AAAI 2025b）处于不同的技术范式。CAD-Llama通过在大量CAD数据上微调Llama模型来内化CAD语法和几何约束，其优势在于推理速度快、端到端一致性好，但代价是需要昂贵的训练资源，且对分布外（OOD）的CAD设计模式泛化能力有限。Seek-CAD的训练免费路线规避了这些限制：通过RAG从本地语料库动态检索相关示例，结合知识约束系统提示来规范输出格式，实现了零样本下的CAD代码生成。实验表明，Seek-CAD在DeepCAD数据集上的CD指标（0.1811 vs. 0.2147）和G-Score（4.0604 vs. 3.3385）均显著优于CAD-Llama，验证了训练免费路线在几何保真度上的竞争力。

### 适用边界与局限

Seek-CAD的能力边界由其设计选择所决定，主要体现在以下几个方面：

**对本地CAD语料库的强依赖**：消融实验（Table 3, Model A）表明，移除RAG模块后模型完全无法生成可编译的CAD命令，Pass@1降至零。这意味着Seek-CAD的泛化能力受限于语料库的覆盖范围，对完全未见过的CAD设计模式或非PythonOCC兼容的命令可能失效。语料库的构建成本和维护负担是实际部署中不可忽视的工程挑战。

**VLM反馈的可靠性瓶颈**：虽然SVF反馈在88.2%的情况下被判断为有帮助（Table 4），但仍有约11.8%的反馈无法提供明确判断，可能引入噪声。此外，反馈质量完全依赖外部Gemini VLM的API调用，引入了额外的延迟和成本，且VLM本身对CAD领域知识的理解深度未经系统验证。

**精炼迭代次数的保守设定**：最大精炼轮次设为1（Table 2显示Round 1后增益已趋于饱和），但对于需要多步修正的复杂几何错误，单轮精炼可能不足以完全纠正。这一设计选择在效率和精度之间做出了权衡，但牺牲了对极端案例的修复能力。

**SSR范式的覆盖范围**：尽管SSR范式扩展了特征集合（增加了fillet、chamfer、shell等精修操作），但仍无法覆盖所有工业CAD命令，如高级曲面特征、装配约束、参数化关系等。对于需要这些操作的CAD模型，Seek-CAD的生成能力存在结构性盲区。

**推理速度的硬件约束**：本地部署DeepSeek-R1-32B-Q4虽然降低了API成本，但推理速度受限于本地GPU性能和量化精度损失，可能不适合实时交互场景。量化模型（Q4）的推理质量与全精度模型之间的差距也未在论文中量化评估。

### 开放问题与未来方向

基于上述局限，Seek-CAD开辟了若干值得探索的方向：

1. **多模态输入的扩展**：当前仅支持文本到CAD的生成，能否将输入模态扩展至图像、点云或多步文本指令，实现从视觉数据到参数化CAD的直接转换，是连接逆向工程与生成式设计的关键问题。

2. **语料库依赖的弱化**：是否可以通过更强的知识约束或语法引导解码，在不依赖本地语料库的情况下保证生成代码的可编译性和格式正确性？这需要探索LLM对CAD领域语法的内在理解边界。

3. **自监督反馈的引入**：将SVF中的VLM反馈与更轻量的自监督信号（如渲染图像与目标图像的像素级损失、几何自交检测等）结合，有望减少对外部VLM的依赖，降低反馈延迟和成本。

4. **SSR范式的可扩展性验证**：在更大规模的语料库（如包含更多CAD软件的异构数据）上验证SSR范式和CapType引用机制的适用性，是推动该方法工业化的必要步骤。

5. **幻觉风险的量化与控制**：DeepSeek-R1作为推理模型，其CoT中可能包含看似合理但实际错误的几何推理。如何量化这种幻觉风险，并在不增加过多约束的情况下提高生成质量，是训练免费方法面临的共性挑战。



## 原文 PDF

![[paperPDFs/ICLR_2026/Seek_CAD_A_Self_refined_Generative_Modeling_for_3D_Parametric_CAD_Using_Local_In_3b6e5b4dcc73.pdf]]
