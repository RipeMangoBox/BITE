---
title: "ReaGEN: Adaptive Generation of Structured Chains-of-Thought for Efficient Multimodal Reasoning"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/ReaGEN_Adaptive_Generation_of_Structured_Chains_of_Thought_for_Efficient_Multimodal_Reasoning.pdf
project_link: null
code_link: "https://github.com/AISmartPerception/ReaGEN"
aliases:
- ReaGEN
tags:
- CVPR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 利用推理过程中跨阶段注意力流，量化各阶段对最终答案的直接与间接贡献（Stage Importance），以此作为抑制低效阶段、增强关键阶段的因果信号，指导思维链结构的优化。
primary_logic: 将思维链结构（阶段序列）视为可学习的对象，通过教师引导的进化搜索自动发现每道问题的最优思维链，并训练一个轻量级生成器（GEN）根据注意力信号预测样本自适应的思维链，从而在推理时以单路径效率获得多路径搜索的灵活性，无需微调基座VLM。
claims:
- ReaGEN在多个多模态推理基准上相对测试时缩放方法VReST最高提升26个绝对准确率百分点。
- ReaGEN将推理时平均token使用量降低79%（相对VReST），相当于减少4倍token消耗。
- 移除注意力衍生信号后，所有基准上的性能一致下降，证明注意力引导对有效阶段选择至关重要。
- ReaGEN通过迭代调用GEN进一步优化思维链，在MMMU-Pro 10选任务上迭代3次达到51.90%，超越单次预测。
---

# ReaGEN: Adaptive Generation of Structured Chains-of-Thought for Efficient Multimodal Reasoning

> [!tip] 核心洞察
> 将思维链结构（阶段序列）视为可学习的对象，通过教师引导的进化搜索自动发现每道问题的最优思维链，并训练一个轻量级生成器（GEN）根据注意力信号预测样本自适应的思维链，从而在推理时以单路径效率获得多路径搜索的灵活性，无需微调基座VLM。

| 字段 | 内容 |
|------|------|
| 中文题名 | ReaGEN：面向高效多模态推理的结构化思维链自适应生成 |
| 英文题名 | ReaGEN: Adaptive Generation of Structured Chains-of-Thought for Efficient Multimodal Reasoning |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Tian_ReaGEN_Adaptive_Generation_of_Structured_Chains-of-Thought_for_Efficient_Multimodal_Reasoning_CVPR_2026_paper.html) · [Code](https://github.com/AISmartPerception/ReaGEN) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | ReaGEN |
| Dataset | MMMU-Pro, VStar, MMStar, MMU-Pro |

> [!tip] 效果简介
> - MMMU-Pro (4-options) 上，Accuracy (%) 64.51 (ReaGEN 4 iter, frozen Qwen3-VL-4B) vs VReST (same student) (not extracted)。
> - VStar 上，Accuracy (%) 84.49 (ReaGEN 4 iter, frozen Qwen3-VL-4B) vs VReST (same student) (not extracted)。
> - MMStar 上，Accuracy (%) 75.77 (ReaGEN 4 iter, frozen Qwen3-VL-4B) vs VReST (not extracted)。

## 概要

当前大型视觉语言模型（LVLM）在复杂多模态推理任务中面临一个关键瓶颈：直接回答的方式难以可靠地引出结构化、多步骤的推理过程。现有的推理时缩放方法（如树搜索 **VReST**（Zhang et al., 2025）和 **Socratic-MCTS**（Acuna et al., 2025））虽然通过多路径探索提高了鲁棒性，但代价是推理延迟和token消耗急剧上升；而训练后微调方法（如 **VisualCoT** / **LLaVA-CoT**（Shao et al., 2024 / Xu et al., 2025））则依赖大规模高质量思维链语料，且不易跨模型迁移。

ReaGEN 的核心洞察在于：将思维链结构本身视为可学习的对象。该方法利用推理过程中跨阶段注意力流，量化各阶段对最终答案的直接与间接贡献（Stage Importance），以此作为抑制低效阶段、增强关键阶段的因果信号。通过教师引导的进化搜索，ReaGEN 自动发现每道问题的最优思维链结构，并训练一个仅18.3M参数的轻量级生成器（GEN），使其能根据注意力信号预测样本自适应的思维链。推理时，GEN 以单路径效率获得多路径搜索的灵活性，且无需对基座VLM进行任何微调。

实验结果表明，ReaGEN 在多个多模态推理基准上相较测试时缩放方法最高提升26个绝对准确率百分点，同时将推理时平均token使用量降低79%（相当于4倍token消耗缩减），VLM调用次数平均减少53%。在MMMU-Pro 10选任务上，通过迭代调用GEN进一步优化思维链，3次迭代即可达到51.90%的准确率，超越单次预测。消融实验证实，移除注意力衍生信号后所有基准性能一致下降，验证了注意力引导对有效阶段选择的关键作用。ReaGEN 在视觉为主的任务（VStar、MMStar）上恢复了教师搜索的大部分性能，且在数学中心数据集上训练的GEN能有效泛化到视觉基准，展现出良好的跨领域迁移能力。

### 问题背景

当前大型视觉语言模型（LVLM）在需要多步骤视觉推理的任务中面临一个核心矛盾：直接生成最终答案的方式难以可靠地引出结构化、多步骤的推理过程，模型往往跳过关键的中间推理环节，导致在复杂多模态基准上的表现不佳。与此同时，增强推理能力的现有方法在两个方向上各有代价：

- **测试时缩放方法**（如树搜索、多路径采样）通过在推理阶段探索多条推理路径来提高鲁棒性。代表性工作包括 **VReST**（Zhang et al., 2025）和 **Socratic-MCTS**（Acuna et al., 2025），它们分别利用树搜索结合自我奖励机制、以及迭代提问与蒙特卡洛树搜索来探索视觉推理路径。然而，这些方法需要数十次调用基座VLM，导致推理延迟和token成本大幅增加。
- **训练后微调方法**（如 **VisualCoT** / **LLaVA-CoT**）通过在人工构建的思维链（CoT）数据集上微调VLM来注入推理能力。这类方法需要大规模高质量的思维链语料，且微调后的推理能力不易跨模型迁移。

### 核心瓶颈

上述两类方法的共同瓶颈在于：**思维链的结构（即推理阶段的类型与顺序）是预定义的固定模板，而非针对每个样本自适应生成的**。在测试时缩放方法中，虽然搜索过程可以探索不同的路径，但搜索空间本身仍受限于预设的阶段类型；在训练后方法中，模型学到的推理模式被固化在参数中，缺乏对单一样本特性的灵活适应能力。

更深层的因果机制是：在VLM的多阶段推理过程中，不同阶段对最终答案的贡献存在显著差异——某些阶段（如关键信息提取）对答案有直接且重要的因果影响，而另一些阶段（如冗余的验证步骤）可能仅产生微弱甚至负面的影响。现有方法缺乏一种机制来**量化并利用这种阶段间的重要性差异**，以指导思维链结构的优化。

### 本文动机

ReaGEN的提出基于以下核心洞察：**将思维链结构本身视为可学习的对象**。具体而言，通过利用推理过程中VLM的跨阶段注意力流，可以量化每个推理阶段对最终答案的直接与间接贡献（即阶段重要性），这一因果信号能够有效地区分高效与低效的推理阶段。基于此信号，可以通过教师引导的进化搜索自动发现每道问题的最优思维链结构，并训练一个轻量级生成器（GEN）来预测样本自适应的思维链，从而在推理时以单路径效率获得多路径搜索的灵活性，且无需微调基座VLM。

这一设计旨在同时解决两个关键问题：（1）**效率**——避免推理时的昂贵搜索，将VLM调用次数从数十次降至2-5次；（2）**自适应能力**——为每个样本生成定制化的推理结构，而非依赖固定模板。

## 核心方法与创新机理

ReaGEN 的核心创新在于将**思维链结构本身视为可学习的对象**，并通过因果信号驱动其优化，从而在推理效率与推理质量之间取得突破性平衡。与现有方法相比，ReaGEN 在三个关键维度上实现了根本性转变：

### 1. 思维链结构来源：从固定模板/搜索到自适应预测

现有方法依赖两类范式：**训练后微调方法**（如 VisualCoT / LLaVA-CoT）使用人工预定义的固定思维链模板，缺乏对样本差异的适应性；**测试时缩放方法**（如 VReST、Socratic-MCTS）通过树搜索或多路径采样动态探索推理路径，虽然提高了鲁棒性，但需要数十次 VLM 调用，推理延迟和 token 成本极高。

ReaGEN 提出了一种根本不同的路径：由轻量级生成器 **GEN**（仅 18.3M 参数）根据从默认思维链推理中提取的注意力信号，直接预测出针对当前问题的自适应结构。这一转变的本质在于——**将搜索过程中发现的“结构知识”压缩到生成器中**，使推理时无需搜索即可获得样本定制的思维链。

### 2. 推理时 VLM 调用次数：从数十次到 2-5 次

VReST 等搜索方法需要反复调用 VLM 来评估和选择推理路径，导致推理成本随搜索规模线性增长。ReaGEN 将推理流程精简为：

- **单次预测**（2 次 VLM 调用）：第一次调用执行默认思维链以收集注意力信号，GEN 据此预测定制思维链，第二次调用在该思维链下产生最终答案。
- **迭代优化**（4-5 次调用）：将 GEN 预测的思维链执行后的新注意力再次输入 GEN，进行迭代精化。

实验表明，ReaGEN（4 次迭代）相比 VReST 平均减少 **53% 的 VLM 调用次数**，同时将推理时 token 使用量降低 **79%**（相当于减少 4 倍 token 消耗）。

### 3. 基座 VLM 的修改：从微调到完全冻结

训练后推理方法（如 VisualCoT）需要在构建的思维链数据集上对 VLM 进行 SFT/RL 微调，这不仅需要大规模高质量思维链语料，且不易跨模型迁移。ReaGEN 将基座 VLM **完全冻结**，仅训练 GEN 这一轻量级模块。GEN 通过以下方式学习推理结构：

- **离线阶段**：利用更强的教师 VLM 进行教师引导的进化搜索，基于注意力信号和奖励迭代优化每个样本的思维链结构，生成训练数据。
- **训练阶段**：GEN 学习从图像嵌入、问题嵌入和注意力摘要到最优思维链结构的映射。

这种设计使 ReaGEN 天然具备跨模型迁移的潜力——GEN 作为独立于基座 VLM 的结构预测器，理论上可适配不同的冻结 VLM（尽管当前实验主要在 Qwen3-VL-4B 上验证）。

### 因果机制：注意力引导的阶段重要性

上述三个 changed slots 的实现依赖于一个关键的因果信号——**跨阶段注意力衍生的阶段重要性**（Stage Importance）。ReaGEN 通过分析 VLM 推理过程中各阶段之间的注意力流，量化每个阶段对最终答案的直接与间接贡献：

$$\mathrm{Imp}(i) = \underbrace{A_{i,F}}_{\mathrm{direct}} + \underbrace{\sum_{j=i+1}^{N} \lambda^{j-i} A_{i,j} \mathrm{Imp}(j)}_{\mathrm{indirect}}$$

其中 $A_{i,F}$ 衡量阶段 $i$ 对最终答案的直接注意力贡献，间接项通过衰减因子 $\lambda$ 折现阶段 $i$ 通过后续阶段传导的影响。这一公式将推理过程建模为信息传播网络，使系统能够**抑制低效阶段、增强关键阶段**，从而指导思维链结构的优化。

消融实验（Appendix Table 9）证实了该信号的关键性：移除注意力衍生信号后，所有基准上的性能一致下降，证明注意力引导对有效阶段选择至关重要。

### 与教师搜索的性能关系

消融实验（Table 3）揭示了 GEN 与教师引导搜索之间的能力边界：在视觉为主的任务（VStar、MMStar）上，ReaGEN 恢复了教师搜索的大部分性能，表明 GEN 能有效学习典型的推理结构；而在数学密集型任务（MathVision）上，ReaGEN 与完全教师搜索仍有一定差距，说明 GEN 在捕捉复杂数值推理模式方面仍有提升空间。这一差距也指向了未来工作的方向——可能通过强化学习使 GEN 在推理过程中根据结果反馈持续在线优化。

ReaGEN 的核心思路是将**思维链（CoT）的结构本身**视为可学习的对象：它不修改基座视觉语言模型（VLM），而是训练一个轻量级生成器（GEN），在推理时根据输入样本自适应地预测最优的推理阶段序列，从而以单路径的效率获得多路径搜索的灵活性与鲁棒性。整个框架由三个关键阶段构成，其流程关系如 Figure 1 所示。

![[assets/figures/papers/paper_list_l2224_https_openaccess_thecvf_com_content_CVPR2026_html_Tian_ReaGEN_Adaptive_G/figures/001_Figure_1.jpg]]
*Figure 1: (a) Offline CoT Evolution. Teacher-guided search mutates seed CoTs; the student VLM executes each candidate to obtain a score, stage outputs (MEM), and cross-stage attention (A). Top candidates are selected and mutated for the next round. (b) Generator Training. A lightweight generator (GEN) is trained on search data to map (I, Q, A, CoTinit) → CoTfinal, learning structure from attention while the VLM remains frozen. (c) Inference Time. GEN predicts a sample-adaptive CoT∗ (single pass, or with few-step refinement); the frozen student VLM follows this CoT to produce the final answer. (d) Multimodal Benchmark Performance Overview. Radar plot of accuracies on MMMU-Pro (10/4 options), VStar, MM...*

### 1. 离线阶段：教师引导的进化搜索

在离线数据构建阶段，ReaGEN 为每个图像–问题对自动发现其最优的思维链结构。这一过程由**能力更强的教师 VLM** 引导，采用进化搜索策略：从一个初始的种子思维链出发，教师模型迭代地对候选阶段序列进行变异（增、删、替换推理阶段），并由**冻结的学生 VLM** 执行每个候选思维链，获取其预测得分、各阶段输出以及跨阶段注意力矩阵。搜索的奖励函数综合了预测得分、长度惩罚和多样性惩罚（见公式 $R(\tau) = \alpha s(\tau) - \beta \ell(\tau) - \gamma d(\tau)$），以偏好准确、简洁且多样的思维链。搜索预算上限为 20 轮进化迭代，最终产出每个样本的优化思维链 $\tau^\star$，形成后续生成器训练所需的监督数据。

这一搜索过程的关键创新在于**利用注意力信号量化阶段重要性**。通过从学生 VLM 中提取跨阶段注意力矩阵 $A$（公式 (4)–(5)），ReaGEN 递归地计算每个推理阶段 $i$ 的重要性 $\mathrm{Imp}(i)$，它由该阶段对最终答案的**直接贡献** $A_{i,F}$ 与通过后续阶段传导的**间接贡献** $\sum_{j=i+1}^{N} \lambda^{j-i} A_{i,j} \mathrm{Imp}(j)$ 加权求和得到（公式 (8)）。这一因果信号为搜索提供了信息瓶颈：抑制低效阶段、增强关键阶段，从而引导思维链结构的优化方向。

### 2. 训练阶段：生成器 GEN 的学习

在获得搜索数据后，ReaGEN 训练一个紧凑的生成器 **GEN**（仅 18.3M 参数，基于 4 层 Transformer 编码–解码器架构）来学习从输入信号到最优思维链的映射。GEN 的输入包括图像嵌入 $E^{\mathrm{Img}}$、问题嵌入 $E^{\mathrm{Q}}$、从默认思维链推理中提取的注意力摘要 $A$，以及初始思维链 $\tau^{\mathrm{init}}$；其输出为一个紧凑的 CoT 表示 $\bar{\Psi}(E^{\mathrm{Img}}, E^{\mathrm{Q}}, A, \tau^{\mathrm{init}})$，即预测的阶段 ID 序列（含 EOS 终止符）。在此过程中，**基座 VLM 完全保持冻结**，仅 GEN 参与训练，这使得 ReaGEN 无需任何领域内微调即可跨模型部署。

### 3. 推理阶段：自适应生成与迭代优化

在推理时，ReaGEN 以极低的计算开销实现自适应推理。首先，学生 VLM 使用默认思维链执行一次推理，收集注意力信号；随后 GEN 根据这些信号直接预测出针对当前样本定制的思维链 $\tau^*$；最后，学生 VLM 在预测的思维链指导下再次推理，产生最终答案。这一单路径流程仅需 **2 次 VLM 调用**（1 次收集注意力 + 1 次最终推理），相比测试时搜索方法（如 VReST 需数十次调用）大幅降低了推理延迟与 token 消耗。

此外，ReaGEN 支持**可选的迭代优化**：将 GEN 预测的思维链执行后获得的新注意力再次输入 GEN，更新思维链结构。实验表明，迭代 3–4 次可进一步提升性能（如 MMMU-Pro 10 选任务上从单次预测的 49.94% 提升至 51.90%），同时仍保持远低于搜索方法的调用次数。

### 4. 模块关系与数据流总结

整体数据流可概括为：
- **离线搜索**：教师 VLM → 进化搜索 → 跨阶段注意力与阶段重要性 → 最优思维链 $\tau^\star$（训练标签）
- **训练**：图像/问题嵌入 + 注意力摘要 + 初始思维链 → **GEN** → 预测思维链（监督信号来自 $\tau^\star$）
- **推理**：输入样本 → 默认 CoT 执行（收集注意力）→ **GEN** 预测自适应 CoT → 最终 CoT 执行 → 答案；可选迭代将新注意力反馈至 GEN 进行优化

这种设计使 ReaGEN 在保持基座 VLM 冻结的前提下，实现了对推理结构的显式建模与自适应优化，为多模态推理的效率与准确性提供了新的平衡点。

ReaGEN 的核心机制围绕一个洞察展开：**思维链的结构（阶段序列）本身是可学习的对象**。系统通过教师引导的进化搜索自动发现每道问题的最优思维链，再训练一个轻量级生成器（GEN）在推理时预测样本自适应的结构，从而将多路径搜索的灵活性压缩为单路径推理的效率。以下按功能模块拆解其关键设计与公式。

### 思维链的阶段编码

ReaGEN 将思维链定义为一个有序的阶段序列，每个阶段对应一个预设的推理动作（如文本解读 TI、文本理解 TU、选项评估 CE 等）。为便于生成器预测，每条思维链被编码为固定长度的阶段 ID 向量：

$$\mathbf{c} = (c_1, \dots, c_L, c_{L+1}, \dots, c_{L_{\mathrm{max}}})$$

其中 $c_t$ 为第 $t$ 步的阶段 ID，$L$ 为实际阶段数，末尾以 EOS 标记，剩余位置填充至最大长度 $L_{\mathrm{max}}$。这种一维序列编码使思维链结构可以作为标准的自回归预测目标。

### 多阶段记忆与跨阶段注意力提取

在执行思维链的每个阶段时，冻结的学生 VLM 接收图像 $I$、问题 $Q$、累积记忆 $M_t$ 和当前阶段提示 $s_t$，输出该阶段的结果 $y_t$：

$$y_t = f_{\theta}(I, Q, M_t, s_t)$$

记忆按如下方式累积，确保后续阶段能访问所有先前的推理输出：

$$M_{t+1} = M_t \cup \{ y_t \}$$

**跨阶段注意力聚合**是 ReaGEN 因果信号的核心来源。对于任意两个阶段 $i < j$，定义 $j$ 对 $i$ 的未归一化跨阶段注意力为 $j$ 中所有 token 对 $i$ 中所有 token 在所有层 $\mathcal{L}$ 和所有注意力头 $\mathcal{H}$ 上的平均注意力值：

$$\tilde{A}_{i,j} = \frac{1}{|T_j|} \sum_{u \in T_j} \sum_{v \in T_i} \left( \frac{1}{|\mathcal{L}| |\mathcal{H}|} \sum_{\ell \in \mathcal{L}} \sum_{h \in \mathcal{H}} \alpha_{u,v}^{(j,\ell,h)} \right), \quad i < j$$

其中 $T_i$、$T_j$ 分别为阶段 $i$、$j$ 的 token 集合，$\alpha_{u,v}^{(j,\ell,h)}$ 是阶段 $j$ 的 token $u$ 对阶段 $i$ 的 token $v$ 在第 $\ell$ 层第 $h$ 个注意力头上的注意力权重。随后对每个阶段 $j$ 做归一化，得到注意力质量矩阵：

$$A_{i,j} = \frac{\tilde{A}_{i,j}}{\sum_{k < j} \tilde{A}_{k,j} + \varepsilon}, \quad i < j$$

该矩阵量化了每个后续阶段对各个先前阶段的相对信息依赖强度。

### 阶段重要性的递归计算

基于注意力质量矩阵，定义每个阶段 $i$ 的**阶段重要性** $\mathrm{Imp}(i)$，它由该阶段对最终答案的直接贡献和通过后续阶段间接传导的影响共同决定：

$$\mathrm{Imp}(i) = \underbrace{A_{i,F}}_{\mathrm{direct}} + \underbrace{\sum_{j=i+1}^{N} \lambda^{j-i} A_{i,j} \mathrm{Imp}(j)}_{\mathrm{indirect}}$$

其中 $A_{i,F}$ 是阶段 $i$ 对最终答案（Final）的注意力质量，$\lambda \in (0,1]$ 为衰减因子，$N$ 为总阶段数。该递归公式从后向前计算：最终阶段的重要性仅由其直接贡献决定，而中间阶段的重要性则包含了其通过下游阶段产生的间接影响。这一因果信号使系统能够识别哪些阶段对推理结果至关重要、哪些阶段冗余低效，从而指导思维链的剪枝与增强。

### 思维链奖励函数

在进化搜索中，每条候选思维链 $\tau$ 的质量由一个综合奖励函数评估：

$$R(\tau) = \alpha s(\tau) - \beta \ell(\tau) - \gamma d(\tau)$$

其中 $s(\tau)$ 为该思维链下学生 VLM 的预测得分（由教师模型评判），$\ell(\tau)$ 为归一化的思维链长度惩罚（鼓励简洁的结构），$d(\tau)$ 为多样性惩罚（防止搜索陷入局部最优）。超参数 $\alpha$、$\beta$、$\gamma$ 控制三者的相对权重。

### 生成器 GEN 的映射与推理

GEN 是一个紧凑的 Transformer 编码-解码器（约 18.3M 参数），其输入为图像嵌入 $E^{\mathrm{Img}}$、问题嵌入 $E^{\mathrm{Q}}$、从默认思维链推理中提取的注意力摘要 $A$ 以及初始思维链 $\tau^{\mathrm{init}}$，输出为优化后的思维链表示：

$$\bar{\Psi}(E^{\mathrm{Img}}, E^{\mathrm{Q}}, A, \tau^{\mathrm{init}})$$

在推理时，GEN 以自回归方式预测阶段 ID 序列，并通过两个输出头分别预测阶段序列和思维链长度。整个过程仅需 2 次 VLM 调用（一次收集注意力信号，一次执行预测的思维链），或通过迭代优化扩展至 3-4 次调用，在保持基座 VLM 完全冻结的前提下实现了样本自适应的结构化推理。

## 实验与关键发现

### 核心结果：多模态推理基准上的性能与效率

ReaGEN在多个复合多模态推理基准上展现了显著的性能提升，同时大幅降低了推理成本。Table 1汇总了基于冻结学生模型Qwen3-VL-4B的准确率对比。在视觉密集型任务上，ReaGEN（4次迭代）在VStar上达到84.49%，在MMStar上达到75.77%，均显著优于测试时缩放基线VReST（Zhang et al., 2025）。在需要跨学科知识的MMMU-Pro基准上，ReaGEN同样表现强劲：4选项任务上达到64.51%，10选项任务上通过3次迭代达到51.90%，超越了直接回答和VReST等基线。

值得注意的是，ReaGEN在效率方面的优势更为突出。Figure 2的推理成本分析显示，ReaGEN在跨基准测试中平均减少了79%的token使用量，相当于将VReST的token消耗降低了约4倍。同时，ReaGEN的VLM调用次数平均减少了53%。这一效率提升源于ReaGEN用单路径自适应思维链替代了VReST的多路径树搜索，仅需2次（单次GEN预测）至4-5次（迭代优化）VLM调用即可完成推理。

### 跨数据集泛化能力

Table 2揭示了GEN学习到的推理结构具有显著的跨域迁移能力。当GEN在数学中心的数据集MathVision上训练后，直接应用于视觉基准MMStar时，相对VReST获得了+26.0个准确率百分点的提升，无需任何重新训练或微调。这一结果表明，数学推理中习得的结构化思维模式（如逐步分解、条件判断）对视觉推理任务同样有效。相比之下，在视觉中心的数据集MMStar上训练的GEN，虽然在视觉任务上表现良好，但对数学密集型任务（如MathVision）的迁移效果有限。这种不对称的泛化行为暗示，数学推理可能蕴含了更通用、更可迁移的推理原语。

### 消融实验：注意力信号与搜索结构的贡献

消融实验从两个关键维度验证了ReaGEN设计的有效性。首先，附录Table 9显示，当移除注意力衍生信号后，VStar、MMMU-Pro和MathVision等基准上的性能一致下降，直接证明了跨阶段注意力流对正确选择推理阶段的关键作用。注意力信号量化了各阶段对最终答案的直接与间接贡献（即Stage Importance），为GEN提供了抑制冗余阶段、强化关键阶段的因果依据。

其次，Table 3对比了教师引导搜索（T-Search，无GEN）与ReaGEN的性能。在视觉为主的任务（VStar、MMStar）上，ReaGEN恢复了搜索方法的大部分性能，表明GEN能够有效学习典型的视觉推理结构。然而，在数学密集型任务（MathVision）上，ReaGEN与完全搜索之间仍存在一定差距，说明GEN在捕捉复杂数值推理的精细模式方面尚有提升空间。这一差距指出了未来工作的方向：可能需要更强的教师模型或更丰富的搜索空间来覆盖数学推理的多样性。

### 迭代优化的增益

ReaGEN的迭代优化机制在困难任务上展现出持续增益。在MMMU-Pro 10选项任务上，从单次预测到2次迭代再到3次迭代，准确率逐步提升至51.90%。这表明，将GEN预测的思维链执行后获得的新的注意力信号再次输入GEN，能够形成有效的反馈闭环，使推理结构在迭代中逐步精化。这种轻量级的在线优化仅需额外1-2次VLM调用，远低于传统搜索方法的成本。

### 公平性说明与局限性

所有对比实验均基于相同的冻结学生模型Qwen3-VL-4B，确保了公平性。对于VReST基线，论文还额外报告了使用与ReaGEN相同教师模型（Qwen3-VL-32B）作为奖励模型的结果，以排除教师模型能力差异的影响。需要指出的是，ReaGEN假设可以访问学生VLM的内部注意力信号，因此主要适用于自托管或开源VLM；对于无法暴露注意力的闭源API模型，本方法不适用。此外，GEN的训练质量依赖于教师模型的搜索能力，若教师模型本身能力不足，可能无法探索到足够好的思维链结构。

![[assets/figures/papers/paper_list_l2224_https_openaccess_thecvf_com_content_CVPR2026_html_Tian_ReaGEN_Adaptive_G/figures/002_Table_1.jpg]]
*Table 1: ReaGEN results on composite benchmarks. All numbers are accuracy (%). Bold denotes the best performance in each benchmark. Color-coded arrows show absolute change relative to the VReST baseline using the same student model (Qwen3-VL-4B).We also report VReST (Teacher-Reward, 32B), where VReST uses Qwen3-VL-4B as the base model and Qwen3-VL-32B as the reward model during search, matching the teacher used by ReaGEN. 2 iter denotes a single-pass ReaGEN: the first student call uses a default/seed CoT to collect attention; GEN predicts a tailored CoT; the second student call produces the final answer under that predicted CoT. Larger iteration counts $(\ge$ 3 ) indicate additional GEN-guided refinem...*

![[assets/figures/papers/paper_list_l2224_https_openaccess_thecvf_com_content_CVPR2026_html_Tian_ReaGEN_Adaptive_G/figures/003_Table_2.jpg]]
*Table 2: Cross-dataset generalization of ReaGEN. The GEN is trained either on the math-centric MathVision dataset or the visioncentric MMStar dataset, and then evaluated on a mix of vision and math benchmarks. Bold values indicate the best accuracy for each evaluation dataset. Color-coded arrows denote absolute improvement relative to the VReST baseline using the same frozen student model. ReaGEN trained on MathVision generalizes particularly well to vision benchmarks such as MMStar, achieving up to +26 points without retraining.*Results are reproduced by us for a fair comparison*

![[assets/figures/papers/paper_list_l2224_https_openaccess_thecvf_com_content_CVPR2026_html_Tian_ReaGEN_Adaptive_G/figures/006_Table_3.jpg]]
*Table 3: Ablation: Teacher-Guided Search vs. ReaGEN. “T-Search” denotes the accuracy obtained by directly using the teacher-guided search output (no GEN). MMMU = MMMU(val), MVerse = MathVerse (w/o vision)*

## 定位与知识库关联

### 1. 核心问题定位：从“推理内容”到“推理结构”

当前多模态大模型（LVLM）在复杂视觉推理中的瓶颈已从“能否产生推理”转向“如何高效组织推理”。现有方案大致分为两条路线：

- **测试时缩放（Test-Time Scaling）**：以 **VReST**（Zhang et al., 2025）和 **Socratic-MCTS**（Acuna et al., 2025）为代表，通过树搜索、多路径采样或自我奖励机制在推理时探索多条思维链，以提升鲁棒性。代价是VLM调用次数激增（通常数十次），推理延迟和token成本居高不下。
- **训练后微调（Post-Training）**：以 **VisualCoT**（Shao et al., 2024）和 **LLaVA-CoT**（Xu et al., 2025）为代表，在人工构建或蒸馏得到的思维链语料上微调VLM参数，使其内化推理模式。问题在于依赖大规模高质量思维链数据，且微调后的推理结构固化，不易跨模型迁移。

ReaGEN在这两条路线之间开辟了第三条路径：**将思维链结构本身作为可学习的对象**，而非仅优化推理内容或搜索路径。其核心洞察是：每道问题的“最优思维链结构”（即阶段序列的组成与顺序）可以通过教师引导的进化搜索自动发现，而一个轻量级生成器（GEN）可以学会直接从注意力信号中预测这种结构——推理时无需搜索，也无需微调基座VLM。

### 2. 方法谱系中的定位：关键设计槽位的变更

为清晰定位ReaGEN相对于基线方法的设计差异，下表梳理了三个关键“可变更槽位”上的对比：

| 设计维度 | 基线方案（测试时缩放/训练后微调） | ReaGEN方案 | 证据锚点 |
|---------|--------------------------------|-----------|---------|
| **思维链结构的来源** | 人工预定义的固定模板（如VisualCoT），或通过树搜索/多路径采样动态生成（如VReST） | 由轻量级生成器（GEN）根据默认思维链推理中提取的注意力信号，直接预测出针对当前问题的自适应结构 | Section 3.3, Figure 1(b,c) |
| **推理时的VLM调用次数** | 多次：VReST等搜索方法需调用数十次VLM | 2次（单次GEN预测）至4-5次（迭代优化），平均减少53% | Figure 2(b) |
| **基座VLM的修改** | SFT/RL等训练后方法需微调VLM参数 | VLM完全冻结，仅训练一个18.3M参数的GEN | Section 3.3, Abstract |

这种设计使得ReaGEN在方法谱系中占据一个独特位置：它继承了测试时缩放方法“每样本自适应”的灵活性（通过GEN为不同问题预测不同结构），同时拥有训练后方法“单路径推理”的效率（推理时仅需2-5次VLM调用）。其技术代价是将复杂性转移到了离线阶段——需要教师引导的进化搜索来构建训练数据。

### 3. 与测试时缩放方法的深度对比

**VReST** 是ReaGEN最直接对比的测试时缩放基线。两者都追求提升视觉推理的鲁棒性，但机制截然不同：

- VReST通过树搜索在推理时探索多条视觉推理路径，用自我奖励机制筛选最优路径。这本质上是“用计算换鲁棒性”。
- ReaGEN通过GEN在推理前预测最优路径结构，然后用单路径执行。这本质上是“用学习换效率”。

实验证据表明，ReaGEN在效率上的优势是压倒性的：推理时平均token使用量降低79%（相当于4倍token消耗减少），VLM调用次数平均减少53%。更关键的是，这种效率提升并未牺牲性能——在多个基准上，ReaGEN相对VReST实现了最高+26个绝对准确率百分点的提升（Abstract，Table 2中跨数据集设置下MMStar上的结果）。

**Socratic-MCTS** 作为另一个测试时基线，采用迭代提问与蒙特卡洛树搜索的方式。ReaGEN与之的核心区别在于：Socratic-MCTS将搜索空间定义在“提问内容”上，而ReaGEN将搜索空间定义在“推理阶段结构”上，且搜索仅发生在离线训练阶段。

### 4. 适用边界与局限性

基于已验证的分析，ReaGEN的适用边界受以下因素制约：

**（1）对注意力信号的可访问性依赖**
ReaGEN假设可以访问学生VLM的内部注意力分布，以计算跨阶段注意力矩阵和阶段重要性（Imp(i)）。这意味着该方法主要适用于自托管或开源VLM（如实验中使用的Qwen3-VL-4B）。对于无法暴露注意力的闭源API模型（如GPT-4V），本方法不适用。这是一个硬性约束，而非可绕过的工程问题。

**（2）教师模型质量的瓶颈效应**
GEN的训练数据来自教师引导的进化搜索，搜索质量直接取决于教师VLM的能力。若教师模型在特定领域（如密集数学推理）能力不足，则可能无法探索到足够好的思维链结构，进而限制GEN的学习上限。消融实验（Table 3）显示，在数学密集型任务MathVision上，ReaGEN与完全教师搜索（T-Search）之间仍存在差距，印证了这一瓶颈。

**（3）跨架构迁移的未验证性**
现有实验主要在Qwen3-VL-4B上进行。虽然跨数据集泛化实验（Table 2）展示了GEN在视觉与数学任务间的迁移能力，但GEN在其他VLM架构（如不同规模的LLaVA系列、InternVL系列）上的效果尚未验证。不同架构的注意力分布模式可能存在差异，GEN能否泛化到这些分布尚需实验确认。

**（4）复杂数值推理的捕捉能力**
在MathVision等需要密集数学推理的任务上，ReaGEN与完全教师搜索的差距表明，GEN在捕捉复杂数值推理模式方面仍有提升空间。这可能是因为数学推理的“最优结构”比视觉推理具有更大的样本间方差，搜索发现的模式更难被紧凑的GEN模型泛化。

### 5. 开放问题与未来方向

**（1）向纯文本推理的扩展**
当前ReaGEN聚焦于多模态视觉推理场景。一个自然的问题是：如何将注意力引导的思维链生成方法扩展到纯文本推理任务（如数学文字题、逻辑推理），以提升大语言模型的推理效率？这需要重新定义“阶段”的语义（从视觉推理阶段转为文本推理阶段），并验证注意力信号在纯文本场景下的有效性。

**（2）闭源模型的近似方案**
对于无法访问内部注意力的闭源模型，是否可以通过提示工程（如要求模型输出中间步骤的置信度）或输出分布估计（如logit层面的熵分析）等方式近似注意力信号？若能找到有效的代理信号，ReaGEN的适用边界将大幅扩展。

**（3）更丰富的结构动作空间**
当前GEN预测的是线性阶段序列。能否将GEN的结构设计成支持更丰富的动作空间，如条件分支（“若上一步置信度低则执行验证阶段”）、循环（“重复分析直至收敛”）？这将使ReaGEN适应更复杂的推理场景，但也对GEN的训练数据和架构设计提出更高要求。

**（4）在线强化学习的融合**
当前GEN完全依赖离线搜索数据进行训练。能否将ReaGEN与强化学习相结合，使GEN在推理过程中根据结果反馈持续在线优化？这将消除对离线搜索数据的依赖，使系统具备自我改进能力，但同时引入了奖励信号稀疏性和训练稳定性等新挑战。

## 原文 PDF

![[paperPDFs/CVPR_2026/ReaGEN_Adaptive_Generation_of_Structured_Chains_of_Thought_for_Efficient_Multimodal_Reasoning.pdf]]
