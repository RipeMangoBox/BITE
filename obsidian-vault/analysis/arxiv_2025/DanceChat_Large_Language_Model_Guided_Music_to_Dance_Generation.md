---
title: "DanceChat: Large Language Model-Guided Music-to-Dance Generation"
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: paperPDFs/arxiv_2025/DanceChat_Large_Language_Model_Guided_Music_to_Dance_Generation.pdf
project_link: null
code_link: null
aliases:
- DanceChat
tags:
- arxiv_2025
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 利用大语言模型（LLM）作为伪编舞师，从结构化音乐描述中生成高层文本舞蹈指令，作为语义桥梁。
primary_logic: 将LLM生成的文本舞蹈指令与音乐节拍特征融合，通过多模态对齐损失，以文本为中介增强音乐与舞蹈的语义联系，从而生成节奏对齐、风格多样的舞蹈动作。
claims:
- 在AIST++数据集上，DanceChat在PFC指标上达到0.828，较SOTA方法Beat-it（0.966）提升0.138。
- 消融实验表明，融合音乐、节拍和文本三种模态后，BAS达到0.28，PFC和Div_k均显著优于单模态配置。
- 多模态对齐损失进一步将PFC从0.843降至0.828，Div_k从9.85提升至10.64，验证了其有效性。
- 用户研究中，DanceChat相对于EDGE在AIST++上的偏好率达60.00%，在in-the-wild音乐上达66.36%。
---

# DanceChat: Large Language Model-Guided Music-to-Dance Generation

> [!tip] 核心洞察
> 将LLM生成的文本舞蹈指令与音乐节拍特征融合，通过多模态对齐损失，以文本为中介增强音乐与舞蹈的语义联系，从而生成节奏对齐、风格多样的舞蹈动作。

| 字段 | 内容 |
|------|------|
| 中文题名 | DanceChat: 大语言模型引导的音乐到舞蹈生成 |
| 英文题名 | DanceChat: Large Language Model-Guided Music-to-Dance Generation |
| 会议/期刊 | arXiv 2025 |
| Links | [paper](https://arxiv.org/abs/2506.10574) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | DanceChat |
| Dataset | AIST++ |

> [!tip] 效果简介
> - AIST++ 上，PFC（Physical Foot Contact）↓ 0.828 vs 0.966（Beat-it） (-0.138)；Div_k（Kinematic Diversity）→（越接近GT 10.61越好） 10.64 vs 10.85（FACT）/ 9.66（Beat-it） (最接近真实分布，全面优于基线)；Div_g（Geometric Diversity）→（越接近GT 7.48越好） 7.36 vs 7.72（Bailando）/ 6.76（BADM） (所有方法中最佳，最接近真实分布)。
> - 用户研究（AIST++） 上，偏好率（%）↑ 86.25% vs FACT; 61.88% vs Bailando; 60.00% vs EDGE vs 50%（随机水平） (显著优于各基线)。

## 概要

### 问题背景与核心瓶颈

音乐到舞蹈生成（Music-to-Dance Generation）面临一个根本性挑战：音乐与舞蹈动作之间存在巨大的语义鸿沟。音乐是高度抽象的时序信号，而舞蹈是空间-时间维度上的高维人体运动序列，从音乐到运动的映射本质上是**一对多、不适定的**。此外，高质量的配对音乐-舞蹈数据稀缺，使得现有方法难以学习丰富的舞蹈模式，往往缺乏对运动内容的显式语义指导。这构成了该领域的核心瓶颈。

### 核心思路：LLM作为语义桥梁

DanceChat 的核心洞察在于引入**大语言模型（LLM）作为“伪编舞师”**，将结构化音乐描述转化为高层的文本舞蹈指令，从而以**语言为中间模态**弥合音乐与运动之间的语义鸿沟。这一设计的直觉来源于真实世界的舞蹈学习场景：学习者依赖编舞师将音乐“翻译”为可执行的动作描述。DanceChat 将这一过程自动化——LLM 接收从音乐中提取的节拍、调性、和弦等结构化描述，生成类似 HumanML3D 风格的文本舞蹈指令，为后续的运动生成提供显式的语义引导。

### 方法定位

从方法谱系来看，DanceChat 属于**多模态条件扩散生成**框架，其创新点在于将文本指令作为一种新的条件模态引入音乐驱动舞蹈生成。与现有方法相比，DanceChat 在以下维度上形成了差异化定位：

- **语义引导方式**：传统方法（如 **EDGE**，Tseng et al., CVPR 2023；**BADM**，Zhang et al., CVPR 2024）仅依赖音乐的抽象特征嵌入，缺乏对“跳什么”的显式描述。DanceChat 利用 LLM 生成与音乐结构对齐的文本舞蹈指令，使生成过程具备可解释的语义锚点。
- **多模态融合策略**：部分工作（如 **Beat-it**，Huang et al., ECCV 2024）虽引入了节拍信息，但未系统整合文本语义。DanceChat 提出分层融合机制——先将音乐与节拍嵌入进行加性融合以增强节奏感知，再与文本指令嵌入拼接，形成统一的跨模态条件表示。
- **跨模态对齐机制**：DanceChat 引入多模态对齐损失，以文本嵌入为桥梁，通过余弦相似度同时拉近音乐-文本和运动-文本的嵌入距离，显式缩小跨模态语义鸿沟。这是现有舞蹈生成方法中未曾采用的技术手段。

### 主要结果概要

在公开数据集 AIST++ 上，DanceChat 在多个关键指标上取得了领先表现：

- **物理真实性**：PFC（Physical Foot Contact）指标达到 **0.828**，较此前最优方法 Beat-it（0.966）降低 0.138，表明生成舞蹈的足部接触模式更接近真实物理规律。
- **运动多样性**：Div_k（运动学多样性）达到 **10.64**，在所有对比方法中最接近真实数据分布（GT = 10.61）；Div_g（几何多样性）达到 **7.36**，同样为所有方法中最佳。
- **节拍对齐**：BAS（Beat Alignment Score）达到 **0.27**，位列第二，仅次于专门优化节拍对齐的 Beat-it（0.66）。
- **用户偏好**：在 AIST++ 测试集上，DanceChat 相对于 EDGE 的用户偏好率达 **60.00%**；在 in-the-wild 音乐上，该比例进一步提升至 **66.36%**，验证了方法在开放场景下的泛化潜力。

消融实验进一步证实，音乐、节拍和文本三种模态的融合对舞蹈质量均有独立贡献，而多模态对齐损失则显著提升了物理真实性与运动多样性，验证了以文本为语义中介这一设计原则的有效性。



### 问题背景：音乐到舞蹈生成的语义鸿沟

音乐驱动的舞蹈生成任务旨在根据输入的音乐片段合成逼真且风格多样的3D人体舞蹈动作序列。该任务的核心挑战在于**音乐与舞蹈动作之间存在巨大的语义鸿沟**：音乐是高度抽象的时间序列信号，而舞蹈动作是连续、高维的人体姿态序列，二者之间的映射关系天然具有一对多（one-to-many）和不适定（ill-posed）的特性。同一段音乐可以对应多种完全不同的舞蹈编排，这使得从音乐到动作的直接映射极为困难。

此外，**高质量的音乐-舞蹈配对数据十分稀缺**。现有数据集规模有限，且覆盖的舞蹈风格和音乐类型较为单一，导致模型难以学习到多样化的舞蹈模式。缺乏显式的运动指导进一步加剧了这一问题——现有方法大多直接从音乐抽象特征中回归或生成动作，缺少对“跳什么动作”这一关键信息的显式建模。

### 现有方法及其局限

当前音乐到舞蹈生成方法主要分为两类：

**基于回归的方法**如 **FACT**（Li et al., ICCV 2021）采用Transformer架构直接建立音乐到动作的映射，**Bailando**（Siyao et al., CVPR 2022）则基于VQ-VAE和actor-critic框架进行舞蹈生成。这些方法通常需要起始姿态作为条件，且缺乏对舞蹈动作高层语义的显式理解。

**基于扩散模型的方法**如 **EDGE**（Tseng, Castellon and Liu, CVPR 2023）、**BADM**（Zhang et al., CVPR 2024）和 **Beat-it**（Huang et al., ECCV 2024）利用扩散过程的强大生成能力取得了显著进展。其中Beat-it通过显式建模节拍信息在节拍对齐方面表现突出，但这些方法仍然主要依赖音乐的低层抽象特征（如频谱特征），缺乏对舞蹈动作结构、风格和节奏模式的高层语义指导。

所有现有方法共享一个根本性局限：**它们缺乏一个显式的语义桥梁来连接音乐与动作**。这导致生成的舞蹈在物理真实性、运动多样性和节拍对齐性之间难以取得平衡——例如，Beat-it在节拍对齐上表现优异（BAS=0.66），但运动多样性（Div_k=9.66）明显偏离真实分布（GT=10.61）。

### 本文动机：LLM作为伪编舞师

本文的动机源自对人类舞蹈学习过程的观察：在真实世界中，舞蹈学习者依赖编舞师将音乐“翻译”为具体的动作指令（如“快速旋转”、“缓慢伸展手臂”）。编舞师充当了音乐与动作之间的语义中介，将抽象的音乐信息转化为结构化的文本描述。

基于这一洞察，**DanceChat提出利用大语言模型（LLM）作为伪编舞师**，从结构化的音乐描述中生成高层的文本舞蹈指令，以此作为连接音乐与舞蹈的语义桥梁。文本作为一种结构化、可解释的中间表征，能够有效缩小音乐到动作的语义鸿沟：音乐首先被解析为节拍、和弦、调性等结构化描述，LLM再将这些描述“翻译”为类似人类编舞指令的文本（如“a person dances with quick arm movements and slow leg movements”），最终这些文本指令与音乐特征共同引导扩散模型生成舞蹈动作。

这一设计使得模型能够显式地获得“跳什么”的语义指导，而非仅仅从音乐特征中隐式推断动作模式，从而有望在保持节拍对齐的同时显著提升运动多样性和物理真实性。



## 核心方法与创新机理

DanceChat 的核心创新在于引入**大语言模型（LLM）作为伪编舞师**，将音乐到舞蹈的映射问题从低级的特征回归提升为**语义中介的跨模态对齐**。这一思路直接针对音乐与舞蹈动作之间的语义鸿沟瓶颈，通过结构化的文本舞蹈指令为运动生成提供了显式的语义引导。

### 创新一：LLM驱动的文本舞蹈指令生成

现有方法（如 **FACT**（Li et al., ICCV 2021）、**EDGE**（Tseng, Castellon and Liu, CVPR 2023））仅从音乐中提取抽象特征作为生成条件，缺乏对“跳什么动作”的显式描述。DanceChat 改变了这一范式：它首先从音乐中提取结构化字幕（速度、和弦、调性、节拍结构），然后通过精心设计的提示工程引导 LLM 生成 HumanML3D 风格的舞蹈动作指令（Section 3.3, Figure 3）。这些文本指令充当了音乐语义与运动语义之间的**可解释桥梁**，将原本一对多、病态的音乐-运动映射转化为更可控的文本-运动映射。

### 创新二：分层多模态融合策略

在条件嵌入的构建上，DanceChat 采用**分层融合**而非简单的特征拼接（Section 3.4, Equations (1)(2)）。具体而言：
- **音乐-节拍节奏融合**：通过相加操作 $E_{M}' = E_{M} + E_{B}$ 将节拍嵌入直接注入音乐嵌入，增强节奏感知；
- **音乐-文本语义融合**：将融合了节拍的音乐嵌入与文本指令嵌入拼接 $E_{F} = [E_{M}'; E_{T}]$，形成统一条件嵌入。

消融实验（Table 3）验证了这一设计的有效性：仅使用音乐（M）时 PFC=1.536，加入节拍（M+B）后降至 1.066 且 BAS 升至 0.27；加入文本（M+T）后 Div_k 升至 9.69，但 BAS 降至 0.26；而融合全部三种模态（M+B+T）获得最高 BAS 0.28，且 PFC 和 Div_k 均表现优异。这表明分层融合策略有效平衡了**节奏对齐**与**运动多样性**。

### 创新三：以文本为中介的多模态对齐损失

DanceChat 提出了**多模态对齐损失** $\mathcal{L}_{\mathrm{align}}$（Equation (8)），以文本嵌入为语义桥梁，同时拉近音乐-文本和运动-文本的余弦相似度：

$$\mathcal{L}_{\mathrm{align}} = \frac{1}{N} \sum_{i=1}^{N} [(1 - \mathrm{sim}(E_{t_i}, E_{m_i})) + (1 - \mathrm{sim}(E_{t_i}, E_{x_i}))]$$

这一设计的关键洞察在于：**文本指令作为显式语义锚点**，能够同时约束音乐编码器和运动解码器向相同的语义空间对齐。消融实验（Table 3 的 MM Align. Loss 行）表明，加入该损失后 PFC 从 0.843 进一步降至 0.828，Div_k 从 9.85 提升至 10.64（最接近真实分布 10.61），验证了其跨模态融合的积极贡献。

### 方法谱系与知识库定位

DanceChat 在舞蹈生成方法谱系中占据**扩散模型 + LLM语义引导**的交叉位置。与基于回归的方法（FACT）、基于 VQ-VAE 的方法（**Bailando**（Siyao et al., CVPR 2022））以及纯扩散方法（EDGE、**BADM**（Zhang et al., CVPR 2024））相比，DanceChat 首次将 LLM 引入舞蹈生成管线。与同样关注节拍同步的 **Beat-it**（Huang et al., ECCV 2024）相比，DanceChat 不依赖专门的节拍优化模块，而是通过文本指令间接提升节奏对齐——这解释了其 BAS（0.27）虽不及 Beat-it（0.66）但 PFC 和多样性指标全面领先的原因。



DanceChat 的整体 pipeline 围绕一个核心思想展开：**用大语言模型（LLM）作为“伪编舞师”，将音乐信号翻译为结构化的文本舞蹈指令，再以文本为语义桥梁，连接音乐与舞蹈动作**。这一设计直接针对音乐到舞蹈生成中的根本瓶颈——音乐与运动之间的巨大语义鸿沟，以及配对舞蹈数据稀缺导致模型难以学习多样化舞蹈模式的问题。

### 三模块架构

如图 2 所示，DanceChat 由三个顺序衔接的模块构成，形成一条完整的信息流：**原始音乐 → 文本舞蹈指令 → 多模态融合嵌入 → 舞蹈动作序列**。

1.  **舞蹈指令生成模块（Dance Instruction Generation）**
    该模块负责将音乐转化为高层文本舞蹈指令。它首先从输入音乐中提取结构化的音乐字幕（music caption），包含**速度（tempo）、节拍（beat）、调性（key）、和弦（chord）**等符号化描述符；随后，利用 LLM（具体实现中使用 ChatGPT-4o API）根据这些字幕生成 HumanML3D 风格的文本舞蹈指令，例如描述身体部位的运动方式、动作的力度和节奏特征等。这一过程将抽象的音乐特征转化为显式的运动描述，为后续模块提供了可解释的语义条件。

2.  **多模态融合模块（Multi-modal Fusion）**
    该模块将来自不同模态的特征编码并分层融合为统一的条件嵌入。具体而言：
    - **音乐特征**：使用冻结的 Jukebox 模型提取，再经两层 Transformer 编码器精炼，得到音乐嵌入 $E_M$。
    - **节拍特征**：通过节拍编码器提取节拍嵌入 $E_B$。
    - **文本特征**：将 LLM 生成的文本指令通过基于 CLIP 的编码器和 Transformer 编码，得到文本嵌入 $E_T$。
    
    融合过程采用**分层策略**：首先通过加法将节拍信息直接注入音乐嵌入，实现**音乐-节拍节奏融合**（$E_{M}' = E_{M} + E_{B}$）；随后将融合了节拍的音乐嵌入与文本指令嵌入进行拼接，完成**音乐-文本语义融合**（$E_{F} = [E_{M}'; E_{T}]$）。这种设计使得最终的条件嵌入 $E_F$ 同时携带了音乐的节奏信息与文本的语义指导。

3.  **扩散运动合成模块（Diffusion-based Motion Synthesis）**
    该模块以融合嵌入 $E_F$ 为条件，通过扩散模型生成最终的舞蹈动作序列。模型在训练时逐步向真实运动 $\mathbf{x}_0$ 添加高斯噪声至接近白噪声 $\mathbf{z}_t$，再学习从噪声中恢复原始运动。推理时，从随机噪声出发，在条件嵌入的引导下逐步去噪，生成与音乐节奏对齐、与文本指令语义一致的舞蹈动作。

### 输入输出流

整个 pipeline 的输入为一段原始音乐，输出为 $N$ 帧的舞蹈运动序列 $\mathcal{X} = \{ x^1, x^2, \ldots, x^N \}$，每帧 $x^i \in \mathbb{R}^{151}$ 包含 24 个关节的 6-DOF 旋转、根节点位移及双脚接触标签。信息流的关键转换节点为：**音乐 → 音乐字幕 → 文本指令 → 多模态嵌入 → 舞蹈动作**，其中文本指令起到了连接音乐语义与运动语义的桥梁作用。

### 补充图表

![[assets/figures/papers/paper_list_l23_https_arxiv_org_abs_2506_10574/figures/002_Figure_2.jpg]]
*Figure 2: Overview of our approach. DanceChat consists of three main components: (a) Dance Instruction Generation module extracts music caption (tempo, key, chord, etc.) from the given music condition, (b) Multi-modal Fusion module integrates the encoded representations of music, beats, and text into a unified conditional embedding, and (c) Diffusion-based Motion Synthesis module uses this unified embedding to guide the generation of realistic dance movement*

![[assets/figures/papers/paper_list_l23_https_arxiv_org_abs_2506_10574/figures/001_Figure_1.jpg]]
*Figure 1: Our approach draws inspiration from real-world dance learning, where learners rely on choreographers to interpret music. DanceChat leverages LLMs as pseudochoreographers to translate music into textual instructions, bridging the semantic gap between music and motion. While the mapping from music to motion is inherently one-tomany and ill-posed, text offers a more structured and interpretable intermediary*



DanceChat 围绕“以文本指令为语义桥梁，弥合音乐与舞蹈动作鸿沟”这一核心洞察，将系统拆解为三个关键模块：**舞蹈指令生成模块**、**多模态分层融合模块** 和 **基于扩散的运动合成模块**。各模块协同运作，其公式体系完整定义了从音乐到舞蹈的生成过程。

### 3.1 问题定义与运动表示

舞蹈运动序列被形式化为一组连续的人体姿态向量。给定一段音乐输入，目标是生成与之语义和节奏对齐的 $N$ 帧舞蹈动作。

运动序列表示为：

$$\mathcal{X} = \{ x^1, x^2, \ldots, x^N \}, \quad x^i \in \mathbb{R}^{D}, \, D=151$$

其中每一帧 $x^i$ 的 151 维向量由三部分拼接构成：24 个关节的 6-DOF 旋转表示（144 维）、根节点全局位移（3 维）以及双脚与地面的二值接触标签（4 维）。这一表示同时编码了姿态的运动学信息和物理接触约束，为后续的扩散生成和接触一致性损失提供了统一的数据结构。

### 3.2 舞蹈指令生成模块

该模块是 DanceChat 区别于现有方法的核心创新点，其功能是将抽象的音乐信号转化为结构化的文本舞蹈指令，充当“伪编舞师”角色。模块包含两个关键步骤：

1. **音乐字幕构建**：基于 Mustango 框架，从原始音乐中提取四个结构化符号描述符——速度（tempo）、和弦（chords）、调性（keys）和节拍结构（beat structure），并按照受控模板构造自然语言音乐描述。
2. **LLM 指令生成**：将音乐字幕输入大语言模型（ChatGPT-4o API），通过精心设计的提示工程，引导 LLM 生成 HumanML3D 风格的文本舞蹈指令。这些指令包含动作类型、身体部位运动描述、节奏变化等高层语义信息，作为音乐与运动之间的可解释中间表征。

该模块的详细流程见 **Figure 3**，生成示例见 **Figure 4** 中各运动序列下方的文本描述。

![[assets/figures/papers/paper_list_l23_https_arxiv_org_abs_2506_10574/figures/003_Figure_3.jpg]]
*Figure 3: Details of our LLM-based textual instruction generation process. The prompt guides an LLM to generate HumanML3D-style dance instructions*

### 3.3 多模态分层融合模块

多模态融合模块接收三种异构特征——音乐嵌入 $E_M \in \mathbb{R}^{d_M}$、节拍嵌入 $E_B$ 和文本指令嵌入 $E_T \in \mathbb{R}^{d_T}$——并将其整合为统一的条件嵌入，以引导后续的扩散生成。融合采用分层策略，先进行节奏层融合，再进行语义层融合。

**音乐-节拍节奏融合**（加法融合）：

$$E_{M}' = E_{M} + E_{B}$$

该设计将节拍信息通过加法直接注入音乐嵌入，使得融合后的表示 $E_{M}'$ 同时携带旋律特征和精确的节拍时间信息，增强模型对音乐节奏结构的感知能力。消融实验证实，仅此一步即可将 BAS 从 0.23 提升至 0.27（见 **Table 3** 中 M vs. M+B 行）。

**音乐-文本语义融合**（拼接融合）：

$$E_{F} = [E_{M}'; E_{T}]$$

将已融合节拍的音乐嵌入 $E_{M}'$ 与文本指令嵌入 $E_T$ 沿特征维度拼接，形成最终的统一条件嵌入 $E_F$。文本指令在此充当语义桥梁，将音乐的高层结构（如“快节奏的旋转动作”“缓慢的手臂伸展”）显式地传递给运动生成模块，弥补了纯音乐特征在语义表达上的不足。

音乐特征通过冻结的 Jukebox 模型提取，并经两层 Transformer 编码器精炼；文本特征由基于 CLIP 的编码器提取，同样经过 Transformer 编码层处理。

### 3.4 基于扩散的运动合成模块

运动合成采用条件扩散模型框架。以统一条件嵌入 $E_F$ 为引导，扩散模型从随机噪声逐步去噪，生成与音乐语义和节拍对齐的舞蹈运动序列。

**前向扩散过程**：逐步向原始运动 $\mathbf{x}_0$ 添加高斯噪声，$t$ 步后得到噪声隐变量 $\mathbf{z}_t$：

$$q(\mathbf{z}_t | \mathbf{z}_{t-1}) = \mathcal{N}(\sqrt{1-\beta_t} \mathbf{z}_{t-1}, \beta_t I)$$

其中 $\beta_t$ 为预定义的噪声调度参数。

**简化训练目标**：模型学习预测原始运动 $\mathbf{x}_0$，主损失为预测运动 $\hat{\mathbf{x}}_{\theta}$ 与真实运动之间的均方误差：

$$\mathcal{L}_{\mathrm{simple}} = \mathbb{E}_{\mathbf{x}, t} [\| \mathbf{x}_0 - \hat{\mathbf{x}}_{\theta}(\mathbf{z}_t, t, E_F) \|_2^2]$$

**运动学辅助损失**：为提升生成动作的物理合理性，引入三项运动学约束：

- **关节位置损失**：通过前向运动学（FK）计算关节三维位置，约束生成动作的空间结构：

$$\mathcal{L}_{\mathrm{joint}} = \frac{1}{N} \sum_{i=1}^{N} \| \mathbf{FK}(\mathbf{x}_i) - \mathbf{FK}(\hat{\mathbf{x}}_i) \|_2^2$$

- **速度损失**：约束相邻帧之间的关节速度一致性，确保动作流畅：

$$\mathcal{L}_{\mathrm{vel}} = \frac{1}{N-1} \sum_{i=1}^{N-1} \| (\mathbf{x}_{i+1} - \mathbf{x}_i) - (\hat{\mathbf{x}}_{i+1} - \hat{\mathbf{x}}_i) \|_2^2$$

- **接触一致性损失**：利用脚部接触标签 $\hat{\mathbf{b}}_i$，强制在接触帧期间脚部不发生滑动：

$$\mathcal{L}_{\mathrm{contact}} = \frac{1}{N-1} \sum_{i=1}^{N-1} \| (\mathbf{FK}(\mathbf{x}_{i+1}) - \mathbf{FK}(\hat{\mathbf{x}}_i)) \cdot \hat{\mathbf{b}}_i \|_2^2$$

**多模态对齐损失**：这是 DanceChat 实现跨模态语义桥接的关键损失项。以文本嵌入 $E_{t_i}$ 为中介，通过余弦相似度同时拉近音乐-文本和运动-文本在嵌入空间中的距离：

$$\mathcal{L}_{\mathrm{align}} = \frac{1}{N} \sum_{i=1}^{N} [(1 - \mathrm{sim}(E_{t_i}, E_{m_i})) + (1 - \mathrm{sim}(E_{t_i}, E_{x_i}))]$$

其中 $\mathrm{sim}(\cdot, \cdot)$ 为余弦相似度，$E_{m_i}$ 和 $E_{x_i}$ 分别为第 $i$ 帧对应的音乐嵌入和运动嵌入。消融实验表明，加入该损失后 PFC 从 0.843 降至 0.828，Div_k 从 9.85 升至 10.64（见 **Table 3** 中 MM Align. Loss 行），验证了其对齐效果。

**总损失**：所有损失项的加权组合：

$$\mathcal{L} = \mathcal{L}_{\mathrm{simple}} + \lambda_{\mathrm{joint}} \mathcal{L}_{\mathrm{joint}} + \lambda_{\mathrm{vel}} \mathcal{L}_{\mathrm{vel}} + \lambda_{\mathrm{contact}} \mathcal{L}_{\mathrm{contact}} + \lambda_{\mathrm{align}} \mathcal{L}_{\mathrm{align}}$$

各权重系数 $\lambda$ 在训练中平衡不同约束的贡献强度。



## 实验与关键发现

### 核心瓶颈与因果机制

音乐到舞蹈生成的核心瓶颈在于音乐与舞蹈动作之间存在巨大的语义鸿沟，且配对舞蹈数据稀缺，导致现有模型难以学习多样化舞蹈模式，缺乏显式的运动指导。DanceChat通过引入大语言模型（LLM）作为伪编舞师，从结构化音乐描述中生成高层文本舞蹈指令，以此作为语义桥梁。其核心洞察在于：将LLM生成的文本舞蹈指令与音乐节拍特征融合，通过多模态对齐损失，以文本为中介增强音乐与舞蹈的语义联系，从而生成节奏对齐、风格多样的舞蹈动作。

### 主实验结果

在AIST++数据集上，DanceChat与现有方法进行了全面的定量比较，结果如Table 1所示。DanceChat在物理真实性指标PFC（Physical Foot Contact）上达到0.828，较当前最优方法**Beat-it**（Huang et al., ECCV 2024）的0.966提升了0.138，表明生成动作的脚部接触物理合理性显著增强。在运动多样性方面，DanceChat的Kinematic Diversity（Div_k）达到10.64，Geometric Diversity（Div_g）达到7.36，两项指标均为所有方法中最接近真实分布（GT：10.61和7.48）的值，验证了文本指令引导对多样化运动模式学习的有效性。在节拍对齐指标BAS（Beat Alignment Score）上，DanceChat获得0.27，位列第二，仅次于专门优化节拍对齐的Beat-it（0.66），说明文本指令的引入在提升多样性与物理真实性的同时，对节拍对齐性能有一定权衡。

用户研究结果（Table 2）进一步验证了DanceChat的感知质量优势。在AIST++测试集上，DanceChat相对于**FACT**（Li et al., ICCV 2021）的偏好率达86.25%，相对于**Bailando**（Siyao et al., CVPR 2022）达61.88%，相对于**EDGE**（Tseng et al., CVPR 2023）达60.00%。在in-the-wild音乐上，DanceChat相对于EDGE的偏好率达66.36%，表明该方法对训练集外音乐具有较好的泛化能力。

![[assets/figures/papers/paper_list_l23_https_arxiv_org_abs_2506_10574/figures/005_Table_2.jpg]]
*Table 2: User study results on AIST++ test set and in-thewild music. We present the Preference Rate ↑ of user evaluations that prefer DanceChat (Ours) to FACT (Li et al. 2021), Bailando (Siyao et al. 2022), and EDGE (Tseng, Castellon, and Liu 2023)*

### 消融实验

Table 3报告了模态消融和多模态对齐损失消融的结果。仅使用音乐特征（M）时，PFC为1.536，Div_k为9.48，BAS为0.23，物理真实性较差。加入节拍信息后（M+B），PFC降至1.066，BAS提升至0.27，表明节拍信息显著改善了物理真实性与节奏对齐。加入文本指令后（M+T），PFC降至1.166，Div_k提升至9.69，但BAS降至0.26，说明文本指导提升了运动多样性和真实性，但缺少节拍信息导致节拍对齐下降。融合全部三种模态（M+B+T）获得最高BAS 0.28，且PFC和Div_k表现出色。额外加入多模态对齐损失后，PFC进一步降至0.828，Div_k提升至10.64，验证了该损失对跨模态融合的积极贡献。

### 关键图表结论

- **Table 1**：DanceChat在物理真实性与运动多样性指标上全面优于现有方法，节拍对齐性能位居第二。
- **Table 2**：用户偏好率在多种基线对比下均显著优于随机水平（50%），在in-the-wild音乐上同样保持优势。
- **Table 3**：三模态融合与多模态对齐损失是性能提升的关键，消融实验验证了各组件的独立贡献。

![[assets/figures/papers/paper_list_l23_https_arxiv_org_abs_2506_10574/figures/004_Table_1.jpg]]
*Table 1: Quantitative comparison with state-of-the-art methods on the AIST++ dataset. FACT and Bailando are Transformerand VQ-VAE-based models that require a starting pose. EDGE, BADM, and Beat-it are diffusion-based approaches. ↑ means higher is better, ↓ means lower is better, → means closer to ground truth is better. Bold indicated the best result; underline indicates the second-best. Our method outperforms the other methods on*

![[assets/figures/papers/paper_list_l23_https_arxiv_org_abs_2506_10574/figures/007_Table_3.jpg]]
*Table 3: Ablation study of modalities, where M indicates music, B indicates beat and T indicates text. The best results are indicated in bold, and the second best are underlined*

### 失败模式与局限性

尽管DanceChat在多项指标上表现优异，仍存在以下局限：LLM生成的文本指令质量高度依赖LLM的能力和提示工程，可能无法覆盖所有舞蹈风格；方法仅在AIST++数据集上验证，对其他舞蹈类型或音乐风格的泛化性未充分测试；节拍对齐性能（BAS）虽有所提升，但仍不及专门优化节拍对齐的方法（如Beat-it）；训练需使用多个预训练模型（Jukebox、CLIP、HumanML3D权重），增加了部署复杂度。这些局限需要在未来工作中进一步解决。

### 补充图表

![[assets/figures/papers/paper_list_l23_https_arxiv_org_abs_2506_10574/figures/006_Figure_4.jpg]]
*Figure 4: Example results generated by our model. Each sequence illustrates a 3D dance motion generated from a given music clip, conditioned on an LLM-generated textual instruction. The sentences below each motion sequence are produced by the LLM and serve as choreography prompts*



## 定位与知识库关联

**核心瓶颈与因果机制**

音乐到舞蹈生成的核心瓶颈在于音乐信号与人体运动之间存在巨大的语义鸿沟：音乐是抽象、连续的声学信号，而舞蹈动作是高维、结构化的运动序列，两者之间的映射天然是一对多且病态的。现有方法（见下文基线谱系）主要依赖从音乐中提取的抽象特征直接预测运动，缺乏显式的运动描述作为中间语义桥梁。DanceChat的因果旋钮在于引入大语言模型（LLM）作为“伪编舞师”——从结构化的音乐描述（速度、和弦、调性、节拍结构）中生成高层的文本舞蹈指令，以此作为语义中介。这一设计的核心洞察是：文本作为一种结构化、可解释的中间表示，能够比原始音乐特征更有效地传递编舞意图，从而缩小音乐与运动之间的语义鸿沟。

**基线谱系与差异化定位**

DanceChat所处的音乐到舞蹈生成领域，方法沿两条技术路线演进：

- **基于回归/量化的方法**：**FACT**（Li et al., ICCV 2021）采用Transformer架构，需要起始姿态作为条件输入，本质上学习的是姿态序列的自回归映射。**Bailando**（Siyao et al., CVPR 2022）引入VQ-VAE与actor-critic框架，通过离散化运动表征和强化学习优化舞蹈质量。这些方法缺乏对音乐节奏结构的显式建模，且未利用文本作为语义桥梁。

- **基于扩散模型的方法**：**EDGE**（Tseng, Castellon and Liu, CVPR 2023）将扩散模型引入舞蹈生成，以音乐特征为条件直接去噪生成运动。**BADM**（Zhang et al., CVPR 2024）提出双向自回归扩散框架。**Beat-it**（Huang et al., ECCV 2024）专注于节拍同步，通过多条件机制实现高精度节拍对齐。这些方法虽在运动质量和多样性上取得进展，但语义引导方式仍局限于音乐抽象特征，缺少对“跳什么动作”的显式描述。

DanceChat相对于上述基线的关键差异化体现在三个改变槽位：

1. **语义引导方式**：基线方法仅依赖音乐抽象特征（如Jukebox嵌入），缺乏显式运动描述。DanceChat利用LLM从音乐结构描述中生成与音乐节奏对齐的文本舞蹈指令（Section 3.3, Figure 2a），将“听音乐”转化为“理解编舞意图”。

2. **多模态融合策略**：部分基线仅使用音乐特征或简单拼接节拍信息。DanceChat采用分层融合——先将音乐嵌入与节拍嵌入相加（$E_{M}' = E_{M} + E_{B}$），增强节奏感知，再将融合结果与文本指令嵌入拼接（$E_{F} = [E_{M}'; E_{T}]$），形成统一条件表示（Section 3.4, Equations 1-2）。

3. **跨模态对齐损失**：基线方法通常仅使用运动重建损失（MSE、关节位置损失、速度损失等），缺乏显式的跨模态对齐机制。DanceChat引入多模态对齐损失（$\mathcal{L}_{\mathrm{align}}$），以文本嵌入为桥梁，通过余弦相似度同时拉近音乐-文本和运动-文本的距离（Section 3.5, Equation 8），显式缩小跨模态语义鸿沟。

**适用边界与局限**

DanceChat的有效性在以下边界内得到验证，超出这些边界需谨慎推广：

1. **数据依赖性**：方法仅在AIST++数据集上验证，该数据集包含10种舞蹈风格（如芭蕾、街舞、拉丁等）与对应音乐，但音乐风格和舞蹈类型仍有限。对其他音乐流派（如电子乐、传统民族音乐）或舞蹈风格（如现代舞、民族舞）的泛化性未经测试。

2. **LLM质量依赖**：文本指令质量高度依赖LLM的能力和提示工程。当音乐结构复杂或风格罕见时，LLM可能生成不准确或过于泛化的指令，进而影响舞蹈质量。指令质量的定量影响机制尚不明确（开放问题）。

3. **节拍对齐性能**：尽管融合节拍信息后BAS达到0.27（第二），但仍显著落后于专门优化节拍对齐的Beat-it（BAS 0.66）。这表明DanceChat的节拍对齐机制（简单的加法融合）在精细节奏同步上存在上限。

4. **部署复杂度**：训练需使用多个预训练模型（Jukebox用于音乐特征提取、CLIP用于文本编码、HumanML3D权重用于文本-运动对齐），增加了工程部署和模型维护的复杂度。

**开放问题与未来方向**

1. **指令质量的影响量化**：LLM生成的文本指令质量如何定量影响舞蹈的多样性（Div_k）和物理真实性（PFC）？能否建立指令质量评估指标与生成效果之间的因果关系模型？

2. **跨域泛化能力**：该框架能否泛化到AIST++未包含的音乐流派或舞蹈风格？是否需要针对新域重新设计音乐描述模板和提示工程？

3. **自适应指令粒度**：如何根据音乐复杂度自适应调整LLM指令的细节程度？对于结构简单的音乐，粗粒度指令可能足够；对于复杂编曲，需要更精细的动作描述。

4. **长序列与多智能体扩展**：当前方法生成固定长度的舞蹈片段。能否扩展到长序列舞蹈生成（如完整曲目）或多人协同舞蹈场景？这需要解决长程一致性和多舞者空间协调问题。

5. **实时性与交互性**：当前框架为离线生成，LLM推理和扩散采样耗时较长。能否优化为实时或交互式系统，支持用户通过文本指令实时调整舞蹈风格？



## 原文 PDF

![[paperPDFs/arxiv_2025/DanceChat_Large_Language_Model_Guided_Music_to_Dance_Generation.pdf]]
