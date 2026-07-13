---
title: Human Interaction-Aware 3D Reconstruction from a Single Image
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Human_Interaction_Aware_3D_Reconstruction_from_a_Single_Image.pdf
project_link: "https://jongheean11.github.io/HUG3D"
code_link: null
aliases:
- HIA3RFSI
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 引入群体-实例多视图扩散模型 (HUG-MVD) 与物理约束的几何优化 (HUG-GR)，实现一致的遮挡补全和交互建模。
primary_logic: 将透视图像变换到规范正交空间以消除尺度歧义，利用群体-实例联合扩散先验补全遮挡区域，并通过物理约束优化网格以强制交互合理性。
claims:
- 在MultiHuman数据集上，HUG3D在所有几何指标（CD, P2S, NC）上均显著优于基线，CD从5.644降至3.631（↓35.7%），NC从0.754提升至0.811
- 在遮挡区域评估中，HUG3D的几何误差（Norm L2）从0.197降至0.140，纹理质量（PSNR）从6.157提升至8.388
- 消融实验证实，移除群体-实例建模或物理约束导致性能大幅下降（CD增加约146%，NC下降约1.5%）
- 统计检验（Wilcoxon signed-rank）表明所有指标上的优势均具有统计显著性（p < 0.001）
---

# Human Interaction-Aware 3D Reconstruction from a Single Image

> [!tip] 核心洞察
> 将透视图像变换到规范正交空间以消除尺度歧义，利用群体-实例联合扩散先验补全遮挡区域，并通过物理约束优化网格以强制交互合理性。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向交互感知的单张图像多人三维重建 |
| 英文题名 | Human Interaction-Aware 3D Reconstruction from a Single Image |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2604.05436) · [Project](https://jongheean11.github.io/HUG3D) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | HUG3D |
| Dataset | MultiHuman |

> [!tip] 效果简介
> - MultiHuman 上，CD (cm) ↓ 3.631 vs 5.644 (SIFU) (-35.7%)；P2S (cm) ↓ 1.752 vs 2.284 (SIFU) (-23.3%)；NC ↑ 0.811 vs 0.754 (SIFU) (+7.6%)。

## 概要

**问题瓶颈**：从单张透视图像重建交互中的多人三维模型面临三重挑战——（1）透视畸变导致几何尺度歧义，（2）现有方法独立处理每个个体，缺乏对群体交互的显式建模，导致接触区域穿透和几何失真，（3）遮挡区域纹理与几何缺失，难以补全（Figure 1）。现有单人类方法（如 **ECON**、**SIFU**、**SiTH**、**PSHuman**）在多人类场景中仅独立重建后拼合，无法推理遮挡与交互关系；多目方法（**DeepMultiCap**）或视频方法（**Multiply**）虽能处理多人，但依赖多视角或时序信息，不适用于单图输入。

**核心思路与因果机制**：HUG3D 通过三个关键设计突破瓶颈。首先，**规范透视-正交视图变换（Pers2Ortho）**将透视输入映射到规范正交空间，消除尺度歧义并为多视图推理提供一致表示（Sec. 3.1）。其次，**群体-实例多视图扩散模型（HUG-MVD）**联合群体与个体信息，在六个规范视图上同时去噪 RGB 和法向图，以隐式交互先验补全遮挡区域的几何与纹理（Sec. 3.2）。最后，**物理约束的几何优化（HUG-GR）**引入群体-实例法向监督、穿透惩罚损失和可见性损失，强制网格在接触区域保持物理合理性（Sec. 3.3.1）。

**方法定位**：HUG3D 属于单目多人三维重建方法，其核心创新在于将多视图扩散与交互感知几何优化相结合。与单人类方法相比，HUG3D 显式建模群体交互与遮挡补全；与多目/视频方法相比，HUG3D 仅需单张图像输入。方法依赖 SMPL-X 姿态初始化，并在单人类数据集（全监督）和多人类数据集（部分几何监督）上联合训练 HUG-MVD。

**主要结果**：在 MultiHuman 数据集上，HUG3D 在所有几何指标上显著优于最强基线：CD 从 5.644 cm 降至 3.631 cm（↓35.7%），P2S 从 2.284 cm 降至 1.752 cm（↓23.3%），NC 从 0.754 提升至 0.811（Table 1）。在遮挡区域评估中，几何误差（Norm L2）从 0.197 降至 0.140，纹理质量（PSNR）从 6.157 提升至 8.388（Table 3）。消融实验证实，移除群体-实例建模或物理约束导致 CD 增加约 146%、NC 下降约 1.5%（Table S15），且所有优势在 Wilcoxon signed-rank 检验下具有统计显著性（p < 0.001，Table S14）。

**局限与开放问题**：方法对环境光照变化敏感，未显式建模物体遮挡，且依赖 SMPL-X 初始化精度。未来方向包括引入物体感知推理、提升极端光照鲁棒性，以及减少对参数化姿态先验的依赖。

从单张图像重建三维人体是计算机视觉与图形学中的核心问题，在虚拟现实、数字人、影视制作等领域有广泛应用前景。近年来，基于数据驱动的方法在**单人体三维重建**上取得了显著进展——从参数化模型（如SMPL/SMPL-X）的拟合，到隐式神经表示与扩散先验驱动的精细化重建，单人的几何与纹理质量已达到较高水平。

然而，当场景中存在**多人**时，问题复杂度发生质变。多人场景不仅涉及多个个体的独立重建，更关键的是个体之间的**空间交互、相互遮挡与物理接触**。现有方法在面对此类场景时暴露出三个核心瓶颈：

1. **透视畸变与尺度歧义**：单张透视图像中，不同深度的人体呈现不同的尺度与形状失真。现有方法通常独立处理每个人，缺乏统一的规范空间表示，导致重建结果在全局坐标系中尺度不一致、空间关系错乱。

2. **交互感知建模缺失**：绝大多数方法将多人场景拆解为独立的单人体重建后简单组合，完全忽略了人与人之间的接触约束。这使得重建结果在接触区域频繁出现**几何穿透、表面分离**等物理不合理现象，无法保持交互的连贯性。

3. **遮挡区域补全困难**：多人交互必然伴随大面积相互遮挡。单人体方法缺乏对遮挡区域的推理能力，导致被遮挡部分的几何缺失和纹理空洞，而简单的图像修复又难以保证多视图一致性。

上述问题共同指向一个根本性缺口：**现有方法缺乏群体层面的交互先验与遮挡推理机制**，仅停留在实例级别的独立处理。这直接限制了单目多人三维重建在实际场景中的应用——无论是体育赛事分析、社交VR，还是影视级的多人数字替身生成，都需要重建结果在几何精度、物理合理性与视觉真实感上同时满足要求。

本文提出的 **HUG3D** 框架正是针对这一缺口设计。其核心动机在于：将多人重建从“独立重建后拼合”的范式转变为**交互感知的联合重建**范式，通过引入群体-实例多视图扩散先验与物理约束优化，系统性地解决透视畸变、遮挡补全与交互建模三大挑战。

## 核心方法与创新机理

HUG3D 的核心创新在于将单目多人三维重建从“独立个体重建后拼合”的范式，推进到“群体交互感知的联合重建”。与现有方法相比，该方法在三个关键环节上实现了根本性改变：

### 1. 从透视独立处理到规范正交群体表示（Pers2Ortho）

现有单人类方法（如 **ECON**、**SIFU**、**SiTH**、**PSHuman**）在多人场景中均采用独立裁剪、分别重建的策略，直接在透视图像空间操作。这一方式存在两个根本缺陷：其一，透视投影导致的近大远小效应使不同个体的尺度关系发生畸变；其二，独立处理完全丧失了群体层面的空间上下文。

HUG3D 提出 **Canonical Perspective-to-Orthographic View Transform (Pers2Ortho)**（Sec. 3.1），将输入透视图像变换到规范正交空间。具体而言，该模块首先利用 Sapiens 预测的深度和法向图，通过几何损失 $\mathcal{L}_{\mathrm{geo}} = \| d_{\mathrm{Sap}}^{\prime\mathrm{in}} - d_{\mathcal{M}}^{\prime\mathrm{in}} \|_2^2 + 1 - \langle n_{\mathrm{Sap}}^{\mathrm{in}}, n_{\mathcal{M}}^{\mathrm{in}} \rangle$ 优化部分三维网格，然后通过正交投影 $\mathcal{P}_i = \mathbf{R}_i \cdot \mathcal{P} + \mathbf{T}_i$ 将稠密点云重投影到 6 个规范视图中。这一变换的核心价值在于：**消除了透视尺度歧义**，使不同个体的空间关系在同一尺度下保持一致，为后续多视图扩散模型提供了几何上可操作的输入空间。消融实验可视化（Fig. 6a, Fig. S25）证实，相比直接使用透视图像或 Era3D，Pers2Ortho 显著提高了投影清晰度并保留了细节。

### 2. 从单实例修复到群体-实例联合扩散先验（HUG-MVD）

单人类方法在遭遇遮挡时，通常只能依赖单实例的修复能力，缺乏对遮挡区域背后内容的合理推断。HUG3D 的核心突破在于 **Human Group-Instance Multi-View Diffusion (HUG-MVD)**（Sec. 3.2），它构建了一个群体与实例信息联合建模的扩散先验。

该扩散模型在 6 个规范视图上联合去噪 RGB 和法向图，训练目标为：
$$\mathcal{L}_{\mathrm{diff}} = \sum_{i=0}^{5} \big( \mathbb{E}_{t,\epsilon} [ \| \epsilon - \epsilon_{\theta}(z_{t,\mathrm{rgb}}^{(i)}, t, x_{\mathrm{mask}}^{(i)}, n_{\mathrm{SMPLX}}^{(i)}) \|_2^2 ] + \mathbb{E}_{t,\epsilon} [ \| \epsilon - \epsilon_{\theta}(z_{t,\mathrm{normal}}^{(i)}, t, x_{\mathrm{mask}}^{(i)}, n_{\mathrm{SMPLX}}^{(i)}) \|_2^2 ] \big)$$

其创新性体现在两个层面：**数据层面**，模型同时在单人类数据集（完整监督，覆盖广泛体型）和多人数据集（部分几何，捕获真实交互）上训练，使模型既能生成高质量个体几何，又能理解群体交互模式；**架构层面**，实例到群体的潜在合成（Instance-to-group latent composition）机制确保了表面连续性，消融实验（Table 4）表明移除此机制会导致性能显著下降。这一设计使得 HUG-MVD 不仅能补全遮挡区域的几何和纹理，更关键的是——它充当了**隐式的物理交互先验**，确保补全结果在群体层面具有物理合理性。

### 3. 从无约束几何优化到物理约束的群体-实例优化（HUG-GR）

现有方法在几何优化阶段通常仅使用单一实例损失，缺乏对多人交互物理合理性的显式约束。HUG3D 的 **Human Group-Instance Geometric Reconstruction (HUG-GR)**（Sec. 3.3.1）引入了三类物理感知约束：

- **群体-实例法向监督**：$\mathcal{L}_{\mathrm{normal}} = \lambda_{\mathrm{group}} \cdot \mathcal{L}_{\mathrm{group}} + \lambda_{\mathrm{inst}} \cdot \mathcal{L}_{\mathrm{instance}}$，同时从群体整体和个体两个粒度驱动网格优化，确保局部细节与全局一致性。

- **穿透惩罚损失**：$\mathcal{L}_{\mathrm{pen}} = \mathrm{mean}_{V} [ \xi \ln (1 + e^{(\mathrm{tol} - |s_1^{i,j} - s_2^{i,j}|)/\xi}) ]$，对接触部件对之间的距离小于阈值进行软惩罚，从根本上解决了多人重建中常见的身体穿透问题。

- **可见性损失**：$\mathcal{L}_{\mathrm{vis}} = \frac{1}{2B} \sum_{k=1}^{K} \sum_{b=1}^{B} \frac{E_b^k}{M_b^k + \epsilon}$，强制渲染掩膜中的遮挡关系与真实掩膜一致，确保网格可见性符合输入图像。

消融实验（Fig. 6b, Table S15）证实，这三类约束各自对最终几何质量有正面贡献，且移除物理约束后 CD 增加约 146%、NC 下降约 1.5%，充分验证了物理感知优化在多人重建中的必要性。

### 创新总结

HUG3D 的三项核心创新构成了一个完整的因果链条：**Pers2Ortho** 解决了“在哪里重建”的表示问题，为多人场景提供了尺度一致的规范空间；**HUG-MVD** 解决了“重建什么”的生成问题，利用群体-实例联合先验补全遮挡区域；**HUG-GR** 解决了“如何保证合理”的约束问题，通过物理感知优化强制交互一致性。这三者协同作用，使得 HUG3D 在 MultiHuman 数据集上实现了 CD 从 5.644 降至 3.631（↓35.7%）、NC 从 0.754 提升至 0.811 的显著性能跃升。

HUG3D 的整体流程由三个核心阶段构成，如图 2 所示：**规范透视-正交视图变换 (Pers2Ortho)**、**群体-实例多视图扩散 (HUG-MVD)** 以及**带纹理网格重建**。给定一张包含多人的单目透视图像，系统首先通过 Pers2Ortho 将其转换到规范正交空间，消除透视畸变和尺度歧义，生成一致的六视图正交表示；随后 HUG-MVD 以此为条件，联合去噪生成多视图 RGB 与法向图，补全被遮挡的几何和纹理区域；最后，在物理约束的几何优化 (HUG-GR) 和遮挡感知纹理融合的驱动下，输出具有交互一致性的带纹理三维网格。

**Pers2Ortho** 是整个管线的入口模块。它利用现成的单目法向/深度估计器（Sapiens）预测初始部分几何，并通过可微渲染与预测深度、法向的对齐损失优化一个粗糙的部分网格；随后将该网格升采样为稠密点云 (PCD)，经正交投影重投影至六个规范视点，生成多视图 RGB 图像和法向图。这一变换的核心价值在于：透视投影下，同一人体在不同图像位置会产生尺度失真，而正交投影消除了这种歧义，使后续多视图扩散模型能够在空间一致的条件下进行推理（见图 3 的对比验证）。

**HUG-MVD** 是一个以多视图掩码 RGB 和 SMPL-X 法向图为条件的扩散模型，在六个规范视图上联合去噪 RGB 和法向。其关键设计在于**群体-实例联合建模**：训练时同时使用单人数据集（提供完整监督，覆盖丰富的体型和身份）和多人数据集（提供部分几何，捕获真实交互模式）；推理时，通过实例到群体的潜在合成 (Instance-to-group latent composition) 将个体特征融合为群体一致的表示，从而在补全遮挡区域的同时维持交互合理性。

**带纹理网格重建**阶段包含几何优化 (HUG-GR) 和纹理融合两个子模块。HUG-GR 以 SMPL-X 网格为初始几何，利用 HUG-MVD 生成的群体-实例多视图法向作为监督信号，结合**穿透惩罚损失**和**可见性损失**进行可微优化。穿透损失对接触部件对之间的过近距离施加软惩罚，防止身体穿透；可见性损失则强制渲染掩膜与真实掩膜一致，消除错误遮挡。纹理融合阶段将多视图 RGB 投影至优化后的网格顶点，并通过遮挡感知加权混合和人脸修复（CodeFormer）生成高保真纹理。对高频语义区域（手部、面部）施加更细粒度的学习率，以提升局部精度。

整个管线是模块化串联的：Pers2Ortho 的输出作为 HUG-MVD 的条件输入，HUG-MVD 的生成结果又作为 HUG-GR 的监督信号。这种设计使得各阶段的错误不会完全阻断下游，但上游质量仍对最终结果有显著影响——例如，若 SMPL-X 姿态估计严重错误，Pers2Ortho 生成的初始几何将偏离真实形状，进而影响扩散模型的补全质量和网格优化的收敛方向。

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2604_05436/figures/003_Figure_2.jpg]]
*Figure 2: Overview of our HUG3D framework. Given a single perspective image, (1) the Canonical Perspective-to-Orthographic View Transform (Pers2Ortho) converts it into a canonical multi-view orthographic representation to resolve scale ambiguity and enable consistent multi-view reasoning. (2) The Human Group-Instance Multi-View Diffusion (HUG-MVD) model completes occluded geometry and texture while maintaining plausible interactions. (3) The Textured Mesh Reconstruction stage refines the mesh and generates high-fidelity textures with our physics-based Human Group-Instance Geometry Reconstruction (HUG-GR), which enforces physical consistency via optimization with multi-view normal cues and interaction...*

HUG3D 框架由四个核心模块级联构成，形成从单张透视图像到带纹理多人三维网格的完整管线（Figure 2）。下面按处理顺序逐一阐述各模块的设计逻辑与关键公式。

### 3.1 规范透视-正交视图变换（Pers2Ortho）

**动机**：透视投影导致不同个体的尺度歧义和几何畸变，直接进行多视图扩散难以保证一致性。Pers2Ortho 将输入变换到规范正交空间，消除尺度歧义，为后续多视图推理提供统一坐标系。

**流程**：
1. **初始几何估计**：使用 Sapiens 从输入透视图像预测每个个体的深度图 $d_{\mathrm{Sap}}$ 和法向图 $n_{\mathrm{Sap}}$，同时拟合 SMPL-X 模型获得初始网格 $\mathcal{M}$。
2. **几何优化**：通过最小化 Sapiens 预测与可微渲染网格之间的差异，优化部分三维几何。损失函数为：

   $$\mathcal{L}_{\mathrm{geo}} = \| d_{\mathrm{Sap}}^{\prime\mathrm{in}} - d_{\mathcal{M}}^{\prime\mathrm{in}} \|_2^2 + 1 - \langle n_{\mathrm{Sap}}^{\mathrm{in}}, n_{\mathcal{M}}^{\mathrm{in}} \rangle \tag{1}$$

   其中 $d_{\mathcal{M}}^{\prime\mathrm{in}}$ 和 $n_{\mathcal{M}}^{\mathrm{in}}$ 为网格 $\mathcal{M}$ 在输入视图下的渲染深度和法向，$d_{\mathrm{Sap}}^{\prime\mathrm{in}}$ 和 $n_{\mathrm{Sap}}^{\mathrm{in}}$ 为 Sapiens 的对应预测。该损失同时约束深度 L2 距离和法向余弦相似度。

3. **PCD 重投影**：将优化后的稠密点云 $\mathcal{P}$ 通过正交投影变换到 6 个规范视图：

   $$\mathcal{P}_i = \Pi_{\mathrm{ortho}}^i(\mathcal{P}) = \mathbf{R}_i \cdot \mathcal{P} + \mathbf{T}_i \tag{2}$$

   其中 $\mathbf{R}_i$ 和 $\mathbf{T}_i$ 为第 $i$ 个规范视图的旋转矩阵和平移向量。相比网格顶点着色，PCD 重投影保留了可见区域的稠密外观细节，同时维持跨视图的空间一致性。

**效果**：Figure 3 的对比表明，基于正交视图训练的多视图扩散模型在投影清晰度和细节保留上显著优于透视视图训练。

### 3.2 群体-实例多视图扩散（HUG-MVD）

**动机**：遮挡区域缺乏几何和纹理信息，需要生成式先验进行补全。同时，多人场景要求生成结果在群体层面保持交互合理性。

**设计**：HUG-MVD 是一个条件扩散模型，在 6 个规范视图上联合去噪 RGB 和法向图。训练目标为：

$$\mathcal{L}_{\mathrm{diff}} = \sum_{i=0}^{5} \Big( \mathbb{E}_{t,\epsilon} [ \| \epsilon - \epsilon_{\theta}(z_{t,\mathrm{rgb}}^{(i)}, t, x_{\mathrm{mask}}^{(i)}, n_{\mathrm{SMPLX}}^{(i)}) \|_2^2 ] + \mathbb{E}_{t,\epsilon} [ \| \epsilon - \epsilon_{\theta}(z_{t,\mathrm{normal}}^{(i)}, t, x_{\mathrm{mask}}^{(i)}, n_{\mathrm{SMPLX}}^{(i)}) \|_2^2 ] \Big) \tag{3}$$

其中 $z_{t,\mathrm{rgb}}^{(i)}$ 和 $z_{t,\mathrm{normal}}^{(i)}$ 为第 $i$ 个视图中带噪的 RGB 和法向潜变量，条件信号包括掩膜 RGB $x_{\mathrm{mask}}^{(i)}$ 和 SMPL-X 法向图 $n_{\mathrm{SMPLX}}^{(i)}$。

**关键机制**：
- **群体-实例联合训练**：同时使用单人类数据集（完整监督，覆盖广泛体型与身份）和多人数据集（部分几何，捕获真实交互与遮挡模式），使模型既能生成高质量个体细节，又能理解群体上下文。
- **实例到群体的潜在合成**：在去噪过程中，将个体潜在表示合成为群体潜在表示，保持表面连续性。消融实验（Table 4）表明，移除该机制会导致性能显著下降。

### 3.3 纹理网格重建

#### 3.3.1 群体-实例几何重建（HUG-GR）

HUG-GR 利用多视图法向线索和物理约束优化初始 SMPL-X 网格，消除穿透并保持交互一致性。

**群体-实例法向损失**：结合群体级和实例级法向监督：

$$\mathcal{L}_{\mathrm{normal}} = \lambda_{\mathrm{group}} \cdot \mathcal{L}_{\mathrm{group}} + \lambda_{\mathrm{inst}} \cdot \mathcal{L}_{\mathrm{instance}} \tag{5}$$

其中群体法向损失为跨 6 个视图的余弦距离之和：

$$\mathcal{L}_{\mathrm{group}} = \sum_{i=0}^{5} \left( 1 - \langle n_{\mathrm{MVD,group}}^{(i)}, n_{\mathcal{M},\mathrm{group}}^{(i)} \rangle \right) \tag{6}$$

实例级损失 $\mathcal{L}_{\mathrm{instance}}$ 同理作用于每个个体网格。

**穿透惩罚损失**：对接触部件对之间的距离小于阈值进行软惩罚，防止身体穿透：

$$\mathcal{L}_{\mathrm{pen}} = \mathrm{mean}_{V} [ \xi \ln (1 + e^{(\mathrm{tol} - |s_1^{i,j} - s_2^{i,j}|)/\xi}) ] \tag{7}$$

其中 $s_1^{i,j}$ 和 $s_2^{i,j}$ 为接触部件对的表面点，$\mathrm{tol}$ 为距离容差，$\xi$ 控制惩罚的软硬程度。

**可见性损失**：强制渲染掩膜与真实掩膜一致，测量错误遮挡像素的比例：

$$\mathcal{L}_{\mathrm{vis}} = \frac{1}{2B} \sum_{k=1}^{K} \sum_{b=1}^{B} \frac{E_b^k}{M_b^k + \epsilon} \tag{8}$$

其中 $E_b^k$ 为第 $k$ 个个体在第 $b$ 个视图中的错误遮挡像素数，$M_b^k$ 为真实掩膜像素数。

**自适应区域优化**：对高频语义区域（手部、面部）应用更精细的学习率，在保持整体形状稳定性的同时提升局部精度。

#### 3.3.2 遮挡与视图感知纹理融合

将多视图 RGB 投影到优化后的网格上生成全身顶点纹理，通过遮挡感知混合策略融合各视图贡献，并对人脸区域进行专项修复（CodeFormer），最终生成高保真带纹理三维模型。

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2604_05436/figures/004_Figure_3.jpg]]
*Figure 3: Comparison of results from multi-view diffusion trained on perspective vs. orthographic images*

## 实验与关键发现

### 主实验结果

HUG3D 在 MultiHuman 数据集上与多个基线方法进行了定量比较。由于目前尚无直接面向单张图像多人重建的公开基线，实验涵盖了单人类方法（**ECON**、**SIFU**、**SiTH**、**PSHuman**）的独立重建组合版本，以及多目多人方法（**DeepMultiCap**）和视频多人方法（**Multiply**）。为公平比较，所有基于 SMPL 的方法均使用真实 SMPL-X 姿态，单人类方法采用真实实例掩膜裁剪后独立重建并在同一坐标框架中对齐组合。

**几何精度**：如表 1 所示，HUG3D 在所有几何指标上均显著优于最优基线。倒角距离（CD）从 SIFU 的 5.644 cm 降至 3.631 cm（↓35.7%），点面距离（P2S）从 2.284 cm 降至 1.752 cm（↓23.3%），法向一致性（NC）从 0.754 提升至 0.811（+7.6%）。特别在接触精度（CP）指标上，HUG3D 达到 0.240，远超 DeepMultiCap 的 0.083（+189%），表明其交互感知重建能力显著优于依赖多目输入的现有方法。

**纹理质量**：如表 2 所示，HUG3D 在纹理质量上也全面领先。PSNR 达到 16.456（SIFU 为 15.202，+8.2%），LPIPS 降至 0.168（SIFU 为 0.202，↓16.8%），SSIM 为 0.754（SIFU 为 0.730）。

**遮挡区域重建**：表 3 专门评估了遮挡区域的几何与纹理质量。HUG3D 在遮挡区域的几何误差（Norm L2）从 0.197 降至 0.140（↓28.9%），纹理 PSNR 从 6.157 提升至 8.388（+36.2%），验证了群体-实例多视图扩散模型（HUG-MVD）对遮挡补全的关键作用。

**统计显著性**：Wilcoxon signed-rank 检验（Table S14）表明，HUG3D 在所有指标上的优势均具有统计显著性（p < 0.001）。

### 交互程度分层分析

为评估交互强度对重建质量的影响，实验按交互程度（低、中、高）对 MultiHuman 测试样本进行分层。Table S8 和 Table S9 显示，HUG3D 在所有交互级别上均保持优势，且在高交互场景下优势更为明显——这直接归因于 HUG-MVD 的群体-实例联合建模和 HUG-GR 的物理约束优化。遮挡区域的分层评估（Table S10）进一步证实，交互越强、遮挡越严重时，HUG3D 的相对提升越大。

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2604_05436/figures/033_Table_S.8.jpg]]
*Table S.8: Quantitative comparison of geometry depending on level of interaction*

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2604_05436/figures/040_Table_S.9.jpg]]
*Table S.9: Quantitative comparison of texture depending on level of interaction*

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2604_05436/figures/041_Table_S.10.jpg]]
*Table S.10: Quantitative comparison within occluded regions depending on level of interaction*

### 端到端评估

Table S6 展示了使用 RoBUDDI 预测的掩膜、SMPL-X 参数和相机估计进行端到端评估的结果。尽管输入包含预测误差，HUG3D 仍优于所有基线，证明了该方法对不完美初始化的鲁棒性。

### 消融实验

**Pers2Ortho 变换**：Figure 6(a) 和 Figure S25 的定性对比表明，相比直接使用透视图像或 Era3D，Pers2Ortho 变换显著提高了多视图投影的清晰度并保留了细节。正交空间消除了透视畸变，使后续扩散模型能生成更一致的多视图输出。

**HUG-MVD 训练策略**：Table 4 的消融显示，同时使用群体数据和个体数据训练优于单独使用任何一方。移除实例到群体的潜在合成（w/o Instance-to-group latent composition）导致表面连续性显著下降，证实了该机制对保持群体一致性的必要性。

**HUG-GR 损失函数**：Figure 6(b) 的可视化消融表明，自适应区域优化、穿透损失和可见性损失均对最终几何质量有正面贡献。移除任一组分都会导致接触区域的穿透或几何失真。

**交互感知建模**：Table S15 的消融实验证实，交互感知建模在两个阶段（HUG-MVD 和 HUG-GR）都必不可少。移除群体-实例建模或物理约束后，CD 增加约 146%，NC 下降约 1.5%，接触区域指标显著恶化。

### 失败模式与局限性

尽管 HUG3D 在多数场景下表现优异，仍存在以下已知失败模式：

1. **光照条件敏感**：方法基于环境光照假设，训练数据光照一致。在低光或强对比光照条件下，纹理生成可能出现瑕疵，法向估计精度下降。
2. **物体交互未建模**：当人体手持或与之交互的物体被误识别为身体一部分时，会导致几何畸变。方法未显式建模物体遮挡。
3. **姿态初始化依赖**：HUG3D 依赖 SMPL-X 姿态初始化。严重错误的姿态估计（如肢体方向完全颠倒）可能导致重建几何与输入图像出现偏差，且后续优化难以完全纠正。
4. **极端遮挡**：当多人重叠区域过大、几乎完全遮挡时，HUG-MVD 的幻觉能力有限，可能产生不合理的几何或纹理。

这些失败模式指向了未来改进方向：引入物体感知推理、提高对复杂光照的鲁棒性、以及减少对 SMPL-X 初始化的依赖。

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2604_05436/figures/017_Table_4.jpg]]
*Table 4: Ablation study of key components in HUG3D. We report geometry (CD, P2S, Norm L2) and texture (PSNR, LPIPS) metrics under various configurations*

## 定位与知识库关联

### 任务定位与基线谱系

HUG3D 面向的是一个尚未被充分定义的任务：**从单张透视图像中重建包含物理交互的多人三维模型**。目前尚无完全对标的公开基线，因此论文的对比实验覆盖了三条相邻技术路线，以展示方法的跨范式优势。

**单人类重建方法的独立应用。** 将当前最先进的单人类重建方法直接应用于多人场景是最自然的基线。论文选取了 **ECON**、**SIFU**、**SiTH** 和 **PSHuman** 四个代表性方法。为公平比较，这些方法使用数据集提供的真实实例掩膜进行裁剪，独立重建每个人体后再在同一坐标框架中对齐组合。其中 PSHuman 还额外测试了直接输入多人图像而不裁剪的变体（记为 PSHuman-multi）。这些方法的共同瓶颈在于：缺乏群体层面的交互先验，导致遮挡区域几何失真、纹理缺失，且无法处理人体间的穿透问题。

**多目多人重建方法。** **DeepMultiCap** 作为多视角多人重建的代表，提供了交互建模的上限参考。其依赖多视角输入，在单目设定下不具备直接可比性，但其在接触精度（CP）指标上的表现（0.083）远低于 HUG3D（0.240），说明多视角几何本身并不自动保证交互合理性。

**视频多人重建方法。** **Multiply** 利用视频中的时序信息进行多人重建，代表了另一条技术路线。其与 HUG3D 的对比表明，即使不借助时序信息，显式的交互建模也能在单帧设定下取得有竞争力的重建质量。

### 核心技术贡献的知识增量

HUG3D 的贡献可从三个维度定位其对现有知识库的增量：

**规范正交表示（Pers2Ortho）消除尺度歧义。** 现有单人类方法在透视空间中进行重建，多人场景下的深度歧义和透视畸变被放大。Pers2Ortho 将输入变换到规范正交空间，使得多视图扩散在一致的尺度下进行推理。这一设计并非简单的坐标变换，而是通过初始几何估计和点云重投影（PCD reprojection）保留了可见区域的密集外观细节，为后续的遮挡补全提供了高质量的条件信号。消融实验证实，相比直接使用透视图像或 Era3D 的投影方式，Pers2Ortho 显著提高了投影清晰度并保留细节（Fig. 6(a)）。

**群体-实例联合扩散先验（HUG-MVD）。** 现有扩散模型在三维生成中的应用多集中于单物体或单人体，HUG-MVD 首次将多视图扩散扩展到群体-实例联合建模。其关键设计在于：在6个规范视图上同时去噪 RGB 和法向图，条件信号包含掩膜 RGB 和 SMPL-X 法向图；训练数据混合了单人类数据集（提供完整监督）和多人数据集（提供部分几何和真实交互）。消融实验表明，同时使用群体数据和个体数据训练优于单独使用任何一方（Table 4），且实例到群体的潜在合成（instance-to-group latent composition）对于保持接触区域的表面连续性至关重要。

**物理约束驱动的几何优化（HUG-GR）。** 现有方法在网格优化阶段通常仅使用单一实例损失，缺乏对多人交互的显式约束。HUG-GR 引入了三个互补的物理约束：群体-实例法向监督（结合群体级和实例级法向一致性）、穿透惩罚损失（对接触部件对之间的距离小于阈值进行软惩罚）和可见性损失（强制网格可见性与真实掩膜一致）。消融实验证实，每个损失项均对最终几何质量有正面贡献（Fig. 6(b)），且移除物理约束后 CD 增加约 146%，NC 下降约 1.5%（Table S15）。

### 适用边界与局限性

论文明确指出了 HUG3D 的四个适用边界，这些边界同时揭示了当前技术路线的方法论局限：

1. **光照假设约束。** 方法基于环境光照假设，训练数据光照条件一致。在低光或强对比光照条件下，多视图扩散生成的纹理可能出现瑕疵。这一局限根源于扩散模型的训练数据分布，而非方法设计本身。

2. **缺乏物体感知。** 方法未显式建模物体遮挡。当人体手持或与之交互的物体被误识别为身体一部分时，会导致几何畸变。这指向了一个开放问题：如何引入物体感知推理以处理人体-物体交互导致的遮挡？

3. **SMPL-X 初始化依赖。** 方法依赖 SMPL-X 姿态初始化，严重错误的姿态估计可能导致重建几何与输入图像出现偏差。这引出了另一个开放问题：能否减少对参数化模型初始化的依赖，实现更端到端的重建？

4. **评估基准的局限性。** 目前尚无完全对标的公开基线，比较基于自行适配的单人类或多目方法，无法进行完全一致的任务对齐。这意味着 HUG3D 的性能优势需要在未来更标准化的基准上进一步验证。

### 统计显著性验证

论文通过 Wilcoxon signed-rank 检验验证了所有指标上的优势均具有统计显著性（p < 0.001，Table S14），这为方法优势提供了严格的统计支撑，而非仅仅依赖数值差异。

### 未来方向

从论文的局限性出发，可识别三个有前景的后续研究方向：(1) 引入物体感知推理以处理人体-物体交互遮挡；(2) 提高方法在复杂或极端光照条件下的鲁棒性，可能通过物理渲染增强或光照不变表示；(3) 减少对 SMPL-X 初始化的依赖，探索更端到端的联合估计与重建框架。

## 原文 PDF

![[paperPDFs/CVPR_2026/Human_Interaction_Aware_3D_Reconstruction_from_a_Single_Image.pdf]]
