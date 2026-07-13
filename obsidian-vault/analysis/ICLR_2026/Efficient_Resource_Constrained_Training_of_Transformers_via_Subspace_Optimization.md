---
title: "Efficient Resource-Constrained Training of Transformers via Subspace Optimization"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Efficient_Resource_Constrained_Training_of_Transformers_via_Subspace_Optimization.pdf
project_link: null
code_link: https://github.com/Le-TrungNguyen/ICLR2026-WASI.git
openreview_forum_id: 0nvQ5kHXf4
aliases:
- WWASI
- ERCTTSO
tags:
- ICLR_2026
- topic/optimization_theory_probabilistic
- topic/optimization_theory_probabilistic/optimization_methods
core_operator: "通过控制解释方差阈值ε，在稳定低秩子空间内同时压缩模型权重和激活，从而调节资源消耗与信息损失的权衡。"
primary_logic: "模型参数在微调过程中驻留在一个稳定的低秩子空间内，激活图的能量也集中在少数主成分上，因此可以在此子空间内进行训练和推理，大幅降低内存和计算开销，同时保持模型性能。"
claims:
- "Layer ranks remain remarkably stable across fine-tuning epochs."
- "WASI matches vanilla accuracy while cutting memory by up to 62× and FLOPs by 1.5× at ε=0.9 on SwinT."
- "WASI achieves up to 100× higher memory efficiency than SVD-LLM at similar accuracy."
- "On TinyLlama, WASI reduces activation memory by up to 953.86× and weight memory by 30.12× without accuracy loss."
---

# Efficient Resource-Constrained Training of Transformers via Subspace Optimization

> [!tip] 核心洞察
> 模型参数在微调过程中驻留在一个稳定的低秩子空间内，激活图的能量也集中在少数主成分上，因此可以在此子空间内进行训练和推理，大幅降低内存和计算开销，同时保持模型性能。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 基于子空间优化的Transformer高效资源受限训练 |
| 英文题名 | Efficient Resource-Constrained Training of Transformers via Subspace Optimization |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=0nvQ5kHXf4) · [GitHub](https://github.com/Le-TrungNguyen/ICLR2026-WASI.git) |
| Topic | #topic/optimization_theory_probabilistic #topic/optimization_theory_probabilistic/optimization_methods |
| Method | WASI (Weight-Activation Subspace Iteration) |
| Dataset | ViT on CIFAR-10 (all linear layers), SwinT on multiple datasets, TinyLlama on BoolQ |

> [!tip] 效果简介
> - ViT on CIFAR-10 (all linear layers) 上，Training Memory (MB) 为 179.61 (ε=0.9)，对比 2349.00 (vanilla, ε=1.0)，变化 13.1× reduction。
> - ViT on CIFAR-10 (all linear layers) 上，Accuracy (%) 为 96.24 (ε=0.9)，对比 97.32 (vanilla)，变化 -1.08。
> - SwinT on multiple datasets 上，Training Memory 为 WASI (ε=0.9)，对比 Vanilla，变化 up to 62× reduction。

## 概要

在边缘设备上微调大型Transformer模型面临严峻的资源瓶颈：反向传播需要存储完整的权重矩阵和激活图，导致内存需求过高；同时，大型矩阵乘法在推理阶段也消耗大量计算资源。现有的压缩方法通常仅针对权重或激活的单一维度，难以在保持模型性能的同时实现训练与推理的全链路资源削减。

**WASI（Weight-Activation Subspace Iteration）** 提出了一种统一的低秩训练框架，其核心洞察在于：模型参数在微调过程中驻留于一个稳定的低秩子空间内，激活图的能量也集中在少数主成分上。基于这一发现，WASI通过引入**解释方差阈值ε**作为可控信息损失旋钮，同时对权重矩阵（经由截断SVD分解为低秩因子$L_i, R_i$）和激活张量（经Tucker分解压缩为核心张量与因子矩阵）进行子空间压缩，并在该低秩表示内完成前向与反向传播。

**方法定位**：WASI区别于仅压缩激活的**ASI**（Nguyen et al., 2025）和仅对权重做低秩分解的**SVD-LLM**（Wang et al., 2024），首次在统一框架下联合压缩权重与激活，并通过子空间迭代（而非每步完整SVD/HOSVD）大幅降低分解本身的计算开销。

**核心实验结果**：
- 在ViT/CIFAR-10上，WASI（ε=0.9）将训练内存从2349 MB降至179.61 MB（**13.1×降低**），精度仅损失1.08%（96.24% vs. 97.32%）。
- 在SwinT上，WASI实现**最高62×的内存削减**和1.5×的FLOPs降低。
- 相较于SVD-LLM，WASI在同等精度下内存效率**最高提升100×**。
- 在TinyLlama/BoolQ上，激活内存最高降低**953.86×**，权重内存降低**30.12×**，且无精度损失。
- 在Raspberry Pi 5端侧设备上，WASI实现约**1.4×的训练与推理加速**。

**局限性**：当前验证主要集中在视觉Transformer（ViT、SwinT），尚未在数十亿参数的大语言模型及更广泛的NLP下游任务上充分评估；低ε值下精度损失仍然存在；方法在持续学习等场景中的子空间稳定性有待验证。



### 资源受限场景下的Transformer训练瓶颈

Transformer架构在视觉和语言任务中取得了显著成功，但其训练和推理过程对计算资源的需求极高。核心瓶颈集中在两个方面：**反向传播时的内存开销**和**推理时的计算开销**。

在标准训练流程中，每个线性层的前向传播计算为 $\mathcal{A}_{i+1} = \mathcal{A}_i \mathcal{W}_i^{\top}$，反向传播则需要同时存储完整的权重矩阵 $\mathcal{W}_i$ 和激活图 $\mathcal{A}_i$ 以计算梯度。对于大规模模型，这些张量的内存占用往往超出边缘设备（如Raspberry Pi、Jetson Orin）的可用容量，使得在资源受限场景下进行模型微调变得极为困难。

与此同时，即使仅进行推理，大型Transformer中的矩阵乘法操作也消耗大量计算资源，限制了模型在移动端和IoT设备上的部署可行性。

### 现有方法的缺口

当前针对Transformer高效训练和推理的方法主要分为两类，但均存在明显局限：

- **仅压缩激活的方法**：如**ASI**（Nguyen et al., 2025）仅对激活图进行低秩近似，在训练过程中仍需维护完整的权重矩阵，内存节省有限。
- **仅压缩权重的方法**：如**SVD-LLM**（Wang et al., 2024）通过对权重矩阵进行低秩分解来减少推理内存，但其设计面向LLM推理场景，未考虑训练过程中的激活存储问题，且缺乏对信息损失的精细控制机制。

更重要的是，现有方法普遍**缺乏一个统一的框架来同时压缩权重和激活**，导致在训练场景下无法最大化资源节省。此外，大多数方法的压缩率选择依赖人工设定（如固定秩或内存预算），缺少以信息保留为导向的自适应机制。

### 本文动机与核心观察

本文的核心动机源于一个关键观察：**模型参数在微调过程中驻留在一个稳定的低秩子空间内**。如Figure 3a所示（Sec. 4.2），在ViT微调过程中，权重矩阵 $\mathcal{W}_6$ 的奇异值分布在不同epoch间保持显著稳定，表明参数的核心信息集中在少数主成分上。同时，Figure 4显示激活图的能量也高度集中于前几个奇异值，验证了激活空间的低秩特性。

基于这一观察，本文提出**WASI（Weight-Activation Subspace Iteration）**方法，通过统一的子空间优化框架，在训练和推理过程中同时压缩权重和激活，并通过**解释方差阈值 $\varepsilon$** 作为单一控制旋钮来调节信息保留与资源消耗之间的权衡。该方法的目标是在保持模型性能的前提下，最大化内存和计算效率，使Transformer能够在资源严重受限的边缘设备上完成微调和部署。



## 核心方法与创新机理

### 核心瓶颈与调控旋钮

大型Transformer在资源受限设备上训练面临双重瓶颈：反向传播需存储完整的权重矩阵和激活图，导致内存需求极高；推理阶段的矩阵乘法同样消耗大量计算资源。WASI的核心调控旋钮是**解释方差阈值 $\varepsilon$**——通过控制$\varepsilon$，在稳定的低秩子空间内同时压缩模型权重和激活，从而调节资源消耗与信息损失的权衡。

这一设计的理论前提经实验验证：权重矩阵的奇异值谱在微调过程中保持显著稳定（Fig. 3a, Sec. 4.2），激活图的能量也集中在少数主成分上（Fig. 4），使得在低秩子空间内进行训练和推理成为可能。

### 相对于Baseline的关键Changed Slots

WASI相对于现有方法的核心创新体现在五个关键维度的系统性改动：

| 维度 | Baseline | WASI | 证据锚点 |
|------|----------|------|----------|
| **权重表示** | 完整矩阵 $\mathcal{W}_i$ | 截断SVD低秩因子 $L_i, R_i$，由 $\varepsilon$ 控制秩 $K_i$ | Sec. 3.3, Eq. 6-7 |
| **激活存储** | 完整张量 $\mathcal{A}_i$ | Tucker分解压缩：核心张量 $\tilde{\mathcal{S}}_i$ 与因子矩阵 | Sec. 3.2, Eq. 4 |
| **反向传播计算** | 标准链式法则，完整张量 | 低秩反向传播，使用ASI近似激活和权重因子 | Sec. 3.3, Eq. 9-10 |
| **秩选择策略** | 手动预算 $B$ 或暴力搜索（ASI） | 动态规划最小化总激活内存，受预调困惑度约束 | Appendix A.2, Eq. 29-32 |
| **训练算法** | 全参数微调 | 仅微调低秩因子，周期性子空间迭代（WSI+ASI） | Algorithm 1, Sec. 3.3 |

### 方法流水线模块

WASI由四个协同模块构成统一框架：

1. **Weight Subspace Iteration (WSI)**：在 $t=0$ 时执行一次完整SVD确定本质子空间，后续迭代复用前一步的正交基进行子空间迭代，避免每次迭代的高昂SVD开销（Sec. 3.3, Algorithm 1）。消融实验表明，WSI在达到相同精度时比完整SVD减少1.36× FLOPs，在等FLOPs条件下精度高出约35%（Fig. 3b）。

2. **Activation Subspace Iteration (ASI)**：对激活图应用Tucker低秩分解，使用热启动的子空间迭代替代昂贵的HOSVD计算（Sec. 3.2, Appendix A.2）。

3. **解释方差驱动的秩选择**：权重层通过强制执行目标解释方差阈值 $\varepsilon$ 确定最优秩 $K_i$；激活层采用动态规划在预调困惑度约束下最小化总激活内存（Sec. 3.3, Appendix A.2）。

4. **统一低秩前向/反向传播**：直接在低秩子空间内计算前向和反向传播，大幅降低FLOPs和内存占用（Sec. 3.3, Eq. 8-11）。前向传播简化为 $\mathcal{A}_{i+1} = \mathcal{A}_i R_i^T L_i^T$，反向激活梯度为 $\widetilde{\frac{\partial \mathcal{L}}{\partial A_i}} = \widetilde{\frac{\partial \mathcal{L}}{\partial A_{i+1}}} \cdot L_i R_i$。

### 与现有方法的本质区别

WASI与**ASI**（Nguyen et al., 2025）的核心差异在于：ASI仅压缩激活，而WASI同时压缩权重和激活，形成统一的低秩训练框架。与**SVD-LLM**（Wang et al., 2024）相比，WASI不依赖额外的LoRA适配器，而是直接在SVD分解的本质上进行子空间迭代训练，在相同精度下实现高达100×的内存效率提升（Fig. 5, Sec. 4.3）。

### 局限性与待验证点

WASI目前主要在视觉Transformer（ViT, SwinT）上验证，尚未在数十亿参数的大规模语言模型上充分评估（仅尝试了TinyLlama）。压缩带来的精度损失在较低 $\varepsilon$ 值下依然存在。此外，该方法在更广泛的NLP下游任务（如文本生成、推理）上的表现，以及与量化、剪枝等技术的正交结合效果，仍需进一步探索。



![[assets/figures/papers/paper_list_l46_https_openreview_net_forum_id_0nvQ5kHXf4/figures/001_Figure_1.jpg]]
*Figure 1: Overview of WASI in a single training iteration*

WASI（Weight-Activation Subspace Iteration）构建了一个统一的低秩训练框架，其核心思想是：模型权重在微调过程中驻留于一个稳定的低秩子空间内，而激活图的能量也高度集中在少数主成分上。基于这一观察，WASI将前向传播、反向传播和参数更新全部迁移到压缩后的低秩表示中进行，从而在受控的信息损失约束下大幅降低内存占用和计算量。

整个pipeline由四个协同模块构成，在一个训练迭代中的执行流程如Figure 1所示：

1. **Weight Subspace Iteration (WSI)**：在训练开始时（t=0），对每一层的权重矩阵 $\mathcal{W}_i$ 执行完整的截断SVD，根据目标解释方差阈值 $\varepsilon$ 确定最优秩 $K_i$，得到低秩因子 $L_i = U_{i,(K_i)} \Sigma_{i,(K_i)}$ 和 $R_i = V_{i,(K_i)}^T$，使得 $\mathcal{W}_i \approx L_i R_i$。在后续迭代中，不再重复完整SVD，而是利用前一步的基进行暖启动的子空间迭代（warm-started subspace iteration），以极低的计算开销维持低秩表示的准确性。消融实验证实，WSI相比每步完整SVD节省1.36×的FLOPs即可达到同等精度，且在等FLOPs条件下精度高出约35%（Fig. 3b）。

2. **Activation Subspace Iteration (ASI)**：对每一层的激活张量 $\mathcal{A}_i$ 应用Tucker分解，将其压缩为核心张量 $\tilde{\mathcal{S}}_i$ 和三个模态的因子矩阵 $\tilde{U}_i^{(1)}, \tilde{U}_i^{(2)}, \tilde{U}_i^{(3)}$。与WSI类似，ASI采用暖启动子空间迭代替代昂贵的HOSVD，利用激活图能量集中于前几个奇异值的特性（Fig. 4），在保持关键信息的同时实现激活内存的大幅压缩。

3. **Explained-Variance Rank Selection**：权重侧的秩 $K_i$ 由解释方差阈值 $\varepsilon$ 自动确定——即选择最小的 $K_i$ 使得 $\sum_{j=1}^{K_i} \sigma_{i,j}^2 \geq \varepsilon \sum_j \sigma_{i,j}^2$。激活侧的秩选择则采用动态规划算法，在预调优困惑度约束下最小化总激活内存（详见附录A.2）。

4. **Unified Low-Rank Forward/Backward Pass**：前向传播直接使用低秩权重因子计算 $\mathcal{A}_{i+1} = \mathcal{A}_i R_i^T L_i^T$，反向传播中激活梯度通过 $\widetilde{\frac{\partial \mathcal{L}}{\partial A_i}} = \widetilde{\frac{\partial \mathcal{L}}{\partial A_{i+1}}} \cdot L_i R_i$ 传播，权重梯度则基于ASI压缩后的激活近似计算 $\widetilde{\frac{\partial \mathcal{L}}{\partial \mathcal{W}_i}}$。参数更新直接作用于低秩因子：$L_i R_i \leftarrow L_i R_i + \eta \cdot \widetilde{\frac{\partial \mathcal{L}}{\partial \mathcal{W}_i}}$。

整个框架通过单一的超参数 $\varepsilon$ 控制信息损失与资源消耗的权衡：$\varepsilon=1.0$ 等价于完整训练的vanilla模式，降低 $\varepsilon$ 则逐步增加压缩率。在ViT on CIFAR-10上，$\varepsilon=0.9$ 时WASI以仅1.08%的精度损失（96.24% vs. 97.32%）换取了13.1×的训练内存缩减（Table 1）；在SwinT上内存最高缩减62×，FLOPs降低1.5×（Fig. 6）；在TinyLlama上激活内存甚至缩减953.86×（Fig. 7）。在Raspberry Pi 5等边缘设备上，WASI实现了约1.4×的实际训练加速（Fig. 8, Table 2）。

> **待验证点**：WASI目前主要在视觉Transformer（ViT, SwinT）上验证，在数十亿参数LLM上的可扩展性尚未充分评估；此外，该方法在NLP领域的其他下游任务（如文本生成、推理）上的表现也需进一步实验确认。



### 3.1 标准前向与反向传播

在讨论压缩方法之前，先建立标准Transformer线性层的前向与反向传播形式。对于第 $i$ 层，给定激活张量 $\mathcal{A}_i$ 和权重矩阵 $\mathcal{W}_i$，前向传播为批矩阵乘法：

$$\mathcal{A}_{i+1} = \mathcal{A}_i \mathcal{W}_i^{\top} \tag{1}$$

反向传播需要计算两个梯度。权重梯度需要存储前向激活 $\mathcal{A}_i$：

$$\frac{\partial \mathcal{L}}{\partial \mathcal{W}_i} = \frac{\partial \mathcal{L}}{\partial \mathcal{A}_{i+1}}^{\top} \cdot \mathcal{A}_i \tag{2}$$

激活梯度用于继续反向传播至前层：

$$\frac{\partial \mathcal{L}}{\partial A_i} = \frac{\partial \mathcal{L}}{\partial A_{i+1}} \cdot \mathcal{W}_i \tag{3}$$

这正是资源瓶颈所在：存储完整的 $\mathcal{A}_i$ 和 $\mathcal{W}_i$ 导致内存需求过高，而矩阵乘法消耗大量计算资源。

### 3.2 激活子空间迭代 (ASI)

ASI对激活图进行Tucker低秩分解，将3D激活张量 $\mathcal{A}_i$ 压缩为核心张量 $\tilde{\mathcal{S}}_i$ 和三个模式上的因子矩阵：

$$\mathcal{A}_i \approx \tilde{\mathcal{S}}_i \times_1 \tilde{U}_i^{(1)} \times_2 \tilde{U}_i^{(2)} \times_3 \tilde{U}_i^{(3)} \tag{4}$$

其中 $\times_n$ 表示第 $n$ 模的张量-矩阵乘积。与传统的HOSVD不同，ASI采用**热启动子空间迭代**：利用前一迭代步的因子矩阵作为初始基，通过正交化迭代逼近最优子空间，避免每次重新计算完整SVD。秩选择通过动态规划在预微调困惑度约束下最小化总激活内存（详见附录A.2）。

### 3.3 权值子空间迭代 (WSI) 与统一低秩训练

**核心洞察**：微调过程中模型参数驻留在稳定的低秩子空间内（Fig. 3a验证了奇异值跨epoch的稳定性）。WSI利用这一性质，对权重矩阵进行截断SVD：

$$\mathcal{W}_i = U_i \Sigma_i V_i^T \tag{5}$$

在 $t=0$ 时执行完整SVD确定本质子空间，之后通过子空间迭代更新因子。给定目标解释方差阈值 $\varepsilon$，最优秩 $K_i$ 定义为满足 $\sum_{j=1}^{K_i} \sigma_{i,j}^2 \geq \varepsilon \cdot \sum_j \sigma_{i,j}^2$ 的最小整数。低秩近似为：

$$\tilde{\mathcal{W}}_i = L_i R_i, \quad L_i = U_{i,(K_i)} \Sigma_{i,(K_i)}, \quad R_i = V_{i,(K_i)}^T \tag{6-7}$$

其中 $L_i \in \mathbb{R}^{O \times K_i}$，$R_i \in \mathbb{R}^{K_i \times I}$。

**统一低秩前向传播**直接使用低秩因子：

$$\mathcal{A}_{i+1} = \mathcal{A}_i R_i^T L_i^T \tag{8}$$

**统一低秩反向传播**同样在子空间内进行。激活梯度通过低秩因子回传：

$$\widetilde{\frac{\partial \mathcal{L}}{\partial A_i}} = \widetilde{\frac{\partial \mathcal{L}}{\partial A_{i+1}}} \cdot L_i R_i \tag{10}$$

权重梯度利用ASI压缩后的激活 $\tilde{\mathcal{A}}_i$ 计算：

$$\widetilde{\frac{\partial \mathcal{L}}{\partial \mathcal{W}_i}} = f_{\mathrm{LR}}\left(\tilde{\mathcal{A}}_i, \widetilde{\frac{\partial \mathcal{L}}{\partial \mathcal{A}_{i+1}}}\right) \tag{9}$$

其中 $f_{\mathrm{LR}}$ 的具体展开涉及对3D激活张量的模式积重组（详见附录A.1，Eq. 12-18），核心思想是将高维张量收缩转化为低秩因子上的高效计算。

**权值更新**直接作用于低秩因子：

$$L_i R_i = L_i R_i + \eta \cdot \widetilde{\frac{\partial \mathcal{L}}{\partial \mathcal{W}_i}} \tag{11}$$

### 3.4 计算与内存压缩的理论分析

从理论角度，对于维度为 $O \times I$ 的权重矩阵和批大小为 $B$ 的激活，WASI将训练内存从 $O(BI + OI)$ 压缩至 $O(B\sum_m r_{i,m} + K_i(O+I))$，其中 $r_{i,m}$ 为激活各模的秩。Figure 2展示了不同维度和秩配置下的压缩率 $C_{\mathrm{training}}$、$C_{\mathrm{inference}}$ 及加速比 $S_{\mathrm{training}}$、$S_{\mathrm{inference}}$ 的演变趋势。

### 关键模块总结

| 模块 | 功能 | 核心机制 |
|------|------|----------|
| **WSI** | 权重低秩分解 | $t=0$ 时完整SVD定基，后续热启动子空间迭代 |
| **ASI** | 激活低秩压缩 | Tucker分解 + 热启动子空间迭代替代HOSVD |
| **解释方差秩选择** | 自动确定最优秩 | 权重按 $\varepsilon$ 阈值截断；激活用动态规划 |
| **统一低秩前向/反向** | 子空间内端到端计算 | Eq. 8-11，大幅降低FLOPs和内存 |



## 实验与关键发现

### 核心假设验证：权重与激活的低秩稳定性

WASI 的设计建立在两个关键假设之上：权重矩阵在微调过程中驻留于稳定低秩子空间，以及激活图的能量集中于少数主成分。实验对此进行了系统验证。

**权重子空间稳定性**（Fig. 3a, Sec. 4.2）：在 Pets 数据集上微调 ViT 时，第 6 层权重矩阵 $W_6$ 的奇异值在不同 epoch 间表现出显著稳定性。这一观察支持了 WSI 的核心逻辑——仅在 $t=0$ 时执行一次完整 SVD 确定必要子空间，后续训练步中通过子空间迭代（subspace iteration）复用前一时刻的正交基，从而避免每步进行昂贵的 SVD 计算。

![[assets/figures/papers/paper_list_l46_https_openreview_net_forum_id_0nvQ5kHXf4/figures/005_Figure_3.jpg]]
*Figure 3: When fine-tuning ViT on the Pets dataset, (a) illustrates the evolution of singular values of $\mathcal { W } _ { 6 }$ across epochs; (b) compares WSI and full SVD in terms of accuracy and training FLOPs under varying explained variance thresholds, ε ∈ {0.4, 0.5, 0.6, 0.7, 0.8, 0.9}. (a)*

**WSI 效率验证**（Fig. 3b）：在相同解释方差阈值 $\varepsilon \in \{0.4, 0.5, 0.6, 0.7, 0.8, 0.9\}$ 下，WSI 相比每步执行完整 SVD 的方案，在达到相同精度时减少 1.36 倍训练 FLOPs；在等量 FLOPs 约束下，WSI 的精度高出约 35 个百分点。这表明子空间迭代的近似质量足以替代昂贵的精确分解。

**激活能量集中性**（Fig. 4）：对 ViT 微调过程中各层激活图 $A_i$ 的奇异值分解显示，解释方差高度集中于前几个奇异值，验证了 ASI 采用 Tucker 分解压缩激活图的合理性。

### 主要结果：资源效率与精度权衡

#### ViT 在 CIFAR-10 上的综合评估

Table 1 报告了 WASI 应用于 ViT 所有线性层（包括注意力投影和 MLP 块）的完整结果。以 $\varepsilon=0.9$ 为例：

![[assets/figures/papers/paper_list_l46_https_openreview_net_forum_id_0nvQ5kHXf4/figures/030_Table_1.jpg]]
*Table 1: Performance of WASI with different ε values on all linear layers (including attention blocks and MLP blocks) of ViT using the CIFAR-10 dataset. Note that ε = 1.0 corresponds to vanilla training*

- 训练内存从 vanilla 的 2349.00 MB 降至 179.61 MB（**13.1 倍压缩**）；
- 推理内存从 324 MB 降至 32 MB（约 10 倍压缩）；
- 训练 FLOPs 和推理 FLOPs 分别获得显著降低；
- 精度从 97.32% 略微下降至 96.24%（**仅损失 1.08 个百分点**）。

随着 $\varepsilon$ 从 0.4 增加到 1.0，资源消耗单调递增，精度也随之提升。$\varepsilon$ 作为信息损失控制旋钮，允许用户在资源约束与精度需求之间灵活调节。

#### 与 SVD-LLM 的对比

Fig. 5 将 WASI 与 SVD-LLM（Wang et al., 2024）进行直接对比。在相似精度水平下，WASI 的内存效率高出 SVD-LLM 高达 **100 倍**。这一差距源于 WASI 同时压缩权重和激活，而 SVD-LLM 仅对模型权重进行低秩分解，未触及激活存储这一主要内存瓶颈。

![[assets/figures/papers/paper_list_l46_https_openreview_net_forum_id_0nvQ5kHXf4/figures/011_Figure_5.jpg]]
*Figure 5: Resource consumption during fine-tuning and inference of ViT on the CIFAR-10 dataset. Each marker in the plots corresponds to a different compression rate, with the red diamond indicating vanilla training*

#### SwinT 跨数据集泛化

Fig. 6 展示了 WASI 在 Swin Transformer 上的跨数据集表现。在 $\varepsilon=0.9$ 时，WASI 匹配 vanilla 精度的同时，训练内存降低高达 **62 倍**，FLOPs 降低 1.5 倍。该结果验证了方法在不同视觉架构和数据集上的鲁棒性。

![[assets/figures/papers/paper_list_l46_https_openreview_net_forum_id_0nvQ5kHXf4/figures/015_Figure_6.jpg]]
*Figure 6: Resource consumption when applying WASI for fine-tuning and inference of SwinT across different datasets. Each marker along the curves represents a different compression rate, while the final marker on each curve corresponds to vanilla training*

#### 语言模型初步验证

Fig. 7 报告了 TinyLlama 在 BoolQ 上的微调结果。WASI 将激活内存降低高达 **953.86 倍**，权重内存降低 30.12 倍，且不损失精度。图表中每个标记代表从最后一层向上微调的层数——靠近 y 轴的标记对应仅微调最后一层，向右依次增加微调层数。WASI 在所有层数配置下均保持与 vanilla 相当的精度，同时大幅压缩内存。

![[assets/figures/papers/paper_list_l46_https_openreview_net_forum_id_0nvQ5kHXf4/figures/019_Figure_7.jpg]]
*Figure 7: Performance of WASI vs. vanilla training when fine-tuning TinyLlama on BoolQ. Each marker indicates the number of layers fine-tuned from the last layer upward: the marker closest to the y-axis of each figure corresponds to fine-tuning only the last layer, the next marker corresponds to the last two layers, and so on*

### 边缘设备实测

#### 延迟与吞吐

Fig. 8 和 Table 2 报告了 Raspberry Pi 5 上的实测延迟。在 $\varepsilon=0.9$ 时，WASI 的训练和推理速度比 vanilla 快约 **1.4 倍**。Table 3 进一步扩展到 Jetson Orin、Jetson Nano 和 Raspberry Pi 4 三款边缘设备，均观察到一致的加速趋势。

![[assets/figures/papers/paper_list_l46_https_openreview_net_forum_id_0nvQ5kHXf4/figures/032_Table_2.jpg]]
*Table 2: Comparison of inference and training time (s) when applying WASI, ASI, and vanilla training to fine-tune ViT on Raspberry Pi 5 at different ε values*

![[assets/figures/papers/paper_list_l46_https_openreview_net_forum_id_0nvQ5kHXf4/figures/033_Table_3.jpg]]
*Table 3: On-device latency of fine-tuning ViT on one minibatch of 128 CIFAR-10 samples initialized with ImageNet-pretrained weights. We report the time for one inference pass and one training iteration on three edge devices*

#### 能耗

Table 4 测量了 Jetson Orin 上的能耗。以 $\varepsilon=0.9$ 为例，WASI 的推理和训练能耗均显著低于 vanilla（$\varepsilon=1.0$）。能耗随 $\varepsilon$ 单调递增，与计算量正相关。

![[assets/figures/papers/paper_list_l46_https_openreview_net_forum_id_0nvQ5kHXf4/figures/034_Table_4.jpg]]
*Table 4: Energy consumption of WASI on Jetson Orin with different ε. Note that $\varepsilon$ = 1 . 0 corresponds to vanilla training*

### 消融实验

**随机种子稳定性**（Fig. 9）：在 Pets 数据集上使用三个不同随机种子重复实验，WASI 在不同 $\varepsilon$ 下的精度和内存使用均表现出低标准差，验证了方法的可复现性。

![[assets/figures/papers/paper_list_l46_https_openreview_net_forum_id_0nvQ5kHXf4/figures/029_Figure_9.jpg]]
*Figure 9: WASI performance on the with different ε values, showing mean accuracy and memory usage across three random seeds. Error bars represent standard deviation*

**卷积网络上的局限性**（Fig. 12）：将 WSI 应用于已高度紧凑的卷积网络 MCUNet 时，内存节省有限，且在高 $\varepsilon$ 下反而可能增加内存占用。这表明 WASI 主要适用于参数冗余度较高的 Transformer 架构，对已优化的轻量级卷积网络增益不明显。

![[assets/figures/papers/paper_list_l46_https_openreview_net_forum_id_0nvQ5kHXf4/figures/031_Figure_12.jpg]]
*Figure 12: Performance of WSI when applied to fine-tune MCUNet (pretrained on ImageNet-1K) on Pets dataset. The number next to each marker indicates how many convolutional layers WSI was applied to*

**全线性层应用**（Table 1）：WASI 不仅适用于 MLP 块，在同时压缩注意力投影层时仍保持有效，精度损失可控。

### 已知局限

1. **模型规模限制**：受硬件条件约束，实验未能在数十亿参数的大型 LLM 上验证，仅测试了 TinyLlama 这一较小规模语言模型。
2. **任务覆盖不足**：NLP 实验仅限于 BoolQ 问答任务，尚未在文本生成、推理等更广泛的下游任务上评估。
3. **精度损失存在**：在较低 $\varepsilon$ 值下，精度下降较为明显，$\varepsilon$ 的选择需要在资源与精度之间权衡。
4. **架构适用性**：如 MCUNet 实验所示，方法对已紧凑设计的卷积架构增益有限。

### 补充图表

![[assets/figures/papers/paper_list_l46_https_openreview_net_forum_id_0nvQ5kHXf4/figures/024_Figure_10.jpg]]
*Figure 10: WASI performance when fine-tuning ViT across multiple datasets. In each plot, markers from left to right represent increasing values of ε; the rightmost marker corresponds to vanilla training*



## 定位与知识库关联

### 与基线方法的关系

**WASI** 的核心贡献在于首次将权重压缩与激活压缩统一到同一个低秩子空间框架中，其设计直接回应了两类现有方法的局限性。

**ASI**（Nguyen et al., 2025）是本工作的直接前身，仅对激活图进行 Tucker 分解压缩，权重仍以全矩阵形式存储和更新。WASI 在此基础上新增了 **Weight Subspace Iteration (WSI)** 模块，将权重也纳入低秩表示，从而实现了训练全链路的压缩。这一扩展使得内存节省从仅激活端扩展至权重端，在 TinyLlama 上激活内存压缩比从 ASI 的已有水平进一步提升至最高 953.86×（Fig. 7）。

**SVD-LLM**（Wang et al., 2024）代表了另一条技术路线——通过对预训练权重进行一次性 SVD 分解并配合 LoRA 适配器进行微调。WASI 与之的关键差异在于：SVD-LLM 仅在训练开始时做一次静态分解，而 WSI 在每轮迭代中通过**子空间迭代**动态更新低秩因子，避免了静态分解在微调后期因参数漂移导致的信息损失。这一设计使 WASI 在同等精度下实现了高达 100× 的内存效率优势（Fig. 5），且 WSI 相比全量 SVD 在同等精度下节省 1.36× FLOPs（Fig. 3b）。

**Vanilla Training** 作为全量微调基线，代表了无压缩的上界性能。WASI 在 ε=0.9 时，ViT 在 CIFAR-10 上的精度仅下降 1.08%（97.32% → 96.24%），同时训练内存减少 13.1×（Table 1）；在 SwinT 上内存最高减少 62×，FLOPs 减少 1.5×（Fig. 6）。

### 适用边界

WASI 的有效性建立在两个经验假设之上，这些假设在视觉 Transformer 上得到了充分验证，但泛化边界需要审慎界定：

1. **权重子空间稳定性假设**：模型参数在微调过程中驻留在一个稳定的低秩子空间内。Fig. 3a 显示 ViT 第 6 层权重的奇异值在微调各 epoch 间保持显著稳定，这为 WSI 的子空间迭代策略提供了经验支撑。然而，这一假设在**持续学习**或**大规模领域迁移**场景下是否仍然成立，目前缺乏验证。

2. **激活能量集中假设**：激活图的解释方差集中在少数主成分上。Fig. 4 证实了 ViT 激活图各模态的奇异值能量高度集中，验证了 ASI 低秩近似的合理性。但对于具有长距离依赖的复杂 NLP 任务（如长文本生成），激活模式的低秩性可能需要更大秩才能保持。

**已验证的适用场景**：
- 视觉 Transformer（ViT, SwinT）在标准图像分类数据集（CIFAR-10, Pets 等）上的微调
- TinyLlama 在 BoolQ 问答任务上的微调
- 边缘设备（Raspberry Pi 5, Jetson Orin）上的部署推理与训练

**效果衰减场景**：
- 当 WSI 应用于已经高度紧凑的卷积网络（如 MCUNet）时，内存节省效果有限，甚至在高 ε 值下因低秩因子的额外开销导致内存增加（Fig. 12）。这表明 WASI 更适合参数量大、冗余度高的 Transformer 架构，而非已经过精心压缩的轻量级模型。
- 在极低的 ε 值（ε < 0.7）下，精度损失显著增加，说明过度的信息压缩会损害模型表达能力。

### 局限与开放问题

**已确认的局限**：

1. **模型规模验证不足**：受硬件限制，WASI 目前仅在 TinyLlama（约 1.1B 参数）上进行了语言模型验证，尚未在数十亿参数级别的大型 LLM 上测试。大规模模型的权重子空间稳定性和激活低秩性是否保持相同特性，仍需实证检验。

2. **任务覆盖有限**：NLP 实验仅覆盖了 BoolQ 问答任务，缺乏在文本分类、摘要生成、推理等更广泛下游任务上的评估。

3. **精度损失不可避免**：尽管在 ε=0.9 时精度损失可控，但压缩本质上是有损的，在需要极高精度的应用场景中可能不可接受。

**待探索的开放问题**：

1. **大规模 LLM 扩展**：如何将 WASI 扩展到数十亿参数的语言模型？大规模模型中的子空间维度选择、子空间迭代的计算开销与收益权衡需要重新评估。

2. **与正交压缩技术的结合**：WASI 目前独立于量化、剪枝、知识蒸馏等技术。能否将这些方法与低秩子空间训练正交结合，实现多维度压缩的叠加效应？

3. **子空间动态性的深入理解**：在持续学习、领域自适应、指令微调等场景中，参数子空间是否会随任务分布变化而发生显著漂移？当前逐迭代的子空间迭代策略是否需要调整？

4. **秩选择的自适应优化**：当前权重秩由解释方差阈值 ε 统一控制，激活秩通过动态规划在预调困惑度约束下分配。能否将秩选择过程与训练目标联合优化，实现端到端的自适应压缩？

5. **更广泛架构的适用性**：WASI 的核心操作基于线性层的矩阵乘法分解，理论上可扩展至任何以线性层为主的计算单元。但在注意力机制、混合专家模型（MoE）等复杂架构中的表现和适配方案尚未探索。



## 原文 PDF

![[paperPDFs/ICLR_2026/Efficient_Resource_Constrained_Training_of_Transformers_via_Subspace_Optimization.pdf]]
