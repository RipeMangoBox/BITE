---
title: "Test-Time Training with KV Binding Is Secretly Linear Attention"
type: paper
paper_level: A
venue: ICML
year: 2026
pdf_ref: paperPDFs/ICML_2026/Test_Time_Training_with_KV_Binding_Is_Secretly_Linear_Attention.pdf
project_link: https://research.nvidia.com/labs/sil/projects/tttla/
aliases:
- TALATL
- TTTKBISLA
tags:
- ICML_2026
- topic/benchmarks_datasets_evaluation
- topic/benchmarks_datasets_evaluation/benchmark_eval
core_operator: "将内循环的梯度更新显式表达为状态矩阵的累加，揭示了TTT就是线性注意力；这一视角允许安全地移除动量、权重归一化等复杂组件，并实现并行计算。"
primary_logic: "任何具有线性最终层的TTT架构都可以等价地重写为学习到的线性注意力算子，从而统一解释梯度上升、查询替换等反直觉现象，并提供架构简化和加速的理论基础。"
claims:
- "增加内循环优化步骤反而降低下游任务性能，违背记忆假说。"
- "用梯度上升替代梯度下降对内循环进行更新，性能保持不变甚至略有提升。"
- "将查询 Q 替换为键 K 几乎不影响模型性能，说明内循环并非执行基于相似度的检索。"
- "理论推导证明，内循环的单步或多步梯度更新（含动量）均可表达为线性注意力形式。"
---

# Test-Time Training with KV Binding Is Secretly Linear Attention

> [!tip] 核心洞察
> 任何具有线性最终层的TTT架构都可以等价地重写为学习到的线性注意力算子，从而统一解释梯度上升、查询替换等反直觉现象，并提供架构简化和加速的理论基础。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 基于键值绑定的测试时训练实际上是线性注意力 |
| 英文题名 | Test-Time Training with KV Binding Is Secretly Linear Attention |
| 会议/期刊 | ICML 2026 |
| Links | [paper](https://arxiv.org/abs/2602.21204); [Project](https://research.nvidia.com/labs/sil/projects/tttla/) |
| Topic | #topic/benchmarks_datasets_evaluation #topic/benchmarks_datasets_evaluation/benchmark_eval |
| Method | TTT as Linear Attention (TTT-LA) |
| Dataset | LaCT-LLM (Book-3 2.5B tokens), LaCT-NVS (RealEstate10K), TTT Layer Inference (LLM throughput) |

> [!tip] 效果简介
> - LaCT-LLM (Book-3 2.5B tokens) 上，Perplexity ↓ 为 16.80，对比 16.43，变化 +0.37。
> - LaCT-NVS (RealEstate10K) 上，PSNR ↑ 为 25.73，对比 25.94，变化 -0.21。
> - TTT Layer Inference (LLM throughput) 上，Tokens per Second 为 124.6M (并行实现)，对比 ≈ 31M (原始递归实现)，变化 ~4.0×。

## 概述

测试时训练（Test-Time Training, TTT）作为一种新兴的序列建模范式，其核心假设是：内循环通过记忆键值对（Key-Value Binding）来存储历史信息，并在推理时基于查询相似度进行检索。然而，本文通过系统的实证分析与理论推导，**从根本上颠覆了这一“存储-检索”假说**。

本文的核心发现是：**TTT的内循环并非执行键值记忆存储与检索，而是诱导了一个可学习的查询-键-值混合机制，其数学本质是线性注意力（Linear Attention）**。具体而言，当内循环的梯度更新被显式表达为状态矩阵的累加时，TTT的输出可以被等价地重写为一个学习到的线性注意力算子。这一视角统一解释了多个反直觉的实验现象——包括增加内循环优化步数反而降低下游任务性能、用梯度上升替代梯度下降性能保持不变、以及将查询替换为键几乎不影响模型表现——并为TTT架构的简化与加速提供了理论基础。

基于上述洞察，本文提出 **TTT as Linear Attention (TTT-LA)**，通过逐步消融将复杂的TTT架构（如LaCT、ViTTT）简化为标准线性注意力。消融轨迹表明，移除动量、权重归一化、梯度正交化等组件后，模型性能衰减极小（LLM困惑度仅上升0.37，新视角合成PSNR仅下降0.21），同时推理吞吐量提升约4倍。这一简化不仅揭示了TTT中各组件的真实贡献，更使得完全并行的状态更新成为可能。

**方法定位**：本文属于模型分析与架构简化工作，通过揭示TTT与线性注意力之间的等价关系，为理解测试时训练的内在机制提供了新的理论框架，并为高效序列建模架构的设计指明了方向。

## 背景与动机

### 测试时训练的内循环：从记忆假说到线性注意力

测试时训练（Test-Time Training, TTT）通过在每个测试样本上执行内循环优化，使模型参数适应输入分布。其中，基于键值绑定（Key-Value Binding, KVB）的 TTT 变体（TTT-KVB）将内循环建模为键到值的映射学习：给定从输入序列中投影得到的键 $k$ 和值 $v$，内循环最小化均方误差损失

$$\mathcal{L} = \| f_{\theta}(k) - v \|^2$$

使模型 $f_{\theta}$ 学会将键映射到对应的值。这一范式被广泛解释为一种记忆机制——内循环通过梯度下降将键值对“存储”到快速权重中，推理时再通过查询进行检索。

然而，这一直觉性的“存储-检索”解释在实证检验下暴露出根本性矛盾。如图 1 所示，增加内循环优化步数虽然持续降低内损失，却一致地恶化下游任务性能。若内循环确实在执行记忆存储，更多优化步骤理应带来更准确的检索，从而提升任务表现。这一反直觉现象直接挑战了记忆假说的有效性。

更令人意外的是，两项关键操作对任务性能几乎不产生影响（表 1）：将内循环的梯度下降替换为梯度上升，性能保持不变甚至略有提升——这从根本上颠覆了“存储”的解释，因为梯度上升显然不是在存储键值对；将查询 $Q$ 替换为键 $K$，性能同样几乎不受影响——这动摇了“检索”的解释，因为基于相似度的检索要求查询与键具有语义对应关系。此外，t-SNE 可视化（图 2）揭示查询与键的分布存在显著不对称，意味着内循环在分布外进行评估，无法执行可靠的相似度检索。

### 核心洞察：TTT 内循环的线性注意力本质

上述反直觉现象指向一个更深层的机制：TTT 的内循环并非进行显式的键值记忆存储与检索，而是诱导了一个可学习的查询-键-值混合机制，其数学本质是线性注意力。当内循环仅包含单层线性变换时，TTT 可直接重写为线性注意力算子。更关键的是，即使内循环采用多层 MLP、动量、权重归一化等复杂组件，其梯度更新仍可表达为状态矩阵的累加过程，等价于线性注意力中键值外积的累积。

这一视角统一解释了所有反直觉现象：梯度上升之所以有效，是因为它仅改变了状态矩阵更新的符号，而线性注意力的核心在于键值外积的累积结构，更新方向并非本质；查询替换之所以不影响性能，是因为内循环并未执行基于查询-键相似度的检索，而是通过学习到的核函数对查询和键进行非线性变换后直接混合。

### 从重新解释到架构简化

将 TTT 重新解释为线性注意力不仅提供了理论统一性，更带来了直接的工程收益。由于线性注意力天然支持并行计算，这一等价性使得原本必须递归执行的 TTT 内循环可以完全并行化。同时，该视角揭示了许多被广泛采用的 TTT 设计组件——动量、权重归一化、梯度正交化、逐 token 学习率——在键和值均可学习的条件下是功能冗余的，可被安全移除而不显著损害性能。这为构建更简洁、更高效的序列建模架构奠定了理论基础。

## 核心创新

本文的核心创新在于**揭示了测试时训练（TTT）的数学本质**，并据此对现有复杂架构进行了**极简重构**。具体而言，作者通过理论证明，任何具有线性最终层的 TTT 内循环都等价于一个可学习的线性注意力算子，从而将 TTT 从“键值记忆存储与检索”的认知框架中彻底解放出来。

基于这一洞察，论文对两种代表性的 TTT 架构——**LaCT**（Zhang et al., 2025）和 **ViTTT**（Han et al., 2025）——进行了系统性的组件消融，将原本包含多层 MLP、动量、权重归一化、梯度正交化等复杂设计的 TTT 层，逐步简化为标准线性注意力。这一简化过程揭示了各设计组件的真实贡献，并最终得到了一个性能衰减极小、但可完全并行化的极简版本。

### 关键组件变更

下表总结了从原始 TTT 架构到简化线性注意力版本的核心变更点：

| 组件 | 原始设计（LaCT / ViTTT） | 简化设计（TTT-LA） | 变更依据 |
|------|--------------------------|-------------------|----------|
| 更新的参数范围 | 所有内循环参数（W₀, W₁, W₂） | 仅最后一层线性矩阵（W₁） | 实验表明仅更新最后一层在所有任务上取得最佳性能（Table 2, Variant 1） |
| 权重归一化 | 每次更新后应用通道级 ℓ₂ 归一化 | 完全移除 | 移除后性能几乎无影响，且是实现并行化的关键前提（Table 2, Variant 2） |
| 内循环架构 | 多层 SwiGLU MLP | 单层线性变换 | 理论证明多层非线性可被吸收为核函数 φ，简化为单层线性后性能衰减极小（Table 2, Variant 3） |
| 逐 token 学习率 | 可学习的逐 token 学习率 | 固定学习率（被值向量吸收） | 理论分析表明逐 token 学习率在功能上是冗余的，可被吸收到可学习的值向量中（Section 6.1, Step 4） |
| 动量 | 使用 SGD 动量 | 移除 | 动量仅改变有效值向量的加权方式，在键和值均可学习时未提供有意义的增益（Table 2, Variant 5） |
| 梯度正交化 | 应用 Muon 正交化（LaCT）/ 梯度归一化（ViTTT） | 移除 | 在线性注意力框架下，梯度正交化等价于对状态更新施加算子，移除后性能基本不变（Table 2, Variant 6） |

### 简化后的核心形式

经过上述消融后，TTT 内循环退化为如下标准线性注意力算子：

$$o = q \big( \boldsymbol{W} + \sum_i \boldsymbol{k}_i^{\top} \boldsymbol{v}_i \big)$$

其中 $q$、$k$、$v$ 分别为查询、键、值向量，$W$ 为初始状态矩阵。这一形式不仅消除了原始 TTT 中递归更新的串行依赖，还使得整个层可以完全并行计算，从而在推理吞吐量上实现了约 4 倍的提升（Table 2, 124.6M tokens/s vs. ~31M tokens/s）。

### 创新的理论根基

上述简化的理论根基在于三个核心定理（Theorem 5.1–5.3），它们共同证明了：

1. **单步更新等价性**：内循环的单步梯度更新可表达为 $o = \phi_{t+1}(q) \left( W_t + \phi_t(k)^{\top} g_t(k) \right)$，即查询-键-值的线性注意力形式。
2. **序列展开等价性**：将内循环沿序列展开后，输出为 $o_t = \hat{q}_t \left( S_0 + \sum_{i=0}^{t} \hat{k}_i^{\top} \hat{v}_i \right)$，即扩展的线性注意力。
3. **动量吸收**：带动量的梯度下降仅将有效值向量变为历史梯度的动量加权和 $\hat{v}_i = m_i(k_i) \triangleq g_i(k_i) \cdot \sum_{j=i}^{t} \beta_i^j$，不改变线性注意力的本质结构。

这些定理共同揭示了一个根本性洞察：**TTT 的内循环并非在进行键值记忆的存储与检索，而是在诱导一个可学习的、历史依赖的查询-键-值混合机制**。这一认知重构使得安全地移除动量、权重归一化等复杂组件成为可能，并为 TTT 架构的简化与加速提供了坚实的理论基础。

## 整体框架

### 核心洞察：TTT 即线性注意力

本文的核心洞察是，任何具有线性最终层的测试时训练（TTT）架构，其内循环在数学上等价于一个可学习的线性注意力算子。这一视角颠覆了传统“键值记忆存储与检索”的解释，将 TTT 统一到线性注意力的理论框架之下。该等价性不仅解释了梯度上升、查询替换等反直觉现象，还为架构简化和并行加速提供了理论基础。

### 整体 Pipeline 概览

论文所揭示的 TTT 等价线性注意力 pipeline 由四个核心模块串联构成，其输入输出流如下：

1.  **Token 投影（Token Projection）**：输入序列的每个 token 被映射为三组表示——查询 $Q$、键 $K$ 和值 $V$。这是所有 Transformer 类架构的标准起点。

2.  **核函数 $\phi$（Kernel Function）**：对 $Q$ 和 $K$ 施加一个（可学习的）静态非线性变换 $\phi(\cdot)$，生成有效查询 $\hat{q} = \phi(q)$ 和有效键 $\hat{k} = \phi(k)$。该核函数的具体形式取决于内循环更新的参数范围（见下文“关键设计选择”）。

3.  **状态矩阵累积（State Matrix Accumulation）**：这是 TTT 内循环的核心。传统理解中，内循环通过梯度下降将键值对“存储”进快速权重矩阵 $W$。本文证明，这一过程等价于线性注意力中的**状态更新**——将键值外积 $\hat{k}_i^\top \hat{v}_i$ 累加到一个可学习的状态矩阵 $S$ 中：
    $$S_t = S_0 + \sum_{i=0}^{t} \hat{k}_i^\top \hat{v}_i$$
    其中初始状态 $S_0$ 对应内循环的初始权重 $W_0$，有效值向量 $\hat{v}_i$ 由原始值 $v_i$ 和梯度信号共同决定。

4.  **输出计算（Output Computation）**：将当前查询 $\hat{q}_t$ 与累积后的状态矩阵 $S_t$ 相乘，得到最终输出：
    $$o_t = \hat{q}_t \cdot S_t$$
    这正是标准线性注意力的输出形式。

### 关键设计选择：单层 vs. 多层更新

Pipeline 中一个决定性的设计选择是**内循环更新的参数范围**，它直接影响核函数 $\phi$ 的性质：

-   **仅更新最后一层参数（最优选择）**：当内循环仅更新线性最终层的权重矩阵 $W_1$ 时，核函数 $\phi$ 变为**静态且可学习的**。这意味着 $\phi(q)$ 和 $\phi(k)$ 仅依赖于各自的输入，不随内循环状态变化。消融实验表明，这种配置在语言建模、新视角合成和图像识别三个任务上均取得**最佳性能**（Table 2, Variant 1），同时为后续的并行化铺平了道路。

-   **更新所有内循环参数**：当更新包括非线性层在内的所有参数时，核函数 $\phi_t$ 变为**动态的**——它依赖于当前内循环权重 $W_t$，因此 $\phi_t(q)$ 和 $\phi_t(k)$ 会随序列位置变化。这增加了表达能力，但引入了顺序依赖性，阻碍并行计算。

### 从复杂到简洁：组件消融路径

基于上述 pipeline，论文通过一条严格的消融路径，将复杂的 TTT 架构逐步简化为标准线性注意力。该路径量化了每个设计组件的实际贡献：

| 消融步骤 | 移除/简化的组件 | 对性能的影响 | 置信度 |
|:---|:---|:---|:---:|
| Step 1 | 仅更新最后一层参数 | **性能提升**（三项任务均达最优） | 高 |
| Step 2 | 权重归一化 | 几乎无影响 | 高 |
| Step 3 | 多层 MLP → 单层线性变换 | 轻微下降 | 高 |
| Step 4 | 逐 token 可学习学习率 | 无影响（被值向量吸收） | 中高 |
| Step 5 | 动量 | 无有意义增益 | 中高 |
| Step 6 | 梯度正交化/归一化 | 基本无影响 | 高 |

经过上述全部消融后，LaCT 和 ViTTT 均退化为如下标准线性注意力形式：
$$o = q \big( \boldsymbol{W} + \sum_i \boldsymbol{k}_i^\top \boldsymbol{v}_i \big)$$

此时，模型在语言建模上的困惑度仅从 16.43 升至 16.80（+0.37），在新视角合成上的 PSNR 从 25.94 降至 25.73（-0.21），性能衰减极小，却换来了**约 4 倍的推理吞吐量提升**（从 ~31M tokens/s 提升至 124.6M tokens/s，Table 2）。

### 并行化实现

移除权重归一化（Step 2）后，状态矩阵的累积过程不再依赖于顺序更新，整个 TTT 层得以实现完全并行化。并行实现利用前缀和算法一次性计算所有位置的状态矩阵，在训练中实现了 **1.19 倍的端到端加速**，同时保持了与原始递归形式相当的收敛曲线（Figure 4）。

### 适用范围与局限

> 需注意，上述等价性和简化路径的严格证明依赖于**内循环具有线性、无偏置最终层**的假设。对于最终层为非线性的 TTT 变体，其是否能表达为某种广义线性注意力，仍是待解决的开放问题。实证验证目前仅覆盖 LaCT 和 ViTTT 两种架构，在其他 TTT 变体（如 Titans、Atlas）上的推广性尚待检验。

## 核心模块与公式推导

### 工作流模块

本文的核心贡献在于揭示 TTT-KVB（Test-Time Training with Key-Value Binding）的内循环并非执行显式的键值记忆存储与检索，而是诱导了一个可学习的线性注意力算子。基于此视角，整个架构可被解构为以下关键模块：

1. **Token 投影**：将输入序列映射为查询 $\boldsymbol{Q}$、键 $\boldsymbol{K}$ 和值 $\boldsymbol{V}$ 三个表示空间（Section 3）。
2. **核函数 $\phi$**：对 $\boldsymbol{Q}$ 和 $\boldsymbol{K}$ 施加静态非线性变换，生成有效的查询和键表示。当内循环仅更新最后一层参数时，$\phi$ 退化为一个静态的可学习核函数；若更新所有参数，则 $\phi_t$ 变为一个随内循环步数演化的动态核（Section 6.1, Step 1）。
3. **状态矩阵累积**：内循环通过梯度下降将键值外积 $\phi_i(k_i)^\top g_i(k_i)$ 累加到状态矩阵 $\boldsymbol{W}$ 中，等价于线性注意力的状态更新过程（Theorem 5.1, Section 5.3）。
4. **输出计算**：将更新后的状态矩阵与有效查询 $\phi_{t+1}(q_t)$ 相乘，得到最终输出，等价于线性注意力算子的前向传播（Theorem 5.1, Section 5.3）。

### 核心公式推导

#### 内循环键值绑定损失

TTT-KVB 的内循环优化目标为最小化模型输出与目标值向量之间的均方误差：

$$\mathcal{L} = \| f_{\theta}(k) - v \|^2$$

其中 $f_{\theta}$ 为内循环模型，$k$ 为键，$v$ 为对应的值向量（Section 3）。这一损失函数是后续所有理论推导的起点。

#### 单步更新下的线性注意力等价性（Theorem 5.1）

当内循环模型 $f_{\theta}$ 具有线性、无偏置的最终层时（即 $f(x) = \phi(x; \Theta)\boldsymbol{W}$），单步梯度更新后的输出可表达为：

$$o = \phi_{t+1}(q) \left( \boldsymbol{W}_t + \phi_t(k)^\top g_t(k) \right)$$

其中：
- $\phi_{t+1}(q)$ 为有效查询向量；
- $\phi_t(k)$ 为有效键向量；
- $g_t(k)$ 为损失对 $\boldsymbol{W}$ 的瞬时梯度，充当有效值向量的角色。

该式表明，TTT 内循环的单步更新本质上执行的是线性注意力操作：状态矩阵 $\boldsymbol{W}_t$ 上累加了一个键值外积项 $\phi_t(k)^\top g_t(k)$，输出为查询与更新后状态矩阵的乘积。

#### 序列累积的扩展线性注意力（Theorem 5.2）

将上述单步更新沿序列展开，得到处理整个序列后的输出形式：

$$o_t = \phi_{t+1}(q_t) \left( \boldsymbol{W}_0 + \sum_{i=0}^{t} \phi_i(k_i)^\top g_i(k_i) \right)$$

这等价于扩展线性注意力的一般形式：

$$o_t = \hat{q}_t \left( \boldsymbol{S}_0 + \sum_{i=0}^{t} \hat{k}_i^\top \hat{v}_i \right)$$

其中 $\boldsymbol{S}_0 = \boldsymbol{W}_0$ 为初始状态矩阵，$\hat{q}_t = \phi_{t+1}(q_t)$，$\hat{k}_i = \phi_i(k_i)$，$\hat{v}_i = g_i(k_i)$。

#### 带动量的梯度下降（Theorem 5.3）

当内循环使用 SGD 动量时，有效值向量变为历史梯度的动量加权和：

$$\hat{v}_i = m_i(k_i) \triangleq g_i(k_i) \cdot \sum_{j=i}^{t} \beta_i^j$$

其中 $\beta_i^j$ 为动量因子的累积乘积：

$$\beta_i^j \triangleq \begin{cases} \prod_{s=i+1}^{j} \alpha_s, & \text{if } i < j \\ 1, & \text{otherwise} \end{cases}$$

$\alpha_s$ 为第 $s$ 步的动量系数。此时 TTT 输出仍保持线性注意力形式：

$$o_t = \phi_{t+1}(q_t) \left( \boldsymbol{W}_0 + \sum_{i=0}^{t} \phi_i(k_i)^\top m_i(k_i) \right)$$

动量仅改变了有效值向量的构成方式，并未破坏线性注意力的数学结构。

#### 简化后的标准线性注意力

通过逐项消融（移除动量、权重归一化、梯度正交化等），TTT 最终退化为标准线性注意力算子（Section 6.1, Step 6）：

$$o = q \big( \boldsymbol{W} + \sum_i \boldsymbol{k}_i^\top \boldsymbol{v}_i \big)$$

其中 $\boldsymbol{W}$ 为可学习的初始状态矩阵，$\sum_i \boldsymbol{k}_i^\top \boldsymbol{v}_i$ 为序列中所有键值外积的累加。这一极简形式在 LaCT-LLM 上仅带来 +0.37 的困惑度损失（Table 2），却获得了约 4 倍的推理吞吐量提升（124.6M tokens/s vs. ~31M tokens/s）。

## 实验与分析

### 反直觉现象：内循环并非键值存储与检索

在深入消融实验之前，本文首先通过一系列受控实验揭示了TTT内循环中若干与“记忆假说”根本矛盾的现象，为后续的理论重构提供了直接的实证动机。

**增加内循环步数反而损害任务性能。** 若TTT内循环确实在存储键值对，那么更充分的优化（更多步数）理应带来更好的存储效果，进而提升下游任务性能。然而，**Figure 1** 显示了一个截然相反的规律：随着内循环优化步数从1增加到5，内损失持续下降（表明“记忆”更充分），但下游任务性能却单调恶化。这一现象在LaCT的LLM任务上表现尤为显著，直接推翻了“内循环=记忆存储”的朴素解释。

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2602_21204/figures/001_Figure_1.jpg]]
*Figure 1: Inner-Loop Optimization vs. Performance. Increasing inner-loop iterations improves inner-loop loss but degrades task performance, contradicting the memorization-based interpretation of TTT. Experiments are based on LaCT (Zhang et al., 2025)*

**梯度上升与梯度下降性能相当。** 若内循环执行的是键值存储，反转梯度方向（即梯度上升）应破坏存储过程，导致性能崩溃。然而，**Table 1** 的数据表明，将内循环的梯度下降替换为梯度上升后，模型性能不仅没有崩溃，反而与基线保持相当甚至略有提升（LaCT-LLM困惑度：16.19 vs. 基线16.43）。这说明内循环的更新方向并非关键，其真正作用并非“存储”。

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2602_21204/figures/002_Table_1.jpg]]
*Table 1: Observations Contradicting the Storage-and-Retrieval Interpretation of TTT. Replacing gradient descent with ascent breaks the storage interpretation, and replacing queries with keys breaks the retrieval interpretation, yet task performance remains mostly unchanged. Experiments are base on LaCT (Zhang et al., 2025) and ViTTT (Han et al., 2025)*

**查询替换为键几乎不影响性能。** 在标准的存储-检索框架中，查询用于从已存储的键值对中检索相关信息，因此查询与键的语义匹配至关重要。然而，**Table 1** 显示，将查询 $Q$ 直接替换为键 $K$ 后，模型性能几乎不变（LaCT-LLM困惑度：16.18 vs. 基线16.43）。**Figure 2** 的 t-SNE 可视化进一步揭示了这一现象的结构性原因：在预训练的LaCT模型中，$Q$ 与 $K$ 的分布存在显著且一致的不对称性——内循环实际上是在分布外被评估的，因此从未真正执行过可靠的检索操作。

上述三个反直觉现象共同指向一个核心结论：TTT内循环的键值绑定过程并非存储与检索，而是一种结构化的、历史依赖的查询-键-值混合机制。

---

### 消融轨迹：从复杂TTT到标准线性注意力

基于理论分析（定理5.1–5.3），本文设计了一条系统性的消融路径，逐步将复杂的TTT架构简化为标准线性注意力算子。消融实验在三个任务上展开：LaCT-LLM（语言建模，760M参数，100B tokens训练）、LaCT-NVS（新视角合成，114M参数）和ViTTT-B（图像分类，90M参数，ImageNet-1K）。完整结果见 **Table 2**。

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2602_21204/figures/005_Table_2.jpg]]
*Table 2: Ablation Trajectory Reducing TTT to Standard Linear Attention. By progressively simplifying complex TTT formulations into standard linear attention (Variant 6), we quantify the contribution of each design component in TTT. Variant 1 achieves the best performance across all three tasks. Variants 2–6 admit parallel implementations. We additionally report the inference throughput of each variant’s TTT layer on the LLM task. † denotes ablations that do not apply, in which case performance matches the preceding variant. * indicates that ViTTT does not use gradient orthogonalization, so we ablate gradient normalization instead*

**Step 1：仅更新最后一层参数。** 将内循环的更新范围从所有参数（$W_0, W_1, W_2$）限制为仅最后一层线性矩阵 $W_1$。这一修改不仅没有损害性能，反而在全部三个任务上取得了**最佳结果**（LaCT-LLM困惑度15.93，LaCT-NVS的PSNR 25.97，ViTTT Top-1准确率79.63%）。这表明内循环中其他参数的更新是冗余的，且当仅更新最后一层时，核函数 $\phi$ 从动态变为静态可学习函数，计算效率显著提升。

**Step 2：移除权重归一化。** 在Step 1的基础上移除每次更新后的通道级 $\ell_2$ 归一化。**Table 2** 显示，这一修改对性能几乎无影响（LaCT-LLM困惑度从15.93变为15.93，LaCT-NVS的PSNR从25.97变为25.97），但带来了一个关键收益：TTT的公式变为完全可并行化，为后续的推理加速奠定了基础。

**Step 3：多层MLP简化为单层线性变换。** 将LaCT中的SwiGLU MLP和ViTTT中的门控线性单元替换为单层线性变换。这一简化使模型更接近标准线性注意力的形式，性能仅有轻微下降（LaCT-LLM困惑度：16.05，LaCT-NVS PSNR：25.84）。

**Step 4：移除逐token学习率。** 原TTT使用可学习的逐token学习率来缩放内循环更新。理论分析表明，在Frobenius内积作为内损失的情况下，该学习率可被吸收到可学习的值向量 $v_t$ 中，功能上是冗余的。消融结果证实了这一判断：移除后性能基本不变。

**Step 5：移除动量。** 带动量的SGD更新在TTT中仅改变有效值向量 $\hat{v}$ 的形式——从瞬时梯度 $g_t(k)$ 变为历史梯度的动量加权和 $m_i(k_i) \triangleq g_i(k_i) \cdot \sum_{j=i}^{t} \beta_i^j$。当键和值均可学习时，动量没有提供有意义的增益，移除后性能几乎无变化。

**Step 6：移除梯度正交化/归一化。** LaCT使用Muon正交化 $M(\Delta W)$ 处理梯度更新，在本文的线性注意力重写下，这等价于对状态更新施加一个算子 $M(k^\top v)$。ViTTT则使用梯度归一化。消融显示，移除这些操作后性能基本保持不变（LaCT-LLM困惑度：16.80，LaCT-NVS PSNR：25.73）。

经过上述六步消融后，LaCT和ViTTT均精确退化为标准线性注意力算子：

$$o = q \big( \boldsymbol{W} + \sum_i \boldsymbol{k}_i^\top \boldsymbol{v}_i \big)$$

**性能差距极小。** 对比原始LaCT与消融后的Variant 6：LLM任务困惑度仅增加0.37（16.43→16.80），NVS任务PSNR仅下降0.21 dB（25.94→25.73）。**Figure 3** 展示了LaCT-LLM消融过程中的困惑度变化曲线，进一步印证了各组件贡献的微小性。

---

### 并行化与推理加速

移除权重归一化后的TTT变体（Variant 2及之后）具备完全并行化的能力。本文将并行化实现与原始递归实现进行了对比：

- **推理吞吐量**：在LLM任务上，Variant 6的并行实现达到**124.6M tokens/秒**，约为原始递归实现（约31M tokens/秒）的**4.0倍**（**Table 2**）。
- **训练加速**：**Figure 4** 比较了原始LaCT-TTT与Variant 2并行形式在训练过程中的损失-时间曲线。并行形式实现了**1.19倍**的端到端训练加速，同时保持了相当的收敛质量。

---

### 失败模式与局限

尽管消融实验证明了TTT可安全简化为线性注意力，但需注意以下边界条件：

1. **非线性最终层的限制**：本文的理论分析（定理5.1–5.3）严格依赖于内循环具有线性、无偏置的最终层。当最终层为非线性时，线性注意力等价性尚未建立。**此点需手动验证**——若目标TTT变体使用非线性最终层，本文的简化路径可能不适用。

2. **架构覆盖范围有限**：实证验证仅涵盖LaCT（Zhang et al., 2025）和ViTTT（Han et al., 2025）两种架构。对于其他TTT变体（如Titans、Atlas等），本文的结论尚未得到检验。

3. **权重归一化移除的代价**：完全并行化以移除权重归一化为前提，这在某些对状态稳定性要求极高的场景中可能影响性能。当前实验中该影响未显现，但在更大规模或更长序列的设置下需要进一步评估。

4. **超大尺度行为未知**：简化到标准线性注意力后的模型在千亿参数级别的行为尚不清楚，性能差距是否会随模型规模扩大而放大仍是一个开放问题。

## 方法谱系与知识库定位

### 与基线工作的关系

本文的核心贡献在于对测试时训练（Test-Time Training, TTT）中键值绑定变体（TTT-KVB）的数学本质进行了重新诠释，而非提出一种全新的架构。分析的直接对象是两个代表性的 TTT-KVB 基线：**LaCT**（Zhang et al., 2025）和 **ViTTT**（Han et al., 2025）。这两种架构均采用了复杂的快速权重参数化方案，包括多层 SwiGLU MLP、动量、权重归一化和梯度正交化等组件。本文的理论推导和消融实验表明，这些复杂的组件并非 TTT 有效性的根本来源——当逐项移除动量、权重归一化、梯度正交化，并将内循环架构从多层 MLP 简化为单层线性变换后，模型退化为标准线性注意力形式 $o = q (W + \sum_i k_i^\top v_i)$，而性能仅出现极小衰减（LaCT-LLM 困惑度从 16.43 升至 16.80，LaCT-NVS PSNR 从 25.94 降至 25.73；Table 2, Variant 6）。

这一发现将 TTT 重新定位于线性注意力家族的谱系中。TTT 的内循环并非执行传统意义上的键值记忆存储与检索，而是诱导了一个可学习的查询-键-值混合机制，其数学本质与 **Linear Attention**（Katharopoulos et al., ICML 2020）等经典线性注意力算子直接对应。定理 5.1 至 5.3 严格证明了：即使内循环包含多层非线性映射和动量，其单步更新、序列累积更新以及带动量的更新均可等价地重写为扩展的线性注意力形式。这一视角统一解释了若干反直觉的实验现象：梯度上升替代梯度下降后性能保持不变甚至略有提升（Table 1），以及将查询 $Q$ 替换为键 $K$ 几乎不影响模型性能（Table 1）——这些现象在“存储-检索”解释框架下完全无法理解，但在线性注意力视角下则成为自然推论。

### 适用边界

本文的分析和结论受限于以下边界条件：

1. **线性最终层假设**：所有理论推导依赖于内循环函数 $f_\theta$ 具有线性、无偏置的最终层。当最终层为非线性时，线性注意力的等价性尚未建立。论文明确指出，将这一洞察扩展到非线性最终层是一个待解决的开放问题。

2. **已验证的架构范围**：实证验证仅覆盖 LaCT 和 ViTTT 两种 TTT-KVB 变体，涵盖语言建模（LaCT-LLM, 760M 参数）、新视角合成（LaCT-NVS, 114M 参数）和图像识别（ViTTT-B, 90M 参数）三个任务。对于其他 TTT 变体（如 Titans、Atlas），论文仅进行了概念性讨论，尚未提供实验验证。

3. **并行化的代价**：完全并行化要求移除权重归一化（Section 6.1, Step 2），因为权重归一化的非结合性阻碍了状态矩阵的并行累积。在那些对状态稳定性有严格要求的场景中，这一移除可能影响性能。

4. **尺度限制**：消融实验在中等规模模型上进行（最大 760M 参数）。简化到标准线性注意力后的模型在超大尺度（如千亿参数）下的行为尚不清楚，性能差距可能随规模扩大而变化。

### 局限与开放问题

**已识别的局限**：

- 内循环优化步数增加虽然降低内损失，却持续恶化下游任务性能（Figure 1），这直接反驳了记忆假说，但论文未深入解释这一“过拟合”现象的深层原因。
- t-SNE 可视化揭示了 $Q$ 与 $K$ 之间显著且一致的分布不对称（Figure 2），说明内循环在分布外被评估，无法执行可靠的检索。然而，这种不对称性在线性注意力框架下的功能意义尚未被充分阐明。
- 逐 token 可学习学习率被证明是功能冗余的，可被值向量吸收（Section 6.1, Step 4），但这一吸收机制是否在所有任务中无损，仍需更广泛的验证。

**开放问题**：

1. **与 DeltaNet 等现代线性注意力的深层对应**：TTT 的内循环状态更新是否与 DeltaNet（Schlag et al., ICML 2021）等基于 delta 规则的线性注意力架构存在更深层的数学对应关系？
2. **非线性最终层的广义线性注意力**：能否设计一种带有非线性最终层但仍可表达为某种广义线性注意力的 TTT 架构？
3. **大规模下的性能差距**：在更大规模的模型上，简化线性注意力与完整 TTT 的性能差距是否会扩大？权重归一化等被移除的组件在大规模场景中是否具有不可替代的作用？
4. **权重归一化的近似替代**：权重归一化的非结合性是否可通过某种近似或替代方案克服，从而在保持状态稳定性的同时实现完全并行的状态更新？
5. **更广泛的 TTT 变体验证**：当 Titans 和 Atlas 等 TTT 变体的实现可用时，本文的线性注意力简化是否同样适用？

## 原文 PDF

![[paperPDFs/ICML_2026/Test_Time_Training_with_KV_Binding_Is_Secretly_Linear_Attention.pdf]]
