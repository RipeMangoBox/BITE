---
title: AnyMoLe Any Character Motion In Betweening Leveraging Video Diffusion Models
type: paper
paper_level: A
venue: CVPR
year: 2025
pdf_ref: paperPDFs/CVPR_2025/AnyMoLe_Any_Character_Motion_In_Betweening_Leveraging_Video_Diffusion_Models.pdf
project_link: null
code_link: null
aliases:
- AACMBLVDM
tags:
- CVPR_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 本文利用在大规模真实视频上预训练的视频扩散模型作为运动先验，通过推理阶段上下文自适应（ICAdapt）弥合真实-渲染域差距，并设计两阶段视频生成与运动-视频模仿优化，从而在无需任何外部训练数据的情况下，为任意角色生成平滑的3D中间运动。
primary_logic: 视频扩散模型已包含丰富的运动过渡知识；仅需用2秒上下文运动渲染视频对模型的空间模块进行微调（ICAdapt），就能使其适用于特定渲染角色，再通过自回归两阶段生成和基于可微渲染的优化，将生成的2D视频提升为3D运动，完全绕过了对角色特定动作数据集的依赖。
claims:
- 在人类和非人类角色测试集上，AnyMoLe的HL2Q指标显著优于所有基线方法（人类角色0.0015，非人类角色0.0019）。
- 消融实验表明，移除ICAdapt会导致视频风格不一致，移除精细生成阶段则帧率不足且运动跳跃，两项消融均使所有评估指标下降。
- 用户研究中，AnyMoLe在相似性、忠实度和自然度三个维度上均获得最高偏好票数（人类角色：相似60.12%，忠实63.10%，自然64.88%；非人类角色：相似90.48%，忠实92.46%，自然91.67%）。
- Humanoid character test set 上 HL2Q ↓ = 0.0015
---

# AnyMoLe Any Character Motion In Betweening Leveraging Video Diffusion Models

> [!tip] 核心洞察
> 视频扩散模型已包含丰富的运动过渡知识；仅需用2秒上下文运动渲染视频对模型的空间模块进行微调（ICAdapt），就能使其适用于特定渲染角色，再通过自回归两阶段生成和基于可微渲染的优化，将生成的2D视频提升为3D运动，完全绕过了对角色特定动作数据集的依赖。

| 字段 | 内容 |
|------|------|
| 中文题名 | AnyMoLe：利用视频扩散模型进行任意角色运动中间帧生成 |
| 英文题名 | AnyMoLe Any Character Motion In Betweening Leveraging Video Diffusion Models |
| 会议/期刊 | CVPR 2025 |
| Links |  |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | AnyMoLe |
| Dataset | Humanoid character test set, Non-humanoid character test set, User study |

> [!tip] 效果简介
> - Humanoid character test set 上，HL2Q ↓ 0.0015 vs best baseline (具体数值未列出，但远高于AnyMoLe) (大幅降低)。
> - Non-humanoid character test set 上，HL2Q ↓ 0.0019 vs best baseline (大幅降低)。
> - User study (humanoid) 上，Similarity (% preferred) 60.12 vs other methods (percentages not individually reported) (显著领先)。

## 概要

### 问题瓶颈

现有运动插值（motion in‑betweening）方法存在一个根本性瓶颈：它们严重依赖特定角色的动作捕捉或关键帧数据集进行训练。这使得方法难以泛化到任意骨架结构的角色——尤其是非人类角色、动物或无法进行动作捕捉的角色，因为这些角色缺乏可用的训练数据，导致无法生成自然的中间帧。换言之，**数据依赖性**构成了当前方法向任意角色扩展的核心障碍。

### 核心思路

AnyMoLe 的核心洞察在于：**大规模真实视频上预训练的视频扩散模型已经内化了丰富的运动过渡知识**，只是这些知识被封装在真实视频域中，尚未被用于渲染角色的运动生成。AnyMoLe 通过三个关键机制将这一先验知识释放出来：

1. **ICAdapt（推理阶段上下文自适应）**：仅用一段约 2 秒的上下文运动渲染视频，对预训练视频扩散模型的空间模块和图像投影器进行微调，冻结时间模块以保留运动动力学，从而弥合真实视频与渲染角色之间的域差距。
2. **两阶段视频生成**：先生成稀疏帧建立运动结构，再生成密集帧实现平滑过渡，全程无需外部训练数据。
3. **运动‑视频模仿优化**：利用场景特定的 3D 关节估计器和可微渲染器，将生成的 2D 视频提升为 3D 运动序列，通过优化使渲染结果贴合生成视频。

这一管线完全绕过了对角色特定动作数据集的依赖，使任意角色的运动插值成为可能。

### 方法谱系与知识库定位

AnyMoLe 处于**视频扩散模型 × 运动生成**的交叉地带，其定位可通过以下对比清晰呈现：

- 相对于 **TS[33]**（Qin et al., TOG 2022）等两阶段 Transformer 插值方法：AnyMoLe 不依赖人类运动数据集训练，而是利用视频扩散模型的通用运动先验，天然支持任意骨架角色。
- 相对于 **SinMDM** 等基于扩散的运动生成方法：AnyMoLe 在推理时仅用 2 秒上下文样本进行微调（极端少样本设置），而 SinMDM 等仍需角色特定数据预训练。
- 相对于 **Deciwatch[53]**（Zeng et al., ECCV 2022）等姿态估计方法：AnyMoLe 具备完整的插值生成能力，而不仅仅是姿态提取。

在知识库定位上，AnyMoLe 贡献了一种**无需外部训练数据的任意角色运动插值范式**，其核心组件 ICAdapt 提供了一种通用的视频扩散模型域适应策略，可被后续工作复用。

### 主要结果速览

在人类和非人类角色测试集上，AnyMoLe 的 HL2Q 指标分别达到 **0.0015** 和 **0.0019**，显著优于所有基线方法（Table 2）。用户感知研究中，AnyMoLe 在相似性、忠实度和自然度三个维度上均获得最高偏好票数，尤其在非人类角色上优势极为显著（相似性 90.48%，忠实度 92.46%，自然度 91.67%）（Table 4）。消融实验证实，ICAdapt 和精细生成阶段对最终性能至关重要——移除任一组件均导致视频风格不一致或运动跳跃，所有评估指标下降（Figure 8, Table 3）。

运动中间帧生成（motion in-betweening）是计算机动画领域的核心任务之一：给定稀疏的关键帧和少量上下文运动帧，自动补全中间过渡运动，从而大幅降低动画师的手动劳动。然而，现有方法面临一个根本性瓶颈——**严重依赖特定角色的动作捕捉或关键帧数据集**。无论是基于Transformer的两阶段方法 **TS**（Qin et al., TOG 2022），还是基于扩散模型的运动生成方法 **SinMDM**，都需要在目标角色的运动数据上进行大规模训练。这意味着，对于缺乏数据的角色——如非人类角色、动物、或无法进行动作捕捉的虚构生物——这些方法几乎无法生成自然的中间帧。当角色骨架结构发生变化时，整个模型必须重新训练，泛化能力近乎为零。

这一瓶颈的因果根源在于：现有方法将“运动先验”与“角色外观/结构”捆绑学习。它们直接从特定角色的3D关节序列中学习运动动力学，却忽略了真实世界中存在一个更丰富、更通用的运动知识源——**海量真实视频**。视频扩散模型（如DynamiCrafter）在大规模真实视频上预训练后，已经内化了丰富的运动过渡知识，包括物理合理性、时序连贯性和场景上下文理解。问题在于，这些模型处理的是真实视频域，而运动中间帧生成需要处理的是特定角色的**渲染域**，两者之间存在显著的域差距（domain gap）。

AnyMoLe的核心洞察正是：**视频扩散模型已包含丰富的运动过渡知识；仅需用极少量上下文运动渲染视频对模型进行轻量适配，就能将其通用运动先验迁移到任意角色上，完全绕过对角色特定数据集的依赖。** 这一思路将问题从“为每个角色收集数据并训练模型”转化为“为每个角色微调一个通用先验”，从根本上改变了运动插值的数据范式。

## 核心方法与创新机理

AnyMoLe 的核心创新在于**将运动插值问题转化为视频生成问题**，从而彻底绕过了传统方法对角色特定动作捕捉数据集的依赖。其关键突破可归纳为三个相互耦合的“changed slots”：

### 1. 训练数据需求：从“大量角色特定数据”到“零外部训练数据”

现有运动插值方法（如 **TS**（Qin et al., TOG 2022）、**TST**、**SinMDM** 等）均需在大量特定角色的动作捕捉或关键帧数据集上训练模型，这导致缺乏数据的角色（如非人类角色、动物或无法进行动作捕捉的角色）难以生成自然中间帧。AnyMoLe 将这一范式彻底反转：**无需任何外部训练数据**，仅在推理时利用一段约 2 秒的上下文运动渲染视频进行微调，即可为任意骨架结构的角色生成平滑的 3D 中间运动（见 Table 1 方法对比）。

这一转变的因果机制在于：AnyMoLe 将运动先验的来源从“角色特定的动作数据集”替换为“在大规模真实视频上预训练的视频扩散模型”。视频扩散模型已内化了丰富的运动过渡知识，AnyMoLe 仅需通过 ICAdapt 弥合真实-渲染域差距，便可将这些知识迁移到任意渲染角色上。

### 2. 域适应策略：ICAdapt——冻结时间模块的精准微调

传统方法直接在角色特定数据上训练，无域适应环节。AnyMoLe 提出了**ICAdapt（Inference-stage Context Adaptation，推理阶段上下文自适应）**，其核心设计是**选择性微调**：仅微调视频扩散模型（DynamiCrafter）的空间模块和图像投影器，同时冻结时间模块和帧率嵌入，以保留从真实视频中学到的运动动力学（见 Figure 3）。

ICAdapt 的目标函数为：

$$\underset {\theta} {\min} \mathbb{E}_{\mathcal{E}_{vae}(\mathbf{x}), t, \epsilon} \left[ \left| \left| \epsilon - \epsilon_{\theta} \left( \mathbf{z}_t; I_0, I_N, \mathbf{txt}, t, fps \right) \right| \right|_2^2 \right]$$

该损失在给定首尾帧 $I_0, I_N$、文本条件 $\mathbf{txt}$ 和帧率 $fps$ 下，逼真地重建渲染帧，从而将空间模块“过拟合”到特定渲染角色的外观风格上。消融实验（Table 3, Figure 8）强有力地验证了这一设计的必要性：移除 ICAdapt 后，视频帧间出现明显的风格漂移，所有定量指标（HL2Q、L2Q、L2P、NPSS、LPIPS、CLIP、SSIM）均显著恶化。

### 3. 运动生成流程：从“直接预测 3D 运动”到“视频生成 + 运动-视频模仿优化”

传统方法使用神经网络直接预测 3D 运动序列。AnyMoLe 将这一流程重构为两个阶段：

**（a）两阶段视频生成（粗-细）**：首先生成低帧率的稀疏帧以建立运动结构（粗阶段），再以自回归方式生成高帧率的密集帧以实现平滑过渡（细阶段），期间通过上下文帧引导的潜在空间修复保持上下文一致性（见 Figure 4, Figure 5）。消融实验（Table 3, Figure 8）表明，省略精细阶段会导致帧率不足，帧间出现跳跃，运动不流畅。

**（b）运动-视频模仿优化**：将生成的 2D 视频提升为 3D 运动。该阶段包含两个子模块：
- **场景特定关节估计器 $E_{scene}$**：融合 DINOv2（2D 语义）和 FiT3D（3D 结构）特征，预测 2D 热力图并回归深度，实现少样本 3D 关节估计（见 Figure 6）。消融实验（Table 3）证实，用通用姿态检测器 XPose 替换 $E_{scene}$ 会导致除 NPSS 外所有指标下降，验证了场景特化的必要性。
- **序列优化**：以关键帧为起点，序贯优化根位置 $P$ 和关节旋转 $R$，最小化渲染结果与生成视频的差异：

$$\underset{P, R}{\mathrm{argmin}} \| \mathcal{T}(\mathcal{M}(P,R), p_{cam}) - \mathcal{E}_{scene}(\hat{I}) \|_2^2 + \lambda_{img} \| I_{P,R} - \hat{I} \|_2^2 + L_{reg}$$

其中正则化项 $L_{reg}$ 包含位置正则化（鼓励根位置接近关键帧插值）和旋转正则化（鼓励相邻帧旋转相似），以稳定优化过程。

### 创新总结

AnyMoLe 的三个 changed slots 形成了完整的因果链：**视频扩散模型提供运动先验 → ICAdapt 弥合域差距 → 两阶段生成产出高质量 2D 视频 → 运动-视频模仿优化将其提升为 3D 运动**。这一链条使得 AnyMoLe 在人类角色（HL2Q = 0.0015）和非人类角色（HL2Q = 0.0019）上均大幅领先所有基线方法（Table 2），并在用户研究的相似性、忠实度和自然度三个维度上获得最高偏好票数（Table 4）。

AnyMoLe 的整体流水线由三个核心阶段构成，其设计哲学是**以视频扩散模型作为通用运动先验，完全绕开对角色特定动作数据集的需求**。

### 流水线总览

如 Figure 2 所示，系统接收两类输入：**上下文运动帧**（context frames）和**目标关键帧**（target keyframes），输出为平滑的中间帧 3D 运动序列。整个流水线按以下顺序执行：

1. **推理阶段上下文自适应（ICAdapt）**：利用约 2 秒的上下文运动渲染视频，对预训练的视频扩散模型 DynamiCrafter 进行轻量微调。仅更新空间模块（spatial module）和图像投影器（image projector），冻结时间模块（temporal module）和帧率嵌入（fps embedding），从而在保留真实视频中学习到的运动动力学知识的同时，弥合真实-渲染域差距（Sec 3.1）。

2. **两阶段视频生成**：微调后的扩散模型 $D_{adp}$ 以自回归方式生成中间帧视频。第一阶段（粗阶段）生成低帧率稀疏帧，建立运动结构骨架；第二阶段（细阶段）在此基础上生成高帧率密集帧，实现平滑过渡。生成过程中通过上下文帧引导的潜在空间修复（latent inpainting）保持与输入上下文的一致性（Sec 3.2）。

3. **运动-视频模仿优化**：将生成的 2D 视频提升为 3D 运动。首先由场景特定关节估计器 $E_{scene}$ 从视频帧中估计 3D 关节位置，然后以关键帧为起点，序贯优化根位置 $P$ 和关节旋转 $R$，最小化渲染结果与生成视频的差异，并辅以位置正则化和旋转正则化约束（Sec 3.3）。

### 关键模块关系

- **ICAdapt** 是连接通用视频先验与特定渲染角色的桥梁。其训练目标为在给定首尾帧 $I_0, I_N$、文本条件 $\mathbf{txt}$ 和帧率 $fps$ 的条件下，逼真地重建渲染帧：

  $$\min_{\theta} \mathbb{E}_{\mathcal{E}_{vae}(\mathbf{x}), t, \epsilon} \left[ \left\| \epsilon - \epsilon_{\theta} \left( \mathbf{z}_t; I_0, I_N, \mathbf{txt}, t, fps \right) \right\|_2^2 \right]$$

- **场景特定关节估计器 $E_{scene}$** 融合 DINOv2（2D 语义特征）和 FiT3D（3D 结构特征），预测 2D 热力图并回归深度，实现少样本 3D 关节估计。其训练损失为相机投影后的真实 3D 关节与估计关节之间的均方误差：

  $$L_{joint} = \| T(G_{joint}, p_{cam}) - J_{est} \|_2^2$$

- **运动-视频模仿优化** 的完整目标函数为：

  $$\underset{P, R}{\mathrm{argmin}} \| \mathcal{T}(\mathcal{M}(P, R), p_{cam}) - \mathcal{E}_{scene}(\hat{I}) \|_2^2 + \lambda_{img} \| I_{P, R} - \hat{I} \|_2^2 + L_{reg}$$

  其中 $L_{reg} = \lambda_{pos} \| P_j - P_{intp} \|_2^2 + \lambda_{rot} \| R_j - R_{prev} \|_2^2$，分别鼓励根位置接近关键帧线性插值、相邻帧旋转平滑。

### 输入输出流

- **输入**：任意角色的上下文运动帧（渲染图像序列）及目标关键帧位姿
- **ICAdapt 输出**：适配该角色的微调扩散模型 $D_{adp}$
- **视频生成输出**：与上下文风格一致、运动平滑的中间帧渲染视频
- **最终输出**：可直接用于动画的 3D 中间运动序列（根位置 + 关节旋转）

整个流水线的核心优势在于**零外部训练数据**：ICAdapt 仅需 2 秒上下文样本（约 500 步微调），关节估计器仅需场景内少量标注帧（约 3500 步训练），即可为任意骨架结构的角色生成自然中间帧运动。

### 3.1 ICAdapt：推理阶段上下文自适应

**设计动机** 预训练视频扩散模型（如 DynamiCrafter）的知识来源于大规模真实视频，直接将其应用于渲染角色视频会产生显著的域差距，表现为帧间风格漂移和运动失真。ICAdapt 的核心思想是：仅利用待插值角色自身的一段极短上下文运动渲染视频（约2秒），在推理阶段对模型的空间感知模块进行微调，使其适配该特定渲染场景的外观和运动风格，同时冻结时间模块以保留从真实视频中学习到的运动动力学先验。

**微调策略** 给定一段由首尾关键帧渲染而成的上下文视频片段，ICAdapt 对 DynamiCrafter 的**空间模块**和**图像投影器**进行过拟合训练，而**时间模块**和**帧率嵌入**保持冻结。这一设计的关键因果机制在于：时间模块编码了通用的运动过渡规律，冻结它确保模型不会因为少量渲染样本而遗忘运动先验；空间模块和图像投影器的微调则使模型学会将渲染域的视觉特征映射到与真实视频一致的潜在空间，从而弥合域差距。

**训练目标** ICAdapt 采用标准的视频扩散去噪损失，其形式化表达如公式 (1) 所示：

$$
\min_{\theta} \mathbb{E}_{\mathcal{E}_{vae}(\mathbf{x}), t, \epsilon} \left[ \left\| \epsilon - \epsilon_{\theta} \left( \mathbf{z}_t; I_0, I_N, \mathbf{txt}, t, fps \right) \right\|_2^2 \right] \tag{1}
$$

其中各变量含义如下：
- $\mathbf{x}$：输入的渲染视频帧；
- $\mathcal{E}_{vae}(\mathbf{x})$：VAE 编码器将视频帧映射到潜在空间，得到初始潜在表示 $\mathbf{z}_0$；
- $t$：扩散时间步；
- $\epsilon$：从标准高斯分布采样的噪声；
- $\mathbf{z}_t$：在时间步 $t$ 加噪后的潜在表示；
- $I_0, I_N$：首帧和尾帧图像，作为条件输入引导生成方向；
- $\mathbf{txt}$：可选的文本条件（如动作描述）；
- $fps$：目标帧率嵌入；
- $\epsilon_{\theta}$：参数为 $\theta$ 的去噪网络（仅空间模块和图像投影器的参数被更新）；
- $\theta$：待优化的模型参数子集。

该损失函数的物理意义是：在给定首尾帧、文本条件和帧率的前提下，使去噪网络能够精确预测所添加的噪声，从而逼真地重建渲染帧。通过最小化该损失，模型学会了在渲染域中生成与上下文运动风格一致的视频帧。

---

### 3.2 两阶段视频生成

**问题建模** 运动插值任务被重新形式化为**上下文帧引导的潜在空间修复**问题。给定上下文运动帧和待插值的关键帧，扩散模型需要在潜在空间中填充缺失的中间帧，同时保持与上下文帧的时空一致性。

**粗生成阶段** 第一阶段以自回归方式生成低帧率视频。具体而言，模型以首尾关键帧为条件，首先生成中间若干稀疏帧，这些帧建立了运动的整体结构和大致轨迹。自回归机制确保每一段生成的稀疏帧与其相邻的上下文帧在潜在空间中保持连贯。

**精细生成阶段** 第二阶段以粗阶段生成的低帧率视频为骨架，进一步生成高帧率视频。通过在稀疏帧之间进行密集插值，精细阶段填充了运动细节，使帧间过渡平滑自然。两阶段设计的关键优势在于：粗阶段提供了全局运动结构约束，精细阶段在此约束下进行局部细节填充，从而避免了直接生成高帧率视频时可能出现的运动跳跃和不连贯。

**上下文一致性保持** 在整个扩散去噪过程中，上下文帧的潜在表示被用作引导信号，通过潜在空间修复机制确保生成帧与已知上下文帧在风格和运动上保持一致。这一机制的具体实现细节可参见 Figure 4 和 Figure 5 的流程示意。

---

### 3.3 场景特定关节估计器

**设计动机** 通用姿态检测器（如 XPose）在渲染角色视频上的精度有限，尤其对于非人类角色或特殊骨架结构，其估计误差会严重损害后续运动优化质量。因此，AnyMoLe 为每个场景训练一个专用的 3D 关节估计器 $E_{scene}$。

**特征融合** 估计器融合两类互补特征：
- **DINOv2 特征**：提供 2D 语义理解能力，帮助定位关节在图像中的大致区域；
- **FiT3D 特征**：提供 3D 结构先验，辅助推理关节的深度信息。

两者结合使估计器能够在少样本条件下准确预测 2D 热力图并回归深度值。

**训练目标** 关节估计器的损失函数如公式 (2) 所示：

$$
L_{joint} = \| \mathcal{T}(G_{joint}, p_{cam}) - J_{est} \|_2^2 \tag{2}
$$

其中：
- $G_{joint}$：真实的 3D 关节位置；
- $p_{cam}$：相机参数；
- $\mathcal{T}(\cdot, p_{cam})$：相机投影函数，将 3D 关节投影到 2D 图像平面；
- $J_{est}$：估计器预测的 2D 关节位置；
- $\|\cdot\|_2^2$：均方误差。

该损失直接比较投影后的真实关节位置与估计位置，驱动估计器学习从渲染图像到 3D 关节的映射。训练时仅使用加权后的关键帧样本，且**不包含后视图图像**，因为后视图会混淆左右关节信息，降低估计精度（消融实验已验证此点）。

---

### 3.4 运动-视频模仿优化

**优化框架** 获得生成视频后，AnyMoLe 通过可微渲染和序列优化将 2D 视频提升为 3D 运动。优化变量为角色各帧的根位置 $P$ 和关节旋转 $R$，目标是最小化渲染结果与生成视频之间的差异。整体目标函数如公式 (3) 所示：

$$
\underset{P, R}{\mathrm{argmin}} \| \mathcal{T}(\mathcal{M}(P, R), p_{cam}) - \mathcal{E}_{scene}(\hat{I}) \|_2^2 + \lambda_{img} \| I_{P,R} - \hat{I} \|_2^2 + L_{reg} \tag{3}
$$

其中各项含义如下：
- $\mathcal{M}(P, R)$：根据根位置 $P$ 和关节旋转 $R$ 计算出的 3D 运动序列；
- $\mathcal{T}(\cdot, p_{cam})$：相机投影函数，将 3D 关节投影到 2D 平面；
- $\mathcal{E}_{scene}(\hat{I})$：场景特定关节估计器对生成帧 $\hat{I}$ 的关节预测结果；
- $I_{P,R}$：根据当前运动参数渲染得到的图像；
- $\hat{I}$：视频扩散模型生成的视频帧；
- $\|\cdot\|_2^2$：均方误差。

第一项为**关节投影损失**：约束优化后的 3D 关节投影应与估计器从生成帧中检测到的 2D 关节位置一致。第二项为**图像级损失**：直接比较渲染图像与生成帧的像素差异，提供更丰富的视觉监督信号。$\lambda_{img}$ 为图像损失权重。

**正则化项** $L_{reg}$ 包含两项约束，如公式 (4) 所示：

$$
L_{reg} = \lambda_{pos} \| P_j - P_{intp} \|_2^2 + \lambda_{rot} \| R_j - R_{prev} \|_2^2 \tag{4}
$$

- **位置正则化**（第一项）：鼓励每帧的根位置 $P_j$ 接近首尾关键帧的线性插值结果 $P_{intp}$，防止根位置漂移；
- **旋转正则化**（第二项）：鼓励相邻帧的关节旋转 $R_j$ 与 $R_{prev}$ 相似，确保运动平滑。

$\lambda_{pos}$ 和 $\lambda_{rot}$ 分别为位置和旋转正则化权重。优化过程以关键帧为起点，序贯优化根位置和关节旋转，通过梯度下降迭代更新直至收敛。

**优化流程** 整个运动-视频模仿优化采用序贯策略：先固定旋转优化根位置，再固定根位置优化旋转，交替进行直至损失收敛。这种分解策略降低了优化难度，提高了收敛稳定性。

![[assets/figures/papers/paper_list_l4_AnyMoLe_Any_Character_Motion_In_Betweening_Leveraging_Video_Diffusion_Mo/figures/002_Figure_2.jpg]]
*Figure 2: Overview of AnyMoLe: First, the video diffusion model is fine-tuned without using any external data (Sec. 3.1) while the scenespecific joint estimator is trained (Sec. 3.3.1). Next, the fine-tuned video generation model produces an in-between video (Sec. 3.2), which is then refined through motion video mimicking to generate the final in-between motion (Sec. 3.3)*

![[assets/figures/papers/paper_list_l4_AnyMoLe_Any_Character_Motion_In_Betweening_Leveraging_Video_Diffusion_Mo/figures/003_Figure_3.jpg]]
*Figure 3: Overview of the ICAdapt training process. The spatial module and image injection module are trained, while the others are frozen*

## 实验与关键发现

### 核心实验设置

AnyMoLe 在人类角色和非人类角色两个测试集上进行了系统评估。ICAdapt 微调阶段使用 500 步、批量大小 16；场景特定关节估计器 $E_{scene}$ 训练 3,500 步、批量大小 32。对比基线包括基于 Transformer 的运动插值方法 **TST** 和 **TS[33]**（Qin et al., TOG 2022）、基于扩散的运动生成方法 **SinMDM** 及其数据增强变体 **SinMDM\***、以及基于 VAE 运动先验的方法 **ERD-QV**。需要指出，所有基线方法均在各自角色特定数据集上预训练，而 AnyMoLe 仅使用 2 秒上下文样本进行推理阶段微调，属于极端少样本设置——这使得 AnyMoLe 在数据效率上具有天然劣势，但其性能仍大幅领先。

### 主实验结果

**定量评估**（Table 2）表明，AnyMoLe 在所有指标上均显著优于竞争方法。在核心指标 HL2Q（Higher Layer 2-norm Quaternion difference）上，AnyMoLe 在人类角色测试集上达到 **0.0015**，在非人类角色测试集上达到 **0.0019**，远低于最佳基线方法（具体数值原文未单独列出，但差距显著）。这一结果验证了视频扩散模型作为运动先验的有效性——即便不依赖任何角色特定训练数据，AnyMoLe 仍能生成与真值高度一致的中间帧运动。

**定性对比**（Figure 7）进一步揭示了基线方法的典型失败模式：SinMDM 和 SinMDM\* 在生成中间帧时出现上下文外运动（蓝色框标注），即运动内容与输入关键帧的语义不一致；TST 则产生部分上下文外脚步（蓝色框）和风格外运动（红色框），表现为运动风格与关键帧不匹配；ERD-QV 生成的运动风格偏离输入，表现为背部僵硬、手部位置尖锐（红色框）。相比之下，AnyMoLe 生成的中间帧与真值高度相似，忠实保持了输入关键帧的运动风格与语义。

**用户感知研究**（Table 4）从三个维度进行了主观评估：真值相似性、目标关键帧忠实度、运动自然度。在人类角色上，AnyMoLe 分别获得 **60.12%**、**63.10%**、**64.88%** 的偏好票数；在非人类角色上，这一优势更为显著，分别达到 **90.48%**、**92.46%**、**91.67%**。非人类角色上的压倒性优势凸显了 AnyMoLe 对任意骨架结构角色的泛化能力——这是传统方法无法实现的。

### 消融实验

消融实验（Table 3, Figure 8）系统验证了三个关键设计的作用：

![[assets/figures/papers/paper_list_l4_AnyMoLe_Any_Character_Motion_In_Betweening_Leveraging_Video_Diffusion_Mo/figures/010_Table_3.jpg]]
*Table 3: Quantitative results of ablation study*

![[assets/figures/papers/paper_list_l4_AnyMoLe_Any_Character_Motion_In_Betweening_Leveraging_Video_Diffusion_Mo/figures/009_Figure_8.jpg]]
*Figure 8: Ablation results on video generation. Without applying ICAdapt, each frame of the video exhibited inconsistencies, such as generating noticeable style shifts (blue box). Omitting the fine-stage process resulted in a low frame rate, making identical or significant jumps between frames*

1. **移除 ICAdapt**：视频帧间出现明显的风格漂移（蓝色框标注），导致 HL2Q、L2Q、L2P、NPSS、LPIPS、CLIP、SSIM 等所有定量指标下降。这证实 ICAdapt 的域适应能力是弥合真实-渲染域差距、保持视频风格一致性的必要条件。

2. **省略精细生成阶段**（仅用粗阶段）：导致帧率不足，帧间出现显著跳跃，运动不流畅。定量指标同样全面下降，表明两阶段生成（粗阶段建立运动结构 → 细阶段填充细节）对实现平滑运动过渡至关重要。

3. **用通用姿态检测器 XPose 替换场景特定关节估计器 $E_{scene}$**：除 NPSS 外所有指标下降，验证了场景特化关节估计的必要性——通用检测器无法适应特定角色的外观和骨架结构。

此外，消融还发现训练关节估计器时若包含后视图图像，会混淆左右信息，降低估计精度，表明视角选择对关节估计质量有直接影响。

### 失败模式与局限性

Figure 10 展示了 AnyMoLe 的典型失败案例：当角色执行快速转身等大幅运动时，视频扩散模型生成的帧可能出现模糊，导致关节估计器难以准确定位关节点，最终影响运动优化质量。这一失败模式揭示了当前方法的瓶颈——视频扩散模型对极端姿态变化的生成质量限制了后续 3D 运动提取的上限。

![[assets/figures/papers/paper_list_l4_AnyMoLe_Any_Character_Motion_In_Betweening_Leveraging_Video_Diffusion_Mo/figures/013_Figure_10.jpg]]
*Figure 10: Visualization of a generated frame from a fast turnaround, showing ambiguity that can hinder joint estimation*

更广泛的局限性包括：每个新角色仍需进行 ICAdapt 微调（约数分钟计算时间），无法实现即插即用；方法在角色正面视角下表现最佳，后视图或罕见视角可能降低性能；当前尚无对多角色交互场景的验证。

### 关键图表结论

- **Table 1**：系统对比了 AnyMoLe 与基线方法在训练数据需求、角色泛化性、域适应策略等维度的差异，明确了 AnyMoLe 的“零外部数据”定位。
- **Table 2**：AnyMoLe 在人类和非人类角色上均以大幅优势领先所有基线，HL2Q 指标降低至 0.0015–0.0019 量级。
- **Table 3**：ICAdapt 和精细生成阶段是两个不可替代的核心组件，移除任一项均导致全面性能退化。
- **Table 4**：用户研究证实 AnyMoLe 在相似性、忠实度、自然度三个主观维度上均获得最高偏好，非人类角色上的优势尤为突出（>90%）。
- **Figure 10**：快速转身场景下的模糊帧是当前方法的主要失败模式，为后续改进指明了方向。

![[assets/figures/papers/paper_list_l4_AnyMoLe_Any_Character_Motion_In_Betweening_Leveraging_Video_Diffusion_Mo/figures/008_Table_2.jpg]]
*Table 2: Quantitative results compared with the baselines. Ours outperformed all competitors with by margin*

## 定位与知识库关联

### 1. 问题瓶颈的重新定义

现有运动中间帧生成（motion in-betweening）方法的核心瓶颈并非模型架构的容量不足，而是**数据依赖的结构性缺陷**：主流方法（如两阶段Transformer、基于VAE的运动先验、扩散运动模型）均需在大量特定角色的动作捕捉或关键帧数据集上进行训练，这导致它们天然无法泛化到任意骨架结构的角色。当面对非人类角色（如动物、幻想生物）、无法进行动作捕捉的角色，或仅有极少关键帧样本的场景时，这些方法完全失效。AnyMoLe通过将问题从“学习特定角色的运动流形”重新定义为“利用通用视觉世界中的运动过渡知识”，从根本上绕过了这一瓶颈。

### 2. 与基线方法的关系与差异

AnyMoLe与现有方法的本质差异体现在三个维度上（见表1），以下逐一剖析其与代表性基线的具体关系：

**（1）训练数据范式：从角色特定数据集到零外部数据**

- **TS[33]**（Qin et al., TOG 2022）作为两阶段Transformer运动插值方法的代表，需要大规模人类运动捕捉数据集进行训练，其运动先验完全内嵌于特定骨架结构，无法迁移至任意角色。AnyMoLe则完全不需要任何外部训练数据，仅利用预训练视频扩散模型（DynamiCrafter）中已蕴含的运动过渡知识。
- **SinMDM** 和 **SinMDM\*** 是基于扩散的运动生成方法，在实验中作为零样本微调基线进行对比。SinMDM\*使用了更多的训练数据，但两者均依赖角色特定的运动数据分布。实验结果显示（Figure 7），SinMDM和SinMDM\*生成的中间帧运动脱离了上下文风格（蓝色框标注），而AnyMoLe则忠实保持了输入关键帧的风格。

**（2）域适应策略：从无适配到推理阶段上下文自适应**

- 传统方法直接在角色特定数据上训练模型，不存在域适应环节。AnyMoLe提出**ICAdapt（Inference-stage Context Adaptation）**，在推理阶段仅使用一段2秒的上下文运动渲染视频，对预训练视频扩散模型的空间模块和图像投影器进行微调（约500步），同时冻结时间模块以保留从真实视频中学到的运动动力学知识。这一策略弥合了真实视频与渲染角色之间的域差距，是使通用视频扩散模型适用于任意渲染角色的关键机制。

**（3）运动生成流程：从直接3D预测到视频-运动模仿优化**

- **TST**（两阶段Transformer）和**ERD-QV**（基于VAE的运动先验）等方法直接使用神经网络预测3D运动序列。Figure 7显示，TST生成的运动部分偏离了上下文的脚步轨迹（蓝色框）且风格不一致（红色框），ERD-QV则产生僵硬的后背和尖锐的手部姿态。
- AnyMoLe采用**两阶段视频生成→运动-视频模仿优化**的间接路径：先在2D视频空间中生成平滑过渡，再利用可微渲染器和场景特定关节估计器将2D视频提升为3D运动。这种设计将运动生成的“创意”部分委托给具有丰富视觉先验的视频扩散模型，而将“精确性”部分交给基于物理渲染的优化过程，实现了泛化性与精确性的解耦。

### 3. 适用边界与局限性

AnyMoLe虽然实现了对任意角色的零数据运动插值，但其适用边界受以下因素约束：

- **运动幅度限制**：当角色执行快速转身等大幅运动时，视频扩散模型可能生成模糊帧，导致后续关节估计器失效。Figure 10展示了这一失败案例，模糊的渲染帧使3D关节估计产生歧义。
- **视角敏感性**：方法在角色正面视角下表现最佳。消融实验表明（Sec 3.3.1），若在训练关节估计器时包含后视图图像，会混淆左右信息，降低估计精度。这意味着对于包含大量后视图或罕见视角的场景，性能可能下降。
- **计算开销**：尽管无需外部训练数据，但每个新角色仍需进行ICAdapt微调（500步，batch size 16）和场景特定关节估计器训练（3,500步，batch size 32），总耗时约数分钟，尚不适合实时应用场景。
- **角色交互缺失**：当前方法针对单角色设计，未考虑多角色场景中的物理约束（如接触、碰撞）。Figure 9虽展示了多对象场景的应用，但这是基于视频扩散模型对上下文的隐式理解，而非显式的物理建模。

### 4. 开放问题与未来方向

AnyMoLe的开创性在于打开了“利用通用视觉先验解决角色运动生成”这一新范式，但以下问题仍有待探索：

**（1）极端姿态变化下的生成稳定性**：两阶段自回归生成过程中，当上下文运动与目标关键帧之间存在极大姿态变化或语义不一致时，视频扩散模型能否保持连贯过渡？当前方法依赖上下文帧引导的潜在空间修复（latent inpainting）来维持一致性，但其在极端情况下的鲁棒性边界尚未被系统刻画。

**（2）通用3D关节估计器的可行性**：当前每个新角色都需要训练专用的场景特定关节估计器E_scene，这增加了部署成本。是否可能预训练一个与角色无关的通用3D关节估计器，使其能够跨角色泛化？这需要解决不同骨架结构之间的对应问题，以及渲染风格差异带来的域偏移。

**（3）多角色交互与物理合理性**：AnyMoLe的视频扩散模型隐式地学习了运动过渡知识，但缺乏显式的物理约束。扩展到多角色交互场景时，需要保证角色间的接触约束、碰撞避免和时序同步。这可能需要在运动-视频模仿优化阶段引入额外的物理损失项，或利用物理仿真器进行后处理修正。

**（4）推理效率优化**：当前方法的推理延迟主要来自ICAdapt微调、两阶段视频生成和序列优化三个环节。探索更轻量级的视频扩散模型（如蒸馏版本）、减少微调步数、或设计更高效的优化算法，将有助于将AnyMoLe推向实时动画工作流。

## 原文 PDF

![[paperPDFs/CVPR_2025/AnyMoLe_Any_Character_Motion_In_Betweening_Leveraging_Video_Diffusion_Models.pdf]]
