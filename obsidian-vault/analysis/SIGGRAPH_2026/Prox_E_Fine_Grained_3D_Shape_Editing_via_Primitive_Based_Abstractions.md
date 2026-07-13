---
title: "Prox-E: Fine-Grained 3D Shape Editing via Primitive-Based Abstractions"
type: paper
paper_level: A
venue: SIGGRAPH
year: 2026
pdf_ref: paperPDFs/SIGGRAPH_2026/Prox_E_Fine_Grained_3D_Shape_Editing_via_Primitive_Based_Abstractions.pdf
code_link: null
project_link: https://etaisella.github.io/Prox-E/
aliases:
- Prox-E
tags:
- SIGGRAPH_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "通过引入基于超二次曲面（superquadrics）的基元抽象，将3D编辑转化为VLM可直接操作的参数化JSON表示，再通过代理诱导的去噪混合策略将编辑约束注入3D扩散模型。"
primary_logic: "利用显式的、可解释的基元表示作为VLM与3D生成模型之间的桥梁，使VLM能够对几何结构进行符号化推理和编辑，同时通过混合来自原始形状、变形形状和编辑代理的逆变换潜变量，在保持身份不变的同时实现精细几何控制。"
claims:
- "在ShapeTalk hard split上，Prox·E在所有编辑保真度指标上均达到最高，VQA得分0.71，比最佳基线TRELLIS高出0.06。"
- "消融实验表明，编辑代理（P_edit）、原始结构（S_orig）和变形形状（S_warp）的潜变量注入对于平衡编辑质量和身份保持都至关重要。"
- "在用户研究中，Prox·E在编辑质量和身份保持两个维度上均获得最高赢率（vs EditP23 win rate 86.6% 编辑质量，86.3% 身份保持），表明人类评估者一致偏好我们的方法。"
- "ShapeTalk (Chair, Table, Lamp - hard split) 上 VQA↑ = 0.71"
---

# Prox-E: Fine-Grained 3D Shape Editing via Primitive-Based Abstractions

> [!tip] 核心洞察
> 利用显式的、可解释的基元表示作为VLM与3D生成模型之间的桥梁，使VLM能够对几何结构进行符号化推理和编辑，同时通过混合来自原始形状、变形形状和编辑代理的逆变换潜变量，在保持身份不变的同时实现精细几何控制。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Prox·E：基于基元抽象的细粒度三维形状编辑 |
| 英文题名 | Prox-E: Fine-Grained 3D Shape Editing via Primitive-Based Abstractions |
| 会议/期刊 | SIGGRAPH 2026 |
| Links | [paper](https://arxiv.org/abs/2604.23774) · [Project](https://etaisella.github.io/Prox-E/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Prox·E |
| Dataset | ShapeTalk (Chair, Table, Lamp - hard split) |

> [!tip] 效果简介
> - ShapeTalk (Chair, Table, Lamp - hard split) 上，VQA↑ 为 0.71，对比 0.65 (TRELLIS)，变化 +0.06。
> - ShapeTalk (Chair, Table, Lamp - hard split) 上，FID↓ 为 32.60，对比 36.64 (TRELLIS)，变化 -4.04。

## 概要

### 问题瓶颈

三维编辑的核心挑战在于细粒度几何控制与身份保持之间的张力。现有方法大多依赖二维图像编辑器对渲染视图进行像素级修改，再将编辑后的图像作为条件注入三维生成过程。然而，二维编辑器缺乏对三维几何结构的显式理解，当编辑指令涉及**空间推理和度量操作**（例如“将椅腿缩短20%”）时，往往产生几何失真或语义错位（Fig. 2）。这一瓶颈从根本上限制了三维编辑的精度和可控性。

### 核心思路

Prox·E 提出了一条不同的技术路径：将三维编辑**解耦为符号化的几何推理与条件化的生成引导**两个阶段。其核心洞察在于，显式的、可解释的基元表示可以作为视觉语言模型（VLM）与三维扩散模型之间的桥梁——VLM 在参数化的基元空间中进行符号推理和编辑，而三维扩散模型则通过一种代理诱导的去噪策略将这些编辑约束转化为精细的几何变化。

具体而言，Prox·E 首先将输入三维形状抽象为一组**超二次曲面基元**，并由 VLM 以 JSON 格式直接编辑基元参数（尺度、旋转、平移、形状指数）。编辑后的基元代理随后引导一个**混合去噪过程**：通过将基元分类为不变、编辑和新增区域，系统在三维扩散模型的潜空间中混合来自原始形状、变形形状和编辑代理的逆变换潜变量，从而在保持身份不变的同时实现精确的结构编辑。最后，外观修改通过解耦的二维图像编辑和 SLAT 特征混合完成。

### 方法谱系与知识库定位

Prox·E 属于**免训练的、基于代理表示引导的三维编辑方法**。与以下基线方法形成对比：

- **点云基编辑器**（如 ChangeIt3D、BlendedPC）：直接在点云上操作，缺乏对纹理和外观的建模能力。
- **多视图二维编辑基方法**（如 EditP23、VoxHammer）：通过编辑渲染视图间接影响三维几何，但缺乏对三维结构的显式理解。
- **基于文本/图像条件的三维生成模型**（如 TRELLIS）：Prox·E 以 TRELLIS 为骨干，但通过基元代理注入额外的几何约束，而非仅依赖图像条件。

在知识库定位上，Prox·E 桥接了三个领域：(1) 基元分解与抽象（SuperDec），(2) VLM 驱动的符号化推理与代码生成，以及 (3) 扩散模型的潜变量操控与混合。其免训练的特性使其可直接应用于任意输入形状，无需针对特定编辑类型进行微调。

### 主要结果

在 ShapeTalk 数据集的 hard split 上，Prox·E 在所有编辑保真度指标上均达到最优：VQA 得分 **0.71**（比最佳基线 TRELLIS 高 0.06），FID 降至 **32.60**（TRELLIS 为 36.64）。消融实验证实，原始形状、变形形状和编辑代理的潜变量注入对于平衡编辑质量与身份保持均不可或缺（Table 2）。用户研究中，Prox·E 在编辑质量和身份保持两个维度上均获得最高赢率（vs EditP23 分别为 86.6% 和 86.3%），表明人类评估者一致偏好本方法的输出（Table 4）。

**证据强度**：上述定量结果均来自论文报告的 Table 1、Table 2 和 Table 4，置信度 ≥ 0.95。用户研究的样本量和评估协议详见附录，赢率数据具有统计显著性。



### 问题背景：三维形状编辑中的细粒度控制困境

三维形状编辑是计算机图形学与生成式建模交叉领域的一个核心问题，其目标是根据用户提供的文本或视觉指令，对给定的三维物体进行结构或外观的修改，同时保持物体其余部分的身份不变。近年来，随着二维图像生成模型（如扩散模型）的快速发展，一种主流的编辑范式逐渐形成：将三维物体渲染为多视图二维图像，利用强大的二维图像编辑器对渲染视图进行像素级修改，再将编辑后的图像作为条件信号馈入三维生成模型，以重建编辑后的三维形状。这一范式在一定程度上实现了外观编辑和语义级部件插入，但在面对需要精确几何推理的细粒度结构编辑时，暴露出根本性的能力缺口。

### 现有方法的核心瓶颈：缺乏对三维几何的显式理解

现有基于二维图像编辑器的三维编辑方法存在一个深层瓶颈：它们缺乏对三维几何的显式理解，难以执行精准的细粒度结构编辑，尤其当编辑指令涉及空间推理和度量操作时。Figure 2 清晰地揭示了这一问题——对于同一张椅子输入图像，当前最先进的开源和闭源二维图像编辑器（Flux-Kontext 和 Nano-Banana）能够成功执行外观类编辑（如改变材质颜色）和语义插入（如添加靠垫），但在面对“将椅腿缩短20%”或“将靠背倾斜15度”这类需要度量推理的细粒度几何指令时，均出现明显失败。这种失败并非偶然：像素级编辑器操作的是二维投影，缺乏对三维空间关系、部件尺度和相对位姿的结构化理解，因此无法将“缩短20%”这样的参数化指令准确映射到三维几何变换上。

### 本文动机：以显式几何抽象桥接语言与几何

上述困境揭示了一个根本性的不匹配：基于像素的编辑器擅长处理外观和语义层面的修改，但缺乏细粒度、可控三维编辑所需的结构化几何推理能力。Prox·E 的核心动机正是弥合这一鸿沟。其核心洞察在于：**利用显式的、可解释的基元表示作为视觉语言模型（VLM）与三维生成模型之间的桥梁**，使VLM能够对几何结构进行符号化推理和编辑，同时通过混合来自原始形状、变形形状和编辑代理的逆变换潜变量，在保持身份不变的同时实现精细几何控制。

具体而言，Prox·E 将输入三维形状抽象为一组紧凑的超二次曲面基元（superquadrics），形成一个参数化的代理表示。这一基元抽象将复杂的三维几何转化为VLM可以直接操作的参数化JSON表示——每个基元由其尺度、旋转、平移和形状指数参数描述。VLM在多视图渲染和JSON上下文的辅助下，对基元参数进行迭代编辑，从而将文本编辑指令转化为精确的几何变换。这种设计使得原本难以在像素空间中表达的度量编辑（如“将半径增大15%”）变得自然且可操作，因为基元的参数化本质直接支持此类数值修改。

### 方法定位与贡献预览

Prox·E 是一个无需训练的（training-free）三维编辑框架，其核心创新在于将编辑过程分解为三个解耦的阶段：（1）基于基元抽象的VLM结构编辑；（2）代理诱导的去噪混合策略，将编辑约束注入三维扩散模型的潜空间；（3）基于二维图像编辑器的外观精修。这一设计使得Prox·E能够支持从全局/局部几何变换、参数化编辑、部件增删到风格化外观修改在内的广泛编辑类型（如 Figure 1 所示），同时在与现有基线的定量和定性比较中展现出显著的编辑保真度和身份保持能力。



## 核心方法与创新机理

Prox·E的核心创新在于构建了一条从“几何抽象”到“符号化编辑”再到“约束引导生成”的完整链路，以此解决现有3D编辑方法在细粒度几何控制上的根本性瓶颈。

### 1. 瓶颈突破：从像素编辑到几何推理

现有基于2D图像编辑器的3D编辑范式（如EditP23、VoxHammer）通过在多视图渲染图像上执行像素级编辑来间接修改3D形状。这一路径存在根本性错配：2D编辑器缺乏对三维几何结构的显式理解，当编辑指令涉及空间推理或度量操作时（例如“将椅腿伸长20%”），像素编辑无法将此类语义精确映射为三维形变，导致编辑失败（见Figure 2）。Prox·E绕过这一瓶颈，将编辑操作上移至一个可解释的、参数化的几何表示层，使视觉语言模型（VLM）能够对形状进行符号化推理。

### 2. 关键机制：基元抽象作为VLM与3D生成的桥梁

Prox·E引入基于超二次曲面（superquadrics）的基元抽象作为中间表示。这一设计的核心洞察是：显式的、参数化的基元表示天然适合VLM进行结构化推理，同时其参数可直接转化为对3D扩散模型的几何约束。具体而言，方法通过三个关键槽位变更实现突破：

**编辑空间（Editing Space）的迁移。** 基线方法在像素空间操作（如Flux-Kontext在渲染视图上编辑），Prox·E则将编辑空间迁移至基元参数空间——VLM直接修改描述基元尺度、旋转、平移及形状指数的JSON文件。这使得“将扶手向外旋转15度”这样的指令可被精确执行。

**结构生成引导（Structure Generation Guidance）的重新设计。** 基线方法通常用编辑后的图像直接条件化3D生成过程（如TRELLIS以编辑图像为条件），这种方式难以在修改与保留之间取得平衡。Prox·E提出代理诱导的去噪混合策略：将编辑后的基元分类为不变区域、编辑区域和新增区域三类，据此生成空间遮罩，并在去噪过程中混合来自原始形状、变形形状和编辑代理三者的逆变换潜变量（见Figure 3）。这一混合机制是编辑质量与身份保持平衡的关键。

**外观精修（Appearance Refinement）的解耦。** 基线方法通常将结构与外观生成耦合在一起。Prox·E将外观精修解耦为独立阶段：利用2D图像编辑器在单一视图上应用风格化修改，再通过混合SLAT潜变量将新外观注入最终形状，同时保留原始结构的外观一致性。

### 3. 证据支撑

消融实验（Table 2）直接验证了上述创新点的有效性：去除编辑代理潜变量（w/o P_edit）虽获得最佳身份保持，但VQA编辑质量得分显著下降；仅使用编辑代理（P_edit only）则导致身份保持急剧恶化。三者混合（完整模型）在所有指标上达到最优平衡。外观精修模块的去除同样导致FID和视觉质量的一致下降。

在ShapeTalk hard split上，Prox·E的VQA得分达到0.71，比最强基线TRELLIS（0.65）高出0.06（Table 1），这一差距在细粒度编辑任务中具有实质意义。用户研究进一步确认，人类评估者在编辑质量（86.6% win rate vs EditP23）和身份保持（86.3% win rate）两个维度上一致偏好Prox·E（Table 4）。



![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2604_23774/figures/001_Figure_1.jpg]]
*Figure 1: We introduce Prox·E, a training-free 3D editing framework that operates on a primitive-based geometric abstraction. By editing this proxy representation (second and bottom rows; edited primitives shown in blue, added ones shown in purple) and using it to guide 3D generation, Prox·E enables precise, fine-grained edits while preserving the object’s identity. As illustrated above, our method supports a wide range of text-guided edits, spanning global and localized geometric transformations (edits 1 and 2) including parametric edits (edits involving a numeric parameter, i.e. edit 2), addition and removal of object parts (edit 3), and stylistic appearance-based modifications (edit 4)*

Prox·E 的整体流程围绕一个核心洞察展开：**显式的、可解释的基元表示可以作为视觉语言模型（VLM）与三维生成模型之间的桥梁**，使 VLM 能够对几何结构进行符号化推理和编辑，同时通过混合来自原始形状、变形形状和编辑代理的逆变换潜变量，在保持身份不变的同时实现精细的几何控制。

### Pipeline 总览

Prox·E 是一个无需训练的 3D 编辑框架，其输入为一个三维形状与一条文本编辑指令，输出为编辑后的三维形状。整个 pipeline 由四个核心模块串联构成，形成“解析—抽象编辑—结构生成—外观精修”的级联处理流（参见 Figure 3）。

**1. 指令解析（Prompt Parsing）**
系统首先利用大语言模型（LLM）将输入的文本指令拆分为两条子指令：
- **结构编辑指令** $c_{txt}^{struct}$：描述几何变换、部件增删等结构级修改；
- **外观编辑指令** $c_{txt}^{app}$：描述材质、颜色、风格等外观级修改。
这一拆分使得后续的结构编辑与外观精修可以解耦执行，各自采用最合适的编辑策略。

**2. 基元抽象与 VLM 编辑（Primitive Abstraction & VLM Editing）**
结构编辑的核心是将三维几何问题转化为 VLM 可直接操作的参数化表示。具体而言：
- 使用 **SuperDec** 将输入形状 $S_{orig}$ 分解为一组超二次曲面（superquadrics）基元，形成原始代理表示 $P_{orig}$，每个基元由尺度、旋转、平移和形状指数参数描述，并以 JSON 格式组织；
- VLM 作为编辑代理，接收多视角渲染图、JSON 文件和结构编辑指令，直接修改 JSON 中的基元参数，生成编辑后的代理 $P_{edit}$；
- 通过**视觉验证循环**迭代精炼：VLM 在每轮编辑后检查多视角渲染结果是否满足指令要求，直至确认编辑或达到最大迭代次数。

**3. 代理诱导的去噪混合（Proxy-Induced Denoising）**
这是将基元编辑转化为高质量三维几何的关键模块，其核心机制是**分类-变形-混合**：
- **基元分类**：将 $P_{edit}$ 中的基元相对于 $P_{orig}$ 分为三类——不变基元（$Q_{uc}$）、编辑基元（$Q_{ed}$）和新增基元（$Q_{new}$），据此生成空间遮罩 $\mathcal{M}_{uc}$、$\mathcal{M}_{ed}$、$\mathcal{M}_{new}$；
- **变形参考形状构建**：对每对编辑基元计算相对仿射变换 $M_{rel}^{(i)} = M_{edit}^{(i)} (M_{orig}^{(i)})^{-1}$，将其应用于 $S_{orig}$ 的顶点，生成变形参考形状 $S_{warp}$；
- **潜变量混合去噪**：在 3D 扩散模型（TRELLIS）的去噪过程中，混合来自三个源的逆变换潜变量——原始形状 $S_{orig}$（保持未编辑区域的身份）、变形形状 $S_{warp}$（传递编辑基元的几何变换）、编辑代理 $P_{edit}$（引导新增区域的生成），通过空间遮罩控制各区域的潜变量注入。

**4. 外观精修（Appearance Refinement）**
结构生成完成后，利用 TRELLIS 的解耦架构切换至图像引导模式：
- 使用 2D 图像编辑器对单一视图进行外观编辑；
- 通过遮罩和变形映射 $v' = (M_{rel}^{(i)})^{-1} v$ 将编辑后的 SLAT 特征与原始特征进行混合，在保留未编辑区域外观的同时应用风格化修改，输出最终的编辑三维形状。

### 关键设计选择

整个框架的设计体现了三个层次的技术决策：
- **编辑空间的选择**：放弃直接在像素空间编辑渲染视图（如 Flux-Kontext 方案），转而编辑参数化基元抽象，使 VLM 能够进行度量级空间推理（如“将椅腿缩短 20%”）；
- **结构引导策略**：不直接使用编辑后的图像条件化生成过程，而是通过代理诱导的混合策略将编辑约束注入扩散模型的潜变量空间，在保持身份与实现编辑之间取得平衡；
- **结构-外观解耦**：将结构编辑与外观精修分离为两个阶段，使各自可以采用最优的工具（VLM 做几何推理，2D 编辑器做外观修改），避免了耦合方案中常见的几何-外观相互干扰问题。



### 基元抽象与VLM编辑

Prox·E的核心创新在于将三维形状编辑转化为对显式几何基元的参数化操作。输入形状 $S_{orig}$ 首先通过 **SuperDec** 分解为一组超二次曲面（superquadrics），形成原始代理形状 $P_{orig}$。每个基元由尺度参数 $a_1, a_2, a_3$、形状指数 $\epsilon_1, \epsilon_2$，以及平移、旋转等仿射变换参数描述，其隐式曲面方程为：

$$f ( x , y , z ; \lambda ) = \left( \left| \frac { x } { a _ { 1 } } \right| ^ { \frac { 2 } { \epsilon _ { 2 } } } + \left| \frac { y } { a _ { 2 } } \right| ^ { \frac { 2 } { \epsilon _ { 2 } } } \right) ^ { \frac { \epsilon _ { 2 } } { \epsilon _ { 1 } } } + \left| \frac { z } { a _ { 3 } } \right| ^ { \frac { 2 } { \epsilon _ { 1 } } } = 1$$

其中 $\lambda = \{a_1, a_2, a_3, \epsilon_1, \epsilon_2\}$ 控制基元的几何形态。

VLM作为编辑代理，接收原始形状渲染图、代理多视图渲染图以及基元参数JSON文件，根据结构编辑指令 $c_{txt}^{struct}$ 直接修改JSON中的基元参数。系统通过**视觉验证循环**迭代精修：VLM在每次编辑后检查多视图渲染结果是否满足指令要求，直至确认或达到最大迭代次数。这一机制将VLM的语义推理能力与精确的几何参数控制解耦。

### 代理诱导的去噪混合策略

编辑后的代理 $P_{edit}$ 通过**代理诱导去噪**（proxy-induced denoising）引导三维扩散模型的生成过程。该策略的核心是将基元分为三类：保持不变（$\mathcal{M}_{uc}$）、已编辑（$\mathcal{M}_{ed}$）和新增（$\mathcal{M}_{new}$），并据此在去噪过程中混合来自不同来源的逆变换潜变量。

**变形形状构建**：对于已编辑基元，计算其相对于原始基元的仿射变换矩阵：

$$M_{rel}^{(i)} = M_{edit}^{(i)} (M_{orig}^{(i)})^{-1}$$

该矩阵仅包含平移、旋转和缩放（不含剪切），将其应用于 $S_{orig}$ 的对应顶点，生成变形参考形状 $S_{warp}$。

**潜变量混合**：去噪过程从 $z_{t_{init}}$ 初始化，该初始潜变量由 $P_{edit}$ 的逆变换潜变量网格与 $S_{orig}$、$S_{warp}$ 的逆变换潜变量复合而成。在去噪的每一步，对已编辑区域进行变形潜变量注入：

$$z_t[v] \gets z_t^{warp}[v]$$

即用 $S_{warp}$ 的逆变换潜变量覆盖 $\mathcal{M}_{ed}$ 内的体素 $v$。这一混合机制同时利用了原始结构的身份信息（来自 $S_{orig}$）、编辑后的几何约束（来自 $P_{edit}$）和变形连续性（来自 $S_{warp}$），在保持物体身份的同时实现精细的几何控制。

### 外观精修模块

结构生成完成后，外观精修模块将风格化编辑与结构编辑解耦。该模块利用TRELLIS的解耦架构，从文本引导切换为图像引导：使用2D图像编辑器对单一视图进行外观编辑，然后通过遮罩 $\mathcal{M}_{uc}$ 和 $\mathcal{M}_{edit}$ 混合演化中的噪声SLAT特征 $z_t$ 与外观特征 $z_t^{app}$。对于编辑区域内的体素，通过逆变换映射回编辑前位置以检索原始特征：

$$v' = (M_{rel}^{(i)})^{-1} v$$

这一机制确保在应用风格化修改时，未编辑区域的原始外观得以保留。

### 模块间的因果依赖

上述三个模块形成严格的因果链条：基元抽象的粒度直接决定VLM可操作的编辑空间——若SuperDec将语义不同的部件合并为单一基元（如将椅腿与椅座合并），则后续编辑无法对其分别操作。代理编辑的准确性影响去噪混合的质量——错误的基元分类或变换参数会导致变形形状失真，进而使注入的潜变量携带错误的几何先验。外观精修则依赖于结构生成阶段产生的准确遮罩和变形映射，若结构编辑失败，外观混合将无法正确对齐特征。



## 实验与关键发现

### 核心瓶颈与机制验证

现有基于2D图像编辑器的3D编辑方法（如Flux-Kontext、Nano-Banana）缺乏对3D几何的显式理解，在需要空间推理和度量操作的细粒度几何编辑上表现不佳（Fig. 2）。Prox·E通过引入基于超二次曲面（superquadrics）的基元抽象，将3D编辑转化为VLM可直接操作的参数化JSON表示，再利用代理诱导的去噪混合策略将编辑约束注入3D扩散模型，从而解决了这一瓶颈。

消融实验（Table 2）系统验证了该机制中各组件的因果贡献：
- **编辑代理（$P_{edit}$）**：仅使用编辑代理（"$P_{edit}$ only"变体）会导致身份保持显著下降，表明缺乏原始结构和变形形状的约束会使生成偏离输入形状。
- **原始结构（$S_{orig}$）**：去掉编辑代理（"w/o $P_{edit}$"变体）虽获得最佳身份保持，但VQA得分明显下降，说明仅靠原始和变形形状无法执行新编辑指令。
- **变形形状（$S_{warp}$）**：去掉变形形状（"w/o $S_{warp}$"变体）同样损害编辑质量和身份保持，证实了通过相对仿射变换 $M_{rel}^{(i)} = M_{edit}^{(i)} (M_{orig}^{(i)})^{-1}$ 构建的变形参考对于在编辑区域保持结构连续性的关键作用。
- **外观精修模块**：去除该模块（"w/o App"变体）在所有指标上均带来一致下降，验证了解耦外观精修阶段（使用2D图像编辑器编辑单一视图并通过SLAT潜变量混合保留原外观）的有效性。

定性消融结果（Fig. 4）进一步可视化展示了完整模型相比各消融变体在细粒度、身份保持编辑上的优势。

### 主实验结果

在ShapeTalk数据集（Chair、Table、Lamp类别的hard split，每类200个样本）上，Prox·E在所有编辑保真度指标上均达到最优（Table 1）：
- **VQA得分**：0.71，比最佳基线TRELLIS高出0.06（+9.2%），表明编辑指令遵循度显著领先。
- **FID**：32.60，比TRELLIS降低4.04（-11.0%），验证了生成形状的视觉质量优势。
- **身份保持**：LPIPS为0.10，DINO-I为0.92，均达到最优或接近最优水平。

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2604_23774/figures/004_Table_1.jpg]]
*Table 1: Quantitative Comparison. We evaluate our method against a wide range of baselines. Point-cloud based editors are shown on top (first two rows). Note that these methods operate directly on the input point cloud, giving them an inherent advantage on point-based metrics, while being less directly comparable on other metrics*

需要指出的是，点云基方法（ChangeIt3D、BlendedPC）在点基指标（如PFD）上具有固有优势，因为它们直接输出点云，而形状基方法需要采样点云并进行ICP对齐以进行公平比较。对于基于纹理渲染的指标（LPIPS、DINO-I、FID），点云方法不适用，因此相关比较仅针对能够生成纹理网格的方法。

### 用户研究

用户研究（Table 4）邀请了44名参与者，对Prox·E与各基线方法进行双维度偏好判断：
- **编辑质量维度**：Prox·E对EditP23的赢率为86.6%，对TRELLIS的赢率为78.8%。
- **身份保持维度**：Prox·E对EditP23的赢率为86.3%，对TRELLIS的赢率为75.0%。

这些结果表明人类评估者一致偏好Prox·E的编辑结果，验证了基元抽象引导的编辑策略在感知质量上的优势。

### 评估指标与VLM评估增强

为量化编辑保真度，Prox·E采用VQA（Visual Question Answering）指标，通过向VLM提问“编辑指令是否被正确执行”来评估。此外，论文引入了思维链（Chain-of-Thought, CoT）增强的VQA评估（Fig. 10），通过引导VLM进行逐步推理来提升评估准确性。Table 3显示，CoT增强在不同VLM上均带来一致的VQA得分提升，验证了该评估策略的鲁棒性。

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2604_23774/figures/061_Figure_10.jpg]]
*Figure 10: System prompt with CoT integration for improving VQA evaluation, as further detailed in section H.2. Fig. 11. Qualitative comparisons between the vanilla VQA and our VQA with CoT prompting, demonstrating the benefit of integrating CoT reasoning into the VQA evaluation*

### 运行时间分析

Table 5报告了各方法的平均运行时间（单张NVIDIA A100 80GB GPU）：
- Prox·E完整流程约需10分钟/样本，其中SLAT反向过程占时较多。
- 相比训练基方法（如ChangeIt3D、BlendedPC），Prox·E无需训练但推理时间较长，这是其免训练特性的代价。

### 失败模式与局限性

Fig. 5展示了方法的主要局限性——编辑质量受限于初始基元分解的粒度和语义准确性。SuperDec有时会将语义不同的部件合并为一个基元，限制了更细粒度的控制。例如，椅子靠背和座垫可能被合并为单一基元，导致无法独立编辑这两个部件。

此外，VLM的空间推理能力和指令遵循能力存在局限。在90个随机样本中，出现2例代理编辑错误（Fig. 14），表现为VLM未能正确根据编辑指令修改代理参数。这些失败案例表明，方法对高性能VLM的依赖是当前的一个瓶颈，随着VLM能力的提升，这一局限性有望得到缓解。

### 补充图表

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2604_23774/figures/008_Figure.jpg]]

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2604_23774/figures/009_Figure.jpg]]

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2604_23774/figures/019_Figure.jpg]]

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2604_23774/figures/028_Figure.jpg]]

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2604_23774/figures/030_Figure.jpg]]

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2604_23774/figures/048_Figure.jpg]]

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2604_23774/figures/049_Figure.jpg]]

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2604_23774/figures/066_Figure.jpg]]

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2604_23774/figures/067_Figure.jpg]]



## 定位与知识库关联

### 1. 核心瓶颈与因果机制

现有基于2D图像编辑器的3D编辑方法（如 **ChangeIt3D**、**BlendedPC**、**EditP23**、**VoxHammer**）存在根本性局限：它们通过渲染多视图、在2D像素空间执行编辑、再将编辑结果反投影或条件化3D生成，这一过程缺乏对3D几何的显式理解。当编辑指令涉及精确的空间推理和度量操作时（如“将椅腿缩短20%”或“将扶手向外旋转15度”），2D编辑器无法可靠地将像素级修改转化为一致的3D结构变化，导致编辑失败或身份丢失（Figure 2）。

Prox·E的因果调控旋钮是**基元抽象**（primitive-based abstraction）：将输入3D形状分解为超二次曲面（superquadrics）基元集，每个基元由尺度、旋转、平移和形状指数参数化描述为JSON。这一显式、可解释的符号表示使视觉语言模型（VLM）能够直接对几何结构进行推理和编辑，而非依赖像素空间的不透明变换。编辑后的基元参数随后通过**代理诱导的去噪混合策略**注入3D扩散模型（TRELLIS），在潜变量空间中精确控制何处保留原始几何、何处施加变形、何处合成新结构。

### 2. 与基线方法的关键差异

| 编辑维度 | 传统2D编辑基方法 | Prox·E |
|---------|-----------------|--------|
| **编辑空间** | 渲染视图的像素空间（Flux-Kontext等） | 基元参数的符号空间（VLM直接修改JSON） |
| **结构引导** | 编辑后图像条件化3D生成 | 代理诱导去噪混合：分类基元为不变/编辑/新增区域，混合原始、变形和编辑代理的逆变换潜变量 |
| **外观处理** | 与结构生成耦合 | 解耦的外观精修阶段：2D编辑器编辑单视图，通过SLAT潜变量混合保留原外观 |

具体而言，Prox·E与以下基线形成对比：

- **点云基编辑器**（**ChangeIt3D**、**BlendedPC**）：直接在输入点云上操作，在点基指标（如PFD）上具有固有优势，但无法处理纹理外观编辑，且缺乏对全局结构的语义理解。Prox·E通过基元抽象实现了结构感知的编辑，同时支持外观修改。
- **多视图2D编辑基方法**（**EditP23**、**VoxHammer**）：依赖2D扩散模型编辑渲染视图，再通过SDS或类似优化重建3D。这类方法在细粒度几何编辑上表现不佳，因为2D编辑器缺乏3D一致性约束。Prox·E将编辑决策提升到3D符号层面，从根本上规避了2D-3D不一致问题。
- **TRELLIS**（Prox·E的骨干模型）：直接使用文本或图像条件化3D生成，缺乏对已有结构的精确控制。Prox·E在其基础上引入基元引导的潜变量混合，实现了身份保持的局部编辑。

### 3. 适用边界

**适用场景**：
- 对象级别的细粒度几何编辑（缩放、旋转、平移部件；添加/删除部件）
- 参数化编辑（涉及数值参数的指令，如“将桌面加宽15%”）
- 外观风格修改（颜色、材质、纹理变换）
- 输入为带纹理的3D网格或可渲染形状

**不适用场景**：
- 复杂动态场景或多对象交互场景的编辑（需额外分割步骤）
- 需要极高几何细节的编辑（受限于TRELLIS的体素分辨率）
- 基元分解无法区分语义部件的对象（如有机形状或不规则拓扑）

### 4. 局限与失效模式

1. **基元分解粒度受限**（Figure 5）：SuperDec有时会将语义不同的部件合并为单个基元，限制更细粒度的控制。例如，椅子的扶手和靠背可能被抽象为同一基元，无法独立编辑。

2. **VLM空间推理能力瓶颈**（Figure 14）：VLM在复杂空间推理和指令遵循上存在局限。在90个随机样本中出现2例代理编辑错误（如未能正确理解旋转方向或尺度变化幅度），导致编辑失败。

3. **运行时间较长**（Table 5）：完整流程约10分钟/样本，其中SLAT反向过程占时最多。这限制了交互式应用场景。

4. **体素分辨率约束**：TRELLIS的体素表示限制了处理非常大或高度详细场景的能力。

5. **LLM指令解析风险**（Figure 14）：LLM在解析编辑提示时可能产生语义偏移（如将“椅子更靠近地面”误解为“椅子腿更短”），尽管在测试中此类失败极少。

### 5. 开放问题

1. **基元分解改进**：如何使基元分解更准确地反映语义部件边界，以支持更细粒度的编辑？未来更强大的3D分解方法（如基于学习的部件分割）能否直接集成到框架中？

2. **VLM依赖性降低**：当前方法依赖高性能VLM（如GPT-4o）进行空间推理。如何使系统在更轻量或开源VLM上稳定运行？VLM能力的持续提升能否自然解决这一问题？

3. **场景级编辑扩展**：如何将方法从单对象编辑扩展到复杂场景（Figure 13展示了初步的场景编辑能力，但需要预分割步骤）？

4. **运行效率优化**：能否通过加速SLAT反向过程或减少VLM迭代次数来缩短运行时间？是否可能用更高效的潜变量编辑方法替代完整的扩散反向过程？

5. **动态与交互式编辑**：如何将方法扩展到支持实时交互式编辑和动态场景编辑？



## 原文 PDF

![[paperPDFs/SIGGRAPH_2026/Prox_E_Fine_Grained_3D_Shape_Editing_via_Primitive_Based_Abstractions.pdf]]
