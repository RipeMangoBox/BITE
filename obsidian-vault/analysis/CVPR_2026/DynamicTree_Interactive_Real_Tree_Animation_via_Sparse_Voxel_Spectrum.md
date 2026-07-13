---
title: "DynamicTree: Interactive Real Tree Animation via Sparse Voxel Spectrum"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/DynamicTree_Interactive_Real_Tree_Animation_via_Sparse_Voxel_Spectrum.pdf
project_link: "https://dynamictree-dev.github.io/DynamicTree.github.io/"
code_link: null
aliases:
- DynamicTree
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 将树木运动表示为稀疏体素频谱——先用体素化压缩空间维度，再沿时间维度做傅里叶变换并仅保留前 K 个频率成分。这种表示同时解决了效率（数据量极大减少）、一致性（频域约束天然保证长期运动）和域差距（体素结构统一了拓扑）三大痛点。
primary_logic: 树木运动本质上是准周期性谐波振荡的叠加，因此在频域具有高度稀疏性；将其与空间稀疏性（体素化）结合，可形成一个极紧凑的 3D 运动表示，既能用扩散模型高效生成，又能直接作为模态基底用于实时的物理交互。
claims:
- 在真实树木 4D 动画任务上，CLIP-I、CLIP-T 和用户偏好 (MA) 均大幅优于 4DGen 和 SV4D 2.0。
- 模拟时间仅 18.22 ms/帧，比 PhysGaussian (1800 ms/帧) 和 PhysFlow (15600 ms/帧) 快近两个数量级，真正实现实时交互。
- 消融实验表明，稀疏体素频谱加上局部频谱平滑损失和两阶段训练是生成无发散、长期一致运动的关键。
- 用户研究中，我们的方法在运动真实感上以 57.86% 的偏好显著超过传统树动画方法 Weber (42.14%)。
---

# DynamicTree: Interactive Real Tree Animation via Sparse Voxel Spectrum

> [!tip] 核心洞察
> 树木运动本质上是准周期性谐波振荡的叠加，因此在频域具有高度稀疏性；将其与空间稀疏性（体素化）结合，可形成一个极紧凑的 3D 运动表示，既能用扩散模型高效生成，又能直接作为模态基底用于实时的物理交互。

| 字段 | 内容 |
|------|------|
| 中文题名 | DynamicTree：基于稀疏体素频谱的交互式真实树木动画 |
| 英文题名 | DynamicTree: Interactive Real Tree Animation via Sparse Voxel Spectrum |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2510.22213) · [Project](https://dynamictree-dev.github.io/DynamicTree.github.io/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | DynamicTree |
| Dataset | 真实树木3D动画 |

> [!tip] 效果简介
> - 真实树木3D动画 (Real-tree 3D Animation) 上，CLIP-I↓ 0.0052 vs 4DGen: 0.0103 (-0.0051)；CLIP-T↓ 0.0021 vs 4DGen: 0.0094 (-0.0073)；用户偏好 MA↑ 93.7% vs 4DGen: 2.1% (+91.6%)。
> - 交互式物理模拟 (Interactive Simulation) 上，仿真时间 (ms/frame)↓ 18.22 vs PhysGaussian: 1800 (降低约99%)；仿真时间 (ms/frame)↓ 18.22 vs PhysFlow: 15600 (降低约99.9%)。
> - 树木动画用户偏好 (User Preference vs Traditional) 上，总体偏好↑ 57.86% vs Weber: 42.14% (+15.72%)。

## 概要

真实树木的 4D 动画生成长期面临三大结构性瓶颈：**(1)** 基于物理模拟或视频扩散模型的现有方法计算开销巨大，无法实现实时交互；**(2)** 直接预测海量高斯体的长序列运动在内存与数据层面均不可行；**(3)** 合成训练数据与真实场景的 3DGS 重建之间存在域差距，导致运动失真。DynamicTree 的核心洞察在于：**树木运动本质上是准周期性谐波振荡的叠加，在频域具有高度稀疏性**。将这一特性与空间稀疏化（体素化）相结合，即可构建一个极紧凑的 3D 运动表示——**稀疏体素频谱**（Sparse Voxel Spectrum）。

该方法的关键因果机制是：先对网格运动序列沿时间维度做傅里叶变换，仅保留前 $K$ 个频率成分，再用体素化压缩空间维度。这一表示同时解决了效率（数据量急剧减少）、长期一致性（频域约束天然保证运动不发散）和域差距（体素结构统一了合成与真实数据的拓扑）三大痛点。在此基础上，DynamicTree 采用两阶段流水线：首先用稀疏体素扩散模型生成网格运动，再通过 GaMeS 表面绑定将变形传递至 3DGS 高斯体，实现从静态重建到 4D 动画的端到端生成。

实验结果表明，在真实树木 3D 动画任务上，DynamicTree 的 CLIP-I（0.0052）和 CLIP-T（0.0021）大幅优于 **4DGen**（Yin et al., arXiv 2023）与 **SV4D 2.0**（Yao et al., arXiv 2025），用户偏好率高达 93.7%。在交互式物理模拟方面，仿真时间仅 18.22 ms/帧，比 **PhysGaussian**（Xie et al., CVPR 2024）快约 99%，比 **PhysFlow**（Liu et al., CVPR 2025）快约 99.9%，真正实现了实时交互。用户研究进一步表明，该方法在运动真实感上以 57.86% 的偏好显著超过传统树木动画方法 **Weber**（Weber and Penn, SIGGRAPH 1995）的 42.14%。消融实验证实，稀疏体素频谱配合局部频谱平滑损失与两阶段训练策略，是生成无发散、长期一致运动的关键设计。

真实树木是自然界中最常见且动态细节最丰富的物体之一。在数字孪生、影视特效、游戏与虚拟现实等应用中，生成结构一致、长期连贯且可实时交互的树木动画是一项长期挑战。然而，现有方法在效率、质量和交互性三个维度上始终难以兼得。

### 核心瓶颈

真实树木 4D 动画生成面临三个相互关联的难题，构成了当前技术路线的主要瓶颈：

**计算效率瓶颈。** 基于物理模拟的方法需要求解复杂的偏微分方程或进行大规模粒子动力学计算，计算开销极高。例如，**PhysGaussian** (Xie et al., CVPR 2024) 单帧模拟耗时约 1800 ms，而 **PhysFlow** (Liu et al., CVPR 2025) 更是高达 15600 ms/帧，完全无法满足实时交互需求。另一方面，基于视频扩散模型的 4D 生成方法（如 **4DGen** (Yin et al., arXiv 2023) 和 **SV4D 2.0** (Yao et al., arXiv 2025)）虽然避开了显式物理求解，但扩散采样的迭代特性同样使其难以实时运行。

**数据规模瓶颈。** 直接预测大量高斯体的长序列运动参数在内存和数据层面均不可行。一棵真实树木的 3DGS 重建通常包含数万乃至数十万个高斯体，每个高斯体每帧需要预测位置、旋转、尺度等变形参数。对于 T 帧的动画序列，直接输出的数据量呈 $O(H \times T)$ 增长，其中 $H$ 为高斯体数量。这种高维输出空间使生成模型的训练和推理都面临严重的可扩展性问题。

**域差距瓶颈。** 现有 4D 生成方法通常在合成数据上训练，而合成树木的运动模式、几何细节与真实扫描的 3DGS 重建之间存在显著的域差距。直接将合成数据训练的模型应用于真实场景，往往导致运动失真、结构崩塌或长期发散。这一域差距在树木这种具有复杂分枝拓扑的物体上尤为突出。

### 核心洞察与动机

本文的核心洞察源于对树木运动本质的重新审视：**树木在风力等外力作用下的运动本质上是准周期性谐波振荡的叠加**。这一物理特性意味着，树木的运动在频域具有高度稀疏性——仅需少量频率成分即可近乎完整地刻画其长期动态。将这一频域稀疏性与空间稀疏性（体素化）相结合，可以构造一个极紧凑的 3D 运动表示，同时解决上述三大瓶颈：

- **效率**：紧凑的频域表示将数据量从 $O(H \times T)$ 压缩至 $O(K \times V)$，其中 $K \ll T$ 为保留的频率成分数，$V$ 为体素数量，使扩散模型的生成和后续模态求解均能实时完成。
- **一致性**：频域约束天然保证了生成运动的长期周期性和时间连贯性，避免了逐帧预测方法常见的运动发散问题。
- **域适应**：体素化的网格结构统一了合成数据与真实扫描的拓扑表达，有效弥合了域差距。

基于这一洞察，本文提出 **DynamicTree** 框架，将树木运动表示为**稀疏体素频谱**——先用体素化压缩空间维度，再沿时间维度做傅里叶变换并仅保留前 $K$ 个频率成分。该表示既是扩散模型的高效生成目标，又可作为模态基底直接用于实时物理交互，从而首次实现了真实树木 4D 动画的“生成-交互”闭环。

## 核心方法与创新机理

DynamicTree 的核心创新在于将真实树木 4D 动画的生成与交互统一到一个极紧凑的表示下——**稀疏体素频谱**。这一表示从三个 changed slots 上根本性地改变了现有方法的设计范式。

### 1. 运动表示：从密集顶点位移到稀疏体素频谱

现有 4D 生成方法（如 **4DGen** (Yin et al., arXiv 2023)、**SV4D 2.0** (Yao et al., arXiv 2025)）和物理模拟方法（如 **PhysGaussian** (Xie et al., CVPR 2024)、**PhysFlow** (Liu et al., CVPR 2025)）均以密集顶点位移序列或逐高斯变形参数表示运动，这导致两个根本瓶颈：（1）直接预测大量高斯体的长序列运动在内存和数据上不可行；（2）逐帧独立预测缺乏对长期时间一致性的结构约束。

DynamicTree 的解决方案是将树木运动表示为**稀疏体素频谱**（§3.2）。具体而言，先从多视角图像重建树木网格并体素化为空间稀疏的体素网格，再沿时间维度对每个体素的运动轨迹做傅里叶变换，仅保留前 $K$ 个频率成分（消融实验表明 $K=16$ 即可近乎无损重建完整频谱）。这一表示将运动数据量压缩数个数量级，同时频域约束天然保证了长期运动的周期一致性与结构稳定性。

### 2. 训练损失与策略：从单一扩散损失到两阶段频谱平滑

仅使用标准扩散损失 $\mathcal{L}_{DM}$ 训练时，生成的体素频谱在相邻体素间缺乏约束，导致重建出的网格运动出现**分支发散**等不真实现象（Figure 5 第 2 列）。为解决此问题，DynamicTree 引入**局部频谱平滑损失** $\mathcal{L}_{LSS}$：

$$\mathcal{L}_{\mathrm{LSS}} = \frac{1}{N} \sum_{i=1}^{N} \sum_{j \in \mathcal{N}(i)} e^{-\alpha d_{ij}} \left( \Vert \mathbf{Re}_i - \mathbf{Re}_j \Vert + \lambda \Vert \mathrm{Im}_i - \mathrm{Im}_j \Vert \right)$$

该损失约束相邻体素在频域的实部与虚部相似，从而鼓励局部运动的一致性。但直接联合训练 $\mathcal{L}_{DM}$ 和 $\mathcal{L}_{LSS}$ 仍会导致训练不稳定。DynamicTree 的关键策略是采用**两阶段训练**（§3.5）：第一阶段仅用 $\mathcal{L}_{DM}$ 训练扩散模型学习频谱分布；第二阶段引入 $\mathcal{L}_{LSS}$ 对频谱进行局部平滑精炼。消融实验（Figure 5, Table 3）证实，这一设计是生成无发散、长期一致运动的关键。

### 3. 高斯变形驱动：从直接预测到网格表面绑定

现有 3DGS 动画方法通常直接预测每个高斯体的变形参数（位置、旋转、尺度），这不仅参数量巨大，且容易产生高斯体脱离物体表面的伪影。DynamicTree 采用 **GaMeS 表面绑定**（§3.6），通过网格面片的顶点位置重新参数化高斯体的中心、旋转和尺度：

$$\mu = \alpha_1 V_1 + \alpha_2 V_2 + \alpha_3 V_3,\quad r = [r_1(f_i), r_2(f_i), r_3(f_i)],\quad s = \mathrm{diag}(s_1(f_i), s_2(f_i), s_3(f_i))$$

这一设计的因果机制在于：网格作为拓扑一致的中间表示，既弥合了合成训练数据与真实 3DGS 重建之间的域差距，又使得频域生成的网格运动可以忠实地传递到高斯体上，保证了渲染质量与运动一致性。

### 4. 交互模态：从重仿真到模态叠加

传统物理模拟方法（如 PhysGaussian 需 1800 ms/帧，PhysFlow 需 15600 ms/帧）每帧都需要重新求解完整的物理方程，无法实时交互。DynamicTree 将生成的频谱直接作为**模态基底**，利用模态叠加实时响应外力：

$$\mathcal{D}(t) = \sum_{k=1}^K \phi_k \cdot q^k(t)$$

这使交互仿真时间降至 **18.22 ms/帧**，比 PhysGaussian 快近两个数量级，真正实现了实时交互。这一能力源于核心表示的巧妙设计——生成阶段产出的频谱天然就是模态分解的结果，无需额外计算。

DynamicTree 采用**两阶段流水线**将静态 3DGS 树木转化为可实时交互的 4D 动画资产，其核心设计围绕一个关键洞察展开：树木运动本质上是准周期性谐波振荡的叠加，在频域具有高度稀疏性。将这一特性与空间稀疏性（体素化）结合，可形成极紧凑的 3D 运动表示，既能用扩散模型高效生成，又能直接作为模态基底用于实时物理交互。

### 流水线总览

整个框架如 Figure 2 所示，分为两个阶段：

![[assets/figures/papers/paper_list_l1060_https_arxiv_org_abs_2510_22213/figures/002_Figure_2.jpg]]
*Figure 2: Our framework animates 3DGS trees in two stages: (1) spectrum-based motion generation in the frequency domain, and (2) deformation transfer to 3DGS through mesh binding. In the first stage, we extract the tree mesh from multi-view images, voxelize it, and encode it into a sparse voxel latent condition. A sparse voxel diffusion model then generates a compact motion representation*

**第一阶段：基于频谱的运动生成。** 从多视角图像出发，首先重建树木网格并对其进行体素化，得到稀疏体素网格条件。随后，一个稀疏体素扩散 U-Net 以该体素条件和频率索引为引导，通过去噪扩散过程生成紧凑的**稀疏体素频谱** $\mathcal{S}$——仅保留前 $K$ 个频率成分。这一表示通过逆傅里叶变换和去体素化操作，即可重建出完整的网格顶点运动序列 $\mathcal{D}_m = \mathrm{Dev}(\mathrm{iFFT}(\mathcal{S}))$。

**第二阶段：网格驱动的 3DGS 动画。** 将 3DGS 高斯体通过 GaMeS 参数化绑定到网格表面，使高斯体的中心、旋转和尺度由对应面片的顶点位置驱动。当网格按第一阶段生成的运动序列变形时，绑定其上的高斯体随之产生一致的动画效果，输出完整的 4D 高斯序列 $\mathcal{G} = \{ G_t \mid G_t = \{ x_i^t, r_i^t, s_i^t, \sigma_i^t, c_i^t \}_{i=1}^{H} \}_{t=0}^{T}$。

### 模块构成与数据流

框架可细化为六个功能模块，形成端到端的数据流：

| 模块 | 功能 | 输入 → 输出 |
|------|------|-------------|
| **Voxel Grid Condition Extraction** | 从多视角图像重建网格并体素化 | 多视角图像 → 体素网格条件 |
| **Sparse Voxel Encoder** | 使用稀疏卷积将体素网格编码为紧凑潜在表示 | 体素网格 → 潜在编码 $g$ |
| **Sparse Voxel Diffusion U-Net** | 基于体素条件和频率索引，通过去噪扩散生成稀疏体素频谱 | $(g, f)$ → 稀疏体素频谱 $\mathcal{S}$ |
| **Devoxelization & Inverse FFT** | 将频谱解码为密集网格运动序列 | $\mathcal{S}$ → 网格运动 $\mathcal{D}_m$ |
| **Mesh-Driven 3DGS Animation** | 通过 GaMeS 绑定将网格运动传递到高斯体 | $(\mathcal{D}_m, \text{3DGS})$ → 4D 高斯序列 |
| **Modal Analysis Interaction** | 利用频谱作为模态基底，实时求解模态方程响应外力 | $(\mathcal{S}, \mathbf{f}(t))$ → 交互形变 $\mathcal{D}(t)$ |

### 设计决策与关键机制

**稀疏体素频谱表示**是整个框架的“因果旋钮”，同时解决了三个核心瓶颈：
1. **效率**：体素化压缩空间维度，傅里叶变换后仅保留前 $K$ 个频率成分，数据量极大减少；
2. **一致性**：频域约束天然保证长期运动的谐波一致性，避免逐帧预测的累积漂移；
3. **域差距**：体素结构统一了合成训练数据与真实 3DGS 重建的拓扑表达，弥合了两者间的鸿沟。

**训练策略**采用两阶段方案：第一阶段仅使用扩散损失 $\mathcal{L}_{DM}$ 训练，使模型学会生成合理的频谱分布；第二阶段引入局部频谱平滑损失 $\mathcal{L}_{LSS}$，约束相邻体素的频谱实部与虚部相似，从而鼓励局部运动一致性。消融实验（Figure 5）证实，直接联合训练两损失或仅用 $\mathcal{L}_{DM}$ 均会导致分支发散等不真实运动，而两阶段训练是生成无发散、长期一致运动的关键。

**高斯变形驱动**未采用直接预测每个高斯体变形参数的方式，而是通过网格表面绑定（GaMeS）间接驱动。这一设计使得高斯的运动继承自网格的物理一致性，避免了大量高斯体独立预测带来的内存和稳定性问题。

### 交互能力

生成的稀疏体素频谱不仅用于离线动画，还直接作为模态基底支撑实时交互。当用户施加外力 $\mathbf{f}(t)$ 时，系统将树木网格视为质量-弹簧-阻尼系统，利用预计算的模态形状 $\phi_k$ 和实时求解的模态坐标 $q^k(t)$ 合成动态响应：

$$\mathcal{D}(t) = \sum_{k=1}^K \phi_k \cdot q^k(t)$$

这使得 DynamicTree 在单帧仿真仅需约 18 ms（其中网格运动计算 13 ms、高斯变形计算 2.57 ms、渲染 2.65 ms），真正实现了实时交互。

### 4D 动画生成的整体范式

DynamicTree 将真实树木 4D 动画生成形式化为一个两阶段流水线（Figure 2）：**第一阶段**在频域生成网格运动，**第二阶段**通过网格表面绑定将变形传递到 3DGS 高斯体。这一设计的关键动机在于——直接预测海量高斯体（$H$ 个）在长序列（$T$ 帧）上的变形参数 $\bar{\mathcal{D}}_g$ 在内存和数据层面均不可行，因此必须寻找一种紧凑的中间运动表示。

待生成的 4D 模型可表示为高斯体序列：

$$\mathcal{G} = \{ G_t \mid G_t = \{ x_i^t, r_i^t, s_i^t, \sigma_i^t, c_i^t \}_{i=1}^{H} \}_{t=0}^{T}$$

其中每帧 $G_t$ 包含全部高斯体的位置 $x_i^t \in \mathbb{R}^3$、旋转 $r_i^t \in \mathbb{R}^4$、尺度 $s_i^t \in \mathbb{R}^3$、不透明度 $\sigma_i^t$ 和颜色 $c_i^t$。若直接预测这些参数的时间变形 $\bar{\mathcal{D}}_g = \{ (\Delta x_i^t, \Delta r_i^t, \Delta s_i^t) \}_{i=1, t=1}^{H, T}$，数据维度将随 $H$ 和 $T$ 线性膨胀，使长序列生成在计算上难以承受。

### 稀疏体素频谱：核心运动表示

该方法的核心创新在于将树木运动压缩为**稀疏体素频谱**（Sparse Voxel Spectrum）。其设计逻辑遵循两条观察：

1. **空间稀疏性**：树木的几何结构在 3D 空间中高度稀疏，大量空白区域无需显式建模运动。通过体素化将网格顶点运动聚合到离散体素网格上，可大幅压缩空间维度。
2. **频域稀疏性**：树木运动本质上是准周期性谐波振荡的叠加（如微风下的枝干摆动），在频域中仅少数低频成分承载了绝大部分运动能量。沿时间维度做傅里叶变换后，仅保留前 $K$ 个频率成分即可近乎无损地重建完整运动——论文验证 $K=16$ 已足够，与 Generative-Dynamics 的结论一致。

最终的运动重建通过逆傅里叶变换和去体素化完成：

$$\mathcal{D}_m = \mathrm{Dev}(\mathrm{iFFT}(\mathcal{S}))$$

其中 $\mathcal{S}$ 为扩散模型生成的稀疏体素频谱，$\mathcal{D}_m$ 为重建的密集网格顶点运动序列。这一表示将原始运动数据量压缩了数个数量级，使得扩散模型能够在可承受的计算预算内生成长期（$T$ 可达数百帧）且时序一致的 4D 运动。

### 稀疏体素扩散模型

运动生成模块构建于 **XCube**（Ren et al.）的稀疏体素 U-Net 架构之上。其输入条件包含两部分：

- **体素网格条件**：从多视角图像重建树木网格，经体素化后由稀疏卷积编码器压缩为紧凑潜在表示 $g$。
- **频率索引 $f$**：显式告知扩散模型当前去噪步骤对应的频率分量，使模型能够逐频率生成频谱。

扩散模型在去噪过程中学习预测噪声 $\epsilon_\theta$，训练目标为标准的扩散损失：

$$\mathcal{L}_{DM} = \mathbb{E}_{\epsilon \sim \mathcal{N}(0,I),\, l \sim \mathcal{U}(\{1,\dots,L\})} \left[ \Vert \epsilon - \epsilon_{\theta}(\mathbf{s}_l; l, g, f) \Vert^2 \right]$$

其中 $\mathbf{s}_l$ 为在时间步 $l$ 加噪后的频谱，$L$ 为总扩散步数。条件 $g$ 提供树木的静态几何信息，$f$ 提供频域位置信息，二者共同引导扩散过程生成与输入树木结构相匹配的频谱。

### 局部频谱平滑损失与两阶段训练

仅使用 $\mathcal{L}_{DM}$ 训练会导致生成的运动出现分支发散等不真实伪影（Figure 5 第 2 列）。根本原因在于：扩散损失仅在像素/体素级监督频谱重建精度，缺乏对**局部运动一致性**的显式约束——相邻体素在物理上应具有相似的振荡模式（相近的频率、振幅和相位），但扩散模型可能为相邻体素生成差异显著的频谱。

![[assets/figures/papers/paper_list_l1060_https_arxiv_org_abs_2510_22213/figures/008_Figure_5.jpg]]
*Figure 5: Ablation of training strategies. Columns 2–4 show the middle frame of sequences generated by each strategy*

为解决此问题，论文引入**局部频谱平滑损失**（Local Spectrum Smoothness, $\mathcal{L}_{LSS}$）：

$$\mathcal{L}_{\mathrm{LSS}} = \frac{1}{N} \sum_{i=1}^{N} \sum_{j \in \mathcal{N}(i)} e^{-\alpha d_{ij}} \left( \Vert \mathbf{Re}_i - \mathbf{Re}_j \Vert + \lambda \Vert \mathrm{Im}_i - \mathrm{Im}_j \Vert \right)$$

其中 $\mathcal{N}(i)$ 为体素 $i$ 的空间邻域，$d_{ij}$ 为体素间距离，$\alpha$ 控制距离衰减速率，$\lambda$ 平衡实部和虚部的权重。该损失惩罚相邻体素在频谱实部 $\mathbf{Re}$ 和虚部 $\mathrm{Im}$ 上的差异，从而鼓励局部区域内的运动模式平滑过渡。

训练策略上，直接联合优化 $\mathcal{L}_{DM}$ 和 $\mathcal{L}_{LSS}$ 仍会导致训练不稳定。论文采用**两阶段训练**：第一阶段仅使用 $\mathcal{L}_{DM}$ 训练若干迭代，使模型先学会生成合理的频谱分布；第二阶段引入 $\mathcal{L}_{LSS}$ 进行精调，消除局部不一致性。消融实验（Figure 5）证实，两阶段策略是获得无发散、细节丰富运动的关键。

### 网格驱动的 3DGS 动画

第二阶段将生成的网格运动传递到 3DGS 高斯体。论文采用 **GaMeS**（Waczyńska et al.）参数化方法，将每个高斯体绑定到网格面片上：

$$\mu = \alpha_1 V_1 + \alpha_2 V_2 + \alpha_3 V_3,\quad r = [r_1(f_i), r_2(f_i), r_3(f_i)],\quad s = \mathrm{diag}(s_1(f_i), s_2(f_i), s_3(f_i))$$

其中 $\mu$ 为高斯中心（由面片顶点 $V_1, V_2, V_3$ 的重心坐标插值得到），$r$ 和 $s$ 分别为旋转和尺度（由面片 $f_i$ 的局部几何参数化）。当网格顶点随 $\mathcal{D}_m$ 变形时，绑定在其上的高斯体自动跟随运动，无需逐帧预测每个高斯的独立变形参数。这种绑定机制同时保证了渲染质量（高斯体始终贴合表面）和运动一致性（高斯体间不会出现相对漂移）。

### 模态分析驱动的实时交互

生成的频谱 $\mathcal{S}$ 不仅用于动画生成，还直接作为**模态基底**支持实时物理交互。论文将树木网格建模为质量-弹簧-阻尼系统，其运动方程为标准二阶动力学形式：

$$M \ddot{d}(t) + C \dot{\mathbf{d}}(t) + K \mathbf{d}(t) = \mathbf{f}(t)$$

其中 $M, C, K$ 分别为质量、阻尼和刚度矩阵，$\mathbf{f}(t)$ 为外部时变力（如拖拽力）。利用预计算的模态形状 $\phi_k$（从生成频谱中提取），可将耦合的大规模动力学方程解耦为 $K$ 个独立的单自由度方程，实时求解模态坐标 $q^k(t)$ 后通过模态叠加得到交互形变：

$$\mathcal{D}(t) = \sum_{k=1}^K \phi_k \cdot q^k(t)$$

此过程每帧仅需约 13 ms 的网格运动计算，加上高斯变形计算（2.57 ms）和渲染（2.65 ms），总计约 18.22 ms/帧，真正实现了实时交互（对比 PhysGaussian 的 1800 ms/帧和 PhysFlow 的 15600 ms/帧）。

## 实验与关键发现

### 实验设置

**数据集**。方法训练使用自建的 **4DTree** 合成数据集（Figure 6），包含多种树种的物理模拟动画。测试评估在真实拍摄的树木场景上进行：先从多视角图像重建静态 3DGS，再以该重建作为输入生成 4D 动画序列。合成训练数据与真实重建之间存在域差距，体素化表示被设计用于弥合这一差距。

**评估协议**。
- *3D 动画质量*：采用 CLIP-I（图像一致性）和 CLIP-T（文本一致性）度量生成序列与输入条件的对齐程度，同时通过两两对比的用户偏好研究（运动真实感 MA）进行主观评价。
- *交互仿真效率*：记录每帧仿真时间（ms/frame），与基于物理的 3DGS 模拟方法对比。
- *与传统方法对比*：通过用户偏好研究将 DynamicTree 与经典树木动画方法 **Weber**（Weber and Penn, SIGGRAPH 1995）进行对比。

**对比方法**。涵盖三类基线：
- 4D 生成方法：**4DGen**（Yin et al., arXiv 2023）、**SV4D 2.0**（Yao et al., arXiv 2025）
- 基于物理的 3DGS 模拟：**PhysGaussian**（Xie et al., CVPR 2024）、**PhysFlow**（Liu et al., CVPR 2025）
- 传统树木动画：**Weber**（Weber and Penn, SIGGRAPH 1995）

所有方法使用相同的真实树木 3DGS 重建作为输入，交互仿真中施加相同的外部拖拽力，保证公平比较。

---

### 主要结果

#### 3D 动画质量

Table 1（上部分）报告了真实树木 3D 动画的定量对比。DynamicTree 在所有指标上显著优于 4D 生成基线：

![[assets/figures/papers/paper_list_l1060_https_arxiv_org_abs_2510_22213/figures/004_Table_1.jpg]]
*Table 1: Quantitative comparison of our method and other methods. The upper part is a comparison of 3D animation, and the lower part is a comparison of interactive simulation*

| 方法 | CLIP-I ↓ | CLIP-T ↓ | 用户偏好 MA ↑ |
|------|----------|----------|----------------|
| 4DGen | 0.0103 | 0.0094 | 2.1% |
| SV4D 2.0 | 0.0081 | 0.0057 | 4.2% |
| **DynamicTree** | **0.0052** | **0.0021** | **93.7%** |

- CLIP-I 较 4DGen 降低 **49.5%**（0.0052 vs. 0.0103），表明生成序列更好地保持了与输入条件的图像一致性。
- CLIP-T 较 4DGen 降低 **77.7%**（0.0021 vs. 0.0094），文本对齐度优势更为显著。
- 用户偏好中，DynamicTree 以 **93.7%** 的压倒性优势被选为运动更真实的方法，而 4DGen 仅获 2.1%。

**定性分析**（Figure 3）：4DGen 和 SV4D 2.0 生成的动画序列在中帧出现明显的 3D 结构退化，时空切片显示运动缺乏长期一致性。DynamicTree 得益于频域表示的天然周期约束，在保持树枝拓扑结构的同时产生自然振荡运动。

#### 交互仿真效率

Table 1（下部分）揭示了 DynamicTree 在仿真效率上的数量级优势：

| 方法 | 仿真时间 (ms/frame) |
|------|---------------------|
| PhysFlow | 15600 |
| PhysGaussian | 1800 |
| **DynamicTree** | **18.22** |

- 相比 PhysGaussian 快约 **99%**（18.22 vs. 1800 ms/帧）
- 相比 PhysFlow 快约 **99.9%**（18.22 vs. 15600 ms/帧）
- 18.22 ms/帧的仿真时间意味着超过 50 FPS 的实时交互能力，其中网格运动计算 13 ms、高斯变形计算 2.57 ms、渲染 2.65 ms。

**定性分析**（Figure 4）：在施加拖拽外力后，PhysGaussian 和 PhysFlow 的响应缺乏树木特有的振荡回弹细节，而 DynamicTree 利用模态分析框架自然产生具有细粒度细节的谐波衰减运动。

#### 与传统树木动画对比

Table 2 的用户偏好研究显示，DynamicTree 在运动真实感上以 **57.86%** 的偏好显著超过 Weber（42.14%），优势为 **+15.72%**。这表明基于学习的频谱生成能够捕捉传统参数化方法难以表达的复杂运动模式。

![[assets/figures/papers/paper_list_l1060_https_arxiv_org_abs_2510_22213/figures/006_Table_2.jpg]]
*Table 2: Quantitative comparison with traditional tree animation methods*

---

### 消融实验

#### 训练策略

Figure 5 和 §3.5 的消融揭示了损失函数和训练策略对生成质量的关键影响：

- **仅使用扩散损失 L_DM**：生成的运动出现分支发散等不真实伪影（Figure 5 第 2 列），说明纯扩散目标缺乏对空间局部一致性的约束。
- **同时联合训练 L_DM + L_LSS**：虽引入局部频谱平滑损失，但联合训练仍导致不稳定的运动模式。
- **两阶段训练**（先 L_DM 后引入 L_LSS）：得到无发散且细节更优的结果（Figure 5 第 4 列）。第一阶段建立合理的全局运动结构，第二阶段在频域施加局部平滑正则化以消除高频伪影。

这一发现表明，频域生成需要先学习全局频谱分布，再引入局部约束进行精化，直接联合优化会干扰扩散模型的去噪过程。

#### 体素分辨率

Table 3 展示了体素分辨率对性能的影响：

![[assets/figures/papers/paper_list_l1060_https_arxiv_org_abs_2510_22213/figures/007_Table_3.jpg]]
*Table 3: Ablation of different resolutions*

| 分辨率 | 批次大小 | 训练时间 | CLIP-I ↓ |
|--------|---------|---------|----------|
| 64³ | 16 | 较低 | 0.0051 |
| **128³** | **8** | 中等 | **0.0039** |
| 256³ | 2 | 较高 | 0.0048 |

- 128³ 分辨率取得最佳 CLIP-I（0.0039），在表示能力和计算效率间达到最优平衡。
- 256³ 分辨率反而导致性能下降（0.0048），作者归因于高分辨率体素扩大了合成训练数据与真实扫描之间的域差距，使得模型泛化能力减弱。

#### 频率成分数量

§3.2 的消融表明，仅保留前 **K=16** 个频率成分即可近乎无损地重建完整频谱，与 Generative-Dynamics 的结论一致。这验证了树木运动在频域的高度稀疏性——准周期性谐波振荡仅需少量傅里叶系数即可表征。

---

### 失败模式与局限性

1. **极端变形场景**：当前方法主要面向中等变形（微风、轻微拖拽），不能处理树枝折断、飓风级风力等破坏性变形。稀疏体素频谱的频域压缩假设准周期性运动，对非周期、大位移形变存在原理性限制。
2. **域差距残留**：尽管体素化有助于弥合合成-真实域差距，对某些非常复杂的真实树枝细节或罕见树种仍可能产生不足。Table 3 中 256³ 分辨率性能下降即为此问题的间接证据。
3. **物理参数粗糙**：交互仿真采用统一的模态分析框架，未考虑不同树干部位杨氏模量等精确物理参数的差异，可能影响极端外力下响应的真实感。

---

### 关键图表结论汇总

- **Figure 1**：DynamicTree 在真实 3DGS 树木上实现结构一致的长时动画和实时交互，时空切片直观展示频域表示的紧凑性。
- **Table 1**：在动画质量和仿真效率两个维度均大幅超越现有方法，仿真速度实现两个数量级的提升。
- **Figure 3**：相比 4DGen 和 SV4D 2.0，DynamicTree 更好地保持 3D 结构，时空切片验证长期运动一致性。
- **Figure 4**：交互仿真中产生更自然的振荡运动，模态分析框架赋予细粒度细节。
- **Figure 5 + Table 3**：两阶段训练和 128³ 体素分辨率是生成无发散、长期一致运动的关键设计选择。
- **Table 2**：在用户偏好中显著超过传统树木动画方法 Weber，证明学习型频谱生成的有效性。

![[assets/figures/papers/paper_list_l1060_https_arxiv_org_abs_2510_22213/figures/010_Figure_6.jpg]]
*Figure 6: Examples from our 4DTree dataset. For clarity of visualization, the leaves and trunk are rendered using two simplified material configurations*

## 定位与知识库关联

### 1. 与基线方法的关系

DynamicTree 在 4D 树木动画生成和交互式物理模拟两个维度上，与现有工作形成了明确的对比关系。

**相对于 4D 生成基线**：**4DGen** (Yin et al., arXiv 2023) 和 **SV4D 2.0** (Yao et al., arXiv 2025) 代表了当前基于视频扩散模型的 4D 内容生成范式，但其直接预测密集高斯变形序列的方式在树木这类细长拓扑结构上容易产生 3D 结构崩塌。DynamicTree 的核心差异在于将运动生成从原始高斯空间迁移到稀疏频域空间——通过体素化压缩空间维度、傅里叶变换压缩时间维度，仅保留前 K 个频率成分（K=16 即可近乎无损重建），使得扩散模型的学习目标从“生成海量高斯位移”转变为“生成紧凑频谱系数”。这一表示层面的变革直接带来了 **Table 1** 中 CLIP-I↓ (0.0052 vs 0.0103)、CLIP-T↓ (0.0021 vs 0.0094) 和用户偏好 MA↑ (93.7% vs 2.1%) 的显著提升。

**相对于物理模拟基线**：**PhysGaussian** (Xie et al., CVPR 2024) 和 **PhysFlow** (Liu et al., CVPR 2025) 分别基于 3DGS 和 4D 表示进行物理仿真，每帧模拟时间分别为 1800 ms 和 15600 ms，无法满足实时交互需求。DynamicTree 将生成的频谱直接作为模态基底，通过模态叠加方程 $\mathcal{D}(t) = \sum_{k=1}^K \phi_k \cdot q^k(t)$ 实时求解外力响应，将单帧模拟时间压缩至 18.22 ms（其中网格运动 13 ms、高斯变形 2.57 ms、渲染 2.65 ms），速度提升约两个数量级。在相同拖拽外力作用下，DynamicTree 产生的振荡运动更自然、细节更丰富（**Figure 4**）。

**相对于传统树木动画基线**：**Weber** (Weber and Penn, SIGGRAPH 1995) 是经典的基于规则的树木建模与动画方法。用户偏好研究中 DynamicTree 以 57.86% vs 42.14% 的总体偏好胜出（**Table 2**），表明数据驱动的频谱生成在运动真实感上已超越手工规则系统。

### 2. 关键设计选择与消融证据

DynamicTree 的性能优势可归因于三个相互耦合的设计选择，消融实验为其提供了因果证据：

- **稀疏体素频谱表示**：将运动压缩到频域是效率与一致性的根本来源。体素分辨率消融（**Table 3**）显示，128³ 在 CLIP-I 上表现最佳（0.0039），而更高分辨率（256³）因合成训练数据与真实扫描之间的域差距反而导致性能下降。这验证了“适度压缩有助于弥合域差距”的假设。

- **局部频谱平滑损失 $\mathcal{L}_{\mathrm{LSS}}$**：仅使用扩散损失 $\mathcal{L}_{\mathrm{DM}}$ 训练会导致分支发散等不真实运动（**Figure 5** 第 2 列）。$\mathcal{L}_{\mathrm{LSS}}$ 约束相邻体素在频域的实部与虚部相似性，本质上是在频域施加局部运动一致性先验。

- **两阶段训练策略**：同时使用 $\mathcal{L}_{\mathrm{DM}}$ 和 $\mathcal{L}_{\mathrm{LSS}}$ 仍可能出现不稳定；采用先 $\mathcal{L}_{\mathrm{DM}}$ 后引入 $\mathcal{L}_{\mathrm{LSS}}$ 的两阶段训练可获得无发散且细节更优的结果（**Figure 5** 第 3–4 列）。这表明频谱平滑约束应在扩散模型已学到合理运动分布后再施加，过早引入会干扰生成质量。

### 3. 适用边界与局限

DynamicTree 的适用边界由其核心假设——“树木运动是准周期性谐波振荡的叠加”——所界定：

- **变形幅度限制**：当前方法主要面向中等变形场景（微风、轻微拖拽），尚不能处理极端破坏性变形（树枝折断、飓风级风力）。这是因为稀疏频谱表示本质上假设运动可被少数谐波成分描述，大变形和非周期性运动超出了该表示的表达能力。

- **域差距的残余影响**：模型训练依赖合成数据集（**4DTree**，**Figure 6**），尽管体素化有助于弥合合成-真实域差距，但对某些非常复杂的真实树枝细节或特定树种仍可能产生不足。**Table 3** 中 256³ 分辨率性能下降即为域差距的直接证据。

- **网格依赖**：高斯变形通过 GaMeS 表面绑定（$\mu = \alpha_1 V_1 + \alpha_2 V_2 + \alpha_3 V_3$）驱动，这意味着动画质量受限于初始网格重建精度。对于网格重建失败的细枝或叶片区域，运动传递可能不准确。

### 4. 开放问题

1. **表示扩展**：稀疏体素频谱能否推广到其他准周期性动态物体（旗帜、衣物、水流）？这些物体的频谱稀疏性假设是否成立，需要进一步验证。

2. **大变形支持**：如何扩展表示以支持断裂、剧烈摇摆等非周期性运动？可能需要引入分段频谱或混合表示（频域 + 时域残差）。

3. **物理参数增强**：能否结合更精确的物理参数（如不同树干部位的杨氏模量）来增强交互的真实感？当前模态分析使用统一的简化物理模型。

4. **训练数据多样性**：合成训练集的树种和几何复杂度是否足以覆盖所有真实场景？4DTree 数据集的多样性与真实世界树木形态分布之间的差距需要量化评估。

## 原文 PDF

![[paperPDFs/CVPR_2026/DynamicTree_Interactive_Real_Tree_Animation_via_Sparse_Voxel_Spectrum.pdf]]
