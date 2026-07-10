---
title: Searching for Fast Demosaicking Algorithms
type: paper
paper_level: A
venue: SIGGRAPH
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_2022/Searching_for_Fast_Demosaicking_Algorithms.pdf
project_link: null
code_link: "https://github.com/NVIDIAGameWorks/Falcor"
aliases:
- RB
- SFDA
tags:
- SIGGRAPH_2022
- topic/other_unclear
core_operator: 将双向路径追踪（BDPT）引入ReSTIR框架，通过扩展路径空间以包含采样技术信息、设计双向混合移位映射、分离焦散存储区及递归MIS权重计算，从而大幅提升采样质量和交互性能。
primary_logic: 在广义重采样重要性采样（GRIS）理论下，将路径与生成技术配对扩展为路径-技术对，允许在重用过程中保留技术信息，避免了传统双向路径复用中的偏差问题，同时利用双向路径的多样采样策略高效捕获焦散路径。
claims:
- 在仅由灯泡内灯丝照明的Bathroom场景中，1920×1080分辨率下，本文方法在70ms内达到MAPE 0.312，而ReSTIR PT在71ms内MAPE为1.368，误差降低约4.4倍。
- 在多个焦散场景的交互式渲染中，本文方法在1spp下显著优于等时运行的ReSTIR PT，能正确解析焦散并降低噪声。
- 使用焦散存储区和时间重用的动画焦散渲染中，方法能够保留墙面上的细小焦散细节，而ReSTIR PT仅能捕获直接照明。
- Bathroom 场景 (Fig. 1) 上 MAPE (mean absolute percentage error) = 0.312
---

# Searching for Fast Demosaicking Algorithms

> [!tip] 核心洞察
> 在广义重采样重要性采样（GRIS）理论下，将路径与生成技术配对扩展为路径-技术对，允许在重用过程中保留技术信息，避免了传统双向路径复用中的偏差问题，同时利用双向路径的多样采样策略高效捕获焦散路径。

| 字段 | 内容 |
|------|------|
| 中文题名 | ReSTIR BDPT：双向ReSTIR路径追踪与焦散渲染 |
| 英文题名 | Searching for Fast Demosaicking Algorithms |
| 会议/期刊 | SIGGRAPH 2022 |
| Links | [Code](https://github.com/NVIDIAGameWorks/Falcor) |
| Topic | #topic/other_unclear |
| Method | ReSTIR BDPT |
| Dataset | Bathroom 场景, Veach Bidir 动画焦散 |

> [!tip] 效果简介
> - Bathroom 场景 (Fig. 1) 上，MAPE (mean absolute percentage error) 0.312 vs 1.368 (ReSTIR PT) (降低 1.056（约4.4倍改善）)。
> - 多场景测试 (Sponza, White Room, Breakfast Room 等, Fig. 11) 上，等时间视觉质量 / 噪声水平 焦散细节清晰，整体噪声低 vs 焦散缺失或模糊，噪声高 (定性大幅改善)。
> - Veach Bidir 动画焦散 (Fig. 9) 上，时间焦散保持质量 随时间重用保持墙面焦散细节 vs 仅捕获周围直接照明 (显著提升焦散稳定性)。

## 概要

现有基于单向路径追踪的实时重采样方法（ReSTIR PT）在焦散和难以到达光源的场景中采样效率极低，导致高误差与视觉质量严重退化。本文提出 **ReSTIR BDPT**，将双向路径追踪（BDPT）引入 ReSTIR 框架，在广义重采样重要性采样（GRIS）理论下扩展路径空间为路径-技术对，设计双向混合移位映射，并分离焦散存储区进行时间重用，从而高效捕获焦散路径。在仅由灯泡内灯丝照明的 Bathroom 场景中，1920×1080 分辨率下，本方法在 70 ms 内达到 MAPE 0.312，而 ReSTIR PT 在 71 ms 内 MAPE 为 1.368，误差降低约 4.4 倍。多个焦散场景的交互式渲染结果表明，本方法在 1 spp 下能正确解析焦散并显著降低噪声，且在动画焦散中可保持墙面细小焦散细节。然而，在光源贡献小的场景（如 Bistro Interior）中，方法效率可能退化至接近 ReSTIR PT。该方法定位为实时重采样框架下首个支持高效双向路径重用的工作，在焦散密集型场景中填补了 ReSTIR 系列的关键能力缺口。

## 核心方法与创新机理

### 问题瓶颈：单向路径追踪在焦散与困难光源前的失效

现有实时重采样路径追踪方法 **ReSTIR PT**（Lin et al., SIGGRAPH 2022）建立在单向路径追踪之上，仅使用两种采样技术：直接命中发光体的零顶点技术（s=0）和下一事件估计（s=1）。这导致两个根本性困难：（1）当光源被玻璃灯罩等折射介质包围时，单向路径几乎不可能随机命中灯丝，产生极高方差；（2）焦散路径（镜面-漫反射-镜面链路）对单向采样极不友好，使得交互式渲染中焦散细节完全丢失。在仅由灯泡内灯丝照明的 Bathroom 场景中，ReSTIR PT 在 71ms 内 MAPE 高达 1.368，误差是本文方法的 4.4 倍。

### 核心洞察：在扩展路径空间中保留采样技术信息

本文的核心创新在于将广义重采样重要性采样（GRIS）理论应用于一个**扩展的路径空间**。传统 ReSTIR 将路径视为无结构的样本点，在空间和时间重用中丢失了路径是由哪种采样技术生成的信息。本文的关键洞察是：将路径样本 $\bar{x}$ 与生成它的采样技术索引 $\tau = (s,t)$ 配对，形成扩展路径 $\hat{x} = (\bar{x}, \tau)$。在这一扩展空间中，像素强度的积分被重新表述为：

$$I = \int_{\hat{\Omega}} \omega_{\tau}(\bar{x}) f(\bar{x}) \, \mathrm{d}(\bar{x}, \tau)$$

其中 $\omega_{\tau}(\bar{x})$ 是技术特定的 MIS 权重，$f(\bar{x})$ 是测量贡献函数。GRIS 的目标函数相应地变为：

$$\hat{p}(\hat{x}) = \omega_{\tau}(\bar{x}) \hat{q}(\bar{x})$$

这意味着在重采样过程中，每条路径的质量评估 $\hat{q}$ 被其对应技术的 MIS 权重加权。这一形式化处理使得不同采样技术（包括光源追踪技术 t≤1）生成的路径可以在统一的 GRIS 框架下被公平地重用，避免了传统双向路径复用中因忽略技术信息而引入的偏差。

### Changed Slot 1：从单向到双向的路径生成

**基线（ReSTIR PT）**：仅使用 s=0 和 s=1 技术，光源子路径不存在。

**本文（ReSTIR BDPT）**：完整采用双向路径追踪的所有 $(s,t)$ 技术组合，特别引入 $t \leq 1$ 的光源追踪技术（light tracing）。光源追踪从光源出发采样子路径，能够高效地穿过玻璃等折射介质找到焦散路径——这正是单向路径追踪的致命弱点。

### Changed Slot 2：技术感知的双向混合移位映射

移位映射是 ReSTIR 中实现路径重用的核心操作：将一条在像素 A 处采样的路径变换为像素 B 处的有效路径。本文设计了**技术特定的双向混合移位映射** $T_{\tau}$，根据路径的技术类型 $\tau = (s,t)$ 选择不同策略：

- **$t > 1$ 且 $s > 0$（存在子路径连接）**：采用混合移位。相机子路径从目标像素出发进行随机重放（random replay），光源子路径从光源出发进行反向随机重放，在首个粗糙光源顶点处进行重连（reconnection）。这与 Lin et al. 的混合移位结构一致，但扩展为双向形式。
- **$t \leq 1$（光源追踪技术）**：仅使用随机重放。从光源出发重放光源子路径至第二个击中点，若该点为粗糙表面则可重连至相机子路径；否则仅使用重放部分。
- **重连约束**：仅允许在采样时被分类为粗糙表面的顶点进行子路径连接（遵循 Manzi et al. 2015 的策略），避免在镜面顶点处引入不可靠的移位。

移位 Jacobian 的计算继承自 ReSTIR PT 的框架：相机子路径随机重放的面积测度 Jacobian 为 $|\partial x_i' / \partial x_i| = |\overrightarrow{p_i} / \overrightarrow{p_i}'|$，光源子路径类似处理。

### Changed Slot 3：分离的焦散存储区与时间重用

焦散路径的特殊性在于其贡献高度集中在特定像素区域，且对移位映射的可见性变化极为敏感。本文设计了**每像素独立的焦散存储区（caustic reservoir）**，与常规存储区完全分离：

- **不参与空间重用**：焦散存储区仅在时间维度上进行重用，避免了空间重连因可见性不一致导致的焦散细节丢失。
- **时间重用机制**：对焦散存储区中的路径应用随机重放移位（不进行重连），生成当前帧对应像素的新路径。
- **代理置信度更新**：使用前一帧的漫反射运动向量将焦散存储区映射到当前帧，以映射后的置信度作为时间重用的权重。这虽非焦散运动的精确建模，但在实践中能有效累积动态场景下的焦散质量。

### 模块管线与因果关系

本文方法的 GPU 实现由四个核心模块组成，按帧顺序执行：

**模块 1：光源子路径采样（Algorithm 1: SampleLightPaths）**
并行追踪 $N_L$ 条光源子路径，将可连接的粗糙顶点原子追加至全局光源顶点缓存（Light Vertex Cache, LVC），同时将完整的光追踪路径以 key-value 形式插入光源存储区映射（Light Reservoir Map, LRM），供后续像素采样时合并。

**模块 2：初始路径采样（Algorithm 2: SampleInitialPaths）**
每个像素独立采样相机子路径。对于 $s > 1$ 技术，在相机子路径的粗糙顶点处从 LVC 中均匀选取光源顶点形成全路径。同时，将 LRM 中对应像素的光追踪路径合并至该像素的常规存储区和焦散存储区，完成初始候选路径的生成。

**模块 3：时空重用与移位（Algorithm 3: ShiftPath）**
对选中的存储路径应用双向混合移位映射。根据路径的技术类型执行相机/光源子路径的随机重放与重连，生成目标像素域中的新路径，计算移位 Jacobian，并将成功移位的路径合并至目标像素的存储区。此模块同时处理空间重用（相邻像素间）和时间重用（前后帧间）。

**模块 4：焦散存储区管理**
独立维护每像素的焦散存储区，仅执行时间重用（随机重放移位），使用运动向量代理置信度更新权重，确保动态场景下焦散质量的稳定累积。

**因果链路**：模块 1 提供了传统 ReSTIR PT 不具备的光源子路径信息 → 模块 2 利用 LVC 和 LRM 生成包含双向技术的初始候选路径 → 模块 3 通过技术感知的移位映射实现高效重用 → 模块 4 解决焦散路径在空间重用中的特殊困难。四个模块共同实现了从“单向路径采样”到“双向路径采样+技术感知重用+焦散专用存储”的完整链路。

### 递归 MIS 权重计算

空间重用中的关键挑战是：移位后的路径需要正确的 MIS 权重 $\omega_{\tau}$，但完整重算代价高昂。本文采用 van Antwerpen (2011) 的递归 MIS 框架，在路径顶点处增量缓存中间量：

- **$d_i^{\mathrm{p}}$**：沿子路径累积的基础量，更新规则为 $d_i^{\mathrm{p}} = [x_{i-1} \text{ nondelta}] \left(1 / \overrightarrow{\rho_i}\right)^{\beta}$，其中 $\overrightarrow{\rho_i}$ 是前向采样概率密度。
- **$d_i^{\mathrm{vc}}$**：累积的连接权重量，更新规则为 $d_i^{\mathrm{vc}} = \left(\overleftarrow{g_{i-1}} / \overrightarrow{p_i}\right)^{\beta} \left([x_{i-1} \text{ nondelta}] d_{i-1}^{\mathrm{vc}} + (1 / \overrightarrow{\rho_i}) d_{i-1}^{\mathrm{p}}\right)$。

最终 MIS 权重由相机和光源子路径在连接顶点处的累积量组合得到：
$$\omega_{\tau} = \left(\bar{w}_{s-1}(\bar{y}) + 1 + \bar{w}_{t-1}(\bar{z})\right)^{-1}$$

这一递归计算仅需连接顶点处的局部信息，避免了遍历全路径的开销，使得在 GPU 上实时重算 MIS 权重成为可能。实验表明，空间重用中复制 MIS 权重（有偏快速变体）会引入明显偏差，而使用递归重连重算可消除该偏差，获得更低误差。

![[assets/figures/papers/sig_p2_36k_l3_https_cseweb_ucsd_edu_tzli/figures/001_Figure_1.jpg]]
*Figure 1: We combine bidirectional path tracing with a novel reuse scheme to enable ReSTIR [Wyman et al. 2023] to better find hard-to-reach light sources and even resolve caustics interactively. Only emissive filaments inside the glass blubs light this Bathroom scene. At a 1920×1080 resolution, our method achieves a mean absolute percentage error (MAPE) of 0.312 in 70ms (with 1M light subpaths), while ReSTIR PT [Lin et al. 2022] achieves a MAPE of 1.368 in 71ms*

## 实验与关键发现

### 主结果：焦散场景的误差大幅降低

本文在多个焦散照明场景中，以等时间协议（通过增加对比方法的初始候选路径数使总渲染时间持平）与 **ReSTIR PT**（Lin et al., SIGGRAPH 2022）进行对比。最关键的定量结果来自 Bathroom 场景（仅由灯泡内灯丝照明，1920×1080 分辨率）：本文方法在 70ms 内达到 MAPE（mean absolute percentage error）0.312，而 ReSTIR PT 在 71ms 内 MAPE 为 1.368，误差降低约 **4.4 倍**（Fig. 1）。这一差异源于双向路径追踪能够高效采样从光源出发、经镜面折射后到达场景的焦散路径，而单向路径追踪仅靠命中发光体或下一事件估计（NEE）几乎无法捕获此类路径。

在多个场景的交互式渲染中（Sponza、White Room、Breakfast Room 等，Fig. 11），本文方法在 1spp 下等时运行均能正确解析焦散并显著降低噪声，而 ReSTIR PT 在这些场景中焦散缺失或模糊。在 Veach Bidir 动画焦散场景中（Fig. 9），光源从右向左移动，光线经玻璃蛋聚焦形成焦散；本文方法通过分离的焦散存储区（caustic reservoir）与光源子路径随机重放的时间重用，能够在墙面上保留细小焦散细节，而 ReSTIR PT 仅能捕获周围的直接照明。

![[assets/figures/papers/sig_p2_36k_l3_https_cseweb_ucsd_edu_tzli/figures/009_Figure_9.jpg]]
*Figure 9: The Veach Bidir scene with animated caustics rendered with 1 sample per pixel. The light moves from right to left during animation, focusing light through the glass egg. With light subpath random replay and separate caustic reservoirs, our work temporal resamples the caustics, even capturing smaller details on the wall. Note: the light around the egg’s shadow captured by ReSTIR PT is direct illumination, not a caustic*

在交互帧率方面，RTX 4090 上 1920×1080 分辨率下单帧约 50ms（含 1M 光源子路径），与 ReSTIR PT 的约 70ms 相当或略快，但在此时间预算内误差大幅降低。

### 离线收敛对比

在离线模式下（3 次空间重用，每次 6 个候选，无时间重用），本文方法与标准 BDPT（Veach and Guibas, SIGGRAPH 1995）及 ReSTIR PT 进行了收敛性对比（Fig. 12）。本文方法由于双向采样改善了候选分布，误差低于 ReSTIR PT。标准 BDPT 在相同时间内能累积更多样本，但重采样使每样本误差更低——这一差异体现了 GRIS 框架在候选质量与样本数量之间的权衡。

### 关键消融实验

**粗糙度阈值的影响（Fig. 7）**：在 Veach Bidir 场景中（含粗糙度纹理的金属桌面），过大的粗糙度阈值会禁用粗糙表面上的双向连接（包括 NEE），迫使系统使用效率较低的移位映射，导致噪声增加。该消融直接验证了“仅在粗糙顶点处允许子路径连接”这一设计决策的必要性。

**光源追踪技术的消融（Fig. 8）**：移除 t ≤ 1 技术（即仅保留相机路径追踪，类似 Liu and Gan 2023、Nabata et al. 2020 的做法）后，当场景主要由焦散照明时，采样效率极大降低。光源追踪技术能从光源出发高效采样经镜面折射的焦散路径，而标准路径追踪几乎无法找到此类路径。该实验确立了双向采样策略中光源子路径的不可替代性。

**MIS 权重计算的偏差消融（Fig. 5）**：在空间重用中直接复制未移位的 MIS 权重会引入偏差，而使用递归重连 MIS 重算（Section 6 方法）可以消除该偏差，获得更低的误差。该消融证明了在扩展路径空间中进行技术感知的 MIS 权重重算对无偏性的关键作用。

### 失败模式与适用边界

**光源贡献小的场景（Fig. 10）**：在 Bistro Interior 场景中，大部分场景灯光对图像贡献极小，光源追踪难以采样到高贡献路径（尤其是墙上的焦散）。此时本文方法性能与单向 ReSTIR PT 相近，甚至因额外开销而略低。这表明方法的优势高度依赖于场景中存在可被光源追踪高效捕获的焦散或难以到达的光源。

**SDS 路径的已知局限**：镜面-漫反射-镜面（SDS）光路仍然是双向采样的固有问题，本文方法未提供专门解决方案，作者指出未来可结合顶点合并或流形移位技术。

**动画焦散的运动向量限制**：当前焦散存储区的时间重用依赖基于漫反射表面运动向量的代理置信度更新，未针对焦散运动进行优化，在复杂动态焦散场景中可能不够理想。

**光源子路径移位实现的工程局限**：光源子路径的移位未独立优化，与相机子路径移位混在同一 GPU 调度中，存在线程分化问题，可能影响大规模并行效率。

### 公平性说明

所有等时间比较均通过增加对比方法的初始候选路径数来补偿本文方法的光源子路径追踪开销。APEX 误差指标使用 MAPE，在参考值极低时可能不稳定，但本文主要关注高贡献焦散区域（该处参考值较高），因此该指标具有参考意义。

![[assets/figures/papers/sig_p2_36k_l3_https_cseweb_ucsd_edu_tzli/figures/005_Figure_5.jpg]]
*Figure 5: Relative error offset (i.e*

![[assets/figures/papers/sig_p2_36k_l3_https_cseweb_ucsd_edu_tzli/figures/007_Figure_7.jpg]]
*Figure 7: The Veach Bidir scene with a metallic table with a roughness texture, rendered with different roughness thresholds. Using too large of a threshold disables bidirectional connections (including NEE) on rough surfaces, and leads us to select less efficient shift mappings, which produces more noise*

![[assets/figures/papers/sig_p2_36k_l3_https_cseweb_ucsd_edu_tzli/figures/008_Figure_8.jpg]]
*Figure 8: Without light tracing (?? ≤ 1) techniques (as in [Liu and Gan 2023; Nabata et al. 2020]), scenes lit by caustics are difficult to sample. Light tracing techniques very efficiently sample caustics, while standard path tracing struggles to find such paths*

![[assets/figures/papers/sig_p2_36k_l3_https_cseweb_ucsd_edu_tzli/figures/010_Figure_10.jpg]]
*Figure 10: Results with 1 sample per pixel in the Bistro Interior. In this scene, light tracing struggles to sample high-contribution paths, especially the caustics on the wall, as most scene lights do not contribute to the image. Our method performs similarly to unidirectional ReSTIR in this case*

## 定位与知识库关联

本文的核心改动在于将 **ReSTIR 框架的路径空间从单向路径追踪扩展为双向路径追踪**，具体而言是将 GRIS 的采样域从纯路径样本 $\bar{x}$ 扩展为路径-技术对 $(\bar{x}, \tau)$，使得重采样过程能够保留并利用生成路径的采样技术信息。这一改动直接针对现有 ReSTIR PT（Lin et al., SIGGRAPH 2022）的一个结构性盲区：其路径生成仅使用单向技术（$s=0$ 的命中发光体与 $s=1$ 的下一事件估计），导致焦散路径和难以到达光源的场景采样效率极低。相比之下，本文引入标准 BDPT（Veach and Guibas, SIGGRAPH 1995）的全套 $s,t$ 技术，特别是 $t \leq 1$ 的光源追踪技术，从根本上改变了候选样本的分布质量。

**改变的 slot 定位**：相对 ReSTIR PT，本文在五个关键 slot 上做出了实质性替换或新增：
1. **路径生成方式**：从单向路径追踪扩展为全双向路径追踪，包含光源子路径追踪。
2. **GRIS 路径空间**：从纯路径空间扩展为路径-技术对空间，目标函数由技术 MIS 权重加权。
3. **移位映射**：从单向混合移位扩展为双向混合移位，对 $t>1$ 路径在首次粗糙光源顶点重连，对 $t \leq 1$ 路径使用光源侧随机重放。
4. **焦散处理**：新增独立的焦散存储区（caustic reservoir），仅进行时间重用。
5. **MIS 权重计算**：从简单复制或全路径重算，改为基于递归重连的局部 MIS 更新。

**知识库挂载点**：本文可挂载到渲染知识库的以下节点：
- **实时重采样路径追踪**：作为 ReSTIR 系列（Bitterli et al., SIGGRAPH 2020; Lin et al., SIGGRAPH 2022; Wyman et al., 2023）的扩展，将双向采样纳入 GRIS 理论框架。
- **双向路径追踪的实时化**：将传统离线 BDPT 通过重采样重用机制推向交互式帧率，与 Manzi et al.（2015）的粗糙表面连接策略和 van Antwerpen（2011）的递归 MIS 形成继承关系。
- **焦散实时渲染**：通过分离的焦散存储区和光源追踪技术，为交互式焦散渲染提供了新的技术路线，区别于光子映射（photon mapping）和屏幕空间方法。

**适用边界**：本文方法在焦散主导或光源难以到达的场景中优势显著——在 Bathroom 场景中，70ms 内 MAPE 从 ReSTIR PT 的 1.368 降至 0.312（约 4.4 倍改善）。然而，当场景中光源贡献小、焦散不突出时（如 Bistro Interior），光源追踪的额外开销可能导致性能略低于 ReSTIR PT，视觉差异不大。此外，镜面-漫反射-镜面（SDS）路径仍然是双向采样的已知局限，本文未予解决。

**后续启发**：
1. 焦散存储区的运动向量代理置信度更新目前基于漫反射假设，针对焦散运动优化可能进一步提升动画焦散质量。
2. 递归重连 MIS 所需的额外缓存量对存储区大小的影响值得量化分析，以评估在更大规模场景中的可扩展性。
3. 在漫反射照明为主的场景中，结合相机信息引导光源子路径采样可能弥补当前方法的效率短板。
4. 移位过程中因可见性变化（V-Buffer 不一致）导致的重用冲突，可通过更精细的可见性验证或自适应重用策略加以改善。
5. 焦散存储区与常规存储区之间的动态合并策略可能进一步提升路径利用效率。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2022/Searching_for_Fast_Demosaicking_Algorithms.pdf]]