---
title: "Separate Motion from Appearance: Customizing Motion via Customizing Text-to-Video Diffusion Models"
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: paperPDFs/arxiv_2025/Separate_Motion_from_Appearance_Customizing_Motion_via_Customizing_Text_to_Video_Diffusion_Models.pdf
project_link: null
code_link: "https://github.com/LiuHuijie6410/SeperateMotionFromAppearance"
aliases:
- SMFATAP
- SMFACMCTVDM
tags:
- arxiv_2025
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 通过约束运动LoRA只作用于时间注意力的Key嵌入（TAP），并修改U-Net跳跃连接的起点，使其从空间Transformer而非LoRA适应的时间Transformer出发（AH），从而在维持运动建模精度的同时阻断外观信息的传播路径。
primary_logic: 预训练的时间注意力Value嵌入已经包含了描绘运动所需的丰富基础组件，通过LoRA调整Key嵌入重塑注意力权重即可组合出新的运动模式，而无需修改Value嵌入本身，从而避免了外观信息的混入。
claims:
- 在时间Transformer中仅对Key嵌入（W_K）应用LoRA，可在保持较高运动质量（64.3）的同时，显著提升外观对齐度（25.52）并降低外观泄漏（21.33），相比修改全部线性层或Value嵌入具有明显优势。
- 增大外观高速公路（AH）的缩放因子可逐步消除生成视频中的外观泄漏（如误出现的“窗户”），而等比例放大标准跳跃连接则毫无效果。
- AH使解码器隐藏状态更接近原始T2V-DM，而更远离注入空间LoRA的模型，表明AH有效恢复了基础模型的外观生成能力；同时运动分类器仍将大部分AH隐藏状态识别为TAP运动，证明AH并未破坏运动信息。
- 组合TAP、AH和分阶段LoRA集成（PLI）在一次性运动定制基准上取得领先的文本对齐分数（28.52 vs. MotionDirector 27.55），验证了方法的整体有效性。
---

# Separate Motion from Appearance: Customizing Motion via Customizing Text-to-Video Diffusion Models

> [!tip] 核心洞察
> 预训练的时间注意力Value嵌入已经包含了描绘运动所需的丰富基础组件，通过LoRA调整Key嵌入重塑注意力权重即可组合出新的运动模式，而无需修改Value嵌入本身，从而避免了外观信息的混入。

| 字段 | 内容 |
|------|------|
| 中文题名 | 分离运动与外观：通过定制文本到视频扩散模型实现运动定制 |
| 英文题名 | Separate Motion from Appearance: Customizing Motion via Customizing Text-to-Video Diffusion Models |
| 会议/期刊 | arXiv 2025 |
| Links | [paper](https://arxiv.org/abs/2501.16714) · [Code](https://github.com/LiuHuijie6410/SeperateMotionFromAppearance) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | Separate Motion from Appearance (TAP + AH + PLI) |
| Dataset | One-shot motion customization |

> [!tip] 效果简介
> - One-shot motion customization (VBench) 上，Text Alignment 28.52 vs 27.55 (MotionDirector) (+0.97)；ViCLIP Score 26.52 vs 25.54 (MotionDirector) (+0.98)。

## 概要

### 问题背景

文本到视频扩散模型（T2V-DM）在通用视频生成上取得了显著进展，但如何让模型学会特定的运动模式（如“一只猫在跳跃”的运动轨迹）并在任意外观条件下复现，即**运动定制**（Motion Customization），仍是一个开放挑战。现有方法（如 **MotionDirector**，Zhao et al., arXiv 2023）通过低秩适配（LoRA）从参考视频中学习运动表示，但存在一个关键瓶颈：**外观泄漏**（Appearance Leakage）——参考视频中的外观元素（如背景中的“窗户”）会被非预期地编码进运动表示中，导致生成视频的外观与文本描述出现偏差，削弱了模型的多样化外观生成能力。

### 核心洞察

本文的核心发现是：预训练的 T2V-DM 中，**时间注意力机制的 Value 嵌入已经包含了描绘运动所需的丰富基础组件**。通过 LoRA 仅调整 Key 嵌入来重塑注意力权重，即可重新组合这些组件以产生新的运动模式，而无需修改 Value 嵌入本身。这一设计从根本上切断了外观信息通过 Value 嵌入混入运动表示的路径。

### 方法与贡献

基于上述洞察，本文提出 **Separate Motion from Appearance** 框架，包含三个互补策略：

1.  **时间注意力净化（Temporal Attention Purification, TAP）**：在时间 Transformer 中，约束运动 LoRA **仅作用于 Key 嵌入（W_K）**，避免修改 Value 嵌入和 Query 嵌入，从而在维持运动建模精度的同时阻断外观信息的传播路径。

2.  **外观高速公路（Appearance Highway, AH）**：修改 U-Net 跳跃连接的起点，使其从**空间 Transformer 的输出**出发，而非从经过 LoRA 适配的时间 Transformer 输出出发。这使得解码器能够直接获取未被运动 LoRA 污染的外观特征，有效恢复基础模型的外观生成能力。

3.  **分阶段 LoRA 集成（Phased LoRA Integration, PLI）**：在推理时，前 τ 步使用带 TAP 与 AH 的适配模型专注运动建模，后续步骤切换回原始 T2V-DM 以完善外观细节，实现运动与外观的解耦生成。

### 主要结果

在一次性运动定制基准（VBench）上，本方法取得了领先的文本对齐分数（**28.52** vs. MotionDirector 27.55）和 ViCLIP 分数（**26.52** vs. 25.54）。消融实验证实，依次添加 TAP、AH 和 PLI 可持续提升文本对齐分数（27.55 → 27.91 → 28.32 → 28.52），验证了各组件的累积贡献。定性结果显示，本方法生成的视频外观更贴合文本描述，运动更符合参考视频，有效抑制了外观泄漏问题。

### 方法定位

本方法属于**基于微调的运动定制**范式，需要针对每个运动概念收集参考视频并进行训练，与 **Tune-A-Video**（Wu et al., ICCV 2023）、**VMC**（Jeong et al., CVPR 2024）等方法同属一类。与无需训练的 **VideoComposer**（Wang et al., NeurIPS 2024）和需要额外图像条件的 **LAMP**（Wu et al., CVPR 2024）、**DreamVideo**（Wei et al., CVPR 2024）相比，本方法在少样本场景下无需图像条件即可取得更优的外观对齐效果。

文本到视频扩散模型（T2V-DM）的快速发展使得高质量视频生成成为可能，但如何精确控制生成视频中的运动模式仍然是一个核心挑战。运动定制（motion customization）任务旨在从少量参考视频中学习特定的运动概念，并将其迁移到由文本描述引导的新外观场景中。这一能力对于电影制作、动画设计、虚拟现实等创意应用具有重要价值。

现有运动定制方法面临一个根本性瓶颈：外观泄漏（appearance leakage）。以代表性方法 **MotionDirector**（Zhao et al., arXiv 2023）为例，其采用双路径 LoRA 框架，分别训练空间 LoRA 捕获外观和时间 LoRA 捕获运动。然而，由于时间注意力中的 Value 嵌入同时承载了运动信息和外观信息，时间 LoRA 在建模运动模式时不可避免地会将参考视频中的外观元素（如背景物体、纹理特征）编码进运动表示中。如 Figure 1 所示，当参考视频包含“窗户”这一外观元素时，先前方法生成的视频中会意外出现窗户，即使文本描述并未提及该元素——这表明外观信息已泄漏到运动 LoRA 中，削弱了模型根据文本生成多样化外观的能力。

这一瓶颈的因果根源在于：时间注意力的 Value 嵌入是信息聚合的最终载体，直接修改 Value 嵌入会同时改变运动表征和外观表征。因此，如何在不修改 Value 嵌入的前提下重塑时间注意力权重，成为分离运动与外观的关键操控点。本文的核心洞察是：预训练 T2V-DM 的时间注意力 Value 嵌入已经包含了描绘运动所需的丰富基础组件，仅需通过 LoRA 调整 Key 嵌入来重塑注意力权重，即可重新组合这些组件以产生新的运动模式，而无需接触 Value 嵌入本身，从而从架构层面阻断外观信息的传播路径。

基于上述洞察，本文提出了一套系统的运动-外观分离框架，包含三个互补策略：时间注意力净化（Temporal Attention Purification, TAP）、外观高速公路（Appearance Highway, AH）和分阶段 LoRA 集成（Phased LoRA Integration, PLI）。TAP 将运动 LoRA 的作用范围严格限制在时间注意力的 Key 嵌入上，避免对 Value 嵌入的修改；AH 通过修改 U-Net 跳跃连接的起点，使解码器从空间 Transformer 而非 LoRA 适配的时间 Transformer 接收隐藏状态，进一步维持基础模型的外观生成能力；PLI 在推理时采用分阶段策略，早期去噪步使用适配模型专注运动建模，后期切换回原始 T2V-DM 完善外观细节。三者协同作用，在保持运动建模精度的同时显著抑制外观泄漏，实现了运动与外观的有效分离。

## 核心方法与创新机理

本工作围绕“运动-外观分离”这一核心目标，针对现有运动定制方法（如 **MotionDirector**，Zhao et al., arXiv 2023）中普遍存在的**外观泄漏**问题，提出了三个关键创新组件。其根本洞察在于：预训练时间注意力中的 Value 嵌入已包含描述运动的丰富基础组件，只需通过调整 Key 嵌入重塑注意力权重即可组合出新运动模式，而无需修改 Value 嵌入本身，从而阻断外观信息的混入路径。

### 1. 时间注意力净化（Temporal Attention Purification, TAP）

**改变的槽位**：时间注意力中 LoRA 的适配范围。

- **基线做法**：MotionDirector 等双路径 LoRA 方法将低秩适配器注入时间 Transformer 的所有线性层（Q、K、V、前馈网络），以学习参考视频的运动模式。然而，这不可避免地使 Value 嵌入（决定输出特征内容）也编码了参考视频的外观信息。
- **本方法做法**：TAP 将时间 LoRA **仅应用于 Key 嵌入（W_K）**。通过仅重塑注意力权重矩阵，Value 嵌入被重新组织以产生新运动，但其本身保持未被 LoRA 修改的状态，从而在源头上抑制外观信息进入运动编码。

**证据支撑**：探索性消融实验（Table 1）显示，仅适配 W_K 在保持较高运动质量（64.3）的同时，显著提升外观对齐度（25.52）并降低外观泄漏（21.33），相比适配全部线性层或 Value 嵌入具有明显优势。适配 Value 嵌入（W_V）会导致外观对齐度骤降至 22.88，验证了 Value 嵌入是外观泄漏的关键通道。

### 2. 外观高速公路（Appearance Highway, AH）

**改变的槽位**：U-Net 跳跃连接的起点。

- **基线做法**：标准空间-时间 U-Net 中，跳跃连接从时间 Transformer 的输出出发，将特征传递给解码器。由于时间 Transformer 已被运动 LoRA 适配，其输出不可避免地携带了参考视频的外观特征。
- **本方法做法**：AH 将跳跃连接的起点**从时间 Transformer 的输出改为空间 Transformer 的输出**。空间 Transformer 未被运动 LoRA 适配，其输出保留了基础模型对文本描述的忠实外观生成能力，从而绕过了被运动 LoRA“污染”的时间 Transformer 输出。

**证据支撑**：
- 定性实验（Figure 3）表明，增大 AH 的缩放因子可逐步消除生成视频中的外观泄漏（如误出现的“窗户”），而等比例放大标准跳跃连接则毫无效果，证明 AH 的阻断作用是特异性的。
- 隐藏状态分析（Figure 4）进一步揭示：AH 使解码器隐藏状态更接近原始 T2V-DM，而更远离注入空间 LoRA 的模型，表明 AH 有效恢复了基础模型的外观生成能力；同时，运动分类器仍将大部分 AH 隐藏状态识别为 TAP 运动，证明 AH 并未破坏运动信息。

### 3. 分阶段 LoRA 集成（Phased LoRA Integration, PLI）

**改变的槽位**：推理时的 LoRA 应用阶段。

- **基线做法**：整个去噪过程均使用适配后的模型，运动建模与外观细节生成在全部时间步上耦合。
- **本方法做法**：PLI 将去噪过程分为两个阶段：前 τ 步使用带 TAP 与 AH 的适配模型，专注于运动模式塑造；后续步骤切换回原始 T2V-DM，利用其强大的先验完善外观细节。其数学形式为：
  $$z_{t-1} = \begin{cases} \frac{1}{\sqrt{\alpha_t}} \left( z_t - \frac{1-\alpha_t}{\sqrt{1-\bar{\alpha}_t}} \epsilon_\theta(z_t, t) \right) + \sigma_t, & t \leq \tau \\ \frac{1}{\sqrt{\alpha_t}} \left( z_t - \frac{1-\alpha_t}{\sqrt{1-\bar{\alpha}_t}} \epsilon_{\theta,\theta_K}(z_t, t) \right) + \sigma_t, & t > \tau \end{cases}$$

**证据支撑**：消融实验（Table 4）显示，在 TAP+AH 基础上叠加 PLI，文本对齐分数从 28.32 进一步提升至 28.52，且时间一致性从 93.71 恢复至 93.83（均优于基线 93.56），验证了分阶段策略对运动-外观解耦的增强作用。

### 创新点总结

三个组件形成互补闭环：**TAP** 从 LoRA 注入范围上阻断外观信息进入运动编码，**AH** 从网络拓扑上切断外观泄漏的传播路径，**PLI** 从推理时序上实现运动建模与外观生成的解耦。三者协同使该方法在一次性运动定制基准上取得领先的文本对齐分数（28.52 vs. MotionDirector 27.55）和 ViCLIP 分数（26.52 vs. 25.54），在保持运动精度的同时显著提升了外观与文本描述的一致性。

本方法建立在预训练的文本到视频扩散模型（T2V-DM）之上，其核心目标是在仅给定一个参考视频的条件下，学习其中的运动模式并迁移到由文本描述指定的新外观中，同时避免参考视频外观信息向生成结果的泄漏。整体框架由**训练**与**推理**两个阶段构成，并通过三个关键模块——**时间注意力净化（Temporal Attention Purification, TAP）**、**外观高速公路（Appearance Highway, AH）** 和**分阶段LoRA集成（Phased LoRA Integration, PLI）**——协同实现运动与外观的解耦。

### 训练阶段：双路径LoRA适配

训练沿用 **MotionDirector**（Zhao et al., arXiv 2023）的双路径LoRA框架，在冻结预训练T2V-DM所有参数的前提下，同时训练两条低秩适配（LoRA）路径（见 Figure 2(a)）：

![[assets/figures/papers/paper_list_l1837_Separate_Motion_from_Appearance_Customizing_Motion_via_Customizing_Text/figures/002_Figure_2.jpg]]
*Figure 2: Overview of our method. This figure illustrates our main contributions: (a) Overall inference process. (b) Temporal Attention Purification where we utilize LoRA only to adapt the Key embeddings to reshape the temporal attention. (c) Appearance Highway where we alter the starting point of skip connection from LoRA-adapted temporal transformer block to non-adapted spatial transformer block*

- **空间LoRA路径**：注入U-Net的空间Transformer，负责重建参考视频的外观信息。
- **时间LoRA路径**：注入U-Net的时间Transformer，负责捕获参考视频的运动模式。

两条路径共享同一个去噪目标。时间LoRA的训练损失函数为：

$$
\operatorname*{min}_{\theta_{tp}} \mathbb{E}_{z_0, y, t, \epsilon} \left[ \left\| \epsilon - \epsilon_{\theta, \theta_{tp}}(z_t, y, t) \right\|_2^2 \right]
$$

其中 $\theta_{tp}$ 为时间LoRA参数，$\epsilon$ 为添加的噪声，$\epsilon_{\theta, \theta_{tp}}$ 为融入时间LoRA的U-Net预测噪声。目标是最小化预测噪声与真实噪声之间的L2距离。

### 推理阶段：运动-外观分离的生成流程

推理阶段的整体流程如 Figure 2(a) 所示，输入为文本描述和训练好的LoRA权重，输出为定制运动的视频。其核心在于三个模块的协同运作：

1. **时间注意力净化（TAP）**：在时间Transformer中，仅将LoRA适配施加于Key嵌入（$W_K$），而不修改Value嵌入（$W_V$）或前馈网络（$W_{ff}$）。其设计依据是：预训练的Value嵌入已包含丰富的运动基础组件，通过LoRA重塑Key嵌入来调整时间注意力权重，即可重新组合Value嵌入以产生新的运动模式，同时阻断外观信息通过Value路径混入运动编码。探测实验（Table 1）证实，仅适配$W_K$可在保持较高运动质量（64.3）的同时，显著提升外观对齐度（25.52）并降低外观泄漏（21.33），相比适配全部线性层或Value嵌入具有明显优势。

2. **外观高速公路（AH）**：修改U-Net中跳跃连接的起点，使其从空间Transformer的输出出发，而非从经过LoRA适配的时间Transformer输出出发（见 Figure 2(c)）。这一设计使解码器能够直接获取编码器中未被时间LoRA污染的空间特征，从而维持基础模型的外观生成能力。Figure 3 的定性结果表明，增大AH的缩放因子可逐步消除生成视频中的外观泄漏（如误出现的“窗户”），而等比例放大标准跳跃连接则毫无效果。Figure 4 的隐藏状态相似度分析进一步证实：AH使解码器隐藏状态更接近原始T2V-DM，而更远离注入空间LoRA的模型，同时运动分类器仍将大部分AH隐藏状态识别为TAP运动，证明AH在恢复外观生成能力的同时并未破坏运动信息。

3. **分阶段LoRA集成（PLI）**：推理时采用分阶段去噪策略。设总去噪步数为 $T$，阈值步数为 $\tau$，则去噪过程为：

$$
z_{t-1} = \begin{cases}
\frac{1}{\sqrt{\alpha_t}} \left( z_t - \frac{1-\alpha_t}{\sqrt{1-\bar{\alpha}_t}} \epsilon_\theta(z_t, t) \right) + \sigma_t, & t \leq \tau \\
\frac{1}{\sqrt{\alpha_t}} \left( z_t - \frac{1-\alpha_t}{\sqrt{1-\bar{\alpha}_t}} \epsilon_{\theta, \theta_K}(z_t, t) \right) + \sigma_t, & t > \tau
\end{cases}
$$

- 在**早期去噪步**（$t > \tau$）：使用融入TAP和AH的适配模型（$\epsilon_{\theta, \theta_K}$），专注于塑造运动模式。
- 在**后期去噪步**（$t \leq \tau$）：切换回原始T2V-DM（$\epsilon_\theta$），专注于完善外观细节。

这一策略利用了扩散模型在不同去噪阶段的行为特性——早期阶段主要决定全局结构和运动，后期阶段主要填充细节纹理——从而在运动建模和外观保真度之间取得更优的平衡。

### 模块间的协同关系

三个模块在推理流程中形成递进式的解耦链路：**TAP** 从LoRA适配的源头限制外观信息进入运动编码，**AH** 在特征传播路径上阻断残留外观信息通过跳跃连接影响解码器，**PLI** 在时间维度上进一步隔离运动建模与外观生成阶段。消融实验（Table 4）表明，依次添加TAP、AH和PLI可累积提升文本对齐分数（27.55 → 27.91 → 28.32 → 28.52），验证了各组件的互补性。其中，虽然单独使用AH会使时间一致性从93.86微降至93.71，但结合PLI后可恢复至93.83，且均优于基线93.56。

本方法的核心架构建立在预训练文本到视频扩散模型（T2V-DM）的 3D U-Net 之上，通过三个关键模块的组合实现运动与外观的解耦定制。整体推理流程如图 Figure 2(a) 所示。

### 双路径 LoRA 训练框架

遵循 MotionDirector（Zhao et al., arXiv 2023）的设计，本方法采用双路径 LoRA 适配方案。训练时同时优化两条低秩适配路径：空间 LoRA 用于重建参考视频的外观，时间 LoRA 用于捕获运动模式，而预训练模型的所有参数保持冻结。时间 LoRA 的训练损失函数为：

$$ \operatorname* { m i n } _ { \theta _ { t p } } \mathbb { E } _ { z _ { 0 } , y , t , \epsilon } \left[ \left\| \epsilon - \epsilon _ { \theta , \theta _ { t p } } ( z _ { t } , y , t ) \right\| _ { 2 } ^ { 2 } \right] $$

其中 $\theta_{tp}$ 为时间 LoRA 的可训练参数，$z_0$ 为干净视频潜变量，$y$ 为文本条件，$t$ 为时间步，$\epsilon$ 为添加的高斯噪声，$\epsilon_{\theta,\theta_{tp}}$ 表示融入了时间 LoRA 的 U-Net 预测噪声。该损失函数的优化目标是使模型学会从噪声潜变量 $z_t$ 中预测出与真实噪声 $\epsilon$ 一致的噪声，从而隐式地编码参考视频的运动信息。

### 时间注意力净化（Temporal Attention Purification, TAP）

TAP 是解决外观泄漏问题的核心机制。其设计洞察在于：预训练时间注意力中的 Value 嵌入已包含丰富的运动描述基础组件，只需通过 LoRA 调整 Key 嵌入来重塑注意力权重矩阵，即可重新组合出新的运动模式，而无需直接修改 Value 嵌入本身。

具体而言，如图 Figure 2(b) 所示，TAP 将时间 LoRA 的注入范围严格限制在时间 Transformer 中注意力机制的 Key 嵌入（$W_K$）上，完全避免对 Value 嵌入（$W_V$）和前馈网络（$W_{ff}$）的修改。这一约束有效地阻断了参考视频外观信息通过 Value 嵌入向后传播的路径。

**设计选择的实验验证**：Table 1 的探测实验系统地比较了在时间注意力 Transformer 的不同线性层上应用 LoRA 的效果。结果显示，仅适配 $W_K$ 可在维持较高运动质量（64.3）的同时，显著提升外观对齐度（25.52）并降低外观泄漏（21.33）。相比之下，同时适配所有线性层的 MotionDirector 虽然运动质量相近（64.1），但外观对齐度大幅下降至 21.26，外观泄漏升至 21.66。适配 $W_V$ 或 $W_{ff}$ 同样会导致外观对齐度的明显退化。这一对比直接验证了限制 LoRA 作用范围为 Key 嵌入的必要性。

### 外观高速公路（Appearance Highway, AH）

AH 模块旨在进一步阻断外观信息通过 U-Net 跳跃连接向解码器传播。标准的 3D U-Net 跳跃连接将编码器中时间 Transformer 的输出直接送入解码器的对应层。然而，由于时间 Transformer 已被时间 LoRA 适配，其输出中不可避免地混合了来自参考视频的外观特征。

AH 的修改策略如图 Figure 2(c) 所示：将每个跳跃连接的起点从 LoRA 适配后的时间 Transformer 输出，改为未适配的空间 Transformer 输出。空间 Transformer 仅由空间 LoRA 进行外观重建训练，其输出更忠实地保留了基础模型的原始外观生成能力，从而绕过了被运动 LoRA“污染”的时间 Transformer 路径。

**AH 有效性的机制验证**：

- **定性分析**（Figure 3）：在生成“一只猴子在开满鲜花的草地上打高尔夫球”的视频时，增大 AH 的缩放因子 $\beta$ 可逐步消除生成视频中误出现的“窗户”（来自参考视频的外观泄漏），而等比例放大标准跳跃连接则毫无效果。这直观地证明了 AH 是抑制外观泄漏的关键结构。

![[assets/figures/papers/paper_list_l1837_Separate_Motion_from_Appearance_Customizing_Motion_via_Customizing_Text/figures/004_Figure_3.jpg]]
*Figure 3: The comparison between the Appearance Highway and the Skip Connection is illustrated in the figure. The figure presents videos generated by “A monkey is playing golf on a field full of flowers”. The first row shows that as the scale of the appearance highway increases, appearance leakage is progressively alleviated. In contrast, the second row shows that increasing the scale of the vanilla skip connection has no impact on appearance leakage. The smaller images below each main image represent subsequent frames of the video*

- **定量分析**（Figure 4）：通过比较不同模型隐藏状态的余弦相似度发现：(a) AH 使解码器隐藏状态与原始 T2V-DM 的相似度显著高于仅使用 TAP 的情况，表明 AH 有效恢复了基础模型的外观生成能力；(b) 同时，AH 的隐藏状态与注入空间 LoRA 的 T2V-DM 相似度更低，说明 AH 成功阻断了空间 LoRA 所携带的外观信息；(c) 运动分类器仍将大部分 AH 隐藏状态识别为 TAP 运动，证明 AH 并未破坏已编码的运动信息。

### 分阶段 LoRA 集成（Phased LoRA Integration, PLI）

PLI 是一种推理阶段的策略，用于在运动建模与外观细节生成之间取得更优平衡。其核心思想是：去噪过程的早期步骤主要决定视频的整体结构和运动模式，而后期步骤则负责细化外观细节。

PLI 的推理公式为：

$$ z_{t-1} = \begin{cases} \frac{1}{\sqrt{\alpha_t}} \left( z_t - \frac{1-\alpha_t}{\sqrt{1-\bar{\alpha}_t}} \epsilon_\theta(z_t, t) \right) + \sigma_t, & t \leq \tau \\ \frac{1}{\sqrt{\alpha_t}} \left( z_t - \frac{1-\alpha_t}{\sqrt{1-\bar{\alpha}_t}} \epsilon_{\theta,\theta_K}(z_t, t) \right) + \sigma_t, & t > \tau \end{cases} $$

其中 $\tau$ 为预设的时间步阈值。当 $t > \tau$（早期去噪步）时，使用引入了 Key LoRA 的适配模型 $\epsilon_{\theta,\theta_K}$ 进行去噪，专注于塑造目标运动模式；当 $t \leq \tau$（后期去噪步）时，切换回原始 T2V-DM $\epsilon_\theta$ 进行去噪，充分利用预训练模型的先验知识来完善外观细节和纹理。$\alpha_t$、$\bar{\alpha}_t$ 和 $\sigma_t$ 为 DDIM 去噪过程中的标准系数。

通过这种分阶段切换，PLI 既保证了运动建模的精度，又避免了适配模型在后期去噪步骤中对外观细节的潜在干扰。

## 实验与关键发现

### 主实验结果：一次性运动定制

在一次性运动定制基准上，本方法在文本对齐（Text Alignment）和视频语义一致性（ViCLIP Score）两项核心指标上均超越现有最优基线。**Table 2** 显示，我们的方法取得 **28.52** 的文本对齐分数，相较 MotionDirector（Zhao et al., arXiv 2023）的 27.55 提升 **+0.97**；ViCLIP Score 达到 **26.52**，相较 MotionDirector 的 25.54 提升 **+0.98**。这一提升源于 TAP 和 AH 的联合作用：TAP 阻断了外观信息通过 Value 嵌入混入运动编码的路径，而 AH 进一步恢复了基础模型的外观生成能力，使生成视频的外观更贴合文本描述。

![[assets/figures/papers/paper_list_l1837_Separate_Motion_from_Appearance_Customizing_Motion_via_Customizing_Text/figures/007_Table_2.jpg]]
*Table 2: Quantitative results on few-shot. In human evaluation, the paired numbers show our method’s voting rate on the left, while previous methods’ voting rate on the right*

在时间一致性（Temporal Consistency）上，我们的方法（93.83）同样优于 MotionDirector（93.56），表明运动分离策略并未损害时序建模质量。与无需微调的方法相比，VideoComposer（Wang et al., NeurIPS 2024）和 Ctrl-A-Video（Chen et al., arXiv 2023）在运动忠实度上明显不足，这验证了针对特定运动概念进行微调的必要性。

定性结果（**Figure 5**）直观展示了外观泄漏的抑制效果：在“两只灰鲨在蓝色海洋的珊瑚礁上游动”等场景中，MotionDirector 生成视频的背景会意外出现参考视频中的元素（如“窗户”），而我们的方法成功消除了此类伪影，生成的外观与文本描述高度一致。

![[assets/figures/papers/paper_list_l1837_Separate_Motion_from_Appearance_Customizing_Motion_via_Customizing_Text/figures/006_Figure_5.jpg]]
*Figure 5: Qualitative results on one-shot. Tune-A-Video [38], VMC [18], MotionDirector [47] and our method need to fine-tune. VideoComposer [35] and Ctrl-A-Video [7] are training free*

### 少样本运动定制

在少样本设定下（**Table 3**），我们的方法在无需额外图像条件的情况下，仍取得具有竞争力的表现。相较需要 Stable Diffusion 生成图像作为条件输入的 LAMP（Wu et al., CVPR 2024）和 DreamVideo（Wei et al., CVPR 2024），我们的方法在输入要求更简洁的前提下保持了相当的文本对齐和运动质量，证明了运动-外观分离策略的泛化能力。

![[assets/figures/papers/paper_list_l1837_Separate_Motion_from_Appearance_Customizing_Motion_via_Customizing_Text/figures/009_Table_3.jpg]]
*Table 3: Quantitative results on few-shot. In human evaluation, the paired numbers show our method’s voting rate on the left, while previous methods’ voting rate on the right*

### 消融实验：组件贡献

**Table 4** 的逐步消融清晰揭示了各组件的累积贡献。以 MotionDirector 为基线（文本对齐 27.55），依次添加各组件：
- 单独引入 **TAP**：文本对齐提升至 **27.91**（+0.36），验证了仅适配 Key 嵌入对抑制外观泄漏的直接作用；
- 叠加 **AH**：文本对齐进一步跃升至 **28.32**（+0.41），表明 AH 有效恢复了被时间 LoRA 削弱的外观生成能力；
- 最终加入 **PLI**：文本对齐达到 **28.52**（+0.20），实现了运动建模与外观保真度的最优平衡。

值得注意的是，单独使用 AH 会使时间一致性从 93.86 微降至 93.71，但结合 PLI 后可恢复至 93.83，且均优于基线 93.56。这说明 PLI 的分阶段推理策略（早期步用适配模型塑形运动，后期步用原始模型完善外观）有效缓解了 AH 对时序连贯性的轻微负面影响。

### 关键设计验证

**TAP 的模块选择依据**（**Table 1**）：
在时间注意力 Transformer 中，仅适配 Key 嵌入（W_K）取得了运动质量（64.3）与外观对齐（25.52）的最佳平衡，外观泄漏（21.33）与适配 Query 嵌入（W_Q）相当，但显著优于适配 Value 嵌入（W_V，运动质量 62.4，外观对齐 22.88）或前馈网络（W_ff，运动质量 69.2 但外观对齐仅 21.23）。这证实了核心洞察：预训练的 Value 嵌入已包含丰富的运动基础组件，仅需通过 LoRA 重塑 Key 嵌入的注意力权重即可重组出新的运动模式，而修改 Value 嵌入会不可避免地将外观信息编码进运动表示。

**AH 的机制验证**（**Figure 3**, **Figure 4**）：
增大 AH 的缩放因子 β 可逐步消除生成视频中的外观泄漏（如误出现的“窗户”），而等比例放大标准跳跃连接则毫无效果（**Figure 3**）。隐藏状态分析（**Figure 4**）从表征层面揭示了原因：AH 使解码器隐藏状态更接近原始 T2V-DM（图 4a），同时更远离注入空间 LoRA 的模型（图 4b），证明 AH 有效恢复了基础模型的外观生成能力；运动分类器仍将大部分 AH 隐藏状态识别为 TAP 运动（图 4c），表明 AH 并未破坏运动信息。

**AH 的实施灵活性**（**Table 5**）：
在训练时采用 AH 与仅在推理时作为后处理使用 AH，各项指标几乎相同（VBench Average 76.21 vs. 76.33），表明 AH 可作为即插即用的推理策略灵活部署，无需重新训练。

### 超参数敏感性

**Table 6** 展示了 AH 缩放因子 β 的影响。β=1.1 时获得最佳文本对齐和美学分数；β 过小（如 1.0）无法充分抑制外观泄漏，β 过大（如 1.2）则会导致性能下降，可能源于过度放大空间特征破坏了运动-外观的信息平衡。目前 β 和 PLI 阈值 τ 的最优值仍需通过网格搜索确定，缺乏理论上的自动化选择机制。

### 失败模式与局限性

尽管外观泄漏得到显著抑制，但在参考视频外观与目标文本描述高度冲突的场景下，仍可能残留少量泄漏。方法需针对每一个新的运动概念收集参考视频并进行微调，无法实现零样本泛化。此外，目前仅在 ZeroScope 和 ModelScope 两种 3D U-Net 架构上验证，迁移到其他视频扩散架构（如 DiT-based 模型）的有效性尚待实验确认。

![[assets/figures/papers/paper_list_l1837_Separate_Motion_from_Appearance_Customizing_Motion_via_Customizing_Text/figures/008_Figure_6.jpg]]
*Figure 6: Qualitative results on few-shot. During training, few videos from UCF Sports dataset [25, 30] are used as reference videos. During inference, we use Stable Diffusion to generate images paired with the texts, which serve as the image conditions for LAMP [40] and DreamVideo [37]. MotionDirector [47] and our method do not need image conditions*

## 定位与知识库关联

### 1. 问题定位：外观泄漏瓶颈

文本到视频扩散模型（T2V-DM）的运动定制任务面临一个核心瓶颈：现有方法在从参考视频中学习运动模式时，不可避免地会将参考视频的外观信息（如背景物体、颜色、纹理）编码到运动表示中，导致生成视频的外观与文本描述出现偏差——即**外观泄漏**。典型表现如 **MotionDirector** (Zhao et al., arXiv 2023) 在将“骑自行车”的运动迁移到新场景时，参考视频中的“窗户”元素会意外出现在生成结果中（Figure 1）。这一问题的根源在于，当前方法对时间注意力模块中所有线性层（Q, K, V, ff）统一施加低秩适配（LoRA），使得外观信息通过 Value 嵌入和后续的跳跃连接扩散至整个解码器，削弱了基础模型原有的多样化外观生成能力。

### 2. 方法谱系：运动定制的两条技术路线

运动定制方法可大致分为两条技术路线：

**路线一：基于微调的运动定制。** 此类方法在推理时针对每个参考视频进行个性化微调，以捕获运动模式。代表工作包括：
- **Tune-A-Video** (Wu et al., ICCV 2023)：通过扩展文本到图像扩散模型实现一次性视频定制，但缺乏对运动和外观的显式解耦。
- **MotionDirector** (Zhao et al., arXiv 2023)：引入双路径 LoRA 分别建模外观和运动，是目前运动定制的主要基线。然而其运动 LoRA 作用于时间注意力的全部线性层，导致外观泄漏。
- **VMC** (Jeong et al., CVPR 2024)：基于噪声残差进行运动定制，但同样未显式处理外观-运动纠缠问题。

**路线二：无需训练的运动转移。** 此类方法通过解耦表示或条件注入实现零样本运动迁移：
- **VideoComposer** (Wang et al., NeurIPS 2024)：将运动视为可控条件之一，通过组合式生成实现运动转移，但运动一致性弱于微调方法。
- **Ctrl-A-Video** (Chen et al., arXiv 2023)：通过可控生成框架实现文本引导的视频编辑与运动控制。

本文方法属于路线一，但在运动-外观解耦机制上做出了根本性改进。

### 3. 因果调控机制：TAP + AH + PLI 的递进式解耦

本文提出三个递进式调控手段，从信息流和训练-推理协同两个层面阻断外观泄漏：

**（1）时间注意力纯化（TAP）：阻断 Value 嵌入的外观注入。** 核心洞察在于，预训练的时间注意力 Value 嵌入已包含描绘运动所需的丰富基础组件（如物体移动、变形的基本模式），通过 LoRA 调整 Key 嵌入重塑注意力权重，即可重新组合这些组件以产生新的运动，而无需修改 Value 嵌入本身。Table 1 的探测实验证实：仅适配 Key 嵌入（W_K）在保持较高运动质量（64.3）的同时，显著提升外观对齐度（25.52）并降低外观泄漏（21.33），效果优于适配全部线性层的 MotionDirector（运动 64.1，外观对齐 21.26，外观泄漏 21.66）。

**（2）外观高速公路（AH）：切断外观信息的跳跃连接传播。** 标准 U-Net 跳跃连接将时间 Transformer 的输出直接送入解码器，使得 LoRA 适配后的时间特征（含外观泄漏）污染解码过程。AH 将跳跃连接的起点从时间 Transformer 输出改为空间 Transformer 输出，绕过 LoRA 适配的时间模块，使解码器接收更接近原始 T2V-DM 的外观特征。Figure 3 的定性对比显示，增大 AH 的缩放因子可逐步消除生成视频中的外观泄漏（如“窗户”元素），而等比例放大标准跳跃连接则毫无效果。Figure 4 的隐藏状态分析进一步验证：AH 使解码器隐藏状态更接近原始 T2V-DM（外观恢复），同时运动分类器仍将大部分 AH 隐藏状态识别为目标运动（运动保持）。

**（3）分阶段 LoRA 集成（PLI）：训练-推理协同的运动-外观分工。** 推理时，前 τ 步使用带 TAP 和 AH 的适配模型专注于运动建模，后续步骤切换回原始 T2V-DM 完善外观细节。这一策略利用了去噪过程中早期步骤决定全局结构（运动），后期步骤细化局部细节（外观）的特性。

### 4. 与相关工作的关键差异

| 维度 | MotionDirector | 本文方法 |
|------|---------------|---------|
| LoRA 作用范围 | 全部线性层 (Q, K, V, ff) | 仅 Key 嵌入 (TAP) |
| 跳跃连接起点 | 时间 Transformer 输出 | 空间 Transformer 输出 (AH) |
| 推理策略 | 全程使用适配模型 | 分阶段切换 (PLI) |
| 外观泄漏控制 | 无显式机制 | TAP + AH 双重阻断 |

在少样本场景中，**LAMP** (Wu et al., CVPR 2024) 和 **DreamVideo** (Wei et al., CVPR 2024) 需要额外使用 Stable Diffusion 生成的图像作为条件输入，而本文方法与 MotionDirector 均无需图像条件，更具实用性。

### 5. 适用边界与局限

**适用场景：**
- 一次性或少量参考视频的运动定制，如将特定人物的走路姿态迁移到不同外观的角色上。
- 需要保持文本描述外观一致性的场景，如“一只猴子在花丛中打高尔夫球”要求不出现参考视频中的无关物体。
- 基于 ZeroScope 或 ModelScope 等 3D U-Net 架构的 T2V-DM。

**已知局限：**
- **需要逐概念微调：** 每个新运动概念需收集参考视频并重新训练 LoRA，无法实现零样本泛化。
- **极端冲突场景的残留泄漏：** 当参考视频外观与目标文本描述高度冲突时（如参考视频为室内场景，目标为户外场景），仍可能残留少量外观泄漏。
- **架构迁移未验证：** 目前仅在 ZeroScope 和 ModelScope 两种 3D U-Net 架构上验证，迁移到 DiT 等其他视频扩散架构的有效性未知。
- **超参数敏感性：** 分阶段阈值 τ 和 AH 缩放因子 β 需手动调节（Table 6 显示 β=1.1 时最优），缺乏自动化确定机制。

### 6. 开放问题与未来方向

1. **超参数自适应：** τ 和 β 的最佳值如何根据参考视频的运动复杂度和外观冲突程度自动确定？是否存在理论上的最优解？
2. **多概念扩展：** 能否扩展该方法以同时定制多个运动概念，并实现不同运动间的组合、插值与平滑过渡？
3. **架构泛化：** TAP 和 AH 的思想是否适用于其他视频生成任务（如视频编辑、帧插值、风格迁移）和其他扩散架构（如 DiT）？
4. **鲁棒性边界：** 在更多样化、更复杂背景的数据集（如 WebVid 或自采集数据）上，方法的鲁棒性如何？外观泄漏的抑制效果是否具有跨域一致性？
5. **评价体系完善：** 当前基于 CLIP 的外观泄漏度量指标是否能完全反映人类感知？是否需要引入更精确的细粒度外观保真度评价体系？
6. **训练效率优化：** 双路径 LoRA 训练和分阶段推理的计算开销能否进一步压缩，以支持实时或交互式运动定制？

## 原文 PDF

![[paperPDFs/arxiv_2025/Separate_Motion_from_Appearance_Customizing_Motion_via_Customizing_Text_to_Video_Diffusion_Models.pdf]]
