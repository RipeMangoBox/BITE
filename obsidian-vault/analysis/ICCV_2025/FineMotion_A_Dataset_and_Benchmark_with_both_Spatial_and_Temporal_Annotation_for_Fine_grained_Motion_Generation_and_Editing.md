---
title: "FineMotion: A Dataset and Benchmark with both Spatial and Temporal Annotation for Fine-grained Motion Generation and Editing"
type: paper
paper_level: A
venue: ICCV
year: 2025
pdf_ref: paperPDFs/ICCV_2025/FineMotion_A_Dataset_and_Benchmark_with_both_Spatial_and_Temporal_Annotation_for_Fine_grained_Motion_Generation_and_Editing.pdf
project_link: null
code_link: null
aliases:
- FineMotion
tags:
- ICCV_2025
- topic/motion_animation
- topic/motion_animation/human_motion_generation
core_operator: "通过构建包含细粒度身体部位运动描述（BPM）和时间切片的运动-文本对，使模型能够学习到空间和时间上的精确对应关系。"
primary_logic: "通过对运动序列进行固定时长的短时切片，并利用PoseFix模型自动生成每个切片的身体部位运动描述，再经人工校正和段落组织，可构建大规模、严格对齐的细粒度运动-文本数据集。该数据集能显著提升现有文本-运动生成模型对细节和时间控制的性能，并支持零样本细粒度运动编辑。"
claims:
- "FineMotion数据集包含超过442,000个人体运动片段及对应的身体部位运动描述，以及约95,000个段落描述。"
- "使用自动或人工细粒度BPM文本训练后，MDM模型的Top-3检索准确率提升了+15.3%。"
- "在(T&DT)2M-GPT变体上，加入人工注释BPM片段描述可使FID从0.123降至0.091，R-Top3从0.781升至0.789。"
- "用户研究表明，所提零样本编辑流水线在空间和时间编辑案例中均获得最高偏好分数，且在时间编辑上表现尤为突出。"
---

# FineMotion: A Dataset and Benchmark with both Spatial and Temporal Annotation for Fine-grained Motion Generation and Editing

> [!tip] 核心洞察
> 通过对运动序列进行固定时长的短时切片，并利用PoseFix模型自动生成每个切片的身体部位运动描述，再经人工校正和段落组织，可构建大规模、严格对齐的细粒度运动-文本数据集。该数据集能显著提升现有文本-运动生成模型对细节和时间控制的性能，并支持零样本细粒度运动编辑。

| 字段 | 内容 |
|------|------|
| 中文题名 | FineMotion：一个面向细粒度运动生成与编辑的具有时空标注的数据集与基准 |
| 英文题名 | FineMotion: A Dataset and Benchmark with both Spatial and Temporal Annotation for Fine-grained Motion Generation and Editing |
| 会议/期刊 | ICCV 2025 |
| Links | [paper](https://arxiv.org/abs/2507.19850)  |
| Topic | #topic/motion_animation #topic/motion_animation/human_motion_generation |
| Method | FineMotion |
| Dataset | HumanML3D test set |

> [!tip] 效果简介
> - HumanML3D test set 上，R-Precision Top-3 为 0.759 (T&DT-MDM BPMP)，对比 0.606 (MDM coarse)，变化 +0.153 (+15.3%)。
> - HumanML3D test set 上，FID 为 0.055 (T&DT-MoMask BPMP)，对比 0.249 (MoMask coarse)，变化 improvement。
> - HumanML3D test set 上，FID 为 0.091 (T&DT-2M-GPT BPMSD)，对比 0.123 (T2M-GPT coarse)，变化 improvement。

## 概要

### 问题瓶颈

现有3D人体运动-文本数据集（如HumanML3D、KIT-ML）的文本描述普遍粗粒度，仅概括整体动作，缺乏对**特定身体部位运动**及其**时间信息**的细粒度刻画。这导致文本-运动生成模型难以实现精确的时空控制：生成的运动要么无法响应“先抬左手再迈右脚”这类时序指令，要么无法针对特定关节进行空间编辑。部分工作尝试通过大语言模型增强文本描述，但增强后的文本往往与实际运动序列**未严格对齐**，反而引入噪声。

### 核心方法

FineMotion提出了一套**可扩展的细粒度运动-文本数据集构建流水线**，核心思路是将运动序列沿时间轴切分为短片段，再为每个片段自动生成身体部位运动（Body Part Movement, BPM）描述，并经人工校正后组织成段落。具体而言：

1. **运动片段切分**：以固定时长 $T_s = 0.5$ 秒将运动序列切分为短片段，平衡描述冗余性与PoseFix模型的时间差约束。
2. **BPM描述生成**：利用**PoseFix**校正文本生成模型，输入片段的起始与结束姿态，自动输出描述身体部位如何从源姿态变为目标姿态的文本。
3. **段落组织与人工校正**：通过**Gemini**大语言模型将片段描述串联为连贯段落；对部分样本进行人工校正，确保描述与运动的严格对齐。

最终构建的FineMotion数据集包含**超过442,000个人体运动片段**及其对应的BPM片段描述，以及约**95,000个段落描述**，规模和细粒度远超现有数据集（Table 1）。

### 方法定位

FineMotion本质上是一种**数据增强方法**，而非全新的生成模型架构。它通过为现有粗粒度运动-文本对注入细粒度时空标注，使主流文本-运动生成模型（如MDM、T2M-GPT、MoMask）在无需修改网络结构的前提下，显著提升对细节和时间控制的性能。在文本编码策略上，FineMotion将粗文本与细文本**分别编码后拼接嵌入**（T&DT），替代简单的单文本拼接（TDT），实验证明这是性能提升的关键设计。

### 主要结果

在HumanML3D测试集上，FineMotion增强的训练数据为多个基线模型带来一致且显著的性能提升：

- **检索精度**：(T&DT)-MDM的Top-3检索准确率从0.606提升至0.759（**+15.3%**）。
- **生成质量**：(T&DT)-MoMask的FID从0.249降至0.055；(T&DT)-T2M-GPT使用人工校正BPM描述后，FID从0.123降至0.091。
- **时间对齐**：所有细粒度变体的FID_c均低于仅用粗文本的基线，验证了BPM描述对时序控制的增益。
- **零样本编辑**：基于FineMotion的编辑流水线在用户研究中获得最高偏好分数，尤其在时间编辑案例上表现突出。

### 局限与开放问题

当前方法在空间编辑上的精度仍弱于时间编辑；获取BPM描述依赖多步流水线，尚未实现端到端；编辑过程中可能在指定区域外引入意外变化；且缺乏直接评估细粒度运动编辑质量的定量指标。



人体运动生成旨在根据文本描述合成逼真的3D人体运动序列，在动画制作、虚拟现实和人机交互等领域具有广泛应用。近年来，基于扩散模型和自回归模型的文本驱动运动生成方法取得了显著进展，但其生成质量高度依赖于训练数据的文本标注质量。

现有的人体运动-文本数据集（如HumanML3D、KIT-ML）存在一个核心瓶颈：**文本描述过于粗糙，缺乏对特定身体部位运动及其时间信息的细粒度刻画**。如图1(a)所示，这些数据集的标注通常仅提供一个概括性的动作短语或简短描述，例如“一个人向前走”，而忽略了“左臂摆动幅度”、“脚步节奏变化”等细节。这种粗粒度的文本-运动对应关系导致生成的运动难以实现精确的空间和时间控制。

为缓解这一问题，近期工作尝试通过大语言模型对现有文本进行增强，生成更详细的描述。然而，如图1(b)所示，这些方法存在一个关键缺陷：**增强后的文本描述并未与实际的运动序列严格对齐**，即语言模型生成的细节可能并不反映真实运动数据中的具体变化。这种“文本增强但未对齐”的策略无法从根本上建立细粒度文本与运动之间的因果对应关系。

上述缺口引出了本文的核心动机：**能否构建一个大规模、严格对齐的细粒度运动-文本数据集，使模型能够学习到身体部位运动在空间和时间维度上的精确对应关系？** 为实现这一目标，FineMotion提出了一种可扩展的数据构建流水线，通过对运动序列进行固定时长的短时切片，并利用PoseFix修正文本生成模型自动生成每个切片的身体部位运动描述（Body Part Movement description, BPM），再经人工校正和段落组织，最终构建了包含超过442,000个人体运动片段及对应细粒度描述的数据集。该数据集不仅显著提升了现有文本-运动生成模型对细节和时间控制的性能，还首次支持了零样本细粒度运动编辑能力。



## 核心方法与创新机理

FineMotion的核心创新在于首次构建了一个**大规模、严格时空对齐的细粒度人体运动-文本数据集**，并基于此提出了一套**零样本细粒度运动编辑流水线**。与现有工作相比，其关键突破体现在以下三个层面。

### 1. 从粗粒度全局描述到细粒度身体部位运动描述

现有运动-文本数据集（如HumanML3D、KIT-ML）的文本标注停留在粗粒度的全局动作描述层面，例如“一个人向前走”，缺乏对**特定身体部位在特定时间段内运动状态**的刻画。这导致文本到运动生成模型难以精确控制局部肢体动作。FineMotion通过以下changed slots实现了从“粗”到“细”的跃迁：

- **文本粒度**：引入**身体部位运动片段描述（BPMSD）** 和**身体部位运动段落描述（BPMP）**，前者针对0.5秒的短时运动切片描述各部位运动，后者将片段描述组织为连贯段落。
- **时间对齐**：将运动序列沿时间轴切分为固定时长 $T_s = 0.5\text{s}$ 的片段，使每个文本描述与一个短时运动片段严格对齐，解决了以往文本增强方法中描述与实际运动序列不对齐的问题。

### 2. 可扩展的自动标注与人工校正混合流水线

FineMotion提出了一套高效、可扩展的数据构建流水线，包含三个核心模块：

- **片段切分**：以0.5秒为固定时长切分运动序列，基于语义特征余弦相似度分析（Figure 4）选择该时长以平衡描述冗余度和PoseFix模型的输入约束。
- **片段描述生成**：利用**PoseFix**修正性文本生成模型，以片段首尾姿态对为输入，自动生成描述身体部位如何从源姿态变化到目标姿态的文本。随后进行人工校正以保证质量。
- **段落生成**：通过**Gemini**模型将片段描述组织为连贯的段落描述。

该流水线最终产出了**超过442,000个运动片段及对应的BPM描述**，以及约**95,000个段落描述**，在规模上远超现有细粒度数据集。

### 3. 粗-细文本分离编码策略

在模型层面，FineMotion改变了文本编码的slot设计：

- **Baseline编码方式**：将粗粒度文本与细粒度文本拼接为单一文本序列（TDT），使用CLIP编码器处理。
- **FineMotion编码方式**：将文本编码器从**CLIP替换为T5-Base**（避免超长详细文本被截断），并采用**分离编码后拼接嵌入**的策略（T&DT），即对粗标题文本和详细描述文本分别进行T5编码和均值池化，再将两个嵌入向量拼接输入生成模型。

消融实验（Table 5）表明，分离编码策略是性能提升的关键：在MoMask BPMSD变体上，T&DT的R-Precision Top-3达到0.811，而TDT仅为0.434，差距悬殊。这一设计使模型能够分别关注全局语义和局部细节，显著提升了对细粒度运动的控制精度。

### 4. 零样本细粒度运动编辑能力

基于FineMotion数据集训练的模型天然具备了**零样本细粒度运动编辑**能力，这是一项现有方法无法实现的新功能。编辑流水线（Figure 6）的核心机制是：

1. 用户提供粗粒度文本描述，由T2M模型生成初始运动。
2. 利用数据集构建流水线提取该运动的BPM片段描述。
3. 用户对片段描述进行细粒度编辑（如“抬起左手”改为“放下左手”）。
4. 将编辑后的详细描述与原始粗标题一同输入(T&DT)2M-GPT，从零生成编辑后的运动。

用户研究表明，该流水线在空间编辑和时间编辑案例中均获得最高偏好分数，且在时间编辑上表现尤为突出。这一能力源于模型在训练阶段学习到了文本中身体部位描述与运动片段之间的精确对应关系。

### 创新边界与局限

需要指出的是，FineMotion的创新主要集中在**数据层面**和**文本编码策略层面**，其运动生成骨干网络（MDM、T2M-GPT、MoMask等）本身并未进行架构创新。此外，时间编辑效果优于空间编辑，反映了当前方法在空间维度精细控制上的不足；重新生成过程可能在指定编辑区域之外引入意外变化，这也是零样本编辑流水线的固有局限。



FineMotion 的整体框架围绕一个核心洞察展开：现有运动-文本数据集缺乏对**特定身体部位运动（Body Part Movement, BPM）及其时间信息**的细粒度描述，导致生成的运动难以精确控制。为解决这一问题，FineMotion 构建了一套从运动序列到细粒度文本描述，再反向支撑生成与编辑的完整流水线。

### 数据集构建流水线

FineMotion 数据集的构建流水线（Figure 3）由三个级联模块组成，实现了从原始运动序列到严格对齐的细粒度运动-文本对的大规模、可扩展生成。

![[assets/figures/papers/paper_list_l7_FineMotion_A_Dataset_and_Benchmark_with_both_Spatial_and_Temporal_Annota/figures/005_Figure_3.jpg]]
*Figure 3: The construction pipeline of our FineMotion dataset*

1.  **Snippet Segmentation（片段切分）**：将运动序列沿时间维度按固定时长 $T_s = 0.5$ 秒切分为短片段。该时长的选择基于两项原则：减少片段间描述冗余，以及不超过 PoseFix 模型中位姿对选取的最大时间差限制。任何长度不足 $T_s$ 的剩余片段同样被视为独立片段处理。

2.  **Snippet Description Generation（片段描述生成）**：利用 **PoseFix** 的校正文本生成模型，为每个片段自动生成身体部位运动描述（BPMSD）。该模型将源位姿与目标位姿的嵌入整合到文本 Transformer 的交叉注意力机制中，生成描述“如何将源位姿各身体部位修正为目标位姿”的校正文本。自动生成的描述随后经过**人工校正**，以确保描述的精确性与对齐质量。

3.  **Paragraph Generation（段落生成）**：通过 **Gemini** 模型的语言能力，将片段描述组织成连贯的段落描述（BPMP），形成对整个运动序列的细粒度文本概括。

最终，FineMotion 数据集包含超过 **442,000** 个人体运动片段及其对应的身体部位运动描述，以及约 **95,000** 个段落描述。

### 文本到运动生成框架

为充分利用 FineMotion 数据集的细粒度文本，论文设计了双文本条件生成框架（以 (T&DT)2M-GPT 为代表，Figure 11）。该框架接收两类文本输入：

-   **粗粒度文本（Coarse Text）**：来自 HumanML3D 的原始简短标题。
-   **细粒度文本（Detailed Text）**：来自 FineMotion 的片段描述，通过固定模板连接所有 BPMSD，空片段以特殊标记 `<Motionless>` 替换，片段间以 `<SEP>` 分隔。

两类文本分别经 **T5-Base** 编码器编码后，其嵌入被拼接作为条件，输入基于 GPT 的运动令牌生成器。生成器通过预测下一个运动令牌的交叉熵损失进行训练：

$$L = - \sum_{i=1}^{\lfloor T / l \rfloor} \log(P(c_i \mid t_{\mathrm{coarse}}, t_{\mathrm{detail}}, c_{<i}, \theta_{\mathrm{GPT}}))$$

其中 $c_i$ 为运动令牌，$t_{\mathrm{coarse}}$ 和 $t_{\mathrm{detail}}$ 分别为粗、细文本的嵌入。

### 零样本细粒度运动编辑流水线

FineMotion 数据集进一步支撑了零样本细粒度运动编辑能力（Figure 6）。编辑流水线的工作流如下：

![[assets/figures/papers/paper_list_l7_FineMotion_A_Dataset_and_Benchmark_with_both_Spatial_and_Temporal_Annota/figures/009_Figure_6.jpg]]
*Figure 6: Pipeline for zero-shot fine-grained motion editing. To edit human motion with fine granularity, users first provide a coarse textual description of the desired motion. An initial motion is generated using any text-to-motion (T2M) model. This motion is then processed through the dataset construction pipeline to extract its BPM snippet descriptions. Users refine these descriptions with detailed editing instructions. Finally, the baseline model generates the fine-grained edited motion by adhering to both the modified BPM snippets and the original coarse caption*

1.  **初始生成**：用户提供粗粒度文本描述，由任意文本到运动模型生成初始运动序列。
2.  **描述提取与编辑**：将初始运动序列送入数据集构建流水线，提取其 BPM 片段描述。用户在片段描述层面进行精细编辑（如指定某身体部位的空间变化或某时间段的行为修改）。
3.  **重新生成**：将编辑后的细粒度描述与原始粗粒度标题一同输入 (T&DT)2M-GPT，从头生成满足编辑要求的运动序列。

该流水线的关键优势在于**零样本**能力：编辑模型无需在编辑对数据上额外训练，直接复用 FineMotion 数据集训练好的文本到运动模型即可。用户研究表明，该流水线在空间编辑和时间编辑任务上均获得最高偏好分数，且在时间编辑上表现尤为突出。

### 关键设计决策

-   **文本编码器替换**：为处理超长的细粒度文本，框架将基线模型中的 CLIP 文本编码器统一替换为 **T5-Base**，避免文本截断。
-   **分离编码策略（T&DT）**：粗文本和细文本分别编码后再拼接嵌入，而非拼接为单一文本后编码。消融实验证实，分离编码策略显著优于拼接编码策略（MoMask BPMSD 的 R-Top3: 0.811 vs 0.434），表明模型能更有效地从独立编码中解耦粗、细语义。
-   **时间增强训练**：训练时使用 FineMotion 的细粒度时间对齐文本，使模型学习到运动与文本在时间维度上的精确对应关系，这是支撑零样本时间编辑能力的核心机制。



### 3.1 数据集构建流水线的关键模块

FineMotion 数据集的核心贡献在于其自动化、可扩展的细粒度运动描述生成流水线（Figure 3），该流水线包含三个关键模块：

**Snippet 切分模块**  
该模块将运动序列沿时间维度切分为短片段。片段时长 $T_s$ 被固定为 0.5 秒，这一选择基于两项原则：其一，减少相邻片段描述之间的冗余；其二，不超过 PoseFix 模型在生成校正文本时对姿态对时间差的最大容忍限制。任何运动序列中不足 $T_s$ 的剩余部分同样被作为一个独立片段处理。

**Snippet 描述生成模块**  
该模块利用 PoseFix 的校正文本生成模型，为每个片段自动生成身体部位运动描述。具体而言，该模型将源姿态与目标姿态的两个嵌入整合到文本 Transformer 的交叉注意力机制中，生成描述身体部位应如何从源姿态修改到目标姿态的校正文本。在自动生成的基础上，部分片段描述经过人工校正，以提供更精确的监督信号。

**段落生成模块**  
该模块借助 Gemini 的语言能力，将片段级别的身体部位运动描述组织成连贯的段落文本，从而为完整运动序列提供全局性的细粒度语义描述。

### 3.2 文本编码策略

为处理细粒度文本的长度问题，FineMotion 将基线模型中的 CLIP 文本编码器替换为 T5-Base，以避免超长详细文本被截断。在此基础上，粗粒度文本与细粒度文本采用分离编码后拼接嵌入的策略（T&DT），而非将二者拼接为单一文本后编码（TDT）。具体嵌入计算如下：

**粗文本嵌入**  
$$
t_{\mathrm{coarse}} = \mathbf{Mean}(\mathrm{T5Encoder}(X_{\mathrm{coarse}})) \in \mathbb{R}^{768}
$$
对粗标题文本 $X_{\mathrm{coarse}}$ 经 T5 编码后的所有 token 嵌入取均值池化，得到 768 维的粗粒度条件向量。

**细粒度文本嵌入**  
$$
\hat{t}_{\mathrm{detail}} = \mathbf{Mean}(\mathrm{T5Encoder}(\hat{X}_{\mathrm{detail}})) \in \mathbb{R}^{768}
$$
对编辑后的细粒度运动描述文本 $\hat{X}_{\mathrm{detail}}$ 经 T5 编码后取均值池化，得到 768 维的细粒度条件向量。在训练与推理中，粗、细两个嵌入被拼接后作为运动生成的条件输入。

### 3.3 运动令牌预测损失

在基于 GPT 的运动生成框架中，训练目标为下一个运动令牌的条件预测交叉熵损失：

$$
L = - \sum_{i=1}^{\lfloor T / l \rfloor} \log(P(c_i \mid t_{\mathrm{coarse}}, \hat{t}_{\mathrm{detail}}, c_{<i}, \theta_{\mathrm{GPT}}))
$$

其中 $c_i$ 为第 $i$ 个运动令牌，$c_{<i}$ 为之前时刻的运动令牌序列，$T$ 为运动序列长度，$l$ 为运动 VQ-VAE 的下采样因子，$\theta_{\mathrm{GPT}}$ 为 GPT 模型参数。该损失函数使模型在粗、细两种文本条件的共同约束下，学习生成与描述严格对齐的运动序列。



## 实验与关键发现

### 文本标注流水线的消融验证

为验证FineMotion数据集构建流水线中文本标注的质量，作者以(T&DT)2M-GPT为基线，在HumanML3D测试集上进行了多组消融实验（Table 2）。实验将粗粒度描述（T）与细粒度详细文本（DT）逐步组合，以观察不同粒度的文本对运动生成性能的影响。

![[assets/figures/papers/paper_list_l7_FineMotion_A_Dataset_and_Benchmark_with_both_Spatial_and_Temporal_Annota/figures/007_Table_2.jpg]]
*Table 2: Evaluation of our textual annotation pipeline with (T&DT)2M-GPT. ‘T’ means coarse descriptions on the HumanML3D, while ‘DT’ means detailed texts on our FineMotion dataset. We repeat all evaluations 20 times and report the average with a 95% confidence interval. Bold text means the best results in each block. Results show that incorporating our fine-grained and human-annotated texts enhances motion generation performance, which proves the quality of our textual annotation pipeline*

仅使用粗文本训练时，模型FID为0.123，R-Top3为0.781。在此基础上引入自动生成的BPM片段描述（BPMSD）后，FID显著降至0.091，R-Top3提升至0.789；若替换为自动生成的BPM段落描述（BPMP），FID进一步降至0.088，R-Top3达到0.790。这一趋势表明，细粒度的身体部位运动描述为模型提供了更精确的运动细节约束，使生成结果更贴近真实运动分布。

更关键的是，当使用**人工标注**的BPM描述替换自动生成文本后，BPMSD配置达到FID 0.091、R-Top3 0.789，BPMP配置达到FID 0.100、R-Top3 0.788。人工标注在FID上并未全面超越自动标注，但作者指出人工标注“提供了更精确的指导”，其优势在定性分析和下游编辑任务中更为明显。综合来看，自动生成与人工标注的BPM文本均能有效提升生成质量，验证了FineMotion标注流水线的有效性。

### FineMotion基准与粗粒度基线对比

Table 3展示了在FineMotion数据集上训练的各变体与在HumanML3D粗文本上训练的基线模型之间的全面对比。为保证公平性，所有带†标记的基线方法均使用相同的T5-Base文本编码器重新实现。

核心发现如下：

- **(T&DT)-MDM** 的R-Precision Top-3达到0.759，相比其粗文本基线MDM的0.606**提升了+15.3%**，这是所有变体中检索准确率提升幅度最大的。同时FID从0.544降至0.121，MModality从2.794提升至3.519，表明细粒度文本训练使MDM生成的运动在语义对齐和多样性上均有质的飞跃。
- **(T&DT)-MoMask** 在FID指标上表现最优，从粗文本基线的0.249降至**0.055**，R-Top3也从0.753提升至0.799。但值得注意的是，其MModality从1.241降至0.986，说明更强的文本约束可能在一定程度上限制了生成多样性。
- **(T&DT)2M-GPT** 在保持较高MModality（2.103 vs 基线1.907）的同时，FID从0.123改善至0.091，R-Top3从0.781提升至0.789，在多样性与质量之间取得了较好的平衡。

所有FineMotion变体在FID和R-Precision上均优于对应的粗文本基线，证明细粒度BPM文本能够为各类主流文本-运动生成架构提供有效的监督信号。

### 粗/细文本编码策略消融

Table 5探究了粗文本与细文本的不同编码方式对性能的影响。实验对比了两种策略：**TDT**（将粗文本与细文本拼接为单一文本后统一编码）与**T&DT**（分别编码两种文本后拼接嵌入向量）。

以MoMask为骨干网络，使用BPMSD细文本时：
- TDT策略的R-Top3仅为0.434，远低于T&DT策略的**0.811**。
- 同时TDT的FID为0.068，T&DT为0.056，后者同样更优。

这一巨大差距揭示了关键因果机制：粗文本和细文本在语义粒度和信息结构上存在本质差异，将它们强行拼接为单一序列会导致文本编码器无法有效区分和提取两种信息。分别编码后拼接嵌入向量的策略，使模型能够独立地从粗文本中捕获全局运动意图、从细文本中提取局部身体部位运动细节，从而实现更精确的条件控制。

### 时间对齐性分析

为量化细粒度文本训练对运动时间对齐性的影响，作者引入了$\mathrm{FID}_c$指标（Table 6），该指标通过计算生成运动与真实运动在时间维度上的分布差异来评估时间对齐精度。

![[assets/figures/papers/paper_list_l7_FineMotion_A_Dataset_and_Benchmark_with_both_Spatial_and_Temporal_Annota/figures/017_Table_6.jpg]]
*Table 6: Comparison of temporal alignment, measured by $\mathrm { F I D } _ { c }$ between baseline text-to-motion models and our fine-grained variants*

在(T&DT)2M-GPT框架下，仅用粗文本训练时$\mathrm{FID}_c$为0.401；加入自动生成的BPMSD后降至0.370，加入BPMP后进一步降至0.349。类似趋势在MoMask和MDM变体上同样成立——所有FineMotion变体的$\mathrm{FID}_c$均低于仅用粗文本的基线。这表明，BPM描述中蕴含的时序信息（通过固定0.5秒切片和顺序排列的片段描述隐式编码）能够有效引导模型学习运动的时间结构，使生成运动的节奏和动作转换更贴近真实数据。

### 零样本细粒度运动编辑

FineMotion数据集还解锁了一项重要能力：零样本细粒度运动编辑（Figure 6）。编辑流水线如下：用户提供粗粒度文本描述，由任意T2M模型生成初始运动；将该运动通过数据集构建流水线提取BPM片段描述；用户对需要修改的片段描述进行编辑（如“将左手从腰部举过头顶”）；最后，(T&DT)2M-GPT根据修改后的BPM描述和原始粗文本重新生成运动。

用户研究（Figure 7）从三个维度评估编辑结果：(1) 是否满足编辑需求，(2) 编辑后运动的自然度，(3) 编辑后运动与原始运动的相似度。在9个编辑案例（3个空间编辑、6个时间编辑）中，所提流水线在所有维度上均获得最高平均偏好分数，且在时间编辑案例上优势尤为突出。

### 失败模式与局限性

尽管FineMotion在运动生成和编辑上取得了显著提升，论文明确指出了以下局限：

1. **空间编辑精度不足**：由于训练数据中的细粒度文本主要通过时间切片获得，模型对时间维度的编辑（如改变动作顺序、调整动作时长）比空间维度的编辑（如修改特定关节的轨迹）更直接、准确。用户研究中空间编辑仅占3/9案例，侧面反映了这一短板。
2. **重生成引入意外变化**：编辑流水线采用“从零生成”而非“局部修改”的策略，可能在指定编辑区域之外引入非预期的运动变化，影响编辑的精确性和可控性。
3. **缺乏定量评估指标**：目前尚无直接评估细粒度运动编辑结果的标准定量指标，用户研究是目前唯一可靠的评估手段，这限制了方法的可复现比较。
4. **文本获取流程复杂**：从运动序列获取详细的BPM文本描述仍需多步骤处理（切片→PoseFix生成→人工校正），端到端的运动-文本联合建模仍是开放问题。

### 补充图表

![[assets/figures/papers/paper_list_l7_FineMotion_A_Dataset_and_Benchmark_with_both_Spatial_and_Temporal_Annota/figures/002_Table_1.jpg]]
*Table 1: Comparisons of 3D human motion-language datasets*

![[assets/figures/papers/paper_list_l7_FineMotion_A_Dataset_and_Benchmark_with_both_Spatial_and_Temporal_Annota/figures/008_Table_3.jpg]]
*Table 3: Benchmark of FineMotion & Comparisons with HumanML3D. We conduct all evaluations 20 times, reporting the average with a 95% confidence interval, except for MModality, which is run 5 times. ‘→’ means results are better if the metric is closer to the real motions. For methods marked with †, we re-implement them using the same text encoder (T5) as ours to ensure fair comparisons. All our variants exhibit performance improvements, with (T&DT)-MDM showing a notable +15.3% increase in Top-3 retrieval accuracy*

![[assets/figures/papers/paper_list_l7_FineMotion_A_Dataset_and_Benchmark_with_both_Spatial_and_Temporal_Annota/figures/015_Table_4.jpg]]
*Table 4: Generation performance of all our variants on the T2M test set, i.e., motion generation conditioned on coarse descriptions only*

![[assets/figures/papers/paper_list_l7_FineMotion_A_Dataset_and_Benchmark_with_both_Spatial_and_Temporal_Annota/figures/016_Table_5.jpg]]
*Table 5: Ablation study on different strategies for encoding coarse and detailed texts*



## 定位与知识库关联

### 1. 与现有工作的关系定位

FineMotion 的核心贡献在于构建了一个**严格对齐的细粒度人体运动-文本数据集**，并基于此数据集展示了现有文本-运动生成模型在细节和时间控制上的显著性能提升。其定位可从以下两个维度理解：

#### 1.1 相对于粗粒度文本-运动生成模型

FineMotion 并非提出一个全新的生成模型架构，而是作为一个**数据增强与文本编码策略**，可直接适配于现有的主流文本-运动生成基线。论文在以下模型上验证了其方法的有效性：

- **MDM**：基于扩散的文本-运动生成模型，作为粗粒度基线。使用 FineMotion 的细粒度文本后，Top-3 检索准确率提升了 **+15.3%**（Table 3），FID 从 0.544 降至 0.081（(T&DT)-MDM BPMP 变体）。
- **T2M-GPT**：基于 VQ-VAE 与 GPT 的运动生成模型。在 (T&DT)2M-GPT 变体上，加入人工注释的 BPM 片段描述（BPMSD）将 FID 从 0.123 降至 **0.091**，R-Top3 从 0.781 升至 **0.789**（Table 2）。
- **MoMask**：基于掩码建模的运动生成方法。在 (T&DT)-MoMask BPMP 变体上，FID 从 0.249 降至 **0.055**（Table 3），取得了所有变体中最佳的 FID 和 R-Precision。
- **TEMOS**、**TM2T**、**Guo et al.**：同样作为粗粒度基线被纳入基准对比（Table 3）。

这些结果表明，FineMotion 的数据集和文本处理策略具有**模型无关性**，可作为即插即用的增强模块提升各类生成模型的细粒度控制能力。

#### 1.2 相对于细粒度文本-运动生成模型

与已有的细粒度方法相比，FineMotion 的差异化优势在于**文本描述与运动序列的严格时空对齐**：

- **MotionDiffuse**：虽然支持细粒度文本条件，但其文本描述并未与特定身体部位的运动时间切片严格对齐。FineMotion 通过固定时长切片（0.5 秒）和身体部位运动（BPM）描述，实现了更精确的对应关系。
- **Fg-T2M** 和 **FineMoGen**：同为细粒度文本-运动生成方法，但其细粒度描述通常通过大语言模型对粗标题进行增强获得，缺乏与真实运动序列的严格对齐验证。FineMotion 则通过 PoseFix 模型从实际运动数据自动生成描述，并辅以人工校正，确保了对齐的可靠性。

### 2. 适用边界

FineMotion 的适用性受以下因素制约：

1. **空间编辑能力弱于时间编辑**：由于训练数据通过时间切片增强，模型沿时间轴的学习更为充分。用户研究表明，所提零样本编辑流水线在时间编辑案例（6 个案例）上获得最高偏好分数，而空间编辑（3 个案例）的提升相对有限（Figure 7）。论文明确指出“沿时间轴的编辑比空间编辑更直接、准确，空间编辑能力仍需提升”。

2. **重新生成过程可能引入意外变化**：编辑流水线采用“从零生成”策略，即在修改后的文本条件下重新生成整个运动序列。这可能导致指定编辑区域之外的意外变化，缺乏对未编辑区域的显式保持机制。

3. **依赖多步骤流水线获取 BPM 描述**：当前获取详细的 BPM 文本描述需要经过运动切片、PoseFix 生成、人工校正等多个步骤，尚未实现端到端的自动化。

4. **缺乏细粒度编辑的定量评估指标**：目前尚无直接评估详细文本与生成运动序列之间时间对齐精度的标准指标，编辑效果的评估主要依赖用户研究（Figure 7）。

### 3. 局限与开放问题

论文明确指出的局限性包括：

- **空间编辑精度不足**：需要开发更有效的空间人体运动编辑方法。
- **BPM 描述获取效率低**：未来可研究端到端模型直接从运动序列推断详细的身体部位文本描述。
- **编辑过程中的非预期变化**：重新生成策略可能引入指定区域外的意外变化。
- **评估指标缺失**：如何量化评估细粒度运动编辑结果仍是一个开放挑战。

此外，论文提出的开放问题还包括：

- 如何利用大语言模型通过多粒度文本描述统一文本到运动和运动到文本的双向任务？
- 能否训练一个直接从运动序列推断详细 BPM 描述的端到端模型？

> **注意**：上述基线工作的具体作者、会议和年份信息在提供的分析材料中未明确给出，建议读者根据论文原文的参考文献列表进行核实。



## 原文 PDF

![[paperPDFs/ICCV_2025/FineMotion_A_Dataset_and_Benchmark_with_both_Spatial_and_Temporal_Annotation_for_Fine_grained_Motion_Generation_and_Editing.pdf]]
