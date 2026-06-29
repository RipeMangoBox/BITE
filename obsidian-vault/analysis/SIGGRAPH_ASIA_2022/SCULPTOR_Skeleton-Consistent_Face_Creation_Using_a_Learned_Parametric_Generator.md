---
title: "SCULPTOR: Skeleton-Consistent Face Creation Using a Learned Parametric Generator"
type: paper
paper_level: A
venue: SIGGRAPH ASIA
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_ASIA_2022/SCULPTOR_Skeleton_Consistent_Face_Creation_Using_a_Learned_Parametric_Generator.pdf
project_link: null
code_link: null
aliases:
- SCULPTOR
tags:
- SIGGRAPH_ASIA_2022
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/benchmarks_datasets_evaluation
core_operator: SCULPTOR 引入的“trait”参数 γ，通过对手术引起的局部骨骼变化进行建模，实现了对下颌骨、颧骨等骨骼结构的独立控制，从而驱动面部特征的局部变化，如下巴形状、脸颊饱满度等。
primary_logic: 通过构建包含术前术后 CT 和 3D 面部扫描的 LUCY 数据集，SCULPTOR 将颅骨、面部几何和纹理联合建模，并在传统形状、姿态、表情融合变形的基础上增加特质融合变形（trait blendshape），在解剖约束下生成既真实又多变的数字人脸。
claims:
- SCULPTOR 通过联合学习 shape 和 trait 空间，能够准确捕捉手术带来的局部骨骼变化，重建出与术后 CT 一致的面部。
- 在颅骨拟合任务中，使用 72 个 trait 分量的 SCULPTOR 相比仅使用 144 个 shape 分量的 SCULPTOR‑SIMPLE，平均顶点均方误差从 2.01/2.04 mm（术前/术后）降至 1.77/1.77 mm。
- 在面部网格拟合任务中，SCULPTOR 在术前、术后 CT 数据和 FaceScape 数据集上均取得比 FLAME 更低的 RMSE（例如，FLAME 1.58 mm，SCULPTOR‑2 1.36 mm），证明了骨骼联合建模的优势。
- SCULPTOR 采用解剖学定义的下颌关节（髁突中点）代替从面部顶点回归的关节，提高了大姿态下表情的真实感。
---

# SCULPTOR: Skeleton-Consistent Face Creation Using a Learned Parametric Generator

> [!tip] 核心洞察
> 通过构建包含术前术后 CT 和 3D 面部扫描的 LUCY 数据集，SCULPTOR 将颅骨、面部几何和纹理联合建模，并在传统形状、姿态、表情融合变形的基础上增加特质融合变形（trait blendshape），在解剖约束下生成既真实又多变的数字人脸。

| 字段 | 内容 |
|------|------|
| 中文题名 | SCULPTOR：基于学习参数化生成器的骨骼一致性人脸创建 |
| 英文题名 | SCULPTOR: Skeleton-Consistent Face Creation Using a Learned Parametric Generator |
| 会议/期刊 | SIGGRAPH ASIA 2022 |
| Links | [paper](https://arxiv.org/abs/2209.06423) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/benchmarks_datasets_evaluation |
| Method | SCULPTOR |
| Dataset | Pre-surgery CT, Post-surgery CT, FaceScape, Skull fitting |

> [!tip] 效果简介
> - Pre-surgery CT (facial mesh fitting) 上，RMSE (mm) 1.36 (SCULPTOR-2) vs 1.58 (FLAME) (-0.22)。
> - Post-surgery CT (facial mesh fitting) 上，RMSE (mm) 1.41 (SCULPTOR-2) vs 1.60 (FLAME) (-0.19)。
> - FaceScape (facial mesh fitting) 上，RMSE (mm) 0.67 (SCULPTOR-2) vs 1.63 (FLAME) (-0.96)。

## 概要

现有参数化面部生成方法（如 FLAME）仅建模外部形状与纹理，忽视了内部颅骨结构与外观之间的生理关联，导致生成结果缺乏解剖一致性，也难以支持骨骼驱动的精细编辑。为此，本文提出 **SCULPTOR**——一种骨骼一致性参数化人脸生成器，在统一的数据驱动框架下联合建模颅骨、面部几何与纹理外观。其核心创新在于引入“特质（trait）”融合变形，专门捕捉由手术引起的局部骨骼变化，从而实现对下颌骨、颧骨等结构的独立控制。SCULPTOR 基于自建的 **LUCY** 数据集（包含术前术后 CT 与 3D 面部扫描）进行训练，并采用解剖学定义的下颌关节替代传统顶点回归关节。实验表明，SCULPTOR 在颅骨拟合与面部网格重建任务上均显著优于仅使用形状分量的简化版本及 FLAME，验证了骨骼联合建模的有效性。该方法在骨骼驱动编辑、考古颅骨面部复原、角色融合等应用中展现出更强的多样性与解剖合理性。

## 核心方法与创新机理

### 问题瓶颈与核心洞察

现有参数化人脸模型（如 FLAME）仅建模面部外部几何、姿态和表情，完全忽视了内部骨骼结构。这一根本缺陷导致两个关键问题：其一，生成的人脸缺乏解剖一致性，面部外形与骨骼支撑关系脱节；其二，模型无法支持骨骼驱动的局部特征编辑（如下颌角宽度、颧骨突出度等），因为这些特征变化本质上源于骨骼形态差异。SCULPTOR 的核心洞察在于：**将颅骨、面部几何和纹理纳入统一的数据驱动框架进行联合建模**，并在传统形状、姿态、表情融合变形的基础上，引入专门捕捉局部骨骼变化的“特质”（trait）融合变形，从而在解剖约束下生成既真实又富有个体特征的人脸。

### 模型整体架构

SCULPTOR 将参数化人脸定义为一个包含几何和外观的联合模型：

$$\mathcal { M } ( \theta , \beta , \gamma , \phi , \alpha ) = \{ \mathcal { G } ( \theta , \beta , \gamma , \phi ) , \mathcal { A } ( \alpha ) \}$$

其中 $\theta$ 为姿态参数，$\beta$ 为形状参数，$\gamma$ 为特质参数（核心创新），$\phi$ 为表情参数，$\alpha$ 为外观参数。几何函数 $\mathcal{G}$ 通过线性混合蒙皮（LBS）计算变形后的网格：

$$\mathcal { G } ( \beta , \gamma , \theta , \phi ) = L B S ( \mathcal { W } , J _ { p } ( \beta , \gamma ) , \operatorname { T } _ { p } ( \beta , \gamma , \theta , \phi ) )$$

### 关键 Changed Slot 1：引入骨骼几何表示

与 FLAME 仅包含面部外部网格不同，SCULPTOR 的模板网格 $\overline{\mathbf{T}}$ 同时包含颅骨（上颌骨、下颌骨）和面部外部表面。这一改变使得模型能够显式建模骨骼与面部外形的空间对应关系，为后续的特质编辑和骨骼一致性约束提供几何基础。

### 关键 Changed Slot 2：特质融合变形（Trait Blendshape）

这是 SCULPTOR 最核心的创新。个性化模板 $\mathbf{T}_p$ 由四类融合变形合成：

$${ \bf T } _ { p } ( \beta , \gamma , \theta , \phi ) = \overline { { \bf T } } + { \cal B } _ { S } ( \beta ; S ) + { \cal B } _ { D } ( \gamma ; \mathcal { D } ) + { \cal B } _ { P } ( \theta ; \mathcal { P } ) + { \cal B } _ { E } ( \phi ; \mathcal { E } )$$

其中 ${ \cal B } _ { D } ( \gamma ; \mathcal { D } ) = \mathcal { D } \gamma$ 即为新增的特质融合变形。与建模全局形状变化的形状分量 $B_S$ 不同，特质分量 $B_D$ 专门捕捉手术带来的**局部骨骼变化**——包括下颌骨截骨前移/后退、颧骨截骨移位、上颌骨牙槽突修整等。这些手术仅改变特定骨骼区域的形态，而特质分量通过 LUCY 数据集中术前术后的配对 CT 数据学习到这种局部变化的低维流形。在生成或编辑时，调节 $\gamma$ 参数即可独立控制下颌角宽度、颧骨突出度等骨骼特征，同时保持面部其他区域不变（见 Fig. 5）。

![[assets/figures/papers/paper_list_l84_https_arxiv_org_abs_2209_06423/figures/006_Figure_5.jpg]]
*Figure 5: Performance of skeleton-driven characteristic face editing on one female (top row) and one male (bottom row) actors’ faces using the trait space in SCULPTOR. Each row of the partial enlargement displays the characteristic facial variations according to a representative trait component*

### 关键 Changed Slot 3：解剖学下颌关节定义

传统方法从面部网格顶点回归关节位置，缺乏解剖依据。SCULPTOR 将下颌关节 $J_p$ 定义为下颌骨髁突中点，通过模板骨骼顶点加上形状和特质变形后确定：

$$J _ { \mathcal { P } } ( \boldsymbol { \beta } , \boldsymbol { \gamma } ) { = } \mathcal { T } ( \overline { { \mathbf { T } } } + B _ { S } ( \boldsymbol { \beta } ; \boldsymbol { S } ) + B _ { D } ( \boldsymbol { \gamma } ; \mathcal { D } ) )$$

其中 $\mathcal{T}$ 是从模板骨骼顶点到关节位置的预定义拓扑映射。这一设计使得大张口等极端姿态下的面部变形更符合解剖学约束，避免了顶点回归关节在极端表情下产生的不自然形变（Fig. 5 提供定性证据）。

### 训练数据与配准流程

SCULPTOR 依赖 LUCY 数据集，包含整形手术患者术前和术后的 CT 扫描及 3DMD 面部扫描。配准流程分两步：

**颅骨配准**采用嵌入变形（embedded deformation）方法，通过控制节点和径向基函数权重将通用颅骨模板变形到目标 CT 分割的骨骼表面。配准能量为：

$$E _ { r s k u l l } = E _ { d } + \lambda _ { l } E _ { l m k } + \lambda _ { r } E _ { r e g }$$

其中稠密对齐项 $E_d$ 结合 Chamfer 距离和法向角度惩罚：

$$E _ { d } = \lambda _ { d } C D ( \overline { { \mathbf { T } } } _ { s } ^ { \prime } , \mathbf { C } _ { s } ) + \big ( 1 - \lambda _ { d } \big ) C D _ { n } ( \overline { { \mathbf { T } } } _ { s } ^ { \prime } , \mathbf { C } _ { s } )$$

$E_{lmk}$ 约束 29 个骨骼 landmarks（由整形外科医生标注，见 Fig. 3a）对齐，$E_{reg}$ 为刚性正则项防止过度扭曲。

**面部配准**将外部面部模板配准到 3DMD 扫描，能量函数为：

$$E _ { r f a c e } = E _ { d } ( \overline { { \mathbf { T } } } _ { f } , \mathbf { C } _ { f } ) + \lambda _ { l } E _ { l m k } + \lambda _ { l a p } E _ { l a p }$$

其中 $E_{lap}$ 为离散拉普拉斯平滑项，保证变形后的面部网格保持局部几何结构。

### 参数学习与训练路径

SCULPTOR 采用交替优化策略在两个数据集上学习所有参数：

**LUCY 数据集上的优化目标**用于学习形状、姿态和表情参数：

$$E _ { L } ( \theta _ { i } , \phi _ { i } , \mathbf { T } _ { p } ^ { i } ) = \lambda _ { v e r t } E _ { v e r t } + \lambda _ { e d g e } E _ { e d g e } + \lambda _ { l a p } E _ { l a p } + \lambda _ { s r e g } E _ { s r e g }$$

其中 $E_{vert}$ 约束变形后网格与配准目标的顶点距离，$E_{edge}$ 保持边长度一致，形状正则项 $E _ { s r e g } = | | \mathbf { T } _ { p f } ^ { i } \tilde { S } ^ { T } | | ^ { 2 }$ 约束外部表面模板保持在初始形状空间内，防止过拟合到噪声。

**FaceScape 数据集上的优化目标**用于学习形状、特质参数以及蒙皮权重和姿态融合变形：

$$E _ { F } ( \beta _ { i } , \theta _ { i } , \gamma _ { i } , \mathcal { W } , \mathcal { P } ) = E _ { v e r t } + \lambda _ { c o l } E _ { c o l } + E _ { \dot { p } r e g }$$

其中 $E_{col}$ 为碰撞惩罚项（防止下颌穿透上颌），参数正则项包含所有可学参数的 L2 或 Frobenius 正则：

$$E _ { p r e g } = \lambda _ { \beta } E _ { \beta } + \lambda _ { \gamma } E _ { \gamma } + \lambda _ { \tilde { W } } E _ { \tilde { W } } + \lambda _ { p } E _ { p }$$

**外观建模**在 UV 空间中进行：将配准后的面部网格通过预定义 UV 映射展开为纹理图像，然后在纹理图像上应用 PCA 学习外观空间 $\mathcal{A}(\alpha)$，生成具有真实肤色变化的面部纹理（Fig. 6）。

### 生成与推理路径

训练完成后，SCULPTOR 的生成流程（Fig. 4）为：从通用模板出发，依次叠加形状分量（全局面部特征）、特质分量（局部骨骼特征）、外观纹理、姿态和表情变形，最终通过环境贴图渲染。在推理阶段（如从单张 RGB 图像重建面部），通过优化形状 $\beta$ 和特质 $\gamma$ 参数最小化重投影误差，同时利用解剖约束（如关节位置合理性、骨骼-面部距离一致性）确保重建结果的物理合理性。

![[assets/figures/papers/paper_list_l84_https_arxiv_org_abs_2209_06423/figures/005_Figure_4.jpg]]
*Figure 4: Our realistic face generation pipeline with trait effect. Starting with SCULPTOR full template, we randomly generate and procedurally add shape, trait, appearance and expression/pose effects on the neutral template, rendering the 3D face with environment maps*

### 因果链路总结

LUCY 数据集的术前术后配对 CT → 特质融合变形学习 → 局部骨骼变化的低维参数化 → 骨骼驱动的独立编辑能力；解剖学关节定义 → 大姿态下真实的下颌运动；颅骨-面部联合模板 → 骨骼与面部外形的空间一致性约束 → 重建和生成结果的解剖合理性。这一因果链路使得 SCULPTOR 在面部拟合精度（Table 3）和骨骼编辑能力（Fig. 5）上均显著优于仅建模外部形状的传统方法。

![[assets/figures/papers/paper_list_l84_https_arxiv_org_abs_2209_06423/figures/007_Figure_6.jpg]]
*Figure 6: Examples of randomly generated facial appearance variations of SCULPTOR on a male and a female face respectively*

## 实验与关键发现

SCULPTOR 的实验验证围绕三个核心问题展开：骨骼建模是否提升了面部拟合精度？trait 分量的引入是否必要？模型在下游应用中是否展现出解剖一致性的优势？以下从主结果、消融分析和应用边界三个层面进行提炼。

### 面部网格拟合：骨骼联合建模带来一致的精度提升

Table 3 报告了 SCULPTOR 与 FLAME 在多个测试集上的面部网格拟合 RMSE。为保证公平，FLAME 使用 300 个形状分量，SCULPTOR‑1 同样使用 300 个形状分量，SCULPTOR‑2 则使用 228 个形状分量加 72 个 trait 分量，总参数量相当。在术前 CT 数据上，FLAME 的 RMSE 为 1.58 mm，SCULPTOR‑2 降至 1.36 mm（降低 0.22 mm）；在术后 CT 数据上，FLAME 为 1.60 mm，SCULPTOR‑2 为 1.41 mm（降低 0.19 mm）。在 FaceScape 数据集上差距最为显著：FLAME 为 1.63 mm，SCULPTOR‑2 仅为 0.67 mm（降低 0.96 mm）。Fig. 8 的逐顶点误差可视化进一步显示，SCULPTOR‑2 的误差分布更为均匀，尤其在颧骨和下颌区域没有出现 FLAME 常见的误差集中现象。

这一结果的因果链路清晰：FLAME 仅建模外部表面形状，当面部外观受内部骨骼结构支配时（如术后骨骼位移导致的面部形态变化），其纯表面驱动的形状空间无法有效解释这类变异。SCULPTOR 通过联合学习颅骨与面部几何，使形状空间隐含了骨骼约束，从而在骨骼结构发生显著变化的术后数据上保持了拟合精度。FaceScape 上的大幅领先则表明，即使在非手术人群中，骨骼-面部的联合先验也比纯表面先验具有更强的泛化能力。

### 颅骨拟合消融：trait 分量是捕捉局部骨骼变化的关键

Table 2 的颅骨拟合实验直接验证了 trait 分量的必要性。SCULPTOR‑SIMPLE（仅使用 144 个 shape 分量，无 trait）在术前 CT 上的平均顶点 MSE 为 2.01 mm，术后为 2.04 mm；而引入 72 个 trait 分量后，SCULPTOR 将误差分别降至 1.77 mm 和 1.77 mm，降幅约 13%。值得注意的是，术后数据的误差改善更为明显——这正是 trait 空间的设计初衷：手术主要改变下颌骨、颧骨和上颌骨牙槽突的局部形态，而 trait 分量正是针对这类局部骨骼变化进行建模的。shape 空间虽然维度更高，但其主成分倾向于捕捉全局的头型变异（如头骨整体大小、长宽比），难以有效表达手术带来的局部骨骼位移。

![[assets/figures/papers/paper_list_l84_https_arxiv_org_abs_2209_06423/figures/009_Table_2.jpg]]
*Table 2: Quantitative results for skull fitting performance. We evaluate Mean Squared Errors in millimeter on pre- and post-surgery test scans. SCULPTOR-SIMPLE stands for the simplified version which only models shape, while SCULPTOR models both shape and trait components*

Table 4 的下颌骨/上颌骨缺失重建实验进一步证实了这一能力。在缺失下颌骨的条件下，SCULPTOR‑2 的 Hausdorff 距离为 2.259 mm，优于 SCULPTOR‑1 的 2.668 mm（降低 0.409 mm）。这表明 trait 空间学到的骨骼先验可以在部分观测条件下进行合理的骨骼补全。

![[assets/figures/papers/paper_list_l84_https_arxiv_org_abs_2209_06423/figures/012_Table_4.jpg]]
*Table 4: Quantitative reconstruction results in missing mandible or maxilla tasks. We report hausdorff distance in millimeters*

### 解剖学关节定义的定性收益

Fig. 5 展示了大开口等极端姿态下的表情真实感对比。SCULPTOR 采用解剖学定义的下颌关节（髁突中点），而非从面部顶点回归关节位置。这一设计的因果效应在于：当嘴巴大幅张开时，面部顶点回归的关节位置会因软组织变形而产生偏移，导致下颌旋转中心错误，进而使下巴区域的皮肤变形失真。解剖学关节定义直接锚定在颅骨的物理旋转中心上，从根本上消除了这一误差源。该实验为定性展示，定量指标需进一步验证，但其解剖学依据可靠。

### 外观建模与生成多样性

Fig. 6 展示了 SCULPTOR 在 UV 空间通过 PCA 学习的外观模型所生成的肤色变化。该模型能够产生自然的肤色过渡和个体差异，但需注意其仅建模了基础肤色分布，未对皱纹、毛孔等高频皮肤细节进行参数化——这是当前方法的明确边界。

### 局限性与适用边界

实验揭示了以下关键边界条件：

1. **骨骼形状分布的局限性**：LUCY 数据集仅来自正颌手术患者，骨骼变异集中于下颌骨、颧骨和上颌骨牙槽突。trait 分量的变形无法覆盖头盖骨等其他骨骼部位的自然个体差异，这意味着 SCULPTOR 在颅顶形态变异较大的群体中可能表现不足。

2. **软组织建模的缺失**：当前模型使用线性混合蒙皮和表情融合变形，未包含肌肉、脂肪等软组织的物理建模。在极端表情或面部挤压场景下，皮肤变形可能缺乏物理真实感。

3. **外观细节的简化**：PCA 外观模型仅捕捉低频肤色变化，无法生成皮肤微观结构。对于需要高质量纹理的应用（如电影级数字人），需要额外的细节生成步骤。

4. **数据驱动的泛化风险**：尽管 FaceScape 测试集上的优异表现证明了跨数据集的泛化能力，但 LUCY 的样本量和人口统计学覆盖范围有限，模型在非手术人群中的骨骼推断精度仍需更大规模验证。

![[assets/figures/papers/paper_list_l84_https_arxiv_org_abs_2209_06423/figures/010_Figure_9.jpg]]
*Figure 9: Archaeological Skeletal Facial Completion. (a) The original maxilla of Ava and face was generated using SCULPTOR without trait components. Rendered skull image from Open Virtual World (Sketchfab). (b)-(d) Characteristic face generations with respect to Ava’s maxilla by varying trait parameters in SCULPTOR*

## 定位与知识库关联

SCULPTOR 在参数化人脸模型的知识谱系中占据一个独特位置：它首次将**颅骨几何**与**面部外部形状、纹理**纳入统一的统计建模框架，从而填补了现有模型在“骨骼‑外观解剖一致性”上的空白。要理解这一贡献，需要明确它相对于基线改变了哪些关键 slot，以及这些改变在知识库中的挂载点。

**相对于 FLAME 的核心 slot 变更。** 论文以 FLAME 作为定量对比的主要基线，SCULPTOR 在四个维度上对其进行了结构性扩展：

1. **几何表示空间**：FLAME 仅建模面部外部表面网格；SCULPTOR 将表示空间扩展为包含上颌骨（maxilla）和下颌骨（mandible）的颅骨网格与面部外部网格的联合体。这一变更使得模型能够显式表达骨骼结构对软组织形态的约束。
2. **融合变形组件**：FLAME 使用 shape、pose、expression 三类融合变形；SCULPTOR 新增第四类——**特质融合变形（trait blendshape）** $B_D(\gamma; \mathcal{D})$，专门建模由手术引起的局部骨骼变化（如下颌角切除、颧骨内推），从而将“骨骼驱动的局部特征编辑”从形状空间中解耦出来。
3. **关节定义方式**：FLAME 从面部网格顶点回归得到下颌关节位置；SCULPTOR 改用解剖学定义——由外科医生标注的下颌髁突中点，通过模板拓扑 $\mathcal{T}$ 从变形后的颅骨顶点直接确定 $J_p(\beta, \gamma)$。这使大开口等极端姿态下的变形更符合解剖约束。
4. **训练数据**：FLAME 基于 4D 面部扫描（如 D3DFACS）；SCULPTOR 构建了 **LUCY 数据集**，包含术前术后的配对 CT 扫描与 3DMD 面部扫描，为骨骼‑形状‑纹理联合学习提供了监督信号。

**在知识库中的挂载点。** SCULPTOR 的方法论直接继承自人体/手部参数化建模的经典范式——SMPL（Loper et al., SIGGRAPH Asia 2015）和 MANO（Romero et al., TOG 2017）所确立的“模板网格 + 线性混合蒙皮 + 融合变形”框架。论文明确指出其网格配准和模型学习流程“analogous to techniques used on exterior faces, hands, and even full body shapes”。SCULPTOR 的创新在于将这一范式从单一表面扩展到了“内部骨骼 + 外部表面”的层级结构，并在融合变形体系中引入了面向手术变化的 trait 分量。这一思路可视为对 FLAME 的“解剖深度补全”：FLAME 解决了面部表情和姿态的参数化，SCULPTOR 则补齐了骨骼形状与面部特征之间的因果关系建模。

**适用边界与限制。** 需要清醒认识到 SCULPTOR 的适用范围受限于 LUCY 数据集的分布特性：该数据集全部来自正颌手术患者，骨骼变化主要集中在颧骨、下颌骨和上颌牙槽突区域。因此，trait 空间的表达能力天然偏向于这些手术涉及部位的特征变化（如脸颊饱满度、下巴宽度），而无法覆盖头盖骨等其他骨骼区域的天然个体差异。此外，模型的外观部分仅基于 PCA 对基础肤色进行建模，未参数化皱纹、毛孔等高频细节；软组织模拟仍依赖线性混合蒙皮和表情融合变形，缺乏肌肉层面的物理建模。这些限制意味着 SCULPTOR 当前更适合作为“骨骼一致的人脸生成与编辑引擎”，而非完整的解剖‑物理模拟器。

**后续研究启发。** SCULPTOR 为若干方向打开了知识接口：（1）**数据增强与泛化**——如何将现有的大规模面部扫描数据集（如 FaceScape）与 LUCY 的骨骼‑形状关联进行跨域迁移，以丰富 trait 空间的覆盖范围；（2）**软组织物理建模**——能否引入动态 MRI 或 4D CT 数据，将肌肉、脂肪等软组织的形变纳入参数化，构建“颅骨‑肌肉‑外表皮”三层联合模型；（3）**语义解耦编辑**——trait 分量目前通过 PCA 学习，能否通过无监督或自监督方法发现更具语义的编辑方向（如“增加下颌角宽度”而非抽象的主成分）；（4）**下游任务集成**——将 SCULPTOR 的解剖约束引入单视图人脸重建或实时表演捕捉管线，可提升注册结果的物理合理性，避免出现骨骼穿透等伪影。

**证据强度评估。** 论文通过消融实验（Table 2）有力地证明了 trait 分量的必要性：移除 trait 后（SCULPTOR-SIMPLE），颅骨拟合误差上升约 13%（术前 MSE 从 1.77 mm 升至 2.01 mm，术后从 1.77 mm 升至 2.04 mm）。面部拟合实验中，SCULPTOR-2 在 FaceScape 数据集上将 FLAME 的 RMSE 从 1.63 mm 降至 0.67 mm，降幅达 59%，这一显著提升部分归因于骨骼‑形状联合建模带来的更强表达能力，但也需注意 FaceScape 本身不包含骨骼真值，该指标反映的是面部表面的拟合精度而非骨骼推理的直接验证。考古学颅骨补全（Fig. 9）和角色融合（Fig. 10）等应用案例虽具视觉说服力，但缺乏系统性的用户研究或量化评估，其结论强度应视为探索性而非确证性。

## 原文 PDF

![[paperPDFs/SIGGRAPH_ASIA_2022/SCULPTOR_Skeleton_Consistent_Face_Creation_Using_a_Learned_Parametric_Generator.pdf]]