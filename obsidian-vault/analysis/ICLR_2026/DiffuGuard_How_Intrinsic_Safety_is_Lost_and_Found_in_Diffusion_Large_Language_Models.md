---
title: "DiffuGuard: How Intrinsic Safety is Lost and Found in Diffusion Large Language Models"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/DiffuGuard_How_Intrinsic_Safety_is_Lost_and_Found_in_Diffusion_Large_Language_Models.pdf
openreview_forum_id: zBPzxhso8M
aliases:
- DiffuGuard
tags:
- ICLR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: "通过在重掩码过程中引入可控随机性（尤其在早期步骤注入更强的随机性以激活安全性token）并结合块级安全审计（利用内部表征偏差检测越狱攻击并执行引导式修正），可以有效激活dLLM的内在安全能力。"
primary_logic: "dLLM具备显著的内在安全潜力——模型在深层表征中已能区分安全与有害内容，但当前贪婪解码策略过早剪枝了安全性路径；通过改进解码范式（而非重新训练模型），可以在保持生成质量的前提下大幅释放这种潜力。"
claims:
- "贪婪重掩码策略相比于引入随机性的策略，在WildJailbreak上使ASR升高约10.3%"
- "早期安全token注入相比中期注入可多降低ASR约22.6%，验证了Denoising-path Dependence"
- "DIFFUGUARD将六种越狱攻击的平均ASR从47.9%降至14.7%（降低约33.2%）"
- "块级审计与修复模块对防御利用dLLM内在机制的攻击（如PAD、DIJA）至关重要——移除该模块后PAD攻击ASR从59.62%飙升至约90%"
---

# DiffuGuard: How Intrinsic Safety is Lost and Found in Diffusion Large Language Models

> [!tip] 核心洞察
> dLLM具备显著的内在安全潜力——模型在深层表征中已能区分安全与有害内容，但当前贪婪解码策略过早剪枝了安全性路径；通过改进解码范式（而非重新训练模型），可以在保持生成质量的前提下大幅释放这种潜力。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | DiffuGuard：扩散大语言模型内在安全性的丧失与找回 |
| 英文题名 | DiffuGuard: How Intrinsic Safety is Lost and Found in Diffusion Large Language Models |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=zBPzxhso8M); [GitHub](https://github.com/niez233/DiffuGuard) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | DIFFUGUARD |
| Dataset | 六种越狱攻击综合（WildJailbreak, JBB-Behaviors, PAD_AdvBench, DIJA_AdvBench, AutoDAN_AdvBench, GCG_AdvBench）, WildJailbreak (LLaDA-8B-Instruct + DIFFUGUARD + Self-reminder), PAD_AdvBench (LLaDA-8B-Instruct + DIFFUGUARD + Self-reminder), PAD_AdvBench (Dream-v0-Instruct-7B + DIFFUGUARD + Self-reminder) |

> [!tip] 效果简介
> - 六种越狱攻击综合（WildJailbreak, JBB-Behaviors, PAD_AdvBench, DIJA_AdvBench, AutoDAN_Adv... 上，Average ASR (%) 为 14.7，对比 47.9，变化 ↓33.2。
> - WildJailbreak (LLaDA-8B-Instruct + DIFFUGUARD + Self-reminder) 上，ASR (%) 为 8.50，对比 23.95，变化 ↓15.45。
> - PAD_AdvBench (LLaDA-8B-Instruct + DIFFUGUARD + Self-reminder) 上，ASR (%) 为 24.42，对比 93.65，变化 ↓69.23。

## 概述

### 1. 问题背景

扩散大语言模型（dLLM）通过迭代去噪与并行生成机制实现了推理效率的突破，但其解码范式本身构成了独特的安全瓶颈。与自回归模型不同，dLLM的安全性脆弱性在两个正交维度上展开：

- **Intra-step维度**：贪婪的低置信度重掩码策略在每一步的并行生成中放大了有害token的选择偏差，导致有害内容在单步内被系统性强化。
- **Inter-step维度**：去噪路径依赖性（Denoising-path Dependence）使得早期步骤中token的安全性对最终输出产生决定性影响——有害token一旦被引入，便通过迭代去噪过程持续传播并自我强化。

实验证据表明，仅改变重掩码策略中的贪婪程度即可使WildJailbreak上的攻击成功率（ASR）产生约10.3%的波动；而在早期步骤注入安全token相比中期注入可多降低ASR约22.6%，进一步验证了路径依赖性的关键作用。

### 2. 核心发现

dLLM并非缺乏安全能力，而是其内在安全潜力被当前解码策略过度压抑。深层表征分析显示，LLaDA模型在第27层已能明确区分安全与有害token——代表拒绝的“Sorry”和代表顺从的“Here”在不同位置同时获得高概率，形成内部安全冲突。然而，贪婪重掩码策略过早剪枝了安全性路径，使得模型在越狱攻击面前表现出脆弱性。

这一发现指向一个关键洞察：**通过改进解码范式而非重新训练模型，可以在保持生成质量的前提下大幅释放dLLM的内在安全能力。**

### 3. DIFFUGUARD方法定位

基于上述分析，DIFFUGUARD提出了一种训练无关的双阶段防御框架，分别针对两个维度的脆弱性：

- **随机退火重掩码（Stochastic Annealing Remasking）**：在intra-step层面引入可控随机性，打破贪婪选择的有害路径。通过步数感知的退火调度，在早期步骤注入更强随机性以激活安全性token，后期逐步恢复置信度选择以保证生成质量。
- **块级审计与修复（Block-level Audit and Repair）**：在inter-step层面利用模型内部表征进行自主安全风险检测，对不安全块执行回退重掩码与引导式再生成，阻断有害内容的跨块传播。

该方法属于推理时防御范式，与基于输入困惑度过滤的**PPL-Filter**（Alon & Kamfonas, 2023）、系统提示注入的**Self-reminder**（Xie et al., 2023）等传统防御策略互补，并可有效防御利用dLLM内在机制的专用攻击，如**PAD**（Zhang et al., 2025b）和**DIJA**（Wen et al., 2025）。

### 4. 主要结果

DIFFUGUARD在四个dLLM家族（LLaDA-8B-Instruct、Dream-v0-Instruct-7B、LLaDA-1.5、MMaDA-8B-MixCoT）和六种越狱攻击方法（WildJailbreak、JBB-Behaviors、PAD、DIJA、AutoDAN、GCG）上进行了全面评估：

- 将六种攻击的**平均ASR从47.9%降至14.7%**（降低约33.2个百分点）。
- 在PAD_AdvBench上，LLaDA-8B的ASR从93.65%降至24.42%（↓69.23）；Dream-v0-Instruct-7B从99.23%降至37.31%（↓61.92）。
- 消融实验证实，块级审计与修复模块是防御dLLM特定攻击的关键——移除后PAD攻击ASR从59.62%飙升至约90%。

框架对模型通用能力（MMLU、GSM8K、HumanEval）和推理速度的影响可忽略，实现了安全性与实用性的有效平衡。

## 背景与动机

### 扩散语言模型的解码范式与安全盲区

离散扩散语言模型（dLLM）通过迭代去噪生成文本，其核心流程为：从全`[MASK]`序列开始，在每一步 $n$ 中并行预测所有掩码位置的候选token，再通过重掩码策略选择部分位置保留，其余位置重新掩码后进入下一步迭代：

$$\mathcal{T}^n = f_\theta(p_0 \oplus \mathcal{T}^{n-1}), \quad n \in \{1, \ldots, N\}$$

$$\hat{\tau}_i^n \sim P_\theta(\cdot \mid p_0 \oplus \mathcal{T}^{n-1}), \quad \mathbb{Z} = \underset{i \in \{1,\ldots,L\}}{\arg\operatorname{top-}k} \operatorname{Prob}(\hat{\tau}_i^n)$$

这种并行生成与迭代精炼的范式带来了效率优势，但也引入了传统自回归语言模型（AR LLM）中不存在的安全脆弱性。DiffuGuard将dLLM的安全分析分解为两个正交维度：

- **Intra-step层面**：标准解码采用贪婪的低置信度重掩码策略——基于绝对logits概率选择top-k位置保留。这一策略在越狱查询下会放大有害token的选择偏差，因为模型深层表征中已同时激活了拒绝token（如"Sorry"）和服从token（如"Here"）的高概率（见Figure 2），而贪婪选择倾向于剪枝安全性路径。实验表明，相比于引入随机性的策略，贪婪重掩码在WildJailbreak上使攻击成功率（ASR）升高约10.3%。

- **Inter-step层面**：dLLM的去噪过程存在**去噪路径依赖性**（Denoising-path Dependence）——早期步骤中被保留的token会通过迭代精炼持续影响后续步骤的输出方向。一旦早期步骤引入了有害token（如"Sure"），模型会在后续步骤中围绕该token构建服从性响应，形成有害内容的自我强化循环。实验证实：在生成第一步强制注入安全token "Sorry"相比在中期步骤注入，可多降低ASR约22.6%（见Figure 5）。

### 现有防御方法的缺口

当前针对LLM越狱攻击的防御策略主要围绕AR LLM设计，存在以下不足：

- **基于提示困惑度的过滤**（如PPL-Filter, Alon & Kamfonas, 2023）仅检查输入层面的统计异常，无法应对精心构造的越狱模板。
- **系统提示注入安全指令**（如Self-reminder, Xie et al., 2023）依赖模型遵循指令的能力，在强攻击下效果有限。
- **针对dLLM的专用攻击已出现**：DIJA（Wen et al., 2025）和PAD（Zhang et al., 2025b）利用dLLM的in-place prompting机制，通过将恶意意图嵌入生成块内部来绕过安全机制，传统防御对此几乎无效——PAD攻击在LLaDA-8B-Instruct上可达93.65%的ASR。

更重要的是，**dLLM具备显著的内在安全潜力**：模型在深层表征中已能区分安全与有害内容（Figure 2d显示Layer 27处拒绝与服从token的分布分离），但当前贪婪解码策略过早剪枝了安全性路径。这意味着通过改进解码范式——而非重新训练模型——即可释放这种潜力。

### DiffuGuard的核心动机

DiffuGuard的核心洞察是：dLLM的安全瓶颈根植于解码策略，而非模型能力缺失。因此，该框架以**训练无关**（training-free）的方式，从intra-step和inter-step两个层面同时介入：

1. **随机退火重掩码**（Stochastic Annealing Remasking）：在重掩码过程中引入可控随机性，尤其在早期步骤注入更强随机性以激活安全性token，打破贪婪选择对有害路径的锁定。
2. **块级审计与修复**（Block-level Audit and Repair）：利用模型内部表征偏差检测越狱攻击，并对不安全块执行引导式修正，阻断有害内容的跨块传播。

该框架在四个dLLM家族（LLaDA-8B-Instruct、Dream-v0-Instruct-7B、LLaDA-1.5、MMaDA-8B-MixCoT）和六种越狱攻击方法上进行了验证，将平均ASR从47.9%降至14.7%（降低约33.2%），同时保持生成质量和推理速度几乎不受影响。

## 核心创新

DIFFUGUARD的核心洞察在于：扩散大语言模型（dLLM）本身具备显著的内在安全能力——模型在深层表征中已能区分安全与有害内容（如Figure 2所示，越狱查询在Layer 27同时激活了拒绝性token与合规性token），但当前解码范式过早剪枝了安全性路径。因此，DIFFUGUARD选择了一条**训练无关的解码侧防御路线**，通过改造两个关键解码槽位来释放模型被压抑的安全潜力，而非重新训练模型。

### 瓶颈诊断：dLLM解码的两重安全脆弱性

dLLM的安全脆弱性可沿两个正交维度分解：

**Intra-step层面——贪婪重掩码的选择偏差。** 标准dLLM解码在每一步采用基于绝对logits概率的贪婪top-k选择来保留token（Eq. 2），这种低置信度重掩码策略在有安全风险的生成场景中会系统性放大有害token的选择偏差。实验证据表明，将贪婪策略替换为引入随机性的策略后，WildJailbreak上的攻击成功率（ASR）降低约10.3%，直接验证了贪婪选择是安全漏洞的关键推手。

**Inter-step层面——去噪路径依赖性（Denoising-path Dependence）。** dLLM的迭代去噪过程具有强烈的路径依赖：早期步骤确定的token会对后续所有步骤的生成产生决定性影响。Figure 4和Figure 5的实验量化了这一效应：强制将首个token设为`Sure`使ASR飙升76.9%，而设为`Sorry`则使ASR降低24.3%；更关键的是，在64步生成中，安全token注入的时机越早效果越显著——早期注入相比中期注入可多降低ASR约22.6%。这意味着有害内容一旦在早期被引入，就会通过迭代去噪持续强化，形成“有害锁死”。

### 创新槽位一：随机退火重掩码（Stochastic Annealing Remasking）

**基线做法：** 标准dLLM使用基于绝对logits概率的贪婪选择，即直接在预测概率上取top-k保留token位置，完全忽视低概率但可能安全的候选路径。

**DIFFUGUARD改进：** 在重掩码的置信度评分中注入可控随机噪声，将选择依据从确定性概率改为概率与随机性的加权混合：

$$\mathcal{Z} = \underset{i \in \{1,\ldots,L\}}{\arg\operatorname{top-}k} \left[(1-\alpha)\cdot\operatorname{Prob}(\hat{\tau}_i^n) + \alpha\cdot R_i\right], \quad R_i \sim U(0,1)$$

其中$\alpha$为随机性权重，$R_i$为均匀随机噪声。这一设计的目的是打破贪婪策略对有害路径的过早锁定，为安全性token（如拒绝性表达）保留被选中的概率空间。

**退火调度——步数感知的随机性衰减：** 仅引入随机性会在提升安全性的同时损害生成质量（Figure 3展示了这一trade-off）。DIFFUGUARD通过步数感知的退火调度来平衡二者：

$$\alpha_n = \alpha_0\left(1 - \frac{n-1}{N-1}\right)$$

随机性权重从初始值$\alpha_0$线性衰减至第$N$步的0。这意味着在早期步骤注入最强的随机性（此时正是安全性路径最容易被剪枝的阶段），而随着生成逐步收敛，恢复置信度主导的选择以保证输出质量。这一调度策略直接响应了Denoising-path Dependence的发现：早期干预的收益远大于后期。

### 创新槽位二：块级审计与修复（Block-level Audit and Repair）

**基线做法：** 标准dLLM无任何显式安全检测或修正机制，有害内容一旦生成便自由传播到后续所有块。

**DIFFUGUARD改进：** 利用模型自身的内部表征构建自主安全监控与自我修正闭环，包含两个子阶段：

**审计（Audit）——基于表征偏差的越狱检测。** 核心指标为安全偏离度（Safety Divergence），计算原始恶意意图$p_{\text{origin}}$与完整越狱提示$p_0$在输出层隐藏状态的余弦距离：

$$\mathrm{SD}(p_0, p_{\text{origin}}) = 1 - \frac{\mathbf{h}_{\text{origin}} \cdot \mathbf{h}_{p_0}}{\|\mathbf{h}_{\text{origin}}\| \cdot \|\mathbf{h}_{p_0}\|}$$

高SD值表明越狱模板已显著扭曲了模型的安全响应表征，当SD超过阈值$\lambda$时触发修复。这一设计的关键洞察是：模型内部表征已经编码了安全与有害的区分信息（见Figure 2），审计模块只是将这种隐式知识显式化为可操作的检测信号。

**修复（Repair）——回退重掩码与引导式再生成。** 对触发审计警报的块执行两步修正：首先按比例$\gamma$随机将非提示token回退为`[MASK]`（Block Remask），然后在再生成阶段将原始有害token的logits设为$-\infty$以强制模型探索安全路径（Guided Regeneration）。修复仅对第一个生成的块激活，以在阻断有害内容源头的同时最小化推理延迟开销。

### 创新定位：训练无关的解码范式改造

DIFFUGUARD的核心创新定位在于**不触及模型权重，仅改造解码范式**。这与传统的安全对齐训练（如RLHF）形成互补而非替代关系：

- **Stochastic Annealing Remasking** 通过改造intra-step的选择机制，解决贪婪策略对安全路径的过早剪枝问题；
- **Block-level Audit and Repair** 通过改造inter-step的传播机制，利用模型内在表征进行自主检测与修正，阻断有害内容的跨块级联。

消融实验（Table 2）量化了两个槽位各自的贡献：移除Block-level Audit and Repair后，LLaDA-8B在PAD_AdvBench上的ASR从59.62%急剧上升至约90%，说明该模块是防御利用dLLM内在机制的攻击（如PAD、DIJA）的关键组件；移除Stochastic Annealing Remasking也会导致防御性能下降，尤其在预优化提示攻击（如AutoDAN）上表现明显。两个模块的互补性验证了从intra-step和inter-step双维度同时介入的必要性。

## 整体框架

![[assets/figures/papers/paper_list_l33_https_openreview_net_forum_id_zBPzxhso8M/figures/001_Figure_1.jpg]]
*Figure 1: Left. The generation diagram of dLLMs; Middle. The unique vulnerabilities of dLLMs, including the intra-step and the inter-step level; Right. DIFFUGUARD framework achieves significant safety improvements while having minimal impact on model performance and inference latency*

DIFFUGUARD是一个训练无关的推理时防御框架，针对扩散大语言模型（dLLM）在越狱攻击下的独特脆弱性而设计。其核心洞察在于：dLLM本身具备显著的内在安全潜力——模型在深层表征中已能区分安全与有害内容，但当前贪婪解码策略过早剪枝了安全性路径。DIFFUGUARD通过改进解码范式而非重新训练模型，在保持生成质量的前提下释放这种潜力。

框架由两个协同模块构成，分别对应dLLM安全脆弱性的两个正交维度：

### 模块一：随机退火重掩码（Stochastic Annealing Remasking）

该模块作用于**intra-step**层面，旨在打破贪婪低置信度重掩码策略对有害token的选择偏差。在标准dLLM解码中，每个去噪步骤根据token预测概率选择top-k位置保留，其余位置回退为`[MASK]`。这种确定性选择在越狱场景下会系统性地放大有害token的保留概率。

DIFFUGUARD将标准置信度评分与均匀随机噪声按比例混合：

$$\mathcal{Z} = \underset{i \in \{1,\ldots,L\}}{\arg\operatorname{top-}k} \left[(1-\alpha)\cdot\operatorname{Prob}(\hat{\tau}_i^n) + \alpha\cdot R_i\right], \quad R_i \sim U(0,1)$$

其中$\alpha$控制随机性强度。为平衡安全性与生成质量，框架采用步数感知的退火调度：

$$\alpha_n = \alpha_0\left(1 - \frac{n-1}{N-1}\right)$$

随机性权重从初始值$\alpha_0$线性衰减至第$N$步的零，在早期步骤注入最强随机性以激活安全性token路径，后期恢复置信度选择以保证输出质量。

### 模块二：块级审计与修复（Block-level Audit and Repair）

该模块作用于**inter-step**层面，利用模型内部表征进行自主安全风险检测与修正，阻断有害内容的跨块传播。dLLM的块级自回归生成方式使得早期块的安全性对最终输出具有决定性影响（即去噪路径依赖性，Denoising-path Dependence）。

**审计阶段**：计算完整越狱提示$p_0$与原始恶意意图$p_{\text{origin}}$在输出层隐藏状态的余弦距离，作为安全偏离度指标：

$$\mathrm{SD}(p_0, p_{\text{origin}}) = 1 - \frac{\mathbf{h}_{\text{origin}} \cdot \mathbf{h}_{p_0}}{\|\mathbf{h}_{\text{origin}}\| \cdot \|\mathbf{h}_{p_0}\|}$$

当$\mathrm{SD}$超过阈值$\lambda$时，表明越狱模板已显著扭曲模型的安全响应，触发修复流程。

**修复阶段**包含两步操作：（1）**块重掩码**：按比例$\gamma$随机将已生成块中的非提示token回退为`[MASK]`；（2）**引导式再生成**：将原始有害token的logits设为$-\infty$，强制模型探索安全路径。该修复仅对第一个生成的块激活，以阻断有害内容源头同时最小化推理延迟。

### 输入输出流

整个pipeline的输入为提示$p_0$，输出为经过安全防护的生成文本。在每个生成步骤内，随机退火重掩码模块介入token保留决策；在每个块生成完成后，审计模块评估安全风险并决定是否触发修复。两个模块协同工作：随机退火从源头降低有害路径被选中的概率，审计修复则作为安全网捕获并纠正漏网的有害输出。

## 核心模块与公式推导

DIFFUGUARD是一个训练无关的推理时防御框架，由两个正交模块构成，分别对应dLLM安全脆弱性的两个维度：**随机退火重掩码**（Stochastic Annealing Remasking）解决intra-step层面的贪婪选择偏差，**块级审计与修复**（Block-level Audit and Repair）阻断inter-step层面的有害内容跨块传播。

### 随机退火重掩码

dLLM的标准解码在每一步通过top-k置信度选择保留的token位置：

$$\mathcal{Z} = \underset{i \in \{1,\ldots,L\}}{\arg\operatorname{top-}k} \operatorname{Prob}(\hat{\tau}_i^n)$$

该贪婪策略在越狱场景下会系统性地放大有害token的选择偏差。DIFFUGUARD的核心创新是将置信度评分与均匀随机噪声按比例混合：

$$\mathcal{Z} = \underset{i \in \{1,\ldots,L\}}{\arg\operatorname{top-}k} \left[(1-\alpha)\cdot\operatorname{Prob}(\hat{\tau}_i^n) + \alpha\cdot R_i\right], \quad R_i \sim U(0,1)$$

其中 $\alpha$ 为随机性平衡因子，$R_i$ 为从均匀分布采样的独立噪声。为平衡安全性与生成质量，引入步数感知的退火调度：

$$\alpha_n = \alpha_0\left(1 - \frac{n-1}{N-1}\right)$$

该调度使随机性权重从初始值 $\alpha_0$ 线性衰减至第 $N$ 步的零，在早期步骤注入最强随机性以激活安全性token路径，后期恢复置信度主导以保证生成质量。

### 块级审计与修复

dLLM以块为单位迭代生成，早期块的安全性对最终输出具有决定性影响（Denoising-path Dependence）。块级审计通过比较原始恶意意图 $p_{\text{origin}}$ 与完整越狱提示 $p_0$ 在输出层隐藏状态的余弦距离来检测攻击：

$$\mathrm{SD}(p_0, p_{\text{origin}}) = 1 - \frac{\mathbf{h}_{\text{origin}} \cdot \mathbf{h}_{p_0}}{\|\mathbf{h}_{\text{origin}}\| \cdot \|\mathbf{h}_{p_0}\|}$$

高SD值表明越狱模板显著扭曲了模型的安全响应表征。当SD超过阈值 $\lambda$ 时触发修复流程，该流程仅对第一个生成块激活以最小化延迟开销。修复包含两个子阶段：

- **块重掩码**（Block Remask）：按比例 $\gamma$ 随机选取非提示token位置回退为 `[MASK]`。
- **引导式再生成**（Guided Regeneration）：将原始有害token的logits设为 $-\infty$，强制模型探索安全路径：

$$\mathrm{Logits}'(\tilde{\tau}_i) = \begin{cases} -\infty & \text{if } \tilde{\tau}_i = \tau_i^N \text{ and } i \in \mathcal{T}_{\text{remask}}, \\ \mathrm{Logits}(\tilde{\tau}_i) & \text{otherwise} \end{cases}$$

消融实验（Table 2）证实：移除块级审计与修复模块后，LLaDA-8B在PAD_AdvBench上的ASR从59.62%急剧上升至约90%，说明该模块是防御利用dLLM内在机制攻击的关键组件；移除随机退火重掩码同样导致防御性能下降，但在AutoDAN等攻击上影响相对较小。

## 实验与分析

### 主实验结果

DIFFUGUARD在四个dLLM家族模型（LLaDA-8B-Instruct、Dream-v0-Instruct-7B、LLaDA-1.5、MMaDA-8B-MixCoT）和六种越狱攻击方法上进行了全面评估。综合来看，DIFFUGUARD将平均攻击成功率（ASR）从**47.9%降至14.7%**，降幅约33.2个百分点（Table 1）。


![[assets/figures/papers/paper_list_l33_https_openreview_net_forum_id_zBPzxhso8M/figures/006_Table_1.jpg]]
*Table 1: A Comprehensive Evaluation of DIFFUGUARD’s Safeguarding Performance. The table reports ASR(%), where bold and underline denote the best and the second-best values respectively*

**跨攻击类型防御效果**：DIFFUGUARD对不同攻击类型展现出差异化的防御能力。在预优化提示攻击（WildJailbreak、JBB-Behaviors）上表现最为突出——LLaDA-8B-Instruct在WildJailbreak上的ASR从23.95%降至8.50%（↓15.45），Dream-v0-Instruct-7B在JBB-Behaviors上仅1.05%。对于利用dLLM内在机制的专用攻击（PAD、DIJA），防御效果同样显著但绝对ASR仍相对较高：LLaDA-8B-Instruct在PAD_AdvBench上从93.65%降至24.42%（↓69.23），在DIJA_AdvBench上从98.65%降至39.04%（↓59.61）。

**跨模型内在安全性差异**：不同dLLM家族的内在安全水平存在显著差异（Section F.1）。Dream系列继承自Qwen2.5-7B的预对齐权重，安全性最高；LLaDA系列代表原生dLLM的安全基线；MMaDA系列因推理能力增强训练导致“Safety Tax”现象，安全性最弱——其Vanilla模型在WildJailbreak上ASR高达72.75%，DIFFUGUARD可将其降至14.25%（↓58.50）。

**与现有防御方法的协同**：DIFFUGUARD与Self-reminder（系统提示注入安全指令）组合使用时效果最佳。单独使用Self-reminder对PAD和DIJA等dLLM专用攻击几乎无效（ASR分别为93.65%和98.65%），但叠加DIFFUGUARD后分别降至24.42%和39.04%，说明DIFFUGUARD在防御机制上与提示层面的安全干预互补。

### 消融实验

Table 2的消融实验量化了两个核心模块各自的贡献：


![[assets/figures/papers/paper_list_l33_https_openreview_net_forum_id_zBPzxhso8M/figures/009_Table_2.jpg]]
*Table 2: Ablation study on the contribution of each component in DIFFUGUARD*

**Block-level Audit and Repair的不可替代性**：移除该模块后，LLaDA-8B在PAD_AdvBench上的ASR从59.62%急剧上升至约90%，验证了块级审计与修复是防御利用dLLM内在机制攻击（PAD、DIJA）的关键组件。这类攻击通过in-place prompting直接操纵模型的生成过程，仅靠随机性注入无法有效阻断。

**Stochastic Annealing Remasking的独立贡献**：单独移除随机退火重掩码也会导致防御性能下降，尤其在AutoDAN等预优化攻击上明显，但影响程度小于Audit and Repair模块。这印证了分析中的论断——随机退火重掩码主要防御Pre-optimized Prompt Attacks，而块级审计与修复针对dLLM特有攻击。

**模块协同效应**：两个模块同时启用时防御效果最优，说明intra-step层面的随机性注入与inter-step层面的安全审计存在互补关系——随机性降低了有害路径被选中的概率，审计与修复则对漏网的有害内容进行事后纠正。

### 安全性-通用能力权衡

Figure 6以雷达图展示了DIFFUGUARD对模型通用能力的边际影响。在MMLU、GSM8K、HumanEval等基准上，LLaDA和Dream模型应用DIFFUGUARD前后的性能几乎无衰减，同时PAD和WildJailbreak的防御成功率大幅提升。


![[assets/figures/papers/paper_list_l33_https_openreview_net_forum_id_zBPzxhso8M/figures/007_Figure_6.jpg]]
*Figure 6: Performance comparison of LLaDA (left) and Dream (right) across multiple metrics, such as safety and general capabilities, before and after applying DIFFUGUARD*

**超参数α₀的敏感性**（Table 7）：较高的初始随机性α₀值可有效降低ASR，但需要在安全性与通用能力之间权衡。Dream模型在α₀=0.3时GSM8K准确率为76.35%，WildJailbreak ASR仅2.35%；当α₀增至0.5时，ASR进一步下降但通用能力开始出现可感知的退化。LLaDA模型对α₀的变化更为敏感，需要在更窄的范围内调参。


![[assets/figures/papers/paper_list_l33_https_openreview_net_forum_id_zBPzxhso8M/figures/015_Table_7.jpg]]
*Table 7: The impact of hyperparameter α0 on model safety and general capability*

**推理延迟**（Figure 7）：DIFFUGUARD框架引入的推理延迟可忽略不计。这是因为块级修复仅对第一个生成块激活，且随机退火重掩码的计算开销极小。

### 自适应攻击鲁棒性

Table 9评估了DIFFUGUARD对三种自适应攻击的鲁棒性：多采样攻击（从多次生成中筛选有害输出）、梯度攻击（利用梯度信息优化越狱提示）、阈值探测攻击（试探性地绕过安全检测阈值）。结果显示DIFFUGUARD在所有自适应攻击场景下仍保持显著低于Vanilla模型的ASR，但梯度攻击和阈值探测攻击确实使ASR有所回升，说明攻击者可能通过探测安全偏离度阈值λ或利用梯度信息来规避检测。

### 失败模式与局限

**MMaDA系列的“Safety Tax”**：MMaDA-8B-MixCoT在应用DIFFUGUARD后ASR仍为14.25%，显著高于LLaDA和Dream系列。这表明增强推理能力的训练可能系统性地削弱了模型的内在安全判别能力，单纯依赖解码策略的改进难以完全弥补训练阶段的安全对齐缺失。

**DIJA攻击的残余风险**：DIJA_AdvBench上DIFFUGUARD的ASR为39.04%，是六种攻击中最高的。DIJA利用in-place prompting机制将恶意意图嵌入提示结构中，使得安全偏离度检测面临挑战——当恶意意图与合法指令高度融合时，SD指标可能无法有效区分。

**评估覆盖的局限性**：当前针对dLLM的专用攻击方法仅有DIJA和PAD两种，评估主要采用了在AR LLM上验证过且具有广泛迁移性的越狱攻击算法。未来dLLM特定攻击的出现可能揭示当前防御框架的盲区。

### 关键图表结论

- **Figure 4（初始Token注入实验）**：使用不安全token（“Sure”）引导生成使ASR升高约76.9%，使用安全token（“Sorry”）使ASR降低约24.3%，直接验证了Denoising-path Dependence——早期token的安全性对最终输出产生决定性影响。

![[assets/figures/papers/paper_list_l33_https_openreview_net_forum_id_zBPzxhso8M/figures/004_Figure_4.jpg]]
*Figure 4: Effect of Initial Tokens on dLLM ASR. We compare the final safety performance when guiding generation with unsafe tokens (e.g.,$^ { 6 6 } { \sf$ S u r e $} ^ { , 9 }$ ) versus safe tokens (e.g., “Sorry”), benchmarked against various baseline methods*

- **Figure 5（安全Token注入时机）**：在64步生成过程中，将“Sorry”注入第1步时ASR仅0.2%，延迟至第32步时ASR升至22.8%。早期干预相比中期干预可多降低ASR约22.6%，证实了安全干预的时机敏感性。

![[assets/figures/papers/paper_list_l33_https_openreview_net_forum_id_zBPzxhso8M/figures/005_Figure_5.jpg]]
*Figure 5: ASR as a Function of the Safe Token Injection Step. The experiment was conducted over 64 generation steps, where we forcibly set the first position to “Sorry” at various steps (1, 2, 4, 8, 16, and 32) and recorded the final ASR*

- **Figure 8（防御案例研究）**：在WildJailbreak攻击实例中，Vanilla模型直接输出有害化学物质列表，DIFFUGUARD则生成教育性拒绝回复；在PAD_AdvBench攻击实例中，Vanilla模型完全遵从恶意指令，DIFFUGUARD成功识别并阻断有害生成。

### 补充图表

![[assets/figures/papers/paper_list_l33_https_openreview_net_forum_id_zBPzxhso8M/figures/011_Table_3.jpg]]
*Table 3: Hyperparameter Settings for Section 3.2*

![[assets/figures/papers/paper_list_l33_https_openreview_net_forum_id_zBPzxhso8M/figures/012_Table_4.jpg]]
*Table 4: Hyperparameter Settings for Section 3.3*

![[assets/figures/papers/paper_list_l33_https_openreview_net_forum_id_zBPzxhso8M/figures/013_Table_5.jpg]]
*Table 5: Generation hyperparameter settings for Section 5.2*

![[assets/figures/papers/paper_list_l33_https_openreview_net_forum_id_zBPzxhso8M/figures/014_Table_6.jpg]]
*Table 6: DIFFUGUARD hyperparameter settings for Section 5.2*

![[assets/figures/papers/paper_list_l33_https_openreview_net_forum_id_zBPzxhso8M/figures/016_Table_8.jpg]]
*Table 8: Comparison of λ and γ on model safety. All values are ASR (%)*



## 方法谱系与知识库定位

### 1. 与现有防御方法的关系

DIFFUGUARD 属于**训练无关的推理时防御框架**，其设计出发点和适用边界与现有安全防御方法存在本质差异。

**与 AR LLM 防御方法的对比。** 传统自回归语言模型的安全防御主要依赖三类策略：输入过滤（如基于提示困惑度的 **PPL-Filter**，Alon & Kamfonas, 2023）、系统提示注入（如 **Self-reminder**，Xie et al., 2023），以及安全对齐训练（RLHF/DPO 等）。这些方法在 AR LLM 上验证有效，但直接迁移到 dLLM 时面临根本性挑战：dLLM 的并行生成与迭代去噪机制使得传统基于逐 token 自回归假设的防御策略失效。实验证据表明，简单的采样温度调整对 dLLM 越狱攻击**完全无效**（Appendix D.3），说明 AR LLM 的安全经验在 dLLM 范式中需要系统性重审。

DIFFUGUARD 与 Self-reminder 等提示级防御并非互斥关系——实验表明二者可以叠加使用，在 PAD 和 DIJA 攻击上将 ASR 从约 96.8% 降至 27.9%（Table 1），形成互补防御层次。

**与 dLLM 特定攻击的攻防关系。** DIFFUGUARD 的两个核心模块分别针对当前已知的两类 dLLM 越狱攻击机制设计：

- **Stochastic Annealing Remasking** 主要防御预优化提示攻击（如 WildJailbreak、AutoDAN、GCG），通过打破贪婪重掩码策略的选择偏差，在 intra-step 层面阻断有害路径的早期形成。
- **Block-level Audit and Repair** 专门应对利用 dLLM 内在机制的 **in-place prompting 攻击**（如 **PAD**，Zhang et al., 2025b；**DIJA**，Wen et al., 2025）。消融实验直接验证了这一分工：移除 Audit and Repair 模块后，LLaDA-8B 在 PAD_AdvBench 上的 ASR 从 59.62% 急剧上升至约 90%（Table 2），而 Stochastic Annealing Remasking 单独对此类攻击的防御效果有限。

### 2. 适用边界与能力定位

**模型覆盖范围。** DIFFUGUARD 在四个不同 dLLM 家族上验证了有效性：LLaDA-8B-Instruct、Dream-v0-Instruct-7B、LLaDA-1.5 和 MMaDA-8B-MixCoT。这些模型代表了 dLLM 安全能力的完整谱系——Dream 系列继承自 Qwen2.5-7B 的预对齐权重（安全性最高），LLaDA 系列代表原生 dLLM 的安全基线，MMaDA 系列因推理能力增强训练导致 “Safety Tax” 而安全性最弱（Section F.1）。跨模型的 ASR 一致性下降趋势（平均从 47.9% 降至 14.7%，↓33.2%）表明该框架对 dLLM 架构本身具有泛化性，而非依赖特定模型的训练特性。

**攻击覆盖范围。** 评估覆盖六种越狱攻击方法，包括预优化提示攻击（WildJailbreak、JBB-Behaviors、AutoDAN、GCG）和 dLLM 专用攻击（PAD、DIJA）。此外，DIFFUGUARD 对自适应攻击（多采样攻击、梯度攻击、阈值探测攻击）也表现出鲁棒性（Table 9），说明防御机制不仅针对已知攻击有效，对利用 dLLM 解码机制的通用攻击模式同样具备抵抗能力。

**生成质量与推理开销。** 作为训练无关的推理时框架，DIFFUGUARD 的核心优势在于无需重新训练模型即可激活内在安全能力。雷达图（Figure 6）显示，应用框架后 LLaDA 和 Dream 在 MMLU、GSM8K、HumanEval 等通用能力指标上几乎无损失，同时推理延迟开销可忽略（Figure 7）。但超参数敏感性分析（Table 7）揭示了安全性-通用能力之间的权衡：较高的初始随机性 α₀ 可有效降低 ASR（Dream 在 α₀=0.3 时 WildJailbreak ASR 仅 2.35%），但 GSM8K 准确率从约 80% 降至 76.35%，需要在部署时根据安全需求进行调节。

### 3. 局限性与开放问题

**攻击方法论的局限性。** 当前针对 dLLM 的专用攻击方法仅有 DIJA 和 PAD 两种，评估主要采用了在 AR LLM 上验证过且具有广泛迁移性的越狱攻击算法。未来 dLLM 特定攻击（尤其是深度利用双向注意力、并行生成、迭代去噪等独特架构特性的攻击）的出现，将为防御策略的评估和迭代提供更精确的目标，也可能暴露当前框架未覆盖的脆弱面。

**威胁模型边界。** DIFFUGUARD 聚焦于推理时越狱攻击，未涵盖训练时威胁（如后门攻击、数据投毒等）。dLLM 特定的训练时攻击方法论尚未建立，这构成了一个重要的安全研究空白。

**互补路径的探索。** 作为训练无关框架，DIFFUGUARD 在通用性和部署灵活性上有优势，但对于深度利用模型机制的攻击（如 in-place prompting），直接通过安全对齐训练增强模型内在判别能力是一条重要且互补的技术路径。如何将 DIFFUGUARD 检测到的攻击样本用于对抗训练，实现推理时防御与训练时对齐的闭环，是尚未探索的方向。

**“Safety Tax” 现象。** MMaDA 系列表现出的推理能力增强训练削弱安全性的现象，说明复杂推理能力与安全性之间存在深层 trade-off。这一现象在多大程度上会泛化到其他推理增强型 dLLM，以及如何在训练阶段进行专门的安全对齐，仍是开放问题。

**Dream 系列的安全迁移机制。** Dream 系列从 AR 模型（Qwen2.5-7B）继承安全对齐能力的机制能否被形式化并迁移到原生 dLLM 的训练中，对于提升整个 dLLM 家族的安全基线具有重要意义，但当前缺乏系统性研究。

## 原文 PDF

![[paperPDFs/ICLR_2026/DiffuGuard_How_Intrinsic_Safety_is_Lost_and_Found_in_Diffusion_Large_Language_Models.pdf]]
