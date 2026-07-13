---
title: "EA3D: Event-Augmented 3D Diffusion for Generalizable Novel View Synthesis"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/EA3D_Event_Augmented_3D_Diffusion_for_Generalizable_Novel_View_Synthesis_bb1d8358dc6f.pdf
project_link: "https://wangpeng000.github.io/BAD-NeRF/"
code_link: "https://github.com/colmap/colmap"
aliases:
- EA3D
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 联合利用异步事件流提供的稠密、抗遮挡几何先验与RGB帧的丰富外观信息。
primary_logic: 事件流蕴含微秒级、抗遮挡的几何结构线索，而RGB帧携带纹理与色彩；通过一个可学习的EA-Renderer将两者融合为视角相关的3D特征，再以此条件驱动视频扩散模型，可在不依赖逐场景优化的情况下生成时空一致的高保真新视角。
claims:
- 在少视图（2-视图）大基线设定下，EA3D的合成质量显著超过仅依赖RGB的可泛化方法ViewCrafter和需要逐场景优化的E-NeRF/Event3DGS。
- 移除事件几何特征后，PSNR在2-视图设置下下降高达4.6 dB，且视图间距越大优势越明显。
- 在真实事件数据(DSEC)上，EA3D无需微调即最优，证明其对真实事件流的泛化能力。
- Tanks-and-Temples (T&T) 上 PSNR↑ / SSIM↑ / LPIPS↓ = 23.50 / 0.756 / 0.218
---

# EA3D: Event-Augmented 3D Diffusion for Generalizable Novel View Synthesis

> [!tip] 核心洞察
> 事件流蕴含微秒级、抗遮挡的几何结构线索，而RGB帧携带纹理与色彩；通过一个可学习的EA-Renderer将两者融合为视角相关的3D特征，再以此条件驱动视频扩散模型，可在不依赖逐场景优化的情况下生成时空一致的高保真新视角。

| 字段 | 内容 |
|------|------|
| 中文题名 | EA3D：事件增强的3D扩散模型用于可泛化的新视角合成 |
| 英文题名 | EA3D: Event-Augmented 3D Diffusion for Generalizable Novel View Synthesis |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=YwawhlWdtm) · [Code](https://github.com/colmap/colmap) · [Project](https://wangpeng000.github.io/BAD-NeRF/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | EA3D |
| Dataset | Tanks-and-Temples, DSEC |

> [!tip] 效果简介
> - Tanks-and-Temples (T&T) 上，PSNR↑ / SSIM↑ / LPIPS↓ 23.50 / 0.756 / 0.218 vs 18.24 / 0.607 / 0.289 (ViewCrafter) (+5.26 / +0.149 / -0.071)。
> - DSEC (真实事件数据) 上，PSNR↑ / SSIM↑ / LPIPS↓ 24.89 / 0.792 / 0.211 vs 18.71 / 0.684 / 0.279 (ViewCrafter) (+6.18 / +0.108 / -0.068)。

## 概要

新视角合成（Novel View Synthesis, NVS）旨在从稀疏输入视图生成任意视角的高保真图像。现有方法面临一对根本性矛盾：**逐场景优化方法**（如E-NeRF、Event3DGS）虽能利用事件相机提供的微秒级几何线索，但需为每个场景重新训练，无法泛化到新环境；**可泛化方法**（如ViewCrafter、NVS-Solver）仅依赖稀疏RGB帧，在快速相机运动或大基线场景下因几何信息严重不足而产生结构崩塌与伪影。

**核心瓶颈**在于：快速运动下，RGB帧稀疏且易受运动模糊影响，难以捕获可靠的几何结构；而事件流虽蕴含稠密、抗遮挡的几何先验，却缺乏纹理与色彩信息。两类信号的优势互补长期未被有效融合。

**EA3D** 针对此瓶颈提出“事件增强的3D扩散”范式。其核心洞察是：事件流提供与视角无关的几何结构线索，RGB帧携带视角相关的纹理外观；通过一个可学习的 **EA-Renderer** 将两者融合为视角相关的3D条件特征，再以此驱动视频扩散模型生成时空一致的新视角序列。该方法无需逐场景优化，实现了可泛化的高保真新视角合成。

**关键实证结论**：
- 在Tanks-and-Temples基准的2视图大基线设定下，EA3D的PSNR达到23.50 dB，较仅RGB的可泛化方法ViewCrafter（18.24 dB）提升 **+5.26 dB**（Table 1）。
- 在真实事件数据DSEC上，EA3D同样以24.89 dB的PSNR显著超越ViewCrafter的18.71 dB（Table 2），验证了对真实事件流的泛化能力。
- 消融实验表明，移除事件几何特征后PSNR下降高达4.6 dB，且视图间距越大优势越显著（Table 3, Figure 5），直接证实事件几何先验是大基线场景下性能提升的关键因果因素。

**方法定位**：EA3D处于“事件增强的可泛化NVS”这一新兴交叉点。与基于优化的方法（E-NeRF, Event3DGS）相比，它舍弃了逐场景训练，以一次前向推理完成合成（推理时间约0.03小时，对比优化方法的数小时，Table 4）；与仅RGB的可泛化方法（ViewCrafter, NVS-Solver）相比，它通过联合事件几何特征显著提升了结构完整性和抗遮挡能力。在方法谱系上，EA3D可视为将事件相机的几何感知优势引入视频扩散模型的一次成功尝试，为事件驱动的3D生成任务开辟了可泛化路径。

**局限与开放问题**：当前EA3D的训练依赖合成事件模拟器（vid2e），对真实事件噪声与传感器退化的鲁棒性仍需更全面验证；骨干视频扩散模型（CogVideoX）固定了最大分辨率与序列长度，尚不支持自适应推理；推理显存消耗约28 GB（A100），部署到边缘设备面临挑战。此外，在强动态场景（非刚性运动、显著光照突变）下的事件-外观融合可靠性，以及通过模型蒸馏实现实时推理的可行性，仍是值得探索的开放问题。



新视角合成（Novel View Synthesis, NVS）旨在从稀疏的输入视图中重建任意相机位姿下的高保真图像，是三维视觉与图形学中的核心问题。近年来，以NeRF（Mildenhall et al., ECCV 2020）和3D高斯泼溅（3DGS, Kerbl et al., SIGGRAPH 2023）为代表的逐场景优化方法取得了令人瞩目的渲染质量，但其根本局限在于：**每遇到一个新场景，都需要从零开始执行耗时的梯度优化**，无法实现跨场景的即时泛化。

更关键的是，现有可泛化方法（如ViewCrafter、NVS-Solver）仅依赖稀疏的RGB帧作为输入。在快速相机运动或大基线场景下，这一范式暴露出一个**结构性瓶颈**：稀疏RGB帧提供的几何信息极为有限——视图间的大幅位移导致严重的遮挡与透视畸变，仅凭RGB投影或深度warp难以恢复完整的场景几何。这使得生成结果常出现结构坍塌、纹理模糊和时序不一致等严重伪影。

事件相机（Event Camera）的兴起为突破上述瓶颈提供了新的可能。与同步曝光的传统RGB相机不同，事件相机以微秒级时间分辨率异步记录像素级的亮度变化，生成稠密的事件流。这一信号具有两个关键特性：（1）**抗遮挡的几何先验**——事件流在快速运动中仍能持续捕获边缘与轮廓结构，不受运动模糊影响；（2）**时序稠密性**——在极短的时间窗口内即可积累丰富的空间结构线索。然而，事件流本身不携带绝对亮度与色彩信息，无法独立完成纹理重建。

本文的核心动机在于：**能否将事件流的稠密几何先验与RGB帧的丰富外观信息进行深度融合，从而在不依赖逐场景优化的前提下，实现可泛化的高保真新视角合成？** 这一问题的挑战在于：事件流是无姿态的异步信号，而RGB帧是带位姿的同步信号，两者的模态鸿沟与时空对齐问题需要在统一的框架中得到解决。EA3D正是围绕这一核心矛盾展开设计，通过可学习的EA-Renderer和3D-aware视频扩散模型，首次实现了事件增强的可泛化新视角合成。



## 核心方法与创新机理

EA3D的核心创新在于**将事件相机与RGB帧的互补优势系统性地注入到可泛化的新视角合成管线中**，从而突破“稀疏RGB帧在快速运动下几何信息匮乏”与“逐场景优化方法无法泛化”的双重瓶颈。与现有基线相比，EA3D在三个关键维度上实现了结构性改变。

### 几何信息来源：从稀疏投影到稠密抗遮挡的事件几何

仅依赖RGB帧的可泛化方法（如**ViewCrafter**（Yu et al., 2025c）和**NVS-Solver**（You et al., 2025））通过深度warp或点投影获取稀疏几何线索，在快速运动和大基线场景下极易产生遮挡、失真和几何退化。逐场景优化方法（如**E-NeRF**（Klenk et al., 2023）和**Event3DGS**（Han et al., 2024））虽可利用事件流，但需为每个场景从头优化，缺乏泛化能力。

EA3D首次在可泛化框架中引入事件流作为几何先验来源。事件相机以微秒级时间分辨率异步记录亮度变化，天然具备抗运动模糊和抗遮挡的特性。EA3D通过**自适应事件切片策略**将连续事件流转化为长短时融合的体素网格，再经由3D卷积编码器提取紧凑的几何特征 $\mathbf{F}_{\mathrm{event}}$（Equation 2）。如Figure 8所示，这些特征图清晰地揭示了物体边缘和轮廓等结构信息，证明事件编码器成功捕获了场景的几何细节。

消融实验（Table 3 “w/o Geometry Feature”）提供了决定性证据：移除事件几何特征后，在2视图设定下PSNR下降高达4.6 dB，且Figure 5显示视图间距越大，几何特征的贡献越显著。这证实了事件流提供的稠密几何先验是EA3D在少视图大基线场景下性能优势的核心来源。

### 条件特征融合：从直接投影到交叉注意力驱动的3D特征对齐

传统方法通常直接将RGB投影特征或图像作为扩散模型的条件，忽略了不同模态特征在姿态空间和语义空间中的异构性。EA3D提出了一种基于**交叉注意力（Perceiver attention）的特征融合机制**，将无姿态的事件几何特征与有姿态的RGB外观特征对齐为视角相关的3D条件特征（Equation 3）：

$$\{ \mathbf{F}_{3\mathrm{D}} \}_{i=1}^{N} = \{ \mathrm{Attention}(Q(\mathbf{F}_{\mathrm{appr}}^{i}), K(\mathbf{F}_{\mathrm{event}}), V(\mathbf{F}_{\mathrm{event}})) \}_{i=1}^{N}$$

这一设计的因果逻辑在于：外观特征 $\mathbf{F}_{\mathrm{appr}}^{i}$ 携带了逐帧的纹理、色彩和粗略视角先验，但受限于稀疏输入视角，存在严重的遮挡和失真；事件特征 $\mathbf{F}_{\mathrm{event}}$ 则提供了与视角无关的稠密几何结构，但缺乏外观信息。通过交叉注意力，EA-Renderer以外观特征为查询，从事件特征中检索并注入几何结构信息，生成兼具纹理细节和几何完整性的3D特征。这种融合策略使得EA3D能够在事件相机轨迹与目标视点轨迹存在偏差时仍保持鲁棒性——Figure 11显示，即使ATE接近1，PSNR仍保持相对稳定。

### 生成模型类型：从单帧扩散或逐场景优化到3D条件视频扩散

逐场景优化方法（NeRF/3DGS）需要针对每个场景进行数千次迭代优化，推理成本高昂（Table 4）。部分可泛化方法使用单帧图像扩散模型逐帧生成新视角，缺乏时序一致性约束。

EA3D采用**基于DiT架构的视频扩散模型**（改编自CogVideoX），以EA-Renderer渲染的3D特征序列 $\mathbf{F}_{3\mathrm{D}}$ 为条件，在潜空间中去噪生成时空一致的视图序列。这一选择的关键优势在于：视频扩散模型内置的时序注意力机制天然保证了生成视图之间的连贯性，而3D条件特征则为去噪过程提供了显式的几何和外观引导。训练使用标准的扩散损失 $\mathcal{L}_{\mathrm{diffusion}}$（Equation 4）和额外的重建损失 $\mathcal{L}_{\mathrm{recon}}$（Equation 5），后者强制渲染的3D特征与真实视图编码特征对齐，加速收敛并提升结构一致性——消融实验（Table 3 “w/o Reconstruction Loss”）证实移除该损失会导致结构一致性和感知质量明显退化。

综上，EA3D通过上述三个changed slots的协同设计，实现了从“仅RGB、逐场景优化”到“事件增强、可泛化、时空一致”的范式跃迁。在最具挑战性的2视图大基线设定下，EA3D在T&T基准上以23.50 PSNR显著超越ViewCrafter的18.24 PSNR（+5.26 dB），在真实事件数据DSEC上以24.89 PSNR领先6.18 dB（Table 1, Table 2），充分验证了创新设计的有效性。



EA3D 的整体 pipeline 围绕一个核心洞察构建：**事件流蕴含微秒级、抗遮挡的几何结构线索，而 RGB 帧携带纹理与色彩**。通过一个可学习的 EA-Renderer 将两者融合为视角相关的 3D 特征，再以此条件驱动视频扩散模型，可在不依赖逐场景优化的情况下生成时空一致的高保真新视角。

### 输入与输出

**输入**由两个互补模态组成：
- **稀疏 RGB 帧**：提供场景的外观信息（纹理、色彩），但帧数少且视角稀疏。
- **连续事件流**：来自事件相机的异步、微秒级事件序列，携带稠密且抗遮挡的几何结构信息。

**输出**为沿任意目标相机轨迹渲染的新视角图像序列，该轨迹无需与事件相机轨迹严格对齐。

### 两大核心模块

EA3D 由两个关键组件级联构成（图1）：

1. **EA-Renderer（事件增强的特征渲染器）**：负责将稀疏 RGB 帧和连续事件流融合为视角相关的 3D 条件特征。该模块分为三个阶段：
   - **外观特征提取**：利用预训练的多视角立体视觉（MVS）模型和 CogVideoX 的 3D VAE 编码器，将投影到目标视角的 RGB 帧编码为逐帧外观特征 $\{\mathbf{F}_{\mathrm{appr}}^{i}\}_{i=1}^{N}$。
   - **事件几何特征提取**：通过自适应切片策略将事件流组织为短/长事件体素网格，再经 3D CNN 编码为紧凑的几何特征 $\mathbf{F}_{\mathrm{event}}$。
   - **特征融合**：采用 Perceiver cross-attention 机制，以无姿态的事件几何特征为 Key/Value、有姿态的外观特征为 Query，生成视角相关的 3D 特征 $\{\mathbf{F}_{3\mathrm{D}}\}_{i=1}^{N}$。

2. **3D-aware 扩散模型**：基于 CogVideoX 的 DiT 架构改编的视频扩散模型。以 EA-Renderer 输出的 3D 特征为条件，在潜空间执行去噪过程，解码出高保真的新视角图像序列。

### 信息流与模块关系

```
稀疏RGB帧 ──→ 外观特征提取 ──→ F_appr ──┐
                                          ├──→ Cross-Attention ──→ F_3D ──→ 视频扩散模型 ──→ 新视角序列
连续事件流 ──→ 自适应切片 ──→ 事件几何特征提取 ──→ F_event ──┘
```

外观特征携带了逐帧的纹理和粗粒度视角先验，但受限于稀疏输入，在遮挡和大基线区域存在严重退化。事件几何特征则提供了时间稠密、外观无关的结构信号，能够有效补充被遮挡区域的几何信息。两者的融合通过交叉注意力实现：每个目标帧的外观特征作为 Query，从全局事件几何特征中检索所需的结构信息，从而生成既包含丰富外观又具备完整几何的 3D 条件特征。

这种设计使得 EA3D 无需对每个新场景进行逐场景优化（如 NeRF 或 3DGS），即可在推理时直接泛化到未见场景。训练时，扩散模型以 $\mathcal{L}_{\mathrm{diffusion}}$ 和 $\mathcal{L}_{\mathrm{recon}}$ 联合优化，其中重建损失强制 EA-Renderer 渲染的 3D 特征与真实视图的编码特征对齐，加速收敛。

### 补充图表

![[assets/figures/papers/paper_list_l17_https_openreview_net_forum_id_YwawhlWdtm/figures/001_Figure_1.jpg]]
*Figure 1: Overview of EA3D. Given a set of sparse RGB frames and continuous event streams, we learn an Event-Augmented Feature Renderer (EA-Renderer) to construct view-dependent 3D features by projecting both appearance cues from RGB frames and occlusion-resilient geometry features from adaptively sliced event voxel grids into each target camera frustum. These 3D features are then passed into a conditional video diffusion model as 3D conditions, facilitating photorealistic and consistent novel view synthesis*



EA3D 由两大关键模块串联构成：**事件增强的特征渲染器（EA-Renderer）** 与 **3D感知的视频扩散模型**。EA-Renderer 负责将稀疏 RGB 帧与连续事件流融合为视角相关的 3D 条件特征，扩散模型则以此特征为条件，在潜空间中生成时空一致的新视角序列。

### EA-Renderer：三阶段特征渲染

EA-Renderer 按以下三个阶段构建目标相机截锥内的 3D 特征：

**阶段一：外观特征提取**

将稀疏 RGB 帧通过相机位姿投影到目标新视角，再经由预训练的 3D VAE 编码器（CogVideoX 的编码器）提取逐帧外观特征：

$$\{ \mathbf{F}_{\mathrm{appr}}^{i} \}_{i=1}^{N} = \mathcal{E}_{\mathrm{appr}}(\{ \mathbf{P}^{i} \}_{i=1}^{N})$$

其中 $\mathbf{P}^{i}$ 为投影后的第 $i$ 帧 RGB 图像，$\mathcal{E}_{\mathrm{appr}}$ 为外观编码器，输出 $N$ 帧的外观特征图 $\mathbf{F}_{\mathrm{appr}}^{i}$。

**阶段二：事件几何特征提取**

对连续事件流进行**自适应切片**，构造短窗口和长窗口的体素网格，以同时捕获细粒度边缘结构与粗粒度空间轮廓。随后通过 3D 卷积网络编码为紧凑的几何特征：

$$\mathbf{F}_{\mathrm{event}} = \mathcal{E}_{\mathrm{event}}(\{ \mathbf{E}^{i} \}_{i=1}^{N})$$

其中 $\{ \mathbf{E}^{i} \}$ 为自适应融合后的事件体素网格，$\mathcal{E}_{\mathrm{event}}$ 为 3D CNN 编码器。事件特征的可视化（Figure 8）表明，编码器成功捕获了物体边缘和轮廓等几何结构信息。

![[assets/figures/papers/paper_list_l17_https_openreview_net_forum_id_YwawhlWdtm/figures/011_Figure_8.jpg]]
*Figure 8: Visualization of event features. The top row shows the RGB images of the scene, while the bottom row shows the visualizations of the event features. The feature maps clearly reveal structural information such as object edges and contours, indicating that the event encoder successfully captures the geometric details of the scene*

**阶段三：跨模态特征融合**

外观特征携带纹理与色彩但缺乏几何，事件特征蕴含稠密几何但无姿态与外观。通过 Perceiver 交叉注意力将二者融合，以无姿态的事件特征作为 Key-Value，有姿态的外观特征作为 Query，生成视角相关的 3D 条件特征：

$$\{ \mathbf{F}_{3\mathrm{D}} \}_{i=1}^{N} = \{ \mathrm{Attention}(Q(\mathbf{F}_{\mathrm{appr}}^{i}), K(\mathbf{F}_{\mathrm{event}}), V(\mathbf{F}_{\mathrm{event}})) \}_{i=1}^{N}$$

这一融合机制使每个目标视角都能从事件流中提取到抗遮挡的几何先验，同时保留 RGB 帧中的外观细节。

### 3D 感知扩散模型

以 EA-Renderer 输出的 3D 特征 $\mathbf{F}_{3\mathrm{D}}$ 为条件，采用基于 DiT 架构的视频扩散模型（改编自 CogVideoX）在潜空间中建模条件分布 $p(\mathbf{I} | \mathbf{F}_{3\mathrm{D}})$，通过迭代去噪生成高保真的新视角图像序列。训练使用标准的扩散去噪损失：

$$\mathcal{L}_{\mathrm{diffusion}} = \mathbb{E}_{\mathbf{I}, \mathbf{F}_{3\mathrm{D}}, t, \epsilon} \left[ \| \epsilon - \epsilon_{\theta}(\mathbf{I}, t, \mathbf{F}_{3\mathrm{D}}) \|_{2}^{2} \right]$$

其中 $\epsilon$ 为添加的噪声，$\epsilon_{\theta}$ 为以 3D 特征为条件的去噪网络，$t$ 为扩散时间步。

### 辅助重建损失

为加速收敛并强制 EA-Renderer 渲染的 3D 特征与真实视图的编码特征对齐，引入额外的 L2 重建损失：

$$\mathcal{L}_{\mathrm{recon}} = \| \mathbf{F}_{3\mathrm{D}} - \mathcal{E}_{\mathrm{appr}}(\mathbf{I}) \|_{2}^{2}$$

其中 $\mathbf{I}$ 为真实目标视图，$\mathcal{E}_{\mathrm{appr}}$ 为冻结的外观编码器。消融实验（Table 3, Figure 4）表明，去除该损失会导致结构一致性和感知质量明显退化。

### 关键设计要点

- **自适应事件切片**：通过均匀采样事件数量 $m \in [1\times 10^5, 3\times 10^5]$ 构造短/长体素网格，在保留细粒度边缘的同时捕获全局几何轮廓。消融实验（Table 3 “w/o Adaptive Slicing”）证实该策略有效提升合成质量并减少伪影。
- **轨迹增广**：训练时对事件流施加时间平移和反转等增广，使模型学习在事件相机轨迹与目标视点轨迹不对齐的情况下仍能提取有效几何先验（Figure 9, Figure 11），这是 EA3D 支持灵活相机轨迹的关键。

### 补充图表

![[assets/figures/papers/paper_list_l17_https_openreview_net_forum_id_YwawhlWdtm/figures/009_Figure_6.jpg]]
*Figure 6: Illustration of adative event slicing*



## 实验与关键发现

### 主实验结果

EA3D在两类截然不同的数据域上均表现出对现有方法的系统性优势：合成事件驱动的开放场景（DL3DV与Tanks-and-Temples）和真实事件驱动的驾驶场景（DSEC）。实验设置上，所有可泛化基线仅使用稀疏RGB输入，不提供事件流；基于优化的方法（E-NeRF、Event3DGS）则接收完整的事件流与RGB帧，但需对每个场景单独优化。EA3D在推理时不执行任何逐场景优化，直接以EA-Renderer输出的3D特征驱动视频扩散模型生成新视角序列。

**开放场景（合成事件）**。在最具挑战性的2-视图大基线设定下，EA3D在Tanks-and-Temples上取得23.50 PSNR / 0.756 SSIM / 0.218 LPIPS，相比仅依赖RGB的可泛化方法**ViewCrafter**（Yu et al., 2025c）的18.24 / 0.607 / 0.289，PSNR提升+5.26 dB，SSIM提升+0.149，LPIPS降低-0.071（Table 1 II部分）。基于优化的**E-NeRF**（Klenk et al., 2023）和**Event3DGS**（Han et al., 2024）虽能访问事件流，但因逐场景优化的过拟合倾向和缺乏生成先验，在跨场景泛化设定下指标明显落后。随着输入视图从2增至6，所有方法的指标均有改善，但EA3D在4-视图和6-视图设置下仍保持最优，表明其优势并非仅在极端稀疏条件下成立。

**真实事件数据（DSEC）**。在DSEC的真实事件流上，EA3D无需任何微调即取得最优结果：2-视图下24.89 PSNR / 0.792 SSIM / 0.211 LPIPS，相比ViewCrafter的18.71 / 0.684 / 0.279，PSNR提升+6.18 dB（Table 2）。值得注意的是，此设定下真实事件流包含传感器噪声和量化效应，而EA3D的训练完全基于合成事件（vid2e模拟器），该跨域迁移能力来源于训练时对对比度阈值和分辨率的混合增广（Figure 7）。定性结果（Figure 3）显示，EA3D在真实事件输入下生成的纹理更清晰、几何结构更完整，而RGB-only基线在大基线区域出现明显的几何坍塌和模糊。

**生成质量评估**。除重建指标外，FID指标（Figure 13）进一步揭示了EA3D的生成能力优势：在Tanks-and-Temples上，EA3D在各输入视图数下均取得最低FID，表明其生成图像的分布更接近真实图像。

### 消融实验

消融实验围绕三个核心设计要素展开：事件几何特征的有效性、重建损失的贡献、以及自适应事件切片策略的作用。所有消融均在2-视图设定下进行，以最大化设计选择的区分度（Table 3, Figure 4）。

![[assets/figures/papers/paper_list_l17_https_openreview_net_forum_id_YwawhlWdtm/figures/006_Table_3.jpg]]
*Table 3: Quantitative ablation on model design and training loss. Experiments are conducted under the challenging 2-view setting on the Tanks-and-Temples (Knapitsch et al., 2017) benchmark and real event data from the DSEC (Gehrig et al., 2021) dataset*

![[assets/figures/papers/paper_list_l17_https_openreview_net_forum_id_YwawhlWdtm/figures/007_Figure_4.jpg]]
*Figure 4: Qualitative ablation on the model design and training loss. Experiment conducted under the challenging 2-view setting*

**事件几何特征的因果作用**。移除事件几何特征（w/o Geometry Feature）——即仅使用RGB外观特征作为扩散模型的条件——导致T&T上PSNR下降超过4 dB，DSEC上同样出现显著退化。Figure 5进一步揭示了该效应的视图依赖性：当源视图与目标视图的间距增大时，仅依赖RGB投影的基线性能急剧下降，而完整EA3D的性能衰减明显更缓。这一现象直接验证了核心假设：事件流提供的稠密、抗遮挡几何先验在大基线条件下具有不可替代的作用。

**重建损失的必要性**。去除重建损失$\mathcal{L}_{\text{recon}}$（w/o Reconstruction Loss）使得结构一致性和感知质量明显退化（Figure 4）。该损失强制EA-Renderer输出的3D特征与真实视图的外观编码对齐，在训练初期为扩散模型提供了关键的收敛信号。缺乏该约束时，3D特征与扩散模型的潜空间之间的语义鸿沟难以弥合。

**自适应事件切片**。替换为固定切片策略（w/o Adaptive Slicing）导致伪影增加和指标下降。自适应切片通过随机采样事件数量$m \in [1\times10^5, 3\times10^5]$，使模型在训练中接触不同时空密度的事件体素网格，从而在推理时对不同运动速度和事件速率具有鲁棒性（Figure 6）。

### 鲁棒性分析

**运动模糊与快速运动**。EA3D对运动模糊输入表现出显著鲁棒性：在合成运动模糊的输入下，PSNR仅从23.50降至22.73（-0.77 dB），而ViewCrafter从18.24降至16.43（-1.81 dB）（Table 5）。在快速运动场景中，事件引导带来的PSNR增益约为4–5 dB（Table 6），因为事件流在微秒级时间分辨率下天然抗运动模糊。

**轨迹不对齐**。由于训练中引入了相机轨迹增广（时间平移、反转等），EA3D对事件相机轨迹与目标新视角轨迹的偏差具有强鲁棒性。Figure 11显示，即使绝对轨迹误差（ATE）接近1，PSNR仍保持相对稳定。这一特性使EA3D在实践中无需严格约束事件相机的运动路径。

**对比度阈值**。Figure 12表明，EA3D在较宽的对比度阈值范围内保持稳定性能，这得益于训练中混合了不同阈值（0.05–0.3）的合成事件。

### 计算成本与效率

Table 4对比了各方法的计算成本。EA3D在推理时无需逐场景优化，单次前向传播即可生成新视角序列，推理时间显著低于需要数千次迭代优化的E-NeRF和Event3DGS。但推理显存消耗约28 GB（A100 GPU），当前不易部署到边缘设备。

### 与事件驱动帧插值方法的对比

Table 7将EA3D与基于事件的帧插值方法VDM-EVFI进行对比。帧插值方法仅能在已有帧之间内插，无法生成超出事件相机轨迹覆盖范围的新视角。EA3D在新视角合成任务上的指标显著优于帧插值方法在对应视角上的表现，验证了其真正的3D感知生成能力。

### 失败模式与局限

尽管EA3D在多数场景下表现优异，仍存在以下已知局限：
1. **强动态场景**：在包含非刚性运动或显著光照突变的场景中，事件-外观融合策略的几何先验可靠性尚未验证。
2. **真实事件退化**：训练完全依赖合成事件模拟器，对真实事件传感器的极端噪声、像素死区等退化模式的鲁棒性未充分评估。
3. **分辨率与序列长度**：骨干视频扩散模型CogVideoX固定了最大分辨率和序列长度，不支持自适应推理。
4. **计算资源需求**：28 GB推理显存限制了对边缘设备的部署可能性。

### 补充图表

![[assets/figures/papers/paper_list_l17_https_openreview_net_forum_id_YwawhlWdtm/figures/003_Table_1.jpg]]
*Table 1: Quantitative comparison on in-the-wild scenes. We evaluate our model on the DL3DV (Ling et al., 2024) and Tanks-and-Temples (Knapitsch et al., 2017) (T&T) benchmarks under 2, 4, and 6 input views*

![[assets/figures/papers/paper_list_l17_https_openreview_net_forum_id_YwawhlWdtm/figures/005_Table_2.jpg]]
*Table 2: Quantitative comparison on real event data. We report performance under 2, 4, and 6 input views on the DSEC dataset (Gehrig et al., 2021)*

![[assets/figures/papers/paper_list_l17_https_openreview_net_forum_id_YwawhlWdtm/figures/004_Figure_3.jpg]]
*Figure 3: Qualitative comparison on real event data. Our method produces sharper textures and more complete geometry compared to both optimization-based and RGB-only baselines, demonstrating its robustness under real-world event inputs*

![[assets/figures/papers/paper_list_l17_https_openreview_net_forum_id_YwawhlWdtm/figures/008_Figure_5.jpg]]
*Figure 5: Ablation on the effectiveness of geometry features extracted from event streams under increasing view range*

![[assets/figures/papers/paper_list_l17_https_openreview_net_forum_id_YwawhlWdtm/figures/014_Table_4.jpg]]
*Table 4: Computation cost comparison with the baselines*

![[assets/figures/papers/paper_list_l17_https_openreview_net_forum_id_YwawhlWdtm/figures/016_Figure_11.jpg]]
*Figure 11: Ablation on robustness to misalignment between novel view trajectory and event camera trajectory*

![[assets/figures/papers/paper_list_l17_https_openreview_net_forum_id_YwawhlWdtm/figures/010_Figure_7.jpg]]
*Figure 7: Event simulation under different contrast thresholds and resolutions. Each row corresponds to a simulated resolution: 1024 × 576, 346 × 260, and 240 × 180, respectively. Each column shows the simulated events under different contrast thresholds: 0.05, 0.12, and 0.3. Lower thresholds lead to denser event firing with more fine-grained structure, while higher thresholds produce sparser events primarily along strong edges. To improve robustness across varying event data quality and settings, we train our model with mixed simulated events from diverse thresholds and resolutions*



## 定位与知识库关联

### 1. 问题定位：稀疏观测下的几何信息瓶颈

在快速相机运动下进行新视角合成，核心瓶颈在于**几何信息的缺失**。传统基于RGB帧的方法（无论是逐场景优化还是可泛化方法）依赖稀疏的彩色图像推断场景结构，当输入视图数量降至2–4帧且基线较大时，视差估计和深度warp过程会因遮挡和纹理不足而严重退化。事件相机以微秒级时间分辨率异步输出亮度变化的像素级信号，天然蕴含稠密、抗遮挡的几何结构线索——物体边缘和轮廓在事件流中以高时间密度持续触发，不受帧率限制。EA3D的核心洞察在于：**事件流提供几何先验，RGB帧提供外观纹理，两者的互补性可以通过一个可学习的特征渲染器（EA-Renderer）和条件视频扩散模型被系统性利用，从而在无需逐场景优化的情况下实现高保真新视角合成**。

### 2. 方法谱系中的位置

EA3D处于**事件驱动新视角合成**与**可泛化扩散先验新视角合成**两条技术路线的交汇点。下表将EA3D与代表性基线在三个关键设计维度上进行对比：

| 方法 | 几何信息来源 | 生成模型类型 | 是否需逐场景优化 |
|------|-------------|-------------|----------------|
| **E-NeRF** (Klenk et al., 2023) | 事件流 + RGB帧 | NeRF体渲染 | 是 |
| **Event3DGS** (Han et al., 2024) | 事件流 + RGB帧 | 3D高斯泼溅 | 是 |
| **ViewCrafter** (Yu et al., 2025c) | 仅RGB帧（点云重建） | 视频扩散模型 | 否 |
| **NVS-Solver** (You et al., 2025) | 仅RGB帧（深度warp） | 单帧扩散+修复 | 否 |
| **EA3D**（本方法） | 事件流（稠密几何）+ RGB帧（外观） | 视频扩散模型（CogVideoX改编） | 否 |

**关键区分**：
- 与E-NeRF和Event3DGS相比，EA3D共享“事件+RGB”的输入模态，但**不依赖逐场景优化**。EA3D的EA-Renderer和扩散模型在训练后可直接泛化到新场景，推理无需梯度更新（Table 4显示推理仅需约1.5秒/帧，而优化方法需数分钟至数十分钟）。
- 与ViewCrafter和NVS-Solver相比，EA3D共享“可泛化+扩散先验”的生成范式，但**额外引入事件流作为几何先验**。消融实验（Table 3）表明，移除事件几何特征后，2-视图设置下PSNR下降高达4.6 dB，且视图间距越大优势越明显（Figure 5）。

### 3. 技术贡献的因果机制

EA3D的性能优势可分解为三个因果环节：

**（1）事件几何特征提取**：自适应事件切片策略（Figure 6）将连续事件流划分为短窗口（捕获细粒度边缘）和长窗口（提供全局结构），通过3D CNN编码为紧凑的几何特征 $\mathbf{F}_{\mathrm{event}}$。该特征**无相机姿态信息**，仅编码场景的几何结构。Figure 8的可视化证实，事件特征图清晰揭示了物体边缘和轮廓。

**（2）跨模态特征融合**：通过Perceiver交叉注意力机制，将无姿态的事件几何特征作为Key-Value，注入到有姿态的RGB外观特征中，生成视角相关的3D特征 $\{ \mathbf{F}_{3\mathrm{D}} \}_{i=1}^{N}$。这一设计的关键在于：**事件特征的姿态无关性使其能够灵活服务于任意目标相机轨迹**，而RGB特征提供粗粒度的视点先验和外观信息。

**（3）3D条件视频扩散**：以 $\mathbf{F}_{3\mathrm{D}}$ 为条件驱动视频扩散模型（CogVideoX的DiT架构），在潜空间生成时空一致的视图序列。与单帧扩散方法（如NVS-Solver）相比，视频扩散模型通过时间注意力层保证了生成视图间的3D一致性。

### 4. 适用边界与局限

**已验证的适用条件**：
- **静态场景**：训练和评估均在静态场景下进行（DSEC数据集使用静态场景以保证参考RGB帧质量）。
- **事件模拟训练**：训练数据依赖vid2e模拟器从RGB视频生成合成事件，通过多对比度阈值（0.05–0.3）和多分辨率（180p–576p）增广提升鲁棒性（Figure 7）。
- **轨迹灵活性**：通过轨迹增广（时间偏移、反转），EA3D对事件相机轨迹与目标视点轨迹的偏差具有鲁棒性（Figure 11，ATE接近1时PSNR仍保持稳定）。

**已验证的局限**：
- **对真实事件噪声的鲁棒性未完全验证**：尽管在DSEC真实事件数据上无需微调即取得最优（Table 2），但论文未系统评估传感器噪声、事件丢失或退化条件下的性能。
- **分辨率与序列长度固定**：骨干视频扩散模型CogVideoX的架构固化了最大分辨率和序列长度，不支持自适应推理。
- **推理资源需求高**：推理显存消耗约28 GB（A100），当前不易部署到边缘设备。

### 5. 开放问题与未来方向

**（1）动态场景的泛化能力**：EA3D当前在静态场景下验证有效，但在非刚性运动、显著光照突变等强动态场景下，事件-外观融合策略是否仍能提供可靠的几何先验，尚待验证。事件流在动态场景中会混合物体运动和相机运动，几何特征提取可能面临歧义。

**（2）轻量化部署**：是否可以通过知识蒸馏或架构瘦身（如采用轻量级DiT变体）将EA3D部署到实时应用中？当前28 GB的显存需求限制了其在机器人和移动设备上的应用。

**（3）多模态传感器融合**：能否将EA3D的事件-外观融合框架扩展到主动深度传感器（如LiDAR、ToF），以更好地建模非朗伯表面和高光区域？事件流对纹理缺失区域（如白墙）的几何信息有限，深度传感器的互补性值得探索。

**（4）与基于事件的帧插值的深层关系**：Table 7与VDM-EVFI的对比显示EA3D在帧插值任务上也具竞争力，但两者在事件信息利用方式上存在本质差异——VDM-EVFI使用事件进行运动估计，而EA3D将事件作为几何先验注入3D特征空间。这一差异是否意味着EA3D的几何特征可以替代显式运动估计，值得进一步研究。



## 原文 PDF

![[paperPDFs/ICLR_2026/EA3D_Event_Augmented_3D_Diffusion_for_Generalizable_Novel_View_Synthesis_bb1d8358dc6f.pdf]]
