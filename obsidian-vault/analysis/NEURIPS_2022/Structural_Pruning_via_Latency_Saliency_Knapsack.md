---
title: "Structural Pruning via Latency-Saliency Knapsack"
type: paper
paper_level: A
venue: NeurIPS
year: 2022
pdf_ref: paperPDFs/NEURIPS_2022/Structural_Pruning_via_Latency_Saliency_Knapsack.pdf
aliases:
- HALPH
- SPLSK
tags:
- NEURIPS_2022
- topic/optimization_theory_probabilistic
- topic/optimization_theory_probabilistic/optimization_methods
core_operator: "在给定的总延迟约束下，通过控制每层保留的神经元组数量（组大小由延迟阶梯步长确定），并根据重要性排序和动态延迟贡献，利用增强的背包算法选择一组保留的神经元，使得累积重要性最大。"
primary_logic: "将结构化剪枝重新形式化为一个带序约束的 0-1 背包问题：以神经元组为对象，泰勒展开梯度重要性作为“价值”，来自硬件延迟查找表的边际延迟贡献作为“重量”，在总延迟预算下最大化累积重要性；同时利用延迟阶梯特性进行分组，既提高了 GPU 利用率，又大幅降低了背包求解的复杂度，从而实现对延迟-准确度权衡的全局优化。"
claims:
- "HALP 将结构性剪枝形式化为在延迟约束下最大化准确度的全局资源分配问题。"
- "使用延迟查找表和全局显著性分数进行滤波器重要性排序。"
- "剪枝问题通过增强的背包求解器解决。"
- "神经元分组利用延迟步长大小，在降低计算开销的同时最大化 GPU 利用率。"
---

# Structural Pruning via Latency-Saliency Knapsack

> [!tip] 核心洞察
> 将结构化剪枝重新形式化为一个带序约束的 0-1 背包问题：以神经元组为对象，泰勒展开梯度重要性作为“价值”，来自硬件延迟查找表的边际延迟贡献作为“重量”，在总延迟预算下最大化累积重要性；同时利用延迟阶梯特性进行分组，既提高了 GPU 利用率，又大幅降低了背包求解的复杂度，从而实现对延迟-准确度权衡的全局优化。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 基于延迟-显著性背包的结构化剪枝 |
| 英文题名 | Structural Pruning via Latency-Saliency Knapsack |
| 会议/期刊 | NeurIPS 2022 |
| Links | [paper](https://arxiv.org/abs/2210.06659); [Project](https://halp-neurips.github.io/) |
| Topic | #topic/optimization_theory_probabilistic #topic/optimization_theory_probabilistic/optimization_methods |
| Method | Hardware-Aware Latency Pruning (HALP) |
| Dataset | ImageNet (ResNet50), ImageNet (ResNet101), PASCAL VOC (SSD), ImageNet (ResNet50, EagleEye baseline) |

> [!tip] 效果简介
> - ImageNet (ResNet50) 上，Top-1 Accuracy / Speedup (vs unpruned) 为 76.5% / 1.60× (HALP-55%)，对比 76.2% / 1× (No pruning)，变化 +0.3% / +0.60×。
> - ImageNet (ResNet101) 上，Top-1 Accuracy / Speedup (vs unpruned) 为 77.2% / 1.90× (HALP-40%)，对比 77.4% / 1× (No pruning)，变化 -0.2% / +0.90×。
> - PASCAL VOC (SSD) 上，mAP / Speedup (vs unpruned) 为 77.42 (0.56 mAP drop) / 1.94× (HALP)，对比 77.98 / 1× (No pruning)，变化 -0.56 mAP / +0.94×。

## 概述

结构化剪枝是压缩深度神经网络、加速推理的主流手段。现有方法普遍使用 FLOPs 或参数量作为剪枝的代理指标，但这些指标与真实硬件上的推理延迟之间存在显著的非线性偏差。在 GPU 等硬件上，卷积层的延迟随通道数变化呈阶梯状模式，逐层独立剪枝无法有效利用这一特性，导致即使大幅削减计算量也无法获得成比例的加速。因此，核心瓶颈在于：**如何在准确建模目标硬件延迟特性的同时，在全局延迟预算下最大化模型准确度**。

针对这一问题，本文提出 **Hardware-Aware Latency Pruning (HALP)**，将结构化剪枝重新形式化为一个带序约束的 0-1 背包问题。HALP 以神经元组为基本选择单元，利用一阶泰勒展开的梯度信息作为“价值”（重要性），以来自硬件延迟查找表的边际延迟贡献作为“重量”，在给定的总延迟约束下通过增强的背包求解器全局选择保留的神经元组合。同时，利用延迟阶梯步长进行动态分组，既提高了 GPU 利用率，又大幅降低了背包求解的复杂度。

在 ImageNet 上，HALP 对 ResNet-50 剪枝后实现 **1.60× 吞吐量提升**，Top-1 准确度反而提升 **0.3%**；对 ResNet-101 实现 **1.90× 加速**，准确度仅下降 0.2%。在 PASCAL VOC 目标检测任务上，HALP 以 0.56 mAP 的代价换取 **1.94× 加速**。与延迟感知的对比方法 **EagleEye**（Li et al., ECCV 2020）相比，HALP 在相同延迟约束下始终取得更高的准确度，且子网络搜索耗时仅为后者的约 1/4.3。

HALP 的核心价值在于将剪枝从“逐层局部贪心 + FLOPs 代理”的范式，推进到“全局延迟约束下的重要性最大化”这一更精确的优化框架，为硬件感知的结构化剪枝提供了可泛化的求解路径。

## 背景与动机

### 结构化剪枝的延迟错觉

深度神经网络在资源受限设备上的部署需求，驱动了结构化剪枝技术的快速发展。结构化剪枝通过移除整个卷积滤波器或通道，直接缩减网络宽度，理论上可同时降低计算量与推理延迟。然而，现有方法普遍使用 **FLOPs（浮点运算次数）** 作为剪枝的代理指标，这一做法隐含着一个危险假设：FLOPs 的减少与推理延迟的降低呈线性关系。

真实硬件上的延迟特性远比这一假设复杂。以 GPU 为例，卷积层的推理延迟呈现**阶梯状模式**（step-wise pattern）——延迟并非随通道数平滑变化，而是在特定的通道数区间内保持不变，到达阶梯边界时突然跃升。这一现象源于 GPU 的并行计算架构对特定张量形状的亲和性：当通道数恰好对齐硬件友好的块大小时，计算单元的利用率达到峰值；而在阶梯内部增减少量通道，延迟几乎不受影响。FLOPs 作为纯数学指标，完全无法捕捉这种硬件层面的非线性行为。

因此，一个以 FLOPs 最小化为目标的剪枝算法，可能移除大量通道却始终未能“跨过”延迟阶梯，导致计算量大幅下降而实际推理速度几乎不变——这正是**延迟错觉**的核心。

### 逐层独立剪枝的次优性

除代理指标的选择偏差外，现有方法的另一个结构性缺陷在于**剪枝决策的局部性**。大多数方法遵循“逐层独立剪枝”范式：为每一层单独设定剪枝率或重要性阈值，贪心地移除该层内最不重要的滤波器，最后将各层结果拼接为完整子网络。

这种局部贪心策略忽略了层间计算资源分配的全局耦合性。在总延迟预算下，不同层对延迟的边际贡献差异显著：某些层（如下采样层或瓶颈层）的通道数变化对总延迟影响巨大，而另一些层的影响微乎其微。逐层独立剪枝无法在层间进行资源的动态调配——它可能在延迟贡献小的层上过度剪枝，导致精度损失，同时在延迟贡献大的层上剪枝不足，浪费了宝贵的延迟预算。全局最优的剪枝方案，应当将更多通道保留在对精度敏感但对延迟不敏感的层中，而这需要一种跨层的联合优化视角。

### 从代理指标到硬件感知的范式转换

上述两个瓶颈——**代理指标偏差**与**决策局部性**——共同指向一个核心问题：如何在准确建模目标硬件延迟特性的同时，在全局延迟预算下最大化模型准确度？

HALP（Hardware-Aware Latency Pruning）针对这一问题提出了根本性的范式转换。其核心动机可概括为三个层面：

1. **延迟建模的精确化**：放弃 FLOPs 等间接代理，直接通过硬件延迟查找表（latency lookup table）获取任意输入/输出通道配置下每一层的真实推理延迟。查找表通过预先在目标硬件上逐配置测量构建，完整保留了延迟的阶梯状结构，使剪枝算法能够“看见”真实的延迟表面。

2. **剪枝决策的全局化**：将结构化剪枝重新形式化为一个带有顺序约束的 **0-1 背包问题**。以神经元组为基本选择单元，泰勒展开梯度重要性作为“价值”，来自硬件查找表的边际延迟贡献作为“重量”，在总延迟预算下最大化累积重要性。这一形式化使剪枝从逐层贪心转变为全局资源分配优化。

3. **硬件亲和的结构设计**：利用延迟阶梯步长（latency step size）确定神经元分组大小，使剪枝后的通道数天然对齐硬件友好的块边界，既提高了 GPU 利用率，又大幅降低了背包求解的搜索空间。

这一范式转换的直接效果是：HALP 在 ResNet-50 上以 1.60× 的吞吐量提升获得了 +0.3% 的 Top-1 准确度增益，在 ResNet-101 上以 1.90× 加速仅损失 0.2% 准确度——在结构化剪枝领域，同时实现显著加速与精度保持甚至提升，标志着硬件感知剪枝的重要进展。

## 核心创新

### 问题重定义：从局部剪枝到全局资源分配

现有结构化剪枝方法普遍将剪枝视为逐层独立的通道选择问题，使用 FLOPs 或参数量的百分比作为约束目标。然而，FLOPs 与真实硬件延迟之间存在显著的非线性映射——GPU 上卷积层的延迟呈**阶梯状模式**（latency step pattern），单纯减少计算量往往无法转化为实际的推理加速。HALP 的核心创新在于将结构化剪枝重新形式化为一个**全局资源分配优化问题**：在给定的硬件延迟预算 $C$ 下，跨所有层选择一组保留的神经元，使得累积重要性最大化：

$$\underset{p_1,\cdots,p_L}{\arg\max} \sum_{l=1}^L I_l(p_l), \quad \mathrm{s.t.} \sum_{l=1}^L T_l(p_{l-1},p_l) \leq C, \quad 0 \leq p_l \leq N_l$$

这一形式化将剪枝从“逐层削砍”转变为“全局背包选择”，使得不同层之间可以根据各自的延迟贡献和重要性进行权衡，从而在全局范围内逼近延迟-准确度的帕累托最优。

### 延迟建模：从代理指标到硬件查找表

**Changed Slot：延迟建模方式**

| 维度 | 基线方法 | HALP |
|------|----------|------|
| 延迟代理 | FLOPs 或参数量，与真实延迟非线性相关 | 逐层、逐通道的硬件延迟查找表（look-up table） |
| 延迟粒度 | 层级别或网络级别 | 通道级别，反映阶梯状延迟表面 |
| 适配性 | 与硬件无关 | 针对特定硬件预测量，可跨同架构系列复用 |

HALP 在目标硬件上预先测量所有可能的输入/输出通道组合下每层卷积的延迟，构建层级别的延迟查找表。对于第 $l$ 层，保留 $p_l$ 个通道时的延迟 $T_l(p_{l-1}, p_l)$ 可直接查表获得。进一步地，每个神经元的**边际延迟贡献**定义为：

$$c_l^j = T_l(p_{l-1},j) - T_l(p_{l-1},j-1), \quad 1 \leq j \leq p_l$$

这一设计使得延迟约束可以精确分解到单个神经元级别，为背包求解提供了准确的“重量”项。查找表构建开销约为 5 小时 GPU 时间（ResNet 系列），但可在同架构系列网络中复用。

### 重要性度量：梯度驱动的全局显著性

**Changed Slot：神经元重要性度量**

| 维度 | 基线方法 | HALP |
|------|----------|------|
| 度量方式 | L2 范数或平方形式的泰勒展开 | 一阶泰勒展开的**绝对值**形式 |
| 计算依据 | 权重幅值 | BN 层缩放因子 $\gamma$ 和偏置 $\beta$ 的梯度 |
| 排序范围 | 层内独立排序 | 层内降序排列后全局背包选择 |

HALP 采用基于一阶泰勒展开的神经元重要性分数，利用 BN 层的参数梯度近似剪除该神经元造成的损失变化：

$$\mathcal{T}_l^n = \left| g_{\gamma_l^n} \gamma_l^n + g_{\beta_l^n} \beta_l^n \right|$$

其中 $g_{\gamma_l^n}$ 和 $g_{\beta_l^n}$ 分别为损失对 BN 层缩放因子和偏置的梯度。绝对值形式避免了正负梯度相互抵消的问题，消融实验（Table 12）表明该度量在较高剪枝率下显著优于 L2 范数。各层神经元按重要性降序排列后，层重要性累积为 $I_l(p_l) = \sum_{j=1}^{p_l} \mathcal{Z}_l^j$，其中 $\mathcal{Z}_l^1 \ge \cdots \ge \mathcal{Z}_l^{N_l}$。

### 背包求解：带序约束的增强动态规划

**Changed Slot：剪枝选择算法**

| 维度 | 基线方法 | HALP |
|------|----------|------|
| 选择策略 | 逐层独立剪枝或局部贪心 | 全局背包问题求解 |
| 约束类型 | 单层通道数或 FLOPs 比例 | 总延迟预算 $C$ |
| 顺序约束 | 无 | 必须从最重要神经元开始连续保留 |

HALP 将剪枝选择形式化为一个**带序约束的 0-1 背包问题**：

$$\operatorname*{max} \sum_{l=1}^{L} \sum_{j=1}^{p_l} \mathcal{Z}_l^j, \quad \mathrm{s.t.} \sum_{l=1}^{L} \sum_{j=1}^{p_l} c_l^j \leq C, \quad 0 \leq p_l \leq N_l, \quad \mathcal{Z}_l^1 \geq \mathcal{Z}_l^2 \geq \dots \mathcal{Z}_l^{N_l}$$

其中 $\mathcal{Z}_l^j$ 为“价值”（重要性），$c_l^j$ 为“重量”（延迟贡献），序约束 $\mathcal{Z}_l^1 \ge \mathcal{Z}_l^2 \ge \dots$ 确保每层保留的神经元是从最重要开始的一段连续前缀。增强的动态规划算法（Algorithm 1）利用贪心近似加速求解，消融实验（Table 16）表明贪心版本与非贪心版本在 ImageNet 上的最终性能几乎一致，验证了该近似的高效性。

### 通道分组：利用延迟阶梯特性

**Changed Slot：通道分组策略**

| 维度 | 基线方法 | HALP |
|------|----------|------|
| 分组方式 | 固定大小分组或无分组 | 根据硬件延迟阶梯步长动态确定 |
| 分组依据 | 启发式规则 | 硬件延迟查找表中的步长大小 $s$ |
| 跨层一致性 | 各层独立 | 残差连接等跨层结构统一分组 |

GPU 等硬件上卷积层的延迟随通道数呈阶梯状变化——通道数在某个步长 $s$ 内增加时延迟几乎不变，超过步长后延迟跃升。HALP 利用这一特性，将每层 $s$ 个通道分为一组（$s$ 等于延迟阶梯步长），组内聚合重要性和延迟贡献。这一策略带来三重收益：(1) 剪枝后的结构落在延迟阶梯的“平台”上，最大化 GPU 利用率；(2) 背包求解的物品种类数大幅减少，加速求解过程；(3) 对于残差连接等跨层结构，统一分组保证了通道数的一致性。消融实验（Figure 4）证实，延迟感知的分组策略（LG）在相同延迟约束下始终优于固定大小分组。

### 迭代剪枝调度

**Changed Slot：剪枝调度**

| 维度 | 基线方法 | HALP |
|------|----------|------|
| 执行方式 | 一次性剪枝或固定步骤 | $k$ 个里程碑的迭代剪枝 |
| 预算调整 | 固定目标 | 指数调度逐渐降低延迟预算 |

HALP 在训练过程中设置 $k$ 个里程碑，延迟预算按指数调度从初始值逐渐降低至最终目标，每个里程碑执行一次全局背包选择并继续训练恢复精度。这种渐进式剪枝策略避免了单次大幅剪枝造成的不可逆精度损失，使得网络有充分时间适应结构变化。

## 整体框架

HALP 将结构化剪枝重新形式化为一个带延迟约束的全局资源分配问题，其整体 pipeline 由五个核心模块串联而成，形成“测量—评估—选择—执行—迭代”的闭环。

**输入**：一个预训练的稠密网络、目标硬件平台、目标延迟预算 $C$。

**Pipeline 流程**：

1. **延迟查找表构建**（离线）：在目标硬件上预先测量每一层在所有可能的输入/输出通道组合下的推理延迟，生成层级别的延迟查找表 $T_l(p_{l-1}, p_l)$。该表捕捉了 GPU 等硬件上卷积层延迟的阶梯状模式，是后续全局优化的基础。

2. **神经元重要性提取与排序**（在线，每次剪枝迭代执行）：通过一次前向-反向传播，计算每个 BN 层的缩放参数 $\gamma$ 和偏置参数 $\beta$ 的梯度，按式 $\mathcal{T}_l^n = \left| g_{\gamma_l^n} \gamma_l^n + g_{\beta_l^n} \beta_l^n \right|$ 得到每个神经元的重要性分数，并在层内按降序排列。

3. **延迟贡献动态调整与分组**：根据当前层保留的神经元数量，从查找表中动态计算每个神经元的边际延迟贡献 $c_l^j = T_l(p_{l-1}, j) - T_l(p_{l-1}, j-1)$。随后，按硬件延迟阶梯步长 $s$ 将神经元分组，组内聚合重要性和延迟贡献，既利用延迟阶梯特性最大化 GPU 利用率，又将背包问题的物品数量从神经元级压缩到组级，大幅降低求解复杂度。

4. **增强的背包求解器**：将每组神经元视为带有“价值”（聚合重要性）和“重量”（聚合延迟贡献）的物品，并施加层内重要性排序约束（保留的神经元必须是从最重要开始的连续前缀），运行增强的动态规划算法在总延迟预算 $C$ 下选择最优保留组集合，最大化累积重要性。

5. **迭代剪枝调度与微调**：在训练过程中设置 $k$ 个里程碑，延迟预算按指数调度从初始值逐步降至目标值。每个里程碑执行一次完整的全局背包选择，剪枝后继续训练以恢复精度。

**输出**：满足目标延迟约束且准确度最大化的剪枝网络结构。

**关键设计决策**：与逐层独立剪枝或基于 FLOPs 代理的方法不同，HALP 通过延迟查找表直接建模真实硬件延迟，并在全局背包框架下统一优化所有层的通道分配，从而在延迟-准确度权衡上获得显著优势。

## 核心模块与公式推导

### 3.1 问题形式化：从局部剪枝到全局资源分配

HALP 将结构化剪枝重新定义为在延迟预算约束下最大化累积重要性的全局优化问题。给定原始网络权重 $\mathbf{W}$，剪枝后权重 $\hat{\mathbf{W}}$ 需满足：

$$
\underset{\mathbf{\hat{W}}}{\arg\min} \ \mathcal{L}(\hat{\mathbf{W}},\mathcal{D}) \quad \mathrm{s.t.} \quad \Phi(f(\hat{\mathbf{W}},x_i)) \leq C \tag{1}
$$

其中 $\mathcal{L}$ 为任务损失，$\Phi(\cdot)$ 为资源度量函数（在 HALP 中即端到端推理延迟），$C$ 为预设的延迟预算。

将式 (1) 转化为逐层选择问题：设第 $l$ 层保留 $p_l$ 个神经元（通道），$N_l$ 为该层原始神经元数，则该层的总重要性为 $I_l(p_l)$，延迟贡献为 $T_l(p_{l-1}, p_l)$（依赖上一层的输出通道数 $p_{l-1}$）。全局优化目标为：

$$
\underset{p_1,\cdots,p_L}{\arg\max} \sum_{l=1}^L I_l(p_l), \quad \mathrm{s.t.} \sum_{l=1}^L T_l(p_{l-1},p_l) \leq C, \quad 0 \leq p_l \leq N_l \tag{2}
$$

### 3.2 神经元重要性度量：一阶泰勒展开

HALP 使用基于梯度的显著性分数来近似剪除单个神经元造成的损失变化。对于第 $l$ 层的第 $n$ 个神经元，利用 BN 层的缩放因子 $\gamma_l^n$ 和偏置 $\beta_l^n$ 的一阶泰勒展开，其重要性定义为：

$$
\mathcal{T}_l^n = \left| g_{\gamma_l^n} \gamma_l^n + g_{\beta_l^n} \beta_l^n \right| \tag{3}
$$

其中 $g_{\gamma_l^n}$ 和 $g_{\beta_l^n}$ 分别为损失对 $\gamma_l^n$ 和 $\beta_l^n$ 的梯度。该绝对值形式相比平方形式在消融实验中表现出更好的剪枝性能（Table 12）。

在每层内部，神经元按重要性降序排列：

$$
I_l(p_l) = \sum_{j=1}^{p_l} \mathcal{Z}_l^j, \quad 0 \le p_l \le N_l, \quad \mathcal{Z}_l^1 \ge \cdots \ge \mathcal{Z}_l^{N_l} \tag{4}
$$

其中 $\mathcal{Z}_l^j$ 为第 $l$ 层排序后第 $j$ 个重要神经元的重要性分数。这一排序约束是后续背包求解中“序依赖”的核心来源——保留 $p_l$ 个神经元意味着必须保留前 $p_l$ 个最重要的神经元。

### 3.3 延迟建模：硬件查找表与边际贡献

HALP 的核心创新之一是抛弃 FLOPs 等代理指标，直接建模目标硬件上的真实延迟。通过预先在目标设备上测量所有可能的输入/输出通道组合下的卷积层延迟，构建逐层延迟查找表（latency look-up table）。对于第 $l$ 层，给定输入通道数 $p_{l-1}$ 和输出通道数 $p_l$，其延迟 $T_l(p_{l-1}, p_l)$ 直接从查找表中获取。

为将层延迟分解为单个神经元的边际贡献，定义第 $j$ 个神经元的延迟增量为：

$$
c_l^j = T_l(p_{l-1}, j) - T_l(p_{l-1}, j-1), \quad 1 \leq j \leq p_l \tag{6}
$$

则层延迟可表示为各神经元延迟贡献之和：

$$
T_l(p_{l-1},p_l) = \sum_{j=1}^{p_l} c_l^j, \quad 0 \le p_l \le N_l \tag{5}
$$

这种分解方式使得延迟约束可以精确到单个神经元粒度，为后续背包求解提供了“物品重量”。

### 3.4 增强背包求解器：带序约束的 0-1 背包

综合以上建模，HALP 将剪枝问题转化为一个带顺序约束的 0-1 背包问题：

$$
\operatorname*{max} \sum_{l=1}^{L} \sum_{j=1}^{p_l} \mathcal{Z}_l^j, \quad \mathrm{s.t.} \sum_{l=1}^{L} \sum_{j=1}^{p_l} c_l^j \leq C, \quad 0 \leq p_l \leq N_l, \quad \mathcal{Z}_l^1 \geq \mathcal{Z}_l^2 \geq \dots \mathcal{Z}_l^{N_l} \tag{7}
$$

其中每个神经元可视为一个“物品”，其“价值”为重要性分数 $\mathcal{Z}_l^j$，“重量”为延迟贡献 $c_l^j$。关键约束是每层内的物品必须按重要性降序依次选取——不能跳过前面的神经元而选择后面的。这一序依赖约束通过增强的动态规划算法（Algorithm 1）求解，其贪心近似版本（Algorithm 1）与非贪心精确版本（Algorithm 2）在 ImageNet 上的最终性能几乎一致（Table 16），验证了贪心近似的高效性。

### 3.5 延迟感知的神经元分组

GPU 等硬件上卷积层的延迟呈阶梯状模式——通道数的变化在达到特定步长（latency step size）时才会引起延迟跳变。HALP 利用这一特性进行神经元分组：将每层中延迟步长大小 $s$ 个通道聚合为一个“超级神经元组”，组内的重要性分数和延迟贡献分别求和。分组后，背包求解的物品数量大幅减少，求解效率显著提升，同时剪枝后的结构天然对齐硬件延迟阶梯，最大化 GPU 利用率。消融实验（Figure 4）表明，这种延迟感知分组（LG）在相同延迟约束下始终优于固定大小的启发式分组。

### 3.6 迭代剪枝调度

HALP 采用 $k$ 个里程碑的迭代剪枝策略。在每个里程碑处执行一次完整的全局背包选择，延迟预算按指数调度逐步降低至最终目标值。每次剪枝后网络继续训练以恢复精度。这一渐进式调度避免了单次激进剪枝带来的不可逆精度损失，使网络能够在剪枝-微调的交替中逐步适应稀疏结构。

## 实验与分析

### 核心实验结果

HALP 在 ImageNet 分类任务上对多种架构进行了结构化剪枝评估，目标硬件为 NVIDIA Titan V GPU。**Table 1** 汇总了与现有方法的全面对比，**Figure 2** 以散点图形式展示了准确度-效率的权衡关系。

![[assets/figures/papers/paper_list_l28_https_arxiv_org_abs_2210_06659/figures/003_Table_1.jpg]]
*Table 1: ImageNet structural pruning results. We compare HALP for ResNet50 with two different dense baselines (left), ResNet101 and VGG16 (right up), MobileNet-V1 and MobileNet-V2 (right bottom) pruning experiments, with detailed comparison to state-of-the-art pruning methods over varying performance metrics. More comparisons and CIFAR10 experiments can be found in Appendix C*

**ResNet50 结果**：在 PyTorch 密集基线（Top-1 76.2%）上，HALP-55%（保留 55% 延迟预算）实现了 **76.5% 的 Top-1 准确度，同时推理吞吐量提升 1.60×**——准确度反而比未剪枝模型高出 0.3 个百分点。当使用与 EagleEye 相同的更强基线（Top-1 77.23%）时，HALP-55% 达到 76.6% 准确度和 1.64× 加速比，而 **EagleEye** (Li et al., ECCV 2020) 的 EagleEye-2G 仅获得 76.4% 准确度和 1.44× 加速比（见 **Figure 8**）。在更激进的 HALP-30% 设置下，准确度为 74.3%，加速比达到 2.55×。引入知识蒸馏（教师模型 RegNetY-16GF，Top-1 82.9%）后，HALP 的准确度-效率前沿进一步上移。

**ResNet101 结果**：HALP-40% 在 Top-1 准确度仅下降 0.2 个百分点（77.2% vs 77.4%）的情况下，实现了 **1.90× 的吞吐量提升**。

**轻量级网络结果**：在 MobileNet-V1 上，HALP-42% 达到 68.3% 准确度和 2.32× 加速比；在 MobileNet-V2 上，HALP-60% 达到 70.4% 准确度和 1.84× 加速比，均显著优于 **AutoSlim** (Yu et al., NeurIPS 2019) 和 **MetaPruning** (Liu et al., ICCV 2019) 等方法。

**跨硬件平台泛化**：**Figure 3** 展示了在 NVIDIA Jetson TX2、Intel Xeon E5 CPU 和 NVIDIA Xavier 三种不同硬件上的剪枝结果。HALP 在所有平台上均保持了优于 EagleEye 的准确度-延迟权衡，验证了延迟查找表方法对不同硬件特性的适应能力。

**TensorRT 量化加速**：**Table 2** 报告了在 RTX 3080 上使用 TensorRT INT8 量化的结果。HALP-30% 相比 PyTorch 密集基线实现了 **14.12× 的总加速比**，而 EagleEye-1G 为 12.29×，HALP 额外获得 1.83× 的优势。

**目标检测任务**：在 PASCAL VOC 上使用 SSD 检测框架，HALP 在 mAP 仅下降 0.56（77.98 → 77.42）的情况下，实现了 **1.94× 的推理加速**，证明了该方法在检测任务上的有效性。

### 消融实验

**神经元重要性度量**：**Table 12** 对比了基于一阶泰勒展开的梯度重要性（First-Taylor）与传统的 L2 范数重要性。在相同延迟约束下，First-Taylor 在所有剪枝率下均优于 L2 范数，且在高剪枝率时差距更加显著——这验证了梯度信息对准确度保持的关键作用。

**延迟感知分组策略**：**Figure 4** 对比了 HALP 提出的延迟感知分组（LG）与多种固定大小分组策略。LG 根据每层的延迟阶梯步长动态确定分组大小，在相同延迟约束下始终获得最高的 Top-1 准确度。**Figure 6** 在 MobileNet-V1 上进一步确认了这一结论。该策略的核心机制在于：分组大小与硬件延迟阶梯对齐，既提高了 GPU 利用率，又大幅降低了背包求解的复杂度。

**贪心背包求解器的有效性**：**Table 16** 对比了贪心增强背包求解器（Algorithm 1）与非贪心版本（Algorithm 2）在 ImageNet 上的最终性能，两者几乎一致，验证了贪心近似在保持解质量的同时显著提升了求解效率。

**剪枝步数的影响**：**Figure 7** 探索了不同剪枝步数 k 对最终性能的影响，结果表明迭代剪枝调度（指数衰减的延迟预算）对准确度恢复有积极作用。

**计算开销对比**：**Table 3** 显示 HALP 的子网络选择阶段仅需约 0.3 GPU 小时，比次优方法快约 4.3×，这得益于增强背包求解器的高效性和神经元分组带来的搜索空间缩减。

### 延迟建模的准确性

**Figure 11** 展示了 HALP 预测的延迟减少量与真实延迟减少量之间的强线性相关性（相关系数接近 1），验证了逐层延迟查找表对硬件行为的准确建模能力。**Figure 9** 通过两个示例层展示了 HALP 与 EagleEye 剪枝后层落在延迟表面上的位置差异：HALP 倾向于选择延迟阶梯的“拐点”处，从而在几乎不增加延迟的情况下保留更多重要通道，而 EagleEye 的独立剪枝策略无法利用这一硬件特性。

### 失败模式与局限性分析

尽管 HALP 在多数场景下表现优异，分析揭示了以下几个局限：

1. **复杂拓扑的延迟估计偏差**：逐层延迟查找表假设层间串行执行，未考虑 GPU 内的层间并行和缓存效应。对于具有多条并行路径的网络（如 InceptionNet），这种简化可能导致延迟估计不够准确，需要手动验证。

2. **查找表构建开销**：为目标硬件预先构建延迟查找表需要约 5 小时 GPU 时间（以 ResNet 系列为例），且该表仅适用于同架构系列网络。当剪枝目标切换到新硬件平台时，需要重新测量。

3. **极端剪枝率下的粒度限制**：分组策略虽然利用了延迟阶梯特性提高效率，但在极端剪枝率下可能限制了解的粒度，导致准确度恢复不充分。此时可能需要动态调整分组策略以平衡求解速度和解的质量。

4. **跨架构迁移成本**：延迟查找表与硬件和网络架构系列强绑定，限制了该方法在新型架构上的快速部署。如何通过少量采样和外推来快速适配新硬件，仍是一个开放问题。

### 补充图表

![[assets/figures/papers/paper_list_l28_https_arxiv_org_abs_2210_06659/figures/010_Table_6.jpg]]
*Table 6: Pruning MobileNet-V1 and MobileNet-V2 on the ImageNet dataset with different targets*

![[assets/figures/papers/paper_list_l28_https_arxiv_org_abs_2210_06659/figures/015_Figure_9.jpg]]
*Figure 9: Two examples of pruned layers from HALP model and EagleEye [32] model. The scattered black points are the locations of the layers fall to after pruning*

![[assets/figures/papers/paper_list_l28_https_arxiv_org_abs_2210_06659/figures/030_Figure_13.jpg]]
*Figure 13: Visualization of the pruned ResNet50 structure*

![[assets/figures/papers/paper_list_l28_https_arxiv_org_abs_2210_06659/figures/004_Figure_3.jpg]]
*Figure 3: Original model EagleEye Li et al. ECCV (2020) AutoSlim Yu et al. NeurIPS (2019) r x RN50 He et al. (2015) MetaPruning Liu et al. ICCV (2019a) GReg Wang et al. ICLR (2021) HALP (Ours) Figure 3: Pruning ResNet50 on the ImageNet dataset with NVIDIA Jetson TX2 (left), Intel CPU Xeon E5 (middle) and NVIDIA Xavier (right). The latency on Jetson TX2 and CPU is measured using PyTorch; on Xavier is measured using TensorRT FP32. Top-left is better*

![[assets/figures/papers/paper_list_l28_https_arxiv_org_abs_2210_06659/figures/005_Table_2.jpg]]
*Table 2: HALP acceleration of ResNet50 on GPUs with TensorRT (version 7.2.1.6)*

![[assets/figures/papers/paper_list_l28_https_arxiv_org_abs_2210_06659/figures/006_Table_3.jpg]]
*Table 3: Comparison of extra computation required by pruning methods on ImageNet. Our approach is around 4.3× faster than the next best method. Sub-network selection timing is approximated as running on same device (a NVIDIA V100)*

![[assets/figures/papers/paper_list_l28_https_arxiv_org_abs_2210_06659/figures/009_Table_5.jpg]]
*Table 5: Additional pruning results and comparison on CIFAR10 and ImageNet dataset. FLOPS (%) are relative to those of the unpruned network*

![[assets/figures/papers/paper_list_l28_https_arxiv_org_abs_2210_06659/figures/016_Table_7.jpg]]
*Table 7: Pruning ResNet50 on the ImageNet dataset (TITAN V) targeting on inference with batch size 1. HALP-X% indicates that X% latency to remain after pruning. The speedup is calculated as the ratio of FPS between the pruned network and the unpruned model*

![[assets/figures/papers/paper_list_l28_https_arxiv_org_abs_2210_06659/figures/017_Table_8.jpg]]
*Table 8: HALP for object detection on the PASCAL VOC dataset*

![[assets/figures/papers/paper_list_l28_https_arxiv_org_abs_2210_06659/figures/018_Table_9.jpg]]
*Table 9: The additional convolution layers in SSD*

![[assets/figures/papers/paper_list_l28_https_arxiv_org_abs_2210_06659/figures/020_Table_10.jpg]]
*Table 10: Pruning ResNet50 on the ImageNet dataset with FLOPs constraint and comparison with state-of-the-art method EagleEye (ECCV’20) [32]. We remeasure the FLOPs, top1 and top5 accuracy of EagleEye to get results with two digits*

## 方法谱系与知识库定位

### 结构化剪枝范式的演进定位

HALP 处于结构化剪枝从“局部贪心-代理指标”范式向“全局优化-硬件感知”范式转型的关键节点。传统结构化剪枝方法的核心逻辑是：先定义滤波器重要性度量（如 L1/L2 范数、BN 缩放因子），再逐层按比例或阈值剪除低分滤波器，最后微调恢复精度。这一范式存在两个根本性缺陷：

1. **代理指标失配**：FLOPs 或参数量作为效率代理，与真实硬件延迟呈非线性且不准确的映射关系。GPU 上卷积层的延迟表面呈阶梯状模式——延迟仅在通道数跨越特定步长（如 32 或 64）时才显著变化，逐层独立剪枝无法利用这一特性。
2. **局部决策次优**：逐层独立分配剪枝率忽略了层间延迟贡献的差异性和互补性，无法在全局延迟预算下最大化累积重要性。

HALP 通过三个关键创新突破了上述瓶颈：将剪枝形式化为带序约束的 0-1 背包问题、引入硬件延迟查找表作为精确约束、利用延迟阶梯步长进行神经元分组以降低求解复杂度。这一框架使剪枝决策从“局部贪心剪除”升级为“全局资源分配优化”。

### 与同期延迟感知方法的对比

**EagleEye** (Li et al., ECCV 2020) 是延迟感知剪枝的代表性工作，采用蒙特卡洛采样生成候选子网络结构，再通过性能预测模型评估并选择最优结构。HALP 与 EagleEye 的核心差异在于：

| 维度 | EagleEye | HALP |
|------|----------|------|
| 搜索策略 | 随机采样 + 评估 | 确定性背包优化 |
| 延迟建模 | 隐式（通过采样结构测量） | 显式（预建逐层查找表） |
| 全局性 | 结构级评估，但搜索非全局最优 | 全局背包求解，理论保证 |
| 计算开销 | 高（需采样大量候选并测量） | 低（查找表查询 + 动态规划） |

实验证据表明，在相同 PyTorch 基线模型（Top-1 77.23%）下，HALP 在准确度和延迟两个维度上均超越 EagleEye（Figure 8）。在 ResNet50 上，HALP-55% 达到 76.6% 准确度 / 1.64× 加速，而 EagleEye-2G 仅 76.4% / 1.44×（Table 1）。子网络选择阶段的计算开销方面，HALP 比次优方法快约 4.3×（Table 3），这得益于背包求解器的高效性。

**AutoSlim** (Yu et al., NeurIPS 2019) 采用可瘦身网络（slimmable network）训练，通过逐步调整通道宽度搜索最优配置。其局限性在于训练过程需维护多个宽度配置，且搜索粒度受限于预定义的宽度集合。HALP 的延迟查找表支持任意通道配置的延迟查询，搜索空间更灵活。

**MetaPruning** (Liu et al., ICCV 2019) 利用元学习生成候选剪枝结构的权重，再通过进化算法搜索最优结构。该方法同样依赖大量候选评估，且元学习训练过程复杂。HALP 避免了候选采样和评估的循环，直接通过优化求解得到剪枝方案。

### 关键设计选择的消融支撑

HALP 的每个核心组件均有消融实验支撑其有效性：

- **神经元重要性度量**：基于一阶泰勒展开的绝对值形式（式 3）优于 L2 范数，尤其在较高剪枝率下差距更显著（Table 12）。这验证了梯度信息相比静态权重幅值更能反映神经元对损失函数的真实贡献。

- **延迟感知分组策略**：根据硬件延迟阶梯步长动态确定分组大小（LG），在相同延迟约束下始终优于固定大小分组，获得更高的 Top-1 准确度（Figure 4）。这证明了利用硬件特性指导分组的重要性。

- **贪心增强背包求解器**：贪心版本（Algorithm 1）与非贪心版本（Algorithm 2）在 ImageNet 上的最终性能几乎一致（Table 16），验证了贪心近似在保持全局最优性的同时大幅降低了求解开销。

### 方法适用边界与局限

HALP 的有效性建立在以下前提之上，超出这些边界时性能可能下降：

1. **延迟查找表的构建成本与可迁移性**：为目标硬件预建查找表需要约 5 小时 GPU 时间（以 ResNet 系列为例），且该表仅适用于同架构系列网络。当剪枝目标切换到新硬件平台时，需重新测量和创建查找表。这限制了 HALP 在快速硬件迭代场景下的部署效率。

2. **层间并行与缓存效应的忽略**：逐层延迟查找表假设层间执行是串行的，未考虑 GPU 内部的层间并行执行和内存缓存行为。对于具有多条并行路径的网络（如 InceptionNet、NAS 生成的复杂架构），延迟估计可能不够准确。这是论文明确指出的局限。

3. **分组策略的粒度限制**：虽然延迟阶梯分组提高了求解效率和 GPU 利用率，但在极端剪枝率下可能限制了解的粒度，导致准确度恢复不充分。当延迟预算极低时，粗粒度分组可能跳过某些“中等重要性但延迟贡献小”的神经元组合。

4. **对 BN 层的依赖**：神经元重要性计算依赖 BN 层的缩放因子 γ 和偏置 β 的梯度（式 3）。对于无 BN 层的架构（如 Transformer 中的 LayerNorm），需要重新设计重要性度量。

### 开放问题与后续研究方向

1. **延迟建模的精细化**：如何将 GPU 内的层间并行执行和内存缓存行为融入延迟查找表，以提高对复杂架构的延迟估计精度？一个可能的方向是引入图级别的延迟模型，考虑计算流图中的并行路径。

2. **查找表的快速适配**：延迟查找表能否通过少量采样和外推/线性校准来快速适配新硬件，从而减少测量开销？Figure 11 展示了预测延迟减少与实际延迟减少之间的线性相关性，这暗示了外推的可行性。

3. **与神经架构搜索的融合**：能否将 HALP 框架与 NAS 结合，同时搜索最优的剪枝率和通道配置？HALP 的背包求解器本质上是一个资源分配优化器，可以扩展为同时搜索剪枝和扩展的联合优化。

4. **动态分组策略**：在更严格的延迟约束下，是否需要动态调整分组策略以平衡求解速度和解的质量？当前固定步长分组可能在极端约束下不是最优。

5. **在线延迟校准**：如何在训练过程中自动学习或微调延迟查找表的线性校准系数，使延迟估计随训练进程自适应调整？这可以减少对预建查找表的依赖。

## 原文 PDF

![[paperPDFs/NEURIPS_2022/Structural_Pruning_via_Latency_Saliency_Knapsack.pdf]]
