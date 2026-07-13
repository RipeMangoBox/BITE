---
title: "VideoPanda: Video Panoramic Diffusion with Multi-view Attention"
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: paperPDFs/arxiv_2025/VideoPanda_Video_Panoramic_Diffusion_with_Multi_view_Attention.pdf
project_link: null
code_link: https://github.com/hpcaitech/Open-Sora
aliases:
- VideoPanda
tags:
- arxiv_2025
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 训练时随机子采样视图数和帧数（随机矩阵策略），结合多视图注意力层和噪声增强，使模型在推理时能泛化到更多视图和更长的时间段，突破训练内存限制并提升生成质量。
primary_logic: 将全景视频生成转化为多视图透视图像的联合生成，通过多视图注意力在帧内不同视图间传播信息，并利用随机子采样训练作为数据增强，使模型保持在预训练视频扩散模型的分布内，避免直接生成等量矩形投影带来的失真和质量下降。
claims:
- 随机矩阵训练相比固定矩阵训练显著提升FVD（916 vs 999），同时改善视觉细节。
- VideoPanda在文本条件全景视频生成上全面超越360DVD，FIDpair降低15%，且在天空/地面区域失真更小。
- 在视频条件生成中，VideoPanda比逐帧外推的MVDiffusion更好地保持全局风格和场景深度，FID降低34.7%。
- 噪声增强训练有效减缓自回归生成中的质量衰减，模型在10次迭代后仍保持合理输出。
---

# VideoPanda: Video Panoramic Diffusion with Multi-view Attention

> [!tip] 核心洞察
> 将全景视频生成转化为多视图透视图像的联合生成，通过多视图注意力在帧内不同视图间传播信息，并利用随机子采样训练作为数据增强，使模型保持在预训练视频扩散模型的分布内，避免直接生成等量矩形投影带来的失真和质量下降。

| 字段 | 内容 |
|------|------|
| 中文题名 | VideoPanda：基于多视图注意力的全景视频扩散模型 |
| 英文题名 | VideoPanda: Video Panoramic Diffusion with Multi-view Attention |
| 会议/期刊 | arXiv 2025 |
| Links | [paper](https://arxiv.org/abs/2504.11389) · [paper](https://arxiv.org/abs/2202.00512) · [Code](https://github.com/hpcaitech/Open-Sora) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | VideoPanda |
| Dataset | WEB360 test set, Out-of-distribution prompts |

> [!tip] 效果简介
> - WEB360 test set (in-distribution) 上，FIDpair (Panorama, equirectangular) 136 vs 160 (360DVD) (-15%)。
> - Out-of-distribution prompts (VBench all dimensions) 上，FID-COCO (Elev. ±60°, 8 views) 93.4 (Ours CogVideoX) vs 128.6 (360DVD) (-27.4%)。
> - WEB360 test set 上，FID (Horizontal 8 views, per-image level) 63.2 vs 96.8 (MVDiffusion) (-34.7%)。

## 概要

全景视频（360°视频）生成面临一个核心瓶颈：**在保持多视图一致性的前提下，高效生成高质量的长全景视频，同时克服全景视频数据稀缺和计算资源限制**。现有方法或直接生成等量矩形投影（equirectangular projection），导致天空和地面区域产生严重失真；或逐帧处理单张全景图，无法维持视频的时间连续性和全局风格一致性。

VideoPanda 提出了一项核心洞察：**将全景视频生成转化为多视图透视图像的联合生成问题**。通过在预训练视频扩散模型中插入多视图注意力层，使不同视角在每一帧内进行信息传播，从而在透视空间而非等量矩形空间中保持多视图一致性。这一设计避免了直接生成等量矩形投影带来的失真，并使模型保持在预训练视频扩散模型的分布内。

方法的关键因果调控手段是**随机子采样训练策略**：训练时随机选择视图数和帧数（如 8×6、6×8、4×12 等矩阵配置），作为一种数据增强形式。这一策略使模型在推理时能够泛化到更多视图和更长的时间段，突破了训练内存限制，同时显著提升了生成质量——消融实验表明，随机矩阵训练相比固定矩阵训练将 FVD 从 999 降至 916（Table 3），并产生了更丰富的高频细节（Figure 7）。

在主要结果上，VideoPanda 展现了全面的优势：
- **文本条件全景视频生成**：在 WEB360 测试集上，FIDpair 降至 136，较基线模型 **360DVD**（Wang et al., 2024a）的 160 降低 15%（Table 1）；在分布外提示下，FID-COCO 降低 27.4%（Table C1）。
- **视频条件全景生成**：相比逐帧外推的 **MVDiffusion**（Tang et al., 2023），VideoPanda 更好地保持了全局风格和场景深度，FID 降低 34.7%（Table 2，Figure 5）。
- **自回归长视频扩展**：通过噪声增强训练，模型在 10 次自回归迭代后仍保持合理输出质量，有效减缓了质量衰减（Figure A3）。

VideoPanda 在方法谱系中定位为**多视图视频扩散模型的统一框架**：它继承了视频潜在扩散模型（VideoLDM）的时空建模能力，引入 MVDream 风格的多视图注意力机制，并通过多任务训练统一了文本条件、视频条件和自回归生成三种模式。该方法可灵活适配不同的基础模型（如 CogVideoX-2B），在保持多视图一致性的同时实现全景视频的高质量生成与扩展。



### 全景视频生成的挑战

360°全景视频的自动生成是计算机视觉与图形学中的一个新兴问题。其核心挑战在于：在保持多视图一致性的前提下，高效生成高质量的全景视频，并支持长视频的自回归扩展。现有的视频生成模型（如VideoLDM、CogVideoX）在透视视频生成上取得了显著进展，但直接将其应用于全景视频生成面临两个根本性困难：

1. **数据稀缺**：全景视频数据极为有限。VideoPanda所使用的WEB360数据集仅包含约2,114个全景视频片段，远不足以从头训练一个大型视频扩散模型。
2. **计算资源限制**：全景视频通常以等量矩形投影（equirectangular projection）表示，分辨率极高且存在严重的几何畸变，直接生成不仅计算开销巨大，还会导致两极区域（天空/地面）的失真和质量下降。

### 现有方法及其缺口

在VideoPanda之前，全景视频生成的代表性工作主要有两类：

- **360DVD**（Wang et al., 2024a）：直接生成等量矩形投影的全景视频。该方法将全景视频视为单一高分辨率视频帧进行处理，但由于等量矩形投影在极区存在严重畸变，生成结果在天空和地面区域容易出现伪影和像素质量下降（见Figure 4、Figure A5）。此外，直接生成高分辨率等量矩形视频对计算资源要求极高。

- **MVDiffusion**（Tang et al., 2023）：采用多视图外推策略，对单帧透视图像逐帧进行全景外推。该方法虽然避免了等量矩形投影的畸变问题，但逐帧独立处理导致视频帧间缺乏时间一致性，难以保持全局风格和场景深度。如Figure 5所示，MVDiffusion生成的天空颜色、物体尺度和深度在帧间不一致。

上述方法的共同缺陷在于：它们无法在**保持多视图一致性的同时，高效利用预训练视频扩散模型的先验知识**。360DVD受限于等量矩形投影的固有畸变，而MVDiffusion则牺牲了时间一致性。

### 本文动机与核心思路

VideoPanda的核心洞察是：**将全景视频生成转化为多视图透视图像的联合生成问题**。具体而言，将等量矩形视频投影为8个透视视图（6个水平90°FOV视图 + 2个天/地100°FOV视图，见Figure 6），然后利用多视图注意力机制在帧内不同视图间传播信息，确保多视图一致性。这一设计使模型能够：

- **保持在预训练视频扩散模型的分布内**：透视视图与预训练模型（如VideoLDM、CogVideoX-2B）的训练数据分布一致，避免了直接生成等量矩形投影带来的分布偏移和失真。
- **通过随机子采样突破训练内存限制**：训练时随机选择视图数和帧数（随机矩阵策略），使模型在推理时能泛化到更多视图和更长的时间段。
- **统一多种条件模式**：通过多任务训练策略（文本条件、视频条件、自回归条件），使单一模型能够处理多种生成任务。

这种设计在因果机制上构成了一个完整的闭环：**训练时的随机子采样（因果旋钮）→ 模型泛化能力的提升 → 推理时高质量全景视频的生成**，从而解决了数据稀缺和计算资源限制下的全景视频生成瓶颈。



## 核心方法与创新机理

VideoPanda 将全景视频生成重新定义为多视图透视图像的联合生成问题，其核心创新在于通过**多视图注意力机制**与**随机子采样训练策略**的组合，在保持多视图一致性的前提下突破计算资源限制，实现高质量 360° 全景视频生成及自回归扩展。

### 从等量矩形到多视图透视的范式转换

现有全景视频生成方法（如 **360DVD**，Wang et al., 2024a）直接生成等量矩形投影（equirectangular projection），这种格式在两极区域存在严重的几何失真，导致天空和地面区域生成质量显著下降。VideoPanda 转而将等量矩形视频投影为 8 个透视视图（6 个水平 90°FOV + 2 个天/地 100°FOV，见 Figure 6），在透视空间中进行联合生成，天然避免了等量矩形格式的失真问题（见 Figure A5）。这一范式转换使生成结果保持在预训练视频扩散模型的分布内，从而充分利用了基础模型的先验知识。

### 多视图注意力：帧内跨视图信息传播

在架构层面，VideoPanda 在预训练视频潜在扩散模型（VideoLDM）的 2D 空间自注意层之后，以残差方式插入**多视图自注意层**（§3.1）。这些多视图注意力层采用零卷积初始化（类似 ControlNet，Zhang et al., 2023），在每一帧的不同视图之间进行自注意运算，使信息能够在同一时刻的 8 个透视视图间自由流动，从而确保全景视频的多视图一致性。同时，模型通过零卷积注入**光线方向嵌入**（ray direction embeddings）作为视图条件，为每个视图提供空间位置信息（Figure 2 中以彩色映射可视化）。

### 随机矩阵训练：突破内存瓶颈的泛化策略

VideoPanda 面临的核心工程瓶颈是训练时的 GPU 内存限制：在 8 个视图配置下，最多只能容纳 6 个时间帧。然而推理时需要生成 16 帧以形成连贯的全景视频。为解决这一矛盾，VideoPanda 提出**随机矩阵训练策略**（§3.2, §4.7）：训练时随机子采样视图数×帧数的组合（如 8×6, 6×8, 4×12 等），使模型学会在不同视图-帧配置下进行生成。这一策略本质上是一种数据增强，使模型在推理时能够泛化到训练时未见过的 8×16 配置。

消融实验（Table 3, Figure 7）证实，随机矩阵训练相比固定矩阵训练显著改善视频质量：FVD 从 999 降至 916，且生成的高频细节更为丰富。这一改进的因果机制在于：随机子采样迫使模型学习更鲁棒的多视图-时序联合分布，而非过拟合于特定的视图-帧组合。

### 多任务条件统一与噪声增强

VideoPanda 通过随机二元掩码将三种条件模式统一到单一模型中（Figure 3）：纯文本条件（全零掩码）、单视图视频条件（首列掩码为 1）、以及自回归条件（首行和首列均为 1）。三种模式以等概率采样训练，使一个统一模型同时支持文本到全景视频、视频条件外推和自回归长视频生成。消融实验（Table 3）表明，多任务训练引入的性能损失可忽略不计，同时赋予模型更强的泛化能力（Figure 8）。

为支持自回归生成中的误差累积控制，VideoPanda 对条件帧施加**噪声增强**（§3.1, §A.3）：向条件帧添加小量噪声并传入噪声水平 σ，使模型学会从带噪条件中恢复。消融实验（Figure A3）显示，缺乏噪声增强时自回归生成质量迅速退化（色彩饱和度过高），而使用噪声增强后退化更为平缓，模型在 10 次迭代后仍保持合理输出。

### 关键设计选择的因果链条

此外，VideoPanda 在噪声调度和预测参数化上做出两项关键调整（§3.1, §A.2）：将噪声调度向高噪声水平偏移，并采用 v-预测替代标准 ε-预测。消融实验（Figure A2）表明，偏移噪声调度是生成清晰天空、水面等平滑区域的关键——若不偏移，模型倾向于在这些区域填充杂乱物体（如突然出现的山脉和岩石），破坏场景整体性。

综合来看，VideoPanda 的创新链条可概括为：**多视图透视投影**避免等量矩形失真 → **多视图注意力**确保帧内视图一致性 → **随机矩阵训练**突破内存限制并提升泛化能力 → **多任务统一条件**赋予模型多模式生成能力 → **噪声增强与噪声调度偏移**保障自回归长视频生成质量。这一系列设计使 VideoPanda 在文本条件生成上 FIDpair 较 360DVD 降低 15%（Table 1），在视频条件生成上 FID 较 MVDiffusion 降低 34.7%（Table 2）。



VideoPanda 将 360° 全景视频生成重新定义为**多视图透视图像的联合生成**问题。其核心 pipeline 由三个关键阶段串联而成：投影分解 → 多视图视频扩散 → 全景拼接。

### 输入输出流

模型接受两类条件输入：
- **文本条件**：自然语言描述，经 CLIP 文本编码器注入扩散模型。
- **视频条件**：单视角透视视频，作为条件帧输入模型，驱动全景外推。

输出为 8 个视角的透视视频帧，经后处理拼接为等量矩形（equirectangular）全景视频。在自回归模式下，模型以滑动窗口方式逐段生成长视频，每次生成 16 帧，以上一段最后一帧的 8 个视图作为下一段的条件输入（Figure 3）。

### 模块拓扑与数据流

整个扩散模型基于预训练视频潜在扩散模型（VideoLDM 或 CogVideoX-2B）构建，在 U-Net 的去噪路径中插入了专用模块。数据流沿以下路径传递：

1. **VAE 编码**：每个 512×512 的透视视图被编码为 64×64×4 的潜在表示。
2. **视图条件注入**：光线方向嵌入（ray direction embedding）通过零卷积（zero-initialized convolution）与潜在表示在通道维度级联，为模型提供每个视图的空间方位信息。
3. **条件掩码**：二元掩码在通道维度与潜在表示级联，标记哪些帧/视图是已知条件、哪些需要预测。训练时掩码被随机化以覆盖三种条件模式（纯文本、首视图视频条件、首帧+首视图自回归条件）。
4. **交错注意力块**：潜在表示依次经过三类注意力层（Figure 2）：
   - **2D 空间自注意**：处理单帧内的空间结构（继承自预训练基础模型，训练时可冻结以保留先验）。
   - **多视图自注意**：在每一帧的不同视图之间传播信息，以残差方式与 2D 自注意结合，用零卷积初始化以保护预训练权重。
   - **时间自注意**：沿时间轴建模运动一致性。
5. **噪声增强**：条件帧在输入扩散模型前被施加少量噪声，同时传入噪声水平 σ，以提升对条件误差的鲁棒性并支持自回归扩展。
6. **去噪与解码**：扩散模型以 v-预测参数化、向高噪声水平偏移的噪声调度进行去噪，生成 8 个视图的潜在表示，经 VAE 解码为透视图像。

![[assets/figures/papers/paper_list_l79_https_arxiv_org_abs_2504_11389/figures/002_Figure_2.jpg]]
*Figure 2: We divide the equi-rectangular video into 8 perspective views via projection. Our diffusion model consists of interleaved spatial, multi-view, and temporal blocks, conditioned on text prompts. Attention is used to propagate information through the multi-view videos to ensure consistency. The input views are embedded using the ray directions as visualized by the color map behind the perspective images*

### 训练时的随机矩阵策略

训练阶段内存限制最多容纳 8 视图 × 6 帧的矩阵。为支持推理时扩展到 16 帧或更多视图，VideoPanda 采用**随机子采样训练**：每次迭代随机选择视图数（如 4、6、8）和帧数（如 6、8、12），构成不同的视图×帧矩阵进行训练。这一策略作为数据增强，使模型学会泛化到训练时未见过的矩阵配置，是实现长视频自回归生成的关键机制。

### 推理与拼接

推理时，模型生成 8 个透视视图的视频帧，通过双三次插值将各视图 warp 到等量矩形全景坐标，重叠区域像素值均匀平均，最终拼接为无缝全景视频。由于模型原生生成透视视图而非直接生成等量矩形投影，有效避免了传统方法在天空/地面区域的高畸变问题（Figure A5）。



### 整体架构：从等量矩形到多视图潜在空间

VideoPanda 的核心设计思路是将全景视频生成转化为**多视图透视图像的联合生成**。如图 Figure 2 所示，模型首先将等量矩形（equirectangular）视频投影为 8 个透视视图（6 个水平 90°FOV 视图 + 2 个天/地 100°FOV 视图），然后通过 VAE 编码器将每个 512×512 的视图图像压缩至 64×64×4 的潜在表示。这一投影-编码流水线使模型始终在透视图像的分布内运行，从根本上规避了直接生成等量矩形投影带来的两极失真问题（见 Figure A5 的定性对比）。

扩散模型的主干由**空间-多视图-时间交错模块**构成，其处理流程为：每个视频帧先经过 2D 空间自注意层处理帧内信息，随后进入多视图自注意层在帧内不同视图间传播信息，最后通过时间自注意层建模运动一致性。文本条件通过交叉注意力注入，视图方向信息则通过光线方向嵌入（ray direction embedding）与潜在表示通道级联后经零卷积（zero-convolution）注入。

### 多视图注意力层：一致性的关键机制

多视图自注意层是 VideoPanda 区别于普通视频扩散模型的核心模块。该层在 2D 空间自注意层之后以**残差方式**插入，并通过零初始化卷积（zero-initialized convolutions）与原有特征结合，这一设计借鉴了 ControlNet 的思路，确保训练初期多视图注意力不会破坏预训练基础模型的先验。

具体而言，对于每一帧 $t$，其 $N$ 个视图的潜在表示被拼接为一个序列，多视图自注意力在该序列上计算：

$$ \text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V $$

其中 $Q, K, V$ 均来自同一帧内所有视图的拼接特征。这使得每个视图的每个空间位置都能直接关注同一帧内其他视图的对应区域，从而在生成过程中传播全局结构和风格信息。与逐帧独立外推的 MVDiffusion 相比，这一机制是 VideoPanda 在视频条件生成中 FID 降低 34.7%（Table 2）且能保持天空颜色和物体尺度一致性的根本原因（Figure 5）。

### 视图条件注入：光线方向嵌入

为了显式告知模型每个视图在全景球面上的位置，VideoPanda 为每个视图注入其对应的**光线方向嵌入**。该嵌入编码了视图的相机方向（方位角和仰角），通过零卷积与 VAE 编码后的潜在表示进行通道级联。Figure 2 中以彩色图可视化了各视图对应的光线方向（不同颜色表示不同朝向），这一条件信号使模型能够区分水平环视视图与天/地视图，并在多视图注意力中建立正确的空间对应关系。

### 噪声调度偏移与 v-预测

VideoPanda 对标准扩散模型的噪声调度和参数化做了两处关键调整：

1. **向高噪声水平偏移的噪声调度**：消融实验（Figure A2）表明，若不将噪声调度向高噪声水平偏移，模型在生成天空、水面等平滑区域时会填充杂乱物体（如突然出现的山脉和岩石）。偏移后的调度使模型在高噪声阶段获得更强的去噪能力，从而在平滑区域产生更清晰的生成结果。

![[assets/figures/papers/paper_list_l79_https_arxiv_org_abs_2504_11389/figures/013_Figure.jpg]]
*Figure: A2: Qualitative comparison of shifting the noise schedule in the video-conditioned setting. Each of the six horizontal views is visualized independently before stitching into a panorama. Without shifting toward higher noise levels, the model struggles to generate clear skies or water, introducing objects that disrupt scene cohesion (e.g., sudden mountains and rocks)*

2. **v-预测参数化**：模型采用 v-预测（velocity prediction）替代标准的 ϵ-预测。v-预测在高噪声水平下数值更稳定，与偏移后的噪声调度配合使用，共同保障了全景视频中大面积均匀区域的生成质量。

### 训练子采样：随机矩阵策略

VideoPanda 在训练时面临内存限制：最多只能容纳 6 个时间帧 × 8 个视图的矩阵（共 48 个视图-帧单元），但推理时期望生成 16 帧视频。为解决这一训练-推理不匹配，模型采用**随机矩阵子采样策略**：训练时从 8 个视图中随机选择 $V$ 个视图、从视频片段中随机选择 $T$ 个帧，构成 $V \times T$ 的子矩阵，其中 $(V, T)$ 的组合如 (8,6), (6,8), (4,12) 等被随机采样。

这一策略本质上是一种**数据增强**：模型在训练期间见过不同的视图-帧组合，从而在推理时能够泛化到训练期间未见过的更大矩阵（如 8×16）。消融实验（Table 3）证实，随机矩阵训练相比固定矩阵训练显著改善视频质量（FVD 从 999 降至 916），且生成更多高频细节（Figure 7），尽管颜色一致性指标 PSNR 略有下降。

### 多任务条件机制与噪声增强

VideoPanda 通过**随机二元掩码**统一了三种条件模式（Figure 3）：
- **文本条件生成**：掩码全为零，初始输入为纯噪声；
- **视频条件生成**：掩码第一列（第一个视图的所有帧）为 1，其余为零；
- **自回归生成**：掩码第一行（第一帧的所有视图）和第一列均为 1。

![[assets/figures/papers/paper_list_l79_https_arxiv_org_abs_2504_11389/figures/003_Figure_3.jpg]]
*Figure 3: The model is trained using three frame conditioning regimes. (a) No image conditions and the initial inputs are pure noise; (b) Conditioning only on the first view of the video; (c) Conditioning on the first frame and first views for auto-regressive video generation. At inference time, we autoregressively condition on long videos by using conditioning (b) to generate the first window and subsequently using the last multi-view images row from the previous time step (the shaded region) as the first row input to our model using condition-type (c)*

三种模式在训练中以等概率随机采样，使单一模型能同时处理所有任务。Table 3 的消融表明，多任务训练引入的性能损失可忽略不计（各指标接近单任务模型），同时使模型获得了处理多种输入模式的灵活性。

为支持自回归长视频生成，模型对条件帧施加**噪声增强**：在条件帧的潜在表示上添加小量噪声，并将噪声水平 $\sigma$ 作为额外条件输入。消融实验（Figure A3）显示，缺乏噪声增强时自回归生成的质量迅速退化（色彩饱和度过高），而使用噪声增强后退化更为平缓，模型在 10 次自回归迭代后仍能保持合理输出。

![[assets/figures/papers/paper_list_l79_https_arxiv_org_abs_2504_11389/figures/014_Figure.jpg]]
*Figure: A3: Qualitative comparison of autoregressive generation with and without noise augmentation. Both models exhibit a decline in output quality over time, but the model trained without noise augmentation shows a more rapid and severe degradation, with frames becoming increasingly saturated. In contrast, the model with noise augmentation deteriorates more gradually*

### 条件机制设计选择

在条件输入的具体实现上，VideoPanda 采用**CAT3D 风格的条件机制**（直接通道级联条件帧），而非 IP Adapter 的交叉注意力方式。消融实验（Figure A1）表明，IP Adapter 在条件视图与相邻视图之间的一致性较差（红色框标注区域），而直接通道级联能更好地保持输入条件与生成视图之间的连续性。这一选择对于视频条件生成和自回归扩展至关重要，因为相邻窗口之间的无缝过渡依赖于条件信息在空间上的精确传播。

![[assets/figures/papers/paper_list_l79_https_arxiv_org_abs_2504_11389/figures/012_Figure.jpg]]
*Figure: A1: Qualitative figure comparing IP vs CAT type architecture for input conditioning. When using IP adapter, the consistency between input conditioning views and neighbouring views (highlighted in red box) is worse compare to CAT*

### 补充图表

![[assets/figures/papers/paper_list_l79_https_arxiv_org_abs_2504_11389/figures/006_Figure_6.jpg]]
*Figure 6: A visualization of the 8 frames used during training, consisting of 6 horizontal views with 90 FOV and 2 views for the top/bottom with 100 FOV*



## 实验与关键发现

### 实验设置

VideoPanda的训练数据为**WEB360数据集**，包含2114个全景视频片段，主要涵盖室外平移拍摄场景。评测时，分布内测试集为来自YouTube的100个未见全景视频片段；分布外评测则使用VBench All Dimensions的946条文本提示进行泛化能力评估。所有对比方法均在相同的WEB360数据集上训练，生成结果统一转换为等量矩形投影（equirectangular）格式以保证公平对比。

推理时，文本条件生成采用无分类器引导（CFG）尺度7.5；视频条件生成使用CFG尺度4.0，其中无条件分数预测不接收文本或视频输入。多视图结果通过双三次插值扭曲至等量矩形格式，视图重叠区域的像素值采用均匀平均融合。

### 文本条件全景视频生成

表1展示了文本条件全景视频生成的定量对比。VideoPanda在等量矩形全景指标**FIDpair**上达到136，较基线**360DVD**（Wang et al., 2024a）的160降低15%，同时在PSNR、SSIM和LPIPS上全面领先。

在分布外文本提示的泛化测试中（Table C1），VideoPanda的**FID-COCO**降至93.4（CogVideoX基座），相比360DVD的128.6降低27.4%，表明多视图透视生成策略天然避免了等量矩形投影在两极区域的失真问题。定性对比（Figure A5）进一步揭示：360DVD在天空和地面区域因投影畸变最大而填充杂乱伪影，而VideoPanda天然生成透视视图，拼接后在这些区域保持清晰合理的内容。

![[assets/figures/papers/paper_list_l79_https_arxiv_org_abs_2504_11389/figures/016_Figure.jpg]]
*Figure: A5: Qualitative figure comparing text conditional video generation, 360DVD VS ours and highlighting the distortion in 360DVD near the poles. Note that both generations were first transformed to the same equirectangular format before consistent sky and ground views were extracted. 360DVD struggles in these views as the distortion is highest here and deviates the most from perspective view images whereas we natively generate perspective views*

### 视频条件全景视频生成

表2展示了单视图视频条件全景生成的定量对比。VideoPanda在水平8视图的逐图像**FID**上达到63.2，较逐帧外推方法**MVDiffusion**（Tang et al., 2023）的96.8降低34.7%，PSNR和SSIM同样显著占优。

定性对比（Figure 5）揭示了更深层的差异：MVDiffusion对每一帧独立进行外推，无法维护全局风格和场景深度的一致性——天空颜色漂移、物体尺度和深度关系错乱。VideoPanda通过多视图注意力在帧内不同视图间传播信息，保持了全局结构和风格的一致性。

![[assets/figures/papers/paper_list_l79_https_arxiv_org_abs_2504_11389/figures/005_Figure_5.jpg]]
*Figure 5: Qualitative figure comparing video conditional generation, MVDiffusion VS ours. Note that MVDiffusion can only outpaint each frame of the video separately. MVDiffusion is worse at maintaining the structure and style of the input view globally compared to ours. For example the sky color and the scales and depths of objects is less consistent for MVDiffusion*

### 消融实验

#### 随机矩阵训练 vs. 固定矩阵训练

训练阶段因内存限制最多容纳6个时间帧×8个视图，但推理时需生成16帧。随机矩阵训练策略（训练时随机子采样视图数和帧数组合，如8×6、6×8、4×12等）作为数据增强，使模型在推理时能泛化到更多视图和更长时段。

表3的消融结果显示：随机矩阵训练的**FVD**为916，固定矩阵训练为999，降低8.3%；FID同样显著改善。定性对比（Figure 7）表明随机矩阵训练生成了更丰富的高频细节。代价是颜色一致性指标PSNR略有下降，这是视频质量与像素级颜色保真度之间的合理权衡。

![[assets/figures/papers/paper_list_l79_https_arxiv_org_abs_2504_11389/figures/010_Figure_7.jpg]]
*Figure 7: Qualitative figure comparing full matrix and random matrix training. Random matrix training generates more high frequency details*

#### 多任务训练的影响

多任务训练统一了文本条件、视频条件和自回归条件三种模式（通过随机二元掩码以均等概率切换），使单一模型能处理多种生成任务。表3显示，多任务模型相比单任务视频条件模型的性能损失可忽略（各指标接近），同时获得了多模式能力。在分布外视频上，多任务训练甚至提供了更好的像素质量（Figure 8）。

#### 噪声增强对自回归生成的关键作用

自回归生成长视频时，模型以前一步生成的最后一帧多视图图像作为条件生成下一个窗口。缺乏噪声增强训练时，质量迅速退化——帧间色彩饱和度过高，输出在数次迭代后即崩溃。引入噪声增强（对条件帧施加小量噪声并传入噪声水平σ）后，模型在10次自回归迭代后仍保持合理输出，退化过程更为平缓（Figure A3）。这一机制对长视频扩展至关重要，但帧间闪烁问题尚未完全解决。

#### 噪声调度偏移

将噪声调度向高噪声水平偏移是生成清晰天空、水面等平滑区域的关键。若不进行偏移，模型倾向于在这些区域填充杂乱物体（如突兀的山脉和岩石），破坏场景一致性（Figure A2）。这一设计选择与v-预测参数化配合，有效抑制了低纹理区域的伪影生成。

#### 基础模型层冻结

在训练时冻结预训练视频扩散模型的空间层有助于保留先验知识。在分布外文本提示下，冻结策略产生的生成结果更为合理，而未冻结模型则可能出现内容退化（Figure A4）。这验证了多视图注意力作为残差扩展的设计合理性——基础模型能力得以保留，新增模块仅负责多视图一致性建模。

#### 条件机制选择

采用CAT3D风格的条件机制（将条件帧直接通道级联输入）相比IP Adapter能更好地保持输入条件与相邻视图之间的连续性（Figure A1）。IP Adapter在条件视图与邻近视图之间产生了明显的不一致性（红色框标注区域），而直接输入方式维持了空间连续性。

### 失败模式与局限性

1. **自回归质量衰减**：尽管噪声增强减缓了退化速度，但长视频自回归生成中质量随时间逐渐下降，帧间闪烁问题尚未解决。
2. **数据覆盖有限**：模型仅在约3小时的WEB360全景视频上训练，内容以室外平移拍摄为主，对复杂动态场景和室内环境的泛化能力未知。
3. **视图配置刚性**：8个视角的固定FOV布局需用户预定义，无法根据输入条件自动调整，且不支持相机内参变化——要求输入视图具有相同的FOV和水平方向。
4. **计算开销**：多视图注意力层虽然提升了跨视图一致性，但增加了显著的计算负担，可能影响高效推理和实时应用场景。

### 补充图表

![[assets/figures/papers/paper_list_l79_https_arxiv_org_abs_2504_11389/figures/007_Table_1.jpg]]
*Table 1: Quantitative comparison for text-conditional panorama video generation*

![[assets/figures/papers/paper_list_l79_https_arxiv_org_abs_2504_11389/figures/008_Table_2.jpg]]
*Table 2: Quantitative comparison of single view video-conditional panorama generation with image panorama outpainting method MVDiffusion. We extract the middle frame from our 16 frame generations to compare at a per image level*

![[assets/figures/papers/paper_list_l79_https_arxiv_org_abs_2504_11389/figures/009_Table_3.jpg]]
*Table 3: Quantitative ablations of our model on single view video-conditional panoramic video generation. Training our model to be multi-task capable incurs a negligible drop in performance. Randomizing the matrix of frames during training results in much improved video quality at a slightly worse color consistency as measured by PSNR*



## 定位与知识库关联

### 与基线方法的关系

VideoPanda 的全景视频生成范式与现有工作形成两条不同的技术路径。基线方法 **360DVD**（Wang et al., 2024a）直接在等量矩形投影（equirectangular projection）上训练视频扩散模型，其根本缺陷在于：等量矩形格式在天空和地面区域存在严重的几何畸变，这些区域的像素分布与透视图像显著偏离，导致模型生成的纹理模糊且物体杂乱（见 Figure A5）。VideoPanda 通过将全景视频分解为 8 个透视视图（6 个水平 90° FOV 视图 + 2 个天/地 100° FOV 视图，Figure 6），使生成始终保持在预训练视频扩散模型所熟悉的透视分布内，从而从因果机制上避免了畸变区域的生成困难。定量上，在 WEB360 测试集上，VideoPanda 的 FIDpair 较 360DVD 降低 15%（136 vs 160，Table 1），在分布外 VBench 提示上的 FID-COCO 差距更大（93.4 vs 128.6，Table C1），印证了透视分解策略对泛化能力的增益。

另一条基线路径是以 **MVDiffusion**（Tang et al., 2023）为代表的逐帧图像外推方法。MVDiffusion 对视频的每一帧独立进行全景外推，缺乏跨帧的时间一致性约束，导致生成结果在全局风格、天空颜色、物体尺度和场景深度上出现帧间不一致（Figure 5）。VideoPanda 通过在视频潜在扩散模型的时空注意力层之间插入多视图自注意力层，使不同视图的信息在每一帧内相互传播，同时时间注意力层维护跨帧运动一致性，从而在统一的时空-多视图联合生成框架下解决该问题。在视频条件生成任务上，VideoPanda 的 FID 较 MVDiffusion 降低 34.7%（63.2 vs 96.8，Table 2），且定性结果显示出更好的全局结构和风格保持能力。

### 核心设计决策的因果机制

VideoPanda 的关键技术决策可从因果角度归纳为以下链条：

1. **多视图注意力 + 视图条件注入**：在 2D 空间自注意层之后以残差方式插入多视图自注意层（零卷积初始化，类似 ControlNet 的注入策略），同时通过零卷积将光线方向嵌入与潜在表示通道级联。这一设计使模型在不破坏预训练 VideoLDM 权重的前提下，逐步学习跨视图的一致性传播。多视图注意力是帧内不同视角间信息交换的瓶颈机制，而视图嵌入为每个视图提供了空间身份标识。

2. **随机矩阵训练策略**：训练时随机子采样“视图数 × 帧数”的组合（如 8×6、6×8、4×12 等），使模型在内存受限（最大仅能容纳 6 帧 × 8 视图）的条件下，学习到不同时空配置下的生成能力。消融实验表明，随机矩阵训练相比固定矩阵训练将 FVD 从 999 降至 916（Table 3），并产生更丰富的高频细节（Figure 7）。这一策略的关键因果效应在于：它作为一种隐式的数据增强，使推理时能够泛化到训练中未见过的 16 帧配置，从而突破内存瓶颈。

3. **噪声调度偏移 + v-预测**：将噪声调度向更高噪声水平偏移，并采用 v-预测参数化。消融显示，若不进行此偏移，模型在天空、水面等平滑区域倾向于填充杂乱物体（如突然出现的山脉和岩石，Figure A2），因为标准噪声调度下模型对低信号区域的去噪能力不足。偏移噪声调度使模型在生成大面积均匀区域时更加“谨慎”，从而产生清晰的天空和水面。

4. **噪声增强训练**：对条件帧施加少量噪声并传入噪声水平 σ。这一设计对自回归生成长视频至关重要：缺乏噪声增强时，自回归迭代中的误差累积导致色彩饱和度迅速升高、质量急剧退化；而噪声增强训练使退化过程显著减缓（Figure A3），在 10 次自回归迭代后仍保持合理输出。这与先前视频生成工作中的稳定性策略一致。

5. **多任务统一条件机制**：通过随机二元掩码以均等概率切换三种条件模式——纯文本条件（全零掩码）、视频条件（仅第一列视图为条件）、自回归条件（第一行和第一列均为条件，Figure 3）。消融表明，多任务训练引入的性能损失可忽略（Table 3），同时使单一模型能够处理文本生成、视频条件生成和自回归扩展三种任务，并在分布外视频上展现出更好的像素质量（Figure 8）。

### 适用边界

**数据域边界**：模型仅在 WEB360 数据集上训练，该数据集包含约 2,114 个全景视频片段，内容以室外平移拍摄为主。因此，模型对室内环境、复杂动态场景（如人群、交通）、以及非平移相机运动的泛化能力未经检验，需要手动验证。

**输入约束**：
- 视图配置（8 个视角、固定 FOV）需由用户预先定义，无法根据输入条件自动调整。
- 要求条件输入视图具有相同的 FOV 和水平方向；对于非水平拍摄或不同 FOV 的输入视频，模型无法直接处理。
- 不支持相机内参变化，限制了在任意相机姿态下的应用。

**计算开销**：多视图注意力层虽然通过残差方式插入以降低对预训练权重的干扰，但其计算复杂度随视图数平方增长，在推理效率和实时应用场景中存在瓶颈。

### 局限与开放问题

**自回归质量衰减**：尽管噪声增强训练缓解了饱和度升高的问题，但自回归生成长视频时，帧间闪烁（flickering）问题尚未完全解决。如何设计动态噪声增强策略，在减少自回归模糊的同时避免帧间闪烁，是一个待解决的核心问题。

**条件灵活性不足**：当前模型无法估计条件输入的视场角和仰角，需要用户手动指定与训练配置一致的视图布局。放宽这一约束——即允许模型自动估计或适应任意输入视角——是提升实用性的关键方向。

**数据覆盖有限**：WEB360 数据集仅约 3 小时的视频内容，且场景类型单一。扩展到更多样化的全景视频数据（包括室内、动态场景、不同拍摄设备）是提升泛化能力的必要条件，但全景视频数据的采集和标注本身仍是领域瓶颈。

**计算效率与一致性的权衡**：多视图注意力是维持跨视图一致性的核心机制，但其计算开销限制了视图数量的扩展和推理速度。如何在保持多视图一致性的前提下降低注意力计算成本（例如通过稀疏注意力或视图间信息压缩），是一个具有实际价值的研究问题。

**长视频自回归的时空一致性**：在自回归扩展中，需要同时维持窗口内的时间一致性和窗口间的空间一致性。当前方法通过将前一窗口的最后一行多视图图像作为条件传递给下一窗口（Figure 3c），但这一机制在更长的时间跨度下可能累积空间偏移。如何有效平衡图像质量、时间一致性和空间一致性三者之间的关系，仍需进一步探索。



## 原文 PDF

![[paperPDFs/arxiv_2025/VideoPanda_Video_Panoramic_Diffusion_with_Multi_view_Attention.pdf]]
