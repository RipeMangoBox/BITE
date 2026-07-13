---
title: "RealCam-I2V: Real-World Image-to-Video Generation with Interactive Complex Camera Control"
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: paperPDFs/arxiv_2025/RealCam_I2V_Real_World_Image_to_Video_Generation_with_Interactive_Complex_Camera_Control.pdf
project_link: null
code_link: null
aliases:
- RI
- RealCam-I2V
tags:
- arxiv_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 将训练和推理中的相机参数从相对尺度对齐到公制尺度，并在扩散早期引入场景约束的噪声成形以引导布局。
primary_logic: 通过单目公制深度估计在预处理阶段重建3D场景，作为训练和推理的统一参考，既解决了尺度不一致问题，又提供了交互式轨迹绘制的界面，从而实现了高可控性的真实世界图像到视频生成。
claims:
- RealCam-I2V 在 RealEstate10K 数据集上显著超越所有对比方法，尤其在公制尺度 TransErr 上较 CamI2V 相对提升 32.24%。
- 公制场景尺度对齐（MSA）单独使 CameraCtrl* 的公制尺度 TransErr 从 5.5090 降至 3.8218，降幅 30.6%。
- 场景约束噪声成形（SNS）单独在基础 DynamiCrafter 上将 RotErr 从 3.3415 降至 1.5163，降幅 54.6%。
- RealEstate10K 上 RotErr ↓ = 0.3884
---

# RealCam-I2V: Real-World Image-to-Video Generation with Interactive Complex Camera Control

> [!tip] 核心洞察
> 通过单目公制深度估计在预处理阶段重建3D场景，作为训练和推理的统一参考，既解决了尺度不一致问题，又提供了交互式轨迹绘制的界面，从而实现了高可控性的真实世界图像到视频生成。

| 字段 | 内容 |
|------|------|
| 中文题名 | RealCam-I2V：真实世界图像到视频的交互式复杂相机控制生成 |
| 英文题名 | RealCam-I2V: Real-World Image-to-Video Generation with Interactive Complex Camera Control |
| 会议/期刊 | arXiv 2025 |
| Links | [paper](https://arxiv.org/abs/2502.10059) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | RealCam-I2V |
| Dataset | RealEstate10K |

> [!tip] 效果简介
> - RealEstate10K 上，RotErr ↓ 0.3884 vs CamI2V 0.4120 (-5.73%)；TransErr (Metric Scale) ↓ 2.2317 vs CamI2V 3.2934 (-32.24%)；FVD (StyleGAN) ↓ 45.460 vs CamI2V 53.361 (-14.81%)。

## 概要

从单张真实图像生成可控相机运动的视频，是视觉内容创作的核心需求。现有基于扩散模型的图像到视频（I2V）方法，如 **MotionCtrl**（Wang et al., SIGGRAPH 2024）、**CameraCtrl** 和 **CamI2V**（Zheng et al., arXiv 2024），虽能以相机轨迹为条件生成视频，却受困于一个根本性瓶颈：**训练时使用的相机参数均为相对尺度**（每个视频片段独立归一化），而真实世界应用要求公制尺度下的精确控制。这种尺度不一致导致模型无法学习物理一致的相机运动，同时用户因缺乏场景深度信息而难以精确绘制轨迹，严重制约了可用性。

**RealCam-I2V** 的核心洞察是：通过单目公制深度估计在预处理阶段重建 3D 场景，将其作为训练与推理的统一参考，可同时解决尺度不一致与交互可用性两大难题。具体而言，该方法引入了两个关键机制：

- **公制场景尺度对齐（Metric Scene-scale Alignment, MSA）**：利用 Depth Anything V2 预测输入图像的公制深度图，将 COLMAP 重建的相对尺度稀疏点云对齐到统一公制尺度，使训练与推理中的相机参数共享同一绝对参考系。
- **场景约束噪声成形（Scene-constrained Noise Shaping, SNS）**：在扩散早期（高噪声阶段），用交互式预览视频的干净潜变量覆盖选定区域，引导生成过程遵循用户预期的场景布局与相机运动。

在实验上，RealCam-I2V 在 RealEstate10K 数据集上显著超越所有对比方法：**公制尺度平移误差（TransErr）较 CamI2V 相对降低 32.24%**，旋转误差（RotErr）降低 5.73%，视频质量指标 FVD 降低 14.81%。消融实验进一步表明，MSA 单独可使 CameraCtrl 的公制尺度 TransErr 下降 30.6%，SNS 单独可使基础 DynamiCrafter 的 RotErr 下降 54.6%，两者组合达到最优。

在方法谱系上，RealCam-I2V 以 **DynamiCrafter**（Xing et al., arXiv 2023）为基础扩散主干，继承了 CameraCtrl 和 CamI2V 的 Plücker 嵌入与极线注意力等相机条件化策略，但通过尺度对齐与噪声成形两个即插即用模块，将相对尺度轨迹控制范式升级为公制尺度的真实世界可控生成，并额外支持循环视频、帧插值与场景过渡等多模式拼接。

### 问题背景

图像到视频（Image-to-Video, I2V）生成旨在从单张静态图像出发，合成一段具有时间连续性和视觉真实感的视频。随着扩散模型在图像和视频生成领域的突破性进展，I2V 的质量近年来取得了长足进步。然而，大多数现有方法将生成过程视为完全自动化的“黑箱”——用户提供一张图像和一段文本描述，模型输出视频，用户对镜头如何运动几乎没有控制权。在实际创作中，摄影师、导演和内容创作者需要精确控制相机的平移、旋转、变焦等运动，以传达特定的叙事意图和视觉节奏。因此，**可控相机运动**成为 I2V 生成从“能生成”走向“可创作”的关键瓶颈。

### 现有方法缺口

近年来，研究者开始探索将相机轨迹作为额外条件注入 I2V 扩散模型。代表性工作包括 **MotionCtrl**（Wang et al., SIGGRAPH 2024），利用 3×4 相机外参矩阵控制全局运动；**CameraCtrl** 和 **CamI2V**（Zheng et al., arXiv 2024）则引入 Plücker 嵌入和极线注意力机制，在相机轨迹跟随精度上取得了当时最优结果。

然而，这些方法面临一个根本性的障碍：**尺度不一致（scale inconsistency）**。现有方法在训练时使用从运动恢复结构（Structure-from-Motion, SfM）获得的相机参数，这些参数是**相对尺度**的——每个视频片段的场景尺度被独立归一化，不同片段之间的“一米”并不等价。如 Figure 3 所示，SfM 重建的点云（黄色）在不同帧之间尺度各异，而公制深度估计重建的点云（RGB 色）则具有统一且鲁棒的尺度。这种相对尺度训练导致模型无法学习物理上一致的相机运动：相同的相机外参变化在不同片段中可能对应截然不同的场景位移量，造成 Figure 4 所示的**相机轨迹歧义**。

更关键的是，这一尺度不一致问题在真实世界应用中会进一步放大。用户在实际使用时，无法得知场景的绝对尺度信息，因此难以精确绘制符合预期的相机轨迹。即便模型在相对尺度下表现良好，一旦部署到真实场景，用户给出的轨迹与训练分布之间存在不可逾越的尺度鸿沟，导致生成结果不可控、不可预测。这一“训练-推理尺度鸿沟”构成了现有相机可控 I2V 方法从实验室走向实际应用的核心障碍。

### 本文动机

针对上述问题，本文提出 **RealCam-I2V**，其核心动机是**将相机控制从相对尺度统一到公制尺度**，从而弥合训练与真实世界应用之间的尺度鸿沟。具体而言，RealCam-I2V 通过以下两个关键设计实现这一目标：

1. **公制场景尺度对齐（Metric Scene-scale Alignment, MSA）**：在训练阶段，利用单目公制深度估计（Depth Anything V2）为每个视频片段重建具有绝对尺度的 3D 场景，将 SfM 获得的相对尺度相机参数对齐到统一的公制尺度。这使得模型在训练时就能学习到物理上一致的相机-场景关系。

2. **交互式 3D 预览与场景约束噪声成形（Scene-constrained Noise Shaping, SNS）**：在推理阶段，同样通过公制深度估计为用户提供的参考图像重建 3D 场景，用户可以在其中自由绘制相机轨迹并实时获得预览视频。这一预览视频随后作为噪声成形的参考，在扩散早期的高噪声阶段引导生成过程，确保最终视频的布局和相机运动与用户期望一致。

通过将单目公制深度估计作为训练和推理的统一参考，RealCam-I2V 不仅解决了尺度不一致这一根本性问题，还为用户提供了直观的交互式轨迹绘制界面，使得高可控性的真实世界图像到视频生成成为可能。

## 核心方法与创新机理

RealCam-I2V 的核心创新并非提出全新的生成架构，而是**系统性地解决了相机可控图像到视频生成中两个相互纠缠的瓶颈**：尺度不一致与交互可用性。其 changed slots 直接对应这两个瓶颈的因果旋钮。

### 从相对尺度到公制尺度的训练范式转换

现有相机轨迹控制方法（如 **MotionCtrl** (Wang et al., SIGGRAPH 2024)、**CameraCtrl**、**CamI2V** (Zheng et al., arXiv 2024)）在训练时均采用**相对尺度**——每个视频片段的相机平移向量被独立归一化，使得模型学到的“移动一米”在不同场景中对应完全不同的像素位移量。这种尺度歧义从根本上阻碍了模型学习物理一致的相机运动（Figure 4），并导致真实世界应用中用户无法精确指定公制尺度的轨迹。

RealCam-I2V 的核心 changed slot 在于将相机参数的尺度基准从**相对尺度**切换为**公制尺度**。实现这一转换的关键是引入**单目公制深度估计**作为统一的中间参考系：

1. 利用 Depth Anything V2 的度量版本从参考图像 $I$ 预测公制深度图 $D(u,v) = f_{\mathrm{depth}}(I)$；
2. 通过相机内参矩阵 $K$ 将像素反投影到相机坐标系，获得场景的三维点云；
3. 将 COLMAP 重建的稀疏点云对齐到该公制点云，求解统一的尺度因子 $\alpha$；
4. 将训练数据中所有相对尺度的相机外参转换为公制尺度：$c_{\mathrm{cam}}^{\mathrm{metric}} = \begin{bmatrix} R & \alpha \cdot T \\ 0 & 1 \end{bmatrix}$。

这一转换使模型在训练阶段即学习公制尺度下的相机运动，推理时用户绘制的轨迹与训练数据共享同一尺度空间，从而消除了尺度不一致的根源。消融实验（Table 2）验证了该 changed slot 的独立贡献：仅将公制场景尺度对齐（MSA）应用于 CameraCtrl*，其公制尺度 TransErr 从 5.5090 降至 3.8218，降幅达 30.6%。

### 从黑箱生成到场景约束的噪声成形

传统扩散模型以标准高斯噪声 $\epsilon \sim \mathcal{N}(0, I)$ 初始化去噪过程，模型在完全随机的初始状态下逐步生成视频内容。这种方式下，即使提供了相机轨迹条件，模型在早期去噪阶段也难以建立场景布局与相机运动之间的全局一致性——用户无法预览生成结果，只能通过反复试错调整轨迹（Figure 5）。

RealCam-I2V 的第二个 changed slot 是将**标准噪声采样**替换为**场景约束噪声成形（Scene-constrained Noise Shaping, SNS）**。其运作机制如下：

1. 在推理预处理阶段，利用公制深度重建的三维场景，允许用户交互式绘制相机轨迹并实时渲染低分辨率预览视频 $z_{\mathrm{preview}}$；
2. 在扩散过程的高噪声阶段（$t > t_{\mathrm{NS}}$，经验阈值 $t_{\mathrm{NS}}$ 对应噪声水平约 0.9），将预览视频的干净潜变量与当前噪声潜变量按掩码 $m$ 混合：
   $$z_t = m \cdot (\alpha_t z_{\mathrm{preview}} + \sigma_t \epsilon) + (1 - m) \cdot z_t$$
3. 掩码 $m$ 仅覆盖预览视频中可见的像素区域，并通过离群点过滤（Figure 11）排除深度边缘的错误像素。

这一设计的因果逻辑在于：扩散模型的早期去噪阶段主要决定图像的**低频结构**（布局、相机运动轨迹），而后期阶段负责**高频细节**（纹理、动态物体）。SNS 通过在高噪声阶段注入场景约束的低频信息，引导模型建立正确的空间布局和相机运动，同时保留后期去噪的自由度以生成动态细节。消融实验（Table 2）表明，仅将 SNS 应用于基础 DynamiCrafter，RotErr 从 3.3415 降至 1.5163，降幅达 54.6%，证明了场景约束对相机控制精度的独立贡献。

### 两阶段协同的因果机制

MSA 与 SNS 并非独立运作，而是形成**两阶段协同**的因果链条：

- **MSA 提供尺度一致的训练基础**：若训练数据本身存在尺度歧义，即使推理时注入场景约束，模型也无法将公制轨迹映射为正确的像素位移。MSA 确保了模型参数空间本身具备公制尺度的相机运动表征能力。
- **SNS 在推理时注入场景先验**：在 MSA 训练的基础上，SNS 将用户期望的轨迹以预览视频的形式“锚定”到扩散过程中，进一步约束模型在正确尺度下生成符合轨迹的视频。

Table 2 的组合消融验证了这一协同效应：MSA 与 SNS 组合（即完整 RealCam-I2V）在全部相机控制指标和视频质量指标上均优于单独使用任一组件的配置，且相对于 CamI2V 在公制尺度 TransErr 上实现 32.24% 的相对提升（Table 1）。

### 交互范式的根本性改变

上述两个 changed slots 共同催生了交互范式的转变：从“绘制轨迹 → 等待生成 → 查看结果 → 重新调整”的**多轮试错**模式，转变为“在三维场景中实时预览 → 确认轨迹 → 一次生成”的**单轮交互**模式。这一转变的关键在于公制深度重建使得预览视频的相机运动与最终生成结果共享尺度空间，用户所见即所得，从根本上提升了系统的可用性。

RealCam-I2V 的整体流程围绕一个核心矛盾展开：现有相机轨迹可控的图像到视频（I2V）方法在训练时依赖**相对尺度**的相机参数，而真实世界的应用场景要求**公制尺度**下的精确控制。这一尺度不一致性构成了从“相对可控”到“公制可控”的关键瓶颈。为解决这一问题，RealCam-I2V 将单目公制深度估计作为预处理环节引入，在训练和推理两端建立统一的公制尺度参考系，从而将相机控制从相对空间迁移到物理世界。

### 训练与推理的双阶段对齐

框架的设计遵循“训练对齐尺度，推理构建场景”的原则，如 Figure 2 所示。训练阶段的核心操作是**公制场景尺度对齐（Metric Scene-scale Alignment, MSA）**：利用单目深度估计器（Depth Anything V2 的公制版本）对视频片段的关键帧进行深度预测，获得公制深度图 $D(u,v) = f_{\mathrm{depth}}(I)$，随后与 COLMAP 重建的稀疏点云进行尺度对齐，计算出统一的尺度因子 $\alpha$。该因子将原本逐片段独立归一化的相对平移向量转换为公制尺度的相机到世界变换矩阵：

![[assets/figures/papers/paper_list_l95_https_arxiv_org_abs_2502_10059/figures/002_Figure_2.jpg]]
*Figure 2: RealCam-I2V pipeline. For training, we align camera parameters from relative scale to metric scale. For inference, we use metric depth estimation to construct the point cloud for users to interactively draw the camera trajectory. Due to the metric scale alignment, the user-given camera trajectory in the 3D scene shares the same scene scale as those in real world*

$$c_{\mathrm{cam}}^{\mathrm{metric}} = \begin{bmatrix} R & \alpha \cdot T \\ 0 & 1 \end{bmatrix}$$

这一对齐操作使模型在训练时即学习公制尺度下的相机运动模式，从根本上消除了相对尺度训练带来的轨迹歧义（Figure 4）。推理阶段则反向利用这一对齐成果：对用户提供的单张参考图像进行公制深度估计，通过相机内参矩阵 $K$ 将像素反投影到三维空间 $\mathbf{p}_c = \mathbf{D}(u,v) \cdot K^{-1} \cdot [u, v, 1]^{\mathsf{T}}$，构建出与训练数据共享同一公制尺度的三维场景点云。用户在此重建场景中交互式绘制相机轨迹，系统实时渲染预览视频，实现了“所见即所得”的控制体验（Figure 5）。

### 场景约束噪声成形

为弥补预览视频与最终生成视频之间的质量差距，RealCam-I2V 引入了**场景约束噪声成形（Scene-constrained Noise Shaping, SNS）**。其核心思想是在扩散模型的早期去噪阶段（高噪声水平 $t > 0.9$），将预览视频中可见区域的干净潜变量特征注入到预测的 $\hat{z}_0$ 中：

$$z_t = m \cdot (\alpha_t z_{\mathrm{preview}} + \sigma_t \epsilon) + (1 - m) \cdot z_t$$

其中 $m$ 为可见性掩码。这一操作在低频层面引导生成结果的布局和相机运动，同时保留扩散模型在高频细节上的生成自由度，实现了相机可控性与视频动态性的平衡。实验表明，SNS 单独作用于基础模型 DynamiCrafter 时，即可将旋转误差 RotErr 从 3.3415 降至 1.5163（降幅 54.6%），验证了其在引导空间结构方面的有效性。

### 条件扩散模型与多模式生成

视频生成的核心是一个以公制尺度相机轨迹 $c_{\mathrm{cam}}$、文本描述 $c_{\mathrm{txt}}$ 和参考图像 $c_{\mathrm{img}}$ 为条件的扩散模型，其训练目标为标准的去噪重构损失：

$$\mathcal{L} = \mathbb{E}_{z, c_{\mathrm{txt}}, c_{\mathrm{img}}, c_{\mathrm{cam}}, \epsilon, t} \left[ \left\| \epsilon - \epsilon_{\theta} \left( z_t, c_{\mathrm{txt}}, c_{\mathrm{img}}, c_{\mathrm{cam}}, t \right) \right\|_2^2 \right]$$

前向扩散过程遵循 $z_t = \alpha_t z_0 + \sigma_t \epsilon$。在推理时，通过多模式拼接策略（Figure 8），框架仅需微小调整即可支持基本生成、帧插值、循环视频和视频延续四种任务模式，展现出良好的任务泛化性。

### 模块间因果链路

整个框架的因果链路可归纳为：**公制深度估计**为训练和推理提供统一的尺度锚点 → **MSA** 消除训练中的尺度歧义，使模型学习到物理一致的相机运动 → **交互式三维场景**将用户的绘制轨迹与训练尺度对齐，实现精确控制 → **SNS** 在扩散早期注入场景约束，平衡可控性与动态性。消融实验证实了这一链路的协同效应：MSA 与 SNS 组合使用达到最优，在所有相机控制指标和视频质量指标上均优于单独使用任一组件。

RealCam-I2V 的核心技术路线围绕一个关键瓶颈展开：现有基于相机轨迹的图像到视频（I2V）方法在训练时使用**相对尺度**的相机参数，而真实世界应用需要**公制尺度**，导致严重的尺度不一致问题。此外，用户缺乏场景深度信息，难以精确绘制相机轨迹。RealCam-I2V 通过两个核心模块——**公制场景尺度对齐（MSA）** 和 **场景约束噪声成形（SNS）**——在训练与推理两端协同解决上述问题。

### 条件视频扩散基础模型

RealCam-I2V 以 **DynamiCrafter**（Xing et al., arXiv 2023）为基础图像到视频生成模型，将其扩展为相机可控的扩散框架。模型以文本描述 $c_{\mathrm{txt}}$、参考图像 $c_{\mathrm{img}}$ 和相机轨迹条件 $c_{\mathrm{cam}}$ 为输入，训练目标为标准扩散重构损失：

$$\mathcal{L} = \mathbb{E}_{z, c_{\mathrm{txt}}, c_{\mathrm{img}}, c_{\mathrm{cam}}, \epsilon, t} \left[ \left\| \epsilon - \epsilon_{\theta} \left( z_t, c_{\mathrm{txt}}, c_{\mathrm{img}}, c_{\mathrm{cam}}, t \right) \right\|_2^2 \right] \tag{1}$$

其中潜变量 $z_t$ 由前向扩散过程生成：

$$z_t = \alpha_t z_0 + \sigma_t \epsilon \tag{2}$$

$\epsilon_{\theta}$ 为去噪网络，$t$ 为扩散时间步，$\alpha_t$ 和 $\sigma_t$ 为噪声调度参数。

### 公制场景尺度对齐（MSA）

**核心问题**：现有方法（如 **MotionCtrl**、**CameraCtrl**、**CamI2V**）在训练时将每个视频片段的相机平移向量独立归一化到相对尺度，导致模型无法学习物理上一致的相机运动——相同的相机位移在不同场景中对应截然不同的归一化平移量（Figure 4）。推理时，用户提供的公制尺度轨迹与训练分布不匹配，造成控制精度严重下降。

**解决方案**：MSA 在数据预处理阶段引入单目公制深度估计作为统一的尺度参考，将所有视频片段的相机参数对齐到同一公制尺度。

具体流程如下：

1. **公制深度估计**：利用 Depth Anything V2 的公制版本 $f_{\mathrm{depth}}$，对每个视频片段的参考图像 $I$ 预测公制深度图：

   $$D(u,v) = f_{\mathrm{depth}}(I)$$

2. **稀疏重建与尺度对齐**：对同一视频片段运行 COLMAP 进行运动恢复结构（SfM）重建，获得稀疏三维点云和相对尺度的相机位姿。通过将 SfM 稀疏点云与公制深度图反投影得到的密集点云进行配准，求解统一的尺度因子 $\alpha$。

3. **相机参数公制化**：利用尺度因子 $\alpha$ 将相对平移向量 $T$ 转换为公制尺度，构建公制相机到世界变换矩阵：

   $$c_{\mathrm{cam}}^{\mathrm{metric}} = \begin{bmatrix} R & \alpha \cdot T \\ 0 & 1 \end{bmatrix}$$

   其中 $R$ 为相机旋转矩阵，内参矩阵 $K$ 定义为：

   $$K = \begin{bmatrix} f_x & 0 & c_x \\ 0 & f_y & c_y \\ 0 & 0 & 1 \end{bmatrix}$$

   包含焦距 $f_x, f_y$ 和主点 $(c_x, c_y)$。

经过 MSA 处理后，所有训练视频的相机参数共享统一的公制尺度，模型得以学习物理上一致的相机运动规律。消融实验（Table 2）证实，仅添加 MSA 即可将 **CameraCtrl** 的公制尺度 TransErr 从 5.5090 降至 3.8218，降幅达 30.6%。

### 交互式轨迹绘制与预览渲染

在推理阶段，MSA 建立的公制深度图同时为用户提供了交互式轨迹绘制的三维场景基础：

1. **三维场景重建**：利用公制深度图 $D(u,v)$ 和内参矩阵 $K$，将参考图像的每个像素反投影到相机坐标系下的三维点：

   $$\mathbf{p}_c = \mathbf{D}(u,v) \cdot K^{-1} \cdot \begin{bmatrix} u \\ v \\ 1 \end{bmatrix}$$

   由此构建场景的密集三维点云。

2. **交互式轨迹绘制**：用户在该三维场景中自由绘制相机轨迹，系统实时渲染预览视频（Figure 7），提供快速反馈。这一设计将相机调整与慢速生成解耦，避免了传统方法中反复试错生成的高昂时间成本（Figure 5）。

![[assets/figures/papers/paper_list_l95_https_arxiv_org_abs_2502_10059/figures/004_Figure_5.jpg]]
*Figure 5: One-round generation versus multi-round generation. Our framework decouples camera adjustment via interactive 3D scenes, enabling fast feedback before slow generation*

### 场景约束噪声成形（SNS）

**核心问题**：即使模型在公制尺度下训练，扩散采样的随机性仍可能导致生成视频的全局布局和相机运动偏离用户预期，尤其在复杂轨迹和大运动场景下。

**解决方案**：SNS 在扩散早期（高噪声阶段）利用预览视频的干净潜变量，对去噪过程施加场景级约束，引导低频结构（全局布局、相机运动）的生成。

具体操作为：在扩散时间步 $t$ 大于阈值 $t_{\mathrm{NS}}$（经验设定 $t > 0.9$，即高噪声阶段）时，将预览视频的干净潜变量 $z_{\mathrm{preview}}$ 在选定像素区域 $m$ 内注入到去噪过程中：

$$z_t = m \cdot (\alpha_t z_{\mathrm{preview}} + \sigma_t \epsilon) + (1 - m) \cdot z_t$$

其中 $m$ 为根据深度一致性筛选的有效像素掩码——仅选择预览视频中在参考图像可见且深度连续的像素，过滤深度边缘处的离群点（Figure 11），避免错误像素干扰生成。

**关键设计选择**：噪声成形仅在高噪声阶段（$t > 0.9$）应用，此时扩散过程主要决定视频的全局布局和相机运动；在低噪声阶段恢复标准采样，保留模型生成细节纹理和动态的能力。这一设计在相机控制精度与视频动态性之间取得了平衡（Table 4 的超参数敏感性实验验证了该阈值选择）。

消融实验（Table 2）表明，仅添加 SNS 即可将基础 **DynamiCrafter** 的 RotErr 从 3.3415 降至 1.5163，降幅达 54.6%，证明噪声成形对相机控制的独立贡献显著。

### 多模式拼接策略

RealCam-I2V 通过简单的帧拼接策略支持三种视频生成模式（Figure 8），无需额外训练：

- **基础模式**：直接生成完整视频序列。
- **插值模式**：在给定首尾帧之间生成中间帧，实现生成式帧插值。
- **循环/延续模式**：将生成视频的末帧作为新一轮生成的条件帧，通过相机轨迹的平滑拼接实现循环视频或长视频延续。

以上模块共同构成了 RealCam-I2V 的完整技术框架：MSA 从数据层面消除尺度歧义，SNS 从采样层面注入场景约束，二者协同实现了真实世界场景下高精度的交互式相机控制视频生成。

## 实验与关键发现

### 主实验结果

RealCam-I2V 在 RealEstate10K 数据集上与所有前沿相机控制方法进行了定量对比，结果如 Table 1 所示。所有轨迹基线方法（MotionCtrl*、CameraCtrl*、CamI2V*）均以相同版本的 **DynamiCrafter**（Xing et al., arXiv 2023）为基础模型，在相同数据划分和训练策略下复现，确保对比的公平性。

![[assets/figures/papers/paper_list_l95_https_arxiv_org_abs_2502_10059/figures/009_Table_1.jpg]]
*Table 1: Quantitative comparison with SOTA methods. Our approach excels all baselines on both relative and metric results, while coherently improve visual quality of generated videos. We observe over 30% improvement on metric scale results and over 10% improvement on FVD. * denotes our reproduced results on DynamiCrafter [76]. Best and second best results are highlighted respectively*

在相机控制精度方面，RealCam-I2V 在所有指标上均达到最优。旋转误差 RotErr 为 0.3884，较当时最优的 **CamI2V**（Zheng et al., arXiv 2024）的 0.4120 相对降低 5.73%。公制尺度平移误差 TransErr (Metric Scale) 为 2.2317，较 CamI2V 的 3.2934 相对降低 32.24%，这是最显著的提升项。整体相机姿态误差 CamMC (Metric Scale) 同样取得最优结果。

在视频质量方面，RealCam-I2V 的 FVD (StyleGAN) 为 45.460，较 CamI2V 的 53.361 相对降低 14.81%，表明生成的视频在视觉保真度上也有明显提升。这些结果表明，公制尺度对齐与场景约束噪声成形的组合，在提升相机控制精度的同时，并未以牺牲视频质量为代价。

### 消融实验

为验证各模块的独立贡献，论文设计了系统的消融实验（Table 2），在 DynamiCrafter 和 CameraCtrl* 两个基座上分别测试公制场景尺度对齐（MSA）和场景约束噪声成形（SNS）的效果。

![[assets/figures/papers/paper_list_l95_https_arxiv_org_abs_2502_10059/figures/010_Table_2.jpg]]
*Table 2: Ablation study of RealCam-I2V plugins. Metric Scene-scale Alignment (MSA) mitigates scale inconsistency for real-world applications, indicating a more stable and unified camera control. Scene-constrained Noise Shaping (SNS) solely provides substantial improvements on the base model but is less effective than the combined approach (ours). * denotes our reproduced results on Dynami-Crafter [76]. Best and second best results are highlighted respectively*

**公制场景尺度对齐（MSA）的独立作用。** 在 CameraCtrl* 上，仅引入 MSA 即可将公制尺度 TransErr 从 5.5090 降至 3.8218，降幅达 30.6%。这表明相对尺度训练是造成公制尺度下相机控制失效的核心瓶颈，而 MSA 通过统一场景尺度有效缓解了这一问题。

**场景约束噪声成形（SNS）的独立作用。** 在基础 DynamiCrafter（无相机控制）上，仅引入 SNS 即可将 RotErr 从 3.3415 降至 1.5163，降幅达 54.6%。这说明即使没有显式的相机条件注入，通过预览视频在扩散早期引导低频布局，也能大幅提升生成视频的相机运动一致性。

**组合效果。** MSA 与 SNS 组合（即完整的 RealCam-I2V）在所有相机控制指标和视频质量指标上均优于单独使用任何一个模块。在 DynamiCrafter 基座上，组合方案将 RotErr 从 3.3415 降至 0.3884，TransErr (Metric Scale) 从 4.5281 降至 2.2317，FVD 从 60.508 降至 45.460。这验证了两个模块的互补性：MSA 解决尺度一致性问题，SNS 提供场景布局引导，二者协同实现了高精度的相机控制与高质量的视频生成。

**静态数据集微调的影响。** Table 3 展示了在 VBench-I2V 上的消融结果。尽管 RealEstate10K 是静态场景数据集，在其上进行相机条件微调后，模型仍能保持动态程度（Dynamic Degree 35.77 vs 基础模型 34.15），同时将相机运动评分从 22.67 大幅提升至 93.32。这表明所提出的方法在增强相机控制能力的同时，并未牺牲视频的动态性。

### 超参数敏感性

**噪声成形阈值 tNS。** Table 4 展示了噪声成形阈值 tNS 的敏感性实验。对于噪声水平 t ∈ [0, 1000]，阈值 tNS 表示仅在扩散早期 t > tNS 的阶段应用噪声成形。实验表明，在高噪声水平（t > 0.9）应用噪声成形能够在相机控制与视频动态性之间取得最佳平衡——过早引入预览视频约束会过度限制生成自由度，过晚则无法有效引导布局。

### 跨域泛化与复杂轨迹

**跨域泛化。** 尽管模型仅在 RealEstate10K 的室内外静态场景上训练，RealCam-I2V 在宠物、风景、动漫、食物等真实场景上展现出自然的泛化能力（Figure 9），验证了公制尺度对齐带来的场景无关性。

**复杂轨迹与大运动。** Figure 10 展示了模型对复杂相机运动路径的精确跟随能力，同时保持了高保真的视频动态生成。配合 Figure 12 所示的相机关键帧插值策略，用户仅需指定稀疏关键帧即可获得平滑的密集轨迹。

**动态数据集扩展。** Table 5 展示了将 RealCam-I2V 迁移到 CogVideoX 主干并在动态数据集 RealCam-Vid 上训练的结果。该数据集包含丰富的场景动态和大幅相机运动（近 360°），引入后视频动态性和相机控制指标均有提升，噪声成形在动态场景下对一致性和质量的改善尤为显著。

### 失败模式与局限

1. **动态场景生成质量。** 当前训练数据主要为 RealEstate10K 的静态场景，在包含显著动态物体和复杂运动的场景下，生成质量仍有提升空间。论文将引入动态数据集作为未来工作方向。

2. **深度估计依赖性。** 方法依赖单目公制深度估计（Depth Anything V2 公制版本）的准确性。当深度预测存在较大误差时，可能导致噪声成形中的边缘误判——Figure 11 展示了离群点过滤策略（滤波核大小 k ≥ 3 可有效过滤错误深度边缘像素），但在极端情况下（如反射表面、透明物体）仍可能失效。

3. **SfM 对齐鲁棒性。** 公制尺度对齐过程依赖 COLMAP 的稀疏重建结果。在极端纹理缺失或纯旋转场景下，SfM 重建可能失败，导致尺度因子无法可靠估计。该问题需要人工验证具体退化程度。

![[assets/figures/papers/paper_list_l95_https_arxiv_org_abs_2502_10059/figures/011_Table_3.jpg]]
*Table 3: Ablation study on Vbench-I2V [30], investigating how camera-conditioned fine-tuning exclusively on static RealEstate10K [101] data affects the generation quality and camera motion of the base model. Notably, even fine-tuned on a static dataset, it preserves dynamics (Dynamic Degree) without compromise. Introducing dynamic datasets will better enhance dynamics, we leave it for future work*

![[assets/figures/papers/paper_list_l95_https_arxiv_org_abs_2502_10059/figures/012_Figure_9.jpg]]
*Figure 9: Visualization on various domains in real life scenarios. Despite training on RealEstate10K [101], our method can generalize naturally to out-of-domain images, including pets, landscape, anime, food and etc*

## 定位与知识库关联

### 1. 问题定位：从相对尺度到公制尺度的范式迁移

现有相机可控的图像到视频（I2V）生成方法，如 **MotionCtrl**（Wang et al., SIGGRAPH 2024）、**CameraCtrl** 和 **CamI2V**（Zheng et al., arXiv 2024），在训练时均采用**相对尺度**的相机参数——每个视频片段的平移向量被独立归一化，导致不同场景甚至同一场景的不同片段之间缺乏统一的尺度参照。这一设计在标准基准上可以获得可观的数值指标，但当用户试图在真实世界图像上绘制精确的相机轨迹时，会遭遇两个根本性障碍：

1. **尺度不一致**：模型学到的“平移1个单位”在不同场景中对应完全不同的物理距离，无法泛化到用户指定的公制尺度轨迹。
2. **交互可用性差**：用户缺乏对场景三维结构的感知，难以凭空绘制出物理上合理的相机路径，往往需要多轮试错生成。

RealCam-I2V 的核心贡献在于识别出这一**相对尺度瓶颈**，并通过引入单目公制深度估计作为统一的场景参照，将整个训练-推理流程从相对尺度范式迁移到**公制尺度范式**。这一迁移并非简单的尺度乘子替换，而是涉及数据预处理、模型条件输入、以及扩散过程约束的全链路重构。

### 2. 与基线方法的结构性对比

RealCam-I2V 建立在 **DynamiCrafter**（Xing et al., arXiv 2023）这一基础图像到视频扩散模型之上。与现有相机控制方法相比，其在两个关键维度上做出了结构性改变：

| 维度 | MotionCtrl / CameraCtrl / CamI2V | RealCam-I2V |
|------|----------------------------------|-------------|
| **相机参数尺度** | 相对尺度（逐片段归一化） | 公制尺度（通过单目深度对齐的统一绝对尺度） |
| **扩散噪声初始化** | 标准高斯噪声采样 | 场景约束噪声成形（SNS）：在扩散早期用预览视频的干净潜变量覆盖选定区域 |

具体而言，**CameraCtrl** 和 **CamI2V** 均采用 Plücker 嵌入作为相机条件表示，CamI2V 进一步引入了极线注意力机制以增强空间一致性。RealCam-I2V 保留了这些条件机制的有效部分，但通过**公制场景尺度对齐（MSA）**将相机外参从相对尺度转换为公制尺度，从而消除了训练-推理之间的尺度鸿沟。消融实验表明，仅将 MSA 应用于 CameraCtrl* 的复现版本，即可将公制尺度 TransErr 从 5.5090 降至 3.8218（降幅 30.6%），验证了尺度对齐本身是独立有效的改进。

### 3. 核心创新机制的知识贡献

#### 3.1 公制场景尺度对齐（MSA）

MSA 的核心思路是：在训练预处理阶段，利用 **Depth Anything V2** 对参考帧进行公制深度估计，然后将 COLMAP 重建的相对尺度稀疏点云对齐到该公制深度图，获得统一的尺度因子 α。这一尺度因子使得所有片段的相机平移向量能够转换到同一公制坐标系下：

$$c_{\mathrm{cam}}^{\mathrm{metric}} = \begin{bmatrix} R & \alpha \cdot T \\ 0 & 1 \end{bmatrix}$$

这一设计的深层意义在于：它将单目深度估计的“场景先验”注入到相机轨迹的表示中，使得模型在训练时就学习到物理上一致的平移量级。与之对比，MotionCtrl 直接使用 3×4 外参矩阵而不做任何尺度归一化，CameraCtrl 和 CamI2V 则依赖逐片段归一化，均无法保证跨场景的尺度一致性。

#### 3.2 场景约束噪声成形（SNS）

SNS 是 RealCam-I2V 在推理阶段的第二个关键创新。其操作方式为：在扩散去噪的高噪声阶段（t > 0.9），将交互式预览视频的干净潜变量在可见区域进行混合：

$$z_t = m \cdot (\alpha_t z_{\mathrm{preview}} + \sigma_t \epsilon) + (1 - m) \cdot z_t$$

这一机制的本质是利用预览视频提供**低频布局引导**——预览视频由重建的三维点云渲染生成，虽然缺乏纹理细节，但准确反映了用户指定的相机运动轨迹和场景几何结构。通过在扩散早期注入这些低频信息，SNS 有效约束了生成视频的相机运动，同时保留了扩散模型生成高频细节的能力。消融实验显示，仅将 SNS 应用于基础 DynamiCrafter，即可将 RotErr 从 3.3415 降至 1.5163（降幅 54.6%），证明了该机制在相机控制上的独立有效性。

值得注意的是，MSA 与 SNS 之间存在**协同效应**：MSA 确保了预览视频的尺度与训练数据一致，SNS 才能有效地将预览信息转化为精确的相机控制。两者组合（即完整的 RealCam-I2V）在所有相机控制指标和视频质量指标上均显著优于单独使用任一组件的配置。

### 4. 适用边界与局限

尽管 RealCam-I2V 在 RealEstate10K 基准上取得了显著提升，其方法设计本身决定了若干适用边界：

1. **静态场景偏好**：当前训练数据主要为 RealEstate10K 的室内外静态场景。尽管模型展现了一定的跨域泛化能力（在宠物、风景、动漫等真实场景上可生成合理结果），但在包含丰富动态物体和大幅相机运动的场景下，生成质量仍有提升空间。VBench-I2V 上的消融显示（Table 3），即使在静态数据集上微调，模型的动态程度（Dynamic Degree 35.77）仍能与基础模型（34.15）持平，但要进一步增强动态表现，需要引入动态数据集。

2. **深度估计依赖性**：整个公制尺度对齐和交互式预览渲染流程强依赖于单目公制深度估计的准确性。当深度预测存在较大误差时——特别是在反射表面、透明物体、或极端纹理缺失区域——可能导致噪声成形中的边缘误判和对齐精度下降。论文通过离群点过滤（Figure 11）缓解了部分问题，但未从根本上解决深度估计失效场景的降级策略。

3. **SfM 对齐鲁棒性**：公制尺度对齐过程依赖 COLMAP 的稀疏重建结果。在极端纹理缺失或纯旋转场景下，SfM 可能无法提供足够的匹配点，导致对齐失败。论文未报告此类失败案例的比例和处理方案。

4. **长视频生成未验证**：当前实验设定为 16 帧生成，帧步长固定为 8。该方法能否扩展到数分钟的长视频生成，并在长时序上保持尺度一致性和相机轨迹的平滑性，尚待验证。

### 5. 开放问题与后续方向

基于论文的分析和实验，以下开放问题值得关注：

1. **动态场景数据集的引入**：论文在 Table 5 中初步展示了在 RealCam-Vid 动态数据集上训练的结果，表明引入动态场景可以进一步提升 VBench-I2V 的相机运动评分。但如何系统性地构建包含丰富动态物体和大幅相机运动（如近 360° 旋转）的数据集，并设计相应的训练策略以平衡动态生成与相机控制精度，仍是一个开放方向。

2. **深度估计鲁棒性增强**：在单目深度估计完全失效的场景下，框架是否可以结合其他深度线索（如多视图立体匹配、激光雷达先验）实现鲁棒降级？这关系到方法在极端真实场景下的可用性。

3. **交互范式的进一步简化**：当前交互式轨迹绘制仍要求用户在三维点云上手动指定路径。是否可以引入自然语言或草图等更直观的交互方式，进一步降低使用门槛？

4. **多模态条件融合**：RealCam-I2V 目前以文本、图像和相机轨迹为条件。是否可以将场景的语义分割、法线图等几何先验纳入条件体系，以进一步提升生成视频的结构一致性？

## 原文 PDF

![[paperPDFs/arxiv_2025/RealCam_I2V_Real_World_Image_to_Video_Generation_with_Interactive_Complex_Camera_Control.pdf]]
