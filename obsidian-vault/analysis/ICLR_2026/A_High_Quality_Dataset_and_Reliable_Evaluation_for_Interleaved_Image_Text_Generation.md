---
title: "A High Quality Dataset and Reliable Evaluation for Interleaved Image-Text Generation"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/A_High_Quality_Dataset_and_Reliable_Evaluation_for_Interleaved_Image_Text_Generation.pdf
project_link: null
code_link: null
aliases:
- ISS
- HQDREIITG
- "InterSyn + SEIR + SynJudge"
tags:
- ICLR_2026
- topic/benchmarks_datasets_evaluation
- topic/benchmarks_datasets_evaluation/benchmark_eval
core_operator: "通过构建大规模（1.8M样本）、高质量（SEIR迭代精炼）、指令丰富（3500主题层次+人工模板）的数据集InterSyn，并配合多维度自动评估器SynJudge，可以系统性地提升模型的文本内容完整性、图像内容完整性、图像质量以及图文协同性。"
primary_logic: "核心洞察在于：1）数据质量可通过自评估-迭代精炼（SEIR）的自动化流程显著提升，无需大量人工干预；2）图文协同（ITS）是比传统图文一致性更关键的评估维度，它奖励互补性而非冗余性；3）仅需25K-50K高质量样本即可带来显著性能提升，表明数据密度比数据规模更重要。"
claims:
- "SEIR方法在TCC、ICC、IQ、ITS四个维度上均取得最高平均分，且方差最低（低于0.61）。"
- "在InterSyn上微调25K-50K样本即可带来显著性能提升，扩展到200K时TCC、ICC和ITS持续改善。"
- "QwenVL微调后的SynJudge与人类判断的对齐最强，平均A@1达到95.4%，RMSE最低。"
- "答案精炼（AR）和图像精炼（IR）均对最终质量有正向贡献，AR提升TCC、ICC和ITS，IR进一步提升ICC和ITS。"
---

# A High Quality Dataset and Reliable Evaluation for Interleaved Image-Text Generation

> [!tip] 核心洞察
> 核心洞察在于：1）数据质量可通过自评估-迭代精炼（SEIR）的自动化流程显著提升，无需大量人工干预；2）图文协同（ITS）是比传统图文一致性更关键的评估维度，它奖励互补性而非冗余性；3）仅需25K-50K高质量样本即可带来显著性能提升，表明数据密度比数据规模更重要。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 面向交错图文生成的高质量数据集与可靠评估方法 |
| 英文题名 | A High Quality Dataset and Reliable Evaluation for Interleaved Image-Text Generation |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=qBORZkk28r) |
| Topic | #topic/benchmarks_datasets_evaluation #topic/benchmarks_datasets_evaluation/benchmark_eval |
| Method | InterSyn + SEIR + SynJudge |
| Dataset | InterSyn Evaluation Benchmark (4000 questions) |

> [!tip] 效果简介
> - InterSyn Evaluation Benchmark (4000 questions) 上，TCC (Human) 为 4.41，对比 GPT-4o+DALL-E3: 4.32，变化 +0.09。
> - InterSyn Evaluation Benchmark (4000 questions) 上，ITS (Human) 为 4.51，对比 GPT-4o+DALL-E3: 4.39，变化 +0.12。
> - InterSyn Evaluation Benchmark (4000 questions) 上，TCC (SynJudge) 为 4.42，对比 GPT-4o+DALL-E3: 4.44，变化 -0.02。

## 概要

交错图文生成——即模型在单次响应中交替输出文本与图像——正成为多模态生成领域的关键能力。然而，现有模型在此任务上的性能受限于一个根本瓶颈：训练数据规模有限、质量参差不齐且指令多样性不足，导致模型难以生成紧密耦合、指令跟随性强的交错输出。

针对这一问题，本文提出了一个系统性的解决方案，包含三个核心贡献：**InterSyn** 数据集、**SEIR** 数据精炼方法，以及 **SynJudge** 多维度评估器。

InterSyn 是迄今规模最大的交错图文指令数据集，包含约 180 万单轮样本和 5 万多轮对话，覆盖 8 大领域、3500 个细粒度主题。其数据质量由 SEIR 方法保障——一种自评估-迭代精炼流程，通过三级循环（问题精炼 QR、答案精炼 AR、图像精炼 IR）自动提升样本质量，无需大量人工干预。实验表明，SEIR 在文本内容完整性（TCC）、图像内容完整性（ICC）、图像质量（IQ）和图文协同性（ITS）四个维度上均取得最高平均分，且方差最低（低于 0.61），甚至使开源模型组合（Qwen+InternVL+Flux）在 TCC 和 ITS 上逼近闭源 GPT-4o+DALL-E3 组合（差距小于 0.03）。

SynJudge 是一个在 48K 人工标注数据上微调的评估模型（基于 QwenVL），输出四个可解释的维度分数。与零样本 MLLM 评估器相比，SynJudge 与人类判断的对齐最强，平均 A@1 达到 95.4%，RMSE 最低。值得注意的是，ITS（图文协同性）被证明是比传统图文一致性更关键的评估维度——它奖励互补性而非冗余性，为评估提供了新的视角。

在 InterSyn 上微调仅 25K–50K 样本即可带来显著性能提升，扩展到 200K 时 TCC 和 ITS 持续改善（如 Anole 的 ITS 从 2.26 提升至 3.11，VILA-U 的 TCC 从 2.46 提升至 3.52），表明数据密度比数据规模更重要。多轮训练能有效减缓后续轮次的性能下降，尤其对 ITS 指标。同时，微调后模型在 MME-P、MMBench 等标准理解基准上的性能基本保持，未出现灾难性遗忘。

当前框架的局限包括：图像视觉保真度受限于文生图模型上限；每轮对话限制为单图像，偏离需要多图像比较或推理的真实场景；SynJudge 仅设计用于单图像响应评估。未来工作可探索 SEIR 向更大规模或更复杂任务的扩展、SynJudge 向视频-文本等领域的迁移，以及多图像评估方案的设计。



交错图文生成（Interleaved Image-Text Generation）要求模型输出由文本段落与插入图像交织而成的多模态内容，是对话系统、教育材料生成、逐步说明等场景的核心能力。然而，现有方法在生成紧密耦合、指令跟随性强的交错输出时表现不佳，其根本瓶颈并非模型架构，而是训练数据在规模、质量和指令多样性三个维度上的系统性不足。

**现有数据集的共同缺陷**是问题的根源。大规模网页级数据集如MMC4（101.2M文档）和OBELICS（141M页面）虽然规模巨大，但本质是爬取数据的拼接，缺乏指令跟随结构，噪声严重且难以控制质量。文档级数据集如CoMM和LeafInstruct虽然经过筛选，但规模通常不超过数万样本，且指令模式单一、缺乏多轮对话能力。更重要的是，这些数据集均未采用标准化的质量控制流程——依赖网页爬取或复用现有语料意味着无法保证图文之间的语义对齐和协同性。这导致模型在训练中无法学习到“文本解释图像”或“图像补充文本”这类精细的互补关系，而只能生成内容冗余或语义脱节的交错输出。

**评估方法的缺口**进一步加剧了问题。现有基准如InterleavedBench和OpenING仅关注粗粒度的图文一致性，无法量化文本完整性、图像质量以及图文之间真正的协同关系。零样本MLLM评估器虽然可扩展，但与人类判断偏差大，无法为模型开发提供可靠的反馈信号。

**本文的动机**正是填补这两个缺口。核心洞察在于：数据质量可通过自动化的自评估-迭代精炼（SEIR）流程系统性地提升，而无需大量人工干预；同时，图文协同（ITS）应被确立为比传统一致性更关键的评估维度，它奖励互补性而非冗余性。为此，作者构建了InterSyn数据集——包含约1.8M单轮样本和50K多轮对话，通过三级精炼（问题精炼QR、答案精炼AR、图像精炼IR）确保质量，并基于3500主题层次和人类偏好模板保证指令多样性。同时，训练了四维评估器SynJudge（TCC文本内容完整性、ICC图像内容完整性、IQ图像质量、ITS图文协同性），在48K人工标注数据上微调QwenVL，使其与人类判断的平均对齐率（A@1）达到95.4%。实验表明，仅需25K-50K高质量样本即可带来显著性能提升，且SEIR方法使开源模型组合的性能逼近闭源模型（GPT-4o+DALL-E3），差距小于0.03分。



## 核心方法与创新机理

本文的核心创新在于系统性地识别并填补了交错图文生成领域的关键瓶颈——**训练数据质量与评估方法的双重缺失**，并围绕这一瓶颈构建了从数据生成到评估的完整解决方案。与现有工作相比，创新体现在以下五个关键维度的改变上。

**1. 数据规模与质量控制机制的范式转变**

现有交错图文数据集（如MMC4、OBELICS）通常依赖网页爬取或现有语料过滤，规模虽大但噪声高、指令跟随性弱；而小规模人工标注数据集（如LeafInstruct、OpenLEAF）则受限于规模。本文提出的InterSyn数据集将规模推至**1.8M单轮样本 + 50K多轮对话**，同时引入了一套全新的质量控制机制——**自评估迭代精炼（SEIR）**。SEIR的核心洞察在于：通过嵌入自检与反馈循环，可以在**无需大量人工干预**的情况下自动化地提升数据质量。具体而言，SEIR包含三级精炼流程：问题精炼（QR）提升指令清晰度，答案精炼（AR）增强文本内容完整性与图文协同性，图像精炼（IR）进一步优化图像内容完整性与视觉质量。消融实验（Table 4）证实，AR和IR均对最终质量有正向贡献，且SEIR对低性能模型组合的提升效果尤为显著（如InternLM+QwenVL的TCC提升+0.60，ITS提升+0.70，见Table 8）。

**2. 指令多样性的系统化保障**

现有数据集往往缺乏指令多样性，多为静态文档或单轮提示。本文通过收集25名参与者的1000个问题，经LLM过滤+专家审查保留500个高质量问题，并从中提取通用问题模板，再结合AI辅助构建的**3500个主题层次结构**，实现了对人类查询风格的系统性捕获与规模化扩展。这一设计使得数据集能够覆盖8个主要领域，指令多样性与上下文丰富性远超现有基准。

**3. 评估维度的重新定义：图文协同性（ITS）**

现有评估方法（如OpenING、IntJudge）仅关注图文一致性或表面正确性，忽略了交错图文生成中**互补性**这一关键特性。本文提出了**四维评估体系**：文本内容完整性（TCC）、图像内容完整性（ICC）、图像质量（IQ）以及**图文协同性（ITS）**。其中ITS是核心创新维度，它奖励图文之间的互补性而非冗余性——例如，当文本描述抽象概念（如“爱因斯坦的相对论”）而图像提供直观示例（如“弯曲的时空网格”）时，ITS评分会高于图文简单重复的场景。这一设计更贴合真实应用场景中图文互补的需求。

**4. 评估器与人类判断对齐度的突破**

零样本MLLM评估器（如GPT-4o、InternVL）与人类判断之间存在显著偏差。本文通过在**48K人工标注样本**上微调QwenVL，训练出SynJudge评估器，实现了**平均A@1达95.4%**的人类一致性，RMSE为所有评估器中最低（Table 6）。这一突破的关键在于：训练数据覆盖了SEIR生成的多样化样本，且每位专家评分后经讨论达成一致，减少了主观偏差。微调后的SynJudge不仅与人类对齐最强，还提供了可解释的四维定量评分，为后续研究提供了标准化评估工具。

**5. 数据密度优于数据规模的发现**

实验表明（Table 1），仅需**25K-50K高质量样本**即可带来显著性能提升（如Anole的TCC从3.09提升至3.36，ITS从2.26提升至2.82），扩展到200K时TCC、ICC和ITS持续改善。这一发现挑战了“数据规模越大越好”的传统认知，揭示了**数据密度（质量/规模比）**在交错图文生成任务中的主导作用。此外，SEIR缩小了开源模型与闭源模型之间的差距——在SEIR优化后，Qwen+InternVL+Flux与GPT-4o+DALL-E3在TCC和ITS上的差距小于0.03（Table 8），表明高质量数据可以部分弥补模型能力的不足。



InterSyn的整体框架由两个核心环节构成：**数据集准备工作**和**自评估迭代精炼（SEIR）流水线**，最终输出高质量的交错图文数据，并配套训练了多维度评估器SynJudge。

**数据集准备工作**（Figure 2上半部分）包含四个步骤：首先，从25名参与者收集1000个初始问题，经LLM过滤和专家审查，保留500个高质量问题作为基准。然后，从这些问题中提取通用问题模板，捕获人类对话查询风格。接着，通过AI辅助主题提取和人工整理，构建基础主题层次结构，并进一步扩展至8个领域、3500个细粒度主题。这一准备工作确保了指令的多样性和覆盖广度，是后续生成高质量数据的前提。

**SEIR流水线**（Figure 2下半部分）是数据质量保障的核心机制，它通过三级迭代精炼循环系统性地提升样本质量。每一级都遵循统一的精炼算子：$x_k = \mathcal{M}_{refine}(x_{k-1}, s_k)$，其中评估器反馈$s_k = \mathcal{M}_{eval}(x_{k-1}, \mathcal{C})$驱动内容的迭代优化。具体流程为：

1. **问题精炼（QR）**：基于主题$z$和对话历史$\mathcal{H}^{(t-1)}$，将初始问题$q_0^{(t)}$迭代精炼为最终问题$q^{(t)}$。Figure 3和实验表明，质量在前三次迭代中显著提升，之后趋于平稳。

2. **答案精炼（AR）**：基于精炼后的问题$q^{(t)}$和历史$\mathcal{H}^{(t-1)}$，将初始答案和临时图像描述迭代精炼为最终答案$\mathbf{a}^{(t)}$和描述$\mathbf{\gamma}^{(t)}$。Table 4显示，AR主要提升文本内容完整性（TCC）、图像内容完整性（ICC）和图文协同性（ITS）。

3. **图像精炼（IR）**：这是最复杂的循环——从描述$c_k^{(t)}$生成图像$I_k^{(t)}$，VLM评估器$\mathcal{V}$基于图像、问题、答案和历史给出反馈$s_c^{(k)}$，然后精炼描述为$c_{k+1}^{(t)}$，循环直至收敛。Table 4表明，IR进一步增强了ICC和ITS。

SEIR流水线输出的最终数据构成**InterSyn数据集**，包含约180万单轮样本和5万多轮对话样本，覆盖8个主要领域。该数据集的独特之处在于：1）通过SEIR实现了自动化质量控制，无需大量人工干预；2）指令多样性通过3500主题层次结构和人类偏好模板得到保证；3）仅需25K-50K高质量样本即可带来显著性能提升（Table 1），表明数据密度比数据规模更重要。

**SynJudge评估器**是框架的另一个关键模块。它在48K人工标注样本上微调QwenVL，训练输出四个可解释的分数：文本内容完整性（TCC）、图像内容完整性（ICC）、图像质量（IQ）和图文协同性（ITS）。其中ITS是比传统图文一致性更关键的维度，它奖励互补性而非冗余性。实验表明（Table 6），微调后的QwenVL评估器与人类判断的对齐最强，平均A@1达到95.4%，RMSE最低。

**整体输入输出流**为：用户问题（可附带对话历史）→ 数据集准备工作生成多样化指令 → SEIR流水线精炼问题、答案和图像 → 输出高质量交错图文样本 → SynJudge提供四维定量评估。这一框架的核心洞察在于：通过自评估-迭代精炼的自动化流程，可以在无需大量人工干预的前提下系统性提升数据质量，而图文协同性（ITS）是比传统图文一致性更关键的评估维度。



该论文的核心技术贡献体现在三个模块：**SEIR**（自评估迭代精炼）数据集构建流水线、**InterSyn**大规模交错图文数据集，以及**SynJudge**四维自动评估器。本节聚焦SEIR的迭代精炼机制及其关键公式。

### SEIR：自评估迭代精炼

SEIR的底层逻辑是一个通用的迭代精炼算子，其核心思想是利用评估器的反馈信号来指导内容生成，形成“生成→评估→精炼”的闭环。通用形式为：

$$x_k = \mathcal{M}_{refine}(x_{k-1}, s_k), \quad \mathrm{where} \quad s_k = \mathcal{M}_{eval}(x_{k-1}, \mathcal{C})$$

其中 $x_k$ 是第 $k$ 次迭代后的内容，$\mathcal{M}_{refine}$ 是精炼模型，$s_k$ 是评估器 $\mathcal{M}_{eval}$ 基于当前内容 $x_{k-1}$ 和上下文 $\mathcal{C}$ 给出的反馈信号。该算子被实例化为三个顺序执行的精炼阶段：

1.  **问题精炼（QR）**：基于主题 $z$ 和对话历史 $\mathcal{H}^{(t-1)}$，将初始问题 $q_0^{(t)}$ 精炼为更清晰、更深入的问题 $q^{(t)}$：
    $$q^{(t)} = \Phi(q_0^{(t)} \mid \mathcal{C} = \{z, \mathcal{H}^{(t-1)}\})$$
    消融实验（Figure 3）表明，QR在前三次迭代中质量提升显著，之后趋于平稳。

2.  **答案精炼（AR）**：基于精炼后的问题 $q^{(t)}$ 和历史 $\mathcal{H}^{(t-1)}$，对初始答案和临时图像描述进行协同优化，得到最终答案 $\mathbf{a}^{(t)}$ 和描述 $\mathbf{\gamma}^{(t)}$：
    $$(\mathbf{a}^{(t)}, \mathbf{\gamma}^{(t)}) = \Phi((\mathbf{a}_0^{(t)}, \mathbf{\gamma}_0^{(t)}) \mid \mathcal{C} = \{\mathbf{q}^{(t)}, \mathcal{H}^{(t-1)}\})$$
    实验（Table 4）证实AR主要提升文本内容完整性（TCC）、图像内容完整性（ICC）和图文协同性（ITS）。

3.  **图像精炼（IR）**：这是SEIR中最关键的循环，它利用视觉语言模型（VLM）对生成图像的评估来反向优化图像描述，从而间接提升图像质量。其循环过程由三个步骤构成：
    $$I_k^{(t)} = \mathcal{G}(c_k^{(t)}), \quad s_c^{(k)} = \mathcal{V}(I_k^{(t)}, q^{(t)}, a^{(t)}, \mathcal{H}^{(t-1)}), \quad c_{k+1}^{(t)} = \mathcal{M}_{refine}(c_k^{(t)}, s_c^{(k)})$$
    其中 $\mathcal{G}$ 是文生图模型，$\mathcal{V}$ 是VLM评估器。该循环从当前描述 $c_k^{(t)}$ 生成图像 $I_k^{(t)}$，然后由VLM给出评估反馈 $s_c^{(k)}$，最后根据反馈精炼描述为 $c_{k+1}^{(t)}$。Table 4显示，IR在AR的基础上进一步提升了ICC和ITS。

### 评估指标与SynJudge

SynJudge在四个维度上对生成结果进行定量评分：
- **TCC**：文本内容完整性
- **ICC**：图像内容完整性
- **IQ**：图像质量
- **ITS**：图文协同性（论文核心洞察，奖励互补性而非冗余性）

评估器与人类判断的对齐程度通过以下指标衡量：

- **平均分**：$S_d = \frac{1}{N} \sum_{i=1}^N x_{i,d}$，表示生成器在维度 $d$ 上的平均性能。
- **方差**：$\sigma_d = \frac{1}{N} \sum_{i=1}^N (x_{i,d} - S_d)^2$，衡量生成器在不同问题上的性能稳定性。SEIR生成的数据方差低于0.61（Table 5），表明一致性高。
- **RMSE**：$\mathrm{RMSE}_d = \sqrt{\frac{1}{N} \sum_{i=1}^N (x_{i,d}^M - x_{i,d}^H)^2}$，衡量模型评估器与人类评估器评分之间的偏差。微调后的QwenVL评估器在所有维度上RMSE最低（Table 6）。
- **人类一致性A@1**：$\mathsf{A@1} = \frac{1}{N} \sum_{i=1}^N \mathbb{I}(|x_{i,d}^M - x_{i,d}^H| \leq 1)$，即模型评分与人类评分偏差不超过1分的样本比例。微调后的QwenVL平均A@1达到95.4%（Table 6）。



## 实验与关键发现

### 主结果：SEIR生成质量与SynJudge评估可靠性

**SEIR流水线的整体表现。** 在包含13个基线生成器的固定评估基准（4000个问题，含500个人工撰写与3500个SEIR生成问题）上，SEIR方法生成的InterSyn样本在文本内容完整性（TCC）、图像内容完整性（ICC）、图像质量（IQ）和图文协同性（ITS）四个维度上均取得了最高平均分，且方差最低（低于0.61）。以人类评估为例，SEIR的TCC为4.41（方差0.55），ITS为4.51（方差0.57），全面超越GPT-4o+DALL-E3（TCC 4.32，ITS 4.39）等强基线（Table 5）。这一结果的核心瓶颈在于：现有模型受限于数据质量与指令多样性不足，而SEIR通过三级精炼循环（QR→AR→IR）系统性地提升了输出质量。

![[assets/figures/papers/iclr26_0003_qBORZkk28r_A_High_Quality_Dataset_and_Reliable_Evaluation_f/figures/008_Table_5.jpg]]
*Table 5: Generator performance evaluated by human judge and SynJudge. Each entry is reported as mean (variance), where the value outside the parentheses denotes the mean score and the value inside the parentheses denotes the variance*

**数据效率与可扩展性。** 在Anole和VILA-U上使用InterSyn子集进行微调，仅25K-50K样本即可带来显著性能提升，且扩展到200K时TCC、ICC和ITS持续改善（Table 1）。例如，Anole的TCC从基线3.09提升至200K时的3.64（+0.55），ITS从2.26提升至3.11（+0.85）；VILA-U的TCC从2.46提升至3.52（+1.06），ITS从2.19提升至3.33（+1.14）。这一结果揭示了因果机制：数据密度比原始规模更重要——高质量、指令丰富的样本能更有效地激活模型的图文协同能力。此外，50K微调后，模型在MME-P、MMBench、MMMU、SEEDBench等通用理解基准上的性能未出现退化（Table 2），表明InterSyn的训练不会牺牲基础能力。

![[assets/figures/papers/iclr26_0003_qBORZkk28r_A_High_Quality_Dataset_and_Reliable_Evaluation_f/figures/003_Table_1.jpg]]
*Table 1: Fine-tuning results on varying subset sizes of InterSyn. Performance consistently improves as training data scales from 25K to 200K samples, demonstrating the dataset’s effectiveness and scalability. Notably, just 50K samples yield substantial gains across all models, with continued improvement in content and synergy metrics (TCC, ICC, ITS) at larger scales. All scores are SynJudge means*

![[assets/figures/papers/iclr26_0003_qBORZkk28r_A_High_Quality_Dataset_and_Reliable_Evaluation_f/figures/004_Table_2.jpg]]
*Table 2: Understanding performance after 50k InterSyn fine-tuning. Values in parentheses denote the change (∆) from the base*

**多轮对话数据的效果。** 多轮训练能有效减缓后续轮次的性能下降，尤其对ITS指标（Table 3）。例如，Anole在仅使用50K多轮数据训练时，第3轮ITS为2.25，而仅使用50K单轮数据时第3轮ITS仅为2.05（下降0.20）。这表明多轮数据的关键作用在于维持对话中图文协同的连贯性，避免长程交互中的质量衰减。

![[assets/figures/papers/iclr26_0003_qBORZkk28r_A_High_Quality_Dataset_and_Reliable_Evaluation_f/figures/005_Table_3.jpg]]
*Table 3: Effectiveness of multi-turn data on conversational performance across across different dialogue test turns. Models are trained on different proportions of single-turn and multi-turn data*

### 消融实验：SEIR各组件的贡献

**问题精炼（QR）的迭代效应。** QR在前三次迭代中质量显著提升，之后趋于平稳（Figure 3）。该模式表明：有限的迭代次数（3轮）足以充分优化问题质量，过度迭代的边际收益递减。这构成了SEIR流水线的效率瓶颈——在保证质量的前提下，应控制迭代次数以避免计算浪费。

**答案精炼（AR）与图像精炼（IR）的协同作用。** 消融实验（Table 4）显示：AR单独提升TCC、ICC和ITS；IR在此基础上进一步提升ICC和ITS，但对TCC影响较小。具体而言，AR=3且IR=3时，TCC达4.42，ICC达4.43，IQ达4.39，ITS达4.46。这一因果链表明：AR负责文本内容的完整性与准确性，IR则专注于图像内容与图文协同的优化。两者互补，缺一不可。

![[assets/figures/papers/iclr26_0003_qBORZkk28r_A_High_Quality_Dataset_and_Reliable_Evaluation_f/figures/007_Table_4.jpg]]
*Table 4: Impact of answer refinement (AR) and image refinement (IR) on answer quality. The table reports human evaluation mean scores across four dimensions (TCC, ICC, IQ, ITS). AR improves TCC, ICC, and ITS, while IR further enhances ICC and ITS, confirming the effectiveness of iterative refinement*

**SEIR对低性能模型的提升效果更显著。** 在SEIR优化前后对比（Table 8）中，InternLM+QwenVL配置的TCC从3.66提升至4.26（+0.60），ITS从3.68提升至4.38（+0.70），提升幅度远超高性能组合（如GPT-4o+DALL-E3的TCC仅提升+0.08）。更重要的是，SEIR缩小了开源模型与闭源模型之间的差距：Qwen+InternVL+Flux的SEIR版本（TCC 4.42，ITS 4.51）与GPT-4o+DALL-E3的SEIR版本（TCC 4.44，ITS 4.54）差距小于0.03。这意味着SEIR流水线本身是一种有效的“质量均衡器”，能补偿基础模型能力的不足。

### 评估器对比：SynJudge与人类判断的对齐

**微调MLLM评估器的优势。** 在48K人工标注样本上微调QwenVL后，SynJudge与人类判断的对齐最强：平均A@1达95.4%，且在各维度上的RMSE均最低（TCC 0.54，ICC 0.72，IQ 0.68，ITS 0.67）（Table 6）。相比之下，零样本GPT-4o的A@1仅为79.7%，RMSE在0.79-1.02之间。这一对比的关键瓶颈在于：零样本MLLM缺乏对交错图文生成任务的细粒度理解，而微调后的评估器能学习到人类偏好的评分模式。

![[assets/figures/papers/iclr26_0003_qBORZkk28r_A_High_Quality_Dataset_and_Reliable_Evaluation_f/figures/010_Table_6.jpg]]
*Table 6: Judge performance comparison. We report average RMSE (lower is better) and Human Agreement (A@1, higher is better) against human scores. The best result in each row is highlighted in bold. QwenVL trained demonstrates the strongest alignment*

**图文协同（ITS）是最具区分度的维度。** 在所有评估器中，ITS维度的RMSE普遍高于其他维度（Table 6的附录数据），且ITS的评分方差也较大（Table 5）。这表明ITS是评估交错图文生成质量的关键瓶颈——传统图文一致性指标无法捕捉互补性，而ITS奖励的是“图文互补而非冗余”，这正是当前模型最薄弱的环节。

### 失败模式与局限性

**图像视觉保真度的上限。** 生成图像的视觉质量受限于当前文生图模型的能力上限。对于细粒度或专业主题（如医学影像、机械图纸），SEIR生成的图像可能不够精确。这一瓶颈在IQ维度上体现为：即使经过IR精炼，IQ分数仍低于TCC和ITS（Table 4中IQ为4.39，而TCC为4.42，ITS为4.46）。

**单图像限制。** 当前InterSyn设计为每轮对话一张图像，简化了建模过程，但偏离了需要同时理解或生成多张图像的真实场景（如比较推理、步骤说明、空间推理）。这一限制意味着：模型在需要多图像上下文的任务上可能表现不佳，而SynJudge目前也未设计用于多图像评估。

**评估器对细微语义不匹配的敏感性。** 尽管SynJudge与人类判断的对齐度很高，但在检测人类可能捕捉到的细微语义不匹配方面仍存在局限性。例如，当图像内容与文本描述在细节上存在微妙差异时，SynJudge可能无法完全捕捉（Table 10-14的差距比例分布显示，仍有少量样本的评分偏差超过1分）。这一点需要进一步的人工验证。



## 定位与知识库关联

**与现有数据集的关系。** InterSyn 在交错图文生成领域填补了一个关键空白。对比现有数据集：MMC4（101.2M 文档）和 OBELICS（141M 页面）虽规模巨大，但均为网页爬取文档，缺乏指令跟随性和多轮对话结构，噪声高且质量不稳定；CoMM 和 LeafInstruct 等数据集规模有限（通常不超过数万样本），且依赖对现有语料的过滤或复用，缺乏标准化的质量控制机制。InterSyn 是首个同时具备大规模（1.8M 单轮样本 + 50K 多轮对话）、指令跟随性和多轮对话能力的交错图文生成数据集（Table 7）。其核心差异在于：不是从现有数据中筛选，而是通过 SEIR 流水线主动生成高质量样本。

**与现有评估基准的关系。** 在评估维度上，现有基准（如 InterleavedBench、OpenING）通常仅关注图文一致性或表面正确性，缺乏对图文协同性（ITS）的细粒度定量评估。SynJudge 引入的四维评估（TCC、ICC、IQ、ITS）将 ITS 作为关键维度，奖励图文之间的互补性而非冗余性——这是一个重要的评估范式转变。在评估器与人类对齐程度上，零样本 MLLM 评估器（如 GPT-4o、InternVL）与人类判断偏差大，而 SynJudge 通过在 48K 人工标注样本上微调 QwenVL，将平均 A@1 提升至 95.4%，RMSE 降至最低（Table 6），显著缩小了自动评估与人工评估之间的差距。

**适用边界与因果机制。** InterSyn + SEIR 方案的有效性依赖于三个因果环节：1）**数据密度优于数据规模**：仅 25K-50K 高质量样本即可带来显著性能提升（Table 1），说明当前模型的瓶颈不在于数据量不足，而在于数据质量不稳定和指令多样性匮乏；2）**迭代精炼的边际收益递减**：QR 在前三次迭代中质量显著提升，之后趋于平稳（Figure 3），AR 和 IR 也呈现类似规律（Table 9），这意味着 3 次迭代是成本-效益的最优平衡点；3）**SEIR 缩小开源-闭源差距**：SEIR 优化后，Qwen+InternVL+Flux 的 TCC（4.42）和 ITS（4.51）与 GPT-4o+DALL-E3（4.44/4.54）的差距小于 0.03（Table 8），表明数据质量提升对低性能模型组合的边际收益更高。

**局限与开放问题。** 当前方案存在三个明确边界：1）**单图像约束**：每轮对话仅生成一张图像，简化了建模但偏离了需要多图像比较推理、步骤说明或空间推理的真实场景；2）**视觉保真度天花板**：生成图像质量受限于当前文生图模型的上限，对细粒度或专业主题的表达可能不够精确；3）**评估器覆盖范围**：SynJudge 目前仅设计用于单图像响应评估，未捕捉多图像上下文带来的额外复杂性和多模态依赖。开放问题包括：SEIR 流水线能否扩展到更大规模或更复杂的交错任务？SynJudge 能否适应视频-文本交错生成等其他多模态领域？多图像评估的 SynJudge 扩展方案应如何设计？这些问题的答案需要手动验证，因为当前论文未提供相关实验证据。



## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/A_High_Quality_Dataset_and_Reliable_Evaluation_for_Interleaved_Image_Text_Generation.pdf

![[paperPDFs/ICLR_2026/A_High_Quality_Dataset_and_Reliable_Evaluation_for_Interleaved_Image_Text_Generation.pdf]]
