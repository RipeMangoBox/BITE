---
title: "VLM-3R: Vision-Language Models Augmented with Instruction-Aligned 3D Reconstruction"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/VLM_3R_Vision_Language_Models_Augmented_with_Instruction_Aligned_3D_Reconstruction.pdf
project_link: "https://vlm-3r.github.io/"
code_link: "https://github.com/assimp/assimp"
aliases:
- V3
- VLM-3R
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 通过引入基于CUT3R的度量级三维几何编码器，从单目视频中隐式提取空间令牌（场景几何）和视图令牌（相机运动），并通过Spatial-Visual-View Fusion将这些三维信息注入视觉语言模型。
primary_logic: 将三维重建与指令调优相结合，利用隐式三维令牌将几何和相机运动先验无缝集成到VLM中，使模型在无显式3D输入的情况下获得鲁棒的度量级空间理解和时序推理能力。
claims:
- VLM-3R在VSI-Bench排行榜上位列开源模型第一（Rank Avg 60.9），显著优于微调后的LLaVA-NeXT-Video-7B（57.7）和其他基线。
- 消融实验显示，移除空间令牌（overall 59.46）或视图令牌（50.09）均导致VSI-Bench总体性能明显下降，证明几何和相机运动信息的关键作用。
- 在VSTemporalI-Bench时序推理基准上，VLM-3R取得领先性能，验证了其对相机运动、物体相对位置等时空关系的有效建模。
- VSI-Bench 整体 上 Rank Average = 60.9
---

# VLM-3R: Vision-Language Models Augmented with Instruction-Aligned 3D Reconstruction

> [!tip] 核心洞察
> 将三维重建与指令调优相结合，利用隐式三维令牌将几何和相机运动先验无缝集成到VLM中，使模型在无显式3D输入的情况下获得鲁棒的度量级空间理解和时序推理能力。

| 字段 | 内容 |
|------|------|
| 中文题名 | VLM-3R：融合指令对齐三维重建的视觉语言模型 |
| 英文题名 | VLM-3R: Vision-Language Models Augmented with Instruction-Aligned 3D Reconstruction |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2505.20279) · [Project](https://vlm-3r.github.io/) · [Code](https://github.com/assimp/assimp) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | VLM-3R |
| Dataset | VSI-Bench 整体, VSI-Bench Absolute Distance, VSI-Bench Room Size, VSI-Bench Relative Direction |

> [!tip] 效果简介
> - VSI-Bench 整体 上，Rank Average 60.9 vs 57.7 (LLaVA-NeXT-Video ft) (+3.2)。
> - VSI-Bench Absolute Distance 上，Accuracy 49.4 vs 20.2 (LLaVA-OneVision-7B) (+29.2)。
> - VSI-Bench Room Size 上，Accuracy 67.1 vs 12.3 (LLaVA-OneVision-7B) (+54.8)。

## 概要

### 核心问题

现有视觉语言模型（VLM）在三维空间推理任务上存在系统性缺陷：它们要么依赖外部深度传感器或预建3D地图，要么缺乏从单目视频中直接恢复度量级三维结构和时序变化的能力。这导致模型在距离估计、空间关系理解等基础任务上表现不佳，严重制约了VLM在具身智能、空间辅助等场景中的应用潜力。

### 核心方法

**VLM-3R** 提出了一种端到端的解决方案，其核心思路是将三维重建与指令调优深度融合。具体而言，该方法引入基于CUT3R的度量级三维几何编码器，从单目视频中隐式提取两类关键信息：**空间令牌**（场景几何）和**视图令牌**（相机运动）。通过设计的Spatial-Visual-View Fusion模块，以交叉注意力机制将三维几何先验无缝注入视觉语言模型的二维语义令牌中，使模型在无需显式3D输入的情况下获得鲁棒的度量级空间理解和时序推理能力。

### 关键结论

- **开源模型领先**：VLM-3R在VSI-Bench排行榜上以Rank Average 60.9位列开源模型第一，显著优于微调后的LLaVA-NeXT-Video-7B（57.7）及其他基线模型（Table 1）。
- **度量级空间感知突破**：在Absolute Distance任务上达到49.4%（基线仅20.2%），在Room Size任务上达到67.1%（基线仅12.3%），验证了度量级几何编码的关键作用。
- **时序推理能力验证**：在提出的VSTemporalI-Bench时序推理基准上取得68.6%的领先性能，证明模型对相机运动、物体相对位置等时空关系的有效建模。
- **消融实验确认**：移除空间令牌或视图令牌均导致性能显著下降（分别降至59.46和50.09），证实几何和相机运动信息各自不可替代的贡献（Table 6）。

### 方法谱系与知识库定位

VLM-3R属于**视频视觉语言模型 + 隐式三维几何注入**技术路线。与依赖显式3D输入的方法（如Spatial-MLLM、VG-LLM）不同，VLM-3R直接从单目视频中恢复度量级三维结构；与使用归一化深度估计的模型（如基于VGGT的方案）相比，CUT3R提供的度量尺度和时序建模能力是实现绝对距离、房间尺寸等任务突破的关键。在知识库定位上，该方法填补了“单目视频→度量级空间理解”的能力空白，为后续具身导航、空间对话等应用提供了可扩展的基座。

### 视觉语言模型的空间推理瓶颈

视觉语言模型（VLM）在图像描述、视频问答等任务上取得了显著进展，但在涉及三维空间理解时仍面临根本性挑战。现有VLM主要从二维视觉信号中学习，缺乏对场景深度、物体间度量距离和相机运动等三维结构信息的直接感知能力。这导致模型在回答“物体A距离相机多远？”“房间面积多大？”等需要绝对尺度估计的问题时，性能急剧下降。

当前解决这一瓶颈的途径主要分为两类。一类方法依赖外部深度传感器或预构建的三维地图作为显式输入，如**Spatial-MLLM**等基于多视图几何变换器的空间VLM。这类方法的局限性在于：它们需要额外的硬件支持或预先完成场景重建，无法从单目视频流中端到端地进行空间推理。另一类方法尝试通过归一化深度估计模型（如VGGT）为VLM补充深度信息，但这些模型通常输出尺度模糊的相对深度，无法提供度量级的三维几何约束，也难以有效建模跨帧的相机运动和时序变化。

### 从单目视频中恢复度量级三维结构的需求

真实世界的空间理解任务——例如室内导航、物体定位和距离估计——要求模型具备从单目视频中恢复度量级三维结构的能力。单目视频是成本最低、最易获取的视觉数据形式，但从中推断绝对尺度、相机位姿和场景几何是一个本质上欠约束的问题。现有视频VLM（如**LLaVA-NeXT-Video**、**LLaVA-OneVision**）仅使用二维视觉编码器提取帧级语义特征，完全忽略了帧间几何对应关系和相机运动信息，因此在VSI-Bench等空间推理基准上表现不佳：例如LLaVA-OneVision-7B在绝对距离估计任务上准确率仅为20.2%，在房间大小估计上仅为12.3%。

### 本文动机：融合三维重建与指令调优

针对上述缺口，本文提出VLM-3R，核心动机是将度量级三维重建能力与视觉语言模型的指令调优范式深度融合。具体而言，VLM-3R引入基于**CUT3R**的几何编码器，从单目视频中隐式提取两类三维令牌——表示场景几何的**空间令牌**和编码相机运动的**视图令牌**——并通过设计的Spatial-Visual-View Fusion模块将其注入VLM的视觉表示中。这一设计使模型无需显式三维输入即可获得鲁棒的度量级空间理解和时序推理能力，在VSI-Bench上以Rank Average 60.9位列开源模型第一，并在新提出的VSTemporalI-Bench时序推理基准上取得领先性能。

## 核心方法与创新机理

VLM-3R的核心创新在于将**度量级三维重建**与**视觉语言模型的指令调优**深度融合，使模型能够从单目视频中直接恢复隐式三维结构并注入空间推理过程，而无需依赖外部深度传感器或预建3D地图。这一设计通过三个关键模块的协同变革实现。

### 从归一化深度到度量级隐式三维令牌

现有空间VLM通常依赖归一化深度估计模型（如VGGT），其输出缺乏绝对尺度信息，导致模型在距离估计、房间尺寸判断等需要度量理解的任务上表现薄弱。VLM-3R引入**CUT3R**作为几何编码器，从单目视频序列中提取两类隐式三维令牌：

- **空间令牌（Spatial Tokens）**：编码全局对齐的度量级场景几何结构，使模型理解物体的绝对位置与空间布局。
- **视图令牌（View Tokens）**：编码相机运动轨迹与姿态变化，为时序推理提供相机动态先验。

CUT3R的tokenization过程可形式化为：

$$F_t = f_{\mathrm{enc}}(I_t), \quad [z_t', F_t'], s_t = f_{\mathrm{dec}}([z, F_t], s_{t-1})$$

其中图像编码器$f_{\mathrm{enc}}$提取帧特征，解码器$f_{\mathrm{dec}}$通过隐状态$s_{t-1}$的循环更新，输出相机视图令牌$z_t'$和空间令牌$F_t'$。这一设计的关键优势在于：CUT3R输出的是**度量尺度**的点云与位姿估计，而非归一化坐标，使下游VLM具备了绝对距离感知能力。

### 从2D-2D特征融合到Spatial-Visual-View交叉注意力融合

传统视频VLM（如LLaVA-NeXT-Video）仅将2D视觉令牌直接送入LLM，缺乏三维几何信息的注入通道。VLM-3R设计了**Spatial-Visual-View Fusion**模块，通过交叉注意力机制将三维令牌与二维视觉令牌深度融合：

$$H_{\mathrm{attn}} = \mathrm{softmax}\left( \frac{(H_v W_Q)(Z_{3D} W_K)^T}{\sqrt{d_k}} \right)(Z_{3D} W_V)$$

$$H_v' = H_v + H_{\mathrm{attn}}$$

该设计以视觉令牌$H_v$为查询（Query），三维令牌$Z_{3D}$为键（Key）和值（Value），通过缩放点积注意力实现2D-3D跨模态交互。残差连接$H_v + H_{\mathrm{attn}}$确保外观语义与几何先验的互补保留，避免三维信息的注入淹没原始视觉特征。消融实验证实，将此交叉注意力替换为2D-2D融合会导致VSI-Bench整体评分从60.90降至58.12（Table 6），验证了三维几何信息注入的必要性。

### 从手工标注到大规模自动重建指令数据

空间推理数据的稀缺是制约VLM空间能力的关键瓶颈。VLM-3R构建了一套高度自动化的数据管线，从现有三维数据集中的视频或多视图图像出发，利用模拟器辅助生成**超过200K的多样化空间推理QA对**，覆盖七种空间任务类型（如绝对距离、房间尺寸、相对方向等）以及具身路径规划任务。这一数据生成策略使模型在VSI-Bench的绝对距离任务上实现从20.2%到49.4%的飞跃（Table 1），房间尺寸任务从12.3%提升至67.1%，充分证明了重建指令调优的有效性。

### 创新点的因果机制总结

上述三个changed slots形成了一条清晰的因果链：**度量级几何编码器**提供了尺度感知的三维表征基础；**交叉注意力融合模块**将这些表征无损注入VLM的推理流；**大规模重建指令数据**则确保模型充分学习如何利用这些几何先验回答空间问题。三者的协同使VLM-3R在无显式3D输入的条件下，获得了鲁棒的度量级空间理解与相机动态推理能力，在VSI-Bench上以Rank Avg 60.9位列开源模型第一（Table 1）。

VLM-3R 的核心设计理念是将度量级三维重建能力以隐式令牌的形式无缝注入视觉语言模型，使模型能够从单目视频中直接恢复空间结构与相机运动，而无需依赖深度传感器或预建 3D 地图。整体架构遵循“双流编码—交叉融合—联合推理”的端到端范式，如 Figure 3 所示。

![[assets/figures/papers/paper_list_l2429_https_arxiv_org_abs_2505_20279/figures/003_Figure_3.jpg]]
*Figure 3: Network Architecture. VLM-3R takes monocular video and language instructions as input. A vision encoder and metricscale geometry encoder extract frame-level appearance, camera-view pose, and globally aligned 3D structure. Spatial-Visual-View Fusion applies 2D-3D attention and a layer projector to inject spatial tokens and view tokens into the VLM. At inference time, the model uses these fused representations to support reliable spatial and temporal reasoning from monocular video, without requiring depth sensors or pre-built 3D maps*

**输入输出流**：系统以单目视频序列和自然语言指令作为输入，输出为空间推理答案或路径规划决策。视频帧同时进入两条并行的编码支路：视觉编码器提取逐帧的二维语义令牌，几何编码器则生成度量级的三维空间令牌与相机视图令牌。

**核心模块关系**：

1. **Vision Encoder**：对每一帧 RGB 图像独立提取语义视觉令牌 $H_v$，保留外观信息。该编码器在训练期间保持冻结。

2. **Geometry Encoder (CUT3R)**：作为度量级三维重建的核心组件，CUT3R 从视频序列中隐式恢复全局对齐的 3D 结构。其工作流程遵循递推式令牌化机制：
   $$F_t = f_{\mathrm{enc}}(I_t), \quad [z_t', F_t'], s_t = f_{\mathrm{dec}}([z, F_t], s_{t-1})$$
   其中 $f_{\mathrm{enc}}$ 对第 $t$ 帧提取特征，$f_{\mathrm{dec}}$ 基于可学习的隐状态 $s_{t-1}$ 更新并输出相机视图令牌 $z_t'$（编码相机运动）和空间令牌 $F_t'$（编码场景几何）。与归一化深度估计方法不同，CUT3R 直接输出度量尺度的点云和位姿估计，这是实现绝对距离、房间尺寸等度量级空间推理的前提。

3. **Spatial-Visual-View Fusion**：这是连接三维几何与二维语义的关键模块。融合以视觉令牌 $H_v$ 为查询（Query），以三维令牌 $Z_{3D}$ 为键（Key）和值（Value），通过缩放点积注意力实现 2D-3D 跨模态交互：
   $$H_{\mathrm{attn}} = \mathrm{softmax}\left( \frac{(H_v W_Q)(Z_{3D} W_K)^T}{\sqrt{d_k}} \right)(Z_{3D} W_V)$$
   随后通过残差连接将几何先验加回原始视觉令牌：
   $$H_v' = H_v + H_{\mathrm{attn}}$$
   这一设计既保留了视觉语义的完整性，又使每个视觉令牌能够“关注”到与其空间位置相关的三维结构信息和相机运动信息。

4. **MLP Projector**：将融合后的特征 $H_v'$ 投影到与 LLM 输入空间对齐的维度。

5. **LLM Backbone**：接收融合后的视觉令牌与语言指令令牌，执行联合空间-语言推理。论文采用 LLaVA-Video-7B 作为基础 VLM，通过 LoRA（rank 128, scale 256）进行高效微调，仅更新融合注意力块和投影层参数，视觉编码器和几何编码器均保持冻结。

**关键设计决策**：消融实验（Table 6）表明，空间令牌和视图令牌各自承担不可替代的角色——移除空间令牌导致整体性能从 60.90 降至 59.46，而移除视图令牌则骤降至 50.09，证明场景几何与相机运动信息对于空间推理是互补且必需的。此外，2D-3D 交叉注意力融合（60.90）显著优于 2D-2D 融合（58.12）和显式点云融合（57.87），验证了隐式令牌级注入三维几何信息的有效性。

![[assets/figures/papers/paper_list_l2429_https_arxiv_org_abs_2505_20279/figures/001_Figure_1.jpg]]
*Figure 1: VLM-3R: 3D Spatial-Temporal Reasoning from Monocular Video. Unlike prior video LMMs and 3D-LLMs (a) that depend on explicit 3D inputs such as depth sensors or pre-built 3D maps, VLM-3R (b) uses an end-to-end architecture with metric-scale spatial encoders that fuse scene and camera tokens to recover implicit 3D structure directly from monocular video. This design targets spatial assistance from raw camera streams and supports detailed reasoning about spatial context, instance layout, and temporal dynamics, leading to consistently stronger performance on VSI-Bench and the proposed VSTemporalI-Bench (c)*

### 整体架构

VLM-3R 的核心设计思想是将度量级三维重建与视觉语言指令调优深度融合。如图 Figure 3 所示，系统由四个关键模块串联构成：视觉编码器、几何编码器、Spatial-Visual-View Fusion 融合模块，以及 LLM 主干网络。单目视频帧分别进入视觉编码器提取语义令牌，进入几何编码器提取隐式三维令牌，随后通过交叉注意力将几何先验注入视觉特征，最终由投影层对齐维度后送入 LLM 进行联合空间-语言推理。

### 三维重建令牌化

几何编码器采用预训练的 **CUT3R** 模型（Section 4.1），其关键特性是输出**度量尺度**的点云图和相机位姿估计，而非归一化尺度。CUT3R 以逐帧流式方式处理视频序列，图像编码器提取帧级特征，解码器维护隐状态并迭代更新：

$$F_t = f_{\mathrm{enc}}(I_t), \quad [z_t', F_t'], s_t = f_{\mathrm{dec}}([z, F_t], s_{t-1})$$

其中 $I_t$ 为第 $t$ 帧输入图像，$f_{\mathrm{enc}}$ 为图像编码器，$F_t$ 为提取的特征；$s_{t-1}$ 为上一时刻的隐状态，$f_{\mathrm{dec}}$ 为解码器，输出当前帧的**视图令牌** $z_t'$（编码相机运动信息）和更新后的**空间令牌** $F_t'$（编码全局对齐的场景几何结构）。这一流式机制使模型能够从单目视频中隐式恢复三维场景结构和相机运动轨迹，无需显式深度传感器或预建三维地图。

### Spatial-Visual-View Fusion

这是将三维几何先验注入视觉语言模型的核心融合模块。设 $H_v$ 为视觉编码器输出的二维语义令牌，$Z_{3D}$ 为几何编码器生成的三维令牌集合（包含空间令牌和视图令牌）。融合过程以视觉令牌为查询、三维令牌为键和值，通过缩放点积注意力实现跨模态交互：

$$H_{\mathrm{attn}} = \mathrm{softmax}\left( \frac{(H_v W_Q)(Z_{3D} W_K)^T}{\sqrt{d_k}} \right)(Z_{3D} W_V)$$

其中 $W_Q$、$W_K$、$W_V$ 分别为查询、键、值的可学习投影矩阵，$d_k$ 为键向量的维度。注意力输出 $H_{\mathrm{attn}}$ 以残差形式加回原始视觉令牌：

$$H_v' = H_v + H_{\mathrm{attn}}$$

残差连接的设计意图是保留原始外观语义信息的同时，注入场景几何和相机运动的隐式先验。融合后的令牌 $H_v'$ 经 MLP 投影层对齐到 LLM 的输入空间，最终与语言指令令牌拼接送入 LLM 主干进行推理。

### 消融验证的关键发现

Table 6 的消融实验揭示了各模块的因果作用：移除空间令牌使 VSI-Bench 整体评分从 60.90 降至 59.46，表明场景几何信息对结构理解任务至关重要；移除视图令牌导致评分骤降至 50.09，证明相机运动信息对方向相关任务不可或缺；用 2D-2D 融合替代 3D-2D 交叉注意力使评分降至 58.12，验证了注入三维几何信息的必要性；显式融合点云（57.87）低于令牌级融合（60.90），表明隐式令牌融合更为稳定。Table D 进一步显示，CUT3R（60.9%）显著优于归一化尺度的 VGGT（58.1%），证实度量尺度和时序建模是空间推理能力的关键瓶颈。

## 实验与关键发现

### 空间推理主结果

VLM-3R在VSI-Bench的八项空间推理任务上取得开源模型第一（Rank Avg 60.9），显著超越微调后的LLaVA-NeXT-Video-7B（57.7）及同期其他空间VLM。该结果来自Table 1的联合排名，所有微调模型均在相同的20万条空间推理QA对上训练，LoRA配置（rank 128, alpha 256）保持一致，视觉编码器与几何编码器冻结，仅更新融合块和投影层，确保比较公平。

度量级空间感知的提升在绝对距离和房间尺寸两项任务上尤为突出。Absolute Distance从LLaVA-OneVision-7B的20.2跃升至49.4（+29.2）；Room Size从12.3提升至67.1（+54.8）。这两项任务要求模型从单目视频中恢复真实世界的物理尺度，正是VLM-3R通过CUT3R几何编码器注入度量级三维先验的直接收益。Relative Direction同样大幅领先（80.5 vs 42.4，+38.1），表明相机运动信息的融合有效支撑了方向判别。

与商用模型相比，VLM-3R在多项任务上接近或超越GPT-4o和Gemini-2.5 Pro，但需注意商用模型的输入模态和训练数据规模不可比，此处仅作参考。

### 时序推理主结果

VLM-3R在VSTemporalI-Bench上取得领先性能（Overall Accuracy 68.6），较LLaVA-NeXT-Video-7B基线（40.0）提升28.6个百分点（Table 2）。该基准包含约13.86万条QA对，覆盖Camera Dynamics（49.6%）、Camera–Object Interactions（38.4%）和Object Relative Position（12.0%）三大类时序空间任务（Figure 2）。VLM-3R的显著优势表明，隐式视图令牌成功编码了相机运动信息，而空间令牌则提供了场景几何的一致性约束，二者协同使模型能够理解“相机如何运动”以及“物体间的相对位置如何随时间变化”。

![[assets/figures/papers/paper_list_l2429_https_arxiv_org_abs_2505_20279/figures/007_Table_2.jpg]]
*Table 2: Evaluations on VSTemporalI-Bench. VLM-3R achieves leading performance, demonstrating strong spatiotemporal reasoning and robust understanding of camera dynamics*

![[assets/figures/papers/paper_list_l2429_https_arxiv_org_abs_2505_20279/figures/002_Figure_2.jpg]]
*Figure 2: VSTemporalI-Bench Overview. It contains 138.6K QA samples across multiple spatio-temporal question types. (a) Statistical distribution of QA pairs by primary categories (inner ring, detailed in the legend) and their sub-categories (outer ring). (b) Example QA pairs illustrating different task types within a benchmark scene*

### 消融实验

Table 6的系统消融揭示了各组件的因果贡献：

- **移除空间令牌**（w/o Spatial Token）：VSI-Bench整体评分从60.90降至59.46。场景几何信息的缺失主要影响结构理解类任务，如房间尺寸和物体布局。
- **移除视图令牌**（w/o View Token）：整体评分骤降至50.09。相机运动信息的缺失对方向判别和时序推理造成灾难性影响，证明视图令牌是时空理解的关键瓶颈。
- **2D-2D融合替代方案**：将3D-2D交叉注意力替换为2D-2D融合，整体评分降至58.12。这表明直接将三维几何信息注入视觉令牌的注意力机制是不可替代的，简单的2D特征混合无法传递度量级空间先验。
- **显式点云融合**（Explicit Points Fusion）：整体评分57.87，低于隐式令牌融合的60.90。显式点云需要额外的投影和对齐步骤，可能引入噪声和不稳定性，而隐式令牌融合在特征空间中端到端地传递几何信息，效果更优。
- **几何编码器选择**（Table D）：CUT3R（60.9%）优于VGGT（58.1%）。VGGT输出归一化尺度，缺乏度量级信息和时序建模能力，CUT3R的度量尺度和时序重建特性是性能优势的根本原因。

### 泛化能力分析

**跨基准泛化**：VLM-3R在ScanQA和SQA3D等传统3D问答基准上同样表现优异（Table 3），尽管其训练数据来自单目视频而非3D扫描输入。在OST-Bench的具身探索场景中（Table 7），VLM-3R在所有类别上一致超越其基座模型LLaVA-Video-7B，尤其在Agent State、Agent–Object Spatial Relationship和Estimation任务上提升显著。这证明从静态室内场景中学到的隐式三维表征具有一定的跨域迁移能力。

**通用能力保持**：Table 4显示，VLM-3R在提升空间感知精度的同时，保持了较强的视频级和图像级通用理解能力。但Table 5的数据混合消融揭示了领域偏移问题：仅使用VSI-Bench领域数据训练（VSI-only）时，Video-MME性能从基座模型的水平降至59.9%；混合3万条LLaVA-Video通用视频样本后（VSI + LLaVA），Video-MME恢复至62.1%。这表明空间推理数据与通用视频数据之间存在分布差异，数据混合策略是缓解灾难性遗忘的有效手段，但通用能力的细微退化依然存在——如Table E中OpenEQA非空间问题从67.22降至65.54。

### 失败模式与局限

1. **Object Size任务提升有限**：VLM-3R在Object Size上为69.15，略低于微调后LLaVA-NeXT-Video的70.82（Table 1）。该任务要求精确估计单个物体的物理尺寸，对单目三维重建的精度要求极高，当前CUT3R的度量级估计在该粒度上仍有不足。

![[assets/figures/papers/paper_list_l2429_https_arxiv_org_abs_2505_20279/figures/004_Table_1.jpg]]
*Table 1: Evaluations on VSI-Bench. Open-source models, including finetuned variants, are jointly ranked by Avg. Models marked with (Finetuned) are further trained using our 200K spatial reasoning QA pairs. VLM-3R ranks first among open-source VLMs, demonstrating the effectiveness of its reconstructive instruction tuning. Within the combined open-source block, dark gray marks the best score and light gray marks the second best. Tied Avg values share the same rank*

2. **动态场景未覆盖**：模型训练和评估均基于静态三维场景，对包含动态物体、交互和遮挡的真实世界视频的空间推理能力尚未验证。

3. **通用能力的细微退化**：即使在混合训练策略下，非空间任务仍存在小幅性能下降。如何自动平衡空间数据与通用数据的混合比例以最小化此损失，仍是开放问题。

4. **对度量级几何编码器的依赖**：消融实验表明CUT3R的度量尺度至关重要，但这也意味着模型性能受限于几何编码器的精度和泛化能力。在纹理稀疏、光照极端或大规模室外场景中，CUT3R的重建质量可能下降，进而影响推理结果。

### 关键实验结论

VLM-3R的实验结果验证了核心假设：将度量级三维重建与指令调优相结合，通过隐式空间令牌和视图令牌将几何与相机运动先验注入VLM，能够在无显式3D输入的情况下获得鲁棒的度量级空间理解和时序推理能力。消融实验证实空间令牌和视图令牌各自承担不可替代的角色——前者支撑场景结构理解，后者支撑相机运动感知——二者的协同通过3D-2D交叉注意力实现，是性能提升的因果瓶颈。

![[assets/figures/papers/paper_list_l2429_https_arxiv_org_abs_2505_20279/figures/010_Table_6.jpg]]
*Table 6: Ablation on VLM-3R components and fusion strategies. We report only overall performance (Avg.) on VSI-Bench. Removing spatial or view tokens slightly reduces performance, while full 2D–3D fusion yields the best overall result*

## 定位与知识库关联

### 一、方法在空间推理VLM谱系中的位置

VLM-3R处于**单目视频空间推理VLM**这一新兴交叉领域，其核心贡献在于首次将度量级隐式三维重建无缝融入视觉语言模型的指令调优流程。

#### 1.1 与纯视觉VLM的关系

传统视频VLM（如**LLaVA-NeXT-Video**、**LLaVA-OneVision**、**Qwen2.5-VL**、**ViLA-1.5**）仅依赖2D视觉编码器提取语义令牌，缺乏对三维几何结构的显式建模。VLM-3R在这些模型基础上引入了一个**并行的几何编码器分支**（CUT3R），在不改变视觉编码器结构的前提下注入度量级空间先验。实验表明，微调后的LLaVA-NeXT-Video-7B在VSI-Bench上仅达57.7（Rank Avg），而VLM-3R以相同LLM主干达到60.9，差距显著（Table 1）。

#### 1.2 与显式3D输入VLM的关系

**Spatial-MLLM**和**VG-LLM**等方法通过多视图几何变换器或显式视觉几何特征注入空间信息，但它们通常依赖：
- 预建3D地图或深度传感器
- 多视图图像作为输入
- 归一化尺度而非度量尺度

VLM-3R的关键突破在于**从单目视频中直接恢复度量级三维结构**，无需任何外部深度传感器或预建地图。这一能力源于CUT3R的度量级点图估计和全局对齐机制，使其在Absolute Distance（49.4 vs 20.2）和Room Size（67.1 vs 12.3）等需要绝对尺度的任务上远超基线（Table 1）。

#### 1.3 与商用模型的对比定位

在VSI-Bench开源模型排名中，VLM-3R以60.9的Rank Avg位列第一，显著优于微调后的LLaVA-NeXT-Video（57.7）。虽然商用模型如**Gemini-2.5 Pro**和**GPT-4o**仍保持领先，但VLM-3R在Relative Direction（80.5）等子任务上已接近商用模型水平，证明其空间推理能力的有效性（Table 1）。

### 二、核心设计选择的谱系分析

#### 2.1 几何编码器选择：CUT3R vs VGGT

消融实验（Table D）对比了两种几何编码器：
- **VGGT**：归一化尺度深度估计，缺乏时序建模能力
- **CUT3R**：度量级多视图重建，具备时序状态传播

CUT3R以60.9% vs 58.1%的整体优势胜出，验证了**度量尺度和时序建模**对空间推理的关键作用。CUT3R的循环解码器设计（$s_t = f_{\mathrm{dec}}([z, F_t], s_{t-1})$）使其能够利用视频帧间的时序连续性，这是VGGT等单帧估计方法所不具备的。

#### 2.2 融合策略：令牌级隐式融合 vs 显式点云注入

VLM-3R的Spatial-Visual-View Fusion采用**交叉注意力机制**将3D令牌与2D视觉令牌融合：

$$H_{\mathrm{attn}} = \mathrm{softmax}\left( \frac{(H_v W_Q)(Z_{3D} W_K)^T}{\sqrt{d_k}} \right)(Z_{3D} W_V)$$

$$H_v' = H_v + H_{\mathrm{attn}}$$

消融实验（Table 6）揭示了融合策略的优劣层次：
- **全令牌融合（60.90）** > 移除空间令牌（59.46） > 2D-2D融合替代（58.12） > 显式点云融合（57.87） > 移除视图令牌（50.09）

这一结果揭示了两个关键洞察：
1. **视图令牌（相机运动信息）的贡献远大于空间令牌（场景几何）**：移除视图令牌导致性能骤降10.81点，说明方向相关任务（如Relative Direction）对相机运动先验高度敏感
2. **隐式令牌融合优于显式点云注入**：显式点云融合（57.87）低于令牌级融合（60.90），表明中间层交叉注意力能更有效地对齐2D语义与3D几何特征空间

#### 2.3 训练数据策略：领域特化 vs 混合训练

VLM-3R使用超过200K自动生成的空间推理QA对进行训练，涵盖七种空间任务类型（Table A）。与仅使用少量手工标注数据的基线（如VSI-Bench原始微调）相比，大规模自动标注管线是其性能优势的重要来源。

数据混合消融（Table 5）显示：
- **纯VSI数据训练**：Video-MME性能降至59.9%，存在领域偏移
- **混合通用视频数据（VSI + LLaVA-Video 30k）**：Video-MME恢复至62.1%，接近基础模型水平

这表明空间推理能力的增强确实以牺牲部分通用视频理解为代价，但通过数据混合策略可以显著缓解这一退化。

### 三、适用边界与能力外推

#### 3.1 已验证的泛化能力

VLM-3R在以下场景展现了超出训练分布的能力：

1. **时序空间推理**（VSTemporalI-Bench）：尽管训练数据以静态场景为主，模型在相机运动、物体相对位置变化等时序任务上取得68.6%的领先性能（Table 2），证明CUT3R的时序状态传播机制有效捕获了动态空间关系。

2. **具身探索场景**（OST-Bench）：在在线具身探索基准上，VLM-3R在Agent State、Agent-Object Spatial Relationship和Estimation任务上均超越基础模型（Table 7），尽管训练数据仅包含静态室内场景。这暗示隐式三维令牌编码的空间先验具有一定的任务无关性。

3. **3D问答基准**（ScanQA、SQA3D）：在需要3D理解的问答任务上，VLM-3R展现出与专用3D输入模型竞争的性能（Table 3），进一步验证了从单目视频中恢复的三维信息的有效性。

#### 3.2 已知能力边界

1. **动态物体推理未探索**：模型训练和评估主要针对静态三维场景。对于包含移动物体、人物交互的真实世界动态视频，其空间推理能力尚未验证。

2. **部分任务提升有限**：Object Size任务上VLM-3R（69.15）略低于微调基线（70.82）（Table 1），暗示单目三维重建在细粒度物体尺度估计上仍有精度瓶颈。

3. **非空间任务的细微退化**：在OpenEQA的非空间问题上，VLM-3R从基础模型的67.22降至65.54（Table E），表明空间先验的注入对纯语义任务存在轻微干扰。混合训练策略（Table 5）部分缓解但未完全消除这一问题。

4. **极端环境未测试**：当前评估集中在室内场景，对室外、低光照、遮挡严重等极端条件的鲁棒性未知。

### 四、局限性与开放问题

#### 4.1 结构性局限

1. **静态场景偏置**：训练数据来自静态3D数据集，模型未学习动态物体的运动模式和物理交互。扩展到包含动态物体的4D场景需要大规模4D数据集的采集和标注，这是当前领域的共同瓶颈。

2. **重建精度依赖**：CUT3R的度量级重建质量直接影响下游空间推理性能。在纹理稀疏、重复结构或大视角变化场景中，重建误差可能传导至VLM输出。

3. **计算开销**：几何编码器（CUT3R）和交叉注意力融合模块增加了推理时的计算负担，相比纯2D VLM，延迟和显存占用更高。论文未提供详细的推理效率对比。

#### 4.2 开放研究问题

1. **动态场景扩展**：如何将隐式三维令牌的时序建模从相机运动推广到场景内物体的独立运动？这可能需要引入4D重建基础模型或对象级运动分割。

2. **自监督预训练**：当前方法依赖CUT3R的度量尺度估计能力。能否通过自监督预训练（如从大规模无标注视频中学习几何先验）进一步减少对度量重建精度的依赖？

3. **具身任务的下游应用**：隐式令牌融合在机器人导航、操作等具身任务中的有效性尚待验证。这些任务对空间推理的精度和实时性要求更高。

4. **数据混合的自动平衡**：如何自动确定空间推理数据与通用视觉语言数据的最优混合比例，以最小化通用能力的损失？当前30k通用样本的混合量是经验性选择，缺乏理论指导。

5. **多模态几何编码器**：除视觉几何外，是否可融合触觉、音频等模态的空间信息，构建更全面的空间理解？

### 五、知识库定位总结

VLM-3R在空间推理VLM谱系中的定位可概括为：

- **上游依赖**：CUT3R（度量级多视图重建）、LLaVA-Video（视频VLM架构）
- **核心创新**：Spatial-Visual-View Fusion（3D-2D交叉注意力融合）+ 重建指令调优（200K自动生成空间QA）
- **下游能力**：单目视频度量级空间推理、时序空间关系理解、具身场景泛化
- **竞争位置**：开源模型第一（VSI-Bench Rank Avg 60.9），在绝对距离和方向推理任务上显著超越同类方法
- **未解决挑战**：动态物体推理、极端环境鲁棒性、通用能力保持的自动平衡

## 原文 PDF

![[paperPDFs/CVPR_2026/VLM_3R_Vision_Language_Models_Augmented_with_Instruction_Aligned_3D_Reconstruction.pdf]]
