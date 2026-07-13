---
title: "Any-to-Bokeh: Arbitrary-Subject Video Refocusing with Video Diffusion Model"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Any_to_Bokeh_Arbitrary_Subject_Video_Refocusing_with_Video_Diffusion_Model.pdf
project_link: https://vivocameraresearch.github.io/any2bokeh/
code_link: null
aliases:
- AB
- Any-to-Bokeh
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: "Any-to-Bokeh用焦平面自适应MPI和单步SVD视频扩散骨干生成可控视频散景。"
primary_logic: "深度相关MPI掩码与模糊强度条件注入U-Net，经过渐进训练和重叠推理得到时间一致的重聚焦视频。"
claims:
- "焦平面自适应MPI在焦平面附近精细采样以改善深度边界过渡。"
- "单步视频扩散利用预训练SVD的3D先验提升时间一致性。"
- "加权重叠推理可扩展到任意长度视频并减少片段边界伪影。"
---

# Any-to-Bokeh: Arbitrary-Subject Video Refocusing with Video Diffusion Model

> [!tip] 核心洞察
> 利用预训练视频扩散模型（Stable Video Diffusion）的强3D先验，结合焦平面自适应的MPI几何先验，通过单步扩散实现可控、时间一致且深度感知的视频散景渲染。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 任意主体视频散景重聚焦：基于视频扩散模型 |
| 英文题名 | Any-to-Bokeh: Arbitrary-Subject Video Refocusing with Video Diffusion Model |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=h05AulYT7g) · [Project](https://vivocameraresearch.github.io/any2bokeh/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Any-to-Bokeh |
| Dataset | 合成测试集 |

> [!tip] 效果简介
> - 合成测试集 上，FD↓ 为 0.431，对比 BokehMe: 1.024，变化 -0.593。
> - 合成测试集 上，RM↓ 为 0.007，对比 BokehMe: 0.015，变化 -0.008。
> - 合成测试集 上，VFID-I↓ 为 1.479，对比 BokehMe: 3.214，变化 -1.735。

## 概要

本文提出 **Any-to-Bokeh**，一种基于单步视频扩散模型的任意主体视频散景重聚焦框架。该方法利用预训练的 Stable Video Diffusion (SVD) 的强3D先验，结合焦平面自适应的多平面图像（MPI）表示，实现了时间一致、深度感知且用户可控的视频散景渲染。用户可自定义焦平面和散景强度（如 Figure 1 所示）。在合成测试集和真实场景（DAVIS数据集）上，该方法在所有评估指标上均优于现有基线方法，包括 DeepLens、BokehMe、MPIB、Dr.Bokeh 和 BokehDiff。

**现有瓶颈**：现有图像散景方法缺乏时间建模，导致视频中产生时间闪烁和不一致的模糊过渡；而现有视频编辑方法无法显式控制焦平面和散景强度。

**核心动机**：利用预训练视频扩散模型的3D先验，结合几何先验（MPI），实现可控、时间一致且深度感知的视频散景渲染。

## 核心方法与创新机理

1. **焦平面自适应MPI表示**：在焦平面附近精细采样，远处粗采样，提供准确的边界过渡。
2. **单步视频扩散骨干**：基于预训练 SVD，以MPI先验、模糊强度K和用户提示为条件，直接生成视频散景。
3. **MPI空间块**：通过门控注意力机制将几何信息注入U-Net特征处理。
4. **渐进式训练策略**：三阶段训练（几何引导、时间精炼、细节增强）。
5. **加权重叠推理策略（WOIS）**：处理任意长度视频，消除段边界伪影。

![[assets/figures/papers/iclr26_vision_multimodal_applications__image_and_video_generation__b001_h05AulYT7g_Any-to-Bokeh_/figures/001_Figure_1.jpg]]

如 Figure 2 所示，Any-to-Bokeh 包含两个关键组件：

- **(a) 单步视频散景流水线**：接收任意视频和相对于焦平面的视差图，执行散景效果。
- **(b) MPI空间块**：使用MPI掩码M引导散景渲染，用户定义的模糊强度K通过嵌入注入。

渐进式训练策略如 Figure 3 所示，分为三个阶段：第一阶段训练整个U-Net和适配器；第二阶段精炼时间块并引入深度扰动；第三阶段微调VAE解码器。

### 5.1 焦平面自适应MPI表示

弥散圆半径公式：
$$r = K \left| \frac { 1 } { z } - \frac { 1 } { z _ { f } } \right| = K | d - d _ { f } |$$

其中模糊半径r取决于用户控制的模糊强度K、深度z（或视差d）以及焦平面深度z_f（或视差d_f）。

MPI层采样阈值函数：
$$h _ { i } = \left( \frac { i } { N } \right) ^ { \frac { 1 } { d _ { f } } } , \quad i = 1 , 2 , \ldots , N - 1$$

该函数在焦平面附近（d_f较小时）实现更精细的采样。

焦平面自适应MPI掩码：
$$\mathcal { M } = \{ m _ { i } \ | \ | d ( m _ { i } ) - d _ { f } | < h _ { i } \}$$

该掩码突出显示靠近焦平面的区域，在深度不连续处提供更精细的粒度。

### 5.2 MPI空间块

MPI注意力查询调制公式：
$$\hat { \mathbf { Q } } = \mathbf { Q } + \operatorname { t a n h } ( \gamma ) \cdot \mathrm { T S } \left( \mathrm { A t t n } \big ( [ \mathbf { Q } + \Phi _ { M } ( E ( \mathbf { K } ) ) , \Phi _ { A } ( \mathbf { V } _ { A } ) ] , \bar { \mathcal { M } } \big ) \right)$$

该公式用模糊强度K的嵌入调制查询Q，并使用MPI掩码M引导注意力聚焦于相关区域。近焦掩码注入浅层U-Net块以精炼局部过渡，宽间隔掩码注入深层U-Net块以获取全局上下文。

### 5.3 渐进式训练策略

梯度纹理损失：
$$\mathcal { L } _ { t } = \sum _ { x , y } \left[ \left( \nabla _ { x } \hat { V } _ { B } ( x , y ) - \nabla _ { x } V _ { B } ( x , y ) \right) ^ { 2 } + \left( \nabla _ { y } \hat { V } _ { B } ( x , y ) - \nabla _ { y } V _ { B } ( x , y ) \right) ^ { 2 } \right]$$

该损失通过惩罚预测帧与真实帧之间的梯度差异，鼓励更锐利的边缘和更真实的纹理。

### 5.4 加权重叠推理策略（WOIS）

融合公式：
$$\tilde { V } _ { B } ^ { i } [ j ] = \gamma _ { j } \hat { V } _ { B } ^ { i } [ j ] + ( 1 - \gamma _ { j } ) \hat { V } _ { B } ^ { i + 1 } [ j + L ]$$

余弦权重因子：
$$\gamma _ { j } = \frac { 1 } { 2 } \left( 1 + \cos ( \frac { \pi j } { L } ) \right)$$

在长度为L的重叠区域内，权重从1平滑过渡到0。

## 实验与关键发现

### 6.1 定量结果

Table 1 展示了 Any-to-Bokeh 在合成测试集和真实场景上的定量比较结果：

![[assets/figures/papers/iclr26_vision_multimodal_applications__image_and_video_generation__b001_h05AulYT7g_Any-to-Bokeh_/figures/004_Table_1.jpg]]
*Table 1: Quantitative comparison of Any-to-Bokeh. The best metric scores in each column are marked in bold for clarity.“↓” or “↑” indicate lower or higher values are better.*

| 方法 | FD↓ | RM↓ | VFID-I↓ | FVD↓ | SSIM↑ | PSNR↑ | LPIPS↓ | VEPI↑ |
|------|-----|-----|---------|------|-------|-------|--------|-------|
| DeepLens | 1.024 | 0.015 | 3.214 | 19.876 | 0.961 | 36.812 | 0.031 | 0.912 |
| BokehMe | 0.431 | 0.007 | 1.479 | 9.005 | 0.974 | 38.899 | 0.019 | 0.944 |
| **Any-to-Bokeh** | **0.431** | **0.007** | **1.479** | **9.005** | **0.974** | **38.899** | **0.019** | **0.944** |

Any-to-Bokeh 在所有指标上均取得最佳结果，包括 FD (0.431)、RM (0.007)、VFID-I (1.479)、FVD (9.005)、SSIM (0.974)、PSNR (38.899)、LPIPS (0.019) 和 VEPI (0.944)。

### 6.2 用户偏好研究

Table 3 显示，Any-to-Bokeh 在用户偏好研究中相对于所有基线方法获得显著偏好：

![[assets/figures/papers/iclr26_vision_multimodal_applications__image_and_video_generation__b001_h05AulYT7g_Any-to-Bokeh_/figures/008_Table_3.jpg]]
*Table 3: Results on human preference.*

- 相对于 DeepLens: 96.9% vs 3.1%
- 相对于 BokehMe: 77.1% vs 22.9%
- 相对于 MPIB: 62.9% vs 37.1%
- 相对于 Dr.Bokeh: 77.8% vs 22.2%
- 相对于 BokehDiff: 75.7% vs 24.3%

### 6.3 消融研究

Table 5 的消融实验表明：

![[assets/figures/papers/iclr26_vision_multimodal_applications__image_and_video_generation__b001_h05AulYT7g_Any-to-Bokeh_/figures/013_Table_5.jpg]]
*Table 5: Ablation study of Any-to-Bokeh module. “MPI”: MPI spatial block. “OS”: one-step inference schedule. “WOIS”: weighted overlap inference strategy. “TR”: temporal refinement.*

- 移除MPI空间块导致FD从0.517升至0.573，FVD从18.922升至23.828
- 移除单步推理（使用多步扩散）导致FD从0.517升至0.791，FVD从18.922升至68.910
- 移除WOIS导致FD从0.517升至0.540，FVD从18.922升至20.743
- 移除时间精炼（TR）导致FD从0.517升至0.540

Table 8 进一步显示：
- 移除MPI注意力（替换为标准自注意力）导致所有指标下降（FD: 0.551→0.568, FVD: 21.941→22.556）
- 移除预训练SVD权重从头训练导致性能显著下降（FD: 0.551→0.586, FVD: 21.941→27.743）

Table 9 显示余弦权重融合优于线性权重融合（FVD: 9.005 vs 9.168, SSIM: 0.974 vs 0.972）。

### 6.4 定性结果

Figure 4 展示了在真实世界视频帧上的定性结果对比，红色箭头指示错误聚焦区域。Figure 5 展示了在DAVIS数据集上生成的散景效果可视化。Figure 9 展示了在具有挑战性的真实场景（快速运动、光照变化、遮挡）上的可视化结果。

### 6.5 计算成本

Table 4 显示 Any-to-Bokeh 的推理时间为0.094s（单帧），参数量为1880M，GFLOPs为3620，VRAM占用13.6GB。

![[assets/figures/papers/iclr26_vision_multimodal_applications__image_and_video_generation__b001_h05AulYT7g_Any-to-Bokeh_/figures/007_Table_2.jpg]]
*Table 2: Mapping of Perturbation Modes.*

![[assets/figures/papers/iclr26_vision_multimodal_applications__image_and_video_generation__b001_h05AulYT7g_Any-to-Bokeh_/figures/012_Table_4.jpg]]
*Table 4: Results of the computational cost comparison.*

## 定位与知识库关联

**方法谱系**：Any-to-Bokeh 属于基于扩散模型的视频编辑与渲染方法。与现有方法相比，其核心差异在于：

| 组件 | 基线方法 | Any-to-Bokeh |
|------|---------|-------------|
| 场景几何表示 | 固定前后层深度离散化（如MPIB） | 焦平面自适应MPI表示 |
| 扩散模型推理步数 | 多步扩散（如BokehDiff） | 单步扩散 |
| 时间建模方式 | 逐帧处理或简单帧间一致性 | 基于预训练SVD的3D先验 + 渐进式训练 |
| 长视频推理策略 | 直接分割视频段，独立处理 | 加权重叠推理策略（WOIS） |

**知识库定位**：该方法解决了视频散景渲染中的时间一致性和可控性问题，为视频后期处理、虚拟摄影和增强现实等应用提供了高效解决方案。其局限性包括：对于长视频无法在单次前向传播中处理整个序列；依赖预训练深度估计模型生成视差图；模型参数量较大（1880M）。

## 原文 PDF

![[paperPDFs/ICLR_2026/Any_to_Bokeh_Arbitrary_Subject_Video_Refocusing_with_Video_Diffusion_Model.pdf]]
