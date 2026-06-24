---
title: "ViPE: Video Pose Engine for 3D Geometric Perception"
type: paper
paper_level: A
venue: Whitepaper
year: 2025
pdf_ref: paperPDFs/WHITEPAPER_2025/ViPE_Video_Pose_Engine_for_3D_Geometric_Perception.pdf
aliases:
- VVPE
- ViPE
tags:
- WHITEPAPER_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "在关键帧BA中联合优化相机内参、位姿和低分辨率深度图，并融合稠密光流约束、稀疏特征点约束和度量深度先验，同时通过语义掩膜去除动态物体，以及对多种相机模型的支持。"
primary_logic: "通过将学习型稠密匹配、度量深度先验和经典稀疏特征紧密结合到高效的关键帧BA框架中，辅以动态物体掩膜和多相机模型适配，实现了对无约束野外视频的鲁棒、度量级联合位姿与密集深度估计。"
claims:
- "ViPE在TUM和KITTI数据集上分别超过无标定基线18%和50%"
- "在TUM Freiburg1静态场景ATE为3.6 cm，动态场景为1.5 cm，内参误差为1.8°/0.6°，均优于DROID-SLAM、MASt3R-SLAM、VGGT、MegaSAM"
- "在KITTI上ATE为9.2 m，优于其他基线，且内参误差仅为1.9°"
- "消融实验表明，稀疏特征和动态掩膜提高鲁棒性，深度正则化和对齐进一步提度精度，全部组件组合取得最佳Sampson和S-ATE"
---

# ViPE: Video Pose Engine for 3D Geometric Perception

> [!tip] 核心洞察
> 通过将学习型稠密匹配、度量深度先验和经典稀疏特征紧密结合到高效的关键帧BA框架中，辅以动态物体掩膜和多相机模型适配，实现了对无约束野外视频的鲁棒、度量级联合位姿与密集深度估计。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | ViPE：面向3D几何感知的视频位姿引擎 |
| 英文题名 | ViPE: Video Pose Engine for 3D Geometric Perception |
| 会议/期刊 | Whitepaper 2025 |
| Links | [paper](https://arxiv.org/abs/2508.10934); [Project](https://research.nvidia.com/labs/toronto-ai/vipe/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | ViPE (Video Pose Engine) |
| Dataset | TUM RGB-D (Freiburg1 static), TUM RGB-D (Freiburg3 dynamic), KITTI Odometry |

> [!tip] 效果简介
> - TUM RGB-D (Freiburg1 static) 上，ATE (cm)↓ 为 3.6，对比 4.4 (DROID-SLAM†)，变化 -0.8。
> - TUM RGB-D (Freiburg3 dynamic) 上，ATE (cm)↓ 为 1.5，对比 2.7 (DROID-SLAM†)，变化 -1.2。
> - TUM RGB-D (Freiburg1 static) 上，Focal (°)↓ 为 1.8，对比 4.1 (DROID-SLAM†)，变化 -2.3。

## 概述

从一段随意拍摄的视频中同时恢复精确的相机运动与度量级密集深度，是3D视觉走向开放世界应用的核心瓶颈。现有方案陷入两难：纯前馈模型（如 **VGGT**，Wang et al., CVPR 2025）推理快但缺乏跨帧一致性，逐帧优化方法（如 **MegaSAM**，Li et al., CVPR 2025）精度尚可但效率低下，而混合SLAM系统（如 **DROID-SLAM**†，Teed and Deng, NeurIPS 2021；**MASt3R-SLAM**，Murai et al., CVPR 2025）在面对无标定、动态、任意长度的野外视频时，位姿估计的鲁棒性和尺度一致性仍严重不足。

**ViPE (Video Pose Engine)** 针对上述瓶颈提出了一条系统性解决路径。其核心洞察在于：将学习型稠密匹配、度量深度先验与经典稀疏特征紧密结合到一个高效的关键帧BA框架中，辅以动态物体语义掩膜和多相机模型适配，可以在不牺牲效率的前提下，实现对无约束野外视频的鲁棒、度量级联合位姿与密集深度估计。

具体而言，ViPE在关键帧BA中**联合优化相机内参、位姿和低分辨率深度图**，并融合三项互补约束——稠密光流重投影、稀疏角点跟踪和度量深度正则化——同时通过GroundingDINO + SAM + XMem提取可移动物体语义掩膜以消除动态干扰，以及对针孔、广角/鱼眼（统一相机模型）和360°全景的多相机支持。最终通过平滑深度对齐步骤，生成与位姿严格一致的全分辨率密集深度图。

实验证据充分支撑了上述设计。在TUM RGB-D数据集上，ViPE在静态和动态场景下分别取得3.6 cm和1.5 cm的ATE，内参估计误差仅1.8°/0.6°，全面优于DROID-SLAM†、MASt3R-SLAM、VGGT和MegaSAM等基线（Table 1）。在KITTI室外驾驶场景，ATE为9.2 m，相较MASt3R-SLAM的122.2 m提升超过一个数量级，且内参误差仅1.9°（Table 2）。消融实验证实，稀疏特征和动态掩膜显著提升了鲁棒性，深度正则化与对齐进一步提高了精度，全组件组合在Sampson误差和S-ATE指标上均达到最优（Table 4）。在广角与鱼眼相机上，采用统一相机模型校正畸变后的结果也明显优于简单针孔假设（Figure 3）。

ViPE以3–5 FPS的单GPU推理速度运行，虽未达实时要求，但已足够支撑大规模视频标注任务。其局限性主要在于依赖预训练网络（在分布外场景可能退化）、动态掩膜限于预定义语义类别、以及极端纹理缺失或纯旋转等退化运动下BA仍可能失效。尽管如此，ViPE作为视频位姿引擎，为从野外视频中提取可扩展的3D几何标注提供了当前最完整的解决方案。

## 背景与动机

从无约束的日常视频中恢复精确的三维几何与相机运动，是计算机视觉领域的一项基础性挑战。随着大规模视频数据在自动驾驶、机器人导航、增强现实和三维内容生成等应用中的爆发式增长，对高效、鲁棒的自动标注工具的需求日益迫切。理想的视频标注引擎应当能够从一段随意拍摄的视频中，同时输出度量级的相机位姿轨迹和与之尺度一致的密集深度图，而无需依赖标定板、已知场景结构或昂贵的传感器。

然而，现有的方法体系在应对这一目标时存在显著缺口。传统的同时定位与建图（SLAM）系统，如基于关键帧的稀疏特征法，虽然具有成熟的优化框架和一定的可扩展性，但在处理无标定、包含动态物体、且时长任意的野外视频时，其位姿估计的精度和鲁棒性往往急剧下降。另一方面，近年来涌现的纯前馈深度学习方法，如**VGGT**（Wang et al., CVPR 2025），通过端到端网络直接从视频回归几何信息，展现了对复杂场景的适应能力，但其输出缺乏全局一致性，且难以保证跨帧的度量尺度统一。混合方法试图弥合这一鸿沟：**DROID-SLAM**（Teed and Deng, NeurIPS 2021）将稠密光流融入经典BA框架，**MASt3R-SLAM**（Murai et al., CVPR 2025）则进一步引入学习型前端，但这些系统通常假设已知相机内参或仅支持针孔模型，在面对广角、鱼眼乃至360°全景等多样化相机时束手无策。此外，针对动态场景的视频标注工作如**MegaSAM**（Li et al., CVPR 2025），虽然能够处理运动物体，却依赖逐帧优化，效率低下，难以扩展至长视频。

上述方法的共同瓶颈在于：**缺乏一个统一的框架，能够将学习型组件的鲁棒感知能力与经典几何优化的全局一致性紧密结合，并系统地解决无标定、动态场景和多相机模型适配这三个相互耦合的难题。**具体而言，无标定意味着内参必须从视频中在线估计，而错误的初始内参会迅速导致位姿漂移和深度尺度畸变；动态物体若不加甄别地纳入优化，会引入大量外点，污染整个BA过程；而广角与鱼眼相机带来的强烈畸变，则要求投影模型本身具备足够的灵活性。

ViPE（Video Pose Engine）正是在这一背景下提出的。其核心动机并非设计一个全新的SLAM系统，而是构建一个**强大且通用的视频标注引擎**，直接面向“任意视频输入，度量级几何输出”这一实用目标。ViPE的设计哲学是：在高效的关键帧BA框架内，将稠密光流约束、稀疏特征点约束和度量深度先验进行联合优化，同时通过语义掩膜主动剔除动态区域，并对多种相机模型提供原生支持。这一思路使得系统既能继承SLAM框架在长序列上的可扩展性和精度，又能借助现代学习模型（如光流网络、度量深度估计网络）的鲁棒性，最终生成与位姿严格一致的密集深度图。与最接近的先前工作MegaSAM相比，ViPE无需逐帧优化，因而在效率上具有显著优势，运行速度可达3–5 FPS（单GPU）。

## 核心创新

ViPE 的核心创新在于将**学习型稠密匹配、度量深度先验与经典稀疏特征**紧密结合到一个高效的关键帧 BA 框架中，并辅以**动态物体掩膜**和**多相机模型适配**，从而首次实现了对无约束野外视频的鲁棒、度量级联合位姿与密集深度估计。其相对于现有基线的关键 changed slots 如下：

### 1. 内参联合优化与多相机模型支持

现有混合 SLAM 系统（如 **DROID-SLAM†**，Teed and Deng, NeurIPS 2021）通常需要已知内参或仅支持针孔模型，限制了其在任意来源视频上的适用性。ViPE 在关键帧 BA 中**联合优化相机内参**，并通过统一的径向投影公式支持多种相机模型：

$$\mathbf{u} = \Pi_k([x,y,z]^\top) = [f \cdot q_k(\theta) \cdot \cos\phi + W/2,\; f \cdot q_k(\theta) \cdot \sin\phi + H/2]^\top$$

其中 $q_k(\theta)$ 根据相机类型选择不同映射函数：针孔模型使用 $\tan\theta$，广角/鱼眼相机采用统一相机模型，360° 全景则通过多相机投影实现（§ 3.2.5; Eq (5); Figure 3）。实验表明，统一相机模型对广角视频的畸变校正效果显著优于简单针孔假设（Figure 3）。

### 2. 动态物体掩膜去除干扰

现有方法（如 **MegaSAM**，Li et al., CVPR 2025）或假设静态场景，或需逐帧优化处理动态物体，效率较低。ViPE 采用 **GroundingDINO + SAM + XMem** 流水线提取可移动物体的语义掩膜（§ 3.2.4；Figure 2），在 BA 优化前将动态区域从稠密光流约束的权重中剔除，从而消除其对位姿估计的干扰。消融实验证实，加入动态掩膜后 Sampson 误差和 S-ATE 等鲁棒性指标显著改善（Table 4）。

### 3. 稀疏特征约束增强高频细节

纯依赖低分辨率稠密光流（如 DROID-SLAM 的原始设计）在纹理丰富区域可能丢失高频几何信息。ViPE 引入了基于 **cuVSLAM** 的稀疏角点跟踪项，通过双线性 splatting 优化稀疏重投影误差：

$$e_{\mathrm{sparse}}(\mathbf{T}_i,\mathbf{T}_j,\mathbf{D}_i,k) = \sum_{\mathbf{p}_i} \| \Pi_k(\mathbf{T}_j^{-1}\mathbf{T}_i \circ \Pi_k^{-1}(\mathrm{Bilerp}(\mathbf{D}_i,\mathbf{p}_i))) - \mathbf{p}_j \|^2$$

该约束为 BA 提供了亚像素精度的互补信息（§ 3.2.2; Eq (3)），消融实验显示其与稠密约束的协同作用显著提升了位姿估计的鲁棒性（Table 4）。

### 4. 度量深度先验缓解尺度漂移

无标定单目 SLAM 的固有尺度模糊性在长视频中会累积为严重的尺度漂移。ViPE 引入度量深度估计网络（Metric3Dv2/UniDepthV2/UniK3D）的预测作为正则化先验：

$$e_{\mathrm{depth}}(\mathbf{D}_i) = \sum_{\mathbf{u}} m[\mathbf{u}] \cdot \| \mathbf{D}_i[\mathbf{u}] - \mathbf{D}_i^{\mathrm{prior}}[\mathbf{u}] \|^2$$

该先验随内参更新而自适应调整权重 $m$（§ 3.2.3; Eq (4)），使 ViPE 在 KITTI 等大尺度场景中输出接近真实尺度的位姿（ATE 9.2 m，显著优于 MASt3R-SLAM 的 122.2 m），且内参误差仅为 1.9°（Table 2）。

### 5. 平滑深度对齐生成全分辨率密集深度

现有方法或仅输出稀疏/低分辨率深度，或逐帧预测缺乏尺度一致性。ViPE 通过**平滑深度对齐**（§ 3.3; Eq (6)）融合视频深度估计（VDA）和 BA 稀疏深度，利用动量仿射变换逐帧对齐反深度尺度：

$$\alpha_i,\beta_i = \arg\min_{\alpha,\beta} \sum_{\mathbf{u}\;\mathrm{valid}} \| \mathbf{M} \cdot (\alpha/\mathbf{D}_i^{\mathrm{VDA}} + \beta - 1/\mathbf{D}_i^{\mathrm{BA}}) \|_2^2$$

辅以动量平滑 $\hat{\alpha}_i = m \cdot \hat{\alpha}_{i-1} + (1-m) \cdot \alpha_i$，最终输出与位姿一致的**全分辨率、度量尺度密集深度图**（Figure 2）。在 SINTEL 上达到 RelAbs 0.21、$\delta_{1.25}$ 80.8% 的深度精度（Table 3）。

**因果机制总结**：上述五个 changed slots 并非孤立改进，而是通过统一的 BA 能量函数 $\epsilon_{\mathrm{ViPE}}$（Eq (1)）形成协同效应——稠密流提供全局几何约束，稀疏点增强局部细节，深度先验锚定绝对尺度，动态掩膜排除离群干扰，多相机模型扩展适用边界，最终在 TUM 静态/动态场景（ATE 3.6/1.5 cm）和 KITTI（ATE 9.2 m）上均显著超越无标定基线（18%/50% 提升），并首次实现了面向任意野外视频的端到端度量级位姿与密集深度联合估计。

## 整体框架

![[assets/figures/papers/paper_list_l21_https_arxiv_org_abs_2508_10934/figures/002_Figure_2.jpg]]
*Figure 2: Pipeline of ViPE. The system takes a video as input and first estimates the semantic segmentation masks of the movable objects. It then estimates the camera poses, intrinsics, and depth maps from the video by solving a dense bundle adjustment problem incorporating various constraints. The final output is a dense depth map that is consistent with the camera poses and the intrinsics after the smooth depth alignment step*

ViPE 的整体流程如图 2 所示，系统以一段任意长度、无标定的野外视频为输入，依次完成可移动物体语义掩膜提取、关键帧位姿与内参联合优化、以及全分辨率密集深度图生成三个核心阶段，最终输出度量尺度的相机轨迹与逐帧密集深度图。

**输入与预处理。** 视频输入后，系统首先调用 GroundingDINO + SAM + XMem 的组合管线，提取潜在可移动物体（如行人、车辆）的语义分割掩膜。该掩膜将在后续 BA 优化中用于屏蔽动态区域，避免其对位姿估计的干扰。

**核心优化：关键帧 BA。** ViPE 的位姿与内参估计建立在类似 DROID-SLAM 的关键帧 SLAM 框架之上，但其 BA 能量函数被显著扩展，联合优化相机内参 $k$、各关键帧位姿 $\mathbf{T}_i$ 和低分辨率深度图 $\mathbf{D}_i$。总能量函数为：

$$\epsilon_{\mathrm{ViPE}} = \sum_{(i,j)\in\mathcal{E}} e_{\mathrm{dense}} + \sum_{(i,j)\in\mathcal{E}} e_{\mathrm{sparse}} + \alpha \sum_{i\in\mathcal{V}} e_{\mathrm{depth}}$$

其中三项约束分别来自：
1. **稠密光流约束** $e_{\mathrm{dense}}$：利用学习型稠密光流网络（基于 RAFT 架构，内部构建代价体并迭代精化）预测帧间光流 $\mathbf{F}_{ij}$，以重投影误差形式约束位姿与深度，权重 $w[\mathbf{u}]$ 融合了光流置信度与动态掩膜。
2. **稀疏特征点约束** $e_{\mathrm{sparse}}$：通过 cuVSLAM 的 Shi-Tomasi 角点检测与 Lucas-Kanade 跟踪获取亚像素精度匹配点对，提供对高频纹理细节的补充约束，实践中以双线性 splatting 替代插值以避免半稀疏 Hessian 结构。
3. **度量深度正则化** $e_{\mathrm{depth}}$：引入 Metric3Dv2 / UniDepthV2 / UniK3D 等度量深度估计网络的预测作为先验 $\mathbf{D}_i^{\mathrm{prior}}$，以不确定性 $m[\mathbf{u}]$ 加权，缓解长序列的尺度漂移。

**多相机模型支持。** ViPE 采用统一的径向投影函数 $\Pi_k$ 处理多种相机模型：对于针孔相机，$q_k(\theta)=\tan\theta$；对于广角/鱼眼相机，使用统一相机模型 $q_k(\theta)=\frac{\tan\theta}{1+\alpha\sqrt{\tan^2\theta+1}}$。内参 $k$ 在全局 BA 阶段解锁优化，初始值由 GeoCalib 在 4 帧均匀采样帧上估计。对于 360° 全景视频，系统先将其投影到 6 个针孔面，再通过多相机外参 $\mathbf{T}_v$ 扩展 BA 公式。

**关键帧选择与位姿填充。** 系统基于加权光流与稀疏点跟踪的综合运动量判断是否添加新关键帧。前端在滑动窗口内执行局部 BA，后端在关键帧数达到阈值时触发全局 BA。非关键帧的位姿通过相邻关键帧的单向边进行填充。

**密集深度生成。** BA 输出的深度图为低分辨率稀疏深度。为获得全分辨率、尺度一致的密集深度图，ViPE 引入平滑深度对齐阶段：首先调用视频深度估计网络（VDA）获得逐帧逆深度 $\mathbf{D}_i^{\mathrm{VDA}}$，然后通过动量仿射变换将其对齐到 BA 稀疏深度 $\mathbf{D}_i^{\mathrm{BA}}$：

$$\alpha_i,\beta_i = \arg\min_{\alpha,\beta} \sum_{\mathbf{u}\;\mathrm{valid}} \| \mathbf{M} \cdot (\alpha/\mathbf{D}_i^{\mathrm{VDA}} + \beta - 1/\mathbf{D}_i^{\mathrm{BA}}) \|_2^2$$

仿射参数以动量 $m$ 在时域上平滑更新，最终生成全分辨率、与位姿和内参一致的度量深度图。

**运行效率。** ViPE 在单 GPU 上以 3–5 FPS 运行（标准输入分辨率），无需逐帧优化，相比 MegaSAM 等基线具有显著的效率优势。

## 核心模块与公式推导

ViPE 的核心是一个基于关键帧的稠密 BA（Bundle Adjustment）系统，其设计继承自 **DROID-SLAM**（Teed and Deng, NeurIPS 2021）。系统将学习型稠密匹配、度量深度先验与经典稀疏特征统一到同一优化框架中，并辅以动态物体掩膜和多相机模型支持，从而实现对无约束野外视频的鲁棒联合位姿与深度估计。

### 关键帧 BA 总能量函数

系统的核心优化目标是最小化如下总能量函数（Eq (1)）：

$$\epsilon_{\mathrm{ViPE}}(\{\mathbf{T}_i\},\{\mathbf{D}_i\},k) = \sum_{(i,j)\in\mathcal{E}} e_{\mathrm{dense}}(\mathbf{T}_i,\mathbf{T}_j,\mathbf{D}_i,k) + \sum_{(i,j)\in\mathcal{E}} e_{\mathrm{sparse}}(\mathbf{T}_i,\mathbf{T}_j,\mathbf{D}_i,k) + \alpha \sum_{i\in\mathcal{V}} e_{\mathrm{depth}}(\mathbf{D}_i)$$

其中 $\{\mathbf{T}_i\}$ 为关键帧位姿集合，$\{\mathbf{D}_i\}$ 为关键帧逆深度图集合，$k$ 为相机内参参数。该能量函数由三项构成：稠密光流约束 $e_{\mathrm{dense}}$、稀疏特征点约束 $e_{\mathrm{sparse}}$ 和深度正则化项 $e_{\mathrm{depth}}$，超参数 $\alpha$ 控制深度先验的权重。

### 稠密光流约束

稠密光流约束（Eq (2)）基于预训练的稠密光流网络，对关键帧对 $(i,j)$ 施加像素级重投影误差：

$$e_{\mathrm{dense}}(\mathbf{T}_i,\mathbf{T}_j,\mathbf{D}_i,k) = \sum_{\mathbf{u}} w[\mathbf{u}] \cdot \| \Pi_k(\mathbf{T}_j^{-1}\mathbf{T}_i \circ \Pi_k^{-1}(\mathbf{D}_i[\mathbf{u}])) - \mathbf{u} - \mathbf{F}_{ij}[\mathbf{u}] \|^2$$

其中 $\mathbf{F}_{ij}$ 为光流网络预测的稠密流场，$\Pi_k$ 和 $\Pi_k^{-1}$ 分别为相机投影与反投影函数，$\mathbf{u}$ 为像素坐标。权重 $w[\mathbf{u}]$ 融合了光流置信度与动态物体掩膜：对于被语义分割网络（GroundingDINO + SAM + XMem）识别为可移动物体的像素，其权重置为零，从而在优化中排除动态区域对位姿估计的干扰。

光流网络内部构建代价体并通过迭代精化模块输出流场，同时提供先验流作为初始引导，使优化过程更稳定。

### 稀疏特征点约束

为弥补稠密光流在低分辨率网格上对高频细节约束不足的问题，ViPE 引入基于 cuVSLAM 的稀疏角点跟踪项（Eq (3)）。该模块使用 Shi-Tomasi 角点检测与 Lucas-Kanade 光流跟踪，提供亚像素精度的稀疏匹配：

$$e_{\mathrm{sparse}}(\mathbf{T}_i,\mathbf{T}_j,\mathbf{D}_i,k) = \sum_{\mathbf{p}_i} \| \Pi_k(\mathbf{T}_j^{-1}\mathbf{T}_i \circ \Pi_k^{-1}(\mathrm{Bilerp}(\mathbf{D}_i,\mathbf{p}_i))) - \mathbf{p}_j \|^2$$

其中 $\mathbf{p}_i$ 和 $\mathbf{p}_j$ 为一对匹配的稀疏特征点。实践中，为避免双线性插值导致的半稀疏 Hessian 模式（影响求解器效率），ViPE 采用双线性 splatting 替代插值操作，将稀疏点的深度残差“泼溅”到邻域像素上，从而保持与稠密项一致的 Hessian 结构。

### 深度正则化先验

纯视觉 BA 存在严重的尺度漂移问题。ViPE 通过引入度量深度估计网络的预测作为正则化先验来缓解这一问题（Eq (4)）：

$$e_{\mathrm{depth}}(\mathbf{D}_i) = \sum_{\mathbf{u}} m[\mathbf{u}] \cdot \| \mathbf{D}_i[\mathbf{u}] - \mathbf{D}_i^{\mathrm{prior}}[\mathbf{u}] \|^2$$

其中 $\mathbf{D}_i^{\mathrm{prior}}$ 来自 Metric3Dv2、UniDepthV2 或 UniK3D 等度量深度网络，权重 $m[\mathbf{u}]$ 为深度网络输出的逐像素不确定性估计。该先验随内参优化过程动态调整：当内参更新时，深度先验的尺度也会相应校正，从而在全局 BA 中保持尺度一致性。

对于极端情况（如纯旋转或纹理缺失），BA 深度可能完全不可靠，此时系统直接使用度量深度网络的输出作为 $\mathbf{D}_i^{\mathrm{BA}}$，并借助 PriorDA 在部分观测和输入图像的条件下补全深度图。

### 多相机模型支持

ViPE 通过统一的径向投影函数支持多种相机模型（Eq (5)）：

$$\mathbf{u} = \Pi_k([x,y,z]^\top) = [f \cdot q_k(\theta) \cdot \cos\phi + W/2,\; f \cdot q_k(\theta) \cdot \sin\phi + H/2]^\top$$

其中 $\theta = \arccos(z/\sqrt{x^2+y^2+z^2})$ 为入射角，$\phi = \arctan2(y,x)$ 为方位角，$f$ 为焦距。径向函数 $q_k(\theta)$ 根据相机类型选择：针孔模型下 $q_k(\theta) = \tan\theta$；广角/鱼眼相机采用统一相机模型 $q_k(\theta) = \tan\theta / (1 + \alpha\sqrt{\tan^2\theta + 1})$，其中 $\alpha$ 为畸变参数。对于 360° 全景视频，系统先将球面投影到 6 个针孔面，再通过多相机投影扩展变换 $\mathbf{T}_i \to \mathbf{T}_v\mathbf{T}_i$ 实现统一优化。

### 平滑深度对齐

BA 输出的深度图是稀疏或低分辨率的。为生成全分辨率、尺度一致的密集深度图，ViPE 在 § 3.3 中设计了平滑深度对齐模块。该模块对每帧求解一个仿射变换，将视频深度估计网络（VDA）的输出对齐到 BA 逆深度空间（Eq (6)）：

$$\alpha_i,\beta_i = \arg\min_{\alpha,\beta} \sum_{\mathbf{u}\;\mathrm{valid}} \| \mathbf{M} \cdot (\alpha/\mathbf{D}_i^{\mathrm{VDA}} + \beta - 1/\mathbf{D}_i^{\mathrm{BA}}) \|_2^2$$

其中 $\mathbf{M}$ 为有效像素掩膜。为抑制帧间抖动，仿射参数通过动量更新平滑：

$$\hat{\alpha}_i = m \cdot \hat{\alpha}_{i-1} + (1-m) \cdot \alpha_i, \quad \hat{\beta}_i = m \cdot \hat{\beta}_{i-1} + (1-m) \cdot \beta_i$$

其中动量因子 $m$ 控制时序平滑强度。最终密集深度图由 $\hat{\alpha}_i/\mathbf{D}_i^{\mathrm{VDA}} + \hat{\beta}_i$ 取倒数得到，既保留了视频深度网络的高分辨率细节，又与 BA 优化的全局几何保持一致。

## 实验与分析

### 核心性能验证

ViPE 在室内外标准数据集上进行了系统评估，与当前最先进的无标定位姿估计方法进行全面对比。实验结果表明，ViPE 在精度、鲁棒性和尺度一致性方面均展现出显著优势。

**室内场景（TUM RGB-D）**：如表 1 所示，ViPE 在 Freiburg1 静态场景下取得 3.6 cm 的绝对轨迹误差（ATE），相比最强基线 DROID-SLAM†（4.4 cm）降低 18%；在 Freiburg3 动态场景下 ATE 仅为 1.5 cm，显著优于 DROID-SLAM† 的 2.7 cm。值得注意的是，ViPE 在无标定条件下联合优化内参的能力使其焦距估计误差仅为 1.8°（静态）和 0.6°（动态），远低于依赖外部标定的 DROID-SLAM†（4.1° 和 1.5°）。纯前馈模型 VGGT 在 TUM 上表现较差（ATE 11.2 cm），因其缺乏 BA 框架的全局一致性约束。

![[assets/figures/papers/paper_list_l21_https_arxiv_org_abs_2508_10934/figures/005_Table_1.jpg]]
*Table 1: Pose and intrinsics accuracy measured on TUM-RGBD [62] dataset. Table 2: Pose and intrinsics accuracy measured on outdoor driving datasets*

**室外驾驶场景（KITTI / RDS）**：在长距离室外场景中，ViPE 的优势更为突出。如表 2 所示，KITTI 上 ViPE 的 ATE 为 9.2 m，而 MASt3R-SLAM 高达 122.2 m，DROID-SLAM† 为 31.3 m，VGGT 为 49.5 m。RDS 数据集上 ViPE 的 ATE 为 5.0 m，同样大幅领先。图 4 的定性结果表明，ViPE 输出的轨迹与真实世界尺度高度一致，而基线方法存在明显的尺度漂移问题。这一优势源于度量深度先验的有效整合。

![[assets/figures/papers/paper_list_l21_https_arxiv_org_abs_2508_10934/figures/006_Figure_4.jpg]]
*Figure 4: Qualitative results of camera pose estimation on KITTI dataset [23]. Output of ViPE can be used as an approximation of the metric scale in real world, while the baseline [37] is not guaranteed to be scale-consistent*

**无真值视频评估**：针对缺乏位姿真值的野外视频，论文采用 Sampson 误差和自洽性指标（S-ATE、S-RTE、S-RRE、S-Focal）进行评估。如图 5 所示，ViPE 在所有自洽性指标上均优于基线方法，表明其在无约束场景下的鲁棒性。

![[assets/figures/papers/paper_list_l21_https_arxiv_org_abs_2508_10934/figures/009_Figure_5.jpg]]
*Figure 5: Qualitative results of camera pose estimation on unposed videos using the proposed metrics. Table 3: Depth estimation accuracy measured on synthetic and real-world indoor datasets*

### 消融实验

表 4 的消融实验系统验证了各组件的贡献：

![[assets/figures/papers/paper_list_l21_https_arxiv_org_abs_2508_10934/figures/011_Figure_6.jpg]]
*Figure 6: Qualitative comparisons of the method output with the baselines on the SINTEL dataset. We subsample the camera frames for clarity only in the visualization. Table 4: Ablation study on the effectiveness of different components in ViPE*

- **稀疏特征约束**：去除稀疏跟踪项后，Sampson 误差从 0.83 上升至 1.12，S-ATE 从 3.80 恶化至 5.20，表明稀疏角点对高频几何细节的约束不可替代。
- **动态物体掩膜**：移除语义掩膜后，Sampson 误差升至 1.05，S-ATE 升至 4.80，说明动态区域去除对位姿鲁棒性至关重要。
- **深度正则化**：去除深度先验后，S-Focal 从 4.26 恶化至 6.80，表明度量深度对尺度一致性和内参优化的支撑作用。
- **全配置**：组合所有模块后，所有指标均达到最优（Sampson 0.83，S-ATE 3.80，S-RRE 0.03°），验证了各组件间的协同效应。

### 深度估计评估

表 3 展示了 ViPE 在 SINTEL（合成）和 ETH3D（真实室内）上的深度估计精度。ViPE 结合视频深度对齐（VDA）与 BA 稀疏深度的策略，在 RelAbs、LogRMSE 和 δ1.25 等指标上均优于纯视频深度估计基线。SINTEL 上 RelAbs 为 0.21，ETH3D 上为 0.16，表明生成的密集深度图兼具全分辨率与尺度一致性。

### 广角与鱼眼相机支持

图 3 展示了 ViPE 对广角相机的适配能力。基线方法采用针孔假设时，位姿估计出现明显偏差；ViPE 通过统一相机模型（Eq (5)）联合优化径向畸变参数，成功恢复了准确的相机轨迹，并输出了校正后的无畸变图像。这验证了内参联合优化的有效性。

![[assets/figures/papers/paper_list_l21_https_arxiv_org_abs_2508_10934/figures/003_Figure_3.jpg]]
*Figure 3: Pose estimation results on wide-angle cameras. (a) Baseline results with the pinhole camera assumption. (b) ViPE’s results using the unified camera model. (c) Sample frames from the video. (d) Rectified frames using ViPE’s intrinsics estimation*

### 关键图表结论

- **Table 1 / Table 2**：ViPE 在室内外场景的位姿和内参精度均全面超越无标定基线，在 KITTI 上提升幅度超过 50%。
- **Table 4**：稀疏特征和动态掩膜提升鲁棒性，深度正则化提升精度，全配置达到最优。
- **Figure 4**：ViPE 输出度量级尺度轨迹，基线方法尺度不一致。
- **Figure 3**：统一相机模型有效处理广角畸变，针孔假设导致失败。

### 失败模式与局限性

尽管整体性能优异，ViPE 在以下场景存在退化风险：

1. **分布外场景**：依赖预训练的单目深度和光流网络，在特殊光照、水下等场景可能出现精度下降。
2. **非预定义动态物体**：动态掩膜基于语义类别，无法处理非预定义类别的可移动物体或非刚性变形。
3. **极端退化运动**：在纹理缺失或纯旋转等情况下，BA 框架仍可能陷入局部极小。
4. **360° 全景视频**：需预先投影至 6 个针孔面，可能引入投影畸变或信息损失。
5. **实时性不足**：当前速度约 3-5 FPS，尚不能支持 >30 FPS 的实时应用需求。

### 补充图表

![[assets/figures/papers/paper_list_l21_https_arxiv_org_abs_2508_10934/figures/007_Figure.jpg]]

![[assets/figures/papers/paper_list_l21_https_arxiv_org_abs_2508_10934/figures/004_Table.jpg]]

## 方法谱系与知识库定位

### 与关键帧稠密SLAM基线的关系

ViPE的架构骨架继承自**DROID-SLAM**（Teed and Deng, NeurIPS 2021）的关键帧稠密BA范式，但在此基础上进行了系统性改造。DROID-SLAM假定内参已知且场景静态，ViPE则通过三个核心扩展突破了这些限制：其一，在BA中联合优化相机内参，使系统能够处理无标定视频（内参由**GeoCalib**在4个采样帧上初始化）；其二，引入基于语义分割的动态物体掩膜（GroundingDINO + SAM + XMem），将可移动物体从位姿估计中剔除；其三，增加稀疏角点跟踪项（基于cuVSLAM的Shi-Tomasi角点与Lucas-Kanade跟踪），弥补纯稠密光流在纹理丰富区域对高频细节约束不足的问题。

与**MASt3R-SLAM**（Murai et al., CVPR 2025）这类以学习型前端为核心的混合方法相比，ViPE保持了经典BA的优化框架，但将学习组件（稠密光流网络、度量深度先验）作为约束项嵌入能量函数，而非完全替代几何优化。这种设计使得ViPE在无标定模式下仍能维持全局几何一致性，而MASt3R-SLAM在KITTI上出现严重尺度漂移（ATE 122.2 m vs. ViPE 9.2 m，Table 2）。

### 与纯前馈方法的边界

**VGGT**（Wang et al., CVPR 2025）代表了纯前馈位姿估计的路线——单次推理输出所有帧的位姿，无需迭代优化。这种方法的优势在于速度，但难以保证长视频的全局一致性。为公平比较，ViPE作者为VGGT设计了滑动窗口策略（窗口120–200帧，重叠5帧）并基于点云Sim(3)对齐，以适配长序列。即便如此，VGGT在TUM Freiburg1静态场景的ATE为10.7 cm，而ViPE为3.6 cm（Table 1），表明BA框架的迭代精化在精度上具有本质优势。ViPE的适用边界恰好位于此：当视频长度适中（数百至数千帧）且对精度要求高时，BA框架更优；当速度优先且可接受粗粒度位姿时，前馈方法更合适。

### 与逐帧优化标注方法的关系

**MegaSAM**（Li et al., CVPR 2025）是动态场景视频标注的近期工作，采用逐帧优化的策略。ViPE与之最接近，但通过关键帧BA实现了更高的效率——不需要对每一帧进行独立优化。这是ViPE作为“标注引擎”的核心定位：在保证与逐帧优化方法可比标注质量的前提下，将计算成本分摊到关键帧上，非关键帧的位姿通过相邻关键帧的单向边进行填充。

### 深度估计谱系中的定位

ViPE的密集深度生成模块处于“视频深度估计”与“BA稀疏深度”的交汇点。它利用视频深度网络（VDA）提供全分辨率、时序平滑的深度预测，再通过动量仿射变换将其对齐到BA输出的度量稀疏深度上（Eq (6)）。这种设计避免了纯视频深度估计的尺度不一致问题，也克服了BA深度在无纹理区域的稀疏性。在SINTEL和ETH3D上，ViPE的深度估计达到RelAbs 0.21/0.16，LogRMSE 0.27/0.22（Table 3），与专门的深度估计方法可比，但额外保证了与位姿的几何一致性。

### 适用边界与局限

ViPE的有效性依赖于其各组件的预训练模型质量，这构成了其首要适用边界：

1. **分布外退化**：稠密光流网络和度量深度网络（Metric3Dv2/UniDepthV2/UniK3D）在特殊光照、水下等分布外场景可能出现退化，导致BA约束质量下降。消融实验（Table 4）表明，去除深度正则化后Sampson误差从0.83升至1.05，说明深度先验对精度有实质贡献，但也意味着系统对该模块的依赖性较强。

2. **动态物体处理的语义依赖**：动态掩膜基于GroundingDINO的语义检测，只能处理预定义类别的可移动物体（如车辆、行人）。对于非预定义类别的可移动物体或非刚性变形（如衣物飘动、水面波纹），系统缺乏有效的处理机制。

3. **计算效率边界**：当前速度约3–5 FPS，尚不能支持实时（>30 FPS）应用。这限制了其在需要在线反馈的场景（如AR/VR、机器人导航）中的直接部署。

4. **极端几何退化**：在极端纹理缺失或纯旋转等退化运动下，BA仍可能陷入局部极小。稀疏特征和深度先验可以缓解但不能完全解决此问题。

5. **360°全景的投影损失**：全景视频需预先投影到6个针孔面，可能引入投影畸变或边界不连续，影响BA约束的质量。

### 开放问题

从当前工作出发，若干方向值得探索：

- **多模态融合**：如何将IMU等惯性测量单元整合进BA框架，以在视觉退化场景提供额外的运动先验？
- **动态物体运动建模**：能否将动态物体的运动直接作为优化变量，而非简单剔除？这将使系统能够同时输出静态背景和动态前景的位姿。
- **移动端部署**：能否通过模型蒸馏或量化，将稠密光流和深度网络压缩到移动端可运行的规模，同时保持BA的精度优势？
- **超长视频的全局一致性**：在超过万帧的视频上，当前的关键帧BA策略可能因误差累积而失去全局一致性。如何设计分层或分块的全局优化策略是一个开放挑战。
- **自适应语义类别**：如何自动确定需要掩膜的语义类别列表，以适应任意视频内容，而非依赖固定的预定义类别集合？

## 原文 PDF

![[paperPDFs/WHITEPAPER_2025/ViPE_Video_Pose_Engine_for_3D_Geometric_Perception.pdf]]
