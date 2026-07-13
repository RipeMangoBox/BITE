---
title: "PackUV: Packed Gaussian UV Maps for 4D Volumetric Video"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/PackUV_Packed_Gaussian_UV_Maps_for_4D_Volumetric_Video.pdf
project_link: "https://ivl.cs.brown.edu/packuv"
code_link: "https://ffmpeg.org"
aliases:
- PPG
- PackUV
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/benchmarks_datasets_evaluation
core_operator: 通过在UV域直接优化高斯属性，并利用光流引导的关键帧划分与高斯动态/静态标记，实现稀疏、紧凑且时域一致的表示。
primary_logic: 将3D高斯属性无损地打包为一系列2D UV图集（采用金字塔式打包策略），使其与标准视频编解码器完全兼容，从而在不损失质量的前提下实现高效流式传输。
claims:
- PackUV-GS在PackUV-2B、SelfCap、N3DV数据集上全面超越所有基线方法的PSNR、SSIM、LPIPS指标。
- 消融实验表明，移除UV初始化和UV剪枝会导致PSNR明显下降，证明直接在UV空间优化对细节保留至关重要。
- 后优化UVGS映射丢失几何细节并产生伪影，而本方法直接优化UV图集可避免此问题。
- 光流关键帧重置梯度有助于保持长序列的时空一致性，避免质量退化。
---

# PackUV: Packed Gaussian UV Maps for 4D Volumetric Video

> [!tip] 核心洞察
> 将3D高斯属性无损地打包为一系列2D UV图集（采用金字塔式打包策略），使其与标准视频编解码器完全兼容，从而在不损失质量的前提下实现高效流式传输。

| 字段 | 内容 |
|------|------|
| 中文题名 | PackUV：用于4D体积视频的压缩高斯UV图集 |
| 英文题名 | PackUV: Packed Gaussian UV Maps for 4D Volumetric Video |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2602.23040) · [Project](https://ivl.cs.brown.edu/packuv) · [Code](https://ffmpeg.org) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/benchmarks_datasets_evaluation |
| Method | PackUV / PackUV-GS |
| Dataset | PackUV-2B, SelfCap, N3DV, DeskGames |

> [!tip] 效果简介
> - PackUV-2B 上，PSNR 27.41 vs 23.17 (3DGStream) (+4.24 dB)；SSIM 0.842 vs 0.826 (3DGStream) (+0.016)；LPIPS 0.28 vs 0.33 (3DGStream) (-0.05)。
> - SelfCap 上，PSNR 22.52 vs 19.77 (3DGStream) (+2.75 dB)；SSIM 0.783 vs 0.769 (3DGStream) (+0.014)；LPIPS 0.31 vs 0.36 (3DGStream) (-0.05)。
> - N3DV (flame salmon) 上，PSNR 33.06 vs Not available (Not available)。

## 概要

体积视频的流式传输与存储面临一个根本性瓶颈：现有基于3D高斯泼溅（3DGS）的动态场景表示方法，在长序列重建中普遍存在**时间不一致、难以处理大运动与遮挡、且输出格式与标准视频编解码管线不兼容**的问题。这些方法要么逐帧独立优化导致时序抖动，要么依赖变形场而引入额外计算与伪影，最终产出的无序点列表无法被现有视频基础设施直接消费。

PackUV 针对上述瓶颈提出了一套**端到端的4D体积视频表示与拟合方案**。其核心洞察在于：将3D高斯的全部属性（位置、协方差、颜色、不透明度等）**无损地打包为一系列结构化的2D UV图集**，并采用金字塔式分层打包策略以适配不同深度层的遮挡稀疏性。这一表示天然兼容标准视频编解码器（如HEVC、FFV1），可在不损失渲染质量的前提下实现高效流式传输。

为从多视角视频中直接获得上述表示，PackUV-GS 在**UV域内直接优化高斯参数**，而非传统“先优化世界坐标再投影”的后处理范式。该方法通过三个关键机制保障长序列的时空一致性：(1) **光流引导的关键帧划分**，在光流峰值处重置优化窗口，避免误差累积；(2) **高斯动态/静态标记与梯度冻结**，利用协方差感知的光流掩码识别运动区域，仅更新动态高斯，防止静态区域漂移；(3) **UV空间剪枝**，包括有效投影剪枝与每像素Top-K剪枝，维持表示稀疏性。此外，**低精度原地优化（LPO）** 使训练过程直接适配8/16位量化，与视频编解码器的量化管线无缝衔接。

**主要实验结果**：在PackUV-2B（自建最大规模4D多视角数据集，含100序列、超20亿帧、50+同步相机）、SelfCap及N3DV数据集上，PackUV-GS在PSNR、SSIM、LPIPS三项指标上**全面超越所有基线方法**（含3DGStream、4DGS、Deformable3DGS、ATGS等流式与变形场方法）。以PackUV-2B为例，PSNR达27.41 dB，较最强基线3DGStream（23.17 dB）提升**+4.24 dB**；LPIPS降至0.28（基线0.33）。消融实验证实：移除UV直接优化导致细节丢失与伪影（Figure 6），移除关键帧机制使PSNR从27.41骤降至20.95，验证了各核心组件的必要性。

**方法定位**：PackUV处于动态高斯泼溅与视频编解码基础设施的交叉点——它不改变渲染管线，而是重新定义了高斯的组织与优化方式，使4D表示首次具备**原生流式兼容性**。这一设计使其区别于所有现有动态GS方法，后者或牺牲时序一致性以换取流式能力，或产出无法被标准编解码器直接处理的表示格式。

### 体积视频的表示瓶颈

体积视频（volumetric video）旨在从任意视角重建动态三维场景，是实现沉浸式媒体体验的核心技术。近年来，三维高斯泼溅（3D Gaussian Splatting, 3DGS）凭借其高质量实时渲染能力，成为静态场景重建的事实标准。然而，将其扩展到动态体积视频面临三个根本性挑战：

**时间不一致性**：现有动态高斯方法（如基于变形场的方法 **4DGS**、**Deformable3DGS**、**Grid4D**，以及基于四维高斯基元的方法 **RealTime4DGS**）在长序列重建中难以维持时空一致性。变形场方法随时间累积误差，导致渲染质量逐步退化；流式方法 **3DGStream**、**GIFStream** 虽支持逐帧处理，但缺乏长程时间约束。

**大运动与遮挡处理不足**：当场景中出现大幅运动、新物体进入或人员进出时，现有方法往往产生伪影或丢失几何细节。**ATGS** 等流式方法在训练中会出现梯度爆炸问题（见 Figure 8），进一步加剧了不稳定。

**编解码管线不兼容**：现有高斯表示输出无序点列表，无法直接对接成熟的视频编解码基础设施（如 HEVC、FFV1）。这导致体积视频的存储和流式传输效率极低，阻碍了实际部署。

### 核心洞察与本文动机

PackUV 的核心洞察在于：**将三维高斯属性无损地打包为一系列二维 UV 图集，使其与标准视频编解码器完全兼容，从而在不损失质量的前提下实现高效流式传输。**

这一设计的因果逻辑链条如下：
- **瓶颈**：现有方法在三维世界坐标下优化无序高斯点集，导致表示稀疏性不可控、时域一致性难以约束，且输出无法被标准视频管线消费。
- **因果旋钮**：通过在 UV 域直接优化高斯属性（位置、颜色、不透明度、尺度、旋转），并利用光流引导的关键帧划分与高斯动态/静态标记，实现稀疏、紧凑且时域一致的表示。
- **效果**：UV 图集序列可直接输入现成的视频编解码器，将四维高斯场景降维为常规视频资产，同时保持忠实的场景恢复。

### 与现有方法的关键差异

PackUV 在五个关键维度上改变了基线设计：

| 设计维度 | 现有方法 | PackUV |
|---------|---------|--------|
| **优化域** | 世界坐标下的 3D 点集 | UV 空间中的 2D 图集（固定分辨率、预定义层数） |
| **属性存储** | 无序点列表 | 打包为 UV 图集序列（金字塔分层打包） |
| **时域建模** | 逐帧独立优化或变形场 | 光流关键帧划分 → 从上一帧初始化 + 动态/静态掩码冻结 |
| **密度控制** | 基于视图空间梯度的自适应控制 | UV 投影有效剪枝 + 每像素 Top-K 剪枝 |
| **训练精度** | 全精度训练后量化 | 低精度原地优化（8/16 位）+ 直通估计器 |

其中，**直接在 UV 空间优化**（而非先优化三维高斯再投影到 UV 的后处理方式）是保留几何细节的决定性因素——消融实验表明，移除 UV 初始化和 UV 剪枝会导致 PSNR 显著下降（Table 3, w/o UV Optim）；Figure 6 进一步证实，后优化 UVGS 映射会丢失几何细节并产生伪影。

### 数据集贡献

为验证方法在大规模、多视角、高帧率场景下的有效性，本文同时提出了 **PackUV-2B** 数据集——包含 100 个序列、总计超过 20 亿帧，使用超过 50 台同步相机以 1920×1200 分辨率拍摄，支持最高 90 FPS，覆盖 360° 视角（Table 1）。该数据集涵盖了机器人交互、人际互动、体育运动、透明/反射物体等丰富场景标签（Table 6），是目前规模最大的 4D 多视角数据集。

## 核心方法与创新机理

PackUV 的核心创新在于将 3D 高斯泼溅的体积视频表示从“无序点云优化”迁移到“结构化 UV 图集优化”，从而一举解决了现有方法在长序列时间一致性、大运动/遮挡处理、以及标准视频编解码兼容性三个维度的瓶颈。其创新体系可解构为五个相互耦合的 **changed slots**。

### 1. 优化域迁移：从世界坐标点集到 UV 空间图集

传统 3DGS 及其动态变体（3DGStream、4DGS、Deformable3DGS 等）在欧氏空间直接优化高斯点集的位置与属性。PackUV-GS 将优化域迁移到 **UV 空间**——一个固定分辨率、预定义层数的 2D 网格。每个高斯根据其球面坐标映射到离散 UV 坐标：

$$u_i = \left\lfloor \frac{\pi + \theta_i}{2\pi} \times M \right\rfloor, \quad v_i = \left\lfloor \frac{\phi_i}{\pi} \times N \right\rfloor$$

UV 图的每个像素层存储该位置对应高斯的完整属性集 $g_i = \{\rho_i, r_i, s_i, o_i, c_i\} \in \mathbb{R}^D$。这一迁移的因果机制在于：**直接在 UV 域优化避免了“先优化 3D 点再投影到 UV”的后处理损失**。消融实验证实，移除 UV 初始化和 UV 剪枝（即退化为后优化投影）会导致 PSNR 显著下降（Table 3, w/o UV Optim），Figure 6 进一步展示了后优化 UVGS 映射丢失几何细节并产生伪影的失败案例。

### 2. 属性存储重构：金字塔打包 UV 图集

基线方法将高斯属性存储为无序点列表，无法直接输入标准视频编解码器。PackUV 提出 **金字塔式分层打包策略**：深层 UV 层因遮挡导致可见高斯稀疏，因此采用几何递减分辨率：

$$(M_k, N_k) = \begin{cases} (M_0, N_0), & k = 0 \\ (M_{k-1}, N_{k-1}/2), & k \text{ odd} \\ (M_{k-1}/2, N_{k-1}), & k \text{ even} \end{cases}$$

各金字塔层按四叉树布局递归打包为单一纹理图集，尺寸为：

$$W_{\mathcal{A}} = N_0 + \sum_{k=1}^{K-1} N_k, \quad \mathcal{H}_{\mathcal{A}} = \max_k M_k$$

这一设计的核心洞察在于：**将稀疏的 3D 高斯属性无损地压缩为 2D 图集序列，使其与 HEVC、FFV1 等标准视频编解码器完全兼容**，从而在不损失质量的前提下实现高效流式传输。

### 3. 时域建模革新：光流关键帧 + 动态/静态标记

现有流式方法（3DGStream、ATGS、GIFStream）通常逐帧独立优化或依赖变形场，难以处理大运动和遮挡。PackUV-GS 引入双重时域机制：

- **光流关键帧选择**：基于光流幅度峰值检测高漂移、遮挡/去遮挡或外观断裂的帧，将其提升为关键帧。关键帧从上一帧初始化并分配更多训练迭代，非关键帧仅需少量微调。消融实验表明，移除关键帧机制后 PSNR 从 27.41 dB 骤降至 20.95 dB（Table 3, w/o Keyframe），证明其对维持长序列时空一致性的关键作用。

- **高斯动态/静态标记**：利用协方差感知的光流掩码判定高斯是否位于运动区域。具体而言，通过投影 2D 协方差 $\Sigma_{i,c}^{2D} = \mathbf{J}_c \Sigma_{i,\text{cam}}^{3D} \mathbf{J}_c^{\top}$ 和马氏距离测试 $d^2(\mathbf{p}; \mathbf{m}_{i,c}, \Sigma_{i,c}^{2D}) \le 9$ 确定高斯椭球覆盖的像素集，若其中任一点落入光流运动掩码 $M_t^c(\mathbf{p})$，则标记该高斯为动态。静态高斯的梯度被置零（$\nabla_{\theta_i}\mathcal{L} \leftarrow D_i \nabla_{\theta_i}\mathcal{L}$），防止漂移。

### 4. 密度控制适配：UV 投影剪枝 + Top-K 剪枝

传统 3DGS 的自适应密度控制基于视图空间梯度，不适用于 UV 域约束。PackUV-GS 设计了两种 UV 原生剪枝策略：
- **有效 UV 投影剪枝**：剔除映射越界（不满足 UV 坐标映射方程）的高斯。
- **每像素 Top-K 剪枝**：对每个 UV 坐标 $(u,v)$，仅保留不透明度最高的 $K$ 个高斯，强制稀疏性。

### 5. 训练精度创新：低精度原地优化（LPO）

不同于基线方法的全精度训练后量化，PackUV-GS 采用 **8/16 位量化代理进行原地训练**，通过直通估计器保持 FP32 主权重。这使得训练过程直接适配标准视频编解码器的精度约束，Figure 5（左）证实 LPO 相比训练后量化几乎无质量损失。

### 创新耦合关系

上述五个 changed slots 构成因果闭环：UV 域优化（Slot 1）使高斯属性天然具备空间结构，为金字塔打包（Slot 2）提供基础；关键帧与动态标记（Slot 3）确保时域一致性，防止 UV 图集序列出现跳变；UV 原生剪枝（Slot 4）在结构化空间内维持稀疏性；LPO（Slot 5）则打通了从训练到标准编解码的最后一步。这一耦合体系使 PackUV 在 PackUV-2B、SelfCap、N3DV 等数据集上全面超越所有基线方法（Table 2, Table 4），同时保持与现有视频编码基础设施的完全兼容。

PackUV 提出了一套端到端的4D体积视频表示与重建管线，其核心思路是将无序的3D高斯泼溅属性重新组织为结构化的2D UV图集序列，从而在保持渲染质量的同时，使输出天然兼容现有视频编解码基础设施。整个框架由两个紧密耦合的部分构成：**PackUV 表示**与**PackUV-GS 拟合方法**。

### 管线总览

Figure 1 给出了方法的全局视图。输入为多视角RGB视频流，输出为一组可直接送入标准视频编码器（如HEVC、FFV1）的UV图集序列，同时支持从任意新视角实时渲染体积视频。

![[assets/figures/papers/paper_list_l37_https_arxiv_org_abs_2602_23040/figures/001_Figure_1.jpg]]
*Figure 1: We propose a novel and compact 4D representation, PackUV, for volumetric videos that packs 3D Gaussian attributes into a sequence of 2D UV atlases (yellow, top right). PackUV is readily compatible with existing video coding infrastructure (e.g., can be coded with HEVC, FFV1). We also propose PackUV-GS, a method to directly fit Gaussian attributes from multi-view RGB videos into structured PackUV (blue, top left) via optical flow-guided keyframing and Gaussian labeling to fit arbitrary length sequences with temporal consistency even in the presence of large motions and disocclusions. The fitted scene can be rendered back to streamable volumetric video from any viewpoint (red, bottom). We als...*

管线可分解为以下关键阶段：

1. **UV金字塔映射**：将3D高斯的球面坐标离散化为多尺度UV图层，深层分辨率几何递减，以匹配遮挡导致的稀疏性分布。
2. **图集打包**：将金字塔各层按四叉树布局递归拼合为单一纹理图集，消除层间冗余空白，形成紧凑的2D表示。
3. **直接UV空间优化**：在UV网格上原地优化高斯属性（位置、协方差、不透明度、颜色），而非先优化3D点再投影，从而避免后处理带来的细节丢失（Figure 6 证实后优化映射会丢失几何细节并引入伪影）。
4. **光流引导的流式训练**：利用光流幅度峰值自动选取关键帧，划分训练段；通过协方差感知的运动掩码将高斯标记为动态/静态，静态高斯梯度冻结，防止长序列中的漂移。
5. **UV域密度控制**：通过有效UV投影剪枝（剔除映射越界的高斯）和每像素Top-K剪枝（按不透明度保留K个）维持稀疏性。
6. **低精度原地优化（LPO）**：以8/16位量化代理进行训练，保持FP32主权重，使训练过程即产出编解码器可直接消费的低精度表示，避免训练后量化带来的质量损失。

### 模块关系与数据流

Figure 2 底部概括了PackUV-GS的模块关系。数据流如下：

- **输入**：时间步 $t$ 的多视角图像 $\{I_t^c\}$。
- **关键帧判定**：基于光流 $\mathbf{F}_{t-1 \to t}^c$ 的幅度峰值决定当前帧是作为关键帧（重新初始化优化器状态）还是过渡帧（从上一帧参数继承并微调）。
- **高斯标记与冻结**：对每台相机 $c$ 计算二值运动掩码 $M_t^c(\mathbf{p})$（光流幅值超阈值 $\tau$ 则为1），再通过投影2D协方差 $\Sigma_{i,c}^{2D}$ 与马氏距离测试判定高斯 $i$ 的椭球覆盖区域 $\mathcal{E}_{i,c}$ 是否落入运动掩码，得到相机级动态标记 $D_{i,c}$。动态高斯参与梯度更新，静态高斯梯度置零，优化器动量定期重置。
- **UV域优化**：所有高斯属性存储在UV图集 $U[u_i, v_i, k] = g_i$ 中，在该空间直接计算光度损失 $\mathcal{L}_{\text{photo}}$、尺度正则化 $\mathcal{L}_{\text{scale}}$ 和不透明度正则化 $\mathcal{L}_{\text{opacity}}$，反向传播更新UV像素上的属性值。
- **剪枝**：在每次更新后执行结构剪枝（剔除不满足UV映射约束的高斯）和Max-K剪枝（每UV坐标仅保留不透明度最高的 $K$ 个高斯）。
- **输出**：训练完成的UV图集序列可直接作为视频帧送入标准编解码器，解码后按Alpha合成公式从后向前渲染新视角图像。

### 设计瓶颈与因果机制

现有基于高斯泼溅的体积视频方法面临三个核心瓶颈：(1) 长序列重建中时间不一致，(2) 无法有效处理大运动和遮挡，(3) 输出格式不兼容标准视频编解码管线。PackUV通过以下因果链条逐一解决：

- **UV域原生优化** → 消除“先优化3D点再投影到UV”的两阶段信息损失，直接约束高斯位于离散射线，使细节保留能力显著提升（Table 3 中 w/o UV Optim 的PSNR明显下降）。
- **光流关键帧与动态/静态标记** → 将长序列切分为可控片段，仅对运动区域的高斯更新，静态区域冻结，从而抑制漂移并稳定训练（Table 3 中 w/o Keyframe 的PSNR从27.41骤降至20.95）。
- **金字塔打包策略** → 利用深层稀疏性压缩UV图集尺寸，使表示紧凑且与视频编码器无缝对接（Table 5 显示30帧存储仅需10 MB）。

> **注意**：光流估计不准确时，PackUV可能产生拖尾高斯伪影，这是当前管线的已知局限，需要在实际部署中手动验证光流质量。

PackUV的核心设计围绕三个紧密耦合的模块展开：金字塔UV映射与图集打包、直接UV空间优化、以及光流引导的时域一致性建模。以下按模块拆解其关键公式与机制。

### 金字塔UV映射与图集打包

该模块将无序的3D高斯点集转化为结构化的2D图集序列，使其与标准视频编解码管线兼容。

**UV坐标映射**：首先将每个高斯中心 $(\theta_i, \phi_i)$ 的球面坐标归一化到离散UV网格。方位角 $\theta_i$ 和极角 $\phi_i$ 分别映射到 $M \times N$ 分辨率的UV层上：

$$u_i = \left\lfloor \frac{\pi + \theta_i}{2\pi} \times M \right\rfloor, \quad v_i = \left\lfloor \frac{\phi_i}{\pi} \times N \right\rfloor$$

该映射将3D空间点投影到2D参数域，为后续的结构化存储奠定基础。

**金字塔分层策略**：由于深层高斯（按不透明度排序后）因遮挡而逐渐稀疏，PackUV采用几何递减的分辨率金字塔来匹配这一特性。第 $k$ 层的分辨率 $(M_k, N_k)$ 定义为：

$$( M _ { k } , N _ { k } ) = \left\{ \begin{array} { l l } { ( M _ { 0 } , N _ { 0 } ) , } & { k = 0 } \\ { ( M _ { k - 1 } , N _ { k - 1 } / 2 ) , } & { k \mathrm { o d d } } \\ { ( M _ { k - 1 } / 2 , N _ { k - 1 } ) , } & { k \mathrm { e v e n } } \end{array} \right.$$

该设计交替降低宽或高，使深层分辨率指数递减，在保持均匀稀疏性的同时大幅减少存储开销。

**图集打包**：将所有金字塔层按四叉树布局递归打包为单一纹理图集，其尺寸为：

$$W _ { \mathcal { A } } = N _ { 0 } + \sum _ { k = 1 } ^ { K - 1 } N _ { k } , \quad \mathcal { H } _ { \mathcal { A } } = \operatorname* { m a x } _ { k } M _ { k }$$

打包后的图集每个像素层存储完整的高斯属性：

$$U [ u _ { i } , v _ { i } , k ] = g _ { i } = \{ \rho _ { i } , r _ { i } , s _ { i } , o _ { i } , c _ { i } \} \in \mathbb { R } ^ { D }$$

其中 $\rho_i$ 为不透明度，$r_i$ 为旋转四元数，$s_i$ 为尺度，$o_i$ 为球谐系数，$c_i$ 为颜色。这种打包方式使高斯属性序列可直接送入标准视频编解码器进行流式传输。

### 光流引导的时域一致性建模

PackUV-GS通过光流关键帧划分与高斯动态/静态标记来处理长序列中的大运动和遮挡问题。

**二值运动掩码**：对每帧的每个相机视图，利用光流幅度阈值化生成运动掩码：

$$M _ { t } ^ { c } ( \mathbf { p } ) = \left\{ { 1 , \quad \| \mathbf { F } _ { t - 1 \to t } ^ { c } ( \mathbf { p } ) \| _ { 2 } > \tau } , \right. \\ 0 , ~ \mathrm { o t h e r w i s e }$$

其中 $\mathbf{F}_{t-1 \to t}^c(\mathbf{p})$ 表示从 $t-1$ 到 $t$ 帧的光流向量，$\tau$ 为运动阈值。该掩码标识了像素级的运动区域。

**投影2D协方差与重叠测试**：为判定高斯是否受到运动影响，首先将3D协方差投影到图像空间：

$$\Sigma _ { i , c } ^ { 2 D } = { \bf J } _ { c } \Sigma _ { i , \mathrm { c a m } } ^ { 3 D } { \bf J } _ { c } ^ { \top }$$

其中 $\mathbf{J}_c$ 为相机 $c$ 的投影雅可比矩阵。随后通过马氏距离判断像素 $\mathbf{p}$ 是否落在高斯椭球内（3σ范围）：

$$d ^ { 2 } ( \mathbf { p } ; \mathbf { m } _ { i , c } , \boldsymbol { \Sigma } _ { i , c } ^ { 2 D } ) = ( \mathbf { p } \mathbf { - m } _ { i , c } ) ^ { \top } \big ( \boldsymbol { \Sigma } _ { i , c } ^ { 2 D } \big ) ^ { - 1 } ( \mathbf { p } \mathbf { - m } _ { i , c } ) \ \le \ 9$$

**相机级动态标记**：若高斯椭球内任一点落入运动掩码，则标记该高斯为动态：

$$D _ { i , c } = \bigvee _ { \mathbf { p } \in \mathcal { E } _ { i , c } } M _ { t } ^ { c } ( \mathbf { p } )$$

其中 $\mathcal{E}_{i,c}$ 为高斯 $i$ 在相机 $c$ 下的椭球覆盖像素集。**梯度冻结**机制对静态高斯执行 $\nabla _ { \pmb { \theta } _ { i } } \mathcal { L } \leftarrow D _ { i } \nabla _ { \pmb { \theta } _ { i } } \mathcal { L }$，将梯度置零并定期重置优化器动量，防止静态区域漂移。

### 损失函数设计

PackUV-GS的优化目标由四项损失加权组合：

$${ \mathcal { L } } \ = \ { \mathcal { L } } _ { \mathrm { p h o t o } } + { \mathcal { L } } _ { \mathrm { d e p t h } } + \lambda _ { \mathrm { s c a l e } } { \mathcal { L } } _ { \mathrm { s c a l e } } + \lambda _ { \mathrm { o p a c i t y } } { \mathcal { L } } _ { \mathrm { o p a c i t y } }$$

**光度损失**混合L1与SSIM：

$${ \mathcal { L } } _ { \mathrm { p h o t o } } = \left( 1 - \lambda _ { \mathrm { s s i m } } \right) \Vert \hat { I } _ { t } ^ { c } - I _ { t } ^ { c } \Vert _ { 1 } + \lambda _ { \mathrm { s s i m } } \left( 1 - \mathrm { S S I M } ( \hat { I } _ { t } ^ { c } , I _ { t } ^ { c } ) \right)$$

**尺度正则化**惩罚过大的高斯尺度，防止浮动物体：

$$\mathcal { L } _ { \mathrm { s c a l e } } = \mathbb { E } _ { i } \left[ \operatorname* { m a x } \{ 0 , \operatorname* { m a x } ( \mathbf { s } _ { i } ) - s _ { \mathrm { m a x } } \} \right] ^ { 2 }$$

**不透明度正则化**鼓励不透明度趋向0或1，减少半透明伪影：

$$\mathcal { L } _ { \mathrm { o p a c i t y } } = \mathbb { E } _ { i } \alpha _ { i } \left( 1 - \alpha _ { i } \right)$$

渲染时采用标准Alpha合成：${ \pmb { C } } = \sum _ { i = 1 } ^ { M } T _ { i } \alpha _ { i } { \pmb { c } } _ { i }$，其中 $T _ { i } = \prod _ { j < i } ( 1 - \alpha _ { j } )$。

## 实验与关键发现

### 主实验：与流式与动态高斯方法的全面对比

PackUV-GS在PackUV-2B、SelfCap、N3DV三个数据集上对所有基线方法实现了全面超越。**Table 2**给出了以60时间步为训练窗口的定量对比。在PackUV-2B数据集上，PackUV-GS取得PSNR 27.41 dB，相比流式方法**3DGStream**的23.17 dB提升+4.24 dB；SSIM从0.826提升至0.842；LPIPS从0.33降至0.28。在SelfCap数据集上，PackUV-GS同样以PSNR 22.52 dB显著优于3DGStream的19.77 dB（+2.75 dB），LPIPS降低0.05。这一优势源于三个关键机制：（1）直接在UV空间优化高斯属性，避免了后优化投影带来的细节损失（见消融部分）；（2）光流引导的关键帧划分与高斯动态/静态标记，有效处理大运动和遮挡场景下的时序一致性；（3）金字塔式UV打包策略使表示紧凑且与标准视频编解码器完全兼容。

![[assets/figures/papers/paper_list_l37_https_arxiv_org_abs_2602_23040/figures/006_Table_2.jpg]]
*Table 2: Quantitative Comparison. We report PSNR, SSIM, LPIPS, and train time (in hours) for a window length of 60 timestamps. We also report the method’s streaming ability and compatibility with the existing video coding infrastructure*

在N3DV（flame salmon）、DeskGames、Technicolor数据集上的PSNR对比（**Table 4**）进一步验证了方法的泛化能力：PackUV-GS分别取得33.06 dB、32.74 dB、31.87 dB，均达到有竞争力的重建质量。

![[assets/figures/papers/paper_list_l37_https_arxiv_org_abs_2602_23040/figures/009_Table_4.jpg]]
*Table 4: PSNR comparison with the baselines on N3DV (flame salmon), DeskGames, and Technicolor datasets*

**存储效率**方面，**Table 5**给出了30帧场景下的存储开销对比。PackUV仅需约10 MB，远低于基于点云或变形场的动态高斯方法。这得益于金字塔式UV图集的几何递减分辨率设计：深层（高k）因遮挡和基于不透明度的排序而包含逐渐稀疏的高斯分布，因此以交替减半的方式降低分辨率，在保持表达力的同时大幅压缩存储。

### 消融实验：各组件的因果贡献

**Table 3**的消融实验揭示了每个设计选择的因果效应。

**移除UV初始化和UV剪枝（w/o UV Optim）** 导致PSNR显著下降。该变体采用先在世界坐标优化高斯、再后优化投影到UV图集的策略。**Figure 6**展示了这一失败模式：即使使用48层、1K分辨率的UV图集，后优化UVGS映射仍无法捕捉真实场景的几何细节，并产生明显伪影。这证明了直接在UV域优化高斯属性的必要性——UV网格上的梯度信号直接引导高斯位置、尺度和不透明度的更新，避免了从3D到2D的有损映射。

**移除关键帧机制（w/o Keyframe）** 使PSNR从27.41骤降至20.95。无关键帧时，长序列中的误差累积导致高斯漂移，尤其在出现大运动或遮挡时。关键帧机制通过光流幅度峰值检测场景突变点，在关键帧处重置优化器动量并重新初始化高斯，切断了误差传播链。**Figure 3**的定性对比直观展示了这一效果：在人物进入房间并分散的大运动场景中，PackUV-GS保持了干净的几何结构，而基线方法出现严重的拖尾和模糊。

**低精度优化（LPO）** 的消融（**Figure 5 Left**）表明，使用8/16位量化代理进行原地训练几乎不损失质量，相比训练后量化的方案具有明显优势。LPO通过直通估计器保持FP32主权重，使训练过程直接适配目标量化精度，从而与HEVC、FFV1等标准视频编解码器无缝对接。

**光流引导的高斯标记与梯度冻结**（**Figure 3**）通过协方差感知的光流掩码判定高斯是否位于运动区域：对于每个相机视图，计算高斯椭球在图像空间的2D投影协方差 $\Sigma_{i,c}^{2D} = \mathbf{J}_c \Sigma_{i,\text{cam}}^{3D} \mathbf{J}_c^\top$，若椭球内任一像素落入运动掩码 $M_t^c(\mathbf{p})$（由光流幅度阈值化得到），则标记该高斯为动态。静态高斯的梯度被置零，优化器动量定期重置，有效防止了静态区域的漂移。

### 失败模式与局限性

尽管PackUV-GS在多数场景下表现优异，分析揭示了以下失败模式：

1. **光流估计不准确时的拖尾伪影**：当光流预测在无纹理区域或快速运动边界失效时，运动掩码可能错误标记高斯，导致动态高斯未被充分更新或静态高斯被误更新，产生拖尾高斯伪影。

2. **后优化UV映射的细节丢失**：如**Figure 6**所示，先优化后投影的策略在复杂真实场景中即使使用高分辨率图集也无法恢复细节，这从反面验证了直接UV优化的必要性，但也说明UV投影的空间排布本身对分辨率有较高要求。

3. **大范围无纹理区域的鲁棒性不足**：光流引导机制在缺乏纹理信息的区域（如白墙、单色衣物）可能失效，影响高斯标记的准确性。

4. **极快速运动的处理边界**：当帧间运动幅度超过光流估计的捕捉能力时，关键帧检测可能滞后，导致短时间内的质量退化。

### PackUV-2B数据集

**Table 1**对比了PackUV-2B与现有多视图数据集的统计特征。PackUV-2B包含100个多样化序列，总计超过20亿帧，由50余台同步相机以1920×1200分辨率采集，支持最高90 FPS，提供360°覆盖。**Table 6**给出了详细的序列清单，标注了机器人交互（RI）、人-人交互（HI）、物体交互（OI）、运动（SP）、大运动（LM）、遮挡（DO）、透明/反射物体（TR）、娱乐（EN）等标签，覆盖了体积视频重建的关键挑战场景。

![[assets/figures/papers/paper_list_l37_https_arxiv_org_abs_2602_23040/figures/007_Table_3.jpg]]
*Table 3: We present quantitative ablation study for various components of our method on PSNR, SSIM, and LPIPS*

![[assets/figures/papers/paper_list_l37_https_arxiv_org_abs_2602_23040/figures/008_Table_5.jpg]]
*Table 5: Storage comparison with the baselines (30 frames)*

![[assets/figures/papers/paper_list_l37_https_arxiv_org_abs_2602_23040/figures/004_Table_1.jpg]]
*Table 1: Dataset Comparisons. We compare our newly captured dataset PackUV-2B with existing multi-view datasets across sequence count, total frames, camera setup, resolution, maximum FPS, scenario type, and view range. PackUV-2B contains 100 diverse sequences totaling over 2B (billion) high-quality frames, recorded with more than 50 cameras at 1920×1200 resolution. The capture system supports up to 90 FPS, providing high temporal fidelity*

## 定位与知识库关联

### 1. 与现有动态高斯方法的谱系关系

PackUV 的核心定位是**将 4D 体积视频表示为与标准视频编解码器完全兼容的 UV 图集序列**，这一设计使其在方法谱系中处于 3D Gaussian Splatting (3DGS) 动态扩展与流式传输方法的交叉地带。

#### 1.1 相对于变形场方法的差异

现有动态 GS 方法的主流范式是通过变形场建模时域变化。**Deformable3DGS** 和 **4DGS** 在规范空间维护一组静态高斯，再通过 MLP 或 HexPlane 预测每帧的位移和属性偏移；**Grid4D** 进一步引入 4D 分解以提升效率。这些方法的共同瓶颈在于：(1) 变形场容量限制了长序列的表达能力；(2) 输出是逐帧的点云属性，无法直接适配视频编码管线。

PackUV 放弃了变形场范式，转而**直接在 UV 域优化高斯属性**，将时域建模转化为 UV 图集序列的优化问题。这一设计使得每一帧的高斯属性天然组织为结构化 2D 图集，可直接输入 HEVC/FFV1 等标准编解码器。

#### 1.2 相对于流式方法的差异

流式 3DGS 方法（如 **3DGStream**、**ATGS**、**GIFStream**）同样面向长序列重建，但它们通常在 3D 世界坐标下逐帧或分段优化高斯点，输出仍为无序点列表。PackUV 与这些方法的关键区别在于**优化域的改变**：从 3D 点云空间迁移到 UV 图集空间（见 `verified_analysis.method.changed_slots`）。这一改变带来了两个结构性优势：

- **存储紧凑性**：金字塔式打包策略利用深层高斯稀疏性，使 UV 图集分辨率按几何级数递减，而非均匀堆叠。
- **编解码兼容性**：UV 图集序列本身就是标准视频格式，无需额外的量化或格式转换步骤。

在 PackUV-2B 数据集上，PackUV-GS 相较 3DGStream 在 PSNR 上提升 **+4.24 dB**（27.41 vs 23.17），SSIM 从 0.826 提升至 0.842，LPIPS 从 0.33 降至 0.28（Table 2）。这一差距的核心来源是 UV 域直接优化避免了后优化投影的信息损失。

#### 1.3 相对于静态/动态分离方法的差异

**Ex4DGS** 通过显式分离静态背景和动态前景高斯来提升效率。PackUV 的光流引导高斯标记策略（`Algorithm 1`）在思路上与此相近，但实现路径不同：PackUV 利用协方差感知的光流掩码（Eq. 3-4）判定每个高斯是否位于运动区域，并对静态高斯执行梯度冻结（`∇θ_i L → D_i ∇θ_i L`），而非显式维护两套独立的高斯集合。消融实验表明，移除关键帧机制（即失去动态/静态分离和梯度重置能力）会导致 PSNR 从 27.41 骤降至 20.95（Table 3），证实该策略对长程时序一致性的关键作用。

### 2. 核心设计决策的因果链条

PackUV 的性能优势可归因于一条清晰的因果链：

1. **UV 域直接优化**（而非后优化映射）→ 保留几何细节，避免 Figure 6 所示的伪影和细节丢失。
2. **金字塔打包**（而非均匀堆叠）→ 利用遮挡导致的深层稀疏性，在相同存储预算下容纳更多有效高斯。
3. **光流关键帧选择**（而非固定窗口）→ 自适应处理大运动和遮挡，防止梯度爆炸（Figure 8 展示了 ATGS 在此场景下的梯度爆炸问题）。
4. **低精度原地优化 (LPO)**（而非训练后量化）→ 在几乎无质量损失的前提下实现与标准视频编解码器的原生兼容（Figure 5 Left）。

### 3. 适用边界与局限

#### 3.1 已知局限

根据 `verified_analysis.limitations`，PackUV 存在以下适用边界：

- **光流依赖**：光流估计不准确时，运动掩码可能遗漏动态区域或误标静态区域，导致拖尾高斯伪影。这一问题在无纹理区域和极快速运动场景下尤为突出。
- **分辨率-存储权衡**：当前 UV 投影的空间排布仍需较大分辨率以捕捉细节（Figure 6 显示即使 48 层 1K 分辨率仍不足以完全保留细节），限制了存储效率的进一步提升空间。
- **设备兼容性**：当前表示尚不支持直接与 AR/VR 设备集成，端到端的沉浸式 4D 流媒体传输仍需额外适配层。

#### 3.2 边界条件推断

基于方法设计，可推断以下边界条件（需实验验证）：

- **场景类型**：PackUV 的 UV 映射基于球面坐标，对 360° 包围式采集（如 PackUV-2B 的 50+ 相机设置）最为适配。对于前向-facing 或窄基线场景，UV 空间的利用率可能下降。
- **序列长度**：光流关键帧机制理论上支持任意长序列，但关键帧密度过高会增加训练开销。Table 2 报告的窗口长度为 60 时间步，更长序列的实际表现需要进一步验证。

### 4. 开放问题与未来方向

基于 `verified_analysis.open_questions` 和方法分析：

1. **光流鲁棒性提升**：是否可以用可学习的光流模块或基于特征的匹配替代现成的光流估计器，以提升在无纹理和快速运动场景下的时序一致性？
2. **更优的打包映射**：是否存在比金字塔式打包更优的 UV 布局策略（如基于内容自适应的非均匀分辨率分配），以进一步压缩存储？
3. **跨表示泛化**：低精度原地优化 (LPO) 策略能否泛化到其他 GS 变体（如 2DGS、Scaffold-GS），在保持编解码兼容性的同时覆盖更多场景类型？
4. **端到端流媒体**：如何将 PackUV 表示与 AR/VR 设备的解码和渲染管线直接对接，实现从采集到显示的完整 4D 流式传输闭环？

### 5. 知识库定位总结

PackUV 在 4D 体积视频表示领域贡献了一个**编解码原生兼容**的新范式。与现有方法相比，其核心区分度不在于渲染质量的绝对提升（尽管指标全面领先），而在于**首次将 3DGS 的优化过程与视频编码基础设施无缝对接**，消除了传统方法中“优化→量化→编码”的多阶段信息损失。这一设计选择使其在需要流式传输和高效存储的应用场景中具有明确的比较优势，但在光流质量敏感和极端分辨率需求场景下仍需进一步改进。

## 原文 PDF

![[paperPDFs/CVPR_2026/PackUV_Packed_Gaussian_UV_Maps_for_4D_Volumetric_Video.pdf]]
