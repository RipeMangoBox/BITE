---
title: "Machine Mental Imagery: Empower Multimodal Reasoning with Latent Visual Tokens"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Machine_Mental_Imagery_Empower_Multimodal_Reasoning_with_Latent_Visual_Tokens.pdf
project_link: "https://vlm-mirage.github.io"
code_link: "https://github.com/UMass-Embodied-AGI/Mirage"
aliases:
- MMIEMRLVT
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 在文本解码流中插入“隐式视觉令牌”（latent visual tokens），作为紧凑的视觉嵌入，代替显式图像生成，使模型进行多模态交织推理。
primary_logic: 受人类心理意象启发，利用两阶段训练使VLM能够内部生成并利用压缩的视觉特征（而非像素），同时通过强化学习对齐任务目标，从而提升推理能力。
claims:
- 两阶段训练消融：仅第二阶段（无视觉锚定）性能从0.58降至0.21，证明第一阶段视觉锚定不可或缺。
- 与统一模型Anole和MVoT相比，Mirage在相同数据量下性能大幅领先（VSP推理 0.87 vs 0.61），且无需显式图像生成。
- t-SNE可视化显示隐式令牌聚集在视觉子空间附近但略有分离，符合两阶段训练的设计意图。
- 加入RL后性能进一步提升（VSP推理+2%），表明强化学习可以进一步对齐多模态推理轨迹。
---

# Machine Mental Imagery: Empower Multimodal Reasoning with Latent Visual Tokens

> [!tip] 核心洞察
> 受人类心理意象启发，利用两阶段训练使VLM能够内部生成并利用压缩的视觉特征（而非像素），同时通过强化学习对齐任务目标，从而提升推理能力。

| 字段 | 内容 |
|------|------|
| 中文题名 | 机器心理意象：以隐式视觉令牌增强多模态推理 |
| 英文题名 | Machine Mental Imagery: Empower Multimodal Reasoning with Latent Visual Tokens |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2506.17218) · [Project](https://vlm-mirage.github.io) · [Code](https://github.com/UMass-Embodied-AGI/Mirage) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Mirage |
| Dataset | VSP Spatial Reasoning, VSP Spatial Planning, COMT Geometry, Jigsaw |

> [!tip] 效果简介
> - VSP Spatial Reasoning (average) 上，Accuracy 0.87 (Ours CoT) vs 0.85 (CoT SFT+GRPO) (+0.02)。
> - VSP Spatial Planning (average) 上，Accuracy 0.58 (Ours CoT) vs 0.51 (CoT SFT+GRPO) (+0.07)。
> - COMT Geometry 上，Accuracy 0.77 (Ours) vs 0.75 (CoT SFT) (+0.02)。

## 概要

**问题瓶颈**：当前视觉语言模型（VLM）在多模态推理任务（如空间推理、规划）中，解码过程完全依赖纯文本序列。人类在解决此类问题时，能够在“心理意象”中进行视觉操作与想象，而VLM缺乏这种内部视觉表征能力，导致推理性能受限。

**核心洞察**：受人类心理意象启发，**Mirage** 提出在文本解码流中插入“隐式视觉令牌”（latent visual tokens）——即模型当前隐藏状态的紧凑视觉嵌入，跳过语言投影头直接作为上下文，使模型能够进行文本与视觉交织的多模态推理，而无需生成完整像素级图像。

**方法定位**：Mirage 采用**两阶段训练范式**（Figure 2）：第一阶段联合监督文本交叉熵损失与隐式令牌的余弦相似度损失，将隐式令牌锚定在视觉子空间中；第二阶段移除视觉监督，仅保留文本损失，使模型自回归生成隐式令牌并通过梯度优化。训练数据通过为每个样本合成辅助图像，并由大VLM生成嵌入该图像的交织推理链获得（Figure 3）。在此基础上，可进一步通过**GRPO强化学习**以格式正确性和答案正确性为奖励进行微调。

**主要结果**：
- 在 **VSP 空间推理**任务上，Mirage（CoT）达到 **0.87** 平均准确率，超越纯文本 CoT SFT+GRPO 基线（0.85），并大幅领先统一多模态模型 MVoT（0.61）和 Anole。
- 在 **VSP 空间规划**任务上，Mirage 达到 **0.58**，相比纯文本强基线（0.51）提升 +0.07。
- 在 **COMT 几何**（0.77）、**Jigsaw 拼图**（0.88）、**SAT 现实**（0.72）等任务上，均一致超越 CoT SFT 基线（+0.02 至 +0.06）。
- 消融实验表明，移除第一阶段视觉锚定后性能从 0.58 骤降至 0.21，验证了视觉 grounding 的不可或缺性；t-SNE 可视化证实隐式令牌聚集在视觉子空间附近，与两阶段设计意图一致（Figure 7）。

**方法谱系与知识库定位**：Mirage 区别于两类现有方案——纯文本推理基线（Zero-Shot、CoT SFT、GRPO 等）缺乏视觉想象能力，而统一多模态模型（如 **Anole**，Chern et al., 2024；**MVoT**，Li et al., 2025a）需生成完整图像，推理性能受限且计算开销大。Mirage 以紧凑的隐式向量替代显式图像生成，在相同数据量下实现更优性能，为多模态推理提供了一种高效、可扩展的中间表征方案。



### 多模态推理中的视觉想象瓶颈

视觉语言模型（VLM）在多数基准测试中已展现强大能力，但在需要**空间推理**和**视觉想象**的任务上仍存在显著短板。这类任务要求模型在推理过程中对空间关系、物体移动或几何变换进行内部模拟——这一认知过程在人类中对应“心理意象”（Mental Imagery）：人们能够在脑海中构建并操作视觉表征，而无需实际看到图像。

然而，当前主流VLM的推理机制存在根本性局限：模型在解码阶段仅生成**纯文本序列**，缺乏对视觉信息进行内部表征和操作的能力。当面对“从起点出发，向东走两步，再向南走一步，最终位置在哪？”这类空间推理问题时，纯文本解码迫使模型将视觉操作“翻译”为语言描述，丧失了视觉空间的直观性和并行处理优势。这一瓶颈在**VSP空间规划**任务上尤为突出——即使采用链式思维监督微调加GRPO强化学习的最强纯文本基线，准确率也仅为0.51。

### 现有方案的困境：显式生成 vs. 纯文本推理

为弥补上述缺口，近期工作尝试了两种路径，但均存在结构性缺陷：

- **统一多模态生成模型**（如**Anole**, Chern et al., 2024；**MVoT**, Li et al., 2025a）：让模型在推理过程中显式生成图像，将视觉信息以像素形式输出。然而，图像生成本身是极高维度的重建任务，与推理目标存在本质张力——模型被迫消耗大量容量在像素级细节上，而非专注于推理逻辑。实验表明，在相同数据量下，MVoT在VSP空间推理上的准确率仅为0.61，远低于纯文本强基线（0.85），说明显式生成路径反而损害了推理质量。

- **纯文本推理增强**（如CoT SFT、GRPO）：通过链式思维微调或强化学习优化文本推理链。虽然性能稳定，但始终受限于文本模态的表达能力——空间关系的描述天然比视觉表征更冗长、更易出错。

### 核心动机：以隐式视觉令牌实现“机器心理意象”

本文的核心洞察来源于对人类认知的类比：心理意象的有效性在于其**紧凑性**和**可操作性**——我们并非在脑海中生成高清照片，而是保留关键的视觉特征用于推理。受此启发，Mirage提出了一种新的解码机制：在文本推理链中插入**隐式视觉令牌**（latent visual tokens），作为压缩的视觉嵌入，使模型能够在“心理意象”空间中进行多模态交织推理，而无需生成完整图像。

这一设计的因果逻辑链如下：
1. **瓶颈识别**：VLM在视觉推理任务上受限于纯文本解码，无法像人类一样操作视觉表征。
2. **因果调节变量**：在解码流中插入紧凑的视觉嵌入，代替显式图像生成，为模型提供可操作的视觉工作空间。
3. **核心机制**：当模型选择进行视觉推理时，生成一个特殊令牌，随后将其当前隐藏状态作为压缩视觉嵌入追加到上下文中，跳过语言投影层，直接进入后续推理。

这种设计的关键优势在于：隐式令牌的维度远低于像素图像（实验中仅使用k=4个令牌向量），使模型能将容量集中在推理逻辑上，同时保留了视觉空间的表征能力。t-SNE可视化（Figure 7）证实，训练后的隐式令牌聚集在视觉嵌入子空间附近但略有分离，表明它们确实承载了视觉信息，同时保持了作为“推理中间件”的灵活性。



## 核心方法与创新机理

### 问题瓶颈：VLM在视觉想象任务中的模态缺失

当前视觉语言模型（VLM）在多模态推理任务中面临一个根本性瓶颈：当任务需要“在脑中想象画面”时（如空间推理、几何变换、拼图重组），模型被迫以纯文本形式进行解码。这种模态约束使得VLM无法像人类那样在心理意象中进行视觉操作，导致推理性能受限。现有的纯文本基线方法（如Chain-of-Thought SFT、GRPO强化学习）虽然在文本推理链上表现良好，但始终无法填补视觉想象这一认知鸿沟。

### 核心洞察：以隐式视觉令牌替代显式图像生成

Mirage的核心创新受人类心理意象（Mental Imagery）启发：**在文本解码流中插入紧凑的隐式视觉令牌（latent visual tokens），使模型能够进行多模态交织推理，而无需生成完整像素图像。** 这一设计的关键在于：

- **压缩表示而非像素重建**：当模型选择进行视觉推理时，它复用当前隐藏状态作为紧凑的视觉嵌入，跳过语言投影头，直接将其作为隐式令牌追加到上下文中。这避免了显式图像生成的高昂计算成本和信息损失。
- **交织推理轨迹**：隐式令牌与普通文本令牌交替出现，形成“文本→视觉想象→文本”的自然推理流，使模型能够在语言推理和视觉想象之间灵活切换。

### Changed Slots：相对基线的方法创新

Mirage相对现有方法在以下关键维度上进行了系统性创新：

| 创新维度 | 基线方法 | Mirage方法 | 证据锚点 |
|---------|---------|-----------|---------|
| **推理轨迹中的模态** | 纯文本序列（CoT SFT、GRPO等） | 文本与隐式视觉令牌交织的序列 | Sec. 3.2, 3.3 |
| **视觉信息的表示形式** | 无需表示，或生成完整图像（Anole、MVoT） | 通过压缩图像嵌入获取的k个隐式向量（平均池化） | Sec. 3.2, Eq. 1 |
| **训练范式** | 单阶段文本监督微调 | 两阶段：第一阶段联合文本和视觉对齐损失，第二阶段仅文本损失释放隐式令牌 | Fig. 2, Sec. 3.2-3.3 |
| **视觉损失函数** | 无，或图像生成损失（如扩散模型损失） | 余弦相似度损失，用于对齐隐式令牌和压缩图像嵌入 | Eq. 1 |

### 与统一多模态模型的本质区别

Mirage与Anole（Chern et al., 2024）和MVoT（Li et al., 2025a）等统一多模态模型的关键区别在于**视觉表示的选择**：

- **Anole/MVoT**：生成完整图像，需要外部视觉解码器（如扩散模型），计算成本高且推理链中缺乏显式的视觉推理思路。
- **Mirage**：在VLM的嵌入空间内直接操作隐式视觉令牌，无需外部解码器。实验表明，在相同数据量（约1k SFT样本）下，Mirage在VSP空间推理任务上达到0.87准确率，大幅领先MVoT的0.61（+0.26）和Anole（具体数值需查Table 1确认）。

### 两阶段训练：视觉锚定与任务适配的协同

Mirage的训练策略是实现隐式视觉推理的关键使能技术：

1. **第一阶段（视觉锚定）**：使用辅助图像的压缩特征作为目标，通过余弦相似度损失将隐式令牌“锚定”在视觉子空间中。消融实验显示，移除该阶段后VSP空间规划性能从0.58骤降至0.21，证明视觉grounding不可或缺。
2. **第二阶段（任务适配）**：移除余弦损失，仅用文本交叉熵损失，让模型自回归生成隐式令牌并通过梯度优化使其适应具体任务需求。t-SNE可视化（Figure 7）证实，隐式令牌聚集在视觉子空间附近但略有分离，符合两阶段训练的设计意图——先锚定后释放。

### 强化学习的增量收益

在GRPO强化学习阶段，Mirage以格式正确性和答案准确性为奖励信号，进一步对齐多模态推理轨迹。实验表明，加入RL后VSP空间推理性能额外提升约2%（Table 1），证明强化学习可以在监督微调基础上进一步优化交织推理的质量。



Mirage 的整体框架围绕一个核心思想构建：在 VLM 的文本解码流中插入紧凑的**隐式视觉令牌**（latent visual tokens），使模型能够像人类“心理意象”一样进行多模态交织推理，而无需生成完整的像素级图像。整个系统由三个关键模块串联而成：**数据生成流水线**、**两阶段监督训练**和**可选的强化学习微调**。

### 数据生成流水线

训练数据的构造是框架的起点。对于每个“问题–答案”对，系统首先利用任务特定工具生成一张**辅助图像**（helper image）——例如在 VSP 空间推理任务中，工具会在原始地图上标注箭头和路径；在 SAT 几何任务中，则依赖 CogVideoX-5B 等生成模型合成参考图。随后，系统提示一个大型推理 VLM（如 Qwen2.5-VL 32B），要求其生成一段**嵌入该辅助图像的文本推理链**。推理链被自然切分为辅助图像之前的部分 $o_{\text{pre}}$ 和之后的部分 $o_{\text{post}}$，形成“文本–图像–文本”的交织结构。这一流程产出的每条训练样本包含输入 $x$、辅助图像 $I$、交织推理链 $o$ 和正确答案 $y$，为后续两阶段训练提供了多模态监督信号（Figure 3）。

![[assets/figures/papers/paper_list_l2325_https_arxiv_org_abs_2506_17218/figures/003_Figure_3.jpg]]
*Figure 3: Data-generation Pipeline. For each question–answer pair, we first create a helper image with task-specific tools (here, annotate the map with arrows), then prompt a VLM to produce textual reasoning that embeds this image. The text and helper image together form the synthetic multimodal trajectory used for training*

### 两阶段监督训练

Mirage 的核心训练范式分为两个阶段，分别解决“隐式令牌锚定”和“自回归生成”两个子问题（Figure 2）。

![[assets/figures/papers/paper_list_l2325_https_arxiv_org_abs_2506_17218/figures/002_Figure_2.jpg]]
*Figure 2: Pipeline of Mirage Framework. Stage 1 jointly supervises text and latent visual tokens, grounding the latter in the visual subspace; Stage 2 drops the latent supervision, anchoring the grounded latent tokens for subsequent text generation*

**第一阶段：联合视觉锚定。** 模型在生成推理链时，当遇到原本嵌入辅助图像的位置，改为生成 $k$ 个隐式视觉令牌。这些隐式令牌的训练目标并非像素重建，而是与辅助图像的压缩视觉特征对齐。具体而言，系统将辅助图像经 VLM 视觉编码器提取的 patch 特征通过平均池化压缩为 $k$ 个显著向量 $\{\bar{e}_j\}_{j=1}^k$，作为隐式令牌的 ground-truth 目标。第一阶段的损失函数由两部分组成：

$$ \mathcal{L}_1 = \mathcal{L}_{\text{visual}} + \gamma \mathcal{L}_{\text{text}} $$

其中视觉对齐损失为余弦相似度：

$$ \mathcal{L}_{\text{visual}} = \ell_{\cos}\big(\hat{e}_j, g_\theta(o_{\text{pre}}, \hat{e}_{1:j-1})\big) $$

迫使模型生成的隐式令牌 $\hat{e}_j$ 逼近压缩图像嵌入。文本交叉熵损失 $\mathcal{L}_{\text{text}}$ 则同时覆盖辅助图像前后的文本令牌，确保语言推理能力不被削弱。系数 $\gamma$ 用于平衡两个目标（默认 $\gamma=0.1$）。这一阶段的关键作用是将隐式令牌“锚定”在 VLM 的视觉表示子空间内，赋予其视觉语义。

**第二阶段：释放隐式令牌。** 第二阶段移除了视觉对齐损失，仅保留文本交叉熵损失。此时模型完全自回归地生成隐式令牌 $e_j = f_\theta(x, o_{\text{pre}}, e_{<j})$，不再依赖外部压缩图像作为目标。梯度通过隐式令牌反向传播，使模型能够根据下游任务自主调整隐式令牌的内容。这一设计使得隐式令牌在第一阶段获得的视觉锚定基础上，进一步适应具体的推理需求。消融实验表明，两个阶段缺一不可：仅保留第二阶段（无视觉锚定）时，VSP 空间规划任务的准确率从 0.58 骤降至 0.21，证明了第一阶段视觉 grounding 的不可或缺性（Figure 4）。

### 强化学习微调

在两阶段监督训练之后，Mirage 可选地引入**群组相对策略优化**（GRPO）进行强化学习微调。奖励函数由两部分组成：格式奖励（确保模型输出符合规范的推理格式）和正确性奖励 $r_{\text{acc}}(o, x)$——当最终答案正确时为 1，否则为 0。加入 RL 后，VSP 空间推理和空间规划任务分别获得额外 +2% 和 +7% 的提升，表明强化学习能够进一步对齐多模态推理轨迹与任务目标。

### 输入输出流

推理时，Mirage 的输入为标准的多模态输入（文本指令与可选的视觉输入），输出为**文本与隐式视觉令牌交织的序列**。当模型判断需要“视觉思考”时，它会生成一个特殊令牌，随后将当前隐藏状态作为紧凑的视觉嵌入直接追加到上下文中，跳过语言投影层。这些隐式令牌在 t-SNE 可视化中聚集在视觉表示子空间附近但略有分离（Figure 7），与两阶段训练的设计意图一致——它们携带视觉信息，但已根据任务进行了适应性调整。最终，模型基于这些交织的隐式令牌和文本令牌生成答案，实现了无需外部解码器的多模态推理闭环。



Mirage 框架的核心由三个训练模块构成，围绕“隐式视觉令牌”这一关键设计展开。

**隐式视觉令牌机制。** 模型在解码过程中，当需要“视觉想象”时，生成一个特殊令牌，随后将当前隐藏状态作为紧凑的视觉嵌入直接追加到上下文中，跳过语言投影层。这一机制使模型能够在不生成像素级图像的情况下，进行文本与视觉特征交织的多模态推理。

**模块一：第一阶段联合监督训练。** 该阶段将隐式令牌锚定在视觉子空间中。对于训练数据中的辅助图像，首先通过视觉编码器提取其patch特征，经平均池化压缩为 $k$ 个显著向量作为目标嵌入。模型在生成隐式令牌时，通过余弦相似度损失将其拉向目标嵌入：

$$\mathcal{L}_{\mathrm{visual}} = \ell_{\cos}\Big(\hat{e}_j, g_\theta\big(o_{\mathrm{pre}}, \hat{e}_{1:j-1}\big)\Big)$$

其中 $\hat{e}_j$ 为压缩后的目标视觉嵌入，$g_\theta$ 为模型基于前文上下文对第 $j$ 个隐式令牌的预测。同时，文本部分通过交叉熵损失进行优化：

$$\mathcal{L}_{\mathrm{text}} = \sum_{i=1}^{|o_{\mathrm{pre}}|} \ell_{\mathrm{CE}}(o_{\mathrm{pre},i}, f_\theta(\boldsymbol{x}, o_{\mathrm{pre},<i})) + \sum_{i=1}^{|o_{\mathrm{post}}|} \ell_{\mathrm{CE}}(o_{\mathrm{post},i}, f_\theta(\boldsymbol{x}, o_{\mathrm{pre}}, \{\hat{e}_j\}_1^k, o_{\mathrm{post},<i}))$$

总损失为 $\mathcal{L}_1 = \mathcal{L}_{\mathrm{visual}} + \gamma \mathcal{L}_{\mathrm{text}}$，其中 $\gamma$ 为平衡系数。

**模块二：第二阶段纯文本监督训练。** 移除余弦相似度损失，模型自回归生成隐式令牌：

$$e_j = f_\theta(x, o_{\mathrm{pre}}, e_{<j})$$

文本损失 $\mathcal{L}_{\mathrm{text}}$ 使用自生成的隐式令牌 $\{e_j\}_1^k$ 替代目标嵌入 $\{\hat{e}_j\}_1^k$，梯度可反向传播至隐式令牌，使其在保持视觉锚定的同时自适应任务需求。

**模块三：强化学习微调。** 采用 GRPO（Group Relative Policy Optimization）进行策略优化。奖励函数包含格式奖励和正确性奖励，其中正确性奖励定义为：

$$r_{\mathrm{acc}}(\pmb{o}, \pmb{x}) = 1$$

当最终答案正确时取1，否则为0。该阶段进一步对齐多模态推理轨迹与任务目标。

### 补充图表

![[assets/figures/papers/paper_list_l2325_https_arxiv_org_abs_2506_17218/figures/001_Figure_1.jpg]]
*Figure 1: Multimodal Reasoning Examples. Mirage interleaves latent visual tokens, which represent compact imagery visual features, with explicit text tokens to solve diverse spatial reasoning multimodal tasks, boosting the reasoning performance without the full pixel-level image generation*

![[assets/figures/papers/paper_list_l2325_https_arxiv_org_abs_2506_17218/figures/010_Figure_7.jpg]]
*Figure 7: Visualization of Latent Embeddings. We visualize our latent tokens along with text and image embeddings with t-SNE. Our latent tokens cluster near, yet just outside, the visual representation subspace, consistent with the two-stage training design*



## 实验与关键发现

### 主实验结果

Mirage在多个空间推理基准上均取得了一致且显著的提升。在VSP基准上（Table 1），Mirage（CoT）在空间推理任务上达到平均准确率0.87，较最强纯文本基线CoT SFT+GRPO（0.85）提升2个百分点；在空间规划任务上达到0.58，较同一基线（0.51）提升7个百分点。即使不采用链式思维，Mirage（Direct）也分别达到0.86和0.76，大幅领先直接使用合成数据微调的纯文本方法（空间推理+3%，空间规划+11%）。

![[assets/figures/papers/paper_list_l2325_https_arxiv_org_abs_2506_17218/figures/004_Table_1.jpg]]
*Table 1: Experimental Results on Visual-Spatial Planning (VSP) tasks*

与统一多模态模型相比，Mirage的优势更为突出。在相同数据量（约1k SFT样本）下，Mirage（CoT）在VSP空间推理上以0.87对0.61领先**MVoT**（Li et al., 2025a），差距达26个百分点；同时显著优于**Anole**（Chern et al., 2024）。这验证了隐式视觉令牌相比显式图像生成在推理效率和质量上的优势。

在COMT、Jigsaw和SAT任务上（Table 2），Mirage同样全面超越纯文本基线。以CoT SFT为参照，Mirage在COMT几何推理上提升2%（0.77 vs 0.75），在Jigsaw拼图推理上提升5%（0.88 vs 0.83），在SAT真实图像推理上提升6%（0.72 vs 0.66）。在Qwen2.5-VL 3B上的扩展实验（Table 3）进一步验证了方法的跨模型泛化能力，Mirage在多个任务上相较纯文本基线提升5%-10%。

![[assets/figures/papers/paper_list_l2325_https_arxiv_org_abs_2506_17218/figures/005_Table_2.jpg]]
*Table 2: Experimental Results on COMT, Jigsaw, and SAT tasks*

![[assets/figures/papers/paper_list_l2325_https_arxiv_org_abs_2506_17218/figures/006_Table_3.jpg]]
*Table 3: Experimental Results with Qwen2.5-VL 3B on COMT, Jigsaw, and SAT tasks*

### 消融研究

**两阶段训练的必要性**（Figure 4/Table 4）是本文最关键的消融发现。在VSP空间规划任务上，仅使用第二阶段训练（无视觉锚定）时性能骤降至0.21，而完整两阶段达到0.58。仅第一阶段训练同样无法达到最优性能，证明两个阶段协同工作不可或缺：第一阶段将隐式令牌锚定在视觉子空间，第二阶段释放其适应任务的能力。值得注意的是，仅第二阶段训练虽优于纯文本基线，但仍远不及完整流程，这印证了VLM中文本与视觉子空间的异质性——缺乏显式视觉锚定的隐式令牌难以自发形成有效的视觉表示。

**隐式令牌数量k**（Figure 5/Table 5）的消融显示，k在2-6范围内性能稳定（0.86-0.88），表现出良好的鲁棒性。但当k增至8时，准确率降至0.75，下降约13%。这表明过多的隐式令牌可能引入冗余或优化困难，当前设计在表示能力上存在上限。

**损失系数γ**（Figure 5/Table 5）对最终性能影响适中。不同γ值下第二阶段后模型均能达到80%以上精度，但γ过大（相当于弱化视觉监督）会导致第一阶段效果不佳。这进一步支持了视觉锚定在初始阶段的关键作用。

### 强化学习的增益

加入GRPO强化学习后（Table 1），Mirage在VSP空间推理和规划任务上分别获得额外+2%的提升，表明基于格式和正确性的奖励信号可以进一步对齐多模态推理轨迹。这一增益叠加在SFT基础上，验证了RL作为第三阶段优化的有效性。

### 隐式令牌的几何解释

t-SNE可视化（Figure 7）为隐式令牌的行为提供了直观解释。隐式令牌的嵌入聚集在视觉表示子空间附近，但略有分离。这与两阶段训练的设计意图一致：第一阶段通过余弦相似度损失将令牌拉向压缩图像嵌入，第二阶段释放约束使其在任务优化中微调位置，从而在“保持视觉信息”和“适应文本推理”之间取得平衡。

### 辅助图像的信息量验证

为验证合成辅助图像的质量，作者将辅助图像作为输入先验进行测试（Figure 6）。在零样本和微调设置下，使用辅助图像作为输入的模型性能均显著提升，表明生成的图像包含有效的空间信息，数据生成流程产出的多模态轨迹具有高质量。

![[assets/figures/papers/paper_list_l2325_https_arxiv_org_abs_2506_17218/figures/008_Figure_6.jpg]]
*Figure 6: Performance with Helper Images as Input Priors. We evaluate model accuracy using synthesized helper images under both zero-shot and fine-tuned settings. The results highlight the informativeness of the generated images and confirm their high data quality*

### 失败模式与局限

尽管Mirage在空间推理上表现优异，但存在以下局限：

1. **合成数据质量瓶颈**：推理链由Qwen2.5-VL 32B生成，偶尔产生次优路径，限制了性能上限。SAT等任务的辅助图像依赖CogVideoX-5B生成，缺乏真实标注，可能引入噪声。
2. **任务泛化未验证**：当前实验集中于空间推理基准（VSP、COMT、Jigsaw、SAT），框架在更广泛多模态任务上的有效性尚待检验。
3. **隐式令牌容量限制**：k=8时性能显著下降，表明当前设计的表示能力有限，难以承载更复杂的视觉信息。
4. **数据生成依赖特定工具**：辅助图像创建依赖任务特定的工具（如OpenAI Gym、视频生成模型），向新任务扩展可能需要额外工程。

### 补充图表

![[assets/figures/papers/paper_list_l2325_https_arxiv_org_abs_2506_17218/figures/007_Figure_4.jpg]]
*Figure 4: Ablation Study of Training Stages on VSP Spatial Planning task. Both training stages work jointly to achieve better reasoning performance*

![[assets/figures/papers/paper_list_l2325_https_arxiv_org_abs_2506_17218/figures/009_Figure_5.jpg]]
*Figure 5: Ablation Study of Latent Size k and Loss Coefficient γ on VSP Spatial Reasoning. Our training pipeline remains robust and superior performance across different hyperparameters*

![[assets/figures/papers/paper_list_l2325_https_arxiv_org_abs_2506_17218/figures/015_Table_5.jpg]]
*Table 5: Data Example of VSP Spatial Planning*



## 定位与知识库关联

### 核心问题与设计动机

当前多模态大模型（VLM）在空间推理等需要“视觉想象”的任务中，其解码过程被限制在纯文本空间。人类在解决此类问题时，会借助“心理意象”（mental imagery）在视觉空间中操作——这正是VLM所缺失的能力。**Mirage** 的核心动机在于：**在文本解码流中插入紧凑的隐式视觉令牌**，使模型能够进行文本与视觉特征交织的多模态推理，而无需生成完整像素级图像。

### 与现有方法的谱系关系

#### 纯文本推理基线（同谱系上游）

Mirage 直接对标的基线是当前VLM的主流推理范式——纯文本链式思维（CoT）微调。这些方法在推理过程中仅输出文本令牌，无法利用视觉空间的表征优势：

- **Zero-Shot / Direct SFT / CoT SFT**：未经微调或仅用文本标签微调的基础VLM，构成性能下界。
- **CoT SFT + GRPO**：链式思维微调后叠加强化学习（GRPO），是当前纯文本推理的最强基线。在VSP空间推理任务上达到0.85（CoT SFT+GRPO），而Mirage（CoT）达到0.87，提升+2%；在空间规划任务上，Mirage以0.58领先0.51达+7个百分点（Table 1）。这表明**隐式视觉令牌的引入在纯文本强基线之上仍能提供增益**。

#### 统一多模态生成模型（同谱系平行）

另一类相关工作试图让模型同时生成图像和文本，形成显式的多模态推理轨迹。Mirage 与这类方法共享“多模态交织推理”的目标，但在实现路径上有本质差异：

- **Anole**（Chern et al., 2024）：统一多模态模型，同时生成图像和文本。在相同数据量（约1k SFT样本）下，其在VSP空间推理上的性能为0.61，远低于Mirage的0.87（Table 1）。显式图像生成不仅计算开销大，且推理质量受限于图像解码器的能力。
- **MVoT**（Li et al., 2025a）：生成动作和状态图像的统一模型，原论文使用6,846训练样本。为保证公平比较，本文将其复现时缩减至1,000样本——尽管复现结果略低于原论文，Mirage仍以0.87 vs 0.61显著领先（Table 1）。MVoT缺少显式推理思路，其生成的图像序列难以形成连贯的逻辑链。

**Mirage 的关键区分点**在于：不生成像素，而是生成压缩的隐式视觉嵌入（k个向量，通过平均池化从辅助图像特征中提取）。这避开了图像解码器的瓶颈，同时保留了视觉空间的表征能力。

#### 强化学习微调（同谱系下游）

在监督微调之后，Mirage 采用 **GRPO**（Group Relative Policy Optimization）进行强化学习微调，以格式正确性和答案正确性为奖励信号。这一步骤与纯文本基线的GRPO微调形成对照：Mirage在加入GRPO后，VSP空间推理性能进一步提升+2%（Table 1），表明强化学习可以进一步对齐多模态交织推理轨迹。

### 方法适用边界

基于当前实验证据，Mirage的适用边界可归纳如下：

1. **任务类型边界**：目前验证集中于空间推理基准（VSP、COMT Geometry、Jigsaw、SAT），框架在更广泛的多模态任务（如视觉问答、视频理解）上的泛化性尚未验证。这是未来工作的重要方向。

2. **隐式令牌容量边界**：隐式令牌数量k在2-6范围内性能稳定（VSP空间推理0.86-0.88），但k=8时性能骤降至0.75（下降约13%，Figure 5消融）。这表明当前设计在视觉信息压缩的表示能力上仍有局限，过大的令牌数量可能引入噪声或优化困难。

3. **数据依赖边界**：合成推理链的质量受制于教师模型 Qwen2.5-VL 32B，偶尔产生次优推理路径，限制了性能上限。SAT等任务的辅助图像依赖生成模型 CogVideoX-5B，缺乏真实标注，可能引入噪声。

4. **训练范式边界**：两阶段训练中，第一阶段（视觉锚定）是不可或缺的——仅第二阶段训练的性能从0.58降至0.21（Table 4 / Figure 4），证明视觉grounding的必要性。这同时暗示：VLM中文本与视觉子空间存在异质性，隐式令牌需要显式的视觉对齐才能有效工作。

### 局限与开放问题

#### 已识别的局限

1. **合成数据质量上限**：数据生成流程依赖特定任务的工具（如OpenAI Gym、视频生成模型CogVideoX-5B），对新任务的扩展需要额外设计。合成推理链的质量受限于教师模型，可能产生次优轨迹。

2. **表示能力瓶颈**：k=8时性能显著下降，表明当前压缩机制在表示复杂视觉信息时存在瓶颈。

3. **任务覆盖面窄**：实验限于空间推理基准，在其他多模态任务上的有效性未经检验。

#### 开放问题

1. **任务泛化**：如何将隐式视觉令牌的生成能力扩展到更广泛的多模态甚至纯文本任务？是否可以在不依赖辅助图像的情况下，通过预训练或自监督方式习得隐式视觉令牌的生成能力？

2. **统一模型的对齐空间利用**：统一多模态模型（如Anole、MVoT）的对齐特征空间是否可以被利用来进一步改善隐式推理设计？当前Mirage的隐式令牌在t-SNE可视化中聚集在视觉子空间附近但略有分离（Figure 7），这是否暗示存在更优的对齐策略？

3. **训练轨迹质量提升**：开发更丰富的提示策略或策划更高质量的训练轨迹，以突破当前教师模型的质量上限，仍是未来工作的重要方向。

4. **推理效率与质量的权衡**：隐式令牌的引入增加了序列长度，如何在保持推理质量的同时控制计算开销，尚未被系统研究。



## 原文 PDF

![[paperPDFs/CVPR_2026/Machine_Mental_Imagery_Empower_Multimodal_Reasoning_with_Latent_Visual_Tokens.pdf]]
