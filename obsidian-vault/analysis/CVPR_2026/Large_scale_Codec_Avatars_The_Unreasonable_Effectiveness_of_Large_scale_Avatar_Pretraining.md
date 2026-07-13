---
title: "Large-scale Codec Avatars: The Unreasonable Effectiveness of Large-scale Avatar Pretraining"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Large_scale_Codec_Avatars_The_Unreasonable_Effectiveness_of_Large_scale_Avatar_Pretraining.pdf
project_link: "https://junxuan-li.github.io/lca"
code_link: null
aliases:
- LSCAL
- LSCAUELSAP
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 引入大规模预训练（百万级野外视频）与高质量后训练（数千人多视角工作室）两阶段范式，将泛化能力与高保真控制解耦：预训练阶段学习通用人体外观与几何先验，后训练阶段注入精细表情、手部驱动和多视角一致性。
primary_logic: 首次证明在3D头像建模中，大规模预训练-后训练范式可打破泛化-保真度不可兼得的固有矛盾；预训练的强泛化能力与后训练的高保真度通过残差双分支架构和对齐的潜在空间形成协同，实现前馈式通用高保真虚拟化身创建。
claims:
- 预训练→后训练方案在工作室和野外测试集上均优于混合训练，工作室PSNR从28.0提升至30.5，野外PSNR从28.0提升至28.2。
- LCA在野外多视角设置中比优化方法ExAvatar高出9.8 dB PSNR，在单视角设置中比LHM高出9.3 dB PSNR。
- 预训练数据规模从10K扩大到1M视频使野外PSNR持续提升（27.67→28.18），验证了大规模预训练的收益。
- 后训练注意力图展示出更干净的语义对应关系，且模型泛化至训练中未见的眼镜、头饰、风格化角色，甚至零样本支持重光照与宽松衣物。
---

# Large-scale Codec Avatars: The Unreasonable Effectiveness of Large-scale Avatar Pretraining

> [!tip] 核心洞察
> 首次证明在3D头像建模中，大规模预训练-后训练范式可打破泛化-保真度不可兼得的固有矛盾；预训练的强泛化能力与后训练的高保真度通过残差双分支架构和对齐的潜在空间形成协同，实现前馈式通用高保真虚拟化身创建。

| 字段 | 内容 |
|------|------|
| 中文题名 | 大规模Codec Avatars：大规模头像预训练的不合理有效性 |
| 英文题名 | Large-scale Codec Avatars: The Unreasonable Effectiveness of Large-scale Avatar Pretraining |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2604.02320) · [Project](https://junxuan-li.github.io/lca) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Large-scale Codec Avatars (LCA) |
| Dataset | Capture-Studio, In-the-Wild, Capture-Studio, Multiview, In-the-Wild, Multiview |

> [!tip] 效果简介
> - Capture-Studio (多视角工作室) 上，PSNR↑ 30.514 vs 28.000 (混合训练) (+2.5)。
> - In-the-Wild (野外) 上，PSNR↑ 28.175 vs 27.998 (混合训练) (+0.2)。
> - Capture-Studio, Multiview 上，PSNR↑ 27.483 vs 23.925 (ExAvatar) (+3.56)。

## 概要

现有3D头像方法面临一个根本性瓶颈：工作室捕捉数据保真度高但缺乏多样性，野外数据覆盖广但因单目稀疏导致3D几何模糊——两者无法同时提供足够的外观多样性与精确几何监督，使泛化能力与重建保真度长期处于不可兼得的矛盾之中。

本文提出**Large-scale Codec Avatars (LCA)**，首次在3D头像建模中引入大规模预训练-后训练两阶段范式来解耦这一矛盾。其核心洞察是：通过在百万级野外视频上进行预训练，模型习得通用的3D人体外观与几何先验，获得强泛化能力；随后在数千人多视角工作室数据上进行高质量后训练，注入精细表情、手部驱动和多视角一致性，实现高保真控制。两阶段通过残差双分支解码器架构和对齐的潜在空间形成协同，最终实现前馈式通用高保真虚拟化身创建。

在方法定位上，LCA属于前馈式3D高斯头像方法，兼具单视图与多视图输入能力，与基于优化的方法（如ExAvatar）、单视图前馈方法（如LHM）以及2D视频扩散方法（如Wan-Animate）形成对比。其关键改进包括：残差双分支解码器（规范分支+姿态相关分支）、自监督面部表情潜在码与注视方向编码、可学习双层节点蒙皮权重校正模块（支持宽松衣物动画），以及交替执行图像注意力、几何注意力与多模态注意力的Transformer编码器架构。

主要实验结果验证了该范式的有效性：
- 预训练→后训练方案在工作室测试集上PSNR达30.5（混合训练为28.0），野外测试集达28.2（混合训练为28.0）；
- 在野外多视角设置中比优化方法ExAvatar高出9.8 dB PSNR，在单视角设置中比LHM高出9.3 dB PSNR；
- 预训练数据规模从10K扩大到1M视频使野外PSNR持续提升（27.67→28.18），验证了大规模预训练的收益；
- 模型泛化至训练中未见的眼镜、头饰、风格化角色，甚至零样本支持重光照与宽松衣物动画。

该方法仍存在若干局限：精细纹理（如刺绣、蕾丝）难以完美重建，严重遮挡与快速运动模糊下质量下降，次级运动（如头发飘动、配饰摆动）尚未支持，重光照模块依赖后训练灯光数据而未在野外光照下完全验证。



3D数字人化身在远程通信、游戏、影视和混合现实中具有广泛的应用前景。理想的化身系统需同时满足两个核心需求：**高保真度**（精确还原面部细节、手部姿态和身体几何）与**强泛化能力**（仅需少量日常照片即可快速创建，并适应多样的外貌、服饰和光照条件）。然而，现有方法在这两个目标之间长期面临不可兼得的困境。

### 现有方法的瓶颈：数据源的内在矛盾

当前3D头像方法通常依赖两类数据源，但各自存在根本性局限：

- **工作室多视角捕捉数据**：在可控光照和多相机设置下获得，能够提供精确的3D几何监督，重建保真度高。但采集成本高昂，且受试者数量有限、外貌和服饰多样性不足，导致模型泛化能力弱。
- **野外单目视频数据**：覆盖广泛的身份、姿态和场景，多样性丰富。但由于单目输入的稀疏性，3D几何监督模糊，重建结果往往缺乏精确的几何结构和细节保真度。

**核心瓶颈**在于：单一数据源无法同时提供足够的外观多样性与精确几何监督。将两类数据简单混合训练（mixed training）看似直观，实则难以调和二者在监督信号强度和数据分布上的差异，导致模型在泛化与保真度之间做出妥协。

### 本文动机：解耦泛化与保真度

本文提出一个根本性的问题：**能否通过训练范式的设计，打破泛化与保真度不可兼得的固有矛盾？**

受大语言模型“大规模预训练+高质量后训练”范式的启发，本文探索将其引入3D头像建模领域。核心假设是：预训练阶段在百万级野外视频上学习通用的人体外观与几何先验，赋予模型强泛化能力；后训练阶段在数千人多视角工作室数据上注入精细的表情、手部驱动和多视角一致性，实现高保真控制。两个阶段各司其职，通过架构设计形成协同，从而在前馈式推理中同时获得通用性与高保真度。

这一思路的关键在于：预训练所学的强泛化表征并非在后训练中被覆盖，而是作为基础被保留和精炼，最终使模型在工作室和野外测试场景下均能超越混合训练范式。



## 核心方法与创新机理

LCA 的核心创新在于首次将**大规模预训练-高质量后训练**的两阶段范式引入3D头像建模，从根本上解耦了泛化能力与重建保真度这一长期矛盾。其关键设计围绕以下四个 changed slots 展开。

### 1. 训练范式：从混合训练到预训练-后训练解耦

现有方法（如混合野外与工作室数据联合训练）受制于单一数据源的内在冲突——工作室数据提供精确多视角几何监督但缺乏外观多样性，野外数据覆盖广泛身份与场景却因单目稀疏导致3D几何模糊。LCA 将这一矛盾拆解为两个阶段：

- **大规模野外视频预训练**：在百万级野外视频上学习通用的人体外观与几何先验，赋予模型强泛化能力。
- **高质量多视角工作室后训练**：在数千人的多视角工作室数据上注入精细的表情、手部驱动和多视角一致性控制。

这一策略的因果效应在 Table 1 中得到直接验证：相比混合训练，预训练→后训练方案在工作室测试集上 PSNR 从 28.0 提升至 30.5，在野外测试集上从 28.0 提升至 28.2。更重要的是，该范式在 10× 缩减的数据规模下依然有效（Pre-100K + Post-500，Table S2），证明了策略本身的鲁棒性而非单纯依赖数据量。

### 2. 解码器架构：残差双分支设计

LCA 将高斯属性解码拆分为两个分支，形成残差结构：

- **规范分支** $H_{cano}$：从几何 token $T^{gs}$ 解码静态身份属性（颜色 $c$、位置 $p$、不透明度 $o$、旋转 $q$、尺度 $s$），对应公式 $c, p, o, q, s = H_{cano}(T^{gs})$。
- **姿态相关分支** $H_{pose}$：根据驱动信号（身体/手部姿态 $\theta$、自监督面部表情潜在码 $\varepsilon$、注视方向 $\psi$）预测属性增量 $\Delta c, \Delta p, \Delta q, \Delta s$，对应公式 $\Delta c, \Delta p, \Delta q, \Delta s = H_{pose}(T^{gs}, \theta, \varepsilon, \psi)$。

这一设计的优势在于：预训练阶段主要塑造规范分支的泛化能力，后训练阶段则精细调整姿态相关分支的驱动精度。消融实验（Table S1）证实双分支设计优于单分支变体——工作室 PSNR 从 30.370 提升至 30.514，野外 PSNR 从 27.936 提升至 28.175。同时，残差结构使推理高效：输入图像仅需一次 Transformer 和规范解码器处理，后续驱动仅调用轻量的姿态解码器。

### 3. 驱动信号编码：更丰富的表情与注视表示

基线方法通常仅使用身体姿态与表情基系数作为驱动信号。LCA 在此基础上加入**自监督学习的面部表情潜在码**和**注视方向**，构成更丰富的驱动向量。这一扩展使模型能够捕捉更精细的面部动态，尤其在野外场景下的表情泛化中发挥作用。该设计的因果效应未单独消融，但其作为姿态相关分支的输入组成部分，与双分支架构共同贡献了 Table 2 中相较于 LHM（单视图）和 ExAvatar（优化方法）的大幅领先。

### 4. 变形建模：可学习双层节点蒙皮校正

传统 LBS（Linear Blend Skinning）使用固定蒙皮权重，难以处理宽松衣物的自然变形。LCA 引入**可学习的双层节点蒙皮权重校正模块**：

$$W' = W(n) + H_{skin}(T^{node})$$

其中 $W(n)$ 为初始蒙皮权重，$H_{skin}$ 根据节点 token $T^{node}$ 预测校正量。该模块通过 ARAP（As-Rigid-As-Possible）损失和稀疏性正则化进行约束。消融实验（Table S3）表明，节点变形器使宽松衣物序列的 PSNR 从 24.538 显著提升至 26.013，有效减少衣物撕裂伪影（Figure 7）。

### 创新协同机制

上述四个 changed slots 并非孤立改进，而是通过**对齐的潜在空间**形成协同：预训练使几何 token 特征空间对野外和工作室身份呈现均匀分布（Figure S1），后训练在此空间上通过注意力图展示出更干净的语义对应关系（Figure 6），最终实现前馈式通用高保真虚拟化身创建——在野外多视角设置中比优化方法 ExAvatar 高出 9.8 dB PSNR，在单视角设置中比 LHM 高出 9.3 dB PSNR（Table 2）。



LCA 的整体 pipeline 遵循“图像/几何标记化 → 多模态 Transformer 编码 → 双分支高斯解码 → 蒙皮变形 → 可微渲染”的前馈流程，将稀疏输入图像转化为可驱动的高保真 3D 高斯头像。

### 输入与标记化

给定同一对象的 $N$ 张多视角图像（默认 $N=8$），系统从两个互补流构建 token：

- **图像 token**：对每张全身图像 $I_i^{body}$ 和面部裁剪 $I_i^{face}$，使用冻结的 Sapiens 视觉编码器 $E_{sap}$ 提取特征，经共享单层 MLP $F_{proj}$ 投影到 $D$ 维 token 空间：

  $$T_i^{body} = F_{proj}(E_{sap}(I_i^{body})), \quad T_i^{face} = F_{proj}(E_{sap}(I_i^{face}))$$

- **几何 token**：从规范姿态下的模板人体网格采样 $G$ 个锚点，其三维坐标 $X \in \mathbb{R}^{G \times 3}$ 经位置编码 $F_{PE}$ 和投影 MLP $F_{proj-gs}$ 生成几何 token $T^{gs}$：

  $$T^{gs} = F_{proj-gs}(F_{PE}(X))$$

### LCA Transformer 编码器

LCA 编码器由 $L=8$ 层 Transformer 组成，每层交替执行三种注意力操作以融合跨模态信息：

1. **图像自注意力**：在所有图像 token 间建模跨视角关系。
2. **几何自注意力**：在几何 token 间建模空间结构关系。
3. **多模态交叉注意力**：以几何 token 为 query，图像 token 为 key/value，将视觉外观信息注入几何表示。

这种交替设计使几何 token 逐步吸收多视角、多部位（全身+面部）的视觉特征，形成富含身份、几何与外观信息的紧凑表示。

### 双分支高斯解码器

编码后的几何 token $T^{gs}$ 被送入两个并行的解码分支，形成残差结构：

- **规范分支** $H_{cano}$：从 $T^{gs}$ 直接解码规范空间的高斯属性——颜色 $c$、位置 $p$、不透明度 $o$、旋转四元数 $q$、尺度 $s$：

  $$c, p, o, q, s = H_{cano}(T^{gs})$$

- **姿态相关分支** $H_{pose}$：以 $T^{gs}$ 和驱动信号（身体/手部姿态 $\theta$、面部表情潜在码 $\varepsilon$、注视方向 $\psi$）为输入，预测高斯属性的增量：

  $$\Delta c, \Delta p, \Delta q, \Delta s = H_{pose}(T^{gs}, \theta, \varepsilon, \psi)$$

最终高斯属性为规范值与增量之和。该残差设计的优势在于：规范分支只需推理一次即可固定身份外观，后续驱动仅需运行轻量的 $H_{pose}$，实现高效推理（Table S1 消融验证双分支优于单分支变体，工作室 PSNR 30.514 vs 30.370）。

### 蒙皮与变形

为将规范空间高斯变换到目标姿态，系统采用线性混合蒙皮（LBS）作为基础变形。针对宽松衣物等 LBS 固有局限，引入**双层节点变形器**：在 SMPL-X 顶点和稀疏节点两个层级上学习蒙皮权重校正 $W' = W(n) + H_{skin}(T^{node})$，使衣物变形更自然（Table S3 显示该模块将宽松衣物序列 PSNR 从 24.538 提升至 26.013）。

### 可微渲染与训练目标

变形后的高斯经可微光栅化器渲染为目标视角图像。训练损失同时监督规范视角 $\hat{I}_{cano}$ 和驱动姿态视角 $\hat{I}_{pose}$ 的重建质量：

$$L = L_{img}(I, \hat{I}_{cano}) + L_{img}(I, \hat{I}_{pose}) + \lambda L_{reg}(p, s)$$

其中 $L_{img}$ 为 $\ell_1$ 与 LPIPS 的组合损失，$L_{reg}$ 为高斯位置和尺度的正则化项。

### 两阶段训练范式

上述架构在**大规模预训练 → 高质量后训练**的范式下运行（Figure 2 右侧对比了两阶段的数据源差异）：

![[assets/figures/papers/paper_list_l1067_https_arxiv_org_abs_2604_02320/figures/002_Figure_2.jpg]]
*Figure 2: (Left) Overview. Given multiple images of a subject, we extract image tokens from full-body images and face crops, and geometric tokens from a template mesh. The LCA encoder alternates image-only, geometry-only, and multimodal attention to fuse information across streams. Our decoders, canonical and pose-dependent, predict Gaussian attributes, which are skinned via linear blend skinning (LBS) and rendered to novel views. Training uses photometric reconstruction losses*

- **预训练阶段**：使用百万级野外视频数据训练完整网络，学习通用人体外观与几何先验，赋予模型强泛化能力。
- **后训练阶段**：在数千人多视角工作室数据上微调，注入精细表情、手部驱动和多视角一致性，同时通过学习率衰减策略（$\gamma=0.65$）保护预训练知识不被灾难性遗忘（Table S1 显示 $\gamma=0.00$ 时工作室 PSNR 骤降至 27.464）。

这一范式解耦了“泛化”与“保真度”两个冲突目标，使最终模型在前馈推理中同时达到通用性与高保真度。



LCA 的核心架构由 **图像/几何标记化**、**LCA Transformer 编码器**、**双分支高斯解码器**、**蒙皮与变形模块** 以及 **可微高斯渲染器** 五个关键模块串联构成。下面按数据流顺序逐一展开。

### 图像与几何标记化

给定多视角输入图像，LCA 首先将视觉信号和几何先验统一为 token 序列。

**图像 token 生成**：对于每个视角 $i$ 的全身图像 $I_i^{body}$ 和面部裁剪 $I_i^{face}$，使用预训练的 Sapiens 特征提取器 $E_{sap}$ 获取图像特征，再通过共享的单层 MLP $F_{proj}$ 投影到 $D$ 维 token 空间：

$$T_i^{body} = F_{proj}(E_{sap}(I_i^{body})) \tag{1}$$
$$T_i^{face} = F_{proj}(E_{sap}(I_i^{face})) \tag{2}$$

**几何 token 生成**：从规范姿态下的模板人体网格上采样 $G$ 个锚点，其三维位置为 $X \in \mathbb{R}^{G \times 3}$。这些锚点经位置编码 $F_{PE}$ 后由投影网络 $F_{proj-gs}$ 映射为几何 token：

$$T^{gs} = F_{proj-gs}(F_{PE}(X)) \tag{3}$$

几何 token 作为 3D 结构先验贯穿整个网络，是连接图像特征与最终高斯属性的桥梁。

### LCA Transformer 编码器

编码器由 $L = 8$ 层 Transformer 构成，每层 token 维度 $D = 1024$。其核心设计在于 **交替执行三种注意力机制**，实现跨视角、跨模态的信息融合：

- **图像自注意力**：在所有图像 token（含全身与面部）之间传播外观信息；
- **几何自注意力**：在几何 token 之间建模 3D 结构关联；
- **多模态交叉注意力**：以几何 token 为 query，图像 token 为 key/value，将 2D 外观特征注入 3D 表示。

这种交替设计使得几何 token 能够有选择地聚合来自不同视角、不同身体部位的图像证据，为后续解码提供丰富的多模态表征。

### 双分支高斯解码器

解码器采用 **规范分支 + 姿态相关分支** 的残差结构，是 LCA 实现泛化与保真度解耦的关键。

**规范分支** 从几何 token 解码出规范空间下的高斯属性——颜色 $c$、位置 $p$、不透明度 $o$、旋转四元数 $q$ 和尺度 $s$：

$$c, p, o, q, s = H_{cano}(T^{gs}) \tag{8}$$

**姿态相关分支** 根据几何 token 和驱动信号（身体/手部姿态 $\theta$、表情潜在码 $\varepsilon$、注视方向 $\psi$）预测高斯属性的增量：

$$\Delta c, \Delta p, \Delta q, \Delta s = H_{pose}(T^{gs}, \theta, \varepsilon, \psi) \tag{9}$$

最终的高斯属性为规范输出与增量之和。这一设计的优势在于：规范分支捕获身份相关的静态外观，姿态分支仅需建模表情与姿态引起的偏差，推理时规范分支只需执行一次，后续驱动仅需轻量的姿态分支。

### 蒙皮与变形模块

将规范空间的高斯变换到目标姿态，基础方案采用线性混合蒙皮（LBS）。对于宽松衣物场景，LCA 引入 **可学习的双层节点变形器** 来校正蒙皮权重。

在模板网格上定义节点图，每个节点 $n$ 的初始蒙皮权重 $W(n)$ 经可学习网络 $H_{skin}$ 修正：

$$W' = W(n) + H_{skin}(T^{node}) \tag{14}$$

训练时对 $H_{skin}$ 施加 As-Rigid-As-Possible 正则化与 $\ell_1$ 稀疏约束，鼓励变形刚性的同时保持权重稀疏性。该模块使 LCA 能够自然地处理训练中未见过的宽松服饰动画，避免衣物撕裂伪影。

### 可微高斯渲染与训练损失

变形后的高斯通过可微光栅化渲染为图像。训练目标同时监督 **规范视角渲染** $\hat{I}_{cano}$ 和 **姿态视角渲染** $\hat{I}_{pose}$，每个渲染均采用 $\ell_1$ 与 LPIPS 的组合损失：

$$L_{img}(I, \hat{I}) = L_{\ell_1}(I, \hat{I}) + L_{LPIPS}(I, \hat{I}) \tag{10}$$

总损失加入高斯位置与尺度的正则项：

$$L = L_{img}(I, \hat{I}_{cano}) + L_{img}(I, \hat{I}_{pose}) + \lambda L_{reg}(p, s) \tag{12}$$

双视角监督迫使网络在规范空间中学习到一致的几何结构，同时确保姿态驱动下的外观保真度。

### 补充图表

![[assets/figures/papers/paper_list_l1067_https_arxiv_org_abs_2604_02320/figures/010_Figure_6.jpg]]
*Figure 6: Attention Map Visualization. Post-training yields cleaner semantic correspondences in last-layer attention maps between geometric and image tokens. The selected geometric tokens on the mesh are shown in red*



## 实验与关键发现

### 核心瓶颈验证：预训练-后训练范式解耦泛化与保真度

LCA的核心主张是：大规模野外预训练+高质量工作室后训练的两阶段范式，能够打破3D头像建模中“泛化-保真度不可兼得”的固有矛盾。**Table 1** 给出了决定性证据。在工作室测试集上，预训练→后训练方案达到 **30.514 PSNR**，而将野外与工作室数据打混训练的混合策略仅为28.000 PSNR（+2.5 dB）；在野外测试集上，预训练→后训练为 **28.175 PSNR**，混合策略为27.998 PSNR（+0.2 dB）。这一结果表明：预训练阶段从百万级野外视频中习得的通用人体外观与几何先验，在后续高质量后训练中并未被灾难性遗忘，反而与精细表情、手部驱动和多视角一致性监督形成协同，同时提升了保真度与泛化能力。

![[assets/figures/papers/paper_list_l1067_https_arxiv_org_abs_2604_02320/figures/005_Table_1.jpg]]
*Table 1: Effect of training schemes evaluated across domains*

消融实验进一步揭示了后训练阶段学习率衰减的关键作用（**Table S.1**）：当后训练学习率不衰减（γ=0.00）时，工作室PSNR骤降至27.464，表明预训练知识被快速覆盖；γ=0.65在保留预训练泛化能力与注入高保真细节之间取得最佳平衡。

### 与SOTA方法的定量对比

**Table 2** 报告了LCA与现有方法在多视角和单视角设置下的全面对比。

**多视角设置**：在工作室域，LCA以 **27.483 PSNR** 显著优于基于优化的 **ExAvatar**（23.925 PSNR，+3.56 dB）；在野外域，优势扩大至 **+9.79 dB**（LCA 27.802 vs. ExAvatar 18.010）。这一巨大差距揭示了优化方法对稀疏视角和域外外观的脆弱性，而LCA的预训练先验提供了强健的3D几何与外观初始化。

**单视角设置**：LCA在工作室域达到 **26.878 PSNR**，比前馈基线 **LHM**（21.897 PSNR）高出 **+4.98 dB**；在野外域，LCA以 **27.685 PSNR** 领先LHM（18.322 PSNR）**+9.36 dB**。值得注意的是，LCA在野外单视角下的PSNR（27.685）甚至接近其在工作室多视角下的表现（27.483），充分体现了大规模预训练带来的强泛化能力。

### 预训练数据规模的缩放效应

**Table 3** 展示了预训练数据规模从10K视频逐步扩大到1M视频的收益曲线。野外PSNR从27.665持续提升至28.175，验证了“数据规模越大，泛化越强”的缩放规律。更重要的是，**Table S.2** 表明即使在10×缩减的数据规模下（100K预训练身份+500后训练身份），预/后训练范式依然保持一致的性能趋势，证明了该策略的鲁棒性——并非单纯依赖数据量，而是范式本身具有内在优势。

### 架构设计消融

**双分支解码器**（**Table S.1**）：规范分支（静态身份）+姿态相关分支（动态表情/姿态）的残差设计优于单分支变体，工作室PSNR从30.370提升至30.514，野外PSNR从27.936提升至28.175。残差结构使模型将身份几何与表情驱动增量解耦，既提升了驱动效率，也增强了泛化能力。

**节点变形器**（**Table S.3**）：可学习的双层级节点蒙皮权重校正模块对宽松衣物序列至关重要。完整模型将PSNR从24.538提升至 **26.013**，并显著减少衣物撕裂伪影。该模块通过公式 $W' = W(n) + H_{skin}(T^{node})$ 在标准LBS蒙皮权重上叠加可学习校正，使模型能够个性化适应宽松衣物的变形模式。

### 定性分析与注意力可视化

**Figure 6** 展示了后训练对注意力图的语义净化效应：后训练模型的最后一层几何-图像token注意力图展现出更干净的语义对应关系，表明后训练阶段注入了更强的3D-2D对应先验。**Figure 5** 的定性对比显示，LCA在多视角和单视角设置下均生成更完整的几何结构和更清晰的面部细节，而基线方法在野外场景中常出现几何塌缩或纹理模糊。

### 泛化边界与失败模式

尽管LCA展现出强泛化能力（支持训练中未见过的眼镜、头饰、风格化角色，甚至零样本重光照），但存在以下明确局限：

1. **精细纹理重建不足**：刺绣、蕾丝等高频细节仍难以完美重建，可能受限于高斯表示的固有分辨率与感知损失的平滑效应。
2. **遮挡与运动模糊**：严重遮挡和快速运动模糊场景下重建质量下降，这是前馈方法的共性瓶颈——单次前向传播缺乏迭代优化机制来处理极端观测不确定性。
3. **次级运动缺失**：头发飘动、配饰摆动等次级运动动力学尚未建模，当前框架仅支持基于骨骼驱动的刚性变形。
4. **重光照的域限制**：重光照模块依赖后训练阶段的灯光阶段数据，在野外任意光照条件下的表现未经充分验证。

### 公平性说明

所有定量评估均基于前景分割掩码计算L1/LPIPS/PSNR，确保方法间比较公平。测试集同时覆盖多视角工作室和野外两类域，全面衡量泛化与保真度。多视角基线方法（如MV-LHM）由作者使用相同数据重新训练，避免训练协议差异引入偏差。

### 补充图表

![[assets/figures/papers/paper_list_l1067_https_arxiv_org_abs_2604_02320/figures/004_Table_2.jpg]]
*Table 2: Quantitative comparison with state-of-the-art 3D avatar methods. * denotes methods trained by us for multi-view inputs*

![[assets/figures/papers/paper_list_l1067_https_arxiv_org_abs_2604_02320/figures/007_Table_3.jpg]]
*Table 3: Effect of scaling pretraining data on downstream performance across data distributions*

![[assets/figures/papers/paper_list_l1067_https_arxiv_org_abs_2604_02320/figures/008_Figure_5.jpg]]
*Figure 5: Qualitative Comparison with State-of-the-Art Methods. LCA outperforms in both multi-view and monocular settings*

![[assets/figures/papers/paper_list_l1067_https_arxiv_org_abs_2604_02320/figures/011_Figure_7.jpg]]
*Figure 7: Loose Garment Support (LGS). (Left) Frontal view of the input condition. (Middle) Post-trained LCA avatar without loose garment support, while the general shape is recovered, skirts behave like pants when moving. (Right) LCA with loose garment support produces plausible animations without splitting garments*

![[assets/figures/papers/paper_list_l1067_https_arxiv_org_abs_2604_02320/figures/012_Table_S.1.jpg]]
*Table S.1: Ablation study on decoder architecture and posttraining learning rate decay. Our dual-branch residual design outperforms a single-branch variant. The learning rate decay is critical for preserving pretraining knowledge, with γ=0.00 (no decay) severely degrading studio performance*

![[assets/figures/papers/paper_list_l1067_https_arxiv_org_abs_2604_02320/figures/014_Table_S.2.jpg]]
*Table S.2: Effect of training data scale. Pre/post-training benefits persist even at 10× smaller scale (100K pretraining identities, 500 post-training identities), with consistent trends across both domains*

![[assets/figures/papers/paper_list_l1067_https_arxiv_org_abs_2604_02320/figures/015_Table_S.3.jpg]]
*Table S.3: Loose garment deformer ablation. Quantitative evaluation on loose-garment sequences. The full model with the deformer improves all metrics and reduces splitting artifacts*

![[assets/figures/papers/paper_list_l1067_https_arxiv_org_abs_2604_02320/figures/013_Figure_S.1.jpg]]
*Figure S.1: PCA of Geometric Token Features. Visualization of the feature space distributions produced by models trained with different strategies. Green points denote studio-captured subjects, while red points denote in-the-wild subjects*

![[assets/figures/papers/paper_list_l1067_https_arxiv_org_abs_2604_02320/figures/016_Figure_S.2.jpg]]
*Figure S.2: Qualitative Comparison with Alternative Paradigms. Comparison with Wan-Animate (2D video diffusion) and GUAVA (upper-body 3D Gaussian avatar)*



## 定位与知识库关联

### 1. 方法谱系：从单数据源混合训练到预训练-后训练范式

LCA的核心贡献在于将3D头像建模从“单一数据源混合训练”范式推进到“大规模预训练+高质量后训练”的两阶段范式。这一转变直接回应了领域的根本瓶颈：工作室捕捉数据（如多视角密集摄像）提供精确的3D几何监督但缺乏外观多样性，而野外单目视频覆盖广泛的衣着、环境与人体形态，却因视角稀疏导致几何模糊。传统方法试图将两类数据混合训练，但泛化能力与重建保真度不可兼得——混合训练在工作室测试集上仅达28.0 PSNR，野外测试集为28.0 PSNR（Table 1）。

LCA通过解耦泛化与保真度的学习阶段，打破了这一矛盾：
- **预训练阶段**：在百万级野外视频上学习通用的人体外观与几何先验，赋予模型强泛化能力；
- **后训练阶段**：在数千人的多视角工作室数据上注入精细的表情、手部驱动和多视角一致性控制，实现高保真度。

这一范式直接对标并超越了以下基线方法：

| 基线方法 | 方法类型 | LCA的优势 | 证据 |
|---------|---------|----------|------|
| **LHM** | 单视图前馈可驱动高斯头像 | 单视角设置下野外PSNR高出9.36 dB（27.685 vs 18.322） | Table 2(b) |
| **MV-LHM** | LHM的多视图扩展 | 多视角工作室PSNR高出3.56 dB（27.483 vs 23.925） | Table 2(a) |
| **ExAvatar** | 基于优化的高斯头像 | 野外多视角PSNR高出9.79 dB（27.802 vs 18.010） | Table 2(a) |
| **UP2You** | 单目驱动头像 | 定性比较中LCA展现出更完整的几何结构与纹理细节 | Figure 5 |
| **Wan-Animate** | 2D视频扩散方法 | LCA提供显式3D几何，支持自由视角渲染与重光照 | Figure S2 |
| **GUAVA** | 上半身3D高斯头像 | LCA覆盖全身驱动，包含手部与面部表情 | Figure S2 |

值得注意的是，LCA与优化类方法（如ExAvatar）的根本差异在于推理效率：LCA是前馈式方法，从少量图像生成头像仅需数秒，而优化方法需要逐样本迭代。同时，LCA的残差双分支架构（规范分支+姿态相关分支）使得驱动阶段仅需运行轻量的姿态解码器，进一步提升了实时动画效率。

### 2. 架构层面的关键创新定位

LCA在3D高斯头像管线中引入了三个关键架构改进，每个改进均有消融实验支撑：

**（1）残差双分支解码器**
传统方法使用单分支解码器同时预测规范属性与姿态相关变形，LCA将其解耦为规范高斯解码器 $H_{cano}$（预测静态身份属性）和姿态相关高斯解码器 $H_{pose}$（预测表情、注视、手部驱动的增量）。消融实验表明，双分支设计在工作室PSNR上从30.370提升至30.514，野外PSNR从27.936提升至28.175（Table S1）。

**（2）可学习双层节点蒙皮校正**
传统LBS（线性混合蒙皮）使用固定的蒙皮权重，无法处理宽松衣物的个性化变形。LCA引入双层节点变形器，通过可学习的蒙皮权重校正模块 $W' = W(n) + H_{skin}(T^{node})$ 实现衣物自然动画。该模块在宽松衣物序列上将PSNR从24.538提升至26.013（Table S3），且与ARAP正则化损失配合使用。

**（3）自监督面部表情潜在码**
传统方法仅使用身体姿态与表情基系数作为驱动信号。LCA额外引入自监督学习的面部表情潜在码和注视方向，构成更丰富的驱动向量 $(\theta, \varepsilon, \psi)$。这一设计使得模型能够捕捉更细腻的面部表情变化，尤其在野外数据中展现出更强的表现力。

### 3. 适用边界与局限性

LCA的能力边界受以下因素制约：

1. **精细纹理重建不足**：刺绣、蕾丝等高频纹理细节仍难以完美重建，这受限于高斯表示的表达能力与当前渲染分辨率。

2. **遮挡与运动模糊退化**：严重遮挡（如手部遮挡面部）和快速运动模糊场景下，图像token的质量下降，导致重建质量降低。这是所有基于图像特征提取方法的共性问题。

3. **次级运动缺失**：头发飘动、配饰摆动等次级运动动力学尚未建模。当前变形模块仅支持基于骨架驱动的刚性变形，无法模拟物理驱动的柔性运动。

4. **重光照的域限制**：重光照模块依赖后训练阶段的灯光阶段数据，在野外任意光照条件下的泛化能力尚未完全验证。该模块本质上是后训练阶段注入的特定能力，而非预训练阶段学到的通用先验。

5. **数据规模的边际收益**：预训练数据从10K扩展到1M视频持续带来收益（野外PSNR从27.67升至28.18，Table 3），但收益曲线是否已趋于饱和尚不明确。10×缩减规模下的实验（Pre-100K+Post-500，Table S2）表明范式具有鲁棒性，但绝对性能随数据量递减。

### 4. 开放问题与未来方向

LCA框架打开了以下研究方向：

1. **全身动态光照与服装物理**：能否将预/后训练范式推广到包含动态光照变化和更复杂服装物理（如褶皱模拟）的场景？当前重光照仅支持静态灯光条件。

2. **次级运动动力学整合**：如何有效整合头发物理、背包摆动等细粒度次级运动？这可能需要引入物理先验或时序建模模块。

3. **多模态驱动与实时渲染**：该框架是否适用于语音驱动、文本驱动的头像动画？更高分辨率（如4K）的实时渲染是否可通过级联细化模块实现？

4. **零样本风格化的内在机制**：LCA展现出对训练中未见过的眼镜、头饰、风格化角色的泛化能力（Figure 1/5/7），但这一零样本能力的来源尚不明确——是预训练数据的隐式覆盖，还是Transformer架构的归纳偏置？理解这一机制可能指导更高效的数据策展策略。

5. **后训练学习率衰减的敏感性**：消融实验表明后训练学习率衰减系数γ至关重要——γ=0.00（无衰减）时工作室PSNR骤降至27.464，而γ=0.65平衡最佳（Table S1）。这一超参数的敏感性是否意味着当前范式对后训练策略有较强依赖，能否通过更鲁棒的持续学习方法缓解？



## 原文 PDF

![[paperPDFs/CVPR_2026/Large_scale_Codec_Avatars_The_Unreasonable_Effectiveness_of_Large_scale_Avatar_Pretraining.pdf]]
