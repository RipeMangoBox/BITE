---
title: "InterDreamer: Zero-Shot Text to 3D Dynamic Human-Object Interaction"
type: paper
paper_level: A
venue: NEURIPS
year: 2024
pdf_ref: paperPDFs/NEURIPS_2024/InterDreamer_Zero_Shot_Text_to_3D_Dynamic_Human_Object_Interaction.pdf
project_link: https://sirui-xu.github.io/InterDreamer/
code_link: null
aliases:
- InterDreamer
tags:
- NEURIPS_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 交互语义与动力学解耦：语义借助LLM和预训练文本到动作模型获取，动力学通过基于接触顶点的世界模型学习，两者均不依赖文本-交互对。
primary_logic: 交互语义（高层描述、接触部位）与交互动力学（物体运动）可由外部知识源和简单物理先验分别获得，无需成对的文本-交互数据进行训练。
claims:
- 基于接触顶点的动作表示在动力学建模中显著优于基于人体运动或标记点的表示，CMD从0.325降至0.151。
- 高层规划（LLM重写文本）能有效提升文本到动作模型在HOI场景下的语义对齐度，MDM Top-1 R-Precision从0.153提高至0.163。
- GPT-4在识别交互对象类别和接触身体部位方面准确率几近完美（99.7%和96.4%），保障了高层规划的可靠性。
- 高层规划显著拉近了HOI描述与HumanML3D训练文本的分布，尤其在分布外描述上相似度从0.838升至0.927。
---

# InterDreamer: Zero-Shot Text to 3D Dynamic Human-Object Interaction

> [!tip] 核心洞察
> 交互语义（高层描述、接触部位）与交互动力学（物体运动）可由外部知识源和简单物理先验分别获得，无需成对的文本-交互数据进行训练。

| 字段 | 内容 |
|------|------|
| 中文题名 | InterDreamer：零样本文本到3D动态人-物交互生成 |
| 英文题名 | InterDreamer: Zero-Shot Text to 3D Dynamic Human-Object Interaction |
| 会议/期刊 | NEURIPS 2024 |
| Links | [Project](https://sirui-xu.github.io/InterDreamer/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | InterDreamer |
| Dataset | BEHAVE, OMOMO |

> [!tip] 效果简介
> - BEHAVE (text-to-interaction generation) 上，CMD↓ 0.151 vs 0.325 (human motion as action) (-0.174)。
> - BEHAVE (human motion quality with MDM) 上，R-Precision Top-1↑ 0.163 vs 0.153 (MDM w/o planning) (+0.010)。
> - BEHAVE (human motion quality with MotionDiffuse) 上，FID↓ 9.015 vs 10.208 (MotionDiffuse w/o planning) (-1.193)。

## 概要

**问题瓶颈**：文本驱动的三维人-物交互（Human-Object Interaction, HOI）生成长期受限于大规模配对文本-交互数据的缺失，导致监督学习方法在扩展性和泛化能力上遭遇根本性困难。

**核心洞察**：InterDreamer 的关键发现是**交互语义与交互动力学可以解耦**——高层语义（交互对象类别、接触身体部位、动作描述）可借助大语言模型（LLM）和预训练文本到动作模型从外部知识源获取，而低层动力学（物体运动、接触保持）则通过基于接触顶点的世界模型学习，两者均无需成对的文本-交互数据进行训练。

**方法定位**：InterDreamer 提出一个零样本文本到三维动态人-物交互生成框架，由三个模块协同构成：
1. **高层规划（High-Level Planning）**：利用 LLM（如 GPT-4）解析自由形式文本描述，提取交互对象类别、接触身体部位，并重写文本以缩小其与 HumanML3D 训练分布的差距。
2. **低层控制（Low-Level Control）**：包含文本到动作模型（如 MDM、MotionDiffuse、MotionGPT）和交互检索模块，前者根据重写文本生成人体动作序列，后者从预建数据库中检索物体初始状态。
3. **世界模型（World Model）**：以稀疏采样的**接触顶点轨迹**作为动作表示，接收连续人体动作并预测物体下一状态，再通过优化过程精化动作与状态，确保物理合理性。

**主要结果**：
- **动力学建模**：基于接触顶点的动作表示在 BEHAVE 数据集上显著优于基于人体整体运动或接触标记点的表示，接触图差异度量（CMD）从 0.325 降至 **0.151**（Table 1）。
- **语义对齐**：高层规划在多种文本到动作骨干模型上一致提升运动质量——以 MDM 为例，Top-1 R-Precision 从 0.153 提升至 **0.163**（Table 2）；在 OMOMO 数据集上，MotionDiffuse 的 FID 从 15.442 降至 **10.815**（Table 3）。
- **LLM 可靠性**：GPT-4 在识别交互对象类别和接触身体部位上的准确率分别达 **99.7%** 和 **96.4%**（Table 4），保障了高层规划的可靠性。
- **分布弥合**：经高层规划重写的文本与 HumanML3D 文本的相似度在分布外描述上从 0.838 大幅提升至 **0.927**（Table 5），验证了其缩小分布差距的关键作用。

**方法谱系与知识库定位**：InterDreamer 在文本到动作生成领域继承并拓展了 MDM（Tevet et al., ICLR 2023）、MotionDiffuse（Zhang et al., IEEE TPAMI 2024）、ReMoDiffuse（Zhang et al., ICCV 2023）和 MotionGPT（Guo et al., arXiv 2023）等扩散/自回归骨干模型；在交互动力学建模上与 InterDiff（Xu et al., ECCV 2024）形成对比——后者使用接触标记点作为动作表示，而 InterDreamer 改用稀疏接触顶点轨迹，实现了更优的动力学控制精度。框架中仅世界模型需要额外训练，其余组件均为零样本复用，体现了“知识解耦、即插即用”的设计哲学。



### 问题背景

生成逼真的三维人-物交互（Human-Object Interaction, HOI）是计算机视觉与图形学中的核心挑战，在虚拟现实、具身智能和数字人动画等领域具有广泛应用。给定一段自由形式的文本描述，系统需要同时生成语义合理的人体运动序列和物体运动轨迹，使得两者在时空上形成自然、物理可信的接触与协同。这一任务的关键难点在于：**交互语义**（如“用左手拿起杯子”）与**交互动力学**（如接触力的传递、物体随手的运动轨迹）紧密耦合，传统方法往往需要大量配对的文本-交互数据来同时学习这两层信息。

### 现有方法的瓶颈

当前主流的文本驱动HOI生成方法通常采用监督学习范式，依赖大规模、高质量的**文本-交互对**数据进行端到端训练。然而，这类数据的采集和标注成本极高——一方面，需要同时捕捉人体运动与物体运动；另一方面，需要为每段交互序列配以精确的文本描述。这导致现有数据集规模远小于纯人体运动数据集（如HumanML3D），严重限制了模型的扩展性和泛化能力。**缺乏大规模配对的文本-人-物交互数据**，构成了该领域从监督学习迈向零样本/开放场景生成的核心瓶颈。

### 本文动机与核心洞察

InterDreamer的提出源于一个关键观察：**交互语义与交互动力学可以被解耦**。

- **交互语义**（高层描述、接触部位、交互意图）并非必须从文本-交互对中学习。大规模语言模型（LLM）具备丰富的常识知识，能够从自由文本中准确提取交互对象类别和接触身体部位；同时，预训练的文本到动作模型（text-to-motion）已经在大规模文本-人体运动数据上学习了从语言到人体运动的映射。这两者共同提供了零样本获取交互语义的外部知识源。
- **交互动力学**（物体如何随人体运动而运动）则可以通过简单的物理先验来建模——当人与物体发生接触时，接触顶点的运动轨迹是物体运动最直接的驱动信号。这意味着，动力学模型仅需学习“接触顶点如何驱动物体运动”，而无需依赖文本监督。

基于这一解耦思想，InterDreamer将零样本文本到HOI生成分解为三个协同模块：利用LLM进行高层语义规划、借助预训练文本到动作模型生成人体动作、通过基于接触顶点的世界模型预测物体运动。**整个框架中，仅世界模型需要额外训练**，大幅降低了对配对文本-交互数据的依赖。

### 方法定位

InterDreamer并非重新训练一个端到端的文本-交互生成器，而是**将已有的大规模知识源（LLM、文本-动作模型、HOI运动数据、简单物理先验）协同整合**，在零样本设定下实现文本驱动的动态HOI生成。这一范式区别于需要文本-交互对监督的现有方法，为开放词汇、跨物体类别的交互生成提供了新的技术路径。



## 核心方法与创新机理

InterDreamer 的核心创新在于**将交互语义与动力学完全解耦**，从而绕过了零样本 HOI 生成的根本瓶颈——缺乏大规模配对的文本-交互数据。这一解耦通过两个关键的 “changed slots” 实现：高层语义规划与基于接触顶点的动力学建模。

### 创新一：高层语义规划——弥合文本分布鸿沟

传统文本到动作模型（如 MDM、MotionDiffuse）在 HumanML3D 等单人运动数据集上训练，其文本分布与自由形式的 HOI 描述存在显著差异。InterDreamer 引入 **LLM 驱动的高层规划** 来解决这一问题：给定原始文本描述 $p$，LLM 输出交互细节 $g = L(p)$，包括目标物体类别、接触身体部位以及重写后的交互文本（Sec. 3.1）。重写文本被设计为更接近 HumanML3D 的训练分布，从而使预训练的单人运动生成器无需微调即可适配 HOI 场景。

**证据链**：
- **分布弥合**：经高层规划重写的文本与 HumanML3D 文本的相似度在分布外描述上从 0.838 显著提升至 0.927（Table 5），验证了其缩小分布差距的核心作用。
- **一致提升**：在 BEHAVE 数据集上，高层规划使 MDM 的 R-Precision Top-1 从 0.153 提升至 0.163，MotionDiffuse 的 FID 从 10.208 降至 9.015（Table 2）；在 OMOMO 数据集上，MotionDiffuse 的 FID 从 15.442 降至 10.815（Table 3），展示出跨骨干模型和跨数据集的稳健增益。
- **LLM 可靠性**：GPT-4 在识别交互对象类别（Q1 Acc* 99.7%）和接触身体部位（Q2 Acc* 96.4%）上近乎完美（Table 4），保障了规划输出的语义准确性。

### 创新二：接触顶点动作表示——精炼动力学控制

动力学建模的传统做法是将人体整体运动向量或接触标记点（如 InterDiff, Xu et al., ECCV 2024）作为动作表示。InterDreamer 提出**稀疏采样的接触顶点轨迹**作为动作表示：基于符号距离场，在物体表面附近按准则 $|\mathbf{sdf}_i(\pmb{v}_i^j)| \leq \delta_1$ 和 $\|\pmb{v}_i^j - \pmb{v}_i^k\| \geq \delta_2$ 采样接触顶点（Sec. 3.3），仅保留与交互直接相关的局部接触信息。

**证据链**：
- **决定性提升**：在 BEHAVE 的文本到交互生成任务上，接触顶点表示将 CMD 从 0.325（人体整体运动）大幅降至 0.151（Table 1），穿透率（Pene.）也从 631 降至 443。
- **因果机制**：消融实验（Figure 8）定性展示了接触顶点表示能持续合成一致接触，而基线方法在相同文本输入下接触频繁断裂。这表明局部接触信息——而非全局人体运动——才是物体动力学预测的关键控制信号。

### 创新三：零样本框架的系统性设计

上述两个 changed slots 被整合进一个模块化框架，其系统性创新在于：**仅有世界模型需要额外训练**，其余组件（LLM、文本到动作模型）均为现成的预训练模型。具体而言：
- 高层规划 $g = L(p)$ 从 LLM 常识中提取交互语义；
- 文本到动作模型 $\mathbf{a}_{t+1} \sim \pi(\mathbf{a}_{t+1} \mid s_t, \{a_i\}_{i=1}^t, g)$ 利用大规模文本-运动数据生成语义对齐的人体动作；
- 交互检索 $\pmb{s}_1 \sim R(\pmb{s}_1 \mid \pmb{a}_1, g)$ 基于手工规则从预建数据库中确定物体初始状态；
- 世界模型 $\mathbf{s}_{t+1} \sim P(\mathbf{s}_{t+1} \mid \mathbf{a}_t, \mathbf{s}_t, \mathbf{a}_{t+1})$ 仅需在 BEHAVE 上训练，即可学习接触顶点驱动的物体动力学。

这种设计使得 InterDreamer 无需任何成对的文本-交互数据即可生成语义一致、物理合理的 HOI 序列，并在 CHAIRS 等未见物体上展示出跨域泛化能力（Figure 5）。



InterDreamer 提出一种**语义与动力学解耦**的零样本文本到3D动态人-物交互生成框架。其核心洞察在于：交互语义（高层描述、接触部位、物体类别）与交互动力学（物体在人体作用下的运动）可以从相互独立的外部知识源获取，从而绕过了对大规模配对文本-交互数据的依赖。

### 框架总览

整个 pipeline 由三个协同模块构成，如 Figure 2 所示：

![[assets/figures/papers/paper_list_l1796_InterDreamer_Zero_Shot_Text_to_3D_Dynamic_Human_Object_Interaction/figures/002_Figure_2.jpg]]
*Figure 2: An overview of our InterDreamer. (i) Our high-level planning analyzes the description using LLMs and provides guidance to the low-level control. (ii) Our low-level control includes a text-to-motion model that translates text into human actions*

1. **高层规划（High-Level Planning）**：接收自由形式的文本描述 $p$，通过大语言模型（LLM）解析出结构化的交互细节 $g = L(p)$，包括目标物体类别、接触身体部位以及重写后的交互文本。这一步将原始HOI描述映射到与预训练文本-动作模型训练分布更接近的语义空间。

2. **低层控制（Low-Level Control）**：包含两个子模块——
   - **文本到动作模型 $\pi$**：根据历史动作序列、当前状态和重写后的文本目标 $g$，采样下一段人体动作 $\mathbf{a}_{t+1} \sim \pi(\mathbf{a}_{t+1} \mid s_t, \{a_i\}_{i=1}^t, g)$。
   - **交互检索模型 $R$**：基于初始动作 $\mathbf{a}_1$ 和文本目标 $g$，从预建数据库中检索物体的初始状态 $\pmb{s}_1 \sim R(\pmb{s}_1 \mid \pmb{a}_1, g)$。

3. **世界模型（World Model）**：由动力学模型和优化过程耦合而成，负责模拟状态转移 $\mathbf{s}_{t+1} \sim P(\mathbf{s}_{t+1} \mid \mathbf{a}_t, \mathbf{s}_t, \mathbf{a}_{t+1})$。动力学模型以**稀疏采样的接触顶点轨迹**作为动作表示，从一对连续动作和前一物体状态预测下一物体状态；优化过程则通过贴合度、速度平滑、接触促进和穿透惩罚等损失项对动作和状态进行精化。

### 输入输出流

完整序列定义为 $M$ 帧的人-物交互元组：

$$\boldsymbol{x} = [(\pmb{h}_1, \pmb{o}_1), \dots, (\pmb{h}_M, \pmb{o}_M)]$$

其中 $\pmb{h}_i$ 为第 $i$ 帧的人体姿态，$\pmb{o}_i$ 为物体姿态。生成流程以文本描述为唯一输入，经过高层规划→低层控制→世界模型的迭代循环，逐帧输出语义对齐且物理合理的人-物交互序列。

### 关键设计选择

框架中**唯一需要额外训练的组件是世界模型**，高层规划和低层控制均利用预训练模型（LLM和文本到动作模型）的零样本能力。这种设计使得 InterDreamer 能够灵活替换不同骨干模型——实验验证了 MDM、MotionDiffuse、ReMoDiffuse 和 MotionGPT 等多种文本到动作模型均可即插即用，且高层规划在所有骨干上一致提升了生成质量（Table 2, Table 3）。

动力学模型采用**接触顶点作为动作表示**是另一关键选择。相比于使用人体整体运动向量或接触标记点轨迹，稀疏采样的接触顶点轨迹将动力学建模的焦点集中在交互发生的局部区域，在 BEHAVE 数据集上将接触图差异度量（CMD）从 0.325 降至 0.151（Table 1），验证了局部接触信息对动力学建模的决定性作用。

### 补充图表

![[assets/figures/papers/paper_list_l1796_InterDreamer_Zero_Shot_Text_to_3D_Dynamic_Human_Object_Interaction/figures/001_Figure_1.jpg]]
*Figure 1: InterDreamer generates vivid 3D human-object interaction sequences guided by text descriptions, by synergizing semantics and dynamics knowledge from large-scale text-motion data (upper left), a large language model (bottom left), human-object interaction data (upper middle), and prior knowledge (bottom middle) from simple physics. We visualize the generated text-guided interaction sequence (upper right), with the beginning of the sequence unfolded (bottom right)*



InterDreamer 将文本到3D动态人-物交互生成分解为三个核心模块：**高层规划**（High-Level Planning）、**低层控制**（Low-Level Control）和**世界模型**（World Model）。整个框架的核心洞见在于交互语义与动力学可以解耦——语义借助大语言模型和预训练文本到动作模型获取，动力学通过基于接触顶点的世界模型学习，两者均不依赖成对的文本-交互数据。

### 交互序列定义

系统将人-物交互定义为一个包含 $M$ 帧的序列，每帧由人体姿态 $\pmb{h}_i$ 和物体姿态 $\pmb{o}_i$ 组成：

$$\boldsymbol{x} = [(\pmb{h}_1, \pmb{o}_1), \dots, (\pmb{h}_M, \pmb{o}_M)]$$

其中人体姿态采用 SMPL-H 模型参数化，物体姿态由 6-DoF 刚体变换表示。

### 高层规划：LLM语义解析

给定自由形式的文本描述 $p$，高层规划模块 $L$ 利用大语言模型（如 GPT-4）提取结构化的交互细节 $g$：

$$g = L(p)$$

$g$ 包含三个关键信息：(1) 目标物体的类别（从预定义列表中确定）；(2) 接触的身体部位；(3) 重写后的交互文本，该文本在语义分布上更接近 HumanML3D 训练语料，从而弥合自由形式 HOI 描述与单人体动作生成模型训练分布之间的差距。实验表明，GPT-4 在识别物体类别和接触部位上的准确率分别达到 99.7% 和 96.4%（Table 4），经高层规划重写的文本与 HumanML3D 的相似度在分布外描述上从 0.838 提升至 0.927（Table 5）。

### 低层控制：文本到动作与交互检索

低层控制包含两个子模块：文本到动作模型 $\pi$ 和交互检索模型 $R$。

**文本到动作采样**：给定当前物体状态 $s_t$、历史动作序列 $\{a_i\}_{i=1}^t$ 以及高层规划输出的目标文本 $g$，预训练的文本到动作模型 $\pi$ 生成下一段人体动作 $\mathbf{a}_{t+1}$：

$$\mathbf{a}_{t+1} \sim \pi(\mathbf{a}_{t+1} \mid s_t, \{a_i\}_{i=1}^t, g)$$

该模块可灵活接入多种文本到动作生成骨干网络，包括 MDM（Tevet et al., ICLR 2023）、MotionDiffuse（Zhang et al., IEEE TPAMI 2024）、ReMoDiffuse（Zhang et al., ICCV 2023）和 MotionGPT（Guo et al., arXiv 2023）。

**交互检索初始状态**：基于初始动作 $\pmb{a}_1$ 和目标 $g$，交互检索模型 $R$ 从预构建的交互数据库中检索物体的初始状态 $\pmb{s}_1$：

$$\pmb{s}_1 \sim R(\pmb{s}_1 \mid \pmb{a}_1, g)$$

检索过程采用手工设计的规则，从数据库中提取与初始动作和目标物体类别相匹配的多样化、逼真的交互起始状态（Figure 6）。

### 世界模型：接触顶点动力学与优化

世界模型是整个框架中唯一需要额外训练的部分，负责根据人体动作预测物体状态的演变。其核心创新在于**接触顶点作为动作表示**（contact vertices as action）。

**接触顶点采样**：对于每帧交互，在物体表面附近稀疏采样接触顶点。采样准则基于符号距离场（SDF），要求顶点 $\pmb{v}_i^j$ 靠近物体表面且彼此间保持最小距离：

$$|\mathbf{sdf}_i(\pmb{v}_i^j)| \leq \delta_1,\quad \|\pmb{v}_i^j - \pmb{v}_i^k\| \geq \delta_2, \forall j \neq k$$

其中 $\delta_1$ 控制顶点到物体表面的距离阈值，$\delta_2$ 确保采样点之间的空间稀疏性。这些接触顶点用红色球体表示人体接触点，蓝色球体表示物体接触点（Figure 2）。

**状态转移**：世界模型 $P$ 接收前一物体状态 $\mathbf{s}_t$、当前动作 $\mathbf{a}_t$ 和下一动作 $\mathbf{a}_{t+1}$，预测下一物体状态 $\mathbf{s}_{t+1}$：

$$\mathbf{s}_{t+1} \sim P(\mathbf{s}_{t+1} \mid \mathbf{a}_t, \mathbf{s}_t, \mathbf{a}_{t+1})$$

**动力学网络架构**：网络由两个分支组成——无接触顶点条件的 $G$ 分支和有接触顶点条件的 $F$ 分支。$G$ 处理全局运动信息，适用于无接触场景；$F$ 将接触顶点条件融入物体轨迹预测。两个分支通过交叉注意力机制融合：

$$x_{k+1}, \{y_{k+1}^j\}_{j=1}^N = \text{Attn}(G_k(x_k, \Theta), \{F_k(y_k^j, \Theta_v)\}_{j=1}^N)$$

其中 $x_k$ 为 $G$ 分支在第 $k$ 层的特征，$y_k^j$ 为 $F$ 分支处理第 $j$ 个接触顶点的特征，$\Theta$ 和 $\Theta_v$ 为各自的可学习参数。交叉注意力使无接触分支能够动态聚合来自多个接触顶点的局部交互信息。

**优化精化**：动力学模型输出后，通过优化过程将状态和动作投影到物理有效的对应物上。总优化损失 $E_{\mathrm{opt}}$ 由四项加权组成：

$$E_{\mathrm{opt}} = \lambda_{\mathrm{fit}} E_{\mathrm{fit}} + \lambda_{\mathrm{vel}} E_{\mathrm{vel}} + \lambda_{\mathrm{cont}} E_{\mathrm{cont}} + \lambda_{\mathrm{pene}} E_{\mathrm{pene}}$$

- $E_{\mathrm{fit}}$：动作贴合度损失，约束优化后的人体姿态与生成动作一致。
- $E_{\mathrm{vel}}$：速度平滑损失，保证运动的时间连续性。
- $E_{\mathrm{cont}}$：接触促进损失，鼓励接触顶点处的物理接触。
- $E_{\mathrm{pene}}$：穿透惩罚损失，利用人体 SDF 惩罚物体侵入人体的部分：

$$E_{\mathrm{pene}} = - \sum_{i=1}^{L} \sum_{d_o} \min(\mathbf{sdf}_{h_i^*}(\pmb{v}_{o_i^*}[d_o]), 0)$$

消融实验（Table 1）验证了接触顶点动作表示的关键作用：将其替换为人体整体运动（human motion as action）会导致 CMD 从 0.151 急剧上升至 0.325，穿透指标也从 443 显著恶化，表明局部接触信息对动力学建模至关重要。

### 补充图表

![[assets/figures/papers/paper_list_l1796_InterDreamer_Zero_Shot_Text_to_3D_Dynamic_Human_Object_Interaction/figures/011_Figure_8.jpg]]
*Figure 8: Ablation study on the dynamics model. Given the text description of “A person walks clockwise while holding a small box with left hand,” our (b) vertex-based control can synthesize consistent contacts, which (a) the baseline fails to do*

![[assets/figures/papers/paper_list_l1796_InterDreamer_Zero_Shot_Text_to_3D_Dynamic_Human_Object_Interaction/figures/010_Figure.jpg]]
*Figure: A person is holding an object withividual is holding onto it. (a) Low-level control w/o planning v.s. w/ planning s. (b) Text feature w/ planning v.s. w/o planning*

![[assets/figures/papers/paper_list_l1796_InterDreamer_Zero_Shot_Text_to_3D_Dynamic_Human_Object_Interaction/figures/015_Figure.jpg]]
*Figure: C: Qualitative results from the interaction retrieval. We demonstrate that our learning-based interaction retrieval can extract diverse and realistic interactions*



## 实验与关键发现

### 核心瓶颈与因果机制

InterDreamer 的核心瓶颈在于：**缺乏大规模配对的文本‑人‑物交互（HOI）数据**，使得传统监督学习方法难以扩展与泛化。针对此瓶颈，该方法引入了一条因果调控路径：**将交互语义与交互动力学解耦**。语义（高层描述、接触部位、物体类别）通过大语言模型（LLM）和预训练文本‑动作模型获取；动力学（物体状态转移）则通过基于接触顶点的世界模型学习——两者均不依赖任何文本‑交互对。该设计使得整个框架中**唯一需要额外训练的模块是世界模型**，其余组件均为即插即用的外部知识源。

### 核心主张与决定性证据

1. **接触顶点动作表示显著优于人体运动或标记点表示**（Table 1）。将动作表示从“人体整体运动向量”替换为“稀疏采样的接触顶点轨迹”后，接触图差异度量 **CMD 从 0.325 降至 0.151**，穿透率也大幅下降。这表明局部接触信息对动力学建模具有决定性作用。

![[assets/figures/papers/paper_list_l1796_InterDreamer_Zero_Shot_Text_to_3D_Dynamic_Human_Object_Interaction/figures/003_Table_1.jpg]]
*Table 1: Quantitative results on evaluating the dynamics model. Our dynamics model with vertexbased action generates interactions of the best quality*

2. **高层规划（LLM 重写文本）一致提升文本‑动作对齐度**（Table 2, Table 3）。在 BEHAVE 数据集上，MDM 的 Top‑1 R‑Precision 从 **0.153 提升至 0.163**；MotionDiffuse 的 FID 从 **10.208 降至 9.015**。在 OMOMO 数据集上，MotionDiffuse 的 FID 从 **15.442 降至 10.815**，提升幅度达 4.627。该增益在 MDM、MotionDiffuse、ReMoDiffuse、MotionGPT 四个骨干模型上均保持一致。

![[assets/figures/papers/paper_list_l1796_InterDreamer_Zero_Shot_Text_to_3D_Dynamic_Human_Object_Interaction/figures/004_Table_2.jpg]]
*Table 2: Quantitative results on human motion quality given our annotation on the BEHAVE [7] dataset. We show that our high-level planning effectively adapts single human generators into humanobject interaction generation. To evaluate R-Precision, a batch size of 16 is selected*

![[assets/figures/papers/paper_list_l1796_InterDreamer_Zero_Shot_Text_to_3D_Dynamic_Human_Object_Interaction/figures/005_Table_3.jpg]]
*Table 3: Quantitative results on human motion quality on the OMOMO [66] dataset with their provided annotation. We show that our high-level planning narrows the distribution gap and adapts single human generators into human-object interaction generation. To evaluate R-Precision, a batch size of 32 is selected*

3. **LLM 的常识知识足以支撑零样本文本解析**（Table 4）。GPT‑4 在识别交互对象类别上的准确率达 **99.7%**，在识别接触身体部位上的准确率达 **96.4%**，几乎完美，保障了高层规划的可靠性。

![[assets/figures/papers/paper_list_l1796_InterDreamer_Zero_Shot_Text_to_3D_Dynamic_Human_Object_Interaction/figures/012_Table_4.jpg]]
*Table 4: Ablation study on the high-level planning. Q1 and Q2 ask to identify the object category and the contact body part, respectively. We assess the accuracy by comparing the LLM’s responses with labels we annotate. Note that the text input to LLMs may contain ambiguities; for example, the annotation is “hand” when the motion uses “right hand.” We include Q1 Acc∗ and Q2 Acc∗ excluding ambiguous text*

4. **高层规划显著弥合文本分布差距**（Table 5）。经 LLM 重写后的文本与 HumanML3D 训练文本的相似度，在分布外描述上从 **0.838 升至 0.927**，在分布内描述上也从 0.946 提升至 0.964，验证了其缩小语义分布鸿沟的作用。

### 消融实验的关键结论

- **动力学模型的动作表示消融**：去除接触顶点动作表示（换用人体整体运动）导致 CMD 从 0.151 急剧上升至 0.325；去除动作控制（w/o action）则使 CMD 进一步恶化至 0.949，穿透率飙升至 10,843。这表明接触顶点级别的控制信号是维持交互质量的核心。
- **高层规划消融**：在所有文本‑动作骨干模型上，去除高层规划均导致 R‑Precision 下降和 FID 上升。定性结果（Figure 7）显示，无规划时生成的动作常出现语义漂移（如“手持盒子”退化为“手部悬空”），而 t‑SNE 可视化证实规划后的文本特征更贴近 HumanML3D 分布。
- **LLM 选择消融**：GPT‑4 在两项识别任务上均优于 Llama 2，但即便是 Llama 2 也保持了较高的准确率（Q1 97.1%，Q2 91.2%），说明该方法对 LLM 的选择具有一定鲁棒性。

### 跨数据集泛化与定性结果

- **跨数据集泛化**：动力学模型仅在 BEHAVE 上训练，但在 CHAIRS 数据集上展示了良好的泛化能力（Figure 5），能够处理训练中未见过的物体类别。
- **复杂场景**：InterDreamer 能够处理自由形式的文本输入，生成具有一致接触的交互序列（Figure 3），并能适应不同物体尺寸和复杂长序列（Figure 4）。
- **交互检索**：基于手工规则的检索方法能够从数据库中提取多样且真实的物体初始状态（Figure 6），为后续动力学模拟提供合理起点。

![[assets/figures/papers/paper_list_l1796_InterDreamer_Zero_Shot_Text_to_3D_Dynamic_Human_Object_Interaction/figures/006_Figure_3.jpg]]
*Figure 3: Qualitative results on free-form text input. The interaction sequences, with textures from [13], are presented through a time-series visualization*

![[assets/figures/papers/paper_list_l1796_InterDreamer_Zero_Shot_Text_to_3D_Dynamic_Human_Object_Interaction/figures/007_Figure_4.jpg]]
*Figure 4: Qualitative results in more challenge scenarios with free-form input not from our annotations, showing the ability of our InterDreamer to fit object sizes and handle complex and long sequences. Here, our synergized models are GPT-4 [88] and MotionGPT [46]*

![[assets/figures/papers/paper_list_l1796_InterDreamer_Zero_Shot_Text_to_3D_Dynamic_Human_Object_Interaction/figures/009_Figure_5.jpg]]
*Figure 5: Qualitative results on the CHAIRS [47] dataset. Our dynamics model trained on the BEHAVE [7] dataset generalizes well on the CHAIRS objects unseen in training. Frames are separately visualized. Here, our synergized models are GPT-4 [88] and MotionGPT [46]*

### 失败模式与局限性

1. **物理建模简化**：世界模型仅学习简单物理先验，在处理非接触交互（如指向、注视）或高度动态的物体行为时可能失效。当前框架未集成物理仿真器，交互的物理真实性存在上限。
2. **手部姿态缺失**：系统不生成精细的手部姿态，导致手‑物接触区域可能不自然，这是生成结果中视觉瑕疵的主要来源之一。
3. **LLM 固有偏见**：文本重写依赖 LLM 的常识推理，在分布外描述或模糊描述下可能产生不理想的输出（如错误识别接触部位），进而传播到下游模块。
4. **接触顶点采样的超参数敏感性**：采样阈值 $\delta_1$ 和 $\delta_2$ 为手工设定，可能无法适应所有物体尺度和交互类型，在极端接触场景下可能采样不足或过密。
5. **训练数据覆盖范围有限**：动力学模型仅在 BEHAVE 数据集上训练，虽然展示了跨数据集泛化，但在更广泛的物体类别和交互类型上的稳健性仍需进一步验证。

### 待解决的开放问题

- 能否将基于模型的强化学习集成到世界模型中，以学习更复杂的交互技能（如推、拉、旋转物体）？
- 如何利用物理仿真器替代或增强现有简单动力学模型，以提升交互的物理真实性和接触一致性？
- 如何将手部姿态纳入生成流程，实现更细腻的手‑物交互？
- 解耦的语义‑动力学范式能否扩展到多人与多物体交互场景？
- 在完全无文本‑交互对监督的条件下，当前框架的性能上限是多少？如何量化并进一步弥合剩余的性能差距？



## 定位与知识库关联

### 核心范式定位

InterDreamer 提出了一种**语义与动力学解耦**的零样本文本到3D人-物交互生成范式。其核心洞察在于：交互语义（高层描述、接触部位）与交互动力学（物体运动）可分别从外部知识源和简单物理先验中获取，无需成对的文本-交互数据进行训练。这一范式将问题分解为三个可独立运作的模块：高层规划（LLM）、低层控制（文本到动作模型 + 交互检索）和世界模型（动力学 + 优化），仅世界模型需要额外训练。

### 与基线方法的关系

#### 动力学模型基线

InterDreamer 的动力学模型在动作表示层面进行了关键创新，与以下基线形成直接对比：

- **InterDiff** (Xu et al., ECCV 2024)：使用接触标记点（contact markers）作为动作表示。InterDreamer 将其替换为**稀疏采样的接触顶点轨迹**（contact vertices as action），在 BEHAVE 数据集上 CMD 从 0.325 降至 0.151（Table 1），穿透率也显著降低。这一改进的机理在于：接触顶点直接编码了物体表面附近的局部几何信息，相比标记点或整体运动向量，能更精确地捕捉接触约束。
- **human motion as action**：使用原始 SMPL 人体姿态作为动作表示。该基线在消融实验中 CMD 为 0.325，而接触顶点表示降至 0.151（Table 1），验证了局部接触信息对动力学建模的决定性作用。
- **w/o action**：完全不使用人体控制信号，进一步验证了动作表示的必要性。

#### 文本到动作生成基线

InterDreamer 的高层规划模块可与多种文本到动作骨干模型协同工作，在 BEHAVE 和 OMOMO 数据集上均一致提升了生成质量：

- **MDM** (Tevet et al., ICLR 2023)：加入高层规划后，R-Precision Top-1 从 0.153 提升至 0.163（Table 2）。
- **MotionDiffuse** (Zhang et al., IEEE TPAMI 2024)：加入高层规划后，BEHAVE 上 FID 从 10.208 降至 9.015（Table 2），OMOMO 上 FID 从 15.442 降至 10.815（Table 3）。
- **ReMoDiffuse** (Zhang et al., ICCV 2023) 和 **MotionGPT** (Guo et al., arXiv 2023)：同样受益于高层规划（Table 2, Table 3），表明该模块具有骨干无关的即插即用特性。

高层规划的核心作用是通过 LLM 重写文本，缩小自由形式 HOI 描述与 HumanML3D 训练文本之间的分布差距。在分布外描述上，文本相似度从 0.838 升至 0.927（Table 5），验证了这一机制的有效性。

### 方法适用边界

1. **交互类型边界**：世界模型仅学习简单物理（基于接触顶点的运动预测 + 穿透惩罚），可能无法精确模拟非接触交互（如指向、挥手示意）或高度动态的物体行为（如抛接、踢球）。当前框架对“接触主导”的交互（持握、坐、推拉等）效果较好，但对涉及复杂物理的交互类型存在局限。

2. **手部姿态边界**：当前系统不支持精细的手部姿态生成，手部-物体接触可能不自然。这是方法层面的结构性限制，而非训练数据不足所致。

3. **物体泛化边界**：动力学模型仅在 BEHAVE 数据集上训练，虽然在 CHAIRS 数据集上展示了跨物体泛化能力（Figure 5），但在更广泛的物体类别和交互类型上的稳健性仍需验证。接触顶点采样依赖手工设定的阈值 $\delta_1$ 和 $\delta_2$，可能无法适应所有交互场景。

4. **文本分布边界**：文本重写依赖 LLM 的固有偏见，在描述严重偏离 HumanML3D 分布时可能产生不理想的输出。尽管 GPT-4 在识别物体类别（准确率 99.7%）和接触身体部位（准确率 96.4%）方面表现优异（Table 4），但在更复杂的语义理解场景下仍存在不确定性。

### 局限与开放问题

**已识别的局限**：
- 世界模型的物理建模能力有限，无法处理复杂非接触交互或高度动态的物体行为。
- 缺乏手部姿态生成能力，限制了手-物交互的自然度。
- 接触顶点采样依赖手工阈值，缺乏自适应性。
- 动力学模型的跨数据集泛化仅在 CHAIRS 上初步验证，更广泛的稳健性未知。

**开放问题**：
1. **物理真实性增强**：能否利用物理仿真器替代或增强现有的简单动力学模型，以提升交互的物理真实性？基于模型的学习方法（如强化学习）是否可以集成到世界模型中，学习更复杂的交互技能？
2. **手部交互扩展**：如何将手部姿态纳入生成流程，实现更细腻的手-物交互？这可能需要额外的手部-物体接触数据或先验知识。
3. **多主体扩展**：解耦的语义-动力学范式能否扩展到多人与多物体交互场景？当前框架的接触顶点表示和世界模型设计是否能直接适配？
4. **性能上限量化**：在无文本监督的情况下，当前框架的上限能达到多少？如何量化并缩小与全监督方法的剩余性能差距？
5. **LLM 依赖性**：高层规划对 LLM 的依赖是否可被更轻量、更可控的语义解析方法替代？如何平衡 LLM 的常识知识与特定领域的精确性需求？



## 原文 PDF

![[paperPDFs/NEURIPS_2024/InterDreamer_Zero_Shot_Text_to_3D_Dynamic_Human_Object_Interaction.pdf]]
