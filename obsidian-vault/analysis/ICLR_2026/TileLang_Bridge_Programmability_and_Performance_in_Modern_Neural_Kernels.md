---
title: "TileLang: Bridge Programmability and Performance in Modern Neural Kernels"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/TileLang_Bridge_Programmability_and_Performance_in_Modern_Neural_Kernels.pdf
project_link: null
code_link: https://github.com/tile-ai/tilelang
openreview_forum_id: Jb1WkNSfUB
aliases:
- TileLang
tags:
- ICLR_2026
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/representation_learning
core_operator: "将tile提升为一级公民并提供可编程的tile抽象，显式控制内存放置、数据移动、布局与并行性；同时通过融合tile数据流图（FTG）上的硬件感知tile推荐（成本模型）与tile推断（约束传播）自动完成优化配置。"
primary_logic: "通过编译器可见的tile语义与自动化tile优化（推荐+推断），TileLang在保持高级Python DSL易用性的同时，实现了接近手工CUDA的性能，显著减少代码量并支持多后端（NVIDIA/AMD）。"
claims:
- "Triton实现的MLA仅需130行代码，性能为手工CUDA(约500行)的14.2%。"
- "TileLang在MLA上达到Triton平均5.56倍的性能，且代码量不到手工核的16%。"
- "Tile推荐基于成本模型提供硬件感知的tile形状、内存放置和warp分区默认值。"
- "Tile推断通过约束传播自动完成剩余配置。"
---

# TileLang: Bridge Programmability and Performance in Modern Neural Kernels

> [!tip] 核心洞察
> 通过编译器可见的tile语义与自动化tile优化（推荐+推断），TileLang在保持高级Python DSL易用性的同时，实现了接近手工CUDA的性能，显著减少代码量并支持多后端（NVIDIA/AMD）。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | TileLang：桥接现代神经核的可编程性与性能 |
| 英文题名 | TileLang: Bridge Programmability and Performance in Modern Neural Kernels |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=Jb1WkNSfUB) · [GitHub](https://github.com/tile-ai/tilelang) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/representation_learning |
| Method | TileLang |
| Dataset | Multi-Head Latent Attention (MLA), GEMM (FP16), Dequantized GEMM (WINT4AFP16) |

> [!tip] 效果简介
> - Multi-Head Latent Attention (MLA) 上，Speedup over Triton on H100 为 4.06×–10.59×，对比 SGLang Triton MLA implementation，变化 4.06×–10.59×。
> - Multi-Head Latent Attention (MLA) 上，Speedup over Triton on MI300X 为 5.64×–12.97×，对比 Triton MLA，变化 5.64×–12.97×。
> - GEMM (FP16) 上，Speedup over PyTorch on H100 为 1.18×–1.40×，对比 PyTorch Inductor (torch.matmul)，变化 1.18×–1.40×。

## 概要

现代AI编译器在性能与编程便捷性之间面临尖锐矛盾。以Triton为代表的DSL大幅降低了GPU核开发门槛，但其对内存层次、数据移动与并行调度的控制高度依赖编译器隐式启发式，开发者在面对复杂算子时几乎无法介入优化决策。一个典型例证是：Triton实现的多头潜在注意力（MLA）仅需130行代码，性能却只有手工CUDA核（约500行）的14.2%。开发者被迫在"高性能手工CUDA"与"高生产力编译器DSL"之间做非此即彼的选择。

TileLang针对这一瓶颈提出了一个统一方案：**将tile提升为一级公民，提供可编程的tile抽象，同时通过编译器可见的tile语义实现自动化优化**。其核心思路是，开发者通过显式原语控制内存放置（`T.alloc_shared`/`T.alloc_fragment`）、数据移动与warp分区策略，而编译器在融合tile数据流图（FTG）之上，通过硬件感知的tile推荐（基于roofline成本模型）与tile推断（约束传播）自动完成tile形状、内存布局、流水线调度等剩余配置。

这一设计在保持Python DSL易用性的同时，实现了接近手工CUDA的性能。在MLA核上，TileLang达到Triton平均5.56倍的性能，代码量不到手工核的16%。在NVIDIA H100上，TileLang相较Triton在多种算子上实现1.08×–10.59×加速（平均3.02×）；在AMD MI300X上实现1.01×–11.56×加速（平均2.65×），同时代码量最多减少85.5%。该方法支持通过统一的`T.call_extern`接口调用NVIDIA cute与AMD ck等后端tile库，实现跨平台可移植性。



### 现代AI核编程的核心困境

现代深度学习模型对GPU核的性能要求日益严苛，然而开发者长期面临一个根本性的权衡：**高性能与编程便捷性难以兼得**。手工CUDA核能够充分发挥硬件潜力，但编写和调优过程极其繁琐；高级领域特定语言（DSL）虽然大幅降低了开发门槛，却因对内存层次、数据移动和并行调度的控制不足，导致性能严重受限。

这一困境在**多头潜在注意力（MLA）**核中表现得尤为突出。MLA是DeepSeek-V3等大模型的核心算子，其数据流复杂、内存访问模式多样。以Triton（Tillet et al., 2019）为例，其MLA实现仅需约130行代码，但性能仅为手工CUDA核（约500行）的**14.2%**——开发者不得不在“易写但慢”与“快但难写”之间做出艰难选择。

### 现有方法的缺口

当前GPU核编程生态中存在两类主流方案，但均存在显著局限：

- **编译器驱动方案**（如Triton、PyTorch Inductor）：通过自动代码生成简化开发，但将内存放置、tile配置、流水线调度等关键优化决策完全交由编译器启发式算法处理。编译器缺乏对复杂数据流模式的全局理解，难以生成接近手工CUDA的代码。
- **模板/库方案**（如CUTLASS、ThunderKittens、Composable Kernel）：通过高度优化的模板提供极致性能，但要求开发者深入理解硬件细节，且代码复用性和跨平台可移植性有限。

近年来出现的Gluon、Helion、Tilus等系统尝试在两者之间取得平衡，但本质上仍受限于其底层抽象——要么暴露的硬件控制粒度不足，要么牺牲了跨平台通用性。

### 核心瓶颈与本文动机

上述困境的根源在于一个结构性问题：**现代AI编译器缺少对内存层次、数据移动与并行调度的显式编程控制**。具体而言：

1. **内存放置不透明**：编译器自行决定数据位于共享内存还是寄存器文件，开发者无法根据算法特征进行精确干预。
2. **tile配置依赖启发式**：tile大小、形状和内存布局的确定缺乏硬件感知的全局优化视角。
3. **并行调度隐式化**：warp分区、流水线深度等调度决策被编译器“黑盒”处理，难以针对特定算子进行定制。

TileLang的提出正是为了打破这一僵局。其核心动机是：**将tile提升为一级公民，通过可编程的tile抽象显式控制上述关键维度，同时借助编译器可见的tile语义与自动化优化（tile推荐与推断），在保持高级Python DSL易用性的前提下，实现接近手工CUDA的性能**。这一设计使得开发者能够聚焦于算法层面的tile级数据流描述，而将硬件细节的配置优化交由编译器的成本模型和约束传播自动完成，从根本上桥接可编程性与性能之间的鸿沟。



## 核心方法与创新机理

TileLang 的核心创新在于**将 tile 提升为一级编程公民**，并通过**编译器可见的 tile 语义**与**自动化 tile 优化**两个层面，系统性地解决了现代 GPU 核开发中“可编程性 vs. 性能”的根本矛盾。

### 瓶颈洞察：编译器黑盒导致性能悬崖

现代 AI 编译器 DSL（如 Triton）虽然大幅降低了 GPU 核的编写门槛，但其对内存层次、数据移动与并行调度的隐式管理形成了编译器黑盒。这一缺陷在复杂算子中暴露无遗：Triton 实现的 MLA（Multi-Head Latent Attention）仅需 130 行代码，但性能仅为手工 CUDA（约 500 行）的 14.2%。开发者被迫在“高性能（手工 CUDA）”与“编程便捷性（Triton DSL）”之间做出艰难权衡。

### 因果杠杆：可编程 tile 抽象 + 自动化 tile 优化

TileLang 的设计围绕两条因果链路展开：

1. **显式控制原语**：提供 `T.alloc_shared`（共享内存分配）和 `T.alloc_fragment`（寄存器分配）等原语，使开发者能够在 tile 粒度上精确控制内存放置、数据移动、内存布局与并行调度（如 warp 分区策略 `policy=FullCol/FullRow`）。这填补了 Triton 在内存层次控制上的空白。

2. **自动化配置推断**：在融合 tile 数据流图（FTG）上，通过**硬件感知的 tile 推荐**（基于 roofline 成本模型生成候选 tile 形状、内存放置和 warp 分区的排序短名单）与**tile 推断**（通过约束传播自动完成剩余配置，包括布局、流水线深度等），将优化决策从开发者负担转变为编译器自动完成的配置。开发者仅需暴露一个 `num_stages` 参数即可获得自动流水线调度。

### 关键机制：从手动调优到成本模型引导

TileLang 的 tile 推荐机制使用静态 roofline 成本模型估算执行时间：

$$Time = \max_{i,j} \left( \frac{\mathrm{MemoryTraffic}_i}{\mathrm{Bandwidth}_i}, \frac{\mathrm{Computation}_j}{\mathrm{Performance}_j} \right) + t_{\mathrm{intrinsic}}$$

该模型能够**修剪 95% 的候选调度，同时保留 98.47% 的最佳性能**（Table 3），将 GEMM 的平均调优时间从 Triton 的约 18-20 秒和 Ansor 的 >400 秒压缩至约 10 秒（Table 5）。

### 变更槽位总结

| 变更维度 | 基线方法（Triton/CUDA） | TileLang 方案 |
|---------|----------------------|-------------|
| 内存放置控制 | 编译器不透明启发式 / 手工放置 | `T.alloc_shared`、`T.alloc_fragment` 显式原语 |
| Tile 配置 | 手工启发式或固定 tile 尺寸 | 成本模型驱动的 tile 推荐 |
| 内存布局确定 | 编译器推断 / 手工编写 swizzle | FTG 上的层次化布局推断（严格/公共/自由三阶段） |
| 流水线调度 | 手工插入异步拷贝 / 有限编译器支持 | 从串行代码自动推断，仅暴露 `num_stages` |
| Warp 分区 | 隐式或手工 warp 调度 | 显式 warp 分区策略 + 成本模型引导推荐 |
| 硬件可移植性 | 平台特定代码（CUDA/PTX vs. HIP/ROCm） | 统一 DSL + 后端特定 tile 库（cute/ck）通过 `T.call_extern` 调用 |

### 效果验证

在 MLA 算子上，TileLang 达到 Triton 平均 **5.56 倍**的性能提升，且代码量不到手工核的 16%（Figure 1）。消融实验揭示了平台特异性的优化贡献：在 H100 上，warp 分区（`+Partition`）贡献了主导性的 4.34 倍加速；而在 MI300X 上，内存放置优化（`+Alloc`）是主要优化，实现了 6.56 倍加速（Figure 9）。这种平台感知的自动优化能力是 TileLang 区别于现有 DSL 的核心优势。



![[assets/figures/papers/paper_list_l29_https_openreview_net_forum_id_Jb1WkNSfUB/figures/006_Figure_6.jpg]]
*Figure 6: Pipeline Inference mechanism in TILELANG*

TileLang 的编译工作流围绕**融合 tile 级数据流图（FTG）**展开，采用“开发者标注 + 编译器自动补全”的协作模式。整个 pipeline 分为五个阶段（Figure 7）：

1. **Tile 级 Python DSL 编写**：开发者使用 TileLang 的 Pythonic DSL 编写 tile 级程序，通过 `T.alloc_shared`、`T.alloc_fragment` 等原语显式控制内存放置，并可选择性标注 tile 形状、warp 分区策略等调度提示。

2. **AST 解析与 FTG 构建**：编译器将 Python DSL 代码翻译为 TileLang AST，进而构建统一的 FTG。FTG 以 tile 为一级公民，显式编码算子间的数据依赖、内存层级归属和并行单元映射。

3. **优化 Pass 执行**：在 FTG 上依次运行两阶段优化——**tile 推荐**和 **tile 推断**：
   - **Tile 推荐**（Section 4.2）基于静态 roofline 成本模型，分析部分标注的算子，生成硬件感知的 tile 形状、内存放置和 warp 分区默认值。成本模型通过比较内存流量/带宽与计算量/算力的最大比值来估算执行时间，能够修剪 95% 的候选调度同时保留 98.47% 的最佳性能。
   - **Tile 推断**（Section 4.3）通过约束传播自动补全剩余配置，包括 tile 尺寸、内存布局、软件流水线和 tensorization。布局推断采用分层策略（Strict / Common / Free），流水线推断自动从串行代码中识别可重叠的 copy 与 gemm 操作，仅暴露 `num_stages` 参数给用户。

4. **循环降级与代码生成**：优化后的 IR 经过循环降级等 TVM 标准 pass，最终生成 CUDA 或 ROCm 等后端代码。跨平台支持通过 `T.call_extern` 统一接口调用 NVIDIA 的 cute 或 AMD 的 ck 等 tile 库实现。

**输入**：开发者编写的 tile 级 Python 程序（含可选调度标注）。  
**输出**：针对目标硬件（NVIDIA H100 / AMD MI300X）优化后的可执行核代码。  
**核心模块关系**：FTG 是贯穿全流程的统一中间表示，tile 推荐为标注不完整的算子提供硬件感知默认值，tile 推断在此基础上通过约束传播完成全局配置闭合，二者协同将开发者的高层意图映射为接近手工 CUDA 性能的低层实现。



### 核心模块

TileLang 的编译管线由五个主要模块构成，围绕融合 Tile 数据流图（FTG）展开：

- **Tile 级 Python DSL**：开发者使用 Pythonic DSL 编写 tile 级程序，组合数据流算子与调度原语。核心原语包括 `T.alloc_shared`（分配共享内存缓冲区）、`T.alloc_fragment`（分配寄存器片段）、`T.call_extern`（调用后端 tile 库如 NVIDIA 的 cute 或 AMD 的 ck）等。Tile 被提升为一级公民，可由 warp、thread block 或程序员自定义的并行单元拥有。

- **AST 解析器**：将 Python DSL 代码翻译为 TileLang AST，作为后续编译阶段的中间表示。

- **FTG 构建**：从 AST 构建统一的融合 Tile 级数据流图（FTG），该图是后续所有优化与推断操作的核心载体。FTG 显式编码了算子间的数据依赖、内存层级和并行分区信息。

- **优化 Pass 序列**：在 FTG 上执行一系列优化 pass，包括 tile 推荐（基于成本模型生成硬件感知的 tile 形状、内存放置和 warp 分区默认值）、布局推断（通过约束传播自动完成内存布局配置）、流水线推断（从串行代码自动生成重叠的异步流水线调度）、循环降级等。

- **代码生成**：将优化后的 IR 降级为 CUDA（NVIDIA）或 ROCm（AMD）等后端代码，通过统一的 `T.call_extern` 接口调用平台特定的 tile 库。

#### 两阶段调度优化工作流

TileLang 在 FTG 上采用统一的两阶段工作流实现调度自动化：

1. **Tile 推荐**：分析 FTG 中部分标注的算子，提供硬件感知的默认配置，覆盖初始 tile 形状、内存放置策略和 warp 分区方案。
2. **Tile 推断**：通过约束传播在 FTG 上自动推断剩余配置，包括 tile 尺寸、内存布局、软件流水线和张量化指令映射。

#### 布局推断的三层策略

布局推断采用分层约束传播算法，集成三种互补策略：

- **严格布局推断**：对已显式标注布局的算子，强制传播其约束。
- **公共布局推断**：在多个消费者共享同一生产者时，选择兼容的公共布局以最大化访存合并效率。
- **自由布局推断**：对无约束的算子，基于硬件特性（如向量化宽度、bank 冲突避免）自主选择最优布局。

#### 流水线推断

TileLang 从串行程序自动推断流水线调度。系统分析 FTG 中的依赖关系，生成保持执行正确性的结构化流水线，仅向用户暴露一个 `num_stages` 参数。如 copy 和 gemm 等操作被自动重叠以提升并行度。

---

### 关键公式

#### 成本模型：Roofline 执行时间估计

Tile 推荐使用静态 roofline 成本模型评估候选配置（tile 形状、内存放置、warp 分区）。模型从 IR 中静态估算执行时间：

$$Time = \max_{i,j} \left( \frac{\mathrm{MemoryTraffic}_i}{\mathrm{Bandwidth}_i}, \frac{\mathrm{Computation}_j}{\mathrm{Performance}_j} \right) + t_{\mathrm{intrinsic}}$$

**变量含义**：
- $\mathrm{MemoryTraffic}_i$：第 $i$ 级内存层次的数据传输量
- $\mathrm{Bandwidth}_i$：第 $i$ 级内存层次的带宽
- $\mathrm{Computation}_j$：第 $j$ 类计算操作的计算量（如浮点运算数）
- $\mathrm{Performance}_j$：第 $j$ 类计算操作的峰值吞吐
- $t_{\mathrm{intrinsic}}$：固有开销（如 kernel launch、同步等）

该模型取内存受限时间与计算受限时间的最大值，加固有开销。模型假设计算与访存完美重叠，实际动态效应可能导致估算偏差。

---

#### 布局函数形式化

布局推断确定如何将多维索引转换为物理内存地址，考虑向量化、内存合并和 bank 冲突避免。

**物理布局地址表达式**：

$$\sum_i y_i s_i$$

其中 $y_i$ 为第 $i$ 维索引，$s_i$ 为其步幅。

**布局函数签名**：

$$\bar{f} : \mathbb{K}^n \to \bar{\mathbb{K}}^m$$

将 $n$ 维高维索引映射到 $m$ 维内存地址空间。

**片段布局签名**：

$$\dot{f} : \mathbb{K}^n \to \mathbb{K}^2$$

将每个索引映射到线程的寄存器 ID 和局部偏移量，用于寄存器级数据排布。

---

#### MLA 潜在投影

Multi-Head Latent Attention 的核心投影操作为：

$$\mathbf{z}_t = \mathbf{x}_t \mathbf{W}_{\mathrm{down}}$$

其中输入 token $\mathbf{x}_t$ 通过下投影矩阵 $\mathbf{W}_{\mathrm{down}}$ 映射到低维潜在向量 $\mathbf{z}_t$。该操作是 MLA 核计算瓶颈的关键组成部分。

---

### 成本模型有效性

实验表明，静态 roofline 成本模型能有效修剪搜索空间：预测的 top-5% 调度保留了 98.47% 的最佳性能，同时修剪了 95% 的候选调度。这使得 TileLang 在 GEMM 上的平均调优时间仅约 10 秒，显著低于 Triton（约 18–20 秒）和 Ansor（>400 秒）。



## 实验与关键发现

### 核心性能结果

TileLang在9种AI核上进行了系统评估，硬件平台覆盖NVIDIA H100 (80GB) 和 AMD Instinct MI300X (192GB)。评估的核心指标是相对于Triton或PyTorch的加速比，同时关注代码行数（LOC）作为可编程性的代理指标。

**MLA核的性能突破。** 多头部潜在注意力（MLA）是TileLang最突出的验证案例。在H100上，TileLang相对于SGLang Triton MLA实现实现4.06×–10.59×加速；在MI300X上，加速比达到5.64×–12.97×（见Figure 1）。更重要的是，TileLang以不到手工CUDA核16%的代码量，达到了接近手工CUDA的性能水平——而Triton实现的MLA虽仅需130行代码，性能却仅为手工CUDA的14.2%。这一结果直接验证了TileLang在桥接可编程性与性能方面的核心主张。

**通用算子的广泛优势。** 在GEMM（FP16）上，TileLang相对于PyTorch Inductor（`torch.matmul`）实现1.18×–1.40×加速；在去量化GEMM（WINT4AFP16）上，相对于专用核Marlin（Frantar et al., 2025）最高加速1.55×。在注意力相关核上，FlashAttention相对于Triton实现加速1.08×–1.58×，块稀疏注意力加速3.42×–7.87×，垂直斜线稀疏注意力相对于PyTorch Inductor加速高达108.55×–280.41×。Figure 8的散点图展示了TileLang在性能-代码量权衡中的系统性优势：其数据点普遍位于左上角（高性能、低代码量），优于Triton和PyTorch基线。

### 消融实验

Figure 9展示了FlashMLA在H100和MI300X上的逐项消融结果，揭示了不同硬件平台上优化优先级的显著差异。

**H100：warp分区是主导优化。** 在H100上，仅添加tile配置（+Tile）带来1.31×的温和加速。在此基础上，warp分区（+Partition）贡献了主导性提升，额外提供4.34×加速。这表明H100架构对warp级别的并行调度高度敏感，TileLang提供的显式warp分区原语（如`policy=FullCol/FullRow`）是释放性能的关键杠杆。

**MI300X：内存放置是首要优化。** 在MI300X上，优化优先级完全反转。内存放置优化（+Alloc）单独实现6.56×加速，成为最关键的优化步骤。进一步结合tiling（+Tile）后，整体提升再增加1.75×。这一差异揭示了AMD MI300X架构对显式内存层次控制（`T.alloc_shared`和`T.alloc_fragment`）的强依赖，也验证了TileLang跨平台可编程抽象的价值——同一套DSL能够在不同硬件上自动适配优化策略。

### 成本模型与调优效率

成本模型是TileLang自动化能力的核心。Table 3显示，成本模型预测的top-5%调度方案保留了98.47%的最佳性能，同时修剪了95%的候选调度空间。这意味着开发者无需在庞大的配置空间中盲目搜索，即可获得接近最优的tile形状、内存放置和warp分区配置。

![[assets/figures/papers/paper_list_l29_https_openreview_net_forum_id_Jb1WkNSfUB/figures/018_Table_3.jpg]]
*Table 3: Accuracy of our analytical cost model: predicted top-5% schedules retain over 98% of the best performance while pruning 95% of candidate schedules*

在调优时间上，TileLang展现出显著优势。GEMM的平均调优时间约为10秒（11.78–14.59秒），显著低于Triton（18.24–20.15秒）和Ansor（455.51–4142.05秒）（Table 5）。Conv2D的调优时间对比同样验证了这一趋势（Table 6）。快速调优的根源在于TileLang的静态roofline成本模型避免了耗时的实测搜索，同时tile推断（约束传播）自动完成了大量配置推导，减少了搜索维度。

![[assets/figures/papers/paper_list_l29_https_openreview_net_forum_id_Jb1WkNSfUB/figures/020_Table_5.jpg]]
*Table 5: Comparison of Average Tuning Times for GEMM*

![[assets/figures/papers/paper_list_l29_https_openreview_net_forum_id_Jb1WkNSfUB/figures/021_Table_6.jpg]]
*Table 6: Comparison of Average Tuning Times for Conv2D*

### 与同类DSL的对比

Figure 10和Table 9展示了TileLang与Gluon（OpenAI, 2025）、Helion（PyTorch, 2025）、Tilus（Ding et al., 2025）在GEMM上的对比。TileLang分别实现1.15–1.62×（vs Helion）、1.52–1.83×（vs Gluon）和1.87–2.12×（vs Tilus）的加速，同时使用更少的代码行数。这一结果表明，单纯暴露更底层的内存层次（如Gluon的shared memory/寄存器控制）并不足以获得最佳性能——TileLang通过编译器可见的tile语义与自动化优化（推荐+推断）实现了更优的权衡。

### 局限性与失败模式分析

尽管整体性能优异，以下情况需要关注：

1. **静态成本模型的偏差风险。** 静态roofline模型假设计算与访存完美重叠，实际运行中的DRAM刷新、缓存抖动等动态效应可能导致估算偏差。在极端不规则访存模式或高度动态的核中，成本模型的排名准确率可能下降，需要手动验证推荐结果。

2. **平台迁移的适配成本。** 消融实验已揭示H100和MI300X的优化优先级截然不同。虽然TileLang的tile推荐能自动适配，但某些深度优化（如Hopper的TMA异步拷贝、warp specialization）高度依赖特定硬件特性，迁移至新架构（如Intel GPU）时仍需额外适配工作。

3. **稀疏核的泛化性。** 垂直斜线稀疏注意力实现了108.55×–280.41×的极端加速，但这部分受益于PyTorch Inductor基线在稀疏模式下的低效。对于更广泛的稀疏核和动态形状工作负载，TileLang的性能泛化性尚待进一步验证。

4. **自动调优的覆盖范围。** 当前自动调优集中于tile形状、内存放置和warp分区，更复杂的调度组合（如算子融合策略、多核并行划分）仍需开发者手动指定。

### 补充图表

![[assets/figures/papers/paper_list_l29_https_openreview_net_forum_id_Jb1WkNSfUB/figures/014_Table_1.jpg]]
*Table 1: A partial list of primitives supported by TILELANG*

![[assets/figures/papers/paper_list_l29_https_openreview_net_forum_id_Jb1WkNSfUB/figures/015_Table_2.jpg]]
*Table 2: Comparison of specifications between NVIDIA H100 SXM and AMD MI300X*

![[assets/figures/papers/paper_list_l29_https_openreview_net_forum_id_Jb1WkNSfUB/figures/019_Table_4.jpg]]
*Table 4: Average Tuning Times for Different Operators*

![[assets/figures/papers/paper_list_l29_https_openreview_net_forum_id_Jb1WkNSfUB/figures/025_Table_7.jpg]]
*Table 7: Performance of Causal MHA on H100 (B = 64, H = 64, D = 128)*

![[assets/figures/papers/paper_list_l29_https_openreview_net_forum_id_Jb1WkNSfUB/figures/026_Table_8.jpg]]
*Table 8: Performance and Lines of Code(LoC) of Causal MHA on RTX 4090 (B = 16, H = 32, D = 128)*

![[assets/figures/papers/paper_list_l29_https_openreview_net_forum_id_Jb1WkNSfUB/figures/027_Table_9.jpg]]
*Table 9: Comparison of TileLang, Gluon (LoC = 68), Helion (LoC = 24), and Tilus (LoC = 110) on GEMM workloads*

![[assets/figures/papers/paper_list_l29_https_openreview_net_forum_id_Jb1WkNSfUB/figures/028_Table_10.jpg]]
*Table 10: Performance of Mamba-chunk-scan on H100, with batch size 8, 80 attention heads, model dimension 64, dstate 128, and sequence lengths ranging from 1024 to 32768. Helion LOC=116, TileLang LOC=114*

![[assets/figures/papers/paper_list_l29_https_openreview_net_forum_id_Jb1WkNSfUB/figures/029_Table_11.jpg]]
*Table 11: Commit hashes for baseline frameworks*



## 定位与知识库关联

### 核心定位：编译器可见的Tile语义与自动化优化

TileLang的核心洞察在于：现代AI编译器（如Triton）虽然提供了Python DSL的编程便捷性，却将内存层次、数据移动与并行调度的关键决策隐藏在编译器不透明的启发式规则中。这导致开发者在面对复杂核（如MLA）时陷入两难——Triton实现的MLA仅需130行代码，性能却只能达到手工CUDA（约500行）的14.2%；若追求性能转向手工CUDA，则需付出高昂的工程成本。

TileLang的解决方案是将**tile提升为一级公民**，使其成为编译器可见的语义单元。开发者通过显式原语（`T.alloc_shared`、`T.alloc_fragment`）控制内存放置，通过`T.use_tile`声明tile形状，通过`T.annotate`指定warp分区策略。这些标注并非简单的编译提示，而是作为**融合tile级数据流图（FTG）**上的约束，驱动后续的自动化优化流水线。

### 与基线方法的关系

**Triton**（Tillet et al., 2019）是TileLang最直接的对比基线。Triton将编程粒度从线程提升到block级别，显著降低了GPU编程门槛，但其编译器对内存层次和调度策略的控制有限。TileLang在保留Python DSL易用性的同时，通过tile推荐与推断机制填补了这一控制缺口。实验表明，TileLang在MLA上达到Triton平均5.56倍的性能，且代码量不到手工核的16%。

**PyTorch Inductor**（Paszke et al., 2019）是GEMM基准测试的主要参照。TileLang在FP16 GEMM上实现1.18–1.40倍的加速，在Vertical Slash Sparse Attention上更是达到108.55–280.41倍的惊人提升，这得益于TileLang对稀疏数据流的显式tile级控制。

**ThunderKittens (TK)**（Spector et al., 2025）和**CUTLASS**（NVIDIA, 2019）代表了模板驱动的高性能路线。TK通过精巧的模板元编程在NVIDIA GPU上实现极致性能，但平台锁定性强。TileLang通过统一的`T.call_extern`接口集成后端tile库（NVIDIA的cute和AMD的ck），在保持高性能的同时实现了跨平台可移植性。

**Gluon**（OpenAI, 2025）、**Helion**（PyTorch, 2025）和**Tilus**（Ding et al., 2025）是近期涌现的GPU DSL。Gluon构建于Triton之上，暴露了更底层的内存层次；Helion是编译到Triton的高层DSL；Tilus提供threadblock级粒度的编程。TileLang在GEMM上分别实现1.15–1.62倍、1.52–1.83倍和1.87–2.12倍的性能优势，同时代码量更少，验证了tile级抽象与自动化优化相结合的有效性。

**Marlin**（Frantar et al., 2025）是专为去量化GEMM优化的核，TileLang在相同任务上实现最高1.55倍的加速，表明通用框架可通过成本模型引导的tile配置超越手工特化核。

**FlashAttention-V3**（Dao, 2023）和**Block Sparse Attention (BSA)**（Guo et al., 2024）代表了注意力机制的极致优化。TileLang在FlashAttention上实现1.08–1.58倍加速，在BSA上实现3.42–7.87倍加速，证明了tile抽象在复杂访存模式下的表达能力。

### 方法变革的关键维度

TileLang相较于基线方法的变革体现在六个核心维度：

1. **内存放置控制**：从Triton的不透明编译器启发式或CUDA的手工放置，转变为`T.alloc_shared`（共享内存）和`T.alloc_fragment`（寄存器）的显式原语。

2. **Tile配置**：从手工试探或固定tile大小，转变为基于roofline成本模型的tile推荐，生成符合硬件tensor-core片段约束的候选短列表。

3. **内存布局确定**：从编译器推断或手工编写swizzle模式，转变为FTG上的层次化布局推断（严格推断、公共推断、自由推断三阶段约束传播）。

4. **流水线调度**：从手工插入异步拷贝/流水线阶段，转变为从串行代码自动推断流水线调度，仅暴露`num_stages`参数。

5. **Warp分区**：从隐式或手工warp调度，转变为显式的`policy=FullCol/FullRow`分区策略，配合成本模型引导的推荐。

6. **硬件可移植性**：从平台特定代码（CUDA/PTX vs. HIP/ROCm），转变为统一DSL配合后端特定tile库的`T.call_extern`调用。

### 适用边界与局限

**抽象层次的固有限制**：TileLang在tile级进行抽象与优化，无法直接控制子tile级别的硬件细节（如寄存器排布、bank冲突的具体模式）。这些底层优化仍依赖后端编译器（如cute/ck）的能力，意味着在需要极致寄存器级调优的场景下，手工CUDA仍可能保有优势。

**成本模型的静态假设**：静态roofline成本模型假设计算与访存完美重叠，实际动态效应（如DRAM刷新、缓存抖动、warp发散）可能导致估算偏差。虽然实验表明预测top-5%的调度保留了98.47%的最佳性能，但在访存模式高度不规则的核上，模型精度可能下降。

**硬件特性的依赖性**：某些优化（如warp specialization）高度依赖特定硬件特性（如Hopper架构的TMA单元）。消融实验揭示了平台差异的显著影响——在H100上warp分区贡献了4.34倍加速，而在MI300X上内存放置优化贡献了6.56倍加速。迁移至新架构（如Intel GPU、专用AI加速器）时，需要额外适配tile推荐规则和推断逻辑。

**自动调优的覆盖范围**：当前自动调优集中于tile形状、内存放置等维度。更复杂的调度组合（如算子融合策略、多kernel协同调度）尚需更多人工干预。GEMM上的平均调优时间（约10秒）虽显著低于Triton（约18-20秒）和Ansor（>400秒），但搜索空间仍受限于预定义的候选维度。

**工作负载的泛化性**：评估覆盖了9种算子（GEMM、Attention、MLA、BSA、Conv2D等），但对于更广泛的神经网络工作负载（如动态形状核、稀疏模式多变的核、图神经网络核）的性能泛化性尚待验证。

### 开放问题

1. **FTG的自动融合扩展**：TileLang的FTG能否进一步自动化支持未知的算子融合模式，而无需开发者重写tile级程序？当前融合边界仍由开发者通过tile程序的结构隐式定义。

2. **成本模型的动态演进**：能否结合运行时profiling数据，实现从静态roofline向动态模型的演进？例如，通过少量实测样本校准模型参数，在不显著增加调优开销的前提下提升预测精度。

3. **多设备与异构扩展**：如何将tile推荐扩展到多GPU或异构计算环境（如CPU+GPU联合调度）？tile的跨设备数据移动和同步将引入新的优化维度。

4. **新硬件的适配成本**：在支持新硬件时，需要多大比例的平台特定代码与推断规则？TileLang的多平台能力目前依赖于后端tile库的成熟度，对于缺乏类似cute/ck生态的硬件，适配成本可能显著增加。

5. **全自动搜索的可行性**：更大的tile编程空间探索（如同时优化tile大小、流水线深度、warp配置、融合策略）能否通过强化学习等全自动方法完成？当前的成本模型修剪策略已能剪除95%的候选，但剩余5%的搜索仍依赖枚举，在维度爆炸时可能成为瓶颈。



## 原文 PDF

![[paperPDFs/ICLR_2026/TileLang_Bridge_Programmability_and_Performance_in_Modern_Neural_Kernels.pdf]]
