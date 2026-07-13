---
title: OccFusion Rendering Occluded Humans with Generative Diffusion Priors
type: paper
paper_level: A
venue: NEURIPS
year: 2024
pdf_ref: paperPDFs/NEURIPS_2024/OccFusion_Rendering_Occluded_Humans_with_Generative_Diffusion_Priors.pdf
project_link: "https://cs.stanford.edu/~xtiange/projects/occfusion/"
code_link: null
aliases:
- OROHGDP
tags:
- NEURIPS_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
core_operator: 通过三阶段流水线（掩码修复 → SDS正则化 → 上下文感知修复）将生成扩散先验（姿态条件的Stable Diffusion 1.5 + ControlNet）引入3D高斯散点表示，以补全被遮挡区域的几何与外观，同时保持多帧一致性。
primary_logic: 将遮挡人体重建解耦为几何补全与外观精炼：先利用扩散模型在二值掩码上的修复获得可靠几何监督；再对渲染的占用图施加SDS约束（姿态空间与规范姿态）强制人体完整性；最后通过上下文感知的图像修复改善未观测区域的细节，并结合对GauHuman的三项针对性改造（仅训练可见像素、加权掩码损失、禁用密集化/剪枝）提升遮挡下的鲁棒性。
claims:
- 在ZJU-MoCap模拟遮挡评测集上，OccFusion取得PSNR 23.96、SSIM 0.9548、LPIPS 32.34（×1000），显著优于所有基线，尤其在LPIPS指标上大幅领先。
- 逐模块消融实验（Table 2）证实：初始化阶段提升PSNR与SSIM；优化阶段SDS正则化移除伪影并增强完整性；精炼阶段使LPIPS从55.35骤降至32.34，同时PSNR提升至23.96。
- 在真实遮挡数据集OcMotion上，OccFusion在可见像素指标上超过专门为遮挡设计的NeRF方法（OccNeRF），PSNR提高2.57 dB，LPIPS降低0.48。
- 定性对比（Figure 5, 6, 7）显示，OccFusion是唯一能够持续生成锐利、无遮挡、完整人体的方法，而基线方法存在变色、漂浮物或模糊。
---

# OccFusion Rendering Occluded Humans with Generative Diffusion Priors

> [!tip] 核心洞察
> 将遮挡人体重建解耦为几何补全与外观精炼：先利用扩散模型在二值掩码上的修复获得可靠几何监督；再对渲染的占用图施加SDS约束（姿态空间与规范姿态）强制人体完整性；最后通过上下文感知的图像修复改善未观测区域的细节，并结合对GauHuman的三项针对性改造（仅训练可见像素、加权掩码损失、禁用密集化/剪枝）提升遮挡下的鲁棒性。

| 字段 | 内容 |
|------|------|
| 中文题名 | OccFusion：利用生成扩散先验渲染被遮挡人体 |
| 英文题名 | OccFusion Rendering Occluded Humans with Generative Diffusion Priors |
| 会议/期刊 | NEURIPS 2024 |
| Links | [paper](https://openreview.net/forum?id=CZwphz5vgz) · [Project](https://cs.stanford.edu/~xtiange/projects/occfusion/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation |
| Method | OccFusion |
| Dataset | ZJU-MoCap, OcMotion |

> [!tip] 效果简介
> - ZJU-MoCap 上，PSNR↑ 23.96 vs OccGaussian (23.29) (+0.67)；SSIM↑ 0.9548 vs OccGaussian (0.9482) (+0.0066)；LPIPS↓ (×1000) 32.34 vs OccGaussian (41.93) (-9.59)。
> - OcMotion 上，PSNR*↑ 18.28 vs OccNeRF (15.71) (+2.57)；SSIM*↑ 0.8875 vs OccNeRF (0.8523) (+0.0352)；LPIPS*↓ (×1000) 82.42 vs OccNeRF (82.90) (-0.48)。

## 概要

**核心问题**：现有单目视频人体渲染方法（如 HumanNeRF、3DGS-Avatar、GauHuman）假设人体各部位始终完全可见。在真实遮挡场景下，部分可见性导致几何不完整、伪影和缺失身体部位，传统方法难以有效处理。

**方法定位**：OccFusion 提出一种三阶段流水线，将 2D 生成扩散先验（姿态条件的 Stable Diffusion 1.5 + ControlNet）引入 3D 高斯散点表示，以补全被遮挡区域的几何与外观。其核心思路是将遮挡人体重建解耦为几何补全与外观精炼两个子问题：先利用扩散模型在二值掩码上的修复获得可靠几何监督，再对渲染的占用图施加 SDS 约束强制人体完整性，最后通过上下文感知的图像修复改善未观测区域的细节。同时，对基线 GauHuman 进行三项针对性改造（仅训练可见像素、加权掩码损失、禁用密集化/剪枝），提升遮挡下的鲁棒性。

**主要结果**：在 ZJU-MoCap 模拟遮挡评测集上，OccFusion 取得 PSNR 23.96、SSIM 0.9548、LPIPS 32.34（×1000），显著优于所有基线，尤其在 LPIPS 指标上大幅领先。在真实遮挡数据集 OcMotion 上，OccFusion 在可见像素指标上超过专门为遮挡设计的 NeRF 方法 OccNeRF，PSNR 提高 2.57 dB。逐模块消融实验证实：初始化阶段提升 PSNR 与 SSIM；优化阶段 SDS 正则化移除伪影并增强完整性；精炼阶段使 LPIPS 从 55.35 骤降至 32.34，是整个流程的关键环节。定性对比显示，OccFusion 是唯一能够持续生成锐利、无遮挡、完整人体的方法。训练仅需约 10 分钟（单 TITAN RTX GPU），远快于基于 NeRF 的方法。



### 问题背景

从单目视频中重建可自由视点渲染的数字化人体，是计算机视觉与图形学中的核心问题，在虚拟现实、远程呈现、电影制作等领域具有广泛应用。近年来，基于神经辐射场（NeRF）和 3D 高斯散点（3D Gaussian Splatting）的方法显著推进了这一方向，能够在数分钟甚至数秒内从人体视频中学习出高质量的可驱动化身。

然而，现有方法普遍依赖一个强假设：**人体各部位在所有训练帧中始终完全可见**。这一假设在真实场景中几乎无法满足——遮挡物（如桌椅、其他行人、前景物体）频繁出现，导致人体仅部分可见。当输入视频包含遮挡时，传统方法面临严峻挑战：

- **几何不完整**：被遮挡区域缺乏观测信号，3D 表示无法学习正确的几何结构，导致渲染结果中出现缺失的身体部位或空洞。
- **外观伪影**：部分可见性使得优化过程在可见区域过拟合，而在未观测区域产生漂浮物、模糊或颜色失真。
- **多帧不一致**：遮挡模式随时间变化，缺乏全局几何约束的方法难以维持跨帧的时空一致性。

### 现有方法缺口

当前人体渲染方法可按是否针对遮挡设计分为两类：

**未针对遮挡设计的方法**（如 **HumanNeRF**、**3DGS-Avatar**、**GauHuman**）在完全可见的设定下表现优异，但面对遮挡时性能急剧下降。以 **GauHuman** 为例，其标准训练流程使用所有像素参与损失计算、默认损失权重，并启用自适应密集化与剪枝控制。在遮挡场景下，这些设计导致：遮挡区域的无效像素污染训练信号；密集化/剪枝操作可能过早移除表示被遮挡部位的高斯原语，使几何结构不可逆地退化。

**针对遮挡设计的方法**（如 **OccNeRF**、**Wild2Avatar**）尝试通过场景解耦或遮挡感知训练来缓解问题，但通常依赖 NeRF 表示，训练耗时数小时，且渲染质量受限于 NeRF 固有的模糊性。并行工作 **OccGaussian** 探索了基于高斯的遮挡人体渲染，但使用了 5 倍于标准设置的训练帧，与常规设定不完全等价。

### 核心瓶颈与动机

上述分析揭示了一个关键瓶颈：**遮挡场景下，部分可见性导致几何监督信号严重稀疏，传统方法既缺乏补全缺失几何的机制，也缺乏在未观测区域生成合理外观的能力**。单纯调整训练策略（如仅训练可见像素）可以缓解部分问题，但无法从根本上解决几何缺失——被遮挡的身体部位如果没有额外的先验信息引导，3D 表示将永远无法恢复。

本文的动机由此明确：**能否利用 2D 生成扩散模型中蕴含的丰富人体先验，来补全遮挡区域的几何与外观？** 扩散模型（如 Stable Diffusion）在海量图像数据上预训练，对人体形态、姿态和外观具有强大的生成能力。然而，直接将其应用于 3D 人体渲染面临两大挑战：

1. **生成不一致性**：扩散模型逐帧独立修复时，生成的人体外观在不同视角和帧间缺乏一致性（见 Figure 4），直接用于 3D 监督会导致渲染闪烁和几何坍塌。
2. **姿态对齐困难**：在复杂姿态下，扩散模型的条件生成可能出现多肢、错位等异常（见 Figure 3），需要更鲁棒的姿态条件策略。

OccFusion 的核心洞察在于：**将遮挡人体重建解耦为几何补全与外观精炼两个子问题**。几何补全可以通过在二值掩码（而非 RGB 图像）上施加扩散先验来实现——因为人体轮廓对微小变化更宽容，帧间一致性更高；外观精炼则可以利用粗重建结果作为上下文参考，引导扩散模型在未观测区域生成细节合理的外观。这一解耦策略使得 3D 高斯散点的高效性与 2D 扩散先验的生成能力得以互补，从而在仅 10 分钟的训练时间内，实现遮挡人体的完整、锐利渲染。



## 核心方法与创新机理

OccFusion 的核心创新在于将**生成扩散先验**引入基于 3D 高斯散点的遮挡人体重建，通过**三阶段流水线**将遮挡问题解耦为几何补全与外观精炼两个子问题，并在每个阶段对基线方法进行了针对性改造。

### 1. 将遮挡人体重建解耦为几何补全与外观精炼

现有单目视频人体渲染方法（如 GauHuman、HumanNeRF、3DGS-Avatar）假设人体各部位始终完全可见。在真实遮挡场景下，部分可见性直接导致几何不完整、渲染伪影和缺失身体部位。OccFusion 的核心洞察是：**几何完整性与外观真实性可以分阶段处理**——先利用扩散模型的生成能力获得可靠的几何监督，再在此基础上恢复被遮挡区域的细节外观。

### 2. 三阶段流水线中的关键 changed slots

相对于基线方法，OccFusion 在以下四个关键维度上做出了实质性改变：

#### (1) 可见性掩码利用：从“仅监督可见像素”到“扩散修复生成完整几何监督”

**基线做法**：GauHuman 等方法仅使用原始分割掩码 $M$ 监督可见像素，遮挡区域无任何额外指导，导致几何在未观测区域坍缩。

**OccFusion 做法**：在**初始化阶段**（Initialization Stage），利用姿态简化的 Stable Diffusion 1.5 + ControlNet 从部分可见性掩码生成完整人形二值掩码 $\hat{M}$。该阶段的关键设计选择包括：
- **移除自遮挡关节**：当 SMPL 关节深度与 2D z-buffer 距离 $d > \sigma$ 时，判定该关节被自遮挡并从 2D 姿态条件中移除（Figure 3），避免生成模型产生多余肢体等异常。
- **修复二值掩码而非 RGB**：直接修复 RGB 图像会导致帧间外观不一致（Figure 4），而二值掩码对轮廓的微小变化容忍度更高，帧间一致性显著优于 RGB 修复。

生成的完整掩码 $\hat{M}$ 为后续优化阶段提供了可靠的几何监督信号。

#### (2) 优化目标：从“纯光度损失”到“SDS 正则化强制几何完整性”

**基线做法**：GauHuman 仅使用组合光度损失（L1、SSIM、LPIPS、Mask L2）训练高斯，缺乏对未观测区域几何的显式约束。

**OccFusion 做法**：在**优化阶段**（Optimization Stage），额外施加**姿态条件的分数蒸馏采样（SDS）损失**在渲染的占用图 $A$ 上：

$$\mathcal{L}_{\mathrm{SDS}}^{(\mathbf{P})} = \mathbb{E}_{t,\epsilon} \left[ w(t) \left( \epsilon_{\phi}(\mathbf{A}; t, \mathbf{P}) - \epsilon \right) \frac{\partial \mathbf{A}}{\partial \Pi} \right]$$

该损失通过扩散模型的分数梯度驱动占用图趋向完整人体形状。同时引入**随机激活的规范姿态正则化**：以 75% 概率激活姿态空间 SDS，25% 概率激活规范姿态 SDS，总梯度为：

$$\nabla_{\Pi} \left[ \mathcal{L}_{photo} + \rho \cdot \lambda_{pose} \mathcal{L}_{\mathrm{SDS}}^{(\mathbf{P})} + (1 - \rho) \cdot \lambda_{can} \mathcal{L}_{\mathrm{SDS}}^{(\hat{\mathbf{P}})} \right]$$

这一设计平衡了几何完整性与外观学习：规范姿态正则化提供跨帧一致的几何约束，而姿态空间 SDS 则适应具体姿态下的形状变化。实验表明，SDS 施加在**占用图上而非 RGB 图像上**至关重要——RGB 生成结果的不一致性会导致渲染缺陷（Figure 9）。

#### (3) 未观测区域外观恢复：从“无额外策略”到“上下文感知修复”

**基线做法**：无额外恢复策略，完全依赖高斯表示的自然补全能力，导致未观测区域细节缺失、模糊。

**OccFusion 做法**：在**精炼阶段**（Refinement Stage），提出**上下文感知修复**（in-context inpainting）：将优化阶段生成的粗略渲染 $\hat{I}$ 与原始遮挡图像 $I$ 上下堆叠作为扩散模型 $\Phi$ 的单张输入，配合提示词 "the same person standing in two different backgrounds"，生成被遮挡区域的 RGB 参考图像 $\tilde{I}$。遮挡区域 $R = (1 - M) \cdot A$ 由可见性掩码和渲染占用图共同确定。随后利用 $\tilde{I}$ 对高斯进行微调：

$$\nabla_{\Pi} \left[ \lambda_{rgb} L_1(\mathbf{M} \cdot \mathbf{I}, \mathbf{M} \cdot \mathbf{I}') + \lambda_{mask} L_2(\hat{\mathbf{M}}, \mathbf{A}) + \lambda_{gen} L_1(\tilde{\mathbf{I}}, \mathbf{R} \cdot \mathbf{I}') + \lambda_{lpips} \mathrm{LPIPS}(\mathbf{I}, \mathbf{I}') \right]$$

消融实验（Table 2）证实，精炼阶段是整个流程的关键环节：LPIPS 从 55.35 骤降至 32.34，同时 PSNR 达到最高 23.96。

#### (4) GauHuman 遮挡适应：三项针对性改造

**基线做法**：标准 GauHuman 训练——所有像素参与训练、默认损失权重、启用密集化/剪枝自适应控制。

**OccFusion 做法**：提出 **OccGauHuman** 作为改进基线，包含三项针对性调整：
- **仅训练可见人类像素**：避免遮挡物像素污染高斯表示。
- **提高掩码损失权重**：增强对可见区域几何的监督强度。
- **禁用密集化和剪枝**：维持 SMPL 初始化的完整几何结构，防止在稀疏观察下错误地移除或添加高斯。

这三项改造使 OccGauHuman 在 ZJU-MoCap 上相比原始 GauHuman 的 PSNR 提升 0.99 dB（21.55 → 22.54），为后续三阶段流水线提供了更强的起点。

### 3. 创新点的因果链条

上述四个 changed slots 构成了完整的因果链条：**OccGauHuman** 提供遮挡鲁棒的基础表示 → **初始化阶段**生成完整几何监督 → **优化阶段**通过 SDS 正则化强制几何完整性并去除伪影 → **精炼阶段**通过上下文感知修复恢复未观测区域的细节外观。各阶段相互依赖，消融实验（Table 2）证实移除任一阶段均会导致性能下降，完整流水线才能达到最优的 PSNR 23.96、SSIM 0.9548、LPIPS 32.34。



OccFusion 采用**三阶段顺序流水线**，将遮挡人体重建解耦为几何补全与外观精炼两个子问题，并通过生成扩散先验桥接二者。流水线的输入为单目遮挡视频帧 ${\mathbf{I}}$、对应的可见性分割掩码 ${\mathbf{M}}$（由 SAM 提取）以及 SMPL 姿态先验 ${\mathbf{P}}$（由 HMR 2.0 估计），输出为可渲染完整人体的 3D 高斯散点表示 $\Pi$。三阶段的模块关系与数据流如 Figure 2 所示，总训练耗时约 10 分钟（单 TITAN RTX GPU）。

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_CZwphz5vgz/figures/002_Figure_2.jpg]]
*Figure 2: OccFusion achieves occluded human rendering via three sequential stages. In the Initialization Stage, we recover complete binary human masks {Mˆ } from occluded partial observations {I} with the help of segmentation priors {M} and pose priors {P}. {Mˆ } will be further used to help optimize the 3D Gaussians Π in subsequent stages. In the Optimization Stage, we apply {P} conditioned SDS on both posed human and canonical human to enforce the human occupancy to remain complete. In the Refinement Stage, we use the coarse human renderings {ˆI} from the Optimization Stage to help generate missing RGB values in {I} through our proposed in-context inpainting. Through this process, both the appearan...*

### 阶段一：初始化（Initialization）

该阶段的目标是从部分可见的遮挡掩码中恢复**完整人形二值掩码** $\hat{\mathbf{M}}$，为后续优化提供可靠的几何监督。核心操作包括：
- **姿态简化**：对原始 SMPL 姿态 $\mathbf{P}$ 进行自遮挡检测——当某关节的 SMPL 深度与 2D z-buffer 的距离 $d$ 超过阈值 $\sigma$ 时（$d > \sigma$），判定该关节被自遮挡并从 2D 姿态条件中移除。如 Figure 3 所示，直接使用原始姿态作为 Stable Diffusion 1.5 + ControlNet 的条件会导致多肢、畸形等生成异常，而移除自遮挡关节后的简化姿态能产生更合理的人体生成结果。
- **掩码修复**：利用姿态简化的扩散模型对遮挡掩码 $\mathbf{M}$ 进行修复，生成完整人形掩码 $\hat{\mathbf{M}}$。选择在二值掩码而非 RGB 图像上进行修复的关键洞察是：生成模型对 RGB 外观的修复在不同帧间高度不一致，但从中提取的二值轮廓却具有更好的帧间一致性（Figure 4），从而为多帧优化提供稳定的几何目标。

### 阶段二：优化（Optimization）

该阶段以改进基线 **OccGauHuman** 为基础，利用修复掩码 $\hat{\mathbf{M}}$ 和 SDS 正则化联合优化 3D 高斯 $\Pi$。OccGauHuman 对原始 GauHuman 进行了三项针对性改造以适应遮挡场景：
1. **仅训练可见像素**：仅在被遮挡区域之外的可见人体像素上计算损失；
2. **加权掩码损失**：提高渲染占用图 $\mathbf{A}$ 与修复掩码 $\hat{\mathbf{M}}$ 之间的 $L_2$ 损失权重；
3. **禁用密集化与剪枝**：保持 SMPL 初始化提供的完整几何结构，避免因稀疏观测导致的自适应控制破坏人体完整性。

在此基础上，优化阶段施加**双重 SDS 正则化**以强制人体几何完整性：
- **姿态空间 SDS**：以 75% 概率激活，对渲染的占用图 $\mathbf{A}$ 施加姿态条件 $\mathbf{P}$ 的分数蒸馏采样损失 $\mathcal{L}_{\mathrm{SDS}}^{(\mathbf{P})}$，驱动占用图趋向完整人体形状；
- **规范姿态 SDS**：以 25% 概率激活规范姿态条件 $\hat{\mathbf{P}}$ 的 SDS 损失 $\mathcal{L}_{\mathrm{SDS}}^{(\hat{\mathbf{P}})}$，作为正则化项增强几何一致性。

总优化梯度如式 (5) 所示，将组合光度损失（RGB $L_1$、掩码 $L_2$、SSIM、LPIPS）与随机激活的双重 SDS 损失统一反向传播至高斯参数 $\Pi$。

### 阶段三：精炼（Refinement）

优化阶段虽能恢复完整几何，但未观测区域的 RGB 外观仍缺乏有效监督。精炼阶段通过**上下文感知修复（in-context inpainting）** 解决这一问题：
- 利用渲染占用图 $\mathbf{A}$ 和可见性掩码 $\mathbf{M}$ 识别被遮挡区域 $\mathbf{R} = (1 - \mathbf{M}) \cdot \mathbf{A}$；
- 将优化阶段输出的粗渲染结果 $\hat{\mathbf{I}}$ 与原始遮挡帧 $\mathbf{I}$ 上下拼接，作为扩散模型 $\Phi$ 的输入，并附加提示短语引导生成被遮挡区域的 RGB 参考图像 $\tilde{\mathbf{I}}$；
- 使用生成的 $\tilde{\mathbf{I}}$ 对高斯 $\Pi$ 进行微调，损失函数包含可见区域的 $L_1$、生成区域的 $L_1$ 以及全局 LPIPS 感知损失（式 (6)）。

消融实验（Table 2）表明，精炼阶段是整条流水线的关键环节：它使 LPIPS 从 55.35 骤降至 32.34，同时将 PSNR 推至最高的 23.96，显著改善了未观测区域的细节质量。



### 3.1 基础表示：LBS 与 3D 高斯散点

OccFusion 的几何表示建立在两个基础模块之上。

**线性混合蒙皮（LBS）** 将规范空间中的点 $\mathbf{x_c}$ 变换到姿态空间 $\mathbf{x_p}$：

$$\mathbf{x_p} = \sum_{k=1}^{K} w_k \left( G_k(\mathbf{J}, \theta) \mathbf{x_c} + b_k(\mathbf{J}, \theta, \beta) \right)$$

其中 $K$ 为骨骼关节数，$w_k$ 为蒙皮权重，$G_k$ 和 $b_k$ 分别表示由姿态 $\theta$ 和形状 $\beta$ 参数驱动的第 $k$ 个关节的旋转矩阵与平移向量。该变换使得高斯散点可随人体姿态动态变形。

**3D 高斯散点渲染** 通过 $\alpha$ 混合计算像素颜色 $C$：

$$C = \sum_{j=1}^{N} c_j \alpha_j \prod_{k=1}^{j-1} (1 - \alpha_k)$$

其中 $N$ 为沿光线有序排列的高斯数量，$c_j$ 和 $\alpha_j$ 分别为第 $j$ 个高斯的颜色与不透明度。渲染的占用图 $\mathbf{A}$ 可通过将 $\alpha$ 混合应用于二值不透明度获得，为后续 SDS 正则化提供几何信号。

### 3.2 OccGauHuman：遮挡适应的改进基线

本文在 GauHuman 基础上提出三项针对性改造，形成 OccGauHuman：

1. **仅训练可见像素**：将训练限制在分割掩码 $\mathbf{M}$ 标记的可见人体像素上，避免遮挡区域噪声干扰。
2. **加权掩码损失**：提高渲染占用图 $\mathbf{A}$ 与分割掩码之间掩码损失的权重，强化几何监督。
3. **禁用密集化与剪枝**：冻结 3D 高斯自适应控制，维持 SMPL 初始化的完整人体几何结构，防止遮挡导致的高斯退化。

### 3.3 初始化阶段：掩码修复

初始化阶段的目标是从部分可见的掩码 $\mathbf{M}$ 生成完整人形掩码 $\hat{\mathbf{M}}$。为避免生成模型直接修复 RGB 图像带来的帧间不一致（Figure 4），本文选择在二值掩码层面进行修复。

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_CZwphz5vgz/figures/004_Figure_4.jpg]]
*Figure 4: While generative models provide inconsistent inpainting results, the binary masks that can be extracted from these generated images are much more consistent*

为提升姿态条件的可行性，引入自遮挡关节移除：当 SMPL 关节深度与对应 2D z-buffer 的距离 $d$ 超过阈值 $\sigma$ 时，判定该关节被自遮挡并从 2D 姿态条件中移除：

$$d > \sigma$$

简化后的姿态条件输入 Stable Diffusion 1.5 + ControlNet，生成完整人形掩码 $\hat{\mathbf{M}}$，为后续优化阶段提供可靠的几何监督。

### 3.4 优化阶段：SDS 正则化

优化阶段在 OccGauHuman 基础上施加 Score Distillation Sampling（SDS）约束，驱动 3D 高斯 $\Pi$ 趋向完整人体形状。

**组合光度损失** 仅在可见像素上计算：

$$\lambda_{rgb} L_1(\mathbf{M} \cdot \mathbf{I}, \mathbf{M} \cdot \mathbf{I}') + \lambda_{mask} L_2(\hat{\mathbf{M}}, \mathbf{A}) + \lambda_{ssim} \mathrm{SSIM}(\mathbf{M} \cdot \mathbf{I}, \mathbf{M} \cdot \mathbf{I}') + \lambda_{lpips} \mathrm{LPIPS}(\mathbf{M} \cdot \mathbf{I}, \mathbf{I}')$$

其中 $\mathbf{I}$ 为真实图像，$\mathbf{I}'$ 为渲染图像，$\hat{\mathbf{M}}$ 为初始化阶段生成的修复掩码。

**SDS 损失** 作用于渲染占用图 $\mathbf{A}$，以姿态条件 $\mathbf{P}$ 引导扩散模型 $\epsilon_{\phi}$ 的分数梯度：

$$\mathcal{L}_{\mathrm{SDS}}^{(\mathbf{P})} = \mathbb{E}_{t,\epsilon} \left[ w(t) \left( \epsilon_{\phi}(\mathbf{A}; t, \mathbf{P}) - \epsilon \right) \frac{\partial \mathbf{A}}{\partial \Pi} \right]$$

其中 $t$ 为扩散时间步，$w(t)$ 为权重函数，$\epsilon$ 为注入噪声。该损失通过扩散模型的去噪分数驱动占用图趋向完整人体形状，从而补全被遮挡区域的几何。

**总梯度** 以概率机制在姿态空间与规范姿态之间切换 SDS 正则化：

$$\nabla_{\Pi} \left[ \mathcal{L}_{photo} + \rho \cdot \lambda_{pose} \mathcal{L}_{\mathrm{SDS}}^{(\mathbf{P})} + (1 - \rho) \cdot \lambda_{can} \mathcal{L}_{\mathrm{SDS}}^{(\hat{\mathbf{P}})} \right]$$

其中 $\rho \sim \mathrm{Bernoulli}(0.75)$，以 75% 概率激活姿态空间 SDS，25% 概率激活规范姿态 SDS（使用规范姿态 $\hat{\mathbf{P}}$）。这一设计平衡了几何完整性与外观学习：姿态空间 SDS 直接约束当前视角的占用图，规范姿态 SDS 则从标准姿态角度强制全局人体完整性。

### 3.5 精炼阶段：上下文感知修复

精炼阶段旨在改善未观测区域的渲染细节。首先利用渲染占用图 $\mathbf{A}$ 与可见性掩码 $\mathbf{M}$ 识别被遮挡区域 $\mathbf{R} = (1 - \mathbf{M}) \cdot \mathbf{A}$。然后采用上下文感知修复（in-context inpainting）：将优化阶段输出的粗渲染 $\hat{\mathbf{I}}$ 与原始图像 $\mathbf{I}$ 拼接为单张图像输入扩散模型 $\Phi$，生成被遮挡区域的 RGB 参考图像 $\tilde{\mathbf{I}}$。

**精炼阶段损失梯度**：

$$\nabla_{\Pi} \left[ \lambda_{rgb} L_1(\mathbf{M} \cdot \mathbf{I}, \mathbf{M} \cdot \mathbf{I}') + \lambda_{mask} L_2(\hat{\mathbf{M}}, \mathbf{A}) + \lambda_{gen} L_1(\tilde{\mathbf{I}}, \mathbf{R} \cdot \mathbf{I}') + \lambda_{lpips} \mathrm{LPIPS}(\mathbf{I}, \mathbf{I}') \right]$$

其中 $\lambda_{gen} L_1(\tilde{\mathbf{I}}, \mathbf{R} \cdot \mathbf{I}')$ 利用生成图像 $\tilde{\mathbf{I}}$ 监督被遮挡区域的渲染，$\mathrm{LPIPS}(\mathbf{I}, \mathbf{I}')$ 在全局图像上施加感知损失。消融实验（Table 2）表明，精炼阶段是 LPIPS 从 55.35 骤降至 32.34 的关键环节。

### 补充图表

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_CZwphz5vgz/figures/003_Figure_3.jpg]]
*Figure 3: Stable Diffusion 1.5 generations [48] conditioned on a challenging pose P. While conditioning on the original pose results in multiple limbs and other abnormalities, our method of simplifying pose by removing self-occluded joints results in more feasible generations*



## 实验与关键发现

### 主实验结果

OccFusion 在模拟遮挡（ZJU-MoCap）与真实遮挡（OcMotion）两个基准上均取得最优渲染质量，尤其在感知指标 LPIPS 上大幅领先所有基线方法。Table 1 汇总了定量对比结果。

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_CZwphz5vgz/figures/005_Table_1.jpg]]
*Table 1: Quantitative comparison on the ZJU-MoCap and OcMotion datasets. LPIPS values are scaled by ×1000. We color cells that have the best and second best metric values*

在 **ZJU-MoCap** 模拟遮挡评测集上，OccFusion 取得 PSNR **23.96**、SSIM **0.9548**、LPIPS **32.34**（×1000）。与最强的并行工作 OccGaussian（PSNR 23.29, SSIM 0.9482, LPIPS 41.93）相比，OccFusion 在 PSNR 上提升 0.67 dB，SSIM 提升 0.0066，LPIPS 降低 9.59——感知质量的提升幅度远大于像素级指标的改善，表明方法在恢复遮挡区域的高频细节和纹理一致性方面具有显著优势。未针对遮挡设计的传统方法（HumanNeRF、3DGS-Avatar、GauHuman）在 LPIPS 上表现更差，其渲染结果普遍存在变色、漂浮伪影或缺失身体部位等问题。

在 **OcMotion** 真实遮挡数据集上，OccFusion 同样超过专门为遮挡设计的 NeRF 方法 OccNeRF：PSNR 从 15.71 提升至 **18.28**（+2.57 dB），SSIM 从 0.8523 提升至 **0.8875**，LPIPS 从 82.90 降至 **82.42**。需要注意的是，OcMotion 缺乏真实背景，所有指标仅在可见像素上计算（以 * 标注），因此 PSNR 绝对值偏低，但相对提升幅度仍然显著。

定性对比（Figure 5, Figure 6, Figure 7）进一步印证了定量结论：OccFusion 是唯一能够持续生成锐利、无遮挡、完整人体的方法。基线方法在遮挡区域常出现模糊、肢体缺失或错误的纹理填充，而 OccFusion 通过三阶段流水线有效补全了几何与外观。

### 消融实验

Table 2 报告了在 ZJU-MoCap 上的逐模块消融结果，揭示了各阶段的因果贡献。

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_CZwphz5vgz/figures/007_Table_2.jpg]]
*Table 2: Ablation results on the ZJU-MoCap [44] dataset. LPIPS values are scaled by ×1000*

**改进基线 OccGauHuman**（Exp. A vs. Exp. 1）：将原始 GauHuman 替换为 OccGauHuman（仅训练可见像素、提高掩码损失权重、禁用密集化与剪枝）后，PSNR 从 21.55 提升至 22.54（+0.99 dB），SSIM 从 0.9479 提升至 0.9506。这表明三项针对性调整有效增强了高斯表示在稀疏观察下的鲁棒性，为后续阶段提供了更强的初始几何。

**初始化阶段**（Exp. B）：引入扩散模型修复的完整人形掩码 M̂ 作为几何监督后，PSNR 进一步提升至 23.52，SSIM 至 0.9516。该阶段的核心作用是提供可靠的完整几何目标，使优化阶段的高斯散点能够向完整人体形状收敛，而非仅拟合可见区域。

**优化阶段的 SDS 正则化**（Exp. C 和 D）：加入姿态空间 SDS 后（Exp. C），PSNR 升至 23.90，但 LPIPS 从 52.35 升至 55.47；加入规范姿态 SDS 后（Exp. D），PSNR 维持 23.91，LPIPS 为 55.35。这一现象揭示了 SDS 正则化的双刃剑效应：它通过扩散模型梯度强制占用图趋向完整人体形状，有效移除了漂浮伪影并增强了几何完整性（PSNR 提升），但扩散模型的生成先验引入了一定的外观不一致性，导致感知质量暂时下降（LPIPS 升高）。这恰好说明了精炼阶段的必要性。

**精炼阶段**（Exp. E）：完整三阶段流水线使 LPIPS 从 55.35 骤降至 **32.34**，同时 PSNR 达到最高 **23.96**。精炼阶段通过上下文感知修复生成被遮挡区域的 RGB 参考图像，并利用 L1 和感知损失对高斯进行微调，显著改善了未观测区域的纹理细节和外观一致性。该阶段是整个流程中 LPIPS 增益最大的单一模块。

定性消融（Figure 6）以可视化方式展示了各阶段的递进效果：初始化阶段补全了人体轮廓，优化阶段移除了伪影，精炼阶段恢复了被遮挡区域的细节纹理。

### 关键设计选择验证

**掩码修复 vs. 直接 RGB 修复**：Figure 4 展示了在遮挡视频帧上直接进行 RGB 修复与先修复二值掩码再提取轮廓的对比。生成模型对 RGB 图像的修复结果在不同帧之间高度不一致（颜色、纹理、姿态均可能变化），而从修复图像中提取的二值掩码则具有更强的帧间一致性。这一观察是初始化阶段选择掩码修复而非 RGB 修复的根本原因。Figure 9 进一步表明，若在 RGB 图像上施加 SDS，会导致渲染结果出现缺陷，而在占用图上施加 SDS 则能稳定地强制几何完整性。

**修复掩码 vs. 完整无遮挡掩码**：Figure 10 对比了使用真实完整掩码与使用修复掩码训练时的渲染质量收敛曲线。尽管修复掩码相比真实掩码存在轻微的不一致性，但训练流程最终收敛到相同的渲染质量水平，验证了掩码修复策略的可靠性。

**上下文感知修复的有效性**：Figure 8 对比了精炼阶段中使用/不使用上下文感知修复的效果。无上下文修复时，修复结果与被遮挡区域的真实外观存在明显偏差；引入上下文参考（将粗渲染 Î 与原始遮挡帧 I 拼接输入扩散模型）后，生成的 RGB 参考图像更好地保持了人物身份和外观一致性，从而提升了微调后的渲染质量。

### 失败模式与局限性

尽管 OccFusion 在整体指标上表现优异，但方法仍存在若干系统性局限：

1. **4D 一致性问题**：生成模型（Stable Diffusion 1.5 + ControlNet）难以完美维持跨帧的时空一致性。如 Figure 4 和 Figure 8 所示，修复结果在不同帧之间仍可能出现纹理漂移或姿态不匹配，这会在精炼阶段引入噪声监督，导致部分生成结果不够连贯。

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_CZwphz5vgz/figures/013_Figure_8.jpg]]
*Figure 8: Comparison of the inpainted human in the Refinement Stage with and without using the proposed in-context inpainting technique. Major differences are highlighted with red arrows*

2. **2D 姿态条件的弱约束**：仅使用 2D 骨架作为扩散模型的条件信号，对生成人体的姿态约束较弱。当目标姿态与训练分布差异较大时，生成的人体姿态不一定与条件姿态精确对齐，引入额外的不确定性。Figure 3 展示了通过移除自遮挡关节来简化姿态条件的策略，但这本质上是一种启发式缓解而非根本解决。

3. **缺乏形式化一致性保证**：三阶段流水线依赖启发式设计和经验调整（如 SDS 损失的激活概率 ρ=0.75、自遮挡阈值 σ 等），未提供收敛性或一致性的理论保证。

4. **代码与模型未开源**：目前仅提供了实现细节，复现需要自行实现完整流水线，包括对 GauHuman 的改造、扩散模型修复的集成以及三阶段训练逻辑。

### 补充图表

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_CZwphz5vgz/figures/006_Figure.jpg]]

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_CZwphz5vgz/figures/008_Figure.jpg]]

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_CZwphz5vgz/figures/009_Figure.jpg]]

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_CZwphz5vgz/figures/010_Figure.jpg]]

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_CZwphz5vgz/figures/011_Figure.jpg]]

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_CZwphz5vgz/figures/014_Figure.jpg]]



## 定位与知识库关联

### 1. 基线谱系与继承关系

OccFusion 直接建立在 **GauHuman** 的 3D 高斯散点（3DGS）人体表示框架之上。GauHuman 利用 SMPL 参数模型初始化规范空间中的 3D 高斯，并通过线性混合蒙皮（LBS）变换驱动姿态变形，以 α 混合渲染像素颜色。OccFusion 继承了这一高效表示，并在其基础上提出三项针对性改造，形成改进基线 **OccGauHuman**：

1. **仅训练可见人体像素**：原始 GauHuman 假设所有像素均可用于监督，但在遮挡场景下，被遮挡区域缺乏真实 RGB 值。OccGauHuman 将训练限制在可见性掩码 $\mathbf{M}$ 标记的像素上，避免对不可见区域施加错误的光度约束。
2. **提高掩码损失权重**：将渲染占用图 $\mathbf{A}$ 与分割掩码之间的 $L_2$ 损失的权重调高，以强化几何监督，弥补可见像素减少带来的信息损失。
3. **禁用密集化与剪枝**：标准 3DGS 的自适应控制（密集化/剪枝）会在稀疏观测下移除或错误生长高斯，破坏 SMPL 初始化的完整几何。OccGauHuman 禁用这一机制，维持人体结构的完整性。

消融实验（Table 2，Exp. A vs. Exp. 1）证实，这三项调整使 ZJU-MoCap 上的 PSNR 从 21.55 提升至 22.54（+0.99 dB），SSIM 从 0.9462 提升至 0.9489。

在更广泛的基线谱系中，OccFusion 与以下方法形成对比：

- **HumanNeRF** 与 **3DGS-Avatar**：未针对遮挡设计的 NeRF 和高斯人体渲染方法，在遮挡下产生几何不完整和伪影。
- **OccNeRF**：专门为遮挡设计的 NeRF 方法，在 OcMotion 真实遮挡数据集上 OccFusion 的 PSNR 超过其 2.57 dB（18.28 vs. 15.71），LPIPS 降低 0.48（82.42 vs. 82.90）。
- **OccGaussian**：并行的基于高斯的遮挡人体渲染方法，在 ZJU-MoCap 上 OccFusion 的 PSNR 领先 0.67 dB（23.96 vs. 23.29），LPIPS 大幅领先 9.59（32.34 vs. 41.93）。需注意 OccGaussian 使用 5 倍训练帧，与本文标准设置不完全等价。
- **Wild2Avatar**：针对遮挡的 NeRF 场景解耦方法，但未直接参与主要定量比较。

### 2. 核心创新在知识库中的定位

OccFusion 的核心贡献在于**将 2D 生成扩散先验系统性地引入 3DGS 人体重建流水线**，以解决遮挡导致的几何不完整与外观缺失。这一思路在知识库中占据以下三个交叉点：

**（a）扩散先验驱动的 3D 重建**

与 Score Distillation Sampling（SDS）在文本到 3D 生成中的经典应用不同，OccFusion 将 SDS 施加于**渲染的占用图 $\mathbf{A}$** 而非 RGB 图像。这一设计选择基于关键观察：生成模型在 RGB 空间的修复结果帧间不一致，但二值掩码的帧间一致性显著更高（Figure 4）。在占用图上施加姿态条件的 SDS（式 (4)），使扩散模型的分数梯度驱动高斯几何趋向完整人体形状，同时避免 RGB 不一致性带来的渲染缺陷（Figure 9 对比验证了这一点）。

**（b）遮挡人体重建的解耦策略**

OccFusion 将遮挡人体重建解耦为**几何补全**与**外观精炼**两个阶段。初始化阶段利用扩散模型修复二值掩码，生成完整人形掩码 $\hat{\mathbf{M}}$ 作为后续阶段的可靠几何监督；优化阶段通过 SDS 正则化强制人体完整性；精炼阶段通过上下文感知修复改善未观测区域的外观细节。消融实验（Table 2）表明，精炼阶段使 LPIPS 从 55.35 骤降至 32.34，是整体性能提升的关键环节。

**（c）姿态条件生成的控制策略**

为提升扩散模型在极端姿态下的生成质量，OccFusion 提出**简化姿态条件**：通过 SMPL 深度与 2D z-buffer 比较（$d > \sigma$）识别自遮挡关节，并从 2D 姿态条件中移除这些关节（Figure 3）。这一策略在保持人体语义完整性的同时，避免了扩散模型生成多肢等异常结果。

### 3. 适用边界

**适用场景**：
- 单目视频中被外部物体或自遮挡部分遮蔽的人体渲染
- 需要快速训练（约 10 分钟，单 TITAN RTX GPU）的应用场景
- 对渲染质量（尤其是 LPIPS 感知质量）有较高要求的任务

**不适用或需谨慎的场景**：
- 极端遮挡比例（超过训练中模拟的 50% 中心遮挡）下，扩散先验的可靠性可能下降
- 需要严格 4D（3D + 运动）一致性的场景：生成模型仍难以完美维持时序一致性，部分生成结果不够连贯
- 对姿态对齐精度要求极高的应用：仅使用 2D 姿态条件对生成模型的约束较弱，生成人体的姿态不一定与条件姿态精确对齐

### 4. 局限与开放问题

**已知局限**：

1. **4D 一致性不足**：生成扩散模型难以完美维持跨帧的 3D 几何与外观一致性，可能影响所有阶段的训练质量（Figure 4、Figure 8 中可见不一致性）。
2. **弱姿态条件**：仅使用 2D 姿态关键点作为条件，对生成模型的约束较弱，生成结果存在姿态偏差风险。
3. **无形式化保证**：方法依赖启发式设计和经验调整，未提供收敛性或一致性的形式化保证。
4. **代码未开源**：当前仅提供实现细节，复现需自行实现完整流水线。

**开放问题**：

1. 如何设计或微调一个**专用于人体的 4D 一致性感知扩散模型**，以更好地维持跨帧几何与外观的连贯性？
2. 能否通过更强的 **3D 感知条件**（如多视角姿态、深度图、或规范空间法向）来提升生成模型在遮挡区域的一致性？
3. 在三阶段流水线中，是否存在**端到端联合优化**的可能，以消除各阶段之间的不一致累积？
4. 如何将 OccFusion 的扩散先验策略扩展到**多人交互遮挡**或**人与物体交互**场景？

### 5. 后续工作可能方向

基于 OccFusion 的框架，后续研究可沿以下路径展开：

- **更强的时序一致性约束**：在 SDS 正则化中引入时序维度的分数蒸馏，或使用视频扩散模型替代单图扩散模型。
- **多模态条件融合**：结合深度估计、光流等多模态先验，增强对遮挡区域的几何推理能力。
- **与 NeRF 的混合表示**：探索 3DGS 的效率优势与 NeRF 的连续表示优势的混合方案，在遮挡边界区域获得更平滑的过渡。
- **在线/实时遮挡处理**：将 OccFusion 的训练时间从 10 分钟进一步压缩至秒级，支持实时遮挡人体渲染应用。



## 原文 PDF

![[paperPDFs/NEURIPS_2024/OccFusion_Rendering_Occluded_Humans_with_Generative_Diffusion_Priors.pdf]]
