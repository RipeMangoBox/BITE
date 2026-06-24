---
title: "No Calibration, No Depth, No Problem: Cross-Sensor View Synthesis with 3D Consistency"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/No_Calibration_No_Depth_No_Problem_Cross_Sensor_View_Synthesis_with_3D_Consistency.pdf
project_link: null
code_link: null
aliases:
- MDCCSMRX3
- NCNDNPCSVS3C
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 置信度感知稠密化与融合（CADF）及自匹配滤波机制——利用图像匹配置信度加权关键点并剔除错误稠密化图块，从而在无需 X 传感器 3D 先验的情况下提升合成质量。
primary_logic: 通过跨模态图像匹配建立稀疏对应，将 X 关键点积累到 RGB 视图，再以 RGB 为引导进行置信度感知的稠密化生成稠密 X 图像；随后通过自匹配滤波剔除不一致块并重新稠密化，最后在 RGB 的 3DGS 框架中统一两种模态，实现既无须 X 的 3D 先验又能保证多视图一致性的跨传感器视角合成。
claims:
- 方法不使用 X 传感器的 3D 先验，仅需对 RGB 进行近乎零成本的 COLMAP。
- 在 METU‑VisTIR‑Cloudy 上所有指标均优于基线方法。
- 消融实验证明每个组件均有贡献，DySPN 置信度集成提升 1 dB，自匹配滤波提升 0.8 dB。
- 即使不使用 3DGS，我们的方法仍优于所有带 3DGS 的基线方法。
---

# No Calibration, No Depth, No Problem: Cross-Sensor View Synthesis with 3D Consistency

> [!tip] 核心洞察
> 通过跨模态图像匹配建立稀疏对应，将 X 关键点积累到 RGB 视图，再以 RGB 为引导进行置信度感知的稠密化生成稠密 X 图像；随后通过自匹配滤波剔除不一致块并重新稠密化，最后在 RGB 的 3DGS 框架中统一两种模态，实现既无须 X 的 3D 先验又能保证多视图一致性的跨传感器视角合成。

| 字段 | 内容 |
|------|------|
| 中文题名 | 无需标定、无需深度：跨传感器视角合成与 3D 一致性 |
| 英文题名 | No Calibration, No Depth, No Problem: Cross-Sensor View Synthesis with 3D Consistency |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2602.23559) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Match‑Densify‑Consolidate (CADF + Self‑matching + RGB‑X 3DGS) |
| Dataset | METU‑VisTIR‑Cloudy, RGB‑NIR‑Stereo, RGBT‑Scenes, DDHR‑HK SAR |

> [!tip] 效果简介
> - METU‑VisTIR‑Cloudy (mean of 6 sequences) 上，p50 (XoFTR similarity diagonal 50th percentile) 34.39 vs 32.07 (MINIMA) (+2.32)。
> - RGB‑NIR‑Stereo (mean of 5 sequences) 上，PSNR↑ 21.152 vs 20.392 (MINIMA) (+0.760)。
> - RGBT‑Scenes (mean of 4 scenes) 上，RMSE↓ (°C) 1.70 (train) / 1.12 (novel) vs 1.76 (XoFTR, train) / 1.38 (XoFTR, novel) (-0.06 (train) / -0.26 (novel))。

## 概述

**核心问题：** 获取像素对齐的 RGB‑X（如热红外、近红外、SAR）跨模态数据依赖繁琐的传感器标定（内参、外参、同步）和精确深度估计，工程成本高昂且难以规模化。现有方法大多假设此类对齐数据已存在，严重制约了大规模真实 RGB‑X 数据集的构建。

**核心洞察：** 本文提出一种 **匹配‑稠密化‑三维巩固（Match‑Densify‑Consolidate）** 框架，彻底摆脱对 X 传感器 3D 先验（深度、传感器相对位姿与内参）的依赖。其关键思路是：通过跨模态图像匹配建立稀疏对应，将多帧 X 关键点积累到 RGB 视图形成半稠密 X‑map；再以 RGB 为引导，在匹配置信度的辅助下进行稠密化生成稠密 X 图像；随后通过自匹配滤波剔除不一致图块并重新稠密化；最后在仅需对 RGB 运行 COLMAP 的 3DGS 框架中统一两种模态，实现多视图一致的跨传感器视角合成。

**方法定位：** 该方法位于跨模态图像匹配与三维场景表示的交叉点。与基于单应性扭曲的基线（如 **XoFTR**，Tuzcuoglu et al., CVPRW 2024；**LightGlue**，Lindenberger et al., ICCV 2023；**LoFTR**，Sun et al., CVPR 2021；**MINIMA**，Ren et al., CVPR 2025）不同，本方法不假设场景为平面，也不要求 X 传感器具备任何 3D 信息；与纯图像生成方法（如 StyleBooth、PixNext）相比，本方法从目标域提取真实锚点进行稠密化，保证了多视图时序一致性。

**主要结果：** 在 METU‑VisTIR‑Cloudy 热红外数据集上，本方法在所有指标上均优于基线（p50 达 34.39，较 MINIMA 提升 +2.32）；在 RGB‑NIR‑Stereo 上 PSNR 达 21.152 dB，超越所有带 3DGS 的基线方法；消融实验证实，置信度感知稠密化与融合（CADF）贡献约 1 dB 提升，自匹配滤波贡献约 0.8 dB 提升；即使完全移除 3DGS 阶段，方法仍以 21.042 dB 的 PSNR 优于所有带 3DGS 的基线，验证了稠密化本身的核心作用。

## 背景与动机

### 跨传感器数据对齐的工程瓶颈

多模态感知系统（如 RGB-热红外、RGB-近红外、RGB-SAR）在自动驾驶、遥感、安防等领域具有重要应用价值。然而，获取像素级对齐的 RGB‑X 图像对需要同时满足三个严苛条件：**内参标定**（两种传感器的焦距、主点等）、**外参标定**（传感器间的相对位姿变换）以及**精确深度**（用于将 X 传感器像素投影到 RGB 视图）。这一标定流程工程成本高昂、难以规模化，且在野外部署或传感器更换时需重复执行，成为构建大规模真实 RGB‑X 数据集的核心障碍。

现有主流方法大多**假设此类对齐数据已经存在**，直接在其上进行训练或推理。例如，基于单应性扭曲（homography warping）的方法利用图像匹配器估计平面变换矩阵，将 X 图像映射到 RGB 视图（如 **XoFTR** (Tuzcuoglu et al., CVPRW 2024)、**MINIMA** (Ren et al., CVPR 2025) 等）；基于图像生成的方法则训练 RGB‑to‑X 翻译网络（如 **StyleBooth**、**PixNext**）。这些范式回避了标定问题，但引入了新的缺陷。

### 单应性假设的失效与多视图不一致

单应性扭曲的核心假设是**场景呈平面结构**。当场景包含明显的前后景层次（如雕塑、建筑立面）时，该假设失效，导致可见的错位伪影（见 Figure 2）。此外，单应性扭曲逐帧独立处理，无法保证跨视图的 3D 一致性——同一三维点在相邻帧的合成结果可能不一致，在视频应用中表现为闪烁或漂移。

纯图像生成方法则面临**时序一致性**挑战：由于 RGB‑to‑X 翻译存在内在歧义性（同一 RGB 外观可对应多种 X 模态响应），生成结果在相邻帧之间缺乏稳定约束，产生不连贯的纹理变化（见 Figure 5 和 Table 2 中 **MEt3R** 指标对比）。

### 本文动机：摆脱 X 传感器的 3D 先验

上述分析揭示了一个关键瓶颈：**现有方法要么依赖完整的 3D 先验（深度 + 双模态标定）而不可规模化，要么放弃 3D 一致性而牺牲合成质量**。本文的核心动机在于打破这一困境——能否在不使用 X 传感器任何 3D 先验（无深度、无内参、无外参）的前提下，实现像素对齐且多视图一致的跨传感器视角合成？

这一目标在工程上具有显著吸引力：RGB 传感器的 SfM 标定（如 COLMAP）已高度成熟且近乎零成本，若能仅依赖 RGB 的 3D 信息来驱动 X 视图合成，即可彻底消除对 X 传感器标定的依赖。本文正是沿此思路，通过“匹配-稠密化-三维巩固”三阶段流程，在 RGB 的 3DGS 框架中统一两种模态，实现了既无须 X 的 3D 先验又能保证多视图一致性的跨传感器视角合成。

## 核心创新

本文的核心贡献在于提出了一套 **匹配‑稠密化‑巩固（Match‑Densify‑Consolidate）** 流程，从根本上改变了跨传感器视角合成的范式：**首次在完全不使用 X 传感器 3D 先验（无需深度、无需跨传感器内外参标定）的条件下，实现了像素对齐的 RGB‑X 视图合成**。其关键创新可归纳为以下四个 changed slots。

### 1. 跨传感器对齐策略：从单应性扭曲到匹配‑稠密化‑三维巩固

现有方法普遍依赖单应性扭曲或图像生成来实现 RGB‑X 对齐。例如，**XoFTR**（Tuzcuoglu et al., CVPRW 2024）、**LightGlue**（Lindenberger et al., ICCV 2023）、**LoFTR**（Sun et al., CVPR 2021）和 **MINIMA**（Ren et al., CVPR 2025）均采用“跨模态匹配 + 单应性扭曲 + 3DGS 渲染”的管线。然而，单应性假设场景为平面结构，当前景与背景存在明显深度分层时会产生可见的错位（Figure 2）。图像生成类方法（如 **StyleBooth** 的 RGB‑to‑Thermal、**PixNext** 的 RGB‑to‑NIR）则缺乏多视图一致性约束，在时序上产生抖动和强度漂移。

本文的替代方案是：首先通过跨模态图像匹配建立稀疏对应关系，将多帧 X 关键点积累到 RGB 视图坐标系得到半稠密 X‑map；随后以 RGB 为引导进行稠密化生成全分辨率 X 图像；最后在 RGB 的 3DGS 框架中统一两种模态，实现多视图一致的渲染。整个流程仅需对 RGB 运行近乎零成本的 COLMAP，彻底摆脱了对 X 传感器深度和标定的依赖。

### 2. 稠密化引导：置信度感知稠密化与融合（CADF）

从稀疏/半稠密 X‑map 到稠密 X 图像的生成是流程的核心瓶颈。基线方法在稠密化过程中未利用匹配置信度信息，低置信度关键点可能误导传播过程。

本文提出 **CADF（Confidence‑Aware Densification and Fusion）** 模块，将图像匹配阶段产生的置信度图 $C_m$ 嵌入到 DySPN 的递归精炼过程中：

$$\mathcal{L}^{t+1} = (1 - C_s C_m) \sum_r \sum_{(a,b)} w_{r,a,b} * \mathcal{L}_{a,b}^t + C_s C_m \mathcal{X}_m$$

其中 $C_s$ 为网络预测的确定性图，$C_m$ 为匹配置信度。两者的乘积 $C_s C_m$ 同时抑制了低置信度关键点的贡献和网络对不确定区域的自适应。在此基础上，对 $C_m$ 进行 K 级阈值化（$K=3$，阈值 $\delta \in \{0.15, 0.3, 0.5\}$）并分别稠密化，再通过融合模块 $F$（基于图像增强网络，在 DIV2K 上预训练去噪/去模糊/超分）将多级结果融合，显著提升了对匹配噪声的鲁棒性。消融实验表明，移除 DySPN 置信度集成导致 PSNR 下降 1 dB，移除多级阈值融合进一步加剧性能退化。

### 3. 错误块过滤：自匹配滤波机制

稠密化网络可能在缺乏可靠匹配的区域（如低纹理平面）生成错误图块。基线方法无任何过滤机制，错误块会直接进入后续流程。

本文提出 **自匹配滤波**，利用匹配器自身的图块级特征进行质量评估。具体而言，从 transformer 匹配器的粗匹配层提取 RGB 与 X 的图块特征 $F_{\mathcal{T}}$ 和 $F_{\mathcal{X}}$，计算缩放点积相似度矩阵：

$$A = \frac{F_{\mathcal{T}} F_{\mathcal{X}}^{\top}}{\tau}$$

通过自匹配损失 $\mathcal{L}_{\mathrm{sim}}$ 促使 $A$ 逼近对角阵，使得正确匹配的图块对在对角线上获得高分。随后计算对角线集中度 $q$，以 $(1-q)$ 分位数作为阈值，剔除低分图块。滤除后的高质量点被重新输入稠密化阶段进行精细稠密化，此时以归一化的自匹配相似度作为新的 $C_m$。消融实验表明，自匹配滤波贡献了 0.8 dB 的 PSNR 提升。

### 4. 多视图一致性：RGB‑X 3DGS 统一巩固

图像生成和逐帧稠密化均无法保证多视图间的一致性。本文在 COLMAP 标定的 RGB 相机位姿下训练 RGB‑X 3DGS，为每个高斯添加 X 通道，共享同一组几何参数（位置、协方差、不透明度），从而将两种模态统一到同一个三维辐射场中。这一设计使得从任意 RGB 视角渲染的 X 图像天然满足多视图几何约束。值得注意的是，即使完全移除 3DGS 阶段，本方法的稠密化结果（PSNR 21.042）仍优于所有带 3DGS 的基线方法，证明了稠密化本身的质量优势；3DGS 的加入则进一步提升了多视图一致性（Table 5）。

### 创新总结

上述四个 changed slots 形成了完整的因果链条：**匹配建立稀疏锚点 → CADF 鲁棒稠密化 → 自匹配滤波剔除错误 → 3DGS 统一巩固**。整个流程无需 X 传感器的任何 3D 先验，仅依赖 RGB 的 COLMAP 位姿，从根本上降低了跨传感器数据获取的工程门槛，为大规模 RGB‑X 数据集建设提供了可规模化的技术路径。

## 整体框架

本文提出一种**匹配‑稠密化‑三维巩固（Match‑Densify‑Consolidate）** 的三阶段流程，在完全不依赖 X 传感器 3D 先验（深度、内参、外参）的前提下，实现像素对齐的跨传感器视角合成。整个管线仅需对 RGB 图像运行近乎零成本的 COLMAP 以获得相机位姿，X 传感器端无需任何标定信息。

### 三阶段流水线

**第一阶段：跨模态匹配与关键点积累。** 使用跨模态图像匹配器（如 XoFTR）建立 RGB 与 X 图像之间的稀疏对应关系。将多帧（N=7，前后各 3 帧）的 X 关键点按 RGB 坐标积累，形成半稠密的 X‑map $\mathcal{X}_m$：

$$
\mathcal{X}_m[p] = \frac{\sum_n \mathbf{1}[p = p_n^{\mathcal{T}}] \mathcal{X}[p_n^{\mathcal{X}}]}{\sum_n \mathbf{1}[p = p_n^{\mathcal{T}}]}
$$

无匹配的位置标记为 void（值 −1）。为降低低纹理/平面区域（天空、地面、墙壁等）的稠密化不确定性，引入 GroundedSAM 分割这些区域，并在其 void 位置均匀采样 warped X 图像的点（仅采样 5%）：

$$
\mathcal{X}_m[p] = \mathcal{X}_W[p], \; p \sim \mathrm{U}(\{p \mid \mathcal{M}(p) = 1 \land \mathcal{X}_m[p] = -1\})
$$

**第二阶段：置信度感知稠密化与融合（CADF）。** 以 RGB 图像和半稠密 X‑map 为输入，通过预训练的稠密化网络 D（含递归单元与 DySPN 层）生成稠密 X 图像。核心创新在于将图像匹配置信度 $C_m$ 嵌入 DySPN 迭代过程：

$$
\mathcal{L}^{t+1} = (1 - C_s C_m) \sum_r \sum_{(a,b)} w_{r,a,b} * \mathcal{L}_{a,b}^t + C_s C_m \mathcal{X}_m
$$

其中 $C_s$ 为网络预测的确定性图，$C_m$ 来自匹配器。置信度乘积 $C_s C_m$ 使网络在迭代中更关注高置信度关键点。进一步对多级阈值（K=3，$\delta \in \{0.15, 0.3, 0.5\}$）的稠密化结果进行融合，得到鲁棒的稠密 X 图像 $\mathcal{X}_d$。融合模块 F 以 SigLIP2 编码器的余弦相似度损失进行自监督训练：

$$
\mathcal{L}_{\mathrm{cos}}(\mathcal{T}, \mathcal{X}_d) = 1 - \frac{f_{\mathrm{SigLIP}}(\mathcal{T})^\top f_{\mathrm{SigLIP}}(\mathcal{X}_d)}{\|f_{\mathrm{SigLIP}}(\mathcal{T})\|_2 \|f_{\mathrm{SigLIP}}(\mathcal{X}_d)\|_2}
$$

**第三阶段：自匹配滤波与精细稠密化。** 利用匹配器粗匹配层的 RGB 与 X 图块特征计算相似度矩阵 $A = F_{\mathcal{T}} F_{\mathcal{X}}^{\top} / \tau$，通过自匹配损失 $\mathcal{L}_{\mathrm{sim}}(A)$ 促使 A 趋近对角阵。以对角线集中度 $q$ 的 $(1-q)$ 分位数为阈值，剔除低质量稠密化图块。随后将归一化的自匹配相似度作为新的 $C_m$，再次执行稠密化以获得精炼结果。

**三维巩固：RGB‑X 3DGS。** 在 COLMAP 得到的 RGB 相机位姿下训练 3D Gaussian Splatting，为每个高斯添加 X 通道，统一两种模态于同一三维辐射场。此阶段仅维护一组 3D 高斯参数，确保多视图渲染的一致性。

### 关键设计决策

1. **无需 X 传感器 3D 先验**：整个管线不依赖 X 传感器的深度、内参或外参，仅需 RGB 的 COLMAP 位姿。这与现有方法（单应性扭曲或图像生成）形成根本区别——单应性扭曲假设场景为平面（Fig. 2 展示了其在非平面场景的明显错位），图像生成则缺乏多视图一致性。

2. **匹配置信度驱动**：CADF 模块将匹配阶段的置信度信息贯穿稠密化全过程，使网络能够区分可靠与不可靠的对应点，从而在稀疏匹配条件下仍能生成高质量稠密结果。

3. **自匹配质量闭环**：自匹配滤波利用匹配器自身的特征相似度评估稠密化质量，形成“稠密化→质量评估→剔除→再稠密化”的闭环，消融实验表明该机制贡献约 0.8 dB 的 PSNR 提升。

4. **模态无关性**：稠密化网络 D 在多种 RGB‑X 模态配对数据上预训练，融合模块 F 在 DIV2K 上预训练用于图像去噪、去模糊和超分辨率，使整个管线可泛化至热红外、NIR、SAR 等多种 X 模态。

### 输入输出规范

- **输入**：未配对的 RGB 多视图图像（含 COLMAP 位姿）与 X 传感器图像（无任何 3D 信息）。
- **输出**：与 RGB 视图像素对齐的稠密 X 图像，以及可在任意新视角渲染的 RGB‑X 3DGS 辐射场。

### 补充图表

![[assets/figures/papers/paper_list_l2554_https_arxiv_org_abs_2602_23559/figures/001_Figure_1.jpg]]
*Figure 1: Problem Setup. Given unpaired RGB-X images from sensors, the task is to synthesize X-images that are pixel-wise aligned with the RGB views for multi-modal applications. Traditional 3D approaches rely on complete 3D priors—including depth and the poses/intrinsics of both modalities—to align and render cross-sensor images. In contrast, our scalable framework removes these dependencies, enabling RGB-guided X-image synthesis without the 3D priors for X to replace calibration for different types of sensors and metric depth acquisition*

![[assets/figures/papers/paper_list_l2554_https_arxiv_org_abs_2602_23559/figures/003_Figure_3.jpg]]
*Figure 3: Method Overview. Our approach consists of three stages. In the first stage, we perform cross-modality feature matching to establish correspondences between RGB and X-images. The matched points are sampled and accumulated onto RGB views to produce semi-dense X-images*

## 核心模块与公式推导

本方法的核心在于将“匹配—稠密化—三维巩固”三阶段流程中的两个关键机制——**置信度感知稠密化与融合（CADF）**和**自匹配滤波**——进行数学化建模，使得跨模态先验信息（匹配置信度、图块自相似度）能够显式地注入稠密化过程，从而在无需 X 传感器 3D 先验的条件下提升合成质量。

### 多帧关键点积累与半稠密 X-map 构建

第一阶段的目标是从非对齐的 RGB-X 图像对中构建一个附着于 RGB 坐标系的半稠密 X 图像 $\mathcal{X}_m$。给定 $N$ 帧 X 图像，利用跨模态匹配器获得 RGB 视图与各 X 帧之间的稀疏对应关系。对于 RGB 视图中的每个像素位置 $p$，其 X 值由多帧匹配点的加权平均得到：

$$
\mathcal{X}_m[p] = \frac{\sum_n \mathbf{1}[p = p_n^{\mathcal{T}}] \mathcal{X}[p_n^{\mathcal{X}}]}{\sum_n \mathbf{1}[p = p_n^{\mathcal{T}}]} \tag{1}
$$

其中 $p_n^{\mathcal{T}}$ 是第 $n$ 帧 X 图像中匹配关键点映射到 RGB 坐标系下的位置，$\mathcal{X}[p_n^{\mathcal{X}}]$ 是该点的 X 传感器读数。若某位置无任何匹配点落入，则标记为 void（值 $-1$）。这一积累机制利用多帧观测的冗余性初步缓解了单帧匹配稀疏和噪声的问题。

对于低纹理平面区域（天空、地面、墙壁等），匹配器天然难以建立可靠对应。为此，方法引入**区域采样**策略：先用 GroundedSAM 对 RGB 图像进行语义分割得到掩码 $\mathcal{M}$，然后在掩码区域内且 $\mathcal{X}_m$ 为 void 的位置上，从单应性扭曲的 X 图像 $\mathcal{X}_W$ 中均匀采样少量点：

$$
\mathcal{X}_m[p] = \mathcal{X}_W[p], \quad p \sim \mathrm{U}\big(\{p \mid \mathcal{M}(p) = 1 \land \mathcal{X}_m[p] = -1\}\big) \tag{2}
$$

这一操作为无匹配区域注入了低成本的几何先验，降低了稠密化阶段在这些区域的不确定性。

### 置信度感知稠密化与融合（CADF）

第二阶段的核心是将半稠密 $\mathcal{X}_m$ 在 RGB 引导下稠密化为完整 X 图像 $\mathcal{X}_d$。稠密化网络 $\mathcal{D}$ 采用递归单元与动态空间传播（DySPN）层的架构。原始 DySPN 的精炼迭代为：

$$
\mathcal{L}^{t+1} = (1 - C_s) \sum_r \sum_{(a,b)} w_{r,a,b} * \mathcal{L}_{a,b}^t + C_s \mathcal{X}_m \tag{3}
$$

其中 $\mathcal{L}^t$ 是第 $t$ 步的中间估计，$w_{r,a,b}$ 是空间注意力权重，$C_s$ 是网络自身预测的确定性图（certainty map）。该公式的核心思想是：在高确定性区域直接信任已知点 $\mathcal{X}_m$，在低确定性区域依赖空间传播来填充。

CADF 的关键创新在于将**图像匹配置信度** $C_m$ 显式嵌入这一迭代过程：

$$
\mathcal{L}^{t+1} = (1 - C_s C_m) \sum_r \sum_{(a,b)} w_{r,a,b} * \mathcal{L}_{a,b}^t + C_s C_m \mathcal{X}_m \tag{4}
$$

$C_m$ 来自匹配器输出的匹配置信度图，其与网络确定性 $C_s$ 相乘后形成联合置信度。这意味着：即使网络认为某区域应信任已知点，若匹配器对该点的置信度很低，该点的影响力也会被抑制。这一乘积形式的耦合机制是 CADF 提升稠密化鲁棒性的因果瓶颈——它使得低质量匹配点不会错误地“锚定”稠密化结果。

在此基础上，CADF 进一步执行 $K$ 级阈值化与融合：对 $C_m$ 取多个阈值 $\delta_k$，生成不同稀疏程度的 $\mathcal{X}_m^{(k)}$，分别进行稠密化后通过融合模块 $\mathcal{F}$ 合并。融合模块 $\mathcal{F}$ 使用 SigLIP2 图像编码器，以余弦相似度损失进行自监督训练：

$$
\mathcal{L}_{\mathrm{cos}}(\mathcal{T}, \mathcal{X}_d) = 1 - \frac{f_{\mathrm{SigLIP}}(\mathcal{T})^\top f_{\mathrm{SigLIP}}(\mathcal{X}_d)}{\|f_{\mathrm{SigLIP}}(\mathcal{T})\|_2 \|f_{\mathrm{SigLIP}}(\mathcal{X}_d)\|_2} \tag{5}
$$

该损失最大化 RGB 图像 $\mathcal{T}$ 与稠密化 X 图像 $\mathcal{X}_d$ 在 SigLIP2 特征空间中的对齐程度，为无配对监督的稠密化提供了语义级训练信号。

### 自匹配滤波与精细阶段稠密化

粗阶段稠密化后，部分图块可能因匹配错误或几何歧义而产生伪影。自匹配滤波机制利用匹配器自身的图块特征来识别并剔除这些低质量块。

具体而言，从匹配器的粗匹配层提取 RGB 特征 $F_{\mathcal{T}}$ 和 X 特征 $F_{\mathcal{X}}$，计算缩放点积相似度矩阵：

$$
A = \frac{F_{\mathcal{T}} F_{\mathcal{X}}^{\top}}{\tau} \tag{6}
$$

其中 $\tau$ 为温度系数。矩阵 $A$ 的每个元素 $A_{ij}$ 表示 RGB 图块 $i$ 与 X 图块 $j$ 的特征相似度。理想情况下，正确稠密化的图块应与其对应的 RGB 图块高度相似，而对其他图块相似度低——即 $A$ 应接近对角阵。

为量化这一特性，定义**自匹配损失**：

$$
\mathcal{L}_{\mathrm{sim}}(A) = -\frac{\mathrm{Tr}(A)}{\|A\|_F} + \lambda \frac{\|A \odot (\hat{\mathbf{1}} - I)\|_1}{\|A\|_F} \tag{7}
$$

第一项 $-\mathrm{Tr}(A)/\|A\|_F$ 鼓励对角线元素之和最大化（即 RGB-X 对应图块的高相似度）；第二项惩罚非对角线元素，$\hat{\mathbf{1}}$ 为全 1 矩阵，$I$ 为单位阵，$\lambda$ 为平衡系数。该损失在稠密化网络训练时作为辅助监督，促使生成的 X 图块在匹配器特征空间中与对应 RGB 图块保持高度一致。

在推理阶段，利用已训练的 $A$ 矩阵进行质量过滤：计算对角线元素集中度 $q$，取 $(1-q)$ 分位数作为阈值，将对角线得分低于该阈值的图块标记为低质量并剔除。随后，将归一化的自匹配相似度作为新的 $C_m$ 代入式 (4)，对过滤后的 X 图像执行精细阶段稠密化。这一“评估—过滤—再稠密化”的闭环设计是消融实验中贡献 0.8 dB 提升的关键。

### 补充图表

![[assets/figures/papers/paper_list_l2554_https_arxiv_org_abs_2602_23559/figures/002_Figure_2.jpg]]
*Figure 2: Homography warping assumes 3D planar structures and causes visible misalignment (statue areas) when the scene contains distinct fore-/background layers*

## 实验与分析

### 核心实验设置与评估基准

方法在四个跨模态基准上进行了系统验证，覆盖热红外（TIR）、近红外（NIR）、长波红外（Thermal）和合成孔径雷达（SAR）四种X模态。所有带3DGS的实验均在相同的RGB COLMAP相机位姿下运行，基线方法统一使用各自的匹配器进行单应性扭曲后由3DGS渲染，确保对比公平性。

- **METU‑VisTIR‑Cloudy**：6个序列的均值评估，主要指标为p50（XoFTR相似度对角线第50百分位数），反映合成X图像与真实X在匹配器特征空间中的一致性。
- **RGB‑NIR‑Stereo**：5个序列，采用PSNR、SSIM、LPIPS等图像质量指标。
- **RGBT‑Scenes**：4个场景，报告训练视角与新视角合成的RMSE（°C）和MAE（°C）。
- **DDHR‑HK SAR**：SAR模态，评估PSNR、SSIM、LPIPS。

### 主结果分析

**METU‑VisTIR‑Cloudy（Table 1）**：本方法在所有指标上一致最优，p50达到34.39，较最强基线MINIMA（32.07）提升+2.32。该指标直接衡量合成图像与真实X在跨模态匹配器特征空间中的对齐程度，提升表明稠密化流程生成的X图像在结构上与真实X更一致，而非仅像素级近似。

**RGB‑NIR‑Stereo（Table 4）**：PSNR达到21.152，SSIM为0.581，均优于所有带3DGS的基线方法。MINIMA以20.392 PSNR位居第二，差距为+0.760 dB。值得注意的是，即使完全移除3DGS阶段（Table 5，"-3DGS"行），本方法的PSNR仍为21.042，**仍高于所有带3DGS的基线方法**。这证明稠密化与自匹配滤波阶段本身已产生高质量的像素对齐X图像，3DGS主要贡献在于多视图一致性巩固而非单帧质量。

**RGBT‑Scenes（Table 3）**：训练视角RMSE为1.70°C（vs XoFTR的1.76°C），新视角RMSE为1.12°C（vs XoFTR的1.38°C）。新视角上的优势更明显（-0.26°C），说明RGB‑X 3DGS在多视图一致性上的增益在未见视角上尤为突出。需注意官方划分的新视角包含较简单视图，误差绝对值低于训练视角。

**DDHR‑HK SAR（Table 7）**：PSNR为17.102（vs MINIMA 15.880），提升+1.222 dB；LPIPS降至0.339（vs MINIMA 0.413）。SAR与RGB的模态差异极大，匹配点数量稀少，但方法仍取得显著提升，体现了CADF模块在低置信度场景下的鲁棒性。

**时序一致性（Table 2）**：与纯图像生成方法相比，本方法的MEt3R得分更低（0.171 vs StyleBooth的0.297），表明match‑densify‑consolidate策略从目标域锚点出发进行稠密化，天然具备更好的多视图时序一致性，而图像生成方法因内在歧义性无法保证跨帧一致。

### 消融实验

Table 5在RGB‑NIR‑Stereo上逐步移除各组件，揭示了每个模块的因果贡献：

| 移除组件 | PSNR变化 | 机制解读 |
|---------|---------|---------|
| 3DGS阶段 | -0.110 dB | 3DGS对单帧质量提升有限，主要贡献在多视图一致性 |
| 自匹配与滤波 | **-0.8 dB** | 剔除错误稠密化图块并基于更可靠点重新稠密化 |
| DySPN置信度集成 | **-1 dB** | 将匹配置信度嵌入递归精炼，降低低置信度关键点干扰 |
| 多级阈值融合 | 进一步下降 | 单阈值无法适应不同区域的匹配置信度分布 |
| 区域采样 | 显著下降 | 低纹理/平面区域若无采样点，稠密化不确定性急剧增加 |

消融结果形成了清晰的因果链：**匹配置信度引导（CADF）→ 错误块过滤（自匹配滤波）→ 三维巩固（3DGS）** 三者递进，前两者贡献了主要的单帧质量增益（合计约1.8 dB），3DGS在此基础上提供多视图一致性。

### 跨模态泛化与失败模式

**成功模式**：在TIR、NIR、Thermal等与RGB共享一定结构信息的模态上，匹配器可提供足够数量的可靠关键点，CADF能有效利用置信度加权，稠密化结果接近真实X。

**边界情况与限制**：
1. **SAR模态**：匹配点数量稀少，稠密化依赖区域采样和低置信度点，PSNR绝对值（17.102）仍较低，表明极端模态差异下性能有上限。
2. **COLMAP依赖性**：3DGS阶段需要对RGB运行COLMAP，对于纹理重复或RGB图像稀少的场景，COLMAP可能失败，此时三维巩固无法执行，但稠密化阶段仍可独立工作（Table 6的无3DGS对比验证了这一点）。
3. **动态场景未验证**：当前实验均在静态场景上进行，动态物体、遮挡和透明表面可能在稠密化中引入伪影，方法的韧性尚需进一步测试。

### 无3DGS的独立验证

Table 6展示了所有方法在完全移除COLMAP/3DGS后的各序列PSNR。本方法在无3DGS条件下仍优于所有带3DGS的基线（均值21.042），这从根本上验证了match‑densify‑consolidate流程不依赖X传感器的任何3D先验——仅凭RGB引导的稠密化即可生成高质量的像素对齐X图像。这一特性使得方法可规模化应用于无法获取X传感器深度和标定的真实场景。

### 补充图表

![[assets/figures/papers/paper_list_l2554_https_arxiv_org_abs_2602_23559/figures/005_Table_1.jpg]]
*Table 1: Results on METU-VisTIR-Cloudy. Results are the mean of all six sequences. We compare with warping by different image matchers, all trained and rendered by 3DGS*

![[assets/figures/papers/paper_list_l2554_https_arxiv_org_abs_2602_23559/figures/014_Table_5.jpg]]
*Table 5: Ablation Study. We ablate each component in turn from the pipeline and report the average scores on RGB-NIR-Stereo*

![[assets/figures/papers/paper_list_l2554_https_arxiv_org_abs_2602_23559/figures/012_Table_4.jpg]]
*Table 4: Results on RGB-NIR-Stereo. Image quality metrics are shown. All methods are run with 3DGS*

![[assets/figures/papers/paper_list_l2554_https_arxiv_org_abs_2602_23559/figures/004_Figure_4.jpg]]
*Figure 4: Visual Results on METU-VisTIR-Cloudy. Our results attain much clearer, sharper, and smoother surface for rendering*

![[assets/figures/papers/paper_list_l2554_https_arxiv_org_abs_2602_23559/figures/009_Figure_7.jpg]]
*Figure 7: Visual Results on RGB-NIR-Stereo. Our view synthesis showcases better structures closer to the groundtruth (GT)*

![[assets/figures/papers/paper_list_l2554_https_arxiv_org_abs_2602_23559/figures/006_Figure_5.jpg]]
*Figure 5: Comparison on Temporal Consistency for Image Generation. StyleBooth [25] generation for thermal images cannot guarantee temporal consistency due to inherent ambiguity, while ours densification creates more consistent multi-views. NIR is closer to the visual spectrum and thus easier to ensure consistency, but the specialized method PixNext [35] still cannot ensure the correct intensity. Compared with our strategy, image translation from the original domain still suffers from inaccurate transformations, whereas our match-densifyconsolidate approach uses information from the target domain as anchors for densification and achieves better results*

![[assets/figures/papers/paper_list_l2554_https_arxiv_org_abs_2602_23559/figures/008_Table_2.jpg]]
*Table 2: Comparison on Temporal Consistency. Compared with pure image generation, our match-densify-consolidate strategy obtains better multiview consistency from lower MEt3R score*

![[assets/figures/papers/paper_list_l2554_https_arxiv_org_abs_2602_23559/figures/011_Table_6.jpg]]
*Table 6: Comparison without 3DGS for all methods. PSNR↑ on each sequence is shown on RGB-NIR-Stereo*

![[assets/figures/papers/paper_list_l2554_https_arxiv_org_abs_2602_23559/figures/013_Table_7.jpg]]
*Table 7: Comparison DDHR-HK SAR. We show image quality metrics against groundtruth*

## 方法谱系与知识库定位

### 核心问题与基线方法

获取像素对齐的 RGB‑X 数据需要繁琐的传感器标定（内参、外参、同步）和精确深度，工程成本高昂且不可规模化。现有工作大多假设此类对齐数据已存在，阻碍了大尺度真实 RGB‑X 数据集建设。本文的核心洞察是：通过跨模态图像匹配建立稀疏对应，将 X 关键点积累到 RGB 视图，再以 RGB 为引导进行置信度感知的稠密化生成稠密 X 图像；随后通过自匹配滤波剔除不一致块并重新稠密化，最后在 RGB 的 3DGS 框架中统一两种模态，实现既无须 X 的 3D 先验又能保证多视图一致性的跨传感器视角合成。

基线方法可归为两类策略：

**第一类：匹配 + 单应性扭曲 + 3DGS 渲染。** 这类方法使用图像匹配器建立 RGB 与 X 的对应关系，然后通过单应性矩阵将 X 图像扭曲到 RGB 视角，最后在 3DGS 中渲染。代表性工作包括：

- **XoFTR**（Tuzcuoglu et al., CVPRW 2024）：跨模态图像匹配器，专门设计用于 RGB‑X 特征匹配。
- **LightGlue**（Lindenberger et al., ICCV 2023）：同域特征匹配器，通过自适应深度和宽度实现高效匹配。
- **LoFTR**（Sun et al., CVPR 2021）：检测器无关的密集匹配器，使用 Transformer 建立像素级对应。
- **MINIMA**（Ren et al., CVPR 2025）：模态不变图像匹配器，通过统一特征空间处理跨模态匹配。

这些方法的根本局限在于单应性扭曲假设场景为平面结构。当场景包含明显的前景/背景层次时（如 Figure 2 所示，雕像区域出现可见的错位），单应性假设失效，导致多视图不一致。本文方法通过匹配‑稠密化‑三维巩固流程替代单应性扭曲，从根本上规避了这一假设。

**第二类：RGB‑to‑X 图像生成。** 这类方法将 X 模态的生成视为图像翻译问题，直接从 RGB 生成 X 图像。代表性工作包括：

- **StyleBooth**：RGB‑to‑Thermal 图像生成方法，通过风格迁移生成热成像。
- **PixNext**：RGB‑to‑NIR 图像生成方法，专门针对近红外模态。

图像生成方法的根本局限在于时序不一致性。如 Figure 5 和 Table 2 所示，StyleBooth 生成的热成像在不同帧之间存在明显的外观漂移（MEt3R 指标为 0.297 vs 本方法 0.171），因为生成过程缺乏对目标域真实信息的锚定。本文方法通过匹配目标域的 X 关键点作为稠密化锚点，保留了目标域的真实辐射信息，从而获得更好的多视图一致性。

### 方法谱系定位

本方法处于“跨传感器视图合成”与“3D 辐射场”的交汇点，其技术谱系可沿以下维度定位：

**1. 对齐策略维度。** 传统方法依赖传感器标定（内参、外参、深度）实现像素级对齐，成本高昂。本文方法将对齐问题转化为“匹配‑稠密化‑巩固”三阶段流程：匹配阶段建立稀疏对应，稠密化阶段以 RGB 为引导从稀疏对应生成稠密 X 图像，巩固阶段在 3DGS 中统一多视图。这一策略的关键优势是**仅需对 RGB 运行近乎零成本的 COLMAP**，完全不需要 X 传感器的 3D 先验。

**2. 置信度利用维度。** 现有稠密化方法（如 DySPN）仅使用网络预测的确定性图 $C_s$，未利用匹配阶段的置信度信息。本文提出的 **CADF（置信度感知稠密化与融合）** 将匹配置信度 $C_m$ 嵌入 DySPN 迭代过程（Eq. 4：$\mathcal{L}^{t+1} = (1 - C_s C_m) \sum_r \sum_{(a,b)} w_{r,a,b} * \mathcal{L}_{a,b}^t + C_s C_m \mathcal{X}_m$），并融合多级阈值结果，使稠密化聚焦于高置信度关键点。消融实验表明，移除 DySPN 置信度集成导致 PSNR 下降 1 dB，移除多级阈值融合进一步下降。

**3. 错误过滤维度。** 现有方法缺乏对稠密化结果的自动质量评估。本文提出的**自匹配滤波机制**利用匹配器自身的图块特征计算相似度矩阵 $A = \frac{F_{\mathcal{T}} F_{\mathcal{X}}^{\top}}{\tau}$，通过自匹配损失（Eq. 7：$\mathcal{L}_{\mathrm{sim}}(A) = -\frac{\mathrm{Tr}(A)}{\|A\|_F} + \lambda \frac{\|A \odot (\hat{\mathbf{1}} - I)\|_1}{\|A\|_F}$）使相似度矩阵接近对角阵，然后根据对角线集中度剔除低质量块。消融实验表明，移除自匹配与滤波导致 PSNR 下降 0.8 dB。

**4. 多视图一致性维度。** 图像生成方法和单应性扭曲方法均逐帧独立处理，无法保证多视图一致性。本文通过 **RGB‑X 3DGS** 在 RGB 相机位姿下为每个高斯添加 X 通道，统一三维辐射场，实现多视图一致的跨传感器渲染。值得注意的是，即使不使用 3DGS，本方法的稠密化结果（PSNR 21.042）仍优于所有带 3DGS 的基线方法（Table 5），验证了稠密化本身的质量优势。

### 适用边界与局限

**1. 跨模态匹配器质量依赖。** 方法性能高度依赖跨模态匹配器的质量。当模态差异过大时（如 SAR 与 RGB），匹配点数量稀少，可能限制稠密化效果。DDHR‑HK SAR 数据集上的结果（Table 7）虽优于基线，但绝对指标（PSNR 17.102, SSIM 0.302）仍较低，反映了这一挑战。

**2. COLMAP 依赖性。** 3DGS 阶段仍需对 RGB 运行 COLMAP。对于 RGB 图像稀少或结构重复的场景（如大面积无纹理墙面），COLMAP 可能失败，从而影响最终三维一致性。这一局限是当前 3DGS 生态的共性瓶颈。

**3. 动态场景未验证。** 当前流程仅在静态场景上验证。动态物体、遮挡和透明表面等复杂情况尚未专门讨论，可能在稠密化和 3D 巩固中引入伪影。如何将框架拓展到动态场景，同时保持跨传感器视图合成的一致性，是重要的开放问题。

**4. 噪声鲁棒性未充分检验。** 当 X 传感器（如低分辨率热像仪）数据噪声较大时，匹配与稠密化的鲁棒性尚未系统评估。是否需要额外的噪声建模是值得探索的方向。

### 开放问题

1. **动态场景拓展。** 如何将匹配‑稠密化‑巩固框架拓展到包含运动物体的动态场景？可能的路径包括引入运动掩码、时序注意力机制或 4D 高斯表示。

2. **轻量化匹配器。** 能否利用更轻量的匹配器或自监督方式完全摆脱对预训练匹配器的依赖，进一步减少离线计算成本？当前流程的匹配阶段是计算瓶颈之一。

3. **下游任务验证。** 所生成的伪对齐数据在语义分割、目标检测等下游任务中的实际增益尚需大规模基准验证。这是衡量方法实用价值的关键维度。

4. **跨模态泛化理论。** 匹配‑稠密化策略在不同模态对（RGB‑Thermal, RGB‑NIR, RGB‑SAR, RGB‑Depth 等）间的泛化能力是否有理论保证？模态间特征空间的几何关系值得深入分析。

## 原文 PDF

![[paperPDFs/CVPR_2026/No_Calibration_No_Depth_No_Problem_Cross_Sensor_View_Synthesis_with_3D_Consistency.pdf]]