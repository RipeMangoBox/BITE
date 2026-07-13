---
title: "LaMoGen: Language-to-Motion Generation Through LLM-Guided Symbolic Inference"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/LaMoGen_Language_to_Motion_Generation_Through_LLM_Guided_Symbolic_Inference.pdf
project_link: https://jjkislele.github.io/LaMoGen/
code_link: null
aliases:
- LaMoGen
tags:
- CVPR_2026
- topic/motion_animation
- topic/motion_animation/human_motion_generation
core_operator: "引入LabanLite——一种基于拉班记谱法的帧级、身体部位感知的符号化运动表示，将运动分解为由概念符号和细节符号组成的序列；并利用LLM通过检索增强提示实现高层次的符号运动规划，取代传统的端到端黑盒映射。"
primary_logic: "人类运动本质上可抽象为离散的、可解释的拉班符号序列，每个概念符号对应一个标准化的文本描述（概念描述），从而允许LLM像处理语言一样进行符号推理、组合与编辑，无需直接处理原始运动数据；这种双层次设计（LLM规划 + 运动生成器）实现了对运动类型、时序和协调性的精细控制。"
claims:
- "在Laban Benchmark上，LaMoGen (GPT4.1) 在所有Laban指标（SMT、TMP、HMN）上均大幅超越现有方法，例如SMT supL达到0.583，而最好的基线MoDiff为0.491。"
- "在HumanML3D标准测试上，LaMoGen在R@3（0.796）和FID（0.252）上与最优方法竞争，同时在Laban指标上保持显著优势，证明其对细粒度文本的理解能力。"
- "消融实验表明，LLM符号规划（相比无LLM的变体）对Laban指标贡献巨大，且更强的LLM（如GPT4.1）带来更好效果。"
- "定性结果显示，LaMoGen能准确执行“前进5步后退3步”等包含精确步数和时序的指令，而MDM等方法只生成通用的行走循环。"
---

# LaMoGen: Language-to-Motion Generation Through LLM-Guided Symbolic Inference

> [!tip] 核心洞察
> 人类运动本质上可抽象为离散的、可解释的拉班符号序列，每个概念符号对应一个标准化的文本描述（概念描述），从而允许LLM像处理语言一样进行符号推理、组合与编辑，无需直接处理原始运动数据；这种双层次设计（LLM规划 + 运动生成器）实现了对运动类型、时序和协调性的精细控制。

| 字段 | 内容 |
|------|------|
| 中文题名 | LaMoGen：通过LLM引导的符号推理实现语言到运动生成 |
| 英文题名 | LaMoGen: Language-to-Motion Generation Through LLM-Guided Symbolic Inference |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.11605) · [Project](https://jjkislele.github.io/LaMoGen/) |
| Topic | #topic/motion_animation #topic/motion_animation/human_motion_generation |
| Method | LaMoGen |
| Dataset | Laban Benchmark (HumanML3D-Laban), HumanML3D, KIT-ML |

> [!tip] 效果简介
> - Laban Benchmark (HumanML3D-Laban) 上，SMT (Semantic Alignment) supL 为 0.583 (GPT4.1)，对比 0.491 (MoDiff)，变化 +0.092。
> - Laban Benchmark (HumanML3D-Laban) 上，FID 为 1.859 (DeepSeekV3)，对比 2.072 (MotionGPT)，变化 -0.213。
> - HumanML3D 上，R-precision Top-3 为 0.796 (GPT4.1)，对比 0.740 (Guo et al.)，变化 +0.056。

## 概要

现有文本到运动生成方法普遍依赖文本-运动联合嵌入，难以精确捕捉指令中的细粒度时间结构（如步数、顺序、持续时间）与多身体部位的协调性，导致在复杂文本上语义与时间对齐不佳，且生成过程缺乏可解释性。LaMoGen 的核心洞察在于：人体运动本质上可抽象为离散、可解释的符号序列——每个符号对应标准化的概念描述，从而使大语言模型能够像处理自然语言一样进行符号推理、组合与编辑，无需直接处理原始运动数据。

该方法的关键突破体现在两个层面。在表示层面，LaMoGen 引入 **LabanLite**——一种基于拉班记谱法的帧级、身体部位感知的符号化运动表示，将运动分解为由概念符号与细节符号组成的序列，并赋予每个概念符号以标准化文本描述。在生成层面，LaMoGen 采用 **LLM 引导的符号推理** 替代传统端到端黑盒映射：首先由 LLM 通过检索增强提示生成高层次概念符号序列（运动规划），再由 Kinematic Detail Augmentor 自回归地补充细节符号，最终由运动解码器重构为 SMPL 姿态序列。这种双层次设计实现了对运动类型、时序与协调性的精细控制，同时使符号序列本身具备人类可读性与 LLM 可编辑性。

实验结果表明，在专门构建的 Laban Benchmark 上，LaMoGen（GPT4.1）在所有拉班指标上大幅超越现有方法——SMT supL 达到 0.583，而最优基线 MoDiff 仅为 0.491（Table 1）。在 HumanML3D 标准测试上，LaMoGen 在 R@3（0.796）上与最优方法竞争，同时在拉班指标上保持显著优势（Table 2）。消融实验确认，LLM 符号规划组件对拉班对齐指标贡献巨大，且更强的 LLM 持续带来性能提升。定性结果进一步显示，LaMoGen 能准确执行“前进 5 步后退 3 步”等含精确步数和时序的指令，而 MDM 等方法仅生成通用行走循环（Figure 3）。

文本驱动的人体运动生成旨在根据自然语言描述合成逼真的三维人体动作序列，在动画制作、虚拟人交互、游戏开发等领域具有广泛的应用前景。近年来，基于扩散模型和离散动作标记的生成方法取得了显著进展，在标准基准（如HumanML3D、KIT-ML）上的FID和R-Precision指标不断刷新。然而，现有方法存在一个关键的瓶颈：**它们主要依赖文本-运动联合嵌入进行端到端的黑盒映射，难以精确捕捉指令中的细粒度时间结构**。

具体而言，当用户输入包含精确步数、顺序约束、持续时间或特定身体部位协调要求的复杂指令时（例如“前进5步，然后后退3步”），基于联合嵌入的方法往往只能生成语义大致相关的通用动作循环，而无法忠实执行指令中的计数、时序和协调细节。这种失败源于两个深层原因：

1. **时间维度被隐式编码**：现有方法将动作序列的时间结构压缩到连续的潜在向量中，缺乏对子动作持续时间和先后顺序的显式建模能力，导致生成的动作在时间对齐上存在偏差。
2. **身体部位协调性难以保证**：文本-运动联合嵌入通常将全身运动作为一个整体进行编码，难以精细控制不同身体部位（如左右臂、双腿）之间的协调关系，当指令涉及多个身体部位的异步或组合动作时，生成的运动往往出现语义错位。

此外，这种黑盒生成范式还带来了**可解释性和可控性不足**的问题。用户无法理解模型为何生成特定动作，也难以对生成结果进行精确的局部编辑——例如将“右手举高”改为“左手举高”，而不影响其他身体部位的运动。

上述问题在现有评估体系下被部分掩盖：标准的FID和R-Precision指标主要衡量生成运动的整体质量与文本的宏观语义匹配，但对细粒度时间结构和身体部位协调性的敏感度不足。因此，亟需一种既能实现精细语义对齐，又具备可解释性和可控性的新范式。

正是在这一背景下，LaMoGen提出了一种根本性的思路转变：**将运动生成从连续的端到端映射，转变为基于离散符号的推理与组合过程**。其核心动机是引入**LabanLite**——一种基于拉班记谱法（Labanotation）的帧级、身体部位感知的符号化运动表示，将运动分解为可解释的符号序列；并利用大语言模型（LLM）的推理能力，通过检索增强提示实现高层次的符号运动规划，从而实现对运动类型、时序和身体部位协调性的精细控制。这一设计不仅解决了细粒度时间结构的建模难题，还赋予了系统人类可读的符号中间表示，使得运动编辑和对话式交互成为可能。

## 核心方法与创新机理

### 1. 瓶颈突破：从黑盒嵌入到可解释符号推理

现有文本-运动生成方法（如 **MDM**、**ReMoDiff**、**MoDiff**、**MotionGPT** 等）主要依赖文本-运动联合嵌入空间进行端到端映射。这种范式存在一个根本性瓶颈：**难以精确捕捉指令中的细粒度时间结构**（如步数、顺序、持续时间）以及**多身体部位的协调性**，导致生成的动作在复杂文本上语义和时间对齐不佳，且生成过程完全黑盒，缺乏可解释性与可控性。

LaMoGen 的核心突破在于**将运动生成从连续嵌入空间的隐式映射，转化为离散符号空间的显式推理**。具体而言，该方法引入了 **LabanLite**——一种基于拉班记谱法（Labanotation）的帧级、身体部位感知的符号化运动表示，将运动分解为由**概念符号**（Conceptual Symbols）和**细节符号**（Detail Symbols）组成的序列。这一设计使得人类运动可被抽象为离散的、可解释的符号序列，每个概念符号对应一个标准化的文本描述（概念描述），从而允许大语言模型（LLM）像处理语言一样进行符号推理、组合与编辑，无需直接处理原始运动数据。

### 2. 关键机制创新：双层次生成架构

LaMoGen 的核心创新体现在其**双层次生成架构**上，该架构将运动生成分解为高层符号规划与低层运动合成两个阶段，实现了对运动类型、时序和协调性的精细控制。

#### 2.1 中间表示的根本变革：从联合嵌入到 LabanLite 符号序列

| 设计维度 | 基线方法 | LaMoGen |
|---------|---------|---------|
| **中间表示** | 连续或离散的文本-运动联合嵌入 | LabanLite 符号序列（概念符号 + 细节符号），关联标准化概念描述 |
| **运动规划机制** | 解码器直接从文本条件生成运动序列（单阶段） | 两阶段：LLM 通过检索增强提示生成高层次概念符号序列，然后 Kinematic Detail Augmentor 自回归地丰富细节 |
| **时间结构处理** | 时间维度隐式编码，难以精确控制持续时间和步数 | 显式的持续时间字段（每符号带时间），帧级标注，LLM 可直接指定子动作的时长 |
| **可解释性与可控性** | 生成过程黑盒，难以解释或编辑 | 符号序列人类可读，可通过编辑符号或文本直接修改运动，LLM 可实现对话式编辑 |

LabanLite 符号序列作为中间表示的核心优势在于：每个概念符号（如“左腿前迈步”）都绑定了一个标准化的**概念描述**，这些描述存储在概念描述数据库中。当 LLM 进行符号规划时，它实际上是在一个语义清晰的文本-符号对应空间中进行操作，而非处理难以解释的潜在向量。

#### 2.2 LLM 引导的符号运动规划

LaMoGen 的第二项关键创新是**利用 LLM 通过检索增强提示（Retrieval-Augmented Prompting）实现高层次的符号运动规划**。给定用户的文本指令，系统从概念描述数据库中检索最相关的示例，构建包含任务描述、可用概念符号列表及检索示例的提示，引导 LLM 生成概念符号序列作为运动计划。

这一设计的核心洞察在于：**LLM 无需理解原始运动数据的数值细节，只需在符号层面进行组合推理**——如同编写一个高层次的动作脚本。消融实验（Table 1）直接验证了该组件的决定性作用：移除 LLM 符号规划（'None' 配置）会导致 SMT 和 TMP 指标显著下降，而使用更强的 LLM（如 GPT4.1 相较于 GPT4.1-mini）持续提升性能。

#### 2.3 Kinematic Detail Augmentor 的细节补充

LLM 生成的概念符号序列仅描述了运动的“骨架”（如动作类型和大致顺序），缺少具体的运动学细节（如幅度、速度变化）。**Kinematic Detail Augmentor** 作为第二阶段的生成模块，自回归地将概念序列扩展为完整的 LabanLite 代码。该模块以文本条件和已生成的部分符号序列为输入，逐帧预测完整的二进制指示向量，其训练目标为二进制交叉熵损失：

$$\mathcal{L}_{gen} = -\sum_{t,n} \left[ v_t^n \log p_t^n + (1 - v_t^n) \log(1 - p_t^n) \right]$$

这种双层次设计实现了**关注点分离**：LLM 负责需要常识推理和组合能力的高层规划，而 Augmentor 负责需要运动学知识的低层细节补充，两者各司其职，协同完成精细运动生成。

### 3. 创新效果的决定性证据

LaMoGen 的创新在多个维度上得到了实验验证：

- **细粒度语义对齐的显著提升**：在 Laban Benchmark 上，LaMoGen (GPT4.1) 在所有 Laban 指标（SMT、TMP、HMN）上均大幅超越现有方法，例如 SMT supL 达到 0.583，而最好的基线 MoDiff 仅为 0.491（Table 1），证明符号推理范式在捕捉细粒度指令方面的优势。

- **精确时序控制能力**：定性结果（Figure 3）显示，LaMoGen 能准确执行“前进5步后退3步”等包含精确步数和时序的指令，而 MDM 等方法只生成通用的行走循环，无法体现步数差异。

- **符号表示的有效性验证**：在标准 MDM 基线上引入符号条件可将 FID 降低约 20 倍（Table 6, Supplementary），直接验证了 LabanLite 作为中间表示的强大表达能力。

- **可编辑性与可解释性**：用户可通过编辑符号序列或修改文本直接调整生成的运动（Section 5.2.1），LLM 支持对话式运动编辑，这是传统黑盒方法无法实现的能力。

### 4. 方法的局限与边界

尽管创新显著，LaMoGen 也存在明确边界：

1. **高层抽象与低层变化的权衡**：LabanLite 的高层抽象将不同速度的相同语义动作编码为相同符号，导致生成运动在标准 FID 指标上未达到最优（HumanML3D 上 0.252 vs ReMoDiff 0.103），运动在视觉细节上可能缺乏变化。

2. **LLM 依赖的风险**：概念描述数据库若不能覆盖文本中的稀有或组合动作，LLM 可能生成不符合预期的计划；LLM 本身存在幻觉风险。

3. **符号检测的启发式局限**：自动符号检测工作流依赖速度阈值等启发式规则，可能在非常慢的运动等特殊动作类型上检测不准。

4. **动作覆盖范围**：当前系统主要建模四肢的主要运动，尚未扩展到手部、手指精细动作和面部表情。

LaMoGen 提出了一种**双层次语言到运动生成框架**，其核心思路是将运动生成分解为高层符号规划与低层运动合成两个阶段，从而实现对复杂文本指令中细粒度时间结构与身体部位协调性的精确控制。

### 框架总览

整个流水线由三个关键组件构成闭环（见 Figure 2）：

![[assets/figures/papers/paper_list_l16_LaMoGen_Language_to_Motion_Generation_Through_LLM_Guided_Symbolic_Infere/figures/002_Figure_2.jpg]]
*Figure 2: Overview of LaMoGen: (a) The Laban-motion Encoder-Decoder enables bidirectional conversion between motion and Laban instances. These instances are human-readable and LLM-editable, as each instance has a symbolic appearance and a conceptual description, stored in the Conceptual Description Database. (b) LLMs perform high-level symbolic planning via retrieval-augmented prompting, generating sequences of conceptual symbols. The Kinematic Detail Augmentor then enriches these sequences with details through autoregressive generation. Enriched symbol sequences are converted to instances, encoded as codes, and decoded into fine-grained motions*

1. **Laban-Motion Encoder-Decoder (E/D)**：实现原始运动数据与 LabanLite 符号序列之间的双向转换，是整个框架的表示基础。
2. **LLM引导的符号规划**：利用大语言模型和检索增强提示，根据用户文本生成高层的概念符号序列，充当“运动规划器”。
3. **Kinematic Detail Augmentor + 运动解码器**：将概念符号序列自回归地丰富为完整的 Laban 代码，再通过解码器重构为 SMPL 姿态序列。

### 数据流与模块关系

框架的输入输出流可概括为以下路径：

**训练阶段（符号提取与编解码器学习）**：
- 原始运动序列 $X$ 通过**自动符号检测工作流 $\mathcal{F}$** 转换为 LabanLite 实例序列 $S = \mathcal{F}(X)$。
- 每个 Laban 实例被编码为二进制指示向量 $v_t$，通过 **Laban 代码本** 映射为潜在表示 $z_t = \sum_{n=1}^{N} v_t^n c_n$。
- **编码器 E** 将 $z_t$ 压缩为运动隐变量，**解码器 D** 从隐变量重构运动 $\hat{X}$，训练目标为重建损失 $\mathcal{L}_{rec}$（包含姿态和速度的 L1 损失）。

**推理阶段（文本到运动生成）**：
- 用户文本首先触发 **LLM 符号规划器**：LLM 从概念描述数据库中检索相关示例，通过提示工程生成概念符号序列（仅包含运动类型和大致持续时间）。
- **Kinematic Detail Augmentor** 以自回归方式，在文本条件和已生成符号的约束下，逐帧预测完整的细节符号，将概念序列扩展为完整的 LabanLite 代码。
- 最终的 Laban 代码经代码本嵌入后，送入**运动解码器 D**，输出 SMPL 姿态序列。

### 关键设计决策

- **符号化中间表示**：与现有方法依赖连续或离散的文本-运动联合嵌入不同，LaMoGen 采用 LabanLite 符号序列作为中间表示。每个符号关联一个标准化的概念描述，使得 LLM 可以像处理语言一样进行符号推理与组合，无需接触原始运动数据。
- **显式时间建模**：LabanLite 在帧级别标注每个符号的持续时间，LLM 可直接指定子动作的持续帧数，解决了传统方法中时间结构隐式编码、难以精确控制的问题。
- **可解释性与可编辑性**：生成的符号序列人类可读，用户可通过编辑符号或修改文本直接调整运动，支持对话式运动编辑。

### 证据强度说明

上述框架描述基于论文 Section 3 的完整方法论阐述，各模块的功能与连接关系在 Figure 2 中有明确可视化呈现。自动符号检测工作流的准确性在专家标注数据集上得到验证（SMT 0.871, TMP 0.852, HMN 0.786），为整个流水线的符号提取环节提供了可靠基础。消融实验进一步证实，LLM 符号规划组件对 Laban 对齐指标贡献巨大，移除 LLM 将导致 SMT 和 TMP 显著下降，验证了双层次设计的必要性。

### 3.1 LabanLite 符号化运动表示

LaMoGen 的核心创新在于引入 **LabanLite**——一种基于拉班记谱法（Labanotation）的帧级、身体部位感知的符号化运动表示。LabanLite 将连续运动数据抽象为离散的符号序列，每个符号实例包含两个层次：

- **概念符号（Conceptual Symbols）**：描述动作的语义类别，如“左腿向前迈步”、“右臂上举”等，每个概念符号关联一个标准化的**概念描述（Conceptual Description）**，使 LLM 能够像处理自然语言一样进行符号推理与组合。
- **细节符号（Detail Symbols）**：补充动作的低层属性，如方向、幅度、速度等，由后续的 Kinematic Detail Augmentor 自回归生成。

这种双层次设计使得运动生成从传统的“文本→运动”黑盒映射，转变为“文本→概念符号序列→完整符号序列→运动”的可解释流水线。Figure 1 对比了文本-运动联合嵌入方法与符号方法的本质差异：前者在结构化指令（如包含精确步数和时序的文本）上常产生语义不一致的运动，而符号方法通过显式的时间结构标注实现了精确对齐。

### 3.2 Laban-Motion 编码器-解码器

Laban-Motion Encoder-Decoder（E/D）实现了运动数据与 LabanLite 符号序列之间的双向转换，是整个框架的基础模块。

#### 3.2.1 自动符号检测工作流 F

给定原始运动数据 $X$（SMPL 姿态序列），自动符号检测工作流 $\mathcal{F}$ 将其转换为 LabanLite 实例序列 $S$：

$$S = \mathcal{F}(X)$$

该工作流包含三个步骤：动态分割（基于速度阈值检测动作边界）、逐帧提取（为每帧分配符号标签）、区间聚合（将连续相同符号合并为带持续时间的实例）。在专家标注数据集上，该工作流取得了高平均 SMT (0.871)、TMP (0.852) 和 HMN (0.786)（Table 3），验证了从运动提取语义符号的准确性。

#### 3.2.2 Laban 码本与潜在表示

所有唯一的 Laban 符号被聚合为 **Laban 码本** $C$，包含 $\bar{N}$ 个可学习的嵌入向量：

$$C = \{c_n\}_{n=1}^{\bar{N}}$$

对于帧 $t$，其潜在表示 $z_t$ 由所有活跃 Laban 码的嵌入向量加权求和得到：

$$z_t = \sum_{n=1}^{N} v_t^n c_n$$

其中 $v_t^n \in \{0, 1\}$ 是指示向量，表示第 $n$ 个码在帧 $t$ 是否活跃。这种求和机制使得编码器能够将离散符号序列压缩为连续的潜在向量，供后续 Transformer 解码器重构运动。

#### 3.2.3 重建损失

编码器-解码器通过以下重建损失进行训练，同时约束姿态和速度的 L1 误差：

$$\mathcal{L}_{rec}(X, \hat{X}) = \|X - \hat{X}\|_1 + \lambda \|\dot{X} - \dot{\hat{X}}\|_1$$

其中 $\hat{X}$ 为重建的运动序列，$\dot{X}$ 为速度（相邻帧姿态差），$\lambda$ 为速度损失的加权系数。该损失确保了解码器能够从 Laban 码本嵌入中准确恢复原始运动。

### 3.3 LLM 引导的双层次生成

LaMoGen 的生成过程分为两个阶段：LLM 高层次符号规划与 Kinematic Detail Augmentor 低层次细节补充。

#### 3.3.1 LLM 引导的概念组合

给定用户文本描述，LLM 通过**检索增强提示（Retrieval-Augmented Prompting）**生成概念符号序列。具体而言，系统从概念描述数据库中检索与输入文本最相关的示例（概念描述-符号对），将其作为上下文注入 LLM 提示，引导 LLM 输出结构化的概念符号序列。每个概念符号自带持续时间字段，使 LLM 能够显式指定子动作的时长（如“前进 5 步”对应 5 个带特定时长的步态符号），从而实现对时间结构的精确控制。

#### 3.3.2 Kinematic Detail Augmentor

Kinematic Detail Augmentor 以自回归方式将概念符号序列扩展为完整的 Laban 码序列。条件依赖于文本输入 $m$ 和历史预测 $\hat{v}_{1:t-1}$，Augmentor 逐帧预测完整的二进制指示向量 $v_t$：

$$\mathcal{L}_{gen} = -\sum_{t,n} \left[v_t^n \log p_t^n + (1 - v_t^n) \log(1 - p_t^n)\right]$$

该二进制交叉熵损失训练 Augmentor 准确预测每帧的细节符号存在性。消融实验表明，在 Laban 码上应用 0.3 的 masking 比例可达到最佳 FID 与生成多样性的平衡（Table 4, Supplementary）。

最终，完整的 Laban 码序列经码本嵌入求和后输入运动解码器 D（基于 Transformer），重构为 SMPL 姿态序列，完成从符号到运动的转换。

## 实验与关键发现

### 核心实验设计

LaMoGen 的评估在两个维度上展开：其一，在作者新构建的 **Laban Benchmark**（基于 HumanML3D-Laban）上，引入三个基于拉班记谱法的专用指标——**语义对齐（SMT）**、**时间对齐（TMP）** 与 **协调对齐（HMN）**——直接度量生成运动对细粒度指令（如步数、顺序、持续时间、身体部位协调）的执行精度。其二，在标准 **HumanML3D** 与 **KIT-ML** 测试集上沿用 R-Precision、FID、MM-Dist、Diversity、Multi-Modality 等常规指标，以检验方法在通用运动质量与文本-运动匹配度上的竞争力。

基线方法覆盖扩散模型（**MDM**、**MoDiff**、**ReMoDiff**）、基于姿态码的 **CoMo**、基于离散动作标记的 **MotionGPT** 以及早期文本-运动生成方法（**Guo et al.**）和运动学短语抽象方法（**KP**）。LaMoGen 自身包含四种 LLM 变体：GPT4.1、GPT4.1-mini、DeepSeekV3 和 Qwen3，以考察不同规模与能力的 LLM 对符号规划质量的影响。

### 主实验结果

#### Laban Benchmark：细粒度语义对齐全面领先

在 Laban Benchmark 上（Table 1），LaMoGen 在所有 Laban 指标上均大幅超越现有方法，且优势集中体现在对复杂时间结构与身体部位协调的精确建模上。以 GPT4.1 为 LLM 规划器的版本在 SMT supL 上达到 **0.583**，较最强基线 MoDiff（0.491）提升 +0.092；在 TMP supL 与 HMN supL 上同样保持显著领先。这表明，通过 LLM 生成的符号运动计划能够显式地捕获文本中的步数、顺序与持续时间约束，而端到端嵌入方法则难以从连续潜空间中解耦这些细粒度时间信息。

![[assets/figures/papers/paper_list_l16_LaMoGen_Language_to_Motion_Generation_Through_LLM_Guided_Symbolic_Infere/figures/003_Table_1.jpg]]
*Table 1: Quantitative comparisons on our Laban Benchmark, using the proposed Labanotation-based metrics, R-precision Top-3 (R@3) and FID. Bold and underlined values indicate the best and the second-best performance, respectively*

FID 指标上，DeepSeekV3 变体取得 **1.859**，优于 MotionGPT（2.072），但需注意 Laban Benchmark 的 FID 绝对值整体偏高，这与 LabanLite 的高层抽象特性直接相关：不同速度的相同语义动作被映射到同一符号，导致生成运动在低级变化上相对匮乏。

#### 标准基准：竞争力与固有局限并存

在 HumanML3D 与 KIT-ML 标准测试集上（Table 2），LaMoGen 在 R-Precision Top-3 上达到 **0.796**（GPT4.1），优于 Guo et al.（0.740），展现出较强的文本-运动语义匹配能力。然而，在 FID 指标上，LaMoGen 的最优结果（0.252，GPT4.1）与 ReMoDiff（0.103）存在明显差距。这一现象的根本原因在于 LabanLite 的符号化设计：它将“快速行走”与“缓慢行走”抽象为相同的概念符号，从而牺牲了低层运动变化以换取高层语义一致性。作者在 fairness notes 中明确指出，这是一种有意的设计取舍——当评估重心转向细粒度指令的语义忠实度时，LaMoGen 的优势便会凸显。

![[assets/figures/papers/paper_list_l16_LaMoGen_Language_to_Motion_Generation_Through_LLM_Guided_Symbolic_Infere/figures/005_Table_2.jpg]]
*Table 2: Quantitative comparisons with state-of-the-art methods on the HumanML3D test and KIT-ML test datasets, under standard protocols. Bold, underlined, and italicised values denote the best, second-best, and third-best performance, respectively. Table 3. Performance of Laban symbol detection on the Labanannotated motion dataset, using average Laban metrics. Bold values denote the best performance*

![[assets/figures/papers/paper_list_l16_LaMoGen_Language_to_Motion_Generation_Through_LLM_Guided_Symbolic_Infere/figures/018_Table_2.jpg]]
*Table 2: Quantitative comparison for LLM usage cost. The approximate token count per motion sequence for generation and modification is reported. Fig. 10. Each ranking position was assigned to exactly one method, ensuring mutual exclusivity*

#### 定性分析：精确时序与组合生成的直观证据

定性对比（Figure 3）提供了关键的行为证据。对于“前进 5 步，后退 3 步”这类包含精确步数和方向的指令，MDM 等方法仅生成通用的行走循环，无法体现步数差异；而 LaMoGen 则准确执行了指定步数，并在前进与后退之间呈现清晰的过渡。LLM 生成的概念符号序列（展示于生成结果下方）直接对应文本中的子动作，使整个过程具有可解释性。在需要多身体部位协调的场景（如“左手抬起同时右腿向前迈出”）中，LaMoGen 同样展现出精确的部位控制能力，而基线方法常出现部位动作错位或遗漏。

### 消融实验

#### LLM 符号规划的核心贡献

消融实验（Table 1 中 LaMoGen 变体与 “None” 配置的对比，以及 Supplementary Table 6）直接验证了 LLM 符号规划组件的决定性作用。移除 LLM（“None” 配置）导致 SMT 和 TMP 指标显著下降，表明高层符号规划是实现细粒度语义对齐的必要条件。此外，使用更强 LLM（从 GPT4.1-mini 到 GPT4.1）持续提升 Laban 指标，说明 LLM 的推理能力直接影响符号计划的准确性与完整性。

#### 符号条件对运动生成的增益

在标准 MDM 基线上引入 Laban 符号条件可将 FID 降低约 20 倍（Table 6，Supplementary），这一幅度远超常规改进，强有力地证明 LabanLite 符号表示本身携带了丰富的运动语义信息，能够有效引导解码器生成与文本意图一致的运动序列。

#### 检索示例数量与 Masking 比例

Supplementary Table 4 的消融显示：将检索示例数量从 1 增加到 3 显著改善 FID 和 MM-Dist，但进一步增加至 5 或 7 无额外收益，说明 3 个示例已能提供足够的上下文引导。在 Laban 代码上应用 0.3 的 masking 比例达到最佳 FID 与生成多样性平衡，这一设置被用于主实验。

![[assets/figures/papers/paper_list_l16_LaMoGen_Language_to_Motion_Generation_Through_LLM_Guided_Symbolic_Infere/figures/024_Table_4.jpg]]
*Table 4: Ablation study of different numbers of top-matched references and masking ratios on the HumanML3D test set*

### 自动符号检测的可靠性验证

自动符号检测工作流 F 的准确性直接决定整个框架的上限。在专家标注数据集上（Table 3，main paper），该工作流取得了高平均 SMT（0.871）、TMP（0.852）和 HMN（0.786），表明从原始运动数据中提取 LabanLite 符号序列的流程足够可靠，为后续 LLM 规划与运动生成提供了坚实的语义基础。

![[assets/figures/papers/paper_list_l16_LaMoGen_Language_to_Motion_Generation_Through_LLM_Guided_Symbolic_Infere/figures/021_Table_3.jpg]]
*Table 3: Quantitative comparisons on the HumanML3D test set, using the proposed Labanotation-based metrics: Semantic Alignment (SMT), Temporal Alignment (TMP), and Harmonious Alignment (HMN), along with Text-to-Motion metrics: R-precision Top-3 (R@3) and FID. Bold and underlined values indicate the best and the second-best performance, respectively*

### 失败模式与局限分析

尽管 LaMoGen 在细粒度语义对齐上表现突出，其局限性同样清晰：

1. **低层运动变化匮乏**：LabanLite 的高层抽象将不同速度、幅度的同类动作映射为相同符号，导致 FID 在标准基准上未达最优，生成的运动在视觉细节上可能显得单调。这是当前符号化设计的内在权衡，而非工程缺陷。

2. **身体部位覆盖不全**：当前系统主要建模四肢的主要运动，尚未扩展到手部、手指精细动作和面部表情，限制了其在需要全身精细控制场景（如手语、乐器演奏）中的应用。

3. **LLM 依赖与幻觉风险**：概念符号规划完全依赖 LLM 的检索增强提示。若概念描述数据库无法覆盖文本中的稀有或组合动作，LLM 可能生成不符合预期的计划；LLM 自身的幻觉问题也可能引入错误的符号序列。

4. **启发式检测的边界敏感性**：自动符号检测依赖速度阈值等启发式规则，对于极慢速运动或静止姿态的检测可能不准确，进而影响训练数据的质量。

5. **评估场景的局限性**：当前评估主要集中于步行类等指令明确的动作，对开放式、艺术性或情感性文本的泛化能力尚待检验。

### 推理效率与成本

尽管引入了 LLM 调用，LaMoGen 的整体生成时间仍低于同样使用 LLM 的 CoMo 方法（Table 5），且 LLM 使用的 token 数量更少（Supplementary Table 2）。这表明，通过符号化中间表示压缩信息密度，可以有效控制 LLM 推理开销，为实际部署提供可行性基础。

## 定位与知识库关联

### 1. 与现有文本-运动生成方法的谱系关系

LaMoGen的方法学定位处于**符号化运动生成**与**大语言模型辅助推理**的交汇点，其核心突破在于将传统端到端的文本-运动联合嵌入范式重构为“LLM符号规划 + 运动生成器”的双层次架构。

**与扩散模型基线的关系**：现有主流方法如 **MDM**、**MoDiff** 和 **ReMoDiff** 均采用扩散模型直接从文本条件生成连续运动序列，其瓶颈在于时间结构与多部位协调的隐式编码难以精确对齐细粒度指令。LaMoGen并未完全否定扩散范式——其运动解码器仍基于Transformer重构SMPL姿态——而是将扩散模型的“黑盒映射”角色降级为符号序列到运动的确定性解码，将高层语义组合任务交给LLM完成。这一分工在Laban Benchmark上得到验证：LaMoGen (GPT4.1) 的SMT supL达到0.583，而最优扩散基线MoDiff仅为0.491（Table 1），差距达+0.092。

**与离散标记方法的关系**：**MotionGPT** 和 **CoMo** 同样探索了离散中间表示，但二者仍将文本-运动映射建模为单阶段序列转换。MotionGPT将运动量化为离散token后直接由语言模型生成，CoMo则基于姿态码本进行文本条件生成。LaMoGen的关键差异在于引入了**LabanLite符号体系**——一种帧级、身体部位感知的符号化表示，其每个概念符号关联一个标准化的概念描述，使得LLM可以像处理自然语言一样进行符号推理与组合，而无需接触原始运动数据。这一设计使得LaMoGen在Laban指标上全面超越MotionGPT和CoMo，同时使用的LLM token数量更少（Table 2 Supp）。

**与运动学抽象方法的关系**：早期工作如 **KP**（运动学短语）和 **Guo et al.** 的方法尝试从文本中提取结构化运动原语，但缺乏统一的符号表示框架和LLM驱动的组合推理能力。LaMoGen的LabanLite继承了拉班记谱法的专业严谨性，并通过自动符号检测工作流（在专家标注数据集上获得SMT 0.871、TMP 0.852、HMN 0.786的高准确率，Table 3）实现了从原始运动到符号的可靠转换，为LLM推理提供了可操作的基础。

### 2. 适用边界与能力范围

**强适用场景**：LaMoGen在包含明确**时序结构**（步数、顺序、持续时间）、**重复计数**和**多部位协调**的指令上表现突出。定性结果（Figure 3, Figure 12）显示其能准确执行“前进5步后退3步”等精确指令，而MDM等方法仅生成通用行走循环。Laban指标（SMT、TMP、HMN）专门评估方向对齐、时间对齐和协调性，LaMoGen在这些维度上具有显著优势。

**弱适用场景与已知局限**：
- **低层运动变化**：LabanLite的高层抽象将不同速度的相同语义动作编码为同一符号，导致在标准HumanML3D FID指标上未达到最优（0.252 vs ReMoDiff 0.103）。生成的运动在视觉自然度和细节变化上可能逊于直接建模连续空间的扩散方法。
- **身体部位覆盖**：当前系统主要建模四肢的主要运动，尚未扩展到手部、手指精细动作和面部表情。
- **稀有组合动作**：依赖检索增强提示，若概念描述数据库无法覆盖文本中的稀有或组合动作，LLM可能生成不符合预期的符号计划；LLM本身存在幻觉风险。
- **动作类型泛化**：评估主要限于步行类等指令明确的动作，对更复杂、开放式或艺术性文本（如舞蹈编排）的泛化能力尚待检验。

### 3. 局限性的深层分析

**抽象层次与视觉质量的权衡**：LabanLite的设计哲学是“语义保真优先”，这导致其将不同低层变化（如快走与慢走）映射到同一概念符号。消融实验（Table 6 Supp）表明，在标准MDM基线上引入符号条件可将FID降低约20倍，验证了符号表示的有效性，但也暗示当前符号体系尚未编码速度、风格等连续属性。这一权衡是方法设计的主动选择，而非技术缺陷。

**LLM依赖的双刃剑**：LLM符号规划组件对Laban指标贡献巨大——移除LLM（“None”配置）导致SMT和TMP显著下降，且更强的LLM（如GPT4.1）持续提升性能（Table 1, Table 6）。然而，这引入了推理成本和延迟，尽管整体生成时间仍低于使用LLM的CoMo方法（Table 5）。在实时交互场景中，LLM调用的延迟可能成为瓶颈。

**符号检测的鲁棒性**：自动符号检测工作流依赖启发式阈值（如速度阈值），可能在非常慢的运动或非标准动作类型上检测不准。当前验证仅在专家标注的步行类数据集上进行，更广泛动作类型的检测准确率需要进一步验证。

### 4. 开放问题与未来方向

1. **符号粒度的扩展**：如何扩展LabanLite以同时编码低层运动变化（如速度、风格、力度），从而兼顾语义对齐和视觉自然度？这可能需要引入连续值字段或分层符号结构。

2. **细粒度骨骼覆盖**：如何将方法应用到手指、脚趾等更细粒度的骨骼，以及面部表情？这需要扩展身体部位分组和符号类别体系。

3. **长文本与连贯性**：若输入超长文本（如完整舞蹈剧本），LLM分段处理是否会导致片段间过渡不自然？可能需要引入全局规划与局部细化相结合的策略。

4. **运动风格解耦**：拉班记谱框架能否用于运动风格迁移——将运动内容（做什么）与个人风格（怎么做）解耦？概念符号天然适合表示内容，细节符号可能承载风格信息。

5. **LLM效率优化**：如何降低LLM调用的成本和延迟，使其适用于实时交互场景？可能的路径包括缓存常见符号计划、使用更小的微调模型替代通用LLM。

6. **用户交互与编辑**：能否为符号序列编辑设计直观的用户界面，并集成到Blender等3D创作工具中？当前系统已展示对话式编辑能力（Section 5.2.1, Figure 13），但交互范式的成熟度仍需提升。

7. **评估体系的完善**：Laban Benchmark填补了现有文本-运动评估对细粒度指令覆盖不足的问题，但其指标（基于最长公共子序列）是否完全捕捉了人类对运动语义的判断，仍需用户研究验证。

## 原文 PDF

![[paperPDFs/CVPR_2026/LaMoGen_Language_to_Motion_Generation_Through_LLM_Guided_Symbolic_Inference.pdf]]
