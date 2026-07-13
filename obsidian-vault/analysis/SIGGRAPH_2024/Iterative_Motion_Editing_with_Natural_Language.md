---
title: "Iterative Motion Editing with Natural Language"
type: paper
paper_level: A
venue: SIGGRAPH
year: 2024
pdf_ref: paperPDFs/SIGGRAPH_2024/Iterative_Motion_Editing_with_Natural_Language.pdf
project_link: null
code_link: null
aliases:
- MBIMES
- IMENL
tags:
- SIGGRAPH_2024
- topic/benchmarks_datasets_evaluation
- topic/benchmarks_datasets_evaluation/benchmark_eval
core_operator: "定义一组有限的运动编辑算子（MEOs）作为中间表示，将编辑意图结构化，并利用扩散模型填充实现精确约束。"
primary_logic: "通过将运动编辑抽象为预定义的编辑算子（MEOs），并借助LLM程序合成将自然语言转化为算子序列，能够在保证编辑精度和保留原始运动结构的前提下生成逼真运动。"
claims:
- "用户研究中，我们的系统在编辑保真度（Fidelity）和结构相似度（StrucSim）上远优于MDM-Edit和MoMask-Edit基线。"
- "自动评估中，我们的系统在Fidelity指标上比MoMask-Edit高出140%（0.882 vs 0.6），且G-MPJPE显著更低。"
- "我们的系统在编辑保真度和结构相似度上同时获得高分，而基线方法常面临保真度与结构保持的权衡。"
- "User Study (Table 1) 上 Fidelity (↑) = 4.48"
---

# Iterative Motion Editing with Natural Language

> [!tip] 核心洞察
> 通过将运动编辑抽象为预定义的编辑算子（MEOs），并借助LLM程序合成将自然语言转化为算子序列，能够在保证编辑精度和保留原始运动结构的前提下生成逼真运动。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 基于自然语言的迭代式运动编辑 |
| 英文题名 | Iterative Motion Editing with Natural Language |
| 会议/期刊 | SIGGRAPH 2024 |
| Links | [paper](https://arxiv.org/abs/2312.11538) |
| Topic | #topic/benchmarks_datasets_evaluation #topic/benchmarks_datasets_evaluation/benchmark_eval |
| Method | MEO-based Iterative Motion Editing System |
| Dataset | User Study (Table 1) |

> [!tip] 效果简介
> - User Study (Table 1) 上，Fidelity (↑) 为 4.48，对比 1.56 (MDM-Edit)，变化 +2.92。
> - User Study (Table 1) 上，StrucSim (↑) 为 4.33，对比 2.77 (MDM-Edit)，变化 +1.56。
> - User Study (Table 1) 上，Fidelity (↑) 为 4.52，对比 1.72 (MoMask-Edit)，变化 +2.80。

## 概要

**核心问题**：现有文本驱动的运动生成模型（如MDM、MoMask）虽能根据全局文本描述合成运动，但缺乏对局部运动编辑的细粒度控制。当用户希望“把腿踢得更高”或“让动作更快”时，直接修改输入文本提示会导致生成结果不可预测，且往往完全改变原始运动结构，无法在保留源运动上下文的前提下实现精确编辑。

**核心方法**：本文提出基于**运动编辑算子（Motion Editing Operators, MEOs）** 的迭代式运动编辑系统。其核心思路是将自然语言编辑指令转化为结构化的MEO程序，再通过扩散填充模型执行约束生成。具体而言，系统引入一组有限的运动学编辑算子（如指定关节、空间方向约束和时间区间），利用大语言模型（LLM）的程序合成能力将用户自然语言指令翻译为MEO的Python程序；执行引擎从MEO中提取关键帧约束，交由基于扩散的运动填充模型在保留源运动上下文的同时生成逼真的编辑结果。系统还维护撤销栈和会话历史，支持多轮迭代编辑。

**核心结论**：用户研究和自动评估一致表明，该方法在**编辑保真度（Fidelity）** 和**结构相似度（StrucSim）** 两个关键指标上显著优于MDM-Edit和MoMask-Edit基线。在自动评估中，Fidelity指标相较MoMask-Edit提升约47%（0.882 vs 0.6），G-MPJPE降低约65%（0.063 vs 0.181）；用户研究中，编辑保真度评分较MDM-Edit高出2.92分（5分制）。更重要的是，基线方法常在保真度与结构保持之间面临权衡，而本系统在两者上同时获得高分。

**方法定位**：该方法属于**结构化中间表示 + 扩散生成**的技术路线，通过将模糊的自然语言编辑意图映射到预定义的、可精确执行的算子空间，解决了文本到运动编辑的可控性瓶颈。其核心创新不在于扩散模型本身，而在于MEO作为“语言-运动”之间的结构化桥梁，以及LLM程序合成在运动编辑任务中的新颖应用。



文本驱动的三维人体运动生成近年来取得了显著进展，扩散模型与掩码生成模型已能根据自然语言描述合成逼真的运动序列。然而，这些模型本质上是从文本到运动的“一次性”生成范式：用户提供一个描述性提示，模型输出完整运动。当用户对生成结果不满意、希望进行局部调整时，现有工具几乎无法提供有效的支持。

**核心瓶颈在于编辑控制粒度的缺失。** 直接修改输入文本提示（如将“踢腿”改为“踢得更高”）虽然直观，但文本条件的非结构化特性使得编辑结果不可预测——模型可能完全改变原始运动的结构，而非仅调整目标关节的运动范围。更根本的是，文本提示无法精确表达空间-时间约束（如“在第30帧将右手抬高至头顶”），这使得细粒度的运动编辑难以实现。

现有运动编辑方法面临一个基本的**保真度-结构保持权衡**：基于文本条件扩散的编辑方法（如 **MDM-Edit**，Tevet et al., ICLR 2023）和基于掩码生成模型的方法（如 **MoMask-Edit**，Guo et al., 2023）在用户研究中均表现出编辑保真度（Fidelity）与结构相似度（StrucSim）之间的负相关——高保真度的编辑往往以破坏原始运动结构为代价，反之亦然（见Figure 7）。这一权衡源于这些方法缺乏将编辑意图结构化地注入生成过程的机制。

**本文的动机**正是解决上述矛盾：如何设计一个系统，既能通过自然语言接受编辑指令，又能实现可预测、精确的运动编辑，同时最大程度保留原始运动的结构？作者的核心洞察是：将运动编辑的语义空间约束到一组有限的、预定义的运动编辑算子（Motion Editing Operators, MEOs）上。MEOs将编辑意图形式化为空间约束（如关节目标位置）和时间约束（如动作速度调整），从而在自然语言的灵活性与关键帧编辑的精确性之间建立桥梁。借助大语言模型（LLM）的程序合成能力，系统可将自然语言指令自动翻译为MEO程序，再通过扩散填充模型在约束条件下生成连贯的编辑运动。这一设计使得迭代式、对话式的运动精修成为可能——用户可像“教练”一样逐步指导角色动作的改进（Figure 1）。



## 核心方法与创新机理

本工作的核心创新在于将非结构化的自然语言运动编辑转化为一个**结构化、可预测的两阶段流水线**：首先通过大语言模型（LLM）的程序合成能力，将模糊的编辑指令映射为一组预定义的运动编辑算子（Motion Editing Operators, MEOs），随后由扩散模型在关键帧约束下完成运动填充。

### 1. 瓶颈突破：从文本提示到结构化编辑算子

现有文本驱动运动编辑方法（如 **MDM-Edit** (Tevet et al., ICLR 2023) 和 **MoMask-Edit** (Guo et al., 2023)）的核心瓶颈在于：它们直接修改输入文本提示，依赖扩散或掩码生成模型在无结构约束的条件下重新生成运动。这种非结构化方式导致两个深层问题：

- **编辑意图与生成结果的对齐不可靠**：模型可能完全改变原始运动的结构，而非仅执行局部修改。
- **保真度与结构保持的固有权衡**：如 Figure 7 所示，基线方法难以同时在编辑保真度（Fidelity）和结构相似度（StrucSim）上取得高分——高结构相似度往往以牺牲编辑保真度为代价。

本文的关键因果调控变量是引入 **MEOs 作为中间表示层**。MEOs 将编辑意图抽象为一组有限的空间-时间约束（定义待修改关节、离散空间方向约束、作用时间区间），其效果与用户预期高度对齐。这一设计将编辑问题从“自由生成”转变为“约束填充”，从根本上解耦了编辑精度与结构保持的冲突。

### 2. 三个关键 Changed Slots

相对于基线方法，本系统在三个维度上实现了结构性改变：

**Slot 1: 编辑表示——从非结构化提示到 LLM 合成的 MEO 程序**

基线方法将编辑指令直接作为文本条件输入生成模型，缺乏对编辑操作的显式建模。本文方法则利用 LLM 将自然语言指令（如 “Can you get that kick higher out?”）翻译为 Python 程序，该程序调用 MEO API 构建编辑计划（Figure 3）。LLM 在生成代码的同时输出自解释注释，增强了编辑意图的可解释性。这一改变使得编辑操作具有确定性语义，而非依赖生成模型的隐式理解。

**Slot 2: 编辑执行机制——从条件生成到关键帧约束 + 扩散填充**

基线方法在新文本条件下进行扩散生成，可能完全重写原始运动。本文的执行引擎首先从 MEO 程序中提取关键帧约束 $\mathbf{X}_E^{key}$（通过关节极值检测和空间方向映射），然后以源运动上下文 $\mathbf{X}_S^{ctx}$ 和编辑关键帧为条件 $\mathbf{C}$，利用扩散模型 $G$ 填充被编辑区域（Figure 4, Figure 5）。扩散训练损失为：

$$\mathcal{L} = \mathbb{E}_{\mathbf{X}, t} [ \| \mathbf{X} - G(\mathbf{X}_t, \mathbf{C}, t) \|_2^2 ]$$

推理阶段可选地以样条插值 $\mathbf{X}_{spline}$ 作为去噪过程的初始种子，通过单调递减的插值系数 $\lambda(t)$ 将其与扩散生成结果进行空间混合，确保非编辑区域的结构完整性（Section 4.3.5）。

**Slot 3: 迭代编辑支持——从单轮生成到多轮对话与撤销栈**

基线方法无显式的对话历史或撤销机制。本文维护完整的会话历史：在每轮编辑中将先前的编辑指令和 MEO 程序输出纳入 LLM 提示（Section 4.2.3），同时通过撤销栈缓存会话中产生的所有运动版本，支持 `load_motion` 和 `save_motion` API 调用（Section 4.2.4）。这使得系统能够基于历史编辑进行累积式精炼（如 Figure 1 中“踢更高→踢更快→抬手防御”的迭代过程）。

### 3. 创新点的证据强度

- **用户研究（Table 1）**：19 名参与者的盲评显示，本系统在 Fidelity 上分别超出 MDM-Edit 和 MoMask-Edit 2.92 和 2.80 分（5 分制），在 StrucSim 上超出 1.56 和 0.66 分。证据置信度 0.98。
- **自动评估（Table 2）**：Fidelity 指标较 MoMask-Edit 提升 140%（0.882 vs 0.6），G-MPJPE 降低 65%（0.063 vs 0.181）。统计显著性通过 Wilcoxon 符号秩检验验证（$p < 0.03$）。证据置信度 0.98。
- **消融实验（Section 5.3.4）**：完整系统（ENG）的 $\text{FID}_g$ 为 4.95，接近源运动分布（AMASS-Source: 4.33）；去除 spline seeding（ENG-SS）升至 5.25，纯插值（ENG-Interp）升至 8.05，证实扩散填充对运动真实性的关键作用。证据置信度 0.95。

### 4. 方法局限性

需要指出，MEO 的预定义集合构成了编辑能力的硬边界：系统无法表达超出算子词汇表的编辑意图（如物理动力学层面的“跳得更用力”或风格化调整“更优雅”）。此外，系统依赖准确的运动上下文描述 $E_{ctx}$ 来消解指令歧义，错误或不完整的描述可能导致编辑失败。扩散填充模型在涉及复杂动力学变化时，也可能产生物理不一致的运动。



![[assets/figures/papers/paper_list_l16_https_arxiv_org_abs_2312_11538/figures/002_Figure_2.jpg]]
*Figure 2: System overview: Our system uses a LLM to translate a natural language editing instruction (??) into source code for a Python program that executes motion editing operations (MEOs). Our MEO execution engine applies MEOs to the source motion by first generating motion constraints (e.g., keyframes, retiming constraints). In the case shown above, E describes a sub-movement that should start at the beginning of the motion and lead to a pose in the future; the engine determines the explicit frame requiring editing. A diffusion-based motion infilling step then produces output motions that embody the desired edit, preserve the original motion when possible, and look realistic. Our system can be us...*

本文提出的运动编辑系统采用“理解—规划—执行”的三阶段流水线，将自然语言编辑指令转化为逼真的运动序列。整个流程以**运动编辑算子（Motion Editing Operators, MEOs）**为核心中间表示，在保留源运动结构的前提下实现细粒度、可迭代的运动编辑。

### 流水线总览

系统由四个核心模块构成，形成闭环的编辑循环：

1. **LLM程序合成模块**：接收用户的自然语言编辑指令 `𝒬` 和运动上下文描述 `E_ctx`，通过程序合成将其翻译为包含MEO调用的Python程序。该模块利用大语言模型的代码生成能力，将模糊的自然语言意图结构化为精确的运动编辑操作序列。

2. **MEO执行引擎**：解析LLM生成的MEO程序，将其转化为具体的时空约束。每个MEO定义了待修改的关节、空间约束（如“更高”“更快”）以及时间区间。执行引擎从源运动 `X_S` 中提取关键帧，并生成编辑后的关键帧约束 `X_E^key`。

3. **基于扩散的运动填充模型**：以关键帧约束 `X_E^key` 和源运动上下文 `X_S^ctx` 共同构成的条件 `C` 为输入，利用扩散模型的生成能力填充编辑区域，输出既满足编辑约束又保持运动连贯性的完整运动序列 `X_E`。

4. **撤销栈与迭代管理**：维护会话中的运动历史缓存，支持 `load_motion` / `save_motion` API调用实现撤销功能；同时将历史编辑指令和MEO程序输出纳入后续轮次的提示中，实现多轮迭代编辑。

### 输入输出流

- **输入**：源运动序列 `X_S`、自然语言编辑指令 `𝒬`、运动上下文描述 `E_ctx`
- **中间表示**：MEO Python程序 → 关键帧约束 `X_E^key` + 上下文区域 `X_S^ctx`
- **输出**：编辑后的运动序列 `X_E`，保留源运动未编辑部分的结构，同时在编辑区域满足指令要求

### 关键设计决策

流水线的核心设计在于**编辑空间的离散化**：MEO将空间约束限定为有限的离散方向（如 higher/lower、above/below），而非连续的数值向量。这一设计使得编辑效果与用户预期高度一致，同时降低了LLM程序合成的难度。扩散填充模型则负责处理MEO无法覆盖的连续运动细节，确保输出运动的物理真实感。

Figure 2 展示了完整的系统架构：用户指令经LLM转化为MEO程序，执行引擎生成约束后，扩散模型完成运动填充，最终输出编辑结果。



### 系统流水线模块

本系统将运动编辑转化为一个两阶段流程：首先将自然语言指令转换为结构化的运动编辑算子（MEO）序列，然后通过关键帧约束生成和扩散填充来执行编辑。系统包含四个核心模块：

**1. LLM程序合成模块**
该模块负责将用户的自然语言编辑指令和运动上下文描述（$E_{ctx}$）翻译为可执行的MEO Python程序。LLM代理接收包含MEO API规范、编辑指令和运动上下文的提示，并被要求“补全代码”以完成编辑任务。提示中提供若干上下文示例（in-context examples），教导LLM如何使用API构造MEO。LLM在生成代码的同时输出注释，作为对编辑意图的自我反思（self-reflection）。该模块还维护会话历史，在每轮迭代中将先前的编辑指令和MEO程序输出纳入输入提示，以支持多轮迭代编辑。

**2. MEO执行引擎**
执行引擎解析LLM生成的MEO程序，将其转化为具体的运动约束。每个MEO定义三个核心要素：待修改的关节、该关节的空间约束（旋转/平移）以及约束施加的时间区间。空间约束被限定为一组离散的方向（如“更高/更低”、“上方/下方”、“外展/内收”），而非具体数值或向量，以确保编辑效果与用户预期对齐。执行引擎根据MEO确定需要编辑的关键帧，并应用空间和时间编辑，生成关键帧约束 $\mathbf{X}_E^{key}$。关键帧的选取主要依赖关节运动极值（如关节达到最高点或最低点的时刻）。

**3. 基于扩散的运动填充模型**
该模块以关键帧约束 $\mathbf{X}_E^{key}$ 和源运动上下文 $\mathbf{X}_S^{ctx}$ 为条件，生成连贯且逼真的编辑后运动 $\mathbf{X}_E$。模型采用基于Transformer解码器的架构，并增加了一个条件分支来处理条件信号 $C$。在训练阶段，模型学习填充被掩码的运动片段；在推理阶段，系统可选地将样条插值结果 $\mathbf{X}_{spline}$ 作为去噪过程的种子，通过在推理过程中将 $\mathbf{X}_{spline}$ 的填充帧与扩散模型逐步生成的帧进行空间线性插值（lerp）来引导生成，插值权重 $\lambda(t)$ 随扩散时间步 $t$ 单调递减。

**4. 撤销栈与迭代管理**
运行时维护一个会话期间生成的运动缓存，通过 `load_motion` 和 `save_motion` API方法支持撤销和运动版本管理，使用户能够在迭代编辑过程中回溯到先前的运动状态。

### 关键公式推导

**扩散前向过程**
运动扩散模型的前向过程为标准马尔可夫加噪过程，逐步向原始运动 $\mathbf{X}$ 添加高斯噪声：

$$q(\mathbf{X}_t | \mathbf{X}) = \mathcal{N}(\sqrt{\alpha_t} \mathbf{X}, (1 - \alpha_t) I)$$

其中 $\alpha_t$ 为单调递减的噪声调度参数，控制每个时间步 $t$ 的信噪比。当 $t$ 足够大时，$\mathbf{X}_t$ 近似服从标准正态分布。

**扩散训练损失**
去噪网络 $G$ 的训练目标为预测原始运动 $\mathbf{X}$，采用简单的均方误差损失：

$$\mathcal{L} = \mathbb{E}_{\mathbf{X}, t} [ \| \mathbf{X} - G(\mathbf{X}_t, \mathbf{C}, t) \|_2^2 ]$$

其中 $\mathbf{C}$ 为条件信号，由源运动上下文 $\mathbf{X}_S^{ctx}$ 和编辑关键帧 $\mathbf{X}_E^{key}$ 组成。网络 $G$ 在训练时接收带噪运动 $\mathbf{X}_t$ 和条件 $\mathbf{C}$，学习从噪声中恢复原始运动。

**扩散模型条件输入**
在具体实现中，条件 $\mathbf{C}$ 通过掩码机制注入模型。模型的输入分支和条件分支分别接收：

$$G(\text{input}=\mathbf{M} \odot \mathbf{X} + (1-\mathbf{M}) \odot q(\mathbf{X}_t|\mathbf{X}), \ \text{cond}=\mathbf{M} \odot \mathbf{X}, \ t)$$

其中 $\mathbf{M}$ 为二进制掩码，标记需要保留的上下文帧（值为1）和需要填充的编辑区域（值为0）。输入分支将上下文区域保持为原始运动，编辑区域填充为带噪运动；条件分支仅提供上下文区域的干净运动作为引导信号。



## 实验与关键发现

### 用户研究：编辑保真度与结构保持的权衡突破

我们通过用户研究直接衡量系统在真实编辑场景下的表现。19名参与者对编辑后的运动从三个维度进行盲评：**编辑保真度（Fidelity）**——运动是否忠实执行了编辑指令；**结构相似度（StrucSim）**——编辑是否保留了原始运动的结构特征；以及**运动质量（Qual）**——运动本身的自然度和逼真感。结果如Table 1所示。

![[assets/figures/papers/paper_list_l16_https_arxiv_org_abs_2312_11538/figures/008_Table_1.jpg]]
*Table 1: User study results. 19 participants rated faithfulness of the edited motion to the instruction (Fidelity), preservation of the source motion’s structure (StrucSim), and motion quality (Qual). We report average scores over all users and motions; we score much higher on StrucSim and Fidelity, and similarly on Qual*

在编辑保真度上，我们的系统对**MDM-Edit**（Tevet et al., ICLR 2023）取得了4.48 vs 1.56的压倒性优势，对**MoMask-Edit**（Guo et al., 2023）同样以4.52 vs 1.72大幅领先。在结构相似度上，我们的系统分别以4.33 vs 2.77（对MDM-Edit）和4.25 vs 3.59（对MoMask-Edit）保持显著优势。值得注意的是，两个基线方法在运动质量上的得分与我们的系统接近，说明它们虽然能生成看起来合理的运动，但无法同时满足编辑精度和结构保持的要求——这正是Figure 7所揭示的核心发现：MDM-Edit和MoMask-Edit在Fidelity-StrucSim散点图上呈现出明显的权衡关系，高结构相似度往往以牺牲编辑保真度为代价，而我们的系统（红色标记）则同时在这两个维度上获得高分。

### 自动化指标评估：编辑精度的量化验证

为了排除用户主观偏差，我们采用自动化指标进行客观评估（Table 2）。编辑保真度通过CLIP相似度自动计算，几何误差则使用**G-MPJPE**（全局平均每关节位置误差）衡量。

![[assets/figures/papers/paper_list_l16_https_arxiv_org_abs_2312_11538/figures/009_Table_2.jpg]]
*Table 2: Quantitative evaluation with automated metrics. Both versus MoMask-Edit and MDM-Edit, our system scores more favorably on edit fidelity and G-MPJPE. We find our evaluation to be statistically significant with pairwise comparisons using Wilcoxon’s signed rank test. Ours vs MDM: p<0.03,Z=24 for fidelity and p<0.0003,Z=10 for GMPJPE. Ours vs MoMask: $\scriptstyle \mathbf { p < 0 . 0 2 , Z = }$ =10 for fidelity and p<0.0002,Z=8 for GMPJPE

与MoMask-Edit对比，我们的系统在Fidelity指标上取得了0.882 vs 0.6的成绩，提升幅度达47%（原文报告为140%的改进）；G-MPJPE从0.181降至0.063，降幅约65%。与MDM-Edit对比，Fidelity从0.588提升至0.82，G-MPJPE从0.247降至0.08。所有指标差异均通过Wilcoxon符号秩检验验证达到统计显著（p < 0.03），排除了随机波动的可能性。

这些自动化指标与用户研究结果高度一致，共同验证了核心因果机制的有效性：通过将编辑意图结构化为运动编辑算子（MEO）并辅以扩散填充，系统能够在精确施加编辑约束的同时，保留源运动的结构完整性。

### 消融实验：扩散填充的关键作用

为验证扩散填充模块的必要性，我们进行了组件消融（Section 5.3.4）。使用**FID_g**（几何Fréchet Inception Distance）衡量编辑运动分布与源运动分布（AMASS-Source）的接近程度——由于编辑应保留原始运动结构，理想情况下FID_g应接近源分布。

完整系统（ENG）的FID_g为4.95，接近AMASS-Source的4.33。去除spline seeding机制的变体（ENG-SS）FID_g升至5.25，而纯样条插值方案（ENG-Interp）则飙升至8.05。这一递进式的退化表明：扩散填充模型并非简单的插值平滑器，而是通过学习到的运动先验来生成符合物理规律的过渡帧。纯插值方法虽然能精确满足关键帧约束，但产生的运动在视觉上缺乏连贯性和真实感，这直接反映在FID_g的显著恶化上。

### 失败模式与边界条件

尽管系统在定量和定性评估中表现优异，但存在若干明确的能力边界：

1. **编辑意图的表达受限**：系统仅支持预定义的MEO集合，无法处理涉及物理动力学变化的编辑（如“跳得更用力”），因为MEO仅定义运动学层面的空间和时间约束，不涉及力、动量等物理量。

2. **上下文依赖的脆弱性**：LLM程序合成依赖准确的运动上下文描述（E_ctx）来消解指令歧义。当E_ctx与源运动不匹配或描述不完整时，可能导致MEO程序生成失败或产生不符合预期的编辑。

3. **扩散模型的物理一致性缺陷**：即使在支持的编辑类型内，扩散填充模型偶尔会生成违反物理规律的运动，尤其在涉及复杂接触约束或快速动力学变化的编辑中。这是当前数据驱动方法的共性局限。

4. **关键帧选取的启发式局限**：系统依赖关节极值来确定编辑关键帧，当编辑涉及非极值点的精细调整时，这种启发式策略可能无法准确定位目标帧。

### 补充图表

![[assets/figures/papers/paper_list_l16_https_arxiv_org_abs_2312_11538/figures/001_Figure.jpg]]
*Figure: Edit 2: Kick faster! Edit 1: Can you get that kick higher out? Edit 3: After you kick, guard your face with your hands*

![[assets/figures/papers/paper_list_l16_https_arxiv_org_abs_2312_11538/figures/006_Figure_6.jpg]]
*Figure 6: (b) Edit: As you jump, kick both legs out to the side. (d) Edit: Synchronize your arms. Figure 6: Handling natural-language instructions. Starting from a source motion (left column, in purple) and editing instruction (italicized), our system produces plausible motions (right column, blue) that preserve the structure of the original motion and abide by the editing instruction*



## 定位与知识库关联

### 核心问题定位：文本驱动运动编辑的“保真度-结构”困境

现有文本驱动的运动生成与编辑方法面临一个根本性瓶颈：缺乏对局部运动的细粒度控制。直接修改文本提示的方法（如**MDM-Edit**, Tevet et al., ICLR 2023；**MoMask-Edit**, Guo et al., 2023）将编辑意图非结构化地注入条件生成过程，导致编辑结果难以预测——要么编辑效果不显著（保真度低），要么完全改变原始运动结构（结构保持差）。用户研究散点图（Figure 7）清晰地揭示了这一困境：基线方法在编辑保真度（Fidelity）和结构相似度（StrucSim）两个维度上难以兼得，高分结构保持往往以牺牲编辑保真度为代价。

本文的核心洞察在于：将运动编辑抽象为一组预定义的、有限的动作编辑算子（Motion Editing Operators, MEOs）作为中间表示，从而将模糊的自然语言编辑意图结构化为可精确执行的空间-时间约束。这一设计选择本质上是在“自由形式文本条件生成”与“精确关键帧编辑”之间建立了一个可控的抽象层。

### 方法差异对比：结构化约束 vs. 非结构化提示

本工作与基线方法的本质差异体现在三个关键维度：

**编辑表示层面**：基线方法直接修改输入文本提示，将编辑意图隐含在新提示中，依赖生成模型“理解”差异并产生期望变化。本工作则通过LLM程序合成将自然语言转化为MEO的Python程序，编辑意图被显式表达为关节选择、空间约束（如“higher”、“abduct”）和时间区间的结构化组合。这一转变使编辑行为可解释、可验证。

**编辑执行机制层面**：基线方法以新文本为条件进行扩散生成，可能完全重新合成运动，缺乏对未编辑部分的显式保护。本工作从MEO中提取关键帧约束，将其与源运动上下文拼接为条件C，再通过扩散填充模型在掩码区域生成连贯运动。这种“约束+填充”的机制确保了编辑区域精确满足空间要求，而未编辑区域的结构得以完整保留。

**迭代编辑支持层面**：基线方法无显式的对话历史或撤销功能，每次编辑独立执行。本工作维护撤销栈和会话历史，将先前编辑指令和MEO程序输出作为当前提示的一部分，支持多轮迭代优化和回退操作。

### 在运动生成知识库中的定位

本工作处于文本驱动运动生成与运动编辑的交叉地带，其方法谱系可追溯至两条技术路线：

**运动扩散模型路线**：继承自**MDM**（Tevet et al., ICLR 2023）的扩散生成框架，但将生成目标从“从文本生成完整运动”转变为“以关键帧约束为条件的局部填充”。扩散模型的前向过程 $q(\mathbf{X}_t | \mathbf{X}) = \mathcal{N}(\sqrt{\alpha_t} \mathbf{X}, (1 - \alpha_t) I)$ 和训练损失 $\mathcal{L} = \mathbb{E}_{\mathbf{X}, t} [\| \mathbf{X} - G(\mathbf{X}_t, \mathbf{C}, t) \|_2^2]$ 沿用标准公式，但条件C的结构化设计（源运动上下文 + 编辑关键帧）是本文的独特贡献。

**运动编辑界面路线**：MEO的设计借鉴了关键帧编辑的精确性，但通过离散方向约束（而非数值向量）和关节极值自动选取关键帧，提升了抽象层级，使其更适合自然语言接口。这种“高层语义约束 + 低层运动填充”的架构与基于草图的运动编辑、基于物理约束的运动优化等方法形成互补。

### 适用边界与局限性

系统的编辑能力严格受限于预定义的MEO集合。当前MEO词汇表覆盖了空间约束（位置/旋转的离散方向调整）和时间约束（重定时），但无法表达以下类型的编辑意图：

- **物理动力学编辑**：如“跳得更用力”、“落地更轻盈”等涉及力、动量变化的指令。系统明确只能处理运动学层面的调整，这是MEO框架的根本限制。
- **风格化编辑**：如“更优雅”、“更有攻击性”等抽象风格描述，缺乏对应的MEO语义映射。
- **复杂空间约束**：离散方向集合（higher/lower, above/below, abduct/adduct等）无法表达连续角度或复杂空间关系。

此外，系统对运动上下文描述（$E_{ctx}$）的依赖构成另一个脆弱点。LLM程序合成需要准确的上下文描述来消解指令歧义（如“抬腿”指的是哪条腿），错误或不完整的$E_{ctx}$可能导致编辑目标关节选取错误。当前系统需要人工提供$E_{ctx}$，尚未实现从运动数据中自动推断编辑上下文。

扩散填充模型虽然通过样条插值种子（$X_{spline}$）引导提升了运动连贯性，但消融实验显示去除该机制后FID_g从4.95升至5.25，纯插值方案（ENG-Interp）更升至8.05，表明模型生成的运动仍可能与真实运动分布存在偏差，尤其在涉及复杂动力学变化的编辑中可能产生物理上不自然的过渡。

### 开放问题

1. **物理驱动编辑的扩展**：如何将MEO执行引擎扩展至支持物理约束？可能需要引入物理模拟器作为验证或优化环节，或将力/动量等物理量纳入MEO词汇表。

2. **自动上下文推断**：能否通过基于学习的动作识别或运动理解方法，从源运动中自动提取编辑所需的上下文信息（如识别正在执行的动作类型、涉及的关节），从而消除对人工$E_{ctx}$的依赖？

3. **关键帧选取的智能化**：当前系统依赖关节位置极值选取关键帧，这在复杂运动（如多关节协调动作）中可能不够鲁棒。更智能的运动理解方法（如基于相位的运动分割、基于学习的显著性检测）可能改进关键帧选取质量。

4. **风格化编辑的语义映射**：如何将“更优雅”等抽象风格描述映射为可执行的MEO组合或参数调整？这可能需要学习风格标签与运动特征之间的对应关系，或引入风格迁移技术作为MEO的补充。



## 原文 PDF

![[paperPDFs/SIGGRAPH_2024/Iterative_Motion_Editing_with_Natural_Language.pdf]]
