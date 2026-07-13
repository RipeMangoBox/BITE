---
title: "Diffusion as Shader: 3D-aware Video Diffusion for Versatile Video Generation Control"
type: paper
paper_level: A
venue: SIGGRAPH
year: 2025
pdf_ref: paperPDFs/SIGGRAPH_2025/Diffusion_as_Shader_3D_aware_Video_Diffusion_for_Versatile_Video_Generation_Control.pdf
project_link: "https://igl-hkust.github.io/das/"
code_link: "https://github.com/black-forest-labs/flux"
aliases:
- DASD
- DAS3AVDVVGC
tags:
- SIGGRAPH_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 使用3D跟踪视频（由运动3D点构建，颜色编码3D坐标）作为扩散模型的条件输入，使生成过程具备3D感知能力。
primary_logic: 视频本质上是动态3D内容的2D渲染；利用3D跟踪视频可以统一各类控制任务（动画网格、运动迁移、相机控制、物体操控），同时通过跨帧颜色一致性提升时序连贯性。
claims:
- 仅需3天在8块H800 GPU上微调不到1万段视频，即实现多种任务控制
- 在相机控制任务上，DaS的TransErr（小幅度）为27.85，RotErr（大幅度）为10.40，显著优于MotionCtrl和CameraCtrl
- 在运动迁移任务上，DaS在Text-Ali和Tem-Con指标上均优于CCEdit和TokenFlow
- 消融实验证明3D跟踪视频在所有指标上均优于深度图控制信号，且对跟踪点密度不敏感
---

# Diffusion as Shader: 3D-aware Video Diffusion for Versatile Video Generation Control

> [!tip] 核心洞察
> 视频本质上是动态3D内容的2D渲染；利用3D跟踪视频可以统一各类控制任务（动画网格、运动迁移、相机控制、物体操控），同时通过跨帧颜色一致性提升时序连贯性。

| 字段 | 内容 |
|------|------|
| 中文题名 | 扩散着色器：三维感知视频扩散模型实现多功能视频生成控制 |
| 英文题名 | Diffusion as Shader: 3D-aware Video Diffusion for Versatile Video Generation Control |
| 会议/期刊 | SIGGRAPH 2025 |
| Links | [paper](http://arxiv.org/abs/2501.03847v2) · [Project](https://igl-hkust.github.io/das/) · [paper](https://arxiv.org/abs/2309) · [Code](https://github.com/black-forest-labs/flux) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | Diffusion as Shader (DaS) |
| Dataset | Camera Control, Motion Transfer, Mesh-to-Video Generation, Object Manipulation |

> [!tip] 效果简介
> - Camera Control (RealEstate10K [Zhou et al. 2018]) 上，TransErr (Translation Error, degree) 27.85 (Small Movement) vs MotionCtrl: 59.51, CameraCtrl: 41.82 (approx, outperformed) (显著优于两个基线)。
> - Camera Control (RealEstate10K) 上，RotErr (Rotation Error, degree) 10.40 (Large Movement) vs MotionCtrl: 65.31, CameraCtrl: 17.13 (approx, outperformed) (显著优于两个基线)。
> - Motion Transfer 上，Text-Ali (CLIP text alignment) 32.6 vs CCEdit: ~30.6, TokenFlow: ~24.2 (outperformed) (优于两个基线)。

## 概要

**问题**：现有视频生成控制方法依赖二维控制信号（如深度图、光流），缺乏对底层三维内容的感知，难以实现通用且精细的物体操控与相机运动控制。

**方法**：提出 **Diffusion as Shader (DaS)**，一种三维感知的视频扩散模型。核心思想是将视频视为动态三维内容的二维渲染，以**三维跟踪视频**（由运动三维点云构建，颜色编码三维坐标）作为统一控制信号，通过可训练的 Condition DiT 将三维条件注入冻结的去噪 DiT，实现多种控制任务的统一。

**主要结果**：仅需在 8 块 H800 GPU 上对不到 1 万段视频微调 3 天，DaS 即可在相机控制（TransErr 27.85、RotErr 10.40，显著优于 MotionCtrl 和 CameraCtrl）、运动迁移（Text-Ali 32.6、Tem-Con 0.971，优于 CCEdit 和 TokenFlow）、网格动画生成及物体操控等任务上取得领先性能。消融实验证实三维跟踪视频在所有指标上全面优于深度图控制信号，且对跟踪点密度不敏感。

**定位**：DaS 首次以统一的三维跟踪视频范式桥接多种视频控制任务，区别于依赖任务特定二维信号的方法（如 MotionCtrl、CameraCtrl），为三维感知视频生成提供了高效、通用的新基线。

## 核心方法与创新机理

### 唯一瓶颈

现有视频生成控制方法（如 MotionCtrl、CameraCtrl、CCEdit）依赖 2D 控制信号（深度图、相机嵌入、光流等），缺乏对底层 3D 场景结构的理解。这导致两个根本性缺陷：**（1）控制精度不足**——2D 信号无法准确描述三维空间中的物体运动和相机位姿变化；**（2）任务通用性差**——不同控制任务需要设计不同的条件表示和注入机制，难以统一。

### 核心机制：3D 跟踪视频作为统一控制信号

DaS 的核心洞察是：**视频本质上是动态 3D 内容的 2D 渲染**。基于此，方法提出使用 **3D 跟踪视频（3D tracking video）** 作为扩散模型的条件输入，使生成过程具备 3D 感知能力。

3D 跟踪视频的构建方式为：给定一组动态 3D 点 $\{\mathbf{p}_i(t) \in \mathbb{R}^3\}$，每个点的颜色由其在第一帧相机坐标系下的归一化坐标决定（映射到 $[0,1]^3$ 并转换为 RGB）。这一设计使得：
- **空间位置显式编码**：每个像素的颜色直接反映该点在 3D 空间中的绝对位置，而非仅深度值；
- **跨帧颜色一致性**：同一 3D 点在不同帧中保持相同颜色，为模型提供强时序对应信号；
- **任务统一表示**：物体操控、相机控制、运动迁移、网格动画化等任务均可通过构建不同的 3D 点运动轨迹来生成对应的跟踪视频（Fig. 3），无需为每类任务设计独立的控制分支。

### 关键改造点（Changed Slots）

**改造点 1：控制信号从 2D 升级为 3D 跟踪视频**

| 维度 | 基线方法 | DaS |
|------|---------|-----|
| 信号类型 | 深度图、相机嵌入、光流等 2D 表示 | 3D 跟踪视频（颜色编码 3D 坐标） |
| 空间信息 | 仅包含深度或 2D 位移 | 完整的 3D 位置信息 |
| 任务通用性 | 每类任务需定制条件 | 统一表示覆盖四类任务 |

**改造点 2：条件注入从标准 ControlNet 改为可训练的 Condition DiT**

DaS 不采用标准 ControlNet 的零初始化卷积注入，而是：
- 复制预训练去噪 DiT（CogVideoX）的前 18 层（共 42 层），作为可训练的 **Condition DiT**；
- 在 Condition DiT 的每层输出后，通过 **零初始化线性层** 将条件特征注入冻结的去噪 DiT 对应层。

这一设计使得条件分支与去噪分支共享 DiT 架构，能够充分利用预训练模型的表示能力，同时零初始化确保训练初期不破坏基座模型的生成质量。

**改造点 3：训练效率从百万级视频降至万级**

基线方法通常需要大规模视频数据集（数百万段）进行训练，而 DaS 仅使用不到 1 万段视频（包含真实视频 MiraData 和合成渲染视频），在 8 块 H800 GPU 上微调 3 天即可获得强大的控制能力。效率提升的关键在于：冻结去噪 DiT 的主体权重，仅训练 Condition DiT 和零初始化线性层，极大降低了训练开销。

### 必要公式与变量含义

**输入输出定义**

- 输入图像：$\mathbf{I} \in \mathbb{R}^{H \times W \times 3}$，高度 $H$，宽度 $W$，3 通道 RGB
- 生成视频：$\mathbf{V} \in \mathbb{R}^{T \times H \times W \times 3}$，帧数 $T$，高度 $H$，宽度 $W$，3 通道 RGB

**相机控制评估指标**

- 旋转误差（RotErr）：$$\mathrm{RotErr} = \operatorname{arccos}\left( \frac{1}{T-1} \sum_{i=2}^{T} \langle \mathbf{\Delta q}_{\mathrm{gen}}^{i}, \mathbf{q}_{\mathrm{gt}}^{i} \rangle \right)$$ 其中 $\mathbf{\Delta q}_{\mathrm{gen}}^{i}$ 为生成视频相邻帧间的估计旋转四元数，$\mathbf{q}_{\mathrm{gt}}^{i}$ 为真值旋转四元数，$\langle \cdot, \cdot \rangle$ 表示内积。该指标计算生成轨迹与真值轨迹之间旋转角度的余弦相似度。

- 平移误差（TransErr）：$$\mathrm{TransErr} = \operatorname{arccos}\left( \frac{1}{T-1} \sum_{i=2}^{T} \langle \mathbf{t}_{\mathrm{gen}}^{i}, \mathbf{t}_{\mathrm{gt}}^{i} \rangle \right)$$ 其中 $\mathbf{t}_{\mathrm{gen}}^{i}$ 和 $\mathbf{t}_{\mathrm{gt}}^{i}$ 分别为生成与真值的帧间平移向量。两个指标均以度为单位，值越小表示相机轨迹控制越精确。

### 架构流程

DaS 的完整推理流水线（Fig. 2）包含六个模块：

![[assets/figures/papers/paper_list_l3_http_arxiv_org_abs_2501_03847v2/figures/002_Figure_2.jpg]]
*Figure 2: Architecture of DaS. (a) We colorize dynamic 3D points according to their coordinates to get (b) a 3D tracking video. (c) The input image and the 3D tracking video are processed by (d) a transformer-based latent diffusion with a variational autoencoder (VAE). The 3D tracking video is processed by a trainable copy of the denoising DiT and zero linear layers are used to inject the condition features from 3D tracking videos into the denoising process*

1. **3D 跟踪视频生成**：根据任务类型构建动态 3D 点云并渲染为颜色编码视频；
2. **VAE 编码器（冻结）**：将输入图像和 3D 跟踪视频编码为潜在向量；
3. **Condition DiT（可训练）**：处理 3D 跟踪视频的潜在向量，提取多尺度条件特征；
4. **去噪 DiT（冻结）**：迭代去噪潜在噪声，生成视频潜在向量；
5. **零初始化线性层**：将 Condition DiT 各层输出注入去噪 DiT 对应层；
6. **VAE 解码器**：将去噪后的潜在向量解码为视频帧。

![[assets/figures/papers/paper_list_l3_http_arxiv_org_abs_2501_03847v2/figures/010_Figure_7.jpg]]
*Figure 7: More results of the animating mesh to video generation task. Our method enables the generation of different styles from the same mesh*

## 实验与关键发现

### 核心定量结果

DaS在相机控制与运动迁移两大任务上均取得显著优势，验证了3D跟踪视频作为统一控制信号的有效性。

**相机控制（Table 1）**：在RealEstate10K数据集上，DaS以TransErr和RotErr度量相机轨迹精度。在小幅度运动场景下，DaS的TransErr为**27.85**，远优于MotionCtrl（59.51）和CameraCtrl（41.82）；在大幅度运动场景下，RotErr为**10.40**，同样大幅领先MotionCtrl（65.31）和CameraCtrl（17.13）。这表明3D感知条件使模型能精确推断空间关系，而非仅拟合2D表观模式。

**运动迁移（Table 2）**：DaS在文本对齐度（Text-Ali: **32.6**）和时序一致性（Tem-Con: **0.971**）上均超越CCEdit（~30.6 / ~0.965）和TokenFlow（~24.2 / ~0.949）。跨帧颜色一致的3D跟踪视频为时序连贯性提供了强约束，这是2D光流类方法难以实现的。

### 关键消融发现

**3D跟踪视频 vs. 深度图（Table 3）**：将控制信号从深度图替换为3D跟踪视频后，PSNR、SSIM、LPIPS、FVD四项指标全面改善。深度图仅提供逐帧几何信息，缺乏跨帧对应关系；而3D跟踪视频通过颜色编码的坐标一致性，隐式注入了时序对应，这是质量提升的因果机制。

**跟踪点密度鲁棒性（Table 3）**：在2500、4900、8100个跟踪点配置下，生成质量相近，说明方法对点密度不敏感。这降低了实际部署中对追踪器精度的要求。

**条件注入策略**：仅微调Condition DiT（去噪DiT前18层的可训练副本）而冻结基座模型，即可有效注入3D控制。零初始化线性层确保训练初期不破坏预训练生成能力，这是微调仅需不到1万段视频（3天8卡H800）的数据效率来源。

### 定性结果与边界

**网格到视频生成**：DaS可从动画网格生成高保真纹理且时序稳定的视频（Fig. 7），支持同一网格输出不同风格。与CHAMP的对比（Fig. 8）显示纹理质量和运动自然度均有优势，但该任务目前仅有定性比较，需手动验证。

**物体操控**：DaS首次演示了精确的物体平移/旋转操控（Fig. 9），通过SAM分割目标物体并构建其3D跟踪点实现。这是现有方法未覆盖的新能力。

### 失败模式

**跟踪视频不兼容（Fig. 11上）**：当提供的3D跟踪视频与输入图像结构不匹配时，模型会强制“过渡”到兼容场景，而非保持原结构。这暴露了条件信号与生成内容之间的硬耦合——模型缺乏拒绝不合理条件的能力。

**跟踪范围外失控（Fig. 11下）**：无3D跟踪点覆盖的区域（如物体移除后露出的背景）不受约束，可能产生不受控内容。这源于3D跟踪视频的稀疏性——它仅约束有点区域，空白区域依赖模型先验填充。

**系统限制**：当前最大输出49帧、分辨率480×720，推理约需2.5分钟（DDIM 50步，CFG 7.0）。依赖外部追踪器（如SpatialTracker），在复杂遮挡下追踪精度下降会传导至生成质量。训练数据包含MiraData真实视频和合成渲染视频，泛化到极端域外场景需谨慎。

![[assets/figures/papers/paper_list_l3_http_arxiv_org_abs_2501_03847v2/figures/005_Table_1.jpg]]
*Table 1: Quantitative results on camera control of MotionCtrl [Wang et al. 2024c], CameraCtrl [He et al. 2024b], and our method. “TransErr” and “RotErr" are the angle differences between the estimated translation and rotation and the ground-truth ones in degree*

![[assets/figures/papers/paper_list_l3_http_arxiv_org_abs_2501_03847v2/figures/008_Table_3.jpg]]
*Table 3: Analysis of applying different 3D control signals for image to video generation. We evaluate PSNR, SSIM, LPIPS, and FVD of generated videos on the validation set of the DAVIS and MiraData datasets. “Depth” means using depth maps as the 3D control signals. “Tracking” means using 3D tracking videos as the control signals. #Tracks means the number of 3D points used in the 3D tracking video*

![[assets/figures/papers/paper_list_l3_http_arxiv_org_abs_2501_03847v2/figures/011_Figure_8.jpg]]
*Figure 8: Qualitative comparison on the animating mesh to video task between our method and CHAMP [Zhu et al. 2024]*

![[assets/figures/papers/paper_list_l3_http_arxiv_org_abs_2501_03847v2/figures/012_Figure_9.jpg]]
*Figure 9: Qualitative results of our method on the object manipulation task. The top part shows the results of translation while the bottom part shows the results of rotating the object*

## 定位与知识库关联

**DaS** 的核心定位是将视频生成的控制信号从2D平面提升到3D空间，从而统一多种此前需要独立方法解决的控制任务。与现有工作的本质差异体现在三个层面：

### 1. 控制信号的维度跃迁

现有视频控制方法依赖2D信号：**MotionCtrl**（Wang et al., SIGGRAPH 2024）和 **CameraCtrl**（He et al., 2024b）分别使用相机嵌入或光流等2D表征进行相机控制，**CCEdit**（Feng et al., 2024b）和 **TokenFlow**（Geyer et al., 2023b）在运动迁移中依赖2D特征匹配。这些方法缺乏对底层3D场景结构的理解，导致控制精度受限且任务类型单一。

DaS 的突破在于引入**3D跟踪视频**作为统一的条件信号——通过在第一帧相机坐标系下对动态3D点的坐标进行颜色编码（归一化至 $[0,1]^3$），将3D运动信息直接注入扩散模型。这一设计使得模型天然具备3D感知能力，能够精确推理空间关系，从而用同一框架支持相机控制、运动迁移、网格动画化和物体操控四类任务。

### 2. 条件注入的架构选择

DaS 采用**可训练的 Condition DiT**（复制预训练去噪 DiT 的前18层）加**零初始化线性层**注入条件特征，而非标准的 ControlNet 式注入。这一设计的关键优势在于：冻结去噪 DiT 保留了基座模型 **CogVideoX**（Yang et al., 2024b）的生成能力，仅通过 Condition DiT 学习3D控制信号到生成空间的映射。消融实验证实，这种冻结策略足以有效注入3D控制，同时大幅降低训练成本（<10k视频，3天8卡H800）。

### 3. 知识库挂载点与适用边界

**可挂载的知识库节点**：
- **3D视觉与跟踪**：依赖外部3D追踪器（如 SpatialTracker）构建跟踪视频；与深度估计、SAM分割等工具链（Kirillov et al., 2023; Bochkovskii et al., 2024）协同工作。
- **视频扩散模型**：基于 CogVideoX 的 DiT 架构微调，继承其 VAE 和去噪框架。
- **可控生成**：与 ControlNet 系列方法并行，但以3D跟踪视频替代2D控制图（深度、边缘等），Table 3 消融实验证明3D跟踪视频在 PSNR、SSIM、LPIPS、FVD 上全面优于深度图控制。

**适用边界与限制**：
- **依赖外部3D信息**：3D跟踪视频的构建需要已有视频或网格，无法从纯文本/图像直接生成；在复杂运动或遮挡场景下，追踪器精度成为瓶颈。
- **输出规格受限**：当前仅支持最大49帧、480×720分辨率，不支持更长或更高分辨率生成。
- **无跟踪点区域失控**：输入图像中未被3D跟踪点覆盖的区域（如超出追踪范围）会失去控制，产生不受控内容（Fig. 11）。
- **场景不匹配时的强制转换**：当提供的跟踪视频与输入图像结构不兼容时，模型会强制转换场景，可能偏离预期（Fig. 11）。

### 4. 后续启发与开放问题

DaS 的成功表明，**将3D先验编码为可渲染的视频格式**是提升视频生成可控性的有效路径。这为后续工作提供了以下方向：

1. **端到端3D信号生成**：训练扩散模型直接从输入图像或文本生成3D跟踪视频，摆脱对现成视频/网格的依赖，是实现完全自主可控生成的关键一步。
2. **扩展性与实时性**：当前推理约需2.5分钟/49帧，探索蒸馏或高效采样策略将其推向交互式应用是重要工程挑战。
3. **多模态指令融合**：将3D跟踪视频与自然语言指令结合，可能实现更灵活的场景编辑（如“将物体向右移动同时改变相机角度”）。
4. **与3D重建的闭环**：DaS 生成的视频可反馈至3D重建管线，形成“重建-生成-验证”的闭环，提升3D内容生成的精度与一致性。

总体而言，DaS 在视频控制领域开辟了“3D跟踪视频作为通用控制接口”的新范式，其核心贡献不在于提出全新的扩散架构，而在于识别出**3D坐标颜色编码**这一简洁而强大的表征，使得预训练视频扩散模型能够以极低成本获得3D感知能力。这一思路可能启发其他生成任务（如4D内容生成、多视角合成）采用类似的3D条件注入策略。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2025/Diffusion_as_Shader_3D_aware_Video_Diffusion_for_Versatile_Video_Generation_Control.pdf]]