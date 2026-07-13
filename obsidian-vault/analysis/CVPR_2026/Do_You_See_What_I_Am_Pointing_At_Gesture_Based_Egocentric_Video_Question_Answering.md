---
title: Do You See What I Am Pointing At? Gesture-Based Egocentric Video Question Answering
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Do_You_See_What_I_Am_Pointing_At_Gesture_Based_Egocentric_Video_Question_Answering.pdf
project_link: "https://yuuraa.github.io/papers/choi2026egovqa"
code_link: null
aliases:
- HITH
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 引入Hand Intent Token (HINT)流，作为模型的额外输入，提供帧对齐的3D手部关键点信息，显式地编码指向意图。
primary_logic: 通过现成的3D手部重建模型（WiLoR）提取每帧21个3D关键点，再用一个轻量级MLP适配器将其投影为单个手势意图令牌，将该令牌与视觉令牌交错输入LLM，使其在回答问题时能利用时空手势上下文来消除歧义。
claims:
- HINT InternVL3-14B在EGOPOINTVQA 6个任务上的平均准确率达到68.1%，比最强基线InternVL3-14B的62.7%提高5.4个百分点。
- 仅使用EGOPOINTVQA进行监督微调（SFT）只能将Reference准确率从66.1%提升到68.5%，而加入手部意图令牌（HINT）后提升至75.0%，表明显式手势架构是必需的。
- 移除视频中的手部手势导致性能急剧下降（Reference从75.0%降至41.7%），证明指向手势是任务的关键信息来源。
- 人类在该数据集上的平均准确率达到95.9%，表明问题清晰可解，但当前最佳模型仍有较大差距。
---

# Do You See What I Am Pointing At? Gesture-Based Egocentric Video Question Answering

> [!tip] 核心洞察
> 通过现成的3D手部重建模型（WiLoR）提取每帧21个3D关键点，再用一个轻量级MLP适配器将其投影为单个手势意图令牌，将该令牌与视觉令牌交错输入LLM，使其在回答问题时能利用时空手势上下文来消除歧义。

| 字段 | 内容 |
|------|------|
| 中文题名 | 你看到我指的是什么了吗？基于手势的自我中心视频问答 |
| 英文题名 | Do You See What I Am Pointing At? Gesture-Based Egocentric Video Question Answering |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.12533) · [Project](https://yuuraa.github.io/papers/choi2026egovqa) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Hand Intent Tokens (HINT) |
| Dataset | EGOPOINTVQA |

> [!tip] 效果简介
> - EGOPOINTVQA 上，Average Accuracy over 6 tasks (%) 68.1 vs 62.7 (InternVL3-14B) (+5.4)。
> - EGOPOINTVQA (Reference task) 上，Accuracy (%) 73.8 vs 63.1 (InternVL3-14B) (+10.7)。
> - EGOPOINTVQA (Reference task, 8B backbone) 上，Accuracy (%) 75.0 vs 66.1 (InternVL3-8B) (+8.9)。

## 概要

**问题瓶颈**：现有MLLM在训练数据中缺乏丰富的指示手势视频，且架构未显式编码手势信息，导致无法理解指向手势并解析指示代词引用（如“this one”）。在EGOPOINTVQA上，最强基线InternVL3-14B平均准确率仅62.7%，而人类可达95.9%，差距显著。

**核心思路**：提出Hand Intent Tokens（HINT），通过现成的3D手部重建模型WiLoR提取每帧21个3D关键点，经轻量级MLP适配器投影为单个手势意图令牌，与视觉令牌交错输入LLM，使模型在回答问题时能利用时空手势上下文消除歧义。

**方法定位**：HINT是一种即插即用的输入增强策略，不改变LLM主体架构，仅新增关键点适配器与令牌交错机制，可适配多种开源MLLM骨干（InternVL3-8B/14B等）。

**主要结果**：
- HINT InternVL3-14B在EGOPOINTVQA六个任务上平均准确率达**68.1%**，较InternVL3-14B（62.7%）提升**5.4个百分点**（Table 1）。
- 在核心Reference任务上，HINT InternVL3-8B达**75.0%**，较基线（66.1%）提升**8.9个百分点**；HINT InternVL3-14B达73.8%（基线63.1%，+10.7）（Table 1）。
- 消融证实：仅SFT只能将Reference从66.1%提至68.5%，加入HINT后跃升至75.0%，表明显式手势架构是必需的（Table 2）；移除视频中的手部手势后性能从75.0%骤降至41.7%，证实指向手势是关键信号（Table 10）。

**关键局限**：HINT依赖WiLoR的关键点估计，在运动模糊、遮挡或手部不可见时可靠性下降；快速视角移动可导致目标跟踪失败；合成数据与真实场景间仍存领域差距。



### 自我中心视频理解中的指示性瓶颈

自我中心视频理解是具身智能与增强现实的核心技术支柱。随着**Meta Ray-Ban**等AI眼镜的普及，用户期望设备能像人类同伴一样，理解“这个”“那个”等指示代词所指代的具体物体。然而，当前最先进的多模态大语言模型（MLLM）在这一场景下暴露出系统性缺陷：如**Figure 1**所示，即使是**GPT-4o**和**Qwen3-VL-32B**这样的旗舰模型，在面对“这两个锅是什么颜色？”的简单问题时，仍会错误地回答颜色不同，而实际上两个锅都是黑色的。模型未能利用视频中的指向手势来消解“这两个”的指代歧义。

这一失败并非偶然，其**核心瓶颈**在于两个层面：其一，现有MLLM的训练数据中缺乏丰富的指示手势视频数据，模型从未学习过手势与物体之间的指代关联；其二，主流MLLM架构未设计显式编码手势信息的通路，视觉编码器将手部区域与背景物体无差别地压缩为视觉令牌，导致指向意图在特征提取过程中被淹没。当问题中出现“this one”等指示代词时，模型只能依赖视觉显著性等不可靠的启发式线索进行猜测，而非真正解析手势语义。

### 任务定义：基于手势的自我中心视频问答

为系统性地衡量和推动这一能力的进步，本文提出了**EGOPOINTVQA**基准数据集，将基于手势的指示性问答形式化为六类子任务（**Figure 2**）：

- **Reference（指代识别）**：识别手指指向的物体是什么。
- **Counting（计数）**：统计与指向物体同类的物体数量。
- **Spatial（空间推理）**：判断指向物体的空间位置或相对深度关系。
- **Temporal（时序推理）**：追踪多次手势的先后顺序。
- **Attribute（属性判断）**：回答指向物体的属性（颜色、材质等）。
- **Feedback（功能反馈）**：判断指向物体能否实现特定功能。

所有问题均包含指示性代词，必须通过视觉接地指向手势才能正确回答。数据集包含4,000段合成视频和400段真实世界视频，涵盖室内外多种场景，确保模型必须真正理解手势语义，而非依赖语言偏见——通过盲测（仅问题文本）和仅选项测试已确认数据集无语言捷径可走。

### 现有方法缺口与本文动机

在基线对比中（**Table 1**），最强的开源模型**InternVL3-14B**在EGOPOINTVQA六个任务上的平均准确率仅为62.7%，而人类表现高达95.9%，两者之间存在超过33个百分点的巨大差距。这一差距表明，仅靠扩大模型规模或增加通用视频训练数据，无法弥合手势理解这一专项能力的缺失。

现有的一些自我中心视频理解专用模型（如**EgoGPT**）或视觉指令特化模型（如**ViSpeak**）同样未针对手势语义进行设计，它们或聚焦于第三人称视角的动作识别，或将手部区域仅作为一般视觉特征处理。**VGLLM-QA**等3D几何理解模型虽能处理空间关系，但缺乏对指向意图的显式建模。

本文的核心动机由此明确：**在现有MLLM架构中引入一条轻量级的手势意图编码通路，以极小的计算开销赋予模型解析指向手势的能力**。这一思路不要求重新训练庞大的视觉编码器或语言模型，而是通过一个即插即用的适配器模块，将现成的3D手部关键点估计结果转化为模型可理解的手势令牌，从而实现手势语义与视觉语义的协同推理。



## 核心方法与创新机理

### 问题瓶颈：MLLM 缺乏手势理解能力

现有通用多模态大模型（MLLM）在自我中心视频问答中面临一个根本性瓶颈：**训练数据中缺乏丰富的指示手势视频，且模型架构未设计显式的手势编码机制**。当用户用手指向物体并说“这个”（this one）时，模型无法解析指示代词的指代对象。Figure 1 展示了这一失败模式——即便是 GPT-4o 和 Qwen3-VL-32B 等最先进的模型，在面对指向手势时也会错误地判断被指物体的属性。

这一瓶颈的因果机制在于：传统 MLLM 仅依赖视觉编码器提取的 RGB 特征，而指向手势所蕴含的空间意图信号（手指方向、指尖位置、手部运动轨迹）无法从通用视觉特征中被有效解耦和利用。

### 核心洞察：显式编码 3D 手部关键点作为手势意图令牌

本文的核心洞察是：**通过现成的 3D 手部重建模型提取每帧的 21 个 3D 关键点，再用一个轻量级 MLP 适配器将其投影为单个“手势意图令牌”（Hand Intent Token, HINT），并将该令牌与视觉令牌交错输入 LLM**。这样，模型在回答问题时能够利用时空手势上下文来消除指示代词的歧义。

这一设计的关键在于“显式”——不是让模型从像素中隐式学习手势，而是将几何信息作为独立的模态流馈入模型，使手势意图成为一个可学习、可操控的因果旋钮。

### Changed Slot：从“无手势令牌”到“帧对齐 HINT 流”

相对于基线方法，HINT 的核心改动只有一个 **changed slot**：

| 组件 | 基线值 | HINT 值 | 证据锚点 |
|------|--------|---------|----------|
| 模型输入序列中的手势令牌 | 无手势令牌，仅视觉令牌 + 文本 | 每帧（当检测置信度 $c_t \geq \tau$）添加一个 HINT 令牌 $H_t$，与视觉令牌交错 | Sections 4.2, 4.3, Figure 6 |

这一改动的实现分为三个流水线模块：

1. **3D 手部姿势估计（WiLoR）**：从每帧 $I_t$ 提取 21 个 3D 手部关键点 $K_t \in \mathbb{R}^{21 \times 3}$，同时输出检测置信度 $c_t$。

2. **关键点适配器（Keypoint Adapter）**：将关键点展平为 63 维向量 $\tilde{k}_t = \mathrm{flatten}(K_t) \in \mathbb{R}^{63}$，通过一个两层 MLP 生成手势意图令牌：
   $$H_t = \begin{cases} W_2 \sigma(W_1 LN(\tilde{k}_t)), & \text{if } c_t \geq \tau \\ \varnothing, & \text{otherwise} \end{cases}$$
   其中 $\sigma$ 为激活函数，$LN$ 为 Layer Normalization，$\tau = 0.5$ 为置信度阈值。

3. **帧-关键点交错（Interleaving）**：将 $H_t$ 插入 LLM 输入序列，与视觉令牌 $V_t$ 交替排列，仅在 $c_t \geq \tau$ 时插入。HINT 令牌占 LLM 总输入令牌的不到 1%，计算开销极小。

### 创新点的决定性证据

消融实验（Table 2）提供了因果证据：仅使用 EGOPOINTVQA 进行监督微调（SFT）只能将 Reference 准确率从 66.1% 提升到 68.5%，而加入 HINT 后提升至 **75.0%**（+8.9 pp）。这表明，**显式的手势架构是必需的，而非单纯的数据增强所能替代**。

进一步，Table 10 的“移除手部”实验显示，当视频中的手部手势被移除后，Reference 准确率从 75.0% 骤降至 41.7%，证明**指向手势是任务的关键信息来源**，而非模型通过其他视觉线索绕过的冗余信号。

### 与替代方案的对比

Table 4 比较了多种手势编码方式：视觉提示（在帧上画箭头）、文本输入坐标、以及 HINT 的学习关键点适配器。结果显示，**学习关键点适配器以 75.0% 的 Reference 准确率显著优于所有替代方案**，说明让模型自主学习如何处理几何手部信息，比通过视觉或文本形式提供更为有效。

### 方法局限

HINT 的性能受限于 WiLoR 的 3D 手部关键点估计质量。在运动模糊、遮挡或手部不在视野内时，关键点不可靠，导致手势令牌缺失或编码错误。快速视角移动也可能导致目标物体跟踪失败。此外，方法目前仅利用单手关键点信息，未显式建模物体边界框或分割，可能限制了更精确的指向意图解析。



HINT 的整体设计遵循**双流并行处理、序列交错融合**的范式，旨在以极低的令牌开销为现有多模态大语言模型（MLLM）注入显式的指向手势理解能力。其核心思想是：不从零训练一个专用模型，而是在冻结的视觉编码器和语言模型之间，插入一条轻量级的手势意图通路，将每帧的 3D 手部关键点转化为单个“手势意图令牌”（Hand Intent Token），并与视觉令牌交错排列，使 LLM 在自回归解码时能够同时关注视觉外观与手势的时空动态。

### 1. 双流输入架构

对于一段包含 $T$ 帧的视频，HINT 同时构建两条令牌序列：

- **视觉流（Visual Stream）**：由标准的视觉编码器（Vision Encoder）和投影器（Projector）将每帧 $I_t$ 映射为一组视觉令牌 $V_t$。该流完全复用基线 MLLM（如 InternVL3、LLaVA-OneVision）的原有组件，不引入额外参数。
- **手势意图流（Hand Intent Stream）**：由现成的 3D 手部重建模型 WiLoR 从每帧 $I_t$ 中提取 21 个 3D 关键点 $K_t \in \mathbb{R}^{21 \times 3}$，再通过一个轻量级**关键点适配器**（Keypoint Adapter）将关键点编码为单个手势意图令牌 $H_t$。

两条流在帧级别保持严格对齐，形成 $\{V_t, H_t\}_{t=1}^T$ 的配对结构。

### 2. 关键点适配器：从 63 维向量到单个令牌

关键点适配器是 HINT 中唯一需要训练的新模块。其计算过程分两步：

**第一步：关键点扁平化。** 将每帧的 21 个 3D 关键点展平为 63 维向量：
$$\tilde{k}_t = \mathrm{flatten}(K_t) \in \mathbb{R}^{63}$$

**第二步：条件令牌生成。** 通过一个两层 MLP（含 LayerNorm 和 GELU 激活）将扁平向量投影为手势意图令牌，同时以手部检测置信度 $c_t$ 作为门控条件：
$$H_t = \begin{cases} W_2 \, \sigma(W_1 \, \mathrm{LN}(\tilde{k}_t)), & \text{if } c_t \geq \tau \\ \varnothing, & \text{otherwise} \end{cases}$$

其中 $\tau = 0.5$ 为检测置信度阈值。当 WiLoR 对手部检测的置信度低于阈值时（如手部被遮挡、运动模糊严重或不在视野内），该帧不生成 $H_t$，避免噪声令牌误导模型。这一门控机制使 HINT 在计算开销上极为高效——在 $\tau=0.5$ 的设置下，HINT 令牌仅占输入 LLM 总令牌数的不到 1%。

### 3. 帧-关键点交错与答案生成

HINT 将视觉令牌与手势意图令牌按帧交错排列，构建 LLM 的完整输入序列：
$$[V_1, H_1, V_2, H_2, \dots, V_T, H_T]$$

在此序列前拼接系统提示词和问题文本 $X_{\mathfrak{q}}$，LLM 以自回归方式逐词生成答案 $X_{\mathfrak{a}}$，其概率建模为：
$$p(X_{\mathfrak{a}} \mid V, X_{\mathfrak{q}}, H) = \prod_{i=1}^{L} p(x_i \mid V, X_{\mathfrak{q},<i}, X_{\mathfrak{a},<i}, H_{<i})$$

交错排列的设计使 LLM 在处理每一帧的视觉信息时，能同步获取该帧的手势空间信息，从而在需要消解指示代词（如“this one”“that object”）时，利用手势的指向方向和时序动态来定位目标物体。这与仅依赖视觉令牌的基线模型形成鲜明对比——后者缺乏对手势信息的显式编码，导致在 Figure 1 所示的失败案例中，即便看到了手部动作，也无法将其解析为指向意图。

### 4. 模块关系与数据流总结

整体数据流可概括为以下四步闭环：

| 步骤 | 模块 | 输入 | 输出 |
|------|------|------|------|
| ① 视觉编码 | Vision Encoder + Projector | 视频帧 $I_t$ | 视觉令牌 $V_t$ |
| ② 手势估计 | WiLoR | 视频帧 $I_t$ | 21×3 关键点 $K_t$ + 置信度 $c_t$ |
| ③ 意图编码 | Keypoint Adapter (MLP) | $\tilde{k}_t$, $c_t$ | 手势意图令牌 $H_t$（或 $\varnothing$） |
| ④ 序列融合 | LLM 输入层 | $\{V_t, H_t\}_{t=1}^T$, $X_{\mathfrak{q}}$ | 答案 $X_{\mathfrak{a}}$ |

其中，仅步骤③的关键点适配器需要训练，其余模块（视觉编码器、WiLoR、LLM）均保持冻结或作为现成工具使用。这种“插件式”设计使 HINT 可以无缝适配多种 MLLM 骨架——论文在 LLaVA-OneVision-7B、InternVL3-8B 和 InternVL3-14B 三个不同规模的模型上验证了其有效性，均取得一致且显著的性能提升。

### 补充图表

![[assets/figures/papers/paper_list_l1059_https_arxiv_org_abs_2603_12533/figures/006_Figure_6.jpg]]
*Figure 6: HINT overall architecture. HINT uses an additional adapter to model the 3D location and movement of the hand directly*



HINT 的整体架构（Figure 6）由两条并行流组成：标准视觉流和新增的手势意图流。视觉流沿用现有 MLLM 的视觉编码器与投影器，从均匀采样的 32 帧视频中提取视觉令牌 $V_t$。手势意图流是 HINT 的核心创新，包含三个关键模块。

**3D 手部姿势估计**。对于每一帧 $I_t$，使用现成的 3D 手部重建模型 **WiLoR** 提取 21 个 3D 手部关键点 $K_t \in \mathbb{R}^{21 \times 3}$，同时输出一个检测置信度 $c_t$。WiLoR 的鲁棒性直接决定了手势令牌的可用性——当手部被遮挡、运动模糊或不在视野内时，$c_t$ 会降低，导致后续令牌缺失。

**关键点适配器（Keypoint Adapter）**。这是一个轻量级的两层 MLP，负责将 21 个 3D 关键点压缩为单个手势意图令牌。首先将关键点展平为 63 维向量：

$$\tilde{k}_t = \mathrm{flatten}(K_t) \in \mathbb{R}^{63}$$

然后将展平后的向量通过带 LayerNorm 和 ReLU 激活的两层 MLP，仅在检测置信度 $c_t$ 超过阈值 $\tau$ 时生成手势令牌 $H_t$：

$$H_t = \begin{cases} W_2 \, \sigma(W_1 \, \mathrm{LN}(\tilde{k}_t)), & \text{if } c_t \geq \tau \\ \varnothing, & \text{otherwise} \end{cases}$$

其中 $W_1$ 和 $W_2$ 是可学习的投影矩阵，$\sigma$ 为 ReLU 激活函数。当 $c_t < \tau$ 时，该帧不产生手势令牌，避免噪声关键点污染模型输入。消融实验（Table 5）表明 $\tau = 0.5$ 实现了滤噪与保留有效手势之间的最佳平衡。

**帧-关键点交错（Interleaving）**。生成的 $H_t$ 令牌被插入 LLM 的输入序列中，与对应帧的视觉令牌 $V_t$ 交替排列。这一设计使 LLM 在逐帧处理视频时能同时获取视觉外观和手部空间位置信息，从而在生成答案时利用时空手势上下文消除指示代词的歧义。最终答案的逐词生成概率为：

$$p(X_{\mathfrak{a}} \mid V, X_{\mathfrak{q}}, H) = \prod_{i=1}^{L} p(x_i \mid V, X_{\mathfrak{q},<i}, X_{\mathfrak{a},<i}, H_{<i})$$

其中 $V$ 为视觉令牌序列，$X_{\mathfrak{q}}$ 为问题文本，$H$ 为手势令牌序列，$X_{\mathfrak{a}}$ 为生成的答案。值得注意的是，当 $\tau = 0.5$ 时，HINT 令牌仅占送入 LLM 总令牌数的不到 1%，计算开销极小。

**关键设计选择**。消融实验（Table 4）对比了多种手势意图编码方式：学习型关键点适配器在 Reference 任务上达到 75.0%，显著优于视觉提示（如画箭头）和文本输入坐标等替代方案。这表明让模型自主学习如何处理几何手势信息，比通过视觉或文本通道间接提供更为有效。

### 补充图表

![[assets/figures/papers/paper_list_l1059_https_arxiv_org_abs_2603_12533/figures/001_Figure_1.jpg]]
*Figure 1: Illustration of EGOPOINTVQA. Left: EGOPOINTVQA includes questions with deictic pronouns requiring gesture understanding, either identifying single pointed objects (top) or tracking multiple references across frames (bottom). Right: State-of-the-art models, including GPT-4o [20] and Qwen3-VL-32B [37], fail to resolve the question with pointing gestures, incorrectly stating the two pots have different colors despite both being black. Zoomed circles highlight the pointed objects*

![[assets/figures/papers/paper_list_l1059_https_arxiv_org_abs_2603_12533/figures/002_Figure_2.jpg]]
*Figure 2: Task taxonomy and examples from EGOPOINTVQA. EGOPOINTVQA includes six subsets of questions regarding the properties of a pointed object. Each example shows egocentric video frames and a question using deictic references. Tasks include reference (object identification), counting (number of same objects), spatial (location and relative depth), temporal (order of multiple gestures), attribute (object properties), and feedback (object function). All questions require resolving deictic references through visual grounding of pointing gestures. The pointed objects are highlighted with red circles for visualization purposes*



## 实验与关键发现

### 主实验结果

为评估模型在基于手势的自我中心视频问答上的能力，作者在EGOPOINTVQA真实世界测试集（300个视频，672道多选题）上对一系列MLLM进行了基准测试。所有视频模型统一采样32帧作为输入，以保证公平对比。

**Table 1**（见文末附表）给出了各模型在六个子任务上的多项选择准确率。核心发现如下：

* **通用MLLM普遍失效**：GPT-4o、Qwen3-VL-32B等强基线在Reference任务上仅达63–66%，表明现有模型缺乏对指向手势的显式理解能力。专有模型（GPT-5等）虽整体较强，但在需要精确手势解析的任务上同样表现不佳。
* **HINT带来一致且显著的提升**：HINT InternVL3-14B在6个任务上的平均准确率达到**68.1%**，比最强基线InternVL3-14B（62.7%）提高**+5.4个百分点**。在核心的Reference任务上，HINT InternVL3-14B达到**73.8%**（基线63.1%，**+10.7pp**）；HINT InternVL3-8B更达到**75.0%**（基线66.1%，**+8.9pp**）。
* **跨骨干泛化**：HINT在LLaVA-OneVision-7B、InternVL3-8B、InternVL3-14B三个不同骨干上均取得一致提升，验证了方法的通用性。
* **人类上限**：5名人类参与者在全部672题上的平均准确率达**95.9%**（Table 9），表明问题清晰可解，当前最佳模型仍有约27个百分点的显著差距。

### 消融实验

作者通过一系列消融实验（均基于InternVL3-8B骨干）验证了HINT各组件的贡献与设计选择。

**HINT组件消融（Table 2）**：仅使用EGOPOINTVQA进行监督微调（SFT）将Reference准确率从66.1%提升至68.5%（+2.4pp），而加入手部意图令牌（HINT）后进一步提升至**75.0%**（+6.5pp over SFT-only）。这表明，单纯增加训练数据只能带来有限增益，显式的手势编码架构是实现大幅提升的关键。

**训练数据组成（Table 3）**：混合合成数据（4,000视频）与真实数据（400视频）训练获得最佳性能（Reference 75.0%）。仅用真实数据训练降至67.3%，仅用合成数据为72.9%。这揭示了合成数据在提供手势多样性方面的价值，同时也表明真实数据对于弥合领域差距不可或缺。

**手势意图建模方式对比（Table 4）**：作者比较了多种编码手势信息的方法——在视频帧上绘制箭头（视觉提示）、将3D关键点坐标转为文本输入、以及学习的Keypoint Adapter。学习适配器以75.0%的Reference准确率显著优于所有替代方案（视觉提示69.1%、文本坐标71.3%），说明让模型自主学习几何手势信息的处理方式比人工设计的表示更有效。

**手部检测置信度阈值（Table 5）**：阈值τ控制过滤噪声检测与保留有效指向手势之间的权衡。τ=0.5在所有任务上取得最佳整体平衡；过高阈值会丢失有效手势信息，过低则引入噪声令牌。

**输入帧采样策略（Table 6）**：均匀采样32帧优于仅使用人工挑选的关键帧（每个指向手势的最清晰帧）。即使关键帧具有“先知”优势，Reference准确率仍比均匀采样低3.0–4.8个百分点，说明时序上下文对理解手势动态至关重要。

**手势的关键作用验证（Table 10）**：移除视频中的手部手势后，所有任务性能急剧下降——Reference从75.0%暴跌至**41.7%**，其他任务也出现类似幅度的下降。这直接证实了指向手势是EGOPOINTVQA任务的核心信息来源，而非模型可绕过的冗余信号。

**计算开销**：在τ=0.5的设置下，HINT令牌仅占输入LLM总令牌数的不到1%，几乎不引入额外计算负担。

### 失败模式分析

尽管HINT大幅提升了性能，Figure 7揭示了四类典型失败案例：

* **基线MLLM的显著性偏差（Figure 7a）**：当场景中存在颜色鲜艳或形状独特的干扰物时，基线模型倾向于被视觉显著性误导，而非依据手势指向进行判断。
* **基线MLLM的时序混淆（Figure 7b）**：当视频中先后出现多次指向手势时，基线模型难以正确关联问题所问的特定手势时刻。
* **HINT的残余失败——关键点不可靠（Figure 7c）**：在运动模糊、遮挡或手部不在视野内的情况下，WiLoR提取的3D手部关键点质量下降，导致手势令牌缺失或编码错误，模型因此无法准确解析指向意图。
* **HINT的残余失败——快速视角漂移（Figure 7d）**：快速的头戴相机移动导致目标物体在帧间大幅位移，模型难以持续跟踪手势与物体的关联。

这些失败模式指明了未来的改进方向：提升手部姿态估计在退化条件下的鲁棒性，以及引入显式的物体跟踪机制来增强手势-物体关联。

### 补充图表

![[assets/figures/papers/paper_list_l1059_https_arxiv_org_abs_2603_12533/figures/007_Table_1.jpg]]
*Table 1: Performance of different MLLMs on the EGOPOINTVQA test set. We report multiple-choice accuracy (%). HINT (highlighted in light blue) consistently improves its corresponding open-source backbones and outperforms all compared baselines. Task categories are Reference (Refer.), Temporal, Spatial, Counting (Count), Attribute (Attr.), and Feedback (Feed.). The random baseline reflects the varying number of answer choices across tasks*

![[assets/figures/papers/paper_list_l1059_https_arxiv_org_abs_2603_12533/figures/008_Table_2.jpg]]
*Table 2: Ablation of HINT components. ‘SFT’ denotes supervised fine-tuning on EGOPOINTVQA. ‘Hand Int.’ denotes use of our Hand Intent Token. Combining both yields the largest gains*

![[assets/figures/papers/paper_list_l1059_https_arxiv_org_abs_2603_12533/figures/017_Table_10.jpg]]
*Table 10: Ablation study on the effect of hand gestures. Performance comparison on our dataset with and without the pointing hand visible in the video frames. The significant drop in performance across all tasks in the ‘w/o Hand’ setting confirms that the pointing gesture is essential for identifying the target*

![[assets/figures/papers/paper_list_l1059_https_arxiv_org_abs_2603_12533/figures/011_Table_4.jpg]]
*Table 4: Different methods of hand intent modeling. We compare different methods to encode the user’s hand pose. Our HINT with learning keypoint adapter outperforms alternative representations, such as visual prompts and textual inputs*

![[assets/figures/papers/paper_list_l1059_https_arxiv_org_abs_2603_12533/figures/009_Table_3.jpg]]
*Table 3: Impact of training dataset. We vary the usage of synthetic and real videos in the training set. Using a synthetic dataset to complement a real dataset yields the best result*

![[assets/figures/papers/paper_list_l1059_https_arxiv_org_abs_2603_12533/figures/010_Table_5.jpg]]
*Table 5: Impact of hand detection confidence threshold τ on HINT. The threshold τ controls a trade-off between filtering noisy detections and retaining valid pointing gestures. A value of 0.5 achieves the best overall performance*

![[assets/figures/papers/paper_list_l1059_https_arxiv_org_abs_2603_12533/figures/012_Table_6.jpg]]
*Table 6: Impact of input frames. We compare uniform 32-frame input with keyframes manually selected as oracle, where each pointing gesture is most clearly visible (one frame per gesture). y Even with this oracle advantage, Reference drops by 4.8/3.0pp (8B/14B) compared to uniform 32-frame input*

![[assets/figures/papers/paper_list_l1059_https_arxiv_org_abs_2603_12533/figures/016_Table_9.jpg]]
*Table 9: Human performance on EGOPOINTVQA. We report the average accuracy of 5 human participants, each evaluating the full test set (672 questions)*

![[assets/figures/papers/paper_list_l1059_https_arxiv_org_abs_2603_12533/figures/015_Figure_7.jpg]]
*Figure 7: Representative failure cases on EGOPOINTVQA. (a)- (b): baseline MLLM failures due to saliency bias and temporal confusion, respectively. (c)-(d): remaining HINT failures caused by unreliable hand keypoints and rapid viewpoint drift*



## 定位与知识库关联

### 任务定位：什么是指示性自我中心视频问答

EGOPOINTVQA 提出的核心问题是一个此前未被系统研究过的任务——**基于手势的自我中心视频问答**（gesture-grounded egocentric video question answering）。与常规视频问答不同，该任务中的问题包含指示代词（如“this one”、“that object”），要求模型必须通过视觉定位指向手势来解析指代关系，才能正确回答。任务被分解为六个子类：Reference（对象识别）、Counting（计数）、Spatial（空间关系）、Temporal（时序顺序）、Attribute（属性判断）和 Feedback（功能反馈），覆盖了从单帧指向消歧到跨帧多手势跟踪的不同难度层级。

### 现有方法与基线

论文将现有基线划分为三个层次，构成从通用到专用的能力梯度：

**通用专有 MLLM**：**GPT-4o** 和 **GPT-5** 作为闭源模型的代表，在 EGOPOINTVQA 上表现不佳，Figure 1 中展示了 GPT-4o 在指向场景下的典型失败——错误判断两个黑色锅的颜色不同。这表明即使是最强的通用模型，在缺乏手势理解机制时也无法处理指示性指代。

**开源通用 MLLM**：包括 **Qwen3-VL**（8B/32B）、**InternVL3**（8B/14B/38B/78B）和 **LLaVA-OneVision**（7B/72B）。其中 InternVL3-14B 是表现最强的开源基线，在六任务上的平均准确率为 62.7%，Reference 子任务仅 63.1%。这些模型虽具备通用视频理解能力，但架构中未设计显式的手势编码通路。

**领域专用 MLLM**：**EgoGPT**（自我中心视频理解）、**ViSpeak**（视觉指令特化）和 **VGLLM-QA**（3D 几何理解）分别从不同角度接近该问题，但均未针对指向手势进行专门建模，因此在 EGOPOINTVQA 上的表现同样受限。

### 方法谱系中的创新定位

HINT 的方法论定位可以沿两条轴线理解：

**输入模态扩展轴**：传统视频 MLLM 的输入序列仅包含视觉令牌（$V_t$）和文本令牌。HINT 在输入序列中插入第三种令牌——手势意图令牌（$H_t$），每帧一个，与视觉令牌交错排列。这种设计将手势信息从“隐式存在于像素中”提升为“显式编码的独立模态”，使 LLM 可以直接关注手部关键点的时空变化，而无需从 RGB 像素中隐式推断指向意图。该思路与多模态融合中的“显式结构化输入”范式一致，但将其首次应用于手势-指代消歧场景。

**几何先验注入轴**：HINT 并非直接从 RGB 学习手势特征，而是通过现成的 3D 手部重建模型 **WiLoR** 提取每帧 21 个 3D 关键点，再经轻量级 MLP 适配器（Keypoint Adapter）投影为单个令牌。这一设计与“几何先验引导的视觉推理”方法同源——通过注入显式的 3D 几何信息来弥补纯外观特征的不足。消融实验（Table 4）证实，学习关键点适配器（Reference 75.0%）显著优于在图像上画箭头（视觉提示）或文本输入坐标等替代方案，说明让模型自主学习几何信息的编码方式比人工设计的几何表示更有效。

### 适用边界与局限

HINT 的有效性受以下条件约束：

1. **手部可见性依赖**：HINT 的核心输入是 3D 手部关键点，当手部因运动模糊、遮挡或出画而无法被 WiLoR 可靠检测时（置信度 $c_t < \tau = 0.5$），该帧不产生手势令牌。Table 10 的消融实验从反面证实了手势信号的关键性——移除视频中的手部后，Reference 准确率从 75.0% 骤降至 41.7%。Figure 7 中的失败案例进一步揭示了不可靠关键点导致的错误。

2. **单手指向假设**：当前 HINT 仅编码单手的关键点信息，未处理多手或多人同时指向的场景。这在家庭协作、多人交互等场景下构成明显局限。

3. **指向-物体关联缺失**：HINT 将手势令牌与视觉令牌交错输入 LLM，依赖 LLM 的注意力机制隐式建立手势与目标物体的关联，但未显式建模物体边界框或分割。在目标物体密集排列或快速视角移动的场景中，这种隐式关联可能失效（Figure 7 中的视角漂移失败案例）。

4. **合成-真实领域差距**：训练数据以合成视频为主（AI2-THOR + MIXAMO），Table 3 显示仅用真实数据训练时 Reference 降至 67.3%，说明合成数据提供了关键的多样性补充。但真实环境中更复杂的手势形态、光照条件和背景噪声仍覆盖不足。

### 开放问题

- **鲁棒手部姿态估计**：如何提高在运动模糊、遮挡和极端视角下的 3D 手部关键点估计可靠性，是减少 HINT 失败的直接路径。
- **多手指向扩展**：能否将 HINT 框架推广到多手、多人同时指向的场景，需要解决手势令牌的实例级对应问题。
- **显式物体关联**：结合物体检测或跟踪模块，在架构层面显式建模“哪只手在指哪个物体”，可能进一步提升精细指向任务的表现。
- **领域自适应**：如何进一步缩小合成到真实的领域差距，例如通过更逼真的仿真渲染或域随机化策略，是实用化部署的关键。
- **人类水平差距**：Table 9 显示人类在该数据集上的平均准确率达到 95.9%，而当前最佳 HINT-14B 仅 68.1%，存在约 28 个百分点的显著差距，表明指示性自我中心视频问答仍是一个远未解决的开放挑战。



## 原文 PDF

![[paperPDFs/CVPR_2026/Do_You_See_What_I_Am_Pointing_At_Gesture_Based_Egocentric_Video_Question_Answering.pdf]]
