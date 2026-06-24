---
title: "D3D-VLP: Dynamic 3D Vision-Language-Planning Model for Embodied Grounding and Navigation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/D3D_VLP_Dynamic_3D_Vision_Language_Planning_Model_for_Embodied_Grounding_and_Navigation.pdf
project_link: null
code_link: "https://github.com/MrZihan/D3D-VLP"
aliases:
- DV
- D3D-VLP
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 将规划、定位、导航统一为单一3D-VLM的自回归生成任务，并通过CoT Memory反馈循环实现状态化、动态重规划与组件间隐式梯度协同。
primary_logic: 动态3D思维链（3D CoT）将多步规划、3D定位与导航行动串行化为一个自回归多模态序列，配合碎片化监督协同学习（SLFS）仅利用损失掩码即可从海量混合部分标注数据中隐式训练各组件。
claims:
- D3D-VLP在R2R-CE上以61.3% SR和56.1% SPL达到新SOTA，比先前最强的端到端模型StreamVLN提升+4.4% SR，比模块化系统InternVLA-N1提升+3.1% SR，且比感知基线Dynam3D带来+8.4% SR的巨大提升。
- 消融实验显示，移除CoT Memory后，SG3D任务级准确率t-ACC从9.3暴跌至4.1，证实动态思维链记忆是长程序列任务的关键机制。
- SLFS策略使模型能从10M混合样本中学习，其中仅175K为全标注，其余为部分标注；掩码自回归损失使导航损失梯度反向传播至规划与定位模块，实现隐式协同训练。
- R2R-CE 上 SR↑ = 61.3
---

# D3D-VLP: Dynamic 3D Vision-Language-Planning Model for Embodied Grounding and Navigation

> [!tip] 核心洞察
> 动态3D思维链（3D CoT）将多步规划、3D定位与导航行动串行化为一个自回归多模态序列，配合碎片化监督协同学习（SLFS）仅利用损失掩码即可从海量混合部分标注数据中隐式训练各组件。

| 字段 | 内容 |
|------|------|
| 中文题名 | D3D-VLP：面向具身定位与导航的动态3D视觉-语言-规划模型 |
| 英文题名 | D3D-VLP: Dynamic 3D Vision-Language-Planning Model for Embodied Grounding and Navigation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.12622) · [Code](https://github.com/MrZihan/D3D-VLP) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | D3D-VLP |
| Dataset | R2R-CE, SG3D-Nav, HM3D-OVON |

> [!tip] 效果简介
> - R2R-CE 上，SR↑ 61.3 vs StreamVLN (56.9) (+4.4)；SPL↑ 56.1 vs StreamVLN (51.9) (+4.2)；SR↑ 61.3 vs InternVLA-N1 (58.2) (+3.1)。
> - SG3D-Nav 上，s-SR↑ 33.7 vs Dynam3D (先前最佳，约16.7) (+17.0 (approx.))。
> - HM3D-OVON 上，SR↑ 47.3 vs Aux-Think (42.7) (+4.6)。

## 概述

具身智能体在开放世界中执行长程任务，需要同时具备规划、三维定位与导航能力。然而，现有方法长期陷入两种范式的对立：**端到端模型**直接将指令映射为导航动作，缺乏可解释性与显式3D推理；**模块化系统**将规划、定位、导航拆分为独立组件，忽略组件间的相互依赖与协同，无法实现动态重规划。这一瓶颈导致二者在复杂长程任务中均难以取得突破。

D3D-VLP 的核心洞见在于：**将规划、定位与导航统一为单一3D视觉-语言模型的自回归生成任务**。具体而言，模型通过**动态3D思维链（3D CoT）**将多步规划、3D定位与导航行动串行化为一个自回归多模态序列，并引入**CoT Memory反馈循环**——将历史规划、已定位目标与智能体轨迹持续注入模型上下文，使智能体具备状态化的动态重规划能力。为从海量混合部分标注数据中隐式训练各组件，论文提出**碎片化监督协同学习（SLFS）**，仅通过损失掩码即可让导航损失的梯度反向传播至规划与定位模块，实现跨组件隐式梯度协同。

在R2R-CE基准上，D3D-VLP以**61.3% SR**和**56.1% SPL**达到新SOTA，比先前最强的端到端模型StreamVLN提升+4.4% SR，比最强模块化系统InternVLA-N1提升+3.1% SR。消融实验揭示，移除CoT Memory后SG3D任务级准确率从9.3暴跌至4.1，证实动态思维链记忆是长程序列任务的关键机制。

**方法谱系与知识库定位**：D3D-VLP处于端到端VLN与模块化具身系统的交叉点。它继承**Dynam3D**（Wang et al., NeurIPS 2025）的多级3D感知编码器作为感知骨架，借鉴**NVILA-Lite-2B**的预训练多模态能力作为推理核心，但在任务架构上根本区别于**StreamVLN**（Wei et al., arXiv 2025）、**NavFoM**（Zhang et al., arXiv 2025）等纯端到端方法，也不同于**InternVLA-N1**（InternNav Contributors, 2025）等LLM+导航的模块化调度范式。其统一自回归生成与CoT Memory设计，为具身模型的可解释性、动态适应性与跨组件协同学习提供了新的范式。

## 背景与动机

具身智能体的核心能力在于根据自然语言指令，在三维环境中执行多步定位与导航。近年来，端到端视觉-语言-导航（VLN）模型和模块化系统分别代表了该领域的两种主流范式，但二者均存在结构性缺陷。

**端到端模型**（如 **Dynam3D**（Wang et al., NeurIPS 2025）、**StreamVLN**（Wei et al., arXiv 2025）、**NavFoM**（Zhang et al., arXiv 2025））将指令直接映射为导航动作，虽然结构简洁，但缺乏可解释性与显式的3D推理能力。这类模型在长程任务中难以进行动态重规划，也无法显式地构建对场景的空间理解。

**模块化系统**（如 **InternVLA-N1**（InternNav Contributors, 2025））将任务拆解为独立的规划、定位和导航组件，通过LLM调度器进行串联。这种设计虽然提升了可解释性，但忽略了组件间的相互依赖与协同——规划模块不知道定位的精度边界，导航模块无法反向影响规划决策，各组件独立训练导致误差累积和次优整体性能。

**根本瓶颈在于**：现有方法要么牺牲可解释性换取端到端效率，要么牺牲协同性换取模块化灵活性，两者均无法实现动态重规划与跨组件联合学习。

针对这一缺口，D3D-VLP提出了一种统一范式：将规划、定位与导航重构为单一3D视觉-语言-规划模型中的自回归生成任务。其核心思路是通过动态3D思维链（3D CoT）将多步规划、3D定位与导航行动串行化为一个多模态序列，并引入CoT Memory反馈循环实现状态化推理与在线重规划。配合碎片化监督协同学习（SLFS）策略，模型仅利用损失掩码即可从海量混合部分标注数据中隐式训练各组件，解决了全标注数据稀缺的瓶颈。

## 核心创新

D3D-VLP 的核心创新在于将具身智能中原本割裂的规划、定位与导航三大组件，统一为**单一3D视觉-语言模型（3D-VLM）的自回归生成任务**，并通过**动态3D思维链（3D CoT）**与**碎片化监督协同学习（SLFS）**两大机制，从根本上解决了传统端到端模型缺乏可解释性与模块化系统忽略组件协同的瓶颈。

### 1. 统一自回归架构：从多阶段流水线到单一3D-VLM

传统方案分为两类：**端到端模型**（如 **StreamVLN**，Wei et al., arXiv 2025）直接将指令映射为导航动作，缺乏显式推理过程；**模块化系统**（如 **InternVLA-N1**，InternNav Contributors, 2025）将LLM规划、独立定位模块与导航执行器组装为流水线，但各组件独立训练，无法实现跨组件梯度协同，且面对动态环境时缺乏在线重规划能力。

D3D-VLP 的核心架构变革在于**将所有组件融合进一个统一的3D-VLM（基于NVILA-Lite-2B预训练）**，将多步规划、3D定位与导航行动串行化为一个自回归生成的多模态序列（Figure 3）。模型在每个时间步接收完整的多级3D视觉令牌、候选路点嵌入和历史思维链记忆，自回归生成包含“下一步计划→定位目标→导航动作→自然语言回答”的统一输出序列：

$$p(\boldsymbol{S}_t \mid \mathcal{T}, \mathcal{M}_t \oplus \mathcal{P}_t, \mathcal{C}_{t-1})$$

这一设计使得规划、定位与导航不再是孤立的模块输出，而是在共享的3D-VLM潜空间中**隐式协同**——导航损失可以通过自回归链反向传播至规划与定位的生成过程，实现真正的联合学习。

### 2. 动态3D思维链（3D CoT）与CoT Memory反馈循环

传统方法或采用“一次性规划”后盲目执行，或完全无历史状态，无法应对长程任务中的环境变化与执行偏差。D3D-VLP 引入了**CoT Memory反馈循环**作为关键创新：

$$\mathcal{C}_t = \mathrm{Concat}(\mathcal{C}_{t-1}, \mathrm{Parse}(S_t))$$

模型将历史规划、已定位目标与智能体轨迹持续反馈至当前推理的上下文中，使智能体成为**有状态、可感知自身进度**的动态推理系统。当环境变化或执行偏离预期时，模型可利用历史记忆进行**在线重规划**，而非从零开始重新推理。

这一机制的因果效应在消融实验中得到了最强证据：**移除CoT Memory后，SG3D-Nav基准上的定位准确率t-ACC从9.3暴跌至4.1**（Table 4），证实动态思维链记忆是长程序列任务不可或缺的核心机制。

### 3. 碎片化监督协同学习（SLFS）：从海量部分标注数据中隐式训练

具身数据标注成本极高，全标注样本稀缺。传统方法需要大量全标注数据独立训练各组件，限制了规模扩展。D3D-VLP 提出的**SLFS策略**彻底改变了这一范式：利用掩码自回归损失，使模型能从**约10M混合样本**中学习，其中仅**175K为全标注**，其余均为部分标注（Table 1）：

$$\mathcal{L}_{CoT} = \sum_{i \in \mathrm{Batch}} \sum_{k \in \mathrm{CoT}} \mathcal{H}_{i,k} \cdot \mathcal{L}_k (S_{\mathrm{pred},i}, S_{\mathrm{gt},i})$$

关键在于，掩码仅忽略缺失标注组件的损失计算，但**梯度仍通过共享的3D-VLM反向传播至整个CoT生成过程**。这意味着，即使某个样本只有导航标注而无规划标注，其导航损失仍能隐式监督和强化内部生成的规划与定位——实现了跨组件的隐式协同训练。消融实验证实，仅使用全标注数据训练时性能显著低于使用混合数据+掩码损失，验证了SLFS的增益。

### 4. 统一空间嵌入的动作空间

传统方法多使用文本动作（如“前进0.5米”）或离散动作空间，与3D视觉感知割裂。D3D-VLM 采用**基于路点预测的统一空间嵌入动作空间**：路点预测器从全景patch令牌中生成候选导航路点，模型直接选择路点作为导航动作。这一设计使动作选择与3D空间表示紧密耦合，消融实验表明，替换为文本动作空间后性能大幅下降（Table 4），验证了统一3D空间嵌入的有效性。

**总结**：D3D-VLP 的四项关键创新——统一自回归架构、CoT Memory反馈循环、SLFS训练策略与统一空间动作空间——形成了完整的因果闭环：统一架构使跨组件梯度协同成为可能，CoT Memory赋予模型动态重规划能力，SLFS解决了大规模训练的数据瓶颈，而空间嵌入动作空间则将3D感知与行动无缝衔接。这一创新组合在R2R-CE上以**61.3% SR**达到新SOTA，比先前最强端到端模型StreamVLN提升**+4.4% SR**，比最强模块化系统InternVLA-N1提升**+3.1% SR**（Table 2）。

## 整体框架

D3D-VLP 将具身智能中原本割裂的规划、3D 定位与导航统一为**单一 3D-VLM 的自回归生成任务**。其整体 pipeline 由四个核心模块串联成一个闭环：

1. **Dynam3D Encoder**（多级 3D 感知与记忆构建）：以流式带位姿的 RGB-D 图像为输入，持续更新一个动态的**多级 3D 记忆** $\mathcal{M}_t = (\mathcal{V}_{\mathrm{patch}}, \mathcal{M}_{\mathrm{inst}}, \mathcal{M}_{\mathrm{zone}})$，分别对应全景 patch 令牌、实例令牌和区域令牌。
2. **Waypoint Predictor**（路点预测器）：基于全景 patch 令牌和 12 个查询令牌，输出当前场景中可导航的候选路点及其 3D 空间嵌入 $(P_t, D_t, \cos(\theta_t), \sin(\theta_t))$，将动作空间从离散文本或固定步长提升为**统一的 3D 空间路点选择**。
3. **3D-VLM Core**（核心推理模型）：基于预训练的 NVILA-Lite-2B，接收自然语言指令 $\mathcal{T}$、多级 3D 令牌 $\mathcal{M}_t \oplus \mathcal{P}_t$、候选路点，以及来自 CoT Memory 的历史上下文 $\mathcal{C}_{t-1}$，自回归生成一条**统一的 3D 思维链（3D CoT）序列** $S_t$——该序列显式包含下一步计划、被定位的目标、选中的导航动作以及自然语言回答。
4. **CoT Memory**（思维链记忆反馈）：将当前输出 $S_t$ 解析为计划、定位、导航等组件，拼接到历史记忆中 $\mathcal{C}_t = \mathrm{Concat}(\mathcal{C}_{t-1}, \mathrm{Parse}(S_t))$，再反馈至下一时刻的模型输入，形成**状态化的动态重规划闭环**。

这一设计的关键因果机制在于：CoT Memory 使模型能够感知自身执行进度与历史决策，从而在长程任务中动态调整后续计划；而统一的 3D 空间嵌入动作空间则消除了文本动作与视觉感知之间的语义鸿沟。训练时，**碎片化监督协同学习（SLFS）** 通过掩码自回归损失 $\mathcal{L}_{CoT} = \sum_{i \in \mathrm{Batch}} \sum_{k \in \mathrm{CoT}} \mathcal{H}_{i,k} \cdot \mathcal{L}_k$，使来自导航损失的梯度能够沿共享的 3D-VLM 反向传播至规划与定位组件，实现**隐式跨组件协同训练**——即便大部分训练样本仅具有部分标注。

与既有范式的本质差异在于（Figure 1）：端到端模型将指令直接映射为导航动作，缺乏显式推理与可解释性；模块化系统则组装多个独立组件，忽略组件间相互依赖。D3D-VLP 以单一 3D-VLM 承载完整的“感知-规划-定位-执行”思维链，在统一架构内实现协同学习与动态规划。

![[assets/figures/papers/paper_list_l2180_https_arxiv_org_abs_2512_12622/figures/001_Figure_1.jpg]]
*Figure 1: Model Architecture Comparison. The end-to-end models directly map instructions to navigation actions, and modular systems assemble multiple specialized components. Our D3D-VLP employs a single 3D-VLM with 3D CoT to unify planning, grounding, and navigation for synergistic learning and planning*

### 补充图表

![[assets/figures/papers/paper_list_l2180_https_arxiv_org_abs_2512_12622/figures/002_Figure_2.jpg]]
*Figure 2: Framework of our D3D-VLP model. Given an instruction and streaming posed RGB-D images, a Dynam3D Encoder [56] builds and updates a Multi-level 3D Memory. This memory provides structured 3D tokens (i.e. panoramic patch, instance, and zone tokens) to the core D3D-VLP model and a Waypoint Predictor. Our D3D-VLP model then integrates these 3D tokens, the instruction, candidate waypoints, and historical context from the CoT Memory to autoregressively generate a unified 3D Chain-of-Thought (CoT) sequence, which includes the next plans, the grounded target, and the navigation action. Finally, this output updates the CoT Memory to create a dynamic feedback loop for stateful reasoning and replanning*

## 核心模块与公式推导

### 多级3D感知与记忆构建

D3D-VLP 的感知前端基于 **Dynam3D Encoder**（Wang et al., NeurIPS 2025），从流式输入的带位姿 RGB-D 图像中在线构建并更新动态的多级 3D 记忆。该记忆在时刻 $t$ 的结构化表示为：

$$\mathcal{M}_t = (\mathcal{V}_{\mathrm{patch}}, \mathcal{M}_{\mathrm{inst}}, \mathcal{M}_{\mathrm{zone}})$$

其中三个组件分别承担不同粒度的场景理解：
- **$\mathcal{V}_{\mathrm{patch}}$**：全景 patch 令牌，提供稠密的局部几何与纹理特征；
- **$\mathcal{M}_{\mathrm{inst}}$**：实例级令牌，编码物体级别的语义与空间信息；
- **$\mathcal{M}_{\mathrm{zone}}$**：区域级令牌，捕捉房间布局等大尺度空间上下文。

为将候选导航路点与 3D 场景显式对齐，模型对每个路点构造统一的空间嵌入。输入到 MLP 空间编码器的特征向量为：

$$(P_t, D_t, \cos(\theta_t), \sin(\theta_t))$$

其中 $P_t$ 为路点的 3D 坐标，$D_t$ 为智能体当前位置到该路点的相对距离，$\theta_t$ 为相对水平偏角。使用三角函数编码角度可避免角度周期性问题，使模型能自然学习方向敏感的空间关系。

### 统一自回归生成范式

D3D-VLP 的核心推理模块是一个基于预训练 **NVILA-Lite-2B** 的 3D-VLM。该模型将规划、3D 定位与导航行动统一为一个自回归生成任务，在每一时刻 $t$ 输出一条完整的多模态思维链序列 $\boldsymbol{S}_t$，其生成概率为：

$$p(\boldsymbol{S}_t \mid \mathcal{T}, \mathcal{M}_t \oplus \mathcal{P}_t, \mathcal{C}_{t-1})$$

各变量含义：
- **$\mathcal{T}$**：自然语言任务指令；
- **$\mathcal{M}_t \oplus \mathcal{P}_t$**：当前多级 3D 记忆与候选路点空间嵌入的拼接输入；
- **$\mathcal{C}_{t-1}$**：上一时刻的历史思维链记忆；
- **$\boldsymbol{S}_t$**：当前时刻自回归生成的完整输出序列，显式包含下一步规划、被定位的目标物体、选中的导航动作以及自然语言回答。

该公式的核心设计在于：模型并非仅输出导航动作，而是将中间推理步骤（规划与定位）也作为生成目标，从而形成可解释、可追溯的决策链路。

### CoT Memory 动态反馈机制

使 3D 思维链具备“动态”特性的关键组件是 CoT Memory 反馈循环。在每一步推理完成后，模型解析当前输出序列 $\boldsymbol{S}_t$ 中的规划、定位与导航令牌，并将其拼接到历史记忆中：

$$\mathcal{C}_t = \mathrm{Concat}(\mathcal{C}_{t-1}, \mathrm{Parse}(S_t))$$

这一机制使智能体成为**有状态**的推理体——模型上下文始终包含过去已执行的计划、已定位的目标以及已走过的轨迹。当环境发生变化或导航偏离预期时，模型可基于完整历史进行在线重规划，而非从零开始重新推理。消融实验为此提供了决定性证据：移除 CoT Memory 后，SG3D 任务级准确率 t-ACC 从 9.3 暴跌至 4.1，证实动态记忆是长程序列任务的瓶颈机制。

### 碎片化监督协同学习（SLFS）

训练策略是 D3D-VLP 能够从海量混合标注数据中学习的核心。SLFS 通过掩码自回归损失实现组件间的隐式协同训练：

$$\mathcal{L}_{CoT} = \sum_{i \in \mathrm{Batch}} \sum_{k \in \mathrm{CoT}} \mathcal{H}_{i,k} \cdot \mathcal{L}_k (S_{\mathrm{pred},i}, S_{\mathrm{gt},i})$$

其中：
- **$k \in \mathrm{CoT}$** 遍历思维链的各组件（规划、定位、导航、回答）；
- **$\mathcal{H}_{i,k}$** 为指示掩码：若样本 $i$ 的组件 $k$ 有标注则为 1，否则为 0；
- **$\mathcal{L}_k$** 为对应组件的交叉熵损失。

该公式的关键效应在于：即使某样本缺少导航标注，其规划与定位的损失梯度仍通过共享的 3D-VLM 主干网络反向传播，**隐式地强化导航能力**。同理，导航损失也会反向监督规划与定位模块。这使得模型能从约 10M 混合样本中学习，其中仅约 175K 为全标注数据，其余均为部分标注。消融实验表明，仅使用全标注数据训练时性能显著低于使用混合数据加掩码损失的配置，验证了 SLFS 的增益。

### 补充图表

![[assets/figures/papers/paper_list_l2180_https_arxiv_org_abs_2512_12622/figures/003_Figure_3.jpg]]
*Figure 3: The Unified Autoregressive Formulation of our D3D-VLP model. The core 3D Vision-Language-Planning model takes a comprehensive set of inputs: the natural language instruction, multi-level 3D visual tokens (i.e. panoramic, instance, and zone) , candidate waypoints, and the historical CoT Memory (including past plans and trajectory). It then autoregressively generates a single and unified 3D Chain-of-Thought (CoT) sequence. This multimodal output stream explicitly contains the next plans, the grounded target, the selected navigation action, and a natural language answer*

## 实验与分析

### 核心实验设置

D3D-VLP的训练采用碎片化监督协同学习（SLFS）策略，在约1000万混合标注样本上进行100K个episode的训练（约14天），使用4张RTX 6000 Ada GPU。模型以掩码自回归交叉熵损失进行优化，核心3D-VLM基于预训练的NVILA-Lite-2B初始化。评估涵盖多个具身导航基准，包括R2R-CE、SG3D-Nav、HM3D-OVON等，采用单目RGB-D输入。

### 主要结果

**Table 2**展示了D3D-VLP在R2R-CE基准上的全面评测结果。D3D-VLP以**61.3% SR**和**56.1% SPL**刷新了该基准的最高水平，相较于先前最强的端到端模型**StreamVLN**（Wei et al., arXiv 2025）提升**+4.4% SR**和**+4.2% SPL**，比**NavFoM**（Zhang et al., arXiv 2025）提升**+5.1% SR**和**+4.9% SPL**。值得注意的是，D3D-VLP甚至超越了最强调度基线——模块化系统**InternVLA-N1**（InternNav Contributors, 2025），领先**+3.1% SR**和**+2.1% SPL**。与仅具备感知能力的基线**Dynam3D**（Wang et al., NeurIPS 2025）相比，D3D-VLP带来了**+8.4% SR**和**+10.4% SPL**的巨大提升，充分证明了统一规划-定位-导航架构的增益。

在SG3D-Nav基准（**Table 3**）上，D3D-VLP在序列成功率（s-SR）上达到**33.7%**，大幅超越此前最佳结果（Dynam3D约16.7%），提升约**+17.0%**。该基准要求模型在长程任务中完成连续的3D定位与导航，其难度远高于单步导航。D3D-VLP在此任务上的优异表现直接验证了动态3D思维链（3D CoT）在长程序列推理中的关键作用。

![[assets/figures/papers/paper_list_l2180_https_arxiv_org_abs_2512_12622/figures/006_Table_3.jpg]]
*Table 3: Evaluation of task-oriented sequential grounding and navigation task on SG3D-Nav [70] benchmark*

在HM3D-OVON基准上，D3D-VLP以**47.3% SR**超越**Aux-Think**（Wang et al., arXiv 2025）的42.7%，提升**+4.6%**，进一步证明了模型在开放词汇目标导航任务上的泛化能力。

### 消融实验

**Table 4**的消融研究系统性地量化了各核心组件的贡献：

**CoT Memory的不可或缺性**：移除CoT Memory反馈循环后，SG3D-Nav上的目标定位准确率（t-ACC）从**9.3暴跌至4.1**，降幅超过55%。这一结果提供了最强证据，证明动态思维链记忆是长程序列任务的关键机制——没有历史状态反馈，模型无法有效追踪已完成的目标和剩余的子任务。

**路点预测动作空间的有效性**：将基于路点预测的统一空间嵌入动作空间替换为基于文本的动作空间（如“前进0.5米”）后，模型性能出现大幅下降。这验证了在3D-VLM中直接嵌入空间推理能力的重要性，文本动作无法有效传递精细的3D空间信息。

**SLFS策略的增益**：仅使用约175K全标注数据训练（无SLFS）时，模型性能显著低于使用混合数据+掩码损失的配置。SLFS通过掩码自回归损失，使导航损失的梯度能够反向传播至规划与定位模块，即使这些组件在部分样本中缺乏显式标注，也能实现隐式协同训练。这一机制是D3D-VLP能够从海量部分标注数据中学习的关键。

### 真实世界验证与局限性

**Table 5**展示了D3D-VLP在真实世界移动操作任务上的评估结果。在10个任务中，模型仅完成**3个**，成功率为30%。这一结果揭示了当前方法的显著局限：

1. **Sim-to-Real差距**：训练数据高度依赖Habitat、AI2-THOR等模拟器，真实世界的视觉噪声、动态光照和物理交互复杂性远超模拟环境，模型泛化能力不足。

2. **训练资源需求极高**：4张RTX 6000 Ada GPU训练14天的资源门槛限制了广泛复现和迭代优化。

3. **缺乏显式验证机制**：CoT生成可能产生不合理的计划或定位错误，当前架构缺乏对生成内容的显式验证与纠错机制，错误会沿思维链传播。

4. **传感器模态单一**：仅支持单目RGB-D输入，未利用LiDAR等传感器进一步强化3D感知精度。

### 失败模式分析

基于消融实验和真实世界测试，D3D-VLP的主要失败模式可归纳为：

- **长程记忆衰减**：尽管CoT Memory显著改善了长程序列性能，但在极长任务中，历史信息的累积仍可能导致上下文窗口溢出或注意力分散，需要进一步研究记忆压缩或选择性遗忘机制。
- **定位错误级联**：当3D定位出现偏差时，后续的导航动作选择会基于错误的空间锚点，导致任务失败。当前架构缺乏独立的定位校验环节。
- **规划不合理**：CoT生成的计划步骤可能不符合物理可行性或环境约束，模型缺乏对动作后果的预测能力。

### 补充图表

![[assets/figures/papers/paper_list_l2180_https_arxiv_org_abs_2512_12622/figures/005_Table_2.jpg]]
*Table 2: Evaluation of embodied navigation benchmarks with monocular camera, ∗ denotes zero-shot method*

![[assets/figures/papers/paper_list_l2180_https_arxiv_org_abs_2512_12622/figures/007_Table_4.jpg]]
*Table 4: Ablation study on components and training data*

![[assets/figures/papers/paper_list_l2180_https_arxiv_org_abs_2512_12622/figures/004_Table_1.jpg]]
*Table 1: Composition of sample annotations in our constructed 3D CoT dataset. The fully annotated gold data is about 175K, and the partially annotated data is about 9.9M*

![[assets/figures/papers/paper_list_l2180_https_arxiv_org_abs_2512_12622/figures/009_Table_5.jpg]]
*Table 5: Evaluation of real-world mobile manipulation task*

![[assets/figures/papers/paper_list_l2180_https_arxiv_org_abs_2512_12622/figures/008_Figure_4.jpg]]
*Figure 4: A demonstration of real-world mobile manipulation task*

## 方法谱系与知识库定位

### 核心瓶颈与创新锚点

当前具身视觉语言导航（VLN）领域存在两条主要技术路线，但各自面临结构性瓶颈：（1）**端到端模型**（如 **StreamVLN**（Wei et al., arXiv 2025）、**NavFoM**（Zhang et al., arXiv 2025）、**NaVid**（Zhang et al., RSS 2024））直接将指令映射为导航动作，缺乏可解释的中间推理与显式3D空间理解，难以应对需要多步规划与动态重规划的复杂任务；（2）**模块化系统**（如 **InternVLA-N1**（InternNav Contributors, 2025）、**VLFM**（Yokoyama et al., ICRA 2024））将规划、定位、导航拆分为独立组件，虽具备一定可解释性，但组件间相互依赖被忽略，无法实现跨模块联合学习与梯度协同。

D3D-VLP 的核心创新在于**将规划、3D定位与导航统一为单一3D-VLM的自回归生成任务**，并通过**动态3D思维链（3D CoT）**与**CoT Memory反馈循环**实现状态化推理与在线重规划。这一设计从根本上改变了信息流：不再是模块间的单向传递或端到端的黑箱映射，而是将多步规划、目标定位与导航行动串行化为一个自回归多模态序列，使各组件在共享表征空间中隐式协同。

### 技术谱系与关系定位

#### 感知基线的继承与超越

D3D-VLP 直接继承 **Dynam3D**（Wang et al., NeurIPS 2025）的3D编码器，用于从流式RGB-D图像构建多级3D记忆（全景patch令牌、实例令牌、区域令牌）。Dynam3D 本身是一个端到端VLN模型，D3D-VLP 将其作为感知前端，但在此基础上叠加了规划与定位能力，使同一3D表征服务于更完整的推理链。实验表明，D3D-VLP 相较 Dynam3D 在 R2R-CE 上带来 **+8.4% SR** 和 **+10.4% SPL** 的显著提升（Section 4.2），证明感知能力的增益必须与高层推理协同才能充分释放。

#### 与端到端方法的对比

- **StreamVLN**（Wei et al., arXiv 2025）是先前R2R-CE上的端到端SOTA（SR 56.9%），D3D-VLP 以 **61.3% SR（+4.4%）** 超越，且路径效率（SPL）同步提升 **+4.2%**。这一差距表明，显式3D思维链推理优于隐式端到端映射。
- **NavFoM**（Zhang et al., arXiv 2025）作为端到端导航基础模型，D3D-VLP 对其SR优势达 **+5.1%**，进一步验证统一规划-定位-导航架构的有效性。
- **Uni-NaVid**（Zhang et al., arXiv 2024）和 **NaVid**（Zhang et al., RSS 2024）均为视频VLM驱动的多任务导航方法，但缺乏显式3D定位与动态重规划机制。D3D-VLP 在 HM3D-OVON 上以 **47.3% SR** 超越 **Aux-Think**（Wang et al., arXiv 2025）的 42.7%（+4.6%），在SG3D-Nav上相较 Dynam3D 的 s-SR 提升约 **+17.0%**（Table 3），凸显3D CoT在长程任务中的关键作用。

#### 与模块化系统的对比

**InternVLA-N1**（InternNav Contributors, 2025）作为最强调度基线，采用LLM规划+导航执行的两阶段流水线，D3D-VLP 对其SR优势为 **+3.1%**（61.3% vs 58.2%），SPL优势 **+2.1%**。这一对比说明，即使模块化系统使用强大的LLM规划器，组件间的信息隔离仍限制了整体性能上限。D3D-VLP 通过 CoT Memory 实现了规划-定位-导航的闭环反馈，使历史决策信息持续影响当前推理，这是模块化流水线难以实现的。

#### 零样本方法的参照

**VLFM**（Yokoyama et al., ICRA 2024）代表零样本语义导航的模块化路线，依赖预训练视觉语言模型进行目标定位。D3D-VLP 的训练范式与之不同——通过碎片化监督协同学习（SLFS）从大规模混合部分标注数据中学习，而非零样本迁移，因此在需要精细3D空间推理的任务上具有天然优势。

### 适用边界

1. **输入模态约束**：模型仅支持单视角RGB-D流式输入，未利用LiDAR或多视角融合，在遮挡严重或纹理稀疏的3D场景中感知鲁棒性可能受限。
2. **任务范围**：当前聚焦于室内具身导航与目标定位（R2R-CE、SG3D-Nav、HM3D-OVON），向移动操作（仅完成3/10真实世界任务，Table 5）和交互式任务的泛化尚不充分。
3. **环境依赖**：训练数据高度依赖 Habitat、AI2-THOR 等模拟器，Sim-to-Real 差距尚未量化，真实世界部署的感知漂移与动力学不确定性可能影响CoT推理链的稳定性。
4. **计算成本**：训练需 4×RTX 6000 Ada GPU 持续14天（约100K episodes），对资源受限的研究团队复现门槛较高。

### 局限与开放问题

#### 已知局限

- **CoT生成缺乏显式验证**：模型自回归生成的规划与定位结果可能包含不合理的目标或错误的空间推理，当前架构缺少显式的几何验证或一致性检查机制，错误可能沿CoT链传播。
- **真实世界泛化不足**：真实世界移动操作任务仅完成3/10（Table 5），说明从模拟器到物理环境的策略迁移仍存在显著差距，尤其是在动态障碍物和复杂光照条件下。
- **训练数据偏差**：SLFS策略虽能利用部分标注数据，但全标注“金标”数据仅约175K（Table 1），模型可能过度拟合模拟器特有的视觉纹理和场景布局。
- **评价指标单一**：当前主要依赖SR和SPL等成功率与路径效率指标，未考虑安全性、能源消耗、实时性等实际部署维度。

#### 开放问题

1. **强化学习与CoT的融合**：未来可引入强化学习优化CoT生成策略，使模型在探索过程中自适应调整规划粒度与重规划时机，提升长程任务的鲁棒性。
2. **任务边界的扩展**：如何将统一3D CoT范式扩展到更广泛的具身任务（如移动操作、人机交互、多智能体协作），需要重新定义CoT序列的结构与语义。
3. **高效训练与模型压缩**：探索LoRA微调、知识蒸馏或混合精度训练策略，降低对4×高端GPU的依赖，使方法在更广泛的学术环境中可复现。
4. **3D场景先验的注入**：利用房间布局、对象共现关系、语义地图等结构化先验（如Figure 5所示的实例级点云与语言描述），可能进一步提升长期任务的成功率与规划合理性。
5. **安全性与可解释性**：在真实部署中，CoT序列本身可作为可解释性输出，但如何确保规划的安全性（如避免碰撞、遵守社交规范）仍需额外约束机制。

### 关键证据强度评估

| 主张 | 证据强度 | 说明 |
|------|---------|------|
| D3D-VLP在R2R-CE上达到新SOTA | **强** | Table 2提供多方法对比，SR 61.3%显著超越StreamVLN（56.9%）和InternVLA-N1（58.2%），置信度0.98 |
| CoT Memory是长程任务关键机制 | **强** | Table 4消融显示移除CoT Memory后SG3D t-ACC从9.3暴跌至4.1，置信度0.95 |
| SLFS使部分标注数据有效协同训练 | **中强** | Table 4消融验证混合数据+掩码损失优于仅全标注数据，但缺少对不同部分标注比例的系统消融，置信度0.95 |
| 真实世界泛化能力 | **弱** | 仅10个真实世界任务、3个成功，样本量过小且缺少统计显著性检验，需更大规模验证 |
| 路点预测动作空间优于文本动作 | **中强** | Table 4消融支持该结论，但未对比其他动作表示（如连续控制），置信度0.95 |

## 原文 PDF

![[paperPDFs/CVPR_2026/D3D_VLP_Dynamic_3D_Vision_Language_Planning_Model_for_Embodied_Grounding_and_Navigation.pdf]]