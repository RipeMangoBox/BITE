---
title: "ArtisanGS: Interactive Tools for Gaussian Splat Selection with AI and Human in the Loop"
type: paper
paper_level: A
venue: arXiv
year: 2026
pdf_ref: paperPDFs/arxiv_2026/ArtisanGS_Interactive_Tools_for_Gaussian_Splat_Selection_with_AI_and_Human_in_the_Loop.pdf
project_link: https://instruct-gs2gs.github.io/
code_link: https://github.com/keijiro/SplatVFX
aliases:
- AIST
- ArtisanGS
tags:
- arxiv_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 引入Cutie视频掩码跟踪网络，利用其记忆帧设计实现用户可修正的多视角掩码传播；同时结合基于可微渲染器的3D聚合优化和灵活的手动投影模式，使得分割过程既快速又允许用户随时介入。
primary_logic: 将单帧用户的2D选择掩码通过Cutie扩展为密集视角的掩码序列，再利用3DGS的可微渲染器通过简单的特征优化将多视角掩码聚合成3D高斯标签，并在循环中支持用户诊断和修正错误，从而在无场景预训练的前提下实现灵活、快速的交互式3D分割。
claims:
- We propose a fast AI-driven method to propagate user-guided 2D selection masks to 3DGS selections, enabling interactive user correction.
- We rely on a robust mask tracking network Cutie, which due to the unique design of its memory frames, makes our interactive segmentation amenable to user correction.
- Our solution is faster than most others and easier to extend to alternative 3DGS formulations, because we treat differentiable splat renderer as a black box component.
- NVOS 上 mIoU = 94.1
---

# ArtisanGS: Interactive Tools for Gaussian Splat Selection with AI and Human in the Loop

> [!tip] 核心洞察
> 将单帧用户的2D选择掩码通过Cutie扩展为密集视角的掩码序列，再利用3DGS的可微渲染器通过简单的特征优化将多视角掩码聚合成3D高斯标签，并在循环中支持用户诊断和修正错误，从而在无场景预训练的前提下实现灵活、快速的交互式3D分割。

| 字段 | 内容 |
|------|------|
| 中文题名 | ArtisanGS: 基于AI与人机协同的交互式高斯泼溅选择工具 |
| 英文题名 | ArtisanGS: Interactive Tools for Gaussian Splat Selection with AI and Human in the Loop |
| 会议/期刊 | arXiv 2026 |
| Links | [paper](https://arxiv.org/abs/2602.10173) · [paper](https://arxiv.org/abs/2412.00518) · [Project](https://instruct-gs2gs.github.io/) · [Code](https://github.com/keijiro/SplatVFX) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | ArtisanGS Interactive Segmentation Toolkit |
| Dataset | NVOS |

> [!tip] 效果简介
> - NVOS 上，mIoU 94.1 vs 92.5 (GaussianCut) (+1.6)；Acc 98.8 vs 98.6 (FlashSplat) / 98.4 (GaussianCut) (+0.2 / +0.4)。

## 概要

3D高斯泼溅（3DGS）能够从多视角图像中重建出照片级真实的三维场景，但要将场景中的单个物体“拆解”出来进行编辑或仿真，现有方法面临一个根本性瓶颈：**要么需要漫长的逐场景预训练，无法纠正错误且缺乏灵活性；要么虽然免去预训练，却未提供用户纠错机制，难以满足实际交互需求**。ArtisanGS 针对这一瓶颈，提出了一套**基于AI与人机协同的交互式高斯泼溅选择工具**，其核心洞察是：将单帧用户的2D选择掩码通过视频掩码跟踪网络Cutie扩展为密集视角的掩码序列，再利用3DGS的可微渲染器以简单的特征优化将多视角掩码聚合成3D高斯标签，并在循环中支持用户诊断和修正错误，从而在**完全无场景预训练**的前提下实现灵活、快速的交互式3D分割。

在方法定位上，ArtisanGS 与现有3DGS分割方法的关键差异体现在三个维度：**训练需求**——无需任何逐场景特征学习，直接复用预训练2D模型和可微渲染器；**用户纠错**——支持用户在自动分割结果上添加额外掩码进行修正，并结合手动投影模式灵活干预；**掩码传播**——采用Cutie的记忆帧设计，使交互式分割对用户修正天然友好，而非依赖点查询或极线搜索的SAM查询。这些设计使得该方法在分割速度上达到1–5秒，显著快于多数同类方法（见表1），且因将可微渲染器视为黑盒组件，易于扩展到其他3DGS变体。

定量评估方面，在NVOS数据集上，ArtisanGS 取得了94.1的mIoU和98.8的Acc，分别比最优无预训练基线GaussianCut和FlashSplat高出1.6和0.2–0.4个百分点（见表2）。消融实验进一步表明，约50个采样视角可在分割质量与速度间取得最优平衡（训练视角mIoU 93.9，速度1.5–2.5秒），而预分割策略能有效移除遮挡物、大幅提升跟踪质量和速度，但需注意其在一个特例（horns_left）中因输入掩码未包含完整目标而失效。需要指出的是，NVOS数据集规模极小（仅8个场景），且其原始scribble标注与现代基于点击的SAM方法不兼容，导致基线方法的性能数值未必完全公平可比，这些结果应在上述限制下审慎解读。

### 从场景重建到对象分解的鸿沟

3D高斯泼溅（3D Gaussian Splatting, 3DGS）已成为从多视角图像重建高质量三维场景的主流技术。然而，重建后的场景本质上是一个“整体”的高斯集合——所有物体、背景、遮挡物被混合在同一表示中，无法直接支持面向单个对象的编辑、物理仿真或场景重组等下游应用。要实现这些应用，必须先将场景“拆解”为独立的对象部件。这正是ArtisanGS所瞄准的核心问题。

现有的3DGS分割方法大致分为两条技术路线：**需逐场景预训练的方法**和**无预训练的快速方法**，但两者在实际交互场景中均存在显著缺陷。

### 现有方法的瓶颈

**预训练依赖型方法**（如SAGA、OmniSeg3D、Gaussian Grouping、GARField、iSegMan）需要在每个新场景上额外训练或提取特征，这一过程通常耗时数分钟到数十分钟。更关键的是，一旦训练完成，分割结果即被“固化”——如果模型在某视角产生错误，用户无法进行任何修正，只能接受不可逆的错误输出。这种缺乏纠错机制的设计，使得这些方法难以胜任需要精确边界的实际编辑任务。

**无预训练方法**（如FlashSplat、GaussianCut、GaussianEditor）虽然避免了逐场景训练的开销，但普遍采用基于SAM的点查询或极线搜索策略来传播2D掩码。这类方法同样不具备用户纠错能力：一旦掩码在某视角出错，错误会沿传播路径累积并最终污染3D聚合结果。此外，部分方法在实际运行中的速度远慢于文献报告值——例如GaussianEditor实际运行约需40秒，远不足以支撑交互式工作流。

**共同的缺失环节**：两类方法都缺乏一个“人在回路”（human-in-the-loop）的机制，使得用户能够诊断分割质量、在必要时添加额外标注以修正错误，并快速迭代优化结果。

### 核心动机与设计目标

ArtisanGS的设计动机源于一个实际需求：**让3D从业者能够从野外捕获的场景中灵活地选取对象，并直接用于编辑、物理仿真等下游任务**（见Figure 1）。为此，方法需要满足三个关键要求：

1. **无预训练**：避免任何逐场景的离线优化，使得分割过程可以“开箱即用”。
2. **可交互修正**：用户能够随时介入，在任意视角添加或修正2D掩码，并将修正反馈融入传播与聚合流程。
3. **快速响应**：分割操作在秒级完成，以支撑真正的交互式迭代。

### 技术突破口

ArtisanGS实现上述目标的关键在于两个技术选择：

- **Cutie视频掩码跟踪网络**：利用其独特的记忆帧（memory frame）设计，将用户提供的单帧2D掩码传播到密集采样视角，同时支持用户随时注入新的标注帧来修正跟踪结果。这与基于点查询的SAM传播策略形成根本差异——记忆帧机制天然兼容“用户干预后重新推理”的交互模式。
- **可微渲染器驱动的轻量3D聚合**：将3DGS的可微渲染器视为黑盒组件，仅通过简单的单通道特征优化和阈值二值化即可将多视角掩码聚合成3D高斯标签。这一设计避免了复杂的投票机制或图割优化，使得方法既快速又易于扩展到不同的3DGS表示变体。

通过将“2D掩码获取—多视角跟踪—3D聚合—用户修正”组织为一个闭环的交互流程，ArtisanGS在保持无预训练的前提下，首次为3DGS分割引入了灵活的人机协同能力。

## 核心方法与创新机理

ArtisanGS的核心创新在于构建了一套**无需场景预训练、支持用户随时介入修正的交互式3DGS分割工具链**。与现有方法相比，它在四个关键维度上实现了根本性的改变：

### 1. 去除场景预训练依赖

现有3DGS分割方法可分为两类：一类需要为每个场景进行逐场景的特征学习或训练（如**SAGA**、**OmniSeg3D** (Ying et al., CVPR 2024)、**Gaussian Grouping** (Ye et al., ECCV 2025)、**GARField** (Kim et al., CVPR 2024)、**iSegMan** (Zhao et al., CVPR 2025)），另一类虽然免训练但在速度或灵活性上存在短板（如**FlashSplat** (Shen et al., ECCV 2025)、**GaussianCut**、**GaussianEditor**）。ArtisanGS完全摒弃了逐场景预训练的需求，直接利用预训练的2D分割模型和3DGS的可微渲染器，将分割时间压缩至1-5秒，使得交互式迭代成为可能（Table 1）。

### 2. 引入可修正的视频掩码跟踪

这是ArtisanGS区别于所有基线方法的核心技术选择。现有无预训练方法（如FlashSplat、GaussianEditor）通常依赖基于点查询或极线搜索的SAM查询来传播掩码，但这类传播缺乏用户修正的机制。ArtisanGS采用**Cutie视频掩码跟踪网络**（Cheng et al., 2024），利用其独特的记忆帧（memory frames）设计，使用户可以在跟踪过程中注入额外的标注掩码，系统能够将修正信息融入后续推理，实现真正的交互式纠错循环（§4.4.4）。

### 3. 简洁的可微渲染聚合

现有方法在将多视角2D掩码聚合为3D高斯标签时，往往采用自定义投票机制、整数线性规划或图割等复杂策略。ArtisanGS将可微3DGS渲染器视为黑盒组件，仅通过单通道特征优化配合L2图像损失，再以简单的阈值二值化（$M > 0.5$）获得二值3D掩码（§4.4.3）。这种极简设计不仅加速了聚合过程，还使得方法易于扩展到其他3DGS变体。

### 4. 灵活的手动投影与布尔选择模式

ArtisanGS提供了锥体裁剪投影（frustum projection）和深度投影两种手动模式，支持与新建、添加、减去、相交四种布尔选择模式组合（§4.1, §4.3）。这种设计使得用户在不依赖自动跟踪的情况下，也能通过简单的2D操作完成精确的3D选择，弥补了纯自动方法在复杂遮挡场景下的不足。

### 创新瓶颈的因果机制

上述四个changed slots并非孤立存在，而是围绕一个核心因果链条协同工作：**Cutie的记忆帧设计使得用户修正成为可能**，而**无预训练的可微渲染聚合保证了修正后的快速反馈**，两者结合形成了“选择-诊断-修正-再聚合”的交互闭环。这一闭环从根本上解决了现有方法“要么慢且无法纠错，要么快但错误固化”的困境。

ArtisanGS提出了一套面向3D高斯泼溅（3DGS）场景的交互式分割工具包，其核心设计目标是：在**无需任何逐场景预训练**的前提下，将用户在任意单一视角上提供的2D选择掩码快速传播为3D高斯粒子的精确选择，并允许用户在流程中随时诊断和纠正错误。

### 总体流程

整个pipeline围绕“2D掩码获取→多视角传播→3D聚合→用户修正”的闭环构建。图3（Fig. 3）展示了自动跟踪分割与用户纠正的总体架构。流程始于用户在某一视角上通过点击（驱动SAM）或手动绘制提供2D目标掩码，随后系统自动将该掩码传播到一组密集采样的目标视角，再利用3DGS的可微渲染器将所有视角的2D掩码聚合为每个高斯粒子的二值标签。用户可随时浏览自动分割结果，对不理想的区域添加额外视角的掩码进行修正，修正后的掩码重新融入传播与聚合循环。

![[assets/figures/papers/paper_list_l67_https_arxiv_org_abs_2602_10173/figures/005_Figure_3.jpg]]
*Figure 3: Auto-Tracked Segmentation with Corrections: We propose automatic way to project 2D user masks*

### 模块组成与数据流

系统由六个功能模块构成，按数据流顺序依次为：

1. **2D掩码获取（§4.2）**：支持基于SAM的点击查询和手动自由绘制两种方式，在用户选定的当前视角上生成目标对象的2D分割掩码 $S^{\boxplus}$。

2. **多视角掩码跟踪（§4.4.2）**：采用Cutie视频掩码跟踪网络（Cheng et al., 2024）将用户提供的2D掩码传播到一组密集采样的目标视角。Cutie的记忆帧（memory frames）设计是本方法支持用户修正的关键——系统通过Jaccard指数选择与用户标注视角最相似的密集视角作为记忆帧注入点（公式1），使后续的用户修正掩码能够无缝融入跟踪过程。

3. **3D掩码聚合（§4.4.3）**：将多视角2D掩码聚合为3D高斯选择。方法极为简洁：为每个高斯粒子分配一个可优化的单通道特征，通过可微3DGS渲染器将其渲染到各视角，以L2图像损失对齐渲染结果与2D掩码，优化完成后以阈值0.5二值化得到最终的3D选择 $S^{\flat}$。这一设计将可微渲染器视为黑盒组件，使其易于扩展到不同的3DGS变体。

4. **交互式修正循环（§4.4.4）**：用户浏览自动分割结果，可在任意视角添加额外掩码（新增、修正或删除区域）。这些修正掩码作为Cutie的额外记忆帧注入，重新驱动掩码跟踪和3D聚合，实现增量式优化。

5. **手动投影模式（§4.3）**：提供锥体裁剪投影（frustum projection）和深度投影（depth projection）两种手动模式，允许用户绕过自动流程，直接将2D掩码投影到3D空间。如图4所示，这两种模式可与布尔选择模式（New, Add, Subtract, Intersect）组合使用，提供灵活的手动选择能力。

6. **预分割加速（§4.4.5）**：可选的预处理步骤。利用用户标注的无遮挡掩码，通过锥体裁剪投影进行粗分割，移除遮挡物后再执行掩码跟踪和聚合。该步骤能有效提升跟踪质量（图6）并大幅加快速度（从约26秒降至1.5-2.5秒），但需注意当输入掩码未包含完整目标时可能引入失败（如NVOS中horns_left案例，mIoU从92.7降至0.0，见表4）。

### 输入输出与交互模式

- **输入**：用户在一个视角上提供的2D选择掩码（点击或手绘），以及可选的修正掩码。
- **输出**：3DGS场景中每个高斯粒子的二值选择标签 $S^{\flat}$，可直接用于后续的编辑、物理仿真等应用（图9）。
- **交互模式**：系统支持四种布尔选择模式——新建（New）、添加（Add）、减去（Subtract）、相交（Intersect），作用于当前活跃的2D掩码或已生成的3D高斯掩码，使用户能够灵活地组合多次操作以构建复杂选择。

### 关键设计决策

整个框架的核心洞察在于：将单帧用户的2D选择通过Cutie扩展为密集视角的掩码序列，再借助3DGS可微渲染器通过简单的特征优化完成3D聚合，并在循环中保留用户介入的入口。这一设计使得ArtisanGS在无场景预训练的前提下，实现了1-5秒的交互式分割速度（表1），显著快于多数现有方法（如GaussianEditor约40秒），同时保持了NVOS数据集上94.1 mIoU的领先分割精度（表2）。

ArtisanGS 的交互式分割工具包由六个核心模块串联而成，形成一条“用户输入 → 2D 传播 → 3D 聚合 → 用户修正”的闭环流水线。

### 1. 2D 掩码获取

用户通过两种方式在任意视角提供 2D 选择掩码 $S^{\boxplus}$：
- **基于 SAM 的点击交互**：用户点击目标物体，由预训练的 Segment Anything Model 生成初始掩码。
- **手动绘制**：用户直接绘制或修正掩码区域。

该模块是整个人机协同循环的起点，所有后续的自动传播和聚合均以此处的 2D 标注为种子。

### 2. 多视角掩码跟踪（Cutie 传播）

这是方法的核心创新之一。系统将用户提供的单帧 2D 掩码传播到密集采样的多视角上，具体机制如下：

**视角相似度选择**：为了将用户标注注入 Cutie 的记忆帧，系统首先从预设的密集目标视角集 $\dot{V}$ 中选出与用户标注视角 $v$ 最相似的视角：

$$\dot{V}^{\ast}(v) := \operatorname*{argmin}_{\dot{v}_j} J\big(\mathrm{viz}(\mathcal{G}, v), \mathrm{viz}(\mathcal{G}, \dot{v}_j)\big)$$

其中 $\mathrm{viz}(\mathcal{G}, v)$ 表示场景 $\mathcal{G}$ 在视角 $v$ 下的可见性掩码，$J(\cdot, \cdot)$ 为 Jaccard 指数。此公式确保记忆帧注入发生在与用户视角内容重叠最大的目标视角上，从而提高跟踪稳定性。

**记忆帧注入与传播**：将用户掩码作为记忆帧注入 **Cutie**（Cheng et al., 2024）视频掩码跟踪网络。Cutie 独特的记忆帧设计使得用户后续添加的修正掩码可以随时注入并影响全局传播结果，这是现有基于点查询或极线搜索的方法（如 FlashSplat、GaussianEditor）所不具备的能力。

### 3. 3D 掩码聚合

获得多视角 2D 掩码后，系统通过可微渲染器将其聚合为 3D 高斯标签。该过程将渲染器视为黑盒组件，无需任何逐场景预训练：

- 为每个高斯分配一个**单通道特征** $m_i$，初始化为 0。
- 使用可微 3DGS 渲染器将特征渲染到各视角，得到渲染特征图。
- 以 L2 图像损失优化 $m_i$，使渲染特征图逼近 Cutie 输出的多视角 2D 掩码。
- 优化完成后，对特征进行**阈值二值化**：$S^{\flat} = \mathbb{1}[M > 0.5]$，得到最终的二值 3D 选择掩码。

这种简单的单通道优化 + 阈值策略替代了现有方法中复杂的投票机制、整数线性规划或图割，在保持精度的同时大幅提升了速度。

### 4. 交互式修正循环

用户可浏览自动生成的掩码结果，在任意视角添加额外掩码进行修正。修正后的掩码重新注入 Cutie 的记忆帧，触发新一轮的跟踪与聚合。这一闭环设计使得分割过程始终允许用户介入，而非像预训练方法那样将错误固化。

### 5. 手动投影模式

为提供更灵活的选择手段，系统提供两种手动 2D 到 3D 投影模式：

- **锥体裁剪投影**：选择所有其均值 $\mu_i$ 投影到当前 2D 掩码内的高斯。
- **深度投影**：在锥体裁剪基础上进一步引入深度约束。

这两种模式可与布尔选择模式（新建、添加、减去、相交）组合使用，实现对 3D 场景的精细手动选择。

### 6. 预分割（可选加速模块）

为提升遮挡场景下的跟踪鲁棒性和速度，系统提供可选的预分割步骤：利用无遮挡标注掩码的锥体裁剪投影对场景进行粗分割，移除遮挡物后再执行 Cutie 跟踪。消融实验表明，预分割可将分割时间从 26–27s 降至 1.5–2.5s，但需注意当输入掩码未包含完整目标时可能导致失败（如 NVOS 中 horns_left 案例的 mIoU 从 92.7 骤降至 0.0）。

## 实验与关键发现

### 主实验结果

在NVOS基准上，ArtisanGS在关闭预分割（pre-segmentation）的情况下取得了最优性能：mIoU达到**94.1**，准确率（Acc）达到**98.8**（Table 2）。与最强无预训练基线相比，mIoU超越**GaussianCut**的92.5（+1.6），Acc超越**FlashSplat**的98.6（+0.2）。开启预分割后，整体mIoU降至**82.4**，Acc为**98.1**，性能下降主要源于单个失败案例“horns_left”（详见下文失败模式分析）。

![[assets/figures/papers/paper_list_l67_https_arxiv_org_abs_2602_10173/figures/007_Table_2.jpg]]
*Table 2: Segmentation Eval on NVOS*

在分割速度方面，ArtisanGS的自动分割仅需**1–5秒**（Table 1），而多数对比方法需数十秒甚至数分钟。相比之下，部分训练自由方法如**GaussianEditor**在实际运行中耗时约40秒，远超文献报告值。这一速度优势使得用户交互式迭代分割成为可能。

![[assets/figures/papers/paper_list_l67_https_arxiv_org_abs_2602_10173/figures/002_Table_1.jpg]]
*Table 1: 3D Segmentation methods for 3D Gaussian Splats, prioritizing methods that take some form of user input. Many approaches require Features training or extraction for every input scene, where in some cases this step is bundled into original 3DGS training (noted as "(bndl)"). When reported, segmentation time is listed, given user input such as a target click*

**公平性说明**：NVOS数据集仅包含8个场景，且为前向视角的受控捕获，难以全面反映野外复杂场景的泛化性能。此外，NVOS原始scribble标注与现代基于点击的SAM方法不兼容，迫使各基线方法重新设计点采样逻辑，而不同采样策略直接影响结果。例如，**OmniSeg3D**（Ying et al., CVPR 2024）在统一点输入下mIoU从原始报告的91.7骤降至78.5，说明Table 2中的数值对比未必完全公平可比。

### 消融实验

在自标注的Figurines 3DGS场景上进行了系统的消融实验（Table 3），核心发现如下：

![[assets/figures/papers/paper_list_l67_https_arxiv_org_abs_2602_10173/figures/009_Table_3.jpg]]
*Table 3: Segmentation Ablations on hand-labeled Figurines 3DGS scene*

**视角数量**：使用约50个采样视图可在分割质量与速度间取得最优平衡——训练视角mIoU达93.9，分割耗时仅1.5–2.5秒。进一步增加视角数对mIoU提升有限，但计算开销线性增长。

**预分割影响**：关闭预分割时，自动分割速度约为26–27秒，mIoU降至83.8–89.0。预分割通过锥体裁剪投影粗分割场景，有效移除遮挡物对跟踪器的干扰（Fig. 6），同时大幅减少后续Cutie跟踪和3D聚合的计算量，是速度提升的关键因素。仅使用用户选择视角时，mIoU为88.9–94.3，表明即使不依赖密集采样，方法仍保持可用性能。

### 失败模式分析

**预分割的边界失效**：在NVOS的“horns_left”案例中，预分割导致mIoU骤降至0.0（Table 4），而不使用预分割时mIoU为92.7。失败根源在于该案例的输入掩码未包含完整目标——目标部分出画（Fig. 5b），锥体裁剪投影无法正确捕捉完整物体，反而将不完整的掩码传播至后续跟踪和聚合流程。这说明预分割策略对输入掩码的完整性高度敏感，在处理部分可见目标时需要用户额外标注或采用更智能的遮挡处理机制。

**遮挡场景的鲁棒性不足**：在严重遮挡场景下，自动分割可能产生错误掩码，需要用户通过交互式修正循环添加额外视角的掩码来纠正。尽管Cutie的记忆帧设计支持这种干预，但完全自动化流程在面对极端遮挡时仍不够稳健。

**2D模型的泛化边界**：基于Cutie的掩码跟踪受限于2D模型的泛化能力，对极端视角或与训练分布差异大的场景可能出现不稳定的掩码传播，这在大规模野外应用中可能成为瓶颈。

### 关键图表结论

**Table 1** 系统对比了现有3DGS分割方法的预训练需求与分割耗时：ArtisanGS是少数同时满足“无需逐场景预训练”和“秒级分割”的方法，且支持用户交互式修正，这一组合在现有方法谱系中具有独特性。

**Table 3** 的消融数据揭示了预分割的双刃剑效应：它大幅提升速度（26–27s → 1.5–2.5s）并改善跟踪输入质量（Fig. 6），但在输入掩码不完整时可能引发灾难性失败。

**Fig. 6** 直观展示了预分割对跟踪器输入质量的改善：无预分割时，遮挡物在输入视图中占据显著区域，干扰Cutie的掩码跟踪；预分割后，遮挡物被移除，目标区域更加清晰，跟踪质量显著提升。

![[assets/figures/papers/paper_list_l67_https_arxiv_org_abs_2602_10173/figures/021_Table_4.jpg]]
*Table 4: NVOS Segmentation evaluation. The “horns_left” is failing with pre-segmentation because the object is partially out of frame in the input mask*

![[assets/figures/papers/paper_list_l67_https_arxiv_org_abs_2602_10173/figures/012_Figure.jpg]]
*Figure: (a) Segmentation pipeline. (b) Working with modes. (c) Depth projection. (d) Comparison with GaussianEditor*

## 定位与知识库关联

### 1. 方法在3DGS分割谱系中的坐标

ArtisanGS针对的核心瓶颈是3DGS场景的交互式物体选择。现有方法大致分为两类：

- **需逐场景预训练的分割方法**：如 **SAGA**、**Gaussian Grouping**（Ye et al., ECCV 2025）、**OmniSeg3D**（Ying et al., CVPR 2024）、**GARField**（Kim et al., CVPR 2024）和 **iSegMan**（Zhao et al., CVPR 2025）。这些方法在3DGS训练阶段或之后为每个场景学习额外的特征场（如SAM特征蒸馏），导致预处理耗时且无法在用户交互中动态修正错误——一旦特征固化，分割结果即被锁定。

- **无预训练的快速分割方法**：如 **FlashSplat**（Shen et al., ECCV 2025）、**GaussianCut**、**GaussianEditor**。它们通过点查询或极线搜索驱动SAM进行多视角掩码传播，省去了场景预训练，但缺乏用户纠错机制，且部分方法实际运行速度远慢于文献报告（如GaussianEditor约40秒）。

ArtisanGS位于后一阵营，但通过两个关键设计实现了差异化：**（1）采用Cutie视频掩码跟踪网络**（Cheng et al., 2024）替代基于点查询的SAM传播，利用其记忆帧设计使用户可随时注入修正掩码并重新推理；**（2）将可微3DGS渲染器视为黑盒组件**，通过简单的单通道特征优化和阈值二值化完成多视角掩码到3D高斯标签的聚合，避免了复杂的投票或图割机制。这使得方法不仅速度快（1-5秒），且易于扩展到其他3DGS变体。

### 2. 因果机制与关键设计选择

ArtisanGS的核心因果链条是：**用户2D掩码 → Cutie记忆帧注入 → 密集视角掩码跟踪 → 可微渲染器驱动的3D聚合 → 用户诊断与修正循环**。

- **Cutie的记忆帧机制**是支持用户修正的关键。与普通视频跟踪器不同，Cutie允许在任意帧注入新的掩码作为"记忆"，后续跟踪会自动融合新信息。这使得用户可以在浏览自动分割结果后，在错误视角添加额外标注，系统无需重新初始化即可修正全局3D掩码。

- **可微渲染器驱动的3D聚合**（§4.4.3）将多视角2D掩码聚合问题转化为简单的优化问题：为每个高斯分配一个单通道特征，通过可微渲染器渲染该特征图，并以L2图像损失拟合多视角2D掩码，最后以0.5阈值二值化得到3D选择。这一设计的优势在于无需手动设计复杂的3D投票或图割逻辑，且天然继承了可微渲染器的梯度传播能力。

- **预分割策略**（§4.4.5）作为可选的性能提升手段，利用无遮挡标注掩码的锥体裁剪投影进行粗分割，去除遮挡物后再输入跟踪器。这一步骤能显著提升跟踪质量并加速聚合（速度从26-27秒降至1.5-2.5秒），但存在失败模式：当输入掩码未包含完整目标时（如NVOS的"horns_left"案例），预分割反而导致mIoU从92.7骤降至0.0。

### 3. 适用边界与已知局限

**适用场景**：
- 静态3DGS场景的交互式物体级分割，支持单点击或手绘掩码作为输入
- 需要用户可干预、可迭代修正的分割流程
- 对速度敏感、无法承受逐场景预训练的应用场景

**已知局限**：
1. **评估基准的局限性**：定量评估仅在NVOS数据集（8个场景）和少量自标注场景上进行。NVOS为前向视角的受控捕获，无法反映真实野外场景的复杂性。此外，NVOS的原始scribble标注与现代基于点击的SAM方法不兼容，迫使基线方法重新设计点采样逻辑，不同采样策略直接影响结果，报告的数值未必公平可比。当采用统一输入时，OmniSeg3D的性能从91.7 mIoU降至78.5，凸显了基准的敏感性。

2. **严重遮挡与目标部分出画的失败**：自动分割在严重遮挡或目标仅部分可见时可能失败，依赖用户额外标注来纠正。预分割策略虽然能缓解遮挡问题，但在输入掩码不完整时会引入新的失败模式（如"horns_left"案例）。

3. **Cutie的泛化边界**：掩码跟踪受限于Cutie作为2D模型的泛化能力，对极端视角或与训练分布差异大的场景可能出现不稳定的掩码传播。

4. **编辑应用的原型阶段**：文中展示的视频修复与3D微调编辑应用仍为早期原型，生成质量与多视角一致性有限，尚未经过系统评估。

5. **工具链成熟度**：整体工具链目前为研究原型，尚未集成到成熟的生产软件中，用户界面和交互流程有待进一步优化。

### 4. 开放问题与潜在后续方向

1. **复杂场景的扩展性**：如何在包含数十乃至上百个物体的复杂场景中保持分割精度与交互效率？当前方法假设场景可被分解为少量感兴趣目标，大规模场景下的跟踪器性能和聚合质量尚未验证。

2. **动态场景支持**：该方法能否扩展到动态场景或非刚性对象的连续帧分割与跟踪？Cutie本身支持视频对象分割，但与3DGS动态表示的结合路径尚不明确。

3. **与生成式编辑的深度结合**：能否将精确的交互式选择与更强大的生成式编辑模型（如3D inpainting）深度结合，实现端到端的可控编辑？当前编辑应用仅展示了初步的定向、物理仿真和局部编辑能力。

4. **更智能的预分割策略**：如何设计能自动处理各种程度遮挡的预分割策略，避免当前"全有或全无"的失败模式？这可能需要引入不确定性估计或自适应阈值机制。

5. **更鲁棒的聚合损失函数**：是否有比当前L2图像损失更鲁棒的多视角掩码聚合损失函数，可进一步降低对视角数量和分布的敏感性？消融实验表明50个视图是质量与速度的平衡点，但更少视图时质量下降明显（用户视角mIoU降至88.9-94.3）。

6. **更大规模、多样化的基准**：当前领域迫切需要超越NVOS的标准化基准，涵盖真实野外场景、多物体遮挡、非前向视角分布等挑战，以公平评估各类方法的实际泛化能力。

## 原文 PDF

![[paperPDFs/arxiv_2026/ArtisanGS_Interactive_Tools_for_Gaussian_Splat_Selection_with_AI_and_Human_in_the_Loop.pdf]]
