---
title: "SparseCam4D: Spatio-Temporally Consistent 4D Reconstruction from Sparse Cameras"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/SparseCam4D_Spatio_Temporally_Consistent_4D_Reconstruction_from_Sparse_Cameras.pdf
project_link: "https://inspatio.github.io/sparse-cam4d/"
code_link: null
aliases:
- SparseCam4D
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 时空扭曲场（Spatio-Temporal Distortion Field, STDF）
primary_logic: 提出轻量级时空扭曲场，在训练期间显式建模生成观察中的时空不一致，将误差解耦到生成视图专用的扭曲高斯中，而规范高斯用于真实视图；训练后丢弃STDF，保证零推理开销，从而在稀疏相机输入下实现高质量时空一致的4D重建。
claims:
- 消融实验表明，移除时空扭曲场会导致渲染质量严重下降（LPIPS从0.264升至0.608，SSIM从0.656降至0.426）。
- 不使用扭曲场时，生成画面的时空不一致性导致重建结果出现严重模糊和时序不稳定性。
- Technicolor 上 PSNR↑ / SSIM↑ / LPIPS↓ = 23.15 / 0.728 / 0.299
- Neural 3D Video 上 PSNR↑ / SSIM↑ / LPIPS↓ = 21.91 / 0.789 / 0.258
---

# SparseCam4D: Spatio-Temporally Consistent 4D Reconstruction from Sparse Cameras

> [!tip] 核心洞察
> 提出轻量级时空扭曲场，在训练期间显式建模生成观察中的时空不一致，将误差解耦到生成视图专用的扭曲高斯中，而规范高斯用于真实视图；训练后丢弃STDF，保证零推理开销，从而在稀疏相机输入下实现高质量时空一致的4D重建。

| 字段 | 内容 |
|------|------|
| 中文题名 | SparseCam4D：稀疏相机下的时空一致4D重建 |
| 英文题名 | SparseCam4D: Spatio-Temporally Consistent 4D Reconstruction from Sparse Cameras |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.26481) · [Project](https://inspatio.github.io/sparse-cam4d/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | SparseCam4D |
| Dataset | Technicolor, Neural 3D Video, Nvidia Dynamic Scenes |

> [!tip] 效果简介
> - Technicolor 上，PSNR↑ / SSIM↑ / LPIPS↓ 23.15 / 0.728 / 0.299 vs 17.97 / 0.578 / 0.352 (MonoFusion*) (PSNR +5.18 dB, SSIM +0.150, LPIPS -0.053)。
> - Neural 3D Video 上，PSNR↑ / SSIM↑ / LPIPS↓ 21.91 / 0.789 / 0.258 vs 18.43 / 0.738 / 0.270 (MonoFusion*) (PSNR +3.48 dB, SSIM +0.051, LPIPS -0.012)。
> - Nvidia Dynamic Scenes 上，PSNR↑ / SSIM↑ / LPIPS↓ 24.81 / 0.794 / 0.150 vs 20.22 / 0.590 / 0.192 (MonoFusion*) (PSNR +4.59 dB, SSIM +0.204, LPIPS -0.042)。

## 概要

从稀疏相机阵列（2–3个视角）重建动态场景的4D表示，是计算机视觉中的一个根本性挑战。传统依赖几何正则化或多视图立体匹配的方法，在输入视角极度稀疏时，因观测信息严重不足，难以恢复时空一致的场景结构与运动。近期视频扩散模型的进展，使得从稀疏视图生成额外视角的时序视频成为可能，但生成结果中普遍存在的**时空不一致性**——包括同一时刻不同视角间的空间不一致，以及同一视角不同时刻间的时间不一致——直接将其用于4D重建会导致严重模糊和时序不稳定性（Fig. 2, Fig. 5）。

**SparseCam4D** 针对上述瓶颈，提出以**时空扭曲场（Spatio-Temporal Distortion Field, STDF）** 为核心机制，将生成观测中的不一致性显式建模为对规范4D高斯的可学习扭曲偏移。该扭曲场仅在训练期间作用于生成视图，真实视图仍由规范高斯渲染；训练完成后STDF被丢弃，新视角渲染**零额外计算开销**。配合相机姿态联合优化、针对生成视图的感知损失，以及多维度正则化，SparseCam4D 在仅2–3个稀疏相机的条件下，实现了高质量的时空一致4D重建。

在 Technicolor、Neural 3D Video 和 Nvidia Dynamic Scenes 三个基准数据集上，SparseCam4D 显著优于现有方法：以 MonoFusion 为基线，PSNR 提升 3.48–5.18 dB，SSIM 提升 0.051–0.204，LPIPS 降低 0.012–0.053（Tab. 1）。消融实验进一步揭示，移除 STDF 会使 LPIPS 从 0.264 剧增至 0.608，SSIM 从 0.656 降至 0.426，验证了时空不一致建模的绝对必要性（Tab. 2）。

### 动态场景重建的稀疏相机困境

从多视角视频中重建动态3D场景（即4D重建）是实现照片级自由视点渲染的核心技术，在VR/AR、影视制作和体育转播等领域有广泛应用。传统方法依赖密集的同步相机阵列（通常15-20台以上）来捕获时空一致的观测，这种硬件配置成本高昂、部署复杂，严重限制了4D重建技术的实际落地。

当相机数量缩减至2-3台时，问题变得极具挑战性：稀疏输入导致观测极度不足，场景中大量区域在绝大多数时刻缺乏直接的多视角约束。以**4DGaussians**为代表的现有方法虽然通过几何正则化在一定程度上缓解了欠约束问题，但由于缺乏足够的跨视角信息，重建结果往往出现严重的几何坍塌和纹理模糊。**MonoFusion**等单目方法则依赖深度估计先验，在复杂动态场景中同样面临时序抖动和细节丢失的困境。

### 视频扩散模型的机遇与陷阱

近期视频扩散模型（Video Diffusion Models, VDMs）的突破为这一困境带来了新的可能。通过以稀疏相机图像和点云渲染为条件，VDMs能够生成未观测视角的时序视频，从而为重建管道提供额外的伪观测。然而，这些生成帧并非可靠的测量——它们存在严重的**时空不一致性**（Spatio-Temporal Inconsistency），具体表现为两类缺陷：

- **空间不一致**：同一时刻不同生成视角之间的内容不连贯，如物体形状漂移、纹理错位；
- **时间不一致**：同一生成视角不同时刻之间的运动不连续，如表面闪烁、运动抖动。

如图2所示，真实相机（灰色）捕获的内容在多视角动态场景中保持一致性，而生成结果（橙色）在不同姿态和时刻之间呈现出明显的偏差。直接将这类不可靠的生成观测喂入重建管道，会导致严重的模糊和伪影——消融实验证实，无处理地使用生成帧时，LPIPS从0.264剧增至0.608，SSIM从0.656骤降至0.426（Table 2），渲染结果出现严重的时空模糊和时序不稳定（Figure 5）。这一现象揭示了问题的本质瓶颈：**视频扩散模型生成的额外观察存在时空不一致性，直接用于4D重建会导致严重模糊和伪影**。

### 核心动机与研究问题

上述分析表明，稀疏相机4D重建面临一个两难困境：一方面，仅依赖真实视图无法提供足够的观测覆盖；另一方面，生成视图虽然扩展了观测范围，却引入了破坏性的时空不一致。现有方法要么完全回避生成先验（如**4D-Rotor**、**RealTime4DGS**仅依赖真实视图和正则化），要么简单地将生成帧视为可靠观测（导致前述的模糊和伪影），缺乏对生成不一致性的显式建模与解耦机制。

本文的核心动机在于回答一个关键问题：**能否设计一种机制，在利用生成先验丰富观测的同时，显式建模并隔离其固有的时空不一致性，从而在稀疏相机输入下实现高质量的时空一致4D重建？** 这一问题的解决需要同时应对三个子挑战：（1）如何形式化地建模生成观测中跨空间和时间的扭曲；（2）如何将该建模无缝嵌入现有的4D高斯泼溅框架；（3）如何保证推理阶段不引入额外计算开销。

## 核心方法与创新机理

SparseCam4D 的核心创新在于**将视频扩散模型的生成能力引入稀疏相机4D重建管道，并通过时空扭曲场（Spatio-Temporal Distortion Field, STDF）显式建模生成观察中的时空不一致性**，从而在训练期间将误差解耦到生成视图专用的扭曲高斯中，而规范高斯仅用于真实视图渲染。训练完成后丢弃STDF，保证零推理开销。

### 问题根因：生成观察的时空不一致

在稀疏相机设置下（2-3个视图），传统4D重建方法因观测极度不足而难以收敛。SparseCam4D 利用相机控制的视频扩散模型生成额外视角的时序视频作为辅助观察（见 Figure 2）。然而，这些生成帧存在两类根本性不一致：

- **空间不一致**：同一时刻不同生成视角之间缺乏多视图一致性；
- **时间不一致**：同一生成视角在不同时刻出现闪烁表面和不稳定运动。

直接将生成视图用于4D重建会导致严重模糊和时序不稳定（见 Figure 5），这一瓶颈构成了本方法的核心设计动机。

### 核心机制：时空扭曲场（STDF）

STDF 是一个轻量级的5D特征场，接收规范4D高斯与时空索引 $(t, s)$，输出位置、旋转、缩放的扭曲偏移量：

$$\mathcal{F} : (\mathcal{G}_{4D}, t, s) \mapsto \Delta \mathcal{G}_{4D}$$

具体实现上，STDF 将5D体积 $(x, y, z, t, s)$ 分解为9个二维特征平面（排除无编码意义的 $(t, s)$ 组合），通过双线性插值提取多分辨率特征，再经小型MLP解码为扭曲偏移量：

$$f(c)_c = \operatorname{interp}(P_c, \pi_c(c)), \quad c \in \{xy, xz, yz, xt, yt, zt, xs, ys, zs\}$$

扭曲后的高斯属性用于渲染生成视图，而规范高斯用于渲染真实视图，从而将生成观察中的不一致性**解耦到扭曲高斯中**，避免污染场景的规范表示。

### 与 Baseline 的关键差异（Changed Slots）

| 设计维度 | Baseline 做法 | SparseCam4D 做法 | 因果效应 |
|---------|-------------|----------------|---------|
| **辅助观察来源** | 仅依赖真实视图和几何正则化 | 利用视频扩散模型生成额外视角时序视频 | 补充稀疏输入的信息缺口 |
| **不一致性建模** | 无显式建模，直接使用生成视图 | 引入STDF显式建模时空扭曲 | 将生成误差隔离于扭曲高斯，保护规范表示 |
| **相机姿态** | 固定姿态（如COLMAP估计） | 将外参作为可学习变量联合优化 | 校正生成视图扭曲对姿态估计的偏置 |
| **生成视图损失** | 标准光度损失（L1 + D-SSIM） | 引入感知损失（LPIPS）应对固有扭曲 | 容忍生成帧的非刚性变形 |

### 消融验证的核心结论

1. **STDF 的绝对必要性**：移除扭曲场后，Train场景 LPIPS 从 0.264 剧增至 0.608，SSIM 降至 0.426（Table 2），渲染结果出现严重模糊和时序不稳定（Figure 5）。
2. **时空联合建模的必要性**：仅建模空间维度（w/o time axis）或仅建模时间维度（w/o pose axis）均导致性能大幅下降，说明生成不一致同时存在于时空两个维度。
3. **对视频扩散模型的泛化性**：将生成先验更换为 ViewCrafter 后，加入 STDF 可将 PSNR 提升 2.51 dB（21.42→23.93），验证了STDF对不同视频扩散模型的通用性（Table 4）。
4. **零推理开销**：STDF 仅在训练时使用，训练后丢弃，新视角渲染无需任何额外计算。

SparseCam4D 的整体管道围绕一个核心矛盾展开：**视频扩散模型能提供稀疏相机之外的辅助观察，但这些生成观察天然携带时空不一致性，直接用于4D重建会导致严重模糊和时序不稳定**。框架通过“生成—扭曲解耦—联合重建—后丢弃”的四阶段流解决这一问题。

### 管道总览

管道由四个核心模块串联组成，其输入输出关系如 Figure 3 所示：

![[assets/figures/papers/paper_list_l46_https_arxiv_org_abs_2603_26481/figures/003_Figure_3.jpg]]
*Figure 3: Method overview. Given a generated frame at temporal index t and pose index s, each 4D Gaussian at*

1. **视频扩散模型生成**  
   以稀疏相机输入（2–3个视图）和从这些视图重建的粗糙点云作为条件，利用相机可控的视频扩散模型生成其他视角的完整时序视频。这些生成帧作为辅助观察，为后续重建提供额外的空间覆盖和时间信息。

2. **4D高斯泼溅重建**  
   使用规范4D高斯表示动态场景。每个4D高斯在给定时间 $t$ 通过时间高斯权重切片为3D高斯（Eq. 1），再经可微泼溅渲染真实视图。这一表示是重建的空间载体。

3. **时空扭曲场（STDF）**  
   这是方法的核心创新。STDF 接收规范4D高斯和时空索引 $(t, s)$，通过九平面（Ennea-plane）表示和轻量MLP解码器输出位置、旋转、缩放的扭曲偏移量，将规范高斯变形为“扭曲高斯”。**扭曲高斯专门用于渲染生成视图，规范高斯则用于渲染真实视图**，从而将生成观察中的时空不一致性显式解耦到生成视图专用的扭曲高斯中，避免污染规范表示。

4. **联合优化与正则化**  
   高斯属性、相机外参、扭曲场参数在统一框架下联合优化。真实视图使用标准光度损失（$\mathcal{L}_{\text{input}}$，Eq. 6），生成视图使用 L1 + LPIPS 的组合损失（$\mathcal{L}_{\text{gen}}$，Eq. 7），以应对生成帧的固有扭曲。同时施加相机姿态正则化（$\mathcal{L}_{\text{pose}}$，Eq. 8）、空间TV平滑（$\mathcal{L}_{\text{TV}}$）和姿态轴平滑（$\mathcal{L}_{\text{smooth}}$，Eq. 9）以增强优化稳定性。

### 关键设计决策

- **训练后丢弃STDF**：扭曲场仅在训练期间存在，用于吸收生成观察的不一致性。训练完成后，STDF 被完全丢弃，新视角渲染仅使用规范4D高斯，**零推理开销**。这一设计使得生成先验的优势得以利用，而不牺牲推理效率。

- **相机姿态联合优化**：将相机外参作为可学习变量与高斯属性同步优化，而非固定于COLMAP估计值。消融实验（Tab. 3）表明，关闭姿态优化会使 SSIM 从 0.656 降至 0.569，LPIPS 从 0.264 升至 0.336，说明生成视图的扭曲会严重偏置姿态估计。

- **生成视图的感知损失**：对生成帧引入 LPIPS 损失，而非仅使用标准 L1+D-SSIM。消融实验（Tab. 3）显示，移除 $\mathcal{L}_{\text{lpips}}$ 后 LPIPS 从 0.264 升至 0.285，验证了感知损失对生成帧扭曲的容忍能力。

### 输入输出流

- **输入**：2–3个稀疏标定（或未标定）相机的多视角动态视频，以及对应的COLMAP初始姿态估计。
- **生成中间产物**：视频扩散模型产生的其他视角时序视频帧。
- **输出**：可渲染任意新视角、任意时刻的规范4D高斯表示，具备时空一致性和照片级真实感。
- **推理时**：仅需规范4D高斯，无需扩散模型或扭曲场，直接泼溅渲染。

SparseCam4D 的完整管道由四个关键模块串联构成，其核心创新在于**时空扭曲场（Spatio-Temporal Distortion Field, STDF）**——一个轻量级的可学习组件，用于显式建模视频扩散模型生成视图中的时空不一致性，并在训练后完全丢弃以实现零推理开销。

### 4D 高斯泼溅表示

动态场景由一组规范 4D 高斯 $\mathcal{G}_{4D}$ 表示，每个高斯在 4D 空间 $(\mathbf{x}, y, z, t)$ 中定义。给定时间 $t$，通过时间高斯权重将 4D 高斯投影到 3D 空间：

$$\mathcal{G}_{3D}(\pmb{x}, t) = \mathrm{e}^{-\frac{1}{2}\lambda(t - \mu_t)^2} \mathrm{e}^{-\frac{1}{2}[\pmb{x} - \pmb{\mu}(t)]^T \pmb{\Sigma}_{3D}^{-1}[\pmb{x} - \pmb{\mu}(t)]}$$

其中第一项为时间高斯权重，控制该高斯在时刻 $t$ 的活跃程度（$\lambda$ 为时间带宽参数，$\mu_t$ 为时间中心）；第二项为标准 3D 空间高斯函数，$\pmb{\mu}(t)$ 和 $\pmb{\Sigma}_{3D}$ 分别为时间 $t$ 下的位置和协方差矩阵。通过可微泼溅渲染，规范高斯用于渲染真实相机视图。

### 时空扭曲场

生成视图存在**空间不一致**（同一时刻不同视角间）和**时间不一致**（同一视角不同时刻间），直接将其用于 4D 重建会导致严重模糊和时序不稳定。STDF 的核心设计是将这种不一致性**解耦到生成视图专用的扭曲高斯中**，而真实视图仍使用原始规范高斯渲染。

STDF 形式化为一个映射：

$$\mathcal{F} : (\mathcal{G}_{4D}, t, s) \mapsto \Delta\mathcal{G}_{4D}$$

其中 $t$ 为时间索引，$s$ 为生成视图的相机姿态索引，$\Delta\mathcal{G}_{4D}$ 为预测的扭曲偏移量（包括位置偏移 $\Delta\pmb{\mu}$、旋转偏移 $\Delta\pmb{q}_l, \Delta\pmb{q}_r$ 和缩放偏移 $\Delta\pmb{s}$）。

**Ennea-平面表示**：STDF 将 5D 体积 $(x,y,z,t,s)$ 分解为 9 个二维特征平面（10 个可能的二元组合中排除不编码扭曲信息的 $(t,s)$ 平面）。对于每个 4D 高斯的 5D 坐标 $c$，将其投影到各特征平面并通过双线性插值提取特征：

$$f(c)_c = \operatorname{interp}(P_c, \pi_c(c)), \quad c \in \{xy, xz, yz, xt, yt, zt, xs, ys, zs\}$$

其中 $P_c$ 为对应平面的可学习特征图，$\pi_c(c)$ 为坐标投影函数。所有平面的特征通过逐元素乘法融合，并串联多分辨率特征：

$$f(c) = \bigcup_{sc} \prod_{P_c \in P} f(c)_c$$

融合特征经轻量级多头 MLP 解码为扭曲偏移量，施加到规范高斯属性上得到扭曲高斯：

$$(\pmb{\mu}', \pmb{q}_l', \pmb{q}_r', \pmb{s}') = (\pmb{\mu} + \Delta\pmb{\mu}, \pmb{q}_l + \Delta\pmb{q}_l, \pmb{q}_r + \Delta\pmb{q}_r, \pmb{s} + \Delta\pmb{s})$$

训练期间，扭曲高斯用于渲染生成视图，规范高斯用于渲染真实视图；训练完成后，STDF 被完全丢弃，新视角渲染仅使用规范 4D 高斯，实现零额外计算开销。

### 相机姿态联合优化

为应对稀疏输入下 COLMAP 姿态估计的不准确性，将相机外参作为可学习变量与高斯属性联合优化。这一设计同时有助于补偿生成视图中的姿态相关扭曲。

### 损失函数设计

针对真实视图与生成视图的不同特性，采用差异化的损失函数。对真实输入视图使用标准光度损失：

$$\mathcal{L}_{\mathrm{input}} = (1 - \lambda)\mathcal{L}_{1} + \lambda\mathcal{L}_{\mathrm{D-SSIM}}$$

对生成视图，考虑到其固有的感知扭曲，引入感知损失（LPIPS）：

$$\mathcal{L}_{\mathrm{gen}} = \lambda_1\mathcal{L}_{1} + \lambda_2\mathcal{L}_{\mathrm{lpips}}$$

此外，为稳定优化过程，引入相机姿态正则化（约束优化后姿态不偏离 COLMAP 初始化过远）：

$$\mathcal{L}_{\mathrm{pose}} = \lambda_p(||T - \hat{T}|| + ||q - \hat{q}||)$$

以及姿态轴平滑正则化（对特征平面沿姿态轴施加二阶导数约束）：

$$\mathcal{L}_{\mathrm{smooth}} = \lambda_s \frac{1}{|C|} \sum_{c \in C} \frac{1}{N_i N_s} \sum_{i,s} \|(P_c^{i,s-1} - P_c^{i,s}) - (P_c^{i,s} - P_c^{i,s+1})\|_2^2$$

总损失为上述各项的加权组合：

$$\mathcal{L} = \mathcal{L}_{\mathrm{input}} + \mathcal{L}_{\mathrm{gen}} + \mathcal{L}_{\mathrm{pose}} + \mathcal{L}_{\mathrm{TV}} + \mathcal{L}_{\mathrm{smooth}}$$

其中 $\mathcal{L}_{\mathrm{TV}}$ 为空间特征平面的总变分平滑正则项。

![[assets/figures/papers/paper_list_l46_https_arxiv_org_abs_2603_26481/figures/011_Figure_6.jpg]]
*Figure 6: Visualization of the STDF. Spatio-Temporal Distortion Field output is rendered as a per-primitive attribute, with brighter regions indicating higher distortions (left). The corresponding areas in the input generated image (right) align with regions exhibiting noticeable deformation (red box)*

## 实验与关键发现

### 主要结果

SparseCam4D 在三个标准动态场景基准上进行了系统评估：**Technicolor**、**Neural 3D Video** 和 **Nvidia Dynamic Scenes**。训练仅使用 2–3 个稀疏相机视图，测试在所有剩余视图上进行。基线方法包括 **HyperReel**、**4DGaussians**、**4D-Rotor**、**RealTime4DGS** 和 **MonoFusion**，其中 MonoFusion 在训练和测试时均使用真值相机姿态，这为基线提供了温和的优势设定。

如 Table 1 所示，本方法在所有数据集的所有指标上均取得最优结果。在 Technicolor 上，PSNR 达到 23.15 dB，比最优基线 MonoFusion 高出 5.18 dB，SSIM 提升 0.150，LPIPS 降低 0.053。在 Neural 3D Video 上，PSNR 为 21.91 dB，领先 3.48 dB。在 Nvidia Dynamic Scenes 上，PSNR 达 24.81 dB，SSIM 提升 0.204。这些提升的核心驱动因素是时空扭曲场（STDF）将生成视图中的不一致性解耦到专用扭曲高斯中，使规范高斯能够从真实视图中学习到清晰、稳定的场景表示。

![[assets/figures/papers/paper_list_l46_https_arxiv_org_abs_2603_26481/figures/004_Table_1.jpg]]
*Table 1: Qualitative comparisons on Technicolor [26], Neural 3D Video [13], and Nvidia Dynamic Scenes [46] Datasets. The first and second best performances are highlighted in red and yellow. Our method shows superior performance compared to all baseline methods across all metrics. Note that MonoFusion∗ is our reproduced version*

定性对比（Figure 4）进一步验证了本方法在细节清晰度和时空一致性上的显著优势：基线方法在稀疏输入下普遍出现模糊、伪影或时序抖动，而 SparseCam4D 保持了照片级真实感和稳定的动态表现。

### 消融实验

#### 时空扭曲场（STDF）的绝对必要性

Table 2 给出了 STDF 的消融结果。**移除整个扭曲场**后，Train 场景的 LPIPS 从 0.264 剧增至 0.608，SSIM 从 0.656 骤降至 0.426——生成帧中的时空不一致直接污染了场景表示，导致严重模糊和时序不稳定。Figure 5 通过时空切片可视化印证了这一现象：无扭曲场时，运动区域（如挥手）出现明显的拖影和时间轴上的剧烈抖动。

![[assets/figures/papers/paper_list_l46_https_arxiv_org_abs_2603_26481/figures/006_Table_2.jpg]]
*Table 2: Ablation studies on STDF. We randomly select one representative scene from Technicolor [26] and Nvidia Dynamic Scenes [46] to ablate Spatio-Temporal Distortion Field*

![[assets/figures/papers/paper_list_l46_https_arxiv_org_abs_2603_26481/figures/007_Figure_5.jpg]]
*Figure 5: Spatio-Temporal Consistency. Rendering results (top) and space-time slices (bottom) constructed by concatenating the red pixel locations across all time steps, demonstrate that direct reconstruction from diffusion observations leads to severe blur and temporal instability(e.g., the moving hand at the bottom right)*

进一步消融 STDF 的时空维度：
- **移除时间轴**（w/o time axis）：仅建模空间不一致，LPIPS 升至 0.458，SSIM 降至 0.480。
- **移除姿态轴**（w/o pose axis）：仅建模时间不一致，LPIPS 升至 0.469，SSIM 降至 0.462。

这表明生成不一致同时存在于空间和时间两个维度，且两者的联合建模是 STDF 有效性的关键。

#### 相机姿态优化与损失组件

Table 3 消融了姿态优化和各损失项。**关闭相机姿态优化**后，Train 场景 SSIM 从 0.656 降至 0.569，LPIPS 升至 0.336——生成视图的扭曲会严重偏置姿态估计，导致重建质量显著下降。移除 LPIPS 损失（w/o $\mathcal{L}_{lpips}$）使 LPIPS 升至 0.285，表明感知损失对应对生成帧的固有扭曲不可或缺。移除空间 TV 平滑（w/o $\mathcal{L}_{TV}$）或姿态轴平滑正则化（w/o $\mathcal{L}_{smooth}$）均导致 LPIPS 升至约 0.31，验证了正则化项对优化稳定性的贡献。

![[assets/figures/papers/paper_list_l46_https_arxiv_org_abs_2603_26481/figures/009_Table_3.jpg]]
*Table 3: Ablation studies on pose optimization and loss components. We randomly select one representative scene from Technicolor [26] and Nvidia Dynamic Scenes [46] Datasets to ablate pose optimization and loss components*

#### 不同视频扩散模型的泛化性

Table 4 展示了使用 **ViewCrafter** 作为替代生成先验的结果。加入 STDF 后，PSNR 从 21.42 dB 提升至 23.93 dB（+2.51 dB），验证了 STDF 对不同视频扩散模型（VDMs）的泛化能力——扭曲场的设计不依赖于特定生成模型，而是对生成不一致性这一普遍问题提供通用解耦机制。

### 失败模式与局限性

本方法的性能高度依赖所使用视频扩散模型的生成质量。当输入场景处于模型训练域外（如人物数据稀少）或点云渲染条件质量较低时，生成帧可能出现严重变形和幻影，此时 STDF 虽能部分缓解，但重建质量仍会下降。此外，当前验证仅覆盖 2–3 个相机视图的设置；对于更极端的稀疏条件（如单目或单视图），管道的适用性尚需进一步研究。测试时需对测试视图进行额外的姿态对齐优化，略微增加了实际部署的复杂度。

### 关键图表索引

- **Table 1**：三个数据集上的主结果定量对比，本方法在所有指标上显著领先。
- **Table 2**：STDF 消融实验，验证完整时空建模的绝对必要性。
- **Table 3**：姿态优化与损失组件消融，各组件对最终质量均有贡献。
- **Table 4**：替代 VDM 的泛化性验证，STDF 在不同生成模型上均有效。
- **Figure 4**：定性对比，展示本方法在细节和时空一致性上的优势。
- **Figure 5**：时空一致性可视化，无扭曲场时出现严重模糊和时间不稳定。
- **Figure 6**：STDF 输出可视化，高扭曲区域与生成图像中的明显变形区域吻合。

## 定位与知识库关联

### 任务定位与基线谱系

SparseCam4D 解决的核心问题是**稀疏多相机（2–3个视角）下的动态场景4D重建**，其输入为未标定的RGB视频流，输出为时空一致的新视角渲染。该设定处于动态神经渲染、4D高斯泼溅与视频扩散先验的交汇点。

论文实验部分对比了以下代表性基线方法：

- **MonoFusion**（论文中标注为 MonoFusion∗ 复现版本）：单目动态重建方法，训练与测试时均使用真值相机姿态，为基线提供了温和的优势设定。
- **4DGaussians**：基于4D高斯的动态场景表示方法。
- **4D-Rotor**：动态场景重建方法。
- **RealTime4DGS**：实时4D高斯泼溅方法。
- **HyperReel**：动态神经渲染方法。

在 Technicolor、Neural 3D Video 和 Nvidia Dynamic Scenes 三个标准基准上，SparseCam4D 在所有指标上显著领先。以 Technicolor 为例，PSNR 达到 23.15 dB，较 MonoFusion∗ 的 17.97 dB 提升 **+5.18 dB**；SSIM 从 0.578 提升至 0.728，LPIPS 从 0.352 降至 0.299（Table 1）。值得注意的是，基线方法使用了真值姿态，而 SparseCam4D 仅依赖未标定的稀疏输入，这一不公平设定反而凸显了方法的鲁棒性。

### 关键设计增量与因果机制

SparseCam4D 的核心增量并非简单的“生成视图+重建”组合，而是对生成先验引入的**时空不一致性**进行了显式建模与解耦。方法谱系上的关键设计变更包括：

| 设计槽位 | 基线做法 | SparseCam4D 做法 | 因果作用 |
|----------|----------|------------------|----------|
| 辅助观察来源 | 仅依赖真实视图与几何正则化 | 利用相机控制的视频扩散模型生成额外视角的时序视频 | 突破稀疏观测的信息瓶颈 |
| 不一致性建模 | 无显式建模，直接将生成视图用于重建 | 引入**时空扭曲场（STDF）**，显式建模生成观察中随空间和时间的扭曲 | 将生成误差解耦到扭曲高斯，保护规范高斯的时空一致性 |
| 相机姿态 | 固定姿态（COLMAP估计） | 将外参作为可学习变量与高斯属性联合优化 | 补偿生成视图扭曲对姿态估计的偏置 |
| 生成视图损失 | 标准光度损失（L1 + D-SSIM） | 引入感知损失（LPIPS）以应对生成帧的固有扭曲 | 容忍生成帧的纹理偏移，避免过拟合到伪影 |

**因果枢纽：时空扭曲场（STDF）**。STDF 接收规范4D高斯与时空索引 $(t, s)$，通过 Ennea-plane 表示（将5D体积分解为9个二维特征平面）和轻量多头 MLP 输出位置、旋转、缩放的扭曲偏移量。训练时，扭曲后的高斯用于渲染生成视图，规范高斯用于渲染真实视图，从而将生成视图的不一致性隔离在扭曲分支中。训练完成后，STDF 被完全丢弃，**新视角渲染零额外推理开销**。

### 消融实验的证据强度

消融实验提供了 STDF 必要性的强证据（Table 2）：

- **移除整个扭曲场**：Train 场景的 LPIPS 从 0.264 剧增至 **0.608**，SSIM 从 0.656 降至 **0.426**。这表明直接使用扩散生成帧进行重建会导致严重的质量退化。
- **仅建模空间维度（w/o time axis）或仅建模时间维度（w/o pose axis）**：性能均大幅下降（LPIPS 升至 0.458–0.469，SSIM 降至 0.462–0.480），验证了生成不一致同时存在于时空两个维度，单一维度的建模不足以解耦误差。

姿态优化和损失组件的消融（Table 3）进一步表明：
- 关闭相机姿态优化后，Train 场景 SSIM 降至 0.569，LPIPS 升至 0.336，证实生成视图的扭曲会严重偏置姿态估计。
- 移除 LPIPS 损失（仅用 L1）导致 LPIPS 从 0.264 升至 0.285，说明感知损失对容忍生成帧的纹理偏移至关重要。
- TV 平滑和姿态轴平滑正则化的移除均导致性能下降，验证了这些正则项对稳定优化的贡献。

**跨模型泛化性**：在 Cook Spinach 场景上使用 ViewCrafter 替代默认视频扩散模型时，加入 STDF 可将 PSNR 从 21.42 提升至 **23.93（+2.51 dB）**（Table 4），验证了 STDF 对不同视频扩散模型的泛化能力。

### 适用边界与局限

1. **生成模型依赖**：重建质量高度依赖视频扩散模型的性能。当输入处于模型训练域外（如人物数据稀少）或点云渲染条件质量较低时，生成帧可能出现严重变形和幻影，导致重建质量下降（论文 Fig. 11 所示，需手动验证具体退化程度）。
2. **稀疏程度上限**：当前仅在 2–3 个相机视图上验证；对于更极端的稀疏设置（如单目或单视图），管道的适用性和重建质量仍需进一步研究。
3. **测试时额外优化**：测试时需要对测试视图进行额外的姿态对齐优化，略微增加了实际部署的复杂度，限制了直接即用的实时性。
4. **相机选择未自动化**：论文未详细讨论相机子集选择策略在目标覆盖率未达标时的回退机制。

### 开放问题

1. **生成与重建的端到端协同**：当前管道将视频扩散模型的生成作为固定先验，能否将生成模型的迭代优化纳入重建循环，实现生成与重建的端到端协同优化？
2. **STDF 的泛化边界**：时空扭曲场是否适用于其他类型的生成先验（如从单目深度估计或光流生成的视图），以及是否可推广到非高斯表示的动态重建框架？
3. **自适应视图选择**：如何量化并自适应地选择最有助于4D重建的生成视图，以在保证重建质量的前提下减少冗余计算和生成开销？
4. **极端稀疏下的理论下限**：在仅有一个或两个输入视图的极端条件下，生成先验与几何正则化之间的信息互补是否存在理论上的重建精度下限？

## 原文 PDF

![[paperPDFs/CVPR_2026/SparseCam4D_Spatio_Temporally_Consistent_4D_Reconstruction_from_Sparse_Cameras.pdf]]
