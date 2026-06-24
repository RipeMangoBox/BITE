---
title: "MotionEnhancer: Leveraging Video Diffusion for Motion-Enhanced Vision-Language Models"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/MotionEnhancer_Leveraging_Video_Diffusion_for_Motion_Enhanced_Vision_Language_Models.pdf
project_link: "https://motion-enhancer.github.io/"
code_link: null
aliases:
- MotionEnhancer
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 通过将 VLM 的文本-视觉注意力与从视频扩散模型（VDM）蒸馏的运动先验（即证据寻求分布 p(V|t)）进行对齐，为 VLM 注入时间动态敏感性。
primary_logic: 视频扩散模型在去噪生成过程中自然编码了运动校准的跨模态注意力，可作为免费的运动监督信号；只需在参数无关的注意力头筛选（MHS）和文本标记筛选（MTTI）后，通过简单的 MSE 注意力对齐，即可显著提升 VLM 的运动理解能力，无需额外训练参数或架构修改。
claims:
- VDM 的交叉注意力图近似证据寻求分布 p(V|t)，并自然地随运动幅度变化而调整，从而为运动理解提供可靠的先验。
- MotionEnhancer 在 MotionBench 和 FAVOR-Bench 两个运动理解基准上一致地提升了多种 VLM（Qwen2.5-VL 3B/7B、InternVL3-8B）的性能，尤其在运动相关指标上。
- MHS 和 MTTI 模块互补，联合使用带来最大增益，且无需任何额外训练参数或架构修改。
- 理论分析揭示了 VLM 的 p(t|V) 分布与运动理解所需的 p(V|t) 分布之间的分布不匹配，从而为注意力对齐提供了依据。
---

# MotionEnhancer: Leveraging Video Diffusion for Motion-Enhanced Vision-Language Models

> [!tip] 核心洞察
> 视频扩散模型在去噪生成过程中自然编码了运动校准的跨模态注意力，可作为免费的运动监督信号；只需在参数无关的注意力头筛选（MHS）和文本标记筛选（MTTI）后，通过简单的 MSE 注意力对齐，即可显著提升 VLM 的运动理解能力，无需额外训练参数或架构修改。

| 字段 | 内容 |
|------|------|
| 中文题名 | MotionEnhancer：利用视频扩散模型增强视觉语言模型的运动理解能力 |
| 英文题名 | MotionEnhancer: Leveraging Video Diffusion for Motion-Enhanced Vision-Language Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Xu_MotionEnhancer_Leveraging_Video_Diffusion_for_Motion-Enhanced_Vision-Language_Models_CVPR_2026_paper.html) · [Project](https://motion-enhancer.github.io/) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | MotionEnhancer |
| Dataset | MotionBench |

> [!tip] 效果简介
> - MotionBench 上，Overall Accuracy 56.60 vs 53.56（由 delta 推断） (+3.04)；Overall Accuracy 57.04 vs 52.81（由 delta 推断） (+4.23)；Overall Accuracy 57.69 vs 54.88（由 delta 推断） (+2.81)。

## 概述

**问题瓶颈**：现有视觉语言模型（VLM）在视频理解中学习的是判别式分布 $p(t|V)$——模型可以依赖静态外观线索（如物体形状、颜色）来回答“动作是什么”，而无需真正理解帧间的细粒度时间动态。这导致 VLM 对运动细节的理解严重不足。

**核心洞察**：视频扩散模型（VDM）在去噪生成过程中，其交叉注意力图天然近似于证据寻求分布 $p(V|t)$，即“给定文本概念，视觉证据在时空中的位置”。这种注意力随实际运动幅度自适应调整，因此可以作为免费的运动监督信号，无需额外标注。

**方法定位**：**MotionEnhancer**（CVPR 2026）提出了一种参数无关的注意力对齐框架，将 VDM 的运动先验蒸馏为 VLM 微调的辅助监督。其核心由两个互补模块构成：**运动敏感头筛选（MHS）** 和 **运动显著文本标记识别（MTTI）**，分别从注意力头和文本标记两个维度过滤运动无关信息。随后通过简单的 MSE 注意力对齐损失，将精炼后的 VDM 注意力与 VLM 的文本-视觉注意力对齐。该方法不修改 VLM 架构，不引入额外训练参数，可适配不同的 VLM 和 DiT 类 VDM。

**主要结果**：MotionEnhancer 在 MotionBench 和 FAVOR-Bench 两个运动理解基准上一致提升多种 VLM 的性能——Qwen2.5-VL 3B 提升 +3.04，7B 提升 +4.23，InternVL3-8B 提升 +2.81。消融实验证实 MHS 与 MTTI 互补，联合使用带来最大增益。

## 背景与动机

### 视觉语言模型的运动理解困境

视觉语言模型（VLM）近年来在视频理解任务上取得了显著进展，能够处理复杂的时空推理问题。然而，现有 VLM 在细粒度运动理解（motion understanding）方面仍存在根本性不足——模型往往能够正确回答“发生了什么”，却难以精确捕捉“如何发生的”这一层面的时间动态细节。

这一困境的根源在于 VLM 的学习机制。VLM 的自回归训练目标为：

$$\mathcal{L}_{\mathrm{AR}} = -\sum_i \log p_\theta(\boldsymbol{r}_i \mid \mathbf{V}, \boldsymbol{r}_{<i})$$

该目标本质上建模的是判别式分布 $p(t \mid V)$，即给定视觉输入 $V$ 预测文本标记 $t$。问题在于，这种分布允许模型通过静态外观线索（如物体类别、场景布局）来满足预测目标，而不必真正关注帧间的细粒度时间动态。例如，模型可能仅凭“球门前的球员”这一静态场景信息就推断“进球”，而无需感知射门动作的完整运动轨迹。

### 分布不匹配的理论根源

MotionEnhancer 通过理论分析揭示了这一问题的深层原因。运动理解任务实际上需要推断潜在运动证据 $\mathbf{E}$ 的分布：

$$p^\star(a \mid \mathbf{V}, q) = \sum_{\mathbf{E}} p^\star(a \mid \mathbf{E}, q) p^\star(\mathbf{E} \mid \mathbf{V}, q)$$

其中运动证据 $\mathbf{E}$ 与帧间特征差异直接相关：

$$\mathbf{E}[\mathrm{Motion}(s,f)] \propto \| V_{f+1}(s) - V_f(s) \|$$

这意味着真正的运动理解需要模型具备证据寻求（evidence-seeking）能力，即建模 $p(V \mid t)$ 分布——给定文本描述，定位与之对应的视觉运动证据。然而，VLM 的文本-视觉注意力近似的是判别式分布：

$$A^{VLM}(t,s,f) \approx p_\theta(t \mid V_f(s), s_{<i})$$

这种 $p(t \mid V)$ 与 $p(V \mid t)$ 之间的分布不匹配，构成了 VLM 运动理解能力不足的核心瓶颈。

### 视频扩散模型的运动先验

与 VLM 形成鲜明对比的是，视频扩散模型（VDM）在去噪生成过程中自然编码了高质量的运动先验。VDM 的交叉注意力图近似证据寻求分布：

$$A^{VDM}(t,s,f) \approx p_\phi(v_{s,f} \mid t, \mathbf{z}_k)$$

这种注意力天然随运动幅度变化而调整——运动越显著的时空位置，对应的注意力权重越高。更重要的是，VDM 的注意力在不同 Transformer 头和文本标记之间呈现出差异化模式：部分注意力头对运动敏感（形成对角线聚焦模式），而部分文本标记（如动作动词、运动描述词）的注意力随时间帧剧烈波动。

这一观察揭示了一个关键洞见：**视频扩散模型可以作为免费的运动监督信号源**，其内在的跨模态注意力无需额外标注即可为 VLM 提供运动先验指导。

### 现有方法的局限与本工作的动机

现有运动增强方法存在明显不足。**Motion-Sight**（Du et al., arXiv 2025）等先前工作试图通过修改模型架构来注入时间信息，但这类方法通常需要引入额外参数或复杂的训练流程。**TE Fusion**（Hong et al., CVPR 2025）等时间建模方法则侧重于特征层面的融合，未能直接解决 $p(t \mid V)$ 与 $p(V \mid t)$ 之间的根本分布不匹配问题。

标准微调（SFT）方法虽然能提升 VLM 的视频理解能力，但由于其仅依赖自回归损失 $\mathcal{L}_{\mathrm{AR}}$，模型仍倾向于学习依赖静态外观线索的捷径，对运动细节的感知提升有限。

基于上述分析，MotionEnhancer 的核心动机是：**在不修改 VLM 架构、不引入额外训练参数的前提下，通过将 VLM 的文本-视觉注意力与 VDM 的运动先验进行对齐，从根本上弥合判别式分布与证据寻求分布之间的鸿沟，从而显著提升 VLM 的运动理解能力。**

## 核心创新

### 问题瓶颈：VLM 的判别式分布忽略了运动细节

现有视觉语言模型（VLM）通过自回归损失 $\mathcal{L}_{\mathrm{AR}} = -\sum_i \log p_\theta(\boldsymbol{r}_i \mid \mathbf{V}, \boldsymbol{r}_{<i})$ 进行训练，其文本-视觉注意力本质上近似于判别式分布 $p_\theta(t \mid V_f(s), s_{<i})$。这一分布的关键缺陷在于：模型可以仅依赖静态外观线索（如物体类别、场景布局）来满足预测目标，而无需真正捕捉帧间的细粒度时间动态。从因果角度来看，VLM 学习的是“给定视觉输入，文本标记是什么”，而非“给定文本概念，视觉证据在时空上如何分布”——后者才是运动理解所需要的证据寻求分布 $p^\star(\mathbf{E} \mid \mathbf{V}, q)$，其中运动证据 $\mathbf{E}[\mathrm{Motion}(s,f)] \propto \| V_{f+1}(s) - V_f(s) \|$ 由帧间特征差异定义。这种分布不匹配构成了当前 VLM 运动理解不足的根本瓶颈。

### 核心洞察：视频扩散模型的注意力是免费的运动先验

MotionEnhancer 的核心洞察在于：视频扩散模型（VDM）在去噪生成过程中自然编码了运动校准的跨模态注意力。具体而言，VDM 的交叉注意力图近似于证据寻求分布 $A^{VDM}(t,s,f) \approx p_\phi(v_{s,f} \mid t, \mathbf{z}_k)$，即“给定文本概念 $t$，视觉特征 $v_{s,f}$ 在时空位置 $(s,f)$ 出现的概率”。由于帧间变化大的区域更难重建，VDM 的注意力会自然地随运动幅度变化而调整——运动越剧烈的区域，模型分配的建模关注越多。这意味着 VDM 的注意力图本身就是一种无需额外标注的运动监督信号，可以直接用于引导 VLM 学习更准确的时间动态表征。

### Changed Slots：从判别式学习到运动感知对齐

MotionEnhancer 的核心创新体现在四个关键设计槽位（changed slots）上，每个槽位都直接针对前述瓶颈进行干预：

**1. 注意力监督信号：从仅自回归损失到 VDM 注意力对齐**

基线 VLM 仅使用自回归损失进行训练，缺乏对运动理解的显式约束。MotionEnhancer 引入了一个额外的注意力对齐损失 $\mathcal{L}_{\mathrm{MSE}} = \|\mathrm{Aligner}(A_{\mathrm{VLM}}) - A_{\mathrm{VDM}}\|_2$，将 VLM 的文本-视觉注意力与从 VDM 蒸馏的运动先验进行对齐。总损失变为 $\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{AR}} + \lambda \mathcal{L}_{\mathrm{MSE}}$，其中 $\lambda$ 为平衡系数。这一设计使得 VLM 在学习语言建模目标的同时，被迫关注与运动相关的视觉区域。

**2. 运动敏感注意力头筛选（MHS）：从平均池化所有头到筛选前 50% 运动相关头**

VDM 的不同 Transformer 注意力头对运动的敏感度差异显著。MotionEnhancer 设计了三个无参数指标来量化每个头的运动相关性：
- **对角线集中度（DFC）**：$\mathrm{DFC} = \frac{\sum_{(i,j) \in \mathcal{M}} A_{\mathrm{v2v}}^2[i,j]}{\sum_{(i,j) \notin \mathcal{M}} A_{\mathrm{v2v}}^2[i,j]}$，衡量注意力在对角线区域（即同一空间位置跨帧的自注意力）的聚焦程度，运动相关头通常呈现更强的对角线模式。
- **时间连续性得分（TCS）**：衡量跨帧空间一致性注意力的持续性，运动感知头倾向于在连续帧中保持对同一运动物体的追踪。
- **对角线显著性比率（DSR）**：统计对角线区域高注意力值的普遍性，反映运动建模的稳定性。

基于这三个指标的综合排序，MHS 模块仅保留前 50% 的运动敏感头用于后续对齐，有效滤除了与运动无关的注意力噪声。

**3. 运动显著文本标记识别（MTTI）：从所有标记参与到筛选前 50% 运动相关标记**

并非所有文本标记都与运动理解相关。MTTI 模块为每个文本标记 $t$ 计算运动评分 $\mathbf{MS}(t) = \operatorname{Mean}_f(A_{\mathrm{t2f}}^t) + \frac{1}{F-1} \sum_{f=1}^{F-1} |A_{\mathrm{t2f}}^t(f+1) - A_{\mathrm{t2f}}^t(f)|$，该评分结合了平均注意力强度（反映该标记在视频中的整体相关性）和帧间注意力波动（反映该标记对时间变化的敏感性）。运动显著标记（如动作动词、方向描述词）通常具有更高的运动评分，而静态描述词（如物体颜色、形状）则评分较低。MTTI 仅保留前 50% 的运动显著标记参与注意力对齐。

**4. 训练目标：从单一自回归损失到联合优化**

上述三个槽位共同构成了一个端到端的联合优化框架：VLM 在标准自回归微调的基础上，同时最小化其筛选后的注意力图与 VDM 运动先验之间的 MSE 损失。值得注意的是，MHS 和 MTTI 均为参数无关模块，不引入任何额外可训练参数，也不修改 VLM 的架构。消融实验证实了两者的互补性：在 Qwen2.5VL-7B 上，仅使用 MHS 在 MotionBench 上提升 +1.77，仅使用 MTTI 同样带来一致增益，而联合使用两者达到最佳性能（MotionBench Overall 57.04，FAVOR-Bench Overall 46.88）。

### 与先前方法的本质区别

相比于 **Motion-Sight**（Du et al., arXiv 2025）等先前运动增强方法，MotionEnhancer 的关键差异在于：它不依赖额外的运动标注数据或专门的运动编码器，而是从已有的视频扩散模型中“免费”蒸馏运动先验。相比于 **TE Fusion**（Hong et al., CVPR 2025）等时间建模方法，MotionEnhancer 不修改 VLM 的时序融合机制，而是通过注意力对齐在表征层面注入运动敏感性。这种“即插即用”的设计使其具有极强的通用性——可适配不同的 VLM（Qwen2.5-VL 3B/7B、InternVL3-8B）和 DiT 类 VDM，无需任何架构修改。

## 整体框架

MotionEnhancer 的整体 pipeline 围绕一个核心思想展开：将视频扩散模型（VDM）中自然编码的运动先验，通过注意力对齐的方式注入到视觉语言模型（VLM）的监督微调过程中，从而增强 VLM 对细粒度时间动态的理解能力。整个框架由四个主要阶段构成，形成一条从运动先验提取到注意力对齐的完整数据流。

**输入与输出。** 框架的输入包括一个视频 $\mathbf{V}$（由 $F$ 帧组成）和对应的文本描述 $t$。输出是经过微调的 VLM，其文本-视觉交叉注意力分布被显式地向 VDM 的证据寻求分布 $p(\mathbf{V}|t)$ 对齐，从而获得更强的运动敏感性。

**阶段一：VDM 注意力提取。** 首先将视频通过 DDIM 逆采样映射到噪声潜空间，再经过 5 步 DDIM 去噪采样，从冻结的 VDM（CogVideoX）中提取多模态交叉注意力图 $A_{\mathrm{mm}}$。该注意力图近似证据寻求分布 $p_\phi(v_{s,f} \mid t, \mathbf{z}_k)$，即给定文本概念 $t$ 时视觉特征在时空位置 $(s,f)$ 上的生成概率。由于 VDM 在去噪过程中必须重建帧间变化较大的区域，其注意力自然随运动幅度校准——运动越显著的位置获得的建模关注越高，这为后续对齐提供了无需人工标注的运动监督信号。

**阶段二：运动敏感注意力头筛选（MHS）。** 并非 VDM 中所有注意力头都与运动相关。MHS 模块利用三个指标筛选运动敏感头：对角线集中度（DFC）衡量注意力在对角线区域的聚焦程度，时间连续性得分（TCS）评估跨帧空间一致性注意力的持续性，对角线显著性比率（DSR）统计高注意力值在对角线区域的普遍性。综合这三个指标，MHS 选择排名前 50% 的头作为运动相关头，过滤掉关注静态背景或噪声的头。

**阶段三：运动显著文本标记识别（MTTI）。** 在聚合运动敏感头之后，MTTI 模块从文本-帧注意力中计算每个文本标记的运动评分 $\mathbf{MS}(t)$，该评分由帧间平均注意力和一阶差分的绝对值之和组成，同时捕捉标记的整体相关性和时间波动性。排名前 50% 的标记被保留用于对齐，从而过滤掉与运动无关的语义标记（如静态属性描述）。

**阶段四：注意力对齐与联合微调。** 经过 MHS 和 MTTI 筛选后的 VDM 注意力图作为目标，与 VLM 的文本-视觉注意力通过 Aligner 模块进行维度匹配后，计算 MSE 损失 $\mathcal{L}_{\mathrm{MSE}}$。该损失与 VLM 原有的自回归损失 $\mathcal{L}_{\mathrm{AR}}$ 加权组合形成总损失 $\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{AR}} + \lambda \mathcal{L}_{\mathrm{MSE}}$，指导 VLM 的视觉编码器、融合层和大语言模型主干的参数更新。

**模块间的互补关系。** MHS 和 MTTI 分别从“哪些注意力头关注运动”和“哪些文本标记描述运动”两个正交维度进行筛选，二者互补。消融实验表明，单独使用 MHS 或 MTTI 均能带来一致的性能提升，而联合使用达到最佳效果，验证了双维度过滤的必要性。

**关键设计特性。** 整个 pipeline 中，VDM 保持完全冻结，MHS 和 MTTI 均为无参数模块，不引入任何额外可训练参数或架构修改。这使得 MotionEnhancer 可以适配不同的 VLM（如 Qwen2.5-VL 3B/7B、InternVL3-8B）和 DiT 类 VDM，具有良好的通用性和即插即用特性。

### 补充图表

![[assets/figures/papers/paper_list_l2328_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_MotionEnhancer_Leve/figures/001_Figure_1.jpg]]
*Figure 1: (A) High-level overview of MotionEnhancer, which incorporates motion priors from the VDM as guidance during supervised fine-tuning of the VLM for improved motion understanding. (B) Observation of VDM attention. We observe distinct patterns in the attention maps across different transformer heads and text tokens in the VDM, which motivates our refinement of motion-centric attention*

![[assets/figures/papers/paper_list_l2328_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_MotionEnhancer_Leve/figures/002_Figure_2.jpg]]
*Figure 2: Framework of MotionEnhancer. Our method leverages motion priors distilled from a powerful VDM as auxiliary supervision to enhance the motion understanding capability of a VLM through attention alignment. Attention maps extracted from the VDM during DDIM sampling are filtered by the Motion-sensitive Head Selection (MHS) and Motion-salient Text Token Identification (MTTI) modules to identify motion-relevant attentions. The resulting text-to-vision attentions are then used to guide the VLM during supervised fine-tuning*

## 核心模块与公式推导

### 3.1 理论动机：从判别式分布到证据寻求分布

当前 VLM 的自回归训练目标为：

$$
\mathcal{L}_{\mathrm{AR}} = -\sum_i \log p_\theta(\boldsymbol{r}_i \mid \mathbf{V}, \boldsymbol{r}_{<i})
$$

其文本-视觉交叉注意力可近似为判别式分布 $p_\theta(t \mid V_f(s), s_{<i})$：

$$
A^{VLM}(t,s,f) \approx p_\theta(t \mid V_f(s), s_{<i})
$$

这一分布允许模型仅依赖静态外观线索（如物体纹理、形状）即可正确预测文本标记，而无需真正理解帧间动态。然而，运动理解任务本质上要求模型推断潜在运动证据 $\mathbf{E}$ 的分布：

$$
p^\star(a \mid \mathbf{V}, q) = \sum_{\mathbf{E}} p^\star(a \mid \mathbf{E}, q) \, p^\star(\mathbf{E} \mid \mathbf{V}, q)
$$

其中逐位置运动证据与帧间特征差异成正比：

$$
\mathbf{E}[\mathrm{Motion}(s,f)] \propto \| V_{f+1}(s) - V_f(s) \|
$$

这里存在一个关键的分布不匹配：VLM 学习的是 $p(t|V)$，而运动理解需要的是 $p(V|t)$——即给定概念 $t$，在时空位置 $(s,f)$ 上视觉特征出现的证据寻求分布。

### 3.2 VDM 注意力作为免费运动先验

Video Diffusion Model 在去噪过程中，其交叉注意力自然近似于证据寻求分布：

$$
A^{VDM}(t,s,f) \approx p_\phi(v_{s,f} \mid t, \mathbf{z}_k)
$$

其中 $\mathbf{z}_k$ 为第 $k$ 步去噪的隐变量。VDM 需要从噪声中重建视频帧，帧间差异大的区域（即运动显著区域）重建难度更高，因此 VDM 的注意力会自然地随运动幅度变化而调整——运动越剧烈的区域，VDM 分配的建模关注越多。这一性质使 VDM 注意力成为无需额外标注的运动校准先验。

### 4.1 多模态注意力提取

MotionEnhancer 从冻结的 CogVideoX VDM 中提取注意力图。给定视频 $\mathbf{V}$，先通过 5 步 DDIM 逆采样得到噪声隐变量，再经 5 步去噪采样，在每一步计算多模态注意力：

$$
A_{\mathrm{mm}} = \mathrm{Softmax}\left(\frac{Q_{\mathrm{mm}} K_{\mathrm{mm}}^T}{\sqrt{d}}\right)
$$

其中 $Q_{\mathrm{mm}}$ 和 $K_{\mathrm{mm}}$ 来自多模态隐变量 $\mathbf{z}_{\mathrm{mm}}$ 的 Query 和 Key 投影。该注意力图包含文本-视觉（t2v）和视觉-视觉（v2v）两个子区域，为后续的运动敏感筛选提供原始信号。

### 4.2 运动中心注意力精炼

原始 VDM 注意力图中并非所有注意力头和文本标记都与运动相关。MotionEnhancer 设计了两个参数无关的筛选模块。

**运动敏感头筛选（MHS）** 基于 VDM 注意力常呈现对角线模式这一观察，利用三个指标筛选运动相关的注意力头：

- **对角线集中度（DFC）**：衡量 v2v 注意力在对角线区域 $\mathcal{M}$ 内的聚焦程度：

$$
\mathrm{DFC} = \frac{\sum_{(i,j) \in \mathcal{M}} A_{\mathrm{v2v}}^2[i,j]}{\sum_{(i,j) \notin \mathcal{M}} A_{\mathrm{v2v}}^2[i,j]}
$$

- **时间连续性得分（TCS）**：衡量跨帧空间一致性注意力的持续性，对每帧 $s$ 计算最大连通分量长度 $l_i$ 并取平均：

$$
\mathrm{TCS} = \frac{1}{S} \sum_{s=1}^{S} \frac{1}{m} \sum_{i=1}^{m} l_i
$$

- **对角线显著性比率（DSR）**：统计对角线区域 $D$ 中高注意力值的普遍程度：

$$
\mathrm{DSR} = \frac{n_{\mathrm{high}}}{|D|}
$$

综合三个指标排序后，选取前 50% 的注意力头作为运动敏感头。

**运动显著文本标记识别（MTTI）** 在聚合运动敏感头后，提取文本-帧注意力区域 $A_{\mathrm{t2f}}^t$，为每个文本标记计算运动评分：

$$
\mathbf{MS}(t) = \operatorname{Mean}_f(A_{\mathrm{t2f}}^t) + \frac{1}{F-1} \sum_{f=1}^{F-1} |A_{\mathrm{t2f}}^t(f+1) - A_{\mathrm{t2f}}^t(f)|
$$

该评分结合了平均注意力强度（反映概念显著度）和帧间一阶差分（反映时间波动性），二者共同指示文本标记与运动的相关程度。按运动评分排序后，选取前 50% 的文本标记参与后续对齐。

### 4.3 注意力对齐与联合训练

筛选后的 VDM 注意力 $A_{\mathrm{VDM}}$ 作为监督信号，通过一个轻量 Aligner（线性投影层）将 VLM 的文本-视觉注意力映射到与 VDM 注意力相同的空间，计算 MSE 损失：

$$
\mathcal{L}_{\mathrm{MSE}} = ||\mathrm{Aligner}(A_{\mathrm{VLM}}) - A_{\mathrm{VDM}}||_2
$$

总损失为自回归损失与注意力对齐损失的加权和：

$$
\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{AR}} + \lambda \mathcal{L}_{\mathrm{MSE}}
$$

其中 $\lambda$ 为平衡超参数。训练时 VLM 的视觉塔、融合层和 LLM 主干均参与更新，而 VDM 保持冻结。

## 实验与分析

### 核心实验结果

MotionEnhancer 在两个运动理解基准上对多种 VLM 展现出一致且可观的性能提升。实验选取 Qwen2.5-VL（3B/7B）和 InternVL3-8B 作为基础 VLM，在 MotionBench 和 FAVOR-Bench 上进行评估。

在 **MotionBench** 上，MotionEnhancer 为所有模型带来显著的总体准确率增益：
- Qwen2.5-VL-3B：56.60%（**+3.04**）
- Qwen2.5-VL-7B：57.04%（**+4.23**）
- InternVL3-8B：57.69%（**+2.81**）

在 **FAVOR-Bench** 上，该方法同样保持一致的提升趋势，验证了其跨基准的泛化能力。值得注意的是，提升主要集中在运动相关的子指标上，而非通用视频理解指标，这直接印证了方法对运动理解的特异性增强效果。

与现有运动增强方法的对比进一步凸显了 MotionEnhancer 的优势。相比 **Motion-Sight**（Du et al., arXiv 2025）和 **TE Fusion**（Hong et al., CVPR 2025），MotionEnhancer 无需修改 VLM 架构或引入额外训练参数，仅通过注意力对齐即可取得更优或相当的性能，展现出更高的参数效率和架构兼容性。

### 消融实验

为验证各模块的贡献，作者在 Qwen2.5-VL-7B 上进行了系统的消融实验。结果确认了 MHS 和 MTTI 的互补性：

- **仅 MHS**：在 MotionBench 上 Overall 提升 +1.77，在 FAVOR-Bench 上 Overall 提升 +1.82，表明筛选运动敏感注意力头本身即可提供有效的运动先验。
- **仅 MTTI**：同样带来一致的性能提升，证明聚焦运动显著的文本标记有助于减少无关语义的干扰。
- **MHS + MTTI 联合**：达到最佳性能（MotionBench Overall 57.04 / Average 52.92；FAVOR-Bench Overall 46.88 / Average 47.01），增益显著高于单独使用任一模块。这验证了两个模块在过滤维度上的互补性——MHS 从注意力头维度筛选运动相关信号，MTTI 从文本标记维度消除运动无关语义，二者协同实现了更精准的运动注意力对齐。

### 失败模式与局限性分析

尽管 MotionEnhancer 在整体上表现优异，分析揭示了其运动理解增强存在场景依赖性。VDM 的训练数据主要包含小物体，导致其对大面积静态主体（如占据整个画面的静止物体）的注意力发散。当视频中的主要运动对象在画面中占比较小、而背景或静态主体占据主导时，VDM 提取的运动先验质量下降，进而限制了 VLM 在这些场景下的运动理解提升。这一数据偏差是当前方法的主要瓶颈，未来需探索更精细的运动区域提取或针对性的数据预处理策略。

此外，当前方法仅使用固定的 CogVideoX 作为运动先验来源，未利用不同 VDM 的互补性。不同 VDM 可能在不同运动模式或场景下具有各自的注意力优势，缺乏自适应选择或融合机制限制了运动先验的覆盖范围和鲁棒性。

### 实验设置要点

训练采用标准的有监督微调范式，VLM 的视觉编码器、融合层和 LLM 主干均参与训练。VDM 保持冻结状态，通过 5 步 DDIM 逆采样后接 5 步去噪提取交叉注意力图，在计算开销和注意力质量之间取得平衡。优化器使用 AdamW（β₁=0.9, β₂=0.999, ε=1e-8），总损失为自回归损失与注意力对齐损失的加权和：

$$\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{AR}} + \lambda \mathcal{L}_{\mathrm{MSE}}$$

其中注意力对齐损失采用 L2 距离：

$$\mathcal{L}_{\mathrm{MSE}} = ||\mathrm{Aligner}(A_{\mathrm{VLM}}) - A_{\mathrm{VDM}}||_2$$

该方法不修改 VLM 架构，可适配不同的 VLM 和 DiT 类 VDM，具有良好的通用性。

### 补充图表

![[assets/figures/papers/paper_list_l2328_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_MotionEnhancer_Leve/figures/003_Table_1.jpg]]
*Table 1: Quantitative results of MotionBench. * denotes results we reproduced using their open-source code, while other results are taken from the original benchmark*

![[assets/figures/papers/paper_list_l2328_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_MotionEnhancer_Leve/figures/004_Table_2.jpg]]
*Table 2: Quantitative results of FAVOR-Bench. * denotes results we reproduced using their open-source code, while other results are taken from the original benchmark. (For more VLMs, please see supplementary materials.)*

![[assets/figures/papers/paper_list_l2328_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_MotionEnhancer_Leve/figures/005_Table_3.jpg]]
*Table 3: Ablation study of MHS and MTTI using Qwen2.5VL-7B. These results confirm that MHS and MTTI are complementary, and combining them yields the highest gains*

![[assets/figures/papers/paper_list_l2328_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_MotionEnhancer_Leve/figures/006_Figure_3.jpg]]
*Figure 3: Qualitative examples of MotionEnhancer. (More examples can be found in supplementary materials.)*

## 方法谱系与知识库定位

### 核心问题与因果机制

现有视觉语言模型（VLM）在视频理解任务中学习的本质是一个判别式分布 $p(t|V)$，即给定视觉输入预测文本标记。这一学习范式允许模型依赖静态外观线索（如物体纹理、场景布局）来满足训练目标，而无需真正捕获帧间的细粒度时间动态，导致对运动细节的理解不足。MotionEnhancer 的核心洞察在于：视频扩散模型（VDM）在去噪生成过程中自然编码了运动校准的跨模态注意力，其注意力图近似于证据寻求分布 $p(V|t)$——即给定文本概念，模型需要在时空维度上定位该概念的视觉证据。这种分布天然对运动幅度敏感：帧间变化越大的区域，重建难度越高，VDM 分配的关注也越多。

MotionEnhancer 的因果操作由此明确：通过将 VLM 的文本-视觉注意力与从 VDM 蒸馏的运动先验进行对齐，为 VLM 注入时间动态敏感性。这一对齐过程不引入额外可训练参数，而是通过两个参数无关的筛选模块——运动敏感头选择（MHS）和运动显著文本标记识别（MTTI）——从 VDM 的原始注意力图中提取高质量的运动监督信号，再以简单的 MSE 损失引导 VLM 微调。

### 与已有工作的关系

**零样本 VLM 基线**：Qwen2.5-VL（3B/7B）和 InternVL3-8B 作为零样本基线，代表了当前主流 VLM 在运动理解上的原生能力。这些模型在 MotionBench 和 FAVOR-Bench 上的表现揭示了判别式训练范式固有的运动理解短板。

**标准 SFT 基线**：在 25k 视频 QA 数据上进行标准监督微调（仅自回归损失 $\mathcal{L}_{\mathrm{AR}}$），不引入 VDM 引导。该基线用于隔离注意力对齐损失带来的增益，证明性能提升并非单纯来自额外训练数据。

**Motion-Sight**（Du et al., arXiv 2025）：作为先前的运动增强方法，Motion-Sight 同样关注 VLM 的运动理解能力提升，但其技术路线与 MotionEnhancer 不同。MotionEnhancer 通过注意力对齐从 VDM 蒸馏运动先验，而无需修改 VLM 架构或引入额外可训练参数。

**TE Fusion**（Hong et al., CVPR 2025）：作为时间建模方法，TE Fusion 侧重于通过时序融合增强视频表征。MotionEnhancer 与之互补——前者改进视觉编码器的时间聚合，后者通过注意力层面的运动先验注入来校准文本-视觉对齐。

### 适用边界与局限性

1. **VDM 训练数据偏差**：当前使用的 CogVideoX 作为固定运动先验来源，其训练数据主要包含小物体。对于大面积静态主体（如占据整个画面的静止物体），VDM 的注意力趋向发散，导致运动理解提升有限。这一偏差源于 VDM 自身的生成分布特性，而非方法设计缺陷，但限制了在特定场景下的增益幅度。

2. **单一 VDM 先验**：方法仅使用了固定的 CogVideoX 作为运动先验来源，未利用不同 VDM 的互补性或自适应选择机制。不同 VDM 在运动建模粒度、时空分辨率上的差异可能为不同类型的运动理解任务提供差异化监督。

3. **DiT 架构依赖**：注意力提取依赖于 VDM 的交叉注意力机制，目前适配于 DiT 类视频扩散模型。对于采用其他架构（如纯 3D 卷积）的生成模型，需重新设计运动先验提取方式。

### 开放问题

1. **VDM 注意力偏差的缓解**：如何通过更精细的运动提取或数据预处理来缓解 VDM 在大面积静态主体上的注意力发散问题？可能的路径包括多尺度运动区域检测、前景运动分割引导的注意力重加权，或引入物理运动估计（如光流）作为辅助先验。

2. **运动潜变量的下游迁移**：从 VDM 提取的运动潜变量能否作为对时间动态高度敏感的下游任务（如机器人抓取、动作预测）的运动感知预训练信号？若能，这种运动先验是否能提高样本效率和时间泛化能力？这需要验证 VDM 注意力中编码的运动信息是否具有任务无关的通用性。

3. **多 VDM 集成与自适应选择**：不同 VDM 在运动建模上可能存在互补性（如某些模型更擅长精细动作，另一些更擅长大幅运动）。能否设计自适应选择机制，根据输入视频的运动特性动态选择最合适的 VDM 先验来源？

4. **理论收敛性**：当前理论分析揭示了 $p(t|V)$ 与 $p(V|t)$ 的分布不匹配，但注意力对齐损失 $\mathcal{L}_{\mathrm{MSE}}$ 的引入如何影响 VLM 原有表征空间的收敛性质，仍需更深入的理论刻画。

## 原文 PDF

![[paperPDFs/CVPR_2026/MotionEnhancer_Leveraging_Video_Diffusion_for_Motion_Enhanced_Vision_Language_Models.pdf]]