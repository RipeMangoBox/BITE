---
title: "MedVR: Annotation-Free Medical Visual Reasoning via Agentic Reinforcement Learning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/MedVR_Annotation_Free_Medical_Visual_Reasoning_via_Agentic_Reinforcement_Learning.pdf
project_link: null
code_link: null
openreview_forum_id: cK35kNVm5r
aliases:
- MedVR
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/vision_models_multimodal
core_operator: "MedVR用熵引导视觉重定位和共识信用分配训练医学VLM主动调用视觉工具。"
primary_logic: "高不确定token触发多轨迹视觉探索，成功轨迹的共识掩码再为工具调用提供自监督奖励。"
claims:
- "MedVR无需中间定位标注，仅用答案正确性和轨迹共识学习视觉推理行为。"
- "EVR在高预测熵节点生成多样化视觉假设，缓解纯文本推理的视觉幻觉。"
- "CCA从成功轨迹聚合视觉足迹，为Zoom-in等工具调用分配细粒度奖励。"
---

# MedVR: Annotation-Free Medical Visual Reasoning via Agentic Reinforcement Learning

> [!tip] 核心洞察
> MedVR

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | MedVR: Annotation-Free Medical Visual Reasoning via Agentic Reinforcement Learning |
| 英文题名 | MedVR: Annotation-Free Medical Visual Reasoning via Agentic Reinforcement Learning |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=cK35kNVm5r) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal |
| Method |  |
| Dataset | |

> [!tip] 效果简介
> 本笔记的既有实验指标、对比结果与适用边界见“实验与关键发现”；本轮仅统一结构，不改写证据。

## 概要

医学视觉问答（Medical VQA）要求模型同时理解图像内容并进行专业推理。现有医学视觉语言模型（VLM）面临一个根本瓶颈：文本推理链缺乏与视觉证据的交互验证，导致模型在缺乏真实视觉监督时产生“视觉幻觉”——即推理过程看似合理，却与实际图像内容脱节。

针对这一问题，本文提出 **MedVR**，首个面向医学 VLM 的端到端强化学习框架，无需任何中间标注即可训练模型执行可验证的视觉推理。MedVR 的核心洞察在于：**利用模型自身的预测不确定性来驱动视觉探索，并通过轨迹间的一致性挖掘自监督信号**，从而在不依赖人工标注的条件下，让模型学会主动操纵图像、验证视觉假设。

框架包含两个关键机制：

- **熵引导视觉重定位（EVR）**：在推理过程中，根据模型逐 token 的预测熵检测不确定性，在高不确定性节点触发并行的视觉探索（如区域放大），生成多条备选推理轨迹。
- **共识信用分配（CCA）**：从成功轨迹中聚合视觉操作足迹，通过多数投票生成共识掩码，以此为每条轨迹的视觉操作提供细粒度奖励信号。

实验覆盖六项公开医学 VQA 基准，分为通用领域（OmniMedVQA、PMC-VQA、MedXpertQA）和模态专项（VQA-RAD、SLAKE、PathVQA）。MedVR 在多个基准上取得最优结果，且仅使用 36K 过滤后的 OmniMedVQA 数据训练，数据规模远小于依赖百万级专有数据的基线方法。消融实验证实，EVR 和 CCA 各自带来显著增益，二者协同使模型在零样本泛化和视觉定位精度（mIoU）上均大幅超越纯文本 RL 基线。

**方法定位**：MedVR 属于“RL + 工具使用”范式，区别于依赖人工推理链标注的监督微调方法和缺乏视觉交互的文本 RL 方法。其训练仅需问题-答案对作为终端奖励信号，视觉操作的监督完全由 CCA 从轨迹一致性中自动生成。



医学视觉问答（Medical VQA）要求模型同时理解视觉内容与医学知识，其核心挑战在于**视觉推理的可验证性**——模型不仅要给出答案，更需将其推理过程锚定在图像中的具体视觉证据上。然而，现有医学视觉语言模型（VLMs）面临一个根本性瓶颈：纯文本推理链缺乏视觉根基，容易产生视觉幻觉，即模型在未真正“看见”关键区域的情况下编造看似合理的推理。

这一瓶颈的深层原因在于**中间监督的缺失**。要让模型学会“看哪里”和“看什么”，传统方法需要昂贵的人工标注——边界框、分割掩码或逐步推理轨迹。医学图像的标注成本尤其高昂，需要专家知识，这严重制约了可扩展性。因此，现有医学VLMs大多停留在浅层视觉理解，无法自发地执行精细的视觉定位和工具使用。

本文的核心动机是打破这一“标注依赖—视觉推理能力”的僵局：**能否在不依赖任何中间标注的情况下，让医学VLM自主学会可验证的视觉推理？** 这需要一个框架，既能驱动模型主动探索图像中的关键区域，又能为这些探索行为提供自生成的监督信号。强化学习（RL）提供了端到端优化的可能性，但直接将RL应用于视觉推理面临双重挑战：如何设计有效的探索策略，以及如何在没有外部标注的情况下为视觉操作分配细粒度奖励。



## 核心方法与创新机理

MedVR 的核心创新在于构建了一套**无需中间标注的视觉推理强化学习框架**，使医学 VLM 能够通过工具使用主动验证视觉证据，而非依赖纯文本推理链。该框架围绕三个紧密协同的 changed slot 展开：

1. **推理范式转变：从文本推理到视觉‑工具推理**
   传统医学 VLM 的推理过程是“看图→文本链→答案”的单向流水线，模型在生成文本推理时并不回头检验图像。MedVR 将推理变为**文本推演与图像操作交替进行**的闭环：模型在生成推理 token 的过程中，可以动态调用 Zoom‑in 等视觉工具，对图像局部进行裁剪、放大和重新审视，将视觉证据直接嵌入推理链。这一改变消除了文本幻觉的根本成因——推理与视觉感知的脱节。

2. **探索策略：Entropy‑guided Visual Regrounding (EVR)**
   传统 RL 探索（如随机采样或固定温度采样）对视觉定位任务效率极低。EVR 的核心机制是**将 token 级预测熵作为视觉不确定性的代理信号**：当模型在决定“看哪里”的 token 上表现出高熵（即 $H_t = -\sum_j p_{t,j} \log p_{t,j}$ 升高），EVR 在该节点触发并行分支，生成多条探索不同视觉区域的轨迹。这一设计的因果逻辑是：高熵 token 对应模型对视觉定位决策缺乏信心，此时增加视觉探索的边际收益最大。EVR 将搜索复杂度从独立采样的 $O(n^2)$ 降至 $O(n \log n)$，同时实验证实 EVR 在训练过程中维持了更高且更稳定的策略熵（Figure 5），有效防止了策略过早坍缩。

3. **奖励机制：Consensus‑based Credit Assignment (CCA)**
   视觉工具调用缺乏 ground‑truth 标注，无法直接判断一次“看向某区域”是否正确。CCA 的解决方案是**从成功轨迹的共识中蒸馏伪监督**：对同一问题生成的多条轨迹中，筛选出答案正确的轨迹集合 $\mathcal{T}^+$，将其视觉操作足迹（如裁剪框）聚合为热力图，通过多数投票二值化得到共识掩码 $\hat{M}$。每条轨迹的工具调用奖励 $R_{\text{tool}}$ 取决于其操作足迹 $M_j$ 与 $\hat{M}$ 的 IoU 是否超过阈值 $\eta=0.5$。这一设计的精妙之处在于：它不需要任何人工标注的定位框，却能为视觉操作提供细粒度的逐步骤反馈信号。消融实验（Table 2）表明，CCA 对域内数据（OmniMedVQA）的提升最为显著（96.55 vs. 95.38），说明共识机制在训练分布内能更可靠地识别高质量视觉路径。

4. **复合奖励的稀疏性设计**
   总奖励 $R(T) = R_{\text{acc}} + R_{\text{format}} + \mathbb{1}(R_{\text{acc}} > 0) \cdot R_{\text{tool}}$ 采用条件激活策略：工具奖励仅在答案正确时才生效。这避免了模型学习“做很多视觉操作但答错”的投机行为，强制工具使用服务于最终答案的正确性，形成“正确答案→回溯奖励有效视觉行为”的因果链。

**与 baseline 的本质差异**：与 Lingshu‑7B、InternVL3‑14B 等依赖大规模标注数据和 SFT 的医学 VLM 不同，MedVR 仅使用 36K 过滤后的 OmniMedVQA 数据，通过 RL 从答案正确性这一终端信号中自主学习视觉定位能力，无需任何中间定位标注（Table 4）。这一 changed slot 使得 MedVR 在数据效率上具有根本性优势，同时避免了监督微调中常见的分布偏移问题。



![[assets/figures/papers/paper_list_l17_https_openreview_net_forum_id_cK35kNVm5r/figures/002_Figure_2.jpg]]
*Figure 2: Overview of MedVR. The framework employs EVR to explore visual actions based on the model’s intrinsic uncertainty and CCA to create a consensus-based reward from successful trajectories, enabling annotation-free training of medical visual reasoning*

MedVR 是一个端到端的强化学习框架，旨在为医学视觉语言模型赋予无需人工标注的视觉推理能力。其核心设计思路是让模型在生成文本推理链的同时，主动调用视觉工具对图像进行操作，从而将推理过程“锚定”在真实的视觉证据上，而非依赖可能产生幻觉的纯文本推断。

框架的整体工作流如下：给定一个医学图像 $I$ 和问题 $Q$，策略模型 $\pi_\theta$ 首先生成一段文本推理。当模型在生成过程中表现出较高的预测不确定性时，**Entropy-guided Visual Regrounding (EVR)** 模块被触发。EVR 利用当前步的 token 级熵 $H_t$ 作为不确定性信号，在推理树的该节点上并行生成多条视觉探索轨迹——每条轨迹包含不同的视觉工具调用（如缩放、裁剪等），从而形成一组多样化的视觉假设。

这些并行轨迹各自产生一个视觉操作足迹（即工具操作的空间掩码 $M_j$）和一个最终答案。框架根据答案正确性筛选出成功轨迹集合 $\mathcal{T}^+$，随后进入 **Consensus-based Credit Assignment (CCA)** 模块。CCA 将所有成功轨迹的视觉足迹聚合为一张热力图 $C = \sum_{\mathcal{T}_i \in \mathcal{T}^+} M_i$，并通过多数投票规则二值化，生成共识掩码 $\hat{M}$。该掩码代表了“多数成功轨迹共同关注的视觉区域”。

最后，CCA 为每条轨迹分配细粒度的工具奖励 $R_{\text{tool}}(T_j)$：若某条轨迹的视觉足迹与共识掩码的 IoU 超过阈值 $\eta$，则获得正向奖励，否则获得较低的奖励。这一奖励信号与答案正确性奖励 $R_{\text{acc}}$ 和格式惩罚 $R_{\text{format}}$ 组合成复合终端奖励 $R(T)$，通过 GRPO 算法回传以优化策略。

**模块间关系**：EVR 负责“探索”——在高不确定性节点上生成多样化的视觉搜索路径；CCA 负责“自监督”——从成功轨迹的共识中提炼出对视觉操作质量的评估信号。两者协同工作，使得模型无需任何中间标注（如边界框、分割掩码）即可学会在推理过程中有效地“看”图像。



MedVR 的训练框架围绕三个核心模块构建：**复合终端奖励设计**、**熵引导的视觉重定位（EVR）** 和 **基于共识的信用分配（CCA）**。以下逐一展开其机制与关键公式。

### 3.1 复合终端奖励设计

MedVR 将视觉推理建模为工具增强的序列决策过程。对于一条完整的推理轨迹 $\mathcal{T}$，其终端奖励由三个分量组成：

$$R(\mathcal{T}) = R_{\mathrm{acc}}(\mathcal{T}) + R_{\mathrm{format}}(\mathcal{T}) + \mathbb{1}\big(R_{\mathrm{acc}}(\mathcal{T}) > 0\big) \cdot R_{\mathrm{tool}}(\mathcal{T})$$

各分量含义：
- **$R_{\mathrm{acc}}(\mathcal{T})$**：答案准确性奖励，根据最终答案是否正确给予主奖励。
- **$R_{\mathrm{format}}(\mathcal{T})$**：格式惩罚项，对语法无效或格式错误的输出施加轻微惩罚，约束输出规范性。
- **$R_{\mathrm{tool}}(\mathcal{T})$**：工具使用奖励，**仅当答案正确时**才激活（由指示函数 $\mathbb{1}(\cdot)$ 控制）。这一条件机制的设计意图是：若模型连答案都无法答对，则其视觉操作大概率是无效探索，不应获得工具奖励，从而避免奖励误导。

策略优化的目标函数为：

$$\max_{\theta} \mathbb{E}_{(Q,I) \sim \mathcal{D}, \mathcal{T} \sim \pi_{\theta}} \Big\{ R(\mathcal{T}) - \beta D_{\mathrm{KL}} \big[ \pi_{\theta}(\cdot | Q,I) \parallel \pi_{\mathrm{ref}}(\cdot | Q,I) \big] \Big\}$$

其中 $Q$ 为问题，$I$ 为输入图像，$\pi_{\theta}$ 为当前策略，$\pi_{\mathrm{ref}}$ 为参考策略，$\beta$ 控制 KL 散度惩罚的强度。该目标在最大化期望奖励的同时，防止策略偏离参考模型过远，维持生成稳定性。

### 3.2 熵引导的视觉重定位（EVR）

EVR 的核心思想是：**用模型自身的预测不确定性来决定何时进行视觉探索**，而非随机触发。

**不确定性度量**：在生成过程的每一步 $t$，模型输出下一个 token 的概率分布 $p_t = \mathrm{Softmax}(z_t / \tau)$（$z_t$ 为 logits，$\tau$ 为温度系数），其熵定义为：

$$H_t = -\sum_{j=1}^{|V|} p_{t,j} \log p_{t,j}$$

$H_t$ 越高，表示模型对当前 token 的预测越不确定，意味着此时可能正处于需要重新审视视觉证据的关键节点。

**探索机制**：EVR 在 $H_t$ 超过阈值时触发并行分支，生成 $M$ 条不同的探索轨迹。每条轨迹对应一种视觉假设（如放大图像的不同区域），从而构成异构的轨迹集合。EVR 的输出是这 $M$ 条轨迹的集合，它们共同体现了模型基于自身不确定性的多样化视觉搜索假设。

**计算复杂度**：EVR 的自适应树搜索机制将计算复杂度从独立采样的 $O(n^2)$ 降至 $O(n \log n)$（论文第 4.4 节分析），在保持探索多样性的同时控制了推理开销。

### 3.3 基于共识的信用分配（CCA）

CCA 解决的核心问题是：**在没有中间标注的情况下，如何为视觉操作提供细粒度的自生成监督信号**。

**共识掩码生成**：对于一批轨迹中答案正确的子集 $\mathcal{T}^+$，提取每条轨迹 $\mathcal{T}_i$ 的视觉操作足迹 $M_i$（即工具调用涉及的空间区域），累加得到热力图 $C = \sum_{\mathcal{T}_i \in \mathcal{T}^+} M_i$，然后通过多数投票规则二值化：

$$\hat{M}(u,v) = \mathbb{1}\big(C(u,v) > |\mathcal{T}^+| / 2\big)$$

$\hat{M}$ 即为共识掩码，它标定了**被大多数成功轨迹共同关注的图像区域**，作为“应该关注哪里”的伪监督信号。

**工具奖励计算**：对于轨迹 $\mathcal{T}_j$，其工具使用奖励取决于其视觉足迹 $M_j$ 与共识掩码 $\hat{M}$ 的对齐程度：

$$R_{\mathrm{tool}}(\mathcal{T}_j) = \begin{cases} 1.0, & \mathrm{if} \ \mathrm{IoU}(M_j, \hat{M}) > \eta \\ 0.5, & \mathrm{otherwise} \end{cases}$$

其中 $\mathrm{IoU}(M_j, \hat{M}) = |M_j \cap \hat{M}| / |M_j \cup \hat{M}|$，$\eta$ 为阈值（论文设为 0.5）。该设计的逻辑是：若某条轨迹的视觉关注区域与共识区域高度重叠，则其视觉操作是有效的，获得全额工具奖励；否则仅获得部分奖励，鼓励模型向共识方向靠拢。

### 模块间的因果联动

三个模块形成闭环：**EVR** 在模型不确定性高处触发探索，生成多样化轨迹；**CCA** 从成功轨迹中提取共识区域，为每条轨迹的视觉操作质量打分；**复合奖励** 将答案正确性、格式规范性和视觉操作有效性统一为标量信号，驱动策略优化。这一设计使得 MedVR 无需任何中间标注即可学习精准的视觉定位能力。



## 实验与关键发现

### 主实验结果

MedVR 在六个公开医学 VQA 基准上进行了系统评估，涵盖通用领域（多项选择）和模态特定（自由文本）两类任务。通用领域基准包括 OmniMedVQA、PMC-VQA 和 MedXpertQA，其中 PMC-VQA 与 MedXpertQA 标记为分布外测试集；模态特定基准包括 VQA-RAD、SLAKE 和 PathVQA。

**Table 1** 展示了 MedVR 与五类通用模型及领域专用医学模型的全面对比。MedVR 在通用领域平均得分 59.2，模态特定平均得分 74.0，均达到最优或次优水平。具体而言，MedVR 显著超越了参数量更大的医学专用模型 **Lingshu-7B**（通用 55.0 / 模态 70.3）和通用视觉语言模型 **InternVL3-14B**（53.0 / 62.4），验证了视觉推理框架在医学场景中的有效性。

![[assets/figures/papers/paper_list_l17_https_openreview_net_forum_id_cK35kNVm5r/figures/003_Table_1.jpg]]
*Table 1: Comprehensive performance comparison on medical VQA benchmarks, divided into General-Domain (multiple-choice) and Modality-Specific (free-text) tasks. Out-of-domain (OOD) test sets are marked with ⋄. The best and second-best results are highlighted in bold and underlined*

**Table 4** 进一步揭示了 MedVR 的数据效率优势：相较于依赖大规模专有数据集（最高达 33M 样本）和多阶段训练流程的基线模型，MedVR 仅使用 36K 过滤后的 OmniMedVQA 数据，通过纯强化学习训练即可取得竞争性甚至更优的性能。

![[assets/figures/papers/paper_list_l17_https_openreview_net_forum_id_cK35kNVm5r/figures/013_Table_4.jpg]]
*Table 4: Summary of training data, methodologies, and benchmark overlap for key baselines*

### 消融实验

**Table 2** 通过逐步引入三个核心组件——Zoom-in 视觉工具、EVR 探索策略和 CCA 奖励机制——量化了各组件的独立贡献：

![[assets/figures/papers/paper_list_l17_https_openreview_net_forum_id_cK35kNVm5r/figures/004_Table_2.jpg]]
*Table 2: Ablation study for core components of MedVR*

- **基础模型 + Zoom-in**：仅引入视觉工具在分布外基准 PMC-VQA 和 MedXpertQA 上带来初步提升，但整体增益有限。
- **+ EVR**：加入 EVR 后，分布外基准提升最为显著（PMC-VQA 53.81，MedXpertQA 24.73），验证了不确定性引导的视觉探索对泛化能力的关键作用。
- **+ CCA（无 EVR）**：单独引入 CCA 在分布内 OmniMedVQA 上贡献最大（96.55），表明共识驱动的自监督信号有效强化了训练分布内的推理模式。
- **完整 MedVR**：三者协同在全部基准上达到最优（OmniMedVQA 96.77，PMC-VQA 54.31，MedXpertQA 26.38）。

消融结果表明，EVR 与 CCA 存在功能互补：EVR 作为不确定性感知的探索器，提出多样化的视觉假设；CCA 则作为精细的自监督器，识别并奖励共识驱动的高质量推理路径。

### 关键分析

**EVR 的熵权重敏感性（Figure 3a）**：熵权重 $\gamma$ 控制 EVR 对不确定性信号的响应强度。实验显示，适中的 $\gamma$ 值在探索与利用之间取得最佳平衡，过高或过低均会导致性能下降。

**CCA 奖励设计的有效性（Figure 3b）**：对比不同奖励分配策略，基于共识掩码的 IoU 阈值奖励（$\eta = 0.5$）优于均匀奖励和仅基于答案正确性的稀疏奖励，验证了细粒度视觉足迹对齐信号的必要性。

**推理时扩展性（Figure 3c）**：随着推理时采样轨迹数增加，MedVR 的准确率持续提升，展现出良好的推理时扩展特性，表明模型能够有效利用额外的计算预算。

**不确定性-定位质量关联（Figure 4）**：token 级熵与视觉定位的 mIoU 之间存在强负相关——低熵生成对应高质量定位，高熵生成对应低质量定位。这从实证层面验证了 token 级熵作为视觉置信度代理指标的可靠性。

**训练稳定性（Figure 5）**：引入 EVR 的训练过程保持更高且更稳定的策略熵，而未使用 EVR 的训练熵持续下降，暗示策略过早收敛和探索不足的风险。

**训练效率（Figure 6）**：EVR 的自适应树搜索机制将计算复杂度从 $O(n^2)$ 降至 $O(n \log n)$，每步训练时间显著低于独立采样的朴素探索策略。

### 跨模型规模泛化

**Table 3** 展示了 MedVR 在不同模型规模（3B、7B、32B 的 Qwen2.5-VL 及 Lingshu-7B）上的表现。MedVR 在所有规模上均一致优于零样本基线和纯文本 RL 基线，且在分布外基准上的增益更为突出，验证了该框架的模型规模无关性。

![[assets/figures/papers/paper_list_l17_https_openreview_net_forum_id_cK35kNVm5r/figures/011_Table_3.jpg]]
*Table 3: Performance of MedVR across model scales and variants*

### 定位质量评估

**Table 5** 在三个定位基准（GEMEX-ThinkVG、ChestX-ray8、ISIC）上量化评估了 MedVR 的视觉定位能力。MedVR 的 mIoU 分别达到 59.62、54.29 和 69.12，远超 Qwen2.5-VL-7B 零样本基线的 17.54、36.53 和 35.73，证明无需定位标注即可学习精确的视觉基础能力。

![[assets/figures/papers/paper_list_l17_https_openreview_net_forum_id_cK35kNVm5r/figures/014_Table_5.jpg]]
*Table 5: Quantitative evaluation of localization quality. MedVR significantly improves the mean Intersection over Union (mIoU) compared to the zero-shot backbone, demonstrating its ability to learn precise visual grounding without annotations*

**Table 6** 进一步将 MedVR 与有监督变体对比：在 GEMEX-ThinkVG 上，无标注 MedVR 的准确率（79.08%）和 mIoU（59.62%）与有监督版本（79.62% / 61.33%）差距极小，表明自监督机制几乎弥补了标注信号的缺失。

### 通用视觉能力验证

**Table 7** 和 **Table 8** 分别在通用视觉定位基准（refCOCO 系列）和多模态数学推理基准（MathVision、MathVerse、MathVista）上评估了 EVA + CCA 框架。该方法在所有基准上均优于 Qwen2.5-VL-7B 基线和 **DeepEyes**，验证了 EVR 和 CCA 机制的领域通用性，不仅限于医学场景。

### 失败模式与局限性

尽管 MedVR 在多数基准上表现优异，仍需注意以下局限：

- **分布外挑战**：在 MedXpertQA 等极具挑战的分布外基准上，绝对准确率（26.38）仍然较低，表明跨领域泛化仍有较大提升空间。
- **推理延迟**：**Table 8** 的推理延迟分析显示，多轨迹采样和视觉工具调用增加了推理开销，在实时临床场景中可能构成瓶颈。
- **视觉工具单一**：当前仅支持 Zoom-in 操作，对旋转、对比度调整等更丰富的图像操作缺乏支持，可能限制复杂视觉推理任务的表现。

### 重要图表结论汇总

| 图表 | 核心结论 |
|------|----------|
| Table 1 | MedVR 在六个医学 VQA 基准上达到 SOTA，超越更大规模专用模型 |
| Table 2 | EVR 与 CCA 功能互补，协同达到最优；EVR 主导 OOD 增益，CCA 主导 ID 增益 |
| Table 3 | 框架在 3B–32B 规模上一致有效 |
| Table 4 | 仅用 36K 数据 + RL 训练即可匹敌大规模多阶段基线 |
| Table 5 | 无标注训练使 mIoU 提升 2–3 倍 |
| Figure 4 | Token 熵与定位质量强负相关，验证 EVR 设计合理性 |
| Figure 5 | EVR 防止策略熵崩溃，维持训练稳定性 |



## 定位与知识库关联

### 1. 方法定位与谱系

MedVR 处于**医学视觉‑语言模型的推理增强**这一研究线上，其核心贡献是将视觉工具调用（zoom‑in）纳入端到端强化学习框架，从而在无需中间监督的条件下实现可验证的视觉推理。与现有工作的关系可从三个维度梳理。

**相对于纯文本推理方法。** 医学 VLM 的早期 RL 训练（如 Text‑only RL）仅优化文本链式思维，缺乏对图像内容的主动交互，容易产生视觉幻觉（Figure 1 左侧）。MedVR 在文本推理中插入视觉工具调用，使模型能够“看后再想”，从根本上改变了推理的证据来源。

**相对于有监督视觉定位方法。** 传统方法依赖人工标注的边界框或分割掩码来训练视觉定位能力。MedVR 通过 CCA 机制从成功轨迹的共识中自动生成伪监督，在 GEMEX‑ThinkVG 上以无标注方式达到 79.08% 准确率，与有监督变体（79.62%）差距极小，同时 mIoU 从零样本基线的 17.54 提升至 59.62（Table 5, Table 6）。这证明自监督信号可以在不牺牲精度的前提下替代昂贵的人工标注。

**相对于通用视觉‑语言模型。** Table 1 显示，MedVR 在通用域医学 VQA（平均 59.2）和模态特异性任务（平均 74.0）上均优于更大规模的通用模型（如 InternVL3‑14B 的 53.0/62.4）和医学专用模型（如 Lingshu‑7B 的 55.0/70.3）。值得注意的是，MedVR 仅使用 36K 过滤后的 OmniMedVQA 数据进行 RL 训练，而基线模型通常依赖数百万至数千万的预训练数据和多阶段训练流程（Table 4），表明 RL 驱动的视觉推理比单纯扩大数据规模更高效。

### 2. 适用边界

MedVR 的适用边界由以下因素共同定义：

- **任务类型。** 框架设计针对需要精细视觉检查的医学 VQA，尤其是定位病灶、识别细微异常等场景。在通用视觉定位基准（refCOCO/+/g）上的迁移实验（Table 7）表明，EVR + CCA 组合也展现出跨域泛化能力，但其主要验证仍集中在医学领域。
- **模型规模。** Table 3 显示 MedVR 在 3B、7B、32B 三个尺度上均取得一致提升，说明方法对模型规模不敏感，但 7B 是论文的主要实验设置。
- **训练数据需求。** 框架仅需问答对作为监督信号，无需定位标注。但 CCA 的有效性依赖于存在足够多的成功轨迹来形成共识——当任务本身极难、成功轨迹稀疏时，共识掩码的质量可能下降。
- **计算开销。** EVR 的并行探索机制在训练时增加了轨迹采样数量（每 prompt 16 条轨迹），但通过自适应剪枝将复杂度从 $\mathcal{O}(n^2)$ 降至 $\mathcal{O}(n \log n)$（Section 4.4）。推理时仅需单条轨迹，不引入额外开销。

### 3. 局限与开放问题

论文自身揭示或暗示的局限包括：

**工具类型单一。** 当前 MedVR 仅支持 zoom‑in 这一种视觉操作。对于需要多尺度分析、跨图像对比或区域关系推理的复杂场景，单一工具的表达力可能不足。扩展工具集（如旋转、窗宽窗位调节、多图协同）是自然的后续方向。

**共识机制的失效模式。** CCA 通过多数投票生成共识掩码，当成功轨迹本身存在系统性偏差（例如都聚焦于错误区域但碰巧答对）时，共识掩码会强化错误定位。论文未讨论这种“共谋失败”的发生频率和检测方法。

**跨域泛化的上限。** 尽管 Table 7 展示了向通用视觉定位的迁移，但医学图像与自然图像在纹理、结构上的本质差异意味着 EVR 的熵信号模式可能需要域适配。论文未提供在非医学领域的长尾分布上的详细分析。

**开放问题**包括：

1. EVR 的熵阈值与 CCA 的 IoU 阈值（$\eta=0.5$）是否需要在不同医学模态（X 光、CT、病理切片）间调整？Figure 3 的敏感性分析仅在 OmniMedVQA 上进行，结论的模态泛化性待验证。
2. 当视觉工具调用本身产生错误（例如 zoom‑in 到无关区域）时，模型能否从这种“视觉误导”中恢复？论文的定性示例（Figure 7）展示了成功案例，但未系统分析失败模式。
3. MedVR 的训练仅使用 OmniMedVQA 数据，其在完全未见的医学成像模态（如超声、OCT）上的零样本表现尚未报告，这限制了对其真实 OOD 鲁棒性的判断。

### 4. 与知识库的关联

MedVR 的方法论贡献可嵌入以下知识节点：

- **RL for VLM reasoning。** 与 GRPO（Group Relative Policy Optimization）的集成使 MedVR 成为医学领域首个将工具调用纳入策略优化的端到端框架，区别于仅在文本空间做 RL 的工作。
- **Uncertainty‑guided exploration。** EVR 利用 token‑level entropy 作为内在探索信号，这与主动学习中的不确定性采样、以及 LLM 推理中的 entropy‑based decoding 共享思想源头，但在视觉动作空间中实现了闭环。
- **Consensus‑based self‑supervision。** CCA 的“成功轨迹投票”机制与多智能体系统中的共识算法、以及自洽性（self‑consistency）解码有概念上的亲缘关系，但将其用于生成空间定位的伪标签是一个新的应用场景。



## 原文 PDF

![[paperPDFs/ICLR_2026/MedVR_Annotation_Free_Medical_Visual_Reasoning_via_Agentic_Reinforcement_Learning.pdf]]
