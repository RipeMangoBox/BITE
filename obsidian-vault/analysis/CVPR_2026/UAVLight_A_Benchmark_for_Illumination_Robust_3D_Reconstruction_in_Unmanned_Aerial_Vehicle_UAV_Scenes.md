---
title: "UAVLight: A Benchmark for Illumination-Robust 3D Reconstruction in Unmanned Aerial Vehicle (UAV) Scenes"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/UAVLight_A_Benchmark_for_Illumination_Robust_3D_Reconstruction_in_Unmanned_Aerial_Vehicle_UAV_Scenes.pdf
project_link: "https://uavlight.github.io/"
code_link: null
aliases:
- UAVLight
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/benchmarks_datasets_evaluation
core_operator: 通过重复的GPS引导飞行轨迹在一天中的不同固定时间进行低空拍摄，从而隔离光照变化，同时保持几何结构和视点一致性。
primary_logic: 通过将光照变化与其他因素解耦，UAVLight能够系统评估跨时间的光度一致性和重光照稳定性，实验表明显式逆渲染方法在跨光照评估中始终优于隐式外观建模方法。
claims:
- 通过RTK定位和地面控制点验证，平均几何误差约为10 cm，确保了可靠的几何参考。
- LumiGauss作为显式光照估计方法，在PSNR、SSIM、LPIPS上始终优于隐式方法（NeRF-W, GS-W等），验证了显式建模在光照鲁棒性方面的优势。
- 数据集设计严格隔离光照变化：相同轨迹在不同时间重复飞行，从而排除几何和语义变化的干扰。
- "UAVLight Scene Town 上 PSNR (dB) = LumiGauss: 23.59"
---

# UAVLight: A Benchmark for Illumination-Robust 3D Reconstruction in Unmanned Aerial Vehicle (UAV) Scenes

> [!tip] 核心洞察
> 通过将光照变化与其他因素解耦，UAVLight能够系统评估跨时间的光度一致性和重光照稳定性，实验表明显式逆渲染方法在跨光照评估中始终优于隐式外观建模方法。

| 字段 | 内容 |
|------|------|
| 中文题名 | UAVLight：面向无人机场景光照鲁棒三维重建的基准 |
| 英文题名 | UAVLight: A Benchmark for Illumination-Robust 3D Reconstruction in Unmanned Aerial Vehicle (UAV) Scenes |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2511.21565) · [Project](https://uavlight.github.io/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/benchmarks_datasets_evaluation |
| Method | UAVLight 数据集构建与评估管线 |
| Dataset | UAVLight Scene Town, UAVLight Scene Footbridge, UAVLight Scene Intersection |

> [!tip] 效果简介
> - UAVLight Scene Town 上，PSNR (dB) LumiGauss: 23.59 vs NeRF-W: 19.63 (+3.96)。
> - UAVLight Scene Footbridge 上，PSNR (dB) LumiGauss: 20.89 vs NeRF-W: 17.25 (+3.64)。
> - UAVLight Scene Intersection 上，PSNR (dB) LumiGauss: 23.04 vs GS-W: 19.98 (+3.06)。

## 概述

**问题瓶颈**：室外无人机（UAV）长时间飞行采集的多视图图像中，自然光照（太阳方向、阴影、环境光）发生剧烈变化，打破了经典三维重建中“恒定光照”的隐含假设。这导致光度一致性失效，进而引发几何漂移、颜色不一致和阴影烙印等系统性问题，严重制约了无人机场景下三维重建的鲁棒性。

**核心因果机制**：现有光照变化数据集往往混杂了几何、语义和视点的变化，无法单独评估光照对重建的影响。UAVLight通过**重复GPS引导的固定轨迹在一天中多个固定时段进行低空天底拍摄**，将光照变化作为唯一变量加以隔离，同时保持几何结构和视点高度一致。这一设计使得跨时段的光度一致性和重光照稳定性可以被系统量化。

**核心发现**：在UAVLight基准上，**显式逆渲染方法（如LumiGauss）在跨光照评估中始终优于隐式外观建模方法（如NeRF-W、GS-W）**。例如，在Town场景中，LumiGauss的PSNR达到23.59 dB，比NeRF-W（19.63 dB）高出3.96 dB；在Footbridge场景中，LumiGauss（20.89 dB）比NeRF-W（17.25 dB）高出3.64 dB。这表明，将外观分解为反射率与光照的显式建模策略，在面对自然光照变化时具有更强的鲁棒性。

**方法定位**：UAVLight本身是一个**数据集构建与评估管线**，而非一种新的重建算法。其关键贡献在于：（1）设计了严格隔离光照的数据采集协议；（2）提出了结合RTK约束的分组光束法平差（Bundle Adjustment）位姿估计方法，使几何参考的平均误差控制在约10 cm；（3）基于GPS和时间戳计算太阳方向真值，为显式光照估计方法提供物理先验；（4）构建了覆盖12个场景、多时段的标准化评估基准。

**知识库定位**：UAVLight填补了现有数据集中“室外自然光照变化+几何一致+视点可控”的空白。如表1所示，已有数据集或局限于室内/物体级（如NeRF合成数据集），或光照变化与几何/语义变化混杂（如野外互联网照片集），无法支持对光照鲁棒性的独立评估。UAVLight的方法谱系可定位于**光照感知三维重建**的交叉点，其评估管线同时兼容隐式外观建模（**NeRF-W**, Martin-Brualla et al., CVPR 2021; **GS-W**, Zhang et al., ECCV 2024）和显式逆渲染（**NeRF-OSR**, Rudnev et al., ECCV 2022; **LumiGauss**）两类范式。

**主要结果概要**：在12个场景的定量评估中，显式方法LumiGauss在PSNR、SSIM、LPIPS三个指标上全面领先。几何精度方面，通过地面控制点验证，平均垂直误差为10.31 cm，平面误差为11.83 cm，确保了基准的几何可靠性。

## 背景与动机

### 问题背景：光照不一致性对多视图重建的挑战

基于多视图几何的三维重建方法，无论是传统的运动恢复结构（SfM）与多视图立体（MVS），还是近年来兴起的神经辐射场（NeRF）和三维高斯泼溅（3DGS），其理论根基都建立在“恒定光照假设”之上——即假设场景在不同视角下的外观保持光度一致性。然而，在室外无人机（UAV）长时间飞行场景中，这一假设被系统性地打破：太阳位置随时间移动，导致阴影位移、高光漂移、环境光色温变化，使得同一几何表面在不同时刻拍摄的图像中呈现截然不同的颜色和亮度。这种光照不一致性直接导致几何重建中的匹配漂移、颜色不一致以及“阴影烙印”（shadow baking）等伪影，即阴影被错误地固化到纹理或几何中。

### 现有方法的两种路径及其缺口

为应对光照变化，现有方法大致分为两条技术路径：

**隐式外观建模（Implicit Appearance Modeling）** 通过在神经场中引入逐视图或逐射线的隐变量来“吸收”曝光、白平衡、阴影和天气引起的外观变化。代表性工作包括 **NeRF-W**（Martin-Brualla et al., CVPR 2021）和 **GS-W / WildGaussians**（Zhang et al., ECCV 2024）等。这类方法将外观变化视为需要补偿的“噪声”，而非需要建模的物理信号，其隐变量缺乏物理可解释性，无法显式推理光照与反射的分离，因此在跨光照场景中容易产生颜色伪影和几何模糊。

**显式逆渲染（Explicit Inverse Rendering）** 则试图将外观分解为反射率（albedo）与光照的乘积，通过估计场景的光照环境来实现物理上可解释的重光照和阴影推理。代表性工作如 **NeRF-OSR**（Rudnev et al., ECCV 2022）和 **LumiGauss**。这类方法需要较强的光照先验（如太阳-天空模型），在室外场景中具有天然优势，但其对光照估计的精度高度依赖先验的准确性。

然而，**评估这两种路径在光照鲁棒重建中的真实能力存在一个根本性瓶颈**：现有数据集无法提供“光照变化而几何不变”的受控条件。室内数据集光照可控但场景单一；室外数据集要么只在单一时段采集（光照恒定），要么在不同时段采集时改变了飞行轨迹，导致几何和语义变化与光照变化混杂，无法归因。这使得研究者难以回答一个核心问题：在真实室外场景中，显式光照建模是否真的比隐式外观建模更鲁棒？

### UAVLight的动机：解耦光照与几何

UAVLight基准的核心动机正是填补这一评估缺口。其设计原则是**将光照作为唯一的变量进行隔离**：通过无人机沿固定航点轨迹在一天中的多个固定时段进行低空天底视角重复飞行，确保不同时段的数据共享几乎一致的几何结构和相机视点，仅光照条件随太阳位置自然变化。这种“可控的自然光照变化”设计，使得UAVLight能够系统性地评估跨时间的光度一致性和重光照稳定性，为光照鲁棒三维重建方法提供可靠的量化比较平台。

## 核心创新

UAVLight 的核心创新并非提出一个新的重建算法，而是构建了一个**将光照变化与其他混淆因素系统性解耦的评估基准**。现有户外数据集通常在一次短时间窗口内采集，光照条件近似恒定，无法评估方法在光照变化下的鲁棒性。UAVLight 通过三个关键的 changed slots 实现了这一解耦。

### 1. 多时段重复轨迹采集协议

传统数据采集采用单次短时间窗口飞行，光照基本恒定。UAVLight 的核心改变在于：**对同一场景，使用 GPS 引导的无人机沿固定航点轨迹，在一天中的多个固定时间进行重复低空飞行**（见 Figure 1）。这一设计直接切中了瓶颈的因果机制——光照不一致性打破了多视图几何重建中的恒定光照假设，导致几何漂移、颜色不一致和阴影烙印。通过重复轨迹采集，场景的几何结构和视点保持一致，仅光照自然变化，从而将光照隔离为唯一的变量。

该协议在物理上也具有可解释性：低空天底视角的飞行使得直接太阳光占据主导，漫反射分量可忽略，光照变化主要由太阳位置决定。这为后续的显式光照建模提供了清晰的物理先验。

### 2. 融合 RTK 约束的分组 Bundle Adjustment

纯 SfM 在位姿估计中不引入绝对尺度约束，难以保证多时段数据之间的几何一致性。UAVLight 将位姿估计改为**分组 Bundle Adjustment 并加入 RTK 位置约束**，总能量函数为：

$$E_{\mathrm{total}} = E_{\mathrm{group}} + \sum_{i} \kappa_{i} \left\| \mathbf{c}_{i} - \mathbf{t}_{\mathrm{RTK}_{i}} \right\|_{2}^{2}$$

其中 $E_{\mathrm{group}}$ 为分组重投影误差项，第二项将相机位置 $\mathbf{c}_{i}$ 约束到 RTK 测量的绝对坐标 $\mathbf{t}_{\mathrm{RTK}_{i}}$。这一设计使得不同时段的重建结果共享统一的度量尺度坐标系，为跨光照评估提供了可靠的几何参考。通过地面控制点验证，平均几何误差约为 10 cm（垂直误差 10.31 cm，平面误差 11.83 cm，Table 6），确保了基准的几何可信度。

### 3. 基于 GPS/时间戳的太阳方向真值

现有数据集不提供光照真值，无法量化光照估计的物理准确性。UAVLight 利用采集时的 GPS 坐标和时间戳，通过标准太阳位置算法计算每个时段的太阳方向矢量，作为**无需额外传感器的光照真值**：

$$s_{\mathrm{E}} = \sin(\gamma_{\mathrm{sun}}), \quad s_{\mathrm{N}} = \cos(\gamma_{\mathrm{sun}}), \quad s_{\mathrm{U}} = \sin(\alpha_{\mathrm{sun}}) = \cos(\theta_{\mathrm{sun}})$$

再通过坐标变换 $\mathbf{s}_{\mathrm{Colmap}} = \mathbf{R} \mathbf{s}_{\mathrm{ENU}}$ 转换到重建坐标系。这一真值为显式逆渲染方法提供了可验证的物理先验，也是评估光照解耦能力的基础。

### 创新带来的核心发现

上述三个 changed slots 共同支撑了 UAVLight 的核心洞察：**显式逆渲染方法在跨光照评估中始终优于隐式外观建模方法**。在成对跨光照协议下（Figure 5），LumiGauss 作为显式光照估计方法，在 12 个场景上均取得最高 PSNR（如 Town 场景 23.59 dB vs. NeRF-W 19.63 dB，Footbridge 场景 20.89 dB vs. NeRF-W 17.25 dB，Tables 3-4）。隐式方法（NeRF-W、GS-W、WildGaussians）虽然通过逐视图/逐射线隐变量吸收了外观变化，但在跨光照泛化时出现纠缠导致的伪影；显式方法将外观分解为反射率和光照，展现出更强的解耦能力和多光照重建稳定性。

## 整体框架

UAVLight 并非提出一种新的重建算法，而是构建了一套从数据采集到评估的完整管线，旨在系统性地解耦并评估光照变化对三维重建的影响。该管线的核心设计逻辑是：**通过重复的GPS引导飞行轨迹在一天中的不同固定时间进行低空拍摄，从而将光照变化隔离为唯一变量，同时保持几何结构和视点的一致性**。

### 管线模块与数据流

整个基准的构建与评估管线由以下模块串联而成：

1. **多时段重复轨迹采集**：无人机沿预设的航点路径，在一天中的多个固定时段（如清晨、正午、傍晚）重复飞行，以天底视角低空拍摄。这一协议确保同一场景在不同自然光照条件下被记录，而场景几何和相机视点保持高度一致（Section 3, Table 5）。

2. **帧采样与度量尺度重建**：从每个时段的视频流中采样关键帧，采用分组Bundle Adjustment（BA）并引入RTK位置约束进行SfM/MVS重建。总能量函数为：
   $$E_{\mathrm{total}} = E_{\mathrm{group}} + \sum_{i} \kappa_{i} \left\| \mathbf{c}_{i} - \mathbf{t}_{\mathrm{RTK}_{i}} \right\|_{2}^{2}$$
   其中 $E_{\mathrm{group}}$ 为分组重投影误差项，$\mathbf{c}_i$ 为相机位置，$\mathbf{t}_{\mathrm{RTK}_i}$ 为RTK测量位置。这一设计使得多时段数据的相机位姿在统一度量坐标系下联合优化，生成具有物理尺度的稠密点云作为几何参考（公式(1)(2)，Section 4）。

3. **后处理与质量控制**：手动筛选去除运动模糊、极端曝光等不良帧，并进行去畸变处理，确保输入数据的质量（Section 4）。

4. **太阳方向真值估计**：利用每帧的GPS坐标和时间戳，通过标准太阳位置算法计算太阳方位角 $\gamma_{\mathrm{sun}}$ 和高度角 $\alpha_{\mathrm{sun}}$，得到本地ENU坐标系下的单位太阳方向矢量：
   $$s_{\mathrm{E}} = \sin(\gamma_{\mathrm{sun}}), \quad s_{\mathrm{N}} = \cos(\gamma_{\mathrm{sun}}), \quad s_{\mathrm{U}} = \sin(\alpha_{\mathrm{sun}}) = \cos(\theta_{\mathrm{sun}})$$
   再通过旋转矩阵 $\mathbf{R}$ 转换至COLMAP重建坐标系：
   $$\mathbf{s}_{\mathrm{Colmap}} = \mathbf{R} \mathbf{s}_{\mathrm{ENU}}$$
   这为显式逆渲染方法提供了物理光照先验（公式(3)(4)，Section 4）。

5. **几何精度验证**：通过地面控制点（checkpoints）对重建点云进行精度验证。经验证，**平均垂直误差约10.31 cm，平面误差约11.83 cm**，确保了几何参考的可靠性（Figure 4, Table 6）。

6. **跨光照评估协议**：采用成对跨光照（paired cross-illumination）设置——光照从同一时段的一个视图子集估计，在另一个子集上评估，并使用标准化的训练/验证/测试分割，避免时序泄露（Section 6.1–6.2）。

### 输入输出流

- **输入**：无人机在多个固定时段沿相同航点轨迹采集的RGB视频流，以及对应的RTK定位数据和时间戳。
- **输出**：
  - 度量尺度的稠密点云（几何参考）；
  - 每帧的相机位姿（在统一坐标系下）；
  - 每帧对应的太阳方向真值；
  - 标准化的训练/验证/测试分割，用于评估不同重建方法在跨光照条件下的光度一致性和重光照稳定性。

### 核心设计逻辑

该管线的关键洞察在于：**传统多视图重建假设光照恒定，而室外UAV长时间飞行中光照不一致性会打破这一假设，导致几何漂移、颜色不一致和阴影烙印**。UAVLight通过重复轨迹采集协议将光照变化与其他因素（几何、视点、语义）解耦，使得基准能够系统评估跨时间的光度一致性和重光照稳定性。实验表明，显式逆渲染方法（如LumiGauss）在跨光照评估中始终优于隐式外观建模方法（如NeRF-W、GS-W），验证了显式建模在光照鲁棒性方面的优势（Table 3, Table 4）。

### 补充图表

![[assets/figures/papers/paper_list_l2729_https_arxiv_org_abs_2511_21565/figures/001_Figure_1.jpg]]
*Figure 1: Overview of the UAVLight benchmark. Each scene is captured by low-altitude UAV flights along fixed waypointed trajectories at multiple times of day. Our benchmark records natural illumination changes along consistent geometry and viewpoints, enabling quantitative evaluation of illumination-robust reconstruction and relighting*

![[assets/figures/papers/paper_list_l2729_https_arxiv_org_abs_2511_21565/figures/003_Figure_2.jpg]]
*Figure 2: Visualization of representative dense point clouds from 12 selected scenes in our benchmark*

## 核心模块与公式推导

UAVLight的数据集构建与评估管线包含五个关键模块，从数据采集到几何验证形成闭环。本节重点解析其中涉及公式推导的核心模块。

### 多时段重复轨迹采集

该模块是整个基准的核心设计——通过GPS引导的固定航点轨迹在一天中多个固定时间（如上午、正午、下午）重复飞行，在保持几何结构和视点一致的前提下，系统性地引入自然光照变化。这一设计将光照与其他变化因素（几何、语义）解耦，使得后续评估能够隔离光照的影响。Table 5记录了每个场景的时段数量与飞行统计。

### 分组Bundle Adjustment与RTK约束

为从多时段数据中获得度量尺度的几何参考，UAVLight采用分组Bundle Adjustment（BA），并引入RTK位置约束。总能量函数定义为：

$$E_{\mathrm{total}} = E_{\mathrm{group}} + \sum_{i} \kappa_{i} \left\| \mathbf{c}_{i} - \mathbf{t}_{\mathrm{RTK}_{i}} \right\|_{2}^{2}$$

其中，$E_{\mathrm{group}}$为分组重投影误差项，$\mathbf{c}_{i}$为第$i$个相机中心的估计位置，$\mathbf{t}_{\mathrm{RTK}_{i}}$为RTK测量的相机位置，$\kappa_{i}$为约束权重。分组重投影误差的具体形式为：

$$E_{\mathrm{group}} = \sum_{j} \rho_{j} \left( \left\| \pi_{g} ( \mathbf{G}_{r}, \mathbf{P}_{c}, \mathbf{X}_{k} ) - \mathbf{x}_{jk} \right\|_{2}^{2} \right)$$

式中，$\pi_{g}$为投影函数，$\mathbf{G}_{r}$为组内共享的相机内参，$\mathbf{P}_{c}$为相机外参，$\mathbf{X}_{k}$为三维点坐标，$\mathbf{x}_{jk}$为对应的二维观测点，$\rho_{j}$为鲁棒损失函数。分组策略将同一时段的图像归入同一组，允许组内共享参数，从而在优化中保持时序一致性。

### 太阳方向真值估计

为提供物理光照先验，UAVLight利用GPS坐标和时间戳计算每个时段的太阳方向。首先在ENU（东-北-天）坐标系中计算太阳方向单位矢量：

$$s_{\mathrm{E}} = \sin(\gamma_{\mathrm{sun}}), \quad s_{\mathrm{N}} = \cos(\gamma_{\mathrm{sun}}), \quad s_{\mathrm{U}} = \sin(\alpha_{\mathrm{sun}}) = \cos(\theta_{\mathrm{sun}})$$

其中$\gamma_{\mathrm{sun}}$为太阳方位角，$\alpha_{\mathrm{sun}}$为太阳高度角，$\theta_{\mathrm{sun}}$为太阳天顶角。随后通过旋转矩阵$\mathbf{R}$将太阳方向转换到COLMAP重建坐标系：

$$\mathbf{s}_{\mathrm{Colmap}} = \mathbf{R} \mathbf{s}_{\mathrm{ENU}}$$

该坐标变换确保了太阳方向与SfM重建的几何参考系对齐，可直接作为显式光照估计方法（如LumiGauss）的物理先验输入。

### 后处理与几何精度验证

帧采样后进行手动筛选，去除运动模糊、极端曝光等不良帧，再经过去畸变处理。几何精度通过地面控制点验证——Table 6显示平均垂直误差为10.31 cm，平均平面误差为11.83 cm，表明重建点云具备可靠的度量尺度，可作为评估光照鲁棒重建的几何参考。

### 补充图表

![[assets/figures/papers/paper_list_l2729_https_arxiv_org_abs_2511_21565/figures/009_Figure_3.jpg]]
*Figure 3: Illumination variations across similar viewpoints at different times of day. Bottom-right shows ground-truth sunlight directions from GPS and timestamps*

![[assets/figures/papers/paper_list_l2729_https_arxiv_org_abs_2511_21565/figures/010_Figure_4.jpg]]
*Figure 4: Checkpoint-based geometric validation of UAVLight*

## 实验与分析

### 评估协议与公平性保障

UAVLight采用标准化的训练/验证/测试划分，按不同时段分割数据以避免时序泄漏。所有方法均在统一的A800 GPU、PyTorch/CUDA环境下训练，使用相同的相机位姿和评估指标（PSNR、SSIM、LPIPS），确保比较的公平性。

核心评估采用**成对跨光照协议**：从同一时段的视图子集中估计光照，在另一子集上评估渲染质量。这一协议直接测试方法将光照与几何解耦的能力——隐式方法必须依赖外观潜变量外推至未见视图，而显式方法则需通过逆渲染重建物理光照参数。

### 主实验结果

Table 3和Table 4报告了12个场景的完整定量结果。关键发现如下：

**显式光照建模方法在跨光照评估中始终优于隐式方法。** 以LumiGauss为代表的显式高斯泼溅方法，在所有场景上均取得最高PSNR：

- **Town场景**：LumiGauss达到23.59 dB，相比NeRF-W的19.63 dB提升**+3.96 dB**（Table 3）。
- **Footbridge场景**：LumiGauss为20.89 dB，NeRF-W仅17.25 dB，差距**+3.64 dB**（Table 4）。
- **Intersection场景**：LumiGauss为23.04 dB，GS-W为19.98 dB，提升**+3.06 dB**（Table 4）。

![[assets/figures/papers/paper_list_l2729_https_arxiv_org_abs_2511_21565/figures/005_Table_3.jpg]]
*Table 3: Quantitative results on Scenes 1–6. Evaluated using PSNR ↑, SSIM ↑, and LPIPS ↓*

![[assets/figures/papers/paper_list_l2729_https_arxiv_org_abs_2511_21565/figures/006_Table_4.jpg]]
*Table 4: Quantitative results on Scenes 7–12. Evaluated using PSNR ↑, SSIM ↑, and LPIPS ↓*

这一趋势在SSIM和LPIPS指标上同样一致。显式方法通过将外观分解为反射率与光照，实现了更强的解耦能力，在跨时段评估中表现出更稳定的重建质量。隐式方法（NeRF-W、GS-W、WildGaussians）虽然能捕获部分高频细节，但外观潜变量容易与几何信息纠缠，导致跨光照条件下的伪影和颜色偏移。

**高斯泼溅类方法整体优于NeRF类方法。** 在标准指标上，基于3D高斯泼溅的方法（GS-W、WildGaussians、LumiGauss）普遍取得比NeRF-W和NeRF-OSR更高的PSNR。这归因于高斯泼溅显式几何表示在稀疏视角UAV场景中的优势。

### 几何精度验证

基准的可靠性依赖于准确的几何参考。通过RTK定位和地面控制点验证，**平均垂直误差为10.31 cm，平面点误差为11.83 cm**（Table 6，Figure 4）。这一精度水平为光照鲁棒性评估提供了可靠的几何基础。

### 失败模式与局限性分析

尽管显式方法在定量指标上占优，实验揭示了若干系统性问题：

1. **隐式方法的阴影烙印效应**：NeRF-W和GS-W倾向于将阴影烘焙为几何或纹理的一部分，而非建模为光照效果。当跨时段评估时，这些“烙印”阴影与实际光照方向不一致，产生明显的几何漂移和颜色不一致。

2. **显式方法的先验依赖性**：LumiGauss依赖太阳-天空模型作为光照先验。在天空区域可见性受限的低空天底视角下，天空光照估计可能不准确，影响重光照的物理真实性。

3. **自动曝光引入的非线性**：UAV相机自动曝光导致图像强度在不同时段间非线性变化，破坏了光度一致性假设。所有方法在处理极端曝光差异时均出现性能下降。

4. **动态物体缺失**：当前场景仅包含静态结构，未覆盖行人、车辆等动态外观变化。这限制了基准对真实UAV应用场景的覆盖范围。

5. **光照多样性不足**：基准仅包含白天自然光照变化，缺少阴天、季节变化和大气散射等极端条件，无法全面评估方法在更广泛光照条件下的鲁棒性。

### 关键图表结论

- **Figure 3**：展示了相同视点在不同时段的光照变化，以及由GPS/时间戳计算的太阳方向真值。这些真值为显式光照估计方法提供了物理先验。
- **Figure 5**：成对跨光照协议示意图，说明了光照估计与评估的解耦逻辑。
- **Figure 6–7**：可视化对比了不同基线在多个场景和时段下的重建结果。显式方法在阴影一致性和颜色稳定性方面明显优于隐式方法。
- **Table 7–8**：补充定量结果进一步验证了显式方法在Road2、Industrial、Roof、City2、Industrial2、City六个额外场景上的优势。

![[assets/figures/papers/paper_list_l2729_https_arxiv_org_abs_2511_21565/figures/011_Figure_5.jpg]]
*Figure 5: Paired cross-light protocol. Lighting is estimated from one view and applied to another captured at the same time slot*

![[assets/figures/papers/paper_list_l2729_https_arxiv_org_abs_2511_21565/figures/012_Figure_6.jpg]]
*Figure 6: Visualization of the reconstruction results from different baselines on five UAVLight scenes*

![[assets/figures/papers/paper_list_l2729_https_arxiv_org_abs_2511_21565/figures/015_Table_7.jpg]]
*Table 7: Extended quantitative results (Part 1) on Road2, Industrial, and Roof. Metrics are reported separately for PSNR, SSIM, and LPIPS (no slash)*

### 总结

UAVLight实验系统验证了**显式逆渲染方法在光照鲁棒三维重建中的优势**。通过将光照变化与其他因素解耦，基准揭示了隐式外观建模在跨光照场景中的根本性局限——外观潜变量的纠缠导致阴影烙印和几何漂移。LumiGauss的持续领先表明，物理光照先验与显式分解是应对室外UAV光照变化的关键方向。然而，自动曝光、天空建模和动态场景等问题仍有待未来工作解决。

### 补充图表

![[assets/figures/papers/paper_list_l2729_https_arxiv_org_abs_2511_21565/figures/013_Figure_7.jpg]]
*Figure 7: Visualization of the reconstruction results from different baselines on Town with five different time slots*

![[assets/figures/papers/paper_list_l2729_https_arxiv_org_abs_2511_21565/figures/002_Table_1.jpg]]
*Table 1: A taxonomy of existing datasets*

![[assets/figures/papers/paper_list_l2729_https_arxiv_org_abs_2511_21565/figures/007_Table_5.jpg]]
*Table 5: UAVLight scene statistics. Each scene is captured under multiple natural illumination conditions along repeated flight trajectories*

## 方法谱系与知识库定位

### 1. 问题定位：光照不一致性对多视图重建的挑战

传统多视图三维重建方法（包括神经辐射场NeRF及其衍生变体）通常建立在**恒定光照假设**之上，即假设场景外观在采集过程中保持不变。然而，在室外无人机长时间飞行场景中，这一假设被系统性打破——太阳位置变化导致阴影位移、高光漂移和整体辐照度改变，使得光度一致性约束失效，进而引发几何漂移、颜色不一致和阴影烙印等伪影。UAVLight的核心贡献在于**将光照变化从其他混杂因素（几何变化、语义变化、视点变化）中解耦**，构建了首个专门评估光照鲁棒三维重建的无人机基准。

### 2. 方法谱系：从隐式外观建模到显式逆渲染

当前处理光照变化的三维重建方法可沿一条关键轴线划分：**隐式外观建模**与**显式光照估计（逆渲染）**。

#### 2.1 隐式外观建模方法

隐式方法通过在神经场中引入逐视图或逐射线的隐变量来吸收外观变化，而不显式建模物理光照过程：

- **NeRF-W**（Martin-Brualla et al., CVPR 2021）：在NeRF基础上引入逐视图的外观嵌入向量，允许网络学习不同图像之间的外观差异。该方法能有效处理曝光变化和白平衡漂移，但由于外观表示与几何表示高度纠缠，在跨光照评估中容易出现几何-外观混淆。

- **GS-W (Gaussian in the Wild)**（Zhang et al., ECCV 2024）：将隐式外观建模思想迁移到3D高斯泼溅框架，通过为每个高斯点附加外观隐变量来处理光照变化。继承了高斯泼溅的高效渲染优势，但在光照解耦方面仍受限于隐式表示的本质。

- **WildGaussians**：另一类隐式高斯泼溅方法，在补充实验中出现，其核心思路与GS-W类似，通过隐式外观编码吸收光照变化。

这些方法的共同局限在于：**隐式外观编码缺乏物理约束**，网络可能将光照变化错误地解释为几何变化（或反之），导致跨光照泛化能力受限。

#### 2.2 显式逆渲染方法

显式方法通过逆渲染将外观分解为反射率（材质）和光照两个独立分量，建立物理上可解释的表示：

- **NeRF-OSR**（Rudnev et al., ECCV 2022）：面向户外的显式逆渲染方法，使用太阳-天空模型作为光照先验，将场景分解为反射率场和环境光照。在UAVLight基准上，该方法展现出优于隐式方法的跨光照稳定性，但受限于NeRF的渲染效率。

- **LumiGauss**：将显式光照估计与3D高斯泼溅结合的方法。在UAVLight的12个场景中，LumiGauss在PSNR、SSIM、LPIPS三项指标上**始终优于所有隐式方法**。以Town场景为例，LumiGauss的PSNR达到23.59 dB，较NeRF-W的19.63 dB提升3.96 dB（Table 3）；在Footbridge场景，LumiGauss的PSNR为20.89 dB，较NeRF-W的17.25 dB提升3.64 dB（Table 4）。这一系统性优势验证了核心洞察：**显式物理建模在光照鲁棒性方面具有根本性优势**。

### 3. 数据集设计的关键创新：隔离光照变量

UAVLight区别于现有数据集的核心设计在于**通过控制变量法隔离光照变化**：

| 设计维度 | 传统数据集 | UAVLight |
|---------|-----------|----------|
| 采集协议 | 单次短时间窗口采集，光照近似恒定 | 重复GPS轨迹在多个固定时间采集，产生自然光照变化且几何一致 |
| 位姿估计 | 纯SfM | 分组Bundle Adjustment加入RTK约束（公式 $E_{\mathrm{total}} = E_{\mathrm{group}} + \sum_{i} \kappa_{i} \| \mathbf{c}_{i} - \mathbf{t}_{\mathrm{RTK}_{i}} \|_{2}^{2}$） |
| 光照真值 | 无 | 由GPS/时间戳计算太阳方向（公式 $\mathbf{s}_{\mathrm{Colmap}} = \mathbf{R} \mathbf{s}_{\mathrm{ENU}}$） |

这一设计使得UAVLight能够**系统评估跨时间的光度一致性和重光照稳定性**，而非像传统数据集那样将光照变化与其他因素混杂。通过RTK定位和地面控制点验证，平均几何误差约10 cm（垂直误差10.31 cm，平面误差11.83 cm，Table 6），为评估提供了可靠的几何参考。

### 4. 适用边界与局限

#### 4.1 当前适用边界

UAVLight基准和评估结论的适用性受以下条件约束：

- **光照类型**：仅包含白天自然光照变化（太阳位置变化导致的直射光/阴影变化），不包含阴天漫射光、人工光源或极端逆光场景。
- **场景类型**：主要覆盖室外城市/基础设施场景（建筑、桥梁、道路等），采用低空天底视角。
- **动态性**：场景为静态，不包含行人、车辆等动态物体的外观变化。
- **大气条件**：未考虑云层遮挡、大气散射、雾霾等因素引起的光谱变化。

#### 4.2 已知局限

1. **照明多样性不足**：缺少阴天、季节变化、大气散射等更极端的照明条件，限制了评估的生态效度。

2. **视角偏向**：主要采用低空天底视角，天空区域可见性有限，可能简化了天空光照建模的难度，对某些需要完整天空表示的方法（如基于环境图的逆渲染）不公平。

3. **缺乏重光照真值**：虽然提供了太阳方向作为光照先验，但缺少真实的重光照地面真值（如HDR环境图或光谱辐射计测量），无法量化重光照的物理准确性。

4. **自动曝光影响**：无人机相机的自动曝光导致图像强度非线性变化，可能影响光度一致性评估的准确性——部分“外观变化”实际上源于曝光而非光照本身。

5. **高斯泼溅方法的主导性**：当前实验中高斯泼溅类方法（GS-W, WildGaussians, LumiGauss）在标准指标上整体优于NeRF类方法，这可能部分归因于高斯泼溅的渲染效率优势，而非纯粹的光照建模优势。

### 5. 开放问题与未来方向

#### 5.1 光照多样性的扩展

当前基准仅覆盖晴天条件下的太阳位置变化。未来扩展方向包括：
- **云层遮挡**：部分云层覆盖产生的动态阴影和漫射光变化
- **季节变化**：植被外观、太阳高度角的季节性漂移
- **大气条件**：雾霾、沙尘等大气散射效应

#### 5.2 成对真实-仿真版本

开发UAVLight的成对真实-仿真版本，通过物理渲染引擎生成具有精确光照真值的合成数据，可支持：
- 重光照准确性的定量评估
- 户外模拟与具身人工智能研究
- 域迁移（sim-to-real）方法的验证

#### 5.3 动态场景扩展

当前基准限于静态场景。引入受控的动态物体（如车辆、行人）可评估方法在光照-动态联合变化下的鲁棒性，这对实际应用（如城市监控、交通分析）至关重要。

#### 5.4 显式方法的进一步发展

虽然LumiGauss等显式方法在跨光照评估中表现优异，但其依赖于太阳-天空模型等强先验。如何在不依赖强先验的情况下实现物理上可解释的光照解耦，仍是一个开放问题。此外，显式方法在处理高频细节（如镜面反射、复杂材质）时可能不如隐式方法灵活，如何结合两者优势值得探索。

## 原文 PDF

![[paperPDFs/CVPR_2026/UAVLight_A_Benchmark_for_Illumination_Robust_3D_Reconstruction_in_Unmanned_Aerial_Vehicle_UAV_Scenes.pdf]]