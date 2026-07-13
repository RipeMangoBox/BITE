---
title: "Energy-GS: Image Energy-guided Pose Alignment Gaussian Splatting with redesigned pose gradient flow"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Energy_GS_Image_Energy_guided_Pose_Alignment_Gaussian_Splatting_with_redesigned_pose_gradient_flow.pdf
project_link: null
code_link: "https://github.com/SkylerGao/ENGS"
aliases:
- EG
- Energy-GS
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/representation_self_supervised_transfer
core_operator: 通过固定高斯原语位置并重新设计密度化策略，建立稳定的渲染图元集，确保位姿梯度的一致性；同时利用图像SVD能量分解，逐步提高监督图像的能量层级，模拟由粗到精的学习过程。
primary_logic: 将图像表示为奇异值分解的能量分量，从低能量（低频结构）到高能量（高频细节）渐进式地提供监督信号，使3DGS在联合优化中能够稳定收敛至全局最优位姿。
claims:
- 1D信号对齐实验中，重新设计的梯度流结合能量策略使平移误差（ATE）降至0.0001，渲染PSNR达63.17，显著优于其他配置。
- 消融实验表明，仅添加可学习位姿而不做任何改进时PSNR仅8.08，加入梯度流设计提升至12.38，进一步加入能量控制后提升至24.12，旋转误差从8.572°降至1.065°。
- 在合成数据集上，本方法位姿估计误差（旋转角和绝对轨迹误差）在所有对比方法中最低。
- 多壳现象（multi-shell）可视化了不稳定梯度流导致的局部极小，而能量策略能显著缓解此问题，使位姿收敛至正确分布。
---

# Energy-GS: Image Energy-guided Pose Alignment Gaussian Splatting with redesigned pose gradient flow

> [!tip] 核心洞察
> 将图像表示为奇异值分解的能量分量，从低能量（低频结构）到高能量（高频细节）渐进式地提供监督信号，使3DGS在联合优化中能够稳定收敛至全局最优位姿。

| 字段 | 内容 |
|------|------|
| 中文题名 | Energy-GS：基于图像能量引导的位姿对齐高斯溅射及重塑位姿梯度流 |
| 英文题名 | Energy-GS: Image Energy-guided Pose Alignment Gaussian Splatting with redesigned pose gradient flow |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Gao_Energy-GS_Image_Energy-guided_Pose_Alignment_Gaussian_Splatting_with_redesigned_pose_CVPR_2026_paper.html) · [Code](https://github.com/SkylerGao/ENGS) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/representation_self_supervised_transfer |
| Method | Energy-GS |
| Dataset | Synthetic NeRF |

> [!tip] 效果简介
> - Synthetic NeRF (chair) 上，PSNR↑ 29.81 vs 28.35 (BARF) (+1.46)。
> - Synthetic NeRF (hotdog) 上，PSNR↑ 32.90 vs 31.90 (BARF) (+1.00)。
> - Synthetic NeRF (lego) 上，PSNR↑ 30.35 vs 26.92 (BARF) (+3.43)。

## 概要

**问题瓶颈**：3D Gaussian Splatting（3DGS）在联合优化相机位姿与场景表示时，其点基渲染机制导致位姿梯度不稳定。与NeRF基于连续MLP的体积渲染不同，3DGS的离散高斯原语在训练过程中位置动态变化，参与位姿梯度计算的图元集合随之漂移，使梯度流缺乏一致性。同时，3DGS缺少体积渲染中固有的空间采样机制，无法实现由粗到精的渐进对齐，导致仅依赖RGB监督的联合优化极易陷入局部极小值。

**核心思路**：Energy-GS从两个层面重塑3DGS的位姿梯度流。其一，**固定高斯原语位置**并重新设计密度化策略，建立稳定的渲染图元集，确保位姿梯度的数值一致性；其二，引入**图像能量引导的渐进对齐策略**——通过奇异值分解（SVD）将图像分解为不同能量层级的分量，从低能量（低频结构）到高能量（高频细节）逐步提高监督信号的能量层级，模拟由粗到精的学习过程，使联合优化稳定收敛至全局最优位姿。

**方法定位**：Energy-GS属于3DGS位姿联合优化范式，与基于NeRF的**BARF**（Lin et al., ICCV 2021）、**SC-NeRF**（Jeong et al., ICCV 2021）以及基于3DGS的**CF-GS**（Fu et al., CVPR 2024）、**3R-GS**（Huang et al., 2025）形成对比。不同之处在于，Energy-GS不依赖额外的深度或特征匹配先验，仅通过重塑梯度流和能量控制策略实现稳定对齐。

**主要结果**：在合成数据集上，Energy-GS的渲染质量（PSNR）和位姿估计误差（旋转角、绝对轨迹误差）均优于对比方法。消融实验表明，仅添加可学习位姿而不做任何改进时PSNR仅8.08；加入梯度流设计提升至12.38；进一步加入能量控制后提升至24.12，旋转误差从8.572°降至1.065°。1D信号对齐等效实验中，完整方法将平移误差降至0.0001，渲染PSNR达63.17，验证了梯度流重塑与能量策略的协同有效性。



### 3DGS 联合优化位姿的核心瓶颈

三维高斯溅射（3D Gaussian Splatting, 3DGS）在已知精确相机位姿的条件下，已展现出高质量、实时的新视角合成能力（Kerbl et al., SIGGRAPH 2023）。然而，在实际采集场景中，通过运动恢复结构（SfM）获得的初始位姿往往含有不可忽略的噪声。将位姿作为可学习变量与场景表示进行联合优化，是解决这一问题的自然思路。

与基于神经辐射场（NeRF）的联合优化方法（如 **BARF** (Lin et al., ICCV 2021)、**SC-NeRF** (Jeong et al., ICCV 2021)）不同，3DGS 的点基渲染机制引入了一个根本性困难：**位姿梯度的不稳定性**。

具体而言，3DGS 将场景表示为一组离散的高斯基元，其在某一视图下的位姿梯度依赖于参与该视图渲染的基元集合：

$$
G_{gs}^{pose}(v) = F(\omega_{gs}^{v}), \quad \omega_{gs}^{v} = \{g_1, g_2, \dots, g_n\}
$$

在原始 3DGS 框架中，基元的位置是可学习参数，训练过程中会持续更新；同时，密度化操作（克隆与分裂）会动态改变基元的数量与分布。此外，渲染时每个瓦片（tile）所选择的基元集合依赖于 3σ 准则：

$$
Set_{B}^{gs} = \{ g_i \in P \mid r(g_i) < 3\sigma \}
$$

其中 σ 本身也是可学习参数，随训练而变化。这三重动态性——**可学习位置、密度化操作、3σ 准则**——导致参与位姿梯度计算的基元集合在连续训练步之间剧烈变化，使得位姿梯度流变得不可预测，联合优化极易陷入局部极小值。

相比之下，NeRF 使用一个全局唯一的 MLP 表示场景，其位姿梯度 $G_{nf}^{pose}(v) = G(\omega_{nf}^{v})$ 作用于连续、稳定的参数集 $\omega_{nf}^{v}$，天然避免了梯度不稳定的问题。Figure 3 直观对比了两者在连续两步训练中的位姿梯度更新差异：3DGS 的梯度方向因基元集合的动态变化而漂移，而 NeRF 的梯度则保持一致。

### 现有方法的缺口

针对 3DGS 位姿对齐问题，已有一些初步探索。**CF-GS** (Fu et al., CVPR 2024) 利用序列帧间的几何约束进行联合优化，但其有效性依赖于帧间连续性假设。**3R-GS** (Huang et al., 2025) 引入了深度和特征对应等额外几何先验来辅助全局联合优化，但这增加了系统的复杂性和对额外模态的依赖。

从更本质的层面看，现有方法均未解决 3DGS 位姿梯度不稳定这一根本问题。仅将位姿设为可学习变量并直接使用全分辨率 RGB 图像进行光度监督，几乎总是导致优化失败——消融实验中，该配置的 PSNR 仅为 8.08（Table 4）。

此外，即使在一定程度上稳定了梯度流，联合优化仍面临 **“多壳现象”（multi-shell phenomenon）** 的困扰。如 Figure 7 所示，优化后的相机位姿可能收敛到围绕真实位姿的多个离散“壳层”上，而非聚集到正确的全局最优。这一现象在 NeRF 基联合优化中也频繁出现，其根源在于缺少由粗到精的渐进对齐机制——NeRF 的体积渲染天然具有从低频到高频的隐式频率编码，而 3DGS 的点基渲染不具备这种空间采样层级。

### 本文动机

基于上述分析，本文识别出 3DGS 联合位姿优化的两个关键缺口：

1. **梯度流稳定性**：需要重新设计高斯原语的优化策略，消除基元集合的动态变化对位姿梯度的干扰，建立数值稳定的梯度流。
2. **渐进对齐机制**：需要为 3DGS 引入一种模拟由粗到精的渐进式监督策略，使其能够先对齐低频结构、再逐步细化高频细节，从而规避多壳现象，稳定收敛至全局最优位姿。

Energy-GS 正是围绕这两个缺口展开设计：通过固定基元位置、延迟密度化、以及基于固定瓦片尺寸的图元选择，重塑位姿梯度流；同时，利用图像 SVD 能量分解，从低能量（低频结构）到高能量（高频细节）渐进式地提供监督信号，实现稳定的粗到细位姿对齐。



## 核心方法与创新机理

Energy-GS 的核心创新在于从根源上解决了 3DGS 在联合优化相机位姿时因点基渲染特性导致的梯度不稳定问题，并引入了一种无需外部先验的由粗到精的对齐策略。其关键创新点可归结为两个层面：**重塑位姿梯度流**以建立稳定的优化基础，以及**图像能量引导的渐进对齐**以规避局部极小值。

### 1. 重塑位姿梯度流：从动态到静态的渲染图元集

原始 3DGS 的位姿梯度不稳定源于其渲染图元集合在训练过程中的动态变化。具体而言，3DGS 中每个瓦片（tile）参与渲染的高斯原语集合依赖于可学习的尺度参数 $σ$，通过 $3σ$ 准则进行筛选：

$$Set_{B}^{gs} = \{ g_i \in P \mid r(g_i) < 3\sigma \}$$

由于 $σ$ 在训练中持续更新，导致每个训练步下对相机位姿产生梯度的原语集合不断变化，位姿梯度因此失去一致性（Figure 3）。这与 NeRF 使用全局唯一的 MLP 表示场景形成鲜明对比——后者的参数集 $\omega_{nf}^v$ 是固定的，梯度流天然稳定：

$$G_{nf}^{pose}(v) = G(\omega_{nf}^v), \quad \omega_{nf}^v = \{ n_1, n_2, ... n_m \}$$

Energy-GS 的核心干预是**将动态的图元选择机制改造为静态机制**。具体包括三个相互配合的 **changed slots**：

- **基元位置可学习性**：将高斯原语的位置从可学习参数改为固定参数，在联合优化阶段禁止其更新。这直接消除了因位置移动导致的图元集合变化。
- **渲染图元选择准则**：放弃 $3σ$ 准则，改用基于固定瓦片尺寸 $t$ 的静态筛选规则：

$$OurSet_{B}^{gs} = \{ g'_i = g_i, r(g'_i) < t \mid g_i \in P \}$$

由于 $t$ 是固定值，每个瓦片参与渲染的原语集合在训练全程保持不变，位姿梯度的计算基础得以稳定。

- **密度化时机**：将克隆与分裂操作从训练全程持续进行改为**延迟激活**。密度化仅在监督图像的能量层级 $lv$ 超过预设阈值 $L$ 后才启动：

$$s = \min\{ step \in \{1, \dots, N\} \mid lv(step) > L \}$$

这一设计确保了在位姿对齐的早期关键阶段，高斯原语的数量和位置均保持恒定，位姿梯度不受密度化操作的干扰。值得注意的是，Energy-GS 虽禁止位置更新，但仍计算位置的反向传播梯度，以保证密度化操作中克隆与分裂的正确执行。

### 2. 图像能量引导的渐进对齐：模拟由粗到精的优化过程

即使建立了稳定的梯度流，仅使用全分辨率 RGB 图像进行联合优化仍容易陷入局部极小值。NeRF 类方法天然受益于体积渲染中沿射线的空间采样机制，隐式地实现了由粗到精的对齐；而 3DGS 的点基渲染缺乏这一特性。

Energy-GS 的创新在于**通过图像奇异值分解（SVD）将监督信号分解为不同能量层级，并渐进式地恢复高频分量**，从而在 2D 监督层面模拟由粗到精的学习过程。具体机制如下：

- **图像能量分解**：将图像 $I$ 的总能量定义为奇异值的平方和：

$$E = \sum_{i=1}^{n} \sigma_i^2, \quad \sigma_1 \geq \sigma_2 \geq \dots \geq \sigma_n > 0$$

使用前 $lv$ 个奇异值重构的低能量图像 $I_E$ 保留了图像的主体结构（低频信息），而丢弃了细节纹理（高频信息）：

$$I_E = U_{lv} \Sigma_{lv} V_{lv}^T = \sum_{i=0}^{lv} u_i \sigma_i v_i^T$$

- **渐进能量掩膜**：对 $lv > 1$ 的能量分量施加平滑权重掩膜，权重随优化进度 $α$ 动态调整：

$$I_E(\alpha) = (\omega(\alpha) \cdot U_{lv}) \cdot (\omega(\alpha) \cdot \Sigma_{lv}) \cdot (\omega(\alpha) \cdot V_{lv}^T)$$

其中权重函数 $\omega(\alpha) = \log_{10}((\alpha - \frac{lv}{n}) \cdot 255) / 255$ 随优化进度逐步增大，使高频能量分量从被抑制到完全恢复。$lv = 1$ 的能量分量始终完全保留，确保基本结构信息不丢失。

- **监督信号切换**：将联合优化的监督目标从原始全分辨率 RGB 图像 $I$ 替换为渐进恢复的能量图像 $I_E(α)$。在优化初期，模型仅需对齐低能量的结构信息，位姿搜索空间被有效平滑；随着优化推进，高频细节逐步引入，位姿估计在已接近全局最优的基础上进一步精细化。

### 3. 创新点的因果机制与证据强度

两项核心创新之间存在明确的因果依赖关系：**稳定的梯度流是渐进能量策略生效的前提条件**。1D 信号对齐的等效降维实验（Figure 4, Table 1）清晰地验证了这一机制：

- 当同时保留可学习位置和密度化时，即使加入能量策略，平移误差（ATE）仍高达 0.0106，渲染 PSNR 仅 38.47。
- 仅重设计梯度流（固定位置 + 延迟密度化）而不使用能量策略时，ATE 降至 0.0013，PSNR 升至 56.64，但位姿仍可能陷入局部极小。
- 将重塑后的梯度流与能量策略结合（完整 Energy-GS），ATE 进一步降至 **0.0001**，PSNR 达到 **63.17**，实现最优性能。

在真实 3D 场景的消融实验中（Table 4），这一因果链同样得到验证：仅添加可学习位姿而不做任何改进时 PSNR 仅 **8.08**，加入梯度流设计提升至 **12.38**，进一步加入能量控制后提升至 **24.12**，旋转误差从 **8.572°** 降至 **1.065°**。Figure 7 可视化了仅重设计梯度流时仍可能出现的“多壳现象”（multi-shell phenomenon）——位姿在多个局部极小值间漂移，而能量策略能显著缓解此问题，使位姿收敛至正确分布。

> **证据强度评估**：上述创新点的有效性在 1D 信号对齐和 3D 场景两个层面均得到了消融实验的定量验证，证据置信度高（0.90–0.95）。方法在合成数据集上取得了所有对比方法中最优的位姿估计精度（Table 3），进一步支持了创新设计的有效性。



Energy-GS 提出了一套仅依赖 RGB 图像的联合优化框架，同时估计 3D 高斯溅射场景表征与相机位姿。其核心设计围绕一个关键瓶颈展开：**3DGS 的点基渲染导致位姿梯度不稳定，且缺少体积渲染中的空间采样机制，无法实现由粗到精的渐进对齐**，使联合优化极易陷入局部极小值。

图 2 展示了整体流程，可分解为五个串联的功能模块：

1. **固定基元初始化**：从不精确的初始相机位姿出发，随机初始化高斯原语，但**将其位置设为非可学习参数**，在后续联合优化中保持空间稳定。
2. **可学习位姿参数化**：将相机位姿显式参数化为可学习变量，使其能够通过反向传播接收梯度更新。
3. **稳定瓦片图元选择**：摒弃原始 3DGS 中依赖动态变化 σ 的 3σ 准则（Eq.2），改用**固定瓦片尺寸 t 选择参与渲染的高斯原语**（Eq.3），确保每个瓦片的图元集合在训练过程中不变，从而消除位姿梯度的数值波动。
4. **延迟密度化控制**：密度化（克隆与分裂）操作不再全程执行，而是根据图像能量层级阈值 L 延迟激活（Eq.5）。当监督图像的能量层级 lv(step) 超过 L 时，才允许密度化发生；在此之前，原语数量与位置均保持冻结。
5. **图像能量分解与渐进掩膜**：将多视图图像通过 SVD 分解为能量分量（Eq.6-7），仅保留低能量层级（低频结构）重构目标图像 I_E。随优化进度 α 增加，通过平滑掩膜 ω(α) 逐步释放更高能量层级（高频细节），模拟由粗到精的渐进监督（Eq.8）。
6. **光度损失联合优化**：以目标能量图像与渲染图像之间的光度损失作为统一目标，同时监督场景重建与相机位姿精化。

**输入**：带噪声初始位姿的多视图 RGB 图像。  
**输出**：精化后的相机位姿与高质量 3DGS 场景表征。  
**数据流**：初始位姿 → 固定基元渲染 → 可学习位姿梯度回传 → 能量渐进监督 → 密度化条件激活 → 联合收敛。

Figure 3 通过对比 3DGS 与 NeRF 在两个连续训练步上的位姿梯度更新，直观揭示了问题根源：原始 3DGS 中高斯原语位置在训练中动态调整，导致对相机位姿梯度有贡献的图元集合不断变化，产生不可预测的位姿漂移；而 NeRF 使用全局唯一的 MLP 表征场景，天然避免了这种不稳定。Energy-GS 通过固定位置与稳定图元选择，使 3DGS 的位姿梯度流在数值上达到与 NeRF 相当的稳定性，为后续能量渐进策略的有效性奠定了基础。

### 补充图表

![[assets/figures/papers/paper_list_l2078_https_openaccess_thecvf_com_content_CVPR2026_html_Gao_Energy_GS_Image_En/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the proposed method. First, Energy-GS starts from imperfect camera poses and randomly initialized Gaussian primitives with fixed, non-learnable positions. Second, the poses are parameterized into learnable variables, and our proposed densification strategy is applied to the Gaussian primitives. Then, benefiting from the fixed positions and the densification, we are able to establish a stable set of primitives for each rendered tile, which ensures the stability of camera pose gradients during joint optimization. Next, the proposed image energy control strategy decomposes and suppresses specific energy components in the multi-view images to generate target energy images. Finally,...*

![[assets/figures/papers/paper_list_l2078_https_openaccess_thecvf_com_content_CVPR2026_html_Gao_Energy_GS_Image_En/figures/001_Figure_1.jpg]]
*Figure 1: Comparison of scene rendering and camera pose estimation. We introduce Energy-GS, a novel joint optimization framework for 3D Gaussian Splatting and camera pose refinement. The method achieves stable, coarse-to-fine scene reconstruction and pose optimization by redesigning the pose gradient flow and introducing an image energy-based progressive alignment strategy. Compared to other joint optimization methods that directly rely on full-energy RGB supervision, our approach attains competitive results in both rendering quality and pose accuracy*



### 3DGS与NeRF的位姿梯度差异

联合优化中，相机位姿的梯度来源于场景表示的可学习参数。对于NeRF，场景由全局唯一的MLP参数集 $\omega_{nf}^v$ 表示，其位姿梯度 $G_{nf}^{pose}(v)$ 来源于稳定的参数空间。而对于3DGS，可学习参数集 $\omega_{gs}^v$ 是一组离散的高斯原语 $\{g_1, g_2, ... g_n\}$，其位姿梯度 $G_{gs}^{pose}(v)$ 依赖于当前参与渲染的原语集合：

$$
\left\{ \begin{array} { l l } { G _ { g s } ^ { p o s e } ( v ) = F ( \omega _ { g s } ^ { v } ) , \omega _ { g s } ^ { v } = \{ g _ { 1 } , g _ { 2 } , . . . g _ { n } \} } \\ { G _ { n f } ^ { p o s e } ( v ) = G ( \omega _ { n f } ^ { v } ) , \omega _ { n f } ^ { v } = \{ n _ { 1 } , n _ { 2 } , . . . n _ { m } \} } \end{array} \right.
$$

**瓶颈分析**：原始3DGS中，高斯原语的位置是可学习的，且在训练过程中持续进行密度化（克隆与分裂）。这导致两个问题：（1）原语集合动态变化，使得相邻训练步的位姿梯度来源不一致（见Figure 3）；（2）3DGS缺乏NeRF体积渲染中沿射线的空间采样机制，无法实现由粗到精的渐进对齐。两者叠加使得仅使用RGB图像的联合优化极易陷入局部极小值。

### 核心模块一：稳定梯度流设计

为消除位姿梯度的不稳定性，Energy-GS从三个层面重塑梯度流：

**（1）固定基元位置**：将高斯原语的位置设为非可学习参数，在联合优化阶段禁止位置更新。这确保了渲染图元集的空间稳定性，位姿梯度不再受原语位置漂移的干扰。

**（2）稳定瓦片图元选择**：原始3DGS基于 $3\sigma$ 准则为每个瓦片 $B$ 选择参与渲染的原语集合：

$$
Set _ { B } ^ { g s } = \{ g _ { i } \in P | r ( g _ { i } ) < 3 \sigma \}
$$

其中 $\sigma$ 是可学习参数，随训练变化，导致同一瓦片的图元集合动态改变。Energy-GS将其替换为基于固定瓦片尺寸 $t$ 的选择准则：

$$
OurSet _ { B } ^ { g s } = \{ g ^ { \prime } { } _ { i } = g _ { i } , r ( g ^ { \prime } { } _ { i } ) < t | g _ { i } \in P \}
$$

该设计使每个瓦片参与渲染的原语集合在训练全程保持不变，消除了因 $\sigma$ 变化导致的梯度来源波动。

**（3）延迟密度化控制**：密度化操作（克隆与分裂）会改变原语数量和分布，破坏已建立的稳定梯度流。Energy-GS将其激活时机与图像能量层级绑定：

$$
s = m i n \{ s t e p \in \{ 1 , \dots , N \} \mid l v ( s t e p ) > L \}
$$

即只有当监督图像的能量层级 $lv$ 超过阈值 $L$ 时，才激活密度化。在低能量阶段（$lv \leq L$），原语集合完全固定，位姿梯度保持稳定；待位姿大致收敛后，再引入密度化以增强场景细节表达能力。值得注意的是，虽然原语位置不更新，但Energy-GS仍计算其反向传播梯度，以确保克隆和分裂操作能正确执行。

### 核心模块二：图像能量引导的渐进对齐

稳定梯度流解决了梯度一致性问题，但联合优化仍可能陷入局部极小——表现为“多壳现象”（Figure 7），即位姿在多个局部极小值之间漂移。Energy-GS通过图像能量分解，模拟由粗到精的渐进学习过程。

**（1）图像能量分解**：对监督图像 $I$ 进行奇异值分解（SVD），定义其总能量为Frobenius范数的平方：

$$
E = \sum _ { i = 1 } ^ { n } \sigma _ { i } ^ { 2 } , \sigma _ { 1 } \geq \sigma _ { 2 } \geq . . . \geq \sigma _ { n } > 0
$$

其中 $\sigma_i$ 为奇异值。使用前 $lv$ 个奇异值及对应向量可重建低能量图像：

$$
I _ { E } = U _ { l v } \Sigma _ { l v } V _ { l v } ^ { T } = \sum _ { i = 0 } ^ { l v } u _ { i } \sigma _ { i } v _ { i } ^ { T }
$$

低 $lv$ 值对应低频结构（主体轮廓），高 $lv$ 值逐步恢复高频细节（纹理边缘）。

**（2）渐进能量掩膜**：为平滑过渡，对 $lv > 1$ 的能量分量施加掩膜控制：

$$
I _ { E } ( \alpha ) = ( \omega ( \alpha ) \cdot U _ { l v } ) \cdot ( \omega ( \alpha ) \cdot \Sigma _ { l v } ) \cdot ( \omega ( \alpha ) \cdot V _ { l v } ^ { T } )
$$

其中权重函数为：

$$
\omega ( \alpha ) = l o g _ { 1 0 } ( ( \alpha - \frac { l v } { n } ) \cdot 2 5 5 ) / 2 5 5
$$

$\alpha$ 随优化进度从0增长至1，逐步释放高频能量。$lv=1$ 的能量分量（最低频结构）始终完全保留，确保基础几何对齐不受掩膜影响。

**（3）由粗到精的监督机制**：优化初期，目标能量图像仅包含低频结构，光度损失引导位姿进行大范围粗对齐；随着 $\alpha$ 增大，高频细节逐步注入，位姿在已收敛的粗位姿基础上进行精细调整。这一机制模拟了NeRF中沿射线由远及近的采样策略，使3DGS在联合优化中能够稳定收敛至全局最优位姿。

### 1D信号对齐等效验证

为隔离验证各模块的有效性，论文设计了1D信号对齐的等效降维实验（Figure 4）。将alpha-blending抽象为可微合成算子，3D场景的位姿对齐退化为1D信号的位移恢复。实验结果（Table 1）表明：仅重设计梯度流（固定原语位置 + 稳定瓦片选择）时，平移误差（ATE）为0.0001，渲染PSNR达63.17，显著优于允许位置学习和密度化的配置。进一步加入能量渐进策略后，性能达到最优。该等效实验直接验证了“固定基元 + 延迟密度化 + 能量渐进”三者协同的必要性。

![[assets/figures/papers/paper_list_l2078_https_openaccess_thecvf_com_content_CVPR2026_html_Gao_Energy_GS_Image_En/figures/004_Figure_4.jpg]]
*Figure 4: Visualization of the equivalent dimensionality-reduction task and 1D signal alignment results. The left part shows that alphablending can be abstracted as a differentiable compositing operator that maps a set of Gaussians to values at query locations. Applied pointwise, the same operator can compose 2D patches and 1D signals. Correspondingly, the alignment variables reduce from 3D camera pose to 2D patch transforms and 1D signal shifts. For 1D alignment, we crop two overlapping segments from the full signal (analogous to a co-visible region in a 3D scene) and treat their locations as ground-truth. Joint optimization then reconstructs each segment while recovering its position to match the g...*

### 补充图表

![[assets/figures/papers/paper_list_l2078_https_openaccess_thecvf_com_content_CVPR2026_html_Gao_Energy_GS_Image_En/figures/003_Figure_3.jpg]]
*Figure 3: Comparison of pose gradients between 3DGS and NeRF over two consecutive training steps. The left side shows the pose gradient updates of the original 3DGS. Since the positions of Gaussian primitives are adjusted during training, the set of primitives contributing to the camera pose gradient changes dynamically, resulting in unpredictable camera pose shifts. In contrast, NeRF employs a globally unique MLP to represent the scene, which avoids unstable gradient changes*



## 实验与关键发现

### 核心实验设计

本文通过在合成数据集（Synthetic NeRF）与真实捕获数据集（MipNeRF360）上，与基于 NeRF 的联合优化方法 **BARF**（Lin et al., ICCV 2021）、**SC-NeRF**（Jeong et al., ICCV 2021），以及基于 3DGS 的联合优化方法 **CF-GS**（Fu et al., CVPR 2024）、**3R-GS**（Huang et al., 2025）进行对比，验证 Energy-GS 在渲染质量与位姿估计精度上的有效性。所有对比方法使用相同随机生成的初始相机位姿噪声，并采用官方开源实现及默认超参数，确保公平性（Table 2 说明）。

![[assets/figures/papers/paper_list_l2078_https_openaccess_thecvf_com_content_CVPR2026_html_Gao_Energy_GS_Image_En/figures/007_Table_2.jpg]]
*Table 2: Quantitative rendering results of different methods on the datasets. The initial camera pose noise for all methods in the same scene is identical and randomly generated. All results are obtained using the official open-source implementations of the respective methods, without any modification to their default hyperparameters. The full results can be found in the supplementary material*

此外，通过 1D 信号对齐的等效降维实验（Figure 4, Table 1），本文在可控条件下剥离了 3D 场景的复杂性，定量验证了各组件对位姿梯度稳定性与收敛性的独立贡献。

![[assets/figures/papers/paper_list_l2078_https_openaccess_thecvf_com_content_CVPR2026_html_Gao_Energy_GS_Image_En/figures/005_Table_1.jpg]]
*Table 1: Rendering quality (PSNR) and shift error (ATE) across four strategies. Signal A is used as a fixed anchor and serves as the position reference. Combining the redesigned gradient flow with the energy strategy (ours) achieves the best overall performance*

![[assets/figures/papers/paper_list_l2078_https_openaccess_thecvf_com_content_CVPR2026_html_Gao_Energy_GS_Image_En/figures/011_Table_4.jpg]]
*Table 4: Quantitative results of the ablation study. After incrementally adding each proposed component, we observe consistent improvements in both scene reconstruction and camera pose estimation. The findings in the 3D scenes align with the conclusions drawn from the 1D experiment in Figure. 4, further validating the effectiveness of our proposed method*

---

### 主实验结果

#### 渲染质量

在合成数据集上，Energy-GS 在多个场景上取得了优于或可比于 BARF 的渲染质量。典型结果如下：

| 场景 | BARF PSNR↑ | Energy-GS PSNR↑ | Δ |
|------|-----------|-----------------|---|
| chair | 28.35 | 29.81 | +1.46 |
| hotdog | 31.90 | 32.90 | +1.00 |
| lego | 26.92 | 30.35 | +3.43 |

（数据来源：Table 2；完整指标含 SSIM 与 LPIPS，详见原文补充材料。）

在 MipNeRF360 数据集上，Energy-GS 的渲染性能与 **3R-GS** 基本持平，后者额外使用了深度与特征对应等几何先验，而本文方法仅依赖 RGB 图像。

#### 位姿估计精度

在合成数据集上，Energy-GS 的位姿估计误差（旋转角与绝对轨迹误差 ATE）在所有对比方法中最低（Table 3）。这一优势在复杂场景（如 stump）中依然保持，表明能量引导策略有效抑制了联合优化中的局部极小值问题。

![[assets/figures/papers/paper_list_l2078_https_openaccess_thecvf_com_content_CVPR2026_html_Gao_Energy_GS_Image_En/figures/008_Table_3.jpg]]
*Table 3: Quantitative pose estimation results of different methods on datasets. The full results are shown in the supplementary material*

---

### 消融实验

消融实验通过逐步叠加组件，揭示了各模块的独立贡献（Table 4, Figure 6）：

![[assets/figures/papers/paper_list_l2078_https_openaccess_thecvf_com_content_CVPR2026_html_Gao_Energy_GS_Image_En/figures/009_Figure_6.jpg]]
*Figure 6: Ablation results of the gradient-flow strategy and the progressive alignment strategy. The results in (a) show that simply adding learnable pose parameters and performing joint optimization does not yield satisfactory outcomes. Based on our experience, training with only RGB supervision almost always fails to converge. The results in (b) demonstrate that reorganizing the pose gradient flow improves optimization performance, yet the method still tends to fall into local minima. In this case, the camera poses may drift within a small range, and the method can easily fail under larger noise, especially when large rotational noise is present. Finally, (c) presents the results of our full pipeli...*

1. **仅添加可学习位姿（无任何改进）**：PSNR 仅 8.08，渲染几乎失败。这表明原始 3DGS 的位姿梯度流无法支撑有效的联合优化。
2. **加入梯度流重设计**：PSNR 提升至 12.38，旋转误差从 8.572° 降至 4.253°。优化有所改善，但仍易陷入局部极小（Figure 6b）。
3. **进一步加入能量控制策略**：PSNR 跃升至 24.12，旋转误差降至 1.065°，实现了稳定的由粗到精的位姿对齐（Figure 6c）。

该消融序列与 1D 信号对齐实验的结论高度一致：仅重设计梯度流而缺乏能量策略时，位姿优化仍会出现“多壳现象”（multi-shell phenomenon，Figure 7），即相机位姿在多个虚假极小值之间漂移；能量控制策略通过渐进式提高监督信号频率，使优化过程能够穿越这些局部极小，收敛至正确位姿分布。

![[assets/figures/papers/paper_list_l2078_https_openaccess_thecvf_com_content_CVPR2026_html_Gao_Energy_GS_Image_En/figures/010_Figure_7.jpg]]
*Figure 7: Multi-shell phenomenon leading to local minima. A common reason for failure in joint optimization, even after establishing stable pose gradients, is the multi-shell phenomenon, which frequently occurs in NeRF-based joint optimization*

#### 1D 信号对齐实验的定量佐证

在 1D 信号对齐实验中（Table 1），重设计梯度流结合能量策略的配置将平移误差（ATE）降至 0.0001，渲染 PSNR 达 63.17，显著优于仅重设计梯度流（ATE 0.0004, PSNR 62.63）及含可学习位置与密度化的配置（ATE 0.0005, PSNR 62.40）。这从降维层面证实了固定基元位置与能量渐进策略对位姿梯度一致性的关键作用。

---

### 失败模式与局限性

Figure 7 明确揭示了即便建立了稳定位姿梯度，联合优化仍可能因“多壳现象”而失败——这是基于 NeRF 的联合优化中已观察到的典型问题，在 3DGS 中同样存在。能量控制策略虽能显著缓解该问题，但本文未报道在更大噪声幅度或更少视图条件下的表现，也未探讨能量层级阈值 $L$ 的自适应选择机制。此外，SVD 分解带来的额外计算开销在实际部署中的可接受性，以及该方法向动态场景或在线 SLAM 系统的扩展，仍属开放问题。

---

### 图表结论摘要

- **Figure 5**：在合成数据集上，Energy-GS 的渲染结果与联合优化后的相机位姿分布均接近真值，紫色相机（优化后）与蓝色相机（真值）高度重合。
- **Table 2**：Energy-GS 在仅使用 RGB 监督的条件下，渲染质量与使用额外几何先验的 3R-GS 可比，且在多数场景上超过 BARF 与 CF-GS。
- **Table 3**：位姿估计误差在所有对比方法中最低，验证了能量引导渐进对齐策略的有效性。
- **Table 4 & Figure 6**：梯度流重设计与能量控制策略缺一不可，二者协同才能实现稳定的位姿收敛与高质量渲染。
- **Figure 7**：多壳现象是导致联合优化失败的核心瓶颈，能量策略通过由粗到精的频率调度有效穿越局部极小。

![[assets/figures/papers/paper_list_l2078_https_openaccess_thecvf_com_content_CVPR2026_html_Gao_Energy_GS_Image_En/figures/006_Figure_5.jpg]]
*Figure 5: Comparison on the synthetic dataset. For each scene, we randomly add noise to the ground truth camera poses and employ a joint optimization strategy to reconstruct the 3D scene. The left side shows the rendering results and the jointly optimized poses obtained by different methods, while the right side presents the ground-truth images and the initial camera poses, where blue cameras represent the ground-truth poses and purple cameras denote the poses after joint optimization. The results demonstrate that our method achieves competitive performance in both reconstruction quality and pose estimation accuracy. The full results can be found in the supplementary material*



## 定位与知识库关联

### 1. 核心瓶颈与因果机制

Energy-GS 的核心洞察源于对 3DGS 与 NeRF 在位姿联合优化中行为差异的深入剖析。原始 3DGS（Kerbl et al., SIGGRAPH 2023）的点基渲染范式存在一个根本性瓶颈：**高斯原语的位置在训练过程中持续变化，导致参与每个瓦片渲染的图元集合动态波动，进而使相机位姿梯度流不稳定**。公式上，3DGS 的位姿梯度定义为 $G_{gs}^{pose}(v) = F(\omega_{gs}^v)$，其中参数集 $\omega_{gs}^v = \{g_1, g_2, ..., g_n\}$ 是离散的高斯原语集合；而 NeRF 的位姿梯度 $G_{nf}^{pose}(v) = G(\omega_{nf}^v)$ 作用于全局唯一的 MLP 参数集，天然具有稳定性（Eq.1, Figure 3）。这一差异使得 3DGS 在仅使用 RGB 图像的联合优化中极易陷入局部极小值，且缺少 NeRF 体积渲染中由粗到精的渐进对齐能力。

针对上述瓶颈，Energy-GS 设计了两个因果调节旋钮：
- **稳定梯度流**：通过固定高斯原语位置为非可学习参数，并重新设计密度化策略（延迟激活、基于固定瓦片尺寸 $t$ 的图元选择替代 3σ 准则），确保每个瓦片的渲染图元集合在训练中保持不变，从而稳定位姿梯度。
- **由粗到精的能量引导**：利用图像 SVD 能量分解，从低能量（低频结构）到高能量（高频细节）渐进式地提供监督信号，模拟体积渲染中的渐进对齐过程，引导联合优化收敛至全局最优位姿。

### 2. 与基线方法的关系

Energy-GS 处于 **3DGS 位姿联合优化**这一新兴研究脉络中，其直接对标的方法可归纳为以下两类：

**NeRF-based 联合优化基线**：
- **BARF**（Lin et al., ICCV 2021）是最早提出将 NeRF 与相机位姿联合优化的代表性工作，通过从低频到高频的渐进式位置编码实现由粗到精的对齐。Energy-GS 借鉴了其“渐进式”思想，但将其从位置编码域迁移至图像能量域，以适配 3DGS 的渲染范式。
- **SC-NeRF**（Jeong et al., ICCV 2021）进一步探索了自标定 NeRF 的位姿优化，但仍受限于 NeRF 的体积渲染框架。

**3DGS-based 联合优化基线**：
- **CF-GS**（Fu et al., CVPR 2024）是较早尝试将 3DGS 与序列帧位姿联合优化的方法，但未从根本上解决梯度不稳定问题。
- **3R-GS**（Huang et al., 2025）通过引入深度和特征对应等额外几何先验来辅助全局联合优化，在 MipNeRF360 等复杂场景上表现强劲。Energy-GS 与之形成互补：3R-GS 依赖多模态先验，而 Energy-GS 仅使用 RGB 图像，通过重塑梯度流和能量策略实现稳定对齐。

**关键差异**：与上述方法相比，Energy-GS 的独特贡献在于**从渲染图元的底层更新机制入手**，而非依赖外部先验或修改网络结构。具体而言，其改变了四个关键设计槽位（Table 1, Figure 4 的 1D 信号实验提供了等效验证）：
1. **基元位置可学习性**：从可学习位置改为固定位置。
2. **密度化时机**：从训练全程持续进行改为根据图像能量阈值 $L$ 延迟激活（$s = \min\{step \in \{1,\dots,N\} \mid lv(step) > L\}$, Eq.5）。
3. **渲染图元选择准则**：从基于 3σ 原则的动态选择改为基于固定瓦片长度 $t$ 的选择（$OurSet_{B}^{gs} = \{g'_i = g_i, r(g'_i) < t \mid g_i \in P\}$, Eq.3）。
4. **监督图像**：从全分辨率 RGB 图像改为根据能量层级渐进恢复的 SVD 图像（$I_E = U_{lv} \Sigma_{lv} V_{lv}^T$, Eq.7）。

### 3. 适用边界与局限性

**适用边界**：
- Energy-GS 在合成数据集（Synthetic NeRF）上展现出最强的位姿估计精度，旋转角和绝对轨迹误差在所有对比方法中最低（Table 3），渲染质量与 BARF 相当或更优（如 lego 场景 PSNR 达 30.35，较 BARF 的 26.92 提升 3.43 dB，Table 2）。
- 在 MipNeRF360 真实场景数据集上，渲染性能和位姿优化结果与 3R-GS 持平（Table 2, Table 3），表明方法对复杂真实场景具有一定泛化能力。

**局限性**（论文未明确列出，基于方法设计和实验结果推断，需进一步验证）：
- **大噪声/少视图场景的收敛性**：能量策略依赖图像 SVD 分解提供稳定的低频结构，当初始位姿噪声极大或视图极度稀疏时，低频结构本身可能不足以提供可靠的几何约束，此时可能需要结合深度或特征匹配等额外先验。
- **能量层级阈值的敏感性**：密度化激活阈值 $L$ 的选择直接影响优化进程，论文未系统探讨其自适应调整机制，实际部署中可能需要针对不同场景手动调参。
- **动态场景与在线系统的适用性**：当前方法假设静态场景，高斯原语位置的固定策略在动态场景中可能需要重新设计；此外，SVD 分解的计算开销在实时 SLAM 系统中可能成为瓶颈。

### 4. 开放问题

1. **几何先验的融合**：在更大噪声或更少视图的极端条件下，Energy-GS 能否通过融合深度、光流或特征对应等几何先验来保证收敛？这将是与 3R-GS 等方法互补的重要方向。
2. **自适应能量调度**：能量层级阈值 $L$ 和掩膜函数 $\omega(\alpha)$ 能否根据场景复杂度和位姿误差自适应调整，以减少人工调参的依赖？
3. **动态场景与时序连续性**：该方法能否扩展至动态场景或在线 SLAM 系统？如何处理时间连续性和计算效率的平衡？
4. **计算效率优化**：图像 SVD 分解带来的额外计算开销在实际部署中是否可接受？是否存在更高效的替代方案（如小波变换、拉普拉斯金字塔）来实现类似的渐进能量控制？
5. **多壳现象的深层机理**：Figure 7 可视化的多壳现象揭示了即使梯度流稳定后仍可能陷入局部极小，其深层几何与优化机理尚待进一步理论分析，这可能为设计更鲁棒的优化策略提供指导。



## 原文 PDF

![[paperPDFs/CVPR_2026/Energy_GS_Image_Energy_guided_Pose_Alignment_Gaussian_Splatting_with_redesigned_pose_gradient_flow.pdf]]
