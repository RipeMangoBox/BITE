---
title: "PatchScene: Patch-based Voxel Diffusion Model for Large-Scale Scene Completion"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/PatchScene_Patch_based_Voxel_Diffusion_Model_for_Large_Scale_Scene_Completion.pdf
project_link: null
code_link: null
aliases:
- PatchScene
tags:
- CVPR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 将分块（patch）体素扩散作为基本生成范式，配合随机化空间融合与密度自适应时间融合，以及由近及远的环形渐进扩散顺序，从局部高保真完成块逐步向外传播信息，最终实现大规模、无限范围且时间一致的场景补全。
primary_logic: 利用 LiDAR 扫描中径向点密度递减的物理特性，采用从传感器中心向外的环形扩散顺序，确保信息丰富的近距补全块可靠地指导稀疏远距块的生成；同时通过随机掩码融合消除块边界伪影，并以跨帧密度一致性自适应加权实现时间平滑，从而在保持高几何精度的前提下实现统一的大规模场景生成。
claims:
- PatchScene 在 SemanticKITTI 的所有标准指标上均达到当时最优性能，优于 LiDiff、LiDPM、ScoreLiDAR 和 XCube 等方法。
- 时间融合将相邻帧之间的双向 RMSE 从单帧补全的约 0.155/0.159 降至 0.086/0.081，显著提升时间一致性。
- 环形向外扩散（Annular outward）的 CD 达到 0.319，优于线性扩散（0.451）和环形向内扩散（0.391），证明由近及远的信息传播有效。
- SemanticKITTI 上 CD↓, JSD 3D↓, JSD BEV↓, Voxel IoU↑ (0.5/0.2/0.1) = CD=0.319, JSD 3D=0.444, JSD BEV=0.371, IoU_0.5=45.3
---

# PatchScene: Patch-based Voxel Diffusion Model for Large-Scale Scene Completion

> [!tip] 核心洞察
> 利用 LiDAR 扫描中径向点密度递减的物理特性，采用从传感器中心向外的环形扩散顺序，确保信息丰富的近距补全块可靠地指导稀疏远距块的生成；同时通过随机掩码融合消除块边界伪影，并以跨帧密度一致性自适应加权实现时间平滑，从而在保持高几何精度的前提下实现统一的大规模场景生成。

| 字段 | 内容 |
|------|------|
| 中文题名 | PatchScene：基于分块体素的扩散模型用于大规模场景补全 |
| 英文题名 | PatchScene: Patch-based Voxel Diffusion Model for Large-Scale Scene Completion |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Xu_PatchScene_Patch-based_Voxel_Diffusion_Model_for_Large-Scale_Scene_Completion_CVPR_2026_paper.html) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | PatchScene |
| Dataset | SemanticKITTI |

> [!tip] 效果简介
> - SemanticKITTI 上，CD↓, JSD 3D↓, JSD BEV↓, Voxel IoU↑ (0.5/0.2/0.1) CD=0.319, JSD 3D=0.444, JSD BEV=0.371, IoU_0.5=45.3 vs 优于 LiDiff, LiDPM, ScoreLiDAR, XCube 等先前最优方法（详见 Table 1） (所有指标均取得显著一致的提升)。

## 概要

大规模 LiDAR 场景补全是自动驾驶与机器人环境感知中的关键任务，其核心挑战在于从稀疏、有限的传感器观测中重建出几何精确、时空一致的密集三维点云。现有方法面临一个根本性的三角困境：**全局密集体素或潜在表示导致计算开销随空间范围呈三次方增长**，多阶段编解码架构引入信息损失与误差累积，且普遍忽略时间维度，难以生成跨帧连贯的补全结果。

PatchScene 针对上述瓶颈提出了一种**分治范式的体素扩散框架**。其核心思路是将全局体素空间划分为相互重叠的局部块（patches），在每个块上独立执行扩散去噪以生成高保真的局部几何，再通过随机化空间融合与密度自适应时间融合将各块整合为统一的全局点云。该方法进一步利用 LiDAR 扫描中径向点密度递减的物理特性，设计了一种**由近及远的环形渐进扩散顺序**：从传感器中心向外逐环生成，使信息丰富的近距补全块可靠地指导稀疏远距块的生成，从而在保持高几何精度的同时实现大规模、无限范围的场景扩展。

在 SemanticKITTI 基准上，PatchScene 在所有标准指标上均取得当时最优性能——Chamfer Distance (CD) 降至 0.319，JSD 3D 为 0.444，JSD BEV 为 0.371，Voxel IoU (阈值 0.5) 达到 45.3%，全面超越 LiDiff、LiDPM、ScoreLiDAR 及 XCube 等先前方法。消融实验表明，**环形向外扩散**相比线性扩散将 CD 从 0.451 降至 0.319，而**时间融合机制**将相邻帧之间的双向 RMSE 从约 0.155/0.159 大幅压缩至 0.086/0.081，验证了所提时空融合策略在提升补全质量与时间一致性方面的关键作用。此外，仅在 20 米感知范围上训练的模型可直接泛化至 50 米场景，展现出良好的空间扩展能力。



大规模场景补全是自动驾驶与机器人感知中的核心任务，其目标是从稀疏、不完整的 LiDAR 扫描中恢复稠密且几何精确的三维点云。这一任务面临一个根本性的三角冲突：**高几何保真度、时间一致性与计算效率三者难以兼得**。

现有方法主要沿两条技术路线展开。基于点的扩散模型（如 **LiDiff** (Nunes et al., CVPR 2024)、**LiDPM** (Martyniuk et al., IV 2025)、**ScoreLiDAR** (Zhang et al., ICCV 2025)）直接在点云上执行去噪生成，虽然避免了体素化的离散误差，但其生成结果往往较为稀疏，且后处理细化容易引入空洞和不一致的幻觉点（见 Figure 3）。基于稀疏体素层级的潜在扩散方法（如 **XCube** (Ren et al., CVPR 2024)）通过分层表示压缩空间维度，但级联式的编解码路径会累积信息损失与误差。

从表示与生成范式的角度审视，上述方法的共同瓶颈在于**全局性假设**：它们试图在统一的全局体素网格或全局潜在空间中一次性完成整个场景的生成。这带来了两个直接后果。其一，**计算复杂度呈三次方增长**——密集体素表示的内存与计算开销随空间范围 $O(H \cdot W \cdot D)$ 急剧膨胀，严重限制了可处理场景的规模。其二，**单阶段或级联式补全缺乏局部精细控制能力**，难以在保持全局一致性的同时，对近距区域的几何细节进行高保真重建。

更为关键的是，现有方法**普遍忽略了时间维度**。逐帧独立补全的策略意味着相邻帧之间不存在信息交互，导致生成的稠密点云在时间轴上缺乏连贯性——同一静态物体在不同帧中可能被补全为不一致的几何形态。这一缺陷在动态场景理解与后续感知任务中尤为致命。

PatchScene 的提出正是为了系统性地解决上述冲突。其核心动机源于一个朴素而深刻的观察：LiDAR 扫描具有天然的**径向密度递减特性**——靠近传感器的区域点云密集、信息丰富，而远离传感器的区域点云稀疏、信息匮乏。这一物理先验暗示了一个由近及远、以信息密集区域指导稀疏区域生成的分治策略。通过将全局体素空间分割为重叠的局部块（patch），在每个块上独立执行扩散去噪，再经由空间与时间融合机制将局部结果聚合为全局一致的点云，PatchScene 实现了**高保真度、时间一致性与无限空间扩展能力**的统一。



## 核心方法与创新机理

PatchScene 的核心创新在于通过**分块体素扩散范式**重构了大规模场景补全的生成机制，从根本上解耦了高保真几何生成与计算可扩展性之间的矛盾。与现有方法相比，该方法在场景表示、融合策略、时间建模和生成调度四个维度上引入了系统性变革。

### 1. 从全局生成到分块扩散的范式转移

现有方法普遍采用全局密集体素网格或全局潜在表示进行单阶段或级联补全，其内存与计算开销随场景范围呈三次方增长，严重限制了大规模场景的几何保真度。PatchScene 将这一范式替换为**局部体素块上的独立扩散去噪**：将全局体素空间 $\mathbf{X} \in \{0,1\}^{H \times W \times D}$ 划分为步长重叠的局部块 $\mathbf{x}^{(k)}$，每个块独立执行前向加噪与反向去噪，网络 $f_\theta$ 直接预测干净体素 $\hat{\mathbf{x}}_0^{(k)}$（式1-6）。这一“分而治之”策略将计算复杂度与场景规模解耦，使得在有限显存下实现高分辨率体素生成成为可能（Sec. 3.1）。

### 2. 随机化空间融合消除块边界伪影

分块生成引入的核心挑战是块间边界的一致性问题。传统方法或缺乏显式融合机制，或采用简单平均等确定性策略，难以消除拼接痕迹。PatchScene 提出了**随机干扰空间融合**机制：在块间重叠区域，以 Bernoulli(0.5) 随机掩码 $B(p)$ 混合全局噪声估计 $\hat{\epsilon}^{\text{global}}(p)$ 与当前块噪声估计 $\hat{\epsilon}^{k}(p)$（式7）。消融实验证实，这一随机耦合方案将 CD 从无融合的 0.451 降至 0.319，显著优于简单平均等确定性融合策略（Table 4, Sec. 4.4）。其机理在于，随机掩码在去噪迭代中持续扰动块边界区域的噪声估计，迫使相邻块在生成过程中相互协商，从而隐式地消除边界伪影。

### 3. 密度自适应时间融合实现跨帧一致性

现有场景补全方法普遍逐帧独立处理，完全忽略时间维度，导致相邻帧之间出现几何跳变。PatchScene 首次将时间一致性纳入扩散生成过程，提出**置信度引导的时空融合**：通过 ICP 配准对齐前后帧后，利用 BEV 局部点密度比值自适应计算融合权重 $\lambda(p) = \min(\rho^{\tau+1}(p) / (\rho^{\tau}(p) + \epsilon), 1.0)$（式9），对前一帧和当前帧的去噪预测进行加权组合（式8）。该设计的核心洞察在于：结构稳定区域的密度比接近 1，可充分继承历史信息；动态变化区域密度比偏离 1，则更多依赖当前帧观测。实验表明，时间融合将相邻帧间的双向 RMSE 从前向 0.155/后向 0.159 大幅降至 0.086/0.081（Table 2, Sec. 4.3），首次在场景补全中实现了有量化指标的时空连贯性。

### 4. 环形流扩散：利用物理先验的生成调度

PatchScene 的第四项关键创新是**环形向外扩散调度**。该方法将体素块按距传感器中心的距离划分为同心圆环，从内环向外环依次生成，内环已完成的高质量结果作为外环去噪的条件信息。这一设计并非任意的启发式，而是直接利用了 LiDAR 扫描中径向点密度递减的物理特性：近距区域点云密集、信息丰富，其补全结果高度可靠，可有效指导稀疏远距块的生成。消融实验证实，环形向外扩散的 CD 达到 0.319，显著优于线性扩散（0.451）和环形向内扩散（0.391），验证了由近及远信息传播策略的有效性（Table 5, Sec. 4.4）。此外，该调度策略天然支持无限空间扩展——仅需在训练范围（20 m）外继续添加外环即可，无需重新训练（Figure 4）。



PatchScene 的整体设计遵循“分治—融合—扩散”的统一范式，其核心思路是将大规模 LiDAR 场景补全从全局密集生成问题转化为一组局部高保真补全与跨区域一致性融合的协同过程。整个框架由三个关键阶段构成：

### 1. 体素分块与局部扩散补全

首先，将全局密集体素空间 $\mathbf{X} \in \{0,1\}^{H \times W \times D}$ 划分为一组具有固定步长重叠的局部体素块 $\mathbf{x}^{(k)}$（式1）。每个局部块独立地经历一个扩散去噪过程：在前向阶段，向干净体素块 $\mathbf{x}_0^{(k)}$ 逐步添加高斯噪声（式2）；在反向阶段，神经网络 $f_\theta$ 以当前噪声块 $\mathbf{x}_t^{(k)}$、时间步 $t$ 和位置编码 $\mathbf{p}_k$ 为条件，直接预测干净体素 $\hat{\mathbf{x}}_0^{(k)}$（式3），并据此反推噪声 $\hat{\epsilon}$（式4），完成单步去噪（式5）。训练目标是最小化随机选取的块和时间步上预测体素与真值之间的均方误差（式6）。这种分块策略将计算复杂度从全局三次方降至局部线性增长，使得高分辨率体素空间的直接生成成为可能。

### 2. 时空融合

局部补全完成后，需要将分散的块融合为全局一致的点云。PatchScene 采用两个互补的融合机制：

- **随机干扰空间融合**：在块间重叠区域，通过伯努利随机掩码 $B(p) \sim \text{Bernoulli}(0.5)$ 以 50% 概率混合全局噪声估计与当前块噪声估计（式7），从而消除块边界伪影，而非简单平均。
- **自适应时间融合**：利用 ICP 配准对齐前后帧，基于 BEV 局部点密度比值自适应计算融合权重 $\lambda(p)$（式9），将前一帧已完成的补全信息加权注入当前帧的去噪预测中（式8）。密度一致性高的区域继承更多历史信息，变化区域则更多依赖当前帧，从而实现跨帧的时空连贯生成。

### 3. 环形流扩散调度

为充分利用 LiDAR 扫描中径向点密度递减的物理特性，PatchScene 采用环形流扩散顺序：将体素空间按距传感器中心的远近划分为同心圆环区域 $\mathcal{R}_\ell$，从最内环向外环依次执行补全。内环因点密度高、信息丰富，其已完成的高质量结果作为外环扩散去噪的条件信息进行传播，由近及远地引导稀疏区域的生成。这一策略不仅提升了远距补全的几何保真度，还天然支持无限空间扩展——模型在 20 m 范围训练后可直接推广至 50 m 场景补全，无需重新训练。

### 输入输出流

- **输入**：单帧或多帧稀疏 LiDAR 观测（体素化后的稀疏占用网格 $\tilde{\mathbf{X}}$）。
- **处理流程**：体素分块 → 局部扩散去噪（环形流顺序调度）→ 随机干扰空间融合 → 自适应时间融合 → 全局密集体素重建。
- **输出**：高几何保真度、时空一致且可无限扩展的密集点云。

图2给出了 PatchScene 的完整架构概览，清晰展示了从分块、独立去噪到时空融合、环形扩散的全流程。

### 补充图表

![[assets/figures/papers/paper_list_l2563_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_PatchScene_Patch_ba/figures/002_Figure_2.jpg]]
*Figure 2: Overview of PatchScene. The voxel space is first divided into overlapping local patches, each processed independently through diffusion-based denoising to generate local point clouds. Spatial and temporal fusion then merges these patches into a coherent global point cloud. Finally, an annular outward diffusion strategy extends completion across the entire scene, handling near-dense and far-sparse LiDAR distributions for large-scale, temporally consistent reconstruction*



PatchScene 围绕“分块体素扩散—空间/时间融合—环形渐进生成”三条主线构建，其核心模块与关键公式如下。

### 体素分块与局部扩散去噪

将全局密集体素空间 $\mathbf{X} \in \{0,1\}^{H \times W \times D}$ 划分为步长重叠的局部块，第 $k$ 个块的真值与稀疏观测分别为：

$$
\mathbf{x}_0^{(k)} = \operatorname{Patch}(\mathbf{X}_0, k), \quad \tilde{\mathbf{x}}^{(k)} = \operatorname{Patch}(\tilde{\mathbf{X}}, k) \tag{1}
$$

对每个局部块独立执行扩散过程。前向加噪遵循标准 DDPM 调度：

$$
\mathbf{x}_t^{k} = \sqrt{\bar{\alpha}_t} \mathbf{x}_0^{k} + \sqrt{1 - \bar{\alpha}_t} \epsilon, \quad t = 1, \dots, T \tag{2}
$$

反向去噪时，网络 $f_\theta$ 以当前噪声块、时间步 $t$ 及位置编码 $\mathbf{p}_k$ 为条件，直接预测干净体素：

$$
\hat{\mathbf{x}}_0^{k} = f_{\theta}(\mathbf{x}_t^{k}, t, \mathbf{p}_k) \tag{3}
$$

由预测的干净体素反推等效噪声：

$$
\hat{\epsilon} = \frac{1}{\sqrt{1 - \bar{\alpha}_t}} \left( \mathbf{x}_t^{k} - \sqrt{\bar{\alpha}_t} \hat{\mathbf{x}}_0^{k} \right) \tag{4}
$$

单步采样更新为：

$$
\mathbf{x}_{t-1}^{k} = \frac{1}{\sqrt{\alpha_t}} \left( \mathbf{x}_t^{k} - \frac{1-\alpha_t}{\sqrt{1-\bar{\alpha}_t}} \hat{\epsilon} \right) + \sigma_t \mathbf{z} \tag{5}
$$

训练目标为随机块与随机时间步上的体素占用 MSE：

$$
\mathcal{L}_{\mathrm{patch}}(\theta) = \mathbb{E}_{k, t} \left[ \| \mathbf{x}_0^{k} - \hat{\mathbf{x}}_0^{k} \|_2^2 \right] \tag{6}
$$

该设计将全局生成解耦为局部高保真重建，从根本上规避了密集体素表示的三次方内存/计算瓶颈。

### 随机干扰空间融合

块间重叠区域若简单平均会产生可察觉的边界伪影。PatchScene 引入随机干扰机制：在每个重叠体素位置 $p$，以 Bernoulli(0.5) 随机掩码 $B(p)$ 混合全局噪声估计与当前块噪声估计：

$$
\hat{\epsilon}_{\mathrm{fused}}^{k}(p) = B(p) \cdot \hat{\epsilon}^{\mathrm{global}}(p) + (1 - B(p)) \cdot \hat{\epsilon}^{k}(p) \tag{7}
$$

该随机化策略在多次去噪迭代中自然消除块边界，无需后处理平滑。消融实验（Table 4）证实，随机耦合方案将 CD 从无融合的 0.451 降至 0.319，显著优于简单平均等确定性融合方式。

### 自适应时间融合

为利用跨帧时序信息，PatchScene 通过 ICP 配准对齐前后帧，基于 BEV 局部点密度比值动态计算融合权重：

$$
\lambda(p) = \min\left( \frac{\rho^{\tau+1}(p)}{\rho^{\tau}(p) + \epsilon}, 1.0 \right), \quad p \in \mathcal{V} \tag{9}
$$

其中 $\rho^{\tau}(p)$ 和 $\rho^{\tau+1}(p)$ 分别为前一帧与当前帧在位置 $p$ 的局部点密度。该权重对前一帧已完成的高置信区域赋予更大继承比例，而对新出现或变化区域则更多依赖当前帧预测。加权融合公式为：

$$
\hat{\mathbf{x}}_{t}^{\tau+1} = \lambda \cdot \hat{\mathbf{x}}_{t}^{\tau} + (1 - \lambda) \cdot \hat{\mathbf{x}}_{t}^{\tau+1} \tag{8}
$$

该机制使相邻帧双向 RMSE 从约 0.155/0.159 大幅降至 0.086/0.081（Table 2），验证了密度一致性引导的有效性。

### 环形流扩散调度

LiDAR 扫描具有径向点密度递减的物理特性——近距区域信息丰富，远距区域极度稀疏。PatchScene 据此设计环形向外扩散顺序：将体素空间按距传感器中心的距离划分为同心圆环 $\mathcal{R}_\ell$，从内环向外环依次生成。内环高质量补全结果作为外环去噪的条件信息，实现由近及远的可靠信息传播。消融实验（Table 5）表明，环形向外扩散的 CD 为 0.319，显著优于线性扩散（0.451）和环形向内扩散（0.391），证明该策略有效利用了 LiDAR 的物理先验。



## 实验与关键发现

PatchScene 在 SemanticKITTI 基准上进行了系统评估，我们从主结果、时间一致性、消融实验三个维度展开分析。

### 主结果：SemanticKITTI 上的定量与定性比较

**Table 1** 报告了 PatchScene 与现有方法的全面定量比较。PatchScene 在所有标准指标上均取得当时最优性能：Chamfer Distance（CD）降至 0.319，3D Jensen-Shannon Divergence（JSD 3D）为 0.444，BEV JSD 为 0.371，Voxel IoU（阈值 0.5）达到 45.3。相较基于点的扩散方法 **LiDiff**（Nunes et al., CVPR 2024）、**LiDPM**（Martyniuk et al., IV 2025）、**ScoreLiDAR**（Zhang et al., ICCV 2025），以及基于潜在扩散的 **XCube**（Ren et al., CVPR 2024），PatchScene 在所有指标上均表现出显著且一致的提升。

定性结果如 **Figure 3** 所示，LiDiff、LiDPM 和 ScoreLiDAR 的补全结果相对稀疏，且后处理细化虽能增加密度，却引入空洞和不一致的幻觉点。相比之下，PatchScene 的补全结果在几何保真度和整体结构上与真值最为接近。

![[assets/figures/papers/paper_list_l2563_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_PatchScene_Patch_ba/figures/003_Figure_3.jpg]]
*Figure 3: Comparison of our method with LiDiff, LiDPM, and ScoreLiDAR on the same scene in SemanticKITTI. All point clouds are height-normalized and color-mapped within the same range. The completion results produced by LiDiff, LiDPM, and ScoreLiDAR remain relatively sparse, and although refinement yields denser predictions, it introduces holes and inconsistent hallucinated points. In contrast, our PatchScene achieves completion results that are closest to the ground truth*

### 时间一致性分析

**Table 2** 展示了时间融合模块对相邻帧一致性的影响。未引入时间融合时，单帧补全结果在相邻帧之间的双向 RMSE 分别为前向 0.155 和后向 0.159。加入自适应时间融合后，前向 RMSE 降至 0.086，后向 RMSE 降至 0.081，降幅接近 50%。这一结果表明，基于 BEV 密度一致性的自适应加权策略（公式 9）能够有效继承前一帧中结构稳定区域的信息，同时让变化区域更多依赖当前帧观测，从而在保持几何精度的前提下大幅提升时间连贯性。

### 消融实验

#### 空间融合策略

**Table 4** 消融了不同空间融合方案的影响。无融合（独立块去噪后直接拼接）的 CD 高达 0.451，JSD BEV 为 0.446，表明块边界处存在严重的几何不连续。简单平均融合虽有所改善，但仍不及随机耦合（random coupling）方案。随机耦合通过 Bernoulli(0.5) 掩码在重叠区域随机混合全局噪声估计与当前块噪声估计（公式 7），将 CD 降至 0.319，JSD BEV 降至 0.371，有效消除了块边界伪影。

#### 去噪时间步数

**Table 3** 和 **Figure 5** 分析了去噪时间步数对补全质量的影响。步数过少（如 5 步）时，补全场景中出现可察觉的块边界，因为迭代融合次数不足，块间一致性较弱。将步数增加到 10 步可显著增强块间一致性，继续增加到 15 步并未带来额外提升。这表明 10 步已能在计算效率与融合质量之间取得良好平衡。

#### 生成方向

**Table 5** 比较了三种扩散顺序：线性扩散、环形向内扩散和环形向外扩散。线性扩散（无特定顺序）的 CD 为 0.451，环形向内扩散（从外向内）的 CD 为 0.391，而环形向外扩散（从传感器中心向外）的 CD 达到 0.319，在所有指标上均为最优。这一结果验证了核心设计动机：LiDAR 扫描中近距区域点密度高、信息丰富，由近及远的环形扩散顺序使高质量内环补全结果能够可靠地指导稀疏外环块的生成，从而实现信息从密集区域向稀疏区域的有效传播。

### 空间泛化能力

**Figure 4** 展示了 PatchScene 的空间泛化能力。模型在 20 m LiDAR 感知范围的场景上训练后，直接应用于 50 m 扩展范围的场景补全，无需重新训练。无论在开阔环境还是狭窄空间中，补全点云均保持高几何保真度，准确保留了物体边界，同时展现出良好的全局场景一致性。这得益于环形向外扩散策略天然支持无限空间扩展的特性。

### 补充图表

![[assets/figures/papers/paper_list_l2563_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_PatchScene_Patch_ba/figures/005_Table_1.jpg]]
*Table 1: Comparison of our method with existing approaches on SemanticKITTI. Baselines, metrics, and ground truth are from LiDPM, with results marked † independently reproduced and evaluated*

![[assets/figures/papers/paper_list_l2563_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_PatchScene_Patch_ba/figures/006_Table_2.jpg]]
*Table 2: Analyzing Temporal Consistency with the RMSE Metric*

![[assets/figures/papers/paper_list_l2563_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_PatchScene_Patch_ba/figures/008_Table_4.jpg]]
*Table 4: Ablation of Spatial Fusion*

![[assets/figures/papers/paper_list_l2563_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_PatchScene_Patch_ba/figures/010_Table_5.jpg]]
*Table 5: Ablation of Generation Direction*

![[assets/figures/papers/paper_list_l2563_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_PatchScene_Patch_ba/figures/004_Figure_4.jpg]]
*Figure 4: We train PatchScene on scenes with a LiDAR sensing range of 20 meters and directly apply it to point cloud completion with an extended range of 50 meters. Whether in open environments or narrow spaces, our completed point clouds consistently maintain high geometric fidelity, accurately preserve object boundaries, and simultaneously ensure strong global scene coherence*

![[assets/figures/papers/paper_list_l2563_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_PatchScene_Patch_ba/figures/007_Table_3.jpg]]
*Table 3: Analyzing the Impact of Denoising Timesteps on Point Cloud Completion Accuracy*

![[assets/figures/papers/paper_list_l2563_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_PatchScene_Patch_ba/figures/009_Figure_5.jpg]]
*Figure 5: The effect of the denoising timestep on completion performance. Less timesteps lead to visible boundaries in the completed scenes, while larger timesteps enable more fusion iterations and yield stronger inter-patch consistency*



## 定位与知识库关联

### 任务定位与核心瓶颈

PatchScene 聚焦于**大规模 LiDAR 场景补全**（Large-scale LiDAR Scene Completion），其输入为单帧或多帧稀疏 LiDAR 扫描，输出为密集、几何精确的完整三维点云。该任务区别于传统目标级点云补全（object-level completion），需同时处理场景级空间范围、多物体几何保真度以及跨帧时间一致性。

现有方法面临一个根本性的三元冲突：**高几何保真度、时间一致性与计算效率**难以兼得。基于全局密集体素或潜在表示的方法（如 **XCube** (Ren et al., CVPR 2024) 的稀疏体素层次潜在扩散）面临体素数量随空间范围的三次方增长，限制了可扩展性；基于点的扩散模型（如 **LiDiff** (Nunes et al., CVPR 2024)、**LiDPM** (Martyniuk et al., IV 2025)、**ScoreLiDAR** (Zhang et al., ICCV 2025)）虽避免了体素化开销，但生成的全局点云常出现稀疏、空洞及不一致的幻觉点，且缺乏对时间维度的显式建模，导致逐帧独立补全在相邻帧之间产生明显的几何跳变。

PatchScene 的核心突破在于将**分块扩散生成**作为基本范式，配合随机化空间融合与密度自适应时间融合，从根本上解耦了局部高保真生成与全局一致性集成之间的张力。

### 方法谱系中的位置

从生成范式的维度审视，PatchScene 处于以下几条技术路线的交叉点：

| 维度 | 先前方法代表 | PatchScene 的差异化定位 |
|------|-------------|----------------------|
| **表示空间** | LiDiff/LiDPM/ScoreLiDAR：点云空间直接扩散；XCube：稀疏体素层次潜在空间扩散 | 显式密集体素空间，但仅在局部块（patch）上操作，兼顾几何精度与计算可行性 |
| **生成范围** | 全局一次性生成或级联生成 | 分块独立生成 + 多层级融合，支持从有限训练范围向更大场景的零样本泛化 |
| **时间建模** | 逐帧独立补全，无跨帧信息交互 | 显式引入基于 BEV 密度一致性的自适应时间融合，首次将时间一致性纳入扩散去噪循环 |
| **生成顺序** | 随机或无特定顺序 | 利用 LiDAR 径向密度衰减的物理先验，设计由近及远的环形流扩散调度，实现信息从高置信度区域向低置信度区域的有序传播 |

在扩散模型用于三维场景生成的谱系中，PatchScene 可被归为**分治式显式体素扩散**（divide-and-conquer explicit voxel diffusion）方法。其与 XCube 的潜在扩散路线形成互补：XCube 通过稀疏体素层次压缩全局信息以提升效率，但潜在空间的信息损失可能限制几何细节的保真度；PatchScene 则通过局部块上的显式体素操作保留精细几何，并通过融合机制弥补分块带来的全局一致性损失。

### 适用边界与限制条件

尽管 PatchScene 在 SemanticKITTI 上取得了当时最优性能，其方法设计隐含了若干适用边界：

1. **LiDAR 径向密度先验的依赖**：环形流扩散策略的有效性建立在传感器中心点密度高、外围密度低的物理特性之上。对于非径向传感器布局或密度分布均匀的采集方式（如稠密多视角 RGB-D 重建），该调度策略的优势可能减弱。

2. **时间融合的配准精度要求**：跨帧时间融合依赖 ICP 配准将前一帧完成点云对齐到当前帧坐标系。在高速运动、大角度旋转或缺乏几何特征的退化场景中，配准误差可能通过式（8）的加权融合传播，反而引入伪影。

3. **分块大小的场景适应性**：局部块的尺寸选择需要在几何细节保留与全局感受野之间权衡。当前工作在 SemanticKITTI 上验证了固定块大小的有效性，但对于包含极大型结构（如长距离隧道、桥梁）或极小型物体（如行人、交通锥）的场景，固定块尺寸可能非最优。

4. **去噪步数的效率-质量权衡**：消融实验表明，去噪步数从 5 步增加到 10 步可显著消除块边界伪影，但继续增加到 15 步并未带来额外提升。这意味着存在一个收益饱和点，实际部署时需根据延迟预算选择步数。

### 开放问题与后续方向

基于 PatchScene 的方法框架和当前局限，以下开放问题值得关注：

- **动态场景中的时间融合鲁棒性**：当前时间融合假设场景结构在相邻帧间基本保持静态，通过 BEV 密度比自适应调节融合权重。对于包含快速移动物体的场景，如何区分“结构变化”与“补全误差”，实现运动感知的时间融合，是一个待探索的方向。

- **分块策略的自适应优化**：能否根据局部场景复杂度（如物体密集度、遮挡程度）动态调整块大小和重叠比例，使计算资源向信息贫乏区域倾斜，进一步提升效率-质量的帕累托前沿。

- **多传感器融合扩展**：PatchScene 当前仅利用 LiDAR 输入。将图像或毫米波雷达等多模态信息引入局部块的条件生成，有望在远距离、稀疏区域提供额外的语义和几何线索，缓解纯 LiDAR 补全的歧义性。

- **无限空间扩展的理论保证**：论文展示了从 20m 训练范围向 50m 测试范围的零样本泛化能力。这种泛化是否随范围继续扩大而保持稳定，以及是否存在理论上的有效扩展上限，仍需进一步分析。



## 原文 PDF

![[paperPDFs/CVPR_2026/PatchScene_Patch_based_Voxel_Diffusion_Model_for_Large_Scale_Scene_Completion.pdf]]
