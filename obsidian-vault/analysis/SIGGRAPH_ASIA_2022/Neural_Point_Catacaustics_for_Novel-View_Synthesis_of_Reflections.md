---
title: Neural Point Catacaustics for Novel-View Synthesis of Reflections
type: paper
paper_level: A
venue: SIGGRAPH ASIA
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_ASIA_2022/Neural_Point_Catacaustics_for_Novel_View_Synthesis_of_Reflections.pdf
project_link: null
code_link: null
aliases:
- NPC
- NPCNVSR
tags:
- SIGGRAPH_ASIA_2022
- topic/graphics_rendering_materials
core_operator: 通过引入可学习的神经扭曲场（Neural Warp Field），将反射点云显式地沿着反射轨迹移动，从而直接建模反射流（即拉格朗日法），使得反射能够随视角正确变化。
primary_logic: 将场景分解为静态主点云和动态反射点云，利用神经扭曲场学习反射点的焦散轨迹，实现了弯曲反射体的高质量、交互式新视角合成。
claims:
- 我们引入了一种新的基于点的表示，称为神经点焦散，用于弯曲反射体的新视角合成。
- 核心是一个神经扭曲场，用于建模反射的焦散轨迹，通过高效的点喷溅与神经渲染器相结合来渲染复杂的镜面效果。
- 我们的方法在定量上优于先前所有方法，且在5个场景上的SSIM达到0.9845，PSNR达到35.85，LPIPS降至0.0179。
- Compot, ConcaveBowl, HallwayLamp, SilverVase, CrazyBlade (平均) 上 SSIM↑ = 0.9845
---

# Neural Point Catacaustics for Novel-View Synthesis of Reflections

> [!tip] 核心洞察
> 将场景分解为静态主点云和动态反射点云，利用神经扭曲场学习反射点的焦散轨迹，实现了弯曲反射体的高质量、交互式新视角合成。

| 字段 | 内容 |
|------|------|
| 中文题名 | 神经点焦散：面向反射场景的新视角合成 |
| 英文题名 | Neural Point Catacaustics for Novel-View Synthesis of Reflections |
| 会议/期刊 | SIGGRAPH ASIA 2022 |
| Links | [paper](https://repo-sam.inria.fr/fungraph/neural_catacaustics/) |
| Topic | #topic/graphics_rendering_materials |
| Method | Neural Point Catacaustics |
| Dataset | Compot, ConcaveBowl, HallwayLamp, SilverVase, CrazyBlade |

> [!tip] 效果简介
> - Compot, ConcaveBowl, HallwayLamp, SilverVase, CrazyBlade (平均) 上，SSIM↑ 0.9845 vs 0.9832 (Deep Blending) (+0.0013)。
> - 同上 上，PSNR↑ 35.8522 vs 35.6316 (Deep Blending) (+0.2206)；LPIPS↓ 0.0179 vs 0.0197 (Deep Blending) (-0.0018)。

## 概要

弯曲反射体（如金属碗、曲面灯罩）在新视角合成中构成核心难题：反射并非附着在固定空间位置，而是随着相机移动沿非线性焦散轨迹快速变化。传统神经渲染方法采用欧拉法——在固定点建模视角相关的颜色——难以捕捉这种高频反射流动，导致渲染模糊或伪影。

本文提出**神经点焦散（Neural Point Catacaustics）**，将场景分解为静态主点云和可变形反射点云，通过一个可学习的**神经扭曲场**显式地移动反射点，直接建模反射流（拉格朗日法）。反射点经EWA喷溅后，由神经渲染器解码为最终图像。

在5个真实场景上，本方法以SSIM 0.9845、PSNR 35.85、LPIPS 0.0179定量优于Deep Blending、MipNeRF、InstantNGP等基线，并支持反射跨视图跟踪、反射编辑、立体渲染等应用。方法定位于点基渲染与神经场景表示的交叉点，以双点云+扭曲场的架构突破了弯曲反射体新视角合成的瓶颈。

## 核心方法与创新机理

### 问题瓶颈与核心洞察

弯曲反射体（如金属碗、曲面镜）在新视角合成中面临一个独特挑战：反射内容并非附着在反射体表面，而是沿着一条称为**焦散轨迹（catacaustic trajectory）**的非线性路径在空间中移动。当相机视角变化时，反射点的位置会发生快速、非线性的位移，这种“反射流”（reflection flow）使得传统的欧拉法（Eulerian）表达——即在固定空间位置建模方向相关的颜色——难以准确捕捉反射的高频变化，导致渲染模糊或伪影。

本方法的核心洞察是采用**拉格朗日法（Lagrangian）**来建模反射：与其在固定位置学习各个视角下的外观，不如直接学习反射点随相机移动的轨迹，让反射点“流动”到正确的位置。这一思路将反射建模问题转化为一个可学习的**神经扭曲场（Neural Warp Field）**，从而实现了弯曲反射体的高质量新视角合成。

### 场景表示：双点云架构

方法将场景分解为两个独立的点云，分别承担不同的表达职责：

- **主点云（Primary Point Cloud）**：表示场景的漫反射和低频视角相关成分，在优化过程中保持**静态**。它负责捕捉场景的几何结构和非镜面外观，例如物体的纹理、颜色等。
- **反射点云（Reflection Point Cloud）**：表示高视角依赖的镜面反射细节，是**动态**的——其点位置会根据相机视角被神经扭曲场移动。反射点云初始化在用户界定的反射体体积边界表面上。

这一双点云设计构成了方法的核心**changed slot**：将传统点渲染方法中的单一静态点云替换为“静态主点云 + 可变形反射点云”的组合，使得场景的漫反射和镜面反射能够被分别建模和处理。

### 流水线模块与因果链

方法的完整流水线包含以下模块，按执行顺序形成因果链：

**1. 预处理：几何与相机标定**
- 对输入照片运行标准Structure-from-Motion（SfM）进行相机标定
- 使用Multi-View Stereo（MVS）方法提取稠密点云作为初始几何
- 用户在少量图像上粗略标记反射体区域，系统据此求解一个满足所有掩码约束的凸3D多面体，作为反射体体积（Reflection Volume）

**2. 点云初始化与优化**
- 主点云由MVS点云初始化，并在优化过程中通过分裂和剪枝操作进行自适应稠密化（densification）
- 反射点云在反射体体积边界表面上随机初始化，其位置在训练中通过神经扭曲场动态调整

**3. 神经扭曲场（Neural Warp Field）**
这是方法的核心模块，负责建模反射流。对于反射点云中的每个点 $\mathbf{p}$，给定相机位置 $\mathbf{c}$，扭曲场 $\mathcal{F}$ 预测其位移：

$$\mathbf{p}' = \mathbf{p} + \mathcal{F}(\mathbf{p}, \mathbf{c})$$

其中 $\mathcal{F}$ 由一个具有可训练参数 $\theta_{\mathrm{warp}}$ 的MLP实现。扭曲后的点 $\mathbf{p}'$ 被用于后续的喷溅渲染。这一模块使得反射点能够沿着焦散轨迹移动，从而在任意新视角下正确呈现反射内容。

**4. EWA喷溅渲染（EWA Splatting）**
将主点云和扭曲后的反射点云分别喷溅到图像平面，生成高维特征图。每个点的2D协方差矩阵由世界空间协方差经视图变换得到：

$$\boldsymbol{\Sigma} = h^{2} \mathbf{J} \mathbf{V} \mathbf{J}^{T} + \mu \nu \mathbf{I}$$

其中 $\mathbf{J}$ 是世界到视图的雅可比矩阵，$\mathbf{V}$ 是世界空间协方差，$h$ 和 $\mu \nu$ 控制足迹缩放和低通滤波。像素的特征值通过front-to-back alpha合成计算：

$$c = \sum_{i \in N} c_{i} \alpha_{i} \prod_{j=1}^{i-1} (1 - \alpha_{j})$$

累积不透明度 $\bar{o} = \prod_{j \in \mathcal{N}} (1 - \alpha_{j})$ 同时被保留，用于损失计算和环境贴图混合。

**5. 神经渲染器（Neural Renderer）**
喷溅生成的中间特征图（包括主点云RGB、反射点云RGB、掩码等缓冲区）被拼接后送入一个轻量级神经渲染网络，解码为最终的RGB图像。该网络负责填补点云渲染的间隙、细化细节，并融合两个点云的贡献。

**6. 损失函数与优化**
总损失由五项加权组成：

$$\mathcal{L} = \lambda_{\ell_1} \mathcal{L}_{\ell_1} + \lambda_{\mathrm{DSSIM}} \mathcal{L}_{\mathrm{DSSIM}} + \lambda_{\mathrm{p}} \mathcal{L}_{\mathrm{p}} + \lambda_{\mathrm{m}} \mathcal{L}_{\mathrm{m}} + \lambda_{m_{TV}} \mathcal{L}_{m_{TV}}$$

其中：
- $\mathcal{L}_{\ell_1}$ 和 $\mathcal{L}_{\mathrm{DSSIM}}$：标准图像重建损失
- $\mathcal{L}_{\mathrm{p}} = \| (\bar{o} - m_{\mathrm{RV}}) m_{\mathrm{RV}} \|_1$：反射体积惩罚项，鼓励反射点只出现在用户界定的反射体体积内
- $\mathcal{L}_{\mathrm{m}}$ 和 $\mathcal{L}_{m_{TV}}$：反射掩码正则化和掩码总变分损失，用于消除反射中可见的拍摄者

权重配置为 $\lambda_{\ell_1}=0.05$, $\lambda_{\mathrm{DSSIM}}=0.2$, $\lambda_{\mathrm{p}}=\lambda_{\mathrm{m}}=0.01$, $\lambda_{m_{TV}}=10^{-5}$。

### 训练与推理路径

**训练路径**：输入为一组标定相机姿态的照片。前向传播时，反射点云经神经扭曲场变形后与主点云一起喷溅，生成特征图经神经渲染器输出预测图像，与真值计算损失后反向传播更新所有可训练参数（包括主点云特征、反射点云特征与位置、扭曲场MLP权重、神经渲染器权重）。优化过程中，点云通过自适应稠密化逐步增加细节。

**推理路径**：给定新视角相机参数，反射点云通过训练好的扭曲场变形到对应位置，与主点云一起喷溅并经神经渲染器生成最终图像。由于采用点喷溅而非体积光线步进，渲染速度支持交互式应用。

### 关键因果机制

1. **扭曲场 → 反射流建模**：神经扭曲场将反射点的位置与相机位置显式关联，使得反射能够随视角变化而沿焦散轨迹流动，这是方法能够准确渲染弯曲反射体的根本原因。

2. **双点云分离 → 解耦漫反射与镜面反射**：主点云处理视角无关或低频视角相关的外观，反射点云专门处理高频镜面反射，避免了单一表示中两类信号的相互干扰。

3. **反射体积约束 → 稳定训练**：$\mathcal{L}_{\mathrm{p}}$ 惩罚项将反射点限制在用户界定的反射体体积内，防止反射点漂移到场景其他区域，是训练稳定性的关键保障。

4. **点喷溅 + 神经渲染 → 效率与质量平衡**：点喷溅提供快速的前向渲染，神经渲染器在此基础上填补间隙并提升图像质量，实现了交互式渲染速度与高保真度的统一。

![[assets/figures/papers/paper_list_l72_https_repo_sam_inria_fr_fungraph_neural_catacaustics/figures/005_Figure_5.jpg]]
*Figure 5: Overview of our method*

![[assets/figures/papers/paper_list_l72_https_repo_sam_inria_fr_fungraph_neural_catacaustics/figures/009_Figure_8.jpg]]
*Figure 8: Results of our method on Compost, ConcaveBowl, HallwayLamp, SilverVase: left is our rendering, right is the ground truth from images not in the input views. Note how our renderings faithfully capture reflections*

## 实验与关键发现

### 主结果：定量对比

在五个真实场景（Compot, ConcaveBowl, HallwayLamp, SilverVase, CrazyBlade）上，Neural Point Catacaustics 在全部三项指标上均优于先前方法。表1给出了各方法的平均定量结果。

| 方法 | SSIM↑ | PSNR↑ | LPIPS↓ |
|------|-------|-------|--------|
| MipNeRF (Barron et al. 2021) | 0.9555 | 30.0585 | 0.0544 |
| InstantNGP (Müller et al. 2022) | 0.9574 | 30.8496 | 0.0487 |
| Point-Based NR (Kopanas et al. 2021) | 0.9684 | 32.3685 | 0.0338 |
| Deep Blending (Hedman et al. 2018) | 0.9832 | 35.6316 | 0.0197 |
| **Neural Point Catacaustics (Ours)** | **0.9845** | **35.8522** | **0.0179** |

本方法相较最强基线 Deep Blending，SSIM 提升 +0.0013，PSNR 提升 +0.2206，LPIPS 降低 -0.0018。虽然 SSIM 和 LPIPS 上的绝对增益不大，但需注意 Deep Blending 在 300 张图像场景中已接近 GPU 显存上限，而本方法显存使用稳定在约 8 GB，且支持交互式渲染。

更重要的是，与基于神经辐射场的方法（MipNeRF, InstantNGP）相比，本方法在 SSIM 上领先约 0.027–0.029，PSNR 领先约 5.0–5.8 dB，LPIPS 降低约 0.030–0.037。这一显著差距源于弯曲反射体的本质困难：欧拉法在固定空间位置建模视角相关颜色，无法捕捉反射沿非线性焦散轨迹的快速流动，导致渲染模糊和伪影。本方法通过拉格朗日法显式建模反射流，从根本上解决了该问题。

所有方法均使用相同的输入图像和相机姿态，在与输入视图不同的独立路径上进行评估，训练和渲染分辨率统一为 1000×666。

### 消融实验

表2给出了在 Compot 场景上的消融结果，系统性地验证了各核心组件的因果贡献。

| 消融变体 | SSIM↑ | 关键发现 |
|----------|-------|----------|
| Full Model | **0.9745** | 完整模型 |
| Primary-Only | 0.9689 | 仅使用主点云，移除反射点云 |
| No-Densification | 0.9727 | 不进行反射点云稠密化 |
| Half-Warp-MLP | 0.9690 | 神经扭曲场 MLP 容量减半 |
| No-LDSSIM | 0.9741 | 移除 DSSIM 损失项 |
| No-LmTV | 0.9731 | 移除掩码 TV 损失项 |

**Primary-Only** 消融（SSIM 降至 0.9689）直接验证了反射点云的必要性。仅使用主点云时，模型无法捕捉镜面反射的移动——反射细节在视角变化时要么消失，要么停留在错误位置。这从反面证明了双点云分解的核心设计：静态主点云负责漫反射和低频场景结构，可变形反射点云专门承载高频反射流。

**Half-Warp-MLP** 消融（SSIM 降至 0.9690）是最具因果诊断力的实验之一。将神经扭曲场的 MLP 容量减半后，模型无法准确学习反射点随相机移动的焦散轨迹，导致反射区域出现严重模糊。这表明弯曲反射体的反射流确实是一个高复杂度的函数——它需要足够的网络容量来编码反射点位置与相机位置之间的非线性映射关系。该消融直接支持了核心主张：神经扭曲场是建模焦散轨迹的关键机制。

**No-Densification** 消融（SSIM 降至 0.9727）揭示了反射点云自适应稠密化的重要性。弯曲反射体会导致反射图像出现拉伸和压缩，初始均匀分布的点云无法覆盖所有反射细节。通过基于梯度的稠密化策略，模型在反射变化剧烈的区域增加点密度，从而准确重建高频镜面效果。

**No-LDSSIM** 和 **No-LmTV** 消融分别验证了 DSSIM 感知损失和掩码 TV 正则化的作用。移除 DSSIM 损失后，模型倾向于产生更平滑但细节缺失的渲染；移除掩码 TV 损失后，反射区域可能出现不连续的伪影。两者的定量影响相对较小（SSIM 下降约 0.0004–0.0014），但定性上对“消除反射中拍摄者自身影像”的效果有显著贡献——掩码损失引导反射点云聚焦于反射体区域，避免将拍摄者等非反射内容错误建模为反射。

### 定性分析与应用验证

定性结果（Fig. 8）展示了本方法在四个场景上与真值的对比：渲染结果忠实地再现了弯曲反射体上的复杂镜面效果，包括反射图像的拉伸、压缩和扭曲。在 ConcaveBowl 场景中，碗内壁的反射随视角变化呈现明显的非线性位移，本方法准确捕捉了这一流动，而基线方法则出现模糊或位置偏差。

本方法的拉格朗日建模带来了超越渲染质量的结构性优势：

- **反射跨视图对应**（Fig. 9）：神经扭曲场天然建立了反射点在不同视图间的稠密对应关系。即使在反射发生严重变形的情况下，仍可准确追踪同一反射特征的位置变化。这是欧拉法无法提供的——欧拉法在每个空间位置独立建模外观，不包含跨视图的几何对应信息。

![[assets/figures/papers/paper_list_l72_https_repo_sam_inria_fr_fungraph_neural_catacaustics/figures/010_Figure_9.jpg]]
*Figure 9: Our neural warpfield formulation naturally establishes correspondences of reflections across views, allowing to track reflections also in the presence of severe deformations. Example correspondences are marked as colored dots; please also refer to the supplemental video*

- **反射编辑**（Fig. 10）：由于反射点云与主点云显式分离，用户可以独立操纵反射内容。例如，改变反射对应的虚拟相机视角，实现对反射图像的放大或平移，而不影响场景其余部分。

![[assets/figures/papers/paper_list_l72_https_repo_sam_inria_fr_fungraph_neural_catacaustics/figures/012_Figure_10.jpg]]
*Figure 10: Reflection editing. (a) Original rendering. (b) Edited reflection, magnifying the right part of the table. The edited reflections correspond to a camera to the left of the primary view camera*

- **场景编辑**（Fig. 11）：显式的点云表示允许克隆反射点云和部分主点云，实现场景元素的复制和重新布局。

- **舒适立体渲染**（Fig. 12）：弯曲反射体常导致双眼视差不一致，引起视觉不适。本方法允许显式修改反射的视差，生成舒适的立体图像对。

![[assets/figures/papers/paper_list_l72_https_repo_sam_inria_fr_fungraph_neural_catacaustics/figures/015_Figure_12.jpg]]
*Figure 12: Our method supports comfortable stereo rendering of reflections. (a) Curved reflectors frequently result in uncomfortable binocular disparities (most prominent at the top left of the blade). (b) Our approach allows for an explicit modification of disparities, preventing visual discomfort. Use anaglyph glasses for stereo impression*

### 适用边界与限制

本方法依赖用户辅助界定反射体体积（Fig. 4）：用户需在少量图像上粗略标记反射区域，系统据此求解满足所有掩码约束的凸三维多面体。这一步骤引入了人工干预，对于包含多个分离反射体的复杂场景，用户工作量会相应增加。

![[assets/figures/papers/paper_list_l72_https_repo_sam_inria_fr_fungraph_neural_catacaustics/figures/004_Figure_4.jpg]]
*Figure 4: Bounding reflector volume: (a, b) The user is asked to paint rough masks marking the reflector in a small set (here 3) of images. (c) From these masks, we compute simple 2D bounding polylines (shown for c2 only). (d) Finally, we solve for the convex 3D polyhedron that satisfies all mask constraints*

反射点云初始化于反射体体积的边界表面，并依赖稠密化策略逐步覆盖反射细节。对于极端弯曲或具有尖锐边缘的反射体，初始点分布可能无法快速收敛到准确的焦散轨迹，需要更长的优化时间。

此外，本方法继承了点喷溅渲染的一般限制：当反射点密度不足或喷溅足迹估计不准确时，渲染可能出现孔洞或过度模糊。EWA 喷溅的协方差矩阵依赖于世界-视图雅可比和足迹缩放参数，这些参数在训练初期可能不稳定。

当前实验覆盖的五个场景均为室内桌面级场景，反射体以单个弯曲物体（碗、花瓶、灯罩等）为主。对于包含多个相互反射的复杂场景（如镜面相互映照），方法的有效性尚待验证。

## 定位与知识库关联

**核心改变的 Slot：从欧拉法到拉格朗日法的反射建模范式**

本工作在场景表示与反射建模两个 slot 上做出了根本性改变。在场景表示 slot，基线方法（如 **Point-Based NR** (Kopanas et al., 2021)、**MipNeRF** (Barron et al., 2021)、**InstantNGP** (Müller et al., 2022)）均采用单一静态表示——无论是以点云还是隐式神经场形式——所有外观信息包括镜面反射都被编码在固定空间位置的方向相关函数中。本方法将这一 slot 替换为**双点云架构**：一个静态主点云负责漫反射与低频视角相关外观，一个可变形反射点云专门承载高频镜面反射。这一拆分的因果意义在于，反射点云可以独立于场景几何被移动，从而为后续的拉格朗日反射流建模提供了结构前提。

在反射建模 slot，这是本工作最关键的改变。所有对比基线——包括神经辐射场类方法（MipNeRF, InstantNGP）和基于点的方法（Point-Based NR）——均采用**欧拉法**范式：在固定空间位置评估外观随视角方向的变化。这种范式对于弯曲反射体存在根本性困难：反射虚像的位置本身随相机移动而沿焦散轨迹快速变化，欧拉法需要每个表面点学习一个高维的方向相关函数来“记住”反射何时出现、何时消失，这不仅导致学习困难，更在本质上无法捕捉反射的连续流动。**Deep Blending** (Hedman et al., 2018) 虽然通过视角相关的图像混合在一定程度上缓解了该问题（也是定量上最接近本方法的基线），但其本质上仍是在图像空间进行欧拉式的视角相关插值，缺乏对反射几何流动的显式建模。

本方法将这一 slot 替换为**拉格朗日法**：通过神经扭曲场 $\mathcal{F}(\mathbf{p}, \mathbf{c})$ 直接学习反射点 $\mathbf{p}$ 随相机位置 $\mathbf{c}$ 的位移轨迹。这意味着反射内容只需被存储一次，其在不同视角下的位置变化由扭曲场显式跟踪。这一改变的因果机制在于：拉格朗日法将“反射随视角变化”这一复杂的外观建模问题，转化为“反射点随相机移动”这一几何配准问题，后者对于神经网络而言是更为结构化的学习任务。扭曲场的输出直接决定了反射点在喷溅时的空间位置，使得反射的变形、位移、出现与消失自然地由点的集体运动产生，而非由每个点独立学习的高维外观函数拟合。

**知识库挂载点：神经渲染中的动态场景表示与基于点的渲染**

本工作在知识库中的挂载位置位于两个研究方向的交叉点。第一个方向是**基于点的神经渲染**，特别是 **Point-Based NR** (Kopanas et al., 2021) 建立的点喷溅+神经解码器范式。本工作继承了该范式的核心组件——EWA 喷溅、前向后 alpha 混合、以及将高维特征图输入神经渲染网络——但将其从静态场景扩展到包含动态反射点的混合场景。第二个方向是**动态场景的神经表示**，特别是那些引入变形场来处理非刚性运动的神经辐射场方法。本工作的神经扭曲场在概念上与这些变形场相似，但应用于一个不同的物理动机：不是建模物体自身的非刚性变形，而是建模反射虚像在焦散面上的轨迹，这一轨迹由弯曲反射体的几何光学决定。

值得注意的知识边界是：本工作的拉格朗日反射建模依赖于一个**用户辅助的反射体积界定**步骤（Fig. 4）。这与全自动的神经渲染方法（如 MipNeRF、InstantNGP）形成对比，后者不需要任何场景特定的先验信息。这一人工介入步骤既是本方法的适用边界——需要用户标注反射体区域——也是其能够有效运作的关键：反射体积提供了反射点云的初始化空间和优化约束（通过 $\mathcal{L}_{\mathrm{p}}$ 损失），使得扭曲场的学习有一个明确的几何范围。

**相对基线的本质差异与适用边界**

与 **MipNeRF** 和 **InstantNGP** 的本质差异不仅是渲染速度（点喷溅 vs. 体积光线步进），更在于对反射现象的建模能力。体积光线步进方法在弯曲反射体场景中面临双重困难：其一，反射虚像位于反射体后方，光线需要穿过反射体表面才能到达虚像位置，这与体积渲染的密度场假设冲突；其二，反射内容的高频特性要求极高的采样密度和网络容量。本方法的点表示天然避开了这些困难——反射点直接存在于反射体积内，无需光线穿越表面。

与 **Deep Blending** 的差异更为微妙。Deep Blending 在定量指标上与本方法接近（SSIM 仅差 0.0013），但其视角相关混合本质上是对输入图像的重组而非对反射物理的建模。这意味着当新视角与所有输入视角都有较大差异时，Deep Blending 的混合权重会趋于均匀，导致反射模糊。本方法的拉格朗日法通过扭曲场显式预测反射点的新位置，理论上可以在任意新视角下保持反射的清晰度，只要扭曲场能够泛化。

本方法的适用边界包括：(1) **需要用户标注反射体**，这对于包含多个分离反射体的复杂场景可能增加交互负担；(2) **反射点云初始化在反射体积表面**，对于反射体几何复杂（如凹面反射体产生多重反射）的场景，单一反射体积可能不足以覆盖所有反射轨迹；(3) **扭曲场 MLP 的容量**是关键瓶颈——消融实验表明减半的 MLP 容量（Half-Warp-MLP）导致 SSIM 从 0.9745 降至 0.9690，说明反射流的复杂度需要足够的网络表达能力；(4) **显存效率**是本方法的优势——约 8GB 的稳定显存使用，相比 Deep Blending 随图像数量线性增长的显存需求，使得本方法更适合处理包含大量输入图像的场景。

**后续启发与可迁移性**

本工作建立的“静态主表示+可变形辅助表示”架构具有超出反射场景的迁移潜力。任何具有可预测几何流动的视角相关现象——如折射、焦散光斑在地面上的投影、甚至动态场景中物体的镜面高光——都可以通过类似的范式建模：将流动的部分分离为独立的可变形点云，用神经网络学习其轨迹。神经扭曲场的形式 $\mathbf{p}' = \mathbf{p} + \mathcal{F}(\mathbf{p}, \mathbf{c})$ 提供了一个轻量但表达力强的流动建模接口，可以嵌入到其他基于点的渲染框架中。

此外，本工作揭示了一个更深层的原则：对于视角相关的外观建模，**将问题从“外观空间”转移到“几何空间”**——即从学习“在这个位置、这个方向看起来是什么颜色”转变为学习“这个内容在哪个位置被看到”——可能是一个通用的有效策略。这一原则对于未来研究在处理其他类型的非朗伯效应时具有指导意义。

## 原文 PDF

![[paperPDFs/SIGGRAPH_ASIA_2022/Neural_Point_Catacaustics_for_Novel_View_Synthesis_of_Reflections.pdf]]