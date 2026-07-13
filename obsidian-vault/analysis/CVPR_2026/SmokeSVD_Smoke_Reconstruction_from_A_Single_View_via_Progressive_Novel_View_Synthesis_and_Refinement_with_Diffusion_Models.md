---
title: "SmokeSVD: Smoke Reconstruction from A Single View via Progressive Novel View Synthesis and Refinement with Diffusion Models"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/SmokeSVD_Smoke_Reconstruction_from_A_Single_View_via_Progressive_Novel_View_Synthesis_and_Refinement_with_Diffusion_Models.pdf
project_link: null
code_link: null
aliases:
- SmokeSVD
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 物理引导的侧视图合成与渐进式新视图细化相结合，循环利用2D扩散合成与3D体积一致性，逐步缓解病态性。
primary_logic: 通过将扩散模型的生成能力与物理一致性优化相集成，首先合成时空一致的侧视图，然后渐进式地细化和扩展多视角，从粗到精重建密度与速度场，实现了效率与质量的双重提升。
claims:
- 提出基于扩散模型的物理引导侧视图合成器，显式融入速度场约束以生成时空一致的侧视图图像。
- 通过渐进式多阶段过程迭代细化新视角图像并重建三维密度场，逐步增加视角。
- 利用可微平流和NS方程估计精细的速度场和流入状态，支持重仿真。
- ScalarFlow 上 Input RMSE↓ / Input PSNR↑ / Side RMSE↓ / Time = 0.0127 / 38.0790 / 0.0853 / 15 mins
---

# SmokeSVD: Smoke Reconstruction from A Single View via Progressive Novel View Synthesis and Refinement with Diffusion Models

> [!tip] 核心洞察
> 通过将扩散模型的生成能力与物理一致性优化相集成，首先合成时空一致的侧视图，然后渐进式地细化和扩展多视角，从粗到精重建密度与速度场，实现了效率与质量的双重提升。

| 字段 | 内容 |
|------|------|
| 中文题名 | SmokeSVD：基于渐进式新视图合成与扩散模型细化的单视图烟雾重建 |
| 英文题名 | SmokeSVD: Smoke Reconstruction from A Single View via Progressive Novel View Synthesis and Refinement with Diffusion Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2507.12156) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | SmokeSVD |
| Dataset | ScalarFlow, Synthetic Dataset |

> [!tip] 效果简介
> - ScalarFlow 上，Input RMSE↓ / Input PSNR↑ / Side RMSE↓ / Time 0.0127 / 38.0790 / 0.0853 / 15 mins vs GlobTrans: 0.0101 / 40.1560 / 0.0352 / >30h (感知质量与GlobTrans可比，计算速度提升120倍以上)。
> - ScalarFlow (vs FluidNexus) 上，Input RMSE↓ / Novel RMSE↓ 0.0172 / 0.0690 vs FluidNexus (最佳阈值): 0.0303 / 0.0565 (输入视图误差显著更低，新视角略低但无需依赖后处理阈值，鲁棒性更强)。
> - Synthetic Dataset 上，Input RMSE↓ / Input PSNR↑ 0.0395 / 28.1332 vs NGT: 0.1844 / 15.6521 (所有指标大幅超越其他方法，尤其在输入视图中保持高保真度)。

## 概要

从单视图视频重建动态三维烟雾是一项高度病态的任务：单一视角天然缺乏多视图一致性，导致密度场的形状与外观存在严重歧义，且现有方法（如基于物理优化的 **GlobTrans**（Franz et al., CVPR 2021）或端到端生成方法 **NGT**（Franz et al., 2023））要么计算极其耗时（>30小时），要么在新视角下保真度不足。本文提出的 **SmokeSVD** 通过将扩散模型的生成能力与物理一致性优化相集成，从根本上缓解了这一病态性。

其核心思路是**渐进式地合成并细化多视角图像**：首先利用一个物理引导的扩散模型（SvDiff）从单前视图生成时空一致的侧视图序列，显式融入速度场约束以保证烟雾运动的物理合理性；随后，通过一个渐进式新视图细化模块（NvRef），以粗密度场为起点，从近视角到远视角逐步渲染并增强新视图图像，最终在粗到细的密度生成器配合下重建出完整的三维密度场与速度场。

在 ScalarFlow 基准上，SmokeSVD 以约 15 分钟的计算时间取得了与 GlobTrans（>30小时）可比的感知质量，速度提升超过 120 倍；输入视图 RMSE 为 0.0127，PSNR 达 38.08 dB。相较于依赖后处理阈值的多视图扩散方法 **FluidNexus**，SmokeSVD 在输入视图误差上显著更低（RMSE 0.0172 vs. 0.0303），且无需阈值调参，鲁棒性更强。在合成数据集上，所有指标均大幅超越 NGT 等基线。消融实验证实，移除速度约束或空间约束会损害侧视图质量并导致速度场发散，而去除渐进式细化则使新视角明显模糊。该方法还支持重仿真、艺术家驱动控制等下游应用，展现出从单视图输入到灵活三维操作的一体化能力。



从单视图视频重建动态三维流体——尤其是烟雾——是计算机视觉与图形学中长期存在的病态问题。烟雾缺乏明确的几何表面，其半透明、非刚体、快速演化的特性使得仅凭一个视角的观测难以唯一确定其三维密度分布与运动状态。这种形状-外观歧义构成了根本性瓶颈：同一组二维投影可能对应截然不同的三维体积，而现有方法的计算效率与重建质量之间始终存在难以调和的矛盾。

**现有方法缺口。** 当前主流路线可大致分为两类。一类是基于物理与可微渲染的优化方法，如 **GlobTrans**（Franz et al., CVPR 2021），它们通过迭代优化三维密度场与速度场来匹配输入视图，能够获得较高的物理保真度，但单场景优化耗时超过30小时，完全不具备实时或交互式应用的可行性。另一类是端到端的快速生成方法，如 **NGT**（Franz et al., 2023），它们利用神经网络直接从单视图推断三维场，速度大幅提升，但缺乏显式的多视角一致性保障，生成结果在非输入视角往往出现形状失真或运动不连贯。基于神经特征轨迹场的 **PICT**（Wang et al., SIGGRAPH 2024）和物理信息神经场 **PINF**（Chu et al., 2022）等方法虽在特定场景下有所改进，但依然受制于稀疏视角下的信息不足。多视图扩散合成方法如 **FluidNexus** 尝试从单视图生成多视角图像再进行重建，却面临后处理阈值敏感、输入视图保真度不足的问题。

**核心动机。** 本文的出发点是：能否将扩散模型的强大生成能力与物理一致性优化有机融合，从而在计算效率与重建质量之间取得突破？直觉上，扩散模型擅长从稀疏条件中生成逼真的图像，但其原生缺乏对三维物理规律的感知；而 Navier-Stokes 方程提供了流体运动的严格约束，却需要足够的多视角信息才能有效施加。因此，关键挑战在于设计一种机制，让二者循环互补——用物理约束引导扩散合成，再用合成结果扩充视角以强化物理重建，形成从粗到精的渐进式闭环。

**本文方法定位。** SmokeSVD 提出了一条“先合成侧视图，再渐进细化多视角，最后联合重建密度与速度场”的技术路线。具体而言，首先通过物理引导的侧视图合成器 SvDiff，在扩散去噪过程中显式融入速度场约束，逐帧生成时空一致的侧视图序列；随后，利用粗粒度密度生成器从已有视角重建初始三维场，并通过渐进式新视图细化模块 NvRef 从近视角到远视角逐步渲染和增强图像，扩充有效观测；最终，在细粒度密度生成与速度场估计阶段，借助可微平流和 Navier-Stokes 方程约束，恢复出可用于重仿真的完整三维烟雾场。这一设计使得 SmokeSVD 在 ScalarFlow 数据集上以约15分钟的重建时间，达到了与优化方法可比拟的输入视图保真度（PSNR 38.079 dB），计算速度提升超过120倍。



## 核心方法与创新机理

### 1. 物理引导的侧视图扩散合成器（SvDiff）

传统单视图重建方法（如 **GlobTrans** (Franz et al., CVPR 2021) 和 **NGT** (Franz et al., 2023)）要么依赖耗时的逐场景优化，要么直接从单视角端到端生成，缺乏对时空一致性的显式保障。SmokeSVD 的核心突破在于提出 **SvDiff**——一个嵌入物理约束的扩散模型，专门用于从单帧前视图逐帧合成时空一致的侧视图序列。

**创新机制：**
- **条件设计**：SvDiff 将当前前视图 $w_{\angle 0^{\circ}}^{t}$ 与前两帧已生成的侧视图 $w_{\angle 90^{\circ}}^{t-1}$、$w_{\angle 90^{\circ}}^{t-2}$ 拼接作为条件 $c^{t}$（Eq. 1），使模型显式感知时序演化。
- **物理引导**：在标准噪声预测损失 $\mathcal{L}_{noise}$（Eq. 2）之外，引入速度场约束 $\mathcal{L}_{vel}$（Eq. 4）——同时惩罚速度散度（不可压缩性）和梯度（光滑性），以及空间分布约束 $\mathcal{L}_{sp}$（Eq. 5）——强制侧视图的行方向密度分布与前视图匹配。
- **多帧训练策略**：通过循环利用历史生成图像与重建密度场的渲染图像进行训练（Figure 3），有效抑制了逐帧生成中的累积误差。消融实验证实，多帧方案（F4）在侧视图合成中达到最佳长期稳定性（Table 3，附录）。

**关键价值**：SvDiff 将扩散模型的强大生成能力与流体力学先验深度融合，使得侧视图合成不再是一个“盲生成”过程，而是受物理规律约束的推理过程，从根本上缓解了单视图重建中的形状-外观歧义。

### 2. 渐进式新视图细化模块（NvRef）

现有方法（如 **FluidNexus**、**PICT** (Wang et al., SIGGRAPH 2024)）在多视图生成后通常不进行细化，或仅做单阶段全局优化，导致新视角图像模糊且缺乏细节。SmokeSVD 提出 **NvRef**——一个基于 UNet3+ 的残差预测模块，采用从近到远的渐进式细化策略。

**创新机制：**
- **渐进式视角扩展**：从清晰视角出发，逐步旋转相机，依次渲染并细化近（near）、中（mid）、远（far）视角图像（Figure 4）。这种由易到难的策略使模型能够逐步积累多视角一致性信息。
- **残差学习**：NvRef 以粗密度场渲染的图像为输入，预测残差图以增强细节。损失函数（Eq. 10）融合了 L2、L1、残差均值惩罚、空间分布约束和 PSNR 差异，全方位约束细化质量。
- **与密度生成器协同**：NvRef 与粗/细密度生成器（$G_{\rho}^{c}$ / $G_{\rho}^{f}$）形成闭环——细化后的图像反过来提升密度重建精度，密度场再渲染出更准确的新视角图像。

**关键价值**：消融实验（Table 6, Figure 12）表明，移除 NvRef 或改用非渐进式方案会导致新视角图像明显模糊，验证了渐进式细化对视图一致性和细节恢复的决定性作用。

### 3. 粗到细密度重建与物理一致性闭环

不同于 **PINF** (Chu et al., 2022) 等直接拟合密度场的方法，SmokeSVD 构建了一个粗到细的密度生成管线，并与速度场估计、流入推断形成物理一致性闭环。

**创新机制：**
- **两级密度生成**：粗密度生成器 $G_{\rho}^{c}$ 从稀疏视角快速重建大致形态，细密度生成器 $G_{\rho}^{f}$ 利用 NvRef 增强后的多视角图像进一步提升精度。
- **联合物理推断**：基于重建密度场，利用可微平流和 Navier-Stokes 方程估计精细速度场（$G_u$）和动态流入状态，使重建结果支持重仿真（re-simulation）和艺术控制等下游应用（Figure 1）。
- **端到端效率**：整个管线在单张 RTX 2080 Ti 上仅需约 15 分钟，相比 **GlobTrans** 的 >30 小时优化过程，速度提升超过 120 倍（Table 1），同时保持可比的感知质量。

### 4. 方法对比总结

| 创新维度 | 基线方法 | SmokeSVD 方案 | 核心优势 |
|---------|---------|--------------|---------|
| 2D 生成方式 | 直接生成多视图，缺乏一致性保障 | SvDiff 物理引导合成，多帧训练 | 时空一致性，物理合理性 |
| 多视图细化 | 单阶段全局或不细化 | NvRef 渐进式残差细化 | 细节增强，视图一致性 |
| 3D 重建流程 | 直接重建或单一密度生成 | 粗到细密度生成 + 速度/流入联合推断 | 精度与物理可解释性 |

这些创新共同构成了一个从“生成-细化-重建-验证”的闭环系统，使得单视图烟雾重建从严重病态问题转变为可工程化解决的任务。



SmokeSVD 旨在从单视图视频序列重建动态三维烟雾的密度场与速度场。其核心挑战在于：单视图输入天然缺失多视角信息，导致重建问题高度病态。为缓解这一歧义，SmokeSVD 构建了一个“合成—细化—重建”三阶段渐进式管线，将二维扩散模型的生成能力与三维物理一致性约束深度耦合。

### 管线总览

整体管线如 Figure 2 所示，按视角类型将图像分为三类：输入的前视图（$\alpha = \angle 0^\circ$）、由 SvDiff 合成的侧视图（$\alpha = \angle 90^\circ$），以及其余所有新视角。管线以逐帧方式运行，每一帧经历以下阶段：

![[assets/figures/papers/paper_list_l2040_https_arxiv_org_abs_2507_12156/figures/002_Figure_2.jpg]]
*Figure 2: Overview of SmokeSVD. We categorize view angles into three types: input as front view*

1. **物理引导侧视图合成**：给定当前帧前视图 $w_{\angle 0^\circ}^{t}$ 及历史侧视图，**SvDiff**（物理引导的侧视图合成器）生成时空一致的侧视图 $w_{p,\angle 90^\circ}^{t}$。该模块以扩散模型为基础，在去噪过程中显式融入速度场约束（不可压缩性与光滑性）和空间分布约束，确保合成侧视图在运动规律和空间结构上与前视图保持一致。

2. **粗密度场重建**：利用已有的前视图和合成侧视图，**粗粒度密度生成器 $G_\rho^c$** 重建当前帧的三维密度场。该生成器以多视角图像为输入，通过可微渲染损失和直接密度差损失进行监督。

3. **渐进式新视图细化**：以粗密度场为起点，**NvRef**（新视图细化模块）沿水平面逐步旋转相机，从近视角到中视角再到远视角，逐层渲染并增强新视角图像。该模块采用 UNet3+ 架构预测残差，结合 L2、L1、残差均值、空间分布及 PSNR 差异等多重损失，在扩展视角覆盖的同时持续提升图像质量。

4. **细密度场与速度场重建**：随着可用视角数量增加，**细粒度密度生成器 $G_\rho^f$** 重建更高精度的密度场。随后，**速度场生成器 $G_u$** 基于细密度场序列估计速度场，并通过 NS 方程推断动态流入状态。最终输出支持重仿真、新视角生成及艺术化控制等下游应用（Figure 1）。

### 关键设计逻辑

管线的核心设计遵循“由粗到精、逐步解耦”的原则：先利用扩散模型的生成先验填补信息缺口（侧视图合成），再通过多视角一致性优化消除剩余歧义（渐进式细化），最后以物理方程约束确保重建结果的运动合理性（速度场估计与流入推断）。这种分阶段策略使得每一阶段只需处理相对可控的子问题，从而在 15 分钟内完成单视图重建，速度较传统优化方法（如 **GlobTrans**，Franz et al., CVPR 2021，耗时 >30h）提升 120 倍以上，同时保持可比的感知质量。



SmokeSVD 的核心管线由三个紧密耦合的模块构成：物理引导的侧视图合成器 **SvDiff**、渐进式新视图细化模块 **NvRef**，以及粗到细的 **3D 密度与速度场重建**。三者形成循环迭代——SvDiff 生成侧视图，密度生成器从多视图重建体积，速度场与流入估计施加物理约束，反馈至下一帧的侧视图合成条件中。

### SvDiff：物理引导的侧视图合成器

SvDiff 将标准图像扩散模型扩展至烟雾序列的逐帧生成。其核心设计在于**条件构造**与**物理约束注入**。

**条件构造**：在第 $t$ 帧，去噪网络的条件 $c^{t}$ 由当前前视图与历史侧视图拼接而成：

$$c^{t} = w_{\angle 0^{\circ}}^{t} \oplus w_{\angle 90^{\circ}}^{t-1} \oplus w_{\angle 90^{\circ}}^{t-2}$$

其中 $w_{\angle 0^{\circ}}^{t}$ 为当前前视图，$w_{\angle 90^{\circ}}^{t-1}$、$w_{\angle 90^{\circ}}^{t-2}$ 为前两帧生成的侧视图。这一设计为模型提供了时序运动线索，是多帧训练策略（F4 方案在消融中表现最优）的基础。

**标准扩散损失**：

$$\mathcal{L}_{noise} = \| \epsilon - \epsilon_{\theta}(w_{\angle 90^{\circ}}^{t}, c^{t}, s) \|^{2}$$

其中 $\epsilon$ 为真实噪声，$\epsilon_{\theta}$ 为网络预测，$s$ 为扩散时间步。

**物理约束**：为保证生成的侧视图在物理上合理，引入两类显式约束：

1. **速度场约束** $\mathcal{L}_{vel}$：对从生成图像估计的速度场 $\mathbf{u}^{i-1}$ 施加不可压缩性（散度最小化）与光滑性（梯度最小化）：

$$\mathcal{L}_{vel} = \Vert \nabla \cdot \mathbf{u}^{i-1} \Vert^{2} + \Vert \nabla \mathbf{u}^{i-1} \Vert^{2}$$

2. **空间分布约束** $\mathcal{L}_{sp}$：强制侧视图的行方向密度分布与前视图一致，缓解单视图固有的形状歧义：

$$\mathcal{L}_{sp} = \| H(w_{c,\angle 90^{\circ}}) - H(w_{\angle 0^{\circ}}) \|^{2}$$

其中 $H(\cdot)$ 表示沿行方向求和操作。消融实验证实，移除速度约束会导致速度场发散、运动不连贯，移除空间约束则损害侧视图的形态合理性。

### 密度生成器：粗到细的 3D 重建

从 SvDiff 合成的侧视图与输入前视图出发，训练两个密度生成器 $\mathcal{G}_{\rho}^{c}$（粗）和 $\mathcal{G}_{\rho}^{f}$（细），将 2D 图像序列映射为 3D 密度场 $\rho^{t}$。其损失函数同时约束直接密度差与多视角渲染差：

$$\mathcal{L}_{\mathcal{G}_\rho} = \lambda_\rho\|\rho_r^t - \rho^t\|^2 + \lambda_{in}\sum_{\alpha\in\mathbb{A}}\|\mathcal{R}(\rho_r^t,\alpha) - \mathcal{R}(\rho^t,\alpha)\|^2 + \lambda_{un}\sum_{\alpha\notin\mathbb{A}}\|\mathcal{R}(\rho_r^t,\alpha) - \mathcal{R}(\rho^t,\alpha)\|^2$$

其中 $\mathcal{R}(\cdot, \alpha)$ 为视角 $\alpha$ 的可微渲染算子，$\mathbb{A}$ 为已有视角集合。第一项直接监督密度值，后两项分别约束已有视角和新视角的渲染一致性——这正是渐进式细化策略的数学基础。

### NvRef：渐进式新视图细化

NvRef 以粗密度场渲染的新视角图像和 UNet3+ 架构预测残差，从近视角到远视角逐步增强。其优化目标融合了五项损失：

$$\mathcal{L}_{NvRef} = \lambda_{mse}\|w_{f,\mathcal{L}\alpha}^t - w_{\mathcal{L}\alpha}^t\|^2 + \lambda_{l1}\|w_{f,\mathcal{L}\alpha}^t - w_{\mathcal{L}\alpha}^t\| + \lambda_{res}\|Mean(res_\alpha^t)\|^2 + \lambda_{sp}\|H(w_{f,\mathcal{L}\alpha}^t) - H(w_{\mathcal{L}\alpha}^t)\|^2 + \lambda_{psnr}\|PSNR(w_{f,\mathcal{L}\alpha}^t) - PSNR(w_{\mathcal{L}\alpha}^t)\|^2$$

其中 $w_{\mathcal{L}\alpha}^t$ 为粗渲染图像，$w_{f,\mathcal{L}\alpha}^t$ 为细化后图像，$res_\alpha^t$ 为 UNet3+ 预测的残差图。五项损失分别约束像素级 L2/L1 误差、残差幅度、空间分布一致性及感知质量（PSNR），形成对细化过程的多层次监督。消融实验表明，去除 NvRef 会导致新视角图像模糊、细节丢失。

### 速度场估计与物理闭环

在获得细粒度密度场后，速度场生成器 $\mathcal{G}_u$ 结合可微平流与 Navier-Stokes 方程估计速度场 $\mathbf{u}$ 和流入状态，使重建结果支持重仿真。这一物理闭环将 2D 扩散生成与 3D 流体动力学统一在可微框架内，是 SmokeSVD 实现“效率-质量”双重提升的关键机制。

### 补充图表

![[assets/figures/papers/paper_list_l2040_https_arxiv_org_abs_2507_12156/figures/003_Figure_3.jpg]]
*Figure 3: Frame-by-frame training of the side-view synthesizer via feature fusion of adjacent frames. In the forward diffusion process, a clean image*

![[assets/figures/papers/paper_list_l2040_https_arxiv_org_abs_2507_12156/figures/004_Figure_4.jpg]]
*Figure 4: The progressive scheme for novel view refinement begins with clear views and incrementally rotates the camera to render and refine novel-view images from near, mid, and far views*



## 实验与关键发现

### 主实验结果

**ScalarFlow 数据集上的定量对比**（Table 1）展示了 SmokeSVD 在效率-质量权衡上的突破性优势。在输入视图（前视图）保真度上，SmokeSVD 取得了 Input RMSE 0.0127、PSNR 38.0790 dB、SSIM 0.9868，与基于物理优化的 **GlobTrans**（Franz et al., CVPR 2021）的 0.0101 / 40.1560 dB 接近，但计算时间从超过 30 小时缩短至约 15 分钟，速度提升超过 120 倍。在侧视图合成质量上，SmokeSVD 的 Side RMSE 为 0.0853，虽然高于 GlobTrans 的 0.0352，但显著优于其他快速方法。这一结果表明，物理引导的扩散合成与渐进式细化策略成功在计算效率与重建精度之间取得了实用化的平衡。

**与多视图扩散方法的对比**（Table 2）进一步揭示了 SmokeSVD 的鲁棒性优势。与 **FluidNexus** 相比，SmokeSVD 的 Input RMSE 为 0.0172，显著低于 FluidNexus 在最佳后处理阈值下的 0.0303；Novel RMSE 为 0.0690，略高于 FluidNexus 的 0.0565，但 SmokeSVD 无需依赖敏感的后处理阈值调优，在不同场景下表现更稳定。这验证了渐进式新视图细化模块 NvRef 通过多视图一致性约束有效缓解了单视图歧义性，且不引入额外的超参数依赖。

**合成数据集上的泛化验证**（Table 4）显示，SmokeSVD 在所有指标上大幅领先现有方法。Input RMSE 为 0.0395、PSNR 为 28.1332 dB，相比之下 **NGT**（Franz et al., 2023）分别为 0.1844 和 15.6521 dB。这一差距表明，端到端快速生成方法在缺乏物理约束和视图细化时难以保持输入视图的高保真度，而 SmokeSVD 的物理引导侧视图合成与粗到细密度生成管线在合成场景下同样有效。

**定性对比**（Figure 5, 6, 9）展示 SmokeSVD 在前视图上能准确匹配输入图像的外观模式，在侧视图上产生合理的烟雾形状和运动结构。与 NeuSmoke 的对比（Figure 8, Table 3）进一步证明，显式合成侧视图的渐进式细化策略比隐式神经渲染更能缓解单视图重建的病态性。

### 消融实验

**物理约束对侧视图合成的影响**（Table 5, Figure 13-15）表明，移除速度约束（$L_{vel}$）或空间分布约束（$L_{sp}$）会显著损害侧视图合成质量。具体而言，去除速度约束后，重建速度场的散度显著增大，导致运动不连贯和物理不合理；去除空间约束则使侧视图的烟雾分布偏离前视图的行方向统计特性。这验证了 $L_{vel}$ 中不可压缩性（散度项）和光滑性（梯度项）约束，以及 $L_{sp}$ 中行方向分布匹配对于生成时空一致侧视图的必要性。

**渐进式新视图细化的贡献**（Table 6, Figure 12, 16）显示，移除 NvRef 模块后，新视角图像变得模糊，细节显著丢失。渐进式策略（从近视图到远视图逐步旋转相机渲染细化）相比一次性全局细化，能够更有效地利用已细化视图的信息，逐步扩展视角覆盖范围。此外，残差损失项（$L_{res}$）的引入进一步提升了细化图像的清晰度。当将 NvRef 与 NGT 的生成结果结合时（Figure 16），也能观察到明显的质量提升，表明细化模块具有一定的通用性。

**多帧训练策略的效果**（Table 3 in Appendix）表明，采用 4 帧训练方案（F4）在侧视图合成中达到最佳性能，有效抑制了逐帧生成中的累积误差，确保了长期运动的稳定性。随着输入视图数量的增加，重建质量持续提升，16 个视图时 PSNR 可达 49.697 dB（Table 4 in Appendix, Figure 13），验证了多视图信息对缓解单视图病态性的正向作用。

### 泛化性与鲁棒性

在无入流烟雾场景（兔子形状，Figure 10）和水平羽流场景（Figure 11）上的测试表明，SmokeSVD 对不同类型的烟雾现象具有一定的泛化能力，能够重建出合理的密度分布和运动模式。这得益于物理约束（NS 方程、可微平流）的引入，使模型不局限于特定入流模式。

![[assets/figures/papers/paper_list_l2040_https_arxiv_org_abs_2507_12156/figures/017_Figure_10.jpg]]
*Figure 10: Reconstruction results for a bunny-shaped smoke scenario without inflow*

### 失败模式与局限性

尽管取得了显著进展，SmokeSVD 仍存在以下局限：

1. **背景与光照假设**：当前方法假设较为干净的背景和一致的照明条件，在复杂真实场景下侧视图合成质量可能下降。
2. **误差传播风险**：尽管采用渐进式优化，早期阶段侧视图合成的显著误差仍可能传播并影响最终重建结果。
3. **场景多样性有限**：目前仅在合成和受控真实数据集（ScalarFlow）上评估，对高度多样化或室外烟雾现象的泛化能力有待进一步验证。
4. **计算成本**：虽远低于优化方法（>30h vs 15min），但在更高分辨率或更长序列时计算成本仍可能显著。
5. **物理模型简化**：仅处理灰度烟雾，未明确处理彩色烟雾、固体障碍物或与复杂环境的交互。

这些局限性指向了未来工作的方向：融合垂直方向多视角、扩展至更复杂流体现象、以及在更低计算预算下实现与优化方法媲美的视觉质量。

### 补充图表

![[assets/figures/papers/paper_list_l2040_https_arxiv_org_abs_2507_12156/figures/010_Table_1.jpg]]
*Table 1: Quantitative comparison on ScalarFlow*

![[assets/figures/papers/paper_list_l2040_https_arxiv_org_abs_2507_12156/figures/005_Figure_5.jpg]]
*Figure 5: Qualitative comparison based on different methods on ScalarFlow. Our method matches the appearance pattern of the input image at the front view, and produces a reasonable shape in the side view*

![[assets/figures/papers/paper_list_l2040_https_arxiv_org_abs_2507_12156/figures/007_Table_2.jpg]]
*Table 2: Comparison with FluidNexus (various post-processing thresholds) on ScalarFlow. Averaged over five scenes, novel views from four non-frontal cameras*

![[assets/figures/papers/paper_list_l2040_https_arxiv_org_abs_2507_12156/figures/015_Table_4.jpg]]
*Table 4: Quantitative comparison on the synthetic dataset*

![[assets/figures/papers/paper_list_l2040_https_arxiv_org_abs_2507_12156/figures/014_Table_5.jpg]]
*Table 5: Ablation studies on SvDiff*

![[assets/figures/papers/paper_list_l2040_https_arxiv_org_abs_2507_12156/figures/020_Table_6.jpg]]
*Table 6: Ablation on novel view refinement. Views 0 (front) and 3 (side) as input, remaining views for evaluation*

![[assets/figures/papers/paper_list_l2040_https_arxiv_org_abs_2507_12156/figures/018_Figure_12.jpg]]
*Figure 12: Ablation on novel view refinement. From top to bottom: reference, results without refinement, without progressive refinement, without res loss and with NvRef. Red boxes show close-ups*

![[assets/figures/papers/paper_list_l2040_https_arxiv_org_abs_2507_12156/figures/019_Figure_13.jpg]]
*Figure 13: Comparison of the divergence of reconstructed velocity fields by SvDiff with different loss functions at various time steps*



## 定位与知识库关联

### 与现有方法的关系

SmokeSVD 处于单视图动态流体重建这一高度病态问题的交叉地带，其设计思路同时关联着三条技术路线：基于物理的优化方法、端到端生成方法、以及基于扩散模型的生成式重建方法。

**相对于基于物理的优化方法**，SmokeSVD 实现了计算效率的跨越式提升。**GlobTrans**（Franz et al., CVPR 2021）通过可微渲染和物理约束从单视图优化密度与速度场，在侧视图感知质量上达到当前最优（STYLE 0.2167），但单场景优化耗时超过 30 小时。SmokeSVD 将这一过程压缩至约 15 分钟（约 120 倍加速），同时在输入视图保真度上达到可比水平（Input PSNR 38.08 vs GlobTrans 40.16），代价是侧视图重建精度略有下降（Side RMSE 0.0853 vs 0.0352）。这一权衡的本质在于：SmokeSVD 用数据驱动的生成先验替代了逐场景的物理优化迭代，将计算负担从推理阶段转移至训练阶段。

**相对于端到端生成方法**，SmokeSVD 引入了显式的物理约束和多视图一致性机制。**NGT**（Franz et al., 2023）直接从前视图预测多视角图像，速度快但缺乏物理合理性保障，在合成数据集上 Input PSNR 仅 15.65。SmokeSVD 通过 SvDiff 中嵌入的速度场散度与梯度约束（Eq. 4），以及渐进式新视图细化模块 NvRef 的多视图一致性损失（Eq. 10），在保持生成效率的同时显著提升了物理合理性。消融实验证实，移除速度约束会导致重建速度场发散（Figure 13），而移除 NvRef 则使新视角图像趋于模糊（Figure 12）。

**相对于基于扩散模型的多视图生成方法**，SmokeSVD 的关键差异在于物理引导的渐进式策略。**FluidNexus** 直接利用 2D 扩散模型合成多视图图像，但需要依赖后处理阈值筛选有效帧，且输入视图误差较高（Input RMSE 0.0303）。SmokeSVD 的 SvDiff 将速度场约束融入去噪过程，从生成源头保障时空一致性，无需后处理即可获得更低的输入视图误差（Input RMSE 0.0172）。**PICT**（Wang et al., SIGGRAPH 2024）和 **PINF**（Chu et al., 2022）分别通过神经特征轨迹场和物理信息神经场处理稀疏视图重建，但均未显式处理单视图输入下的侧视图合成问题。

### 适用边界

SmokeSVD 的有效性建立在以下前提之上：

1. **输入假设**：假设背景相对干净、光照条件一致，且烟雾运动主要由水平方向的平流主导。当前设计仅合成水平 90° 侧视图，未利用垂直方向的多视角信息。
2. **数据分布**：在 ScalarFlow 数据集（受控实验室环境下的热羽流）和合成数据集上验证有效，对室外复杂场景、彩色烟雾或存在固体障碍物的情况泛化能力未经验证。
3. **重建范围**：仅处理灰度烟雾的密度与速度场重建，未涉及温度场、多相流或烟雾与环境的交互建模。
4. **计算资源**：虽然相比优化方法大幅提速，但在高分辨率或长序列场景下，扩散模型的逐帧推理和渐进式细化仍构成计算瓶颈。

### 局限与开放问题

**已知局限**（论文明确讨论或消融实验揭示）：

- **初始侧视图质量依赖**：渐进式细化策略虽然能缓解早期误差，但无法完全消除 SvDiff 初始合成错误的影响。当初始侧视图存在显著形变或运动不连贯时，后续的密度生成与 NvRef 细化均会受到污染。
- **长期稳定性**：尽管多帧训练方案（F4）在消融实验中表现最优，但长序列生成中的累积误差问题仍然存在。当前设计仅回溯两帧历史信息（Eq. 1），对更长程的时间依赖建模不足。
- **物理约束的充分性**：速度损失仅施加了不可压缩性和光滑性约束（Eq. 4），未显式建模 Navier-Stokes 方程中的对流项和压力项。可微平流（Eq. 13）虽然提供了物理一致性保障，但其精度受限于估计的速度场质量。

**开放问题**：

1. **多视角扩展**：当前仅利用水平 90° 侧视图，如何融合垂直方向或更多中间视角以进一步提高重建质量？消融实验显示，随着输入视图数量增加，重建质量持续提升（16 视图时 PSNR 达 49.697 dB），暗示多视角信息具有显著的边际收益。
2. **复杂流体现象**：如何将框架扩展到彩色烟雾、多相流或存在固体边界的场景？这需要重新设计密度场的表征方式和物理约束形式。
3. **计算效率的进一步优化**：能否在更低计算预算下（例如通过潜在空间扩散或蒸馏策略）实现与 GlobTrans 相当的侧视图感知质量？
4. **真实场景泛化**：如何将方法适配到野外视频中的烟雾现象？这需要解决背景分离、光照变化和相机运动等额外挑战。



## 原文 PDF

![[paperPDFs/CVPR_2026/SmokeSVD_Smoke_Reconstruction_from_A_Single_View_via_Progressive_Novel_View_Synthesis_and_Refinement_with_Diffusion_Models.pdf]]
