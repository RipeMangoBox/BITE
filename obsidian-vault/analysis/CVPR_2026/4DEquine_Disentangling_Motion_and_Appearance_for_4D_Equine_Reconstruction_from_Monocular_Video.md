---
title: "4DEquine: Disentangling Motion and Appearance for 4D Equine Reconstruction from Monocular Video"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/4DEquine_Disentangling_Motion_and_Appearance_for_4D_Equine_Reconstruction_from_Monocular_Video.pdf
project_link: "https://luoxuestar.github.io/4DEquine_Project_Page/"
code_link: null
aliases:
- 4DMA4ERFMV
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 将单目4D重建显式解耦为动态运动恢复与静态外观重建两个子问题，通过VAREN参数化网格模型作为桥接，使得运动和外观可以分别由可扩展的前馈网络处理，从而绕过逐视频优化的计算瓶颈并增强对稀疏视角的鲁棒性。
primary_logic: 同一条视频内马匹的外观通常保持不变，而运动具有时序连续性；因此可以将4D重建拆分为一个仅需单张图像的高保真外观生成任务和一个需要时序建模的平滑运动回归任务，二者通过VAREN模型的线性混合蒙皮（LBS）整合，使整个流程变成高效的前馈推断。
claims:
- AniMoFormer（时空Transformer + 后优化）在真实视频数据集 APT-36K 和 AiM 上达到了最高的PCK、最低的加速度误差和Chamfer距离，显著优于所有基线。
- 在AiM的马匹子集上，4DEquine 在感知质量（LPIPS）和结构相似度（SSIM）上明显超过优化方法GART及生成方法GVFDiffusion，同时推理速度比GART快数个数量级。
- 仅通过合成数据训练（VarenPoser + VarenTex），模型在未见的斑马子集上实现零样本泛化，全面超越包括全优化 GART 在内的所有方法。
- AiM (Horse subset) 上 PCK@0.05 ↑ = 87.9
---

# 4DEquine: Disentangling Motion and Appearance for 4D Equine Reconstruction from Monocular Video

> [!tip] 核心洞察
> 同一条视频内马匹的外观通常保持不变，而运动具有时序连续性；因此可以将4D重建拆分为一个仅需单张图像的高保真外观生成任务和一个需要时序建模的平滑运动回归任务，二者通过VAREN模型的线性混合蒙皮（LBS）整合，使整个流程变成高效的前馈推断。

| 字段 | 内容 |
|------|------|
| 中文题名 | 4DEquine: 解耦运动与外观的单目视频4D马科动物重建 |
| 英文题名 | 4DEquine: Disentangling Motion and Appearance for 4D Equine Reconstruction from Monocular Video |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.10125) · [Project](https://luoxuestar.github.io/4DEquine_Project_Page/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | 4DEquine |
| Dataset | AiM |

> [!tip] 效果简介
> - AiM (Horse subset) 上，PCK@0.05 ↑ 87.9 vs 81.8 (GART) (+6.1)；LPIPS ↓ (novel view/pose appearance) 0.1720 vs 0.2000 (GART∗; Few-shot) (-0.0280)。
> - AiM (Zebra subset) 上，PCK@0.05 ↑ 89.0 vs 82.5 (GART) (+6.5)。
> - AiM (Zebra subset, zero-shot) 上，LPIPS ↓ 0.2000 vs 0.2560 (GART, fully optimized) (-0.0560)。

## 概要

从单目视频中重建动态动物的4D表示是一项极具挑战的任务。现有方法（如 **GART**、**4D-Fauna** 等）通常需要在整段视频上进行昂贵的逐视频联合优化，且对观测视角的完整性高度敏感——往往要求360°旋转拍摄才能恢复完整外观，难以应对真实场景中随意拍摄的稀疏视角视频。

**4DEquine** 提出了一种根本性的思路转变：将单目4D重建显式解耦为**动态运动恢复**与**静态外观重建**两个子问题。其核心洞察在于，同一段视频中马匹的外观通常保持不变，而运动具有时序连续性。因此，4D重建可以被拆分为一个仅需单张图像的高保真外观生成任务，与一个需要时序建模的平滑运动回归任务，二者通过 **VAREN** 参数化网格模型的线性混合蒙皮（LBS）进行整合，使整个流程变为高效的前馈推断，绕过了逐视频优化的计算瓶颈，并增强了对稀疏视角的鲁棒性。

该方法由两个解耦的前馈网络构成：
- **AniMoFormer**：一个时空Transformer网络，结合基于2D关键点/掩码的可微渲染后优化，从视频片段中恢复准确且平滑的VAREN姿态与形状参数序列。
- **EquineGS**：一个前馈网络，从单张代表性图像直接预测规范空间下的3D高斯属性，生成可驱动的高保真化身，无需任何逐视频优化。

值得注意的是，4DEquine的运动网络和外观网络**完全在合成数据上训练**——VarenPoser（合成视频数据集）和VarenTex（多视图合成图像数据集），却能在真实数据集上取得领先性能。

在真实视频数据集 **APT-36K** 和 **AiM** 上，AniMoFormer达到了最高的PCK、最低的加速度误差和Chamfer距离，显著优于所有基线。在AiM的马匹子集上，4DEquine在感知质量（LPIPS）和结构相似度（SSIM）上明显超过优化方法GART及生成方法GVFDiffusion，同时推理速度比GART快数个数量级。更关键的是，仅在合成数据上训练的模型在未见的斑马子集上实现了零样本泛化，全面超越包括全优化GART在内的所有方法。

**局限与开放问题**：当输入图像存在严重遮挡或截断时，EquineGS难以重建完整一致的外观；模型无法处理鬃毛和尾巴等非刚性细节；且未包含重光照模块。未来方向包括高效融合多关键帧外观、增强非刚性动态效果，以及适应动态光照变化。

### 问题背景

从单目视频中重建动态动物的4D表示（3D几何+时间）是计算机视觉与图形学中的基础难题。马科动物（马、斑马、驴等）因其复杂的非刚性运动、多样的外观纹理以及在农业、体育、影视等领域的广泛应用，成为极具代表性的重建对象。然而，单目视频天然缺乏深度信息，且马匹运动涉及四肢的大幅度变形与自遮挡，使得从随意拍摄的短视频中恢复时空一致的4D表示极具挑战。

### 现有方法缺口

当前主流方法存在两个突出的结构性问题：

**逐视频联合优化的计算瓶颈。** 以 **GART**、**SMALR** 等为代表的基于优化的方法，需要在整段视频上进行昂贵的联合优化，同时恢复运动与外观。这一范式不仅推理耗时（通常需要数小时处理一段视频），而且对视角覆盖极为敏感——往往要求近乎360°的旋转拍摄才能恢复完整外观，难以应用于真实场景中常见的局部视角、随意拍摄视频。

**运动与外观的耦合导致效率低下。** 现有方法将动态运动恢复与静态外观重建绑定在同一优化循环中，未能利用一个关键观察：在同一条视频内，马匹的外观（纹理、毛色、体型）通常保持不变，而运动则具有时序连续性。这种耦合使得模型无法分别针对两个子问题设计高效的前馈网络，也限制了从稀疏视角中聚合外观信息的能力。

### 本文动机

针对上述瓶颈，4DEquine 提出将单目4D重建显式解耦为两个独立子问题：**动态运动恢复**与**静态外观重建**。核心洞察在于，马匹的外观仅需从视频中的一张代表性图像即可高保真地重建，而运动则需要利用时序上下文来保证平滑性。通过 VAREN 参数化网格模型作为桥接——其线性混合蒙皮（LBS）机制天然支持将规范空间下的外观“驱动”到任意姿态——运动和外观可以分别由可扩展的前馈网络处理，从而彻底绕过逐视频优化的计算瓶颈，并增强对稀疏视角的鲁棒性。

这一解耦策略将整个4D重建流程转变为高效的前馈推断：运动网络从视频片段中回归平滑的姿态序列，外观网络从单张图像生成可驱动的3D高斯化身，二者通过 VAREN 模型无缝整合。该设计不仅大幅提升了推理速度（比优化方法快数个数量级），还使得模型可以完全在合成数据上训练，并在真实场景中实现零样本泛化。

## 核心方法与创新机理

4DEquine 的核心创新在于将单目视频的 4D 马科动物重建显式解耦为**动态运动恢复**与**静态外观重建**两个独立子问题，并通过 VAREN 参数化网格模型作为桥接，使整个流程变为高效的前馈推断，从根本上绕过了现有方法（如 **GART**、**SMALR** 等）需要在整段视频上进行昂贵逐视频联合优化的瓶颈。

### 1. 解耦-桥接-前馈范式

现有基于优化的 4D 动物重建方法面临双重困境：一方面，它们需要在整段视频上联合优化几何与外观，计算开销极大；另一方面，它们对视角完整性高度敏感，通常要求 360° 旋转视频才能恢复完整外观，难以应用于真实场景的随意拍摄视频。

4DEquine 的核心洞察在于：同一条视频内马匹的外观通常保持不变，而运动具有时序连续性。据此，它将 4D 重建拆分为两个可独立求解的子问题：

- **运动恢复**：需要时序建模以捕捉运动平滑性，由时空 Transformer **AniMoFormer** 处理；
- **外观重建**：仅需单张代表性图像即可生成高保真外观，由前馈网络 **EquineGS** 处理。

二者通过 VAREN 模型的线性混合蒙皮（LBS）整合——AniMoFormer 输出每一帧的姿态与形状参数驱动 VAREN 网格变形，EquineGS 在规范空间下预测的 3D 高斯属性随之变形并渲染。这种设计使得整个流程变成高效的前馈推断，推理速度比 GART 快数个数量级。

### 2. 关键 changed slots

相较于基线方法，4DEquine 在以下维度实现了根本性改变：

**运动估计方式**：从单帧回归（如 **AniMer**、**GenZoo**）或逐帧优化，转变为**时空 Transformer + 后优化**。AniMoFormer 在 AniMer 的空间 Transformer 基础上引入 Temporal Transformer，通过跨 N 帧窗口的自注意力建模时序关系，捕捉局部运动上下文；随后通过基于 2D 关键点和掩码的可微渲染后优化，将预测网格与像素级证据对齐，实现几何精度与运动平滑度的双重提升。

**外观重建方式**：从基于纹理拼接或逐视频隐式/高斯优化，转变为**前馈网络直接从单张图像预测 3D 高斯属性**。EquineGS 采用双流 Transformer 融合架构（DSTG-Block）：一路用预训练 DINOv3 提取图像多尺度特征，另一路用 MLP 加位置编码处理 VAREN 模板点云坐标，通过交叉注意力实现 2D 纹理信息向 3D 几何的注入，一次性预测所有高斯的位移、旋转、尺度、颜色和不透明度。

**训练数据策略**：从依赖少量真实标注或特定场景优化，转变为**完全使用合成数据训练**。运动网络在 VarenPoser（首个大规模 4D VAREN 标注合成视频数据集）上训练，外观网络在 VarenTex（基于多视图扩散模型生成的合成多视角图像数据集）上训练。这一策略使模型在仅见合成数据的情况下，在真实数据集 APT-36K 和 AiM 上达到最优性能，并在未见的斑马子集上实现零样本泛化，全面超越包括全优化 GART 在内的所有方法。

### 3. 创新强度评估

解耦-桥接-前馈范式的有效性得到多维度验证：在 AiM 马匹子集上，4DEquine 的 PCK@0.05 达到 87.9，较 GART 的 81.8 提升 6.1 个百分点；LPIPS 降至 0.1720，优于 GART 的 0.2000（Table 2, Table 6）。消融实验进一步证实，移除后优化导致 PSNR 从 15.66 降至 13.84（Table 4），移除时间 Transformer 使加速度误差升高（Table 3），验证了各 changed slot 的必要性。在零样本斑马子集上，4DEquine 的 LPIPS 为 0.2000，显著优于全优化 GART 的 0.2560（Table 2），表明解耦范式带来的泛化能力超越了传统联合优化的上限。

4DEquine 将单目视频的 4D 重建显式解耦为两个可独立求解的子问题：**动态运动恢复** 与 **静态外观重建**。这一解耦设计的核心洞察在于，同一段视频中马匹的外观通常保持不变，而运动具有时序连续性——因此，可以分别用一个仅需单张图像的前馈网络生成高保真外观，以及一个需要时序建模的网络回归平滑运动，再通过 VAREN 参数化网格模型的线性混合蒙皮（LBS）将二者整合为可驱动的 4D 化身。

整个 pipeline 由两大模块构成，如 Figure 2 所示：

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2603_10125/figures/002_Figure_2.jpg]]
*Figure 2: Overview of 4DEquine. (a) AniMoFormer: A spatio-temporal transformer with post-optimization for motion recovery. (b) EquineGS: A feed-forward network to reconstruct a canonical 3D Gaussian avatar from a single image. (c) DSTG-Block: The dual-stream architecture used in EquineGS*

1. **AniMoFormer（运动模块）**：以一段 $N$ 帧的视频片段为输入，通过时空 Transformer 回归每一帧的 VAREN 姿态与形状参数，再经基于可微渲染的后优化（Post-Optimization）与 2D 关键点及掩码对齐，输出平滑且像素级精确的 4D 几何序列。
2. **EquineGS（外观模块）**：仅从单张代表性图像出发，利用双流 Transformer（DSTG-Block）融合图像特征与 VAREN 模板点云特征，前馈预测规范空间下的 3D Gaussian 属性（位置偏移、旋转、尺度、颜色、不透明度），生成可动画化的静态外观化身。

推理时，给定一段单目视频：
- 选取一帧作为外观参考图像，送入 EquineGS 一次性生成规范 Gaussian 化身；
- 将整段视频送入 AniMoFormer，逐帧输出 VAREN 姿态序列；
- 利用 VAREN 的 LBS 将规范化身变形到各帧姿态，再通过 3D Gaussian Splatting 渲染出任意视角的 RGB 图像与掩码。

这种“运动-外观解耦 + 前馈推断”的设计，使得 4DEquine 无需在整段视频上进行昂贵的逐视频联合优化，从根本上绕过了现有方法（如 GART、SMALR）对 360° 旋转视频的依赖和计算瓶颈。两个子网络均完全在合成数据上训练——AniMoFormer 使用 VarenPoser 合成视频数据集，EquineGS 使用 VarenTex 多视图合成图像数据集——却能在真实场景数据集 APT-36K 和 AiM 上达到最优性能，并展现出对未见物种（如斑马、驴）的零样本泛化能力。

4DEquine 将单目视频的 4D 重建显式解耦为两个独立子问题：**动态运动恢复** 与 **静态外观重建**。运动子问题由时空 Transformer 网络 **AniMoFormer** 结合基于可微渲染的后优化处理；外观子问题由前馈网络 **EquineGS** 从单张代表性图像直接预测规范空间下的 3D 高斯化身。二者通过 VAREN 参数化网格模型的线性混合蒙皮（LBS）桥接，使整个流程变成高效的前馈推断，无需逐视频的昂贵联合优化。

---

### AniMoFormer：时空运动恢复

AniMoFormer 以 AniMer 的单帧空间编码器为基础，构建了一个两阶段的运动恢复管线。

**第一阶段：时空 Transformer。** 对于长度为 $N$ 的输入视频片段，首先通过空间编码器逐帧提取特征，得到 $N$ 帧空间特征堆栈；随后将其送入 Temporal Transformer，利用跨帧自注意力建模时序关系，捕获局部运动上下文。训练时采用如下总损失：

$$
\mathcal{L} = \lambda_{\mathrm{varen}} \mathcal{L}_{\mathrm{varen}} + \lambda_{\mathrm{smooth}} \mathcal{L}_{\mathrm{smooth}} + \lambda_{\mathrm{2D}} \mathcal{L}_{\mathrm{2D}} + \lambda_{\mathrm{3D}} \mathcal{L}_{\mathrm{3D}}
$$

其中 $\mathcal{L}_{\mathrm{varen}}$ 约束预测的姿态参数 $\hat{\pmb{\theta}}$ 和形状参数 $\hat{\pmb{\beta}}$ 与真值一致；$\mathcal{L}_{\mathrm{3D}}$ 为 3D 关键点损失；$\mathcal{L}_{\mathrm{2D}}$ 为 2D 关键点重投影损失。时序平滑损失显式惩罚相邻帧间的参数跳变：

$$
\mathcal{L}_{\mathrm{smooth}} = \sum_{t=2}^{N} ||\hat{\vec{\beta}}_{t} - \hat{\vec{\beta}}_{t-1}||_{2}^{2} + \sum_{t=2}^{N} ||\hat{\vec{\theta}}_{t} - \hat{\vec{\theta}}_{t-1}||_{2}^{2}
$$

消融实验（Table 3）证实：移除 Temporal Transformer（w/o Temporal）导致加速度误差显著升高，表明时序建模对运动平滑度至关重要；增大输入帧窗口 $N$（4→8→16）可逐步提升 PCK 并降低加速度误差，但 $N=32$ 时内存溢出。

**第二阶段：后优化（Post-Optimization）。** Transformer 输出的 VAREN 参数序列在几何上已较为平滑，但像素级对齐仍有不足。后优化阶段使用可微渲染器将预测网格投影为渲染掩码和 2D 关键点，并与真实观测对齐，优化目标为：

$$
\mathcal{L} = \lambda_{\mathrm{2D}} \mathcal{L}_{\mathrm{2D}} + \lambda_{\mathrm{smooth}} \mathcal{L}_{\mathrm{smooth}} + \lambda_{\mathrm{reg}} \mathcal{L}_{\mathrm{reg}} + \lambda_{\mathrm{mask}} \mathcal{L}_{\mathrm{mask}}
$$

其中 $\mathcal{L}_{\mathrm{mask}}$ 为掩码对齐损失，$\mathcal{L}_{\mathrm{reg}}$ 为姿态正则化项。消融实验（Table 4）显示，移除后优化（w/o PO）使 PSNR 从 15.66 降至 13.84，LPIPS 从 0.1720 升至 0.1737，验证了 2D 对齐对最终重建质量的关键作用。

---

### EquineGS：前馈 3D 高斯化身生成

EquineGS 从单张代表性图像直接预测规范空间下的可驱动 3D 高斯化身，核心设计是双流 Transformer 融合架构 **DSTG-Block**。

**规范形状表示。** 将 VAREN 模板网格上采样至 $N_G = 55,486$ 个顶点作为 3D 点云，用于初始化 3D 高斯的位置。每个高斯的完整属性包括位移 $\Delta\pmb{\mu}_i$、旋转四元数 $\mathbf{r}_i$、尺度 $\mathbf{s}_i$、颜色 $\mathbf{c}_i$ 和不透明度 $o_i$。

**双流特征提取与融合。** 图像流使用预训练的 DINOv3（ViT-Large）提取多尺度特征图 $\mathbf{F}_{\mathrm{I}}$；点云流对 3D 坐标施加位置编码后通过 MLP 编码。DSTG-Block 的关键操作是从图像特征中提取全局上下文向量，用于调制点云特征的注意力：

$$
\mathbf{F}_{\mathrm{context}} = \mathbf{MLP}(\operatorname{AvgPool}(\mathbf{F}_{\mathrm{I}}))
$$

该上下文向量在 DSTG 解码器中引导交叉注意力，使点云特征能够有效聚合来自图像的外观信息。最终从融合特征 $\mathbf{F}_{\mathrm{DSTG}}$ 中预测所有高斯属性：

$$
\{\Delta \pmb{\mu}_{i}, \mathbf{r}_{i}, \mathbf{s}_{i}, \mathbf{c}_{i}, o_{i}\}_{i=1}^{N_{G}} = \mathbf{MLP}(\mathbf{F}_{\mathrm{DSTG}})
$$

**训练损失。** EquineGS 的训练目标结合图像重建、掩码约束和正则化：

$$
\mathcal{L} = \lambda_{\mathrm{image}} \mathcal{L}_{\mathrm{image}} + \lambda_{\mathrm{mask}} \mathcal{L}_{\mathrm{mask}} + \lambda_{\mathrm{reg}} \mathcal{L}_{\mathrm{reg}}
$$

其中 $\mathcal{L}_{\mathrm{image}}$ 包含 L1 损失与 LPIPS 感知损失。消融实验（Table 4）表明，用标准交叉注意力块替换 DSTG-Block（w/o DSTG）导致 PSNR、SSIM、LPIPS 全部恶化，验证了双流 Transformer 融合设计的有效性。

---

### 数据解耦：VarenPoser 与 VarenTex

两个子网络完全在合成数据上训练，实现了训练数据与推理场景的解耦。

- **VarenPoser**：通过将 VAREN 模型拟合到基于标记点的马匹运动数据集 PFERD 获取姿态参数，随机分配形状参数，并利用 MV-Adapter 生成多样化纹理，构建了首个大规模带有 4D VAREN 标注的合成视频数据集，用于训练 AniMoFormer。
- **VarenTex**：从 VarenPoser 网格渲染法向图和规范坐标图，结合 ControlNet 生成的参考图像，通过 UniTex 合成多视角训练图像（共 150K 张，分辨率 512×512），用于训练 EquineGS。

## 实验与关键发现

### 实验设置与基准

4DEquine 在三个数据集上进行评估：**APT-36K**（马匹测试子集，30个视频片段，402帧）、**AiM**（马匹测试子集，10个视频片段，453帧）以及合成数据集 **VarenPoser**。运动恢复网络 AniMoFormer 仅在 VarenPoser 的合成数据上训练，外观重建网络 EquineGS 仅在 VarenTex（15万张512×512多视图合成图像）上训练——两个组件均未接触任何真实训练数据。

对比方法涵盖多个范式：
- **基于模型的单帧回归方法**：Dessie（hSMAL 马匹重建）、AniMer（Transformer 单帧姿态估计）、GenZoo（SMAL+ 通用动物重建）
- **无模型化身方法**：3D-Fauna、4D-Fauna
- **逐视频优化方法**：GART（3D高斯泼溅化身重建）
- **生成式方法**：GVFDiffusion（视频到4D合成）

在外观对比中，EquineGS 仅使用每个视频的第一帧进行推理，而 GART 使用全部训练帧优化，其余方法在整个视频上逐帧重建，遵循与 DogRecon 类似的公平对比协议。此外，GART 被提供与 4DEquine 相同的 VAREN 基模板和 AniMoFormer 输出的姿态序列作为运动输入。

### 主实验结果

#### 运动恢复精度

Table 1 展示了在三个数据集上的运动恢复定量对比。AniMoFormer 在所有基准上全面超越现有方法：

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2603_10125/figures/006_Table_1.jpg]]
*Table 1: Quantitative comparisons on the APT36K dataset, AiM dataset and VarenPoser dataset*

- 在 **APT-36K** 上，PCK@0.05 达到 61.8，显著高于第二名方法（AniMer 的 52.3），提升约 9.5 个百分点。加速度误差（Accel）和 Chamfer 距离也均为最优。
- 在 **AiM** 马匹子集上，PCK@0.05 达到 87.9，领先 GART（81.8）达 6.1 个百分点，同时加速度误差大幅降低，验证了时空 Transformer 对运动平滑度的关键作用。
- 在合成数据集 **VarenPoser** 上同样保持领先，表明模型在域内和域外数据上均具有鲁棒性。

#### 外观重建质量

Table 2 报告了新视角/新姿态下的外观重建指标。4DEquine 在感知质量（LPIPS）和结构相似度（SSIM）上均明显优于优化方法 GART 和生成方法 GVFDiffusion：

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2603_10125/figures/008_Table_2.jpg]]
*Table 2: Novel view/pose quantitative comparisons with SOTA methods on the horse and zebra. GART∗: Few-shot GART. Bold and underlined numbers indicate the best performance and the second best performance, respectively*

- 在 **AiM 马匹子集**上，LPIPS 降至 0.1720，而 Few-shot GART（GART∗）为 0.2000，全优化 GART 为 0.1890。推理速度比 GART 快数个数量级。
- 在 **AiM 斑马子集**上，4DEquine 实现零样本泛化——模型从未见过斑马纹理训练数据，但 LPIPS 达到 0.2000，显著优于全优化 GART 的 0.2560（降低 0.056），PCK@0.05 达到 89.0 对 82.5（Table 6, Supplementary）。这验证了“合成数据训练+解耦设计”带来的强泛化能力。

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2603_10125/figures/014_Table_6.jpg]]
*Table 6: Quantitative comparisons on the AiM dataset. GART*: Few-shot GART*

Figure 4 的定性对比进一步显示，4DEquine 重建的马匹纹理清晰、姿态准确，而 GART 在稀疏视角下容易出现模糊和几何失真。

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2603_10125/figures/004_Figure_4.jpg]]
*Figure 4: Qualitative comparison with the SOTA methods on the AiM dataset. GART∗: Few-shot GART. “Input” here is the middle frame of each test video clip. Note that the input image for EquineGS is the first image in the video; therefore, the results of “Ours” shown in this figure correspond to novel-pose animation*

### 消融实验

#### AniMoFormer 消融（Table 3）

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2603_10125/figures/009_Table_3.jpg]]
*Table 3: Ablation study for AniMoFormer*

- **移除时间 Transformer（w/o Temporal）**：加速度误差显著升高，表明时序建模对运动平滑度至关重要。空间 Transformer 单独处理每帧无法捕捉帧间连续性。
- **移除后优化（w/o PO）**：所有渲染指标大幅下降——PSNR 从 15.66 降至 13.84，LPIPS 从 0.1720 升至 0.1737（Table 4），验证了基于 2D 关键点和掩码的可微渲染后优化对像素级几何精度的关键贡献。
- **增大输入帧窗口 N**：从 4 帧增至 8 帧再增至 16 帧，PCK 逐步提升，加速度误差逐步降低，验证了时空上下文的有效性。N=32 时因内存溢出无法训练（Section 9.3, Supplementary）。

#### EquineGS 消融（Table 4）

- **移除 DSTG-Block（w/o DSTG）**：用标准交叉注意力块替换双流 Transformer 融合设计后，PSNR、SSIM、LPIPS 全部变差，证明双流架构在融合图像特征与点云几何信息方面的设计有效性。
- **移除后优化（w/o PO）**：如前述，对最终渲染质量影响显著，说明即使外观网络本身强大，2D 对齐步骤仍是高保真重建的必要环节。
- **网格细分消融**（Figure 6）：将 VAREN 模板网格从默认分辨率上采样至 55,486 个顶点，为 3D 高斯提供更密集的初始化点云。可视化结果表明，更高分辨率的几何基元能承载更精细的外观细节。

### 失败模式与局限性

Figure 11 展示了典型失败案例：当输入图像存在**严重遮挡或截断**时（如马匹身体大面积被障碍物遮挡），EquineGS 难以重建完整一致的外观。这是因为前馈网络仅从单张代表性图像推断外观，无法凭空补全不可见区域。论文明确指出，需要确保关键帧中马匹未被大面积遮挡。

此外，当前方法存在两个结构性局限：
1. **非刚性细节未建模**：VAREN 参数化模型不包含鬃毛和尾巴，因此这些动态细节无法被重建和驱动。
2. **无重光照能力**：模型未包含重光照模块，无法应对真实场景中的动态光照变化。

### 关键实验结论

1. **解耦策略有效**：将 4D 重建拆分为运动恢复（AniMoFormer）和外观重建（EquineGS）两个独立的前馈网络，绕过了逐视频优化的计算瓶颈，同时增强了对稀疏视角的鲁棒性。
2. **合成数据训练可实现零样本泛化**：仅在合成数据上训练的模型，在未见过的真实斑马子集上全面超越全优化 GART，证明 VAREN 参数化模型作为桥接的有效性。
3. **时空建模与 2D 对齐缺一不可**：消融实验表明，时间 Transformer 保证运动平滑，后优化保证像素级几何精度，二者共同构成高保真 4D 重建的必要条件。
4. **推理效率优势显著**：前馈推断使 4DEquine 的推理速度比逐视频优化的 GART 快数个数量级，使其具备实际应用潜力。

## 定位与知识库关联

### 4D动物重建的范式演进

4D动物重建旨在从单目视频中同时恢复动态几何与外观，其方法谱系可沿两条轴线梳理：**优化驱动范式**与**前馈/生成范式**。

**优化驱动范式**长期占据主导地位。早期工作如基于hSMAL模型的**Dessie**、利用SMAL+的**GenZoo**，以及无模型化身方法**3D-Fauna**和**4D-Fauna**，均依赖逐视频的迭代优化来拟合参数化模型或隐式表示。这一脉络的近期代表是**GART**，它将3D高斯泼溅（3D Gaussian Splatting）引入化身重建，但仍需在整段视频上进行昂贵的联合优化，且对不完整的视角观测敏感——通常要求接近360°的旋转视频才能恢复完整外观，难以应对真实场景中随意拍摄的片段。另一条分支**GVFDiffusion**则利用预训练生成模型进行视频到4D的合成，绕过了逐视频优化，但其生成质量受限于预训练先验，缺乏对特定实例的精确几何约束。

**前馈范式**试图以单帧或少量帧的直接推断替代迭代优化。**AniMer**基于Transformer从单帧回归动物姿态，速度快但缺乏时序一致性；4DEquine正是在这一基础上，将前馈思想从单帧姿态估计拓展到完整的4D重建。

### 4DEquine的核心定位：解耦-桥接-前馈

4DEquine的方法论贡献不在于发明全新的基础组件，而在于**重新组织问题结构**。其核心洞察是：在同一条视频内，马匹的外观通常保持不变，而运动具有时序连续性。这一观察使得4D重建可以被显式拆分为两个子问题——

1. **动态运动恢复**：需要时序建模的平滑姿态回归任务；
2. **静态外观重建**：仅需单张图像的高保真外观生成任务。

关键的制度性设计是**VAREN参数化网格模型作为桥接表示**：运动网络输出VAREN的姿态与形状参数，外观网络在VAREN的规范空间（canonical space）中预测3D高斯属性，二者通过VAREN内置的线性混合蒙皮（LBS）整合为可驱动化身。这一解耦使得两个子问题可以分别由可扩展的前馈网络处理，从而绕过了逐视频优化的计算瓶颈，并增强了对稀疏视角的鲁棒性。

与现有前馈方法（如AniMer的单帧回归）相比，4DEquine的增量在于：(1) 引入时空Transformer（AniMoFormer）显式建模帧间时序依赖，输出平滑运动序列；(2) 将前馈推断从姿态估计延伸到完整的3D高斯外观生成（EquineGS），形成端到端的4D重建管线。

### 适用边界与局限

**适用场景**：4DEquine最适用于目标对象外观在视频内保持稳定、且存在至少一张无严重遮挡的关键帧的单目视频。其合成数据驱动的训练策略使其对马科动物（马、斑马）表现出良好的零样本泛化能力，甚至可迁移至未见过的驴。

**已知局限**：

1. **遮挡敏感性**：当输入图像存在严重遮挡或截断时，EquineGS难以重建完整一致的外观。系统要求关键帧中马匹未被大面积遮挡，这限制了其在拥挤场景或部分可见拍摄条件下的应用。
2. **非刚性细节缺失**：当前模型无法处理马的鬃毛和尾巴等非刚性动态细节，这些部分未在VAREN模型中建模，导致重建结果在这些区域缺乏真实感。
3. **光照不变性假设**：未包含重光照模块，无法应对视频中的动态光照变化。模型隐式假设外观在整段视频中保持恒定，在户外场景的阴影变化或室内人工光源切换下可能出现渲染不一致。
4. **内存约束**：时空Transformer的输入帧窗口N受限于GPU内存（N=32时溢出），这限制了其捕捉长程运动依赖的能力。

### 开放问题

论文明确指出的开放问题指向三个方向：

- **多帧外观聚合**：如何高效融合多个关键帧以聚合来自无遮挡视角的外观信息？当前EquineGS仅依赖单张代表性图像，在遮挡场景下缺乏信息补偿机制。
- **物理增强的动态细节**：如何用基于物理的表示（如毛发模拟）增强马匹的鬃毛和尾巴的动态效果？这需要超越VAREN参数化模型的表达能力。
- **动态光照适应**：如何添加重光照模块以适应真实场景中的动态光照？这涉及将外观解耦为材质与光照因子的更细粒度分解。

从更宏观的视角看，4DEquine的“解耦-桥接-前馈”范式是否可推广到其他非刚性物体类别（如人类以外的灵长类、犬科动物），取决于是否存在类似VAREN的高质量参数化模型作为桥接。当前合成数据训练策略的成功表明，高质量参数化模型与生成式数据增强的结合可能是通向通用可驱动化身重建的关键路径。

## 原文 PDF

![[paperPDFs/CVPR_2026/4DEquine_Disentangling_Motion_and_Appearance_for_4D_Equine_Reconstruction_from_Monocular_Video.pdf]]
