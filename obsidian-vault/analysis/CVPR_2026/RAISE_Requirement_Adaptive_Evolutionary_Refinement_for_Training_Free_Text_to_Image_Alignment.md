---
title: "RAISE: Requirement-Adaptive Evolutionary Refinement for Training-Free Text-to-Image Alignment"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/RAISE_Requirement_Adaptive_Evolutionary_Refinement_for_Training_Free_Text_to_Image_Alignment.pdf
project_link: null
code_link: "https://github.com/LiyaoJiang1998/RAISE"
aliases:
- RAISE
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/representation_self_supervised_transfer
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 引入需求驱动的自适应缩放机制，通过分析器动态提取未满足的语义需求，并仅在需求未达标时分配额外计算，从而将计算量与提示难度对齐，使得进化过程能够持续收敛。
primary_logic: 将文本到图像对齐形式化为需求驱动的自适应进化过程，通过并行多动作变异（提示重写、噪声重采样、指令式编辑）扩大搜索空间，并利用工具辅助验证（检测、深度估计、描述）形成“分析-精化-验证”闭环，实现无需训练的推理时自改进。
claims:
- RAISE在GenEval上取得0.94的总体分数，超过所有训练无关和基于训练的推理时缩放方法，包括ReflectionFlow (0.91) 和 Qwen-Image-RL (0.91)。
- RAISE以平均18.6个生成样本和7.3次VLM调用实现上述性能，相比ReflectionFlow样本减少41.9%，VLM调用减少88.6%。
- RAISE在多轮缩放中保持性能-效率帕累托前沿，随着采样预算增加持续提升GenEval分数，而其他基线趋于饱和或下降。
- 消融实验表明，工具辅助验证和指令式编辑对属性绑定、颜色等细粒度对齐类别至关重要，移除后性能下降。
---

# RAISE: Requirement-Adaptive Evolutionary Refinement for Training-Free Text-to-Image Alignment

> [!tip] 核心洞察
> 将文本到图像对齐形式化为需求驱动的自适应进化过程，通过并行多动作变异（提示重写、噪声重采样、指令式编辑）扩大搜索空间，并利用工具辅助验证（检测、深度估计、描述）形成“分析-精化-验证”闭环，实现无需训练的推理时自改进。

| 字段 | 内容 |
|------|------|
| 中文题名 | RAISE：需求自适应的免训练进化精化方法用于文本到图像对齐 |
| 英文题名 | RAISE: Requirement-Adaptive Evolutionary Refinement for Training-Free Text-to-Image Alignment |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.00483) · [Code](https://github.com/LiyaoJiang1998/RAISE) |
| Topic | #topic/vision_multimodal_applications #topic/representation_self_supervised_transfer #topic/vision_multimodal_applications/image_and_video_generation |
| Method | RAISE |
| Dataset | GenEval, DrawBench |

> [!tip] 效果简介
> - GenEval 上，Overall Score 0.94 vs 0.91 (ReflectionFlow / Qwen-Image-RL) (+0.03)；Counting 0.95 vs 0.93 (Qwen-Image-RL) (+0.02)；Colors 0.98 vs 0.95 (ReflectionFlow) (+0.03)。
> - DrawBench 上，VQAScore 0.885 vs 0.844 (ReflectionFlow) (+0.041)。

## 概要

文本到图像生成模型在遵循复杂提示方面仍存在显著对齐瓶颈：现有免训练的推理时缩放方法（如噪声重采样、提示重写）依赖固定的迭代预算或阈值，无法根据提示的语义复杂度动态分配计算量，导致多轮精化效果停滞甚至下降。RAISE 将文本到图像对齐形式化为**需求驱动的自适应进化过程**，通过并行多动作变异（提示重写、噪声重采样、指令式编辑）扩大搜索空间，并利用工具辅助验证（检测、深度估计、描述）形成“分析—精化—验证”闭环，实现无需训练的推理时自改进。

核心结论：RAISE 在 GenEval 上取得 **0.94** 的总体分数，超过所有训练无关和基于训练的推理时缩放方法（包括 ReflectionFlow 的 0.91 和 Qwen-Image-RL 的 0.91），同时平均仅生成 18.6 个样本、调用 7.3 次 VLM——相比 ReflectionFlow 样本减少 41.9%，VLM 调用减少 88.6%。在多轮缩放中，RAISE 保持性能-效率帕累托前沿，随着采样预算增加持续提升 GenEval 分数，而其他基线趋于饱和或下降。消融实验表明，工具辅助验证和指令式编辑对属性绑定、颜色等细粒度对齐类别至关重要。

### 文本到图像生成的推理时缩放瓶颈

文本到图像（T2I）扩散模型近年来取得了显著进展，但即使是最先进的模型，在复杂提示下仍会出现属性绑定错误、计数不准确和空间关系混乱等问题。为提升生成质量，推理时缩放（inference-time scaling）方法通过增加推理阶段的计算量来精化输出，已成为一条重要的研究路径。

然而，现有的推理时缩放方法存在一个根本性瓶颈：**固定的计算预算与提示难度不匹配**。无论是基于噪声重采样的随机搜索（如Noise Scaling），还是基于提示重写的迭代精化（如TIR），抑或是基于反射微调的训练方法（如ReflectionFlow），它们都使用预设的迭代轮数或固定的分数阈值来决定何时停止。这种“一刀切”的策略导致两个问题：对简单提示，系统浪费计算资源做无效迭代；对困难提示，固定的预算又不足以收敛到满意结果。更严重的是，多轮精化往往出现**效果停滞甚至下降**的现象——额外计算投入不再带来对齐质量的提升，系统缺乏真正的自改进能力。

### 现有方法的缺口

当前推理时缩放方法可大致分为三类，各有局限：

- **训练无关的随机搜索**（如噪声重采样）：仅通过重采初始噪声生成多样本，缺乏对未满足需求的感知，搜索效率低，多轮扩展后性能饱和。
- **代理式提示重写**（如T2I-Copilot）：通过VLM改写提示来引导生成，但动作空间单一（仅重写提示），无法纠正已生成图像中的细粒度错误，且缺乏结构化的验证机制。
- **基于训练的反射微调**（如ReflectionFlow）：需要额外训练反射模型，泛化性受限，且其迭代过程仍依赖固定轮数，计算开销大（ReflectionFlow平均需32个生成样本和64次VLM调用）。

这些方法的共同缺陷在于：**缺乏对提示语义复杂度的动态感知**，无法根据实际需求满足情况自适应地分配计算资源，也难以形成“分析-精化-验证”的闭环自改进。

### 本文动机

针对上述瓶颈，本文提出核心问题：**能否设计一种需求驱动的自适应推理时缩放机制，使计算量与提示难度对齐，并通过多动作进化实现持续的推理时自改进？**

本文的动机源于一个关键洞察：文本到图像对齐本质上可以形式化为一个**需求满足过程**——用户提示隐含着结构化的语义需求清单（如对象存在性、属性绑定、空间关系、计数等），生成图像的质量取决于这些需求的满足程度。如果能动态提取未满足的需求，并仅在需求未达标时分配额外计算，就能实现真正的自适应缩放。同时，引入进化算法中的并行多动作变异（提示重写、噪声重采样、指令式编辑）可以扩大搜索空间，配合基于视觉工具的证明式验证，形成“分析-精化-验证”的闭环，使系统在无需训练的条件下持续收敛。

基于此，本文提出RAISE（Requirement-Adaptive Evolutionary Refinement），一个免训练的、需求驱动的自适应进化精化框架，旨在以更少的生成样本和VLM调用实现更优的文本到图像对齐。

## 核心方法与创新机理

RAISE 的核心创新在于将文本到图像对齐重新形式化为**需求驱动的自适应进化过程**，通过三个相互协同的机制突破现有推理时缩放方法的瓶颈。

### 瓶颈洞察：固定预算无法匹配语义复杂度

现有训练无关的推理时缩放方法（如噪声重采样、提示重写）采用固定的迭代轮数或分数阈值作为停止准则，缺乏对提示语义复杂度的感知能力。这导致两类典型失效模式：简单提示在需求已满足后仍浪费计算资源，而困难提示在多轮精化后性能趋于饱和甚至下降——系统无法判断何时真正“完成”，也无法将计算量向未满足的语义需求倾斜。RAISE 的核心洞察是：**推理时缩放的有效性取决于计算量是否与提示的语义需求对齐**，而非简单地堆叠迭代轮数。

### 关键机制一：需求驱动的自适应缩放

RAISE 引入**需求分析器（Analyzer）**作为自适应缩放的决策核心。分析器从用户提示中提取结构化的需求清单 $\mathcal{R}_i$，并基于上一轮的验证反馈 $\mathcal{F}_{i-1}^*$ 将需求划分为已满足子集 $\mathcal{R}_i^+$ 和未满足子集 $\mathcal{R}_i^-$，同时输出二进制决策变量 $d_i^{\mathrm{analyzer}} \in \{\text{END}, \text{CONTINUE}\}$：

$$O_i^{\mathrm{analyzer}} = \mathcal{A}_{\mathrm{analyzer}}(x_{\mathrm{user}}, y_{i-1}^*, x_{i-1}^*, \mathcal{F}_{i-1}^*, x_{i-1}', \mathcal{F}_{i-1}') = (\mathcal{R}_i, \mathcal{R}_i^+, \mathcal{R}_i^-, Q_i, d_i^{\mathrm{analyzer}})$$

这一机制实现了**计算量的语义级分配**：仅当分析器判定主要需求未满足（$d_i^{\mathrm{analyzer}} = \text{CONTINUE}$）且校验器的全局决策 $d_i^{\mathrm{verifier}}$ 为 False 时，系统才启动新一轮精化。双重停止信号确保了缩放过程不会过早终止或无限循环，使计算预算与提示难度自然对齐。实验证据表明，RAISE 在 GenEval 上以平均 **18.6 个生成样本**和 **7.3 次 VLM 调用**即达到 0.94 的总体分数，相比 ReflectionFlow 样本减少 41.9%，VLM 调用减少 88.6%（Table 1），且在多轮缩放中持续提升性能而非饱和（Figure 4）。

### 关键机制二：并行多动作变异扩大搜索空间

与现有方法仅依赖单一精化动作（如仅重写提示或仅重采样噪声）不同，RAISE 在每轮进化中并行执行三类变异操作：

- **重采样（Resampling）**：$m_{i,j}^{\mathrm{resample}}(c_{i-1}^*) = (\epsilon_{i,j}, x_{\mathrm{user}}, \emptyset)$，通过重采样初始噪声探索同一提示下的不同视觉配置；
- **提示重写（Prompt Rewriting）**：由重写器根据未满足需求 $\mathcal{R}_i^-$ 生成改写提示 $x_i^{\mathrm{rewrite}}$，引导扩散模型聚焦于缺失语义；
- **指令式编辑（Instructional Editing）**：针对已生成图像中特定未满足需求，生成编辑指令直接修改图像内容，避免从头生成带来的语义漂移。

三种变异并行作用于父代候选 $c_{i-1}^*$，生成多样化的子代种群。消融实验（Table 3）显示，禁用指令式编辑后属性绑定从 0.87 降至 0.83，证明编辑变异对纠正细粒度需求不可或缺。

### 关键机制三：工具辅助的结构化验证闭环

RAISE 将验证从简单的 VLM 评分升级为**基于视觉工具的证明式验证**。校验器（Verifier）首先调用检测、深度估计、描述等离线视觉工具，从图像中提取对象实体、属性和空间关系的结构化文本证据 $G_i'$，然后基于这些证据对分析器生成的二元问题集 $\mathcal{Q}_i$ 逐一回答：

$$\mathcal{V}_i = \{v_{i,k} = (q_{i,k}, a_{i,k}, e_{i,k}) \mid a_{i,k} \in \{\text{Yes}, \text{No}\}\}$$

每个验证三元组包含问题、是/否答案和解释，最终汇总为全局决策 $d_i^{\mathrm{verifier}}$。工具证据弥补了纯 VLM 推理在视觉感知上的不足，使验证结果具有可追溯的因果链。消融实验（Table 3）证实，移除视觉工具后属性绑定（0.84 vs 0.87）和颜色（0.96 vs 0.98）显著下降，表明工具辅助验证对细粒度对齐类别至关重要。

### 创新总结：从固定缩放到自适应进化

RAISE 通过上述三个 changed slots——**需求驱动的自适应停止准则**替代固定预算、**并行多动作变异**替代单一精化路径、**工具辅助的结构化验证**替代简单评分——将推理时缩放从“盲目重试”升级为“感知需求的自改进闭环”。这一范式转换使 RAISE 在 GenEval 上达到 0.94 的 SOTA 分数（Table 1），同时在性能-效率帕累托前沿上持续领先（Figure 4），验证了**将计算量与语义需求对齐**这一核心主张的有效性。

RAISE 是一个免训练的、以需求为驱动的自适应进化缩放框架，用于文本到图像（T2I）生成。其核心思想是将图像生成形式化为一个推理时的种群进化过程：系统在每一轮中通过多种变异动作并行生成候选图像，并利用结构化的需求验证机制动态评估对齐程度，仅在未满足需求上追加计算，从而实现计算预算与提示难度的自适应匹配。

### 多智能体协作架构

RAISE 构建为一个三智能体协作系统，三个智能体共享同一个 VLM 骨干网络（默认使用 Mistral-Small-3.2-24B-Instruct-2506），各司其职：

1. **需求分析器（Analyzer）**：从用户提示中提取结构化的需求清单，并基于上一轮的验证反馈动态更新需求状态。其输出包含完整需求集 $\mathcal{R}_i$、已满足需求子集 $\mathcal{R}_i^+$、未满足需求子集 $\mathcal{R}_i^-$、一组二元验证问题 $\mathcal{Q}_i$，以及一个决策变量 $d_i^{\text{analyzer}}$，用于判断是否已达到“结束”条件（主需求全部满足）。

2. **重写器（Rewriter）**：根据分析器输出的未满足需求，生成两种精化信号——改写后的 T2I 生成提示 $x_i^{\text{rewrite}}$，或针对已有图像的编辑指令（包含编辑提示和参考图像）。这为后续变异提供了文本侧的搜索方向。

3. **校验器（Verifier）**：对每一张生成的候选图像，利用离线视觉工具（目标检测、深度估计、图像描述）提取结构化的视觉证据 $\mathcal{G}_i'$，然后结合分析器给出的二元问题 $\mathcal{Q}_i$，逐一判定每个需求是否满足，输出验证三元组集合 $\mathcal{V}_i = \{v_{i,k} = (q_{i,k}, a_{i,k}, e_{i,k})\}$ 和一个全局决策变量 $d_i^{\text{verifier}}$。

### 进化精化主循环

框架的整体流程如 Figure 2 所示，每轮迭代包含“分析—变异—验证—选择”四个阶段：

![[assets/figures/papers/paper_list_l2339_https_arxiv_org_abs_2603_00483/figures/002_Figure_2.jpg]]
*Figure 2: Framework overview. RAISE employs diverse mutational refinement actions concurrently—including prompt rewriting, noise resampling, and instructional editing—to evolve candidates in each round. It operates as a multi-agent system composed of an analyzer, rewriter, and verifier: 1) Analyzer performs requirement analysis by extracting a structured and detailed checklist of prompt requirements based on user prompt and previous verification results; 2) Rewriter refines T2I generation prompts or produces image editing instructions to address unsatisfied requirements; 3) Verifier evaluates generated candidates via structured tool-grounded verification*

**阶段一：需求分析。** 分析器接收用户提示 $x_{\text{user}}$、上一轮的全局最优候选 $c_{i-1}^*$ 及其反馈 $\mathcal{F}_{i-1}^*$、上一轮的轮次最优候选 $c_{i-1}'$ 及其反馈 $\mathcal{F}_{i-1}'$，输出结构化的需求分析结果。若分析器判定主需求已满足（$d_i^{\text{analyzer}} = \text{“结束”}$），则触发停止信号。

**阶段二：多动作并行变异。** 以父代候选 $c_{i-1}^*$ 为基础，同时执行三种变异操作以扩大搜索空间：
- **噪声重采样**：保持原始用户提示不变，仅重新采样初始噪声 $\epsilon_{i,j} \sim \mathcal{N}(0, I)$，探索不同的视觉配置；
- **提示重写**：使用重写器生成的改写提示 $x_i^{\text{rewrite}}$ 替代原始提示，搭配新采样的噪声生成候选；
- **指令式编辑**：以重写器生成的编辑指令对参考图像进行定向修改，修正特定未满足需求。

三种变异并行产生 $n_i$ 个新候选，形成当前轮的候选种群。

**阶段三：工具辅助验证。** 对每个候选图像，先通过视觉工具提取接地证据，再由校验器根据证据和二元问题逐一判定需求满足情况。验证结果 $\mathcal{V}_i$ 和全局决策 $d_i^{\text{verifier}}$ 构成反馈信号 $\mathcal{F}_i'$，回传给下一轮的分析器。

**阶段四：适应度选择。** 使用对齐评分函数 $f(y_{i,j}, x_{\text{user}})$ 对所有候选打分，选出当前轮最优 $c_i'$ 和全局历史最优 $c_i^*$：
$$c_i^* = \arg\max_{c_{t,j}, t \le i} f(y_{t,j}, x_{\text{user}})$$

### 自适应停止机制

RAISE 不依赖固定的迭代次数或分数阈值，而是采用双重停止信号：分析器的“结束”判定（主需求满足）与校验器的 True 判定（所有需求满足）。当两者同时触发时，循环终止，输出全局最优候选 $c^*$ 对应的图像 $y^*$。这一机制使计算资源天然向困难提示倾斜——简单提示快速收敛，复杂提示获得更多轮精化，从而在性能与效率之间取得帕累托最优（见 Table 6 和 Figure 4）。

### 3.1 需求驱动的自适应缩放

RAISE 将文本到图像生成形式化为一个**需求驱动的自适应进化过程**。其核心控制变量是分析器输出的决策变量 $d_i^{\mathrm{analyzer}}$，它决定当前轮次是否终止缩放。这一机制使得计算量能够根据提示的语义复杂度动态分配——简单提示快速收敛，困难提示获得更多精化轮次。

**分析器（Analyzer）** 是自适应缩放的枢纽。它以用户提示、上一轮最优候选、上一轮校验反馈为输入，输出结构化的需求分析结果：

$$
O_i^{\mathrm{analyzer}} = \mathcal{A}_{\mathrm{analyzer}}(x_{\mathrm{user}}, y_{i-1}^*, x_{i-1}^*, \mathcal{F}_{i-1}^*, x_{i-1}', \mathcal{F}_{i-1}') = (\mathcal{R}_i, \mathcal{R}_i^+, \mathcal{R}_i^-, Q_i, d_i^{\mathrm{analyzer}})
$$

各变量含义如下：
- $\mathcal{R}_i$：第 $i$ 轮提取的完整需求清单（结构化文本）
- $\mathcal{R}_i^+$：已满足的需求子集
- $\mathcal{R}_i^-$：尚未满足的需求子集——这些将成为后续精化动作的目标
- $Q_i$：针对每个需求的二值验证问题集合，供校验器逐一判定
- $d_i^{\mathrm{analyzer}} \in \{\text{continue}, \text{end}\}$：分析器的“结束”信号，当主需求已满足时触发

全局最优候选的选择遵循适应度最大化原则：

$$
c_i^* = \arg\max_{c_{t,j}, t \le i} f(y_{t,j}, x_{\mathrm{user}})
$$

其中 $f(\cdot)$ 为适应度函数（VLM 评分），$y_{t,j}$ 为第 $t$ 轮第 $j$ 个候选图像，$x_{\mathrm{user}}$ 为用户原始提示。该选择跨所有历史轮次，确保最终输出是全局最优而非仅当前轮最优。

### 3.2 多动作变异精化

RAISE 的进化搜索空间由三种并行的变异动作构成，每种动作从父代候选 $c_{i-1}^*$ 出发生成子代种群。

**重采样变异（Resampling）** 保持用户原始提示不变，通过重新采样初始噪声探索不同的视觉配置：

$$
m_{i,j}^{\mathrm{resample}}(c_{i-1}^*) = (\epsilon_{i,j}, x_{\mathrm{user}}, \emptyset), \quad \epsilon_{i,j} \sim \mathcal{N}(0, I)
$$

其中 $\epsilon_{i,j}$ 为从标准正态分布采样的新噪声，$\emptyset$ 表示无需参考图像。

**提示重写变异（Prompt Rewriting）** 由重写器代理根据未满足需求 $\mathcal{R}_i^-$ 生成优化的文本提示 $x_i^{\mathrm{rewrite}}$，然后以新噪声采样生成候选：

$$
m_{i,j}^{\mathrm{rewrite}}(c_{i-1}^*) = (\epsilon_{i,j}, x_i^{\mathrm{rewrite}}, \emptyset)
$$

**指令式编辑变异（Instructional Editing）** 是 RAISE 区别于其他方法的独特动作。它不重新生成图像，而是对当前最优图像 $y_{i-1}^*$ 施加针对性编辑。编辑指令 $x_i^{\mathrm{edit}}$ 同样由重写器根据 $\mathcal{R}_i^-$ 生成：

$$
m_{i,j}^{\mathrm{edit}}(c_{i-1}^*) = (\epsilon_{i,j}, x_i^{\mathrm{edit}}, y_{i-1}^*)
$$

三种变异动作并行执行，每轮生成 $n_i$ 个候选，构成种群 $\{c_{i,1}, \dots, c_{i,n_i}\}$。这种多动作并行策略扩大了搜索空间，使进化过程能同时探索“重新生成”和“局部修正”两条路径。

### 3.3 结构化工具辅助验证

验证环节是 RAISE “分析-精化-验证”闭环的最后一环，也是其区别于仅依赖 VLM 评分的方法的关键设计。

**图像生成** 根据候选定义中的参考图像字段决定使用生成模型还是编辑模型：

$$
y_{i,j} = \begin{cases}
\mathscr{G}(\epsilon_{i,j}, x_{i,j}), & \text{if } y_{i,j}' = \emptyset, \\
\mathscr{E}(\epsilon_{i,j}, x_{i,j}, y_{i,j}'), & \text{otherwise}.
\end{cases}
$$

其中 $\mathscr{G}$ 为扩散生成模型（FLUX.1-dev），$\mathscr{E}$ 为指令式编辑模型（FLUX.1-Kontext-dev）。

**工具辅助验证** 在校验器执行需求判定之前，先调用视觉工具从候选图像中提取结构化证据 $G_i'$，包括：
- **目标检测**：提取物体边界框与类别标签
- **深度估计**：获取空间深度信息，用于判断空间关系（如“上方”“左侧”）
- **图像描述**：生成图像的自然语言描述，作为语义对齐的参考

校验器基于这些工具证据和二元问题 $Q_i$，输出验证三元组集合和全局决策：

$$
(\mathcal{F}_i', d_i^{\mathrm{verifier}}) = \mathcal{A}_{\mathrm{verifier}}(y_i', G_i', \mathcal{Q}_i)
$$

$$
\mathcal{V}_i = \{v_{i,k} = (q_{i,k}, a_{i,k}, e_{i,k}) \mid a_{i,k} \in \{\text{Yes}, \text{No}\}\}
$$

其中 $q_{i,k}$ 为第 $k$ 个验证问题，$a_{i,k}$ 为二值答案，$e_{i,k}$ 为解释文本。$d_i^{\mathrm{verifier}} \in \{\text{True}, \text{False}\}$ 表示所有需求是否均满足。

**双重停止准则** 确保精化在需求真正满足时终止：只有当分析器的 $d_i^{\mathrm{analyzer}} = \text{end}$ 且校验器的 $d_i^{\mathrm{verifier}} = \text{True}$ 同时成立时，缩放过程才停止。这一设计防止了分析器的误判导致过早终止。

## 实验与关键发现

### 主实验结果

RAISE 在两个核心基准上全面验证了其文本到图像对齐能力。在 **GenEval** 基准上，RAISE 以 **0.94 的总体分数** 取得最优（Table 1），超越所有训练无关和基于训练的推理时缩放方法，包括 ReflectionFlow（0.91）和 Qwen-Image-RL（0.91）。在细粒度子类别中，RAISE 在 Counting（0.95）、Colors（0.98）和 Attribute Binding（0.87）上均达到最佳或次佳，其中 Attribute Binding 相较 Qwen-Image-RL 提升 +0.04，Colors 相较 ReflectionFlow 提升 +0.03。在 **DrawBench** 上，RAISE 取得 **0.885 VQAScore**，显著优于 ReflectionFlow 的 0.844（+0.041，Table 2）。

![[assets/figures/papers/paper_list_l2339_https_arxiv_org_abs_2603_00483/figures/003_Table_1.jpg]]
*Table 1: Quantitative comparison on GenEval [11]. The best and second results are bolded and underlined, respectively; category-best methods are also bolded. “Avg. #Samples Generated” and “Avg. #Calls VLM” indicate efficiency*

![[assets/figures/papers/paper_list_l2339_https_arxiv_org_abs_2603_00483/figures/007_Table_2.jpg]]
*Table 2: Quantitative comparison on the DrawBench [36]. The best result in each column is bolded, the second-best is underlined. The top-performing setting for each method is also bolded*

**效率优势**是 RAISE 的另一关键维度。在 GenEval 上，RAISE 平均仅需生成 **18.6 个样本** 和调用 **7.3 次 VLM**，相比 ReflectionFlow 样本减少 41.9%，VLM 调用减少 88.6%（Table 1）。这一效率源于需求驱动的自适应停止机制：简单提示快速收敛，计算资源自动向 Colors、Position、Attribute Binding 等高难度类别倾斜（Table 7 末行）。

**预算弹性实验**（Table 6）进一步表明，RAISE 在最大样本预算 8、16、32 的设置下均保持最高 GenEval 分数，且性能随预算增加持续提升，而其他基线方法趋于饱和甚至下降。Figure 4 的帕累托前沿图直观展示了 RAISE 在性能-效率坐标系中的支配地位。

### 消融实验

Table 3 的消融实验揭示了 RAISE 各组件的因果贡献：

![[assets/figures/papers/paper_list_l2339_https_arxiv_org_abs_2603_00483/figures/006_Table_3.jpg]]
*Table 3: Ablation Studies on the GenEval [11] benchmark. The best result in each column is bolded, the second-best is underlined*

- **移除视觉工具（w/o Vision Tools）**：Attribute Binding 从 0.87 降至 0.84，Colors 从 0.98 降至 0.96。这表明工具辅助验证（检测、深度估计、描述）为细粒度对齐提供了关键的视觉证据，弥补了 VLM 纯文本推理的感知盲区。
- **禁用指令式编辑（w/o Editing）**：Attribute Binding 从 0.87 降至 0.83。编辑变异使系统能直接修正已生成图像中的未满足需求，而非仅依赖重新生成，是纠正属性绑定错误的核心动作。
- **完整 RAISE 框架**在所有子类别上达到最优，验证了多动作进化（重采样、提示重写、编辑）与工具辅助验证协同的必要性。

### 跨模型泛化

RAISE 作为即插即用框架，在不同基础扩散模型和 VLM 上均表现出稳定的增益：

- **基础扩散模型替换**（Table 4）：在 FLUX.1-dev、FLUX.1-schnell 和 SANA-1.5 4.8B 上，RAISE 均显著提升 GenEval 分数，且保持低样本生成和 VLM 调用量。
- **基础 VLM 替换**（Table 5）：使用 Mistral-Small-3.2-24B、Qwen2.5-VL-32B 等不同 VLM 作为代理骨干时，RAISE 的性能保持稳健，证明框架对 VLM 选择不敏感。

![[assets/figures/papers/paper_list_l2339_https_arxiv_org_abs_2603_00483/figures/008_Table_4.jpg]]
*Table 4: Evaluation with different base DMs (FLUX.1-dev [18], FLUX.1-schnell [18], SANA-1.5 4.8B [46]) on GenEval [11]. The best and second best results are bolded and underlined. “Avg. #Samples Generated” and “Avg. #Calls VLM” indicate efficiency*

### 失败模式与局限

尽管 RAISE 在整体指标上表现优异，分析中仍存在可识别的局限：

- **极复杂场景的对齐错误**：当提示涉及多层空间关系、罕见属性组合或高度抽象概念时，基础扩散模型和 VLM 的固有能力上限限制了 RAISE 的改进空间，工具检测（如深度估计）的噪声可能引入错误的空间判断。
- **系统提示的手工设计**：分析器、重写器和校验器的系统提示为固定模板（Figure 6–9），未针对特定风格或领域优化，在需要特定领域知识的场景下可适应性有限。
- **工具依赖性**：视觉工具（检测、深度估计）的性能直接影响验证精度，在遮挡严重或小目标场景下可能产生误导性证据，需人工核查。

![[assets/figures/papers/paper_list_l2339_https_arxiv_org_abs_2603_00483/figures/010_Table_6.jpg]]
*Table 6: Efficiency comparison on GenEval [11]. RAISE consistently achieves the highest GenEval score across budgets (Max #Samples = 8, 16, 32). At 32 samples, it requires 41.9% fewer samples generated and 88.6% fewer VLM calls on average than the second-best method*

## 定位与知识库关联

### 推理时缩放方法的演进与RAISE的定位

文本到图像生成的对齐问题长期依赖大规模训练或强化学习微调，而推理时缩放（inference-time scaling）提供了一条免训练的替代路径。现有方法可沿两条轴线分类：**动作空间的丰富程度**与**计算分配策略的智能程度**。

**单一动作 + 固定预算**的早期范式以噪声重采样（Noise Scaling）和提示重写（TIR）为代表。前者通过多次采样初始噪声进行随机搜索，后者利用VLM改写提示后重新生成，但两者均采用固定的迭代轮数或候选数量，无法感知当前提示的实际难度。当简单提示被过度精化时，计算被浪费；当复杂提示精化不足时，性能停滞。

**多动作 + 固定预算**的方法以T2I-Copilot为代表，引入了代理式工作流，但仍缺乏对“何时停止”的动态判断。

**反射微调（reflection tuning）** 路线以ReflectionFlow为代表，通过训练使模型具备自我修正能力，在GenEval上达到0.91的总体分数。然而，这类方法需要额外的训练阶段，且在多轮缩放中同样面临性能饱和问题——当反射轮数增加时，改进幅度迅速衰减。

**统一多模态模型**路线以Qwen-Image-RL为代表，通过强化学习训练直接优化对齐目标，在计数（0.93）和属性绑定（0.83）等细粒度类别上表现强劲，但依赖于大规模训练数据和RL调优。

RAISE在上述谱系中的核心突破在于**将需求感知引入缩放决策**：通过分析器动态提取未满足的语义需求，仅在需求未达标时分配额外计算，从而将计算量与提示难度对齐。这一设计使其在**训练无关**的约束下，同时实现了**多动作并行变异**（重采样、提示重写、指令式编辑）和**工具辅助的结构化验证**，形成了“分析-精化-验证”的闭环进化过程。

### 核心差异：需求驱动的自适应停止

RAISE与其他推理时缩放方法的根本差异在于停止准则的设计。传统方法依赖最大轮数或固定分数阈值——这些超参数与具体提示的语义复杂度无关。RAISE则引入了双重停止信号：分析器的“结束”判定（主需求满足）与校验器的True判定（所有需求满足）。这一机制使得系统对简单提示能快速收敛（平均仅需少量样本和VLM调用），而对复杂提示（如涉及颜色、位置、属性绑定的提示）自动分配更多计算资源。Table 7的最后一行明确展示了这种自适应分配：RAISE在Colors、Position和Attribute Binding等困难类别上消耗了更多计算，而在Single Object等简单类别上快速停止。

### 适用边界与能力上限

RAISE的性能受限于两个外部因素：**基础扩散模型的生成能力**和**VLM的视觉理解能力**。Table 4和Table 5分别验证了这一点——当基础扩散模型从FLUX.1-dev切换为更轻量的FLUX.1-schnell或SANA-1.5时，GenEval总体分数下降；当VLM骨干从Mistral-Small-3.2-24B切换为能力较弱的模型时，性能同样衰减。这表明RAISE的进化精化无法超越其底层模型的能力天花板。

此外，视觉工具（检测、深度估计）本身存在精度限制。当检测器漏检小目标或深度估计在复杂遮挡场景下出错时，校验器的判断可能被误导，进而影响分析器对未满足需求的识别。工具噪声是当前框架的固有脆弱点。

### 局限性与开放问题

**系统提示的手工设计瓶颈**是当前框架的显著局限。分析器、重写器和校验器的行为完全由固定的系统提示（Figure 6-9）定义，这些提示为通用场景手工编写，未针对特定风格、领域或文化语境进行优化。当面对高度专业化的提示（如医学影像描述、建筑图纸规格）时，需求提取的粒度和准确性可能不足。

**对离线视觉工具的依赖**增加了系统的复杂性和延迟。每个候选图像需要经过检测、深度估计、描述等多个工具的串行或并行调用，这些工具本身的计算开销不容忽视。如何将部分工具能力内化到VLM的端到端推理中，是提升效率的潜在方向。

**开放问题**包括：（1）能否通过自动提示优化或元学习，使代理的系统提示适应不同领域？（2）RAISE的进化框架能否泛化到视频生成、3D资产生成等更大规模的多模态生成任务？（3）引入更强大的视觉工具（如开放词汇分割、OCR、关系检测）能否进一步提升属性绑定和空间关系判断的精度？（4）在保持验证质量的前提下，能否通过工具选择策略动态决定调用哪些工具，进一步减少计算冗余？

## 原文 PDF

![[paperPDFs/CVPR_2026/RAISE_Requirement_Adaptive_Evolutionary_Refinement_for_Training_Free_Text_to_Image_Alignment.pdf]]
