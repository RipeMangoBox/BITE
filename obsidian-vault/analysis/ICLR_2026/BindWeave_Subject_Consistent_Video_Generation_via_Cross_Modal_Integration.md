---
title: "BindWeave: Subject-Consistent Video Generation via Cross-Modal Integration"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/BindWeave_Subject_Consistent_Video_Generation_via_Cross_Modal_Integration.pdf
aliases:
- BindWeave
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: "用MLLM跨模态推理隐藏状态联合条件化主体一致视频扩散生成。"
primary_logic: "BindWeave先用MLLM绑定文本指令和参考主体，再联合T5、CLIP与VAE条件信号驱动DiT生成视频。"
claims:
- "MLLM隐藏状态提供主体身份、关系和动作绑定的高层推理信号，弥补浅层后融合不足。"
- "T5文本嵌入对训练稳定性必要，仅依赖MLLM条件化无法稳定收敛。"
- "自适应多参考条件化支持把多个参考图像作为时间槽位注入视频潜变量。"
- "OpenS2V-Eval和用户研究显示BindWeave在主体一致性与总分上优于对比方法。"
---

# BindWeave: Subject-Consistent Video Generation via Cross-Modal Integration

> [!tip] 核心洞察
> 在生成过程开始之前，利用MLLM对多模态输入进行深层的、有推理的理解，取代浅层的后融合。MLLM生成的隐藏状态提供了高层推理信号，与T5提供的精确语言锚点、CLIP提供的语义身份信号以及VAE提供的低层外观细节信号协同作用，共同引导扩散过程，生成在视觉上忠实于主体、在逻辑和语义上与复杂用户指令对齐的视频。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | BindWeave：基于跨模态整合的主体一致性视频生成 |
| 英文题名 | BindWeave: Subject-Consistent Video Generation via Cross-Modal Integration |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=FP2XNyV9WL); [Project](https://lzy-dot.github.io/BindWeave/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | BindWeave |
| Dataset | OpenS2V-Eval |

> [!tip] 效果简介
> - OpenS2V-Eval 上，Total Score 为 57.61%，对比 55.16% (T5-only)，变化 +2.45%。
> - OpenS2V-Eval 上，NexusScore 为 46.84%，对比 45.79% (T5-only)，变化 +1.05%。
> - OpenS2V-Eval 上，Aesthetics 为 45.55%，对比 42.80% (T5-only)，变化 +2.75%。

## 概述

BindWeave 是一个面向主体到视频（subject-to-video）生成任务的统一框架，旨在解决现有方法在处理多主体、复杂交互和时序逻辑时出现的主体身份混淆、动作错位和属性混合问题。其核心创新在于利用多模态大语言模型（MLLM）替代传统的浅层跨模态融合机制，对参考图像和文本提示进行深层推理，从而生成编码了主体身份和交互关系的高层隐藏状态，并以此条件化扩散 Transformer（DiT）进行视频生成。在 OpenS2V-Eval 基准上，BindWeave 取得了最高的总分（57.61%）和 NexusScore（46.84%），优于所有对比的开源和商业方法。

## 背景与动机

现有主体一致性视频生成方法普遍采用“分离-融合”的浅层信息处理范式：分别用独立编码器提取图像和文本特征，再通过简单拼接或交叉注意力进行后融合。这种范式缺乏跨模态输入的深层语义关联，导致模型在解析涉及多主体间复杂交互、空间关系和时序逻辑的文本指令时能力不足，常出现身份混淆、动作错位或属性混合等问题。具体而言，当提示词要求“一只猫坐在一只狗旁边”时，模型可能无法正确区分哪个主体执行哪个动作，或者将两个主体的外观特征混合。

## 核心创新

BindWeave 的核心洞察是：在生成过程开始之前，利用 MLLM 对多模态输入进行深层的、有推理的理解，取代浅层的后融合。具体创新包括：

1. **MLLM 作为智能指令解析器**：使用预训练的 MLLM（Qwen2.5-VL-7B）对参考图像和文本提示构建的统一交错序列进行深度跨模态推理，将文本命令绑定到对应的视觉实体上，生成编码了主体身份和交互关系的高层隐藏状态。

2. **联合条件化信号**：将 MLLM 隐藏状态（经轻量级连接器投影）与 T5 文本嵌入拼接，形成联合关系条件信号 `c_joint = Concat(c_mllm, c_text)`，同时使用 CLIP 图像特征提供语义身份信号，VAE 低层特征提供外观细节信号。

3. **自适应多参考条件化**：在噪声视频潜变量的时间轴上填充 K 个零槽位，将参考图像的 VAE 特征和对应二值掩码放入这些槽位，再沿通道拼接，实现灵活的多参考图像注入。

## 整体框架

![[assets/figures/papers/iclr26_vision_multimodal_applications__image_and_video_generation__b001_FP2XNyV9WL_BindWeave_Sub/figures/001_Figure_1.jpg]]
*Figure 1: Examples of subject-to-video generation results of our proposed BindWeave, demonstrating its ability to produce high-fidelity, subject-consistent videos across a broad spectrum of scenarios from single-subject inputs to complex multi-subject compositions.*

BindWeave 的整体框架如 Figure 2 所示。其工作流程如下：

1. **多模态序列构建**：将文本提示和 K 个图像占位符构建成交错序列 `X = [T, <img>_1, <img>_2, ..., <img>_K]`。

2. **MLLM 推理**：MLLM 处理该序列及对应的参考图像列表 I，生成隐藏状态 `H_mllm = MLLM(X, I)`。

3. **条件信号生成**：通过轻量级连接器 `C_proj` 将 MLLM 隐藏状态投影到对齐的条件空间 `c_mllm = C_proj(H_mllm)`；同时 T5 编码器独立编码文本提示 `c_text = E_T5(T)`；两者拼接形成联合条件 `c_joint = Concat(c_mllm, c_text)`。

4. **扩散生成**：DiT 骨干网络接收联合条件信号（通过交叉注意力）、CLIP 图像特征（通过交叉注意力）和 VAE 低层特征（通过通道拼接），进行条件化视频生成。

## 核心模块与公式推导

### 5.1 扩散基础

BindWeave 基于 Transformer 潜扩散架构，使用 Rectified Flow 定义扩散动力学。训练目标为 Flow Matching 损失：

$$\mathcal{L} = \mathbb{E}_{t,z_0,\epsilon,c_{\mathrm{text}}} \left\| u_\Theta(z_t, t, c_{\mathrm{text}}) - v_t \right\|_2^2$$

其中 $v_t = dz_t/dt = \epsilon - z_0$ 为真实速度场。

### 5.2 自适应多参考条件化

如 Figure 3 所示，在噪声视频潜变量的时间轴上填充 K 个零槽位，将参考图像的 VAE 特征和对应二值掩码放入这些槽位，再沿通道拼接后分块嵌入：

$$H_{vid} = \mathrm{PatchEmbed}(\mathrm{concat}_c(\tilde{\mathbf{x}}_t, \tilde{c}_{\mathrm{vae}}, \tilde{m}_{\mathrm{ref}}))$$

### 5.3 交叉注意力条件化

视频令牌与来自联合条件和 CLIP 条件的交叉注意力输出之和：

$$H_{out} = H_{vid} + \mathrm{Attn}(\mathbf{Q}_{vid}, \mathbf{K}_{\mathrm{joint}}, \mathbf{V}_{\mathrm{joint}}) + \mathrm{Attn}(\mathbf{Q}_{vid}, \mathbf{K}_{\mathrm{clip}}, \mathbf{V}_{\mathrm{clip}})$$

### 5.4 训练与推理

训练使用两阶段课程学习策略，在从 OpenS2V-5M 筛选出的约 100 万视频-文本子集上进行，采用 512 个 xPU、全局批大小 512、学习率 5e-6 和 AdamW 优化器。推理使用 50 步 Rectified Flow 和无分类器引导（CFG），引导尺度 ω=5。

## 实验与分析

### 6.1 定量主结果

Table 1 展示了在 OpenS2V-Eval 基准上的定量比较结果。BindWeave 取得了最高的总分（57.61%）和 NexusScore（46.84%），优于所有对比方法，包括开源方法（Phantom, VACE, SkyReels-A2, MAGREF）和商业产品（Kling-1.6, Vidu-2.0, Pika, Hailuo）。


![[assets/figures/papers/iclr26_vision_multimodal_applications__image_and_video_generation__b001_FP2XNyV9WL_BindWeave_Sub/figures/004_Table_1.jpg]]
*Table 1: Quantitative comparison among different methods for subject-to-video task. Total score is the normalized weighted sum of other scores. “↑” higher is better.*

### 6.2 消融实验

Table 2 的消融实验表明，MLLM+T5（BindWeave）在所有指标上均优于仅使用 T5 的变体：

![[assets/figures/papers/iclr26_vision_multimodal_applications__image_and_video_generation__b001_FP2XNyV9WL_BindWeave_Sub/figures/008_Table_2.jpg]]
*Table 2: Quantitative ablation results comparing T5-only and T5+Qwen2.5-VL conditioning.*

- 总分从 55.16% 提升至 57.61%（+2.45%）
- MotionAmplitude 从 7.48% 提升至 13.91%（+6.43%）
- GmeScore 从 62.26% 提升至 67.79%（+5.53%）
- NaturalScore 从 63.38% 提升至 66.85%（+3.47%）

### 6.3 关键发现

1. **MLLM 的必要性**：仅依赖 MLLM 进行条件化（不含 T5 文本编码器）的架构在训练中不稳定且无法收敛（Figure 9），表明 T5 提供的精确语言锚点对稳定优化是必要的。

2. **提示冲突场景**：在提示词与参考图像冲突的场景下（提示词为“a man”，参考图为婴儿），大多数基线方法生成了成年男性，而 BindWeave 忠实保留了婴儿的外观（Figure 11）。

3. **复制-粘贴问题**：在简单提示词下，许多基线方法（如 Phantom, VACE）存在明显的复制-粘贴问题，主体在帧间静止不动，而 BindWeave 避免了此问题，生成了自然且时间上连贯的运动（Figure 12）。

### 6.4 用户研究

Table 3 和 Figure 7 的用户研究（20 名参与者）显示，BindWeave 在主体一致性方面取得了最佳表现，并在所有评估指标上领先。

### 补充图表

![[assets/figures/papers/iclr26_vision_multimodal_applications__image_and_video_generation__b001_FP2XNyV9WL_BindWeave_Sub/figures/002_Figure_2.jpg]]
*Figure 2: Framework of our method. A multimodal large language model performs cross-modal reasoning to ground entities and disentangle roles, attributes, and interactions from the prompt and optional reference images. The resulting subject-aware signals condition a Diffusion Transformer through cross-attention and lightweight adapters, guiding identity-faithful, relation-consistent, and temporally coherent video generation.*

![[assets/figures/papers/iclr26_vision_multimodal_applications__image_and_video_generation__b001_FP2XNyV9WL_BindWeave_Sub/figures/003_Figure_3.jpg]]
*Figure 3: Illustration of our adaptive multi-reference conditioning strategy.*



![[assets/figures/papers/iclr26_vision_multimodal_applications__image_and_video_generation__b001_FP2XNyV9WL_BindWeave_Sub/figures/011_Table_3.jpg]]
*Table 3: User study results comparing different methods. “Total Score” means the average score.*

## 方法谱系与知识库定位

BindWeave 属于主体一致性视频生成（subject-consistent video generation）领域，该领域旨在根据参考图像和文本提示生成保持主体身份的视频。与现有方法（如 Phantom, VACE）采用浅层融合范式不同，BindWeave 首次将 MLLM 引入作为深层推理引擎，实现了从“分离-融合”到“统一推理”的范式转变。

该方法建立在以下技术基础之上：
- **扩散模型**：基于 DiT（Peebles & Xie, 2023）和 Rectified Flow（Liu et al., 2022）
- **视频生成基础模型**：基于 Wan（Wan et al., 2025）的 VAE 和图像条件化方法
- **多模态理解**：使用 Qwen2.5-VL-7B（Bai et al., 2025）作为 MLLM
- **文本编码**：使用 T5（Raffel et al., 2020）提供精确语言锚点
- **语义特征**：使用 CLIP（Radford et al., 2021b）提供语义身份信号

BindWeave 的贡献在于提出了一种新的条件化范式，即利用 MLLM 的跨模态推理能力替代传统的浅层融合，为视频生成提供更丰富、更准确的高层语义指导。这一思路可推广至其他需要精细跨模态对齐的生成任务。

## 原文 PDF

![[paperPDFs/ICLR_2026/BindWeave_Subject_Consistent_Video_Generation_via_Cross_Modal_Integration.pdf]]
