---
title: "E.T. the Exceptional Trajectories: Text-to-camera-trajectory generation with character awareness"
type: paper
paper_level: A
venue: ECCV
year: 2024
pdf_ref: paperPDFs/ECCV_2024/E_T_the_Exceptional_Trajectories_Text_to_camera_trajectory_generation_with_character_awareness.pdf
aliases:
- DDTCT
- ETETTCTGCA
tags:
- ECCV_2024
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 关键因果变量是引入角色轨迹作为显式生成条件，并采用全局坐标系代替角色相对坐标系。这使扩散模型能学习相机运动与角色运动之间的复杂时空关联，从而生成更符合电影语法的相机轨迹。
primary_logic: 通过从真实电影中构建大规模、多模态的相机-角色轨迹数据集（E.T.），并配套基于对比学习的语言-轨迹嵌入（CLaTr）进行评估，可以训练出对角色运动感知更强、文本遵循度更高的相机轨迹扩散模型（Director），显著提升生成的电影感与可控性。
claims:
- Director C在E.T.混合子集上显著超越所有基线，FDCLaTr从CCD的35.81降至3.76，CLaTr-Score从6.26提升至21.95。
- E.T.数据集包含115K样本、11M帧、120小时，具备相机与角色轨迹及两类文本描述，规模与多样性远超现有相机轨迹数据集。
- CLaTr嵌入在文本-轨迹检索任务上达到R@1=19.73%，表明学习到的联合嵌入空间具有良好的跨模态对齐性。
- E.T. mixed subset 上 FD_CLaTr ↓ = 3.76 (Director C)
---

# E.T. the Exceptional Trajectories: Text-to-camera-trajectory generation with character awareness

> [!tip] 核心洞察
> 通过从真实电影中构建大规模、多模态的相机-角色轨迹数据集（E.T.），并配套基于对比学习的语言-轨迹嵌入（CLaTr）进行评估，可以训练出对角色运动感知更强、文本遵循度更高的相机轨迹扩散模型（Director），显著提升生成的电影感与可控性。

| 字段 | 内容 |
|------|------|
| 中文题名 | E.T.非凡轨迹：具有角色感知的文本到摄像机轨迹生成 |
| 英文题名 | E.T. the Exceptional Trajectories: Text-to-camera-trajectory generation with character awareness |
| 会议/期刊 | ECCV 2024 |
| Links | [paper](https://arxiv.org/abs/2407.01516) · [Project](https://www.lix.polytechnique.fr/vista/projects/2024\_et\_courant) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Director (DiffusIon tRansformEr Camera TrajectORy) |
| Dataset | E.T. mixed subset |

> [!tip] 效果简介
> - E.T. mixed subset 上，FD_CLaTr ↓ 3.76 (Director C) vs 6.79 (MDM) (-3.03)；FD_CLaTr ↓ 3.76 (Director C) vs 35.81 (CCD) (-32.05)；CLaTr-Score (CS) ↑ 21.95 (Director C) vs 18.32 (MDM) (+3.63)。

## 概述

真实电影级相机轨迹的自动生成是连接语言描述与视觉叙事的关键环节，但该任务长期受制于三大瓶颈：**数据匮乏**（缺乏同时包含相机与角色轨迹及详细文本描述的大规模真实电影数据集）、**建模简化**（现有方法采用角色相对坐标系，无法建模相机与角色间的复杂同步与偏移关系）、以及**评估粗糙**（基于简单六类动作分类器的指标无法反映生成轨迹的真实质量与语义一致性）。

针对上述瓶颈，本文提出了一套从数据、模型到评估的完整解决方案。首先构建了**E.T.数据集**——一个基于Condensed Movies Dataset的大规模多模态相机-角色轨迹数据集，包含约115K样本、11M帧、120小时内容，每条样本配有独立的相机运动描述和相机-角色关系描述。其次，设计了**Director扩散模型**，以全局坐标系下分离表示的相机与角色轨迹为条件，通过三种可选的Transformer条件注入机制（上下文前缀、AdaLN调制、交叉注意力）生成符合电影语法的相机轨迹。最后，提出**CLaTr对比语言-轨迹嵌入**，学习文本与轨迹的联合表示空间，用于计算FDCLaTr距离和CLaTr-Score等更准确的评估指标。

核心实验结果表明，采用交叉注意力机制的**Director C**在E.T.混合子集上显著超越所有基线：FDCLaTr从CCD的35.81降至3.76，CLaTr-Score从6.26提升至21.95，验证了角色感知的全局坐标系建模和CLaTr评估的有效性。该方法在可控性、多样性和角色感知方面展现出良好的定性效果，为文本驱动的电影级相机控制提供了新的基准。

## 背景与动机

### 电影视觉叙事中的相机控制困境

在电影和动画制作中，相机轨迹是视觉叙事的核心语法元素。通过推拉、横移、摇镜等运动，导演引导观众注意力、塑造空间感并传达情感。然而，在AI驱动的视频生成取得显著进展的背景下，一个关键瓶颈依然存在：**如何根据文本描述自动生成符合电影语法的相机轨迹**。

现有方法面临三重根本性挑战：

**第一，数据匮乏。** 真实电影级相机轨迹的获取需要同时捕获相机与角色的三维运动，并配以详细的文本描述。现有数据集要么聚焦于静态场景（如RealEstate10K），要么仅包含合成数据，缺乏真实电影中相机与角色之间的复杂互动模式。

**第二，建模简化。** 此前的工作（如CCD）采用角色相对坐标系来简化问题——将相机运动表示为相对于角色位置的偏移。这种简化虽然降低了学习难度，却从根本上牺牲了相机与角色之间复杂的时空同步关系：在真实电影中，相机可能独立于角色运动（如建立镜头），也可能与角色保持精确的相对运动（如跟拍），甚至在不同阶段切换行为模式。

**第三，评估失真。** 现有评估指标依赖仅能区分六个基本动作类别的分类器特征，无法捕捉生成轨迹与文本描述之间的细粒度语义一致性。例如，“相机缓慢向右横移以跟随角色”与“相机快速向右横移并超越角色”在语义上截然不同，但在粗粒度分类器下可能被判定为相似。

### 本文的核心洞察

本文的核心洞察是：**将角色轨迹作为显式生成条件，并采用全局坐标系代替角色相对坐标系**，是解锁电影级相机轨迹生成的关键。这一设计选择使扩散模型能够学习相机运动与角色运动之间丰富的因果关联——相机何时跟随、何时预判、何时独立于角色运动——从而生成更符合电影语法的轨迹。

为支撑这一范式转变，作者构建了**E.T.（Exceptional Trajectories）数据集**——首个大规模、多模态的电影相机-角色轨迹数据集，包含115K样本、11M帧、120小时的内容，并提出了配套的**CLaTr（Contrastive Language-Trajectory）嵌入**用于评估，以及**Director扩散模型**用于生成。三者形成闭环：数据提供学习基础，嵌入提供评估标准，模型实现可控生成。

## 核心创新

E.T. 工作的核心创新并非提出一种全新的生成范式，而是针对“文本到相机轨迹生成”这一任务，系统性地重构了建模坐标系、条件输入和评估体系，从而将任务从简化的合成场景推向真实的电影级生成。

### 坐标系重构：从角色相对到全局绝对

此前的工作 **CCD** 采用角色相对坐标系建模相机运动。这一设计虽然简化了学习问题，却造成了一个根本性的能力瓶颈：相机轨迹与角色轨迹之间的复杂时空同步与偏移关系被隐式地消解了，模型无法学习到“角色向左移动时，相机从右侧平行跟拍”这类需要全局空间感知的电影语法。

Director 的核心决策是将坐标系切换为**全局坐标系**，并将相机轨迹与角色轨迹**分离表示**。这一改变使扩散模型能够直接感知相机与角色在共同世界空间中的绝对位置关系，从而学习到更丰富的相机-角色交互模式。从因果角度看，坐标系是关键的**因果旋钮**——它决定了模型能否访问角色运动与相机运动之间的完整联合分布，而非仅仅是条件于角色位置的局部偏移。

### 条件机制：引入角色轨迹作为显式生成条件

在条件输入层面，Director 的改进体现为两个维度的扩展：

1. **文本描述的丰富化**：不同于 CCD 使用有限词汇的简单描述，E.T. 数据集提供了两类文本描述——纯相机运动描述和相机-角色关系描述。后者明确编码了“相机如何相对于角色运动”的语义信息，为模型提供了更强的语言引导信号。

2. **角色轨迹的显式条件注入**：这是最关键的 changed slot。Director 将角色的 3D 轨迹序列作为与文本并行的条件输入，而非像 CCD 那样仅将其作为坐标变换的参照系。这一设计使得模型能够同时关注“文本说了什么”和“角色在做什么”，从而生成既符合语言描述又与角色运动协调的相机轨迹。

### 条件注入机制的架构探索

为了有效融合文本和角色轨迹这两种异构条件，Director 系统性地探索了三种 Transformer 条件注入机制（Figure 5）：

- **Director A（上下文前缀）**：将条件作为序列前缀 token 直接拼接到噪声轨迹序列前，通过自注意力实现隐式融合。
- **Director B（AdaLN 调制）**：利用自适应层归一化（AdaLN）对 Transformer 各层进行条件相关的缩放和平移调制，其操作为 $\mathrm{ADALN}(\gamma, \beta, x) = (1 + \gamma) \mathrm{LN}(X) + \beta$。
- **Director C（交叉注意力）**：将 CLIP 文本嵌入与线性投影后的角色轨迹拼接，通过额外的 Transformer 编码器层处理后，以交叉注意力的方式注入去噪网络。这一设计保留了条件的完整序列长度，信息损失最小。

实验表明，交叉注意力机制（Director C）在 E.T. 混合子集上取得了最优的 FD_CLaTr（3.76），显著优于 AdaLN 方案（Director B, 6.10）和上下文前缀方案（Director A, 3.88），验证了保留条件序列完整信息对于相机-角色关系建模的重要性。

### 评估体系的范式转换

评估指标的革新是另一个关键的 changed slot。CCD 依赖一个基于六类基本动作的分类器来提取特征，这一简化评估方案无法反映生成轨迹的真实语义质量——例如，它难以区分“缓慢推进”与“快速推进”之间的差异，也无法评估轨迹与文本描述之间的细粒度一致性。

E.T. 提出的 **CLaTr**（Contrastive Language-Trajectory embedding）通过对比学习构建了一个文本与轨迹的联合嵌入空间。基于此，引入两个新指标：

- **FD_CLaTr**：在 CLaTr 嵌入空间中计算生成轨迹与真实轨迹分布的 Fréchet 距离，衡量生成质量。
- **CLaTr-Score**：计算生成轨迹嵌入与对应文本嵌入的余弦相似度，衡量文本-轨迹一致性。

这一评估体系使得模型性能的衡量更贴近“生成的相机运动是否符合文本描述的电影语义”这一实际目标。CLaTr 在文本-轨迹检索任务上达到 R@1=19.73%（Table 3），表明其嵌入空间具有良好的跨模态对齐性，为评估指标的可靠性提供了支撑。

### 创新依赖的基础：E.T. 数据集

上述方法创新的可行性建立在 **E.T. 数据集**之上。该数据集从 Condensed Movies Dataset (CMD) 构建，包含 115K 样本、11M 帧、120 小时的真实电影数据，同时提供相机与角色的 3D 轨迹以及两类文本描述。相比 CCD 使用的合成数据，E.T. 在规模和真实性上均有质的飞跃，为训练具有角色感知能力的全局坐标相机轨迹生成模型提供了必要的数据基础。

## 整体框架

E.T. 系统围绕三个核心模块构建了一条从真实电影数据到可控相机轨迹生成的完整流水线：**E.T. 数据集构建** → **Director 扩散模型** → **CLaTr 对比嵌入评估**。三个模块在逻辑上形成“数据—生成—评估”的闭环，但在训练上是解耦的：E.T. 数据集为 Director 和 CLaTr 提供训练与评估样本，CLaTr 嵌入则作为 Director 生成质量的语义感知度量。

### 数据流与输入输出

整个流水线的输入是真实电影的视频帧序列，最终输出是在全局坐标系下、以角色轨迹和文本描述为条件的相机轨迹。具体流转路径如下：

1. **从视频到结构化轨迹**：给定电影镜头的 RGB 帧序列，系统首先通过 SLAHMR 等工具提取相机和角色的 3D 位姿，经过去噪、对齐和分块拼接后，形成相机轨迹 $\mathbf{x}_{1:N}$（$N$ 个连续相机位姿的序列）和角色轨迹 $\mathbf{h}_{1:N}$。两者均表示在全局坐标系中，而非角色相对坐标系——这是与 CCD 等前人工作的关键分叉点。

2. **从轨迹到文本描述**：对提取的轨迹进行运动标注（motion tagging），使用基于速度阈值的规则将轨迹划分为纯运动片段，并赋予“平移左/右”“推近/拉远”等基础运动标签。随后，利用大语言模型将这些标签翻译为两类自然语言描述：**相机专用描述**（仅描述相机运动）和**相机-角色联合描述**（描述相机相对于角色运动的语义关系，如“相机向右平移以跟随角色”）。

3. **从文本+角色轨迹到相机轨迹**：Director 扩散模型接收角色轨迹 $\mathbf{h}$ 和相机-角色联合文本描述 $c$ 作为条件，通过去噪扩散过程生成相机轨迹 $\mathbf{x}$。文本条件经 CLIP 编码为嵌入序列，角色轨迹经线性投影后，根据架构变体的不同，以三种方式注入 Transformer 去噪器：上下文前缀（Director A）、AdaLN 调制（Director B）或交叉注意力（Director C）。

4. **从生成轨迹到语义评估**：CLaTr 将文本和相机轨迹分别编码到联合嵌入空间，通过计算生成轨迹嵌入与条件文本嵌入之间的 FD（Fréchet Distance）和余弦相似度，得到 FDCLaTr 和 CLaTr-Score 两个指标，分别衡量生成轨迹的整体质量分布和单样本条件一致性。

### 模块间的因果依赖

三个模块之间存在明确的因果依赖关系：

- **E.T. 数据集是 Director 和 CLaTr 的共同基础**：Director 在该数据集上学习从角色轨迹和文本到相机轨迹的条件映射；CLaTr 在该数据集上学习文本-轨迹的跨模态对齐。这种共享数据基础既保证了训练信号的一致性，也引入了潜在的评估自洽偏差——CLaTr 和 Director 在相同数据分布上训练，CLaTr 指标可能对 Director 的生成结果存在偏好。

- **全局坐标系是角色感知生成的前提**：若采用 CCD 的角色相对坐标系，相机轨迹被简化为相对于角色的偏移量，无法表达“相机绕角色旋转”或“相机静止而角色运动”等复杂电影语法。E.T. 数据集在构建时即采用全局坐标系，Director 在生成时也保持全局坐标输出，这使得模型能够学习相机与角色在空间中的独立运动及其同步/偏移关系。

- **CLaTr 嵌入的语义空间定义了“好轨迹”的评判标准**：传统评估依赖六类基础动作的分类器特征（如 CCD 所用），无法捕捉“相机跟随角色右移”与“相机自行右移”的语义差异。CLaTr 通过对比学习将文本语义与轨迹结构对齐，使得评估能够区分轨迹是否真正满足了文本条件——这一能力直接决定了 Director 各变体在 CLaTr-Score 上的排序。

### 架构选择的因果机制

Director 的三种条件注入机制（图 5）反映了对条件信息利用方式的不同假设：

- **Director A（上下文前缀）**：将条件嵌入作为额外的上下文 token 前置到噪声轨迹序列中，依赖自注意力机制隐式地融合条件信息。这种方式信息瓶颈在于条件 token 的固定长度表示。
- **Director B（AdaLN 调制）**：通过自适应层归一化 $\mathrm{ADALN}(\gamma, \beta, x) = (1 + \gamma) \mathrm{LN}(X) + \beta$ 将条件信息注入每一层的归一化参数中，提供全局但粗粒度的条件控制。
- **Director C（交叉注意力）**：保留条件序列的完整长度，通过交叉注意力让去噪器在每个位置动态查询相关的文本和角色轨迹信息。实验表明，这种细粒度的条件交互在 FDCLaTr（3.76）和 CLaTr-Score（21.95）上均优于前两者，验证了保留条件序列完整时空结构的必要性。

### 需要手动验证的环节

以下环节的证据在现有分析中不够充分，建议在撰写时核实：

- **SLAHMR 位姿提取的精度与失败模式**：分析中提到存在噪声和片段不连续的风险，但未给出定量评估（如重投影误差分布或人工校验比例）。这直接影响 E.T. 数据集作为训练信号的可信度。
- **运动标注的阈值调参敏感性**：阈值法需要手动设置速度阈值来判定运动/静止边界，不同阈值可能导致轨迹片段划分不一致，进而影响文本描述的质量。当前分析未提供消融实验或参数敏感性分析。
- **CLaTr 嵌入在分布外数据上的泛化性**：CLaTr 与 Director 在相同数据集上训练，其作为评估指标的公正性尚未在独立电影或非电影数据上验证。

### 补充图表

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2407_01516/figures/006_Figure_5.jpg]]
*Figure 5: DiffusIon tRansformEr Camera TrajectORy (Director). We display 3 variants of our diffusion model Director. Director A incorporates the conditioning as in-context tokens. Director B leverages AdaLN modulation of the transformer block to add the conditioning. Director C uses the full text and character trajectory sequences by relying on cross-attention*

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2407_01516/figures/004_Figure_3.jpg]]
*Figure 3: Dataset creation pipeline. Given RGB frames from a video, we first extract and pre-process camera and character poses, then tag resulting camera and character trajectories (sequence of poses) to obtain rough independent descriptions (middle part). Finally, we translate these descriptions into rich textual captions, aligning the camera trajectory with that of the character (right part)*

## 核心模块与公式推导

### 问题形式化

Director 将相机轨迹生成问题建模为条件生成任务：给定角色轨迹序列和相机-角色关系文本描述，生成符合电影语法的全局坐标系相机轨迹。形式上，一条相机轨迹被定义为一个包含 $N$ 个连续相机位姿的序列 $\mathbf{x}_{1:N}$，每个位姿包含相机在全局坐标系中的位置和朝向信息。

### 扩散模型框架

Director 采用基于去噪分数匹配（Denoising Score Matching）的扩散框架进行训练。其核心损失函数为：

$$\mathcal{L}_{\mathrm{score}} = \big( D(\mathbf{x}, \mathbf{h}, c; \sigma) - \mathbf{x} \big) / \sigma^2$$

其中：
- $\mathbf{x}$ 为真实相机轨迹；
- $\mathbf{h}$ 为条件信息（角色轨迹与文本描述）；
- $c$ 为噪声强度控制参数；
- $\sigma$ 为当前噪声标准差；
- $D$ 为待训练的去噪器模块。

该损失函数的本质是训练去噪器 $D$ 从不同噪声水平的扰动轨迹中恢复原始轨迹，从而学得轨迹分布的条件梯度场。

### 三种条件注入机制

Director 设计了三种 Transformer 架构变体，以不同方式将角色轨迹和文本描述注入扩散去噪过程（见 Figure 5）：

**Director A（上下文前缀）**：将条件信息编码为上下文令牌（in-context tokens），直接拼接到噪声轨迹序列之前，通过自注意力机制实现条件融合。该方案最为简洁，但条件与轨迹之间的交互受限于前缀位置。

**Director B（AdaLN 调制）**：采用自适应层归一化（Adaptive Layer Normalization）进行条件调制，其核心操作为：

$$\mathrm{ADALN}(\gamma, \beta, x) = (1 + \gamma) \mathrm{LN}(X) + \beta$$

其中 $\gamma$ 和 $\beta$ 由条件信息通过可学习映射生成，$\mathrm{LN}$ 为标准层归一化。该调制操作被插入到每个自注意力和前馈层之前。遵循 **DiT**（Peebles & Xie, ICCV 2023）的设计，AdaLN 输出初始化为零，使模型从恒等映射开始训练，提升稳定性。每个自注意力和交叉注意力的输出还乘以可学习的缩放因子 $\lambda$ 进行残差缩放。

**Director C（交叉注意力）**：充分利用条件的完整序列长度。具体流程为：将 CLIP 编码的文本序列与线性投影后的角色轨迹序列拼接，经过两层 Transformer 编码器得到条件表示；在去噪 Transformer 的解码器中，通过交叉注意力层将该条件表示注入每一层。实验表明该方案性能最优（见 Table 2）。

### CLaTr 对比嵌入

CLaTr（Contrastive Language-Trajectory embedding）是用于评估生成质量的跨模态嵌入模块。它通过对比学习将文本描述和相机轨迹投影到共享的潜在嵌入空间，使得语义一致的文本-轨迹对在嵌入空间中距离更近。基于该嵌入空间，定义了两个核心评估指标：

- **FDCLaTr**：在 CLaTr 嵌入空间中计算生成轨迹分布与真实轨迹分布之间的 Fréchet 距离，衡量生成轨迹的整体质量；
- **CLaTr-Score**：计算生成轨迹嵌入与其对应文本嵌入之间的余弦相似度，衡量文本-轨迹的条件一致性。

### 关键设计决策

从坐标系选择来看，Director 放弃前人方法 **CCD** 使用的角色相对坐标系，转而采用全局坐标系。这一改变的因果机制在于：全局坐标系使模型能够显式学习相机运动与角色运动之间的空间偏移关系（如“相机在角色左侧跟拍”），而非将相机运动隐含在角色运动的相对变换中。这是实现角色感知相机轨迹生成的核心架构决策。

从条件粒度来看，Director 同时接受角色轨迹序列和文本描述作为条件，而非仅依赖文本。这使得模型在生成相机轨迹时能够参考角色的具体运动模式（如移动方向、速度变化），从而产生更符合电影语法的同步运动（如推拉镜头与角色走近的配合）。

## 实验与分析

### 主实验结果

我们在E.T.数据集的纯相机子集（pure subset）和混合子集（mixed subset）上对Director及其基线进行了系统评估。评估采用两类指标：轨迹质量指标（FDCLaTr、APDCLaTr、CLaTr-Score）和文本-相机一致性指标（C↑、R-Precision）。其中FDCLaTr衡量生成轨迹分布与真实轨迹分布之间的CLaTr嵌入距离（越低越好），CLaTr-Score衡量生成轨迹与对应文本描述的语义对齐度（越高越好）。

**Director C在所有指标上均显著超越基线。** 在最具挑战性的混合子集上，Director C的FDCLaTr降至3.76，相比CCD的35.81降低了32.05，相比MDM的6.79降低了3.03。在CLaTr-Score上，Director C达到21.95，远超CCD的6.26和MDM的18.32。这一巨大差距的核心原因在于CCD使用角色相对坐标系，无法建模相机与角色之间的复杂空间关系，而MDM虽为强基线但缺乏对角色轨迹的显式建模能力。Director通过全局坐标系和角色轨迹条件注入，成功捕捉了相机运动与角色运动之间的时空耦合。

在纯相机子集上（仅含相机轨迹描述，无角色信息），Director C的FDCLaTr为3.67，同样优于MDM的4.76和CCD的25.31，表明即使在不提供角色轨迹的条件下，Director的架构设计仍具有优势。

### 消融实验

**条件注入机制对比。** 我们对比了三种Transformer条件注入策略（Figure 5）：
- **Director A**（上下文前缀）：将条件作为输入序列的前缀token，FDCLaTr=3.88，CLaTr-Score=21.40
- **Director B**（AdaLN调制）：通过自适应层归一化注入条件，FDCLaTr=6.10，CLaTr-Score=16.36
- **Director C**（交叉注意力）：使用完整序列长度的交叉注意力，FDCLaTr=3.76，CLaTr-Score=21.95

交叉注意力机制（Director C）在两个指标上均取得最优，表明让模型在每一步去噪过程中动态关注文本和角色轨迹的完整序列信息，比静态前缀或全局调制更有效。AdaLN调制（Director B）表现最差，可能因为将变长序列条件压缩为固定维度的尺度和偏移参数，丢失了细粒度的时空对应关系。

**引导尺度权衡。** Figure 6展示了classifier-free guidance尺度在0.6至2.2范围内变化时，FDCLaTr与CLaTr-Score的权衡曲线。随着引导强度增加，CLaTr-Score（文本对齐度）持续提升，但FDCLaTr（分布质量）呈U型曲线——适度引导改善质量，过度引导则损害多样性。这一现象与文本到图像扩散模型中的观察一致。

### 失败模式分析

尽管Director取得了显著进展，我们识别出以下典型失败模式：

1. **轨迹精细度不足。** 当前文本描述缺乏对相机运动速度、幅度以及角色在屏幕上精确位置的修饰词，导致模型在某些场景下生成的轨迹在语义上正确但运动幅度或节奏与真实电影不符。例如，提示"camera trucks right to follow the character"可能生成正确方向的运动，但平移速度与角色步速不匹配。

2. **SLAHMR估计噪声传播。** 数据集构建依赖SLAHMR进行3D位姿估计，在遮挡严重或运动模糊的场景中，提取的轨迹存在噪声和片段不连续（Figure 10展示了块对齐前后的对比）。这些噪声直接进入训练数据，模型可能学到并放大这些伪影。

3. **多角色场景未处理。** 当前方法假设场景中仅有一个主要角色。当存在多个角色时，模型无法确定应以哪个角色的运动为参考，生成的相机轨迹可能出现语义混乱。

4. **评估指标的自洽偏差风险。** CLaTr嵌入与Director在相同数据集E.T.上训练，作为评价指标可能存在过拟合偏差。虽然CLaTr在检索任务上表现良好（R@1=19.73%，Table 3），但其在分布外数据上的评估可靠性尚未验证。

### 数据集规模与多样性分析

E.T.数据集包含115K样本、11M帧、约120小时内容，每个样本同时包含相机轨迹、角色轨迹以及两类文本描述（纯相机描述和相机-角色联合描述）。Table 1的对比显示，E.T.在样本数量上远超现有相机轨迹数据集CCD和RealEstate10K，且是唯一同时提供相机与角色轨迹及详细文本描述的数据集。Figure 4的统计分布表明，数据集覆盖了丰富的相机运动类型（平移、旋转、变焦等）和角色运动模式，为模型学习多样化的电影语法提供了基础。

### 定性结果

Figure 7展示了Director在四个维度上的定性表现：
- **可控性**：给定不同文本提示，模型生成语义匹配的相机轨迹
- **多样性**：相同条件下可生成多种合理的轨迹变体
- **复杂性**：能够处理包含多个运动阶段的复杂描述
- **角色感知**：相机运动与角色轨迹保持合理的空间关系

这些结果表明Director已初步具备电影级相机轨迹生成的能力，但需注意上述失败模式中提到的局限性。

### 补充图表

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2407_01516/figures/008_Table_2.jpg]]
*Table 2: Quantitative Results. Comparison of Director and concurrent methods on E.T. pure and mixed subsets, evaluating trajectory quality (left) and caption coherence (right). First best and second best*

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2407_01516/figures/003_Table_1.jpg]]
*Table 1: Dataset comparison. We compare the E.T. dataset to (i) two human motion datasets KIT [36] and HumanML3D [14]; and (ii) camera trajectory datasets RealEstate10K [53] and CCD [24]. Here the notion of sample is common across all datasets and corresponds to data associated with a continuous temporal sequence*

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2407_01516/figures/009_Figure_7.jpg]]
*Figure 7: Qualitative results. Generated camera trajectories with corresponding prompts and character trajectories, highlighting (a) controllability, (b) diversity, (c) complexity, and (d) character awareness. Darker shades indicate later frames*

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2407_01516/figures/005_Figure_4.jpg]]
*Figure 4: E.T. statistics*

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2407_01516/figures/014_Figure.jpg]]
*Figure: (a) Trajectory length (in #frames) (b) Camera length (in meters) (c) Character length (in meters)*

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2407_01516/figures/016_Figure_10.jpg]]
*Figure 10: Raw chunk alignment. We show in (a) the raw independent chunks just after the SLAHMR [50] extraction. In (b) we display the result of the chunk alignment process. Each color (red, blue, green) corresponds to a different chunk*

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2407_01516/figures/018_Figure.jpg]]
*Figure: (a) Overview of CLaTr framework. CLaTr projects (b) t-SNE visualization of CLaTr both text and camera trajectories into a common latent embedding of text (vivid colors) and space using encoders. Self-similarity is then computed, and trajectory (pastel colors). Each color a shared-weight decoder decodes both text and camera tra- corresponds to a K-Mean cluster of the jectory features back into a camera trajectory. text embedding*

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2407_01516/figures/001_Figure_1.jpg]]
*Figure 1: Different results generated by our camera trajectory diffusion system. Project page https://www.lix.polytechnique.fr/vista/projects/2024_et_courant*

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2407_01516/figures/010_Figure.jpg]]
*Figure: [Camera-only] ” throughout the entire shot.”The camera moves laterally to the left (trucking) (a)*

## 方法谱系与知识库定位

### 1. 方法演化与基线关系

E.T. 与 Director 的核心突破在于将**角色轨迹**显式地引入相机轨迹生成的条件空间，并采用**全局坐标系**替代前人使用的角色相对坐标系。这一转变直接回应了此前工作的根本瓶颈。

**与 CCD 的对比。** 前人工作 **CCD** 使用角色相对坐标系进行相机轨迹生成，其核心简化在于将相机运动表达为相对于角色的偏移量。这种设计虽然降低了学习难度，却从根本上牺牲了建模相机与角色之间复杂时空关系的能力——例如，当角色静止而相机执行推拉或横摇时，角色相对坐标系下的表示会退化为无意义的恒等映射。E.T. 的分析表明，CCD 在真实电影数据上表现极差：在 E.T. mixed 子集上，其 FD_CLaTr 高达 35.81，CLaTr-Score 仅为 6.26（Table 2），几乎不具有可用的文本-相机一致性。这一结果部分可归因于 CCD 原在合成数据上训练，直接迁移至真实电影数据存在分布偏移（见公平性说明），但其坐标系设计的结构性局限是更根本的原因。

**与 MDM 的对比。** **MDM**（Tevet et al., ICLR 2023）原为人体运动扩散模型，本文将其改编为相机轨迹生成的强基线。MDM 使用全局坐标系，但其条件输入仅为文本描述，缺乏对角色轨迹的显式建模。在 E.T. mixed 子集上，MDM 的 FD_CLaTr 为 6.79，CLaTr-Score 为 18.32（Table 2），显著优于 CCD 但仍远逊于 Director C（FD_CLaTr 3.76, CLaTr-Score 21.95）。这一差距表明，仅靠文本条件不足以捕捉电影语法中相机运动对角色运动的精细响应——角色轨迹作为结构化条件，提供了文本难以完整编码的运动先验。

**Director 的三条架构路径。** Director 探索了三种将文本与角色轨迹条件注入扩散 Transformer 的机制（Figure 5）：(A) 上下文前缀（in-context tokens），将条件序列拼接至噪声轨迹序列前端；(B) AdaLN 调制，通过自适应层归一化将条件信息注入每个 Transformer 块，其操作形式为 $\mathrm{ADALN}(\gamma, \beta, x) = (1 + \gamma) \mathrm{LN}(X) + \beta$（Equation 2），并采用 AdaLN-Zero 初始化以稳定训练；(C) 交叉注意力，使用完整的条件序列（CLIP 文本嵌入与线性投影后的角色轨迹拼接，经两层 Transformer 编码器处理）通过交叉注意力层与去噪轨迹交互。消融实验（Table 2）表明，交叉注意力机制（Director C）在轨迹质量与文本一致性上均最优（FD_CLaTr 3.76 vs. Director A 3.88 vs. Director B 6.10），说明保留完整的条件序列信息并通过注意力进行细粒度交互，优于将其压缩为前缀或全局调制参数。

### 2. 评估范式的演进

E.T. 工作同时推动了评估指标的升级。CCD 时代依赖基于简单六类动作分类器特征的评估，这种指标粒度粗、无法捕捉轨迹的语义一致性。本文提出的 **CLaTr**（Contrastive Language-Trajectory embedding）通过对比学习将文本与轨迹映射到联合嵌入空间，在文本-轨迹检索任务上达到 R@1=19.73%（Table 3），并据此定义了 FD_CLaTr（轨迹质量）和 CLaTr-Score（文本-相机一致性）两个指标。这一评估框架的引入，使得生成模型的优化目标从“生成看起来合理的轨迹”转向“生成与文本描述语义对齐的轨迹”，是相机轨迹生成领域评估标准的重要升级。

### 3. 适用边界与局限

**数据依赖与分布约束。** E.T. 数据集基于 Condensed Movies Dataset (CMD) 构建，涵盖 115K 样本、11M 帧、120 小时的真实电影数据（Section 3.1, Table 1），其轨迹分布受限于电影领域的拍摄语法。Director 在此分布上训练，其生成能力天然偏向电影风格的相机运动模式。在体育转播、监控录像、用户生成内容等非电影场景中，相机运动规律可能截然不同（如体育中的快速摇摄、监控中的固定视角），Director 的泛化能力尚未验证。

**文本描述的表达粒度。** 当前 E.T. 的文本描述未包含相机运动的速度、幅度等修饰词，也未编码角色在屏幕上的精确位置（如“角色位于画面左侧三分之一处”）。这限制了 Director 对精细拍摄意图的响应能力。例如，用户无法指定“缓慢推近”与“快速推近”的区别，或要求角色始终保持在画面的特定构图位置。

**单角色假设。** 方法目前仅考虑单个主要角色的轨迹作为条件，未处理多角色场景。在多人对话、群像戏等常见电影场景中，相机运动往往需要同时响应多个角色的位置与运动，这一能力的缺失是向实用化迈进的关键瓶颈。

**评估的自洽偏差风险。** CLaTr 嵌入与 Director 在相同数据集 E.T. 上训练，作为评价指标可能存在自洽偏差——即 CLaTr 可能对 Director 生成轨迹的分布存在偏好，从而高估其质量。在独立的外部数据集上验证 CLaTr 指标的鲁棒性，是确立其作为通用评估标准的前提。

**数据构建管线的噪声。** 数据集构建依赖 SLAHMR 进行 3D 位姿估计，存在估计噪声和片段不连续的风险（Figure 10 展示了块对齐过程）；运动标注使用基于速度的阈值法，需要手动调参（Section 3.2）。这些噪声可能以隐式方式影响生成模型的学习目标。

### 4. 开放问题

1. **精细文本控制。** 如何扩展文本描述的表达力，使其包含运动修饰词（速度、幅度、缓入缓出）以及角色在画面中的精确构图位置？这可能需要更结构化的标注方案或更大规模的视觉-语言模型辅助。

2. **评估指标的独立验证。** 在更复杂、更多样的轨迹分布上（如非电影数据），CLaTr 嵌入相比 CCD 专用分类器特征的评估优势是否依然成立？是否需要在多个异构数据集上训练 CLaTr 以提升其作为通用指标的鲁棒性？

3. **端到端视频生成集成。** 如何将 Director 生成的相机轨迹与视频扩散模型结合，实现从文本到相机轨迹再到渲染视频的端到端管线？这涉及轨迹表示与视频生成模型条件接口的对齐问题。

4. **跨域泛化。** Director 在体育、纪录片、用户生成内容等不同视觉领域的泛化能力如何？是否需要域适应或微调策略？

5. **多角色场景建模。** 如何处理多角色场景下的相机轨迹生成，并使生成的相机运动保持电影语法的连贯性（如正反打、群体构图等）？这可能需要引入角色间的交互建模和图结构条件。

## 原文 PDF

![[paperPDFs/ECCV_2024/E_T_the_Exceptional_Trajectories_Text_to_camera_trajectory_generation_with_character_awareness.pdf]]
