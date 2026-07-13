---
title: "Dehallu3D: Hallucination-Mitigated 3D Generation from a Single Image via Cyclic View Consistency Refinement"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Dehallu3D_Hallucination_Mitigated_3D_Generation_from_a_Single_Image_via_Cyclic_View_Consistency_Refinement.pdf
project_link: null
code_link: null
aliases:
- Dehallu3D
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 通过引入密集中间视点并强制相邻视点间的深度图一致性（循环深度一致性损失 L_DC）和基于图像梯度的自适应平滑约束（深度平滑损失 L_DS），可以在保留锐利几何特征的前提下消除外点。
primary_logic: 利用密集小角度相邻视点的深度一致性可以有效弥合稀疏视图的间隙；同时利用彩色图像梯度作为指导，自适应调整深度平滑强度，可避免过度平滑并保留锐利特征。
claims:
- CVCR 模块通过循环深度一致性损失 L_DC（结合 SSIM 和余弦相似度）强制相邻 5° 视点的深度对齐，显著减少了外点。
- 自适应深度平滑损失 L_DS 根据图像梯度加权，在颜色梯度大的区域保留深度不连续性，防止过度平滑。
- 消融实验证明联合使用 L_DC 和 L_DS 可获得最佳网格质量（PSNR 达 21.8407），而单独使用一项效果较差。
- 采用 5° 角度间隔在重建质量与计算成本之间实现最佳均衡（PSNR 21.8407，耗时 163.3 秒）。
---

# Dehallu3D: Hallucination-Mitigated 3D Generation from a Single Image via Cyclic View Consistency Refinement

> [!tip] 核心洞察
> 利用密集小角度相邻视点的深度一致性可以有效弥合稀疏视图的间隙；同时利用彩色图像梯度作为指导，自适应调整深度平滑强度，可避免过度平滑并保留锐利特征。

| 字段 | 内容 |
|------|------|
| 中文题名 | Dehallu3D：基于循环视图一致性细化的单图三维幻觉缓解生成 |
| 英文题名 | Dehallu3D: Hallucination-Mitigated 3D Generation from a Single Image via Cyclic View Consistency Refinement |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Wang_Dehallu3D_Hallucination-Mitigated_3D_Generation_from_a_Single_Image_via_Cyclic_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | Dehallu3D |
| Dataset | GSO |

> [!tip] 效果简介
> - GSO 上，PSNR ↑ 21.8407 vs — (best competing method in Table 1) (—)；SSIM ↑ 0.8966 vs — (—)；LPIPS ↓ 0.1453 vs — (—)。

## 概要

单张图像到三维网格的重建是计算机视觉与图形学中的核心挑战。现有主流方法（如 **Unique3D** (Wu et al., NeurIPS 2024)、**InstantMesh** (Xu et al., arXiv 2024)、**TripoSR** (Tochilkin et al., arXiv 2024) 等）通常依赖稀疏生成的多视图图像进行重建。然而，稀疏视图之间存在显著的视角间隙与不连续性，导致后续重建过程中引入**幻觉性结构外点**——表现为网格表面的异常孔洞、突出物或漂浮碎片，严重损害几何保真度。

针对这一瓶颈，本文提出 **Dehallu3D**，一种基于**循环视图一致性细化（Cyclic View Consistency Refinement, CVCR）** 的即插即用优化模块。其核心洞察在于：通过在稀疏正交视图之间渲染密集的小角度相邻视点（5°间隔，共72个视图），并强制相邻深度图之间的一致性，可以有效弥合视角间隙，消除外点。同时，利用彩色图像梯度作为自适应权重，在平滑噪声与保留锐利几何特征之间取得动态平衡，避免传统平滑策略导致的过度平滑问题。

在方法谱系上，Dehallu3D 定位于**后处理式网格优化**范畴。其流程分为两个阶段：首先通过多视图生成器获得正交彩色图与法向贴图，经深度估计与泊松重建初始化网格，并在粗重建阶段利用表面曝光加权法向损失快速修正全局拓扑；随后，CVCR 模块以即插即用的方式介入，通过循环深度一致性损失（$\mathcal{L}_{DC}$）和自适应深度平滑损失（$\mathcal{L}_{DS}$）进行精细优化。该方法可与现有重建框架（如 Unique3D）灵活集成，无需修改其内部结构。

实验结果表明，Dehallu3D 在 GSO 数据集上取得了优异的网格质量：PSNR 达 21.8407，SSIM 为 0.8966，LPIPS 低至 0.1453，Chamfer Distance 为 0.02023。消融研究证实，联合使用 $\mathcal{L}_{DC}$ 和 $\mathcal{L}_{DS}$ 是消除外点的关键，单独使用其中一项效果显著下降。此外，5° 角度间隔在重建质量与计算开销（约163秒）之间实现了最佳均衡。

**局限性与开放问题**：当前优化耗时仍距实时应用有差距；CVCR 在其他重建框架上的泛化性尚未充分验证；严重依赖初始多视图生成质量。未来方向包括探索自适应角度密度分配、动态场景扩展，以及将异常风险度量（ORM）直接作为训练损失等。

### 单图三维生成的核心瓶颈：稀疏视图间的幻觉性外点

从单张二维图像重建三维网格是计算机视觉和图形学中的一项基础性挑战。近年来，基于多视图生成的重建方法取得了显著进展，其典型流程为：首先利用扩散模型或多视图生成器从输入图像生成一组正交视图的彩色图像和法向贴图，随后通过立体匹配或可微渲染将这些视图融合为三维网格。然而，这一范式存在一个深层瓶颈：**生成的视图数量稀疏且视角间存在较大间隙**（通常仅覆盖前、后、左、右四个正交方向），导致相邻视点之间的几何信息高度不连续。

这种不连续性在后续重建阶段会引发严重的“幻觉”现象——网格表面出现异常孔洞、突兀的突起物或漂浮的碎片结构，本文将这些缺陷统称为**网格外点（mesh outliers）**。外点的产生并非源于单一模块的失效，而是稀疏视图重建中信息缺失的系统性后果：当优化器试图弥合两个相距90°的视点时，中间区域的几何形状缺乏任何观测约束，从而为不可靠的推断留下了空间。

现有方法对这一问题的处理存在明显缺口。多数工作将重点放在提升多视图生成的质量或改进网格初始化策略上，但未从根本上解决**视图间连续性约束缺失**的问题。正交视图一致性约束只能保证网格在四个特定角度下的投影正确，却无法约束这些视角之间的过渡区域。因此，即使生成视图本身质量较高，重建结果仍可能在不可见区域出现结构异常。

### 核心思路：密集中间视点的循环一致性约束

Dehallu3D 的动机源于一个关键洞察：**利用密集的小角度相邻视点之间的深度一致性，可以有效弥合稀疏视图的信息间隙**。具体而言，如果在360°范围内以较小的角度间隔（如5°）渲染密集视图，并强制相邻视点的深度图在结构和方向上保持一致，那么原本缺乏约束的过渡区域将获得充分的几何监督，从而消除外点产生的条件。

这一思路面临两个相互制约的子问题。其一，**如何定义有效的深度一致性度量**：简单的逐像素差异无法捕捉深度图的结构相似性，而过于宽松的约束则难以消除外点。其二，**如何在消除外点的同时保留锐利几何特征**：密集一致性约束天然倾向于平滑化，可能导致物体边缘和细节的过度模糊。Dehallu3D 通过两项互补设计解决这一矛盾——采用结合SSIM和余弦相似度的循环深度一致性损失来精确对齐相邻深度图，同时引入基于彩色图像梯度的自适应平滑权重，在颜色梯度大的区域（对应几何边缘）自动减弱平滑惩罚，从而在去除外点与保留锐利特征之间取得平衡。

### 即插即用的模块化设计理念

Dehallu3D 的另一个重要动机是**通用性**。上述循环视图一致性细化策略被封装为一个独立的**即插即用（plug-and-play）优化模块**，称为循环视图一致性细化（Cyclic View Consistency Refinement, CVCR）。该模块不依赖于特定的网格初始化方式或多视图生成器架构，理论上可集成到各类单图三维重建流程中。论文通过在 **Unique3D**（Wu et al., NeurIPS 2024）上验证CVCR的即插即用性，初步证明了该设计的通用潜力。

## 核心方法与创新机理

Dehallu3D 的核心创新在于提出了一种**即插即用的循环视图一致性细化（CVCR）模块**，以解决现有单图到三维重建方法中因稀疏多视图间隙导致的网格幻觉性外点问题。该方法围绕三个关键的 changed slots 展开：

### 1. 密集中间视点与循环深度一致性约束

现有方法（如 Unique3D (Wu et al., NeurIPS 2024)）通常仅依赖 4 个正交视图进行重建，视角间存在较大间隙和不连续性，导致后续重建引入异常孔洞或突出物等外点。Dehallu3D 将视图数量扩展至 **72 个密集视点**（5° 角度间隔），并显式建模 360° 旋转中相邻视点间的循环关系。其核心是**循环深度一致性损失（L_DC）**：

$$\mathcal{L}_{DC} = \sum_{i=1}^{V} (1 - \Delta(D_i^R, D_{i \bmod V + 1}^R))$$

其中深度相似度函数 $\Delta(D_i^R, D_j^R) = \mathrm{SSIM}(D_i^R, D_j^R) \cdot \mathrm{CS}(D_i^R, D_j^R)$ 结合了结构相似性（SSIM）和余弦相似度（CS），强制相邻视点的深度图在结构和方向上对齐。这一设计有效弥合了稀疏视图间的信息缺口，从根源上抑制了外点的产生。

### 2. 自适应深度平滑：保留锐利几何特征

仅施加深度一致性约束可能导致过度平滑，丢失物体的锐利边缘。Dehallu3D 引入**自适应深度平滑损失（L_DS）**，利用彩色图像梯度动态调整平滑惩罚强度：

$$w_i^{j,k} = \exp(-\|\nabla I_i^{R(j,k)}\|_2)$$

在颜色梯度大的区域（即物体边缘），权重 $w_i^{j,k}$ 趋近于零，平滑惩罚被衰减，从而保留深度不连续性；在纹理平坦区域，权重趋近于 1，施加正常平滑约束。这一机制实现了“保边平滑”，避免了传统方法中细节丢失的问题。

### 3. 表面曝光加权法向损失：快速全局拓扑修正

在粗重建阶段，Dehallu3D 在标准的掩码和法向 MSE 损失基础上，增加了**表面曝光加权法向损失（L_SE）**：

$$\mathcal{L}_{SE} = \sum_{v \in \mathcal{V}} \sum_{i}^{4} \epsilon_{i}^{v} \cdot | N_{v}^{R} - N_{i}^{v} |_{2}^{2}$$

其中 $\epsilon_{i}^{v} = m_{i}^{v} \cdot \frac{A_{i}^{v}}{\sum_{j} m_{j}^{v} A_{j}^{v}}$ 根据顶点在各视图中的可见性和投影面积动态分配权重，使高可见性视图对法向优化贡献更大。这有助于快速纠正初始网格的全局拓扑结构，为后续 CVCR 精细优化提供稳定的起点。

### 创新协同机制

上述三个 changed slots 形成递进式协同：L_SE 快速修正全局结构 → L_DC 弥合视图间隙消除外点 → L_DS 自适应保留锐利特征。消融实验证实，联合使用 L_DC 和 L_DS 可获得最佳网格质量（PSNR 达 21.8407），单独使用任一项效果均显著下降。CVCR 模块的即插即用特性使其可集成至各类网格重建管线，已在 Unique3D 骨干网络上验证了有效性。

Dehallu3D 采用“生成—初始化—粗重建—精炼”的四阶段流水线，将单张 RGB 图像转化为高保真三维网格。其核心设计在于将几何幻觉的消除问题转化为**密集相邻视点的深度一致性约束**，从而弥合稀疏多视图之间的信息间隙。

### 流水线总览

整个框架由四个顺序模块构成（Figure 2）：

![[assets/figures/papers/paper_list_l2249_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_Dehallu3D_Halluci/figures/002_Figure_2.jpg]]
*Figure 2: Overview of Dehallu3D. Dehallu3D first generate orthographic multi-view color images and corresponding normal maps, which are used to initialize a coarse mesh. Next, a globally plausible mesh is quickly constructed through the Coarse Mesh Reconstruction stage. Finally, the proposed Cyclic View Consistency Refinement (CVCR) module is employed to mitigate outliers and further refine the mesh*

1. **多视图生成器（Multi-View Generator）**  
   输入单张图像，输出 4 个正交视点的彩色图像及对应的法向贴图。该模块为后续所有阶段提供基础视觉几何信号。

2. **网格初始化（Mesh Initialization）**  
   利用前、后视图的法向贴图进行深度估计，结合随机旋转策略增强深度可靠性，再通过泊松重建生成初始网格。此阶段不追求细节精度，而是为后续优化提供一个拓扑合理的起点。

3. **粗网格重建（Coarse Mesh Reconstruction）**  
   基于可微渲染，以掩码损失 $\mathcal{L}_{mask}$、法向损失 $\mathcal{L}_{normal}$ 和**表面曝光加权法向损失** $\mathcal{L}_{SE}$ 联合驱动网格顶点变形，快速修正全局拓扑结构。$\mathcal{L}_{SE}$ 的核心机制是根据顶点在不同视图中的投影面积动态加权法向差异，使高可见度视图在优化中占据主导，从而加速形状收敛。

4. **循环视图一致性精炼（Cyclic View Consistency Refinement, CVCR）**  
   这是 Dehallu3D 的核心贡献模块，设计为**即插即用**的优化组件。它在 4 个正交视图之外，以 5° 角间隔渲染 72 个密集视点，通过**循环深度一致性损失 $\mathcal{L}_{DC}$** 和**自适应深度平滑损失 $\mathcal{L}_{DS}$** 消除网格外点并保留锐利几何特征。

### CVCR 的因果机制

CVCR 解决幻觉外点的逻辑链条如下：

- **瓶颈**：稀疏的正交视图间存在较大视角间隙，导致不可见区域的几何推断缺乏约束，产生异常孔洞或突出物。
- **调控变量**：引入密集中间视点并强制相邻视点（角间隔仅 5°）的深度图对齐，使原本“不可见”的区域获得间接监督。
- **$\mathcal{L}_{DC}$ 的作用**：对相邻视点的渲染深度图 $D_i^R$ 和 $D_{i+1}^R$ 计算结构相似性（SSIM）与余弦相似度（CS）的乘积 $\Delta(D_i^R, D_j^R)$，最小化 $1 - \Delta$ 以强制深度结构和方向的一致性。循环设计（$i \bmod V + 1$）确保 360° 范围的全局连贯。
- **$\mathcal{L}_{DS}$ 的作用**：对深度图施加梯度惩罚，但惩罚权重 $w_i^{j,k} = \exp(-\|\nabla I_i^{R(j,k)}\|_2)$ 由彩色图像梯度自适应调节——在颜色突变处（如边缘）权重趋近于 0，保留深度不连续性；在平坦区域权重趋近于 1，施加平滑约束。这解决了单纯使用 $\mathcal{L}_{DC}$ 可能导致的过度平滑问题。

### 即插即用特性

CVCR 模块与具体的网格初始化策略解耦，可集成到各类重建管线中。论文以 **Unique3D**（Wu et al., NeurIPS 2024）为骨干网络验证了其即插即用能力——将 CVCR 插入 Unique3D 后，网格外点显著减少，锐利特征得以保留（Figure 6）。

Dehallu3D 采用**两阶段优化管线**：粗网格重建（Coarse Mesh Reconstruction）与循环视图一致性细化（Cyclic View Consistency Refinement, CVCR）。前者快速修正全局拓扑，后者作为即插即用模块消除幻觉性外点并保留锐利几何特征。

### 3.1 多视图生成与网格初始化

管线首先通过多视图生成器（Multi-View Generator）从单张输入图像生成4个正交视图的彩色图像及对应法向贴图。网格初始化阶段利用前后视图的法向贴图进行深度估计，结合随机旋转与泊松重建技术生成初始网格。

### 3.2 粗网格重建

粗重建阶段的目标是快速修正网格的全局形状。基于可微渲染，该阶段优化以下联合损失：

$$
\mathcal{L}_{coarse} = \mathcal{L}_{mask} + \mathcal{L}_{normal} + \mathcal{L}_{SE} \tag{1}
$$

其中：
- **掩码损失** $\mathcal{L}_{mask} = \sum_{i=1}^{4} \| M_{i} - M_{i}^{R} \|_{2}^{2}$：约束生成掩码与渲染掩码的一致性。
- **法向损失** $\mathcal{L}_{normal} = \sum_{i=1}^{4} \| N_{i} - N_{i}^{R} \|_{2}^{2}$：约束生成法向图与渲染法向图的像素级对齐。
- **表面曝光加权法向损失**（Surface Exposure-weighted Normal Loss）$\mathcal{L}_{SE}$ 是该阶段的关键创新，定义为：

$$
\mathcal{L}_{SE} = \sum_{v \in \mathcal{V}} \sum_{i}^{4} \epsilon_{i}^{v} \cdot | N_{v}^{R} - N_{i}^{v} |_{2}^{2} \tag{2}
$$

其中 $\epsilon_{i}^{v} = m_{i}^{v} \cdot \frac{A_{i}^{v}}{\sum_{j} m_{j}^{v} A_{j}^{v}}$ 为曝光权重：$m_{i}^{v}$ 表示顶点 $v$ 在视图 $i$ 中的可见性，$A_{i}^{v}$ 为该顶点的投影面积。该权重根据顶点在不同视图中的可见性和投影面积动态分配优化优先级，使高可见性视图对顶点法向的约束更强，从而快速纠正全局结构偏差。

### 3.3 循环视图一致性细化（CVCR）

CVCR 是 Dehallu3D 的核心即插即用模块。它在4个正交视图之外渲染 $V=72$ 个密集视点（相邻视点角度间隔 $5^\circ$），并沿完整的 $360^\circ$ 旋转周期显式建模相邻视图间的循环关系。CVCR 的优化目标为：

$$
\mathcal{L}_{CVCR} = \mathcal{L}_{mask} + \mathcal{L}_{normal} + \lambda_1 \mathcal{L}_{DC} + \lambda_2 \mathcal{L}_{DS} \tag{5}
$$

其中 $\lambda_1$ 和 $\lambda_2$ 为平衡系数。核心创新在于两项新增损失：

#### 3.3.1 循环深度一致性损失 $\mathcal{L}_{DC}$

该损失强制相邻视点渲染深度图的结构和方向相似性，弥合稀疏正交视图间的几何不连续性：

$$
\mathcal{L}_{DC} = \sum_{i=1}^{V} (1 - \Delta(D_{i}^{R}, D_{i \bmod V + 1}^{R})) \tag{6}
$$

深度相似性函数 $\Delta$ 联合结构相似性（SSIM）和余弦相似度（CS）度量：

$$
\Delta(D_{i}^{R}, D_{j}^{R}) = \mathrm{SSIM}(D_{i}^{R}, D_{j}^{R}) \cdot \mathrm{CS}(D_{i}^{R}, D_{j}^{R})
$$

SSIM 捕获深度图的结构一致性，余弦相似度约束深度方向的对齐。两者乘积形式的联合度量确保相邻视点的深度图在结构和方向上均保持一致，从而有效消除因视角间隙产生的异常孔洞和突出物。

#### 3.3.2 自适应深度平滑损失 $\mathcal{L}_{DS}$

单纯的深度一致性约束可能导致过度平滑，丢失锐利几何特征。$\mathcal{L}_{DS}$ 通过图像梯度自适应调节平滑强度：

$$
\mathcal{L}_{DS} = \sum_{i=1}^{V} \sum_{j,k}^{\text{pixel}} |\nabla D_{i}^{R(j,k)}| \cdot w_{i}^{j,k} \tag{7}
$$

其中自适应权重 $w_{i}^{j,k}$ 由对应彩色图像的梯度幅值决定：

$$
w_{i}^{j,k} = \exp(-\|\nabla I_{i}^{R(j,k)}\|_{2})
$$

**机制解析**：在颜色梯度大的区域（如物体边缘），$\|\nabla I\|_{2}$ 较大，$w$ 趋近于 0，平滑惩罚被抑制，从而保留深度不连续性；在颜色平坦区域，$w$ 接近 1，施加正常平滑约束。这种“以彩色图像梯度为指导”的自适应机制实现了锐利特征保留与噪声平滑之间的动态平衡。

### 3.4 关键设计决策

消融实验（Table 2, Section 4.4）验证了各损失项的协同作用：单独使用 $\mathcal{L}_{DC}$ 能提升几何一致性但可能导致过度平滑；加入 $\mathcal{L}_{DS}$ 后 PSNR 达到 21.8407，在所有指标上取得最优。角度间隔消融（Table 3）表明 $5^\circ$ 是质量与效率的最佳平衡点——进一步减小至 $2.5^\circ$ 仅带来微小增益，却显著增加计算开销（$5^\circ$ 耗时约 163.3 秒）。

## 实验与关键发现

### 主实验结果

Dehallu3D 在 Google Scanned Objects (GSO) 数据集上与六个主流方法进行对比，涵盖视觉质量和几何精度两个维度。所有方法均以 512×512 分辨率输入，生成网格归一化到 [-0.5, 0.5] 范围内，从 {0°, 15°, 30°} 仰角和 8 个均匀方位角渲染 24 视图计算视觉指标。

定量结果（Table 1）显示，Dehallu3D 在全部指标上取得最优或次优表现。在视觉质量方面，PSNR 达到 21.8407，SSIM 为 0.8966，LPIPS 降至 0.1453，Clip-Sim 为 0.7753；几何精度方面，Chamfer Distance 为 0.02023，F-Score 为 0.4212。对比基线中，**SF3D** (Boss et al., CVPR 2025) 和 **Unique3D** (Wu et al., NeurIPS 2024) 在部分指标上表现接近，但 Dehallu3D 在几何指标上的优势更为显著。

![[assets/figures/papers/paper_list_l2249_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_Dehallu3D_Halluci/figures/004_Table_1.jpg]]
*Table 1: Quantitative comparison results. We mark the best scores in bold and the second-best scores with an underline*

定性对比（Figure 3）进一步揭示，**CRM** (Wang et al., ECCV 2024)、**InstantMesh** (Xu et al., arXiv 2024)、**TripoSR** (Tochilkin et al., arXiv 2024) 和 **Wonder3D** (Long et al., CVPR 2024) 等方法生成的网格在薄壁结构、边缘区域常出现异常孔洞或突出物（红色和蓝色框标注），而 Dehallu3D 在对应区域显著消除了这些外点，同时保留了锐利的几何特征。

### 异常值度量指标 ORM

为量化网格中的外点程度，论文提出了一种基于条件风险价值（CVaR）的异常风险度量 ORM。该指标将点云中每个点的异常分数定义为局部邻域密度比与全局 VAE 重建损失的加权和：

$$S(\mathcal{P}) = S_l(\mathcal{P}) + \lambda S_g(\mathcal{P})$$

其中局部度量 $S_l(\mathcal{P})$ 基于 k 近邻距离比检测稀疏离群点，全局度量 $S_g(\mathcal{P})$ 通过点云 VAE 的重建误差捕捉全局结构异常。最终 ORM 值由尾部风险 CVaR 在置信水平 $\xi$ 下计算：

$$\mathrm{CVaR}_{\xi}(\varphi) = \frac{1}{1-\xi} \sum_{r_i \geq \mathrm{VaR}_{\xi}} \mathcal{D}(r_i) r_i$$

Figure 5 的 ORM 对比柱状图显示，Dehallu3D 在所有方法中取得最低的 ORM 分数，定量验证了其外点去除效果。

![[assets/figures/papers/paper_list_l2249_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_Dehallu3D_Halluci/figures/008_Figure_5.jpg]]
*Figure 5: Comparison of ORM results across all methods*

### 消融实验

消融实验围绕三个关键设计展开：表面曝光加权法向损失 L_SE、循环深度一致性损失 L_DC 和自适应深度平滑损失 L_DS。

**损失函数消融**（Table 2）表明：
- 仅使用 L_DC 可显著提升几何一致性，但可能导致过度平滑，PSNR 和 F-Score 均低于完整方案。
- 仅使用 L_DS 能保留锐利特征，但缺乏跨视图一致性约束，外点消除不彻底。
- 联合使用 L_DC 和 L_DS 在所有指标上达到最优（PSNR 21.8407），证明循环一致性和自适应平滑之间存在协同效应——前者弥合视图间隙消除外点，后者利用图像梯度 $\nabla I_i^{R(j,k)}$ 自适应衰减平滑惩罚，在颜色梯度大的区域保留深度不连续性。

引入 L_SE 损失有助于粗重建阶段快速纠正全局拓扑结构，为后续 CVCR 精炼提供更稳定的初始网格。

**角度间隔消融**（Table 3）考察 CVCR 模块中相邻视点的角度间隔对质量与效率的影响：
- 从 10° 减小到 5°，PSNR 持续提升（从约 21.3 到 21.8407），外点消除更彻底。
- 进一步减小至 2.5°，质量增益微小，但优化耗时显著增加。
- 5° 间隔（72 个密集视点）在重建质量与计算成本（约 163.3 秒）之间实现最佳均衡。

定性消融（Figure 4）直观展示了 L_DC 和 L_DS 的独立与联合效果：仅用 L_DC 时网格表面趋于平滑但细节丢失；加入 L_DS 后边缘锐度明显恢复。

![[assets/figures/papers/paper_list_l2249_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_Dehallu3D_Halluci/figures/005_Figure_4.jpg]]
*Figure 4: Qualitative comparison results for ablation study on*

### 即插即用验证

为验证 CVCR 模块的即插即用特性，论文将其插入 **Unique3D** (Wu et al., NeurIPS 2024) 的重建流程。Figure 6 显示，插入 CVCR 后 Unique3D 生成网格的外点显著减少，几何质量明显改善，表明该模块可有效泛化至不同重建主干。但需注意，该验证目前仅限 Unique3D，在其他框架（如前馈式 LRM）上的泛化性尚未充分评估。

### 失败模式与局限

尽管 Dehallu3D 在外点消除上表现突出，仍存在以下局限：
1. **计算开销**：CVCR 的 72 视图优化耗时约 163 秒，距离实时应用仍有差距。
2. **初始多视图依赖**：方法严重依赖多视图生成器的输出质量。若生成的彩色图像或法向贴图存在较大误差（如遮挡推理错误），CVCR 的修复能力可能受限，外点仍会残留。
3. **ORM 指标局限**：ORM 虽能反映外点程度，但其阈值依赖和与人类感知质量的完全对齐仍需进一步验证。
4. **泛化边界**：CVCR 的即插即用性仅在 Unique3D 上验证，在更大规模数据集（如 Objaverse）和更多样化的重建框架上的表现尚不明确。

![[assets/figures/papers/paper_list_l2249_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_Dehallu3D_Halluci/figures/006_Table_2.jpg]]
*Table 2: Quantitative comparison results for ablation study on the proposed losses*

![[assets/figures/papers/paper_list_l2249_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_Dehallu3D_Halluci/figures/007_Table_3.jpg]]
*Table 3: Ablation study of angular intervals between adjacent views in the CVCR module*

## 定位与知识库关联

### 问题定位与核心瓶颈

单图到三维重建的主流范式依赖稀疏的多视图图像（通常为4个正交视图）进行三维推理。然而，稀疏视图之间存在较大的视角间隙和不连续性，导致后续重建过程在缺乏足够几何约束的区域引入**幻觉性结构外点**（hallucinated mesh outliers），表现为异常孔洞、突出物或漂浮碎片。Dehallu3D将这一现象归因于“稀疏视图间隙引入的几何歧义”，并据此提出**循环视图一致性细化**（Cyclic View Consistency Refinement, CVCR）作为系统性解决方案。

### 方法谱系与基线对比

Dehallu3D并非完全独立的重建框架，而是在现有流水线基础上插入的**即插即用优化模块**。其技术谱系可沿以下基线展开：

- **Unique3D** (Wu et al., NeurIPS 2024)：作为Dehallu3D的主要骨干和CVCR模块的验证平台。Unique3D采用多视图法向贴图驱动的网格重建，但缺乏显式的跨视图几何一致性约束，易在稀疏视图间隙区域产生外点。Dehallu3D通过CVCR模块弥补了这一缺陷，并在消融实验中展示了CVCR对Unique3D的显著改进（见Figure 6）。
- **SF3D** (Boss et al., CVPR 2025)、**CRM** (Wang et al., ECCV 2024)、**InstantMesh** (Xu et al., arXiv 2024)、**TripoSR** (Tochilkin et al., arXiv 2024)、**Wonder3D** (Long et al., CVPR 2024)：这些方法在GSO数据集上构成当前SOTA对比基线。Dehallu3D在视觉指标（PSNR 21.8407, SSIM 0.8966, LPIPS 0.1453, Clip-Sim 0.7753）和几何指标（Chamfer Distance 0.02023, F-Score 0.4212）上均取得最优或次优结果，验证了CVCR模块在主流重建流水线上的竞争力。

### 核心改进槽位

Dehallu3D相对于基线方法的改进可归纳为四个关键槽位：

| 改进槽位 | 基线做法 | Dehallu3D做法 | 证据锚点 |
|---------|---------|--------------|---------|
| 粗重建损失 | Mask + Normal MSE | 增加表面曝光加权法向损失 $\mathcal{L}_{SE}$ | Section 3.3, Eq. 1-2 |
| 视图一致性约束 | 隐式或限于正交视图 | 显式循环深度一致性损失 $\mathcal{L}_{DC}$（72个密集相邻视图） | Section 3.4, Eq. 6 |
| 锐利特征保留 | 无（潜在过度平滑） | 自适应深度平滑损失 $\mathcal{L}_{DS}$（图像梯度加权） | Section 3.4, Eq. 7 |
| 密集视图渲染 | 4个正交视图 | 72个密集视图（5°角度间隔）用于循环细化 | Section 3.4 (V=72) |

其中，**表面曝光加权法向损失** $\mathcal{L}_{SE}$ 通过顶点投影面积动态调整不同视图的法向监督权重，优先利用高可见性视图的信息，有助于快速修正粗网格的全局拓扑结构。消融实验证实，引入 $\mathcal{L}_{SE}$ 可提升后续CVCR优化的稳定性。

### 因果机制与证据强度

CVCR模块的核心因果机制在于**弥合稀疏视图间隙**：通过在360°范围内渲染密集小角度相邻视点（5°间隔），强制相邻视点深度图的结构和方向相似性。这一机制通过两个互补损失实现：

1. **循环深度一致性损失** $\mathcal{L}_{DC}$：结合SSIM和余弦相似度 $\Delta(D_i^R, D_j^R) = \mathrm{SSIM}(D_i^R, D_j^R) \cdot \mathrm{CS}(D_i^R, D_j^R)$，强制相邻视点深度对齐，显著减少外点（置信度0.98）。
2. **自适应深度平滑损失** $\mathcal{L}_{DS}$：利用彩色图像梯度加权 $w_i^{j,k} = \exp(-\|\nabla I_i^{R(j,k)}\|_2)$，在颜色梯度大的区域（如边缘）保留深度不连续性，防止过度平滑（置信度0.98）。

消融实验为这一因果机制提供了决定性证据：联合使用 $\mathcal{L}_{DC}$ 和 $\mathcal{L}_{DS}$ 可获得最佳网格质量（PSNR达21.8407），而单独使用其中一项效果明显较差（Table 2, Section 4.4）。仅用 $\mathcal{L}_{DC}$ 虽能提升几何一致性，但会导致过度平滑；加入 $\mathcal{L}_{DS}$ 可有效保留锐利特征（Figure 4）。

### 适用边界与局限

尽管CVCR模块在GSO数据集上展示了显著改进，其适用边界仍存在以下局限：

- **计算开销**：采用5°角度间隔在重建质量与计算成本之间实现最佳均衡（PSNR 21.8407，耗时163.3秒），但距离实时应用仍有差距。进一步减小间隔至2.5°仅带来微小增益，却显著增加计算开销（Table 3）。
- **即插即用泛化性**：CVCR的即插即用性目前仅在Unique3D上得到验证，其在其他重建框架（如feed-forward LRM架构）上的泛化性未充分评估。
- **初始多视图生成依赖**：方法严重依赖初始多视图生成的质量，若生成图像本身存在较大误差，CVCR的修复能力可能受限。
- **ORM指标局限**：提出的异常风险度量（ORM）指标虽能反映外点程度，但其阈值依赖和与人类感知的完全对齐仍需进一步验证。

### 开放问题与未来方向

Dehallu3D开启了若干值得探索的方向：

- **自适应计算分配**：能否通过神经网络学习自适应角度密度，在几何复杂区域动态增加视点密度，在平坦区域减少计算资源？
- **动态场景扩展**：该方法是否能扩展到动态场景或非刚体物体的三维生成？
- **ORM作为训练损失**：ORM能否作为可微训练损失直接优化，以实现更彻底的外点消除？
- **大规模数据集验证**：在更大规模数据集（如Objaverse）上，CVCR模块是否仍能保持优越性？
- **实时架构集成**：如何将CVCR集成到更快的重建架构（如feed-forward LRM）中以实现实时质量提升？

## 原文 PDF

![[paperPDFs/CVPR_2026/Dehallu3D_Hallucination_Mitigated_3D_Generation_from_a_Single_Image_via_Cyclic_View_Consistency_Refinement.pdf]]
