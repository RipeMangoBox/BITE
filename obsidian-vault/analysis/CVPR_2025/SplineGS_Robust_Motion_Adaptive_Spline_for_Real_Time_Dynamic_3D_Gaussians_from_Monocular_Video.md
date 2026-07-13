---
title: "SplineGS: Robust Motion-Adaptive Spline for Real-Time Dynamic 3D Gaussians from Monocular Video"
type: paper
paper_level: A
venue: CVPR
year: 2025
pdf_ref: paperPDFs/CVPR_2025/SplineGS_Robust_Motion_Adaptive_Spline_for_Real_Time_Dynamic_3D_Gaussians_from_Monocular_Video.pdf
project_link: https://kaist-viclab.github.io/splinegs-site/
code_link: null
aliases:
- SplineGS
tags:
- CVPR_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "引入基于三次Hermite样条的运动自适应样条（MAS）和自适应控制点剪枝（MACP），用少量可学习控制点精确描述每个动态高斯的连续运动轨迹。"
primary_logic: "采用样条表示动态高斯轨迹，配合联合相机参数优化，实现无需COLMAP预处理的快速高质量动态场景重建与渲染。"
claims:
- "SplineGS在NVIDIA数据集上平均PSNR达到27.21 dB，LPIPS 0.053，渲染速度400 FPS，显著优于所有对比方法。"
- "消融实验表明MAS优于MLP、网格、多项式、贝塞尔等变形模型 (Table 3-(a))。"
- "MACP在保证渲染质量的同时减少控制点数量，PSNR与固定控制点相比取得最佳权衡 (Table 3-(c))。"
- "去除任何损失项（如L_pc）会导致PSNR急剧下降，证明联合相机优化及一致性损失的必要性 (Table 3-(b))。"
---

# SplineGS: Robust Motion-Adaptive Spline for Real-Time Dynamic 3D Gaussians from Monocular Video

> [!tip] 核心洞察
> 采用样条表示动态高斯轨迹，配合联合相机参数优化，实现无需COLMAP预处理的快速高质量动态场景重建与渲染。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | SplineGS：面向单目视频的实时动态3D高斯鲁棒运动自适应样条 |
| 英文题名 | SplineGS: Robust Motion-Adaptive Spline for Real-Time Dynamic 3D Gaussians from Monocular Video |
| 会议/期刊 | CVPR 2025 |
| Links | [paper](https://arxiv.org/abs/2412.09982) · [Project](https://kaist-viclab.github.io/splinegs-site/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | SplineGS |
| Dataset | NVIDIA dataset (novel view synthesis) |

> [!tip] 效果简介
> - NVIDIA dataset (novel view synthesis) 上，PSNR / LPIPS / FPS 为 27.21 / 0.053 / 400，对比 MoSca (COLMAP-free best) 26.61 / 0.069 / N/A，变化 +0.60 PSNR / -0.016 LPIPS。

## 概要

从单目视频重建动态场景并合成新时空视角，是计算机视觉中的核心挑战。现有动态3D高斯泼溅（3DGS）方法存在两个关键瓶颈：其一，运动建模依赖MLP网络、网格分解或固定阶多项式，难以灵活适应复杂多变的场景动态；其二，相机参数获取依赖COLMAP等SfM预处理，在真实单目视频中稳定性差，甚至完全失效。

SplineGS针对上述瓶颈提出了三个因果性改进：
1. **运动自适应样条（MAS）**：用基于三次Hermite样条的可学习控制点替代MLP或固定多项式，以少量控制点精确描述每个动态高斯的连续运动轨迹。
2. **运动自适应控制点剪枝（MACP）**：在训练中动态决定每个高斯的最佳控制点数，在保证渲染质量的同时减少冗余控制点。
3. **联合相机参数优化**：通过两阶段优化（预热阶段+主训练阶段）联合估计相机内外参和高斯属性，实现无需COLMAP预处理的端到端重建。

核心结论：SplineGS在NVIDIA数据集上新视角合成达到平均PSNR 27.21 dB、LPIPS 0.053，渲染速度400 FPS，显著优于所有对比方法（Table 1）。消融实验证实，MAS在运动建模上优于MLP、网格、多项式及贝塞尔曲线等替代方案（Table 3-a），MACP以更少控制点实现更高PSNR（Table 3-c），去除光度一致性损失则导致PSNR骤降至17.49（Table 3-b）。



动态场景的新视角合成是计算机视觉与图形学的核心问题，其目标是从一组稀疏的二维观测中重建并渲染任意时刻、任意视角下的三维动态场景。近年来，以3D Gaussian Splatting（3DGS）为代表的显式辐射场表示凭借其高保真渲染与实时性能，迅速成为该领域的主流范式。然而，将3DGS从静态场景拓展至动态场景时，一个根本性瓶颈浮现：**如何精确、高效地建模每个3D高斯随时间的连续运动轨迹**。

现有动态3DGS方法在运动建模上存在明显的机制性缺陷。一类方法采用MLP网络直接预测每一帧的变形场（如4DGS），虽具备一定的表达能力，但MLP推理延迟高，严重拖累渲染速度，且隐式建模缺乏对运动轨迹的结构化约束，容易产生时间不一致的伪影。另一类方法将运动轨迹建模为固定阶次的多项式（如STGS），或使用时空网格分解，这些参数化形式过于刚性，无法灵活适应场景中不同区域运动复杂度的巨大差异——例如，背景区域的静态高斯仅需常数表示，而快速运动的肢体则需要高阶曲线描述。此外，几乎所有现有方法都依赖COLMAP等外部SfM工具进行相机参数预处理。在真实单目视频中，COLMAP常因纹理稀疏、运动模糊或动态前景干扰而失效，导致整个重建流程崩溃。即便是少数COLMAP-free的动态NeRF方法（如RoDynRF），其渲染速度也远不能满足实时交互需求。

上述缺口揭示了动态3DGS领域的一个核心因果杠杆：**运动表示的选择直接决定了重建质量、渲染效率与系统鲁棒性的三角平衡**。SplineGS正是围绕这一杠杆展开设计。其核心洞察是：三次Hermite样条作为一种经典的分段插值工具，能够以极少的控制点精确描述任意复杂度的连续轨迹，同时保持解析可微与计算轻量。通过将每个动态高斯的均值轨迹建模为可学习的样条函数，并引入自适应控制点剪枝机制（MACP）动态调节每条样条的复杂度，SplineGS从根本上解决了“统一参数化无法适配异质运动”的难题。在此基础上，联合优化相机参数的两阶段训练框架消除了对COLMAP的依赖，使系统在真实单目视频上具备端到端的鲁棒性。



## 核心方法与创新机理

SplineGS 的核心创新在于从根本上重构了动态 3DGS 的运动建模范式，解决了现有方法在单目视频场景下面临的三个瓶颈：运动表示灵活性不足、对 COLMAP 预处理的强依赖，以及控制点数量与运动复杂度之间的失配。其创新通过以下三个关键机制实现。

### 1. 运动自适应样条（MAS）：从离散变形到场域连续轨迹

现有动态 3DGS 方法普遍采用 MLP 网络、网格分解或固定阶多项式来建模高斯均值随时间的变化。这些表示要么缺乏对复杂非刚性运动的表达能力，要么在长序列上产生累积误差。SplineGS 的核心洞察在于：**每个动态高斯的运动轨迹本质上是一条连续的空间曲线，应当用样条而非逐帧变形来刻画**。

具体而言，MAS 将每个动态高斯的均值参数 $\mu$ 替换为一组可学习的控制点 $\mathbf{P}$，并通过分段三次 Hermite 样条函数 $S(t, \mathbf{P})$ 计算任意时刻 $t$ 的高斯位置：

$$\mu(t) = S(t, \mathbf{P})$$

三次 Hermite 样条的关键优势在于其局部支撑性——每个控制点仅影响相邻两个区间的曲线形状，这使得优化过程更加稳定，且天然支持对不同时间段的运动进行独立调整。与 MLP 的全局隐式表示相比，样条的显式几何参数化带来了两个直接收益：训练收敛更快，推理时无需网络前向计算，变形延迟仅为 5.63 ns。

### 2. 自适应控制点剪枝（MACP）：以最少控制点匹配运动复杂度

传统样条方法通常为所有高斯分配相同数量的控制点，但这忽略了场景中运动复杂度的空间异质性——静态背景区域的高斯几乎不需要控制点，而快速运动的前景目标则需要更密集的控制点来精确描述轨迹。固定控制点数量会导致两种失效模式：控制点过少时欠拟合复杂运动，过多时则引入冗余自由度导致过拟合。

MACP 在 3D 高斯致密化过程之上引入了一个自适应剪枝机制：对每个动态高斯，尝试用减少一个控制点的样条 $\mathbf{P}'$ 逼近原始样条 $\mathbf{P}$，通过最小二乘拟合求解：

$$\min_{\mathbf{P}'} \sum_{t=0}^{N_f-1} \| S(t, \mathbf{P}) - S(t, \mathbf{P}') \|_2^2$$

剪枝的接受条件由重投影误差决定：

$$E = \frac{1}{N_f} \sum_{t=0}^{N_f-1} \| \pi_{\hat{K}}(\hat{R}_t S(t, \mathbf{P}) + \hat{T}_t) - \pi_{\hat{K}}(\hat{R}_t S(t, \mathbf{P}') + \hat{T}_t) \|_2^2$$

当 $E < \epsilon$ 时接受剪枝。这一设计使得简单运动区域的高斯自动收敛到极少的控制点，而复杂运动区域保留更多控制点，在渲染质量与计算效率之间取得了最优权衡（Table 3-(c)：PSNR 27.21 vs. 固定 $N_c=4$ 的 26.79 和固定 $N_c=N_f$ 的 26.83）。

### 3. COLMAP-free 联合优化：端到端消除预处理依赖

大多数动态 3DGS 方法依赖 COLMAP 等 SfM 流水线提供相机参数和初始点云，但在真实单目视频中，COLMAP 常因纹理不足、运动模糊或动态前景干扰而失效。SplineGS 采用两阶段优化策略彻底移除了这一依赖：

- **预热阶段**：仅优化相机参数，使用光度一致性损失 $\mathcal{L}_{\mathrm{pc}}$ 和几何一致性损失 $\mathcal{L}_{\mathrm{gc}}$ 约束相邻帧间的外观与 3D 结构一致性。
- **主训练阶段**：联合优化 3D 高斯属性、MAS 控制点和相机参数。

相机外参通过 MLP 从时间位置编码直接预测 $[\hat{R}_t | \hat{T}_t] = F_\theta(\gamma(t))$，内参在所有帧间共享。消融实验（Table 3-(b)）表明，移除 $\mathcal{L}_{\mathrm{pc}}$ 会导致 PSNR 从 27.21 骤降至 17.49，验证了联合优化中一致性约束的关键作用。

### 创新总结

SplineGS 的三个创新形成了完整的因果链：MAS 提供了灵活且高效的连续运动表示，MACP 使这一表示自适应地匹配局部运动复杂度，COLMAP-free 联合优化则将整个流程从预处理依赖中解放出来。三者协同使得 SplineGS 在 NVIDIA 数据集上以 27.21 dB PSNR 和 400 FPS 的渲染速度显著超越所有对比方法，同时无需任何外部相机标定。



SplineGS 的整体架构围绕“无需 COLMAP 预处理的动态 3DGS 实时渲染”这一目标设计，核心思路是用**可学习的样条控制点**替代传统 MLP 或固定阶多项式来建模每个动态高斯的连续运动轨迹，并通过**两阶段联合优化**同时估计相机参数与高斯属性。

### 两阶段优化流程

SplineGS 采用**预热阶段（Warm-up Stage）**与**主训练阶段（Main Training Stage）**串联的优化策略，如 Figure 2 所示。

- **预热阶段**：仅优化相机参数（外参由 MLP 预测，内参共享），利用光度一致性损失 $\mathcal{L}_{\mathrm{pc}}$ 与几何一致性损失 $\mathcal{L}_{\mathrm{gc}}$ 进行约束（Eq. 14）。该阶段不涉及任何 3D 高斯优化，旨在为主训练提供可靠的相机初值，避免 COLMAP 预处理在真实单目视频中失效的问题。
  
- **主训练阶段**：联合优化 3D 高斯属性、相机参数和运动自适应样条（MAS）。总损失 $\mathcal{L}_{\mathrm{total}}^{\mathrm{main}}$（Eq. 15）整合了 RGB 渲染损失、深度损失、掩码损失（Dice loss）、光度一致性损失、深度一致性损失和几何一致性损失，引导模型从纯单目视频中有效重建动态场景。

### 核心模块与数据流

1. **运动自适应样条（MAS）**  
   将每个动态高斯的均值 $\mu(t)$ 建模为三次 Hermite 样条函数 $S(t, \mathbf{P})$（Eq. 3-4），其中 $\mathbf{P}$ 为一组可学习的控制点。相比 MLP 或网格变形，样条表示能用极少的控制点精确描述连续运动轨迹，且推理时仅需插值计算，延迟极低（5.63 ns，Table 3）。

2. **控制点初始化**  
   利用长期 2D 跟踪和度量深度先验，通过反投影函数 $\mathcal{W}_t$（Eq. 5）将 2D 轨迹提升到 3D 空间，再以最小二乘拟合（Eq. 6）初始化每个高斯的控制点集。这一初始化策略为后续优化提供了合理的运动先验。

3. **运动自适应控制点剪枝（MACP）**  
   在训练过程中周期性（每 100 次迭代）评估每个高斯的控制点数是否冗余。通过求解减少一个控制点的近似样条（Eq. 7），并计算重投影误差 $E$（Eq. 8），当 $E < \epsilon$ 时接受剪枝。MACP 使简单运动的高斯使用更少控制点，复杂运动的高斯保留更多控制点，在保证渲染质量的同时降低计算开销（Table 3-(c)）。

4. **渲染模块**  
   采用与原始 3DGS 一致的可微分光栅化管线，对静态和动态高斯分别处理：动态高斯的均值由 MAS 根据时间 $t$ 插值得到，随后通过 $\alpha$ 混合（Eq. 2）合成像素颜色 $\mathbf{C}$ 和运动掩码 $\hat{M}_t$（Eq. 17）。运动掩码用于分离动态/静态区域，指导掩码损失 $\mathcal{L}_{\mathrm{M}}$（Eq. 16）的优化。

整个框架的输入为单目视频帧序列，输出为新时空视角的渲染图像，无需任何外部相机标定预处理。



SplineGS 将动态场景建模分解为三个紧密耦合的核心模块：运动自适应样条（MAS）描述高斯均值轨迹、自适应控制点剪枝（MACP）平衡表达力与效率、以及无 COLMAP 的相机参数联合优化。以下逐一推导其数学形式与变量含义。

### 动态高斯的样条化均值建模（MAS）

传统 3DGS 中每个高斯的均值 $\pmb{\mu}$ 是静态参数。SplineGS 将其替换为一组可学习的控制点 $\mathbf{P}$，并通过三次 Hermite 样条函数 $S(t, \mathbf{P})$ 计算任意时刻 $t$ 的均值：

$$\mu(t) = S(t, \mathbf{P})$$

三次 Hermite 样条的具体形式为分段插值：

$$S(t, \mathbf{P}) = (2t_r^3 - 3t_r^2 + 1)\mathbf{p}_{\lfloor t_s \rfloor} + (t_r^3 - 2t_r^2 + t_r)\mathbf{m}_{\lfloor t_s \rfloor} + (-2t_r^3 + 3t_r^2)\mathbf{p}_{\lfloor t_s \rfloor + 1} + (t_r^3 - t_r^2)\mathbf{m}_{\lfloor t_s \rfloor + 1}$$

其中 $t_s = t \cdot (N_c - 1) / (N_f - 1)$ 将时间 $t$ 映射到控制点索引空间，$t_r = t_s - \lfloor t_s \rfloor$ 为段内局部参数。$\mathbf{p}_k$ 为第 $k$ 个控制点的空间位置，$\mathbf{m}_k$ 为对应的切线向量，二者均为可学习参数。$N_c$ 为控制点数量，$N_f$ 为视频总帧数。

该设计的因果机制在于：样条的局部支撑性使得每个控制点仅影响相邻时间段的轨迹，少量控制点即可精确描述复杂运动，避免了 MLP 的全局耦合和多项式的高阶振荡。

### 控制点初始化

为给 MAS 提供合理的初始轨迹，SplineGS 利用现成的 2D 跟踪器获取像素轨迹 $\varphi_t^{\mathrm{tr}}$，结合度量深度先验 $\boldsymbol{d}_t(\varphi_t^{\mathrm{tr}})$ 和当前相机参数估计，通过反投影函数 $\mathcal{W}_t$ 将 2D 轨迹提升到 3D 世界空间：

$$\mathcal{W}_t(\boldsymbol{\varphi}_t^{\mathrm{tr}}) = \hat{R}_t^\top \pi_{\hat{K}}^{-1}(\boldsymbol{\varphi}_t^{\mathrm{tr}}, \boldsymbol{d}_t(\boldsymbol{\varphi}_t^{\mathrm{tr}})) - \hat{R}_t^\top \hat{T}_t$$

其中 $\pi_{\hat{K}}^{-1}$ 为已知内参 $\hat{K}$ 的反投影，$\hat{R}_t, \hat{T}_t$ 为当前估计的相机外参。随后通过最小二乘拟合将样条对齐到初始 3D 轨迹：

$$\operatorname*{min}_{\mathbf{p}} \sum_{t=0}^{N_f-1} \| \mathcal{W}_t(\varphi_t^{\mathrm{tr}}) - S(t, \mathbf{P}) \|_2^2$$

这一步为后续联合优化提供了物理上合理的运动先验，避免了随机初始化导致的收敛困难。

### 运动自适应控制点剪枝（MACP）

不同动态高斯对应的运动复杂度差异显著：静态区域仅需极少控制点，而快速变形区域需要更密集的控制点。MACP 在 3D 高斯致密化过程中周期性地评估每个动态高斯，尝试将控制点数 $N_c$ 减少 1。具体地，求解缩减后的控制点集 $\mathbf{P}'$：

$$\operatorname*{min}_{\mathbf{P}'} \sum_{t=0}^{N_f-1} \| S(t, \mathbf{P}) - S(t, \mathbf{P}') \|_2^2$$

然后计算原始样条与缩减样条在图像平面的重投影误差：

$$E = \frac{1}{N_f} \sum_{t=0}^{N_f-1} \| \pi_{\hat{K}}(\hat{R}_t S(t, \mathbf{P}) + \hat{T}_t) - \pi_{\hat{K}}(\hat{R}_t S(t, \mathbf{P}') + \hat{T}_t) \|_2^2$$

若 $E < \epsilon$（$\epsilon$ 为预设阈值），则接受剪枝，将 $\mathbf{P}$ 替换为 $\mathbf{P}'$；否则保留原控制点。该机制在图像空间评估剪枝影响，直接关联渲染质量，确保控制点减少不会引入可感知的视觉退化。消融实验证实 MACP 以更少控制点实现了比固定 $N_c=4$ 或 $N_c=N_f$ 更高的 PSNR（27.21 vs. 26.79/26.83），变形延迟仅 5.63 ns（Table 3-(c)）。

### 相机参数联合估计

为摆脱对 COLMAP 预处理依赖，SplineGS 使用小型 MLP $F_\theta$ 从时间位置编码 $\gamma(t)$ 直接预测每帧外参：

$$[\hat{R}_t | \hat{T}_t] = F_\theta(\gamma(t))$$

内参 $\hat{K}$ 在所有帧间共享并联合优化。相机参数通过两阶段优化逐步精化：预热阶段仅使用光度一致性损失 $\mathcal{L}_{\mathrm{pc}}$ 和几何一致性损失 $\mathcal{L}_{\mathrm{gc}}$ 优化相机参数；主训练阶段则联合优化高斯属性、MAS 控制点和相机参数。消融实验表明，移除 $\mathcal{L}_{\mathrm{pc}}$ 导致 PSNR 从 27.21 骤降至 17.49（Table 3-(b)），验证了光度一致性约束对相机估计的关键作用。

### 渲染与损失函数

动态高斯的渲染沿用 3DGS 的可微分光栅化管线。对于每个像素，按深度排序的 $\mathcal{N}$ 个高斯通过 $\alpha$ 混合计算颜色：

$$\pmb{C} = \sum_{i \in \mathcal{N}} \pmb{c}_i \alpha_i \prod_{j=1}^{i-1}(1 - \alpha_j)$$

其中 $\pmb{c}_i$ 为第 $i$ 个高斯的颜色，$\alpha_i$ 为评估密度乘以协方差后的不透明度。主训练阶段的总损失为：

$$\mathcal{L}_{\mathrm{total}}^{\mathrm{main}} = \lambda_{\mathrm{rgb}} \mathcal{L}_{\mathrm{rgb}} + \lambda_{\mathrm{d}} \mathcal{L}_{\mathrm{d}} + \lambda_{\mathrm{M}} \mathcal{L}_{\mathrm{M}} + \lambda_{\mathrm{pc}} \mathcal{L}_{\mathrm{pc}} + \lambda_{\mathrm{d-pc}} \mathcal{L}_{\mathrm{d-pc}} + \lambda_{\mathrm{gc}} \mathcal{L}_{\mathrm{gc}}$$

其中 $\mathcal{L}_{\mathrm{rgb}}$ 为 L1 与 SSIM 的组合，$\mathcal{L}_{\mathrm{d}}$ 为深度损失，$\mathcal{L}_{\mathrm{M}}$ 为动态/静态分离的 Dice 掩码损失，$\mathcal{L}_{\mathrm{pc}}$ 和 $\mathcal{L}_{\mathrm{gc}}$ 分别为光度和几何一致性损失，$\mathcal{L}_{\mathrm{d-pc}}$ 为深度一致性损失。各损失项的协同作用通过消融实验得到充分验证（Table 3-(b)）。



## 实验与关键发现

### 主要结果：NVIDIA 数据集新视角合成

SplineGS 在 NVIDIA 数据集的新视角合成任务上取得了最优性能。如 Table 1 所示，SplineGS 平均 PSNR 达到 **27.21 dB**，LPIPS 为 **0.053**，渲染速度达到 **400 FPS**。与 COLMAP-free 方法中表现最好的 MoSca 相比，PSNR 提升 0.60 dB，LPIPS 降低 0.016；与基于 COLMAP 的最优方法 4DGS 相比，PSNR 提升 0.47 dB。在渲染速度方面，SplineGS 分别是 RoDynRF 和 DynNeRF 的 **890 倍**和 **8000 倍**，证明了样条表示在实时渲染中的显著优势。

Table 1 还揭示了 COLMAP-free 与 COLMAP-based 方法之间的性能格局：SplineGS 作为 COLMAP-free 方法，不仅超越了所有同类方法，也优于依赖精确预计算相机参数的 4DGS、STGS 等方法。这表明联合优化相机参数与高斯属性的策略有效弥补了缺少 SfM 先验的劣势。

### 新视角与时间合成

在同时合成新视角和新时刻的任务中（Table 2），SplineGS 同样达到最优，PSNR 为 **25.92 dB**，LPIPS 为 **0.098**，tOF 为 0.703。该任务要求模型在未见过的相机视角和时间戳上生成图像，对运动建模的连续性和准确性提出了更高要求。SplineGS 的样条表示天然支持任意时刻的连续插值，使得其在该设定下优于基于离散帧建模的方法。

### 消融实验

Table 3 系统性地消融了 SplineGS 的三个核心设计：运动表示、损失函数和控制点剪枝。


![[assets/figures/papers/paper_list_l10_SplineGS_Robust_Motion_Adaptive_Spline_for_Real_Time_Dynamic_3D_Gaussian/figures/010_Table_3.jpg]]
*Table 3: Ablation studies. We ablate our framework and report the average results on the NVIDIA dataset with the same setting as Novel View Synthesis experiment in Sec. 5.1*

**运动表示消融 (Table 3-(a))**：将 MAS 替换为 MLP、多分辨率网格（HexPlane）、固定阶多项式或贝塞尔曲线后，PSNR 均出现显著下降。MLP 变形模型 PSNR 降至 24.12 dB，网格方法降至 26.28 dB，多项式降至 26.58 dB，贝塞尔曲线降至 26.83 dB。MAS 的 PSNR 为 27.21 dB，且变形延迟仅 5.63 ns，表明三次 Hermite 样条在表达能力和计算效率之间取得了最优平衡。贝塞尔曲线虽然也是样条类方法，但其控制点的全局影响特性导致局部运动编辑能力弱于分段 Hermite 样条。

**损失函数消融 (Table 3-(b))**：移除光度一致性损失 $\mathcal{L}_{\mathrm{pc}}$ 会导致 PSNR 从 27.21 dB 骤降至 **17.49 dB**，LPIPS 升至 0.853，这验证了在 COLMAP-free 设定下，光度一致性是约束相机参数和几何结构的关键信号。移除深度损失 $\mathcal{L}_{\mathrm{d}}$ 或掩码损失 $\mathcal{L}_{\mathrm{M}}$ 也会造成约 0.5–1.0 dB 的 PSNR 下降，表明多模态监督的互补性。

**控制点剪枝消融 (Table 3-(c))**：固定控制点数 $N_c=4$ 时 PSNR 为 26.79 dB，$N_c=N_f$（即每帧一个控制点）时为 26.83 dB，而 MACP 自适应选择控制点数达到 27.21 dB。这说明过少的控制点无法充分描述复杂运动，过多的控制点则导致过拟合和计算冗余。MACP 以 5.63 ns 的变形延迟实现了最佳质量-效率权衡。

### MACP 有效性分析

Figure 8 的热力图和直方图展示了 MACP 对不同运动复杂度的自适应行为。在运动简单的区域（如静态背景），动态高斯的控制点数被剪枝至接近最小值；在运动复杂的区域（如快速移动的肢体），保留了更多控制点。这种运动自适应的控制点分配机制是 SplineGS 在保持高渲染质量的同时控制计算开销的关键。


![[assets/figures/papers/paper_list_l10_SplineGS_Robust_Motion_Adaptive_Spline_for_Real_Time_Dynamic_3D_Gaussian/figures/011_Figure_8.jpg]]
*Figure 8: Analysis of MACP’s Efficacy. (a) $N _ { c }$ Heatmaps as the averaged $N _ { c }$ values of dynamic 3D Gaussians and their corresponding rendered frames $\hat { I } _ { t }$ for ‘Balloon2’ and ‘Skating’ scenes. (b) Histograms of the number of control points ( $N _ { c }$ ) in percentages (%) of dynamic 3D Gaussians in two scenes*

### 运动跟踪可视化

Figure 6 通过 2D 像素轨迹可视化了动态高斯的运动建模能力。与 STGS 和 4DGS 相比，SplineGS 的 MAS 能够更准确地跟踪像素级运动轨迹，这归因于样条表示的连续性和控制点初始化的物理合理性。


![[assets/figures/papers/paper_list_l10_SplineGS_Robust_Motion_Adaptive_Spline_for_Real_Time_Dynamic_3D_Gaussian/figures/008_Figure_6.jpg]]
*Figure 6: Visual comparisons for motion tracking. We visualize 2D pixel tracks to analyze motions of dynamic 3D Gaussians*

### 内存占用

Table 4 比较了各方法的内存占用。SplineGS 在保持较少高斯总数（与 MoSca 相当）的同时实现了更高的渲染质量。MACP 通过减少控制点数量进一步压缩了动态高斯的存储开销。

### 失败模式与局限性

当输入单目视频帧存在运动模糊时，SplineGS 无法有效重建清晰的新视角图像（Figure 12）。根本原因在于当前框架未集成去模糊模块，模型会过拟合到模糊的训练帧，导致渲染结果中出现伪影。这一问题在快速运动场景的真实视频中尤为突出，需要将去模糊方法直接整合到联合优化流程中才能解决。

### 补充图表

![[assets/figures/papers/paper_list_l10_SplineGS_Robust_Motion_Adaptive_Spline_for_Real_Time_Dynamic_3D_Gaussian/figures/001_Figure.jpg]]
*Figure: horsejump-low, t=20 (Ours) (a) Visual comparison for novel view synthesis on the DAVIS dataset (b) Performance gain on the NVIDIA dataset*

![[assets/figures/papers/paper_list_l10_SplineGS_Robust_Motion_Adaptive_Spline_for_Real_Time_Dynamic_3D_Gaussian/figures/014_Figure_11.jpg]]
*Figure 11: Visual results of novel view synthesis at a specific time using the same STGS [21] models after optimization with (a) their original time-varying opacity and (b) timeindependent spatial opacity, respectively. Please note that we use their original time-varying opacity during training*

![[assets/figures/papers/paper_list_l10_SplineGS_Robust_Motion_Adaptive_Spline_for_Real_Time_Dynamic_3D_Gaussian/figures/022_Figure.jpg]]
*Figure: D3DGS [49] RoDynRF [27] STGS [21] SplineGS (Ours) DynNeRF[11]*

![[assets/figures/papers/paper_list_l10_SplineGS_Robust_Motion_Adaptive_Spline_for_Real_Time_Dynamic_3D_Gaussian/figures/004_Figure_3.jpg]]
*Figure 3: Visual comparisons for novel view synthesis on the NVIDIA dataset*

![[assets/figures/papers/paper_list_l10_SplineGS_Robust_Motion_Adaptive_Spline_for_Real_Time_Dynamic_3D_Gaussian/figures/005_Figure_4.jpg]]
*Figure 4: Visual comparisons for novel view synthesis on the DAVIS dataset*

![[assets/figures/papers/paper_list_l10_SplineGS_Robust_Motion_Adaptive_Spline_for_Real_Time_Dynamic_3D_Gaussian/figures/017_Figure_13.jpg]]
*Figure 13: Visual comparisons for novel view synthesis on the Jumping scene from the NVIDIA dataset*

![[assets/figures/papers/paper_list_l10_SplineGS_Robust_Motion_Adaptive_Spline_for_Real_Time_Dynamic_3D_Gaussian/figures/018_Figure_14.jpg]]
*Figure 14: Visual comparisons for novel view synthesis on the Playground scene from the NVIDIA dataset*

![[assets/figures/papers/paper_list_l10_SplineGS_Robust_Motion_Adaptive_Spline_for_Real_Time_Dynamic_3D_Gaussian/figures/019_Figure_15.jpg]]
*Figure 15: Visual comparisons for novel view synthesis on the Truck scene from the NVIDIA dataset*

![[assets/figures/papers/paper_list_l10_SplineGS_Robust_Motion_Adaptive_Spline_for_Real_Time_Dynamic_3D_Gaussian/figures/020_Figure_16.jpg]]
*Figure 16: Visual comparisons for novel view and time synthesis on the Balloon2 scene from the NVIDIA dataset*




## 定位与知识库关联

### 与现有动态3DGS方法的关系

SplineGS处于动态3D高斯泼溅（3DGS）方法谱系中，其核心目标是解决单目视频下无需COLMAP预处理的实时高质量动态场景重建。现有动态3DGS方法可按运动建模方式和相机参数依赖两个维度进行定位：

**运动建模维度。** 早期工作如**STGS**（Li et al., 2023）采用固定阶多项式描述高斯均值轨迹，灵活性受限于多项式阶数。**4DGS**（Yang et al., 2024）使用网格分解表示时空变形场，需大量参数覆盖复杂运动。更通用的方案如**Deformable 3DGS**（Wu et al., 2024）依赖MLP网络预测逐帧偏移，表达能力虽强但推理速度慢、易过拟合。SplineGS提出的运动自适应样条（MAS）以三次Hermite样条为核心，用少量可学习控制点精确描述每个动态高斯的连续运动轨迹，在表达力与效率之间取得关键平衡——Table 3-(a)的消融实验直接证实：MAS（PSNR 27.21）显著优于MLP变形（24.12）、网格变形、多项式变形和贝塞尔曲线变形等替代方案，同时变形计算延迟仅5.63 ns。

**相机参数维度。** 传统动态3DGS方法（STGS、4DGS等）严重依赖COLMAP预处理获取相机内外参，这一瓶颈在真实单目视频中尤为突出——DAVIS数据集上COLMAP对多数场景无法提供合理相机参数。SplineGS通过两阶段联合优化（预热阶段仅优化相机参数，主训练阶段联合优化高斯属性与相机参数）实现了COLMAP-free，其有效性由去除光度一致性损失L_pc后PSNR暴跌至17.49（Table 3-(b)）这一决定性证据支撑。在COLMAP-free方法谱系中，SplineGS优于动态NeRF的**RoDynRF**（Liu et al., 2023）和动态3DGS的**MoSca**（Lei et al., 2024），在NVIDIA数据集上以PSNR 27.21 vs. 26.61（MoSca）和25.38（RoDynRF）取得领先（Table 1）。

**控制点自适应维度。** 现有方法通常对所有动态高斯使用固定数量的控制参数（如STGS对所有高斯使用相同阶数的多项式）。SplineGS的运动自适应控制点剪枝（MACP）在训练中动态决定每个高斯的最佳控制点数——简单运动区域用更少控制点，复杂运动区域保留更多控制点（Figure 8热力图直观展示了这一自适应分布）。Table 3-(c)表明，MACP相较于固定控制点数（N_c=4或N_c=N_f）以更少的平均控制点数实现了更高PSNR（27.21 vs. 26.79/26.83），证明了自适应策略的优越性。

### 适用边界与局限

**适用场景。** SplineGS适用于单目视频输入下的动态场景新视角合成和新时空视角合成，在NVIDIA数据集的多对象动态场景（如Balloon、Skating等）上表现突出。其400 FPS的渲染速度使其具备实时应用潜力，显著优于基于NeRF的方法（DynNeRF约0.05 FPS，RoDynRF约0.45 FPS）。

**核心局限。** 当输入单目视频帧存在运动模糊时，SplineGS无法有效重建清晰的新视角图像（Figure 12）。这是因为方法未集成去模糊模块，优化过程可能过拟合到模糊训练帧，导致渲染结果出现伪影。这一局限源于方法假设输入帧清晰且运动可被样条准确描述——在快速运动或低光照场景中该假设不成立。

**对COLMAP失效场景的依赖性。** 虽然SplineGS不依赖COLMAP，但其相机参数估计依赖光度一致性和几何一致性损失。在纹理稀疏或运动剧烈的场景中，这些一致性约束可能不足以提供稳定监督，相机估计精度下降会级联影响重建质量。DAVIS数据集上的结果（Figure 1(a)）表明方法在此类场景下仍能工作，但定量评估受限于COLMAP真值的缺失。

### 开放问题

1. **联合去模糊与动态重建。** 如何将运动去模糊模块直接整合到SplineGS的优化流程中，建立联合去模糊与动态渲染的统一框架？这需要同时估计模糊核（或模糊帧的清晰对应）和动态高斯属性，可能涉及对渲染方程引入模糊建模，以及设计额外的清晰度先验损失。

2. **长视频的可扩展性。** MACP的样条简化算法（Eq. (7)-(8)）计算开销随帧数线性增长。对于长视频（数百帧以上），控制点剪枝效率和样条拟合精度之间的权衡需要更深入的研究，可能的方向包括分段样条或层次化控制点结构。

3. **动态场景分解的鲁棒性。** 当前方法依赖运动掩码（通过Dice loss监督）分离静态和动态高斯。在动态纹理丰富或静态区域存在光照变化的场景中，掩码预测的准确性可能下降，影响整体重建质量。如何在没有精确运动掩码标注的情况下实现更鲁棒的动静态分解仍需探索。

4. **相机轨迹先验的引入。** 当前相机参数估计完全从数据驱动，预热阶段仅使用光度与几何一致性。在极端运动或纯旋转场景中，引入惯性测量单元（IMU）等传感器先验或学习型单目深度估计的强约束，可能进一步提升相机估计的稳定性和重建精度。



## 原文 PDF

![[paperPDFs/CVPR_2025/SplineGS_Robust_Motion_Adaptive_Spline_for_Real_Time_Dynamic_3D_Gaussians_from_Monocular_Video.pdf]]
