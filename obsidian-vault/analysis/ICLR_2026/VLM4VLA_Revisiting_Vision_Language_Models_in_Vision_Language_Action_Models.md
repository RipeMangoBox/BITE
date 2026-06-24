---
title: "VLM4VLA: Revisiting Vision-Language-Models in Vision-Language-Action Models"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/VLM4VLA_Revisiting_Vision_Language_Models_in_Vision_Language_Action_Models.pdf
aliases:
- VLM4VLA
tags:
- ICLR_2026
- topic/other_unclear
- topic/other_unclear/general
core_operator: "视觉编码器是否在具身数据上进行微调，以及是否接受控制相关的监督，是影响下游VLA性能的关键调节变量。"
primary_logic: "通用VLM的基准能力不能有效预测其在具身控制任务上的表现，当前VLM预训练目标与具身动作规划需求之间存在显著的域差距，增强视觉编码器的具身适应性比追求通用VLM基准分数更为重要。"
claims:
- "冻结视觉编码器导致性能大幅下降（PaliGemma-1在SimplerBridge从55.25降至13.25）。"
- "通用VLM能力与SimplerEnv和Libero上的VLA性能相关性弱或为负（SimplerEnv: r=-0.321, Libero: r=0.381），表明通用能力不是好的预测指标。"
- "在辅助具身任务上微调VLM并未提升下游控制任务表现，甚至略有下降（Qwen2.5VL-7B +Robobrain2 从4.057降至3.887）。"
- "Calvin ABC-D 上 平均完成任务数 = 4.057 (Qwen2.5VL-7B)"
---

# VLM4VLA: Revisiting Vision-Language-Models in Vision-Language-Action Models

> [!tip] 核心洞察
> 通用VLM的基准能力不能有效预测其在具身控制任务上的表现，当前VLM预训练目标与具身动作规划需求之间存在显著的域差距，增强视觉编码器的具身适应性比追求通用VLM基准分数更为重要。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | VLM4VLA：重新审视视觉-语言模型在视觉-语言-动作模型中的作用 |
| 英文题名 | VLM4VLA: Revisiting Vision-Language-Models in Vision-Language-Action Models |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=tc2UsBeODW); [Project](https://cladernyjorn.github.io/VLM4VLA.github.io/) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | VLM4VLA |
| Dataset | Calvin ABC-D, SimplerEnv-Bridge, Libero‑10 (long) |

> [!tip] 效果简介
> - Calvin ABC-D 上，平均完成任务数 为 4.057 (Qwen2.5VL-7B)，对比 3.801 (OpenVLA*) / 3.509 (pi0*)，变化 +0.256 / +0.548。
> - SimplerEnv-Bridge 上，总体成功率 (%) 为 60.4 (KosMos-2 / InternVL3.5-4B)，对比 60.4 (OpenVLA*)，变化 持平。
> - Libero‑10 (long) 上，成功率 (%) 为 62.8 (InternVL3.5-4B)，对比 59.2 (ThinkAct)，变化 +3.6。

## 概述

通用视觉‑语言模型（VLM）正被广泛用作视觉‑语言‑动作模型（VLA）的骨干，但其内部哪部分能力真正决定下游操控任务的表现仍不明确。本文发现，**VLM的视觉编码器（而非语言模块）是VLA性能的主要瓶颈**：冻结视觉编码器会导致成功率断崖式下降（PaliGemma‑1在SimplerBridge上从55.25降至13.25，Table 3），而通用VLM基准能力与SimplerEnv和Libero上的VLA性能呈弱甚至负相关（r=−0.321/0.381，Figure 3）。在辅助具身任务上微调VLM亦未能带来提升，多数略有下降（Table 8）。这表明当前VLM预训练目标与具身动作规划之间存在显著的域差距，提升视觉编码器的具身适应性远比追求通用榜单分数更为关键。

针对这一问题，我们提出 **VLM4VLA**——一个将通用VLM转换为VLA策略的最小化适配框架。它仅引入不足1%的新参数（一个可学习的动作查询令牌及小尺寸MLP策略头），采用最大似然模仿学习直接输出动作块；同时刻意排除本体感觉输入，仅依赖单视图图像与语言指令，以隔离VLM自身能力对控制的影响。所有VLM参数（视觉编码器、词嵌入与LLM）均在下游任务上全参数微调。在Calvin ABC‑D、SimplerEnv‑Bridge和Libero‑10三个仿真基准上的实验表明，VLM4VLA使用多种VLM骨干（Qwen2.5VL、KosMos‑2、InternVL3.5等）即可达到或超越专家VLA（OpenVLA、pi0、ThinkAct）的性能，例如Qwen2.5VL‑7B在Calvin上平均完成任务数达4.057，超越OpenVLA*的3.801和pi0*的3.509（Table 1）。总体而言，本文系统揭示了视觉编码器是VLM→VLA迁移的关键调节变量，并为未来面向具身控制的VLM预训练指明了方向。

## 背景与动机

视觉-语言-动作（VLA）模型致力于将大规模视觉-语言模型（VLM）用于机器人操作策略，以期借助预训练的多模态知识提升少样本泛化与指令跟随能力。然而，现有工作在将通用VLM适配至具身控制任务时，存在以下关键缺口：

**1）VLM能力与VLA性能之间的弱关联**  
主流方法倾向于选择在通用视觉问答（VQA）或指令跟随基准上得分更高的VLM作为策略骨干，但实际表现并不理想。实验表明，通用VLM的基准能力与下游控制任务上的VLA性能之间的线性相关性弱甚至为负（SimplerEnv: $r=-0.321$；Libero: $r=0.381$），说明通用能力并非好的预测指标（Figure 3, Appendix A.4）。这一现象指向VLM预训练目标与具身动作规划需求之间存在巨大的域差距。

**2）视觉编码器成为性能瓶颈**  
过去的设计往往冻结视觉编码器以保留通用视觉知识，或仅微调语言模块，但消融实验揭示冻结视觉编码器会导致性能急剧下跌。例如，PaliGemma-1在SimplerBridge上的成功率从55.25%降至13.25%；Qwen2.5VL-3B在Calvin ABC-D上的平均完成任务数从3.856下降至2.855（Table 3）。相反，全参数微调（尤其是视觉编码器的充分训练）则是将VLM迁移为有效VLA策略的关键因果杠杆，其重要性远高于语言部分参数量的增加。

**3）辅助具身任务微调并未带来增益**  
为弥合域差距，近期工作尝试将VLM在辅助的具身感知或推理任务上先行微调，再用于控制。但系统评估显示，这种做法对下游VLA性能几乎没有帮助，甚至略有下降：Qwen2.5VL-7B在Robobrain2上微调后，Calvin总分由4.057降至3.887（Table 8, Figure 4）。这意味着现有具身VQA风格的任务设计无法为端到端控制提供有效迁移，针对控制目标的预训练或微调信号更值得探索。

**4）复杂动作解码器未必带来性能提升**  
部分专家VLA模型采用扩散模型或流匹配等复杂动作解码器，以期提升动作生成的多样性或精度。然而，将这些专家模型适配至统一输入条件（单视图图像，无本体感觉）后，其表现并未超越基于简单MLP动作头的轻量设计（pi0*在Calvin上得分3.509，与原始Paligemma-1的3.506几乎持平；Table 1）。这表明在输入模态与训练监督对齐之前，解码器的复杂度不是首要瓶颈。

基于以上观察，本文的动机在于**系统性地重新审视VLM在VLA中扮演的角色**，而非默认将性能瓶颈归于语言模块或动作解码器。我们提出 **VLM4VLA 轻量适配框架**：仅引入可学习的`⟨ActionQuery⟩`令牌和一个小型MLP策略头（新增参数<1%），便可将任意通用VLM转换为离散动作策略；该框架刻意排除本体感觉等额外模态，仅依赖单视图视觉输入与自然语言指令，从而在公平的设定下隔离VLM能力的影响（Section 1, Figure 1）。通过控制输入条件、训练步数和评估协议，我们能够可靠地研究三个关键问题：（i）不同VLM骨干对VLA表现的影响；（ii）视觉编码器微调相较于语言模块的重要性；（iii）辅助具身微调是否真正有益，从而为未来VLM向VLA的高效迁移提供经验性指导。

## 核心创新

VLM4VLA提出了一套参数增量极小的适配框架（新增参数<1%），将通用视觉‑语言模型（VLM）转换为视觉‑语言‑动作（VLA）策略。相较于现有专家VLA（如OpenVLA的离散动作空间、pi0的流匹配动作专家），其核心创新体现在以下若干受控设计槽（changed slots）上，背后由关于视觉编码器瓶颈的经验发现所驱动。

### 1. 轻量动作解码器与不确定性控制
VLM4VLA用一个可学习的动作查询令牌（⟨ActionQuery⟩）与一个小型MLP头替代扩散／流匹配动作专家，动作由$\mathbf{action} = \mathbf{MLP}\big( \mathrm{VLM}\big( [ \langle img\rangle \dots \langle img\rangle \langle text\rangle \dots \langle ActionQuery\rangle ] \big) \big)$解码（Section 3.2）。该设计消除了扩散过程的随机性，提升推理稳定性与评估鲁棒性，同时使新增参数远远少于扩散头（Section 1）。

### 2. 训练目标从扩散损失转向最大似然模仿学习
与扩散损失或流匹配损失不同，VLM4VLA采用直接的最大似然模仿学习目标：
$$\mathcal{L} = \frac{1}{|\mathcal{B}|} \sum_{\mathcal{B}} \left( \| \boldsymbol{a}^{\mathrm{pos}} - \hat{\boldsymbol{a}}^{\mathrm{pos}} \|_2^2 + \mathrm{BCE}(a^{\mathrm{end}}, \hat{a}^{\mathrm{end}}) \right)$$
其中MSE用于末端执行器相对位置，BCE用于末端执行器离散状态（Equation (1), Section 3.2）。该选择避免了扩散多步推理中的不稳定因素，并与简化MLP头协同，在Calvin ABC‑D上实现与复杂扩散专家可比甚至更优的性能（例如pi0*在同等训练设置下并未超越基于同一VLM骨干的MLP变体，Table 1）。

### 3. 输入模态的刻意简化：排除本体感觉
VLM4VLA刻意仅依赖单视图图像与语言指令，摒弃本体感觉输入（Section 3）。相较于pi0和OpenVLA的多模态输入，这一设计旨在隔离VLM的视觉‑语言能力，防止模型直接从状态学习动作映射，从而将下游性能准确归因于VLM骨干本身（Section A.2.1）。实验设置中对所有基线模型统一了此单模态输入，确保比较公平性。

### 4. 全参数微调以释放视觉编码器潜力
与先前工作常冻结视觉编码器的做法不同，VLM4VLA在训练时微调VLM的所有参数，包括视觉编码器、词嵌入和LLM（Section 3.2, A.2.1）。这一设计由消融实验直接驱动：冻结视觉编码器导致性能崩塌（例如PaliGemma‑1在SimplerBridge从55.25骤降至13.25；Qwen2.5VL‑3B在Calvin ABC‑D从3.856降至2.855，Table 3）。数据强烈暗示视觉模块（而非语言部分参数量的增减）是下游控制性能的主要瓶颈。因此，将视觉编码器纳入全参数微调成为框架的关键调节手段。

上述创新共同锚定于一项核心洞察：通用VLM基准能力不能有效预测其在下游具身控制任务上的表现（SimplerEnv: $r = -0.321$；Libero: $r = 0.381$，Figure 3），且辅助具身VQA式微调未能提升甚至轻微损害VLA性能（Table 8, Figure 4）。因此，增强视觉编码器的具身适应性——而非单纯追求通用VLM基准分数——是VLM4VLA设计哲学的根基。

## 整体框架

![[assets/figures/papers/iclr26_0014_tc2UsBeODW_VLM4VLA_Revisiting_Vision-Language-Models_in_Vis/figures/002_Figure_2.jpg]]
*Figure 2: VLA Network in VLM4VLA*

![[assets/figures/papers/iclr26_0014_tc2UsBeODW_VLM4VLA_Revisiting_Vision-Language-Models_in_Vis/figures/001_Figure_1.jpg]]
*Figure 1: An overview of our VLM4VLA framework. (Left) The evaluation pipeline for testing different VLM backbones, which are evaluated on downstream tasks after an optional fine-tuning stage on auxiliary embodied tasks. (Bottom Right) We systematically investigate three factors influencing VLM-to-VLA transfer: the choice of VLM backbone, the impact of fine-tuning on auxiliary embodied tasks, and the vision encoder’s training strategy (frozen vs. fine-tuned). (Top Right) A visualization of inconsistent performance of various VLM backbones across downstream tasks*

VLM4VLA 是一个**轻量级适配管线**，旨在以最小代价将通用视觉‑语言模型（VLM）转换为视觉‑语言‑动作（VLA）策略。其核心设计原则是仅引入不足总参数量 1% 的新增权重，并采用简化的 MLP 策略头替代扩散或流匹配等复杂解码器，从而在保证推理稳定性的同时，为不同 VLM 骨干提供完全对齐的评估条件。

### 模块组成与连接关系
VLM4VLA 由三个模块串联构成（见图 2）：

- **VLM 骨干网络（VLM Backbone）**：负责处理视觉和语言输入，提取多模态表征。单帧图像经 VLM 自带的视觉编码器编码，语言指令经词嵌入转换为标记序列。
- **可学习的动作查询令牌（Action Query Token）**：一个特殊的、可训练的令牌，追加在图像和文本标记之后。它通过 VLM 的自注意力机制，从多模态上下文中主动提取与具身操控相关的知识。
- **小型 MLP 策略头（MLP Policy Head）**：以 Action Query 令牌的最后一层隐藏状态为输入，将其解码为动作序列。该 MLP 头新增参数极少，在所有 VLM 骨干中仅占总参数量的千分之几（见表 7）。

整个前向计算过程可概括为：

$$
\mathbf{action} = \mathbf{MLP}\big( \mathrm{VLM}\big( \big[ \langle \text{img}\rangle \dots \langle \text{img}\rangle \langle \text{text}\rangle \dots \langle \text{ActionQuery}\rangle \big] \big) \big)
$$

### 输入输出流与训练范式
框架刻意**排除了本体感觉状态**，仅使用**单视角图像**（224×224 分辨率）和**语言任务指令**作为输入，以迫使模型从纯视觉‑语言通道学习规划与执行，而非直接记忆状态‑动作映射。输出为包含末端执行器相对位置与离散状态的**动作块（action chunk）**。

训练时，**所有 VLM 参数（视觉编码器、令牌嵌入、LLM 主体）均被微调**，采用最大似然模仿学习目标，将多元动作预测分解为位置维度的均方误差（MSE）损失与状态维度的二元交叉熵（BCE）损失：

$$
\mathcal{L} = \frac{1}{|\mathcal{B}|} \sum_{\mathcal{B}} \left( \| a^{\mathrm{pos}} - \hat{a}^{\mathrm{pos}} \|_2^2 + \mathrm{BCE}(a^{\mathrm{end}}, \hat{a}^{\mathrm{end}}) \right)
$$

这种统一的设计使得在不同 VLM 骨干之间可以实现严格的公平比较，并能够系统性地考察**VLM 骨干选择**、**辅助具身任务微调**以及**视觉编码器训练策略**三个因素对 VLA 性能的独立影响。

## 核心模块与公式推导

VLM4VLA 通过最小化架构适配将通用视觉‑语言模型直接转换为视觉‑语言‑动作策略，其核心由三个模块与一个轻量训练范式构成。

### 核心模块架构

- **VLM 骨干**：直接复用现成的 VLM（如 Qwen2.5VL、PaliGemma、InternVL 等），同时处理视觉和语言输入。输入仅由单视图图像与语言指令组成，刻意排除本体感觉等额外模态，以隔离 VLM 自身的多模态理解能力。
- **动作查询令牌（⟨ActionQuery⟩）**：一个可学习的特殊令牌，附加在标准文本序列末尾。它充当“查询”角色，从 VLM 的隐藏表示中提取与具身动作相关的知识。
- **MLP 策略头**：一个小型多层感知机（新增参数量 <1%），接收 ⟨ActionQuery⟩ 令牌经 VLM 编码后的最后一层隐藏状态，直接解码出动作块序列。

训练时，框架采用**全参数微调**（包括视觉编码器、词嵌入与 LLM 部分），以最大似然模仿学习为目标，使用简单的 MSE + BCE 损失函数，避免扩散类解码器引入的随机性，从而增强评估稳定性。

### 关键公式与变量含义

**动作解码公式**

$$ \mathbf{action} = \mathbf{MLP}\big( \mathrm{VLM}\big( \big[ \langle img\rangle \cdot \dots \langle img\rangle \langle text\rangle \dots \langle text\rangle \langle ActionQuery\rangle \big] \big) \big) $$

- $ \langle img \rangle $ 表示图像嵌入后的令牌序列；
- $ \langle text \rangle $ 表示语言指令的文本令牌；
- $ \langle ActionQuery \rangle $ 为可学习的动作查询令牌；
- $ \mathrm{VLM}(\cdot) $ 将多模态令牌序列送入冻结前或微调后的 VLM 骨干，得到各令牌的隐藏状态；
- $ \mathbf{MLP}(\cdot) $ 表示策略头，以 $ \langle ActionQuery \rangle $ 的最后一层隐藏状态为输入，输出连续动作向量 $ \mathbf{action} $。

**训练损失函数**

$$ \mathcal{L} = \frac{1}{|\mathcal{B}|} \sum_{\mathcal{B}} \left( \| a^{\mathrm{pos}} - \hat{a}^{\mathrm{pos}} \|_2^2 + \mathrm{BCE}(a^{\mathrm{end}}, \hat{a}^{\mathrm{end}}) \right) $$

- $ \mathcal{B} $ 表示一个 mini‑batch；
- $ a^{\mathrm{pos}} $ 与 $ \hat{a}^{\mathrm{pos}} $ 分别为末端执行器相对位置的真实动作与预测动作；
- $ a^{\mathrm{end}} $ 与 $ \hat{a}^{\mathrm{end}} $ 分别为末端执行器离散状态（如开‑闭）的真实标签与预测概率；
- $ \mathrm{BCE} $ 为二元交叉熵损失。

该公式将连续位置预测的均方误差与离散状态预测的交叉熵相结合，构成完整的模仿学习目标。以上公式均源自 Section 3.2，未引入任何额外假设。

## 实验与分析

### 主任务性能
VLM4VLA 在三个具身操控基准上进行了系统评估，所有模型均采用统一超参数、统一单视图（224×224）视觉输入并排除本体感觉，以隔离 VLM 骨干的能力。在 Calvin ABC‑D 上，Qwen2.5VL‑7B 取得平均完成 4.057 个任务（Table 1），比 expert VLA 基线 OpenVLA\*（3.801）和 pi0\*（3.509）分别提升 +0.256 和 +0.548。值得注意的是，pi0\* 虽然带有额外的流匹配动作专家，但其性能与基础 PaliGemma‑1 几乎持平（3.509 vs 3.506），表明扩散动作头在此范式下未带来增益。在 SimplerEnv‑Bridge 上，KosMos‑2 与 InternVL3.5‑4B 均达到 60.4% 总体成功率，与 OpenVLA\* 持平（Table 2），但 VLM4VLA 模型只引入了 <1% 的新参数和简单的 MLP 策略头。在 Libero‑10 long‑horizon 任务上，InternVL3.5‑4B 达到 62.8% 成功率，比强基线 ThinkAct（59.2%）高 +3.6 个百分点（Table 2）。这些结果表明，通用 VLM 通过极简适配即可匹敌乃至超越专门设计的 VLA 模型。

![[assets/figures/papers/iclr26_0014_tc2UsBeODW_VLM4VLA_Revisiting_Vision-Language-Models_in_Vis/figures/003_Table_1.jpg]]
*Table 1: Results on Calvin ABC-D. Entries marked with * are expert VLAs modified and reproduced with our training and test settings*

### 消融实验
#### 视觉编码器是关键瓶颈
冻结 VLM 的视觉编码器导致性能大幅崩塌（Table 3）：PaliGemma‑1 在 SimplerBridge 上的成功率从 55.25% 骤降至 13.25%；Qwen2.5VL‑3B 在 Calvin ABC‑D 上的平均完成数从 3.856 跌至 2.855。相比之下，增大语言模型的可训参数对性能提升远不如微调视觉模块敏感。这表明**当前 VLM 的视觉编码器（而非语言模块）是 VLA 性能的主要瓶颈**——其预训练特征来自通用图像分布，尚未适应具身场景中的精细几何与动力学线索。

![[assets/figures/papers/iclr26_0014_tc2UsBeODW_VLM4VLA_Revisiting_Vision-Language-Models_in_Vis/figures/007_Table_3.jpg]]
*Table 3: Influence of freezing vision encoder of VLMs*

#### 预训练知识不可替代
从随机初始化训练相同的 VLM 架构（Table 4）时，性能全面崩溃：Qwen2.5‑VL‑3B 在 Calvin 上仅得 1.381（预训练为 3.856），PaliGemma‑1 低至 0.284（预训练为 3.506）；在 SimplerBridge 上，Qwen2.5‑VL‑7B 从预训练的 53.35 跌至 6.10。这证明**大规模 VLM 预训练所积累的视觉‑语言联合表示对具身控制至关重要**，从头学习无法在有限机器人数据下重建该能力。

#### 辅助具身微调未带来收益
在将 VLM 适配为 VLA 之前，先用多个公开具身 VQA/描述数据集（RoboVQA、Robobrain2、Omni‑Generation 等）对 VLM 进行中间微调，然后在 Calvin 上评测 VLA 性能（Figure 4, Table 8）。结果表明，绝大多数辅助任务未带来任何提升，甚至导致轻微下降：Qwen2.5VL‑7B 在 Robobrain2 后从 4.057 下降至 3.887，在 Omni‑Generation 后进一步降至 3.876。箱线图（Figure 4）显示，不同辅助任务对应的 VLA 性能分布高度重叠，且中位数常低于未微调的基线。这表明**现有的具身 VQA 任务与端到端动作决策之间存在明显的表征鸿沟**：辅助任务虽同为具身领域，但其监督信号未对齐于控制所需的动态推理，无法提升底层视觉编码器的场景理解质量。

![[assets/figures/papers/iclr26_0014_tc2UsBeODW_VLM4VLA_Revisiting_Vision-Language-Models_in_Vis/figures/006_Figure_4.jpg]]
*Figure 4: Performance of different auxiliary VLM finetune tasks. The ’Length’ dimension is scaled by a factor of 5 to normalize it to the range [0, 1]. The results for the VLAs trained under each task and for each gradient steps (10k, 15k, 20k, 25k and 30k) are rendered as box plots to provide a view of the impact of different tasks on the VLA’s performance and stability*

### 通用 VLM 能力与 VLA 性能的脱节
Figure 3 将多个 VLM 在通用 VQA 基准上的分数与下游 VLA 性能进行线性拟合。在 Calvin 上相关性弱（r≈0.38），在 SimplerEnv 上甚至呈现负相关（r≈‑0.32）。这一发现直接挑战了“更强的通用 VLM 自然产生更强的 VLA”的假设，并揭示**VLM 预训练目标（图文对齐、常识问答）与具身动作规划所需的（稀疏奖励、时序一致、物理约束）之间存在着根本性的域差距**。这解释了为何单纯追求通用 VLM 榜单排名并不保证机器人操控的进步。

![[assets/figures/papers/iclr26_0014_tc2UsBeODW_VLM4VLA_Revisiting_Vision-Language-Models_in_Vis/figures/005_Figure_3.jpg]]
*Figure 3: Comparison of the linear relationship between general VLM capabilities and VLA performance*

### 局限与待验证问题
所有评估均在仿真器（Calvin、SimplerEnv、Libero）中完成，尚未在真实机器人上验证。受算力限制，所考察的 VLM 参数集中在 1B–10B，更大规模模型的行为未知。视觉编码器瓶颈的深层机制——例如到底是归因于感受野、频率偏置还是几何表征的缺失——仍待解剖。同时，当前结果表明，常规具身 VQA 微调无效，亟需设计新型辅助训练任务（如基于视点变换的预测、接触感知特征学习），以弥合视觉编码器的预训练分布与控制任务分布之间的鸿沟。

## 方法谱系与知识库定位

VLM4VLA 属于一类将通用视觉-语言模型极简适配为视觉-语言-动作策略的方法。它与专门设计的专家 VLA（如 OpenVLA、pi0、ThinkAct）不同：后者通常为特定架构和训练目标构建，而 VLM4VLA 通过新增不足 1% 的可学习参数（一个可学习的动作查询令牌和一个小型 MLP 头）将现成的 VLM 转化为端到端控制策略，并在全参数微调下最大化预训练表征的利用（Section 1，Figure 2）。这种“最小适配”设计使得 VLM4VLA 能够对多种 VLM 骨干进行系统性横向比较，从而揭示 VLM 到 VLA 迁移中的关键瓶颈。

**与基线方法的关系与差异**

- **OpenVLA**：基于 Llama2-7B 和 DINOv2/SigLIP 视觉编码器的专家 VLA，采用离散动作空间。在统一测试设置下（单视图图像、无本体感觉），VLM4VLA 以连续动作 MLP 头在 Calvin ABC‑D 上将平均完成任务数从 3.801 提升至 4.057（Qwen2.5VL-7B，Table 1），同时保持 SimplerEnv-Bridge 上的总体成功率持平（60.4 vs 60.4，Table 2）。这表明，即使不使用专门的动作空间设计，增强视觉-语言骨干并全参数微调也能释放较强的控制能力。
- **pi0**：同样基于 PaliGemma-1 的专家 VLA，但额外配备了流匹配动作专家（Flow-matching expert）。在相同骨干下，VLM4VLA 仅凭 MLP 头就几乎追平了 pi0 的 Calvin 得分（3.506 vs 3.509，Table 1）。值得注意的是，pi0 额外的扩散专家并未带来显著增益，反而引入更大的推理随机性；MLP 头则降低了调参复杂度并提高了评估稳定性（Section 1）。
- **ThinkAct**：将 Qwen2.5VL-7B 作为 VLA 骨干并通过强化学习增强。VLM4VLA 在 Libero‑10 长序列任务上以 62.8% 对 59.2% 超过 ThinkAct（Table 2），显示全参数监督微调在特定条件下可能优于 RL 微调，尤其是当视觉表征被充分更新的情况下。
- **原始通用 VLM**：不经微调或将 VLM 部分冻结时，性能急剧下降。例如，冻结 PaliGemma-1 的视觉编码器使 SimplerBridge 成功率从 55.25 暴跌至 13.25（Table 3）；从头训练重新初始化更使 Calvin 分数从 3.856 跌至 1.381（Table 4）。这确认了 VLM 预训练知识不可或缺，且视觉编码器是决定下游控制性能的核心瓶颈。

**设计空间的因果调节变量**

VLM4VLA 的框架有四个关键改变相较于常见专家 VLA（Section 3.2）：
1. **动作解码器从扩散头简化为 MLP 头**：动作解码目标从流匹配损失变为最大似然模仿学习（MSE+BCE，公式 (1)），减少了随机性依赖并隔离了 VLM 能力的影响。
2. **输入模态仅包含视觉-语言信息**：排除了本体感觉状态，迫使模型从视觉场景和语言指令中推断动作，从而更纯粹地衡量 VLM 的表征质量。
3. **训练目标统一为监督学习**：直接在末端执行器相对位姿上回归，摒弃扩散或强化学习损失，使不同 VLM 的控制能力可直接比较。
4. **全参数微调**：包括视觉编码器、LLM 和词嵌入，保证 VLM 所有模块都适应具身控制场景。其中，视觉编码器的微调被证明是最大的性能杠杆：冻结视觉编码器导致巨大差距，而仅增加 LLM 可训参数无法弥补（Table 3）。

**适用边界与假设**

当前 VLM4VLA 的结论建立在以下边界内：
- **仿真基准**：所有实验均限于 Calvin ABC‑D、SimplerEnv-Bridge 和 Libero‑10 三个模拟环境，缺乏真实机器人验证，sim-to-real 迁移能力未知。
- **输入限制**：仅使用单视角图像（224×224）和语言指令，不接入任何本体感觉或力反馈信息，因此可能不适用于需要精细位姿估计或力矩控制的任务。
- **动作表示**：MLP 头输出未来若干步的相对末端执行器位移和开合状态，受限于固定短序列预测，未测试高频或极高自由度动作空间。
- **模型规模**：被测试的 VLM 参数在 1B 至 10B 之间，更大模型的迁移特性尚未探索。
- **全参数微调成本**：需要更新 VLM 所有权重，对计算资源有一定要求；本文未探索参数高效微调（如 LoRA）在此框架下的效果。
- **预训练对齐性**：辅助具身 VQA 微调（如 Robobrain2、Vica332k）并未提升下游 VLA 性能，多数任务甚至导致轻微下降（Table 8），说明当前具身 VQA 预训练与 VLA 需求之间存在结构性错位。因此，VLM4VLA 目前假设直接从头端到端微调优于先进行额外的 VQA 适应步骤。

**局限与开放问题**

工作揭示了几个尚未解释的深层机制，构成未来研究的关键路径：
- **视觉编码器瓶颈的成因**：实验证实视觉模块是关键瓶颈，但为何视觉表征的适应性对下游控制远超语言部分？该现象背后的表征几何和优化动态尚未阐明。
- **通用能力与具身能力的度量鸿沟**：通用 VLM 基准得分与 VLA 性能呈弱相关甚至负相关（SimplerEnv 上 r=-0.321，Libero 上 r=0.381，Figure 3），暴露了现行 VQA 基准无法度量具身推理能力的缺陷。是否需要全新的视觉-动作基准来驱动预训练，仍为悬疑。
- **针对性预训练设计**：如何设计视觉预训练或辅助任务，才能直接提升控制表现？当前具身 VQA 任务的失败（Figure 4，Table 8）要求未来工作探索更贴近动作规划的监督形式，如轨迹预测、操控点定位、物体交互图等。
- **更复杂的动作解码器**：简单 MLP 头已展现出与扩散专家相匹配的性能，但在长序列、高精度或灵巧操作中，扩散模型或其他生成式头是否能够突破现有瓶颈，尚未在本文框架内验证。
- **域差距的系统性缩小**：VLM 预训练数据以自然图像和文本为主，而具身环境在纹理、光照、动力学上显著不同。如何通过数据混合、对比学习或数据增强使视觉编码器更快适应具身域，是一个开放的工程与科学问题。

## 原文 PDF

![[paperPDFs/ICLR_2026/VLM4VLA_Revisiting_Vision_Language_Models_in_Vision_Language_Action_Models.pdf]]
