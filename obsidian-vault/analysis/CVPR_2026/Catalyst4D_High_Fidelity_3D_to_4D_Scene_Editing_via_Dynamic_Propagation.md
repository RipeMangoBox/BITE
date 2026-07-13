---
title: "Catalyst4D: High-Fidelity 3D-to-4D Scene Editing via Dynamic Propagation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Catalyst4D_High_Fidelity_3D_to_4D_Scene_Editing_via_Dynamic_Propagation.pdf
project_link: null
code_link: null
aliases:
- Catalyst4D
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 通过Anchor-based Motion Guidance (AMG) 构建锚点并利用非平衡最优传输建立区域级对应，实现一致的局部变形传播；同时结合Color Uncertainty-guided Appearance Refinement (CUAR) 量化高斯颜色不确定性，选择性纠正因遮挡导致的外观伪影。
primary_logic: 将3D编辑与4D时间传播解耦，利用锚点对应和颜色不确定性量化，在无需重新训练变形网络的条件下，将静态3D编辑的高保真、多视角一致性扩展至动态序列。
claims:
- 在 DyNeRF（Sear-steak, Coffee-martini）和 MeetRoom（Trimming）基准上，Catalyst4D 在 CLIP 相似度上均优于所有对比方法（Instruct 4D-to-4D, Instruct-4DGS, CTRL-D），同时保持具有竞争力的时间一致性。
- 消融实验表明，AMG 模块对于正确运动传播至关重要（去除 AMG 后 CLIP 从 0.252 降至 0.245，一致性从 0.971 降至 0.966），而 CUAR 模块进一步提升了视觉保真度。
- 在局部编辑和全局风格迁移任务上，Catalyst4D 实现了更精准的局部修改和更一致的风格传播，避免了 CTRL-D 等 2D 方法造成的模糊、过度平滑和非目标区域误修改。
- Sear-steak (DyNeRF) 上 CLIP sim.↑ = 0.252
---

# Catalyst4D: High-Fidelity 3D-to-4D Scene Editing via Dynamic Propagation

> [!tip] 核心洞察
> 将3D编辑与4D时间传播解耦，利用锚点对应和颜色不确定性量化，在无需重新训练变形网络的条件下，将静态3D编辑的高保真、多视角一致性扩展至动态序列。

| 字段 | 内容 |
|------|------|
| 中文题名 | Catalyst4D：基于动态传播的高保真3D到4D场景编辑 |
| 英文题名 | Catalyst4D: High-Fidelity 3D-to-4D Scene Editing via Dynamic Propagation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.12766) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Catalyst4D |
| Dataset | Sear-steak, Coffee-martini, Trimming |

> [!tip] 效果简介
> - Sear-steak (DyNeRF) 上，CLIP sim.↑ 0.252 vs 0.249 (CTRL-D) (+0.003)。
> - Coffee-martini (DyNeRF) 上，CLIP sim.↑ 0.249 vs 0.246 (CTRL-D) (+0.003)。
> - Trimming (MeetRoom) 上，CLIP sim.↑ 0.251 vs 0.248 (CTRL-D) (+0.003)。

## 概要

**目标问题**：现有的 2D 扩散模型直接扩展到 4D 动态场景编辑时，缺乏显式的几何推理，导致运动伪影、时间闪烁以及非目标区域的意外修改，难以同时维持空间一致性和时间一致性。

**核心思想**：Catalyst4D 将 3D 空间编辑与 4D 时间传播解耦——先在首帧完成高保真的 3D 高斯编辑，再通过基于锚点的运动引导（Anchor-based Motion Guidance, AMG）和颜色不确定性引导的外观细化（Color Uncertainty-guided Appearance Refinement, CUAR），将编辑结果可靠地传播至全部帧。这一设计无需重新训练变形网络，即可将静态 3D 编辑的多视角一致性和编辑灵活性扩展到动态序列。

**方法定位**：Catalyst4D 是一种 3D-to-4D 编辑传播框架，区别于直接从 2D 扩散编辑帧拟合 4D 表示的 Instruct 4D-to-4D、Instruct-4DGS 和 CTRL-D 等方法。其核心创新在于 AMG 通过锚点构建与非平衡最优传输建立区域级对应，实现局部一致的变形传递；CUAR 则通过量化高斯颜色不确定性，选择性纠正因遮挡引起的外观伪影。

**主要结果**：在 DyNeRF（Sear-steak、Coffee-martini）和 MeetRoom（Trimming）基准上，Catalyst4D 的 CLIP 相似度均优于所有对比方法（最高达 0.252 vs. CTRL-D 的 0.249），同时保持具有竞争力的时间一致性（0.986 vs. 0.983）。消融实验证实，AMG 模块对正确运动传播至关重要——移除后 CLIP 相似度从 0.252 降至 0.245，一致性从 0.971 降至 0.966；CUAR 模块进一步提升了视觉保真度，有效抑制了颜色伪影和闪烁。在局部编辑和全局风格迁移任务上，Catalyst4D 实现了更精准的局部修改和更一致的风格传播，避免了对比方法常见的模糊、过度平滑和非目标区域误修改问题。

### 动态场景编辑的核心瓶颈

将2D扩散模型的强大编辑能力直接迁移到4D动态场景面临一个根本性矛盾：**空间编辑精度与时间一致性难以兼得**。现有方法通常采用“2D-to-4D”范式——先用2D扩散模型逐帧编辑视频，再将编辑结果拟合为4D表示（如动态NeRF或4D高斯泼溅）。然而，这一路径缺乏显式的几何推理，导致三个典型失效模式：

1. **运动伪影**：逐帧独立的2D编辑破坏了帧间运动连续性，产生抖动和闪烁。
2. **非目标区域误修改**：扩散模型的编辑边界模糊，常将修改扩散到不应改变的区域。
3. **遮挡所致外观退化**：动态场景中的遮挡关系随时间变化，2D编辑无法感知3D几何，造成被遮挡区域的颜色不一致。

这些问题的根源在于：2D扩散模型在编辑时仅考虑单帧的像素级语义对齐，而缺少对底层3D几何结构和时间变形场的理解。

### 现有方法的局限性

当前主流的4D编辑方法可归为三类，各有不足：

- **Instruct 4D-to-4D** 和 **Instruct-4DGS** 尝试直接在4D表示上进行文本引导编辑，但受限于Score Distillation Sampling的模糊性和多视角不一致性，编辑结果往往过度平滑，且难以实现精确的局部修改。
- **CTRL-D** 采用DreamBooth式微调，将编辑信息注入4D重建过程，但在风格迁移任务中容易造成全局模糊，且无法精确定位编辑区域。
- 更根本的是，这些方法都**未将空间编辑与时间传播解耦**：编辑信号和运动信号纠缠在一起，使得任何一方的优化都可能损害另一方。

### 核心动机：解耦编辑与传播

Catalyst4D的核心洞察是：**3D编辑的高保真性应建立在静态场景上，而时间一致性应通过显式的运动传播机制保证**。将二者解耦意味着：

- 在首帧（canonical frame）上应用成熟的3D高斯编辑方法（如DGE、DreamCatalyst、SGSST），充分利用其多视角一致性和局部编辑精度。
- 随后通过一个独立的传播管道，将首帧的几何和外观修改沿时间轴扩散到所有帧，**无需重新训练变形网络**。

这一解耦设计的关键挑战在于：如何在不依赖逐帧2D扩散监督的条件下，将首帧的编辑可靠地传播到动态序列中？这要求传播机制必须同时解决两个子问题——**运动引导**（编辑后的高斯如何跟随场景运动）和**外观细化**（因遮挡和运动导致的颜色伪影如何修正）。Catalyst4D分别通过Anchor-based Motion Guidance (AMG) 和 Color Uncertainty-guided Appearance Refinement (CUAR) 回应了这两个挑战。

## 核心方法与创新机理

Catalyst4D 的核心创新在于将静态 3D 编辑的高保真、多视角一致性扩展至动态 4D 序列时，**解耦空间编辑与时间传播**，通过两个关键模块解决直接 2D-to-4D 扩展带来的运动伪影、时间闪烁和非目标区域误修改等瓶颈问题。

### 1. 编辑传播管道的范式转换：从 2D-to-4D 到 3D-to-4D

现有 4D 编辑方法（如 **Instruct 4D-to-4D**、**CTRL-D**、**Instruct-4DGS**）通常采用 2D-to-4D 范式：先在各帧上应用 2D 扩散模型进行编辑，再将编辑结果拟合为 4D 表示。这一范式缺乏显式几何推理，导致编辑在多视角间不一致，且容易在非目标区域产生意外修改（参见 Figure 4 中基线方法的模糊、过度平滑和误修改现象）。

Catalyst4D 转而采用 **3D-to-4D 传播范式**：首先在动态场景的首帧上应用现有 3D 高斯编辑方法（如 DGE、DreamCatalyst、SGSST）进行编辑，获得具有几何一致性的编辑结果；随后通过专门的传播机制，将首帧编辑传递至全部时间帧。这一范式转换使编辑过程继承了静态 3D 编辑的灵活性和多视角一致性，同时避免了逐帧 2D 编辑带来的时间闪烁问题。

### 2. 运动传播机制：Anchor-based Motion Guidance (AMG)

传统 4D 编辑方法在传播编辑时，通常直接复用原始变形网络或采用 KNN 插值来驱动编辑后高斯的运动。然而，编辑操作（如移除物体、改变几何结构）可能破坏原始场景的拓扑结构，导致变形网络无法正确匹配，产生运动漂移和跨区域干扰。

AMG 模块通过**构建锚点并利用非平衡最优传输建立区域级对应关系**来解决这一问题：

- **锚点构建**：从原始和编辑后的首帧高斯云中提取结构稳定、空间代表性的锚点。锚点的生成采用自适应圆柱体检测机制——仅当多个邻近高斯持续落在自适应定义的圆柱体内时才生成锚点（Figure 5），从而过滤掉噪声和不稳定区域。
- **最优传输匹配**：在锚点之间通过非平衡最优传输（Sinkhorn 算法）建立区域级对应关系。这种匹配对极端拓扑变化具有鲁棒性，NDD 指标在广泛正则化范围内保持稳定（Figure A3）。
- **变形聚合**：编辑后高斯的位置变形通过对应源高斯变形的加权平均得到，权重结合不透明度和马氏距离（Eq. 9-10），确保变形传播的局部性和一致性。

消融实验（Table 2, Figure 6）表明，去除 AMG 后 CLIP 相似度从 0.252 降至 0.245，时间一致性从 0.971 降至 0.966，验证了 AMG 对正确运动传播的关键作用。

### 3. 外观细化机制：Color Uncertainty-guided Appearance Refinement (CUAR)

现有方法通常缺乏对运动传播过程中外观伪影的显式处理，导致遮挡区域出现颜色失真和闪烁。

CUAR 模块通过**量化高斯颜色不确定性并选择性纠正伪影**来提升外观保真度：

- **颜色不确定性估计**：基于高斯在不同帧间的投影颜色差异，估计每个高斯的颜色不确定性（Eq. 15）。不确定性高的区域通常对应遮挡导致的伪影。
- **伪影掩模生成**：利用不确定性估计生成伪影掩模，精确定位需要细化的区域。
- **选择性细化**：通过首帧图像翘曲（warping）提供伪真值监督，仅在伪影区域施加前景细化损失（Eq. 18），避免对非伪影区域的不必要修改。

消融实验（Table 2, Figure 7）显示，去除 CUAR 后 CLIP 相似度降至 0.248，一致性降至 0.969，且出现明显的颜色伪影和闪烁，证明 CUAR 对提升视觉保真度有显著贡献。

### 创新总结

Catalyst4D 的三个 changed slots 形成协同效应：**3D-to-4D 范式**奠定了几何一致性基础，**AMG** 确保编辑在时间维度上的正确运动传播，**CUAR** 进一步消除传播过程中引入的外观伪影。这一组合使 Catalyst4D 在无需重新训练变形网络的条件下，实现了对局部编辑和全局风格迁移任务的高保真 4D 编辑。

Catalyst4D 的核心设计理念是将**空间编辑**与**时间传播**解耦：先在动态序列的首帧（canonical frame）上完成高保真的 3D 高斯编辑，再通过两个专用模块将编辑结果传播至全部时间帧。这一 3D-to-4D 范式避免了直接将 2D 扩散模型扩展到 4D 时因缺乏显式几何推理而产生的运动伪影、时间闪烁和非目标区域意外变化。

### 管道概览

Figure 2 展示了 Catalyst4D 的完整管道，其输入输出流如下：

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2603_12766/figures/002_Figure_2.jpg]]
*Figure 2: Overview of Catalyst4D. Given the first-frame edited dynamic Gaussians, our (a) Anchor-based Motion Guidance establishes region-level correspondences with the original Gaussians via anchor construction and optimal transport, enabling reliable deformation transfer. Then, (b) Color Uncertainty-guided Appearance Refinement leverages first-frame warping and Gaussian color consistency to identify and correct motion-induced artifacts across time*

1. **输入**：一个已重建的 4D 动态高斯场景，包含正则空间高斯云 $\mathcal{G}_c$ 和变形网络 $\mathcal{F}_{\boldsymbol{\theta}}$，后者可将正则高斯变形到任意时刻 $t$ 的帧高斯 $\mathcal{G}^t = \mathcal{F}_{\boldsymbol{\theta}}(\mathcal{G}_c, t)$。
2. **首帧 3D 编辑**（外部模块）：应用现有的 3D 高斯编辑方法（如 DGE、DreamCatalyst、SGSST）对首帧高斯 $\mathcal{G}^1$ 进行编辑，得到编辑后的首帧高斯 $\mathcal{G}_{\text{edit}}^1$。该步骤充分利用了静态 3D 编辑器在多视角一致性和编辑灵活性上的优势。
3. **Anchor-based Motion Guidance (AMG)**：从原始首帧高斯 $\mathcal{G}^1$ 和编辑后首帧高斯 $\mathcal{G}_{\text{edit}}^1$ 中分别提取结构稳定、空间代表性的锚点，通过非平衡最优传输建立区域级对应关系。随后，将原始高斯的逐帧变形（由变形网络预测）按对应关系聚合传播给编辑后的高斯，驱动其随时间运动。
4. **Color Uncertainty-guided Appearance Refinement (CUAR)**：针对运动传播过程中因遮挡等因素产生的颜色伪影，估计每帧每个高斯的颜色不确定性，生成伪影掩模，并通过首帧图像翘曲的伪真值监督进行选择性细化，最终输出编辑后的完整 4D 序列。

### 模块关系与数据流

两个核心模块呈**串行级联**关系，各司其职：

- **AMG 负责几何一致性**：解决“编辑后的高斯应该往哪里移动”的问题。它通过锚点对应机制，将源高斯的变形场可靠地迁移到目标高斯，避免直接复用变形网络或 KNN 插值带来的运动漂移和跨区域干扰。
- **CUAR 负责外观一致性**：解决“移动后的高斯颜色是否正确”的问题。它利用高斯在相邻帧间的投影颜色差异量化不确定性，仅对高不确定性区域进行细化，在纠正伪影的同时避免对正确区域的不必要修改。

这种解耦设计的关键优势在于：整个传播过程**无需重新训练变形网络**，也不修改底层 4D 重建的高斯密度，因此计算开销可控（单块 NVIDIA A100 GPU 上训练约 40–50 分钟），且方法对底层 4D 表示的依赖性被显式隔离在 AMG 的变形迁移环节。

Catalyst4D 的核心设计理念是**将空间编辑与时间传播解耦**：先在首帧完成高质量的 3D 高斯编辑，再通过两个协同模块——Anchor-based Motion Guidance (AMG) 和 Color Uncertainty-guided Appearance Refinement (CUAR)——将编辑结果高保真地传播至整个动态序列。这一管道避免了直接使用 2D 扩散模型扩展到 4D 时因缺乏显式几何推理而产生的运动伪影和时间闪烁。

### 关键模块

**Anchor-based Motion Guidance (AMG)** 负责解决运动传播问题。给定原始动态高斯场景和编辑后的首帧高斯，AMG 首先从两者中提取结构稳定、空间代表性的锚点（anchor），然后通过非平衡最优传输（unbalanced optimal transport）建立锚点间的区域级对应关系。基于此对应，AMG 将原始源高斯的时域变形聚合传递到编辑后的目标高斯上，实现一致的局部变形传播。这一机制避免了直接复用变形网络或 KNN 插值带来的运动漂移和跨区域干扰。

**Color Uncertainty-guided Appearance Refinement (CUAR)** 负责解决因遮挡和运动导致的外观伪影。CUAR 通过估计每个高斯的颜色不确定性来识别伪影区域：当某个高斯在相邻帧间投影颜色差异较大时，其不确定性较高。随后，CUAR 利用首帧图像通过渲染光流翘曲生成的伪真值监督，对高不确定性区域进行选择性外观细化，从而纠正色彩闪烁和遮挡伪影。

### 核心公式推导

**首帧高斯获取**。原始动态场景由规范空间高斯 $\mathcal{G}_c$ 和变形网络 $\mathcal{F}_{\boldsymbol{\theta}}$ 表示。首帧高斯通过变形场在 $t=1$ 时刻获得：

$$\mathcal{G}^1 = \mathcal{F}_{\boldsymbol{\theta}}(\mathcal{G}_c, t=1)$$

**位置变形聚合**（AMG 核心）。对于编辑后的目标高斯 $\mathbf{g}$，其从帧 1 到帧 $t$ 的位置变形 $\Delta\mu_{\mathbf{g}}^{t}$ 由对应源高斯 $\mathbf{g}'\in\mathcal{G}_{\mathrm{src}}^{1,\mathrm{sub}}$ 的变形加权平均得到：

$$\Delta\mu_{\mathbf{g}}^{t} = \frac{\sum_{\mathbf{g}'\in\mathcal{G}_{\mathrm{src}}^{1,\mathrm{sub}}} w_{\mathbf{g}'} \Delta\mu_{\mathbf{g}'}^{t}}{\sum_{\mathbf{g}'\in\mathcal{G}_{\mathrm{src}}^{1,\mathrm{sub}}} w_{\mathbf{g}'}}$$

其中 $\Delta\mu_{\mathbf{g}'}^{t}$ 由变形网络预测。权重 $w_{\mathbf{g}'}$ 结合了源高斯的不透明度 $\sigma_{\mathbf{g}'}$ 和与目标高斯的马氏距离：

$$w_{\mathbf{g}'} = \sigma_{\mathbf{g}'} \exp\Big(-\frac{1}{2}(\mu_{\mathbf{g}'}-\mu_{\mathbf{g}})^{\mathrm{T}}\boldsymbol{\Sigma}_{\mathbf{g}'}^{-1}(\mu_{\mathbf{g}'}-\mu_{\mathbf{g}})\Big)$$

**渲染光流**。为支持 CUAR 的帧间翘曲，需要渲染从帧 1 到帧 $t$ 的光流图。对于视图 $v$，渲染光流通过 alpha 混合获得：

$$F_{1t}^{v} = \sum_{i\in\mathcal{N}} f_{i,1t}^{v} \alpha_{i} \prod_{j=1}^{i-1}(1-\alpha_{j})$$

其中 $f_{i,1t}^{v}$ 为第 $i$ 个高斯在视图 $v$ 下从帧 1 到帧 $t$ 的投影位移。

**高斯颜色不确定性**（CUAR 核心）。对于视图 $v$ 在时刻 $t$，颜色不确定性 $\xi_{t}^{v}$ 基于帧间投影颜色差异 $C_{\mathrm{diff}}^{v,t}$ 估计：

$$\xi_{t}^{v} = 1 - \exp(-C_{\mathrm{diff}}^{v,t})$$

不确定性高的区域即被识别为潜在伪影区域，需要后续细化。

**细化前景损失**（CUAR 优化）。对伪影掩模 $M_{t}^{v}$ 标记的前景区域，通过翘曲图像 $\mathrm{warp}_{t}^{v}$ 监督渲染图像 $\mathrm{render}_{t}^{v}$ 进行细化：

$$L_{\mathrm{fore}} = (1-\eta)\|M_{t}^{v}\odot(\mathrm{render}_{t}^{v}-\mathrm{warp}_{t}^{v})\|_{1} + \eta L_{\mathrm{ssim}}(M_{t}^{v}\odot\mathrm{render}_{t}^{v}, M_{t}^{v}\odot\mathrm{warp}_{t}^{v})$$

该损失结合 L1 损失和 SSIM 损失，$\eta$ 为平衡系数。

## 实验与关键发现

### 1. 实验设置

Catalyst4D 在三个具有不同采集特性的动态场景数据集上进行评估：**DyNeRF**（单目多视角）、**MeetRoom**（多相机阵列）和 **HyperNeRF**（单目手持拍摄），覆盖了从精确局部编辑到全局风格迁移的多种任务。对比的基线方法包括三类代表性的 4D 编辑方法：基于 Instruct-Pix2Pix 的 **Instruct 4D-to-4D (IN4D)**、面向 4D Gaussian Splatting 的 **Instruct-4DGS (I4DGS)**，以及基于 DreamBooth 的 **CTRL-D**。所有方法均在相同测试视图上评估，采用 **CLIP 相似度**（语义保真度）和 **VBench 时间一致性**作为核心度量指标。为公平比较，CTRL-D 的风格迁移实验使用与 Catalyst4D 相同的 3D 编辑基线生成的首帧渲染图像作为风格参考。IN4D 使用 2 块 GPU，而 Catalyst4D 在单块 NVIDIA A100 GPU 上完成训练，训练时间约 40–50 分钟。

### 2. 主实验结果

#### 2.1 定量比较

Table 1 报告了在 DyNeRF（Sear-steak、Coffee-martini）和 MeetRoom（Trimming）三个场景上的定量结果。Catalyst4D 在所有场景上均取得了最高的 CLIP 相似度，同时在时间一致性上保持高度竞争力：

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2603_12766/figures/005_Table_1.jpg]]
*Table 1: Quantitative comparison with Instruct 4D-to-4D (IN4D), Instruct-4DGS (I4DGS) and CTRL-D. Bold and underlined denote the best and second-best results, respectively. * indicates 2 GPUs are used. Our method achieves superior semantic fidelity while maintaining highly competitive temporal stability*

- **Sear-steak**：CLIP 相似度 0.252，优于 CTRL-D（0.249）、I4DGS（0.244）和 IN4D（0.232）；一致性 0.983，与 CTRL-D 持平。
- **Coffee-martini**：CLIP 相似度 0.249，优于 CTRL-D（0.246）；一致性 0.986，优于所有对比方法。
- **Trimming**：CLIP 相似度 0.251，优于 CTRL-D（0.248）；一致性 0.967，略低于 CTRL-D（0.969），但显著优于 IN4D（0.951）和 I4DGS（0.943）。

**关键发现**：Catalyst4D 在语义保真度上全面领先，同时维持了极具竞争力的时间稳定性。值得注意的是，IN4D 和 I4DGS 虽然在某些场景下一致性尚可，但 CLIP 相似度显著偏低，反映出其编辑语义传达能力的不足。CTRL-D 作为最强基线，在一致性上与 Catalyst4D 接近，但在语义保真度上始终落后约 0.003，这源于其 2D 扩散编辑缺乏显式几何约束，难以在动态序列中保持编辑语义的精准传递。

#### 2.2 定性比较

Figure 4 展示了与三种基线方法的视觉对比。CTRL-D 等方法在处理局部编辑时，常出现**非目标区域的意外修改**和**编辑边界的模糊扩散**——例如，对特定物体的编辑会“泄漏”到周围背景或相邻物体上。相比之下，Catalyst4D 通过将 3D 编辑与时间传播解耦，实现了精准的局部修改：编辑仅作用于目标区域，非目标区域保持原样。在全局风格迁移任务上（见 Fig. A4），CTRL-D 倾向于产生过度平滑的结果并丢失细节纹理，而 Catalyst4D 在传播风格的同时保留了场景的结构细节和运动一致性。

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2603_12766/figures/004_Figure_4.jpg]]
*Figure 4: Qualitative comparison with Instruct 4D-to-4D, Instruct-4DGS and CTRL-D. Red boxes indicate magnified regions. While competing methods often cause unintended modifications to non-target regions, Catalyst4D demonstrates precise, localized editing*

### 3. 消融实验

为验证两个核心模块的贡献，Table 2 和 Figure 6、Figure 7 报告了系统的消融分析。

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2603_12766/figures/008_Table_2.jpg]]
*Table 2: Quantitative Ablation studies on AMG and CUAR modules. The results show that AMG is critical for establishing correct motion propagation, while CUAR further enhances both semantic and temporal scores by refining appearance consistency*

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2603_12766/figures/007_Figure_6.jpg]]
*Figure 6: Ablation study on the Anchor-based Motion Guidance. Our method effectively avoids geometric distortions caused by incorrect motion propagation*

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2603_12766/figures/009_Figure_7.jpg]]
*Figure 7: Ablation study on the Color Uncertainty-guided Appearance Refinement (CUAR). It significantly enhances visual fidelity by mitigating color artifacts*

#### 3.1 Anchor-based Motion Guidance (AMG) 的作用

**去除 AMG（w/o AMG）** 意味着直接复用原始变形网络来驱动编辑后高斯的运动，而不建立区域级对应。定量结果显示：
- CLIP 相似度从 0.252 降至 0.245（−0.007）
- 时间一致性从 0.971 降至 0.966（−0.005）

Figure 6 的定性结果表明，缺少 AMG 时，编辑后高斯因缺乏正确的运动引导而出现明显的**几何畸变**——物体部件发生错位、拉伸或断裂。这验证了 AMG 通过锚点对应和最优传输建立区域级变形传播的必要性：直接复用原始变形场无法处理编辑引入的几何变化，会导致运动漂移和跨区域干扰。

#### 3.2 Color Uncertainty-guided Appearance Refinement (CUAR) 的作用

**去除 CUAR（w/o CUAR）** 后，CLIP 相似度降至 0.248（−0.004），一致性降至 0.969（−0.002）。Figure 7 显示，缺少 CUAR 的编辑结果在动态序列中出现明显的**颜色伪影和闪烁**，尤其是在遮挡边界区域——这些区域因高斯在帧间被遮挡/显现而缺乏稳定的外观监督。CUAR 通过估计高斯颜色不确定性并利用首帧翘曲图像作为伪真值，选择性地纠正了这些由遮挡引起的外观不一致，从而提升了视觉保真度。

#### 3.3 锚点构建策略的影响

Figure 5 比较了不同的锚点构建方法。Catalyst4D 采用的**自适应圆柱体过滤策略**（仅在多个邻近高斯持续落入自适应定义的圆柱体时才生成锚点）能够有效筛选出结构稳定、空间代表性的锚点，避免了基于简单距离阈值或随机采样方法产生的噪声锚点和不稳定对应。这一设计对于后续最优传输匹配的质量至关重要。

### 4. 失败模式与局限性分析

尽管 Catalyst4D 在多数场景下表现优异，但分析揭示了以下边界条件和失败模式：

1. **对初始 3D 编辑质量的依赖**：Catalyst4D 的时间传播建立在首帧 3D 编辑结果之上。若 3D 编辑本身缺乏足够的空间一致性（例如，不同视角下编辑效果不一致），这种不一致会被传播到整个动态序列，导致时空一致性的退化。这意味着 Catalyst4D 的性能上限受限于所采用的 3D 编辑器。

2. **对底层 4D 重建稳定性的依赖**：方法未修改变形网络或重新优化高斯密度，因此依赖于底层 4D 重建的质量。在存在严重重建噪声的场景中（如点抖动、低不透明度高斯、运动模糊区域），AMG 的运动引导可能局部失效，导致编辑后高斯出现不自然的运动轨迹。

3. **极端拓扑变化的挑战**：虽然 AMG 中的 Sinkhorn 算法在广泛正则化范围内表现出稳定的对应关系（Fig. A3 通过 NDD 指标验证），但在涉及大幅度拓扑结构变化（如物体分裂、融合）的编辑场景中，锚点对应可能难以完全捕捉这种非连续变形，仍有待进一步探索。

### 5. 补充定量证据

在补充材料中，Table A1 使用 **EditScore** 和 **VE-Bench** 指标进一步验证了 Catalyst4D 的优势。Table A2 的消融实验在额外指标上确认了 AMG 和 CUAR 的独立贡献。这些结果与主实验结论一致，强化了方法设计的有效性。

## 定位与知识库关联

### 1. 方法谱系：从 2D 编辑传播到 3D 原生编辑的范式迁移

Catalyst4D 的核心创新在于将动态场景编辑从“2D 扩散模型直接拟合 4D 表示”的范式，迁移到“先 3D 编辑，再 4D 传播”的解耦架构。这一转变直接针对现有方法的瓶颈：2D 扩散模型缺乏显式几何推理，在扩展到 4D 动态场景时不可避免地产生运动伪影、时间闪烁和非目标区域的意外变化。

在方法谱系上，Catalyst4D 与以下基线工作形成对比：

- **Instruct 4D-to-4D**（IN4D）：采用文本引导的 4D 编辑方法，直接从 2D 扩散编辑帧拟合 4D 表示。该方法需要 2 块 GPU 进行训练，而 Catalyst4D 在单块 NVIDIA A100 GPU 上即可完成训练（40–50 分钟），训练效率更具竞争力。然而，IN4D 的 2D-to-4D 管道缺乏对几何结构的显式建模，容易导致运动传播错误。

- **Instruct-4DGS**（I4DGS）：基于 4D Gaussian Splatting 的编辑方法，同样遵循从 2D 编辑到 4D 拟合的路径。该方法受限于 4D 高斯表示的固有复杂性，在局部编辑精度上存在不足，常出现非目标区域的误修改。

- **CTRL-D**：基于 DreamBooth 风格的 4D 编辑方法，在语义保真度上表现较强（在 DyNeRF 和 MeetRoom 基准上 CLIP 相似度仅次于 Catalyst4D），但其 2D 扩散驱动的编辑方式容易造成模糊、过度平滑和非目标区域的误修改，尤其在局部编辑任务上表现不佳。

Catalyst4D 的关键差异在于**编辑传播管道的重构**：将编辑操作限定在首帧的 3D 高斯表示上（利用现有的 3D 高斯编辑器如 DGE、DreamCatalyst、SGSST），然后通过 Anchor-based Motion Guidance（AMG）和 Color Uncertainty-guided Appearance Refinement（CUAR）两个模块，将编辑结果传播至全部时间帧。这种“3D-to-4D”的解耦设计，使编辑后的场景既能保留静态 3D 编辑的灵活性和高保真度，又能维持动态序列所需的结构一致性和时间稳定性。

### 2. 知识库定位：几何驱动的运动传播与不确定性感知的外观细化

Catalyst4D 在知识库中的定位可以从两个技术模块来理解：

**Anchor-based Motion Guidance（AMG）的几何推理贡献**：AMG 模块通过构建锚点并利用非平衡最优传输（Sinkhorn 算法）建立区域级对应关系，解决了现有方法中运动传播的核心难题。基线方法通常采用 KNN 插值或直接复用原始变形网络来传播编辑后高斯的运动，这容易导致运动漂移和跨区域干扰——即编辑后高斯错误地跟随非对应区域的运动轨迹。AMG 通过以下机制克服了这一局限：

1. **锚点构建**：从原始和编辑后的首帧高斯云中提取结构稳定、空间代表性的锚点。锚点的生成条件是多个邻近高斯在自适应定义的圆柱体内一致分布（见 Fig. 5），这确保了锚点的几何稳定性和区域代表性。
2. **最优传输对应**：通过 Sinkhorn 算法在锚点间建立区域级对应关系，避免了逐点匹配的噪声敏感性。消融实验表明，在极端拓扑变化下，Sinkhorn 算法表现出稳定的对应关系，NDD 指标在广泛正则化范围内保持稳定（Fig. A3）。
3. **变形聚合**：编辑后高斯的位置变形通过对应源高斯变形的加权平均得到（Eq. 9），权重结合了不透明度和马氏距离（Eq. 10），实现了局部一致的变形传播。

消融实验（Table 2）证实了 AMG 的关键作用：去除 AMG 后，CLIP 相似度从 0.252 降至 0.245，时间一致性从 0.971 降至 0.966，且出现明显的几何失真（Fig. 6）。

**Color Uncertainty-guided Appearance Refinement（CUAR）的外观细化贡献**：CUAR 模块通过量化高斯颜色不确定性，选择性纠正因遮挡导致的外观伪影。其核心机制包括：

1. **颜色不确定性估计**：基于帧间投影颜色差异估计每个高斯的颜色不确定性 $\xi_{t}^{v} = 1 - \exp(-C_{\mathrm{diff}}^{v,t})$（Eq. 15），生成伪影掩模。
2. **伪真值监督**：利用首帧图像翘曲（warping）生成伪真值，结合前景细化损失 $L_{\mathrm{fore}}$（Eq. 18）进行选择性外观细化。

消融实验（Table 2, Fig. 7）表明，去除 CUAR 后 CLIP 相似度和一致性均有下降（0.248 vs 0.252, 0.969 vs 0.971），并出现明显的颜色伪影和闪烁。

### 3. 适用边界与局限

Catalyst4D 的适用边界受以下因素制约：

1. **初始 3D 编辑质量的依赖性**：方法的时间连续性受初始 3D 编辑质量的影响。若 3D 编辑结果缺乏足够的空间一致性（例如编辑操作本身引入了多视角不一致），这种不一致可能通过传播管道波及最终动态输出的时空一致性。这意味着 Catalyst4D 的性能上限受限于所采用的 3D 编辑器。

2. **底层 4D 重建的稳定性要求**：方法未修改变形网络或重新优化高斯密度，因此依赖于底层 4D 重建的质量。在严重重建噪声（如点抖动、低不透明度高斯）的情况下，运动引导可能局部失效。这是因为 AMG 的锚点构建和变形聚合都依赖于源高斯云的结构完整性。

3. **极端拓扑变化的鲁棒性**：虽然 Sinkhorn 算法在实验中表现出一定的稳定性，但方法对具有极端拓扑结构变化的编辑（如物体的添加/删除、大范围形变）的鲁棒性仍有待探索。这是论文明确指出的开放问题之一。

### 4. 开放问题与未来方向

论文指出的开放问题包括：

- **极端编辑的适应性**：如何使方法对具有极端拓扑结构变化的编辑更加鲁棒，例如物体的完全移除或新增，以及大范围的非刚性形变。
- **高不确定性序列的适应**：如何适应不确定性更高的动态序列，例如快速运动、严重遮挡或光照剧烈变化的场景。在这些场景中，颜色不确定性估计和运动对应关系可能面临更大的挑战。
- **与 3D 编辑器的协同优化**：当前方法将 3D 编辑视为黑盒外部模块，未来可探索 3D 编辑与 4D 传播的联合优化，以在编辑阶段就考虑时间传播的约束，从而提升整体一致性。

## 原文 PDF

![[paperPDFs/CVPR_2026/Catalyst4D_High_Fidelity_3D_to_4D_Scene_Editing_via_Dynamic_Propagation.pdf]]
