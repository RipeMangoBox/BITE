---
title: "PAM: A Pose-Appearance-Motion Engine for Sim-to-Real HOI Video Generation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/PAM_A_Pose_Appearance_Motion_Engine_for_Sim_to_Real_HOI_Video_Generation.pdf
project_link: https://gasaiyu.github.io/PAM.github.io/
code_link: https://github.com/black-forest-labs/flux
aliases:
- PPAME
- PAM
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 通过多模态条件（深度图、语义分割、手部关键点）桥接仿真和真实域，设计分阶段解耦的生成引擎，无需真实第一帧，仅需初始和目标姿态及物体几何作为输入。
primary_logic: 将复杂的高维 HOI 视频生成任务解耦为三个顺序阶段——姿态生成、外观生成、运动生成，每个阶段专注于不同属性，并通过统一的多模态条件（几何、语义、姿态）驱动，显著提升可控性和真实感，同时打破传统方法对真实第一帧的依赖。
claims:
- 在 DexYCB 数据集上，PAM 的 FVD 为 29.13，显著优于 InterDyn 的 38.83，且生成分辨率更高（480×720 vs. 256×384）。
- 在 DexYCB 上，PAM 的 MPJPE 为 19.37 mm，相比 CosHand 的 30.05 mm 降低了 35.5%。
- 在 OAKINK2 数据集上，全多条件模型将 FVD 从 CosHand 的 68.76 降低到 46.31。
- 多条件消融实验表明，同时使用深度、分割和关键点始终获得最佳性能（FVD, LPIPS, MPJPE）。
---

# PAM: A Pose-Appearance-Motion Engine for Sim-to-Real HOI Video Generation

> [!tip] 核心洞察
> 将复杂的高维 HOI 视频生成任务解耦为三个顺序阶段——姿态生成、外观生成、运动生成，每个阶段专注于不同属性，并通过统一的多模态条件（几何、语义、姿态）驱动，显著提升可控性和真实感，同时打破传统方法对真实第一帧的依赖。

| 字段 | 内容 |
|------|------|
| 中文题名 | PAM：仿真到真实手物交互视频生成的姿态-外观-运动引擎 |
| 英文题名 | PAM: A Pose-Appearance-Motion Engine for Sim-to-Real HOI Video Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Gao_PAM_A_Pose-Appearance-Motion_Engine_for_Sim-to-Real_HOI_Video_Generation_CVPR_2026_paper.html) · [Project](https://gasaiyu.github.io/PAM.github.io/) · [Code](https://github.com/black-forest-labs/flux) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | PAM (Pose-Appearance-Motion Engine) |
| Dataset | DexYCB, OAKINK2 |

> [!tip] 效果简介
> - DexYCB 上，FVD (↓) 29.13 vs 38.83 (InterDyn) (减少 9.70 (相对 25.0%))；MPJPE (mm, ↓) 19.37 vs 30.05 (CosHand) (减少 10.68 mm (35.5%))。
> - OAKINK2 上，FVD (↓) 46.31 vs 68.76 (CosHand) (减少 22.45)。

## 概要

**问题瓶颈**：现有手物交互（HOI）生成方法各自独立——姿态合成、外观生成、视频生成分属不同范式，且视频生成方法依赖完整的姿态序列和真实第一帧输入，无法实现真正的仿真到真实（sim-to-real）迁移，严重制约了可扩展的 HOI 数据生成。

**核心思路**：PAM 提出将高维 HOI 视频生成任务解耦为三个顺序阶段——姿态生成、外观生成、运动生成，每个阶段专注于不同属性，并通过统一的多模态条件（深度图、语义分割、手部关键点）桥接仿真域与真实域。整个引擎仅需初始与目标姿态及物体几何作为输入，无需真实第一帧，从根本上打破了传统方法对真实图像的依赖。

**方法定位**：PAM 属于三阶段解耦的仿真到真实 HOI 视频生成引擎。与仅预测姿态轨迹的方法（Pose-Only）、仅生成静态外观的方法（Appearance-Only）、以及需要完整姿态序列与真实第一帧的视频生成方法（如 **CosHand** (Sudhakar et al., ECCV 2024)、**InterDyn**、**ManiVideo** (Pang et al., CVPR 2025)）相比，PAM 首次在无需真实第一帧的条件下实现了从仿真姿态序列到真实视频的端到端迁移。

**主要结果**：
- 在 DexYCB 数据集上，PAM 的 FVD 为 29.13，显著优于 InterDyn 的 38.83，且生成分辨率更高（480×720 vs. 256×384）；MPJPE 为 19.37 mm，相比 CosHand 的 30.05 mm 降低 35.5%。
- 在 OAKINK2 数据集上，PAM 将 FVD 从 CosHand 的 68.76 降低至 46.31。
- 消融实验证实，同时使用深度、分割和关键点三种条件在所有指标上均取得最佳性能。
- 下游任务验证：使用 50% 真实数据加上 PAM 生成的 3400 个合成视频，手部姿态估计模型可达到与 100% 真实数据基线相同的 PA-MPJPE（5.5 mm），证明了合成数据的实用价值。



### 手物交互视频生成的困境

手物交互（Hand-Object Interaction, HOI）视频生成在机器人操作学习、虚拟现实和增强现实中具有重要价值。高质量 HOI 视频能够为下游任务（如手部姿态估计、机器人策略学习）提供可扩展的训练数据。然而，真实世界中采集大规模、标注完备的 HOI 视频成本极高，这催生了从仿真向真实域迁移（sim-to-real）的生成需求。

当前 HOI 合成领域存在三种主要范式，但各自存在根本性局限，无法构成完整的 sim-to-real 链路：

- **姿态合成（Pose-Only Synthesis）**：仅预测 MANO 手部参数轨迹，不生成像素级视觉数据。这无法为需要 RGB 输入的下游视觉模型提供训练信号。
- **外观生成（Appearance Generation）**：基于掩码或 2D 线索生成单帧外观，但缺乏动态运动信息，无法刻画手物交互的时间演化过程。
- **运动生成（Motion Generation）**：如 **InterDyn** 和 **ManiVideo**（Pang et al., CVPR 2025）等方法需要完整的姿态序列和真实第一帧（ground-truth first frame）作为输入。这一依赖从根本上切断了仿真域向真实域的迁移路径——仿真器可提供姿态序列，但无法提供真实第一帧。

### 核心瓶颈：对真实第一帧的依赖

上述运动生成方法的共同瓶颈在于对真实第一帧的硬性依赖。在 sim-to-real 场景下，目标恰恰是从仿真条件（初始手部姿态、物体几何、目标姿态）直接生成真实域视频，而真实第一帧正是待生成的未知量。这一“先有鸡还是先有蛋”的困境使得现有方法无法实现真正的仿真到真实迁移，阻碍了可扩展的 HOI 数据生成流水线的构建。

### 本文动机与核心洞察

PAM 的核心洞察是：将复杂的高维 HOI 视频生成任务解耦为三个顺序阶段——姿态生成、外观生成、运动生成，每个阶段专注于不同属性，并通过统一的多模态条件（几何、语义、姿态）驱动。这一设计带来两个关键突破：

1. **打破第一帧依赖**：外观模块直接合成第一帧，运动模块基于合成第一帧生成全视频，整个流水线仅需初始与目标姿态及物体几何作为输入。
2. **多模态桥接仿真与真实域**：深度图、语义分割、手部关键点三类条件在仿真器中可精确渲染，在真实域中可估计或标注，构成了跨越域差异的稳定信号桥梁。

通过这一解耦设计，PAM 首次实现了无需任何真实帧输入的完整 HOI 视频生成引擎，为 sim-to-real 数据扩展提供了可行的技术路径。



## 核心方法与创新机理

### 1. 范式级创新：从依赖真实第一帧到仿真-真实域迁移

现有手物交互（HOI）视频生成方法存在根本性局限：**ManiVideo**（Pang et al., CVPR 2025）需要完整姿态序列与真实第一帧作为输入，**InterDyn** 同样依赖真实第一帧与手部掩码序列，**CosHand**（Sudhakar et al., ECCV 2024）虽以手部掩码为主要条件，但仍需真实图像作为起点。这些方法本质上无法实现真正的仿真到真实（sim-to-real）迁移——即从仿真引擎生成的姿态序列直接产生逼真的真实世界视频。

PAM 的核心范式突破在于**彻底移除对真实第一帧的依赖**。其生成模型映射为：

$$f_{\pmb{\theta}} : ( \mathbf{h}_0, \mathbf{m}, \mathbf{o}_0, \mathbf{h}_T ) \rightarrow \{ I_t \}_{t=0}^T$$

仅需初始手部姿态 $\mathbf{h}_0$、物体网格 $\mathbf{m}$（无外观信息）、初始物体姿态 $\mathbf{o}_0$ 和目标手部姿态 $\mathbf{h}_T$ 作为输入，即可生成完整的照片级真实视频序列。这一设计使得仿真引擎输出的姿态序列可直接转换为真实域视频，打通了 sim-to-real 的数据生成闭环。

### 2. 架构创新：三阶段解耦生成策略

PAM 将高维 HOI 视频生成任务解耦为三个顺序阶段，每个阶段专注于不同属性：

| 阶段 | 功能 | 核心技术 |
|------|------|----------|
| **姿态生成** | 基于初始/目标姿态和物体网格，插值生成完整的 HOI 姿态序列 | 预训练 GraspXL 模型 |
| **外观生成** | 在多模态条件下合成真实感第一帧图像 | Flux + ControlNet |
| **运动生成** | 将姿态序列渲染为全视频序列 | CogVideoX + ControlNet |

这种解耦设计的因果逻辑在于：姿态、外观、运动是 HOI 视频的三个正交属性，端到端建模会导致可控性下降和训练难度上升。分阶段处理使得每个模块可以专注于自身子任务，同时通过统一的多模态条件（深度图、语义分割、手部关键点）保持跨阶段一致性。

### 3. 条件设计创新：多模态桥接仿真与真实域

与基线方法仅使用手部掩码（CosHand）或掩码序列（InterDyn）不同，PAM 引入了**三通道多模态条件**：

- **深度图**：提供手物几何结构信息，桥接仿真渲染与真实场景的空间关系
- **语义分割**：提供物体和手部的语义边界，增强外观生成的区域一致性
- **手部关键点**：提供精确的手部姿态约束，保证生成视频的几何精度

条件注入采用 ControlNet 机制，将 VAE 编码后的多条件潜变量通道拼接，通过零卷积注入 DiT 模块：

$$f_l = f_l + \mathcal{Z}(f_l')$$

消融实验（Table 3）证实，同时使用三种条件在所有指标（FVD、LPIPS、MPJPE）上均优于任何单一或双条件组合，验证了多模态条件互补的必要性。

### 4. 关键指标突破

PAM 的创新在定量指标上得到充分验证：

- **FVD**：DexYCB 上 29.13 vs. InterDyn 38.83（降低 25.0%），OAKINK2 上 46.31 vs. CosHand 68.76（降低 32.6%）
- **MPJPE**：DexYCB 上 19.37 mm vs. CosHand 30.05 mm（降低 35.5%）
- **分辨率**：生成 480×720 视频，显著高于 InterDyn 的 256×384

这些提升源于解耦架构与多模态条件的协同作用——外观模块保证视觉质量，运动模块保证时序一致性，多条件保证几何精度。

### 5. 下游任务验证：合成数据的实用价值

PAM 的创新不仅体现在生成质量上，更体现在合成数据的实际效用。在 DexYCB 数据集上，使用 **50% 真实数据 + PAM 生成的 3400 个合成视频**训练 SimpleHand 手部姿态估计模型，可达到与 100% 真实数据基线相同的 PA-MPJPE（5.5 mm）。这一结果直接证明了 PAM 在可扩展 HOI 数据生成中的实用价值，为仿真到真实的数据增强提供了可行路径。



### 问题定义与核心映射

PAM 的目标是实现仿真到真实（sim-to-real）的手物交互（HOI）视频生成。给定初始手部姿态 $\mathbf{h}_0$、物体网格 $\mathbf{m}$（不含外观）、初始物体 6-DoF 姿态 $\mathbf{o}_0$ 和目标手部姿态 $\mathbf{h}_T$，生成模型学习一个映射：

$$f_{\pmb{\theta}} : ( \mathbf{h}_0, \mathbf{m}, \mathbf{o}_0, \mathbf{h}_T ) \rightarrow \{ I_t \}_{t=0}^T$$

该映射输出一段照片级真实的 RGB 视频帧序列 $\{I_t\}_{t=0}^T$。与传统方法的关键区别在于，PAM **不需要真实第一帧**作为输入——这一设计打破了现有 HOI 视频生成方法（如 InterDyn、ManiVideo）对真实第一帧的依赖，使仿真域的姿态序列可以直接迁移为真实域视频。

### 三阶段解耦生成策略

面对高维 HOI 视频生成任务的复杂性，PAM 将其解耦为三个顺序阶段，每个阶段专注于不同属性：

1. **姿态生成（Pose Generation）**：基于初始/目标姿态和物体网格，利用预训练模型生成插值的 HOI 姿态序列。
2. **外观生成（Appearance Generation）**：在多模态条件（深度图、语义分割、手部关键点）驱动下，合成真实的第一帧图像。
3. **运动生成（Motion Generation）**：将姿态序列和多模态条件渲染为完整的视频序列。

这一解耦设计的核心洞察在于：姿态、外观和运动是 HOI 视频的三个正交属性，分阶段处理可以显著提升可控性和真实感，同时降低端到端建模的难度。

### 多模态条件桥接仿真与真实域

PAM 通过统一的多模态条件来桥接仿真域和真实域。具体而言，三个条件信号包括：

- **深度图（Depth map）**：提供手物几何的空间结构信息；
- **语义分割（Semantic segmentation）**：提供手、物体和背景的语义类别信息；
- **手部关键点（Hand keypoints）**：提供手部姿态的精确几何约束。

这些条件从仿真渲染或数据集标注中获取，在三个生成阶段中均被用作控制信号。ControlNet 将条件 VAE 编码后在通道维度拼接，注入到 DiT 块的零卷积层中：

$$f_l = f_l + \mathcal{Z}(f_l')$$

其中 $f_l$ 为第 $l$ 个 DiT 块的输出，$f_l'$ 为复制块处理条件后的输出，$\mathcal{Z}(\cdot)$ 为零卷积操作。

### 与传统范式的对比

Figure 2 将 PAM 与三种现有 HOI 合成范式进行了对比：

![[assets/figures/papers/paper_list_l5_https_openaccess_thecvf_com_content_CVPR2026_html_Gao_PAM_A_Pose_Appeara/figures/002_Figure_2.jpg]]
*Figure 2: Overview of Four Approaches to HOI Synthesis. (a) Pose-Only Synthesis [78]: This method predicts the MANO trajectories without generating pixel data; (b) Apperance Generation [82]: This approach generates appearance based on masks or 2D cues but lacks dynamic motion; (c) Motion Generation [3, 48]: These methods require both the full pose sequence and the groundtruth first frame as inputs, limiting their application for true simto-real transfer. (d) Our Pipeline PAM: In this approach, video generation does not rely on the first frame or the whole HOI pose sequence, allowing for the transfer of HOI pose sequences from the simulator to real-world videos*

- **仅姿态合成（Pose-Only Synthesis）**：仅预测 MANO 轨迹，不生成像素数据；
- **外观生成（Appearance Generation）**：基于掩码或 2D 线索生成外观，但缺乏动态运动；
- **运动生成（Motion Generation）**：需要完整姿态序列和真实第一帧作为输入，限制了真正的 sim-to-real 迁移。

PAM 的独特之处在于：视频生成既不依赖真实第一帧，也不需要完整的 HOI 姿态序列，从而实现了从仿真器到真实世界视频的真正迁移。这一设计使 PAM 成为首个统一姿态-外观-运动的 sim-to-real HOI 视频生成引擎。

### 补充图表

![[assets/figures/papers/paper_list_l5_https_openaccess_thecvf_com_content_CVPR2026_html_Gao_PAM_A_Pose_Appeara/figures/003_Figure_3.jpg]]
*Figure 3: Overview of our three-stage generation pipeline. (1) Pose Generation: A pretrained pose generation model generates the intermediate hand-object interaction (HOI) poses based on the initial and target poses, along with the object mesh. (2) Appearance Generation: A controllable image diffusion model synthesizes the first frame of the video, conditioned on multi-modal inputs (depth maps, semantic masks, and keypoint annotations). (3) Motion Generation: The generated HOI sequence and the first frame are rendered into a full video sequence by a video diffusion model, conditioned on the same multi-modal inputs used in the appearance generation stage*



PAM 将高维手物交互视频生成任务解耦为三个顺序阶段：姿态生成、外观生成、运动生成。每个阶段专注于不同属性，并通过统一的多模态条件驱动，实现从仿真姿态序列到真实视频的迁移。

### 整体生成映射

给定初始 MANO 手部姿态 $\mathbf{h}_0$、无外观的物体网格 $\mathbf{m}$、初始 6-DoF 物体姿态 $\mathbf{o}_0$ 以及目标手部姿态 $\mathbf{h}_T$，PAM 的生成模型定义为：

$$f_{\pmb{\theta}} : ( \mathbf{h}_0, \mathbf{m}, \mathbf{o}_0, \mathbf{h}_T ) \rightarrow \{ I_t \}_{t=0}^T$$

该映射将上述四元组输入转换为长度为 $T$ 的 RGB 视频帧序列 $\{I_t\}_{t=0}^T$。与现有方法不同，该映射不依赖真实第一帧，仅需初始与目标姿态及物体几何即可完成生成。

### 阶段一：姿态生成模块

姿态生成模块基于预训练模型 **GraspXL**，以初始手部姿态 $\mathbf{h}_0$、目标手部姿态 $\mathbf{h}_T$ 和物体网格 $\mathbf{m}$ 为输入，插值生成完整的 MANO 手物交互姿态序列。该阶段输出 $\{ \mathbf{h}_t \}_{t=0}^T$，为后续外观和运动生成提供几何先验。

### 阶段二：外观生成模块

外观生成模块基于 **Flux** 扩散模型与 **ControlNet** 分支，在三种多模态条件引导下合成视频的第一帧 $I_0$。三种条件分别为：

- **深度图** $D_0$：由 DepthCrafter 从姿态序列估计得到；
- **语义分割图** $S_0$：来自数据集标注；
- **手部关键点图** $K_0$：由 MANO 姿态渲染获得。

这些条件首先经 VAE 编码至 $\frac{H}{8} \times \frac{W}{8} \times 16$ 的潜在空间，在通道维度拼接后注入 DiT 模块的两个特定层。注入方式遵循 ControlNet 的标准范式：

$$f_l = f_l + \mathcal{Z}(f_l')$$

其中 $f_l$ 为原始 DiT 第 $l$ 层的输出，$f_l'$ 为处理条件的复制 DiT 块输出，$\mathcal{Z}(\cdot)$ 表示零初始化卷积操作。这一设计使得训练初期条件分支输出为零，模型从预训练权重平滑启动。

### 阶段三：运动生成模块

运动生成模块基于 **CogVideoX** 视频扩散模型与 ControlNet，将阶段一生成的姿态序列 $\{ \mathbf{h}_t \}_{t=0}^T$ 与阶段二生成的合成第一帧 $I_0$ 作为输入，在相同的深度、语义、关键点多模态条件驱动下，渲染生成完整的视频序列 $\{ I_t \}_{t=0}^T$。该阶段负责确保时序连贯性和手物交互的运动一致性。

### 运动保真度评估指标

为量化生成视频中手部运动的准确性，论文提出运动保真度（Motion Fidelity, MF）指标。首先定义两条轨迹 $\tau$ 与 $\tilde{\tau}$ 在 $F$ 帧上的位移相关性：

$$\mathbf{corr}(\tau, \tilde{\tau}) = \frac{1}{F} \sum_{k=1}^{F} \frac{\mathbf{v}_k \cdot \tilde{\mathbf{v}}_k}{\|\mathbf{v}_k\| \|\tilde{\mathbf{v}}_k\|}$$

其中 $\mathbf{v}_k$ 和 $\tilde{\mathbf{v}}_k$ 分别为第 $k$ 帧的位移向量。该式衡量两条轨迹在速度方向上的平均余弦相似度。

基于此，运动保真度对称地计算真实轨迹集合 $\mathcal{T}$ 与生成轨迹集合 $\tilde{\mathcal{T}}$ 之间的最大相关性均值：

$$\mathbf{MF} = \frac{1}{|\tilde{\mathcal{T}}|} \sum_{\tilde{\tau} \in \tilde{\mathcal{T}}} \max_{\tau \in \mathcal{T}} \mathbf{corr}(\tau, \tilde{\tau}) + \frac{1}{|\mathcal{T}|} \sum_{\tau \in \mathcal{T}} \max_{\tilde{\tau} \in \tilde{\mathcal{T}}} \mathbf{corr}(\tau, \tilde{\tau})$$

该指标同时惩罚生成轨迹中缺少真实运动模式（第一项）和真实轨迹中运动模式未被生成覆盖（第二项）的情况，全面评估运动保真度。

### 关键设计要点

三个阶段的解耦设计使得每个模块可独立优化和替换：姿态生成专注运动合理性，外观生成专注视觉真实感，运动生成专注时序连贯性。多模态条件（深度、语义、关键点）贯穿外观与运动两阶段，形成统一的几何-语义-姿态表示空间，是实现仿真到真实域迁移的核心机制。消融实验（Table 3）证实，三种条件联合使用在所有指标（FVD、LPIPS、MPJPE）上均优于单一或两条件组合，验证了多模态互补信息的必要性。

### 补充图表

![[assets/figures/papers/paper_list_l5_https_openaccess_thecvf_com_content_CVPR2026_html_Gao_PAM_A_Pose_Appeara/figures/001_Figure_1.jpg]]
*Figure 1: (a) Pose Generation. Given an initial and target hand–object pose, our pose generation module synthesizes a full MANO-based HOI trajectory. (b) Appearance Generation. Conditioned on rendered hand–object geometry, the appearance model produces diverse and realistic reference frame. (c) Motion Generation. Using the same rendered conditions, the motion model generates the full HOI video with coherent dynamics and hand–object interactions. (d) Quality and Downstream Validation. Our unified engine substantially improves video fidelity and geometric accuracy over prior methods*



## 实验与关键发现

### 主实验结果

PAM 在两个主流手物交互基准上进行了全面评估，并与当前最先进的视频生成方法进行了定量对比。评估指标涵盖视频感知质量（FVD, LPIPS）、运动保真度（MF）和手部姿态几何精度（MPJPE）。其中，MPJPE 通过 HaMeR 估计器从生成视频中提取手部关节点，计算与真值之间的平均欧氏距离（根对齐后，单位 mm）。

**DexYCB 数据集**（Table 1）：PAM 在所有指标上均取得最优性能。具体而言，FVD 为 29.13，相比 InterDyn 的 38.83 降低了 9.70（相对提升 25.0%）；MPJPE 为 19.37 mm，相比 CosHand 的 30.05 mm 降低了 10.68 mm（相对提升 35.5%）。值得注意的是，PAM 生成视频的分辨率为 480×720，显著高于 InterDyn 的 256×384 和 CosHand 的 256×256，同时保持了更优的感知质量和几何精度。与需要完整姿态序列和真实第一帧的 ManiVideo 相比，PAM 在仅依赖初始与目标姿态的条件下仍展现出竞争力。

**OAKINK2 数据集**（Table 2）：在更具挑战性的 OAKINK2 子集上，PAM 将 FVD 从 CosHand 的 68.76 降至 46.31，降幅达 22.45。同时，LPIPS 和 MPJPE 也均有显著改善，验证了多模态条件策略在复杂场景下的鲁棒性。

为确保公平比较，CosHand 在与 PAM 相同的 DexYCB s0-split 训练集上进行了微调；OAKINK2 上两者使用相同的训练子集。InterDyn 和 ManiVideo 的结果直接引用自原论文。

### 消融实验

**输入条件消融**（Table 3, Figure 5）：为验证多模态条件融合的有效性，论文在 DexYCB 上对深度图、语义分割图和手部关键点图进行了系统消融。结果表明，同时使用三种条件的全多条件模型在所有指标（FVD, LPIPS, MPJPE）上均取得最佳性能。定性可视化（Figure 5）进一步揭示：仅使用语义掩码或深度图时，生成的手部姿态可能出现几何偏差；仅使用关键点时，外观质量显著下降。三种条件在几何约束、语义理解和姿态引导上形成互补，共同驱动了高质量生成。

### 下游任务验证

**数据增强实验**（Table 4, Figure 7）：PAM 的核心价值在于为下游任务提供可扩展的合成训练数据。论文以手部姿态估计模型 SimpleHand 为下游任务，设计了数据增强实验。基线为使用 100% 真实 DexYCB 数据训练的模型，其 PA-MPJPE 为 5.5 mm。当仅使用 50% 真实数据并辅以 PAM 生成的 3400 个合成视频时，下游模型达到了与 100% 真实数据基线相同的 PA-MPJPE（5.5 mm）。Figure 7 展示了不同真实数据比例（25%、50%、75%、100%）下的增强效果曲线，进一步证实了 PAM 合成数据的有效性和可扩展性。

### 零样本泛化

Figure 8 展示了 PAM 在 OAKINK2 上的零样本图像到视频（i2v）生成结果。模型仅使用 DexYCB 训练权重，无需在 OAKINK2 上微调，即可生成具有合理手物交互和运动一致性的视频序列，初步验证了该框架的跨数据集泛化潜力。

![[assets/figures/papers/paper_list_l5_https_openaccess_thecvf_com_content_CVPR2026_html_Gao_PAM_A_Pose_Appeara/figures/012_Figure_8.jpg]]
*Figure 8: Zero-shot result on OAKINK2 dataset for i2v task. We use the weight trained on DexYCB dataset*

### 失败模式与局限性

尽管 PAM 在主实验和消融中表现优异，论文指出了以下局限性：首先，未讨论模型的计算开销和推理速度，实际部署效率有待量化；其次，当前框架聚焦于单手-单物体场景，尚未扩展到多物体交互或双手协作等更复杂的 HOI 场景；最后，外观生成和运动生成阶段目前为顺序解耦训练，尚未实现端到端联合优化，可能限制了整体生成质量的上限。这些方面需要后续工作进一步探索，当前结论需结合这些限制审慎解读。

### 补充图表

![[assets/figures/papers/paper_list_l5_https_openaccess_thecvf_com_content_CVPR2026_html_Gao_PAM_A_Pose_Appeara/figures/004_Table_1.jpg]]
*Table 1: Quantitative comparison on DexYCB dataset. Our method is evaluated against CosHand, InterDyn, and ManiVideo. Results for InterDyn and ManiVideo are taken from their original papers. For fair comparison, CosHand was fine-tuned on the s0-split training set identical to ours. Our approach achieves state-of-the-art performance across all metrics (FVD, LPIPS, MF, MPJPE) while generating high-resolution 480x720 videos*

![[assets/figures/papers/paper_list_l5_https_openaccess_thecvf_com_content_CVPR2026_html_Gao_PAM_A_Pose_Appeara/figures/005_Table_2.jpg]]
*Table 2: Quantitative results on the OAKINK2 dataset. Comparison of our method with CosHand. For a fair evaluation, both models are trained on the same dataset. Our approach achieves state-of-the-art performance, outperforming CosHand across all evaluated metrics*

![[assets/figures/papers/paper_list_l5_https_openaccess_thecvf_com_content_CVPR2026_html_Gao_PAM_A_Pose_Appeara/figures/006_Table_3.jpg]]
*Table 3: Ablation study on input conditions on DexYCB dataset*

![[assets/figures/papers/paper_list_l5_https_openaccess_thecvf_com_content_CVPR2026_html_Gao_PAM_A_Pose_Appeara/figures/010_Table_4.jpg]]
*Table 4: Downstream task evaluation on SimpleHand [92]*

![[assets/figures/papers/paper_list_l5_https_openaccess_thecvf_com_content_CVPR2026_html_Gao_PAM_A_Pose_Appeara/figures/007_Figure_4.jpg]]
*Figure 4: Qualitative comparison against CosHand. Example results on DexYCB and OAKINK2 highlight the strengths of our method in two key areas: (1) higher visual fidelity in both foreground and background generation, and (2) improved geometric accuracy of the synthesized hand poses*

![[assets/figures/papers/paper_list_l5_https_openaccess_thecvf_com_content_CVPR2026_html_Gao_PAM_A_Pose_Appeara/figures/011_Figure_7.jpg]]
*Figure 7: Data augmentation analysis with varying ratios of real data. We augment different portions of the DexYCB training set (25%, 50%, 75%, 100%) with our generated synthetic data. The baseline (dashed line) indicates performance when training solely on 100% of the real DexYCB data without synthetic augmentation*

![[assets/figures/papers/paper_list_l5_https_openaccess_thecvf_com_content_CVPR2026_html_Gao_PAM_A_Pose_Appeara/figures/009_Figure_6.jpg]]
*Figure 6: Sim-to-real transfer results. Our pipeline can generate realistic videos given initial and target states with diversity*

![[assets/figures/papers/paper_list_l5_https_openaccess_thecvf_com_content_CVPR2026_html_Gao_PAM_A_Pose_Appeara/figures/008_Figure_5.jpg]]
*Figure 5: Ablation study on input conditions on DexYCB dataset*



## 定位与知识库关联

### 1. 与现有方法的谱系关系

PAM 的核心贡献在于将原本割裂的 HOI 合成子任务统一为一个无需真实第一帧的 sim-to-real 生成引擎。为理解这一贡献的谱系位置，Figure 2 将现有方法归纳为三类范式，PAM 构成了第四类。

**范式一：仅姿态合成（Pose-Only Synthesis）。** 此类方法仅预测 MANO 手部姿态轨迹，不生成任何像素数据。它们解决了“手如何运动”的问题，但无法产生可感知的视觉输出，因此不能直接用于下游视觉任务的数据增强。PAM 的姿态生成模块（Stage I）继承了这一范式的能力，但将其作为整个管线的上游输入，而非最终输出。

**范式二：仅外观生成（Appearance Generation）。** 此类方法基于掩码或二维线索生成静态的手物交互图像，但缺乏动态运动信息。PAM 的外观生成模块（Stage II）在功能上与此类方法对齐，但其关键区别在于：PAM 的外观模块以多模态几何条件（深度图、语义分割、手部关键点）而非简单的掩码作为驱动信号，从而获得更强的几何可控性。

**范式三：运动生成（Motion Generation）。** 此类方法以 **InterDyn** 和 **ManiVideo** (Pang et al., CVPR 2025) 为代表，能够生成完整的 HOI 视频序列。然而，它们存在一个根本性限制：**必须输入完整的姿态序列和真实第一帧**。这意味着它们本质上是“图像到视频”（image-to-video）或“姿态到视频”（pose-to-video）的转换器，无法实现真正的仿真到真实迁移——因为仿真环境中不存在真实第一帧，而完整的姿态序列在仿真中虽然可获得，但无法直接驱动这些模型产生真实感视频。

**范式四：PAM 的解耦 sim-to-real 引擎。** PAM 打破了范式三对真实第一帧的依赖。其核心创新在于：通过多模态条件（深度图、语义分割、手部关键点）作为仿真域与真实域之间的“桥梁表示”，使得外观模块能够从纯几何信息合成逼真的第一帧，进而使运动模块能够基于合成第一帧和姿态序列生成完整视频。这种设计的因果逻辑是：**几何条件（深度、分割、关键点）在仿真和真实域之间具有高度一致性，因此以它们为条件的生成模型天然具备跨域泛化能力。**

在与具体基线的直接对比中：
- **CosHand** (Sudhakar et al., ECCV 2024) 是外观生成范式向视频生成的延伸，主要使用手部掩码作为条件。PAM 在 DexYCB 上将 MPJPE 从 30.05 mm 降至 19.37 mm（降低 35.5%），在 OAKINK2 上将 FVD 从 68.76 降至 46.31，表明多模态几何条件相比单一掩码条件在手部姿态精度和视频质量上均有显著优势。
- **InterDyn** 需要手部掩码序列作为输入，PAM 在 DexYCB 上将 FVD 从 38.83 降至 29.13，且生成分辨率更高（480×720 vs. 256×384）。
- **ManiVideo** 需要完整姿态序列与真实第一帧，PAM 仅需初始和目标姿态，输入需求更宽松。

### 2. 适用边界

PAM 的适用边界由其设计假设和实验覆盖范围共同界定：

**输入假设。** PAM 假设用户能够提供初始手部姿态、目标手部姿态、物体网格以及初始物体姿态。在仿真环境中，这些信息可通过物理引擎直接获取；在真实场景中，初始和目标姿态可通过手动设定或稀疏关键点估计获得。物体网格需要已知的 CAD 模型，这限制了其在完全未知物体上的应用。

**物体交互复杂度。** 论文的实验覆盖了单手操作单个已知物体的场景（DexYCB 和 OAKINK2 数据集中的抓取、操纵动作）。对于多物体交互、双手协作、或涉及非刚性物体的场景，PAM 的有效性尚未验证。这是论文明确指出的局限之一。

**视频质量边界。** 虽然 PAM 在 FVD 和 MPJPE 上取得了显著提升，但生成视频的绝对质量仍受限于底层扩散模型的固有问题（如时序闪烁、细粒度纹理失真）。此外，论文未报告推理速度或计算开销，其实时性和部署可行性需要手动验证。

**sim-to-real 泛化边界。** PAM 的 sim-to-real 能力依赖于深度、分割、关键点等几何条件在域间的一致性。当仿真渲染的几何条件与真实深度估计（使用 DepthCrafter）之间存在系统性偏差时，生成质量可能下降。论文未对此类退化情况进行系统分析。

### 3. 局限与开放问题

**已识别的局限。**

1. **阶段解耦带来的次优性。** 外观生成和运动生成是独立训练的两个阶段，运动模块接收外观模块的输出作为输入，但二者之间没有端到端的梯度流动。这意味着外观模块的生成误差会直接传播到运动模块，且运动模块无法通过反向传播来指导外观模块生成更有利于后续运动的图像。论文明确指出“外观和运动阶段尚未端到端联合优化”是一个待解决的问题。

2. **场景复杂度受限。** 当前实验仅限于单手操作单个已知物体的场景。论文未探索多物体交互、双手协作、工具使用等更复杂的 HOI 场景。这些场景中物体间的遮挡、接触约束和协调运动模式将给姿态生成和外观生成带来新的挑战。

3. **计算开销未量化。** 三阶段管线涉及 GraspXL 姿态生成、Flux 图像生成和 CogVideoX 视频生成三个独立模型，其总体推理时间和显存占用未被报告。对于实际应用，这是一个需要手动验证的关键指标。

4. **对深度估计器的依赖。** 在真实场景中，深度图需通过 DepthCrafter 等工具估计获得。深度估计的误差会直接影响外观和运动模块的条件信号质量，进而影响生成结果的几何精度。

**开放问题。**

1. **如何将运动与外观阶段统一为端到端模型？** 这需要在保持各阶段专业性的同时建立可微的信息通道。可能的路径包括：在外观模块中引入运动感知损失，或设计联合训练策略使两个模块共享部分条件编码器。

2. **如何扩展至更复杂的物体交互和双手协作？** 这要求姿态生成模块能够处理多物体碰撞检测、双手协调约束等更复杂的物理约束，同时外观和运动模块需要能够处理更复杂的遮挡关系和交互动力学。

3. **合成数据在真实机器人操作中的泛化性如何？** 虽然 Table 4 和 Figure 7 展示了合成数据在下游手部姿态估计任务上的数据增强效果（使用 50% 真实数据加 PAM 合成数据可达到与 100% 真实数据相同的 PA-MPJPE 5.5 mm），但这些实验仅限于静态姿态估计。合成视频数据是否能够提升机器人操作策略的学习效果，仍需在真实机器人平台上验证。

4. **多模态条件的冗余性与互补性。** Table 3 的消融实验表明深度、分割和关键点三者联合使用始终最优，但各条件的相对贡献和失效模式尚未被深入分析。理解这一点对于在实际部署中简化条件获取流程（例如，是否可以用更易获取的深度图替代语义分割）具有重要意义。



## 原文 PDF

![[paperPDFs/CVPR_2026/PAM_A_Pose_Appearance_Motion_Engine_for_Sim_to_Real_HOI_Video_Generation.pdf]]
