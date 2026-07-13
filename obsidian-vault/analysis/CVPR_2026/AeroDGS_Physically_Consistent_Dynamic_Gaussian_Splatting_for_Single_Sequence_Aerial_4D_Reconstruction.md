---
title: "AeroDGS: Physically Consistent Dynamic Gaussian Splatting for Single-Sequence Aerial 4D Reconstruction"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/AeroDGS_Physically_Consistent_Dynamic_Gaussian_Splatting_for_Single_Sequence_Aerial_4D_Reconstruction.pdf
project_link: null
code_link: null
aliases:
- AeroDGS
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 引入物理先验（地面支撑、直立稳定性、轨迹平滑性）作为可微约束，将欠定姿态估计转化为物理一致的解。
primary_logic: 城市场景具有结构性规律，动态物体遵循地面接触、竖直对齐和连续运动等物理约束；将这些约束编码为可微损失，指导单目动态重建。
claims:
- AeroDGS在Aero4D和UAV3D数据集上均优于现有方法，尤其动态区域PSNR提升最高4dB。
- 消融实验证明物理约束（地面支撑、直立、轨迹平滑）对动态重建质量至关重要，移除任一项导致Dyn-PSNR下降。
- Monocular Geometry Lifting模块提供了可靠的场景几何初始化，使得后续物理优化可行。
- Aero4D Intersection-Night 上 PSNR / SSIM / LPIPS / Dyn-PSNR = 32.71 / 0.971 / 0.024 / 17.65
---

# AeroDGS: Physically Consistent Dynamic Gaussian Splatting for Single-Sequence Aerial 4D Reconstruction

> [!tip] 核心洞察
> 城市场景具有结构性规律，动态物体遵循地面接触、竖直对齐和连续运动等物理约束；将这些约束编码为可微损失，指导单目动态重建。

| 字段 | 内容 |
|------|------|
| 中文题名 | AeroDGS: 面向单序列航空4D重建的物理一致动态高斯泼溅 |
| 英文题名 | AeroDGS: Physically Consistent Dynamic Gaussian Splatting for Single-Sequence Aerial 4D Reconstruction |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2602.22376) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | AeroDGS |
| Dataset | Aero4D Intersection-Night, Aero4D Downtown-High, Aero4D Intersection-Day, Synthetic UAV3D |

> [!tip] 效果简介
> - Aero4D Intersection-Night 上，PSNR / SSIM / LPIPS / Dyn-PSNR 32.71 / 0.971 / 0.024 / 17.65 vs 多种SOTA方法（见表1） (动态区域Dyn-PSNR最高提升约4 dB)。
> - Aero4D Downtown-High 上，PSNR / SSIM / LPIPS / Dyn-PSNR 37.91 / 0.974 / 0.013 / 22.47 vs 多种SOTA方法 (动态区域Dyn-PSNR最高提升约4 dB)。
> - Aero4D Intersection-Day 上，PSNR / SSIM / LPIPS / Dyn-PSNR 34.84 / 0.971 / 0.018 / 21.75 vs 多种SOTA方法 (动态区域Dyn-PSNR最高提升约4 dB)。

## 概要

**研究问题**：从单目航空视频实现动态城市场景的4D重建，面临深度模糊与运动估计不稳定的根本性挑战。无人机俯拍视角下，动态物体在图像中占据像素极少、位移幅度大，传统依赖多视图几何或预训练先验的方法难以准确恢复其三维运动，导致单目4D重建高度病态。

**核心方法**：AeroDGS提出一种物理引导的动态高斯泼溅框架，将城市场景的结构化先验编码为可微约束，从而将欠定的单目姿态估计问题转化为物理一致的解。框架包含两个关键模块：**Monocular Geometry Lifting** 通过零样本深度估计、尺度对齐与实例跟踪，从单序列恢复稠密场景几何并初始化动态物体；**Physics-Guided Optimization** 引入地面支撑、直立稳定性与轨迹平滑性三个可微正则化项，约束动态物体的运动自由度，消解单目深度歧义。

**方法定位**：现有动态场景重建方法（如 **4DGS** (Wu et al., CVPR 2024)、**Dynamic 3D Gaussian Fields** (Fischer et al., NeurIPS 2024)、**CoDA-4DGS** (Song et al., ICCV 2025) 等）主要面向地面视角或自动驾驶场景，依赖多视图几何约束或预训练运动先验，难以适配单目航空视频的极端视角与尺度条件。AeroDGS首次将物理先验作为核心优化驱动力引入动态高斯泼溅，开辟了单目航空4D重建的新范式。

**主要结果**：在真实数据集Aero4D与合成数据集UAV3D上，AeroDGS均显著优于现有方法，尤其动态区域PSNR最高提升约4 dB。消融实验证实，三个物理约束对动态重建质量至关重要，移除任一项均导致Dyn-PSNR下降。



**应用场景与核心矛盾** 无人机航拍是城市监测、交通分析和应急响应的关键感知手段。从单目航空视频中重建动态城市场景的4D表示（3D几何+时间），能够支撑自由视角渲染、场景编辑和时空分析等下游任务。然而，这一任务面临根本性的病态挑战：单目航空视角下，动态物体（如车辆）在图像中占据极小像素面积，且伴随大幅位移，导致深度估计严重模糊、运动轨迹难以稳定恢复。传统依赖多视图几何或预训练先验的方法在此类场景中极易失效，单目4D重建高度欠定。

**现有方法缺口** 当前动态场景重建方法主要分为两类。一类基于动态高斯泼溅的通用框架，如**4DGS**（Wu et al., CVPR 2024）和**Dynamic 3D Gaussian Fields**（Fischer et al., NeurIPS 2024），它们依赖多视图一致性或稠密时序观测来解耦动静结构，但在单目航空场景下因缺乏有效几何约束而性能骤降。另一类面向自动驾驶场景的方法，如**CoDA-4DGS**（Song et al., ICCV 2025）和**DeGauss**（Wang et al., ICCV 2025），假设地面平面已知或相机运动平滑，这些先验在无人机自由飞行、视角大幅变化的条件下不再成立。此外，**Uni4D**（Yao et al., CVPR 2025）等前馈模型虽能快速推理，但在域外航空数据上泛化能力有限。上述方法均未显式利用城市场景的结构化物理规律来约束动态物体的运动自由度，导致重建结果出现漂浮、倾斜或抖动等非物理伪影。

**核心动机与洞察** 城市场景中的动态物体（车辆）遵循可归纳的物理规律：它们始终与地面保持接触（地面支撑）、竖直方向对齐于重力方向（直立稳定性）、运动轨迹连续平滑（轨迹平滑性）。这些约束在物理世界中普遍成立，但在纯数据驱动的单目重建流程中被忽略。AeroDGS的核心动机是将上述物理先验编码为可微损失函数，嵌入到高斯泼溅的优化过程中，从而将原本欠定的单目姿态估计问题转化为物理一致的确定性求解。这一思路将场景结构规律转化为正则化信号，为单目航空4D重建提供了新的范式。



## 核心方法与创新机理

AeroDGS的核心创新在于将城市场景的结构化物理先验编码为可微约束，解决了单目航空视频4D重建中的根本性病态问题。与现有方法依赖多视图几何或预训练运动先验不同，AeroDGS通过三个紧密耦合的机制实现了物理一致的动态重建。

### 单目几何提升：从深度模糊到可靠初始化

传统SfM+MVS流程在航空场景中产生稀疏几何，且完全缺失动态物体。AeroDGS的**Monocular Geometry Lifting**模块（Sec. 3.2）从根本上改变了这一局面：它利用零样本深度估计获取每帧稠密深度，通过全局尺度对齐校正单目深度的尺度模糊，并结合2D实例跟踪分离动态前景。反投影公式

$$X_{t}(x) = \Pi^{-1}(x, \tilde{D}_{t}(x), K)$$

将校正后的深度转化为三维空间中的几何种子，为后续动态优化提供了稠密的地面估计和初始化的动态实例。这一模块是整个方法可行的前提——没有可靠的场景几何，后续物理约束将失去参照基准。

### 物理引导优化：将欠定问题转化为约束求解

单目航空视频中，动态物体因单视角几何和微小图像足迹而存在严重的3D位置与姿态不确定性（Fig. 3a）。AeroDGS将这一欠定估计问题转化为物理约束下的可微优化，引入三个互补的正则化项：

- **地面支撑约束**（Eq. 9）：强制动态物体中心沿视线方向贴近估计的局部地平面，防止物体漂浮或陷入地面。损失函数 $\mathcal{L}_{\mathrm{support}} = \mathbb{E}_{o,t} [ \psi( \mathbf{r}_{o,t}^{\top} ( \mathbf{c}_{o,t} - \hat{\mathbf{c}}_{o,t}^{g} ) ) ]$ 通过鲁棒核函数 $\psi$ 允许微小偏差，适应地面估计的不完美。

- **直立稳定性约束**（Eq. 10）：$\mathcal{L}_{\mathrm{upright}} = \mathbb{E}_{o,t} [ 1 - | \mathbf{u}_{o,t} \cdot \mathbf{v}_{o,t} | ]$ 使物体垂直轴与重力方向对齐，消除非物理旋转。这对车辆等刚体尤为关键，因为单目观测无法区分物体旋转与透视形变。

- **轨迹平滑性约束**（Eq. 11）：$\mathcal{L}_{\mathrm{traj}} = \mathbb{E}_{o,t} [ \| \mathbf{c}_{o,t+1} - 2 \mathbf{c}_{o,t} + \mathbf{c}_{o,t-1} \|_{2}^{2} ]$ 采用二阶差分惩罚运动加速度，强制连续无跳跃的轨迹，抑制单帧歧义导致的抖动。

这三个约束的协同作用将原本模糊的图像线索转化为物理一致的单一解（Fig. 3e），其有效性在消融实验中得到严格验证：移除任一项均导致动态区域PSNR下降（Table 3）。

### 连续外观场：超越独立球谐函数

与3DGS中每个高斯独立建模球谐函数参数不同，AeroDGS采用**共享的连续外观场**（Eq. 2）：

$$A_{i} = f_{\phi}(\mu_{i}, d, t, e_{o})$$

该场融合空间哈希编码、方向球谐基和时间正弦嵌入，以实例嵌入 $e_{o}$ 区分不同动态物体。这一设计不仅减少了内存开销，更重要的是增强了时序外观一致性——外观变化由连续函数而非离散参数控制，避免了逐帧独立优化导致的闪烁伪影。

### 与现有方法的本质差异

现有动态高斯泼溅方法在单目航空场景中的失败根源在于其运动估计策略不适用于该场景的病态特性：**Dynamic 3D Gaussian Fields**（Fischer et al., NeurIPS 2024）依赖多视图一致性，**4DGS**（Wu et al., CVPR 2024）和**CoDA-4DGS**（Song et al., ICCV 2025）面向自动驾驶场景假设了更丰富的观测条件，**Uni4D**（Yao et al., CVPR 2025）的前馈先验在航空视角下泛化不足。AeroDGS的关键突破在于认识到城市场景的结构化规律——车辆接触地面、保持竖直、连续运动——并显式地将这些规律编码为可微正则化，而非依赖数据驱动的隐式先验。这一设计哲学使其在动态区域取得最高4 dB的PSNR提升（Table 1, Table 2），证明了物理约束在解决单目动态重建病态性方面的核心作用。



AeroDGS 以单目航空视频为输入，输出物理一致的动态 4D 场景模型。其核心挑战在于：单视角观测下，动态物体在图像中占据的像素面积小、位移幅度大，导致深度估计与运动恢复高度病态。AeroDGS 通过将城市场景的结构化先验（地面支撑、直立稳定、轨迹平滑）编码为可微约束，将欠定的姿态估计问题转化为物理一致的求解过程。

### 框架总览

AeroDGS 由四个核心模块串联构成，形成从原始视频到可渲染 4D 表示的全流程：

1. **Monocular Geometry Lifting**（单目几何提升）：从单序列输入中恢复稠密场景几何、相机位姿及动态实例，为后续优化提供可靠的初始化基础。
2. **Gaussian Scene Representation**（高斯场景表示）：用统一的 3D 高斯原语表达静态背景与动态前景，支持连续外观场建模与可微渲染。
3. **Physics-Guided Optimization**（物理引导优化）：引入地面支撑、直立稳定性、轨迹平滑性三类可微物理约束，消解单目深度歧义，约束动态物体的六自由度运动。
4. **Differentiable Rasterization**（可微光栅化）：基于 3DGS 的可微光栅化管线，将场景高斯投影到图像平面，与输入帧进行光度比对。

上述模块的协作关系如 Figure 2 所示：Monocular Geometry Lifting 模块首先从单目航空序列中重建场景几何，将动态前景与静态背景分离；恢复的几何种子随后被组合到统一的高斯表示中联合优化；Physics-Guided Optimization 模块则在此过程中持续施加物理约束，确保动态物体的运动在物理上一致。

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2602_22376/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the proposed AeroDGS. Given a monocular aerial sequence, AeroDGS introduces a Monocular Geometry Lifting module to reconstruct scene geometry and separate dynamic foreground from static background. The recovered seeds are composed and jointly optimized in a unified Gaussian representation. A Physics-Guided Optimization module is proposed to resolve pose ambiguity of dynamic objects under monocular settings, ensuring physically consistent 4D reconstruction*

### 输入输出流

- **输入**：单目航空视频序列（单序列，无多视图或深度传感器辅助）。
- **中间产物**：经尺度对齐的稠密深度图、相机位姿估计、2D 实例跟踪结果、动态/静态几何种子。
- **输出**：由静态高斯集合 $\mathcal{G}_{\text{static}}$ 与各动态物体高斯集合 $\mathcal{G}_o$ 经时变刚体变换 $T'_{o,t}$ 组合而成的 4D 场景表示 $\mathcal{G}(t)$（Eq. 6），支持任意新视角的逼真渲染。

### 关键设计动机

与现有动态场景重建方法（如 **4DGS** (Wu et al., CVPR 2024)、**Dynamic 3D Gaussian Fields** (Fischer et al., NeurIPS 2024) 等）依赖多视图几何或预训练先验不同，AeroDGS 的物理引导优化模块是专门针对单目航空场景的欠定特性设计的。其核心洞察在于：城市场景中的动态物体（车辆等）遵循可预测的物理规律——它们在地面上行驶、保持竖直姿态、运动轨迹连续平滑。将这些规律形式化为可微损失函数，相当于为优化过程注入了强先验，将原本存在无穷多解的病态问题约束到物理合理的解空间内。

Figure 3 直观展示了这一机制的运作方式：在单目无人机视角下，动态物体因单视图几何和小图像足迹而呈现不确定的 3D 位置与朝向；物理引导约束分别强制地面接触（b）、竖直对齐（c）和轨迹平滑（d），最终将欠定姿态转化为单一的真实世界一致配置（e），实现准确的运动恢复与稳定的优化过程。

### 补充图表

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2602_22376/figures/001_Figure_1.jpg]]
*Figure 1: Summary. Given (a) a monocular aerial video of dynamic urban scenes, AeroDGS reconstructs a physically consistent 4D model by jointly integrating static structures and dynamic motion with Gaussian representation. The framework (b) performs photorealistic novelview synthesis with temporally coherent geometry and (c) achieves higher reconstruction fidelity compared to state-of-the-art methods. Please use Adobe Reader / PDF-XChange Editor to see animations*



AeroDGS 的核心架构由三个紧密耦合的模块构成，形成从几何初始化到物理约束优化的完整管线。

### 3.1 单目几何提升（Monocular Geometry Lifting）

该模块解决单目航空视频中深度信息缺失和动态物体几何未知的问题。给定单序列输入，模块首先利用零样本深度估计网络获取逐帧稠密深度图，然后通过尺度对齐将其与相机位姿估计统一到一致的度量空间。在此基础上，结合 2D 实例跟踪结果，模块能够区分静态背景与动态前景，并重建稠密的地平面几何。

**反投影公式**（Eq. 1）将像素映射到三维空间：

$$X_{t}(x) = \Pi^{-1}(x, \tilde{D}_{t}(x), K)$$

其中 $x$ 为像素坐标，$\tilde{D}_{t}(x)$ 为校正后的深度值，$K$ 为相机内参矩阵，$\Pi^{-1}$ 表示反投影操作。该步骤为后续高斯场景表示提供了可靠的几何种子点。

### 3.2 高斯场景表示（Gaussian Scene Representation）

场景采用 3D 高斯原语统一表示静态背景和动态前景。每个高斯原语包含位置、协方差、不透明度等几何属性，以及外观参数。

**外观场**（Eq. 2）通过连续函数建模，避免为每个高斯独立存储外观参数：

$$A_{i} = f_{\phi}(\mu_{i}, d, t, e_{o})$$

其中 $\mu_{i}$ 为高斯中心的空间位置，$d$ 为观察方向，$t$ 为时间索引，$e_{o}$ 为动态实例嵌入。函数 $f_{\phi}$ 融合空间哈希编码、方向球谐基和时间正弦嵌入，实现紧凑且时序一致的外观表示。

**动态物体轨迹**（Eq. 3）在 SE(3) 群上建模为连续六自由度运动：

$$T_{o,t} = \exp(\xi_{o}(t))$$

其中 $\xi_{o}(t)$ 为物体 $o$ 在时刻 $t$ 的李代数表示，$\exp$ 为指数映射。为处理姿态估计的残余不确定性，引入微小残差修正（Eq. 4）：

$$T'_{o,t} = \Delta T_{o,t} \cdot T_{o,t}$$

**世界空间变换**（Eq. 5）将规范空间的高斯中心变换到世界坐标系：

$$\mu_{i,t} = T'_{o,t} \circ \mu_{i}$$

**场景合成**（Eq. 6）将静态背景与所有动态物体的变换后高斯合并：

$$\mathcal{G}(t) = \mathcal{G}_{\mathrm{static}} \cup \bigcup_{o \in \mathcal{O}} T'_{o,t} \circ \mathcal{G}_{o}$$

### 3.3 物理引导优化（Physics-Guided Optimization）

针对单目设置下动态物体 3D 位置和朝向的高度不确定性，该模块引入三种可微物理约束，将欠定问题转化为物理一致的解。

**总损失函数**（Eq. 8）联合光度监督与物理正则化：

$$\mathcal{L} = \lambda_{\mathrm{photo}} \mathcal{L}_{\mathrm{photo}} + \lambda_{\mathrm{sup}} \mathcal{L}_{\mathrm{support}} + \lambda_{\mathrm{upr}} \mathcal{L}_{\mathrm{upright}} + \lambda_{\mathrm{traj}} \mathcal{L}_{\mathrm{traj}}$$

其中 $\mathcal{L}_{\mathrm{photo}}$ 为渲染图像与输入图像之间的光度损失，权重设置为 $\lambda_{\mathrm{photo}}=1.0$，$\lambda_{\mathrm{sup}}=0.05$，$\lambda_{\mathrm{upr}}=0.1$，$\lambda_{\mathrm{traj}}=0.02$。

**地面支撑损失**（Eq. 9）强制动态物体保持与估计地平面的接触：

$$\mathcal{L}_{\mathrm{support}} = \mathbb{E}_{o,t} \big[ \psi \big( \mathbf{r}_{o,t}^{\top} ( \mathbf{c}_{o,t} - \hat{\mathbf{c}}_{o,t}^{g} ) \big) \big]$$

其中 $\mathbf{c}_{o,t}$ 为物体中心，$\hat{\mathbf{c}}_{o,t}^{g}$ 为沿视线方向 $\mathbf{r}_{o,t}$ 投影到地平面的期望位置，$\psi$ 为惩罚函数。该约束防止物体漂浮或陷入地面。

**直立稳定性损失**（Eq. 10）保持物体垂直轴与重力方向对齐：

$$\mathcal{L}_{\mathrm{upright}} = \mathbb{E}_{o,t} [ 1 - | \mathbf{u}_{o,t} \cdot \mathbf{v}_{o,t} | ]$$

其中 $\mathbf{u}_{o,t}$ 为物体当前垂直轴方向，$\mathbf{v}_{o,t}$ 为参考重力方向。该约束抑制非物理的倾斜或翻转。

**轨迹平滑性损失**（Eq. 11）通过二阶差分约束运动连续性：

$$\mathcal{L}_{\mathrm{traj}} = \mathbb{E}_{o,t} \left[ \| \mathbf{c}_{o,t+1} - 2 \mathbf{c}_{o,t} + \mathbf{c}_{o,t-1} \|_{2}^{2} \right]$$

该约束惩罚轨迹中的突变和抖动，确保运动加速度连续。三种物理约束协同作用，将单目深度歧义转化为符合现实世界物理规律的唯一解。

### 补充图表

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2602_22376/figures/003_Figure_3.jpg]]
*Figure 3: Physics-Guided Optimization. (a) In monocular UAV scenes, dynamic objects exhibit uncertain 3D positions and orientations due to single-view geometry and small image footprints. AeroDGS introduces differentiable physics-guided constraints that enforce (b) ground support, maintaining consistent contact with the local plane; (c) upright stability, aligning the vertical axis with the reference direction; and (d) trajectory smoothness, ensuring continuous acceleration and temporally coherent motion. (e) These constraints transform under-determined poses into a single real-world-consistent configuration, yielding accurate motion recovery and stable optimization*



## 实验与关键发现

### 主要结果

AeroDGS在真实航空数据集Aero4D和合成数据集UAV3D上均取得最优性能，尤其在动态区域重建上优势显著。表1和表2汇总了与多个SOTA方法的定量对比，包括**Dynamic 3D Gaussian Fields**（Fischer et al., NeurIPS 2024）、**4DGS**（Wu et al., CVPR 2024）、**Uni4D**（Yao et al., CVPR 2025）、**CoDA-4DGS**（Song et al., ICCV 2025）和**BezierGS**（Ma et al., ICCV 2025）等。

在Aero4D的三个真实场景中，AeroDGS在全部指标上均优于基线方法。以Intersection-Night场景为例，AeroDGS取得PSNR 32.71、SSIM 0.971、LPIPS 0.024，动态区域Dyn-PSNR达17.65。在Downtown-High场景中，整体PSNR达37.91，Dyn-PSNR达22.47。在Intersection-Day场景中，PSNR为34.84，Dyn-PSNR为21.75。值得注意的是，在动态区域指标Dyn-PSNR上，AeroDGS相比次优方法最高提升约4 dB，验证了物理引导优化对动态物体重建的关键作用。

在合成UAV3D数据集Town03序列上，AeroDGS同样取得最优结果，PSNR 33.61、SSIM 0.972、LPIPS 0.026、Dyn-PSNR 15.60，在动态区域上显著领先于其他方法。合成场景提供了精确的真值，进一步证实了物理约束在单目动态重建中的有效性。

### 消融实验

消融实验系统验证了三个物理约束对动态重建质量的贡献，结果见表3。完整模型在Aero4D数据集上取得Dyn-PSNR 20.07，为最优配置。

移除地面支撑损失后，Dyn-PSNR降至19.23，下降0.84 dB。此时动态目标出现漂浮或陷入地面的现象，说明地面支撑约束有效消除了单目深度歧义导致的物体位置偏移。

移除直立稳定性损失后，Dyn-PSNR降至19.35，下降0.72 dB。物体出现非物理旋转，垂直轴偏离重力方向，表明直立约束对维持物体姿态合理性不可或缺。

移除轨迹平滑性损失后，Dyn-PSNR降至19.89，下降0.18 dB。运动轨迹出现明显抖动，二阶平滑约束的缺失导致时序一致性降低。

三个物理约束的独立移除均导致性能下降，且地面支撑和直立稳定性的贡献尤为显著，证明了它们之间的互补性——地面支撑约束位置，直立稳定性约束姿态，轨迹平滑性约束运动连贯性。

### 失败模式与局限性

尽管AeroDGS在整体上表现优异，但仍存在若干值得关注的失败模式：

**动静分类阈值问题**：当前方法使用3米位移阈值判断物体动静属性，这一硬阈值策略可能导致小范围运动物体被误判为静态，进而造成动态区域模糊。在交通场景中，缓慢移动的车辆可能因此被错误纳入静态背景，影响重建精度。

**小目标重建能力不足**：在高空俯拍视角下，行人等小目标的像素覆盖极少，当前方法无法有效重建。这源于单目几何提升模块对小目标的深度估计精度有限，以及物理约束在小目标上的作用减弱。

**物理先验的场景依赖性**：物理约束依赖场景先验（如地平面估计），在非平坦地形（如坡道、立交桥）或复杂城市结构下，地面支撑和直立稳定性约束可能退化，需要手动验证其鲁棒性。

### 关键图表结论

**表1（Aero4D数据集）**：AeroDGS在三种不同高度、光照条件和真实场景下均优于所有SOTA方法，动态区域Dyn-PSNR提升最高约4 dB，证明了物理引导优化在单目航空场景中的通用性。

**表2（UAV3D合成数据集）**：在具有精确真值的合成场景中，AeroDGS的动态区域性能显著领先，验证了物理约束的有效性不依赖特定数据分布。

**表3（消融实验）**：三个物理约束均对动态重建质量有正向贡献，地面支撑和直立稳定性贡献最大，三者互补构成完整的物理一致优化框架。

### 补充图表

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2602_22376/figures/004_Table_1.jpg]]
*Table 1: Novel-view synthesis results on Aero4D dataset. AeroDGS performs better than state-of-the-art methods under varying altitudes, illumination, and real-world conditions*

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2602_22376/figures/006_Table_2.jpg]]
*Table 2: Novel-view synthesis results on the challenging synthetic UAV3D [49] dataset. AeroDGS outperforms the state of the art, with notably better performance in dynamic scene regions*

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2602_22376/figures/005_Table_3.jpg]]
*Table 3: Ablation study. Novel view synthesis on the Aero4D dataset*

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2602_22376/figures/007_Figure_4.jpg]]
*Figure 4: Qualitative comparison of novel-view synthesis results. Our method achieves high overall reconstruction quality on both synthetic and real-world UAV datasets, maintaining high fidelity under diverse altitudes, illumination, and object motion patterns. Sharper structures and more consistent appearance are preserved compared with state-of-the-art methods. Yellow and red rectangular boxes highlight enlarged views of corresponding areas for visual comparison*



## 定位与知识库关联

### 任务定位：单序列航空4D重建

AeroDGS解决的核心问题是**单目航空视频的动态4D重建**——仅从一段无人机拍摄的城市场景视频中，同时恢复静态背景的稠密几何、动态物体的时空轨迹，并支持自由视角的照片级新视图合成。这一问题高度病态：单目观测下深度歧义严重，无人机高空视角使得动态物体（如车辆）在图像中占据像素极少，运动幅度却可能很大，传统依赖多视图几何或预训练先验的方法在此场景下失效。

### 与现有方法的谱系关系

AeroDGS处于**动态高斯泼溅（Dynamic Gaussian Splatting）**和**物理先验驱动重建**两条技术路线的交汇点。其直接对比的基线方法包括：

**通用动态高斯泼溅基线。** **4DGS**（Wu et al., CVPR 2024）将3DGS扩展到时间维度，通过变形场建模场景运动，但依赖多视图输入来消解几何歧义。**Dynamic 3D Gaussian Fields**（Fischer et al., NeurIPS 2024）进一步引入动态高斯场表示，但在单目航空场景下仍面临深度估计不可靠的问题。AeroDGS与这些方法的核心差异在于：它不依赖多视图几何来约束运动，而是通过**物理引导优化**将欠定的单目姿态估计转化为物理一致的解。

**动态分解与轨迹建模方法。** **DeGauss**（Wang et al., ICCV 2025）和**CoDA-4DGS**（Song et al., ICCV 2025）分别针对动静态分解和自动驾驶场景进行动态重建，但均假设地面视角或较近距离的观测，动态物体在图像中占据足够像素以支撑可靠的几何推断。**BezierGS**（Ma et al., ICCV 2025）使用贝塞尔曲线建模连续运动轨迹，与AeroDGS的SE(3)样条轨迹在数学形式上有相似之处，但缺少物理约束来正则化单目条件下的姿态估计。

**前馈单视频方法。** **Uni4D**（Yao et al., CVPR 2025）是前馈式单视频4D重建模型，通过大规模预训练学习运动先验，但在域外场景（如航空视角）的泛化能力有限。AeroDGS采用per-scene优化的范式，通过场景特定的物理约束弥补数据驱动的先验不足。

### 核心差异点：物理先验作为可微正则化

AeroDGS的方法论创新在于将**城市场景的结构性规律**编码为可微损失函数，直接作用于动态物体的姿态优化。这一设计将原本高度欠定的单目运动估计问题转化为受物理约束的优化问题：

- **地面支撑约束**（Eq. 9）强制动态物体中心沿视线方向贴近估计的地面投影，防止物体漂浮或陷入地面——这是单目深度歧义最直接的物理化解方式。
- **直立稳定性约束**（Eq. 10）使物体垂直轴与重力方向对齐，消除单目观测下常见的非物理旋转——这一约束利用了城市场景中绝大多数动态物体（车辆、行人）保持直立的事实。
- **轨迹平滑性约束**（Eq. 11）通过二阶差分正则化强制运动轨迹连续无跳跃，补偿单帧观测的信息不足。

这三个约束的**互补性**已在消融实验中验证：移除任一项均导致动态区域PSNR显著下降（Table 3），完整模型取得最佳Dyn-PSNR 20.07。

### 适用边界与局限

**适用场景。** AeroDGS在以下条件下表现最佳：(1) 城市场景，存在可估计的地平面；(2) 动态物体主要为刚体（车辆），遵循地面接触和直立运动规律；(3) 场景光照相对稳定，无剧烈变化。在Aero4D和UAV3D数据集上，动态区域PSNR最高提升约4 dB（Table 1, Table 2），证明了物理约束在目标场景中的有效性。

**已知局限。** 论文明确指出的局限性包括：

1. **动静分类策略粗糙。** 当前使用3米位移阈值判断物体动静状态，可能将小范围运动物体误判为静态，导致动态区域模糊。这一阈值缺乏场景自适应性。
2. **极小目标重建失败。** 高空俯拍下行人像素覆盖极少，当前方法无法恢复其几何与运动，限制了在人群监控等场景的应用。
3. **物理约束的脆弱性。** 地面支撑和直立稳定性依赖于场景先验（如地面估计的准确性），在非平坦地形（如坡道、立交桥）或复杂城市结构下可能退化。论文未提供这些条件下的鲁棒性分析。

### 开放问题

从当前工作出发，以下问题值得进一步探索：

1. **自适应物理约束强度。** 当前物理损失的权重（$\lambda_{\text{sup}}=0.05$, $\lambda_{\text{upr}}=0.1$, $\lambda_{\text{traj}}=0.02$）为固定值。如何根据场景特性（如地面平坦度、物体类型）自适应调整约束强度，是提升泛化能力的关键。
2. **物理先验与学习先验的融合。** 能否将物理引导优化与基于学习的运动先验（如从大规模数据中习得的车辆运动模式）结合，在极端条件下（如部分遮挡、剧烈光照变化）提供更强的正则化？
3. **多物体遮挡与交互。** 当前方法独立处理每个动态实例，未显式建模物体间的遮挡关系和交互约束（如车辆跟驰、避让）。在密集交通场景中，这类交互可能成为重要的物理先验。
4. **多无人机协同与长时序扩展。** 单目观测的信息瓶颈可通过多无人机协同观测缓解，但多视角下的物理约束融合和时序一致性维护是新的挑战。



## 原文 PDF

![[paperPDFs/CVPR_2026/AeroDGS_Physically_Consistent_Dynamic_Gaussian_Splatting_for_Single_Sequence_Aerial_4D_Reconstruction.pdf]]
