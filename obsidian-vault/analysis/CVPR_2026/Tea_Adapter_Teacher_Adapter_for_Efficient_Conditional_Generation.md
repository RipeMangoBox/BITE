---
title: "Tea-Adapter: Teacher Adapter for Efficient Conditional Generation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Tea_Adapter_Teacher_Adapter_for_Efficient_Conditional_Generation.pdf
project_link: null
code_link: null
aliases:
- TA
- Tea-Adapter
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
- topic/representation_self_supervised_transfer
core_operator: 利用同一架构族小模型与大模型在潜在空间中的强特征相似性，通过冻结的小型教师扩散模型进行反向知识蒸馏，配合混合条件专家（MCE）的动态路由机制，仅训练轻量 Tea-Adapter 即可使大型模型获得多条件可控生成能力，无需为每个新条件重复训练大模型。
primary_logic: 发现同一架构族的小型视频扩散模型与大型模型之间存在显著的特征分布相似性，使得控制知识可以从高效微调的小模型跨尺度迁移至大模型；同时不同视觉条件（如 Canny 边缘、深度图、姿态）具有内在关联，可通过专家混合统一学习、动态路由，甚至实现零样本泛化到未见条件。
claims:
- 在 Canny Edge 条件下，Tea-Adapter 的 FVD 达到 289.565，远低于 Ctrl-Adapter 的 427.060；在所有单条件下均取得最低 FVD 和最高 CLIP/LPIPS/SSIM。
- 消融实验显示，移除 MCE 层后 FVD 从 292.341 上升到 303.202，适配器数量减半后 FVD 急剧升至 398.013，证明 MCE 和足够适配器对性能至关重要。
- Tea-Adapter 的可训练参数量比 DiT-ControlNet 减少 70%（不含 MCE 层），同时保持可比性能。
- MCE 层支持零样本泛化：仅在部分条件上训练的模型，可以成功控制未见过的条件类型，生成高质量视频。
---

# Tea-Adapter: Teacher Adapter for Efficient Conditional Generation

> [!tip] 核心洞察
> 发现同一架构族的小型视频扩散模型与大型模型之间存在显著的特征分布相似性，使得控制知识可以从高效微调的小模型跨尺度迁移至大模型；同时不同视觉条件（如 Canny 边缘、深度图、姿态）具有内在关联，可通过专家混合统一学习、动态路由，甚至实现零样本泛化到未见条件。

| 字段 | 内容 |
|------|------|
| 中文题名 | Tea-Adapter：面向高效条件生成的教师适配器 |
| 英文题名 | Tea-Adapter: Teacher Adapter for Efficient Conditional Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Zhang_Tea-Adapter_Teacher_Adapter_for_Efficient_Conditional_Generation_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion #topic/representation_self_supervised_transfer |
| Method | Tea-Adapter |
| Dataset | Canny Edge, Depth Map, Pose, Overall Temporal Consistency |

> [!tip] 效果简介
> - Canny Edge (custom 100-video test set) 上，FVD↓ 289.565 vs 427.060 (Ctrl-Adapter) (-137.495)。
> - Depth Map (custom 100-video test set) 上，FVD↓ 292.341 vs 448.291 (Ctrl-Adapter) (-155.950)。
> - Pose (custom 100-video test set) 上，FVD↓ 300.582 vs 487.429 (Ctrl-Adapter) (-186.847)。

## 概要

**核心问题**：将多种视觉条件（如边缘图、深度图、人体姿态）注入大型视频扩散模型以实现可控生成，面临三重瓶颈——（1）对每个新条件全量微调大模型的计算成本极高；（2）级联多个独立 ControlNet 导致参数随条件数量线性增长，且无法动态融合多条件；（3）现有图像适配器直接迁移至视频时，难以保持跨帧的条件一致性与时序连贯性。

**核心洞见**：同一架构族的小型视频扩散模型与大型模型之间存在显著的潜在特征分布相似性（Figure 2）。这意味着，控制知识可以从高效微调的小模型跨尺度迁移至大模型，而无需直接训练大模型本身。同时，不同视觉条件（Canny 边缘、深度图、姿态等）具有内在关联，可通过专家混合机制统一学习与动态路由，甚至实现零样本泛化至未见条件。

**方法与定位**：Tea-Adapter 提出一种**反向知识蒸馏**范式——以冻结的小型条件视频扩散模型为“教师”，通过轻量适配器将其控制特征传递至冻结的大型文本到视频扩散模型（“学生”），仅训练适配器参数。其核心调控组件为**混合条件专家（MCE）层**与**特征传播模块**：MCE 由共享专家和条件特定专家组成，通过动态门控实现单次前向的多条件融合；特征传播模块则通过可学习调制因子、时间投影和上投影层，将条件特征对齐至大模型潜在空间并保持时序一致性。该方法在方法谱系上区别于：**Ctrl-Adapter**（Lin et al., arXiv 2024）的单一适配器设计、**Multi-ControlNet**（Sun et al., arXiv 2025）的级联独立分支、**Uni-ControlNet**（Zhao et al., NeurIPS 2024）的局部/全局控制组合，以及 **UniControl**（Qin et al., NeurIPS 2023）的 MoE 风格适配器。Tea-Adapter 的核心差异在于利用小模型作为“控制知识源”，而非直接从条件信号学习。

**主要结果**：在 Canny Edge、Depth Map、Pose 三个条件基准上，Tea-Adapter 的 FVD 分别达到 289.565、292.341、300.582，较 Ctrl-Adapter 分别降低 137.495、155.950、186.847，且在 CLIP、LPIPS、SSIM 指标上全面领先（Table 1）。时序一致性达 0.984，显著优于图像基线 UniControl 的 0.876。消融实验证实，移除 MCE 层使 FVD 从 292.341 升至 303.202，适配器数量减半后 FVD 急剧升至 398.013（Table 2），表明 MCE 和充足的适配器位置对条件保真度与生成质量至关重要。在参数效率方面，Tea-Adapter 的可训练参数量比 DiT-ControlNet 减少约 70%（不含 MCE 层），同时保持可比性能。此外，MCE 层支持零样本泛化：仅在部分条件上训练的模型可成功控制未见条件类型（Figure 8）。

### 问题背景：视频扩散模型的条件可控生成困境

大型文本到视频（Text-to-Video, T2V）扩散模型在视觉质量和文本跟随能力上取得了显著突破，但其“黑箱”式生成过程难以精确控制输出内容。在实际应用中，用户往往需要指定边缘轮廓、深度结构、人体姿态等条件信号来引导生成。然而，将这类条件控制能力注入大型视频扩散模型面临三个核心瓶颈：

1. **全量微调成本极高**：为每个新条件对大模型进行全量微调需要大量 GPU 资源和训练时间，引入一个新条件通常需要超过 48 GPU 小时，参数增量约 5 亿，这在资源受限环境下难以持续扩展。
2. **级联架构的线性增长**：Multi-ControlNet 等方案通过级联多个独立 ControlNet 实现多条件控制，但每增加一个条件就需要新增一个完整分支，导致参数线性膨胀，且各条件分支相互隔离，无法动态融合多条件信号。
3. **帧间一致性与时序连贯性缺失**：现有图像适配器方法（如 Uni-ControlNet、UniControl）将条件控制直接注入各帧，缺乏显式的时序对齐和尺度调制机制，难以保证视频帧间的条件一致性和运动连贯性。

### 现有方法缺口：从独立训练到跨尺度迁移的鸿沟

当前主流方案可分为两类，各有其结构性缺陷：

- **基于 ControlNet 的方法**（如 **DiT-ControlNet** (Hu and Xu, arXiv 2023)、**Multi-ControlNet** (Sun et al., arXiv 2025)）：将零卷积模块引入扩散模型的骨干网络，但需要为每个新条件训练独立的 ControlNet 副本，无法实现知识共享，且在多条件场景下通过简单加权求和融合，缺乏对条件间内在关联的建模。
- **基于适配器的方法**（如 **Ctrl-Adapter** (Lin et al., arXiv 2024)、**X-Adapter** (Ran et al., CVPR 2024)）：通过轻量适配器注入条件信号，参数量较小，但在视频场景下仍面临帧间一致性不足的问题。Ctrl-Adapter 在 Canny Edge 条件下的 FVD 高达 427.060，Pose 条件下达到 487.429，与理想水平有显著差距。

这些方法的共同盲点是：**始终围绕单一大型模型进行训练或适配，忽略了同一架构族内小模型与大模型之间潜在的特征相似性**。小型视频扩散模型可以在低资源下高效微调以获得条件控制能力，但这一能力如何迁移至大型模型，此前缺乏有效的桥接机制。

### 核心动机：跨模型特征相似性与反向知识蒸馏

Tea-Adapter 的核心动机源于一个关键发现：**同一架构族的小型视频扩散模型与大型模型在潜在空间中存在显著的特征分布相似性**（见 Figure 2）。这意味着，小型模型经过高效微调（如 LoRA）获得的条件控制特征，在分布上与大型模型所需的控制信号高度对齐。基于此，本文提出“反向蒸馏”范式——不再让大模型“教”小模型，而是让冻结的小型教师扩散模型将条件控制知识通过轻量适配器传递至冻结的大型学生模型。

这一范式转变带来了三重优势：

1. **训练效率飞跃**：仅需训练 Tea-Adapter 的轻量参数，在不使用 MCE 层时比 DiT-ControlNet 减少 70% 可训练参数，无需为每个新条件重复训练大模型。
2. **多条件统一融合**：通过混合条件专家（MCE）层替代级联 ControlNet，以动态路由机制激活共享和条件特定专家，实现单次前向的多条件融合，并具备零样本泛化到未见条件的能力。
3. **时序一致性保障**：特征传播模块（Feature Propagation Module）引入可学习调制因子、时间投影层和上投影层，动态调整条件特征并保证帧间一致性。

Figure 3 直观对比了 Tea-Adapter 与先前方法的范式差异：传统方法需要为每个条件重复训练大模型或级联多个 ControlNet，而 Tea-Adapter 仅需在低资源环境下训练适配器，即可驱动大型模型获得多条件可控生成能力。

## 核心方法与创新机理

Tea-Adapter 的核心创新在于**控制知识的跨尺度反向蒸馏**与**统一混合条件专家路由**两大机制，从根本上改变了大型视频扩散模型的可控生成范式。

### 1. 控制知识获取方式：从“逐条件重训大模型”到“小模型教大模型”

传统方法（如 DiT-ControlNet、Ctrl-Adapter）为每个新视觉条件（Canny 边缘、深度图、姿态等）引入新的控制分支时，需对大模型进行全量微调或训练独立 ControlNet 副本。当条件数量增加时，参数开销与训练成本线性增长——引入一个新条件约需增加 5 亿参数和超过 48 GPU 小时的训练。

Tea-Adapter 的解法是**反向知识蒸馏**：冻结一个小型条件视频扩散模型（教师）和一个大型文本到视频扩散模型（学生），仅训练一个轻量 Tea-Adapter 桥接两者。其可行性建立在作者的关键发现之上：**同一架构族的小模型与大模型在潜在空间中存在显著的特征分布相似性**（Figure 2）。小模型经 LoRA 或微调后已具备精准的条件跟随能力，Tea-Adapter 只需将小模型各 DiT Block 的条件控制特征提取、调制后注入大模型对应层，即可使大模型“继承”小模型的控制知识，全程无需修改两个预训练模型的参数。

这一设计将控制知识获取从“每条件重训大模型”变为“小模型学会后教给大模型”，可训练参数量比 DiT-ControlNet 减少约 70%（不含 MCE 层），同时保持可比性能。

### 2. 多条件融合架构：从“级联独立 ControlNet”到“统一混合条件专家”

多条件控制生成的经典方案是 Multi-ControlNet——级联多个独立 ControlNet，各条件分支相互隔离。其致命缺陷在于：条件数量增加时参数线性膨胀，且各分支独立训练导致条件间缺乏协同，难以动态融合。

Tea-Adapter 提出**混合条件专家（Mixture of Condition Experts, MCE）层**替代级联设计。MCE 由共享专家 $\mathcal{E}_{s}$ 和条件特定增量专家 $\Delta\mathcal{E}_{c_k}$ 组成，每个条件专家 $\mathcal{E}_{c_k}$ 通过加法组合共享知识与条件特有知识：

$$\mathcal{E}_{c_{k}}(x_{t}^{a}, t) = \mathcal{E}_{s}(x_{t}^{a}, t) + \Delta\mathcal{E}_{c_{k}}(x_{t}^{a}, t)$$

门控函数 $g_k(c_k, t)$ 根据输入条件类型和时间步动态路由，激活相关专家并加权融合：

$$h_{t}^{mce} = \sum_{k=1}^{K} g_{k}(c_{k}, t) \cdot \mathcal{E}_{c_{k}}(x_{t}^{a}, t)$$

这一设计的因果价值体现在三个层面：
- **参数共享**：共享专家捕获跨条件的通用控制模式，条件特定增量仅学习差异部分，避免为每个条件复制完整网络；
- **动态融合**：门控路由使单次前向即可融合多条件信号，无需手动加权或后处理；
- **零样本泛化**：门控机制学习到条件间的内在关联，使得仅在部分条件上训练的模型可以成功控制未见过的条件类型（Figure 8），这是级联方案无法实现的。

消融实验（Table 2）证实：移除 MCE 层后，FVD 从 292.341 升至 303.202，CLIP 从 0.913 降至 0.904，验证了 MCE 对条件融合质量的关键作用。

### 3. 特征传递与对齐：从“直接注入”到“时序感知的尺度调制”

将小模型特征直接注入大模型存在两个障碍：一是小模型与大模型的潜在空间维度不匹配，二是视频生成要求帧间条件信号保持时序一致。Tea-Adapter 的**特征传播模块（Feature Propagation Module）**通过三层机制解决这一问题：

- **上投影层（Up-Projection）**：将小模型特征 $\boldsymbol{x}_t^a$ 和 MCE 输出 $\boldsymbol{h}_t^{mce}$ 映射到大模型的潜在空间维度；
- **时间投影层（Time.Proj）与可学习调制因子（Modulation）**：生成动态尺度因子 $\boldsymbol{\alpha}_{\mathrm{scale}} = \mathrm{Modulation} + \mathrm{Time.Proj}(t)$，使特征强度随扩散时间步自适应调节；
- **残差集成**：最终适配器输出以残差形式注入大模型：$x_t = x_t + x_t^{a'}$，在保持预训练先验的同时注入条件控制。

完整传播函数为：

$$x_t^{a'} = u(x_t^a, c_{txt}, t; \theta)$$

其中 $\theta$ 为可训练参数，$c_{txt}$ 为文本编码。这一设计确保了跨帧条件信号的一致性和时序连贯性，在 Temporal Consistency 指标上达到 0.984，远高于 UniControl 的 0.876（Table 1）。

### 创新总结

Tea-Adapter 的三项 changed slots 构成一个闭环：**反向蒸馏**降低控制知识获取成本，**MCE 动态路由**实现多条件统一融合与零样本泛化，**特征传播模块**保证跨尺度对齐与时序一致。三者协同使 Tea-Adapter 成为一个即插即用的轻量适配器，仅需在低资源环境下训练适配器即可驱动冻结的大模型支持多种条件生成，消除了传统方案中冗余的逐条件训练开销。

Tea-Adapter 的整体设计围绕一个核心洞察展开：**同一架构族的小型视频扩散模型与大型模型在潜在空间中存在显著的特征分布相似性**（见 Figure 2）。基于这一发现，方法构建了一条“反向知识蒸馏”通路——将控制知识从高效微调的小模型跨尺度迁移至冻结的大模型，从而避免为每个新条件重复训练大模型。

### 任务形式化

条件视频生成任务可形式化为：

$$V_{\mathrm{gen}} = F_{l}\left( T, S( F_{s}( C ) ) \right)$$

其中，$C$ 为输入条件（如 Canny 边缘、深度图、姿态骨架等），$F_s$ 为冻结的小型条件视频扩散模型（教师），$S$ 为 Tea-Adapter 适配器，$F_l$ 为冻结的大型文本到视频扩散模型（学生），$T$ 为文本提示，$V_{\mathrm{gen}}$ 为生成视频。整个 pipeline 中，**仅 Tea-Adapter 的参数是可训练的**。

### 模块关系与数据流

Figure 4 给出了完整的架构概览，数据流按以下顺序组织：

![[assets/figures/papers/paper_list_l938_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_Tea_Adapter_Teac/figures/004_Figure_4.jpg]]
*Figure 4: Overview of Tea-Adapter. Left: To drive a large text-to-video diffusion model with new conditions, we first feed the condition latents to a frozen small pretrained conditional diffusion model, whose features are first injected into Tea-Adapter and then mapped to the frozen large diffusion model. Right: For each adapter, we design an Mixture of Condition Experts (MCE) layer to learn multiple control signals and a Feature Propagation module to transfer knowledge efficiently*

1. **条件注入小型教师模型**：输入条件 $C$ 首先送入冻结的小型条件视频扩散模型 $F_s$。该模型经过 LoRA 或轻量微调，能够接受多种条件输入，并在其 DiT Block 中生成富含控制信息的潜在特征。

2. **特征提取与适配器注入**：从 $F_s$ 的选定 DiT Block（首、尾及若干中间层）提取条件潜在特征，注入 Tea-Adapter。适配器内部包含三个关键子模块：
   - **Attention 模块**：对适配器内部特征执行自注意力，并与文本嵌入 $c_{txt}$ 进行交叉注意力，增强特征表达。
   - **混合条件专家（MCE）层**：由共享专家 $\mathcal{E}_s$ 和条件特定增量专家 $\Delta\mathcal{E}_{c_k}$ 组成，通过门控函数 $g_k(c_k, t)$ 动态路由激活相关专家，输出融合特征 $h_t^{mce}$：
     $$h_{t}^{mce} = \sum_{k=1}^{K} g_{k}(c_{k}, t) \cdot \mathcal{E}_{c_{k}}(x_{t}^{a}, t)$$
     $$\mathcal{E}_{c_{k}}(x_{t}^{a}, t) = \mathcal{E}_{s}(x_{t}^{a}, t) + \Delta \mathcal{E}_{c_{k}}(x_{t}^{a}, t)$$
   - **特征传播模块**：通过可学习调制因子 $\alpha_{scale}$、时间投影层和上投影层，将适配器特征对齐到大型模型的潜在空间，并保持帧间时序一致性：
     $$\alpha_{\mathrm{scale}} = \mathrm{Modulation} + \mathrm{Time.Proj}(t)$$
     $$\boldsymbol{x}_{t}^{a'} = \mathrm{Up.Proj}(\boldsymbol{x}_{t}^{a}) \cdot \boldsymbol{\alpha}_{\mathrm{scale}} + \mathrm{Up.Proj}(\boldsymbol{h}_{t}^{mce})$$

3. **残差注入大型学生模型**：Tea-Adapter 的最终输出 $x_t^{a'}$ 以残差形式添加到冻结的大型模型 $F_l$ 对应时间步的潜在变量中：
   $$x_{t} = x_{t} + x_{t}^{a'}$$

   这种残差集成方式在保持预训练先验的同时注入条件控制信号，最终由 $F_l$ 生成受控视频。

### 与基线方法的架构差异

Figure 3 对比了 Tea-Adapter 与现有范式的根本区别：
- **Multi-ControlNet**（Sun et al., arXiv 2025）等方案需为每个新条件训练独立的 ControlNet 分支并级联使用，参数随条件数量线性增长，且各分支相互隔离，无法动态融合。
- **DiT-ControlNet**（Hu and Xu, arXiv 2023）将 ControlNet 零模块引入 DiT 架构，但每次新增条件仍需重复训练大模型侧的控制模块。
- Tea-Adapter 将控制知识的学习完全转移到小型教师模型和轻量适配器上，**大模型始终冻结**。MCE 层通过共享专家实现参数复用，通过动态门控实现多条件的统一前向融合，甚至支持对未见条件的零样本泛化（见 Figure 8）。

### 参数效率

在不使用 MCE 层的情况下，Tea-Adapter 的可训练参数量比 DiT-ControlNet 减少约 **70%**，同时保持可比的控制性能（见 Section 3.3 及 Figure 6）。当需要支持多种条件时，MCE 层的共享专家设计进一步避免了参数随条件数量线性膨胀的问题。

Tea-Adapter 的核心设计围绕一个关键洞察展开：同一架构族的小型视频扩散模型与大型模型在潜在空间中存在显著的特征分布相似性（Figure 2）。基于此，方法通过冻结的小型教师模型提取条件控制特征，经轻量适配器传递至冻结的大型学生模型，仅训练适配器参数即可实现多条件可控生成。

### 任务形式化

条件视频生成任务可形式化为：

$$V_{\mathrm{gen}} = F_{l}\left( T , S( F_{s}( C ) ) \right)$$

其中 $F_s$ 为经过 LoRA 或微调的冻结小型条件视频扩散模型，接收条件 $C$（如 Canny 边缘图、深度图、姿态骨架等）并生成控制特征；$S$ 为 Tea-Adapter；$T$ 为文本提示；$F_l$ 为冻结的大型文生视频扩散模型（如 Wan2.1-14B / CogVideoX-5B）；$V_{\mathrm{gen}}$ 为最终生成的视频。

### 混合条件专家（MCE）层

为统一处理多种视觉条件并支持零样本泛化，Tea-Adapter 内部设计了混合条件专家层。在时间步 $t$，MCE 的输出为各条件专家的门控加权和：

$$h_{t}^{mce} = \sum_{k=1}^{K} g_{k}(c_{k}, t) \cdot \mathcal{E}_{c_{k}}(x_{t}^{a}, t)$$

其中 $x_t^a$ 为适配器当前时间步的输入特征，$g_k(c_k, t)$ 为条件 $c_k$ 对应的动态门控函数，决定各专家的激活权重。每个条件专家由共享专家与条件特定增量相加构成，实现参数高效与知识共享：

$$\mathcal{E}_{c_{k}}(x_{t}^{a}, t) = \mathcal{E}_{s}(x_{t}^{a}, t) + \Delta \mathcal{E}_{c_{k}}(x_{t}^{a}, t)$$

$\mathcal{E}_s$ 为所有条件共用的共享专家，$\Delta \mathcal{E}_{c_k}$ 为条件 $c_k$ 的特定增量。这种设计使得 MCE 能够学习不同视觉条件之间的内在关联，在仅训练部分条件时即可泛化至未见条件类型（Figure 8）。

### 特征传播模块

从教师模型提取的条件特征需要对齐到大型学生模型的潜在空间，同时保持视频帧间的时序一致性。特征传播模块通过以下步骤完成这一映射：

$$\alpha_{\mathrm{scale}} = \mathrm{Modulation} + \mathrm{Time.Proj}(t)$$

$$\boldsymbol{x}_{t}^{a'} = \mathrm{Up.Proj}(\boldsymbol{x}_{t}^{a}) \cdot \boldsymbol{\alpha}_{\mathrm{scale}} + \mathrm{Up.Proj}(\boldsymbol{h}_{t}^{mce})$$

其中 $\mathrm{Up.Proj}$ 为上投影层，将适配器特征维度对齐到大型模型的潜在空间；$\mathrm{Modulation}$ 为可学习的调制因子；$\mathrm{Time.Proj}(t)$ 为时间投影层，根据扩散时间步动态调整调制强度；$\boldsymbol{h}_{t}^{mce}$ 为 MCE 层的输出，通过上投影后以残差形式融入。整体特征传播函数可表示为：

$$x_{t}^{a'} = u(x_{t}^{a}, c_{txt}, t; \theta)$$

其中 $c_{txt}$ 为文本编码，$\theta$ 为适配器所有可训练参数。

### 残差集成

Tea-Adapter 的输出以残差方式注入大型模型的潜在变量，在保持预训练先验的同时引入条件控制：

$$x_{t} = x_{t} + x_{t}^{a'}$$

这一设计确保了大型模型原有的生成能力不被破坏，仅通过轻量残差信号实现精确的条件跟随。

### 适配器位置选择

Tea-Adapter 并非在大型模型的每一层都插入适配器，而是选择性地在第一个、最后一个以及若干中间 DiT Block 处传递条件潜在特征。这种稀疏插入策略在保持条件保真度的同时，大幅减少了可训练参数量——在不使用 MCE 层时，Tea-Adapter 的可训练参数比 **DiT-ControlNet**（Hu and Xu, arXiv 2023）减少 70%。

### 关键消融验证

消融实验（Table 2）从因果角度验证了上述模块的必要性：移除 MCE 层后，FVD 从 292.341 上升至 303.202，CLIP 从 0.913 降至 0.904，表明动态专家路由对多条件融合至关重要；将适配器使用的 DiT Block 数量减半后，FVD 急剧升至 398.013，CLIP 降至 0.875，说明足够的适配器插入位置是条件保真度的必要条件。

## 实验与关键发现

### 核心定量结果

Tea-Adapter 在三个主流视频控制条件下全面超越现有方法，同时保持最低的视频生成失真。Table 1 汇总了与 SOTA 基线的定量对比：

![[assets/figures/papers/paper_list_l938_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_Tea_Adapter_Teac/figures/006_Table_1.jpg]]
*Table 1: Comparison of state-of-the-art baselines. The best result in each column is bolded, and the second best is underscored*

- **Canny Edge 条件**：Tea-Adapter 取得 FVD 289.565，较 **Ctrl-Adapter**（Lin et al., arXiv 2024）的 427.060 降低 137.495（降幅约 32%），同时 CLIP 得分 0.918、LPIPS 0.255、SSIM 0.585 均为最优。
- **Depth Map 条件**：FVD 292.341，较 Ctrl-Adapter 的 448.291 降低 155.950（降幅约 35%），CLIP 0.913 领先。
- **Pose 条件**：FVD 300.582，较 Ctrl-Adapter 的 487.429 降低 186.847（降幅约 38%），条件跟随精度显著提升。
- **时序一致性**：Temporal Consistency 达 0.984，远超 **UniControl**（Qin et al., NeurIPS 2023）的 0.876（提升 0.108），验证了特征传播模块中时间投影层对帧间连贯性的关键作用。

上述结果基于 100 段视频的自定义测试集，评估指标覆盖生成质量（FVD）、语义对齐（CLIP）、感知相似度（LPIPS）和结构保真度（SSIM）。Tea-Adapter 在所有单条件场景下均取得最低 FVD 和最高 CLIP/LPIPS/SSIM，表明其控制知识迁移机制在保持视频自然度的同时实现了精准的条件跟随。

> **公平性提示**：各基线方法使用的训练数据、backbone 模型（如 Wan2.1 vs. CogVideoX）及训练策略存在差异，横向数值对比需结合这些因素综合判断。

### 消融实验

Table 2 报告了关键组件的消融结果（以 Depth Map 条件为例）：

![[assets/figures/papers/paper_list_l938_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_Tea_Adapter_Teac/figures/008_Table_2.jpg]]
*Table 2: Ablation study of key components*

- **移除 MCE 层的影响**：去除混合条件专家层后，FVD 从 292.341 升至 303.202（+10.861），CLIP 从 0.913 降至 0.904，LPIPS 从 0.251 升至 0.268。这表明 MCE 层的动态专家路由和条件共享机制对多条件融合及生成质量有实质性贡献。
- **适配器数量减半的影响**：将 Tea-Adapter 使用的 DiT Block 数量从 12 个减至 7 个后，FVD 急剧升至 398.013（+105.672），CLIP 降至 0.875，SSIM 降至 0.550。性能的大幅退化说明足够的适配器注入点对于条件保真度至关重要——过少的适配器位置无法充分传递控制信号，导致条件跟随能力显著下降。
- **参数效率验证**：在不使用 MCE 层的情况下，Tea-Adapter 的可训练参数量比 **DiT-ControlNet**（Hu and Xu, arXiv 2023）减少约 70%，同时维持可比性能。这得益于反向蒸馏架构中教师模型和学生模型均保持冻结，仅训练轻量适配器的设计。

Figure 7 的视觉消融结果进一步印证了上述定量发现：移除 MCE 层后视频的运动连贯性出现可见退化，而适配器数量减半则导致条件结构（如深度轮廓）的保真度明显降低。

![[assets/figures/papers/paper_list_l938_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_Tea_Adapter_Teac/figures/009_Figure_7.jpg]]
*Figure 7: Ablation results. We present results by removing the MCE layer and changing the number of adapters. Without the MCE layer and a half number of adapters, it exhibits different levels of degradation in motion coherence and quality*

### 多条件融合与零样本泛化

Tea-Adapter 的 MCE 层展现出两项关键能力：

1. **多条件融合**：通过共享专家与条件特定专家的动态路由（公式 $h_{t}^{mce} = \sum_{k=1}^{K} g_{k}(c_{k}, t) \cdot \mathcal{E}_{c_{k}}(x_{t}^{a}, t)$），MCE 可在单次前向传播中融合多种异质控制信号（如背景图、参考实例、人体运动），无需级联多个独立 ControlNet。Figure 8（Bottom）展示了同时给定背景、参考对象和人体姿态三种条件时的生成效果，各条件约束均得到有效满足且无冲突退化。

2. **零样本泛化**：MCE 的门控机制能够学习不同视觉条件之间的内在关联，使得仅在部分条件上训练的模型可以泛化到未见条件类型。Figure 8（Top）展示了这一能力：模型在未见过特定条件的情况下仍能生成高质量、可控的视频。这一性质源于条件特定专家 $\mathcal{E}_{c_{k}}$ 的增量设计（$\mathcal{E}_{c_{k}} = \mathcal{E}_{s} + \Delta\mathcal{E}_{c_{k}}$），共享专家 $\mathcal{E}_{s}$ 捕获跨条件通用知识，增量部分 $\Delta\mathcal{E}_{c_{k}}$ 则通过路由权重实现对新条件的隐式适应。

### 定性对比

Figure 5 展示了 Tea-Adapter 与五个基线方法在 Canny Edge、Depth Map 和 OpenPose 三种条件下的视觉对比。基于图像的方法（如 Uni-ControlNet）在跨帧一致性上表现较差，出现明显的帧间抖动和结构漂移；而基于适配器的视频方法中，Tea-Adapter 在条件轮廓保真度和运动平滑性上均优于 Ctrl-Adapter 等方案，验证了特征传播模块中可学习调制因子 $\alpha_{\mathrm{scale}}$ 和时间投影层对时序对齐的有效性。

![[assets/figures/papers/paper_list_l938_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_Tea_Adapter_Teac/figures/005_Figure_5.jpg]]
*Figure 5: Qualitative comparisons with baselines. “Ctrl” stands for “ControlNet” and “Apt” stands for “Adapter.” We perform the visual comparison with five baselines using the same conditions, while the image-based method shows poor performance in cross-frame consistency, and our method obtains better performance in the adapter-based methods*

### 参数效率分析

Figure 6 对比了各方法在引入多条件控制时的可训练参数量。传统 **Multi-ControlNet**（Sun et al., arXiv 2025）方案因级联多个独立 ControlNet，参数量随条件数量线性增长；Tea-Adapter 在移除 MCE 层后仅需最少可训练参数即可支持多条件控制。即使包含 MCE 层，其参数开销仍远低于为每个新条件训练独立 ControlNet 的方案（据原文估计，引入一个新条件需增加约 5 亿参数和超过 48 GPU 小时的训练），体现了反向蒸馏架构在资源效率上的显著优势。

![[assets/figures/papers/paper_list_l938_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_Tea_Adapter_Teac/figures/007_Figure_6.jpg]]
*Figure 6: Comparison of trainable model parameters in the diffusion model. Our methodology requires the fewest trainable parameters for multiple control signals when the MCE layer is removed, compared with other methods*

### 已知局限与待验证问题

- 当前实验基于 15K 视频训练集和特定 backbone（Wan2.1-14B / CogVideoX-5B），在更大规模视频基础模型（如 30B+ 参数）和超长时序生成场景下的效率与一致性表现尚待验证。
- MCE 层的零样本泛化能力目前仅在有限条件类型上得到展示，其对更广泛、更极端未见条件的适应边界需要进一步探索。
- 专家数量和路由策略的自动化优化（如动态增减专家）可能进一步提升多条件融合的灵活性和泛化能力，当前设计中这些超参数仍需人工设定。

## 定位与知识库关联

### 与现有工作的关系

**Tea-Adapter** 的核心设计动机源于对当前视频扩散模型可控生成范式的三重反思：大模型全量微调的高昂成本、级联式 ControlNet 的参数线性膨胀，以及图像级适配器在视频时序维度上的固有不足。其方法论定位可从以下几条谱系线索加以理解。

**（1）适配器范式的继承与超越。** Tea-Adapter 直接继承了面向扩散模型的适配器（Adapter）思想，但与 **X-Adapter**（Ran et al., CVPR 2024）等以插件兼容性为目标的方案不同，Tea-Adapter 的适配器并非用于桥接不同架构族的预训练模型，而是充当同一架构族内小模型与大模型之间的“控制知识传递器”。这一设计选择的关键前提是论文揭示的一个经验发现：同一架构族的小型与大型视频扩散模型在潜在空间中存在显著的特征分布相似性（参见 Figure 2）。因此，Tea-Adapter 的适配器本质上执行的是**反向知识蒸馏**——让冻结的大型学生模型从冻结的小型教师模型中“继承”条件控制能力，而非传统蒸馏中由大教小的方向。

**（2）统一条件控制路线的演进。** 在条件融合架构上，Tea-Adapter 的混合条件专家（MCE）层与 **Uni-ControlNet**（Zhao et al., NeurIPS 2024）和 **UniControl**（Qin et al., NeurIPS 2023）处于同一技术脉络。Uni-ControlNet 通过组合局部与全局控制分支实现图像级的统一条件控制；UniControl 则采用 MoE 风格的适配器和任务感知超网络实现跨任务的视觉控制统一。Tea-Adapter 的 MCE 层在此基础上进一步引入了**动态专家路由**和**共享/条件特定专家的分解设计**（见公式 $h_{t}^{mce} = \sum_{k=1}^{K} g_{k}(c_{k}, t) \cdot \mathcal{E}_{c_{k}}(x_{t}^{a}, t)$ 及 $\mathcal{E}_{c_{k}} = \mathcal{E}_{s} + \Delta\mathcal{E}_{c_{k}}$），使得多条件融合不再依赖多个独立分支的级联，而是在单次前向传播中通过门控函数动态激活相关专家。这一设计的直接对标对象是 **Multi-ControlNet**（Sun et al., arXiv 2025）——后者通过级联多个独立 ControlNet 实现多条件控制，每增加一个新条件就需要引入一个完整的 ControlNet 副本，导致参数线性增长。Tea-Adapter 以 MCE 层替代级联设计，在参数效率和扩展性上形成代际差异。

**（3）视频时序一致性的针对性解决。** 与 **Ctrl-Adapter**（Lin et al., arXiv 2024）和 **DiT-ControlNet**（Hu and Xu, arXiv 2023）等面向视频的适配器/ControlNet 方案相比，Tea-Adapter 的关键区分点在于其特征传播模块（Feature Propagation Module）的时序对齐设计。该模块通过可学习调制因子 $\alpha_{\mathrm{scale}} = \mathrm{Modulation} + \mathrm{Time.Proj}(t)$ 和时间投影层，将适配器特征动态对齐到大型模型的潜在空间，同时保持帧间一致性。相比之下，Ctrl-Adapter 虽也追求高效适配多种控制信号，但其特征注入方式缺乏显式的时序调制机制；而 DiT-ControlNet 虽将 ControlNet 的零卷积模块引入 DiT 架构，但仍需为每个新条件训练独立的控制分支。实验数据（Table 1）从侧面印证了这一差异：在 Canny Edge 条件下，Tea-Adapter 的 FVD 为 289.565，Ctrl-Adapter 为 427.060；在 Depth Map 条件下，FVD 差距更达 155.950。

### 适用边界

Tea-Adapter 的有效性建立在若干前提之上，理解这些边界条件对于正确评估其适用范围至关重要。

**（1）架构族内同源性要求。** Tea-Adapter 的核心假设——小模型与大模型之间存在潜在特征分布相似性——依赖于两者同属一个架构族（如 Wan 系列或 CogVideoX 系列）。若教师模型与学生模型来自不同的架构设计（例如，教师为 U-Net 架构的视频扩散模型，学生为 DiT 架构的模型），特征空间的跨架构对齐可能失效，适配器的知识传递效率将大幅下降。论文中的实验均在 Wan2.1-14B 和 CogVideoX-5B 等 DiT 架构族内进行，未验证跨架构族的迁移能力。

**（2）教师模型的条件覆盖范围。** Tea-Adapter 本身不直接学习条件到视频的映射，而是依赖冻结的小型教师模型 $F_s$ 来提取条件控制特征。这意味着教师模型必须已经具备对目标条件的控制能力（通过 LoRA 微调或全量微调获得）。对于教师模型完全未见过的全新条件类型，适配器缺乏可提取的控制信号源，MCE 层的零样本泛化能力（Figure 8 所示）仅限于在训练中见过的条件类型之间进行内插或组合，而非真正的外推到语义完全不同的新模态。

**（3）多条件冲突的隐式处理。** MCE 层通过动态路由实现多条件融合，但论文并未明确讨论当多个条件信号存在语义冲突时（例如，姿态骨架指示人物向右运动，而深度图暗示场景向左倾斜），路由机制如何解决冲突或进行优先级排序。当前设计依赖门控函数的软加权求和，本质上是对各条件专家输出的隐式折中，缺乏显式的冲突消解策略。

**（4）训练数据与基线的公平性。** 论文中各基线方法在其原有的训练数据和训练策略下评估，与 Tea-Adapter 使用的 15K 视频训练集及 backbone 存在差异，横向比较需持审慎态度。特别是，部分基线方法可能使用了更大规模或更高质量的训练数据，直接对比的公平性需要进一步控制变量验证。

### 局限与开放问题

尽管 Tea-Adapter 在参数效率和条件控制质量上展现了显著优势，但论文自身揭示及分析过程中浮现的若干局限值得关注。

**（1）MCE 层的参数开销权衡。** 论文明确指出，Tea-Adapter 在不使用 MCE 层时可训练参数比 DiT-ControlNet 减少 70%。然而，MCE 层本身引入了额外的可训练参数（共享专家和条件特定专家的参数），当条件类型数量增加时，条件特定专家 $\Delta\mathcal{E}_{c_k}$ 的数量也会相应增长。虽然 MCE 通过共享专家 $\mathcal{E}_s$ 实现了参数的部分复用，但在极端多条件场景下（例如，同时支持 10 种以上条件类型），MCE 层的总参数量是否会逼近甚至超过级联 ControlNet 方案，论文未给出定量分析。消融实验（Table 2）显示移除 MCE 后 FVD 从 292.341 升至 303.202，证明 MCE 对性能的贡献是显著的，但其参数效率的上界需要进一步研究。

**（2）适配器数量的敏感性与选择策略。** 消融实验显示，将 DiT Block 适配器数量从 12 减半至 7 后，FVD 急剧升至 398.013（Table 2），表明适配器的插入位置和数量对最终性能高度敏感。论文采用了“首、尾及若干中间 DiT Block”的启发式选择策略，但未提供系统性的适配器位置优化方法。在更大规模的视频基础模型（如 30B+ 参数级别）中，DiT Block 数量更多，如何自动确定最优的适配器插入位置是一个开放问题。

**（3）超长时序生成的未验证性。** 论文的实验设置聚焦于常规长度的视频生成，未测试 Tea-Adapter 在超长时序（如分钟级视频）生成场景下的表现。随着生成帧数的增加，特征传播模块中的时间投影层能否持续保持跨帧一致性，以及 MCE 层的动态路由在长时序下是否会出现专家激活漂移，均是需要进一步验证的问题。

**（4）开放问题。** 基于以上分析，以下几个方向值得后续工作关注：

- **跨任务泛化**：Tea-Adapter 的反向蒸馏架构能否扩展到其他视觉理解或生成任务（如基于小模型的多模态理解、图像编辑等），使大型基础模型通过冻结的小型专家模型获得多样化的下游能力？
- **自动化专家管理**：MCE 层中的专家数量和路由策略能否进一步自动化，例如通过动态增加或修剪条件特定专家来适应未知条件的零样本合成，而非依赖固定的专家池？
- **更大规模模型的适配**：在 30B+ 参数级别的视频基础模型和超长时序生成场景下，Tea-Adapter 的参数效率和时序一致性表现如何？适配器的插入策略是否需要根本性的调整？
- **条件冲突的显式建模**：是否可以通过引入条件间的显式依赖建模（如条件注意力或因果图）来替代 MCE 当前的隐式加权融合，从而在多条件存在语义冲突时实现更可控的合成结果？

## 原文 PDF

![[paperPDFs/CVPR_2026/Tea_Adapter_Teacher_Adapter_for_Efficient_Conditional_Generation.pdf]]
