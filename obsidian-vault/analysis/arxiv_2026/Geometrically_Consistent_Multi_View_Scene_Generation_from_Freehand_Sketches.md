---
title: Geometrically Consistent Multi-View Scene Generation from Freehand Sketches
type: paper
paper_level: A
venue: arXiv
year: 2026
pdf_ref: paperPDFs/arxiv_2026/Geometrically_Consistent_Multi_View_Scene_Generation_from_Freehand_Sketches.pdf
project_link: null
code_link: null
aliases:
- CAVDSCS
- GCMVSGFFS
tags:
- arxiv_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
core_operator: 通过在视频扩散Transformer中引入并行相机感知注意力适配器（CA3）以编码相对射影几何（PRoPE），并在适配器的查询-键投影上施加稀疏InfoNCE对应监督损失（CSL），显式强制模型学习跨视角几何一致性。
primary_logic: 将相机参数注入注意力计算可赋予生成模型显式处理多视角投影的能力，而对应监督损失教会模型哪些空间位置应跨视角相互关注，二者协同将抽象的草图笔触转化为一致的3D表达。
claims:
- 在S2MV测试集上，本文方法相比两阶段基线在真实感（FID）上提升超过60%，几何一致性（Corr-Acc）提升23%，同时推理速度提升3.7倍。
- 移除CA3模块后，FID从18.49恶化至266.06，PSNR降至5.026，证实相机感知注意力对几何推理至关重要。
- 移除CSL损失后，Corr-Acc从0.199降至0.175，且注意力图变得扩散非结构化，验证了对应监督对实现几何一致性的核心作用。
- S2MV test set (477 samples, N=33 views, 3 seeds) 上 FID↓ = 18.49
---

# Geometrically Consistent Multi-View Scene Generation from Freehand Sketches

> [!tip] 核心洞察
> 将相机参数注入注意力计算可赋予生成模型显式处理多视角投影的能力，而对应监督损失教会模型哪些空间位置应跨视角相互关注，二者协同将抽象的草图笔触转化为一致的3D表达。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于自由手绘草图的几何一致性多视角场景生成 |
| 英文题名 | Geometrically Consistent Multi-View Scene Generation from Freehand Sketches |
| 会议/期刊 | arXiv 2026 |
| Links | [paper](https://arxiv.org/abs/2604.14302) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation |
| Method | CA3-Adapted Video DiT with Sparse Correspondence Supervision |
| Dataset | S2MV test set |

> [!tip] 效果简介
> - S2MV test set (477 samples, N=33 views, 3 seeds) 上，FID↓ 18.49 vs 46.34 (SEVA) / 48.22 (ViewCrafter) (-60.1% (vs SEVA), -61.7% (vs ViewCrafter))。
> - S2MV test set 上，Corr-Acc↑ 0.199 vs 0.161 (SEVA) / 0.136 (ViewCrafter) (+23.6% (vs SEVA), +46.3% (vs ViewCrafter))。
> - S2MV test set (inference time, N=33 views, single A100 GPU) 上，Time/sample ~50 s vs ~3.1 min (FLUX+SEVA) / ~35 min (FLUX+ViewCrafter) (3.7× speedup over SEVA, 42× over ViewCrafter)。

## 概要

### 问题瓶颈

从单一自由手绘草图生成几何一致的多视角3D场景，面临三重耦合挑战：**（i）配对训练数据完全缺失**——现有大规模数据集均为照片或文字驱动，无法直接迁移至草图域；**（ii）草图本身具有极端的几何不确定性**——扭曲的2D笔画缺乏精确的深度、比例和相机信息，模型必须从高度抽象的线条中推断合理的相机几何；**（iii）跨视角结构一致性难以保证**——多视图生成要求不同视角下的物体形态、纹理和空间关系保持严格一致，而草图的稀疏性使这一约束极易被违反。现有方法如SEVA和ViewCrafter均采用两阶段流水线（草图→照片→多视图），虽可借助预训练模型缓解域差距，但中间照片生成阶段引入的误差会逐级放大，且缺乏端到端的几何一致性学习机制。

### 核心方法

本文提出**CA3-Adapted Video DiT with Sparse Correspondence Supervision**，以单阶段端到端方式直接从草图生成多视角图像。核心调控旋钮有二：**（i）并行相机感知注意力适配器（CA3）**——在冻结的视频扩散Transformer（Wan 2.1）的每个DiT块中插入轻量级并行分支，通过射影旋转位置编码（PRoPE）将相对相机几何显式注入注意力分数计算，使模型具备处理多视角投影的几何偏置；**（ii）稀疏InfoNCE对应监督损失（CSL）**——利用SfM（COLMAP）从伪真值多视图数据中提取跨视角关键点对应，在CA3的查询-键投影上施加对比损失，显式教会模型哪些空间位置应跨视角相互关注。二者协同，将抽象的草图笔触转化为一致的3D表达。

### 方法谱系与知识库定位

| 维度 | 现有方法 | 本文方法 |
|------|---------|---------|
| **流水线阶段** | 两阶段（草图→照片→多视图），如SEVA、ViewCrafter | 单阶段端到端（草图→多视图一次去噪完成） |
| **相机几何感知** | 全局相机参数注入或无显式几何偏置 | 并行CA3适配器，PRoPE编码相对射影变换至注意力分数 |
| **跨视角监督** | 隐式（共享特征体积、极线约束）或无 | 显式稀疏InfoNCE对应损失，基于SfM关键点 |
| **训练数据** | 依赖百万级自然视频数据 | 自动构建的9,222组草图-多视图配对数据集（S2WV） |

在知识库定位上，本文处于**草图理解**与**多视角生成**的交汇点。相较于单视图草图生成方法（仅关注2D真实感），本文首次将问题拓展至3D一致的多视角空间；相较于已有的多视角扩散模型（如MVDream、Zero123++），这些方法以照片或文本为输入，无法处理草图的几何模糊性。本文通过**相机感知注意力适配器**和**对应监督损失**两个技术增量，在冻结的视频扩散模型上实现了草图到多视图的直接映射，参数增量仅约2.7%。

### 主要结果

在S2MV测试集（477个草图，每样本33个视角，3个随机种子）上，本文方法相较于两阶段基线取得显著提升：

- **真实感（FID↓）**：18.49，较SEVA（46.34）提升60.1%，较ViewCrafter（48.22）提升61.7%。
- **几何一致性（Corr-Acc↑）**：0.199，较SEVA（0.161）提升23.6%，较ViewCrafter（0.136）提升46.3%。
- **推理效率**：单A100 GPU生成33个视角仅需约50秒，较FLUX+SEVA（约3.1分钟）提速3.7倍，较FLUX+ViewCrafter（约35分钟）提速42倍。

消融实验进一步验证了各组件的决定性作用：移除CA3模块后FID从18.49骤升至266.06，PSNR从12.169降至5.026，模型完全丧失生成有意义视图的能力；移除CSL损失后Corr-Acc降至0.175，注意力图变为扩散非结构化（Fig. 6），证实对应监督对几何一致性的核心贡献。

### 局限与开放问题

当前方法存在以下局限：训练数据仅8,304个样本，远少于基线所用的百万级视频数据，限制了场景多样性，复杂遮挡场景的后视图易产生模糊或幻觉；多视角训练视图由图像编辑模型生成，可能包含光照不一致、纹理漂移等伪影；训练分辨率受限于480×480，因并行处理N个视图消耗大量GPU内存。开放问题包括：如何扩展数据流水线以覆盖更复杂的多对象遮挡场景；如何在缺乏真实3D标注的情况下减少生成真值带来的伪影；能否通过梯度检查点或模型并行突破内存瓶颈以实现更高分辨率训练。



### 问题背景：从草图到3D场景的认知鸿沟

自由手绘草图是人类表达三维空间构思最本能、最便捷的媒介之一——寥寥数笔即可勾勒出物体的轮廓、遮挡关系和空间布局。然而，将这种高度抽象、几何不确定的二维笔画转化为一组空间一致、照片般真实的多视角图像，始终是计算机视觉与图形学交叉领域的一项核心挑战。

这一问题的本质在于**三重复合困难**。首先，自由手绘草图天然携带几何扭曲：画者并非精密制图员，线条比例失调、透视不准确、局部细节残缺是常态。其次，从单一视角的2D笔画推断完整的3D场景结构本身是严重欠约束的逆问题——同一幅草图理论上可对应无穷多种三维解释。最后，当目标不仅是重建单一视角，而是生成覆盖完整360°方位角、多个仰角的多张视图时，跨视角的结构一致性成为额外的硬约束：同一物体在不同视角下的外观必须遵循刚体变换和透视投影的物理规律，否则视觉上会立刻暴露“拼接感”。

### 现有方法的缺口

当前主流的多视角生成方法可归为两条技术路线，但均无法直接处理草图输入。

**基于照片的扩散模型路线**以**SEVA**（Stable Virtual Camera）和**ViewCrafter**为代表，采用两阶段流水线：先将草图通过FLUX等图像生成模型转化为真实照片，再将照片作为输入，利用潜在扩散模型或视频扩散模型逐视角生成新视图。这一范式存在两个根本性局限。其一，草图到照片的翻译步骤是一个信息瓶颈——生成的照片可能偏离草图的语义意图，而后续的多视角生成完全依赖这张可能已失真的中间产物，错误将级联放大。其二，两阶段流程中各模块独立训练，缺乏端到端的跨视角几何约束，导致生成的新视图之间容易出现结构漂移。

**基于3D重建的路线**依赖Structure-from-Motion（SfM）或点云估计（如DUSt3R）从照片中显式恢复相机参数和稀疏几何，再以此为条件驱动新视图合成。这类方法对输入照片的质量高度敏感，且计算开销巨大——ViewCrafter在单张A100 GPU上处理33个视角需耗时约35分钟（Table 3），难以满足交互式创作场景的实时性需求。

更根本的瓶颈在于**训练数据的缺失**：自然图像领域有海量的照片-多视图配对数据，但草图-多视图配对数据几乎不存在。这迫使已有方法要么绕道照片域，要么在缺乏配对监督的条件下隐式学习，难以建立从扭曲笔画到空间一致场景的直接映射。

### 本文动机：端到端几何感知的草图到多视图生成

本文的核心动机在于回答一个开放性问题：**能否让生成模型直接“读懂”草图中的空间意图，并在单次推理中输出几何一致的多视角场景？**

实现这一目标需要在三个维度上突破现有范式：

1. **流水线重构**：摒弃两阶段翻译-生成的中间瓶颈，构建从草图到多视图的端到端单阶段模型，使梯度信号能够贯穿整个生成过程，从像素级真实感监督中隐式学习草图到3D的映射。

2. **几何注入**：将相机参数显式编码进生成模型的注意力计算中，使模型“知道”不同视角之间的相对射影变换关系，而非仅依赖数据驱动的隐式关联。这要求设计轻量、可插拔的适配器模块，既能注入几何先验，又不破坏预训练视频扩散模型的生成能力。

3. **跨视角监督**：利用SfM从伪真值多视图数据中提取稀疏关键点对应，将其转化为注意力层的对比学习监督信号，显式教会模型哪些空间位置应跨视角相互关注，从而在推理时自动维护几何一致性。

这三项设计协同作用，构成了本文提出的**CA3-Adapted Video DiT**框架：一个在预训练视频扩散Transformer中引入并行相机感知注意力适配器（CA3），并通过稀疏对应监督损失（CSL）训练的端到端草图到多视角生成系统。



## 核心方法与创新机理

本文的核心创新在于将“草图→多视角3D场景”这一极具几何不确定性的任务，从一个脆弱的**两阶段流水线**（草图→照片→多视角）重构为一个**端到端的单阶段视频扩散框架**。这一重构并非简单的流程简化，而是通过三个相互协同的机制，将相机几何显式注入到生成过程中，从而解决了困扰两阶段方法的核心瓶颈：中间照片阶段的语义偏差与跨视角几何不一致。

### 创新一：从两阶段到单阶段的范式跃迁

现有方法（如 **SEVA** 与 **ViewCrafter**）遵循“先翻译后生成”的逻辑：首先使用 FLUX 等模型将草图转换为逼真的照片，再将该照片作为条件输入到多视角生成器中。这一设计存在根本性缺陷——草图到照片的翻译过程不可避免地引入语义偏差和纹理幻觉，这些误差会在第二阶段被放大，导致生成的多视角图像在结构上相互矛盾。

本文方法（**CA3-Adapted Video DiT**）直接以草图为唯一输入，在单次去噪过程中同时生成全部 N 个视角的图像（Fig. 2(a)）。这一设计消除了中间照片阶段的误差传播路径，使模型能够端到端地学习从抽象笔触到空间一致场景的直接映射。定量结果表明：仅此流水线重构，便使 FID 从两阶段基线的 46.34（SEVA）和 48.22（ViewCrafter）降至 18.49，降幅超过 60%（Table 1）。

### 创新二：相机感知注意力适配器（CA3）——将几何注入注意力

单阶段流水线本身并不足以保证几何一致性。核心挑战在于：如何让一个预训练的视频扩散模型（**Wan 2.1**）理解各视角之间的相对射影变换关系？

本文的解决方案是**相机感知注意力适配器（CA3）**。在每个 DiT 块的自注意力层旁，并行插入一个轻量级的 CA3 适配器（仅增加约 2.7% 的参数量），其关键设计在于：

1. **PRoPE 编码**：将每个视角的相机参数构建为射影矩阵 $\mathbf{P}^{(n)} = [\mathbf{K} \mathbf{\Lambda_1^0}] \cdot (\mathbf{T}^{(n)})^{-1}$，并通过投影旋转位置编码（PRoPE）将其注入到注意力分数的计算中。这使得注意力机制能够感知不同视角之间的相对几何关系——例如，左侧视图的某个像素应当更多地关注前视图中与之空间对应的区域。

2. **并行零初始化分支**：CA3 作为原始自注意力的并行分支存在，遵循零初始化范式，使得训练初期模型行为与冻结的预训练主干一致，随后逐步学习几何偏置。

消融实验提供了决定性证据（Table 2, row b）：移除 CA3 后，PSNR 从 12.169 骤降至 5.026，FID 从 18.49 恶化至 266.06。这表明**没有显式几何偏置，模型完全无法从草图中生成有意义的视图**，CA3 是几何推理的基石。

### 创新三：稀疏对应监督损失（CSL）——教会模型“哪里该关注”

CA3 赋予了模型处理相机几何的能力，但并未直接告诉模型**哪些空间位置应在不同视图间相互对应**。本文通过引入**对应监督损失（CSL）** 填补了这一空白。

具体而言，CSL 在 CA3 适配器的查询-键（Q-K）投影上施加稀疏 InfoNCE 对比损失：

$$\mathcal{L}_{\mathrm{corr}} = -\frac{1}{M} \sum_{i=1}^{M} w_i \cdot \log \frac{\exp(\mathbf{q}_i^{\top} \mathbf{k}_i^{+} / \tau)}{\exp(\mathbf{q}_i^{\top} \mathbf{k}_i^{+} / \tau) + \sum_{j=1}^{N_{\mathrm{neg}}} \exp(\mathbf{q}_i^{\top} \mathbf{k}_j^{-} / \tau)}$$

其中正样本对 $(\mathbf{q}_i, \mathbf{k}_i^{+})$ 来自 COLMAP 的 SfM 跨视角关键点匹配（Fig. 4），负样本则从其他空间位置随机采样。该损失仅在 DiT 的特定层（{10, 15, 20, 25}）上计算，以课程调度权重 $\lambda_{\mathrm{corr}}$ 与流匹配损失联合优化。

CSL 的效果在消融实验中得到了清晰验证（Table 2, row d）：移除 CSL 后，几何一致性指标 Corr-Acc 从 0.199 降至 0.175，而注意力可视化（Fig. 6）显示，无 CSL 的模型其注意力图变得扩散且非结构化，缺乏明确的空间聚焦。这表明 **CSL 是驱动模型学习跨视角几何对应关系的关键信号**。

### 创新四：自动化训练数据构建管线

上述方法面临一个根本性障碍：不存在配对的“草图-多视角”训练数据集。本文设计了一条全自动的数据构建管线（Fig. 3），通过**多种子生成→语义分割→mIoU 最佳种子选择→多视角合成→质量过滤**五个步骤，从 FS-COCO 数据集的草图和文本描述出发，构建了包含 9,222 个高质量样本的 S2WV 数据集。其中最佳种子选择策略 $I^{*} = \arg\max_{i\in\{1..5\}}\mathrm{mIoU}(\mathcal{M}_{s},\mathcal{M}_{g,i})$ 确保了生成的前视图与草图在语义布局上高度一致，为后续多视角合成提供了可靠的基础。

### 创新协同效应

上述四个创新并非孤立存在，而是形成了相互增强的闭环：CA3 提供了处理几何的能力，CSL 提供了学习几何对应关系的监督信号，单阶段流水线消除了中间翻译的误差累积，而自动数据管线则为这一切提供了训练基础。消融实验（Table 2）证实，移除任何一个组件都会同时损害单视图质量（PSNR, FID）和跨视图一致性（Corr-Acc），验证了这些创新之间的协同依赖性。



本文提出一种端到端的单阶段框架，以单张自由手绘草图和文本描述为输入，直接生成覆盖完整360°方位角、多个仰角的N个几何一致的真实感多视角图像。该框架的核心思想是将多视角生成任务重新表述为视频序列建模问题，并通过注入显式相机几何偏置和跨视角对应监督，迫使模型从扭曲的2D笔画中推断出空间一致的3D场景表达。

### 输入输出流

系统接收两个输入：
- **自由手绘草图** $S$：具有高度几何不确定性的单张2D笔画图像，来自FS-COCO等数据集。
- **目标相机位姿**：$N$个预定义的相机视角，由方位角 $\theta$ 和仰角 $\phi$ 参数化，覆盖完整的观察球面。

输出为$N$张分辨率为480×480的真实感视图，所有视图在单次前向去噪过程中联合生成，无需中间照片转换、参考照片或逐场景优化。

### Pipeline概览

如图2(a)所示，整体pipeline由三个关键阶段组成：

1. **草图编码**：输入草图经过VAE编码器映射到潜空间，与文本嵌入和时间步信息一同输入视频扩散Transformer骨干网络。

2. **联合去噪生成**：编码后的潜变量通过改造后的视频扩散Transformer（Wan 2.1）进行去噪。该Transformer的每个块包含两个并行的注意力分支：
   - **自注意力分支**：配备LoRA适配器（秩16），负责从自然视频域到草图域的适应。
   - **相机感知注意力适配器（CA3）**：并行分支，通过射影旋转位置编码（PRoPE）将相对相机几何注入注意力计算，赋予模型显式的多视角投影推理能力。

3. **多视角解码**：去噪后的潜变量经VAE解码器恢复为$N$个视角的真实感图像。

### 关键模块关系

框架的三个核心创新模块形成协同关系：

- **帧复制（Frame Replication）**：将每个视角重复4次（$N \to 4N+1$），以规避VAE的4倍时域压缩导致的跨视角信息丢失。消融实验（Table 2, row f）表明，移除该机制使FID翻倍至42.54。

- **CA3适配器**：在冻结的骨干网络基础上，以零初始化并行分支的形式引入，仅增加约2.7%的参数量（~35.4M）。每个适配器具有8倍瓶颈结构和2个注意力头，通过PRoPE将相机外参矩阵 $\mathbf{T}^{(n)} = [\mathbf{R}^{(n)} \, \mathbf{t}^{(n)}] \in SE(3)$ 编码为射影矩阵 $\mathbf{P}^{(n)}$，直接修改注意力分数以反映视角间的几何关系。消融实验（Table 2, row b）表明，移除CA3导致PSNR从12.169骤降至5.026，FID从18.49恶化至266.06，证实了显式几何偏置的不可或缺性。

- **对应监督损失（CSL）**：在训练阶段，利用COLMAP SfM从伪真值多视图图像中提取稀疏关键点对应关系，在CA3适配器的查询-键投影上施加稀疏InfoNCE对比损失。该损失应用于第{10, 15, 20, 25}层，教会模型哪些空间位置应跨视角相互关注。消融实验（Table 2, row d）表明，移除CSL后Corr-Acc从0.199降至0.175，且注意力图变得扩散非结构化（Fig. 6），验证了对应监督对实现几何一致性的核心作用。

### 训练数据构建

由于不存在配对的草图-多视角数据集，本文提出自动化数据构建流水线（Fig. 3）：
1. 对每个草图生成5个种子图像，通过mIoU与草图分割掩码比较选取最佳种子：$I^{*} = \arg\max_{i \in \{1..5\}} \mathrm{mIoU}(\mathcal{M}_s, \mathcal{M}_{g,i})$。
2. 使用Qwen Image Edit Angles从选定种子合成多视角图像。
3. 经质量过滤后得到9,222个高质量样本（8,304训练/918测试）。

### 训练目标

总损失函数为流匹配损失与课程调度加权的对应损失之和：
$$\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{flow}} + \lambda_{\mathrm{corr}} \cdot \mathcal{L}_{\mathrm{corr}}$$

其中流匹配损失 $\mathcal{L}_{\mathrm{flow}} = \mathbb{E}_{t,\mathbf{z}_0,\epsilon}[\|\mathbf{v}_{\theta}(\mathbf{z}_t, t, \mathbf{c}) - (\mathbf{z}_0 - \epsilon)\|^2]$ 负责基本生成质量，CSL损失通过课程学习策略逐步引入，以在训练后期强化几何一致性。

### 补充图表

![[assets/figures/papers/paper_list_l16_https_arxiv_org_abs_2604_14302/figures/002_Figure_2.jpg]]
*Figure 2: Method overview. (a) A freehand sketch is encoded then denoised by a video DiT augmented with our CA3. All N views are generated in a single forward denoising process. (b) Each DiT block contains a self-attention with LoRa and a parallel CA3 to inject relative camera geometry. (c) During training, SfM correspondences from pseudo ground-truth views supervise the CA3 query–key projections via a sparse InfoNCE loss. Dashed boxes: frozen modules*



### 3.1 视频扩散Transformer骨干与帧复制

本方法构建于预训练视频扩散Transformer **Wan 2.1**（约1.3B参数）之上，将其重新用于多视角序列建模。给定一幅自由手绘草图 $S$ 和 $N$ 个目标相机位姿，模型在单次前向去噪过程中联合生成 $N$ 幅几何一致的逼真视图。

标准DiT块的自注意力计算为：

$$\mathrm{Attn}(\mathbf{Q},\mathbf{K},\mathbf{V}) = \mathrm{softmax}\left(\frac{\mathbf{Q}\mathbf{K}^{\top}}{\sqrt{d}}\right)\mathbf{V} \quad \text{(1)}$$

训练采用流匹配范式，最小化速度场误差：

$$\mathcal{L}_{\mathrm{flow}} = \mathbb{E}_{t,\mathbf{z}_{0},\epsilon}\left[\|\mathbf{v}_{\theta}(\mathbf{z}_{t},t,\mathbf{c}) - (\mathbf{z}_{0} - \epsilon)\|^{2}\right] \quad \text{(2)}$$

其中 $\mathbf{z}_t$ 为时间步 $t$ 的噪声隐变量，$\mathbf{c}$ 为条件信号（草图与文本提示），$\mathbf{v}_\theta$ 为DiT预测的速度场。

**帧复制（Frame Replication）**：由于VAE的4倍时域压缩会将每帧压缩为4帧一组，直接输入 $N$ 个视角会导致视角信息在时域压缩中丢失。因此，将每个视角重复4次，形成 $4N+1$ 帧的序列（额外一帧为条件草图帧），确保多视角高频细节得以保留。消融实验（Table 2, row f）证实，移除帧复制后FID从18.49翻倍至42.54。

### 3.2 相机感知注意力适配器（CA3）

为赋予冻结的DiT骨干显式处理多视角投影几何的能力，在每个DiT块的自注意力旁并联一个轻量级**相机感知注意力适配器（CA3）**。该适配器采用零初始化的并行分支范式，仅增加约35.4M参数（占骨干的约2.7%）。

**PRoPE位置编码**：CA3的核心是将相对相机几何注入注意力计算。对于第 $n$ 个视角，定义其相机到世界外参矩阵：

$$\mathbf{T}^{(n)} = [\mathbf{R}^{(n)} \; \mathbf{t}^{(n)}] \in SE(3) \quad \text{(4)}$$

构建射影矩阵：

$$\mathbf{P}^{(n)} = [\mathbf{K} \; \mathbf{\Lambda_1^0}] \cdot (\mathbf{T}^{(n)})^{-1} \quad \text{(5)}$$

其中 $\mathbf{K}$ 为共享内参矩阵，$\mathbf{\Lambda_1^0}$ 为将世界原点映射到齐次坐标的增广矩阵。**PRoPE**（Projective Rotary Position Encoding）利用 $\{\mathbf{P}^{(n)}\}_{n=1}^{N}$ 将不同视角间的相对射影变换编码为旋转位置嵌入，直接修改注意力分数中的查询-键内积，使模型能够感知“两个空间位置在不同视角下的投影关系”。

每个DiT块的前向计算融合自注意力和相机感知注意力：

$$\mathbf{h}_{\ell}^{\prime} = \mathbf{h}_{\ell} + \mathcal{A}_{\ell}^{\mathrm{self}}(\mathbf{h}_{\ell}) + \mathcal{A}_{\ell}^{\mathrm{cam}}(\mathbf{h}_{\ell}, \{\mathbf{P}^{(n)}\}_{n=1}^{N}) \quad \text{(6)}$$

其中 $\mathcal{A}_{\ell}^{\mathrm{self}}$ 为带LoRA（秩16，约5.9M参数）的自注意力，$\mathcal{A}_{\ell}^{\mathrm{cam}}$ 为CA3的相机感知注意力。每个CA3适配器具有8倍瓶颈结构和2个注意力头。

**消融证据**：移除CA3模块后，PSNR从12.169骤降至5.026，FID从18.49恶化至266.06（Table 2, row b），证实相机感知注意力对几何推理是**必要条件**——没有显式几何偏置，模型完全无法从扭曲的2D笔画中推断有意义的3D结构。

### 3.3 对应监督损失（CSL）

CA3提供了处理相机几何的**机制**，但模型仍需被**教会**哪些空间位置应跨视角相互关注。为此，引入**对应监督损失（CSL）**，利用训练数据的SfM稀疏对应点作为显式监督信号。

**监督信号构建**：对伪真值多视图运行COLMAP，提取跨视角的SfM关键点匹配对，构成对应集合：

$$\mathcal{C} = \{ (q_i, k_i, w_i) \}_{i=1}^{M}$$

其中 $q_i$ 为查询视角中某空间patch的索引，$k_i$ 为目标视角中匹配patch的索引，$w_i$ 为置信度权重。

**稀疏InfoNCE损失**：在CA3的查询-键投影上施加对比损失，从DiT层子集 $\mathcal{U} = \{10, 15, 20, 25\}$ 提取查询嵌入 $\mathbf{q}_i$ 和键嵌入 $\mathbf{k}_i$，计算：

$$\mathcal{L}_{\mathrm{corr}} = -\frac{1}{M} \sum_{i=1}^{M} w_i \cdot \log \frac{\exp(\mathbf{q}_i^{\top} \mathbf{k}_i^{+} / \tau)}{\exp(\mathbf{q}_i^{\top} \mathbf{k}_i^{+} / \tau) + \sum_{j=1}^{N_{\mathrm{neg}}} \exp(\mathbf{q}_i^{\top} \mathbf{k}_j^{-} / \tau)} \quad \text{(7)}$$

其中 $\mathbf{k}_i^{+}$ 为正样本键（匹配的跨视角patch），$\mathbf{k}_j^{-}$ 为同一目标视图中的随机负样本键，$\tau$ 为温度参数。该损失显式强制匹配的跨视角空间位置在CA3的查询-键投影空间中彼此吸引，而非匹配位置相互排斥。

**总训练目标**：

$$\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{flow}} + \lambda_{\mathrm{corr}} \cdot \mathcal{L}_{\mathrm{corr}} \quad \text{(8)}$$

其中 $\lambda_{\mathrm{corr}}$ 采用课程调度策略，训练初期较小以避免干扰流匹配收敛，后期逐步增大以强化几何一致性。

**消融证据**：移除CSL后，Corr-Acc从0.199降至0.175（Table 2, row d），且注意力可视化（Fig. 6）显示注意力图变得扩散非结构化，缺乏空间聚焦。这证实CSL是将CA3的几何**能力**转化为实际几何**行为**的关键——它教会模型在注意力空间中建立正确的跨视角空间对应关系。

### 补充图表

![[assets/figures/papers/paper_list_l16_https_arxiv_org_abs_2604_14302/figures/004_Figure_4.jpg]]
*Figure 4: SfM correspondences across views. Each correspondence image shows two views with colored lines connecting matched keypoints identified by Structure-from-Motion (COLMAP). The view angles (azimuth, elevation) for each pair are indicated above the correspondence visualizations. These correspondences serve as supervision targets for our camera-aware attention adapters (Sec. 3.4)*

![[assets/figures/papers/paper_list_l16_https_arxiv_org_abs_2604_14302/figures/008_Figure_6.jpg]]
*Figure 6: Attention correspondence visualisation. Query pixel (red dot) in the front view; heatmaps show attention at layer 20 over three target viewpoints. Left: with correspondence supervision. Right: without (ablation Tab. 2 row b)*



## 实验与关键发现

### 主实验结果

我们在自建的S2MV测试集（477个样本，每样本33个视角，3个随机种子）上对提出的单阶段方法与两个两阶段基线SEVA和ViewCrafter进行了全面对比。**Table 1** 汇总了六项指标的定量结果。

![[assets/figures/papers/paper_list_l16_https_arxiv_org_abs_2604_14302/figures/005_Table_1.jpg]]
*Table 1: Quantitative comparison on S2MV test set (477 samples, N=33 views each, 3 seeds). Our single-stage method is compared against two-stage baselines that first translate the sketch to a photograph via FLUX.2-dev*

**真实感与感知质量。** 本文方法在FID上达到18.49，相比SEVA（46.34）和ViewCrafter（48.22）分别降低60.1%和61.7%，表明生成图像的真实感显著优于两阶段基线。在LPIPS上，本文方法（0.632）同样优于SEVA（0.705）和ViewCrafter（0.680），说明生成视图的感知特征更接近真值。CLIP-I达到0.828，比SEVA（0.756）和ViewCrafter（0.739）分别高出9.5%和12.0%，验证了生成内容与输入草图-文本对在语义层面的一致性。

**几何一致性。** Corr-Acc是衡量跨视角结构一致性的核心指标。本文方法达到0.199，较SEVA（0.161）提升23.6%，较ViewCrafter（0.136）提升46.3%。这一优势源于CA3模块中PRoPE编码的显式相机几何注入与CSL损失的联合作用——前者将相对射影变换融入注意力计算，后者通过稀疏InfoNCE损失强制模型学习跨视角的空间对应关系。

**像素级重建精度。** 在PSNR（12.169 vs. 11.310/10.823）和SSIM（0.302 vs. 0.265/0.249）上，本文方法同样取得最优。值得注意的是，两阶段基线在PSNR和SSIM上的差距相对较小（SEVA的PSNR为11.310，仅比本文低0.859），但在FID和Corr-Acc上差距悬殊，这暗示两阶段方法的失败模式并非简单的像素偏移，而是结构性的几何错乱和纹理失真——这正是单阶段联合生成与显式几何注入所解决的问题。

**推理效率。** **Table 3** 展示了在单张A100 GPU上生成33个视角的端到端耗时。本文方法仅需约50秒，而SEVA（FLUX照片生成+多视图扩散）约需3.1分钟，ViewCrafter（FLUX+DUSt3R点云估计+逐视角视频扩散）更长达约35分钟。本文方法分别实现了3.7倍和42倍的推理加速。效率优势来自两个层面：(i) 单阶段去噪一次性生成所有视角，无需中间照片生成和逐视角迭代；(ii) CA3适配器仅增加2.7%参数，计算开销极小。

**定性对比。** **Figure 5** 展示了三个典型场景的8个方位角视图（0°–315°，45°间隔）。在“a stone building”场景中，本文方法在背视图（180°）保持了建筑立面的结构完整性，而SEVA和ViewCrafter均出现明显的几何扭曲和纹理塌缩。在“a wooden table”场景中，本文方法在侧面视角（90°、270°）准确还原了桌腿的相对位置和比例，两阶段基线则出现了桌腿错位或消失的现象。更多定性对比见 **Figure 8** 和 **Figure 9**。

### 消融实验

**Table 2** 系统评估了各模块的贡献。完整模型（行a）作为基准，逐一移除关键组件。

**移除CA3模块（行b）。** 这是影响最剧烈的消融。PSNR从12.169骤降至5.026（降幅58.7%），FID从18.49恶化至266.06（增幅超13倍），Corr-Acc从0.199降至0.157。这些数字表明，没有相机感知注意力适配器，模型完全丧失了生成有意义多视图的能力——扩散过程退化为近似随机噪声，无法从草图笔触中推断任何空间结构。这证实了PRoPE编码的相对射影几何信息是模型理解“不同视角间空间关系”的**必要条件**。

**移除CSL对应监督损失（行d）。** Corr-Acc从0.199降至0.175（降幅12.1%），PSNR从12.169降至11.453，FID从18.49升至25.15。虽然降幅不如移除CA3剧烈，但CSL的移除直接削弱了跨视角几何一致性。**Figure 6** 的注意力可视化进一步揭示了机制层面的差异：有CSL时，前视图的查询像素（红色点）在侧视图和后视图的注意力热力图呈现聚焦的、与空间对应位置一致的激活模式；移除CSL后，注意力图变得扩散且无结构，模型无法建立跨视角的空间对应关系。这验证了CSL通过稀疏InfoNCE损失**教会模型哪些空间位置应跨视角相互关注**的核心作用。

**移除LoRA域适应（行c）。** FID从18.49升至28.70，PSNR降至11.188。LoRA（秩16，约5.9M参数）承担了从预训练视频分布到草图-多视图分布的域迁移任务。移除后模型仍能生成基本结构（PSNR降幅有限），但纹理细节和真实感显著下降，说明LoRA主要影响生成质量而非几何推理。

**移除帧复制（行f）。** FID翻倍至42.54，PSNR降至9.982。Wan 2.1 VAE的4倍时域压缩会将33个视角压缩为仅8个潜在帧，导致严重的视角信息丢失。帧复制（每视图重复4次，33→132帧）是保留多视图高频细节的关键工程手段。

**移除PRoPE编码（行e）。** 用标准RoPE替代PRoPE后，Corr-Acc降至0.177，PSNR降至11.694。这表明PRoPE编码的射影变换信息比标准位置编码更有效地指导了跨视角注意力。

### 失败模式分析

尽管本文方法在定量和定性评估中均显著优于基线，但仍存在以下失败模式：

1. **重度遮挡场景的后视图退化。** 当场景包含多个相互遮挡的物体时（如密集排列的家具），后视图（180°附近）可能产生模糊纹理或幻觉内容。这是因为训练数据中此类复杂排列样本不足（仅8,304个训练样本），且多视角真值由图像编辑模型生成，本身可能包含遮挡处理的不一致性。

2. **光照与纹理漂移。** 在部分样本中，不同视角间的光照方向和材质高光存在轻微不一致。这源于训练数据由Qwen Image Edit Angles生成，而非来自真实3D资产渲染，真值本身携带了光照不一致的伪影。

3. **分辨率限制。** 当前训练和推理分辨率均为480×480，因为并行处理33个视角需消耗大量GPU内存（8×A100，每卡80GB）。在更高分辨率下，部分细粒度纹理（如文字、规则图案）可能出现模糊。

### 泛化能力

**Figure 7** 展示了在训练分布外草图域上的零样本泛化结果。在TU-Berlin物体草图（风格化线稿，与FS-COCO的自由手绘风格显著不同）上，本文方法仍能生成几何一致的多视角视图，表明CA3模块学习的相机几何推理能力具有跨域迁移性。在InkScenes密集纹理场景草图上，方法同样保持鲁棒性，未出现严重的结构崩溃。这归因于：(i) 冻结的Wan 2.1骨干保留了大规模视频预训练的先验；(ii) CA3适配器仅编码相机几何，与草图风格解耦。

### 补充图表

![[assets/figures/papers/paper_list_l16_https_arxiv_org_abs_2604_14302/figures/007_Table_2.jpg]]
*Table 2: Ablation study. We remove each contribution independently. Row (a) is the full model. Removing any single component degrades both per-view quality and geometric consistency, confirming that the contributions are mutually reinforcing*

![[assets/figures/papers/paper_list_l16_https_arxiv_org_abs_2604_14302/figures/010_Table_3.jpg]]
*Table 3: Inference efficiency. Wall-clock time per sample on a single A100 GPU (N =33 views)*

![[assets/figures/papers/paper_list_l16_https_arxiv_org_abs_2604_14302/figures/006_Figure_5.jpg]]
*Figure 5: Qualitative comparison of multi-view generation from sketches. For each example we show the input sketch with its text prompt (left) and eight azimuth views (0◦–315◦ at 45◦ intervals) generated by each method. GT: ground-truth views; Ours: our single-pass sketch-to-multiview method; VC: ViewCrafter; SEVA: Stable Video Diffusion. Additional comparisons are provided in the supplementary material (Sec. A)*

![[assets/figures/papers/paper_list_l16_https_arxiv_org_abs_2604_14302/figures/009_Figure_7.jpg]]
*Figure 7: Generalisation to unseen sketch domains. 12 views per sketch at four elevations. (Top) TU-Berlin object sketches [11]: consistent multi-view output despite a distinctly different sketch style. (Bottom) InkScenes [43]: robust to dense, textured scene compositions unseen during training*

![[assets/figures/papers/paper_list_l16_https_arxiv_org_abs_2604_14302/figures/001_Figure_1.jpg]]
*Figure 1: Sketch-to-Multi-View generation. Given a single freehand sketch and a text caption, our method generates geometrically consistent multi-view images spanning a full 360◦ azimuth orbit at four different elevations. Top three rows: in-domain examples from FS-COCO [9]. Bottom two rows: zero-shot generalisation to unseen sketch domains (TU-Berlin [11] and InstantStyle [43])*

![[assets/figures/papers/paper_list_l16_https_arxiv_org_abs_2604_14302/figures/011_Figure_8.jpg]]
*Figure 8: Additional qualitative comparison. Same format as Fig. 5: input sketch with text prompt (left) and eight azimuth views generated by each method*

![[assets/figures/papers/paper_list_l16_https_arxiv_org_abs_2604_14302/figures/012_Figure_9.jpg]]
*Figure 9: Additional qualitative comparison. Same format as Fig. 5: input sketch with text prompt (left) and eight azimuth views generated by each method*

![[assets/figures/papers/paper_list_l16_https_arxiv_org_abs_2604_14302/figures/003_Figure_3.jpg]]
*Figure 3: S2WV dataset generation pipeline. (a) Multi-seed image generation from sketch and caption. (b) Segmentation of sketch and generated images. (c) Best seed selection via mIoU. (d) Multi-view synthesis from the selected image. (e) Dataset curation yields 9,222 samples. More details in Sec. 3.2*



## 定位与知识库关联

### 任务定位：从草图到多视角3D场景生成

本文聚焦一个尚未被充分探索的问题：仅以单张自由手绘草图和文本描述为条件，生成几何一致且逼真的多视角场景图像（Sketch-to-Multi-View, S2MV）。该任务处于草图理解、多视角生成与3D场景推理的交汇点，其核心瓶颈在于：自由手绘草图具有高度的几何不确定性和抽象性，缺乏纹理、光照和精确的深度线索，而模型必须从中推断出完整的相机几何和跨视角结构一致性。

### 与现有方法的关系

#### 两阶段基线：草图→照片→多视角

当前最直接的基线方法是两阶段流水线：先利用预训练的图像生成模型（如FLUX）将草图转换为逼真的参考照片，再将该照片作为输入送入多视角生成器。本文比较的两个代表性基线为：

- **SEVA**（Stable Virtual Camera）：通过FLUX.2-dev将草图转为照片后，利用潜在扩散模型生成多视角新视图。
- **ViewCrafter**：草图转照片后，通过DUSt3R进行点云估计，再利用视频扩散模型逐步生成每个视角。

两阶段范式存在根本性缺陷：中间照片生成阶段可能引入与原始草图语义不一致的虚假纹理或结构，且两阶段独立优化，相机几何信息无法从草图端到端地传递，导致跨视角结构不一致和误差累积。

#### 本文方法的突破：单阶段端到端生成

本文提出的**CA3-Adapted Video DiT with Sparse Correspondence Supervision**方法，将多视角生成重新定义为单阶段去噪过程：草图直接作为条件输入，N个视角在视频扩散Transformer的一次前向去噪中联合生成，彻底消除了中间照片生成阶段。这一设计使相机几何可以从草图端到端地学习，避免了语义漂移和误差累积。

#### 与多视角/3D生成领域的关系

更广泛地，多视角生成和3D重建领域的工作可沿以下维度定位：

| 维度 | 典型方法 | 输入模态 | 本文位置 |
|------|----------|----------|----------|
| 稀疏视图重建 | DUSt3R, MASt3R | 多张照片 | 正交：本文仅需草图 |
| 单图到多视角 | Zero-1-to-3, ViewCrafter | 单张照片 | 本文处理更抽象的草图 |
| 文本到多视角 | MVDream, VideoMV | 文本描述 | 本文引入空间精确的草图控制 |
| 草图到3D | Sketch2Model, 3Doodle | 草图+3D监督 | 本文无需3D资产，仅需2D多视角 |
| 视频扩散模型 | Wan 2.1, CogVideoX | 自然视频 | 本文将其适配为多视角序列建模 |

本文的核心贡献在于填补了“草图→多视角”这一空白，并通过相机感知注意力机制显式建模跨视角几何关系，区别于以往依赖隐式特征共享或后处理优化的方法。

### 方法适用边界与局限

#### 数据规模与多样性限制

训练数据集通过自动化流水线生成，包含8,304个训练样本（9,222个样本中划分出训练集），数量级远小于基线方法所用的数百万级视频数据。这限制了场景的多样性：训练样本主要来自FS-COCO数据集中的对象和简单场景，对于复杂遮挡、多对象排列或非典型视角的场景，模型可能产生模糊或幻觉内容，尤其是后视图区域。

#### 真值质量约束

多视角训练视图由图像编辑模型（Qwen Image Edit Angles）生成，而非来自真实3D资产渲染。这意味着训练真值可能包含：
- 光照不一致：不同视角的光源方向和强度可能不匹配
- 纹理漂移：跨视角的纹理细节可能发生非物理变化
- 几何伪影：编辑模型可能引入不符合真实3D投影的形变

这些伪影会限制生成质量的上限，并使Corr-Acc等几何一致性指标难以达到更高水平。

#### 分辨率与计算资源瓶颈

训练分辨率限制在480×480，因为并行处理N=33个视图需要大量GPU内存（8×A100）。更高分辨率需要梯度检查点或模型并行等工程优化，目前尚未实现。

#### 相机轨迹约束

当前方法假设虚拟相机围绕场景中心在半球面上采样（固定半径，变化方位角和仰角），不支持任意6-DoF相机运动或自由视角插值。相机轨迹的多样性受限于训练数据的采样策略。

### 开放问题与未来方向

1. **数据流水线扩展**：如何生成更多样、更复杂的场景样本，特别是处理重度遮挡的多对象排列和室内外复杂场景？能否利用3D资产渲染（如Objaverse）结合草图风格迁移来构建更高质量的训练数据？

2. **真值质量提升**：在缺乏真实3D场景标注的情况下，如何减少由生成的真值带来的伪影？可能的途径包括引入多视角一致性正则化、利用3D重建模型（如DUSt3R）进行几何验证，或采用对抗训练判别真值伪影。

3. **分辨率与效率权衡**：能否通过梯度检查点、模型并行或序列并行突破GPU内存限制，实现更高分辨率的训练和生成？低分辨率训练+高分辨率微调的两阶段策略是否可行？

4. **更大规模训练的增益**：该方法在更大规模训练数据（如百万级草图-多视角对）下的性能增益如何？Corr-Acc和FID是否随数据量呈对数线性改善，还是会遇到由草图固有模糊性决定的上限？

5. **相机控制自由度**：如何扩展方法以支持任意6-DoF相机轨迹和自由视角插值？这需要重新设计相机参数编码策略和训练数据采样方案。

6. **与3D重建的融合**：生成的几何一致多视角图像能否直接用于3D高斯泼溅或NeRF重建？若能，则可将方法定位为“草图到3D资产”流水线的核心前端模块，具有重要的应用价值。



## 原文 PDF

![[paperPDFs/arxiv_2026/Geometrically_Consistent_Multi_View_Scene_Generation_from_Freehand_Sketches.pdf]]
