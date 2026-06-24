---
title: "VideoMage: Multi-Subject and Motion Customization of Text-to-Video Diffusion Models"
type: paper
paper_level: A
venue: CVPR
year: 2025
pdf_ref: paperPDFs/CVPR_2025/VideoMage_Multi_Subject_and_Motion_Customization_of_Text_to_Video_Diffusion_Models.pdf
aliases:
- VideoMage
tags:
- CVPR_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: "采用主体LoRA和运动LoRA分别捕获视觉和运动信息；引入外观无关的运动学习（基于负分类器自由引导）以分离运动与外观；并设计时空协同组合方案（梯度融合+注意力正则化+协同引导）整合多主体与运动。"
primary_logic: "通过负分类器自由引导条件化于视觉外观，可有效解耦运动模式；利用梯度融合和注意力图对齐实现多主体LoRA与运动LoRA的协同生成。"
claims:
- "外观无关的运动学习使用负分类器自由引导，以消除外观信息，使运动LoRA专注于运动动态。"
- "多主体LoRA融合采用梯度融合和空间注意力正则化，确保各主体外观保留并合理布局。"
- "时空协同采样（SCS）通过对齐时间自注意力图和空间交叉注意力图实现主体与运动分支的协同。"
- "定量实验显示VideoMage在DINO-I上超越MotionDirector（0.407 vs 0.370），并在人类偏好研究中全面占优。"
---

# VideoMage: Multi-Subject and Motion Customization of Text-to-Video Diffusion Models

> [!tip] 核心洞察
> 通过负分类器自由引导条件化于视觉外观，可有效解耦运动模式；利用梯度融合和注意力图对齐实现多主体LoRA与运动LoRA的协同生成。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | VideoMage: 面向文本到视频扩散模型的多主体与运动定制 |
| 英文题名 | VideoMage: Multi-Subject and Motion Customization of Text-to-Video Diffusion Models |
| 会议/期刊 | CVPR 2025 |
| Links | [paper](https://arxiv.org/abs/2503.21781); [Project](https://jasper0314-huang.github.io/videomage-customization) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | VideoMage |
| Dataset | 多主体与运动定制, 多主体定制（Table 4） |

> [!tip] 效果简介
> - 多主体与运动定制 上，CLIP-T 为 0.662，对比 DreamVideo: 0.649, MotionDirector: 0.656，变化 +0.013 / +0.006。
> - 多主体与运动定制 上，CLIP-I 为 0.670，对比 DreamVideo: 0.655, MotionDirector: 0.653，变化 +0.015 / +0.017。
> - 多主体与运动定制 上，DINO-I 为 0.407，对比 MotionDirector: 0.370，变化 +0.037。

## 概述

### 问题瓶颈

文本到视频（T2V）扩散模型的定制化生成是当前研究热点，但现有方法存在显著局限：它们通常只能处理单一概念——要么定制主体身份，要么定制运动模式，无法同时实现多主体外观及其交互运动的协同定制。更关键的是，运动学习过程中普遍存在**外观泄漏**问题，即运动模块会意外捕获参考视频中的视觉外观信息，导致生成结果中主体身份与运动模式相互污染。现有方法缺乏对主体与运动组合的有效引导机制，难以在保持各主体外观一致性的同时精确复现目标运动。

### 核心方法

VideoMage 提出了一套解耦-融合-协同的三阶段框架来解决上述瓶颈：

1. **外观无关的运动学习**：采用负分类器自由引导（Negative CFG），以视觉外观为条件反向消除运动学习中的外观信息，使运动 LoRA 专注于运动动态本身，从根本上解决外观泄漏问题。
2. **多主体 LoRA 融合**：通过梯度融合将多个主体 LoRA 蒸馏为单一融合 LoRA，并引入空间注意力正则化（以 Grounded-SAM2 分割掩码为监督），确保各主体外观在组合生成中得以保留且空间布局合理。
3. **时空协同采样（SCS）**：在推理阶段，通过交替对齐主体分支与运动分支的空间交叉注意力图和时间自注意力图，实现外观与运动的时空一致协同生成。

### 主要结果

在多主体与运动联合定制的定量评估中，VideoMage 在 DINO-I 指标上达到 **0.407**，显著超越 MotionDirector（0.370）和 DreamVideo（0.370），提升幅度达 **+0.037**；在 CLIP-I 上达到 0.670，较 DreamVideo（0.655）和 MotionDirector（0.653）分别提升 +0.015 和 +0.017。人类偏好研究中，VideoMage 在运动保真度、主体保真度、文本对齐和视频质量四个维度上全面优于基线方法。消融实验进一步验证了各模块的关键作用：去除 SCS 导致 DINO-I 从 0.407 骤降至 **0.234**，去除外观无关运动损失使 CLIP-I 从 0.670 降至 0.651。

### 方法定位

VideoMage 属于基于 LoRA 的扩散模型定制范式，在方法谱系中处于**多概念解耦定制**与**测试时优化组合**的交汇点。与 DreamVideo（多主体+运动联合定制但缺乏外观-运动解耦）、MotionDirector（仅运动定制）和 CustomVideo/DisenStudio（仅多主体定制）相比，VideoMage 首次实现了外观与运动的显式解耦学习，并通过时空协同采样将两者有机整合，填补了多主体与运动联合定制中“解耦-组合”的技术空白。

## 背景与动机

文本到视频（T2V）扩散模型近年来取得了显著进展，使得用户能够通过自然语言描述生成高质量视频。然而，纯文本提示难以精确传达用户对特定视觉主体外观和运动模式的细粒度需求，这催生了视频定制（video customization）这一研究方向。

现有视频定制方法存在一个核心瓶颈：**它们仅能处理单一概念**——要么定制主体身份（如 DreamVideo、CustomVideo、DisenStudio），要么定制运动模式（如 MotionDirector），但无法同时定制多个主体及其交互运动。具体而言，当需要生成“一只特定外观的猫和一只特定外观的狗按照参考视频中的舞蹈动作一起运动”这样的视频时，现有方法面临三个关键挑战：

1. **外观泄漏问题**：在从参考视频学习运动模式时，运动 LoRA 不可避免地会捕获视频中的视觉外观信息，导致生成结果中出现不需要的外观残留。
2. **多主体组合困难**：将多个主体 LoRA 简单合并会导致属性绑定错误（如猫的外观特征错误地出现在狗身上）和空间布局混乱。
3. **主体与运动缺乏协调**：分别训练的主体 LoRA 和运动 LoRA 在推理时缺乏有效的协同机制，难以保证生成视频中主体外观与运动模式在时空维度上的一致性。

VideoMage 的动机正是填补这一空白：**实现多主体外观与运动模式的联合定制**。其核心洞察在于，通过负分类器自由引导（negative classifier-free guidance）条件化于视觉外观，可以有效解耦运动模式；同时，利用梯度融合和注意力图对齐机制，可以实现多主体 LoRA 与运动 LoRA 的协同生成。这一思路使得 VideoMage 能够首次在统一框架内，根据用户提供的多张主体图像、一段参考运动视频和一条文本提示，生成外观忠实、运动准确且时空一致的定制视频。

## 核心创新

VideoMage 的核心创新在于突破了现有视频定制方法仅能处理单一概念（主体身份或运动模式）的瓶颈，首次实现了多主体与运动的协同定制。其关键创新点可归纳为三个相互关联的“changed slots”：

### 1. 外观无关的运动学习（Appearance-agnostic Motion Learning）

**基线缺陷：** 现有运动定制方法（如 MotionDirector）在微调运动 LoRA 时使用标准扩散损失，导致运动 LoRA 不可避免地捕获参考视频中的视觉外观信息，产生外观泄漏（appearance leakage）。当该运动 LoRA 与新的主体组合时，参考视频的外观会污染生成结果。

**创新方案：** VideoMage 提出基于负分类器自由引导（negative classifier-free guidance）的外观无关运动学习目标。核心思想是：在运动学习阶段，显式地条件化于视觉外观提示 $c_{ap}$，通过负引导消除外观信息，迫使运动 LoRA 仅关注运动动态。具体而言，训练目标中的噪声项变为外观无关噪声：

$$\epsilon_{\mathrm{ap-free}} = (1+\omega)\epsilon - \omega \epsilon_{\theta}(x_{m,t}, c_{\mathrm{ap}}, t)$$

其中 $\omega$ 控制负引导强度。运动学习损失为：

$$\mathcal{L}_{mot} = \mathbb{E}_{x_m, \epsilon, t} \left[ \| \epsilon_{\theta_m}(x_{m,t}, c_m, t) - \epsilon_{\mathrm{ap-free}} \|_2^2 \right]$$

**因果机制：** 负引导项 $-\omega \epsilon_{\theta}(x_{m,t}, c_{\mathrm{ap}}, t)$ 将模型预测推向“远离外观条件”的方向，使得运动 LoRA $\theta_m$ 学到的残差仅编码运动动态，而与具体外观解耦。消融实验（Table 2）证实，移除该损失（w/o $\mathcal{L}_{mot}$）导致 CLIP-I 从 0.670 降至 0.651，并出现明显的外观泄漏（Figure 7 红色框标注）。

### 2. 多主体 LoRA 融合策略（Multi-Subject LoRA Fusion）

**基线缺陷：** 现有多主体定制方法（如 CustomVideo、DisenStudio）或采用简单组合策略，缺乏对多主体空间布局的显式引导，容易出现属性绑定错误（attribute binding）——即主体 A 的外观错误地出现在主体 B 的区域。

**创新方案：** VideoMage 采用梯度融合（gradient-based fusion）与空间注意力正则化相结合的策略。首先，通过匹配融合 LoRA $\hat{\theta}_s$ 与各主体特定 LoRA 的噪声预测来蒸馏多主体身份：

$$\mathcal{L}_{fusion} = \frac{1}{N} \sum_{n=1}^{N} \mathbb{E}_{x_n, \epsilon, t} \left[ \| \epsilon_{\hat{\theta}_s}(x_{n,t}, c_n, t) - \epsilon_n \|_2^2 \right]$$

其次，引入空间注意力正则化损失 $\mathcal{L}_{attn}$，将 UNet 空间交叉注意力图与 Grounded-SAM2 生成的真实分割掩码对齐：

$$\mathcal{L}_{attn} = \frac{1}{2} \sum_{i=1}^{2} \| \mathcal{M}_{SCA,i} - \hat{\mathcal{M}}_i \|_2^2$$

总目标为 $\mathcal{L} = \mathcal{L}_{fusion} + \lambda_2 \mathcal{L}_{attn}$。

**因果机制：** 梯度融合确保融合 LoRA 继承各主体的身份特征，而注意力正则化通过显式监督空间注意力分布，强制模型在正确区域激活对应主体的特征，从根本上解决属性绑定问题。消融实验（Table 2, Figure 7）表明，移除 $\mathcal{L}_{attn}$ 会导致严重的属性绑定错误。

### 3. 时空协同采样（Spatial-Temporal Collaborative Sampling, SCS）

**基线缺陷：** 现有方法将主体 LoRA 和运动 LoRA 分别应用于扩散模型，缺乏两者之间的协调机制，导致生成视频中主体身份与运动模式不一致——主体可能执行错误的运动，或运动过程中主体外观发生畸变。

**创新方案：** SCS 在采样过程中构建主体分支（使用融合主体 LoRA $\hat{\theta}_s$）和运动分支（使用运动 LoRA $\theta_m$），并通过跨模态注意力图对齐实现双向协同：

- **运动正确性保证：** 将主体分支的时间自注意力图 $\mathcal{M}_{TSA,s}$ 对齐到运动分支的对应图 $\mathcal{M}_{TSA,m}$，损失为 $\mathcal{L}_{m \to s} = \| \mathcal{M}_{TSA,s} - \mathcal{M}_{TSA,m} \|_2^2$。
- **空间布局保证：** 将主体分支的空间交叉注意力图 $\mathcal{M}_{SCA,s}$ 对齐到运动分支的对应图 $\mathcal{M}_{SCA,m}$，损失为 $\mathcal{L}_{s \to m} = \| \mathcal{M}_{SCA,s} - \mathcal{M}_{SCA,m} \|_2^2$。
- **噪声融合：** 最终预测噪声为两分支噪声的加权组合 $\epsilon_t = \beta_s \epsilon_t^{sub} + \beta_m \epsilon_t^{mot}$（$\beta_s = \beta_m = 0.5$），并通过梯度更新潜变量 $x_t^{sub} := x_t^{sub} - \alpha_t \nabla_{x_t^{sub}} \mathcal{L}_{m \to s}$。

**因果机制：** 时间自注意力图编码了帧间运动动态，其对齐确保主体分支“模仿”运动分支的时序模式；空间交叉注意力图编码了主体在空间中的位置，其对齐确保运动分支尊重主体的空间布局。双向对齐形成闭环约束，使主体身份与运动模式在时空维度上协同一致。该模块的作用极为关键：消融实验（Table 2）显示，移除 SCS 导致 DINO-I 从 0.407 急剧下降至 0.234，降幅高达 42.5%，证明 SCS 对主体身份保持不可或缺。

---

**创新总结：** 三个 changed slots 构成递进式创新链条——外观无关运动学习从源头解耦运动与外观，多主体融合策略确保多身份的空间正确绑定，时空协同采样在推理阶段实现主体与运动的无缝整合。这一组合使 VideoMage 在 DINO-I 指标上超越 MotionDirector 达 9.9%（0.407 vs 0.370），并在人类偏好研究中全面占优（Figure 6）。

## 整体框架

![[assets/figures/papers/paper_list_l8_VideoMage_Multi_Subject_and_Motion_Customization_of_Text_to_Video_Diffus/figures/002_Figure_2.jpg]]
*Figure 2: Overview of VideoMage. (a) Given images of multiple subjects and a reference video with desirable motion, VideoMage advances LoRAs to capture the knowledge of visual appearances and appearance-agnostic motion information, respectively. (b) With a text prompt relating the aforementioned visual and motion concepts, our spatial-temporal collaborative composition refines the input noisy latent x _ { t } for generating videos matching the desirable visual and motion information*

VideoMage 的整体 pipeline 围绕“解耦学习—融合—协同采样”三阶段展开，目标是同时接收多张主体图像、一段参考运动视频和一条文本提示，输出外观与运动均对齐的定制视频（Figure 2）。

**第一阶段：解耦学习。** 系统分别训练两类 LoRA 模块——主体 LoRA 与运动 LoRA——以独立捕获视觉外观和运动动态。主体 LoRA 仅注入 UNet 的空间层，避免干扰时间动态；训练时使用辅助视频数据集（Panda70M）进行正则化，以保留预训练模型的时间先验。运动 LoRA 注入 UNet 的时间层，其核心创新在于外观无关的运动学习：通过负分类器自由引导（negative classifier-free guidance），以视觉外观为条件生成无外观噪声 $\epsilon_{\mathrm{ap-free}}$，迫使运动 LoRA 专注于运动模式本身，从而解耦外观信息。

**第二阶段：多主体 LoRA 融合。** 当存在多个主体时，系统采用梯度融合将各主体 LoRA 的知识蒸馏至单一融合 LoRA。融合过程中引入空间注意力正则化 $\mathcal{L}_{attn}$，利用 Grounded-SAM2 生成的分割掩码监督空间交叉注意力图，确保各主体外观在融合后仍能正确绑定到对应区域，避免属性混淆。

**第三阶段：时空协同采样（Spatial-Temporal Collaborative Sampling, SCS）。** 推理时，系统并行运行两条分支：主体分支使用融合后的主体 LoRA，运动分支使用运动 LoRA。SCS 通过双向注意力对齐实现协同——将主体分支的空间交叉注意力图对齐到运动分支，确保运动正确作用于对应主体区域；同时将运动分支的时间自注意力图对齐到主体分支，保证时序一致性。两条分支的预测噪声以等权重加权组合，并通过梯度引导更新潜变量，最终生成时空一致的定制视频。

## 核心模块与公式推导

### 3.1 主体定制模块

VideoMage 的主体定制基于 LoRA 微调，核心损失函数为：

$$
\mathcal{L}_{sub} = \mathbb{E}_{x_s, \epsilon, t} \left[ \| \epsilon_{\theta_s}(x_{s,t}, c_s, t) - \epsilon \|_2^2 \right] \quad \text{(Eq. 2)}
$$

其中 $x_{s,t}$ 为加噪后的主体图像潜变量，$c_s$ 为包含特殊标记 `V*` 的文本条件，$\epsilon_{\theta_s}$ 为注入主体 LoRA $\Delta\theta_s$ 后的 UNet 噪声预测。该 LoRA **仅应用于 UNet 的空间层**，避免干扰时间动态先验。

为防止主体微调破坏预训练模型的时间先验，引入辅助视频数据集（如 Panda70M）上的正则化损失：

$$
\mathcal{L}_{reg} = \mathbb{E}_{x_{aux}, \epsilon, t} \left[ \| \epsilon_{\theta_s}(x_{aux,t}, c_{aux}, t) - \epsilon \|_2^2 \right] \quad \text{(Eq. 3)}
$$

总主体定制目标为：

$$
\mathcal{L} = \mathcal{L}_{sub} + \lambda_1 \mathcal{L}_{reg} \quad \text{(Eq. 4)}
$$

其中 $\lambda_1$ 为视频保留正则化权重，消融实验确定最优值为 $\lambda_1 = 0.25$（Table 3）。

---

### 3.2 外观无关运动学习模块

运动 LoRA $\Delta\theta_m$ 注入 UNet 的时间层。为避免运动学习过程中捕获参考视频的外观信息（外观泄漏），VideoMage 提出**外观无关运动学习**，其核心机制为负分类器自由引导（Negative CFG）：

$$
\epsilon_{\mathrm{ap-free}} = (1+\omega)\epsilon - \omega \epsilon_{\theta}(x_{m,t}, c_{\mathrm{ap}}, t) \quad \text{(Eq. 5)}
$$

其中 $c_{\mathrm{ap}}$ 为强调外观信息的文本提示（如 "a photo of [subject]"), $\omega$ 为负引导强度（最优值 $\omega = 0.5$，Table 3）。该操作通过**减去外观条件化噪声预测**，从标准噪声 $\epsilon$ 中剥离外观成分，得到无外观噪声 $\epsilon_{\mathrm{ap-free}}$。运动学习损失为：

$$
\mathcal{L}_{mot} = \mathbb{E}_{x_m, \epsilon, t} \left[ \| \epsilon_{\theta_m}(x_{m,t}, c_m, t) - \epsilon_{\mathrm{ap-free}} \|_2^2 \right] \quad \text{(Eq. 5)}
$$

**因果机制**：标准扩散损失 $\|\epsilon_{\theta} - \epsilon\|^2$ 迫使模型从含外观的参考视频中同时学习外观与运动；而将目标噪声替换为 $\epsilon_{\mathrm{ap-free}}$ 后，模型被引导去预测已剥离外观信息的噪声，从而将运动 LoRA 的优化方向约束在纯运动动态上（Fig. 3）。

**消融证据**：移除 $\mathcal{L}_{mot}$（改用标准扩散损失 Eq. 1）后，CLIP-I 从 0.670 降至 0.651（Table 2），可视化中出现明显外观泄漏（Fig. 7 红色框）。

---

### 3.3 多主体 LoRA 融合模块

给定 $N$ 个独立训练的主体 LoRA $\{\Delta\theta_s^{(n)}\}_{n=1}^N$，VideoMage 通过**梯度融合**将其蒸馏为单一融合 LoRA $\Delta\hat{\theta}_s$：

$$
\mathcal{L}_{fusion} = \frac{1}{N} \sum_{n=1}^{N} \mathbb{E}_{x_n, \epsilon, t} \left[ \| \epsilon_{\hat{\theta}_s}(x_{n,t}, c_n, t) - \epsilon_n \|_2^2 \right] \quad \text{(Eq. 6)}
$$

该损失强制融合模型对每个主体的噪声预测与对应主体特定 LoRA 的预测一致。

为防止多主体属性绑定（如将主体 A 的外观错误赋予主体 B），引入**空间注意力正则化**：利用 Grounded-SAM2 生成 CutMix 式合成视频及分割掩码 $\hat{\mathcal{M}}_i$，对齐空间交叉注意力图：

$$
\mathcal{L}_{attn} = \frac{1}{2} \sum_{i=1}^{2} \| \mathcal{M}_{SCA,i} - \hat{\mathcal{M}}_i \|_2^2 \quad \text{(Eq. 7)}
$$

多主体融合总目标为：

$$
\mathcal{L} = \mathcal{L}_{fusion} + \lambda_2 \mathcal{L}_{attn} \quad \text{(Eq. 8)}
$$

其中 $\lambda_2$ 为注意力正则化权重（最优值 $\lambda_2 = 0.6$，Table 3）。

**消融证据**：移除 $\mathcal{L}_{attn}$ 导致属性绑定问题（Fig. 7），定量指标下降（Table 2）。

---

### 3.4 时空协同采样（SCS）

SCS 在推理时协同融合主体 LoRA $\hat{\theta}_s$ 与运动 LoRA $\theta_m$，核心为**跨分支注意力图对齐**与**加权噪声融合**。

**协同引导损失**：

$$
\mathcal{L}_{s \to m} = \| \mathcal{M}_{SCA,s} - \mathcal{M}_{SCA,m} \|_2^2, \quad \mathcal{L}_{m \to s} = \| \mathcal{M}_{TSA,s} - \mathcal{M}_{TSA,m} \|_2^2
$$

- $\mathcal{L}_{s \to m}$：将主体分支的空间交叉注意力图对齐到运动分支，确保主体在运动视频中的空间布局正确。
- $\mathcal{L}_{m \to s}$：将主体分支的时间自注意力图对齐到运动分支，确保主体运动模式与参考运动一致。

**潜变量梯度更新**：

$$
x_t^{sub} := x_t^{sub} - \alpha_t \nabla_{x_t^{sub}} \mathcal{L}_{m \to s}, \quad x_t^{mot} := x_t^{mot} - \alpha_t \nabla_{x_t^{mot}} \mathcal{L}_{s \to m}
$$

其中 $\alpha_t$ 为协同引导尺度（最优值 $\alpha_t = 10^4$，Table 3），引导步数 $\tau = 15$（Table 3）。

**噪声融合**：

$$
\epsilon_t = \beta_s \epsilon_t^{sub} + \beta_m \epsilon_t^{mot}, \quad \beta_s = \beta_m = 0.5
$$

**决定性证据**：移除 SCS（直接组合 $\theta_s$ 与 $\theta_m$ 推理）导致 DINO-I 从 0.407 骤降至 0.234（Table 2），证明 SCS 对主体身份保持至关重要。

## 实验与分析

### 多主体与运动定制定量评估

VideoMage 在同时定制多个主体外观与参考运动的任务上，与现有基线进行了系统比较。表 1 汇总了在 CLIP-T（文本对齐）、CLIP-I（图像对齐）、DINO-I（身份保持）和时序一致性四个维度上的定量结果。


![[assets/figures/papers/paper_list_l8_VideoMage_Multi_Subject_and_Motion_Customization_of_Text_to_Video_Diffus/figures/006_Table_1.jpg]]
*Table 1: Quantitative comparison on multi-subject and motion customization. We follow [44, 51] to adopt metrics including CLIP-Text Alignment (CLIP-T), CLIP-Image Alignment (CLIP-I), DINO-Image Alignment (DINO-I), and Temporal Consistency (T. Cons.)*

**表 1：多主体与运动定制定量比较**

| 方法 | CLIP-T | CLIP-I | DINO-I | 时序一致性 |
|------|--------|--------|--------|------------|
| DreamVideo | 0.649 | 0.655 | — | — |
| MotionDirector | 0.656 | 0.653 | 0.370 | — |
| **VideoMage** | **0.662** | **0.670** | **0.407** | — |

VideoMage 在所有指标上均取得最优。其中 DINO-I 达到 0.407，相比 MotionDirector 的 0.370 提升了 0.037，表明外观无关运动学习与时空协同采样对主体身份保持的贡献显著。CLIP-I 较 DreamVideo 和 MotionDirector 分别高出 0.015 和 0.017，说明多主体融合策略有效保留了各主体的视觉外观。CLIP-T 的微弱优势（+0.013 / +0.006）则反映了协同组合方案对文本语义的更好遵循。

此外，在仅评估多主体定制能力的消融实验中（表 4），VideoMage 的 CLIP-I 和 DINO-I 分别为 0.681 和 0.403，与 CustomVideo（0.679 / 0.402）持平或略优。需注意，为公平比较，DisenStudio 所需的额外边界框输入被省略。


![[assets/figures/papers/paper_list_l8_VideoMage_Multi_Subject_and_Motion_Customization_of_Text_to_Video_Diffus/figures/013_Table_4.jpg]]
*Table 4: Quantitative comparison on multi-subject customization. Following [8, 43], we evaluate using CLIP-Text Alignment (CLIP-T), CLIP-Image Alignment (CLIP-I), DINO-Image Alignment (DINO-I), and Temporal Consistency (T. Cons.)*

### 人类偏好研究

图 6 展示了人类偏好研究的结果。参与者在运动保真度、主体保真度、文本对齐和视频质量四个维度上对 VideoMage 与 DreamVideo、MotionDirector 的生成结果进行两两比较。VideoMage 在所有维度上均获得显著优势，与定量指标的趋势一致。


![[assets/figures/papers/paper_list_l8_VideoMage_Multi_Subject_and_Motion_Customization_of_Text_to_Video_Diffus/figures/007_Figure_6.jpg]]
*Figure 6: Human preference study. Our VideoMage consistently achieves the best human preference compared to DreamVideo [44] and MotionDirector [47]*

### 消融实验

表 2 系统拆解了 VideoMage 三个核心组件的贡献。


![[assets/figures/papers/paper_list_l8_VideoMage_Multi_Subject_and_Motion_Customization_of_Text_to_Video_Diffus/figures/009_Table_2.jpg]]
*Table 2: Quantitative ablation study. Ablation of our proposed objectives/sampling strategy in VideoMage*

**表 2：核心组件消融**

| 配置 | CLIP-I | DINO-I |
|------|--------|--------|
| VideoMage（完整） | 0.670 | 0.407 |
| w/o L_mot（去除外观无关运动损失） | 0.651 | — |
| w/o L_attn（去除空间注意力正则化） | — | — |
| w/o SCS（去除时空协同采样） | — | 0.234 |

去除外观无关运动损失（w/o L_mot）后，运动 LoRA 采用标准扩散损失训练，CLIP-I 从 0.670 降至 0.651，证实了外观泄漏的存在——运动学习过程中捕获了不应有的外观信息。去除空间注意力正则化（w/o L_attn）导致主体属性绑定问题，图 7 的可视化消融中可观察到明显的属性混淆。最关键的发现来自时空协同采样（SCS）：去除 SCS 后，DINO-I 从 0.407 急剧下降至 0.234，降幅达 42.5%，说明直接组合主体和运动 LoRA 而不进行注意力对齐与协同引导，将严重损害主体身份保持。

### 超参数敏感性

表 3 报告了关键超参数的消融结果。视频保留正则化权重 $\lambda_1=0.25$、注意力正则化权重 $\lambda_2=0.6$、负引导强度 $\omega=0.5$、协同引导尺度 $\alpha_t=10^4$、协同引导步数 $\tau=15$ 时达到最佳综合性能。外观提示模板 $c_{ap}$ 的选择对运动解耦效果有直接影响，需根据具体场景调整。


![[assets/figures/papers/paper_list_l8_VideoMage_Multi_Subject_and_Motion_Customization_of_Text_to_Video_Diffus/figures/012_Table_3.jpg]]
*Table 3: Ablation studies on various hyperparameters, including the weights for video preservation loss ( $\lambda _ { 1 }$ ) and attention regularization loss $\left( \lambda _ { 2 } \right$) , the template for appearance prompt ( $c _ { \mathrm { a p } }$ ) , the negative guidance scale factor (ω), the collaborative guidance scale (αt) and steps (τ )

### 失败模式与局限

尽管 VideoMage 在定量和定性评估中表现优异，仍存在以下局限：

1. **长视频生成的计算瓶颈**：当前方法在处理高分辨率长视频时需要大量计算资源，限制了生成更长、更复杂定制视频的能力。训练和推理的高资源消耗使得快速定制分钟级视频变得困难。
2. **泛化边界**：系统可能难以泛化到训练数据中未出现的新主体类型或极端运动模式，这在开放域定制场景中构成潜在风险。
3. **多主体交互复杂性**：虽然注意力正则化缓解了属性绑定问题，但在涉及三个以上主体或复杂交互的场景中，主体间的空间关系仍可能出现偏差。

这些失败模式指向两个开放方向：如何扩展方法以定制长时间运动并生成分钟级视频；以及是否可以集成无需训练的定制方法以降低长视频的计算成本。

### 补充图表

![[assets/figures/papers/paper_list_l8_VideoMage_Multi_Subject_and_Motion_Customization_of_Text_to_Video_Diffus/figures/011_Table.jpg]]
*Table: (a) Weight for video preservation loss \lambda _ { 1 }*


## 方法谱系与知识库定位

### 1. 问题定位：从单概念定制到多主体-运动联合生成

文本到视频扩散模型的定制化生成（customization）是当前生成式AI的核心挑战之一。现有方法可大致分为两条独立的技术路线：**主体定制**与**运动定制**。主体定制方法（如 **CustomVideo**、**DisenStudio**）专注于从少量图像中学习特定对象的视觉外观，但无法控制运动模式；运动定制方法（如 **MotionDirector**）则从参考视频中提取运动动态，却难以同时保留多主体的身份特征。**DreamVideo** 虽然尝试同时处理主体与运动，但其简单组合策略导致外观泄漏（appearance leakage）——运动LoRA在学习运动时不可避免地捕获了参考视频中的视觉外观信息，从而污染了主体身份。

VideoMage 的核心贡献在于首次系统性地解决了这一瓶颈：**如何在同一生成框架中解耦并协同组合多主体外观与运动模式**。其技术定位处于主体定制与运动定制的交叉地带，通过LoRA模块化设计和时空协同采样机制，填补了多主体-运动联合定制的空白。

### 2. 与基线方法的关键差异

VideoMage 相对于代表性基线方法的核心改进体现在三个操作槽位（changed slots）上：

| 操作槽位 | 基线做法 | VideoMage 方案 | 证据锚点 |
|---------|---------|---------------|---------|
| **运动学习方式** | 标准扩散损失（如 MotionDirector），导致运动LoRA捕获外观信息 | 外观无关运动学习：负分类器自由引导目标（Eq.5）解耦外观 | Eq. (5), Fig. 3 |
| **多主体组合策略** | 单一主体定制或简单LoRA叠加（如 DreamVideo） | 梯度融合（Eq.6）+ 空间注意力正则化（Eq.7）合并多主体LoRA | Sec. 3.3, Eq. (6-8), Fig. 4(a) |
| **主体与运动整合** | 分别使用主体和运动LoRA，缺乏协调机制 | 时空协同采样（SCS）：通过注意力图对齐与加权噪声融合实现协同生成 | Sec. 3.3, Algorithm 1, Fig. 4(b) |

**外观无关运动学习**是VideoMage区别于 MotionDirector 等方法的根本性创新。MotionDirector 在微调运动LoRA时使用标准噪声预测损失，导致模型同时学习参考视频中的外观和运动特征——定量消融显示，若VideoMage移除此组件（w/o L_mot），CLIP-I从0.670降至0.651，证实了外观泄漏对主体身份保持的负面影响（Table 2）。VideoMage通过负分类器自由引导（negative classifier-free guidance）构建无外观噪声 $\epsilon_{\mathrm{ap-free}} = (1+\omega)\epsilon - \omega \epsilon_{\theta}(x_{m,t}, c_{\mathrm{ap}}, t)$，显式抑制外观信息，使运动LoRA仅编码运动动态。

**多主体LoRA融合**方面，DreamVideo 等方法的简单组合无法保证各主体在生成视频中的空间布局合理性。VideoMage采用梯度融合（gradient-based fusion）将多个主体LoRA蒸馏为单一融合LoRA，并引入空间注意力正则化 $\mathcal{L}_{attn}$——利用 Grounded-SAM2 生成的CutMix式视频和分割掩码，强制模型的空间交叉注意力图对准正确的主体区域。消融实验表明，移除 $\mathcal{L}_{attn}$ 会导致属性绑定错误（Figure 7红框标注）。

**时空协同采样（SCS）** 是VideoMage在推理阶段的核心机制。与直接组合两个LoRA进行推理的朴素方案不同，SCS通过对齐主体分支和运动分支的注意力图实现跨模态协同：主体到运动的引导损失 $\mathcal{L}_{s \to m}$ 对齐空间交叉注意力图以确保主体位置正确，运动到主体的引导损失 $\mathcal{L}_{m \to s}$ 对齐时间自注意力图以注入运动动态。消融实验显示，移除SCS导致DINO-I从0.407急剧下降至0.234（Table 2），证明该机制对主体身份保持至关重要。

### 3. 方法适用边界与局限

**适用场景**：VideoMage 适用于给定2-3个主体参考图像和一个运动参考视频，生成包含这些主体执行目标运动的短视频片段。其设计假设主体外观与运动模式可被LoRA模块有效解耦，且参考视频的运动模式具有足够的代表性。

**已知局限**（论文明确指出的限制）：

1. **长视频生成的计算瓶颈**：当前方法在处理长视频，尤其是高分辨率场景时需要大量计算资源。SCS在每一步采样中需对主体和运动两个分支进行梯度更新，显著增加了推理开销，限制了生成更长、更复杂定制视频的能力。

2. **训练与推理的高资源消耗**：主体LoRA和运动LoRA的独立微调，以及测试时的多主体融合和协同采样，使得快速定制长视频变得困难。超参数消融（Table 3）显示，协同引导步数 $\tau$ 和引导尺度 $\alpha_t$ 对性能敏感，需要针对不同输入进行调优。

3. **泛化能力受限**：系统可能难以泛化到训练数据中未出现的新主体类型或极端运动模式。运动LoRA依赖于参考视频中运动模式的可学习性，对于过于复杂或非重复性的运动，外观无关学习的效果可能下降。

**需要手动验证的边界**：论文未提供对以下情况的系统性评估——（a）主体数量超过3个时的性能退化曲线；（b）主体外观与参考视频中对象外观高度相似时，外观无关运动学习是否仍能有效解耦；（c）运动模式涉及多个独立移动对象时的协同生成质量。这些边界条件需要在实际应用中谨慎测试。

### 4. 开放问题与后续方向

基于VideoMage的当前设计，以下几个方向值得探索：

1. **长时运动定制与分钟级视频生成**：如何扩展方法以定制长时间运动并生成分钟级视频？这可能需要引入运动表征的层次化编码或时序压缩技术，同时降低SCS的每步计算成本。

2. **无需训练的定制方法集成**：是否可以集成无需训练的定制方法以降低长视频的计算成本？例如，利用预训练的时空注意力先验替代部分测试时优化步骤，可能显著减少推理时间。

3. **多主体交互的复杂性与真实性提升**：如何在不显著增加计算开销的情况下提高多主体交互的复杂性和真实性？当前的空间注意力正则化仅约束主体空间位置，未显式建模主体间的物理交互（如遮挡、碰撞），未来可引入物理先验或场景图约束。

4. **运动泛化与零样本迁移**：VideoMage的运动LoRA与特定参考视频强绑定，能否实现运动模式的跨视频泛化，或从文本描述中直接合成运动模式？这需要运动表征的语义解耦和组合泛化能力。

## 原文 PDF

![[paperPDFs/CVPR_2025/VideoMage_Multi_Subject_and_Motion_Customization_of_Text_to_Video_Diffusion_Models.pdf]]
