---
title: "3D Scene Prompting for Scene-Consistent Camera-Controllable Video Generation"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/3D_Scene_Prompting_for_Scene_Consistent_Camera_Controllable_Video_Generation.pdf
aliases:
- 3SPSCCCVG
- 3DScenePrompt
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: "引入双时空滑动窗口策略，在标准时间邻域条件化之外，增加基于3D场景记忆的空间邻域条件化。该记忆仅保留从完整输入视频中提取的静态几何结构，通过动态SLAM和动态掩码策略实现。"
primary_logic: "视频中的邻域关系不仅是时间上的，也是空间上的。当相机回访相似视角时，生成帧可能与输入序列中很早的帧在空间上相邻。利用这一双重邻域性质，通过静态3D点云投影提供几何一致的空间提示，同时允许动态区域从时间上下文自然演化，从而在不增加计算负担的情况下实现长程空间一致性。"
claims:
- "在RealEstate10K和DynPose-100K数据集上，3DScenePrompt在空间一致性（PSNR, SSIM, LPIPS）和几何一致性（MEt3R）指标上均显著优于DFoT基线。"
- "与DFoT相比，MEt3R评估误差降低了77%（0.041 vs 0.181）。"
- "消融实验表明，不使用动态掩码时PSNR下降约0.8dB，MEt3R误差增加；不使用空间投影（n=0）时场景一致性和相机控制精度显著下降。"
- "在DynPose-100K上，3DScenePrompt在相机控制精度（mRotErr, mTransErr, mCamMC）和视频质量（FVD, VBench++）方面均达到最优。"
---

# 3D Scene Prompting for Scene-Consistent Camera-Controllable Video Generation

> [!tip] 核心洞察
> 视频中的邻域关系不仅是时间上的，也是空间上的。当相机回访相似视角时，生成帧可能与输入序列中很早的帧在空间上相邻。利用这一双重邻域性质，通过静态3D点云投影提供几何一致的空间提示，同时允许动态区域从时间上下文自然演化，从而在不增加计算负担的情况下实现长程空间一致性。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 3D场景提示：面向场景一致且相机可控的视频生成 |
| 英文题名 | 3D Scene Prompting for Scene-Consistent Camera-Controllable Video Generation |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=3XxoBwMusJ); [Project](https://cvlab-kaist.github.io/3DScenePrompt) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | 3DScenePrompt |
| Dataset | RealEstate10K |

> [!tip] 效果简介
> - RealEstate10K 上，PSNR 为 20.8932，对比 17.8919，变化 +3.0013。
> - RealEstate10K 上，SSIM 为 0.7171，对比 0.6362，变化 +0.0809。
> - RealEstate10K 上，LPIPS 为 0.2120，对比 0.2995，变化 -0.0875。

## 概述

3DScenePrompt（ICLR 2026）针对现有相机可控视频生成方法的一个根本瓶颈：它们只能利用极短的输入序列（通常仅几帧）作为条件，当需要回访早期视角或探索邻近区域时，生成内容与输入视频的场景几何严重不一致。该问题的根源在于，现有方法仅将视频中的邻域关系理解为时间上的，而忽略了空间上的邻域关系——当相机回访相似视角时，生成帧可能与输入序列中很早的帧在空间上相邻。

本文的核心洞察是引入**双时空滑动窗口策略**，在标准的时间邻域条件化之外，增加基于3D场景记忆的空间邻域条件化。该记忆通过动态SLAM（MegaSAM / DepthAnything v3）和一套三阶段动态掩码流水线（光流差异检测→反向点跟踪聚合→SAM2传播生成物体级掩码），从完整输入视频中提取并保留**仅包含静态几何结构**的3D点云。生成时，将该点云投影到目标相机视角，提供几何一致的空间提示帧，而动态区域则从时间上下文自然演化。该方法无需修改扩散模型架构，通过零填充槽注入条件信息。

决定性证据来自定量评估：在RealEstate10K和DynPose-100K数据集上，3DScenePrompt在空间一致性（PSNR、SSIM、LPIPS）和几何一致性（MEt3R）指标上均显著优于主要基线DFoT。其中，在RealEstate10K上MEt3R评估误差降低了77%（0.041 vs 0.181）。消融实验进一步验证了核心设计：不使用动态掩码时PSNR下降约0.8dB，MEt3R误差增加；不使用空间投影（n=0）时场景一致性和相机控制精度显著下降。在DynPose-100K上，该方法在相机控制精度（mRotErr、mTransErr、mCamMC）和视频质量（FVD、VBench++）方面均达到最优。

## 背景与动机

现有的相机可控视频生成方法（如CameraCtrl, MotionCtrl, FloVD, VD3D）通常仅以单张图像或文本作为条件，生成遵循指定相机轨迹的视频。这类方法在面对需要与长输入视频保持场景一致性的任务时，暴露出根本性缺陷：由于缺乏对完整场景几何结构的理解，生成的视频在相机回访早期视角或探索邻近区域时，内容与输入视频的场景几何严重不一致。

更近期的视频到未来视频生成方法（如DFoT）通过时间滑动窗口机制，利用输入视频的最后几帧来保证时间连贯性（即V_out = G(V_in[L-w:L], T)）。然而，这种仅依赖时间邻域条件化的策略存在一个关键瓶颈：当相机轨迹需要回访输入视频中较早出现的视角时，最后几帧中不包含该视角的几何信息，导致生成帧无法维持与输入视频的空间一致性。这种“空间记忆缺失”是现有方法在长程场景一致生成中的核心障碍。

本文的动机正是为了解决这一缺口。核心洞察在于：视频中的邻域关系不仅是时间上的，也是空间上的。当相机回访相似视角时，生成帧可能与输入序列中很早的帧在空间上相邻。基于此，作者提出双时空条件化策略，在标准的时间邻域条件化之外，增加基于3D场景记忆的空间邻域条件化。该记忆仅保留从完整输入视频中提取的静态几何结构，通过动态SLAM（MegaSAM / DepthAnything v3）和精心设计的三阶段动态掩码流水线（光流差异检测 → 反向点跟踪聚合 → SAM2传播生成物体级掩码），识别并排除了动态区域，从而构建纯净的静态3D点云。对于每个目标相机姿态C_t，通过投影该静态点云生成空间提示帧，与时间邻域帧共同作为视频扩散模型（CogVideoX-I2V-5B）的条件输入。整个过程无需修改模型架构，通过零填充槽注入条件化信息。

这一设计的关键因果机制在于：空间提示帧提供了与目标视角几何对齐的静态场景信息，迫使生成过程在结构上锚定于输入视频的场景几何；而时间邻域帧则负责保证动态区域的运动连贯性，允许其自然演化。两者的协同作用使得模型能够在不增加计算负担的情况下，实现长程空间一致性。

## 核心创新

3DScenePrompt 的核心创新在于重新定义了视频生成的条件化策略，将仅依赖时间邻域窗口的范式扩展为**双时空滑动窗口条件化**。其根本洞察在于：视频帧之间的邻域关系不仅存在于时间轴上（相邻帧），也存在于空间轴上（相似视角的帧）。当相机回访早期视角时，目标帧与输入序列中较早的帧在空间上相邻，但它们在时间上相距甚远，因此无法被传统的时间窗口捕获。

**因果机制**：现有方法（如 DFoT）仅使用输入视频的最后 w 帧作为条件（Equation 3: `V_out = G(V_in[L-w:L], T)`），这导致两个瓶颈：1）当需要生成回访早期视角的内容时，条件帧中不包含该视角的信息，模型只能“猜测”场景几何；2）动态物体在条件帧中的位置与真实场景不一致，进一步破坏了空间一致性。3DScenePrompt 通过引入**3D场景记忆**（`M = (C_hat, P_static)`）来打破这一瓶颈。该记忆仅保留从完整输入视频中提取的**静态几何结构**（Equation 7: `P_static = union of P_i ⊙ (1 - M_i_obj)`），并通过投影生成空间提示帧（Equation 9: `Spatial(t) = Π(K · C_t · P_static^(n))`）。这样，模型在生成时同时获得：时间邻域帧（保证运动连贯性）和空间邻域帧（保证几何一致性），如 Equation 4 所示。

**关键变更槽位**：

1. **条件化策略**：从“仅时间窗口”（baseline）变为“双时空窗口”。这是最根本的变更，直接对应论文的核心公式 Equation 4。

2. **空间信息表示**：从“直接检索历史帧”（包含动态内容，导致鬼影）变为“构建仅静态的3D点云记忆”。这一变更通过三阶段动态掩码流水线实现（Figure 5）：(1) 光流差异检测像素级运动；(2) 反向点跟踪聚合跨帧运动证据；(3) SAM2 传播生成完整物体级掩码。消融实验（Table 6）表明，不使用动态掩码时 PSNR 下降约 0.8dB，MEt3R 误差显著增加，证实了静态几何提取的必要性。

3. **动态物体处理**：从“无显式处理”变为“三阶段流水线”。这是支撑变更 2 的关键工程贡献，直接决定了静态点云的纯净度。

4. **架构修改**：从“需要 ControlNet 风格适配器”（baseline 方法）变为“无需架构修改，通过零填充槽注入条件”。这一变更降低了实现复杂度，使得方法可以直接基于 CogVideoX-I2V-5B 等现有模型实现。

**决定性证据**：

- **定量压倒性优势**：在 RealEstate10K 上，3DScenePrompt 的 PSNR 达到 20.89（DFoT 为 17.89，+3.00），MEt3R 误差从 0.181 降至 0.041（降低 77%）。在 DynPose-100K 上，相机控制精度（mRotErr: 2.38 vs 3.41）和视频质量（FVD: 127.48 vs 142.65）均全面超越基线（Table 1, 2, 3）。

- **消融验证**：Table 4 和 Table 8 显示，不使用空间投影（n=0）时所有指标显著下降，而使用 n=4 或 n=7 个投影视图时性能大幅提升，且 n=7 后趋于稳定。这直接证明了空间邻域条件化的必要性。

- **定性对比**：Figure 6 和 Figure 7 的视觉结果直观展示了 DFoT 在回访早期视角时生成内容与输入视频不一致（如白色墙壁变为其他内容），而 3DScenePrompt 能准确保持场景几何。

**证据强度**：Table 1-3 的定量结果置信度均为 1.0，消融实验置信度 0.95-1.0。唯一需要谨慎的是“无需架构修改”这一主张（置信度 0.95），因为虽然论文声称通过零填充槽注入，但具体实现细节（如如何处理不同数量的条件帧）仍需验证。

## 整体框架

![[assets/figures/papers/iclr26_0001_3XxoBwMusJ_3D_Scene_Prompting_for_Scene-Consistent_Camera-C/figures/001_Figure_1.jpg]]
*Figure 1: Teaser. Our framework generates the next video chunk that follows a user-specified camera trajectory while maintaining scene consistency. Our dual spatio-temporal conditioning jointly leverages the last few frames to ensure temporal continuity and the rendered point cloud to enforce spatial consistency*

3DScenePrompt 的核心设计围绕一个瓶颈展开：现有相机可控视频生成方法（如 DFoT）仅依赖短时间邻域窗口（通常最后 w 帧）进行条件化，当相机回访早期视角或探索邻近区域时，生成内容与输入视频的场景几何严重不一致。其根本原因在于，视频中的邻域关系不仅是时间上的，也是空间上的——回访视角可能与输入序列中很早的帧在空间上相邻，但时间窗口无法覆盖这种长程空间关联。

为解决此问题，论文引入 **双时空滑动窗口策略**，将标准的时间邻域条件化与基于 3D 场景记忆的空间邻域条件化并行组合。整体流水线（Figure 3）如下：

1.  **动态 SLAM 与 3D 结构提取**：输入任意长度视频 $V_{\mathrm{in}} \in \mathbb{R}^{L \times H \times W \times 3}$ 后，首先通过动态 SLAM 框架（MegaSAM 或 DepthAnything v3）估计相机姿态 $\hat{\mathbf{C}}$ 和初始 3D 点云 $\mathbf{P}$（Equation 5）。这一步建立了几何基础，但点云中混杂了动态物体。

2.  **动态掩码流水线**：这是构建干净静态记忆的关键。采用三阶段流水线（Figure 5）：
    - **光流差异检测**：计算光流与基于深度的 warp 流之间的 L1 差异，阈值化得到像素级动态掩码 $M_i^{\mathrm{pixel}}$（Equation 6）。
    - **反向点跟踪聚合**：对检测到的动态区域采样点，使用 CoTracker3 进行跨所有帧的反向跟踪，聚合运动证据以捕获任何时刻移动的物体。
    - **SAM2 传播**：将聚合后的第一帧动态点传播至整个视频，生成完整物体级掩码 $M_i^{\mathrm{obj}}$。
    
    最终通过 $\mathbf{P}_{\mathrm{static}} = \bigcup_{i=1}^{L} \mathbf{P}_i \odot (1 - M_i^{\mathrm{obj}})$（Equation 7）得到仅包含静态几何的点云。

3.  **3D 场景记忆构建**：将估计的相机姿态与静态点云组合为 3D 场景记忆 $\mathcal{M} = (\hat{\mathbf{C}}, \mathbf{P}_{\mathrm{static}})$（Equation 8）。该记忆是整个框架的“空间锚点”，为后续生成提供全局一致的几何参考。

4.  **空间提示生成**：对于目标相机姿态 $C_t$，通过投影方程 $\mathrm{Spatial}(t) = \Pi(K \cdot C_t \cdot \mathbf{P}_{\mathrm{static}}^{(n)})$（Equation 9）将静态点云渲染为 n 个空间提示帧。这些帧从空间最相关的输入视角投影而来，提供几何一致的条件化信号。

5.  **双时空条件化与视频生成**：最终条件化集合为 $\tilde{\mathbf{V}}_{\mathrm{in}} = \{\mathrm{Temporal}(w)\} \cup \{\mathrm{Spatial}(T)\}$（Equation 4），其中 Temporal(w) 是最后 w 帧（保证运动连续性），Spatial(T) 是空间投影帧（保证场景几何一致性）。这些帧通过零填充槽直接注入视频扩散模型 CogVideoX-I2V-5B，无需任何架构修改。输出视频 $V_{\mathrm{out}} \in \mathbb{R}^{T \times H \times W \times 3}$ 同时遵循用户指定的相机轨迹 $\mathbf{C}$。

**关键设计选择**：时间窗口大小 w=9 是平衡运动连贯性与计算效率的折中（Table 7 消融验证）；空间投影数量 n=7 时性能趋于稳定（Table 8 消融验证）。动态掩码的存在至关重要——消融实验（Table 6）显示，不使用动态掩码时 PSNR 下降约 0.8dB，MEt3R 误差显著增加，因为动态物体会在点云中产生“鬼影”伪影（Figure 4）。

**与其他方法的本质区别**：相比 DFoT 仅使用时间邻域（Equation 3），3DScenePrompt 通过 3D 场景记忆实现了空间邻域的条件化，使得生成帧在回访视角时能与输入视频中任意早的帧保持几何一致。相比 ReCamMaster 等长程方法，本框架不局限于输入视频的时空覆盖范围，而是通过显式静态几何记忆实现更灵活的空间推理。相比 SPMem 等并发工作，本框架采用不同的动态物体处理策略（三阶段流水线 vs. 朴素 TSDF）和条件化架构（零填充注入 vs. 额外适配器）。

## 核心模块与公式推导

本节梳理 3DScenePrompt 的核心设计模块及其数学形式化表达，重点阐明“双时空条件化”如何通过静态 3D 场景记忆解决长程空间一致性问题。

### 问题形式化与基线对比

现有相机可控视频生成方法（如 CameraCtrl, MotionCtrl）仅以单帧或文本为条件，其生成过程可写为：

$$
\mathbf{V}_{\mathrm{out}} = \mathcal{F}(\mathbf{I}_{\mathrm{ref}}, \mathcal{T}, \mathbf{C}), \quad \text{或} \quad \mathbf{V}_{\mathrm{out}} = \mathcal{F}(\mathcal{T}, \mathbf{C})
$$

其中 $\mathbf{I}_{\mathrm{ref}}$ 为参考图像，$\mathcal{T}$ 为文本描述，$\mathbf{C} = \{C_t\}_{t=1}^T$ 为期望的相机轨迹。这类方法无法利用输入视频中的丰富场景上下文。

视频到未来视频生成方法（如 DFoT）使用时间滑动窗口，仅以最后 $w$ 帧作为条件：

$$
\mathbf{V}_{\mathrm{out}} = \mathcal{G}(\mathbf{V}_{\mathrm{in}}[L-w:L], \mathcal{T})
$$

其中 $\mathbf{V}_{\mathrm{in}} \in \mathbb{R}^{L \times H \times W \times 3}$ 为输入视频，$L$ 为帧数。该策略的瓶颈在于：当生成帧需要回访输入视频中较早的视角时，条件窗口内不包含该空间信息，导致场景几何不一致。

### 双时空条件化（核心公式）

3DScenePrompt 的核心创新在于将条件化从单一时间轴扩展为双时空轴：

$$
\mathbf{V}_{\mathrm{out}} = \mathcal{F}(\tilde{\mathbf{V}}_{\mathrm{in}}, T, \mathbf{C}), \quad \text{其中} \quad \tilde{\mathbf{V}}_{\mathrm{in}} = \{\mathrm{Temporal}(w)\} \cup \{\mathrm{Spatial}(T)\}
$$

- **时间邻域** $\mathrm{Temporal}(w)$：输入视频的最后 $w$ 帧，用于保证运动连贯性。
- **空间邻域** $\mathrm{Spatial}(T)$：从 3D 场景记忆投影到目标视角的 $n$ 帧（实验中 $n=7$ 性能趋于稳定），用于提供几何一致的空间提示。

该公式的本质是：视频的邻域关系不仅是时间上的，也是空间上的。当相机回访相似视角时，生成帧与输入序列中较早的帧在空间上相邻，因此需要空间维度的条件化。

### 3D 场景记忆构建

#### 动态 SLAM 与静态点云提取

首先通过动态 SLAM 从输入视频估计相机姿态和 3D 点云：

$$
(\hat{\mathbf{C}}, \mathbf{P}) = \mathcal{D}_{\mathrm{SLAM}}(\mathbf{V}_{\mathrm{in}})
$$

其中 $\hat{\mathbf{C}}$ 为估计的相机姿态，$\mathbf{P}$ 为初始 3D 点云。由于点云中包含动态物体的鬼影伪影，需要动态掩码流水线进行过滤。

#### 三阶段动态掩码流水线

1. **像素级运动检测**：基于光流差异的阈值化生成像素级掩码：
   
$$
M_i^{\mathrm{pixel}} = \Im\left[\|\mathrm{Flow}_{\mathrm{optical}} - \mathrm{Flow}_{\mathrm{warp}}\|_1 > \tau\right]
$$

   其中 $\mathrm{Flow}_{\mathrm{optical}}$ 为光流估计，$\mathrm{Flow}_{\mathrm{warp}}$ 为基于深度和相机姿态的 warp 流，$\tau$ 为阈值。

2. **反向点跟踪聚合**：从检测到的运动区域采样点，使用 CoTracker3 进行跨帧反向跟踪，聚合所有帧中该物体的运动证据。

3. **SAM2 传播**：将第一帧中聚合的运动点传播到整个视频，生成完整的物体级掩码。

最终静态点云为：

$$
\mathbf{P}_{\mathrm{static}} = \bigcup_{i=1}^{L} \mathbf{P}_i \odot (1 - M_i^{\mathrm{obj}})
$$

其中 $M_i^{\mathrm{obj}}$ 为物体级动态掩码，$\odot$ 为逐元素过滤。

#### 3D 场景记忆

3D 场景记忆由估计的相机姿态和静态点云组成：

$$
\mathcal{M} = (\hat{\mathbf{C}}, \mathbf{P}_{\mathrm{static}})
$$

该记忆仅保留输入视频中所有空间相关帧的静态几何结构，不包含动态内容。

### 空间提示生成

对于目标相机姿态 $C_t$，通过投影静态点云生成空间提示帧：

$$
\mathrm{Spatial}(t) = \Pi(K \cdot C_t \cdot \mathbf{P}_{\mathrm{static}}^{(n)})
$$

其中 $\Pi$ 为投影函数，$K$ 为相机内参，$\mathbf{P}_{\mathrm{static}}^{(n)}$ 为从 $n$ 个最相关输入帧中选取的静态点云子集。投影过程本质上是将 3D 场景记忆渲染到目标视角，生成几何一致的 RGB 帧作为空间条件。

### 关键设计选择

1. **无需架构修改**：空间和时间条件通过零填充槽注入 CogVideoX-I2V-5B 模型，不改变扩散 Transformer 架构。
2. **时间窗口大小**：$w=9$ 在运动连贯性和计算效率之间取得平衡（Table 7 消融实验验证）。
3. **空间提示数量**：$n=7$ 时性能趋于稳定，更多投影视图带来的增益有限（Table 4, Table 8 消融实验验证）。
4. **动态掩码必要性**：不使用动态掩码时 PSNR 下降约 0.8dB，MEt3R 误差显著增加（Table 6 消融实验验证），说明动态物体污染是空间一致性退化的关键原因。

### 公式体系总结

| 公式 | 含义 | 关键变量 |
|------|------|----------|
| Eq.1 | 问题定义：输入视频 → 输出视频 | $\mathbf{V}_{\mathrm{in}}, \mathbf{C}, T$ |
| Eq.4 | 双时空条件化 | $\mathrm{Temporal}(w), \mathrm{Spatial}(T)$ |
| Eq.5 | 动态 SLAM 估计 | $\hat{\mathbf{C}}, \mathbf{P}$ |
| Eq.6 | 光流差异运动检测 | $M_i^{\mathrm{pixel}}, \tau$ |
| Eq.7 | 静态点云聚合 | $\mathbf{P}_{\mathrm{static}}, M_i^{\mathrm{obj}}$ |
| Eq.8 | 3D 场景记忆 | $\mathcal{M} = (\hat{\mathbf{C}}, \mathbf{P}_{\mathrm{static}})$ |
| Eq.9 | 空间提示投影 | $\Pi, K, C_t, \mathbf{P}_{\mathrm{static}}^{(n)}$ |

该公式体系的核心因果链条为：**动态掩码 → 静态点云 → 3D 场景记忆 → 空间提示投影 → 双时空条件化 → 场景一致生成**。每个环节的失败（如动态掩码质量差）都会导致下游几何一致性的退化，这解释了为什么消融实验中移除动态掩码会导致 PSNR 和 MEt3R 显著下降。

## 实验与分析

### 主要结果

**空间与几何一致性。** 主实验在RealEstate10K（静态场景）和DynPose-100K（动态场景）两个基准上进行，评估回访早期视角时的生成一致性。如Table 1所示，3DScenePrompt在所有指标上显著超越基线DFoT。在RealEstate10K上，PSNR从17.89提升至20.89（+3.00 dB），SSIM从0.636提升至0.717，LPIPS从0.300降至0.212。几何一致性指标MEt3R的改进更为突出：误差从0.181降至0.041，降幅达77%，表明空间提示对保持场景几何结构的决定性作用。在更具挑战性的DynPose-100K动态场景上，PSNR提升0.82 dB（12.23→13.05），SSIM提升0.060（0.306→0.367），MEt3R误差降低8%（0.135→0.124）。LPIPS在该数据集上差异极小（0.382 vs 0.381），这可能是由于动态场景中运动区域的感知质量主导了该指标，而空间提示主要影响静态背景一致性。

**相机控制精度与视频质量。** Table 2和Table 3在DynPose-100K上对比了多种方法。在相机控制方面，3DScenePrompt的旋转误差（mRotErr=2.377）、平移误差（mTransErr=7.417）和综合相机运动一致性误差（mCamMC=8.635）均优于所有基线，包括单帧条件化方法（CameraCtrl, MotionCtrl, FloVD, VD3D）和长程场景一致方法（ReCamMaster, TrajectoryCrafter, Star-Gen）。在视频质量方面，FVD降至127.48（对比DFoT的142.65），VBench++综合得分提升至0.775（对比DFoT的0.743）。这些结果表明，双时空条件化在提升空间一致性的同时，并未牺牲视频的自然度和运动连贯性。

![[assets/figures/papers/iclr26_0001_3XxoBwMusJ_3D_Scene_Prompting_for_Scene-Consistent_Camera-C/figures/007_Table_2.jpg]]
*Table 2: Camera controllability evaluation*

### 消融实验

**空间提示的关键性。** Table 4和Table 8系统地研究了空间投影图像数量n的影响。当n=0（即仅使用时间条件化，不使用空间提示）时，PSNR从13.05降至12.53，MEt3R误差从0.124增至0.132，且相机控制精度显著下降（mRotErr从2.38增至3.02）。当n=4时性能大幅提升，n=7时趋于稳定，进一步增加n带来的改进微乎其微。这验证了空间提示是场景一致性的核心因果机制——仅靠时间窗口无法提供回访视角所需的几何信息。

![[assets/figures/papers/iclr26_0001_3XxoBwMusJ_3D_Scene_Prompting_for_Scene-Consistent_Camera-C/figures/011_Table_4.jpg]]
*Table 4: Ablation study on varying n*

**动态掩码的必要性。** Table 6的消融实验表明，移除动态掩码（使用包含动态物体的朴素点云）导致PSNR下降约0.8 dB，MEt3R误差显著增加。Figure 4直观展示了这一机制：无掩码时，移动物体（如马匹和骑手）在点云中产生“鬼影”伪影，投影到新视角后严重破坏场景几何。三阶段动态掩码流水线（光流差异→反向点跟踪→SAM2传播）通过生成完整的物体级掩码，有效解决了这一问题。

**时间窗口大小的权衡。** Table 7显示，时间窗口w从1增加到9时，相机控制精度持续提升（mRotErr从2.83降至2.38），同时运动平滑度（VBench运动平滑指标）保持稳定。w=9被选为平衡计算效率和运动连贯性的关键设计点。进一步增加w可能导致计算开销非线性增长，而性能增益趋于饱和。

**3D记忆生成方法的可替换性。** Table 9展示了将MegaSAM替换为DepthAnything v3的效果：PSNR从13.05提升至13.45，SSIM从0.367提升至0.398，LPIPS从0.381降至0.364。这表明框架对SLAM组件的选择具有鲁棒性，且随着基础模型进步（如更优的深度估计器）可自然获益。Table 10的推理时间对比显示，使用DepthAnything v3将总推理时间从7分18秒降至5分13秒，同时提升性能。

### 定性分析与失败模式

**回访视角的生成对比。** Figure 6展示了关键定性结果：当要求生成器回访输入视频早期视角时，DFoT由于仅能条件化最后几帧，生成的场景结构与原始输入严重不一致（例如墙壁纹理、物体位置错误）。3DScenePrompt则通过空间提示准确重建了原始场景几何，同时允许动态区域（如行人）自然演化。Figure 7进一步对比了多种基线方法：在回访白色墙壁视角时，CameraCtrl、MotionCtrl等方法丢失了场景细节或产生了结构畸变，而3DScenePrompt准确“记忆”了白色墙壁并保持了场景元素的一致性。

**长视频生成的误差累积。** Table 5在DAVIS数据集上评估了长视频生成（多块连续生成）。3DScenePrompt在PSNR（17.28）、SSIM（0.60）和LPIPS（0.35）上均优于基线，但性能相比单块生成有所下降。这表明存在长期漂移问题：随着生成块数增加，空间提示的误差（来自SLAM估计和点云投影）可能逐步累积。论文未提供误差累积的定量分析，这是需要手动验证的潜在弱点。

![[assets/figures/papers/iclr26_0001_3XxoBwMusJ_3D_Scene_Prompting_for_Scene-Consistent_Camera-C/figures/012_Table_5.jpg]]

**动态掩码的失败边界。** 动态掩码质量直接影响生成保真度。当动态物体与背景纹理相似、运动幅度极小或遮挡严重时，三阶段流水线可能无法生成完整的物体级掩码，导致静态点云中残留动态伪影。论文未报告此类失败案例的分布频率，该点需要手动验证。

### 补充图表

![[assets/figures/papers/iclr26_0001_3XxoBwMusJ_3D_Scene_Prompting_for_Scene-Consistent_Camera-C/figures/006_Table_1.jpg]]
*Table 1: Evaluation of spatial and geometric consistency. We compare DFoT and our framework on the RealEstate10K (Zhou et al., 2018) and DynPose-100K (Rockwell et al., 2025) datasets. For spatial consistency, we evaluate PSNR, SSIM, and LPIPS on revisited camera trajectories, while for geometric consistency, we report the MEt3R (Asim et al., 2025) metric*

![[assets/figures/papers/iclr26_0001_3XxoBwMusJ_3D_Scene_Prompting_for_Scene-Consistent_Camera-C/figures/009_Table_3.jpg]]
*Table 3: Evaluation of video generation quality. We assess the quality of generated videos using FVD and VBench++ scores. For FVD, lower values indicate higher video quality. For VBench++ scores, higher values indicate better performance. All VBench++ scores are normalized*

## 方法谱系与知识库定位

### 与基线/后续工作的关系

3DScenePrompt 的核心创新在于将视频生成的条件化策略从单一的时间邻域扩展为双时空邻域，这一设计直接回应了现有方法的核心瓶颈。在方法谱系中，它位于两条技术路线的交汇点：其一是以 DFoT 为代表的“视频到未来视频”生成范式，其二是以 CameraCtrl、MotionCtrl、FloVD、VD3D 为代表的“单帧条件化相机可控生成”范式。DFoT 的瓶颈在于其时间滑动窗口机制（Equation 3: `V_out = G(V_in[L-w:L], T)`）仅能利用输入视频的最后 w 帧，当相机回访早期视角时，这些帧中不包含目标视角的场景信息，导致生成内容与输入视频的场景几何严重不一致。单帧条件化方法则更弱，它们仅以单张参考图像 I_ref 或文本 T 为条件（Equation 2），完全无法利用输入视频中的丰富上下文。

3DScenePrompt 通过引入双滑动窗口策略（Equation 4: `V_out = F(tilde{V}_in, T, C)`, where `tilde{V}_in = {Temporal(w)} ∪ {Spatial(T)}`）打破了这一限制。其核心洞察是：视频中的邻域关系不仅是时间上的，也是空间上的——当相机回访相似视角时，生成帧可能与输入序列中很早的帧在空间上相邻。利用这一双重性质，3DScenePrompt 在标准时间条件化之外，增加了基于 3D 场景记忆的空间条件化。这一记忆（Equation 8: `M = (hat{C}, P_static)`）仅保留从完整输入视频中提取的静态几何结构，通过动态 SLAM（Equation 5: `(hat{C}, P) = D_SLAM(V_in)`）和动态掩码流水线实现。

与并发工作 SPMem 相比，两者概念上相似但实现路径不同：SPMem 使用不同的动态物体处理和条件化架构，且其代码未公开，因此无法进行直接定量比较。与 ReCamMaster、TrajectoryCrafter、Star-Gen 等长程场景一致生成方法相比，3DScenePrompt 的优势在于无需假设静态世界，通过动态掩码显式处理运动物体，从而适用于动态场景。

### 适用边界与条件

3DScenePrompt 的适用性取决于几个关键前提条件。首先，输入视频必须包含足够的相机运动，使得动态 SLAM 能够可靠地估计相机姿态和 3D 结构。在近乎静态的拍摄条件下，SLAM 的退化可能导致空间条件化失效。其次，动态掩码的质量直接影响生成保真度——消融实验表明，不使用动态掩码时 PSNR 下降约 0.8dB，MEt3R 误差显著增加（Table 6）。这意味着在高度动态的场景中，若动态物体占据画面主体且运动模式复杂，三阶段掩码流水线（光流差异检测 → 反向点跟踪聚合 → SAM2 传播）可能无法干净分离静态背景，导致 3D 场景记忆被污染。第三，框架依赖 MegaSAM 或 DepthAnything v3 进行 SLAM 处理，引入了额外的计算开销（推理时间约 5 分钟），这限制了其在实时或低延迟场景中的应用。

### 局限与开放问题

论文明确承认了几个关键局限。最突出的是长期漂移（误差累积）问题：在极长视频生成中，空间条件化虽然缓解了时间窗口的视野限制，但 3D 场景记忆本身是静态快照，无法捕捉场景的长期变化（如光照、季节、物体位移），这可能导致生成内容与输入视频的视觉风格逐渐偏离。此外，与 SPMem 的直接比较因代码未公开而无法进行，这削弱了方法在竞争格局中的定位清晰度。

从开放问题来看，最紧迫的是如何设计专用细化模块来处理时间误差累积，而不是依赖纯数据驱动的扩散模型去隐式补偿。其次，动态掩码质量对生成保真度的具体影响程度尚未被系统量化——现有消融实验仅给出了有无掩码的对比，但不同动态场景复杂度下的性能边界未知。第三，能否将当前组件（如 SLAM 模块、掩码策略）替换为更先进的模型以进一步提升性能？论文已初步探索了将 MegaSAM 替换为 DepthAnything v3 的效果（Table 9），但这只是单一维度替换，更系统的组件级搜索可能带来更大收益。最后，3DScenePrompt 的架构设计（零填充槽注入条件化）使其无需修改模型架构，这一特性是否意味着它可以作为通用插件集成到其他视频扩散模型中，是一个值得探索的方向。

## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/3D_Scene_Prompting_for_Scene_Consistent_Camera_Controllable_Video_Generation.pdf

![[paperPDFs/ICLR_2026/3D_Scene_Prompting_for_Scene_Consistent_Camera_Controllable_Video_Generation.pdf]]
