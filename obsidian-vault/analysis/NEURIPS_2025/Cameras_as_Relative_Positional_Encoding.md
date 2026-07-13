---
title: "Cameras as Relative Positional Encoding"
type: paper
paper_level: A
venue: NeurIPS
year: 2025
pdf_ref: paperPDFs/NEURIPS_2025/Cameras_as_Relative_Positional_Encoding.pdf
project_link: https://www.liruilong.cn/prope/
code_link: null
aliases:
- PPPE
- CARPE
tags:
- NEURIPS_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "将相机几何编码从绝对raymap改为基于注意力的相对投影编码PRoPE，通过注入相机全视锥体（内参和外参）作为相对位置编码，提升模型对相机参数变化的鲁棒性及多任务泛化能力。"
primary_logic: "利用相机之间的完整投影变换（包括内参和外参）作为注意力中的相对位置编码，能够捕捉视锥体间的几何关系，在保持全局坐标系不变性的同时，显著改善多视角Transformer在新视角合成、立体深度估计和空间认知任务上的性能与泛化能力。"
claims:
- "在恒定内参的新视角合成任务上，PRoPE大幅优于绝对raymap编码。"
- "当场景内相机内参变化时，PRoPE显著超越所有对比方法，包括仅考虑外参的相对编码。"
- "PRoPE与CamRay结合可获得最佳性能，且纯注意力的PRoPE已优于GTA+CamRay混合方案。"
- "PRoPE对测试时的长序列和未知焦距展现出强鲁棒性。"
---

# Cameras as Relative Positional Encoding

> [!tip] 核心洞察
> 利用相机之间的完整投影变换（包括内参和外参）作为注意力中的相对位置编码，能够捕捉视锥体间的几何关系，在保持全局坐标系不变性的同时，显著改善多视角Transformer在新视角合成、立体深度估计和空间认知任务上的性能与泛化能力。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 摄像机作为相对位置编码 |
| 英文题名 | Cameras as Relative Positional Encoding |
| 会议/期刊 | NeurIPS 2025 |
| Links | [paper](https://arxiv.org/abs/2507.10496) · [Project](https://www.liruilong.cn/prope/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | PRoPE (Projective Positional Encoding) |
| Dataset | RealEstate10K (novel view synthesis, constant intrinsics per scene), varying intrinsics per scene), Objaverse (novel view synthesis, varying intrinsics), RGBD (stereo depth estimation) |

> [!tip] 效果简介
> - RealEstate10K (novel view synthesis, constant intrinsics per scene) 上，PSNR↑ 为 22.80，对比 20.48 (Plücker Raymap)，变化 +2.32。
> - RealEstate10K (novel view synthesis, varying intrinsics per scene) 上，PSNR↑ 为 21.42，对比 19.89 (Plücker Raymap)，变化 +1.53。
> - Objaverse (novel view synthesis, varying intrinsics) 上，PSNR↑ 为 22.98，对比 21.43 (Plücker Raymap)，变化 +1.55。

## 概要

### 问题背景

多视角Transformer在三维视觉任务中需要将相机参数作为“位置信息”注入模型。现有方法主要分为两类：

- **绝对编码**：如Naive Raymap和Plücker Raymap，将每个像素的光线原点与方向作为token级特征拼接输入。这类方法绑定于全局坐标系，难以泛化到不同相机内参和场景。
- **相对位姿编码**：如CAPE和GTA，在注意力层注入相机间的SE(3)相对位姿变换。然而，这些方法忽略了相机内参（焦距、主点等），无法捕捉完整视锥体间的投影关系。

**核心瓶颈**：绝对raymap编码缺乏跨场景泛化能力；现有相对编码仅建模外参而遗漏内参，限制了多视角几何推理的上限。

### 核心方法

本文提出**PRoPE（Projective Positional Encoding）**，将相机之间的完整投影变换（同时包含内参与外参）作为注意力中的相对位置编码。具体而言：

- 利用相机全视锥体间的投影矩阵 $\tilde{P}_{i_1} \tilde{P}_{i_2}^{-1}$ 编码相对几何关系；
- 通过GTA风格的注意力机制，将该投影变换同时注入Q、K、V矩阵；
- 结合图像内patch坐标的RoPE编码，形成块对角形式的组合编码。

PRoPE不引入额外可学习参数，可与标准Transformer架构和融合注意力核无缝集成。

### 方法定位

PRoPE属于**注意力层级相对编码**方法，与既有工作的关系如下：

| 方法 | 编码层级 | 编码内容 |
|------|----------|----------|
| Plücker Raymap | Token级绝对编码 | 全局坐标系光线参数 |
| CAPE | 注意力级相对编码 | SE(3)外参 |
| GTA | 注意力级相对编码 | SE(3)外参 + 值变换 |
| **PRoPE（本文）** | **注意力级相对编码** | **完整投影变换（内参+外参）+ patch坐标** |

### 主要结果

PRoPE在多个任务上展现出一致且显著的性能提升：

- **新视角合成**（RealEstate10K，恒定内参）：PSNR从20.48（Plücker Raymap）提升至22.80（**+2.32**）；
- **新视角合成**（变化内参场景）：PSNR从19.89提升至21.42（**+1.53**），显著超越GTA等仅建模外参的方法；
- **立体深度估计**（UniMatch+PRoPE）：Abs Rel在RGBD上从0.123降至0.105（**-14.6%**），在Scenes11上从0.065降至0.049（**-24.6%**）；
- **空间认知任务**（DL3DV，9视图）：准确率从76.9%提升至93.0%（**+16.1%**）；
- **鲁棒性**：对测试时的长输入序列和未知焦距展现出强泛化能力；
- **缩放性**：在更大算力规模下，PRoPE依然保持对Plücker raymap的优势。

### 局限与展望

PRoPE当前假设针孔相机模型，未考虑镜头畸变；在极端焦距下投影矩阵与特征向量相乘可能引入数值不稳定。未来工作可探索扩展到通用相机模型、设计更稳定的数值方案，以及在机器人导航等更广泛的多模态任务中验证其泛化能力。

### 多视角Transformer中的位置编码困境

多视角三维视觉任务——包括新视角合成、立体深度估计和空间认知——的核心挑战在于，模型必须将多个相机捕获的二维图像信息融合为一致的三维表示。这一过程与语言模型中序列位置信息的处理有着本质的相似性：Transformer架构本身不具备对输入顺序或空间关系的感知能力，必须通过额外的“位置编码”机制将结构信息注入模型。

在多视角场景中，这种“位置信息”体现为每张图像对应的相机参数，包括内参（焦距、主点等）和外参（相机在世界坐标系中的位姿）。然而，现有的相机条件化方法存在一个根本性的瓶颈：**它们要么将相机信息编码为绑定于全局坐标系的绝对表示，难以泛化到不同的相机配置和场景；要么仅考虑相机之间的外参关系，完全忽略了内参变化对多视角几何推理的影响**。

### 现有方法的局限性

当前主流的多视角Transformer普遍采用**绝对编码策略**，最典型的代表是**Plücker Raymap**——将每个像素对应的Plücker坐标直接拼接到token特征中。这种token级别的绝对编码虽然同时捕获了内参和外参信息，但它将相机参数固化在全局坐标系下，导致模型对训练时未见过的相机内参、视角数量或场景几何缺乏鲁棒性。实验表明，当测试场景中的相机焦距发生变化时，基于raymap的方法性能显著下降。

另一类方法是**基于注意力的相对位姿编码**，如**CAPE**和**GTA**（Geometric Transform Attention）。这些方法通过将相机之间的SE(3)刚性变换注入自注意力机制，避免了对全局坐标系的一致定义，并且与FlashAttention等融合注意力核兼容。然而，它们的设计存在一个关键缺口：**仅编码了相机外参的相对关系，而完全忽略了内参**。在真实世界的多视角数据中，相机内参往往随场景或采集设备而变化，忽略内参意味着模型无法感知视锥体形状的差异，从而限制了多视角几何推理的上限。

### PRoPE的核心动机

本文的核心洞察是：**相机之间的完整投影变换——同时包含内参和外参——应当作为注意力机制中的相对位置编码**。具体而言，对于两个相机$i_1$和$i_2$，它们之间的投影关系由矩阵$\tilde{P}_{i_1} \tilde{P}_{i_2}^{-1}$完整描述，其中$\tilde{P}_i$编码了相机$i$的完整视锥体（内参+外参）。将这种投影关系注入注意力计算，使得模型能够在保持全局坐标系不变性的同时，显式地建模视锥体之间的几何对应关系。

这一设计动机源于一个简单的观察：在语言模型中，相对位置编码（如RoPE）通过编码token之间的相对距离，赋予了模型对序列长度的泛化能力。类似地，在多视角Transformer中，**将相机视为“相对位置编码”**——即用相机之间的投影变换替代token之间的序列距离——有望使模型获得对相机参数变化和视角数量变化的强鲁棒性。PRoPE正是沿着这一思路，将相机条件化从token级别的绝对编码提升为注意力级别的相对投影编码。

## 核心方法与创新机理

### 瓶颈：绝对相机编码的泛化困境

当前多视角Transformer的主流方案是将相机参数编码为逐token的绝对位置信息（如Plücker raymap），然后拼接到输入序列中。这种范式存在两个根本性局限：

1. **绑定全局坐标系**：绝对编码（raymap）将每个像素的光线方向与原点绑定于统一的世界坐标系下。当场景中的相机内参（焦距、主点）发生变化时，同一空间点在像素平面上的投影关系发生改变，绝对编码无法自然地捕捉这种跨视锥体的几何变换，导致模型泛化能力受限。

2. **相对位姿编码忽略内参**：已有的注意力层级相对编码方法，如**CAPE**和**GTA**，仅编码相机之间的SE(3)刚体变换（外参），完全忽略了相机内参（焦距、主点等）对视锥体形状的影响。这使得模型无法感知不同相机之间由于变焦或传感器差异引起的投影变化，限制了多视角几何推理的上限。

### 核心洞察：相机全投影作为相对位置编码

PRoPE的核心洞察在于：**将相机之间的完整投影变换（同时包含内参和外参）作为注意力机制中的相对位置编码**。这一设计与语言模型中相对位置编码的逻辑一脉相承——正如语言模型需要编码token之间的相对序列位置，多视角Transformer也需要编码相机视锥体之间的相对投影关系。

具体而言，对于任意两个相机 $i_1$ 和 $i_2$，PRoPE编码它们之间的完整投影变换：

$$\tilde{P}_{i_1} \tilde{P}_{i_2}^{-1}$$

其中 $\tilde{P}_i = K_i [R_i^{cw} \mid t_i^{cw}]$ 是相机 $i$ 的完整投影矩阵，同时包含了内参矩阵 $K_i$ 和外参 $(R_i^{cw}, t_i^{cw})$。这一变换直接描述了从相机 $i_2$ 的图像平面到相机 $i_1$ 的图像平面的映射关系，使注意力机制能够显式地建模“一个相机中的像素在另一个相机中对应哪个位置”的几何约束。

### 关键改动：从绝对Raymap到注意力层级投影编码

PRoPE对现有范式做出的核心改动如下表所示：

| 改动维度 | 基线方案 | PRoPE方案 |
|---------|---------|----------|
| **编码层级** | Token-level（逐token拼接） | Attention-level（注入注意力计算） |
| **编码内容** | 绝对光线参数（Plücker/Navie raymap） | 相对投影变换（内参+外参） |
| **坐标系依赖** | 依赖全局坐标系定义 | 仅依赖相对关系，全局坐标系无关 |
| **内参建模** | 隐含于光线方向中 | 显式编码于投影矩阵 |

PRoPE通过**GTA风格的注意力机制**注入这一相对编码。具体而言，它将投影变换构造为块对角矩阵 $\mathbf{D}_t^{\mathtt{PRoPE}}$，该矩阵由两部分组成：

$$\mathbf{D}_t^{\mathtt{PRoPE}} = \begin{bmatrix} \mathbf{D}_t^{\mathtt{Proj}} & \mathbf{0} \\ \mathbf{0} & \mathbf{D}_t^{\mathtt{RoPE}} \end{bmatrix}$$

其中：
- **$\mathbf{D}_t^{\mathtt{Proj}}$**：编码相机间的相对投影关系，由对齐的投影矩阵 $\tilde{\pmb P}_{i(t)}$ 通过克罗内克积构造。
- **$\mathbf{D}_t^{\mathtt{RoPE}}$**：编码图像内patch坐标的相对位置，使用旋转位置编码（RoPE）。

这些矩阵通过以下注意力公式作用于Q、K、V：

$$\mathrm{Attn}^{\mathbb{GTA}}(Q, K, V) = \mathbf{D}^{\mathbb{GTA}} \otimes \mathrm{Attn}\left((\mathbf{D}^{\mathbb{GTA}})^\top \otimes Q, (\mathbf{D}^{\mathbb{GTA}})^{-1} \otimes K, (\mathbf{D}^{\mathbb{GTA}})^{-1} \otimes V\right)$$

### 创新独特性分析

PRoPE与现有方案的差异集中体现在**对相机内参的显式建模**：

- **vs. Plücker Raymap**：Raymap将内参隐含地编码在光线方向中，但这是绝对编码，无法捕捉相机间的相对内参变化。当测试时遇到未见过的焦距时，Raymap的泛化能力显著下降（见Table 2，PRoPE在变内参场景下PSNR领先+1.53 dB）。

- **vs. CAPE/GTA**：这些方法仅编码SE(3)外参变换，完全忽略了内参。PRoPE通过投影矩阵 $\tilde{P}$ 同时编码内参和外参，使得注意力机制能够感知“变焦”引起的视锥体形状变化。消融实验（Table A.1）证实，移除投影项 $\mathbf{D}_t^{\mathtt{Proj}}$ 会导致PSNR从21.78骤降至16.04，证明相机间投影关系是核心贡献。

- **vs. CamRay**：CamRay是一种token-level的内参编码（相机坐标系下的光线方向），但它仍然是绝对编码，且无法编码相机间的相对内参关系。PRoPE可以与CamRay互补使用，形成混合编码策略（Table 3），但纯注意力的PRoPE已经优于GTA+CamRay的混合方案。

### 需要人工核实的内容

- 文中未提供CAPE和GTA的具体引用信息（作者/会议/年份），需查阅原文补充。
- 投影变换的非交换性带来的数值稳定性问题在极端焦距下的具体表现缺乏定量分析，仅作为局限性提及。

PRoPE 的设计遵循一个核心原则：**将相机之间的完整投影变换注入到 Transformer 的注意力层中，作为一种相对位置编码**。这一框架不修改模型的主体架构，而是通过替换标准自注意力中的相对变换矩阵，将多视角几何先验无缝嵌入到现有的多视角 Transformer 中。

### 输入表示

模型的输入为多视角图像及其对应的相机参数。对于 $N$ 个输入视图，每个视图 $i$ 提供：
- 图像 $I_i$
- 内参矩阵 $K_i$（包含焦距和主点）
- 外参矩阵 $T_i^{cw}$（从世界坐标系到相机坐标系的刚体变换）

图像首先被划分为 patch，每个 patch 被映射为一个 token。与绝对编码方法（如 Plücker raymap）不同，PRoPE **不将相机参数编码为 token 级别的输入特征**，而是将其转化为注意力层中的相对位置编码。这意味着相机信息仅通过注意力机制中的几何变换来注入，而非作为额外的输入通道拼接在 token 上。

### 核心模块：PRoPE 注意力

PRoPE 的注意力机制建立在 **GTA（Geometric Transform Attention）** 的框架之上。GTA 注意力通过块对角矩阵 $\mathbf{D}^{\text{GTA}}$ 对查询 $\mathbf{Q}$、键 $\mathbf{K}$ 和值 $\mathbf{V}$ 进行变换，从而将相对位姿信息注入到注意力计算中：

$$\mathrm{Attn}^{\mathbb{G}\mathrm{TA}}(Q, K, V) = \mathbf{D}^{\mathbb{G}\mathrm{TA}} \otimes \mathrm{Attn}\left((\mathbf{D}^{\mathbb{G}\mathrm{TA}})^\top \otimes Q, (\mathbf{D}^{\mathbb{G}\mathrm{TA}})^{-1} \otimes K, (\mathbf{D}^{\mathbb{G}\mathrm{TA}})^{-1} \otimes V\right)$$

其中 $\otimes$ 表示分块矩阵乘法。PRoPE 的关键创新在于重新定义了 $\mathbf{D}$ 矩阵的内容：**将 GTA 中仅编码外参相对位姿的 $\mathbf{D}^{\text{GTA}}$ 替换为同时编码内参和外参的 $\mathbf{D}^{\text{PRoPE}}$**。

### PRoPE 的块矩阵结构

PRoPE 的变换矩阵是一个块对角矩阵，由两个子模块组成：

$$\mathbf{D}_t^{\mathtt{PRoPE}} = \begin{bmatrix} \mathbf{D}_t^{\mathtt{Proj}} & \mathbf{0} \\ \mathbf{0} & \mathbf{D}_t^{\mathtt{RoPE}} \end{bmatrix}$$

**投影子项 $\mathbf{D}_t^{\mathtt{Proj}}$** 编码相机之间的完整投影变换。对于任意两个相机 $i_1$ 和 $i_2$，它们之间的投影关系由全视锥体变换矩阵给出：

$$\tilde{P}_{i_1} \tilde{P}_{i_2}^{-1}$$

其中 $\tilde{P}_i = K_i T_i^{cw}$ 是相机 $i$ 的完整投影矩阵，同时包含内参和外参。$\mathbf{D}_t^{\mathtt{Proj}}$ 通过对齐的相机投影矩阵构造，将这一投影关系编码为注意力中的相对变换：

$$\mathbf{D}_t^{\mathtt{Proj}} = \mathbf{I}_{d/8} \otimes \tilde{\pmb P}_{i(t)}$$

**RoPE 子项 $\mathbf{D}_t^{\mathtt{RoPE}}$** 编码图像内部 patch 之间的相对空间位置，使用旋转位置编码（RoPE）：

$$\mathbf{D}_t^{\mathsf{RoPE}} = \begin{bmatrix} \mathrm{RoPE}_{d/4}(x_t) & \mathbf{0} \\ \mathbf{0} & \mathrm{RoPE}_{d/4}(y_t) \end{bmatrix}$$

### 与混合编码的集成

PRoPE 作为注意力层级的相对编码，与 token 层级的绝对编码是**正交且可组合的**。在混合编码方案中（Figure 2, Table 3），PRoPE 负责在注意力中建模相机视锥体之间的投影关系，而 **CamRay**（相机坐标系下的 raymap）作为 token 层级的输入特征，编码局部的光线方向。两者同时使用时，PRoPE 已能单独达到或超越 GTA+CamRay 组合的性能（Table 3），表明注意力层级的投影建模本身就足以捕获关键的相机几何信息。

### 数据流总结

1. **输入**：多视角图像 patch tokens + 相机参数 $(K_i, T_i^{cw})$
2. **Token 层级**：可选地拼接 CamRay 作为局部光线编码
3. **注意力层级**：在每个自注意力层中，根据 token 所属的相机索引，构造 $\mathbf{D}_t^{\mathtt{PRoPE}}$ 矩阵，通过 GTA 风格的注意力机制注入投影几何关系
4. **输出**：经过多视角几何增强的特征表示，可直接用于新视角合成、深度估计等下游任务

PRoPE 的核心思想是将多视角Transformer中的相机条件化从**绝对编码**（如Plücker raymap）转变为**注意力层级的相对位置编码**，显式建模完整相机视锥体之间的投影变换关系。其技术实现建立在GTA（Geometric Transform Attention）框架之上，但将注入的相对变换从纯外参的SE(3)位姿替换为同时包含内参和外参的投影矩阵。

### 关键模块架构

PRoPE 由三个核心模块协同构成，分别编码不同层级的几何关系：

**D_t^{Proj} — 相机间投影变换编码**
这是PRoPE区别于所有现有方法的决定性模块。它计算不同相机视锥体之间的完整投影关系 $\tilde{P}_{i_1} \tilde{P}_{i_2}^{-1}$，其中 $\tilde{P}_i = K_i [R_i^{cw} | t_i^{cw}]$ 为相机的3×4投影矩阵，同时包含了内参矩阵 $K_i$ 和外参 $(R_i^{cw}, t_i^{cw})$。该投影变换直接编码了“从相机 $i_2$ 的图像平面到相机 $i_1$ 的图像平面”的完整映射关系，而非仅编码相机中心之间的刚体运动。在注意力机制中，该模块以块对角矩阵形式作用于每个token对的Query和Key向量。

**D_t^{RoPE} — 图像内Patch坐标编码**
该模块使用旋转位置编码（RoPE）对每个patch在其所属图像内的二维坐标 $(x_t, y_t)$ 进行编码。它独立于相机参数，确保模型能够感知同一图像内不同patch之间的空间邻近关系。其形式为对patch的x坐标和y坐标分别应用RoPE后组成的块对角矩阵。

**GTA风格注意力 — 相对变换注入机制**
PRoPE 采用GTA提出的注意力变体，将相对变换同时注入到Q、K、V矩阵中。对于任意两个token $t_1$ 和 $t_2$，注意力计算形式为：

$$[\text{Attn}^{\text{GTA}}(Q,K,V)]_{t_1} = \sum_{t_2} \alpha_{t_1,t_2} \mathbf{D}_{t_1}^{\text{GTA}} (\mathbf{D}_{t_2}^{\text{GTA}})^{-1} V_{t_2}$$

其中 $\mathbf{D}_t^{\text{GTA}}$ 是token $t$ 对应的变换矩阵。该机制的核心优势在于：相对变换 $\mathbf{D}_{t_1} \mathbf{D}_{t_2}^{-1}$ 自然地出现在注意力输出中，使模型能够在计算token间交互时直接感知它们之间的几何关系。

### PRoPE的完整块矩阵构造

PRoPE将投影编码和RoPE编码组合为一个统一的块对角矩阵：

$$\mathbf{D}_t^{\text{PRoPE}} = \begin{bmatrix} \mathbf{D}_t^{\text{Proj}} & \mathbf{0} \\ \mathbf{0} & \mathbf{D}_t^{\text{RoPE}} \end{bmatrix}$$

其中：

$$\mathbf{D}_t^{\text{Proj}} = \mathbf{I}_{d/8} \otimes \tilde{\mathbf{P}}_{i(t)}$$

$$\mathbf{D}_t^{\text{RoPE}} = \begin{bmatrix} \text{RoPE}_{d/4}(x_t) & \mathbf{0} \\ \mathbf{0} & \text{RoPE}_{d/4}(y_t) \end{bmatrix}$$

这里 $\tilde{\mathbf{P}}_{i(t)}$ 是token $t$ 所属相机 $i$ 的投影矩阵，$\otimes$ 表示克罗内克积，$\mathbf{I}_{d/8}$ 是 $d/8$ 维单位矩阵。该构造将投影变换复制到特征维度的一个子空间上，同时为patch坐标保留独立的编码子空间。

### 与基线方法的本质区别

PRoPE与现有方法的关键差异体现在**changed_slots**中：

- **Plücker Raymap（绝对编码）**：将每个像素的Plücker坐标（方向向量+矩向量）直接拼接到token特征中，绑定于全局坐标系，缺乏对相机间相对关系的显式建模。
- **CAPE / GTA（相对SE(3)编码）**：仅在注意力中注入相机外参之间的相对刚体变换，完全忽略了内参（焦距、主点）对视锥体几何的影响。
- **PRoPE**：将完整的投影矩阵 $\tilde{\mathbf{P}}_i$（同时包含内参和外参）作为每个token的“位置标识”，使得注意力计算中的相对变换 $\mathbf{D}_{t_1}^{\text{PRoPE}} (\mathbf{D}_{t_2}^{\text{PRoPE}})^{-1}$ 自然地编码了“从token $t_2$ 的图像坐标到token $t_1$ 的图像坐标”的完整映射关系。消融实验（Table A.1）证实，移除 $\mathbf{D}_t^{\text{Proj}}$ 会导致PSNR从21.78骤降至16.04，证明相机间投影关系是PRoPE性能的核心贡献因素。

> **注意**：上述公式均来自论文Section 3.3和Section 3.4（Equation 14-19），变量含义已通过verified_analysis中的formulas条目交叉验证。未在verified_analysis中出现的公式细节（如具体的维度分配策略）未做推测性展开。

## 实验与关键发现

### 核心瓶颈与因果机制

现有多视角Transformer普遍依赖**绝对相机编码**（如Plücker raymap），将每像素的射线坐标直接拼接为token级特征。这种编码绑定于全局坐标系，导致模型难以泛化到不同相机内参和场景布局。另一类方法采用**相对位姿编码**（如CAPE、GTA），在注意力层注入相机间的SE(3)外参关系，但完全忽略了相机内参（焦距、主点等），限制了多视角几何推理的上限。

PRoPE的因果调节点在于：**将相机编码从绝对raymap替换为基于注意力的相对投影编码**。具体而言，PRoPE在GTA注意力框架中注入相机全视锥体之间的完整投影变换（同时包含内参和外参），使模型能够在保持全局坐标系不变性的前提下，显式捕捉视锥体间的几何对应关系。这一设计直接解决了raymap的泛化瓶颈和纯外参编码的信息缺失问题。

---

### 新视角合成主结果

#### 恒定内参场景

在RealEstate10K数据集上，所有场景内相机内参保持恒定。PRoPE在LVSM框架下取得**PSNR 22.80**，相比Plücker raymap（20.48）提升**+2.32 dB**，显著优于Naive Raymap（20.60）、CAPE（21.82）和GTA（21.97）。这表明即使在内参不变的情况下，相对投影编码也比绝对raymap提供了更强的几何归纳偏置（Table 1）。

![[assets/figures/papers/paper_list_l29_https_arxiv_org_abs_2507_10496/figures/002_Table_1.jpg]]
*Table 1: Novel view synthesis comparison, with constant intrinsics in each scene. We compare different camera conditioning approaches applied to the LVSM [8] framework. Table 2: Novel view synthesis, with varying intrinsics in each scene. We compare the LVSM [8] model trained with different camera conditioning strategies, on intrinsics-augmented dataset variants*

#### 变化内参场景

当场景内相机内参随机变化时，PRoPE的优势进一步扩大。在RealEstate10K上达到**PSNR 21.42**，超过Plücker raymap（19.89）**+1.53 dB**；在Objaverse上达到**PSNR 22.98**，超过Plücker raymap（21.43）**+1.55 dB**。值得注意的是，仅考虑外参的相对编码方法CAPE（20.40 / 22.55）和GTA（20.70 / 22.69）在此设定下明显落后于PRoPE，直接验证了**内参建模是相对编码方法的关键缺失**（Table 2）。

---

### 混合编码策略

PRoPE作为注意力级编码，与token级编码天然兼容。将PRoPE与CamRay（相机坐标系下的raymap，仅编码内参）结合后，性能进一步提升：在RealEstate10K上达到**PSNR 21.78**，Objaverse上达到**PSNR 22.98**。关键发现是：**纯注意力的PRoPE（21.42 / 22.82）已经优于GTA+CamRay混合方案（21.41 / 22.69）**，说明在注意力层统一建模投影关系比“外参加token级内参”的分离式方案更有效（Table 3）。

![[assets/figures/papers/paper_list_l29_https_arxiv_org_abs_2507_10496/figures/004_Table_3.jpg]]
*Table 3: Novel view synthesis with hybrid camera encodings, with varying intrinsics in each scene. Intrinsics can be conditioned by concatenating local frame camera rays to the network input*

---

### 分布外鲁棒性

PRoPE在测试时展现出强鲁棒性（Figure 4, 5, 6）：
- **长序列泛化**：模型仅在2视图上训练，测试时扩展到16视图。PRoPE的PSNR下降幅度显著小于Plücker raymap和GTA，表明相对投影编码天然适应视图数量的变化。
- **未知焦距泛化**：测试焦距在1×–5×范围内变化时，PRoPE始终保持对GTA的优势。这归因于PRoPE在注意力中显式建模了相对内参关系，而GTA仅依赖外参。

---

### 任务泛化

#### 立体深度估计

将PRoPE集成到UniMatch立体匹配模型中，在多个数据集上取得一致改进（Table 4）：
- **RGBD**：Abs Rel从0.123降至**0.105**（↓14.6%）
- **Scenes11**：Abs Rel从0.065降至**0.049**（↓24.6%）
- **SUN3D**：Abs Rel从0.052降至**0.048**（↓7.7%）

![[assets/figures/papers/paper_list_l29_https_arxiv_org_abs_2507_10496/figures/009_Table_4.jpg]]
*Table 4: Performance Improvement on Stereo Depth Estimation Task with UniMatch [14]. †The “Sq Rel” metric is less reliable on the RGBD dataset due to the imperfect depth and camera pose [64]. Figure 7: Qualitative Results on Stereo Depth Estimation Task. Attention-level camera conditioning in UniMatch [14] leads to significant estimation improvements*

PRoPE未引入额外参数，仅通过替换注意力中的位置编码即可提升深度估计精度，验证了投影关系编码对稠密匹配任务的通用价值。

#### 空间认知

在DL3DV数据集上，模型需检测“图像-相机参数不一致”的样本对（Figure A.3）。PRoPE+CamRay在9视图设定下达到**93.0%准确率**，远超Plücker raymap的**76.9%**（+16.1个百分点）。CamRay单独使用时准确率为86.0%，PRoPE的加入进一步提升了7个百分点，说明相对投影编码帮助模型更好地理解跨视图的几何一致性（Table 5）。

![[assets/figures/papers/paper_list_l29_https_arxiv_org_abs_2507_10496/figures/010_Table_5.jpg]]
*Table 5: Spatial cognition results. We report the accuracy of detecting inconsistent image-camera pairs on the DL3DV [15] dataset under varying numbers of input views. Both CamRay and PRoPE significantly help with performance, without introducing additional model parameters. An illustration of this task can be found in Figure A.3*

---

### 消融实验

对PRoPE的两个核心组件进行消融（Table A.1）：
- **移除投影项 $D_t^{\text{Proj}}$**：PSNR从21.78骤降至**16.04**，降幅达5.74 dB，证明相机间的投影关系是PRoPE性能的主要来源。
- **移除RoPE项 $D_t^{\text{RoPE}}$**：PSNR降至21.39，降幅0.39 dB，表明patch相对位置编码有辅助作用但贡献较小。

![[assets/figures/papers/paper_list_l29_https_arxiv_org_abs_2507_10496/figures/015_Table.jpg]]
*Table: PSNR (↑) across zoom-in levels. SSIM (↑) across zoom-in levels. LPIPS (↓) across zoom-in levels. Table A.3: Additional Novel View Synthesis Results on Out-of-distribution Intrinsics at Test Time. Experiments are conducted with LVSM on RealEstate10K dataset with augmented intrinsics (1-3× zoom-in) as described in Section 4.3*

![[assets/figures/papers/paper_list_l29_https_arxiv_org_abs_2507_10496/figures/016_Table.jpg]]
*Table: abs_rel (↓) across zoom-in levels. sq_rel (↓) across zoom-in levels. rmse (↓) across zoom-in levels. rmse_log (↓) across zoom-in levels. Table A.4: Additional Stereo Depth Estimation Results on Out-of-distribution Intrinsics at Test Time. Experiments are conducted with UniMatch ’s official code as described in Section 4.6 but with 1/8 of the training resources (2 GPUs x 50k steps)*

---

### 缩放实验

在更大算力规模下（更多GPU和训练步数），PRoPE依然保持对Plücker raymap的稳定优势（Table 6）：
- 小规模：PRoPE 21.78 vs Plücker 20.48（+1.30）
- 大规模：PRoPE 23.10 vs Plücker 21.82（+1.28）

![[assets/figures/papers/paper_list_l29_https_arxiv_org_abs_2507_10496/figures/011_Table_6.jpg]]
*Table 6: Scaling LVSM with increased compute. We compare LVSM [8] models trained with Plücker raymaps versus PRoPE on RealEstate10K [12] at two compute scales*

这表明PRoPE的增益不会随模型容量增加而消失，具有良好的可扩展性。

---

### 失败模式与局限性

1. **极端焦距的数值稳定性**：当测试焦距远超训练分布（如5×以上变焦）时，投影矩阵与Q/K/V向量的直接相乘可能导致数值不稳定。论文未给出具体失效阈值，需要手动验证。
2. **针孔模型假设**：当前PRoPE仅适用于针孔相机，未考虑镜头畸变等更复杂的相机模型。对于鱼眼或广角畸变明显的场景，投影变换的精度会下降。
3. **非交换性限制**：投影变换的非交换性使得无法像RoPE那样通过多频编码注入相机参数，限制了更丰富的频率表示。这可能是PRoPE在极细粒度几何任务上的潜在瓶颈。
4. **CamRay与PRoPE的冲突**：在分布外焦距测试中，PRoPE+CamRay的性能反而不如纯PRoPE（Table A.3），说明token级内参编码可能与注意力级投影编码产生信息冲突，具体机制尚不明确。

### 补充图表

![[assets/figures/papers/paper_list_l29_https_arxiv_org_abs_2507_10496/figures/005_Figure_3.jpg]]
*Figure 3: Out-of-distribution tasks. Left: We evaluate camera conditioning methods on both longer sequence lengths and unseen camera intrinsics. Right: PRoPE improves results for both unseen sequence lengths and unseen intrinsics*

![[assets/figures/papers/paper_list_l29_https_arxiv_org_abs_2507_10496/figures/008_Table.jpg]]

![[assets/figures/papers/paper_list_l29_https_arxiv_org_abs_2507_10496/figures/012_Table.jpg]]
*Table: A.1: Ablation Study on PRoPE. \overline { { \mathbf { D } _ { t } ^ { \mathrm { P r o j } } } } is crucial for encoding the relative camera information, and \mathbf { D } _ { t } ^ { \mathrm { R o P E } } is also helpful to capture the relative patch coordinate. Experiments are conducted on RealEstate10K with CamRay as input*

![[assets/figures/papers/paper_list_l29_https_arxiv_org_abs_2507_10496/figures/014_Table.jpg]]

## 定位与知识库关联

### 1. 相机条件化的技术谱系

多视角Transformer中“如何让模型感知相机参数”这一问题，形成了从**绝对编码**到**相对位姿编码**再到**全视锥体投影编码**的演进路线。PRoPE处于该谱系的最新节点，其核心突破在于将编码对象从“全局坐标系中的射线”或“相机间的刚体运动”拓展为“相机完整投影变换（含内参与外参）”。

#### 1.1 绝对编码：将相机信息注入Token级表示

早期多视角Transformer采用**绝对编码**策略，将相机参数转换为逐像素（per-pixel）的特征向量，直接拼接到输入Token上。代表性方案包括：

- **Naive Raymap**：对每像素计算光线原点 $o_i$ 和方向向量 $d_i^{u,v}$，形成 $\mathbf{M}_{i,\text{Naive}}^{u,v} = [o_i, d_i^{u,v}] \in \mathbb{R}^6$ 的6维编码。该编码绑定于全局坐标系，光线原点随相机位姿变化，缺乏对光线本身的等变表示。

- **Plücker Raymap**：将原点项替换为矩项（moment term）$\mathbf{M}_{i,\text{Plücker}}^{u,v} = [d_i^{u,v}, o_i \times d_i^{u,v}] \in \mathbb{R}^6$，使光线表示对沿光线方向的平移具有不变性。这是当前多视角合成（如LVSM）中最广泛使用的绝对编码方案。

绝对编码的根本瓶颈在于：它们将相机信息“固化”在Token表示中，模型必须从数据中隐式学习不同相机参数下的几何对应关系。当测试场景的相机内参与训练分布不一致时（如焦距变化），这种隐式学习难以泛化——Table 2显示Plücker Raymap在变内参场景下PSNR仅19.89，远低于恒定内参下的20.48。

#### 1.2 相对位姿编码：在注意力层建模相机间几何关系

为克服绝对编码的泛化局限，研究者转向**注意力层级**的相对编码，将相机间的几何关系直接注入自注意力计算。这类方法不修改Token表示，而是通过变换注意力矩阵的Q/K/V来编码相对位姿：

- **CAPE**：将相机间的相对SE(3)位姿编码为注意力偏置，使模型显式感知两帧之间的刚体运动。但CAPE仅编码外参（相机位姿），完全忽略了内参（焦距、主点等）的差异。

- **GTA**：在CAPE基础上引入对Value矩阵的变换，通过块对角矩阵 $\mathbf{D}^{\text{GTA}}$ 同时作用于Q、K、V：
  $$
  \text{Attn}^{\text{GTA}}(Q, K, V) = \mathbf{D}^{\text{GTA}} \otimes \text{Attn}\left((\mathbf{D}^{\text{GTA}})^\top \otimes Q, (\mathbf{D}^{\text{GTA}})^{-1} \otimes K, (\mathbf{D}^{\text{GTA}})^{-1} \otimes V\right)
  $$
  GTA仍仅编码相对SE(3)位姿，未涉及相机内参。Table 1显示GTA在恒定内参下PSNR为21.21，优于Plücker Raymap的20.48，但在变内参场景下（Table 2），GTA的PSNR降至20.52，与PRoPE的21.42存在显著差距。

**关键瓶颈**：CAPE和GTA将“相机”简化为“无内参的刚体位姿”，忽略了视锥体形状（由焦距、传感器尺寸决定）对多视角几何推理的根本影响。当两个相机拍摄同一场景但焦距不同时，即使位姿相同，像素级对应关系也完全不同——这一差异无法通过纯SE(3)编码捕获。

#### 1.3 PRoPE：全视锥体投影编码

PRoPE将编码对象从“相机位姿”升级为“相机间的完整投影变换”，其核心构造为：

$$
\tilde{P}_{i_1} \tilde{P}_{i_2}^{-1}
$$

其中 $\tilde{P}_i = K_i [R_i^{cw} | t_i^{cw}]$ 是相机 $i$ 的完整投影矩阵（3×4），同时包含内参矩阵 $K_i$ 和外参 $[R_i^{cw} | t_i^{cw}]$。这一变换描述了从相机 $i_2$ 的图像平面到相机 $i_1$ 的图像平面的完整映射，自然编码了两相机视锥体之间的所有几何关系。

在注意力机制实现上，PRoPE沿用GTA的框架，但将 $\mathbf{D}^{\text{GTA}}$ 替换为块对角矩阵：

$$
\mathbf{D}_t^{\text{PRoPE}} = \begin{bmatrix} \mathbf{D}_t^{\text{Proj}} & \mathbf{0} \\ \mathbf{0} & \mathbf{D}_t^{\text{RoPE}} \end{bmatrix}
$$

其中：
- $\mathbf{D}_t^{\text{Proj}} = \mathbf{I}_{d/8} \otimes \tilde{P}_{i(t)}$ 编码相机投影关系（通过克罗内克积扩展到注意力头维度）
- $\mathbf{D}_t^{\text{RoPE}}$ 编码图像内patch坐标的相对位置（沿用RoPE的旋转编码）

这种设计使PRoPE同时具备三种能力：(1) 建模相机间的完整投影几何（含内参）；(2) 保持全局坐标系不变性（仅依赖相对关系）；(3) 兼容FlashAttention等融合注意力核。

### 2. 适用边界与局限

#### 2.1 已验证的适用场景

PRoPE在以下任务-数据组合中展现出显著且一致的性能提升：

| 任务 | 数据集 | 关键条件 | 性能增益（vs. Plücker） |
|------|--------|----------|-------------------------|
| 新视角合成 | RealEstate10K | 恒定内参 | +2.32 PSNR (Table 1) |
| 新视角合成 | RealEstate10K | 变化内参 | +1.53 PSNR (Table 2) |
| 新视角合成 | Objaverse | 变化内参 | +1.55 PSNR (Table 2) |
| 立体深度估计 | RGBD | 双目 | -0.018 Abs Rel (Table 4) |
| 立体深度估计 | Scenes11 | 双目 | -0.016 Abs Rel (Table 4) |
| 空间认知 | DL3DV | 9视图 | +16.1% 准确率 (Table 5) |

PRoPE对**测试时分布偏移**展现出强鲁棒性：在仅用2视图训练的情况下，测试时扩展到16视图仍优于所有对比方法（Figure 4a）；在1×-5×焦距变化范围内持续保持优势（Figure 4b）。此外，PRoPE与token级编码**CamRay**兼容，混合方案（PRoPE+CamRay）可进一步提升性能（Table 3），且PRoPE已可集成到CAT3D等多视角扩散模型中（Table A.2）。

#### 2.2 方法局限

**数值稳定性**：PRoPE通过投影矩阵 $\tilde{P}_i$ 直接作用于Q/K/V向量。当相机焦距极端（如长焦）时，投影矩阵的条件数恶化，可能导致注意力计算中的数值不稳定。论文未提供矩阵归一化或正则化策略。

**相机模型假设**：当前PRoPE假设针孔相机模型（pinhole camera），未考虑镜头畸变、卷帘快门等实际相机特性。对于具有显著畸变的广角相机，投影矩阵无法准确描述像素级对应关系。

**频率表示受限**：由于投影变换的非交换性（non-commutativity），PRoPE无法像标准RoPE那样通过多频编码注入丰富的频率信息。这限制了模型对不同尺度几何关系的感知能力，可能影响细粒度深度估计或高频纹理重建。

**计算开销的边际效应**：虽然PRoPE不引入额外模型参数，但GTA风格的注意力需要对Q/K/V进行矩阵乘法变换。在极大规模模型或实时应用中，这一开销可能变得显著。Table 6显示在更大算力规模下PRoPE仍保持优势，但未报告绝对延迟数据。

### 3. 开放问题

**极长焦距下的稳定化**：能否通过投影矩阵的归一化（如按焦距缩放）或采用对数极坐标表示来改善数值条件？这需要理论分析和实证验证。

**通用相机模型扩展**：如何将PRoPE扩展到包含畸变参数的相机模型？一种可能方向是对每个patch计算局部投影近似，但会增加计算复杂度。另一种思路是将畸变参数作为额外的token级条件注入，与PRoPE的投影编码形成互补。

**多频投影编码**：为非交换的投影变换设计多频编码方案是一个开放的理论问题。可能的路径包括：在投影矩阵的李代数空间中进行频率分解，或采用可学习的频率基函数。

**跨任务泛化边界**：PRoPE在机器人导航、3D重建、多模态对齐等任务中的有效性尚未验证。这些任务对相机几何的依赖方式与新视角合成不同，PRoPE的投影编码是否仍是最优选择需要进一步研究。

**与绝对编码的理论关系**：PRoPE作为相对编码，与Plücker Raymap等绝对编码在数学上是否存在等价或互补关系？理解两者的信息论特性可能指导更优的混合策略设计。

## 原文 PDF

![[paperPDFs/NEURIPS_2025/Cameras_as_Relative_Positional_Encoding.pdf]]
