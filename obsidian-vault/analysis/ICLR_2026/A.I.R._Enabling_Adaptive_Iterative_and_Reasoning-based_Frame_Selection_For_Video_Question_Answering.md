---
title: "A.I.R.: Enabling Adaptive, Iterative, and Reasoning-based Frame Selection For Video Question Answering"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/A.I.R._Enabling_Adaptive_Iterative_and_Reasoning-based_Frame_Selection_For_Video_Question_Answering.pdf
aliases:
- IR
- IREAIRBFSVQA
acceptance: accepted
tags:
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/vision_models_multimodal
core_operator: 查询与帧之间关系的语义理解深度和计算分配策略。通过VLM只对少量高潜帧进行推理分析，并利用局部密度采样迭代扩展相关区域，在控制计算成本的同时实现准确选择。
primary_logic: 利用强大的VLM进行深度语义分析，但通过迭代循环仅处理少量高潜帧，并通过局部密度采样发现被轻量模型低估的关键帧，从而在计算效率上实现VLM分析的可处理性，同时保持高精度帧选择。
claims:
- "A.I.R. performs frame selection in three stages: Adaptive Initial Sampling, Iterative Frame Selection, and QA Stage."
- Adaptive threshold is dynamically computed per video using GMM, separating high-relevance frames from low-relevance ones.
- Iterative Frame Selection progressively refines the candidate set using a four-step loop with VLM analysis on small batches.
- A.I.R. + InternVL-3 achieves 62.8% on LongVideoBench (+4.5%) and 82.6% on NextQA, while analyzing far fewer frames.
paradigm: 利用强大的VLM进行深度语义分析，但通过迭代循环仅处理少量高潜帧，并通过局部密度采样发现被轻量模型低估的关键帧，从而在计算效率上实现VLM分析的可处理性，同时保持高精度帧选择。
---

# A.I.R.: Enabling Adaptive, Iterative, and Reasoning-based Frame Selection For Video Question Answering

> [!tip] 核心洞察
> 利用强大的VLM进行深度语义分析，但通过迭代循环仅处理少量高潜帧，并通过局部密度采样发现被轻量模型低估的关键帧，从而在计算效率上实现VLM分析的可处理性，同时保持高精度帧选择。

| 字段 | 内容 |
|------|------|
| 中文题名 | A.I.R.: 自适应、迭代和基于推理的帧选择用于视频问答 |
| 英文题名 | A.I.R.: Enabling Adaptive, Iterative, and Reasoning-based Frame Selection For Video Question Answering |
| 会议/期刊 | ICLR 2026 (accepted) |
| Links | [paper](https://openreview.net/forum?id=SZVpOKw0YD) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal |
| Method | A.I.R. |
| Dataset | Video-MME (w/o subtitle), LongVideoBench (LVB), NextQA |

> [!tip] 效果简介
> - Video-MME (w/o subtitle) 上，Accuracy (%) 为 68.2 (InternVL3-8B + A.I.R.)，对比 65.6 (InternVL3-8B Uniform)，变化 +2.6。
> - LongVideoBench (LVB) 上，Accuracy (%) 为 62.8 (InternVL3-8B + A.I.R.)，对比 58.3 (InternVL3-8B base)，变化 +4.5。
> - NextQA 上，Accuracy (%) 为 81.3 (QwenVL-2.5 + A.I.R.)，对比 74.3 (QwenVL-2.5 base)，变化 +7.0。

## 概述

视频问答任务通常需要从长视频中筛选出与查询相关的帧。现有方案主要面临两难：轻量级相似度模型（如CLIP）产生的得分尽管计算成本低，但在处理复杂查询时往往无法准确反映帧与查询的真实语义相关性；而直接使用强大的视觉语言模型（VLM）对所有帧进行深度分析则会产生难以承受的计算开销。这一瓶颈的症结在于**帧-查询关系的语义理解深度**与**计算资源分配策略**之间的冲突。

针对上述问题，本文提出 **A.I.R.**（Adaptive, Iterative, and Reasoning‑based Frame Selection），一种完全训练自由（training‑free）且即插即用的帧选择框架。其核心思想是：利用强大的分析用 VLM 进行深层语义挖掘，但通过**迭代循环只将少量高潜力帧送入 VLM 分析**，同时采用**局部密度采样**发现被轻量模型低估的关键帧，从而在可承受的计算成本下实现高精度的查询相关帧选择。整个方法包含三个阶段（Fig. 2）：

- **自适应初始采样**（Adaptive Initial Sampling）：利用高斯混合模型（GMM）为每个视频动态计算自适应相似度阈值，识别出与查询相关的“事件”片段，并按事件宽度比例分配帧数，从中采样高相关帧作为初始候选集（Sec. 3.2）。
- **迭代帧选择**（Iterative Frame Selection）：每轮迭代包含四步：通过区间潜力排名选出高潜力的帧区间；由分析 VLM 对少量帧进行推理评估并给出相关性评分；利用提前停止机制在达到自适应预算时终止；对已验证的正帧邻域进行局部密度采样，发现被轻量模型低估的帧并反馈至下一轮（Sec. 3.3）。
- **问答阶段**（QA Stage）：将最终选定的帧集送入答案生成 VLM 完成一次推理，得到答案。

通过这种机制，A.I.R. 将 VLM 的分析次数严格控制在由视频长度决定的自适应范围内，既能避免轻量模型的歧义问题，又避免了 VLM 全量分析的计算爆炸。实验表明，在 LongVideoBench 上，InternVL‑3‑8B 结合 A.I.R. 取得了 62.8% 的准确率，较基线提升 4.5%；在 NextQA 上，QwenVL‑2.5 结合 A.I.R. 达到 81.3%，提升 7.0%；在 Video‑MME（无字幕）上，同样模型下亦有 2.6% 的增益，且这些提升均在使用远少于均匀采样的帧数下实现（Tab. 1, Tab. 2, Tab. 4）。消融实验进一步证实，移除迭代框架、推理型 VLM 分析或自适应初始采样均会导致性能显著下降，验证了每一步设计的必要性（Tab. 4）。与其他训练自由的帧选择方法相比，A.I.R. 在多个基准上均表现出更好或相当的性能，且无需任何微调，证明了该框架的有效性与通用性。

## 背景与动机

视频问答（Video QA）要求模型在理解整段视频语义的基础上，针对用户的自然语言问题给出准确答案。一个关键的子任务是**查询相关的帧选择**：从原始视频中找出与当前问题高度相关的少数帧，供后续回答模型使用。这一环节直接决定了回答模型能否“看到”关键信息，因此成为影响整体性能的瓶颈。

现有的帧选择方法主要分为两条技术路线（图 1a）：  
- **轻量相似度模型**：以 CLIP 为代表，为每一帧与查询计算相似度得分，再通过得分筛选帧。这种方法计算开销极低，但面对复杂、细粒度的查询时，简单的相似度往往无法可靠地反映真实的语义相关性——即“相似度模糊”问题（图 1b）。  
- **大型视觉语言模型（VLM）分析**：直接使用强大的 VLM 对所有帧逐一进行推理分析，能够捕捉深层的语义关联，但计算量与帧数成正比，当视频较长时计算代价不可接受——“计算成本爆炸”成为主要障碍（图 1c）。

因此，**核心矛盾**在于：轻量模型缺乏足够的语义理解能力，难以应对复杂查询；而大型 VLM 分析虽然具备深度语义推理能力，却因计算成本过高而难以大规模使用。此前的工作要么完全信赖轻量相似度（容易忽略被低估的关键帧），要么一次性将大量候选帧送入 VLM 分析（造成资源浪费），缺乏一种在计算效率和分析深度之间动态平衡的机制。

为缓解上述矛盾，本文提出 **A.I.R.（自适应、迭代和基于推理的帧选择）**，其核心动机是：**只让强大的 VLM 处理少量最有可能相关的帧，并通过迭代反馈持续发现被轻量模型遗漏的关键区域**。这一思路源于一个关键洞察：轻量相似度虽然在大粒度上不够可靠，但其整体分布仍能提供关于“事件”结构的先验信号，可以用来在初始阶段缩小搜索范围；而 VLM 的深度分析可以被组织成一个增量式的验证-扩展循环，从而在精度与成本之间实现可控的权衡。

A.I.R. 的总体流程（图 2）由三个阶段组成：
1. **自适应初始采样**：利用 CLIP 相似度并通过高斯混合模型（GMM）动态计算每视频的自适应阈值，识别出可能相关的“事件”区间，按事件长度比例分配采样预算，产生少量高潜力初始帧。
2. **迭代帧选择**：在一个四步循环中，每一轮仅选取约 C（8 ~ 12）帧送入分析 VLM 进行推理打分，若验证为正相关则在帧邻域进行局部密度采样，将未被轻量模型高估的帧重新加入下一轮候选，直到达到自适应预算或提前停止。
3. **问答阶段**：将最终选定的帧集送入问答 VLM，输出答案。

这一设计从根本上改变了计算分配方式：分析型 VLM 不再是对全部帧的“暴力穷举”，而是只在最需要的局部区域进行聚焦式推理。后续实验表明，该方法在多个长视频基准（如 LongVideoBench、NextQA、Video-MME）上，能以远少于均匀采样的分析帧数，获得最高 +4.5% ~ +7.0% 的绝对精度提升，验证了其“低成本、高精度”的可行性。

## 核心创新

A.I.R. 的核心创新在于重新定义了**VLM分析的计算分配策略**与**查询‑帧相关性的语义理解深度**之间的权衡关系。传统方法面临一个根本性瓶颈：轻量相似度模型（如 CLIP）计算廉价但对复杂查询产生不可靠的相关性信号（Figure 1b），而强大的分析VLM虽能进行深度语义推理，但对所有候选帧逐一分析却导致计算成本爆炸（Figure 1c）。A.I.R. 将这一困境转化为可操作的迭代优化问题。

### 关键创新点

**1. 轻量模型从决策者降级为启发式指引**

Baseline 方法将 CLIP 相似度得分作为最终帧选择的直接依据，导致对需要时序推理、因果关系理解或细粒度视觉匹配的查询频繁失败。A.I.R. 仅让 CLIP 承担两项辅助任务：① 对均匀采样帧计算查询‑帧相似度信号 $S$，用于初步的事件边界识别；② 在迭代循环外部提供轻量的邻域搜索空间。真正的相关性判断完全交由分析 VLM 完成。

**2. 迭代式 VLM 分析替代一次性暴力推理**

与 VideoTree 等方法将所有候选帧一次性送入 VLM 不同，A.I.R. 设计了一个**四步迭代循环**（Algorithm 1）。每轮只分析少量高潜帧（chunk $C \approx 8$–$12$ 帧），通过提前停止机制严格控制总分析量。这使 VLM 的工作负载满足 $w_{\text{best}} \leq n_{\text{A.I.R.}} \leq w_{\text{worst}}$，确保计算成本在可预测范围内，同时保留充分的语义分析深度。

**3. 自适应初始采样替代静态 Top‑K 选择**

A.I.R. 引入**基于 GMM 的动态阈值机制**：

$$T = \max(\mu_1, \mu_2) - \gamma \cdot \max(\sigma_1, \sigma_2)$$

该阈值根据每个视频独特的相似度分布动态计算，将高于阈值 $T$ 的连续帧识别为候选“事件”（events）。随后的事件宽度比例采样确保预算 $K$ 按事件时长分配，每个事件至少获得 1 帧，并在事件内部取峰值相似度帧。相比固定阈值或全局 Top‑K 的 baseline，该策略在视频内和视频间均自适应调整。

**4. 局部密度采样发现被低估的关键帧**

这是 A.I.R. 最有特色的机制。CLIP 等轻量模型常低估某些对查询至关重要但视觉相似度不突出的帧。A.I.R. 在每轮迭代结束后，在已验证正帧 $\mathcal{F}^* = \{f_i \mid R_i > \theta\}$ 的邻域进行细粒度搜索（Localized Density Sampling），在原始视频的 $N$ 帧（非均匀采样的 $n$ 帧）层级上进行。新发现的帧被反馈到下一轮迭代的候选池中，形成闭环优化。消融实验（Table 4）表明，移除该组件使准确率从 68.2% 降至 66.9%，验证了其对纠正轻量模型误判的关键作用。

**5. 区间潜力排名引导 VLM 关注信息密集区域**

候选帧生成并非仅依赖单帧得分，而是通过区间潜力函数综合评估帧间区域：

$$\text{Potential}(\text{I}_i) = \underbrace{\text{Mean}(S_{f_i:f_{i+1}})}_{\text{相关性}} \cdot \underbrace{\left(1 + \frac{\sum |S_{j+1} - S_j|}{f_{i+1} - f_i}\right)}_{\text{复杂度}} \cdot \underbrace{(1 + c_{\text{len}} \cdot \lg(f_{i+1} - f_i))}_{\text{长度}}$$

该公式优先选择相似度均值高、变化剧烈（可能蕴含事件转折）、跨度大的区间，使 VLM 的有限分析预算集中于信息最丰富的视频片段。

### 创新总结

| 变化维度 | Baseline 做法 | A.I.R. 做法 | 核心收益 |
|---------|-------------|-----------|---------|
| 初步相似度利用 | CLIP 直接决定最终选择 | CLIP 仅用于事件识别和初始化 | 避免轻量模型的语义误判 |
| VLM 分析策略 | 一次性大范围分析 | 迭代式小批次分析 + 提前停止 | 计算成本可控，深度保留 |
| 候选帧生成 | 均匀采样或 Top‑K | GMM 自适应阈值 + 事件比例采样 | 视频间/视频内自适应 |
| 相关区域发现 | 无 | 局部密度采样反馈循环 | 纠正 CLIP 低估的帧 |

这些创新协同作用，使 A.I.R. 成为一个完全 **training‑free** 的框架，在多个基准上以平均 **22.5% 更少的分析帧数**实现一致且显著的性能提升（Table 1、Table 2、Table 4），并能泛化到时间定位任务（Table 8），展现出跨任务、跨 VLM 骨架的鲁棒性。

## 整体框架

![[obsidian-vault/assets/figures/papers/iclr26_0005_SZVpOKw0YD_A.I.R._Enabling_Adaptive_Iterative_and_Reasoning/figures/002_Figure_2.jpg]]
*Figure 2: General pipeline of A.I.R. with three stages: (1) Adaptive Initial Sampling that identifies potential 'events' based on query similarity and dynamically samples frames around them using an adaptive budget; (2) Iterative Frame Selection that progressively refines the frame selection via four steps; and (3) QA Stage that feeds the final selected frames into Answering VLM*

![[obsidian-vault/assets/figures/papers/iclr26_0005_SZVpOKw0YD_A.I.R._Enabling_Adaptive_Iterative_and_Reasoning/figures/003_Figure_3.jpg]]
*Figure 3: Two main stages in our A.I.R.. (a) Adaptive Initial Sampling: A GMM-based adaptive threshold is applied to the query-frame similarity S to identify potential events, and then event-wise sampling is conducted on the refined events to obtain K frames ( \mathcal { F } _ { \mathrm { i n i t i a l } } ) . (b) Iterative Frame Selection: In each iteration, 1) High-potential candidates are selected via Interval Potential Ranking; 2) A VLM performs reasoning-based analysis to validate the best frames; 3) An Early Stop mechanism checks if the frame budget is met; And 4) if not met, the Localized Density Sampling (LDS) discovers more frames around the validated frames and feed them into the next itera...*

A.I.R. 的整体流程分为三个阶段：**自适应初始采样（Adaptive Initial Sampling）**、**迭代帧选择（Iterative Frame Selection）** 和 **问答阶段（QA Stage）**（图 2）。其设计核心在于绕开轻量模型直接筛选的歧义性与大型 VLM 全量分析的计算爆炸，通过**只对少量高潜帧进行推理型 VLM 分析，并利用局部密度采样迭代扩展相关区域**，在可控成本下实现精确的查询‑相关性帧选择。

**预处理与相似度信号**  
对原始视频（共 N 帧）先以固定帧率均匀采样得到 n 帧。这 n 帧通过 CLIP 模型计算与查询的相似度序列 S，作为后续两个阶段的基础信号（Sec. 3.1）。

**阶段一：自适应初始采样**  
本阶段从 n 帧中动态选出 K 个与查询相关的帧，为后续迭代提供先验并降低计算量。具体步骤如下：  
1. **自适应阈值**：对相似度序列 S 拟合两分量高斯混合模型（GMM），由高、低相关簇的均值（μ₁, μ₂）和标准差（σ₁, σ₂）按公式 (1) 动态计算阈值 T，分离出高相关帧。  
2. **事件识别与采样**：将连续高于 T 的帧段定义为“事件”。根据视频长度自适应地确定总采样预算 B，再按事件时长比例分配帧数，每事件至少采样一帧，并从各事件内选择相似度峰值帧，最终组成初始帧集 $\mathcal{F}_{\mathrm{initial}}$（Sec. 3.2, 附录 A.2.2）。  

**阶段二：迭代帧选择**  
这一阶段以分析型 VLM 的深度语义判断为主，但通过迭代循环仅在每轮处理少量高潜候选（C ≈ 8–12 帧），并在满足自适应预算时提前终止，从而大幅限制 VLM 调用总次数（Alg. 1）。每轮迭代包含四个步骤（Fig. 3(b)）：

1. **区间潜力排名（Interval Potential Ranking）**  
   将当前候选帧之间的区间 $\mathrm{I}_i$ 计算潜力分数，综合考虑区间内相似度均值（相关性）、总变分（复杂度）以及区间长度，按公式 (4) 排序，选出得分最高的 C 个区间。

2. **推理型 VLM 分析（Reasoning‑Based VLM Analysis）**  
   将选中区间的帧送入分析 VLM，由 VLM 输出每帧的相关性评分 Rᵢ 和解释文本，并通过阈值 θ 筛选出正相关帧，构成验证帧集 $\mathcal{F}^*$（公式 (5)）。

3. **提前停止机制（Early Stop）**  
   若已验证的帧数已达到自适应预算 B，则终止迭代；否则继续第四步。

4. **局部密度采样（Localized Density Sampling）**  
   在原视频（N 帧）上，以已验证正帧的邻域为中心进行细粒度搜索，发掘被 CLIP 低估的关键帧，并将其作为下一轮迭代的新候选，形成反馈循环（Sec. 3.3, 附录 A.2.3）。

**阶段三：问答阶段**  
上述迭代结束后，将最终选定的帧集与查询一起送入答案 VLM，进行一次推理生成最终答案（Sec. 3.1）。整个过程中，A.I.R. 不依赖任何微调，属于完全训练免的方法。

## 核心模块与公式推导

A.I.R. 的核心洞察是：轻量相似度模型（如 CLIP）对复杂查询产生的相似度得分无法准确反映真实的查询‑帧相关性，而直接使用 VLM 对所有帧进行深度分析计算成本过高。因此，A.I.R. 将强大的 VLM 分析限制在少量高潜帧上，并通过局部密度采样发现被轻量模型低估的关键帧，从而在控制计算成本的同时实现准确选择。整体流程由三个阶段组成：自适应初始采样、迭代帧选择、问答阶段（Fig. 2）。

### 1. 自适应初始采样（Adaptive Initial Sampling）

此阶段的目标是在正式迭代前，快速筛选出 $K$ 个与查询相关的候选帧，为后续 VLM 分析提供先验指导并降低计算压力。

**自适应阈值计算**：对 CLIP 模型在 $n$ 帧均匀采样后得到的相似度序列 $S$，采用高斯混合模型（GMM）拟合成高相关簇与低相关簇。自适应阈值 $T$ 由下式给出：

$$
T = \operatorname*{max}( \mu_1, \mu_2 ) - \gamma \cdot \operatorname*{max}( \sigma_1, \sigma_2 )
$$

其中 $\mu_1, \mu_2$ 和 $\sigma_1, \sigma_2$ 分别为两簇的均值和标准差，$\gamma$ 为控制阈值宽松程度的超参数。该阈值完全根据每个视频独有的相似度分布动态计算，避免了固定阈值对不同视频的适应性不足。

**事件识别与采样**：将相似度持续高于 $T$ 的连续帧段记为“事件” $\mathcal{E}'$。为提高可靠性，论文通过合并短间隔等后处理得到精炼事件集 $\mathcal{E}$。随后按事件持续时间比例分配采样预算 $k_j$，每个事件至少采样 1 帧，并优先选取相似度峰值点，最终形成初始候选帧集合 $\mathcal{F}_{\text{initial}}$，共 $K$ 帧。

### 2. 迭代帧选择（Iterative Frame Selection）

该阶段是 A.I.R. 的核心引擎，在每轮迭代中仅对少量帧应用 Analysis VLM 进行推理分析，并通过反馈机制逐步扩大搜索范围。每次迭代包含四个步骤：

**Step 1: 区间潜力排名（Interval Potential Ranking）**
对 $\mathcal{F}_{\text{initial}}$ 中相邻帧构成的区间 $I_i = [f_i, f_{i+1}]$，计算其潜力分数，用以决定本轮应将 VLM 分析资源投向哪些区间：

$$
\mathrm{Potential}(I_i) = \underbrace{\mathrm{Mean}(S_{f_i:f_{i+1}})}_{\mathrm{Relevance}} \cdot \underbrace{\left(1 + \frac{\sum_{j=f_i}^{f_{i+1}} |S_{j+1} - S_j|}{f_{i+1} - f_i}\right)}_{\mathrm{Complexity}} \cdot \underbrace{(1 + c_{\mathrm{len}} \cdot \lg(f_{i+1} - f_i))}_{\mathrm{Length}}
$$

公式由三项相乘构成：
- **相关性（Relevance）**：区间内 CLIP 相似度的均值，反映该区间整体与查询的相关程度。
- **复杂度（Complexity）**：通过相似度序列的总变分归一化后加 1，捕捉区间内语义波动剧烈的程度——波动大的区间更可能隐藏关键帧。
- **长度（Length）**：对区间帧数取对数后加权，防止大区间遗漏信息。

根据潜力排名选出 $C$ 个高潜区间，并在每个区间内选取得分最高的帧作为本轮候选 $\mathcal{F}_{\text{cand}}$。

**Step 2: 基于推理的 VLM 分析（Reasoning‑based VLM Analysis）**
将 $\mathcal{F}_{\text{cand}}$ 中的帧连同查询一起送入 Analysis VLM，要求 VLM 对每帧的相关性进行推理并给出 $[0,1]$ 的评分 $R_i$。只有评分超过阈值 $\theta$ 的帧被纳入验证帧集合 $\mathcal{F}^*$：

$$
\mathcal{F}^* = \{ f_i \in \mathcal{F}_{\mathrm{cand}} \mid R_i > \theta \}
$$

此步骤是整个方法的关键因果调节变量——用强大 VLM 的语义理解取代轻量模型不可靠的相似度，但又只对少量候选帧执行，从而保证可行性。

**Step 3: 提前停止（Early Stop）**
检查当前已验证帧数是否达到自适应预算 $B$（根据视频帧数 $n$ 按比例计算，并夹在 $V_{\min}$ 与 $V_{\max}$ 之间）：

$$
B = \operatorname*{max}\left( \operatorname*{min}\left( \left| V_{\max} \cdot \frac{n}{300} \right|, V_{\max} \right), V_{\min} \right)
$$

若已达到或超过 $B$，则立即终止迭代，将已验证帧作为最终选定帧集输出。

**Step 4: 局部密度采样（Localized Density Sampling）**
若未达到停止条件，则在已验证正帧的邻域进行细粒度搜索——返回原始视频（$N$ 帧而非均匀采样的 $n$ 帧）中在正帧附近采样额外的帧，将其加入下一轮迭代的候选池。这一机制使得被轻量模型低估但在时间上紧邻高相关帧的关键帧得以被 VLM 重新评估，形成“发现‑验证‑扩展”的正反馈循环（详见 Alg. 1 及 Fig. 3(b)）。

### 3. 消融证据

消融实验（Table 4）验证了各模块的因果贡献：移除整个迭代帧选择阶段导致 Accuracy 从 68.2% 降至 65.2%（降幅最大）；移除基于推理的 VLM 分析（改为仅用相似度排名）降至 66.0%；移除区间潜力排名降至 66.7%；移除自适应初始采样降至 66.9%。此外，用固定 32 帧预算替代自适应预算仅增加 0.1% Accuracy，但多使用了 7.2 帧（24.8 → 32.0），印证了自适应预算在效率上的优势。

> **需手动验证**：GMM 拟合的超参数 $\gamma$、停止阈值 $\theta$、以及 $C$（每轮候选帧数）和 $T_{\max}$（最大迭代次数）的具体取值及其调参敏感性，在审查范围内未获提供，建议根据原文 Sec. 4.2 或附录确认。

## 实验与分析

![[obsidian-vault/assets/figures/papers/iclr26_0005_SZVpOKw0YD_A.I.R._Enabling_Adaptive_Iterative_and_Reasoning/figures/004_Table_1.jpg]]
*Table 1: Comparison of VLMs and various frame selection methods on Video-MME, MLVU, and LongVideo Bench. ∗ denotes reported results, while † means reproduced ones (see Sec. 4.1)*

![[obsidian-vault/assets/figures/papers/iclr26_0005_SZVpOKw0YD_A.I.R._Enabling_Adaptive_Iterative_and_Reasoning/figures/010_Table_4.jpg]]
*Table 4: Ablations of A.I.R.'s components on Video-MME using InternVL3-8B. We compare on average frames for answering VLMs and accuracy (Acc.)*

![[obsidian-vault/assets/figures/papers/iclr26_0005_SZVpOKw0YD_A.I.R._Enabling_Adaptive_Iterative_and_Reasoning/figures/009_Table_3.jpg]]
*Table 3: Comparison of different VLM scales with A.I.R. on Video-MME (w/o subtitle, 32 frames)*

![[obsidian-vault/assets/figures/papers/iclr26_0005_SZVpOKw0YD_A.I.R._Enabling_Adaptive_Iterative_and_Reasoning/figures/014_Table_8.jpg]]
*Table 8: Generalization results on temporal grounding benchmark Charades-STA (Gao et al., 2017). mIoU. Notably, A.I.R. substantially outperforms general-purpose VideoLLMs like Qwen2.5-VL-7B (44.5% → 59.5% R1@0.3) and even surpasses GPT-4o (32.0% vs. 39.5% R1@0.5). More impressively, our method achieves comparable or superior results to GenS (Yao et al., 2025), a trained frame selection method specifically designed for grounding tasks, while remaining completely trainingfree. While specialized temporal grounding models like TimeSuite (Zeng et al., 2024) achieve higher performance through task-specific training, our results demonstrate that A.I.R.'s adaptive sampling and iterative refinement effective...*

A.I.R. 的核心设计目标是在仅需轻量级 CLIP 相似度信号的训练‑free 条件下，用可控量级的 VLM 分析预算实现高精度帧选择。本节从主结果、消融、效率‑精度权衡及典型失败模式几个维度，系统验证这一设计是否成立，并归纳关键图表结论。

### 主结果：跨基准、跨模型尺度的稳定增益

在 LongVideoBench（LVB）、NextQA 和 Video‑MME 上，A.I.R. 均以显著更少的分析帧数取得了一致且可观的性能提升（Table 1，Table 2，Table 3）。

| 基准 | 问答 VLM | 基线方法 | 基线 Acc(%) | A.I.R. Acc(%) | Δ |
|------|----------|----------|--------------|----------------|----|
| LongVideoBench | InternVL3‑8B | Uniform（≤32帧） | 58.3 | 62.8 | +4.5 |
| NextQA | QwenVL‑2.5‑7B | Uniform | 74.3 | 81.3 | +7.0 |
| Video‑MME (w/o sub.) | InternVL3‑8B | Uniform（≤32帧） | 65.6 | 68.2 | +2.6 |
| Video‑MME (w/o sub.) | QwenVL‑2.5‑72B | Uniform（≤32帧） | 67.0 | 68.2 | +1.2 |

随着基础 VLM 能力增强，A.I.R. 带来的增益虽稍有收窄（从 7B 的 +4.2 降至 72B 的 +1.2，Table 3），但始终为正，且在小模型上尤为显著。这印证了方法的核心价值：在问答模型自身推理能力有限时，高质量帧选择能大幅弥补上下文窗口的压力。同时在 Video‑MME 的六种问题类型上，A.I.R. 在所有类型上均优于均匀采样（Fig. 4），其中对需要时序推理的“Temporal”类问题提升最大——这类查询恰好是纯相似度模型最容易失效的场景。

### 消融实验：迭代 VLM 分析与自适应机制缺一不可

Table 4 给出了 A.I.R. 各模块的消融结果（Video‑MME，InternVL3‑8B，最大 32 帧）。如下关键因果链条被证实：

1. **迭代帧选择阶段（整个 Sec 3.3 模块）是最关键的组件**：将其移除后准确率从 68.2% 骤降至 65.2%，甚至略低于均匀采样的 65.6%。这直接证明了仅依赖自适应初始采样（本质上是基于 CLIP 相似度的事件分割与自适应分配）不足以捕捉查询的真正需求，后续的 VLM 分析迭代是不可或缺的。
2. **推理型 VLM 分析**：若把迭代循环中的 VLM 分析替换为简单的相似度分数投票（即不做推理），准确率跌至 66.0%，说明让 VLM “理解”帧内容与查询的语义关联而非依赖底层相似度是提升的关键。
3. **区间潜力排名**和**自适应初始采样**分别贡献了约 1.5 和 1.3 个百分点的增益（移除后分别降至 66.7% 和 66.9%）。这两个模块共同解决了“在哪里找候选帧”的问题：自适应采样以事件宽度比例分配初始候选，潜力排名则在迭代中优先探索最有信息量的区间。
4. **自适应预算的有效性**：将自适应采样预算 B 换为固定 32 帧，准确率仅增加 0.1%（68.3%），但平均使用帧数从 24.8 帧升至 32.0 帧。这确认了公式 (8) 的自适应机制能够将 22.5% 的分析帧节省转化为几乎无损的精度（亦见 Appendix A.2.1 和 Table 4 最后一行）。

进一步超参数消融（Table 12、Table 14）显示，默认配置（候选数 C=12、最大迭代次数 $\mathcal{T}_{\mathrm{max}}=6$、自适应阈值系数 $\gamma=0.7$ 等）在 NextQA 和 LVB 上获得了效率‑精度的良好平衡：将 C 提升至 24 虽可获得 82.64% 的 NextQA 精度，但 VLM 分析总时长从 34.24 s 增至 59.38 s，实用性下降。局部密度采样的最小区间长度 $l_{\mathrm{min}}$ 和最小距离 $d_{\mathrm{min}}$ 对短时序视频（如 NextQA）影响较大，而过小的值容易引入噪声，表现为 NextQA 精度下降约 0.4–0.5 p.p.（Table 14）。

### 效率关键：VLM 分析帧数的实质性压缩

A.I.R. 将 VLM 分析帧数从典型的 128 帧（一次性深度分析）压缩至平均 12.4 ~ 36.5 帧（Tables 6、7）。例如，在 NextQA 上仅分析 12.4 帧便达到 81.7%（$w_{\mathrm{worst}}=16$），相比分析 128 帧的 VideoTree 等方法节省了一个数量级的 VLM 调用。时间维度上，Video‑MME 的总分析时间从 128 帧均匀分析的 162.03 s 降至 42.31 s（Table 7），且该时间尚包括 QA 阶段本身的前向推理开销。这种压缩之所以可行，是因为局部密度采样（LDS）在已确认的高相关帧周围进行细粒度搜索，将“被 CLIP 低估”的关键帧重新拉回候选池，使得迭代循环中的每轮 VLM 分析都聚焦于高信息量区域（详见 Sec 3.3 和 Fig. 3(b)）。

### 失败模式与挑战

尽管整体性能领先，所有方法（包括 A.I.R.）在“计数”（Counting）类问题上表现最差，A.I.R. 的精度仅为 49.3%（详见 Appendix 结果）。这一失败模式的存在与方法的底层假设直接相关：如果查询要求对大量相似目标或短暂出现的事件进行精确计数，CLIP 提供的初始相似度序列很难形成明显的高相关事件段，自适应阈值可能无法有效识别这些区域；随后即便有 VLM 参与迭代，也可能因候选集缺乏正确的锚点帧而难以收敛。该问题需要手动验证，也是未来改进的主要方向。

### 定性观察与泛化

A.I.R. 的迭代精炼过程在 Fig. 6 和 Fig. 7 中得到了直观展示：最初的候选帧集（自适应采样结果）已覆盖事件大致范围，但包含不少低相关帧；经过一至两轮 VLM 分析与 LDS 反馈后，帧集迅速集中到真正反映查询动作的时间段。此外，A.I.R. 在时序定位任务 Charades‑STA 上取得了远超通用 VideoLLM 的 mIoU（Table 8），进一步表明这种以查询为导向的迭代帧筛选能力并不局限于选择题式 QA，具有较好的任务泛化性。

## 方法谱系与知识库定位

A.I.R. 定位于视频问答中查询相关帧选择的训练无关（training‑free）方法谱系，其核心贡献在于用**迭代式 VLM 深度语义分析**替代以往要么只使用轻量相似度、要么一次性对所有帧使用 VLM 的做法。

### 与基线/后续工作的关系

**与纯轻量方法的对比**。传统的 Uniform Sampling 和 CLIP Top‑K 仅依赖单一 CLIP 相似度得分，在面对复杂查询时相似度得分无法可靠反映帧‑查询的相关性（Figure 1(b) 所揭示的核心瓶颈）。A.I.R. 并未抛弃 CLIP，而是将其降级为预处理步骤——提供初步相似度信号 S，供后续自适应采样使用；真正决定帧入选的判别由 VLM 推理完成（Sec. 3.1）。实验表明，A.I.R. 在同等 32 帧预算下，与 Uniform 基线相比在 Video‑MME、LongVideoBench、NextQA 上分别取得 +2.6、+4.5、+7.0 的绝对准确率提升（Table 1、Table 2、Table 4）。

**与基于 VLM 但未迭代优化的方法对比**。VideoTree 等方法虽然引入了 VLM 分析，但往往一次性分析大量帧（如 128 帧），导致高昂的计算开销；Frame‑Voyager 则需要微调，丧失了训练无关性。A.I.R. 通过迭代循环每轮仅对 C≈8–12 帧执行 VLM 分析，并配合提前停止和自适应预算 B（公式 (8)），使分析帧数远小于全帧规模（Table 6、Table 7）。在与同样训练无关的轻量方法（MDP3、BOLT、Q‑Frame 等）的横向对比中，A.I.R. 在多个基准上保持显著优势，且对不同的基础 VLM（QwenVL‑2.5 7B/32B/72B、InternVL3‑8B、GPT‑4o）均能稳定提升（Table 3、Table 1）。

**与 Agent 类方法的对比**。在后附的 Table 10 中也与 LLoVi、VideoAgent 等基于 VLM 智能体的帧选择方案进行了比较，A.I.R. 在训练无关的前提下表现出竞争性的精度，且计算效率更可控。

当前论文未出现明确标注为 A.I.R. 后续工作的文献，但该方法为未来更复杂的自适应采样策略（如结合多模态查询、多轮对话中的帧选择）提供了可堆叠的基础框架。

### 适用边界

**训练无关性的优势与代价**。A.I.R. 完全不需对 VLM 进行微调，因此可以即插即用于不同骨干模型，并易于继承预训练 VLM 的能力升级。其代价是，帧选择的全部“高级判别能力”来自于分析 VLM 在少量帧上的推理，而初筛阶段完全依赖 CLIP 相似度分布。若 CLIP 对某一查询的相似度排序存在系统性偏差（如特定领域视频与自然语言分布不一致），GMM 自适应阈值可能无法正确分离高相关事件，导致初始候选集质量不足，进而影响迭代阶段的效率。

**自适应阈值的分布假设**。GMM 自适应阈值 $T$（公式 (1)）假设相似度得分可被高低两个高斯簇区分。当实际相似度分布呈现单峰、多峰或严重偏斜时，阈值确定性降低。论文未在极端分布（如所有帧相似度都很低）下进行消融，该边界需在实际部署中留意。

**计数问题的薄弱性**。在细粒度题型分析中，A.I.R. 在“计算/计数”类问题上准确率仅 49.3%（Figure 4 相关报告），且该问题类型对所有方法都构成挑战。这表明当回答依赖于对多个帧内离散目标进行精确累加时，即使经过 VLM 推理的帧选择仍可能遗漏关键证据帧，是当前迭代选择逻辑的显式短板。

**对分析 VLM 推理质量的依赖**。若分析 VLM 对单帧的查询‑帧相关性判断存在幻觉（例如误认为某个无关场景的相关性高），局部密度采样（Localized Density Sampling）会在伪正帧周围扩大搜索，既增加计算又可能引入噪声。论文中的高置信度正帧是通过阈值 $\theta$ 筛选的（公式 (5)），但 $\theta$ 的设置受 VLM 输出分布影响，缺乏统一的鲁棒性分析。

**适用任务范式的限制**。论文仅验证了单轮 Video QA 和 Charades‑STA 上的时序定位迁移（Table 8），尚未涉及多轮问答、对话式视频理解等需要动态更新帧集的场景，这些情境下迭代过程的早期停止策略可能需要重新设计。

### 局限与开放问题

1. **CLIP 初筛的瓶颈突破**。目前 A.I.R. 的初始事件检测完全依赖 CLIP 相似度，当查询需要空间细粒度对象检测（如“第二个戴帽子的人”）时，CLIP 的全局相似度可能失灵。是否可以通过在预处理阶段引入轻量检测模型或文本‑区域对齐来增强初筛，是一个开放方向。

2. **自适应预算的更精细建模**。当前的预算 $B$ 仅与视频长度 $n$ 成正比并在 $V_\text{min}$ 与 $V_\text{max}$ 间夹断（公式 (8)），未利用查询复杂度或内容动态性。未来可探索将查询的推理难度或视频的视觉变化率纳入预算函数，进一步减少不必要分析。

3. **VLM 分析深度的自适应控制**。迭代循环的终止条件为达到预算 $B$，但未区分问题简单或困难。简单查询可能只需极少量 VLM 分析即可得出可靠帧集，而困难问题可能需要的分析帧数超过预算上限。能否让 VLM 自评估不确定性并动态调整分析深度，仍是未解问题。

4. **对长时依赖和跨事件推理的优化**。局部密度采样在已验证正帧的附近搜索，对邻近帧的覆盖良好，但如果正确答案需要从视频开头和结尾的不连续片段同时取证，迭代选择可能只收敛到其中一个事件周围。如何让框架具备主动搜索全局不连续关键帧的能力，值得进一步研究。

5. **多模态查询与多轮交互的扩展**。当前仅处理文本查询，未考虑以图像、音频片段作为查询条件的帧选择，也未涵盖连续对话中以先前上下文为条件的动态选择。在这些更开放的场景中，轻量预处理和迭代 VLM 分析的耦合方式将有显著变化。

6. **在线/流式视频应用**。A.I.R. 的预处理步骤（均匀采样并计算 CLIP 相似度）和迭代 VLM 分析均需先拥有全部帧（或至少已采样帧）的全局信息，不适用于实时流式输入的视频流。若要拓展至在线场景，需重新设计局部化的采样与反馈机制。

7. **大规模验证的缺失**。尽管在多个公开基准上表现稳健，但对超长视频（>1 小时）或低质量视频（摄像头噪声、监控）的测试仍然缺失，未来需要在该方向上补全实验证据以界定方法的通用边界。

## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/A.I.R._Enabling_Adaptive_Iterative_and_Reasoning-based_Frame_Selection_For_Video_Question_Answering.pdf

## 相关样本

- [[obsidian-vault/analysis/ICLR_2026/AdaReasoner_Dynamic_Tool_Orchestration_for_Iterative_Visual_Reasoning.md|AdaReasoner]]：同属视觉推理样本，可对照帧选择式迭代推理和多轮工具编排。

![[obsidian-vault/paperPDFs/ICLR_2026/A.I.R._Enabling_Adaptive_Iterative_and_Reasoning-based_Frame_Selection_For_Video_Question_Answering.pdf]]
