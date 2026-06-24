---
title: CAMDM Taming Diffusion Probabilistic Models for Character Control
type: paper
paper_level: A
venue: SIGGRAPH
year: 2024
pdf_ref: paperPDFs/SIGGRAPH_2024/CAMDM_Taming_Diffusion_Probabilistic_Models_for_Character_Control.pdf
aliases:
- CAMDMC
- CTDPMCC
tags:
- SIGGRAPH_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 无分类器引导（Classifier-Free Guidance）作用于历史运动标记（past motion token）的尺度 γ，控制模型对历史运动的依赖程度，是解决风格过渡的核心因果机制。
primary_logic: 将扩散模型自回归地应用于角色控制时，必须解决条件歧义、轨迹不一致与风格过渡难题；通过分别对历史运动、风格标签和轨迹信号进行独立 token 化、在历史运动标记上应用无分类器引导、以及启发式地扩展预测轨迹，可以仅用 8 步扩散在实时条件下生成高质量、多样化且可控的角色动画。
claims:
- CAMDM 在单风格控制中取得 FID 0.913，风格准确率 89.5%，显著优于所有基线方法（LMP, MANN‑DP, MM‑DP, MoGlow）。
- 多风格控制中，CAMDM 的风格过渡成功率达 94.2%，远超在风格标记上应用 CFG 的变体（8.9%），验证了 CFG‑PM 的核心作用。
- 仅使用 8 个扩散步骤即可在 RTX 3060 上实现每代 13 ms 的推理速度，且 FID 保持 0.913，证明 CAMDM 达到了实时高质量生成的最佳平衡。
- 单风格控制（大规模 mocap 运动数据集） 上 FID = 0.913
---

# CAMDM Taming Diffusion Probabilistic Models for Character Control

> [!tip] 核心洞察
> 将扩散模型自回归地应用于角色控制时，必须解决条件歧义、轨迹不一致与风格过渡难题；通过分别对历史运动、风格标签和轨迹信号进行独立 token 化、在历史运动标记上应用无分类器引导、以及启发式地扩展预测轨迹，可以仅用 8 步扩散在实时条件下生成高质量、多样化且可控的角色动画。

| 字段 | 内容 |
|------|------|
| 中文题名 | CAMDM：驯服扩散概率模型实现角色控制 |
| 英文题名 | CAMDM Taming Diffusion Probabilistic Models for Character Control |
| 会议/期刊 | SIGGRAPH 2024 |
| Links | [Code](https://github.com/onnx/onnx) · [paper](https://doi.org/10.1145/3592395) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | Conditional Autoregressive Motion Diffusion Model (CAMDM) |
| Dataset | 单风格控制（大规模 mocap 运动数据集）, 实时推理效率（8 步扩散） |

> [!tip] 效果简介
> - 单风格控制（大规模 mocap 运动数据集） 上，FID 0.913 vs 所有基线方法（成绩优于它们） (显著优于所有基线)。
> - 单风格控制 上，风格准确率 (Style Accuracy) 89.5% vs 所有基线方法（成绩优于它们） (最优)。
> - 多风格控制 上，风格过渡成功率 (Success Rate) 94.2% vs 所有基线方法（成绩优于它们） (最优)。

## 概述

本报告对 **CAMDM：驯服扩散概率模型实现角色控制**（ACM Trans. Graph., 2023）进行结构化解读。报告聚焦于该工作如何解决确定性运动生成模型在角色控制中长期存在的核心瓶颈，梳理其因果机制、方法定位与关键实证结果。

### 核心问题与瓶颈

实时角色控制的根本挑战在于：确定性运动生成模型（如自回归神经网络）难以捕捉真实运动的多模态分布，导致生成动作陷入“均值姿态”——输出单一、缺乏多样性，并伴随脚滑动等伪影。尤其在用户切换风格标签时，现有方法缺乏灵活的过渡机制，无法在保持运动质量的同时平滑衔接不同风格。

### 核心洞察与因果机制

CAMDM 的核心洞察在于将扩散模型自回归地应用于角色控制时，必须系统性地解决三个关键难题：**条件歧义**、**轨迹不一致**与**风格过渡**。其因果调控的核心旋钮是作用于历史运动标记（past motion token）的**无分类器引导（Classifier-Free Guidance, CFG）**尺度 γ。当用户切换风格时，通过将 γ 降至 0.7，模型主动降低对历史运动的依赖，从而在缺乏过渡数据的条件下实现平滑的风格切换——这是解决风格过渡难题的核心因果机制。

### 方法定位：方法谱系与知识库定位

CAMDM 属于**条件自回归运动扩散模型**，其方法定位可通过与基线方法的差异化设计来理解：

| 设计维度 | 基线做法 | CAMDM 设计 |
|----------|----------|-------------|
| 条件表示 | 所有条件拼接为单一特征向量 | 独立条件 Token 化（Separate Condition Tokenization），通过 Transformer 注意力融合 |
| 无分类器引导目标 | 作用于风格标签（CFG-S）或不使用 | 作用于历史运动标记（CFG-PM），风格切换时 γ=0.7 |
| 轨迹对齐 | 直接混合预测轨迹与用户合成轨迹 | 启发式未来轨迹扩展（HFTE）：复用最后 K=4 个预测点循环扩展 |
| 扩散步骤 | 1000 步（标准扩散） | 8 步（训练与推理均使用 8 步） |
| 去噪预测目标 | 预测添加的噪声 ε | 直接预测干净信号 x₀（便于施加几何损失） |

在基线对比中，CAMDM 与 **MoGlow**（Henter et al., TOG 2020）等基于归一化流的概率控制方法形成对照——后者不支持朝向控制。相较于 LMP、MANN-DP、MM-DP 等实时控制基线，CAMDM 在单风格与多风格场景下均取得显著优势。

### 主要实证结果

**单风格控制**：CAMDM 取得 FID 0.913、风格准确率 89.5%，显著优于所有基线方法（Table 1）。在相同控制输入下，其生成的运动多样性远超确定性基线（Figure 4）。

**多风格控制**：风格过渡成功率达 94.2%，远超在风格标记上应用 CFG 的变体（仅 8.9%），直接验证了 CFG-PM 在风格切换中的核心作用（Table 2 & Table 4）。即使在数据集中不存在过渡样本的风格对之间，CAMDM 也能生成自然过渡（Figure 5）。

**实时推理效率**：仅使用 8 个扩散步骤，在 RTX 3060 上每次自回归生成仅需 13 ms，同时保持 FID 0.913 的高质量——这是实时控制与生成质量的最佳平衡点（Table 5）。

**消融实验**：完整模型在 FID、脚滑动和轨迹误差三个指标上均优于所有消融版本，验证了独立条件 Token 化、CFG-PM 和 HFTE 三个组件的不可或缺性（Table 3）。

## 背景与动机

### 问题背景：确定性生成模型的多样性困境

在实时角色动画控制中，核心挑战在于如何根据用户的高级控制信号（如摇杆方向、风格标签）生成自然、多样且物理合理的运动。传统方法通常采用确定性运动生成模型，即给定相同的控制输入，模型始终输出完全相同的运动序列。这种确定性范式带来了三个相互关联的严重缺陷：

1. **均值姿态坍塌**：当模型在自回归循环中反复生成未来运动时，确定性预测倾向于回归到训练数据中该控制信号下的“平均”运动，导致角色动作逐渐丧失个性与表现力。
2. **低多样性**：用户即使在相同控制输入下反复操作，也无法获得不同的运动变体。这对于需要丰富表现的游戏角色或交互式虚拟人而言，是一个根本性的限制。
3. **脚滑动伪影**：在自回归生成过程中，预测误差会逐帧累积，导致角色脚部与地面之间出现明显的滑动现象，破坏运动真实感。

这些问题在风格切换场景下被进一步放大。当用户改变风格标签时（例如从“正常行走”切换为“跳跃”），确定性模型缺乏灵活的过渡机制，往往产生生硬、不自然的动作衔接。

### 现有方法的缺口

近年来，扩散概率模型（Diffusion Probabilistic Models）在图像和视频生成领域取得了突破性进展，其核心优势在于能够捕捉复杂、多模态的数据分布。然而，将扩散模型应用于实时角色控制面临三重挑战：

- **条件歧义**：角色控制涉及多种异构条件信号（历史运动、风格标签、轨迹约束、朝向约束），简单地将它们拼接为单一特征向量输入网络，会导致条件之间相互干扰，控制稳定性差。
- **轨迹不一致**：在自回归推理过程中，模型预测的未来轨迹长度与用户提供的合成轨迹长度可能不匹配，直接混合不同长度的轨迹会引发运动抖动。
- **风格过渡困难**：标准扩散模型在风格切换时缺乏专门机制来调节历史运动与风格条件之间的平衡，导致过渡生硬或失败。

此外，现有的实时角色控制方法（如 LMP、MANN-DP、MM-DP）虽然能实现低延迟推理，但均为确定性模型，无法解决多样性不足的问题。而基于归一化流的 MoGlow（Henter et al., TOG 2020）虽然支持概率生成，却不支持朝向控制，且风格过渡能力有限。

### 本文动机与核心思路

本文的核心洞察是：**将扩散模型自回归地应用于角色控制时，必须解决条件歧义、轨迹不一致与风格过渡三大难题**。为此，CAMDM 提出了三项关键设计：

1. **独立条件标记化（Separate Condition Tokenization）**：为历史运动、风格标签、根位移和根方向分别学习独立的 token，通过 Transformer 注意力机制实现条件间的有效融合，消除条件歧义。
2. **历史运动标记上的无分类器引导（CFG-PM）**：将无分类器引导（Classifier-Free Guidance）作用于历史运动标记而非风格标记，通过调节引导尺度 γ 控制模型对历史运动的依赖程度。当用户切换风格时，降低 γ 至 0.7，使模型减少对历史运动的依赖，从而实现平滑、自然的风格过渡。
3. **启发式未来轨迹扩展（HFTE）**：当自回归触发导致预测轨迹短于用户合成轨迹时，通过循环复用最后 4 个轨迹点构造平滑扩展，解决轨迹长度不匹配导致的抖动问题。

这些设计使得 CAMDM 仅需 8 个扩散步骤即可在实时条件下生成高质量、多样化且可控的角色动画，从根本上突破了确定性模型在运动多样性上的瓶颈。

## 核心创新

CAMDM 的核心创新并非简单地“将扩散模型用于运动生成”，而是系统性地解决了将扩散模型**自回归部署**到实时角色控制时暴露出的三个深层瓶颈：条件歧义、轨迹不一致与风格过渡失能。为此，该方法在条件表示、引导策略、轨迹对齐和扩散加速四个维度上进行了针对性改造。

### 1. 独立条件标记化（Separate Condition Tokenization, SCT）

**基线做法：** 将历史运动、风格标签、根位移、根方向等所有条件拼接为单一特征向量，直接馈入网络。这种做法容易造成条件信号在特征空间中相互干扰，导致控制不稳定。

**CAMDM 创新：** 为每一种条件学习**独立的 token**（Separate Condition Tokenization），并将所有条件 token 置于噪声运动序列前端，一并输入 Transformer 编码器。通过自注意力机制，模型能够自适应地融合不同条件，而非被动接受一个混杂的拼接向量。这一设计从根源上缓解了条件歧义问题，是实现稳定控制的结构性前提（见 Figure 2 架构图）。

### 2. 历史运动标记上的无分类器引导（CFG-PM）

**基线做法：** 标准扩散模型不使用 CFG，或仅在风格标签上应用 CFG（CFG-S）以增强风格一致性。

**CAMDM 创新：** 将**无分类器引导（Classifier-Free Guidance）作用于历史运动标记（past motion token）**，而非风格标签。训练时以 15% 的概率将历史运动 token 置为空，推理时通过引导尺度 $\gamma$ 调节历史运动对生成的影响：

$$\mathcal{G}_{\gamma}(\mathbf{x}_{t}, t; \mathbf{p}, \mathbf{c}) = \mathcal{G}(\mathbf{x}_{t}, t; \mathbf{p}=\emptyset, \mathbf{c}) + \gamma \big( \mathcal{G}(\mathbf{x}_{t}, t; \mathbf{p}, \mathbf{c}) - \mathcal{G}(\mathbf{x}_{t}, t; \mathbf{p}=\emptyset, \mathbf{c}) \big)$$

当用户切换风格标签时，CFG-PM 被触发，$\gamma$ 设为 0.7，**主动削弱历史运动约束**，使模型更自由地生成符合新风格的运动，从而实现平滑的风格过渡。这一因果机制是 CAMDM 解决风格切换难题的核心——消融实验（Table 4）表明，若将 CFG 作用于风格标记（CFG-S），多风格过渡成功率将从 **94.2% 骤降至 8.9%**。

### 3. 启发式未来轨迹扩展（HFTE）

**基线做法：** 自回归触发时，直接混合模型预测轨迹与用户合成轨迹。当预测轨迹因部分帧已被应用而短于用户轨迹时，长度不匹配导致混合边界产生剧烈抖动。

**CAMDM 创新：** 提出启发式未来轨迹扩展（Heuristic Future Trajectory Extension）。当预测轨迹长度不足时，循环复用最后 $K=4$ 个预测点，每次复用都在最后一个轨迹点处建立局部坐标系，将位置翻转、方向复制，直至长度与用户合成轨迹匹配。这一轻量级启发式策略以极低计算成本消除了自回归触发时的轨迹不一致问题（见 Figure 3 示意图）。

### 4. 8 步扩散与直接预测 $x_0$

**基线做法：** 标准扩散模型通常需要 1000 步去噪，预测目标是添加的噪声 $\epsilon$。

**CAMDM 创新：** 仅使用 **8 个扩散步骤**进行训练和推理，且将预测目标从噪声 $\epsilon$ 改为**直接预测干净运动 $x_0$**。这一设计有两个关键收益：(1) 直接预测 $x_0$ 便于在训练中施加关节位置损失、脚接触损失等几何约束；(2) 8 步扩散在 RTX 3060 上实现每次自回归生成仅 **13 ms** 的推理延迟，同时保持 **FID 0.913** 的高质量，达到了实时控制与生成质量的最佳平衡（Table 5）。

### 创新总结

| 创新维度 | 基线做法 | CAMDM 做法 | 解决的核心问题 |
|---------|---------|-----------|-------------|
| 条件表示 | 单一拼接向量 | 独立条件标记化 (SCT) | 条件歧义 |
| 无分类器引导 | 风格标签 CFG 或不使用 | 历史运动标记 CFG (CFG-PM) | 风格过渡失能 |
| 轨迹对齐 | 直接混合（长度不匹配时抖动） | 启发式未来轨迹扩展 (HFTE) | 轨迹不一致 |
| 扩散步骤 | 1000 步 | 8 步 + 直接预测 $x_0$ | 实时推理可行性 |

这些创新相互协同：SCT 提供稳定的条件融合基础，CFG-PM 赋予风格切换能力，HFTE 保障自回归轨迹平滑，8 步扩散使整个系统满足实时部署要求。消融实验（Table 3）证实，完整模型在 FID、脚滑动和轨迹误差三项指标上全面优于任一组件被移除的变体，验证了每个创新的不可或缺性。

## 整体框架

CAMDM 是一个条件自回归运动扩散模型，其核心 pipeline 由五个紧密协作的模块构成，形成“条件编码 → 扩散去噪 → 引导调节 → 轨迹对齐 → 自回归控制”的闭环。

**输入与输出流**：在每一帧，系统收集角色过去 10 帧的历史姿态 **p** 以及用户提供的高层控制信号，包括风格标签 **cₗ**、未来根位移 **cᵣᵥ** 和根方向 **cᵣₒ**。这些条件与随机采样的高斯噪声一起输入去噪网络，网络直接预测未来 45 帧的干净运动 $\hat{\mathbf{x}}_0$（而非预测噪声 $\epsilon$），随后将部分预测姿态应用到角色上，完成一帧动画的生成。

**Separate Condition Tokenization (SCT)**：不同于将全部条件拼接为单一特征向量的传统做法，SCT 为历史运动、风格标签、根位移和根方向分别学习独立的 token，并将这些条件 token 附加到噪声运动序列的开头，一并送入 Transformer 编码器。通过注意力机制，模型能够有效利用每种条件的独特信息，从而获得稳定的控制效果——这是解决条件歧义问题的关键设计。

**Denoising Transformer Encoder**：去噪网络采用纯编码器架构的 Transformer，接收噪声运动 token 与全部条件 token，在每一个扩散步直接预测干净运动 $\hat{\mathbf{x}}_0$。训练时仅使用 8 个扩散步骤，损失函数为四项几何损失的加权和：
$$\mathcal{L} = \lambda_{\mathrm{samp.}} \mathcal{L}_{\mathrm{samp.}} + \lambda_{\mathrm{pos.}} \mathcal{L}_{\mathrm{pos.}} + \lambda_{\mathrm{foot.}} \mathcal{L}_{\mathrm{foot}} + \lambda_{\mathrm{vel.}} \mathcal{L}_{\mathrm{vel}}$$
其中 $\mathcal{L}_{\mathrm{samp.}}$ 是预测干净运动与真实干净运动的均方误差，$\mathcal{L}_{\mathrm{pos.}}$ 通过正向运动学计算全局关节位置误差，$\mathcal{L}_{\mathrm{foot}}$ 和 $\mathcal{L}_{\mathrm{vel}}$ 分别约束脚部接触与运动速度。

**Classifier-Free Guidance on Past Motion (CFG-PM)**：推理时，无分类器引导作用于历史运动标记 **p** 而非风格标记。训练阶段以 0.15 的概率将历史运动 token 置为空，使模型学会在有无历史运动条件下进行预测。推理时通过引导尺度 $\gamma$ 调节历史运动的影响：
$$\mathcal{G}_{\gamma}(\mathbf{x}_{t}, t; \mathbf{p}, \mathbf{c}) = \mathcal{G}(\mathbf{x}_{t}, t; \mathbf{p}=\emptyset, \mathbf{c}) + \gamma \big( \mathcal{G}(\mathbf{x}_{t}, t; \mathbf{p}, \mathbf{c}) - \mathcal{G}(\mathbf{x}_{t}, t; \mathbf{p}=\emptyset, \mathbf{c}) \big)$$
当用户切换风格标签时，将 $\gamma$ 设为 0.7 以降低历史运动约束，实现平滑的风格过渡——这是解决风格过渡难题的核心因果机制。

**Heuristic Future Trajectory Extension (HFTE)**：自回归触发时，模型预测的未来轨迹因已应用部分帧而短于用户提供的合成轨迹，直接混合会导致抖动。HFTE 循环复用预测轨迹的最后 K=4 个点：每次复用都在最后一个轨迹点处建立局部坐标系，翻转位置并复制朝向，直至长度匹配用户合成轨迹，从而消除轨迹不一致问题。

**Autoregressive Controller**：运行时逐帧收集历史姿态和控制信号，调用上述扩散流程生成未来运动，并将预测运动的部分帧应用到角色。训练时预测长未来运动（45 帧）并应用尽可能多的帧，显著提升了自回归过程中的风格内多样性。

### 补充图表

![[assets/figures/papers/paper_list_l1922_CAMDM_Taming_Diffusion_Probabilistic_Models_for_Character_Control/figures/002_Figure_2.jpg]]
*Figure 2: Conditional Autoregressive Motion Diffusion Model (CAMDM). At each denoising step, the model takes as input a noisy motion sample*

## 核心模块与公式推导

CAMDM 以条件自回归方式工作：给定角色过去 10 帧的运动 $\mathbf{p}$ 和用户控制参数 $\mathbf{c}$（包括风格标签 $\mathbf{c}_l$、未来根位移 $\mathbf{c}_{rv}$ 和根朝向 $\mathbf{c}_{ro}$），模型学习未来 45 帧运动 $\mathbf{x}$ 的条件分布。运行时，每帧收集历史姿态和控制信号，加入随机高斯噪声，通过扩散模型生成未来运动并部分应用到角色上，实现自回归控制。

### 去噪预测目标

与标准扩散模型预测噪声 $\epsilon$ 不同，CAMDM 在每个去噪步直接预测干净信号 $\hat{\mathbf{x}}_0$，以便施加几何损失：

$$\hat{\mathbf{x}}_{0} = \mathcal{G}(\mathbf{x}_{t}, t; \mathbf{p}, \mathbf{c}_{l}, \mathbf{c}_{rv}, \mathbf{c}_{ro})$$

其中 $\mathbf{x}_t$ 为噪声运动，$t$ 为扩散步，$\mathcal{G}$ 为基于 Transformer Encoder 的去噪网络。

### 独立条件标记化（Separate Condition Tokenization, SCT）

历史运动、风格标签、根位移和根方向分别通过独立的标记器编码为条件 token，拼接在噪声运动序列前端后输入 Transformer。通过注意力机制，模型能有效融合各类条件，避免将所有条件拼成单一向量时出现的控制不稳定。

### 无分类器引导作用于历史运动（CFG-PM）

为解决风格切换时的过渡难题，CAMDM 将无分类器引导（CFG）施加于历史运动标记 $\mathbf{p}$ 而非风格标记。训练时以 0.15 的概率将历史运动标记置为空；推理时，引导生成公式为：

$$\mathcal{G}_{\gamma}(\mathbf{x}_{t}, t; \mathbf{p}, \mathbf{c}) = \mathcal{G}(\mathbf{x}_{t}, t; \mathbf{p}=\emptyset, \mathbf{c}) + \gamma \big( \mathcal{G}(\mathbf{x}_{t}, t; \mathbf{p}, \mathbf{c}) - \mathcal{G}(\mathbf{x}_{t}, t; \mathbf{p}=\emptyset, \mathbf{c}) \big)$$

当用户切换风格标签时，触发 CFG-PM，将引导尺度 $\gamma$ 设为 0.7，降低历史运动对生成的约束，使模型能平滑过渡到新风格。这是实现 94.2% 风格过渡成功率的核心因果机制。

### 启发式未来轨迹扩展（Heuristic Future Trajectory Extension, HFTE）

自回归生成中，模型预测的未来轨迹（45 帧）会在应用部分姿态后短于用户提供的合成轨迹，直接混合不同长度的轨迹会导致运动抖动。HFTE 通过循环复用预测轨迹的最后 $K=4$ 个点来扩展轨迹：每次循环在最后一个轨迹点处建立局部坐标系，翻转位置并复制朝向，直至长度匹配用户轨迹。

### 训练损失

总损失为四项加权和，权重均设为 1：

$$\mathcal{L} = \lambda_{\mathrm{samp.}} \mathcal{L}_{\mathrm{samp.}} + \lambda_{\mathrm{pos.}} \mathcal{L}_{\mathrm{pos.}} + \lambda_{\mathrm{foot.}} \mathcal{L}_{\mathrm{foot}} + \lambda_{\mathrm{vel.}} \mathcal{L}_{\mathrm{vel}}$$

- **样本损失** $\mathcal{L}_{\mathrm{samp.}} = \mathbb{E} \|\hat{\mathbf{x}}_{0} - \mathbf{x}_{0}\|_{2}^{2}$：预测干净运动与真实运动的均方误差。
- **关节位置损失** $\mathcal{L}_{\mathrm{pos.}} = \|\mathrm{FK}(\hat{\mathbf{x}}_{0}, \mathbf{S}) - \mathrm{FK}(\mathbf{x}_{0}, \mathbf{S})\|_{2}^{2}$：通过正向运动学 FK 将局部姿态映射为全局关节位置后计算 MSE，骨架 $\mathbf{S}$ 为固定参数。
- **脚接触损失** $\mathcal{L}_{\mathrm{foot}}$ 和 **速度损失** $\mathcal{L}_{\mathrm{vel}}$：分别约束脚滑动和运动平滑性（具体公式未在给定材料中完整呈现）。

### 实时推理

训练和推理均仅使用 8 个扩散步骤，在 RTX 3060 上每次自回归生成仅需 13 ms，在保持 FID 0.913 的同时满足实时控制需求。

### 补充图表

![[assets/figures/papers/paper_list_l1922_CAMDM_Taming_Diffusion_Probabilistic_Models_for_Character_Control/figures/003_Figure_3.jpg]]
*Figure 3: Illustration of heuristic future trajectory extension. Top*

## 实验与分析

### 核心实验设计

为全面评估 CAMDM 的角色控制能力，作者构建了三个递进的实验场景：**单风格控制**（验证生成质量与多样性）、**多风格控制**（验证风格过渡能力）以及**实时推理效率**（验证工程可行性）。所有实验均在同一大规模运动捕捉数据集上训练，并使用完全相同的用户控制输入进行评估。对比基线包括四种代表性方法：**LMP**、**MANN-DP**、**MM-DP** 以及基于归一化流的 **MoGlow**（Henter et al., TOG 2020）。需注意 MoGlow 不支持朝向控制，因此朝向误差指标不适用于该基线。

### 单风格控制：质量与多样性

在单风格控制任务中，模型需根据用户提供的轨迹与风格标签生成多样化的运动序列。评估指标涵盖生成质量（FID）、风格一致性（Style Accuracy）、轨迹跟踪精度（Trajectory Error）、脚滑动程度（Foot Sliding）以及朝向误差（Orientation Error）。

如 Table 1 所示，CAMDM 在核心指标上全面超越所有基线方法：**FID 达到 0.913，风格准确率达到 89.5%**，均为最优成绩。相比之下，确定性方法（如 LMP、MANN-DP）虽然轨迹跟踪精度较高，但生成的运动多样性严重不足，在 FID 指标上表现较差；MoGlow 虽能生成多样化运动，但对控制信号的遵循度弱于 CAMDM。Figure 4 的可视化对比直观展示了这一差异：在完全相同的控制输入下，CAMDM 生成的左右手轨迹（红色与绿色）与根轨迹（黑色）在紧密跟随用户指令的同时，呈现出丰富的运动变化，而基线方法则倾向于产生均值化姿态或偏离控制轨迹。

![[assets/figures/papers/paper_list_l1922_CAMDM_Taming_Diffusion_Probabilistic_Models_for_Character_Control/figures/004_Table_1.jpg]]
*Table 1: Quantitative results on single-style character control. The orientation error is not applicable for MoGlow as it does not support facing direction control*

![[assets/figures/papers/paper_list_l1922_CAMDM_Taming_Diffusion_Probabilistic_Models_for_Character_Control/figures/010_Figure_4.jpg]]
*Figure 4: Visual comparisons of single-style control. From top to bottom: Ours, LMP, MANN-DP, MM-DP and MoGlow, all using the same control inputs. The trajectory of the left hand, right hand, and root are colored in red, green, and black, respectively. Observe the high diversity and better adherence to the control trajectory of our method compared to the other baselines*

这一结果验证了核心洞察：**扩散模型的自回归应用能够有效捕捉运动的多模态分布**，而分离式条件标记化（SCT）确保了控制信号的稳定传递，避免了单一特征向量拼接带来的条件歧义问题。

### 多风格控制：风格过渡机制

多风格控制是 CAMDM 最具挑战性的测试场景。实验设置中，用户在运动过程中切换风格标签（如从“LeftHop”切换至“RightHop”），模型需在后续 120 帧内平滑过渡到目标风格。评估指标为**风格过渡成功率（Success Rate）**，即生成运动被分类器判定为目标风格的比例。

Table 2 的结果显示，**CAMDM 的风格过渡成功率达到 94.2%**，远超所有基线方法。Figure 5 的可视化对比进一步揭示：基线方法在风格切换时往往出现运动僵直或风格混淆，而 CAMDM 能够生成自然流畅的过渡序列。这一能力的关键在于**无分类器引导作用于历史运动标记（CFG-PM）** 的设计：当用户切换风格时，推理过程将引导尺度 γ 设为 0.7，主动降低模型对历史运动的依赖，从而为新风格的涌现释放空间。Table 4 的消融实验提供了决定性证据：若将 CFG 作用于风格标记而非历史运动标记（CFG-S），过渡成功率从 94.2% 骤降至 8.9%，证明 CFG-PM 是解决风格过渡瓶颈的因果机制。

![[assets/figures/papers/paper_list_l1922_CAMDM_Taming_Diffusion_Probabilistic_Models_for_Character_Control/figures/005_Table_2.jpg]]
*Table 2: Quantitative results of multi-style character control. The target style label is given in the middle, and we record the character’s motion over the subsequent 120 frames*

![[assets/figures/papers/paper_list_l1922_CAMDM_Taming_Diffusion_Probabilistic_Models_for_Character_Control/figures/009_Table_4.jpg]]
*Table 4: Ours (w/ CFG-PM) vs. Ours w/ CFG-S. Ours w/ CFG-S leads to significantly degraded performance*

![[assets/figures/papers/paper_list_l1922_CAMDM_Taming_Diffusion_Probabilistic_Models_for_Character_Control/figures/011_Figure_5.jpg]]
*Figure 5: Visual comparisons of multi-style control. From top to bottom: Ours, LMP, MANN-DP, MM-DP and MoGlow. Our method can transition naturally between distinct styles (“LeftHop” and “RightHop” in this case), whereas baselines fail*

### 消融实验：各组件的不可替代性

Table 3 系统消融了 CAMDM 的三个核心组件：分离式条件标记化（SCT）、无分类器引导（CFG-PM）以及启发式未来轨迹扩展（HFTE）。完整模型在 FID（0.913）、脚滑动（0.685）和轨迹误差（22.818）三项指标上均优于所有消融版本，验证了每个组件的独立贡献：

![[assets/figures/papers/paper_list_l1922_CAMDM_Taming_Diffusion_Probabilistic_Models_for_Character_Control/figures/008_Table_3.jpg]]
*Table 3: Ablation study. Our full model performs best over all ablated versions*

- **移除 SCT**：将条件拼接为单一向量输入网络，导致控制信号相互干扰，FID 显著恶化，轨迹误差增大。
- **移除 CFG-PM**：模型在多风格切换时失去调节历史运动依赖的能力，过渡成功率大幅下降（见 Table 4）。
- **移除 HFTE**：当自回归触发导致预测轨迹短于用户合成轨迹时，直接混合不等长轨迹会引入运动抖动，表现为脚滑动和轨迹误差的明显增加。

### 实时推理效率：8 步扩散的工程折衷

扩散模型通常需要数百至上千步去噪，难以满足实时应用需求。CAMDM 的关键工程发现是：**仅使用 8 个扩散步骤即可在训练和推理中同时获得令人信服的生成质量**。Table 5 系统评估了不同扩散步数的影响：8 步配置在 RTX 3060 上实现每次自回归生成仅需 13 ms 的推理延迟，同时 FID 保持 0.913。将步数增加至 16 或 32 步仅带来微弱的 FID 改善（<0.02），但推理时间成倍增长；减少至 4 步则导致生成质量显著下降。这一结果确立了 8 步扩散作为实时高质量角色控制的最佳工程折衷点。

![[assets/figures/papers/paper_list_l1922_CAMDM_Taming_Diffusion_Probabilistic_Models_for_Character_Control/figures/007_Table_5.jpg]]
*Table 5: The effect of different diffusion steps*

### 失败模式与局限性

尽管 CAMDM 在实验设定下表现优异，仍需指出以下局限：

1. **计算负荷上限**：13 ms 的推理延迟虽满足实时要求，但 8 步扩散模型的计算量仍较高，难以直接部署至移动端或嵌入式设备。
2. **环境感知缺失**：当前模型仅在人类与平坦地面交互的运动数据上训练与验证，未涉及包含障碍物、楼梯等复杂环境感知的场景。
3. **控制接口表达力限制**：摇杆式控制信号仅能描述粗略的运动意图（方向、速度、风格），无法精确表达更复杂的期望动作（如特定手势或交互行为）。

这些局限为后续研究指明了方向：引入一致性模型等加速技术以降低延迟，融合环境感知数据以扩展适用场景，以及开发多模态控制接口以提升表达力。

## 方法谱系与知识库定位

### 问题瓶颈：确定性模型下的多模态运动生成困境

在 CAMDM 之前，实时角色控制的主流方法（如 LMP、MANN-DP、MM-DP）多为确定性运动生成模型。这类模型在自回归生成过程中，倾向于输出条件分布的平均值，导致三个核心问题：**均值姿态**——生成的运动缺乏多样性，难以体现同一控制信号下人类运动的自然多模态性；**脚滑动伪影**——自回归误差累积导致足部与地面接触不稳定；**风格过渡失败**——当用户切换风格标签时，模型无法生成平滑自然的过渡动作，因为训练集中往往缺乏对应的风格切换数据。MoGlow（Henter et al., TOG 2020）虽引入归一化流实现概率生成，但不支持朝向控制，且风格控制能力有限。上述瓶颈的本质在于：确定性模型无法捕捉运动数据中的多模态条件分布，而现有概率方法又未能有效解决条件歧义和轨迹一致性问题。

### 因果机制：无分类器引导作用于历史运动标记

CAMDM 的核心因果机制是 **无分类器引导作用于历史运动标记**（Classifier-Free Guidance on Past Motion, CFG-PM）。推理时，通过调节历史运动标记的引导尺度 $\gamma$，控制模型对历史运动的依赖程度：

$$\mathcal{G}_{\gamma}(\mathbf{x}_{t}, t; \mathbf{p}, \mathbf{c}) = \mathcal{G}(\mathbf{x}_{t}, t; \mathbf{p}=\emptyset, \mathbf{c}) + \gamma \big( \mathcal{G}(\mathbf{x}_{t}, t; \mathbf{p}, \mathbf{c}) - \mathcal{G}(\mathbf{x}_{t}, t; \mathbf{p}=\emptyset, \mathbf{c}) \big)$$

当 $\gamma=1$ 时，模型正常依赖历史运动；当用户切换风格时，将 $\gamma$ 设为 0.7，降低历史运动标记的影响，使生成更依赖风格标签，从而在无对应过渡数据的情况下实现平滑的风格切换。这一设计的有效性在消融实验中得到了决定性验证：若将 CFG 作用于风格标记（CFG-S）而非历史运动标记，多风格过渡成功率从 **94.2% 骤降至 8.9%**（Table 4），充分证明了 CFG-PM 是解决风格过渡问题的关键。

### 方法谱系定位

CAMDM 在方法谱系中处于**扩散概率模型 × 自回归运动生成 × 实时角色控制**的交汇点，其设计决策与现有工作的关系如下：

| 设计维度 | 传统做法 | CAMDM 创新 |
|----------|----------|------------|
| **条件表示** | 将所有条件拼接为单一特征向量（LMP、MANN-DP 等） | 独立条件标记化（Separate Condition Tokenization），通过 Transformer 注意力融合 |
| **无分类器引导** | 作用于风格标签或不用 CFG | 作用于历史运动标记（CFG-PM），风格切换时 $\gamma=0.7$ |
| **轨迹对齐** | 直接混合预测轨迹与用户合成轨迹 | 启发式未来轨迹扩展（HFTE），复用最后 K=4 个预测点 |
| **扩散步骤** | 标准 1000 步 | 训练与推理均仅用 8 步 |
| **去噪目标** | 预测噪声 $\epsilon$ | 直接预测干净信号 $\hat{x}_0$，便于施加几何损失 |

CAMDM 与后续工作的潜在连接点包括：一致性模型（Consistency Models）或潜在一致性模型（Latent Consistency Models）可进一步降低推理延迟；引入环境感知（如场景几何）可扩展至复杂地形导航；多模态控制接口（文本、音频等）可丰富控制表达能力。

### 适用边界与局限性

1. **计算负荷**：尽管 8 步扩散在 RTX 3060 上达到 13 ms/代，满足实时要求（Table 5），但相比轻量级确定性模型仍较高，难以直接部署到移动设备。
2. **环境交互受限**：仅在人类与平坦地面交互的运动数据上验证，未处理包含障碍物、楼梯、斜坡等复杂场景感知的控制任务。
3. **控制精度有限**：摇杆控制器表达能力有限，难以精确描述复杂的期望动作（如特定手部轨迹或全身舞蹈编排）。
4. **数据依赖**：模型的风格多样性和过渡能力受限于训练数据的风格覆盖范围。

### 开放问题

- 可否引入一致性模型或潜在一致性模型等先进加速技术，将推理延迟降低至移动端可接受的水平（<5 ms）？
- 模型能否有效理解来自环境的更复杂感知数据（如点云、深度图），并实时生成适应场景变化的自然运动？
- 如何开发融合文本、音频、脑电等多模态信号的新控制接口，从而生成更丰富的复杂动作？
- 当前 8 步扩散的设计是否在更高质量要求的应用（如影视级动画）中仍然足够？是否存在步数-质量-延迟的更优帕累托前沿？

## 原文 PDF

![[paperPDFs/SIGGRAPH_2024/CAMDM_Taming_Diffusion_Probabilistic_Models_for_Character_Control.pdf]]