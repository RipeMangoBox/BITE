---
title: Rethinking Prompt Design for Inference-time Scaling in Text-to-Visual Generation
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Rethinking_Prompt_Design_for_Inference_time_Scaling_in_Text_to_Visual_Generation.pdf
project_link: "https://subin-kim-cv.github.io/PRIS"
code_link: "https://github.com/blackforest-labs/flux"
aliases:
- PPRITS
- RPDITSTVG
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过跨样本分析识别反复出现的语义元素失败模式，并自适应地修订提示词，以加强对未充分实现的元素的强调。
primary_logic: 提示词本身也是推理时缩放的关键维度，通过联合缩放提示与视觉，利用生成诊断信号指导后续样本朝向更高保真度，打破了仅扩展视觉搜索空间的局限。
claims:
- PRIS 在 GenAI-Bench 上获得 7% 的提升，在 VBench2.0 上获得 15% 的提升，显著优于固定提示的 Best-of-N。
- EFC 验证器在构建的基准上准确率达到 0.763，超越最强奖励模型 VideoAlign (0.693)。
- 迭代提示修订持续提升给定和未见过奖励的分数，而固定提示则饱和。
- 固定提示的 BoN 在 NFEs 增加时迅速饱和，而 PRIS 持续提升。
---

# Rethinking Prompt Design for Inference-time Scaling in Text-to-Visual Generation

> [!tip] 核心洞察
> 提示词本身也是推理时缩放的关键维度，通过联合缩放提示与视觉，利用生成诊断信号指导后续样本朝向更高保真度，打破了仅扩展视觉搜索空间的局限。

| 字段 | 内容 |
|------|------|
| 中文题名 | 文本到视觉生成中推理时缩放的提示重新设计 |
| 英文题名 | Rethinking Prompt Design for Inference-time Scaling in Text-to-Visual Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.03534) · [Project](https://subin-kim-cv.github.io/PRIS) · [Code](https://github.com/blackforest-labs/flux) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | PRIS (Prompt Redesign for Inference-time Scaling) |
| Dataset | GenAI-Bench, VBench2.0 Controllability & Creativity, VBench2.0 Commonsense & Physics |

> [!tip] 效果简介
> - GenAI-Bench (T2I) 上，VQA-Score (Given) 0.854 vs 0.783 (+0.071)；DA-Score w. BLIP2-VQA (Unseen) 0.707 vs 0.682 (+0.025)。
> - VBench2.0 Controllability & Creativity (T2V, Wan2.1-1.3B) 上，Average 65.45 (PRIS*) vs 57.73 (BoN*) (+7.72 (↑+13.88% relative))。
> - VBench2.0 Controllability & Creativity (T2V, Wan2.1-14B) 上，Average 68.85 (PRIS*) vs 58.51 (BoN*) (+10.34 (↑+15.19% relative))。

## 概要

**问题瓶颈**：在文本到视觉生成的推理阶段，现有方法主要通过增加采样步数或样本数量来扩展视觉计算（即“推理时缩放”）。然而，当提示词固定时，这种纯视觉缩放会迅速遭遇性能饱和——生成结果反复遗漏或错误实现提示中的某些语义元素，而单纯增加计算无法弥补提示本身的模糊或不完整性。这表明，提示词本身也是推理时缩放的关键维度，但长期被忽视。

**核心方法**：本文提出 **PRIS**（Prompt Redesign for Inference-time Scaling），一种在推理阶段自适应修订提示词的框架。PRIS 的核心洞察是：跨样本分析可以识别出反复出现的语义失败模式，通过针对性地修订提示词以加强对未充分实现元素的强调，从而打破固定提示下视觉搜索空间的局限。为实现细粒度的诊断反馈，作者设计了 **EFC**（Element-level Factual Correction）验证器，将提示分解为原子语义元素，并利用多模态大模型进行逐元素的文本-文本事实校正，以准确判断每个元素在生成视觉中的满足状态。

**主要结果**：在文本到图像（T2I）的 GenAI-Bench 上，PRIS 获得 **7%** 的提升；在文本到视频（T2V）的 VBench2.0 上，提升幅度达 **15%**，显著优于固定提示的 Best-of-N 基线。EFC 验证器在构建的基准上准确率达到 **0.763**，超越现有最强奖励模型。实验一致表明，固定提示的 BoN 在推理计算增加时迅速饱和，而 PRIS 通过联合缩放提示与视觉，持续提升生成质量，且增益可泛化至未见过的奖励指标。

**方法定位**：PRIS 属于**推理时提示优化**范式，与现有的视觉缩放方法（如 DAS、RBF、EvoSearch）正交，可以即插即用地集成到这些方法之上。与在生成前盲目扩展提示的标准做法不同，PRIS 利用生成过程中的诊断信号进行数据驱动的针对性修订。与基于学习的单样本修正方法（如 ReflectionFlow）相比，PRIS 无需训练，且通过跨样本共同失败模式进行修订，效果更优。



文本到视觉生成（Text-to-Visual Generation）近年来取得了显著进展，但在面对包含多对象、多属性、空间关系与动作时序的复杂提示时，生成结果仍然频繁出现语义遗漏或错位。为提升生成质量，推理时缩放（Inference-time Scaling）已成为一条重要路径，其核心思想是在推理阶段增加计算资源——例如生成更多候选样本（Best-of-N，BoN）、修改采样路径（**DAS** ）、调整噪声注入（**RBF** ）或在采样空间中搜索（**EvoSearch**）——以期从更大的视觉搜索空间中选出更优结果。

然而，现有推理时缩放方法存在一个被忽视的瓶颈：**提示词本身被固定不变**。当仅扩展视觉搜索而保持提示静态时，系统反复生成的样本往往共享相同的失败模式——模型对提示中某些语义元素始终无法正确实现，而单纯增加样本数或调整噪声并不能弥补提示本身的模糊或不完整性。如 Figure 1 所示，固定提示下的 BoN 在推理计算（NFEs）增加后迅速饱和，尤其在未见过的奖励模型（unseen rewards）上表现停滞，说明仅扩展视觉维度无法突破提示-视觉对齐的性能上限。

这一现象的深层原因在于：许多生成错误并非源于视觉搜索不足，而是**提示词未能提供足够清晰或充分的语义约束**。当用户提供的原始提示存在模糊表述、隐含假设或信息缺失时，生成模型即使拥有强大的视觉先验，也难以准确推断意图。现有应对方式包括在生成前进行标准提示扩展（Standard Prompt Expansion），但这种“盲目”扩展缺乏对实际生成失败的诊断反馈，往往无法针对性地修正问题。

针对上述缺口，本文提出**PRIS（Prompt Redesign for Inference-time Scaling）**，其核心动机是：**提示词本身应被视为推理时缩放的另一个关键维度**。PRIS 通过跨样本分析识别反复出现的语义元素失败模式，并自适应地修订提示词，以加强对未充分实现元素的强调，同时保留用户原始意图。这一联合缩放策略打破了仅扩展视觉搜索空间的局限，利用生成诊断信号指导后续样本朝向更高保真度。为支撑这一框架，作者还设计了**EFC（Element-level Factual Correction）**——一种细粒度文本-文本验证器，将提示分解为原子语义元素并进行逐项自然语言推理验证，为提示修订提供可解释的诊断依据。

实验表明，PRIS 在 GenAI-Bench 上相较固定提示 BoN 提升 7%，在 VBench2.0 上提升 15%，且迭代提示修订在给定和未见过奖励上均持续带来增益，而固定提示则饱和。这一结果验证了“联合缩放提示与视觉”这一核心洞察的有效性。



## 核心方法与创新机理

### 瓶颈诊断：固定提示导致推理时视觉扩展的早期饱和

现有文本到视觉生成的推理时缩放方法（如 **Best-of-N**、**DAS** (Chen et al., 2024)、**RBF** (Liu et al., 2024)）均将计算资源集中于扩展视觉搜索空间——增加采样步数、修改噪声路径或搜索采样空间——但始终保持提示词固定不变。PRIS 揭示了一个被忽视的根本瓶颈：**许多生成错误并非源于视觉搜索不足，而是源于提示词本身的模糊性或不完整性**。当固定提示中存在语义歧义或缺失关键约束时，仅扩展视觉计算会导致生成结果反复出现相同的失败模式，性能迅速饱和（Figure 1 中橙色曲线），且这种饱和在未见过的奖励函数上尤为严重。

### 核心洞察：提示词本身是推理时缩放的关键维度

PRIS 的核心创新在于将**提示词设计**提升为推理时缩放的一个独立且可优化的维度，打破了“提示固定、仅扩展视觉”的范式。其关键因果机制是：通过跨样本分析识别反复出现的语义元素失败模式，利用这些诊断信号自适应地修订提示词，从而引导后续生成朝向更高保真度的方向。这一设计使得推理计算不再仅用于“搜索更好的视觉输出”，而是同时用于“搜索更好的任务描述”，二者形成正向反馈循环。

### 方法谱系与知识库定位

PRIS 在推理时缩放方法谱系中开辟了“提示-视觉联合缩放”这一新分支：

| 缩放维度 | 代表方法 | 机制 | 局限 |
|---------|---------|------|------|
| 仅视觉（采样） | **Best-of-N** (BoN) | 固定提示，生成 N 个样本后选择最优 | 早期饱和，无法修正提示缺陷 |
| 仅视觉（噪声） | **DAS**, **RBF** | 改变采样路径或噪声分布 | 仍受限于固定提示的语义约束 |
| 仅视觉（搜索） | **EvoSearch** | 在采样空间中进化搜索 | 计算开销大，未见奖励泛化差 |
| 提示扩展（盲目） | Standard Prompt Expansion | 生成前用 LLM 盲目扩展提示 | 无诊断反馈，可能引入噪声 |
| 单样本修正 | **ReflectionFlow** (Liu et al., 2024) | 基于学习模型对单样本进行修正 | 依赖训练，无法利用跨样本失败模式 |
| **提示-视觉联合** | **PRIS** (本文) | 跨样本诊断→提示修订→重新生成 | 需要验证器，首次修订已获主要增益 |

PRIS 与上述方法的本质区别在于其**反馈驱动的闭环设计**：它不是一次性的提示扩展，而是基于生成结果的实证诊断进行针对性修订。这一思想与 LLM 推理中的 self-refine 和 multi-step reasoning 有家族相似性，但将其首次系统性地引入视觉生成领域，并证明了提示修订的收益可迁移至未见过的奖励函数（Table 3）。

### 关键 Changed Slots

PRIS 相对于固定提示推理时缩放基线，在三个关键设计槽位上做出了根本性改变：

**Slot 1: 推理阶段的提示设计策略**

- **Baseline**: 生成过程中保持提示固定（使用原始提示或标准盲目扩展）
- **PRIS**: 根据跨样本的反复失败模式自适应修订提示，强化未满足的语义元素
- **机制**: 先以固定提示生成 $M = \lfloor N/2 \rfloor$ 个候选样本，通过 EFC 验证器识别哪些原子语义元素在多个样本中反复失败，然后针对这些共同失败修订提示，再用修订提示和 $k = \lceil N/4 \rceil$ 个最佳种子生成剩余样本
- **证据**: Table 6 消融表明，基于共同失败的修订（Common-failure）始终优于基于单样本的修订（Per-sample）和标准提示扩展；Figure 1 显示固定提示在 NFEs 增加时迅速饱和，而 PRIS 持续提升

**Slot 2: 文本-视觉对齐验证器**

- **Baseline**: 整体标量奖励模型（如 VQA-Score、VideoAlign），输出单一分数，无法定位具体失败
- **PRIS**: **EFC (Element-level Factual Correction)**，将提示分解为原子语义元素 $p = \{p_1, p_2, \dots, p_s\}$，对每个元素进行文本-文本自然语言推理（NLI）验证，输出细粒度的蕴含/矛盾/中性判断
- **机制**: EFC 先利用 MLLM 从生成的视觉中提取描述性标注，然后将每个提示元素与该标注进行事实校正比对，避免了直接 QA 带来的偏差
- **证据**: Table 5 显示 EFC 在选择真实视觉输出的准确率达到 0.763，超越最强学习型奖励模型 VideoAlign (0.693) 和分解式二值 VQA (0.700)；Table 9 进一步提供了逐类准确性验证

**Slot 3: 缩放维度**

- **Baseline**: 仅扩展视觉（增加采样步数/样本数），计算资源完全投入视觉搜索
- **PRIS**: 联合扩展提示与视觉，将部分计算预算用于生成诊断反馈和提示修订，利用诊断信号指导后续视觉生成
- **机制**: 通过“生成-验证-诊断-修订-再生成”的闭环，使提示和视觉在推理过程中协同进化
- **证据**: Table 7 在匹配计算开销下，PRIS 在 T2I 和 T2V 上均优于 BoN；Table 4 显示 PRIS 可与 DAS、RBF、EvoSearch 等视觉缩放方法正交集成，进一步提升性能

### 设计哲学：从“搜索答案”到“修正问题”

PRIS 的深层设计哲学可概括为：**当模型反复失败时，与其在固定的问题空间中搜索更好的答案，不如利用失败信号修正问题本身**。这一思想的具体实现依赖于两个关键设计选择：(1) 使用跨样本共同失败而非单样本失败来驱动修订，因为共同失败更可能反映提示的系统性缺陷而非随机波动；(2) 使用文本-文本验证而非文本-视觉直接评分，因为前者更细粒度、更可解释，且避免了视觉评分中的过优化问题。Figure 10 显示，RBF 单独使用时因奖励过优化导致提示文字直接渲染在图像上，而与 PRIS 集成后显著缓解了此类伪影，进一步验证了这一设计哲学的有效性。



PRIS（Prompt Redesign for Inference-time Scaling）的核心思想是：在推理时扩展视觉生成计算的过程中，**提示词本身也是一个关键的缩放维度**。仅靠增加采样数量（Best-of-N）或改变采样路径（如 DAS、RBF 等视觉缩放方法）而保持提示词固定，会在早期遭遇性能饱和——因为许多生成错误源于提示词本身的模糊或不完整，而非视觉搜索空间不足。PRIS 通过联合缩放提示与视觉，利用跨样本的生成诊断信号来指导后续生成，打破了这一瓶颈。

### 框架总览

PRIS 的整体框架由两个核心模块构成：**EFC 验证器**和**PRIS 提示重设计循环**。EFC 负责提供细粒度的文本-视觉对齐诊断信号，PRIS 循环则利用这些信号识别反复出现的失败模式并自适应修订提示词。Figure 2 展示了这一框架的完整流程。

![[assets/figures/papers/paper_list_l2341_https_arxiv_org_abs_2512_03534/figures/002_Figure_2.jpg]]
*Figure 2: Overview of Prompt Redesign for Inference-time Scaling (PRIS), which leverages diagnostic feedback from our verifier EFC to revise prompts during inference based on generated visuals. EFC decomposes prompts into semantic elements and verifies each element for fine-grained text-visual alignment (left). Guided by the EFC, PRIS proceeds as follows (right): Step 1 reviews initial generations with EFC; Step 2 selects top-k successful samples and identifies recurring failures; Step 3 redesigns the prompt to emphasize common failures; and Step 4 regenerates visuals with the revised prompt and top-k seeds. The process can be iterated by returning from Step 4 to Step 2*

#### 模块一：EFC（Element-level Factual Correction）验证器

EFC 是一个基于多模态大模型的细粒度验证器，其核心创新在于将提示遵循验证从“整体打分”转变为“逐元素事实校正”。具体流程为：

1. **提示分解**：将原始提示 $p$ 分解为一组可验证的原子语义元素集合 $p = \{ p_{1}, p_{2}, \dots, p_{s} \}$，并将每个元素分类为核心（core）或额外（extra）。
2. **视觉描述生成**：从生成的视觉内容中提取描述性字幕。
3. **逐元素 NLI 验证**：对每个语义元素，通过自然语言推理（NLI）将其与视觉字幕进行文本-文本比对，分类为蕴含（entailment）、中性（neutral）或矛盾（contradiction）。对于初始标记为中性的元素（因字幕中缺失相关提及），EFC 会进行二次评估以区分蕴含与矛盾。

这种设计避免了对视觉内容的直接 QA，转而采用更可靠的文本-文本验证策略。在构建的基准上，EFC 的准确率达到 **0.763**，显著超越最强学习型奖励模型 VideoAlign（0.693）以及分解式二值 VQA（0.700）（Table 5）。

#### 模块二：PRIS 提示重设计循环

PRIS 循环包含四个步骤，形成一个从生成诊断到提示修订再到重新生成的闭环：

- **Step 1 — 生成与验证**：使用原始提示（或标准扩展提示）生成 $M = \lfloor N / 2 \rfloor$ 个候选视觉样本，并通过 EFC 评估每个样本对提示语义元素的满足情况。
- **Step 2 — 选择与诊断**：根据 EFC 评分选择得分最高的 $k = \lceil N / 4 \rceil$ 个成功样本作为种子，同时跨样本识别**反复出现的共同失败模式**（common failures）——即那些在多个生成样本中均未得到满足的语义元素。
- **Step 3 — 提示修订**：基于识别的共同失败，自适应修订提示词，强化对未充分实现元素的强调，同时保持用户原始意图不变。修订后的提示词会生成两个变体以供后续使用。
- **Step 4 — 重新生成**：使用修订后的提示词和 top-k 种子重新生成剩余的视觉样本。

该过程可以迭代执行：从 Step 4 返回 Step 2，利用新生成的样本再次进行诊断和修订。实验表明，首次迭代已获得主要增益，但第二次迭代仍可带来持续改进（Table 3）。

### 输入输出流

- **输入**：用户提供的文本提示词，以及推理时的总生成样本数 $N$。
- **中间产物**：EFC 分解的原子语义元素、每个样本的逐元素验证结果、跨样本的共同失败模式、修订后的提示词。
- **输出**：经过提示修订和重新生成后的最终视觉样本（图像或视频）。

### 与视觉缩放方法的协同

PRIS 的提示修订策略与现有的视觉缩放方法（如 DAS、RBF、EvoSearch、SMC）是**正交且可叠加的**。在集成实验中，PRIS 不仅自身带来提升，还能有效缓解视觉缩放方法的一些固有问题——例如 RBF 单独使用时因奖励过度优化导致提示文字直接渲染在图像上的伪影，在与 PRIS 结合后得到显著缓解（Figure 10）。这进一步验证了“提示-视觉联合缩放”这一核心洞察的有效性。



PRIS 框架由两个核心模块构成：**EFC（Element-level Factual Correction）验证器**和**PRIS 提示重设计循环**。EFC 提供细粒度的文本-视觉对齐诊断信号，PRIS 则利用该信号识别跨样本的反复失败模式并自适应修订提示，从而在推理时联合缩放提示与视觉。

### EFC：元素级事实校正验证器

EFC 的核心设计是将整体提示对齐评估转化为一组原子语义元素的逐项验证。给定原始提示 $p$，EFC 首先将其分解为一组可验证的原子语义元素：

$$p = \{ p_{1}, p_{2}, \dots, p_{s} \}$$

其中每个 $p_i$ 被进一步分类为 **core**（核心）或 **extra**（额外）元素。这一分解使得验证粒度从整体标量评分细化为逐元素的对齐判断，从而能够精确定位生成结果中哪些语义元素未被满足。

EFC 的验证流程（Figure 2a, Figure 9）分为三步：
1. **生成描述**：从生成的视觉内容中提取文本描述（caption）。
2. **事实校正**：对每个原子元素 $p_i$，在文本层面与生成的描述进行自然语言推理（NLI），将其分类为 **entailment**（蕴含）、**neutral**（中性）或 **contradiction**（矛盾）。
3. **重评估**：对于初始被标记为 neutral 的元素（因描述中未提及），EFC 进行二次判断，以区分真正的 entailment 与 contradiction，避免直接 QA 方式带来的误判。

![[assets/figures/papers/paper_list_l2341_https_arxiv_org_abs_2512_03534/figures/018_Figure_9.jpg]]
*Figure 9: Illustration of EFC. The figure illustrates how EFC provides fine-grained, interpretable verification of prompt adherence. It first decomposes the prompt into semantic elements, then generates captions from the visuals, and applies factual correction to classify each element as entailment, neutral, or contradiction. Elements initially labeled neutral (due to missing mentions in the caption) are reevaluated to decide between entailment and contradiction. This design avoids direct QA, leading to more accurate verification*

EFC 基于预训练多模态大模型 Qwen2.5-VL 实现，无需额外训练。在构建的验证基准上，EFC 的准确率达到 **0.763**，显著优于最强的学习型奖励模型 VideoAlign（0.693）和分解式二值 VQA 方法（0.700），验证了文本-文本 NLI 策略在细粒度对齐判断上的优势（Table 5, Table 9）。

### PRIS 提示重设计循环

PRIS 循环（Figure 2b）包含四个步骤，在推理时利用 EFC 的诊断反馈指导提示修订：

**Step 1 — 生成与验证**：首先生成 $M$ 个候选视觉样本，使用 EFC 评估每个样本对各原子元素的满足情况。

**Step 2 — 选择与诊断**：从 $M$ 个样本中选出 top-$k$ 个最佳样本，同时识别在多个样本中反复出现的失败元素（common failures），即那些在多数候选样本中均未被正确实现的语义元素。

**Step 3 — 提示修订**：针对识别出的共同失败模式，自适应地修订提示，强化对未充分实现元素的强调，同时保持用户的原始意图不变。修订策略是**跨样本**的，而非针对单个样本的修正。

**Step 4 — 重新生成**：使用修订后的提示和 top-$k$ 种子的变体重新生成视觉内容。

该循环可迭代执行：从 Step 4 返回 Step 2，基于新生成的样本再次识别失败模式并进一步修订提示。

在推理计算分配上，PRIS 将总样本数 $N$ 分为两部分：

$$M = \lfloor N / 2 \rfloor, \quad k = \lceil N / 4 \rceil$$

即首先生成一半样本用于审查诊断，取其中四分之一作为最佳种子，用于生成修订提示的两个变体各 $k$ 个样本，总计仍为 $N$ 个样本。这一分配策略在匹配计算开销下确保了 PRIS 相对于固定提示 BoN 的公平比较。



## 实验与关键发现

### 核心实验设置

PRIS 的推理管线将总计算预算 $N$ 个样本分为两阶段：首先生成 $M = \lfloor N / 2 \rfloor$ 个候选视觉样本，经 EFC 验证后选取 $k = \lceil N / 4 \rceil$ 个最佳种子，基于识别出的共同失败模式修订提示，再生成剩余样本。EFC 验证器以 Qwen2.5-VL 为基础，无需额外微调。T2I 实验采用 FLUX.1-dev，T2V 实验采用 Wan2.1-1.3B（小模型，$N=20$）和 Wan2.1-14B（大模型，$N=10$）。带 * 标记的结果表示初始生成使用了标准提示扩展。

### 主实验结果

#### 文本到图像生成（GenAI-Bench）

Table 1 汇总了 T2I 任务的量化对比。PRIS 在给定奖励（VQA-Score）上达到 **0.854**，较固定提示 BoN 的 0.783 提升 **+0.071**（相对提升约 7%）。在未见奖励（DA-Score w. BLIP2-VQA）上，PRIS 为 0.707，BoN 为 0.682，提升 +0.025。值得注意的是，PRIS 在美学质量（Aesthetic Quality）上同样保持竞争力（5.765 vs. BoN 的 5.719），表明提示修订未损害视觉保真度。

![[assets/figures/papers/paper_list_l2341_https_arxiv_org_abs_2512_03534/figures/004_Table_1.jpg]]
*Table 1: Quantitative results of T2I on GenAI-Bench. ∗ denotes results with standard prompt expansion; BoN refers to “Best-of-N” selection using fixed prompts. Bold shows the best*

标准提示扩展（*）本身已带来一定增益（BoN* 的 VQA-Score 为 0.837），但 PRIS* 在此基础上进一步提升至 0.853，验证了自适应修订相比盲目扩展的优越性。

#### 文本到视频生成（VBench2.0）

Table 2 展示了 T2V 任务的结果，分为“可控性与创造性”和“常识与物理”两个维度。在可控性与创造性上，PRIS* 在 Wan2.1-1.3B 上达到 **65.45**（BoN* 为 57.73），相对提升 **+13.88%**；在 Wan2.1-14B 上达到 **68.85**（BoN* 为 58.51），相对提升 **+15.19%**。在常识与物理维度上，PRIS* 同样在两个模型规模上分别取得 +3.46 和 +3.84 的增益。

![[assets/figures/papers/paper_list_l2341_https_arxiv_org_abs_2512_03534/figures/005_Table_2.jpg]]
*Table 2: Quantitative comparisons of T2V generation on VBench-2.0. ∗ denotes results obtained using the standard prompt expansion, and bold indicates the best results. We use N = 20 samples for Wan2.1-1.3B (small) and N = 10 for Wan2.1-14B (large), which can lead to the smaller model achieving higher scores due to the larger number of samples. BoN refers to “Best-of-N” selection using fixed prompts*

定性结果（Figure 4）进一步印证了 PRIS 在时序因果关系上的修正能力：例如，修订后的提示明确强调“灯在触摸时立即亮起”，从而纠正了原始生成中时序错乱的问题。

![[assets/figures/papers/paper_list_l2341_https_arxiv_org_abs_2512_03534/figures/006_Figure_4.jpg]]
*Figure 4: Qualitative comparisons on T2V generation. Our revised prompt elaborates on previous failures by emphasizing causal order, ensuring the lamp turns on immediately when touched*

### 推理时缩放行为

Figure 1 和 Table 3 共同揭示了 PRIS 的核心缩放特性。固定提示的 BoN 随推理计算量（NFEs）增加迅速饱和，尤其对于未见奖励几乎不再增长。而 PRIS 通过迭代提示修订持续提升分数：Table 3 显示，经过两次迭代修订，给定和未见奖励均保持上升趋势，且增益可泛化至未见奖励。Figure 5 的定性示例表明，随着计算量增加，PRIS 生成的树逐渐变高同时满足所有属性要求，而 BoN 始终遗漏部分元素。

![[assets/figures/papers/paper_list_l2341_https_arxiv_org_abs_2512_03534/figures/001_Figure_1.jpg]]
*Figure 1: Our prompt redesign scales with compute, while fixed-prompts plateau. Given a user-provided complex text prompt, scaling visuals alone with a fixed prompt at inference time often leads to early performance plateaus, especially for unseen rewards (see orange line and boxes). It also repeatedly produces outputs that exhibit common failures and cover only parts of the prompt, even as compute increases to sample more visuals. In contrast, scaling visuals alongside our redesigned prompts yields progressively improved generations and substantially higher prompt-adherence scores as compute increases for both given and unseen rewards (see blue line and boxes)*

![[assets/figures/papers/paper_list_l2341_https_arxiv_org_abs_2512_03534/figures/008_Table_3.jpg]]
*Table 3: Quantitative results for iterative prompt refinement with increasing inference-time compute. Iteratively revision prompts consistently improves reward scores by addressing common failures, and the gains even generalize to unseen rewards. In contrast, fixed prompts often saturate and fail to transfer*

![[assets/figures/papers/paper_list_l2341_https_arxiv_org_abs_2512_03534/figures/007_Figure_5.jpg]]
*Figure 5: Qualitative examples with increasing inference-time compute. PRIS generates progressively taller trees while satisfying all attributes, whereas BoN consistently misses some*

### 消融研究

#### 提示修订策略对比（Table 6）

![[assets/figures/papers/paper_list_l2341_https_arxiv_org_abs_2512_03534/figures/013_Table_6.jpg]]
*Table 6: Ablation study of PRIS. # d.e. and #*

Table 6 对比了三种修订策略：“共同失败”（Common-failure）基于跨样本反复出现的失败元素进行修订；“单样本”（Per-sample）仅基于单个最佳样本的失败修订；“奖励模型”使用整体奖励分数指导修订。结果表明，基于共同失败的修订始终优于其他两种策略，验证了跨样本诊断信号的核心价值。

#### 验证器准确性（Table 5, Table 9）

![[assets/figures/papers/paper_list_l2341_https_arxiv_org_abs_2512_03534/figures/009_Table_5.jpg]]
*Table 5: Quantitative results on verifier accuracy in selecting GT visual outputs. Bold indicates the best results*

EFC 在作者构建的验证基准上达到 **0.763** 的准确率，显著超越最强学习型奖励模型 VideoAlign（0.693）和分解式二值 VQA（0.700）。Table 9 进一步展示了 EFC 在不同提示类别上的逐类准确性，表明文本-文本验证策略在细粒度对齐判断上具有稳定优势。

#### 计算开销匹配（Table 7）

![[assets/figures/papers/paper_list_l2341_https_arxiv_org_abs_2512_03534/figures/012_Table_7.jpg]]
*Table 7: Quantitative evaluation with matched compute*

在匹配计算开销的条件下，PRIS 在 T2I 和 T2V 上均优于 BoN，排除了“增益仅来自更多计算”的替代解释。

### 与视觉缩放方法的集成

PRIS 作为提示维度的缩放方法，可与现有视觉缩放方法正交集成。Table 4 显示，将 PRIS 与 DAS、RBF、EvoSearch 等噪声/采样空间缩放方法结合，在 GenAI-Bench 上均取得进一步提升。值得注意的是，RBF 单独使用时易因奖励过优化导致提示文字直接渲染在图像上的伪影，而集成 PRIS 后显著缓解了此问题（Figure 10）。EvoSearch 在 T2V 任务上单独使用时无法泛化至未见奖励，集成 PRIS 后性能得到改善（Table 8）。

![[assets/figures/papers/paper_list_l2341_https_arxiv_org_abs_2512_03534/figures/011_Table_4.jpg]]
*Table 4: Quantitative results of integrating PRIS with T2I visual scaling methods on GenAI-Bench. BoN refers to “Best-of-N” selection using fixed prompts. Bold shows the best*

### 失败模式与局限性

尽管 PRIS 在多数指标上表现优异，论文也报告了若干边界情况。奖励模型可能对特定数值过度拟合，导致热力学类别性能略有下降。EFC 的单次验证时间约为图像生成的 3 倍、视频生成的 1 倍，未进行任务特定微调以降低延迟。此外，PRIS 的有效性依赖于基础生成模型具备一定程度的提示遵循能力——对于几乎无法执行指令的模型，提示修订无法发挥作用。提示修订的跨模型可迁移性目前仅在单模型上初步验证（Figure 15），系统性的多模型泛化评估仍为开放问题。



## 定位与知识库关联

### 推理时缩放范式的重新定义

PRIS 在推理时缩放（Inference-time Scaling）这一新兴范式中占据了一个独特且具有范式转换意义的位置。现有推理时缩放方法几乎全部聚焦于**视觉维度的扩展**，包括改变采样路径的 **DAS** 、修改噪声的 **RBF** 、以及搜索采样空间的 **EvoSearch** 等。这些方法的核心假设是：通过增加推理阶段的计算量来探索更大的视觉生成空间，可以找到更优的生成结果。然而，PRIS 揭示了一个被忽视的关键瓶颈——**固定提示词本身构成了性能上限**。当提示词模糊或不完整时，仅扩展视觉搜索空间无法弥补语义层面的根本缺陷，导致性能快速饱和（见 Figure 1 中固定提示的橙色曲线）。

PRIS 的核心突破在于将**提示词本身作为推理时缩放的另一个关键维度**，实现了提示与视觉的联合缩放。这一设计打破了现有方法仅将推理时计算用于视觉搜索的局限，转而利用生成过程中的诊断信号（通过 EFC 验证器获取）来指导提示词的适应性修订，从而引导后续生成朝向更高保真度。从方法谱系来看，PRIS 并非替代现有视觉缩放方法，而是作为**正交的增强层**与之集成——实验证明 PRIS 可以与 DAS、RBF、EvoSearch 等方法协同工作，进一步提升其性能（Table 4）。

### 与基线方法的关系定位

**Best-of-N (BoN)** 是推理时缩放的最朴素形式，通过生成 N 个候选并选择奖励最高的样本来利用额外计算。PRIS 可被视为 BoN 的**语义增强版本**：BoN 仅进行被动选择，而 PRIS 在生成过程中主动诊断并修正提示词，使后续生成具有更强的语义针对性。在匹配计算开销下，PRIS 始终优于 BoN（Table 7），且 BoN 在 NFE 增加时迅速饱和，而 PRIS 持续提升（Figure 1）。

**Standard Prompt Expansion** 在生成前盲目扩展提示词，缺乏对生成结果的反馈闭环。PRIS 的提示修订是**反馈驱动的自适应过程**，基于跨样本的反复失败模式进行针对性强化。消融实验（Table 6）证实，基于共同失败的修订（Common-failure）始终优于基于单个样本的修订（Per-sample）和标准提示扩展，验证了跨样本诊断的必要性。

**ReflectionFlow** 代表了基于学习模型的单样本修正方法，需要额外训练。PRIS 在无需训练的情况下显著优于 ReflectionFlow（Figure 14），表明利用跨样本共享失败模式的提示修正策略比学习得到的单样本修正更有效。这一对比凸显了 PRIS 的核心洞察：**反复出现的失败模式携带了比单样本错误更丰富的诊断信息**。

### 适用边界与依赖条件

PRIS 的有效性建立在以下前提之上：

1. **基础生成模型需具备基本的提示遵循能力**。论文明确指出，对于几乎无法执行指令的模型，提示重设计无法发挥作用。这一限制在 Table 10 中得到了间接体现——作者排除了提示遵循度过差的 T2V 模型。

2. **EFC 验证器的准确性是系统性能的上限**。EFC 在构建的基准上达到 0.763 的准确率，超越最强学习型奖励模型 VideoAlign (0.693)，但其基于预训练 MLLM（Qwen2.5-VL）的文本-文本验证策略仍存在误判可能。验证器的单次验证时间约为图像生成的 3 倍、视频生成的 1 倍，构成了计算开销的主要来源。

3. **提示修订的可迁移性尚未系统验证**。虽然 Figure 15 展示了 Flux1.dev 修订的提示可迁移至 Firefly Image 4 Ultra 的孤立案例，但跨模型、跨架构的泛化稳定性仍是一个开放问题。

### 局限性与开放问题

**验证器效率与偏见**：EFC 未针对任务进行微调，推理延迟显著。此外，论文未评估 EFC 在不同数据分布下的偏见问题，这可能导致对特定语义元素的系统性误判。

**迭代次数的饱和点**：实验观察到两次迭代修订仍可带来增益（Table 3），但未探索饱和边界。首次修订已获得主要增益，后续迭代的边际收益递减规律尚不明确。

**奖励过度拟合**：论文注意到奖励模型可能过度拟合特定数值，导致热力学类别性能略微下降。这一现象暗示基于奖励的评估框架本身可能引入系统性偏差。

**训练型扩展的可能性**：论文提出的一个关键开放问题是：是否可以通过在原始简短提示与基于失败的修订提示对上微调 LLM，来降低验证开销并实现离线高质量提示生成？这将使 PRIS 从推理时方法演进为训练型方法。

**跨模态推广**：共同失败识别与针对性提示修订的思想是否能推广到其他模态和任务（如文本到音频、文本到代码），挑战现有的推理时缩放定律，是一个值得探索的方向。



## 原文 PDF

![[paperPDFs/CVPR_2026/Rethinking_Prompt_Design_for_Inference_time_Scaling_in_Text_to_Visual_Generation.pdf]]
