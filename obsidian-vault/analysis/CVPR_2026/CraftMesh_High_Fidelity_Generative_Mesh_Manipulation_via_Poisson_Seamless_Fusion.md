---
title: "CraftMesh: High-Fidelity Generative Mesh Manipulation via Poisson Seamless Fusion"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/CraftMesh_High_Fidelity_Generative_Mesh_Manipulation_via_Poisson_Seamless_Fusion.pdf
project_link: "https://jameshu.org/CraftMesh"
code_link: null
aliases:
- CraftMesh
tags:
- CVPR_2026
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 基于泊松无缝融合的混合SDF/Mesh表示，在梯度域求解泊松方程，利用混合法向图编辑和纹理梯度传播，实现编辑区域与原始网格的无缝几何与纹理融合。
primary_logic: 将网格编辑任务重构为二维图像编辑→三维网格生成→无缝融合的流水线，利用二维编辑的强大控制力和三维生成的保真度，再通过SDF域的泊松融合保证几何和纹理的平滑过渡，避免了传统三维直接编辑的多视角不一致和高计算复杂度。
claims:
- Poisson Geometry Blending 和 Poisson Texture Harmonization 单独使用均能提升编辑质量，两者结合表现最优。
- 我们的方法在 CLIP_sim、CLIP_dir、NIQE、NIMA 四项指标上均优于现有方法 FocalDreamer、MagicClay、Instant3dit 等。
- 定性比较显示，CraftMesh 能够产生和谐的几何结构、精细的局部细节和高保真颜色，而其他方法结果简单且不一致。
- CraftMesh Editing Benchmark 上 CLIP_sim ↑ = 20.801 (Ours-MeshyAI)
---

# CraftMesh: High-Fidelity Generative Mesh Manipulation via Poisson Seamless Fusion

> [!tip] 核心洞察
> 将网格编辑任务重构为二维图像编辑→三维网格生成→无缝融合的流水线，利用二维编辑的强大控制力和三维生成的保真度，再通过SDF域的泊松融合保证几何和纹理的平滑过渡，避免了传统三维直接编辑的多视角不一致和高计算复杂度。

| 字段 | 内容 |
|------|------|
| 中文题名 | CraftMesh：基于泊松无缝融合的高保真生成式网格操作 |
| 英文题名 | CraftMesh: High-Fidelity Generative Mesh Manipulation via Poisson Seamless Fusion |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Hu_CraftMesh_High-Fidelity_Generative_Mesh_Manipulation_via_Poisson_Seamless_Fusion_CVPR_2026_paper.html) · [Project](https://jameshu.org/CraftMesh) |
| Topic | #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation #topic/generative_models_diffusion/diffusion_image_video |
| Method | CraftMesh |
| Dataset | CraftMesh Editing Benchmark, Computational Cost |

> [!tip] 效果简介
> - CraftMesh Editing Benchmark 上，CLIP_sim ↑ 20.801 (Ours-MeshyAI)；CLIP_dir ↑ 18.479 (Ours-MeshyAI)；NIQE ↓ 4.710 (Ours-MeshyAI)。
> - Computational Cost 上，几何融合时间 (单张4090, 1000次迭代) ~5分钟 vs N/A；纹理和谐化时间 (单张4090, 2000次迭代) ~1分钟 vs N/A。

## 概要

三维网格编辑是生成式AI在3D内容创作中的核心需求，但现有方法面临一个关键瓶颈：**在施加复杂几何编辑时，难以保持原始网格的几何细节与纹理一致性**。基于分数蒸馏采样（SDS）或多视图扩散（MVD）的直接3D编辑方法，往往在编辑区域与原始网格之间产生明显的融合边界，表现为几何不连续与色彩偏移，严重限制了编辑的保真度和可控性。

针对这一问题，CraftMesh 提出了一种**范式转换**——将网格编辑任务重构为“二维图像编辑 → 三维网格生成 → 无缝融合”的三阶段流水线。其核心思想在于：利用二维编辑模型的强大控制力与三维生成模型的高保真重建能力，再通过**基于泊松方程的无缝融合**保证编辑区域与原始网格在几何与纹理上的平滑过渡，从而规避传统三维直接编辑中多视角不一致和高计算复杂度的固有问题。

方法的关键技术贡献包括两项：

- **泊松几何融合**：在混合SDF/Mesh表示下，通过法向图融合引导顶点优化，在梯度域求解泊松方程，实现编辑区域几何的自然过渡与细节保持。
- **泊松纹理和谐化**：通过梯度保持、软边界过渡和颜色分布对齐三个损失项，消除纹理接缝与色彩偏移，实现视觉一致的纹理融合。

实验结果表明，CraftMesh 在 CLIP_sim、CLIP_dir、NIQE、NIMA 四项指标上均优于 FocalDreamer、MagicClay、Instant3dit 等现有方法（Table 1）。消融研究进一步证实，几何融合与纹理和谐化各自独立使用即可提升编辑质量，两者结合则取得最优性能（Table 2）。定性比较显示，CraftMesh 能够生成和谐的几何结构、精细的局部细节和高保真色彩，而其他方法的结果往往简单且不一致（Figure 4）。

从方法谱系来看，CraftMesh 不同于基于 SDS 优化的 **FocalDreamer**（Li et al., AAAI 2024）和 **MagicClay**，也不同于基于多视图扩散重建的 **Instant3dit** 与 **CMD**（Li et al., SIGGRAPH 2025）。它通过将融合计算域从三维体积/坐标域降至二维图像域，将泊松方程求解的计算复杂度从 $O(n^3)$ 降至 $O(kn^2)$，在单张 RTX 4090 上几何融合约需 5 分钟，纹理和谐化约需 1 分钟。

需要指出的是，该方法的效果高度依赖上游二维编辑和三维网格生成模型的性能，且当前泊松融合主要解决局部几何与纹理的连续性，对于涉及大幅全局结构变形的编辑任务可能力有不逮。计算开销亦非实时，尚难直接应用于交互式创作环境。这些构成了方法的主要局限，也为后续研究指明了方向。

### 3D 内容编辑的需求与困境

随着 AIGC 技术在三维领域的快速渗透，高质量 3D 资产的需求正从专业建模向大众创作迁移。然而，现有生成式 3D 编辑方法在应对复杂几何编辑时，普遍面临一个核心瓶颈：**难以在修改网格局部区域的同时，保持原始网格的几何细节与纹理一致性**。具体表现为编辑区域与保留区域之间存在明显的融合边界、几何不连续以及色彩偏移，严重制约了编辑结果的保真度和可控性。

### 现有方法的局限

当前主流的生成式 3D 编辑范式可归纳为两类，各有其固有缺陷：

- **基于 Score Distillation Sampling (SDS) 的直接 3D 优化方法**（如 **FocalDreamer** (Li et al., AAAI 2024)、**MagicClay**）：通过在 3D 表示（NeRF、SDF 或 Mesh）上直接优化 SDS 损失来实现文本驱动的编辑。这类方法虽然灵活，但在处理复杂几何变化时，SDS 梯度固有的多视角不一致性容易导致几何退化、细节丢失和纹理模糊，且优化过程计算开销大。

- **基于多视图扩散的 3D 重建方法**（如 **Instant3dit**、**CMD** (Li et al., SIGGRAPH 2025)）：先利用微调的多视图扩散模型生成编辑后的多视角图像，再通过重建管线恢复 3D 表示。这类方法受限于多视图生成的一致性，在复杂编辑场景下常出现跨视角纹理不匹配和几何结构失真，且重建过程可能引入额外的伪影。

上述方法的共同症结在于：**将编辑任务完全限定在 3D 域内求解**，既难以充分利用 2D 图像编辑成熟的控制力，又受限于 3D 优化的高计算复杂度和多视角一致性问题。

### 本文动机与核心思路

CraftMesh 的出发点是将网格编辑任务**重构为“二维图像编辑 → 三维网格生成 → 无缝融合”的流水线**。这一设计背后的直觉是：

1. **2D 图像编辑**拥有最丰富、最可控的工具生态（文本引导、拖拽交互等），能够以低成本实现精准的语义编辑。
2. **3D 网格生成**模型（如 Hunyuan3D）已能从单张图像重建出高质量的三维网格，为编辑区域提供几何与纹理基础。
3. **融合**是连接两者的关键——如何将生成的编辑区域网格与原始网格无缝拼接，消除几何接缝和纹理突变，是实现高保真编辑的决定性环节。

为此，CraftMesh 引入两项核心技术：**泊松几何融合（Poisson Geometry Blending）** 和 **泊松纹理和谐化（Poisson Texture Harmonization）**。前者在 SDF 域求解泊松方程，利用混合法向图编辑实现编辑区域与原始网格的平滑几何过渡；后者通过梯度保持、软边界过渡和颜色分布对齐损失，消除纹理色彩偏移。两者协同，使得编辑结果在几何和纹理两个维度均达到无缝融合（Table 2 消融实验证实，两者单独使用均能提升编辑质量，结合后取得最优 CLIP_sim 20.801）。

此外，将泊松方程的求解域从传统 3D 体积降至 2D 图像域，使计算复杂度从 $O(n^3)$ 降至 $O(kn^2)$，在保证融合质量的同时显著提升了计算效率。

## 核心方法与创新机理

CraftMesh 的核心创新在于将网格编辑任务重构为**图像编辑 → 三维网格生成 → 无缝融合**的流水线，并引入基于泊松方程的两阶段融合技术，从根本上规避了现有方法在直接三维编辑中面临的多视角不一致和高计算复杂度问题。

### 范式转换：从直接三维编辑到 2D-3D-融合流水线

现有生成式网格编辑方法（如基于 Score Distillation Sampling 的 **FocalDreamer**（Li et al., AAAI 2024）、**MagicClay**，以及基于多视图扩散的 **Instant3dit**、**CMD**（Li et al., SIGGRAPH 2025））直接在三维空间进行优化或重建。这一范式存在根本性瓶颈：多视角一致性难以保证，且三维体积域的计算复杂度高达 $O(n^3)$，限制了编辑的保真度和可控性。

CraftMesh 的因果杠杆在于**将编辑操作上移至二维图像域**，充分利用二维编辑模型的强大控制力（文本驱动、拖拽驱动等），再通过图像到网格生成模型（如 Hunyuan3D）将编辑区域提升至三维，最后以泊松融合实现编辑区域与原始网格的无缝衔接。这一范式转换使计算复杂度从 $O(n^3)$ 降至 $O(kn^2)$，因为泊松方程的求解被转移到了二维图像域。

### 泊松几何融合：SDF 域的法向引导优化

传统坐标域泊松网格编辑直接在顶点坐标上求解，难以同时保持局部几何细节和全局平滑过渡。CraftMesh 提出**混合 SDF/Mesh 表示下的泊松几何融合**，其关键创新体现在三个层面：

1. **混合表示**：将网格转换为 SDF 表示，在 SDF 域进行优化，同时保留显式网格的可渲染性，使法向图可以作为优化信号。
2. **法向图融合引导**：将目标网格和编辑参考网格的法向图投影到二维，利用泊松图像编辑算法 $\Gamma(\cdot)$ 生成融合法向图 $n_p = \Gamma(n_t, n_e, mask^{opt})$，再以渲染法向图与融合法向图之间的 Frobenius 范数差作为损失函数 $\mathcal{L}_{poisson} = \sum_i \|\hat{n}_t^i - n_p^i\|_F^2$ 驱动顶点优化。
3. **受限优化区域**：通过距离阈值 $\epsilon_0$ 和 $\epsilon_1$（$\epsilon_1 < \epsilon_0$）定义嵌套的优化区域 $M_t^{opt} \subset M_t^{in}$，将修改严格限制在编辑边界附近，避免全局变形。

几何融合总损失结合了泊松损失、平滑正则项和 Eikonal 约束：
$$\mathcal{L}_{geo} = \mathcal{L}_{poisson} + \lambda_1 \mathcal{L}_{smooth} + \lambda_2 \mathcal{L}_{eik}$$

消融实验（Table 2）证实，泊松几何融合独立使用时即可将 CLIP_sim 从 17.723 提升至 20.502（+2.779），有效解决了几何不连续问题。

### 泊松纹理和谐化：梯度保持与分布对齐

纹理融合面临的核心挑战是色彩偏移和边界接缝。CraftMesh 的泊松纹理和谐化通过三个互补的损失函数解决这一问题：

1. **梯度保持损失** $\mathcal{L}_{grad}$：通过比较 sigmoid 归一化后的当前颜色梯度与原始颜色梯度，保留高频纹理细节，防止融合过程中纹理模糊。
2. **边界混合损失** $\mathcal{L}_{boundary}$：以距离加权方式约束新生成区域的颜色与保留区域接近，权重 $w_i = (1 - \delta / \|p_i^{new} - p_i^{pr}\|_2)^2$ 随距离增大而衰减，实现平滑颜色过渡。
3. **分布对齐损失** $\mathcal{L}_{distribution}$：对齐编辑区域与原始区域的整体颜色分布，消除系统性色彩偏移。

纹理和谐化总损失为：
$$\mathcal{L}_{tex} = \mathcal{L}_{distribution} + \theta_1 \mathcal{L}_{grad} + \theta_2 \mathcal{L}_{boundary}$$

消融实验显示，移除分布损失会降低纹理一致性（Figure 6e），移除梯度损失会损失高频细节（Figure 6f），移除边界损失会引入明显颜色边界（Figure 6g）。泊松纹理和谐化独立使用时将 CLIP_sim 从 17.723 提升至 19.399。

### 协同效应

几何融合与纹理和谐化的协同是 CraftMesh 取得最优性能的关键。Table 2 显示，两者结合（Ours-MeshyAI）取得最佳 CLIP_sim 20.801，显著优于单独使用任一组件的配置。定性结果（Figure 4）进一步验证，完整流水线能够产生和谐的几何结构、精细的局部细节和高保真颜色，而其他方法的结果简单且不一致。

### 方法谱系与知识库定位

CraftMesh 在网格编辑方法谱系中占据独特位置。与基于 SDS 优化的方法（FocalDreamer、MagicClay）相比，它避免了迭代优化的不稳定性；与基于多视图扩散重建的方法（Instant3dit、CMD）相比，它通过显式的泊松融合保证了几何和纹理的连续性。其技术路线可视为二维泊松图像编辑在三维网格域的延伸，但通过 SDF 域的法向融合和纹理梯度传播实现了跨维度的适配。

CraftMesh 将网格编辑重构为“图像编辑 → 三维网格生成 → 无缝融合”的流水线（Figure 2），从而将二维编辑的灵活控制力与三维生成的高保真度解耦复用。整个框架由三个核心模块串联构成。

![[assets/figures/papers/paper_list_l2186_https_openaccess_thecvf_com_content_CVPR2026_html_Hu_CraftMesh_High_Fide/figures/002_Figure_2.jpg]]
*Figure 2: An overview of the CraftMesh framework. Our framework follows an image editing–mesh generation–seamless fusion pipeline that fully leverages the strengths of 2D models for image editing and 3D models for high-quality mesh generation. First, Edited Region Mesh Generation produces meshes for the editing region. Then, Poisson Geometry Blending achieves natural geometric transitions through normal blending. Finally, Poisson Texture Harmonization performs texture fusion to seamlessly color the edited regions*

**Edited Region Mesh Generation**  
用户首先在二维参考图像上执行编辑（文本驱动或拖拽驱动），然后通过图像到网格生成模型（如 Hunyuan3D）将编辑后的图像区域提升为三维网格。该模块的输出是仅覆盖编辑区域的局部网格，承载了用户期望的几何与纹理变化，但尚未与原始网格建立连续过渡关系。

**Poisson Geometry Blending**  
该模块负责将编辑区域网格无缝嵌入原始网格。它采用混合 SDF/Mesh 表示，在梯度域求解泊松方程：将目标网格与编辑参考网格的法向图投影到二维，通过泊松图像编辑生成融合法向图，再以此驱动优化区域的顶点变形。优化损失由三部分构成：

$$
\mathcal{L}_{\mathrm{geo}} = \mathcal{L}_{\mathrm{poisson}} + \lambda_{1} \mathcal{L}_{\mathrm{smooth}} + \lambda_{2} \mathcal{L}_{\mathrm{eik}}
$$

其中 $\mathcal{L}_{\mathrm{poisson}}$ 最小化渲染法向图与融合法向图的 Frobenius 范数差，$\mathcal{L}_{\mathrm{smooth}}$ 约束顶点位移的平滑性，$\mathcal{L}_{\mathrm{eik}}$ 保持 SDF 的 Eikonal 性质。这一设计将三维体积域的计算复杂度从 $O(n^3)$ 降至二维图像域的 $O(kn^2)$，单张 RTX 4090 上约需 5 分钟完成融合。

**Poisson Texture Harmonization**  
几何融合完成后，新生成区域的纹理仍需与保留区域协调。该模块通过三项损失联合优化纹理：

$$
\mathcal{L}_{\mathrm{tex}} = \mathcal{L}_{\mathrm{distribution}} + \theta_{1} \mathcal{L}_{\mathrm{grad}} + \theta_{2} \mathcal{L}_{\mathrm{boundary}}
$$

- **梯度保持损失** $\mathcal{L}_{\mathrm{grad}}$ 对 sigmoid 归一化后的颜色梯度施加 MSE 约束，保留高频纹理细节；
- **边界混合损失** $\mathcal{L}_{\mathrm{boundary}}$ 以距离衰减权重约束新区域颜色向保留区域平滑过渡；
- **分布对齐损失** $\mathcal{L}_{\mathrm{distribution}}$ 匹配两区域的颜色分布，消除整体色彩偏移。

纹理和谐化在单张 RTX 4090 上约需 1 分钟。

**输入输出流**  
整个流水线的输入是原始网格与用户编辑指令（文本描述或拖拽向量），输出是经过几何与纹理双重无缝融合的编辑后网格。三个模块串行执行，上游模块的输出直接作为下游模块的输入，但编辑效果高度依赖外部二维编辑模型和图像到网格生成模型的输出质量——若上游模型生成的编辑区域网格存在缺陷，融合模块无法从根本上修复其几何或纹理错误。

CraftMesh 将网格编辑重构为“二维图像编辑→三维网格生成→无缝融合”的流水线，其核心由三个模块串联构成，如图2所示。以下聚焦几何融合与纹理和谐化两个关键模块及其数学机制。

### 3.1 编辑区域网格生成

用户对参考图像进行二维编辑后，系统通过图像到网格生成模型（如 Hunyuan3D）将编辑后的参考图提升为三维网格，作为后续融合的编辑参考网格。该模块本身不涉及新公式，但为后续泊松融合提供结构引导。

### 3.2 泊松几何融合

几何融合的目标是将编辑区域网格无缝嵌入原始网格，消除几何不连续。CraftMesh 采用**混合 SDF/Mesh 表示**，在符号距离场域求解泊松方程，通过法向图融合驱动顶点优化。

#### 3.2.1 区域定义

首先将编辑参考网格与原始网格合并，识别交叉顶点集 $V_{in}$，并据此定义两个关键区域：

**合并网格的交叉区域**（Equation 1）：

$$
M_{t}^{in} = \left\{ v \in M_{t} \ \middle| \ \min_{u \in V_{in}} \| u - v \|_{2} < \epsilon_{0} \right\}
$$

**编辑参考网格的交叉区域**（Equation 2）：

$$
M_{e}^{in} = \left\{ v \in M_{e} \ \middle| \ \min_{u \in V_{in}} \| u - v \|_{2} < \epsilon_{0} \right\}
$$

其中 $\epsilon_{0}$ 为距离阈值，用于界定交叉邻域的范围。

为避免过度变形，进一步定义更小的优化子集（Equation 3）：

$$
M_{t}^{opt} = \left\{ v \in M_{t}^{in} \ \middle| \ \min_{u \in V_{in}} \| u - v \|_{2} < \epsilon_{1} \right\}, \quad \epsilon_{1} < \epsilon_{0}
$$

该区域限制了几何优化的作用范围，确保远离交叉边界的原始网格结构不受影响。

#### 3.2.2 法向图泊松融合

核心思想是将三维几何融合问题投影到二维图像域求解。将目标网格法向图 $n_{t}$ 和编辑参考网格法向图 $n_{e}$ 渲染到二维，利用泊松图像编辑算法 $\Gamma(\cdot)$ 在优化区域掩码内进行梯度域融合（Equation 4）：

$$
n_{p} = \Gamma(n_{t}, n_{e}, mask^{opt})
$$

融合后的法向图 $n_{p}$ 在编辑区域保留了编辑参考网格的几何细节，在边界处与原始网格梯度平滑过渡。

#### 3.2.3 优化目标

几何优化的核心损失为**泊松损失**（Equation 5），最小化渲染法向图 $\hat{n}_{t}$ 与融合法向图 $n_{p}$ 之间的 Frobenius 范数差：

$$
\mathcal{L}_{\mathrm{poisson}} = \sum_{i} \| \hat{n}_{t}^{i} - n_{p}^{i} \|_{F}^{2}
$$

总几何融合损失（Equation 6）结合三项约束：

$$
\mathcal{L}_{\mathrm{geo}} = \mathcal{L}_{\mathrm{poisson}} + \lambda_{1} \mathcal{L}_{\mathrm{smooth}} + \lambda_{2} \mathcal{L}_{\mathrm{eik}}
$$

- $\mathcal{L}_{\mathrm{poisson}}$：驱动顶点法向与泊松融合结果对齐；
- $\mathcal{L}_{\mathrm{smooth}}$：平滑正则项，抑制局部噪声；
- $\mathcal{L}_{\mathrm{eik}}$：Eikonal 约束，保证 SDF 表示的符号距离场性质。

**关键设计选择**：将泊松方程求解从三维体积域（复杂度 $O(n^{3})$）转移到二维图像域（复杂度 $O(kn^{2})$），显著降低计算开销。

### 3.3 泊松纹理和谐化

几何融合完成后，编辑区域的纹理需与原始区域协调。泊松纹理和谐化通过三项损失实现无缝色彩过渡。

#### 3.3.1 梯度保持损失

为保留高频纹理细节，约束当前颜色场梯度与原始颜色场梯度一致（Equation 7）：

$$
\mathcal{L}_{\mathrm{grad}} = \mathbf{MSE}\left( \sigma\left( \frac{\nabla C_{new}}{\gamma} \right), \sigma\left( \frac{\nabla C_{new}^{ori}}{\gamma} \right) \right)
$$

其中 $\sigma(\cdot)$ 为 sigmoid 归一化函数，$\gamma$ 为缩放因子。该损失确保编辑区域的纹理模式（如织物纹路、皮肤细节）不被模糊或改变。

#### 3.3.2 边界混合损失

以距离加权方式约束新生成区域的颜色与保留区域接近（Equation 8）：

$$
\mathcal{L}_{\mathrm{boundary}} = \sum_{p_{i}^{new} \in M_{t}^{new}} w_{i} \| C_{new}(p_{i}^{new}) - C_{pr}(p_{i}^{pr}) \|_{2}^{2}
$$

边界权重 $w_{i}$ 根据采样点到最近保留点的欧氏距离计算（Equation 9）：

$$
w_{i} = \left( 1 - \frac{\delta}{\| p_{i}^{new} - p_{i}^{pr} \|_{2}} \right)^{2}
$$

距离越近权重越大，在边界处强制颜色连续，向内则逐渐放松约束，实现软边界过渡。

#### 3.3.3 总损失

纹理和谐化的优化目标整合分布对齐、梯度保持和边界过渡（Equation 10）：

$$
\mathcal{L}_{\mathrm{tex}} = \mathcal{L}_{\mathrm{distribution}} + \theta_{1} \mathcal{L}_{\mathrm{grad}} + \theta_{2} \mathcal{L}_{\mathrm{boundary}}
$$

- $\mathcal{L}_{\mathrm{distribution}}$：颜色分布对齐损失，消除编辑区域与原始区域的整体色彩偏移；
- $\mathcal{L}_{\mathrm{grad}}$：保留高频纹理；
- $\mathcal{L}_{\mathrm{boundary}}$：平滑边界过渡。

消融实验证实三者缺一不可：移除分布损失会降低纹理一致性（Figure 6e），移除梯度损失会损失高频细节（Figure 6f），移除边界损失会引入明显颜色接缝（Figure 6g）。

### 3.4 模块间协同机制

泊松几何融合和泊松纹理和谐化并非独立运作。几何融合为纹理和谐化提供平滑的几何基底，避免纹理映射时的拉伸与错位；纹理和谐化则在几何融合的基础上消除色彩不连续。定量消融（Table 2）表明，几何融合单独使用使 CLIP_sim 从 17.723 提升至 20.502（+2.779），纹理和谐化单独使用提升至 19.399，两者结合达到最优的 20.801，验证了协同效应。

## 实验与关键发现

### 评估设置

CraftMesh 在自建的 **CraftMesh Editing Benchmark** 上进行评估，涵盖文本驱动和拖拽驱动两类编辑任务。评估体系包含四项指标：**CLIP_sim** 衡量编辑结果与目标文本的语义一致性，**CLIP_dir** 衡量编辑方向与文本描述方向的对齐程度，**NIQE** 评估无参考图像质量（越低越好），**NIMA** 评估人类感知的美学质量。所有几何融合实验在单张 NVIDIA RTX 4090 上运行，几何融合约需 5 分钟（1000 次迭代），纹理和谐化约需 1 分钟（2000 次迭代）。

### 与基线方法的定量对比

Table 1 报告了 CraftMesh 与现有方法的全面对比。CraftMesh（Ours-MeshyAI）在所有四项指标上均取得最优结果：

![[assets/figures/papers/paper_list_l2186_https_openaccess_thecvf_com_content_CVPR2026_html_Hu_CraftMesh_High_Fide/figures/004_Table_1.jpg]]
*Table 1: Quantitative comparison with baselines. Our method consistently achieves the best performance across all metrics, demonstrating better semantic consistency and visual quality compared to existing methods*

- **CLIP_sim** 达到 20.801，表明编辑后的网格与目标文本描述具有最强的语义对齐。
- **CLIP_dir** 达到 18.479，说明编辑方向与文本语义方向高度一致。
- **NIQE** 低至 4.710，NIMA 高达 5.928，反映输出渲染图具有优异的视觉质量和美学感知。

相比基于 SDS 的方法（如 **FocalDreamer**，Li et al., AAAI 2024）和基于多视图扩散的方法（如 **CMD**，Li et al., SIGGRAPH 2025），CraftMesh 的优势源于其流水线设计：二维编辑提供了强大的语义控制力，三维生成保证了网格质量，而泊松融合消除了几何与纹理的不连续性。这些方法在直接三维空间中优化时，往往受限于多视角不一致和高计算复杂度，导致语义对齐弱且视觉质量下降。

### 定性对比

Figure 4 的定性对比进一步验证了定量结论。CraftMesh 生成的编辑结果具有和谐的几何结构、精细的局部细节和高保真的色彩过渡。相比之下，基线方法的结果常出现几何结构简单、细节缺失、颜色不一致等问题。例如，在添加衣物的编辑任务中，CraftMesh 能生成自然的褶皱和纹理，而其他方法仅产生模糊的几何凸起和色彩偏移。

![[assets/figures/papers/paper_list_l2186_https_openaccess_thecvf_com_content_CVPR2026_html_Hu_CraftMesh_High_Fide/figures/005_Figure_4.jpg]]
*Figure 4: Qualitative comparisons show that our method produces harmonious geometry structure, intricate local details, and high-fidelity colors, while other methods give simple and inconsistent results*

### 消融实验

Table 2 和 Figure 6 系统地验证了各模块的贡献。

![[assets/figures/papers/paper_list_l2186_https_openaccess_thecvf_com_content_CVPR2026_html_Hu_CraftMesh_High_Fide/figures/009_Figure_6.jpg]]
*Figure 6: Ablation studies. (a,b) Poisson Geometry Blending; (c,d) Poisson Texture Harmonization; (e) the distribution loss; (f) the gradient loss; (g) the boundary loss*

**几何融合的独立贡献**：仅使用 Poisson Geometry Blending 时，CLIP_sim 从无融合流水线的 17.723 提升至 20.502（+2.779），证明 SDF 域的法向泊松融合能有效解决编辑区域与原始网格的几何不连续问题。Figure 6(a,b) 显示，几何融合将生硬的几何接缝转化为具有真实细节（如衣物褶皱）的平滑过渡。

**纹理和谐化的独立贡献**：仅使用 Poisson Texture Harmonization 时，CLIP_sim 从 17.723 提升至 19.399，验证了梯度保持、边界衰减和颜色分布对齐策略的有效性。Figure 6(c,d) 展示纹理和谐化能协调编辑区域与保留区域的色调（如将手部的亮色调与身体的深灰色调统一），并消除纹理边界。

**完整方案的协同效果**：结合几何融合与纹理和谐化的完整方案取得最佳 CLIP_sim 20.801，表明两者具有互补性——几何融合提供结构基础，纹理和谐化在此基础上实现视觉一致性。

**纹理损失项的消融**：Figure 6(e-g) 分别展示了移除各损失项的影响。移除分布损失（distribution loss）会降低纹理一致性，导致编辑区域与原始区域的颜色分布不匹配；移除梯度损失（gradient loss）会损失高频纹理细节，使表面变得模糊；移除边界损失（boundary loss）会在融合边界引入明显的颜色接缝。

### 拖拽式编辑的适配性

Figure 5 展示了 CraftMesh 对拖拽式网格编辑的有效适配。用户通过指定拖拽控制点，框架能够实现精确且直观的几何操作。这验证了“图像编辑→网格生成→无缝融合”流水线的通用性——拖拽操作在二维图像空间中完成，随后通过网格生成和无缝融合迁移到三维网格，无需针对拖拽任务重新设计三维优化策略。

![[assets/figures/papers/paper_list_l2186_https_openaccess_thecvf_com_content_CVPR2026_html_Hu_CraftMesh_High_Fide/figures/007_Figure_5.jpg]]
*Figure 5: Our method effectively adapts to drag-based mesh editing, enabling precise and intuitive geometry manipulation through user-specified drag controls. (a) shows the original mesh, with arrows drawn to signify drag; (b) shows the editing results*

### 计算效率分析

CraftMesh 将泊松融合的计算域从三维体积（复杂度 O(n³)）降至二维图像域（复杂度 O(kn²)），这是实现实用化编辑时间的关键设计。几何融合约 5 分钟、纹理和谐化约 1 分钟的总耗时虽非实时，但远低于直接在三维空间求解泊松方程或进行 SDS 优化的开销，使方法具备实际应用价值。

### 失败模式与局限性

尽管 CraftMesh 在多数编辑任务中表现优异，实验揭示了若干局限性：

1. **上游模型依赖性**：编辑效果高度依赖二维图像编辑模型和三维网格生成模型（如 Hunyuan3D）的输出质量。若上游模型生成质量不佳，融合结果会继承这些缺陷，这是流水线设计的固有风险。
2. **全局结构变形能力有限**：泊松融合主要解决局部几何与纹理的连续性，对于涉及大幅全局结构变形的编辑任务（如改变物体整体比例或姿态）可能无法胜任，因为融合策略假设编辑区域与原始网格在拓扑上具有对应关系。
3. **非实时性能**：约 6 分钟的总处理时间限制了在交互式创作场景中的直接应用，需要进一步优化泊松求解效率或探索更轻量的融合策略。
4. **表示局限性**：当前方法仅针对显式网格表示设计，未验证对神经辐射场（NeRF）、3D 高斯泼溅（3DGS）等其他三维表示的支持，限制了框架的适用范围。

![[assets/figures/papers/paper_list_l2186_https_openaccess_thecvf_com_content_CVPR2026_html_Hu_CraftMesh_High_Fide/figures/001_Figure_1.jpg]]
*Figure 1: Mesh editing results produced by CraftMesh. CraftMesh is a versatile 3D mesh editing framework that enables users to perform text-based and drag-based editing, and delivers high-quality outputs even in challenging editing scenarios*

## 定位与知识库关联

### 1. 与现有工作的关系

CraftMesh 的核心思路是将网格编辑重构为“图像编辑 → 3D 网格生成 → 无缝融合”的流水线，这与当前主流的直接 3D 编辑范式形成了明确的对比。理解这一差异，是定位该方法在知识谱系中位置的关键。

**与基于 SDS 优化的方法对比。** 以 **FocalDreamer**（Li et al., AAAI 2024）和 **MagicClay** 为代表，这类方法直接在 3D 表示上通过分数蒸馏采样（SDS）进行优化。其因果瓶颈在于：SDS 的梯度信号来自 2D 扩散模型的多视角随机采样，天然存在多视角不一致性，导致编辑结果几何结构简单、纹理模糊，且难以保留原始网格的精细细节。CraftMesh 避开了这一瓶颈——它将编辑控制权交给成熟的 2D 图像编辑模型，将 3D 生成交给专用的图像到网格生成模型（如 Hunyuan3D），仅在最后的融合阶段介入 3D 优化，从而在语义一致性和视觉质量上取得了显著优势（Table 1 中 CLIP_sim 和 NIMA 均最优）。

**与基于多视图扩散的方法对比。** **CMD**（Li et al., SIGGRAPH 2025）和 **Instant3dit** 通过微调多视图扩散模型来实现 3D 编辑，试图缓解 SDS 的多视角不一致问题。然而，这类方法仍受限于扩散模型对复杂几何编辑的建模能力，且计算开销较大。CraftMesh 的融合流水线不依赖多视图扩散的一致性，而是通过泊松方程在梯度域直接约束几何与纹理的平滑过渡，从根本上绕开了多视角一致性的难题。

**与坐标域泊松编辑的对比。** 传统泊松网格编辑在 3D 坐标域直接求解泊松方程，计算复杂度为 $O(n^3)$，难以处理高分辨率网格。CraftMesh 的关键创新在于将泊松融合迁移到 2D 图像域——通过渲染法向图并在 2D 上进行泊松编辑，将复杂度降至 $O(kn^2)$，同时利用混合 SDF/Mesh 表示保持几何精度。这一“降维求解”策略是方法得以实用化的关键因果 knob。

### 2. 适用边界

CraftMesh 的设计决定了其适用范围存在明确的边界条件：

- **编辑类型边界。** 方法擅长局部几何与纹理的编辑（如添加配饰、替换部件、纹理调整），因为泊松融合的核心能力在于保证编辑区域与保留区域之间的平滑过渡。对于涉及大幅全局结构变形的任务（如改变物体整体比例、大幅度姿态变换），泊松融合无法提供足够的变形自由度，编辑效果可能不理想。

- **上游模型依赖。** 编辑质量高度依赖外部 2D 图像编辑模型和 3D 网格生成模型的性能。若上游图像编辑未能准确响应用户指令，或图像到网格生成模型输出的几何质量较差，融合阶段无法弥补这些缺陷。这是一个需要手动验证的环节——实际部署时应根据任务选择合适的 2D/3D 生成模型。

- **表示形式限制。** 当前方法仅针对显式网格表示设计，未探讨对神经辐射场（NeRF）、3D 高斯泼溅（3DGS）等其他三维表示的支持。对于以这些表示为输出的生成流水线，需要额外的转换步骤。

- **计算效率边界。** 几何融合约需 5 分钟（单张 RTX 4090，1000 次迭代），纹理和谐化约需 1 分钟（2000 次迭代），总计约 6 分钟的处理时间使其难以直接应用于实时交互式创作场景。

### 3. 局限与开放问题

基于上述分析，CraftMesh 存在以下局限和值得探索的方向：

**已确认的局限：**

1. **上游模型瓶颈。** 编辑效果高度依赖 2D 编辑和 3D 网格生成模型的质量，若上游输出不佳，融合结果会直接受影响。
2. **全局变形能力不足。** 泊松融合主要解决局部几何与纹理的连续性，对大幅全局结构变形的编辑任务可能无法胜任。
3. **非实时性能。** 约 6 分钟的总处理时间限制了交互式应用场景。
4. **表示形式单一。** 仅支持显式网格，未覆盖 NeRF、3DGS 等表示。

**开放问题：**

- **更复杂的网格编辑技术。** 未来工作可探索结合物理仿真、骨架驱动变形或更高级的语义控制，以扩展编辑能力的边界。
- **动态与场景级编辑。** 能否将框架拓展至动态网格序列或场景级编辑，实现时空一致的编辑效果？这需要解决跨帧一致性和更大规模融合的问题。
- **实时化方向。** 如何进一步降低泊松融合的计算开销？可能的路径包括更高效的泊松求解器、神经加速方法，或将部分优化过程前移。
- **多表示泛化。** 将泊松融合的思想迁移到 NeRF 或 3DGS 表示中，需要重新设计梯度域约束的形式，这是一个非平凡的理论问题。

## 原文 PDF

![[paperPDFs/CVPR_2026/CraftMesh_High_Fidelity_Generative_Mesh_Manipulation_via_Poisson_Seamless_Fusion.pdf]]
