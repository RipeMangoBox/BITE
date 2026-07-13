---
title: Learning Explicit Continuous Motion Representation for Dynamic Gaussian Splatting from Monocular Videos
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Learning_Explicit_Continuous_Motion_Representation_for_Dynamic_Gaussian_Splatting_from_Monocular_Videos.pdf
project_link: null
code_link: "https://github.com/hhhddddddd/se3bsplinegs"
aliases:
- SB
- LECMRDGSFMV
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/representation_self_supervised_transfer
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 采用SE(3)累积B样条运动基显式建模动态高斯的连续位置与朝向轨迹，并通过自适应修剪与稠密化机制动态调整基与控制点数量，以在计算效率与表达能力间取得平衡；辅以软分段重建策略减少长时间运动干扰，以及多视图扩散先验缓解过拟合。
primary_logic: 通过数学上连续的SE(3) B样条统一表示动态高斯的位姿变形，使变形轨迹在任意时刻保持平滑；自适应地根据局部运动复杂度调整运动基密度，从而显著提升单目视频新视图合成的质量与泛化能力。
claims:
- 在iPhone和NVIDIA数据集上，本方法在mPSNR/mSSIM/mLPIPS等指标上均大幅领先先前SOTA方法（Table 1），证明显式连续运动表示的有效性。
- 消融实验表明，移除自适应控制、软分段重建或SDS先验均导致性能明显下降，验证各组件的必要性（Table 2）。
- 替换运动表示为SoM的SE(3)姿态变换或MoSca的运动支架后，mPSNR分别降至18.17和19.26，远低于Ours的20.17，证实SE(3) B样条连续建模的贡献（Table 3）。
- iPhone 上 mPSNR / mSSIM / mLPIPS = 20.17 / 0.729 / 0.274
---

# Learning Explicit Continuous Motion Representation for Dynamic Gaussian Splatting from Monocular Videos

> [!tip] 核心洞察
> 通过数学上连续的SE(3) B样条统一表示动态高斯的位姿变形，使变形轨迹在任意时刻保持平滑；自适应地根据局部运动复杂度调整运动基密度，从而显著提升单目视频新视图合成的质量与泛化能力。

| 字段 | 内容 |
|------|------|
| 中文题名 | 从单目视频中学习显式连续运动表示以实现动态高斯泼溅 |
| 英文题名 | Learning Explicit Continuous Motion Representation for Dynamic Gaussian Splatting from Monocular Videos |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.25058) · [Code](https://github.com/hhhddddddd/se3bsplinegs) |
| Topic | #topic/vision_multimodal_applications #topic/representation_self_supervised_transfer #topic/vision_multimodal_applications/image_and_video_generation |
| Method | SE3-BSplineGS |
| Dataset | iPhone, NVIDIA |

> [!tip] 效果简介
> - iPhone 上，mPSNR / mSSIM / mLPIPS 20.17 / 0.729 / 0.274 vs SoM, MoSca, SplineGS, MarbleGS, HiMoR, MoDec-GS (所有对比方法均低于本方法) (最佳 (准确差值未解析))。
> - NVIDIA 上，PSNR / SSIM / LPIPS 27.81 / 0.871 / 0.049 vs 所有对比方法 (均低于本方法) (最佳 (准确差值未解析))。

## 概要

单目视频动态场景的新视图合成是计算机视觉与图形学中的核心挑战。现有基于3D高斯泼溅（3DGS）的动态方法通常将运动建模为逐时间戳的仿射变换，或仅对位置轨迹施加连续性约束，**未能显式建模动态高斯的位置与朝向在连续时间上的平滑变形轨迹**，导致在复杂运动区域出现非连续朝向变化和长期运动干扰，产生严重伪影。此外，固定数量的运动基无法适应局部运动复杂度的差异，进一步加剧了表达能力的不足。

针对上述瓶颈，本文提出 **SE3-BSplineGS**，核心思路是**通过数学上连续的SE(3)累积B样条统一表示动态高斯的位姿变形**，使变形轨迹在任意时刻保持平滑；同时**自适应地根据局部运动复杂度调整运动基与控制点数量**，在计算效率与表达能力之间取得平衡。具体而言，方法引入以下关键设计：

- **SE(3) B样条运动基**：从3D tracklets构建累积B样条，同时建模位置与朝向的连续变形轨迹，解决了仅建模位置连续而忽略朝向连续所带来的朝向伪影问题。
- **自适应控制机制**：根据轨迹拟合误差和渲染误差动态修剪或稠密化控制点，在复杂运动区域增加运动基密度，在简单区域减少冗余。
- **软分段重建**：根据参考时间戳与观测时间戳的间隔调整高斯不透明度，抑制长时间运动带来的干扰。
- **多视图扩散先验**：利用Zero123-xl-diffusers多视图扩散模型施加SDS损失，为训练视图中不可见区域提供多视图线索，缓解单目过拟合。

在iPhone和NVIDIA两个动态场景数据集上，SE3-BSplineGS在mPSNR、mSSIM、mLPIPS等指标上均大幅领先先前SOTA方法（Table 1）。消融实验证实，SE(3) B样条运动基相较于SoM的SE(3)姿态变换（mPSNR 18.17）和MoSca的运动支架（mPSNR 19.26）有显著提升（Table 3），而移除自适应控制、软分段重建或SDS先验均导致性能明显下降（Table 2），验证了各组件的必要性。方法同时展示了良好的跨场景泛化能力，但在大非刚性运动场景下仍存在失效风险（Figure 7）。



### 动态场景新视图合成的挑战

从单目视频中重建动态场景并合成高质量新视图，是计算机视觉与图形学中长期存在的核心难题。与静态场景不同，动态场景中的物体随时间发生位置和朝向变化，要求表示方法不仅能够捕获瞬时的几何与外观，还必须精确建模高斯的连续运动轨迹。近年来，3D Gaussian Splatting（3DGS）凭借其显式表示和实时渲染能力，在静态场景重建中取得了突破性进展。然而，将其扩展至动态场景时，如何为每个动态高斯赋予时间维度上的连续变形，成为一个关键瓶颈。

### 现有方法的缺口

当前单目动态高斯泼溅方法在运动建模上存在两个根本性不足：

**其一，缺乏连续的位置与朝向变形建模。** 多数方法采用逐时间戳的仿射变换或仅对位置进行连续建模（如 **SplineGS** 使用三次Hermite样条仅建模位置轨迹），忽略了朝向的平滑演化。这导致在复杂运动区域（如旋转的风车叶片）出现非连续的朝向跳变，渲染结果产生明显的撕裂与伪影。**Shape-of-Motion (SoM)** 虽引入了SE(3)运动基的线性组合，但其运动表示本质上是离散姿态的插值，缺乏严格的连续性保证。**MoSca** 依赖4D运动支架，同样无法确保朝向变形的平滑性。

**其二，运动基密度缺乏自适应控制。** 现有方法通常使用固定数量的运动基或控制点来描述整个动态场景。然而，不同空间区域的运动复杂度差异显著——静态背景区域几乎不需要运动基，而快速变形的局部区域则需要更密集的控制点来精确拟合轨迹。固定密度的设计要么在简单区域造成计算冗余，要么在复杂区域因表达能力不足而产生欠拟合。

这些缺陷在单目设定下被进一步放大：由于仅有一个训练视角，网络极易过拟合到训练视图，对不可见区域的新视图合成质量急剧下降。长时间运动序列中，某一时刻的高斯可能对远距离时间戳的渲染产生干扰，进一步加剧了伪影问题。

### 本文动机与核心思路

针对上述缺口，本文提出 **SE3-BSplineGS**，核心动机可概括为三点：

1. **显式连续运动表示**：采用数学上严格连续的SE(3)累积B样条（Cumulative B-spline）统一建模动态高斯的位置与朝向轨迹，使变形在任意时刻保持平滑，从根本上消除朝向跳变伪影。

2. **自适应运动基控制**：设计基于渲染误差和轨迹拟合误差的自适应修剪与稠密化机制，动态调整运动基和控制点的数量，在计算效率与表达能力之间取得最优平衡。

3. **多维度正则化与先验**：引入软分段重建策略抑制长时间运动干扰，并利用多视图扩散模型的SDS损失为不可见区域提供额外的多视图线索，缓解单目过拟合问题。

通过这些设计，SE3-BSplineGS在iPhone和NVIDIA两个基准数据集上均取得了显著优于先前SOTA方法的新视图合成质量，验证了显式连续运动表示在单目动态高斯泼溅中的关键作用。



## 核心方法与创新机理

本工作 **SE3-BSplineGS** 的核心创新在于首次将**显式连续 SE(3) 运动表示**引入单目动态高斯泼溅，并辅以**自适应运动基控制**与**软分段重建**，系统性地解决了现有方法中运动轨迹不连续、运动基密度固定导致的复杂区域伪影问题。以下从四个关键维度展开分析。

---

### 1. 从离散仿射到连续 SE(3) 轨迹：运动表示的质变

**瓶颈诊断**：现有动态高斯泼溅方法（如 SplineGS 仅对位置做三次 Hermite 样条插值，SoM 使用 SE(3) 姿态变换的线性组合）均未能同时建模高斯的位置与朝向连续变形轨迹。在纸风车等旋转运动场景中，朝向变形的不连续直接导致渲染伪影（Figure 1）。

**核心机制**：本方法采用 **SE(3) 累积 B 样条**统一表示动态高斯的位姿变形轨迹：

$$T(t) = \left(\prod_{i=0}^{N_c-1} \exp(\Omega_i(t) \xi_i)\right) T_0$$

其中 $\xi_i \in \mathfrak{se}(3)$ 为各控制点的李代数螺旋运动参数，$\Omega_i(t)$ 为 B 样条基函数在时刻 $t$ 的权重。这一公式将全部控制点的螺旋运动累积融合，在数学上保证轨迹的 $C^2$ 连续性，使高斯在任意时刻都能获得平滑的位置与朝向变形。

**证据强度**：运动表示消融实验（Table 3）显示，将本方法的 SE(3) B 样条替换为 SoM 的 SE(3) 姿态变换后，iPhone 数据集 mPSNR 从 20.17 骤降至 18.17；替换为 MoSca 的运动支架后降至 19.26。这一近 2 dB 的差距直接验证了连续位置与朝向联合建模的不可替代性。定性对比（Figure 6）进一步表明，缺少连续朝向建模的变体在旋转物体边缘产生明显撕裂伪影。

---

### 2. 自适应运动基控制：从固定密度到按需分配

**瓶颈诊断**：现有方法使用固定数量的运动基或控制点，无法根据局部运动复杂度动态调整表达能力。在运动剧烈区域，固定基数量导致欠拟合；在静态区域则造成计算冗余。

**核心机制**：本方法设计了**基于渲染误差与运动掩膜的自适应稠密化与修剪策略**。每 $N_{densify}=500$ 次迭代，计算渲染误差掩膜 $m_{error}$ 与动态区域掩膜 $m_d$ 的交集 $m = m_{error} \cap m_d$，将 3D 运动基投影至 2D 后筛选落在交集内的基进行稠密化——在现有控制点之间插入新点并更新节点向量。同时每 $N_{prune}=500$ 次迭代，选择轨迹拟合误差最小且低于阈值 $\epsilon_{prune}=5.0$ 的控制点进行修剪，移除冗余基。

**证据强度**：消融实验（Table 2）中移除自适应控制后，iPhone 数据集 mPSNR 从 20.17 降至 19.64，mSSIM 从 0.729 降至 0.715。修剪策略对比（Table 6）进一步表明，所提出的“选择最小误差且低于阈值”策略（mPSNR 20.17）显著优于随机修剪（19.84）和全部修剪（19.37）。Figure 9 的定性消融显示，不当修剪会导致动态区域出现空洞伪影。

---

### 3. 软分段重建：抑制长时间运动干扰

**瓶颈诊断**：在长视频序列中，动态高斯绑定的参考时间戳与观测时间戳间隔过大时，累积变形误差会导致背景区域出现“幽灵”伪影，干扰新视图合成质量。

**核心机制**：引入**软分段重建策略**，根据参考时间戳 $t_{ref}$ 与观测时间戳 $t_{obs}$ 的时间间隔动态调节高斯不透明度：

$$o' = \text{sigmoid}\big(\text{scale}(1 - |t_{ref} - t_{obs}|)\big) \cdot o$$

当观测时刻远离参考时刻时，高斯不透明度被平滑抑制，从而降低长时间运动带来的干扰。这与硬分段（直接剔除）不同，软分段保留了梯度传播，使模型仍能从远距离帧中学习有效信息。

**证据强度**：消融实验（Table 2）中移除软分段重建后，iPhone 数据集 mPSNR 从 20.17 降至 19.83。Figure 10 在纸风车场景的定性对比显示，移除该策略后风车叶片边缘出现明显的拖影伪影，证实其对长时运动一致性的关键作用。

---

### 4. 多视图扩散先验：弥补单目信息缺失

**瓶颈诊断**：单目视频训练中，部分视角区域从未被观测到，仅靠重建损失无法有效约束这些区域的生成，容易导致过拟合与不可见视角的崩溃。

**核心机制**：利用 **Zero123-xl-diffusers 多视图扩散模型**，仅在前景区域施加 Score Distillation Sampling (SDS) 损失：

$$\mathcal{L}_{sds} = \mathbb{E}_{t,\epsilon} \left[ \| \omega(t) (\epsilon_{\phi}(z_t, t, P_t P_s^{-1}, I_s) - \epsilon) \|_2^2 \right]$$

该损失以参考图像 $I_s$ 和相对相机位姿变换 $P_t P_s^{-1}$ 为条件，将目标视图的生成分布拉向合理图像，为训练视图中不可见区域提供多视图线索。损失权重 $\lambda_{sds}=0.01$ 较低，确保先验起辅助而非主导作用。

**证据强度**：消融实验（Table 2）中移除 SDS 先验后，iPhone 数据集 mPSNR 从 20.17 降至 19.91，NVIDIA 数据集 PSNR 从 27.81 降至 27.43。视觉消融（Figure 5）显示，移除 SDS 后不可见区域的纹理细节明显模糊。

---

### 创新点总结

| 创新维度 | 现有方法局限 | 本方法贡献 | 关键证据 |
|---------|------------|-----------|---------|
| 运动表示 | 仅位置连续或离散姿态组合 | SE(3) B 样条统一建模位置与朝向连续轨迹 | Table 3: +2.0 dB vs. SoM 姿态变换 |
| 运动基控制 | 固定数量基与控制点 | 自适应修剪与稠密化机制 | Table 2: +0.53 dB; Table 6: 策略消融验证 |
| 长时运动处理 | 无专门机制 | 软分段不透明度调节 | Table 2: +0.34 dB; Figure 10 定性验证 |
| 多视图监督 | 仅单目训练视图 | 多视图扩散 SDS 先验 | Table 2: +0.26 dB; Figure 5 定性验证 |

这些创新并非孤立存在，而是形成了一条完整的因果链：**连续 SE(3) 轨迹提供运动建模的数学基础，自适应控制确保表达能力与效率的平衡，软分段重建与扩散先验分别从时序一致性和多视图一致性两个维度补充约束**，共同实现了单目动态新视图合成的显著提升。



SE3-BSplineGS 的整体流程围绕“显式连续运动表示”展开，将单目视频重建为可驱动的高斯泼溅场景。图2给出了完整的模块关系与数据流。

**输入与初始化**  
系统输入为一组单目视频帧及其相机参数。首先通过深度重投影初始化静态高斯，同时利用预训练的2D跟踪先验（遵循MoSca的预处理流程）提取3D tracklet，初始化动态高斯及其参考时间戳。动态高斯随后被绑定到运动基上，作为后续变形的基础。

**核心运动表示：SE(3)累积B样条运动基**  
从3D tracklet的相邻帧相对姿态变换 $\Delta Q = Q_i^{-1} Q_{i+1}$ 出发，将其映射到李代数空间得到 $\xi = \log(\Delta Q)$，作为运动速度的表示。系统构建SE(3)累积B样条运动基，其连续时间下的位姿轨迹由所有控制点的累积螺旋运动定义：

$$T(t) = \left(\prod_{i=0}^{N_c-1} \exp(\Omega_i(t) \xi_i)\right) T_0$$

这一表示同时建模了动态高斯的位置与朝向连续变形轨迹，避免了逐时间戳仿射变换或仅位置连续样条（如SplineGS）带来的非连续朝向变形问题。

**自适应运动基控制**  
为在计算效率与表达能力间取得平衡，系统设计了自适应修剪与稠密化机制。每 $N_{prune}=500$ 次迭代，根据轨迹拟合误差和渲染误差对控制点进行修剪，优先移除贡献最小的点；每 $N_{densify}=500$ 次迭代，在复杂运动区域（由误差掩码与动态区域掩码的交集 $m^i = m_{error}^i \cap m_d^i$ 标识）稠密化新的运动基与控制点。这使得运动基密度能够根据局部运动复杂度动态调整。

**动态高斯变形与DQB融合**  
每个动态高斯被绑定至其最近的SE(3) B样条运动基。为平滑不同运动基之间的过渡，系统采用对偶四元数融合（DQB）聚合高斯 $g$ 的 $K$ 个最近邻运动基的相对姿态：

$$\Delta Q^g = \text{DQB}\left(\{(w_i, \Delta Q^i)\}_{i=1}^K\right)$$

融合后的相对姿态用于将高斯从参考空间变换到观测空间，获得观测时刻的位置与朝向。

**软分段重建**  
为抑制长时间运动带来的干扰，系统根据参考时间戳 $t_{ref}$ 与观测时间戳 $t_{obs}$ 的间隔，自适应调整高斯不透明度：

$$o' = \text{sigmoid}(\text{scale}(1 - |t_{ref} - t_{obs}|)) \cdot o$$

时间间隔越大，不透明度越低，从而减轻长时变形引起的伪影（如图10所示，在纸风车场景中显著改善了长期一致性）。

**扩散多视图先验**  
针对单目视频中不可见区域的信息缺失，系统利用Zero123-xl-diffusers多视图扩散模型，仅在前景区域施加得分蒸馏采样（SDS）损失：

$$\mathcal{L}_{sds} = \mathbb{E}_{t,\epsilon} \left[ \| \omega(t) (\epsilon_\phi(z_t, t, P_t P_s^{-1}, I_s) - \epsilon) \|_2^2 \right]$$

该损失以参考图像 $I_s$ 和相对相机位姿 $P_t P_s^{-1}$ 为条件，将目标视图的生成分布拉向合理图像，为训练视图不可见区域提供多视图线索。

**损失函数与优化**  
总损失为各项的加权组合：

$$\mathcal{L} = \lambda_{rec}\mathcal{L}_{rec} + \lambda_{geo}\mathcal{L}_{geo} + \lambda_{sds}\mathcal{L}_{sds} + \lambda_{arap}\mathcal{L}_{arap} + \lambda_{track}\mathcal{L}_{track} + \lambda_{smo}\mathcal{L}_{smo}$$

其中重建损失 $\mathcal{L}_{rec} = (1-\beta)\mathcal{L}_1(\hat{I}, I) + \beta\mathcal{L}_{ssim}(\hat{I}, I)$（$\beta=0.2$）平衡像素精度与感知质量；深度几何损失 $\mathcal{L}_{geo}$ 约束场景几何；ARAP运动平滑损失 $\mathcal{L}_{arap}$ 保持局部刚性；光流轨迹损失 $\mathcal{L}_{track}$ 约束跟踪一致性；相机平滑损失 $\mathcal{L}_{smo}$ 正则化相机外参。权重配置为 $\lambda_{rec}=1.0$、$\lambda_{geo}=0.075$、$\lambda_{arap}=1.0$、$\lambda_{track}=1.0$、$\lambda_{sds}=0.01$、$\lambda_{smo}=0.01$。

**输出**  
优化完成后，系统输出包含静态高斯与绑定SE(3) B样条运动基的动态高斯的完整场景表示，可在任意新视角与时间戳下进行高质量渲染。

### 补充图表

![[assets/figures/papers/paper_list_l1028_https_arxiv_org_abs_2603_25058/figures/002_Figure_2.jpg]]
*Figure 2: Overview of our method. We first initialize static Gaussians via depth reprojection and dynamic Gaussians from tracking points, by modeling their transformations with learnable SE(3) B-spline Motion Bases. We then adjust the number of motion bases and control points based on an adaptive control mechanism. Next, we employ a soft segment reconstruction strategy to fuse dynamic Gaussians at different reference timestamps to the observation timestamp, and further supplement the monocular video with scene-level multi-view cues derived from a multi-view diffusion model*



**SE3-BSplineGS** 的核心设计围绕一个关键瓶颈展开：现有单目动态高斯泼溅方法未能显式建模高斯的位置与朝向连续变形轨迹，且缺乏对运动基密度的自适应控制，导致复杂运动区域出现非连续朝向变形和长期运动干扰。该方法通过三个紧密耦合的模块——SE(3) 累积B样条运动基、自适应控制机制和软分段重建——构建了统一的连续运动表示，并辅以多视图扩散先验缓解单目过拟合。

### SE(3) 累积B样条运动基

运动基的构建从3D tracklet的预处理开始。给定相邻时间戳的tracklet位姿 $Q = [R, t]$，首先计算相对位姿变换：

$$\Delta Q = Q_i^{-1} Q_{i+1}$$

将其映射到李代数空间，得到表示位姿变化速度的螺旋运动参数：

$$\xi = \log(\Delta Q)$$

这些李代数向量作为控制点，构建SE(3)累积B样条。对于任意时刻 $t$，运动基的连续位姿轨迹由所有控制点的加权累积给出：

$$T(t) = \left(\prod_{i=0}^{N_c-1} \exp(\Omega_i(t) \xi_i)\right) T_0$$

其中 $\Omega_i(t)$ 是B样条基函数在时刻 $t$ 的权重，$N_c$ 为控制点数量，$T_0$ 为初始位姿。该公式将离散的控制点信息融合为一条数学上连续的位姿轨迹，同时建模位置和朝向的平滑变形——这是区别于仅建模位置连续性的SplineGS或仅使用线性姿态组合的Shape-of-Motion的核心所在。

### 动态高斯变形与DQB融合

每个动态高斯绑定至其最近的SE(3) B样条运动基。为获得更平滑的整体变形，对每个动态高斯 $g$，取其 $K$ 个最近邻运动基的相对姿态，通过对偶四元数混合（DQB）进行融合：

$$\Delta Q^{g} = \text{DQB}\left(\{(w_{i}, \Delta Q^{i})\}_{i=1}^{K}\right)$$

其中 $w_i$ 为基于距离的融合权重。该融合后的相对姿态直接作用于高斯的协方差矩阵和位置，实现从参考时间戳到观测时间戳的连续变形。这一设计使得即使单个运动基的表达能力有限，通过K近邻融合也能覆盖复杂的局部运动模式。

### 自适应控制机制

运动基的控制点数量并非固定，而是通过自适应修剪与稠密化动态调整。每 $N_{\text{prune}} = 500$ 次迭代执行修剪操作：选择具有最小修剪误差且该误差低于阈值 $\varepsilon_{\text{prune}} = 5.0$ 的控制点进行移除。稠密化则由复杂运动区域的掩码序列 $M$ 驱动——掩码由渲染误差区域与动态前景区域的交集定义：

$$m^{i} = m_{\text{error}}^{i} \cap m_{d}^{i}$$

其中 $m_{\text{error}}^{i}$ 为第 $i$ 个视图中渲染误差超过阈值的区域，$m_{d}^{i}$ 为动态高斯投影覆盖的区域。运动基的3D位置通过 $p = K P(t) T(t)^{j}$ 投影到图像平面，落在掩码区域内的运动基被选中进行稠密化，在复杂运动区域增加控制点数量以提升表达能力。

### 软分段重建

为抑制长时间运动带来的干扰，引入软分段重建策略。对每个动态高斯，根据其参考时间戳 $t_{\text{ref}}$ 与观测时间戳 $t_{\text{obs}}$ 的时间间隔调整不透明度：

$$o' = \text{sigmoid}\big(\text{scale}(1 - |t_{\text{ref}} - t_{\text{obs}}|)\big) \cdot o$$

其中scale为可学习参数。当观测时刻远离参考时刻时，高斯的不透明度被显著压低，从而抑制因长时变形累积导致的伪影。这一机制在纸风车等长时间运动场景中尤为关键（见Figure 10的消融对比）。

### 多视图扩散先验与损失函数

为补充单目训练视图中不可见区域的多视图线索，使用Zero123-xl-diffusers多视图扩散模型，仅在前景区域施加得分蒸馏采样（SDS）损失：

$$\mathcal{L}_{\text{sds}} = \mathbb{E}_{t,\epsilon} \left[ \| \omega(t) (\epsilon_{\phi}(z_t, t, P_t P_s^{-1}, I_s) - \epsilon) \|_2^2 \right]$$

其中 $I_s$ 为源视图，$P_t P_s^{-1}$ 为目标与源视图的相对相机位姿，$\epsilon_{\phi}$ 为扩散模型的去噪网络。总损失函数加权组合六个项：

$$\mathcal{L} = \lambda_{\text{rec}}\mathcal{L}_{\text{rec}} + \lambda_{\text{geo}}\mathcal{L}_{\text{geo}} + \lambda_{\text{sds}}\mathcal{L}_{\text{sds}} + \lambda_{\text{arap}}\mathcal{L}_{\text{arap}} + \lambda_{\text{track}}\mathcal{L}_{\text{track}} + \lambda_{\text{smo}}\mathcal{L}_{\text{smo}}$$

其中 $\mathcal{L}_{\text{rec}} = (1-\beta)\mathcal{L}_1(\hat{I}, I) + \beta\mathcal{L}_{\text{ssim}}(\hat{I}, I)$，$\beta=0.2$；权重设置为 $\lambda_{\text{rec}}=1.0$，$\lambda_{\text{geo}}=0.075$，$\lambda_{\text{sds}}=0.01$，$\lambda_{\text{arap}}=1.0$，$\lambda_{\text{trac}}=1.0$，$\lambda_{\text{smo}}=0.01$。ARAP损失约束局部刚性，轨迹损失对齐2D跟踪先验，平滑损失正则化相机外参。

**证据强度说明**：上述公式均来自论文方法部分（3.1-3.4节）的显式定义，置信度≥0.95。消融实验（Table 2, Table 3）从定量角度验证了各模块的必要性：移除自适应控制、软分段重建或SDS先验均导致iPhone数据集上mPSNR下降0.5-1.5 dB；将运动表示替换为SoM的姿态变换或MoSca的运动支架后，mPSNR分别降至18.17和19.26（Ours为20.17），证实SE(3) B样条连续建模的核心贡献。

### 补充图表

![[assets/figures/papers/paper_list_l1028_https_arxiv_org_abs_2603_25058/figures/009_Figure_6.jpg]]
*Figure 6: Effect of SE(3) B-spline Motion Bases*

![[assets/figures/papers/paper_list_l1028_https_arxiv_org_abs_2603_25058/figures/014_Figure_9.jpg]]
*Figure 9: Effect of pruning strategy*

![[assets/figures/papers/paper_list_l1028_https_arxiv_org_abs_2603_25058/figures/016_Figure_10.jpg]]
*Figure 10: Effect of soft segmentation reconstruction*



## 实验与关键发现

### 核心定量结果

Table 1 汇总了在 iPhone 与 NVIDIA 两个动态场景基准上的新视图合成对比。SE3-BSplineGS 在两个数据集的所有指标上均取得最佳成绩：iPhone 上 mPSNR/mSSIM/mLPIPS 分别为 **20.17/0.729/0.274**，NVIDIA 上 PSNR/SSIM/LPIPS 分别为 **27.81/0.871/0.049**。对比方法包括 **SoM**（SE(3) 运动基线性组合）、**MoSca**（4D 运动支架）、**SplineGS**（仅位置连续样条）、**MarbleGS**、**HiMoR** 以及 **MoDec-GS**，均低于本方法。该结果直接支撑了核心论断：显式连续运动表示在单目动态重建中具有决定性优势。

![[assets/figures/papers/paper_list_l1028_https_arxiv_org_abs_2603_25058/figures/006_Table_1.jpg]]
*Table 1: Quantitative comparison of novel view synthesis on the iPhone [12] and NVIDIA [48] datasets. Note that all training times are measured on the skating scene using a single NVIDIA RTX 4090 GPU, and FPS is measured on the same GPU at 480 × 360 resolution*

**公平性说明**：训练时间与 FPS 均在单块 RTX 4090 上测量（skating 场景），未验证跨硬件效率；iPhone 数据集仅使用 5 个场景（排除了 2 个相机姿态不准的场景），可能高估平均性能；部分对比方法的超参数可能未针对这些数据集充分调优。

### 消融实验：组件贡献

Table 2 展示了系统级消融。移除自适应控制（w/o Adap.）、软分段重建（w/o Soft.）或多视图 SDS 先验（w/o SDS）均导致 mPSNR/mSSIM/mLPIPS 在 iPhone 和 NVIDIA 上一致下降，验证了每个组件对最终性能的必要性。定性消融见 Figure 5，缺失组件会导致动态区域出现明显伪影或几何不连续。

![[assets/figures/papers/paper_list_l1028_https_arxiv_org_abs_2603_25058/figures/007_Table_2.jpg]]
*Table 2: Ablation studies on the iPhone and NVIDIA dataset. “w/o Adap.” denotes removing the adaptive control in SE(3) Bspline motion bases, “w/o Soft.” means omitting soft segment reconstruction, and “w/o*

![[assets/figures/papers/paper_list_l1028_https_arxiv_org_abs_2603_25058/figures/005_Figure_5.jpg]]
*Figure 5: Visual ablation study on scenes from the iPhone and NVIDIA datasets*

### 运动表示消融：SE(3) B样条的核心贡献

Table 3 直接对比了不同运动表示对 iPhone 数据集性能的影响。将 SE(3) B样条替换为 **SoM** 的 SE(3) 姿态变换后，mPSNR 骤降至 18.17；替换为 **MoSca** 的运动支架后，mPSNR 降至 19.26，均远低于 Ours 的 20.17。这表明仅对位置或姿态进行线性/离散建模无法保证朝向的连续性与轨迹平滑性，而 SE(3) 累积 B样条通过统一建模位置与朝向的连续变形，是性能提升的关键因果旋钮。Figure 6 的定性结果进一步佐证了该结论。

![[assets/figures/papers/paper_list_l1028_https_arxiv_org_abs_2603_25058/figures/008_Table_3.jpg]]
*Table 3: Ablation study of SE(3) B-spline motion bases on the iPhone dataset. “w/ Pose trans.” means replacing our motion representation with the SE(3)-based pose transformation used in SoM [40]. “w/ Motion scaff.” indicates replacing the representation with the motion scaffolds used in MoSca [22]*

### 自适应控制策略的有效性

Table 6 比较了控制点修剪策略：本方法采用“选择最小修剪误差且低于阈值”的策略（iPhone mPSNR 20.17，NVIDIA PSNR 27.81），优于随机修剪（19.84/27.59）和全部修剪（19.37/27.26）。这表明自适应地根据局部运动复杂度调整运动基密度，能在计算效率与表达能力间取得有效平衡。Figure 9 的定性消融展示了不同修剪策略对动态区域重建质量的影响。

![[assets/figures/papers/paper_list_l1028_https_arxiv_org_abs_2603_25058/figures/015_Table_6.jpg]]
*Table 6: Ablation on the iPhone and NVIDIA datasets. “w/ Random” denotes randomly pruning a control point with error below*

### 软分段重建的长期一致性

软分段重建通过 $o' = \text{sigmoid}(\text{scale}(1 - |t_{\text{ref}} - t_{\text{obs}}|)) \cdot o$ 抑制长时间运动带来的干扰。Figure 10 以纸风车场景为例，移除该机制后长时间变形区域出现明显伪影，证实其对长期一致性的贡献。

### 鲁棒性与局限性

**鲁棒性**：Table 4 显示本方法在对应点跟踪精度（PCK-T↑）上达到 0.833，优于对比方法。Table 5 表明对 2D 跟踪先验施加 [-15, 15] 范围内的随机扰动后，mPSNR 仅从 20.17 降至 20.11，展现了对先验误差的一定容忍度。

**失败模式**：Figure 7 明确展示了本方法在大幅度非刚性运动场景下的失效情况——出现严重伪影甚至重建失败。这与方法依赖 SE(3) B样条建模刚体/近刚体运动的假设一致：当场景包含复杂人体动作等强非刚性变形时，运动基无法准确捕捉高斯粒子的独立形变。此外，多视图扩散先验仅作用于前景且需在训练视图附近采样，极端新视角下的生成能力受限；相机参数不准时，虽可通过学习外参并施加平滑损失缓解，但无法完全消除由此产生的伪影。

### 关键图表索引

- **Table 1**：主定量对比，支撑整体性能优势
- **Table 2**：组件消融，验证各模块必要性
- **Table 3**：运动表示消融，证明 SE(3) B样条的核心贡献
- **Table 6**：控制点修剪策略消融，展示自适应机制的优越性
- **Figure 7**：失败案例，揭示方法在大非刚性运动下的局限
- **Figure 10**：软分段重建消融，展示长期一致性机制的效果

### 补充图表

![[assets/figures/papers/paper_list_l1028_https_arxiv_org_abs_2603_25058/figures/001_Figure_1.jpg]]
*Figure 1: Dynamic Gaussian Splatting from monocular videos. Our method synthesizes high-quality novel views from monocular videos, while the compared methods, e.g., MoSca [22], HiMoR [25], and SplineGS [32], fail to faithfully reconstruct the dynamic windmill*

![[assets/figures/papers/paper_list_l1028_https_arxiv_org_abs_2603_25058/figures/011_Table_4.jpg]]
*Table 4: Comparison of correspondence on the iPhone dataset*

![[assets/figures/papers/paper_list_l1028_https_arxiv_org_abs_2603_25058/figures/012_Table_5.jpg]]
*Table 5: Effect of 2D prior errors. “w/ Prior pert.” indicates that the 2D tracking prior is perturbed by adding random noise within the range of [-15, 15]*



## 定位与知识库关联

### 1. 与基线工作的关系

**SE3-BSplineGS** 的核心目标是在单目动态场景重建中实现**显式、连续的动态高斯位姿轨迹建模**，其设计直接回应了现有方法的若干关键瓶颈。

*   **相对于仅位置连续建模的方法 (如 SplineGS):** SplineGS 使用三次 Hermite 样条建模高斯的连续位置轨迹，但未显式处理朝向的连续变形。SE3-BSplineGS 通过 **SE(3) 累积 B 样条** 统一建模位置与朝向的连续轨迹，避免了在复杂旋转区域出现的非连续朝向变形伪影。Table 3 的消融实验直接证实了这一点：将本方法的运动表示替换为基于 SE(3) 的姿态变换（“w/ Pose trans.”，类似 SoM 的思路）后，mPSNR 从 20.17 降至 18.17。

*   **相对于基于运动支架的方法 (如 MoSca):** MoSca 构建 4D 运动支架来表示场景运动，但其运动基的数量和分布是固定的，缺乏对局部运动复杂度的自适应。SE3-BSplineGS 引入了**自适应控制机制**，根据渲染误差和轨迹拟合误差动态地对 SE(3) B 样条运动基的控制点进行修剪与稠密化。Table 3 显示，替换为 MoSca 的运动支架（“w/ Motion scaff.”）后，mPSNR 降至 19.26，证明了自适应、连续运动基的优势。

*   **相对于基于运动基线性组合的方法 (如 Shape-of-Motion, SoM):** SoM 将场景运动表示为多个 SE(3) 运动基的线性组合，但未采用样条保证时间连续性。本方法通过累积 B 样条公式 $T(t) = (\prod_{i=0}^{N_c-1} \exp(\Omega_i(t) \xi_i)) T_0$ 实现了数学上连续的轨迹，且控制点数量远少于 SoM 所需的逐帧姿态数量，在表达能力和计算效率间取得了更好的平衡。

*   **相对于其他动态高斯方法 (如 MarbleGS, MoDec-GS):** MarbleGS 和 MoDec-GS 是同期或更早的动态高斯泼溅工作。如 Figure 1 和 Figure 4 所示，它们在本方法重点解决的复杂运动场景（如旋转的风车、摆动的衣服）中，会产生更明显的伪影或几何失真。本方法通过**软分段重建**策略（根据时间间隔调整不透明度 $o' = \text{sigmoid}(\text{scale}(1 - |t_{ref} - t_{obs}|)) * o$）有效抑制了长时间运动带来的干扰，这是前述方法所不具备的。

### 2. 适用边界与局限性

本方法的有效性建立在若干前提之上，其适用边界在论文的失败案例分析中得到了明确界定：

1.  **运动幅度限制：** 该方法的核心假设是场景运动可以由一组 SE(3) B 样条运动基近似。对于包含**大幅度非刚性运动**的场景（如复杂的人体动作、剧烈形变的衣物），该假设被破坏。**Figure 7** 明确展示了在此类场景下的失败案例，出现严重的几何破碎和伪影。这是该方法最根本的局限性。

2.  **对 2D 跟踪先验的依赖：** 运动基的初始化依赖于由 MoSca 预处理流程得到的 3D tracklets，该流程又依赖于 2D 跟踪先验。**Table 5** 显示，当对 2D 先验施加扰动时，性能（mPSNR）从 20.17 轻微下降至 20.11，表明方法对此类误差具有一定的鲁棒性，但无法完全消除其影响。若先验存在系统性的大误差，重建质量将不可避免的下降。

3.  **扩散先验的约束：** 多视图扩散模型（Zero123-xl-diffusers）施加的 SDS 损失仅作用于前景区域，且需要在训练视图附近采样新视角以确保先验的可靠性。这限制了该方法在极端新视角下的生成和补全能力，对于训练视图中大面积被遮挡的区域，扩散先验可能无法提供有效信息。

4.  **相机位姿精度：** 尽管方法包含相机外参的微调和相机平滑损失，但论文指出，在 iPhone 数据集中排除了 2 个因相机姿态不准的场景。这表明，对于相机位姿估计误差较大的输入，方法无法完全消除由此产生的伪影。

### 3. 开放问题

基于该方法的现有设计和局限性，以下问题值得进一步探索：

*   **运动模糊与快速运动：** 该方法如何处理包含严重运动模糊和散焦的快速运动单目视频？当前的管道依赖于清晰的 2D 跟踪点，运动模糊会直接破坏这一前提。
*   **自适应控制的泛化性：** 自适应控制机制的超参数（如修剪间隔 `N_prune=500`，误差阈值 `ε_prune=5.0`）对不同场景的敏感度如何？能否设计完全自适应的、无需手动调节阈值的控制策略，以应对包含多个运动速度不同物体的复杂场景？
*   **更强先验的集成：** 当前使用的 Zero123-xl-diffusers 是一个图像扩散模型。能否将其替换为更强大的**视频扩散模型**，以提供时序上更一致的多视图先验，从而更好地处理动态场景和被遮挡区域？
*   **多模态数据扩展：** 该方法目前仅使用单目 RGB 视频。是否可以将该框架扩展到**多目视频**或融合**深度传感器数据**，以从根本上解决单目重建中的尺度模糊性和遮挡问题，从而应对更具挑战性的大幅度非刚性运动场景？



## 原文 PDF

![[paperPDFs/CVPR_2026/Learning_Explicit_Continuous_Motion_Representation_for_Dynamic_Gaussian_Splatting_from_Monocular_Videos.pdf]]
