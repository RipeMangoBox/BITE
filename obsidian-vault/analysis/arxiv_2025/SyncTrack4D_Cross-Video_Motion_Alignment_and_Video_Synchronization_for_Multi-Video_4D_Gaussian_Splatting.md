---
title: "SyncTrack4D: Cross-Video Motion Alignment and Video Synchronization for Multi-Video 4D Gaussian Splatting"
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: paperPDFs/arxiv_2025/SyncTrack4D_Cross_Video_Motion_Alignment_and_Video_Synchronization_for_Multi_Video_4D_Gaussian_Splatting.pdf
project_link: null
code_link: null
aliases:
- SyncTrack4D
tags:
- arxiv_2025
- topic/vision_multimodal_applications
- topic/representation_self_supervised_transfer
core_operator: 以密集4D轨迹为统一线索，通过Fused Gromov-Wasserstein匹配实现跨视频轨迹对齐，并在运动样条支架下联合优化时间偏移和4DGS重建。
primary_logic: 将4D跟踪、最优传输匹配与样条支架结合，使时间同步与几何重建互为约束，利用显式轨迹的刚性结构实现亚帧级同步。
claims:
- 在Panoptic Studio多视图配置下，平均时间偏移误差低至0.26帧，显著优于初始偏移和SyncNeRF。
- 去除运动样条支架后PSNR从27.30降至23.21，轨迹出现不连贯。
- Fused Gromov-Wasserstein匹配比特征仅匹配产生几何更一致的对应。
- Panoptic Studio (many-view) 上 平均时间偏移误差 (帧) ↓ = 0.260
---

# SyncTrack4D: Cross-Video Motion Alignment and Video Synchronization for Multi-Video 4D Gaussian Splatting

> [!tip] 核心洞察
> 将4D跟踪、最优传输匹配与样条支架结合，使时间同步与几何重建互为约束，利用显式轨迹的刚性结构实现亚帧级同步。

| 字段 | 内容 |
|------|------|
| 中文题名 | SyncTrack4D：面向多视频4D高斯泼溅的跨视频运动对齐与视频同步 |
| 英文题名 | SyncTrack4D: Cross-Video Motion Alignment and Video Synchronization for Multi-Video 4D Gaussian Splatting |
| 会议/期刊 | arXiv 2025 |
| Links | [paper](https://arxiv.org/abs/2512.04315) |
| Topic | #topic/vision_multimodal_applications #topic/representation_self_supervised_transfer |
| Method | SyncTrack4D |
| Dataset | Panoptic Studio |

> [!tip] 效果简介
> - Panoptic Studio (many-view) 上，平均时间偏移误差 (帧) ↓ 0.260 vs SyncNeRF (未提供具体值, 优于SyncNeRF) (优于SyncNeRF和初始偏移)。
> - Panoptic Studio 上，PSNR↑ 26.3 vs SyncNeRF (未提供具体值) (显著优于SyncNeRF)。

## 概要

**SyncTrack4D** 针对一个被现有4D高斯泼溅（4DGS）方法普遍忽略的核心瓶颈：现有方法依赖硬件同步的多视角视频，无法直接处理野外场景中常见的未同步视频，其隐式变形表达极易受时间错位干扰。该工作提出以密集4D轨迹为统一线索，通过**Fused Gromov-Wasserstein（FGW）最优传输匹配**实现跨视频轨迹对齐，并在运动样条支架（motion-spline scaffold）下联合优化时间偏移与4DGS重建，使时间同步与几何重建互为约束，最终实现亚帧级同步精度。

### 核心结论

- **亚帧级同步精度**：在Panoptic Studio多视图配置下，平均时间偏移误差低至**0.26帧**，显著优于初始偏移和SyncNeRF（Kim et al., AAAI 2024）。
- **高质量4D重建**：同步后的4DGS重建PSNR达到**26.3**，在Panoptic Studio和SyncNeRF Blender数据集上均显著优于SyncNeRF。
- **运动样条支架的关键作用**：消融实验表明，移除运动样条支架后PSNR从27.30骤降至23.21，且轨迹出现明显不连贯（Table 4, Figure 9），验证了该模块对重建质量的决定性影响。

### 方法定位

SyncTrack4D在方法谱系上处于**4D高斯泼溅重建**与**多视频时间同步**的交叉点。其核心创新在于将4D跟踪、最优传输匹配与样条支架相结合，形成一套端到端的多阶段管道：

1. **Per-Video 4D Feature Track Estimation**：为每段视频提取密集4D轨迹与DINOv3特征，构建4DGS特征场。
2. **Cross-Video 4D Track Matching**：通过Fused Gromov-Wasserstein匹配建立跨视频4D轨迹对应，融合特征相似性与轨迹内几何结构（Figure 3），相比仅依赖特征的最优传输匹配产生几何更一致的对应。
3. **Coarse Temporal Synchronization**：在匹配轨迹的几何差异矩阵上利用动态时间规整（DTW）估计粗时间偏移（Figure 4）。
4. **Joint Refinement with Multi-Video 4DGS**：以三次Hermite样条参数化的运动样条支架压缩每视频锚点轨迹，联合优化轨迹、外观与时序偏移，光度损失结合ARAP正则、速度与加速度约束。

与基线方法SyncNeRF（基于NeRF隐式学习每视频时间偏移）相比，SyncTrack4D的关键差异在于：以**显式4D轨迹的刚性结构**替代隐式变形场作为同步线索，并通过**样条支架**为时间偏移优化提供时间可微的连续表示。

### 主要结果概览

| 指标 | 结果 | 对比基准 |
|------|------|----------|
| 平均时间偏移误差（Panoptic Studio多视图） | 0.260帧 | 优于SyncNeRF与初始偏移 |
| PSNR（Panoptic Studio） | 26.3 | 显著优于SyncNeRF |
| 消融：移除运动样条支架后PSNR | 23.21（下降4.09） | 完整模型27.30 |

### 局限与边界条件

- 深度与光流先验依赖现成模型，其精度直接影响最终性能。
- 假设已知相机内外参，不适用于完全无约束设置。
- 在动态区域稀少或静态背景为主时，跟踪匹配可能退化，同步质量下降。
- 当前为离线处理方法，无法满足实时或在线同步需求。

### 动态场景重建的“同步”瓶颈

从多视角视频重建动态三维场景是计算机视觉与图形学中的核心挑战，在自由视点视频、沉浸式远程呈现和运动分析等领域有广泛需求。近年来，以**4D Gaussian Splatting (4DGS)** 为代表的方法在渲染质量和重建效率上取得了显著进展，但其成功高度依赖一个被长期忽视的前提：**输入的多视角视频必须在时间上严格同步**。

这一假设在受控的实验室环境中（如多相机阵列配合硬件同步触发器）可以成立，但在野外场景、用户生成内容或任意多视频集合中几乎无法满足。当视频之间存在未知的时间偏移时，4DGS的隐式变形场会将时间错位错误地解释为空间变形，导致几何坍塌、运动模糊和渲染伪影。这一根本性瓶颈使得现有4DGS方法无法直接应用于大量真实世界的未同步视频数据。

### 现有方法的缺口

针对非同步视频的动态重建，已有工作主要围绕NeRF范式展开。**SyncNeRF**（Kim et al., AAAI 2024）通过隐式学习每视频的时间偏移来解决同步问题，但其同步精度受限于NeRF的隐式表达，难以达到亚帧级对齐，且缺乏对显式运动线索的利用。更关键的是，这类方法将时间同步与几何重建解耦或仅弱耦合，未能充分利用两者之间的互约束关系。

在4DGS框架下，**MoSca**等工作引入了显式的锚点轨迹来表示动态场景，但这些轨迹仅服务于单视频重建，从未被用作跨视频对齐的线索。另一方面，跨视频匹配领域的最优传输方法通常仅依赖特征相似性，忽略了轨迹内部的几何结构一致性，容易产生不合理的跨视频对应。

### 核心动机与解决思路

SyncTrack4D的出发点是：**密集的4D像素轨迹本身蕴含了场景运动的刚性结构信息，可以作为跨视频时间对齐的统一线索**。如果能在不同视频之间建立可靠的4D轨迹对应，那么时间偏移就可以通过匹配轨迹的几何差异显式求解，而非隐式推断。

为此，本文提出将三个关键组件融合为一个联合框架：
1. **Fused Gromov-Wasserstein (FGW) 匹配**：在最优传输中同时考虑特征相似性和轨迹内几何结构，产生几何一致的跨视频轨迹对应。
2. **基于轨迹几何的DTW粗同步**：利用匹配轨迹对的几何距离矩阵，通过动态时间规整显式估计帧级时间偏移。
3. **运动样条支架**：将每视频的锚点轨迹压缩为时间连续的三次Hermite样条，使时间偏移可微，从而在4DGS的光度优化中实现同步与重建的联合细化。

这一设计使时间同步与几何重建互为约束：准确的同步提升重建质量，而高质量的重建反过来验证并细化同步参数。在Panoptic Studio多视图配置下，该方法实现了平均仅0.26帧的时间偏移误差和26.3 PSNR的新视点合成质量，验证了显式轨迹驱动同步范式的有效性。

## 核心方法与创新机理

SyncTrack4D 的核心创新在于将**跨视频4D轨迹匹配**、**最优传输时间同步**与**运动样条支架**三者耦合为一个闭环，使时间对齐与几何重建互为约束，从而首次在4DGS框架下实现亚帧级精度的未同步多视频联合重建。

### 创新一：融合几何结构的跨视频轨迹匹配

传统方法仅依赖外观特征相似性进行跨视频对应，在纹理重复或视角变化剧烈时易产生歧义匹配。SyncTrack4D 引入 **Fused Gromov-Wasserstein (FGW)** 最优传输框架，将匹配目标分解为两项：

$$\gamma^{\star} = \arg \min_{m_{a,b}} \sum_{i,k \in [N_a]} (C_{ik}^{a} - C_{jl}^{b})^{2} \gamma_{ij} \gamma_{kl} + \frac{\alpha}{2} \sum_{i,j} M_{ij}^{ab} \gamma_{ij}$$

其中第一项为**结构保真项**，约束匹配前后轨迹对之间的几何距离关系一致；第二项为**特征相似项**，衡量DINOv3特征的余弦距离。视频内几何距离定义为两轨迹在所有时间帧上的最大欧氏距离：

$$C_{ij} = \max_{t \in \mathcal{T}^{v}} \| \tau_{i,t} - \tau_{j,t} \|_2$$

这一刚性结构约束使FGW匹配在动态场景中产生几何上更一致的对应关系（见Figure 3），为后续时间同步提供了更可靠的线索。

### 创新二：显式轨迹驱动的DTW粗同步

与 **SyncNeRF**（Kim et al., AAAI 2024）通过NeRF隐式学习每视频时间偏移的机制不同，SyncTrack4D 利用已匹配的4D轨迹直接构建几何差异成本矩阵：

$$D_{ij}^{\mathrm{geo}}(t_i^a, t_j^b) = \frac{1}{N_{ab}'} \sum_{(i,j) \in \mathcal{M}_{ab}} \| \tau_{t_i}^a - \tau_{t_j}^b \|_1$$

在此成本矩阵上运行动态时间规整（DTW），以所有视频对偏移量的众数作为每视频的粗时间偏移。这种显式几何驱动的方式避免了隐式表达在时间错位下的梯度混淆，为后续细化提供了可靠的初始化。

### 创新三：运动样条支架——时间可微的轨迹表达

这是SyncTrack4D最关键的结构性创新。将MoSca的离散运动支架扩展为**时间连续的三次Hermite样条**表示：

$$\hat{\tau}_j^v(t) = \mathrm{Spline}(t + \Delta t_v; \hat{\Phi}_j^v)$$

样条参数化带来两个关键优势：
1. **时间可微性**：每视频时间偏移 $\Delta t_v$ 可直接通过光度损失反向传播梯度进行细化，使同步误差从粗同步阶段进一步收敛至亚帧级（见Figure 8）。
2. **轨迹压缩与正则化**：样条平滑先验抑制了逐帧轨迹的抖动，使4DGS重建更加稳定。

消融实验（Table 4）表明，移除运动样条支架后PSNR从27.30骤降至23.21，轨迹出现明显不连贯（Figure 9），证实了样条支架对联合优化的关键支撑作用。

### 创新四：同步与重建的联合闭环优化

上述三个创新构成闭环：FGW匹配提供轨迹对应 → DTW利用几何差异估计粗偏移 → 运动样条支架使偏移可微 → 多视频4DGS联合优化将光度误差反传至样条参数与时间偏移。联合损失函数为：

$$\mathcal{L} = \lambda_{\mathrm{photo}} \mathcal{L}_{\mathrm{photo}} + \lambda_{\mathrm{arap}} \mathcal{L}_{\mathrm{arap}} + \lambda_{\mathrm{vel}} \mathcal{L}_{\mathrm{vel}} + \lambda_{\mathrm{acc}} \mathcal{L}_{\mathrm{acc}}$$

其中ARAP正则、速度损失和加速度损失共同约束样条轨迹的物理合理性。这一设计使得时间同步不再是独立预处理步骤，而是与几何重建相互增强——更准的同步提升光度一致性，更好的几何又反过来细化匹配与偏移。

SyncTrack4D 提出了一种从**未同步多视频集合**中联合恢复时间同步与4D场景表示的多阶段框架。其核心思想是将密集4D轨迹作为统一线索，贯通跨视频运动对齐与4D高斯泼溅（4DGS）重建两个核心任务，使时间同步与几何重建互为约束。

### 输入输出

**输入**：一组未时间同步的多视角RGB视频，每段视频独立拍摄同一动态场景，但起始时间、帧率可能存在偏移。系统同时要求已知相机内参与外参（可通过前馈多视图模型或传感器获取），并利用现成模型提取深度与光流等2D先验。

**输出**：一个统一的4DGS场景表示，以及每段视频相对于参考视频的时间偏移量。该表示支持任意时刻、任意新视点的高保真渲染。

### 四阶段Pipeline

整体流程分为四个递进阶段，如图2所示：

**阶段一：每视频4D特征轨迹估计**。对每段单目视频，系统首先提取密集的4D轨迹（即场景点在时间序列上的3D位置序列），并借助4DGS优化过程嵌入DINOv3特征图，构建每视频的4D特征轨迹集合。这些轨迹同时携带外观特征与几何位置信息，为后续跨视频匹配提供基础。

**阶段二：跨视频4D轨迹匹配**。采用**Fused Gromov-Wasserstein（FGW）最优传输**框架建立不同视频间4D轨迹的对应关系。与仅依赖特征相似性的传统最优传输不同，FGW同时融合特征差异与轨迹内部的几何结构（以同一视频内两轨迹的最大欧氏距离度量），从而产生几何上更加一致的跨视频匹配对。

**阶段三：粗粒度时间同步**。基于匹配的4D轨迹对，构建几何差异成本矩阵（匹配轨迹对在给定帧对的平均L1距离），然后通过**动态时间规整（DTW）** 在成本矩阵上搜索最优单调对齐路径，估计每段视频相对于参考视频的帧级时间偏移。最终偏移取所有成对估计偏移的众数，确保全局一致性。

**阶段四：联合细化与多视频4DGS重建**。将每视频的4D轨迹及其初始时间偏移聚合到统一的**运动样条支架（motion-spline scaffold）** 中。该支架以时间连续的三次Hermite样条参数化每视频的锚点轨迹，使轨迹表示在时间域可微。在此支架下，系统联合优化高斯参数、样条控制点与每视频时间偏移，优化目标融合光度误差、ARAP正则、速度与加速度损失。光度监督驱动时间偏移从粗粒度帧级逐步收敛至亚帧级精度。

### 关键设计决策

- **显式轨迹作为统一线索**：与隐式学习时间偏移的方法（如SyncNeRF）不同，SyncTrack4D将4D轨迹显式化，使其同时服务于匹配、同步与重建，避免了隐式表达在时间错位下的退化。
- **FGW匹配的结构保持**：在跨视频匹配中引入轨迹内几何距离，使匹配对不仅特征相似，而且在各自视频内的相对空间结构保持一致，这对后续DTW同步的可靠性至关重要。
- **运动样条支架的桥梁作用**：样条支架将离散的4D轨迹压缩为时间连续表示，既为时间偏移优化提供了可微接口，又通过ARAP等正则项约束了轨迹的刚性结构，防止光度优化过程中的漂移。

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2512_04315/figures/002_Figure_2.jpg]]
*Figure 2: SyncTrack4D Pipeline. Given unsynchronized multi-video RGB inputs, we extract diverse 2D priors along with depths and camera poses from feed-forward multi-view models or sensors. (1) For each monocular video, we estimate 4D tracks and embed feature maps through 4DGS optimization. (2) We perform dense cross-video 4D track matching via a Fused Gromov–Wasserstein formulation that fuses feature similarity and geometric structure. (3) The resulting correspondences enable frame-level synchronization by minimizing intervideo motion discrepancies. (4) Finally, we aggregate all per-video 4D tracks with their initial offsets and jointly refine synchronization and geometry with a unified multi-video 4...*

SyncTrack4D 的核心思想是将 4D 轨迹作为跨视频运动对齐与 4DGS 重建的统一线索。其关键创新在于将 Fused Gromov-Wasserstein 最优传输匹配、动态时间规整粗同步与运动样条支架下的联合细化有机结合，使时间同步与几何重建互为约束。

### 运动样条支架

为支持时间偏移的可微细化，本方法将 MoSca 的运动支架扩展为**运动样条支架**：每个锚点轨迹 $\hat{\tau}_j^v$ 以时间连续的三次 Hermite 样条参数化，并合并每视频时间偏移：

$$\hat{\tau}_j^v(t) = \mathrm{Spline}\big(t + \Delta t_v; \hat{\Phi}_j^v\big)$$

其中 $\hat{\Phi}_j^v$ 为样条控制点，$\Delta t_v$ 为视频 $v$ 的时间偏移量。该表示使轨迹在时间域可微，为后续联合优化提供了基础。

### 跨视频 4D 轨迹匹配

跨视频轨迹对应是同步的核心前提。本方法采用 **Fused Gromov-Wasserstein** 框架建立对应，其目标函数为：

$$\gamma^{\star} = \arg \min_{m_{a,b}} \sum_{i,k \in [N_a]} \big(C_{ik}^{a} - C_{jl}^{b}\big)^{2} \gamma_{ij} \gamma_{kl} + \frac{\alpha}{2} \sum_{i,j} M_{ij}^{ab} \gamma_{ij}$$

式中第一项为 Gromov-Wasserstein 项，衡量轨迹集内部几何结构的保真度；第二项为特征差异项。$C_{ij}$ 定义为同一视频内两轨迹的最大欧氏距离，用于保持刚性结构：

$$C_{ij} = \max_{t \in \mathcal{T}^{v}} \| \tau_{i,t} - \tau_{j,t} \|_2$$

与仅依赖特征相似性的最优传输匹配相比，FGW 同时建模特征相似性与结构一致性，产生几何上更连贯的对应（Figure 3）。

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2512_04315/figures/003_Figure_3.jpg]]
*Figure 3: Feature-Only Optimal Transport matches and Fused Gromov–Wasserstein (FGW) matches. FGW produces geometrically more coherent correspondences by jointly modeling feature similarity and structural consistency*

### 粗时间同步

在获得跨视频匹配轨迹对 $\mathcal{M}_{ab}$ 后，定义几何差异成本矩阵：

$$D_{ij}^{\mathrm{geo}}(t_i^a, t_j^b) = \frac{1}{N_{ab}'} \sum_{(i,j) \in \mathcal{M}_{ab}} \| \tau_{t_i}^a - \tau_{t_j}^b \|_1$$

该矩阵度量匹配轨迹对在给定帧对的平均 L1 距离。随后通过 **动态时间规整** 在成本矩阵上估计每视频相对参考视频的最优时间偏移 $\Delta t_v$，选取所有成对偏移的众数作为全局粗同步结果（Figure 4）。

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2512_04315/figures/006_Figure_4.jpg]]
*Figure 4: Synchronization examples using Dynamic Time Warping (DTW). (a) Boxes, (b) Softball. DTW computes optimal monotonic correspondences (red line) between two temporal sequences. The optimal offset (green line) is selected as the mode of all estimated pairwise offsets. The softball scenes exhibit more distinctive cost maps due to their rich motion patterns*

### 联合细化

在粗同步基础上，通过多视频 4DGS 联合优化高斯参数与时间偏移。总损失函数为：

$$\mathcal{L} = \lambda_{\mathrm{photo}} \mathcal{L}_{\mathrm{photo}} + \lambda_{\mathrm{arap}} \mathcal{L}_{\mathrm{arap}} + \lambda_{\mathrm{vel}} \mathcal{L}_{\mathrm{vel}} + \lambda_{\mathrm{acc}} \mathcal{L}_{\mathrm{acc}}$$

其中 $\mathcal{L}_{\mathrm{photo}}$ 为光度误差，$\mathcal{L}_{\mathrm{arap}}$ 为尽可能刚性正则项，$\mathcal{L}_{\mathrm{vel}}$ 和 $\mathcal{L}_{\mathrm{acc}}$ 分别为速度和加速度平滑损失。运动样条支架使时间偏移可通过梯度反向传播细化，初始非同步的逐视频 4DGS 逐步收敛至同步表示（Figure 5）。

### 关键消融证据

去除运动样条支架后，PSNR 从 27.30 骤降至 23.21，且 4D 轨迹出现不连贯（Table 4, Figure 9），验证了样条支架对轨迹一致性和重建质量的关键支撑作用。

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2512_04315/figures/010_Figure_9.jpg]]
*Figure 9: Visualization of our 4D dense tracks with (left) and without (right) motion-spline scaffold*

## 实验与关键发现

### 评估设置

SyncTrack4D在两个数据集上进行评估：**Panoptic Studio**（多视图动态场景，提供真值时间偏移）和**SyncNeRF Blender**（合成动态场景，用于与SyncNeRF对比）。评估指标包括时间同步误差（帧）和新视点合成质量（PSNR、SSIM、LPIPS）。基线方法为**SyncNeRF**（Kim et al., AAAI 2024），一种基于NeRF的动态场景重建与同步方法。

需注意实验设置的几个限制：方法依赖现成的深度和光流模型，其精度直接影响最终性能；假设已知相机内外参，不适用于完全无约束场景；在动态区域稀少或静态背景过多的场景中，跟踪匹配可能退化。

### 时间同步精度

**双视图同步**（Table 1）在Panoptic Studio上按时间偏移幅度分为三个区间评估（0≤|Δt|≤10、10≤|Δt|≤30、30≤|Δt|≤50帧）。方法在大多数场景下保持较低的同步误差，例如Boxes场景在三个区间分别达到1.97、2.37、2.55帧的平均绝对偏移。但在Juggle场景的大偏移区间（30–50帧）误差升至22.62帧，表明极端时间错位下匹配质量可能显著下降。

**多视图同步**（Table 2）是核心结果：SyncTrack4D在Panoptic Studio多视图配置下，经DTW粗同步与运动样条支架光度细化后，平均时间偏移误差低至**0.260帧**，显著优于初始偏移和SyncNeRF。值得注意的是，样条拟合步骤虽轻微降低原始跟踪指标，但为后续时间偏移细化提供了时间可微结构，这是实现亚帧级精度的关键。

### 新视点合成质量

Table 3报告了新视点合成结果。在Panoptic Studio上，SyncTrack4D达到**26.3 PSNR**，显著优于SyncNeRF（具体数值未提供）。在SyncNeRF Blender数据集上同样展现出优势。未同步设置下，随着时间偏移增大，渲染质量急剧下降，验证了精确同步对高质量4D重建的必要性。

### 消融实验：运动样条支架的核心作用

Table 4和Figure 9揭示了运动样条支架的决定性贡献。**移除运动样条支架**（w/o motion-scaffold spline）后，PSNR从27.30骤降至**23.21**，降幅超过4 dB。Figure 9的定性对比显示，无样条支架时4D密集轨迹出现明显不连贯和抖动，而有样条支架的轨迹保持平滑一致。这证实了三次Hermite样条的时间连续性约束对维持轨迹几何一致性至关重要。

### 匹配策略对比

Figure 3定性展示了特征仅匹配与Fused Gromov-Wasserstein（FGW）匹配的差异。特征仅匹配产生大量语义模糊的误匹配（如将不同人体部位错误关联），而FGW通过联合建模特征相似性与轨迹内几何结构，产生几何上更一致的对应关系。这一优势源于FGW目标函数中结构失真项对刚性结构的保持作用。

### 同步收敛行为

Figure 8展示了时间偏移在4DGS联合细化阶段的收敛曲线。初始DTW粗同步已接近真值，经多视频4DGS光度优化后，各相机的时间偏移进一步收敛至极小误差，且相机间偏差很小。Figure 5的可视化也佐证了从未同步到同步表示的收敛过程。

### 失败模式与局限性

尽管整体表现优异，方法存在以下已知失败模式：
- **大偏移退化**：Table 1中Juggle场景在30–50帧偏移区间误差达22.62帧，表明当动态区域运动模式复杂且时间错位极大时，FGW匹配和DTW同步可能失效。
- **静态场景退化**：在动态区域极小或静态背景过多的场景中，4D跟踪匹配缺乏足够的运动线索，同步质量可能下降。
- **先验依赖**：深度和光流先验来自现成模型，其误差会传播至跟踪和匹配阶段，影响最终重建精度。

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2512_04315/figures/012_Table_4.jpg]]
*Table 4: Ablation study of multi-video 4DGS. We report PSNR↑, SSIM↑, and LPIPS↓*

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2512_04315/figures/008_Figure_6.jpg]]
*Figure 6: Qualitative comparison of rendered novel view images on CMU Panoptic Studio dataset*

## 定位与知识库关联

### 与现有工作的关系

SyncTrack4D 处于**多视频4D重建**与**视频同步**的交叉点，其核心思路是将显式4D轨迹作为统一线索，桥接跨视频匹配、时间对齐与高斯泼溅重建三个环节。这一设计使其与以下几条工作线形成明确的继承与差异化关系：

**相对于4DGS重建方法**：现有4DGS方法（如4D Gaussian Splatting系列）通常依赖硬件同步的多视角视频，通过隐式变形场或离散4D轨迹建模动态场景。SyncTrack4D 的关键改变在于引入**运动样条支架（motion-spline scaffold）**——将每视频的密集4D锚点轨迹压缩为时间连续的三次Hermite样条参数化表示。这一设计不仅提供了时间可微结构以支持偏移细化，还使跨视频轨迹对齐成为可能。消融实验表明，移除运动样条支架后PSNR从27.30骤降至23.21，且4D轨迹出现明显不连贯（Table 4, Figure 9），验证了样条支架对重建质量的结构性支撑作用。

**相对于视频同步方法**：**SyncNeRF**（Kim et al., AAAI 2024）是基于NeRF的动态场景重建与同步方法，通过隐式学习每视频时间偏移实现同步。SyncTrack4D 与之形成两条不同的技术路线：SyncNeRF 将同步嵌入隐式辐射场优化中，而 SyncTrack4D 采用**显式轨迹驱动的两阶段同步**——先通过匹配轨迹的几何差异进行DTW粗同步，再在运动样条支架下进行光度细化。在Panoptic Studio多视图配置下，SyncTrack4D 的平均时间偏移误差低至0.26帧（Table 2），显著优于SyncNeRF和初始偏移，表明显式轨迹线索在同步精度上具有优势。

**相对于跨视频匹配方法**：传统最优传输匹配仅依赖特征相似性建立对应。SyncTrack4D 引入**Fused Gromov-Wasserstein（FGW）框架**，在特征匹配成本之外融合轨迹内几何结构约束——以同一视频内两轨迹的最大欧氏距离 $C_{ij} = \max_{t \in \mathcal{T}^{v}} \| \tau_{i,t} - \tau_{j,t} \|_2$ 保持刚性结构。Figure 3 的定性对比显示，FGW匹配比纯特征匹配产生几何上更一致的对应关系，这一改进直接提升了后续DTW同步和联合优化的输入质量。

### 适用边界与局限

SyncTrack4D 的设计隐含若干前提假设，超出这些边界时性能可能退化：

1. **相机参数依赖**：方法假设已知相机内外参，通过前馈多视图模型或传感器获取深度和位姿。这使其不适用于完全无约束的野外视频集合，与某些纯自监督重建方法相比，部署灵活性受限。

2. **先验模型精度瓶颈**：深度和光流先验依赖现成模型（如DINOv3特征提取），这些模型的误差会直接传导至4D轨迹估计和后续匹配。论文未单独量化先验误差对最终同步精度的影响，这一误差传播链的鲁棒性有待进一步验证。

3. **动态区域密度敏感**：方法以密集4D轨迹为同步线索。在动态区域稀少或静态背景占主导的场景中，可用于匹配的轨迹数量不足，可能导致DTW同步退化。Table 1中basketball和football场景在较大偏移带（30–50帧）下误差显著升高（分别达9.87和8.84帧），暗示动态复杂度与同步难度之间存在非线性关系。

4. **离线处理限制**：当前管道为离线设计，无法满足实时或在线视频同步需求。多阶段流程（逐视频跟踪→跨视频匹配→DTW同步→联合优化）的计算开销使其难以直接迁移到流式场景。

### 开放问题

论文指出的未来方向包括：将方法扩展到在线多视频设置；在轨迹匹配框架中引入显式实例分割以提升语义一致性；利用多模态线索增强同步鲁棒性。此外，从知识库定位角度看，以下问题值得关注：

- **与基于事件的同步方法的融合潜力**：当前方法完全依赖RGB轨迹，若能与事件相机或IMU等异步传感器融合，可能在高速运动或光照剧变场景中获得更稳健的同步信号。
- **样条支架的泛化能力**：运动样条支架在Panoptic Studio和SyncNeRF Blender上验证有效，但其对更复杂运动模式（如非刚体形变、拓扑变化）的建模能力尚未被充分探索。
- **同步精度下界**：0.26帧的平均误差已接近亚帧级精度，但论文未分析误差的理论下界——这一下界可能由相机帧率、轨迹估计噪声和场景动态频率共同决定。

## 原文 PDF

![[paperPDFs/arxiv_2025/SyncTrack4D_Cross_Video_Motion_Alignment_and_Video_Synchronization_for_Multi_Video_4D_Gaussian_Splatting.pdf]]
