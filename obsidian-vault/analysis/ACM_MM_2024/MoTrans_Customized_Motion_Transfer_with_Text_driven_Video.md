---
title: "MoTrans: Customized Motion Transfer with Text-driven Video"
type: paper
paper_level: A
venue: "ACM MM"
year: 2024
pdf_ref: paperPDFs/ACM_MM_2024/MoTrans_Customized_Motion_Transfer_with_Text_driven_Video.pdf
aliases:
- MoTrans
tags:
- ACM_MM_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: "通过多模态大语言模型（MLLM）重描述器扩展提示、外观注入模块以及运动特定残差嵌入，促进外观与运动的解耦，增强运动建模。"
primary_logic: "利用互补的文本和视觉多模态信息在不同训练阶段分别建模外观和运动，并通过动词嵌入增强来捕获特定运动模式，从而有效缓解有限数据下的过拟合问题。"
claims:
- "在单一和多个参考视频设置下，MoTrans 在 CLIP-T、CLIP-E、TempCons 和 MoFid 指标上均优于所有对比方法。"
- "消融研究显示，移除 MLLM 重描述器或外观注入器导致 CLIP 分数下降、运动保真度升高，表明外观过拟合；移除运动增强器导致 MoFid 下降，证明其对运动学习的必要性。"
- "用户研究显示 MoTrans 在文本对齐、时间一致性、与参考视频动作相似性三个维度均获得最高比例，与定量结果一致。"
- "Custom Motion Dataset (12 motion types) 上 CLIP-T (↑) = 0.2275"
---

# MoTrans: Customized Motion Transfer with Text-driven Video

> [!tip] 核心洞察
> 利用互补的文本和视觉多模态信息在不同训练阶段分别建模外观和运动，并通过动词嵌入增强来捕获特定运动模式，从而有效缓解有限数据下的过拟合问题。

| 字段 | 内容 |
| ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 中文题名 | MoTrans：基于文本驱动视频扩散模型的定制化动作迁移 |
| 英文题名 | MoTrans: Customized Motion Transfer with Text-driven Video |
| 会议/期刊 | ACM MM 2024 |
| Links | [paper](https://arxiv.org/abs/2412.01343) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | MoTrans |
| Dataset | Custom Motion Dataset (12 motion types) |

> [!tip] 效果简介
> - Custom Motion Dataset (12 motion types) 上，CLIP-T (↑) 为 0.2275，对比 0.2079 (MotionDirector)，变化 +0.0196。
> - Custom Motion Dataset (12 motion types) 上，CLIP-E (↑) 为 0.2192，对比 0.2137 (MotionDirector)，变化 +0.0055。
> - Custom Motion Dataset (12 motion types) 上，TempCons (↑) 为 0.9895，对比 0.9801 (MotionDirector)，变化 +0.0094。

## 概述

预训练文本到视频（T2V）扩散模型在生成复杂、以人为中心的动作时面临瓶颈：直接在有限参考视频上微调，极易导致外观与运动耦合，模型倾向于记忆参考帧的视觉外观，而非学习可迁移的运动模式。**MoTrans** 针对这一瓶颈，提出以多模态信息解耦为核心的两阶段定制化动作迁移框架。

其核心思路是：利用互补的文本与视觉多模态信息，在不同训练阶段分别建模外观和运动。具体而言，在外观学习阶段，通过多模态大语言模型（MLLM）重描述器将基础文本提示扩展为外观丰富的描述，仅训练空间 LoRA 以充分捕获外观信息；在运动学习阶段，冻结空间 LoRA 并共享权重，通过外观注入模块将视频帧的图像嵌入作为外观先验注入时间 Transformer 之前，迫使时间 LoRA 聚焦于运动建模，同时引入基于动词嵌入的残差运动增强器，以捕获参考视频中的特定运动模式。这一设计有效缓解了有限数据下的过拟合问题，在单一参考视频（one-shot）和多个参考视频（few-shot）设置下均取得了最优性能。

在包含 12 种动作类别的 Custom Motion Dataset 上，MoTrans 在文本对齐（CLIP-T）、实体对齐（CLIP-E）、时间一致性（TempCons）和运动保真度（MoFid）四项指标上全面超越 **MotionDirector**、**LAMP**、**DreamVideo** 等现有方法：few-shot 设置下 CLIP-T 达到 0.2275，MoFid 达到 0.5695，较 MotionDirector 分别提升 +0.0196 和 +0.0278（Table 1）。消融研究进一步验证了各组件的必要性：移除 MLLM 重描述器或外观注入器会导致 CLIP 分数下降而 MoFid 异常升高，表明外观过拟合；移除运动增强器则直接导致 MoFid 显著降低（从 0.5695 降至 0.5541），证实残差动词嵌入对运动学习的关键作用（Table 2）。用户研究同样表明，MoTrans 在文本对齐、时间一致性及与参考视频动作相似性三个维度均获得最高比例（Figure 6）。

当前方法的局限在于：主要适用于以人体为中心的动作迁移，难以泛化至无肢体物体（如鱼类）；且仅针对 2–3 秒的短视频片段优化，长时序运动生成仍面临挑战。

## 背景与动机

文本到视频（T2V）扩散模型的快速发展使得从自然语言描述生成高质量视频成为可能。然而，预训练 T2V 模型在实际应用中面临一个核心瓶颈：**难以生成复杂、以人为中心的精确运动模式**。当用户希望将特定动作（如滑板推地、举杯饮水、弹吉他等）迁移到新的主体或场景时，现有方法暴露出明显的局限性。

直接对预训练 T2V 模型（如 **ZeroScope**、**VideoCrafter**）在有限参考视频上进行微调，是解决运动定制化的直观思路。但这种方法存在根本性的缺陷：**外观与运动的耦合**。在少样本甚至单样本设置下，模型极易将参考视频中的外观信息（人物衣着、背景、物体纹理）与运动模式一同“记住”，导致生成结果缺乏外观多样性，无法将运动迁移到新的主体上。换言之，模型学到的不是“如何动”，而是“谁在动”以及“在什么环境中动”。

这一问题的根源在于，预训练 T2V 模型的空间模块和时间模块在微调过程中缺乏有效的解耦机制。当训练数据极为有限时，模型倾向于将所有可观测特征——包括外观和运动——不加区分地编码到同一参数空间中，从而削弱了对运动模式本身的建模能力。

针对上述缺口，**MoTrans** 提出了一个核心洞察：利用互补的文本和视觉多模态信息，在不同训练阶段分别建模外观和运动，从而有效缓解有限数据下的过拟合问题。具体而言，该方法通过三个关键设计实现外观与运动的解耦：

1. **多模态大语言模型（MLLM）重描述器**：将基础文本提示扩展为全面描述外观的文本，引导空间模块充分学习外观信息，而非让运动模块承担外观建模的负担。
2. **外观注入模块**：在运动学习阶段，将参考视频帧的图像嵌入作为外观先验注入时间 Transformer 之前，迫使时间 LoRA 专注于运动动态建模。
3. **运动特定残差嵌入**：通过 MLP 学习动词标记的残差嵌入，增强文本条件中与运动相关的语义表示，使模型能够更精准地捕获参考视频中的特定运动模式。

MoTrans 在包含 12 种动作类型的 Custom Motion Dataset 上验证了其有效性。定量结果表明，该方法在 CLIP-T、CLIP-E、TempCons 和 MoFid 四项指标上均优于 **MotionDirector**、**LAMP**、**DreamVideo** 等主流定制化方法。消融研究进一步证实，移除任一解耦组件都会导致外观过拟合或运动保真度下降，验证了各模块的必要性。

## 核心创新

MoTrans 的核心创新在于通过**多模态信息的阶段化解耦**，系统性地解决预训练文本到视频（T2V）模型在有限参考视频上微调时面临的**外观-运动耦合瓶颈**。其关键设计可归纳为三个互为支撑的 changed slots：

### 1. 两阶段训练策略：外观与运动的分治建模

与单阶段微调直接学习外观-运动联合分布不同，MoTrans 将训练过程拆分为**外观学习阶段**和**运动学习阶段**。第一阶段仅训练空间 LoRA，冻结时间模块；第二阶段冻结空间 LoRA 权重并共享，转而训练时间 LoRA。这一设计迫使空间分支专注于外观信息，时间分支专注于运动动态，从结构层面实现解耦。消融实验从反面验证了该策略的必要性：若移除两阶段设计中的关键组件（如外观注入器或 MLLM 重描述器），模型会退化为外观过拟合——MoFid 升高但 CLIP-T/CLIP-E 下降（Table 2）。

### 2. 多模态先验注入：外观先验的显式引导

MoTrans 引入两类互补的多模态先验来强化外观建模并释放运动学习能力：

- **MLLM 重描述器**：利用多模态大语言模型将基础提示扩展为全面描述外观的文本（Figure 3）。扩展后的提示 $c_r$ 在空间损失 $\mathcal{L}_s$ 中作为条件，引导空间 LoRA 充分学习外观信息。移除该模块后，CLIP-T 从 0.2275 降至 0.2179，MoFid 反而升至 0.5997，证实模型在缺乏丰富外观描述时会过拟合参考视频的外观（Table 2, Figure 7）。

- **外观注入器**：在时间 Transformer 之前，将随机选择的视频帧图像嵌入通过线性层融合到空间 Transformer 输出的隐藏状态中：

  $$h_t^l = h_s^l \odot (W_{\mathcal{P}} \cdot \psi(\mathbf{f^i}))$$

  这一“预注入”机制为时间模块提供了显式的外观先验，使其无需自行建模外观，从而专注于运动动态。移除该模块导致 CLIP-T 降至 0.2143、MoFid 升至 0.6030，与移除重描述器的退化模式一致（Table 2）。

### 3. 运动特定残差嵌入：动词级运动增强

MoTrans 观察到视频中的运动模式通常与文本提示中的动词对齐，因此提出**运动增强器**来捕获参考视频中的特定运动模式。该模块通过 MLP 从视频帧的均值池化特征和动词基础文本嵌入中学习残差嵌入：

$$E_r = W_2 \cdot (\sigma_{GELU}(W_1 \cdot ([MeanPool(\psi(\mathcal{V})), \tau_{\theta}(\mathbf{s_i})])))$$

最终的增强运动条件嵌入为 $E_{cond} = E_b + E_r$，其中 $E_b$ 是基础动词嵌入，$E_r$ 是捕捉特定运动偏差的残差项，并通过 L2 正则化 $\mathcal{L}_{reg} = ||E_r||_2^2$ 约束其幅度。消融实验中，移除运动增强器后 MoFid 从 0.5695 显著降至 0.5541（few-shot），而 CLIP 分数几乎不变，证明该模块在不损害外观-文本对齐的前提下，是捕获特定运动模式的关键组件（Table 2）。

### 创新点之间的因果链条

三个 changed slots 形成清晰的因果链条：**MLLM 重描述器**提供丰富的外观文本条件，**外观注入器**提供显式的视觉外观先验，二者共同将外观信息从时间模块的学习目标中剥离；**两阶段训练**在结构上强制执行这一分工；**运动增强器**则在时间模块获得“纯净”运动学习空间后，通过动词级残差嵌入精准捕获特定运动模式。Table 2 的消融数据和 Figure 9 中 MoFid 与 CLIP 分数的权衡关系，共同验证了这一因果链条的有效性：任一组件的缺失都会破坏外观-运动解耦，导致过拟合或运动学习不足。

## 整体框架

![[assets/figures/papers/paper_list_l17_MoTrans_Customized_Motion_Transfer_with_Text_driven_Video/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the proposed MoTrans. In the appearance learning stage, an MLLM-based recaptioner is employed to extend the base prompt, encouraging the spatial LoRAs to sufficiently learn appearance information. The weights of spatial LoRAs are shared in the second stage. In the motion learning stage, video frame embeddings are injected as appearance priors, compelling the temporal LoRAs to concentrate on motion learning. Furthermore, we adopt MLP to learn a motion-specific embedding, which is jointly trained with the temporal LoRAs to fit specific motion patterns in the reference video*

MoTrans 的整体训练流水线分为两个阶段：**外观学习阶段**与**运动学习阶段**，如图 2 所示。其核心设计逻辑在于：预训练的文本到视频（T2V）扩散模型在有限参考视频上微调时，外观与运动极易耦合，导致模型要么过拟合参考视频的外观，要么无法有效捕获特定的运动模式。MoTrans 通过将外观和运动分别交由空间和时间模块处理，并引入互补的文本与视觉多模态先验来解耦二者。

**外观学习阶段**。给定参考视频 $\mathcal{V} = \{\mathbf{f}^i \mid i = 1, \dots, l\}$ 及其基础文本提示，首先利用一个基于多模态大语言模型（MLLM）的重描述器（recaptioner）将基础提示扩展为全面刻画外观的文本 $\mathbf{c}_r$（图 3）。随后，仅训练空间低秩适配器（Spatial LoRAs），冻结基座模型其余参数，以标准扩散去噪损失 $\mathcal{L}_s$（式 1）驱动空间模块充分学习参考帧的外观信息。该阶段训练完成后，空间 LoRA 的权重被冻结并共享至下一阶段。

**运动学习阶段**。在此阶段，外观信息通过**外观注入器**（Appearance Injector）被预先注入时间 Transformer 之前的隐藏状态中：随机选取的参考视频帧经图像编码器 $\psi$ 提取嵌入后，通过线性层 $W_{\mathcal{P}}$ 广播并与空间 Transformer 输出的隐藏状态 $\mathbf{h}_s^l$ 逐元素相加（式 2），形成外观先验 $\mathbf{h}_t^l$。这一设计迫使后续的时间 LoRAs 专注于运动动态建模，而非外观重建。

与此同时，**运动增强器**（Motion Enhancer）从文本侧强化运动表示。直觉上，视频中的运动模式通常与提示中的动词对齐。MoTrans 将基础动词嵌入 $\tau_\theta(\mathbf{s}_i)$ 与参考视频帧均值池化特征 $MeanPool(\psi(\mathcal{V}))$ 拼接后送入一个 MLP，生成运动特定的残差嵌入 $E_r$（式 3），再与基础运动嵌入 $E_b$ 相加得到增强的运动条件嵌入 $E_{cond}$（式 4）。最终，运动学习阶段的总损失 $\mathcal{L}_{motion}$ 由视频帧级 MSE 损失 $\mathcal{L}_t$ 与残差嵌入的 L2 正则项 $\mathcal{L}_{reg}$ 加权组合而成（式 6–7），其中 $\lambda$ 为 $10^{-4}$。

**推理流程**。训练完成后，给定目标文本提示，MoTrans 利用冻结的空间 LoRA 保持外观信息，同时通过时间 LoRA 和增强的运动嵌入驱动生成具有参考视频运动模式的新视频。受益于两阶段解耦设计，外观与运动可分别由 UNet 的空间和时间 Transformer 独立控制——例如，可将参考视频的运动迁移至由示例图像指定的新主体上（图 8）。

> **证据强度说明**：上述框架描述均来自论文第 3 节的明确声明（置信度 ≥ 0.95），消融实验（表 2、图 7）进一步证实了各模块的必要性：移除 MLLM 重描述器或外观注入器会导致 CLIP-T/CLIP-E 下降而 MoFid 升高，表明外观过拟合；移除运动增强器则使 MoFid 显著降低，验证了残差动词嵌入对运动学习的因果作用。

## 核心模块与公式推导

### 整体架构与两阶段训练

MoTrans 的训练流程分为**外观学习阶段**和**运动学习阶段**（Figure 2）。基础 T2V 模型（ZeroScope）保持冻结，仅通过低秩适配器（LoRA）注入可训练参数。空间 LoRA 注入 UNet 的空间 Transformer，负责外观建模；时间 LoRA 注入时间 Transformer 的自注意力和前馈网络，负责运动建模。两阶段权重共享策略使外观与运动解耦：第一阶段训练的空间 LoRA 权重在第二阶段冻结共享，迫使时间 LoRA 专注于运动模式学习。

### MLLM 重描述器（Appearance Learning Stage）

在外观学习阶段，给定参考视频的若干帧，MLLM 重描述器根据任务指令将基础提示扩展为全面描述外观的文本 $\mathbf{c}_r$（Figure 3）。该阶段仅训练空间 LoRA，损失函数为标准图像级去噪 MSE：

$$\mathcal{L}_s = \mathbb{E}_{\mathbf{z_0^i}, \mathbf{c}_r, \epsilon \sim N(0, I), t} \left[|| \epsilon - \epsilon_\theta (\mathbf{z_t^i}, \tau_\theta (\mathbf{c}_r), t) ||_2^2\right] \quad \text{(Eq. 1)}$$

其中 $\mathbf{z_0^i}$ 为单帧潜变量，$\tau_\theta(\mathbf{c}_r)$ 为重描述提示的文本嵌入，$\epsilon_\theta$ 为去噪网络。该阶段通过扩展提示引导空间 LoRA 充分学习参考视频的外观信息。

### 外观注入器（Appearance Injector）

进入运动学习阶段前，外观注入器将随机选取的视频帧图像嵌入作为外观先验注入时间 Transformer 之前（Figure 4(b)）。具体操作为：通过冻结的图像编码器 $\psi$ 提取帧嵌入 $\psi(\mathbf{f^i})$，经线性层 $W_{\mathcal{P}}$ 投影后与空间 Transformer 输出的隐藏状态 $h_s^l$ 逐元素相加：

$$h_t^l = h_s^l \odot (W_{\mathcal{P}} \cdot \psi(\mathbf{f^i})) \quad \text{(Eq. 2)}$$

该预注入机制迫使时间 LoRA 在已有外观信息的条件下专注于运动动态建模，有效缓解外观-运动耦合问题。

### 运动增强器（Motion Enhancer）

运动增强器的核心思路是：视频中的运动模式通常与文本提示中的动词对齐，强化动词嵌入可增强运动建模能力。该模块通过 MLP 学习一个运动特定的残差嵌入 $E_r$，与基础动词嵌入 $E_b$ 相加形成增强的运动条件嵌入。

残差嵌入的生成过程（Figure 2(b)）：首先通过图像编码器提取参考视频所有帧的特征，进行均值池化 $MeanPool(\psi(\mathcal{V}))$；同时获取动词 $s_i$ 的基础文本嵌入 $\tau_\theta(s_i)$。两者拼接后经两层 MLP（含 GELU 激活）生成残差嵌入：

$$E_r = W_2 \cdot (\sigma_{GELU}(W_1 \cdot ([MeanPool(\psi(\mathcal{V})), \tau_{\theta}(\mathbf{s_i})]))) \quad \text{(Eq. 3)}$$

最终的运动条件嵌入为：

$$E_{cond} = E_b + E_r \quad \text{(Eq. 4)}$$

其中 $E_b$ 可视为通用运动类别的粗粒度嵌入，$E_r$ 则捕获参考视频中该运动的细粒度特定模式。为防止残差嵌入过大，施加 L2 正则化：

$$\mathcal{L}_{reg} = ||E_r||_2^2 \quad \text{(Eq. 5)}$$

### 运动学习阶段损失函数

运动学习阶段使用基础提示 $\mathbf{c}_b$（非重描述提示），在 $N$ 帧视频序列上进行去噪训练，时间损失为标准帧级 MSE：

$$\mathcal{L}_t = \mathbb{E}_{\mathbf{z}_0^{1:\mathrm{N}}, \mathbf{c}_b, \epsilon \sim \mathcal{N}(0, I), t} \left[||\epsilon - \epsilon_{\theta}(\mathbf{z_t^{1:\mathrm{N}}}, \tau_{\theta}(\mathbf{c}_b), t)||_2^2\right] \quad \text{(Eq. 6)}$$

运动学习总损失结合时间损失与正则化项：

$$\mathcal{L}_{motion} = \mathcal{L}_t + \lambda \mathcal{L}_{reg} \quad \text{(Eq. 7)}$$

$\lambda$ 为残差嵌入的正则化系数，实验中设为 $1\times10^{-4}$。

### 运动保真度评估指标（MoFid）

为量化生成视频与参考视频之间的运动一致性，MoTrans 引入基于 VideoMAE 特征的运动保真度指标。对于运动集合 $\mathcal{M}$ 中的每个运动 $m$，计算生成视频 $v_m^i$ 与参考视频 $\bar{v}_m$ 在 VideoMAE 特征空间中的平均余弦相似度：

$$\mathcal{E}_m = \frac{1}{\vert \mathcal{M} \vert \vert \bar{v}_m \vert} \sum_{m \in \mathcal{M}} \sum_{k=1}^{\vert \bar{v}_m \vert} cos(f(v_m^i), \bar{v}_k) \quad \text{(Eq. 8)}$$

其中 $f(\cdot)$ 为 VideoMAE 编码器，$\bar{v}_k$ 为参考视频的第 $k$ 帧特征。该指标与 CLIP-T/CLIP-E 配合使用：高 MoFid 配合低 CLIP 分数表明外观过拟合参考视频，运动保真度与文本对齐度之间的权衡关系如 Figure 9 所示。

## 实验与分析

### 评估设置

实验基于 **ZeroScope** 作为基础文本到视频（T2V）模型，在空间与时间 Transformer 中注入 LoRA（秩 32）进行微调。训练采用 AdamW 优化器，学习率 5e-4，约 600 步。推理使用 DDIM 采样器，30 步，分类器无关引导系数 12，生成 24 帧、8 fps 的约 3 秒视频。评估在自建的 **Custom Motion Dataset**（覆盖 12 种动作类型）上进行，包含单样本（one-shot）和少样本（few-shot）两种设定。

评估指标包括：
- **CLIP-T / CLIP-E**：衡量生成视频与文本/实体提示的语义对齐；
- **TempCons**：评估时序一致性；
- **MoFid**：基于 VideoMAE 特征的余弦相似度，量化生成视频与参考视频之间的运动保真度，公式为：

$$\mathcal{E}_m = \frac{1}{|\mathcal{M}| |\bar{v}_m|} \sum_{m \in \mathcal{M}} \sum_{k=1}^{|\bar{v}_m|} \cos(f(v_m^i), \bar{v}_k)$$

### 主实验结果

**表 1** 展示了 MoTrans 与 **Tune-a-Video**、**MotionDirector**、**LAMP** 等主流定制化方法的定量对比。在少样本设定下，MoTrans 在所有指标上均取得最优：CLIP-T 达 0.2275，CLIP-E 达 0.2192，TempCons 达 0.9895，MoFid 达 0.5695，分别超出最强基线 MotionDirector 约 +0.0196、+0.0055、+0.0094、+0.0278。单样本设定下，MoTrans 同样在 CLIP-T 和 CLIP-E 上领先。

![[assets/figures/papers/paper_list_l17_MoTrans_Customized_Motion_Transfer_with_Text_driven_Video/figures/007_Table_1.jpg]]
*Table 1: Quantitative evaluation of customized motion transfer methods. The best results under one-shot and few-shot settings are highlighted in blue and red, respectively*

在多参考视频场景下，**表 3** 显示 MoTrans 的 CLIP-T（0.2168）显著优于 **DreamVideo**（0.1791），提升约 +0.0377，表明其运动迁移与文本对齐能力在多视频条件下仍保持优势。

![[assets/figures/papers/paper_list_l17_MoTrans_Customized_Motion_Transfer_with_Text_driven_Video/figures/012_Table_3.jpg]]
*Table 3: Quantitative comparison results of motion customization on multiple videos*

定性结果（**图 5**）显示，MoTrans 生成的视频在保持参考运动模式的同时，能有效将动作迁移到不同外观的主体上，而对比方法常出现外观残留或运动模糊。

用户研究（**图 6**）从文本对齐、时序一致性、与参考视频动作相似性三个维度进行主观评估，MoTrans 在所有维度均获得最高比例，与定量指标相互印证。

### 消融实验

**表 2** 和 **图 7** 报告了关键模块的消融结果：

![[assets/figures/papers/paper_list_l17_MoTrans_Customized_Motion_Transfer_with_Text_driven_Video/figures/008_Table_2.jpg]]
*Table 2: Quantitative results of the ablation study*

- **移除 MLLM 重描述器**：CLIP-T 降至 0.2179，CLIP-E 同步下降，但 MoFid 反而升至 0.5997。这表明模型在缺乏扩展提示时过度拟合参考视频外观，牺牲了文本对齐能力。
- **移除外貌注入器**：CLIP-T 降至 0.2143，MoFid 升至 0.6030，同样呈现外观过拟合趋势，证实外观注入对解耦外观与运动具有关键作用。
- **移除运动增强器（残差动词嵌入）**：MoFid 从 0.5695 降至 0.5541，说明动词特定的残差嵌入对捕捉参考视频中的精细运动模式不可或缺。

**图 9** 进一步揭示了文本/实体对齐与运动保真度之间的权衡关系：高 MoFid 伴随低 CLIP-T/CLIP-E 意味着模型外观过拟合，缺乏多样性；MoTrans 在二者之间取得了更优的平衡。

### 失败模式与局限

论文明确指出两类主要局限：
1. **运动类型不匹配**：当前方法针对以人体为中心的动作设计，不适合将人体运动（如跑步）迁移到无肢体的物体（如鱼），因为动作本质差异导致迁移失效。
2. **时长限制**：模型仅针对 2–3 秒的短视频片段优化，生成长时间运动序列仍面临时序一致性与运动多样性保持的挑战。

此外，MoFid 指标依赖 VideoMAE 特征，当动作类别与预训练分布不匹配时可能存在偏差，需要更鲁棒的运动评估方案，这一点尚待进一步验证。

### 补充图表

![[assets/figures/papers/paper_list_l17_MoTrans_Customized_Motion_Transfer_with_Text_driven_Video/figures/003_Figure_4.jpg]]
*Figure 4: Details of trainable LoRAs and appearance injector. (a) Parameters of the base model are frozen and only parameters of LoRAs are updated. (b) The image embedding is processed through a Linear layer before being fused with the hidden states from the spatial transformers. This preinjected appearance prior encourages the temporal LoRAs to capture motion patterns effectively*

![[assets/figures/papers/paper_list_l17_MoTrans_Customized_Motion_Transfer_with_Text_driven_Video/figures/015_Figure.jpg]]

![[assets/figures/papers/paper_list_l17_MoTrans_Customized_Motion_Transfer_with_Text_driven_Video/figures/016_Figure_13.jpg]]
*Figure 13: Additional qualitative comparisons on customized motion transfer given multiple reference videos*

## 方法谱系与知识库定位

### 问题定位与核心瓶颈

预训练文本到视频（T2V）扩散模型（如 **ZeroScope**、**VideoCrafter**）在生成以人为中心的复杂运动时面临一个关键瓶颈：在少量参考视频上微调时，模型极易将外观信息与运动模式耦合在一起，导致运动学习能力大幅削弱。具体而言，当模型试图从参考视频中学习特定的动作模式（如“滑板推地滑行”或“抬手喝水”）时，它往往同时记住了参考视频中人物的外观、背景等视觉元素，使得生成结果缺乏外观多样性，甚至直接复制参考帧。这一“外观-运动耦合”问题在单样本（one-shot）或少样本（few-shot）设置下尤为突出。

### 现有方法谱系

在定制化视频生成领域，已有方法可大致分为以下几类：

**单样本定制化方法**：以 **Tune-a-Video** 为代表，通过对单段参考视频进行微调来实现外观或运动的迁移。这类方法虽然开创了视频定制化的范式，但在运动建模方面缺乏专门的解耦设计，容易导致外观过拟合。

**运动定制化基线方法**：**MotionDirector** 是当前运动迁移任务的主要基线。该方法通过双路径架构分别处理外观和运动信息，在一定程度上缓解了耦合问题。然而，它在处理复杂人体运动时仍存在外观泄漏，且对文本条件的利用较为有限。

**少样本动作定制化方法**：**LAMP** 在少样本设置下尝试学习动作模式，但其训练策略未明确分离外观与运动的学习阶段。

**双分支适配器方法**：**DreamVideo** 采用双分支适配器分别处理外观和运动，但其在多参考视频场景下的文本对齐能力（CLIP-T 仅 0.1791）和运动保真度均弱于 MoTrans。

### MoTrans 的方法学突破

MoTrans 的核心创新在于**利用互补的多模态信息在不同训练阶段分别建模外观和运动**，通过三个关键设计实现了外观与运动的有效解耦：

1. **两阶段训练策略**：将训练过程明确划分为外观学习阶段和运动学习阶段。第一阶段仅训练空间 LoRA，使用 MLLM 重描述器扩展的提示来充分学习外观信息；第二阶段冻结空间 LoRA 权重，转而训练时间 LoRA 以捕获运动模式。这种分阶段策略从根本上避免了外观与运动在训练过程中的相互干扰。

2. **多模态先验注入**：通过 MLLM 重描述器（文本模态）和外观注入器（视觉模态）分别提供互补的先验信息。重描述器将基础提示扩展为全面描述外观的文本，引导空间 LoRA 专注于外观学习；外观注入器则将视频帧的图像嵌入注入到时间 Transformer 之前，迫使时间 LoRA 聚焦于运动建模。消融实验证实，移除任一组件都会导致 CLIP 文本/实体对齐分数下降、运动保真度升高——这正是外观过拟合的典型信号。

3. **运动特定残差嵌入**：基于“运动模式通常与文本中的动词对齐”这一直觉，MoTrans 通过 MLP 学习动词标记的残差嵌入，增强运动特定的文本条件。该嵌入由视频帧的均值池化特征和动词基础文本嵌入共同生成，使模型能够精确捕捉参考视频中的特定运动模式。消融实验中，移除运动增强器后 MoFid 从 0.5695 降至 0.5541，验证了该设计的必要性。

### 适用边界与局限

**适用场景**：
- 以人体为中心的动作迁移（如运动、舞蹈、日常动作）
- 单一或多段参考视频的动作定制化
- 需要将特定动作迁移到新主体或新场景的任务
- 2-3 秒短视频片段的运动生成

**已知局限**：
- **跨形态迁移受限**：不适合将人体中心运动迁移到无肢体的物体（如鱼），因为动作本质不同，模型缺乏处理此类跨形态运动映射的能力。
- **时序长度受限**：目前仅针对 2-3 秒的短视频段优化，生成长时间视频仍然面临挑战，运动一致性与多样性难以在更长时序上同时保持。
- **运动评估偏差风险**：MoFid 指标基于 VideoMAE 特征计算余弦相似度，当动作类别与预训练数据分布不匹配时可能存在偏差，需要更鲁棒的运动评估方案。

### 开放问题

1. **跨形态运动迁移**：如何将定制化运动迁移扩展到无肢体的物体或抽象主体？这需要模型理解动作的抽象语义，而非仅仅复制关节运动轨迹。

2. **长时序运动生成**：如何实现更长时间的运动序列生成，同时保持运动一致性与多样性？当前的两阶段训练策略在长视频场景下可能面临计算开销和时序建模能力的双重挑战。

3. **运动评估的鲁棒性**：MoFid 依赖 VideoMAE 特征空间中的余弦相似度，当参考动作与生成动作在语义上相似但视觉表现不同时，该指标可能无法准确反映运动保真度。是否有更鲁棒的运动评估方案，能够捕捉运动模式的语义等价性？

4. **多动作组合与过渡**：当前方法针对单一动作模式进行定制化，如何处理多个动作的组合与自然过渡，使生成视频包含更复杂的动作序列？

## 原文 PDF

![[paperPDFs/ACM_MM_2024/MoTrans_Customized_Motion_Transfer_with_Text_driven_Video.pdf]]
