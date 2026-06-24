---
title: "FreqEdit: Preserving High-Frequency Features for Robust Multi-Turn Image Editing"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/FreqEdit_Preserving_High_Frequency_Features_for_Robust_Multi_Turn_Image_Editing.pdf
project_link: "https://freqedit.github.io/"
code_link: null
aliases:
- FreqEdit
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/representation_self_supervised_transfer
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 从当前上下文图像（即本轮编辑的输入）构造参考速度场，并通过小波变换将其高频成分注入到编辑速度场中，以补偿高频信息的丢失。注入强度、空间自适应性和轨迹补偿共同构成了这一控制机制。
primary_logic: 上下文图像自身蕴含丰富的高频细节，如果在去噪早期将这些细节「借给」生成过程，就可以在不破坏编辑目标的前提下为多轮编辑提供稳定的几何与纹理锚点。小波分解使我们可以分离并融合不同尺度的特征，从而精确控制编辑与保留的平衡。
claims:
- 对源图施加双边滤波或锐化掩模扰动高频成分，会使主体变形提前到第三轮编辑，证实高频完整性对保持主体身份至关重要。
- 仅注入高频特征即可防止主体变形，而注入全部成分或仅注入低频成分会导致编辑失败或主体变形，说明高频成分是关键因果因素。
- 去掉自适应注入策略后，模型无法执行背景变换等复杂语义编辑；移除路径补偿则会产生幽灵伪影。
- Multi-turn editing (70 images × 10 turns) 上 CLIP-I (Turn10, higher is better) = 0.884 (FLUX.1 Kontext + FreqEdit)
---

# FreqEdit: Preserving High-Frequency Features for Robust Multi-Turn Image Editing

> [!tip] 核心洞察
> 上下文图像自身蕴含丰富的高频细节，如果在去噪早期将这些细节「借给」生成过程，就可以在不破坏编辑目标的前提下为多轮编辑提供稳定的几何与纹理锚点。小波分解使我们可以分离并融合不同尺度的特征，从而精确控制编辑与保留的平衡。

| 字段 | 内容 |
|------|------|
| 中文题名 | FreqEdit：保留高频特征以实现鲁棒的多轮图像编辑 |
| 英文题名 | FreqEdit: Preserving High-Frequency Features for Robust Multi-Turn Image Editing |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.01755) · [Project](https://freqedit.github.io/) |
| Topic | #topic/vision_multimodal_applications #topic/representation_self_supervised_transfer #topic/vision_multimodal_applications/image_and_video_generation |
| Method | FreqEdit |
| Dataset | Multi-turn editing |

> [!tip] 效果简介
> - Multi-turn editing (70 images × 10 turns) 上，CLIP-I (Turn10, higher is better) 0.884 (FLUX.1 Kontext + FreqEdit) vs 0.854 (FLUX.1 Kontext) (+0.030)；LPIPS (Turn10, lower is better) 0.418 (FLUX.1 Kontext + FreqEdit) vs 0.546 (FLUX.1 Kontext, approx.) (-0.128)；Instruction Following (Instr., average/turn10) 0.790 (FLUX.1 Kontext + FreqEdit) vs 0.803 (FLUX.1 Kontext) (-0.013)。

## 概述

多轮图像编辑（multi-turn image editing）的核心瓶颈在于**高频信息的渐进性丢失**：随着编辑轮次增加，模型生成的主体出现变形、边缘过度锐化和纹理塌缩。这一退化的根源在于早期去噪步骤优先恢复低频全局结构，高频细节被持续抑制，累积误差使生成轨迹趋向训练数据中的平均化表示。FreqEdit 通过受控实验证实了该因果链条——对源图施加双边滤波或锐化掩模扰动高频成分后，主体变形提前至第三轮编辑（Figure 2），说明高频完整性是维持主体身份的关键。

FreqEdit 的核心洞察是：**上下文图像（即本轮编辑的输入）自身蕴含丰富的高频细节**，若在去噪早期将这些细节“借给”生成过程，就能在不破坏编辑目标的前提下为多轮编辑提供稳定的几何与纹理锚点。小波分解使这一分离-融合操作成为可能：从上下文图像构造参考速度场 $v^{\mathrm{ref}}$，通过二维离散小波变换（2-level DWT）提取其多尺度高频成分，再以空间自适应的强度注入编辑速度场 $v^{\mathrm{edit}}$，最终经逆小波变换（IDWT）重建校正速度场 $v^{\mathrm{corr}}$。

FreqEdit 是一种**无训练（training-free）框架**，可即插即用于基于整流流（rectified flow）的图像编辑模型。在 FLUX.1-Kontext-dev 上，FreqEdit 将 10 轮编辑后的主体一致性（CLIP-I）从 0.854 提升至 **0.884**，LPIPS 从约 0.546 降至 **0.418**，同时指令遵循能力仅轻微下降（0.803 → 0.790），在编辑灵活性与身份保持之间取得了显著更优的平衡。定性对比（Figure 5）表明，FreqEdit 优于 FLUX.1 Kontext、Qwen-Image、Seedream 4.0、Nano Banana、MTC、VINCIE 和 Bagel 等方法。消融实验进一步确认：仅注入高频成分即可防止主体变形，而注入全部成分或仅注入低频成分则导致编辑失败或语义泄漏（Figure 6d），证实高频是关键因果因素；移除自适应注入策略会导致复杂语义编辑（如背景替换）失败（Figure 6a），移除路径补偿则引入幽灵伪影（Figure 6b）。

FreqEdit 的主要局限包括：对源图像高频细节的依赖（低质量输入效果受限）、大面积编辑时自适应注入图判别力下降，以及推理时修改速度场可能使轨迹偏离训练分布。尽管如此，其无训练特性为未来将高频保持原则融入训练损失、或扩展至视频等多模态编辑提供了可迁移的基础思路。

## 背景与动机

图像编辑模型正经历从单轮指令执行到多轮交互式迭代编辑的范式跃迁。在单轮场景中，用户给定一张源图像与一条编辑指令，模型输出修改后的图像；而在多轮编辑中，用户持续对上一轮的输出追加新指令，逐步塑造图像内容。这种迭代式工作流更贴近真实创作过程，但也暴露了现有模型的一个深层脆弱性：**图像质量随编辑轮次增加而持续退化**。

具体而言，主流编辑模型（如 **FLUX.1-Kontext-dev**、**Qwen-Image**、**Seedream 4.0**、**Nano Banana** 等）在多轮编辑中会系统性地出现三类退化现象：**主体变形**（人物或物体的几何结构逐渐偏离原始身份）、**边缘过度锐化**（轮廓出现不自然的高对比度伪影）和**纹理塌缩**（细节区域变得模糊且缺乏真实感）。Figure 1 直观展示了这一退化过程：基础模型在迭代编辑中逐步丧失视觉保真度，而本文提出的 FreqEdit 则有效抑制了这种退化。

### 退化根源：高频信息的渐进性丢失

本文通过受控消融实验定位了退化的因果瓶颈。如 Figure 2 所示，对源图像分别施加**双边滤波**（削弱高频纹理）和**锐化掩模**（扰动高频结构）后，即使仅执行一次预处理，主体变形也会提前至第三轮编辑出现。这一现象揭示了关键机制：**高频信息（边缘、纹理、精细几何结构）的完整性是维持主体身份跨轮次一致性的必要条件，而多轮编辑过程恰好会渐进性地侵蚀这些高频成分**。

从生成动力学角度理解，基于整流流（Rectified Flow）的扩散模型在去噪早期优先恢复低频全局结构（如整体布局、颜色分布），高频细节则在后期逐步补充。当编辑指令改变图像内容时，模型倾向于向训练数据中的平均化表示靠拢，导致那些与训练分布略有偏离的精细特征被逐步抹平。这种累积效应在多轮编辑中被逐轮放大，最终形成不可逆的质量塌缩。

### 现有方法的缺口

当前应对多轮编辑退化的策略主要分为两类：一是通过**训练式方法**在特定编辑分布上微调模型以增强鲁棒性；二是通过**推理时引导**（如注意力注入、特征约束）在生成过程中保留源图像信息。然而，前者依赖大量标注数据且泛化性受限，后者往往采用全局均匀的保留策略，无法区分“应保留的未编辑区域”与“应修改的语义编辑区域”，导致编辑指令执行不彻底（过保留）或保留失效（欠保留）。

一个被忽视的关键洞察是：**当前轮的上下文图像（即本轮编辑的输入）自身就蕴含丰富的高频细节**。如果在去噪早期将这些细节“借给”生成过程，就可以在不破坏编辑目标的前提下，为多轮编辑提供稳定的几何与纹理锚点。这一思路构成了 FreqEdit 的核心动机：通过小波域的高频特征分离与注入，实现编辑灵活性与保真度之间的精细平衡。

## 核心创新

FreqEdit 的核心创新在于将多轮图像编辑的质量退化问题重新定义为**高频信息渐进性丢失**问题，并围绕这一瓶颈设计了一套无训练（training-free）的频域特征注入与轨迹控制机制。其关键创新点体现在以下三个相互耦合的 changed slots 上。

### 1. 小波域高频特征注入：从“预测”到“校正”的速度场重构

传统编辑方法直接使用模型预测的编辑速度场 $v^{\mathrm{edit}}$ 进行去噪，而 FreqEdit 的核心操作是将速度场计算从“纯预测”切换为“频域校正”。具体而言，方法从当前上下文图像（即本轮编辑的输入 $Z_0^{\mathrm{ref}}$）构造一个参考速度场 $v^{\mathrm{ref}} = \frac{Z_0^{\mathrm{ref}} - Z_{t_i}}{t_0 - t_i}$（Eq. 4），该速度场天然携带了源图像完整的高频细节。随后，通过 2-level 离散小波变换（DWT）分别提取 $v^{\mathrm{ref}}$ 和 $v^{\mathrm{edit}}$ 的多尺度高频系数，并以 CFG 风格的线性外推将参考速度的高频成分注入编辑速度：

$$\tilde{\mathbf{D}}^{(\ell)} = \mathbf{D}_{\mathrm{edit}}^{(\ell)} + \alpha (\mathbf{D}_{\mathrm{ref}}^{(\ell)} - \mathbf{D}_{\mathrm{edit}}^{(\ell)})$$

最终通过逆小波变换（IDWT）将编辑速度的低频成分 $\mathbf{LL}_{\mathrm{edit}}^{(2)}$ 与融合后的高频系数 $\tilde{\mathbf{D}}^{(\ell)}$ 重组，得到校正速度场 $v^{\mathrm{corr}}$（Eq. 8）。这一设计实现了**编辑语义（低频全局结构）与身份保持（高频细节）的解耦融合**：低频成分由编辑指令驱动，高频成分由上下文图像锚定。

因果验证（Figure 6(d)）表明，仅注入高频成分即可防止主体变形，而注入全部频率成分或仅注入低频成分则分别导致编辑失败或主体变形，证实高频成分是防止退化的关键因果因素。

### 2. 空间自适应注入强度：从“均匀注入”到“语义感知调制”

均匀注入强度 $\alpha$ 会在语义编辑区域（如背景替换）产生过保留（over-preservation），导致编辑不彻底。FreqEdit 将其替换为**空间自适应的注入强度图** $\boldsymbol{\alpha}(x,y)$，其计算流程为：

1. 计算编辑速度与参考速度的逐通道 $L_2$ 差异图 $\mathbf{M} = \lVert v^{\mathrm{edit}} - v^{\mathrm{ref}} \rVert_2$（Eq. 9），差异大的区域对应语义修改区；
2. 归一化并反转得到 $\tilde{\mathbf{M}}$（Eq. 10），使未编辑区获得高注入值；
3. 通过指数缩放 $\alpha = \alpha_0 (e^{\gamma \cdot \tilde{\mathbf{M}}} - 1)$（Eq. 11）增强保留区与编辑区之间的对比度；
4. 将空间自适应强度以逐元素乘法融入频域注入公式（Eq. 12）。

这一机制使高频保留仅作用于身份相关区域，而语义编辑区域则不受阻碍地执行指令。消融实验（Figure 6(a)）显示，移除自适应注入后模型无法完成背景变换等复杂语义编辑。

### 3. 轨迹补偿机制：从“无约束注入”到“等价轨迹重定向”

高频注入会不可避免地使实际去噪轨迹偏离纯编辑速度场 $v^{\mathrm{edit}}$ 的方向，导致**幽灵伪影**（ghosting artifacts）——即编辑信号与保留信号在空间上冲突。FreqEdit 引入路径补偿机制来解决这一冲突：

- 在每个时间步累积编辑速度与校正速度的差异 $\Delta v_{t_i} = v_{t_i}^{\mathrm{edit}} - v_{t_i}^{\mathrm{corr}}$（Eq. 13），按时间步长加权存入轨迹缓冲 $B$（Eq. 14）；
- 周期性地将累积偏差 $B$ 加到当前潜在变量上（Eq. 15），将去噪轨迹重新定向到编辑方向。

这一设计的理论保证是：经过补偿后的实际轨迹等价于一条完全由 $v^{\mathrm{edit}}$ 主导的蓝色虚线轨迹（Figure 4），即“在参考速度高频信息的条件下预测编辑速度并沿编辑方向去噪”。消融实验（Figure 6(b)）证实，移除路径补偿会引入明显的幽灵伪影。

### 4. 模型特化适配：FLUX 的质量引导融合

针对 FLUX.1 Kontext 在多轮编辑中出现的噪声积累问题，FreqEdit 额外引入质量引导融合机制：在去噪的最后阶段（$t_i < \tau_{\mathrm{guide}}$），将编辑速度与来自原始图像 $X^{[1]}$ 的辅助速度按比例 $\lambda$ 混合（Eq. 16），以抑制噪声伪影。这一模块是模型特化的补偿设计，而非通用框架的核心组件。

## 整体框架

FreqEdit 是一个无训练的框架，旨在解决多轮图像编辑中因高频信息渐进性丢失导致的质量退化问题。其核心思路是：当前轮次的上下文图像本身蕴含丰富的高频细节，如果在去噪早期将这些细节“借给”生成过程，就能在不破坏编辑目标的前提下为多轮编辑提供稳定的几何与纹理锚点。

框架的整体工作流如下：

1. **速度场构造**：在每一轮编辑的去噪过程中，模型同时维护两个速度场——编辑速度场 $v^{edit}$（由模型根据当前编辑指令 $p^{[k]}$ 和上下文图像 $X^{[k]}$ 预测）和参考速度场 $v^{ref}$（从当前上下文图像 $Z_0^{ref}$ 推导的平均速度场，保留了该图像的高频特征）。

2. **小波域高频注入**：对两个速度场分别进行 2-level 离散小波变换（DWT），提取低频分量 $\mathbf{LL}^{(2)}$ 和多尺度高频分量 $\mathbf{D}^{(1)}, \mathbf{D}^{(2)}$。将参考速度场的高频成分以可控强度注入编辑速度场，得到融合后的高频系数 $\tilde{\mathbf{D}}^{(\ell)}$，再与编辑速度场的低频分量一起通过逆小波变换（IDWT）重建为校正速度场 $v^{corr}$。该模块是防止主体变形和纹理塌缩的核心。

3. **自适应注入策略**：根据编辑速度场与参考速度场之间的 $L_2$ 差异图 $\mathbf{M}$，生成空间自适应的注入强度图 $\boldsymbol{\alpha}$。在语义修改区域（差异大），注入强度低，以保证编辑指令的完整执行；在未修改区域（差异小），注入强度高，以最大化细节保留。这解决了均匀注入导致的“过保留”问题。

4. **路径补偿机制**：由于高频注入会持续引入偏离编辑方向的轨迹偏差，框架周期性地将累积的速度差异缓冲 $B$ 加到当前潜在变量上，将去噪轨迹重定向回编辑方向。该机制消除了因编辑速度与参考速度冲突而产生的幽灵伪影。

5. **质量引导去噪**（仅针对 FLUX.1 Kontext 等存在噪声积累的模型）：在去噪的最后阶段，将编辑速度与来自原始图像 $X^{[1]}$ 的辅助速度按系数 $\lambda$ 混合，以抑制多轮编辑中累积的噪声伪影。

上述模块的关系可概括为：高频注入是主体，自适应策略控制注入的空间分布，路径补偿修正注入引入的轨迹偏差，质量引导则作为特定基座模型的噪声抑制后处理。整个流程在每一轮编辑的每个去噪步上执行，无需额外训练或微调。

### 补充图表

![[assets/figures/papers/paper_list_l876_https_arxiv_org_abs_2512_01755/figures/003_Figure_3.jpg]]
*Figure 3: High-Frequency Feature Injection Pipeline. (A) We construct the reference velocity*

![[assets/figures/papers/paper_list_l876_https_arxiv_org_abs_2512_01755/figures/001_Figure_1.jpg]]
*Figure 1: FreqEdit enables consistent multi-turn image editing. Base models (FLUX.1 Kontext and Qwen-Image) exhibit progressive quality deterioration during iterative editing, including body deformations, edge over-sharpening, and texture collapse. FreqEdit addresses these limitations through strategic high-frequency reinforcement*

## 核心模块与公式推导

FreqEdit 的核心设计围绕一个因果控制旋钮展开：**从当前上下文图像构造参考速度场，并通过小波变换将其高频成分注入到编辑速度场中**。该框架包含四个关键模块，分别解决多轮编辑中的不同退化机制。

### 问题建模与速度场定义

设第 $k$ 轮编辑的上下文图像为 $X^{[k]}$，文本指令为 $p^{[k]}$。在整流流（Rectified Flow）框架下，模型预测编辑速度场：

$$v_{t_i}^{\mathrm{edit}} = v_{\theta}(Z_{t_i}, t_i, X^{[k]}, p^{[k]})$$

其中 $Z_{t_i}$ 为当前噪声潜变量，$t_i$ 为时间步。标准方法直接沿此速度场去噪，导致高频信息在多轮迭代中渐进性丢失——这正是主体变形、边缘过度锐化和纹理塌缩的根本原因（Figure 2 证实：对源图施加双边滤波或锐化掩模扰动高频成分后，主体变形提前至第 3 轮）。

![[assets/figures/papers/paper_list_l876_https_arxiv_org_abs_2512_01755/figures/002_Figure_2.jpg]]
*Figure 2: Bilateral filtering and unsharp masking are each applied once to the source image before editing. Both perturbations accelerate quality degradation, causing subject deformation as early as Turn 3 (red boxes). This confirms that high-frequency integrity is critical for maintaining subject identity across editing turns*

### 模块一：小波域高频特征注入

该模块是 FreqEdit 的核心，其基本思路是：上下文图像 $Z_0^{\mathrm{ref}}$ 自身蕴含丰富的高频细节，若在去噪早期将这些细节「借给」生成过程，就能在不破坏编辑目标的前提下提供稳定的几何与纹理锚点。

**参考速度场构造。** 从上下文图像推导平均速度场，保留其高频特征：

$$v_{t_i}^{\mathrm{ref}} = \frac{Z_0^{\mathrm{ref}} - Z_{t_i}}{t_0 - t_i}$$

**小波分解。** 对编辑速度场和参考速度场分别施加 2-level 离散小波变换（DWT），提取多尺度频率分量：

$$\mathrm{DWT}(v^{\mathrm{ref}}) = \{\mathbf{LL}_{\mathrm{ref}}^{(2)}, \mathbf{D}_{\mathrm{ref}}^{(2)}, \mathbf{D}_{\mathrm{ref}}^{(1)}\}$$

$$\mathrm{DWT}(v^{\mathrm{edit}}) = \{\mathbf{LL}_{\mathrm{edit}}^{(2)}, \mathbf{D}_{\mathrm{edit}}^{(2)}, \mathbf{D}_{\mathrm{edit}}^{(1)}\}$$

其中 $\mathbf{LL}^{(2)}$ 为第二层低频系数（捕获全局结构与颜色），$\mathbf{D}^{(2)}$ 和 $\mathbf{D}^{(1)}$ 分别为第二层和第一层高频系数（编码边缘、纹理及最精细细节如发丝和织物纹理，见 Figure 12 的潜空间频率对齐验证）。

![[assets/figures/papers/paper_list_l876_https_arxiv_org_abs_2512_01755/figures/015_Figure_12.jpg]]
*Figure 12: Latent-space frequency alignment. Images are reconstructed by retaining only the specified frequency band(s) from the 2-level DWT of the latent representation and decoding via VAE*

**高频注入。** 采用 CFG 风格的线性外推，将参考速度的高频细节注入编辑速度：

$$\tilde{\mathbf{D}}^{(\ell)} = \mathbf{D}_{\mathrm{edit}}^{(\ell)} + \alpha \left(\mathbf{D}_{\mathrm{ref}}^{(\ell)} - \mathbf{D}_{\mathrm{edit}}^{(\ell)}\right)$$

其中 $\alpha$ 为注入强度。消融实验（Figure 6(d)）提供了决定性证据：仅注入高频成分可防止主体变形，而注入全部成分或仅注入低频成分会导致编辑失败或主体变形，证实高频成分是关键因果因素。

**校正速度场重建。** 保留编辑速度的低频成分（确保语义编辑方向），融合注入后的高频成分，通过逆小波变换（IDWT）重建：

$$v^{\mathrm{corr}} = \mathrm{IDWT}\left(\mathbf{LL}_{\mathrm{edit}}^{(2)}, \tilde{\mathbf{D}}^{(2)}, \tilde{\mathbf{D}}^{(1)}\right)$$

### 模块二：自适应注入策略

均匀注入强度会过度保留语义编辑区域的高频信息，导致编辑不完全（如背景替换失败）。该模块通过空间自适应的注入强度图解决此问题。

**速度差异图。** 计算编辑速度与参考速度之间的逐通道 $L_2$ 范数，反映各空间位置的语义更改程度：

$$\mathbf{M} = \lVert v^{\mathrm{edit}} - v^{\mathrm{ref}} \rVert_2$$

差异大的区域（需编辑）应降低注入强度，差异小的区域（需保留）应提高注入强度。

**归一化反差异图。** 将差异图归一化并反转：

$$\tilde{\mathbf{M}} = 1 - \frac{\mathbf{M} - \min(\mathbf{M})}{\max(\mathbf{M}) - \min(\mathbf{M})}$$

**指数缩放注入强度图。** 通过指数缩放增强保留区与编辑区之间的对比：

$$\boldsymbol{\alpha} = \alpha_0 \left(e^{\gamma \cdot \tilde{\mathbf{M}}} - 1\right)$$

其中 $\alpha_0$ 为基础注入强度，$\gamma$ 控制对比度。FLUX.1 Kontext 使用 $\alpha_0=1.6, \gamma=2.0$；Qwen-Image 使用 $\alpha_0=2.0, \gamma=1.6$（Section 5.1）。

**自适应注入。** 将空间自适应强度图融入频率域注入公式：

$$\tilde{\mathbf{D}}^{(\ell)} = \mathbf{D}_{\mathrm{edit}}^{(\ell)} + \boldsymbol{\alpha}^{(\ell)} \odot \left(\mathbf{D}_{\mathrm{ref}}^{(\ell)} - \mathbf{D}_{\mathrm{edit}}^{(\ell)}\right)$$

消融实验（Figure 6(a), Figure 8）证实：移除自适应注入策略后，模型无法执行背景变换等复杂语义编辑，出现过度保留现象。

### 模块三：路径补偿机制

高频注入会改变去噪轨迹，引入编辑速度与校正速度之间的累积偏差，导致幽灵伪影（ghosting artifacts）。路径补偿机制周期性修正这一偏差。

**速度差异。** 每步记录编辑速度与校正速度的差异：

$$\Delta v_{t_i} = v_{t_i}^{\mathrm{edit}} - v_{t_i}^{\mathrm{corr}}$$

**轨迹缓冲更新。** 按时间步加权累加速度差异：

$$B \gets B + (t_{i-1} - t_i) \cdot \Delta v_{t_i}$$

**路径补偿应用。** 每隔 $n$ 步将累积偏差加到潜变量上，使实际轨迹等价于纯粹编辑速度场的轨迹（Figure 4）：

$$Z_{t_{i-n}} \gets Z_{t_{i-n}} + B$$

Figure 13 可视化了中间去噪步的校正潜变量及缓冲热图：高频注入后的潜变量残留与编辑目标冲突的结构（红框），而轨迹缓冲携带对应的结构化校正信号（蓝框）以抵消该残留结构。消融实验（Figure 6(b), Figure 9）证实：移除路径补偿会引入幽灵伪影，如重复的滑板者、毕业姿势和幽灵般的父母形象。

![[assets/figures/papers/paper_list_l876_https_arxiv_org_abs_2512_01755/figures/016_Figure_13.jpg]]
*Figure 13: Visualization of path compensation at an intermediate denoising step. The corrected latent*

### 模块四：质量引导去噪（仅 FLUX 模型）

FLUX.1 Kontext 在多轮编辑中会出现噪声积累（Figure 6(c)）。该模块在去噪最后阶段（$t_i < \tau_{\mathrm{guide}}$）混合原始图像的速度信息以抑制噪声：

$$\boldsymbol{v}_{t_i}^{\mathrm{final}} = (1 - \lambda) \cdot \boldsymbol{v}_{t_i}^{\mathrm{edit}} + \lambda \cdot \boldsymbol{v}_{\theta}(\boldsymbol{Z}_{t_i}, t_i, \boldsymbol{X}^{[1]}, p_{\mathrm{neutral}})$$

其中 $\lambda$ 为混合权重，$p_{\mathrm{neutral}}$ 为中性提示词。Figure 10 的消融显示：在原生模型上添加质量引导即可有效抑制噪声积累；与高频注入框架结合后，进一步消除残余噪声伪影，提升视觉保真度。

### 模块间的因果依赖

四个模块构成递进的因果链条：高频注入是防止退化的核心（决定性证据来自 Figure 6(d) 的频率成分消融），自适应注入确保编辑灵活性（Figure 6(a) 证实其必要性），路径补偿修正注入引入的轨迹偏差（Figure 6(b) 证实其消除幽灵伪影的作用），质量引导作为 FLUX 模型的补充模块处理其特有的噪声积累问题（Figure 6(c) 证实）。超参数敏感性分析（Figure 11）表明，$\alpha_0$、$\gamma$、$\lambda$ 在合理范围内具有鲁棒性，超出范围则出现失败区域。

### 补充图表

![[assets/figures/papers/paper_list_l876_https_arxiv_org_abs_2512_01755/figures/004_Figure_4.jpg]]
*Figure 4: Path Compensation Mechanism. The actual denoising trajectory (orange line*

## 实验与分析

### 核心发现：高频退化是多轮编辑质量下降的根本瓶颈

FreqEdit 的核心实验发现是：多轮编辑过程中高频信息的渐进性丢失是导致图像质量退化的根本原因，具体表现为主体变形、边缘过度锐化和纹理塌缩。早期去噪步骤优先恢复低频全局结构，高频细节容易被抑制，累积误差使生成模型趋向训练数据中的平均化表示。

这一结论通过受控消融实验（Figure 2）得到直接验证：对源图分别施加**双边滤波**（削弱高频）和**锐化掩模**（增强高频伪影）扰动高频成分后，原本在正常多轮编辑中能维持多轮的主体，在第三轮即出现明显的主体变形。这证实了高频完整性对保持主体身份在多轮编辑中的关键作用。

### 主实验结果：多轮编辑的定量与定性评估

主实验在 70 张图像 × 10 轮编辑的设定下进行，对比了 FreqEdit 增强后的 FLUX.1 Kontext 和 Qwen-Image 与多个基线方法的性能。

**Table 1** 展示了 10 轮编辑的累计定量结果。以 FLUX.1 Kontext 为基座，FreqEdit 在第 10 轮将 **CLIP-I** 从 0.854 提升至 **0.884**（+0.030），将 **LPIPS** 从约 0.546 降至 **0.418**（-0.128），并将主体一致性指标（Cons.）从约 0.709 提升至 **0.798**（+0.089）。指令遵循能力（Instr.）仅轻微下降 0.013（从 0.803 到 0.790），表明高频注入几乎不影响语义编辑的准确性。Qwen-Image + FreqEdit 在所有一致性指标上均取得最优结果，同时保持了有竞争力的指令遵循能力。

**Table 2** 补充了 PSNR、SSIM 和 DINO-Sim 的累计平均指标，进一步证实 FreqEdit 在低层细节保持和高层语义一致性上的稳定优势。

定性对比（Figure 5 及 Figure 15–20）显示，基线模型 FLUX.1 Kontext、Qwen-Image、Seedream 4.0、Nano Banana、MTC、VINCIE 和 Bagel 在多轮编辑中均出现不同程度的质量退化，而 FreqEdit 在指令遵循、主体一致性和整体感知质量三者之间取得了最佳平衡。

![[assets/figures/papers/paper_list_l876_https_arxiv_org_abs_2512_01755/figures/005_Figure_5.jpg]]
*Figure 5: Qualitative comparison of iterative editing. Compared to FLUX.1 Kontext [27], Qwen-Image [55], Seedream 4.0 [46], Nano Banana [18], MTC [62], VINCIE [41], and Bagel [9], our method achieves a better balance among instruction following, subject consistency, and overall perceptual quality. Please zoom in for a better view*

### 消融实验：各模块的因果贡献

消融实验（Figure 6，Section 5.3）系统验证了 FreqEdit 四个核心模块的因果作用：

![[assets/figures/papers/paper_list_l876_https_arxiv_org_abs_2512_01755/figures/007_Figure_6.jpg]]
*Figure 6: Ablation study. (a) Without the adaptive injection strategy, the model fails to perform background transformation and subject removal. (b) Removing the path compensation mechanism introduces visible ghosting artifacts. (c) Without quality guidance, FLUX.1 Kontext exhibits severe noise artifacts after several editing iterations. (d) Injecting all features or low-frequency components, rather than selectively fusing high-frequency features, leads to semantic leakage and editing failures*

1. **自适应注入策略（Adaptive Injection）**：移除该模块（改用均匀注入强度）后，模型无法执行背景替换等复杂语义编辑，语义修改区域出现过保留现象（Figure 6a, Figure 8）。这是因为均匀注入无法区分编辑区域与保留区域，导致需要修改的区域也被高频信息“锚定”。

2. **路径补偿机制（Path Compensation）**：移除后出现明显的幽灵伪影（ghosting artifacts），如重复的滑板运动员或重叠的人物姿态（Figure 6b, Figure 9）。这是因为编辑速度与参考速度的冲突信号未被消除，导致两个速度场的视觉元素同时显现。

3. **质量引导去噪（Quality Guidance，仅 FLUX.1 Kontext）**：去除该模块后，FLUX.1 Kontext 在多轮编辑后出现严重的噪声积累伪影（Figure 6c, Figure 10）。该模块通过在去噪最后阶段混合原始图像的速度信息，有效抑制了噪声积累。

4. **频率成分选择性注入**：仅注入低频或全部频率成分会导致编辑失败或主体变形，而**仅注入高频成分**则能保持结构稳定（Figure 6d）。这直接证明了高频成分是防止多轮编辑退化的关键因果因素，而非低频或全频段信息。

### 失败模式与局限性

FreqEdit 的局限性在实验中也得到明确揭示：

- **对源图质量的依赖**：若初始图像本身缺少高频细节（如低分辨率或模糊图像），注入效果有限，因为参考速度场中可提取的高频信息本身不足。
- **大面积编辑效果减弱**：当单条指令覆盖图像大部分区域时，自适应注入图失去判别力（编辑区与保留区差异图趋于均匀），注入精度下降。不过多轮编辑天然将复杂操作拆分为小区域改动，可部分缓解此问题。
- **分布外风险**：作为无训练方法，推理时修改速度场可能使生成轨迹脱离训练分布，极端输入仍可能出现不理想结果，尽管自适应注入和路径补偿已提供一定缓解。

### 关键图表结论汇总

- **Figure 2**：高频扰动使主体变形提前至第 3 轮，确立高频完整性为因果前提。
- **Figure 5 + Table 1**：FreqEdit 在 10 轮编辑中实现指令遵循与主体一致性的最佳平衡。
- **Figure 6**：四个模块消融分别揭示过保留、幽灵伪影、噪声积累和频率选择性的因果机制。
- **Figure 7**：逐轮性能曲线显示 FreqEdit 在所有编辑轮次上持续改善 PSNR、SSIM 和 DINO-Sim。
- **Figure 11**：超参数敏感性分析给出 α₀、γ、λ 的鲁棒范围（FLUX.1 Kontext 默认值：α₀=1.6, γ=2.0, λ=0.3）。

![[assets/figures/papers/paper_list_l876_https_arxiv_org_abs_2512_01755/figures/006_Table_1.jpg]]
*Table 1: Quantitative results across 10 sequential edits. Our method demonstrates stable performance across all metrics throughout the editing sequence. “Instr.” and “Cons.” denote instruction-following and consistency metrics, respectively. The best results are highlighted in bold, while the second-best results are underlined*

![[assets/figures/papers/paper_list_l876_https_arxiv_org_abs_2512_01755/figures/009_Figure_7.jpg]]
*Figure 7: Per-turn metrics across 10 sequential editing steps. We report SSIM (left), PSNR (middle), and DINO-Sim (right) at each turn k, all computed by comparing the edited image*

![[assets/figures/papers/paper_list_l876_https_arxiv_org_abs_2512_01755/figures/013_Figure_11.jpg]]
*Figure 11: Hyperparameter sensitivity analysis on FLUX.1 Kontext. Each row varies one hyperparameter while fixing the others to their default values*

### 补充图表

![[assets/figures/papers/paper_list_l876_https_arxiv_org_abs_2512_01755/figures/008_Table_2.jpg]]
*Table 2: Additional quantitative results using PSNR, SSIM and DINO-Sim. We report cumulative averages computed from turn 1 through each specified turn (1, 4, 7, 10) across 10 sequential edits. Bold indicates the best results, and underlined values denote the secondbest results*

## 方法谱系与知识库定位

### 问题定位与基线关系

FreqEdit 面向多轮图像编辑中**高频信息渐进性丢失**这一瓶颈——具体表现为主体变形、边缘过度锐化和纹理塌缩。此问题在现有基于整流流（rectified flow）的编辑模型中普遍存在，但此前未被系统性地识别为根本退化机制。论文通过受控消融实验（Figure 2）证实：对源图施加双边滤波或锐化掩模扰动高频成分，会使主体变形提前到第三轮编辑，从而确立高频完整性对多轮编辑鲁棒性的因果作用。

FreqEdit 在以下主流图像编辑模型上进行了验证：

| 基线方法 | 角色 | 编辑范式 |
|---------|------|---------|
| **FLUX.1-Kontext-dev** | 基础模型/基线 | 基于整流流的上下文感知编辑 |
| **Qwen-Image** | 基础模型/基线 | 基于扩散的指令驱动编辑 |
| **Seedream 4.0** | 对比基线 | 商业级图像编辑 |
| **Nano Banana** | 对比基线 | 迭代式图像编辑 |
| **MTC** | 对比基线 | 多轮文本条件编辑 |
| **VINCIE** | 对比基线 | 基于反演的连续编辑 |
| **Bagel** | 对比基线 | 基于引导的编辑框架 |

FreqEdit 与上述方法的关键区别在于：它**不修改模型参数**，而是通过操纵去噪过程中的速度场来实现高频保留。具体而言，FreqEdit 在四个维度上改变了标准编辑流程：

1. **速度场计算**：将标准编辑速度场 $v^{edit}$ 替换为校正速度场 $v^{corr}$，后者通过小波域高频注入并结合编辑速度场的低频成分重构得到（Eq. 8）。
2. **注入强度调节**：将均匀注入强度 $\alpha$ 替换为空间自适应的注入强度图 $\alpha(x,y)$，基于编辑/参考速度场的 L2 差异并经过指数缩放（Eq. 12）。
3. **轨迹对齐**：引入路径补偿机制，周期性利用累积的速度差异缓冲 $B$ 对潜在变量进行修正（Eq. 15），这是现有编辑方法中未见的设计。
4. **噪声处理**（仅 FLUX 模型）：在去噪最后阶段将编辑速度与来自原始图像的辅助速度混合（Eq. 16），以抑制 FLUX.1 Kontext 在多轮编辑中出现的噪声积累。

### 方法谱系中的位置

FreqEdit 属于**无训练（training-free）的推理时编辑框架**，其核心操作发生在速度场/潜空间而非像素空间。从技术谱系上看：

- **与基于反演的方法**（如 VINCIE）的关系：反演方法依赖 DDIM 反演将编辑图像映射回噪声空间再重新生成，在多轮编辑中反演误差会累积。FreqEdit 不依赖反演，而是直接从上下文图像构造参考速度场，避免了反演误差的传播。
- **与基于注意力注入的方法**的关系：许多编辑方法通过注入自注意力图来保持结构一致性。FreqEdit 的操作对象是速度场而非注意力图，且通过小波分解实现了频率层面的精确控制，这在编辑方法中较为独特。
- **与基于引导的方法**（如 Bagel）的关系：引导方法通常通过分类器或无分类器引导来约束生成方向。FreqEdit 的注入机制在形式上类似 CFG 风格的外推（Eq. 7），但其引导信号来自上下文图像自身的高频成分，而非外部条件。

### 适用边界与局限

FreqEdit 的适用性受以下因素约束：

1. **对源图像质量的依赖**：若初始图像本身缺少高频细节（如低分辨率、强压缩或过度平滑的图像），注入效果有限。这是该方法的根本性约束——它只能「借用」已有细节，无法凭空生成。

2. **分布外行为的潜在风险**：推理时修改速度场可能使生成轨迹脱离训练分布。虽然自适应注入和路径补偿在一定程度上缓解了这一问题，但论文明确指出极端输入仍可能出现不理想结果。这一局限的严重程度缺乏定量刻画，需要进一步验证。

3. **大面积编辑效果减弱**：当单条指令覆盖图像大部分区域时，自适应注入图失去判别力（因为编辑与参考速度场在全局范围内均有较大差异），注入精度下降。多轮编辑天然将复杂操作拆分为小区域改动，可部分缓解此问题，但在单轮大面积编辑场景下该方法的优势可能不明显。

4. **模型特异性**：质量引导去噪模块（Section 4.5）专门针对 FLUX.1 Kontext 的噪声积累问题设计，对 Qwen-Image 等其他模型并不必要。这意味着 FreqEdit 的完整流水线在不同基础模型上需要调整。

### 开放问题

论文提出了以下值得进一步探索的方向：

1. **训练阶段的整合**：当前 FreqEdit 完全在推理时运作。能否将高频保持原则融入训练损失函数，以提高训练式编辑模型的固有鲁棒性？这涉及将频率域约束引入整流流或扩散模型的训练目标中。

2. **跨模态扩展**：FreqEdit 的核心机制——从小波域提取并注入高频特征——在原理上不限于图像。能否将其扩展到视频多轮编辑（利用时序高频一致性）或其他模态（如音频、3D 形状）的迭代编辑中？

3. **极端条件下的鲁棒性**：在极端失真、非自然图像（如医学影像、遥感图像）或大范围遮挡的条件下，自适应注入和路径补偿的鲁棒性尚未得到验证。这些场景下速度场的语义可解释性可能降低，影响注入精度。

4. **注入强度的自动化调参**：当前 $\alpha_0$、$\gamma$、$\lambda$ 等超参数需要针对不同基础模型手动调整（FLUX.1 Kontext 使用 $\alpha_0=1.6, \gamma=2.0$，Qwen-Image 使用 $\alpha_0=2.0, \gamma=1.6$）。能否设计自适应的参数选择策略，减少人工调参负担？

5. **与其他编辑策略的协同**：FreqEdit 的高频注入机制与注意力注入、结构引导等方法在原理上互补。探索这些策略的协同组合可能进一步提升多轮编辑的鲁棒性和编辑精度。

## 原文 PDF

![[paperPDFs/CVPR_2026/FreqEdit_Preserving_High_Frequency_Features_for_Robust_Multi_Turn_Image_Editing.pdf]]
