---
title: "Vision-Language-Action Instruction Tuning: From Understanding to Manipulation"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Vision_Language_Action_Instruction_Tuning_From_Understanding_to_Manipulation.pdf
openreview_forum_id: tsxwloasw5
aliases:
- VLAITFUM
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/vision_models_multimodal
core_operator: "两阶段训练与混合专家（MoE）适应机制。Stage-1通过语言运动监督预训练动作专家，将低层控制与VLM解耦；Stage-2通过可切换的LoRA专家和标量头动态融合多模态推理与潜在动作生成，实现推理增强的操控。"
primary_logic: "利用潜在动作查询作为中间表征，将VLM的异步自回归推理与基于流匹配的动作专家解耦。MoE适应让模型在语言推理和潜在动作预测之间自适应切换，从而既保留VLM的通用多模态能力，又能在推理过程中注入任务相关知识以提升操控表现。"
claims:
- "在SimplerEnv封闭式操控中，InstructVLA-Expert比SpatialVLA提升33%。"
- "在SimplerEnv-Instruct基准上，InstructVLA-Generalist相比微调的OpenVLA提升96%。"
- "移除动作专家中的DINOv2视觉编码器导致50%的性能下降。"
- "为通用模型启用推理（thinking）相比直接执行指令带来36.1%的性能增益。"
---

# Vision-Language-Action Instruction Tuning: From Understanding to Manipulation

> [!tip] 核心洞察
> 利用潜在动作查询作为中间表征，将VLM的异步自回归推理与基于流匹配的动作专家解耦。MoE适应让模型在语言推理和潜在动作预测之间自适应切换，从而既保留VLM的通用多模态能力，又能在推理过程中注入任务相关知识以提升操控表现。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 视觉-语言-动作指令微调：从理解到操控 |
| 英文题名 | Vision-Language-Action Instruction Tuning: From Understanding to Manipulation |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=tsxwloasw5); [Project](https://yangs03.github.io/InstructVLA_Home/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal |
| Method | InstructVLA |
| Dataset | SimplerEnv (Google Robot tasks, Expert), SimplerEnv-Instruct (任务聚合+情境推理), SimplerEnv-Instruct, LIBERO (四类任务平均) |

> [!tip] 效果简介
> - SimplerEnv (Google Robot tasks, Expert) 上，平均成功率 (Avg) 为 50.9，对比 SpatialVLA-3B: 45.9，变化 +33.3% (相对提升)。
> - SimplerEnv-Instruct (任务聚合+情境推理) 上，平均成功率 (Avg) 为 46.2 (Generalist)，对比 OpenVLA (FT): 23.9，变化 +96% (相对提升)。
> - SimplerEnv-Instruct 上，平均成功率 (Avg) 为 46.2 (Generalist)，对比 OpenVLA (FT&GPT-4o): 35.6，变化 +29% (相对提升)。

## 概述

现有视觉-语言-动作（VLA）模型在将多模态推理能力转化为精确操控技能时面临根本性瓶颈：联合学习视觉理解、语言推理与动作生成极易引发灾难性遗忘，而富含多模态监督的操控数据又极为稀缺。如何在不侵蚀视觉-语言模型（VLM）通用推理能力的前提下习得操控技能，并反过来利用推理增强操控表现，是该领域的核心挑战。

InstructVLA 提出**视觉-语言-动作指令微调（VLA-IT）**这一训练范式，核心机制在于将 VLM 的异步自回归推理与基于流匹配的动作生成解耦。其关键设计包括：（1）**潜在动作查询**作为高层规划与低层控制之间的中间表征；（2）**混合专家（MoE）适应机制**，通过可切换的 LoRA 专家和标量头，使模型在语言推理与潜在动作预测之间自适应切换；（3）**两阶段训练**——阶段一利用语言运动监督预训练动作专家，阶段二通过多模态-动作混合数据联合微调。

主要实证结论如下：

- 在 **SimplerEnv 封闭式操控**中，InstructVLA-Expert 相比 SpatialVLA 相对提升 **33%**（Table 2）。
- 在 **SimplerEnv-Instruct 基准**上，InstructVLA-Generalist 相比微调的 OpenVLA 提升 **96%**，相比 GPT-4o 辅助的动作专家提升 **29%**（Table 2, Abstract）。
- 在 **LIBERO 四类任务**上，InstructVLA-1.5B 达到 **95.8%** 成功率，远超 OpenVLA-7B 的 76.5%（Table 10）。
- 启用推理（thinking）为通用模型带来 **36.1%** 的性能增益（Figure 7b），验证了推理增强操控的有效性。
- 多模态理解能力几乎无损：InstructVLA-Generalist 在 MM-Vet 上得分 51.7，与专用 VLM Eagle2-1.5B 的 53.8 仅差 2.1 分（Table 1）。

消融实验进一步揭示：移除动作专家中的 DINOv2 视觉编码器导致性能下降 50%；加入语言运动监督提升 9.3%；在 VLA-IT 数据中引入场景问答与描述使泛化能力提升 10.8%。潜在动作令牌数量在 64 时达到性能与效率的最佳平衡。

当前方法仍受限于基础操作原语和单目视觉输入，在深度估计不足和分布外场景下存在失败风险。如何扩展到更灵巧的技能、整合多模态感官信息，以及利用合成数据减少对真实世界采集的依赖，是未来值得探索的方向。

## 背景与动机

### 视觉-语言-动作模型的兴起与困境

赋予机器人通用操控能力是具身智能的核心目标。近年来，大规模视觉-语言模型（VLMs）的进展催生了视觉-语言-动作模型（VLAs），试图将多模态理解与物理操控统一到单一框架中。然而，现有VLA模型面临一个根本性困境：**联合学习多模态推理与精确动作生成时，任务干扰会导致灾难性遗忘，而缺乏丰富多模态监督的操控数据进一步加剧了这一问题**。

具体而言，直接微调VLM以适应操控任务——如OpenVLA（Kim et al., 2024）——会导致其多模态理解能力几乎完全丧失（多模态得分降至0，见Table 1）。这种能力退化使得模型无法利用VLM的推理能力来增强操控表现，形成“理解”与“行动”之间的断裂。

### 现有方法的三大瓶颈

当前VLA研究在从理解走向操控的过程中，面临三个相互关联的障碍：

1. **灾难性遗忘**：操控数据通常仅包含简单的动作指令，缺乏场景描述、问答等丰富的语言监督。当VLM仅在这些稀疏信号上微调时，其通用的多模态推理能力迅速退化。

2. **监督信号匮乏**：大规模操控数据集（如Fractal、Bridge）仅提供离散动作标签，缺少将感知、推理与动作关联起来的中间表征。这使得模型难以学习“为什么这么做”的因果链条。

3. **推理-行动耦合缺失**：现有方法要么缺乏推理能力（如RT-2-X、OpenVLA），要么仅采用文本链式思考（CoT）作为外部附加模块（如ECoT, Zawalski et al., 2024），未与动作生成模块形成紧密的闭环。两阶段的推理-行动方法无法充分利用VLM的多模态能力来指导实时操控决策。

### 核心动机与研究问题

本文的核心动机源于一个关键问题：**如何在不侵蚀VLM多模态推理能力的前提下学会操控技能，并反过来利用这种推理增强操控？**

这一问题的本质是表征与训练范式的双重挑战。从表征角度，需要一个中间界面将VLM的高层语义推理与低层连续控制解耦；从训练角度，需要一个机制让模型在语言推理和动作预测之间自适应切换，而非相互干扰。

InstructVLA正是围绕这一动机展开：通过潜在动作查询（Latent Action Queries）作为中间表征、混合专家（MoE）适应机制实现模态切换、以及两阶段的视觉-语言-动作指令微调（VLA-IT）范式，首次系统性地探索了从多模态理解到推理增强操控的完整路径。

## 核心创新

InstructVLA 的核心创新在于提出了一套系统性的**视觉-语言-动作指令微调（VLA-IT）范式**，通过架构创新与训练策略创新，在根本上解决了现有 VLA 模型在联合学习多模态推理与精确动作生成时面临的三大障碍：任务干扰导致的灾难性遗忘、缺乏丰富多模态监督的操纵数据、以及缺少有效机制将 VLM 的推理能力转化为动作生成。

### 1. 混合专家（MoE）适应机制：解耦推理与动作生成

InstructVLA 在 VLM 主干网络中引入了 MoE 适应模块，这是实现推理与操控无缝集成的关键开关。该模块包含动作 LoRA、语言 LoRA 和一个标量头（scalar head），其前向传播公式为：

$$h = W_0 x + \sum_{i=0}^{K} B_i A_i x \cdot \alpha_i \cdot \lambda_i$$

其中标量头预测的门控系数 $\lambda_i$ 对每个 LoRA 适配器的缩放因子 $\alpha_i$ 进行重标定（$\alpha_i^* = \alpha_i \cdot \lambda_i$），使模型能够根据输入上下文动态加权两个 LoRA 专家的输出。这一设计使得 VLM 可以在语言推理与潜在动作预测之间自适应切换，从而既保留了 VLM 的通用多模态能力，又能在推理过程中注入任务相关知识以提升操控表现。

与此形成鲜明对比的是，现有方法如 **OpenVLA**（Kim et al., 2024）在直接微调后多模态得分降至 0，显示出严重的灾难性遗忘；而 InstructVLA 采用 MoE 适应与 1:7 多模态-动作混合训练，保持了与专用 VLM 相当的多模态性能（Table 1，MM-Vet 得分 51.7 vs. Eagle2-1.5B 的 53.8，仅轻微下降 2.1）。

### 2. 潜在动作查询：高层推理与低层控制的中间界面

InstructVLA 设计了 N 个可学习的潜在动作查询令牌（Latent Action Queries），通过交叉注意力与 VLM 的隐藏状态交互，生成任务相关的潜在动作表征 $C \in \mathbb{R}^{N \times D}$。这一中间表征充当了高层规划与低层控制之间的解耦界面，使得 VLM 的异步自回归推理与基于流匹配的动作专家得以独立运作。

在推理时，模型支持**异步自回归文本推理与潜在动作预测交替进行**，并支持潜在动作缓存和双频推理。具体而言，生成过程分为三步：
1. VLM 进行异步自回归推理；
2. 生成潜在动作表征；
3. 动作专家基于流匹配解码连续动作块。

这种设计从根本上改变了动作生成机制——从传统的自回归离散动作令牌（如 RT-2、OpenVLA）转变为流匹配连续动作生成，由 VLM 输出的潜在动作令牌条件化。

### 3. 两阶段训练范式：语言运动监督与多模态指令微调

InstructVLA 采用两阶段训练策略，有效解决了操纵数据缺乏丰富多模态监督的问题：

**Stage 1（动作预训练）**：通过语言运动监督预训练动作专家。VLM 学习将视觉线索与操作基元关联，同时动作专家学习从潜在动作表征生成连续动作。总损失为语言建模交叉熵损失与流匹配损失的直接相加：

$$\dot{\mathcal{L}} = \mathcal{L}_{LM} + \mathcal{L}_{FM}$$

其中流匹配损失定义为：

$$\mathcal{L}_{FM} = \mathbb{E}\left[ \left. V_\theta(\mathbf{A}^\tau, q_t) - (\epsilon - \mathbf{A}) \right.^2 \right]$$

**Stage 2（VLA-IT）**：引入 650K 多模态指令数据集，包含场景理解、指令多种重写和上下文创建。此阶段添加语言 LoRA 和标量头，与 Stage 1 的动作 LoRA 构成 MoE 适应模块。该模块是 Stage 2 唯一可训练的部分，总计 220M 参数，大幅减少了可训练参数量。

消融实验证实了这一范式的有效性：加入语言运动监督使整体成功率提升 9.3%（Table 3）；在 VLA-IT 数据中加入场景 QA 和描述使泛化能力提升 10.8%（Table 4）；冻结动作专家仅微调 VLM 的性能与联合微调几乎相同（Figure 6a），验证了架构解耦设计的合理性。

### 4. 推理增强的操控：从理解到行动的闭环

InstructVLA 首次实现了推理与操控的紧密耦合。与缺乏或仅使用文本链式思考（CoT）的现有方法（如 ECoT, Zawalski et al., 2024）不同，InstructVLA 的异步自回归机制允许模型在生成动作前进行多模态推理，并将推理结果注入潜在动作表征。实验表明，为通用模型启用推理（thinking）相比直接执行指令带来 36.1% 的性能增益（Figure 7b），验证了推理增强操控的核心假设。

### 创新总结

| 创新维度 | 基线方法 | InstructVLA |
|---------|---------|-------------|
| 动作生成机制 | 自回归离散动作令牌 | 流匹配连续动作生成，由潜在动作令牌条件化 |
| 多模态能力保持 | 直接微调导致灾难性遗忘 | MoE 适应与混合训练，保持 VLM 多模态性能 |
| 训练数据与范式 | 仅操作数据或简单混合 | 两阶段：语言运动监督 + 650K 多模态指令数据集 |
| 推理与操控集成 | 缺乏或仅文本 CoT，未与动作模块耦合 | 异步自回归推理与潜在动作预测交替，支持双频推理 |

## 整体框架

![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_tsxwloasw5/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the InstructVLA. InstructVLA integrates the multimodal reasoning capabilities of a vision-language model with robotic manipulation. Generation consists of three steps: (1) asynchronous auto-regressive reasoning by the VLM, (2) latent action generation, and (3) action decoding. A MoE adaptation enables the VLM to alternate between reasoning and latent action prediction. The flow matching action expert decodes the final actions, conditioned on latent actions*

![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_tsxwloasw5/figures/047_Figure_30.jpg]]
*Figure 30: Detailed overview of the MoE adaptation architecture. The frozen VLM backbone’s last hidden states are classified by a scalar head to produce gating weights $\lambda _ { 1 }$ and $\lambda _ { 2 }$ . , which control the weighted MoE adaptation. Similar to finetuning VLMs with multiple LoRA adapters, the MoE adaptation computes a weighted sum over the LoRA experts. The predicted tokens are then used differently based on their token type: language tokens are directly decoded as the model’s response, while features corresponding to action tokens are decoded by the action expert (see Figure 2 (right)) to produce continuous actions

![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_tsxwloasw5/figures/001_Figure_1.jpg]]
*Figure 1: Method overview. InstructVLA integrates vision-language understanding with precise robotic control to achieve reasoning-guided manipulation. Its core training strategy, Vision-Language-Action Instruction Tuning, enhances manipulation by unifying general multimodal knowledge, embodied reasoning, and atomic instruction-based manipulation into a coherent chain of thought*

InstructVLA 的核心设计目标是在单一 VLM 内实现多模态推理与语言引导的潜在动作规划的统一，同时将低层控制与高层理解解耦。其整体 pipeline 遵循“异步自回归推理 → 潜在动作生成 → 动作解码”三阶段流程（Figure 2）。

### 系统架构

**VLM Backbone** 采用 Eagle2-2B 作为多模态理解与推理引擎。该 backbone 在 448×448 分辨率下处理视觉输入，生成文本响应，同时通过附加的可学习查询从隐藏状态中提取潜在动作表征。模型通过混合专家（MoE）适应机制在语言推理与潜在动作预测之间切换，而非简单地微调整个 VLM。

**MoE Adaptation Module** 是架构的关键控制节点。它包含两个 LoRA 专家——动作 LoRA 和语言 LoRA——以及一个标量头（scalar head）。标量头根据 VLM 最后一层的隐藏状态预测门控系数 λ₁ 和 λ₂，动态加权两个 LoRA 专家的输出。其前向传播公式为：

$$ \boldsymbol { h } = \boldsymbol { W _ { 0 } } \boldsymbol { x } + \sum _ { i = 0 } ^ { K } B _ { i } \boldsymbol { A _ { i } } \boldsymbol { x } \cdot \boldsymbol { \alpha _ { i } } \cdot \boldsymbol { \lambda _ { i } } $$

其中标量因子 αᵢ 与门控系数 λᵢ 共同控制各 LoRA 专家的贡献权重，使模型能根据输入上下文自适应地在推理模式与动作模式之间切换。在 Stage-2 训练中，该 MoE 模块是唯一可训练组件，总计 220M 参数，大幅降低了微调成本。

**Latent Action Queries** 作为高层规划与低层控制之间的界面。N 个可学习的查询令牌通过交叉注意力与 VLM 的隐藏状态交互，生成任务相关的潜在动作表征 C ∈ R^{N×D}。实验表明，N=64 时性能与效率达到最佳平衡（Figure 9）。

**Action Expert** 是基于流匹配（flow matching）的动作解码器，采用 12 层 Transformer（hidden size 768），在 224×224 分辨率下运行。它接收三路输入：DINOv2 视觉编码器提取的视觉特征、潜在动作 C、以及噪声动作令牌。视觉特征通过 FiLM 调制层与潜在动作交互，增强空间定位与任务相关性。流匹配目标为：

$$ \mathcal { L } _ { F M } = \mathbb { E } \left[ \left. V \theta ( \mathbf { A } ^ { \tau } , q _ { t } ) - ( \epsilon - \mathbf { A } ) \right. ^ { 2 } \right] $$

推理时通过 N=10 步前向欧拉积分迭代去噪生成连续动作块。

### 两阶段训练范式

**Stage-1：动作预训练**。利用语言运动监督（language motion）预训练动作专家，将低层控制与 VLM 解耦。语言运动将低层动作转化为文本描述，增强 VLM 将视觉线索与操作原语关联的能力。该阶段联合优化语言建模交叉熵损失与流匹配损失：

$$ \mathbf { \dot { \mathcal { L } } } = \mathcal { L } _ { L M } + \mathcal { L } _ { F M } $$

**Stage-2：VLA 指令微调（VLA-IT）**。在 Stage-1 的动作 LoRA 基础上，新增语言 LoRA 和标量头，构成完整的 MoE 适应模块。训练数据为 650K 多模态指令数据集，涵盖场景理解、指令多种重写和上下文创建等标注。采用 1:7 的多模态-动作混合训练比例，确保模型在学会操控技能的同时保留 VLM 的多模态推理能力。

### 推理机制

InstructVLA 支持异步推理：VLM 先进行自回归文本推理（thinking），生成任务相关的语义分析；随后切换到动作模式，基于推理结果生成潜在动作 C；最后由动作专家解码为连续控制信号。这种设计支持潜在动作缓存和双频推理——推理可在低频运行，而动作生成保持高频，实现推理增强的操控。消融实验表明，为通用模型启用推理相比直接执行指令带来 36.1% 的性能增益（Figure 7(b)）。

## 核心模块与公式推导

### 整体架构与推理流程

InstructVLA 将 VLM 的多模态推理与基于流匹配的动作生成统一到单一框架中。其生成过程分为三个异步步骤（Figure 2）：

1. **异步自回归推理**：VLM 首先进行文本推理，生成语言响应。
2. **潜在动作生成**：通过可学习的潜在动作查询从 VLM 隐藏状态中提取任务相关的潜在动作表征 $\mathbf{C} \in \mathbb{R}^{N \times D}$，作为高层规划与低层控制之间的界面。
3. **动作解码**：动作专家以潜在动作 $\mathbf{C}$ 和视觉特征为条件，通过流匹配去噪过程生成连续动作块。

这种解耦设计的核心优势在于：VLM 的推理频率与动作生成频率可以独立设定（双频推理），推理结果可缓存复用，避免了对每个控制周期都进行完整自回归生成的沉重计算负担。

### MoE 适应模块

为实现语言推理与潜在动作预测之间的无缝切换，InstructVLA 在 VLM 的 Transformer 层中引入混合专家（MoE）适应机制。该模块包含三个可训练组件：**动作 LoRA**（Stage-1 预训练）、**语言 LoRA** 和**标量头**（Stage-2 新增）。

MoE 层的前向传播公式为：

$$
\boldsymbol { h } = \boldsymbol { W _ { 0 } } \boldsymbol { x } + \sum _ { i = 0 } ^ { K } B _ { i } \boldsymbol { A _ { i } } \boldsymbol { x } \cdot \boldsymbol { \alpha _ { i } } \cdot \boldsymbol { \lambda _ { i } }
$$

其中：
- $\boldsymbol{W_0 x}$ 为冻结的原始权重输出；
- $\boldsymbol{B_i A_i x}$ 为第 $i$ 个 LoRA 专家的低秩适应贡献；
- $\alpha_i$ 为各 LoRA 专家的基础缩放因子；
- $\lambda_i$ 为标量头根据输入上下文动态预测的门控系数，实现对动作专家和语言专家贡献的自适应重标定：$\alpha_i^* = \alpha_i \cdot \lambda_i$。

标量头使模型能够根据当前推理模式（语言生成 vs. 动作预测）自动调节两个 LoRA 专家的混合比例，从而在保留 VLM 多模态能力的同时注入操控知识。Figure 8 的门控激活可视化证实了这一机制：在推理阶段语言 LoRA 激活占优，在动作预测阶段动作 LoRA 激活占优。

### 动作专家与流匹配

动作专家采用 12 层 Transformer（隐藏维度 768），以 DINOv2 视觉编码器提取的图像特征和潜在动作 $\mathbf{C}$ 为条件。视觉特征通过 FiLM 调制层接受潜在动作的调制，增强空间定位与任务相关性。

动作生成采用流匹配目标，训练时预测从噪声到真实动作的向量场：

$$
\mathcal { L } _ { F M } = \mathbb { E } \left[ \left. V _ { \theta } ( \mathbf { A } ^ { \tau } , q _ { t } ) - ( \epsilon - \mathbf { A } ) \right. ^ { 2 } \right]
$$

其中 $\mathbf{A}^\tau$ 为噪声化的动作块，$q_t$ 为条件信息（视觉特征 + 潜在动作），$\epsilon$ 为高斯噪声，$\mathbf{A}$ 为真实动作。

推理时采用前向欧拉积分进行迭代去噪（$N=10$ 步）：

$$
\mathbf { A } ^ { \tau + 1 / N } = \mathbf { A } ^ { \tau } + \frac { 1 } { N } V _ { \theta } ( \mathbf { A } ^ { \tau } , q _ { t } )
$$

### 两阶段训练损失

**Stage-1（动作预训练）** 联合优化语言建模和流匹配目标：

$$
\mathcal { L } = \mathcal { L } _ { L M } + \mathcal { L } _ { F M }
$$

其中 $\mathcal{L}_{LM}$ 为语言运动描述的交叉熵损失，$\mathcal{L}_{FM}$ 为流匹配损失。这种语言运动监督使 VLM 学会将视觉线索与操控原语关联起来，消融实验表明其带来 9.3% 的整体成功率提升（Table 3）。

**Stage-2（VLA 指令微调）** 仅微调 MoE 适应模块（约 220M 参数），冻结 VLM 主干和动作专家，在保持多模态能力的同时注入操控推理能力。

## 实验与分析

### 核心实验设置

InstructVLA采用两阶段训练范式：**阶段一**进行动作预训练，联合优化语言建模损失与流匹配损失，训练动作专家；**阶段二**进行VLA指令微调，仅训练MoE适应模块（约220M参数），冻结VLM主干与动作专家。评估时，VLM以448×448分辨率运行，动作专家以224×224分辨率处理视觉输入，推理温度设为0以加速生成，所有结果均为三个随机种子的平均值并报告标准误。

---

### 多模态理解保持

**Table 1**展示了InstructVLA与各基线在标准VLM基准上的多模态理解能力。InstructVLA-Generalist（1.5B LLM骨干）在MM-Vet上取得51.7分，与原始Eagle2-1.5B的53.8分相比仅轻微下降2.1分；在MMStar上取得56.2分，OCRBench取得814分，HallB取得45.9分。相比之下，直接微调的OpenVLA-7B在同类基准上多模态得分几乎归零，验证了MoE适应策略在保持VLM通用多模态能力上的有效性。InstructVLA-Expert（不含多模态训练）在这些基准上同样表现良好，表明动作专家的解耦设计并未侵蚀VLM的理解能力。

![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_tsxwloasw5/figures/005_Table_1.jpg]]
*Table 1: Multimodal understanding. #Params is the size of LLM backbone. S. denotes robot state*

---

### 操控性能主结果

**Table 2**展示了在SimplerEnv上的封闭式操控结果。在Google Robot具身的原子任务上，InstructVLA-Expert取得**50.9%**的平均成功率，相比SpatialVLA-3B的45.9%相对提升**33.3%**。在WidowX Robot上，InstructVLA-Expert达到39.0%，同样优于SpatialVLA的31.7%。

![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_tsxwloasw5/figures/006_Table_2.jpg]]
*Table 2: Robotic manipulation. Google and WidowX Robot denote two embodiments in SimplerEnv. For SimplerEnv-Instruct, we focus on two reasoning levels instead of embodiments. Magma† denotes evaluation with sampling. The results of InstructVLA are averaged over three random seeds*

在更具挑战性的**SimplerEnv-Instruct**基准上，InstructVLA-Generalist取得**46.2%**的平均成功率，相比微调后的OpenVLA-7B（23.9%）提升**96%**，相比GPT-4o辅助的动作专家（35.6%）提升**29%**。加入机器人状态信息的InstructVLA-Generalist(S.)进一步提升至46.9%。这一基准包含任务聚合（Task Aggregation）和情境推理（Situated Reasoning）两类子任务，要求模型在理解指令语义的同时完成精确操控，InstructVLA的优势在此尤为显著。

在**LIBERO**基准（Table 10）上，InstructVLA-1.5B在四类任务（Spatial、Object、Goal、10 Long）上取得**95.8±0.4%**的平均成功率，显著超过OpenVLA-7B的76.5±0.6%（提升19.3个百分点），也优于π₀-3B的92.1±0.4%和GR00T-N1.5-3B的90.0±0.6%。

在**真实世界实验**（Figure 5）中，InstructVLA在原子指令上相比OpenVLA提升23.3%，在少样本推理任务上提升41.7%，在零样本推理任务上提升46.7%，验证了推理增强操控在实际场景中的有效性。

---

### 关键消融分析

#### 动作专家视觉设计（Table 3）

移除动作专家中的**DINOv2视觉编码器**导致操控成功率下降**50.0%**，表明鲁棒的视觉特征对低层控制至关重要。在此基础上引入**FiLM调制层**，利用潜在动作令牌调制视觉特征，进一步带来**15.3%**的性能提升。加入**语言运动监督**（language motion）使整体成功率提升**9.3%**，说明用自然语言描述低层运动原语有助于VLM建立视觉线索与操控原语之间的关联。

#### 微调策略（Figure 6）

冻结动作专家仅微调VLM的性能与联合微调几乎相同，但大幅减少了可训练参数量。这表明InstructVLA的模块化设计允许仅通过调整VLM来适应新任务，无需改变预训练好的动作专家。在Figure 6(b)中，当多模态与操控任务共存时，全量微调（FFT）导致多模态性能显著下降，而MoE适应策略在保持多模态能力的同时实现了操控性能的稳步提升。

#### 数据多样性与规模（Table 4, Figure 7）

在VLA-IT数据中加入场景QA和描述标注使InstructVLA在SimplerEnv-Instruct上的泛化能力提升**10.8%**。Figure 7(a)展示了VLA-IT标注数据的缩放行为：随着标注数据量增加，模型在SimplerEnv-Instruct上的性能持续提升，未出现饱和迹象。Figure 7(b)显示，在通用模型上启用推理（thinking）相比直接执行指令带来**36.1%**的性能增益，验证了异步自回归推理对情境任务的显著贡献。

![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_tsxwloasw5/figures/012_Figure_7.jpg]]
*Figure 7: Data scaling and multimodal training. Impact of scaling and training strategies on manipulation with multimodal reasoning*

#### 潜在动作令牌数量（Figure 9）

潜在动作令牌数量为**64**时达到性能与效率的最佳平衡。继续增加至128会导致性能下降，可能因为过多的潜在令牌引入了冗余信息，干扰了动作专家的解码过程。

---

### 失败模式分析

InstructVLA存在两类典型失败模式：

1. **深度估计不足**（Figure 19）：模型仅依赖单目第三视角图像，在需要精确深度判断的抓取任务中，难以准确估计夹爪与物体的相对位置，导致夹爪到位但无法成功抓取。

2. **真实-仿真域迁移中的分布外崩溃**（Figure 20）：由于真实场景中桌面缺少仿真环境中的机械臂反射等视觉线索，模型在深度估计上出现系统性偏差，导致机器人陷入异常位姿而无法完成任务。这表明当前视觉表征对特定域特征存在过拟合。

---

### 推理与操控的协同增益

Figure 10对30个情境推理任务进行了逐任务对比：启用推理后，在子任务识别（Subtask）、常识推理（Commonsense Reasoning）和工具使用常识（Commonsense for Tool-use）三类任务上均呈现一致的正向增益。Figure 11进一步展示了测试时思考与双频推理评估：模型可在低频（约1-2Hz）下进行文本推理，在高频（10-20Hz）下执行动作生成，实现推理与操控的异步协同。

---

### 跨具身与零样本泛化

Table 5的指令微调数据消融显示，仅在Bridge数据集上进行VLA-IT即可带来显著的跨具身泛化增益；同时使用Fractal和Bridge数据集进行VLA-IT可获得最佳性能。Figure 12的跨具身案例研究表明，InstructVLA能够在不同机器人平台间迁移推理能力，对未见过的具身配置仍能生成合理的任务规划与动作序列。Figure 13展示了模型在OCR等标准多模态任务上的零样本能力保持，进一步验证了MoE适应策略在防止灾难性遗忘方面的有效性。

![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_tsxwloasw5/figures/018_Table_5.jpg]]
*Table 5: Instruction tuning data ablation. We evaluate three settings: without VLA-IT data, with data only on Bridge, and with VLA-IT data on both Fractal and Bridge. This ablation examines the contribution of the VLA-IT dataset and the cross-embodiment generalization of InstructVLA on SimplerEnv-Instruct*

### 补充图表

![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_tsxwloasw5/figures/008_Table_3.jpg]]
*Table 3: Ablation of action expert vision design and language motion. “w/o Lang.” denotes without using language motion. “w/o FiLM” denotes using only DINO. “w/o DINO” denotes action expert without the vision input. (a)*

![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_tsxwloasw5/figures/010_Figure_6.jpg]]
*Figure 6: Finetuning strategies. (a) Freezing or finetuning the action head during VLA-IT training. (b) Training strategies when multimodal and manipulation tasks co-exist. “FFT” denotes full finetuning. “AR” denotes auto-regressive*

![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_tsxwloasw5/figures/013_Table_4.jpg]]
*Table 4: Effect of data dievrsity. “T.A.” denotes task aggregation, and “S.R.” denotes situated reasoning on SimplerEnv-Instruct*

![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_tsxwloasw5/figures/021_Table_6.jpg]]
*Table 6: Data comparison of different methods. “Trans.” denotes transitions*

![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_tsxwloasw5/figures/022_Table_7.jpg]]
*Table 7: VLA-IT captioning evaluation. “Sentence-BERT” and “SimCSE” represent learning-based evaluation methods, while the remaining metrics are traditional n-gram-based evaluations focused on word distribution*

## 方法谱系与知识库定位

### 1. 方法谱系：在VLA演进中的坐标

InstructVLA 处于视觉-语言-动作模型从“端到端模仿”向“推理增强操控”过渡的关键节点。其方法谱系可沿两条轴线梳理：动作生成机制的演进，以及多模态推理与操控的融合深度。

**动作生成范式的切换。** 早期VLA模型普遍采用自回归离散动作令牌方案。**RT-2-X**（Collaboration et al., 2023）将动作离散化为文本令牌，直接拼接在VLM的输出序列中进行自回归预测；**OpenVLA-7B**（Kim et al., 2024）延续了这一范式，将7B级VLM微调为动作令牌生成器。这类方案的优势在于实现简洁，但存在根本性局限：离散化损失连续动作的精度，且自回归解码的逐令牌延迟与高频控制需求之间存在张力。InstructVLA 以流匹配连续动作生成替代离散令牌方案，由VLM输出的潜在动作令牌$C \in \mathbb{R}^{N \times D}$条件化，将动作生成从VLM的自回归循环中解耦——这是其与RT-2/OpenVLA谱系的核心分水岭。同期的**π0-3B**（Black et al., 2024）和**GR00T-N1.5-3B**（Bjorck et al., 2025）也探索了流匹配或扩散动作生成，但InstructVLA的独特之处在于通过潜在动作查询建立了VLM隐藏状态与动作专家之间的显式信息瓶颈。

**推理-操控融合的深度差异。** 在将VLM的推理能力注入操控方面，现有方法可划分为三个层级：第一层是“推理与操控分离”的两阶段方案，如**ECoT**（Zawalski et al., 2024）先让VLM生成文本链式思考，再将思考结果作为条件输入独立策略网络——推理与动作模块之间仅通过文本传递信息，缺乏梯度耦合和表征共享。第二层是“推理作为上下文”的方案，如**ChatVLA**（Zhou et al., 2025）和**Magma-8B**（Yang et al., 2025），在VLM内部同时生成文本和动作令牌，但推理过程与动作生成共享同一自回归循环，导致推理时的逐令牌延迟直接拖累控制频率。InstructVLA 处于第三层：通过MoE适应机制实现异步自回归推理与潜在动作预测的交替执行。推理时VLM以文本自回归方式生成推理链，仅在需要行动时切换到动作LoRA专家输出潜在动作令牌，随后由独立的流匹配动作专家以更高频率解码为连续动作块。这种“双频推理”设计使推理深度与控制实时性得以兼顾——这是相较于ECoT和ChatVLA的关键架构优势。

**与SpatialVLA的直接对比。** **SpatialVLA-3B**（Qu et al., 2025）是SimplerEnv封闭式操控任务上的强基线，InstructVLA-Expert在相同设定下实现33%的相对提升。这一增益主要源于两处差异：一是InstructVLA的动作专家配备了DINOv2视觉编码器与FiLM调制层（消融实验表明移除DINOv2导致50%性能崩塌），而SpatialVLA缺乏此类专用视觉骨干；二是语言运动监督为VLM提供了将视觉线索与操控基元关联的预训练信号，使潜在动作表征更具任务判别力。

### 2. 适用边界与约束条件

InstructVLA的设计决策划定了其有效性的边界：

**任务复杂度边界。** 当前模型的操作技能受限于基础运动基元——抓取、放置、开/关、推/拉等——这些基元在Fractal和Bridge数据集中占据主导。对于需要精细力控、双手协调或工具使用的灵巧操作，InstructVLA缺乏相应的动作表征粒度和训练数据覆盖。这一限制并非架构固有缺陷，而是训练数据分布的反映：Fractal和Bridge数据集的操作多样性远低于标准VLM基准（如MMBench、MM-Vet）所覆盖的上千种任务。

**视觉感知边界。** 模型仅依赖单目第三视角RGB图像，在深度估计不足的场景中表现出系统性脆弱性。失败案例分析揭示，当目标物体与背景的纹理对比度低，或真实-仿真域迁移中缺失关键视觉线索（如机器人手臂在图像中的反射）时，模型容易产生分布外崩溃。引入深度或触觉模态是突破这一边界的自然方向，但当前架构尚未整合此类传感器。

**推理-行动交替的深度限制。** 尽管双频推理实现了推理与控制的异步解耦，但当前设计主要支持单轮“感知→推理→行动”的流水线模式。在多轮交互场景中——例如用户中途给出修正指令，或环境发生意外变化需要重新规划——模型对推理-行动交替的灵活切换能力尚未被充分验证。MoE门控机制在理论上有能力支持更复杂的交替模式，但训练数据的构建和评估基准的设计仍以单轮任务为主。

**多模态能力的保持边界。** Table 1显示InstructVLA-Generalist在MM-Vet上得分为51.7，与其VLM骨干Eagle2-1.5B的53.8相比仅有轻微下降（-2.1），且显著优于直接微调的OpenVLA（多模态得分接近0）。这一保持能力的代价是MoE模块的220M可训练参数（约占VLM骨干的15%），以及1:7的多模态-动作数据混合比例。当多模态数据占比进一步降低时，理解能力是否仍能保持尚待验证。

### 3. 局限性与已知失败模式

**动作专家的视觉依赖性过强。** 消融实验（Table 3）揭示了动作专家对DINOv2视觉编码器的极端敏感：移除后性能下降50%。这意味着当视觉条件恶化（遮挡、光照剧变、域迁移）时，整个操控流水线缺乏冗余的感知通路。语言运动监督在一定程度上缓解了这一问题（贡献9.3%的提升），但远不足以替代视觉信号。

**域迁移中的分布外崩溃。** 从仿真到真实世界的迁移中，InstructVLA在特定场景下表现出灾难性失败。例如，当真实环境中机器人手臂的反射特征与仿真训练分布不一致时，模型可能完全无法定位末端执行器。这反映了VLM的视觉编码器（训练于通用图像）与机器人操作场景之间存在表征鸿沟，而当前的VLA-IT数据增强策略（场景QA、描述生成）不足以弥合这一鸿沟。

**推理增益的任务依赖性。** Figure 10的30个情境推理任务对比显示，启用推理（thinking）带来的增益在不同任务类别间差异显著：在需要常识推理的工具使用任务上增益最大，而在简单的子任务识别上增益有限甚至为负。这表明推理模块的介入需要更智能的门控策略——当前模型对所有任务统一启用或关闭推理，缺乏对任务推理需求的在线评估能力。

**训练数据标注质量瓶颈。** VLA-IT数据集的构建依赖GPT辅助标注，但Table 14揭示的常见错误类型（时间定位错误、物体指代歧义）表明，VLMs在具身场景中的时间定位能力不足是标注质量的关键瓶颈。这些标注噪声可能在微调过程中被模型放大，导致对指令的误解。

### 4. 开放问题与未来方向

**技能粒度的扩展。** 如何将InstructVLA的两阶段训练范式扩展到更复杂的操作技能？一个可能的方向是将运动基元库从当前的6D基元扩展到包含力控、双手协调等高维动作空间，同时设计对应的语言运动描述体系。这需要新的数据收集策略——大规模遥操作或仿真数据生成管线的支持。

**多模态感知融合的架构设计。** 当前架构为视觉-语言-动作三模态设计，但触觉、深度、力矩等模态的缺失限制了物理交互的安全性。将这些模态整合进InstructVLA框架面临两个挑战：一是如何在MoE适应中为不同模态设计专家模块而不引发维度爆炸；二是如何在流匹配动作专家中有效融合多模态条件信号。FiLM调制层提供了一个可扩展的接口，但其对非视觉模态的有效性尚待验证。

**推理-行动交替的深化。** 将当前的单轮流水线扩展为真正的多轮交互推理-行动循环，需要两个关键能力：一是VLM对历史推理和行动结果的记忆与回溯——这可能需要引入显式的记忆模块或扩展上下文窗口；二是MoE门控对推理需求的自适应判断——即模型自主决定何时需要“慢思考”而非直接行动。Figure 11初步探索了测试时思考与双频评估，但距离真正的自适应推理仍有差距。

**泛化评估的系统化。** 当前评估以SimplerEnv和LIBERO为主，这些基准的任务多样性和环境复杂性远低于真实世界部署需求。构建覆盖更多具身形态、更多操作技能、更丰富语言指令的标准化评估体系，是推动VLA领域从“方法驱动”走向“问题驱动”的关键基础设施。SimplerEnv-Instruct基准的提出是朝这一方向迈出的第一步，但其30个情境推理任务的覆盖范围仍显有限。

**合成数据与数字孪生的角色。** Table 6的数据量对比显示，InstructVLA使用的训练数据量（约650K多模态指令样本）远小于纯VLM训练所需的上亿级样本。利用大规模合成数据和数字孪生技术生成多样化的操作场景与语言标注，是突破数据瓶颈的潜在路径。但合成数据的真实感保真度与标注准确性之间的权衡，以及合成-真实域迁移的泛化保证，仍是开放挑战。

## 原文 PDF

![[paperPDFs/ICLR_2026/Vision_Language_Action_Instruction_Tuning_From_Understanding_to_Manipulation.pdf]]
