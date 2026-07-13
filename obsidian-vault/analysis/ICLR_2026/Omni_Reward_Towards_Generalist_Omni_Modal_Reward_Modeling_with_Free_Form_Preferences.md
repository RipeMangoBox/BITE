---
title: "Omni-Reward: Towards Generalist Omni-Modal Reward Modeling with Free-Form Preferences"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Omni_Reward_Towards_Generalist_Omni_Modal_Reward_Modeling_with_Free_Form_Preferences.pdf
project_link: https://hf.co/datasets/HongbangYuan/OmniRewardBench
code_link: https://github.com/HongbangYuan/OmniReward
openreview_forum_id: 9C4gVbPqSy
aliases:
- Omni-Reward
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "通过构建覆盖文本、图像、视频、音频与3D的全模态基准（Omni-RewardBench）并引入自由形式偏好指令微调，使奖励模型能够动态适应多种评估标准，从而缓解模态不平衡和偏好刚性。"
primary_logic: "将奖励模型从单一模态和固定偏好扩展至全模态自由形式偏好，结合大规模多样化偏好数据与指令微调，可显著提升模型在多样化任务上的泛化性，并在不牺牲可解释性的前提下与商业模型性能相媲美。"
claims:
- "Omni-RewardModel-BT在Omni-RewardBench上取得w/o Ties 73.68%和w/ Ties 65.36%的准确率，超过所有开源模型和多数商业模型。"
- "Omni-RewardModel在VL-RewardBench上以76.3%准确率取得SOTA，超越此前最佳模型Skywork-VL-Reward的73.1%。"
- "Omni-RewardBench 上 Accuracy w/ Ties = 65.36 (Omni-RewardModel-BT)"
- "VL-RewardBench 上 Overall Accuracy = 76.3 (Omni-RewardModel-BT)"
---

# Omni-Reward: Towards Generalist Omni-Modal Reward Modeling with Free-Form Preferences

> [!tip] 核心洞察
> 将奖励模型从单一模态和固定偏好扩展至全模态自由形式偏好，结合大规模多样化偏好数据与指令微调，可显著提升模型在多样化任务上的泛化性，并在不牺牲可解释性的前提下与商业模型性能相媲美。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Omni-Reward：面向自由形式偏好的通用全模态奖励建模 |
| 英文题名 | Omni-Reward: Towards Generalist Omni-Modal Reward Modeling with Free-Form Preferences |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=9C4gVbPqSy) · [GitHub](https://github.com/HongbangYuan/OmniReward) · [Project](https://hf.co/datasets/HongbangYuan/OmniRewardBench) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | Omni-Reward |
| Dataset | Omni-RewardBench, VL-RewardBench |

> [!tip] 效果简介
> - Omni-RewardBench 上，Accuracy w/ Ties 为 65.36 (Omni-RewardModel-BT)，对比 66.54 (Claude 3.5 Sonnet)，变化 -1.18。
> - VL-RewardBench 上，Overall Accuracy 为 76.3 (Omni-RewardModel-BT)，对比 73.1 (Skywork-VL-Reward)，变化 +3.2。

## 概要

**核心问题**：当前多模态奖励模型（Reward Model, RM）普遍存在两个结构性瓶颈——**模态不平衡**与**偏好刚性**。绝大多数RM仅覆盖文本和图像模态，对视频、音频、3D等模态支持严重不足；同时，训练范式依赖固定的二元偏好对，无法捕捉用户个性化、细粒度的评估需求。

**方法定位**：Omni-Reward 从三个层面系统性地回应上述瓶颈：（1）构建首个覆盖文本、图像、视频、音频、3D五大模态的**全模态基准 Omni-RewardBench**（3,725组人工标注偏好对，涵盖9类任务）；（2）构建包含248K通用偏好对与69K指令微调对的**Omni-RewardData**，引入自由形式偏好描述；（3）提出**Omni-RewardModel**，同时训练判别式RM（Bradley-Terry损失）与生成式RM（GRPO强化学习），使模型能根据动态评估标准灵活打分。

**核心结论**：Omni-RewardModel-BT 在 Omni-RewardBench 的 w/o Ties 设置下达到 **73.68%** 准确率，w/ Ties 设置下达到 **65.36%**，超越所有开源模型，与最强商业模型 Claude 3.5 Sonnet（66.54%）差距仅1.18个百分点。在 VL-RewardBench 上以 **76.3%** 取得 SOTA，超越此前最佳模型 Skywork-VL-Reward（73.1%）。消融实验证实，自由形式指令微调数据与全模态混合训练是性能增益的关键驱动因素。

**主要局限**：音频生成（T2A准确率44.77%）与3D生成（T23D准确率39.40%）任务性能显著偏低，模态不平衡问题未完全解决；指令微调数据完全由GPT-4o生成，尽管经过多模型验证过滤，仍可能存在未被检测的偏差。



### 问题背景

大型多模态模型（LMMs）的快速发展使其在文本、图像、视频、音频乃至3D内容生成等任务上展现出强大能力。然而，将这些模型的输出与人类偏好对齐仍高度依赖奖励模型（Reward Model, RM）。一个理想的奖励模型应当能够：**跨模态**地理解多样化内容，并**灵活适应**不同用户细粒度的评价标准。

### 现有方法的双重瓶颈

当前奖励建模面临两个相互交织的核心瓶颈：

**模态不平衡**。主流奖励模型——无论是**GPT-4o**（OpenAI, 2024）、**Claude 3.5 Sonnet**（Anthropic, 2024b）等商业生成式RM，还是**UnifiedReward**（Wang et al., 2025b）、**Skywork-VL-Reward**（Zang et al., 2025a）等专用判别式RM——其训练和评估主要集中在文本和图像模态。对视频、音频、3D等模态的支持严重不足，导致在这些弱势模态上的评估能力显著退化。证据显示，即使Omni-Reward自身在音频生成（T2A）和3D生成（T23D）任务上的准确率也仅分别为44.77%和39.40%，模态不平衡远未解决。

**偏好刚性**。现有奖励模型通常采用固定二元偏好对（chosen vs. rejected）进行训练，这隐含假设所有用户共享同一套评价标准。然而，真实场景中偏好高度个性化——同一对响应在不同评价维度（如“创造性”vs.“准确性”）下可能得出截然相反的偏好判断。固定偏好格式无法捕捉这种多样性，限制了RM在开放场景下的泛化能力。

### 本文动机

针对上述瓶颈，Omni-Reward提出两个关键转向：

1. **从双模态到全模态**：构建覆盖文本、图像、视频、音频、3D五类模态的统一评估与训练框架，使奖励模型具备跨模态的通用评估能力。
2. **从固定偏好到自由形式偏好**：引入自由形式偏好描述（free-form preference descriptions）作为条件输入，使RM能够根据用户指定的任意评价标准动态调整判断，从而缓解偏好刚性。

这一设计将奖励建模从“单一模态+固定标准”的封闭范式推向“全模态+动态标准”的开放范式，目标是实现一个通用全模态奖励模型（generalist omni-modal reward model），在不牺牲可解释性的前提下，使开源模型性能接近甚至匹敌商业闭源方案。



## 核心方法与创新机理

Omni-Reward 的核心创新在于从**模态覆盖**和**偏好表达**两个维度同时突破现有奖励模型的瓶颈，构建了一个面向全模态、支持自由形式偏好的通用奖励建模框架。

### 1. 从固定二元偏好到自由形式偏好指令

现有奖励模型（如 **UnifiedReward** (Wang et al., 2025b)、**Skywork-VL-Reward** (Zang et al., 2025a)）通常采用固定的二元偏好对进行训练，即模型仅学习在给定的两个响应中判断孰优孰劣。这种训练范式存在**偏好刚性**问题：模型无法捕捉用户评价标准的多样性——同一对响应在不同评价维度下（如“准确性”、“简洁性”、“创造性”）可能有完全相反的偏好结论。

Omni-Reward 将偏好格式从固定二元对扩展为**自由形式偏好描述与指令微调**。具体而言，每个数据样本表示为 $(x, y_1, y_2, c, p)$，其中 $c$ 是自由形式的评价标准（如“Which response provides more accurate factual information?”），$p$ 为基于该标准的偏好标签。Omni-RewardData 包含 248K 通用偏好对和 69K 专门收集的指令微调对，使模型能够动态适应多种评估标准，从根本上缓解偏好刚性问题。

消融实验证实了这一创新的关键作用：移除指令微调数据导致 Omni-RewardBench 上性能明显下降。

### 2. 从文本-图像到全模态覆盖

现有奖励模型主要聚焦于文本和图像模态，对视频、音频、3D 等模态支持有限，存在严重的**模态不平衡**问题。Omni-Reward 将模态覆盖扩展至全模态（文本、图像、视频、音频、3D），并通过构建 Omni-RewardBench 提供统一的评估基准。该基准包含 3,725 个高质量人工标注的偏好对，覆盖 9 个不同任务，横跨五种模态。

这一扩展并非简单的模态堆叠。消融实验表明，同时使用混合多模态数据的全部训练集在 Omni-RewardBench w/ Ties 设置下达到 65.36% 整体准确率，优于单一模态训练，验证了跨模态联合训练的有效性。

### 3. 训练目标的差异化设计

与直接使用多模态语言模型通过提示生成评分的做法（如 **GPT-4o** (OpenAI, 2024)、**Claude 3.5 Sonnet** (Anthropic, 2024b)）不同，Omni-Reward 针对不同应用场景设计了两种训练范式：

- **判别式 RM（Omni-RewardModel-BT）**：采用 Bradley-Terry 损失进行训练，冻结视觉编码器和音频编码器参数，仅更新语言模型解码器和 Value Head，输出标量奖励分数。损失函数为：

$$\mathcal{L}_{\mathrm{BT}} = -\log \frac{\exp(r_{\mathrm{BT}}(c, x, y_c))}{\exp(r_{\mathrm{BT}}(c, x, y_c)) + \exp(r_{\mathrm{BT}}(c, x, y_r))}$$

- **生成式 RM（Omni-RewardModel-R1）**：基于 GRPO 强化学习进行优化，模型首先生成思维链解释，再输出偏好决策，仅使用 3% 的训练数据。

这种双轨设计使 Omni-Reward 在判别式精确评分和生成式可解释推理之间取得平衡。在 Omni-RewardBench w/ Ties 设置下，Omni-RewardModel-BT 以 65.36% 的准确率接近 **Claude 3.5 Sonnet** 的 66.54%，在 VL-RewardBench 上以 76.3% 超越此前 SOTA **Skywork-VL-Reward** 的 73.1%。

### 创新边界与局限

尽管上述创新显著提升了全模态奖励建模的性能，但模态不平衡问题并未完全解决：音频生成任务（T2A）准确率仅 44.77%，3D 生成任务（T23D）仅 39.40%，与文本、图像任务之间存在高达 28.37% 的性能差距。此外，指令微调数据完全由 GPT-4o 生成，尽管经过多模型验证流程（GPT-4o-mini、Qwen2.5-VL 7B、Gemma-3-12B-it）筛除不一致样本，仍可能引入未被发现的偏差。



![[assets/figures/papers/paper_list_l17_https_openreview_net_forum_id_9C4gVbPqSy/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the architecture of Omni-RewardModel*

Omni-Reward 旨在构建一个面向全模态自由形式偏好的通用奖励模型，其整体框架由三个核心组件构成：**基准构建（Omni-RewardBench）**、**数据构建（Omni-RewardData）** 与 **模型训练（Omni-RewardModel）**。三个组件形成闭环——基准定义评估标准，数据提供训练信号，模型则通过判别式与生成式两条路径学习将自由形式偏好映射为奖励信号。

### 数据流与模块关系

框架的输入是一个五元组 $(x, y_1, y_2, c, p)$，其中 $x$ 为输入提示，$y_1$ 和 $y_2$ 为两个候选响应，$c$ 为自由形式的用户偏好描述（即评估标准），$p$ 为偏好标签。这一表示贯穿基准构建与模型训练的全流程。

**Omni-RewardBench** 覆盖文本、图像、视频、音频和 3D 五种模态，包含 9 类任务（见图 1），提供两种评估设置：w/o Ties（排除平局）和 w/ Ties（包含平局），后者对模型的分辨能力要求更高。

**Omni-RewardData** 包含 248K 通用偏好对和 69K 带有自由形式偏好描述的指令微调对，为模型提供大规模、多样化的偏好信号。指令微调数据由 GPT-4o 生成，并通过多模型验证流程（GPT-4o-mini、Qwen2.5-VL 7B、Gemma-3-12B-it）筛除不一致样本，最终保留的标注数据 Krippendorff's alpha 为 0.701。

**Omni-RewardModel** 的架构如图 2 所示，由四个模块串联：

- **Vision Encoder** 与 **Audio Encoder**：分别处理图像/视频和音频输入，参数在训练中冻结。
- **Language Model Decoder**：接收多模态编码后的表示与自由形式偏好 $c$，作为核心推理模块，参数可训练。
- **Value Head**：仅在判别式 RM 中使用，将解码器输出映射为标量奖励分数。

模型按训练目标分为两个变体：
- **Omni-RewardModel-BT**（判别式）：在完整 Omni-RewardData 上使用 Bradley-Terry 损失训练，损失函数为

$$\mathcal{L}_{\mathrm{BT}} = -\log \frac{\exp(r_{\mathrm{BT}}(c, x, y_c))}{\exp(r_{\mathrm{BT}}(c, x, y_c)) + \exp(r_{\mathrm{BT}}(c, x, y_r))}$$

其中 $r_{\mathrm{BT}}(c, x, y)$ 表示在偏好 $c$ 下对响应 $y$ 的奖励分数，$y_c$ 和 $y_r$ 分别为选定响应与拒绝响应。

- **Omni-RewardModel-R1**（生成式）：仅使用 3% 的 Omni-RewardData（约 10K 样本），基于 GRPO 强化学习从零训练，以 Qwen2.5-VL-7B-Instruct 为基础模型。给定输入 $(c, x, y_1, y_2)$，模型首先生成思维链解释 $e$，再输出偏好决策，无需大型模型蒸馏。

### 关键设计决策

框架的核心设计在于将“自由形式偏好指令微调”作为连接多模态输入与奖励信号的桥梁。消融实验表明，移除指令微调数据会导致 Omni-RewardBench 上性能明显下降；同时使用混合多模态数据的全量训练（65.36% w/ Ties 准确率）优于单一模态训练，验证了跨模态联合训练的必要性。

该框架的瓶颈在于弱势模态（音频、3D）的性能仍显著偏低——T2A 准确率仅 44.77%，T23D 为 39.40%，模态不平衡问题未完全解决。此外，指令微调数据完全由 GPT-4o 生成，尽管经过多模型验证，仍可能引入未被发现的偏差。



### 架构总览

Omni-RewardModel 的整体架构如图 Figure 2 所示，由四个核心模块构成：

- **Vision Encoder**：处理图像与视频输入，训练时参数冻结。
- **Audio Encoder**：处理音频输入，训练时参数冻结。
- **Language Model Decoder**：接收多模态输入与用户自由形式偏好条件 $c$，作为模型训练中唯一更新的语言解码器。
- **Value Head**：位于解码器输出端，为判别式奖励模型输出标量奖励分数。

训练策略上，视觉编码器与音频编码器保持冻结，仅更新语言模型解码器与 Value Head 的参数。

### 判别式奖励模型与 Bradley-Terry 损失

对于判别式奖励模型 **Omni-RewardModel-BT**，训练目标采用经典的 Bradley-Terry 损失函数。给定用户偏好条件 $c$、输入提示 $x$，以及选定响应 $y_c$ 与拒绝响应 $y_r$，损失定义为：

$$\mathcal{L}_{\mathrm{BT}} = -\log \frac{\exp(r_{\mathrm{BT}}(c, x, y_c))}{\exp(r_{\mathrm{BT}}(c, x, y_c)) + \exp(r_{\mathrm{BT}}(c, x, y_r))}$$

其中 $r_{\mathrm{BT}}(c, x, y)$ 表示模型对给定偏好条件与输入下候选响应的标量奖励估计。该损失通过最大化选定响应相对于拒绝响应的得分概率，驱动模型学习符合自由形式偏好的排序能力。

### 生成式奖励模型与 GRPO 强化学习

生成式奖励模型 **Omni-RewardModel-R1** 采用成对评估格式：给定输入 $(c, x, y_1, y_2)$，模型首先生成思维链解释 $e$，随后输出偏好决策。训练采用基于 GRPO 的强化学习优化策略，从 Omni-RewardData 中仅抽取 10K 样本从头训练，基座模型为 Qwen2.5-VL-7B-Instruct（Bai et al., 2025），不依赖大模型蒸馏。

### 数据样本表示

Omni-RewardBench 中每个偏好样本统一表示为五元组：

$$(x, y_1, y_2, c, p)$$

- $x$：输入提示；
- $y_1, y_2$：两个候选响应；
- $c$：自由形式的评价标准（用户偏好描述）；
- $p$：偏好标签，在 w/o Ties 设定下取值为 $\{y_1, y_2\}$，在 w/ Ties 设定下扩展为 $\{y_1, y_2, \text{tie}\}$。

这一表示将固定二元偏好对泛化为可动态适应的自由形式偏好条件，是模型实现偏好灵活性的结构基础。



## 实验与关键发现

### 主实验结果

Omni-RewardModel-BT 在两个核心基准上展现了领先性能。在 Omni-RewardBench 的 w/o Ties 设置下，模型取得 **73.68%** 的准确率；在更具挑战性的 w/ Ties 设置下，准确率为 **65.36%**（见 Table 1）。这一结果超越了所有开源模型，仅以 1.18 个百分点的差距落后于表现最强的商业模型 **Claude 3.5 Sonnet**（Anthropic, 2024b）的 66.54%。相比之下，同为专用奖励模型的 **UnifiedReward**（Wang et al., 2025b）在该设置下仅取得 59.69%，差距显著。

![[assets/figures/papers/paper_list_l17_https_openreview_net_forum_id_9C4gVbPqSy/figures/003_Table_1.jpg]]
*Table 1: Evaluation results on Omni-RewardBench under the w/ Tie setting*

在视觉语言奖励建模的外部基准 VL-RewardBench 上，Omni-RewardModel-BT 以 **76.3%** 的整体准确率取得 SOTA，较此前最佳模型 **Skywork-VL-Reward**（Zang et al., 2025a）的 73.1% 提升了 3.2 个百分点（见 Table 2）。这一跨基准的优势表明，全模态训练与自由形式偏好指令微调不仅没有损害模型在特定模态上的判别力，反而带来了正向迁移。

![[assets/figures/papers/paper_list_l17_https_openreview_net_forum_id_9C4gVbPqSy/figures/004_Table_2.jpg]]
*Table 2: Evaluation results on VL-RewardBench*

Figure 6 的雷达图揭示了任务级性能的显著差异：模型在不同任务间的准确率最大差距达 **28.37%**，其中文本到文本（T2T）和文本-图像到文本（TI2T）等成熟模态任务表现强劲，而文本到音频（T2A，44.77%）和文本到 3D（T23D，39.40%）等弱势模态任务则构成主要瓶颈。

### 消融实验

Table 3 报告了在 Omni-RewardBench w/ Ties 设置下的消融结果，揭示了两个关键因素的作用机制：

![[assets/figures/papers/paper_list_l17_https_openreview_net_forum_id_9C4gVbPqSy/figures/005_Table_3.jpg]]
*Table 3: Ablation results on Omni-RewardBench under the w/ Tie setting. achieves SOTA performance on VL-RewardBench, with an accuracy of 76.3%. On Multimodal RewardBench (Table 9), Omni-RewardModel also matches the performance of Claude 3.5 Sonnet*

**指令微调数据的必要性。** 移除指令微调数据后，模型性能出现明显下降。这一发现验证了自由形式偏好描述对于模型理解多样化评估标准的核心作用——仅靠传统的二元偏好对无法充分捕捉用户意图的丰富性。

**混合多模态数据的互补效应。** 为分离模态混合的贡献，研究团队以 MiniCPM-o-2.6 为基础，分别使用单一模态数据（T2T、TI2T、T2I/T2V）和混合多模态数据进行训练。结果显示，使用全量混合数据训练的模型达到 65.36% 的整体准确率，优于任一单一模态训练方案。这表明不同模态的偏好数据之间存在互补性，联合训练有助于模型习得更通用的奖励建模能力。

**生成式 RM 的数据效率瓶颈。** Omni-RewardModel-R1 仅使用 Omni-RewardData 中 3% 的样本（约 10K）进行 GRPO 强化学习训练，在 w/ Ties 设置下整体准确率为 60.18%。虽然这一结果在生成式 RM 中已具竞争力，但与全量数据训练的判别式版本相比仍有明显差距，暴露出生成式 RM 在有限数据下的性能瓶颈。

### 模态不平衡与失败模式

尽管 Omni-Reward 在全模态覆盖上取得了突破，模态不平衡问题仍未根本解决。T2A 任务的 44.77% 准确率和 T23D 任务的 39.40% 准确率远低于整体平均水平，构成两个明确的失败模式。这一现象的成因可能是多方面的：音频和 3D 生成的评估本身具有更高的主观性和细粒度要求；相应模态的偏好数据规模和标注质量可能不及文本和图像模态；底层视觉编码器和音频编码器在训练中被冻结，限制了模型在这些模态上的适应能力。

### 思维链推理的影响

Figure 7 分析了思维链推理对生成式 RM 性能的影响。结果表明，引入 CoT 推理后，模型在多数任务上的准确率有所提升，尤其是在需要复杂推理的 TI2T 和 T2I 任务上。但 CoT 并非在所有场景下都带来正向收益——在部分任务上，直接输出偏好判断反而更为准确，这可能与 CoT 生成过程中的推理偏差或幻觉有关。

### 外部基准泛化验证

除 VL-RewardBench 外，Omni-RewardModel 在 Multimodal RewardBench（Table 9）上也展现出与 Claude 3.5 Sonnet 相当的判别能力，进一步佐证了模型在跨基准泛化上的稳健性。这一结果尤其值得注意，因为 Multimodal RewardBench 的评估维度与训练数据分布并不完全重叠，模型的强泛化表现归因于自由形式偏好指令微调赋予的动态适应能力。

![[assets/figures/papers/paper_list_l17_https_openreview_net_forum_id_9C4gVbPqSy/figures/016_Table_9.jpg]]
*Table 9: Evaluation results on Multimodal RewardBench*

### 补充图表

![[assets/figures/papers/paper_list_l17_https_openreview_net_forum_id_9C4gVbPqSy/figures/009_Table_4.jpg]]
*Table 4: The comparison between Omni-RewardBench and other reward modeling benchmarks*

![[assets/figures/papers/paper_list_l17_https_openreview_net_forum_id_9C4gVbPqSy/figures/010_Table_5.jpg]]
*Table 5: Data statistics of Omni-RewardBench. The Avg. #Tokens (Prompt), Avg. #Tokens (Response), and Avg. #Tokens (Criteria) columns report the average number of tokens in the prompt, model-generated response, and human-written evaluation criteria, respectively, all measured using the tokenizer of Qwen2.5-VL-7B-Instruct. The Prompt Source column specifies where the prompts were collected from, while the Model column identifies which models were used to produce the corresponding responses. The letters “V”, “I”, “A”, and “D” in the table stand for Video, Image, Audio, and 3D content, respectively*

![[assets/figures/papers/paper_list_l17_https_openreview_net_forum_id_9C4gVbPqSy/figures/011_Table_6.jpg]]
*Table 6: Statistics of free-form criteria per preference pair in Omni-RewardBench*

![[assets/figures/papers/paper_list_l17_https_openreview_net_forum_id_9C4gVbPqSy/figures/012_Table_7.jpg]]
*Table 7: Data statistics of Omni-RewardData. * denotes the subset constructed in this work*

![[assets/figures/papers/paper_list_l17_https_openreview_net_forum_id_9C4gVbPqSy/figures/015_Table_8.jpg]]
*Table 8: Evaluation results on Omni-RewardBench under the w/o Tie setting*

![[assets/figures/papers/paper_list_l17_https_openreview_net_forum_id_9C4gVbPqSy/figures/018_Table_10.jpg]]
*Table 10: Ablation results on Omni-RewardBench under the w/o Tie setting*

![[assets/figures/papers/paper_list_l17_https_openreview_net_forum_id_9C4gVbPqSy/figures/019_Table_11.jpg]]
*Table 11: Overall performance of generative RMs under different scoring strategies*



## 定位与知识库关联

### 1. 与现有工作的关系

Omni-Reward 在奖励模型（Reward Model, RM）领域填补了**模态覆盖**与**偏好表达**两个维度的空白，其定位可通过与以下代表性工作的对比来理解：

- **模态覆盖的扩展**：现有专用 RM 大多聚焦于文本和图像模态。例如，**Skywork-VL-Reward**（Zang et al., 2025a）专注于视觉理解任务的奖励建模，在 VL-RewardBench 上取得 73.1% 的准确率；**UnifiedReward**（Wang et al., 2025b）则覆盖图像/视频的理解与生成任务。Omni-Reward 将模态边界进一步推至**视频、音频与 3D**，首次构建了覆盖五种模态的统一奖励建模框架。这一扩展并非简单的模态堆砌——消融实验表明，混合多模态数据联合训练（Omni-RewardBench w/ Ties 整体准确率 65.36%）显著优于单一模态训练，验证了跨模态知识迁移的收益。

- **偏好格式的革新**：传统 RM（包括上述专用模型及多数基于 Bradley-Terry 损失的判别式 RM）依赖**固定二元偏好对**进行训练，即模型仅需判断“哪个响应更好”。这种范式无法捕捉用户偏好的多样性——例如，同一对响应在不同评价标准下（“简洁性” vs. “创造性”）可能得出相反的偏好结论。Omni-Reward 引入**自由形式偏好描述与指令微调**，将评价标准 $c$ 显式地编码为自然语言指令，使模型能够动态适应多种评估维度。这一设计与**GPT-4o**（OpenAI, 2024）和**Claude 3.5 Sonnet**（Anthropic, 2024b）等商业生成式 RM 的思路相近，但 Omni-Reward 将其系统化并开源，且在判别式框架下实现了可比的性能。

- **与通用视觉语言模型的对比**：**Qwen2.5-VL-72B-Instruct**（Bai et al., 2025）等大型视觉语言模型可通过提示工程充当生成式 RM，但缺乏针对奖励建模任务的专门优化。Omni-RewardModel 通过 Bradley-Terry 损失或 GRPO 强化学习进行专门训练，在 Omni-RewardBench 上显著超越同级别的通用模型，证明了**任务专用训练**的必要性。

### 2. 适用边界

Omni-Reward 的适用性受以下因素约束：

- **模态覆盖的盲区**：尽管 Omni-RewardBench 覆盖文本、图像、视频、音频和 3D 五种模态，但基准仅包含 9 个任务，无法涵盖所有现实世界中的交互模态。例如，**具身智能**中的触觉反馈、**多模态交互**中的实时传感器数据流等场景尚未被纳入。在这些场景中，Omni-RewardModel 的性能缺乏实证支持。

- **弱势模态的性能瓶颈**：即使在全模态联合训练下，音频与 3D 生成任务的性能仍然较低——文本到音频（T2A）任务准确率仅 44.77%，文本到 3D（T23D）任务仅 39.40%（Omni-RewardBench w/ Ties 设置）。这表明**模态不平衡问题**并未完全解决，模型在稀疏训练数据的模态上泛化能力有限。

- **生成式 RM 的数据效率**：Omni-RewardModel-R1（生成式 RM）仅使用 3% 的训练数据（约 10K 样本），在 Omni-RewardBench 上取得 60.18% 的整体准确率，明显弱于全量训练的判别式版本（65.36%）。这表明当前生成式 RM 的训练范式在**低数据场景**下效率不足，距离实用化仍有差距。

### 3. 局限与开放问题

**已识别的局限**：

1. **指令微调数据的偏差风险**：Omni-RewardData 中的 69K 指令微调偏好对完全由 GPT-4o 生成。尽管作者采用了多模型验证流程（GPT-4o-mini、Qwen2.5-VL 7B、Gemma-3-12B-it）筛除不一致样本，并移除了 38% 的标注数据（23% 因无效标准，15% 因标注分歧，Krippendorff's alpha = 0.701），但**模型生成的监督信号**仍可能引入未被发现的系统性偏差，例如对某些评价维度的过度偏好或对特定表达模式的隐式拟合。

2. **音频与 3D 模态的评估深度不足**：Omni-RewardBench 在音频和 3D 任务上的样本量及评价维度的丰富性均弱于文本和图像任务。当前的低准确率可能部分源于**基准本身的不完善**，而非模型能力的绝对上限。

3. **判别式与生成式 RM 的性能差距**：Omni-RewardModel-R1 在多个任务上的表现弱于 Omni-RewardModel-BT，且训练成本更高（需 GRPO 强化学习）。如何在保持生成式 RM 可解释性优势的同时缩小与判别式 RM 的性能差距，仍是未解决的问题。

**开放问题**：

- 如何进一步减轻音频、3D 等弱势模态的不平衡问题？是否需要**模态特定的架构设计**或**数据增强策略**？
- 能否设计更高效的训练方法（如课程学习、元学习），使生成式 RM 在有限数据下达到判别式 RM 的性能？
- 自由形式偏好如何拓展至更复杂的多模态交互场景（如具身智能中的物理约束、触觉反馈的质量评估）？
- 如何保证大规模自动生成指令微调数据的忠实度，避免噪声在训练过程中被放大？是否需要引入**对抗验证**或**人类反馈闭环**？

### 4. 知识库定位

Omni-Reward 的核心贡献在于**将奖励建模从“固定模态+固定偏好”的封闭范式推向“全模态+自由形式偏好”的开放范式**。其在方法谱系中的位置可概括为：

- **上游继承**：继承了 Bradley-Terry 损失（Bradley & Terry, 1952）和 GRPO 强化学习等成熟的 RM 训练框架，以及 Qwen2.5-VL 等多模态基础模型的编码器架构。
- **核心创新**：构建了首个覆盖五种模态的奖励建模基准（Omni-RewardBench）和大规模自由形式偏好数据集（Omni-RewardData），并通过指令微调使 RM 动态适应多样化的评价标准。
- **下游启示**：为多模态对齐（如 RLHF、DPO）提供了更通用的奖励信号源，也为研究跨模态偏好迁移和个性化奖励建模提供了实验平台。

对于后续工作，Omni-Reward 提供了两条可追踪的改进路径：（1）**提升弱势模态的性能**，通过数据增强或模态特定的架构设计缩小模态间差距；（2）**优化生成式 RM 的训练效率**，使可解释的奖励建模在低资源场景下更具竞争力。



## 原文 PDF

![[paperPDFs/ICLR_2026/Omni_Reward_Towards_Generalist_Omni_Modal_Reward_Modeling_with_Free_Form_Preferences.pdf]]
