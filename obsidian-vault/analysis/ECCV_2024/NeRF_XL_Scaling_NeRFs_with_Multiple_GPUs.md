---
title: "NeRF-XL: Scaling NeRFs with Multiple GPUs"
type: paper
paper_level: A
venue: ECCV
year: 2024
pdf_ref: paperPDFs/ECCV_2024/NeRF_XL_Scaling_NeRFs_with_Multiple_GPUs.pdf
project_link: https://research.nvidia.com/labs/toronto-ai/nerfxl/
code_link: null
aliases:
- NX
- NeRF-XL
tags:
- ECCV_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "将多个NeRF联合训练，每个GPU仅负责一个不重叠的空间区域（tile），并在前向传播中进行全局信息汇集以还原单GPU的体渲染数学等价性；同时通过将体渲染方程和损失函数重写为分段积分与alpha合成形式，将GPU间通信量从O(S K²)降至O(S²)，实现高效的分布式渲染与训练。"
primary_logic: "体渲染、透过率、累积权重和深度乃至畸变损失均属于“可分解积分族”，能够分解为各段的独立积分和跨段的加权组合。基于该性质，只需在GPU间交换极少量每段汇总数据即可合成精确的全局体渲染结果，从而使完全无交叠的分布式NeRF在训练和推理上数学等价于单GPU版本，既消除了独立训练方案的冗余与混合伪影，又极大降低了多GPU通信开销。"
claims:
- "Mega-NeRF 在 University4 上使用 2/4/8 个 tile 时，分别有 38%/56%/62% 的采样点落在指定 tile 区域之外，表明独立训练造成严重的容量冗余。"
- "通过重写体渲染方程，多GPU数据交换从O(K S²)降至O(S²)，实际通信成本降低超过2倍。"
- "在 Garden、Building、University4 和 MatrixCity 上，提出的联合训练方法随着GPU数量增加在PSNR和渲染速度上均实现近似线性提升，而Block-NeRF和Mega-NeRF等基线方法的PSNR保持不变或下降。"
- "Garden 上 PSNR = 随GPU数量增加近似线性提升"
---

# NeRF-XL: Scaling NeRFs with Multiple GPUs

> [!tip] 核心洞察
> 体渲染、透过率、累积权重和深度乃至畸变损失均属于“可分解积分族”，能够分解为各段的独立积分和跨段的加权组合。基于该性质，只需在GPU间交换极少量每段汇总数据即可合成精确的全局体渲染结果，从而使完全无交叠的分布式NeRF在训练和推理上数学等价于单GPU版本，既消除了独立训练方案的冗余与混合伪影，又极大降低了多GPU通信开销。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | NeRF-XL：通过多GPU扩展神经辐射场 |
| 英文题名 | NeRF-XL: Scaling NeRFs with Multiple GPUs |
| 会议/期刊 | ECCV 2024 |
| Links | [paper](https://arxiv.org/abs/2404.16221) · [Project](https://research.nvidia.com/labs/toronto-ai/nerfxl/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | NeRF-XL |
| Dataset | Garden, Building, University4, MatrixCity |

> [!tip] 效果简介
> - Garden 上，PSNR 为 随GPU数量增加近似线性提升，对比 无明显提升（Block-NeRF, Mega-NeRF），变化 显著。
> - Building 上，PSNR 为 随GPU数量增加提升，对比 无明显提升或下降，变化 显著。
> - University4 上，PSNR 为 随GPU数量增加提升，对比 无明显提升，变化 显著。

## 概要

**问题瓶颈**：现有基于独立训练的多GPU NeRF方法（如 **Block-NeRF**（Tancik et al., 2022）和 **Mega-NeRF**（Turki et al., CVPR 2022））面临三重困境。其一，每个独立NeRF被迫同时建模焦点区域与周围背景，造成严重的**容量冗余**——在University4场景上，Mega-NeRF使用2/4/8个tile时，分别有38%/56%/62%的采样点落在指定区域之外（Fig. 2）。冗余度随GPU数量增加而加剧，使得增加计算资源无法转化为重建质量提升。其二，渲染时需对重叠区域进行2D或3D混合，引入**模糊与伪影**（Fig. 3, Fig. 5）。其三，各NeRF独立优化相机或外观嵌入，导致**跨区域不一致**，进一步恶化混合渲染质量（Fig. 4）。这些因素共同导致基线方法的PSNR和渲染速度随GPU增加而保持不变甚至下降（Fig. 8）。

**核心思路**：NeRF-XL将体渲染、透过率、累积权重、深度乃至畸变损失统一视为**可分解积分族**——每条光线的全局积分可分解为各段的独立积分与跨段的加权组合。基于这一数学性质，NeRF-XL将场景划分为不重叠的tile，每个GPU仅负责一个tile的NeRF实例，在前向传播中仅交换每段汇总数据（而非逐采样点通信）即可合成精确的全局体渲染结果，反向传播则仅计算局部梯度。这使得完全无交叠的分布式NeRF在训练和推理上**数学等价于单GPU版本**，同时将GPU间通信量从$O(K S^2)$降至$O(S^2)$，实际通信成本降低超过2倍（Fig. 12）。

**方法定位**：NeRF-XL属于**联合训练式多GPU NeRF**，区别于独立训练+混合渲染范式（Block-NeRF、Mega-NeRF）和光线并行范式（PyTorch DDP）。其关键设计包括：基于SfM点云或射线采样CDF的递归二分空间划分以平衡负载；分tile独立hash编码与密度MLP配合DDP共享颜色MLP；前向全局汇集与反向局部梯度的通信模式；以及将体渲染方程和畸变损失重写为分段合成形式以最小化通信量。

**主要结果**：在Garden、Building、University4和MatrixCity四个异构场景上，NeRF-XL随GPU数量增加在PSNR和渲染速度上均实现**近似线性提升**，而Block-NeRF和Mega-NeRF等基线方法无明显改善（Fig. 8）。消融实验表明，大场景NeRF更受益于增加模型容量而非增多光线（Fig. 11），且分段式体渲染是通信效率的关键使能技术（Fig. 12）。

### 大规模场景重建与神经辐射场

神经辐射场（NeRF）已成为三维场景重建与视图合成的核心范式，其通过多层感知机（MLP）隐式编码场景的几何与外观，并利用体渲染方程沿光线积分颜色与密度来生成像素值。然而，单GPU的内存与算力限制使得NeRF难以直接扩展至城市级乃至更大规模场景——单个GPU所能容纳的模型参数和处理的采样光线数量均存在硬性上限，这构成了大规模NeRF训练的根本瓶颈。

### 现有多GPU方案的困境

为突破单GPU限制，研究者提出了多种多GPU分布式NeRF方案，其中最具代表性的是基于独立训练的**Block-NeRF**（Tancik et al., 2022）和**Mega-NeRF**（Turki et al., CVPR 2022）。这些方法将场景划分为若干重叠的空间区域，每个GPU独立训练一个覆盖其指定区域的NeRF，渲染时再通过2D混合（Block-NeRF）或3D混合（Mega-NeRF）合成最终图像。然而，这种“分而治之”的策略存在三个深层缺陷，导致增加GPU资源无法有效提升重建质量：

**容量冗余（Capacity Redundancy）**：每个独立训练的NeRF被迫同时建模其焦点区域和周围背景，因为渲染一条穿越多个区域的光线时，各NeRF需要独立输出该光线在其覆盖段内的颜色与密度。这种冗余随GPU数量增加而急剧恶化——在University4场景上，Mega-NeRF使用2/4/8个tile时，分别有38%/56%/62%的采样点落在指定tile区域之外，表明大量算力被浪费在重复建模上。

**混合伪影（Blending Artifacts）**：独立训练后，各NeRF对场景的理解并不一致，渲染时需通过2D或3D混合合成最终图像。2D混合（如Block-NeRF）直接在图像空间加权平均，不可避免地引入模糊；3D混合（如Mega-NeRF）虽在体素空间操作，但各NeRF独立优化的相机位姿和外观嵌入可能产生跨区域不一致——相机优化本质上是一个“移动相机还是移动场景”的模糊问题，独立训练导致各NeRF做出不同选择，进而使混合渲染产生严重伪影。实验表明，在Mega-NeRF中即使使用15%的空间重叠，3D混合仍会引入明显伪影。

**资源利用失效**：由于上述问题，Block-NeRF和Mega-NeRF等基线方法在Garden、Building、University4和MatrixCity等多个场景上，随着GPU数量增加，PSNR和渲染速度均无明显提升甚至下降，未能实现分布式计算应有的性能增益。

### 关键洞察与本文动机

上述困境的根源在于独立训练破坏了体渲染的全局一致性。本文的核心洞察是：**体渲染、透过率、累积权重乃至畸变损失均属于“可分解积分族”**——它们可以分解为各段的独立积分与跨段的加权组合。这意味着，若能将多个NeRF联合训练，并在前向传播中汇集各GPU的段内汇总数据，即可合成与单GPU完全等价的全局体渲染结果，从而从根本上消除独立训练的冗余与混合伪影。

基于这一洞察，本文提出**NeRF-XL**，一种原则性的多GPU联合训练框架，其设计目标包括：

1. **数学等价性**：分布式体渲染结果与单GPU版本严格一致，确保训练与推理的一致性；
2. **高效通信**：通过重写体渲染方程，将GPU间数据交换从样本级（$O(K S^2)$）降至tile级（$O(S^2)$），使通信成本降低超过2倍；
3. **线性可扩展性**：随GPU数量增加，模型容量和渲染质量实现近似线性提升，真正释放多GPU资源的潜力。

## 核心方法与创新机理

NeRF-XL 的核心创新在于将“独立训练 + 后混合”的多 GPU 范式彻底重构为**数学等价于单 GPU 的联合训练框架**，从根本上消除了容量冗余、混合伪影和训练-推理不一致三大瓶颈。其关键改动体现在以下四个维度。

### 从独立训练到联合训练：消除容量冗余与混合伪影

现有方法（**Block-NeRF**，Tancik et al., 2022；**Mega-NeRF**，Turki et al., CVPR 2022）在每个 GPU 上独立训练一个 NeRF，各 NeRF 需覆盖重叠的空间区域，并在渲染时通过 2D 或 3D 混合合成最终图像。这一设计导致三个连锁问题：

1. **容量冗余**：每个独立 NeRF 被迫同时建模其焦点区域和周围背景，冗余度随 GPU 数量增加而急剧恶化。在 University4 场景上，Mega-NeRF 使用 2×/4×/8× tile 时，分别有 38%/56%/62% 的射线采样点落在指定 tile 区域之外，直接量化了这一冗余程度（置信度 0.95）。
2. **混合伪影**：2D 混合引入模糊，3D 混合则因各 NeRF 独立优化相机或外观嵌入导致跨区域不一致，产生严重伪影（见 Fig. 3–5）。
3. **训练-推理不一致**：训练时各 NeRF 独立，推理时需混合，两者存在本质差异。

NeRF-XL 将多个 NeRF **联合训练**，每个 GPU 仅负责一个不重叠的空间区域（tile），并在前向传播期间进行全局信息汇集（broadcast），使每个 GPU 获得完整的体渲染结果。反向传播时，各 GPU 仅计算自己参数的局部梯度，无需跨 GPU 梯度同步。这一设计使得训练与推理使用完全相同的渲染方式，从根本上消除了混合步骤及其伴随的伪影。

### 分段体渲染：将通信量从 O(K S²) 降至 O(S²)

联合训练的朴素实现需要在 GPU 间交换每个采样点的颜色和密度，通信量为 $O(K S^2)$（$K$ 为每射线采样点数，$S$ 为 GPU 数量），在多 GPU 场景下迅速成为瓶颈。

NeRF-XL 的核心洞察是：**体渲染、透过率、累积权重、深度乃至畸变损失均属于“可分解积分族”**，可以分解为各段的独立积分和跨段的加权组合。基于此，作者将体渲染方程重写为分段形式：

$$C(t_1 \to t_{N+1}) = \sum_{k=1}^N T(t_1 \to t_k) \, C(t_k \to t_{k+1})$$

其中 $T(t_1 \to t_k) = \prod_{i=1}^{k-1} T(t_i \to t_{i+1})$ 为到第 $k$ 段的累积透过率。类似地，畸变损失 $\mathcal{L}_{dist}$ 也被分解为段内惩罚与跨段辅助项的组合（Equation 7–8）。这一重写将采样级全局组合转化为 tile 级汇总数据交换，通信量从 $O(K S^2)$ 降至 $O(S^2)$，实际通信成本降低超过 2 倍（Fig. 12，置信度 0.95）。

### 基于 CDF 的负载均衡空间划分

独立训练方法通常采用均匀网格或基于轨迹的启发式划分，易导致各 GPU 负载不均衡。NeRF-XL 提出基于场景内容分布的递归二分策略：从 SfM 稀疏点云或训练射线采样点构建 3D 点分布，沿各轴计算累积分布函数（CDF），在 CDF = 0.5 处选择使分区宽高比最接近 1 的平面进行切分，递归执行以生成 2 的幂次个 tile（Fig. 13）。该策略使各 tile 内场景内容量近似相等，尽可能平衡 GPU 计算负载（置信度 0.95）。

### 与其他并行范式的本质区别

NeRF-XL 的扩展路径与 PyTorch DDP 的光线并行形成鲜明对比：DDP 通过分发更多光线到多 GPU 来加速渲染，但模型容量不变；NeRF-XL 则将模型参数分布到多 GPU，使总参数量随 GPU 数量线性增长。在 University4 上的消融实验表明，使用 N 个 GPU 获得 N 倍参数的 NeRF-XL，其 PSNR 远超仅通过 N 倍光线并行的 DDP，表明**大场景 NeRF 更需要增加模型容量而非增多光线**（Fig. 11，置信度 0.9）。

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2404_16221/figures/006_Figure_6.jpg]]
*Figure 6: Our Training Pipeline. Our method jointly trains multiple NeRFs across all GPUs, each of which covers a disjoint spatial region. The communication across GPUs only happens in the forward pass but not the backward pass (shown in gray arrows). (a) We can train this system by evaluating each NeRF to get the sample color and density, then broadcast these values to all other GPUs for a global volume rendering (§ 4.2). (b) By rewriting volume rendering equation we can dramatically reduce the data transfer to one value per-ray, thus improving efficiency (§ 4.3)*

NeRF-XL 提出了一种原则性的多 GPU 联合训练范式，其核心在于将 3D 空间划分为互不重叠的 tile，每个 GPU 仅负责一个 tile 内的 NeRF 实例，并通过前向传播中的全局信息汇集来实现与单 GPU 体渲染在数学上等价的分布式渲染。整个 pipeline 由四个关键模块串联而成：**空间划分**、**分 tile NeRF 实例**、**前向全局汇集** 和 **分段体渲染与损失重构**，反向传播仅计算局部梯度，无需跨 GPU 梯度通信。

### 模块关系与数据流

1. **空间划分**  
   在训练开始前，系统基于场景的 SfM 稀疏点云或训练射线的采样点构建 3D 点分布的概率密度函数（PDF），沿 x、y、z 轴分别计算累积分布函数（CDF），递归地在 CDF=0.5 处选择使划分后区域宽高比最接近 1 的平面进行二分。该过程递归执行，生成 2 的幂次个不重叠 tile（2×、4×、8×…），使得每个 tile 内的场景内容量近似相等，从而尽可能平衡各 GPU 的计算负载（Fig. 13, Fig. 14）。

2. **分 tile NeRF 实例**  
   每个 GPU 维护一个独立的 NeRF 实例，拥有独立的 hash encoding 和密度 MLP，但颜色 MLP 通过 PyTorch DDP 在所有 GPU 间共享参数。这种设计使得模型容量随 GPU 数量线性扩展（N 个 GPU 即 N 倍可学习参数），同时共享颜色 MLP 有助于保持跨区域的外观一致性。采样区间被严格限制在各 tile 的边界框内，确保样本不会跨越 tile 边界。

3. **前向全局汇集**  
   每条光线根据其穿越的 tile 序列被分段，各 GPU 仅查询自己 tile 内样本的颜色和密度。随后，通过 broadcast 操作将所有 GPU 的局部查询结果汇集到每个 GPU 上，使每个 GPU 都能执行完整的全局体渲染。这一汇集过程仅发生在前向传播中，反向传播时各 GPU 仅计算自己参数的局部梯度，无需梯度同步。

4. **分段体渲染与损失重构**  
   这是整个框架的理论基石。体渲染方程、透过率、累积权重、深度乃至畸变损失均属于“可分解积分族”，可以被分解为各段内的独立积分与跨段的加权组合。具体而言，整条光线的颜色 $C(t_1 \to t_{N+1})$ 可表示为各段颜色 $C(t_k \to t_{k+1})$ 以累积透过率 $T(t_1 \to t_k)$ 为权重的加权和：

   $$C(t_1 \to t_{N+1}) = \sum_{k=1}^N T(t_1 \to t_k) \, C(t_k \to t_{k+1})$$

   其中累积透过率 $T(t_1 \to t_k) = \prod_{i=1}^{k-1} T(t_i \to t_{i+1})$。畸变损失 $\mathcal{L}_{dist}$ 同样可分解为段内惩罚与跨段辅助项的组合。基于此，GPU 间仅需交换每段的汇总数据（颜色、透过率、累积权重、深度），而非所有采样点的原始数据，将通信量从 $O(K S^2)$ 降至 $O(S^2)$（其中 $K$ 为每段样本数，$S$ 为 tile 数），实际通信成本降低超过 2 倍（Fig. 12）。全局组合通过并行 prefix scan 高效实现。

### 关键设计决策

- **无重叠 + 联合训练**：与 Block-NeRF（50% 重叠，2D 混合）和 Mega-NeRF（15% 重叠，3D 混合）不同，NeRF-XL 使用完全无重叠的 tile，从根本上消除了独立训练带来的容量冗余和混合渲染伪影。Mega-NeRF 在 University4 上使用 2×/4×/8× tile 时，分别有 38%/56%/62% 的采样点落在指定 tile 区域之外，直观说明了独立训练的冗余程度。
- **训练-推理一致性**：联合体渲染在训练和推理阶段使用完全相同的计算路径，无需任何 2D 或 3D 混合，消除了训练-推理不一致导致的性能退化。
- **仅前向通信**：反向传播无需跨 GPU 梯度同步，这是通过将体渲染和损失函数重写为分段形式实现的——各 GPU 的局部梯度计算仅依赖前向汇集后的全局量，从而天然解耦了反向传播的依赖关系。

### 核心模块

NeRF-XL 由五个关键模块构成，共同实现无交叠、数学等价的分布式 NeRF 训练与渲染。

**空间划分（Spatial Partitioning）**。系统首先根据场景的 SfM 稀疏点云或训练射线采样点构建三维点分布，沿各轴计算累积分布函数（CDF），递归地在 CDF=0.5 处选择使划分后包围盒长宽比最接近1的平面进行二分，生成 2 的幂次个不重叠 tile，每个 tile 分配给一个 GPU。该策略使各 tile 内场景内容量近似相等，尽可能平衡 GPU 计算负载（Fig. 13, Fig. 14）。

**分 tile NeRF 实例**。每个 GPU 维护独立的 hash 编码和密度 MLP，而颜色 MLP 通过分布式数据并行（DDP）在所有 GPU 间共享参数。采样区间严格不跨越 tile 边界，确保每个 GPU 仅查询其负责空间区域内的样本颜色和密度。

**前向全局汇集**。各 GPU 查询其 tile 内样本的颜色和密度后，通过 broadcast 操作将所有 GPU 的局部结果汇总至每个 GPU，使每个 GPU 都能执行完整的全局体渲染并得到完全相同的损失值。通信仅发生在前向传播，反向传播无需梯度同步。

**分段体渲染与损失重构**。将体渲染方程、累积权重、深度和畸变损失重写为各段的独立积分与跨段的加权组合形式，利用并行 prefix scan 实现高效的全局合成。该模块将 GPU 间通信量从朴素采样级通信的 $O(K S^2)$ 降至 $O(S^2)$（其中 $K$ 为每射线样本数，$S$ 为 tile 数），实测通信成本降低超过 2 倍（Fig. 12）。

**反向局部梯度**。各 GPU 仅基于本地损失计算自己参数的梯度，无需跨 GPU 梯度通信，进一步降低分布式训练开销。

### 关键公式推导

NeRF-XL 的核心数学洞察是：体渲染、透过率、累积权重、深度乃至畸变损失均属于"可分解积分族"，可分解为各段独立积分与跨段加权组合。以下给出关键公式及其变量含义。

**基础体渲染方程**。沿光线从近端 $t_n$ 到远端 $t_f$ 的像素颜色为：

$$C(t_n \to t_f) = \int_{t_n}^{t_f} T(t_n \to t) \, \sigma(t) \, c(t) \, dt$$

其中 $\sigma(t)$ 为体积密度，$c(t)$ 为颜色，透过率 $T(t_n \to t)$ 定义为：

$$T(t_n \to t) = \exp\left(-\int_{t_n}^{t} \sigma(s) \, ds\right)$$

**畸变损失**（Mip-NeRF 360 提出）惩罚沿光线分布的多个密度峰：

$$\mathcal{L}_{dist}(t_n \to t_f) = \iint w(t_i) \, w(t_j) \, |t_i - t_j| \, dt_i \, dt_j$$

其中 $w(t) = T(t_n \to t) \, \sigma(t)$ 为体渲染权重。

**分段体渲染**。将整条光线 $[t_1, t_{N+1}]$ 划分为 $N$ 个不重叠段 $[t_k, t_{k+1}]$，每段对应一个 GPU 的 tile。体渲染可等价分解为：

$$C(t_1 \to t_{N+1}) = \sum_{k=1}^{N} T(t_1 \to t_k) \, C(t_k \to t_{k+1})$$

其中 $C(t_k \to t_{k+1})$ 是第 $k$ 段内的独立体渲染结果，$T(t_1 \to t_k)$ 是到达第 $k$ 段起点的累积透过率，满足：

$$T(t_1 \to t_k) = \prod_{i=1}^{k-1} T(t_i \to t_{i+1})$$

该分解将样本级全局组合转化为 tile 级汇总数据交换：每个 GPU 只需广播其段内积分结果，通信量从 $O(K S^2)$ 降至 $O(S^2)$。

**分段畸变损失**。畸变损失同样可分解为段内惩罚与跨段惩罚之和：

$$\mathcal{L}_{dist}(t_1 \to t_{N+1}) = 2 \sum_{k=1}^{N} T(t_1 \to t_k) \, S(t_1 \to t_k) + \sum_{k=1}^{N} T(t_1 \to t_k)^2 \, \mathcal{L}_{dist}(t_k \to t_{k+1})$$

其中跨段辅助项 $S$ 利用段内累积权重 $A$ 和深度 $D$ 计算跨段交互：

$$S(t_1 \to t_k) = D(t_k \to t_{k+1}) \, A(t_1 \to t_k) - A(t_k \to t_{k+1}) \, D(t_1 \to t_k)$$

累积权重 $A$ 同样满足分段组合性质：

$$A(t_1 \to t_{N+1}) = \sum_{k=1}^{N} T(t_1 \to t_k) \, A(t_k \to t_{k+1})$$

以上分解使分布式 NeRF 在训练和推理上数学等价于单 GPU 版本，既消除了独立训练方案的容量冗余与混合伪影，又极大降低了多 GPU 通信开销。

## 实验与关键发现

### 实验设置与数据集

实验覆盖六种不同采集方式的大规模场景，包括街道级捕获（University4、MatrixCity、Laguna Seca）、航拍捕获（Building、Mexico Beach）以及物体中心360°捕获（Garden），场景尺度和采集方式具有高度多样性（Table 1）。所有方法均在同一框架下重实现，使用相同的NeRF表示（Instant-NGP）、占用网格加速和畸变损失，训练迭代数统一为20K，每迭代总采样数保持一致，仅多GPU策略不同。对于Block-NeRF和Mega-NeRF基线，采用其默认的空间重叠配置（50%和15%），确保基线以最佳配置运行。

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2404_16221/figures/007_Table_1.jpg]]
*Table 1: Data Statistics. Our experiments are conducted on these captures from various sources, including street captures (University4, MatrixCity, Laguna Seca), aerial captures (Building, Mexico Beach) and an object-centric 360-degree capture (Garden). These data span a wide range of scales, enabling a comprehensive evaluation of the multi-GPU system. Pixc and Pixd are denoted for color pixels and depth pixels, respectively*

### 主实验结果

**定量对比（Figure 8）**：在Garden、Building、University4和MatrixCity四个场景上，NeRF-XL随着GPU数量增加在PSNR和渲染速度（Rays Per Second）上均实现近似线性提升。相比之下，基于独立训练的Block-NeRF和Mega-NeRF在增加GPU资源后PSNR保持不变甚至下降，渲染速度也无明显改善。这一对比直接验证了核心因果机制：独立训练方案中的容量冗余和混合伪影从根本上阻止了多GPU资源向重建质量的转化，而联合训练通过消除冗余和通信优化实现了有效的资源扩展。

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2404_16221/figures/009_Figure_8.jpg]]
*Figure 8: Quantitative Comparison. Prior works based on independent training fails to realize performance improvements with additional GPUs, while our method enjoys improved rendering quality and speed as more resources are added to training*

**定性对比（Figure 7）**：在所有类型数据上，NeRF-XL的渲染结果在细节保留和边界清晰度上均优于独立训练基线。独立训练方法在GPU数量增加时并未带来可视化质量的提升，这与定量结果一致。

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2404_16221/figures/008_Figure_7.jpg]]
*Figure 7: Qualitative Comparison. Comparing to prior works, our method efficiently harnesses multi-GPU setups for performance improvement on all types of data*

**可扩展性验证（Figure 9）**：从1×到8× GPU的渲染质量逐步提升，更多GPU带来更多可学习参数，模型容量随之增长，可视化细节逐步增强。这表明NeRF-XL的参数分布式策略能够有效突破单GPU显存限制，实现模型容量的水平扩展。

### 消融实验

**分段式体渲染的通信效率（Figure 12）**：在University4场景上，分段式体渲染（tile-based communication）相比朴素采样级通信（sample-based communication）将多GPU数据交换量降低超过2倍，验证了体渲染方程重写为分段积分形式的有效性。然而，多GPU通信仍是系统主要瓶颈，尤其在负载不均衡时更为明显。

**模型容量扩展 vs. 光线并行（Figure 11）**：在University4上使用N个GPU时，NeRF-XL获得N倍模型参数，而PyTorch DDP仅通过N倍光线并行加速训练。NeRF-XL在PSNR上远优于DDP，表明大场景NeRF更受益于增加模型容量而非增多光线。这一发现揭示了当前多GPU NeRF方法的根本误区：单纯的光线并行无法解决大场景对高容量表示的需求。

### 失败模式与局限性

1. **通信开销仍是瓶颈**：尽管分段式体渲染大幅降低了通信量，多GPU同步和通信开销导致联合训练速度比独立训练慢约1–1.5倍。在负载不均衡时，GPU等待时间进一步加剧效率损失。

2. **空间划分依赖SfM点云**：当前空间划分算法依赖SfM稀疏点云或训练射线采样点估计场景内容分布。对于缺乏可靠点云的场景或自由轨迹采集，划分可能次优，导致GPU负载不均衡。

3. **表示通用性未验证**：当前实现仅基于Instant-NGP表示（hash grid + MLP），尚未验证该方法在其他NeRF表示（如Mip-NeRF 360、Triplane、TensoRF）上的通用性，也未扩展到动态场景或非静态任务。

4. **GPU数量限制**：空间划分生成2的幂次个tile，限制了GPU数量的灵活选择，且在大规模异构集群或带宽受限环境下的适用性尚未探索。

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2404_16221/figures/001_Figure_1.jpg]]
*Figure 1: Our principled multi-GPU distributed training algorithm enables scaling up NeRFs to arbitrarily-large scale*

## 定位与知识库关联

### 1. 多GPU NeRF方法的演进脉络

NeRF-XL 处于大规模场景神经渲染与分布式训练的交汇点。在多GPU NeRF方法的谱系中，此前的工作可划分为两条主线：

**独立训练范式**：以 **Block-NeRF**（Tancik et al., 2022）和 **Mega-NeRF**（Turki et al., CVPR 2022）为代表。这类方法将场景在空间上划分为多个重叠区域，每个GPU独立训练一个NeRF，渲染时通过2D混合（Block-NeRF）或3D混合（Mega-NeRF）合成最终图像。其核心假设是各区域可独立建模，但这一假设带来了三重代价：其一，每个独立NeRF被迫同时建模焦点区域与周围背景，造成严重的容量冗余——Mega-NeRF在University4上使用2/4/8个tile时，分别有38%/56%/62%的采样点落在指定tile区域之外；其二，2D/3D混合引入模糊和伪影，尤其当各NeRF独立优化相机或外观嵌入时，跨区域不一致性会进一步恶化混合质量；其三，增加GPU资源无法转化为重建质量的提升，PSNR和渲染速度均趋于饱和甚至下降。

**光线并行范式**：以PyTorch Distributed Data Parallel（DDP）为代表，将光线分发到不同GPU并行计算，所有GPU共享同一份模型参数。此范式受限于单GPU显存容量，无法扩展模型参数规模，对大场景的建模能力存在天然上限。

NeRF-XL 在谱系中的定位是**联合训练范式**的开创者：它将空间划分为不重叠的tile，每个GPU负责一个tile，但通过前向传播中的全局信息汇集实现数学上等价于单GPU的体渲染，从而同时消除了独立训练的容量冗余与混合伪影，又突破了光线并行的模型容量瓶颈。

### 2. 核心设计决策与因果机制

NeRF-XL 的关键设计决策可归纳为三个层次：

**空间划分策略**：基于SfM稀疏点云或训练射线采样点构建3D点分布，沿各轴计算CDF，递归二分选择CDF=0.5且划分后子区域长宽比最接近1的平面。这一策略以“各tile内空间内容量近似相等”为目标，尽可能均衡GPU计算负载，是后续联合训练得以高效运行的基础。

**分段体渲染的数学重构**：这是方法的核心洞察。体渲染积分、透过率、累积权重、深度乃至畸变损失均属于“可分解积分族”——整条光线的渲染结果可分解为各段的独立积分与跨段的加权组合。具体而言：
- 分段体渲染：$C(t_1 \to t_{N+1}) = \sum_{k=1}^N T(t_1 \to t_k) C(t_k \to t_{k+1})$
- 分段透过率：$T(t_1 \to t_k) = \prod_{i=1}^{k-1} T(t_i \to t_{i+1})$
- 分段畸变损失：$\mathcal{L}_{dist}(t_1 \to t_{N+1}) = 2 \sum_{k=1}^N T(t_1 \to t_k) S(t_1 \to t_k) + \sum_{k=1}^N T(t_1 \to t_k)^2 \mathcal{L}_{dist}(t_k \to t_{k+1})$

基于此重构，GPU间仅需交换每段的汇总数据（颜色、透过率、累积权重、深度），而非逐采样点的原始值，通信量从$O(K S^2)$降至$O(S^2)$（$K$为每段采样数，$S$为段数/GPU数），实际通信成本降低超过2倍。

**前向汇集+反向局部梯度**：前向传播中，每GPU查询其tile内样本的颜色和密度，通过全局广播使所有GPU获得完整的体渲染结果和相同的损失值；反向传播中，各GPU仅计算自己参数的梯度，无需跨GPU梯度同步。这一设计使得训练过程的通信开销仅限于前向传播，且与模型参数规模解耦。

### 3. 适用边界与局限

**已验证的适用场景**：
- 大规模静态场景的新视角合成，涵盖街道级（University4、MatrixCity、Laguna Seca）、航拍（Building、Mexico Beach）和物体中心360度（Garden）等多种数据类型
- 基于Instant-NGP表示（hash grid + MLP）的NeRF架构
- 均匀GPU集群环境，GPU数量为2的幂次（2/4/8 GPU）

**已知局限**：
- **通信开销仍是瓶颈**：尽管分段体渲染大幅降低了通信量，多GPU同步仍是系统主要瓶颈，尤其在负载不均衡时更明显。联合训练相比独立训练存在额外同步开销，训练速度约慢1–1.5倍。
- **表示方法的单一性**：当前实现仅验证了Instant-NGP表示，尚未在Mip-NeRF 360、Triplane、TensoRF等其他NeRF表示上验证通用性，也未扩展到动态场景或非静态任务。
- **空间划分的依赖性**：划分质量依赖于SfM点云或训练射线采样，对缺乏可靠点云的场景（如弱纹理区域）或自由轨迹可能产生次优划分，导致负载不均衡进而影响效率。

### 4. 开放问题

1. **更优的空间划分算法**：如何设计自适应划分策略以进一步平衡各GPU的工作负载，减少通信等待时间？是否可以在训练过程中动态调整每个GPU负责的空间区域？

2. **表示方法的泛化**：该分布式框架能否无缝迁移到其他NeRF表示（如Mip-NeRF 360、3D Gaussian Splatting），以及拓展到动态场景合成或可变形模型？

3. **异构与大规模扩展**：如何将联合训练思想推广到异构GPU集群或带宽受限环境，实现城市级乃至国土级场景的分布式训练？是否需要层次化的通信拓扑？

4. **训练效率的进一步提升**：能否结合梯度压缩、异步通信或局部损失近似等技术，在保持数学等价性的前提下进一步降低通信开销？

## 原文 PDF

![[paperPDFs/ECCV_2024/NeRF_XL_Scaling_NeRFs_with_Multiple_GPUs.pdf]]
