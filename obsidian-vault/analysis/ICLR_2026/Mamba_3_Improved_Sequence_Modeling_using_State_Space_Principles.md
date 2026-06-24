---
title: "Mamba-3: Improved Sequence Modeling using State Space Principles"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Mamba_3_Improved_Sequence_Modeling_using_State_Space_Principles.pdf
openreview_forum_id: HwCvaJOiCj
aliases:
- M3
- Mamba-3
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/segmentation
core_operator: "采用指数梯形离散化（二阶精度）、复数值状态更新（实现数据依赖的旋转动态）以及多输入多输出（MIMO）结构，从状态空间原理出发系统性地提升模型的表达能力和推理硬件效率。"
primary_logic: "从状态空间模型的连续-离散理论出发，通过指数梯形离散化和复数值状态，可以在不增加推理开销的情况下显著提升序列建模能力；进一步通过MIMO结构提高解码算术强度，实现相同推理延迟下更强的模型性能。"
claims:
- "Mamba-3 (MIMO) 在1.5B参数规模上，平均下游语言理解准确率比Gated DeltaNet高1.8个百分点，比Mamba-2高1.9个百分点。"
- "Mamba-3 (MIMO) 在使用一半状态大小（state size 64）的情况下即可匹配 Mamba-2 使用 128 状态大小时的预训练困惑度。"
- "Mamba-3 能够解决 Mamba-2 无法处理的合成状态跟踪任务（奇偶校验、模运算），准确率分别达 100% 和 98.51%。"
- "指数梯形离散化与BC偏差的组合使得短因果卷积成为可选，同时模型性能不降反升。"
---

# Mamba-3: Improved Sequence Modeling using State Space Principles

> [!tip] 核心洞察
> 从状态空间模型的连续-离散理论出发，通过指数梯形离散化和复数值状态，可以在不增加推理开销的情况下显著提升序列建模能力；进一步通过MIMO结构提高解码算术强度，实现相同推理延迟下更强的模型性能。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Mamba-3：基于状态空间原理的改进序列建模 |
| 英文题名 | Mamba-3: Improved Sequence Modeling using State Space Principles |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=HwCvaJOiCj) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/segmentation |
| Method | Mamba-3 |
| Dataset | Downstream language tasks (LAMBADA, HellaSwag, PIQA, Arc-Easy/Challenge, WinoGrande, OpenBookQA), Downstream language tasks (同上), Synthetic state tracking (Parity, Modular Arithmetic), FineWeb-Edu validation perplexity |

> [!tip] 效果简介
> - Downstream language tasks (LAMBADA, HellaSwag, PIQA, Arc-Easy/Challenge, WinoGr... 上，Average accuracy 为 Mamba-3 SISO (1.5B) 56.4，对比 Mamba-2 (1.5B) 55.7，变化 +0.7。
> - Downstream language tasks (同上) 上，Average accuracy 为 Mamba-3 MIMO (1.5B) 57.6，对比 Mamba-2 (1.5B) 55.7，变化 +1.9。
> - Synthetic state tracking (Parity, Modular Arithmetic) 上，Scaled accuracy (%) 为 Mamba-3: Parity 100%, Arith. w/o brackets 98.51%，对比 Mamba-2: 接近随机猜测，变化 显著提升。

## 概述

序列模型在处理长程依赖时始终面临表达性与效率的权衡。Transformer 的注意力机制计算复杂度随序列长度平方增长，而以 Mamba-2 为代表的线性序列模型虽在推理效率上具有优势，却在状态跟踪任务上暴露了结构性缺陷——其解码阶段算术强度低，导致硬件利用率不足，难以在实际推理中高效扩展。

Mamba-3 从状态空间模型的连续-离散理论出发，用三项系统性的改进回应上述瓶颈：

1. **指数梯形离散化**：将 Mamba-2 的一阶指数欧拉离散化推广为二阶指数梯形格式，在理论上有可证明的误差界，在实践上等价于在状态输入上施加数据依赖的短卷积。
2. **复值状态空间**：将状态转移从实值标量对角阵扩展为复值旋转块，等效为数据依赖的旋转位置嵌入（RoPE），使模型获得状态跟踪能力。
3. **多输入多输出（MIMO）结构**：将单输入单输出的外积式状态更新替换为矩阵乘法式更新，在不增加状态维度的前提下线性提升解码算术强度。

在 100B FineWeb-Edu 令牌上训练的 1.5B 参数规模下，Mamba-3 MIMO 的平均下游语言理解准确率比 Mamba-2 高 1.9 个百分点，比 Gated DeltaNet 高 1.8 个百分点。更重要的是，Mamba-3 MIMO 在使用一半状态大小（64 vs 128）时即可匹配 Mamba-2 的预训练困惑度，意味着在相同推理延迟下可部署更强的模型。在合成状态跟踪任务上，Mamba-3 在奇偶校验和模运算中分别达到 100% 和 98.51% 的准确率，而 Mamba-2 接近随机猜测。

方法层面，Mamba-3 在 Mamba-2 架构的基础上修改了六个关键插槽：离散化方法、状态空间类型、输入/输出结构、短因果卷积的可选性、B/C 投影后归一化（BCNorm）以及 B/C 偏置。消融实验表明，BC 偏置与指数梯形离散化的组合使得原本普遍使用的短因果卷积变为可选，同时模型性能不降反升。

## 背景与动机

### 序列建模中的状态跟踪瓶颈

现代序列建模的核心挑战之一在于，模型不仅需要捕捉局部模式，还必须具备在长序列中持续跟踪和更新内部状态的能力。Transformer 架构通过自注意力机制天然具备这种能力，但其计算复杂度随序列长度呈二次增长，导致推理成本高昂。为突破这一瓶颈，以 Mamba 系列为代表的线性状态空间模型（SSM）应运而生，通过将状态转移参数化为一阶递归，实现了训练时的并行化和推理时的恒定时间复杂度。

然而，现有线性 SSM 存在一个关键的性能缺口：**状态跟踪能力不足**。以 Mamba-2（Dao & Gu, 2024）为例，其状态转移被简化为标量对角形式：

$$h_t = \alpha_t h_{t-1} + \gamma_t B_t x_t, \quad y_t = C_t^\top h_t$$

这种简化虽然保证了计算效率，却严重限制了模型对序列中离散状态的记忆和操作能力。在需要精确状态跟踪的合成任务（如奇偶校验、模运算）上，Mamba-2 的表现接近随机猜测，暴露出其动态系统表达能力的根本性局限。

### 推理效率的硬件瓶颈

除表达能力外，现有线性 SSM 在推理阶段还面临**硬件利用率低下**的问题。Mamba-2 采用单输入单输出（SISO）结构，其状态更新本质上是外积运算，导致解码过程的算术强度（Arithmetic Intensity）偏低。在内存带宽受限的硬件上，低算术强度意味着计算单元大量时间处于等待数据的状态，无法充分利用 GPU 的算力资源。这使得模型在保持相同推理延迟的情况下，难以通过增大状态维度来换取性能提升——状态越大，解码越慢，性能-效率的帕累托前沿被严重约束。

### 连续-离散理论视角的缺失

更根本地，现有方法在离散化策略上多采用启发式的一阶指数欧拉方法，缺乏对连续时间 SSM 理论的系统性利用。连续时间 SSM 的标准形式为：

$$\dot{h}(t) = A(t) h(t) + B(t) x(t)$$

其离散化精度直接影响递归模型对连续动态的逼近质量。一阶欧拉离散化仅使用当前时间步的端点值，本质上丢弃了区间内的动态信息。从数值积分的角度看，这等价于用矩形近似梯形——精度受限且缺乏可证明的误差界。这一理论层面的妥协，是导致现有模型状态跟踪能力薄弱的深层原因。

### 本文动机

基于以上分析，Mamba-3 从三个相互关联的维度出发，系统性地改进序列建模：

1. **离散化精度**：引入指数梯形离散化（二阶精度），通过同时利用当前和前一时间步的输入信息，在不增加推理开销的前提下提升递归的表达能力。
2. **状态空间结构**：将实值标量状态扩展为复值状态空间，等价于实现数据依赖的旋转位置嵌入（RoPE），使模型天然具备状态跟踪所需的旋转动态。
3. **输入输出架构**：引入多输入多输出（MIMO）结构，将外积状态更新转换为矩阵乘法，在相同状态大小下提高解码算术强度，从而在不牺牲推理速度的情况下获得更强的建模性能。

这三个改进共同指向一个核心目标：**在不增加推理开销的约束下，通过状态空间原理的系统性应用，显著提升线性序列模型的表达能力和硬件效率**。

## 核心创新

Mamba-3 的核心创新并非引入全新的架构范式，而是从状态空间模型的连续-离散理论出发，对 Mamba-2 的三个关键环节进行系统性升级，形成一组相互增强的改动槽位（changed slots）。

### 1. 离散化：从指数欧拉到指数梯形

Mamba-2 采用的离散化方法本质上是**指数欧拉法**（exponential-Euler），这是一阶方法，局部截断误差为 $O(\Delta_t^2)$。Mamba-3 将其替换为**指数梯形离散化**（exponential-trapezoidal discretization），这是一种二阶方法，局部截断误差 $O(\Delta_t^3)$，全局误差 $O(\Delta_t^2)$（Proposition 1, Remark 3）。

指数梯形离散化带来的关键变化是状态更新中引入了**前一时间步的输入项**：

$$h_t = \alpha_t h_{t-1} + \beta_t B_{t-1} x_{t-1} + \gamma_t B_t x_t$$

其中 $\alpha_t = e^{\Delta_t A_t}$，$\beta_t = (1 - \lambda_t) \Delta_t e^{\Delta_t A_t}$，$\gamma_t = \lambda_t \Delta_t$。当 $\lambda_t = 1$ 时退化为 Mamba-2 的欧拉法；当 $\lambda_t = 1/2$ 时退化为经典梯形法则（Remark 2）。实际训练中 $\lambda_t$ 由数据驱动学习，且不强制满足 $\lambda_t = 1/2 + O(\Delta_t)$ 的理论约束时性能最优。

这一改动的影响远不止精度提升：指数梯形离散化等效于在状态输入上施加了一个**数据依赖的卷积核大小为 2 的因果卷积**，这使得 Mamba-2 中普遍使用的短因果卷积（kernel size 4）变得可选。消融实验证实，BC 偏置与指数梯形离散化的组合使得移除短卷积后模型性能不降反升（Table 3a, Section 4.2）。

### 2. 状态空间：从实值标量转移到复值旋转动态

Mamba-2 的状态转移矩阵为实值对角阵，本质上只执行标量衰减。Mamba-3 将状态空间扩展为**复值 SSM**（Proposition 2）：

$$\dot{\pmb{h}}(t) = \mathrm{Diag}(\boldsymbol{A}(t) + i\pmb{\theta}(t))\pmb{h}(t) + (\pmb{B}(t) + i\pmb{\hat{B}}(t))\boldsymbol{x}(t)$$

这一扩展在离散化后等价于一个实值 SSM，其状态转移矩阵变为 **2×2 块对角旋转矩阵** $R_t$（Proposition 2）。进一步通过数学变换（Proposition 3），复值递归可转化为对 B 和 C 投影施加**数据依赖的旋转位置编码**（RoPE trick）：

$$h_t = e^{\Delta_t A_t} h_{t-1} + \left( \prod_{i=0}^t R_i^\top \right) B_t x_t, \quad y_t = \left[ \left( \prod_{i=0}^t R_i^\top \right) C_t \right]^\top h_t$$

这一改动直接解决了 Mamba-2 在状态跟踪任务上的根本弱点。在合成状态跟踪任务上，Mamba-3 的奇偶校验准确率达 100%，模运算准确率达 98.51%，而 Mamba-2 接近随机猜测（Table 3b）。

### 3. 输入/输出结构：从 SISO 到 MIMO

Mamba-2 采用单输入单输出（SISO）结构，其解码阶段的算术强度（arithmetic intensity）约为 2.5 ops/byte（Table 7a），属于内存受限操作，硬件利用率低。Mamba-3 引入**多输入多输出（MIMO）**结构，将状态更新从外积形式切换为矩阵乘法形式（Section 3.3, Appendix D），使算术强度随秩 $R$ 线性增长（Table 7b），在相同推理延迟下获得更强的建模能力。

实际部署中 MIMO 使用秩 $R=4$，并通过缩减 MLP 隐藏维度来匹配 SISO 变体的总参数量（MIMO Parameter Matching table），确保比较公平。实验表明，MIMO 变体在 1.5B 规模上平均下游准确率比 SISO 再提升 1.2 个百分点（Table 1），且使用**一半状态大小**（state size 64）即可匹配 Mamba-2 使用 128 状态大小时的预训练困惑度（Figure 2）。

### 4. 辅助改动：BCNorm 与 BC 偏置

除上述三个核心槽位外，Mamba-3 还引入了两个辅助改动：

- **BCNorm**：在 B、C 投影后添加 RMS 归一化，类似 Transformer 中的 QKNorm，用于稳定训练。
- **BC 偏置**：在 BCNorm 之后添加可学习的、按头、按通道的偏置，初始化为 1。消融表明同时为 B 和 C 添加偏置带来最佳困惑度（ppl 15.69），而仅添加 B 偏置无益甚至有害（Table 9b）。

这些改动共同构成了 Mamba-3 相对于 Mamba-2 的完整创新谱系，其核心洞察在于：**从 SSM 的连续-离散理论出发，通过更高阶的离散化和更丰富的状态空间，可以在不增加推理开销的前提下显著提升序列建模能力**。

## 整体框架

Mamba-3 延续了 Mamba-2 的宏观架构骨架，但在核心的序列混合器（sequence mixer）层面进行了系统性重构。其整体 pipeline 由六个串行模块构成，输入输出流与标准 Transformer 解码器层完全兼容。

### 输入投影与门控分支

给定层输入 $\mathbf{u} \in \mathbb{R}^{L \times d}$（$L$ 为序列长度，$d$ 为模型维度），首先通过一个线性投影层同时生成四个分支：

- **B 投影**：生成状态输入矩阵 $\mathbf{B} \in \mathbb{R}^{L \times H \times N}$，其中 $H$ 为注意力头数，$N$ 为状态维度。
- **C 投影**：生成状态输出矩阵 $\mathbf{C} \in \mathbb{R}^{L \times H \times N}$。
- **X 投影**：生成标量输入序列 $\mathbf{x} \in \mathbb{R}^{L \times H}$。
- **门控 Z 投影**：生成门控信号 $\mathbf{z} \in \mathbb{R}^{L \times H}$。

这一投影结构直接继承自 Mamba-2 的 SSD 层设计，但 Mamba-3 在投影后引入了两个关键的正则化操作。

### BCNorm 与 BC 偏置

在 B 和 C 投影之后，Mamba-3 插入 **RMSNorm**（称为 BCNorm），这一设计直接对应 Transformer 中广泛使用的 QKNorm 策略，用于稳定训练过程中的梯度传播。

归一化之后，Mamba-3 进一步为 B 和 C 添加**可学习的、按头、按通道的偏置**参数。这些偏置初始化为 1，与指数梯形离散化协同作用，使得原本在 Mamba-2 中必需的短因果卷积（kernel size=4）变为可选组件。消融实验（Table 3a）表明，同时为 B 和 C 添加偏置可获得最佳预训练困惑度（15.69），而仅添加 B 偏置则无益甚至有害（Table 9b）。

### 复值指数梯形 SSM 核心

Mamba-3 的序列混合核心是**复值指数梯形状态空间模型**，其完整递归由 Proposition 4 给出：

$$
\pmb{h}_t = \alpha_t \pmb{h}_{t-1} + \beta_t \left( \prod_{i=0}^{t-1} \pmb{R}_i^\top \right) \pmb{B}_{t-1} x_{t-1} + \gamma_t \left( \prod_{i=0}^{t} \pmb{R}_i^\top \right) \pmb{B}_t x_t
$$

$$
y_t = \left[ \left( \prod_{i=0}^{t} R_i^\top \right) C_t \right]^\top h_t
$$

该递归融合了两项核心创新：

1. **指数梯形离散化**（Section 3.1）：将状态-输入积分的近似从 Mamba-2 的一阶指数欧拉方法提升为二阶指数梯形方法，引入数据依赖的插值系数 $\lambda_t$，使得当前时间步的状态更新同时依赖于当前输入 $\mathbf{B}_t x_t$ 和上一时间步的输入 $\mathbf{B}_{t-1} x_{t-1}$。这等价于在状态输入上施加了一个数据依赖的、大小为 2 的因果卷积（Figure 1 左图展示了由此产生的结构化掩码）。

2. **复值状态空间**（Section 3.2）：将 SSM 的状态转移矩阵从实值标量（Mamba-2 的对角线单位阵）推广为复值对角矩阵。通过 Proposition 2 的复-实等价变换，这等效为在状态转移中引入块对角旋转矩阵 $\mathbf{R}_t$。进一步通过 Proposition 3 的“RoPE trick”，这些旋转矩阵可以被等价地吸收到 B 和 C 投影上，形成**数据依赖的旋转位置嵌入（data-dependent RoPE）**。这一设计使得模型天然具备状态跟踪能力——Table 3b 显示 Mamba-3 在奇偶校验任务上准确率达 100%，在无括号模运算上达 98.51%，而 Mamba-2 在此类任务上接近随机猜测。

### 门控与输出投影

SSM 输出 $y_t$ 与门控信号 $\mathbf{z}_t$ 通过 SiLU 激活函数进行逐元素乘法（门控机制），随后通过线性输出投影映射回模型维度 $d$，与残差连接相加后完成整个层的计算。

### MIMO 可选扩展

Mamba-3 默认采用单输入单输出（SISO）结构以与 Mamba-2 等基线公平对比，但提供了多输入多输出（MIMO）变体（秩 $R=4$）。MIMO 将状态更新从外积形式切换为矩阵乘法形式：

$$
H_t = a_t H_{t-1} + B_t X_t^\top, \quad Y_t = H_t^\top C_t
$$

这一改变将解码阶段的算术强度从约 2.5 ops/byte 线性提升至 $R$ 倍（Table 7），在相同推理延迟下显著改善硬件利用率。为保持总参数量可比，MIMO 变体通过缩减 MLP 隐藏维度进行参数匹配（见 MIMO Parameter Matching 表）。Figure 2 显示，MIMO 在使用状态大小 64 时即可匹配 Mamba-2 使用状态大小 128 的预训练困惑度，整体帕累托前沿显著前移。

### 与 Mamba-2 的架构差异总结

Figure 3 给出了 Mamba-2 与 Mamba-3 的架构对比。核心差异可归纳为五个“槽位”变更：离散化方法从指数欧拉升级为指数梯形、状态空间从实值标量升级为复值旋转、输入输出结构增加 MIMO 选项、短因果卷积变为可选、以及新增 BCNorm 与 BC 偏置。这些变更系统性地提升了模型的表达能力与推理效率，而无需对训练流程或推理管线进行根本性改造。

## 核心模块与公式推导

Mamba-3 的架构改进根植于状态空间模型的连续-离散理论，其核心模块围绕三个关键创新展开：指数梯形离散化、复值状态空间和 MIMO 结构。以下按模块逐一推导关键公式。

### 连续时间 SSM 基础

Mamba-3 的起点是线性时变状态空间模型，其连续时间动力学方程为：

$$\dot{\pmb{h}}(t) = \pmb{A}(t) \pmb{h}(t) + \pmb{B}(t) \pmb{x}(t)$$

$$y(t) = C(t)^\top h(t)$$

其中 $\pmb{h}(t)$ 是状态向量，$\pmb{x}(t)$ 是输入，$\pmb{A}(t)$ 为状态转移矩阵，$\pmb{B}(t)$ 和 $\pmb{C}(t)$ 为输入和输出投影矩阵。Mamba-2 采用指数欧拉离散化，得到标量状态转移的简化递归：

$$\pmb{h}_t = \alpha_t \pmb{h}_{t-1} + \gamma_t \pmb{B}_t \pmb{x}_t, \quad y_t = \pmb{C}_t^\top \pmb{h}_t$$

这是 Mamba-3 改进的基线形式。

### 模块一：指数梯形离散化

Mamba-2 的指数欧拉离散化仅为一阶精度，且只使用当前时间步的输入。Mamba-3 引入广义指数梯形规则，将状态更新扩展为同时依赖当前和前一时间步的输入。

**命题 1（广义梯形递归）**：对状态-输入积分应用广义梯形规则，得到二阶精度的离散递归：

$$h_t = e^{\Delta_t A_t} h_{t-1} + (1 - \lambda_t) \Delta_t e^{\Delta_t A_t} B_{t-1} x_{t-1} + \lambda_t \Delta_t B_t x_t$$

紧凑形式为：

$$h_t = \alpha_t \pmb{h}_{t-1} + \beta_t \pmb{B}_{t-1} x_{t-1} + \gamma_t \pmb{B}_t x_t$$

其中系数定义为：

$$\alpha_t := e^{\Delta_t A_t}, \quad \beta_t := (1 - \lambda_t) \Delta_t e^{\Delta_t A_t}, \quad \gamma_t := \lambda_t \Delta_t$$

$\Delta_t$ 为时间步长，$\lambda_t \in [0,1]$ 为数据依赖的插值参数。当 $\lambda_t = 1$ 时退化为 Mamba-2 的欧拉规则；当 $\lambda_t = 1/2$ 时退化为经典梯形规则。该方法具有局部截断误差 $O(\Delta_t^3)$ 和全局误差 $O(\Delta_t^2)$，是二阶方法。

**关键洞察**：指数梯形离散化等价于对状态输入施加一个数据依赖的、核大小为 2 的因果卷积，这解释了为何 Mamba-3 中传统的短因果卷积变为可选（见 Table 3a 消融验证）。

### 模块二：复值状态空间与数据依赖 RoPE

Mamba-3 将状态空间推广到复数域，以增强状态跟踪能力。

**命题 2（复值 SSM 定义）**：

$$\dot{\pmb{h}}(t) = \mathrm{Diag}(\boldsymbol{A}(t) + i\pmb{\theta}(t))\pmb{h}(t) + (\pmb{B}(t) + i\pmb{\hat{B}}(t))\boldsymbol{x}(t)$$

其中 $\pmb{\theta}(t)$ 控制状态旋转的频率。离散化后，该复值系统等价于一个实值 SSM，其状态转移矩阵为块对角旋转矩阵：

$$\pmb{h}_t = e^{\Delta_t A_t} \pmb{R}_t \pmb{h}_{t-1} + \Delta_t \pmb{B}_t x_t, \quad y_t = \pmb{C}_t^\top \pmb{h}_t$$

$\pmb{R}_t$ 为 $2 \times 2$ 旋转矩阵构成的块对角矩阵。

**命题 3（RoPE 等价性）**：通过展开递归，复值 SSM 等价于对 $\pmb{B}$ 和 $\pmb{C}$ 施加数据依赖的旋转位置编码（RoPE）：

$$h_t = e^{\Delta_t A_t} h_{t-1} + \left( \prod_{i=0}^t R_i^\top \right) B_t x_t$$

$$y_t = \left[ \left( \prod_{i=0}^t R_i^\top \right) C_t \right]^\top h_t$$

这意味着状态更新中的旋转操作可以完全转移到输入和输出投影上，无需在状态空间内部显式执行旋转。

### 模块三：Mamba-3 完整递归

将指数梯形离散化与复值状态结合，得到 Mamba-3 的完整递归（命题 4）：

$$\pmb{h}_t = \alpha_t \pmb{h}_{t-1} + \beta_t \left( \prod_{i=0}^{t-1} \pmb{R}_i^\top \right) \pmb{B}_{t-1} x_{t-1} + \gamma_t \left( \prod_{i=0}^{t} \pmb{R}_i^\top \right) \pmb{B}_t x_t$$

$$y_t = \left[ \left( \prod_{i=0}^{t} R_i^\top \right) C_t \right]^\top h_t$$

该递归同时具备二阶离散化精度和数据依赖的旋转动态，是 Mamba-3 层的核心计算。

### 模块四：MIMO 结构

Mamba-3 引入可选的多输入多输出（MIMO）结构，将 SISO 的外积形式状态更新替换为矩阵乘法形式。设秩为 $R$，状态更新和输出为：

$$H_t = a_t H_{t-1} + B_t X_t^\top, \quad Y_t = H_t^\top C_t$$

其中 $H_t \in \mathbb{R}^{N \times R}$ 为状态矩阵，$X_t \in \mathbb{R}^{R}$ 为输入，$B_t, C_t$ 的维度相应调整。MIMO 将解码阶段的算术强度从约 2.5 ops/byte（SISO）线性提升至 $R$ 倍（Table 7），在相同状态大小下显著提高硬件利用率。

### 辅助模块：BCNorm 与 BC 偏置

在 $\pmb{B}$ 和 $\pmb{C}$ 投影后添加 RMSNorm（BCNorm），类似于 Transformer 中的 QKNorm。此外，引入可学习的、按头、按通道的偏置，初始化为 1。消融实验（Table 9b）表明，同时为 $\pmb{B}$ 和 $\pmb{C}$ 添加偏置带来最佳预训练困惑度（ppl 15.69），仅添加 $\pmb{B}$ 偏置无益甚至有害。BC 偏置与指数梯形离散化的组合使得短因果卷积成为可选模块（Table 3a）。

### 完整流水线

Mamba-3 层的完整计算流水线（Figure 3）为：输入投影 → BCNorm → BC 偏置加法 → 复值指数梯形 SSM（命题 4）→ SiLU 门控 → 输出投影。其中 SSM 核心通过数据依赖的 RoPE（命题 3）和指数梯形递归（命题 1）实现，MIMO 变体进一步将状态更新替换为矩阵乘法形式以提高算术强度。

## 实验与分析

### 下游语言理解评估

Mamba-3 在 100B FineWeb-Edu 令牌训练的模型上进行了系统的下游语言理解评估，涵盖 LAMBADA、HellaSwag、PIQA、Arc-Easy、Arc-Challenge、WinoGrande 和 OpenBookQA 七个基准。Table 1 展示了从 180M 到 1.5B 四个规模下的平均准确率结果。


![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_HwCvaJOiCj/figures/001_Table_1.jpg]]
*Table 1: Downstream language modeling evaluations on models trained with 100B FineWeb-Edu tokens. Best results are bolded, and second best are underlined, excluding Mamba-3 MIMO variants. All models are trained with the same procedure. Mamba-3 SISO outperforms Mamba-2 and others at every model scale, and MIMO with rank R=4 further improves modeling capabilities*

**SISO 变体**在所有模型规模上均一致超越 Mamba-2（Dao & Gu, 2024）和 Gated DeltaNet（Schlag et al., 2021; Yang et al., 2025）等基线。以 1.5B 规模为例，Mamba-3 SISO 平均准确率达 56.4，较 Mamba-2 的 55.7 提升 0.7 个百分点，较 Gated DeltaNet 的 55.8 提升 0.6 个百分点。这一增益在更小规模上同样稳定存在：880M 时领先 Mamba-2 1.0 个百分点（54.4 vs 53.4），440M 时领先 0.2 个百分点（49.8 vs 49.6）。

**MIMO 变体**（秩 R=4）进一步放大了性能优势。在 1.5B 规模上，Mamba-3 MIMO 平均准确率达 57.6，比 Mamba-2 高出 1.9 个百分点，比 Gated DeltaNet 高出 1.8 个百分点，比 Transformer 基线高出 2.2 个百分点。值得注意的是，MIMO 变体在 440M 规模上即实现了 51.0 的准确率，较 SISO 的 49.8 提升 1.2 个百分点，表明多输入多输出结构在较小模型上同样有效。

**公平性说明**：所有 MIMO 变体通过降低 MLP 隐藏维度来匹配对应 SISO 变体的总参数量（见 MIMO Parameter Matching 表），确保比较的公平性。

### 状态大小与推理效率的帕累托前沿

Figure 2 展示了状态大小（推理速度的代理指标）与预训练困惑度（性能代理指标）之间的帕累托前沿。核心发现是：**Mamba-3 MIMO 在使用一半状态大小（state size 64）的情况下，即可匹配或超越 Mamba-2 使用 128 状态大小时的预训练困惑度**。这意味着在相同的推理延迟下，Mamba-3 可以提供显著更强的建模能力；或在相同性能水平下，实现更快的推理速度。


![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_HwCvaJOiCj/figures/005_Figure_2.jpg]]
*Figure 2: Exploration of state size (inference speed proxy) versus pretraining perplexity (performance proxy) across different Mamba variants. Mamba-3 improves the Pareto frontier compared to previous recurrent SISO models, while incorporating MIMO further shifts the frontier through better modeling performance without increasing state size. Table 4: Kernel latency (in milliseconds) comparison across models, precision, and $d _ { \mathrm { s t a t e } }$ values. Mamba-3 introduces minimal overhead compared to Mamba-2 and features highly efficient practical implementations. Our Mamba-3 SISO kernels are faster than reference Mamba-2 and GDN kernels at the commonly used bf16, $d _ { \mathrm { s t a t e } }$...

MIMO 结构通过将算术强度从 SISO 的约 2.5 ops/byte 线性提升至 R 倍（Table 7），有效缓解了解码阶段的内存带宽瓶颈。Table 4 的核延迟测量证实，Mamba-3 SISO 内核在常用的 bf16、$d_{state}=128$ 设置下比参考 Mamba-2 和 GDN 内核更快，而 MIMO（R=4）相比 SISO 仅引入极小的额外开销。


![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_HwCvaJOiCj/figures/009_Table_7.jpg]]
*Table 7: Arithmetic Intensity for (a) SISO, (b) MIMO. The batch and head dimensions cancel out. The arithmetic intensity of MIMO increases linearly with rank R, enabling better hardware utilization during memory-bound phases like decode. Here N is the state size (expansion factor) and P is the head dimension. For Mamba-3, typically R $\ll$ N , P*

### 合成状态跟踪能力

Table 3b 揭示了 Mamba-2 的一个关键缺陷及其在 Mamba-3 中的解决。在奇偶校验（Parity）和模运算（Modular Arithmetic without brackets）两项合成状态跟踪任务上，Mamba-2 的表现接近随机猜测，而 Mamba-3 分别取得了 100% 和 98.51% 的准确率。这一能力飞跃归因于复值状态空间引入的数据依赖旋转嵌入（RoPE trick，Proposition 3），使模型能够有效跟踪序列中的离散状态变化——这是实值标量状态转移无法实现的功能。

### 核心组件消融

Table 3a 在 440M 规模上对关键设计选择进行了消融分析：

- **BC 偏置与指数梯形离散化的协同**：同时移除 BC 偏置和指数梯形离散化（回退到 Mamba-2 的欧拉离散化）导致困惑度从 15.72 显著上升至 16.68（Mamba-3-bias-trap 配置）。
- **短因果卷积变为可选**：BC 偏置与指数梯形离散化的组合使得原本在 Mamba-2 中必需的短因果卷积（核大小 4）可以被移除，且移除后模型性能不降反升。这一发现表明，指数梯形离散化通过其隐式的二阶卷积结构（Figure 1 左），已经内建了足够的局部上下文建模能力。
- **BC 偏置的细粒度消融**（Table 9b）：同时为 B 和 C 添加可学习的按头、按通道偏置带来最佳预训练困惑度（15.69）；仅添加 B 偏置无益甚至有害，说明输入和输出投影的偏置需要协同作用。

### $\lambda_t$ 参数化选择

Table 6 对指数梯形更新中 $\lambda_t$ 的参数化方式进行了消融。默认的 $\sigma(u_t)$ 参数化（通过 sigmoid 门控学习数据依赖的积分权重）在所有变体中获得了最低的预训练困惑度（15.72）。值得注意的是，不强制 $\lambda_t = 1/2 + O(\Delta_t)$ 的二阶精度约束反而带来更好的经验性能，表明模型能够自主学习适合任务的积分策略。

### 检索能力分析

Table 2 展示了 Mamba-3 在检索任务上的能力分布：


![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_HwCvaJOiCj/figures/002_Table_2.jpg]]
*Table 2: Retrieval capabilities measured by a mixture of real-world and synthetic retrieval tasks. Real-world retrieval tasks utilize cloze variants of the original datasets and are truncated to 2K length. Mamba-3 demonstrates strong associative recall, question-answering, and length generalization on needle-in-a-haystack (NIAH), but suffers with information extraction of semi-structured and unstructured data. The Transformer baseline uses RoPE which may explain its length generalization issues, and hybrid models utilize NoPE (no positional embeddings). We find a pre-gate, grouped RMSNorm can be added to Mamba-3 SISO hybrid models to improve the length generalization of the NIAH tasks at a slight de...*

- **强项**：Mamba-3 SISO 在关联回忆和问答类任务上表现强劲。在 NIAH-Single-1 任务上，1024 和 2048 上下文长度下均达到 100% 准确率，4096 长度下仍保持 88.2%。这表明数据依赖的 RoPE 机制赋予了模型良好的上下文检索能力。
- **弱项**：在需要从半结构化和非结构化数据中提取信息的任务（如 SWDE、DROP）上表现不佳。这一失败模式提示，纯线性注意力机制在处理需要精确信息定位的复杂检索场景时仍存在局限。
- **混合模型归一化探索**（Table 8）：在混合 Mamba-3 SISO 模型（线性层与 NoPE 自注意力以 5:1 交错）中，无额外归一化获得最强的平均上下文检索性能；而预门控分组 RMSNorm 在超长合成检索任务（NIAH）上表现最佳，尤其是在超过训练上下文长度的设置下。理想的归一化配置（类型与位置）仍需根据具体场景权衡。


![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_HwCvaJOiCj/figures/012_Table_8.jpg]]
*Table 8: Ablations of optional norm type (grouped vs default) and placement (pre- vs post-gate) on pretrained hybrid Mamba-3 SISO models at the 1.5B scale. All models have BCNorm. No additional norm demonstrates the strongest in-context retrieval performance on average, while pre-gate, grouped RMS results in the best performance on synthetic retrieval, especially on lengths longer than its training context*

### 长度外推能力

Figure 4 展示了 1.5B 预训练模型在 FineWeb-Edu 测试集上随上下文长度变化的表现。Mamba-3 展现出较强的长度外推能力，在超出训练长度的上下文下仍保持稳定的困惑度；而 Mamba-2 在长上下文下性能明显下降。这一优势可能源于指数梯形离散化的二阶精度带来的更稳定的长程依赖建模。

### 预训练性能曲线

Figure 5 的验证集困惑度曲线显示，Mamba-3 在整个预训练过程中持续优于 Mamba-2 和 Gated DeltaNet 等强基线。Figure 6 进一步确认，在包含 Gated DeltaNet 基线的状态大小-困惑度帕累托前沿上，Mamba-3 和 Mamba-3 MIMO 持续占据最优位置。

### 已知局限

1. **MIMO 训练开销**：MIMO 结构带来约 R 倍的 FLOPs 增加，尽管通过减少 MLP 宽度进行参数匹配，训练速度仍有所下降。
2. **检索任务短板**：半结构化和非结构化数据的信息提取能力不足。
3. **规模验证有限**：当前实验最大规模为 1.5B 参数，尚未在 7B+ 规模上验证。
4. **超参数敏感性**：复值 SSM 和指数梯形离散化引入了额外超参数（如 $\lambda_t$），最优参数化可能依赖于任务和规模。

### 补充图表

![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_HwCvaJOiCj/figures/003_Table.jpg]]
*Table: (a) Component ablation at 440M scale. Combining BC bias and exponential-trapezoidal discretization makes the ubiquitous short convolution optional. (b) Performance comparison on formal language tasks. Unlike Mamba-2, Mamba-3 features state-tracking ability stemming from data-dependent RoPE embeddings*

![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_HwCvaJOiCj/figures/006_Table_5.jpg]]
*Table 5: Table of canonical linear-time invariant discretizations (top) and custom linear-time varying discretizations derived from our exponential-adjusted framework (bottom), along with their appearance in structured SSMs used in deep learning. Our framework formalizes the prior Mamba discretization as exponential-Euler and extends it with the more expressive exponential-trapezoidal method. Discretization methods convert the continuous SSM $\begin{array} { r } { \dot { \pmb { h ( t ) } } = \pmb { A ( t ) } \pmb { h ( t ) } + \pmb { B ( t ) } \pmb { x ( t ) } } \end{array}$ into the discrete recurrence $h _ { t } = \alpha _ { t } h _ { t - 1 } + \beta _ { t } B _ { t - 1 } x _ { t - 1 } + \gamma _ { t...$

![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_HwCvaJOiCj/figures/007_Table.jpg]]

![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_HwCvaJOiCj/figures/010_Table.jpg]]
*Table: MIMO Parameter Matching. The MIMO variant of Mamba3 incurs additional parameters compared to its SISO counterpart. We therefore reduce the hidden dimension of the MLP layers to parameter-match the SISO variants as follows*

![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_HwCvaJOiCj/figures/015_Table.jpg]]

![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_HwCvaJOiCj/figures/016_Table.jpg]]

![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_HwCvaJOiCj/figures/017_Table_10.jpg]]
*Table 10: Kernel DSL and fusion structure for forward (prefill) kernels*


## 方法谱系与知识库定位

### 1. 与基线方法的关系

Mamba-3 的核心贡献在于从状态空间模型（SSM）的连续-离散理论出发，对 Mamba-2 的三个关键维度进行了系统性升级：离散化精度、状态空间表达能力、以及解码硬件效率。这三项改进并非孤立的技巧堆叠，而是共同作用于“在不增加推理开销的前提下提升序列建模能力”这一统一目标。

**相对于 Mamba-2**（Dao & Gu, 2024）：Mamba-2 采用指数欧拉离散化（一阶）和实值标量状态转移，其状态更新本质上是 $h_t = \alpha_t h_{t-1} + \gamma_t B_t x_t$ 的简化递归。Mamba-3 将这一框架推广为指数梯形离散化（二阶），引入了前一时间步的输入项 $B_{t-1} x_{t-1}$，使递归变为 $h_t = \alpha_t h_{t-1} + \beta_t B_{t-1} x_{t-1} + \gamma_t B_t x_t$（Proposition 1, eq. (3)）。这一推广的实质是将 Mamba-2 的“保持端点”近似替换为“平均端点”近似，从而获得可证明的二阶全局误差界 $O(\Delta_t^2)$（Remark 3, Section 3.1.1）。更重要的是，指数梯形离散化与 BC 偏置的组合使得 Mamba-2 中普遍使用的短因果卷积（kernel size 4）变为可选——消融实验显示，移除短卷积后模型性能不降反升（Table 3a, Section 4.2），这直接归因于指数梯形递归展开后隐含的数据依赖卷积效应（Section 3.1.2）。

在状态空间类型上，Mamba-3 将实值标量状态转移矩阵推广为复值对角矩阵，其离散化后的等效实值形式为 $h_t = e^{\Delta_t A_t} R_t h_{t-1} + \Delta_t B_t x_t$，其中 $R_t$ 是块对角旋转矩阵（Proposition 2, eq. (6)）。进一步通过“RoPE trick”，该递归可等价转换为对 B 和 C 投影施加数据依赖的旋转嵌入（Proposition 3, eq. (7)）。这一设计使 Mamba-3 具备了 Mamba-2 完全缺失的状态跟踪能力——在奇偶校验任务上达到 100% 准确率，在模运算任务上达到 98.51%，而 Mamba-2 的表现接近随机猜测（Table 3b, Section 4.2）。

**相对于 Gated DeltaNet**（Schlag et al., 2021; Yang et al., 2025）：Gated DeltaNet 是线性注意力变体中的最新强基线，引入了门控机制。Mamba-3 在 1.5B 参数规模上，SISO 变体的平均下游准确率比 Gated DeltaNet 高 0.6 个百分点，MIMO 变体则高出 1.8 个百分点（Table 1, Section 4.1）。这一差距表明，Mamba-3 从 SSM 理论出发的结构化改进（而非仅在注意力机制上添加门控）能更有效地提升序列建模质量。

**相对于标准 Transformer**（带 RoPE）：Mamba-3 MIMO 在 1.5B 规模上的平均下游准确率比 Transformer 基线高 2.2 个百分点（Section 1）。值得注意的是，Mamba-3 的复值 SSM 通过数据依赖的旋转嵌入实现了类似 RoPE 的位置编码效果，但该旋转是数据依赖的，而非 Transformer 中使用的固定频率旋转——这可能是其在长度外推上表现更优的原因之一（Figure 4, Section 4.1）。

### 2. 适用边界与局限

Mamba-3 的改进并非在所有场景下都带来增益，其适用边界主要体现在以下几个方面：

**检索任务的非对称表现**：Mamba-3 在联想回忆和问答类检索任务上表现强劲，但在需要从半结构化和非结构化数据中提取信息的任务上表现不佳（如 SWDE、DROP 等，Table 2, Section 4.1.2）。这表明复值状态和指数梯形离散化主要增强了序列内部的因果推理能力，但对需要精确信息定位和结构化解析的任务，其表达能力仍不及注意力机制。混合模型（以 5:1 比例交错线性层和 NoPE 自注意力）在超长合成检索（NIAH）上通过添加预门控分组 RMSNorm 有所改善，但这是在牺牲部分真实世界检索性能的代价下获得的（Table 8, Section 4.1.2）。

**MIMO 的训练计算开销**：MIMO 结构通过将状态更新从外积形式改为矩阵乘法形式，将解码阶段的算术强度从约 2.5 ops/byte 线性提升至 $R$ 倍（Table 7, Section D），从而提高了硬件利用率。然而，这一改进的代价是训练时 FLOPs 增加 $R$ 倍。当前通过减少 MLP 隐藏维度来匹配 SISO 变体的总参数量（MIMO Parameter Matching table, Section 4.1），但训练速度仍有所下降。这意味着 MIMO 的优势主要体现在推理部署阶段，对训练预算敏感的场景可能更倾向于使用 SISO 变体。

**规模验证的局限**：当前所有实验均在 1.5B 参数量级及以下进行（最大 1.5B，训练数据 100B FineWeb-Edu tokens），尚未在更大规模（如 7B+）上验证。复值 SSM 和指数梯形离散化引入的额外超参数（如 $\lambda_t$ 的参数化方式）在小规模上的最优设置（默认 $\sigma(u_t)$ 参数化，Table 6）是否在大规模上仍然最优，需要进一步验证。

**归一化策略的未决问题**：混合模型中归一化的类型（分组 vs 默认）和位置（预门控 vs 后门控）存在明显的 trade-off——无额外归一化在平均上下文检索性能上最强，但预门控分组 RMSNorm 在超长合成检索上表现最佳（Table 8）。这一平衡点尚未被充分探索。

### 3. 开放问题

1. **大规模混合架构的集成策略**：如何将 Mamba-3 有效集成到更大规模的混合架构中（如与注意力层交错），并确定最佳的混合比例和归一化策略？当前仅在 5:1 的固定比例下进行了初步探索。

2. **复杂推理任务的能力边界**：Mamba-3 的复值状态和 MIMO 结构在合成状态跟踪任务上表现卓越，但在多步推理、数学推理等更复杂的场景中能否带来比现有线性模型更大的增益，尚待验证。

3. **MIMO 训练效率的优化**：能否进一步优化 MIMO 的训练算法以减少计算开销，而无需像当前这样仔细调整块大小？这是 MIMO 从实验室走向大规模实际应用的关键瓶颈。

4. **理论局限性的深入分析**：数据依赖的旋转嵌入（RoPE trick）是否存在理论上的表达能力上限？是否可以与标准的位置编码方案更好地结合，以在检索和推理任务之间取得更优的平衡？

5. **超大规模扩展的验证**：当前模型仅在相对较小的规模上验证，扩展到数十亿参数时，指数梯形离散化的二阶精度优势是否会被其他因素（如优化难度、数值稳定性）所抵消，仍需实证检验。

## 原文 PDF

![[paperPDFs/ICLR_2026/Mamba_3_Improved_Sequence_Modeling_using_State_Space_Principles.pdf]]
