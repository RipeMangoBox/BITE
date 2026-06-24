---
title: "On the Reasoning Abilities of Masked Diffusion Language Models"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/On_the_Reasoning_Abilities_of_Masked_Diffusion_Language_Models.pdf
openreview_forum_id: BVnIsh4Nz1
aliases:
- IMDMMPP
- RAMDLM
tags:
- ICLR_2026
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/representation_learning
core_operator: "掩蔽扩散模型（MDM）的\"去噪步数 T\"和\"输出填充空间大小 P\"是控制推理能力的核心变量：更多步数和更大填充空间可将表达能力从AC^0（常数步）提升到AC^d（多项式对数步）并最终达到并行问题类NC。同时，\"规划器（planner）的非均匀解掩蔽策略\"（而不是均匀随机解掩蔽）使得模型能够按需选择先解哪些子问题，实现有向的并行分解。"
primary_logic: "掩蔽扩散模型在有限精度对数宽度Transformer框架下，与填充循环Transformer（PLT）等价。这一等价性使MDM继承了已知PLT的复杂性理论表征：O(log N)步可识别正则语言，而Chain-of-Thought在O(log N)步内无法做到，从而证明MDM在可并行化问题上具有严格更高的推理效率。去噪过程的迭代解掩蔽天然映射到循环推理，而同时生成多个符号的能力使其比逐符号CoT更高效。"
claims:
- "MDM与填充循环Transformer（PLT）在有限精度对数宽度下等价。"
- "MDM可模拟pCoT（并行链式思考）且pCoT可模拟MDM，但MDM模拟pCoT需要平方级额外输出空间。"
- "O(log N)步的MDM能识别所有正则语言，而O(log N)步的CoT不能，构成严格表达能力分离。"
- "多项式对数去噪步数且多项式输出空间的MDM等价于L-uniform AC^d，当步数足够多时收敛至所有可并行化问题类NC。"
---

# On the Reasoning Abilities of Masked Diffusion Language Models

> [!tip] 核心洞察
> 掩蔽扩散模型在有限精度对数宽度Transformer框架下，与填充循环Transformer（PLT）等价。这一等价性使MDM继承了已知PLT的复杂性理论表征：O(log N)步可识别正则语言，而Chain-of-Thought在O(log N)步内无法做到，从而证明MDM在可并行化问题上具有严格更高的推理效率。去噪过程的迭代解掩蔽天然映射到循环推理，而同时生成多个符号的能力使其比逐符号CoT更高效。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 掩蔽扩散语言模型的推理能力研究 |
| 英文题名 | On the Reasoning Abilities of Masked Diffusion Language Models |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=BVnIsh4Nz1) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/representation_learning |
| Method | Idealized Masked Diffusion Model (MDM) with Planner and Predictor |
| Dataset |  |

## 概述

自回归语言模型配合思维链（Chain‑of‑Thought, CoT）推理已成为大语言模型解决复杂任务的标配范式。然而，该范式存在一个根本性的**顺序性瓶颈**：即使问题可分解为多个相互独立的子问题，模型仍需逐符号生成，导致推理步数与问题规模线性相关，无法通过并行化加速求解。这一瓶颈在数学表达式求值等天然可并行的任务上尤为突出——串行策略需要11步，而并行策略仅需3步（Figure 3）。

本文从计算复杂性理论角度，系统研究了**掩蔽扩散语言模型（Masked Diffusion Model, MDM）** 的推理能力边界。核心发现可概括为三条主线：

**1. MDM与循环Transformer等价。** 在有限精度、对数宽度的Transformer框架下，MDM与填充循环Transformer（Padded Looped Transformer, PLT）相互可模拟（Theorem 3.1），且在忽略对数因子的填充长度下完全等价（Corollary 3.1）。这一等价性将已知的PLT复杂性表征直接迁移至MDM，为后续分析奠定基础。

**2. 去噪步数与输出空间控制表达能力层级。** MDM的推理能力由两个核心变量决定：去噪步数 $T$ 和输出填充空间大小 $P$。常数步去噪无法超越标准Transformer的表达能力，即 $ \mathsf{MDM}[\mathcal{O}(1), \mathsf{poly}(N)] = \mathsf{L\text{-}uniform\ AC}^0 $（Corollary 3.3）；多项式对数步数 $ \mathcal{O}(\log^d N) $ 则将表达能力提升至 $ \mathsf{AC}^d $，并最终收敛至所有可并行化问题类 $ \mathsf{NC} $（Corollary 3.4）。

**3. MDM在可并行化问题上严格优于CoT。** $ \mathcal{O}(\log N) $ 步的MDM可识别所有正则语言，而同步数的CoT无法做到，构成严格的表达能力分离：$ \mathsf{CoT}[\log N] \subsetneq \mathsf{MDM}[\log N, N] $（Corollary 3.7）。MDM的迭代解掩蔽过程天然映射到循环推理，而同时生成多个符号的能力使其在可分解问题上具备严格更高的推理效率。

为实现上述理论分析，本文将MDM形式化为两个理想化组件的协同：**规划器（Planner）** 决定每步解掩蔽或重采样哪些位置，**预测器（Predictor）** 基于完整上下文为选定位置生成符号分布。这一框架突破了标准MDM的两项关键限制——均匀随机解掩蔽和逐位置独立的因子化近似——从而释放了并行推理的表达潜力。

## 背景与动机

### 自回归语言模型的“顺序性瓶颈”

自回归语言模型（autoregressive LMs）已成为当前大语言模型的主流范式。在推理任务中，这类模型通常依赖**链式思考（Chain-of-Thought, CoT）**（Wei et al., 2022）来逐步生成中间推理步骤，最终给出答案。然而，这种逐符号（token-by-token）的生成方式存在一个根本性的结构限制——**顺序性瓶颈（sequentiality bottleneck）**：即使问题本身可以分解为多个相互独立的子问题，模型仍然必须按顺序逐个生成符号，导致推理步数与问题规模呈线性相关，无法通过并行化来加速求解。

这一瓶颈在可并行化的推理任务上尤为突出。例如，在数学表达式求值中，多个不相关的子表达式可以同时计算，但CoT必须将它们串行展开，浪费了问题结构天然蕴含的并行性。

### 掩蔽扩散模型的潜力与已知局限

**掩蔽扩散语言模型（Masked Diffusion Models, MDMs）** 提供了一种不同于自回归的生成范式：从完全掩蔽的噪声字符串出发，通过多步去噪过程逐步解掩蔽（unmask）符号，最终生成完整文本。MDM的核心优势在于其**内在的并行性**——在每一步去噪中，多个位置可以同时被预测和填充，理论上具备打破顺序性瓶颈的潜力。

然而，标准MDM存在两个关键假设，严重限制了其实际表达能力：

1. **均匀随机解掩蔽**：每一步随机选择位置进行解掩蔽，无法根据问题结构优先处理关键子问题。
2. **位置独立的因子化近似**：反向过程假设各位置相互独立进行预测（Eq. (1)），忽略了位置间的依赖关系，导致模型无法匹配某些简单分布。

在这两个假设下，即使假定模型具有完美的近似能力，标准MDM的表达能力也无法超越**AC⁰**——即标准Transformer的表达能力层级，常数步去噪无法带来实质性的能力提升。

### 本文的核心动机与研究问题

上述背景引出了本文的核心研究问题：

> **如果放开标准MDM的限制性假设——允许非均匀的、由“规划器”决定的解掩蔽策略，并允许预测器基于完整上下文进行条件预测——MDM的表达能力能否得到根本性提升？这种提升在计算复杂性理论中如何精确刻画？**

具体而言，本文旨在回答以下子问题：

- MDM与已知的循环推理架构（如**填充循环Transformer, PLT**；Dehghani et al., 2019; London & Kanade, 2025）之间存在怎样的表达力关系？
- 去噪步数 $T$ 和输出填充空间 $P$ 如何控制MDM的表达能力层级——从正则语言到可并行化问题类 **NC**？
- MDM相对于CoT是否具有**严格的**推理效率优势？在什么条件下可以证明这种分离？

### 理论分析框架的选择

为严格回答上述问题，本文选择在**有限精度、对数宽度Transformer**的计算框架下进行分析。这一框架已被广泛用于分析Transformer的表达能力与电路复杂度类之间的关系，使得MDM的能力可以与经典复杂度类（如AC⁰、ACᵈ、NC、正则语言类Reg）建立精确映射。论文的核心发现——MDM与PLT的等价性、MDM对CoT的严格包含关系、以及去噪步数与表达能力层级之间的对应——均在这一框架下以定理和推论的形式给出形式化证明。

## 核心创新

本文的核心创新不在于提出新的模型架构，而在于**通过理论分析揭示掩蔽扩散语言模型（MDM）的并行推理潜力，并给出其表达能力的严格复杂性刻画**。相对自回归链式思考（CoT）和标准均匀解掩蔽MDM，本文在三个维度上实现了突破。

### 1. 非均匀规划器：打破因子化独立性的表达力瓶颈

标准MDM的反向过程采用**逐位置独立近似**（Eq. (1)），且假定**均匀随机解掩蔽**和**完美近似**。这一组合将模型表达力限制在 $\text{AC}^0$——即标准Transformer的复杂度类（Corollary 3.3），无法超越。

本文的关键改造是将反向过程分解为两个独立组件：
- **规划器（Planner）**：决定每步解掩蔽哪些位置，允许非均匀策略和对已生成符号的**重采样（resampling）**；
- **预测器（Predictor）**：基于完整上下文为指定位置生成符号分布，不再受位置独立因子化的限制。

这一改造的核心意义在于：**规划器可以按需选择先解哪些子问题，实现有向的并行分解**。例如，在数学表达式求值中（Figure 3），规划器可优先解掩蔽相互独立的子表达式位置，使多步并行求值成为可能，而非被迫逐符号生成。

### 2. 去噪步数与填充空间：控制表达力的双变量

本文通过等价性分析，将MDM的表达力精确映射到两个可控变量：

| 变量 | 作用 | 关键结论 |
|------|------|----------|
| 去噪步数 $T$ | 控制推理深度 | $T = O(1)$：等价于 $\text{AC}^0$（Cor. 3.3）；$T = O(\log^d N)$：等价于 $\text{AC}^d$（Cor. 3.4）；$T$ 足够大时收敛至 $\text{NC}$ |
| 输出填充空间 $P$ | 控制并行宽度 | $P = \text{poly}(N)$ 配合足够步数可达 $\text{NC}$；$P = N$ 配合 $O(\log N)$ 步可识别所有正则语言（Cor. 3.7） |

这一双变量控制机制揭示了MDM的**“步数换表达力”**特性：增加去噪步数可将模型从有限深度的并行电路类逐步提升至所有可并行化问题类 $\text{NC}$。这与CoT的逐符号生成形成鲜明对比——CoT的推理步数与问题规模线性相关，无法通过增加步数实现类似的表达力跃迁。

### 3. 严格表达能力分离：MDM > CoT

本文最有力的理论贡献是证明了MDM与CoT之间的**严格包含关系**：

$$\text{CoT}[\log N] \subsetneq \text{MDM}[\log N, N]$$

具体而言，$O(\log N)$ 步的MDM能识别所有正则语言，而相同步数的CoT无法做到（Corollary 3.7）。这一分离的本质原因在于：**MDM的迭代解掩蔽天然映射到循环推理，而同时生成多个符号的能力使其在处理可分解子问题时具有并行优势**——CoT即使面对相互独立的子问题，也必须逐符号串行生成（即“顺序性瓶颈”）。

此外，MDM与填充循环Transformer（PLT）的等价性（Corollary 3.1：$\text{MDM}[T, \widetilde{\mathcal{O}}(N^K)] = \text{PLT}[T, \mathcal{O}(N^K)]$）为上述结论提供了技术基础：这一等价性使MDM继承了PLT已知的复杂性理论表征，从而能够严格定位其在电路复杂度谱系中的位置。

### 4. 重采样机制：修正错误的并行能力

传统MDM仅允许从掩码状态转换到非掩码状态，一旦生成符号便无法修改。本文引入的**重采样（resampling）**机制允许规划器将已解掩蔽位置重新标记为需预测，从而修正先前错误。这一机制在并行推理场景中尤为关键：当模型同时生成多个符号时，后续步的重采样提供了纠错通道，避免了错误在并行分支间的级联传播。

## 整体框架

![[assets/figures/papers/paper_list_l48_https_openreview_net_forum_id_BVnIsh4Nz1/figures/001_Figure_1.jpg]]
*Figure 1: A summary of masked diffusion model expressivity in relation to padded looped transformers and chain of thought. X ãÑ Y indicates the inclusion of X in Y. Dashed arrows represent strict inclusions. Red arrows denote novel results. Edge labels with blue background indicate constraints on the source node, while labels with orange background indicate constraints on the target node*

![[assets/figures/papers/paper_list_l48_https_openreview_net_forum_id_BVnIsh4Nz1/figures/002_Figure_2.jpg]]
*Figure 2: A summary of masked diffusion model expressivity in relation to classical complexity classes. x $\hookrightarrow$ y indicates the inclusion of X in Y, and $\dot { \mathcal { X } } \mathcal { Y }$ indicates equality. Dashed arrows represent strict inclusions. Red arrows denote novel results. Reg refers to all regular languages. Edge labels with blue background indicate constraints on the source node, while labels with orange background indicate constraints on the target node (in case of Ø, on MDMs)

本文提出一个理想化的掩蔽扩散语言模型（Idealized Masked Diffusion Model, MDM）分析框架，旨在从理论层面刻画MDM的推理表达能力，而非描述一个可训练的工程流水线。该框架将MDM的生成过程抽象为两个核心模块的迭代交互：**规划器（Planner）**与**预测器（Predictor）**，并通过去噪步数 $T$ 和输出填充空间大小 $P$ 两个自由度来控制模型的表达能力。

### 输入输出流

- **输入**：一个长度为 $N$ 的字符串，来自有限字母表 $\Sigma$。
- **初始状态**：一个完全掩蔽的填充字符串（所有位置均为掩码符号 $\mathfrak{m}$），填充后总长度为 $N + P$，其中 $P$ 为额外填充空间。
- **迭代过程**：在 $T$ 个去噪步内，规划器与预测器交替作用，逐步将掩蔽字符串转化为最终输出。
- **输出**：一个判定结果（语言成员判定问题中的接受/拒绝），而非自由文本生成。模型最终输出一个符号来指示输入字符串是否属于目标语言。

### 核心模块与交互关系

整个推理流水线由以下三个模块构成，其交互关系如 Figure 1 所示（该图以分类学图的形式总结了MDM与填充循环Transformer、链式思考之间的表达力包含关系）：

**1. 规划器（Planner）**
规划器是MDM区别于标准掩蔽扩散模型的关键创新点。在每一步 $t$，规划器根据当前部分掩蔽的字符串状态，决定下一步哪些位置需要被解掩蔽（unmask）或重采样（resample）。与标准MDM中“均匀随机选择位置解掩蔽”的策略不同，理想化框架允许规划器采用**非均匀、确定性**的解掩蔽策略，从而能够按需优先解决某些子问题，实现有向的并行分解。此外，规划器可以将已解掩蔽的位置重新标记为需预测状态，这赋予了模型修正先前错误的能力——这是传统MDM（仅允许从掩码到非掩码的单向转换）所不具备的。

**2. 预测器（Predictor）**
预测器接收当前部分掩蔽的字符串，为规划器指定的每个待解掩蔽位置生成一个符号分布。在实现上，预测器基于Transformer架构，通过计算每个位置的“填补概率”来确定最可能的符号。与标准MDM中“逐位置独立预测”的因子化近似（Eq. (1)）不同，理想化框架中的预测器可以基于完整上下文进行条件预测，从而规避了位置独立性假设带来的表达力限制。

**3. 解码/解掩蔽过程（Decoder / Unmasking Process）**
整个解码过程是规划器与预测器的 $T$ 步迭代：从完全掩蔽的初始状态出发，每步由规划器选定解掩蔽位置，再由预测器为这些位置生成符号，逐步将掩蔽字符串转换为最终输出。这一迭代解掩蔽过程天然地映射到循环推理，而同时生成多个符号的能力使其比逐符号生成的自回归模型（如Chain-of-Thought）在可并行化问题上具有更高的推理效率。

### 与基线方法的差异

| 模块/特性 | 标准MDM（均匀解掩蔽） | 本文理想化MDM |
|-----------|----------------------|---------------|
| 解掩蔽策略 | 均匀随机选择位置 | 规划器决定，支持非均匀/确定性策略 |
| 反向过程因子化 | 逐位置独立（Eq. (1)） | 预测器可基于完整上下文条件预测 |
| 重采样已解掩蔽符号 | 不允许 | 允许，规划器可修正先前错误 |

### 表达能力关系的整体图景

Figure 1 和 Figure 2 从两个维度总结了MDM的表达能力定位：

- **Figure 1** 展示了MDM与填充循环Transformer（PLT）、链式思考Transformer（CoT）之间的包含关系。核心结论是：MDM与PLT在有限精度对数宽度下等价（推论3.1），且MDM可以模拟CoT（定理3.3），反之亦然（定理3.4），但模拟CoT时MDM需要平方级的额外输出空间。

- **Figure 2** 将MDM置于经典电路复杂度类的层级中：常数步去噪的MDM等价于 $\text{AC}^0$（标准Transformer的表达能力）；$O(\log^d N)$ 步去噪且多项式输出空间的MDM等价于 $\text{L-uniform AC}^d$；当去噪步数足够多时，MDM收敛至 $\text{NC}$——所有可并行化问题的类。特别地，$O(\log N)$ 步的MDM能识别所有正则语言，而同等步数的CoT无法做到，构成严格的表达能力分离（推论3.7）。

### 关键控制变量

整个框架的表达能力由两个核心变量控制：

- **去噪步数 $T$**：更多步数使模型能够进行更深层的迭代推理，将表达能力从 $\text{AC}^0$（常数步）提升到 $\text{AC}^d$（多项式对数步）并最终达到 $\text{NC}$。
- **输出填充空间 $P$**：更大的填充空间为模型提供了更多的“草稿纸”来存储中间计算结果，是实现并行推理的必要资源。

这两个变量共同决定了MDM在复杂度类层级中的位置，也构成了本文所有理论分析的基础参数空间。

## 核心模块与公式推导

### 2.1 理想化掩蔽扩散模型的分解架构

本文提出的理想化掩蔽扩散模型（MDM）将反向去噪过程分解为两个核心组件：**规划器（Planner）** 与 **预测器（Predictor）**。这一分解直接回应了标准MDM中两个限制表达力的假设——均匀随机解掩蔽（Assumption 2.1）和逐位置独立预测的完美近似（Assumption 2.2）。

**规划器**（Definition B.15）根据当前部分掩蔽的字符串状态，决定下一步哪些位置需要被解掩蔽或重采样。与标准MDM的均匀随机选择不同，规划器支持**非均匀、确定性的解掩蔽策略**，并允许将已生成的符号重新标记为“需预测”（resampling），从而修正先前错误。这一能力克服了传统MDM“一旦生成即不可修改”的根本限制。

**预测器**（Definition B.16）在给定当前部分掩蔽字符串的条件下，为规划器指定的每个解掩蔽位置生成符号分布。预测器通过Transformer实现，其核心操作是计算各位置的填补概率，不再受限于逐位置独立的因子化近似。

**去掩蔽过程**（Definition B.18）将上述组件组合为 $T$ 步迭代：从完全掩蔽的填充字符串出发，每步依次执行规划与预测，逐步将掩码符号替换为实际符号，最终输出生成字符串。

### 2.2 关键公式及其变量含义

**前向掩蔽过程**定义了从原始字符串 $\pmb w^{(0)}$ 到第 $t$ 步噪声字符串 $\pmb w^{(t)}$ 的概率：

$$q_{t|0}(\pmb w^{(t)} \mid \pmb w^{(0)}) = \prod_{n=1}^{N} q_{t|0}(\pmb w_n^{(t)} \mid \pmb w_n^{(0)}), \qquad q_{t|0}(\pmb w_n^{(t)} \mid \pmb w_n^{(0)}) = \begin{cases} 1-\alpha(t/T), & \text{if } \pmb w_n^{(t)} = \mathfrak{m} \\ \alpha(t/T), & \text{otherwise} \end{cases}$$

其中 $\mathfrak{m}$ 为掩码符号，$\alpha(\cdot)$ 为掩蔽调度函数，控制各时间步保留原始符号的概率。前向过程按位置独立施加掩蔽，是后续反向去噪的噪声源。

**标准MDM的因子化反向近似**为：

$$\widehat{q}_{t-1|t}(\pmb w^{(t-1)} \mid \pmb w^{(t)}) = \prod_{n=1}^{N} \widehat{q}_{t-1|t}(\pmb w_n^{(t-1)} \mid \pmb w^{(t)})$$

该近似假设各位置的去噪预测相互独立，虽支持并行生成，但忽略了位置间的依赖关系。本文通过引入规划器和预测器的解耦设计，**放弃此因子化假设**，使预测器可基于完整上下文进行条件预测，从而规避因子化带来的表达力限制。

### 2.3 架构修改的三个关键槽位

相较于标准MDM，理想化MDM在三个关键设计点上进行了修改：

| 槽位 | 基线值（标准MDM） | 本文方案 | 证据锚点 |
|------|-------------------|----------|----------|
| 解掩蔽策略 | 均匀随机选择位置 | 规划器决定，支持非均匀/确定性策略及重采样 | §2.2.1 |
| 反向过程因子化 | 逐位置独立近似（Eq. 1） | 预测器基于完整上下文条件预测，放弃位置独立性 | §2.2.1 |
| 重采样机制 | 仅允许掩码→非掩码，禁止修改已生成符号 | 规划器可将已解掩蔽位置重新标记为需预测 | §2.2.1 |

这三个修改共同构成了MDM表达力提升的**因果旋钮**：非均匀解掩蔽策略使模型能按需选择先解哪些子问题（实现有向并行分解），放弃因子化假设使预测器能捕获位置间依赖，而重采样机制则允许模型在后续步骤中修正早期错误——这些能力是标准MDM被限制在 $\text{AC}^0$ 表达力（推论3.3）的根本原因。

## 实验与分析

![[assets/figures/papers/paper_list_l48_https_openreview_net_forum_id_BVnIsh4Nz1/figures/003_Figure_3.jpg]]
*Figure 3: Two strategies for solving a mathematical expression. (a) Parallel: Parallel computation of intermediate values (three steps). (b) Sequential: Step-by-step generation (eleven steps)*

**本文为纯理论分析，未包含任何实证实验。** 所有“结果”均为定理、推论及复杂性包含/分离关系的形式化证明。评估优劣的基准是表达能力类（如 AC⁰、TC⁰、NC 等）和所需步数/输出空间，而非实验指标。以下按主结果、消融分析和失败模式三个维度梳理论文的理论发现。

### 主结果

#### 1. MDM 与填充循环 Transformer 等价（核心桥梁）

**Theorem 3.1** 建立了理想化掩蔽扩散模型与填充循环 Transformer 之间的双向模拟关系：

$$\mathsf{MDM}[T, P] \subseteq \mathsf{PLT}[T, P] \quad \text{且} \quad \mathsf{PLT}[T, P] \subseteq \mathsf{MDM}[T, (N+P)D]$$

其中 $D$ 为 PLT 的模型宽度。在忽略对数因子的填充长度下，二者完全等价（**Corollary 3.1**）：

$$\mathsf{MDM}[T, \widetilde{\mathcal{O}}(N^K)] = \mathsf{PLT}[T, \mathcal{O}(N^K)]$$

这一等价性是全文理论推导的枢纽：MDM 继承了 PLT 已知的复杂度表征，同时 PLT 到 MDM 的模拟仅引入因子 $D$ 的额外填充。

#### 2. 去噪步数决定表达力层级

通过 PLT 等价性，论文将 MDM 的表达力与经典电路复杂度类建立了精确对应：

- **常数步 MDM = AC⁰**（**Corollary 3.3**）：$\mathsf{MDM}[\mathcal{O}(1), \mathsf{poly}(N)] = \mathsf{L\text{-}uniform\ }\mathsf{AC}^0$。这意味着仅用常数次去噪步无法超越标准 Transformer 的表达能力，解释了为何均匀随机解掩蔽的标准 MDM 受限于此。
- **多项式对数步 MDM = ACᵈ**（**Corollary 3.4**）：$\mathsf{MDM}[\mathcal{O}(\log^d N), \mathsf{poly}(N)] = \mathsf{L\text{-}uniform\ }\mathsf{AC}^d$。去噪步数从常数增加到多项式对数，表达力从 AC⁰ 向上逐级跃迁。
- **充分多步 MDM 收敛至 NC**：当步数足够多时，MDM 等价于所有可并行化问题类 NC。

**关键因果机制**：去噪步数 $T$ 和输出填充空间 $P$ 是控制表达力的核心变量。更多步数允许更深层的迭代推理，更大填充空间支持同时生成多个符号，二者共同使 MDM 从 AC⁰ 逐步提升至 NC。

#### 3. MDM 严格超越 Chain-of-Thought

论文证明了 MDM 相对于 CoT 的严格表达能力分离：

- **正则语言分离**（**Corollary 3.7**）：$\mathsf{CoT}[\log N] \subsetneq \mathsf{MDM}[\log N, N]$。$\mathcal{O}(\log N)$ 步的 MDM 能识别所有正则语言，而相同步数的 CoT 不能，构成严格包含关系。
- **相互模拟**：MDM 可模拟 pCoT（并行链式思考），但需平方级额外输出空间（**Theorem 3.3**：$\mathsf{pCoT}[T, P] \subseteq \mathsf{MDM}[T, P + (N+P)^2]$）；反之 pCoT 模拟 MDM 仅需线性层数膨胀（**Theorem 3.4**）。
- **多项式步 MDM 仍在 P 内**（**Theorem 3.5**）：$\mathsf{MDM}[\mathsf{poly}(N), \mathsf{poly}(N)] \subseteq \mathsf{CoT}[\mathsf{poly}(N)] \subseteq \mathsf{P}$，说明 MDM 不会突破多项式时间可计算的上界。

**Figure 1** 和 **Figure 2** 以可视化方式总结了上述包含/等价/严格分离关系：Figure 1 聚焦 MDM、PLT、CoT 三类模型间的表达力关系，Figure 2 展示 MDM 与 Reg、NC、ACᵈ、AC⁰ 等经典复杂度类的对应。

### 消融分析

论文通过理论构造而非实验进行了以下“消融”式分析：

#### 规划器策略的影响

- **均匀随机解掩蔽（标准 MDM）**：在完美近似假定下，标准 MDM 的表达式能力不超越 AC⁰（**Corollary 3.3** 的推论）。这是因为均匀解掩蔽无法按需选择先解哪些子问题，丧失了有向并行分解的能力。
- **规划器控制的非均匀解掩蔽**：通过引入可决定每步解掩蔽位置的规划器（**Definition B.15**），MDM 获得了按需分配计算资源的灵活性，这是实现并行效率增益的关键。规划器还可将已解掩蔽位置重新标记为需预测（重采样），允许修正先前错误，克服了传统 MDM 不可逆决策的限制。

#### 预测器因子化形式的影响

- **位置独立预测（标准 MDM 的 Eq. (1)）**：$\widehat{q}_{t-1|t}(\pmb w^{(t-1)} \mid \pmb w^{(t)}) = \prod_{n=1}^{N} \widehat{q}_{t-1|t}(\pmb w_n^{(t-1)} \mid \pmb w^{(t)})$ 按位置独立预测，虽支持并行生成但忽略位置间依赖，导致模型无法匹配简单分布。
- **基于完整上下文的条件预测**：理想化 MDM 的预测器（**Definition B.16**）不受位置独立限制，可基于完整上下文进行条件预测，从而规避因子化带来的表达力瓶颈。

#### 去噪步数的消融

| 去噪步数 | 表达力等价类 | 能否超越标准 Transformer |
|---------|------------|----------------------|
| $\mathcal{O}(1)$ | L-uniform AC⁰ | 否 |
| $\mathcal{O}(\log N)$ | 包含所有正则语言 | 是（严格超越 CoT） |
| $\mathcal{O}(\log^d N)$ | L-uniform ACᵈ | 是 |
| 充分多（polylog） | NC | 是（覆盖所有可并行化问题） |

**Figure 3** 以数学表达式求值为例直观说明了并行策略的效率优势：并行策略仅需 3 步计算中间值，而串行策略需 11 步逐符号生成。

### 失败模式与局限

#### 已知局限

1. **纯理论分析，无实验验证**：所有结论建立在有限精度对数宽度 Transformer 的理想化模型上，真实 MDM（受训练目标、注意力实现等约束）可能无法直接达到上述理论界限。
2. **模拟 CoT 的平方开销可能高估**：**Theorem 3.3** 中 MDM 模拟 pCoT 需 $P + (N+P)^2$ 的填充空间，论文未证明该上界是否紧致。若能通过非掩码自注意力的更高效因果掩码近似，该开销可能降至线性。
3. **规划器的学习是开放问题**：规划器与预测器是分开定义的理想化组件，实际训练中规划器的学习策略尚未解决。论文仅在附录 C.1 讨论了与 top-k 解掩蔽的联系，未提供训练算法。
4. **分析聚焦于确定性语言识别**：所有结论针对字符串识别（语言成员判定），未直接涉及概率分布建模或困惑度等语言建模指标，结论对生成任务的外推需谨慎。
5. **架构泛化性未知**：分析建立在有限精度 Transformer 上，对状态空间模型、RNN 等其他架构的泛化能力未探讨。

#### 待验证的开放问题

- 实际训练中能否学到有效近似理想规划器的策略？学习到的规划能否在真实任务上复现理论预期的并行效率？
- 在算术推理、代码生成、状态追踪等实际基准上，MDM 能否展现出相对于自回归模型的可测量并行效率增益？如何设计能凸显并行优势的评测任务？
- MDM 的并行推理能力是否有助于处理在线学习/交互式场景中的低延迟需求？

> **注意**：上述“失败模式”均来自论文自身的局限声明和开放问题讨论，非实验观察。若需实证层面的失败分析，需等待后续实验工作。

## 方法谱系与知识库定位

### 1. 理论框架定位：掩蔽扩散模型作为循环推理的并行实现

本文的核心理论贡献在于建立了**理想化掩蔽扩散模型（MDM）**与**填充循环Transformer（PLT）**之间的等价关系，从而将MDM的表达能力锚定在已知的电路复杂度层级中。这一等价性（推论3.1）是全文推理的枢纽：它使得MDM可以“继承”PLT已有的复杂性理论表征，同时揭示了去噪过程的迭代解掩蔽天然映射到循环推理，而同时生成多个符号的能力使其比逐符号的链式思考（CoT）更高效。

具体而言，MDM与PLT的相互模拟关系由定理3.1给出：

$$\mathsf{MDM}[T, P] \subseteq \mathsf{PLT}[T, P] \quad \text{且} \quad \mathsf{PLT}[T, P] \subseteq \mathsf{MDM}[T, (N+P)D]$$

其中PLT到MDM的模拟引入了因子$D$（模型宽度）的额外填充。在忽略对数因子的填充长度下，两者等价（推论3.1）：

$$\mathsf{MDM}[T, \widetilde{\mathcal{O}}(N^K)] = \mathsf{PLT}[T, \mathcal{O}(N^K)]$$

这一等价关系是理解MDM表达能力上界和下界的钥匙。

### 2. 与自回归推理范式的关系：超越顺序性瓶颈

MDM与**Chain-of-Thought（CoT）Transformer**（Wei et al., 2022）的关系是本文的另一条主线。自回归语言模型在CoT推理中存在根本性的“顺序性瓶颈”（sequentiality bottleneck）：即使问题可分解为相互独立的子问题，模型仍需逐符号生成，导致推理步数与问题规模线性相关，无法加速求解。

本文通过严格的理论包含关系证明了MDM在可并行化问题上具有严格更高的推理效率：

- **MDM可模拟pCoT**（并行链式思考，Theorem 3.3）：$\mathsf{pCoT}[T, P] \subseteq \mathsf{MDM}[T, P + (N+P)^2]$，但模拟需要平方级额外输出空间。
- **pCoT可模拟MDM**（Theorem 3.4）：$\mathsf{MDM}[T, P] \subseteq \mathsf{pCoT}[T, L T (P+N)]$，模拟仅需线性层级膨胀。
- **严格表达能力分离**（Corollary 3.7）：$\mathsf{CoT}[\log N] \subsetneq \mathsf{MDM}[\log N, N]$，即$O(\log N)$步的MDM能识别所有正则语言，而同步数的CoT无法做到。

这一分离的深层原因在于：MDM的迭代解掩蔽过程天然支持并行生成多个符号，而CoT的逐符号生成模式使其在固定步数内只能处理有限长度的上下文依赖。

### 3. 与标准掩蔽扩散模型的关键差异

本文提出的理想化MDM与**标准掩蔽扩散模型（Uniform Unmasking）**有两个关键设计差异，这些差异直接决定了表达能力的跃升：

| 组件 | 标准MDM（基线） | 本文理想化MDM（改进） |
|------|----------------|---------------------|
| **解掩蔽策略** | 均匀随机选择位置解掩蔽 | 由规划器（planner）决定每步解掩蔽哪些位置，支持确定/非均匀规划 |
| **反向过程因子化** | 逐位置独立预测（Eq. (1)），忽略位置间依赖 | 预测器可基于完整上下文进行条件预测，不限定位置独立 |
| **重采样能力** | 仅允许从掩码到非掩码，不可修改已生成符号 | 规划器可将已解掩蔽位置重新标记为需预测，允许修正先前错误 |

这些设计松弛直接突破了标准MDM的表达力上限。论文指出，在均匀解掩蔽和完美近似的假设下，标准MDM不能超越$\mathsf{AC}^0$（即标准Transformer的表达能力）。而引入非均匀规划器后，常数步去噪仍受限于$\mathsf{AC}^0$（推论3.3），但增加去噪步数可将表达能力从$\mathsf{AC}^0$提升到$\mathsf{AC}^d$（推论3.4），并最终收敛至并行问题类$\mathsf{NC}$。

### 4. 适用边界与核心局限

本文的结论建立在严格的理想化假设之上，适用边界清晰但受限：

**理论假设的脆弱性：**
1. **有限精度对数宽度Transformer框架**：所有结论基于该特定计算模型，对于其他架构（如状态空间模型SSM、RNN）的泛化能力未知。
2. **规划器与预测器的理想分离**：规划器被定义为可任意选择解掩蔽位置的神谕组件，实际训练中规划器的学习是开放问题。论文仅在附录C.1讨论了与top-k解掩蔽的联系，但未提供训练算法。
3. **完美近似假定**：分析假定预测器能完美拟合反向过程的条件分布，真实MDM的训练目标（如去噪得分匹配）可能无法达到该界限。

**结论外推的谨慎性：**
- 分析聚焦于**确定性字符串识别**（语言成员判定），未直接涉及概率分布建模或困惑度等语言建模指标，结论对生成任务的外推需谨慎。
- 模拟CoT时引入的**平方级额外输出空间**（Theorem 3.3）可能高估实际开销，论文未证明该上界是否紧致。
- 本文为**纯理论分析**，未包含任何实证实验；所有“结果”均为定理、推论及复杂性包含/分离关系的形式化证明，评估“优劣”的基准是表达能力类而非实验指标。

### 5. 开放问题与未来方向

论文明确指出了若干待解决问题，这些构成了该方向后续研究的关键路径：

1. **规划器的可训练性**：如何实际训练一个能有效近似理想规划器的MDM？学习到的规划策略能否在真实任务上复现理论上预期的并行效率？这是从理论到实践的核心鸿沟。

2. **模拟效率的紧致性**：Theorem 3.3中模拟CoT所需的平方输出空间能否通过更高效的非因果掩码注意力机制降低到线性？非掩码自注意力是否存在更优的因果掩码近似？

3. **实证基准设计**：在NLP实际基准（如状态追踪state-tracking、算术推理、代码生成）上，MDM能否展现出相对于自回归模型的可测量并行效率增益？如何设计能够凸显并行优势的评测任务？

4. **低延迟场景的潜力**：MDM的并行推理能力是否有助于处理在线学习/交互式场景中的低延迟需求？

5. **架构泛化**：能否将MDM的复杂性分析从有限精度Transformer推广到其他实用架构（如状态空间模型）？

## 原文 PDF

![[paperPDFs/ICLR_2026/On_the_Reasoning_Abilities_of_Masked_Diffusion_Language_Models.pdf]]
