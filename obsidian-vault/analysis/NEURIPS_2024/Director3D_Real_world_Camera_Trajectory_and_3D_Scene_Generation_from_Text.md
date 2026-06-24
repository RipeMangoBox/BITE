---
title: "Director3D: Real-world Camera Trajectory and 3D Scene Generation from Text"
type: paper
paper_level: A
venue: NEURIPS
year: 2024
pdf_ref: paperPDFs/NEURIPS_2024/Director3D_Real_world_Camera_Trajectory_and_3D_Scene_Generation_from_Text.pdf
aliases:
- Director3D
tags:
- NEURIPS_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 通过轨迹扩散Transformer生成自适应相机轨迹，结合高斯驱动的多视角潜在扩散模型直接生成像素对齐的3D高斯，并利用SDS++损失进行精炼，实现了真实世界3D场景的生成。
primary_logic: 将真实世界多视角数据建模为相机轨迹与图像序列的联合分布，分别采用轨迹扩散Transformer、高斯驱动的多视角潜在扩散模型和SDS++损失进行分治，有效解决了真实世界文本到3D生成的关键挑战。
claims:
- Director3D在T3Bench上取得BRISQUE 32.3、NIQE 4.35、CLIP-Score 85.5，显著优于其他方法。
- SDS++损失的消融实验表明，去除自适应源预测会导致过平滑，去除图像空间损失会导致细节缺失，验证了各组件的重要性。
- 与GRM、GaussianDreamer等基线方法的定性比较中，Director3D生成的场景更真实，具有更好的光影、材质和背景一致性。
- 使用随机生成相机轨迹的消融实验生成结果视角不佳或范围受限，证明了场景特定轨迹的重要性。
---

# Director3D: Real-world Camera Trajectory and 3D Scene Generation from Text

> [!tip] 核心洞察
> 将真实世界多视角数据建模为相机轨迹与图像序列的联合分布，分别采用轨迹扩散Transformer、高斯驱动的多视角潜在扩散模型和SDS++损失进行分治，有效解决了真实世界文本到3D生成的关键挑战。

| 字段 | 内容 |
|------|------|
| 中文题名 | Director3D：真实世界相机轨迹与3D场景文本生成 |
| 英文题名 | Director3D: Real-world Camera Trajectory and 3D Scene Generation from Text |
| 会议/期刊 | NEURIPS 2024 |
| Links | [paper](https://arxiv.org/abs/2406.17601) · [Code](https://github.com/imlixinyang/director3d) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | Director3D |
| Dataset | T3Bench |

> [!tip] 效果简介
> - T3Bench 上，BRISQUE ↓ 32.3 vs 61.5 (ProlificDreamer) (-29.2)；NIQE ↓ 4.35 vs 7.07 (ProlificDreamer) (-2.72)；CLIP-Score ↑ 85.5 vs 69.4 (ProlificDreamer) (+16.1)。

## 概述

**Director3D** 提出了一种从文本描述直接生成真实世界3D场景及其自适应相机轨迹的框架。现有文本到3D生成方法主要面向物体级别，依赖预定义或用户指定的固定相机轨迹，难以建模真实世界多视角数据中复杂的场景特定轨迹和无界背景，导致生成质量与通用性受限。

Director3D 的核心洞察在于将真实世界多视角数据建模为相机轨迹与图像序列的联合分布，并通过三个分治模块实现文本到3D场景的生成：(1) **Traj-DiT**（轨迹扩散Transformer）作为 Cinematographer，从文本自适应生成密集相机轨迹；(2) **GM-LDM**（高斯驱动的多视角潜在扩散模型）作为 Decorator，利用轨迹的稀疏子集直接生成像素对齐的3D高斯场景；(3) **SDS++损失**作为 Detailer，通过密集相机插值渲染与2D扩散先验精炼细节。

在 T3Bench 基准上，Director3D 取得 BRISQUE 32.3、NIQE 4.35、CLIP-Score 85.5，显著优于 **ProlificDreamer**（Wang et al., 2023）等基线方法。消融实验验证了场景特定相机轨迹与 SDS++ 各组件的关键作用。该方法为真实世界文本到3D场景生成提供了新的方法论范式。

## 背景与动机

### 文本到3D生成的演进与瓶颈

近年来，文本到3D生成技术取得了显著进展。以**DreamFusion**（Poole et al., ICLR 2023）为代表的Score Distillation Sampling（SDS）方法，通过利用预训练的2D扩散模型作为先验，实现了从文本描述到3D资产的生成。后续工作如**Magic3D**（Lin et al., CVPR 2023）、**ProlificDreamer**（Wang et al., 2023）等进一步提升了生成质量与保真度。然而，这些方法的成功主要局限于**物体级别**的生成——它们通常依赖预定义的、环绕物体的固定相机轨迹（如环绕物体的半球面采样），并假设场景是封闭的、有界的。

这一范式在面对**真实世界3D场景生成**时暴露出根本性缺陷。真实世界的多视角捕获数据（如室内房间、室外景观）具有两个关键特征：其一，相机轨迹是**场景特定的**，由场景布局、深度范围和内容语义共同决定，远非简单的环绕轨迹所能涵盖；其二，场景通常是**无界的**，包含复杂的背景、光影和材质变化。现有方法无法有效利用这些真实世界数据中的丰富信息，导致生成质量与通用性严重受限。

### 核心瓶颈：相机轨迹与场景表示的割裂

问题的本质在于，现有方法将相机轨迹视为一个独立于场景内容的“外部变量”——要么采用固定的环绕轨迹，要么由用户手动指定。这种割裂导致了两个层面的失败：

1. **轨迹不适配**：固定的环绕轨迹无法适应真实场景的几何与语义结构。例如，对于“一个狭窄的走廊”和“一个开阔的广场”，最优的观察视角和移动路径截然不同。使用随机生成的相机轨迹进行消融实验表明，生成结果会出现视角怪异或相机范围受限的问题（Figure 12, Appendix E），直接验证了场景特定轨迹的必要性。

2. **生成范式错位**：物体级别的生成方法（如SDS优化NeRF或3D高斯）假设从任意视角观察物体都是合理的，但场景生成需要考虑视角的合理性和背景的一致性。基于2D多视角扩散加重建的方法虽然能利用真实数据，但往往需要密集的视角覆盖，且难以保证3D一致性。

### Director3D的动机与核心洞察

Director3D的核心洞察在于：**将真实世界多视角数据建模为相机轨迹与图像序列的联合分布**，并采用分治策略分别处理这一联合分布的不同维度。具体而言：

- **相机轨迹**的分布由场景语义决定，需要一个能够理解场景结构并生成合理观察路径的模块；
- **3D场景表示**需要与相机轨迹紧密耦合，确保从生成轨迹的任意视角观察时，场景都是像素对齐且一致的；
- **细节精炼**需要利用2D扩散先验，但必须适应真实世界场景的复杂性和无界特性。

基于这一洞察，Director3D设计了三个协同工作的核心组件：Cinematographer（轨迹扩散Transformer）负责生成自适应相机轨迹，Decorator（高斯驱动的多视角潜在扩散模型）负责生成像素对齐的初始3D高斯场景，Detailer（SDS++损失）负责通过密集相机插值渲染与2D扩散先验精炼细节。这一框架首次实现了从文本描述到真实世界3D场景（含自适应相机轨迹）的端到端生成。

## 核心创新

Director3D 的核心创新在于将真实世界文本到 3D 场景生成问题重新建模为**相机轨迹与图像序列的联合分布学习**，并通过三个关键组件的协同分治，系统性地突破了现有方法在真实世界场景生成中的瓶颈。

### 瓶颈定位：从物体到真实世界场景的范式迁移

现有文本到 3D 生成方法（如 **DreamFusion** (Poole et al., ICLR 2023)、**ProlificDreamer** (Wang et al., 2023) 等）主要针对物体级别生成，其相机轨迹通常为简单的环绕仰角固定轨迹。然而，真实世界多视角捕获数据中的相机轨迹具有场景特定的复杂性（如无界背景、非均匀采样），且合成数据集的简化轨迹分布与真实世界分布存在本质差异（见 Figure 3 左）。这一分布差异导致现有方法在真实世界场景生成中面临**生成质量受限**和**通用性不足**的双重困境。

### 关键创新槽位

Director3D 在三个关键维度上实现了相对 baseline 的突破性改进：

**1. 相机轨迹生成：从固定预设到自适应生成**

- **Baseline 做法**：预定义或用户指定的固定轨迹（如环绕仰角轨迹）。
- **Director3D 创新**：提出 **Trajectory Diffusion Transformer (Traj-DiT)**（见 Figure 4 左），将相机外参建模为时序 token，通过扩散 Transformer 从文本条件自适应生成密集的、场景特定的相机轨迹。该模块从噪声轨迹出发，经多步去噪逐步恢复出与文本语义匹配的相机轨迹（见 Figure 4 右）。
- **因果机制**：Traj-DiT 直接对真实世界捕获数据中的轨迹分布 $p(\mathcal{C}|y)$ 进行建模，使生成的轨迹天然具备真实世界场景的复杂特性，为后续 3D 场景生成提供合理的基础观测视角。

**2. 3D 场景表示生成：从 2D 扩散+重建到像素对齐的直接生成**

- **Baseline 做法**：先通过 2D 多视角扩散生成图像，再重建 3D 表示，或通过 SDS 优化隐式表示。
- **Director3D 创新**：提出 **Gaussian-driven Multi-view Latent Diffusion Model (GM-LDM)**（见 Figure 5 左），从 2D LDM 微调而来，利用稀疏子集相机轨迹进行图像序列扩散，通过**渲染驱动的去噪**直接生成像素对齐的 3D Gaussian。训练时采用联合损失 $\mathcal{L}_{2\mathrm{d}}$（潜在空间多视角去噪）和 $\mathcal{L}_{3\mathrm{d}}$（渲染图像与真实图像重建损失），使生成的 3D Gaussian 天然与多视角图像保持像素级一致性。
- **因果机制**：GM-LDM 将 3D 表示生成内嵌于扩散去噪过程中，避免了“先 2D 后 3D”两阶段流程中的信息损失，同时 3D Gaussian 的无界表达能力使其天然适配真实世界场景的无界背景。

**3. 细节精炼损失：从标准 SDS 到自适应 SDS++**

- **Baseline 做法**：标准 Score Distillation Sampling (SDS) 损失。
- **Director3D 创新**：提出 **SDS++ 损失**（见 Figure 5 右），包含两个关键改进：
  - **自适应源预测**：使用可学习文本嵌入 $\hat{y}$ 进行源噪声预测 $\hat{\epsilon}_{\mathrm{src}} = \epsilon_{\theta}(z_t, \hat{y}, t)$，替代标准 SDS 中直接使用目标文本条件的做法，有效估计当前渲染分布的 score，避免过平滑。
  - **潜在空间与图像空间联合目标**：损失函数 $\mathcal{L}_{\mathrm{SDS++}} = \mathbb{E}_{t,c,\epsilon} \left[ w(t) \frac{\sqrt{\bar{\alpha}_t}}{\sqrt{1-\bar{\alpha}_t}} \left( \lambda_z \|z - \hat{z}\|_2^2 + \lambda_x \|x - \hat{x}\|_2^2 \right) \right]$ 同时考虑潜在空间目标（$\lambda_z=1$）和图像空间目标（$\lambda_x=0.01$），结合分类器自由引导的目标预测 $\hat{\epsilon}_{\mathrm{trg}}$（$\omega_{\mathrm{cfg}}=7.5$），在细节丰富度和文本对齐度之间取得平衡。
- **因果机制**：自适应源预测避免了将目标分布强加于当前渲染导致的过平滑问题；联合空间目标使精炼过程既能利用潜在空间的语义先验，又能保留图像空间的高频细节。

### 创新有效性验证

消融实验（Figure 8, Section 5.5）系统性地验证了各创新组件的因果贡献：
- **去除精炼过程**：视觉质量显著下降，细节缺失。
- **将 $\epsilon_{\mathrm{src}}$ 设为 $\epsilon$**：SDS++ 退化为 SDS+，引起过平滑，证明自适应源预测的必要性。
- **将 $\omega_{\mathrm{cfg}}$ 设为 1**：SDS++ 退化为 LODS，导致噪声细节，验证分类器自由引导的作用。
- **仅使用潜在空间损失**：导致噪声与伪影；**仅使用图像空间损失**：导致细节缺失。证明联合空间目标的必要性。

随机生成相机轨迹的消融实验（Figure 12, Appendix E）进一步证明，使用随机轨迹生成的场景视角不佳或范围受限，验证了 Traj-DiT 生成场景特定轨迹的重要性。

### 方法谱系与知识库定位

Director3D 在文本到 3D 生成领域的方法谱系中占据独特位置：

| 方法类别 | 代表方法 | 核心范式 | Director3D 的差异 |
|---------|---------|---------|------------------|
| SDS 优化 | DreamFusion, SJC, ProlificDreamer | 通过 2D 扩散先验优化 3D 表示 | 引入自适应源预测与联合空间目标，解决过平滑与细节缺失 |
| 解耦几何与外观 | Fantasia3D (Chen et al., ICCV 2023) | 分别优化几何与外观 | 统一框架同时生成轨迹与场景，避免解耦误差 |
| 前馈式生成 | GRM (Xu et al., arXiv 2024) | 前馈网络直接预测 3D Gaussian | 引入扩散模型的迭代精炼能力，提升生成质量 |
| 场景级生成 | DreamScene, LucidDreamer (Chung et al., 2023) | 场景级 3D 生成 | 通过自适应轨迹生成实现更真实的相机运动与场景一致性 |

**待验证点**：由于缺乏部分 baseline 方法的完整引用信息（如 DreamScene 的准确引用），上述谱系定位中个别方法的对比需结合原始文献进一步确认。

## 整体框架

Director3D 将真实世界文本到3D场景生成建模为**图像序列与相机轨迹在文本条件下的联合分布**学习问题，并通过三个解耦模块分治该联合分布：$p((\mathcal{X}, \mathcal{C}) \mid y)$。

### 核心设计动机

现有文本到3D方法主要面向物体级别生成，依赖预定义或用户指定的固定相机轨迹。然而，真实世界多视角捕获数据中的相机轨迹分布远比合成数据复杂（Figure 3 左），包含场景特定的仰角变化、轨迹弧度和无界背景。直接套用固定轨迹策略会导致生成视角不佳或范围受限。Director3D 的核心洞察在于：**将相机轨迹本身作为生成目标**，使其与场景内容协同优化，从而突破物体级方法的泛化瓶颈。

### 三阶段流水线

整体框架（Figure 1）由三个功能互补的模块串联构成：

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2406_17601/figures/001_Figure_1.jpg]]
*Figure 1: Given textual descriptions, Director3D employs three key components: the Cinematographer generates the camera trajectories, the Decorator creates the initial 3D scenes, and the Detailer refines the details*

| 模块 | 角色 | 输入 | 输出 | 关键作用 |
|------|------|------|------|----------|
| **Traj-DiT** | Cinematographer（摄影师） | 文本描述 $y$ | 密集相机轨迹 $\mathcal{C}$ | 自适应生成场景特定的多视角相机路径 |
| **GM-LDM** | Decorator（装饰师） | 文本 $y$ + 轨迹稀疏子集 $\mathcal{C}_{\text{sparse}}$ | 像素对齐的初始3D高斯 $\mathcal{G}_{\text{init}}$ | 建立粗粒度但几何一致的3D场景骨架 |
| **SDS++ Loss** | Detailer（细化师） | 初始3D高斯 $\mathcal{G}_{\text{init}}$ + 密集轨迹插值渲染 | 精炼后的3D高斯 $\mathcal{G}_{\text{refined}}$ | 补充高频细节、改善材质与光影 |

三者的信息流严格单向递进：Traj-DiT 生成的轨迹为 GM-LDM 提供多视角渲染锚点，GM-LDM 输出的初始高斯为 SDS++ 精炼提供可微初始化。这种解耦设计使得每个模块可以独立利用其最适合的预训练先验（轨迹扩散先验、多视角潜在扩散先验、2D扩散先验），同时避免端到端联合训练带来的优化困难。

### 模块间接口与数据流

1. **Traj-DiT → GM-LDM**：Traj-DiT（Figure 4）将相机外参视为时序 Token，通过 Transformer 架构在文本条件 $y$ 下进行条件去噪，直接从噪声中预测干净轨迹 $\mathcal{C}$。GM-LDM 仅选取该轨迹的**稀疏子集**（约 $N_{\text{sparse}}$ 个视角）作为输入，而非全量密集轨迹，以降低多视角扩散的计算开销。

2. **GM-LDM → SDS++**：GM-LDM（Figure 5 左）从 2D LDM 微调而来，在潜在空间中执行多视角去噪，同时通过**渲染驱动去噪**（rendering-based denoising）将去噪结果投影为像素对齐的 3D 高斯。该过程联合优化两个损失：
   - $\mathcal{L}_{\text{2d}}$：多视角潜在空间的 $\epsilon$-预测损失
   - $\mathcal{L}_{\text{3d}}$：渲染图像与真实图像的像素级重建损失

   输出的初始高斯 $\mathcal{G}_{\text{init}}$ 已具备粗粒度几何结构，但缺乏高频纹理和细节。

3. **SDS++ 精炼**：Detailer 阶段（Figure 5 右）利用 Traj-DiT 生成的**密集轨迹**进行插值渲染，将渲染结果送入原始 2D LDM 计算 SDS++ 损失。该损失的核心创新在于：
   - **自适应源预测**：使用可学习文本嵌入 $\hat{y}$ 估计当前分布的源噪声 $\hat{\epsilon}_{\text{src}}$，避免标准 SDS 的过平滑问题
   - **双空间联合目标**：同时在潜在空间（$\lambda_z \|z - \hat{z}\|_2^2$）和图像空间（$\lambda_x \|x - \hat{x}\|_2^2$）施加损失，平衡语义一致性与像素级细节
   - **分类器自由引导**：通过 $\omega_{\text{cfg}}$ 控制目标噪声预测，增强文本对齐度

### 与基线方法的架构差异

相比 **DreamFusion**（Poole et al., ICLR 2023）等纯 SDS 优化方法，Director3D 用 GM-LDM 的前馈生成替代了从零开始的逐场景优化，大幅缩短推理时间。相比 **GRM**（Xu et al., arXiv 2024）等前馈式重建方法，Director3D 通过 Traj-DiT 自适应生成相机轨迹，避免了固定轨迹导致的视角单一问题。相比 **GaussianDreamer**（Yi et al., CVPR 2024）结合 2D 与 3D 扩散模型的方案，Director3D 的 SDS++ 损失在精炼阶段同时利用潜在空间和图像空间监督，有效缓解了过平滑与细节缺失的权衡困境（Figure 8 消融验证）。

### 已知局限

该框架存在两个结构性的限制：其一，GM-LDM 支持的视角范围有限，导致生成场景的可探索视角广度受限；其二，开放世界泛化依赖额外的 SDS++ 精炼过程，降低了整体效率。论文指出，引入更广泛的多视角数据集可能缓解对精炼器的依赖，但当前尚无法完全消除这一环节。

## 核心模块与公式推导

Director3D 将真实世界多视角数据建模为图像序列与相机轨迹在文本条件下的联合分布 $p((\mathcal{X}, \mathcal{C}) | y)$，并通过三个核心模块分治求解：Cinematographer（轨迹生成）、Decorator（场景初始化）和 Detailer（细节精炼）。

---

### 4.2 Cinematographer：Trajectory Diffusion Transformer (Traj-DiT)

**瓶颈**：现有文本到3D方法依赖预定义或用户指定的固定相机轨迹（如环绕仰角轨迹），无法适应真实世界场景中复杂、自由的相机运动分布（Figure 3 左）。

**核心设计**：Traj-DiT 将相机轨迹建模为时序 token 序列，通过条件扩散模型从文本直接生成密集视图的相机外参。每帧相机外参 $\mathcal{C} = \{c_i\}_{i=1}^{N}$ 被展平为 token，Transformer 在噪声轨迹 $\mathcal{C}_t$ 上进行条件去噪，文本条件 $y$ 通过交叉注意力注入。

**训练损失**（$x_0$-prediction 形式）：

$$L = \mathbb{E}_{\mathcal{C}, \epsilon \sim \mathcal{N}(0,1), t} \Big[ \| \mathcal{C} - \mathcal{C}_{\theta}(\mathcal{C}_t, y, t) \|_2^2 \Big] \tag{5}$$

其中 $\mathcal{C}$ 为真实相机轨迹，$\mathcal{C}_t$ 为加噪后的轨迹，$\mathcal{C}_{\theta}$ 为 Traj-DiT 预测的去噪轨迹。Figure 4 右侧展示了不同去噪时间步下轨迹从随机噪声逐步收敛至合理相机路径的过程。

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2406_17601/figures/004_Figure_4.jpg]]
*Figure 4: Left: Architecture of Traj-DiT. Right: Visualization of the predicted camera trajectory for different denoising timesteps*

**因果机制**：该模块将相机轨迹从“人工预设”变为“文本条件生成”，使后续的场景生成能获得场景特定的、符合真实世界分布的多视角观测，这是 Director3D 区别于物体级方法的根本原因。

---

### 4.3 Decorator：Gaussian-driven Multi-view Latent Diffusion Model (GM-LDM)

**瓶颈**：直接对密集视图进行全序列扩散计算成本过高，且难以保证多视角一致性。

**核心设计**：GM-LDM 从 Traj-DiT 生成的密集轨迹中选取稀疏子集 $\boldsymbol{c} \subset \mathcal{C}$，在潜在空间中进行多视角图像序列扩散，同时通过渲染驱动的去噪生成像素对齐的 3D 高斯作为中间表示。该模型从 2D LDM 微调而来，仅增加少量修改（Figure 5 左）。

**两阶段训练损失**：

**(1) 多视角潜在扩散损失**（2D 监督）：

$$\mathcal{L}_{2\mathrm{d}} = \mathbb{E}_{\boldsymbol{\mathcal{X}}, \boldsymbol{c}, \boldsymbol{y}, \boldsymbol{\epsilon}, t} \Big[ \| \mathcal{Z} - \hat{\mathcal{Z}} \|_2^2 \Big] \tag{6}$$

其中 $\mathcal{Z}$ 为多视角真实图像的潜在编码，$\hat{\mathcal{Z}}$ 为模型预测的去噪潜在编码。

**(2) 渲染驱动去噪损失**（3D 监督）：

$$\mathcal{L}_{3\mathrm{d}} = \mathbb{E}_{x, c, y, \epsilon, t} \Big[ \ell(x, \mathcal{R}(\mathcal{G}, c)) \Big] \tag{7}$$

其中 $\mathcal{G}$ 为 3D 高斯场，$\mathcal{R}(\mathcal{G}, c)$ 为在相机 $c$ 下渲染的图像，$x$ 为对应真实图像，$\ell$ 为重建损失。该损失将去噪后的潜在表示解码为图像，并与高斯渲染结果对齐，从而将 2D 扩散先验转化为 3D 高斯参数。

**因果机制**：GM-LDM 的核心创新在于将“先扩散后重建”的两阶段流程压缩为端到端的渲染驱动去噪，使初始 3D 高斯天然具备像素对齐特性，避免了传统方法中 2D 生成与 3D 重建之间的域间隙。

---

### 4.4 Detailer：SDS++ Loss

**瓶颈**：标准 SDS 损失（**DreamFusion**, Poole et al., ICLR 2023）使用固定的无条件噪声预测作为源分布估计，导致生成结果过平滑；且仅在潜在空间计算损失，缺少对高频细节的约束。

**核心设计**：SDS++ 引入三个关键改进：

**(1) 联合潜在空间与图像空间目标**：

$$\mathcal{L}_{\mathrm{SDS++}} = \mathbb{E}_{t,c,\epsilon} \left[ w(t) \frac{\sqrt{\bar{\alpha}_t}}{\sqrt{1-\bar{\alpha}_t}} \left( \lambda_z \|z - \hat{z}\|_2^2 + \lambda_x \|x - \hat{x}\|_2^2 \right) \right] \tag{9}$$

其中 $z$ 为渲染图像的潜在编码，$\hat{z}$ 为目标潜在编码；$x$ 为渲染图像，$\hat{x}$ 为目标图像。$\lambda_z$ 控制潜在空间损失权重（设为 1），$\lambda_x$ 控制图像空间损失权重（设为 0.01）。潜在空间损失保证语义一致性，图像空间损失补充高频细节。

**(2) 自适应源预测**（Learnable Source Prediction）：

$$\hat{\epsilon}_{\mathrm{src}} = \epsilon_{\theta}(z_t, \hat{y}, t) \tag{11}$$

其中 $\hat{y}$ 为可学习的文本嵌入，在精炼过程中优化以匹配当前 3D 场景的分布。这替代了标准 SDS 中固定的无条件预测 $\epsilon_{\theta}(z_t, t)$，使源分布估计能自适应地逼近当前生成结果，避免过平滑。

**(3) 分类器自由引导目标预测**：

$$\hat{\epsilon}_{\mathrm{trg}} = \omega_{\mathrm{cfg}} \cdot ( \epsilon_{\theta}(z_t, y, t) - \epsilon_{\theta}(z_t, \phi, t) ) + \epsilon_{\theta}(z_t, \phi, t) \tag{12}$$

其中 $\omega_{\mathrm{cfg}}$ 为引导强度（设为 7.5），$y$ 为文本条件，$\phi$ 为空文本嵌入。该公式通过外推有条件与无条件预测的差异，增强文本对齐度。

**消融验证**（Figure 8, Section 5.5）：
- 去除精炼过程 → 细节显著缺失
- 将 $\hat{\epsilon}_{\mathrm{src}}$ 替换为固定无条件预测 $\epsilon$（退化为 SDS+）→ 过平滑
- 将 $\omega_{\mathrm{cfg}}$ 设为 1（退化为 LODS）→ 噪声细节
- 仅使用潜在空间损失 → 噪声与伪影
- 仅使用图像空间损失 → 细节缺失

这些消融实验（置信度 0.95）证实了 SDS++ 各组件对生成质量均有独立且不可替代的贡献。

### 补充图表

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2406_17601/figures/005_Figure_5.jpg]]
*Figure 5: Left: Architecture of GM-LDM. The model is fine-tuned from a 2D LDM with minor modifications, performing rendering-based denoising for generating initial 3D Gaussians. Right: Pipeline of calculating SDS++ loss, which refines the 3D Gaussians with the original 2D LDM*

## 实验与分析

### 主实验结果

Director3D 在 T3Bench 基准上的定量评估结果如 Table 1 所示。该方法在三个核心指标上均显著优于现有基线方法：

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2406_17601/figures/008_Table_1.jpg]]
*Table 1: Quantitative comparison of different models with text prompts in T3Bench*

- **BRISQUE ↓**：32.3，相比 ProlificDreamer（61.5）降低 29.2，表明生成图像的感知质量更接近自然图像。
- **NIQE ↓**：4.35，相比 ProlificDreamer（7.07）降低 2.72，表明图像的自然度显著提升。
- **CLIP-Score ↑**：85.5，相比 ProlificDreamer（69.4）提升 16.1，表明生成内容与文本描述的对齐度更高。

这些结果表明，Director3D 通过联合建模相机轨迹与图像序列分布，有效解决了真实世界文本到3D场景生成中的关键瓶颈。对于不具备自适应相机轨迹的基线方法（如 DreamFusion、Magic3D 等），评估时采用固定仰角环绕3D表示渲染视频的方式，保证了比较的公平性。

定性对比（Figure 7）进一步验证了上述结论。与 **GRM**（Xu et al., arXiv 2024）、**GaussianDreamer**（Yi et al., CVPR 2024）、DreamScene 和 LucidDreamer 等基线方法相比，Director3D 生成的场景在光影一致性、材质真实感和背景连贯性方面均表现出明显优势。

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2406_17601/figures/007_Figure_7.jpg]]
*Figure 7: Qualitative comparison between Director3D and different baselines*

### 消融实验

消融实验围绕 SDS++ 损失的精炼过程展开（Figure 8, Section 5.5），揭示了各组件的因果作用：

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2406_17601/figures/009_Figure_8.jpg]]
*Figure 8: Ablation of SDS++ loss*

- **去除精炼过程**：直接使用 GM-LDM 生成的初始 3D 高斯场景（“Ours w/o refining”）导致视觉质量显著下降，细节缺失。定量上，BRISQUE 升至 37.1，NIQE 升至 6.41，CLIP-Score 降至 80.0（Table 1），验证了 Detailer 阶段对最终质量的关键贡献。
- **去除自适应源预测**：将 $\hat{\epsilon}_{\mathrm{src}}$ 替换为无条件噪声预测 $\epsilon$ 会使 SDS++ 退化为 SDS+，导致生成结果出现过平滑现象，证明可学习文本嵌入 $\hat{y}$ 对准确估计当前分布至关重要。
- **去除分类器自由引导**：将 $\omega_{\mathrm{cfg}}$ 设为 1 会使 SDS++ 退化为 LODS，导致噪声细节增加，验证了分类器自由引导在提升文本对齐度方面的作用。
- **损失空间消融**：仅使用潜在空间损失（$\lambda_x = 0$）会导致噪声与伪影，仅使用图像空间损失（$\lambda_z = 0$）会导致细节缺失，证明双空间联合监督的必要性。

### 相机轨迹消融

使用随机生成相机轨迹替代 Traj-DiT 生成的场景特定轨迹时，生成结果的视角选择不佳或场景范围受限（Figure 12, Appendix E），直接证明了自适应轨迹生成模块对最终3D场景质量的决定性影响。

### 失败模式与局限性

尽管 Director3D 在整体指标上表现优异，仍存在以下已知局限：

- **视角范围受限**：GM-LDM 支持的多视角范围有限，制约了生成 3D 场景的视角广度。
- **效率瓶颈**：为达到开放世界泛化能力，需要额外的 SDS++ 精炼过程（1000 次迭代），降低了框架的整体效率。引入更广泛的多视角数据集可能缓解此问题。
- **复杂提示处理**：对于组合式、长文本描述或涉及精确数量、铰接物体的提示，生成成功率下降，表明模型在细粒度语义理解方面仍有提升空间。

### 补充图表

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2406_17601/figures/002_Figure_2.jpg]]
*Figure 2: Multi-view image results rendered with the generated camera trajectories and 3D scenes*

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2406_17601/figures/006_Figure.jpg]]

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2406_17601/figures/010_Figure_9.jpg]]
*Figure 9: Generation results with diversity*

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2406_17601/figures/011_Figure_11.jpg]]
*Figure 11: More multi-view image results*

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2406_17601/figures/012_Figure.jpg]]
*Figure: A blue and white china cup on a saucer*

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2406_17601/figures/003_Figure_3.jpg]]
*Figure 3: Left: Comparison of the simplified camera trajectory distributions between synthetic and real-world multi-view datasets. Right: Pipeline and models of Director3D*

## 方法谱系与知识库定位

### 核心瓶颈与设计动机

现有文本到3D生成方法的根本瓶颈在于：它们主要针对物体级别设计，依赖预定义或用户指定的固定相机轨迹（如环绕物体的圆周轨迹），难以有效利用真实世界多视角捕获数据中复杂的场景特定相机轨迹和无界背景。这导致生成质量受限，且缺乏对真实世界场景的通用性。Director3D 的核心洞察是将真实世界多视角数据建模为相机轨迹与图像序列的联合分布 $p((\mathcal{X}, \mathcal{C}) | y)$，并采用分治策略：分别用轨迹扩散Transformer、高斯驱动的多视角潜在扩散模型和 SDS++ 损失处理三个子问题，从而突破上述瓶颈。

### 与基线方法的关系

Director3D 与现有文本到3D生成方法在三个关键维度上存在根本差异：

**1. 相机轨迹建模方式**

- **DreamFusion** (Poole et al., ICLR 2023)、**SJC** (Wang et al., 2023)、**ProlificDreamer** (Wang et al., 2023) 等方法依赖预定义的固定相机轨迹，在优化过程中无法自适应调整视角分布。
- **Director3D** 通过 Traj-DiT 从文本直接生成密集的、场景特定的自适应相机轨迹，使生成结果在视角选择和空间覆盖上更符合真实世界场景分布。消融实验（Figure 12, Appendix E）表明，使用随机生成轨迹会导致视角不佳或范围受限，验证了场景特定轨迹的关键作用。

**2. 3D表示生成方式**

- **GRM** (Xu et al., arXiv 2024) 和 **GaussianDreamer** (Yi et al., CVPR 2024) 采用前馈式或结合2D/3D扩散的方式生成3D高斯，但缺乏对像素对齐和无界场景的针对性设计。
- **Director3D** 的 GM-LDM 通过高斯驱动的渲染降噪，直接生成像素对齐的3D高斯作为中间表示，在生成质量上显著优于上述方法。定性对比（Figure 7）显示，Director3D 生成的场景在光影、材质和背景一致性上均优于 GRM 和 GaussianDreamer。

**3. 精炼损失设计**

- 标准 SDS 损失及其变体（如 **Magic3D** (Lin et al., CVPR 2023)、**Fantasia3D** (Chen et al., ICCV 2023) 中使用的损失）缺乏对当前分布的自适应估计，容易导致过平滑或细节缺失。
- Director3D 提出的 SDS++ 损失通过引入可学习的自适应源预测 $\hat{\epsilon}_{\mathrm{src}} = \epsilon_{\theta}(z_t, \hat{y}, t)$ 和潜在/图像空间联合目标，在保持细节的同时提升文本对齐度。消融实验（Figure 8, Section 5.5）证实：去除自适应源预测会导致过平滑，仅使用图像空间损失会导致细节缺失，验证了各组件的必要性。

**4. 场景级生成方法的对比**

- **DreamScene** 和 **LucidDreamer** (Chung et al., 2023) 同样面向场景级文本到3D生成，但分别依赖2D基础模型或缺乏对相机轨迹的显式建模。Director3D 在 T3Bench 上的定量结果（Table 1）显示，其 BRISQUE 32.3、NIQE 4.35、CLIP-Score 85.5 显著优于 ProlificDreamer 的 61.5/7.07/69.4，间接表明其在场景级生成上的优势。

### 适用边界与局限

**1. 视角范围受限**

GM-LDM 支持的视角范围有限，这直接限制了生成3D场景的视角广度。对于需要全向自由视角的应用场景，该方法可能无法完全满足需求。

**2. 效率瓶颈**

为达到开放世界泛化，Director3D 需要额外的精炼过程（1000次迭代），降低了框架的整体效率。论文指出，通过引入更广泛的多视角数据集可能缓解这一问题，但当前版本仍存在此局限。

**3. 复杂语义处理能力下降**

对于复杂的组合式提示、精确数量描述或包含铰接物体的场景，生成成功率下降。这表明模型在细粒度语义理解和组合泛化方面仍有不足。

**4. 数据集依赖**

方法的效果依赖于真实世界多视角数据集的质量和多样性。当前多视角数据集的规模和多样性有限，制约了模型的泛化能力。

### 开放问题

1. **联合分布建模**：如何直接建模相机轨迹和图像序列的联合分布，而非当前的分治策略？这有望进一步提升生成一致性。

2. **消除精炼器依赖**：如何克服多视角数据集多样性和数量有限的挑战，使 GM-LDM 直接生成高质量结果，从而消除对 SDS++ 精炼器的需求？

3. **复杂语义泛化**：该方法在更复杂、更长文本描述下的泛化能力如何？能否通过改进网络架构或训练策略提升对组合式提示的处理能力？

4. **效率与质量权衡**：能否通过改进网络架构（如更高效的注意力机制）或训练策略（如蒸馏、渐进式训练）进一步提升效率，同时保持或提升生成质量？

5. **场景交互与编辑**：当前方法生成静态场景，如何扩展到支持场景编辑、物体交互或动态场景生成？

### 知识库定位

Director3D 处于文本到3D生成、多视角扩散模型和3D高斯溅射三个领域的交叉点。其核心贡献在于：

- **方法层面**：首次将真实世界相机轨迹生成与3D场景生成统一在文本条件框架下，提出了 Cinematographer-Decorator-Detailer 三阶段流水线。
- **技术层面**：Traj-DiT 将扩散Transformer应用于相机轨迹建模，GM-LDM 实现了高斯驱动的多视角潜在扩散，SDS++ 损失创新性地结合了自适应源预测与双空间目标。
- **评估层面**：在 T3Bench 上建立了新的性能基准，为后续真实世界文本到3D场景生成研究提供了参考。

该方法可作为后续研究的基础框架，特别是在以下方向具有扩展潜力：(a) 引入更强的多视角先验以消除精炼步骤；(b) 扩展至动态场景或交互式生成；(c) 结合大规模预训练模型提升开放世界泛化能力。

## 原文 PDF

![[paperPDFs/NEURIPS_2024/Director3D_Real_world_Camera_Trajectory_and_3D_Scene_Generation_from_Text.pdf]]