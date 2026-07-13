---
title: "Neural Fields meet Explicit Geometric Representations for Inverse Rendering of Urban Scenes"
type: paper
paper_level: A
venue: CVPR
year: 2023
pdf_ref: paperPDFs/CVPR_2023/Neural_Fields_meet_Explicit_Geometric_Representations_for_Inverse_Rendering_of_Urban_Scenes.pdf
code_link: null
project_link: https://research.nvidia.com/labs/toronto-ai/fegr/
aliases:
- NFMEGRIRUS
tags:
- CVPR_2023
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "提出混合延迟渲染管线：神经场体积渲染生成G缓冲区，从有符号距离场提取显式网格，利用OptiX高效计算二次光线可见性，将光照分解为一次光线（体积渲染）与二次光线（网格光追）。"
primary_logic: "神经场的高分辨率细节与显式网格的快速光线求交相结合，并利用语义分割先验正则化光照，从而在城市场景逆渲染中首次实现逼真的重光照与带阴影的虚拟物体插入。"
claims:
- "Our method uses a neural field for primary rays and an explicit mesh for secondary rays to produce higher-order lighting effects."
- "FEGR significantly outperforms NeRF-OSR on relighting across all three scenes, e.g., PSNR 21.53 vs 19.34 on Site 1."
- "Combining neural field with explicit mesh is crucial; ray-traced shadows and exposure compensation boost PSNR by up to 1.5 dB."
- "User study: 86.2% prefer our method over Hold-Geoffroy et al., 68.9% prefer over Wang et al. for virtual object insertion."
---

# Neural Fields meet Explicit Geometric Representations for Inverse Rendering of Urban Scenes

> [!tip] 核心洞察
> 神经场的高分辨率细节与显式网格的快速光线求交相结合，并利用语义分割先验正则化光照，从而在城市场景逆渲染中首次实现逼真的重光照与带阴影的虚拟物体插入。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 神经场与显式几何表示结合的城市场景逆渲染 |
| 英文题名 | Neural Fields meet Explicit Geometric Representations for Inverse Rendering of Urban Scenes |
| 会议/期刊 | CVPR 2023 |
| Links | [paper](https://arxiv.org/abs/2304.03266) · [Project](https://research.nvidia.com/labs/toronto-ai/fegr/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | FEGR |
| Dataset | NeRF-OSR Site 1, NeRF-OSR Site 2, NeRF-OSR Site 3, Virtual Object Insertion User Study |

> [!tip] 效果简介
> - NeRF-OSR Site 1 上，PSNR (dB) ↑ 为 21.53，对比 19.34 (NeRF-OSR)，变化 +2.19。
> - NeRF-OSR Site 2 上，PSNR (dB) ↑ 为 17.00，对比 16.35 (NeRF-OSR)，变化 +0.65。
> - NeRF-OSR Site 3 上，PSNR (dB) ↑ 为 17.57，对比 15.66 (NeRF-OSR)，变化 +1.91。

## 概要

### 问题与瓶颈

从多视角图像中恢复场景的几何、材质与光照（即逆渲染）是计算机视觉与图形学的长期目标。基于神经辐射场的逆渲染方法虽然在场景重建上取得了显著进展，但其核心瓶颈在于体积积分的时间复杂度为 $O(nm)$，无法高效渲染二次光线（如阴影、高光），导致重光照与虚拟物体插入效果受限。另一方面，基于显式网格的方法虽能进行快速光线求交，却受限于分辨率，难以处理大规模城市场景的复杂细节。

### 核心洞察

FEGR 的核心洞察在于将神经场的高分辨率细节能力与显式网格的快速光线求交能力相结合：**一次光线**由神经场通过体积渲染生成 G 缓冲区（法向、基色、材质、深度），**二次光线**则利用从有符号距离场（SDF）提取的显式网格，通过 OptiX 高效计算可见性与着色。这一混合延迟渲染管线从根本上解耦了场景表示与光照计算，使城市场景逆渲染首次实现了逼真的重光照与带阴影的虚拟物体插入。

### 方法定位

FEGR 属于**基于物理的逆渲染方法**，与现有工作的关键区别在于：

- 相对于纯神经场方法（如 **NeRF-OSR**，Rudnev et al., ECCV 2022），FEGR 引入显式网格进行二次光线追踪，突破了体积积分对高阶光照效果（投射阴影、环境光遮蔽）的限制。
- 相对于基于网格的逆渲染方法（如 **Nvdiffrecmc**，Hasselgren et al., arXiv 2022），FEGR 利用神经场的高分辨率表示能力，避免了网格分辨率对场景细节的约束。
- 在光照建模上，FEGR 采用带有哈希编码的 HDR 天空穹顶 MLP，支持高频率方向光，并引入语义感知的遮阴先验损失正则化 HDR 环境光估计，这是现有工作中尚未出现的机制。

### 主要结果

在 NeRF-OSR 数据集上，FEGR 在所有三个场景的重光照任务中均显著优于 NeRF-OSR：Site 1 的 PSNR 提升 **+2.19 dB**（21.53 vs 19.34），Site 3 提升 **+1.91 dB**（17.57 vs 15.66）。消融实验表明，显式网格的二次光线追踪与曝光补偿分别贡献了高达 1.5 dB 的增益。在虚拟物体插入的用户调研中，86.2% 的参与者偏好 FEGR 的结果（对比 Hold-Geoffroy et al., CVPR 2019），68.9% 的参与者偏好 FEGR（对比 Wang et al., ECCV 2022），验证了其在 AR/VR 应用中的实用价值。

城市场景的真实感渲染与编辑是计算机视觉和图形学中的核心挑战，其应用涵盖增强现实、虚拟现实和自动驾驶仿真。要从一组带位姿的相机图像中恢复场景的内在属性——几何结构、空间变化材质和高动态范围（HDR）光照——并支持重光照和虚拟物体插入，需要解决**逆渲染**问题。

现有方法主要沿两条技术路线展开。基于**神经辐射场（NeRF）**的逆渲染方法（如 **NeRF-OSR**，Rudnev et al., ECCV 2022）利用体积渲染对场景进行隐式建模，能够重建高分辨率的几何和外观细节。然而，这类方法的根本瓶颈在于：体积积分需要在每条光线上密集采样，复杂度为 $O(nm)$（$n$ 为采样点，$m$ 为光线数），这使得它们**无法高效地渲染二次光线**——即从表面点出发、用于计算阴影、高光和间接光照的辅助光线。因此，基于纯神经场的方法难以产生逼真的高阶光照效果，如清晰的投射阴影。

另一条路线采用**显式网格表示**，通过网格和物理基础的光线追踪实现快速可见性计算。但基于网格的方法受限于网格分辨率，在建模大规模城市场景时面临存储和计算开销的巨大压力，难以同时保证几何精度和材质细节。

这两类方法的互补特性揭示了一个明确的研究缺口：**如何将神经场的高分辨率细节表达能力与显式网格的高效光线求交能力结合起来**，从而在城市场景逆渲染中同时实现高质量的几何重建和物理上正确的光照效果？此外，现有方法在光照建模上多采用低阶球谐系数或简单的环境网络，无法捕捉HDR环境光中的高频方向性信息（如太阳），进一步限制了重光照的真实感。

本文的动机正是填补这一缺口。我们提出 **FEGR**（Neural Fields meet Explicit Geometric Representations），一种混合延迟渲染框架：利用神经场处理一次光线，产生包含法向、基色、材质和深度的G缓冲区；同时从底层有符号距离场（SDF）中提取显式网格，借助 OptiX 高效计算二次光线的可见性，从而在城市场景中首次实现带逼真阴影的重光照和虚拟物体插入。

## 核心方法与创新机理

FEGR的核心创新在于**将神经场的高分辨率细节表达能力与显式网格的高效光线求交能力解耦并协同**，构建了一条混合延迟渲染管线，从而在城市场景逆渲染中首次实现逼真的高阶光照效果（阴影、高光）和带阴影的虚拟物体插入。

### 关键机制：一次光线与二次光线的分工

此前的NeRF类逆渲染方法（如**NeRF-OSR**，Rudnev et al., ECCV 2022）依赖纯体积积分来渲染所有光线，其计算复杂度为$O(nm)$（$n$为采样点数，$m$为二次光线数），这使得对阴影和全局光照所需的二次光线进行密集采样在计算上不可行。基于网格的方法（如**Nvdiffrecmc**，Hasselgren et al., arXiv 2022）虽能高效追踪二次光线，但受限于网格分辨率，难以捕捉城市场景的复杂几何细节。

FEGR的解决方案是将渲染任务一分为二（Figure 2）：

1. **一次光线（Primary Rays）—— 神经场体积渲染**：相机光线通过神经本征场（Neural Intrinsic Field）进行体积积分，生成高分辨率的G缓冲区（法向、基色、材质参数、深度）。这一步保留了神经场对复杂几何和材质的表达能力。

2. **二次光线（Secondary Rays）—— 显式网格光追**：从神经场的SDF中通过Marching Cubes提取显式网格$\mathcal{S}$，利用NVIDIA OptiX库高效计算二次光线的可见性$v_i(x, \omega_i, \mathcal{S})$，并基于此进行蒙特卡洛着色（含多重重要性采样MIS）。这一步解决了体积积分无法高效处理阴影光线的问题。

> 原文明确指出：“*the extracted mesh s enables us to determine the visibility v of each secondary ray with OptiX, a highly-optimized library for ray-mesh intersection queries.*”

### Changed Slots：相对于基线的关键改进

| 改进维度 | 基线方案 | FEGR方案 | 证据强度 |
|---------|---------|---------|---------|
| **二次光线渲染** | 无或MLP近似可见性 | 显式网格+OptiX光追计算可见性与着色 | 消融实验证实去除阴影使PSNR下降约0.9 dB |
| **场景表示** | 纯神经场（密度/辐射度） | 混合：神经场负责一次光线，显式网格负责二次光线 | “仅网格”消融使PSNR从21.53降至18.94 |
| **光照模型** | 低频球谐系数或简单环境网络 | HDR天空穹顶MLP（含哈希编码），支持高频方向光 | 定性结果展示了锐利阴影边界 |
| **法向估计** | SDF梯度直接作为法向 | 体积渲染法向作为主输出，SDF梯度仅作为角度正则项 | 角度损失$\mathcal{L}_{\mathrm{norm.}}$显式约束二者一致性 |
| **遮阴正则化** | 无 | 逐语义类可学习反照率重渲染损失$\mathcal{L}_{\mathrm{shade}}$，迫使阴影由环境光解释 | 消融实验（Figure B）表明无此损失时HDR环境图无法产生锐利阴影 |
| **曝光补偿** | 无 | 逐图像可学习曝光参数（跨所有图像归一化） | 消融实验证实去除曝光补偿使PSNR下降约0.8 dB |

### 创新点之间的因果依赖

这些改进并非孤立，而是形成了一条因果链：

1. **HDR天空穹顶**提供了高频光照的表达能力，但若没有**遮阴正则化**$\mathcal{L}_{\mathrm{shade}}$，优化过程会倾向于将阴影“烘焙”进反照率，而非正确估计环境光的高动态范围成分。消融实验（Figure B）清晰展示了这一依赖关系：去掉$\mathcal{L}_{\mathrm{shade}}$后，估计的环境图无法产生锐利阴影，阴影尺度也不正确。

2. **显式网格光追**使得二次光线可见性计算成为可能，但若没有**神经场的一次光线渲染**，仅靠网格本身的分辨率无法产生高质量的G缓冲区——“仅网格”（Ours mesh only）变体在Site 1上PSNR从21.53骤降至18.94，证实了神经场对一次光线质量的关键作用。

3. **法向的体积渲染**与**SDF梯度正则化**的配合，使得法向估计既受益于体积渲染的平滑性，又受到SDF几何一致性的约束，避免了纯梯度法向在表面附近的不稳定性。

### 与最相关工作的本质差异

- **vs NeRF-OSR**：NeRF-OSR完全依赖体积积分，无法高效处理二次光线，因此在重光照任务上PSNR显著低于FEGR（Site 1: 19.34 vs 21.53）。
- **vs Nvdiffrecmc**：Nvdiffrecmc基于网格表示，虽然支持高效光追，但在驾驶场景等复杂城市场景中，网格分辨率不足以捕捉细节。
- **vs 光照估计方法（Hold-Geoffroy et al., CVPR 2019; Wang et al., ECCV 2022）**：这些方法仅估计光照，不重建完整的场景本征属性。用户调研显示，在虚拟物体插入任务中，86.2%的用户偏好FEGR的结果。

### 需要人工验证的细节

- 网格每20次迭代重新提取并重建BVH的具体计算开销，原文未给出定量数据，仅提及“增加了计算负担”。
- 语义分割网络的具体架构和训练细节，原文未详细说明，仅提及使用了现成的语义分割网络。

FEGR 的整体管线围绕一个核心设计展开：**将神经场的高分辨率细节与显式网格的高效光线求交能力解耦组合**。输入为一组已知相机位姿的 RGB 图像（可来自单一光照或多光照采集），输出包括场景几何、空间变化材质以及 HDR 环境光照，最终支持重光照、新视角合成和虚拟物体插入等应用（Figure 2）。

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2304_03266/figures/002_Figure_2.jpg]]
*Figure 2: Overview of FEGR. Given a set of posed camera images, FEGR estimates the geometry, spatially varying materials, and HDR lighting of the underlying scene. We model the intrinsic properties of the scene using a neural intrinsic field and use an HDR Sky Dome to represent the lighting. Our Hybrid Deferred Renderer models the primary rays with volumetric rendering of the neural field, while the secondary rays are ray-traced using an explicit mesh reconstructed from the SD field. By modeling the HDR properties of the scene FEGR can support several scene manipulations including novel-view synthesis, scene relighting, and AR*

### 模块拓扑与数据流

FEGR 由五个关键模块串联构成，数据流遵循“神经场前向推理 → G 缓冲区生成 → 显式网格提取 → 二次光线着色 → 损失反向优化”的闭环：

1. **神经本征场（Neural Intrinsic Field）**  
   以 3D 点坐标 $\mathbf{x}$ 为输入，输出有符号距离值 $s$、法向 $\mathbf{n}$、基色（漫反射颜色）$\mathbf{k}_d$ 以及粗糙度/金属度参数 $\mathbf{k}_s$：
   $$F_{\phi}: \mathbf{x} \mapsto (s, \mathbf{n}, \mathbf{k}_d, \mathbf{k}_s)$$
   该模块是整个场景表示的基础，所有后续渲染所需的几何与材质信息均来源于此。

2. **HDR 天空穹顶（HDR Sky Dome）**  
   将远场环境光照建模为方向到 HDR 辐射度的 MLP：
   $$\mathbf{e} = f_{\mathrm{env.}}(\mathbf{d}; \theta_{\mathrm{env.}})$$
   该模块支持高频方向光照，是产生清晰投射阴影和正确阴影尺度的关键（消融实验证实，移除遮阴先验将导致环境光无法产生锐利阴影，见 Figure B）。

3. **神经 G 缓冲区渲染（Neural G-buffer Rendering）**  
   对每条相机光线 $\mathbf{r}$ 执行体积积分，渲染得到法向图、基色图、材质参数图和深度图。深度缓冲的渲染公式为：
   $$\mathcal{D}(\mathbf{r}) = \int_{t_n}^{t_f} T(t) \rho(\mathbf{r}(t)) t \, dt$$
   其中不透明度 $\rho$ 由 SDF 经可学习尖锐度 $\kappa$ 的 Sigmoid 函数转换得到（Eq. (3)）。此阶段仅处理一次光线（primary rays），避免了体积积分在二次光线上的高昂开销。

4. **显式网格提取（Mesh Extraction）**  
   从当前优化的 SDF 场中通过 Marching Cubes 提取显式三角网格 $S$。该步骤每 20 次迭代执行一次，并重建 BVH 加速结构以供后续光追使用。

5. **着色通道与可见性计算（Shading Pass with Visibility）**  
   利用提取的显式网格 $S$ 和 OptiX 光线求交引擎，对每个表面点 $\mathbf{x}$ 的二次光线方向 $\omega_i$ 计算二值可见性：
   $$v_i(\mathbf{x}, \omega_i, S) = \begin{cases} 0 & \text{if } \omega_i \text{ is blocked by } S \\ 1 & \text{otherwise} \end{cases}$$
   随后通过蒙特卡洛采样结合多重重要性采样（MIS）完成基于物理的着色，输出最终颜色 $C_{\mathrm{render}}$。

### 优化闭环

整个管线的优化遵循“预热—联合优化”策略：首先仅使用辅助辐射场损失 $\mathcal{L}_{\mathrm{rad.}}$ 初始化几何（此时不分解材质与光照），随后启用全部损失项进行联合优化。总损失函数为：
$$\mathcal{L} = \mathcal{L}_{\mathrm{render}} + \lambda_{\mathrm{depth}} \mathcal{L}_{\mathrm{depth}} + \lambda_{\mathrm{rad.}} \mathcal{L}_{\mathrm{rad.}} + \lambda_{\mathrm{norm.}} \mathcal{L}_{\mathrm{norm.}} + \lambda_{\mathrm{shade}} \mathcal{L}_{\mathrm{shade}} + \lambda_{\mathrm{reg.}} \mathcal{L}_{\mathrm{reg.}}$$
其中 $\mathcal{L}_{\mathrm{render}}$ 为混合渲染器输出与真值的 L1 重建损失，$\mathcal{L}_{\mathrm{shade}}$ 为语义感知遮阴先验损失（通过逐语义类可学习反照率重渲染来迫使阴影由环境光解释），$\mathcal{L}_{\mathrm{norm.}}$ 为 SDF 梯度法向与体积渲染法向之间的角度正则项。在含 LiDAR 深度数据的驾驶数据集上，额外引入 $\mathcal{L}_{\mathrm{depth}}$ 深度损失。

### 关键设计决策

- **一次光线与二次光线的解耦**：一次光线保留神经场的体积渲染质量（避免网格分辨率限制导致的细节丢失），二次光线则利用显式网格的快速求交能力高效计算阴影与全局光照。消融实验表明，若将一次光线也迁移至网格渲染（“mesh only”模式），Site 1 的 PSNR 从 21.53 骤降至 18.94，验证了神经场对一次光线质量的关键作用。
- **每图像曝光补偿**：针对多光照数据集中相机白平衡不一致的问题，为每张图像学习一个可优化的曝光参数，移除该模块导致 PSNR 下降至 20.70。
- **语义遮阴先验**：通过引入逐语义类的辅助反照率参数，强制环境光照解释图像中的亮度变化，避免了材质与光照的歧义分解。消融实验证实，缺少该先验时 HDR 环境光无法产生锐利阴影（Figure B）。

### 3.1 神经本征场与HDR天空穹顶

FEGR将场景本征属性分解为两个核心组件：**神经本征场（Neural Intrinsic Field）** 与 **HDR天空穹顶（HDR Sky Dome）**。

**神经本征场** $F_{\phi}$ 将三维空间点 $\mathbf{x}$ 映射为四个本征量：

$$F_{\phi} : \mathbf{x} \mapsto (s, \mathbf{n}, \mathbf{k}_d, \mathbf{k}_s)$$

其中 $s$ 为有符号距离（SD）值，$\mathbf{n}$ 为法向量，$\mathbf{k}_d$ 为基色（漫反射反照率），$\mathbf{k}_s$ 为镜面反射材质参数（粗糙度与金属度）。该场由MLP参数化，为后续体积渲染提供连续的场景表示。

**HDR天空穹顶**将远场环境光照建模为从方向到HDR辐射度的MLP：

$$\mathbf{e} = f_{\mathrm{env.}}(\mathbf{d}; \theta_{\mathrm{env.}})$$

其中 $\mathbf{d}$ 为入射方向，$\theta_{\mathrm{env.}}$ 为可学习参数。该MLP采用哈希编码（hash encoding）以支持高频方向性光照，能够捕捉太阳等小面积高亮光源——这对产生清晰投射阴影至关重要。

### 3.2 混合延迟渲染管线

FEGR的核心创新在于**混合延迟渲染器（Hybrid Deferred Renderer）**：一次光线采用神经场的体积渲染，二次光线采用显式网格的光线追踪。

#### 3.2.1 神经G缓冲区渲染（一次光线）

对于每条相机光线 $\mathbf{r}$，系统通过体积渲染生成G缓冲区（G-buffer），包含基色图 $\mathcal{K}_d$、法向图、材质图与深度图。

**基色图**通过alpha合成沿光线积分得到：

$$\mathcal{K}_d(\mathbf{r}) = \int_{t_n}^{t_f} T(t) \rho(\mathbf{r}(t)) \mathbf{k}_d(\mathbf{r}(t)) dt$$

其中 $T(t)$ 为累积透射率，$\rho$ 为体密度。

**体密度**由SD场通过可学习Sigmoid函数 $\Phi_{\kappa}$ 转换而来，$\kappa$ 控制尖锐度：

$$\rho(\mathbf{r}(t)) = \max\left( \frac{-\frac{\mathrm{d}\Phi_{\kappa}}{\mathrm{d}t}\bigl(f_{\mathrm{SDF}}(\mathbf{r}(t))\bigr)}{\Phi_{\kappa}(f_{\mathrm{SDF}}(\mathbf{r}(t)))}, 0 \right)$$

**深度缓冲**类似地通过体积渲染得到：

$$\mathcal{D}(\mathbf{r}) = \int_{t_n}^{t_f} T(t) \rho(\mathbf{r}(t)) t dt$$

法向量 $\mathbf{n}_{\mathbf{x}}$ 通过体积渲染估计，而SD场的梯度法向 $\tilde{\mathbf{n}}_{\mathbf{x}}$ 仅作为正则化项使用，以角度损失约束二者一致性。

#### 3.2.2 显式网格提取与二次光线着色

每20次迭代，系统从当前优化的SD场中通过Marching Cubes提取显式网格 $\mathcal{S}$。该网格用于后续二次光线的可见性判断。

**出射辐射度**由渲染方程给出，在表面点 $\mathbf{x}$ 沿方向 $\omega_o$ 的出射光为：

$$L_o(\mathbf{x}, \omega_o) = \int_{\Omega} f_r(\mathbf{x}, \omega_o, \omega_i) L_i(\mathbf{x}, \omega_i) \left| \mathbf{n} \cdot \omega_i \right| d\omega_i$$

其中 $f_r$ 为BRDF，$L_i$ 为来自HDR天空穹顶的入射辐射度。

**可见性函数**利用OptiX在显式网格 $\mathcal{S}$ 上高效计算二次光线遮挡：

$$v_i(x, \omega_i, \mathcal{S}) = \begin{cases} 0 & \text{if } \omega_i \text{ is blocked by } \mathcal{S} \\ 1 & \text{otherwise} \end{cases}$$

该二值可见性直接参与蒙特卡洛采样中的阴影计算，使得FEGR能够产生物理正确的投射阴影。OptiX作为高度优化的光线-网格求交库，显著降低了二次光线可见性查询的计算开销。

### 3.3 优化目标与损失函数

FEGR采用分阶段训练策略：首先仅用辐射场损失初始化几何，随后联合优化所有损失项。总损失函数为：

$$\mathcal{L} = \mathcal{L}_{\mathrm{render}} + \lambda_{\mathrm{depth}} \mathcal{L}_{\mathrm{depth}} + \lambda_{\mathrm{rad.}} \mathcal{L}_{\mathrm{rad.}} + \lambda_{\mathrm{norm.}} \mathcal{L}_{\mathrm{norm.}} + \lambda_{\mathrm{shade}} \mathcal{L}_{\mathrm{shade}} + \lambda_{\mathrm{reg.}} \mathcal{L}_{\mathrm{reg.}}$$

**渲染损失**为混合渲染器输出颜色 $C_{\mathrm{render}}$ 与真值 $C_{\mathrm{gt}}$ 之间的L1损失：

$$\mathcal{L}_{\mathrm{render}} = \frac{1}{|\mathcal{R}|} \sum_{\mathbf{r} \in \mathcal{R}} |C_{\mathrm{render}}(\mathbf{r}) - C_{\mathrm{gt}}(\mathbf{r})|$$

**辅助辐射场损失**用于几何初始化阶段：

$$\mathcal{L}_{\mathrm{rad.}} = \frac{1}{|\mathcal{R}|} \sum_{\mathbf{r} \in \mathcal{R}} |C_{\mathrm{rad.}}(\mathbf{r}) - C_{\mathrm{gt}}(\mathbf{r})|$$

**深度损失**（仅在LiDAR数据可用时启用）：

$$\mathcal{L}_{\mathrm{depth}} = \frac{1}{|\mathcal{R}_{\mathrm{d}}|} \sum_{\mathbf{r} \in \mathcal{R}_{\mathrm{d}}} |\mathcal{D}(\mathbf{r}) - \mathcal{D}_{\mathrm{gt}}(\mathbf{r})|$$

**法向角度损失**约束SD梯度法向与体积渲染法向一致：

$$L_{\mathrm{norm.}} = \frac{1}{|\mathcal{R}|} \sum_{\mathbf{r} \in \mathcal{R}} \cos^{-1}{(|\tilde{\mathbf{n}}_{\mathbf{x}} \cdot \mathbf{n}_{\mathbf{x}}|)}$$

**遮阴正则化损失**是FEGR的关键创新：为每个语义类引入可学习的辅助反照率参数，强制其重渲染结果与真值图像一致：

$$\mathcal{L}_{\mathrm{shade}} = \frac{1}{B} \sum_{b=1}^{B} \frac{1}{|\mathcal{R}_b|} \sum_{\mathbf{r} \in \mathcal{R}_b} |C_{\mathrm{diffuse}}^{b}(\mathbf{r}) - \hat{C}(\mathbf{r})|$$

该损失迫使阴影信息由环境光图解释，而非被“烘焙”进反照率，是实现干净本征分解的核心机制。消融实验证实，去除该损失后HDR环境光无法产生清晰的投射阴影（见Figure B）。

**正则化项** $\mathcal{L}_{\mathrm{reg.}}$ 包含Eikonal损失（约束SD梯度模长为1）、平滑损失（约束基色、材质、法向的局部一致性）以及天空掩码损失。完整形式见附录：

$$\mathcal{L}_{\mathrm{Eikonal}} = \frac{1}{|\mathcal{X}|} \sum_{\mathbf{x} \in \mathcal{X}} (||\nabla_{\mathbf{x}} s(\mathbf{x})||_2 - 1)^2$$

$$\mathcal{L}_{\mathrm{smooth}} = \frac{1}{|\mathcal{X}|} \sum_{\mathbf{x} \in \mathcal{X}} |\mathbf{k}_d(\mathbf{x}) - \mathbf{k}_d(\mathbf{x} + \epsilon)| + \frac{1}{|\mathcal{X}|} \sum_{\mathbf{x} \in \mathcal{X}} |\mathbf{k}_s(\mathbf{x}) - \mathbf{k}_s(\mathbf{x} + \epsilon)| + \frac{1}{|\mathcal{X}|} \sum_{\mathbf{x} \in \mathcal{X}} |\mathbf{n}(\mathbf{x}) - \mathbf{n}(\mathbf{x} + \epsilon)|$$

此外，系统还优化每张图像的逐通道曝光参数，以补偿不同相机白平衡设置带来的不一致性。消融实验表明，去除曝光补偿后PSNR下降约0.8 dB。

## 实验与关键发现

### 核心瓶颈与设计动机

基于NeRF的逆渲染方法（如NeRF-OSR）面临一个根本性矛盾：体积积分在渲染一次光线时表现优异，但处理二次光线（阴影光线、高光采样）时，其计算复杂度为O(nm)（n为采样点数，m为二次光线数），使得带阴影的重光照几乎不可行。而纯网格方法虽能快速求交，却受限于分辨率，无法捕捉城市场景的细粒度几何与材质细节。FEGR的核心洞察在于将两类表示的优势解耦：**神经场负责一次光线的高分辨率G缓冲区渲染，显式网格负责二次光线的快速可见性判定**，从而在城市场景逆渲染中首次实现逼真的重光照与带阴影的虚拟物体插入。

### 主实验结果

#### 场景重光照（NeRF-OSR数据集）

Table 1报告了在NeRF-OSR三个室外场景上的重光照定量结果。FEGR在所有场景上均显著超越NeRF-OSR基线：

- **Site 1**：PSNR 21.53 dB vs 19.34 dB（+2.19 dB）
- **Site 2**：PSNR 17.00 dB vs 16.35 dB（+0.65 dB）
- **Site 3**：PSNR 17.57 dB vs 15.66 dB（+1.91 dB）

这一提升的关键在于显式网格光线追踪带来的正确阴影投射能力。Figure 3的定性结果显示，FEGR重建的漫反射反照率干净无阴影残留，重光照结果具有逼真的投射阴影边界。相比之下，NeRF-OSR的体积近似难以精确判定二次光线可见性，阴影模糊或缺失。

#### 本征分解（驾驶数据集）

Figure 4展示了驾驶数据集上的本征分解定性结果。FEGR成功将阴影从漫反射反照率中分离（见图中标记），同时从HDR环境图中重建出高强度、小面积的光源区域。这一能力源于语义感知遮阴先验损失L_shade的正则化作用——它迫使环境图解释图像中的亮度变化，而非让阴影渗入反照率。

#### 虚拟物体插入用户调研

Table 2报告了虚拟物体插入质量的用户偏好调研结果。在Amazon Mechanical Turk上进行的A/B测试中：

- **86.2%** 的用户偏好FEGR的结果，而非Hold-Geoffroy et al.（CVPR 2019）
- **68.9%** 的用户偏好FEGR的结果，而非Wang et al.（ECCV 2022）

Figure 6的定性对比显示，FEGR忠实重建的环境图能产生边界锐利的投射阴影，而基线方法往往只能产生模糊或无阴影的插入效果。

### 消融实验

Table 1同时包含完整的消融分析，在Site 1场景上揭示了各组件的贡献：

**1. 神经场与显式网格的组合是关键。** 当完全移除神经场、仅使用网格渲染一次和二次光线时（Ours mesh only），PSNR骤降至18.94 dB（-2.59 dB）。这表明神经场的高分辨率G缓冲区对一次光线质量至关重要，纯网格表示无法恢复相同细节。

**2. 光线追踪阴影显著提升真实感。** 禁用二次光线阴影（Ours w/o shadow）导致PSNR降至20.62 dB（-0.91 dB），证实了OptiX光线追踪可见性判定的重要性。无阴影时，重光照结果缺乏遮挡线索，场景立体感减弱。

**3. 曝光补偿处理相机不一致性。** 移除逐图像、逐通道曝光补偿（Ours w/o exposure）使PSNR降至20.70 dB（-0.83 dB）。城市场景数据通常由不同相机、不同白平衡设置拍摄，曝光补偿有效归一化了这些差异。

**4. 遮阴先验损失L_shade对HDR环境图估计至关重要。** Figure B的定性消融显示，不施加L_shade时，估计的HDR环境图无法产生清晰的投射阴影，阴影尺度也不正确。该损失通过逐语义类可学习反照率重渲染与真值的一致性约束，迫使环境图学习高动态范围的光源分布。

### 失败模式与局限性

尽管FEGR在静态城市场景上表现优异，其设计存在若干结构性局限：

- **依赖人工设计的语义正则项**：L_shade等损失函数依赖预训练的语义分割网络，引入离线计算开销，且正则化形式由人工设计，缺乏从数据中学习逆渲染先验的能力。
- **仅适用于静态场景**：当前管线假设场景几何、材质和光照在捕获期间不变，无法处理动态物体或移动光源。
- **网格重建开销**：训练过程中每20次迭代需通过Marching Cubes重新提取网格并重建BVH加速结构，增加了计算负担。对于大规模场景，这一开销可能成为瓶颈。

### 公平性说明

与NeRF-OSR的比较遵循严格公平协议：所有方法使用相同的测试环境图进行重光照评估；动态物体、天空和植被像素通过统一的分割掩码排除；深度监督（LiDAR）仅在驾驶数据集上使用，匹配各数据集特性。用户调研遵循先前工作的标准协议。

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2304_03266/figures/001_Figure_1.jpg]]
*Figure 1: We present FEGR, an approach for reconstructing scene geometry and recovering intrinsic properties of the scene from posed camera images. Our approach works both for single and multi-illumination captured data. FEGR enables various downstream applications such as VR and AR where users may want to control the lighting of the environment and insert desired 3D objects into the scene*

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2304_03266/figures/003_Table_1.jpg]]
*Table 1: Outdoor scene relighting results on NeRF-OSR dataset*

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2304_03266/figures/008_Table_2.jpg]]
*Table 2: User study results of object insertion quality. Users consistently prefer ours over results from baseline methods*

## 定位与知识库关联

**FEGR** 处于基于神经场的逆渲染与基于显式网格的光线追踪的交汇点，其核心设计动机源于对两类方法根本性瓶颈的回应：基于 NeRF 的逆渲染管线（如 **NeRF-OSR**，Rudnev et al., ECCV 2022）受限于体积积分复杂度 $O(nm)$，无法高效渲染二次光线（阴影、高光）；而纯网格方法受限于分辨率，难以处理大规模城市场景的细节重建。FEGR 通过**混合延迟渲染管线**将二者解耦：一次光线由神经场体积渲染生成 G 缓冲区，二次光线则由从有符号距离场（SDF）提取的显式网格通过 OptiX 进行快速光线求交，从而在城市场景逆渲染中首次实现逼真的重光照与带阴影的虚拟物体插入。

### 与基线方法的关系

**NeRF-OSR**（Rudnev et al., ECCV 2022）是 FEGR 在室外场景重光照任务上的直接对比基线。NeRF-OSR 采用纯神经场表示，依赖 MLP 估计可见性或忽略高阶光照效应。FEGR 在三个测试场景上均显著超越 NeRF-OSR（PSNR 提升最高达 2.19 dB），且定性上产生了更清晰的阴影边界（Figure 3）。这一差距的因果根源在于：NeRF-OSR 无法在体积渲染框架内高效查询二次光线遮挡，而 FEGR 的网格光追机制直接解决了该瓶颈。

**Nvdiffrecmc**（Hasselgren et al., arXiv 2022）作为驾驶数据上的逆渲染基线，同样面临网格分辨率与场景尺度的权衡。FEGR 在驾驶数据集上的本征分解定性结果（Figure 4）表明，混合表示能有效分离阴影与漫反射反照率，并重建出 HDR 环境图中高强度、小面积的光源区域。

在虚拟物体插入任务上，FEGR 与两类光照估计基线进行了用户调研对比：**Hold-Geoffroy et al.**（CVPR 2019）和 **Wang et al.**（ECCV 2022）。调研结果显示 86.2% 的用户偏好 FEGR 优于 Hold-Geoffroy et al.，68.9% 偏好 FEGR 优于 Wang et al.（Table 2）。FEGR 的优势在于其 HDR 天空穹顶 MLP 结合哈希编码，能表达高频方向性光照，而基线方法通常限于低频球谐系数或简单环境网络。

### 技术谱系中的关键设计选择

FEGR 的方法架构可沿以下维度定位其创新点：

1. **场景表示**：从纯神经场（NeRF-OSR）或纯网格（Nvdiffrecmc）走向**混合表示**——SDF 驱动的神经场负责一次光线的高分辨率细节，显式网格负责二次光线的快速可见性查询。消融实验证实，将本征属性转移到网格顶点并完全使用网格渲染（Ours mesh only）会导致 PSNR 从 21.53 降至 18.94，证明神经场对一次光线质量至关重要。

2. **光照模型**：从低频 SH 系数升级为**基于哈希编码的 HDR 天空穹顶 MLP**，支持高动态范围和高频方向性光照。消融实验表明，移除阴影光线追踪（w/o shadow）使 PSNR 降至 20.62，移除逐通道曝光补偿（w/o exposure）降至 20.70，二者合计贡献高达 1.5 dB PSNR 提升。

3. **正则化策略**：FEGR 引入**语义感知的遮阴先验损失** $\mathcal{L}_{\mathrm{shade}}$，为每个语义类学习辅助反照率参数，迫使阴影由环境光解释。消融实验（Figure B）显示，无此损失时 HDR 环境图无法产生清晰阴影和正确阴影尺度，说明语义先验是光照分解的关键约束。

4. **法向估计**：FEGR 通过体积渲染估计法向 $\mathbf{n}_x$，而将 SDF 梯度法向 $\tilde{\mathbf{n}}_x$ 仅作为角度正则化项 $\mathcal{L}_{\mathrm{norm.}}$ 使用，避免了梯度法向在体积渲染边界处的噪声问题。

### 适用边界与局限

FEGR 的适用边界受以下因素制约：

- **静态场景假设**：当前方法仅适用于静态场景，无法处理动态物体或移动光源。这是神经场逆渲染方法的共性局限，但 FEGR 的网格重建步骤（每 20 次迭代重新提取网格并重建 BVH）进一步增加了动态扩展的难度。
- **语义分割依赖**：遮阴先验损失依赖现成的语义分割网络，引入了额外的离线计算开销，且正则化效果受限于语义分割的精度。这是一个人工设计的正则化项，缺乏从数据中学习逆渲染先验的能力。
- **计算开销**：训练过程中周期性网格提取与 BVH 重建增加了计算负担，限制了方法在资源受限场景下的部署效率。

### 开放问题

FEGR 揭示了两个值得进一步探索的方向：

1. **从数据中学习逆渲染先验**：当前的语义遮阴先验是人工设计的，如何利用大量可用数据学习更通用的逆渲染先验，以替代手工正则化项，是提升方法泛化能力的关键。

2. **动态场景扩展**：如何将 FEGR 的混合渲染框架扩展至动态场景，例如结合动态 NeRF 的进展，使网格光追机制能处理时变几何与移动光源，是一个有前景但尚未解决的方向。

*注：以上分析基于论文提供的实验证据与消融研究。部分局限（如语义分割依赖的具体精度影响）在论文中未进行定量消融，需要进一步验证。*

## 原文 PDF

![[paperPDFs/CVPR_2023/Neural_Fields_meet_Explicit_Geometric_Representations_for_Inverse_Rendering_of_Urban_Scenes.pdf]]
