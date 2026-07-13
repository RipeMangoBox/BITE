---
title: "BEAT: Visual Backdoor Attacks on VLM-based Embodied Agents via Contrastive Trigger Learning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/BEAT_Visual_Backdoor_Attacks_on_VLM_based_Embodied_Agents_via_Contrastive_Trigger_Learning.pdf
project_link: https://zqs1943.github.io/BEAT
code_link: null
openreview_forum_id: OwinX7PI83
aliases:
- BEAT
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/vision_models_multimodal
core_operator: "CTL（对比触发器学习）通过偏好学习显式锐化决策边界，实现精准的触发器响应。"
primary_logic: "将触发器判别建模为偏好学习问题：在相同上下文下对比有无触发器时的行为偏好，可精准切换良性/恶意策略。"
claims:
- "BEAT在VAB-OmniGibson上将攻击成功率(ASR)提升至77.9%，同时误触发率(FTR)降至0% (Qwen2-VL-7B)。"
- "CTL将后门触发F1分数(F1BT)相比无CTL最多提高39%。"
- "CTL使得在仅有10%后门数据(k=0.1)时ASR提升超过5倍。"
- "移除CTL导致EB-ALFRED上InternVL3-8B的FTR高达81.3%，而完整BEAT将其降至0%。"
---

# BEAT: Visual Backdoor Attacks on VLM-based Embodied Agents via Contrastive Trigger Learning

> [!tip] 核心洞察
> 将触发器判别建模为偏好学习问题：在相同上下文下对比有无触发器时的行为偏好，可精准切换良性/恶意策略。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | BEAT：基于对比触发器学习的VLM具身代理视觉后门攻击 |
| 英文题名 | BEAT: Visual Backdoor Attacks on VLM-based Embodied Agents via Contrastive Trigger Learning |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=OwinX7PI83) · [Project](https://zqs1943.github.io/BEAT) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal |
| Method | BEAT |
| Dataset | VAB-OmniGibson |

> [!tip] 效果简介
> - VAB-OmniGibson 上，SR↑ 为 18.0，对比 17.0 (Benign SFT)，变化 +1.0。
> - VAB-OmniGibson 上，ASR↑ 为 77.9，对比 47.6 (BEAT w/o CTL)，变化 +30.3。
> - VAB-OmniGibson 上，FTR↓ 为 0.0，对比 7.0 (BEAT w/o CTL)，变化 -7.0。

## 概要

具身智能体将视觉语言模型（VLM）作为核心决策组件，使其能够根据视觉输入与交互历史生成动作序列。然而，VLM的黑盒特性与对视觉输入的强依赖，为后门攻击打开了新的攻击面。现有针对纯语言模型或静态图像VLM的后门方案，难以应对具身场景中视觉触发器在视角、光照、遮挡下的高变异性——传统监督微调方法在此条件下往往无法可靠激活后门，且频繁产生误触发。

论文提出 **BEAT**，一种面向VLM驱动具身代理的视觉后门攻击框架。其核心瓶颈在于：视觉触发器的高变异性导致决策边界模糊，模型难以精准区分“何时应激活恶意策略”。BEAT的核心洞察是将触发器判别建模为偏好学习问题：在完全相同的交互上下文下，对比有无触发器时的行为偏好，可精准切换良性/恶意策略。

方法上，BEAT引入两阶段训练范式：第一阶段通过监督微调（SFT）使模型获得通用任务能力与基本后门行为；第二阶段通过**对比触发器学习（CTL）**，利用偏好损失显式锐化触发器的决策边界。CTL在相同历史上下文中，要求模型对无触发器输入倾向良性动作，对有触发器输入倾向恶意动作，从而大幅提升触发器响应的精准性。

关键实证结论：

- **攻击成功率（ASR）大幅提升**：在VAB-OmniGibson基准上，BEAT将ASR从BEAT w/o CTL的47.6%提升至77.9%（Qwen2-VL-7B），提升30.3个百分点（Table 1）。
- **误触发率（FTR）降至零**：CTL在EB-ALFRED上将InternVL3-8B的FTR从81.3%降至0%，在VAB-OmniGibson上将FTR从7.0%降至0%，几乎完全消除误触发（Table 1）。
- **低数据效率**：当后门数据比例仅为10%（k=0.1）时，CTL使ASR提升超过5倍（§4.3）。
- **后门触发F1分数（F1BT）提升显著**：CTL将F1BT相比无CTL最多提高39%（§4.2）。

BEAT在方法谱系中定位为**两阶段偏好学习驱动的视觉后门攻击**，区别于单阶段SFT混合训练（BEAT w/o CTL）和纯良性SFT（Benign SFT）。其对比数据集构造与CTL损失函数的设计，为具身场景下的精准后门植入提供了新的范式。



### 具身智能体的视觉后门威胁

基于视觉语言模型（VLM）的具身智能体正被广泛应用于机器人操控、家庭服务等物理交互场景，其决策链路由用户查询、交互历史和当前场景帧共同驱动。然而，VLM的视觉感知通道引入了一类独特的安全威胁：攻击者可通过在环境中植入视觉触发器（如特定物体），在特定时刻动态切换智能体的行为策略，使其从良性任务执行转向恶意操作。

Figure 1 对比了三类后门攻击范式。在基于大语言模型（LLM）的具身智能体中，后门通过注入静态文本触发器（如“灰色箱子”）来操纵决策；在纯VLM后门攻击中，静态视觉触发器（如红色气球）仅诱导单步恶意输出。相比之下，**面向VLM驱动具身智能体的后门攻击**利用环境中的物体作为触发器——这些物体在不同视角和光照下呈现高变异性——在多个时间步上动态激活后门策略，逐步实现攻击者目标。

### 核心瓶颈：触发器变异性与决策边界模糊

视觉触发器在实际部署中面临的核心挑战是**高变异性**：同一触发物体（如花瓶、刀具）在不同场景、视角、光照条件下外观差异显著。传统后门植入方法——将良性数据与后门数据混合进行单阶段监督微调（SFT）——难以可靠地激活后门策略，具体表现为两类失败模式：

1. **激活失败**：模型未能识别出变异的触发器，导致攻击成功率（ASR）低下。
2. **误触发**：模型在良性场景中错误地切换到恶意策略，产生高误触发率（FTR）。

实验证据揭示了这一问题的严重性：在EB-ALFRED基准上，移除CTL的BEAT变体（即仅混合SFT）在InternVL3-8B上的误触发率高达**81.3%**，而完整BEAT将其降至**0%**（Table 1）。这表明，仅靠最终动作标签的间接监督信号，无法让模型习得清晰的触发器判别边界。

### 动机：将触发器判别建模为偏好学习

BEAT的核心洞察在于：**触发器判别本质上是一个偏好学习问题**。在相同的交互历史上下文中，模型应当对无触发器输入偏好良性动作，对有触发器输入偏好恶意动作。通过显式构造这种对比偏好信号，可以锐化模型的决策边界，实现精准的触发器响应。

基于此，BEAT提出两阶段训练框架：先通过混合数据SFT赋予模型通用任务能力和基本后门行为，再通过**对比触发器学习（CTL）**——一种基于偏好损失的训练范式——显式强化模型对触发器存在与否的判别能力。CTL在仅有**10%后门数据**（k=0.1）时可将ASR提升超过**5倍**，并将后门触发F1分数（F1BT）最高提升**39%**，验证了偏好学习范式在解决触发器变异性问题上的有效性。



## 核心方法与创新机理

BEAT的核心创新在于将视觉后门植入重新定义为一个**偏好学习问题**，并据此设计了两阶段训练范式，从根本上解决了传统监督微调（SFT）方法在具身代理后门攻击中的关键瓶颈。

### 瓶颈诊断：SFT难以应对视觉触发器的高变异性

在VLM驱动的具身代理场景中，后门触发依赖于环境中的特定物体（如刀、花瓶）。这些物体在不同视角、光照和局部遮挡条件下呈现**高视觉变异性**。传统的SFT方法将良性数据和后门数据混合进行单阶段训练，模型仅通过最终动作标签间接学习触发器的判别能力。这导致两个严重问题：

1. **误触发率高**：模型在无触发器的良性场景中也可能错误激活后门策略。实验显示，移除CTL后，BEAT w/o CTL在EB-ALFRED上InternVL3-8B的误触发率（FTR）高达81.3%（Table 1）。
2. **攻击成功率受限**：在低后门数据比例下，模型难以建立可靠的触发器-恶意行为关联。当后门数据比例k=0.1时，BEAT w/o CTL的攻击成功率极低。

### 核心机制：对比触发器学习（CTL）

BEAT的CTL模块将触发器判别建模为**偏好学习问题**，通过对比信号显式锐化决策边界。其核心设计包含三个changed slots：

**1. 训练范式：从单阶段SFT到两阶段SFT+CTL**

BEAT采用两阶段训练（Figure 2）：
- **阶段一（SFT）**：在混合数据集上进行监督微调，使模型同时获得通用任务能力和基本后门行为。
- **阶段二（CTL）**：在SFT基础上，通过偏好损失进一步锐化触发器决策边界，实现精准的行为切换。

消融实验表明，两阶段互补性显著：仅CTL（无SFT）时ASR最高仅67.6%，且良性成功率（SR）骤降至3.0（Table 3）；仅SFT（无CTL）则导致高误触发和低ASR。

**2. 触发器判别监督信号：从间接动作标签到显式偏好对比**

SFT仅通过最终动作标签间接监督触发器判别，信号稀疏且模糊。CTL则引入**偏好对比信号**：在相同交互历史下，模型被明确训练为：
- 无触发器时，倾向良性动作 $a_{\text{benign}}$
- 有触发器时，倾向恶意动作 $a_{\text{attack}}$

这种显式对比监督使得模型能够精准学习触发器的视觉特征与策略切换的因果关系，而非仅记忆表面统计关联。

**3. 数据处理：从单实例到图像对比对**

为支持偏好学习，BEAT构造了**图像对比数据集**：针对同一交互历史，生成成对示例——一个包含触发器（$v^+$），一个不包含（$v^-$），分别对应恶意动作和良性动作。这种配对设计使得CTL的偏好损失能够直接对比模型在有无触发器条件下的行为差异，从而锐化决策边界。

### 效果验证

CTL带来的改进在多个维度上得到验证：
- **攻击成功率提升**：在VAB-OmniGibson上，Qwen2-VL-7B的ASR从47.6%（BEAT w/o CTL）提升至77.9%（Table 1）。
- **误触发消除**：CTL将EB-ALFRED上InternVL3-8B的FTR从81.3%降至0%（Table 1）。
- **低数据效率**：当k=0.1时，CTL将ASR提升超过5倍（§4.3），显示出在有限后门数据下的强鲁棒性。
- **后门触发F1分数**：CTL将F1BT相比无CTL最高提升39%（§4.2），表明触发器判别精度显著提高。



![[assets/figures/papers/paper_list_l16_https_openreview_net_forum_id_OwinX7PI83/figures/002_Figure_2.jpg]]
*Figure 2: Two-stage backdoor fine-tuning scheme in BEAT. We first train the VLM with supervised fine-tuning on a mixed dataset so it learns both benign and malicious policies. We then apply contrastive trigger learning, using a preference-paired dataset to strengthen its ability to distinguish and switch between behaviors: given the same interaction history h, the model prefers the benign action $a _ { \mathrm { b e n i g n } }$ on trigger-free inputs (v−) and the backdoor action $a _ { \mathrm { a t t a c k } }$ on triggered inputs ( $v _ { + }$ )

BEAT 是一个针对 VLM 驱动具身代理的视觉后门攻击框架，其核心目标是在保持良性任务性能的同时，实现对视觉触发器的精准响应。整个 pipeline 由**数据构建**与**两阶段训练**两大环节串联而成，形成“数据采集→监督微调→对比触发器学习”的完整流程。

### 数据构建层

BEAT 首先构建三类数据集，为后续训练提供差异化监督信号：

1. **良性数据集** $\mathcal{D}_{\text{benign}}$：在无触发器环境中，由基础 VLM 策略 $\pi_{\text{VLM}}$ 执行任务，收集成功轨迹。每条轨迹记录用户查询 $q$、交互历史 $h_t$、当前场景帧 $v_t$ 及采样的动作 $a_t$，为模型提供标准任务能力的基础。
2. **后门数据集** $\mathcal{D}_{\text{attack}}$：在环境中放置触发器物体后，轨迹前半段仍由 VLM 策略执行良性动作；当触发器首次出现在视野中（触发步 $\hat{t}$），控制权切换至基于规则的恶意策略 $\pi_{\text{rule}}$，执行多步恶意计划。仅保留触发步之后的轨迹片段，并分解为逐步训练实例 $\{(q^i, h_t^i, v_t^i, a_t^i)\}_{t=\hat{t}_i}^{T_i}$。
3. **对比数据集** $\mathcal{D}_{\text{contrast}}$：针对每个触发步 $\hat{t}_i$，构造一对共享相同交互历史 $h_{\hat{t}_i}$ 的示例——一张含触发器的帧 $v_{\hat{t}_i(+)}$ 对应恶意动作 $a_{\text{attack}}$，一张移除触发器的帧 $v_{\hat{t}_i(-)}$ 对应由 VLM 策略重新采样的良性动作 $a_{\text{benign}}$。这种“仅触发器有无不同”的成对设计，是 CTL 偏好学习的基础。

### 两阶段训练层

BEAT 的训练分为监督微调（SFT）和对比触发器学习（CTL）两个阶段，分别解决“能力获取”与“边界锐化”两个子问题。

**阶段一：监督微调（SFT）**
将 $\mathcal{D}_{\text{benign}} \cup \mathcal{D}_{\text{attack}}$ 混合，通过最大化真实动作的对数似然训练 VLM：

$$\max_{\theta} \sum_{(q^i, h^i, v^i, a^i) \in \mathcal{D}_{\text{SFT}}} \log \pi_{\theta}(a^i \mid q^i, h^i, v^i)$$

此阶段采用良性样本与后门样本交替训练的策略，防止任一模态主导优化过程，使模型同时获得通用任务执行能力和基本的后门行为模式。

**阶段二：对比触发器学习（CTL）**
将触发器判别建模为偏好学习问题。给定对比数据集中的成对示例，CTL 的目标是让模型明确偏好：在无触发器输入 $v_{(-)}$ 上倾向良性动作 $a_{\text{benign}}$，在有触发器输入 $v_{(+)}$ 上倾向恶意动作 $a_{\text{attack}}$。其损失函数为：

$$\mathcal{L}(a^w, a^l \mid h, v) = -\log \sigma\Big(\beta \log\frac{\pi_{\theta}(a^w \mid h, v)}{\pi_{\text{ref}}(a^w \mid h, v)} - \beta \log\frac{\pi_{\theta}(a^l \mid h, v)}{\pi_{\text{ref}}(a^l \mid h, v)}\Big) - \alpha \frac{\log\pi_{\theta}(a^w \mid h, v)}{|a^w|}$$

其中 $a^w$ 为偏好动作（正确动作），$a^l$ 为非偏好动作，$\pi_{\text{ref}}$ 为 SFT 阶段产出的参考模型。偏好损失项推动模型增大偏好动作与非偏好动作的相对概率比，NLL 正则项则防止模型遗忘已学能力。此外，通过采样比率 $\gamma$ 从 SFT 数据集中混合部分样本，平衡能力保持与触发器边界锐化。

### 输入输出流

整个框架的推理流程为：给定用户查询 $q$，代理在每个时间步根据交互历史 $h_t$ 和当前场景帧 $v_t$ 采样动作 $a_t \sim \pi_{\theta}(\cdot \mid q, h_t, v_t)$。正常状态下，模型执行良性策略；一旦场景中出现触发器物体，CTL 阶段锐化的决策边界使模型可靠切换至恶意策略，执行攻击者预设的多步恶意计划。

**关键设计瓶颈**：传统单阶段 SFT 将触发器判别信号淹没在动作标签的间接监督中，导致高误触发率（FTR）和低攻击成功率（ASR）。BEAT 通过引入显式的对比偏好信号，将“是否触发”这一隐式决策显式化为偏好学习目标，从根本上解决了视觉触发器在高变异性场景下的可靠激活问题。



BEAT 的核心由两个训练阶段构成：监督微调（SFT）与对比触发器学习（CTL）。SFT 阶段赋予模型基本的任务执行能力和初步的后门行为；CTL 阶段则将触发器判别建模为偏好学习问题，通过对比信号锐化决策边界，从而实现精准的良性/恶意策略切换。

### 策略采样与后门切换

具身代理的策略可形式化为在给定用户查询 $q$、交互历史 $h_t$ 及当前场景帧 $v_t$ 时采样动作：

$$a_t \sim \pi_{\theta}( \cdot \mid q, h_t, v_t )$$

后门攻击的目标是使代理在遇到视觉触发器后切换至恶意策略。设触发器首次出现的步数为 $\hat{t}$，后门策略 $\tilde{\pi}_{\boldsymbol{\theta}}$ 定义为分段函数：

$$a_t \sim \tilde{\pi}_{\boldsymbol{\theta}}( \cdot \mid q, h_t, v_t) = \begin{cases} \pi_{\boldsymbol{\theta}}^{\mathrm{benign}}( \cdot \mid q, h_t, v_t), & t < \hat{t}, \\ \pi_{\boldsymbol{\theta}}^{\mathrm{attack}}( \cdot \mid q, h_t, v_t), & t \geq \hat{t}, \end{cases}$$

该公式是 BEAT 攻击目标的核心表达：在触发器步之前，代理执行良性策略；从触发器步开始，切换至攻击策略执行恶意多步计划。

### 第一阶段：监督微调（SFT）

SFT 阶段在混合数据集 $\mathcal{D}_{\mathrm{SFT}}$（包含良性轨迹与后门轨迹）上最大化真实动作的对数似然：

$$\max_{\theta} \sum_{(q^i, h^i, v^i, a^i) \in \mathcal{D}_{\mathrm{SFT}}} \log \pi_{\theta}(a^i \mid q^i, h^i, v^i)$$

训练时交替采样良性与后门样本，防止任一模式主导训练，从而在保持良性任务能力的同时植入基本后门行为。

### 第二阶段：对比触发器学习（CTL）

CTL 的核心创新在于将触发器判别显式建模为偏好学习问题。对于同一交互历史 $h$，模型应在无触发器输入 $v^-$ 时偏好良性动作 $a^{\mathrm{benign}}$，在有触发器输入 $v^+$ 时偏好攻击动作 $a^{\mathrm{attack}}$。CTL 的损失函数结合偏好损失与负对数似然（NLL）正则项：

$$\mathcal{L}(a^w, a^l \mid h, v) = -\log \sigma\Big(\beta \log\frac{\pi_{\theta}(a^w \mid h, v)}{\pi_{\mathrm{ref}}(a^w \mid h, v)} - \beta \log\frac{\pi_{\theta}(a^l \mid h, v)}{\pi_{\mathrm{ref}}(a^l \mid h, v)}\Big) - \alpha \frac{\log\pi_{\theta}(a^w \mid h, v)}{|a^w|}$$

其中：
- $a^w$ 为偏好动作（winning action），即当前输入对应的正确动作（有触发器时为攻击动作，无触发器时为良性动作）；
- $a^l$ 为拒绝动作（losing action），即另一个动作；
- $\pi_{\mathrm{ref}}$ 为第一阶段 SFT 后的参考模型，用于约束策略更新幅度；
- $\beta$ 控制偏好损失的强度，$\alpha$ 控制 NLL 正则项的权重；
- $\sigma(\cdot)$ 为 sigmoid 函数。

该损失函数的因果机制在于：偏好项 $\log\frac{\pi_{\theta}(a^w)}{\pi_{\mathrm{ref}}(a^w)} - \log\frac{\pi_{\theta}(a^l)}{\pi_{\mathrm{ref}}(a^l)}$ 迫使模型增大偏好动作与拒绝动作之间的概率差距，从而锐化触发器决策边界；NLL 正则项 $\log\pi_{\theta}(a^w)$ 则防止模型在偏好对齐过程中丧失生成能力。消融实验证实，移除 CTL 后，InternVL3-8B 在 EB-ALFRED 上的误触发率（FTR）高达 81.3%，而完整 BEAT 将其降至 0%（Table 1），验证了该损失函数对消除误触发的关键作用。



## 实验与关键发现

### 核心瓶颈与因果机制

BEAT 要解决的根本瓶颈在于：视觉触发器在具身环境中呈现高变异性——同一物体在不同视角、光照、遮挡条件下外观差异显著，传统监督微调（SFT）仅通过最终动作标签提供间接监督信号，难以建立稳定、精准的“触发器→恶意策略”映射。这导致两个典型失败模式：**弱激活**（模型对触发器不敏感，后门未被可靠触发）和**误触发**（在无触发器的良性场景中错误激活恶意行为）。

BEAT 的核心因果调节变量是**对比触发器学习（CTL）**。CTL 将触发器判别建模为偏好学习问题：给定完全相同的交互历史 $h$，模型在无触发器图像 $v^-$ 上应偏好良性动作 $a_{\text{benign}}$，在有触发器图像 $v^+$ 上应偏好攻击动作 $a_{\text{attack}}$。通过显式构造这种成对对比信号，CTL 锐化了决策边界，使模型学会精准区分“何时该切换策略”，而非仅靠动作标签隐式推断。

### 主实验结果

Table 1 汇总了四个模型变体在 VAB-OmniGibson 和 EB-ALFRED 两个基准上的表现，涵盖 Qwen2-VL-7B、InternVL3-8B 和 GPT-4o 三款 VLM。


![[assets/figures/papers/paper_list_l16_https_openreview_net_forum_id_OwinX7PI83/figures/003_Table_1.jpg]]
*Table 1: Experiment results of BEAT. We evaluate four model variants: Original refers to off-theshelf pretrained VLM; Benign SFT is a model fine-tuned on $\mathcal { D } _ { \mathrm { b e n i g n } }$ ; BEAT w/o CTL denotes the model fine-tuned on $\mathcal { D } _ { \mathrm { b e n i g n } } \cup \mathcal { D } _ { \mathrm { a t t a c k } }$ ; BEAT adapts two-stage training scheme on $\mathcal { D } _ { \mathrm { b e n i g n } } \cup \mathcal { D } _ { \mathrm { a t t a c k } } \cup \mathcal { D } _ { \mathrm { c o n t r a s t } }$ . Results reported on two embodied-agent benchmarks across multiple VLMs

**VAB-OmniGibson 基准（Qwen2-VL-7B）：**

| 指标 | Benign SFT | BEAT w/o CTL | BEAT | 提升 |
|------|-----------|-------------|------|------|
| SR↑ | 17.0 | 10.0 | **18.0** | +8.0 (vs w/o CTL) |
| ASR↑ | — | 47.6 | **77.9** | +30.3 |
| FTR↓ | — | 7.0 | **0.0** | −7.0 |
| F1BT↑ | — | 0.713 | **0.923** | +0.210 |

BEAT 在保持良性任务成功率（SR=18.0）的同时，将攻击成功率（ASR）推至 77.9%，较无 CTL 版本提升超过 30 个百分点。更关键的是，误触发率（FTR）从 7.0% 降至 0%，后门触发 F1 分数（F1BT）从 0.713 跃升至 0.923，表明 CTL 几乎消除了“该触发时不触发”和“不该触发时误触发”两类错误。

**EB-ALFRED 基准（InternVL3-8B）：**

| 指标 | BEAT w/o CTL | BEAT | 变化 |
|------|-------------|------|------|
| ASR↑ | 69.0 | **80.8** | +11.8 |
| FTR↓ | 81.3 | **0.0** | −81.3 |

EB-ALFRED 上的结果更为极端：无 CTL 时 FTR 高达 81.3%，意味着模型在绝大多数良性任务中都会错误激活后门——这正是单阶段 SFT 缺乏明确触发器判别信号的典型症状。完整 BEAT 将 FTR 压至 0%，同时 ASR 提升至 80.8%，证明 CTL 的偏好学习机制在不同环境和 VLM 上均有效。

**跨模型泛化：** GPT-4o 因微调 API 不支持基于图像的偏好优化，仅能执行 SFT 阶段。其 BEAT w/o CTL 在 VAB-OmniGibson 上 ASR=27.1，FTR=0.0，SR=20.0。ASR 显著低于开源模型上的完整 BEAT，暗示专有模型若支持 CTL 可能获得更高攻击效能，但这一推断需手动验证。

### 消融实验

**CTL 的独立贡献（Table 3）：**

![[assets/figures/papers/paper_list_l16_https_openreview_net_forum_id_OwinX7PI83/figures/010_Table_3.jpg]]
*Table 3: Ablation results of SFT with different backdoor data ratios k on Qwen2-VL-7B-Instruct using the VAB benchmark*

- 移除 CTL（BEAT w/o CTL）导致 Qwen2-VL-7B 在 VAB 上的 SR 从 18.0 骤降至 10.0，ASR 从 77.9 降至 47.6。这表明 SFT 阶段学到的后门行为极不稳定，CTL 是可靠激活的关键。
- 仅使用 CTL 而跳过 SFT（BEAT w/o SFT，k=1.0）时，ASR 最高达 67.6，但 SR 暴跌至 3.0。这揭示了两阶段的互补性：SFT 提供通用任务能力地基，CTL 在其上精准刻画触发器边界。单独任一阶段均无法兼顾任务性能与攻击效能。

**后门数据比例 k 的影响（Figure 4, Table 3）：**

![[assets/figures/papers/paper_list_l16_https_openreview_net_forum_id_OwinX7PI83/figures/008_Figure_4.jpg]]
*Figure 4: Impact of backdoor data ratio in BEAT. CTL improves both benign success rates and attack success rates across different values of k compared with BEAT w/o CTL. Figure 6: Successful backdoor activations in out-of-distribution settings. Examples depict trigger objects placed in unconventional scenes (e.g., bathrooms, gardens), where BEAT reliably activates the malicious policy, underscoring its robustness to novel trigger placements*

- 定义 $k = |\mathcal{D}_{\text{attack}}| / |\mathcal{D}_{\text{benign}}|$。随 k 增大，ASR 单调上升，SR 单调下降，揭示了**任务能力与后门植入之间的固有权衡**。
- CTL 在低数据区间的增益尤为显著：当 k=0.1 时，CTL 将 ASR 提升超过 **5 倍**，证明偏好学习即使在极少量对比样本下也能有效建立触发器-恶意行为的关联。
- 无 SFT 时（BEAT w/o SFT），k=0.5 取得最高 F1BT=0.993，但 SR 仅 8.0——模型几乎完全退化为后门专用，丧失了良性任务执行能力。

**误触发率消融（Figure 5）：**
CTL 在所有设置下将 FTR 压至接近 0%。相比之下，BEAT w/o CTL 在 EB-ALFRED InternVL3-8B 上 FTR 达 81.3%，在 VAB Qwen2-VL-7B 上为 7.0%。这一差异的根源在于：SFT 阶段混合训练使模型对触发器相关视觉特征产生模糊关联，而 CTL 通过显式偏好对比消除了这种模糊性。


![[assets/figures/papers/paper_list_l16_https_openreview_net_forum_id_OwinX7PI83/figures/007_Figure_5.jpg]]
*Figure 5: False triggering rate (FTR). CTL sharply reduces FTRs on benign tasks*

**超参数敏感性（Table 2）：**
对偏好损失权重 $\alpha$ 和 $\beta$ 的扫描显示，BEAT 对超参数不敏感。在 $\alpha \in [0.2, 0.6]$、$\beta \in [0.01, 0.1]$ 范围内，ASR 稳定在 60% 以上，SR 波动幅度有限。默认设置（$\alpha=0.4, \beta=0.05$）取得最优综合性能。


![[assets/figures/papers/paper_list_l16_https_openreview_net_forum_id_OwinX7PI83/figures/009_Table_2.jpg]]
*Table 2: Sensitivity test of α and β on Qwen2-VL-7B-Instruct using the VAB benchmark*

### 分布外泛化与鲁棒性

**OOD 触发器放置（Figure 6）：** 将触发器物体（刀）放置于训练时未见过的场景（如浴室、花园），BEAT 仍取得 **92.3%** 的 ASR。这表明 CTL 学到的不是对特定背景的过拟合，而是对触发器物体本身语义的泛化识别。

**部分可见与多实例场景（Figure 7）：** 当触发器物体仅部分可见，或场景中存在多个不同外观的同类别物体时，BEAT 仍能成功激活后门。这进一步验证了 CTL 偏好学习的鲁棒性——模型学会的是“存在触发器物体”这一抽象条件，而非对特定像素模式的记忆。

### 失败模式与局限性

1. **无边界框条件下的退化风险：** VAB-OmniGibson 依赖物体边界框注释来标识触发器位置，简化了学习难度。EB-ALFRED 的无框实验对此进行了部分补偿，但完全自然的视觉条件下触发器学习的鲁棒性仍需进一步验证。

2. **模拟器到真实世界的鸿沟：** 所有评估均在 OmniGibson 和 AI2-THOR 模拟器中进行，真实环境中的光照、遮挡、物体外观分布偏移可能影响触发可靠性。

3. **专有模型的 CTL 缺失：** GPT-4o 因 API 限制无法执行 CTL，其 ASR 仅为 27.1%，可能低估了完整 BEAT 在更大规模商业模型上的潜在威胁。该推断需待 API 能力更新后手动验证。

4. **触发器类别限制：** 当前后门绑定于特定物体类别（刀、花瓶），攻击者需预先选定目标物体。更灵活的条件触发器（如“任何红色物体”）尚未探索。

5. **初步防御的抵抗能力：** 论文提及的初步防御尝试（提示约束、聚类检测、良性微调）均未能完全消除后门，但系统性的防御研究仍是开放问题。



## 定位与知识库关联

### 与基线方法的对比定位

BEAT 的攻击范式与三类基线形成清晰对比：

- **Original VLM（未微调预训练模型）**：作为下界，原始 VLM 在无触发器环境中具备一定任务成功率，但几乎不具备后门激活能力（ASR 接近 0%），因为模型从未接触过后门行为模式。
- **Benign SFT（仅良性数据微调）**：仅使用良性数据微调的模型保持了较高的良性成功率（SR），但同样无法激活后门，其 F1BT 接近 0。这验证了后门行为必须通过显式的后门数据注入。
- **BEAT w/o CTL（单阶段混合 SFT）**：这是与 BEAT 最直接的对比基线。该变体将良性数据与后门数据混合进行单阶段监督微调，模型确实获得了一定的后门激活能力，但存在两个致命瓶颈：① 攻击成功率（ASR）显著低于 BEAT（VAB-OmniGibson 上 Qwen2-VL-7B 的 ASR 仅 47.6%，而 BEAT 达 77.9%）；② 误触发率（FTR）极高，尤其在 EB-ALFRED 上 InternVL3-8B 的 FTR 高达 81.3%，而 BEAT 将其降至 0%。这一对比直接揭示了核心瓶颈：**单阶段 SFT 无法在视觉触发器的高变异性下学习到可靠的决策边界**。

### 方法谱系中的知识贡献

BEAT 的核心知识贡献在于**将具身代理的后门攻击从“隐式动作监督”推进到“显式偏好学习”**，具体体现在以下因果链条上：

1. **瓶颈识别**：视觉触发器在不同视角、光照和部分遮挡条件下呈现高变异性，传统监督微调仅通过最终动作标签间接监督触发器判别，导致模型无法可靠地区分“有触发器”与“无触发器”状态。这解释了 BEAT w/o CTL 的高 ASR 与高 FTR 并存的现象——模型对触发器既“迟钝”（漏触发）又“过敏”（误触发）。

2. **因果调节变量**：CTL（对比触发器学习）通过偏好学习显式锐化决策边界。其关键设计是在**相同交互历史**下构造图像对比对（有/无触发器），并利用偏好损失直接优化模型对“良性动作 vs. 恶意动作”的相对倾向。这使得模型不再依赖间接的动作标签，而是直接学习“触发器存在性”这一判别信号。

3. **核心洞察**：将触发器判别建模为偏好学习问题。在相同上下文下对比有无触发器时的行为偏好，可精准切换良性/恶意策略。这一洞察的证据强度极高：CTL 将后门触发 F1 分数（F1BT）相比无 CTL 最多提高 39%；在仅有 10% 后门数据（k=0.1）时，CTL 将 ASR 提升超过 5 倍。

### 两阶段训练的必要性

BEAT 的两阶段设计（SFT → CTL）并非简单的流程堆叠，而是解决了一个根本性的能力权衡：

- **仅 SFT**：ASR 低、FTR 高，决策边界模糊。
- **仅 CTL（无 SFT）**：在 k=1.0 时 ASR 最高仅 67.6%，且 SR 骤降至 3.0。这表明 CTL 虽然锐化了触发器判别，但缺乏 SFT 阶段提供的通用任务能力基础。
- **SFT + CTL**：SR 保持在 18.0（与 Benign SFT 的 17.0 相当），ASR 达 77.9，FTR 为 0。两阶段互补：SFT 建立任务能力与基本后门行为，CTL 在此基础上精确校准触发器响应边界。

### 适用边界与局限

1. **模型边界**：CTL 仅在开源 VLM（Qwen2-VL-7B、InternVL3-8B）上完整评估。GPT-4o 因微调 API 不支持基于图像的 DPO，仅执行了 SFT 阶段，其 ASR 较低，可能低估了完整 BEAT 在专有模型上的潜力。这一局限需在 API 能力更新后重新验证。

2. **环境边界**：所有实验均在模拟器（OmniGibson、AI2-THOR）中进行，尚未扩展至真实物理环境。模拟中的视觉条件（光照、遮挡、视角）虽已覆盖一定变异性，但真实世界的噪声、动态遮挡和传感器误差可能进一步挑战触发器的鲁棒性。

3. **触发器假设**：VAB-OmniGibson 依赖物体边界框注释来标识触发器对象，这简化了触发器检测的评估。EB-ALFRED 的无框实验对此进行了部分补偿，但两者仍假设触发器为特定物体类别（刀、花瓶）。更自然的无框条件下触发器学习仍需进一步研究。

4. **数据权衡**：增加后门数据比例 k 可提高 ASR，但同时降低 SR，揭示了任务能力与后门植入的固有权衡。这一权衡在资源受限的攻击场景下尤为重要。

### 开放问题

1. **无边界框注释的触发器学习**：当前方法依赖或受益于物体边界框注释，如何在全自然视觉条件下学习鲁棒的触发器判别仍是一个开放挑战。

2. **真实物理环境部署**：BEAT 在模拟器中展现出高 ASR 和低 FTR，但真实世界的域迁移（domain shift）可能导致性能退化，实际部署的有效性和鲁棒性待验证。

3. **复杂触发器形式**：CTL 是否能泛化到更复杂的触发器形式（如动态触发器、组合物体、时序触发器模式）尚未探索。

4. **有效防御机制**：论文初步尝试了提示约束、激活聚类和良性微调等防御手段，但均未完全奏效。针对基于偏好学习的后门攻击，设计有效防御仍是一个紧迫的开放问题。

5. **更大规模模型的扩展性**：当前实验限于 7B-8B 参数规模，在更大规模的 VLM 和多模态模型上，BEAT 是否仍能保持高攻击成功率与低误触发，以及 CTL 的偏好学习范式是否需要调整，尚待研究。



## 原文 PDF

![[paperPDFs/ICLR_2026/BEAT_Visual_Backdoor_Attacks_on_VLM_based_Embodied_Agents_via_Contrastive_Trigger_Learning.pdf]]
