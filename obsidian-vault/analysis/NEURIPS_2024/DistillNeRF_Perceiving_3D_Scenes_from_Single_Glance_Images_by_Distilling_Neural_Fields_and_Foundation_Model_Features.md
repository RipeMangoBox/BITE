---
title: "DistillNeRF: Perceiving 3D Scenes from Single-Glance Images by Distilling Neural Fields and Foundation Model Features"
type: paper
paper_level: A
venue: NeurIPS
year: 2024
pdf_ref: paperPDFs/NEURIPS_2024/DistillNeRF_Perceiving_3D_Scenes_from_Single_Glance_Images_by_Distilling_Neural_Fields_and_Foundation_Model_Features.pdf
project_link: https://distillnerf.github.io/
code_link: null
aliases:
- DistillNeRF
tags:
- NEURIPS_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "通过离线优化、具备动静态分解的每场景NeRF（EmerNeRF）生成稠密深度图和虚拟相机视图作为附加几何监督，同时从2D视觉基础模型（CLIP、DINOv2）蒸馏语义特征，从而在无需逐场景优化的前馈模型中注入精确的几何与丰富的语义。"
primary_logic: "将离线NeRF的强大重建能力与2D基础模型的语义潜力，通过知识蒸馏统一迁移到可泛化前馈模型中，使模型能够在单帧稀疏多视角输入下实时预测高质量的3D神经场景表示，同时实现渲染、深度估计、零样本语义占用预测和开放词汇查询。"
claims:
- "DistillNeRF在RGB重建上达到与逐场景优化的EmerNeRF相当的水平（PSNR 30.11 vs 30.88, SSIM 0.917 vs 0.879），并远超可泛化SOTA（SelfOcc PSNR 20.67, UniPAD 19.44）。"
- "通过蒸馏离线NeRF的稠密深度和虚拟相机，模型在稠密深度估计的Abs Rel达到0.228，显著优于SelfOcc (0.348)和UniPAD (0.276)。"
- "消融实验显示移除深度蒸馏导致PSNR从30.11降至28.01，移除预训练2D编码器则降至21.35，表明核心组件的关键作用。"
- "模型能够零样本生成语义占用，在Occ3D-nuScenes上的mIoU达到8.93（有蒸馏），而无蒸馏仅为4.63。"
---

# DistillNeRF: Perceiving 3D Scenes from Single-Glance Images by Distilling Neural Fields and Foundation Model Features

> [!tip] 核心洞察
> 将离线NeRF的强大重建能力与2D基础模型的语义潜力，通过知识蒸馏统一迁移到可泛化前馈模型中，使模型能够在单帧稀疏多视角输入下实时预测高质量的3D神经场景表示，同时实现渲染、深度估计、零样本语义占用预测和开放词汇查询。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | DistillNeRF：通过蒸馏神经场和基础模型特征从单幅图像感知3D场景 |
| 英文题名 | DistillNeRF: Perceiving 3D Scenes from Single-Glance Images by Distilling Neural Fields and Foundation Model Features |
| 会议/期刊 | NeurIPS 2024 |
| Links | [paper](https://arxiv.org/abs/2406.12095) · [Project](https://distillnerf.github.io/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | DistillNeRF |
| Dataset | nuScenes validation set, nuScenes (Dense Depth GT), Waymo NOTR (zero-shot transfer, after finetuning) |

> [!tip] 效果简介
> - nuScenes validation set 上，RGB Reconstruction PSNR / SSIM 为 30.11 / 0.917，对比 EmerNeRF (per-scene): 30.88 / 0.879; SelfOcc: 20.67 / 0.556; UniPAD: 19.44 / 0.497，变化 接近每场景优化方法，PSNR略低0.77，SSIM更高0.038；比最佳可泛化方法SelfOcc高45.6% PSNR。
> - nuScenes validation set 上，Novel-View Synthesis PSNR / SSIM 为 20.78 / 0.590，对比 Single-Frame EmerNeRF: 20.95 / 0.585; SelfOcc: 18.22 / 0.464; UniPAD: 16.45 / 0.375，变化 与每场景优化方法相当，SSIM稍高；比SelfOcc高14.0% PSNR。
> - nuScenes (Dense Depth GT) 上，Abs Rel ↓ 为 0.228 (Depth+Virt Distill)，对比 SelfOcc: 0.348; UniPAD: 0.276，变化 相对误差降低34.5% vs SelfOcc。

## 概要

自动驾驶场景中的3D场景感知面临一个根本性瓶颈：车载相机视角稀疏且重叠区域有限，导致基于前馈模型的可泛化NeRF存在严重的深度与几何模糊，其重建质量远不及需要逐场景离线优化的NeRF方法。DistillNeRF针对这一瓶颈，提出了一种知识蒸馏驱动的可泛化框架——将离线NeRF的强大几何重建能力与2D视觉基础模型的丰富语义，统一迁移到前馈模型中，使模型能够在单帧多视角图像输入下实时预测高质量的3D神经场景表示。

核心思路是双源蒸馏：一方面，利用具备动静态分解能力的离线NeRF（**EmerNeRF**）生成稠密深度图和虚拟相机视图，为前馈模型注入精确的几何监督；另一方面，从CLIP和DINOv2等2D基础模型蒸馏语义特征，赋予模型开放词汇理解能力。通过这种“教师-学生”范式，DistillNeRF无需测试时的逐场景优化，即可在单次前向推理中完成渲染、深度估计、零样本语义占用预测和开放词汇查询。

实验结果表明，DistillNeRF在nuScenes验证集上的RGB重建PSNR达到30.11，与逐场景优化的EmerNeRF（30.88）相当，SSIM（0.917）甚至更高，同时远超可泛化SOTA方法SelfOcc（20.67）和UniPAD（19.44）。在稠密深度估计上，Abs Rel降至0.228，较SelfOcc降低34.5%。消融实验进一步揭示，移除深度蒸馏会使PSNR从30.11骤降至28.01，而移除预训练2D编码器则导致PSNR崩塌至21.35，验证了几何蒸馏与语义先验的核心作用。在跨数据集泛化方面，模型在Waymo NOTR上微调后PSNR达到29.84，甚至超越了在该数据集上逐场景优化的EmerNeRF（28.87），展现出强大的迁移能力。

在方法谱系上，DistillNeRF定位为可泛化前馈NeRF，与逐场景优化的EmerNeRF形成“教师-学生”关系，同时显著超越同为可泛化方法的SelfOcc和UniPAD。其关键创新在于将知识蒸馏从传统的模型压缩范式，拓展为连接离线优化质量与实时推理效率的桥梁，为自动驾驶场景的3D表征学习提供了新的技术路径。

### 自动驾驶场景下的3D感知困境

自动驾驶系统需要从有限的2D传感器观测中理解复杂的3D环境。与传统的物体级3D重建不同——后者通常采用“向内”的多视角设置，即大量相机环绕目标物体进行密集拍摄——自动驾驶场景面临截然不同的挑战（Figure 5）。车载相机呈“向外”的稀疏布局，相邻相机之间的重叠区域极为有限，导致基于多视图几何的深度推断面临严重的模糊性。同时，场景中的物体分布在从近处到远方的广阔范围内，像素占用极不均匀：近处物体占据大量像素但只需粗略深度即可定位，而远处物体仅占极少像素却需要精确的深度估计才能正确重建。

这种稀疏、重叠有限的多相机配置，使得从单帧图像学习准确的3D表征成为一个本质上的病态问题。

### 现有方法的局限性

当前解决这一问题的技术路线大致分为两类：

**逐场景优化的NeRF**（如**EmerNeRF**）能够通过大量迭代优化，对单个场景学习高质量的几何与外观表示，甚至实现动静态分解，生成稠密的深度图和逼真的新视角合成。然而，这类方法需要在每个新场景上进行耗时的测试时优化（通常需要数分钟到数十分钟），无法满足自动驾驶对实时性的要求。

**可泛化的前馈NeRF方法**（如**SelfOcc**、**UniPAD**）试图通过单次前向传播直接从多视图图像预测3D场景表示，无需逐场景优化，因而推理速度较快。但这些方法在重建质量上远逊于逐场景优化的NeRF：在nuScenes验证集上，SelfOcc的RGB重建PSNR仅为20.67，UniPAD更是只有19.44，而逐场景优化的EmerNeRF达到30.88（Table 1）。这种巨大差距的根源在于，稀疏的相机视角使得前馈模型难以仅凭RGB重建损失学习到精确的深度和几何信息——深度模糊问题未得到有效解决。

### 核心瓶颈与突破动机

上述困境揭示了一个关键瓶颈：**自动驾驶场景中相机视角稀疏且重叠有限，导致基于前馈模型的可泛化NeRF面临严重的深度/几何模糊，难以从单帧多视角图像学习准确的3D表征**。

这引出了一个自然的动机：能否将离线NeRF的强大重建能力“迁移”到可泛化前馈模型中？具体而言，离线NeRF在逐场景优化后能生成稠密的深度图和高质量的虚拟视角渲染，这些信息恰好可以作为额外的几何监督信号，弥补稀疏视角下的深度模糊。同时，2D视觉基础模型（如CLIP、DINOv2）已在海量数据上学习了丰富的语义特征，若能将其蒸馏到3D场景表示中，则有望赋予模型超越纯几何重建的语义理解能力。

DistillNeRF正是沿着这一思路，通过知识蒸馏将离线NeRF的几何精确性与基础模型的语义丰富性统一注入到可泛化前馈模型中，使模型能够在单帧稀疏多视角输入下实时预测高质量的3D神经场景表示，同时实现渲染、深度估计、零样本语义占用预测和开放词汇查询。

## 核心方法与创新机理

DistillNeRF 的核心创新在于将**离线逐场景优化 NeRF 的精确几何**与**2D 视觉基础模型的丰富语义**，通过知识蒸馏统一迁移到可泛化的前馈模型中，使模型在单帧稀疏多视角输入下即可实时预测高质量的 3D 神经场景表示。这一思路直接回应了自动驾驶场景的核心瓶颈：相机视角稀疏且重叠有限，导致基于前馈模型的可泛化 NeRF 面临严重的深度/几何模糊，远不及逐场景优化的 NeRF。

围绕上述目标，DistillNeRF 在以下四个关键维度上对 baseline 方法（如 SelfOcc、UniPAD 等可泛化 NeRF）进行了系统性改进：

### 1. 两阶段由粗到精的概率性深度预测

传统 LSS（Lift-Splat-Shoot）方法一次性预测类别深度分布，难以捕捉精细的深度结构。DistillNeRF 提出两阶段策略：

- **第一阶段**：预测离散深度候选的概率分布，通过光线行进（ray marching）计算每个像素的体素占用权重 $\mathbb{O}(h,w,d)$，并聚合成粗深度估计 $\mathbb{D}(h,w)$（见 Eq 1-2）。
- **第二阶段**：以粗深度为中心，在其邻域内动态采样更细粒度的深度候选，再次预测概率分布。

消融实验证实，将两阶段 LSS 替换为传统单阶段 LSS 会导致 RGB 重建 PSNR 从 28.01 降至 27.40（Table 5），验证了粗到细深度预测对几何准确性的贡献。

### 2. 稀疏层次化双八叉树体素表示

Baseline 方法通常采用密集固定分辨率体素（如 UniPAD、SelfOcc 的有限范围密集网格），在处理大规模驾驶场景时空区域浪费计算，远区域分辨率不足。DistillNeRF 引入**稀疏层次化双八叉树**：

- 维护一个细节八叉树和一个粗粒度八叉树，仅对非空区域分配体素。
- 渲染时优先从细八叉树采样，空缺处由粗八叉树补齐（密度互补机制）。
- 应用稀疏卷积编码体素间交互，兼顾效率与表示能力。

消融实验表明，移除密度互补机制（仅使用细八叉树）使 PSNR 从 28.01 骤降至 22.76（Table 5），证明粗细八叉树协同对处理远处区域和空区域至关重要。

### 3. 参数化神经场处理无界场景

传统方法通常限定固定范围（如 50m），直接忽略远处几何。DistillNeRF 采用参数化坐标变换 $f(p)$（Eq 3），将无界世界坐标映射到 $[0,1]$ 的参数空间：内部区域（$|p| \le p_{inner}$）保持线性缩放以保留高分辨率细节，外部区域渐进收缩以支持无界场景表示。这使得模型能够同时处理近处精细结构和远处背景，而不受固定范围限制。

### 4. 多源知识蒸馏训练范式

这是 DistillNeRF 区别于所有可泛化 baseline 的根本性创新。训练监督从单一的 RGB 重建损失扩展为**渲染损失 + 蒸馏损失**的组合（Eq 4）：

- **离线 NeRF 蒸馏**（$L_{NeRF}$）：利用逐场景优化的 EmerNeRF 生成稠密深度图和虚拟相机视图，为前馈模型提供精确的几何监督。消融实验显示，增加深度蒸馏将 PSNR 从 28.01 提升至 30.11（Table 5），说明外部几何监督对解决稀疏视角下的深度模糊具有决定性作用。
- **基础模型特征蒸馏**（$L_{found}$）：从 CLIP 和 DINOv2 等 2D 视觉基础模型提取特征向量作为回归目标，使模型在 3D 体素空间中隐式学习语义信息。移除预训练 2D 编码器（即无基础模型先验）会导致 PSNR 从 28.01 剧降至 21.35（Table 5），凸显预训练特征在下游几何学习中的关键作用。

### 创新总结

上述四个 changed slots 形成了一条清晰的因果链：**两阶段深度预测**提供更准确的 2D→3D 提升 → **稀疏层次体素**高效表示大规模场景 → **参数化坐标变换**处理无界范围 → **多源蒸馏**注入离线 NeRF 的精确几何和基础模型的语义先验。这些创新共同使 DistillNeRF 在 RGB 重建上达到与逐场景优化的 EmerNeRF 相当的水平（PSNR 30.11 vs 30.88，SSIM 0.917 vs 0.879），并远超可泛化 SOTA（SelfOcc PSNR 20.67，UniPAD 19.44），同时支持零样本语义占用预测和开放词汇查询等 emergent capability。

DistillNeRF 是一个面向室外自动驾驶场景的可泛化前馈模型，其核心设计目标是从**单时间步的多视角相机图像**出发，在不进行任何测试时逐场景优化的情况下，实时预测高质量的 3D 场景表示。该框架由三个紧密耦合的模块构成：单视图两阶段 LSS 编码器、多视图融合与稀疏层次化体素构建、以及可微体积渲染，整体架构如 Figure 2 所示。

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2406_12095/figures/002_Figure_2.jpg]]
*Figure 2: DistillNeRF model architecture. (left) single-view encoding with two-stage probabilistic depth prediction; (center) multi-view pooling into a sparse hierarchical voxel representation using sparse quantization and convolution; (right) volumetric rendering from sparse hierarchical voxels*

**输入与特征提取**：模型接收 $N$ 张已标定位姿的 RGB 相机图像 $\{I_i\}_{i=1}^N$，首先通过一个 2D 骨干网络（基于预训练视觉编码器）提取对应的特征图 $\{X_i\}_{i=1}^N$。该预训练编码器被证明是下游几何学习的关键——消融实验中将其替换为随机初始化编码器会导致 RGB 重建 PSNR 从 28.01 骤降至 21.35（Table 5）。

**单视图两阶段 LSS 编码器**：对每幅特征图，模型执行由粗到精的概率性深度预测（Section 3.1）。第一阶段预测离散深度类别的概率分布，并通过光线行进将其聚合为粗深度估计 $\mathbb{D}(h,w) = \sum_{d=1}^{D} \mathbb{O}(h,w,d) t_d$，其中 $\mathbb{O}(h,w,d)$ 为像素 $(h,w)$ 在深度候选 $d$ 处的体素占用权重（Eq 1-2）。第二阶段在粗深度附近动态采样更细粒度的深度候选，再次预测概率分布，从而获得更准确的深度。随后，像素特征依据预测的深度概率被提升到 3D 视锥体空间。消融实验表明，将两阶段 LSS 替换为传统单阶段 LSS 会使 PSNR 从 28.01 降至 27.40（Table 5），证实了粗到细策略对几何精度的贡献。

**多视图融合与稀疏体素构建**：各视图的视锥体被变换到统一的世界坐标系，通过平均池化融合到共享的稀疏层次化双八叉树体素中。该表示包含一个细节八叉树和一个粗粒度八叉树：细八叉树负责捕获近景高分辨率细节，粗八叉树填补远处区域的几何空缺。随后应用稀疏卷积编码体素间的空间交互。移除密度互补机制（仅使用细八叉树）会导致 PSNR 从 28.01 降至 22.76（Table 5），凸显了粗细八叉树协同对处理无界场景远处区域的必要性。

**参数化坐标变换**：为处理自动驾驶场景的无界特性，模型引入参数化神经场坐标映射（Eq 3）。世界坐标 $p$ 在内部区域 $|p| \le p_{inner}$ 保持线性缩放，在外部区域则渐进收缩至 $[0,1]$ 区间，使得有限体素分辨率能够同时覆盖近处精细几何与远处结构。

**可微体积渲染与解码**：从稀疏层次体素沿光线采样点，优先查询细八叉树的特征与密度，空缺处由粗八叉树补齐。经两阶段采样（均匀采样 + 重要性采样）后，通过体积渲染生成 2D 特征图，再经由 CNN 解码器上采样得到最终 RGB 输出。移除 CNN 解码器会使 PSNR 从 28.01 降至 25.76（Table 5），表明解码器能有效抑制渲染特征中的噪声并恢复高频细节。

**多源蒸馏训练**：模型的总训练目标为渲染损失与蒸馏损失的线性组合（Eq 4）：
$$L = \underbrace{L_{rgb} + L_{depth} + L_{density}}_{\text{rendering}} + \underbrace{L_{NeRF} + L_{found}}_{\text{distillation}}$$
其中 $L_{rgb}$ 结合 L2 损失与 LPIPS 感知损失（Appendix Eq 6），$L_{depth}$ 为归一化 L1 和 MSE 深度损失（Appendix Eq 7），$L_{density}$ 为密度熵损失以鼓励清晰表面。蒸馏部分 $L_{NeRF}$ 利用离线逐场景优化的 EmerNeRF 教师模型生成的稠密深度图和虚拟相机视图作为额外几何监督，$L_{found}$ 则从 CLIP 和 DINOv2 等 2D 视觉基础模型蒸馏语义特征。消融实验显示，增加深度蒸馏将 PSNR 从 28.01 提升至 30.11（Table 5），是解决稀疏视角下深度模糊的决定性因素。

**推理流程**：给定单帧多视角图像，模型经单视图编码→多视图融合→体积渲染的端到端前向传播，即可同时输出 RGB 重建、深度估计和基础模型特征渲染，无需任何测试时优化。在 RTX 4090 上以 228×128 分辨率推理，整体速度显著优于逐场景优化的 EmerNeRF（Table 7）。

DistillNeRF 的核心设计围绕三个关键模块展开：单视图两阶段深度预测、稀疏层次化体素表示、以及多源蒸馏训练。以下逐一阐述其机制与关键公式。

### 单视图两阶段深度预测

传统 LSS 方法一次性预测类别深度分布，在稀疏视角下难以捕捉精细的几何结构。DistillNeRF 提出两阶段由粗到精的概率性深度预测策略（Section 3.1, Figure 2 left）：

**第一阶段**：对每幅相机图像提取 2D 特征后，预测离散深度候选上的类别概率，并通过光线行进聚合为粗深度估计。像素 $(h,w)$ 在深度候选 $d$ 处的体素占用权重定义为：

$$\mathbb{O}(h,w,d) = \exp\left(-\sum_{j=1}^{d-1} \delta_j \sigma_{h,w,j}\right) \big(1 - \exp(-\delta_d \sigma_{h,w,d})\big) \tag{Eq 1}$$

其中 $\sigma_{h,w,d}$ 为预测的密度值，$\delta_d$ 为相邻深度候选的间距。该公式模拟了沿光线的透射率与当前体素的吸收概率。

随后通过加权求和得到粗深度估计：

$$\mathbb{D}(h,w) = \sum_{d=1}^{D} \mathbb{O}(h,w,d) \, t_d \tag{Eq 2}$$

其中 $t_d$ 为第 $d$ 个深度候选的实际深度值。

**第二阶段**：以 $\mathbb{D}(h,w)$ 为中心，在附近动态采样更细粒度的深度候选，再次预测概率分布。这种粗到细的策略使模型能在计算可控的前提下获取更准确的深度几何。

### 稀疏层次化双八叉树体素

为高效处理自动驾驶场景中大量空区域与远端细节的并存问题，DistillNeRF 采用稀疏层次化体素表示（Section 3.1, Figure 2 center）：

- **细八叉树**：存储高分辨率细节信息，覆盖场景中的关键区域。
- **粗八叉树**：以较低分辨率覆盖更大范围，填补细八叉树中的空缺区域。
- 多视图特征通过平均池化融合到共享的稀疏体素中，随后应用稀疏卷积编码体素间交互。

在体积渲染时，沿光线优先查询细八叉树的特征与密度；若对应位置为空，则回退至粗八叉树。这种密度互补机制确保了对远处区域的有效覆盖。

### 无界场景的参数化坐标映射

为处理自动驾驶中无界的场景范围，DistillNeRF 引入参数化坐标变换（Section 3.1, Eq 3）：

$$f(p) = \begin{cases} \alpha \dfrac{p}{p_{inner}} & |p| \le p_{inner} \\ \left(1 - \dfrac{p_{inner}}{|p|}(1-\alpha)\right) \dfrac{p}{|p|} & |p| > p_{inner} \end{cases} \tag{Eq 3}$$

其中 $p = (x, y, z)$ 为世界坐标，$p_{inner}$ 为内部区域半径，$\alpha$ 为收缩系数。内部区域保持线性缩放以保留真实比例与高分辨率，外部区域渐进收缩映射到 $[0,1]$ 的参数空间，使模型能以有限体素分辨率表达无界场景。

### 多源蒸馏训练目标

总损失由渲染损失和蒸馏损失线性组合而成（Section 3.2, Eq 4）：

$$L = \underbrace{L_{rgb} + L_{depth} + L_{density}}_{\text{rendering}} + \underbrace{L_{NeRF} + L_{found}}_{\text{distillation}} \tag{Eq 4}$$

- **$L_{rgb}$**：结合 L2 损失与 LPIPS 感知损失的 RGB 重建损失。
- **$L_{depth}$**：归一化的 L1 和 MSE 深度损失，监督预测深度图。
- **$L_{density}$**：密度熵损失，鼓励形成清晰的表面和结构化的密度分布。
- **$L_{NeRF}$**：来自离线逐场景优化的 EmerNeRF 的稠密深度和虚拟相机视图提供的 RGB/深度监督。
- **$L_{found}$**：从 2D 视觉基础模型（CLIP、DINOv2）蒸馏的特征重建损失，将语义知识注入 3D 表征。

这种多源蒸馏策略的核心洞察在于：将离线 NeRF 的强大几何重建能力与 2D 基础模型的语义潜力，通过知识蒸馏统一迁移到可泛化前馈模型中，使其在单帧稀疏多视角输入下即可实时预测高质量的 3D 神经场景表示。

## 实验与关键发现

### 核心实验设置

DistillNeRF 在 nuScenes 数据集上训练，并在验证集的未见场景上评估。所有可泛化方法均不进行测试时逐场景优化。新视角合成任务使用下一时刻的相机姿态渲染图像，与下一时刻的真值图像比较；为确保公平，基线 EmerNeRF 仅用单时间步训练（Single-Frame EmerNeRF）。深度估计同时评估稀疏 LiDAR 真值和 EmerNeRF 渲染的稠密深度真值，以揭示不同监督信号的影响。推理速度在相同硬件（RTX 4090）和分辨率（228×128）下测量。

### 主结果分析

**RGB 重建与新视角合成。** Table 1 展示了 nuScenes 验证集上的核心结果。DistillNeRF 在 RGB 重建上达到 PSNR 30.11 / SSIM 0.917，与逐场景优化的 EmerNeRF（PSNR 30.88 / SSIM 0.879）相当——PSNR 仅低 0.77 dB，而 SSIM 反超 0.038。相比可泛化 SOTA 方法，优势极为显著：SelfOcc 的 PSNR 为 20.67，UniPAD 为 19.44，DistillNeRF 的 PSNR 相对提升 45.6% 和 54.9%。在新视角合成任务上，DistillNeRF 达到 PSNR 20.78 / SSIM 0.590，与 Single-Frame EmerNeRF（20.95 / 0.585）几乎持平，且显著优于 SelfOcc（18.22 / 0.464，PSNR 提升 14.0%）和 UniPAD（16.45 / 0.375）。这表明，通过蒸馏离线 NeRF 的几何知识，可泛化前馈模型能够弥合与逐场景优化方法之间的性能鸿沟。

**深度估计。** Table 2 报告了深度估计结果。在稠密深度真值（EmerNeRF 渲染）下，DistillNeRF 的 Abs Rel 达到 0.228，显著优于 SelfOcc（0.348）和 UniPAD（0.276），相对误差分别降低 34.5% 和 17.4%。在稀疏 LiDAR 真值下，DistillNeRF 同样表现最优（Abs Rel 0.265 vs SelfOcc 0.303）。这验证了来自离线 NeRF 的稠密深度蒸馏对解决稀疏视角下深度模糊的关键作用——离线 NeRF 通过动静态分解和多帧优化获得了更完整的几何先验，DistillNeRF 将其蒸馏至前馈模型中。

**跨数据集泛化。** Table 3 和 Figure 4 展示了 nuScenes → Waymo NOTR 的零样本迁移能力。零样本条件下，DistillNeRF 已能产生可辨认的重建结果；经简单色彩校正后质量进一步提升；微调后 PSNR 达到 29.84 / SSIM 0.911，超越逐场景优化的 EmerNeRF（28.87 / 0.814）。这证明蒸馏得到的表征具有良好的跨域鲁棒性，而非对训练集场景的过拟合。

**零样本语义占用预测。** Table 4 展示了在 Occ3D-nuScenes 上的无监督 3D 占用预测结果。DistillNeRF（有蒸馏）的 mIoU 达到 8.93，而无蒸馏版本仅为 4.63，表明从 2D 基础模型（CLIP、DINOv2）蒸馏的语义特征能有效迁移至 3D 体素空间，使模型在没有任何 3D 语义标注的情况下学习到合理的语义占用。

### 消融实验

Table 5 系统消融了各核心组件的贡献（基线为无深度蒸馏的 DistillNeRF，PSNR 28.01）：

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2406_12095/figures/010_Table_5.jpg]]
*Table 5: Ablation studies on key components in our model*

- **移除深度蒸馏**：PSNR 从 30.11 降至 28.01，降幅 2.10 dB。这是所有消融项中影响最大的单因素，直接证明了离线 NeRF 稠密深度监督是解决稀疏多视角几何模糊的瓶颈性组件。
- **移除预训练 2D 编码器**（随机初始化）：PSNR 剧降至 21.35，SSIM 降至 0.536。这表明预训练特征中蕴含的语义先验对下游几何学习有极强的引导作用，缺乏该先验时模型几乎无法收敛到有效解。
- **移除密度互补机制**（仅使用细八叉树）：PSNR 从 28.01 降至 22.76。粗细八叉树的协同设计对处理远处区域至关重要——细八叉树覆盖近景高分辨率区域，粗八叉树填补远景空缺，单独使用细八叉树会导致远处几何严重退化。
- **移除 CNN 解码器**：PSNR 从 28.01 降至 25.76。渲染后的 CNN 解码器能有效抑制体素渲染特征中的噪声并恢复高频细节。
- **将两阶段 LSS 替换为传统单阶段 LSS**：PSNR 从 28.01 降至 27.40。粗到细的概率性深度预测相比一次性分类深度能获取更准确的深度估计，进而提升 3D 体素构建质量。

定性消融（Figure 7）进一步展示了深度蒸馏和参数化空间的关键作用：无深度蒸馏时深度预测出现明显不一致；无参数化空间时深度范围受限；引入参数化空间后能合理处理无界深度。

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2406_12095/figures/005_Table_1.jpg]]
*Table 1: Reconstruction and novel-view synthesis on nuScenes validation set. DistillNeRF is on par with the per-scene optimized NeRFs, both in RGB and foundation feature rendering, and significantly outperforms SOTA generalizable NeRF methods. In the DistillNeRF variants, we denote ’Depth’ as the depth distillation from offline NeRFs, ’Param.’ as the parameterized space, and ’Virt.’ as the distillation from virtual cameras in offline NeRFs. See Fig. 6 and Fig. 7 for qualitative results*

### 效率分析

Table 7 报告了推理时间分解。DistillNeRF 在 RTX 4090 上的总推理时间约为 0.5 秒（含 2D 编码器、LSS 提升、稀疏卷积和体积渲染），显著快于逐场景优化的 EmerNeRF（需数十分钟），且与 SelfOcc、UniPAD 等可泛化方法处于同一量级。Table 6 对比了两种生成基础模型特征图的方法：DistillNeRF 直接渲染特征图比先渲染 RGB 再经 2D 基础模型提取特征快约 3 倍，同时保持相当的重建精度，验证了特征蒸馏在效率上的实际收益。

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2406_12095/figures/011_Table_6.jpg]]
*Table 6: The reconstruction accuracy and inference speed of two approaches to generate foundation model feature images*

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2406_12095/figures/012_Table_7.jpg]]
*Table 7: Inference time comparison with SOTA methods, and a breakdown on each component in our model*

### 失败模式与局限

1. **训练稳定性**：深度预测在不同 epoch 和运行之间可能出现波动，归因于稀疏层次体素设计与渲染精度之间的权衡——稀疏体素在减少计算的同时可能丢失细粒度几何线索。
2. **动态物体**：模型基于单时间步输入，缺乏时序信息或显式的动静态分离。当场景中存在快速移动物体时，新视角合成的准确性会受到影响，因为模型无法区分静态背景与动态前景的视差变化。
3. **语义利用深度有限**：蒸馏得到的基础模型特征目前仅用于简单的开放词汇查询（Figure 3），其在 3D 多模态对齐、闭环规划等下游任务中的潜力尚未系统验证。
4. **训练开销**：完整训练在 8 张 A100 GPU 上约需 4 天，主要瓶颈在于离线 NeRF 的预计算和多源蒸馏损失的联合优化。

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2406_12095/figures/004_Figure_4.jpg]]
*Figure 4: DistillNeRF Generalizability - Trained on the nuScenes dataset, our model demonstrates strong zero-shot transfer performance on the unseen Waymo NOTR dataset, achieving decent reconstruction quality (row 2). This quality can be further enhanced by applying simple color alterations to account for camera-specific coloring discrepancies (row 3). After fine-tuning (row 4), our model surpasses the offline per-scene optimized EmerNeRF, achieving higher PSNR (29.84 vs. 28.87) and SSIM (0.911 vs. 0.814). See Tab 3 for quantitative results*

## 定位与知识库关联

### 1. 问题定位与核心瓶颈

DistillNeRF 瞄准的是自动驾驶场景中**可泛化神经场**的根本困境：相机视角稀疏且向外发散（Figure 5），相邻帧之间重叠区域极为有限，导致前馈模型面临严重的深度-几何模糊。现有可泛化方法（如 **SelfOcc**、**UniPAD**）在场景重建和新视角合成上的表现远不及逐场景优化的 NeRF——这一差距的核心并非模型容量不足，而是**缺乏足够强的几何监督信号**来消解稀疏多视角带来的歧义。

DistillNeRF 的因果杠杆在于：将离线逐场景优化 NeRF 的强大重建能力，通过知识蒸馏注入可泛化前馈模型，同时从 2D 视觉基础模型（CLIP、DINOv2）迁移语义潜力，使模型在单帧稀疏多视角输入下即可实时预测高质量的 3D 神经场景表示。

### 2. 与基线方法的关系

#### 2.1 作为教师模型的离线 NeRF

**EmerNeRF** 是本工作的核心教师模型。它是一种逐场景优化的 NeRF，具备动静态分解能力，能够从多时间步数据中分离静态背景与动态物体。DistillNeRF 利用 EmerNeRF 生成两类关键监督：

- **稠密深度图**：替代稀疏 LiDAR 点云，为每个像素提供完整的深度真值；
- **虚拟相机视图**：在训练视角之外渲染新视图，提供额外的 RGB 和深度监督。

这一定位使 EmerNeRF 在 DistillNeRF 框架中扮演"几何教师"的角色——其重建质量直接决定了蒸馏信号的上限。值得注意的是，DistillNeRF 在 RGB 重建上已达到与 EmerNeRF 相当的水平（PSNR 30.11 vs 30.88，SSIM 0.917 vs 0.879，Table 1），但推理无需任何逐场景优化。

#### 2.2 可泛化 NeRF 基线

- **SelfOcc**：基于稀疏体素隐式表示的可泛化方法，支持渲染和深度估计，是驾驶场景中表现最好的可泛化基线之一。DistillNeRF 在 RGB 重建 PSNR 上比 SelfOcc 高 45.6%（30.11 vs 20.67），在新视角合成上高 14.0%（20.78 vs 18.22），说明蒸馏策略带来的几何监督远强于纯 RGB 重建损失。
- **UniPAD**：基于 3D→2D 投影的体素方法，在深度估计和渲染质量上均弱于 SelfOcc。DistillNeRF 在稠密深度估计的 Abs Rel 上达到 0.228，而 UniPAD 为 0.276（Table 2b），相对误差降低约 17.4%。

#### 2.3 单时间步对比基线

为公平评估新视角合成能力，论文引入了 **Single-Frame EmerNeRF**——仅用单时间步数据训练的 EmerNeRF。DistillNeRF 在新视角合成 PSNR 上达到 20.78，与该基线（20.95）几乎持平，SSIM 甚至略高（0.590 vs 0.585），证明前馈模型在蒸馏后可以达到与逐场景优化相仿的泛化新视角合成能力。

### 3. 方法谱系中的关键设计选择

DistillNeRF 并非简单地将教师模型输出作为额外损失项，而是通过一系列架构创新使前馈模型能够有效吸收蒸馏信号：

| 设计槽位 | 基线方案 | DistillNeRF 方案 | 因果作用 |
|---------|---------|-----------------|---------|
| 深度预测 | 单阶段 LSS 分类深度 | 两阶段由粗到精的概率性深度预测 | 粗阶段通过光线行进聚合深度概率（Eq 1-2），精阶段在粗深度附近动态采样，缓解稀疏视角下的深度模糊 |
| 体素表示 | 密集固定分辨率体素 | 稀疏层次化双八叉树（细八叉树 + 粗八叉树互补） | 细八叉树捕获近景细节，粗八叉树覆盖远景和空区域，消融显示移除密度互补使 PSNR 从 28.01 降至 22.76（Table 5） |
| 场景范围 | 固定范围（如 50m） | 参数化坐标变换（Eq 3），内部线性缩放，外部渐进收缩 | 使模型能处理无界场景，内部保持真实比例高分辨率，外部映射到 [0,1] |
| 训练监督 | 纯 RGB 重建损失 | 渲染损失 + 离线 NeRF 蒸馏 + 基础模型特征蒸馏（Eq 4） | 深度蒸馏将 PSNR 从 28.01 提升至 30.11（Table 5）；预训练 2D 编码器的移除使 PSNR 骤降至 21.35 |

### 4. 适用边界与局限

**适用场景**：
- 自动驾驶场景的稀疏多视角输入（6 个环视相机），单时间步推理；
- 需要实时或近实时的 3D 场景理解，无法承受逐场景优化开销；
- 需要同时输出 RGB 渲染、深度估计、语义占用预测和开放词汇查询的多任务场景。

**已知局限**（论文明确提及或可从实验推断）：

1. **训练成本高**：在 8 张 A100 GPU 上约需 4 天，主要来自离线 NeRF 蒸馏数据的预生成和多源损失的联合优化。
2. **训练不稳定性**：深度预测在不同 epoch 和运行之间可能出现波动，归因于稀疏层次体素设计与渲染精度之间的权衡——稀疏体素在效率与细节保真度之间存在内在张力。
3. **时序信息缺失**：模型仍基于单时间步输入，未整合时序信息或显式的动静态分离。动态物体（如移动车辆）可能在新视角合成中产生伪影，因为模型缺乏对场景动力学的建模。
4. **基础模型特征利用有限**：当前仅展示了简单的开放词汇查询（Figure 3 rows 6-8），尚未系统探索蒸馏特征在下游任务（如 3D 多模态对齐、闭环规划）中的通用性。
5. **域迁移需要微调**：在 Waymo NOTR 上的零样本迁移虽已展现一定泛化能力，但要超越逐场景优化的 EmerNeRF 仍需微调（Table 3：微调后 PSNR 29.84 vs 零样本约 24.84），且需处理相机色彩差异（Figure 4 row 3）。

### 5. 开放问题

论文提出的开放问题指向该方向的几个关键延伸：

1. **体素表示效率的帕累托前沿**：如何更好地平衡低分辨率稠密体素与高分辨率稀疏体素，在保持细节的同时进一步降低计算开销？当前的双八叉树设计是一个实用折中，但并非理论最优。
2. **表示形式的替代**：能否将 3D 高斯泼溅（3D Gaussian Splatting）等显式表示替代体素隐式表示，以实现更快速的渲染？这涉及到蒸馏框架与不同表示形式的兼容性。
3. **时序扩展与动静态分解**：如何将多时间步输入或时序信息融入可泛化框架，并实现与离线 EmerNeRF 中类似的静态-动态分解？这需要解决前馈模型中时序融合与动静态解耦的架构设计问题。
4. **蒸馏特征的通用性验证**：蒸馏得到的基础模型特征在 3D 多模态对齐、闭环规划、行为预测等下游任务中的通用性如何？当前仅在语义占用预测（Occ3D-nuScenes，Table 4）和简单文本查询上做了初步验证。

### 6. 知识库定位

DistillNeRF 处于以下研究脉络的交汇点：

- **可泛化 NeRF** 脉络：继承 pixelNeRF、GNT 等前馈神经渲染的思想，但针对自动驾驶的稀疏外视场景做了专门的架构设计（两阶段 LSS、稀疏层次体素、参数化坐标变换）。
- **知识蒸馏** 脉络：将逐场景优化 NeRF 作为教师，通过稠密深度和虚拟视图将几何知识迁移到前馈模型，这与 MonoDepth 系列中利用 SfM 或 LiDAR 作为监督有相似动机，但蒸馏源更丰富（包含 RGB、深度、密度熵）。
- **2D 基础模型→3D 迁移** 脉络：将 CLIP、DINOv2 的特征通过体积渲染蒸馏到 3D 表示中，与 LERF、3D-OVS 等工作的目标一致，但 DistillNeRF 是在前馈可泛化框架中实现，而非逐场景优化。
- **自监督 3D 场景理解** 脉络：无需 3D 标注即可生成语义占用预测（Table 4），与 SelfOcc、OccNeRF 等方法同属自监督占用预测方向，但通过基础模型蒸馏获得了更强的语义能力（有蒸馏 mIoU 8.93 vs 无蒸馏 4.63）。

## 原文 PDF

![[paperPDFs/NEURIPS_2024/DistillNeRF_Perceiving_3D_Scenes_from_Single_Glance_Images_by_Distilling_Neural_Fields_and_Foundation_Model_Features.pdf]]
