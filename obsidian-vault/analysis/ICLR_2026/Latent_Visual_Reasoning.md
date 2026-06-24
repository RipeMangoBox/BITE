---
title: "Latent Visual Reasoning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Latent_Visual_Reasoning.pdf
aliases:
- LVRL
- LVR
tags:
- ICLR_2026
- topic/other_unclear
- topic/other_unclear/general
core_operator: "将推理空间从离散文本token扩展至连续视觉token：让LLM在潜在空间中直接重建与查询相关的视觉语义（即‘潜在视觉推理’），并将重建的视觉信号作为后续文本生成的条件，从根本上打通视觉与语言的联合推理。"
primary_logic: "既然视觉与文本token被映射到同一语义空间，就应当对二者进行联合推理，而非局限在文本一侧。通过让LLM的最后一个隐藏状态去近似问题相关的视觉特征，可在不依赖外部工具的前提下实现更深层的跨模态推理。"
claims:
- "在MMVP测试上，LVR（4步）达到72.0%，较Qwen2.5-VL基线的66.67%显著提升5.33个百分点。"
- "在V*基准上，LVR（8步）取得81.7%，V*_D.A.达84.4%，V*_R.P.达77.6%，超越所有开源基线。"
- "标准LVR（无额外head）在所有消融实验中表现最佳，表明LLM原生即可对齐视觉与文本语义。"
- "强化学习阶段（GRPO_latent）可进一步提升3B模型在多个视觉任务上的表现，验证了RL对潜在推理的积极作用。"
---

# Latent Visual Reasoning

> [!tip] 核心洞察
> 既然视觉与文本token被映射到同一语义空间，就应当对二者进行联合推理，而非局限在文本一侧。通过让LLM的最后一个隐藏状态去近似问题相关的视觉特征，可在不依赖外部工具的前提下实现更深层的跨模态推理。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 潜在视觉推理 |
| 英文题名 | Latent Visual Reasoning |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=j84WR5ORsC); [GitHub](https://github.com/VincentLeebang/lvr); [Project](https://vincentleebang.github.io/lvr-project-page/) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | Latent Visual Reasoning (LVR) |
| Dataset | MMVP (Qwen2.5-VL-7B), V* (Qwen2.5-VL-7B), V*_D.A. (Qwen2.5-VL-7B), V*_R.P. (Qwen2.5-VL-7B) |

> [!tip] 效果简介
> - MMVP (Qwen2.5-VL-7B) 上，Accuracy 为 72.0 (LVR 4 Steps)，对比 66.67 (Qwen2.5-VL)，变化 +5.33。
> - V* (Qwen2.5-VL-7B) 上，Accuracy 为 81.7 (LVR 8 Steps)，对比 N/A (exceeds all baselines)，变化 +2.7 (vs base model on V*_D.A.)。
> - V*_D.A. (Qwen2.5-VL-7B) 上，Accuracy 为 84.4 (LVR 8 Steps)，对比 81.7 (estimated from +2.7% claim)，变化 +2.7。

## 概述

当前多模态大语言模型虽已集成先进的视觉编码器，但受限于模态投影偏差与跨模态注意力干扰，其对视觉细节的捕获常与文本查询脱节，形成从视觉输入到最终答案的根本性断层。现有范式——“思考图像”（Think about Images）在纯文本空间进行推理，“用图像思考”（Think with Images）则依赖外部工具操作图像——均未能使视觉信号深度参与核心推理过程，跨模态理解能力因此受限。

针对上述瓶颈，本文提出**潜在视觉推理（Latent Visual Reasoning, LVR）**，一种全新的多模态推理范式。其核心创新在于将推理空间从离散文本 token 拓展至连续视觉语义空间：在大语言模型的潜在空间中，通过迭代地让最后一个隐藏状态逼近与查询相关的视觉 token，实现**视觉语义的重建**，并将重建后的连续信号作为后续文本生成的条件。该方法充分利用了视觉与文本嵌入已被映射至同一语义空间的事实，使大模型无需借助任何外部工具即可完成视觉与语言的**联合推理**。

LVR 的训练采用两阶段策略。**监督微调（SFT）**阶段，利用边界框标注获取查询相关的视觉区域，联合优化视觉重建损失（MSE）与文本生成损失（交叉熵），指导模型在隐空间进行多步推理；**强化学习（GRPO_latent）**阶段，则通过重放潜在隐藏状态，仅对文本生成部分计算策略梯度，支持潜在推理下的策略优化。推理时，由特殊 token 触发与终止潜在推理，当前最优的中止策略为固定步数。

在多项视觉中心基准测试中，LVR 取得了显著提升。以 **Qwen2.5-VL-7B** 为基础模型，LVR（4步）在 **MMVP** 上达到 72.0%，较基线提升 5.33 个百分点；在 **V*** 基准上，LVR（8步）整体准确率达 81.7%，属性识别（V*_D.A.）与空间关系推理（V*_R.P.）分别达 84.4% 和 77.6%，均优于所有开源基线。消融实验表明，**不加额外投影头**的标准 LVR 设计在所有视觉基准上表现最佳，证明大语言模型本身即可有效对齐视觉与文本语义；**GRPO_latent** 强化学习则可进一步提升 3B 模型在多个视觉任务上的性能，验证了策略优化对潜在推理的积极作用。

当前 LVR 仍存在若干局限：主要面向单图像场景，在多图像任务上表现欠佳；可变长度的潜在推理中止机制尚不稳定（可学习的 Latent End Token 易导致性能崩溃），固定步数虽可靠但缺乏灵活性；SFT 阶段依赖边界框标注，制约了训练数据的可扩展性；额外推理步骤带来的计算开销亦有待量化分析。后续工作可聚焦于多帧/多图像扩展、更鲁棒的自适应中止条件，以及利用无监督数据预训练等方向。

## 背景与动机

当前多模态大语言模型（MLLMs）虽然普遍集成了高性能视觉编码器，但在视觉信息向文本答案转换的关键路径上仍存在根本性断层。由于模态投影偏差、跨模态注意力失衡以及语言模型内部的模态干扰，骨干LLM往往无法稳定捕获与文本查询最相关的视觉细节，导致模型在面对细粒度视觉理解任务（如空间关系判别、目标计数）时频繁失败。这一瓶颈的根源在于，视觉信号与文本生成之间始终缺乏直接、共享的推理空间，推理过程被单向压缩到离散的文本token侧，连续视觉语义中的丰富信息在早期投影后便被冻结。

现有工作围绕该瓶颈大致形成了两种范式，但均未能弥合跨模态语义鸿沟。**“Think about Images”** 类方法（如Vision-R1）将多模态推理完全展开在文本空间中，视觉表征仅充当静态提示，推理的动态过程无法反哺或细化视觉理解；**“Think with Images”** 类方法（如PAPO、PixelReasoner）虽然引入了外部工具对图像进行显式操控，但推理控制流本质上仍由文本驱动，视觉信号的二次编码与返回过程引入了额外的信息损失与延迟。两者的共性问题在于，它们都将视觉与语言视为两个分离的子系统，而忽略了二者在MLLM的嵌入层之后早已被映射到同一个语义空间这一事实——既然如此，为何不对二者进行联合推理？

针对上述缺口，本文提出**潜在视觉推理（Latent Visual Reasoning, LVR）**，核心动机在于：将推理空间从离散文本token延展至连续的视觉嵌入，让LLM在潜空间中直接迭代重建与问题相关的视觉语义，并用重建后的视觉语义显式地条件化后续文本生成。这一机制打通了从视觉输入到文本输出的闭合环路：LLM在接收到触发指令后，通过传播隐藏状态逐步逼近目标视觉特征，相当于在语义层面上“想象”与答案紧密相关的图像区域，而后再基于该内部表征进行语言解码。由于整个过程完全在LLM的现有潜空间内完成，LVR无需外部视觉工具或独立的视觉编码器，并且可自然地与标准文本生成交替执行，实现混合模态推理。

初步验证证明了该动机的迫切性与可行性：在MMVP基准上，LVR仅通过4步潜在推理便将Qwen2.5-VL基线的准确率从66.67%提升至72.0%，揭示了单纯依靠文本空间推理的潜力瓶颈；而在V*系列任务中，LVR（8步）的表现全面超越所有开源基线，进一步说明直接建模视觉语义对于细粒度理解任务具有不可替代的价值。因此，LVR并非对现有MLLM架构的颠覆，而是对其内置联合语义潜力的激活，促使模型真正实现“看到即推理”的跨模态协同。

## 核心创新

当前多模态大模型虽已集成先进的视觉编码器，但受限于模态投影偏差、跨模态注意力偏差与模态干扰，骨干语言模型往往无法捕获与文本查询最为相关的视觉细节，导致从视觉输入到最终文本答案之间存在根本性的信息断层。现有“Think about Images”与“Think with Images”两种范式本质上仍以文本空间推理为主导，未能真正弥合视觉信号与文本生成之间的鸿沟。

**Latent Visual Reasoning (LVR)** 针对这一瓶颈提出了一条截然不同的路径：将推理空间从离散文本 token 扩展到连续视觉 token，让语言模型在潜在空间中直接重建与查询相关的视觉语义，并将重建的视觉信号作为后续文本生成的条件，从根本上打通视觉与语言的联合推理。

### 相对于 baseline 的三大变更切入点

与以 Qwen2.5-VL 为代表的常规多模态大模型相比，LVR 在以下三个关键模块上进行了系统性替换（changed slots）：

| 变更点 | baseline 做法 | LVR 做法 | 证据强度 |
|---|---|---|---|
| **推理输出模态** | 全程输出离散文本 token | 混合模式：插入潜在推理阶段，该阶段输出连续隐藏状态以近似视觉 token；随后切换回文本生成模式 | 高（Section 3.1） |
| **训练目标** | 单一的下一个 token 预测（交叉熵损失） | 联合优化：视觉重建损失（MSE）+ 文本生成损失（交叉熵）；第二阶段引入 GRPO_latent 强化学习 | 高（Section 3.2） |
| **推理过程控制** | 无特殊控制，全程文本自回归 | 特殊 token（`<|lvr_start|>`、`<|lvr_end|>`）触发与终止潜在推理；采用固定步数或可学习的结束 token 作为解码策略 | 中-高（Section 3.1, 3.3） |

这些变更的核心在于：既然视觉与文本 token 在同一个语义空间中被对齐，就没有理由仅局限在文本一侧进行推理。LVR 直接利用语言模型最后一个时间步的隐藏状态去近似问题相关的视觉嵌入，使跨模态推理在不需要任何外部工具的情况下成为可能。

### 潜在推理机制与混合生成

LVR 的推理流程可概括为“触发—潜在重建—条件生成”的三段式架构（参见 Figure 2）：

1. **触发**：模型在生成特殊 token `<|lvr_start|>` 后自动进入潜在推理模式。
2. **潜在重建**：此阶段语言模型以步骤化方式传播隐藏状态，每一时间步的隐藏状态 $\mathbf{h}_t$ 都被要求逼近对应的真实视觉嵌入 $\mathbf{v}_t$（即与查询相关的图像区域特征）。该过程不输出 token，仅内部更新隐藏状态，步数由预设的固定 budget（如 4 步、8 步）决定。
3. **文本生成**：当满足中止条件（如达到预定步数或生成 `<|lvr_end|>`）后，模型退出推理阶段，并将在潜在推理阶段累积的隐藏状态作为上下文条件，继续以标准方式预测文本答案。

这一混合式生成策略在推理时实现了视觉信息的内部“回想”——语言模型不再依赖静态的图像特征，而是主动在潜在空间中重构当前问题真正需要的视觉语义。

### 针对潜在空间的联合训练目标

为培养上述潜在推理能力，LVR 设计了崭新的监督微调（SFT）与强化学习（RL）两阶段训练框架。

**SFT 阶段**：将文本生成损失与视觉重建损失联合优化。具体地，给定边界框标注（用于定位与问题相关的视觉区域），模型被要求最小化潜在推理期间的隐藏状态与对应视觉嵌入之间的均方误差（MSE，$\mathcal{L}_{\mathrm{LVR}}$），同时最大化以重建视觉语义为条件的文本答案概率（$\mathcal{L}_{\mathrm{NTP}}$）。联合目标为：

$$
\mathcal{L} = \mathcal{L}_{\mathrm{NTP}} + \lambda_{\mathrm{LVR}} \cdot \mathcal{L}_{\mathrm{LVR}}
$$

其中 $\lambda_{\mathrm{LVR}}$ 控制视觉重建信号的强度。

**RL 阶段**：提出 GRPO_latent 变体，专门适配潜在推理的特有结构。该算法在计算策略梯度时，仅对文本生成部分的 token 进行操作，潜在推理过程的隐藏状态通过 teacher-forcing 进行重放（replay），从而计算出 token 级的新旧策略概率比。其核心目标公式为：

$$
J_{\mathrm{GRPO}_{\mathrm{latent}}}(\theta) = \mathbb{E}_{q,I,o\sim\pi_{\theta_{\mathrm{old}}}} \left[ \frac{1}{|y|} \sum_{t=1}^{|y|} \min\left( r_t(\theta) \hat{A}_t, \mathrm{clip}\big( r_t(\theta), 1-\varepsilon, 1+\varepsilon \big) \hat{A}_t \right) - \beta D_{\mathrm{KL}}\big( \pi_{\theta}(\cdot|q,I) \big|\big| \pi_{\mathrm{ref}}(\cdot|q,I) \big) \right]
$$

这一设计使得强化学习可以在不破坏潜在重建能力的前提下进一步优化文本生成质量。

### 关键消融发现：原生对齐优于额外结构

一系列消融实验揭示了一个重要结论：**标准的 LVR（不加任何额外的投影头）在所有视觉基准上均取得最佳表现**（Table 3，Fig. 3），而添加 MLP 或 GLU 等 LVR head 反而带来性能下降。这表明语言模型本身已具备在原生语义空间中对齐视觉与文本语义的能力，无需另行介入。

在解码策略方面，尝试使用可学习的 Latent End Token 作为中止条件会导致推理极不稳定，V* 准确率暴跌至 39.8；另一种模式切换损失（Mode Switching Loss）也未能成功，常使 LVR 步数退化为零。相比之下，采用固定步数的 budget 是目前最可靠的中止策略，但也暴露了可变长度潜在推理仍待解决的难题。

### 有效性证据

LVR 的核心创新直接转化为显著的性能提升：
- 在 **MMVP** 基准上，LVR（4 步）达到 72.0%，较 Qwen2.5-VL 基线的 66.67% 提升 **5.33** 个百分点（Table 1）。
- 在 **V*** 基准上，LVR（8 步）分别取得整体 81.7%、Spatial Attribute 84.4% 和 Relationship 77.6%，均超越所有开源基线（Table 1）。
- **强化学习阶段**（GRPO_latent）能够进一步提振 3B 模型的视觉推理能力，验证了 RL 对潜在推理的正向调节作用（Table 2）。

这些结果共同表明，LVR 不仅仅是一种架构上的小修小补，它切实开拓了多模态大模型从“思考图像”到“在视觉空间中思考”的新范式，并且在无需外部工具或额外视觉处理的条件下，实现了更紧密的跨模态联合推理。

## 整体框架

![[assets/figures/papers/iclr26_0015_j84WR5ORsC_Latent_Visual_Reasoning/figures/002_Figure_2.jpg]]
*Figure 2: Training and inference pipeline of LVR. The overall framework closely follows a standard MLLM. Images are encoded into tokens by a visual encoder and mapped into a joint semantic space with text embeddings. During the SFT stage, bounding boxes are provided to identify query-relevant visual tokens, which supervise the last hidden states in the LVR process. Here, only the LLM’s last hidden states are passed forward for latent reasoning, optimized with a mean squared error (MSE) loss. The LVR process is wrapped with special tokens that indicate reasoning mode. Once all query-relevant visual tokens are consumed, the model exits LVR and resumes standard text generation with cross-entropy loss. D...*

Latent Visual Reasoning (LVR) 的设计出发点在于：当前多模态大模型 (MLLMs) 虽然配备了强大的视觉编码器，但模态投影偏差、跨模态注意力偏差等问题使得骨干 LLM 往往无法有效捕获与文本查询最相关的视觉细节，形成视觉输入与最终文本答案之间的根本性断层。LVR 的核心理念是将推理空间从离散的文本 token 扩展到连续的视觉 token 空间，让 LLM 在生成文本答案之前，于潜在空间中主动重建与问题相关的视觉语义，从而打通视觉与语言的联合推理通道。

**整体管线与模块关系**  
LVR 的框架严格遵循标准 MLLM 的架构，由三个关键模块构成：  
- **视觉编码器 (Vision Encoder)**：将输入图像编码成视觉特征。  
- **多模态投影器 (Multimodal Projector)**：将视觉特征映射到与文本相同的语义空间，产生视觉 token $\mathbf{V}_T$。  
- **LLM 骨干 (LLM Backbone)**：接收视觉 token 与文本 token 的嵌入序列，并作为唯一的可训练组件（在 SFT 和 RL 阶段均冻结视觉编码器与投影器）执行混合推理。

**输入输出流与混合推理机制**  
在推理时，流程如下所述（参见 Figure 2）：  
1. 输入图像经视觉编码器与投影器得到视觉 token $\mathbf{V}_T$，与文本查询的嵌入拼接后送入 LLM 骨干。  
2. LLM 正常生成文本，直至生成特殊 token `<|lvr_start|>`，自动触发 **潜在视觉推理 (LVR) 阶段**。  
3. 在 LVR 阶段，LLM 不再采样离散 token，而是将其最后一个隐藏状态作为当前步的“潜在输出”。该隐藏状态一方面被用作下一步的输入（实现自回归迭代），另一方面在训练时与由边界框标注给出的问题相关视觉嵌入进行 MSE 对齐，以重建与查询相关的视觉语义。这一过程持续固定步数（如 4、8、16 步）或直到生成特殊 token `<|lvr_end|>`（尽管可学习的终止机制目前仍不稳定，固定步数是当前最优的中止策略）。  
4. 退出 LVR 阶段后，模型恢复正常的文本生成，此时 LLM 以重建后的视觉语义为条件，预测最终答案的每个 token。

**训练范式**  
LVR 采用两阶段训练管道来建立上述能力：  
- **监督微调 (SFT)**：联合优化两个目标。**视觉重建损失** $\mathcal{L}_{\mathrm{LVR}} = \frac{1}{T_v} \sum_{t=1}^{T_v} \|\mathbf{h}_t - \mathbf{v}_t\|_2^2$ 强制 LVR 阶段的隐藏状态接近真实视觉嵌入；**下一 token 预测损失** $\mathcal{L}_{\mathrm{NTP}}$ 则确保以重建的视觉语义为条件仍能正确生成文本。总损失为 $\mathcal{L} = \mathcal{L}_{\mathrm{NTP}} + \lambda_{\mathrm{LVR}} \cdot \mathcal{L}_{\mathrm{LVR}}$。SFT 阶段依赖带边界框的数据，用于提供问题相关的视觉区域监督。  
- **强化学习 (GRPO_latent)**：针对潜在推理设计的策略梯度变体。由于 LVR 阶段不产生离散 token，GRPO_latent 仅在文本生成部分计算策略损失，且通过 Teacher Forcing 重放之前保存的潜在隐藏状态，来计算 token 级重要性比率。该阶段无需边界框标注，使模型可进一步自我演化，在多个视觉基准上提升性能。

整个框架并未引入额外的投影头（消融实验表明 LLM 原生即可对齐视觉与文本语义），也无需依赖外部图像编辑工具，仅在标准 MLLM 内部通过控制解码流程和损失函数，实现了视觉信号与文本生成之间的深层耦合。

## 核心模块与公式推导

**瓶颈与机制**  
当前多模态大模型（MLLM）普遍存在“视觉–文本断层”——即便视觉编码器足够强大，骨干 LLM 依然难以捕获与文本查询高度相关的视觉细节。Latent Visual Reasoning（LVR）将推理空间从纯文本 token 扩展至连续视觉 token，通过让 LLM 在潜在空间中直接重建查询相关的视觉语义，并将重建的视觉信号作为后续文本生成的上下文，从根本上打通跨模态联合推理。

**关键模块**  
LVR 沿用标准 MLLM 的三组件结构（§3.1, Figure 2）：  
1. **Vision Encoder** 将输入图像编码为原始视觉特征 $\mathbf{V}$；  
2. **Multimodal Projector** 通过可训练的投影层 $proj(\cdot)$ 将这些特征映射到 LLM 的语义空间，产生视觉 token 嵌入 $\mathbf{V}_T$；  
3. **LLM Backbone** 同时接收 $\mathbf{V}_T$ 与文本嵌入，并在特殊 token 的触发下进入混合推理模式——在潜在空间内传播隐藏状态以近似视觉语义，随后切回正常的文本自回归生成。  

训练时仅更新 LLM 参数（视觉编码器和投影器冻结），避免破坏预训练的视觉–语言对齐。

**混合推理中的模态切换**  
推理过程由一对特殊 token 控制：生成 `⟨lvr_start⟩` 后，模型进入 **潜在推理阶段**，不再输出离散 token，而是连续地传播最后一层隐藏状态 $\mathbf{h}_t$；当满足中止条件（例如达到预定义的固定步数 $T_v$，或生成 `⟨lvr_end⟩`）时，系统切回标准文本生成模式。这种“潜在推理 + 文本生成”的交替机制使模型能够在不依赖外部工具的前提下实现对感兴趣区域（ROI）的渐进式对准。

**监督微调阶段的公式**  
给定包含边界框标注的训练样本，SFT 阶段通过两个损失函数联合优化（§3.2.1）：  

*视觉重建损失（LVR Loss）*  
$$
\mathcal{L}_{\mathrm{LVR}} = \frac{1}{T_v} \sum_{t=1}^{T_v} \| \mathbf{h}_t - \mathbf{v}_t \|_2^2
$$
其中 $\mathbf{h}_t$ 是 LLM 在潜在推理第 $t$ 步的 last hidden state，$\mathbf{v}_t$ 是真实 ROI 对应的视觉嵌入，$T_v$ 为潜在推理步数。该损失强制隐藏状态向查询相关的视觉语义靠近。

*下一 token 预测损失（NTP Loss）*  
$$
\mathcal{L}_{\mathrm{NTP}} = -\frac{1}{T_y} \sum_{t=1}^{T_y} \log p_{\theta}( y_t \mid y_{<t}, \mathbf{h}_{1:T_v} )
$$
以潜在推理阶段最终获得的视觉上下文 $\mathbf{h}_{1:T_v}$ 为条件，最大化文本答案 $y_{1:T_y}$ 的似然。

*联合目标*  
$$
\mathcal{L} = \mathcal{L}_{\mathrm{NTP}} + \lambda_{\mathrm{LVR}} \cdot \mathcal{L}_{\mathrm{LVR}}
$$
超参 $\lambda_{\mathrm{LVR}}$ 平衡视觉重建信号与文本生成信号。

**强化学习阶段的扩展**  
为进一步提升泛化性，LVR 在 SFT 之后引入一个适配后的 GRPO 变体——**GRPO_latent**（§3.2.2, Equation 4）。其核心创新在于：仅对文本生成部分的 token 计算策略梯度，而潜在推理阶段通过 teacher-forcing 重放训练时记录的隐藏状态 $\widetilde{h}_i^{\mathrm{latent}}$ 来获得稳定的条件概率。具体地，token 级重要性比率为  

$$
r_{i,t}(\theta) = \frac{ \pi_{\theta}( y_{i,t} \mid q, I, \widetilde{h}_i^{\mathrm{latent}}, y_{i,<t}) }{ \pi_{\theta_{\mathrm{old}}}( y_{i,t} \mid q, I, \widetilde{h}_i^{\mathrm{latent}}, y_{i,<t}) }
$$

PPO 风格的目标函数在此基础上施加 clip 操作与 KL 惩罚，保证训练稳定。

**设计选择的有效性与失效模式**  
消融实验（§4.5, Table 3/Fig. 3）揭示出几个关键事实：  
- **标准 LVR（无额外投影头）在所有视觉基准上表现最优**，说明 LLM 原生已能在潜在空间中对齐视觉与文本语义，额外 MLP/GLU 头反而引入冗余扰动。  
- **固定步数是当前最可靠的中止策略**；可学习的 `⟨latent_end⟩` token 解码极不稳定，甚至导致 V* 准确率骤降至 39.8。  
- **Mode Switching Loss（在潜在阶段直接监督 token 分布）完全失效**，常使 LVR 步数坍缩至零，未能可靠编码停止条件。  

这些结果表明 LVR 的潜力在于其简洁的主干对齐机制，而动态、自适应长度的潜在推理中止策略仍是开放难题。

## 实验与分析

### 主实验结果

在视觉中心的多项基准上，LVR（潜在视觉推理）相较仅文本推理的基线实现了一致且显著提升。Table 1汇总了Qwen2.5‑VL‑7B模型下不同步数LVR与主流“思考图像”/“用图像思考”方法的对比：在MMVP上，4步LVR达到72.0%，比Qwen2.5‑VL基线的66.67%提高5.33个百分点；在V*整体指标上，8步LVR取得81.7%，其中V*_D.A. 84.4%和V*_R.P. 77.6%分别超出基线约2.7个和5.3个百分点，超越所有开源竞争对手（如PixelReasoner、Vision‑R1等）。固定步数的LVR（4/8/16步）在这些任务上性能稳健，未见随步数增加而崩溃，表明连续视觉语义重建有效弥补了跨模态投影偏差。

![[assets/figures/papers/iclr26_0015_j84WR5ORsC_Latent_Visual_Reasoning/figures/003_Table_1.jpg]]

强化学习阶段进一步放大了LVR的收益。Table 2显示，在3B规模模型上应用GRPO_latent后，多个视觉任务指标相较纯监督微调仍有提升，验证了将潜在推理嵌入策略梯度的有效性——模型能在自演化中更好地平衡视觉重建与文本生成。

### 消融实验

消融研究围绕“如何切换推理模态”与“是否需要额外投影头”展开（Table 3 / Fig. 3）。关键发现包括：

![[assets/figures/papers/iclr26_0015_j84WR5ORsC_Latent_Visual_Reasoning/figures/005_Table_3.jpg]]
*Table 3: Ablation studies on the 7B model show the standard approach performs best, indicating the LLM natively aligns visual and textual semantics without an extra head. However, the unstable latent end token suggests a need for future work on variable-length reasoning*

1. **标准LVR（无额外head）在所有视觉基准上表现最佳**。即便引入2层MLP或门控线性单元（GLU）将LLM隐藏状态显式映射至视觉语义空间，也未超越原生LLM直接对齐视觉与文本语义的能力，表明MLLM的骨千经训练可内部完成跨模态对齐，无需附加参数。

2. **可学习的Latent End Token策略极度不稳定**，导致V*指标暴跌至39.8，印证了端到端学习中止条件的困难。模式切换损失（Mode Switching Loss）同样未能有效编码停止信号，常使LVR步数在训练中收敛至零，进一步佐证可变长度潜在推理的控制瓶颈。

3. **固定步数（Fixed Token Budget）是当前最可靠的中止策略**。虽然缺乏根据样本难度自适应调整的灵活性，但至少避免了因解码策略波动而破坏推理过程的稳定性。

4. **所有消融中，去除额外head的方案均优于MLP/GLU设计**，且在多个基准上保持优势，确认了当前LVR架构的核心贡献不在于head工程，而在于将视觉重建目标直接作用于LLM最终隐藏态。

### 失败模式与局限性

- **可变长度推理机制不成熟**：固定步数策略虽稳定，却无法根据问题复杂度弹性分配推理预算；可学习结束token和模式切换损失均表现脆弱，甚至引发步数坍缩，制约更高效、更自适应的应用。
- **多图像场景泛化不足**：在需要多图对比的任务（如Relative Reflect）上LVR表现欠佳，暴露出当前设计仅针对单图像场景；论文亦指出需探索跨图像数据增强以弥补该短板。
- **训练数据依赖边界框标注**：监督微调需要具有兴趣区域（RoI）边界框的标注数据来构造视觉重建目标，限制了训练数据的可扩展性；虽然强化学习阶段可缓解该依赖，但冷启动仍受标注量约束。
- **计算开销未量化**：论文未分析潜在推理步数与推理延迟、显存占用之间的关系，高步数场景下的实时性风险未被评估。
- **任务覆盖面有限**：目前仅在视觉问答基准上验证，视频理解、具身推理等其他多模态任务的可迁移性尚未探索。

### 重要图表结论

- **Fig. 1（概念对比）**：通过三种范式——纯文本推理、借助外部工具操作图像、潜在空间视觉语义重建——的示意图，清晰揭示LVR的核心差异：不依赖外部工具，直接在LLM的语义空间中打通视觉与文本的联合推理通道。
- **Fig. 2（训练‑推理流程）**：展示从视觉编码、多模态投影、潜在推理重建到文本生成的完整管线，突出监督微调与强化学习两阶段如何在同一个框架下协同优化。
- **Table 1**：以V*、MMVP为代表的视觉核心任务上，LVR的绝对优势确立其在“无需工具”范式下的领先地位；4‑8步即可超过基于工具操作的最强系统，暗示内部视觉重建的性价比。
- **Table 2**：强化学习阶段的增量收益证明LVR可通过策略优化自我进化，向无监督自适应推理迈进。
- **Table 3 / Fig. 3**：消融图谱明确指向“少即是多”的设计哲学：原生LLM的隐藏态对齐能力已足够强，不必借助额外head或复杂中止机制，而可变长度的中止控制仍是开放难题。

![[assets/figures/papers/iclr26_0015_j84WR5ORsC_Latent_Visual_Reasoning/figures/001_Figure_1.jpg]]
*Figure 1: Conceptual illustration of LATENT VISUAL REASONING (LVR). We compare LVR with two paradigms: “Think about images,” which performs multimodal reasoning entirely in text space, and “Think with images”, which leverages external visual tools to highlight regions of interest (ROIs). In contrast, LVR leverages the LLM’s latent space to reconstruct the semantics of ROIs, enabling seamless cross-modal reasoning*

### 公平性与可复现性

实验基于开源模型Qwen2.5‑VL、公开数据集（Visual CoT、ViRL）以及Hugging Face Trainer与DeepSpeed实现，训练时冻结视觉编码器和多模态投影器，仅更新LLM参数。这些选择有助于保证对比的公平性与结果的复现性。然而，部分子任务（如V*_D.A.和V*_R.P.）的提升幅度来自对基线得分的推算，文中未直接报告基线的精确值，对应断言需交叉核对原始数据方可确认。

## 方法谱系与知识库定位

LVR 的提出本质上是对“文本空间推理”与“借助外部工具推理”两种主流范式的根本性突破。当前多模态大模型虽然配备先进视觉编码器，但因模态投影偏差与跨模态注意力偏差，骨干语言模型常难以捕获与文本查询最相关的视觉细节，导致视觉输入与最终答案之间存在断层。已有的“Think about Images”（如 Vision‑R1）仅以文本 token 进行推理，视觉信号被冻结在编码器输出之后无法动态修正；“Think with Images”（如 PAPO、PixelReasoner）则依赖外部工具对图像进行操作，虽然可引入额外视觉信息，但引入了工具调度与执行延迟，且推理过程并非内在统一于语言模型。LVR 放弃了这两种思路，转而将推理空间从离散文本 token 扩展至连续的视觉 token：语言模型在潜在空间中直接重建查询相关的视觉语义，而后将重建的视觉信号作为后续文本生成的条件，从而从根本上打通视觉与语言的联合推理。

在具体实现上，LVR 在推理阶段通过特殊 token（`<|lvr_start|>`, `<|lvr_end|>`）触发与终止潜在推理，使语言模型在每一推理步中将其最后一个隐藏状态逼近目标视觉嵌入，执行多次迭代后返回文本生成模式。该方法的基础架构与 Qwen2.5‑VL 等标准 MLLM 完全兼容——它复用了原有的视觉编码器、多模态投影器以及语言模型主干，仅增加了潜在推理的控制逻辑和联合训练目标。在 SFT 阶段，训练依赖边界框标注数据，以真实视觉嵌入监督隐藏状态，联合优化文本生成交叉熵与视觉重建均方误差；在 RL 阶段，作者提出 `GRPO_latent` 变体，通过重放潜在隐藏状态计算 token 级重要性比率，对纯文本输出进行策略梯度更新，避免新增视觉恢复任务的奖励设计。与纯文本 RL（如 Vision‑R1 的策略）不同，`GRPO_latent` 明确适配了推理过程中隐藏状态的传递，这是 LVR 区别于其他强化学习多模态基线的重要设计点。

从实验证据看，LVR 相对于基线的提升集中体现在视觉细节敏感的基准上。7B 模型上，LVR（4 步）在 MMVP 上达到 72.0%，较 Qwen2.5‑VL 基线的 66.67% 提升 5.33 个百分点；在 V* 基准上，LVR（8 步）取得 81.7%（总体）、84.4%（V*_D.A.）和 77.6%（V*_R.P.），超越所有开源基线，表明潜在视觉推理在需要精确定位和细粒度属性判断的任务中具有明显优势。进一步，消融实验（表 3）显示：不额外增加投影头的“标准 LVR”在所有视觉基准上表现最佳，说明语言模型原生即可对齐视觉与文本语义，无需复杂的中间映射层；相反，使用可学习 Latent End Token 的中止策略极不稳定，在 V* 上骤降至 39.8%，而“模式切换损失”常导致潜在推理步数崩溃至零，被迫退化为纯文本推理。这些证据指向一个核心结论：LVR 的关键增益机制在于让语言模型直接掌握何时以及如何通过隐藏状态重建视觉信号，任何试图通过额外损失或学习 token 来强制切换的行为都会破坏已学到的隐式对齐。

基于以上特性，LVR 的适用边界与当前局限也十分清晰。第一，范式目前主要针对单图像、单轮问答任务设计，实验覆盖的基准（MMVP、V*、CV‑Bench 等）均为单图场景；在多图像推理（如 Relative Reflect）上表现不足，需要跨图像数据增强等补充技术。第二，推理过程的长度控制尚未达到灵活自适应：固定步数策略虽然可靠，但缺乏任务相关的动态性；可学习的中止 token 与模式切换损失均未能稳定工作，意味着可变长度潜在推理仍是开放问题。第三，监督微调的数据高度依赖边界框标注（用于标记查询相关区域），限制了训练规模的可扩展性——尽管 RL 阶段不再需要框标注，但 SFT 的质量仍受限于人工标注数据的覆盖度。第四，论文仅在视觉问答领域验证了有效性，尚未探索视频理解、具身推理等包含时间序列或多模态输入的更复杂场景。第五，计算开销与推理延迟未给出定量分析；高步数潜在推理需要额外前向传播，可能增加显存占用和响应时间，对部署环境的约束尚不明确。

综合来看，LVR 在方法谱系上可被定位为一种“原生多模态联合推理”的测试时增强技术，它既不同于纯文本推理的“Think about Images”路线，也不同于借助外部工具的“Think with Images”路线，而是利用语言模型已有的语义空间完成视觉信号的重建与补充。其知识库贡献在于：首次系统验证了将连续视觉 token 纳入语言模型内部循环推理的可行性，并通过详细的消融与强化学习实验揭示了最优设计应遵循“少即多”原则——即不应引入繁复的外部映射或强行切换，而应信任语言模型自身对联合语义的表征能力。然而，当前方法仍存在多帧扩展不力、长度控制不稳定、数据依赖性强等瓶颈，未来工作需围绕以下方向展开：① 研究适用于多图像、视频序列的跨帧潜在推理，通过交叉注意力或时空 token 聚合实现联合视觉语义恢复；② 设计基于置信度估计或上下文动态中止的条件机制，取代固定步数，实现可变长推理；③ 探索利用大规模无监督图文对进行预训练（例如以图文匹配度作为重建质量的弱监督信号），减少对精细框标注的依赖；④ 评估潜在推理在不同模态（如音频、触觉）中的迁移能力，推动全模态统一推理；⑤ 量化推理效率，通过蒸馏、稀疏化或提前退出策略在性能与成本之间取得平衡。对于更复杂的数学、规划类任务，LVR 是否需要与结构化外部工具协同仍有待验证，这可能是该范式下一个重要的交叉点。

## 原文 PDF

![[paperPDFs/ICLR_2026/Latent_Visual_Reasoning.pdf]]
