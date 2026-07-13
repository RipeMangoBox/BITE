---
title: "TimeViper: A Hybrid Mamba-Transformer Vision-Language Model for Efficient Long Video Understanding"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/TimeViper_A_Hybrid_Mamba_Transformer_Vision_Language_Model_for_Efficient_Long_Video_Understanding.pdf
project_link: "https://xuboshen.github.io/TimeViper/"
code_link: null
aliases:
- TimeViper
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 混合Mamba-Transformer架构中，视觉信息在深层逐渐转移到指令token（视觉到文本信息聚合现象），导致视觉token在深层高度冗余，可被大量压缩或丢弃而几乎不损失性能。
primary_logic: 在混合LLM内部引入门控交叉注意力模块TransV，显式地将冗余视觉token的信息转移到指令token中，在保留关键视觉信息的同时大幅压缩视觉token，使模型能处理超过10,000帧的长视频，并保持与Transformer基线相当的性能。
claims:
- 指令中心任务（MCQ、TVG）中，阻断视觉到指令的信息流在浅层导致性能急剧下降，但在深层影响可忽略（Figure 3）。
- 视觉中心任务（VDC）中，阻断视觉到响应的信息流在浅层导致急剧下降，表明视觉token在浅层直接贡献（Figure 3）。
- 视觉token冗余随层深增加，深层几乎100%冗余，即使完全丢弃所有视觉token，模型仍可依赖指令token达到高性能（Figure 4）。
- 与仅使用ToMe相比，TransV在4096帧时将GPU内存占用降低54.8%，预填充时间减少15.7%，并能处理10K+帧（Figure 5, 6）。
---

# TimeViper: A Hybrid Mamba-Transformer Vision-Language Model for Efficient Long Video Understanding

> [!tip] 核心洞察
> 在混合LLM内部引入门控交叉注意力模块TransV，显式地将冗余视觉token的信息转移到指令token中，在保留关键视觉信息的同时大幅压缩视觉token，使模型能处理超过10,000帧的长视频，并保持与Transformer基线相当的性能。

| 字段 | 内容 |
|------|------|
| 中文题名 | TimeViper：一种用于高效长视频理解的混合Mamba-Transformer视觉语言模型 |
| 英文题名 | TimeViper: A Hybrid Mamba-Transformer Vision-Language Model for Efficient Long Video Understanding |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2511.16595) · [Project](https://xuboshen.github.io/TimeViper/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | TimeViper |
| Dataset | VideoMME (overall) / M-Avg, Charades-STA, VDC, LVBench |

> [!tip] 效果简介
> - VideoMME (overall) / M-Avg 上，accuracy 56.9 / 48.2 (TimeViper w/ TransV) vs 55.5 / - (Video-XL) ; 65.1 / - (Qwen2.5-VL) (与Video-XL相当，但效率更高)。
> - Charades-STA 上，mIoU 37.9 (TimeViper w/ TransV) vs 34.6 (VTimeLLM) (+3.3)。
> - VDC 上，avg. score 39.1 (TimeViper w/ TransV) vs 39.0 (AuroraCap) (+0.1)。

## 概要

长视频理解面临的核心瓶颈在于：现有基于Transformer的视觉语言模型因自注意力的 $O(n^2)$ 计算复杂度，难以高效扩展至数千乃至上万帧。视觉token在LLM内部存在严重冗余，且深层计算成为主要效率障碍。**TimeViper** 针对这一问题，提出了一种**混合Mamba-Transformer架构**，结合状态空间模型（SSM）的 $O(n)$ 线性复杂度与自注意力机制的上下文表达能力，从根本上缓解长序列建模的计算压力。

通过系统性的信息阻断实验（Figure 3）与token冗余分析（Figure 4），作者揭示了混合MLLM中一个关键现象：**视觉信息在浅层逐渐聚合到指令token中，导致深层视觉token高度冗余，甚至可被完全丢弃而几乎不损失性能**。基于这一洞察，TimeViper引入了 **TransV**——一种部署于LLM内部的门控交叉注意力模块，显式地将冗余视觉token的信息转移到指令token中，在保留关键视觉信息的同时大幅压缩视觉token数量。

在效率方面，TransV在4096帧时将GPU内存占用降低54.8%，预填充时间减少15.7%，并使模型能够处理超过10,000帧的长视频（Figure 5, Figure 6）。在性能方面，TimeViper在VideoMME（56.9）、Charades-STA（mIoU 37.9）、VDC（39.1）和LVBench（35.6）等长视频理解基准上，取得了与Transformer基线相当甚至更优的结果（Table 2），同时保持了显著的推理效率优势。

长视频理解是多模态大语言模型（MLLM）走向实际应用的关键能力，涵盖小时级视频问答、时间定位和详细描述等任务。然而，现有基于Transformer的MLLM面临一个根本性瓶颈：**自注意力机制的O(n²)计算复杂度**使得处理长视觉序列时效率急剧下降。随着视频帧数增加，视觉token数量线性增长，LLM内部的长序列处理成为主要计算瓶颈，严重阻碍了视频帧数的扩展。

为缓解这一问题，混合Mamba-Transformer架构应运而生。该类模型将状态空间模型（SSM）的高效序列建模能力与注意力机制的精确上下文查询能力相结合：Mamba层以O(n)复杂度和O(1)隐藏状态缓存取代部分自注意力层，显著降低了内存占用和推理延迟。然而，仅靠架构替换仍不足以突破超长视频（万帧级别）的处理门槛——**视觉token本身存在严重冗余**，大量token在深层对任务贡献甚微，却持续消耗计算资源。

现有视觉token压缩策略（如ToMe）通常在LLM输入前的投影器中进行一次性合并，缺乏对LLM内部信息流动的动态感知。这导致两个问题：一是压缩发生在信息聚合之前，可能丢失关键视觉细节；二是压缩率受限于输入阶段，无法随层深自适应增强。因此，**如何在LLM内部显式利用视觉token的冗余特性，实现更激进而无损的压缩，是长视频理解效率突破的核心挑战**。

TimeViper正是针对上述缺口提出的解决方案。其核心动机源于一个关键发现：在混合MLLM中，视觉信息在浅层逐渐聚合到指令token，使得深层视觉token高度冗余（Figure 4显示深层几乎100%冗余）。基于此，TimeViper在LLM内部引入**TransV模块**，通过门控交叉注意力将冗余视觉token的信息显式转移到指令token中，在保留关键视觉信息的同时大幅压缩视觉token数量，使模型能处理超过10,000帧的长视频，并保持与Transformer基线相当的性能。

## 核心方法与创新机理

TimeViper 的核心创新围绕一个被揭示的关键现象展开：**视觉信息在混合 Mamba-Transformer LLM 的深层会高度聚合到指令 token 中，导致视觉 token 在深层几乎完全冗余**。基于这一发现，TimeViper 在两个关键维度上对现有长视频理解模型进行了重构。

### 1. 混合 Mamba-Transformer 骨干：打破 O(n²) 瓶颈

现有长视频模型（如 **Video-XL**，Shu et al., CVPR 2025）普遍采用纯 Transformer 骨干，其自注意力机制的计算复杂度随序列长度平方增长（O(n²)），成为处理数千帧视频时的核心效率瓶颈。TimeViper 将 LLM 骨干替换为**混合 Mamba-2 + 自注意力架构**（27 层 Mamba-2、4 层自注意力、25 层 MLP），从根本上改变了计算特性：

- **Mamba-2 层**基于状态空间模型（SSM），核心更新为 $h_t = A_t h_{t-1} + B_t x_t$，$y_t = C_t^T h_t$，实现 O(n) 线性复杂度和 O(1) 隐藏状态缓存，无需维护庞大的 KV 缓存。
- **自注意力层** $y = \mathrm{SoftMax}(L \odot \frac{Q K^T}{\sqrt{D}}) \cdot V$ 保留精确的上下文查询能力，用于关键层的全局信息整合。

这一混合设计使得 TimeViper 在处理 32k 输入 token（约 2k 帧）时，每秒生成 token 数比纯 Transformer 的 **Qwen3** 高出 40.1%（Figure 1），从根本上缓解了 LLM 内部处理长序列的计算瓶颈。

### 2. TransV：LLM 内部的视觉 token 信息转移与压缩

现有方法通常在 LLM 输入前的投影器中应用 token 合并（ToMe）来压缩视觉 token，但这种方式在深层仍会保留大量冗余视觉 token，且无法利用 LLM 内部的信息聚合特性。TimeViper 提出了 **TransV**——首个在 LLM 内部工作的 token 信息转移模块，其设计直接源于对视觉 token 冗余和信息聚合现象的因果分析：

#### 2.1 核心洞察：视觉到文本的信息聚合

通过信息阻断实验（Figure 3），TimeViper 揭示了混合 MLLM 中清晰的任务相关聚合模式：
- **指令中心任务**（多选问答 MCQ、时间视频定位 TVG）：阻断视觉到指令的信息流在浅层导致性能急剧下降，但在深层影响可忽略——视觉信息已在浅层转移到指令 token。
- **视觉中心任务**（视频详细描述 VDC）：阻断视觉到响应的信息流在浅层导致急剧下降，表明视觉 token 在浅层直接为生成提供细节。

同时，token 冗余分析（Figure 4）表明，视觉 token 的冗余度随层深增加而单调递增，深层几乎达到 100% 冗余——即使完全丢弃所有视觉 token，模型仍可依赖已聚合信息的指令 token 达到高性能。

#### 2.2 TransV 工作机制

TransV 通过**门控交叉注意力**，在 LLM 的特定层将冗余视觉 token 的信息显式转移到指令 token，随后丢弃被转移的视觉 token：

$$\tilde{X}_1^l = \mathrm{CrossAttn}_l(X_1^l, \mathrm{TD}_l(X_0^l))$$

$$X_1^{l+1} = X_1^l + \tanh(\alpha_l) \tilde{X}_1^l$$

其中 $X_0^l$ 为视觉 token，$X_1^l$ 为指令 token，$\mathrm{TD}(\cdot)$ 为 token 丢弃算子（支持均匀丢弃和基于注意力的 Top-k 丢弃），$\alpha_l$ 为可学习的标量门控参数，控制信息转移强度。

TransV 在浅层（第 7 层）使用 50% 均匀丢弃，在深层（第 39 层）使用 90% 注意力引导丢弃。这种分阶段策略匹配了信息聚合的时序特性：浅层保留足够视觉 token 完成信息转移，深层仅保留与指令高度相关的少量视觉 token。

#### 2.3 效率与性能的突破

TransV 带来的效率提升是实质性的（Figure 5, Figure 6）：
- 在 4096 帧时，**GPU 内存占用降低 54.8%**，预填充时间减少 15.7%
- 使模型能够处理 **超过 10,000 帧**的长视频，而仅使用 ToMe 的基线仅能扩展到约 5,000 帧
- 低帧数场景下无额外延迟开销

消融实验（Table 1）验证了 TransV 设计的每个关键选择：若仅使用 ToMe 而无 TransV 进行 token 转移，Charades mIoU 从 40.5 骤降至 26.1；引入 TransV 后恢复至 38.1，证明 token 信息转移而非简单丢弃是保持性能的关键。

TimeViper 的整体 pipeline 围绕“在混合 Mamba-Transformer LLM 内部主动压缩视觉 token”这一核心思想构建，其设计目标是在保持长视频理解能力的前提下，突破 Transformer 自注意力机制的 O(n²) 计算瓶颈。模型由四个关键模块串联构成，形成从原始视频帧到最终文本响应的端到端流。

**输入与视觉编码。** 视频首先以 1 fps 采样，每帧缩放到 384×384 分辨率，送入一个冻结的 ViT 视觉编码器，输出高维视觉 token 序列。ViT 在整个训练过程中保持冻结，这与部分竞争方法（如 LLaVA-Video、Qwen2.5-VL）不同，后者对 ViT 进行了微调以提升视觉特征质量。

**投影与帧级压缩。** ViT 输出的 token 经过一个可训练的投影器，映射到 LLM 的嵌入空间。投影器中集成了 token merging（ToMe），将每帧的视觉 token 压缩为固定的 16 个 token，以此消除帧内冗余。这一步压缩发生在 LLM 外部，与后续的 LLM 内部压缩形成互补。

**混合 Mamba-Transformer LLM 骨干。** 压缩后的视觉 token 与系统提示、用户指令 token 拼接后，送入混合架构的 LLM。该骨干由 27 个 Mamba-2 层、4 个自注意力层和 25 个 MLP 层交错组成。Mamba-2 层通过状态空间模型实现 O(n) 复杂度的序列建模和 O(1) 的隐藏状态缓存，大幅降低长序列场景下的内存占用和预填充延迟；自注意力层则提供精确的全局上下文查询能力，弥补 SSM 在特定位置检索上的不足。这种混合设计使得 TimeViper 在处理 32K 输入 token（约 2,000 帧）时，每秒生成 token 数比 Qwen3 高出 40.1%。

**TransV：LLM 内部的视觉 token 信息转移。** 这是 TimeViper 区别于其他视频 MLLM 的核心创新。TransV 模块部署在 LLM 内部的特定层——浅层（第 7 层）和深层（第 39 层）——通过门控交叉注意力机制，将冗余视觉 token 的信息显式转移到指令 token 中，随后丢弃大部分视觉 token。具体而言，浅层 TransV 使用均匀丢弃策略，以 50% 的丢弃率减少视觉 token；深层 TransV 则基于注意力得分进行 Top-k 选择，以 90% 的丢弃率进一步压缩。信息转移过程由可学习的标量门控参数 α 控制，公式为：

$$\tilde{X}_1^l = \mathrm{CrossAttn}_l(X_1^l, \mathrm{TD}_l(X_0^l))$$
$$X_1^{l+1} = X_1^l + \tanh(\alpha_l) \tilde{X}_1^l$$

其中 $X_0^l$ 为视觉 token，$X_1^l$ 为指令 token，$\mathrm{TD}_l(\cdot)$ 为 token 丢弃操作，$\mathrm{CrossAttn}$ 以指令 token 为 query、视觉 token 为 key/value 进行交叉注意力计算。这一设计使得模型在 4,096 帧输入时，GPU 内存占用降低 54.8%，预填充时间减少 15.7%，并能处理超过 10,000 帧的长视频，而仅依赖 ToMe 的基线在约 5,000 帧时即达到内存上限。

**输出生成。** 经过 TransV 压缩后，剩余的视觉 token 与指令 token 继续在 LLM 的后续层中交互，最终生成文本响应。整个 pipeline 的信息流可概括为：视频帧 → ViT 编码 → 投影器 + ToMe 帧级压缩 → 混合 LLM 浅层处理 → TransV 浅层信息转移与压缩 → 混合 LLM 深层处理 → TransV 深层信息转移与压缩 → 响应生成。

**训练流程。** TimeViper 采用两阶段训练：第一阶段在 3M 高质量图文对上预训练投影器，实现视觉与语言模态的对齐；第二阶段在 7.8M 样本上进行视觉指令微调，涵盖多选问答、时间定位、视频描述等任务。TransV 模块额外引入约 100M 参数，在效率与参数量之间形成可控的权衡。

TimeViper 的核心设计围绕两个关键模块展开：**混合 Mamba-Transformer LLM 骨干**和**内部视觉Token压缩模块 TransV**。前者通过状态空间模型（SSM）与自注意力机制的混合实现长序列的高效建模，后者在LLM内部显式地将冗余视觉Token信息转移到指令Token中，从而大幅压缩视觉Token数量。

### 混合Mamba-Transformer骨干

LLM骨干由 **27层 Mamba-2**、**4层自注意力** 和 **25层 MLP** 组成（Section 3.1）。Mamba-2 层的核心是状态空间模型的递推更新：

$$h_t = A_t h_{t-1} + B_t x_t$$
$$y_t = C_t^T h_t$$

其中 $h_t$ 为隐藏状态，$x_t$ 为当前输入，$y_t$ 为输出。该结构通过遗忘和记忆机制维护隐藏状态，实现 $O(n)$ 计算复杂度和 $O(1)$ 缓存开销。自注意力层则采用带因果掩码的缩放点积注意力：

$$y = \mathrm{SoftMax}(L \odot \frac{Q K^T}{\sqrt{D}}) \cdot V$$

其中 $L$ 为因果掩码，$Q$、$K$、$V$ 分别为查询、键、值投影，$D$ 为维度。混合架构在保留注意力机制上下文表达力的同时，借助SSM的效率优势处理长序列。

### TransV：视觉Token信息转移模块

TransV 是嵌入LLM内部的轻量级压缩模块，其核心机制是通过**门控交叉注意力**将冗余视觉Token的信息显式转移到指令Token中（Section 3.2, Eq. (6)）。具体操作为：

$$\tilde{X}_1^l = \mathrm{CrossAttn}_l(X_1^l, \mathrm{TD}_l(X_0^l))$$
$$X_1^{l+1} = X_1^l + \tanh(\alpha_l) \tilde{X}_1^l$$

其中 $X_0^l$ 为视觉Token，$X_1^l$ 为指令Token，$\mathrm{TD}_l(\cdot)$ 为Token丢弃算子，$\mathrm{CrossAttn}_l$ 以指令Token为查询、视觉Token为键和值计算交叉注意力，$\alpha_l \in [-1, 1]$ 为可学习的门控标量，控制信息转移强度。该设计使视觉信息在压缩前被“吸收”到指令Token中，避免直接丢弃导致的信息丢失。

Token丢弃算子 $\mathrm{TD}(X)$ 支持两种策略（Eq. (5)）：

$$\mathrm{TD}(X) = \begin{cases} \mathrm{Uniform}(X, T_d) & \text{(均匀丢弃)} \\ \mathrm{Topk}(X, -\mathrm{Attn}(X_{T_1}, X), T_d) & \text{(注意力引导丢弃)} \end{cases}$$

浅层使用均匀丢弃，深层使用基于注意力得分的 Top-k 丢弃，保留与指令Token交互最强的视觉Token。

### 信息阻断分析公式

为揭示混合LLM内部的视觉-文本信息聚合现象，TimeViper引入信息阻断掩码（Section 3.2）。阻断视觉到指令信息流（V2I）的掩码为：

$$[X_0^{l+1}, X_1^{l+1}, Y_{:t}^{l+1}] = \begin{bmatrix} 1 & 0 & 0 \\ 0 & 1 & 0 \\ 1 & 1 & 1 \end{bmatrix} \cdot [X_0^l, X_1^l, Y_{:t}^l]$$

阻断视觉到响应信息流（V2R）的掩码为：

$$[X_0^{l+1}, X_1^{l+1}, Y_{:t}^{l+1}] = \begin{bmatrix} 1 & 0 & 0 \\ 1 & 1 & 0 \\ 0 & 1 & 1 \end{bmatrix} \cdot [X_0^l, X_1^l, Y_{:t}^l]$$

其中 $Y_{:t}$ 为响应Token。通过在不同层施加阻断并观察性能变化，可精确定位视觉信息向指令Token转移的层深规律——这直接支撑了TransV在浅层和深层分别进行压缩的设计决策。

![[assets/figures/papers/paper_list_l787_https_arxiv_org_abs_2511_16595/figures/003_Figure_3.jpg]]
*Figure 3: Comparison of information blocking to illustrate the vision-to-text information aggregation phenomenon in hybrid MLLMs. For instruction-centric tasks (e.g., multi-choice video QA), information is first aggregated from vision tokens to instruction tokens, which are then used for response generation. In contrast, for vision-centric tasks*

## 实验与关键发现

### 核心发现：视觉Token冗余与信息聚合现象

TimeViper的实验分析围绕一个关键因果发现展开：在混合Mamba-Transformer架构的LLM内部，视觉token在深层存在严重冗余，且视觉信息会逐渐向指令token聚合。这一发现通过两组信息阻断实验得到验证（Figure 3）：

- **指令中心任务**（如多选问答MCQ、时间视频定位TVG）：阻断从视觉token到指令token的信息流（V2I阻断），在浅层导致性能急剧下降，但在深层影响可忽略。这表明视觉信息在浅层已被充分转移到指令token，深层视觉token几乎不再直接贡献。
- **视觉中心任务**（如视频详细描述VDC）：阻断从视觉token到响应token的信息流（V2R阻断），在浅层即造成性能崩溃。这说明视觉中心任务中，视觉token在浅层就直接参与响应生成，而非先聚合到指令token。

基于此发现，论文进一步量化了视觉token的冗余程度（Figure 4）。实验表明，视觉token冗余随层深增加而单调递增：在浅层，即使仅丢弃50%的视觉token也会造成明显性能损失；而在深层，即使丢弃90%以上的视觉token，模型性能几乎不受影响。深层视觉token近乎100%冗余——即使完全丢弃所有视觉token，模型仍可依赖指令token中已聚合的视觉信息维持高性能。

### TransV消融实验

Table 1系统消融了TransV的设计选择，揭示了以下关键规律：

1. **Token转移的必要性**：若仅使用均匀丢弃（TDuni）而不进行信息转移，在浅层50%丢弃率下，Charades-STA的mIoU从40.5骤降至26.1。引入TransV的门控交叉注意力进行token转移后，mIoU恢复至38.1。这证明单纯的token丢弃会不可逆地丢失关键视觉信息，而TransV通过将信息转移到指令token，在压缩的同时保留了任务所需的视觉信息。

2. **压缩率与层深的权衡**：在浅层（第7层）使用50%压缩率是安全的（VideoMME 56.7），但将浅层压缩率提升至90%会导致VideoMME从56.7降至53.4。深层（第39层）则可承受90%的注意力引导压缩，性能损失极小（VideoMME 56.6 vs. 无压缩58.8）。

3. **最优配置**：浅层均匀50%压缩 + 深层注意力引导90%压缩（uni-7-0.5 + attn39-0.9）在VideoMME上达到56.6，VDC上39.1，Charades上37.9，在性能与效率间取得最佳平衡，并能将处理帧数扩展至10K+。

4. **压缩位置的影响**：将浅层TransV从第7层移至第2层（uni-2-0.5），VDC性能从38.9升至39.7，但VideoMME从56.7降至56.1。这表明不同任务对压缩位置的敏感度不同，视觉中心任务更依赖浅层未压缩的视觉token。

### 效率分析

TransV的效率优势在Figure 5和Figure 6中得到量化验证：

- **GPU内存占用**（Figure 5）：在4096帧输入下，TransV将GPU内存占用降低54.8%。仅使用ToMe时，上下文窗口仅能扩展至约5000帧；而配备TransV后，模型可高效处理超过10000帧的视频。
- **预填充时间**（Figure 6）：在4096帧时，TransV将预填充时间减少15.7%。值得注意的是，在低帧数（如64帧）下，TransV不引入任何额外延迟，体现了其轻量设计。

![[assets/figures/papers/paper_list_l787_https_arxiv_org_abs_2511_16595/figures/007_Figure_5.jpg]]
*Figure 5: Comparison of GPU memory usage during inference. While ToMe extends the context window to about 5K frames, TransV efficiently scales beyond 10K frames*

![[assets/figures/papers/paper_list_l787_https_arxiv_org_abs_2511_16595/figures/005_Figure_6.jpg]]
*Figure 6: Comparison of prefilling time. TransV incurs no additional latency at low frame inputs (e.g., 64 frames) while significantly reducing prefilling time at high frame inputs. For instance, at 4,096 frames, TransV reduces prefilling time by 15.7% compared to the ToMe baseline*

### 主实验结果

Table 2展示了TimeViper与现有方法在多个长视频理解基准上的对比：

| 基准 | 指标 | TimeViper (w/ TransV) | 对比方法 | 结果 |
|------|------|----------------------|----------|------|
| VideoMME | accuracy | 56.9 | Video-XL (55.5) | 相当，效率更高 |
| Charades-STA | mIoU | 37.9 | VTimeLLM (34.6) | +3.3 |
| VDC | avg. score | 39.1 | AuroraCap (39.0) | +0.1 |
| LVBench | accuracy | 35.6 | Gemini-1.5-Pro (33.1) | +2.5 |

在VideoMME上，TimeViper以56.9的准确率与基于Transformer的Video-XL（55.5）相当，但受益于Mamba层的O(n)计算复杂度和O(1)缓存成本，推理效率显著更高。在时间定位任务Charades-STA上，TimeViper以37.9 mIoU显著超越专用模型VTimeLLM（34.6）。在小时级长视频理解LVBench上，超越Gemini-1.5-Pro达2.5个百分点。

### 公平性说明

需注意以下对比公平性因素：
- TimeViper未对ViT进行微调（因计算资源限制），而LLaVA-Video、Qwen2.5-VL等竞争方法进行了ViT微调，这可能影响视觉特征提取质量。
- 训练数据总量为7.8M样本，远小于Nanov2-VL的46.7M，后者可视为混合架构的性能上界。
- 所有比较均采用统一评估协议：1 fps采样，最多256帧，384×384分辨率，每帧压缩为16个token。

### 跨架构迁移分析

Table 4揭示了TransV在不同LLM架构上的迁移效果：将TransV应用于纯Transformer的Qwen2.5时，LVBench提升0.4但VDC下降1.3（-1.3）；而应用于混合架构Nano时，VDC仅下降0.6。这表明混合架构（Mamba + 自注意力）对token压缩更为鲁棒，纯Transformer架构在视觉中心任务上对视觉token的压缩更为敏感。

### 扩展性分析

Figure 7展示了测试时增加输入帧数的扩展性。模型训练时使用256帧，评估时以1 fps采样。随着最大帧数从64增至1024，TimeViper在VideoMME上的性能持续提升，验证了模型对长序列的有效利用能力。值得注意的是，即使输入帧数远超训练时的256帧，模型仍能稳定获益，体现了混合架构和TransV带来的长序列泛化能力。

### 失败模式与局限

1. **浅层高压缩率的性能损失**：浅层使用90%压缩率导致VideoMME下降3.3点（Table 1），表明浅层视觉token仍承载不可忽视的细粒度信息，过度压缩会损害性能。
2. **参数开销**：TransV增加约100M参数，在效率与参数量之间存在权衡。
3. **视觉中心任务的敏感性**：VDC等视觉中心任务对token压缩更为敏感，纯Transformer架构下该敏感性进一步放大（Table 4）。
4. **数据规模约束**：当前7.8M训练样本可能限制了模型性能上限，与Nanov2-VL（46.7M样本）的性能差距部分源于数据量不足。

![[assets/figures/papers/paper_list_l787_https_arxiv_org_abs_2511_16595/figures/006_Table_1.jpg]]
*Table 1: Ablation of TransV choices. The “uni 7 0.5-attn 39 0.9” denotes applying uniform TranV at the 7th layer with a dropping rate of*

![[assets/figures/papers/paper_list_l787_https_arxiv_org_abs_2511_16595/figures/014_Table_4.jpg]]
*Table 4: Performance of applying TransV to Qwen2.5 and Nano*

![[assets/figures/papers/paper_list_l787_https_arxiv_org_abs_2511_16595/figures/011_Figure_9.jpg]]
*Figure 9: Qualitative results of TimeViper on three long video understanding tasks. (1) MCQ: The model demonstrates reasoning capability by correctly answering a multi-choice question about the video’s content. (2) TVG: It accurately localizes the temporal boundaries for a specific event, reaching an IoU of 0.75. (3) VDC: The model generates a detailed description that showcases its fine-grained comprehension. Green text highlights accurate detailed descriptions. Some output in the middle is omitted for brevity*

## 定位与知识库关联

### 1. 与现有工作的关系

TimeViper 处于**长视频理解**与**高效视觉语言模型**两条技术路线的交汇点，其核心贡献可从架构选择和压缩策略两个维度进行定位。

#### 1.1 架构谱系：从纯Transformer到混合Mamba-Transformer

长视频理解的主流方案长期由Transformer架构主导。**Video-XL**（Shu et al., CVPR 2025）代表了基于纯Transformer的超长视频模型路线，通过内部视觉token压缩来扩展可处理帧数，但其底层仍受制于自注意力机制的O(n²)计算复杂度。**LLaVA-Video**（Zhang et al., TMLR 2025）则通过大规模视频指令微调来提升Transformer MLLM的视频理解能力，同样未触及架构层面的效率瓶颈。**Qwen2.5-VL**（Yang et al., technical report）作为纯Transformer基线的性能上界，在多个基准上表现优异，但其推理效率随帧数增加而急剧下降。

TimeViper选择了一条不同的路径：采用**混合Mamba-2 + Self-Attention**的LLM骨干（27层Mamba-2、4层自注意力、25层MLP）。这一设计借鉴了状态空间模型在长序列建模上的线性复杂度优势，同时保留了注意力层在关键位置的精确上下文查询能力。与纯Transformer基线**Qwen2.5-7B**（使用相同训练配方训练）相比，TimeViper的核心差异在于用Mamba层替换了大部分自注意力层，从而将计算复杂度从O(n²)降至O(n)，并将KV缓存替换为O(1)的隐藏状态缓存。

值得注意的是，**Nanov2-VL**作为同期工作，同样采用了混合架构，并在46.7M训练样本上取得了更强的性能，可视为混合架构路线的性能上界。TimeViper仅使用7.8M训练样本即展现出与Transformer基线相当的性能，表明混合架构在数据效率方面具有潜力，但性能上限仍受数据量约束。

#### 1.2 压缩策略谱系：从外部压缩到内部信息转移

视觉token压缩是长视频理解的关键技术。传统方法通常在LLM输入前的投影器中进行token合并（如ToMe），这是一种**外部压缩**策略。TimeViper的核心创新在于将压缩从LLM外部移至**LLM内部**，并通过TransV模块实现**视觉到指令的信息转移**。

这一设计选择源于对混合LLM内部信息流动的深入分析。通过信息阻断实验（Figure 3），TimeViper揭示了两个关键现象：
- **指令中心任务**（如MCQ、TVG）中，视觉信息在浅层被聚合到指令token，深层视觉token高度冗余；
- **视觉中心任务**（如VDC）中，视觉token在浅层直接贡献于响应生成。

基于这一发现，TransV在浅层（第7层）使用均匀丢弃（50%压缩率）进行温和压缩，在深层（第39层）使用注意力引导的Top-k丢弃（90%压缩率）进行激进压缩。这种**分层差异化压缩**策略与ToMe的全局统一压缩形成鲜明对比：消融实验（Table 1）显示，若仅使用ToMe而不使用TransV，Charades mIoU会从40.5骤降至26.1，而引入TransV后恢复至38.1，证明token信息转移是保持性能的关键。

#### 1.3 任务专用模型对比

在具体任务上，TimeViper与多个专用模型形成对比：
- **时间视频定位（TVG）**：**VTimeLLM**（基于Vicuna-13B）是时间视频定位的专用MLLM，TimeViper在Charades-STA上以37.9 mIoU超越其34.6 mIoU（+3.3），同时保持通用视频理解能力。
- **视频详细描述（VDC）**：**AuroraCap**（基于Vicuna-7B）是视频详细描述模型，TimeViper以39.1 vs 39.0的微弱优势（+0.1）与之持平，表明压缩策略未显著损害视觉中心任务的细粒度描述能力。

### 2. 适用边界

TimeViper的设计选择决定了其适用的场景边界：

**适用场景**：
- **超长视频理解**：得益于Mamba层的线性复杂度和TransV的token压缩，TimeViper可处理超过10,000帧的视频（Figure 5），适用于小时级视频分析、监控视频理解等场景。
- **指令中心任务**：MCQ、TVG等依赖高层语义推理的任务，视觉token在深层高度冗余，TransV的激进压缩几乎不损害性能（Figure 3）。
- **推理效率敏感场景**：在4096帧输入时，TransV降低54.8% GPU内存占用和15.7%预填充时间（Figure 5, 6），且低帧数下无额外延迟。

**不适用或需谨慎的场景**：
- **视觉中心任务**：VDC等需要细粒度视觉信息的任务，深层压缩可能导致细节丢失。Table 4显示，将TransV应用于Qwen2.5时VDC下降1.3点，而混合架构仅下降0.6点，表明混合架构对压缩更鲁棒，但仍存在轻微损失。
- **浅层高压缩率场景**：Table 1显示，浅层使用90%压缩率会导致VideoMME从56.7降至53.4（-3.3），表明浅层视觉token仍承载关键信息，需保守压缩。
- **参数敏感场景**：TransV增加约100M参数，在追求极致参数效率的场景中需权衡。

### 3. 局限与开放问题

#### 3.1 已知局限

1. **参数效率权衡**：TransV模块增加约100M参数，在提升长序列处理能力的同时牺牲了参数效率。这一开销是否可通过知识蒸馏或参数共享进一步降低，尚待探索。

2. **视觉编码器未微调**：当前TimeViper未对ViT进行微调，而许多竞争方法（如LLaVA-Video、Qwen2.5-VL）进行了ViT微调。这可能导致视觉特征提取质量受限，尤其在视觉中心任务上。在计算资源允许的情况下，ViT微调可能带来额外收益。

3. **训练数据规模约束**：7.8M的训练数据总量远小于Nanov2-VL的46.7M，性能上限受数据量制约。在更大规模数据下，混合架构与TransV的性能增益能否持续保持，仍需验证。

4. **压缩率的手动设计**：当前TransV的层深选择和压缩率（浅层50%、深层90%）基于经验设定，缺乏自适应机制。不同视频的视觉冗余程度不同，固定压缩率可能导致信息丢失或压缩不足。

5. **Mamba层可解释性不足**：分析发现Mamba层的注意力模式多样（稀疏、局部、全局），但其对视觉-文本信息聚合的具体贡献机制尚不清晰，限制了进一步优化的方向。

#### 3.2 开放问题

1. **跨架构泛化性**：TransV的信息转移机制能否直接应用于其他混合架构（如Samba、Hymba）以实现即插即用？Table 4显示TransV在Qwen2.5和Nano上的效果存在差异，暗示不同架构对信息转移的响应不同，其泛化条件需系统研究。

2. **自适应压缩**：如何根据输入视频的复杂度（帧数、运动程度、语义密度）自适应选择最优压缩率和应用层？这可能需要引入轻量级的视频复杂度估计模块或基于强化学习的动态压缩策略。

3. **视觉-文本聚合的普遍性**：视觉-文本信息聚合现象是否在单张图片或图文交错任务中也普遍存在？若存在，TransV的设计思路可能推广至更广泛的多模态场景。

4. **跨层信息转移**：当前TransV仅实现视觉到指令的单向信息转移。能否通过跨层信息转移（如深层视觉token向浅层指令token的反馈）进一步提升压缩效率并减少性能损失？

5. **规模化行为**：在更大规模数据（>50M样本）和更大模型尺寸（>13B参数）下，混合架构的线性复杂度优势能否持续保持？TransV的压缩-性能权衡曲线是否会发生变化？这需要更大规模的实验验证。

6. **与长上下文技术的结合**：TransV的token压缩与RoPE外推、位置编码插值等长上下文技术是否存在协同效应？两者的结合能否进一步扩展可处理视频的时长上限？

## 原文 PDF

![[paperPDFs/CVPR_2026/TimeViper_A_Hybrid_Mamba_Transformer_Vision_Language_Model_for_Efficient_Long_Video_Understanding.pdf]]
