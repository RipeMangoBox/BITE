---
title: "Lafite: A Generative Latent Field for 3D Native Texturing"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Lafite_A_Generative_Latent_Field_for_3D_Native_Texturing.pdf
project_link: null
code_link: null
aliases:
- Lafite
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 通过VAE从密集采样点云中学习稀疏潜在颜色场，将纹理表示为连续的3D隐式函数；生成时利用同一编码器从单色点云提取几何潜在，为流匹配模型提供精确对齐的3D几何条件。
primary_logic: 强大的3D纹理生成必须建立在强大的3D表示之上。直接将纹理编码为连续的稀疏潜在场，既避免了2D投影带来的信息损失和矛盾，又通过共享编码器提取无遮挡的纯几何信息，实现了表示与条件的优雅协同设计。
claims:
- VAE重建PSNR在128^3体素分辨率下达到34.62 dB，超越TRELLIS基线（23.07 dB）超过11.5 dB，表明表示高保真度。
- 在图像/文本条件纹理生成中，LaFiTe在无光照和有光照渲染下的FD_CLIP、KD_DINO等指标上达到最优或次优（Table 1），且视觉上无接缝、更一致。
- VAE重建质量随输入点云密度增加而持续提升（128分辨率下从20K点的26.07 PSNR到4M点的34.45 PSNR），验证了表示的可扩展性。
- 3D原生方法在自遮挡区域保持纹理完整，而投影方法出现明显瑕疵（Figure 3）。
---

# Lafite: A Generative Latent Field for 3D Native Texturing

> [!tip] 核心洞察
> 强大的3D纹理生成必须建立在强大的3D表示之上。直接将纹理编码为连续的稀疏潜在场，既避免了2D投影带来的信息损失和矛盾，又通过共享编码器提取无遮挡的纯几何信息，实现了表示与条件的优雅协同设计。

| 字段 | 内容 |
|------|------|
| 中文题名 | LaFiTe：一种用于3D原生纹理生成的生成式潜在场 |
| 英文题名 | Lafite: A Generative Latent Field for 3D Native Texturing |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.04786) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | LaFiTe |
| Dataset | VAE Reconstruction, Image-conditioned generation |

> [!tip] 效果简介
> - VAE Reconstruction (128^3 resolution) 上，PSNR 34.62 vs 23.07 (TRELLIS-RF128*) (+11.55 dB)；SSIM 0.934 vs 0.798 (TRELLIS-RF128*) (+0.136)。
> - Image-conditioned generation (unshaded) 上，FD_CLIP competitive/best vs baseline range (qualitative advantage)。

## 概要

### 1. 问题背景与核心瓶颈

3D内容创作中，为给定的几何体生成高质量、无缝且一致的纹理是一个长期存在的挑战。现有方法主要沿两条路径展开：**多视角投影方法**将纹理生成转化为2D渲染图像的生成与反投影，但不可避免地引入视图间不一致、接缝以及自遮挡区域的纹理缺失；**UV空间生成方法**直接在参数化的2D纹理图上操作，却面临UV展开带来的扭曲变形和网格拓扑依赖问题。

这些困境指向一个根本瓶颈：**缺乏一种强大、紧凑且与网格拓扑无关的3D纹理原生表示**。该表示需要同时满足三个苛刻要求——捕获高频细节、保持全局无缝一致性、适配生成模型的潜在空间约束。

### 2. LaFiTe的核心思想

LaFiTe（Latent Field for Texturing）提出了一种3D原生纹理生成框架，其核心洞察是：**强大的3D纹理生成必须建立在强大的3D表示之上**。具体而言，LaFiTe将纹理建模为一种**稀疏潜在颜色场**——一个从网格表面密集采样的彩色点云中学习到的连续3D隐式函数。这一表示选择带来了三重优势：

- **避免投影信息损失**：直接在3D空间编码纹理，消除了2D投影带来的信息压缩和视图矛盾。
- **拓扑无关的紧凑性**：采用稀疏体素结构，仅存储物体表面附近的活跃体素，兼顾了表达能力和计算效率。
- **表示与条件的协同设计**：通过共享VAE编码器，从单色点云（所有颜色设为白色）中提取纯几何潜在，为生成模型提供精确对齐的3D几何条件，无需额外的条件编码器。

### 3. 方法定位与知识库定位

在3D纹理生成的方法谱系中，LaFiTe占据了一个独特的位置：

| 方法类别 | 代表方法 | 核心表示 | 主要局限 |
|---------|---------|---------|---------|
| 多视角投影 | MVPaint | 2D渲染图像 | 视图不一致、自遮挡失效 |
| UV空间生成 | TexGen | UV纹理图 | 变形、拓扑依赖 |
| 隐式3D表示 | **TRELLIS** (Xiang et al., CVPR 2025) | 投影图像特征的体素网格 | 仍依赖2D投影，信息损失 |
| **3D原生潜在场** | **LaFiTe（本文）** | **直接从彩色点云学习的稀疏潜在颜色场** | 训练数据规模受限 |

与最接近的隐式3D方法TRELLIS相比，LaFiTe的关键区别在于**输入模态的根本转变**：TRELLIS使用从多视角渲染图像中提取的投影特征作为体素网格的输入，本质上仍受投影信息损失的制约；LaFiTe则直接从网格表面采样的彩色点云中学习，实现了对纹理的无偏3D原生编码。这一区别在VAE重建保真度上体现为超过11.5 dB PSNR的显著提升。

在生成模型层面，LaFiTe采用**条件整流流（Rectified Flow）**作为生成范式，以几何潜在为条件，从噪声中恢复纹理潜在向量。这种选择在保持生成质量的同时提供了一条从几何到纹理的确定性映射路径，相较于扩散模型具有更高效的采样特性。

### 4. 主要结果概览

LaFiTe在多个维度上验证了其表示和生成框架的有效性：

**表示保真度**：在128³体素分辨率下，VAE重建PSNR达到34.62 dB，相比TRELLIS基线（23.07 dB）提升超过11.5 dB；SSIM从0.798提升至0.934（Table 2）。这一差距在视觉上表现为LaFiTe重建的纹理更清晰、细节更丰富，避免了TRELLIS的模糊和伪影（Figure 4）。

**生成质量**：在图像/文本条件纹理生成任务中，LaFiTe在FD_CLIP、KD_DINO等指标上达到最优或次优水平（Table 1），且生成的纹理在视觉上无接缝、与参考图像和几何体的一致性更强（Figure 5）。

**自遮挡鲁棒性**：3D原生表示使LaFiTe在高度自遮挡区域仍能生成完整且连贯的纹理，而投影方法在这些区域出现明显的纹理缺失或错误（Figure 3）。

**可扩展性**：VAE重建质量随输入点云密度增加而持续提升——从20K点的PSNR 26.07到4M点的PSNR 34.45（Table 3），验证了该表示能够从更密集的表面采样中获益，具备良好的可扩展性。

### 5. 局限与开放问题

尽管LaFiTe在3D原生纹理表示上取得了显著进展，仍存在若干局限：

- **数据瓶颈**：训练依赖高质量3D资产，而此类数据的规模远不及2D图像/视频数据，限制了模型对稀有风格的泛化能力。
- **2D先验缺失**：未有效利用大规模2D生成先验（如预训练的扩散模型），导致文本语义理解和文字纹理生成仍有不足。
- **采样密度敏感性**：若输入网格的表面采样点密度不足，重建质量会明显下降，需要用户或自动流程确保足够的采样。

这些局限指向三个开放的探索方向：（1）如何将大规模2D生成先验融入3D原生纹理生成，以提升语义合理性和文本渲染质量；（2）能否利用大规模2D图像/视频数据缓解高质量纹理3D训练数据的稀缺性；（3）该表示是否可以扩展到更复杂的全局光照效果或体纹理，而不仅是表面颜色。



### 3D纹理生成的现状与瓶颈

随着3D内容创作在游戏、影视、虚拟现实和工业设计中的广泛应用，自动化纹理生成成为3D生成式AI的核心任务之一。当前，主流3D资产生成平台（如Tripo AI 、Rodin 、Meshy AI 、Hunyuan3D 等）已能产出高质量的几何体，但纹理生成仍面临根本性挑战。

现有3D纹理生成方法主要沿两条技术路线展开：**基于多视角投影的方法**和**基于UV空间的方法**。前者将纹理生成转化为2D图像生成问题，通过对3D模型的多视角渲染图像进行纹理合成，再投影回模型表面。然而，这一范式存在固有缺陷——不同视角生成的纹理之间缺乏一致性约束，导致视图间出现接缝和风格断裂；在自遮挡区域，投影方法因无法获取有效观测而生成错误或缺失的纹理（Figure 3）。后者在UV参数化空间进行纹理生成，虽然避免了多视角不一致问题，但UV展开不可避免引入几何拉伸和变形，且难以保持纹理在不同UV图块边界处的连续性。

### 根本瓶颈：3D纹理表示能力的缺失

上述问题的根源在于**缺乏一种强大、紧凑且与网格拓扑无关的3D纹理表示**。理想的纹理表示应同时满足三个要求：① 能够无偏地捕获高频外观细节；② 在几何表面全局保持一致、无接缝；③ 结构紧凑，适合作为生成模型的潜在空间。现有表示均无法同时满足这些条件——投影方法将纹理信息分散在多个2D视图中，丢失了3D连贯性；UV空间表示则受限于参数化质量，且对网格拓扑敏感。

TRELLIS（Xiang et al., CVPR 2025）等近期工作尝试通过体素表示学习3D纹理，但其编码器使用投影图像特征作为输入，重建保真度有限（PSNR仅23.07 dB，Table 2），且生成的纹理存在模糊和伪影（Figure 4）。这表明，**强大的3D纹理生成必须建立在强大的3D表示之上**——表示本身必须直接从3D数据中学习，而非通过2D代理间接构建。

### LaFiTe的核心思路

针对上述瓶颈，LaFiTe提出了一种根本性的范式转变：**将3D纹理建模为连续的稀疏潜在颜色场**。具体而言，该方法从网格表面密集采样彩色点云（包含位置、法向和颜色），通过一个专门设计的变分自编码器（VAE）将其编码为结构化的稀疏潜在向量，解码时则可查询任意表面点的RGB颜色。这一表示天然具有3D原生性——不依赖2D投影，不对网格拓扑做任何假设，且在3D空间中保持全局一致。

更重要的是，该表示实现了**表示与条件的优雅协同设计**：生成纹理时，仅需将输入点云的全部颜色设为白色（形成单色点云），通过同一VAE编码器即可提取不含外观信息的纯几何潜在，作为生成模型的条件。这种统一的几何条件编码方式避免了独立几何编码器可能引入的表示空间不对齐问题，为后续的流匹配生成模型提供了精确的3D几何约束。



## 核心方法与创新机理

LaFiTe的核心创新在于对3D纹理生成的根本性反思：**将纹理从2D投影或UV展开的“平面”范式，彻底转向3D原生表示**。这一转变并非简单的输入形式替换，而是围绕“强大的3D纹理生成必须建立在强大的3D表示之上”这一洞察，对表示、编码、条件和监督四个维度进行了协同重构。

### 从2D投影到3D点云的表示跃迁

现有方法（如**MVPaint**、**TexGen**）依赖多视角渲染图像或UV展开图作为纹理表示，本质上是在2D空间处理3D问题。这带来了两类根本性缺陷：一是多视角投影间的视图不一致导致接缝；二是UV展开引入的几何变形破坏了纹理的局部连续性。LaFiTe直接以**从网格表面均匀采样的彩色点云**（含位置$p_i$、法向$n_i$、颜色$c_i$）作为输入，在3D空间原生地捕获纹理信息。这一表示选择消除了投影带来的信息损失和矛盾，也为后续的编码器设计提供了无偏的几何上下文。

### 点-体素注意力：从平均池化到结构化聚合

传统点云编码方法（如PointNet池化）通过简单的平均或最大池化将点特征聚合为全局或局部特征，无法有效保留高频细节。LaFiTe设计了**点-体素注意力机制**，分两步实现精细的特征提取：

1. **体素内自注意力**（Eq. 1）：对同一体素内的点进行自注意力操作，使每个点的特征能够感知邻域点的几何与外观信息，得到增强的点特征$\widetilde{x}_i$：
   $$\widetilde{x}_i = \sum_{j=1}^{n} \mathrm{softmax}\big(\frac{Q_{x_i} K_{x_j}^T}{\sqrt{d}}\big) \cdot V_{x_j}$$

2. **点-体素交叉注意力**（Eq. 2）：利用可学习的体素查询向量，从增强后的点特征集合中聚合出最终的体素纹理特征$\widetilde{v}_k$：
   $$\widetilde{v}_k = \sum_{i=1}^{n} \mathrm{softmax}\big(\frac{Q_{v_k} K_{\widetilde{x}_i}^T}{\sqrt{d}}\big) \cdot V_{\widetilde{x}_i}$$

这一设计替代了PointNet的简单池化，显著改善了对局部细节的捕捉能力（Figure 4）。与使用投影图像特征的**TRELLIS**（Xiang et al., CVPR 2025）相比，LaFiTe在128³体素分辨率下的VAE重建PSNR达到34.62 dB，领先超过11.5 dB（Table 2），直接验证了3D原生编码相对于2D投影编码的表示优势。

### 共享编码器的几何条件解耦

纹理生成的核心挑战之一是如何为生成模型提供精确的几何条件。传统方法或使用独立的几何编码器，或将几何信息隐式地混入2D投影中。LaFiTe的解决方案是**共享VAE编码器，通过输入单色点云（所有颜色设为白色）提取纯几何潜在$z_{\mathrm{geo}}$**。这一设计的精妙之处在于：同一编码器对彩色点云提取纹理潜在、对单色点云提取几何潜在，两者天然处于对齐的潜在空间中，无需额外的对齐模块。这种“表示与条件的优雅协同设计”使得后续的流匹配生成模型（Eq. 6）能够在几何条件与纹理目标之间建立精确的映射关系。

### 3D空间直接监督：告别渲染损失

传统纹理生成方法通常依赖基于渲染的损失（如LPIPS、SSIM），即先渲染纹理到2D图像再计算损失。这种间接监督引入了渲染管线的不确定性，且无法保证3D空间中的纹理一致性。LaFiTe直接在3D空间使用**L1颜色重建损失**（Eq. 5），在点云层面比较预测颜色与真实颜色的差异。这一监督方式的转变，配合VAE的KL散度正则化，迫使模型学习紧凑且高保真的纹理潜在空间，而非仅追求特定视角下的渲染效果。

### 创新协同的因果链条

上述四项创新并非孤立存在，而是形成了紧密的因果链条：3D点云表示消除了投影/UV变形带来的信息损失→点-体素注意力高效地从点云中提取结构化特征→共享编码器在统一空间中解耦几何与纹理→3D直接监督确保潜在空间忠实于真实纹理。这一链条的终端效果体现在Table 3的消融实验中：随着输入点云密度从20K增至4M，VAE重建PSNR从26.07 dB持续提升至34.45 dB，证明表示本身具备良好的可扩展性，能够从更密集的采样中持续获益。



LaFiTe 的核心设计理念是将 3D 纹理建模为一种**稀疏潜在颜色场**（sparse latent color field），通过一个 VAE 自编码器从数据中学习这一紧凑表示，并以此为基础构建生成模型。整个框架分为两大阶段：**表示学习**与**条件生成**，如图 Figure 2 所示。

![[assets/figures/papers/paper_list_l2530_https_arxiv_org_abs_2512_04786/figures/002_Figure_2.jpg]]
*Figure 2: The LaFiTe Pipeline. (Top) A VAE autoencoder learns a sparse latent color field representation by encoding a colored point cloud sampled from the mesh surface. (Bottom) For generation, the VAE encoder first extracts a geometry latent from a monochrome point cloud. This geometry latent then conditions a rectified flow model to synthesize a texture latent, which is decoded to the 3D texture*

### 表示学习：稀疏潜在颜色场的 VAE

该阶段的目标是从任意带纹理的 3D 网格中提取一个连续、紧凑且与拓扑无关的纹理表示。

**输入**：从网格表面密集采样的彩色点云 $\mathcal{P} = \{x_i = (p_i, n_i, c_i)\}$，其中 $p_i$ 为三维坐标，$n_i$ 为法向量，$c_i$ 为 RGB 颜色。

**编码流程**：
1. **体素化与分组**：将 3D 空间离散为稀疏体素网格，仅保留物体表面附近的活跃体素，将点云按空间位置分组到各体素内。
2. **点-体素注意力编码**：对每个体素内的点执行**体素内自注意力**（Eq. 1），使各点的几何与外观特征相互增强；随后通过**点-体素交叉注意力**（Eq. 2），利用可学习的体素查询向量将增强后的点特征聚合为体素级纹理特征。
3. **稀疏 VAE 编码器**：通过移位窗口注意力（shifted-window attention）将体素特征进一步压缩为一组结构化的稀疏潜在向量 $\{z_k\}_{k=1}^{L}$（Eq. 3）。

**解码**：解码器 $\mathcal{D}$ 将潜在向量解码为局部特征网格，再通过 MLP 查询任意表面点 $p_j$ 的 RGB 颜色 $c_j$（Eq. 4），形成一个连续的 3D 颜色场 $\mathcal{C}(p)$。

**训练监督**：直接在 3D 空间使用 L1 颜色重建损失与 KL 散度正则化项（Eq. 5），避免了 2D 投影方法中渲染损失（如 LPIPS/SSIM）带来的信息损失和视角偏差。

### 几何条件的隐式编码

LaFiTe 的一个关键设计是**共享同一 VAE 编码器来提取纯几何条件**。具体做法是将输入点云的全部颜色 $c_i$ 设为规范值（如白色 $(1,1,1)$），得到单色点云。该单色点云通过同一编码器后，输出的潜在向量 $z_{\mathrm{geo}}$ 仅编码了无纹理遮挡的纯几何信息（位置与法向），为后续生成模型提供了精确对齐的 3D 结构条件。

### 条件生成：整流流与分层 PBR 生成

**基础色生成**：以几何潜在 $z_{\mathrm{geo}}$ 为条件，训练一个条件整流流模型（rectified flow）从噪声中恢复纹理潜在向量（Eq. 6）。生成完成后，解码器将纹理潜在解码为连续颜色场，再通过**纹理烘焙模块**查询到标准 UV 贴图上，实现与传统渲染管线的兼容。

**PBR 材质生成**：采用分层策略——先生成基础色（albedo），再以基础色潜在为条件生成粗糙度-金属度（roughness-metallic）纹理。该过程复用预训练的颜色纹理 VAE，仅将其三个颜色通道替换为粗糙度、金属度和一个零填充通道，从而在物理依赖关系上更忠实地建模材质属性。

**后处理能力**：框架还支持**局部细化**——用户可在指定区域重新执行局部潜在生成与解码，获得更高分辨率的纹理细节；以及**多视角投影整合**——将多视角 2D 投影结果作为部分观测，由 LaFiTe 补全被遮挡区域的纹理。

### 模块关系总结

| 模块 | 功能 | 输入 | 输出 |
|------|------|------|------|
| 点-体素注意力编码 | 点特征增强与体素特征聚合 | 分组彩色点云 | 体素纹理特征 |
| 稀疏 VAE 编码器 | 压缩为结构化潜在向量 | 体素特征 | 纹理潜在 $\{z_k\}$ / 几何潜在 $z_{\mathrm{geo}}$ |
| 连续颜色场解码器 | 查询任意点的 RGB 颜色 | 潜在向量 + 查询点 $p_j$ | 颜色 $c_j$ |
| 条件整流流生成模型 | 以几何为条件生成纹理潜在 | 噪声 + $z_{\mathrm{geo}}$ | 纹理潜在 |
| PBR 材质生成分支 | 分层生成粗糙度-金属度 | 基础色潜在 | PBR 纹理 |
| 纹理烘焙模块 | 转换为标准 UV 贴图 | 连续颜色场 + UV 坐标 | UV 纹理贴图 |

这一设计实现了**表示与条件的优雅协同**：VAE 编码器同时服务于纹理压缩和几何条件提取，点-体素注意力机制保证了局部细节的捕捉能力，稀疏体素结构确保了计算效率，而连续颜色场解码则赋予了表示对任意拓扑的泛化能力。



### 点-体素注意力编码模块

LaFiTe的核心创新在于将纹理表示为**稀疏潜在颜色场**，其编码过程从网格表面均匀采样的彩色点云出发。每个点 $x_i = (p_i, n_i, c_i)$ 包含位置、法向和RGB颜色信息。编码器首先将3D空间离散化为体素网格，仅保留物体表面附近的活跃体素，形成稀疏结构。

对于每个包含 $n$ 个点的活跃体素，采用**点-体素注意力机制**进行特征聚合，分为两步：

**体素内自注意力** 对同一体素内的点进行特征增强：

$$\widetilde{x}_i = \sum_{j=1}^{n} \mathrm{softmax}\big(\frac{Q_{x_i} K_{x_j}^T}{\sqrt{d}}\big) \cdot V_{x_j}$$

其中 $Q_{x_i}$、$K_{x_j}$、$V_{x_j}$ 分别为点 $x_i$ 的查询、键、值投影，$d$ 为特征维度。该操作使每个点能够感知同体素内其他点的几何与外观信息，捕获局部纹理细节。

**点-体素交叉注意力** 将增强后的点特征聚合为体素级特征：

$$\widetilde{v}_k = \sum_{i=1}^{n} \mathrm{softmax}\big(\frac{Q_{v_k} K_{\widetilde{x}_i}^T}{\sqrt{d}}\big) \cdot V_{\widetilde{x}_i}$$

其中 $Q_{v_k}$ 为可学习的体素查询向量，$\widetilde{x}_i$ 为经自注意力增强后的点特征。该设计替代了传统PointNet的平均池化，使模型能够自适应地关注不同点的重要性，显著改善局部细节的捕捉能力（Figure 4）。

### 稀疏体素VAE编码器

编码器 $\mathcal{E}$ 将分组点云映射为稀疏潜在向量序列：

$$\mathcal{E}: \{\{x_j\}_{j=1}^{N_i}\}_{i=1}^{L} \to \{z_k\}_{k=1}^{L}$$

其中 $L$ 为活跃体素数量，$N_i$ 为第 $i$ 个体素内的点数。编码器采用移位窗口注意力（shifted-window attention）在体素特征间传递上下文信息，最终输出每个活跃体素位置的结构化潜在向量 $z_k$。

### 连续颜色场解码器

解码器 $\mathcal{D}$ 将潜在向量解码为局部特征网格，并通过MLP实现任意点的连续颜色查询：

$$\mathcal{D}: \{z_k\}_{k=1}^{L} \times p_j \to c_j$$

给定潜在向量集合和3D查询点 $p_j$，解码器预测该点的RGB颜色 $c_j$。这种连续表示使纹理查询与网格拓扑解耦，天然避免了UV展开带来的变形和接缝问题。

### VAE训练损失

VAE的训练目标为增强颜色的L1重建损失与KL散度正则化：

$$\mathcal{L} = \mathbb{E}_{\boldsymbol{x}_i \sim \mathcal{M}} [ | \mathcal{D}(\mathcal{E}(\{\hat{x}_i\}), p_j) - \hat{c}_j | ] + \mathcal{L}_{\mathrm{KL}}$$

其中 $\hat{x}_i$ 为原始彩色点云，$\hat{c}_j$ 为真实颜色，$\mathcal{L}_{\mathrm{KL}}$ 约束潜在分布接近标准高斯分布，保证潜在空间的连续性和生成友好性。与依赖渲染损失（LPIPS/SSIM）的投影方法不同，该损失直接在3D空间监督，避免了多视角投影带来的信息损失和矛盾。

### 几何潜在分支

为向生成模型提供精确的3D几何条件，LaFiTe采用**共享VAE编码器**提取纯几何信息。具体做法是将输入点云的所有颜色 $c_i$ 设为规范值白色 $(1,1,1)$，得到单色点云。该单色点云经由同一编码器处理后，输出的潜在向量 $z_{\mathrm{geo}}$ 仅编码了无遮挡的几何结构信息，与纹理外观解耦。这种设计避免了额外几何编码器的训练开销，同时保证了几何条件与纹理潜在空间的对齐。

### 条件整流流生成模型

纹理生成采用整流流（rectified flow）模型，以几何潜在 $z_{\mathrm{geo}}$ 为条件，从噪声恢复纹理潜在向量：

$$\mathcal{L}_{\mathrm{albedo}} = \mathbb{E} \| v(x_t; t, z_{\mathrm{geo}}) - (\epsilon - x_0) \|$$

其中 $x_0$ 为目标纹理潜在，$\epsilon \sim \mathcal{N}(0, I)$ 为高斯噪声，$x_t = t x_0 + (1-t) \epsilon$ 为线性插值的中间状态，$v(\cdot)$ 为速度场预测网络。该损失训练模型学习从噪声到数据的直线路径，在推理时通过常微分方程求解器逐步去噪，生成与输入几何匹配的纹理潜在向量。

### PBR材料生成分支

对于物理渲染（PBR）纹理，LaFiTe采用层次化生成策略：先生成基础色（albedo）纹理，再以基础色潜在为条件生成粗糙度-金属度图。具体实现中，将预训练的颜色纹理VAE的三个颜色通道替换为粗糙度、金属度和一个零填充通道，复用编码器架构，从而以较小的训练代价扩展至PBR材质生成。



## 实验与关键发现

### 核心实验设计

LaFiTe的实验验证围绕三个递进层次展开：(1) VAE表示的重建保真度——验证稀疏潜在颜色场本身能否无损捕获高频纹理细节；(2) 条件纹理生成的视觉与定量质量——验证以几何潜在为条件的整流流模型能否生成与输入条件对齐的无缝纹理；(3) 关键设计选择的消融——揭示表示能力对输入密度和注意力机制的依赖关系。

所有方法在统一策划的3D资产数据集上训练，采用标准度量（FID、FD_CLIP、KD_DINO等），并尽可能复现官方实现以保证公平性。VAE在16块NVIDIA A800 GPU上训练600K步（batch size 256），整流流反照率生成模型在32块A800上训练500K步。

### 主结果：VAE重建保真度

VAE重建实验是验证表示能力的核心证据。LaFiTe在128³体素分辨率下达到**PSNR 34.62 dB**，相比TRELLIS基线（23.07 dB）提升超过11.5 dB（Table 2）。SSIM同样从0.798跃升至0.934。这一差距的本质原因在于输入模态的根本差异：TRELLIS依赖从多视角渲染图像中提取的投影特征，存在信息压缩和视角间不一致问题；而LaFiTe直接从网格表面密集采样的彩色点云中学习，避免了投影带来的信息损失。

![[assets/figures/papers/paper_list_l2530_https_arxiv_org_abs_2512_04786/figures/006_Table_2.jpg]]
*Table 2: VAE Reconstruction Fidelity. Our VAE, which uses a direct point cloud input, achieves significantly higher fidelity than TRELLIS, which uses projected image features. ‘*’ denotes the result is derived from the 64 resolution model without training on higher resolutions*

Table 2还揭示了分辨率维度的优势：即使在64³分辨率下，LaFiTe的PSNR（31.73 dB）仍显著优于TRELLIS在128³下的表现（23.07 dB），说明表示效率而非单纯分辨率是性能瓶颈。

### 主结果：条件纹理生成

Table 1汇总了图像/文本条件纹理生成的定量对比。在无光照渲染（unshaded）设置下，LaFiTe在FD_CLIP、KD_DINO等感知对齐指标上达到最优或次优；在有光照渲染（shaded）设置下，FD_CLIP达到46.28的最优值。这验证了3D原生表示在保持多视角一致性方面的优势——投影方法在不同视角下可能产生矛盾的纹理信号，而LaFiTe的连续颜色场天然保证任意视角查询的一致性。

定性结果（Figure 5）进一步佐证：LaFiTe生成的纹理与参考图像和给定几何体的对齐更忠实，且无接缝或不一致。在自遮挡区域（Figure 3），投影方法出现明显的纹理缺失或错误，而LaFiTe的3D原生公式保持了完整且连贯的纹理。

![[assets/figures/papers/paper_list_l2530_https_arxiv_org_abs_2512_04786/figures/004_Figure_3.jpg]]
*Figure 3: Robustness to self-occlusion. LaFiTe’s 3D-native formulation generates complete and coherent textures even in highly occluded regions where projection methods fail*

![[assets/figures/papers/paper_list_l2530_https_arxiv_org_abs_2512_04786/figures/008_Figure_5.jpg]]
*Figure 5: Qualitative comparison of image-conditioned 3D texture generation. Textures generated by LaFiTe are more faithfully aligned to both the reference image and the given geometry, and are free from seams or inconsistencies*

### 消融分析

**点云采样密度的影响**（Table 3）是验证表示可扩展性的关键消融。在128³分辨率下，输入点云从20K增至4M点时，PSNR从26.07 dB单调提升至34.45 dB。这表明：(1) 表示能从更密集的表面采样中持续获益，未出现饱和；(2) 实际部署中可通过控制采样密度在质量与计算开销间灵活权衡。

**点-体素注意力机制**是另一个关键设计选择。与使用PointNet平均池化的SparseFlex基线相比，LaFiTe的体素内自注意力+点-体素交叉注意力模块显著改善了局部细节的捕捉能力（Figure 4）。平均池化将体素内所有点的特征无差别压缩，丢失了空间变化信息；而注意力机制允许模型选择性聚合与体素查询最相关的点特征，从而保留高频纹理结构。

### 扩展能力验证

LaFiTe展示了多项超出基础纹理生成的扩展能力：

- **多视角投影整合**（Figure 6）：LaFiTe可作为补全模块，接收多视角投影产生的部分纹理，生成被遮挡区域的完整纹理。这为与现有投影方法的协同提供了路径。
- **PBR材质生成**（Figure 7）：通过层次化生成策略（几何→反照率→粗糙度-金属度），LaFiTe可基于2D材质图生成带有PBR属性的纹理，实现材质迁移。
- **局部细化**（Figure 8）：用户可在指定区域触发局部潜在再生成，以更高分辨率增强该区域的纹理质量，无需重新生成整个纹理。

![[assets/figures/papers/paper_list_l2530_https_arxiv_org_abs_2512_04786/figures/009_Figure_6.jpg]]
*Figure 6: Integration with multi-view projections. LaFiTe can be used to complete occluded regions for the partial 3D texture projected from multi-view images*

![[assets/figures/papers/paper_list_l2530_https_arxiv_org_abs_2512_04786/figures/010_Figure_7.jpg]]
*Figure 7: Material Transfer. LaFiTe can generate textures with PBR materials conditioned on a 2D material image*

![[assets/figures/papers/paper_list_l2530_https_arxiv_org_abs_2512_04786/figures/011_Figure_8.jpg]]
*Figure 8: Local Refinement. LaFiTe can further enhance the generation quality by refining a local region*

### 失败模式与局限

尽管LaFiTe在重建和生成质量上取得了显著优势，但验证分析也揭示了明确的失败模式：

1. **训练数据依赖性**：模型对高质量3D资产的依赖限制了其对稀有风格（如特定艺术风格或小众题材）的泛化能力。当输入条件偏离训练分布时，生成质量会明显下降。
2. **文本语义理解不足**：由于未有效利用大规模2D生成先验（如预训练的扩散模型），LaFiTe在文本条件生成中的语义理解和文字纹理渲染方面仍存在不足——这是3D原生方法共有的局限，因为3D文本-纹理配对数据远少于2D图文数据。
3. **采样密度敏感性**：若输入网格的表面采样点密度不足（如稀疏几何体或用户未正确配置采样参数），重建质量会明显退化（Table 3中20K点的PSNR仅为26.07 dB），需要用户或自动流程确保足够的表面覆盖。

### 关键图表结论

- **Table 2**：LaFiTe VAE在128³分辨率下PSNR达34.62 dB，超越TRELLIS基线11.55 dB，证明直接点云输入优于投影特征。
- **Table 1**：LaFiTe在图像/文本条件纹理生成中达到最优或次优的FD_CLIP和KD_DINO分数，3D原生方法在多视角一致性上具有结构性优势。
- **Table 3**：重建质量随点云密度单调提升，从20K点的26.07 PSNR到4M点的34.45 PSNR，验证了表示的可扩展性。
- **Figure 3**：自遮挡区域的定性对比揭示了投影方法的根本缺陷——3D原生表示是解决遮挡一致性的正确方向。
- **Figure 4**：点-体素注意力机制重建的纹理更清晰、细节更丰富，避免了平均池化导致的模糊和伪影。

![[assets/figures/papers/paper_list_l2530_https_arxiv_org_abs_2512_04786/figures/003_Table_1.jpg]]
*Table 1: Quantitative comparison for conditional texture generation. We evaluate LaFiTe against leading text- and image-conditioned texture generation methods. LaFiTe achieves superior or competitive performance across nearly all metrics, demonstrating its state-of-theart generation quality. Lower is better for all metrics*

![[assets/figures/papers/paper_list_l2530_https_arxiv_org_abs_2512_04786/figures/005_Table_3.jpg]]
*Table 3: Effect of Sample Point Density for Reconstruction. VAE reconstruction quality consistently improves with denser input point cloud sampling, showcasing the model’s scalability*

![[assets/figures/papers/paper_list_l2530_https_arxiv_org_abs_2512_04786/figures/007_Figure_4.jpg]]
*Figure 4: Visual comparison of VAE reconstruction quality. Our method reconstructs sharper, more detailed textures, avoiding the blurs and artifacts of the TRELLIS baseline*

### 补充图表

![[assets/figures/papers/paper_list_l2530_https_arxiv_org_abs_2512_04786/figures/001_Figure_1.jpg]]
*Figure 1: A gallery of diverse 3D assets textured by our 3D-native framework, LaFiTe, demonstrating high-fidelity, seamless textures across a wide range of visual styles*



## 定位与知识库关联

### 3D纹理生成的方法谱系

当前3D纹理生成技术可按纹理表示空间划分为三大范式：**投影法**、**UV空间法**和**3D原生法**。LaFiTe属于第三范式，其核心突破在于将纹理建模为连续的稀疏潜在颜色场，从根本上规避了前两种范式的固有缺陷。

**投影法**（如MVPaint、GlassPBR）通过多视角渲染将纹理生成转化为2D图像合成问题，再利用逆投影将颜色映射回网格表面。这类方法天然受限于视角选择——自遮挡区域无法获得有效纹理信息，且多视角投影之间缺乏显式一致性约束，容易产生接缝和颜色跳变（Figure 3）。此外，投影过程本身引入的信息损失（如透视变形、离散化误差）使得高频细节难以保真。

**UV空间法**（如TexGen）将网格展开到2D平面后直接生成UV贴图。虽然UV空间是标准图形管线中的成熟表示，但切割展开必然引入几何变形和边界不连续性——在3D空间中相邻的纹理区域在UV空间中可能被强制分离，生成模型难以学习这种非局部对应关系。TexGen等方法的输出常表现为UV边界处的纹理断裂或模糊。

**3D原生法**是LaFiTe所代表的新方向。与TRELLIS（Xiang et al., CVPR 2025）虽同属3D生成框架，但两者在纹理表示上存在本质差异：TRELLIS依赖从多视角渲染图像中提取的2D特征投影到稀疏体素网格，本质上仍受投影信息损失的影响；LaFiTe则直接从网格表面采样的彩色点云中学习，输入域与目标域在3D空间内天然对齐。这一差异直接体现在VAE重建保真度上——LaFiTe在128³体素分辨率下的PSNR达到34.62 dB，较TRELLIS-RF128*的23.07 dB提升超过11.5 dB（Table 2），SSIM从0.798提升至0.934。视觉上，LaFiTe重建的纹理更清晰、细节更丰富，避免了TRELLIS的模糊和伪影（Figure 4）。

### 表示设计的核心差异

LaFiTe的表示设计包含三个关键选择，每个都对应着对现有方法的改进：

1. **输入表示**：从多视角渲染图像（投影法）或UV展开图（UV空间法）转向从网格表面均匀采样的彩色点云。点云作为3D原生的几何载体，天然避免了投影遮挡和UV切割变形。消融实验表明，VAE重建质量随采样密度增加而持续提升——从20K点的26.07 PSNR到4M点的34.45 PSNR（Table 3, 128³分辨率），验证了该表示的可扩展性。

2. **编码器架构**：采用点-体素注意力机制替代PointNet式的平均池化（如SparseFlex所用）。具体而言，先对同一体素内的点执行自注意力以捕捉局部几何-外观关联（Eq. 1），再通过可学习的体素查询向量与增强后的点特征进行交叉注意力聚合（Eq. 2）。这一设计使得编码器能自适应地关注信息丰富的表面点，而非简单平均，从而更好地保留高频细节（Figure 4间接佐证）。

3. **几何条件编码**：通过共享VAE编码器输入单色点云（所有颜色设为白色）获得纯几何潜在，作为生成模型的条件。这一设计与使用独立几何编码器或2D位置/法向投影图的方法形成对比——共享编码器确保了纹理潜在与几何潜在在同一个结构化空间中对齐，为后续流匹配生成提供了精确的3D几何条件。

### 适用边界

**强项场景**：
- 高保真纹理重建与生成，尤其在需要保持无缝一致性和高频细节时
- 自遮挡严重的复杂几何体（Figure 3）
- 需要PBR材质生成时，分层生成策略（几何→基础色→粗糙度-金属度）能有效建模物理依赖关系
- 多视角投影结果的补全——LaFiTe可整合不完整的多视角投影纹理，补全被遮挡区域（Figure 6）
- 局部纹理细化——用户可在指定区域重新生成更高分辨率纹理（Figure 8）

**弱项与局限**：
- 训练数据依赖高质量3D资产，而此类数据规模仍然有限，限制了模型对稀有风格和长尾概念的泛化能力
- 未有效利用大规模2D生成先验（如预训练的扩散模型），导致文本语义理解和文字纹理生成仍有不足——这是相对于可借助Stable Diffusion等2D先验的投影法的劣势
- 若输入网格的采样点密度不足，重建质量会明显下降（Table 3），需要由用户或自动流程确保足够的表面采样
- 当前表示仅覆盖表面颜色和简单PBR材质（粗糙度、金属度），尚未扩展到更复杂的全局光照效果或体纹理

### 开放问题与未来方向

1. **2D先验融合**：如何将大规模2D生成先验融入3D原生纹理生成，以提升语义合理性和文本渲染质量，是当前最紧迫的开放问题。可能的路径包括在潜在空间中引入2D-3D联合训练，或利用2D扩散模型作为教师模型蒸馏语义知识。

2. **数据稀缺性缓解**：能否利用大规模2D图像/视频数据缓解高质量纹理3D训练数据的稀缺性问题？多视角重建、单目深度估计与LaFiTe表示的联合训练可能是可行方向。

3. **表示扩展**：该稀疏潜在场表示是否可以扩展到更复杂的材质模型（如次表面散射、各向异性反射）或体纹理，而不仅是表面颜色和简单PBR参数？

4. **生成控制**：当前方法以图像或文本为条件，但缺乏对纹理风格、细节密度、材质属性等维度的精细控制。引入解耦的潜在空间或可插拔的控制模块是值得探索的方向。



## 原文 PDF

![[paperPDFs/CVPR_2026/Lafite_A_Generative_Latent_Field_for_3D_Native_Texturing.pdf]]
