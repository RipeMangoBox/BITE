---
title: "LLaVA-4D: Embedding SpatioTemporal Prompt into LMMs for 4D Scene Understanding"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/LLaVA_4D_Embedding_SpatioTemporal_Prompt_into_LMMs_for_4D_Scene_Understanding.pdf
openreview_forum_id: URpbmVEsqB
aliases:
- L4
- LLaVA-4D
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "引入基于4D坐标（3D位置+1D时间）的动态感知时空提示，并将其与时空解耦的视觉特征融合。该提示通过可学习的傅里叶特征编码3D位置，并在时间编码中引入光流作为运动辅助信息，使模型能够有效区分静态背景和动态物体。"
primary_logic: "静态背景与动态物体在空间位置上具有相似性，但在时间维度上运动模式差异显著；同时，视觉特征可以被解耦为空间分量（关注外观）和时间分量（关注运动），这种解耦表示本身更具判别力，再结合4D坐标提示可以大幅提升4D场景理解性能。"
claims:
- "添加4D坐标嵌入、特征解耦和特征融合三个模块后，Chat4D基准上的CIDEr、BLEU-4、SAcc@0.5、TAcc分别从62.3/11.7/34.8/12.7提升至93.5/17.2/58.9/54.6。"
- "与仅使用3D位置编码或1D时间编码相比，完整的4D坐标编码在所有指标上均取得最佳性能（CIDEr:93.5, BLEU-4:17.2, SAcc@0.5:58.9, TAcc:54.6）。"
- "时空解耦特征可视化显示，解耦后的特征能够清晰地区分背景和物体簇，而原始视觉特征中物体区域分散。"
- "基于注意力的融合策略（Attention）在各项指标上均优于简单拼接和加权融合，验证了自适应调整融合权重的重要性。"
---

# LLaVA-4D: Embedding SpatioTemporal Prompt into LMMs for 4D Scene Understanding

> [!tip] 核心洞察
> 静态背景与动态物体在空间位置上具有相似性，但在时间维度上运动模式差异显著；同时，视觉特征可以被解耦为空间分量（关注外观）和时间分量（关注运动），这种解耦表示本身更具判别力，再结合4D坐标提示可以大幅提升4D场景理解性能。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | LLaVA-4D：将时空提示嵌入大型多模态模型以实现4D场景理解 |
| 英文题名 | LLaVA-4D: Embedding SpatioTemporal Prompt into LMMs for 4D Scene Understanding |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=URpbmVEsqB); [GitHub](https://github.com/hyzhouboy/LLaVA-4D) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | LLaVA-4D |
| Dataset | VSI-Bench, Chat4D |

> [!tip] 效果简介
> - VSI-Bench 上，Average Accuracy 为 48.6，对比 48.4 (Spatial-MLLM)，变化 +0.2。
> - Chat4D 上，CIDEr 为 93.5。
> - Chat4D 上，BLEU-4 为 17.2。

## 概述

### 问题瓶颈

现有3D大语言多模态模型（3D LMMs）在理解物理世界时，仅将3D位置坐标作为空间提示注入视觉特征，以统一的静态空间表示处理场景。这一范式在应对包含动态物体的4D场景时暴露出根本性缺陷：静态背景与动态物体在空间位置上可能高度相似，但运动模式截然不同，而3D LMMs缺乏时间维度的建模能力，无法捕捉物体的运动轨迹与状态变化，导致对动态场景的理解能力严重不足。

### 核心思路

LLaVA-4D 的核心洞察在于：**视觉特征可以被解耦为空间分量（关注外观）和时间分量（关注运动），这种解耦表示本身更具判别力；再结合4D坐标提示（3D位置 + 1D时间），可大幅提升4D场景理解性能。** 基于此，方法引入了三个关键机制：

- **动态感知4D坐标编码**：将多视角视频中的2D像素反投影至世界坐标系，构建 $[x,y,z,t]$ 四维张量，对位置和时间分别进行可学习傅里叶编码，并在时间编码中引入光流作为运动辅助信息，使模型能够区分静态背景与动态物体。
- **时空解耦视觉嵌入**：通过计算跨视图相关性与跨时间相关性，将视觉特征显式分离为空间特征 $f_s$ 和时间特征 $f_t$，可视化表明解耦后的特征能清晰地区分背景和物体簇，而原始视觉特征中物体区域分散（Figure 3）。
- **基于交叉注意力的融合**：以4D坐标嵌入 $p_{4D}$ 为查询，与时空视觉特征进行交叉注意力融合，并通过学习到的目标门控 $\alpha$ 动态平衡融合输出与原始空间特征，实现自适应信息整合。

### 主要结果

在4D场景理解基准 Chat4D 上，LLaVA-4D 取得了显著性能：逐步增加坐标嵌入、特征解耦和特征融合三个模块后，CIDEr 从 62.3 提升至 93.5，BLEU-4 从 11.7 提升至 17.2，空间准确率 SAcc@0.5 从 34.8 提升至 58.9，时间准确率 TAcc 从 12.7 提升至 54.6（Table 4）。与仅使用3D位置编码或1D时间编码相比，完整的4D坐标编码在所有指标上均取得最佳性能（Table 5）。在空间智能基准 VSI-Bench 上，LLaVA-4D 以 48.6 的平均准确率超越当前最强基线 **Spatial-MLLM**（Wu et al., arXiv 2025）的 48.4（Table 2）。

### 方法定位

LLaVA-4D 属于**时空提示增强的4D多模态大模型**，在方法谱系上位于3D LMMs（如 **LLaVA-3D**，Zhu et al., arXiv 2024）与视频理解LMMs（如 **Video-3D LLM**，Zheng et al., arXiv 2024）的交汇处。其核心贡献在于首次将动态感知的4D坐标作为可学习提示嵌入LMM，并通过时空解耦表示实现静态场景与动态物体的联合理解，为4D场景理解建立了新的基线范式。

## 背景与动机

三维场景理解是具身智能与空间推理的核心能力。近年来，大型多模态模型（LMM）通过将3D位置编码为空间提示，在静态场景的视觉问答、密集描述和视觉定位等任务上取得了显著进展。然而，现实世界的物理场景本质上是动态的——物体在时间维度上持续运动，其空间位置随时间演化。现有3D LMM（如**LLaVA-3D**, Zhu et al., arXiv 2024; **Video-3D LLM**, Zheng et al., arXiv 2024）将多视角视觉特征以统一空间表示处理，仅使用3D位置作为空间提示，**无法捕捉动态物体随时间变化的运动模式**，导致对包含动态物体的4D场景理解能力严重不足。

这一瓶颈的根源在于：静态背景与动态物体在空间位置上可能具有相似性，但在时间维度上运动模式差异显著。例如，一个静止的桌子和一个正在移动的椅子在某一时刻的3D坐标可能相近，但二者的运动轨迹截然不同。若模型缺乏时间维度的感知能力，就无法有效区分二者。与此同时，视觉特征本身可以被解耦为空间分量（关注跨视图外观一致性）和时间分量（关注跨帧运动相关性），这种解耦表示本身比统一视觉特征更具判别力（**Figure 3** 的可视化表明，原始视觉特征中动态物体区域分散，而时空解耦特征能清晰区分背景与物体簇）。

针对上述缺口，本文提出 **LLaVA-4D**，核心动机是：**将动态感知的4D时空提示嵌入LMM**，使模型具备同时理解空间位置和时间演化的能力。具体而言，LLaVA-4D 引入三个关键设计：
1. **动态感知4D坐标编码**：基于3D位置和1D时间构建4D坐标张量 $[x,y,z,t]$，并利用光流作为运动辅助信息增强时间编码；
2. **时空解耦视觉嵌入**：将多视角视频特征显式分离为空间特征和时间特征；
3. **交叉注意力融合**：以4D坐标嵌入为查询，自适应融合时空视觉特征。

消融实验（**Table 4**）表明，逐步添加上述三个模块后，Chat4D基准上的CIDEr从62.3提升至93.5，BLEU-4从11.7提升至17.2，空间准确率SAcc@0.5从34.8提升至58.9，时间准确率TAcc从12.7提升至54.6，验证了各模块对4D场景理解的累积贡献。

## 核心创新

LLaVA-4D 的核心创新在于将**动态感知的4D时空提示**系统性地嵌入大型多模态模型（LMM），从而将3D场景理解范式提升至4D。其关键洞察是：静态背景与动态物体在空间位置上具有相似性，但在时间维度上运动模式差异显著；同时，视觉特征可以被解耦为空间分量（关注外观）和时间分量（关注运动），这种解耦表示本身更具判别力。基于此，该方法引入了三个紧密协作的**changed slots**：

### 1. 动态感知4D坐标编码（坐标编码 slot）

**基线方法**（如 **LLaVA-3D**，Zhu et al., arXiv 2024）仅使用3D位置编码作为空间提示，将视觉特征以统一空间表示处理，完全忽略时间维度，导致对动态物体运动模式的捕捉能力严重不足。

**LLaVA-4D** 构建了完整的4D坐标张量 $[x, y, z, t]$：利用相机内外参和深度将2D像素反投影至世界坐标系获取3D位置，同时引入光流作为运动辅助信息调制时间编码。具体而言，空间编码采用可学习的傅里叶特征：

$$p_{xyz} = \mathrm{PE}(x,y,z) = 1/\sqrt{d}[\cos([x,y,z]W_r^\top) \parallel \sin([x,y,z]W_r^\top)]$$

时间编码则通过光流 $\beta$ 增强动态感知能力：

$$p_t = \mathrm{TE}(t) \cdot \beta = 1/\sqrt{d}[\cos(t W_r^\top) \parallel \sin(t W_r^\top)] \cdot (1 + \Phi(\beta))$$

最终形成时空提示 $p_{4D} = w_p \cdot [\mathrm{PE}(x,y,z) \parallel \mathrm{TE}(t) \cdot \beta]$。消融实验（Table 5）表明，完整的4D坐标编码（3D位置+1D时间）在所有指标上均显著优于无编码、仅3D位置或仅1D时间编码，CIDEr从62.3提升至93.5，TAcc从12.7提升至54.6。

### 2. 时空解耦视觉嵌入（视觉特征表示 slot）

**基线方法**使用统一的视觉特征，不区分空间和时间成分，导致动态物体的特征分散、与背景难以区分（Figure 3左）。

**LLaVA-4D** 提出时空解耦视觉嵌入 $\mathrm{STD}(f)$，显式地将多视角视频的视觉特征分离为空间特征 $f_s$（通过计算跨视图相关性获得，关注外观）和时间特征 $f_t$（通过计算跨帧相关性获得，关注运动）。可视化证据（Figure 3右）显示，解耦后的特征能够清晰地区分背景和物体簇，而原始视觉特征中物体区域分散。消融实验（Table 4）证实，单独添加特征解耦即可将CIDEr从62.3提升至72.8，SAcc@0.5从34.8提升至40.2。

### 3. 基于注意力的时空特征融合（特征融合机制 slot）

**基线方法**通常采用简单拼接或未专门设计融合模块，无法自适应地调整坐标信息与视觉特征的整合权重。

**LLaVA-4D** 设计了基于交叉注意力的融合策略，以4D坐标嵌入 $p_{4D}$ 作为查询，与拼接的时空视觉特征 $[f_s, f_t]$ 进行交叉注意力计算，并通过可学习的目标门控 $\alpha$ 动态平衡融合输出与原始空间特征：

$$f_{st} = \alpha \cdot \mathrm{softmax}\left(\frac{(w_q p_{4D})(w_k[f_s,f_t])^\top}{\sqrt{d}}\right)(w_v[f_s,f_t]) + (1-\alpha)\cdot f_s$$

其中 $\alpha = \sigma(\mathrm{MLP}_{obj}(p_{4D}))$ 由4D坐标自适应学习，使模型能根据场景内容动态调整融合强度。Table 6的消融实验表明，基于注意力的融合策略在CIDEr（93.5）、BLEU-4（17.2）、SAcc@0.5（58.9）、TAcc（54.6）上均优于简单拼接和加权融合，验证了动态调整融合权重的关键作用。

### 4. 文本侧坐标对齐（语言侧坐标对齐 slot）

**基线方法**未对文本中的时空坐标进行编码，LLM需要从原始文本中隐式理解位置和时间信息，容易产生误解。

**LLaVA-4D** 对文本指令中的位置标签 $tp$ 和时间标签 $tt$ 应用相同的时空编码：$\tau_s = \mathrm{PE}(tp), \tau_t = \mathrm{TE}(tt)$，并将其融入词嵌入。Table 7显示，这一设计在所有指标上均有提升，进一步减少了LLM对时空坐标的误解。

### 模块协同效应

三个核心模块（坐标编码、特征解耦、特征融合）之间存在显著的协同效应（Table 4）：逐步添加各模块时，CIDEr从62.3→72.8→78.5→93.5，TAcc从12.7→25.3→30.8→54.6，呈阶梯式提升。其中坐标编码贡献了最大的性能跃升（TAcc提升约24点），而特征解耦和融合在此基础上进一步释放了4D场景理解的上限。

## 整体框架

![[assets/figures/papers/paper_list_l19_https_openreview_net_forum_id_URpbmVEsqB/figures/002_Figure_2.jpg]]
*Figure 2: Our LLaVA-4D consists of three stages: 1) 4D coordinate encoding. Encode 3D position and 1D time with optical flow. 2) Vision embedding. Disentangle visual features into spatiotemporal features and embed the encoded 4D coordinates via cross-attention fusion. 3) Language embedding. Align textual position and time with the fused vision embedding for 4D scene understanding*

LLaVA-4D 的整体架构围绕一个核心设计展开：将动态感知的时空提示（spatiotemporal prompt）系统性地嵌入大型多模态模型（LMM），使其从仅理解静态3D场景跨越到能够理解包含动态物体的4D场景。整个pipeline由三个紧密协作的阶段构成，如 **Figure 2** 所示。

### 阶段一：动态感知的4D坐标编码

该阶段负责将多视角视频的原始像素信号转化为携带运动信息的4D时空坐标表示。具体而言，系统首先利用SfM（Structure from Motion）和MVS（Multi-View Stereo）估计相机姿态与深度，将各帧的2D像素通过反投影变换至世界坐标系：

$$x_{3D} = R^{-1} (D(x_{2D}) \cdot K^{-1} x_{2D} - T)$$

随后，将得到的3D位置与对应的时间戳拼接，形成4D坐标张量 $[x, y, z, t]$。这一坐标张量并非直接送入模型，而是经过可学习的傅里叶特征编码转化为高维嵌入。其中，空间编码 $p_{xyz}$ 对3D坐标进行映射：

$$p_{xyz} = \mathrm{PE}(x,y,z) = 1/\sqrt{d}[\cos([x,y,z]W_r^\top) \parallel \sin([x,y,z]W_r^\top)]$$

时间编码 $p_t$ 则引入光流 $\beta$ 作为运动辅助信息，通过softmax归一化后调制时间嵌入，使模型感知运动强度：

$$p_t = \mathrm{TE}(t) \cdot \beta = 1/\sqrt{d}[\cos(t W_r^\top) \parallel \sin(t W_r^\top)] \cdot (1 + \Phi(\beta))$$

最终，空间与时间编码经MLP投影后组合为统一的动态感知时空提示：

$$p_{4D} = w_p \cdot [\mathrm{PE}(x,y,z) \parallel \mathrm{TE}(t) \cdot \beta]$$

### 阶段二：时空解耦的视觉嵌入与融合

视觉编码器（CLIP-ViT-L-336px）从多视角视频中提取统一的视觉特征 $f$，这些特征在原始空间中难以区分静态背景与动态物体。LLaVA-4D 通过 **STD（Spatiotemporal Disentanglement）** 模块将其显式解耦为空间特征 $f_s$ 和时间特征 $f_t$：$f_s, f_t = \mathrm{STD}(f)$。**Figure 3** 的可视化表明，解耦后的特征能清晰地区分背景簇与物体簇，而原始视觉特征中物体区域分散、与背景混杂。

解耦完成后，系统以4D坐标嵌入 $p_{4D}$ 作为查询（Query），对拼接后的时空特征 $[f_s, f_t]$ 执行交叉注意力融合。融合过程还引入一个可学习的门控权重 $\alpha$，动态平衡融合输出与原始空间特征：

$$f_{st} = \alpha \cdot \mathrm{softmax}\left(\frac{(w_q p_{4D})(w_k[f_s,f_t])^\top}{\sqrt{d}}\right)(w_v[f_s,f_t]) + (1-\alpha)\cdot f_s$$

这一设计使模型能够根据场景内容自适应地决定对时空提示的依赖程度。

### 阶段三：坐标对齐的语言嵌入

融合后的时空视觉特征 $f_{st}$ 经MLP投影为语言空间的视觉token $\tau_v^{st}$。与此同时，对文本指令中出现的位置描述 $tp$ 和时间描述 $tt$，系统应用与阶段一完全相同的空间编码 $\mathrm{PE}(\cdot)$ 和时间编码 $\mathrm{TE}(\cdot)$，生成文本侧坐标嵌入 $\tau_s$ 和 $\tau_t$，并融入语言token序列。这一坐标对齐策略有效减少了LLM对时空坐标的误解（见 **Table 7** 的消融验证）。最终，视觉token与语言token拼接后送入LLM（LLaVA-1.5-7B）进行推理。

### 训练流水线

训练过程分为三个递进阶段（**Figure 4 (b)**）：
- **阶段一（Content Alignment）**：仅更新交叉注意力融合模块和投影器参数，4D坐标特征暂以零填充，使模型先对齐视觉与语言的基本内容。
- **阶段二（Spatiotemporal Coordinate Alignment）**：利用Chat4D中的2D/3D视觉定位任务数据，精调坐标编码与融合模块，建立视觉-语言间的时空坐标对齐。
- **阶段三（4D Task Instruction Fine-Tuning）**：使用Chat4D的4D视觉语言数据，以多任务指令微调方式更新除视觉编码器外的全部参数，强化细粒度时空理解能力。

### 数据流总结

多视角视频 → SfM/MVS估计位姿与深度 → 反投影构建4D坐标 → 傅里叶编码（空间+光流调制时间）→ 视觉特征解耦为 $f_s, f_t$ → 交叉注意力融合 $p_{4D}$ 与 $[f_s, f_t]$ → MLP投影为视觉token → 文本坐标同步编码 → 拼接送入LLM → 输出4D场景理解结果。

## 核心模块与公式推导

LLaVA-4D 的核心架构由三个紧密协作的模块构成：动态感知 4D 坐标编码、时空解耦视觉嵌入，以及坐标对齐语言嵌入。其设计根植于一个核心洞察：静态背景与动态物体在空间位置上可能相似，但在时间维度上运动模式差异显著；同时，视觉特征可被解耦为关注外观的空间分量与关注运动的时间分量，这种解耦表示本身更具判别力，再结合 4D 坐标提示可大幅提升 4D 场景理解性能。

### 动态感知 4D 坐标编码

该模块的目标是将多视角视频中的像素映射到统一的 4D 时空坐标系，并生成富含运动信息的时空提示。首先，利用相机内外参和深度信息，将 2D 像素反投影至世界坐标系：

$$x_{3D} = R^{-1} (D(x_{2D}) \cdot K^{-1} x_{2D} - T)$$

其中 $R$、$T$ 为相机外参，$K$ 为内参，$D(x_{2D})$ 为像素深度。将时间维度与 3D 位置拼接，构建 4D 坐标张量 $[x, y, z, t]$。

随后，对 3D 位置和 1D 时间分别进行可学习的傅里叶特征编码。空间编码采用标准傅里叶映射：

$$p_{xyz} = \mathrm{PE}(x,y,z) = \frac{1}{\sqrt{d}}[\cos([x,y,z]W_r^\top) \parallel \sin([x,y,z]W_r^\top)]$$

时间编码则引入光流 $\beta$ 作为运动辅助信息，使编码对动态变化更敏感：

$$p_t = \mathrm{TE}(t) \cdot \beta = \frac{1}{\sqrt{d}}[\cos(t W_r^\top) \parallel \sin(t W_r^\top)] \cdot (1 + \Phi(\beta))$$

其中 $\Phi(\beta)$ 为 softmax 归一化后的光流值。最终，通过 MLP 权重 $w_p$ 组合空间与时间编码，形成动态感知的 4D 时空提示：

$$p_{4D} = w_p \cdot [\mathrm{PE}(x,y,z) \parallel \mathrm{TE}(t) \cdot \beta]$$

### 时空解耦视觉嵌入

视觉编码器（CLIP-ViT-L-336px）从多视角视频中提取特征 $f$ 后，通过计算跨视图相关性和跨时间相关性，将其显式解耦为空间特征 $f_s$ 和时间特征 $f_t$：

$$f_s, f_t = \mathrm{STD}(f)$$

其中 $f_s$ 关注跨视图的外观一致性，$f_t$ 关注跨帧的运动变化。Figure 3 的特征可视化验证了这一设计的有效性：解耦后的特征能够清晰地区分背景和物体簇，而原始视觉特征中物体区域分散、难以判别。

### 交叉注意力融合

为将 4D 坐标嵌入注入视觉表示，模块以 $p_{4D}$ 为查询，对拼接后的时空特征 $[f_s, f_t]$ 进行交叉注意力融合，并通过学习的目标门控 $\alpha$ 动态平衡融合输出与原空间特征：

$$f_{st} = \alpha \cdot \mathrm{softmax}\left(\frac{(w_q p_{4D})(w_k[f_s,f_t])^\top}{\sqrt{d}}\right)(w_v[f_s,f_t]) + (1-\alpha)\cdot f_s$$

其中 $\alpha = \sigma(\mathrm{MLP}_{obj}(p_{4D}))$，由 4D 坐标嵌入经 MLP 和 sigmoid 激活学习得到。该门控机制使模型能自适应调整融合权重，在保留空间外观信息的同时注入运动感知能力。Table 6 的消融实验证实，基于注意力的融合策略在 CIDEr、BLEU-4、SAcc@0.5、TAcc 上均显著优于简单拼接和加权融合。

### 坐标对齐语言嵌入

融合后的视觉时空特征 $f_{st}$ 通过 MLP 投影为语言空间的视觉 token $\tau_v^{st}$。同时，对文本指令中描述的位置 $tp$ 和时间 $tt$ 应用相同的时空编码，融入语言 token：

$$\tau_s = \mathrm{PE}(tp), \quad \tau_t = \mathrm{TE}(tt)$$

这种坐标对齐设计减少了 LLM 对时空坐标的误解，Table 7 的消融表明，对文本坐标进行编码相比仅使用原始坐标文本，在所有指标上均有提升。

### 模块协同的因果链条

Table 4 的逐模块消融清晰揭示了三个组件的因果贡献：从无任何模块的基线（CIDEr 62.3 / BLEU-4 11.7 / SAcc@0.5 34.8 / TAcc 12.7），逐步添加坐标嵌入、特征解耦和特征融合后，各项指标跃升至 93.5 / 17.2 / 58.9 / 54.6。其中，坐标嵌入是拉动整体性能的关键杠杆，特征解耦提升了性能上限，而特征融合进一步增强了时空理解能力。Table 5 进一步表明，完整的 4D 坐标编码（3D 位置 + 1D 时间）在所有指标上均优于仅使用 3D 位置或仅使用 1D 时间的编码方案，验证了时空联合建模的必要性。

## 实验与分析

### 主实验结果

LLaVA-4D在3D与4D场景理解任务上均展现出显著优势。在3D基准上，LLaVA-4D在Scan2Cap、ScanQA、Multi3DRefer和ScanRef四个数据集上取得了最优或接近最优的性能（Table 1）。具体而言，在Scan2Cap上CIDEr@0.5达到85.3，ScanQA上CIDEr达到97.8，均优于Video-3D LLM（Zheng et al., arXiv 2024）和LLaVA-3D（Zhu et al., arXiv 2024）等基线方法。在VSI-Bench空间智能基准上，LLaVA-4D以48.6的平均准确率超越了此前最强的Spatial-MLLM（Wu et al., arXiv 2025）的48.4，尤其在物体计数（68.2）、物体尺寸（64.8）和房间尺寸（49.6）等数值型子任务上表现突出（Table 2）。

![[assets/figures/papers/paper_list_l19_https_openreview_net_forum_id_URpbmVEsqB/figures/007_Table_1.jpg]]
*Table 1: Quantitative results of LMMs for scene understanding tasks on different 3D and 4D datasets*

在4D场景理解的核心基准Chat4D上，LLaVA-4D取得了CIDEr 93.5、BLEU-4 17.2、空间准确率SAcc@0.5 58.9、时间准确率TAcc 54.6的全面领先成绩（Table 1）。时间理解专项对比（Table 3）进一步表明，LLaVA-4D在SAcc@0.5、TAcc和tIoU@0.5三项指标上均大幅超越Grounded-VideoLLM和LLaVA-ST等时序理解基线，验证了4D时空提示对动态场景建模的关键作用。

定性对比（Figure 5）展示了LLaVA-4D在多视角动态场景下的理解优势。面对“骑手在马背上跳跃”的4D场景查询，LLaVA-3D因缺乏时间建模而无法感知运动，Video-3D LLM虽有时序处理能力但空间定位模糊，而LLaVA-4D能够准确描述骑手的空间位置变化和时间节点。

### 消融实验

#### 视觉表示模块的逐模块贡献

Table 4展示了逐步添加坐标嵌入、特征解耦和特征融合三个模块的效果。基线模型（无任何模块）在Chat4D上的CIDEr仅为62.3，SAcc@0.5为34.8，TAcc低至12.7。单独加入4D坐标嵌入后，CIDEr跃升至87.5，TAcc大幅提升至46.3，表明时空坐标信息是理解动态场景的核心驱动力。进一步加入特征解耦后，CIDEr提升至90.8，SAcc@0.5从49.2升至56.6，验证了空间-时间特征分离对空间定位能力的增强。最终加入交叉注意力融合后，全模块配置达到最优：CIDEr 93.5、BLEU-4 17.2、SAcc@0.5 58.9、TAcc 54.6。

![[assets/figures/papers/paper_list_l19_https_openreview_net_forum_id_URpbmVEsqB/figures/012_Table_4.jpg]]
*Table 4: Effect of visual representation modules*

#### 坐标编码策略的对比

Table 5系统比较了不同坐标编码方案。无编码条件下CIDEr仅87.5，仅使用3D位置编码时CIDEr为89.1、TAcc为37.2，仅使用1D时间编码时CIDEr为88.3、SAcc@0.5为51.4。完整的4D坐标编码（3D位置+1D时间+光流调制）在所有指标上均取得最优性能，特别是TAcc达到54.6，相比仅3D编码提升17.4点，相比仅1D编码提升11.3点。这一结果表明，空间位置和时间信息对4D场景理解具有互补性，缺一不可。

![[assets/figures/papers/paper_list_l19_https_openreview_net_forum_id_URpbmVEsqB/figures/013_Table_5.jpg]]
*Table 5: Role of coordinate encoding*

#### 时空融合策略的选择

Table 6对比了三种特征融合策略。简单拼接（Concatenation）在CIDEr上为90.8，加权融合（Weighting）提升至92.1，而基于交叉注意力的融合（Attention）达到最优的93.5。注意力机制的优势在于以4D坐标嵌入为查询，能够自适应地选择与当前时空位置最相关的视觉特征，并通过门控参数 $\alpha$ 动态平衡融合特征与原空间特征，避免了静态融合策略对动态场景的适应性不足。

![[assets/figures/papers/paper_list_l19_https_openreview_net_forum_id_URpbmVEsqB/figures/014_Table_6.jpg]]
*Table 6: Discussion on spatiotemporal fusion*

#### 文本坐标编码的影响

Table 7显示，对文本指令中的位置和时间标签应用与视觉侧相同的时空编码（Coordinate w/ Encoding），相比直接使用原始坐标文本（Coordinate w/o Encoding），在CIDEr上从91.8提升至93.5，TAcc从51.3提升至54.6。这表明统一的坐标表示空间能够减少LLM对时空坐标的误解，使语言侧和视觉侧的时空信息在语义层面上对齐。

#### 时间编码策略：帧率 vs. 运动速度

Table 9比较了基于帧率（Frame rate-based）和基于运动速度（Motion speed-based）两种时间编码策略。基于运动速度的编码在所有指标上均优于帧率编码，其中TAcc的提升最为显著（54.6 vs. 49.5，+5.1点），CIDEr也从91.0提升至93.5。运动速度编码是一种局部自适应的编码方案，能够直接反映场景中物体的实际运动幅度，而非均匀的时间间隔，因此对物理动态的刻画更为精确。

#### 标注噪声鲁棒性

Table 8验证了模型对时空标注噪声的鲁棒性。在使用经扰动标注（模拟真实场景中的定位误差）微调后，CIDEr仅从93.5降至93.0，SAcc@0.5从58.9降至58.2，各项指标下降均小于1个点。这表明LLaVA-4D通过时空解耦和注意力融合机制，对轻度的标注误差具有较好的容忍度，具备一定的实际部署潜力。

### 特征可视化分析

Figure 3展示了时空解耦前后的特征分布对比。在原始视觉特征空间中，动态物体的特征点分散在背景特征簇之间，难以区分。经过时空解耦后，空间特征 $f_s$ 和时间特征 $f_t$ 形成了清晰的判别边界：背景和物体各自聚集成簇，且簇间距离增大。Figure 6进一步展示了模块叠加过程中的特征演变——仅加入特征解耦时，物体与背景的分离度已有改善；再加入4D坐标嵌入后，两者在特征空间中被进一步拉开，为LLM的准确理解提供了更具判别力的视觉表示。

![[assets/figures/papers/paper_list_l19_https_openreview_net_forum_id_URpbmVEsqB/figures/003_Figure_3.jpg]]
*Figure 3: Feature distribution of static background and dynamic object in a 4D dynamic scene. Visual features of dynamic objects appear scattered while static backgrounds are clustered. In contrast, spatiotemporal features show clear discrimination between objects and background*

### 失败模式与局限性

尽管LLaVA-4D在多项基准上表现优异，其性能仍受限于以下因素：

1. **外部预处理依赖**：4D坐标的构建依赖SfM进行相机姿态估计和MVS进行深度计算，这一预处理管线不仅增加了计算开销，还可能引入累积误差。当场景纹理稀疏或存在运动模糊时，深度估计和光流计算的质量下降，会直接影响时间编码的准确性。

2. **光流质量敏感性**：时间编码中的光流调制项 $\beta$ 对运动速度敏感。在极快运动（如高速旋转）或极慢运动（如缓慢漂移）场景下，光流的数值范围可能导致时间编码的动态范围不足或过饱和，削弱运动信息的表达能力。

3. **长时程动态理解未验证**：Chat4D数据集中的视频片段主要为6-12秒，模型在更长时程（数十秒以上）的持续性动态理解上的能力尚待验证。对于需要长程因果推理的场景（如“物体A在30秒前被移动到了哪里”），当前框架可能面临上下文窗口和记忆机制的瓶颈。

4. **多视角输入要求**：方法需要多视角视频作为输入，限制了其在单视角视频或静态图像场景下的直接应用。对于仅有一个固定摄像头的监控场景，4D坐标的构建将退化为不完整的空间信息。

## 方法谱系与知识库定位

### 1. 方法谱系：从3D LMM到4D LMM的关键跃迁

LLaVA-4D并非孤立出现，而是站在两条技术路线的交汇点上：一是以3D位置提示为核心的3D大语言多模态模型（3D LMMs），二是具备时空信息处理能力的视频理解LMM。

**与3D LMMs的关系。** 现有3D LMMs的代表性工作包括 **LLaVA-3D**（Zhu et al., arXiv 2024）和 **Spatial-MLLM**（Wu et al., arXiv 2025）。这些方法的核心设计是将3D坐标（x, y, z）编码为空间提示，使LLM能够感知场景的几何结构。然而，这一范式的根本局限在于：它将所有视觉特征统一为空间表示，不区分静态背景与动态物体。当场景中存在运动物体时，同一空间位置在不同时刻可能对应不同语义，而3D LMMs无法捕捉这种时间维度的变化——这正是LLaVA-4D所瞄准的核心瓶颈。

LLaVA-4D的解决方案是将提示从3D空间扩展为4D时空（x, y, z, t），并引入三个关键设计来填补3D LMMs的能力缺口：动态感知的4D坐标编码、时空解耦的视觉嵌入、以及基于交叉注意力的特征融合。在VSI-Bench上，LLaVA-4D以48.6的平均准确率略优于Spatial-MLLM的48.4（Table 2），但在专门设计的4D基准Chat4D上，其CIDEr达到93.5、TAcc达到54.6，而3D基线因缺乏时间建模能力在这些指标上表现严重不足。

**与视频理解LMMs的关系。** 在时间理解维度上，LLaVA-4D与 **Video-3D LLM**（Zheng et al., arXiv 2024）、**Grounded-VideoLLM** 和 **LLaVA-ST** 形成对比。Video-3D LLM已具备时空信息处理能力，可作为3D场景理解的基线；Grounded-VideoLLM和LLaVA-ST则分别侧重于时间理解和细粒度时空理解。LLaVA-4D在时间理解指标上显著超越这些基线：其SAcc@0.5达到58.9，TAcc达到54.6，tIoU@0.5亦有大幅领先（Table 3）。这一优势来源于其独特的设计——将光流作为运动辅助信息融入时间编码（Eq. 6），使模型能够直接感知运动幅度而非仅依赖帧率索引。

**方法谱系中的定位。** LLaVA-4D可被视为3D LMM与视频LMM之间的“桥梁方法”：它继承了3D LMM的坐标提示思想，但将其从静态空间扩展为动态时空；同时借鉴了视频理解中的时序建模思路，但将其与显式的4D坐标对齐，而非仅依赖隐式的视觉特征学习。这种“坐标显式化+特征解耦”的组合策略，使其在4D场景理解这一新兴任务上建立了新的基准。

### 2. 适用边界与条件约束

LLaVA-4D的性能优势建立在若干前提条件之上，这些条件同时定义了其适用边界。

**数据层面的约束。** 模型需要多视角视频输入来构建4D坐标张量。具体而言，其依赖SfM（Structure from Motion）进行相机姿态估计，以及MVS（Multi-View Stereo）进行深度计算，从而将2D像素反投影到世界坐标系（Eq. 4）。这意味着LLaVA-4D难以直接应用于单视角视频或静态图像，对数据采集条件要求较高。此外，构建的Chat4D数据集主要来自6-12秒的短视频片段，模型在更长时程（数十秒以上）的持续性动态理解上的能力尚待验证。

**计算管线的依赖。** 模型需要预计算光流作为时间编码的辅助输入。消融实验表明，基于运动速度的编码策略（Motion speed-based）在所有指标上均优于基于帧率的策略（Frame rate-based），其中TAcc提升达5.1点（Table 9）。这一结果验证了运动信息的关键作用，但也意味着模型对光流质量和场景运动速度存在敏感性——在运动模糊严重或光流估计误差较大的场景下，性能可能退化。

**模型规模的限制。** 当前实验仅使用了7B规模的LLM（基于LLaVA-1.5-7B和CLIP-ViT-L-336px），未探索更大模型容量对4D场景理解的影响。考虑到LLM的规模定律，更大模型可能带来进一步的能力提升，但相应的计算成本也会显著增加。

### 3. 局限性与失败模式分析

**外部模块依赖与误差累积。** LLaVA-4D的预处理管线依赖外部SfM模块进行相机姿态估计和深度计算。这一设计增加了预处理时间，且SfM本身可能引入累积误差——姿态估计的偏差会通过反投影传播到4D坐标构建，进而影响时空提示的质量。这阻碍了端到端训练的可能性，使得整个系统在面对大规模数据时效率受限。

**标注噪声的鲁棒性边界。** 消融实验显示，模型对轻度的时空标注噪声具有一定鲁棒性：在经扰动标注微调后，各指标下降均小于1个点（如CIDEr从93.5降至93.0，Table 8）。然而，这一实验仅测试了轻度噪声场景，对于更严重的标注错误（如大幅位置偏移或时间戳错位），模型的鲁棒性极限尚不明确。

**动态场景的覆盖范围。** Chat4D数据集主要覆盖6-12秒的短视频，这意味着模型对于快速运动、长时间遮挡、或复杂多物体交互场景的泛化能力缺乏充分验证。此外，模型在真实世界含噪声、遮挡或相机抖动的场景下的表现，仍有待进一步评估。

### 4. 开放问题与未来方向

**端到端几何估计的替代方案。** 一个直接且重要的开放问题是如何用端到端的单目几何估计模型（如MonST3R）替代外部SfM预处理。这不仅能提升整体效率，还能减少模块间的误差传递，使整个系统更易于扩展和部署。

**多模态时空提示的扩展。** 当前时空提示仅包含位置和时间信息。一个自然的问题是：能否进一步引入音频、语义知识或动作标签，以增强对复杂动态事件的综合理解？Figure 7展示了时空提示向语义和动作掩码任务扩展的可视化，暗示了这一方向的可行性，但具体的性能增益和设计空间尚待探索。

**长程动态理解与因果推理。** 对于超过30秒的视频流，现有的6-12秒训练数据是否足够？模型的长程记忆和因果推理能力应如何增强？这可能需要新的训练数据构建策略（如合成更长时序的4D场景）或架构改进（如引入记忆模块）。

**具身AI场景的迁移。** 能否将LLaVA-4D的4D时空提示框架推广到机器人导航与操作等具身AI任务中？在这些场景下，LMM需要理解动态物理交互（如物体被推动后的运动轨迹），LLaVA-4D的坐标-特征解耦设计可能为此提供基础，但需要针对具体任务的适配和验证。

**更大规模模型的潜力。** 当前仅使用7B LLM的实验结果已展现出显著优势，更大规模模型（如13B、34B乃至更大）是否能带来非线性提升？这涉及到4D场景理解的“涌现能力”问题，值得进一步探索。

## 原文 PDF

![[paperPDFs/ICLR_2026/LLaVA_4D_Embedding_SpatioTemporal_Prompt_into_LMMs_for_4D_Scene_Understanding.pdf]]
