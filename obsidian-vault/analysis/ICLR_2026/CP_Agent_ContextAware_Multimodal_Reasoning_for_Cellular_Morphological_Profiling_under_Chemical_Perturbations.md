---
title: "CP-Agent: Context‑Aware Multimodal Reasoning for Cellular Morphological Profiling under Chemical Perturbations"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/CP_Agent_ContextAware_Multimodal_Reasoning_for_Cellular_Morphological_Profiling_under_Chemical_Perturbations.pdf
project_link: null
code_link: https://github.com/letitia-zhang/CP-Agent
openreview_forum_id: 7BLnSeWuei
aliases:
- CP-Agent
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/planning_control
core_operator: "通过CP-CLIP将结构化实验上下文（化合物描述符、浓度、时间）编码为连续嵌入并与细胞图像联合对齐，再结合多智能体MLLM推理，实现上下文感知的可解释形态学分析。"
primary_logic: "将实验上下文编码为连续数值嵌入，并与细胞绘画图像在统一对比学习框架中对齐，可显著提升化合物识别和机制推断的准确性，同时支撑下游智能体生成结构化、可解释的假设报告。"
claims:
- "CP-CLIP在化合物分类任务上达到Macro-avg F1=0.896，显著优于所有通用MLLM基线（最高仅0.102，甚至低于随机基线0.10）。"
- "掩码化合物名称和MoA导致文本到图像R@1从98.70暴跌至3.50（相对下降96.45%），证明模型并非依赖元数据相关性，而是学习了化合物特异性信息。"
- "CP-CLIP在未见药物匹配上平均余弦相似度较基线CLIP绝对提升14.6%（0.432 vs 0.286），表现出强泛化能力。"
- "化合物分类（10类已知药物） 上 Macro-avg F1 = 0.896 (CP-CLIP ViT-B/16 descriptor)"
---

# CP-Agent: Context‑Aware Multimodal Reasoning for Cellular Morphological Profiling under Chemical Perturbations

> [!tip] 核心洞察
> 将实验上下文编码为连续数值嵌入，并与细胞绘画图像在统一对比学习框架中对齐，可显著提升化合物识别和机制推断的准确性，同时支撑下游智能体生成结构化、可解释的假设报告。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | CP-Agent：化学扰动下细胞形态学分析的上下文感知多模态推理 |
| 英文题名 | CP-Agent: Context‑Aware Multimodal Reasoning for Cellular Morphological Profiling under Chemical Perturbations |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=7BLnSeWuei) · [GitHub](https://github.com/letitia-zhang/CP-Agent) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/planning_control |
| Method | CP-Agent |
| Dataset | 化合物分类（10类已知药物）, 未见药物匹配（零样本）, 上下文到图像检索 |

> [!tip] 效果简介
> - 化合物分类（10类已知药物） 上，Macro-avg F1 为 0.896 (CP-CLIP ViT-B/16 descriptor)，对比 0.102 (Grok-4, 最佳MLLM)，变化 +0.794。
> - 未见药物匹配（零样本） 上，平均余弦相似度 为 0.432 (CP-CLIP ViT-B/16 descriptor)，对比 0.286 (CLIP ViT-B/16)，变化 +0.146。
> - 上下文到图像检索 上，R@1 为 77.09 (CP-CLIP ViT-B/16 descriptor)，对比 66.80 (CLIP ViT-B/16)，变化 +10.29。

## 概要

细胞形态学分析（Cell Painting）是药物发现中评估化合物生物活性的关键工具，但现有方法普遍忽略实验上下文（细胞系、剂量、时间等），导致形态学响应建模不准确、泛化能力差，且缺乏语义可解释性，限制了假设生成与决策支持。

**核心结论**：本文提出 CP-Agent，通过上下文感知的多模态对齐模块 CP-CLIP 将结构化实验元数据（化合物描述符、浓度、时间）编码为连续嵌入并与细胞图像联合对齐，再结合多智能体 MLLM 推理，实现可解释的形态学分析。CP-CLIP 在化合物分类上达到 Macro-avg F1=0.896，显著优于所有通用 MLLM 基线（最高仅 0.102，甚至低于随机基线 0.10）；在未见药物匹配上平均余弦相似度较基线 CLIP 绝对提升 14.6%（0.432 vs 0.286），表现出强泛化能力。掩码消融实验证实模型并非依赖元数据相关性，而是学习了化合物特异性信息——掩码化合物名称和 MoA 导致文本到图像 R@1 从 98.70 暴跌至 3.50（相对下降 96.45%）。

**方法定位**：CP-Agent 属于**上下文感知的多模态对比学习 + 工具增强型多智能体推理**范式。其核心 CP-CLIP 在 CLIP 框架基础上做出两项关键改动：(1) 图像分支输入由单幅扰动图像改为扰动图像与对照图像沿通道维度拼接，使模型直接学习扰动引起的差异；(2) 文本编码端引入混合序列，将标准子词嵌入与通过专用 MLP 编码的结构化上下文嵌入（`<CMPD>`、`<CONC>`、`<TIME>`）融合，替代传统 CLIP 仅使用自然语言描述的方式。CP-CLIP 在 190 万图像-上下文对上预训练后，作为下游 CP-Agent 的记忆检索与感知骨干，驱动六个模块化智能体（CPContext、ChannelSeg、CellFeat、FeatRank、StatSynth、ReportGen）协同完成从上下文检索、细胞分割、特征提取、特征排序、统计检验到报告生成的全流程。

**主要结果速览**：在化合物分类（10 类已知药物）上，CP-CLIP 的 Macro-avg F1 达到 0.896，较最佳通用 MLLM（Grok-4，0.102）提升 0.794；在零样本未见药物匹配上，平均余弦相似度 0.432，较 CLIP 基线（0.286）提升 0.146；在上下文到图像检索上，R@1 达到 77.09，较 CLIP（66.80）提升 10.29 个点。消融实验进一步表明，连续描述符编码优于二进制指纹编码，浓度信息具有中等重要性，而时间信息贡献较小。CP-Agent 生成的报告能够识别清晰（Taxol）、细微（Sorbinil）和复杂（BGT226）的形态学响应，并将其与合理的生物学机制关联。



### 细胞形态学分析在药物发现中的核心地位

基于图像的细胞形态学分析（Cell Painting）已成为药物发现和系统生物学中不可或缺的表型筛选工具。其核心假设是：化学扰动引发的细胞形态变化携带着关于化合物作用机制（Mechanism of Action, MoA）和靶点活性的丰富信息。通过高通量显微镜采集多通道荧光图像，研究者能够以无偏方式捕捉细胞在形态、纹理和空间组织上的细微变化，从而推断化合物的生物效应。

然而，将原始图像转化为可操作的生物学见解面临根本性挑战。单次实验往往涉及多种细胞系、多个浓度梯度和不同处理时间，产生高维、异质的图像数据。现有方法在从这些数据中提取稳健、可泛化且语义可解释的表型特征方面，仍存在显著不足。

### 现有方法的瓶颈：忽视实验上下文

当前细胞形态学分析的主流范式存在一个系统性缺陷：**将细胞图像视为孤立样本，忽略了产生这些图像的实验上下文**。具体而言，化合物身份、浓度剂量、处理时间、细胞系类型等关键元数据，要么被完全丢弃，要么仅在后期以简单拼接方式引入。这导致三个核心问题：

**其一，形态学响应建模不准确。** 同一化合物在不同浓度下可能诱导截然不同的表型——低浓度可能仅引起轻微应激反应，而高浓度则触发凋亡或坏死。若模型不知晓浓度信息，则无法区分这些本质不同的生物状态，将同一化合物的异质响应错误地归为噪声或矛盾信号。

**其二，泛化能力受限。** 当模型未学习到“浓度-形态”或“时间-形态”的映射关系时，其学得的表征高度依赖于训练数据的特定分布。面对未见化合物或新实验条件时，模型缺乏将图像变化与化学或物理上下文关联的能力，导致零样本泛化性能急剧下降。

**其三，缺乏语义可解释性。** 即使模型能正确分类化合物或预测MoA，其决策过程仍是黑箱。研究者无法得知哪些形态特征在何种浓度下发生了显著变化，也无法将表型变化与已知的药理学机制建立可追溯的联系。这严重限制了药物发现中的假设生成与决策支持。

### 通用MLLM的直接应用：表现令人失望

一个直观的思路是借助当前强大的多模态大语言模型（MLLMs）直接分析细胞图像。然而，CP-Agent的工作通过系统评估揭示了这一路径的根本局限。在化合物分类任务上（10类已知药物），**Grok-4**（xAI, 2025）、**GPT-5**（OpenAI, 2025）、**Claude-4-Sonnet**（Anthropic, 2025）和**Gemini-2.5-Pro**（Google DeepMind, 2025）等顶尖MLLM的Macro-avg F1最高仅为0.102，几乎与随机基线（0.10）持平（Table 2）。这表明通用视觉-语言模型缺乏对细胞绘画图像中微妙表型差异的感知能力，更无法将图像与结构化的实验条件相关联。

### 本文动机：走向上下文感知的可解释形态学分析

上述缺口指向一个明确的研究方向：**如何构建一个能够联合编码细胞图像与结构化实验上下文的模型，并在此基础上实现可解释的推理？**

CP-Agent的动机正是填补这一空白。其核心思路是双重的：首先，通过CP-CLIP将实验上下文（化合物分子描述符、浓度、时间）编码为连续嵌入，并与细胞图像在统一对比学习框架中对齐，使模型学会上下文感知的表征；其次，基于该表征构建模块化多智能体系统，依次执行上下文检索、细胞分割、特征提取、统计推断和报告生成，最终输出包含机制推断与后续实验建议的结构化假设报告。这一设计旨在将细胞形态学分析从“盲目的模式匹配”提升为“上下文引导的机制推理”。



## 核心方法与创新机理

### 瓶颈与因果机制

现有细胞形态学分析方法存在一个根本性瓶颈：**忽略实验上下文**（细胞系、剂量、时间等元数据），导致形态学响应建模不准确、泛化能力差，且缺乏语义可解释性，限制了药物发现中的假设生成与决策。CP-Agent 的核心因果调控变量在于：**通过 CP-CLIP 将结构化实验上下文编码为连续嵌入并与细胞图像联合对齐**，再结合多智能体 MLLM 推理，实现上下文感知的可解释形态学分析。

### 关键创新点（Changed Slots）

CP-Agent 相对于现有基线在三个关键维度上实现了结构性改变：

**1. 图像分支输入：从单幅扰动图像到双通道对照拼接**

基线方法（如 CLIP ViT-B/16、SigLIP）仅将单幅扰动图像作为视觉输入。CP-CLIP 将扰动图像与匹配的对照图像沿通道维度拼接，形成双通道输入：

$$\hat{x} = \text{concat}(x_p, \dot{x}_c) \in \mathbb{R}^{512 \times 512 \times 2}$$

这一设计使得模型能够直接感知扰动相对于对照的形态学变化，而非孤立地编码扰动状态（Section 2.3）。

**2. 文本编码方式：从纯自然语言到混合结构化嵌入**

基线方法仅使用自然语言文本描述进行编码。CP-CLIP 引入**字段专用占位符**（`<CMPD>`、`<CONC>`、`<TIME>`），并通过专用 MLP 将结构化上下文编码为与子词嵌入同维度的连续嵌入：

$$e_{\text{cmpt}} = f_{\text{cmpt}}(z_{\text{cmpt}}) \in \mathbb{R}^{D}$$

这些嵌入与标准子词嵌入交替排列，构成混合文本序列：

$$X = [\text{CLS}, t_1, t_2, \dotsc, \underbrace{e_{\text{cmpt}}}_{<\text{CMPD}>}, \dotsc, \underbrace{e_{\text{conc}}}_{<\text{CONC}>}, \dotsc, \underbrace{e_{\text{time}}}_{<\text{TME}>}, \dotsc]$$

其中化合物描述符采用 174 个 RDKit2D 描述符经 z-score 标准化后输入 MLP，浓度编码为归一化剂量对 $[\rho_{\text{max}}, s(C)]$，时间归一化至单位区间 $\tilde{t} = t / T_{\text{max}}$（$T_{\text{max}}=112$）（Section 2.4）。

**3. 实验上下文利用：从忽略元数据到记忆增强的上下文感知推理**

基线方法要么完全忽略实验元数据，要么仅在后期简单拼接。CP-Agent 采用**模块化记忆增强架构**：CP-CLIP 作为轻量级记忆检索器，从知识库中获取最可能的实验上下文；MLLM 作为策略层，动态路由任务至可互换的专用智能体（CPContext Agent、ChannelSeg Agent、CellFeat Agent、FeatRank Agent、StatSynth Agent、ReportGen Agent），实现感知、检索、分析和报告生成的协调统一（Section 2.5）。

### 核心洞察

将实验上下文编码为连续数值嵌入，并与细胞绘画图像在统一对比学习框架中对齐，可显著提升化合物识别和机制推断的准确性。决定性证据包括：

- **化合物分类 Macro-avg F1 = 0.896**（CP-CLIP ViT-B/16 descriptor），而最佳通用 MLLM（Grok-4）仅为 0.102，甚至低于随机基线 0.10（Table 2）。
- **掩码消融实验**：掩码化合物名称和 MoA 后，文本到图像 R@1 从 98.70 暴跌至 3.50（相对下降 96.45%），证明模型并非依赖元数据相关性，而是学习了化合物特异性信息（Table 17）。
- **未见药物泛化**：CP-CLIP 平均余弦相似度较基线 CLIP 绝对提升 14.6%（0.432 vs 0.286），表现出强泛化能力（Table 3）。

### 证据强度与局限

上述创新点在化合物分类、零样本匹配和消融实验中均有高置信度证据支撑（confidence ≥ 0.95）。但需注意：当前验证仅限于三组公开 Cell Painting 数据集（BBBC021、CPJUMP1、RxRx3），更大规模的跨机构验证尚需进行；CP-Agent 的报告质量高度依赖底层 LLM 的推理能力，复杂机制下仍可能出现幻觉。



![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_7BLnSeWuei/figures/002_Figure_1.jpg]]
*Figure 1: Illustration of the CP-agent (top) and CP-CLIP (bottom). CP-Agent connects perception, memory retrieval, and modular analysis into a unified pipeline for generating reports for Cell Painting experiments. CP-CLIP forms the backbone of the CP-Agent’s perception module, providing joint embeddings of Cell Painting images and structured experimental context*

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_7BLnSeWuei/figures/003_Figure_2.jpg]]
*Figure 2: Automated cell-phenotype assessment pipeline of CP-Agent. Upon user query, CP-CLIP retrieves the relevant experimental context to guide cell segmentation and feature extraction. Downstream agents then rank morphological changes and generate interpretable, end-to-end phenotype reports*

CP-Agent 采用模块化、记忆增强的架构，将感知、检索、分析和报告生成解耦为专用智能体，形成单次推理流水线（图 1 顶部，图 2）。系统入口是用户提供的 Cell Painting 荧光图像；轻量级记忆检索器 **CP-CLIP** 首先从预构建的知识库中匹配最可能的实验上下文（化合物身份、浓度、处理时间），随后将标准化元数据分发给下游工具。

### 流水线模块与职责

CP-Agent 的核心流水线由六个专用智能体串联而成，各模块职责明确，输入输出边界清晰：

1. **CPContext Agent**：利用预训练的 CP-CLIP 检索器获取实验上下文，并将化合物描述符、浓度、时间等结构化元数据标准化为统一格式，作为后续推理的锚定信息。

2. **ChannelSeg Agent**：接收上下文指导，对 DNA 染色通道执行核实例分割，对非 DNA 通道（如 Actin、ER、Mito）执行全细胞分割，输出通道特异性掩码。该模块的细胞分割参数由 CellProfiler 管道配置（表 5、表 6 定义了 DNA 和 Actin 通道的测量特征模块）。

3. **CellFeat Agent**：基于分割掩码，调用配置好的 CellProfiler 管道提取单细胞特征，涵盖形态、强度、纹理、粒度、邻域和占据特征等维度。

4. **FeatRank Agent**：根据扰动可能性对提取的特征进行评分排序，识别最可能受扰动影响的 Top-K 特征，生成带置信度权重的特征重要性排序。在温度 0 下运行 30 次，选出的 Top-5 特征完全一致，表明排序高度稳定。

5. **StatSynth Agent**：计算对照与扰动样本间的统计证据，包括分布偏移、效应量（Cliff's delta）、Bootstrap 置信区间和统计显著性。该模块使用的统计参数体系由表 10（样本量定义）和表 11（18 个特征级统计指标定义，含中位数、MAD、分位数、delta median 等）规范化。

6. **ReportGen Agent**：整合统计摘要、排序特征和实验上下文，调用底层 MLLM 生成结构化报告，包含机制推断与后续实验建议。

### 核心感知模块：CP-CLIP

CP-CLIP 是整个系统的感知骨干（图 1 底部）。它在标准 CLIP 架构基础上引入两项关键设计：

- **图像分支**：将扰动图像与匹配的对照图像沿通道维度拼接为双通道输入 $\hat{x} = \text{concat}(x_p, \dot{x}_c) \in \mathbb{R}^{512 \times 512 \times 2}$，使模型显式感知扰动前后的形态差异。
- **文本分支**：采用混合序列编码，将标准子词嵌入与结构化上下文嵌入交替排列。化合物描述符、浓度、时间分别通过专用 MLP 映射为与文本嵌入同维度的连续向量 $e_{cmpd}, e_{conc}, e_{time}$，插入占位符 `<CMPD>`、`<CONC>`、`<TIME>` 位置，形成融合序列 $X = [CLS, t_1, ..., e_{cmpd}, ..., e_{conc}, ..., e_{time}, ...]$。

CP-CLIP 在 184.6 万对图像-上下文对上预训练，采用对称 InfoNCE 损失 $\mathcal{L}_{\text{InfoNCE}}$ 优化图像-文本对齐。训练完成后，其联合嵌入空间可直接支撑检索式推理：通过计算图像嵌入与候选文本提示的余弦相似度进行化合物分类和未见药物匹配。

### 智能体协调机制

MLLM 作为策略层，动态将任务路由至可互换的工具智能体，并整合其输出。CP-CLIP 的嵌入表示作为感知层的统一接口，同时为记忆检索提供语义锚点——CPContext Agent 通过检索最相似的实验上下文来初始化整个分析流水线。这种“感知-检索-分析-报告”的模块化设计使得各组件可独立升级（如替换分割算法或特征提取器），而无需改变整体架构。



### CP-CLIP：上下文感知的多模态对齐核心

CP-Agent 的感知基础是 **CP-CLIP**，它在标准 CLIP 框架上进行了两项关键改造，将实验上下文编码为连续嵌入并与细胞图像联合对齐。

**图像分支改造**：传统方法仅输入单幅扰动图像，CP-CLIP 将扰动图像 $x_p$ 与匹配的对照图像 $x_c$ 沿通道维度拼接，形成双通道输入：

$$\hat{x} = \text{concat}(x_p, x_c) \in \mathbb{R}^{512 \times 512 \times 2}$$

这一设计使模型能够直接学习扰动相对于对照的差异信号，而非孤立的形态特征。

**文本分支改造**：CP-CLIP 的核心创新在于将结构化实验元数据注入文本编码器。具体而言，系统为三类关键上下文引入专用占位符 token——`<CMPD>`（化合物描述符）、`<CONC>`（浓度）、`<TIME>`（时间点），并通过领域特定的轻量级 MLP 将数值特征映射为与子词嵌入同维度的连续向量。

化合物描述符编码方面，每个分子通过 RDKit 提取 174 维 2D 描述符，经固定维度映射 $f_{\mathrm{desc}}: \mathcal{X} \to \mathbb{R}^d$ 后，对各特征维度独立进行 z-score 标准化，得到 $z_{\mathrm{cmpd}}$。

浓度编码采用归一化给药对 $[\rho_{\mathrm{max}}, s(C)]$。其中最大质量浓度将分子量与标称最大浓度统一到物理量纲：

$$\rho_{\mathrm{max}} [\mathrm{mg/mL}] := \frac{M [\mathrm{Da}] \cdot C_{\mathrm{max}} [\mu\mathrm{M}]}{10^6}$$

对数剂量步索引反映 2 倍连续稀释方案下的相对位置（$\Delta \log = 0.5$）：

$$s(C) := \frac{\log_{10}(C_{\mathrm{max}}) - \log_{10}(C)}{\Delta \log}$$

时间编码通过归一化缩放至单位区间：$\tilde{t} = \frac{t}{T_{\mathrm{max}}}$，其中 $T_{\mathrm{max}} = 112$ 小时。

三类上下文的嵌入由专用 MLP 动态计算：

$$e_{\mathrm{cmpd}} = f_{\mathrm{cmpd}}(z_{\mathrm{cmpd}}) \in \mathbb{R}^D$$

$$e_{\mathrm{conc}} = f_{\mathrm{conc}}([\rho_{\mathrm{max}}, s(C)]) \in \mathbb{R}^D$$

$$e_{\mathrm{time}} = f_{\mathrm{time}}(\tilde{t}) \in \mathbb{R}^D$$

最终，标准子词嵌入 $t_i$ 与结构化嵌入交替排列，构成混合文本序列输入：

$$X = [\mathrm{CLS}, t_1, t_2, \dotsc, \underbrace{e_{\mathrm{cmpd}}}_{<\mathrm{CMPD}>}, \dotsc, \underbrace{e_{\mathrm{conc}}}_{<\mathrm{CONC}>}, \dotsc, \underbrace{e_{\mathrm{time}}}_{<\mathrm{TIME}>}, \dotsc]$$

训练采用对称 InfoNCE 损失，鼓励匹配的图像-文本对具有高余弦相似度：

$$\mathcal{L}_{\mathrm{InfoNCE}} = \frac{1}{2N} \sum_{k=1}^{N} [\ell_{\mathrm{CE}}(S_{it}^{(k,;)}, y_k) + \ell_{\mathrm{CE}}(S_{ti}^{(k,;)}, y_k)]$$

CP-CLIP 在 1,846,436 对图像-文本数据上预训练，验证集包含 9,395 对（Table 1）。

### CP-Agent：模块化多智能体推理架构

CP-Agent 采用模块化、记忆增强的架构，将感知、检索、分析和报告分离为六个专用智能体，由 MLLM 作为策略层动态路由任务并整合输出（Figure 1, Figure 2）。

**CPContext Agent**：利用预训练 CP-CLIP 作为检索器，从知识库中获取最可能的实验上下文并标准化元数据，为下游分析提供条件信息。

**ChannelSeg Agent**：对 DNA 染色通道进行核实例分割，对非 DNA 通道进行全细胞分割，输出通道特异性掩码。

**CellFeat Agent**：基于配置好的 CellProfiler 管道，提取单细胞的形态、强度、纹理、粒度、邻域及占据特征。

**FeatRank Agent**：根据扰动可能性对特征评分排序，生成带置信度的解释。消融实验表明，在温度 0 下运行 30 次，选出的 Top-5 特征完全一致（Table 15），特征排序高度稳定。

**StatSynth Agent**：计算对照与扰动间的统计证据，汇总分布偏移、效应量、置信区间及统计显著性，为 LLM 推理提供定量基础。

**ReportGen Agent**：整合统计摘要、排序特征和实验上下文，生成包含机制推断与后续建议的结构化报告。

### 关键设计决策的证据支撑

消融实验揭示了各上下文组件的相对重要性。掩码化合物名称和 MoA 导致文本到图像 R@1 从 98.70 暴跌至 3.50（相对下降 96.45%），证明模型高度依赖化合物特异性信息而非元数据相关性。掩码浓度导致 R@1 下降约 42%，掩码时间仅下降约 6%，表明浓度信息具有中等重要性，时间信息贡献较小（Table 17）。在反事实提示下，CP-CLIP 的浓度分类 F1 较 CLIP 提升 50.55%，时间分类 F1 提升 35.23%，进一步证实模型学到了鲁棒的多模态关联（Table 20, Table 21）。连续描述符编码在化合物分类（F1: 0.896 vs 0.887）和未见药物匹配（相似度: 0.432 vs 0.360）上均优于二进制指纹编码（Table 2, Table 3）。



## 实验与关键发现

### 核心发现：CP-CLIP 在化合物识别上远超通用 MLLM

Table 2 的主实验结果揭示了一个关键瓶颈：通用多模态大模型在细胞形态学分类任务上几乎完全失效。在 10 类已知药物的化合物分类任务中，表现最佳的通用 MLLM **Grok-4** 仅达到 Macro-avg F1 = 0.102，与随机猜测基线（0.10）无显著差异；而 **CP-CLIP ViT-B/16 (descriptor)** 达到 **0.896**，绝对提升 0.794（Table 2）。这一巨大差距表明，当前通用 MLLM 缺乏对实验上下文（化合物特性、剂量、时间）的结构化编码能力，无法从高内涵图像中提取药理学相关的形态学信号。

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_7BLnSeWuei/figures/004_Table_2.jpg]]
*Table 2: Model performance on classification tasks*

CP-CLIP 的优势不仅限于化合物识别。在细胞系分类上，CP-CLIP ViT-B/16 (descriptor) 的 F1 达到 0.887，而 Gemini-2.5-Pro 仅为 0.526；在通道预测任务上，CP-CLIP 同样以 0.858 显著优于 MLLM 基线（Table 2）。这验证了 CP-CLIP 的联合嵌入策略——将结构化实验上下文编码为连续嵌入并与图像对齐——是解决该瓶颈的关键因果机制。

### 零样本泛化：未见药物匹配

Table 3 的零样本评估进一步验证了 CP-CLIP 的泛化能力。在未见药物匹配任务上，CP-CLIP ViT-B/16 (descriptor) 的平均余弦相似度达到 **0.432**，较基线 CLIP ViT-B/16 的 0.286 绝对提升 14.6%。值得注意的是，连续描述符编码（descriptor）一致优于二进制指纹编码（fingerprint）：未见药物匹配相似度分别为 0.432 vs 0.360，化合物分类 F1 分别为 0.896 vs 0.887（Table 2, Table 3）。这表明 RDKit 2D 描述符提供的丰富分子表征比稀疏指纹更适合与图像特征对齐。

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_7BLnSeWuei/figures/005_Table_3.jpg]]
*Table 3: Unseen drugs similarity score*

缩放视觉编码器也带来增益：ViT-L/16 (descriptor) 将未见药物相似度进一步提升至 0.444，但边际收益递减（相对 ViT-B/16 仅提升 2.8%），说明当前瓶颈更多在于上下文编码策略而非视觉骨干容量。

### 消融实验：上下文信息的因果贡献

Table 17 的掩码消融实验直接量化了各上下文字段对模型性能的因果贡献：

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_7BLnSeWuei/figures/103_Table_17.jpg]]
*Table 17: Retrieval performance before and after masking different textual components*

- **掩码化合物名称和 MoA** 导致文本到图像 R@1 从 **98.70 暴跌至 3.50**（相对下降 96.45%），图像到文本 R@1 从 98.70 降至 3.30。这一极端降幅证明 CP-CLIP 并非依赖数据集中的元数据相关性，而是真正学习了化合物特异性的形态学表征。
- **掩码浓度** 导致 R@1 下降约 42%，表明剂量信息具有中等重要性，与药理学中剂量-响应关系一致。
- **掩码时间** 仅导致 R@1 下降约 6%，说明在当前数据分布下，时间点信息对形态学变化的区分贡献有限，可能因为数据集中的时间跨度不足以产生显著的形态学漂移。

### 反事实鲁棒性验证

Table 20 和 Table 21 的反事实提示实验进一步排除了“元数据相关性假象”。当故意干扰其他元数据字段（如给定错误浓度或时间提示）时，CP-CLIP 的浓度分类 F1 较 CLIP 提升 **50.55%**，时间分类 F1 提升 **35.23%**。这表明 CP-CLIP 学得的是鲁棒的多模态关联，而非简单的元数据模式匹配。

### CP-Agent 推理稳定性

在智能体层面，FeatRank Agent 的重复性测试（Table 15）显示：在温度 0 下运行 30 次，选出的 Top-5 特征完全一致，表明特征排序逻辑高度稳定。然而，当温度非零时，报告生成的一致性有所下降，这是当前基于 LLM 的推理模块的主要脆弱点——报告质量对解码策略敏感，复杂机制或极端剂量下仍可能出现幻觉（见局限性讨论）。

### 嵌入可视化与剂量响应

Figure 3 的 UMAP 可视化提供了定性证据：CP-CLIP 的图像嵌入按化合物身份（Figure 3a）和作用机制（MoA, Figure 3b）形成清晰聚类，说明学得的表征编码了生物学相关的形态学信息。Figure 3c 进一步展示了剂量依赖的形态学变化模式，嵌入随浓度梯度呈现有序漂移，验证了浓度编码的有效性。

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_7BLnSeWuei/figures/011_Figure_3.jpg]]
*Figure 3: CP-CLIP captures pharmacologically meaningful morphology. UMAP projections of CP-CLIP image embeddings, colored by (a) compound identity and (b) mechanism of action (MoA). The clear clustering indicates that the learned representation encodes biologically relevant morphology. (c) Concentrationdependent morphological changes are captured using image embeddings extracted from samples treated with varying compound doses*

### 上下文到图像检索

Table 23 的检索实验显示，CP-CLIP ViT-B/16 (descriptor) 的上下文到图像 R@1 达到 **77.09**，较 CLIP ViT-B/16 的 66.80 提升 10.29 个百分点。这表明联合嵌入空间不仅支持图像到文本的匹配，也支持反向检索，为 CP-Agent 中的 CPContext Agent 提供了检索基础。

### 失败模式与局限

尽管 CP-CLIP 在化合物分类上表现优异，但以下失败模式值得关注：

1. **小样本统计效力不足**：StatSynth Agent 依赖对照与扰动组的分布比较，当样本量较小时，效应量估计的置信区间过宽，可能导致 FeatRank Agent 的错误特征排序和后续机制归因偏差。
2. **复杂机制的幻觉风险**：ReportGen Agent 在 BGT226（PI3K/mTOR 双靶点抑制剂）等复合机制药物上，生成的机制推断可能出现过度简化或部分错误（Figure 4 案例），需人工审核。
3. **特征提取的覆盖盲区**：当前 CellFeat Agent 基于传统 CellProfiler 管道，可能遗漏深度视觉特征（如纹理的层次化模式），这限制了可解释特征的完备性。
4. **时间维度利用不足**：消融实验显示时间信息贡献仅约 6%，说明当前编码策略未能充分捕捉时间序列中的形态学动态变化，这可能是未来改进方向。



## 定位与知识库关联

### 核心创新与因果机制

现有细胞形态学分析流程长期存在一个关键瓶颈：**实验上下文（细胞系、化合物浓度、处理时间等）被系统性忽略或仅作为后期元数据简单拼接**，导致形态学响应建模不准确、跨实验泛化能力差，且缺乏语义可解释性。CP-Agent 的核心洞察在于：将结构化实验上下文编码为连续数值嵌入，并与细胞绘画图像在统一对比学习框架中对齐，可显著提升化合物识别和机制推断的准确性。

这一洞察的实现依赖于两个因果调节旋钮：
1. **上下文感知的联合嵌入**：CP-CLIP 将化合物描述符、浓度、时间等结构化元数据通过专用 MLP 编码为连续嵌入，与图像在对称 InfoNCE 损失下联合对齐，使模型学习到“该化合物在此浓度和时间下应产生何种形态”的因果关联，而非表面的元数据相关性。
2. **模块化智能体推理**：CP-Agent 将感知、检索、分析、报告分离为六个专用智能体（CPContext、ChannelSeg、CellFeat、FeatRank、StatSynth、ReportGen），以 MLLM 作为策略层动态路由任务，实现从原始图像到可解释机制报告的单次流水线。

### 方法谱系定位

#### 与通用视觉-语言模型的对比

CP-CLIP 直接对标 CLIP（Radford et al., 2021）和 SigLIP（Zhai et al., 2023）等通用对比学习框架，但在输入空间上进行了关键改造：

| 维度 | 基线方法 | CP-CLIP 改造 |
|------|----------|--------------|
| 图像输入 | 单幅扰动图像 | 扰动图像与匹配对照图像沿通道维度拼接（$ \hat{x} = \text{concat}(x_p, x_c) \in \mathbb{R}^{512 \times 512 \times 2} $） |
| 文本编码 | 仅自然语言子词嵌入 | 混合序列：标准子词嵌入与结构化上下文嵌入（`<CMPD>`、`<CONC>`、`<TIME>`）融合 |
| 上下文利用 | 忽略 | 联合嵌入图像和结构化元数据，作为智能体记忆检索与推理的基础 |

这一改造的效果具有决定性证据支持：在化合物分类任务上，CP-CLIP ViT-B/16（descriptor）达到 Macro-avg F1=0.896，而最佳通用 MLLM（Grok-4）仅 0.102，甚至低于随机基线 0.10（Table 2）。在零样本未见药物匹配上，CP-CLIP 的平均余弦相似度较基线 CLIP 绝对提升 14.6%（0.432 vs 0.286，Table 3）。

#### 与通用多模态大语言模型的对比

论文系统评估了 Grok-4（xAI, 2025）、GPT-5（OpenAI, 2025）、Claude-4-Sonnet（Anthropic, 2025）、Gemini-2.5-Pro（Google DeepMind, 2025）等前沿 MLLM。这些模型在化合物分类上表现极差（F1 均不超过 0.102），根本原因在于：通用 MLLM 缺乏对 Cell Painting 荧光图像的领域特定感知能力，且无法有效利用实验上下文进行跨条件对齐。CP-Agent 通过预训练的 CP-CLIP 作为感知骨干，弥补了这一鸿沟。

#### 与分子-图像对比学习方法的对比

CP-CLIP 与 CLOOME 等分子-图像对比学习方法同属一个谱系，但关键差异在于：CLOOME 主要关注分子结构与图像的对齐，而 CP-CLIP 将对齐空间扩展至**完整的实验上下文**（化合物 + 浓度 + 时间），使其能够捕捉剂量-响应和时间依赖的形态学变化（Figure 3c）。

### 适用边界与局限

**数据集覆盖范围有限**：CP-Agent 仅在三个公开 Cell Painting 数据集（BBBC021、CPJUMP1、RxRx3）上验证，涵盖的扰动类型和细胞系多样性有限。更大规模的跨机构验证（如 JUMP-CP 联盟的全量数据）尚需进行。

**报告质量依赖底层 LLM**：CP-Agent 的报告生成高度依赖底层 MLLM 的推理能力。在复杂机制或非典型剂量下，仍可能出现幻觉或推理错误。论文报告显示，在非零温度下报告一致性有所下降。

**特征提取受限于传统管道**：当前 CellFeat Agent 基于 CellProfiler 提取手工特征，可能遗漏深度视觉特征。尚未整合组学数据或文本知识图谱等多模态信息以进一步提高机制分辨力。

**剂量-响应分析不完整**：剂量-响应分析仅限于部分化合物，缺乏完整的浓度梯度和时间序列实验来确认机制特异性。

### 关键消融发现与证据强度

1. **掩码化合物名称和 MoA 导致文本到图像 R@1 从 98.70 暴跌至 3.50**（相对下降 96.45%，Table 17），证明模型并非依赖元数据相关性，而是学习了化合物特异性信息。**证据强度：强**。

2. **掩码浓度导致 R@1 下降约 42%，掩码时间仅下降约 6%**（Table 17），说明浓度信息具有中等重要性，而时间信息在当前数据中贡献较小。**证据强度：中等**，时间维度的低贡献可能与数据集中时间点覆盖不足有关。

3. **在反事实提示下（干扰其他元数据），CP-CLIP 的浓度分类 F1 较 CLIP 提升 50.55%**（Table 20-21），表明模型学得鲁棒的多模态关联，而非依赖表面相关性。**证据强度：强**。

4. **连续描述符编码优于二进制指纹编码**：化合物分类 F1 分别为 0.896 vs 0.887，未见药物匹配相似度 0.432 vs 0.360（Table 2-3）。**证据强度：中等**，差异幅度较小但方向一致。

5. **FeatRank Agent 在温度 0 下运行 30 次，Top-5 特征完全一致**（Table 15），表明特征排序高度稳定。**证据强度：强**，但仅在温度 0 下验证，非零温度下的鲁棒性仍需进一步评估。

### 开放问题

1. **扰动类型扩展**：如何将 CP-Agent 扩展至遗传扰动（如 CRISPR 敲除）、组合药物处理等更广泛的扰动类型和细胞状态？

2. **规模泛化验证**：在更大规模、更多样化的 Cell Painting 数据集（如 JUMP-CP 全量）上，CP-CLIP 的上下文感知优势是否依然显著？

3. **多模态整合**：能否将 CP-Agent 与高通量测序数据（如转录组学 L1000）整合，利用跨模态约束进一步提高机制分辨力？

4. **自动化验证闭环**：对于 CP-Agent 生成的机制假设，如何设计自动化的后续实验验证闭环（如推荐验证性染色或剂量-响应实验）？

5. **小样本统计推断**：在统计效力不足时（如罕见扰动仅有少量重复），如何避免 FeatRank 和 StatSynth 产生错误的机制归因？



## 原文 PDF

![[paperPDFs/ICLR_2026/CP_Agent_ContextAware_Multimodal_Reasoning_for_Cellular_Morphological_Profiling_under_Chemical_Perturbations.pdf]]
