---
title: "Yo'City: Personalized and Boundless 3D Realistic City Scene Generation via Self-Critic Expansion"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Yo_City_Personalized_and_Boundless_3D_Realistic_City_Scene_Generation_via_Self_Critic_Expansion.pdf
project_link: null
code_link: null
aliases:
- YC
- YCPB3RCSGSCE
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 通过引入‘城市-区域-网格’层次化多智能体规划（Global Planner + Local Designer）和‘产生-优化-评估’自批评生成循环，将城市生成从序列依赖转变为并行自批评过程，并利用关系引导的场景图优化实现无界扩展。
primary_logic: 将城市生成建模为层次化布局规划与自批评生成相结合的任务；利用LLM/VLM的世界知识进行自上而下的推理，在网格级并行生成并通过迭代评估保证质量，从而实现空间连贯、用户定制且可无限扩展的真实感3D城市。
claims:
- Yo'City在VQAScore语义一致性指标上达到0.7151，超越所有基线（SynCity 0.6975）。
- 在几何保真度（Geometric Fidelity）的GPT-5和人工评估中，Yo'City对SynCity的胜率均≥85%。
- 在纹理清晰度（Texture Clarity）上，Yo'City对SynCity的GPT-5胜率为78.5%，人工胜率为81.5%。
- 粗到细规划（coarse-to-fine）消融实验表明，该策略将布局连贯性（Layout Coherence）的GPT-5胜率从27%提升至73%，总体真实感（Overall Realism）胜率从24.5%提升至75.5%。
---

# Yo'City: Personalized and Boundless 3D Realistic City Scene Generation via Self-Critic Expansion

> [!tip] 核心洞察
> 将城市生成建模为层次化布局规划与自批评生成相结合的任务；利用LLM/VLM的世界知识进行自上而下的推理，在网格级并行生成并通过迭代评估保证质量，从而实现空间连贯、用户定制且可无限扩展的真实感3D城市。

| 字段 | 内容 |
|------|------|
| 中文题名 | Yo'City：通过自我批评扩展实现个性化且无边界的3D真实城市场景生成 |
| 英文题名 | Yo'City: Personalized and Boundless 3D Realistic City Scene Generation via Self-Critic Expansion |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Lu_YoCity_Personalized_and_Boundless_3D_Realistic_City_Scene_Generation_via_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | Yo'City |
| Dataset | Yo'City evaluation benchmark dataset |
> [!tip] 效果简介
> - 自定义多维评估基准（包含语义、几何、纹理、布局等维度） 上，VQAScore Yo'City: 0.7151 vs SynCity: 0.6975 (+0.0176)。
> - 自定义多维评估基准 上，几何保真度 GPT-5胜率 Yo'City: 85.00% vs SynCity: 15.00% (+70.00%)；纹理清晰度 GPT-5胜率 Yo'City: 78.50% vs SynCity: 21.50% (+57.00%)；布局连贯性 GPT-5胜率 Yo'City: 86.00% vs SynCity: 14.00% (+72.00%)。

## 概述

**问题与瓶颈**  
现有3D城市场景生成方法主要依赖端到端扩散模型或自回归逐块拼贴，缺乏对城市层次化结构的显式建模。这类“扁平”生成范式导致因果依赖积累、全局布局不一致，且难以根据用户个性化需求进行可控扩展，成为生成真实、连贯且可无限延伸的3D城市的核心瓶颈。

**核心思路**  
Yo’City将城市生成重新建模为**层次化布局规划与自批评生成相结合**的任务。其关键洞察在于：利用LLM/VLM的世界知识进行自上而下的“城市—区域—网格”推理，在网格级实现并行生成，并通过迭代“产生—优化—评估”循环保证输出质量。这一设计从根本上打破了传统自回归生成中的因果依赖，使空间连贯、用户定制且可无限扩展的真实感3D城市成为可能。

**方法定位**  
Yo’City由四个核心模块构成一个完整的生成与扩展流水线（见Figure 2）：
- **Global Planner**：将用户文本提示转化为包含区域划分与功能定位的全局城市布局。
- **Local Designer**：将区域蓝图细化为网格级别的文字描述，保持多网格区域内部一致性。
- **3D Generator**：通过“产生—优化—评估”循环生成等距2D图像，再经由预训练图像到3D模型转换为3D资产并拼装。
- **Expansion Module（关系引导扩展）**：根据用户需求推断新网格内容，构建场景图，通过距离与语义感知优化确定最佳放置位置，实现城市演化。

相比基线方法，Yo’City在生成范式上从“自回归逐块生成”转变为**并行网格对齐生成**，在城市规划机制上从“扁平或无明确规划”升级为**层次化粗到细规划**，并在2D图像生成中引入**迭代自批评优化**，从而在多个维度上取得显著提升。

**主要结果**  
在自定义多维评估基准上，Yo’City在语义一致性（VQAScore 0.7151）上超越最强基线SynCity（0.6975）。在视觉质量的GPT-5与人工成对评估中，Yo’City对SynCity的几何保真度胜率均≥85%，纹理清晰度胜率分别为78.5%和81.5%，布局连贯性GPT-5胜率达86%。消融实验进一步证实，**粗到细规划策略**是布局连贯性（GPT-5胜率从27%提升至73%）和总体真实感（从24.5%提升至75.5%）大幅提升的关键因素。此外，关系引导扩展机制使城市在多次扩展中VQAScore保持稳定，验证了无界生成的能力。

## 背景与动机

### 问题背景：3D城市场景生成的现实需求

大规模、高真实感的3D城市场景生成是数字孪生、影视制作、游戏开发和自动驾驶仿真等领域的核心需求。理想的城市场景生成系统需要同时满足三个关键目标：**真实性**（几何与纹理的高保真度）、**个性化**（根据用户意图定制城市风格与功能布局）和**可扩展性**（能够无边界地扩展城市范围）。然而，这三个目标的协同实现构成了一个开放性的技术挑战。

### 现有方法的瓶颈

当前主流的3D城市场景生成方法主要分为两类，但各自存在结构性缺陷：

**端到端扩散模型方法**试图直接从文本或布局条件生成完整的3D场景，但受限于模型容量和训练数据规模，难以捕捉城市级场景的复杂空间结构和长程依赖关系，生成结果往往缺乏全局一致性。

**逐块生成（tile-by-tile）方法**以 **SynCity** 为代表，采用自回归范式逐个生成网格（grid），每个新网格的生成依赖于已生成网格作为条件。这种机制引入了严格的因果依赖链：网格 $(x, y)$ 的生成必须条件化于先前生成的网格集 $\tau(x, y)$。这带来三个根本性问题：

1. **误差累积**：早期网格的生成错误会沿着依赖链传播和放大，导致后续网格偏离用户意图。
2. **缺乏全局规划**：自回归生成缺乏对城市整体布局的预先规划，各网格之间难以保持空间连贯性和功能一致性。
3. **扩展困难**：当需要向已有城市添加新区域时，自回归框架无法自动推理新网格与现有城市的语义关系和空间适配性。

此外，现有方法普遍采用**扁平化的文本提示**直接驱动生成，缺乏对城市层次化结构的显式建模。真实城市的规划天然遵循“城市—区域—网格”的层次化组织逻辑，而现有方法跳过这一中间推理层，直接从抽象文本映射到具体场景，导致布局失序和语义漂移。

### 核心动机与解决思路

针对上述瓶颈，Yo’City 提出了一种范式转换：**将城市生成从序列依赖的自回归过程转变为层次化规划引导的并行自批评过程**。其核心动机在于：

- **用层次化规划替代扁平生成**：引入“城市—区域—网格”三级结构，通过 Global Planner 进行自上而下的粗到细（coarse-to-fine）布局推理，在生成前建立全局空间蓝图，从根本上解决全局一致性问题。
- **用并行自批评替代自回归依赖**：打破网格间的因果依赖链，所有网格并行生成，并通过“产生—优化—评估”（generate-optimize-evaluate）的迭代循环进行自我批评和质量控制，既提升效率又避免误差累积。
- **用关系引导扩展实现无界演化**：将城市扩展建模为场景图（scene graph）关系推理与距离/语义感知的布局优化问题，使城市能够根据用户需求持续演化，而非一次性静态生成。

这种设计使得 Yo’City 能够生成个性化定制、空间连贯且可无限扩展的真实感3D城市，在语义一致性、几何保真度和纹理清晰度等关键维度上实现对现有方法的显著超越。

## 核心创新

Yo'City 的核心创新在于将 3D 城市场景生成从**自回归序列依赖**重构为**层次化规划驱动的并行自批评过程**，并引入**关系引导的场景图扩展机制**实现无界演化。以下从四个关键维度展开。

### 1. 生成范式：从因果依赖到并行网格对齐生成

现有训练自由的方法（如 SynCity）采用自回归逐块生成，当前瓦片的生成必须以前序瓦片为条件，形成严格的因果依赖链。这种范式不仅限制了生成效率，更导致误差累积和全局一致性缺失。Yo'City 打破了这一范式：所有瓦片在同一轮次内**并行生成**，消除了瓦片间的因果依赖（Sec. 3.1）。并行化的可行性建立在后续的层次化规划之上——全局规划器预先决定了所有网格的功能定位与空间关系，使得每个网格的生成任务相互独立。

### 2. 城市规划机制：城市-区域-网格层次化粗到细规划

基线方法通常依赖扁平文本提示或无明确空间规划，难以在保持全局连贯的同时实现细粒度控制。Yo'City 引入**Global Planner + Local Designer**的双层规划架构（Sec. 3.3, Sec. 3.4）：

- **Global Planner** 将用户个性化提示转化为“城市-区域-网格”三层结构的高层布局，确定区域划分与功能定位，并利用检索增强生成（RAG）从 Wikipedia 获取参考城市的事实知识以增强规划合理性。
- **Local Designer** 进一步将区域蓝图细化为每个网格的详细文字描述，确保同一区域内多网格间的内部一致性。

消融实验（Table 3）强有力地验证了这一设计的因果作用：引入粗到细规划后，布局连贯性 GPT-5 胜率从 27% 跃升至 73%，总体真实感胜率从 24.5% 提升至 75.5%，VQAScore 从 0.7034 提升至 0.7151。这表明层次化规划是全局一致性的关键因果杠杆。

### 3. 2D 图像生成：产生-优化-评估自批评循环

基线方法通常采用单次文本到图像生成，缺乏质量保证机制。Yo'City 的 3D Generator 引入**迭代“产生-优化-评估”循环**（Sec. 3.5）：先生成等距视角 2D 图像，结合固定基座与图像编辑模型进行迭代优化，通过自批评评估确保输出质量，再将高质量等距图像经预训练图像到 3D 模型转换为 3D 资产。这一循环将质量保证内嵌于生成过程，而非事后筛选。

### 4. 城市扩展：关系引导的距离与语义感知布局优化

现有方法缺乏自动扩展机制。Yo'City 的 Expansion Module（Sec. 3.6）根据用户需求推断新网格内容，构建场景图编码网格间关系，通过优化目标函数确定最佳放置位置：

$$L_{\mathrm{dist}}(x) = \sum_{g \in \mathcal{G}} \gamma_{r(g)} \| x - g \|_2$$

$$L_{\mathrm{sem}}(x) = -\sum_{y \in \mathcal{N}(x)} \mathrm{EmbeddingSim}(d_{\mathrm{new}}, d_y)$$

$$L(x) = L_{\mathrm{dist}}(x) + \lambda L_{\mathrm{sem}}(x)$$

其中 $L_{\mathrm{dist}}$ 通过带符号权重 $\gamma_{r(g)}$ 控制新网格与已有网格的吸引/排斥距离，$L_{\mathrm{sem}}$ 利用句子嵌入相似度鼓励语义兼容。最终通过 $x^{*} = \arg\min_{x \in \mathcal{X}} L(x)$ 确定最优位置。实验表明（Figure 5），在 5 个城市 4 步扩展中 VQAScore 保持稳定，验证了扩展机制不损害场景质量。

### 方法谱系与知识库定位

Yo'City 处于**训练自由 3D 场景生成**与**LLM/VLM 驱动空间规划**的交叉点。其与关键基线的差异：

- **vs SynCity**（训练自由逐块生成）：从自回归拼贴转向层次化规划+并行生成，消除了因果依赖瓶颈。
- **vs Trellis / Hunyuan3D**（3D 资产生成）：二者聚焦单资产质量，缺乏场景级布局与扩展能力；Yo'City 将其作为 3D 生成后端，在上层引入规划与关系推理。
- **vs CityCraft**（城市生成）：Yo'City 通过 LLM/VLM 世界知识实现个性化与无界扩展，而非依赖固定模板。

## 整体框架

Yo’City 提出了一种**层次化规划 + 并行生成 + 自批评优化**的 3D 城市场景生成范式，其核心设计在于打破传统自回归逐块生成的因果依赖，转而采用“城市–区域–网格”三级结构进行自上而下的粗到细规划，并在网格级别实现并行生成与迭代质量评估。整个框架由四个关键模块串联构成：**Global Planner**、**Local Designer**、**3D Generator** 和 **Expansion Module**（关系引导扩展），Figure 2 给出了完整的流水线概览。

![[assets/figures/papers/paper_list_l2632_https_openaccess_thecvf_com_content_CVPR2026_html_Lu_YoCity_Personalized/figures/002_Figure_2.jpg]]
*Figure 2: Overview of Yo’City. Global Planner: Converts the user prompt into a coarse city layout. Local Designer: Refines the layout into detailed, per-grid textual descriptions. 3D Generator: Synthesizes 3D assets for each grid by lifting isometric images. Expansion Module: Determines the content and optimal placement for new grids to evolve the city. Finally, all generated 3D assets are assembled into the complete city scene*

### 核心设计理念：从因果依赖到并行自批评

现有方法（如 SynCity）通常以自回归方式逐块生成场景，当前块的生成必须以前序已生成块为条件，形成严格的因果链。Yo’City 将城市空间离散化为 $H \times W$ 的网格 $\mathcal{T} = \{0, \dots, H-1\} \times \{0, \dots, W-1\}$，**所有网格的生成在逻辑上并行执行**，消除了“块 $(x, y)$ 必须以已生成块集为条件”的因果瓶颈（Sec. 3.1）。这一设计使后续的规划、生成与扩展可以独立作用于各网格，为层次化粗到细规划和自批评循环奠定了基础。

### 四模块流水线与数据流

Figure 2 清晰地展示了四个模块之间的输入输出关系：

1. **Global Planner（全局规划器）**  
   接收用户提供的抽象文本提示 $p_0$，将其转化为包含区域划分与功能定位的全局城市布局。该模块采用“城市–区域–网格”层次化结构建模，输出 $N$ 个区域蓝图 $\{B_i \mid i = 1, 2, \dots, N\}$，并借助检索增强生成（RAG）从策划好的 Wikipedia 语料库中检索参考城市的相关事实信息，以增强规划的事实基础（Sec. 3.3）。

2. **Local Designer（局部设计器）**  
   以 Global Planner 的区域蓝图为输入，将每个区域的粗粒度描述细化为网格级别的文字描述。其关键作用是保持多网格区域内部的空间与语义一致性，使相邻网格的生成描述在功能和风格上协调（Sec. 3.4）。

3. **3D Generator（3D 生成器）**  
   针对每个网格的文字描述，通过**“产生–优化–评估”迭代循环**生成高质量的等距（isometric）2D 图像，再利用预训练的图像到 3D 模型将等距图像转换为 3D 资产。由于所有网格的生成过程是网格对齐且并行的，3D 资产可直接按照 Global Planner 预定义的布局进行拼装，无需复杂的 3D 融合操作来解决边界不一致问题（Sec. 3.5）。

4. **Expansion Module（关系引导扩展模块）**  
   根据用户后续的扩展需求推断新网格的内容描述 $d_{\text{new}}$，构建场景图来建模新旧网格之间的空间与语义关系，并通过最小化距离驱动空间目标 $L_{\text{dist}}(x)$ 与语义正则化 $L_{\text{sem}}(x)$ 的加权组合 $L(x)$，在候选位置集 $\mathcal{X}$ 中搜索最优放置位置 $x^*$，实现城市的无界演化（Sec. 3.6）。

### 粗到细规划与自批评循环的协同

Yo’City 将城市生成建模为**层次化布局规划与自批评生成相结合**的任务。Global Planner 和 Local Designer 构成粗到细的规划链路，利用 LLM 的世界知识进行自上而下的推理；3D Generator 中的“产生–优化–评估”循环则在网格级并行执行，通过迭代评估保证每个网格的视觉质量与语义一致性。消融实验（Table 3）证实，粗到细规划策略将布局连贯性的 GPT-5 胜率从 27% 提升至 73%，总体真实感胜率从 24.5% 提升至 75.5%，VQAScore 从 0.7034 提升至 0.7151，验证了该框架设计的有效性。

## 核心模块与公式推导

### 城市生成范式转换：从自回归拼贴到并行自批评

现有方法（如 **SynCity**）采用自回归逐块生成，每个瓦片的生成严格依赖于先前生成瓦片的状态，形成因果依赖链。Yo’City 的核心革新在于打破这一依赖：将所有瓦片并行生成，并通过层次化规划预先注入全局一致性约束。这一范式转换使得城市布局从“序列拼贴”升级为“规划驱动的并行生成”，为后续的自我批评优化提供了结构基础。

### 层次化规划：Global Planner 与 Local Designer

Yo’City 将城市建模为“城市—区域—网格”三层结构，由两个级联模块完成粗到细的规划。

**Global Planner** 负责将用户的抽象文本提示 $p_0$ 转化为全局城市布局。其关键机制包括：
- 利用 LLM 的世界知识进行自上而下的推理，确定城市整体尺寸 $H \times W$；
- 划分 $N$ 个功能区域，并为每个区域生成概念蓝图 $B_i \; (i = 1, 2, \dots, N)$；
- 引入检索增强生成（RAG）模块，从维基百科语料库检索参考城市的相关事实信息，增强布局的事实基础与合理性。

**Local Designer** 将每个区域蓝图进一步细化为网格级别的文字描述。其核心作用是在保持区域内多网格一致性的前提下，为每个网格生成详细的场景描述，作为后续 3D 生成模块的精确输入条件。

### 3D 生成器：产生—优化—评估循环

3D Generator 采用迭代自批评机制生成每个网格的 3D 资产，流程如下：
1. **产生**：根据 Local Designer 提供的网格描述，生成等距视角 2D 图像；
2. **优化**：利用图像编辑模型对生成图像进行细化，修复不一致区域；
3. **评估**：引入评估模型对图像质量进行打分，若未达到阈值则触发重新生成。

通过这一“产生—优化—评估”循环，系统在网格级别实现并行质量自检，确保每个网格的视觉质量达标后，再利用预训练图像到 3D 模型将等距图像转换为 3D 资产。最终，所有 3D 模型按照 Global Planner 预定义的布局直接拼装，无需复杂的 3D 融合操作。

### 关系引导扩展模块与核心公式

城市扩展模块负责根据用户新需求推断新网格内容，并确定其最优放置位置。该模块首先构建场景图，显式建模新网格与已有网格之间的空间和语义关系，随后通过优化以下目标函数确定最佳候选位置 $\mathcal{X}$ 中的最优解。

**距离驱动空间目标**：
$$L_{\mathrm{dist}}(x) = \sum_{g \in \mathcal{G}} \gamma_{r(g)} \| x - g \|_2$$
其中 $\mathcal{G}$ 为已有网格集合，$\gamma_{r(g)}$ 为关系 $r(g)$ 对应的符号权重（正权重拉近，负权重推远），$x$ 为候选网格位置，$g$ 为已有网格位置。

**语义正则化**：
$$L_{\mathrm{sem}}(x) = -\sum_{y \in \mathcal{N}(x)} \mathrm{EmbeddingSim}(d_{\mathrm{new}}, d_y)$$
其中 $\mathcal{N}(x)$ 为候选位置 $x$ 的邻近网格集合，$\mathrm{EmbeddingSim}$ 为句子嵌入相似度（基于 Sentence-BERT），$d_{\mathrm{new}}$ 和 $d_y$ 分别为新网格与邻近网格的文字描述。负号确保最大化语义兼容性。

**总体目标函数与最优位置**：
$$L(x) = L_{\mathrm{dist}}(x) + \lambda L_{\mathrm{sem}}(x)$$
$$x^{*} = \arg\min_{x \in \mathcal{X}} L(x)$$
其中 $\lambda$ 为平衡空间目标与语义正则化的超参数。求得最优位置 $x^{*}$ 后，3D 生成器合成对应网格的 3D 模型并拼入城市场景。

## 实验与分析

### 主实验结果

Yo'City在自定义多维评估基准上与多个基线方法进行了对比，包括无训练逐块生成方法**SynCity**、3D资产生成基线**Trellis**与**Hunyuan3D**（Lai et al., arXiv 2025），以及城市生成基线**CityCraft**。所有方法使用相同提示输入，每项对比重复两次以减少随机性。评估维度涵盖语义一致性（VQAScore）与五项视觉质量指标（几何保真度、纹理清晰度、布局连贯性、场景覆盖度、整体真实感），同时采用GPT-5自动评估与人工评估双重判定。

在语义一致性上，Yo'City取得VQAScore为0.7151，超越最强基线SynCity的0.6975（Table 1）。在视觉质量维度上，Yo'City展现出显著优势：几何保真度方面，GPT-5胜率对SynCity达85.00%，人工胜率达88.00%；对Trellis、Hunyuan3D、CityCraft的GPT-5胜率分别高达93.50%、88.00%和90.50%。纹理清晰度方面，Yo'City对SynCity的GPT-5胜率为78.50%，人工胜率为81.50%。布局连贯性上，Yo'City对SynCity的GPT-5胜率高达86.00%，人工胜率为87.00%。整体真实感维度，Yo'City对SynCity的GPT-5胜率为77.50%，人工胜率为80.00%。GPT-5评估与人工评估趋势一致，表明Yo'City在几何结构、纹理细节和空间布局上均实现了对基线方法的全面超越。

![[assets/figures/papers/paper_list_l2632_https_openaccess_thecvf_com_content_CVPR2026_html_Lu_YoCity_Personalized/figures/003_Table_1.jpg]]
*Table 1: Quantitative comparison of different methods across six evaluation dimensions. We use the VQAScore to evaluate semantic consistency. For the five aspects of visual quality, we conduct pairwise comparisons evaluated by both GPT-5 and human judges, and reported the win rate for each method. To reduce randomness, each comparison is performed twice*

在网格级细粒度评估中（Table 2），Yo'City的对齐得分（Alignment Score）为0.6927，美学得分（Aesthetic Score）为5.52，分别超出SynCity 0.0355和0.57，进一步验证了其在局部网格生成质量上的优势。

![[assets/figures/papers/paper_list_l2632_https_openaccess_thecvf_com_content_CVPR2026_html_Lu_YoCity_Personalized/figures/005_Table_2.jpg]]
*Table 2: Grid-level experimental comparison between SynCity and Yo’City. We report the Alignment Score and Aesthetic Score for both methods for comprehensive assessment*

### 消融实验

消融实验聚焦于粗到细规划策略（Coarse-to-Fine Planning）的有效性（Table 3）。移除该策略的变体Yo'City (w/o reason)采用单阶段规划，其布局连贯性GPT-5胜率仅为27.00%，整体真实感胜率仅为24.50%。引入完整的Global Planner + Local Designer层次化规划后，Yo'City (w reason)的布局连贯性胜率跃升至73.00%，整体真实感胜率提升至75.50%，VQAScore也从0.7034提升至0.7151。该结果直接证明了“城市-区域-网格”层次化推理是保证空间连贯性和整体真实感的关键因果机制。

![[assets/figures/papers/paper_list_l2632_https_openaccess_thecvf_com_content_CVPR2026_html_Lu_YoCity_Personalized/figures/008_Table_3.jpg]]
*Table 3: Ablation study on the planning strategy. Yo’City (w/o reason) denotes the model without this strategy, while Yo’City (w reason) includes it. We evaluate both variants using VQAScore and GPT-5 win rates for Layout Coherence and Overall Realism*

### 城市扩展稳定性验证

关系引导扩展机制（Expansion Module）的性能通过多步扩展实验验证（Figure 5）。在5个不同城市的4步连续扩展过程中，VQAScore保持稳定，未出现随城市规模增长而显著退化的现象。Figure 4展示了扩展过程的可视化效果：初始生成结果经过五次连续扩展迭代后，新扩展网格（蓝色区域）与原有城市布局在空间和语义上保持协调，验证了距离驱动空间目标与语义正则化联合优化的有效性。

![[assets/figures/papers/paper_list_l2632_https_openaccess_thecvf_com_content_CVPR2026_html_Lu_YoCity_Personalized/figures/007_Figure_5.jpg]]
*Figure 5: VQAScore across four expansion steps for five cities*

### 关键图表结论

- **Table 1**：Yo'City在全部六项评估维度上均超越所有基线方法，尤其在几何保真度和布局连贯性上优势最为突出（胜率≥85%）。
- **Table 2**：网格级评估证实Yo'City在局部对齐精度与美学质量上均优于SynCity。
- **Table 3**：粗到细规划策略是Yo'City性能的核心支撑，移除后布局连贯性胜率从73%骤降至27%。
- **Figure 4**：扩展过程可视化展示了关系引导扩展机制在保持城市演化一致性方面的实际效果。
- **Figure 5**：多步扩展中VQAScore的稳定性验证了扩展机制不会引入累积误差。

![[assets/figures/papers/paper_list_l2632_https_openaccess_thecvf_com_content_CVPR2026_html_Lu_YoCity_Personalized/figures/006_Figure_4.jpg]]
*Figure 4: Visualization of expansion. The first row presents the city’s global instruction. The leftmost city shows the initial generation result, followed by five successive expansion iterations. In the top-left corner, a BEV thumbnail depicts the city layout, with blue regions indicating newly expanded grids, while red boxes in the rendered images highlight their appearances*

### 补充图表

![[assets/figures/papers/paper_list_l2632_https_openaccess_thecvf_com_content_CVPR2026_html_Lu_YoCity_Personalized/figures/004_Figure_3.jpg]]
*Figure 3: Qualitative comparison between our method and the baselines given the same city instructions. The red boxes highlight regions in SynCity that exhibit spatial inconsistency, lack of realism, and poor texture fidelity. We additionally provides zoom-in visualizations for Yo’City, demonstrating clearer structural coherence and finer visual details. More cases are shown in Appendix. A.1*

## 方法谱系与知识库定位

### 与现有工作的关系

**Yo'City** 的生成范式与当前主流的3D城市场景生成方法存在根本性差异，其核心突破在于将**层次化多智能体规划**与**自批评生成循环**相结合，打破了传统方法的因果依赖瓶颈。

#### 与训练自由逐块生成方法的对比

**SynCity** 代表了训练自由、自回归拼贴的逐块生成路线。该方法在生成每个网格时严格依赖先前已生成网格的上下文，形成序列化的因果链。Yo'City 则通过 **Global Planner + Local Designer** 的“城市-区域-网格”层次化粗到细规划，将所有网格的生成解耦为**并行网格对齐生成**，从根本上消除了块间因果依赖。这一范式转变在布局连贯性上表现尤为突出：Yo'City 对 SynCity 的 GPT-5 胜率达到 **86.00%**（Table 1），消融实验进一步证实粗到细规划将布局连贯性胜率从 27% 提升至 73%（Table 3）。

#### 与3D资产生成基线的对比

**Trellis** 和 **Hunyuan3D**（Lai et al., arXiv 2025）代表了高保真3D资产生成路线，但它们缺乏城市级的空间规划与场景构图能力。Yo'City 在语义一致性（VQAScore 0.7151）上显著超越 Trellis（0.6189）和 Hunyuan3D（0.6198），在几何保真度上对两者的 GPT-5 胜率分别达到 93.50% 和 88.00%（Table 1）。这表明单纯的资产质量提升无法弥补全局规划的缺失——Yo'City 的优势来源于**自上而下的规划推理**而非生成模型的原始能力。

#### 与城市生成基线的对比

**CityCraft** 作为城市生成基线，在 VQAScore 上仅取得 0.5639，远低于 Yo'City 的 0.7151（Table 1）。该差距反映了扁平提示或无明确规划机制在处理复杂城市语义时的根本局限。Yo'City 通过引入 **RAG（检索增强生成）** 模块，利用 Wikipedia 知识库为 Global Planner 提供事实性地理与城市场景信息锚定（Sec. 3.3），使其能够处理“哈利波特主题公园”等高度个性化需求，而基线方法缺乏此类知识注入机制。

#### 在方法谱系中的定位

从生成范式的演进来看，Yo'City 处于**规划驱动生成**与**自批评优化**的交汇点：

| 维度 | 传统自回归生成 | Yo'City |
|------|---------------|---------|
| 生成范式 | 序列依赖 | 并行网格对齐 + 层次化规划 |
| 规划机制 | 扁平提示/无规划 | 城市-区域-网格粗到细规划 |
| 2D生成 | 直接文生图 | “产生-优化-评估”迭代循环 |
| 扩展能力 | 无自动扩展 | 场景图关系引导的距离与语义感知优化 |

Yo'City 的“产生-优化-评估”循环（Sec. 3.5）将 2D 图像生成从单次推理转变为**迭代自批评过程**：固定基座模型生成初始视图，利用图像编辑模型进行优化，再通过评估反馈决定是否接受。这一机制与近期自改进生成的研究趋势一致，但在3D城市场景领域尚属首次应用。

### 适用边界

1. **网格级并行生成的前提**：Yo'City 的并行生成依赖于 Global Planner 和 Local Designer 预先完成全局布局与网格级描述，这意味着其适用性受限于 LLM/VLM 对城市语义的理解能力。当用户提示极为抽象或超出 LLM 世界知识范围时，规划质量可能下降——尽管 RAG 模块部分缓解了这一问题。

2. **3D转换的保真度瓶颈**：3D Generator 将等距2D图像通过预训练图像到3D模型转换为3D资产（Sec. 3.5），这一步骤的几何与纹理质量受限于下游转换模型的能力。Table 1 中 Yo'City 在纹理清晰度上对 SynCity 的 GPT-5 胜率为 78.5%（几何保真度为 85%），暗示纹理维度仍有提升空间。

3. **扩展的语义漂移风险**：关系引导扩展模块通过场景图维护新增网格与已有城市的语义一致性（Sec. 3.6），但 Figure 5 仅验证了 4 步扩展内的 VQAScore 稳定性。更长链式扩展是否会出现语义漂移或布局退化，原文未提供证据，需要进一步验证。

### 局限与开放问题

1. **计算开销**：Yo'City 的“产生-优化-评估”循环和层次化规划引入了额外的 LLM/VLM 调用开销，原文未报告生成时间或计算成本，实际部署效率需要手动验证。

2. **动态场景与交互**：当前框架生成的是静态3D场景，未涉及动态元素（如交通流、行人）或用户交互，这限制了其在游戏引擎、数字孪生等需要实时交互场景中的应用。

3. **细粒度可控性**：虽然 Global Planner 支持区域级功能定位，但用户无法直接操控单个建筑的风格或布局细节。如何在保持全局一致性的前提下提升局部可控性，是一个开放问题。

4. **评估维度的完整性**：当前评估聚焦于语义一致性和视觉质量，缺乏对生成多样性、用户满意度、以及极端提示下鲁棒性的系统评估。原文未报告失败案例，方法的失效模式尚不明确。

5. **与物理仿真引擎的衔接**：生成的3D资产直接按布局拼装（Sec. 3.5），未涉及物理合理性验证（如建筑间距、日照遮挡等），这在实际城市规划应用中可能构成限制。

## 原文 PDF

![[paperPDFs/CVPR_2026/Yo_City_Personalized_and_Boundless_3D_Realistic_City_Scene_Generation_via_Self_Critic_Expansion.pdf]]