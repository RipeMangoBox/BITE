---
title: "MajutsuCity: Language-driven Aesthetic-adaptive City Generation with Controllable 3D Assets and Layouts"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/MajutsuCity_Language_driven_Aesthetic_adaptive_City_Generation_with_Controllable_3D_Assets_and_Layouts.pdf
project_link: "https://longhz140516.github.io/MajutsuCity/"
code_link: null
aliases:
- MajutsuCity
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 将自然语言编码为结构化的多维城市设计规格（布局、资产、材质、天空盒），通过语言驱动的方式分解意图，从而统一控制宏观布局和细粒度美学属性。
primary_logic: 自然语言本身蕴含着宏观几何逻辑（如“繁华的市中心”）和细粒度美学意图（如“日落下的粉色灯光”），通过一个结构化的“语言到城市规格”管道，可以将文本转换为可控、一致的3D城市组合。
claims:
- MajutsuCity在布局FID上比CityDreamer降低83.7%，比CityCraft降低20.1%
- 在AQS和RDR所有维度上均排名第一，在几何保真度、材质真实感和美学适应性上全面超越基线
- 消融实验表明，移除细粒度空间文本和LongCLIP编码器分别导致FID从22.7上升至35.7和28.0
- Layout Generation (FID) 上 FID = 22.7
---

# MajutsuCity: Language-driven Aesthetic-adaptive City Generation with Controllable 3D Assets and Layouts

> [!tip] 核心洞察
> 自然语言本身蕴含着宏观几何逻辑（如“繁华的市中心”）和细粒度美学意图（如“日落下的粉色灯光”），通过一个结构化的“语言到城市规格”管道，可以将文本转换为可控、一致的3D城市组合。

| 字段 | 内容 |
|------|------|
| 中文题名 | MajutsuCity：语言驱动的美学自适应可控三维资产与布局城市生成 |
| 英文题名 | MajutsuCity: Language-driven Aesthetic-adaptive City Generation with Controllable 3D Assets and Layouts |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2511.20415) · [Project](https://longhz140516.github.io/MajutsuCity/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | MajutsuCity |
| Dataset | Layout Generation, City Scene Generation AQS |

> [!tip] 效果简介
> - Layout Generation (FID) 上，FID 22.7 vs CityDreamer: ~139.4 (基于83.7%降低推算) / CityCraft: 未报告 (较CityDreamer降低83.7%，较CityCraft降低20.1%)。
> - City Scene Generation AQS (GPT-based) 上，SVC / SRC / MTF / LA SVC 8.56, SRC 8.33, MTF 7.00, LA 6.67 vs 其他方法得分均低于本方法 (全部维度排名第一)。

## 概述

城市生成面临一个根本性瓶颈：**隐式神经表示**（如CityDreamer, GaussianCity）虽能合成视觉丰富的场景，却存在多视图不一致和对象级不可控的问题；**显式网格资产检索方法**（如CityCraft）虽支持编辑，但受限于资产库的多样性和风格覆盖，难以响应自然语言中的细粒度美学意图。MajutsuCity的核心洞察在于——自然语言本身同时蕴含宏观几何逻辑（如“繁华的市中心”）和微观美学属性（如“日落下的粉色灯光”），关键在于将其**结构化地分解为可执行的城市设计规格**。

基于这一洞察，MajutsuCity提出了一条**语言驱动的四阶段流水线**：场景设计→布局生成→资产与材质生成→场景组装，将文本意图转化为可控、一致的3D城市组合。同时，集成的**MajutsuAgent**支持通过自然语言进行对象级交互编辑（增、删、改、移、换五种原子操作），实现了生成与编辑的统一框架。

**主要结果**：在布局生成上，MajutsuCity的FID较CityDreamer（Xie et al., CVPR 2024）降低83.7%，较CityCraft降低20.1%；在完整城市场景评估中，AQS和RDR所有维度均排名第一，在几何保真度、材质真实感和美学适应性上全面超越基线。消融实验证实，细粒度空间文本和LongCLIP编码器是布局质量的关键驱动因素——移除后FID分别从22.7退化至35.7和28.0。

**方法谱系与知识库定位**：MajutsuCity处于**文本驱动的显式组合式城市生成**这一交叉点。相较于无条件/隐式生成方法（CityDreamer, GaussianCity, InfiniCity）和纯资产检索方法（CityCraft），其核心改变在于三个维度：(1) 布局生成条件从简短标签升级为LongCLIP编码的细粒度长文本空间描述；(2) 场景表示从隐式场或预定义资产库升级为“先合成布局，再按需生成形状约束的3D资产和可平铺材质”的显式组合框架；(3) 首次引入语言驱动的原子级交互编辑能力。该框架不依赖特定城市或资产库，具有跨风格的泛化潜力。

**局限与待解决问题**：布局生成对提示的逻辑一致性高度敏感，空间描述中的逻辑矛盾可能导致级联错误传播；对于拓扑复杂或不规则的建筑，形状约束难以同时保证视觉质量和几何有效性；独立合成的建筑资产缺少全局尺度感知，可能导致场景中相对大小不协调。这些开放问题指向未来方向：提示逻辑校验机制、复杂拓扑的几何保证策略，以及跨资产的全局尺度一致性约束。

## 背景与动机

城市是高度结构化的复杂空间系统，其自动生成在数字孪生、影视制作和虚拟世界构建等领域具有重要应用价值。然而，现有城市生成方法在**创造性与可控性之间面临根本性的权衡**：一方面，基于隐式神经表示的方法（如CityDreamer、GaussianCity）能够生成视觉丰富的城市场景，但存在严重的多视图不一致问题，且缺乏对象级的可编辑能力；另一方面，基于显式网格资产检索的方法（如CityCraft）虽然支持对象级操作，却受限于预定义资产库的多样性和风格覆盖，难以根据自然语言描述生成具有特定美学风格的城市。

这一瓶颈的根源在于，现有方法未能有效利用自然语言中蕴含的多层次城市设计信息。事实上，自然语言描述同时承载着**宏观几何逻辑**（如“繁华的市中心，高楼林立”）和**细粒度美学意图**（如“日落下的粉色灯光，赛博朋克风格”），但当前系统要么完全忽略语言引导，要么仅使用简短的类别标签，导致生成的场景缺乏几何保真度、风格多样性和交互编辑能力。

MajutsuCity正是在这一背景下提出的。其核心动机在于：**将自然语言编码为结构化的多维城市设计规格，通过语言驱动的方式分解用户意图，从而统一控制从宏观布局到细粒度美学属性的完整生成过程**。该工作试图回答一个关键问题：能否构建一个端到端的语言驱动框架，既保持文本生成的创造性，又提供对象级的可控性和交互式编辑能力？

## 核心创新

MajutsuCity 的核心创新在于将自然语言同时作为**宏观几何逻辑**（如“繁华的市中心”）和**细粒度美学意图**（如“日落下的粉色灯光”）的统一控制信号，通过一个结构化的“语言到城市规格”管道，将文本转换为可控、一致的 3D 城市组合。这一设计直接回应了现有方法的核心瓶颈：隐式表示存在多视图不一致问题，而显式网格方法受限于资产库的多样性和风格覆盖，导致生成场景缺乏几何保真度、风格多样性和交互编辑能力。

### 关键创新点与 changed slots

相较于现有基线方法，MajutsuCity 在以下三个维度上实现了根本性的范式转变：

**1. 布局生成条件：从简短标签到细粒度长文本空间描述**

现有方法（如 **CityDreamer** (Xie et al., CVPR 2024)、**CityCraft**）的布局生成通常依赖无语言引导或简短类别标签，无法捕捉用户对城市空间结构的复杂意图。MajutsuCity 引入**细粒度长文本空间描述**，并由 **LongCLIP** 编码器将其编码为语义特征，作为布局扩散模型的条件输入（Section 3.2）。消融实验证实了这一设计的决定性作用：移除细粒度空间文本后，布局 FID 从 22.7 退化至 35.7；移除 LongCLIP 编码器后，FID 退化至 28.0（Table 3），表明长文本语义理解是高质量布局生成的关键因果旋钮。

**2. 场景表示与资产生成：从隐式/检索式到显式组合式按需生成**

基线方法要么采用隐式神经场（如 CityDreamer、**GaussianCity** (Xie et al., CVPR 2025)），面临多视图不一致的固有问题；要么依赖检索预定义资产库（如 CityCraft），受限于资产多样性和风格覆盖。MajutsuCity 采用**显式组合框架**：先通过两级联扩散模型合成语义布局图和建筑高度图，再按需生成受形状约束的 3D 建筑资产和可平铺材质（Section 3.3, 3.4）。这一设计使得每个建筑资产独立可控，同时保证了生成场景的几何保真度和风格多样性。

**3. 交互编辑能力：从无编辑到语言驱动的原子操作代理**

现有城市生成方法几乎不具备对象级编辑能力，或仅支持全局修改。MajutsuCity 引入 **MajutsuAgent**——一个集成于框架内的语言驱动交互式编辑代理，支持**增、删、改、移、换**五种原子操作（Section 3.5）。用户可通过自然语言指令对已生成的 3D 城市进行对象级迭代精修，实现了从“一次性生成”到“持续创作”的范式升级。

### 创新效果的定量验证

上述创新带来的性能提升在定量实验中得到了充分验证：
- 布局生成 FID 较 CityDreamer 降低 **83.7%**，较 CityCraft 降低 **20.1%**（Table 1）；
- 在城市场景生成的 AQS 和 RDR 所有维度上均排名第一，在几何保真度、材质真实感和美学适应性上全面超越基线（Table 2）。

这些结果表明，将语言信号结构化地分解为布局、资产、材质、天空盒等多维规格，并以显式组合方式实现，是平衡文本创造性与对象级可控性的有效路径。

## 整体框架

MajutsuCity 的核心设计思想是将自然语言蕴含的宏观几何逻辑与细粒度美学意图，通过一条结构化的“语言到城市规格”管道，解耦为可控的三维城市组合。整个框架由四个串行阶段构成，外加一个交互式编辑代理，形成从文本到可编辑三维场景的闭环。

### 四阶段生成管道

**场景设计 (Scene Design)** 作为管道的入口，利用大语言模型 (LLM) 对用户提示进行意图推理，将自由形式的自然语言解析为多维度的城市设计模板。该模板覆盖四个关键维度：布局 (Layout)、资产 (Assets)、材质 (Materials) 和天空球 (Skymap)。LLM 在此承担“规划师”角色，将模糊的文本意图转化为下游模块可执行的结构化规格，从而统一控制宏观布局与细粒度美学属性。

**布局生成 (Layout Generation)** 接收场景设计输出的空间描述，采用两级联框架生成城市布局。第一阶段以 LongCLIP 作为文本编码器的扩散模型，将细粒度长文本空间描述编码为语义特征，合成语义布局图；第二阶段基于 ControlNet 架构，以语义布局图为条件，进一步生成建筑高度图。两个阶段均采用标准潜变量扩散损失进行训练：

$$\mathcal { L } = \mathbb { E } _ { z _ { 0 } , c , \epsilon \sim \mathcal { N } ( 0 , 1 ) , t } \left[ \big \| \epsilon - \epsilon _ { \theta } \big ( z _ { t } , t , c \big ) \big \| _ { 2 } ^ { 2 } \right]$$

这种级联设计确保了语义布局与高度信息之间的空间一致性，为后续的三维实例化提供了可靠的空间蓝图。

**资产与材质生成 (Assets & Materials Generation)** 基于布局阶段输出的形状约束，按需合成三维建筑资产和可平铺材质。建筑资产生成引入图像和点云双重形状约束，以在保证视觉质量的同时维持几何有效性。材质生成则采用在 MajutsuDataset-Material 和 MajutsuDataset-Skybox 上微调的 Qwen-Image 模型，分别合成无缝可平铺的 PBR 纹理贴图和高品质全景天空球。

**场景组装 (Scene Generation)** 将前序模块的输出整合为可渲染的三维城市。地面、道路、水域和植被被组织为四个平面层，直接由语义布局图驱动；建筑资产根据布局图中的位置和高度图进行实例化放置；天空球提供全局光照环境。这种显式组合框架使得每个建筑资产都是独立可寻址的对象，为后续交互编辑奠定了基础。

### 交互式编辑代理

**MajutsuAgent** 是集成在框架中的语言驱动编辑代理，支持五种原子操作：增加 (Add)、删除 (Delete)、修改 (Edit)、移动 (Move) 和替换 (Replace)。用户通过自然语言指令即可对已生成的城市场景进行对象级迭代编辑，无需重新生成整个场景。该代理与四阶段生成管道共享同一套语言理解机制，形成了“生成—编辑—再生成”的闭环工作流。

整个框架的输入输出流清晰：输入为自然语言文本描述，输出为包含独立可编辑三维资产、材质和天空球的城市场景。各模块之间的数据依赖关系为：场景设计 → 布局生成 → 资产与材质生成 → 场景组装，MajutsuAgent 则作为横切关注点，可在场景组装完成后对任意对象施加编辑操作。

### 补充图表

![[assets/figures/papers/paper_list_l2539_https_arxiv_org_abs_2511_20415/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the proposed MajutsuCity framework. MajutsuCity is an aesthetic-adaptive generative framework that enables controllable, object-level 3D urban scene generation from natural language descriptions. It consists of Scene Design, Layout Generation, Assets & Materials Generation, and Scene Generation*

![[assets/figures/papers/paper_list_l2539_https_arxiv_org_abs_2511_20415/figures/001_Figure_1.jpg]]
*Figure 1: MajutsuCity is a language–driven, aesthetic-adaptive system that unifies controllable urban scene generation and interactive editing within a single framework. Conditioned on textual instructions, the framework synthesizes a complete stylized city through layout–height creation, asset instantiation, and terrain/material generation, and further enables iterative refinement through five atomic editing operations. This paradigm forms the core contribution of MajutsuCity, empowering users to create and continuously modify large-scale, stylistically diverse urban scenes through natural language*

## 核心模块与公式推导

MajutsuCity 将自然语言到三维城市的生成分解为四个级联模块，形成一条“语言→结构化规格→显式三维场景”的转化链（Fig. 2）。其核心设计理念在于：自然语言不仅蕴含宏观几何逻辑（如“繁华的市中心”），还包含细粒度美学意图（如“日落下的粉色灯光”），因此需要一个结构化管道将二者分离并分别可控地实现。

### 3.1 场景设计 (Scene Design)

该模块是整个管道的语义入口。LLM 接收用户的自然语言提示，推理其潜在规划意图，并将意图分解为多维度的城市设计模板，显式覆盖四个维度：**Layout**（布局）、**Assets**（资产）、**Materials**（材质）和 **Skymap**（天空球）。这一分解将模糊的自然语言转化为下游各模块可独立消费的结构化规格，是连接高层语义与低层几何的关键桥梁。

### 3.2 布局生成 (Layout Generation)

布局生成采用**两级联扩散框架**，依次合成语义布局图和建筑高度图，确保空间一致性。

**第一阶段**：以细粒度空间文本为条件，通过潜变量扩散模型生成语义布局图 $I_{\text{layout}}$。此阶段将原始 CLIP 文本编码器替换为 **LongCLIP**（Zhang et al., 2024），以增强对长文本空间描述的语义对齐能力。训练目标为标准潜变量扩散损失：

$$\mathcal{L} = \mathbb{E}_{z_0, c, \epsilon \sim \mathcal{N}(0,1), t} \left[ \big\| \epsilon - \epsilon_\theta(z_t, t, c) \big\|_2^2 \right]$$

其中 $z_0$ 为布局图的潜变量表示，$c$ 为 LongCLIP 编码的文本条件，$\epsilon$ 为标准高斯噪声，$\epsilon_\theta$ 为噪声预测网络，$t$ 为扩散时间步。该损失最小化噪声预测误差，驱动模型学习从文本条件到布局潜变量的映射。

**第二阶段**：以第一阶段生成的语义布局图为条件，采用 ControlNet 架构生成建筑高度图。两级联设计使得高度图的生成严格受语义布局约束，避免语义区域与高度分布之间的不一致。

### 3.3 资产与材质生成 (Assets & Materials Generation)

该模块将布局规格实例化为可渲染的三维内容，分为两个并行的生成通道。

**三维建筑资产生成**：采用按需生成策略，根据布局图中各建筑区块的形状约束（图像和点云双重约束）合成对应风格的建筑网格资产。这一设计避免了传统显式方法对预定义资产库的依赖，使建筑形态能够适配布局的几何边界。

**材质与天空球生成**：以 Qwen-Image 为视觉骨干，分别在 MajutsuDataset-Material 和 MajutsuDataset-Skybox 上微调，生成可平铺的 PBR 材质贴图和全景 HDR 天空球。可平铺材质保证了建筑表面纹理的无缝拼接，天空球则为场景提供全局光照与氛围基调。

### 3.4 场景组装 (Scene Generation)

将前述模块的输出组装为完整的可渲染三维城市。地面、道路、水域和植被被组织为四个平面层，直接由语义布局图驱动；建筑资产按布局位置实例化放置；天空球包裹整个场景。这一显式组合框架使得每个对象均可独立寻址，为后续交互编辑提供了对象级粒度。

### 3.5 MajutsuAgent：交互式语言驱动编辑

MajutsuAgent 是集成在框架内的语言驱动编辑代理，支持五种原子操作：**增**（Add）、**删**（Delete）、**改**（Edit）、**移**（Move）、**换**（Replace）。用户通过自然语言指令触发操作，代理将指令解析为目标对象和操作类型，直接修改场景图中的对应节点。这一设计将生成与编辑统一在同一显式场景表示下，无需重新推理整个场景即可实现迭代式精细化修改。

## 实验与分析

### 实验设置

MajutsuCity 的实验围绕两个核心任务展开：**城市布局生成**和**完整城市场景生成**。布局生成以预训练的 Stable Diffusion v2.1 作为基础扩散模型，将原始 CLIP 文本编码器替换为 LongCLIP 以支持长文本空间描述的条件注入。场景生成评估则采用统一的 VLM 评估框架，结合 GPT 评分与用户研究进行双重验证，所有对比方法使用相同的测试数据和评估协议。

### 布局生成：定量与定性结果

Table 1 报告了城市布局生成的定量对比。MajutsuCity 的 FID 达到 **22.7**，较 **CityDreamer**（Xie et al., CVPR 2024）的隐式神经场方法降低 **83.7%**，较 **CityCraft** 的显式资产检索方法降低 **20.1%**。KID 指标仅为 0.013，进一步验证了生成布局与真实数据分布的高度一致性。

![[assets/figures/papers/paper_list_l2539_https_arxiv_org_abs_2511_20415/figures/005_Table_1.jpg]]
*Table 1: Quantitative comparison of Layout Generation*

这一显著提升的因果机制在于两级联框架的设计：第一阶段扩散模型以 LongCLIP 编码的细粒度空间文本为条件，合成语义布局图；第二阶段基于 ControlNet 架构生成建筑高度图，确保空间一致性。Figure 4 的定性对比直观展示了这一优势——MajutsuCity 生成的布局在道路网络连贯性、功能区划分合理性上明显优于 **InfiniCity**（Lin et al., ICCV 2023）、CityDreamer 和 CityCraft。

![[assets/figures/papers/paper_list_l2539_https_arxiv_org_abs_2511_20415/figures/004_Figure_4.jpg]]
*Figure 4: Qualitative comparison of city layouts generation. Our method yields more realistic and coherent urban layouts than prior InfiniteGAN [32], CityDreamer [51] and CityCraft [6]*

### 城市场景生成：多维度评估

Table 2 展示了完整城市场景生成的 **AQS**（Absolute Quantitative Scoring）和 **RDR**（Relative Dimension Ranking）结果。在四个评估维度上，MajutsuCity 均排名第一：

![[assets/figures/papers/paper_list_l2539_https_arxiv_org_abs_2511_20415/figures/006_Table_2.jpg]]
*Table 2: Absolute Quantitative Scoring (AQS) and Relative Dimension Ranking (RDR) for city scene generation. For each metric, we report both GPT-based and user-based scores*

- **SVC**（场景视觉一致性）：GPT 评分 8.56，用户评分 8.35
- **SRC**（风格相关性）：GPT 评分 8.33，用户评分 8.16
- **MTF**（材质真实感）：GPT 评分 7.00，用户评分 8.03
- **LA**（布局美学性）：GPT 评分 6.67，用户评分 7.67

与 **GaussianCity**（Xie et al., CVPR 2025）的神经渲染方法和 **UrbanWorld**（Shang et al., arXiv 2024）的世界模型方法相比，MajutsuCity 在几何保真度和多视图一致性上具有明显优势。Figure 5 的渲染对比表明，基线方法在复杂城市场景中常出现纹理模糊或结构坍塌，而 MajutsuCity 的显式组合框架通过按需生成形状约束的 3D 建筑资产和可平铺材质，有效规避了隐式表示的多视图不一致问题。Figure 6 进一步展示了四种不同美学风格的城市生成结果，验证了框架在风格多样性和风格内一致性上的能力。

![[assets/figures/papers/paper_list_l2539_https_arxiv_org_abs_2511_20415/figures/007_Figure_5.jpg]]
*Figure 5: Qualitative comparison of city scene. We compare our method with CityDreamer [51], GaussianCity [52], UrbanWorld [39], and CityCraft [6] across two representative scenes. Our approach produces scenes with higher geometric fidelity, better multi-view consistency, and richer stylistic diversity than all baselines*

![[assets/figures/papers/paper_list_l2539_https_arxiv_org_abs_2511_20415/figures/008_Figure_6.jpg]]
*Figure 6: Style-driven city generation results. Four city scenes with different well-known styles generated by MajutsuCity show high fidelity and strong intra-style consistency*

### 消融实验：细粒度空间文本与 LongCLIP 的关键作用

Table 3 的消融实验揭示了布局生成性能的两个关键支撑点。移除**细粒度空间文本**（Spatial Text）后，FID 从 22.7 急剧退化至 **35.7**；移除 **LongCLIP 编码器**后，FID 退化至 **28.0**。这表明：

![[assets/figures/papers/paper_list_l2539_https_arxiv_org_abs_2511_20415/figures/009_Table_3.jpg]]
*Table 3: Ablation Study of Layout Generation. ’Spatial Text’ represents fine-grained spatial text, and ’LongCLIP’ represents the long-text visual-language pre-training module [62]*

1. 自然语言中蕴含的宏观几何逻辑（如“繁华的市中心”“沿海岸线分布”）是生成合理布局的核心信号源，简短类别标签无法替代。
2. LongCLIP 的长文本编码能力是有效提取这些细粒度空间语义的必要条件，原始 CLIP 编码器在处理复杂空间描述时存在信息瓶颈。

### 失败模式与局限性

尽管整体性能领先，MajutsuCity 存在三类可复现的失败模式：

1. **逻辑矛盾传播**：当用户提示中的空间描述存在逻辑矛盾（如“市中心同时是安静的郊区”）时，LLM 场景设计阶段可能生成不一致的规格，错误经级联管道传播至后续模块，导致布局混乱。该问题在复杂多约束提示下尤为突出。

2. **复杂建筑形状控制不足**：尽管引入了图像和点云形状约束，对于拓扑复杂或不规则的建筑（如螺旋结构、悬挑体块），按需资产生成模块难以同时保证视觉质量和几何有效性，可能产生表面伪影或结构断裂。

3. **全局尺度不一致**：由于每个建筑资产独立合成，缺少全局尺度感知机制，最终场景组装时可能出现建筑间相对大小不协调的问题，尤其在远景视角下更为明显。

以上失败模式指向三个开放问题：如何检测并处理用户提示中的逻辑矛盾、如何增强对复杂建筑拓扑的几何保证、以及如何在独立合成资产时强制全局尺度一致性。

## 方法谱系与知识库定位

### 1. 问题定位：城市生成中的“创造性-可控性”张力

现有3D城市生成方法长期面临一个结构性矛盾：隐式神经表示（如NeRF、3D高斯泼溅）能够合成视觉逼真的场景，但缺乏对象级可编辑性，且存在严重的多视图不一致问题；显式网格方法（基于资产库检索与放置）天然支持编辑，却受限于资产库的多样性和风格覆盖能力，难以响应开放式的文本描述。MajutsuCity的核心洞察在于：自然语言本身同时承载了宏观几何逻辑（如“繁华的市中心”）和细粒度美学意图（如“日落下的粉色灯光”），通过构建一个结构化的“语言到城市规格”管道，可以将文本意图分解为可控、一致的3D城市组合，从而在创造性与可控性之间建立新的平衡点。

### 2. 方法谱系：从隐式生成到语言驱动的显式组合

**隐式/神经渲染路线**以 **CityDreamer**（Xie et al., CVPR 2024）和 **GaussianCity**（Xie et al., CVPR 2025）为代表。前者采用无条件生成范式，通过隐式神经场合成城市场景，后者则基于3D高斯泼溅实现神经渲染。这类方法在视觉质量上表现突出，但存在两个根本性局限：一是场景表示是整体性的，无法对单个建筑或区域进行独立编辑；二是多视图渲染时容易出现几何不一致（如建筑在不同视角下形态漂移）。MajutsuCity在布局FID上较CityDreamer降低83.7%，直接量化了这一路线在空间结构控制力上的不足。

**显式网格/资产检索路线**以 **CityCraft** 为代表。该方法通过检索预定义资产库并放置网格模型来构建城市场景，天然支持对象级编辑。然而，其生成能力被资产库的规模和风格多样性严格约束——当用户描述超出库内覆盖范围（如“赛博朋克风格的哥特教堂”）时，系统无法按需合成匹配资产。MajutsuCity通过引入“按需资产生成”模块（基于形状约束的3D建筑合成和可平铺材质生成），突破了这一边界，在保持显式表示的可编辑性同时，大幅扩展了风格和几何的生成空间。

**世界模型路线**以 **UrbanWorld**（Shang et al., arXiv 2024）为代表，尝试构建城市世界模型以实现更全面的场景生成。但该方法仍以检索和组装为主，缺乏对语言描述的细粒度美学响应能力。MajutsuCity在AQS和RDR所有维度上均排名第一（Table 2），特别是在材质真实感（MTF）和美学适应性（LA）维度上全面超越包括UrbanWorld在内的所有基线，验证了语言驱动美学控制的有效性。

**早期无限尺度合成**以 **InfiniCity**（Lin et al., ICCV 2023）为代表，探索了无限尺度城市的合成可能性，但其布局生成缺乏语言引导，导致生成结果的结构合理性和多样性受限。MajutsuCity的两级联布局生成框架（语义布局图→建筑高度图）在FID、KID和IS三项指标上均显著优于InfiniCity（Table 1），体现了语言条件注入对布局质量的结构性提升。

### 3. 知识库定位：结构化语言到场景规格的中间表示

MajutsuCity在知识库中的独特定位在于其“结构化中间表示”设计。不同于端到端的文本到场景生成（将语言直接映射到像素或隐特征），也不同于纯检索式方法（将语言仅用于查询匹配），MajutsuCity通过LLM将自然语言解析为多维度的城市设计模板（布局、资产、材质、天空盒），形成一种可解释、可编辑、可验证的中间规格。这一设计将生成问题分解为四个解耦的子任务（场景设计→布局生成→资产材质生成→场景组装），每个子任务可以在各自领域内采用最优技术方案（如布局阶段使用LongCLIP增强的扩散模型，材质阶段使用Qwen-Image微调），同时通过结构化的规格接口保证全局一致性。

这种“语言→规格→场景”的范式在以下方面拓展了现有知识边界：
- **控制粒度**：从全局风格标签扩展到细粒度空间文本（如“市中心有高密度商业区，滨水区域为低层住宅”），消融实验表明移除细粒度空间文本会导致FID从22.7退化至35.7（Table 3），证明了语言粒度对布局质量的关键作用。
- **编辑能力**：通过MajutsuAgent集成五种原子操作（增、删、改、移、换），将交互式编辑从专业3D软件的操作空间迁移到自然语言空间，降低了城市设计的人机交互门槛。
- **美学适应性**：将材质和天空盒纳入语言驱动的生成流程，使场景风格（如“日落下的粉色灯光”）成为可控维度，而非后处理滤镜。

### 4. 适用边界与局限

**适用场景**：MajutsuCity适用于需要兼顾创造性生成与对象级编辑的城市设计场景，如游戏关卡原型设计、影视概念可视化、城市规划方案比选等。其语言驱动特性使其特别适合非专业用户通过自然语言描述进行快速迭代。

**已知局限**（来自论文明确讨论）：
1. **逻辑敏感性**：布局生成对提示的逻辑一致性高度敏感。若用户提供的空间描述存在逻辑矛盾（如“市中心同时是低密度住宅区和高密度商业区”），可能导致级联生成错误并传播到后续模块。系统目前缺乏对用户意图的逻辑校验机制。
2. **复杂几何控制**：尽管引入了图像和点云形状约束，对于拓扑复杂或不规则的建筑（如螺旋形塔楼、异形曲面结构），仍难以同时保证视觉质量和几何有效性。这限制了在高度风格化或非欧几里得建筑场景中的应用。
3. **全局尺度一致性**：由于每个建筑资产独立合成，缺少全局尺度感知，导致最终场景中各建筑的相对大小可能不协调。这一问题在包含多种建筑风格的大型场景中尤为突出。

**不适用场景**：需要严格物理仿真（如光照计算、交通模拟）的城市数字孪生应用；要求厘米级几何精度的建筑遗产数字化；以及需要实时动态交互（如大规模多人游戏中的流式加载）的场景——这些场景对几何精度、物理一致性和运行时性能有超出当前框架能力的要求。

### 5. 开放问题

1. **意图矛盾检测与消解**：如何自动检测用户提示中的逻辑矛盾或几何上不可行的布局要求，并在错误传播前进行修正或向用户请求澄清？这可能需要引入形式化的城市设计约束知识库或基于LLM的意图一致性校验模块。

2. **复杂拓扑的几何保证**：如何增强模型对高度复杂或不规则建筑拓扑的几何保证？可能的路径包括引入拓扑约束的扩散先验、基于程序化语法的形状合成，或混合表示（如将隐式表面用于复杂局部几何，显式网格用于整体结构）。

3. **全局尺度一致性强制**：如何在独立合成建筑资产时强制全局尺度一致性？这可能需要引入场景级的尺度感知损失函数，或在组装阶段增加基于布局上下文的尺度修正步骤。

4. **物理合理性与视觉和谐性**：如何在不损失可控性的前提下，进一步提升复杂城市布局的物理合理性（如建筑间距、日照遮挡）和视觉和谐性（如风格过渡、天际线韵律）？这可能需要将城市规划领域的专业知识编码为可微分约束或奖励信号。

## 原文 PDF

![[paperPDFs/CVPR_2026/MajutsuCity_Language_driven_Aesthetic_adaptive_City_Generation_with_Controllable_3D_Assets_and_Layouts.pdf]]