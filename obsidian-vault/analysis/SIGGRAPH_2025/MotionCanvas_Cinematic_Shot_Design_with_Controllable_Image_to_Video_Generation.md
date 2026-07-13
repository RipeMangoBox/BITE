---
title: "MotionCanvas: Cinematic Shot Design with Controllable Image-to-Video Generation"
type: paper
paper_level: A
venue: SIGGRAPH
year: 2025
pdf_ref: paperPDFs/SIGGRAPH_2025/MotionCanvas_Cinematic_Shot_Design_with_Controllable_Image_to_Video_Generation.pdf
project_link: https://motion-canvas25.github.io/
code_link: null
aliases:
- MotionCanvas
tags:
- SIGGRAPH_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "Motion Signal Translation模块，该模块利用深度估计和相机针孔模型，将用户定义的3D场景空间运动（包括相机路径、物体全局边界框和局部点轨迹）通过层次变换转换为2D屏幕空间运动信号，作为视频扩散模型的条件输入，从而在不依赖3D标注的情况下实现3D感知的运动控制。"
primary_logic: "核心洞察在于通过2D点追踪和边界框轨迹等可自动估计的屏幕空间运动表征，结合推理时的场景空间到屏幕空间转换，能够使视频生成模型在训练中规避对3D标注的依赖，同时为用户提供直观的3D感知运动设计接口。"
claims:
- "Motion Signal Translation模块将场景空间运动意图转换为屏幕空间信号，实现3D感知控制。"
- "在RealEstate10K上零样本相机运动控制性能超越MotionCtrl和CameraCtrl。"
- "在VIPSeg上物体运动控制准确度（ObjMC）和帧质量（FID）均大幅领先DragAnything等基线。"
- "用户研究显示MotionCanvas在运动遵循度、运动质量和帧保真度上获得~75-79%的偏好率。"
---

# MotionCanvas: Cinematic Shot Design with Controllable Image-to-Video Generation

> [!tip] 核心洞察
> 核心洞察在于通过2D点追踪和边界框轨迹等可自动估计的屏幕空间运动表征，结合推理时的场景空间到屏幕空间转换，能够使视频生成模型在训练中规避对3D标注的依赖，同时为用户提供直观的3D感知运动设计接口。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | MotionCanvas：可控图像到视频生成的电影镜头设计 |
| 英文题名 | MotionCanvas: Cinematic Shot Design with Controllable Image-to-Video Generation |
| 会议/期刊 | SIGGRAPH 2025 |
| Links | [paper](https://arxiv.org/abs/2502.04299) · [Project](https://motion-canvas25.github.io/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | MotionCanvas |
| Dataset | RealEstate10K (相机控制), RealEstate10K, VIPSeg (物体控制) |

> [!tip] 效果简介
> - RealEstate10K (相机控制) 上，RotErr 为 0.6334 (Ours*)，对比 0.8460 (MotionCtrl)，变化 -0.2126。
> - RealEstate10K 上，TransErr 为 0.2188 (Ours*)，对比 0.2567 (MotionCtrl)，变化 -0.0379。
> - RealEstate10K 上，FVD 为 34.09 (Ours*)，对比 48.03 (MotionCtrl)，变化 -13.94。

## 概要

**问题瓶颈**：现有图像到视频生成方法难以同时精确控制相机运动和物体运动。其根本障碍在于，用户的运动意图通常在3D场景空间中定义（例如“镜头绕物体旋转”），而视频生成模型基于2D屏幕空间信号训练，两者之间缺乏有效的转换机制。此外，获取大规模带有3D标注（如相机姿态、深度图）的训练视频数据成本高昂，进一步限制了3D感知运动控制的发展。

**核心洞察**：MotionCanvas的核心思路是**规避对3D标注的依赖**。通过使用2D点追踪和边界框轨迹这类可自动、可靠估计的屏幕空间运动表征，结合推理时的“场景空间→屏幕空间”层次变换，系统既能让用户在直观的3D场景空间中设计运动，又能使视频生成模型在训练中仅依赖自动提取的2D信号。

**方法定位**：MotionCanvas提出**Motion Signal Translation模块**作为连接用户3D意图与模型2D条件的因果旋钮。该模块利用深度估计和相机针孔模型，将用户定义的3D相机路径、场景锚定物体边界框和局部点轨迹，通过层次变换转换为2D屏幕空间运动信号，再经由专门设计的运动条件化机制注入DiT架构的视频扩散模型。这一设计使得方法在训练中无需3D标签，仅使用约1.1M自然视频即可学习。

**关键结果**：
- **相机运动控制**：在RealEstate10K数据集上零样本测试，旋转误差（RotErr）0.6334，平移误差（TransErr）0.2188，显著优于MotionCtrl（Wang et al., ACM SIGGRAPH 2024）和CameraCtrl。
- **物体运动控制**：在VIPSeg数据集上，物体运动准确度（ObjMC）25.72，FID 42.47，大幅领先DragAnything（Wu et al., ECCV 2024）等基线。
- **用户研究**：在运动遵循度（75.24%）、运动质量（79.05%）和帧保真度（77.14%）三个维度上均获得压倒性偏好率。

### 问题背景：从静态图像到电影级镜头的生成鸿沟

将单张静态图像转化为一段具有电影感的动态视频，是视觉内容创作领域的核心需求之一。这一任务要求生成模型同时具备两种能力：一是对**相机运动**的精确控制，如推拉摇移、变焦等镜头语言；二是对画面中**物体运动**的灵活编排，如人物的移动、物体的轨迹变化。两者协同作用，才能构成完整的电影镜头设计（cinematic shot design）。

然而，现有图像到视频（image-to-video, I2V）生成方法在这两个维度上的控制能力存在显著割裂。部分工作专注于相机运动控制，另一些则聚焦于物体运动操控，鲜有方法能在一个统一框架内同时精确驾驭二者。这种割裂的根源在于一个根本性的空间表征矛盾。

### 核心瓶颈：场景空间意图与屏幕空间信号之间的转换缺失

用户对运动的构思天然发生在**3D场景空间**中——例如，“镜头从左侧环绕拍摄，同时画面中的汽车从左向右行驶”——这类意图包含了对深度、视角和物体空间关系的隐含理解。但主流的视频扩散模型（video diffusion models）是在**2D屏幕空间**的像素信号上进行训练的，其条件输入（如控制点坐标、光流图）本质上是二维的。

这一矛盾构成了领域的关键瓶颈：**缺乏从场景空间到屏幕空间的有效转换机制**。用户难以将脑海中的3D运动意图直接翻译为模型可理解的2D控制信号。更棘手的是，获取大规模带有3D标注（如逐帧相机姿态、物体三维轨迹）的视频训练数据成本极高，这使得直接训练3D感知的视频生成模型在数据层面就面临难以逾越的障碍。

### 现有方法的局限

围绕上述瓶颈，现有方法大致可分为两类，各自存在明显短板：

**相机运动控制方法**，如 **MotionCtrl**（Wang et al., ACM SIGGRAPH 2024）和 **CameraCtrl**，通常依赖Plücker坐标或高斯图等显式3D表示作为条件输入。这类方法需要在RealEstate10K等包含3D相机姿态标注的特定数据集上进行训练，数据多样性受限，难以泛化到自然场景。更重要的是，它们仅处理相机运动，无法同时控制画面内的物体运动。

**物体运动控制方法**，如 **DragAnything**（Wu et al., ECCV 2024）、**MOFA-Video** 和 **TrackDiffusion**，允许用户通过拖拽点或定义屏幕坐标来操控物体。但这些操作完全在2D屏幕空间中进行，缺乏对场景深度和相机运动的感知。当用户试图同时施加相机运动和物体运动时，两类控制信号在屏幕空间中的交互变得复杂且难以解耦，导致运动不自然或控制失效。

### 本文动机：以2D信号承载3D意图

上述分析揭示了一个清晰的研究方向：能否在不依赖昂贵3D标注的前提下，让视频生成模型理解并执行用户在3D场景空间中定义的运动意图？

MotionCanvas的核心动机正是回答这一问题。其关键洞察在于：**2D点轨迹（point trajectories）和边界框序列（bounding box sequences）** 是两种可以通过现成工具（如RAFT光流、DEVA分割）从普通视频中自动、可靠提取的屏幕空间运动表征。如果能在推理阶段建立一套从场景空间到屏幕空间的转换机制，将这些2D表征与用户的3D运动意图桥接起来，就能在训练中完全规避对3D标注的依赖，同时为用户提供直观的3D感知运动设计接口。

这一思路直接催生了MotionCanvas的三大设计支柱：**运动设计模块**（捕捉场景空间意图）、**运动信号转换模块**（将场景空间意图翻译为屏幕空间信号）和**运动条件视频生成模型**（以2D信号为条件生成视频）。后续章节将逐一展开这些组件的技术细节。

## 核心方法与创新机理

MotionCanvas 的核心创新在于构建了一条从**3D场景空间运动意图**到**2D屏幕空间运动信号**的可微分转换通路，使视频扩散模型在不依赖3D标注的条件下获得3D感知的运动控制能力。这一通路围绕三个紧密耦合的 changed slots 展开。

### 1. 运动控制表示空间的升维：从屏幕空间到场景空间

现有方法（如 DragAnything、MotionCtrl）要求用户直接在2D屏幕空间操作拖拽点或定义屏幕坐标，缺乏深度感知和相机运动上下文，导致运动控制与场景几何割裂。MotionCanvas 将控制表示空间从2D屏幕空间提升至3D场景空间：用户定义的是场景锚定的物体边界框轨迹、物体局部点轨迹，以及由外参/内参序列 $(E_{l}, K_{l})_{l=1}^{L}$ 描述的3D相机路径。这一改变使得运动意图的表达与场景几何内禀绑定，为后续的层次化运动分解奠定了基础。

### 2. Motion Signal Translation：场景空间到屏幕空间的层次变换

这是系统的核心因果旋钮。Motion Signal Translation 模块通过深度估计和相机针孔模型，将用户定义的场景空间运动意图转换为视频生成模型可消费的屏幕空间信号。具体而言：

- **相机运动**：通过深度合成将3D相机路径转化为2D点轨迹，使相机运动以点追踪的形式表达，无需3D相机姿态标签。
- **物体全局运动**：场景锚定的边界框 $b_{\text{scene}}^{l}$ 经相机运动变换 $\mathcal{T}_{\text{camera}}^{l}$ 投影至屏幕空间：$b_{\text{screen}}^{l} = \mathcal{T}_{\text{camera}}^{l}(b_{\text{scene}}^{l})$。
- **物体局部运动**：场景空间控制点 $p_{\text{scene}}^{l}$ 先经物体全局运动变换 $\mathcal{T}_{\text{global}}^{l}$，再经相机运动变换投射至屏幕空间：$p_{\text{screen}}^{l} = \mathcal{T}_{\text{camera}}^{l}(\mathcal{T}_{\text{global}}^{l}(p_{\text{scene}}^{l}))$，实现局部运动与全局运动的解耦。

消融实验（Figure 13）证实，移除相机感知变换或相机-物体感知变换会导致物体运动不自然或错误，验证了层次变换的必要性。

### 3. 无需3D标注的运动条件化机制

传统方法（如 CameraCtrl 使用 Plücker 坐标）依赖带有3D相机姿态标注的专门领域数据集（如 RealEstate10K）进行训练，数据多样性和规模受限。MotionCanvas 采用两种可从自然视频中自动提取的屏幕空间运动表征作为条件：

- **相机运动条件**：将2D点轨迹编码为离散余弦变换（DCT）系数（$K=10$），作为紧凑的条件令牌输入 DiT 模型。消融实验（Table 4）表明，该方案在 RotErr（0.6334）、TransErr（0.2188）和 FVD（34.09）上显著优于 Gaussian map 和 Plücker 坐标，同时仅增加约1.1%的令牌开销。
- **物体运动条件**：将边界框轨迹光栅化为彩色蒙版序列，利用预训练的3D-VAE编码为时空嵌入，与噪声视频潜变量求和后送入 DiT。相比直接拼接坐标序列（Ours_coord），该方案在 ObjMC 和 FID 上均有显著提升（Table 2）。

这种设计使训练数据从约1.1M自然视频中通过 DEVA 分割和 RAFT 光流自动提取约600K高质量2D点追踪和边界框注释，彻底规避了对3D标注的依赖，同时支持丰富多样的场景。

### 创新总结

| 维度 | 基线方法 | MotionCanvas |
|------|----------|-------------|
| 控制表示空间 | 2D屏幕空间（拖拽点、屏幕坐标） | 3D场景空间（相机路径、场景锚定边界框、局部点轨迹） |
| 相机运动条件 | Plücker坐标/高斯图（需3D标签） | 2D点轨迹的DCT系数（自动提取，无3D标签） |
| 物体运动条件 | 坐标拼接或显式扭曲 | 3D-VAE编码的时空蒙版嵌入 |
| 训练数据 | 专门领域数据集（RealEstate10K） | 约600K自然视频（自动标注） |

这三个 changed slots 形成了正向反馈闭环：场景空间表示使运动意图与场景几何对齐，层次变换将其无损转换为屏幕空间信号，而屏幕空间信号的自动可提取性又使大规模无标注训练成为可能，最终实现了零样本设置下对 MotionCtrl 和 CameraCtrl 的显著超越（Table 1）。

![[assets/figures/papers/paper_list_l22_MotionCanvas_Cinematic_Shot_Design_with_Controllable_Image_to_Video_Gene/figures/006_Figure_6.jpg]]
*Figure 6: Generated videos with diverse and fine-grained local motion controls (upper), and in coordination with camera motion control (bottom). Figure 7. Results when our method is applied for: (upper) motion transfer, and (bottom) video editing for changing objects, adding and removing objects*

![[assets/figures/papers/paper_list_l22_MotionCanvas_Cinematic_Shot_Design_with_Controllable_Image_to_Video_Gene/figures/002_Figure_2.jpg]]
*Figure 2: Overview of MotionCanvas. Given an input image and high-level scene-space motion intent, MotionCanvas decomposes and translates the motion (camera and object motion with their timing) into screen space by leveraging the depth-based synthesis and hierarchical transformation with the Motion Signal Translation module. These screen-space motion signals are subsequently passed to a video generation model to produce the final cinematic shots*

MotionCanvas 的整体 pipeline 围绕一个核心矛盾展开：用户对运动的意图天然定义在 3D 场景空间（相机路径、物体的空间位置与局部形变），而视频生成模型只能接收 2D 屏幕空间的运动信号。因此，系统的设计瓶颈在于**如何在不依赖 3D 标注的条件下，将场景空间的运动意图可靠地转换为屏幕空间的条件信号**。

整个框架由三个主模块串联构成，形成“意图捕获 → 空间转换 → 条件化生成”的因果链路：

1.  **运动设计模块（Motion Design Module）**：捕捉用户在 3D 场景空间中的运动意图，包括相机运动、物体全局运动与物体局部运动，并支持关键帧插值与时间控制。相机运动定义为外参/内参序列 $(E_{l}, K_{l})_{l=1}^{L}$；物体全局运动通过场景锚定的边界框轨迹定义；物体局部运动则通过物体自身坐标系内的点轨迹定义。

2.  **运动信号转换模块（Motion Signal Translation Module）**：这是系统的**因果调节旋钮**。它利用单目深度估计和相机针孔模型，执行层次化变换，将场景空间运动意图投影为 2D 屏幕空间信号：
    -   **相机运动**：通过将 3D 空间中的采样点经相机变换投影到屏幕，生成 2D 点轨迹。
    -   **物体全局运动**：场景空间边界框经相机变换投影为屏幕空间边界框轨迹：$b_{\mathrm{screen}}^{l} = \mathcal{T}_{\mathrm{camera}}^{l}(b_{\mathrm{scene}}^{l})$。
    -   **物体局部运动**：场景空间控制点先经物体全局运动变换，再经相机运动变换，解耦后投影到屏幕空间：$p_{\mathrm{screen}}^{l} = \mathcal{T}_{\mathrm{camera}}^{l}(\mathcal{T}_{\mathrm{global}}^{l}(p_{\mathrm{scene}}^{l}))$。

    该模块使系统在训练和推理中完全规避了对 3D 标注的依赖，因为其输出的屏幕空间信号（点轨迹、边界框轨迹）均可从视频中自动估计。

3.  **运动条件化视频生成模型（Motion-conditioned Video Generation Model）**：基于 DiT 架构的图像到视频扩散模型，接收转换后的屏幕空间信号作为条件：
    -   **点轨迹**：被编码为离散余弦变换（DCT）系数的紧凑表示，作为条件令牌输入。
    -   **边界框轨迹**：被光栅化为彩色蒙版序列，经预训练的 3D-VAE 编码为时空嵌入，与噪声视频潜变量**求和**后送入 DiT。
    
    模型通过流匹配损失进行训练：
    $$\min_{\theta} \mathbb{E}_{t, X^{0}, X^{1}} \left[ \| V^{t} - v_{\theta}(X^{t}, t \vert C_{\mathrm{img}}, C_{\mathrm{traj}}, C_{\mathrm{bbox}}, C_{\mathrm{txt}}) \|_{2}^{2} \right]$$
    其中 $V^t$ 为速度向量，条件包括输入图像 $C_{\mathrm{img}}$、点轨迹 $C_{\mathrm{traj}}$、边界框 $C_{\mathrm{bbox}}$ 和文本 $C_{\mathrm{txt}}$。

此外，MotionCanvasAR 自回归扩展模块通过重新计算输入运动信号，使前一 16 帧视频片段作为条件，支持生成变长视频，解决了片段间运动不连续问题。

整个 pipeline 的输入输出流为：**静态图像 + 场景空间运动意图 → 屏幕空间点轨迹与边界框轨迹 → 条件化视频扩散模型 → 电影级运动视频**。

MotionCanvas 的系统架构由三个核心模块串联构成：**运动设计模块**捕获用户的场景空间运动意图，**运动信号转换模块**将其解耦并投影为屏幕空间信号，**运动条件视频生成模型**则基于这些2D信号生成最终视频。

### 运动信号转换模块

这是整个系统的核心创新所在，解决了“用户在3D场景空间定义运动，而视频生成模型在2D屏幕空间操作”这一根本性矛盾。模块通过层次化变换，将三种运动意图分别转换为屏幕空间信号：

**相机运动 → 2D点轨迹。** 用户定义一条3D相机路径，由每帧的外参 $E_l$ 和内参 $K_l$ 序列给出：

$$(E_{l}, K_{l})_{l=1}^{L}$$

系统利用深度估计和相机针孔模型，将该路径转换为屏幕空间中的2D点轨迹。这些轨迹随后被编码为离散余弦变换（DCT）系数（取前 $K=10$ 个系数），作为紧凑的条件信号送入生成模型。

**物体全局运动 → 边界框轨迹。** 用户在输入图像上放置场景锚定的边界框，指定起始、结束及可选的中间关键框。系统通过相机运动变换 $\mathcal{T}_{\mathrm{camera}}^{l}$，将场景空间边界框投影到屏幕空间：

$$b_{\mathrm{screen}}^{l} = \mathcal{T}_{\mathrm{camera}}^{l}(b_{\mathrm{scene}}^{l})$$

得到的边界框序列被光栅化为独特的彩色蒙版，再经预训练的3D-VAE编码为时空嵌入，与噪声视频潜变量求和后输入DiT模型。

**物体局部运动 → 点轨迹分解。** 用户在物体自身坐标系内定义拖拽式点轨迹。这些场景空间控制点 $p_{\mathrm{scene}}^{l}$ 首先经过物体全局运动变换 $\mathcal{T}_{\mathrm{global}}^{l}$，再经过相机运动变换 $\mathcal{T}_{\mathrm{camera}}^{l}$，最终投影到屏幕空间：

$$p_{\mathrm{screen}}^{l} = \mathcal{T}_{\mathrm{camera}}^{l}(\mathcal{T}_{\mathrm{global}}^{l}(p_{\mathrm{scene}}^{l}))$$

该层次变换解耦了物体局部运动与全局场景运动，使得物体可以在自身运动的同时，正确响应相机和场景级变化。

### 运动条件视频生成模型

模型基于DiT架构的图像到视频扩散模型，接收三类条件输入：输入图像 $C_{\mathrm{img}}$、点轨迹的DCT系数 $C_{\mathrm{traj}}$、边界框序列的时空嵌入 $C_{\mathrm{bbox}}$，以及文本提示 $C_{\mathrm{txt}}$。训练目标为流匹配损失，即预测速度向量 $V^t$ 与真实速度之间的均方误差：

$$\min_{\theta} \mathbb{E}_{t, X^{0}, X^{1}} \left[ \| V^{t} - v_{\theta}(X^{t}, t \vert C_{\mathrm{img}}, C_{\mathrm{traj}}, C_{\mathrm{bbox}}, C_{\mathrm{txt}}) \|_{2}^{2} \right]$$

其中 $X^0$ 和 $X^1$ 分别为噪声和真实视频潜变量，$X^t$ 为时间 $t$ 的插值状态。该设计的关键优势在于：训练时所需的点轨迹和边界框均可从自然视频中自动提取（通过DEVA分割和RAFT光流），**完全规避了对3D标注数据的依赖**，使得模型能够在大规模多样化视频上训练。

### 消融验证的关键结论

对相机运动表示方式的消融实验（Table 4）表明，DCT系数编码（Traj. coeff）在RotErr（0.6334）、TransErr（0.2188）和FVD（34.09）上均显著优于Gaussian map和Plücker坐标表示，同时仅增加1.1%的令牌开销和32秒的生成延迟。对Motion Signal Translation模块的消融（Figure 13）则验证了层次变换的必要性：移除相机感知变换或相机-物体感知变换会导致物体运动不自然或错误。

## 实验与关键发现

### 核心实验设置

MotionCanvas的训练数据来自约110万高质量自然视频，通过DEVA分割与RAFT光流自动提取约60万条带有2D点追踪和边界框注释的视频片段，完全规避了对3D姿态标注的依赖。视频生成模块从预训练的图像到视频DiT模型微调10万步，所有生成结果统一以8 FPS输出14帧（约2秒视频），确保公平比较。对比方法均使用官方代码及相同输入条件生成，标准化编码以消除实现差异。

### 相机运动控制：RealEstate10K零样本评估

Table 1展示了在RealEstate10K测试集（1K样本）上的零样本相机运动控制对比。MotionCanvas（Ours*）在旋转误差RotErr上达到0.6334，较MotionCtrl（Wang et al., ACM SIGGRAPH 2024）的0.8460降低25.1%；平移误差TransErr为0.2188，低于MotionCtrl的0.2567。相机运动一致性CamMC达到0.9453，视频质量指标FVD和FID分别为34.09和7.60，均显著优于所有基线方法。

![[assets/figures/papers/paper_list_l22_MotionCanvas_Cinematic_Shot_Design_with_Controllable_Image_to_Video_Gene/figures/009_Table_1.jpg]]
*Table 1: Quantitative comparison with state-of-the-art methods on the RealEstate10K test set (1K). ∗ denotes zero-shot performance*

这一优势的因果机制在于：Motion Signal Translation模块利用深度估计和针孔相机模型，将用户定义的3D相机路径转换为2D点轨迹，再通过离散余弦变换（DCT，K=10）编码为紧凑条件令牌。Table 4的消融实验证实，该轨迹系数编码（Traj. coeff）在RotErr、TransErr和FVD上均显著优于Gaussian map和Plücker坐标表示，同时仅增加1.1%的令牌开销和约32秒的生成延迟。值得注意的是，Figure 8的定性对比显示，MotionCanvas在处理复杂镜头类型（如Dolly-Zoom变焦推拉）时，对相机运动意图的遵循度明显优于基线方法，后者常出现运动漂移或场景扭曲。

![[assets/figures/papers/paper_list_l22_MotionCanvas_Cinematic_Shot_Design_with_Controllable_Image_to_Video_Gene/figures/011_Table_4.jpg]]
*Table 4: Ablation study of applying different camera motion representations on our base model. : Zero-shot performance*

### 物体运动控制：VIPSeg评估

Table 2汇报了在VIPSeg数据集上的物体运动控制性能。MotionCanvas（Ours_map）在物体运动控制准确度ObjMC上达到25.72，相比DragAnything（Wu et al., ECCV 2024）的32.37降低20.5%（ObjMC越低越好）；帧质量FID为42.47，较DragAnything的64.32大幅降低34.0%。在用户研究（Table 3）中，MotionCanvas在运动遵循度、运动质量和帧保真度上分别获得75.24%、79.05%和77.14%的偏好率，远超DragAnything的14.29%、10.10%和MOFA-Video的12.95%。

![[assets/figures/papers/paper_list_l22_MotionCanvas_Cinematic_Shot_Design_with_Controllable_Image_to_Video_Gene/figures/010_Table_2.jpg]]
*Table 2: Quantitative comparison for object motion control on VIPSeg*

![[assets/figures/papers/paper_list_l22_MotionCanvas_Cinematic_Shot_Design_with_Controllable_Image_to_Video_Gene/figures/012_Table_3.jpg]]
*Table 3: User study statistics of the preference rate for motion adherence, motion quality, and frame fidelity*

物体运动控制的核心设计在于边界框轨迹的时空嵌入编码：将边界框序列光栅化为独特彩色蒙版，利用预训练3D-VAE编码为时空嵌入，与噪声视频潜变量求和后送入DiT。Table 2的消融对比Ours_coord（直接将边界框坐标拼接到视觉令牌）表明，时空嵌入方案在ObjMC和FID上均有显著优势，验证了该条件化策略对运动精度和生成质量的双重增益。

### 消融实验：运动表示与变换机制

**相机运动表示消融**（Table 4）：对比三种相机运动条件化方案——Gaussian map、Plücker坐标和轨迹DCT系数（Traj. coeff）。轨迹系数方案在全部指标上最优，且令牌开销极低（+1.1%），证明了2D点追踪DCT编码作为相机运动条件的有效性和高效性。补充实验进一步揭示，高密度点轨迹能更好地遵循轨道相机运动，而低密度轨迹会导致运动模糊和不准确。

**层次变换的必要性**（Figure 13及补充材料）：移除相机感知变换（camera-aware transformation）或相机-物体感知变换（camera-object-aware transformation）后，物体运动出现不自然漂移或与相机运动不一致的错误。这验证了Motion Signal Translation模块中层次变换设计的关键作用——先应用物体全局运动变换，再经相机运动变换投影到屏幕空间，才能正确解耦物体局部运动与相机运动。

**文本提示的影响**（补充材料F.2）：文本提示对相机运动控制无显著影响，但可以引入多样化动态效果（如下雨、人物转身），表明运动条件与文本条件在模型中相对独立地发挥作用。

### 失败模式与局限性

尽管MotionCanvas在定量和定性评估中表现优异，仍存在以下局限：

1. **推理速度瓶颈**：生成约2秒视频需要约35秒，限制了实时交互应用。这源于DiT架构的迭代去噪过程，是当前扩散模型共有的效率问题。
2. **深度近似假设**：物体局部运动被近似为正面平行深度平面，在处理极端特写或微距镜头时可能出现投影不准确。该假设在常规场景下足够鲁棒，但在深度变化剧烈的场景中需要更显式的3D建模。
3. **运动-文本信号冲突**：系统目前未显式协调用户运动设计与文本提示，当两者不一致时可能导致生成结果偏离预期。例如，用户定义物体向左移动而文本描述向右移动时，模型缺乏明确的冲突解决机制。

### 关键图表结论汇总

- **Table 1**：零样本相机运动控制在RealEstate10K上全面超越MotionCtrl和CameraCtrl，验证了2D点轨迹DCT编码作为相机运动条件的有效性。
- **Table 2**：物体运动控制在VIPSeg上显著优于DragAnything等基线，时空嵌入编码策略在控制精度和帧质量上双重领先。
- **Table 3**：用户研究确认MotionCanvas在运动遵循度、运动质量和帧保真度三个维度均获得压倒性偏好（75-79%）。
- **Table 4**：轨迹DCT系数编码在性能-效率权衡上最优，仅1.1%令牌开销即可实现鲁棒的相机内外参控制。
- **Figure 8/9/10**：定性对比显示MotionCanvas在复杂相机运动、物体运动及联合控制场景下均表现出更准确的运动遵循和更高的视觉质量。

### 补充图表


## 定位与知识库关联

### 核心瓶颈与设计动机

现有图像到视频生成方法在运动控制上面临一个根本性瓶颈：用户意图通常在3D场景空间中定义（如“摄像机从左向右平移，同时物体向前移动”），而视频生成模型基于2D屏幕空间信号训练，缺乏从场景空间到屏幕空间的有效转换机制。更关键的是，获取大规模带有3D标注（如相机姿态、深度图）的视频训练数据成本高昂，使得直接训练3D感知的运动控制模型不切实际。

MotionCanvas的核心洞察在于：通过2D点追踪和边界框轨迹等可自动估计的屏幕空间运动表征，结合推理时的场景空间到屏幕空间转换，能够使视频生成模型在训练中规避对3D标注的依赖，同时为用户提供直观的3D感知运动设计接口。这一设计将“3D控制需求”与“2D训练约束”之间的矛盾转化为一个可解的翻译问题。

### 控制表示空间的范式转换

与现有方法的根本差异体现在运动控制的**表示空间**上：

- **基线范式**：用户直接操作2D屏幕空间运动信号。例如，**DragAnything**（Wu et al., ECCV 2024）通过拖拽屏幕上的点来定义物体运动，**MotionCtrl**（Wang et al., ACM SIGGRAPH 2024）和**CameraCtrl**使用Plücker坐标或高斯图等显式3D表示进行相机运动条件化，但这些方法仍要求训练数据带有3D相机姿态标签（如RealEstate10K），限制了训练数据的多样性和规模。

- **MotionCanvas范式**：用户定义3D场景空间运动意图——包括相机路径（外参/内参序列）、场景锚定的物体全局边界框轨迹、以及物体局部点轨迹——由Motion Signal Translation模块在推理时将其转换为2D屏幕空间信号。该转换利用深度估计和相机针孔模型，通过层次变换完成：
  - 相机运动变换将场景空间物体边界框投影到屏幕空间：$b_{\mathrm{screen}}^{l} = \mathcal{T}_{\mathrm{camera}}^{l}(b_{\mathrm{scene}}^{l})$
  - 物体局部控制点先经全局运动变换，再经相机运动变换投射到屏幕空间：$p_{\mathrm{screen}}^{l} = \mathcal{T}_{\mathrm{camera}}^{l}(\mathcal{T}_{\mathrm{global}}^{l}(p_{\mathrm{scene}}^{l}))$

这一范式转换的关键价值在于：训练时仅需2D屏幕空间信号（点轨迹、边界框序列），这些信号可从自然视频中自动提取，无需3D标注；推理时则通过Motion Signal Translation模块桥接用户的3D意图与模型的2D条件空间。

### 条件编码机制的技术定位

在条件编码层面，MotionCanvas对相机运动和物体运动分别采用了不同的策略，与现有方法形成对比：

**相机运动条件**：采用从视频自动提取的2D点轨迹，并编码为离散余弦变换（DCT）系数作为条件（$K=10$），而非使用Plücker坐标或高斯图等需要3D标签的显式表示。消融实验（Table 4）表明，DCT轨迹编码（Traj. coeff）在RotErr（0.6334）、TransErr（0.2188）和FVD（34.09）上显著优于Gaussian map和Plücker坐标，同时仅增加1.1%的令牌开销和32秒的生成延迟。高密度点轨迹能更好地遵循轨道相机运动，而低密度轨迹会导致运动模糊且不准确。

**物体运动条件**：将物体边界框轨迹光栅化为彩色蒙版序列，利用预训练的3D-VAE编码为时空嵌入，与噪声视频潜变量求和后送入DiT，而非像**Ours_coord**那样将边界框坐标序列直接拼接到视觉令牌中。实验表明，这种时空嵌入方案在物体运动控制准确度（ObjMC 25.72 vs. 32.37）和帧质量（FID 42.47 vs. 64.32）上均大幅领先DragAnything等基线（Table 2）。

### 训练数据策略的差异

数据层面，MotionCanvas的策略与依赖专门领域数据集的基线方法形成鲜明对比：

- **基线依赖**：MotionCtrl、CameraCtrl等方法依赖RealEstate10K等包含静态场景视频和3D相机姿态标注的数据集，虽然标注质量高，但场景多样性有限。
- **MotionCanvas策略**：使用约1.1M自然视频，通过DEVA分割和RAFT光流自动提取约600K高质量的2D点追踪和边界框注释。这一策略使模型能够在丰富多样的自然场景上训练，同时避免了昂贵的3D标注成本。

### 适用边界与失效模式

尽管MotionCanvas在零样本相机运动控制和物体运动控制上均取得了领先性能，其适用边界仍需明确：

1. **推理速度限制**：视频扩散模型推理速度较慢，生成约2秒视频需要约35秒，限制了实时交互应用场景。这是扩散模型架构的固有瓶颈，非MotionCanvas特有。

2. **深度近似的精度边界**：物体局部运动被近似为正面平行深度平面，在处理极端特写或微距镜头等深度变化显著的场景时可能不准确。当物体在深度方向上发生剧烈位移时，该近似会导致屏幕空间投影偏差。

3. **多模态控制信号冲突**：系统目前未显式协调运动设计与文本提示，当用户的运动输入与文本描述不一致时（如文本描述“静止的汽车”但用户定义了移动轨迹），可能导致两个控制源之间的信号冲突，生成结果出现伪影或不自然。

4. **运动不连续性问题**：在自回归扩展（MotionCanvasAR）中，需要重新计算输入运动信号以对齐训练设置，否则可能出现运动不连续性（Figure 14）。这表明长视频生成中的运动一致性仍是一个需要额外处理的挑战。

### 开放问题

1. **深度感知的显式建模**：如何整合更显式的3D公式来处理极度特写或微距等深度变化显著的场景？可能的路径包括引入更精细的深度估计或允许用户提供稀疏深度标注。

2. **运动感知的提示协调**：如何实现运动感知的提示协调机制，以避免用户运动输入与文本描述之间的冲突？这可能需要一个显式的仲裁模块或联合优化框架。

3. **实时推理优化**：如何通过模型蒸馏、步数压缩或专用硬件加速，将生成延迟从35秒降低到可交互水平，是推动该技术走向实际应用的关键工程问题。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2025/MotionCanvas_Cinematic_Shot_Design_with_Controllable_Image_to_Video_Generation.pdf]]
