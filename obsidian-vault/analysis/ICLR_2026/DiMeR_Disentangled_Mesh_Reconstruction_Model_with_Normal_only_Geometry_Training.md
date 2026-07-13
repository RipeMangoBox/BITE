---
title: "DiMeR: Disentangled Mesh Reconstruction Model with Normal-only Geometry Training"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/DiMeR_Disentangled_Mesh_Reconstruction_Model_with_Normal_only_Geometry_Training_a5d58f656555.pdf
project_link: null
code_link: null
aliases:
- DiMeR
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/representation_self_supervised_transfer
core_operator: 将几何预测与纹理解耦，仅以法线图作为几何分支输入，并引入3D GT SDF监督和物理渲染（PBR）期望损失。
primary_logic: 法线图编码了纯粹的表面朝向信息，与几何具有一一映射关系，消除了外观歧义，使得几何学习任务简化且有效；结合高效的网格提取改进和物理渲染约束，可显著提升重建精度。
claims:
- 仅使用法线图作为几何输入将CD从0.041降至0.028，F1从0.981升至0.992
- 去除FlexiCubes的变形和权重MLP几乎不影响性能，但减少约2.5倍计算开销和1.5倍显存
- 引入PBR期望损失和3D SDF正则化后CD从0.039/0.037降至0.028
- GSO 上 CD (↓) = 0.028 (DiMeR GT)
---

# DiMeR: Disentangled Mesh Reconstruction Model with Normal-only Geometry Training

> [!tip] 核心洞察
> 法线图编码了纯粹的表面朝向信息，与几何具有一一映射关系，消除了外观歧义，使得几何学习任务简化且有效；结合高效的网格提取改进和物理渲染约束，可显著提升重建精度。

| 字段 | 内容 |
|------|------|
| 中文题名 | DiMeR：基于仅法线几何训练的解耦网格重建模型 |
| 英文题名 | DiMeR: Disentangled Mesh Reconstruction Model with Normal-only Geometry Training |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=fK2pCgoavb) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/representation_self_supervised_transfer |
| Method | DiMeR |
| Dataset | GSO, OmniObject3D |

> [!tip] 效果简介
> - GSO 上，CD (↓) 0.028 (DiMeR GT) vs 0.041 (PRM) (31.7% ↓)；F1 (↑) 0.992 vs 0.977 (+0.015)；PSNR (↑) 23.40 vs 21.68 (+1.72)。
> - OmniObject3D 上，CD (↓) 0.024 (DiMeR GT) vs 0.034 (PRM) (29.4% ↓)。
> - GSO (single-image-to-3D) 上，CD (↓) 0.052 (DiMeR) vs 0.059 (PRM) (11.9% ↓)。

## 概要

从单张或多张 RGB 图像重建三维网格面临一个根本性瓶颈：**纹理与几何的耦合**。同一张 RGB 图像可能对应多种几何-纹理组合，导致训练目标冲突，网络倾向于收敛到模糊的平均解。此外，主流方法中常用的网格提取组件（如 FlexiCubes）存在冗余计算且缺乏三维监督，进一步限制了重建精度。

DiMeR 提出了一条解耦路径来解决上述问题。其核心洞察是：**法线图编码了纯粹的表面朝向信息，与几何具有一一映射关系，从而消除了外观歧义**。基于此，DiMeR 将几何预测与纹理解耦为两个独立分支——几何分支仅以法线图作为输入，纹理分支以 RGB 图像作为输入。几何分支进一步引入三维 GT SDF 监督、Eikonal 正则化以及基于物理渲染（PBR）的高光/漫反射期望损失，并精简了 FlexiCubes 中不必要的变形和权重 MLP。

这一设计带来了显著的性能提升：在 GSO 数据集上，仅使用法线图作为几何输入将 Chamfer Distance (CD) 从 0.041 降至 0.028，F1 从 0.981 升至 0.992；去除 FlexiCubes 的变形和权重 MLP 几乎不影响性能，但减少了约 2.5 倍计算开销和 1.5 倍显存；引入 PBR 期望损失和 3D SDF 正则化后，CD 进一步从约 0.039 降至 0.028。

DiMeR 在稀疏视图重建和单图像到三维任务上均取得了领先性能，但其重建质量依赖于外部法线预测模型的精度，且目前仅针对目标级重建，无法处理场景级输入。

### 问题背景

从图像或文本生成高质量三维网格是计算机视觉与图形学领域的核心挑战之一。现有方法通常将几何重建与纹理预测统一建模，以RGB图像作为输入，直接从外观信号推断三维形状。然而，这种统一范式存在一个根本性的瓶颈：**纹理与几何的耦合导致训练目标冲突**。

如图 Figure 2 所示，同一RGB外观可以由多种几何-纹理组合产生——例如，一个真实的球体配以复杂的纹理，与一个凹凸不平的几何体配以简单的纹理，在渲染后可能呈现几乎相同的图像。这种外观歧义性使得网络在学习过程中面临一个混合解空间，其中包含多个可行的几何-纹理配对。当训练数据中存在这种“冲突的输入-真值对”时，网络倾向于收敛到一个平均解，导致几何精度显著下降。

### 现有方法缺口

当前主流的稀疏视图或单图像到3D方法，如 **InstantMesh** (Xu et al., 2024a)、**PRM** (Ge et al., 2024)、**CRM** (Wang et al., 2025) 和 **MeshLRM** (Wei et al., 2024)，均采用统一预测几何和纹理的范式。这些方法在以下方面存在明显不足：

1. **几何-纹理耦合**：网络被迫从RGB信号中同时推断几何和纹理，而RGB信号本身无法唯一确定几何形状，导致几何学习不充分且不稳定。
2. **网格提取冗余**：常用网格提取组件（如FlexiCubes）包含变形MLP和权重MLP，这些模块增加了计算开销和显存占用，但对几何精度的贡献有限。
3. **缺乏3D监督**：现有方法主要依赖2D渲染损失（如RGB、法线、深度、掩码损失）进行监督，缺少直接的3D几何约束（如SDF监督），导致训练不稳定且几何细节丢失。

### 本文动机

针对上述问题，DiMeR提出了一种**解耦的网格重建框架**，核心动机包括：

- **消除外观歧义**：法线图编码了纯粹的表面朝向信息，与几何具有一一映射关系，不受纹理干扰。因此，仅以法线图作为几何分支的输入，可以将混合解空间拆分为两个独立的子空间，使几何学习任务简化且有效。
- **精简网格提取**：去除FlexiCubes中冗余的变形和权重MLP，在保持几何精度的同时显著降低计算开销。
- **引入3D正则化与物理渲染约束**：通过3D GT SDF监督、Eikonal损失以及基于物理渲染（PBR）的高光和漫反射期望损失，为几何分支提供更直接、更稳定的训练信号。

通过上述设计，DiMeR旨在从根本上解决几何-纹理耦合导致的训练冲突问题，显著提升网格重建的几何精度与稳定性。

## 核心方法与创新机理

DiMeR 的核心创新在于**将几何与纹理的学习过程彻底解耦**，以消除传统 RGB 图像输入带来的几何‑外观歧义。这一设计围绕三个关键“改变点”（changed slots）展开：几何分支的输入格式、网格提取组件的精简，以及几何监督信号的重构。

### 1. 几何分支输入：从 RGB 到仅法线图

现有稀疏视图网格重建方法（如 **InstantMesh** (Xu et al., 2024a)、**PRM** (Ge et al., 2024)）通常以 RGB 图像或 RGB‑法线混合作为几何分支的输入。然而，RGB 图像同时编码了几何、材质和光照信息，导致**一个外观对应多种几何‑纹理组合**，网络在训练时被迫收敛到模糊的平均解（图 2）。

DiMeR 将几何分支的输入**替换为仅法线图**。法线图只编码表面朝向，与几何存在一一映射关系，从而消除了外观歧义。这一改变的效果极为显著：消融实验（Table 3）表明，仅用法线输入将 Chamfer Distance 从 0.041（RGB+法线）降至 0.028，F1 从 0.981 提升至 0.992。该结论在 Table 13 的详细消融中得到进一步验证，纯 RGB 输入的 CD 高达 0.043，进一步证实了 RGB 信号对几何学习的干扰。

### 2. 网格提取组件：精简 FlexiCubes

基线方法普遍采用 FlexiCubes 进行等值面提取，其包含**变形 MLP** 和**权重 MLP** 两个可学习模块，旨在微调顶点位置和面片拓扑。DiMeR 发现这两个 MLP 在具备强 3D 监督的条件下是冗余的——移除它们后 CD 和 F1 几乎不变（Table 5：CD 0.045 vs 0.045，F1 0.963 vs 0.964），但 GPU 显存占用和推理时间显著降低（约 2.5 倍计算开销和 1.5 倍显存减少，Table 14）。这一精简使得 DiMeR 能够将 SDF 网格分辨率从 128 提升至 192，从而获取更精细的几何细节（Table 6）。

### 3. 几何监督信号：3D 正则化与 PBR 期望损失

传统方法依赖 FlexiCubes 自带的局部平滑正则化，缺乏对 SDF 场的直接 3D 约束。DiMeR 引入了两项关键监督改进：

- **3D SDF 正则化**：包括 Eikonal 损失（$$\mathcal{L}_{eik} = \mathbb{E}_{\pmb{x}} ( \| \nabla_{\pmb{x}} \mathrm{SDF}(\pmb{x}) \|_2 - 1 )^2$$，Eq.1）和 GT SDF 监督（$$\mathscr{L}_{sdf} = \| \mathrm{SDF}(\pmb{v}) - \mathrm{SDF}_{\mathrm{GT}}(\pmb{v}) \|_2^2$$，Eq.2），直接约束 SDF 场的梯度模长和顶点处的符号距离值。
- **PBR 期望损失**：在随机环境光、材质和粗糙度下渲染预测网格与真值网格的高光图（$$\mathcal{L}_{spec}$$，Eq.3）和漫反射图（$$\mathcal{L}_{diff}$$，Eq.4），计算 MSE 和 LPIPS 的统计期望。这为几何分支提供了物理渲染层面的间接监督，使预测网格在多种光照条件下均与真值保持一致。

消融实验（Table 4）显示，引入上述监督后 CD 从 0.039/0.037 降至 0.028，验证了 3D 正则化和 PBR 期望损失的叠加增益。

### 4. 分支解耦架构

上述改变统一于**解耦的双分支架构**（图 3）：几何分支以法线图和相机嵌入为输入，经 ViT 编码器和 Triplane 解码器生成 SDF 网格，再由精简的 FlexiCubes 提取网格；纹理分支以 RGB 图像为输入，独立预测纹理 Triplane 特征，并通过坐标投影和采样（Eq.9‑10）将纹理映射到几何网格表面，最终由 RGB 解码器生成纹理图像（Eq.11）。两个分支分别由几何损失（Eq.8）和纹理损失（Eq.12）独立监督，彻底避免了训练目标的冲突。

**需要手动验证的内容**：PBR 期望损失中环境光和材质的随机采样策略的具体参数范围、以及其对真实世界多样性的覆盖程度，在现有分析证据中未充分展开，建议查阅原文 Sec 3.1 的补充细节。

DiMeR 的核心设计是将网格重建任务**解耦为几何分支与纹理分支**，从根本上切断 RGB 外观与三维形状之间的模糊耦合。如图 3 所示，框架的上半部分为几何分支，**仅接收法线图作为输入**；下半部分为纹理分支，接收 RGB 图像作为输入。两个分支独立训练，分别由几何专用损失和外观专用损失监督，最终在网格顶点级别通过坐标投影实现纹理映射。

### 几何分支

几何分支的目标是从法线图中恢复精确的三维网格。其处理流程为：

1. **Normal Encoder（ViT）**：将输入的法线图与相机嵌入编码为 patch 特征。
2. **Triplane Decoder（Transformer）**：聚合 patch 特征，生成 Triplane 几何表示。
3. **SDF Grid Extraction**：从 Triplane 查询 SDF 值，构建三维 SDF 网格。
4. **Adapted FlexiCubes**：从 SDF 网格中提取等值面，得到网格顶点和面片。与标准 FlexiCubes 不同，DiMeR **移除了变形 MLP 和权重 MLP**，在几乎不影响几何精度（CD 和 F1 基本持平）的前提下，将计算开销降低约 2.5 倍、GPU 显存占用降低约 1.5 倍（Table 5, Table 14）。

几何分支的监督信号完全排除了 RGB 渲染项，转而采用以下损失函数组合（Eq. 1–8）：

- **Eikonal 损失**（Eq. 1）：约束 SDF 梯度模长为 1，保证符号距离场的物理合理性；
- **3D GT SDF 损失**（Eq. 2）：在网格顶点处直接监督 SDF 值与真值的一致性；
- **PBR 期望损失**（Eq. 3–4）：在随机采样的环境光、材质和粗糙度条件下，分别对高光图（Specular）和漫反射图（Diffuse）施加 MSE + LPIPS 损失，从物理渲染层面约束几何；
- **法线、深度、掩码损失**（Eq. 5–7）：分别监督法线图、深度图和二值掩码的预测精度。

总几何损失为上述各项之和（Eq. 8）。

### 纹理分支

纹理分支独立于几何分支运行，其输入为 RGB 图像，输出为纹理映射：

1. **Image Encoder（ViT）**：将 RGB 图像与相机嵌入编码为纹理 patch 特征。
2. **Triplane Decoder（Texture）**：生成纹理 Triplane 特征。
3. **Coordinate Rasterization & Sampling**（Eq. 9–10）：将几何分支输出的网格顶点通过相机投影到图像坐标，在纹理 Triplane 上采样对应特征。
4. **RGB Decoder**（Eq. 11）：解码采样到的纹理特征为 RGB 图像。

纹理分支的损失函数（Eq. 12）为 RGB 图像的 MSE 损失与 LPIPS 感知损失之和。

### 输入输出流与解耦逻辑

整个框架的信息流严格单向：**几何分支仅依赖法线图，纹理分支仅依赖 RGB 图**。这一设计的核心动机在于：法线图编码了纯粹的局部表面朝向信息，与几何之间存在一一映射关系，从而消除了 RGB 图像中“同一外观对应多种几何-纹理组合”的歧义性（Figure 2）。解耦后的两个分支各自收敛到明确的解空间，避免了统一预测时网络趋向平均解的瓶颈。

在推理阶段，若输入为 RGB 图像，系统需先通过外部法线预测模型（如 Lotus 或 StableNormal）估计法线图，再分别送入两个分支；若已有真值法线图，则可直接获得最优几何精度（CD 从 0.041 降至 0.028，F1 从 0.981 升至 0.992，见 Table 3）。

![[assets/figures/papers/paper_list_l72_https_openreview_net_forum_id_fK2pCgoavb/figures/003_Figure_3.jpg]]
*Figure 3: The framework of our DiMeR. The upper part is the geometry branch, and exclusively uses normal maps as input. The lower part is the texture branch*

DiMeR 的核心设计在于将几何重建与纹理生成解耦为两个独立分支，并通过精心设计的损失函数与精简的网格提取模块，消除外观歧义对几何学习的干扰。

### 几何分支

几何分支**仅以法线图作为输入**，从根本上切断 RGB 外观与几何之间的模糊耦合。如图 3 上部所示，该分支由以下模块串联构成：

- **Normal Encoder (ViT)**：将输入的法线图与相机嵌入编码为 patch 特征。
- **Triplane Decoder (Transformer)**：聚合 patch 特征，生成几何 Triplane 表示。
- **SDF Grid Extraction**：从 Triplane 查询 SDF 值，构建三维 SDF 网格。
- **精简版 FlexiCubes**：从 SDF 网格中提取等值面，直接输出网格顶点与面片。**关键改动**：移除了原始 FlexiCubes 中的变形 MLP 和权重 MLP。消融实验（Table 5、Table 14）表明，去除这两个组件几乎不影响 CD 和 F1 指标，但可减少约 2.5 倍计算开销和 1.5 倍显存占用。

几何分支的监督信号完全来自几何一致性损失，不包含任何 RGB 渲染项，避免了外观歧义对几何的反向传播干扰。

### 纹理分支

纹理分支以 RGB 图像为输入，在几何分支提供的网格顶点坐标上查询纹理特征，流程如下：

- **Image Encoder (ViT)**：将 RGB 图像与相机嵌入编码为纹理 patch 特征。
- **Triplane Decoder (Texture)**：生成纹理 Triplane 特征 $\mathcal{F}_c$。
- **坐标光栅化与采样**：将几何网格顶点 $v$ 经相机投影至图像坐标，再在 Triplane 上采样特征：
  $$Coord_{\mathcal{T}} = \mathrm{Rast}(v, \mathrm{Camera}) \tag{9}$$
  $$\mathcal{F}_{\mathcal{T}} = \mathrm{Sample}(Coord_{\mathcal{T}}, \mathcal{F}_c) \tag{10}$$
- **RGB Decoder**：将采样到的纹理特征解码为 RGB 图像：
  $$\hat{\mathcal{T}} = \mathrm{RGB\_Decoder}(\mathcal{F}_{\mathcal{T}}) \tag{11}$$

### 关键损失函数

几何分支的总损失 $\mathcal{L}_g$ 由七项构成（Eq. 8），其中四项为核心创新：

**1. Eikonal 正则化损失（Eq. 1）**
$$\mathcal{L}_{eik} = \mathbb{E}_{\pmb{x}} ( \| \nabla_{\pmb{x}} \mathrm{SDF}(\pmb{x}) \|_2 - 1 )^2, \quad \pmb{x} \sim \mathrm{Uniform}(-1,1)$$
约束 SDF 梯度模长为 1，确保 SDF 场的物理合理性。

**2. 3D GT SDF 监督损失（Eq. 2）**
$$\mathcal{L}_{sdf} = \| \mathrm{SDF}(\pmb{v}) - \mathrm{SDF}_{\mathrm{GT}}(\pmb{v}) \|_2^2$$
在网格顶点 $\pmb{v}$ 处直接监督 SDF 值与真值一致。**消融实验（Table 4）表明，引入 Eikonal 损失和 SDF 损失后，CD 从 0.039 降至 0.028。**

**3. PBR 期望损失（Eq. 3–4）**

这是 DiMeR 最具特色的监督信号。在随机采样的环境光 $e$、材质 $m$ 和粗糙度 $r$ 下，分别渲染预测网格 $\hat{\mathcal{O}}$ 与真值网格 $\mathcal{O}$ 的高光图 $\mathrm{Spec}$ 和漫反射图 $\mathrm{Diff}$，并计算 MSE 与 LPIPS 的组合损失：

$$\mathcal{L}_{spec} = \mathbb{E}_{e,m,r} [(\mathrm{Spec}(\hat{\mathcal{O}}, e, m, r) - \mathrm{Spec}(\mathcal{O}, e, m, r))^2 + \mathrm{LPIPS}(\dots)] \tag{3}$$
$$\mathcal{L}_{diff} = \mathbb{E}_{e,m,r} [(\mathrm{Diff}(\hat{\mathcal{O}}, e, m, r) - \mathrm{Diff}(\mathcal{O}, e, m, r))^2 + \mathrm{LPIPS}(\dots)] \tag{4}$$

该损失通过统计期望的方式，在多样化光照和材质条件下对齐预测网格与真值网格的物理渲染结果，提供了强几何约束。**Table 4 消融实验证实，加入 PBR 期望损失后，CD 从 0.037 进一步降至 0.028。**

**4. 辅助几何损失（Eq. 5–7）**

- **法线损失**：$\mathcal{L}_{nor} = \mathcal{M}_{\mathrm{GT}} \otimes (1 - \hat{\mathcal{N}} \cdot \mathcal{N}_{\mathrm{GT}})$，监督渲染法线与真值法线的一致性。
- **深度损失**：$\mathcal{L}_{dep} = \mathcal{M}_{\mathrm{GT}} \otimes |\hat{\mathcal{D}} - \mathcal{D}_{\mathrm{GT}}|$，MAE 形式的深度监督。
- **掩码损失**：$\mathcal{L}_{mask} = (\hat{\mathcal{M}} - \mathcal{M}_{\mathrm{GT}})^2$，二值掩码的 MSE 损失。

几何分支总损失为上述各项之和：
$$\mathcal{L}_g = \mathcal{L}_{eik} + \mathcal{L}_{sdf} + \mathcal{L}_{spec} + \mathcal{L}_{diff} + \mathcal{L}_{nor} + \mathcal{L}_{dep} + \mathcal{L}_{mask} \tag{8}$$

**5. 纹理损失（Eq. 12）**
$$\mathcal{L}_t = (\hat{\mathcal{T}} - \mathcal{T}_{\mathrm{GT}})^2 + \mathrm{LPIPS}(\hat{\mathcal{T}}, \mathcal{T}_{\mathrm{GT}})$$
纹理分支采用 RGB 的 MSE 损失与 LPIPS 感知损失的组合进行监督。

## 实验与关键发现

### 一、核心定量结果

DiMeR 在稀疏视图重建和单图像到三维两个任务上均取得了最优的几何精度，同时在纹理质量上也具备竞争力。

**稀疏视图重建（Table 1）**：在 GSO 和 OmniObject3D 两个标准基准上，DiMeR 均显著超越此前的 SOTA 方法 **PRM**（Ge et al., 2024）。使用真值法线图作为输入时，DiMeR (GT) 在 GSO 上的 Chamfer Distance (CD) 低至 **0.028**，较 PRM 的 0.041 降低 **31.7%**；F1 分数从 0.977 提升至 **0.992**。在 OmniObject3D 上，CD 从 0.034 降至 **0.024**，降幅达 **29.4%**。当使用预测法线图（Lotus 或 StableNormal）时，DiMeR 仍保持明显优势：DiMeR (SN) 在 GSO 上 CD 为 0.032，优于 PRM 的 0.041。纹理质量方面，DiMeR 的 PSNR 达到 23.40，高于 PRM 的 21.68。

**单图像到三维（Table 2）**：DiMeR 与 Stable-Zero123++ 和 StableNormal 组合后，在 GSO 上的 CD 为 **0.052**，优于 PRM 的 0.059（降幅 11.9%），F1 从 0.961 提升至 **0.981**，在 **CRM**（Wang et al., 2025）和 **MeshLRM**（Wei et al., 2024）等单图方法中同样表现最优。

> **公平性说明**：DiMeR 在评估时若使用预测法线，其输入与基准方法完全一致（均为 RGB 图像），确保了对比的公平性。法线预测模型的选择对结果有一定影响，但论文通过评估多种法线模型（Lotus、StableNormal）展示了方法的鲁棒性（Table 9）。

![[assets/figures/papers/paper_list_l72_https_openreview_net_forum_id_fK2pCgoavb/figures/012_Table_9.jpg]]
*Table 9: Quantitative results for reconstruction task with different normal predictors. CD means Chamfer Distance. Error is the angle between predicted normal vectors and gt normal vectors*

### 二、关键设计消融

DiMeR 的性能增益来源于三个核心设计选择：仅法线几何输入、精简的网格提取、以及增强的几何监督。

#### 2.1 仅法线输入消除几何歧义（Table 3）

![[assets/figures/papers/paper_list_l72_https_openreview_net_forum_id_fK2pCgoavb/figures/008_Table_3.jpg]]
*Table 3: The ablation studies of different input and output formats*

这是 DiMeR 最关键的因果旋钮。实验对比了三种输入格式：

- **RGB → Geometry**：CD 为 0.043，F1 为 0.977
- **RGB + Normal → Geometry**：CD 为 0.041，F1 为 0.981
- **Only Normal → Geometry (DiMeR)**：CD 降至 **0.028**，F1 升至 **0.992**

仅使用法线图作为几何分支输入，将 CD 从 0.041 大幅压缩至 0.028。这一结果直接验证了论文的核心洞察：RGB 图像中外观与几何的耦合导致训练目标冲突，网络收敛到多种几何-纹理组合的平均解；而法线图编码了纯粹的表面朝向信息，与几何具有一一映射关系，从根本上消除了外观歧义。

#### 2.2 精简 FlexiCubes 降低开销（Table 5）

![[assets/figures/papers/paper_list_l72_https_openreview_net_forum_id_fK2pCgoavb/figures/011_Table_5.jpg]]
*Table 5: The ablation studies of the effectiveness of Deformation and Weight MLP. GPU Mem is training occupancy*

标准 FlexiCubes 包含变形 MLP 和权重 MLP 两个可学习组件。DiMeR 将其移除后发现：

- CD 和 F1 **几乎不受影响**（CD 0.045 vs 0.045，F1 0.963 vs 0.964）
- 训练 GPU 显存占用显著降低，计算开销减少约 **2.5 倍**，显存减少约 **1.5 倍**（Table 14）

这表明在 DiMeR 的框架下，FlexiCubes 的变形和权重网络是冗余的——仅法线输入和增强的 3D 监督已经足够约束网格提取过程。

#### 2.3 3D 正则化与 PBR 期望损失（Table 4）

![[assets/figures/papers/paper_list_l72_https_openreview_net_forum_id_fK2pCgoavb/figures/009_Table_4.jpg]]
*Table 4: The ablation studies of 3D regularization and PBR expectation*

逐步添加几何监督组件，CD 从基础配置的 0.039/0.037 逐步降至 0.028：

- **+3D Regularization**（Eikonal 损失 + GT SDF 损失）：替代 FlexiCubes 原有的正则化损失，提供显式的 SDF 梯度约束和顶点级 SDF 监督
- **+PBR Expectation**（specular + diffuse 期望损失）：在随机环境光和材质参数下渲染高光和漫反射光图，与真值网格的渲染结果计算 MSE + LPIPS 损失

这两个组件共同作用，使得几何分支在没有 RGB 渲染损失的情况下仍能获得精确的 3D 监督信号。

#### 2.4 其他消融发现

- **SDF 网格分辨率**（Table 6）：将分辨率从 128 提升至 192 可进一步改善性能，说明更高的空间分辨率有助于捕捉几何细节。
- **法线噪声鲁棒性**（Table 11）：训练时向法线图注入高斯噪声（标准差 0.02），可将预测法线下的 CD 从 0.036 降至 0.032，提升了对实际法线预测误差的容忍度。
- **法线源选择**（Table 9, Table 10）：不同法线预测模型（Lotus、StableNormal）对最终重建精度有影响，但 DiMeR 在所有法线源下均优于 PRM，且使用更准确的 StableNormal 时 CD 可达 0.032。

![[assets/figures/papers/paper_list_l72_https_openreview_net_forum_id_fK2pCgoavb/figures/014_Table_6.jpg]]
*Table 6: Experiments about grid resolutions*

### 三、定性结果

**稀疏视图重建**（Figure 5）：DiMeR 重建的网格在细节保留和几何完整性上明显优于 PRM 和 InstantMesh，尤其在薄结构和高曲率区域。

**单图像到三维**（Figure 6）：与 CRM、MeshLRM 等方法相比，DiMeR 生成的网格具有更清晰的几何边界和更准确的拓扑结构。

### 四、失败模式与局限性

论文明确指出了一个失败案例（Figure 9）：DiMeR 目前仅针对**目标级重建**设计，无法处理场景级输入（背景为白色）。当输入包含复杂背景或多物体场景时，方法会失效。

此外，方法的性能依赖于外部法线预测模型的精度。尽管已展示对噪声的鲁棒性，但法线预测误差仍会导致几何精度下降（CD 约上升 0.004，Table 9）。训练计算资源需求较高（几何分支需 2 天 × 8 H100），对于稀疏视图任务需要多视角输入，不能直接从单张 RGB 图像端到端重建（但可与现有多视图生成方法组合使用）。

## 定位与知识库关联

### 1. 问题定位与核心瓶颈

DiMeR 试图解决的核心问题是**稀疏视图网格重建中纹理与几何的耦合**。在现有方法中，几何与纹理通常共享同一 RGB 输入，并在统一的损失函数下联合优化。然而，如 Figure 2 所示，单张 RGB 图像在几何-纹理联合解空间中允许大量等价解——不同的几何与纹理组合可以产生几乎相同的外观。这种歧义性导致两个后果：

1. **训练目标冲突**：数据集中存在“输入-GT”不一致的配对（Figure 2b），网络被迫收敛到平均解，几何精度受损。
2. **监督信号混杂**：RGB 渲染损失同时惩罚几何误差和纹理误差，无法为几何分支提供纯净的梯度。

DiMeR 的解决策略是将联合解空间**解耦**为两个独立子空间（Figure 2c）：几何分支仅以法线图作为输入，纹理分支以 RGB 图像作为输入，各自使用专属的监督信号。

### 2. 与基线方法的关系

#### 2.1 稀疏视图网格重建基线

DiMeR 直接对比的稀疏视图重建方法包括：

- **InstantMesh**（Xu et al., 2024a）：采用统一编码器处理多视图 RGB 输入，联合预测几何与纹理。
- **PRM**（Ge et al., 2024）：同样使用 RGB 多视图输入，通过 FlexiCubes 提取网格。

DiMeR 与上述方法的**关键设计差异**在于输入模态的解耦。PRM 和 InstantMesh 的几何分支接收 RGB 或 RGB+法线混合输入，而 DiMeR 的几何分支**仅接收法线图**。这一改变在 GSO 数据集上将 CD 从 PRM 的 0.041 降至 0.028（使用 GT 法线），降幅达 31.7%（Table 1）。即使使用预测法线（Lotus 或 StableNormal），CD 仍降至 0.032，显著优于所有 RGB 输入基线。

#### 2.2 单图像到 3D 基线

在单图像到 3D 任务中，DiMeR 与以下方法对比：

- **CRM**（Wang et al., 2025）：单图像到 3D 的端到端方法。
- **MeshLRM**（Wei et al., 2024）：基于大型重建模型的单图网格生成方法。

DiMeR 在此任务中并非端到端方案，而是与 Stable-Zero123++ 和 StableNormal 组合使用（Figure 4 中部流程）。Table 2 显示，DiMeR 在 GSO 上将 CD 从 PRM 的 0.059 降至 0.052，F1 从 0.961 提升至 0.981。需要注意的是，此场景下 DiMeR 的优势部分受限于外部法线预测模型的精度。

#### 2.3 网格提取组件的简化

DiMeR 继承了 FlexiCubes 的等值面提取框架，但**移除了变形 MLP 和权重 MLP**。Table 5 的消融实验表明，移除这两个模块后 CD 和 F1 几乎不变（w/o: 0.045/0.963 vs w/: 0.045/0.964），但 GPU 显存占用和推理时间显著降低。这一发现表明，在具备强 3D 监督（SDF GT + Eikonal 损失）的条件下，FlexiCubes 的变形能力是冗余的。

### 3. 方法谱系中的位置

从方法谱系角度看，DiMeR 位于以下几条研究线的交汇处：

| 研究线 | 代表工作 | DiMeR 的继承与改进 |
|--------|----------|---------------------|
| 稀疏视图网格重建 | PRM, InstantMesh | 继承 Triplane + FlexiCubes 架构，但解耦几何/纹理输入 |
| 法线驱动的 3D 重建 | — | 首次将法线图作为几何分支的**唯一**输入模态 |
| 物理渲染监督 | — | 引入 PBR 期望损失（Eq.3-4）作为几何分支的额外约束 |
| 3D 表示学习 | FlexiCubes | 简化变形/权重 MLP，证明强 3D 监督下可省略 |

DiMeR 的核心贡献不是提出全新的网络架构，而是**重新设计了输入-监督的耦合关系**。这一设计选择使得几何学习任务从“推断几何+纹理的联合分布”简化为“从法线推断 SDF”，消除了外观歧义带来的优化困难。

### 4. 适用边界与局限

DiMeR 的适用边界由以下因素界定：

1. **目标级重建限定**：DiMeR 仅针对白色背景下的单个物体重建，无法处理场景级输入。Figure 9 展示了一个场景级输入的失败案例，模型无法正确解析复杂背景中的几何结构。

2. **对外部法线预测模型的依赖**：在实际部署中（使用预测法线而非 GT 法线），DiMeR 的重建质量受限于法线预测模型的精度。Table 9 显示，不同法线预测器的角度误差会导致 CD 约 0.004 的波动。论文通过在训练时注入高斯噪声（Table 11）提升了鲁棒性，但无法完全消除这一依赖。

3. **计算资源需求**：几何分支训练需要 2 天 × 8 H100 GPU，这限制了其在资源受限场景下的可复现性。

4. **多视图需求**：稀疏视图重建任务需要 4-6 个视角的输入，不能直接从单张图像重建（需与 Zero123++ 等新视图合成方法组合）。

### 5. 开放问题

基于 DiMeR 的设计选择和实验结论，以下问题值得进一步探索：

- **更轻量的法线预测方案**：能否通过联合训练法线预测器和几何分支来减少对外部模型的依赖？或者，是否存在比法线图更紧凑的几何表示（如曲率图、深度边缘图）可以达到类似效果？

- **场景级扩展**：DiMeR 的解耦策略是否可以通过引入深度图作为额外几何线索来扩展到室内场景？场景级重建面临的遮挡和尺度变化问题需要新的架构设计。

- **PBR 期望损失的泛化性**：Eq.3-4 中的环境光和材质随机采样是否足够覆盖真实世界的多样性？在材质复杂（如半透明、次表面散射）的物体上，当前的 PBR 简化模型可能不足。

- **更少视图下的表现**：论文主要评估了 4-6 视图的重建质量，在 2-3 个视图的极端稀疏场景下，法线图的歧义性是否仍能保持低水平？这需要进一步实验验证。

- **非刚性物体与动态场景**：DiMeR 假设物体几何是静态的，法线图与 SDF 的一一映射关系在非刚性变形下是否仍然成立？这关系到方法向可变形物体重建的推广可能性。

## 原文 PDF

![[paperPDFs/ICLR_2026/DiMeR_Disentangled_Mesh_Reconstruction_Model_with_Normal_only_Geometry_Training_a5d58f656555.pdf]]
