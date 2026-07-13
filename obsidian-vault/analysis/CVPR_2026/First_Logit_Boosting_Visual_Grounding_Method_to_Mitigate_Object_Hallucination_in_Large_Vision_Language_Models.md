---
title: "First Logit Boosting: Visual Grounding Method to Mitigate Object Hallucination in Large Vision-Language Models"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/First_Logit_Boosting_Visual_Grounding_Method_to_Mitigate_Object_Hallucination_in_Large_Vision_Language_Models.pdf
project_link: null
code_link: "https://github.com/jiwooha20/FLB"
aliases:
- FLBF
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 首个生成token的logit（l_0），因其在视觉token之后立即生成，保留了最强的视觉信号。
primary_logic: 将首个token的logit存储并在整个解码过程中加入后续token预测，可维持视觉接地，抑制语言先验；同时提升以“The”开头的句子概率，间接抑制幻觉。
claims:
- 对比解码方法均无法抑制长距离衰减，而FLB有效缓解了幻觉预测
- 首个token的logit中，真实物体词比幻觉词具有一致更高的logit
- "FLB在AMBER基准上实现最低CHAIR（LLaVA1.5: 6.1 vs. Baseline 11.5），全面超越VCD、ICD和M3ID"
- AMBER (LLaVA1.5) 上 CHAIR↓ = 6.1 (±0.37)
---

# First Logit Boosting: Visual Grounding Method to Mitigate Object Hallucination in Large Vision-Language Models

> [!tip] 核心洞察
> 将首个token的logit存储并在整个解码过程中加入后续token预测，可维持视觉接地，抑制语言先验；同时提升以“The”开头的句子概率，间接抑制幻觉。

| 字段 | 内容 |
|------|------|
| 中文题名 | First Logit Boosting：缓解大型视觉-语言模型物体幻觉的视觉接地方法 |
| 英文题名 | First Logit Boosting: Visual Grounding Method to Mitigate Object Hallucination in Large Vision-Language Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2604.00455) · [Code](https://github.com/jiwooha20/FLB) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | First Logit Boosting (FLB) |
| Dataset | AMBER, CHAIR |

> [!tip] 效果简介
> - AMBER (LLaVA1.5) 上，CHAIR↓ 6.1 (±0.37) vs 11.5 (±0.29) (减少5.4（降幅47%）)；Hal↓ 31.6 (±0.99) vs 48.9 (±0.78) (减少17.3)。
> - CHAIR (LLaVA1.5, MSCOCO) 上，CHAIR_i↓ 12.0 (±0.50) vs 17.3 (±0.74) (减少5.3（降幅31%）)。
> - AMBER (InstructBLIP) 上，CHAIR↓ 9.0 (±0.19) vs 11.6 (±0.22) (减少2.6)。

## 概要

大型视觉-语言模型（LVLMs）在生成文本时普遍存在**物体幻觉（object hallucination）**——即生成的内容包含图像中并不存在的物体。现有研究多归因于视觉-语言对齐不足或训练数据偏差，但本文揭示了更深层的瓶颈：**视觉接地存在长距离衰减（long-term decay）**。随着自回归解码的推进，视觉信息逐渐被语言先验淹没，导致后部token频繁产生幻觉。已有的对比解码方法（如VCD、ICD、M3ID）均无法有效抑制这一趋势（Figure 2）。

本文提出 **First Logit Boosting (FLB)**，核心思路简洁而巧妙：**首个生成token的logit（l₀）** 因紧接视觉token之后生成，保留了最强的视觉信号。FLB将l₀缓存并在整个解码过程中以时间递增权重w_t=γ(1−e^{-λt})加到后续token预测上，同时引入**自适应合理性约束**（仅保留原始概率≥β·max概率的候选token），从而持续维持视觉接地。该方法包含两个互补机制：**直接视觉接地**（l₀中真实物体词的logit一致高于幻觉词，Figure 3）和**隐式视觉参照**（提升以“The”开头的句子概率，间接抑制长距离幻觉，Figure 6）。

**主要结果**：在AMBER基准上，LLaVA1.5的CHAIR从11.5降至6.1（降幅47%），Hal从48.9降至31.6；在MSCOCO CHAIR上，CHAIR_i从17.3降至12.0（降幅31%）。FLB在InstructBLIP和mPLUGOwl2等不同架构上也表现出一致的增益，且推理开销可忽略。消融实验证实直接视觉接地和“The”效应各自独立有效，全开FLB达最优。

**方法定位**：FLB属于解码时干预（decoding-time intervention），无需重新训练或微调模型，与现有的对比解码方法正交。其知识贡献在于首次揭示并利用**首个token logit的视觉锚定效应**来对抗长距离衰减，为缓解LVLM幻觉提供了新的因果操控维度。

### 大型视觉-语言模型的物体幻觉困境

大型视觉-语言模型（LVLMs）在图像描述、视觉问答等多模态任务中展现出强大能力，但其生成文本中频繁出现与视觉输入不一致的“物体幻觉”（object hallucination）——即描述图像中并不存在的物体。这一问题的核心瓶颈在于**视觉接地的长距离衰减**（long-term decay）：随着自回归解码步数增加，模型对视觉信息的依赖逐渐减弱，语言先验逐步主导生成过程，导致后部token位置产生大量幻觉预测。

### 现有对比解码方法的局限

为缓解幻觉，近期工作提出了多种对比解码（Contrastive Decoding, CD）策略，其核心思路是通过对比原始输入与扰动输入（如失真图像、扰动指令）的输出logit，放大视觉相关信息。代表性方法包括：

- **VCD（Visual Contrastive Decoding）**：对比原始图像与失真图像（如添加高斯噪声）的logit，以公式 $p_{\mathrm{vcd}}(y \mid v, v', x) = \mathrm{softmax}[(1+\alpha)\mathrm{logit}_\theta(y \mid v, x) - \alpha\,\mathrm{logit}_\theta(y \mid v', x)]$ 进行修正。
- **ICD（Instruction Contrastive Decoding）**：通过对比完整指令与扰动指令的输出来抑制幻觉。
- **M3ID（Multi-Modal Mutual-Information Decoding）**：基于互信息准则调整多模态解码。

然而，如 Figure 2 所示，这些方法存在一个共同缺陷：**均无法有效抑制长距离衰减**。随着生成序列增长，所有CD变体中真实物体token的平均logit持续下降，而幻觉token的logit持续上升，VCD、ICD、M3ID均未能扭转这一趋势。这表明，仅靠对比扰动信号不足以在长文本生成中维持稳定的视觉接地。

### 核心洞察：首个token的视觉锚定效应

FLB方法的关键发现来自对解码过程早期信号的细致观察：

1. **首个token的logit（$l_0$）保留最强视觉证据**：如 Figure 3 所示，在描述一张图像时，首个生成token的logit中，真实物体词（如“man”）的logit始终高于幻觉词（如“women”）。这是因为$l_0$在视觉token之后立即生成，受语言先验的累积偏置最小，视觉信号最强。

2. **“The”效应的隐性视觉引用**：如 Figure 4 所示，首个token的logit中排名最高的token多为“The”、“In”、“A”等句子起始词。其中，“The”作为定冠词，其高概率意味着模型倾向于以确定性的指代开启描述。Figure 6 进一步揭示，以“The”开头的句子在长距离token位置上的幻觉概率显著低于其他句子——这种“The”效应为后续名词选择提供了稳定初始化，在长距离衰减加剧前就锁定了指代对象。

### 本文动机

基于上述洞察，FLB提出了一条不同于传统对比解码的路径：**直接利用首个token的logit作为贯穿整个解码过程的视觉锚点**。通过将$l_0$存储并按时间加权加入后续每个token的预测中，FLB同时激活两种互补机制——（1）直接视觉接地：$l_0$中保留的视觉证据持续抑制幻觉token的logit增长；（2）隐性视觉引用：提升以“The”开头的句子概率，使模型在长距离衰减发生前就选择视觉确定的指代对象，从而间接抑制后续幻觉。

这一设计无需额外训练、无需图像扰动、无需外部模型，仅需缓存一个logit向量，推理开销可忽略不计。

## 核心方法与创新机理

FLB 的核心创新在于**将视觉接地从“事后纠正”转变为“源头锚定”**，通过一个极低成本的解码干预，从根本上改变了 LVLM 生成过程中视觉信号逐渐衰减的动力学。

### 问题根源：长距离衰减与对比解码的失效

LVLM 在自回归生成过程中存在一个被忽视的系统性缺陷：**长距离衰减**（long-term decay）。随着生成序列的延长，语言先验逐渐主导预测，视觉信息的影响力持续下降，导致后部 token 频繁产生物体幻觉。现有主流的对比解码（Contrastive Decoding, CD）方法——包括 **VCD**（Visual Contrastive Decoding，基于失真图像）、**ICD**（Instruction Contrastive Decoding，基于扰动指令）和 **M3ID**（Multi-Modal Mutual-Information Decoding，基于互信息）——均试图通过对比原始分布与扰动分布来放大视觉信号，但 **Figure 2** 提供了决定性证据：这些方法都无法抑制长距离衰减趋势，随着序列增长，幻觉词的 logit 仍然持续上升，真实物体词的 logit 持续下降。FLB 是唯一有效逆转这一趋势的方法。

### 关键洞察：首个 token 的视觉锚定效应

FLB 建立在一个被验证的因果观察之上：**首个生成 token 的 logit（l₀）保留了最强的视觉信号**。如 **Figure 3** 所示，在首个 token 的 logit 分布中，真实物体词（如 "man"）的 logit 一致高于幻觉词（如 "women"）。这一现象的机制在于：首个 token 紧接视觉 token 之后生成，尚未受到自回归过程中逐步累积的语言先验干扰，因此构成了最纯净的视觉接地信号。

### 方法创新：存储-加权-约束三段式解码干预

FLB 将上述洞察转化为一个三段式的解码干预机制，其核心 `changed_slots` 在于将标准自回归解码规则：

$$y_t \sim p_\theta(y_t \mid v, x, y_{<t})$$

替换为受约束的加权解码规则：

$$y_t \sim \mathrm{softmax}\big[\mathrm{logit}_\theta(y \mid v, x, y_{<t}) + w_t l_0\big], \quad \text{subject to } y_t \in \mathcal{V}_{\mathrm{head}}(y_{<t})$$

具体包含三个模块：

1. **First Logit Storage（l₀ 缓存）**：在生成首个 token 时，将其完整 logit 向量缓存为 $l_0 = \mathrm{logit}_\theta(y \mid x, v)$，作为后续所有解码步的视觉锚点。

2. **Weighted Addition（时序加权注入）**：在后续每个解码步中，将 $l_0$ 按时间权重 $w_t = \gamma(1 - e^{-\lambda t})$ 加到原始 logit 上。该权重函数随时间步 $t$ 逐渐增大，精确对抗长距离衰减——越靠后的 token，视觉锚点的注入强度越大。$\gamma$ 控制最大注入强度，$\lambda$ 控制增速。

3. **Adaptive Plausibility Constraint（自适应合理性约束）**：构建候选集 $\mathcal{V}_{\mathrm{head}}(y_{<t}) = \{y_t \in \mathcal{V} : p_\theta(y_t \mid v, x, y_{<t}) \geq \beta \max_w p_\theta(w \mid v, x, y_{<t})\}$，仅保留原始概率不低于 $\beta$ 倍最大概率的 token，防止不合理词汇因 logit 扰动而被采样。

### 双重作用机制

FLB 的效果来自两个互补的机制，消融实验（**Table 5**）证实两者各自独立有效，联合使用达到最佳性能：

- **直接视觉接地**：$l_0$ 中真实物体词的高 logit 直接提升后续 token 中对应物体的概率，起到持久的视觉锚定作用。
- **隐式视觉引用**：$l_0$ 中高频首词 "The" 的 logit 提升，使得生成句子更倾向于以 "The" 开头。**Figure 6** 揭示了这一效应的深层机制：以 "The" 开头的句子在长距离上展现出显著更低的幻觉增长，因为 "The" 作为定冠词要求后续名词具有明确的视觉指代，从而在句子初始化阶段就建立了更稳定的指称一致性。

### 与对比解码的本质差异

FLB 与 CD 类方法在干预逻辑上存在根本性差异。CD 方法通过对比原始分布与失真分布来“放大”视觉信号，但其扰动源（失真图像、扰动指令）本身与视觉接地并无直接的因果关联。FLB 则直接利用解码过程中自然存在的视觉信息梯度——首个 token 的 logit——作为锚点，干预的对象是视觉信号衰减的动力学过程本身，而非对分布进行事后修正。这一设计使得 FLB 在推理速度上几乎无额外开销（仅需存储和加法操作），而 CD 方法因需要两次前向传播，速度近乎减半。

FLB 的整体 pipeline 由一个极其精简的解码期干预闭环构成：**存储→加权注入→约束过滤**，无需额外训练、不引入外部模型，完全在现有 LVLM 的自回归生成循环内运行。

### 核心数据流

1. **首次生成与 logit 缓存**  
   给定视觉输入 $v$ 和文本提示 $x$，模型执行第一步自回归预测，生成首个 token 的 logit 向量：
   $$l _ { 0 } = \operatorname { l o g i t } _ { \theta } ( y \mid x , v )$$
   该向量被完整存储，作为后续所有解码步的“视觉锚点”（Figure 1）。这一步的关键在于：$l_0$ 是视觉 token 处理完毕后立即产生的分布，保留了最强的视觉接地信号——真实物体词（如 “man”）的 logit 一致高于幻觉词（如 “women”）（Figure 3）。

![[assets/figures/papers/paper_list_l752_https_arxiv_org_abs_2604_00455/figures/001_Figure_1.jpg]]
*Figure 1: Overview of First Logit Boosting (FLB). FLB stores the logit of the first generated token and reuses it during decoding, which leverages two complementary effects. (1) Direct visual grounding: the first token logit inherently carries stronger visual evidence (man) than hallucinated token (women), serving as an anchor that preserves visual cues weakened by positional drift. (2) Implicit visual referencing: by boosting the probability of starting a sentence with “The”, FLB increases the likelihood of selecting nouns established before long-term decay occurs, thus maintaining referential coherence and mitigating hallucination*

2. **逐步加权注入**  
   在后续每个解码步 $t$，模型先正常计算当前步的条件 logit $\log \mathrm { i t } _ { \theta } ( y \mid v , x , y _ { < t } )$，然后将缓存的 $l_0$ 以时间权重 $w_t$ 叠加：
   $$y _ { t } \sim \mathrm { s o f t m a x } \Big [ \log \mathrm { i t } _ { \theta } ( y \mid v , x , y _ { < t } ) + w _ { t } l _ { 0 } \Big ]$$
   权重函数采用渐近增长形式：
   $$w _ { t } = \gamma ( 1 - e ^ { - \lambda t } )$$
   其中 $\gamma$ 控制最大干预强度，$\lambda$ 控制增长速度。这种设计直接针对 **长距离衰减**——随着序列增长，语言先验逐渐主导，视觉信号减弱（Figure 2 显示 VCD、ICD、M3ID 均无法抑制这一趋势），而 $w_t$ 随 $t$ 增大恰好反向补偿衰减。

3. **自适应合理性约束**  
   直接叠加 logit 可能将低概率 token 推入采样候选集，产生语法错误或不合理生成（如句子中间异常插入 “The”）。为此，FLB 在 softmax 采样前施加一个硬约束，仅保留原始概率不低于 $\beta$ 倍最大概率的 token：
   $$\mathcal { V } _ { \mathrm { h e a d } } ( y _ { < t } ) = \{ y _ { t } \in \mathcal { V } : p _ { \theta } ( y _ { t } \mid v , x , y _ { < t } ) \geq \beta \underset { w } { \operatorname* { m a x } } p _ { \theta } ( w \mid v , x , y _ { < t } ) \}$$
   最终完整的 FLB 解码规则为：
   $$y _ { t } \sim \mathrm { s o f t m a x } \Big [ \log \mathrm { i t } _ { \theta } ( y \mid x , v , y _ { < t } ) + w _ { t } l _ { 0 } \Big ] , \mathrm { s u b j e c t ~ t o ~ } y _ { t } \in \mathcal { V } _ { \mathrm { h e a d } } ( y _ { < t } )$$
   消融实验（Table 15, Figure 9）表明，$\beta=0.1$ 在抑制幻觉和保持真实物体覆盖之间取得最优平衡；移除该约束（$\beta=0$）会导致生成质量下降。

### 模块关系与干预时机

三个模块形成**单向串行闭环**：

- **First Logit Storage** 仅在 $t=0$ 执行一次，是唯一的“记忆写入”操作；
- **Weighted Addition** 在每个 $t \geq 1$ 步执行，是持续的“视觉信号补偿”；
- **Adaptive Plausibility Constraint** 紧随加权加法之后，作为“安全过滤器”确保生成合理性。

整个流程嵌入在标准自回归循环中，不改变模型参数、不修改注意力机制、不增加额外前向传播。与 VCD、ICD、M3ID 等对比解码方法相比（这些方法需要额外运行失真图像或扰动指令的前向传播，推理速度约为基线的两倍），FLB 仅需缓存一个 logit 向量并执行向量加法，推理速度几乎无退化（Figure 5）。

### 双重效应机制

FLB 的干预同时激活两个互补效应（Figure 1）：

1. **直接视觉接地**：$l_0$ 中真实物体词的 logit 高于幻觉词，将其持续注入后续步相当于为模型提供持续的视觉证据锚点，直接抑制后部 token 的幻觉倾向。
2. **隐式视觉引用**：$l_0$ 中 “The” 等句首冠词具有极高 logit（Figure 4），FLB 因此提升了以 “The” 开头的句子概率。以 “The” 开头的句子在长距离上表现出更低的幻觉增长（Figure 6），形成一种“稳定初始化”效应，间接维持指代一致性。

消融实验（Table 5）证实两个效应各自独立有效：单独激活直接视觉接地（仅保留 $l_0$ 中名词 token 的 logit）和单独激活 “The” 效应（仅保留冠词 token 的 logit）均能降低 CHAIR，但全开 FLB 达到最佳性能（CHAIR: 5.7 vs. 单独视觉 9.2, 单独 “The” 6.5）。

### 超参数与跨模型适配

FLB 仅引入三个超参数：$\gamma$（最大权重）、$\lambda$（增长速度）、$\beta$（约束阈值）。默认设置在 LLaVA1.5 和 InstructBLIP 上均有效，在 mPLUG-Owl2 上也表现出跨架构迁移能力（Table 18），但更广泛的跨模型泛化性仍需验证。

![[assets/figures/papers/paper_list_l752_https_arxiv_org_abs_2604_00455/figures/026_Table_18.jpg]]
*Table 18: Performance comparison of mPLUGOwl2 on AMBER. The highest scores are marked in bold*

### 3.1 问题形式化：自回归解码中的视觉衰减

标准LVLM的自回归解码过程可表述为：

$$y _ { t } \sim p _ { \theta } ( y _ { t } \mid v , x , y _ { < t } ) \propto \exp { \big ( } \log \mathrm { i t } _ { \theta } ( y _ { t } \mid v , x , y _ { < t } ) { \big ) }$$

其中 $v$ 为视觉输入，$x$ 为文本提示，$y_{<t}$ 为已生成的token序列。核心瓶颈在于：随着解码步数 $t$ 增加，视觉token与当前生成位置之间的距离增大，RoPE位置编码导致视觉信息发生**长距离衰减（long-term decay）**，语言先验逐渐主导预测，使后续token更易产生与视觉事实不符的物体幻觉。Figure 2 的定量分析证实，现有对比解码方法（VCD、ICD、M3ID）均无法有效抑制这一趋势，而FLB则显著缓解了幻觉预测的增长。

![[assets/figures/papers/paper_list_l752_https_arxiv_org_abs_2604_00455/figures/002_Figure_2.jpg]]
*Figure 2: Comparison of the probability between all ground truth (left) and hallucination (right) words across token steps for each mitigation method. As sentence length increases, hallucinated word logits become more dominant; while VCD, ICD, and M3ID fail to suppress this trend, FLB (ours) effectively mitigates hallucinated predictions*

### 3.2 核心洞察：首个Token Logit的视觉锚定性质

FLB的方法论基础建立在一个关键观察之上：**首个生成token的logit（$l_0$）保留了最强的视觉信号**。由于 $l_0$ 紧接视觉token序列之后生成，其分布受视觉输入的直接影响最大，尚未受到长距离衰减的显著侵蚀。Figure 3 的个案分析表明，在首个token的logit中，真实物体词（如“man”）的logit值一致高于幻觉词（如“women”），验证了 $l_0$ 作为视觉锚点的可靠性。

![[assets/figures/papers/paper_list_l752_https_arxiv_org_abs_2604_00455/figures/003_Figure_3.jpg]]
*Figure 3: This figure shows the logits of the ground truth words (left) and hallucination words (middle) for the first token during caption generation for a case image (right). The logit of ground truth words are generally higher than that of hallucination words*

### 3.3 FLB的三大核心模块

FLB由三个协同工作的模块构成，形成完整的幻觉抑制流水线：

**模块一：首个Logit存储（First Logit Storage）**

在解码开始时，缓存首个生成token的原始logit向量：

$$l _ { 0 } = \operatorname { l o g i t } _ { \theta } ( y \mid x , v )$$

该向量在整个解码过程中保持不变，作为视觉锚定信号的基础载体。

**模块二：加权注入（Weighted Addition）**

在每个后续解码步 $t$，将存储的 $l_0$ 以时变权重 $w_t$ 添加到当前logit上：

$$y _ { t } \sim \mathrm { s o f t m a x } \Big [ \log \mathrm { i t } _ { \theta } ( y \mid v , x , y _ { < t } ) + w _ { t } l _ { 0 } \Big ]$$

时变权重函数设计为：

$$w _ { t } = \gamma ( 1 - e ^ { - \lambda t } )$$

其中 $\gamma$ 控制最大注入强度，$\lambda$ 控制权重增长速度。权重随 $t$ 单调递增的设计意图在于：随着解码深入、视觉衰减加剧，需要更强的 $l_0$ 信号来对抗语言先验的漂移。

**模块三：自适应合理性约束（Adaptive Plausibility Constraint）**

为防止 $l_0$ 的注入引入不合理token，FLB在softmax之前对候选token集合施加约束，仅保留原始模型概率不低于阈值 $\beta$ 倍最大概率的token：

$$\mathcal { V } _ { \mathrm { h e a d } } ( y _ { < t } ) = \{ y _ { t } \in \mathcal { V } : p _ { \theta } ( y _ { t } \mid v , x , y _ { < t } ) \geq \beta \underset { w } { \operatorname* { m a x } } p _ { \theta } ( w \mid v , x , y _ { < t } ) \}$$

该约束确保FLB只在模型原本认为“合理”的候选集中进行重排，避免因logit扰动产生语法错误或语义断裂。

### 3.4 完整解码规则

综合以上三个模块，FLB的最终解码规则为：

$$y _ { t } \sim \mathrm { s o f t m a x } \Big [ \log \mathrm { i t } _ { \theta } ( y \mid x , v , y _ { < t } ) + w _ { t } l _ { 0 } \Big ] , \mathrm { s u b j e c t ~ t o ~ } y _ { t } \in \mathcal { V } _ { \mathrm { h e a d } } ( y _ { < t } )$$

### 3.5 双重作用机制

FLB通过 $l_0$ 的注入同时激活两种互补的幻觉抑制机制：

1. **直接视觉接地（Direct Visual Grounding）**：$l_0$ 中真实物体词的高logit值直接提升后续token中对应物体的概率，为解码提供持续的视觉锚定。消融实验（Table 5）中通过仅保留 $l_0$ 中名词token的logit来隔离该效应，证实其独立有效。

2. **隐式视觉引用（Implicit Visual Referencing）**：Figure 4 显示首个token的logit中“The”等冠词排名极高，FLB因此提升了以“The”开头的句子比例（约+21.9个百分点）。Figure 6 进一步揭示，以“The”开头的句子在长距离token位置上的幻觉概率显著更低，表明“The”提供了稳定的初始化，抑制了累积性幻觉。

消融实验（Table 5）表明，两个效应各自独立有效（单独视觉接地 CHAIR=9.2，单独“The”效应 CHAIR=6.5），全开FLB达到最优性能（CHAIR=5.7），验证了双重机制的互补性。

## 实验与关键发现

### 核心实验结果

FLB在多个基准、多种模型架构上一致地大幅降低了物体幻觉。Table 1展示了AMBER生成任务上的主结果：以LLaVA1.5为骨干，FLB将CHAIR从Baseline的11.5降至**6.1**（降幅47%），Hal从48.9降至**31.6**，同时Cover和Cog也全面优于VCD、ICD和M3ID。在InstructBLIP上，FLB同样将CHAIR从11.6降至**9.0**，表现出跨模型泛化能力。

Table 2的MSCOCO-based CHAIR基准进一步验证了结论：LLaVA1.5上CHAIR_i从17.3降至**12.0**（降幅31%），CHAIR_s从49.3降至**43.5**。值得注意的是，Table 3显示FLB生成句子的平均词数和token数与Baseline无显著差异，排除了通过缩短输出“取巧”降低幻觉的可能性。

Table 4的GPT-4V辅助评估表明，FLB在精度、详细度和表达多样性三个维度上不仅未受损，反而有所提升。这一结果与Table 17中“The”首词比例上升约21.9个百分点的现象形成呼应——FLB改变了句子的起始分布，但并未损害生成质量。

### 消融实验：两种效应的独立验证

FLB的核心机制可分解为两个互补效应：**直接视觉接地**（仅保留l_0中名词token的logit）和**隐式视觉引用**（即“The”效应，仅保留l_0中冠词token的logit）。Table 5的消融结果揭示了二者的独立贡献与协同关系：

- 单独激活直接视觉接地：CHAIR为9.2，Cover为49.0
- 单独激活“The”效应：CHAIR为6.5，Cover为49.4
- 全开FLB：CHAIR达到最优的**5.7**，Cover为50.3

这表明两个效应各自有效且互补——直接视觉接地提供了视觉锚定，而“The”效应通过改变句子起始分布间接抑制了长距离衰减带来的幻觉增长。Figure 6从句子层面佐证了“The”效应的机制：以“The”开头的句子在后期token位置上的幻觉词概率显著低于其他句子，且这一差距随序列增长而扩大。

### 超参数分析与合理性约束

FLB引入三个关键超参数：γ（最大加权强度）、λ（权重增速）和β（合理性约束阈值）。Table 13和Table 14分别在LLaVA1.5和InstructBLIP上进行了网格搜索，默认值在两种模型上均有效，但最优值存在模型间差异，需要手动调整——这是该方法的一个实用限制。

自适应合理性约束（β）的作用尤为关键。Table 15显示，移除该约束（β=0）会导致句子中间异常插入“The”等token，因为l_0中冠词的logit在整个解码过程中被无差别地叠加。β=0.1被证明是在抑制幻觉和保持真实物体覆盖之间的最优平衡点。Figure 9提供了β过大或过小的定性示例，直观展示了不合理token的插入问题。

### 对比解码方法的系统性失效

Figure 2揭示了现有对比解码方法的共同瓶颈：随着序列增长，VCD、ICD和M3ID均无法抑制幻觉词logit的上升趋势，真实物体词的logit持续下降。这一长距离衰减（long-term decay）现象源于RoPE位置编码导致的视觉信息稀释，而FLB通过持续注入首个token的视觉信号，有效打破了这一衰减曲线。Figure 7在MMHalBench上的分析进一步印证：随着句子长度增加，其他方法的得分持续下降，而FLB保持了稳健的性能。

### 判别式任务的局限性

Table 19显示，在POPE、MME等判别式任务上，FLB等同于仅使用β-only（即不施加视觉接地，仅保留合理性约束）。这表明FLB的增益主要来自对长文本自回归生成过程的干预，而非对模型判别能力的根本性改变。这一局限性是方法设计的自然结果——首个token的logit在短答案或分类场景中无法发挥视觉锚定作用。

### 贪婪解码的适配性

Table 16比较了FLB在采样解码和贪婪解码下的表现。贪婪解码下CHAIR同样有效降低，但Cover略有下降，可能需要额外的超参数调整。这提示FLB的权重函数w_t和合理性约束在确定性解码下的行为与随机采样存在差异，需要针对具体解码策略进行微调。

### 推理效率

与需要两次前向传播的对比解码方法（VCD、ICD、M3ID）相比，FLB仅需缓存首个token的logit并在后续步骤中执行一次向量加法，推理速度几乎无退化。这一轻量特性使其在实际部署中具有显著优势。

![[assets/figures/papers/paper_list_l752_https_arxiv_org_abs_2604_00455/figures/011_Table_5.jpg]]
*Table 5: Ablation results isolating the two core effects of FLB*

![[assets/figures/papers/paper_list_l752_https_arxiv_org_abs_2604_00455/figures/024_Table_16.jpg]]
*Table 16: Performance comparison of LLaVA1.5 and greedy sampling on AMBER generative tasks. The highest scores are marked in bold*

## 定位与知识库关联

### 与对比解码方法的谱系关系

FLB 与当前主流的视觉对比解码（Visual Contrastive Decoding, VCD）、指令对比解码（Instruction Contrastive Decoding, ICD）以及多模态互信息解码（Multi-Modal Mutual-Information Decoding, M3ID）同属**解码端干预**范式——即不修改模型权重，仅在自回归采样阶段调整 logit 分布以抑制幻觉。然而，FLB 在干预机制上与上述方法存在根本性差异：

- **VCD** 通过对比原始图像 $v$ 与失真图像 $v'$ 的 logit 差异来放大视觉信号，其核心操作是 logit 减法：$p_{\mathrm{vcd}} \propto \mathrm{softmax}[(1+\alpha)\mathrm{logit}_\theta(y|v,x) - \alpha\,\mathrm{logit}_\theta(y|v',x)]$。该方法依赖额外的前向传播计算失真图像的 logit，推理开销约为基线的两倍。
- **ICD** 与 **M3ID** 同样遵循对比范式，分别在指令空间或互信息空间构造对比信号，均需要额外的模型前向计算。
- **FLB** 则采取**logit 加法**策略，将首个生成 token 的 logit $l_0$ 缓存后直接加权叠加到后续 token 的 logit 上：$y_t \sim \mathrm{softmax}[\mathrm{logit}_\theta(y|v,x,y_{<t}) + w_t l_0]$。这一设计仅需一次额外的 logit 存储与读取，不引入额外前向传播，因此推理速度几乎无衰减（Figure 5 区域）。

从效果上看，Figure 2 的 token 位置概率曲线揭示了关键差异：随着序列长度增加，VCD、ICD 和 M3ID 均无法阻止幻觉词 logit 的持续上升趋势，而 FLB 有效抑制了这一长距离衰减。这表明**基于对比的 logit 减法无法从根本上对抗语言先验随位置加深的累积效应**，而 FLB 通过注入早期视觉锚点实现了更持久的视觉接地。

### 与视觉接地方法的谱系关系

在视觉接地（visual grounding）这一更广泛的谱系中，FLB 的独特贡献在于**将接地信号的时间维度纳入设计**。现有方法多聚焦于空间维度的视觉-文本对齐（如注意力图约束、区域-短语匹配），或通过外部知识库进行事实校验。FLB 则揭示了**首个解码 token 的时间优先性**：由于 $l_0$ 在视觉 token 之后立即生成，受 RoPE 位置编码的长距离衰减影响最小，因此携带最强的视觉信号。这一洞察将“何时接地”提升到与“何处接地”同等重要的地位。

Figure 3 的案例分析为这一机制提供了直接证据：在首个 token 的 logit 中，真实物体词（如 “man”）的 logit 一致高于幻觉词（如 “women”），说明 $l_0$ 天然具备区分真实与幻觉物体的能力。Figure 4 进一步显示，首个 token 的 top-20 logit 中大量出现 “The”、“In”、“A” 等句子起始词，这为后续发现的“The 效应”埋下了伏笔。

### 适用边界

FLB 的有效性依赖于以下几个前提条件，这些条件同时界定了其适用范围：

1. **长文本生成场景**：FLB 的核心优势在于对抗长距离衰减，因此在需要多句生成的描述任务（如 AMBER、CHAIR、MMHalBench）上效果显著。在判别式任务（如 POPE、MME）上，由于不涉及长序列自回归生成，FLB 退化为仅使用自适应合理性约束（$\beta$-only），无额外增益（Table 19）。
2. **自回归解码框架**：FLB 的 logit 加法操作直接作用于自回归采样的中间 logit，对基于编码器-解码器或非自回归的生成架构不适用。
3. **模型无关但超参数敏感**：FLB 在 LLaVA1.5 和 InstructBLIP 上均有效，但需要手动设置三个超参数——最大权重 $\gamma$、增长速度 $\lambda$ 和合理性约束阈值 $\beta$。默认值（如 $\beta=0.1$）在两款模型上均表现良好，但跨模型泛化性仍需更大规模的验证。

### 局限与开放问题

**已知局限**：

- **风格多样性偏移**：FLB 使句子以 “The” 开头的比例上升约 21.9 个百分点。虽然 GPT-4V 评估表明精度、详细度和表达多样性未受损（Table 4），但这一分布偏移可能影响特定应用场景的风格需求。论文指出可通过调整 $\gamma$ 控制该效应强度。
- **贪婪解码下的覆盖度下降**：在贪婪解码模式下，FLB 的 Cover 指标略有下降（Table 16），可能需要在贪婪解码场景下进行额外的超参数微调。
- **判别式任务无增益**：如前所述，FLB 在非生成式评估中无额外贡献，限制了其作为通用幻觉缓解方案的适用性。

**开放问题**：

1. **与自适应 token 级视觉接地的结合**：当前 FLB 使用固定的 $l_0$ 作为全局锚点，是否可以将 $l_0$ 替换为动态更新的视觉接地信号，实现更细粒度的 token 级干预？
2. **RoPE 长距离衰减的根本性解决**：FLB 本质上是对 RoPE 位置编码衰减效应的补偿性修复，而非根治。能否通过衰减感知的位置编码机制从模型结构层面解决这一问题？
3. **跨语言与多模态对话的泛化**：FLB 的 “The 效应” 高度依赖英语的冠词系统。在无冠词语言（如中文、日语）或多轮对话场景中，首个 token 的视觉接地作用是否依然成立？
4. **贪婪解码的覆盖度保持**：如何在保持 FLB 幻觉抑制能力的同时，避免贪婪解码下的覆盖度损失？是否需要引入额外的多样性促进机制？

## 原文 PDF

![[paperPDFs/CVPR_2026/First_Logit_Boosting_Visual_Grounding_Method_to_Mitigate_Object_Hallucination_in_Large_Vision_Language_Models.pdf]]
