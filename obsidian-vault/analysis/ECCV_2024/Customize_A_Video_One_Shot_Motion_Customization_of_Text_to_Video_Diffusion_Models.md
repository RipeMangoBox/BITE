---
title: "Customize-A-Video: One-Shot Motion Customization of Text-to-Video Diffusion Models"
type: paper
paper_level: A
venue: ECCV
year: 2024
pdf_ref: paperPDFs/ECCV_2024/Customize_A_Video_One_Shot_Motion_Customization_of_Text_to_Video_Diffusion_Models.pdf
aliases:
- CV
- Customize-A-Video
tags:
- ECCV_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: "在预训练文本到视频扩散模型的所有时间交叉帧注意力层上注入低秩适配（Temporal LoRA），并引入外观吸收器（Appearance Absorbers）分阶段训练以吸收并剥离空间外观，使T-LoRA专注于运动建模。"
primary_logic: "通过将空间外观吸收与时间运动学习解耦，即使在只有一个参考视频的条件下，也能实现既忠实于原始运动又能在新场景中产生丰富多样变化的一次性运动定制。"
claims:
- "仅将LoRA应用于时间注意力层能显著提升运动建模质量，优于在空间注意力层上应用LoRA。"
- "外观吸收器（尤其是双吸收器）有效地分解了空间信息，使得生成的视频既保留了目标运动，又清晰展现了新主体和背景。"
- "在用户研究中，带有双外观吸收器的方法在运动保真度和运动多样性上均显著优于基线方法（Fidelity: 3.72, Diversity: 3.72）。"
- "在定量基准上，我们的方法在文本对齐和时序一致性上超过了所有对比方法，同时提供了更高的多样性。"
---

# Customize-A-Video: One-Shot Motion Customization of Text-to-Video Diffusion Models

> [!tip] 核心洞察
> 通过将空间外观吸收与时间运动学习解耦，即使在只有一个参考视频的条件下，也能实现既忠实于原始运动又能在新场景中产生丰富多样变化的一次性运动定制。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Customize-A-Video：面向文本到视频扩散模型的一次性运动定制 |
| 英文题名 | Customize-A-Video: One-Shot Motion Customization of Text-to-Video Diffusion Models |
| 会议/期刊 | ECCV 2024 |
| Links | [paper](https://arxiv.org/abs/2402.14780); [Project](https://customize-a-video.github.io) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Customize-A-Video |
| Dataset | LOVEU-TGVE-2023 subset (53 videos) |

> [!tip] 效果简介
> - LOVEU-TGVE-2023 subset (53 videos) 上，Text Alignment (CLIPScore) ↑ 为 32.632 (Ours TextInv AA)，对比 32.500 (MotionDirector LoRA rank 4)，变化 +0.132。
> - LOVEU-TGVE-2023 subset (53 videos) 上，Temporal Consistency (LPIPS) ↓ 为 0.160 (Ours TextInv AA)，对比 0.163 (MotionDirector LoRA rank 4)，变化 -0.003。
> - LOVEU-TGVE-2023 subset (53 videos) 上，Diversity (LPIPS) ↑ 为 0.631 (Ours Both AA)，对比 0.606 (MotionDirector LoRA rank 4)，变化 +0.025。

## 概述

**核心问题**：现有文本到视频（T2V）扩散模型的运动定制方法面临一个根本性瓶颈——从单个参考视频中难以解耦空间外观与运动信息。基于DDIM反转的方法（如 **Tune-A-Video** 和 **Video-P2P**）虽然能保留运动，但生成结果固守原始帧结构与布局，缺乏帧间多样性；而并发工作 **MotionDirector** 在联合训练空间与时间LoRA时，外观信息容易泄漏到运动模块中，影响对新主体的适应能力。仅靠提示工程驱动预训练模型（如 **ModelScope**）则无法精确控制运动模式。

**核心方法**：**Customize-A-Video** 通过两个关键设计解决上述解耦难题：

1. **Temporal LoRA（T-LoRA）**：仅在预训练T2V模型的所有时间交叉帧注意力层上注入低秩适配，使参数更新专注于运动建模，而非空间外观。
2. **外观吸收器（Appearance Absorbers）**：在无序视频帧上预训练空间信息吸收模块（如S-LoRA、文本倒置），分阶段剥离参考视频的身份、纹理、场景等静态信号，确保T-LoRA阶段学习的运动信号纯净。

两阶段训练流程（先训练并冻结外观吸收器，再训练T-LoRA）实现了空间外观与时间运动的显式解耦，推理时仅加载T-LoRA即可在新主体上复现目标运动。

**核心结论**：
- 在LOVEU-TGVE-2023数据集子集（53个视频）上，配备双外观吸收器的方法在文本对齐（CLIPScore 32.193）和时序一致性（LPIPS 0.631）上均优于对比基线，同时提供更高的多样性（LPIPS 0.631）。
- 用户研究中，双外观吸收器配置在运动保真度（3.72/5）和运动多样性（3.72/5）上显著领先。
- 消融实验证实：仅将LoRA应用于时间注意力层是运动建模质量的关键；外观吸收器（尤其是双吸收器组合）能最大程度剥离原始外观，使T-LoRA专注于运动。

**方法定位**：该方法属于基于预训练T2V扩散模型的一次性运动定制范式，通过参数高效微调（LoRA）和分阶段解耦训练，在单参考视频条件下实现运动迁移。其即插即用设计支持与现有图像定制方法（如Dreambooth）及多运动组合的灵活集成。

## 背景与动机

### 文本到视频生成与运动定制的困境

近年来，基于扩散模型的文本到视频（Text-to-Video, T2V）生成取得了显著进展，用户只需提供一段文本描述即可获得一段视频。然而，单纯的文本提示难以精确控制视频中的运动模式——比如让一个角色做出特定的舞蹈动作、或让摄像机以特定的轨迹运镜。这催生了“运动定制”（Motion Customization）的需求：给定一个参考视频，将其中的运动模式提取出来，并迁移到由新文本描述的新主体、新场景中。

这一任务的核心瓶颈在于**空间外观与时间运动的解耦**。参考视频同时包含了静态的外观信息（如人物身份、衣着、背景纹理）和动态的运动信息（如肢体动作、摄像机运动）。理想的运动定制应当只提取后者，而完全剥离前者，从而在推理时能自由替换新外观。

### 现有方法的缺口

现有的视频编辑与定制方法在面对这一瓶颈时，存在两类典型缺陷：

**第一类方法**，如 **Tune-A-Video** 和 **Video-P2P**，通过对单视频进行微调或利用DDIM反演（DDIM Inversion）来保持原视频的结构。这类方法虽然在时序一致性上表现良好，但其生成结果**固守于原始视频的帧结构和布局**，缺乏帧间的多样性——例如无法改变视角、背景或主体的空间位置，本质上是对原视频的“重绘”而非“运动迁移”。

**第二类方法**，如并发工作 **MotionDirector**，尝试通过双路径LoRA联合训练来分别学习空间和时间信息。然而，由于空间路径与时间路径在训练中相互耦合，**外观信息容易泄漏到运动模块中**，导致生成结果中残留原视频的外观特征，或在新主体上产生运动伪影。

此外，直接使用预训练T2V模型（如 **ModelScope**）配合精心设计的提示词，也无法忠实复现参考视频中的特定运动模式——文本对运动的描述能力天然有限。

### 本文的核心思路

本文提出 **Customize-A-Video**，其核心洞察在于：**将空间外观吸收与时间运动学习彻底解耦**，即使在只有一个参考视频的极端条件下，也能实现既忠实于原始运动、又能在新场景中产生丰富多样变化的一次性运动定制。

为实现这一目标，方法引入了两个关键组件：

1. **时间LoRA（Temporal LoRA, T-LoRA）**：仅在预训练T2V模型的所有时间交叉帧注意力层上注入低秩适配，使其专注于学习运动模式，而避免被空间信息干扰。
2. **外观吸收器（Appearance Absorbers）**：在T-LoRA训练之前，先通过一个独立的阶段，利用空间LoRA（S-LoRA）或文本倒置（Textual Inversion）在无序帧上吸收并剥离参考视频的空间外观信息，使后续的T-LoRA训练能够在“纯净”的运动信号上进行。

通过这种分阶段的训练策略，Customize-A-Video在运动保真度与生成多样性之间取得了突破性平衡，支持将同一运动迁移到不同主体、组合多个运动模式，甚至与现有的图像定制方法协同工作。

## 核心创新

### 问题瓶颈

现有视频编辑与运动定制方法面临一个根本性困境：从单个参考视频中解耦空间外观与运动信息极为困难。基于单视频微调的方法（如 **Tune-A-Video**）通过附加时间层实现运动转移，但生成结果固守原始帧结构与布局，缺乏帧间多样性；基于 DDIM 反转的方法（如 **Video-P2P**）输出确定性结果，缺少视角变化。并发工作 **MotionDirector** 虽引入双路径 LoRA 联合训练，但空间外观信息容易泄漏到时间模块中，影响对新主体的适应能力。核心瓶颈在于：运动建模与外观建模在参数空间中耦合，导致运动转移时要么多样性不足，要么外观信息污染运动表征。

### 关键创新：因果调控旋钮

Customize-A-Video 的核心创新在于通过**分阶段解耦训练**，将空间外观吸收与时间运动学习彻底分离。该设计包含两个相互配合的 changed slots：

**1. 运动学习参数注入位置（Temporal LoRA）**

与在空间和时间注意力层上均应用 LoRA 或全参数微调的基线策略不同，本方法**仅在所有时间交叉帧注意力层上注入低秩适配（T-LoRA）**。这一设计选择基于一个关键洞察：时间交叉帧注意力层是视频扩散模型中运动信号建模的核心载体，将 LoRA 限定于此可最大化运动建模能力，同时避免空间注意力层上的参数更新引入外观记忆。消融实验（Fig. 4 左）直接验证了该选择的因果效应：在空间注意力层上额外添加 S-LoRA 会严重干扰运动建模，导致生成结果保留大量原始室内家具和墙面装饰；而仅使用 T-LoRA 则能将画作转换为入口、沙发转换为泳池长椅，实现清晰的空间重构。

**2. 外观信息解耦策略（Appearance Absorbers）**

基线方法通常缺乏专门的外观吸收模块，或依赖额外的多样性数据与损失函数来间接缓解外观泄漏。本方法引入**外观吸收器**（包括 S-LoRA、文本倒置 Token 及二者的组合），在**第一阶段**于无序帧上训练，以外观描述文本为条件，主动吸收参考视频中的身份、纹理、场景等空间信息；训练完成后冻结吸收器参数。在**第二阶段**，T-LoRA 在完整视频序列上以完整文本标签进行训练，此时外观信息已被剥离，T-LoRA 可专注于运动模式学习。推理时仅加载 T-LoRA，外观吸收器被完全丢弃，从而实现纯净的运动迁移。

消融实验（Fig. 4 右）揭示了外观吸收器的因果贡献：不使用任何吸收器（No AA）时，T-LoRA 仍会学习到部分空间信息（如添加时尚眼镜和 Logo 但保留大部分原始外观）；引入 S-LoRA 或文本倒置单一吸收器能显著提升质量，但仍存在墙面条纹或部分白色袖管等外观残留；双吸收器（Dual AA）组合达到最佳空间清除效果，新主体服装和背景清晰呈现。附录实验进一步表明，在无序帧上使用裁剪训练（patch training，最优裁剪比例 0.33–0.67）可防止外观吸收器过拟合于全局结构，增强第二阶段运动学习的稳定性。

### 核心洞察

上述两个 changed slots 共同实现了一个简洁而强大的因果机制：**通过将空间外观吸收与时间运动学习在训练阶段解耦，即使在只有一个参考视频的条件下，T-LoRA 也能学习到纯净的运动表征，在推理时与任意新外观文本提示结合，生成既忠实于原始运动又具备丰富多样变化的视频。** 定量证据支持这一洞察：在 LOVEU-TGVE-2023 子集（53 个视频）上，带有文本倒置外观吸收器的配置在文本对齐（CLIPScore 32.632）和时序一致性（LPIPS 0.160）上均优于 MotionDirector；用户研究中，双吸收器配置在运动保真度（3.72/5）和运动多样性（3.72/5）上均显著领先。

## 整体框架

![[assets/figures/papers/paper_list_l39_Customize_A_Video_One_Shot_Motion_Customization_of_Text_to_Video_Diffusi/figures/011_Figure_8.jpg]]
*Figure 8: Additional generation results of our method*

Customize-A-Video 的核心目标是从**单个参考视频**中提取运动模式，并将其迁移到由文本提示指定的新外观上。为实现这一目标，该方法设计了一套**两阶段训练、单阶段推理**的管线，其关键在于将空间外观信息与时间运动信息彻底解耦。

### 管线总览

整个框架围绕一个**冻结的预训练文本到视频（T2V）扩散模型**（ModelScope）构建，通过注入两类低秩适配模块来实现功能扩展。如 Fig. 2 所示，管线分为三个核心阶段：

1.  **第一阶段：外观吸收器训练**
    在此阶段，基础 T2V 模型的**所有时间层被旁路**，模型退化为逐帧图像生成器。在无序排列的参考视频帧上训练**外观吸收器**，使其专门吸收并建模参考视频中的空间信息（如主体身份、纹理、场景布局）。训练完成后，外观吸收器的权重被冻结。

2.  **第二阶段：时间 LoRA 训练**
    恢复完整 T2V 模型的时间层，并在**所有时间交叉帧注意力层**上注入**时间 LoRA（T-LoRA）**。此时，第一阶段训练好的外观吸收器被加载并保持冻结状态。T-LoRA 在完整的参考视频序列上进行训练，由于空间信息已被外观吸收器剥离，T-LoRA 能够专注于学习纯粹的运动模式。

3.  **推理阶段**
    仅将训练好的 T-LoRA 加载到基础 T2V 模型上，外观吸收器被完全丢弃。用户提供一个描述新外观和所需运动的文本提示，模型即可生成既忠实于参考视频运动、又具备全新外观和丰富多样性的视频。

### 核心模块与交互关系

管线的有效性建立在两个互补模块的协同作用上：

-   **外观吸收器**：其任务是“吸收”并带走参考视频的空间外观信号。论文探索了两种具体形式：**空间 LoRA（S-LoRA）** 和**文本倒置**。S-LoRA 在空间注意力层上注入低秩残差权重，而文本倒置则学习一个新的文本令牌嵌入。两者均在无序帧上训练，以确保学习到的空间特征与运动无关。最终，**双吸收器**（同时使用 S-LoRA 和文本倒置）被证明能最彻底地剥离原始外观，为 T-LoRA 提供最“纯净”的运动信号。

-   **时间 LoRA**：这是运动定制能力的直接载体。通过在时间交叉帧注意力层上添加低秩残差矩阵 $\Delta \theta_T$，T-LoRA 能够高效地捕获帧间的动态变化。其训练目标是在冻结外观吸收器的前提下，最小化完整视频序列的重建损失：
    $$L_{\Delta \theta_T} = \mathbb{E}_{x^{1...F}, \epsilon, t} [ \| \epsilon - \epsilon_{\theta' + \Delta \theta_T}(x_t^{1...F}, t, \tau_{v'}(y)) \| ]$$
    其中 $\theta'$ 和 $v'$ 分别代表已加载并冻结的外观吸收器权重和文本嵌入。由于 T-LoRA 以残差形式作用于原始时间层，推理时可以通过**加载多个不同的 T-LoRA 模块**来实现多运动组合（如 Fig. 5 所示），展现出高度的灵活性。

### 输入输出流

-   **输入**：一段单主体参考视频，以及推理时用于描述新外观和运动的文本提示。
-   **第一阶段数据流**：参考视频 → 无序帧 → 旁路时间层的基础模型 → 训练外观吸收器（S-LoRA / 文本倒置）。
-   **第二阶段数据流**：参考视频序列 → 完整基础模型（加载并冻结外观吸收器）→ 训练 T-LoRA。
-   **推理数据流**：随机噪声 + 文本提示 → 基础模型（仅加载 T-LoRA）→ 生成定制运动的新视频。
-   **输出**：一段包含目标运动、但具备全新外观和帧间多样性的视频。

该框架的核心洞见在于**通过分阶段训练实现空间与时间信号的因果解耦**。消融实验（Fig. 4）强有力地证实了这一点：若在空间注意力层上额外添加 LoRA，会严重干扰运动建模，导致生成结果保留大量原始外观；而完全不使用外观吸收器时，T-LoRA 仍会学习到部分空间信息，限制了新外观的生成能力。

## 核心模块与公式推导

### 基础模型与扩散损失

本方法建立在预训练文本到视频（T2V）扩散模型之上，采用3D UNet架构进行视频去噪。给定一段包含 $F$ 帧的视频 $x^{1...F}$，模型通过以下损失函数学习预测噪声：

$$L_{\theta} = \mathbb{E}_{x^{1...F}, \epsilon, t} [\| \epsilon - \epsilon_{\theta}(x_t^{1...F}, t, \tau_v(y)) \|]$$

其中 $\epsilon$ 为真实噪声，$\epsilon_{\theta}$ 为3D UNet的噪声预测，$t$ 为时间步，$\tau_v(y)$ 为文本提示 $y$ 的编码嵌入。该损失函数源自标准视频扩散训练范式（Eq. 1, Sec. 3.1）。

### 低秩适配（LoRA）机制

在注意力层上引入低秩适配，通过残差方式更新权重而不改变原始模型参数。其前向路径为：

$$\theta = \theta_0 + \alpha \Delta \theta = \theta_0 + \alpha \theta_B \theta_A$$

其中 $\theta_0$ 为冻结的原始权重，$\Delta \theta = \theta_B \theta_A$ 为低秩分解的可训练残差矩阵，$\alpha$ 为缩放系数。该公式为后续所有LoRA变体的数学基础（Eq. 2, Sec. 3.1）。

### 外观吸收器：空间信息解耦

外观吸收器的核心目标是在无序视频帧上剥离空间外观信息（身份、纹理、场景），使运动信号纯净地保留给后续的时间模块。论文提出两种互补的实现形式。

**空间LoRA（S-LoRA）** 在绕过所有时间层的T2V模型上训练，以外观描述 $y_S$ 为条件，在单帧 $x^f$ 上进行去噪：

$$L_{\Delta \theta_S} = \mathbb{E}_{x, \epsilon, t} [\| \epsilon - \epsilon_{\theta_0 + \Delta \theta_S}(x_t^f, t, \tau_{v_0}(y_S)) \|]$$

其中 $\Delta \theta_S$ 为注入空间注意力层的低秩残差，$v_0$ 为原始文本编码器参数（Eq. 3, Sec. 3.2）。

**文本倒置（Textual Inversion）** 则冻结UNet权重，仅优化文本编码器中的特殊令牌嵌入 $\Delta v$：

$$L_{\Delta v} = \mathbb{E}_{x, \epsilon, t} [\| \epsilon - \epsilon_{\theta_0}(x_t^f, t, \tau_{v_0 + \Delta v}(y_S)) \|]$$

该损失同样在无序帧上以外观描述为条件进行训练（Eq. 4, Sec. 3.2）。

### 时间LoRA（T-LoRA）：运动建模

在完成外观吸收器训练并冻结其参数后，第二阶段在完整视频序列上训练T-LoRA。此时基础模型权重更新为 $\theta' = \theta_0 + \Delta \theta_S$（若使用S-LoRA），文本编码器更新为 $v' = v_0 + \Delta v$（若使用文本倒置）。T-LoRA在所有时间交叉帧注意力层上注入低秩残差 $\Delta \theta_T$，训练目标为：

$$L_{\Delta \theta_T} = \mathbb{E}_{x^{1...F}, \epsilon, t} [\| \epsilon - \epsilon_{\theta' + \Delta \theta_T}(x_t^{1...F}, t, \tau_{v'}(y)) \|]$$

其中 $y$ 为完整的视频描述标签（包含运动和外观信息）。该损失确保T-LoRA在已剥离外观的模型上专注于学习时序运动模式（Eq. 5, Sec. 3.2）。

### 关键设计决策

**注入位置选择**：消融实验证实，仅在时间交叉帧注意力层上应用LoRA（即T-LoRA）是运动建模质量的关键。若在空间注意力层上额外添加S-LoRA，会严重干扰运动学习——S-LoRA会记忆室内家具和墙面装饰等静态外观，导致T-LoRA将画作转化为入口、沙发转化为泳池长椅（Fig. 4左, Sec. 4.2）。

**双吸收器协同**：S-LoRA擅长捕获局部纹理细节，文本倒置擅长语义层面的外观表征。两者组合（Dual AA）达到最佳的空间清除效果，生成的视频同时清晰展现新主体和背景，在用户研究中运动保真度与多样性均达3.72分（Table 2, Sec. 4.1）。

**无序帧训练与裁剪策略**：外观吸收器在绕过时间层的无序帧上训练，本质退化为图像生成任务。为防止过拟合全局结构，采用裁剪训练（patch training），将帧随机裁剪为局部块，最优裁剪比例在0.33至0.67之间（Appendix A.2）。

## 实验与分析

### 核心实验设置

所有实验基于预训练文本到视频扩散模型 **ModelScope** 构建，评估在 LOVEU-TGVE-2023 数据集的 53 个视频子集上进行。对比方法包括 **Tune-A-Video**（单视频微调 T2I 模型附加时间层）、**Video-P2P**（基于 DDIM 反转的精确编辑）以及并发工作 **MotionDirector**（双路径 LoRA 联合训练）。为确保公平，与 MotionDirector 的对比采用相同的 LoRA 秩（4）、学习率等超参数配置。

### 定量评估

**Table 1** 展示了各方法在文本对齐（CLIPScore ↑）、时序一致性（LPIPS ↓）和多样性（LPIPS ↑）三个维度上的表现。本方法采用文本倒置外观吸收器的配置（Ours TextInv AA）在文本对齐上达到 32.632，时序一致性为 0.621，均优于所有对比方法。采用双外观吸收器的配置（Ours Both AA）在多样性上取得 0.631，显著高于 MotionDirector 的 0.606。与并发工作 MotionDirector 的专项对比见 **Table 3**，本方法在参数量相当的条件下，三个指标均保持领先。

![[assets/figures/papers/paper_list_l39_Customize_A_Video_One_Shot_Motion_Customization_of_Text_to_Video_Diffusi/figures/004_Table_1.jpg]]
*Table 1: Quantitative comparisons on [51] dataset. ∼ w/o DDIM Inversion represents the above method without DDIM inverted latent input. Video-P2P outputs video clips of 4 FPS with 512 × 512 resolution. MotionDirector is a concurrent work to ours and is tested with either the same LoRA rank or comparable amount of parameters to ours*

![[assets/figures/papers/paper_list_l39_Customize_A_Video_One_Shot_Motion_Customization_of_Text_to_Video_Diffusi/figures/010_Table_3.jpg]]
*Table 3: Quantitative and model size comparison with concurrent work*

**Table 2** 的用户研究结果进一步验证了上述结论：在运动保真度和运动多样性两个维度上，带有双外观吸收器的方法均获得 3.72 分（1–5 星制），显著高于 Tune-A-Video（保真度 2.18，多样性 1.79）和 MotionDirector（保真度 3.14，多样性 3.31）。

![[assets/figures/papers/paper_list_l39_Customize_A_Video_One_Shot_Motion_Customization_of_Text_to_Video_Diffusi/figures/005_Table_2.jpg]]
*Table 2: Human user study results on [51] dataset. Methods are evaluated from 1 (worst) to 5 (best) stars on each benchmark*

### 定性对比

**Figure 3** 展示了各方法的生成示例。仅凭文本引导的 ModelScope 无法忠实复现参考运动；Tune-A-Video 和 Video-P2P 依赖 DDIM 反转潜在输入，输出确定性复制原始帧结构，缺乏视角和布局变化。MotionDirector 虽能产生多样输出，但在复杂或剧烈运动场景下存在外观伪影和运动失真。本方法在运动准确性与细节多样性（视角、帧布局）之间取得了更好的平衡。

### 消融实验

消融实验围绕两个关键设计展开（**Figure 4**）：

**LoRA 注入位置的影响**（Figure 4 左）：在空间注意力层上额外添加 S-LoRA 会严重干扰运动建模——S-LoRA 倾向于记忆室内家具和墙面装饰，而 T-LoRA 则将画作转换为入口、沙发转换为泳池长凳。仅将 LoRA 应用于时间交叉帧注意力层（即 T-LoRA）能够最大化运动信号的建模质量。

**外观吸收器类型的影响**（Figure 4 右）：不使用任何外观吸收器（No AA）时，T-LoRA 仍会学习到部分空间信息（如添加时尚眼镜和标志），但保留了大部分原始外观。单独使用 S-LoRA 或文本倒置（TextInv AA）显著提升生成质量，但仍存在墙面条纹和袖口部分发白等残留问题。双吸收器（Dual AA）联合两者的优势，实现了最佳的空间信息剥离效果，新主体服装和背景清晰呈现。

**附录 A.2** 进一步揭示了裁剪训练（patch training）对防止外观吸收器过拟合于全局结构的关键作用：在无序帧上随机裁剪比例设为 0.33 至 0.67 之间时效果最优，能够在第二阶段训练中有效保留目标运动。

### 失败模式与局限性

尽管方法在整体上表现优异，但仍存在以下局限：

1. **逐视频微调成本**：每个新的参考视频都需要独立的微调过程，超参数和迭代步数依赖于具体视频内容。简单运动（如相机移动）收敛较快，复杂动作（如动物或人类行为）则需要更多调优步数（**Figure 10**），存在欠拟合与过拟合的权衡。

2. **空间域偏移风险**：当参考视频的外观过于独特或超出基础 T2V 模型的泛化范围时，外观吸收器的微调可能引起空间域偏移，影响后续 T-LoRA 阶段的解析能力。

3. **文本令牌映射冲突**：部分外观定制模块（如改动文本编码器的方案）可能与 T-LoRA 在推理时产生文本令牌映射冲突，导致运动定制未被正确触发。

4. **分辨率与时域限制**：当前模型针对 256×256 分辨率和 2 秒短视频训练，长时域、高分辨率的扩展尚未验证。在复杂运动、长视频和相机剧烈运动场景下，运动保真度与外观一致性的平衡仍是开放问题。

### 扩展应用验证

**Figure 5** 展示了两个扩展应用场景：左侧将 T-LoRA 与已有的预训练 S-LoRA 结合，实现外观与运动的双重定制；右侧同时加载两个 T-LoRA 模块（慢跑 + 推拉变焦），验证了残差连接设计使多运动组合成为可能。**Figure 6** 进一步验证了与 DDIM 反转结合的精确帧级编辑，以及使用第三方 Dreambooth UNet 作为外观吸收器的兼容性，表明方法具有良好的模块化扩展能力。

### 补充图表

![[assets/figures/papers/paper_list_l39_Customize_A_Video_One_Shot_Motion_Customization_of_Text_to_Video_Diffusi/figures/015_Figure.jpg]]
*Figure: B*

![[assets/figures/papers/paper_list_l39_Customize_A_Video_One_Shot_Motion_Customization_of_Text_to_Video_Diffusi/figures/016_Figure.jpg]]
*Figure: C D*

![[assets/figures/papers/paper_list_l39_Customize_A_Video_One_Shot_Motion_Customization_of_Text_to_Video_Diffusi/figures/018_Figure_12.jpg]]
*Figure 12: An example question in the human user study. Participants are asked to rate each algorithm’s output videos from 1 to 5 stars*

## 方法谱系与知识库定位

### 核心瓶颈与设计动机

当前文本到视频（T2V）扩散模型的一次性运动定制面临一个关键瓶颈：从单个参考视频中解耦空间外观与运动信息极为困难。现有方法在处理这一解耦任务时，普遍存在两类失败模式。

- **空间-运动信息纠缠**：**Tune-A-Video** 等基于单视频微调的方法虽然通过附加时间层实现了运动转移，但其依赖 DDIM 反转潜在输入，导致输出固守原始帧的结构与布局，缺乏帧间多样性。**Video-P2P** 同样因使用 DDIM 反转而输出确定性结果，缺少视角变化。
- **外观泄漏**：并发工作 **MotionDirector** 采用双路径 LoRA 联合训练空间与时间模块，但由于空间路径在时间模块训练时同时被调优，参考视频的外观信息容易泄漏到运动模块中，影响对新主体外观的适应能力。仅依赖文本提示的 **ModelScope** 原生 T2V 模型则无法精确控制运动模式。

Customize-A-Video 的核心洞察在于：**将空间外观吸收与时间运动学习解耦为两个独立阶段**，即使在只有一个参考视频的条件下，也能实现既忠实于原始运动又能在新场景中产生丰富多样变化的一次性运动定制。

### 方法演进与关键改进

Customize-A-Video 在预训练 T2V 扩散模型（基于 ModelScope）的基础上，引入了两个关键改进，形成清晰的“吸收-建模”两阶段范式。

| 改进维度 | 基线做法 | 本方法 | 因果机制 |
|----------|----------|--------|----------|
| 运动学习参数注入位置 | 在空间和时间注意力层上均应用 LoRA，或全参数微调 | **仅在所有时间交叉帧注意力层上注入 T-LoRA** | 避免空间层学习外观信息，使 LoRA 残差专注于跨帧运动模式的建模 |
| 外观信息解耦策略 | 无专门外观吸收模块，或依赖额外多样性数据/损失函数 | **引入外观吸收器（S-LoRA / 文本倒置），分阶段吸收空间信息** | 在无序帧上训练吸收器以捕获身份、纹理、场景等静态信号，使 T-LoRA 阶段不受外观干扰 |
| 训练流程 | 单阶段联合训练时间与空间模块 | **两阶段训练：先训练并冻结外观吸收器，再训练 T-LoRA** | 阶段一剥离空间信息，阶段二在“纯净”运动信号上学习，推理时仅加载 T-LoRA |

具体而言，第一阶段将预训练 T2V 模型的所有时间层旁路，在空间注意力层上训练外观吸收器（S-LoRA 或文本倒置），以外观描述为条件在无序帧上进行去噪。为防止吸收器过拟合于全局结构，采用裁剪训练（patch training），最优裁剪比例在 0.33–0.67 之间。第二阶段冻结外观吸收器，在完整视频序列的所有时间交叉帧注意力层上注入 T-LoRA，以完整视频标签为条件学习运动模式。推理时仅加载 T-LoRA，通过新的文本提示即可生成具有目标运动的新主体视频。

### 知识库定位与适用边界

**适用场景**：
- 从单个参考视频中提取运动模式，并转移至全新的主体和场景
- 多运动组合：利用 T-LoRA 的残差连接特性，同时加载多个 T-LoRA 模块实现复合运动（如慢跑 + 推拉变焦）
- 与现有图像定制方法（如 DreamBooth）结合，实现外观与运动的双重定制
- 与 DDIM 反转结合，支持精确的帧级视频编辑

**已知局限**：
- 每个新参考视频需要独立的微调过程，调优超参数和迭代步数依赖于具体视频内容，简单运动（如相机移动）收敛较快，复杂动作（如人体或动物运动）需更多步数
- 当参考视频的外观过于独特或超出基础 T2V 模型的泛化范围时，外观吸收器的微调可能引起空间域偏移，影响后续 T-LoRA 阶段的解析能力
- 部分外观定制模块（如改动文本编码器）可能与 T-LoRA 在推理时产生文本令牌映射冲突，导致运动定制未被正确触发
- 当前模型针对低分辨率（256×256）和 2 秒短视频训练，长时域、高分辨率的扩展尚未验证

**开放问题**：
- 如何探索更多类型的外观吸收器（如图像定制方法），利用不同机制的特性进一步增强运动定制的性能和灵活性
- 如何使方法更好地兼容快速演进的新一代视频生成基础模型，支持更多样的时间注意力形式
- 能否设计自动化的调优策略，根据视频内容自适应确定最优训练轮数，减少手动调整需求
- 在复杂运动、长视频和相机剧烈运动场景下，如何保持运动保真度和外观一致性的平衡

## 原文 PDF

![[paperPDFs/ECCV_2024/Customize_A_Video_One_Shot_Motion_Customization_of_Text_to_Video_Diffusion_Models.pdf]]
