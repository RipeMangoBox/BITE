---
title: "TraceGen: World Modeling in 3D Trace Space Enables Learning from Cross-Embodiment Videos"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/TraceGen_World_Modeling_in_3D_Trace_Space_Enables_Learning_from_Cross_Embodiment_Videos.pdf
project_link: "https://tracegen.github.io"
code_link: null
aliases:
- TraceGen
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 将世界模型的预测目标从像素空间转移到3D轨迹空间，以抽象掉外观、背景和相机变化，从而专注于操纵所需的几何结构。
primary_logic: 尽管具身在运动学和尺度上不同，但被操纵物体和末端执行器的运动具有共享的、以场景为中心的3D结构，可表示为紧凑的3D轨迹序列，从而忽略外观和背景。
claims:
- 仅用5个目标机器人演示，TraceGen在四个任务上达到80%成功率。
- 仅用5个未校准手持人类视频（不同背景和物体位置），TraceGen在真实机器人上获得67.5%成功率。
- TraceGen的推理速度是视频生成世界模型的50–600×。
- 在大规模跨具身预训练（TraceForge-123K）下，5视频微调达到80%成功率，而从零训练的仅25%。
---

# TraceGen: World Modeling in 3D Trace Space Enables Learning from Cross-Embodiment Videos

> [!tip] 核心洞察
> 尽管具身在运动学和尺度上不同，但被操纵物体和末端执行器的运动具有共享的、以场景为中心的3D结构，可表示为紧凑的3D轨迹序列，从而忽略外观和背景。

| 字段 | 内容 |
|------|------|
| 中文题名 | TraceGen：3D轨迹空间世界建模实现跨具身视频学习 |
| 英文题名 | TraceGen: World Modeling in 3D Trace Space Enables Learning from Cross-Embodiment Videos |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2511.21690) · [Project](https://tracegen.github.io) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | TraceGen |
| Dataset | 4 real-world tasks (Clothes, Ball, Brush, Block) on Franka, 5 robot videos warmup, 4 tasks, 5 handheld human videos warmup, Inference efficiency comparison, Long-horizon Sorting |

> [!tip] 效果简介
> - 4 real-world tasks (Clothes, Ball, Brush, Block) on Franka, 5 robot videos warm... 上，Overall Success Rate 80% vs 0% (NovaFlow Wan2.2 zero-shot) (+80%)。
> - 4 tasks, 5 handheld human videos warmup 上，Overall Success Rate 67.5% vs 0% (From Scratch) (+67.5%)。
> - Inference efficiency comparison 上，Relative speed (predictions per minute) 3.8× faster than trace baselines, >50× faster than video models vs Video generation models (e.g., NovaFlow Veo3.1) (>50×)。

## 概要

**核心问题**：不同具身（人类、各类机器人）、相机视角和环境背景之间的巨大差异，使得跨具身操纵视频难以直接复用。这导致了一个关键瓶颈——无法利用海量的人类活动视频来解决小样本机器人学习问题，因为外观、背景和相机变化淹没了操纵所需的运动结构。

**核心洞察**：尽管具身在运动学和尺度上千差万别，被操纵物体和末端执行器的运动却共享一套以场景为中心的3D几何结构。将世界模型的预测目标从像素空间转移到3D轨迹空间（trace-space），可以抽象掉外观和背景，专注于操纵所必需的几何运动。

**方法定位**：TraceGen 是一个在3D轨迹空间中运行的流模型世界模型。它不生成像素帧，而是预测未来时刻的3D运动轨迹。为支撑大规模训练，配套的 TraceForge 数据流水线将异构的跨具身视频（包括野外人类视频和机器人数据）统一转化为一致的3D轨迹序列，构建了包含 123K 视频、1.8M 观测-轨迹-语言三元组的 TraceForge-123K 数据集。

**主要结果**：
- 仅使用 **5个目标机器人演示** 进行微调，TraceGen 在四个真实世界操纵任务上达到 **80%** 成功率，而视频生成基线（NovaFlow Wan2.2）零样本成功率为 0%。
- 仅使用 **5个未校准手持人类视频**（不同背景和物体位置），TraceGen 在真实机器人上获得 **67.5%** 成功率，从头训练模型为 0%。
- 推理速度比视频生成世界模型快 **50–600倍**，比同类轨迹基线快 3.8 倍。
- 大规模跨具身预训练（TraceForge-123K）是关键：预训练后5视频微调达 80%，而从零训练仅 25%。

**方法谱系与知识库定位**：TraceGen 在具身世界模型领域开辟了“3D轨迹空间预测”这一新范式，区别于主流的像素级视频生成路线（如 **NovaFlow** 系列、**AVDC**）和基于边界框/目标检测的2D轨迹预测方法（如 **3DFlowAction**）。其架构融合了 CogVideoX 的3D变换器骨干、Prismatic-VLM 的多编码器融合策略，以及基于随机插值的流模型生成框架，将世界建模从外观生成重构为几何运动预测。



### 问题背景：跨具身数据复用的核心瓶颈

机器人学习长期面临数据稀缺的困境——在特定机器人平台上采集高质量演示数据成本高昂，而互联网上存在海量的人类操作视频。直觉上，这些人类视频应当能够为机器人提供丰富的运动先验，但实际复用却极为困难。根本瓶颈在于：**不同具身（人手、各类机械臂）、相机视角和操作环境之间存在巨大的视觉差异**，使得在像素空间中直接迁移几乎不可行。视频生成式世界模型试图通过预测未来像素帧来学习通用动力学，但这类方法不可避免地需要建模外观、背景、光照等与操作本质无关的视觉细节，导致泛化能力受限于训练数据的视觉分布。

### 现有方法及其缺口

当前具身世界模型主要沿两条路径展开，但均存在结构性缺陷：

**视频生成世界模型**（如基于扩散模型或自回归变换器的像素预测方法）虽然在视觉保真度上取得了进展，但面临三重困境：（1）**几何幻觉**——模型可能生成视觉上合理但物理上不可行的物体状态，例如物体凭空出现或消失；（2）**推理效率低下**——生成高分辨率视频帧的计算开销极大，单次预测耗时数秒至数十秒，难以满足实时控制需求；（3）**跨域泛化弱**——在实验室固定相机下训练的模型，面对野外手持视频中不同的背景和相机运动时几乎完全失效。

**结构化预测方法**（如基于边界框或2D轨迹的模型）试图通过抽象掉外观来提升泛化性，但引入新的问题：边界框过于粗糙，无法捕捉工具末端或物体关键点的精细运动（Figure 3c-d）；而2D轨迹缺乏深度信息，无法为3D空间中的机器人执行提供足够的几何约束。此外，这些方法通常依赖目标检测器或启发式过滤，在单张图像上容易失败，且难以从跨具身数据中统一学习。

### 核心洞察：3D轨迹空间作为跨具身通用表征

本文的关键洞察在于：**尽管具身在运动学和尺度上千差万别，但被操纵物体和末端执行器的运动在3D空间中共享一个以场景为中心的几何结构**。无论是人手抓取衣物、还是Franka夹爪推动方块，其末端在空间中的运动轨迹都可以被抽象为一系列3D关键点序列——这些序列紧凑地编码了操作所需的全部几何信息，同时天然地忽略了外观、背景、相机参数等无关变量。

这一洞察指向了一个根本性的设计转变：将世界模型的预测目标从像素空间转移到**3D轨迹空间（trace-space）**。在轨迹空间中，不同具身的运动被统一表示为场景坐标系下的3D位移序列，从而使得从人类视频中提取的运动模式可以直接迁移到机器人执行中。这种抽象不仅大幅压缩了预测空间的维度（从百万级像素到数百个3D坐标），还使得模型能够专注于学习操作本身的物理结构，而非视觉表象。

### 本文动机与目标

基于上述洞察，本文提出**TraceGen**——一个在3D轨迹空间中运行的世界模型，以及配套的大规模数据生成流水线**TraceForge**。核心动机是回答一个关键问题：**能否通过跨具身视频的大规模预训练，使模型仅需极少的目标机器人演示（5个）即可达到实用级的操作成功率？**

具体而言，本文致力于解决两个相互关联的挑战：（1）如何从异构的、野外采集的人类和机器人视频中自动提取统一、可靠的3D轨迹监督信号；（2）如何设计一个高效的生成模型架构，在轨迹空间中学习跨具身的运动先验，并支持对新任务和新环境的快速少样本适应。



## 核心方法与创新机理

### 问题瓶颈：跨具身视觉鸿沟

机器人学习长期受困于数据稀缺——高质量机器人演示的采集成本极高。然而，互联网上存在海量的人类操作视频，理论上可作为丰富的学习资源。核心瓶颈在于**不同具身、相机视角和环境背景之间的巨大差异**，使得这些视频无法直接复用：人类手部与机器人夹爪的运动学结构不同，手持相机与固定相机的外参未知，背景和光照千差万别。现有方法试图通过视频生成世界模型在像素空间弥合这一鸿沟，但像素级预测不可避免地耦合了外观、背景等无关因素，导致几何幻觉和跨域泛化失败（Figure 3）。

### 核心洞察：3D轨迹空间作为跨具身不变表征

TraceGen的核心洞察是**将世界模型的预测目标从像素空间转移到3D轨迹空间**。尽管不同具身在运动学和尺度上存在差异，但被操纵物体和末端执行器的运动共享一个以场景为中心的3D结构——无论是一只手还是一只机械臂在推动一个方块，其末端轨迹的几何形态本质上是相似的。通过将这一结构抽象为紧凑的3D轨迹序列（场景级关键点的时空坐标），可以彻底剥离外观、背景和相机参数等干扰因素，从而建立一个真正跨具身的世界模型。

### Changed Slots：相对于基线的关键设计变更

TraceGen相对于现有方法的核心变更体现在四个维度：

**1. 输出空间：从像素帧到3D轨迹**

| 维度 | 基线方法 | TraceGen |
|------|----------|----------|
| 预测目标 | 像素帧（视频生成）或2D轨迹 | 3D轨迹空间 $(x, y, z)$，场景级关键点，无边界框 |
| 外观耦合 | 强耦合，需重建纹理和背景 | 完全解耦，仅保留操纵所需的几何结构 |
| 推理效率 | 视频扩散模型推理缓慢 | 50–600× 加速（Figure 7） |

视频生成世界模型（如 **NovaFlow** 基于Wan2.2或Veo3.1）需要逐帧生成高维像素，不仅计算成本高昂，还容易产生几何幻觉。**3DFlowAction** 虽预测3D轨迹，但依赖目标检测器提取物体边界框，在单张图像上检测器经常失效，且边界框可能遗漏工具或过于宽泛（Figure 3c-d）。TraceGen直接预测场景级3D轨迹，无需显式目标检测，从根源上规避了这些失败模式。

**2. 数据生成：TraceForge统一跨具身流水线**

TraceGen的有效性依赖于大规模、高质量的3D轨迹监督。为此，作者设计了**TraceForge**数据生成流水线（Figure 4），将异构的野外视频转化为一致的3D轨迹，其关键创新包括：

- **相机运动补偿**：通过估计每帧相机位姿和深度，将多视角追踪的3D点重投影到统一的参考相机坐标系下，消除手持相机晃动带来的轨迹噪声。
- **速度重定向**：不同具身的运动速度差异巨大（如人手通常比机械臂快），TraceForge通过速度归一化将具身相关的运动节奏映射到统一尺度，使模型学习到具身无关的运动模式。

这一流水线从123K视频中生成了1.8M个观测-轨迹-语言三元组（TraceForge-123K），规模超过先前工作的15倍（Figure 2），涵盖桌面、第一人称和野外场景。

**3. 模型架构：多编码器融合的流模型**

TraceGen基于**CogVideoX**架构构建，但将其3D Transformer从像素空间适配到轨迹空间，并采用**Prismatic-VLM**的多编码器融合策略（Figure 5）：

- **视觉编码**：RGB图像分别通过DINOv3和SigLIP提取语义和细粒度特征，深度图通过带可学习stem adapter的SigLIP编码器处理，三者拼接后线性投影为统一视觉token：
  $$\mathbf{F}_{\mathrm{vis}} = \mathrm{Concat}(\mathbf{F}_{\mathrm{dino}}, \mathbf{F}_{\mathrm{siglip}}, \mathbf{F}_{\mathrm{depth}}) \in \mathbb{R}^{N \times (D_d + D_s + D_s)}$$
  $$\mathbf{F}_{\mathrm{vis}} = \mathrm{Linear}(\mathbf{F}_{\mathrm{vis}}) \in \mathbb{R}^{N \times D}$$

- **轨迹生成**：采用**随机插值（Stochastic Interpolants）**框架，通过ODE积分从噪声生成3D轨迹。训练时最小化速度场预测与真实速度之间的Score Interpolation Loss：
  $$\mathcal{L}_{\mathrm{SI}} = \mathbb{E}_{\tau, \mathbf{X}^0, \mathbf{X}^1} \left[ \| v_\theta(\mathbf{X}^\tau, \tau, \mathbf{F}_{\mathrm{cond}}) - (\mathbf{X}^1 - \mathbf{X}^0) \|^2 \right]$$
  推理时通过100步ODE积分即可生成轨迹，无需扩散模型的多步去噪。

- **编码器冻结策略**：所有编码器（DINOv3、SigLIP、T5）在训练期间保持冻结，仅训练融合层和解码器，高效利用预训练表征。

**4. 训练策略：大规模跨具身预训练 + 少样本微调**

TraceGen的训练分为两阶段：

- **预训练阶段**：在TraceForge-123K的1.8M三元组上进行大规模跨具身预训练，混合人手视频（Something-Something V2）、机器人数据（Agibot）和野外视频，学习通用的3D运动先验。
- **微调阶段**：仅需5个目标机器人演示视频进行少样本热身微调，即可将预训练先验适配到新任务和新环境。

消融实验证实了这一策略的关键性：仅用跨具身混合数据预训练可达70%成功率，而仅用机器人数据（Agibot）为45%，仅用人手数据（SSV2）为25%（Table 2）；从零训练仅25%，而预训练模型达到80%（Table 1）。

### 创新总结

TraceGen的核心创新在于**将跨具身世界建模的战场从像素空间迁移到3D轨迹空间**，通过TraceForge数据流水线、多编码器流模型架构和大规模预训练策略三个层面的协同设计，实现了从少量人类或机器人演示中快速学习新技能的能力。这一范式在推理效率上超越视频生成方法50–600倍，同时在小样本场景下将成功率从0–25%提升至67.5–80%。



TraceGen 的整体框架由两条核心流水线构成：**TraceForge** 负责将异构的跨具身视频转化为统一的 3D 轨迹训练信号，**TraceGen** 则作为基于流的条件生成模型，在 3D 轨迹空间中预测未来运动。两条流水线协同工作，共同实现从任意具身视频到机器人可执行轨迹的端到端映射。

### 数据生成流水线：TraceForge

TraceForge 的设计目标是消除不同具身、相机视角和环境背景带来的外观差异，将原始视频抽象为场景中心的 3D 轨迹序列。其处理流程分为四个阶段（参见 Figure 4）：

![[assets/figures/papers/paper_list_l49_https_arxiv_org_abs_2511_21690/figures/005_Figure_4.jpg]]
*Figure 4: Building the TraceForge dataset. From an input video Vin: (i) chunk task-relevant spans for curation and generate task instructions (Sec. 3.1); (ii) estimate camera pose and depth, select a reference image and track 3D points to form a raw trace (Sec. 3.2); (iii) apply world–to-camera alignment (Sec. 3.3); (iv) speed retargeting to produce the final 3D trace (Sec. 3.4)*

1. **事件分块与指令生成**：从输入视频中切分出任务相关的时间片段，并利用 VLM 为每个片段生成三种互补的任务指令：简短祈使句、多步分解描述和自然语言请求。
2. **3D 点追踪**：估计每帧的相机位姿和深度，选定参考帧后跟踪 3D 关键点，形成原始轨迹。
3. **相机-世界对齐**：将各帧的 3D 点统一投影到固定的参考相机坐标系下，消除相机运动带来的轨迹漂移。
4. **速度重定向**：对轨迹进行速度归一化，消除不同具身执行速度差异的影响，生成最终的 3D 轨迹。

通过这一流水线，TraceForge 从 123K 个视频中提取了 **1.8M 个观测-轨迹-语言三元组**，覆盖桌面操作、第一人称和野外场景，为跨具身预训练提供了大规模结构化监督信号。

### 世界模型：TraceGen

TraceGen 接收多模态观测（RGB 图像、深度图和语言指令），输出未来时刻的 3D 轨迹序列。其架构基于 **CogVideoX** 的 3D Transformer，并采用 **Prismatic-VLM** 的多编码器融合策略（参见 Figure 5）。

![[assets/figures/papers/paper_list_l49_https_arxiv_org_abs_2511_21690/figures/006_Figure_5.jpg]]
*Figure 5: Overview of TraceGen. Given language, RGB, and depth inputs, text is encoded by a frozen T5 encoder, RGB images are processed by DINOv3 and SigLIP, and depth maps are passed through a SigLIP encoder with a learnable stem adapter. The resulting visual features (RGB + depth) are concatenated and linearly projected to form unified visual tokens. Together with text tokens, these serve as conditioning inputs to a CogVideoX-based flow model, which predicts a velocity field that transforms Gaussian noise into trace patches via ODE integration*

**输入编码流程**如下：

- **文本编码**：由冻结的 T5 编码器处理语言指令。
- **视觉编码**：RGB 图像分别通过 DINOv3 和 SigLIP 提取特征，深度图通过带可学习 stem adapter 的 SigLIP 编码器处理。
- **特征融合**：三类视觉特征沿特征维度拼接后经线性层投影到统一维度 $D = 768$：

$$
\mathbf{F}_{\mathrm{vis}} = \mathrm{Concat}(\mathbf{F}_{\mathrm{dino}}, \mathbf{F}_{\mathrm{siglip}}, \mathbf{F}_{\mathrm{depth}}) \in \mathbb{R}^{N \times (D_d + D_s + D_s)}
$$

$$
\mathbf{F}_{\mathrm{vis}} = \mathrm{Linear}(\mathbf{F}_{\mathrm{vis}}) \in \mathbb{R}^{N \times D}
$$

融合后的视觉 token 与文本 token 共同作为条件输入，送入基于 **随机插值（Stochastic Interpolants）** 的流解码器。解码器预测速度场 $v_{\theta}$，通过 ODE 积分将高斯噪声逐步转化为轨迹 patch。训练目标为 Score Interpolation Loss：

$$
\mathscr{L}_{\mathrm{SI}} = \mathbb{E}_{\tau, \mathbf{X}^{0}, \mathbf{X}^{1}} \left[ \| v_{\theta}(\mathbf{X}^{\tau}, \tau, \mathbf{F}_{\mathrm{cond}}) - (\mathbf{X}^{1} - \mathbf{X}^{0}) \|^{2} \right]
$$

推理时采用 100 步 ODE 积分生成轨迹，所有编码器保持冻结，仅训练融合层和解码器。

### 执行闭环

生成的 3D 轨迹通过逆运动学映射为机器人关节命令，直接驱动 Franka Research 3 机械臂执行操作任务。这一设计使得 TraceGen 的预测输出无需额外的感知或规划模块即可落地到真实机器人。

### 训练与适应策略

TraceGen 采用**大规模跨具身预训练 + 少样本微调**的策略：

- **预训练阶段**：在 TraceForge-123K 的 1.8M 三元组上训练，学习通用的 3D 运动先验。
- **微调阶段**：仅需 5 个目标机器人演示视频或 5 个手持人类视频，即可快速适应新任务和新环境。

消融实验表明，预训练是成功的关键——仅用 5 个视频微调时，预训练模型达到 **80%** 成功率，而从零训练的模型仅 **25%**（Table 1）。跨具身混合数据（TraceForge-123K）的效果远优于单一数据源：仅用机器人数据（Agibot）为 45%，仅用人手数据（SSV2）为 25%（Table 2）。

### 效率优势

由于直接在紧凑的 3D 轨迹空间（$20 \times 20$ 网格，每个点含 $x, y, z$ 坐标）中预测，而非生成高维像素帧，TraceGen 的推理速度比基于视频生成的世界模型快 **50–600 倍**（Figure 7），同时保持了更高的任务成功率。



TraceGen 是一个基于流的条件生成模型，其核心任务是从多模态观测（RGB、深度、语言指令）预测未来 3D 运动轨迹。系统由两个关键模块构成：**多编码器特征提取** 和 **基于 CogVideoX 的流解码器**。

### 多编码器特征融合

模型采用 Prismatic-VLM 风格的多编码器融合策略，将异构视觉信息统一为紧凑的 token 表示。给定 RGB 图像和深度图，分别通过三个编码器提取特征：

- **DINOv3**：提取语义丰富的视觉特征 $\mathbf{F}_{\mathrm{dino}} \in \mathbb{R}^{N \times D_d}$
- **SigLIP**：提取视觉-语言对齐特征 $\mathbf{F}_{\mathrm{siglip}} \in \mathbb{R}^{N \times D_s}$
- **深度编码器**：使用带可学习 stem adapter 的 SigLIP 编码器处理深度图，得到 $\mathbf{F}_{\mathrm{depth}} \in \mathbb{R}^{N \times D_s}$

三者沿特征维度拼接后线性投影到统一维度 $D = 768$：

$$\mathbf{F}_{\mathrm{vis}} = \mathrm{Concat}(\mathbf{F}_{\mathrm{dino}}, \mathbf{F}_{\mathrm{siglip}}, \mathbf{F}_{\mathrm{depth}}) \in \mathbb{R}^{N \times (D_d + D_s + D_s)}$$

$$\mathbf{F}_{\mathrm{vis}} = \mathrm{Linear}(\mathbf{F}_{\mathrm{vis}}) \in \mathbb{R}^{N \times D}$$

文本指令由冻结的 T5 编码器处理，与投影后的视觉 token 共同构成条件输入 $\mathbf{F}_{\mathrm{cond}}$。所有编码器在训练期间保持冻结，仅训练融合层和解码器。

### 轨迹表示与速度场建模

TraceGen 将世界模型预测目标从像素空间转移到 3D 轨迹空间。轨迹表示为屏幕对齐的 3D 关键点序列：

$$\mathbf{T}_{\mathrm{ref}}^{t:t+L} = [x_i, y_i, z_i]_{i=t}^{t+L}$$

其中 $(x_i, y_i)$ 为参考相机视角下的像素坐标，$z_i$ 为对应深度值，$L$ 为预测时间跨度。相邻时间步的轨迹增量定义为速度：

$$\Delta \mathbf{T}_{\mathrm{ref}}^{t} = \mathbf{T}_{\mathrm{ref}}^{t+1} - \mathbf{T}_{\mathrm{ref}}^{t}$$

### 随机插值与 ODE 生成

模型采用随机插值（Stochastic Interpolants）框架进行轨迹生成。在训练时，在真实轨迹 $\mathbf{X}^1$ 和高斯噪声 $\varepsilon$ 之间构建插值路径：

$$\mathbf{I}_{\tau} = \alpha_{\tau} \mathbf{X}^{1} + \sigma_{\tau} \varepsilon, \quad \tau \in [0,1]$$

模型学习预测从噪声指向数据的向量场 $v_{\theta}$，训练目标为 Score Interpolation Loss：

$$\mathscr{L}_{\mathrm{SI}} = \mathbb{E}_{\tau, \mathbf{X}^{0}, \mathbf{X}^{1}} \left[ \| v_{\theta}(\mathbf{X}^{\tau}, \tau, \mathbf{F}_{\mathrm{cond}}) - (\mathbf{X}^{1} - \mathbf{X}^{0}) \|^2 \right]$$

推理时采用线性调度 ODE，速度场恒定，通过 100 步 ODE 积分从初始噪声 $\mathbf{X}^0$ 生成轨迹：

$$\mathbf{X}^{\tau} = (1 - \tau) \mathbf{X}^{0} + \tau \mathbf{X}^{1}, \quad \tau \in [0,1]$$

### 从轨迹到执行

生成的 3D 轨迹通过逆运动学（IK）映射为 Franka Research 3 机器人的关节命令，完成从预测到执行的闭环。



## 实验与关键发现

### 主实验结果

TraceGen 在四个真实世界机器人任务（衣物整理、球体放置、刷子操作、积木放置）上接受了系统评估，使用 Franka Research 3 机器人平台。核心发现如下：

**机器人域内少样本微调。** 在仅使用 5 个目标机器人演示视频进行热身微调后，TraceGen 在四个任务上达到 **80% 的整体成功率**（Figure 7）。相比之下，视频生成世界模型基线 **NovaFlow (Wan2.2)** 在零样本条件下成功率为 **0%**，而从头训练的 TraceGen 变体仅达到 **25%**（Table 1）。这一差距揭示了预训练 3D 运动先验的核心贡献：在 5 视频微调下，预训练模型相较从头训练提升了 **55 个百分点**。当微调视频数增加到 15 时，预训练模型提升至 **82.5%**，从头训练仅提升至 **30%**，呈现收益递减趋势，表明少量高质量演示已足以激活预训练先验。

**人类到机器人的跨具身迁移。** 使用 5 个未校准手持手机拍摄的人类演示视频（不同背景、不同物体位置），TraceGen 微调后达到 **67.5%** 的真实机器人成功率（Figure 8），而从头训练模型完全失败（**0%**）。这一结果表明，TraceForge 流水线成功将野外人类视频转化为与机器人执行兼容的 3D 轨迹表示，且预训练模型习得了可跨具身迁移的运动结构。

**推理效率优势。** TraceGen 的推理速度比轨迹预测基线快 **3.8 倍**，比大型视频生成模型（如 **NovaFlow (Veo3.1)**）快 **50 倍以上**（Figure 7）。视频生成世界模型的推理延迟（Veo 3.1 基于 API 平均响应时间测量）使其在实际机器人部署中不具竞争力，而 TraceGen 的轻量级 3D 轨迹解码器通过 100 步 ODE 积分即可生成可执行轨迹。

**长时域任务稳定性。** 在包含四个连续子任务的排序任务中（Table 4），预训练 TraceGen 各子任务成功率稳定在 **0.8 / 0.8 / 0.8 / 0.8**，而从头训练模型从 1.0 衰减至 0.4，表现出明显的误差累积。这说明跨具身预训练提供的运动先验有效抑制了长序列预测中的漂移问题。

### 消融分析

**预训练数据源的影响。** Table 2 对比了不同预训练数据源在 5 视频微调下的效果。使用跨具身混合数据（TraceForge-123K）预训练达到 **70%** 成功率，仅使用机器人数据（Agibot）降至 **45%**，仅使用人手数据（SSV2）降至 **25%**，与从头训练持平。这一结果表明，跨具身数据的多样性——而非单纯的规模——是习得可迁移运动先验的关键因素。

**3D 轨迹提取精度。** TraceForge 流水线的端到端轨迹提取误差在相机坐标系下为亚厘米级：X 轴 **1.66 cm**，Y 轴 **1.79 cm**，Z 轴 **2.26 cm**（Table 3）。这一精度为 TraceGen 的训练提供了可靠监督信号，Z 轴误差相对较大可能与单目深度估计的固有不确定性有关。

### 失败模式分析

针对四个任务的失败模式分解（Figure 9–12）揭示了 TraceGen 的主要失效原因：

![[assets/figures/papers/paper_list_l49_https_arxiv_org_abs_2511_21690/figures/014_Figure_9.jpg]]
*Figure 9: Failure-mode breakdown for the Clothes task*

- **抓取失败**：预测的 3D 轨迹末端位置与物体实际可抓取区域存在偏差，导致夹爪闭合时未能稳固抓取。这在衣物和刷子等非刚性或细长物体上尤为突出。
- **轨迹偏移**：预测轨迹在接近目标区域时出现厘米级偏移，导致放置或操作动作偏离预期位置。
- **深度估计误差**：单目深度估计在遮挡或纹理稀疏区域的误差传播至轨迹预测，影响 Z 轴方向的动作精度。

这些失败模式与 TraceGen 的局限性一致：精细操作任务可能缺乏足够的运动细节，且零样本生成在新环境下不够可靠，需依赖少样本微调来校准模型行为。

### 公平性说明

所有视频生成基线（NovaFlow 系列、AVDC）均使用统一的视频到轨迹提取流水线（VGGT + TAPIP3D），与 TraceForge 保持一致，确保比较的公平性。**3DFlowAction** 基线使用真实分割掩码代替其原目标检测器，因为原检测器在单张图像上经常失败，这一调整为基线提供了有利条件。NovaFlow (Veo3.1) 的推理延迟基于 API 平均响应时间，实际为基线有利的测量方式。

### 补充图表

![[assets/figures/papers/paper_list_l49_https_arxiv_org_abs_2511_21690/figures/008_Figure_7.jpg]]
*Figure 7: Success rate vs. inference efficiency (predictions per minute; higher and rightward is better). TraceGen achieves the best combination of success and efficiency, outperforming both video and trace-based baselines by a large margin. Gains stem from its strong 3D motion prior and a lightweight warm-up in trace space via TraceForge. In contrast, video-generation baselines (e.g., NovaFlow or video backbone in AVDC) offer no practical few-shot warm-up path in our setting, and several trace baselines rely on object detectors or heuristic object filtering, making warm-up technically difficult. (The Veo 3.1 latency is measured based on its average API call time.)*

![[assets/figures/papers/paper_list_l49_https_arxiv_org_abs_2511_21690/figures/009_Figure_8.jpg]]
*Figure 8: Human-to-robot skill transfer using human demo videos. TraceGen, finetuned on 5 in-the-wild handheld phone videos, successfully executes four manipulation tasks, with a success rate of 67.5%. In contrast, the From Scratch model fails (0%), indicating that cross-embodiment pretraining is essential*

![[assets/figures/papers/paper_list_l49_https_arxiv_org_abs_2511_21690/figures/010_Table_1.jpg]]
*Table 1: Effect of cross-embodiment pretraining under 5-video and 15-video warmup. Pretraining significantly improves success rates compared to training from scratch*

![[assets/figures/papers/paper_list_l49_https_arxiv_org_abs_2511_21690/figures/011_Table_2.jpg]]
*Table 2: Effect of pretraining source on 5-video warmup performance. Cross-embodiment pretraining with a larger dataset (TraceGen) yields substantially higher success than single-source pretraining and full scratch training*

![[assets/figures/papers/paper_list_l49_https_arxiv_org_abs_2511_21690/figures/012_Table_3.jpg]]
*Table 3: Absolute endpoint error along the x, y, z axes in camera coordinate between predicted and ground-truth trajectories*

![[assets/figures/papers/paper_list_l49_https_arxiv_org_abs_2511_21690/figures/025_Table_4.jpg]]
*Table 4: Long-horizon Sorting task: per-subtask success rates (left to right indicates temporal order)*

![[assets/figures/papers/paper_list_l49_https_arxiv_org_abs_2511_21690/figures/015_Figure_10.jpg]]
*Figure 10: Failure-mode breakdown for the Block task*

![[assets/figures/papers/paper_list_l49_https_arxiv_org_abs_2511_21690/figures/003_Figure_2.jpg]]
*Figure 2: TraceForge-123K dataset distribution. Our corpus contains 1.8M observation–trace–language triplets, spanning tabletop, egocentric, and in-the-wild footage with moving cameras to support generalization across embodiments and scenes*

![[assets/figures/papers/paper_list_l49_https_arxiv_org_abs_2511_21690/figures/004_Figure_3.jpg]]
*Figure 3: Failure cases of existing embodied world models. (a) Video-based models can hallucinate geometry or affordance. (b) VLM token outputs fail to capture fine motion. Bounding boxes miss the tool (c) or become overly broad (d)*



## 定位与知识库关联

### 与现有世界模型的范式对比

TraceGen 的核心差异在于将世界模型的预测目标从像素空间迁移到3D轨迹空间。这一转变使其与三类现有方法形成明确边界：

**视频生成世界模型**（如 **NovaFlow (Wan2.2)**、**NovaFlow (Veo3.1)**、**AVDC**）直接预测未来帧的RGB像素。这类方法面临两个根本性瓶颈：(1) 需要消耗大量计算资源建模与操纵无关的外观、背景和光照变化，导致推理速度比 TraceGen 慢50–600×；(2) 在跨具身场景下，像素空间的外观差异使得人类视频几乎无法直接复用。实验表明，NovaFlow (Wan2.2) 在零样本条件下成功率为0%，且缺乏实用的少样本微调路径——因为视频生成模型的小样本微调通常需要大量同域数据才能避免灾难性遗忘。

**2D/3D轨迹预测方法**（如 **3DFlowAction**）虽然也输出轨迹，但依赖目标检测器或启发式物体过滤来提取关键点，这在单张图像上经常失败（原文为公平比较使用了真实分割掩码替代原检测器）。TraceGen 直接输出场景级3D轨迹，无需边界框或检测器，避免了检测失败导致的级联误差。

**VLM token输出方法**（如将动作编码为离散token）在精细运动捕捉上存在天然不足——离散token化会丢失连续运动的细微变化，这在需要精确力控或微小位移的操作中尤为致命。

### 数据生成范式的革新：TraceForge

TraceForge 流水线解决了跨具身视频到统一训练信号的转化问题，其关键模块包括：

- **相机运动补偿**：从移动相机视频中恢复每个视点的逐帧3D点轨迹，使野外手持拍摄的视频也能产生有效的训练监督。
- **速度重定向**：将不同具身（人手、不同机器人）的运动速度归一化到统一尺度，消除具身依赖的运动差异。
- **端到端精度**：3D轨迹提取的绝对端点误差为亚厘米级（X: 1.66cm, Y: 1.79cm, Z: 2.26cm），为模型训练提供了可靠监督。

这一定位使 TraceForge 区别于依赖静态相机和实验室环境的传统数据采集方式。其产出的 TraceForge-123K 数据集包含1.8M观测-轨迹-语言三元组，规模超过先前工作15×以上，涵盖桌面、第一人称和野外场景。

### 架构设计的知识库定位

TraceGen 的架构设计体现了对现有成熟组件的系统性融合：

- **生成骨干**：基于 **CogVideoX** 的3D Transformer架构，但将输出空间从视频帧改为轨迹patch，通过随机插值（Stochastic Interpolants）和ODE积分生成3D轨迹。
- **多编码器融合**：借鉴 **Prismatic-VLM** 的融合策略，将DINOv3、SigLIP（RGB）、SigLIP（深度，带可学习stem adapter）和T5（文本）的特征拼接并线性投影到统一维度（D=768）。
- **编码器冻结策略**：所有编码器在训练期间保持冻结，仅训练融合层和解码器，这继承了Prismatic-VLM的高效微调范式。

这种“成熟骨干+输出空间重定向”的设计思路，使得TraceGen能够充分利用预训练视觉和语言表征，同时避免在像素空间进行昂贵的生成。

### 适用边界与局限

TraceGen 的适用边界由其核心抽象——3D轨迹空间——决定：

1. **具身形态限制**：轨迹空间的抽象主要针对类人操作任务（单臂/双臂、人手），其假设被操纵物体和末端执行器的运动具有共享的以场景为中心的3D结构。扩展到轮式、蛇形、四足等迥异机器人时，这一假设可能不再成立。

2. **操作精度限制**：当前轨迹输出为20×20网格密度，对于需要精确力控或亚厘米级精细运动的任务，可能缺乏足够的运动细节。虽然3D轨迹提取精度已达亚厘米级，但模型生成的分辨率仍是瓶颈。

3. **零样本可靠性不足**：模型在新具身或未见环境下需要少样本微调才能达到高成功率，零样本生成不够可靠。5视频微调达到80%，但15视频微调仅提升至82.5%，呈现收益递减趋势，表明当前微调策略的利用效率仍有提升空间。

4. **运动多模态性未充分建模**：当前仅采用线性插值ODE（$\mathbf{X}^{\tau} = (1 - \tau) \mathbf{X}^{0} + \tau \mathbf{X}^{1}$），未探索其他随机插值调度来处理模糊任务中的多模态运动分布。

5. **数据质量依赖**：TraceForge管道虽然准确，但仍可能因视频噪点、遮挡等带来误差；尽管进行了过滤，部分噪声演示仍然存在，规模化和改进过滤仍是工程挑战。

### 开放问题

1. **闭环规划集成**：如何将TraceGen与基于模型的控制或强化学习结合，实现基于预测轨迹的闭环规划，而非当前的开放环执行？

2. **跨具身迁移的上限**：能否通过更大的预训练数据集和更丰富的机器人类型（如双臂、移动操作）进一步提升迁移能力？预训练数据源消融显示，跨具身混合数据（TraceForge-123K）达到70%，而单一机器人数据（Agibot）仅45%，人手数据（SSV2）仅25%，表明数据多样性的边际收益尚未饱和。

3. **轨迹分辨率与效率的权衡**：如何在保持推理效率（当前3.8×快于轨迹基线，>50×快于视频模型）的同时提高3D轨迹的分辨率？

4. **人→机器人微调稳定性**：如何设计更好的微调策略，使模型在仅有人类演示时更稳定地适应不同场景？当前人→机器人迁移成功率为67.5%，而机器人微调为80%，两者之间仍有显著差距。

5. **与低层控制器的集成**：能否将TraceGen的轨迹预测作为高级规划目标，与阻抗控制器或导纳控制器等低层控制器集成，以处理需要力控的接触丰富任务？



## 原文 PDF

![[paperPDFs/CVPR_2026/TraceGen_World_Modeling_in_3D_Trace_Space_Enables_Learning_from_Cross_Embodiment_Videos.pdf]]
