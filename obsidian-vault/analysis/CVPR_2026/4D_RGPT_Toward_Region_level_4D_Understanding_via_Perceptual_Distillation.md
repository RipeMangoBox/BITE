---
title: "4D-RGPT: Toward Region-level 4D Understanding via Perceptual Distillation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/4D_RGPT_Toward_Region_level_4D_Understanding_via_Perceptual_Distillation.pdf
project_link: null
code_link: https://github.com/HumanSignal/label-studio
aliases:
- 4R
- 4RTRL4UPD
tags:
  - CVPR_2026
  - topic/vision_multimodal_applications
  - topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 通过从冻结的 4D 感知专家模型（L4P）中蒸馏潜在的 4D 表示和显式的 4D 信号，并注入时间戳位置编码（TPE），可显著增强 MLLM 对动态场景的 4D 感知和问答能力。
primary_logic: 在训练阶段引入仅训练时使用的 4D 感知模块，利用潜在蒸馏（对齐中间特征）和显式蒸馏（对齐预测的深度、光流等低层信号）将专家知识迁移至 MLLM，同时以正弦位置编码注入帧时间戳，使模型在无额外推理成本下获得时空感知能力。
claims:
- 4D-RGPT 在非区域级 3D/4D 基准上平均提升 +5.3%（6 个基准），在区域级 R4D-Bench 上提升 +4.3%。
- P4D 双分支蒸馏（潜在蒸馏 LD + 显式蒸馏 ED）在 R4D-Bench 上显著优于直接 SFT（4D-SFT）和简单拼接策略（4D-Concat, 4D-PE）。
- 潜在蒸馏（LD）单独使用已带来提升，组合 LD 和 ED 达到最佳平均性能。
- 时间戳位置编码（TPE）在 STI-Bench 和 R4D-Bench 上持续带来性能提升。
---

# 4D-RGPT: Toward Region-level 4D Understanding via Perceptual Distillation

> [!tip] 核心洞察
> 在训练阶段引入仅训练时使用的 4D 感知模块，利用潜在蒸馏（对齐中间特征）和显式蒸馏（对齐预测的深度、光流等低层信号）将专家知识迁移至 MLLM，同时以正弦位置编码注入帧时间戳，使模型在无额外推理成本下获得时空感知能力。

| 字段 | 内容 |
|------|------|
| 中文题名 | 4D-RGPT：通过感知蒸馏实现区域级4D理解 |
| 英文题名 | 4D-RGPT: Toward Region-level 4D Understanding via Perceptual Distillation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.17012) · [Code](https://github.com/HumanSignal/label-studio) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | 4D-RGPT |
| Dataset | STI-Bench, VLM4D-real, VSTI-Bench, R4D-Bench |

> [!tip] 效果简介
> - STI-Bench 上，Accuracy 37.6 vs 33.8 (NVILA-Lite-8B) (+3.8)。
> - VLM4D-real 上，Accuracy 52.7 vs 46.5 (NVILA-Lite-8B) (+6.2)。
> - VSTI-Bench 上，Accuracy 59.1 vs 45.2 (NVILA-Lite-8B) (+13.9)。

## 概要

当前多模态大语言模型（MLLMs）在理解动态视频时面临一个关键瓶颈：它们缺乏精细的 4D 感知能力——包括深度、光流等低层特征，以及显式的时间理解——因而难以在动态场景中追踪特定区域并进行精确的时空推理。现有 3D/4D VQA 基准要么缺少动态视频数据，要么不提供区域提示，无法系统评估这一能力缺口。

针对这一问题，本文提出 **4D-RGPT**，一种具备 4D 感知能力的专用 MLLM。其核心思路是通过**感知 4D 蒸馏（Perceptual 4D Distillation, P4D）**框架，从冻结的 4D 感知专家模型（L4P）中蒸馏知识，同时注入**时间戳位置编码（Timestamp Positional Encoding, TPE）**，使模型在无额外推理成本的前提下获得时空感知能力。训练时，4D-RGPT 通过潜在蒸馏（对齐中间特征）和显式蒸馏（对齐预测的深度、光流、运动、相机射线等低层信号）将专家知识迁移至自身；推理时，这些训练专用模块被移除，保持与基线 MLLM 相同的推理效率。

在实验验证上，4D-RGPT 在 **6 个非区域级 3D/4D 基准**上平均提升 **+5.3%**（相对于基线 NVILA-Lite-8B），在本文新构建的**区域级 4D 基准 R4D-Bench** 上提升 **+4.3%**。消融实验表明：P4D 双分支蒸馏显著优于直接 SFT 和简单拼接策略；潜在蒸馏单独使用已带来增益，组合显式蒸馏后达到最佳；TPE 在多个基准上持续贡献正向提升。方法局限在于精确数值估计任务（如速度、位移计算）上表现次优，且 4D 感知能力受限于冻结教师模型的上限。



### 从视频理解到 4D 时空推理

多模态大语言模型（MLLMs）在图像和视频理解任务上取得了显著进展，但当任务要求模型对动态场景中的**特定区域**进行精确的时空推理时，现有模型暴露出了根本性的能力缺口。以图1所示的区域级4D视觉问答（VQA）为例，模型需要同时完成三个层次的感知：**2D区域追踪**（定位并跟踪目标物体在视频帧中的位置）、**3D深度感知**（判断物体与相机之间的空间关系）、以及**4D时间进展**（理解物体随时间的运动变化）。当前的MLLMs——无论是专有模型如**GPT-4o**（OpenAI, arXiv 2024）、**Gemini-2.5-Pro**（Comanici et al., arXiv 2025），还是开源模型如**Qwen2.5-VL-7B**（Qwen Team, arXiv 2025）、**VideoLLaMA3-7B**（Zhang et al., arXiv 2025）——往往无法同时把握这三个维度中的某一个或多个方面，导致在需要精细时空推理的问题上回答错误。

### 现有方法的瓶颈

当前MLLMs在4D理解上的不足源于两个核心瓶颈：

**瓶颈一：缺乏精细的4D感知能力。** 通用MLLMs主要依赖视觉编码器提取高层语义特征，缺少对深度、光流、运动轨迹等低层4D信号的显式建模。这使得模型难以从视频中提取精确的时空几何信息，无法可靠地判断物体的空间位置、运动方向和速度。

**瓶颈二：缺少显式的时间理解机制。** 大多数MLLMs将视频帧作为无序的视觉标记序列输入，没有为模型提供帧之间的时间戳信息。即使模型能够感知单帧的空间结构，缺乏时间线索也使其难以建立帧间的因果关联，从而无法进行可靠的时间推理。

### 现有3D/4D VQA基准的局限

如表1所示，现有的3D/4D VQA基准在评估MLLMs的时空理解能力时存在明显不足。部分基准虽然提供了动态视频数据，但缺少对特定区域的精细提示（region prompts）；另一些基准虽然支持区域级问答，但仅局限于静态场景。**R4D-Bench**的出现填补了这一空白——它是首个同时提供**区域提示**和**大规模动态视频数据**的4D VQA基准，能够系统性地评估模型在静态和动态场景下的区域级时空推理能力。

### 本文动机与核心思路

针对上述瓶颈，本文提出**4D-RGPT**——一个具备4D感知能力的专用MLLM。其核心动机在于：如果能让MLLM在训练过程中“学会”感知深度、光流等低层4D信号，并在推理时显式地感知时间进展，模型就能在不增加推理成本的前提下获得更强的时空推理能力。

为实现这一目标，4D-RGPT引入了两大关键设计：

1. **感知4D蒸馏（Perceptual 4D Distillation, P4D）**：在训练阶段引入一个冻结的4D感知专家模型（L4P）作为教师，通过**潜在蒸馏**（对齐中间特征表示）和**显式蒸馏**（对齐预测的深度、光流等低层信号）将专家知识迁移至MLLM。这些4D感知模块仅在训练时使用，推理时被移除，因此不引入额外计算开销。

2. **时间戳位置编码（Timestamp Positional Encoding, TPE）**：将每帧的时间戳编码为正弦位置编码，直接注入视觉特征，为MLLM提供显式的时间线索，使其能够感知视频中的时间进展。

实验结果表明，4D-RGPT在非区域级3D/4D基准上平均提升**+5.3%**（覆盖6个基准），在区域级R4D-Bench上提升**+4.3%**，验证了通过感知蒸馏增强MLLM 4D理解能力的有效性。



## 核心方法与创新机理

4D-RGPT 的核心创新在于通过**仅训练时存在的 4D 感知蒸馏框架（P4D）** 和**时间戳位置编码（TPE）**，将冻结的 4D 感知专家模型的知识迁移至多模态大语言模型（MLLM），使 MLLM 在无额外推理成本的前提下获得精细的时空感知能力。以下从 **changed slots** 的角度剖析其相对于基线 MLLM 的关键设计变更。

### 训练目标：从纯 SFT 到多信号联合蒸馏

基线 MLLM（如 **NVILA-Lite-8B**，Liu et al., CVPR 2025）仅依赖标准的监督微调（SFT）损失进行训练。4D-RGPT 将训练目标扩展为三项损失的加权组合：

$$\mathcal{L} = \mathcal{L}_{\mathrm{SFT}} + \alpha \mathcal{L}_{\mathrm{LD}} + \beta \mathcal{L}_{\mathrm{ED}}$$

其中 $\alpha=0.5$，$\beta=0.1$（见附录 A1.3）。这一设计的关键在于：
- **潜在蒸馏损失 $\mathcal{L}_{\mathrm{LD}}$** 对齐 MLLM 内部隐藏状态与教师模型（L4P）的中间 4D 特征，使 MLLM 学会隐式编码时空结构；
- **显式蒸馏损失 $\mathcal{L}_{\mathrm{ED}}$** 对齐预测的低层 4D 信号（深度、光流、运动、camray）与教师输出，强制 MLLM 掌握可解释的物理量。

消融实验（Table 5）表明，单独使用潜在蒸馏（LD）即可带来性能提升，而 LD 与 ED 的组合达到最佳平均性能，证实了两类信号在知识迁移中的互补性。

### 时间信息注入：从无语义时间线索到正弦时间戳编码

基线 MLLM 通常将视频帧作为无序序列输入，缺乏显式的时间感知机制。4D-RGPT 引入了**时间戳位置编码（TPE）**，将每帧的时间戳 $t^{(n)}$ 编码为 $D$ 维正弦向量：

$$p^{(n)}[2i] = \sin\left(\frac{t^{(n)}}{T^{\frac{2i}{D}}}\right), \quad p^{(n)}[2i+1] = \cos\left(\frac{t^{(n)}}{T^{\frac{2i}{D}}}\right)$$

该编码直接加至视觉编码器（SigLIP）的输出特征上，在进入投影层之前注入时间信息。消融实验（Table 6）显示，TPE 在 STI-Bench 和 R4D-Bench 上均持续带来性能提升，验证了显式时间线索对动态场景理解的必要性。

### 4D 感知模块：从无专用模块到训练时 4D 解码器

基线 MLLM 不具备任何专用的 4D 感知组件。4D-RGPT 在训练阶段引入了两个仅训练时使用的模块：
- **4D 感知解码器 $\mathrm{D}_{\mathrm{4DP}}$**：一个 MLP，从 LLM 的隐藏状态中解码潜在 4D 表示 $\hat{\pmb{F}}_{\mathrm{4D}}$；
- **预测头 $\mathrm{D}_m$**：复用冻结的 L4P 模型的预测头，从 $\hat{\pmb{F}}_{\mathrm{4D}}$ 预测显式低层信号 $\hat{P}_m$。

这些模块在推理时被完全移除，因此不引入额外计算开销。Table 4 的消融显示，P4D 蒸馏策略显著优于直接 4D SFT（4D-SFT）以及简单的特征拼接（4D-Concat）或位置编码替代（4D-PE）策略，表明“训练时蒸馏、推理时丢弃”的设计在效率与效果之间取得了关键平衡。

### 创新总结

上述三个 changed slots 共同构成了 4D-RGPT 的因果调节旋钮：TPE 提供显式时间定位，P4D 的双分支蒸馏将冻结教师模型的潜在时空表示和显式物理信号迁移至学生 MLLM，而训练时专用模块的引入与推理时移除策略保证了零额外推理成本。这一组合使 4D-RGPT 在非区域级 3D/4D 基准上平均提升 +5.3%（6 个基准），在区域级 R4D-Bench 上提升 +4.3%。



4D-RGPT 的整体框架围绕一个核心设计展开：**在训练阶段引入仅训练时使用的 4D 感知模块，通过感知蒸馏将冻结专家模型的知识迁移至 MLLM，推理时完全移除这些模块，不增加任何额外计算开销**。

### 输入流水线

给定一段包含 $N$ 帧的视频 $\pmb{V} = \{I^{(1)}, I^{(2)}, \dots, I^{(N)}\}$，每一帧 $I^{(n)}$ 首先通过冻结的视觉编码器 $\pmb{\mathsf{E}}_{\mathtt{V}}$（SigLIP）提取视觉特征。随后，系统为每一帧生成一个**时间戳正弦位置编码（Timestamp Positional Encoding, TPE）** $\pmb{p}^{(n)}$，直接加至视觉特征上，为 MLLM 提供显式的时间线索。TPE 的生成公式为：

$$p^{(n)}[2i] = \sin\left(\frac{t^{(n)}}{T^{\frac{2i}{D}}}\right) \quad \text{and} \quad p^{(n)}[2i+1] = \cos\left(\frac{t^{(n)}}{T^{\frac{2i}{D}}}\right)$$

其中 $t^{(n)}$ 为帧的时间戳，$T$ 为最大时间尺度，$D$ 为编码维度。注入 TPE 后的视觉特征经多模态投影器 $\pmb{\mathsf{E}}_{\mathtt{P}}$ 对齐到文本特征空间，与文本指令一同送入 LLM（Qwen2）进行自回归生成。

### 训练时 4D 感知模块

在训练阶段，框架额外引入两个仅训练时使用的模块，构成感知蒸馏的知识迁移通道：

1. **4D 感知解码器 $\pmb{\mathsf{D}}_{\mathtt{4DP}}$**：一个 MLP，从 LLM 某一层的隐藏状态 $\pmb{F}_{\mathrm{hidden}}^{(n)}$ 中解码出潜在的 4D 表示 $\hat{\pmb{F}}_{\mathrm{4D}}^{(n')}$：
   $$\hat{\pmb{F}}_{\mathrm{4D}}^{(n')} = \pmb{\mathsf{D}}_{\mathrm{4DP}} \left( \mathrm{Rearrange}(\pmb{F}_{\mathrm{hidden}}^{(n)}) \right)$$

2. **预测头 $\pmb{\mathsf{D}}_m$**：继承自冻结的 4D 感知专家模型 L4P，从潜在 4D 特征 $\hat{\pmb{F}}_{\mathrm{4D}}$ 中预测显式的低层 4D 信号（深度、光流、运动掩码、相机射线）：
   $$\hat{P}_m = \pmb{\mathsf{D}}_m ( \hat{F}_{\mathrm{4D}} )$$

这两个模块在推理时被完全移除，模型仅保留标准的 MLLM 推理路径。

### 感知 4D 蒸馏（P4D）训练框架

P4D 框架以冻结的 L4P 模型作为教师，通过双分支蒸馏将 4D 感知知识迁移至 4D-RGPT 学生模型。教师模型从输入视频 $\pmb{V}$ 中提取真实的 4D 潜在特征 $\pmb{F}_{\mathtt{4D}}$ 和显式信号 $\pmb{P}_m$，与学生端的对应预测进行对齐。训练总损失为三项的加权组合：

$$\mathcal{L} = \mathcal{L}_{\mathtt{SFT}} + \alpha \mathcal{L}_{\mathtt{LD}} + \beta \mathcal{L}_{\mathtt{ED}}$$

其中：
- $\mathcal{L}_{\mathtt{SFT}}$ 为标准交叉熵监督微调损失；
- $\mathcal{L}_{\mathtt{LD}}$ 为**潜在蒸馏损失**，对齐师生双方的潜在 4D 特征：$\mathcal{L}_{\mathrm{LD}} = \sum_{n'=1}^{N'} \Delta_{\mathrm{LD}}(F_{\mathrm{4D}}^{(n')}, \hat{F}_{\mathrm{4D}}^{(n')})$；
- $\mathcal{L}_{\mathtt{ED}}$ 为**显式蒸馏损失**，加权对齐深度、光流等多模态低层信号：$\mathcal{L}_{\mathrm{ED}} = \sum_{n=1}^{N} \sum_{m \in \mathcal{M}} \lambda_m \Delta_m(\pmb{P}_m^{(n)}, \hat{\pmb{P}}_m^{(n)})$。

权重设置为 $\alpha=0.5$，$\beta=0.1$。

### 整体数据流

Figure 2 展示了完整的 P4D 框架架构。视频帧经视觉编码器和 TPE 注入后进入 MLLM 主干，训练时从 LLM 隐藏状态分叉出 4D 感知解码器和预测头，与冻结的 L4P 教师模型进行潜在蒸馏和显式蒸馏。推理时，分叉路径被切除，模型以标准 MLLM 方式运行，在无额外推理成本的前提下获得了时空感知能力。

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2512_17012/figures/003_Figure_2.jpg]]
*Figure 2: | Perceptual 4D Distillation (P4D) framework for 4D-RGPT. For each frame*

### 补充图表

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2512_17012/figures/001_Figure_1.jpg]]
*Figure 1: | Overview of Region-level 4D Understanding. 4D region-level VQA, e.g., our R4D-Bench, requires MLLMs to be able to track regions (2D), perceive depth (3D), and temporal progression (4D). Baseline MLLMs cannot recognize one or more of these aspects and thus fail to answer questions correctly. With our distillation framework, our 4D-RGPT better perceives these aspects and answers accurately. We note that the regions labeled with (*) are not provided in R4D-Bench; they are visualized for readability*



### 4D-RGPT 整体架构

4D-RGPT 在标准 MLLM 骨干（NVILA-Lite-8B，视觉编码器 SigLIP + 大语言模型 Qwen2）上引入三个关键组件，均在训练时使用、推理时移除，不增加额外推理成本：

- **视觉编码器 (E_V)**：从输入视频 $V = \{I^{(n)}\}_{n=1}^{N}$ 的每一帧提取视觉特征。
- **多模态投影器 (E_P)**：将视觉特征映射到与 LLM 文本特征对齐的空间。
- **4D 感知解码器 (D_4DP)**：一个仅训练时使用的 MLP，从 LLM 隐藏状态中解码潜在 4D 表示。
- **预测头 (D_m)**：从冻结的 4D 感知专家模型 L4P 继承的预测头，用于从潜在 4D 特征预测显式低层信号（深度、光流、运动、camray）。
- **时间戳位置编码 (TPE)**：以正弦位置编码形式将帧时间戳直接注入视觉特征，提供显式的时间感知线索。

### 关键公式与变量含义

**4D 潜在特征提取（教师模型）**

$$
\pmb{F}_{\mathtt{4D}} = \pmb{\mathsf{E}}_{\mathtt{4D}}(\pmb{V}) \in \mathbb{R}^{N' \times h' \times w' \times c'}
$$

其中 $\pmb{\mathsf{E}}_{\mathtt{4D}}$ 为冻结的 4D 感知编码器（L4P），$\pmb{V}$ 为输入视频，输出 $N'$ 个空间分辨率为 $h' \times w'$、通道数为 $c'$ 的 4D 潜在特征。

**学生模型潜在 4D 表示解码**

$$
\hat{\pmb{F}}_{\mathrm{4D}}^{(n')} = \pmb{\mathrm{D}}_{\mathrm{4DP}} \left( \mathrm{Rearrange}(\pmb{F}_{\mathrm{hidden}}^{(n)}) \right)
$$

其中 $\pmb{F}_{\mathrm{hidden}}^{(n)}$ 为 LLM 第 $n$ 层的隐藏状态，经重排后通过 4D 感知解码器 $\pmb{\mathrm{D}}_{\mathrm{4DP}}$ 映射为学生端的潜在 4D 特征 $\hat{\pmb{F}}_{\mathrm{4D}}^{(n')}$。

**显式 4D 信号预测**

$$
\hat{P}_m = \pmb{\mathrm{D}}_m ( \hat{F}_{4\mathrm{D}} )
$$

其中 $\pmb{\mathrm{D}}_m$ 为模态 $m \in \mathcal{M} = \{\text{depth, flow, motion, camray}\}$ 对应的预测头，从学生潜在 4D 特征 $\hat{F}_{4\mathrm{D}}$ 解码出显式低层信号 $\hat{P}_m$。

**时间戳正弦位置编码**

$$
p^{(n)}[2i] = \sin\left(\frac{t^{(n)}}{T^{\frac{2i}{D}}}\right) \quad \text{and} \quad p^{(n)}[2i+1] = \cos\left(\frac{t^{(n)}}{T^{\frac{2i}{D}}}\right)
$$

其中 $t^{(n)}$ 为第 $n$ 帧的时间戳，$D$ 为编码维度，$T$ 为最大时间尺度。该编码直接加至视觉编码器输出 $E_V(I^{(n)})$ 上，再送入投影器 $E_P$。

**潜在蒸馏损失**

$$
\mathcal{L}_{\mathrm{LD}} = \sum_{n'=1}^{N'} \Delta_{\mathrm{LD}}(F_{4\mathrm{D}}^{(n')}, \hat{F}_{4\mathrm{D}}^{(n')})
$$

其中 $\Delta_{\mathrm{LD}}$ 为教师与学生潜在 4D 特征之间的差异度量（文中采用 smooth L1 损失），$N'$ 为特征样本数。

**显式蒸馏损失**

$$
\mathcal{L}_{\mathrm{ED}} = \sum_{n=1}^{N} \sum_{m \in \mathcal{M}} \lambda_m \Delta_m(\pmb{P}_m^{(n)}, \hat{\pmb{P}}_m^{(n)})
$$

其中 $\pmb{P}_m^{(n)}$ 为教师模型预测的模态 $m$ 真值信号，$\hat{\pmb{P}}_m^{(n)}$ 为学生预测，$\lambda_m$ 为各模态的损失权重，$\Delta_m$ 为对应模态的距离函数。

**总训练损失**

$$
\mathcal{L} = \mathcal{L}_{\mathtt{SFT}} + \alpha \mathcal{L}_{\mathtt{LD}} + \beta \mathcal{L}_{\mathtt{ED}}
$$

其中 $\mathcal{L}_{\mathtt{SFT}}$ 为标准交叉熵监督微调损失，$\alpha=0.5$、$\beta=0.1$ 为蒸馏损失的平衡系数（详见附录 A1.3）。

### 核心机制总结

P4D 框架的核心在于**双分支蒸馏**：潜在蒸馏（LD）对齐师生模型在中间特征空间的 4D 表示，使 LLM 内部隐式习得时空结构；显式蒸馏（ED）则强制学生模型从潜在特征中准确恢复深度、光流等低层感知信号，从而将冻结专家 L4P 的感知能力迁移至 MLLM。TPE 以极低成本为视觉特征注入帧级时间戳，弥补了标准 MLLM 缺乏显式时间线索的短板。三者协同，使 4D-RGPT 在无额外推理开销的前提下获得显著增强的时空感知与推理能力。



## 实验与关键发现

### 实验设置

4D-RGPT 采用 **NVILA-Lite-8B**（Liu et al., CVPR 2025）作为 MLLM 骨干网络，其中视觉编码器 E_V 为 SigLIP，大语言模型为 Qwen2。4D 感知专家模型 E_4D 和预测头 D_m 直接沿用冻结的 **L4P** 架构与权重。训练时，总损失函数为 SFT 交叉熵损失与蒸馏损失的加权组合：

$$\mathcal{L} = \mathcal{L}_{\mathtt{SFT}} + \alpha \mathcal{L}_{\mathtt{LD}} + \beta \mathcal{L}_{\mathtt{ED}}$$

其中 α=0.5, β=0.1（见附录 A1.3）。推理时，4D 感知解码器 D_4DP 和预测头 D_m 被完全移除，不引入额外推理成本。

### 非区域级 3D/4D 基准主结果

Table 2 汇总了 6 个非区域级 3D/4D VQA 基准上的多选准确率。4D-RGPT-8B 在所有基准上均优于其骨干模型 NVILA-Lite-8B，平均提升 **+5.3%**。其中：

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2512_17012/figures/006_Table_2.jpg]]
*Table 2: | Evaluation on non-region-level 3D / 4D benchmarks. We report the average multiple-choice accuracy (↑) on each benchmark. For simplicity, we use the following abbreviations: STI (STI-Bench [22]), V4D (VLM4D-real [23]), MMSI (MMSI-Bench [26]), OS (OmniSpatial [25]), and VSTI (VSTI-Bench [18])*

- **STI-Bench**：37.6 vs. 33.8（+3.8）
- **VLM4D-real**：52.7 vs. 46.5（+6.2）
- **VSTI-Bench**：59.1 vs. 45.2（+13.9）

值得注意的是，VSTI-Bench 上的 +13.9 提升幅度最大，表明 P4D 蒸馏对时空推理密集型任务尤为有效。4D-RGPT 同样显著超越 GPT-4o、Gemini-2.5-Pro 等专有模型，以及 VideoLLaMA3-7B、LLaVA-Video-7B 等开源通用 MLLM。

### 区域级 R4D-Bench 主结果

Table 3 展示了 R4D-Bench 上静态与动态划分以及 9 个子任务的分类精度。4D-RGPT 在平均准确率上达到 **42.2**，较 NVILA-Lite-8B 的 37.9 提升 **+4.3**；在动态划分上从 41.3 提升至 45.7（+4.4）。

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2512_17012/figures/007_Table_3.jpg]]
*Table 3: | Evaluation on R4D-Bench. We report performance on the static split ( Sta ), the dynamic split ( Dyn ), and all 9 tasks of R4D-Bench. For simplicity, we abbreviate them as follows: 3D Video Grounding ( VG); Dimension Measurement ( DM); Spatial Relationship ( SR); Rotational ( R); Counting ( C ); Translational ( T ); False Positive ( FP ); Speed & Acceleration (SA); and Displacement & Path Length ( DP)*

与 3D/4D 专用 MLLM 相比，4D-RGPT 同样表现突出：VLM-3R-7B（Fan et al., arXiv 2025）在 R4D-Bench 上仅取得 35.5，ViLaSR-7B（Wu et al., NeurIPS 2025）为 36.8，SpatialReasoner-7B（Ma et al., NeurIPS 2025）为 37.2——4D-RGPT 分别领先 +6.7、+5.4、+5.0 个百分点。这验证了 P4D 蒸馏框架在区域级 4D 理解任务上的有效性。

### P4D 蒸馏策略消融

**替代策略对比（Table 4）**。将 P4D 与三种替代方案比较：
- **4D-SFT**：直接在 4D VQA 数据上监督微调，不引入蒸馏
- **4D-Concat**：将 4D 专家特征直接拼接到视觉特征后输入 MLLM
- **4D-PE**：将 4D 特征作为额外的位置编码注入

P4D 在所有基准上均显著优于这些策略。4D-SFT 的提升有限，说明仅靠 SFT 难以有效注入 4D 感知能力；4D-Concat 和 4D-PE 的简单拼接/注入策略效果不佳，表明需要更精细的知识迁移机制。

**蒸馏模态组合消融（Table 5）**。潜在蒸馏（LD）单独使用已带来性能提升，验证了中间特征对齐对 4D 感知迁移的关键作用。组合 LD 和显式蒸馏（ED）达到最佳平均性能，说明两种蒸馏信号互补：LD 对齐高层语义表示，ED 对齐深度、光流、运动、camray 等低层物理信号。

**训练过程可视化（Figure 5）**。训练过程中预测深度图的可视化显示，随着训练步数增加，4D-RGPT 预测的深度图逐渐逼近教师模型 L4P 的输出，直观验证了蒸馏的有效性。

### 时间戳位置编码消融

Table 6 对比了三种显式时间线索注入方式：
- **无时间线索**（baseline）
- **文本提示**：在问题中附加时间戳文本
- **视觉标记**：将时间戳作为额外视觉 token
- **TPE**：正弦时间戳位置编码直接加至视觉特征

TPE 在 STI-Bench 和 R4D-Bench 上均带来持续提升，且优于文本提示和视觉标记方案。这表明将时间信息编码为连续的正弦位置信号，比离散的文本或 token 表示更利于 MLLM 捕获帧间时序关系。

### 训练设计消融

Table 7 探索了不同训练配置：
- **仅微调投影器** vs. **微调投影器 + LLM**：后者性能更优
- **冻结视觉编码器 E_V**：保持冻结获得最佳性能，全量微调 E_V 反而导致性能下降，可能是因为破坏了预训练的视觉表示
- **LoRA 微调 LLM** vs. **全量微调 LLM**：全量微调效果更好，表明 4D 感知知识的迁移需要充分更新语言模型的参数

### 失败模式与局限性

尽管 4D-RGPT 在多项基准上取得显著提升，仍存在以下不足：

1. **数值推理精度不足**：在需要精确数值估计的任务（如计算速度、位移、时间间隔）上表现次优。这可能源于训练数据中缺乏逐步推理（Chain-of-Thought）过程，模型倾向于给出近似判断而非精确计算。

2. **教师模型上限约束**：4D 感知能力的理论上限受限于冻结的 L4P 教师模型。当教师模型在特定场景（如极端光照、快速运动）下预测不准时，蒸馏信号本身存在偏差，学生模型无法超越教师。

3. **跨骨干泛化性未验证**：当前实验仅基于 NVILA-Lite-8B 骨干，P4D + TPE 框架对其他 MLLM 架构（如 LLaVA 系列、Qwen2.5-VL 等）的泛化效果尚待验证。

### 开放问题

- 引入 Chain-of-Thought 训练数据是否能改善数值推理精度？
- 不同视频帧率和采样策略对 TPE 效果的影响如何？
- P4D 框架与强化学习（RL）结合能否进一步提升 4D 问答能力？

### 补充图表

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2512_17012/figures/008_Table_4.jpg]]
*Table 4: | Alternative strategies for 4D VQA. We compare P4D with direct SFT (4D-SFT) and straightforward designs of incorporating*

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2512_17012/figures/009_Table_5.jpg]]
*Table 5: | Analysis of 4D modalities in P4D. We ablate the effectiveness of different combinations of distillation in latent distillation (LD) on*

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2512_17012/figures/012_Table.jpg]]
*Table: DemoTable 6 | Ablation studies on explicit temporal cues. We experiment without and with different Demo Demochoices of explicit time cues. For simplicity, we use the same abbreviations as Tab. 4*

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2512_17012/figures/010_Figure_5.jpg]]
*Figure 5: | Predicted depth maps at different training steps. We visualize the progress of*

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2512_17012/figures/005_Figure_4.jpg]]
*Figure 4: | VQA comparison among baseline ⟨R1⟩MLLMs and 4D-RGPT on R4D-Bench. For the (*) (*)baseline MLLMs, we use GPT-4o-20241120 [5], Qwen-2.5VL-7B-Instruct [35], and NVILA-Lite-8B [36]. We note that the regions labeled with (*) or (*) are not Q: What direction is ⟨R1⟩ moving forward ?provided in R4D-Bench; they are visualized for readability*

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2512_17012/figures/002_Table_1.jpg]]
*Table 1: | Comparison among 3D / 4D VQA Benchmarks. Existing benchmarks either lack dynamic video data or region prompts, while our R4D-Bench is the first to provide both at scale. All benchmarks are downloaded from official sources as of August 2025, and the numbers of VQA might differ from the original papers. Static videos contain only camera movement, while dynamic videos contain both camera and object movement. †We only adopt real-world videos from the VLM4D benchmark*

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2512_17012/figures/004_Figure_3.jpg]]
*Figure 3: | Curation pipeline of our R4D-Bench. Given existing non-region 4D VQA benchmarks, we (a) first extract the noun keywords from the question as candidates for objects of interest. (b) Next, if ground truth segmentation masks are provided, we use them for step (d). Otherwise, we use off-the-shelf GroundingDINO [70] and SAM2 [71] to extract segmentation masks for each object of interest. (c) We generate a SoM [59] image for the first frame. (d) We prompt Qwen-2.5VL [35] with the SoM image and the referee, fighter MLLMprocessed question to match the objects referred to in the question with the regions. (e) Finally, the generated identify key objsmatching results are verified by human experts*

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2512_17012/figures/032_Figure_5.jpg]]
*Figure 5: Similar to the format of Fig. 5, we visualize the training progress of*



## 定位与知识库关联

### 1. 在 3D/4D 多模态大模型谱系中的位置

4D-RGPT 处于**通用多模态大模型（MLLM）向时空专用模型演进**的关键节点。现有 3D/4D 专用 MLLM 可大致分为两类：

**（a）通用 MLLM 的零样本/微调基线。** 包括专有模型 **GPT-4o**（OpenAI, arXiv 2024）、**Gemini-2.5-Pro**（Comanici et al., arXiv 2025），以及开源模型 **Qwen2.5-VL-7B**（Qwen Team, arXiv 2025）、**VideoLLaMA3-7B**（Zhang et al., arXiv 2025）、**LLaVA-Video-7B**（Zhang et al., arXiv 2024）、**LLaVA-OneVision-7B**（Li et al., TMLR 2025）、**LLaVA-NeXT-Video-7B**（Liu et al., 2024）和 **NVILA-Lite-8B**（Liu et al., CVPR 2025）。这些模型在标准视频理解任务上表现强劲，但缺乏精细的 4D 感知能力（深度、光流等低层特征）和显式的时间理解，难以在动态视频中追踪区域并进行精确时空推理。4D-RGPT 直接以 NVILA-Lite-8B 为骨干进行增强，在非区域级基准上平均提升 +5.3%，在区域级 R4D-Bench 上提升 +4.3%，验证了通用 MLLM 的 4D 感知短板。

**（b）3D/4D 专用 MLLM。** 包括 **VLM-3R-7B**（Fan et al., arXiv 2025）、**ViLaSR-7B**（Wu et al., NeurIPS 2025）、**SpatialReasoner-7B**（Ma et al., NeurIPS 2025），以及 LLaVA-Video-7B + SAT 和 SpaceR-7B。这些工作通过空间推理模块或 3D 感知增强来提升空间理解，但多数聚焦于静态 3D 场景或缺乏对动态时间维度的系统建模。4D-RGPT 的独特贡献在于通过**感知蒸馏**同时引入潜在 4D 表示和显式 4D 信号（深度、光流、运动、camray），并以**时间戳位置编码（TPE）**注入帧级时间信息，首次在 MLLM 中实现了训练时 4D 感知与推理时零额外开销的统一。

### 2. 核心设计决策与因果机制

4D-RGPT 的核心洞察是：**在训练阶段引入仅训练时使用的 4D 感知模块，利用潜在蒸馏（对齐中间特征）和显式蒸馏（对齐预测的深度、光流等低层信号）将专家知识迁移至 MLLM，同时以正弦位置编码注入帧时间戳，使模型在无额外推理成本下获得时空感知能力。** 具体而言：

- **因果旋钮（causal knob）：** 从冻结的 4D 感知专家模型 **L4P** 中蒸馏潜在的 4D 表示和显式的 4D 信号，并注入 TPE，可显著增强 MLLM 对动态场景的 4D 感知和问答能力。
- **真实瓶颈（real bottleneck）：** 当前 MLLMs 缺乏精细的 4D 感知能力（如深度、光流等低层特征）和显式的时间理解，难以在动态视频中追踪区域并进行精确的时空推理。

消融实验（Table 4-7）提供了因果证据链：
1. **P4D 蒸馏 vs. 替代策略（Table 4）：** P4D 双分支蒸馏（潜在蒸馏 LD + 显式蒸馏 ED）在 R4D-Bench 上显著优于直接 SFT（4D-SFT）和简单拼接策略（4D-Concat, 4D-PE），表明感知知识的迁移比简单特征拼接或微调更有效。
2. **蒸馏模态组合（Table 5）：** 潜在蒸馏（LD）单独使用已带来提升，组合 LD 和 ED 达到最佳平均性能，验证了潜在特征对齐与显式信号预测的互补性。
3. **时间戳位置编码（Table 6）：** TPE 在 STI-Bench 和 R4D-Bench 上持续带来性能提升，证明显式时间线索注入对动态场景理解的必要性。
4. **训练设计（Table 7）：** 同时微调投影器（E_P）和 LLM 并冻结视觉编码器（E_V）获得最佳性能，为类似框架的微调策略提供了参考。

### 3. 适用边界与局限

4D-RGPT 的适用边界由以下因素界定：

- **输入模态：** 需要视频帧序列及对应的时间戳信息，适用于动态场景的 4D 区域级问答，但不适用于纯静态图像或单帧 3D 推理任务。
- **4D 感知能力上限：** 受限于冻结的教师模型 L4P 的性能。若教师模型在特定场景（如极端遮挡、无纹理区域）的深度或光流预测失败，蒸馏信号将带有噪声，可能影响学生模型的感知质量。
- **数值推理精度：** 在需要精确数值估计的任务（如计算速度、位移）上表现次优，可能因为训练中缺乏逐步推理过程（chain-of-thought）。这是一个已知的局限，需在后续工作中通过 CoT 训练或强化学习来改善。
- **骨干网络依赖：** 当前实现基于 NVILA-Lite-8B，P4D + TPE 框架对其他 MLLM 骨干（如 LLaVA 系列）的泛化性尚未验证，属于开放问题。

### 4. 开放问题与未来方向

1. **跨骨干泛化：** P4D + TPE 框架能否泛化到其他 MLLM 骨干网络（除 NVILA 外），例如 Qwen2.5-VL 或 VideoLLaMA3？
2. **帧率与采样策略：** 不同的帧率或视频采样策略对 TPE 效果有何影响？当前 TPE 设计假设均匀采样，非均匀时间间隔下的编码策略值得探索。
3. **时间线索的替代注入方式：** 是否可以在不修改输入数据的前提下提供时间线索（类似 TPE），例如通过可学习的时间嵌入或交叉注意力机制？
4. **推理能力增强：** 加入链式思维（CoT）训练是否能改善数值推理精度？将 P4D 与强化学习（RL）结合能否进一步提升 4D 问答能力？
5. **教师模型升级：** 随着更强大的 4D 感知模型出现，替换 L4P 教师是否能直接提升 4D-RGPT 的性能上限？蒸馏框架的即插即用特性为此提供了便利。

### 5. 知识库定位

4D-RGPT 在知识库中应定位为**首个通过感知蒸馏实现训练时 4D 增强、推理时零额外开销的区域级 4D 理解 MLLM**。其方法论贡献——P4D 蒸馏框架与 TPE 时间编码——为后续 4D MLLM 研究提供了可复用的训练范式。配套的 **R4D-Bench** 是首个同时提供区域提示和动态视频数据的大规模 4D VQA 基准（Table 1），填补了现有基准在区域级动态评估上的空白。代码已开源（https://github.com/HumanSignal/label-studio），便于社区复现和扩展。



## 原文 PDF

![[paperPDFs/CVPR_2026/4D_RGPT_Toward_Region_level_4D_Understanding_via_Perceptual_Distillation.pdf]]
