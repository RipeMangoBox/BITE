---
title: "It's All Just Vectorization: einx, a Universal Notation for Tensor Operations"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Its_All_Just_Vectorization_einx_a_Universal_Notation_for_Tensor_Operations.pdf
openreview_forum_id: QqvQ3iAdpC
aliases:
- ISAJVEUNTO
tags:
- ICLR_2026
- topic/benchmarks_datasets_evaluation
- topic/benchmarks_datasets_evaluation/benchmark_eval
core_operator: "将张量操作分解为基本操作与显式向量化表示，通过统一的声明式符号（einx）表达任意向量化模式。"
primary_logic: "所有张量操作本质上都是基本操作的向量化，因此可以用统一的符号系统解耦操作与向量化，将复杂API简化为少量基本操作。"
claims:
- "多种Numpy-like操作可归约为少数einx基本操作，如表1所示。"
- "einx支持的操作类别（包括串联、重复）远超einsum和einops，如表2所示。"
- "einx通过方括号区分向量化轴和基本操作轴，使表达式具有清晰的解释。"
- "einx.id (transpose) compilation overhead 上 time (ms) = 6.8 ± 1.3"
---

# It's All Just Vectorization: einx, a Universal Notation for Tensor Operations

> [!tip] 核心洞察
> 所有张量操作本质上都是基本操作的向量化，因此可以用统一的符号系统解耦操作与向量化，将复杂API简化为少量基本操作。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 一切皆向量化：einx——一种通用的张量运算符号 |
| 英文题名 | It's All Just Vectorization: einx, a Universal Notation for Tensor Operations |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=QqvQ3iAdpC); [GitHub](https://github.com/fferflo/einx) |
| Topic | #topic/benchmarks_datasets_evaluation #topic/benchmarks_datasets_evaluation/benchmark_eval |
| Method | einx |
| Dataset | einx.id (transpose) compilation overhead, einx.add (simple) compilation overhead, einx.add (with d=2) compilation overhead |

> [!tip] 效果简介
> - einx.id (transpose) compilation overhead 上，time (ms) 为 6.8 ± 1.3，对比 0.077 ± 0.003，变化 +6.723。
> - einx.add (simple) compilation overhead 上，time (ms) 为 9.3 ± 2.4，对比 0.077 ± 0.003，变化 +9.223。
> - einx.add (with d=2) compilation overhead 上，time (ms) 为 23.5 ± 3.1，对比 0.077 ± 0.003，变化 +23.423。

## 概述

现有Numpy-like张量框架（如NumPy、PyTorch）面临一个根本性瓶颈：API庞大且不一致，缺乏通用的向量化表示，导致代码难以阅读和编写，并频繁引发形状错误。例如，仅索引类操作就需要`torch.take`、`torch.gather`、`torch.index_select`等多个函数来处理不同的向量化模式。

einx的核心洞察是：**所有张量操作本质上都只是基本操作的向量化**。基于这一认识，einx提出了一套统一的声明式符号系统，通过方括号显式区分传递给基本操作的轴与向量化轴，将复杂的API归约为少量基本操作（如`add`、`multiply`、`get_at`等），并用一致的规则表达任意向量化模式。

在方法谱系中，einx定位为ein*-符号家族的新成员，但实现了质的跨越：相比**einsum**（Wiebe, 2011）仅支持有限操作、**einops**（Rogozhnikov, 2022a）缺乏通用向量化能力，einx首次将符号系统推广到任意张量操作，并引入了串联轴（`+`）、多省略号等新特性（Table 2展示了各符号系统的功能对比）。与使用符号轴名进行隐式向量化的**named tensors**（如Haliax）不同，einx采用显式声明方式，表达式具有清晰的可解释性。

实验方面，einx的首次调用编译开销在毫秒级（如`einx.id`转置约6.8ms），后续缓存调用开销降至0.1ms以下，对实际使用影响有限。使用统计（Table 4）显示，einsum和einops在ML会议论文中的使用率分别达35.27%和21.19%，表明社区对统一张量符号存在真实需求，einx有潜力成为下一代的整合方案。

## 背景与动机

### 张量框架的API碎片化困境

现代张量计算框架（如NumPy、PyTorch、JAX）已成为科学计算与深度学习的核心基础设施。然而，这些框架长期面临一个根本性矛盾：**操作语义的高度统一与API形态的极度碎片化**。以索引操作为例，NumPy-like框架提供了`take`、`take_along_axis`、`gather`、`tensor[:]`等多个函数，它们在底层执行相同的“从张量中按坐标取值”的基本操作，差异仅在于向量化模式——即基本操作沿哪些轴广播、沿哪些轴独立执行。类似地，`repeat`与`tile`、`concat`与`stack`等函数对，本质上也是同一基本操作在不同向量化模式下的变体。

这种设计导致了三个连锁问题：

1. **学习负担沉重**：用户必须记忆大量函数名及其特定轴语义，而非理解少数核心操作的向量化规则。
2. **形状错误频发**：每个函数对输入张量的维度排列有隐含假设，缺乏显式的形状声明机制，调试成本高昂。
3. **代码可读性差**：点自由风格（point-free style）的API调用无法直观表达“哪个轴参与操作、哪个轴被向量化”的意图。

### ein*-符号系统的演进与局限

为解决上述问题，一系列基于爱因斯坦求和约定（Einstein summation convention）的符号系统被提出。爱因斯坦求和约定通过隐式求和规则简化了张量缩并的表达：`A_{ij} B_{jk} = \sum_j A_{ij} B_{jk}`，其中重复指标`j`自动求和。

**einsum**（Wiebe, 2011）将这一约定实现为`einsum("ij, jk -> ik", A, B)`的形式，支持点积、转置、对角线提取等操作，现已被NumPy、PyTorch、TensorFlow等主流框架内置。然而，einsum仅支持有限的操作类别，无法表达展平、重复、串联等常见向量化模式。

**einops**（Rogozhnikov, 2022a）扩展了einsum的符号，引入括号表示轴展平，提供了`rearrange`、`reduce`、`repeat`三个操作，大幅提升了张量重塑的表达力。其后续扩展`einops.pack/unpack`（Rogozhnikov, 2022b）增加了打包/解包操作。但einops的符号设计存在结构性局限：**不区分传递给基本操作的轴与向量化轴**，所有轴在表达式中地位等同，导致符号语义模糊——用户无法从表达式本身判断哪些轴参与核心计算、哪些轴仅被广播。

**eindex**进一步扩展了索引操作的ein-符号，但同样缺乏向量化轴的显式标记。此外，**named tensors**（如Haliax）尝试通过符号轴名实现隐式向量化，但其设计目标与ein*-符号系统正交，更侧重类型安全而非操作统一。

### 核心洞察与本文动机

本文的核心洞察是：**所有张量操作本质上都是基本操作的向量化**。以矩阵乘法为例，`z = x @ y`可被理解为“将向量点积操作沿`a`和`c`轴向量化”——沿`a`轴遍历`x`的行、沿`c`轴遍历`y`的列，对每一对行-列执行点积。类似地，`torch.gather`可被理解为“将索引取值操作沿指定轴向量化”。

这一洞察揭示了现有框架的根本瓶颈：**缺乏一种通用的、声明式的向量化表示**，使得同一基本操作的不同向量化模式被分散为多个独立API。如果存在一种符号系统，能够：

- **解耦基本操作与向量化模式**：用少量基本操作（如`add`、`multiply`、`get_at`、`set_at`）替代庞大API；
- **显式标记向量化轴**：让用户一眼识别哪些轴参与基本操作、哪些轴被广播；
- **统一规则覆盖所有操作**：同一套符号规则适用于任意张量操作，包括自定义函数；

那么上述碎片化问题将从根本上得到解决。这正是einx的设计动机：将“一切皆向量化”的哲学具体化为一种**声明式、有指向（pointful）的符号系统**，通过类比循环记法（loop notation）定义，用方括号显式区分向量化轴与基本操作轴，从而将Numpy-like框架的复杂API归约为少数基本操作与一套统一的向量化表达规则（参见Table 1）。

## 核心创新

### 创新动机：张量API的碎片化困境

当前主流张量框架（NumPy、PyTorch等）面临一个根本性瓶颈：**API庞大、不一致且缺乏统一的向量化表达**。同一底层操作因向量化模式不同而对应数十个不同函数——例如索引操作在PyTorch中分散于`torch.take`、`torch.gather`、`torch.index_select`等函数（Table 1），这些函数本质上共享相同的核心语义，仅在向量化方式上存在差异。这种碎片化导致代码难读难写，并频繁引发形状错误。

### 核心洞察：一切皆向量化

einx的核心洞察在于：**所有张量操作本质上都是基本操作的向量化**。矩阵乘法可视为向量化点积，批量索引可视为向量化标量索引。基于这一认识，einx将复杂API解耦为两个正交维度——**基本操作**与**向量化模式**——并用统一的声明式符号系统表达任意向量化组合。

### 关键创新：方括号区分向量化轴与操作轴

einx最核心的符号创新是引入**方括号标记机制**，明确区分两种轴角色（Sec. 4.1）：

- **无括号轴**：表示向量化轴，沿这些轴对子张量进行并行处理
- **方括号轴**：表示传递给基本操作的子张量轴

以矩阵乘法为例：
$$z = \text{einx.dot}(\text{"a [b], [b] c → a c"}, x, y)$$

其中`[b]`标记被点乘的轴，而`a`和`c`是向量化轴。这一区分使表达式具有清晰的解释：沿`a`和`c`轴对`[b]`维度的子张量进行点积运算。

相比之下，einsum和einops均**不区分向量化轴与操作轴**（Table 2），所有轴在符号层面地位相同，用户无法从表达式中直接识别哪些轴参与基本运算、哪些轴仅用于并行。

### 轴组合的扩展：串联轴

einx引入了**串联轴**（用`+`表示），这是einsum完全不支持、einops仅部分支持的能力（Table 2）：
$$\text{einx.id}(\text{"a b, a c → a (b + c)"}, x, y)$$

该表达式将两个张量沿`b`和`c`轴串联，`(b + c)`表示串联后的轴。这种轴组合方式在所有einx操作中可用，而einops的串联仅在其`pack/unpack`子集中支持，且始终伴随展平操作。

### 操作支持范围的质变

einx从设计上**可向量化任意操作**，包括用户自定义函数（Sec. 4.2）。这与einsum/einops形成根本差异：

| 能力维度 | einsum | einops | **einx** |
|---------|--------|--------|----------|
| 预定义操作 | 点积、归约 | 重排、归约、重复 | 所有NumPy-like操作 |
| 自定义操作 | 不支持 | 不支持 | **支持** |
| 向量化表达 | 隐式 | 部分显式 | **完全显式** |

这一扩展使得einx不仅能表达现有API的所有操作（Table 1），还能表达einsum和einops无法表示的向量化模式，如任意操作的重复向量化（输出端向量化）和串联向量化（Table 2）。

### 多省略号机制

einsum中省略号只能引用同一组轴，而einx支持**多个独立的省略号**，分别对应不同轴集（Appendix C）。这使einx能表达复杂的广播模式，例如类克罗内克积：
$$\text{einx.multiply}(\text{"a…, b… → (a b)…"}, x, y)$$

其中两个省略号独立展开，分别对应`x`和`y`的非显式轴。

### 与现有方法的本质差异

einx与**named tensors**（如Haliax）的根本区别在于：named tensors通过轴名实现隐式向量化，要求框架层面支持；而einx是**声明式符号层**，不改变底层张量语义，可在任何NumPy-like框架上实现。einx表达式自我文档化轴名，但采用声明式而非命令式风格。

## 整体框架

einx 的整体设计遵循**“一切皆向量化”**的核心思想，将任意张量操作分解为基本操作与其向量化表示两个正交维度。其工作流可概括为三个阶段：**AST生成与轴解析 → 计算图构建 → 代码生成与优化**。

### 输入：einx表达式与张量参数

用户通过统一的函数入口（如 `einx.dot`、`einx.add`、`einx.get_at` 等）调用 einx，传入的参数包括：
- **向量化字符串**：采用声明式、点完整（pointful）的符号，以方括号标记传递给基本操作的子张量轴，无括号的轴表示向量化轴。例如 `einx.dot("a [b], [b] c -> a c", x, y)` 中，`[b]` 是被点乘的轴，`a` 和 `c` 是向量化轴。
- **输入张量**：实际数据，其形状必须与表达式中的轴约束一致。
- **可选轴长度参数**：当某些轴长度无法从输入张量唯一确定时，需显式指定（如 `ds=4`）。

### 阶段一：AST生成与轴解析

编译器首先将 einx 表达式字符串解析为抽象语法树（AST），在此过程中完成：
- **省略号展开**：einx 支持多个独立的省略号，分别对应不同的轴集，这与 einsum 中省略号只能引用同一组轴有本质区别。
- **轴长度确定**：遍历 AST，结合输入张量的实际形状与用户指定的轴长度参数，推导所有轴的长度。若存在歧义或无法唯一确定，则立即报错。

### 阶段二：计算图构建

基于解析后的形状 AST、操作类型（如 `dot`、`add`、`get_at`）以及目标后端框架（NumPy、PyTorch 等），编译器构建一个计算图：
- 图中节点代表具体的后端操作（如转置、重塑、基本运算）。
- 边记录操作间的依赖关系与数据流向。
- 向量化逻辑在此阶段被“编译”为对基本操作的显式循环或批量调用模式。

### 阶段三：代码生成与优化

计算图被转换为一段独立的 Python 代码片段，并应用启发式优化（如消除冗余转置、合并连续重塑操作）：
- 首次调用时，通过 Python 的 `exec` 将代码片段编译为可调用函数对象并缓存。
- 后续相同签名的调用直接复用缓存的函数，编译开销降至 0.1 ms 以下（首次调用为 6–24 ms 量级，见 Table 3）。

### 输出：可调用函数与计算结果

最终返回一个可直接作用于输入张量的函数对象，执行后得到结果张量。整个流程对用户透明，用户仅需提供声明式的向量化表达式，无需手动管理循环、索引对齐或形状变换。

### 模块关系总结

```
einx表达式 + 张量参数
        │
        ▼
┌─────────────────────┐
│  AST生成与轴解析     │  ← 展开省略号，确定轴长度
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  计算图构建          │  ← 基于后端框架与操作类型构建DAG
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  代码生成与优化      │  ← 生成Python代码，启发式优化，JIT缓存
└────────┬────────────┘
         │
         ▼
   可调用函数 + 计算结果
```

这一流水线的核心优势在于**解耦操作与向量化**：无论底层基本操作是点积、加法还是自定义函数，向量化的表达规则完全一致，从而将 NumPy-like 框架中庞大且不一致的 API 归约为少数几个基本操作入口（见 Table 1）。

## 核心模块与公式推导

### 核心设计思想

einx 的核心洞察在于：所有张量操作本质上都是基本操作的向量化。基于此，einx 将复杂 API 解耦为**少量基本操作**与**统一的声明式向量化符号**两部分。用户通过类比循环记法（loop notation）构造向量化字符串，显式指定哪些轴传递给基本操作（方括号内）、哪些轴用于向量化（方括号外），从而用单一规则表达任意向量化模式。

### 关键符号约定

einx 表达式的构造遵循以下规则（Sec. 4.1）：

- **方括号 `[...]`**：标记传递给基本操作的子张量轴。括号内的轴构成基本操作所见的参数形状。
- **无括号轴**：表示向量化轴，沿这些轴对基本操作进行隐式循环。
- **圆括号 `(...)`**：将多个轴展平（flatten）为一个轴。
- **加号 `+`**：将多个轴串联（concatenate）为一个轴，仅 `einx.id` 等操作支持。

以矩阵乘法为例：
$$z = \text{einx.dot}(\text{"a [b], [b] c} \to \text{a c"}, x, y)$$
其中 `[b]` 标记被点积消耗的轴，`a` 和 `c` 为向量化轴。该表达式等价于循环记法 `z[a, c] = dot(x[a, :], y[:, c])`。

### 核心公式

einx 通过统一符号表达多种张量操作，以下为代表性公式：

**展平操作**（`einx.id`）：
$$\text{einx.id}(\text{"a b c} \to \text{(a b) c"}, x)$$
将 `a` 和 `b` 轴展平为一个轴，等价于 `reshape`。

**串联操作**（`einx.id`）：
$$\text{einx.id}(\text{"a b, a c} \to \text{a (b + c)"}, x, y)$$
沿 `b`/`c` 轴串联两个张量，等价于 `concatenate`。这是 einx 引入的新型轴组合方式（串联轴），在 einsum/einops 中缺乏对应支持（Table 2）。

**N 维平均池化**（`einx.mean`）：
$$\text{einx.mean}(\text{"(s [ds])\dots"}, x, ds=4)$$
将空间维度 `s` 分解为输出空间轴和池化窗口轴 `[ds]`，沿 `[ds]` 取均值。省略号 `\dots` 使其适用于任意维数。

**深度到空间变换**（`einx.id`）：
$$\text{einx.id}(\text{"b s\dots (c ds\dots)} \to \text{b (s ds)\dots c"}, ds=4)$$
将通道维度 `c` 与空间块尺寸 `ds` 重新排列，实现深度到空间的像素重组。

**类 Kronecker 乘法**（`einx.multiply`）：
$$\text{einx.multiply}(\text{"a\dots, b\dots} \to \text{(a b)\dots"}, x, y)$$
利用省略号实现任意维度的向量化逐元素乘法，输出轴 `(a b)` 将两输入的对应轴展平。

### 后端编译流程

einx 将表达式编译为可执行的后端代码，流程分为三个关键模块（Appendix D）：

1. **AST 生成与轴解析**：将向量化字符串解析为抽象语法树，展开省略号，根据输入张量形状推断所有轴的长度。
2. **计算图构建**：基于后端框架（NumPy/PyTorch 等）、操作类型和形状 AST 构建计算图，记录各操作的依赖关系。
3. **代码生成与优化**：将计算图转换为隔离的 Python 代码片段，应用启发式优化（如轴合并），通过 `exec` 编译为可调用对象并缓存，后续相同签名的调用直接复用缓存。

### 与基线方法的根本差异

| 维度 | einsum/einops | einx |
|------|--------------|------|
| 轴区分 | 不区分向量化轴与基本操作轴 | 方括号显式标记基本操作轴 |
| 轴组合 | 仅支持展平（括号） | 支持展平（括号）和串联（+） |
| 操作范围 | 仅预定义操作（点积、归约等） | 可向量化任意操作，包括自定义函数 |
| 省略号 | 只能引用同一组轴 | 支持多个独立省略号 |

这些差异使 einx 能将 NumPy-like 框架中数十个功能不同的函数（如 `torch.take`、`torch.gather`、`torch.scatter` 等）统一为 `einx.get_at`、`einx.set_at` 等少数基本操作，仅通过向量化字符串区分行为（Table 1）。

## 实验与分析

### 核心主张的实证支撑

论文的核心主张——“所有张量操作本质上都是基本操作的向量化”——主要通过对API覆盖度的定性分析来支撑，而非传统的定量基准测试。**Table 1** 展示了多种Numpy-like操作（如 `np.sum`、`np.stack`、`torch.gather`、`torch.take` 等）如何被归约为 `einx` 中的少数基本操作（如 `einx.sum`、`einx.get_at`），仅通过改变向量化字符串来区分。这一映射关系直接证明了 `einx` 符号的统一能力，但该表仅展示了“可表达性”，并未量化表达简洁性或代码可读性的提升。

**Table 2** 从操作类别维度系统比较了 `einx` 与现有 `ein*`-符号系统（`einsum`、`einops` 各变体、`eindex`）的覆盖范围。`einx` 是唯一同时支持排列（P）、展平（F）、重复（R）和串联（C）四类操作的系统，而 `einsum` 仅支持排列，`einops.rearrange` 不支持重复和串联。这一对比为 `einx` 的“通用性”主张提供了直接证据（置信度 0.95）。

![[assets/figures/papers/paper_list_l11_https_openreview_net_forum_id_QqvQ3iAdpC/figures/001_Table_2.jpg]]
*Table 2: Support for classes of operations and vectorization in different types of ein*-notation. P: Permutation. F: Flattening. R: Repetition (i.e. output-only vectorization). C: Concatenation. *: Always and only flattens concatenated axes. **: Coordinate axis must be first axis*

### 编译开销与性能特征

论文提供了有限的定量性能数据。**Table 3** 报告了三种 `einx` 操作在 Numpy 后端的编译开销：

| 操作 | einx 开销 (ms) | 原生 Numpy (ms) | 额外开销 |
|------|---------------|-----------------|---------|
| `einx.id` (transpose) | 6.8 ± 1.3 | 0.077 ± 0.003 | +6.723 |
| `einx.add` (simple) | 9.3 ± 2.4 | 0.077 ± 0.003 | +9.223 |
| `einx.add` (with d=2) | 23.5 ± 3.1 | 0.077 ± 0.003 | +23.423 |

这些数据揭示了两个关键特征：
1. **首次调用开销**：编译过程引入毫秒级延迟（6.8–23.5 ms），对于极小张量或极简单操作，这一开销可能远超原生执行时间。
2. **JIT缓存机制**：论文指出编译结果在首次调用后被缓存，后续调用开销降至 0.1 ms 以下，因此在重复执行的训练循环中，摊销后的开销可忽略。

**公平性说明**：这些测试仅测量了编译开销，并未与 `einsum` 或 `einops` 进行直接的性能对比。论文未提供端到端的训练吞吐量或内存占用数据，因此无法评估 `einx` 在真实深度学习工作负载中的性能影响。此外，`einx` 的后端无关设计意味着实际性能高度依赖底层框架（Numpy/PyTorch/JAX）的 `vmap` 实现质量。

### 社区采纳度与生态定位

**Table 4** 提供了相关张量符号库的使用统计，作为 `einx` 潜在影响力的背景参考：

![[assets/figures/papers/paper_list_l11_https_openreview_net_forum_id_QqvQ3iAdpC/figures/002_Table_4.jpg]]
*Table 4: Usage statistics of libraries in the context of tensor notations. *: einsum is implemented in different tensor frameworks, not a single repository. **: torchdim was upstreamed into the larger functorch repository on Aug 1, 2024. ***: No reliable search term*

- `einsum`（集成于各框架中）是绝对主流，其 GitHub 星数和会议使用率远超其他方案。
- `einops`（Rogozhnikov, 2022a）拥有显著的社区基础，表明开发者对声明式张量操作存在真实需求。
- `torchdim`（named tensors）已被合并至 `functorch`，说明隐式向量化的思路正在被主流框架吸收。

`einx` 的定位是“统一的超集”——它试图覆盖 `einsum` 和 `einops` 的全部功能并提供更多。但论文未提供从 `einops` 迁移到 `einx` 的实际案例或用户调研，其“可替代性”主张仍需社区验证。

### 已知局限与失败模式

1. **串联操作的受限支持**：轴串联（`+`）仅在 `einx.id` 操作中可用。对于 `einx.add` 等操作，串联会改变参数的数量和位置索引，因此不被支持。这意味着某些需要动态拼接的向量化模式仍需回退到原生 API。

2. **静态形状约束**：表达式中的所有轴长度必须在调用时通过输入张量与约束唯一确定。动态形状或部分维度未知的场景会直接引发错误，这限制了 `einx` 在可变批量大小或数据依赖形状场景中的适用性。

3. **首次调用延迟**：毫秒级的编译开销使其不适合极低延迟推理场景（如实时系统中的单次前向传播）。论文未讨论预热（warmup）策略或提前编译（ahead-of-time compilation）机制。

4. **缺乏自动微分验证**：论文未展示 `einx` 与 PyTorch/JAX 自动微分系统的集成测试，自定义操作的梯度传播正确性需要手动验证。

## 方法谱系与知识库定位

### 符号系统的演化脉络

einx 并非凭空出现，而是站在 ein*-符号家族的肩膀上。理解这一谱系，有助于定位 einx 的创新边界与适用场景。

**einsum**（Wiebe, 2011）开创了用爱因斯坦求和约定表达张量运算的先河，但其设计存在两个根本性局限：一是仅支持求和操作，无法表达排列、展平、重复等通用向量化模式；二是省略号只能引用同一组轴，缺乏多组独立省略号的能力。**einops**（Rogozhnikov, 2022a）通过引入 `rearrange`、`reduce`、`repeat` 等操作，将符号的覆盖范围扩展到排列和归约，但其核心缺陷在于——没有区分"传递给基本操作的轴"与"向量化轴"，导致符号的表达能力受限于预定义的操作集合。**einops.pack/unpack**（Rogozhnikov, 2022b）进一步补充了打包/解包操作，**eindex** 则针对索引操作做了专门扩展，但两者均未触及根本问题：符号与操作的耦合。

einx 的核心突破在于**将操作与向量化解耦**。这一设计决策的因果链条清晰：通过方括号标记传递给基本操作的子张量轴，无括号的轴表示向量化轴，einx 首次实现了"任意操作 + 任意向量化模式"的统一表达。表2（Table 2）直接量化了这一差异：在排列（P）、展平（F）、重复（R）和串联（C）四类向量化操作中，einx 是唯一全部支持的符号系统。

### 与命名张量框架的关系

**named tensors**（如 Haliax）代表了另一种思路：通过为轴赋予符号名来实现隐式向量化。这类框架的优势在于类型安全，但其向量化逻辑被隐藏在框架内部，用户无法显式控制向量化的粒度。einx 则选择了声明式、显式的路线——用户通过表达式精确描述"什么操作被向量化到哪些轴上"，这与命名张量的隐式风格形成互补而非替代关系。当前论文未提供两者在相同任务上的直接对比，这一比较需要手动验证。

### 适用边界与局限

einx 的适用边界由以下三个约束划定：

1. **轴串联的操作限制**：仅 `einx.id` 操作支持轴串联（`+`），其他操作（如 `add`）不支持，因为串联会改变参数的数量和位置索引。这意味着需要拼接多个张量的场景必须通过 `einx.id` 显式处理，无法在向量化表达式中内联完成。

2. **形状的静态确定性**：表达式中的所有轴长度必须在调用时通过输入张量与约束唯一确定。动态形状或部分维度未知的情况将直接引发错误。这一限制源于编译器的设计选择——在首次调用时完成所有形状推导和代码生成，后续调用复用缓存结果。对于 batch size 可变等常见场景，用户需要将可变维度置于向量化轴（无括号轴）中，而非基本操作轴（方括号轴）中。

3. **首次调用的编译开销**：表3（Table 3）显示，简单转置操作的首次调用开销约为 6.8 ms，带二维展平的加法操作约为 23.5 ms，而原生 Numpy 操作仅需约 0.077 ms。虽然后续调用开销降至 0.1 ms 以下（得益于 JIT 编译缓存），但在极低延迟场景（如实时推理的每次调用都使用不同形状）中，这一开销可能不可接受。

### 开放问题

论文留下的开放问题指向三个方向：

- **生态采纳**：einsum 和 einops 已拥有庞大的用户基础（表4显示 einops 在 GitHub 上有 8k+ stars，在 NeurIPS 2023 论文中出现 40+ 次）。einx 能否说服社区迁移，取决于其符号的认知负担是否足够低、与现有代码的互操作是否足够平滑。

- **编译开销优化**：当前实现通过 `exec` 生成 Python 代码片段并缓存，首次调用的毫秒级开销在批量处理场景中可忽略，但在交互式探索或低延迟服务中仍是障碍。是否可以通过预编译或 AOT（ahead-of-time）模式消除这一开销，是工程层面的关键问题。

- **自动微分集成**：论文未讨论 einx 与自动微分框架的深度集成。对于自定义操作，用户需要手动提供梯度实现，这限制了 `einx` 在需要反向传播的训练循环中的灵活性。能否将 einx 的向量化语义直接映射到 vmap + autograd 的组合，是一个值得探索的方向。

## 原文 PDF

![[paperPDFs/ICLR_2026/Its_All_Just_Vectorization_einx_a_Universal_Notation_for_Tensor_Operations.pdf]]
