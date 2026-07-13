---
title: "MIDAS: Multi-Image Dispersion and Semantic Reconstruction for Jailbreaking MLLMs"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/MIDAS_Multi_Image_Dispersion_and_Semantic_Reconstruction_for_Jailbreaking_MLLMs.pdf
project_link: null
code_link: https://github.com/Winnie-Lian/MIDAS
openreview_forum_id: tXsE2wKPvx
aliases:
- MIDAS
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "通过将有害语义分解并分散到多个图像中，利用游戏式视觉推理模板强制模型进行长时间的结构化推理，从而延迟有害内容的暴露并降低安全注意力，是提升越狱成功率的核心可控因素。"
primary_logic: "将有害查询拆分为风险子单元，隐藏于看似无害的视觉谜题中，结合人格驱动的文本重构诱导模型逐步融合并重建恶意意图，利用自回归生成惯性在安全机制反应前输出有害内容。"
claims:
- "MIDAS在HADES基准上对Gemini-2.5-FT模型的攻击成功率（ASR）达93.34%，远超最强基线VisCRA的46.98%"
- "消融实验显示移除游戏式视觉推理后ASR从80%骤降至22%，证明该模块是成功的最关键组件"
- "MIDAS将有害关键词的平均暴露位置从48.44%推迟到64.53%，并将平均推理长度从419.64 tokens延长至3195.30 tokens，有效延迟了有害语义的出现"
- "在强防御系统提示下（System Prompt 3），MIDAS对Gemini-2.5-Pro仍保持67.26%的ASR，而VisCRA仅剩5.36%"
---

# MIDAS: Multi-Image Dispersion and Semantic Reconstruction for Jailbreaking MLLMs

> [!tip] 核心洞察
> 将有害查询拆分为风险子单元，隐藏于看似无害的视觉谜题中，结合人格驱动的文本重构诱导模型逐步融合并重建恶意意图，利用自回归生成惯性在安全机制反应前输出有害内容。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | MIDAS：用于越狱多模态大模型的多图像分散与语义重构 |
| 英文题名 | MIDAS: Multi-Image Dispersion and Semantic Reconstruction for Jailbreaking MLLMs |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=tXsE2wKPvx) · [GitHub](https://github.com/Winnie-Lian/MIDAS) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | MIDAS |
| Dataset | HADES, MM-SafetyBench (tiny), AdvBench |

> [!tip] 效果简介
> - HADES 上，ASR 为 93.34%，对比 46.98% (VisCRA)，变化 +46.36%。
> - MM-SafetyBench (tiny) 上，ASR 为 99.16%，对比 49.70% (VisCRA)，变化 +49.46%。
> - AdvBench 上，ASR 为 97.96%，对比 4.00% (FigStep)，变化 +93.96%。

## 概要

### 核心问题与瓶颈

多模态大模型（MLLM）的安全对齐在面对多步跨模态推理时存在一个深层脆弱性：模型的安全注意力会随着推理链的延长而滑移，导致有害内容在安全机制反应前即被输出。现有越狱方法普遍依赖单图像或孤立的视觉线索，仅能实现浅层推理扩展，难以有效突破对齐较强的闭源模型（如GPT-4o、Gemini-2.5-Pro）的安全防护。

### 方法定位

**MIDAS**（Multi-Image Dispersion and Semantic Reconstruction）提出了一种系统性的越狱框架，其核心策略是将有害语义分解为风险子单元，分散嵌入多张游戏式视觉推理模板图像中，同时通过人格驱动的文本重构诱导模型逐步融合并重建恶意意图。该方法在方法谱系中的定位如下：

| 维度 | 现有方法 | MIDAS |
|------|---------|-------|
| 图像数量 | 单图像（FigStep、VisCRA、HIMRD等） | 多图像（默认6张） |
| 视觉嵌入 | 直接像素掩码、视觉提示或孤立线索 | 六种游戏式视觉推理模板（Letter Equation、Jigsaw Letter、Rank-and-Read等） |
| 文本策略 | 直接有害指令或简单模板 | 人格驱动推理诱导 + 占位符绑定 + 分层角色结构 |
| 语义分布 | 集中于单一模态 | 跨多图像分散，满足交叉覆盖、单单元隔离、平衡分配约束 |
| 解码路径 | 单步直接解码或浅层推理 | 多步结构化推理驱动的文本重构 |

MIDAS通过将有害关键词的平均暴露位置从48.44%推迟到64.53%，并将平均推理长度从约420 tokens延长至约3195 tokens（Table 6），有效延迟了有害语义的显现，利用自回归生成惯性在安全机制反应前输出有害内容。

### 主要结果

在三个基准上的核心结果如下：

- **HADES基准**（Table 1）：MIDAS对Gemini-2.5-FT模型的攻击成功率（ASR）达**93.34%**，远超最强基线VisCRA的46.98%（+46.36个百分点）；有害性评分（HR）达4.32，远超VisCRA的2.22。
- **MM-SafetyBench (tiny)**（Table 2）：MIDAS对Gemini-2.5-FT的ASR达**99.16%**，VisCRA仅49.70%。
- **AdvBench**（Table 3）：MIDAS对Gemini-2.5-Pro的ASR达**97.96%**，而FigStep仅4.00%。

消融实验（Table 5）揭示了各组件的重要性：移除游戏式视觉推理后ASR从80%骤降至22%，证明该模块是框架最关键组件；将多图像分散替换为单图像处理后ASR降至50%；移除角色驱动诱导后ASR降至59%。

在鲁棒性方面，MIDAS在强防御系统提示下对Gemini-2.5-Pro仍保持**67.26%**的ASR，而VisCRA仅剩5.36%（Table 8）；跨评判一致性实验（Table 12）使用四个独立评判模型证实MIDAS在所有评判下均稳定超越基线，结果不受评判偏差影响。

### 局限性

该方法目前仅在静态多图像场景下验证，尚未探索长时程视频或流式输入中的行为；游戏模板设计依赖人工经验，可能引入认知偏差；在强防御（如ShieldLM）下成功率下降至约48.81%，表明输入过滤仍有一定抑制作用。



多模态大模型（MLLM）通过融合视觉与文本输入，展现出强大的跨模态理解和生成能力，其生成过程可形式化为 $r = \Gamma(i, t)$ 及自回归分布 $p_{\Theta}(z \mid i, t) = \prod_{k=1}^{|z|} p_{\Theta}(z_k \mid z_{<k}, r)$。然而，这种跨模态融合机制在拓展模型能力边界的同时，也引入了新的安全脆弱面——攻击者可通过精心构造的视觉-文本联合输入，诱导模型生成被禁止的有害内容。

当前针对MLLM的越狱攻击方法主要沿两条路径展开：**单图像视觉提示**（如FigStep, Gong et al., 2025；SI-Attack, Zhao et al., 2025b）和**跨模态语义操纵**（如HADES, Li et al., 2024b；VisCRA, Sima et al., 2025；HIMRD, Teng et al., 2024）。这些方法的核心思路是将有害语义嵌入视觉通道，试图绕过以文本为主的安全过滤器。然而，它们存在一个共同的结构性缺陷：**有害语义在单一模态（单张图像或孤立视觉线索）中过于集中，模型的安全注意力能够在浅层推理阶段便被激活并阻断攻击**。即便VisCRA引入了单图像掩码与分步推理，其推理链长度仍然有限（平均仅419.64 tokens），有害关键词在生成序列中的平均暴露位置仅为48.44%，安全机制有充足时间介入。

更深层的瓶颈在于：**MLLM的安全对齐在面对多步跨模态推理时，其安全注意力会随着推理链的延长而滑移**。现有方法未能有效利用这一特性——它们或依赖单图像、或仅进行浅层推理扩展，无法迫使模型进入长时间的结构化推理状态，从而无法突破对齐较强的闭源模型（如GPT-4o、Gemini-2.5-Pro）的安全防护。这一缺口在强防御设置下尤为突出：当部署防御性系统提示时，VisCRA对Gemini-2.5-Pro的攻击成功率（ASR）仅剩5.36%。

上述分析揭示了一个关键的可控因素：**通过将有害语义分解并分散到多个图像中，利用游戏式视觉推理模板强制模型进行长时间的结构化推理，从而延迟有害内容的暴露并降低安全注意力，是提升越狱成功率的核心机制**。MIDAS正是围绕这一洞察展开设计——将有害查询拆分为风险子单元，隐藏于看似无害的视觉谜题中，结合人格驱动的文本重构诱导模型逐步融合并重建恶意意图，利用自回归生成惯性在安全机制反应前输出有害内容。



## 核心方法与创新机理

MIDAS 的核心创新在于将越狱攻击从“单模态集中暴露”重构为“多模态分散-延迟重构”范式，通过五个关键维度的协同改变，实现了对强对齐闭源多模态大模型的大幅攻击成功率提升。

### 从单图像到多图像分散：语义风险的跨模态解耦

现有越狱方法（如 **VisCRA**（Sima et al., 2025）、**HIMRD**（Teng et al., 2024））将有害语义集中于单张图像或单一文本通道，安全过滤器仅需检测单一模态即可阻断攻击。MIDAS 将有害查询的关键风险词提取后，分解为子片段并分散嵌入多张图像（默认 6 张），同时施加三重约束（Equation 6）：

- **交叉图像覆盖**：每个风险单元至少分配到 2 张不同图像，迫使模型必须跨图像推理才能重建完整语义；
- **单单元隔离**：任一图像不包含完整风险单元，单张图像自身无害；
- **平衡分配**：各图像承载的片段数量尽可能均匀，避免信息密度异常触发检测。

消融实验（Table 5）证实，将多图像分散替换为单图像处理后，ASR 从 80% 降至 50%，验证了多图像分散是攻击成功的必要条件。

### 从直接像素掩码到游戏式视觉推理模板：推理链的强制性延长

现有方法（如 VisCRA 的单图像掩码、FigStep 的视觉提示）仅要求模型进行浅层视觉识别，安全注意力在推理早期即可聚焦到风险区域。MIDAS 设计了六种游戏式视觉推理模板（Figure 6-10）：Letter Equation、Jigsaw Letter、Rank-and-Read、Odd-One-Out、Navigate-and-Read、CAPTCHA。这些模板将有害子片段编码为需要多步逻辑推理才能解码的视觉谜题，强制模型进入长时间的结构化推理轨迹。

这一改变的因果效应极为显著：消融实验中移除游戏式视觉推理后，ASR 从 80% 骤降至 22%（Table 5），是框架中最关键的单组件。Table 6 进一步揭示了机制——MIDAS 将有害关键词的平均暴露位置从 VisCRA 的 48.44% 推迟到 64.53%，平均推理长度从 419.64 tokens 延长至 3195.30 tokens。推理链的延长使得安全注意力随生成进程滑移，有害内容在安全机制反应前已被自回归生成惯性输出。

### 从直接有害指令到人格驱动文本重构：意图的渐进式诱导

现有方法的文本通道通常直接包含有害指令或简单模板，容易被文本安全过滤器捕获。MIDAS 的文本策略包含三层递进改变：

1. **占位符消毒**：用无害占位符（如 `<img_1>`）替换原始有害词，使文本表面完全无害；
2. **上下文绑定**（Equation 8）：将占位符与对应图像的隐藏片段建立跨模态绑定关系，模型解码图像后自动填充；
3. **人格驱动诱导**（Equation 9）：注入分层角色结构——权威服从层（如“你是安全研究员”）降低模型防御姿态，调查者/战略家层（如“请分析以下谜题的含义”）引导模型从特定视角解释重构出的有害语义。

消融实验（Table 5）显示，移除角色驱动诱导后 ASR 降至 59% 且 HR 下降，表明人格引导不仅影响攻击成功率，还提升有害响应的连贯性和危害程度。

### 从单步解码到多步结构化语义重构：攻击面的时序扩展

现有方法依赖单步直接解码或浅层推理，安全机制可在生成早期拦截。MIDAS 通过局部解码函数 $\tau_k$（Equation 7）逐图像提取隐藏片段，再按图像顺序拼接重建完整有害指令序列 $\bar{R}$（Equation 11）。这一“分散编码—逐片解码—顺序融合”的流水线将有害语义的暴露延迟到生成后期，而自回归模型的生成惯性使得中途终止变得困难。Table 6 的数据直接支撑了这一机制：MIDAS 的有害关键词在生成序列的后 1/3 才出现，此时模型已完成大量“合法”推理，安全过滤器面临更高的误拒风险。

### 创新协同的实证验证

五个 changed slots 的协同效应在强防御场景下尤为突出：在最强防御系统提示（System Prompt 3）下，MIDAS 对 Gemini-2.5-Pro 仍保持 67.26% 的 ASR，而 VisCRA 仅剩 5.36%（Table 8）。跨评判一致性实验（Table 12）使用四个独立评判模型（GPT-5-nano、Gemini-2.5-FT、Qwen3、DeepSeek-R1）验证了结果的稳健性，排除单一评判偏差的干扰。



![[assets/figures/papers/paper_list_l44_https_openreview_net_forum_id_tXsE2wKPvx/figures/002_Figure_2.jpg]]
*Figure 2: Pipeline of MIDAS. (1) Text Process: extract risk-bearing units, decompose them into subunits, and replace them with placeholders; (2) Image Process: embed the subunits into multiple benign-looking puzzle images that enforce step-by-step reasoning; (3) Model Output: the model decodes puzzle fragments, reconstructs the hidden semantics, and generates harmful responses under persona-driven reasoning guidance*

![[assets/figures/papers/paper_list_l44_https_openreview_net_forum_id_tXsE2wKPvx/figures/001_Figure_1.jpg]]
*Figure 1: Overview. (a) Compared to text-only (T) and text+image (T+I) attacks that are blocked by safety filters, our proposed MIDAS leverages Game-based Visual Reasoning (GVR) to bypass defenses and induce harmful outputs. (b) Examples of visual reasoning puzzles used in our MIDAS. (c) Our proposed MIDAS achieves significantly higher Attack Success Rate (ASR) and Harmfulness Rating (HR) than other baselines*

MIDAS 将越狱攻击建模为一个**多模态语义分散与跨模态重构**问题。其核心思想是：将有害查询的语义分解为多个看似无害的风险子单元，分别嵌入多张图像和消毒后的文本模板中，然后通过强制模型执行多步结构化推理，逐步融合并重建恶意意图，最终在安全机制反应前生成有害输出。

### 流水线总览

整个框架由三个顺序阶段构成（Figure 2），形成“分散—隐藏—重构”的攻击闭环：

1.  **文本处理**：从原始有害查询中提取关键风险词（risk-bearing units），将其分解为子片段，并用无害占位符替换原词，生成消毒后的文本骨架。
2.  **图像处理**：将分解后的子片段嵌入多张外观无害的游戏式视觉推理谜题中，每张图像仅包含部分语义碎片，单独审视不构成威胁。
3.  **模型输出**：目标模型在解码视觉谜题时被迫执行逐步推理以恢复隐藏片段，随后按图像顺序填充文本占位符，在人格驱动的诱导下重建完整有害指令并生成有害响应。

### 攻击目标的形式化

MIDAS 将多模态大模型（MLLM）视为条件生成模型，通过融合算子 $\Gamma$ 将视觉输入 $i$ 与文本输入 $t$ 映射到统一的跨模态表示 $r$，再自回归生成输出序列 $z$：

$$r = \Gamma ( i , t ), \quad p _ { \Theta } ( z \mid i , t ) = \prod _ { k = 1 } ^ { | z | } p _ { \Theta } \left( z _ { k } \mid z _ { < k } , r \right)$$

越狱攻击的目标是构造对抗性输入 $(i^*, t^*)$，最大化模型生成禁止输出 $z^\dagger$ 的对数似然：

$$\operatorname* { m a x } _ { ( i ^ { * } , t ^ { * } ) } \ \log p _ { \Theta } ( z ^ { \dagger } \mid r ^ { * } )$$

与现有方法将有害语义集中于单一模态（文本或单张图像）不同，MIDAS 将风险**分散到多张图像和文本通道**，确保每个组件在孤立状态下无害，仅当跨模态融合表示被重建时才恢复恶意意图。这一设计直接针对多模态大模型安全对齐的瓶颈：安全注意力会随着推理链延长而滑移，而 MIDAS 通过延长推理链来延迟有害内容的暴露。

### 五大核心模块

MIDAS 的流水线可细化为五个功能模块，各模块之间存在严格的依赖关系：

| 模块 | 功能 | 关键机制 |
|------|------|----------|
| **风险单元提取** | 从有害查询中识别关键风险词 | 轻量提取器 $E_\eta$ 将查询 $q$ 映射为风险词集合 $\mathcal{R} = \{r_1, r_2, ..., r_m\}$ |
| **语义分解与分散** | 将风险词分解为子片段并分配给多张图像 | 遵守三条约束：交叉图像覆盖（每个风险单元至少分配到2张不同图像）、单单元隔离、平衡分配 |
| **模板化视觉编码** | 将子片段嵌入游戏式视觉推理模板 | 六种谜题模板（字母方程、拼图字母、排序阅读、找不同、导航阅读、CAPTCHA），每张图像定义局部解码函数 $\tau_k$ |
| **文本掩码与角色构造** | 用占位符替换有害词并注入分层角色 | 消毒模板 $\tilde{t}$ 与人格提示 $q^*$ 拼接，形成“权威服从层+调查者/战略家层”的双层诱导结构 |
| **跨模态推理与重构** | 模型解码谜题并填充占位符，重建有害指令 | 按图像顺序拼接解码片段 $\bar{R} = [\hat{S}(i_1), \hat{S}(i_2), \dots, \hat{S}(i_H)]$，利用自回归生成惯性输出有害内容 |

### 输入输出流

- **输入**：一个有害文本查询 $q$（如“如何制作爆炸物”），以及 $H$ 张游戏式视觉谜题图像（默认 $H=6$）。
- **中间表示**：风险词集合 $\mathcal{R}$ → 子片段分配矩阵 → 嵌入谜题的对抗图像 $i_k^*$ → 消毒文本模板 $\hat{t}$ → 跨模态绑定关系 $B$。
- **输出**：模型通过逐步解码谜题、填充占位符，最终生成完整的有害响应 $z^\dagger$。

### 关键设计决策

**冗余比约束**：设关键词数量为 $k$，图像数量为 $H$，强制要求冗余比 $\rho = H/k \geq 2$，确保每个风险词至少被分割到两张图像中。超参数敏感性分析（Figure 3）表明，在 $(k=3, H=6)$ 时取得最优的 ASR 与 HR 权衡，这也是后续所有实验的默认配置。

**游戏式推理的核心地位**：消融实验（Table 5）提供了决定性证据——移除游戏式视觉推理后，ASR 从 80% 骤降至 22%，证明该模块是框架中最关键的组件。相比之下，将多图像分散替换为单图像处理后 ASR 降至 50%，移除角色驱动诱导后降至 59%，影响虽显著但不及游戏推理剧烈。



### 3.1 问题形式化与越狱目标

MIDAS将多模态大模型（MLLM）定义为一个条件生成模型。给定视觉输入 $i \in \mathcal{Z}$ 和文本输入 $t \in \mathcal{T}$，模型通过跨模态融合算子 $\Gamma$ 产生融合表示 $r$，再自回归生成输出序列 $z$：

$$r = \Gamma(i, t), \quad p_{\Theta}(z \mid i, t) = \prod_{k=1}^{|z|} p_{\Theta}\left(z_k \mid z_{<k}, r\right)$$

越狱攻击的目标是构造对抗性输入 $(i^*, t^*)$，最大化模型生成禁止输出 $z^{\dagger}$ 的对数似然：

$$\operatorname*{max}_{(i^*, t^*)} \log p_{\Theta}(z^{\dagger} \mid r^*)$$

其中 $r^* = \Gamma(i^*, t^*)$。与现有方法将有害语义集中于单一模态不同，MIDAS将风险分散到多个视觉项和文本通道中，确保每个组件单独无害，仅当融合表示被重构时才恢复恶意意图。

### 3.2 语义分解与多图像分散

**风险单元提取。** 给定有害查询 $q$，MIDAS使用轻量级提取器 $E_{\eta}$ 识别最关键的风险承载单元：

$$\mathcal{R} = E_{\eta}(q) = \{r_1, r_2, ..., r_m\}, \quad 1 \leq m \leq m_{\max}$$

**片段分解与分配。** 每个风险单元 $r_u$ 被分解为更小的片段 $S(r_u) = \{s_{u,1}, ..., s_{u,\ell}\}$，然后分配到图像集 $I = \{i_1, ..., i_H\}$。分配满足三个约束：

1. **交叉图像分散**：每个风险单元至少分配到两个不同图像，即 $\left|\left\{k : \exists j, A_{(u,j),k} = 1\right\}\right| \geq 2, \forall u$；
2. **单单元隔离**：同一图像不包含来自同一风险单元的多个片段；
3. **平衡分配**：最小化各图像包含片段数量的方差 $\min \operatorname{Var}_k(|S(i_k)|)$。

**模板化视觉编码。** 将片段嵌入游戏式视觉推理模板中，生成对抗图像 $i_k^*$：

$$i_k^* = \psi_v^{(k)}\big(i_k, \boldsymbol{S}^{(k)}, T_k\big)$$

其中 $T_k$ 为选定的游戏模板，$\boldsymbol{S}^{(k)}$ 为分配给该图像的片段集。

### 3.3 文本掩码与人格驱动诱导

**文本消毒与占位符绑定。** 将有害查询 $q$ 中的风险词替换为无害占位符，得到消毒模板 $t^*$，并将其与图像占位符序列绑定：

$$\tilde{t} = \psi_t\bigl(t^*, \{\langle \mathrm{img}_1 \rangle, \dots, \langle \mathrm{img}_H \rangle\}\bigr)$$

形成跨模态绑定关系 $B = \{\langle \mathrm{img}_k \rangle S^{(k)}\}_{k=1}^{H}$。

**人格驱动推理诱导。** 在消毒模板上拼接人格提示 $q^*$，将恶意意图抽象为高阶角色视角：

$$\hat{t} = \tilde{t} \oplus q^*$$

该策略采用分层角色结构——权威服从层与调查者/战略家层——引导模型从特定视角解释重构出的有害语义，降低安全注意力。

### 3.5 跨模态重构与解码

定义局部解码函数 $\tau_k$，从游戏图像中提取隐藏片段：

$$\hat{S}(i_k) = \tau_k(i_k^*)$$

按图像顺序拼接解码出的片段，得到重建的有害指令序列：

$$\bar{R} = \left[\hat{S}(i_1), \hat{S}(i_2), \dots, \hat{S}(i_H)\right]$$

模型在文本占位符处依次填充解码结果，利用自回归生成惯性在安全机制反应前输出完整有害内容。这一多步结构化推理驱动的重构过程是延迟有害语义暴露的核心机制——消融实验证实，移除游戏式视觉推理后，ASR从80%骤降至22%（Table 5），验证了该模块的决定性作用。



## 实验与关键发现

### 核心实验设置

MIDAS 默认采用冗余比 $\rho = H/k \geq 2$ 的约束（即每个关键词至少被分片到两张图像中），经超参数敏感性分析（Figure 3）确定最优配置为关键词数 $k=3$、图像数 $H=6$，该设置在 ASR 和 HR 上取得最可靠的折衷，并作为后续所有实验的默认参数。实验在单个 NVIDIA RTX 3090 GPU（CUDA 12.2）上运行，MIDAS 无需额外 GPU 加速或大内存，运行时比较公平。

### 主实验结果

**HADES 基准（Table 1）**：MIDAS 在全部 7 个模型（4 个商业模型、3 个开源模型）上均取得最优 ASR 和 HR。在 Gemini-2.5-FT 上，MIDAS 的 ASR 达 93.34%，HR 达 4.32，而最强基线 VisCRA 仅为 46.98% 和 2.22，ASR 提升 +46.36 个百分点。在 GPT-5-Chat 上，MIDAS 的 ASR 为 64.00%，远超 VisCRA 的 14.68%。

![[assets/figures/papers/paper_list_l44_https_openreview_net_forum_id_tXsE2wKPvx/figures/005_Table_1.jpg]]
*Table 1: Comparison results with state-of-the-art jailbreak methods on the HADES benchmark across 4 commercial models and 3 open-source models. Bold numbers indicate the best jailbreak performance*

**MM-SafetyBench (tiny) 基准（Table 2）**：MIDAS 在 Gemini-2.5-FT 上取得近乎完美的 99.16% ASR 和 4.35 HR，在 GPT-4o 上为 86.67%，在 GPT-5-Chat 上为 82.50%，在所有模型上均以大幅优势超越 VisCRA、HIMRD、SI-Attack 和 FigStep。

![[assets/figures/papers/paper_list_l44_https_openreview_net_forum_id_tXsE2wKPvx/figures/006_Table_2.jpg]]
*Table 2: demonstrate that enforcing multi-image dispersion and structured semantic reconstruction enables MIDAS to outperform state-of-the-art jailbreak methods by a large margin on challenging scenarios. Table 2: Comparison results with state-of-the-art jailbreak methods on the MM-SafetyBench (tiny) benchmark across 4 commercial models and 1 open-source model. Bold numbers indicate the best jailbreak performance. Results on MM-SafetyBench. Results on MM-Safetybench (Liu et al., 2024) are summerized in Table 2. This benchmark contains diverse multimodal safety-critical scenarios, making it a strong test of generalization. MIDAS achieves nearly perfect ASR on Gemini-2.5-FT and QVQ-Max, and maintains...*

**AdvBench 基准（Table 3）**：在更具挑战性的纯文本有害查询场景下，MIDAS 在 Gemini-2.5-Pro 上取得 97.96% ASR，而 FigStep 仅 4.00%，HIMRD 仅 2.00%，提升幅度超过 93 个百分点。在 GPT-5-Chat 上 MIDAS 仍保持 64.00% ASR，证明多图像分散策略对强对齐闭源模型同样有效。

![[assets/figures/papers/paper_list_l44_https_openreview_net_forum_id_tXsE2wKPvx/figures/007_Table_3.jpg]]
*Table 3: Comparison results with state-of-the-art jailbreak methods on Advbench benchmark across 4 commercial models and 1 open-source model. Bold numbers indicate the best jailbreak performance*

**运行效率（Table 4）**：MIDAS 在 Gemini-2.5-Pro 上平均耗时 190.23 秒，在 GPT-5-Chat 上仅 55.63 秒，显著快于 VisCRA（分别为 421.81 秒和 107.96 秒）和 HIMRD（3357.00 秒和 266.78 秒），表明多图像并行推理在效率上具有优势。

![[assets/figures/papers/paper_list_l44_https_openreview_net_forum_id_tXsE2wKPvx/figures/008_Table_4.jpg]]
*Table 4: Runtime comparison of different jailbreak methods on Gemini-2.5-Pro and GPT-5-Chat*

### 消融实验

Table 5 展示了在 AdvBench 上逐步移除 MIDAS 各组件的效果，完整 MIDAS 的 ASR 为 80%、HR 为 3.12：

![[assets/figures/papers/paper_list_l44_https_openreview_net_forum_id_tXsE2wKPvx/figures/009_Table_5.jpg]]
*Table 5: Ablation study of MIDAS on Advbench*

- **移除游戏式视觉推理（w/o Game-Style Reasoning）**：ASR 从 80% 骤降至 22%，HR 从 3.12 降至 0.92，降幅最大。这证明强制模型进行结构化视觉推理是延迟安全注意力滑移、引导有害语义重建的最关键组件。
- **将多图像分散替换为单图像处理（w/o Multi-Image）**：ASR 降至 50%，HR 降至 2.24，验证了跨图像语义分散对降低单图像可检测性的核心作用。
- **移除角色驱动诱导（w/o Role-Driven Induction）**：ASR 降至 59%，HR 降至 2.76，表明人格引导有助于模型更连贯地组装有害响应，但对攻击成功率的贡献次于视觉推理和多图像分散。
- **移除占位符绑定（w/o Placeholder Binding）**：ASR 降至 72%，HR 降至 2.88，影响相对较小但仍不可忽略。

### 推理链分析与安全机制评估

**推理链延长效应（Table 6）**：MIDAS 将有害关键词的平均暴露位置从 VisCRA 的 48.44% 推迟到 64.53%，平均推理长度从 419.64 tokens 延长至 3195.30 tokens（约 7.6 倍）。这表明 MIDAS 通过游戏式视觉推理强制模型进入更长、更结构化的推理轨迹，有害语义仅在生成的后期阶段才被揭示，从而在安全机制反应前完成有害输出。

![[assets/figures/papers/paper_list_l44_https_openreview_net_forum_id_tXsE2wKPvx/figures/010_Table_6.jpg]]
*Table 6: Comparison of keyword exposure position and reasoning length on the HADES benchmark*

**LlamaGuard 安全性评估（Figure 4a）**：使用 LlamaGuard 对输入和输出进行安全性分类，结果显示 MIDAS 的输入被一致判定为安全，而输出则被判定为有害，证明该攻击能有效绕过基于输入过滤的安全检测。

**防御鲁棒性（Table 7, Table 8, Figure 4b）**：
- 在 ShieldLM 外部过滤防御下，MIDAS 的 ASR 从 99.16% 降至 48.81%，但仍显著高于 VisCRA 的 7.50%。
- 在 Self-Reminder 内部自校正防御下，MIDAS 保持 70.83% ASR，而 VisCRA 仅 10.83%。
- 在三种不同强度的防御系统提示下（Table 8），MIDAS 对 Gemini-2.5-Pro 的 ASR 分别为 85.71%、81.82% 和 67.26%，而 VisCRA 在最严格提示下仅剩 5.36%。MIDAS 的 ASR 相对下降幅度远小于 VisCRA，证明多图像分散策略对防御提示具有更强的鲁棒性。

![[assets/figures/papers/paper_list_l44_https_openreview_net_forum_id_tXsE2wKPvx/figures/021_Table_8.jpg]]
*Table 8: ASR comparison under different defensive system prompts*

![[assets/figures/papers/paper_list_l44_https_openreview_net_forum_id_tXsE2wKPvx/figures/018_Table_7.jpg]]

### 游戏模板与复杂度分析

**模板通用性（Table 9）**：六种游戏模板在 AdvBench 上攻击 Gemini-2.5-Pro 的 ASR 均超过 87%，其中 Letter Equation 达 97.96%，CAPTCHA 最低为 87.76%，说明模板设计具有良好的通用性和可替换性。

**认知难度与攻击效果的关系（Table 10, Table 11）**：Table 10 从符号推理、视觉搜索、空间排列、干扰抵抗和序列记忆五个维度对各模板评分。中等难度模板（如 Letter Equation）取得最佳攻击效果。Table 11 显示手动调节复杂度时，中等复杂度级别取得峰值 ASR 和 HR，过低则安全注意力未被充分消耗，过高则模型解码失败率上升。

### 跨评判一致性验证

Table 12 使用 GPT-5-nano、Gemini-2.5-FT、Qwen3 和 DeepSeek-R1 四个独立评判模型对 GPT-4o 和 GPT-5-Chat 上的攻击结果进行评估。尽管不同评判器的绝对评分因严格度不同而略有波动，MIDAS 在所有评判器下均一致超越所有基线方法，确认实验结果不受单一评判偏差影响。

![[assets/figures/papers/paper_list_l44_https_openreview_net_forum_id_tXsE2wKPvx/figures/025_Table_12.jpg]]
*Table 12: Cross-judge evaluation results attacking GPT-4o and GPT-5-Chat. While absolute scores vary slightly due to different judge strictness, MIDAS consistently outperforms all baselines across every evaluator, confirming that our results are robust to the choice of judge*

### 失败模式与局限性

- **强外部过滤**：在 ShieldLM 防御下 ASR 降至约 48.81%，表明基于输入的过滤仍对 MIDAS 有一定抑制作用，部分有害查询在输入阶段即被拦截。
- **极高复杂度模板**：CAPTCHA 模板的 ASR 相对较低（87.76%），过高的感知难度可能导致模型解码失败，反而降低攻击成功率。
- **静态图像场景限制**：方法仅在静态多图像场景下验证，未探索长时程视频或流式输入中的行为，该场景下的有效性需要手动验证。
- **评判偏差**：尽管进行了跨评判验证，绝对评分仍可能受评判模型严格度的影响，不同评判器间的绝对数值不可直接横向对比。

### 补充图表

![[assets/figures/papers/paper_list_l44_https_openreview_net_forum_id_tXsE2wKPvx/figures/020_Table_7.jpg]]
*Table 7: ASR comparison between VisCRA and our MIDAS under different defense mechanisms. MIDAS demonstrates significantly higher robustness against both external filtering and internal self-correction*



## 定位与知识库关联

### 与现有越狱范式的关键分岔

MIDAS 的定位可以从**语义暴露时机**和**推理链深度**两个轴来理解，它与现有方法的根本差异在于是否主动延迟有害语义的暴露。

**单图像/单模态集中暴露**是早期越狱方法的主流范式。**FigStep**（Gong et al., 2025）将有害指令直接编码到视觉提示中，模型在解码初期即遭遇完整有害语义，安全过滤器有充分时间介入。**SI-Attack**（Zhao et al., 2025b）利用图像-文本顺序不一致性制造冲突，但有害内容仍集中于单一模态，安全注意力未被有效分散。这些方法的共同瓶颈在于：有害语义的暴露位置过早（通常在生成序列的前50%位置），安全对齐机制能够在有害输出生成前完成拦截。

**跨模态融合操纵**代表了第二阶段的尝试。**HADES**（Li et al., 2024b）通过跨模态融合操纵试图绕过对齐，但本质上仍依赖孤立的视觉线索。**VisCRA**（Sima et al., 2025）引入了单图像掩码与分步推理，将有害内容隐藏在掩码后并要求模型逐步揭示，这是向延迟暴露迈出的重要一步。然而，VisCRA 的推理链深度有限——实验数据显示其平均推理长度仅为 419.64 tokens，有害关键词的平均暴露位置在 48.44%，意味着有害语义仍在生成过程的中段就被模型捕获，安全机制有约一半的生成窗口进行干预。

**MIDAS 的突破在于将“延迟暴露”推向极致**。通过多图像分散（默认6张图像）和游戏式视觉推理模板，MIDAS 将平均推理长度拉长至 3195.30 tokens（约7.6倍于VisCRA），有害关键词的平均暴露位置推迟到 64.53%。这意味着模型在输出超过六成内容后才开始暴露有害语义，安全注意力已在长程推理中被逐步滑移和稀释，自回归生成惯性使得安全机制在反应过来之前有害内容已输出完毕。

### 核心机制的知识贡献

MIDAS 的知识贡献可分解为三个相互强化的机制，每个机制都有明确的消融证据支撑：

**多图像语义分散**是基础架构创新。与 **HIMRD**（Teng et al., 2024）的启发式风险跨模态分散不同，MIDAS 引入了形式化的分配约束——交叉图像覆盖（每个风险单元至少分配到两个不同图像）、单单元隔离、平衡分配——确保有害语义的碎片化程度最大化。消融实验显示，将多图像分散替换为单图像处理后，ASR 从 80% 降至 50%，验证了碎片化程度与越狱成功率之间的因果关联。

**游戏式视觉推理**是 MIDAS 最关键的贡献，也是消融实验中影响最大的组件：移除该模块后 ASR 从 80% 骤降至 22%。六种模板（Letter Equation、Jigsaw Letter、Rank-and-Read、Odd-One-Out、Navigate-and-Read、CAPTCHA）的共同特征是将有害片段嵌入看似无害的谜题中，强制模型进行结构化推理才能解码。这种设计利用了 MLLM 的推理能力本身作为攻击载体——模型越擅长推理，越容易被诱导完成有害语义的重构。认知难度评分（Table 10）表明，中等难度的模板效果最佳，过于简单则无法有效延迟暴露，过于复杂则模型可能解码失败。

**人格驱动文本重构**提供语义连贯性保障。通过分层角色结构（权威服从层 + 调查者/战略家层），MIDAS 将消毒后的文本模板与人格提示拼接，引导模型从特定视角解释重构出的有害语义。消融显示移除该模块后 ASR 降至 59%，且有害响应质量（HR）下降，表明人格引导不仅影响成功率，还影响有害输出的连贯性和危害程度。

### 适用边界与局限

**已知有效域**：MIDAS 在静态多图像场景下经过充分验证，覆盖 4 个闭源商业模型（Gemini-2.5-FT/Pro、GPT-4o、GPT-5-Chat）和 3 个开源模型（QVQ-Max、Qwen2.5-VL、InternVL2.5），在 HADES、MM-SafetyBench、AdvBench 三个基准上均取得最优。方法无需 GPU 加速或额外内存，运行时效率显著优于基线（Table 4）。

**已知失效域与衰减**：
- **强输入过滤**：在 ShieldLM 防御下，MIDAS 的 ASR 降至约 48.81%（Table 7），表明外部输入过滤仍能在一定程度上识别分散后的有害片段。
- **强系统提示**：在最具防御性的 System Prompt 3 下，MIDAS 对 Gemini-2.5-Pro 的 ASR 降至 67.26%，虽然仍远超 VisCRA 的 5.36%，但绝对衰减幅度达约 25 个百分点（Table 8）。
- **未探索域**：方法仅在静态多图像场景下验证，长时程视频或流式输入中的语义分散行为与鲁棒性尚未探索。游戏模板的设计依赖人工经验，可能引入人类认知偏差。

### 开放问题

1. **长时程多模态场景的泛化**：在视频或流式输入中，如何在时间维度上有效调度分散片段并可靠重建，同时保持隐蔽性？
2. **过程感知防御**：当前防御（ShieldLM、Self-Reminder）主要依赖输入过滤或输出自检。能否开发推理过程感知的监控机制，在中间状态检测有害意图的重构趋势，而非仅靠静态筛查？
3. **模板自动优化**：游戏模板的难度和多样性目前依赖人工设计。能否自动搜索最优模板配置以最大化攻击效果，同时保持对安全过滤器的隐蔽性？
4. **动态多阶段防御**：面对迟滞性语义重构攻击，如何设计动态、多阶段防御体系，在推理链的不同节点设置检查点，同时避免对正常多步推理任务的过度干扰？



## 原文 PDF

![[paperPDFs/ICLR_2026/MIDAS_Multi_Image_Dispersion_and_Semantic_Reconstruction_for_Jailbreaking_MLLMs.pdf]]
