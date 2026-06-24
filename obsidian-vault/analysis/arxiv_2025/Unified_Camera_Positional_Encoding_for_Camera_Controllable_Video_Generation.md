---
title: Unified Camera Positional Encoding for Camera-Controllable Video Generation
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: paperPDFs/arxiv_2025/Unified_Camera_Positional_Encoding_for_Camera_Controllable_Video_Generation.pdf
aliases:
- UUCPE
- UCPECCVG
tags:
- arxiv_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
core_operator: 相对射线编码（Relative Ray Encoding）将每个图像标记映射到其独立的射线坐标系，使注意力在射线空间操作，而非相机空间，从而统一了任意透镜的几何推理。
primary_logic: 通过为每个token构造世界到射线的局部变换矩阵，并融合纬度-上方向图提供的绝对方向上下文，UCPE为扩散Transformer提供了与相机模型无关的、物理可解释的位置编码，使模型在异构相机设置下实现精确的可控生成。
claims:
- UCPE 在合成数据集上在所有透镜、方向和位姿控制指标上均优于基线，同时仅增加 0.5% 的参数量。
- 在 RealEstate10K 上，UCPE 无需微调即取得最低的旋转、平移和运动一致性误差，显示出强泛化性。
- 消融实验表明压缩比 1/8 和并行适配器设计最佳，替换为 PRoPE 或 GTA 会导致控制力下降。
- Synthesized dataset 上 Trainable Parameters ↓ = 35.6M
---

# Unified Camera Positional Encoding for Camera-Controllable Video Generation

> [!tip] 核心洞察
> 通过为每个token构造世界到射线的局部变换矩阵，并融合纬度-上方向图提供的绝对方向上下文，UCPE为扩散Transformer提供了与相机模型无关的、物理可解释的位置编码，使模型在异构相机设置下实现精确的可控生成。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向相机可控视频生成的统一相机位置编码 |
| 英文题名 | Unified Camera Positional Encoding for Camera-Controllable Video Generation |
| 会议/期刊 | arXiv 2025 |
| Links | [paper](https://arxiv.org/abs/2512.07237) · [Code](https://github.com/chengzhag/UCPE) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation |
| Method | UCPE (Unified Camera Positional Encoding) |
| Dataset | Synthesized dataset, RealEstate10K |

> [!tip] 效果简介
> - Synthesized dataset 上，Trainable Parameters ↓ 35.6M vs ReCamMaster (~355M) (90% fewer)；Lens Control (k1 error) ↓ 0.129 vs ReCamMaster (fails to reproduce intended distortion) (qualitative improvement)。
> - RealEstate10K (Out-of-distribution) 上，Rotation Error (RotErr) ↓ 0.56 vs best competing method (lowest (see Table 2))；Video Quality (Q-Align) ↑ 0.9694 vs CameraCtrl / AC3D (higher)。

## 概述

### 问题瓶颈

现有相机可控视频生成方法普遍依赖**针孔相机模型**假设，其位置编码（如 Plücker 编码、投影位置编码或直接参数化）无法统一表达鱼眼、广角等镜头的**非线性畸变**与**非中心投影**。这导致三个连锁困境：跨相机类型的泛化能力弱；缺乏对绝对俯仰角和横滚角的显式控制，使生成视频的朝向模糊；以及编码在相机空间而非射线空间操作，难以捕捉像素级几何差异。

### 核心方法：统一相机位置编码（UCPE）

本文提出 **UCPE（Unified Camera Positional Encoding）**，一个与相机模型无关的框架，将完整的相机几何——包括 6-DoF 位姿、内参和畸变——注入扩散 Transformer 的注意力机制。其核心由三个模块构成：

- **相对射线编码（Relative Ray Encoding, RRE）**：为每个图像 token 构造独立的局部射线坐标系，将注意力计算从相机空间转移到**射线空间**，使模型能统一推理任意透镜的几何关系。
- **绝对朝向编码（Absolute Orientation Encoding, AOE）**：通过纬度-上方向图（Lat-Up map）为每个 token 提供重力对齐的绝对方向上下文，实现对俯仰角和横滚角的显式控制。
- **空间注意力适配器（Spatial Attention Adapter）**：一个与原始自注意力并行的轻量分支，融合 RRE 与 RoPE 的混合编码，并通过零初始化线性层注入，在保持预训练先验的同时仅增加 **0.5% 的可训练参数**（35.5M / 7.3B）。

### 方法定位

UCPE 在方法谱系中处于**射线级、模型无关**的位置编码范式。相较于 **ReCamMaster**（直接参数注入，参数量约 355M，缺乏几何可解释性）、**CameraCtrl / AC3D**（基于 Plücker 编码的 U-Net/ControlNet 方法，限于针孔模型）、**PRoPE**（相对投影编码，同样限于针孔）和 **GTA**（相对相机编码，变换查询-键-值），UCPE 首次以射线为粒度、以任意射线映射函数 $\Phi_\psi$ 为桥梁，统一了异构相机几何下的可控生成。

### 核心结论

- **合成数据集**：UCPE 在所有镜头、朝向和位姿控制指标上均优于基线，同时参数量比 ReCamMaster 减少 90%，视频质量（Q-Align）保持竞争力。
- **RealEstate10K 零样本泛化**：无需微调即取得最低的旋转误差（0.56）、平移误差和运动一致性误差，且 Q-Align 得分（0.9694）高于在该数据集上训练的 CameraCtrl 和 AC3D。
- **消融实验**：空间注意力适配器的压缩比为 1/8 时可控性与保真度最佳；并行适配器设计优于前置或后置；将 RRE 替换为 PRoPE 或 GTA 会显著削弱镜头与位姿控制力。
- **推理效率**：在单块 NVIDIA A800 上生成 81 帧 480×832 视频约需 184 秒，与 ReCamMaster（179 秒）相当。

### 局限与开放问题

当前 UCPE 依赖精确的位姿监督，且未覆盖变焦、聚焦、景深等镜头属性。对训练时未见过的极端投影模型（如等距柱状投影 ERP），生成质量明显下降。未来方向包括：扩展至更多镜头属性、减少对位姿监督的依赖、与 NeRF/3DGS 表示的结合，以及在视频到视频任务中的验证。

## 背景与动机

### 相机可控视频生成的兴起与核心挑战

视频扩散模型近年来取得了显著进展，使得高质量的文生视频成为可能。然而，生成具有精确相机控制的视频仍然是一个开放性问题。在实际应用中，用户不仅希望控制相机的6自由度位姿（平移与旋转），还需要指定镜头类型（如鱼眼、针孔）、视场角以及畸变参数，以实现电影级的创作自由度。

当前相机可控视频生成方法的核心瓶颈在于**编码方式的局限性**。现有方法普遍假设针孔相机模型，将相机参数编码为全局的、与相机坐标系绑定的表示。这种设计在以下两个关键维度上存在根本性缺陷：

1. **跨镜头类型的泛化能力差**：针孔假设无法统一表示鱼眼镜头、全景相机等具有非线性畸变和非中心投影的镜头模型。当用户切换镜头类型时，编码的几何解释性丧失，导致生成质量急剧下降。
2. **绝对方向控制缺失**：现有方法通常不显式编码相机的俯仰角（pitch）和横滚角（roll），导致生成视频中地平线倾斜或仰角模糊，无法满足对绝对方向有严格要求的应用场景。

### 现有编码范式的局限

Figure 2 对比了三种主流的相机编码范式及其各自的不足：

- **直接参数化**（Direct Parameterization，Figure 2a）：将相机内参和外参作为原始数值直接注入模型。这种方法缺乏几何可解释性，且在不同相机类型之间不兼容。代表方法如 **ReCamMaster**，虽扩展至支持畸变参数，但参数量大，泛化能力有限。
- **Plücker 编码**（Plücker Encoding，Figure 2b）：将每条射线表示为一对方向和矩向量，提供了物理上有意义的描述。然而，这种表示是**绝对的、坐标依赖的**，使得模型难以学习相对相机运动的规律。基于此的方法包括 **CameraCtrl**（注入U-Net时间注意力）和 **AC3D**（基于ControlNet）。
- **投影位置编码**（Projective Positional Encoding，Figure 2c）：如 **PRoPE** 和 **GTA**，在投影空间中编码相对相机关系，但**仍然假设针孔投影**，无法建模非线性镜头畸变。

这些方法的共同缺陷在于：它们要么在相机空间操作（将所有像素的编码绑定到同一相机坐标系），要么受限于特定的投影模型，无法为扩散Transformer提供一种**与相机模型无关的、物理可解释的位置编码**。

### 本文动机：从相机空间到射线空间

本文的核心洞察是：**将位置编码从相机空间迁移到射线空间**。在射线空间中，每个图像标记（token）对应其自身的观测射线，注意力机制直接在射线间的相对几何关系上操作，而非依赖全局相机坐标系。这种设计天然地统一了任意透镜的几何推理——无论底层投影模型如何复杂，每条射线的局部坐标系都可以用统一的方式构建。

基于这一洞察，本文提出 **UCPE（Unified Camera Positional Encoding）**，一种相机模型无关的框架，将完整的相机几何信息——包括6自由度位姿、内参和畸变——注入Transformer注意力。UCPE通过两个互补的编码组件实现这一目标：

- **相对射线编码**（Relative Ray Encoding）：为每个token构建世界到射线的局部变换矩阵，使注意力在射线空间操作。
- **绝对方向编码**（Absolute Orientation Encoding）：通过纬度-上方向图（Lat-Up Map）提供重力对齐的绝对方向上下文，使模型能够显式控制俯仰角和横滚角。

这两种编码的结合，使得UCPE能够在异构相机设置下实现精确的可控生成，同时仅增加极少的可训练参数（约35.5M，占7.3B基座模型的0.5%）。

## 核心创新

### 问题瓶颈：从相机空间到射线空间的范式转移

现有相机可控视频生成方法的核心瓶颈在于**编码粒度和投影模型的局限**。主流方案（如基于 Plücker 编码的 **CameraCtrl** 和 **AC3D**，以及直接参数注入的 **ReCamMaster**）均在相机级别（camera-level）共享编码，即同一视图内的所有图像标记（token）使用相同的相机参数。这种设计隐含地假设了针孔投影模型，无法统一表示鱼眼、全景等非线性畸变和非中心投影。此外，这些方法缺乏对绝对方向（俯仰角 pitch 和横滚角 roll）的显式控制，导致生成结果中相机朝向的歧义性。

UCPE 的核心洞察在于：**将几何推理从相机空间迁移到射线空间**。每个像素对应一条独立的世界空间观测射线，不同相机模型的差异仅体现在从像素坐标到射线的映射函数 $\Phi_{\psi}$ 上。通过为每个 token 构建其专属的射线坐标系，注意力机制得以直接在射线空间操作，从而天然地统一了任意透镜几何。

### Changed Slots：三个维度的关键改进

| 设计维度 | 基线方法 | UCPE 方案 | 改进机制 |
|:---|:---|:---|:---|
| **编码粒度** | 相机级共享 | 射线级独立（per-token） | 每个 token 对应其观测射线的局部坐标变换，捕捉细粒度几何变化 |
| **投影模型** | 仅针孔 | 模型无关（通过 $\Phi_{\psi}$ 统一） | 任意相机模型仅需替换射线映射函数，无需修改编码框架 |
| **全局方向** | 未控制（俯仰/横滚模糊） | 通过 Lat-Up 图显式控制 | 纬度图提供绝对仰角，上方向图锚定重力对齐的参考方向 |

### 相对射线编码（RRE）：射线空间的几何推理

RRE 的核心操作是为每个图像 token $t$ 构造一个局部射线到世界的变换矩阵 $\mathbf{T}_t^{\mathrm{wr}}$。具体而言，以 token 对应的世界空间射线方向 $\mathbf{d}_t$ 为 z 轴，以该帧相机的向下方向 $\mathbf{y}_{i(t)}^{\mathrm{cam}}$ 为辅助向量，构建正交基：

$$\mathbf{z}_t = \mathbf{d}_t,\; \mathbf{x}_t = \mathbf{y}_{i(t)}^{\mathrm{cam}} \times \mathbf{z}_t,\; \mathbf{y}_t = \mathbf{z}_t \times \mathbf{x}_t$$

该正交基与射线原点 $\mathbf{o}_t$ 共同构成 $\mathbf{T}_t^{\mathrm{wr}} \in SE(3)$。与 **PRoPE**（限于针孔的相对投影编码）和 **GTA**（变换查询、键、值的相对相机编码）相比，RRE 的关键优势在于：变换矩阵的定义完全基于射线的局部几何，不依赖于特定投影模型，因此能统一处理针孔、UCM、甚至训练中未见过的相机模型（如 Brown-Conrady 模型，仅需在推理时替换 $\Phi_{\psi}$）。

### 绝对方向编码（AOE）：Lat-Up 图的物理可解释性

AOE 通过两个互补的物理量提供全局方向上下文：

- **纬度图** $\mathrm{Lat}_t = \arctan2(-d_{t,y}, \sqrt{d_{t,x}^2 + d_{t,z}^2})$：编码射线相对于水平面的仰角，直接对应俯仰角信息。
- **上方向图** $\mathrm{Up}_t$：通过向世界向上方向微扰后投影的归一化像素位移定义，编码横滚角信息。

Lat-Up 编码 $[\mathrm{Lat}_t, \mathrm{Up}_t]$ 为每个 token 提供了明确的绝对方向锚点，使模型能够在生成过程中精确控制相机的俯仰和横滚。消融实验证实，加入 AOE 不仅提升了方向控制精度，还通过提供外观线索间接改善了镜头控制效果。

### 混合编码与空间注意力适配器

UCPE 的最终编码采用块对角混合形式：

$$\mathbf{D}_t^{\mathrm{UCPE}} = \mathrm{blkdiag}(\mathbf{D}_t^{\mathrm{Ray}},\; \mathbf{D}_t^{\mathrm{RoPE}})$$

其中 $\mathbf{D}_t^{\mathrm{Ray}}$ 来自 RRE 的射线空间变换，$\mathbf{D}_t^{\mathrm{RoPE}}$ 保留旋转位置编码以维持序列建模能力。这种混合设计使模型同时具备射线空间的几何推理能力和序列位置的相对关系建模。

编码通过一个**并行于原始自注意力的轻量适配器**注入预训练 Transformer。该适配器（Spatial Attention Adapter）采用 LoRA 风格的旁路设计，仅引入 35.5M 可训练参数（占 7.3B 基座模型的 0.5%），在保持预训练先验的同时实现精确的相机控制。消融实验表明：并行位置优于前置（Pre-Attn）或后置（Post-Attn）变体；1/8 维度的压缩比在可控性和保真度之间取得最佳平衡；替换为 PRoPE 或 GTA 会导致镜头控制和位姿控制显著下降。

### 方法谱系与知识库定位

UCPE 处于**相机可控生成**与**位置编码设计**的交叉点。相较于直接参数化方法（**ReCamMaster**），UCPE 提供了物理可解释的几何编码；相较于 Plücker 编码方法（**CameraCtrl**、**AC3D**、**Wan CameraCtrl**），UCPE 通过射线级粒度和模型无关设计突破了针孔假设的限制；相较于相对投影编码（**PRoPE**、**GTA**），UCPE 通过局部射线坐标系的构建统一了任意透镜的几何推理。其核心贡献在于首次实现了对异构相机几何（6-DoF 位姿、内参、畸变）的统一位置编码，为扩散 Transformer 提供了与相机模型无关的可控生成能力。

## 整体框架

UCPE 的整体设计遵循一个核心原则：将扩散 Transformer 中的几何推理从相机空间迁移到射线空间，并通过轻量适配器注入预训练模型，从而在不破坏原有先验的前提下实现跨相机模型的精确可控生成。整个框架围绕三个相互协作的模块构建：**相对射线编码（Relative Ray Encoding, RRE）**、**绝对方向编码（Absolute Orientation Encoding, AOE）** 和 **空间注意力适配器（Spatial Attention Adapter）**。

### 输入与预处理

框架的输入包括两部分：用户文本提示和完整的相机参数。相机参数涵盖三类信息：
- **6-DoF 位姿**：每帧的世界坐标系下旋转矩阵 $\mathbf{R}$ 和平移向量 $\mathbf{t}$。
- **内参与畸变**：由统一的射线映射函数 $\Phi_{\psi}$ 描述，该函数将任意像素坐标 $(u, v)$ 映射到相机坐标系下的射线原点 $\mathbf{o}_{u,v}^{\mathrm{cam}}$ 和方向 $\mathbf{d}_{u,v}^{\mathrm{cam}}$。这一抽象层使得 UCPE 天然兼容针孔、UCM 乃至未训练的相机模型（如 Brown-Conrady），只需替换 $\Phi_{\psi}$ 即可。
- **绝对方向**：可选的俯仰角和横滚角，通过纬度-上方向图（Lat-Up map）显式指定。

每个视频帧的每个像素被表示为一个图像 token，预处理阶段为其计算世界坐标系下的射线表示：
$$d_{u,v} = \mathbf{R} d_{u,v}^{\mathrm{cam}}, \quad o_{u,v} = t.$$
由此，每个 token $t$ 获得其世界空间中的射线参数化 $r_t = (o_t, d_t)$。

### 模块关系与数据流

三个模块的协作流程如下：

1. **相对射线编码（RRE）** 为每个 token 构建从世界坐标系到局部射线坐标系的变换矩阵。具体而言，以射线方向 $\mathbf{d}_t$ 为 z 轴，以相机向下方向为辅助向量，构建正交基：
$$\mathbf{z}_t = \mathbf{d}_t, \; \mathbf{x}_t = \mathbf{y}_{i(t)}^{\mathrm{cam}} \times \mathbf{z}_t, \; \mathbf{y}_t = \mathbf{z}_t \times \mathbf{x}_t.$$
由此得到局部射线到世界的变换矩阵 $\mathbf{T}_t^{\mathrm{wr}}$。这一逐 token 的变换使得注意力机制能够在射线空间而非相机空间操作，从而统一了任意透镜下的几何推理。

2. **绝对方向编码（AOE）** 为每个 token 提供全局方向上下文。通过计算射线相对于水平面的仰角得到纬度图 $\mathrm{Lat}_t$，通过向世界向上方向微扰后投影的像素位移得到归一化的上方向图 $\mathrm{Up}_t$。两者拼接为 Lat-Up 编码，使模型能够显式控制相机的俯仰角和横滚角。

3. **空间注意力适配器** 将上述两种编码融合并注入预训练 Transformer。适配器采用并行于原始自注意力的轻量分支设计（LoRA 风格），构建混合编码算子：
$$\mathbf{D}_t^{\mathrm{UCPE}} = \mathrm{blkdiag}\big( \mathbf{D}_t^{\mathrm{Ray}}, \; \mathbf{D}_t^{\mathrm{RoPE}} \big).$$
该算子将相对射线编码与 RoPE 结合，在空间注意力中施加几何变换，最终通过零初始化的线性层将相机感知的 token 特征融合回主干网络。

### 设计决策与证据

**并行适配器的位置选择**是关键设计点。消融实验表明，将适配器置于自注意力之前（Pre-Attn）或之后（Post-Attn）均会导致相机控制力和视频质量的明显下降，而并行设计在保持预训练先验的同时实现了最佳的可控性-保真度平衡。此外，适配器内部的压缩比选择也经过验证：1/8 维度的压缩在可控性和保真度之间取得最优折衷。

**射线级编码粒度**是 UCPE 区别于先前方法的根本差异。传统方法（如 ReCamMaster、CameraCtrl）在相机级别编码，所有 token 共享相同的几何表示，无法捕捉像素间的细微几何差异。UCPE 通过为每个 token 构建独立的射线坐标系，使注意力机制能够感知逐像素的几何变化，这是其在异构相机设置下实现精确控制的核心机制。

**绝对方向控制的引入**解决了现有方法中俯仰角和横滚角模糊的问题。Lat-Up 图不仅提供了明确的全局方向参考，还作为外观线索改善了镜头控制效果（Table 1 中 UCPE w/ vs. w/o Absolute Orientation 的对比验证了这一点）。

整个框架仅引入 35.5M 可训练参数（占 7.3B 基座模型的 0.5%），比 ReCamMaster 少 90%，却在合成数据集的所有控制指标上取得一致最优，并在 RealEstate10K 上无需微调即展现出强泛化能力。

### 补充图表

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2512_07237/figures/002_Figure_2.jpg]]
*Figure 2: Comparison of camera encoding methods. (a) Direct Parameterization encodes camera intrinsics and extrinsics as raw parameters, which lacks geometric interpretability and compatibility across camera types. (b) Plucker Encoding ¨ represents each ray as a pair of direction and moment vectors, providing a physically grounded but absolute, coordinate-dependent description. (c) Projective Positional Encoding encodes relative cameras in projective space, yet assumes pinhole projection and cannot model non-linear lens distortions. (d) Our Relative Ray Encoding reformulates geometric relationships in ray space, where each token corresponds to its own viewing ray, enabling better pose generalization...*

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2512_07237/figures/003_Figure_3.jpg]]
*Figure 3: Overview of Spatial Attention Adapter. The adapter injects UCPE into pretrained Transformers through a lightweight branch that preserves pretrained priors. It constructs hybrid encoding from the world-to-ray transform*

## 核心模块与公式推导

### 3.1 问题形式化：从相机模型到世界空间射线

UCPE 的核心前提是：**任意相机模型均可归结为一个射线映射函数**。给定相机参数 $\psi$（内参和畸变系数），每个像素坐标 $(u,v)$ 通过映射函数 $\Phi_{\psi}$ 唯一确定一条相机坐标系下的射线：

$$(o_{u,v}^{\mathrm{cam}}, d_{u,v}^{\mathrm{cam}}) = \Phi_{\psi}(u,v)$$

其中 $o_{u,v}^{\mathrm{cam}} \in \mathbb{R}^3$ 为射线原点，$d_{u,v}^{\mathrm{cam}} \in \mathbb{S}^2$ 为归一化方向。随后通过相机外参——旋转矩阵 $\mathbf{R}$ 和平移向量 $t$——将射线变换到世界坐标系：

$$d_{u,v} = \mathbf{R} \, d_{u,v}^{\mathrm{cam}}, \quad o_{u,v} = t \tag{1}$$

这一统一形式使得 UCPE 能够以模型无关的方式表示针孔、鱼眼、UCM 等异构相机，为后续的射线空间编码奠定基础。

---

### 3.2 相对射线编码（Relative Ray Encoding, RRE）

现有方法（如 Plücker 编码、PRoPE）要么在绝对世界坐标系下描述射线，要么局限于针孔假设，导致跨相机类型的泛化能力差。RRE 的核心创新在于：**为每个图像 token 构建独立的局部射线坐标系，使注意力机制直接在射线空间而非相机空间操作**。

对于每个图像 token $t$，其对应的世界空间射线记为 $r_t = (o_t, d_t)$，其中 $o_t \in \mathbb{R}^3$ 为原点，$d_t \in \mathbb{S}^2$ 为单位方向。RRE 以射线方向 $d_t$ 作为局部坐标系的 $z$ 轴，并利用该 token 所属帧的相机向下方向 $y_{i(t)}^{\mathrm{cam}}$ 构建正交基：

$$\mathbf{z}_t = \mathbf{d}_t, \quad \mathbf{x}_t = \mathbf{y}_{i(t)}^{\mathrm{cam}} \times \mathbf{z}_t, \quad \mathbf{y}_t = \mathbf{z}_t \times \mathbf{x}_t \tag{6}$$

由此得到局部射线到世界的变换矩阵：

$$\mathbf{T}_t^{\mathrm{wr}} = \begin{bmatrix} \mathbf{R}_t^{\mathrm{wr}} & \mathbf{t}_t^{\mathrm{wr}} \\ \mathbf{0}^{\top} & 1 \end{bmatrix} \tag{7}$$

其中 $\mathbf{R}_t^{\mathrm{wr}} = [\mathbf{x}_t, \mathbf{y}_t, \mathbf{z}_t]$ 为旋转部分，$\mathbf{t}_t^{\mathrm{wr}} = o_t$ 为平移部分。该矩阵将局部射线坐标系中的几何关系映射回世界空间，使得任意两个 token 之间的相对几何关系可以在统一的射线空间中计算，**天然兼容任意透镜的投影非线性**。

---

### 3.3 绝对方向编码（Absolute Orientation Encoding, AOE）

RRE 解决了相对几何推理问题，但缺乏对相机绝对姿态（俯仰角 pitch 和横滚角 roll）的显式控制——这是现有相机编码方法的共同盲区。AOE 通过引入一个与重力对齐的“上方向”参考来解决这一问题，输出 **Lat-Up 图**作为全局方向上下文。

**Latitude 图** 计算射线相对于水平面的仰角：

$$\mathrm{Lat}_t = \arctan2\big(-d_{t,y}, \sqrt{d_{t,x}^2 + d_{t,z}^2}\big) \tag{8}$$

其中 $d_{t,y}$ 为射线方向在世界坐标系 $y$ 轴（重力反方向）的分量。

**Up 图** 通过微扰法计算：将相机原点沿世界向上方向微扰后重新投影，得到像素位移 $[\Delta u_t, \Delta v_t]$，归一化后编码横滚信息：

$$\mathrm{Up}_t = \frac{[\Delta u_t, \Delta v_t]}{\lVert [\Delta u_t, \Delta v_t] \rVert} \tag{9}$$

将 Lat 和 Up 拼接后通过浅层 MLP 注入空间注意力适配器，为每个 token 提供显式的俯仰和横滚控制信号。

---

### 3.4 混合位置编码与空间注意力适配器

UCPE 采用**混合编码策略**：将 RRE 的射线几何编码与 RoPE 的位置编码融合，形成统一的块对角算子：

$$\mathbf{D}_t^{\mathrm{UCPE}} = \mathrm{blkdiag}\big(\mathbf{D}_t^{\mathrm{Ray}}, \; \mathbf{D}_t^{\mathrm{RoPE}}\big) \tag{10}$$

其中 $\mathbf{D}_t^{\mathrm{Ray}}$ 由 $\mathbf{T}_t^{\mathrm{wr}}$ 的逆矩阵 $\mathbf{T}_t^{\mathrm{rw}}$ 构造，负责射线空间的几何推理；$\mathbf{D}_t^{\mathrm{RoPE}}$ 保留标准的旋转位置编码，维持序列建模能力。

**空间注意力适配器**（Spatial Attention Adapter）以并行分支形式注入 UCPE：在预训练 Transformer 的原始自注意力旁路增加一个轻量分支，该分支接收混合编码 $\mathbf{D}_t^{\mathrm{UCPE}}$ 和 Lat-Up 嵌入，执行相机感知的注意力计算后，通过零初始化的线性层融合回主分支。这一设计（图 3）在保持预训练先验的同时，仅增加 35.5M 可训练参数（基座模型 7.3B 的 0.5%），且适配器位置消融实验证实**并行设计显著优于前置或后置**。

---

### 3.5 关键公式变量速查

| 符号 | 含义 | 公式 |
|------|------|------|
| $\Phi_{\psi}$ | 相机射线映射函数 | $\Phi_{\psi}: (u,v) \mapsto (o_{u,v}^{\mathrm{cam}}, d_{u,v}^{\mathrm{cam}})$ |
| $\mathbf{T}_t^{\mathrm{wr}}$ | 局部射线到世界的变换矩阵 | Eq. (7) |
| $\mathrm{Lat}_t$ | 射线仰角（纬度） | Eq. (8) |
| $\mathrm{Up}_t$ | 归一化像素上方向 | Eq. (9) |
| $\mathbf{D}_t^{\mathrm{UCPE}}$ | 混合位置编码算子 | Eq. (10) |

---

### 3.6 与基线方法的本质差异

图 2 系统对比了四类相机编码范式：(a) **直接参数化**（ReCamMaster 采用）将原始相机参数注入网络，缺乏几何可解释性；(b) **Plücker 编码**（CameraCtrl、AC3D 采用）在绝对坐标系下描述射线，是坐标依赖的全局表示；(c) **投影位置编码**（PRoPE 采用）在投影空间编码相对相机关系，但限于针孔假设。UCPE 的 RRE（图 2d）将几何关系重构到**每个 token 自身的射线空间**，既保留了相对编码的泛化优势，又通过射线映射函数 $\Phi_{\psi}$ 统一了任意透镜的非线性投影。消融实验直接验证了这一优势：将 RRE 替换为 PRoPE 或 GTA 后，镜头控制和位姿控制指标均显著下降。

### 补充图表

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2512_07237/figures/011_Figure.jpg]]
*Figure: D.1. Implementation of Baseline And Ablation Models. (a) ReCamMaster injects per-frame camera parameters into each Transformer block after spatial repetition. (b) Wan CameraCtrl injects Plucker-encoded rays into video tokens using a convolutional ¨ adapter. (c) Our UCPE ablations insert a spatial attention adapter before, after, or in parallel with the original self-attention module*

## 实验与分析

### 主实验结果

#### 合成数据集上的可控性与质量评估

我们在自建的合成数据集上对 UCPE 与多个基线方法进行了全面对比（Table 1）。该数据集包含约 48k 个从 360° 视频中合成的片段，使用统一相机模型（UCM）渲染，覆盖了不同的透镜畸变参数、6-DoF 相机位姿以及绝对方向控制。评估指标涵盖镜头控制（k1 误差）、方向控制（俯仰角/横滚角误差）和相对位姿控制（旋转/平移误差），同时以视频质量指标（FVD、Q-Align）衡量生成保真度。

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2512_07237/figures/006_Table_1.jpg]]
*Table 1: Quantitative comparison on our synthesized dataset. UCPE outperforms all baselines across lens, orientation, and pose control while maintaining strong video quality with 90% fewer parameters than ReCamMaster. Under both w/o and w/ Absolute Orientation Control, it yields lower pitch, roll, and rotation errors. Ablation results (bottom) show that moderate compression ratios in the Spatial Attention Adapter (e.g., 1/8-dim) best balance controllability and fidelity. Gray cells denote metrics not applicable due to missing control. Here, 1/C-dim denotes the token projection compression ratio, and ($d\times n)$ are the per-head dimension and number of attention heads*

**UCPE 在所有控制维度上一致优于基线**，同时仅引入 35.5M 可训练参数——占 7.3B 基座模型的 0.5%，比 ReCamMaster 少约 90%。在无绝对方向控制（w/o Absolute Orientation）和有绝对方向控制（w/ Absolute Orientation）两种配置下，UCPE 均取得了更低的俯仰角、横滚角和旋转误差。值得注意的是，Lat-Up 图不仅提供了方向控制信号，其外观线索还进一步改善了镜头控制效果（UCPE w/ vs. w/o Absolute Orientation 对比）。

定性结果（Figure 4）印证了量化发现：UCPE 忠实跟随目标轨迹，并生成与 Lat-Up 图可视化一致的透镜畸变效果。相比之下，Wan CameraCtrl 出现相机运动偏差，而 ReCamMaster 未能复现预期的畸变模式。

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2512_07237/figures/004_Figure_4.jpg]]
*Figure 4: Comparison on our synthesized dataset. UCPE faithfully follows target trajectories and produces consistent lens distortions aligned with visualization of the Lat-Up Map. In contrast, Wan CameraCtrl shows camera motion deviations, while ReCam-Master fails to reproduce the intended distortion. Colors correspond to the highlighted effects in the figure*

#### RealEstate10K 上的跨域泛化

为验证 UCPE 的泛化能力，我们在 RealEstate10K 数据集上进行了零样本评估（Table 2）。测试采用 100 个随机选取的片段，统一配置为 100° 水平视场角的针孔相机。**UCPE 无需微调即取得了最低的旋转误差（0.56）、平移误差和运动一致性误差**，且 Q-Align 得分（0.9694）高于在 RealEstate10K 上训练的 CameraCtrl 和 AC3D。这一结果说明，UCPE 的射线空间编码策略使其能够适应训练时未见过的场景分布和相机配置。

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2512_07237/figures/007_Table_2.jpg]]
*Table 2: Quantitative comparison on RealEstate10K. UCPE generalizes well without fine-tuning, achieving the lowest rotation, translation, and motion errors, and showing higher Q-Align scores than models trained on RealEstate10K (CameraCtrl and AC3D)*

定性对比（Figure 5）进一步展示了 UCPE 的优势：生成的帧更清晰、细节更丰富，且更好地跟随目标相机运动。CameraCtrl 在部分场景中产生严重伪影和构图失衡，AC3D 保留了训练数据集的美学特征但出现取景偏差和低动态范围问题。尽管 Wan CameraCtrl 和 ReCamMaster 基于相同的基座模型，它们在针孔设置下仍面临相机一致性挑战，表现为运动减弱或非预期的畸变伪影。

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2512_07237/figures/005_Figure_5.jpg]]
*Figure 5: Comparison on the RealEstate10K dataset. UCPE generates sharper, more detailed frames that better follow the target camera motion. CameraCtrl produces severe artifacts (left) and poor composition (right), while AC3D preserves the training dataset’s aesthetic but shows unbalanced framing (left) and low dynamic range (right). Wan CameraCtrl and ReCamMaster, though based the same backbone, struggle with camera consistency, leading to reduced motion (left) and undesired distortion artifacts (right) under the pinhole setup*

### 消融实验

我们在合成数据集上系统验证了 UCPE 各组件的设计选择（Table 1 下半部分）。

**空间注意力适配器的压缩比**是影响可控性与保真度平衡的关键因素。实验表明，中等压缩比（1/8 维度）取得了最优结果：过低的压缩比导致控制力不足，而过高的压缩比则损害视频质量。

**适配器的插入位置**对性能有显著影响。与并行设计相比，前置（Pre-Attn）和后置（Post-Attn）变体在相机控制和视频质量上均明显退化（Figure D.1c 展示了三种架构）。并行适配器通过零初始化线性层融合相机感知特征，有效保留了预训练先验。

**相对射线编码（RRE）的替换实验**验证了其核心贡献。将 RRE 替换为 PRoPE（限于针孔模型的相对投影位置编码）或 GTA（相对相机编码，变换查询、键和值）后，镜头控制和相对位姿控制均显著减弱，视频质量下降。这证实了射线空间建模对于统一异构相机几何的必要性。

### 推理效率

在单块 NVIDIA A800 GPU 上测得的推理延迟（Table D.1）显示，UCPE 的额外计算开销保持在可接受范围内。具体延迟数值因帧数和分辨率而异，详见附录表格。

### 鲁棒性与扩展应用

**文本-相机冲突鲁棒性**：即使文本提示指定“长焦”视角，UCPE 仍能正确合成鱼眼视频（Figure E.1），表明相机编码信号能够覆盖矛盾的语义先验。

**未见相机模型的泛化**：在推理时仅替换射线映射函数 Φ_ψ，UCPE 即可泛化至训练时未观察到的模型（如 Brown-Conrady 畸变模型），无需额外微调（Figure E.2）。

**图像到视频（I2V）任务**：我们在 Wan2.1-I2V-14B 上进行微调，验证了 UCPE 在 I2V 任务上的可行性（Figure E.4）。

### 失败模式与局限

**极端投影模型**：当测试等距柱状投影（ERP）射线映射时，生成结果出现明显伪影（Figure E.3）。这是因为模型在训练期间未接触此类极端全景投影，表明 UCPE 的泛化能力在分布外投影类型上仍存在边界。

**未建模的相机属性**：当前 UCPE 仅编码位姿、内参和畸变参数，尚未包含变焦、聚焦、景深等更丰富的镜头属性。这些属性的控制需要额外的条件信号和训练数据。

**位姿监督依赖**：UCPE 的训练依赖精确的位姿标注，这在实际应用中可能难以获取。如何通过自监督几何损失减少对精确监督的依赖，是一个有待探索的方向。

### 方法谱系与知识库定位

在相机可控视频生成的方法谱系中，UCPE 的定位可从以下几个维度理解：

- **相对于直接参数化方法**：ReCamMaster 通过直接注入原始相机参数实现控制，缺乏几何可解释性和跨相机类型的兼容性。UCPE 通过射线映射函数 Φ_ψ 统一了任意透镜的几何推理，解决了这一瓶颈。

- **相对于 Plücker 编码方法**：CameraCtrl 和 AC3D 基于 Plücker 坐标，将射线表示为方向-矩向量对，具有物理基础但本质上是绝对坐标描述。Wan CameraCtrl 在此基础上引入卷积适配器。UCPE 的 RRE 将每个 token 映射到其独立的射线坐标系，使注意力在射线空间而非相机空间操作，实现了更好的位姿泛化能力。

- **相对于投影位置编码**：PRoPE 在投影空间中编码相对相机关系，但假设针孔投影，无法建模非线性透镜畸变。UCPE 的模型无关设计突破了这一限制。

- **绝对方向控制的引入**：现有方法普遍缺乏对俯仰角和横滚角的显式控制。UCPE 的 AOE 通过 Lat-Up 图提供重力对齐的绝对方向参考，填补了这一空白。

总体而言，UCPE 为扩散 Transformer 提供了一种与相机模型无关的、物理可解释的位置编码方案，在异构相机设置下实现了精确的可控生成，同时保持了极低的参数开销。

### 补充图表

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2512_07237/figures/012_Table.jpg]]
*Table: D.1. Inference latency comparison. Latencies are measured on a single NVIDIA A800 GPU, with corresponding frame counts and resolutions provided for reference*

## 方法谱系与知识库定位

### 1. 核心瓶颈与动机

现有相机可控视频生成方法在编码相机几何信息时，普遍存在两个根本性局限，构成UCPE设计的直接动机：

**瓶颈一：针孔模型假设导致的跨相机泛化失败。** 绝大多数方法（如基于Plücker编码的CameraCtrl、AC3D，以及基于相对投影编码的PRoPE）均假定相机遵循理想的针孔投影模型。当面对鱼眼镜头、广角镜头等具有显著非线性畸变的真实相机时，这些方法要么完全无法建模畸变，要么需要为每种相机重新设计编码方案。直接注入原始相机参数的方法（如ReCamMaster）虽然理论上可以扩展支持畸变参数，但缺乏几何可解释性，参数空间与视觉特征之间的关系不透明，导致控制精度和泛化能力受限。

**瓶颈二：绝对方向控制的缺失。** 现有方法仅编码相对位姿变化，无法显式指定相机的绝对俯仰角（pitch）和横滚角（roll）。这意味着在生成过程中，模型对“重力方向”的感知是模糊的——用户无法精确控制地平线的倾斜程度或相机的仰角，导致生成结果在方向一致性上存在不可控的随机性。

### 2. 方法谱系：从相机级编码到射线级编码

UCPE在方法谱系中的定位，可以通过编码粒度和投影模型两个维度来刻画：

| 方法 | 编码粒度 | 投影模型 | 绝对方向 |
|------|---------|---------|---------|
| Direct Parameterization (ReCamMaster) | 相机级（逐帧共享） | 可扩展但缺乏几何解释 | 无 |
| Plücker Encoding (CameraCtrl, AC3D, Wan CameraCtrl) | 射线级（绝对坐标） | 针孔模型 | 无 |
| Projective PE (PRoPE) | 射线级（相对坐标） | 针孔模型 | 无 |
| GTA (Relative Camera Encoding) | 射线级（相对坐标） | 针孔模型 | 无 |
| **UCPE (本文)** | **射线级（局部射线坐标）** | **模型无关（通过Φ_ψ统一）** | **Lat-Up编码** |

**关键跃迁：从“相机空间”到“射线空间”的注意力操作。** PRoPE和GTA虽然也引入了相对编码的思想，但它们仍然在相机投影空间中进行几何推理，依赖于针孔模型的线性投影假设。UCPE的核心创新在于为每个图像token构建独立的局部射线坐标系——以该像素对应的世界空间射线方向为z轴，相机向下方向为辅助轴，形成一个正交基。这使得自注意力机制中的几何关系计算完全发生在“射线空间”中，而非“相机空间”中。这一转变的深层意义在于：无论底层相机模型是针孔、鱼眼还是全景，每个像素最终都对应一条世界空间中的射线；在射线空间中，几何关系的表达是统一的、模型无关的。

**与基线方法的具体关系：**

- **ReCamMaster**：作为直接参数注入的代表，ReCamMaster将相机内参和外参展平为向量后注入Transformer。UCPE在参数效率上具有显著优势——仅增加35.5M参数（基座模型7.3B的0.5%），而ReCamMaster需要约355M可训练参数（90%更多）。更重要的是，ReCamMaster缺乏几何可解释性，其控制信号与视觉特征之间的映射是隐式的，导致在镜头畸变控制上表现不佳（Table 1中k1误差显著高于UCPE）。

- **Wan CameraCtrl**：基于Plücker编码和卷积适配器的方法。Plücker编码将每条射线表示为方向向量和矩向量的对，虽然具有物理基础，但是绝对坐标依赖的——它描述的是射线在世界坐标系中的绝对位置，而非token之间的相对几何关系。这限制了其对相对位姿变化的建模能力。此外，Plücker编码同样限于针孔模型。

- **CameraCtrl / AC3D**：这两个方法将Plücker编码注入U-Net架构（而非DiT），在RealEstate10K上训练。UCPE无需在RealEstate10K上微调即可取得更低的旋转误差（RotErr 0.56）和更高的视频质量（Q-Align 0.9694），显示出更强的泛化能力（Table 2）。

- **PRoPE / GTA**：这两个方法与UCPE的“相对射线编码”最为接近，但消融实验（Table 1底部）直接验证了关键差异——将UCPE的相对射线编码替换为PRoPE或GTA后，镜头控制和相对位姿控制指标均显著下降，视频质量也降低。这证实了“射线空间”编码相对于“投影空间”编码的优势。

### 3. 知识库定位与适用边界

**UCPE贡献的知识增量：**

1. **统一相机几何编码框架**：通过射线映射函数Φ_ψ，UCPE将任意相机模型（针孔、UCM、Brown-Conrady等）统一为从像素坐标到世界空间射线的映射。这一抽象使得编码方案与具体相机模型解耦，实现了真正的“模型无关”几何推理。

2. **绝对方向编码机制**：Lat-Up编码通过计算射线相对于水平面的仰角（Lat_t）和世界向上方向在像素平面的投影（Up_t），为每个token提供了重力对齐的全局方向上下文。这使得用户可以在生成时显式控制相机的俯仰角和横滚角，填补了现有方法的空白。

3. **轻量适配器集成范式**：空间注意力适配器以并行分支的形式注入UCPE，通过零初始化线性层融合，保持了预训练先验的完整性。消融实验表明，并行位置优于前置（Pre-Attn）或后置（Post-Attn）变体。

**适用边界与局限：**

- **位姿监督依赖**：UCPE的训练需要精确的相机位姿标注。当前框架仅建模位姿、内参和畸变，尚未涵盖变焦、聚焦、景深等更丰富的镜头属性。对于缺乏精确位姿监督的场景，需要探索自监督几何损失的可能性。

- **极端投影模型的泛化限制**：虽然UCPE在训练中未见过的Brown-Conrady模型上展现出一定的泛化能力（Figure E.2），但对于训练分布之外的极端投影（如等距柱状投影ERP），生成质量明显下降，出现显著伪影（Figure E.3）。这表明模型的泛化依赖于训练数据的投影分布覆盖度。

- **任务范围约束**：当前验证集中在文生视频（T2V）和图生视频（I2V）任务，尚未在视频到视频（V2V）或更复杂的3D重建/新视角合成任务上验证。

### 4. 开放问题

基于UCPE的当前设计，以下方向值得进一步探索：

1. **扩展可控维度**：能否将UCPE的编码框架扩展，以同时控制变焦（zoom）、聚焦（focus）和景深（depth of field）？这需要在射线映射函数Φ_ψ中引入额外的连续参数。

2. **减少位姿监督依赖**：是否可以通过自监督的几何一致性损失（如相邻帧之间的重投影误差）来减少对精确位姿标注的依赖，使UCPE能够在更广泛的数据上训练？

3. **与3D表示的融合**：UCPE的射线空间编码与NeRF、3D Gaussian Splatting等基于射线的3D表示存在天然的接口。是否可以将UCPE与这些表示无缝结合，用于更高质量的3D感知视频生成或新视角合成？

4. **视频到视频任务的适配**：在视频到视频任务中，输入视频本身携带的相机运动信息如何与UCPE的显式控制信号协调，是一个尚未探索的问题。

## 原文 PDF

![[paperPDFs/arxiv_2025/Unified_Camera_Positional_Encoding_for_Camera_Controllable_Video_Generation.pdf]]