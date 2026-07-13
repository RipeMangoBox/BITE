---
title: "TokenMotion: Decoupled Motion Control via Token Disentanglement for Human-centric Video Generation"
type: paper
paper_level: A
venue: CVPR
year: 2025
pdf_ref: paperPDFs/CVPR_2025/TokenMotion_Decoupled_Motion_Control_via_Token_Disentanglement_for_Human_centric_Video_Generation.pdf
project_link: null
code_link: null
aliases:
- TokenMotion
tags:
- CVPR_2025
- topic/motion_animation
- topic/motion_animation/human_motion_generation
core_operator: "引入高细粒度的基于人体姿态（DWPose）和摄像机Plücker嵌入的运动表示，通过拆分-融合策略与动态遮罩（结合可学习分量和硬姿态先验），在统一时空令牌空间中对两种运动进行解耦和交互建模，并配合运动补丁化适配DiT骨干。"
primary_logic: "将相机轨迹和人体姿态视为同一时空令牌空间中的不同运动令牌，利用拆分-融合模块强制模型从融合表示中解耦出两类运动，并通过含有姿态先验的动态遮罩使人体运动仅作用在人体区域，从而在DiT框架下实现精细的、无冲突的联合运动控制。"
claims:
- "TokenMotion在T2V联合控制上的PoseErr（45.24）和DetErr（2.50%）远低于所有基线（例如MotionBooth的165.49和13.19%），证明人体运动控制质量的显著提升。"
- "去除拆分-融合模块（直接相加）导致FVD从361.03剧烈升高到890.39，验证了拆分-融合策略对于联合运动控制的必要性。"
- "TokenMotion在I2V上FVD达到332.27，相比ImageConductor的878.59有大幅领先，说明方法在两种生成范式下均有效。"
- "定性结果显示TokenMotion生成的视频中，人体动作与相机运动始终与输入文本提示保持一致，而基线方法常出现运动冲突或人物变形。"
---

# TokenMotion: Decoupled Motion Control via Token Disentanglement for Human-centric Video Generation

> [!tip] 核心洞察
> 将相机轨迹和人体姿态视为同一时空令牌空间中的不同运动令牌，利用拆分-融合模块强制模型从融合表示中解耦出两类运动，并通过含有姿态先验的动态遮罩使人体运动仅作用在人体区域，从而在DiT框架下实现精细的、无冲突的联合运动控制。

| 字段 | 内容 |
|------|------|
| 中文题名 | TokenMotion: 基于令牌解耦的分离式运动控制用于以人为本的视频生成 |
| 英文题名 | TokenMotion: Decoupled Motion Control via Token Disentanglement for Human-centric Video Generation |
| 会议/期刊 | CVPR 2025 |
| Links | [paper](https://arxiv.org/abs/2504.08181) |
| Topic | #topic/motion_animation #topic/motion_animation/human_motion_generation |
| Method | TokenMotion |
| Dataset | HumanVid + RealEstate10K (T2V, joint control), HumanVid + RealEstate10K (I2V, RealEstate10K (camera-only control) |

> [!tip] 效果简介
> - HumanVid + RealEstate10K (T2V, joint control) 上，FVD↓ 为 361.03，对比 795.59 (MotionBooth)，变化 -434.56。
> - HumanVid + RealEstate10K (T2V, joint control) 上，PoseErr↓ 为 45.24，对比 165.49 (MotionBooth)，变化 -120.25。
> - HumanVid + RealEstate10K (I2V, joint control) 上，FVD↓ 为 332.27，对比 878.59 (ImageConductor)，变化 -546.32。

## 概要

**核心问题**：在以人为本的视频生成中，现有方法只能单独控制相机运动或人体运动；当试图联合控制时，普遍采用边界框或对象级关键点等粗粒度表示，无法捕获细微姿态变化。同时，这些方法大多基于 UNet 骨干，将两类运动信号分离到空间和时间分支处理，缺乏对相机运动与人体运动之间空间-时间交互的统一建模能力，导致运动冲突、控制精度下降和人物变形。

**核心方法**：TokenMotion 是首个基于 DiT（Diffusion Transformer）骨干的联合运动控制框架。其核心思路是将相机轨迹和人体姿态视为同一时空令牌空间中的不同运动令牌，通过**拆分-融合（Decouple-and-Fuse）策略**与**动态遮罩**强制模型解耦两类运动信号，并在融合阶段引入基于人体姿态的硬先验，使人体运动仅作用于人体区域，从而在统一的全注意力建模下实现精细、无冲突的联合控制。具体而言，相机运动通过 Plücker 嵌入编码为逐像素射线表示，人体运动通过 DWPose 提取全身关键点；两类信号经运动补丁化压缩后，在拆分-融合模块中经由可学习掩码与硬姿态先验加权融合，最终通过交叉注意力注入视觉令牌。

**主要结果**：
- 在 T2V 联合控制任务上，TokenMotion 的 PoseErr 达到 **45.24**，远低于 MotionBooth 的 165.49；FVD 达到 **361.03**，相比 MotionBooth 的 795.59 降低约 435。
- 在 I2V 联合控制任务上，FVD 达到 **332.27**，相比 ImageConductor 的 878.59 大幅领先。
- 消融实验表明，去除拆分-融合模块（直接相加）会导致 FVD 从 361.03 急剧升高到 890.39，验证了该策略对联合运动控制的必要性。

### 问题背景

生成式视频模型近年来取得了显著进展，文本到视频（T2V）和图像到视频（I2V）的生成质量持续提升。然而，在实际应用中，用户往往需要对生成内容进行精确的运动控制——不仅需要控制摄像机的运动轨迹（如推拉摇移），还需要同时控制画面中人物的动作姿态。这种**联合运动控制**能力对于电影预可视化、虚拟内容创作等以人为本的视频生成场景至关重要。

当前方法在处理这一需求时面临一个核心瓶颈：**现有工作只能单独控制相机运动或人体运动，一旦需要联合控制，就不得不依赖粗糙的运动表示**。例如，一些方法使用对象级边界框或稀疏关键点来描述人体运动，这类粗粒度表示无法捕获细微的姿态变化（如手指动作、身体旋转角度）；同时，这些方法未对相机运动和人体运动之间的空间-时间交互进行显式建模，导致两种运动信号在生成过程中产生冲突，最终表现为控制精度下降和视觉质量退化。

### 现有方法缺口

从技术路线来看，现有联合运动控制方法存在三个层面的不足：

1. **运动表示粒度过粗**：基线方法（如 **MotionCtrl** (Wang et al., SIGGRAPH 2024)、**MotionBooth** (Wu et al., arXiv 2024)）采用对象级关键点或边界框作为人体运动条件，丢失了大量姿态细节信息，难以支撑精细的人体动作控制。

2. **多运动融合策略简单**：大多数方法对相机运动和人体运动信号分别学习后，仅通过直接加权或相加的方式进行融合，未设计专门的机制来处理两种运动在空间维度上的交互与冲突。例如，当相机向左平移而人物向右移动时，简单融合容易产生运动方向混乱或人物变形。

3. **骨干网络架构限制**：主流联合控制方法（如 **Direct-A-Video** (Yang et al., SIGGRAPH 2024)、**ImageConductor** (Li et al., arXiv 2024)）基于UNet视频扩散模型，通常将对象运动与相机运动分离到不同的空间和时间分支中处理。这种架构设计本质上限制了对两类运动信号进行统一时空建模的能力。

### 本文动机

针对上述缺口，本文的核心动机是：**在统一的时空令牌空间中，通过精细的运动表示和显式的解耦-融合机制，实现相机运动与人体运动的高质量联合控制**。

具体而言，TokenMotion的提出基于以下关键洞察：如果将相机轨迹和人体姿态视为同一时空令牌空间中的不同运动令牌，就可以利用Transformer架构（DiT）的全注意力机制对两者进行统一建模。在此基础上，通过设计专门的**拆分-融合模块**（decouple-and-fuse module），强制模型从融合表示中解耦出两类运动信号，并利用含有姿态先验的**动态遮罩**使人体运动仅作用在人体区域，从而在DiT框架下实现精细的、无冲突的联合运动控制。

这一思路的技术基础在于：DiT骨干（以 **CogVideoX-2B** (Yang et al., arXiv 2024) 为代表）通过3D全注意力机制天然支持对时空令牌的统一处理，为同时注入和交互两类运动信号提供了架构上的可行性。TokenMotion正是首个基于DiT的、面向以人为本视频生成的联合运动控制框架。

## 核心方法与创新机理

TokenMotion 的核心创新在于将**相机运动**与**人体运动**统一到同一时空令牌空间中，通过“拆分-融合”策略实现两种运动信号的解耦与协同控制，从而突破现有方法在联合运动控制中粗粒度表示与运动冲突的瓶颈。具体而言，其创新体现在三个互为支撑的维度：

### 1. 高细粒度运动表示：从对象级到像素级与全身姿态

现有联合控制方法（如 **MotionCtrl** (Wang et al., SIGGRAPH 2024)、**MotionBooth** (Wu et al., arXiv 2024)）通常使用对象级关键点或边界框来表示人体运动，这种粗粒度表示无法捕获细微的姿态变化（如手腕旋转、躯干倾斜），导致生成结果中人体动作与输入条件存在偏差。

TokenMotion 将运动表示的粒度提升至两个维度：
- **相机运动**：采用 Plücker 嵌入（Equation 2），将每个像素坐标和相机位姿编码为 6 维射线表示 $\mathbf{p}_{u,v,f} = \frac{(\mathbf{d}_{u,v,f}, \mathbf{t}_f \times \mathbf{d}_{u,v,f})}{||\mathbf{d}_{u,v,f}||}$，实现逐像素的相机轨迹描述，而非全局参数。
- **人体运动**：使用 DWPose 提取全身姿态关键点，覆盖躯干、四肢等细粒度部位，相比边界框能更精确地约束人体各部分的运动轨迹。

这一表示粒度的提升是后续解耦与融合操作的基础——只有足够精细的运动信号，才可能在令牌空间中实现区域级的控制分离。

### 2. 拆分-融合策略与动态遮罩：从信号叠加到区域感知交互

现有方法在处理多运动信号时，通常采用“分别编码后直接相加或加权”的策略，未显式建模相机运动与人体运动在空间上的交互关系。这种做法容易导致两类运动信号在人体区域产生冲突——例如相机推进时，人体运动令牌可能错误地影响背景区域的生成。

TokenMotion 的**拆分-融合模块**（Decouple-and-Fuse Module）通过以下机制解决此问题：

1. **自注意力学习全局依赖**：先将相机运动令牌 $z_{\text{camera}}^n$ 和人体运动令牌 $z_{\text{pose}}^n$ 通过自注意力建模时空依赖关系。
2. **动态遮罩生成**：通过线性层和层归一化从两类运动令牌中分别生成可学习掩码 $\mathcal{M}_{\text{camera}}^n$ 和 $\mathcal{M}_{\text{pose}}^n$（Equation 3），同时引入基于姿态关键点的**硬先验掩码** $\mathcal{M}_{\text{pose}}^{\text{prior}}$，强制人体运动信号仅作用于人体区域。
3. **掩码加权融合**：将可学习掩码与硬先验相加后通过 Softmax 归一化，对姿态和相机令牌进行加权融合（Equation 4）：
   $$z_{\text{fused}}^n = \text{Softmax}\left([ \mathcal{M}_{\text{pose}}^n + \mathcal{M}_{\text{pose}}^{\text{prior}} ; \mathcal{M}_{\text{camera}}^n ]\right) [ z_{\text{pose}}^n ; z_{\text{camera}}^n ]$$

消融实验证实了这一策略的关键作用：**去除拆分-融合模块（直接相加）导致 FVD 从 361.03 剧烈升高至 890.39**（Table 3），生成质量大幅下降，验证了显式解耦与区域感知融合对于联合运动控制的必要性。进一步地，仅使用可学习掩码而不加入姿态硬先验时，性能也略有下降（FVD 略高），表明硬先验对局部化控制具有正向贡献。

### 3. DiT 骨干适配：从 UNet 分离分支到统一时空令牌建模

现有联合控制方法（如 MotionCtrl、Direct-A-Video）多基于 UNet 骨干，将对象运动与相机运动分离到空间和时间分支中处理。这种架构设计限制了模型对两类运动信号在统一时空维度上交互关系的建模能力。

TokenMotion 首次在 **DiT（Diffusion Transformer）骨干**上实现联合运动控制，基于 CogVideoX-2B 的 3D 全注意力机制对时空令牌进行统一建模。为适配 DiT 架构，TokenMotion 引入**运动补丁化**（motion patchification）：先通过三维卷积将运动信号压缩为固定长度的令牌序列，再通过交叉注意力与 LoRA 注入视觉令牌（Equation 5）：
$$z_{\text{visual}}^n += \text{Lora}(\text{CrossAttn}(Q_{\text{visual}}^n, K_{\text{fused}}^n, V_{\text{fused}}^n))$$

消融实验表明，将运动补丁化替换为 ControlNet 风格的全尺寸特征注入会导致 FVD 升高（Table 3, "Token Compression" 行），说明补丁化有助于稳定 DiT 训练并提升控制精度。

### 创新点之间的关系

上述三个创新构成因果链条：**高细粒度表示**为拆分-融合提供了可操作的信号基础；**拆分-融合与动态遮罩**在令牌空间中实现了两类运动的解耦与区域感知交互；**DiT 骨干适配**则为这一统一建模提供了架构支撑。三者共同使 TokenMotion 在 T2V 联合控制任务上取得 PoseErr 45.24（MotionBooth 为 165.49）和 DetErr 2.50%（MotionBooth 为 13.19%）的显著提升（Table 1），并在 I2V 场景下将 FVD 从 ImageConductor 的 878.59 降至 332.27。

TokenMotion是一个基于DiT（Diffusion Transformer）架构的视频扩散框架，首次实现了对摄像机轨迹、人体运动及其联合交互的细粒度控制。该框架以CogVideoX-2B为骨干，在统一的时空令牌空间中同时建模两类运动信号，并通过拆分-融合（Decouple-and-Fuse）策略解决运动冲突问题。

整个pipeline的输入输出流如下：给定文本提示（T2V）或参考图像+文本提示（I2V），以及可选的摄像机运动参数和人体运动序列，框架首先生成对应的运动令牌，然后将这些令牌注入视觉令牌的生成过程，最终输出受控的视频序列。

框架由四个核心模块构成：

1. **Camera Motion Encoder（摄像机运动编码器）**：将逐帧的摄像机内参/外参转换为Plücker射线嵌入，再通过三维卷积压缩为固定长度的摄像机运动令牌。该表示继承了CameraCtrl（He et al., arXiv 2024）的Plücker嵌入方案，为每个像素提供独立的射线方向与原点信息。

2. **Human Motion Encoder（人体运动编码器）**：利用DWPose从视频帧中提取全身姿态关键点，通过相同的运动补丁化（motion patchification）模块生成人体运动令牌。与基线方法使用的对象级关键点或边界框相比，DWPose提供了更细粒度的姿态表示。

3. **Decouple-and-Fuse Module（拆分-融合模块）**：这是TokenMotion的核心创新。该模块首先通过自注意力学习两类运动令牌的全局依赖关系，然后利用动态遮罩（dynamic mask）分别调控摄像机运动和人体运动的影响区域。动态遮罩由两个分量组成：可学习掩码（通过线性层和层归一化从运动令牌生成）和基于姿态的硬先验（pose prior）。摄像机运动被全局投射，人体运动则通过姿态先验被约束在人体区域。最终，两种运动令牌通过Softmax加权融合为统一的运动令牌，送入后续的交叉注意力层。

4. **Cross-Attention + LoRA Injection（交叉注意力与LoRA注入）**：融合后的运动令牌作为键（Key）和值（Value），通过交叉注意力机制控制视觉令牌的更新。同时，LoRA层被用于稳定训练并保持基础模型的生成质量。

训练目标为标准去噪得分匹配损失（Equation 1）：

$$\mathbb{E}_{(z,c,s)}\left[\lambda_{\sigma}\left\|D_{\theta}(\tilde{z};\sigma,c,s)-z\right\|_{2}^{2}\right]$$

其中$z$为干净视觉令牌，$\tilde{z}$为加噪令牌，$c$为文本条件，$s$为运动条件，$D_\theta$为去噪网络。

与现有方法的本质区别在于：基线方法（如MotionCtrl、Direct-A-Video、MotionBooth）通常基于UNet骨干，将摄像机运动与对象运动分离到空间和时间分支中分别处理，且使用粗粒度的运动表示（边界框或稀疏关键点）。TokenMotion则利用DiT的3D全注意力机制对时空维度统一建模，并通过拆分-融合策略和动态遮罩在令牌级别显式解耦两类运动信号，从根本上避免了运动冲突。

![[assets/figures/papers/paper_list_l24_TokenMotion_Decoupled_Motion_Control_via_Token_Disentanglement_for_Human/figures/003_Figure_3.jpg]]
*Figure 3: Visualization of joint-control video generation results from Direct-A-Video [46], MotionCtrl [38], MotionBooth [39] and our TokenMotion-T. Above cases shows that our TokenMotion method succeeds in jointly handling controls of both human motion and camera motion, while being consistently aligned with the input prompts at the same time*

![[assets/figures/papers/paper_list_l24_TokenMotion_Decoupled_Motion_Control_via_Token_Disentanglement_for_Human/figures/001_Figure_1.jpg]]
*Figure 1: TokenMotion is a transformer-based video generation framework that enables simultaneous control of camera trajectories and human kinematic patterns. The framework demonstrates versatility across both text-to-video and image-to-video generation paradigms, while supporting flexible control configurations. *Text prompts are abbreviated for conciseness*

TokenMotion 的核心架构由三个关键模块串联构成：双运动编码器、拆分-融合模块，以及交叉注意力注入层。整体流程为：首先将相机轨迹与人体姿态分别编码为时空运动令牌，随后通过拆分-融合策略在令牌空间中解耦两类运动并建模其交互，最后将融合后的运动令牌通过交叉注意力与 LoRA 注入视觉令牌，实现对视频生成过程的精细控制（Figure 2）。

### 3.1 运动编码器

**相机运动编码器** 将每帧的相机内外参转换为逐像素的 Plücker 射线表示，以捕获精确的相机轨迹。对于帧 $f$ 中像素坐标 $(u,v)$，其 Plücker 嵌入定义为：

$$
\mathbf{p}_{u,v,f} = \frac{(\mathbf{d}_{u,v,f}, \mathbf{t}_f \times \mathbf{d}_{u,v,f})}{||\mathbf{d}_{u,v,f}||},\quad \mathbf{d}_{u,v,f} = \mathbf{R}_f\mathbf{K}_f^{-1}[u,v,1]^T + \mathbf{t}_f
$$

其中 $\mathbf{R}_f$、$\mathbf{t}_f$ 为相机外参旋转矩阵与平移向量，$\mathbf{K}_f$ 为内参矩阵。该 6 维表示将每个像素对应的射线方向和力矩编码为统一形式，随后通过三维卷积压缩为固定长度的相机运动令牌 $z_{\text{camera}}$。

**人体运动编码器** 采用 DWPose 提取全身姿态关键点，生成与视频帧对应的姿态热力图序列，并通过相同的运动补丁化模块压缩为人体运动令牌 $z_{\text{pose}}$。与基线方法使用的对象级关键点或边界框相比，DWPose 提供的全身细粒度姿态表示能捕获更细微的肢体变化。

### 3.2 拆分-融合模块

该模块是 TokenMotion 实现无冲突联合运动控制的核心机制。其设计思想是：将相机运动视为全局信号（作用于整个画面），将人体运动视为局部信号（仅作用于人体区域），通过动态遮罩强制模型解耦两类运动的影响范围。

模块首先对两类运动令牌分别施加自注意力，学习各自的时空依赖关系。随后，通过可学习的线性投影生成注意力掩码：

$$
\mathcal{M}_{\text{pose}}^n = \mathrm{LN}(\mathrm{Linear}_{\text{pose}}^n(z_{\text{pose}}^n)),\quad \mathcal{M}_{\text{camera}}^n = \mathrm{LN}(\mathrm{Linear}_{\text{camera}}^n(z_{\text{camera}}^n))
$$

其中 $\mathrm{LN}$ 为层归一化，$n$ 表示第 $n$ 个 Transformer 层。

为增强人体运动的局部化控制，模块引入基于 DWPose 姿态关键点的硬先验掩码 $\mathcal{M}_{\text{pose}}^{\text{prior}}$，该掩码在人体区域取高值、背景区域取低值。最终融合通过 Softmax 加权实现：

$$
z_{\text{fused}}^n = \mathrm{Softmax}\left([ \mathcal{M}_{\text{pose}}^n + \mathcal{M}_{\text{pose}}^{\text{prior}} ; \mathcal{M}_{\text{camera}}^n ]\right) [ z_{\text{pose}}^n ; z_{\text{camera}}^n ]
$$

这一设计的因果逻辑在于：可学习掩码提供内容自适应的运动强度调控，而硬姿态先验确保人体运动信号不会泄漏到背景区域，从而避免与相机运动产生冲突。消融实验证实，去除拆分-融合模块（直接相加）会导致 FVD 从 361.03 急剧升高至 890.39，验证了该策略的必要性（Table 3）。

### 3.3 交叉注意力注入

融合后的运动令牌通过交叉注意力机制控制视觉令牌的更新，并配合 LoRA 层稳定训练：

$$
z_{\text{visual}}^n += \mathrm{LoRA}(\mathrm{CrossAttn}(Q_{\text{visual}}^n, K_{\text{fused}}^n, V_{\text{fused}}^n))
$$

其中 $Q_{\text{visual}}^n$ 为视觉令牌的查询向量，$K_{\text{fused}}^n$、$V_{\text{fused}}^n$ 由融合运动令牌经线性投影得到。LoRA 层的引入使得运动控制信号能够以低秩适应的方式注入预训练的 DiT 骨干，在保持基础模型生成质量的同时实现精确的运动引导。

### 3.4 训练目标

整个网络 $F_\theta$ 以去噪分数匹配为目标进行训练，损失函数为标准 L2 回归：

$$
\mathbb{E}_{(z,c,s)}\left[\lambda_{\sigma}\left\|D_{\theta}(\tilde{z};\sigma,c,s)-z\right\|_{2}^{2}\right]
$$

其中 $\tilde{z}$ 为加噪后的视觉令牌，$\sigma$ 为噪声水平，$c$ 为文本条件，$s$ 为运动条件，$\lambda_{\sigma}$ 为噪声水平相关的权重系数。

## 实验与关键发现

### 核心定量结果：联合运动控制

TokenMotion 在 T2V 与 I2V 两种范式下均实现了对相机运动与人体运动的联合精细控制，并在各项指标上显著超越现有基线。Table 1 汇总了联合控制任务上的定量对比。

![[assets/figures/papers/paper_list_l24_TokenMotion_Decoupled_Motion_Control_via_Token_Disentanglement_for_Human/figures/005_Table_1.jpg]]
*Table 1: Quantitative comparisons for joint controlling camera and human motion for both T2V and I2V generation. * denotes the original CogVideoX model, whose camera metrics and human-motion metrics are not calculated because no motion control is performed*

在 T2V 场景下，TokenMotion 的 FVD 达到 361.03，相比最强基线 MotionBooth 的 795.59 降低了 434.56，降幅超过 50%。人体运动控制精度方面，TokenMotion 的 PoseErr 仅为 45.24，而 MotionBooth 为 165.49，Direct-A-Video 为 117.39，MotionCtrl 为 114.65，说明基于 DWPose 的细粒度姿态表示和拆分-融合策略有效捕获了细微的姿态变化。检测误差 DetErr 方面，TokenMotion 达到 2.50%，远低于 MotionBooth 的 13.19% 和 Direct-A-Video 的 7.00%，验证了动态遮罩对人体区域定位的有效性。

在 I2V 场景下，TokenMotion 的 FVD 为 332.27，相比 ImageConductor 的 878.59 降低了 546.32，降幅达 62%。值得注意的是，ImageConductor 本身采用分离式控制设计，但 TokenMotion 在 DiT 骨干上通过统一的时空令牌建模实现了更优的联合控制效果。

基础模型 CogVideoX-2B（无运动控制）的 FVD 为 402.34，仅反映生成质量基线，其相机和人体运动指标因无法执行运动控制而未计算。

### 相机单独控制与泛化能力

Table 2 展示了仅相机控制任务上的定量结果。TokenMotion 的 KptsErr 为 4.36，显著优于 MotionCtrl 的 6.72，与 Direct-A-Video 的 3.85 接近但在综合指标上更优。定性结果（Figure 4）显示，TokenMotion 在多样化场景和复杂相机轨迹（如环绕、推拉）下保持了较高的视觉保真度，且控制灵活性优于商业工具 Runway。

![[assets/figures/papers/paper_list_l24_TokenMotion_Decoupled_Motion_Control_via_Token_Disentanglement_for_Human/figures/007_Table_2.jpg]]
*Table 2: Quantitative evaluation results for camera-only control video generation*

### 消融实验

Table 3 系统验证了三个关键设计选择的有效性：

![[assets/figures/papers/paper_list_l24_TokenMotion_Decoupled_Motion_Control_via_Token_Disentanglement_for_Human/figures/009_Table_3.jpg]]
*Table 3: Ablation studies about Token Compression, Decouple and fusion, and Hybrid-mask*

**令牌压缩（Token Compression）**：将运动补丁化替换为 ControlNet 风格的全尺寸特征注入后，FVD 从 361.03 升高至约 400，表明将运动信号压缩为固定长度令牌有助于稳定 DiT 训练并提升控制精度。

**拆分-融合模块（Decouple-and-Fuse）**：去除该模块，直接将相机和人体运动令牌相加（direct addition），FVD 从 361.03 剧烈升高至 890.39，生成质量大幅下降。这验证了拆分-融合策略对于联合运动控制的必要性——简单的线性组合无法处理两类运动信号的空间-时间交互，导致运动冲突和生成退化。

**混合遮罩（Hybrid-mask）**：仅使用可学习遮罩而不加入基于姿态的硬先验时，性能略低于混合遮罩（FVD 略有升高），证明姿态先验有助于将人体运动控制局部化到人体区域，减少对背景的干扰。

### 定性分析

Figure 3 的定性对比直观展示了各方法的差异。TokenMotion 生成的视频中，人体动作与相机运动始终与输入文本提示保持一致，而 Direct-A-Video、MotionCtrl 和 MotionBooth 常出现运动冲突（如相机平移时人体姿态漂移）或人物变形。Figure 6 和 Figure 7 进一步展示了 TokenMotion 在复杂人体动作组合和不同粒度运动控制（包括大肢体运动和面部表情变化）上的能力。

![[assets/figures/papers/paper_list_l24_TokenMotion_Decoupled_Motion_Control_via_Token_Disentanglement_for_Human/figures/008_Figure_6.jpg]]
*Figure 6: Human-motion control with complex composition. (b) Human-motion control with large body movements. Figure 7. Control with human motions of different granularity*

### 局限性与失败模式

尽管 TokenMotion 在联合运动控制上取得了显著进展，仍存在以下局限：

1. **精细动作建模不足**：对手指运动和面部表情细节的建模仍有待加强，生成结果在这些区域可能出现模糊或失真。当前基于 DWPose 的 2D 关键点表示难以捕获手指关节的细微运动，引入 3D 参数化模型（如 SMPL）可能是改进方向。

2. **视觉质量受限于基础模型**：当前模型建立在 CogVideoX-2B 骨干上，视频视觉质量受限于基础模型的规模和训练数据，与更大规模的商业模型相比仍有差距。适配到更大规模 DiT 骨干（如 CogVideoX-5B）的可扩展性尚未验证。

3. **场景泛化性未充分验证**：评估主要使用 HumanVid 和 RealEstate10K，对动态背景、多人物复杂交互等更广泛场景的泛化性尚不明确。

4. **训练数据偏差**：训练时对缺少人体运动的 RealEstate10K 样本输入空白人体运动提示，可能导致模型在纯摄像机运动场景中对人体运动信号的处理存在鲁棒性不足。

5. **基线公平性**：部分基线（如 MotionCtrl、Direct-A-Video）基于 UNet 骨干，与 DiT 骨干的参数量和训练数据可能不同，性能差异也可能部分源于基础模型的差异，需在解读定量对比时予以注意。

## 定位与知识库关联

**核心定位**：TokenMotion 是首个基于 DiT（Diffusion Transformer）骨干的视频扩散框架，针对**以人为本的视频生成**中的相机运动与人体运动**联合精细控制**问题，提出了基于令牌解耦与动态遮罩的分离式控制策略。

**与已有工作的关系与推进**：

1. **从 UNet 到 DiT 的骨干迁移**：此前联合控制相机与对象运动的方法，如 **MotionCtrl** (Wang et al., SIGGRAPH 2024)、**Direct-A-Video** (Yang et al., SIGGRAPH 2024) 和 **MotionBooth** (Wu et al., arXiv 2024)，均建立在 UNet 骨干之上，通常将相机运动与对象运动分别注入空间和时间分支。这种架构设计难以在统一的时空维度上建模两类运动的交互。TokenMotion 选择 **CogVideoX-2B** (Yang et al., arXiv 2024) 作为 DiT 基础模型，利用其 3D 全注意力机制对时空令牌进行统一建模，为联合运动控制提供了更一致的表示空间。

2. **从粗粒度到细粒度的运动表示升级**：现有方法在联合控制时多使用边界框或对象级关键点等粗粒度表示，无法捕获细微的姿态变化。TokenMotion 引入**基于 DWPose 的全身姿态关键点**作为人体运动信号，并使用 **Plücker 嵌入**（沿袭 **CameraCtrl** (He et al., arXiv 2024) 的相机表示方案）将相机位姿编码为逐像素射线表示，从而在令牌空间中实现高细粒度的运动描述。

3. **从独立注入到拆分-融合的交互建模**：以往方法通常对相机和人体运动信号分别学习后直接相加或加权融合，缺乏对两类运动空间-时间交互的显式建模，容易导致运动冲突。TokenMotion 的核心创新在于**拆分-融合（Decouple-and-Fuse）模块**：先将相机运动令牌和人体运动令牌通过自注意力学习全局依赖，再通过**动态遮罩**（融合可学习分量和基于姿态的硬先验）分别调控两类运动的作用区域，最后经 Softmax 加权融合为统一运动令牌，通过交叉注意力注入视觉令牌。这一机制强制模型从融合表示中解耦出两类运动，并使人体运动仅作用于人体区域，有效避免了运动冲突。

4. **与仅相机控制方法的对比**：在纯相机控制任务上，TokenMotion 的旋转误差（RotErr 0.71°）和平移误差（TransErr 5.19）显著优于 **MotionCtrl**（1.79°/14.14），关键点误差（KptsErr 4.36）也优于 **MotionCtrl**（6.72），但略高于 **Direct-A-Video**（3.85）。这表明 TokenMotion 在保持联合控制能力的同时，其相机控制精度已达到或超越专用相机控制方法的水准。

**适用边界与局限**：

- **精细动作与面部细节不足**：当前方法对**手指运动**和**面部表情**的建模仍有明显局限，生成结果在这些区域可能出现模糊或失真。这受限于 DWPose 的姿态表示粒度，若引入 SMPL 等 3D 参数化模型可能有所改善，但尚未验证。
- **视觉质量受限于基础模型规模**：TokenMotion 建立在 CogVideoX-2B 之上，生成视频的视觉保真度与 **Runway Alpha Gen3** 等大规模商业模型相比仍有差距。定性结果（Figure 4）虽显示 TokenMotion 在控制灵活性上优于 Runway，但视觉质量本身并非其优势所在。
- **多人场景与复杂背景的泛化性未验证**：当前评估主要使用 **HumanVid** 和 **RealEstate10K** 数据集，对动态背景、多人物复杂交互等更广泛场景的泛化能力尚不明确。动态遮罩机制理论上可扩展为实例级遮罩以支持多人独立控制，但这一方向尚未探索。
- **训练策略的潜在偏差**：训练时对无人体运动的 RealEstate10K 样本输入空白人体运动提示，可能导致模型在纯相机运动场景中倾向于忽略人体运动信号，影响该类场景下的鲁棒性。

**开放问题**：

1. 如何将 TokenMotion 的联合控制策略适配到更大规模的 DiT 骨干（如 CogVideoX-5B 或更高版本），以同时提升生成质量和运动控制精度？
2. 能否引入更丰富的人体运动表示（如 3D 参数化模型 SMPL）来解决手指和面部的细节问题？
3. 是否可以将动态遮罩扩展为实例级遮罩，以支持多人场景中不同人物的独立运动控制？
4. 在保持控制精度的同时，如何降低训练和推理的计算开销，以适应实时或低资源场景？

## 原文 PDF

![[paperPDFs/CVPR_2025/TokenMotion_Decoupled_Motion_Control_via_Token_Disentanglement_for_Human_centric_Video_Generation.pdf]]
