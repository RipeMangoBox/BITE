---
title: "Mantis: A Versatile Vision-Language-Action Model with Disentangled Visual Foresight"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Mantis_A_Versatile_Vision_Language_Action_Model_with_Disentangled_Visual_Foresight.pdf
project_link: null
code_link: "https://github.com/SJTU-DENG-Lab/Mantis"
aliases:
- Mantis
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/representation_self_supervised_transfer
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过解耦视觉前瞻预测（DVF），使用meta queries与DiT头分离视觉预测任务，减轻VLA主干负担，使其专注语言理解与动作学习。
primary_logic: 将当前视觉状态通过残差连接馈入DiT，引导meta queries自动捕获帧间动态（即潜在动作），为显式动作预测提供紧凑而有指导性的辅助信号；同时采用渐进式多模态训练，在引入动作与视觉时保护语言理解能力。
claims:
- Mantis通过结合meta queries和DiT头实现视觉前瞻解耦，残差连接使meta queries自动捕获潜在动作。
- 在LIBERO仿真基准上，Mantis达到96.7%平均成功率，超过UnifiedVLA等强基线，且收敛速度更快。
- 真实世界实验中，Mantis在分布内和分布外指令跟随上均优于π0.5，语言监督对泛化至关重要。
- Mantis-ATE自适应时间集成策略可将推理调用减少近50%，且性能持平。
---

# Mantis: A Versatile Vision-Language-Action Model with Disentangled Visual Foresight

> [!tip] 核心洞察
> 将当前视觉状态通过残差连接馈入DiT，引导meta queries自动捕获帧间动态（即潜在动作），为显式动作预测提供紧凑而有指导性的辅助信号；同时采用渐进式多模态训练，在引入动作与视觉时保护语言理解能力。

| 字段 | 内容 |
|------|------|
| 中文题名 | Mantis：具有解耦视觉前瞻的多功能视觉-语言-动作模型 |
| 英文题名 | Mantis: A Versatile Vision-Language-Action Model with Disentangled Visual Foresight |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2511.16175) · [Code](https://github.com/SJTU-DENG-Lab/Mantis) |
| Topic | #topic/vision_multimodal_applications #topic/representation_self_supervised_transfer #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Mantis |
| Dataset | LIBERO, LIBERO Spatial, LIBERO Object, LIBERO Goal |

> [!tip] 效果简介
> - LIBERO 上，Average Success Rate (%) 96.7 vs 95.7 (F1) / 95.5 (UnifiedVLA) (+1.0 (over F1))。
> - LIBERO Spatial 上，Success Rate (%) 98.8 vs 98.2 (F1) (+0.6)。
> - LIBERO Object 上，Success Rate (%) 99.2 vs 98.8 (π0) (+0.4)。

## 概要

机器人的视觉-语言-动作（VLA）模型旨在将多模态感知与语言理解转化为可执行的动作。然而，低维动作信号的稀疏性难以充分监督大规模VLA模型的学习。现有方法试图通过**视觉前瞻预测**（Visual Foresight）引入辅助信号——要么显式生成未来像素帧，要么预测压缩视觉表示。前者引入大量冗余信息，分散模型对动作学习的注意力；后者则造成信息瓶颈，且普遍缺乏语言监督，导致模型的理解与推理能力退化。

Mantis 提出了一种**解耦视觉前瞻**（Disentangled Visual Foresight, DVF）机制来解决上述瓶颈。其核心思路是：将视觉预测任务从VLA主干网络中剥离，交由独立的扩散Transformer（DiT）头处理。具体而言，Mantis 引入一组可学习的 **meta queries**（称为 latent-action queries），与当前视觉观察一同输入主干网络；随后，通过残差连接将当前观察馈入DiT头，以简单的下一帧预测目标驱动 meta queries 自动捕获帧间动态——即隐含的“潜在动作”。这些紧凑而有指导性的潜在动作信号，被送入基于DiT的动作头，用于显式动作预测。同时，Mantis 采用**渐进式多模态训练**策略（先视觉预训练，再引入动作，最后加入语言监督），在融入动作与视觉能力时保护语言理解不被侵蚀。

在 LIBERO 仿真基准上，Mantis 达到 **96.7%** 的平均成功率，超过 UnifiedVLA、F1 等强基线，且收敛速度显著更快。真实世界实验中，Mantis 在分布内和分布外指令跟随任务上均优于开源VLA模型 π0.5，验证了语言监督对泛化能力的关键作用。此外，Mantis 的自适应时间集成策略（ATE）可将推理调用减少近 50%，同时保持性能持平。

**方法定位**：Mantis 属于视觉增强型VLA，通过解耦的扩散头实现隐式潜在动作学习，区别于显式像素预测（如 DreamVLA）和压缩表示引导（如 ATM）的范式。其渐进式训练与语言监督设计，使其在操作成功率、收敛效率与指令泛化三个维度上建立了新的综合优势。



### 视觉-语言-动作模型的核心瓶颈

视觉-语言-动作模型（VLA）旨在将大规模视觉-语言模型的语义理解能力迁移到机器人操作中，使机器人能够根据自然语言指令在复杂环境中执行任务。然而，当前VLA面临一个根本性挑战：**低维动作信号过于稀疏，无法为大规模VLA主干网络提供充分监督**。机器人示教数据中的动作通常仅为末端执行器的位姿序列（6-7维），而VLA主干的参数量往往达到数十亿级别，这种信号与模型容量之间的严重不匹配导致动作学习效率低下、泛化能力受限。

### 现有视觉增强范式的结构性缺陷

为缓解上述瓶颈，研究者提出利用视觉信号作为辅助监督，形成了三类主要范式（Figure 1）：

- **视觉前瞻（Visual Foresight）**：通过显式预测未来帧来增强动作学习。代表性工作如**UnifiedVLA**和**DreamVLA**，让VLA主干直接生成未来RGB图像。然而，生成高维像素级预测会引入大量与动作无关的视觉细节（如背景纹理），不仅造成计算冗余，还会分散模型对动作关键信息的注意力。
- **轨迹引导（Track Guidance）**：使用压缩的视觉状态表示（如**ATM**中的track tokens）指导动作预测。这种方式虽然减少了信息冗余，但压缩过程本身构成信息瓶颈，可能丢失对精确操作至关重要的细粒度空间线索。
- **潜在动作监督（Latent Action Supervision）**：通过辅助的潜在动作学习来改善动作预测。然而，这类方法通常缺乏显式的视觉预测目标，无法为模型提供直观的“前瞻”信号来引导动作规划。

上述方法的共同缺陷在于：**视觉预测任务与动作学习任务共享同一主干网络，导致容量竞争**——主干必须在有限的计算资源下同时处理语言理解、视觉生成和动作预测，最终在各项能力之间做出妥协。

### 语言能力退化的隐性危机

更值得关注的是，在引入视觉和动作监督的过程中，**现有方法普遍忽视了对语言理解能力的保护**。大规模VLA的初始语言能力来源于预训练的视觉-语言模型（如Qwen2.5-VL），但在面向机器人任务的微调阶段，模型参数被动作损失和视觉损失联合更新，语言相关的知识表征可能被覆盖或扭曲。这一退化在需要语言泛化的场景中尤为致命：当面对训练中未见的指令表述（分布外指令）时，模型可能无法正确解析语义意图，导致任务失败。

### 本工作的核心动机

针对上述问题，本文提出**Mantis**，核心动机可概括为三个层面：

1. **解耦视觉前瞻与动作学习**：将视觉预测任务从VLA主干中剥离，通过独立的解耦视觉前瞻（Disentangled Visual Foresight, DVF）模块处理，使主干专注于语言理解和动作推理。
2. **构建紧凑而有指导性的辅助信号**：利用meta queries自动捕获帧间动态（即“潜在动作”），为动作预测提供精准的前瞻线索，避免像素级预测的冗余与压缩表示的瓶颈。
3. **保护语言理解能力**：通过渐进式多模态训练策略，在引入视觉和动作监督的同时，显式维护语言监督信号，确保模型的指令遵循和语义泛化能力不被侵蚀。



## 核心方法与创新机理

Mantis针对现有视觉-语言-动作（VLA）模型的核心瓶颈——低维动作信号稀疏导致监督不足，而显式视觉前瞻预测（如像素生成）引入冗余、压缩表示（如track tokens）造成信息瓶颈——提出了三项关键创新，形成了一条从“解耦视觉前瞻”到“高效推理”的完整技术链路。

### 创新一：解耦视觉前瞻预测（DVF）

传统方法将未来帧预测任务直接置于VLA主干之上（如**UnifiedVLA**）或预测压缩轨迹表示（如**ATM**），前者与动作学习竞争模型容量，后者丢失细粒度视觉信息。Mantis的核心洞察在于**将视觉预测与动作学习彻底解耦**。

具体实现上，Mantis引入一组可学习的**潜在动作查询（Latent-Action Queries, `[LAT]`）** 与主干网络交互。这些查询令牌通过注意力机制自动捕获当前帧与未来帧之间的动态变化——即“潜在动作”。随后，一个独立的**扩散Transformer（DiT）头**（基于**Sana**架构）负责生成未来帧，其条件输入由两部分构成：主干输出的隐藏状态，以及通过**残差连接**注入的当前视觉观察 $\mathbf{o}_t$。这一残差设计至关重要——消融实验表明，移除残差连接会导致性能下降，因为它迫使meta queries仅依赖主干隐藏状态来推断帧间变化，而残差连接直接将当前状态 $\mathbf{o}_t$ 馈入DiT，使`[LAT]`能够更精准地聚焦于“从当前到未来”的变化量，即潜在动作。

形式化地，给定当前观察 $\mathbf{o}_t$ 和语言指令 $l$，主干编码过程为：

$$\mathbf{h}_t = \mathcal{P}(\mathbf{o}_t, l, [\mathrm{LAT}])$$

未来帧预测为：

$$\mathbf{o}_{t+n} = \mathcal{D}(\mathcal{C}(\mathbf{o}_t, \mathbf{h}_t))$$

其中 $\mathcal{C}$ 为连接器（12层Transformer编码器），$\mathcal{D}$ 为DiT头。动作预测则从包含`[LAT]`和动作查询`[ACT]`的隐藏状态中解码：

$$\mathbf{a}_{t:t+n} = \pi(\mathcal{P}(\mathbf{o}_t, l, [\mathrm{LAT}], [\mathrm{ACT}]))$$

这种设计使主干网络专注于语言理解与动作学习，而DiT头承担视觉预测的计算负载。收敛速度对比（Figure 5）直接验证了这一优势：Mantis在LIBERO上迅速收敛，而**UnifiedVLA**在前10个epoch成功率始终为零，说明共享主干的视觉预测严重干扰了动作学习的早期优化。

### 创新二：渐进式多模态训练策略

直接将视觉、动作、语言三种模态联合训练容易引发模态竞争与不稳定收敛。Mantis提出**三阶段渐进式训练**（Figure 2左），逐阶段解冻参数并引入新模态：

- **Stage 1（视频预训练）**：仅训练DVF头与连接器，主干冻结。在大规模视频数据上预训练视觉预测能力，为后续阶段提供高质量的潜在动作先验。消融实验（Table 2）证实，预训练的DVF（Pretrained-DVF）比从头训练的DVF（Scratch-DVF）平均成功率高约4.9个百分点（96.2% vs. 91.3%）。
- **Stage 2（视觉-动作联合训练）**：解冻主干，在机器人演示数据（**DROID**，76K条轨迹）上联合训练DVF与动作头，损失函数为 $\alpha \mathcal{L}_{\mathrm{DVF}} + \mathcal{L}_{\mathrm{action}}$，视觉损失权重 $\alpha=0.1$。此时模型已具备基本的视觉前瞻与动作预测能力。
- **Stage 3（语言监督混合训练）**：引入语言监督，在38个多模态数据集与DROID数据上联合微调，总损失扩展为 $\alpha \mathcal{L}_{\mathrm{DVF}} + \mathcal{L}_{\mathrm{action}} + \beta \mathcal{L}_{\mathrm{lang}}$，其中 $\mathcal{L}_{\mathrm{lang}}$ 为交叉熵损失。此阶段保护了主干的多模态理解能力——在VQA基准上（Table 3），Mantis相比原始**Qwen2.5-VL**主干性能仅轻微下降，且优于依赖VLM的基线（如**ECoT**、**ChatVLA**）。真实世界实验中，语言监督对分布外（OOD）指令泛化至关重要：移除语言监督的变体Mantis-LU在OOD任务上性能显著下降（Figure 9）。

### 创新三：自适应时间集成（ATE）

VLA模型常采用时间集成（Temporal Ensemble）提升运动平稳性，但固定集成策略带来高昂的计算开销。Mantis-ATE通过动态切换集成强度实现效率与性能的平衡。

ATE维护两组视觉令牌：**目标令牌**（与语言指令最相关的图像区域）和**动态令牌**（相邻帧间变化显著的区域）。当目标区域与动态区域重叠度低时（即操作已接近完成或场景趋于稳定），自动降低集成强度，减少推理调用。实验表明（Figure 8），Mantis-ATE将推理调用减少近50%，同时保持与标准Mantis相当的任务成功率。消融中使用的阈值参数为 $\tau_{\mathrm{target}} = 1$ 和 $\tau_{\mathrm{dynamic}} = 12$（Figure 4）。

### 创新总结

三项创新构成了一条因果链路：**DVF解耦**为动作学习提供紧凑而有指导性的辅助信号，解决了容量竞争与信息瓶颈；**渐进训练**确保多模态能力稳定融合，保护语言理解；**ATE**在部署端大幅降低推理成本，使系统具备实用价值。这一设计在LIBERO仿真基准上达到96.7%平均成功率（Table 1），在真实世界三个场景中，分布内和分布外指令跟随均优于开源基线**π0.5**（Table 6, Figure 6），验证了创新点的有效性。



Mantis 的整体设计围绕一个核心洞察展开：**视觉前瞻预测与动作学习应解耦**，从而避免主干网络在视觉生成与动作预测之间产生容量竞争。如图 2 所示，框架由三个核心模块构成：**Backbone（主干网络）**、**DVF Head（解耦视觉前瞻头）** 和 **Action Head（动作头）**，辅以连接器（Connector）和三类可学习查询令牌（queries）完成信息流转。

### 模块关系与信息流

1. **多模态输入打包**  
   对于时刻 $t$，系统将当前视觉观察 $\mathbf{o}_t$、语言指令 $l$ 以及一组可训练的**潜在动作查询** $[\mathrm{LAT}]$ 打包送入主干网络 $\mathcal{P}$，编码为隐藏状态：
   $$\mathbf{h}_t = \mathcal{P}(\mathbf{o}_t, l, [\mathrm{LAT}])$$

2. **解耦视觉前瞻预测**  
   连接器 $\mathcal{C}$ 将当前观察 $\mathbf{o}_t$ 与隐藏状态 $\mathbf{h}_t$ 融合，映射为 DVF 头 $\mathcal{D}$ 的条件输入。DVF 头基于扩散 Transformer（DiT）生成未来帧 $\mathbf{o}_{t+n}$：
   $$\mathbf{o}_{t+n} = \mathcal{D}(\mathcal{C}(\mathbf{o}_t, \mathbf{h}_t))$$
   关键设计在于**残差连接**：当前视觉状态直接馈入 DiT，使得 $[\mathrm{LAT}]$ 查询仅需捕获帧间动态差异——即“潜在动作”——而无需重建完整场景。这为显式动作预测提供了紧凑而有指导性的辅助信号。

3. **动作预测**  
   动作头 $\pi$ 接收主干输出（包含 $[\mathrm{LAT}]$ 和专门的动作查询 $[\mathrm{ACT}]$），预测从 $t$ 到 $t+n$ 的动作序列：
   $$\mathbf{a}_{t:t+n} = \pi(\mathcal{P}(\mathbf{o}_t, l, [\mathrm{LAT}], [\mathrm{ACT}]))$$
   $[\mathrm{LAT}]$ 在此充当视觉前瞻与动作学习之间的信息桥梁，使动作头能够利用 DVF 提取的时序动态。

4. **多间隔视觉监督**  
   除 $[\mathrm{LAT}]$ 和 $[\mathrm{ACT}]$ 外，Mantis 还引入**多间隔查询** $[\mathrm{GAP}]$，引导 DVF 头生成不同时间步间隔的未来帧，增加视觉监督密度，进一步提升潜在动作的提取质量（参见 Figure 3）。

### 关键设计决策

- **解耦的代价与收益**：传统方法（如 UnifiedVLA）让主干直接预测未来帧，导致视觉生成与动作学习共享容量；而 Mantis 将视觉预测外包给独立的 DiT 头，主干专注于语言理解与动作学习，收敛速度显著更快（Figure 5）。
- **残差连接的作用**：消融实验表明，移除残差连接会导致性能下降（Table 2），验证了“当前状态引导 + 查询捕获差异”这一机制的有效性。
- **渐进式多模态训练**：Mantis 采用三阶段训练——先视觉预训练，再引入动作联合训练，最后加入语言监督——逐阶段解冻参数，避免模态竞争，保护语言理解能力（详见训练策略章节）。

### 推理效率优化

标准 Mantis 使用时间集成（Temporal Ensemble, TE）提升运动平稳性，但带来高计算开销。为此，Mantis 提出**自适应时间集成（ATE）**：通过维护目标区域（与语言指令最相关的图像块）和动态区域（帧间变化显著的图像块），仅当两者重叠超过阈值时才触发集成，否则直接复用上一帧的动作预测。该策略可将推理调用减少近 50%，且任务成功率持平（Figure 8）。

> **注意**：框架图中的具体连接器实现（12 层 Transformer Encoder）、DVF 头采用的 Sana DiT 架构、动作头的 DiT 设计等细节，将在后续模块章节展开。

### 补充图表

![[assets/figures/papers/paper_list_l2401_https_arxiv_org_abs_2511_16175/figures/003_Figure_2.jpg]]
*Figure 2: Left: Progressive training recipe. Mantis progressively integrates multiple modalities to achieve stable and well-balanced optimization. Center: Overview of Mantis. The framework consists of a backbone network, a DVF head, and an action head. The DVF head predicts future frames to facilitate latent action learning, thereby improving action prediction. Language supervision helps maintain the backbone’s capability for understanding and reasoning. Right: Adaptive Temporal Ensemble. Mantis-ATE dynamically adjusts the ensemble strength based on the overlap between target tokens and dynamic tokens*



Mantis 的核心架构由四个关键模块构成：**主干网络**（Backbone）、**连接器**（Connector）、**解耦视觉前瞻头**（DVF Head）和**动作头**（Action Head）。其设计哲学是将视觉预测任务从 VLA 主干中剥离，通过一组可学习的查询令牌（queries）在模块间传递紧凑的“潜在动作”信号，避免显式像素生成或压缩表示带来的信息冗余与容量竞争。

### 主干编码与潜在动作查询

主干网络 $\mathcal{P}$（基于 Qwen2.5-VL）接收当前视觉观察 $\mathbf{o}_t$、语言指令 $l$ 和一组可训练的**潜在动作查询** $[\mathrm{LAT}]$，将其打包编码为隐藏状态：

$$\mathbf{h}_t = \mathcal{P}(\mathbf{o}_t, l, [\mathrm{LAT}])$$

$[\mathrm{LAT}]$ 是整个框架的信息瓶颈：它们在主干内部通过注意力机制与视觉-语言上下文交互，自动捕获帧间动态——即描述视觉轨迹变化的“潜在动作”。这些查询随后分别流向 DVF 头和动作头，为两个任务提供共享的时序表征。

### 解耦视觉前瞻（DVF）与残差连接

DVF 头的核心创新在于**残差连接**。连接器 $\mathcal{C}$ 将当前观察 $\mathbf{o}_t$ 与主干输出的隐藏状态 $\mathbf{h}_t$ 融合，映射为扩散 Transformer（DiT）头 $\mathcal{D}$ 的条件输入，生成未来帧 $\mathbf{o}_{t+n}$：

$$\mathbf{o}_{t+n} = \mathcal{D}(\mathcal{C}(\mathbf{o}_t, \mathbf{h}_t))$$

这里 $\mathbf{o}_t$ 通过残差路径直接馈入 DiT，使得 DVF 头始终能访问原始视觉信息。这一设计的关键因果机制是：**DiT 已知当前状态，只需预测“变化量”**，因此 $[\mathrm{LAT}]$ 被迫编码帧间差异——即潜在动作——而非完整的视觉内容。消融实验证实，移除残差连接会导致性能下降（Table 2, No-Residual variant），验证了该设计对潜在动作捕获的必要性。

此外，DVF 头引入**多间隔查询** $[\mathrm{GAP}]$，引导 DiT 生成不同时间步间隔的未来帧，增加视觉监督密度，使潜在动作表征更具时序一致性（Figure 3）。

![[assets/figures/papers/paper_list_l2401_https_arxiv_org_abs_2511_16175/figures/004_Figure_3.jpg]]
*Figure 3: Visualization of multi-gap future frame generation*

### 动作预测

动作头 $\pi$（同样基于 DiT）从主干输出中提取信息进行动作序列预测。此时主干额外接收**动作查询** $[\mathrm{ACT}]$：

$$\mathbf{a}_{t:t+n} = \pi(\mathcal{P}(\mathbf{o}_t, l, [\mathrm{LAT}], [\mathrm{ACT}]))$$

$[\mathrm{LAT}]$ 携带的潜在动作信号为显式动作预测提供了紧凑而有指导性的辅助信息，而 $[\mathrm{ACT}]$ 则负责从上下文中提取动作相关的直接线索。两者协同，使得动作头无需自行建模视觉动态。

### 渐进式多模态训练损失

Mantis 采用三阶段渐进训练，逐步引入视觉、动作和语言模态，各阶段损失函数递进叠加。

**第二阶段**（视觉-动作联合训练）的目标函数为：

$$\alpha \mathcal{L}_{\mathrm{DVF}} + \mathcal{L}_{\mathrm{action}}$$

其中 $\mathcal{L}_{\mathrm{DVF}}$ 为 DVF 头的扩散损失，$\mathcal{L}_{\mathrm{action}}$ 为动作头的扩散损失，$\alpha$ 为视觉损失权重（论文中设为 0.1）。

**第三阶段**引入语言监督，总损失扩展为：

$$\alpha \mathcal{L}_{\mathrm{DVF}} + \mathcal{L}_{\mathrm{action}} + \beta \mathcal{L}_{\mathrm{lang}}$$

$\mathcal{L}_{\mathrm{lang}}$ 为语言输出的交叉熵损失，$\beta$ 为其权重。语言监督使主干在适应机器人数据的同时保留视觉-语言理解能力，消融实验表明移除语言监督（Mantis-LU）会导致分布外指令泛化性能显著下降（Figure 9）。

### 自适应时间集成（ATE）

ATE 并非训练模块，而是推理时的效率优化策略。其核心思想是维护两组输入视觉补丁——**目标补丁**（与语言指令最相关的区域）和**动态补丁**（帧间变化显著的区域）——并根据两者的重叠程度动态切换时间集成的强度。当机器人末端执行器接近目标区域时，重叠增大，ATE 减少集成步数以降低计算开销；远离时则增强集成以保证运动平稳性。实验表明 Mantis-ATE 可将推理调用减少近 50%，同时保持与标准时间集成相当的任务成功率（Figure 8）。

### 补充图表

![[assets/figures/papers/paper_list_l2401_https_arxiv_org_abs_2511_16175/figures/002_Figure_1.jpg]]
*Figure 1: Vision-augmented action learning paradigms. (a) Visual Foresight enhances action prediction by forecasting future frames. (b) Track Guidance employs compressed visual state representations to guide action prediction. (c) Latent Action Supervision improves action learning through auxiliary latent actions*

![[assets/figures/papers/paper_list_l2401_https_arxiv_org_abs_2511_16175/figures/005_Figure_4.jpg]]
*Figure 4: Visualization of ATE. The attention heatmap uses darker colors to represent higher values, whereas in the cosine similarity heatmap the opposite holds. The parameters are set as*



## 实验与关键发现

### 核心实验设定

Mantis 的训练分为三阶段。Stage 1 在视频数据上进行视觉预训练；Stage 2 在 **DROID** 数据集（76K 机器人片段）上进行视觉-动作联合训练，视觉损失权重 α=0.1；Stage 3 引入语言监督，将 38 个多模态数据集（源自 LLaVA-OneVision-1.5-Instruct 的指令微调数据，排除专业领域，详见 Table 4）与 DROID 联合训练 1.5 个 epoch，此时解冻 Backbone 并施加交叉熵语言损失。所有 LIBERO 基准测试采用统一的数据集划分、训练周期和评估协议，基线结果直接引用自原始文献或统一复现。

### LIBERO 仿真基准主结果

Table 1 给出了 LIBERO 四个子任务上的全面对比。Mantis 在 Spatial、Object、Long 三个子任务上取得最优，平均成功率达到 **96.7%**，超过此前最强的显式视觉前瞻方法 **F1**（95.7%）和隐式方法 **UnifiedVLA**（95.5%）。在 Goal 子任务上，Mantis 为 94.4%，略低于 UnifiedVLA 的 95.6%，但仍处于第一梯队。值得注意的是，Mantis 在 Object 任务上达到 99.2%，超过 **π0** 的 98.8%，表明解耦视觉前瞻对物体操作类任务尤为有效。

![[assets/figures/papers/paper_list_l2401_https_arxiv_org_abs_2511_16175/figures/006_Table_1.jpg]]
*Table 1: Comparison on the LIBERO benchmark. Mantis exhibits superior performance on 3 of 4 tasks and attains the highest average success rate compared to existing baseline methods, demonstrating the effectiveness of leveraging DVF for action prediction. Bold indicates the best performance, and Italics indicates the second-best performance*

| 子任务 | Mantis | F1 | UnifiedVLA | π0 |
|--------|--------|-----|-----------|-----|
| Spatial | **98.8** | 98.2 | — | — |
| Object | **99.2** | — | — | 98.8 |
| Goal | 94.4 | — | **95.6** | — |
| Long | **94.2** | — | 94.0 | — |
| **平均** | **96.7** | 95.7 | 95.5 | — |

### 收敛速度分析

Figure 5 展示了 Mantis 与传统视觉前瞻方法的收敛速度对比。Mantis 从训练初期即快速提升成功率，而 **UnifiedVLA** 在前十个 epoch 成功率始终为零，收敛最慢。这一差异直接验证了核心设计动机：将视觉预测任务解耦到独立的 DVF 头，避免了 Backbone 内部的容量竞争，使模型能更快地学习有效的动作策略。

![[assets/figures/papers/paper_list_l2401_https_arxiv_org_abs_2511_16175/figures/007_Figure_5.jpg]]
*Figure 5: Convergence speed comparison. Compared with traditional visual foresight methods such as UnifiedVLA [43], Mantis achieves significantly faster convergence speed, underscoring the necessity of decoupling foresight prediction from action learning*

### 消融实验：DVF 架构与训练策略

Table 2 系统消融了 DVF 的四个关键设计维度：

![[assets/figures/papers/paper_list_l2401_https_arxiv_org_abs_2511_16175/figures/011_Table_2.jpg]]
*Table 2: Comparison of four DVF variants. Bold indicates the best performance, Italics indicates the second-best performance*

1. **DVF 的存在性**：无 DVF 的变体平均成功率仅 91.3%，为所有变体中最低，直接证明视觉前瞻对动作学习的辅助价值。
2. **残差连接**：移除残差连接（No-Residual）导致性能下降，说明将当前视觉状态直接馈入 DiT 头对于 meta queries 捕获帧间动态至关重要。
3. **视频预训练**：从零开始训练 DVF（Scratch-DVF）的性能低于预训练 DVF（Pretrained-DVF），后者达到 **96.2%** 的最优平均成功率，验证了 Stage 1 视频预训练的有效性。

### 语言监督的消融与泛化能力

Figure 9 对比了 Mantis 与移除语言监督的变体 **Mantis-LU**。在分布内（ID）指令上，两者性能接近；但在分布外（OOD）指令上，Mantis-LU 的性能显著下降。这表明语言监督并非简单提升绝对成功率，而是赋予模型理解未见指令、进行常识推理的能力，是实现 OOD 泛化的关键因素。

![[assets/figures/papers/paper_list_l2401_https_arxiv_org_abs_2511_16175/figures/013_Figure_9.jpg]]
*Figure 9: Comparison between Mantis and Mantis-LU*

Table 3 进一步从 VQA 与多模态理解基准角度验证语言能力保留。Mantis 在三个基准中的两个上取得最优，且与原始 Backbone（Qwen2.5-VL）相比性能仅轻微下降，证明渐进式多模态训练有效保护了语言理解能力。

![[assets/figures/papers/paper_list_l2401_https_arxiv_org_abs_2511_16175/figures/012_Table_3.jpg]]
*Table 3: Comparison on VQA and multimodal understanding benchmarks. Mantis achieves superior performance on 2 of the 3 benchmarks. Compared with the original backbone, its performance decreases only marginally. Bold denotes the best results*

### 真实世界实验

真实世界实验在 Agilex 平台上进行，涵盖三个场景，每个场景包含 4 条分布内指令和 4 条分布外指令（OOD 指令分别评估世界知识、基础推理能力和人类意图理解，详见 Table 5）。Mantis 与开源 VLA 模型 **π0.5** 使用相同的机器人平台、数据收集和微调流程进行公平对比，但 Mantis 额外接受语言监督。

Table 6 和 Figure 6(c) 显示：在 ID 指令上，Mantis 平均成功次数为 7.83，略高于 π0.5 的 7.25；在 OOD 指令上，差距急剧拉大——Mantis 为 6.58，π0.5 仅为 2.83。OOD 增益达 +3.75，与仿真消融结论一致，再次印证语言监督对泛化的决定性作用。

![[assets/figures/papers/paper_list_l2401_https_arxiv_org_abs_2511_16175/figures/008_Figure_6.jpg]]
*Figure 6: Real World Experiments. (a) The Agilex platform. (b) Scenario setups and example instructions. Each scenario shows one ID instruction and the corresponding OOD instruction. (c) Average success counts for Mantis and*

### DVF 生成质量验证

Figure 7 可视化了 DVF 生成的未来帧。在多种操作任务中，最后生成的未来帧与真值终态高度吻合，证实 DVF 能够有效捕捉任务完成时的目标状态，为动作预测提供紧凑且有指导性的前瞻信号。

![[assets/figures/papers/paper_list_l2401_https_arxiv_org_abs_2511_16175/figures/009_Figure_7.jpg]]
*Figure 7: Visualization of Generated Future Frames. The last generated future frame closely mirrors the ground truth final state, substantiating the efficacy of the DVF in refining action prediction across diverse manipulation tasks*

### 推理效率：自适应时间集成

Figure 8 对比了标准 Mantis（使用固定时间集成 TE）与 **Mantis-ATE**。Mantis-ATE 在保持任务成功率基本持平的前提下，将推理调用次数减少近 50%。其核心机制（Figure 4 可视化）是维护目标区域（target patches）和动态区域（dynamic patches）两组视觉 patch，根据二者重叠程度动态切换时间集成的强度：当场景变化剧烈时加强集成以保证运动平稳性，当场景稳定时减少集成以节省计算。消融中使用的阈值参数为 $\tau_{\mathrm{target}} = 1$ 和 $\tau_{\mathrm{dynamic}} = 12$。

![[assets/figures/papers/paper_list_l2401_https_arxiv_org_abs_2511_16175/figures/010_Figure_8.jpg]]
*Figure 8: Comparison between standard Mantis (TE) and Mantis-ATE. The primary vertical axis denotes success rate (SR), and the secondary vertical axis denotes inference count (IC)*

### 失败模式与局限

尽管整体表现优异，Mantis 仍存在以下已知局限：

- **空间精度受限**：模型输入主要依赖 RGB 图像，缺乏 3D 几何信息（如点云），在 LIBERO Goal 子任务上未能超越 UnifiedVLA，暗示高精度空间推理场景仍是薄弱环节。
- **实时性瓶颈**：即使 ATE 减少了近半推理调用，单次推理仍基于大规模扩散模型，难以满足高频实时控制需求。
- **真实世界覆盖不足**：目前仅在桌面操作场景验证，尚未在移动操作等更复杂、非结构化环境中充分测试。



## 定位与知识库关联

### 视觉增强动作学习的范式演进

Mantis 的提出建立在视觉增强动作学习的三条技术路线之上（Figure 1）：

1. **显式视觉前瞻（Visual Foresight）**：直接预测未来帧作为辅助信号。代表工作包括 **UnifiedVLA** 和 **F1**。此类方法将未来帧预测任务加载到 VLA 主干上，导致主干容量被视觉生成任务挤占，同时生成的像素级冗余信息可能分散模型对动作学习的注意力。

2. **轨迹引导（Track Guidance）**：使用压缩的视觉状态表示（如 track tokens）引导动作预测，典型工作如 **ATM**。该方法通过压缩表示缓解了信息冗余，但压缩过程本身引入了信息瓶颈，可能丢失对精细操作至关重要的视觉细节。

3. **隐式动作监督（Latent Action Supervision）**：通过辅助的隐式动作学习改善动作预测，如 **DreamVLA** 采用隐式视觉前瞻。此类方法缺乏显式的语言监督，导致模型的理解与推理能力在引入动作与视觉模态后下降。

Mantis 提出的**解耦视觉前瞻（Disentangled Visual Foresight, DVF）**可视为对上述三条路线的综合改进：将视觉预测任务从主干中剥离，交由独立的 DiT 头处理，既避免了显式方法的容量竞争，又通过 meta queries 与残差连接自动提取紧凑的帧间动态（潜在动作），绕过了压缩方法的信息瓶颈。同时，渐进式多模态训练策略在引入动作与视觉模态时保护了语言理解能力。

### 关键设计选择与基线对比

| 设计维度 | 传统方法 | Mantis 方案 | 改进机制 |
|---------|---------|------------|---------|
| 视觉前瞻预测 | 主干直接预测未来帧（UnifiedVLA）或压缩表示（ATM） | 解耦到独立 DiT 头，通过 meta queries 提取潜在动作 | 消除容量竞争，提供紧凑而有指导性的辅助信号 |
| 多模态训练 | 同时训练视觉、语言、动作，易造成模态竞争 | 渐进式三阶段：先视觉预训练，再引入动作，最后加入语言监督 | 逐阶段解冻参数，保护语言能力不被动作与视觉任务侵蚀 |
| 推理效率 | 固定时间集成（Temporal Ensemble）提升运动平稳性 | 自适应时间集成（ATE），根据目标区域与动态区域重叠动态切换 | 减少近 50% 推理调用，性能持平 |

### 在 VLA 模型谱系中的定位

Mantis 以 Qwen2.5-VL 为主干，属于**大规模视觉-语言-动作模型**阵营，与以下工作处于同一竞争赛道：

- **OpenVLA**：非视觉增强的 VLA 基线，直接基于视觉-语言模型预测动作，缺乏对物理动态的显式建模。
- **π0 / π0.5**：开源 VLA 模型，π0.5 作为真实世界基线在本文中被直接对比。在分布内（ID）与分布外（OOD）指令跟随任务上，Mantis 均显著优于 π0.5，尤其在 OOD 场景中优势明显（平均成功次数 6.58 vs 2.83），验证了语言监督对泛化能力的关键作用。
- **UnifiedVLA**：最直接的视觉增强对比对象，采用隐式视觉前瞻。Mantis 在 LIBERO 平均成功率上以 96.7% 超越 UnifiedVLA 的 95.5%，且收敛速度显著更快（Figure 5），证明解耦设计的必要性。

### 适用边界与局限

1. **输入模态限制**：Mantis 主要依赖 RGB 图像，缺乏 3D 几何信息（如点云）。在处理高精度空间推理任务（如 LIBERO Goal 子任务上 Mantis 的 94.4% 低于 UnifiedVLA 的 95.6%）时，二维视觉信号可能不足以捕捉精细的空间关系。

2. **实时性瓶颈**：尽管 ATE 将推理调用减少近 50%，单次推理仍基于大规模扩散模型（DiT 头 + Qwen2.5-VL 主干），难以满足高频实时控制需求（如 >10Hz 的阻抗控制场景）。

3. **真实世界验证范围有限**：真实世界实验仅在 Agilex 平台的三个桌面操作场景上完成，尚未在移动操作、人机交互、非结构化环境等更复杂条件下充分测试。

4. **损失权重敏感性**：渐进式训练的联合损失 $\alpha \mathcal{L}_{\mathrm{DVF}} + \mathcal{L}_{\mathrm{action}} + \beta \mathcal{L}_{\mathrm{lang}}$ 涉及两个平衡系数 α 和 β，其对语言能力与操作性能的权衡尚未被系统性地消融研究。

### 开放问题与后续方向

- **多模态融合**：如何整合 3D 点云、触觉或音频模态以提升操作精度和任务多样性？DVF 框架是否可扩展至预测多模态未来状态？
- **推理加速**：能否通过模型蒸馏、量化或更轻量的预测头（如 flow matching 替代扩散）进一步压缩推理延迟，实现更高频率的闭环控制？
- **开放环境泛化**：解耦的视觉前瞻机制在非结构化、动态变化的环境中是否依然有效？meta queries 捕获的潜在动作能否泛化到未见过的物体与场景？
- **语言-操作权衡**：如何在更强的语言能力与操作性能之间取得最佳折衷？语言监督阶段使用的 38 个多模态数据集（Table 4）中，是否存在与机器人操作任务产生负迁移的数据分布？



## 原文 PDF

![[paperPDFs/CVPR_2026/Mantis_A_Versatile_Vision_Language_Action_Model_with_Disentangled_Visual_Foresight.pdf]]
