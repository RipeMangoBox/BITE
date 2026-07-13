---
title: "Hidden Dangers of Compositional Generation: Diagnosing Semantic Safety Failures in Text-to-Image Models"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Hidden_Dangers_of_Compositional_Generation_Diagnosing_Semantic_Safety_Failures_in_Text_to_Image_Models.pdf
project_link: null
code_link: null
aliases:
- CCRA
- HDCGDSSFTIM
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 在纯文本空间内进行细粒度语义分解与迭代选择重组，而非修改扩散模型的采样过程，使攻击在完全黑盒条件下即可绕过安全审查。
primary_logic: 组合生成模型天然倾向于将离散语义单元整合为连贯场景。攻击者可逆向利用该特性：将恶意意图分解为一组低风险的视觉元素，借助模型自身的组合能力将其自然融合为有害输出，从而在维持语义一致性的同时规避安全检查。
claims:
- CoRA在所有测试的T2I模型上显著提升攻击成功率（ASR），例如在Cogview4上达到0.733，远超最强基线Ring-a-Bell的0.563，同时在DALL·E 3上以0.644远超DACA的0.407。
- 通过人工排序框架（Elo、Hodgerank、Rank Centrality），CoRA始终排名第一，Elo分数约为1528，显著高于中性阈值1500，表明其生成的图像危害性最高且评判置信度高。
- 仅使用视觉隐喻而不进行选择性重组与迭代优化的变体（Metaphor-only）在ASR和IS上均大幅下降，证明选择性重组和迭代生成是攻击成功的关键。
- CoRA是一种黑盒攻击且极其高效，单次攻击平均耗时仅32秒，而最快的基线DACA仍需72.9秒，实现了效率与成功率的大幅领先。
---

# Hidden Dangers of Compositional Generation: Diagnosing Semantic Safety Failures in Text-to-Image Models

> [!tip] 核心洞察
> 组合生成模型天然倾向于将离散语义单元整合为连贯场景。攻击者可逆向利用该特性：将恶意意图分解为一组低风险的视觉元素，借助模型自身的组合能力将其自然融合为有害输出，从而在维持语义一致性的同时规避安全检查。

| 字段 | 内容 |
|------|------|
| 中文题名 | 组合生成中的隐形危险：诊断文本到图像模型的语义安全失败 |
| 英文题名 | Hidden Dangers of Compositional Generation: Diagnosing Semantic Safety Failures in Text-to-Image Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Yang_Hidden_Dangers_of_Compositional_Generation_Diagnosing_Semantic_Safety_Failures_in_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | CoRA (Composable Reassembly Attack) |
| Dataset | Cogview4, DALL·E 3, SDXL, Multi-model |

> [!tip] 效果简介
> - Cogview4 上，ASR 0.733 vs 0.563 (Ring-a-Bell) (+0.170)。
> - DALL·E 3 上，ASR 0.644 vs 0.407 (DACA) (+0.237)。
> - SDXL 上，ASR 0.593 vs 0.585 (Ring-a-Bell) (+0.008)。

## 概要

当前文本到图像（T2I）模型普遍部署了安全过滤机制，以防止生成有害内容。然而，这些机制在**语义组合层面存在系统性盲点**：当攻击者将恶意意图拆解为一组表面上无害的子场景，并借助模型自身的组合生成能力将其重新融合时，单一子场景不会触发报警，而组合后的整体语义却隐含危险。本文揭示了这一“组合生成中的隐形危险”，并提出了一种名为 **CoRA（Composable Reassembly Attack，可组合重组攻击）** 的黑盒攻击方法，用于系统性地诊断该安全漏洞。

CoRA 的核心洞见在于**逆向利用组合生成模型的天然倾向**——即模型擅长将离散语义单元整合为连贯场景。攻击者无需访问模型内部参数或修改采样过程，仅在纯文本空间内通过细粒度语义分解与迭代选择重组，即可引导目标模型自然融合出有害输出，同时规避安全检查。具体而言，CoRA 首先将恶意意图解析为结构化场景组件（人物、地点、动作、物体），再将其分解为多个低风险子场景并引入视觉隐喻以稀释有害元素；随后通过选择性重组与迭代生成，在最大化语义对齐的同时隐式绕过安全过滤器。

实验覆盖 Cogview4、DALL·E 3、SDXL、Hunyuan、Tongyiwanxiang 等多款主流 T2I 模型，以及 GPT-4o 等真实网络界面。主要结果如下：

- **攻击成功率（ASR）大幅领先**：CoRA 在 Cogview4 上达到 0.733，远超最强基线 Ring-a-Bell 的 0.563；在 DALL·E 3 上以 0.644 远超 DACA 的 0.407（Table 1）。
- **危害性排序第一**：通过 Elo、Hodgerank、Rank Centrality 三种人工排序聚合算法，CoRA 始终排名首位，Elo 分数约 1528，显著高于中性阈值 1500（Figure 4）。
- **效率与成功率双优**：单次攻击平均仅需 32.0 秒，而最快基线 DACA 需 72.9 秒（Table 2），实现了效率与攻击效果的大幅领先。
- **组件必要性验证**：消融实验表明，仅使用视觉隐喻而不进行选择性重组与迭代优化的变体（Metaphor-only），其 ASR 和 IS 均大幅下降，证明选择性重组和迭代生成是攻击成功的关键（Table 5）；更换不同规模的辅助模型对性能影响极小（Table 6），方法具有良好稳定性。

CoRA 的威胁模型为纯黑盒设定，仅需文本输入即可完成攻击，不依赖梯度、潜在变量或采样过程修改。这一特性使其对当前商用 T2I 系统构成现实威胁，同时也为防御方指明了方向：未来的安全机制必须从单一的提示级过滤，升级为能够感知语义组合风险的**分解-检测**范式。



### 文本到图像生成的安全困境

文本到图像（T2I）生成模型近年来取得了显著进展，代表性系统如 **DALL·E 3**（OpenAI, 2023）、**Cogview**（Zhipu AI）、**通义万相**（Alibaba Cloud）、**Hunyuan**（Tencent AI Lab）以及 **Gemini 2.0 Flash**（Google DeepMind）等已广泛应用于创意设计、内容生产等场景。这些模型通常内置安全过滤机制，旨在阻止生成暴力、色情等有害视觉内容。然而，当前安全策略主要针对**显式有害提示词**进行拦截——当用户输入包含高风险语义的完整场景描述时，过滤器能够有效阻断生成过程。

### 组合生成中的语义安全盲点

本研究的核心发现是：**T2I模型的安全过滤机制在语义组合层面存在系统性盲点**。如 Figure 1 所示，当有害意图被拆解为表面上无害的独立概念并分别输入时，模型可以正常生成每个子场景的图像；但当这些概念被直接组合为完整场景时，由于高风险语义的集中呈现，安全过滤器会立即触发阻断。这揭示了一个关键漏洞：**单一子场景不触发报警，但组合后的整体语义却隐含危险**。

更值得警惕的是，组合生成（compositional generation）模型天然倾向于将离散语义单元整合为连贯场景。攻击者可以逆向利用这一特性：将恶意意图分解为一组低风险的视觉元素，借助模型自身的组合能力将其自然融合为有害输出，从而在维持语义一致性的同时规避安全检查。

### 现有攻击方法的局限

已有针对T2I安全机制的攻击方法存在明显不足：

- **白盒依赖**：**MMA-Diffusion**（Yang et al., CVPR 2024）等方法需要同时扰动文本与图像通道，或修改扩散模型的采样过程，要求访问模型内部参数或梯度，在商业API等黑盒场景下完全失效。
- **语义一致性差**：**DACA**（Deng et al., arXiv 2023）等分治攻击方法虽将有害提示拆分为多个无害组件，但重组后的图像往往缺乏语义连贯性，难以真正还原原始恶意意图。
- **效率与成功率不足**：**Ring-a-Bell**（Tsai et al., ICLR 2024）等方法针对特定防御场景设计，泛化能力有限；**QF-GREEDY/QF-GENETIC/QF-PGD**（Zhuang et al., CVPR 2023）等无查询黑盒攻击虽不依赖模型内部信息，但在攻击成功率和生成质量上仍有较大提升空间。

### 本文动机与核心思路

针对上述缺口，本文提出 **CoRA（Composable Reassembly Attack）**，一种**纯文本空间中的黑盒攻击框架**。CoRA的核心洞察在于：攻击者无需修改扩散模型的采样过程，只需在文本层面进行**细粒度语义分解与迭代选择重组**，即可驱动T2I模型在生成过程中自然融合有害语义，同时规避安全审查。

具体而言，CoRA将攻击建模为一个约束优化问题：在保证各子场景单独通过安全检查的前提下，通过迭代选择与重组，最大化生成图像与原始恶意意图的语义对齐度。这一范式在完全黑盒条件下即可实施，仅需目标模型的文本输入接口，无需任何内部信息。



## 核心方法与创新机理

### 1. 攻击范式的根本转变：从采样空间侵入到纯文本语义操控

现有T2I安全攻击方法的核心思路几乎都依赖于对扩散模型采样过程的直接干预。例如，**MMA-Diffusion** (Yang et al., CVPR 2024) 同时扰动文本与图像两个模态通道，**QF-GREEDY/QF-GENETIC/QF-PGD** (Zhuang et al., CVPR 2023) 系列方法则通过无查询黑盒方式在潜在空间进行搜索优化。这些方法的共同前提是需要访问模型内部参数、梯度或采样步骤——即白盒或灰盒设定。

CoRA的关键创新在于**将攻击完全迁移到纯文本空间**。如 Figure 2 所示，整个攻击流水线不触及目标T2I模型的任何内部机制：攻击者仅通过精心构造的自然语言提示与模型进行黑盒交互。这一范式转变的因果机制在于：T2I模型天然具备将离散语义单元整合为连贯场景的组合生成能力，CoRA逆向利用该特性，将恶意意图编码为一系列表面无害的语义片段，交由模型自身的组合能力去“自然融合”为有害输出。

具体而言，这一转变体现在两个 **changed slots** 上：

| 维度 | 基线方法 | CoRA |
|------|----------|------|
| **攻击实现方式** | 修改扩散模型的采样过程（白盒/灰盒，需访问内部参数或梯度） | 纯文本空间中的语义分解与迭代重组（完全黑盒，仅使用文本输入） |
| **语义融合机制** | 通过潜在空间的条件概率最大化实现组合生成（修改采样步骤） | 基于大语言模型的细粒度语义补全与上下文模板组织，驱动T2I模型在生成过程中自然融合语义 |

这一设计使CoRA在真实部署场景中具有显著优势：攻击者无需任何模型内部信息，仅通过API调用即可实施攻击。Table 2 证实了该范式的效率优势——CoRA单次攻击平均耗时仅 **32.0秒**，而最快的基线方法DACA仍需 **72.9秒**，效率提升超过一倍。

### 2. 语义分解-选择性重组：破解组合安全盲区的核心机制

当前T2I模型安全过滤器的根本盲区在于：**它们在语义组合层面缺乏感知能力**。如 Figure 1 左侧所示，当有害意图被拆解为单独概念输入时，模型可以正常生成；但当这些概念被直接组合为完整场景时，安全过滤器会因高风险语义的存在而阻断生成。传统组合生成方法通过修改采样过程来维持语义一致性，但CoRA在不修改采样过程的前提下实现了同等效果。

CoRA破解这一盲区的核心机制是**细粒度语义分解与选择性重组**。其方法论逻辑如下：

1. **场景理解与结构化分解**：辅助模型 $\mathcal{M}$ 将恶意意图 $G$ 解析为结构化场景组件 $[C, L, A, O]$（人物、地点、动作、物体），如公式1所示：
   $$[C, L, A, O] = \mathcal{M}(G \mid P_G)$$

2. **子场景分解与安全性约束**：将结构化组件进一步分解为 $N$ 个子场景集合 $\{S_i\}_{i=1}^{N}$（公式2），并在保证子场景数量损失不超过阈值 $\epsilon$ 的前提下，最小化每个子集的安全性风险（公式3）：
   $$\{S_i\}_{i=1}^{N} = \mathcal{M}\big([C,L,A,O] \mid P_C\big)$$
   $$\underset{S_i^* \subseteq S_i}{\arg\min}\ \mathcal{M}(S_i^* \mid P_E)\ \mathrm{s.t.}\ \mathrm{Card}(S_i) - \mathrm{Card}(S_i^*) \le \epsilon$$

3. **选择性重组**：从每个安全子集中选出与原始恶意目标 $G$ 视觉最相关的候选描述（公式4），确保重组后的提示紧密对齐原意图：
   $$\mathbf{c}_i^* \in \underset{\mathbf{c} \in \mathbf{S}_i^*}{\arg\max}\ \mathcal{M}(\mathbf{S}_i^*, \mathbf{G} \mid P_{\mathcal{S}})$$

4. **迭代对齐优化**：利用上下文模板 $Z$ 将筛选出的子场景组织为连贯提示 $T(S^*)$（公式6），驱动目标模型 $\mathcal{V}$ 生成图像 $I(S^*)$（公式7），并通过一致性评估 $\mathcal{E}$ 的反馈迭代优化子场景选择，最大化生成图像与原始恶意目标的对齐度（公式8）：
   $$\underset{S^*}{\arg\max}\ \mathcal{E}(I(S^*), G)\ \mathrm{s.t.}\ I(S^*) = \mathcal{V}(T(S^*)),\ T(S^*) = \mathcal{M}(S^*, Z)$$

**消融实验（Table 5）提供了该机制必要性的决定性证据**：仅使用视觉隐喻但不进行选择性重组与迭代优化的变体（Metaphor-only）在ASR和IS上均大幅下降，证明选择性重组和迭代生成是攻击成功不可或缺的组件。这表明，单纯将有害元素“稀释”为隐喻并不足以绕过安全过滤器——关键在于通过迭代选择机制，从众多候选子场景中精准筛选出那些既能规避安全检查、又能在组合后恢复原始恶意识别的语义片段。

### 3. 辅助模型不敏感性：方法的鲁棒泛化特性

CoRA的另一重要创新特性是其**对辅助模型选择的低敏感性**。由于语义分解与选择性重组依赖辅助大语言模型（LLM）进行场景解析，一个自然的疑问是：更换不同规模或来源的LLM是否会显著影响攻击效果？

**Table 6 的消融实验给出了明确答案**：更换不同规模与来源的辅助模型（Qwen3-8B、Qwen2-7B、Qwen3-235B）对ASR和SC的影响极小，最大差异仅 **0.03/0.01**。这一结果表明，CoRA的攻击逻辑根植于语义分解与重组的结构性原理，而非特定LLM的涌现能力——只要辅助模型具备基本的场景解析与语义补全能力，攻击即可有效执行。该特性显著降低了攻击者的资源门槛，也意味着防御方不能寄希望于通过限制特定模型来阻断此类攻击。



CoRA（Composable Reassembly Attack）的整体设计遵循“分解—筛选—重组—迭代”的四阶段流水线，全程在纯文本空间中操作，不修改目标T2I模型的采样过程，从而在黑盒条件下实现语义安全绕行。其核心逻辑是：将有害意图拆解为表面上无害的细粒度视觉元素，利用T2I模型自身的组合生成能力，通过迭代选择与重组逐步恢复原始恶意语义，同时规避安全过滤器。

流水线由四个模块串联构成，如图2所示：

1. **场景理解 (Scene Understanding)**：以辅助模型 $\mathcal{M}$ 对输入的恶意目标意图 $G$ 进行语义解析，依据预定义提示 $P_G$ 提取结构化场景组件 $[C, L, A, O]$（人物、地点、动作、物体），即 $[C, L, A, O] = \mathcal{M}(G \mid P_G)$。

2. **语义分解 (Semantic Decomposition)**：将结构化组件进一步划分为 $N$ 个子场景集合 $\{S_i\}_{i=1}^{N}$，每个 $S_i$ 包含若干候选描述。分解过程由提示 $P_C$ 引导：$\{S_i\}_{i=1}^{N} = \mathcal{M}\big([C,L,A,O] \mid P_C\big)$。随后，在保证子场景数量损失不超过阈值 $\epsilon$ 的前提下，筛选出低风险子集 $S_i^*$，最小化其危害性评估得分：$\underset{S_i^* \subseteq S_i}{\arg\min}\ \mathcal{M}(S_i^* \mid P_E)\ \mathrm{s.t.}\ \mathrm{Card}(S_i) - \mathrm{Card}(S_i^*) \le \epsilon$。

3. **选择性重组 (Selective Reassembly)**：从每个安全子集 $S_i^*$ 中选取与原始目标 $G$ 视觉最相关的候选描述 $\mathbf{c}_i^*$：$\mathbf{c}_i^* \in \underset{\mathbf{c} \in \mathbf{S}_i^*}{\arg\max}\ \mathcal{M}(\mathbf{S}_i^*, \mathbf{G} \mid P_{\mathcal{S}})$。这一步骤确保重组后的提示在语义上紧密对齐原意图，而非随机拼接。

4. **迭代生成 (Iterative Generation)**：利用上下文模板 $Z$ 将筛选出的子场景集 $S^*$ 组织为连贯的对抗性图像提示 $T(S^*) = \mathcal{M}(S^*, Z)$，输入目标T2I模型 $\mathcal{V}$ 生成图像 $I(S^*) = \mathcal{V}(T(S^*))$。通过一致性评估 $\mathcal{E}(I(S^*), G)$ 的反馈，迭代更新子场景选择 $S^*$，以最大化生成图像与恶意目标 $G$ 的对齐度：$\underset{S^*}{\arg\max}\ \mathcal{E}(I(S^*), G)$，同时隐式满足安全约束。

该流水线的关键设计在于：**选择性重组与迭代生成**是攻击成功的核心驱动。消融实验（Table 5）表明，若仅使用视觉隐喻并随机选择子场景（Metaphor-only变体），攻击成功率（ASR）和语义一致性（SC）均大幅下降，证明随机拼接无法有效恢复恶意语义。迭代反馈机制则使攻击在维持语义一致性的同时，持续优化子场景选择以逼近原始有害意图。

### 补充图表

![[assets/figures/papers/paper_list_l2316_https_openaccess_thecvf_com_content_CVPR2026_html_Yang_Hidden_Dangers_of/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the CoRA (Composable Reassembly Attack) method: the potentially harmful intent is first decomposed into a set of fine-grained visual elements, which are then iteratively selected, refined, and reassembled into coherent prompts that guide the target T2I model to reconstruct the original malicious scene while avoiding safety checks by operating purely in the text space instead of modifying the model’s sampling process*



CoRA 的核心设计理念是**将有害意图的语义重构过程完全限定在文本空间内**，不触碰目标 T2I 模型的采样过程，从而在黑盒条件下实现高效攻击。整个流水线由四个关键模块串联构成，对应两组核心公式体系。

### 3.1 场景理解与语义分解

**模块一：场景理解 (Scene Understanding)**

攻击的起点是将恶意意图 $G$ 解析为结构化的场景组件。CoRA 利用辅助模型 $\mathcal{M}$ 完成这一语义解析：

$$[C, L, A, O] = \mathcal{M}(G \mid P_G)$$

其中 $P_G$ 是预定义的场景解析提示模板，四个提取出的组件分别代表：
- **C (Characters)**：场景中的人物角色
- **L (Location)**：场景发生的地点
- **A (Actions)**：场景中的动作行为
- **O (Objects)**：场景中的关键物体

这一步将模糊的自然语言意图转化为可操作的结构化语义单元，为后续分解提供精确的语义锚点。

**模块二：语义分解 (Semantic Decomposition)**

结构化组件被进一步拆解为多个低风险的子场景集合：

$$\{S_i\}_{i=1}^{N} = \mathcal{M}\big([C,L,A,O] \mid P_C\big)$$

$\mathcal{M}$ 根据分解提示 $P_C$ 将每个场景组件展开为 $N$ 个子场景 $S_i$，每个子场景包含一组候选视觉描述。此处的关键创新在于引入**视觉隐喻**来稀释有害元素的直接可识别性——例如，将暴力动作转化为抽象的运动姿态描述，在保留语义完整性的同时降低每个子场景的风险等级。

随后，CoRA 通过安全性约束筛选子场景子集：

$$\underset{S_i^* \subseteq S_i}{\arg\min}\ \mathcal{M}(S_i^* \mid P_E)\ \mathrm{s.t.}\ \mathrm{Card}(S_i) - \mathrm{Card}(S_i^*) \le \epsilon$$

其中 $P_E$ 是危害性评估提示，$\epsilon$ 控制允许移除的子场景数量上限。该约束在最小化安全风险与保留足够语义信息之间取得平衡——过度删减将导致语义断裂，使后续重组无法恢复原意图。

### 3.2 选择性重组与迭代生成

**模块三：选择性重组 (Selective Reassembly)**

从每个安全子集 $S_i^*$ 中，CoRA 选择与原始恶意目标 $G$ 视觉最相关的候选描述：

$$\mathbf{c}_i^* \in \underset{\mathbf{c} \in \mathbf{S}_i^*}{\arg\max}\ \mathcal{M}(\mathbf{S}_i^*, \mathbf{G} \mid P_{\mathcal{S}})$$

$P_{\mathcal{S}}$ 是语义相关性评估提示。这一选择机制确保重组后的提示与原始意图保持紧密对齐，而非随机拼接。

筛选出的子场景集 $S^*$ 通过上下文模板 $Z$ 组织为连贯的对抗性图像提示：

$$T(S^*) = \mathcal{M}(S^*, Z)$$

该提示随后被送入目标 T2I 模型 $\mathcal{V}$ 生成图像：

$$I(S^*) = \mathcal{V}(T(S^*))$$

**模块四：迭代生成 (Iterative Generation)**

单次重组可能无法充分恢复恶意语义。CoRA 引入一致性评估 $\mathcal{E}$ 的反馈循环，迭代优化子场景选择：

$$\underset{S^*}{\arg\max}\ \mathcal{E}(I(S^*), G)\ \mathrm{s.t.}\ I(S^*) = \mathcal{V}(T(S^*)),\ T(S^*) = \mathcal{M}(S^*, Z)$$

这一优化目标直接最大化生成图像 $I(S^*)$ 与原始恶意目标 $G$ 的语义对齐度。每次迭代中，$\mathcal{E}$ 评估当前输出与目标的差距，反馈驱动 $S^*$ 的更新，使得有害语义在迭代中逐步“渗透”进生成结果，同时整个流程始终在文本空间内操作，不触发安全过滤器的警报。

### 关键设计决策的证据支撑

消融实验（Table 5）为上述模块的必要性提供了有力佐证：**仅使用视觉隐喻而不进行选择性重组与迭代优化的变体（Metaphor-only），其 ASR 和 IS 均大幅下降**，证明选择性重组（模块三）和迭代生成（模块四）是攻击成功的决定性组件。此外，辅助模型消融（Table 6）显示，更换不同规模的 Qwen 系列模型对 ASR 和 SC 的影响极小（最大差异仅 0.03/0.01），表明上述公式体系对辅助模型选择不敏感，性能稳定。

### 补充图表

![[assets/figures/papers/paper_list_l2316_https_openaccess_thecvf_com_content_CVPR2026_html_Yang_Hidden_Dangers_of/figures/001_Figure_1.jpg]]
*Figure 1: The left part shows that when individual concepts are input separately, the model can generate images; however, when these concepts are combined into a complete scene, the generation is blocked by the safety filter due to the presence of high-risk semantics. To address this, we decompose the original scene into multiple sub-scenes, which can be generated but lead to semantic inconsistency as a whole. In contrast, compositional generation with modified sampling can maintain semantic consistency, while our fine-grained semantic completion achieves a similar effect without modifying the sampling process*



## 实验与关键发现

### 主结果：跨模型攻击成功率与语义一致性

CoRA 在六款主流 T2I 模型上均展现出显著优于所有基线方法的攻击成功率（ASR），同时保持了有竞争力的语义一致性（SC），如 **Table 1** 所示。

![[assets/figures/papers/paper_list_l2316_https_openaccess_thecvf_com_content_CVPR2026_html_Yang_Hidden_Dangers_of/figures/004_Table_1.jpg]]
*Table 1: Comparisons of ASR and SC between our method and baselines across multiple T2I models, with darker shading indicating better performance*

**瓶颈突破**：现有安全过滤机制在语义组合层面存在盲点——当有害意图被拆解为表面上无害的子场景并重新组合时，过滤器难以识别潜在恶意语义。CoRA 正是利用这一盲点，在纯文本空间内进行细粒度语义分解与迭代选择重组，实现了黑盒条件下的高效攻击。

**关键数据点**：
- 在 **Cogview4** 上，CoRA 的 ASR 达到 **0.733**，远超最强基线 Ring-a-Bell 的 0.563（+0.170）。
- 在 **DALL·E 3** 上，CoRA 的 ASR 达到 **0.644**，远超 DACA 的 0.407（+0.237），增幅高达 58%。
- 在 **SDXL** 上，CoRA（0.593）与 Ring-a-Bell（0.585）差距较小（+0.008），但 CoRA 的语义一致性（SC）在多数模型上表现更优，例如在 Cogview4 上 SC 为 0.260，在 Hunyuan 上为 0.276，在 Tongyiwanxiang 上为 0.269，均为所有方法中最高。

**因果机制**：CoRA 的攻击优势源于其“分解—选择—重组—迭代”的四阶段设计。与 DACA 的简单分治策略不同，CoRA 引入了视觉隐喻以稀释有害元素，并通过选择性重组确保重组后的提示与原恶意目标在视觉上紧密对齐；与 Ring-a-Bell 等依赖概念移除测试的方法不同，CoRA 不修改扩散模型的采样过程，完全在文本空间操作，因此对黑盒模型同样有效。

**证据强度**：Table 1 中的 ASR 和 SC 数据覆盖 Cogview4、DALL·E 3、Hunyuan、SDXL、Tongyiwanxiang 和 SafeGen 六款模型，实验结果高度一致，置信度极高（0.98）。

### 危害性排序：人工评估与聚合算法

仅靠 ASR 无法完全衡量攻击的实际危害程度。为此，作者引入了基于人工评判的危害性排序框架，采用 **Elo**、**Hodgerank** 和 **Rank Centrality** 三种聚合算法对六种攻击方法进行综合排名，如 **Figure 4** 所示。

![[assets/figures/papers/paper_list_l2316_https_openaccess_thecvf_com_content_CVPR2026_html_Yang_Hidden_Dangers_of/figures/005_Figure_4.jpg]]
*Figure 4: (a) Ranking visualizations produced by three aggregation algorithms (Elo, Hodgerank, and Rank Centrality) are shown side by side, with each column representing one algorithm’s output. Each node corresponds to an attack method (1: Ours; 2: DACA; 3: MMA-Diffusion; 4: QF-GREEDY; 5: QF-PGD; 6: Ring-a-Bell). The vertical placement of a node reflects its relative rank under that algorithm, and darker shading denotes higher harmfulness. (b) Distribution of Elo scores for the six attack methods. Each point represents a method, with its brightness and marker size both proportional to its Elo score—higher scores indicate attacks judged more harmful*

**核心发现**：
- 在三种聚合算法下，CoRA 始终排名第一（节点 1 在所有列中均位于最上方），表明其生成的图像危害性最高且评判置信度高。
- CoRA 的 **Elo 分数约为 1528**，显著高于中性阈值 1500，而其余方法（DACA、MMA-Diffusion、QF-GREEDY、QF-PGD、Ring-a-Bell）的 Elo 分数均低于 1528，说明 CoRA 在“绕过安全过滤器”与“恢复有害语义”之间实现了最佳平衡。

**定性证据**：**Figure 3** 的对抗图像可视化进一步佐证了这一结论。尽管所有方法都能绕过安全检查，但 CoRA 生成的图像中有害内容的严重程度明显更高（敏感内容已做模糊处理）。

### 时间效率：速度与成功率的双重领先

CoRA 不仅攻击效果最强，而且效率极高，如 **Table 2** 所示。

![[assets/figures/papers/paper_list_l2316_https_openaccess_thecvf_com_content_CVPR2026_html_Yang_Hidden_Dangers_of/figures/006_Table_2.jpg]]
*Table 2: Time efficiency comparisons with baselines*

**关键数据**：
- CoRA 单次攻击平均耗时仅 **32.0 秒**，而最快的基线 DACA 仍需 72.9 秒，CoRA 实现了 **40.9 秒** 的加速，效率提升超过一倍。
- 其他基线方法（如 MMA-Diffusion、Ring-a-Bell 等）耗时更长，部分方法因需要修改采样过程或进行多模态扰动而效率低下。

**因果解释**：CoRA 的高效源于其完全在文本空间操作的设计——无需访问模型内部参数或梯度，也无需修改扩散采样步骤。所有计算仅涉及辅助 LLM 的语义解析与迭代选择，单次迭代成本极低。

### 图像质量与提示对齐：IS 与 PPL

**Table 3** 报告了各方法生成图像的 Inception Score（IS，衡量图像质量与多样性）和 Perplexity（PPL，衡量提示与图像的对齐程度）。

**核心结论**：CoRA 在所有六款 T2I 模型上均取得了最高的 IS 和最低的 PPL，表明其在维持高攻击成功率的同时，并未牺牲图像质量或语义对齐。例如在 Cogview4 上，CoRA 的 IS 为 4.07、PPL 为 37.28，均为最优。

### 真实网络界面攻击验证

为进一步验证 CoRA 在实际部署环境中的有效性，作者在 **GPT-4o** 和 **GPT-4.1** 的官方网络界面上进行了交互式手动测试，结果如 **Table 4** 所示。

![[assets/figures/papers/paper_list_l2316_https_openaccess_thecvf_com_content_CVPR2026_html_Yang_Hidden_Dangers_of/figures/008_Table_4.jpg]]
*Table 4: Comparison of ASR and SC for GPT-4o and GPT-4.1, manually evaluated through interactive testing on the official web interface*

**关键发现**：
- 在 GPT-4o (web) 上，CoRA 的 ASR 达到 **0.667**，显著领先于其他方法。
- 这证明 CoRA 的黑盒攻击范式不仅适用于 API 调用的 T2I 模型，也能有效攻击带有前端安全审查的真实网络界面。

### 消融实验：核心组件的必要性

**视觉隐喻与选择性重组的关键作用**（**Table 5**）：

仅使用视觉隐喻而不进行选择性重组与迭代优化的变体（Metaphor-only）在 ASR 和 IS 上均大幅下降。这证明：
1. 单纯的隐喻替换不足以有效绕过安全过滤器——缺乏选择性重组会导致重组后的提示与原恶意目标语义偏离。
2. 迭代生成是最大化有害语义恢复的关键——单次生成无法保证攻击效果，需要通过一致性评估反馈循环持续优化子场景选择。

**辅助模型的鲁棒性**（**Table 6**）：

更换不同规模与来源的辅助模型（Qwen3-8B、Qwen2-7B、Qwen3-235B）对 CoRA 的 ASR 和 SC 影响极小，最大差异仅为 0.03/0.01。这表明 CoRA 对辅助 LLM 的选择不敏感，性能高度稳定，在受限环境下使用较小模型即可达到接近的效果。

### 失败模式与局限性

尽管 CoRA 在多数场景下表现优异，但分析揭示了以下边界：

1. **SDXL 上的边际优势**：在 SDXL 上，CoRA 的 ASR（0.593）仅以 0.008 的微弱优势领先 Ring-a-Bell（0.585）。这可能是因为 SDXL 的安全过滤器对语义组合的敏感度较低，或其对文本提示的解析方式不同于其他模型，使得分解-重组策略的增益有限。**此点需要手动验证具体原因**。

2. **动态防御的未知性**：论文未评估 CoRA 在面对自适应安全过滤器或在线动态防御时的鲁棒性。如果防御方引入语义分解检测机制（例如在预生成阶段对提示进行分解-风险评估），CoRA 的有效性可能受到挑战。

3. **LLM 依赖的潜在风险**：方法依赖辅助 LLM 进行场景解析与选择。尽管消融实验显示模型间差异微小，但在 LLM 完全不可用或极端受限的环境下，CoRA 的性能可能受到影响。论文未探索纯规则或模板驱动的替代方案。

### 补充图表

![[assets/figures/papers/paper_list_l2316_https_openaccess_thecvf_com_content_CVPR2026_html_Yang_Hidden_Dangers_of/figures/009_Table_5.jpg]]
*Table 5: Comparison between the Metaphor-only variant and the full CoRA framework across multiple T2I models. Higher is better for ASR, SC, IS, and lower is better for PPL*

![[assets/figures/papers/paper_list_l2316_https_openaccess_thecvf_com_content_CVPR2026_html_Yang_Hidden_Dangers_of/figures/010_Table_6.jpg]]
*Table 6: Comparisons across auxiliary models and T2I models, demonstrating CoRA’s adaptability and consistency across different model configurations. Higher values are better for ASR, SC, IS; lower is better for PPL*

![[assets/figures/papers/paper_list_l2316_https_openaccess_thecvf_com_content_CVPR2026_html_Yang_Hidden_Dangers_of/figures/003_Figure_3.jpg]]
*Figure 3: Visualization of adversarial images generated by different methods. Sensitive prompt tokens are highlighted in red, and sensitive content in the images has been masked for display. Although all methods successfully bypass the safety mechanisms, the severity of harmful content in the resulting images varies significantly*

![[assets/figures/papers/paper_list_l2316_https_openaccess_thecvf_com_content_CVPR2026_html_Yang_Hidden_Dangers_of/figures/007_Table_3.jpg]]
*Table 3: Comparison of IS and PPL between our method and baselines across multiple T2I Models, with darker shading indicating better performance*



## 定位与知识库关联

### 攻击范式谱系中的坐标

CoRA 的定位可从两条轴线理解：**对模型内部的访问程度**与**语义操纵的粒度**。传统 T2I 安全攻击大多沿其中一条轴线展开，而 CoRA 在两条轴线上同时实现了位移。

**白盒/灰盒攻击**以 **MMA-Diffusion** (Yang et al., CVPR 2024) 为代表，同时扰动文本与图像双通道，需要访问模型内部参数或梯度信息。这类方法在实验室条件下攻击力强，但面对商业黑盒 API（如 DALL·E 3、Cogview4）时完全失效。CoRA 的纯文本空间操作使其天然适用于黑盒场景，无需任何模型内部信息。

**分治式攻击**以 **DACA** (Deng et al., arXiv 2023) 为典型，将有害提示拆分为多个无害组件后分别生成。DACA 的瓶颈在于：简单的组件拆分破坏了语义连贯性，重组后的图像往往与原有害意图偏差较大。CoRA 通过引入**细粒度语义补全**机制——利用辅助 LLM 在分解时保留语义完整性，再通过选择性重组与迭代对齐——在维持语义一致性的同时实现更高的攻击成功率。定量对比：在 DALL·E 3 上，CoRA 的 ASR 达到 0.644，而 DACA 仅为 0.407（Table 1）。

**概念移除测试攻击**如 **Ring-a-Bell** (Tsai et al., ICLR 2024) 和**无查询黑盒攻击**系列 **QF-GREEDY/QF-GENETIC/QF-PGD** (Zhuang et al., CVPR 2023) 均侧重于在文本空间中进行提示优化，但缺乏对语义组合风险的利用。Ring-a-Bell 在 Cogview4 上取得 0.563 的 ASR，已是基线中最强，但仍被 CoRA 的 0.733 显著超越（+0.170），说明语义分解-重组的攻击逻辑比单纯的提示扰动更为根本。

### 核心机制差异：语义融合的实现路径

Figure 1 揭示了 CoRA 与先前方法的关键分水岭。传统组合生成通过修改扩散模型的采样过程（在潜在空间中最大化条件概率）来实现语义融合；CoRA 则**不触碰采样过程**，转而利用 LLM 的语义补全能力，在纯文本空间中组织上下文模板，驱动 T2I 模型在自身生成过程中自然融合子场景语义。这一设计选择带来了两个后果：

1. **攻击可迁移性极强**：CoRA 在 Cogview4、DALL·E 3、SDXL、Hunyuan、Tongyiwanxiang、SafeGen、GPT-4o 等 7 个不同架构的模型上均有效，且对辅助 LLM 的选择不敏感（Table 6，更换 Qwen3-8B/Qwen2-7B/Qwen3-235B 时 ASR 最大差异仅 0.03）。
2. **效率优势显著**：单次攻击平均耗时 32.0 秒，而最快的基线 DACA 仍需 72.9 秒（Table 2），效率提升超过一倍。

### 适用边界与局限

尽管 CoRA 在黑盒设定下表现突出，其适用边界值得审慎界定：

- **对辅助 LLM 的依赖**：场景理解、语义分解、选择性重组与迭代评估均依赖外部 LLM 作为辅助模型 M。消融实验（Table 6）表明不同 LLM 间的性能差异微小，但这建立在 LLM 本身具备足够语义解析能力的前提下。在极端受限环境（如无可用的高性能 LLM API）中，CoRA 的性能可能退化。一个开放问题是：能否通过纯文本模板或规则引擎替代 LLM，实现类似的细粒度语义操纵？

- **动态防御的未知性**：论文未评估 CoRA 在面对自适应安全过滤器时的鲁棒性。当前实验均在静态安全机制下进行；若防御方引入**预生成阶段的语义分解检测**——即将 CoRA 的攻击逻辑逆向用于防御——攻击成功率可能大幅下降。这一攻防博弈方向尚未被探索。

- **多模态扩展的开放性**：CoRA 的核心洞察——逆向利用组合生成模型的语义整合倾向——原则上可推广至视频生成、3D 场景生成等其他生成模态。然而，这些模态的语义空间更为复杂，分解-重组的粒度与评估指标需要重新设计。

### 知识库定位：安全攻击与防御研究的交叉点

CoRA 的工作位于三个研究方向的交汇处：

| 方向 | 与 CoRA 的关系 |
|------|---------------|
| **T2I 安全过滤** | 揭示当前安全机制的语义组合盲点：过滤器在单一子场景层面安全，但无法感知组合后的整体风险 |
| **组合生成** | 逆向利用组合生成模型“将离散语义单元整合为连贯场景”的天然倾向，将其从特性转化为攻击向量 |
| **黑盒对抗攻击** | 提供一种仅需文本访问的高效攻击范式，不依赖梯度、潜在空间或采样过程修改 |

从防御视角看，CoRA 提出的真正挑战并非具体攻击方法本身，而是其揭示的**结构性脆弱性**：只要安全过滤在语义组合层面存在盲点，攻击者就可以通过分解-重组策略绕过。这指向一个更深层的研究问题——如何设计能够感知语义组合风险的防御机制，在不损害模型创意生成能力的前提下有效阻断此类攻击。



## 原文 PDF

![[paperPDFs/CVPR_2026/Hidden_Dangers_of_Compositional_Generation_Diagnosing_Semantic_Safety_Failures_in_Text_to_Image_Models.pdf]]
