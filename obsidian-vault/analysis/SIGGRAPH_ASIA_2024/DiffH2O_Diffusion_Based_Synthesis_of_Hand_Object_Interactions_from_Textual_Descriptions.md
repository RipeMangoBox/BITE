---
title: "DiffH2O: Diffusion-Based Synthesis of Hand-Object Interactions from Textual Descriptions"
type: paper
paper_level: A
venue: SIGGRAPH ASIA
year: 2024
pdf_ref: paperPDFs/SIGGRAPH_ASIA_2024/DiffH2O_Diffusion_Based_Synthesis_of_Hand_Object_Interactions_from_Textual_Descriptions.pdf
project_link: null
code_link: null
aliases:
- DiffH2O
tags:
- SIGGRAPH_ASIA_2024
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 时间两阶段扩散过程（抓取与交互分离）与序列补全机制，结合物体相对位姿表示和SDF编码。
primary_logic: 通过将手物交互分解为静态物体抓取和动态交互两个阶段，并引入首帧归一化位姿和SDF距离编码来弱化手与物体的耦合，扩散模型能够在小规模数据下实现对未见物体的交互生成；同时通过抓取引导和详细文本描述增强可控性。
claims:
- DiffH2O 是首个从文本描述合成未见物体的手物交互的方法。
- 两阶段设计和抓取引导在物理与运动多样性指标上显著优于 IMoS 以及 HOI 适配的 MDM、GMD 扩散基线。
- 详细文本描述将手部控制准确率从 59.3% 提升到 86.5%，显著提升生成的可控性。
- 子序列补全（subsequence imputing）比单帧过渡产生更平滑的抓取‑交互过渡。
---

# DiffH2O: Diffusion-Based Synthesis of Hand-Object Interactions from Textual Descriptions

> [!tip] 核心洞察
> 通过将手物交互分解为静态物体抓取和动态交互两个阶段，并引入首帧归一化位姿和SDF距离编码来弱化手与物体的耦合，扩散模型能够在小规模数据下实现对未见物体的交互生成；同时通过抓取引导和详细文本描述增强可控性。

| 字段 | 内容 |
|------|------|
| 中文题名 | DiffH2O: 基于扩散的文本描述到手物交互合成 |
| 英文题名 | DiffH2O: Diffusion-Based Synthesis of Hand-Object Interactions from Textual Descriptions |
| 会议/期刊 | SIGGRAPH ASIA 2024 |
| Links |  [paper](https://doi.org/10.1145/3680528.3687563)|
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | DiffH2O |
| Dataset | GRAB |

> [!tip] 效果简介
> - GRAB (unseen subject split, interaction stage) 上，动作识别准确率 (Action Recognition Accuracy, AR) ↑ 0.810 (DiffH2O Transformer) vs 0.588 (IMoS) (+0.222)。
> - GRAB (unseen object split, full sequence) 上，抓取误差 (Grasp Error, GE) ↓ [m] 0.12 (Ours) vs 0.38 (MDM adapted) (-0.26)。

## 概要

从文本描述生成逼真的手物交互运动，是计算机图形学与具身智能交叉领域的一个关键挑战。其核心瓶颈在于：手物交互数据采集成本极高，现有动作捕捉数据集规模有限，且手与物体之间的紧密耦合导致模型难以泛化到训练时未见过的物体——在保持物理合理性（如无穿透、稳定接触）和语义对齐的前提下，这一问题尤为突出。

针对上述瓶颈，**DiffH2O**（SIGGRAPH Asia 2024）提出了一种基于扩散模型的框架，其核心洞察在于将手物交互**解耦为两个时间阶段**：静态物体的抓取阶段，以及抓取后的动态交互阶段。这一解耦使模型能够分别处理“手接近物体并形成抓取”与“手持物体执行动作”这两个在物理特性和运动模式上截然不同的过程。在此基础上，该方法引入**首帧物体相对位姿表示**与**手部关节到物体表面的SDF距离编码**来弱化手与物体的空间耦合，从而在小规模数据下实现对未见物体的交互泛化。同时，通过**抓取引导**（推理时最小化抓取末帧与目标手势的距离）和**三阶段详细文本描述**（预动作‑动作‑后动作），显著增强了生成的可控性。

在GRAB数据集上，DiffH2O在交互阶段的动作识别准确率达到0.810，较现有方法**IMoS**（Ghosh et al., 2023）的0.588提升了22.2个百分点；在全序列生成中，抓取误差（GE）从适配扩散基线**MDM**的0.38 m降至0.12 m。消融实验进一步验证了各组件的关键作用：详细文本描述将手部控制正确率从59.3%提升至86.5%；子序列补全机制使抓取‑交互过渡的腕部速度显著降低，保证了运动平滑性；首帧相对位姿与SDF编码的组合在接触比率和穿透体积上均优于每帧相对表示。

该方法的主要局限包括：生成运动偶尔出现穿透等物理伪影（未集成物理仿真约束）；推理效率较低（生成32个样本约需300秒）；抓取引导需要手动对齐，且当文本提示与目标抓取冲突时可能忽略引导；对训练分布外的极端物体尺寸泛化能力有限。

在方法谱系上，DiffH2O属于**时间两阶段扩散生成**范式，区别于单阶段扩散基线（如适配后的MDM、GMD）和基于后优化的方法（如IMoS）。其知识库定位在于：将手物交互生成从“端到端黑箱映射”推进到“结构化分解+条件引导”的框架，为后续集成物理约束和提升推理效率的研究提供了明确的切入点。



### 问题背景：手物交互合成的核心挑战

生成逼真的手物交互运动是计算机图形学与具身智能领域的一项基础性难题。与全身人体运动生成不同，手物交互涉及高自由度的手部关节、精细的接触约束以及手与物体之间的复杂物理耦合。这一任务的瓶颈在于：**手物交互数据获取成本极高，且现有方法难以在保持物理合理性和语义对齐的前提下泛化到未见物体**。具体而言，手物交互数据稀缺源于动捕设备对手部精细运动的采集难度，以及标注手‑物体接触状态的复杂性。这使得模型极易过拟合于训练集中的物体形状与交互模式，面对新物体时往往产生穿透、脱离接触或语义错位等伪影。

### 现有方法的缺口

当前手物交互合成方法主要分为两类，但各自存在显著局限：

1. **基于优化的方法**：以 **IMoS**（Ghosh et al., 2023）为代表，首先生成全身人体运动，再通过后优化步骤拟合物体运动。这种解耦策略在处理精细操作（如物体换手）时容易引入运动伪影，且优化过程计算开销大，难以保证物理一致性。

2. **单阶段扩散方法**：将人体运动扩散模型（如 **MDM**、**GMD**）直接适配到手物交互场景，一次性生成整个交互序列。然而，这类方法忽略了手物交互的关键结构特性——**物体在被抓取之前保持静止**。单阶段生成缺乏对抓取与交互两个物理阶段的分治建模，导致抓取精度低、过渡不自然，且难以在推理时注入目标抓取先验以提升对未见物体的泛化能力。

此外，上述方法在**可控性**方面也存在明显不足：它们通常依赖简单的模板文本（如“The person <verb> <object>.”），无法精细描述手部动作的语义细节（如哪只手执行什么操作、物体如何被移动），限制了用户对生成运动的细粒度控制。

### 本文动机

针对上述缺口，DiffH2O 提出三个核心动机驱动的设计：

1. **解耦抓取与交互**：利用“物体在被抓取前静止”这一观察，将手物交互分解为静态物体抓取和动态交互两个时间阶段，分别用不同的扩散模型建模，从而降低单阶段建模的复杂度，提升对未见物体的泛化能力。

2. **弱化手‑物体耦合**：通过首帧物体相对位姿表示和手部关节的符号距离函数（SDF）编码，将手与物体的空间关系从绝对坐标中解耦，使模型更关注相对接触几何而非绝对位置，增强跨物体迁移能力。

3. **增强生成可控性**：引入抓取引导机制和详细文本描述，使用户能够在推理时指定目标抓取手势，并通过三阶段文本（预动作‑动作‑后动作）精细控制手部行为，弥补简单文本条件在语义表达力上的不足。

> 注：DiffH2O 是首个从文本描述合成未见物体手物交互的方法（Section 1 声明，置信度 0.95），其在 GRAB 数据集上的两阶段设计、抓取引导和详细文本条件均通过消融实验和对比实验得到了充分验证。



## 核心方法与创新机理

DiffH2O 的核心创新在于通过**时间两阶段扩散生成**与**手‑物体弱耦合表示**，首次实现了从文本描述到未见物体手物交互的合成。其关键设计围绕以下几个维度的范式转变展开：

### 1. 时间两阶段扩散：抓取与交互的解耦生成

现有方法（如适配后的 **MDM** 和 **GMD**）采用单阶段扩散模型直接生成整个手物交互序列，这要求模型同时学习“手如何靠近并抓取物体”与“手如何操控物体”两种本质上不同的运动模式，导致对未见物体的泛化困难。

DiffH2O 的核心洞察是：**物体在被抓取之前是静止的**。基于这一观察，方法将生成过程解耦为两个时间阶段：

- **抓取阶段**（Grasping Stage）：使用 **ε‑预测扩散模型**，生成双手从初始姿态靠近并抓取静态物体的运动序列。训练目标为预测噪声：
  $$\mathbb{E}_{\epsilon \sim N(0,1), t} || \epsilon_{\theta}(\mathbf{x}_t^{g}, \mathcal{T}, M, t) - \epsilon ||_2^2$$
  采用 classifier‑free 方式训练，为推理时的抓取引导提供便利。

- **交互阶段**（Interaction Stage）：使用 **x₀‑预测扩散模型**，在抓取完成后生成双手与物体同步运动的交互序列。训练目标为直接预测去噪后的输出：
  $$\mathbb{E}_{\epsilon \sim N(0,1), t} || \mathbf{x}_{0,\theta}^{i}(\mathbf{x}_t^{i}, \mathcal{T}, \mathcal{M}, t) - \mathbf{x}_0^{i} ||_2^2$$
  x₀‑预测相比 ε‑预测能产生更干净、更高质量的运动。

两阶段设计的有效性在消融实验中得到验证：与单一扩散模型相比，DiffH2O 在抓取误差（GE）、手性准确率（HA）、穿透体积（IV）等多项物理与运动指标上均取得显著优势（Table 1, Table 2, Table 3）。

### 2. 弱耦合手‑物体表示：首帧归一化位姿 + SDF 距离编码

传统方法（如 D‑Grasp）通常使用每帧物体相对位姿来表示手与物体的空间关系，这种强耦合表示使模型对物体形状变化敏感，限制了向未见物体的泛化。

DiffH2O 提出了一种**弱耦合表示策略**：

- **首帧物体归一化位姿**：将双手位姿统一表示在首帧物体坐标系下，而非每帧独立计算相对位姿。这降低了手与物体运动的耦合程度，使模型更容易适应不同物体几何。
- **手部关节 SDF 距离编码**：对手部每个关节计算到物体表面的有符号距离（Signed Distance），作为额外的空间关系信号注入模型。这种编码近似于有符号距离场（SDF），为扩散模型提供了物体形状的隐式感知。

消融实验（Table 4）证实：首帧物体相对位姿表示 + SDF 距离编码的组合，相比每帧物体相对表示，显著降低了穿透体积并提高了接触比率，有效减少了物理伪影。

### 3. 子序列补全：平滑的阶段过渡

两阶段扩散模型面临的核心挑战是如何将抓取阶段的输出无缝衔接到交互阶段的生成中。单帧过渡（即仅用抓取末帧初始化交互首帧）会导致腕部速度在过渡点急剧增大，运动平滑性显著下降（Table 3）。

DiffH2O 引入**子序列补全**（Subsequence Imputing）机制：
$$\tilde{\mathbf{x}}_{0,\theta}^{i} = (1 - M_g^{i}) \odot \mathbf{x}_{0,\theta}^{i} + M_g^{i} \odot P_g^{i} \mathbf{x}_0^{g}$$
具体而言，将抓取阶段输出的末段序列经投影变换后，按掩码区域填充到交互去噪结果的起始部分。这种“修复式”融合使两个阶段的过渡更加平滑自然，在 Table 3 的消融中表现为过渡速度（T_vel）指标的显著改善。

### 4. 推理时可控性：抓取引导 + 详细文本描述

现有扩散基线在推理时缺乏对目标抓取姿势的约束，仅依赖文本条件，导致生成结果的可控性不足。DiffH2O 从两个层面增强了可控性：

- **抓取引导**（Grasp Guidance）：在抓取扩散模型的推理采样过程中，通过梯度引导使最终帧逼近目标抓取手势：
  $$\nabla_{\mathbf{x}_t^{g}} \log \phi(\mathbf{c} | \mathbf{x}_t^{g}) \approx - \nabla_{\mathbf{x}_t^{g}} || \mathbf{h}_{0,\theta}^{g}(\mathbf{x}_t^{g}) - \hat{\mathbf{h}}_0^{g} ||_2^2$$
  这使用户可以指定期望的抓取方式，模型在保持文本语义一致的前提下生成符合目标抓取的运动。

- **详细文本描述**：将简单模板文本（如“The person <verb> <object>.”）替换为三阶段详细描述（预动作‑动作‑后动作），包含手部信息与空间位置细节。实验表明（Table 5），详细文本训练将动作识别准确率从 51.6% 提升到 88.7%，手部控制正确率从 59.3% 提升到 86.5%，显著增强了生成的可控性与语义对齐能力。

### 创新总结

DiffH2O 的方法论贡献可归纳为四个 **changed slots** 的协同作用：两阶段扩散解耦了运动模式的复杂性，弱耦合表示降低了对物体几何的敏感度，子序列补全保障了阶段过渡的平滑性，抓取引导与详细文本描述则赋予生成过程精细的可控性。这些设计共同使得在小规模 GRAB 数据集上训练的模型能够泛化到未见物体，并生成物理合理、语义对齐的手物交互运动。



### 问题定义与生成目标

DiffH2O 的核心任务是从文本描述和物体几何形状出发，生成双手与物体交互的完整运动序列。给定文本提示 $\mathcal{T}$ 和物体网格，模型建模条件概率分布 $p(\mathbf{x} \mid \mathbf{c}, G=0)$，其中 $\mathbf{x}$ 表示手物交互序列，$\mathbf{c}$ 为条件信号，$G=0$ 指示物体处于静态（未被抓取）的初始状态。这一设定将生成问题分解为两个本质上不同的子阶段：物体静止时的抓取接近，以及抓取后的动态交互。

### 两阶段生成流水线

DiffH2O 的整体流水线由五个核心模块串联构成，形成“编码—抓取生成—过渡补全—交互生成—可控引导”的完整链路：

1. **条件编码层**：将文本提示 $\mathcal{T}$ 通过 CLIP 编码为文本嵌入 $\mathbf{T}$，将物体网格通过基点点集（Basis Point Set, BPS）编码为形状表示 $\mathbf{M}$。同时，扩散时间步 $t$ 经正弦函数编码后注入后续网络。这一层为整个生成过程提供统一的语义与几何条件信号（Figure 6）。

2. **抓取扩散模型（Grasping Diffusion）**：采用 $\epsilon$-预测的扩散模型，生成双手从初始位置逐步靠近并抓取静态物体的运动序列 $\mathbf{x}^g$。该阶段以预测噪声为目标进行训练（classifier-free 方式），损失函数为：
   $$\mathbb{E}_{\epsilon \sim N(0,1), t} \| \epsilon_{\theta}(\mathbf{x}_t^{g}, \mathcal{T}, M, t) - \epsilon \|_2^2$$
   这一设计为后续推理时的抓取引导提供了便利——模型可直接利用噪声预测进行梯度引导，而无需额外的分类器训练。

3. **子序列补全模块（Subsequence Imputing）**：将抓取阶段的输出序列投影并填充到交互阶段的起始帧区域，实现两阶段间的平滑过渡。具体而言，通过掩码 $M_g^i$ 将抓取序列末段 $\mathbf{x}_0^g$ 经投影矩阵 $P_g^i$ 变换后，与交互去噪结果 $\mathbf{x}_{0,\theta}^i$ 进行加权融合：
   $$\tilde{\mathbf{x}}_{0,\theta}^{i} = (1 - M_g^{i}) \odot \mathbf{x}_{0,\theta}^{i} + M_g^{i} \odot P_g^{i} \mathbf{x}_0^{g}$$
   这一机制取代了简单的单帧过渡，有效消除了阶段衔接处的运动不连续性（Table 3 消融实验证实，去除子序列补全将导致过渡腕部速度 T_vel 急剧增大）。

4. **交互扩散模型（Interaction Diffusion）**：采用 $\mathbf{x}_0$-预测的扩散模型，生成抓取后双手与物体协同运动的交互序列 $\mathbf{x}^i$。与抓取阶段不同，该阶段直接预测去噪后的原始输出，以获得更干净、高质量的运动：
   $$\mathbb{E}_{\epsilon \sim N(0,1), t} \| \mathbf{x}_{0,\theta}^{i}(\mathbf{x}_t^{i}, \mathcal{T}, \mathcal{M}, t) - \mathbf{x}_0^{i} \|_2^2$$
   两个扩散模型共享相同的 UNet 骨干网络（配备自适应组归一化 AdaGN），但分别针对各自阶段的运动特征进行训练。

5. **抓取引导模块（Grasp Guidance）**：在推理时，通过梯度引导使抓取扩散模型的最终帧接近用户指定的目标抓取手势 $\hat{\mathbf{h}}_0^g$。引导梯度近似为：
   $$\nabla_{\mathbf{x}_t^{g}} \log \phi(\mathbf{c} \mid \mathbf{x}_t^{g}) \approx - \nabla_{\mathbf{x}_t^{g}} \| \mathbf{h}_{0,\theta}^{g}(\mathbf{x}_t^{g}) - \hat{\mathbf{h}}_0^{g} \|_2^2$$
   该模块使得用户可以在推理阶段指定期望的抓取姿态，增强生成的物理合理性与可控性。

### 手物耦合表示

流水线的输入表示采用首帧物体归一化位姿与手部关节 SDF 距离编码的耦合方案。具体而言，手部关节位置相对于首帧物体位姿进行归一化表示，同时计算手部关节点到物体表面的有符号距离（SDF）作为附加特征。这一表示策略的因果机制在于：**弱化手与物体的绝对位姿耦合**，使模型在训练时学习到手物交互的相对几何关系，而非记忆特定物体的绝对空间配置。Table 4 的消融实验证实，该表示方案相比每帧物体相对位姿表示，显著降低了穿透体积（Interpenetration Volume）并提高了接触比率（Contact Ratio）。

### 文本条件与可控性增强

DiffH2O 支持两种粒度的文本控制：简单模板文本（如“The person <verb> <object>.”）和详细三阶段描述（预动作—动作—后动作，包含手部与位置信息）。详细文本描述通过提供更丰富的语义约束，将手部控制准确率从 59.3% 提升至 86.5%（Table 5），显著增强了生成的可控性。文本嵌入 $\mathbf{T}$ 作为全局条件注入 UNet 的 AdaGN 层，与时间步编码和物体形状编码共同指导去噪过程。

### 数据流与推理效率

在推理阶段，完整流水线从随机噪声出发，依次经过抓取扩散（可选抓取引导）、子序列补全、交互扩散，最终输出完整的 $N$ 帧手物交互序列。然而，该流程存在显著的效率瓶颈：生成 32 个样本约需 300 秒，主要受限于两个扩散模型的顺序采样过程。这一限制使得 DiffH2O 目前难以满足实时交互式应用的需求，也是论文明确指出的开放问题之一。

### 补充图表

![[assets/figures/papers/paper_list_l1807_DiffH2O_Diffusion_Based_Synthesis_of_Hand_Object_Interactions_from_Textu/figures/002_Figure_2.jpg]]
*Figure 2: Overview of DiffH2O. We couple hands and objects by representing hands relative to the object position in the initial frame and encoding hand-object distances (Sec. 4.1). We observe that objects are static until they have been grasped, and propose to decouple grasping and interaction stages and modelling them with two different diffusion processes (Sec. 4.2). Finally, we make use of grasp guidance and subsequence imputation to ensure a smooth transition between these two stages (Sec. 4.2.3). We further show fine-grained synthesis controllability through our detailed textual descriptions (Sec. 4.4)*



### 3.1 运动表示与手物耦合

DiffH2O 将手物交互序列表示为规范化的位姿向量 $\mathbf{x} = (O, \mathcal{H}_l, \mathcal{H}_r) \in \mathbb{R}^N$。其核心设计在于**弱耦合**而非强耦合：手部关节位姿被变换到首帧物体坐标系下，使模型学习的是“手相对于初始物体位姿”的运动模式，而非每帧跟随物体运动的绝对关系。这种首帧物体相对位姿表示（object-relative pose in the initial frame）显著降低了对未见物体形状的过拟合风险。

同时，为弥补弱耦合带来的接触信息缺失，模型引入**手部关节到物体表面的 SDF 距离编码**（signed-distance encoding）。具体而言，对每个手部关节计算其到物体网格的带符号距离，形成一组标量特征，作为手物空间关系的显式代理信号。消融实验（Table 4）证实，首帧物体相对位姿与 SDF 距离编码的耦合，比传统的每帧物体相对位姿表示获得更高的接触比率（contact ratio）和更低的穿透体积（interpenetration volume）。

### 3.2 两阶段扩散框架

DiffH2O 的核心洞见在于：**物体在被抓取之前保持静止**。基于这一观察，整个手物交互序列被解耦为两个时间阶段——抓取阶段（grasping stage）和交互阶段（interaction stage），并由两个独立的扩散模型分别建模。

**抓取扩散模型（ε-预测）** 负责生成双手从初始位置靠近并抓取静态物体的运动序列 $\mathbf{x}^g$。该模型采用 classifier-free 方式训练，以预测噪声 $\epsilon$ 为目标：

$$\mathbb{E}_{\epsilon \sim N(0,1), t} \ || \epsilon_{\theta}(\mathbf{x}_t^{g}, \mathcal{T}, M, t) - \epsilon ||_2^2 \tag{Eq. 3}$$

其中 $\mathcal{T}$ 为 CLIP 文本嵌入，$M$ 为物体 BPS 形状编码，$t$ 为扩散时间步。选择 ε-预测而非 $x_0$-预测，是为后续推理时的抓取引导（grasp guidance）提供梯度接口的便利性。

**交互扩散模型（$x_0$-预测）** 负责生成抓取后的双手与物体协同运动序列 $\mathbf{x}^i$。该模型直接预测去噪后的原始输出 $x_0$：

$$\mathbb{E}_{\epsilon \sim N(0,1), t} \ || \mathbf{x}_{0,\theta}^{i}(\mathbf{x}_t^{i}, \mathcal{T}, \mathcal{M}, t) - \mathbf{x}_0^{i} ||_2^2 \tag{Eq. 4}$$

选择 $x_0$-预测的原因是交互阶段运动复杂度更高，直接预测干净输出可获得更高质量、更少噪声的运动序列（见 Section 4.2.2 原文论述）。

### 3.3 子序列补全机制

两阶段模型独立生成后，需将抓取阶段的末段与交互阶段的首段平滑连接。DiffH2O 提出**子序列补全**（subsequence imputing），其核心操作如下：

$$\tilde{\mathbf{x}}_{0,\theta}^{i} = (1 - M_g^{i}) \odot \mathbf{x}_{0,\theta}^{i} + M_g^{i} \odot P_g^{i} \mathbf{x}_0^{g} \tag{Eq. 5}$$

其中 $P_g^{i}$ 是将抓取序列 $\mathbf{x}_0^{g}$ 投影到交互序列坐标系下的变换矩阵，$M_g^{i}$ 为二值掩码，标记交互序列起始段中需要被替换的区域。该公式的直觉是：在交互扩散去噪的每一步，将抓取阶段输出的对应帧（经位姿对齐后）按掩码直接填充到交互序列的起始位置，使两段运动在重叠的时间窗口内自然融合。

消融实验（Table 3）表明，去除子序列补全、仅用单帧过渡（single-frame transition）会导致抓取-交互过渡处的腕部速度（T_vel）急剧增大，运动平滑性显著下降。

### 3.4 抓取引导

为增强推理时的可控性，DiffH2O 在抓取扩散模型的采样过程中引入**抓取引导**（grasp guidance）。其原理源于分类器引导的均值偏移公式：

$$\pmb{\mu}_{\theta}(\mathbf{x}_t, t) = \pmb{\mu}_{\theta}(\mathbf{x}_t, t)' + s \beta \nabla_{\mathbf{x}_t} \log \mathcal{p}(\mathbf{c} | \mathbf{x}_t) \tag{Eq. 2}$$

在抓取场景下，引导信号 $\mathbf{c}$ 被具体化为目标抓取手势 $\hat{\mathbf{h}}_0^{g}$。由于无法直接计算 $\log p(\mathbf{c} | \mathbf{x}_t^g)$，DiffH2O 采用梯度近似：

$$\nabla_{\mathbf{x}_t^{g}} \log \phi(\mathbf{c} | \mathbf{x}_t^{g}) \approx - \nabla_{\mathbf{x}_t^{g}} || \mathbf{h}_{0,\theta}^{g}(\mathbf{x}_t^{g}) - \hat{\mathbf{h}}_0^{g} ||_2^2 \tag{Eq. 6}$$

其中 $\mathbf{h}_{0,\theta}^{g}(\mathbf{x}_t^{g})$ 为从当前噪声状态 $\mathbf{x}_t^{g}$ 估计的去噪手部姿态。该近似在每一步去噪时最小化预测抓取末帧与目标抓取手势的 L2 距离，从而将生成过程引导至期望的抓取姿态。抓取引导与子序列补全协同工作：前者确保抓取阶段的终点可控，后者保证该终点平滑过渡到交互阶段。

### 3.5 扩散架构与条件注入

两个扩散模型共享相同的 UNet 主干网络（Fig. 6），其条件注入路径如下：

![[assets/figures/papers/paper_list_l1807_DiffH2O_Diffusion_Based_Synthesis_of_Hand_Object_Interactions_from_Textu/figures/013_Figure_6.jpg]]
*Figure 6: Overview of the diffusion architecture. Our pipeline relies on a UNet block and processes three input signals: the time step ?? (?? ), a textprompt embedding T and an object shape encoding M. The time step is encoded using sinusoidal functions, the text-prompt embedding is generated by the CLIP text encoder model and the object encoding is obtained from BPS[Prokudin et al. 2019]. Similarly to [Karunratanakul et al. 2023], we use Adaptive Group normalization in 1D block*

- **文本编码器**：使用 CLIP 将文本提示编码为嵌入向量 $\mathcal{T}$。
- **物体编码器**：使用 BPS（Basis Point Set）将物体网格编码为形状表示 $M$。
- **时间步编码**：扩散时间步 $t$ 经正弦函数编码后注入 UNet。
- **自适应组归一化（AdaGN）**：文本嵌入 $\mathcal{T}$ 与时间步嵌入通过 AdaGN 层融合到 UNet 的归一化操作中，实现条件引导。

该架构设计使模型能够同时感知文本语义、物体几何和扩散进度，为两阶段生成提供统一的条件框架。



## 实验与关键发现

### 主实验结果

DiffH2O 在 GRAB 数据集的两个关键测试场景上均取得显著领先：未见主体分割（unseen subject split）和未见物体分割（unseen object split）。表 1 和表 2 分别汇总了交互阶段和全序列生成的核心指标。

**交互阶段对比（Table 1）**：在未见物体测试集上，DiffH2O（Transformer 骨干）的动作识别准确率（AR）达到 0.810，远超 IMoS 的 0.588（+0.222）。UNet 骨干版本同样优于 IMoS，验证了方法对骨干网络选择的鲁棒性。在多样性指标（DIV）上，DiffH2O 也保持较高水平，表明生成的运动既准确又富有变化。需要注意的是，IMoS 在原论文的未见主体分割下评测时，其模型可能在训练阶段接触过部分测试物体数据，导致其指标被高估（详见原文 Table 8 说明），因此 DiffH2O 的实际优势可能更大。

**全序列对比（Table 2）**：与适配手物交互的扩散基线 MDM 和 GMD 相比，DiffH2O 在抓取误差（GE）上从 0.38 m 降至 0.12 m（−0.26），手性准确率（HA）和穿透体积（IV）也全面占优。单阶段扩散模型在抓取‑交互过渡处出现明显的腕部速度（T_vel）跳变，而 DiffH2O 的两阶段设计配合子序列补全显著平滑了过渡。

**定性对比（Figure 3）**：IMoS 的后优化策略在精细操作（如物体换手）时出现明显伪影，而 DiffH2O 能无缝处理这类复杂交互。

### 消融实验

**两阶段设计与关键组件（Table 3）**：消融实验逐项验证了各组件的贡献。去除子序列补全（退化为单帧过渡）导致过渡腕部速度（T_vel）急剧增大，运动平滑性严重受损。去除抓取引导使抓取误差（GE）上升，手性准确率（HA）下降。两阶段设计本身相比单阶段基线在所有物理和动作指标上均大幅领先，证实了抓取‑交互解耦的核心价值。

**位姿表示与 SDF 编码（Table 4）**：首帧物体相对位姿表示配合手部关节 SDF 距离编码，相比每帧物体相对表示（类似 D‑Grasp 的做法）显著降低了穿透体积并提高了接触比率。这一结果说明，弱化手‑物体的逐帧耦合、代之以首帧归一化和隐式距离场编码，是扩散模型在小规模数据上实现未见物体泛化的关键设计。

**文本条件（Table 5）**：详细文本描述训练将动作识别准确率从 51.6% 提升至 88.7%，手部控制正确率从 59.3% 提升至 86.5%。简单模板文本（如“The person <verb> <object>.”）无法提供足够的空间和时序信息，而三阶段详细描述（预动作‑动作‑后动作）使模型能够精确控制手性、位置和动作类型。

### 失败模式与局限性

Figure 5 展示了三类典型失败案例：

![[assets/figures/papers/paper_list_l1807_DiffH2O_Diffusion_Based_Synthesis_of_Hand_Object_Interactions_from_Textu/figures/012_Figure_5.jpg]]
*Figure 5: Failure Cases. We present three possible failure cases of our method. a) The generated motion does not match the action described in the input prompt, such as trying to perform a bottle opening motion with an apple. b) During grasp guidance, the reference grasp is largely ignored in the diffusion process, resulting in an interaction that is distinct from the grasp reference. c) Despite training with our curated text annotations, the model sometimes does not pick up on the cue of handedness and may interact with a hand different from the one provided in the text prompt*

1. **动作‑文本不匹配**：生成的运动与输入提示中的动作描述不一致，说明语义对齐在部分情况下仍不可靠。
2. **抓取引导被忽略**：当文本提示与目标抓取手势冲突时，模型倾向于遵循文本条件而忽略引导梯度，导致目标抓取未能实现。
3. **手性识别错误**：模型偶尔无法正确理解文本中的左右手提示，生成错误的手性分配。

此外，分析揭示以下系统性局限：
- 物理伪影（穿透、不稳定接触）偶有出现，模型未显式集成物理仿真约束。
- 推理效率低，生成 32 个样本约需 300 秒，难以满足实时应用。
- 对训练分布外极大或极小物体（如 64 cm³ 金字塔或 2208 cm³ 盒子）的泛化能力有限，可能产生严重穿透或脱离接触。
- 详细文本标注依赖人工成本，可扩展性受限。

### 关键图表结论

- **Figure 2**：完整展示了方法框架——首帧归一化表示、两阶段扩散模型、抓取引导与子序列补全的协同工作流。
- **Figure 4**：定性示例覆盖标准生成、抓取引导生成和详细文本控制生成三种模式，直观展示了可控性的提升。
- **Table 6**：提供了网络架构和超参数细节，UNet 配合 AdaGN 实现多条件信号（时间步、文本嵌入、物体编码）的有效融合。
- **附录 Table 8‑9**：补充了 FID、KID 以及多样性和多模态性的标准差，进一步验证了定量分析的可靠性。

![[assets/figures/papers/paper_list_l1807_DiffH2O_Diffusion_Based_Synthesis_of_Hand_Object_Interactions_from_Textu/figures/009_Figure_4.jpg]]
*Figure 4: Qualitative Examples. We provide more qualitative examples with a) standard generation without any guidance b) grasp guidance c) our model trained with detailed text descriptions*

![[assets/figures/papers/paper_list_l1807_DiffH2O_Diffusion_Based_Synthesis_of_Hand_Object_Interactions_from_Textu/figures/014_Table_6.jpg]]
*Table 6: Network architecture. Model and hyperparameters of DiffH2O*

![[assets/figures/papers/paper_list_l1807_DiffH2O_Diffusion_Based_Synthesis_of_Hand_Object_Interactions_from_Textu/figures/016_Table_8.jpg]]
*Table 8: Details of the quantitative analysis with action feature based metrics. We provide further details for the quantitative analysis in Table 1 of the main paper and report standard deviations of multimodality and diversity metrics as well as FID and KID scores. The results here are obtained using action recognition models trained on hand pose data of the respective training splits as indicated in the first column. We either use a subject-based split (top 3 rows) or an object-based split (bottom 3 rows). For IMoS, we use the same pretrained model, which is trained on unseen subject split, across all our experiments (unseen subject and unseen object splits) due to difficulties in reproducing tra...*

### 补充图表

![[assets/figures/papers/paper_list_l1807_DiffH2O_Diffusion_Based_Synthesis_of_Hand_Object_Interactions_from_Textu/figures/003_Table_1.jpg]]
*Table 1: Comparison to State-of-the-Art in the Interaction Stage. We compare our method with two backbones (transformer and UNet) against IMoS [Ghosh et al. 2023]. We report results on an unseen subject split (top 3 rows) [Ghosh et al. 2023], and on our unseen object test dataset (bottom 3 rows). For IMoS, we use the same pretrained model, trained on unseen subject split, across all our experiments (unseen subject/object splits), due to difficulties in reproducing training performance for the unseen object split (indicated with IMoS* in the table). ↑: higher values are better, ↓: lower values are better*

![[assets/figures/papers/paper_list_l1807_DiffH2O_Diffusion_Based_Synthesis_of_Hand_Object_Interactions_from_Textu/figures/005_Table_2.jpg]]
*Table 2: Comparison to Diffusion Baselines for the Full Sequence. We compare against HOI-adapted versions of MDM and GMD. We measure the grasp error (GE) and the accuracy of handedness (HA) with respect to the reference grasp, the interpenetration volume (IV), and the wrist joint velocities*

![[assets/figures/papers/paper_list_l1807_DiffH2O_Diffusion_Based_Synthesis_of_Hand_Object_Interactions_from_Textu/figures/007_Table_3.jpg]]
*Table 3: Ablation Study. We provide ablations of our components against the base model. We measure the grasp error (GE) and the accuracy of handedness (HA) with respect to the reference grasp, as well as interpenetration volume (IV). We also provide the wrist joint velocities*

![[assets/figures/papers/paper_list_l1807_DiffH2O_Diffusion_Based_Synthesis_of_Hand_Object_Interactions_from_Textu/figures/006_Table_4.jpg]]
*Table 4: Pose Representation Evaluation. We compare different alternative pose representations in interaction stage and demonstrate the benefits of object-relative pose representation and encoding hand-object signed distances. Bold indicates the best result, underlined is the*

![[assets/figures/papers/paper_list_l1807_DiffH2O_Diffusion_Based_Synthesis_of_Hand_Object_Interactions_from_Textu/figures/008_Table_5.jpg]]
*Table 5: Text evaluation. We demonstrate that detailed text descriptions enable us to generate motions more representative of the description, and allow fine-grained controllable hand-object motion synthesis*

![[assets/figures/papers/paper_list_l1807_DiffH2O_Diffusion_Based_Synthesis_of_Hand_Object_Interactions_from_Textu/figures/004_Figure_3.jpg]]
*Figure 3: Qualitative Comparison. Post-optimizing object motion as in IMoS [Ghosh et al. 2023] (bottom row) exhibits artifacts with fine-grained manipulations, e.g., when an object switches hands. In contrast, our approach (top row) seamlessly handles such cases. Best seen in supplemental video*



## 定位与知识库关联

### 任务定位与核心突破

DiffH2O 聚焦于**从文本描述和物体几何生成灵巧手-物交互运动**，其核心瓶颈在于手物交互数据的稀缺性与对未见物体的泛化需求。与现有方法相比，DiffH2O 在三个维度上实现了关键突破：

1. **未见物体泛化**：首次实现从文本描述直接合成对未见物体的手物交互，而无需在测试时访问目标物体的交互数据。
2. **阶段解耦生成**：利用“物体在被抓取前保持静止”这一观察，将生成过程分解为抓取阶段与交互阶段，分别由两个扩散模型处理。
3. **精细文本控制**：通过详细的三阶段文本描述（预动作-动作-后动作）替代传统简单模板，显著提升生成的可控性。

### 与基线方法的关系

#### IMoS（Ghosh et al., 2023）

IMoS 是基于语言的全身体人-物交互合成方法，通过后优化生成物体运动。DiffH2O 在以下方面与之形成对比：

- **生成范式**：IMoS 先生成人体运动、再后优化物体轨迹，这种两阶段分离策略在精细操作（如物体换手）中易产生伪影（见 Figure 3）。DiffH2O 则通过统一的扩散框架同时生成手与物体运动，避免了后优化带来的不一致性。
- **未见物体泛化**：IMoS 在训练时可能接触到部分未见物体测试数据（见 Table 8 说明），导致指标被高估。DiffH2O 在严格未见物体划分下仍显著优于 IMoS：动作识别准确率从 0.588 提升至 0.810（Table 1）。
- **物理合理性**：IMoS 的后优化策略无法保证手物接触的物理一致性，而 DiffH2O 通过 SDF 距离编码和两阶段设计显著降低了穿透体积。

#### MDM（adapted）与 GMD（adapted）

MDM 和 GMD 是人体运动扩散模型的代表性工作，DiffH2O 将其适配为手物交互基线进行对比：

- **MDM（adapted）**：单阶段扩散生成整个交互序列，无抓取引导。在全序列评估中，其抓取误差（GE）为 0.38m，而 DiffH2O 仅为 0.12m（Table 2），表明单阶段模型难以同时处理抓取与交互的异质性需求。
- **GMD（adapted）**：带推理时引导的扩散模型，但省略了 2D 轨迹生成阶段。其过渡速度（T_vel）显著高于 DiffH2O，说明缺乏显式的阶段过渡机制导致运动不平滑。

DiffH2O 相对于这两类扩散基线的优势源于三个设计选择：**两阶段扩散**（分离抓取与交互的生成目标）、**子序列补全**（替代单帧过渡）和**抓取引导**（提供目标抓取先验）。

### 方法谱系中的关键设计选择

#### 时间两阶段扩散 vs. 单阶段扩散

DiffH2O 将运动生成分解为抓取阶段（ε-预测扩散模型）和交互阶段（x₀-预测扩散模型），这一设计的合理性在于：

- **抓取阶段**的目标是生成手部从初始位置到稳定抓取物体的运动，物体在此期间保持静止。使用 ε-预测便于在推理时通过梯度引导（Eq. 6）控制抓取末帧。
- **交互阶段**的目标是生成抓取后的动态操作运动，物体开始运动。使用 x₀-预测可获得更干净、高质量的运动输出（Eq. 4）。

消融实验（Table 3）表明，单一扩散模型在抓取误差、穿透体积和过渡平滑性上均显著劣于两阶段设计。

#### 首帧物体相对位姿 + SDF 编码 vs. 每帧物体相对位姿

传统方法（如 D-Grasp）使用每帧物体相对位姿表示手物关系，但这引入了手与物体运动的强耦合，不利于泛化。DiffH2O 采用首帧物体归一化位姿 + 手部关节 SDF 距离编码（Section 4.1），其优势在于：

- **弱化耦合**：仅在首帧建立手物相对关系，后续帧通过 SDF 距离隐式编码接触信息，使模型更容易适应不同物体的几何形状。
- **物理合理性**：Table 4 的消融显示，该表示比每帧物体相对表示显著降低穿透体积并提高接触比率。

#### 子序列补全 vs. 单帧过渡

两阶段生成面临的核心挑战是阶段间的平滑过渡。DiffH2O 提出子序列补全（subsequence imputing），将抓取阶段末段投影到交互阶段起始段，通过掩码融合实现平滑连接（Eq. 5）。Table 3 的消融表明，去除子序列补全（改用单帧过渡）会导致腕部过渡速度（T_vel）急剧增大，运动平滑性显著下降。

#### 详细文本描述 vs. 简单模板文本

现有方法多使用简单模板（如“The person <verb> <object>.”）作为文本条件。DiffH2O 引入三阶段详细文本描述，包含手部动作细节和位置信息（Section 4.4）。Table 5 显示，详细文本训练使动作识别准确率从 51.6% 提升到 88.7%，手部控制正确率从 59.3% 提升到 86.5%，证明了精细文本标注对运动可控性的关键作用。

### 适用边界与局限

尽管 DiffH2O 在手物交互生成上取得了显著进展，其适用边界受以下因素制约：

1. **物理伪影**：模型未显式集成物理仿真约束，生成的动作偶尔出现穿透和不稳定接触。对于训练分布外的极端物体尺寸（如 64 cm³ 的小金字塔或 2208 cm³ 的大盒子），物理伪影更为明显。
2. **推理效率**：生成 32 个样本约需 300 秒，难以满足实时交互应用需求。
3. **抓取引导冲突**：当文本提示与目标抓取手势冲突时，模型可能优先遵循文本而忽略引导（见 Figure 5b），控制可靠性有待提升。
4. **数据规模限制**：仅在 GRAB 数据集上训练，开放域交互的泛化性未经验证。
5. **文本标注成本**：详细文本描述依赖人工标注，可扩展性受限。
6. **手性识别**：模型偶尔无法正确识别左右手提示（见 Figure 5c），对细粒度语义的敏感性不足。

### 开放问题

基于上述局限，DiffH2O 开启的研究方向包括：

1. **物理约束集成**：如何将接触力、稳定性等物理约束显式融入扩散生成过程，以消除穿透和不稳定接触等伪影？
2. **推理加速**：能否通过潜在空间扩散或高效采样策略将推理时间压缩至秒级，以支持交互式应用？
3. **引导冲突消解**：如何自动对齐目标抓取与文本提示，避免两者冲突导致的控制失效？
4. **极端尺度泛化**：如何改进模型对训练分布外物体尺寸和形状的鲁棒性？
5. **弱监督文本控制**：在不依赖大规模人工标注的前提下，如何自动生成或利用弱监督文本描述来增强运动控制？



## 原文 PDF

![[paperPDFs/SIGGRAPH_ASIA_2024/DiffH2O_Diffusion_Based_Synthesis_of_Hand_Object_Interactions_from_Textual_Descriptions.pdf]]
