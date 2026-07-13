---
title: "tttLRM: Test-Time Training for Long Context and Autoregressive 3D Reconstruction"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/tttLRM_Test_Time_Training_for_Long_Context_and_Autoregressive_3D_Reconstruction.pdf
project_link: https://cwchenwang.github.io/tttLRM
code_link: null
aliases:
- tttLRM
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 引入测试时训练（Test-Time Training）层作为核心构建块，利用快速权重（fast weights）在推理时动态更新并将多视图信息压缩为固定大小的隐式3D神经记忆；该过程仅具有线性计算复杂度，从根本上突破了长序列建模的效率瓶颈。
primary_logic: TTT 的快速权重天然充当跨视图的隐式3D表示，通过虚拟令牌（如虚拟相机平面或三平面特征）查询即可解码为 3DGS、NeRF 等多种显式3D格式，从而统一了高质量前馈重建与自回归流式重建，且保持线性复杂度。
claims:
- tttLRM 利用 TTT 层实现具有线性复杂度的长上下文、自回归3D重建。
- 快速权重将输入序列的键值对缓存编码为固定大小的神经记忆。
- 模型可无缝扩展到 1024×1024 分辨率，而 GS-LRM 在高分辨率下出现内存不足。
- 在场景级重建中，相较 Long-LRM 获得约 1 dB PSNR 提升，且单个模型即可适配不同视图数。
---

# tttLRM: Test-Time Training for Long Context and Autoregressive 3D Reconstruction

> [!tip] 核心洞察
> TTT 的快速权重天然充当跨视图的隐式3D表示，通过虚拟令牌（如虚拟相机平面或三平面特征）查询即可解码为 3DGS、NeRF 等多种显式3D格式，从而统一了高质量前馈重建与自回归流式重建，且保持线性复杂度。

| 字段 | 内容 |
|------|------|
| 中文题名 | tttLRM：基于测试时训练的长上下文自回归3D重建 |
| 英文题名 | tttLRM: Test-Time Training for Long Context and Autoregressive 3D Reconstruction |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2602.20160) · [Project](https://cwchenwang.github.io/tttLRM) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | tttLRM |
| Dataset | GSO, DL3DV-140, Tanks&Temples |

> [!tip] 效果简介
> - GSO (Object-level, 512×512) 上，PSNR 34.02 vs 32.83 (GS-LRM) (+1.19)。
> - DL3DV-140 (Scene-level, 32 views) 上，PSNR 25.07 vs 24.10 (Long-LRM 32v model) (+0.97)。
> - Tanks&Temples (32 views) 上，PSNR 19.22 vs 18.38 (Long-LRM 32v model) (+0.84)。

## 概要

### 问题与瓶颈

3D重建领域长期面临一个根本性效率困境：基于前馈网络的快速重建模型——如 **GS-LRM**（Zhang et al., ECCV 2024）和 **Long-LRM**（Chen et al., ICCV 2025）——依赖自注意力机制聚合多视图信息，其计算复杂度随输入视图数呈平方增长，难以扩展至超过32个视图的高分辨率场景，更无法支持自回归式的流式输入序列处理；而逐场景优化方法（如 **3DGS**（Kerbl et al., ACM TOG 2023）、**Mip-Splatting**（Yu et al., CVPR 2024）、**Scaffold-GS**（Lu et al., CVPR 2024））虽能获得较高重建质量，但每个场景需耗费数分钟至数小时的优化时间，无法满足实时应用需求。如何在保持线性计算复杂度的同时，实现高质量、长上下文且支持流式输入的前馈3D重建，是该领域的核心瓶颈。

### 核心方法

tttLRM 提出了一个统一的解决方案：将测试时训练（Test-Time Training, TTT）引入3D重建框架。其核心操作单元为 LaCT（Large Chunk Test-Time Training）块，通过在推理时动态更新一组快速权重（fast weights），将任意长度的输入视图序列压缩为固定大小的隐式3D神经记忆。这一过程的计算复杂度与序列长度呈线性关系，从根本上突破了注意力机制的平方复杂度瓶颈。快速权重天然充当跨视图的隐式3D表示，通过引入虚拟令牌（如虚拟相机平面或可学习的三平面特征）作为查询，即可解码为 3DGS、三平面 NeRF 等多种显式3D格式，实现了前馈重建与自回归流式重建的统一。

### 关键结果

在对象级重建基准 GSO 上，tttLRM 以8视图、512×512分辨率取得 34.02 PSNR，较 GS-LRM 提升 1.19 dB，且能无缝扩展至 1024×1024 分辨率（GS-LRM 在该分辨率下出现内存不足）。在场景级重建中，tttLRM 以单一模型适配不同视图数：DL3DV-140 数据集上32视图取得 25.07 PSNR（较 Long-LRM 提升 0.97 dB），64视图取得 25.95 PSNR（提升 1.32 dB）；Tanks&Temples 上32视图取得 19.22 PSNR（提升 0.84 dB）。消融实验进一步表明，TTT-LVSM 预训练初始化可显著加速收敛并提升最终质量，自回归全重建策略优于“预测-合并”策略（避免累积误差），Muon 优化器配合透明度和深度正则化可达到最佳性能。

### 方法谱系与知识库定位

tttLRM 处于前馈3D重建与序列建模方法的交叉点。它继承了 GS-LRM 和 Long-LRM 的前馈重建范式，但用 LaCT 块替换了其中的自注意力机制，从而将复杂度从 $O(N^2 d)$ 降至 $O(N d^2)$。其快速权重机制源自 TTT 系列工作，但首次被重新解释为隐式3D表示，并通过虚拟令牌查询实现了与多种显式3D格式的解码对接。这一设计使得 tttLRM 既能作为高质量前馈重建器，又能以因果顺序更新快速权重的方式支持自回归流式输入，填补了前馈方法与逐场景优化方法之间的效率-质量鸿沟。

### 3D重建的两条路径及其根本矛盾

从多视图图像恢复三维结构是计算机视觉的核心问题。当前主流方案可归为两条技术路线：**逐场景优化**与**前馈推理**。

逐场景优化方法以 **3D Gaussian Splatting（3DGS）**（Kerbl et al., ACM TOG 2023）及其改进版本 **Mip-Splatting**（Yu et al., CVPR 2024）、**Scaffold-GS**（Lu et al., CVPR 2024）为代表，通过对单个场景反复迭代优化高斯参数，能够生成高保真度的新视角渲染。然而，这类方法通常需要数十分钟的优化时间，无法满足实时应用的需求。

前馈推理方法则试图用一个统一模型直接从输入图像预测3D表示，无需逐场景迭代。代表性工作如 **GS-LRM**（Zhang et al., ECCV 2024）和 **Long-LRM**（Chen et al., ICCV 2025），它们基于 Transformer 架构，利用注意力机制聚合多视图信息，在推理速度上具有显著优势。但这些方法面临一个根本性的效率瓶颈：**注意力机制的计算复杂度随输入视图数呈平方增长**。

### 注意力瓶颈的具体表现

这一瓶颈带来了三重限制：

1. **视图数量受限**：由于计算开销随序列长度平方级膨胀，现有前馈模型难以扩展到超过 32 个输入视图。在需要密集覆盖的场景级重建任务中，这直接限制了重建质量的上限。

2. **分辨率扩展困难**：当输入分辨率提升至 1024×1024 时，GS-LRM 会因内存不足而无法训练，而 tttLRM 则可无缝扩展到该分辨率。这意味着注意力机制的显存占用严重制约了高分辨率场景下的应用。

3. **自回归推理缺失**：注意力机制要求一次性输入所有视图，无法支持流式、逐步到来的输入序列。在实际应用中——如机器人导航、AR/VR 场景构建——相机是连续移动的，模型需要能够以自回归方式逐步接收新视图并实时更新场景表示，而现有前馈方法完全不具备这一能力。

### 线性复杂度序列建模的探索与不足

为突破平方复杂度限制，研究者尝试将 Mamba 等线性复杂度序列模型引入3D重建。Mamba 通过状态空间模型实现线性计算复杂度，理论上可支持更长的序列。然而，实验表明其长程建模能力显著弱于注意力机制，在重建质量上存在明显差距。这意味着，**单纯追求线性复杂度而牺牲建模能力，并非可行的替代方案**。

### 核心动机：在保持建模能力的同时实现线性复杂度

上述分析揭示了一个清晰的方法缺口：能否设计一种机制，既保持注意力级别的长程建模能力，又将计算复杂度从平方降至线性？tttLRM 的核心动机正是填补这一缺口。其关键洞察在于：**测试时训练（Test-Time Training, TTT）中的快速权重天然适合充当跨视图的隐式3D表示**——它们在推理时通过梯度更新动态吸收输入信息，将变长的多视图序列压缩为固定大小的神经记忆，而这一过程的计算复杂度仅为线性。

这一设计不仅解决了长序列建模的效率问题，还意外地统一了前馈重建与自回归流式重建两种范式：快速权重可按照因果顺序逐步更新，使得模型能够像 RNN 一样处理流式输入，而无需改变核心架构。

## 核心方法与创新机理

tttLRM 的核心创新在于将**测试时训练**范式引入前馈3D重建框架，从根本上重构了多视图信息聚合的计算机制。与现有方法依赖注意力机制（二次复杂度）或状态空间模型（线性但长程建模能力弱）不同，tttLRM 通过以下关键槽位替换实现了线性复杂度下的高质量长序列建模。

### 从注意力到 LaCT 块：线性复杂度的序列建模

现有前馈重建模型的核心瓶颈在于序列建模层的计算复杂度。**GS-LRM**（Zhang et al., ECCV 2024）采用双向自注意力，计算量随输入视图数呈平方增长，难以扩展到超过32个视图，且在高分辨率（如 1024×1024）下出现显存溢出。**Long-LRM**（Chen et al., ICCV 2025）虽针对场景级长序列设计，但仍依赖双向注意力，且需为不同视图数分别训练独立模型。

tttLRM 将序列建模层替换为 **LaCT（Large Chunk Test-Time Training）块**。其核心机制如下：输入图像经分块和线性映射后形成令牌序列，令牌在通过每个 LaCT 块时，首先经过窗口注意力模块捕获视图内局部空间关系，随后以当前令牌批次为训练数据，通过 Muon 优化器以梯度下降更新该块的快速权重 $W$：

$$W = \mathrm{Update}(\{ \mathbf{T}_i \}_{i=1}^{N})$$

这一更新过程将输入序列的键值对缓存压缩为**固定大小的隐式神经记忆**，计算复杂度与序列长度呈线性关系。更新后的快速权重随即应用于令牌，完成信息的前向传播。整个更新与应用过程均为线性复杂度，从根本上突破了长序列建模的效率瓶颈。

### 快速权重作为隐式3D表示

tttLRM 的第二个关键创新在于对快速权重的语义重解释。现有方法缺乏专门的隐式3D表示，仅依赖显式的令牌缓存或特征图进行解码。tttLRM 将 TTT 层的快速权重直接解释为**隐式潜在空间中的3D表示**——多视图观测信息被压缩进固定容量的神经记忆中，形成场景的隐式编码。

为从该隐式记忆中提取信息，tttLRM 引入**虚拟令牌查询机制**。在 3DGS 重建中，虚拟令牌对应虚拟相机视图；在三平面 NeRF 重建中，虚拟令牌为可学习的三平面特征。虚拟令牌不参与快速权重的更新，仅作为查询向量：

$$\mathbf{T}_i^{\mathrm{v}} = \mathrm{Apply}(W, \mathbf{T}_i^{\mathrm{v}})$$

查询后的虚拟令牌经线性解码器映射为显式3D参数（如逐像素的高斯属性或三平面特征）。这一设计使得同一套快速权重可被不同查询方式解码为 **3DGS、NeRF 等多种显式3D格式**，实现了表示层面的统一。

### 因果更新与自回归流式重建

传统前馈方法要求一次性输入所有视图，无法支持流式场景。tttLRM 通过修改快速权重的更新与应用步骤，引入**因果依赖关系**：对于每个新到达的视图批次，模型以增量方式更新快速权重并立即预测对应的 3D 高斯，将模型转化为类 RNN 的推理过程。这一设计使 tttLRM 天然支持自回归、流式输入序列的处理，且保持线性复杂度。

### 创新点的协同效应

上述三个槽位替换并非孤立改进，而是形成协同效应：LaCT 块的线性复杂度使长序列处理成为可能，快速权重的隐式记忆特性为多视图信息提供了紧凑的融合载体，虚拟令牌查询则解耦了信息存储与任务解码。三者共同支撑了 tttLRM 的核心能力——在单个模型中统一高分辨率前馈重建、长上下文场景重建与自回归流式重建，且全程保持线性计算复杂度。

tttLRM 的核心设计将测试时训练（Test-Time Training, TTT）快速权重作为跨视图的隐式 3D 神经记忆，并围绕这一机制构建了线性复杂度的前馈重建管线。整个框架由五个紧密耦合的模块串联而成，数据流从原始图像输入到显式 3D 表示输出，全程保持计算效率与表示灵活性。

### 1. 图像标记化与射线嵌入

输入为一组带有相机位姿的视图 $\{\mathbf{I}_i\}_{i=1}^{N}$。首先，将每张图像与其对应的射线嵌入（ray embeddings）沿通道维度拼接，随后进行分块处理（patchify），并通过一个轻量线性层将图像块映射为令牌序列 $\{\mathbf{T}_{i,j}\}$。这一步骤将几何先验（射线方向、原点）注入视觉特征，为后续的跨视图信息压缩奠定基础。

### 2. 窗口注意力模块

在每个 LaCT 块内部，首先对令牌施加窗口注意力（window attention），捕获单个视图内的局部空间关系：

$$\mathbf{T}_i = \mathbf{T}_i + \mathrm{WinAttn}(\mathbf{T}_i)$$

该模块仅作用于各视图内部的令牌，不引入跨视图交互，其作用是为后续的快速权重更新提供更丰富的局部特征表达。

### 3. LaCT 块：快速权重的更新与应用

这是 tttLRM 的核心计算单元，由两个关键操作构成——更新（update）与应用（apply），两者均具有线性计算复杂度。

**更新阶段**：视觉令牌被送入 LaCT 块，通过 Muon 优化器迭代更新快速权重 $W$，将序列信息压缩为固定大小的隐式神经记忆。更新规则遵循 TTT 的标准范式：

$$W = W - \eta \nabla \mathcal{L}_{\mathrm{MSE}}(f_W(k), v)$$

其中 $k, v$ 为令牌的键值对。LaCT 的关键创新在于支持大块更新（chunk size 可达百万级令牌），使得长序列的快速权重学习在计算上可行。从功能上看，快速权重相当于将输入序列的键值缓存（KV cache）编码为固定大小的神经记忆，这是突破注意力机制二次复杂度瓶颈的根本原因。

**应用阶段**：更新后的快速权重被应用于令牌，完成特征增强。更新与应用操作均保持与序列长度的线性复杂度关系。

### 4. 虚拟令牌查询

为从快速权重中提取下游任务所需的信息，tttLRM 引入一组虚拟令牌（virtual tokens）作为查询。这些令牌不参与快速权重的更新，仅执行应用操作：

$$\mathbf{T}_i^{\mathrm{v}} = \mathrm{Apply}(W, \mathbf{T}_i^{\mathrm{v}})$$

虚拟令牌的具体形式取决于目标 3D 表示：在 3DGS 重建中，它们对应虚拟相机视点；在三平面 NeRF 重建中，它们则是可学习的三平面特征令牌。这种设计将隐式 3D 记忆的解码与目标表示格式解耦，赋予框架高度的表示灵活性。

### 5. 线性解码器与 3D 表示生成

查询后的虚拟令牌通过线性解码器映射为显式 3D 参数。对于 3DGS，解码器输出每个图像块对应的高斯属性（颜色、不透明度、缩放、旋转、位置）；对于三平面 NeRF，则输出三平面特征。整个解码过程仅涉及线性变换，计算开销极低。

### 自回归流式推理

在自回归模式下，上述管线以因果顺序处理流式输入的视图批次。如 Algorithm 1 所示，对于每个到达的视图小批次 $\mathbf{T}_{(b)}$（例如每次 4 张图像），模型先更新快速权重，再立即预测对应的 3D 高斯，随后将预测结果合并到全局场景中。这一过程将模型转化为类似 RNN 的增量推理模式，无需一次性输入所有视图。论文还引入了一种无需训练的历史选择性更新策略，利用历史快速权重进一步改善自回归模型的重建质量。

### 分布式训练与推理

为支持大规模场景训练，tttLRM 采用序列并行策略：将标记化后的输入视图沿序列维度切分到多个 GPU，各设备独立更新快速权重后同步，再各自预测所分配虚拟视图的高斯参数，最后收集构建完整场景并分别渲染新视角计算损失、聚合梯度。这一设计使模型可以线性加速，训练时使用了 64 块 A100 GPU。

### 测试时训练（TTT）快速权重更新

tttLRM 的核心构建块是测试时训练层，其关键机制是在推理时动态更新一组快速权重 $W$。给定输入序列的键值对 $(k, v)$，快速权重通过最小化均方误差进行在线梯度更新：

$$W = W - \eta \nabla \mathcal{L}_{\mathrm{MSE}}(f_W(k), v)$$

其中 $\eta$ 为学习率，$f_W(\cdot)$ 表示以 $W$ 为参数的模型函数。这一更新过程将输入序列的键值缓存（KV cache）压缩为固定大小的神经记忆，且计算复杂度与序列长度呈线性关系。与标准 TTT 不同，tttLRM 采用大块测试时训练（LaCT）策略，支持高达百万级令牌的大块更新，从而在保持线性复杂度的同时实现强大的长程建模能力。

### 图像标记化与射线嵌入

给定一组带有相机位姿的输入图像 $\{\mathbf{I}_i\}_{i=1}^N$，模型首先将每张图像与其对应的射线位置嵌入（ray embedding）按通道拼接，然后划分为大小为 $p \times p$ 的图像块，最后通过一个轻量线性层映射为令牌序列：

$$\{ \mathbf{T}_{i,j} \}_{i=1, j=1}^{N, HW/p^2} = \mathrm{Tokenize}\big( \mathrm{Patchify}( [\{ \mathbf{I}_i \}_{i=1}^N, \mathrm{RayEmb} ]) \big)$$

其中 $H$、$W$ 分别为图像高度和宽度，$N$ 为输入视图数。射线嵌入为每个图像块提供空间位置先验，辅助模型建立跨视图的几何对应关系。

### LaCT 块：窗口注意力与快速权重应用

每个 LaCT 块内部包含一个窗口注意力模块（window attention），用于在单视图内捕获局部空间关系：

$$\mathbf{T}_i = \mathbf{T}_i + \mathrm{WinAttn}(\mathbf{T}_i)$$

经过窗口注意力增强后的令牌随后用于更新 LaCT 块中的快速权重 $W$，整个更新过程采用 Muon 优化器实现。更新完成后，另一组虚拟令牌（virtual tokens）$\mathbf{T}_i^{\mathrm{v}}$ 作为查询，在不进一步修改权重的前提下从快速权重中提取信息：

$$\mathbf{T}_i^{\mathrm{v}} = \mathrm{Apply}(W, \mathbf{T}_i^{\mathrm{v}})$$

在 3DGS 重建中，这些虚拟令牌对应于虚拟相机视图；在三平面 NeRF 等其他 3D 表示中，它们可以是可学习的三平面特征令牌。

### 训练损失函数

模型训练采用组合损失函数。RGB 渲染损失结合了像素级 MSE 和基于 VGG-19 的感知损失：

$$\mathcal{L}_{\mathrm{RGB}} = \mathrm{MSE}(\mathbf{I}_{\mathrm{pred}}, \mathbf{I}_{\mathrm{gt}}) + \lambda \mathrm{Perceptual}(\mathbf{I}_{\mathrm{pred}}, \mathbf{I}_{\mathrm{gt}})$$

最终训练目标进一步引入深度正则化项 $\mathcal{L}_{\mathrm{depth}}$ 和透明度正则化项 $\mathcal{L}_{\mathrm{opacity}}$：

$$\mathcal{L} = \mathcal{L}_{\mathrm{RGB}} + \lambda_{\mathrm{depth}} \mathcal{L}_{\mathrm{depth}} + \lambda_{\mathrm{opacity}} \mathcal{L}_{\mathrm{opacity}}$$

消融实验表明，同时采用 Muon 优化器并加入深度和透明度正则化可达到最佳 PSNR，并有效减少冗余的不透明高斯数量（Table 5）。

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2602_20160/figures/005_Figure_6.jpg]]
*Figure 6: We show that tttLRM, as a general framework, can also interpret the latent 3D memory into formats besides 3DGS. In this experiment, we use a set of triplane tokens to query the fast weights and then fine-tune the model for triplane-based NeRF reconstruction. We visualize the resulting triplanes and present the corresponding renderings and depth maps for 4 views at a resolution of 512 × 512*

## 实验与关键发现

tttLRM 在对象级、场景级、高分辨率单图到3D以及自回归流式重建等多个维度上进行了系统验证，实验覆盖了从定量指标到定性可视化、从消融分析到效率对比的完整链路。以下按任务类型与关键发现分层展开。

### 对象级前馈重建

在 GSO 数据集上，tttLRM 与基于注意力的前馈基线 **GS-LRM**（Zhang et al., ECCV 2024）进行了系统对比（Table 1）。在 512×512 分辨率、8 个输入视图的设置下，tttLRM 取得 34.02 dB PSNR，较 GS-LRM 的 32.83 dB 提升约 1.19 dB，同时推理速度约为其两倍。当分辨率提升至 1024×1024 时，GS-LRM 出现显存溢出而无法训练，tttLRM 则凭借线性计算复杂度无缝扩展，保持了高保真重建能力（PSNR 33.14）。这一结果直接验证了核心主张：TTT 层从根本上解决了注意力机制在长序列高分辨率输入下的平方复杂度瓶颈。

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2602_20160/figures/006_Table_1.jpg]]
*Table 1: Comparison between our method and GS-LRM [68] on the GSO dataset under different resolutions and numbers of input views. Our method consistently outperforms GS-LRM in both inference speed and reconstruction quality, and also shows strong generalization ability. V. denotes the number of virtual views used to query the fast weight, which equals input views unless noted*

值得注意的是，tttLRM 在仅使用 4 个虚拟视图查询快速权重的条件下（V=4），PSNR 仍达 33.14，与使用全部 8 个虚拟视图（V=8）的 34.02 相比仅略有下降，表明快速权重所编码的隐式 3D 记忆具有高度信息密度，少量查询即可恢复场景结构。

### 场景级长序列重建

在更具挑战性的场景级任务上，tttLRM 在 DL3DV-140 和 Tanks&Temples 两个数据集上与 **Long-LRM**（Chen et al., ICCV 2025）以及多个逐场景优化方法（**3DGS**、**Mip-Splatting**、**Scaffold-GS**）进行了对比（Table 2、Table 7）。

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2602_20160/figures/007_Table_2.jpg]]
*Table 2: Quantitative comparison on both DL3DV-140 and Tanks&Temples datasets under different numbers of input views. Our method surpasses previous feedforward methods and is comparable with optimization-based methods. Note that Long-LRM trains a separate model for each input view, while we are a single model across all input views. Our model can be linearly accelerated with multiple GPUs, here we report time on 1 A100*

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2602_20160/figures/014_Table_7.jpg]]
*Table 7: More quantitative comparison on both DL3DV-140 and Tanks&Temples datasets under 32/64 input views. Our method surpasses previous feedforward methods and can further surpass optimization-based methods with a few steps post-optimization. Note that Long-LRM trains a separate model for each input view, while we are a single model across all input views. Our model can be linearly accelerated with multiple GPUs, here we report time on a single Nvidia A100 80GB GPU*

核心发现如下：
- **单一模型跨视图数泛化**：Long-LRM 需为每个视图数（32、64）单独训练一个模型，而 tttLRM 以单一模型适配所有视图数设置。在 DL3DV-140 上，32 视图下 tttLRM 取得 25.07 dB PSNR，较 Long-LRM 的 24.10 dB 提升约 0.97 dB；64 视图下进一步拉开差距，达到 25.95 dB vs 24.63 dB（提升 1.32 dB）。在 Tanks&Temples 上同样呈现一致优势（32 视图：19.22 vs 18.38）。
- **与优化方法的竞争力**：尽管 tttLRM 是纯前馈模型，其重建质量已接近甚至部分超过逐场景优化方法。在 DL3DV-140 的 64 视图设置下，tttLRM 的 25.95 dB 已超过 3DGS 的 25.39 dB。若辅以 3 步或 10 步后优化，tttLRM 可进一步超越 Mip-Splatting 和 Scaffold-GS 等强优化基线（Table 7）。
- **线性加速特性**：受益于序列并行设计，tttLRM 可通过多 GPU 分布式推理实现线性加速，单张 A100 上的推理时间已具备实用价值。

定性可视化（Figure 4）进一步印证了定量结论：tttLRM 在几何细节、纹理保真度和边缘锐度上均优于 Long-LRM 及优化基线，尤其在高频区域（如建筑立面纹理、植物细节）的优势更为显著。

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2602_20160/figures/004_Figure_4.jpg]]
*Figure 4: Qualitative comparison between our method and baseline approaches. Our model reconstructs the 3DGS scene with higher fidelity than both optimization-based and feedforward baselines, as also reflected in the PSNR metrics. Please zoom in for a better comparison*

### 高分辨率单图到3D生成

tttLRM 的 1024×1024 高分辨率模型与多视图生成器结合后，展示了从单张图像生成高质量 3D 内容的能力（Figure 5）。模型能够恢复毛发、皮毛纹理、文字等细粒度真实感细节。这一能力建立在 TTT 层对高分辨率长序列令牌的高效处理之上——注意力基线在同等分辨率下已无法完成训练。

### 自回归流式重建

tttLRM 支持因果顺序的流式输入，在自回归模式下逐步接收视图并实时更新快速权重，即时预测对应区域的 3D 高斯。消融实验（Table 4）对比了两种自回归策略：
- **全重建（Ours）**：每步对当前累积的所有视图进行完整 3DGS 重建，PSNR 达 23.63 dB。
- **预测-合并（Predict & Merge）**：每步仅预测新视图对应的高斯并将其与历史高斯合并，PSNR 仅 21.50 dB。

后者因累积误差导致质量显著下降，表明在自回归场景下，利用快速权重对全局信息进行重整合是维持重建质量的关键。

进一步的训练无关选择性更新策略（Table 6）通过考虑历史快速权重状态，将自回归模型的 PSNR 从 24.81 dB 提升至 24.95 dB，SSIM 从 0.814 提升至 0.818，验证了记忆保持机制对流式场景的价值。

### 消融实验

#### 预训练的作用

Table 3 和 Figure 7 系统验证了 TTT-LVSM 预训练初始化的贡献。在 3DGS 重建任务上，带预训练的模型达到 33.14 dB PSNR，而从头训练仅 32.77 dB；在三平面 NeRF 重建上，差距更为显著（27.87 vs 26.40）。训练曲线（Figure 7）显示，预训练模型在早期训练阶段即迅速收敛至较高 PSNR，收敛速度与最终性能均显著优于从头训练。这一发现表明，TTT 层在新视角合成任务上习得的隐式 3D 先验可有效迁移至显式 3D 重建。

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2602_20160/figures/010_Table_3.jpg]]
*Table 3: Leveraging pretrained knowledge from novel view synthesis tasks improves the final 3D reconstruction quality across different 3D representations*

#### 优化器与正则化

Table 5 在场景级 32 视图 256×144 输入设置下消融了优化器选择和正则化项的影响：
- 基线（AdamW + 基础损失）PSNR 为 20.44 dB。
- 切换至 Muon 优化器后提升至 20.68 dB。
- 进一步加入透明度正则化与深度正则化（Muon + Opacity + Depth）达到最佳 20.76 dB，同时有效减少了不透明高斯的冗余数量。

这一组合被采纳为最终配置，在提升重建质量的同时改善了 3D 表示的紧凑性。

#### 效率分析

Figure 8 对比了 3 层注意力与 24 层 LaCT 块在不同令牌数量下的推理时间。随着令牌数增加，注意力的平方复杂度导致耗时急剧上升，而 LaCT 的线性复杂度使其在长序列场景下保持显著效率优势。这从计算层面解释了 tttLRM 能够处理 1024×1024 高分辨率输入和 64 视图长序列的根本原因。

### 跨表示泛化

tttLRM 的快速权重作为通用隐式 3D 记忆，不仅限于解码为 3DGS。通过将虚拟令牌替换为可学习的三平面令牌，同一架构可微调后用于三平面 NeRF 重建（Figure 6、Table 3）。在三平面设置下，带预训练的模型达到 27.87 dB PSNR，展示了框架的表示无关性。这一特性使 tttLRM 有潜力成为统一的 3D 重建骨干，适配多种显式表示格式。

### 失败模式与局限性

尽管整体表现优异，tttLRM 仍存在若干已知局限：
- **记忆容量固定**：快速权重的参数量决定了隐式记忆的上限。在处理极复杂场景或超长序列（如数百张视图）时，早期信息可能被逐步覆盖遗忘，导致远端区域的渲染质量下降。这是 TTT 层固定容量设计的固有约束。
- **自回归权重漂移**：流式推理中，快速权重随新视图持续更新，缺乏对历史状态的显式约束。当前依赖训练无关的选择性更新策略缓解此问题，但将其集成到训练过程中有望获得更优的权重稳定性。
- **训练资源需求高**：模型训练使用了 64 块 A100 GPU，在资源受限环境中复现存在门槛。论文未提供小规模配置下的性能参考。
- **公平性与鲁棒性未评估**：论文未讨论模型在不同光照条件、场景复杂度或数据分布偏移下的表现差异，极端条件下的鲁棒性仍是开放问题。

### 待验证与开放问题

以下结论基于论文证据可确认，但部分边界情况需读者结合自身场景评估：
- 快速权重作为隐式 3D 记忆的解释在 3DGS 和三平面 NeRF 两种表示上均得到验证，但在其他表示（如 SDF、占用场）上的泛化性尚未实验。
- 自回归选择性更新的增益（+0.14 dB PSNR）幅度有限，训练时集成该策略的潜在收益需进一步探索。
- 实时流式重建（<1 秒延迟）虽在架构上具备线性复杂度基础，但当前推理时间距离严格实时仍有差距，工程优化空间较大。

## 定位与知识库关联

### 1. 与基线方法的关系

tttLRM 的核心技术路径是通过**测试时训练（Test-Time Training）** 替代传统注意力机制，从而在 3D 重建任务中实现线性计算复杂度。这一选择使其与前馈重建基线形成明确的功能边界与性能差异。

**相比 GS-LRM（Zhang et al., ECCV 2024）**：GS-LRM 是典型的对象级前馈 3DGS 重建方法，依赖自注意力机制处理输入视图序列。其计算复杂度随输入视图数呈平方增长，导致两个关键瓶颈：一是在高分辨率（如 1024×1024）下出现内存不足而无法训练；二是推理速度随视图数增加急剧下降。tttLRM 将序列建模层从双向自注意力替换为 LaCT 块（大块测试时训练），通过快速权重更新将多视图信息压缩为固定大小的隐式神经记忆，更新与应用操作均为线性复杂度。在 GSO 数据集 512×512 分辨率 8 视图设定下，tttLRM 的 PSNR 达到 34.02，相较 GS-LRM 的 32.83 提升 1.19 dB，且推理速度约为注意力模型的两倍（Table 1）。更重要的是，tttLRM 可无缝扩展到 1024×1024 分辨率，而 GS-LRM 在此设定下因内存不足无法训练——这是 LaCT 线性复杂度带来的根本性能力突破。

**相比 Long-LRM（Chen et al., ICCV 2025）**：Long-LRM 是场景级长序列 3DGS 重建基线，同样采用注意力机制（双向注意力）处理多达 64 个输入视图。其关键局限在于：不同视图数需训练独立模型，无法以单一模型适配可变长度输入。tttLRM 以单一模型跨所有视图数设定，在 DL3DV-140 数据集 32 视图下 PSNR 达 25.07，相较 Long-LRM 的 24.10（32 视图专用模型）提升约 1 dB；在 64 视图下 PSNR 达 25.95，相较 Long-LRM 的 24.63（64 视图专用模型）提升 1.32 dB（Table 2）。在 Tanks&Temples 数据集上，32 视图设定下 tttLRM 的 PSNR 为 19.22，Long-LRM 为 18.38，提升 0.84 dB。值得注意的是，即使 Long-LRM 结合额外的后优化步骤（post-optimization），tttLRM 仍持续优于该增强基线（Table 7），表明快速权重所编码的隐式 3D 表示本身具有更高的初始质量。

**相比逐场景优化方法（3DGS、Mip-Splatting、Scaffold-GS）**：以 **3DGS**（Kerbl et al., ACM TOG 2023）、**Mip-Splatting**（Yu et al., CVPR 2024）和 **Scaffold-GS**（Lu et al., CVPR 2024）为代表的优化方法通过逐场景迭代获得高质量重建，但耗时通常在分钟至小时级别。tttLRM 作为前馈方法在推理速度上具有数量级优势（单张 A100 上秒级完成），且定性对比（Figure 4）显示其重建保真度已可比肩甚至部分超越优化基线。定量上，在结合少量后优化步骤（3 步或 10 步）后，tttLRM 可进一步超越优化方法的 PSNR（Table 7），说明快速权重提供的隐式 3D 先验具有作为优化初始化的潜力。

### 2. 方法谱系中的技术定位

tttLRM 处于三条技术路线的交叉点：**测试时训练**、**前馈 3D 重建**和**隐式神经表示**。

**测试时训练谱系**：tttLRM 直接继承自 TTT（Sun et al., ICML 2024）和 LaCT（大规模块测试时训练）的理论框架。TTT 的核心机制是在推理时通过最小化键值对的均方误差更新快速权重 $W = W - \eta \nabla \mathcal{L}_{\mathrm{MSE}}(f_W(k), v)$，使模型获得动态适应输入序列的能力。LaCT 将这一机制扩展至大规模块（可达百万级令牌），使得快速权重能够有效编码长序列的键值缓存为固定大小的神经记忆。tttLRM 的关键创新在于**首次将 TTT 的快速权重重新解释为隐式 3D 表示**：输入视图的几何与外观信息被压缩进快速权重的参数空间，随后通过虚拟令牌查询即可解码为 3DGS、三平面 NeRF 等多种显式格式。这一“压缩即表示”的范式突破了传统前馈重建模型对注意力缓存的依赖。

**前馈 3D 重建谱系**：与 GS-LRM、Long-LRM 等基于注意力的前馈方法相比，tttLRM 的核心差异在于**隐式 3D 表示的形成机制**。基线方法缺乏专门的隐式表示层，仅依赖令牌缓存或显式特征；tttLRM 则将快速权重本身作为跨视图的隐式 3D 记忆。查询机制亦有所不同：基线直接使用输入令牌进行解码，tttLRM 则引入虚拟令牌（虚拟视图或可学习的三平面令牌）作为查询媒介，这些虚拟令牌不参与快速权重的更新过程，仅从已更新的权重中提取任务相关特征。这一设计使得同一组快速权重可被不同查询解码为不同格式的 3D 表示，赋予框架极强的表示灵活性。

**自回归流式重建**：tttLRM 在自回归能力上实现了前馈基线无法支持的功能。通过修改快速权重的更新与应用步骤以纳入令牌间的因果依赖关系，模型可处理流式输入——每接收一小批视图（如 4 张图像）即更新快速权重并立即预测对应的 3D 高斯，随后丢弃该批图像。这一 RNN 式推理过程（Algorithm 1）使得模型无需一次性加载所有视图，在内存受限或流式采集场景中具有独特优势。

### 3. 适用边界与局限

**记忆容量的固定性**：快速权重的参数规模是固定的，其记忆容量存在上限。当处理极复杂场景或超长序列时，早期输入信息可能被后续更新覆盖，导致重建质量下降。论文未系统评估记忆容量与场景复杂度之间的定量关系，这一边界需要进一步刻画。

**自回归模式的权重漂移**：在流式推理中，快速权重随新视图持续更新，可能导致早期预测的高斯参数与后续更新的权重产生不一致。论文目前采用无需训练的历史选择性更新策略（Table 6）缓解此问题——该策略将 PSNR 从 24.81 提升至 24.95，SSIM 从 0.814 提升至 0.818——但权重漂移并未完全解决。论文明确指出，将选择性更新集成到训练过程中有望进一步改进，目前仅作为推理时的启发式策略。

**训练资源需求**：tttLRM 的训练依赖大规模分布式计算资源（64 块 A100 GPU，Figure 3 展示了分布式训练流水线），在资源受限环境中复现门槛较高。虽然推理时可通过多 GPU 实现线性加速，但训练成本仍是实际部署的考量因素。

**公平性与鲁棒性未评估**：论文未讨论模型在不同群体、极端光照条件或大面积遮挡下的性能表现。在 GSO（对象级）和 DL3DV-140/Tanks&Temples（场景级）数据集上的评估覆盖了标准条件，但缺乏对分布外场景的系统测试。

### 4. 开放问题

1. **记忆机制的可扩展性**：如何设计更高效的快速权重更新策略或层次化记忆结构，以支持百万级令牌的超长序列处理，同时保持线性复杂度优势？

2. **训练时集成历史选择性更新**：当前的历史选择性更新为推理时无需训练的启发式策略。将其作为可学习组件集成到训练过程中，能否从根本上解决自回归模式下的权重漂移问题？

3. **极端条件下的鲁棒性**：模型在极端光照、大面积遮挡、稀疏视角等条件下的重建质量如何？快速权重在这些场景下是否仍能形成有效的隐式 3D 表示？

4. **实时流式重建的工程化**：当前单张 A100 上的推理时间为秒级。通过进一步的工程优化（如模型量化、更高效的并行策略），能否实现真正的实时（<1 秒）流式高分辨率重建？

5. **表示格式的扩展边界**：论文展示了 3DGS 和三平面 NeRF 两种解码格式。快速权重所编码的隐式 3D 记忆能否被解码为其他表示形式（如 SDF、占用场），以及不同格式之间的转换是否存在信息损失？

## 原文 PDF

![[paperPDFs/CVPR_2026/tttLRM_Test_Time_Training_for_Long_Context_and_Autoregressive_3D_Reconstruction.pdf]]
