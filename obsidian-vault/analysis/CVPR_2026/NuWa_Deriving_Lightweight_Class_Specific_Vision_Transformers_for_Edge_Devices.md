---
title: "NuWa: Deriving Lightweight Class-Specific Vision Transformers for Edge Devices"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/NuWa_Deriving_Lightweight_Class_Specific_Vision_Transformers_for_Edge_Devices.pdf
project_link: null
code_link: "https://github.com/CGCL-codes/NuWa"
aliases:
- NuWa
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过自我知识净化（SKP）学习二值化掩码自主识别并剪除类别有害权重，并结合多元注意力（MHA）与多层感知器（MLP）模块的低秩分解与闭式优化，实现无需重训练的快速结构化剪枝。
primary_logic: 在类别特定的模型压缩中，移除有害于目标类别的权重可以提升性能；将剪枝形式化为矩阵低秩逼近和最小二乘问题，利用闭式解可避免重训练，大幅提高剪枝效率，使大规模定制成为可能。
claims:
- 随机移除MLP神经元可提高特定类别准确率，揭示了类别有害权重的存在。
- NuWa在类特定任务上超越训练无关方法高达29.00%准确率，且比最好的训练相关方法提速33.69倍，成本降低99.83%。
- ImageNet-1K sub-tasks (DeiT-Base, |S|=25), overall best 上 Class-specific accuracy improvement over training-free meth... = NuWa
- ImageNet-1K sub-tasks (DeiT-Base), pruning rate 0.40 上 Average class-specific accuracy improvement = NuWa
---

# NuWa: Deriving Lightweight Class-Specific Vision Transformers for Edge Devices

> [!tip] 核心洞察
> 在类别特定的模型压缩中，移除有害于目标类别的权重可以提升性能；将剪枝形式化为矩阵低秩逼近和最小二乘问题，利用闭式解可避免重训练，大幅提高剪枝效率，使大规模定制成为可能。

| 字段 | 内容 |
|------|------|
| 中文题名 | NuWa：面向边缘设备的轻量级类别特定视觉Transformer派生方法 |
| 英文题名 | NuWa: Deriving Lightweight Class-Specific Vision Transformers for Edge Devices |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Wei_NuWa_Deriving_Lightweight_Class-Specific_Vision_Transformers_for_Edge_Devices_CVPR_2026_paper.html) · [Code](https://github.com/CGCL-codes/NuWa) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | NuWa |
| Dataset | ImageNet-1K sub-tasks (DeiT-Base, /S/=25), overall best, ImageNet-1K sub-tasks (DeiT-Base), pruning rate 0.40, ImageNet-1K sub-tasks (DeiT-Base), pruning rate 0.60, Pruning efficiency |

> [!tip] 效果简介
> - ImageNet-1K sub-tasks (DeiT-Base, |S|=25), overall best 上，Class-specific accuracy improvement over training-free methods NuWa vs Best training-free method (+29.00%)。
> - ImageNet-1K sub-tasks (DeiT-Base), pruning rate 0.40 上，Average class-specific accuracy improvement NuWa vs Training-free methods (+15.37%)。
> - ImageNet-1K sub-tasks (DeiT-Base), pruning rate 0.60 上，Average class-specific accuracy improvement NuWa vs Training-free methods (+10.04%)。

## 概要

**问题瓶颈**：现有的视觉Transformer（ViT）剪枝方法普遍采用类无关（class-agnostic）的重要性评估策略，对所有类别平等对待，无法为特定类别任务提供定制化的轻量模型。更重要的是，这些方法忽视了模型中存在的**类别有害权重**（class-detrimental weights）——某些神经元对特定类别的识别反而起负面作用。此外，剪枝后通常需要昂贵的重训练来恢复精度，使得为大规模、多样化的边缘设备场景逐一派生定制模型变得不切实际。

**核心洞察**：NuWa的核心发现是，在类别特定的模型压缩中，**主动移除对目标类别有害的权重不仅可以压缩模型，还能提升该类别的识别精度**（Figure 1）。基于此，NuWa将剪枝问题形式化为两个可闭式求解的优化问题——多头注意力（MHA）的低秩矩阵逼近和MLP的激活重构最小二乘问题——从而完全避免了重训练，实现了极速的结构化剪枝。

**方法定位**：NuWa是一种**无需重训练的类别特定ViT剪枝框架**，包含两个阶段：
1. **自我知识净化（SKP）**：冻结基础ViT，在MLP模块中嵌入可学习的二值化掩码，通过目标类别数据驱动的方式自动识别并剪除类别有害权重，生成更小且精度更高的锚点模型。
2. **优化驱动快速剪枝（OFP）**：将MHA和MLP模块的进一步剪枝分别形式化为低秩逼近和伪逆求解问题，利用闭式解直接获得剪枝后的权重，无需任何重训练。

**主要结果**：
- 在ImageNet-1K的类别特定子任务上，NuWa相比最优训练无关剪枝方法**准确率提升高达29.00%**，相比训练相关方法实现**33.69倍加速**，在大规模派生场景（50个子任务×10个资源约束）下**成本降低高达99.83%**，而平均精度损失仅为0.61%。
- 派生出的边缘ViT在Jetson Orin NX上实现**1.31×至2.07×的推理加速**。



### 边缘部署的“一刀切”困境

视觉Transformer（ViT）在图像识别任务中表现卓越，但其庞大的参数量和计算开销使其难以直接部署到资源受限的边缘设备（如Jetson Orin NX）。剪枝是缓解这一矛盾的主流手段，但现有剪枝方法几乎都遵循**类无关（class-agnostic）**范式：它们对所有类别使用相同的重要性评分标准（如权重幅度、梯度、激活值等），统一移除“不重要”的参数，再通过昂贵的重训练恢复精度。

然而，边缘场景的实际需求往往是**类别特定（class-specific）**的——一个部署在超市的识别系统可能只需要精确区分50种商品，而非ImageNet的全部1000类。类无关剪枝无法感知这种类别偏好，导致两个根本性缺陷：

1. **无法移除类别有害权重**：某些参数对全局任务是“重要”的，但对目标类别却是干扰源。类无关方法会保留这些权重，从而损害特定类别的准确率。
2. **定制成本不可承受**：若为每个子任务和每种资源约束都从头执行“剪枝+重训练”，在大规模部署场景下（例如N个子任务×M个约束级别），时间和算力开销将呈指数级膨胀。

### 一个被忽视的现象：剪枝可以提升准确率

Figure 1 展示了一个反直觉的发现：在DeiT-Base的MLP模块中**随机移除部分神经元**，竟然意外地提高了模型在特定类别上的准确率。这一现象揭示了ViT中存在**类别有害权重（class-detrimental weights）**——这些权重在处理目标类别时产生负面贡献，移除它们反而能净化模型的知识表达。

遗憾的是，现有重要性度量指标（如权重大小、梯度范数、激活值等）完全无法捕获这一信号。Figure 4 表明，基于这些指标进行剪枝后，模型在特定类别上的准确率随剪枝率增大而单调下降，从未出现提升——这与随机剪枝的“意外之喜”形成鲜明对比。这说明，**传统重要性指标与类别特定性能之间不存在正相关关系**，亟需一种能主动识别并剔除类别有害权重的剪枝策略。

### 重训练：剪枝效率的真正瓶颈

现有训练相关（training-dependent）剪枝方法（如**X-Pruner**（Yu and Xiang, CVPR 2023）、**MDP**（Sun et al., CVPR 2025））虽然能获得较高的剪枝后精度，但Figure 3揭示了一个残酷的现实：在AWS EC2 g5.48xlarge实例上，为单个子任务（25类）从DeiT-Base派生一个剪枝模型，这些方法耗时长达数小时甚至数十小时，成本高达数十美元。当子任务数量扩展到50个、约束级别扩展到10个时，总成本将飙升至数千美元量级——这对于大规模边缘部署而言是完全不可接受的。

训练无关（training-free）方法（如**Wanda**（Sun et al., ICLR 2024））虽然速度快，但它们在类特定任务上的准确率远逊于训练相关方法，且同样无法移除类别有害权重。

### NuWa的核心动机

上述分析将问题收敛到一个清晰的瓶颈：**如何在无需重训练的前提下，为任意类别子集快速派生出高准确率的轻量级ViT？** 这要求同时解决两个技术挑战：

- **识别并剪除类别有害权重**，而非依赖盲目的全局重要性排序；
- **将剪枝形式化为可闭式求解的优化问题**，从而彻底绕过重训练的高昂开销。

NuWa正是沿着这一思路设计的：通过自我知识净化（SKP）学习二值化掩码自主发现有害权重，再将MHA和MLP模块的结构化剪枝分别转化为低秩逼近和最小二乘问题，利用SVD截断和伪逆闭式解直接获得剪枝后权重，实现“一次前向+一次矩阵分解”即可完成类定制模型的派生。



## 核心方法与创新机理

NuWa 的核心创新在于将类别特定的 ViT 剪枝从“重要性评分+重训练”范式转变为“有害权重净化+闭式优化”范式。这一转变由两个紧密协同的机制实现，分别对应剪枝策略与推导效率的根本性突破。

### 创新一：自我知识净化（SKP）——识别并剪除类别有害权重

现有剪枝方法基于权重幅度、梯度等类无关的重要性指标，对所有类别同等处理，无法针对特定类别优化模型。NuWa 首次提出**类别有害权重**（class-detrimental weights）的概念——即那些对目标类别预测产生负面影响的冗余参数。Figure 1 的动机实验直接揭示了这一现象：随机移除 DeiT-Base 的 MLP 神经元，竟能意外提高特定类别的准确率。Figure 4 进一步证实，基于现有重要性指标的剪枝无法系统性地提升类别特定准确率——这些指标根本不能区分“有害”与“有益”的冗余。

SKP 通过数据驱动的方式自动完成这一区分。其核心设计是：冻结基础 ViT（**DeiT-Base**, Touvron et al., ICML 2021），在 MLP 模块中嵌入可学习的连续掩码向量 $M^{(l)}$ 和控制因子 $\beta^{(l)}$，构造剪枝搜索空间。通过直通估计器（straight-through estimator）将连续掩码二值化为 $M_{\mathrm{bin.}}^{(l)}$（Eq. 3），并作用于 MLP 的前向传播（Eq. 4）：

$$M_{\mathrm{bin.}}^{(l)}[i] = \left\{ 1, \quad \mathrm{if } M^{(l)}[i] \geq \mathrm{Sel}_{\lfloor e_l \times \sigma(\beta^{(l)}) \rfloor}(M^{(l)}) \right.$$

$$\mathbf{MLP}^{(l)}(\mathbf{X}) = \sum_{i=1}^{e_l} \phi(\mathbf{X}W_1^{(l)}[i]) \otimes (M_{\mathrm{bin.}}^{(l)}[i] \cdot W_2^{(l)\top}[i])$$

仅使用目标类别的少量数据训练掩码，模型在保持对目标类别预测能力的同时，自动学会将有害神经元的掩码置零。训练完成后，根据二值掩码直接裁剪权重矩阵（Eq. 5），生成一个**剪枝率更高、类别特定准确率更强**的锚点模型 $\nu_A$。Figure 8 的可视化分析表明，SKP 后的特征分布（t-SNE）和预测概率分布均向目标类别显著集中，验证了有害知识被有效净化的因果机制。

消融实验（Table 4）给出决定性证据：移除 SKP 导致平均准确率下降 **18.75%**，证明自知识净化是整个方法的关键前提。超参数分析（Figure 10）进一步揭示，小批量（batch size = 1）使模型在剪枝空间中遍历更充分，锚点模型的剪枝率与性能均更优。

### 创新二：优化驱动的快速剪枝（OFP）——闭式解消除重训练

传统剪枝方法在移除权重后，必须通过昂贵的重训练来恢复精度（Figure 3 显示，以 AWS EC2 g5.48xlarge 定价，单模型剪枝+重训练成本高昂）。NuWa 的核心洞察是：将 MHA 和 MLP 模块的剪枝分别形式化为矩阵低秩逼近和最小二乘问题，利用闭式解直接获得剪枝后的最优权重，完全绕开重训练。

**MHA 剪枝**：将 QK 维度剪枝建模为最小化原始 QK 乘积与剪枝后乘积的 Frobenius 范数（Eq. 7）：

$$\operatorname* { m i n } _ { W _ { Q } ^ { ( l , h ) \prime } , W _ { K } ^ { ( l , h ) \prime } } \| W _ { Q } ^ { ( l , h ) \top } W _ { K } ^ { ( l , h ) } - W _ { Q } ^ { ( l , h ) \prime \top } W _ { K } ^ { ( l , h ) \prime } \| _ { F } ^ { 2 }$$

根据 Eckart-Young 定理，该问题等价于对 $W_Q^{\top}W_K$ 进行截断 SVD，闭式解由 Eq. (8) 给出。VO 维度剪枝同理。

**MLP 剪枝**：将中间维度剪枝建模为最小化激活重构误差。基于校准样本的隐藏层激活 $\mathcal{H}^{(l)}$，选择激活值最高的 $e_l'$ 个神经元索引集 $\mathcal{T}_r^{(l)}$，通过伪逆闭式解更新 $W_2^{(l)}$ 以补偿剪枝带来的输出偏差（Eq. 12）：

$$W _ { 2 } ^ { ( l ) \prime } = W _ { 2 } ^ { ( l ) } \mathcal { H } ^ { ( l ) \top } \mathcal { H } _ { r } ^ { ( l ) } ( \mathcal { H } _ { r } ^ { ( l ) \top } \mathcal { H } _ { r } ^ { ( l ) } ) ^ { \dagger }$$

消融实验（Table 4）验证了闭式解的决定性作用：跳过 MHA 剪枝降低准确率 15.39%，跳过 MLP 剪枝导致准确率骤降 **85.95%**；将 MLP 闭式解替换为直接移除低激活行，准确率下降 14.75%。Figure 12 显示 OFP 仅需 **128 个校准样本**即可获得稳定的闭式解，进一步降低了数据依赖。

### 创新三：可复用计算实现大规模定制

两个阶段的剪枝具有不同的计算复用特性。SKP 阶段（P1）的 SVD 分解仅依赖基础模型权重，与目标类别无关，因此**跨任务完全可复用**。OFP 阶段（P2）的校准特征提取虽需类别特定数据，但仅需极少样本。这一设计使得 NuWa 在大规模定制场景下（如 N=50 个子任务、M=10 个资源约束级别）展现出压倒性的效率优势：与最优训练相关方法 **X-Pruner**（Yu and Xiang, CVPR 2023）相比，总成本降低 **99.83%**，推导速度提升 **33.69 倍**，而平均准确率仅损失 0.61%（Table 2）。同时，NuWa 在类别特定准确率上超越训练无关方法（如 **Wanda**, Sun et al., ICLR 2024）高达 **29.00%**，且派生出的边缘 ViT 在 Jetson Orin NX 上实现 1.31× 至 2.07× 的推理加速（Table 3）。

**方法谱系定位**：NuWa 处于训练无关剪枝（追求效率但无法类别定制）与训练相关剪枝（可定制但成本极高）的交叉点。它通过 SKP 引入了轻量级的类别特定学习（仅训练掩码，冻结骨干），又通过 OFP 的闭式优化消除了重训练需求，实现了“定制能力”与“推导效率”的双重突破。



NuWa 的整体派生流程由两个串行且互补的核心模块构成：**自我知识净化（Self-Knowledge Purification, SKP）** 与 **优化驱动的快速剪枝（Optimization-based Fast Pruning, OFP）**，如图 Figure 5 所示。给定一个预训练的基础 ViT（如 **DeiT-Base** (Touvron et al., ICML 2021)）和一组目标类别数据，NuWa 首先通过 SKP 自动识别并剪除对特定类别有害的权重，生成一个更紧凑且在该类别上准确率更高的“锚点模型”；随后，OFP 将 MHA 与 MLP 模块的进一步结构化剪枝分别形式化为低秩矩阵逼近和最小二乘问题，利用闭式解直接获得剪枝后的权重，完全无需重训练。

![[assets/figures/papers/paper_list_l2108_https_openaccess_thecvf_com_content_CVPR2026_html_Wei_NuWa_Deriving_Ligh/figures/005_Figure_5.jpg]]
*Figure 5: Overview of NuWa. 1) Self-Knowledge Purification (SKP): learning binarized masks to identify and prune class-detrimental weights. 2) Optimization-based Fast Pruning (OFP): pruning MHA and MLP modules through closed-form optimization*

### 模块关系与数据流

1. **输入**：基础 ViT 模型 `γ_B` 与目标类别子集 `S` 对应的少量样本。
2. **阶段一：SKP**  
   - 冻结 `γ_B` 的全部参数，仅在其 MLP 模块中嵌入可学习的连续掩码向量 `M^{(l)}` 与控制因子 `β^{(l)}`，构建剪枝搜索空间。  
   - 通过目标类别数据驱动优化，将连续掩码二值化为 `M_bin^{(l)}`（Eq. 3），直接移除被判定为类别有害的神经元（Eq. 5），输出锚点模型 `ν_A`。  
   - 该阶段的核心因果机制在于：掩码学习过程本质上是在搜索“保留哪些权重能最大化目标类别准确率”，从而将传统剪枝从“重要性保留”转变为“有害性剔除”。
3. **阶段二：OFP**  
   - 以锚点模型 `ν_A` 为基础，分别对 MHA 和 MLP 模块实施闭式剪枝：  
     - **MHA 剪枝**：将 QK 权重乘积矩阵的低秩逼近问题通过截断 SVD 求解（Eq. 7–8），同时压缩 `Q`、`K` 维度和 `V`、`O` 维度。  
     - **MLP 剪枝**：基于少量校准样本提取中间层激活，通过伪逆最小化输出重构误差（Eq. 11–12），直接更新 `W_2` 权重，实现中间维度的均衡削减（Eq. 10）。  
   - 两个子模块共享校准样本的前向传播结果，计算高度复用。
4. **输出**：满足目标资源约束（由总体剪枝率 `α` 控制）的类定制轻量级边缘 ViT `γ_E`。

### 设计瓶颈与因果链路

现有类无关剪枝方法的根本瓶颈在于：它们对所有类别一视同仁，既无法移除对特定类别有害的冗余权重，又依赖昂贵的重训练来恢复精度。NuWa 通过以下因果链路打破这一瓶颈：

- **SKP → 消除类别有害权重**：Figure 1 揭示的“随机移除 MLP 神经元可意外提升特定类别准确率”这一现象，是 SKP 设计的直接动因。SKP 将这一随机发现转化为可学习的自动化过程，使锚点模型在剪枝的同时获得比基础 ViT 更高的类别特定准确率（Figure 6）。消融实验（Table 4）证实，移除 SKP 会导致平均准确率下降 18.75%，验证了其关键地位。
- **OFP → 闭式优化替代重训练**：传统剪枝方法（如 **X-Pruner** (Yu and Xiang, CVPR 2023)、**MDP** (Sun et al., CVPR 2025)）每次剪枝后必须进行完整重训练，这在面对大量类别-资源约束组合时成本不可接受（Figure 3）。OFP 将剪枝转化为有闭式解的优化问题，使单模型推导速度达到 X-Pruner 的 33.69 倍，在大规模场景（50 个子任务 × 10 个约束级别）下总成本降低高达 99.83%（Table 2），而平均精度损失仅为 0.61%。
- **两阶段协同**：SKP 提供的锚点模型已剔除类别有害权重，为 OFP 提供了更“干净”的起点；OFP 则在此基础上通过数学上最优的低秩/最小二乘逼近进一步压缩，两者共同实现了“无需重训练、类别定制、高效大规模派生”的目标。

### 关键操作锚点

| 模块 | 核心操作 | 公式锚点 | 输入 | 输出 |
|------|----------|----------|------|------|
| SKP | 掩码学习与二值化剪枝 | Eq. 3–5 | 基础 ViT + 目标类别数据 | 锚点模型 `ν_A` |
| OFP-MHA | 截断 SVD 低秩逼近 | Eq. 7–8 | `ν_A` 的 QK 权重乘积 | 压缩后的 Q/K/V/O 权重 |
| OFP-MLP | 激活选择 + 伪逆重构 | Eq. 10–12 | 校准样本激活 | 压缩后的 MLP 权重 |

> **注意**：上述模块关系与数据流基于论文 Section 3 的描述和 Figure 5 的框架图综合得出。消融实验中 MLP 剪枝跳过导致准确率骤降 85.95%（Table 4），表明 MLP 闭式解在整个 OFP 流程中起决定性作用，而 SKP 的小批量设置（batch size=1）被证实能使剪枝空间探索更充分（Figure 10）。



NuWa 的整体框架由两大核心模块构成：**自我知识净化（Self-Knowledge Purification, SKP）** 与 **基于优化的快速剪枝（Optimization-based Fast Pruning, OFP）**，如 Figure 5 所示。SKP 负责自动识别并剪除对目标类别有害的权重，生成一个更紧凑且类别特定准确率更高的锚点模型；OFP 则在此基础上，将多注意力头（MHA）与多层感知器（MLP）模块的进一步剪枝形式化为闭式优化问题，完全无需重训练即可高效推导出边缘 ViT。

### ViT 基础计算形式

在阐述核心模块之前，先回顾 ViT 中 MHA 与 MLP 的前向计算。第 $l$ 层第 $h$ 个注意力头的计算为：

$$
\mathcal{A}^{(l,h)} = \mathrm{Softmax}\Big(\frac{QK^{\top}}{\sqrt{q_l}}\Big)VW_O^{(l,h)\top}
\tag{1}
$$

其中 $q_l$ 为每个头的维度，$Q, K, V$ 分别为查询、键和值矩阵，$W_O^{(l,h)}$ 为输出投影权重。

MLP 层的前向计算可表示为神经元输出的加权和：

$$
\mathbf{MLP}^{(l)}(\mathbf{X}) = \sum_{i=1}^{e_l} \phi(\mathbf{X}W_1^{(l)}[i]) \otimes W_2^{(l)\top}[i]
\tag{2}
$$

其中 $e_l$ 为第 $l$ 层 MLP 的中间神经元个数，$\phi$ 为激活函数，$W_1^{(l)}[i]$ 表示第一层权重矩阵的第 $i$ 列，$W_2^{(l)\top}[i]$ 表示第二层权重矩阵的第 $i$ 行。

### 自我知识净化（SKP）

SKP 的核心机制是在冻结基础 ViT $\gamma_B$ 的前提下，向其 MLP 模块中嵌入可学习的连续掩码向量 $M^{(l)}$ 与控制因子 $\beta^{(l)}$，构建一个剪枝空间。通过在该空间中以目标类别数据驱动的方式进行优化，模型自动学习哪些神经元对目标类别有害。

掩码的二值化过程由控制因子 $\beta^{(l)}$ 动态决定 Top-k 选择阈值：

$$
M_{\mathrm{bin.}}^{(l)}[i] = \begin{cases} 1, & \text{if } M^{(l)}[i] \geq \mathrm{Sel}_{\lfloor e_l \times \sigma(\beta^{(l)}) \rfloor}(M^{(l)}) \end{cases}
\tag{3}
$$

其中 $\sigma(\cdot)$ 为 Sigmoid 函数，$\mathrm{Sel}_k(\cdot)$ 表示选取第 $k$ 大的元素值。二值掩码被应用于 MLP 的前向传播中，实现对特定神经元的屏蔽：

$$
\mathbf{MLP}^{(l)}(\mathbf{X}) = \sum_{i=1}^{e_l} \phi(\mathbf{X}W_1^{(l)}[i]) \otimes (M_{\mathrm{bin.}}^{(l)}[i] \cdot W_2^{(l)\top}[i])
\tag{4}
$$

SKP 收敛后，根据二值掩码中为 0 的位置 $\mathbb{Z}(\mathcal{M}_{\mathrm{bin.}}^{(l)})$ 物理移除对应的权重行或列，得到锚点模型 $\nu_A$：

$$
W_1^{(l)} = W_1^{(l)}[\mathbb{Z}(\mathcal{M}_{\mathrm{bin.}}^{(l)})], \quad W_2^{(l)} = W_2^{(l)}[:,\mathbb{Z}(\mathcal{M}_{\mathrm{bin.}}^{(l)})]
\tag{5}
$$

### 基于优化的快速剪枝（OFP）

OFP 将 MHA 和 MLP 模块的进一步结构化剪枝分别形式化为矩阵低秩逼近和最小二乘问题，利用闭式解避免重训练。

**MHA 剪枝。** 为减少注意力头的维度 $q_l$，OFP 将剪枝后的 QK 权重乘积逼近原始乘积，目标函数为：

$$
\min_{W_Q^{(l,h)\prime}, W_K^{(l,h)\prime}} \| W_Q^{(l,h)\top} W_K^{(l,h)} - W_Q^{(l,h)\prime\top} W_K^{(l,h)\prime} \|_F^2
\tag{7}
$$

该问题本质上是低秩矩阵逼近。根据 Eckart-Young 定理，对 $W_Q^{(l,h)\top} W_K^{(l,h)}$ 进行截断 SVD 即可获得最优解。剪枝后的 Q 权重闭式解为：

$$
W_Q^{(l,h)\prime} = (U_{QK}^{(l,h)}[:, :q_l^{\prime}] \Sigma_{QK}^{(l,h)}[:q_l^{\prime}, :q_l^{\prime}])^{\top} \times \sqrt{q_l^{\prime} / q_l}
\tag{8}
$$

其中 $U_{QK}$ 和 $\Sigma_{QK}$ 来自 SVD 分解，$q_l^{\prime}$ 为剪枝后的头维度。V 和 O 权重的剪枝采用类似策略。

**MLP 剪枝。** 在 SKP 得到的锚点模型基础上，OFP 进一步减少每层 MLP 的中间维度。首先根据总剪枝量均衡分配各层保留的神经元数：

$$
e_l^{\prime} = \min(e_l, \lfloor (\sum_{i=1}^{L} e_i - e_{\mathrm{prune}}) / L \rfloor)
\tag{10}
$$

然后，基于校准样本的激活值选择最重要的神经元索引集 $\mathcal{T}_r^{(l)}$，并通过最小化输出重构误差的伪逆解更新 $W_2$ 权重：

$$
W_2^{(l)\prime} = W_2^{(l)} \mathcal{H}^{(l)\top} \mathcal{H}_r^{(l)} (\mathcal{H}_r^{(l)\top} \mathcal{H}_r^{(l)})^{\dagger}
\tag{12}
$$

其中 $\mathcal{H}^{(l)}$ 为原始模型的隐藏层激活矩阵，$\mathcal{H}_r^{(l)}$ 为按 $\mathcal{T}_r^{(l)}$ 索引选出的激活子矩阵，$(\cdot)^{\dagger}$ 表示 Moore-Penrose 伪逆。该闭式解直接给出了剪枝后 $W_2$ 的最优权重，无需任何迭代训练。

### 补充图表

![[assets/figures/papers/paper_list_l2108_https_openaccess_thecvf_com_content_CVPR2026_html_Wei_NuWa_Deriving_Ligh/figures/001_Figure_1.jpg]]
*Figure 1: Pruning can sometimes improve class-specific performance. Randomly removing certain neurons from the MLP modules of DeiT-Base unexpectedly increases model accuracy on specific classes, revealing the existence of class-detrimental weights*

![[assets/figures/papers/paper_list_l2108_https_openaccess_thecvf_com_content_CVPR2026_html_Wei_NuWa_Deriving_Ligh/figures/002_Figure_2.jpg]]
*Figure 2: Comparison of model derivation settings for ViTs. (a) Class-agnostic derivation compresses the base ViT without considering class differences, lacking customization for diverse scenarios. (b) Class-specific derivation uses class-specific data for pruning and retraining but fails to remove class-detrimental knowledge and is time-consuming, limiting scalability. (c) NuWa removes class-detrimental weights and formulates pruning as closed-form optimization problems, enabling fast derivation of lightweight and customized edge ViTs*

![[assets/figures/papers/paper_list_l2108_https_openaccess_thecvf_com_content_CVPR2026_html_Wei_NuWa_Deriving_Ligh/figures/010_Figure_8.jpg]]
*Figure 8: Comparison in feature and probability distributions before and after SKP. The feature distributions are visualized by applying t-SNE to the CLS tokens from the last block, while the bar charts show the average output probability over*



## 实验与关键发现

### 核心发现：类别特定准确率与推导效率的双重突破

NuWa 在类别特定任务上实现了“性能反超”与“推导极速”的统一，这是现有方法无法同时达成的。在 ImageNet-1K 子任务上（以 DeiT-Base 为基础模型，|S|=25），NuWa 相比最优训练无关剪枝方法的类别特定准确率提升最高可达 **29.00%**。在剪枝率 0.40 和 0.60 的设置下，NuWa 相较训练无关方法的平均准确率提升分别为 **15.37%** 和 **10.04%**。更关键的是，NuWa 完全无需重训练——其推导出的轻量级边缘 ViT 甚至能在目标类别上**超越原始未剪枝的 DeiT-Base**，而现有训练无关方法均无法做到这一点（Figure 6）。

在推导效率上，NuWa 展现出数量级优势。与最优训练相关方法 X-Pruner（Yu and Xiang, CVPR 2023）相比，NuWa 在单个模型的剪枝速度上达到 **33.69 倍**加速。当面向大规模定制场景（N=50 个子任务，M=10 个资源约束层级，共需派生 500 个模型）时，NuWa 的总成本可降低高达 **99.83%**，而平均准确率仅损失 **0.61%**（Table 2）。这一效率优势源于 NuWa 的两阶段设计：P1 阶段的 SVD 分解可跨任务复用，P2 阶段的闭式伪逆解仅需 128 个校准样本即可稳定收敛（Figure 12）。

![[assets/figures/papers/paper_list_l2108_https_openaccess_thecvf_com_content_CVPR2026_html_Wei_NuWa_Deriving_Ligh/figures/008_Table_2.jpg]]
*Table 2: Comparison in derivation efficiency between NuWa and training-dependent baselines across different sub-tasks scales. P and T denote pruning and retraining costs. Accuracy is averaged over*

### 与训练相关方法的全面对比

Table 1 系统对比了 NuWa 与三类训练相关剪枝基线（MDP、X-Pruner、Wanda）在 9 个不同规模子任务上的表现。NuWa 在多数设置下取得最优或次优准确率，且下标标注显示其推导模型在目标类别上持续优于原始 DeiT-Base。值得注意的是，NuWa 取得这一结果**完全无需重训练**，而所有训练相关基线均依赖昂贵的剪枝后重训练步骤。

![[assets/figures/papers/paper_list_l2108_https_openaccess_thecvf_com_content_CVPR2026_html_Wei_NuWa_Deriving_Ligh/figures/006_Table_1.jpg]]
*Table 1: Comparison between NuWa and training-dependent pruning baselines, with the best and second-best accuracies highlighted in bold and underlined, respectively. Subscripts indicate improvements over DeiT-Base*

Table 2 进一步揭示了效率差异的结构性原因。以 X-Pruner 为例，其总成本由剪枝成本 P 和重训练成本 T 构成，且重训练占据主导。NuWa 通过闭式优化消除了 T，并将 P 压缩至极低水平。在大规模场景下，NuWa 的 P1 阶段 SVD 计算可跨子任务共享，仅 P2 阶段需要针对每个子任务执行轻量的校准与伪逆计算，从而实现了近乎恒定的边际推导成本。

### 实际推理加速验证

Table 3 报告了 NuWa 派生模型在 GPU（RTX 4090）和边缘设备（Jetson Orin NX）上的实测推理加速。在不同总体剪枝率 α 下，边缘 ViT 相较原始 DeiT-Base 在 RTX 4090 上实现 **1.30× 至 1.92×** 加速，在 Jetson Orin NX 上实现 **1.31× 至 2.07×** 加速。这验证了 NuWa 的剪枝策略不仅能提升类别特定准确率，还能切实转化为边缘设备上的推理效率增益。

![[assets/figures/papers/paper_list_l2108_https_openaccess_thecvf_com_content_CVPR2026_html_Wei_NuWa_Deriving_Ligh/figures/012_Table_3.jpg]]
*Table 3: Comparison in computational efficiency between DeiT-Base and edge ViTs derived by NuWa under different*

### 泛化性验证

NuWa 的适用性不限于特定基础模型或数据集。Figure 7 展示了在多种基础 ViT（DeiT-Base、DeiT-Small、DeiT-Tiny）和多个数据集（ImageNet-1K、CIFAR-100、Tiny-ImageNet）上的表现，NuWa 派生的边缘 ViT 在随机选择的类别子集上均能保持甚至超越基础模型的类别特定准确率。这表明 SKP 识别类别有害权重的机制具有跨架构和跨数据分布的泛化能力。

![[assets/figures/papers/paper_list_l2108_https_openaccess_thecvf_com_content_CVPR2026_html_Wei_NuWa_Deriving_Ligh/figures/009_Figure_7.jpg]]
*Figure 7: Performance of NuWa-derived edge ViTs across different base ViTs and datasets, with randomly selected classes in*

### 消融实验：各组件的因果贡献

Table 4 的消融实验严格量化了 NuWa 各组件的必要性（α=0.6，DeiT-Base）：

![[assets/figures/papers/paper_list_l2108_https_openaccess_thecvf_com_content_CVPR2026_html_Wei_NuWa_Deriving_Ligh/figures/015_Table_4.jpg]]
*Table 4: Ablation study of pruning techniques and settings used by NuWa on DeiT-Base with*

- **移除 SKP**：平均准确率下降 **18.75%**，直接验证了自我知识净化在识别和剪除类别有害权重中的核心作用。
- **跳过 MHA 剪枝**：准确率降低 **15.39%**，说明注意力头的低秩剪枝对保持模型表达能力至关重要。
- **跳过 MLP 剪枝**：准确率骤降 **85.95%**，这是最剧烈的退化，表明 MLP 中间维度的剪枝在 NuWa 框架中起决定性作用。这一结果与 Figure 1 的动机观察一致——类别有害权重主要存在于 MLP 模块中，因此 MLP 剪枝是性能提升的关键杠杆。
- **将 MLP 闭式解替换为直接移除低激活行**：准确率下降 **14.75%**，证明了基于伪逆的最小二乘闭式解在保持输出重构精度上显著优于简单的启发式选择。

### 超参数敏感性分析

三个关键超参数的实验揭示了 NuWa 的设计合理性：

- **SKP 批量大小**（Figure 10）：小批量（batch size=1）使基础模型在剪枝空间中遍历更充分，产生的锚点模型同时具有更高的剪枝率和更优的类别特定性能。这符合直觉——小批量引入的梯度噪声有助于逃离局部最优掩码配置。
- **保留能量比 ρ**（Figure 11）：随着总体剪枝率 α 增大，最优 ρ 逐渐减小。这表明在更激进的剪枝目标下，MHA 模块需要保留的奇异值能量占比可以相应降低，为自适应确定 ρ 提供了经验依据。
- **校准样本数量 K**（Figure 12）：OFP 仅需 128 个校准样本即可获得稳定的闭式剪枝解，继续增加 K 带来的边际收益极小。这一低样本需求是 NuWa 实现极速推导的关键因素之一。

![[assets/figures/papers/paper_list_l2108_https_openaccess_thecvf_com_content_CVPR2026_html_Wei_NuWa_Deriving_Ligh/figures/013_Figure_11.jpg]]
*Figure 11: Effect of the retained energy ratio*

### 失败模式与局限

当前分析中未发现论文明确报告的失败案例。但需注意：NuWa 的 SKP 阶段依赖于目标类别的少量数据来学习掩码，当目标类别数据极度稀缺（如仅有个位数样本）时，SKP 能否有效识别类别有害权重需要手动验证。此外，OFP 的闭式解基于线性最小二乘假设，对于非线性激活主导的层间交互误差传播，其理论最优性保证尚不明确。

### 补充图表

![[assets/figures/papers/paper_list_l2108_https_openaccess_thecvf_com_content_CVPR2026_html_Wei_NuWa_Deriving_Ligh/figures/003_Figure_3.jpg]]
*Figure 3: Existing pruning methods are time-consuming and costly. Experiments are conducted at a pruning rate of 0.50 using randomly selected 25 ImageNet classes to derive one model from DeiT-Base. Cost is based on AWS EC2 g5.48xlarge pricing*

![[assets/figures/papers/paper_list_l2108_https_openaccess_thecvf_com_content_CVPR2026_html_Wei_NuWa_Deriving_Ligh/figures/004_Figure_4.jpg]]
*Figure 4: Existing importance metrics fail to improve classspecific accuracy through pruning. The solid lines with standard deviation bands represent the mean accuracy of pruned DeiT-Base on three random sub-tasks (|S|=25) across different pruning rates*



## 定位与知识库关联

### 问题定位与现有范式

边缘设备上部署视觉Transformer（ViT）面临的核心矛盾在于：单一通用模型难以满足多样化场景下差异巨大的资源约束与类别定制需求。现有模型派生方法可归为三类范式（Figure 2）：

**（a）类无关派生（Class-agnostic derivation）**。以**Wanda**（Sun et al., ICLR 2024）为代表的训练无关剪枝方法，以及**X-Pruner**（Yu and Xiang, CVPR 2023）、**MDP**（Sun et al., CVPR 2025）等训练相关剪枝方法，均基于权重幅度、梯度或激活值等通用重要性指标对所有类别同等处理。这类方法忽视了一个关键现象：某些权重对特定类别不仅冗余，而且**有害**——随机移除MLP神经元可意外提高特定类别准确率（Figure 1）。类无关方法无法识别并利用这一特性，导致剪枝后模型在目标类别上难以超越原始基础ViT。

**（b）类特定派生（Class-specific derivation）**。现有方法可在剪枝后使用目标类别数据进行重训练以恢复性能，但存在三重瓶颈：其一，重训练成本高昂（Figure 3显示单模型剪枝+重训练耗时以小时计）；其二，无法主动识别并移除类别有害知识，仅能被动恢复剪枝损失；其三，当面临N个子任务×M个资源约束级别的大规模定制需求时，需从头执行N×M次剪枝与重训练，成本线性膨胀至不可接受。

NuWa的定位是**类特定、无需重训练的快速结构化剪枝框架**，填补了上述两类范式之间的空白：既具备类特定派生的定制能力，又拥有训练无关方法的推导效率。

### 核心技术路线与差异化

NuWa的方法论创新体现在两个耦合模块：

**（1）自我知识净化（Self-Knowledge Purification, SKP）**。与依赖预设重要性指标的现有剪枝方法不同，SKP冻结基础ViT权重，在MLP模块中嵌入可学习的连续掩码向量$M^{(l)}$与控制因子$\beta^{(l)}$，通过目标类别数据驱动优化，自动学习二值化掩码$M_{\mathrm{bin.}}^{(l)}$以识别并剪除类别有害权重。这一过程将剪枝从“被动评估重要性”转变为“主动净化知识”，生成的锚点模型$\nu_A$在更高剪枝率下仍能超越基础ViT的目标类别准确率。消融实验表明，移除SKP导致平均准确率下降18.75%（Table 4），证实其不可替代性。

**（2）优化驱动的快速剪枝（Optimization-based Fast Pruning, OFP）**。现有方法剪枝后必须重训练的根本原因在于：直接移除权重会引入难以补偿的误差。OFP将剪枝重新形式化为有闭式解的优化问题，从根本上规避重训练。具体而言：
- **MHA剪枝**：将QK维度缩减建模为低秩矩阵逼近问题$\min \|W_Q^\top W_K - W_Q^{\prime\top} W_K^{\prime}\|_F^2$，通过截断SVD获得闭式解（Eq. 7-8），由Eckart-Young定理保证最优性。
- **MLP剪枝**：基于校准样本的激活值选择保留神经元索引，通过伪逆解$\mathcal{H}_r(\mathcal{H}_r^\top\mathcal{H}_r)^\dagger$最小化输出重构误差（Eq. 12），将剪枝转化为最小二乘问题。

这种“闭式优化替代重训练”的策略使NuWa在推导效率上产生质变：单模型剪枝速度相比最佳训练相关方法**X-Pruner**提升**33.69倍**，在大规模场景（N=50子任务，M=10约束级别）下总成本降低**99.83%**，而平均准确率仅损失**0.61%**（Table 2）。值得注意的是，OFP的第一阶段（MHA剪枝的SVD计算）可跨任务复用，进一步摊薄大规模定制的边际成本。

### 适用边界与局限

**适用边界**：
- **基础架构**：论文在DeiT-Base（Touvron et al., ICML 2021）上进行了主要验证，并在其他ViT变体及数据集上展示了泛化性（Figure 7），但对非Transformer架构（如CNN、Mamba）的适用性未经验证。
- **任务类型**：面向图像分类的类别特定剪枝，核心假设是“存在类别有害权重”这一现象具有普遍性。该假设在ImageNet-1K子任务上得到验证，但在细粒度分类、少样本类别或目标检测等任务上的迁移性需进一步检验。
- **剪枝粒度**：当前实现聚焦于MHA的QK/VO维度与MLP中间维度的结构化剪枝，未涉及注意力头数、层数等更粗粒度的结构搜索。
- **校准数据依赖**：OFP的MLP剪枝依赖少量校准样本（默认K=128）计算激活值，实验表明K≥128时解已稳定（Figure 12），但极端数据稀缺场景（如每个目标类别仅有个位数样本）下的表现尚不明确。

**局限与待验证问题**：
- 论文未报告SKP阶段本身的收敛稳定性对超参数（学习率、训练步数）的敏感性边界。虽然Figure 10显示小批量（batch size=1）有利于充分探索剪枝空间，但不同基础模型规模下的最优设置可能需要重新调参。
- 类别有害权重的理论成因未得到深入解释——论文通过现象（Figure 1）和净化效果（Figure 8的t-SNE可视化）展示了其存在与影响，但未从表示学习或优化动力学角度给出机理性分析。
- 在极端剪枝率（如α>0.7）下，闭式解的近似误差可能累积，当前论文主要报告α∈{0.40, 0.60}的结果。Figure 11显示保留能量比ρ需随α增大而减小，暗示存在精度-效率的折衷边界，但该边界的系统性刻画尚不完整。

### 知识库定位

NuWa处于**模型压缩**、**边缘智能**与**类别定制化部署**的交叉点。其核心贡献——将剪枝重构为无需重训练的闭式优化问题——为“大规模定制化模型派生”建立了新的效率基准。与现有工作的关系可概括为：
- **超越训练无关方法**：在类特定准确率上提升高达29.00%，且是唯一能使剪枝后模型超越基础ViT的框架（Figure 6）。
- **替代训练相关方法**：在保持可比准确率（-0.61%）的前提下，将推导成本降低两个数量级以上，使大规模边缘部署从经济不可行变为可行。
- **开启新方向**：SKP揭示的“类别有害权重”概念可能启发新的剪枝准则设计，而OFP的闭式优化范式可推广至其他模块（如LayerNorm、位置编码）的压缩。



## 原文 PDF

![[paperPDFs/CVPR_2026/NuWa_Deriving_Lightweight_Class_Specific_Vision_Transformers_for_Edge_Devices.pdf]]
