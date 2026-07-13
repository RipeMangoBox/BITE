---
title: "AnchorFlow: Training-Free 3D Editing via Latent Anchor-Aligned Flows"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/AnchorFlow_Training_Free_3D_Editing_via_Latent_Anchor_Aligned_Flows.pdf
project_link: null
code_link: "https://github.com/ZhenglinZhou/AnchorFlow"
aliases:
- AnchorFlow
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 通过引入一个在全时间步上共享的全局潜锚点，并强制源轨迹和目标轨迹在潜空间中与该锚点对齐，从而稳定编辑流。
primary_logic: 随机噪声锚点引起的潜空间不一致性是编辑失败的根本原因；通过共享一个全局潜锚点并最小化源和目标轨迹的单步逆推潜变量差异，可实现更强且更稳定的语义编辑，同时保留几何结构。
claims:
- AnchorFlow建立了一个由源和目标轨迹共享的全局潜锚点，并通过松弛锚点对齐损失以及锚点对齐更新规则强制一致性。
- 编辑不足源于去噪过程中每个时间步采样的新高斯噪声，每次都重置了潜锚点，导致随机流方向相互抵消。
- 潜锚点对齐损失定义为源和目标轨迹的单步逆推潜变量的均方差。
- 将传统的速度差更新替换为基于梯度的锚点对齐更新，显式地对齐源和目标轨迹，产生几何一致的编辑。
---

# AnchorFlow: Training-Free 3D Editing via Latent Anchor-Aligned Flows

> [!tip] 核心洞察
> 随机噪声锚点引起的潜空间不一致性是编辑失败的根本原因；通过共享一个全局潜锚点并最小化源和目标轨迹的单步逆推潜变量差异，可实现更强且更稳定的语义编辑，同时保留几何结构。

| 字段 | 内容 |
|------|------|
| 中文题名 | AnchorFlow: 基于隐式锚点对齐流的免训练三维编辑 |
| 英文题名 | AnchorFlow: Training-Free 3D Editing via Latent Anchor-Aligned Flows |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2511.22357) · [Code](https://github.com/ZhenglinZhou/AnchorFlow) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | AnchorFlow |
| Dataset | Eval3DEdit |

> [!tip] 效果简介
> - Eval3DEdit (Overall) 上，CLIP_img 0.7173 vs 0.7106 (Inversion-free Editing) (+0.0067)；CLIP_txt 0.4866 vs 0.4705 (Inversion-free Editing) (+0.0161)。

## 概要

### 问题背景

免训练三维编辑旨在不重新训练模型的前提下修改三维物体的语义属性。当前主流方法依赖隐式潜锚点机制：在编辑过程中，每个时间步采样独立的高斯噪声作为潜空间参考点，源轨迹与目标轨迹围绕该锚点构建编辑流。然而，这种逐时间步采样的随机噪声锚点在不同时间步之间发生漂移，导致编辑流向不一致——部分时间步的编辑信号相互抵消，最终表现为**编辑不足**或**几何失真**。

### 核心发现与解决方案

AnchorFlow 识别出上述瓶颈的因果机制：随机噪声锚点引起的潜空间不一致性是编辑失败的根本原因。针对这一问题，方法提出两个关键设计：

1. **全局潜锚点**：建立一个在源轨迹与目标轨迹之间共享的全局潜锚点，为全时间步提供一致的潜空间参考，消除时间步间的锚点漂移。
2. **锚点对齐损失与更新规则**：通过松弛锚点对齐损失 $\mathcal{L}_{\text{align}}$ 强制源与目标轨迹的单步逆推潜变量接近，并将传统速度差欧拉更新替换为基于梯度的锚点对齐更新，显式地对齐两条轨迹。

定性消融实验（Figure 2）直观展示了三种锚点策略的效果差异：随机时间步锚点导致编辑不足与几何破损；固定锚点过度约束轨迹，使模型偏离源流形而产生过度编辑；AnchorFlow 的对齐锚点则实现了平衡的编辑效果，既满足语义修改又保持几何一致性。

### 方法定位

AnchorFlow 是一个**免训练、免掩码**的三维编辑框架，属于基于三维基础模型（LFM）的编辑方法。与需要显式掩码或优化的方法（如 **TextDeformer** 的微分渲染优化）相比，AnchorFlow 无需任何掩码标注或额外训练；与同属 LFM 路线的 **Inversion-free Editing** 基线相比，AnchorFlow 不依赖随机噪声的隐式对应，而是通过显式锚点对齐机制稳定编辑流。方法流程分为三个阶段：条件构建（多视图渲染与最优视角选择）、潜锚点对齐流采样（核心编辑过程）、网格解码（通过 Hunyuan3D 2.1 生成最终三维网格）。

### 主要结果

在 Eval3DEdit 基准上，AnchorFlow 整体 CLIP 文本相似度达到 0.4866，较 Inversion-free Editing 基线（0.4705）提升 0.0161；CLIP 图像相似度为 0.7173，略高于基线的 0.7106。消融实验表明，AnchorFlow 在几乎不增加计算开销的情况下（单次编辑约 26.71 秒，与基线持平），获得了比方向平均策略更大的性能增益。方法支持动作变化、物体添加、物体替换、风格变化四类编辑任务，在语义忠实度与几何一致性之间实现了有效平衡。

### 局限与展望

当前方法的细节保留能力受限于三维 VAE 的重建保真度，细粒度特征可能出现退化。未来高保真三维基础模型有望缓解这一限制。此外，AnchorFlow 能否扩展到动态场景或四维编辑，以及如何进一步降低锚点对齐的计算开销以支持实时编辑，仍是值得探索的开放问题。

三维内容编辑是计算机图形学与视觉计算中的核心任务，其目标在于根据用户指令修改三维形状的语义属性，同时保持几何结构的完整性和身份一致性。近年来，随着大规模三维基础模型（3D foundation models）的快速演进，基于隐式潜空间的生成式编辑方法逐渐成为主流。这类方法将三维形状编码为连续潜变量，并利用概率流模型（flow matching models）在潜空间中构建编辑轨迹，从而实现免训练（training-free）的三维编辑。

然而，当前免训练三维编辑方法面临一个关键瓶颈：**编辑过程中依赖时间步相关的随机高斯噪声作为隐式潜锚点（latent anchor）**。具体而言，在免逆推（inversion-free）编辑框架下，源轨迹由源潜变量与每个时间步独立采样的高斯噪声线性插值构成。这些随机噪声锚点在不同时间步发生漂移，导致源轨迹与目标轨迹之间的流向不一致，进而产生两类典型失败模式——**编辑不足（under-editing）**与**几何失真（geometric breakage）**。Figure 2(a) 直观展示了这一现象：随机时间步锚点引起的不一致流使得编辑效果微弱，甚至导致三维结构的断裂。

针对上述问题，已有方法尝试通过固定锚点（fixed anchor）来约束轨迹，但过度约束会使模型偏离源流形，引发**过度编辑（over-editing）**，同样无法满足实际编辑需求（Figure 2(b)）。因此，如何在潜空间中建立一致且灵活的锚点机制，成为提升免训练三维编辑质量的核心挑战。

本文的动机源于对上述失败机制的深入分析：**随机噪声锚点引起的潜空间不一致性是编辑失败的根本原因**。基于这一洞察，我们提出 **AnchorFlow**——一种免训练、免掩码的三维编辑框架。AnchorFlow 的核心思想是引入一个在源轨迹与目标轨迹之间共享的全局潜锚点，并通过显式的锚点对齐机制强制两条轨迹在潜空间中保持一致性，从而稳定编辑流。这一设计使得 AnchorFlow 能够在实现更强语义编辑的同时，有效保留源形状的几何结构，弥补了现有免训练方法的不足。

## 核心方法与创新机理

AnchorFlow 的核心创新在于揭示并解决了免训练三维编辑中的一个根本性瓶颈：**潜空间锚点漂移（Latent Anchor Drift）**。现有免训练方法（如 Inversion‑free Editing）在编辑过程中，每个时间步独立采样随机高斯噪声作为隐式潜锚点；这些锚点在不同时间步之间发生漂移，导致流向不一致，最终表现为编辑不足或几何失真（见 Figure 2a）。AnchorFlow 通过引入一个**全时间步共享的全局潜锚点**，并强制源轨迹与目标轨迹在潜空间中与该锚点对齐，从根本上稳定了编辑流。

具体而言，AnchorFlow 在三个关键模块（changed slots）上进行了针对性设计：

1. **潜锚点（Latent Anchor）**：将基线方法中“时间步相关的随机高斯噪声”替换为“源与目标轨迹共享的全局潜锚点”。该锚点通过松弛锚点对齐损失（Latent Anchor Alignment Loss）显式约束，使得源和目标轨迹在噪声空间中保持一致的参考基准，消除了随机锚点漂移带来的编辑不稳定。

2. **对齐机制（Alignment Mechanism）**：引入显式的 $\mathcal{L}_{\text{align}}$ 损失，定义为源与目标轨迹单步逆推潜变量的均方差：
   $$\mathcal{L}_{\text{align}} = \frac{1}{2} \sum_{t \in [0,1]} \| F_t(\boldsymbol{X}_t^{\text{tar}}) - F_t(\boldsymbol{X}_t^{\text{src}}) \|^2$$
   其中单步逆推近似 $F_t(X_t, t, c) \approx X_t + (1-t) v_\theta(X_t, t, c)$ 利用一阶后向步从当前状态估计噪声空间中的潜锚点。这一设计使得锚点对齐的计算开销可控，同时为后续更新提供了稳定的梯度信号。

3. **更新规则（Update Rule）**：将传统基于速度差的欧拉更新替换为基于锚点对齐损失的梯度下降更新：
   $$X_{t-\delta_t}^{\text{FE}} = X_t^{\text{FE}} - \delta_t (2 - t) \nabla_{X_t^{\text{FE}}} \mathcal{L}_{\text{align}}$$
   该更新规则显式地对齐源和目标轨迹，使编辑过程在保持语义一致性的同时，有效抑制了几何结构的破坏。

上述三个模块协同工作，使得 AnchorFlow 在无需任何训练或掩码的条件下，实现了对动作变换、物体添加、物体替换和风格变换等多种编辑任务的稳定支持。消融实验（Figure 2）直观地验证了潜锚点选择的关键作用：随机锚点导致编辑不足与几何断裂，固定锚点过度约束轨迹并偏离源流形，而 AnchorFlow 的对齐锚点则实现了平衡且一致的编辑效果。

AnchorFlow 是一个免训练、免遮罩的三维编辑框架，其整体流程围绕“条件构建—潜锚点对齐流采样—网格解码”三条主线展开，核心目标是解决现有免反转编辑方法中因随机噪声锚点漂移导致的编辑不足与几何失真问题。

**输入与输出。** 框架接收一个源三维模型和一条编辑指令，输出编辑后的三维网格。整个过程无需任何训练或微调，也不依赖显式的编辑遮罩，可直接作用于三维基础模型的隐空间。

**Pipeline 模块关系。** 如图 Figure 3 所示，系统由三个串行模块构成：

1. **条件构建（Condition Construction）**：从源模型渲染 8 个图像条件视图，利用大型多模态模型 Gemini-2.5-Flash 对视图与编辑指令的对齐程度进行排序，选取排名最高的视图作为源条件 $c_{\text{src}}$；随后通过图像编辑模型对该视图进行修改，生成目标条件 $c_{\text{tar}}$。这一步骤将三维编辑问题转化为条件驱动的隐空间轨迹对齐问题。

2. **潜锚点对齐流采样（Latent Anchor-Aligned Flow Sampling）**：这是框架的核心（详见 Algorithm 1）。给定源潜变量 $X_0^{\text{src}}$ 和条件对 $(c_{\text{src}}, c_{\text{tar}})$，模块首先构造源轨迹 $X_t^{\text{src}}$ 和目标轨迹 $X_t^{\text{tar}}$，并形成编辑轨迹 $X_t^{\text{FE}} = X_t^{\text{tar}} - X_t^{\text{src}} + X_0^{\text{src}}$。然后，在每一步去噪过程中，通过单步逆推近似估计源和目标的潜锚点 $F_t(X_t^{\text{src}})$ 与 $F_t(X_t^{\text{tar}})$，计算锚点对齐损失 $\mathcal{L}_{\text{align}}$，并以梯度下降方式更新编辑状态 $X_t^{\text{FE}}$。这一机制用全局共享的潜锚点替代了传统方法中每步独立采样的随机噪声锚点，从根本上消除了流向不一致性。

3. **网格解码（Mesh Decoding）**：最终的潜变量 $X_0^{\text{FE}}$ 通过 Hunyuan3D 2.1 解码为可用的三维网格。

**关键因果机制。** 现有免反转编辑方法在每个时间步重新采样高斯噪声，导致隐式潜锚点随时间步漂移，不同步的随机流方向相互抵消，表现为编辑不足或几何断裂（见 Figure 2a）。AnchorFlow 的因果干预在于引入一个全局潜锚点 $\mathbf{A}$，并通过松弛锚点对齐损失 $\mathcal{L}_{\text{align}} = \frac{1}{2} \sum_{t \in [0,1]} \| F_t(\mathbf{X}_t^{\text{tar}}) - F_t(\mathbf{X}_t^{\text{src}}) \|^2$ 强制源和目标轨迹在噪声空间中与该锚点对齐。更新规则从传统的速度差欧拉步替换为基于梯度的锚点对齐更新 $X_{t-\delta_t}^{\text{FE}} = X_t^{\text{FE}} - \delta_t (2 - t) \nabla_{X_t^{\text{FE}}} \mathcal{L}_{\text{align}}$，在稳定编辑流的同时保留几何结构。

**效率。** 在 NVIDIA H100 (96GB) GPU 上，每个编辑实例约耗时 26.71 秒，与基线方法 Inversion-free Editing 的运行时间相当，但编辑质量更高（见 Table 2）。

![[assets/figures/papers/paper_list_l2035_https_arxiv_org_abs_2511_22357/figures/003_Figure_3.jpg]]
*Figure 3: Overview of the AnchorFlow for Training-free and Mask-free 3D Editing. Given a source model and an editing instruction, AnchorFlow first constructs the source sample*

### 3.1 问题建模与免逆推编辑瓶颈

AnchorFlow建立在连续时间流匹配框架之上。给定源条件$c_{src}$和目标条件$c_{tar}$，潜轨迹由以下ODE控制：

$$\mathrm{d}X_t = v_\theta(X_t, t, c) \mathrm{d}t \quad \text{(Eq. 1)}$$

其中$v_\theta$为预训练的流基三维生成模型（如Hunyuan3D 2.1）的速度场，$c$为条件输入。

免逆推编辑通过构造编辑轨迹实现从源到目标的变换：

$$X_t^{\mathrm{FE}} = X_t^{\mathrm{tar}} - X_t^{\mathrm{src}} + X_0^{\mathrm{src}} \quad \text{(Eq. 2)}$$

该构造满足边界条件$X_1^{\mathrm{FE}} = X_0^{\mathrm{src}}$和$X_0^{\mathrm{FE}} = X_0^{\mathrm{tar}}$。源轨迹通过线性插值生成：

$$X_t^{\mathrm{src}} = (1 - t) X_0^{\mathrm{src}} + t N_t, \quad N_t \sim \mathcal{N}(0, I) \quad \text{(Eq. 3)}$$

**瓶颈分析**：现有免逆推编辑方法（如FlowEdit）在每个时间步独立采样高斯噪声$N_t$，这些时间步相关的随机噪声充当隐式潜锚点。由于不同时间步的锚点相互独立且发生漂移，导致流向不一致——部分流向相互抵消，最终表现为编辑不足或几何失真。这是本文识别的核心因果瓶颈。

### 3.2 全局潜锚点与对齐损失

为消除随机噪声锚点引起的不一致性，AnchorFlow引入一个在全时间步上共享的全局潜锚点$\mathbf{A}$，理想情况下满足：

$$\mathbf{A} = F_t(X_t^{\mathrm{src}}, t, c_{\mathrm{src}}) = F_t(X_t^{\mathrm{tar}}, t, c_{\mathrm{tar}}), \quad \forall t \in [0, 1] \quad \text{(Eq. 5)}$$

其中$F_t(\cdot)$表示从当前潜状态$X_t$逆向映射到噪声空间的操作。该等式要求同一锚点能同时重建源轨迹和目标轨迹，从而强制两条轨迹在潜空间中保持对齐。

由于精确求解$\mathbf{A}$不可行，将其松弛为最小二乘优化目标：

$$\min_{\mathbf{A}} \sum_{t \in [0, 1]} \left( \|F_t(X_t^{\mathrm{src}}) - \mathbf{A}\|^2 + \|F_t(X_t^{\mathrm{tar}}) - \mathbf{A}\|^2 \right) \quad \text{(Eq. 6)}$$

消去全局变量$\mathbf{A}$后，得到**松弛锚点对齐损失**：

$$\mathcal{L}_{\mathrm{align}} = \frac{1}{2} \sum_{t \in [0, 1]} \|F_t(X_t^{\mathrm{tar}}) - F_t(X_t^{\mathrm{src}})\|^2 \quad \text{(Eq. 7)}$$

该损失直接度量源轨迹与目标轨迹在噪声空间中单步逆推结果的均方差，无需显式维护全局锚点变量。

### 3.3 单步逆推近似

$F_t(\cdot)$的精确计算需要完整的逆向ODE积分，计算代价高昂。利用一阶后向步近似：

$$F_t(X_t, t, c) \approx X_t + (1 - t) v_\theta(X_t, t, c) \quad \text{(Eq. 8)}$$

该近似将当前潜状态沿速度场反方向外推一步，以极低计算成本估计对应的噪声空间锚点。

### 3.4 锚点对齐更新规则

传统免逆推编辑使用速度差进行欧拉步更新。AnchorFlow将其替换为基于$\mathcal{L}_{\mathrm{align}}$梯度的锚点对齐更新：

$$X_{t - \delta_t}^{\mathrm{FE}} = X_t^{\mathrm{FE}} - \delta_t (2 - t) \nabla_{X_t^{\mathrm{FE}}} \mathcal{L}_{\mathrm{align}} \quad \text{(Eq. 11)}$$

其中$\delta_t$为时间步长，$(2 - t)$为时间相关的缩放因子。该更新规则显式地对齐源轨迹和目标轨迹在噪声空间中的潜锚点，使得编辑轨迹在保持语义变换的同时继承源结构的几何一致性。

### 3.5 条件构建模块

AnchorFlow的条件构建流程包含三步（详见Algorithm 1）：

1. **多视图渲染与筛选**：按预定义相机分布渲染源模型的8个图像条件视图，使用大语言多模态模型（Gemini-2.5-Flash）对每个视图与编辑指令的对齐程度进行排序，选择排名最高的视图作为源条件$c_{src}$。
2. **目标条件生成**：通过图像编辑模型对选定视图进行修改，生成目标条件$c_{tar}$。
3. **网格解码**：编辑完成后的最终潜变量$X_0^{\mathrm{FE}}$通过Hunyuan3D 2.1解码为三维网格。

### 3.6 关键公式汇总

| 公式 | 表达式 | 核心含义 |
|------|--------|----------|
| Eq. 1 | $\mathrm{d}X_t = v_\theta(X_t, t, c) \mathrm{d}t$ | 流匹配ODE，控制潜轨迹演化 |
| Eq. 2 | $X_t^{\mathrm{FE}} = X_t^{\mathrm{tar}} - X_t^{\mathrm{src}} + X_0^{\mathrm{src}}$ | 免逆推编辑轨迹构造 |
| Eq. 7 | $\mathcal{L}_{\mathrm{align}} = \frac{1}{2} \sum_t \|F_t(X_t^{\mathrm{tar}}) - F_t(X_t^{\mathrm{src}})\|^2$ | 锚点对齐损失，强制源/目标轨迹一致 |
| Eq. 8 | $F_t(X_t, t, c) \approx X_t + (1 - t) v_\theta(X_t, t, c)$ | 单步逆推近似，估计噪声空间锚点 |
| Eq. 11 | $X_{t - \delta_t}^{\mathrm{FE}} = X_t^{\mathrm{FE}} - \delta_t (2 - t) \nabla_{X_t^{\mathrm{FE}}} \mathcal{L}_{\mathrm{align}}$ | 锚点对齐梯度更新规则 |

**证据强度**：Eq. 7和Eq. 11的公式形式经代码仓库验证（置信度0.98），Eq. 8的一阶近似为方法的核心计算简化手段（置信度0.95）。条件构建中Gemini-2.5-Flash的选图策略为原文明确描述的实现细节（置信度0.98）。

## 实验与关键发现

### 核心瓶颈的实证验证

AnchorFlow的设计动机源于对免训练3D编辑中“编辑不足”现象的因果分析。实验表明，Inversion-free Editing（FlowEdit）在每个去噪时间步重新采样高斯噪声，导致隐式潜锚点发生漂移，不同时间步的编辑流方向相互抵消，最终产生编辑不足或几何断裂（Figure 2a）。若简单地将所有时间步的噪声固定为同一个随机噪声，虽然能增强编辑强度，但会过度约束轨迹，使模型偏离源形状的流形，导致身份信息丢失（Figure 2b）。AnchorFlow通过共享全局潜锚点并施加松弛的锚点对齐损失，在编辑强度与几何一致性之间取得了平衡（Figure 2c），从机制上验证了“潜空间不一致性是编辑失败的根本原因”这一核心洞察。

### 主实验结果

在Eval3DEdit基准（100个编辑样本，涵盖动作变化、物体添加、物体移除、物体替换和风格变化五类任务）上，AnchorFlow取得了最优的整体性能。Table 1显示，AnchorFlow的整体CLIP_img达到0.7173，CLIP_txt达到0.4866，相较于直接基线Inversion-free Editing分别提升+0.0067和+0.0161。CLIP_txt的显著提升表明，锚点对齐机制有效缓解了编辑不足的问题，使编辑结果在语义上更贴合目标描述；CLIP_img的稳定表现则验证了全局潜锚点对源形状身份的保持能力。

定性比较（Figure 4）进一步印证了定量结论。在动作变化和物体替换等需要精细几何调整的任务中，Inversion-free Editing常出现局部编辑不足或结构断裂，而AnchorFlow在保持整体几何一致性的同时，实现了更忠实的语义编辑。值得指出的是，AnchorFlow作为免掩码方法，在局部编辑场景（如物体添加和替换）中无需显式掩码即可实现高质量编辑，展现出对编辑区域的自然聚焦能力。

![[assets/figures/papers/paper_list_l2035_https_arxiv_org_abs_2511_22357/figures/004_Figure_4.jpg]]
*Figure 4: Qualitative Comparisons. Each column shows condition pairs, source model, and the corresponding results from various baselines and our method. Compared with previous approaches, especially Inversion-Free Editing [26], our method produces edits that are both semantically faithful and geometrically consistent, effectively mitigating cases of insufficient edits and distorted geometry*

### 消融研究

**方向平均的效果**（Figure 5）：通过对多个噪声方向进行平均，可以稳定编辑流的更新方向。实验表明，方向平均对Inversion-free Editing和AnchorFlow均有正向作用，但AnchorFlow在几乎不增加计算开销的情况下获得了更大的性能增益。这验证了锚点对齐更新规则本身已具备隐式的方向稳定效果，方向平均仅作为补充的正则化手段。

**参数敏感性分析**（Figure 6, Figure 7）：关键参数 $(n_{\text{max}}, s_{\text{tar}})$ 的选择对编辑性能有显著影响。$n_{\text{max}}$ 控制锚点对齐更新的最大步数，$s_{\text{tar}}$ 控制目标条件的引导强度。实验发现，平衡设置 $n_{\text{max}}=37, s_{\text{tar}}=6.0$ 在五类编辑任务上提供了较好的折中。不同编辑类型对参数的敏感度存在差异——例如，物体替换任务对 $s_{\text{tar}}$ 更敏感，而风格变化任务对 $n_{\text{max}}$ 更敏感——这提示在实际应用中可根据编辑类型进行参数微调以获得更优效果。

### 效率与补充指标

**推理效率**（Table 2）：在NVIDIA H100 (96GB) GPU上，AnchorFlow的每实例编辑时间约为26.71秒，与Inversion-free Editing相当，但编辑质量更高。这表明锚点对齐更新规则引入的额外计算开销很小，方法具有实际部署的可行性。

**Uni3D指标验证**（Table 3）：使用Uni3D度量（Uni3D_pc用于身份保持，Uni3D_txt用于语义对齐）的补充实验进一步确认了AnchorFlow的优势。在所有LFM方法中，AnchorFlow在保持竞争性身份分数的同时，实现了最强的语义对齐，这为CLIP指标之外的评估提供了交叉验证。

### 失败模式与局限性

AnchorFlow的主要局限性来源于三维VAE的重建保真度瓶颈（Figure 8）。由于编辑过程在潜空间中进行，最终网格需通过Hunyuan3D 2.1的VAE解码器重建，细粒度几何细节（如纹理褶皱、薄壁结构）可能出现退化。这一问题并非AnchorFlow的编辑机制所致，而是当前三维基础模型共有的限制。未来更高保真度的三维基础模型有望缓解这一局限。

此外，在极端编辑场景（如大幅度的非刚性变形或完全替换主要部件）中，锚点对齐损失可能不足以完全约束几何一致性，导致局部伪影。这提示全局潜锚点假设在编辑幅度过大时可能面临挑战，需要人工核验极端案例的编辑质量。

![[assets/figures/papers/paper_list_l2035_https_arxiv_org_abs_2511_22357/figures/005_Table_1.jpg]]
*Table 1: Quantitative Comparison on Eval3DEdit. We report results using*

![[assets/figures/papers/paper_list_l2035_https_arxiv_org_abs_2511_22357/figures/008_Figure_7.jpg]]
*Figure 7: Qualitative Analysis of Parameter Selection. We visualize the effect of*

![[assets/figures/papers/paper_list_l2035_https_arxiv_org_abs_2511_22357/figures/010_Table_2.jpg]]
*Table 2: Comparison of the Time Cost. Our method matches the runtime of [26] while achieving higher editing quality*

![[assets/figures/papers/paper_list_l2035_https_arxiv_org_abs_2511_22357/figures/011_Table_3.jpg]]
*Table 3: Quantitative Comparison across Different 3D Editing Methods on the Eval3DEdit benchmark. We report results using*

## 定位与知识库关联

### 方法谱系

AnchorFlow 处于免训练三维编辑方法的前沿，其核心贡献在于识别并解决了隐式潜锚点漂移这一根本瓶颈。在方法谱系上，它直接建立在基于流匹配的免反转编辑（Inversion-free Editing，即 FlowEdit）之上，但通过引入全局潜锚点对齐机制，从根本上改变了编辑轨迹的构造方式。

**与基于优化的方法对比**：早期工作如 **TextDeformer** 依赖迭代优化来实现无掩码三维编辑，但优化过程计算开销大且收敛不稳定。AnchorFlow 完全免训练的特性使其在部署效率上具有显著优势。

**与基于重建模型的方法对比**：**MVEdit** 和 **EditP23** 等方法利用大型重建模型进行三维编辑，但受限于重建模型的泛化能力和几何一致性。AnchorFlow 直接操作于三维潜空间，避免了对中间重建质量的依赖。

**与基于流匹配的方法对比**：在流匹配范式下，**Direct Editing** 和 **Editing-by-Inversion** 代表了两种不同的编辑策略。Direct Editing 在每个时间步采样新高斯噪声，导致隐式潜锚点不断重置，这是编辑不足的根本原因——不同时间步的随机流方向相互抵消。Editing-by-Inversion 虽然通过 DDIM 反演保持了轨迹一致性，但反演过程引入额外的计算开销和累积误差。AnchorFlow 的直接基线 Inversion-free Editing（FlowEdit）通过构造 $X_t^{FE} = X_t^{tar} - X_t^{src} + X_0^{src}$ 的编辑轨迹，避免了反演，但依然继承了随机噪声锚点漂移的问题。

**AnchorFlow 的核心改进**体现在三个关键槽位：

| 模块 | 基线方法 | AnchorFlow |
|------|---------|------------|
| 潜锚点 | 时间步相关的随机高斯噪声（隐式锚点，导致漂移） | 源和目标轨迹共享的全局潜锚点，通过锚点对齐损失强制一致性 |
| 更新规则 | 速度差欧拉步（FlowEdit） | 基于锚点对齐损失的梯度下降更新 $X_{t-\delta_t}^{FE} = X_t^{FE} - \delta_t (2-t) \nabla_{X_t^{FE}} \mathcal{L}_{align}$ |
| 对齐机制 | 无显式对齐（依赖随机噪声对应） | 显式 $\mathcal{L}_{align}$ 损失，配合单步反演近似 $F_t(X_t, t, c) \approx X_t + (1-t) v_\theta(X_t, t, c)$ |

### 适用边界与局限

**适用场景**：AnchorFlow 在 Eval3DEdit 基准的五个编辑类别（动作变化、物体添加、物体移除、物体替换、风格变化）上均表现出色，尤其适用于需要同时保持几何一致性和语义对齐的编辑任务。方法无需显式掩码，支持刚性和非刚性编辑。

**已知局限**：
1. **三维 VAE 重建保真度约束**：最终编辑结果的质量受限于底层三维 VAE 的重建能力，细粒度特征可能出现退化（Figure 8）。这是当前三维基础模型的共同瓶颈。
2. **参数敏感性**：关键参数 $(n_{max}, s_{tar})$ 的选择显著影响编辑性能，不同编辑类型需要不同的参数配置（Figure 6、Figure 7）。平衡设置 $n_{max}=37, s_{tar}=6.0$ 提供了较好的折中，但并非对所有编辑类型都最优。
3. **计算效率的边际提升**：AnchorFlow 的推理时间约为每编辑实例 26.71 秒（NVIDIA H100 96GB），与 Inversion-free Editing 相当，锚点对齐机制几乎不增加额外时间开销，但也未实现显著加速。

### 开放问题

1. **高保真基础模型的集成**：未来高保真三维基础模型能否缓解 VAE 重建质量带来的限制，从而进一步提升 AnchorFlow 的细节保留能力？
2. **动态场景扩展**：AnchorFlow 的全局潜锚点对齐机制能否扩展到动态场景或四维编辑（三维+时间），在保持时序一致性的同时实现语义编辑？
3. **实时编辑支持**：如何进一步减少锚点对齐带来的额外计算量，或通过模型蒸馏、缓存策略等手段，使方法支持实时交互式编辑？
4. **多模态条件融合**：当前方法依赖单视图条件构建，能否引入多视图或多模态条件（如文本+图像联合指导）来提升编辑的精确性和鲁棒性？
5. **编辑数据规模化生成**：AnchorFlow 的免训练特性使其具备规模化生成配对三维编辑数据的潜力，如何系统性地评估和利用这一能力来训练下游编辑模型？

## 原文 PDF

![[paperPDFs/CVPR_2026/AnchorFlow_Training_Free_3D_Editing_via_Latent_Anchor_Aligned_Flows.pdf]]
