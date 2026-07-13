---
title: "Motion 3-to-4: 3D Motion Reconstruction for 4D Synthesis"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Motion_3_to_4_3D_Motion_Reconstruction_for_4D_Synthesis.pdf
project_link: https://motion3-to-4.github.io/
code_link: null
aliases:
- M34
- M343MR4S
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 将4D合成分解为静态3D形状生成和基于参考网格的运动重建，通过把运动估计表示为表面点与视频像素间的对应关系学习，规避了直接生成完整4D动态对大数据的需求。
primary_logic: 借助一个静态参考网格（可取自生成模型或用户提供）提供稳定的几何锚点，将动态4D问题简化为从单目视频中估计每帧的3D运动流，由此实现对可见与遮挡区域的完整几何恢复。
claims:
- 框架将4D生成分解为静态3D形状编码和动态运动重建，并利用参考网格估计每帧的运动流。
- 运动重建被转化为表面点与视频像素的对齐问题，无需后处理对齐。
- 本方法（含真值网格）在 Motion-80 数据集上显著优于所有基线，Chamfer Distance 达 0.0437，F-Score 达 0.6774。
- 在 Consistent4D 基准上，本方法在 LPIPS、CLIP、DreamSim 等外观指标上均取得最优。
---

# Motion 3-to-4: 3D Motion Reconstruction for 4D Synthesis

> [!tip] 核心洞察
> 借助一个静态参考网格（可取自生成模型或用户提供）提供稳定的几何锚点，将动态4D问题简化为从单目视频中估计每帧的3D运动流，由此实现对可见与遮挡区域的完整几何恢复。

| 字段 | 内容 |
|------|------|
| 中文题名 | Motion 3-to-4：面向4D合成的3D运动重建 |
| 英文题名 | Motion 3-to-4: 3D Motion Reconstruction for 4D Synthesis |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Chen_Motion_3-to-4_3D_Motion_Reconstruction_for_4D_Synthesis_CVPR_2026_paper.html) · [Project](https://motion3-to-4.github.io/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Motion 3-to-4 |
| Dataset | Motion-80, Consistent4D |

> [!tip] 效果简介
> - Motion-80 (short sequences) 上，Chamfer Distance (CD) ↓ 0.1113 (outperforms all baselines)。
> - Motion-80 (short sequences, with GT mesh) 上，Chamfer Distance (CD) ↓ 0.0437 (outperforms all baselines)；F-Score ↑ 0.6774 (outperforms all baselines)。
> - Consistent4D 上，LPIPS ↓ 0.1455 (outperforms all baselines)。

## 概要

**Motion 3-to-4** 提出了一种面向单目视频的 4D 动态内容合成框架，其核心思路是将原本高度不适定的 4D 生成问题分解为两个更易处理的子任务：静态 3D 形状生成与动态运动重建。该分解策略的关键洞察在于，借助一个静态参考网格（可来自生成模型或用户提供）作为稳定的几何锚点，将运动估计转化为表面点与视频像素之间的对应关系学习问题，从而规避了直接端到端生成完整 4D 动态序列对大规模高质量训练数据的依赖。

在方法定位上，该工作区别于现有的前馈式 4D 高斯回归方法（如 **L4GM**）、基于潜在扩散的视频到 4D 方法（如 **GVFD**），以及逐帧生成后做时序对齐的方案（如 **V2M4**）。Motion 3-to-4 将 4D 生成重新表述为“3D 形状合成 + 运动重建”的组合路径，通过预测每帧相对于参考姿态的 3D 顶点轨迹流来实现运动建模，并采用帧级 Transformer 架构支持任意长度视频输入，具备良好的可扩展性。

实验结果表明，该方法在 **Motion-80** 数据集上显著优于所有基线方法：当使用真值参考网格时，Chamfer Distance 达到 0.0437，F-Score 达到 0.6774；在 **Consistent4D** 基准上，外观指标同样取得最优（LPIPS 0.1455，CLIP 0.8609，DreamSim 0.1691）。此外，该方法还展示了在开放场景视频到 4D 合成以及运动迁移任务上的泛化能力。

当前方法的主要局限在于：对参考网格质量较为敏感，且缺乏显式拓扑约束，导致在物体部件切分不清或后续帧发生显著拓扑变化时可能出现顶点粘连或重建失败。



### 问题背景：4D动态内容的生成困境

从单目视频中重建动态3D内容——即4D合成——是计算机视觉与图形学中长期存在的核心挑战。该任务要求在仅给定一段二维视频的条件下，同时恢复物体的三维几何形状及其随时间演化的运动轨迹。这一问题的根本困难来自两个层面：

**数据瓶颈**：高质量4D动态训练数据极度稀缺。与静态3D资产（如Objaverse等大规模数据集）相比，带有精确时空标注的动态3D数据在规模、多样性和质量上均存在数量级差距。这直接导致基于变分自编码器（VAE）的运动潜在空间泛化能力弱，难以覆盖开放世界中丰富多变的运动模式。

**歧义性困境**：单目视频固有地存在几何与运动的双重歧义性——同一段二维观测可以对应无穷多种三维形状与运动的组合。同时恢复形状和运动是一个高度欠定的病态问题，尤其是在遮挡区域和纹理缺失区域。

### 现有方法的两条路径及其缺口

当前从单目视频进行4D合成的方法大致可分为两类，但各自存在结构性局限：

**逐帧生成 + 后处理对齐**：以 **V2M4** 为代表的方法先对每帧独立生成3D网格，再通过后处理步骤进行时序对齐。这种策略将运动一致性完全托付给后处理阶段，缺乏对运动本身的显式建模，导致时序抖动和几何不连贯。

**端到端4D回归**：以 **L4GM**（feedforward 4D Gaussian regression）和 **GVFD**（video-to-4D via latent diffusion over 3D Gaussians）为代表的方法直接从视频回归4D高斯表示或通过潜在扩散生成动态场景。这类方法将形状生成与运动预测耦合在单一前馈或扩散过程中，依赖大规模4D训练数据来隐式学习运动先验。在数据稀缺的现实约束下，其泛化能力受限，尤其在面对训练分布之外的新形状或复杂运动时表现退化。

两条路径的共同缺口在于：**缺乏一个稳定的几何锚点来解耦形状与运动**，使得运动估计可以在已知几何的约束下进行，而非同时从零推断两者。

### 本文动机：分解与锚定

本文的核心洞察是：**借助一个静态参考网格提供稳定的几何锚点，将动态4D问题简化为从单目视频中估计每帧的3D运动流**。这一参考网格可以来自预训练的3D生成模型，也可以由用户直接提供。

基于此，Motion 3-to-4 将4D合成分解为两个更易处理的部分：
- **静态3D形状编码**：从参考网格提取紧凑的几何表示；
- **动态运动重建**：将运动估计转化为表面点与视频像素间的对应关系学习问题。

这一分解策略的关键优势在于：
1. **规避数据瓶颈**：运动重建模块仅需学习“给定几何下如何运动”，而非同时学习“几何是什么”和“如何运动”，降低了对4D训练数据规模的依赖；
2. **显式处理遮挡**：以完整参考网格为基底，即使部分表面在当前视角被遮挡，仍可通过学习的对应关系推断其在三维空间中的运动轨迹；
3. **自然支持运动迁移**：形状与运动的解耦使得同一运动模式可以迁移到不同形状上，反之亦然。

通过将运动合成表述为表面点与视频像素的对齐问题（*“taking motion synthesis as an alignment problem between surface points and video pixels”*），该方法无需后处理对齐即可获得时序一致的4D资产，为后续的几何生成与运动重建的协同优化奠定了基础。



## 核心方法与创新机理

Motion 3-to-4 的核心创新在于将极具歧义性的 4D 生成问题**解耦为两个相对可控的子任务**：静态 3D 形状生成与动态运动重建。这一解耦并非简单的模块拆分，而是从根本上改变了问题的求解范式——将运动合成重新定义为**表面点与视频像素之间的对齐问题**（“taking motion synthesis as an alignment problem between surface points and video pixels”）。

### 关键范式转变：从“生成全部”到“锚定几何+估计运动流”

现有前馈式 4D 生成方法（如 **L4GM** 从多视角视频回归 4D Gaussian、**GVFD** 通过潜在扩散在 3D Gaussian 上生成运动）试图端到端地直接产出完整的 4D 动态表示。这类范式面临的核心瓶颈在于：高质量 4D 动态训练数据极度稀缺，导致基于 VAE 的运动潜在空间泛化能力薄弱。同时，单目视频固有的几何与运动歧义性使得同时恢复形状和运动极为困难。

Motion 3-to-4 的因果调控旋钮（causal knob）在于引入一个**静态参考网格**作为稳定的几何锚点。该参考网格可来自预训练 3D 生成器或用户直接提供，其作用是为运动估计提供确定的几何基底。在此基础上，方法仅需从单目视频中估计每帧的 3D 运动流——即表面点相对于参考姿态的位移轨迹。这一设计将问题的自由度从“同时推断形状与运动”压缩为“在已知几何上推断运动”，大幅降低了对大规模 4D 训练数据的依赖。

### Changed Slots：与基线方法的结构性差异

下表归纳了 Motion 3-to-4 在三个关键设计维度上与代表性基线的本质差异：

| 设计维度 | 基线方案 | Motion 3-to-4 方案 |
|---------|---------|-------------------|
| **4D 问题建模** | 端到端逐帧生成（V2M4）或全局运动生成（GVFD） | 解耦为 3D 形状生成 + 基于参考网格的逐帧运动重建 |
| **运动预测形式** | 预测 Gaussian 偏移量或全局潜在运动 | 预测每帧 3D 顶点轨迹，作为相对于参考姿态的运动流 |
| **序列处理机制** | 固定长度或逐实例优化 | 帧级 transformer，交替全局/局部注意力，支持任意长度视频 |

具体而言，**V2M4** 采用逐帧生成 3D 网格再进行事后时序对齐的策略，这导致帧间一致性天然不足。**L4GM** 和 **GVFD** 则在 3D Gaussian 表示上操作，其运动预测通常体现为对 Gaussian 原语的偏移量回归，缺乏显式的表面几何约束。Motion 3-to-4 的逐帧运动流预测直接建立在参考网格的采样点上，每一帧的输出点云与参考网格共享相同的拓扑结构，从而天然保证了时序一致性。

### 架构创新：帧级 Transformer 与交替注意力

为支持任意长度视频输入并对不同分辨率的网格保持鲁棒，方法设计了**帧级 transformer 架构**（“frame-wise transformer architecture that is robust to input meshes of varying resolution and supports flexible processing of videos of arbitrary length”）。其核心机制是**交替注意力**（Alternating Attention）：

1. **全局帧间注意力**：在所有帧的 token 之间进行注意力计算，捕获长程时序依赖；
2. **帧内自注意力**：在每帧内部进行注意力更新，精细化单帧的运动表示。

该设计使得模型既能感知全局运动趋势，又能保持对局部细节的建模能力。同时，通过将全局形状 token $\mathbf{Z}_{\mathbf{X}_0}$ 拼接到每一帧的 token 中，形状信息被持续注入到运动推理过程中，确保运动预测始终以参考几何为条件。

### 运动解码：从潜变量到密集运动流

运动解码器以参考网格的采样点 $\hat{\mathbf{X}}_0$ 为查询，通过交叉注意力从运动潜变量 $\mathbf{Z}_t$ 中提取对应信息，直接预测每帧的三维点位置 $\hat{\mathbf{X}}_t$：

$$\hat{\mathbf{X}}_t = \mathrm{MotionDecoder}(\hat{\mathbf{X}}_0, \mathbf{Z}_t)$$

训练采用预测点与真值点之间的均方误差损失进行密集监督：

$$\mathcal{L} = \frac{1}{M T} \sum_{i=1}^{M}\sum_{t=1}^{T} \|\hat{\mathbf{X}}_t^i - \mathbf{X}_t^i\|_2^2$$

这种逐点监督方式使得模型能够学习精细的表面到像素对应关系，从而在可见区域和遮挡区域均实现完整的几何恢复。

### 创新的外延能力

上述解耦设计天然衍生出两项重要的外延能力：

- **运动迁移**：由于运动重建与形状生成相互独立，可以将从一段视频中提取的运动流应用到完全不同的静态网格上，实现对艺术家创作的静态 3D 资产的动画化（“Motion 3-to-4 is the only approach capable of converting artist-created static 3D meshes into dynamic 4D sequences”）。
- **开放场景泛化**：将运动重建建模为表面到像素的对齐问题，使得方法对未见过的形状和运动模式具有较强的泛化能力，在真实拍摄视频和生成动画等开放场景中均能稳定工作（Figure 5）。



Motion 3-to-4 将病态的 4D 生成问题分解为**静态 3D 形状生成**与**动态运动重建**两个可解耦的子任务，核心洞察在于：利用一个静态参考网格（可来自生成模型或用户提供）作为稳定的几何锚点，将单目视频的每帧运动估计转化为表面点与视频像素间的对应关系学习问题。框架由两大组件构成：运动潜变量学习（motion latent learning）与运动解码（motion decoding）。

### 输入输出流

- **输入**：一段单目视频（任意帧数）及其对应的首帧参考网格 $\mathbf{X}_0$（可为真值网格或由 3D 生成器提供）。
- **输出**：每一帧 $t$ 的三维顶点轨迹 $\hat{\mathbf{X}}_t$，即相对于参考姿态的逐帧 3D 运动流，从而构成时序一致的 4D 动态资产。

### Pipeline 模块关系

1. **几何编码器 (Geometry Encoder)**：从参考网格采样 $N$ 个表面点 $\mathbf{X}_0$，通过可学习查询集 $\mathcal{A}$ 进行交叉注意力编码，生成紧凑的形状潜变量 $\mathbf{Z}_{\mathbf{X}_0}$：
   $$\mathbf{Z}_{\mathbf{X}_0} = \mathrm{CrossAttn}(\mathcal{A}, \mathrm{PointEmb}(\mathbf{X}_0))$$

2. **视频特征提取与时间嵌入 (Video Feature Extractor + Temporal Embedding)**：使用 DINOv2 提取每帧的 patch 级特征，注入时间位置嵌入后形成帧 tokens。随后将全局形状 token $\mathbf{Z}_{\mathbf{X}_0}$ 追加到每一帧 token 中，构成逐帧运动表示，从而支持任意长度视频输入。

3. **交替注意力模块 (Alternating Attention Blocks)**：通过 $L$ 层交替注意力对帧 tokens 进行更新——先在全局维度对所有帧执行全局注意力，再对每帧内部执行自注意力，生成各帧的运动感知潜变量：
   $$[\mathbf{Z}_0^{(\ell-\frac{1}{2})}, \dots, \mathbf{Z}_{T-1}^{(\ell-\frac{1}{2})}] = \mathrm{GlobalAttn}(\mathbf{Z}_0^{(\ell-1)}, \dots, \mathbf{Z}_{T-1}^{(\ell-1)})$$
   $$\mathbf{Z}_t^{(\ell)} = \mathrm{FrameAttn}(\mathbf{Z}_t^{(\ell-\frac{1}{2})}), \quad \forall t = 0,\dots,T-1$$

4. **运动解码器 (Motion Decoder)**：以参考网格采样点 $\hat{\mathbf{X}}_0$ 为查询，交叉注意力到对应帧的运动潜变量 $\mathbf{Z}_t$，解码出每帧的预测三维点位置：
   $$\hat{\mathbf{X}}_t = \mathrm{MotionDecoder}(\hat{\mathbf{X}}_0, \mathbf{Z}_t)$$

5. **训练监督**：采用预测点与真值点之间的均方误差损失进行密集监督：
   $$\mathcal{L} = \frac{1}{M T} \sum_{i=1}^{M}\sum_{t=1}^{T} \|\hat{\mathbf{X}}_t^i - \mathbf{X}_t^i\|_2^2$$

### 关键设计优势

- **帧级 transformer 架构**：交替的全局/局部注意力机制使模型对输入视频长度和网格分辨率具有高度鲁棒性与可扩展性。
- **表面-像素对齐范式**：将运动合成建模为表面点与视频像素的对齐问题，无需后处理对齐步骤，即可实现对可见与遮挡区域的完整几何恢复。
- **与生成模型的解耦**：框架可与任意预训练 3D 生成器组合，实现从艺术家创建的静态网格到 4D 动态序列的转换，以及跨源的**运动迁移**（motion retargeting）。

### 补充图表

![[assets/figures/papers/paper_list_l9_https_openaccess_thecvf_com_content_CVPR2026_html_Chen_Motion_3_to_4_3D/figures/003_Figure_2.jpg]]
*Figure 2: An overview of our Motion 3-to-4 framework for 4D synthesis. At the core of the framework is a motion–latent learning module consisting of a geometry encoder and a video encoder, which jointly process the input video and sampled points. The resulting latent tokens are decoded into a frame-wise 3D motion flow relative to the first video frame, producing temporally consistent 4D assets*



Motion 3-to-4 框架将病态的4D生成问题分解为两个可解耦的组件——静态形状编码和动态运动重建——并围绕“运动潜在学习”与“运动解码”两大模块构建流水线。

### 几何编码器：从参考网格到形状潜变量

给定第一帧的参考网格表面采样点集 $\mathbf{X}_0 \in \mathbb{R}^{N \times 3}$，几何编码器通过一组可学习查询 $\mathcal{A}$ 对点嵌入进行交叉注意力编码，生成紧凑的形状潜在表示：

$$
\mathbf{Z}_{\mathbf{X}_0} = \mathrm{CrossAttn}(\mathcal{A}, \mathrm{PointEmb}(\mathbf{X}_0)) \tag{Eq. 1}
$$

其中 $\mathrm{PointEmb}(\cdot)$ 将每个采样点映射到高维嵌入空间，$\mathcal{A}$ 作为可学习查询集从点云中聚合全局几何信息。该模块输出 $K$ 个形状潜变量（$K=64$），作为后续运动推理的几何锚点。这种设计使框架天然支持任意来源的参考网格——无论是预训练的3D生成器输出，还是艺术家手工创建的静态资产。

### 视频特征提取与时序嵌入

视频编码器采用冻结的 DINOv2 作为骨干网络，从每帧提取 patch 级视觉特征。为注入时序信息，每帧特征与可学习的时间位置嵌入相加，形成帧级 token 序列。随后，全局形状 token $\mathbf{Z}_{\mathbf{X}_0}$ 被拼接到每一帧 token 上，构成帧级运动表示。这一拼接策略使模型能够处理任意长度的视频输入，无需固定帧数约束。

### 交替注意力块：全局与局部的协同更新

运动潜在学习模块的核心是 $L$ 层交替注意力块（$L=16$），每层依次执行全局帧间注意力和帧内自注意力更新。对于第 $\ell$ 层，更新过程为：

$$
\begin{aligned}
[\mathbf{Z}_0^{(\ell-\frac{1}{2})}, \dots, \mathbf{Z}_{T-1}^{(\ell-\frac{1}{2})}] &= \mathrm{GlobalAttn}(\mathbf{Z}_0^{(\ell-1)}, \dots, \mathbf{Z}_{T-1}^{(\ell-1)}) \\
\mathbf{Z}_t^{(\ell)} &= \mathrm{FrameAttn}(\mathbf{Z}_t^{(\ell-\frac{1}{2})}), \quad \forall t = 0,\dots,T-1
\end{aligned} \tag{Eq. 2}
$$

全局注意力在所有帧的 token 之间建立跨时序关联，使模型感知长程运动依赖；帧内注意力则聚焦单帧内部的局部几何-外观对齐。这种交替设计在计算效率与运动一致性之间取得平衡，且对输入网格的分辨率具有鲁棒性。

### 运动解码器：从潜变量到逐帧运动流

运动解码器以参考网格采样点 $\hat{\mathbf{X}}_0$ 为查询，交叉注意力到各帧的运动潜变量 $\mathbf{Z}_t$，直接预测每帧的三维顶点位置：

$$
\hat{\mathbf{X}}_t = \mathrm{MotionDecoder}(\hat{\mathbf{X}}_0, \mathbf{Z}_t) \tag{Eq. 3}
$$

该模块将运动合成形式化为表面点与视频像素之间的对齐问题——解码器隐式学习从参考姿态到各帧的3D运动流（scene flow），而非预测抽象的全局运动参数或高斯偏移。这种逐顶点的密集预测使得方法能够同时恢复可见区域和遮挡区域的完整几何，且无需后处理的对齐步骤。

### 训练损失

模型采用预测点与真值点之间的均方误差作为监督信号，对所有帧和所有采样点进行密集回归：

$$
\mathcal{L} = \frac{1}{M T} \sum_{i=1}^{M}\sum_{t=1}^{T} \|\hat{\mathbf{X}}_t^i - \mathbf{X}_t^i\|_2^2 \tag{Eq. 4}
$$

其中 $M$ 为每帧采样的真值点数（$M=4096$），$T$ 为序列帧数。训练使用 12 帧序列，总 batch size 为 256，在 8 张 H100 GPU 上以学习率 $4\times10^{-4}$ 训练约 60k 步（约 1.5 天）。



## 实验与关键发现

### 实验设置

**数据集**：训练数据从 Objaverse 和 Objaverse-XL 中筛选约 16,000 个高质量动态物体（从约 50,000 个模型中精选），每个物体渲染为 12 帧的短视频序列。测试主要在两个基准上开展：自建的 **Motion-80** 数据集（包含短序列和长序列）以及公开的 **Consistent4D** 基准（7 个测试案例，每例 32 帧，从 4 个新视角渲染）。

**训练配置**：对每个网格采样 $N = 4096$ 个表面点作为形状输入，编码为 $K = 64$ 个形状潜变量，经过 $L = 16$ 层交替注意力模块处理。训练使用总批次大小 256，8 块 H100 GPU，学习率 $4 \times 10^{-4}$，共 60,000 步，约 1.5 天完成。

**评估指标**：几何质量采用 Chamfer Distance（CD↓）和 F-Score（↑）；外观质量采用 LPIPS（↓）、CLIP（↑）、DreamSim（↓）以及 FVD（↓）。为消除尺度与方向歧义，几何评估前对所有方法的第一帧进行 ICP 对齐。

**对比基线**：包括 **L4GM**（基于多视角视频的前馈 4D 高斯回归）、**GVFD**（基于潜在扩散的视频到 4D 生成）和 **V2M4**（逐帧网格生成加后处理时序对齐）。

### 主要结果

**Motion-80 基准（Table 2）**：在短序列上，Motion 3-to-4 的完整 pipeline（无真值网格）在几何指标上显著优于所有基线，CD 达到 0.1113，F-Score 达到 0.3171。当使用第一帧真值网格初始化（Ours w/m）时，性能大幅跃升：CD 降至 0.0437，F-Score 升至 0.6774，同时外观指标全面领先——LPIPS 0.0921、CLIP 0.9251、DreamSim 0.0614、FVD 497.43。这一对比揭示了两层信息：其一，完整 pipeline 已具备强泛化能力；其二，参考网格质量是运动重建精度的关键瓶颈——当真值几何锚点可用时，运动估计的保真度极高。

**Consistent4D 基准（Table 3）**：在外观指标上，本方法同样取得最优——LPIPS 0.1455、CLIP 0.8609、DreamSim 0.1691。几何对比（Figure 3）进一步显示，通过空间一致的运动重建，本方法能获得合理且高质量的三维几何，而基线方法在时序一致性上明显逊色。

**定性对比（Figure 4）**：在 Motion-80 上的可视化比较表明，本方法生成的 4D 资产在时序连贯性和结构一致性上均优于 GVFD、L4GM 和 V2M4。尤其值得注意的是，Motion 3-to-4 是唯一能将艺术家创建的静态 3D 网格转化为动态 4D 序列的方法，这得益于其解耦的网格表示和基于场景流的运动建模。

### 泛化与运动迁移

**真实场景泛化（Figure 5）**：方法对真实拍摄视频和生成动画均表现出良好泛化能力。将运动重建形式化为表面点到像素的对齐问题，使其能在不同形状和运动模式下学习鲁棒的局部对应关系。

**运动迁移（Figure 6）**：由于将 4D 合成分解为 3D 网格生成与运动重建，框架可将来自不同源视频的运动重新定向到静态关节物体上，实现运动迁移。

### 失败模式分析

**顶点粘连（Figure 7A）**：当物体不同部分在参考网格中切分不清或彼此靠近时，几何编码器因缺乏显式拓扑约束，可能导致运动预测中出现顶点粘连。根本原因在于点级运动预测缺乏对部件级结构关系的建模。

**拓扑变化适应（Figure 7B）**：当后续帧发生显著拓扑变化（如关节大幅度弯曲或物体分离），以第一帧网格作为参考几何无法表达这些变化，导致重建失败。这暴露了当前框架的核心局限：参考网格的拓扑在整个序列中保持固定，无法自适应演化。

**依赖参考网格质量**：Ours w/m 与完整 pipeline 的性能差距表明，方法对首帧网格的几何完整性和精度高度敏感。当使用生成模型产生的网格时，误差会向后续帧传播。

**外观敏感性**：视频特征提取依赖 DINOv2 的外观特征，在剧烈光照变化或纹理缺失场景下可能退化。这一点在分析中提及但缺乏定量消融验证，需在后续研究中确认影响程度。

### 方法谱系与知识库定位

Motion 3-to-4 在 4D 生成方法谱系中占据独特位置。与 **L4GM** 的端到端高斯回归和 **GVFD** 的全局潜在扩散不同，本方法将问题解耦为静态形状生成与逐帧运动重建，通过参考网格提供几何锚点，将运动估计转化为表面-像素对应学习。与 **V2M4** 的逐帧生成加后处理对齐相比，本方法在框架层面即保证了时序一致性，无需额外对齐步骤。

技术上，该方法融合了三个关键组件：基于交叉注意力的几何编码器（将点云压缩为紧凑形状潜变量）、交替全局/局部注意力架构（支持任意长度视频输入）、以及以参考点为查询的运动解码器（预测逐帧三维运动流）。这种帧级 transformer 设计对网格分辨率鲁棒，具有高度可扩展性。

核心洞见在于：通过将 4D 动态简化为“静态锚点 + 运动流”的表示，规避了对大规模 4D 动态训练数据的直接依赖，同时保留了完整的几何表达能力。这一思路与近年来的“解耦生成-重建”范式一脉相承，但首次将其系统性地应用于单目视频到 4D 的通用合成任务。

### 补充图表

![[assets/figures/papers/paper_list_l9_https_openaccess_thecvf_com_content_CVPR2026_html_Chen_Motion_3_to_4_3D/figures/004_Table_2.jpg]]
*Table 2: Quantitative evaluation on our Motion-80 set. Results are reported for both short and long sequences. “Ours w/m” denotes our method initialized with the ground-truth static mesh from the first frame. Thanks to the disentangled mesh representation and sceneflow–based motion modeling, our approach capable of transforming artist-created static 3D meshes into fully dynamic 4D sequences*

![[assets/figures/papers/paper_list_l9_https_openaccess_thecvf_com_content_CVPR2026_html_Chen_Motion_3_to_4_3D/figures/005_Table_3.jpg]]
*Table 3: Quantitative evaluation on Consist4D benchmark. We evaluate rendering performance across 7 test cases, each containing 32 frames, rendered from 4 target novel views*

![[assets/figures/papers/paper_list_l9_https_openaccess_thecvf_com_content_CVPR2026_html_Chen_Motion_3_to_4_3D/figures/006_Figure_3.jpg]]
*Figure 3: Geometric comparison on the Consistent4D benchmark [29]. Through spatially consistent motion reconstruction, we obtain plausible and high-quality 3D geometry*

![[assets/figures/papers/paper_list_l9_https_openaccess_thecvf_com_content_CVPR2026_html_Chen_Motion_3_to_4_3D/figures/007_Figure_5.jpg]]
*Figure 5: In-the-Wild Video-to-4D Synthesis. Our method generalizes to diverse in-the-wild inputs, including real-world videos (top row) and generated animations (bottom row). By formulating motion reconstruction as surface-to-pixel alignment, we achieve robust local correspondence reasoning across varied shapes and motion patterns*

![[assets/figures/papers/paper_list_l9_https_openaccess_thecvf_com_content_CVPR2026_html_Chen_Motion_3_to_4_3D/figures/008_Figure_6.jpg]]
*Figure 6: Motion Transfer Example. By disentangling 4D synthesis into 3D mesh generation and motion reconstruction, our framework can animate static articulated objects with motion retargeted from videos of different sources*

![[assets/figures/papers/paper_list_l9_https_openaccess_thecvf_com_content_CVPR2026_html_Chen_Motion_3_to_4_3D/figures/001_Figure_1.jpg]]
*Figure 1: From a single glance, Motion 3-to-4 unfolds: weaving time, shape, and movement into living 4D reality*



## 定位与知识库关联

### 问题定位与核心瓶颈

高质量4D动态训练数据的极度稀缺是制约该领域发展的根本瓶颈。现有基于VAE的运动潜在空间方法因数据不足导致泛化能力薄弱，而单目视频固有的几何与运动歧义性使得同时恢复形状和运动极具挑战。Motion 3-to-4 的核心洞察在于：借助一个静态参考网格（可取自生成模型或用户提供）提供稳定的几何锚点，将动态4D问题简化为从单目视频中估计每帧的3D运动流，由此实现对可见与遮挡区域的完整几何恢复。

### 与现有4D合成方法的谱系关系

当前从单目视频进行4D合成的方法可大致分为三类，Motion 3-to-4 在技术路径上采取了正交策略：

- **逐帧生成 + 后处理对齐**：以 **V2M4** 为代表，先逐帧生成3D网格，再通过后处理进行时间对齐。这类方法将形状生成与运动估计解耦不彻底，后处理对齐难以保证长序列的时间一致性。
- **全局运动生成**：以 **L4GM**（feedforward 4D Gaussian regression from multi-view videos）和 **GVFD**（video-to-4D via latent diffusion over 3D Gaussians）为代表，直接从视频预测全局运动或高斯偏移。这类端到端方法受限于4D训练数据规模，对新形状的泛化能力有限。
- **解耦形状与运动**（本方法路径）：Motion 3-to-4 将4D合成分解为静态3D形状生成和基于参考网格的运动重建两个可独立处理的子问题。通过把运动估计表述为表面点与视频像素间的对应关系学习，规避了直接生成完整4D动态对大数据的需求。

Table 1 对上述方法在表征形式、运动建模方式、是否支持运动迁移及推理速度等维度进行了系统对比。Motion 3-to-4 是其中唯一支持将艺术家创作的静态3D网格直接转换为动态4D序列的方法，这得益于其解耦的网格表征和基于场景流的运动建模。

### 关键技术路径的适用边界

**适用场景**：
- 单目视频到4D资产的重建与生成，支持任意长度视频输入
- 运动迁移：将源视频的运动模式迁移到不同的静态3D形状上（Figure 6）
- 开放场景视频的泛化：包括真实拍摄视频和生成动画（Figure 5）
- 对网格分辨率具有鲁棒性，支持灵活的视频长度处理

**不适用或需谨慎使用的场景**：
- **顶点粘连问题**：当物体不同部分在参考网格中切分不清或彼此靠近时，几何编码器因缺乏显式拓扑约束，可能导致运动预测中顶点粘连（Figure 7A）
- **拓扑变化适应性**：当后续帧发生显著拓扑变化（如关节大幅度弯曲或物体分离），以第一帧网格作为参考几何可能无法表达这些变化，导致重建失败（Figure 7B）
- **参考网格质量依赖**：方法性能受限于提供的或生成的第一帧网格的几何完整性和精度
- **光照与纹理变化**：视频特征提取依赖外观信息，在剧烈光照变化或纹理缺失时可能退化

### 局限与开放问题

**已识别的局限**：
1. 几何编码器缺乏显式拓扑约束机制，无法感知物体部件的语义分割，导致近距离部件间的顶点粘连
2. 以第一帧为固定参考拓扑的设定，本质上假设运动过程中拓扑结构不变，无法处理物体分离、合并等拓扑变化
3. 对外观特征的依赖使其在纹理缺失或剧烈光照变化场景下鲁棒性不足

**值得探索的开放问题**：
1. 如何显式建模或推断拓扑变化，使运动重建能自适应后续帧中出现的大尺度结构变化？
2. 能否引入拓扑先验（如骨架或分块结构）来缓解顶点粘连现象？
3. 在缺乏参考网格时，如何更稳健地生成高质量首帧网格，避免误差向后传播？
4. 该方法能否扩展至多对象交互或更复杂的动态场景？



## 原文 PDF

![[paperPDFs/CVPR_2026/Motion_3_to_4_3D_Motion_Reconstruction_for_4D_Synthesis.pdf]]
