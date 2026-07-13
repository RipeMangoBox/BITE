---
title: "EasyCreator: Empowering 4D Creation through Video Inpainting"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/EasyCreator_Empowering_4D_Creation_through_Video_Inpainting_0433338d18d5.pdf
project_link: "https://runwayml.com/research/gen-1"
code_link: null
aliases:
- EasyCreator
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 将4D生成重新定义为视频修复任务，构建包含点云可见性掩码、编辑掩码及联合掩码的组合掩码数据集对基础模型进行微调，并结合自迭代调优与时间打包推理策略。
primary_logic: 借助先进的视频修复先验，通过逐步增加视角的自迭代训练和利用已生成视图引导后续视图的时间打包推理，可在极少量额外训练下解锁高质量、多视图一致的4D视频生成与灵活的提示编辑能力。
claims:
- 组合掩码微调是实现4D生成与编辑的关键，去掉后模型无法完成基本任务，视觉质量大幅下降（FID从58.26升至78.27）。
- 自迭代调优大幅提升大角度相机运动下的时序一致性（FVD从145.71升至197.24）。
- 时间打包推理策略显著提升多视图生成的一致性（FVD-V从119.52升至137.64; CLIP-V从89.87降至84.71）。
- 在真实场景视频、长视频及挑战性相机运动下均取得SOTA性能，远超先前方法。
---

# EasyCreator: Empowering 4D Creation through Video Inpainting

> [!tip] 核心洞察
> 借助先进的视频修复先验，通过逐步增加视角的自迭代训练和利用已生成视图引导后续视图的时间打包推理，可在极少量额外训练下解锁高质量、多视图一致的4D视频生成与灵活的提示编辑能力。

| 字段 | 内容 |
|------|------|
| 中文题名 | EasyCreator: 通过视频修复赋能4D创作 |
| 英文题名 | EasyCreator: Empowering 4D Creation through Video Inpainting |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=mU8Ubd8aNK) · [Project](https://runwayml.com/research/gen-1) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | EasyCreator |
| Dataset | VBench, Kubric-4D, Quantitative comparison, Real-world videos |

> [!tip] 效果简介
> - VBench (40 real + 40 generated videos) 上，Overall Consis.↑ 0.2915 vs 0.2463 (TrajectoryCrafter) (+0.0452)。
> - Kubric-4D 上，PSNR↑ 22.15 vs 15.82 (TrajectoryCrafter) (+6.33)。
> - Quantitative comparison (Tab.2) 上，FID↓ 58.26 vs 61.57 (TrajectoryCrafter) (-3.31)。

## 概要

**问题瓶颈**：现有4D视频生成方法难以在保持多视图一致性的同时，实现灵活的相机轨迹控制和内容编辑。其根本瓶颈在于预训练视频修复基础模型（如Wan2.1）无法直接处理由点云渲染产生的遮挡掩码（分布外），且在大角度相机运动下缺乏三维感知能力，导致时序不一致、伪影及多视图不一致。

**核心思路**：EasyCreator将4D视频创作重新定义为视频修复任务。通过构建包含点云可见性掩码、编辑掩码及联合掩码的组合掩码数据集，对基础模型进行微调，并结合自迭代调优与时间打包推理策略，在极少量额外训练下解锁高质量、多视图一致的4D视频生成与灵活的提示编辑能力。

**方法定位**：EasyCreator属于基于拟合的4D生成方法，以**Wan2.1-14B**视频修复模型为基础骨干，利用**DepthCrafter**估计深度构建动态点云作为中间表示。与**TrajectoryCrafter**（YU et al., 2025）、**ReCapture**（Zhang et al., 2024a）、**Reangle-A-Video**（Jeong et al., 2025）等同期工作相比，EasyCreator通过组合掩码微调、角度递增的自迭代训练和时间打包推理三个关键设计，在视觉质量、相机精度和视图同步性上均取得显著提升。

**主要结果**：在VBench基准上，EasyCreator的总体一致性指标达到0.2915，超越TrajectoryCrafter的0.2463；在Kubric-4D上PSNR达到22.15（对比最佳基线15.82）；在真实场景视频、长视频（>30帧）及挑战性相机运动下均取得SOTA性能。用户研究排名第一。消融实验证实，组合掩码微调是任务可行性的基础（去掉后FID从58.26升至78.27），自迭代调优保障大角度时序一致性（FVD从145.71升至197.24），时间打包推理增强多视图一致性（FVD-V从119.52升至137.64）。

4D视频创作——即给定一段单目视频，在任意新相机轨迹下生成时空一致且支持内容编辑的新视频——是视觉生成领域的前沿挑战。该任务要求模型同时具备**新视角合成**的几何准确性、**时序一致性**的保持能力，以及**多视图一致性**的全局协调能力。现有方法在这三个维度上存在系统性缺口。

**现有方法的瓶颈**。当前4D生成方法大致分为三类：（1）基于新视角合成的方法，如**GCD**（Hoorick et al., 2024），通常依赖显式3D表示（如点云或NeRF），但在大角度相机运动和复杂动态场景下容易出现几何失真和时序抖动；（2）相机可控视频生成方法，如**Trajectory-Attention**（Xiao et al., 2024b）、**ReCamMaster**（Bai et al., 2025）、**TrajectoryCrafter**（YU et al., 2025），通过注入相机姿态条件来控制生成视角，但缺乏对多视图间一致性的显式建模，导致不同轨迹生成的视频在重叠区域出现内容冲突；（3）基于视频修复的4D方法，如**Reangle-A-Video**（Jeong et al., 2025），将新视角生成视为修复任务，但未充分利用预训练大模型的视频先验，且缺乏针对大角度运动的专门优化。

**核心瓶颈的深层分析**。本文识别出阻碍4D视频生成质量提升的**根本瓶颈**：预训练视频修复基础模型（如Wan2.1-14B）虽然拥有强大的视频先验，但无法直接处理由动态点云渲染产生的遮挡掩码——这类掩码属于分布外（out-of-distribution）信号，与模型训练时见到的随机遮挡掩码存在本质差异。此外，基础模型缺乏三维感知能力，在大角度相机运动下无法保持几何一致性和时序连贯性，导致生成结果出现伪影、闪烁和多视图不一致。

**本文动机**。基于上述分析，本文提出**EasyCreator**，核心动机是将4D视频创作重新定义为**视频修复任务**，通过三个关键设计解锁预训练视频修复模型的4D生成潜力：（1）构建组合掩码数据集，使模型学会处理点云可见性掩码的分布外特性；（2）设计自迭代调优策略，从小视角逐步扩展到大视角，渐进式增强模型的大角度生成能力；（3）提出时间打包推理机制，利用已生成视图的信息引导后续视图生成，显式增强多视图一致性。这一框架在极少量额外训练（约2000步LoRA微调）下，即可实现高质量、多视图一致的4D视频生成与灵活的提示编辑。

## 核心方法与创新机理

EasyCreator 的核心创新在于将 4D 视频生成重新定义为**视频修复任务**，并围绕这一范式重构了从数据构造、模型调优到推理策略的完整技术链路。与现有方法相比，其关键 changed slots 体现在三个层面：

### 1. 组合掩码训练数据：从分布内修复到 4D 感知修复

**Baseline 状态**：标准视频修复模型（如 Wan2.1）使用随机遮挡、光流引导掩码等分布内数据进行训练，无法处理由 3D 几何投影产生的遮挡掩码（分布外），更不具备多视图一致性意识。

**EasyCreator 方案**：通过动态点云的双重投影，构造包含三种掩码的组合掩码数据集：

- **点云可见性掩码**：利用 DepthCrafter 估计输入视频的逐帧深度，结合相机内参反投影为动态点云序列 $\mathcal{P}_i = \phi([\mathbf{I}_i, \mathbf{D}_i], \mathbf{K})$，再通过双重投影将新视角下的不可见区域映射回原始相机平面，生成精确的遮挡掩码。该掩码标记了因相机运动而需要填充的“洞”区域，使模型学习 3D 几何约束下的修复。
- **编辑掩码**：支持用户指定的首帧编辑区域，实现内容编辑与视角生成的解耦。
- **联合掩码**：将可见性掩码与编辑掩码叠加，提供多样化的训练监督信号。

这一设计将 4D 生成的几何约束显式编码为修复掩码，使预训练视频修复模型能够在不改变架构的前提下“理解”3D 遮挡关系。消融实验表明，**去除组合掩码训练后模型完全无法完成 4D 生成与编辑任务**，FID 从 58.26 急剧恶化至 78.27（Table 4, Figure 6(a)），验证了该 slot 变更的决定性作用。

### 2. 自迭代调优：从小视角到大视角的渐进式能力解锁

**Baseline 状态**：现有方法通常采用单阶段微调（固定视角）或直接使用预训练权重，在大角度相机运动下时序一致性严重退化。

**EasyCreator 方案**：提出角度递增的自迭代调优策略，通过“生成-训练-再生成”的循环逐步扩展模型的视角处理能力：

1. **小视角起步**：首先生成小视角（如 30°）掩码视频，利用 LoRA（秩 128）对 Wan2.1-14B 进行微调。
2. **几何外推**：使用当前模型权重，通过几何扭曲函数 $\widetilde{\mathbf{I}}_i^j = \psi(\mathcal{P}_i^j, \mathbf{K}, \mathbf{T}_i^j)$ 外推更大视角（间隔 10°）的渲染视频 $\widetilde{V}^j$。
3. **循环一致性更新**：将外推视频作为下一阶段训练数据，通过循环一致性损失迭代更新 LoRA 权重：
   $$\mathbf{W}_{LoRA}^{(j)} = \mathbf{W}_{LoRA}^{(j-1)} + \eta \nabla_{\mathbf{W}} \mathcal{L}_{cycle}(\widetilde{V}^j, \mathbf{M}^j, \Delta\mathbf{W})$$

该策略的核心机制在于：每次迭代生成的视频为下一轮训练提供了“伪真值”，模型通过自我监督逐步适应更大的视角偏移。消融实验证实，**去除自迭代调优后大角度相机运动下的时序一致性严重退化**，FVD 从 145.71 升至 197.24（Table 4, Figure 6(b)），凸显了渐进式训练对稳定大运动生成的关键作用。

### 3. 时间打包推理：利用视图间重叠增强多视图一致性

**Baseline 状态**：逐相机轨迹独立生成，不同视角之间无信息交互，导致多视图生成结果不一致。

**EasyCreator 方案**：在推理阶段引入时间打包策略，利用已生成视图作为先验引导当前视图生成：

- **先验帧选择**：从先前轨迹的生成结果中，按修复面积选取 Top-K 帧 $\mathbf{F} = \mathrm{top\text{-}k\text{-}argmax}(S[\widetilde{V}^a, \mathbf{M}^a])$，确保选中的帧包含丰富的有效像素信息。
- **时间维度拼接**：将先验帧的 token 与当前轨迹的“洞视频” token 沿时间维度拼接：
  $$x_{input} = [\mathrm{patchify}(\mathcal{E}(\mathbf{F})), \mathrm{patchify}(\mathcal{E}(\mathbf{V}^b))]_{\mathrm{temporal}}$$
- **全局自注意力**：利用预训练模型的全局时空注意力机制，使当前视图的遮挡区域能够直接参照已生成视图的对应区域，从而实现多视图一致生成。

该策略的动机源于相机轨迹间的自然重叠区域（Figure 3），EasyCreator 将这种几何先验转化为模型输入层面的显式引导。消融实验表明，**去除时间打包策略后多视图一致性显著降低**，FVD-V 从 119.52 升至 137.64，CLIP-V 从 89.87 降至 84.71（Table 4, Figure 7），验证了视图间信息交互对一致性的关键贡献。

### 创新点之间的协同关系

三个 changed slots 并非孤立存在，而是形成了一条完整的因果链：**组合掩码**为模型提供了理解 3D 遮挡的基础能力；**自迭代调优**在此基础上逐步扩展视角处理范围；**时间打包推理**则利用已解锁的多视图生成能力进一步提升一致性。这一“数据构造→能力扩展→推理增强”的递进设计，使得 EasyCreator 在仅需约 2 小时单视频优化的条件下，即可实现高质量、多视图一致的 4D 视频生成与灵活的内容编辑。

EasyCreator 将 4D 视频生成重新定义为**视频修复（video inpainting）**任务，其核心 pipeline 包含四个紧密耦合的模块：**动态点云生成**、**组合掩码构建**、**视频修复基础模型微调**、以及**自迭代调优与时间打包推理**。整体流程如图 Figure 2 所示。

![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_mU8Ubd8aNK/figures/002_Figure_2.jpg]]
*Figure 2: Overview of our method. We reformulate the 4D video creation as a video inpainting task. Left: given a video, we first generate the composite masks from the dynamic point cloud and feed them into the video inpainting model to unlock its 4D video creation capability. Right: To unlock the capability of generating 4D video with larger motion, we first generate videos with small motion, then feed them into the model to improve the temporal consistency progressively*

**输入与输出流**：给定一段输入视频和一个目标相机轨迹，系统首先利用 **DepthCrafter** 估计逐帧深度，结合相机内参 $\mathbf{K}$ 将每帧反投影为 3D 点云 $\mathcal{P}_i$（Eq. 1），形成动态点云序列。该动态点云作为连接原始视图与新视角的核心中间表示。随后，通过双重投影策略，将新视角下的不可见区域映射回原始相机平面，生成**点云可见性掩码**；同时构造**编辑掩码**和**联合掩码**，三者共同构成组合掩码训练数据。这些掩码与原始视频配对，送入以 **Wan2.1-14B** 为基础模型的视频修复网络进行 LoRA 微调（秩 128，2000 步），使其学会填充由视角变化造成的遮挡区域。

**自迭代调优**：为提升大角度相机运动下的时序一致性，系统采用角度递增方案：首先生成小视角（如 30°）掩码视频进行微调，随后利用几何扭曲函数 $\psi(\cdot)$ 外推更大视角的渲染图像，将当前模型生成的视频作为下一阶段训练数据，通过循环一致性损失迭代更新 LoRA 权重（Eq. 3-6）。

**时间打包推理**：在推断阶段，从已生成视图的修复区域中按面积选取 Top-K 帧作为先验，将其 token 与当前轨迹的洞视频 token 沿时间维度拼接（Eq. 7-8），借助预训练模型的全局时空自注意力机制增强多视图一致性。

**关键瓶颈与因果调节**：预训练视频修复模型无法直接处理由点云渲染产生的分布外遮挡掩码，且缺乏三维感知能力。EasyCreator 通过**组合掩码微调**注入 4D 感知能力，通过**自迭代调优**逐步扩展视角范围，通过**时间打包推理**显式利用多视图重叠区域，三者协同以极少量额外训练解锁高质量、多视图一致的 4D 视频生成与灵活编辑（Figure 4 展示了方法在相机轨迹变化和首帧编辑下的生成画廊）。

EasyCreator将4D视频生成重新定义为视频修复任务，其核心由四个关键模块构成，通过组合掩码、自迭代调优与时间打包推理三大策略解锁预训练视频修复基础模型的4D生成能力。

### 动态点云生成

给定输入视频帧 $\mathbf{I}_i$ 及其单目深度估计 $\mathbf{D}_i$，利用相机内参矩阵 $\mathbf{K}$ 将每帧反投影为三维点云：

$$\mathcal{P}_i = \phi([\mathbf{I}_i, \mathbf{D}_i], \mathbf{K}) \tag{1}$$

其中 $\phi(\cdot)$ 为DepthCrafter深度估计与反投影函数。随后，对任意新相机位姿 $\mathbf{T}_i$，将点云渲染回图像平面：

$$\mathbf{I}_i^a = \psi(\mathcal{P}_i, \mathbf{K}, \mathbf{T}_i) \tag{2}$$

$\psi(\cdot)$ 为可微渲染函数。动态点云作为连接原始帧与新视角的关键中间表示，使模型无需显式三维重建即可完成视角外推。

### 组合掩码构建

预训练视频修复基础模型（Wan2.1-14B）无法直接处理由点云渲染产生的分布外遮挡掩码。EasyCreator通过双重投影策略，将新视角下的不可见区域映射回原始相机平面，生成三种互补掩码：

- **点云可见性掩码**：标记因相机运动而新暴露的遮挡区域
- **编辑掩码**：标记用户指定的首帧编辑区域
- **联合掩码**：将上述两种掩码组合，形成复合训练监督

该组合掩码数据集使基础模型在微调过程中同时学习填充遮挡区域与保持编辑一致性，是解锁4D生成与编辑能力的关键。

### 自迭代调优

为应对大角度相机运动下的时序不一致问题，EasyCreator采用角度递增的自迭代训练策略。首先在小视角（如30°）下生成掩码视频并进行LoRA微调：

$$\mathbf{W}_{LoRA}^* = \arg\min_{\mathbf{W}} \mathcal{L}(\mathbf{V}^k, \mathbf{M}^k, \Delta\mathbf{W}) \tag{3}$$

随后，利用几何扭曲函数 $\psi(\cdot)$ 将当前模型生成的视频外推至更大视角：

$$\widetilde{\mathbf{I}}_i^j = \psi(\mathcal{P}_i^j, \mathbf{K}, \mathbf{T}_i^j) \tag{4}$$

$$\widetilde{V}^j = \{\mathbf{I}_0^j, \dots, \mathbf{I}_{N-1}^j\} \tag{5}$$

以10°为间隔递增角度，将每次迭代生成的视频作为下一阶段训练数据，通过循环一致性损失迭代更新LoRA权重：

$$\mathbf{W}_{LoRA}^{(j)} = \mathbf{W}_{LoRA}^{(j-1)} + \eta \nabla_{\mathbf{W}} \mathcal{L}_{cycle}(\widetilde{V}^j, \mathbf{M}^j, \Delta\mathbf{W}) \tag{6}$$

该策略使模型逐步适应更大视角的修复需求，显著提升大角度相机运动下的时序一致性。

### 时间打包推理

不同相机轨迹间存在视场重叠区域（图3），时间打包推理利用这一特性增强多视图一致性。对于已生成的先验轨迹视频 $\widetilde{V}^a$ 及其掩码 $\mathbf{M}^a$，按修复面积选取Top-K帧作为先验：

$$\mathbf{F} = \mathrm{top\text{-}k\text{-}argmax}(S[\widetilde{V}^a, \mathbf{M}^a]) \tag{7}$$

将先验帧的patchify编码与当前洞视频 $\mathbf{V}^b$ 沿时间维度拼接，输入模型：

$$x_{input} = [\mathrm{patchify}(\mathcal{E}(\mathbf{F})), \mathrm{patchify}(\mathcal{E}(\mathbf{V}^b))]_{\mathrm{temporal}} \tag{8}$$

借助预训练模型的全局时空自注意力机制，先验帧为当前轨迹的遮挡区域提供多视图上下文约束，从而提升生成结果的多视图一致性。

## 实验与关键发现

### 主要结果

EasyCreator 在涵盖真实场景视频、生成视频、合成基准及挑战性相机运动的多个测试集中，均取得了全面领先的性能。在 VBench 综合基准（40 段真实视频 + 40 段高质量生成视频）上，本文方法的总体一致性指标达到 **0.2915**，显著优于第二名的 **TrajectoryCrafter**（0.2463），提升幅度为 +0.0452（Table 1）。在 Kubric-4D 合成数据集上，PSNR 达到 **22.15**，远超 TrajectoryCrafter 的 15.82，绝对增益高达 +6.33 dB（Table 3）。

![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_mU8Ubd8aNK/figures/006_Table_1.jpg]]
*Table 1: VBench results between ours and baselines. We collect a comprehensive video benchmark with 40 real-world videos and 40 high-quality generated videos to evaluate the performance. Red stands for the best result, Blue stands for the second best result*

![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_mU8Ubd8aNK/figures/008_Table_3.jpg]]
*Table 3: Comparison results on Kubric-4D. Red and Blue denote the best and second best results*

从视觉质量与多视图一致性维度看，EasyCreator 同样表现最优。在定量对比中，FID 降至 **58.26**（TrajectoryCrafter 为 61.57），FVD 降至 **145.71**（TrajectoryCrafter 为 154.23），均取得最佳结果（Table 2）。针对真实场景视频，FID 为 **59.14**，优于 TrajectoryCrafter 的 62.49；在长视频（>30 帧）条件下，FVD 为 **165.71**，同样优于 TrajectoryCrafter 的 174.23；在挑战性相机运动（大视角、快速运动）下，FID 为 **65.32**，领先 TrajectoryCrafter 达 5.94（Table 5）。

![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_mU8Ubd8aNK/figures/016_Table_5.jpg]]
*Table 5: Quantitative comparison on challenge camera motion videos (including challenging viewpoints, larger camera motions, and faster camera movements). We assess visual quality, camera accuracy, and view synchronization. Red stands for the best result, Blue stands for the second best result*

![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_mU8Ubd8aNK/figures/013_Table_2.jpg]]
*Table 2: Comparison using WAN-2.1 backbone. (re-implemented baselines). We select two SOTA approaches, ReCapture (Zhang et al., 2024a) and Reangle-A-Video (Jeong et al., 2025) for fair comparison. Red stands for the best result, Blue stands for the second best result*

为确保对比公平性，论文在 WAN-2.1 统一骨干上重新实现了 **ReCapture**（Zhang et al., 2024a）和 **Reangle-A-Video**（Jeong et al., 2025），EasyCreator 在所有指标上仍保持最优（Table 2, WAN-2.1 backbone）。用户研究同样证实，EasyCreator 的平均排名最优（Table 1, User Study）。

### 消融实验

消融实验系统验证了三个核心设计组件的关键作用，结果汇总于 Table 4。

![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_mU8Ubd8aNK/figures/009_Table_4.jpg]]
*Table 4: Quantitative ablation results. Red and Blue denote the best and second best results*

**组合掩码微调（Composite Mask Tuning）** 是方法可行的基础。去除该组件后，模型无法完成 4D 视频生成与编辑任务，视觉质量大幅退化：FID 从 58.26 攀升至 **78.27**，FVD 从 145.71 升至 153.28，CLIP-T 从 33.23 降至 30.81（Table 4, W/o composite mask tuning）。定性结果（Figure 6a）进一步显示，缺乏组合掩码时生成结果出现严重的时序不一致与伪影。

**自迭代调优（Self-Iterative Tuning）** 对大角度相机运动下的时序一致性至关重要。移除该策略后，FVD 从 145.71 升至 **197.24**，FVD-V 从 119.52 升至 157.25，CLIP-V 从 89.87 降至 83.76（Table 4, W/o iterative tuning）。Figure 6b 的视觉对比表明，无自迭代调优时大角度运动下的时序连贯性显著恶化。

**时间打包推理（Temporal-Packing Inference）** 是保障多视图一致性的核心推断策略。去除该策略后，FVD-V 从 119.52 升至 **137.64**，CLIP-V 从 89.87 降至 **84.71**（Table 4, W/o temporal pack strategy）。Figure 7 的消融可视化显示，时间打包推理有效利用了不同相机轨迹间的重叠区域，显著提升了多视图生成的一致性。

此外，关于文本提示与首帧编辑的消融表明，仅使用文本提示或仅使用首帧编辑均不如两者结合的方法，本文方法通过融合两种模态取得了最佳结果（Figure 4, Ablation text+edit）。

### 失败模式与局限性

EasyCreator 的失败模式主要源于其依赖链中的上游组件。首先，**不真实的首帧编辑**和**不准确的视频分割**会直接传播到后续生成管线，导致 4D 输出中出现语义错误或边界伪影。这一问题继承自基础模型的能力边界，需依赖分割与编辑技术的进步来改善（Figure 3, Limitation）。

其次，作为**基于拟合的方法**，EasyCreator 需要为每个特定视频进行单独优化，相比一次性调优方法更耗时（约 2 小时），尽管其资源需求相对较低。使用 WAN 模型作为基础模型导致 LoRA 优化时间较长，未来需探索更高效的加速策略。

第三，方法**无法处理自由风格的输入视频**（如缺乏相机参数的视频），受限于预训练基础模型对相机参数等结构化输入的需求。深度估计误差在极端遮挡或高度动态场景下仍可能影响点云质量，进而降低生成结果的几何一致性。

## 定位与知识库关联

### 与现有工作的关系

EasyCreator 将 4D 视频生成重新定义为视频修复任务，这一核心决策使其与现有方法在范式上产生根本差异。传统 4D 生成方法通常依赖显式 3D 表示（如 NeRF、3D Gaussian Splatting）或多视图扩散模型，而 EasyCreator 选择在预训练视频修复基础模型（Wan2.1-14B）之上进行轻量适配，从而绕过了对昂贵 3D 监督的需求。

在相机控制生成领域，EasyCreator 与以下方法形成直接对比：

- **TrajectoryCrafter**（YU et al., 2025）采用双重投影策略进行相机重定向，但缺乏 EasyCreator 的自迭代调优与时间打包推理机制，导致在大角度相机运动下时序一致性显著下降（FVD 差距约 8.52）。
- **ReCapture**（Zhang et al., 2024a）和 **Reangle-A-Video**（Jeong et al., 2025）代表基于拟合的相机控制方法。为公平比较，EasyCreator 在统一 Wan2.1 骨干上重新实现了这两个基线，结果仍显示 EasyCreator 在多视图一致性和视觉质量上具有明显优势。
- **ReCamMaster**（Bai et al., 2025）和 **SynCammaster**（Bai et al., 2024）分别关注相机重定向和多视图视频生成，但均未将任务建模为视频修复问题，因此在编辑灵活性和 4D 一致性上受限。
- **GCD**（Hoorick et al., 2024）作为 4D 新视图合成基线，缺乏对视频时序建模的能力。

在场景编辑方面，**PaintScene4D** 等方法通常需要显式场景表示，而 EasyCreator 通过组合掩码中的编辑掩码直接支持首帧编辑与文本提示编辑，无需额外场景重建步骤。

### 适用边界

EasyCreator 的适用性受以下条件约束：

1. **输入视频要求**：方法依赖 DepthCrafter 估计逐帧深度并反投影为动态点云，因此要求输入视频具有可估计的深度信息。对于缺乏纹理、存在严重运动模糊或极端光照的场景，深度估计质量下降会导致点云精度不足，进而影响掩码构建和渲染质量。

2. **相机参数依赖**：框架假设输入视频具有已知或可估计的相机内参 $\mathbf{K}$。对于无相机参数的自由风格视频（如手持拍摄、未知焦距），方法无法直接应用，需依赖额外的相机标定步骤。

3. **编辑质量上限**：首帧编辑依赖于外部编辑工具（如图像修复或生成模型），不真实的首帧编辑会直接传播到后续生成帧。同样，文本提示编辑的效果受限于基础模型 Wan2.1 的语言理解与生成能力。

4. **动态场景鲁棒性**：方法使用动态点云作为中间表示，但对于包含快速非刚性变形、复杂遮挡或透明物体的场景，点云投影可能产生不完整的可见性掩码，导致修复区域出现伪影。

5. **计算资源**：作为基于拟合的方法，EasyCreator 为每个特定视频进行 LoRA 微调（约 2000 步，2 小时），相比一次性调优方法更耗时。虽然资源需求低于全参数微调，但限制了实时或大规模部署场景。

### 局限与开放问题

**已识别的局限性：**

- **基础模型继承缺陷**：EasyCreator 的视频修复能力完全建立在 Wan2.1-14B 之上，因此继承了该模型的所有局限性，包括对复杂语义理解的不稳定性、长视频生成中的漂移问题，以及对分布外掩码模式的泛化不足。
- **深度估计敏感**：消融实验（Table 7）表明，使用不同深度估计器（Marigold vs. Depth Anything）会导致性能波动，说明方法对深度估计质量存在依赖。在极端遮挡或动态场景下，深度估计误差的上限尚不明确。
- **自迭代调优的收敛性**：自迭代调优通过逐步增加视角角度（间隔 10°）来扩展模型能力，但该过程的收敛性缺乏理论保证。当目标视角过大时，几何扭曲函数 $\psi(\cdot)$ 产生的伪影可能被错误地作为训练信号，导致误差累积。
- **时间打包推理的局限性**：时间打包策略假设不同相机轨迹之间存在足够重叠区域（如 Figure 3 所示）。当相机运动幅度过大导致重叠区域过小时，Top-K 帧选择策略可能无法提供有效的多视图先验，推理退化为独立生成。

**开放问题：**

1. **泛化性扩展**：当前自迭代调优针对单个视频进行优化。是否可以将该过程推广到多视频/多场景联合训练，以学习更通用的 4D 生成先验，减少单视频优化时间？

2. **效率优化**：LoRA 微调 2 小时的耗时能否通过模型蒸馏、更高效的参数高效微调方法（如 AdaLoRA、DoRA）或推理阶段加速策略（如 FlashAttention、token 剪枝）显著缩短？

3. **自由风格视频支持**：如何将框架扩展到无相机参数的自由风格视频？是否可以通过联合优化相机参数和修复模型来实现端到端处理？

4. **动态场景建模**：当前点云表示对非刚性变形和快速运动建模能力有限。引入可学习的变形场或运动先验是否能提升动态场景下的修复质量？

5. **多模态编辑融合**：文本提示与首帧编辑的最佳融合策略是什么？消融实验（Figure 4）表明两者结合优于单独使用，但其协同机制尚缺乏深入分析。

6. **评估基准完善**：当前评估依赖 VBench、Kubric-4D 等合成或半合成数据集。真实场景下的 4D 生成质量评估缺乏统一的基准和指标，特别是对于多视图一致性的感知评价。

## 原文 PDF

![[paperPDFs/ICLR_2026/EasyCreator_Empowering_4D_Creation_through_Video_Inpainting_0433338d18d5.pdf]]
