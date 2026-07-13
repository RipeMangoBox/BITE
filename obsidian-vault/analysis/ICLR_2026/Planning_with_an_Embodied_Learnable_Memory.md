---
title: "Planning with an Embodied Learnable Memory"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Planning_with_an_Embodied_Learnable_Memory.pdf
project_link: null
code_link: null
openreview_forum_id: 79BOATBal9
aliases:
- EPME
- PELM
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/vision_models_multimodal
core_operator: "EPM作为单一可学习VLM，通过离散操作（添加、更新、删除）维护文本化的环境表示，使规划器无需显式查询即可直接利用。"
primary_logic: "将记忆更新建模为VLM的序列预测任务，能够端到端学习动态场景跟踪，并结合人类演示重放和难度感知RL（DDAFT）训练鲁棒的规划器。"
claims:
- "EPM以单一VLM实现添加、移除、更新操作，统一处理动态场景。"
- "EPM编码具有3D坐标和自然语言描述的对象中心表示。"
- "采用人类演示和DDAFT训练的规划器在PARTNR基准上成功率的绝对提升高达55%。"
- "即使在基线具有真实感知时，我们的方法仍优于它们。"
---

# Planning with an Embodied Learnable Memory

> [!tip] 核心洞察
> 将记忆更新建模为VLM的序列预测任务，能够端到端学习动态场景跟踪，并结合人类演示重放和难度感知RL（DDAFT）训练鲁棒的规划器。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 基于具身可学习记忆的规划 |
| 英文题名 | Planning with an Embodied Learnable Memory |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=79BOATBal9) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal |
| Method | Embodied Perception Memory (EPM) |
| Dataset | PARTNR (single-agent), Spot-Indoor |

> [!tip] 效果简介
> - PARTNR (single-agent) 上，Success Rate 为 HD+DDAFT (learned perception) 0.58 ± 0.02，对比 DynaMem (learned perception) 0.03 ± 0.01，变化 +0.55。
> - PARTNR (single-agent) 上，Success Rate 为 HD+DDAFT (learned perception) 0.58 ± 0.02，对比 PP (learned perception) 0.46，变化 +0.12。
> - PARTNR (single-agent) 上，Success Rate 为 HD+DDAFT (GT perception) 0.68 ± 0.02，对比 PP (GT perception) 0.51，变化 +0.17。

## 概要

### 问题背景与瓶颈

具身智能体在动态大规模环境中执行长期任务时，面临一个根本性挑战：如何构建和维护一个能够跟踪物体移动、添加与消失的环境记忆。现有方法存在三类核心瓶颈：

1. **动态适应不足**：主流记忆表示（如**ConceptFusion** (Jatavallabhula et al., RSS 2023)、**ConceptGraphs** (Gu et al., ICRA 2024)、**3D-Mem** (Yang et al., CVPR 2025)）依赖多模型流水线与启发式规则，难以鲁棒地处理物体移动、重关联与错误校正。
2. **计算开销与集成复杂**：系统由多个独立模块拼凑而成，需显式查询才能检索信息，阻碍与语言模型规划器的无缝衔接。
3. **规划器训练低效**：现有规划器多为零样本LLM或仅依赖有限人类演示微调，缺乏对感知噪声的鲁棒性。

### 核心方法：具身可学习记忆（EPM）

本文提出**Embodied Perception Memory (EPM)**，一个单一的可学习视觉-语言模型（VLM），通过离散操作（添加、更新、删除）维护文本化的环境表示。其核心洞察在于：将记忆更新建模为VLM的序列预测任务，端到端学习动态场景跟踪。EPM编码对象中心表示，每个物体以3D坐标和自然语言状态描述表征，无需显式查询即可被规划器直接利用。

规划器方面，本文引入两种互补的训练策略：**人类演示重放**（从遥操作数据中提取规划轨迹，并注入探索动作）与**DDAFT**（Dynamic Difficulty-Aware Fine-Tuning），一种无价值函数的在线强化学习方法，通过动态调整采样难度提升训练效率。

### 主要结果

在PARTNR单智能体基准上，EPM结合所提规划训练方法取得了显著提升：

- 相较于强基线**DynaMem** (Liu et al., arXiv 2024)，成功率绝对提升**55%**（0.58 vs 0.03）。
- 相较于零样本规划器**PP** (Chang et al., ICLR 2025)，提升**12%**。
- 即使基线方法获得真实感知信息（GT perception），本文方法仍保持优势，GT感知下成功率达**0.68**，超越PP的0.51。

### 方法定位

EPM在记忆表示谱系中占据独特位置（Table 1）：它是首个同时满足开放词汇、对象关系编码、动态更新、无需显式查询、单一模型、错误校正六项能力的系统。在规划层面，DDAFT与人类演示重放的组合将规划器训练从零样本范式推向在线自适应微调，为具身规划中的感知-规划协同优化提供了新路径。



具身智能体在动态、大规模家庭环境中执行长期任务（如整理房间、取送物品）时，需要持续感知环境变化并据此调整规划。这一能力的核心瓶颈在于**记忆表示**——智能体如何从自我中心的流式观察中构建并维护对环境的理解。

现有记忆表示方法普遍存在三个结构性缺陷。其一，**动态更新能力弱**：多数方法（如 **ConceptFusion** (Jatavallabhula et al., RSS 2023)、**ConceptGraphs** (Gu et al., ICRA 2024)、**3D-Mem** (Yang et al., CVPR 2025)）假设静态场景，无法处理物体移动、移除或状态变化。少数支持动态更新的方法（如 **DynaMem** (Liu et al., arXiv 2024)）依赖启发式规则与阈值进行物体重关联和校正，在复杂场景中容易失效。其二，**计算架构冗余**：主流方案采用多模型流水线（如点云处理 + CLIP 特征提取 + 显式查询接口），系统复杂度高且难以端到端优化。其三，**规划器与记忆解耦**：规划器必须通过显式查询才能从记忆模块中检索信息，记忆本身并不直接适配规划器的推理需求。

从规划训练的角度看，现有方案同样存在缺口。零样本 LLM 规划器（如 **PP (PARTNR-Pretrained)** (Chang et al., ICLR 2025)）虽具备一定泛化能力，但缺乏对具体环境动态的适应。仅用人类演示微调虽能注入任务先验，却受限于演示的次优性和分布覆盖不足，难以应对探索需求。

本文的核心动机在于：**能否将记忆更新建模为单一可学习 VLM 的序列预测任务，使记忆模块直接输出规划器可消费的文本化环境表示，并通过人类演示重放与难度感知强化学习联合训练，实现感知与规划的高效协同？** 这一思路旨在消除多模型集成的启发式依赖，让记忆的维护与校正成为可端到端学习的能力，同时让规划器在训练中主动适应感知噪声与任务难度。



## 核心方法与创新机理

本工作针对具身规划中记忆表示的核心瓶颈——动态环境跟踪困难、多模型流水线计算开销大、依赖启发式规则集成、以及规划器需要显式查询才能检索信息——提出了三个层次的关键创新，构成一个从感知到规划的完整闭环。

### 创新一：单一VLM端到端维护文本化动态记忆

传统具身记忆系统（如 **ConceptFusion** (Jatavallabhula et al., RSS 2023)、**ConceptGraphs** (Gu et al., ICRA 2024)、**3D-Mem** (Yang et al., CVPR 2025)）通常依赖多模型流水线，分别处理点云、CLIP特征和语义映射，并通过启发式阈值判断物体是否移动或被移除。**EPM (Embodied Perception Memory)** 将这一复杂流程统一为单一VLM的序列预测任务：给定上一时刻的文本化环境状态 $M^{t-1}$、当前自我中心RGB观察 $o^t$、以及智能体动作 $a^t$，模型直接预测一组离散操作（Add、Update、Remove、No updates），通过函数 $M^{t} = f(M^{t-1}, o^{t}, a^{t})$ 更新环境表示。这种设计将物体重关联与错误校正内化于模型的学习过程中，避免了手工阈值和启发式规则带来的脆弱性。

### 创新二：无需显式查询的对象中心文本表示

EPM输出的环境状态 $M^t$ 采用对象中心表示，每个物体由其3D坐标和自然语言描述（包含状态与上下文信息）共同表征。与需要规划器主动查询才能检索信息的记忆系统（如 **DynaMem** (Liu et al., arXiv 2024) 的网格化记忆需通过体素-查询对齐分数进行探索）不同，EPM直接生成结构化的文本表示，使高层LLM规划器可以无缝、即时地利用完整的环境信息。这一“无查询”特性在 Table 1 中被列为EPM区别于其他记忆表示的关键能力之一。

### 创新三：人类演示重放与难度感知RL联合训练规划器

规划器训练面临两个核心挑战：如何从人类遥操作演示中提取适用于在线感知系统的规划轨迹，以及如何高效地进行在线强化学习微调。本工作提出了一套完整的训练策略：

1. **演示轨迹重放**：在仿真环境中回放人类演示，同时运行EPM在线感知，使规划轨迹适配感知系统的实际输出；通过推断探索动作序列教会智能体主动搜索，并移除未能推进任务进展的次优交互片段（Figure 3）。

2. **DDAFT (Dynamic Difficulty-Aware Fine-Tuning)**：一种无需价值函数的在线RL方法，通过动态调整任务指令的采样难度分布来提升样本效率——优先采样当前策略表现较差的困难指令，使训练聚焦于能力边界。

实验证据表明，HD（仅人类演示训练）在GT感知下使用8B参数的LLM即超越了70B参数的零样本PP（**PARTNR-Pretrained** (Chang et al., ICLR 2025)）模型，成功率提升0.12；DDAFT在此基础上进一步将PP和HD的成功率分别提升0.15和0.05。在learned perception设置下，HD+DDAFT相对于DynaMem和PP分别实现了55%和12%的绝对成功率提升，证明了从记忆表示到规划训练的端到端创新链条的有效性。



![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_79BOATBal9/figures/001_Figure_1.jpg]]
*Figure 1: We present a memory representation for embodied planing in large-scale environments. Our method includes Embodied Perception Memory (EPM), a VLM-based system that represents the environment from egocentric observations. Our novel LLM-based planner trained with human demonstrations and RL reason over EPM to plan agent actions*

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_79BOATBal9/figures/002_Table_1.jpg]]
*Table 1: Comparison to different memory representations. We compare EPM with other popular embodied memory representations. Object Relationships: whether object-furniture relationships are encoded. Dynamics: whether the representation allows for a changing environment. No Query: whether the representation needs to be queried to retrieve information*

本文提出一个面向大规模动态环境的具身规划系统，其核心由两个模块构成：**具身感知记忆（Embodied Perception Memory, EPM）** 和 **高层次LLM规划器**。系统以自我中心（egocentric）的RGB观察为输入，通过EPM维护一个文本化的环境状态，规划器再基于该状态生成高层次动作，最终由特权技能策略转换为低层控制指令。图1展示了这一完整流水线。

### 系统流水线

整个系统遵循“感知→记忆更新→规划→执行”的闭环结构：

1. **感知输入**：智能体在每个时间步接收自我中心的RGB图像观察 $o^t$、自身位姿信息以及上一时刻执行的动作 $a^{t-1}$。
2. **记忆更新（EPM）**：EPM作为单一VLM，接收上述输入及当前文本化环境状态 $M^{t-1}$，预测一组离散操作（Add、Update、Remove、No updates），生成更新后的环境表示 $M^t$。该过程可形式化为：
   $$M^{t} = f(M^{t-1}, o^{t}, a^{t})$$
   其中 $f$ 由EPM的VLM端到端学习得到，无需显式查询即可直接输出环境文本。
3. **高层次规划**：LLM规划器采用ReAct范式，接收任务描述 $\omega$ 和EPM输出的环境状态 $M^t$，生成高层次动作（如导航至某物体、拾取物品等）。
4. **低层执行**：技能策略将高层次动作转换为具体控制指令（导航、拾取、放置等），完成与环境的交互。

### 模块关系与数据流

系统采用两层控制架构，各模块间的数据流关系如下：

- **EPM → 规划器**：EPM维护的环境状态 $M^t$ 直接作为规划器的提示（prompt）输入，无需规划器显式查询记忆。这是EPM区别于DynaMem等需要显式检索的记忆系统的关键设计——EPM以文本形式直接呈现所有已知实体及其关系，实现与LLM规划器的无缝集成。
- **规划器 → 技能策略**：规划器输出的高层次动作被翻译为低层技能调用。为隔离感知与规划的影响，所有方法共享相同的特权技能策略。
- **EPM内部**：EPM将记忆更新建模为序列预测任务。给定RGB观察、文本化环境状态、机器人动作和智能体位姿，VLM直接预测Add/Update/Remove/No updates四类操作。对象的**重关联（re-association）与校正**均在EPM内部学习完成，避免了传统方法中的启发式规则与阈值设定。

### 规划器训练管线

规划器的训练分为两个阶段：

- **人类演示重放**：在仿真环境中回放人类遥操作数据，同时在线运行感知系统，生成与EPM输出分布一致的规划轨迹。为适应感知噪声并教导探索行为，系统推断并插入探索动作序列；同时剔除未能推进任务进展的次优交互。
- **DDAFT在线微调**：提出**动态难度感知微调（Dynamic Difficulty-Aware Fine-Tuning, DDAFT）**，一种无价值函数的在线RL方法。DDAFT通过动态调整任务指令的采样难度分布，使规划器在训练过程中逐步面对更具挑战性的场景，从而提升采样效率和策略鲁棒性。

### 与其他记忆表示的系统性对比

表1从六个维度对比了EPM与主流具身记忆表示（ConceptFusion、ConceptGraphs、3D-Mem、DynaMem）的能力差异。EPM是唯一同时满足**单一模型（Single Model）**、**无需显式查询（No Query）**、**支持动态环境（Dynamics）**、**编码对象关系（Object Relationships）** 和**具备错误校正能力（Error Correction）** 的方法。这一架构统一性使得EPM在动态场景中避免了多模型流水线的累积误差和计算开销。



### 环境状态的形式化定义

具身规划的核心是维护一个随时间演化的环境表示。本文将该过程形式化为一个状态更新函数：

$$M^{t} = f(M^{t-1}, o^{t}, a^{t})$$

其中：
- $M^{t}$ 是时刻 $t$ 的环境记忆状态；
- $M^{t-1}$ 是上一时刻的记忆状态；
- $o^{t}$ 是当前时刻的自我中心观察（RGB图像）；
- $a^{t}$ 是机器人执行的动作；
- $f$ 是将历史记忆、当前观察和动作映射为新记忆状态的更新函数。

该公式定义了具身感知记忆的核心问题：如何在动态环境中，基于不完整的自我中心观察，持续更新对场景的理解。

### 记忆表示：对象中心化的文本编码

EPM 采用**对象中心化**的表示方式。每个对象由两个要素刻画：

- **3D空间坐标**：对象在环境中的位置；
- **自然语言描述**：对象的状态、类别及其与家具/容器的关系（如“放在沙发上的剪刀”）。

这种设计的因果机制在于：文本表示天然适配LLM规划器的输入接口，避免了传统方法中需要显式查询记忆才能检索信息的瓶颈。同时，对象-家具关系的编码使规划器能够推理物体之间的空间依赖（如“抽屉里的遥控器”），这是纯空间坐标表示无法提供的语义信息。

### EPM更新操作：离散操作集

EPM将记忆更新建模为VLM的序列预测任务，输出四种离散操作：

| 操作类型 | 功能 | 触发场景 |
|---------|------|---------|
| **Add** | 向记忆中添加新对象及其3D坐标和描述 | 探索新区域或发现先前未见的物体 |
| **Update** | 修改已有对象的属性（位置、状态、关系） | 物体被移动或状态改变 |
| **Remove** | 从记忆中删除对象 | 物体被移走或确认之前的检测为误检 |
| **No updates** | 保持记忆不变 | 当前观察未发现需要记录的变化 |

**关键机制**：VLM接收RGB观察、文本化的当前记忆状态、机器人动作和位姿作为输入，直接预测应执行的操作序列。重关联（re-association）和纠错（correction）被内化在VLM的学习过程中，**避免**了传统方法（如DynaMem）依赖启发式规则和阈值进行物体匹配的脆弱性。

### 规划器架构：两级控制

规划器采用**两级控制架构**：

1. **高层规划器（LLM-based）**：接收任务描述 $\omega$ 和EPM输出的环境状态 $M^{t}$，使用ReAct范式生成高层动作（如“导航到客厅”、“拿起剪刀”）。该层基于Llama模型，通过人类演示重放和DDAFT进行微调。

2. **低层技能策略（Skill Policy）**：将高层动作翻译为具体的运动控制指令（导航、拾取、放置、打开抽屉等）。在实验中，该层使用**特权技能**以隔离感知与规划的影响——这意味着所有对比方法共享相同的低层执行能力，性能差异完全归因于记忆表示和规划策略。

### 规划器训练：人类演示重放 + DDAFT

训练数据的生成遵循一个关键流程（见Figure 3）：

1. **演示重放**：在仿真环境中回放人类遥操作轨迹，同时运行感知系统（EPM）在线生成观察-记忆对；
2. **探索动作注入**：推断并插入探索动作序列，使训练轨迹适应感知系统的不确定性，并教会规划器主动探索；
3. **次优轨迹清洗**：移除未能推进任务进度的人类交互，缓解演示数据中的次优行为。

**DDAFT（Dynamic Difficulty-Aware Fine-Tuning）** 是一种**无价值函数**的在线RL方法。其核心机制是：在微调过程中动态调整采样任务的难度分布，使训练集中在规划器当前表现较差的任务上，从而提高样本效率。消融实验证实，DDAFT在GT感知下将PP的成功率提升0.15，将HD提升0.05。

### 模块间依赖关系

EPM作为独立的感知模块，与规划器之间通过**文本化的环境状态**解耦。这意味着：
- 感知评估可以脱离规划回路独立进行（Table 2）；
- 规划器可以在GT感知或learned感知两种设置下运行，以分别衡量规划和感知的贡献（Table 3）；
- 记忆表示本身不依赖特定的规划器架构——PP（零样本LLM）和HD（微调LLM）均可使用相同的EPM输出。



## 实验与关键发现

### 感知评估：EPM 的独立记忆追踪能力

在 PARTNR 仿真数据集上，EPM 的节点 F1 达到 **0.34**，边 F1 达到 **0.46**，显著优于 DynaMem（节点 F1 0.17，边 F1 0.17）和 GPT-4o（节点 F1 0.04，边 F1 0.04）（Table 2）。这一优势的核心机制在于 EPM 通过单一 VLM 端到端地学习 Add/Update/Remove 操作，避免了 DynaMem 依赖启发式阈值进行物体重关联所引入的累积误差。GPT-4o 作为零样本 VLM 直接预测环境图，其极低的边 F1 表明缺乏显式记忆更新机制时，VLM 难以维持跨时间步的对象间关系一致性。


![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_79BOATBal9/figures/006_Table_2.jpg]]
*Table 2: Perception-only Results. Perception evaluation outside the planning loop*

然而，在真实世界 Spot-Indoor 数据集上，EPM 的节点 F1 下降至 **0.24**，甚至低于 DynaMem 的 0.51（Table 2）。这一性能反转揭示了 EPM 的关键瓶颈：纯文本表示在真实世界复杂场景中面临物体分类和重关联的挑战。定性结果（Fig. 4 右）显示，EPM 在真实场景中出现了物体类别误判和多实例混淆，而 DynaMem 依赖点云特征匹配的显式查询机制在此类场景下反而更鲁棒。这暗示当前 EPM 的 VLM 训练数据（仅限仿真）不足以覆盖真实世界的视觉多样性。

### 规划评估：EPM 与规划器训练的协同效应

Table 3 展示了 PARTNR 单智能体基准上的完整规划结果，揭示了三个关键发现。


![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_79BOATBal9/figures/007_Table_3.jpg]]
*Table 3: Planning Results. Results on the PARTNR single-agent benchmark. We pair planners with various forms of memory in the groundtruth (top) and learned (bottom) perception settings*

**人类演示训练的有效性。** 在真实感知（GT perception）设置下，仅使用人类演示轨迹微调的 HD 方法（Llama3.1-8b-Instruct）成功率达到 **0.56 ± 0.02**，比零样本 PP 方法（Llama3.3-70b-Instruct）高出 0.12（row 4 vs row 2）。这证明从人类演示中重放并适配感知系统的训练策略，即使使用小得多的模型（8b vs 70b），也能有效教会规划器理解 EPM 的文本化环境表示并做出合理决策。

**DDAFT 的增益模式。** 在 GT 感知下，DDAFT 对 PP 的提升为 **0.15**（从 0.51 到 0.66），而对 HD 的提升仅为 **0.05**（从 0.56 到 0.68）（Table 3 rows 2-5）。这种差异化的增益模式表明：零样本 PP 的规划策略存在大量次优行为，DDAFT 通过动态调整采样难度有效纠正了这些缺陷；而 HD 从人类演示中已学到较强的先验策略，DDAFT 的边际改进空间较小。值得注意的是，HD+DDAFT 在 GT 感知下达到最高的 **0.68 ± 0.02** 成功率，验证了人类先验与在线强化学习微调的互补性。

**学习感知下的闭环性能。** 在学习感知（learned perception）设置下，HD+DDAFT 成功率达到 **0.58 ± 0.02**，比 DynaMem 的 0.03 高出 **55 个百分点**，比 PP 的 0.46 高出 **12 个百分点**（Table 3 rows 8-10）。DynaMem 的极低成功率（0.03）表明其显式查询机制在规划闭环中严重失效——规划器无法有效利用基于体素和 CLIP 特征的多模态记忆来生成合理的探索与操作动作。相比之下，EPM 的文本化记忆天然适配 LLM 规划器，无需额外查询即可直接作为提示的一部分，这是闭环性能大幅领先的根本原因。

消融实验进一步揭示：PP+DDAFT 和 HD+DDAFT 在学习感知下均达到 0.58 成功率，说明 DDAFT 在线微调能够有效补偿 EPM 感知误差对规划的影响，使得两种初始化策略收敛到相近的性能水平。

### 失败模式与局限

尽管整体性能显著优于基线，EPM-规划器系统仍存在明确的失败模式。首先，在真实世界感知评估中，EPM 的节点 F1 仅为 0.24，物体分类错误和多实例重关联失败是主要问题。其次，纯文本记忆表示可能遗漏需要视觉推理的对象属性（如液体状态、精细几何形状），这在需要精确物理交互的任务中可能成为瓶颈。此外，当前规划器依赖特权技能策略执行低层动作，实际部署中替换为基于学习的技能模块可能引入额外的控制误差。最后，训练数据完全来自仿真环境，在真实世界动态场景中进行完整规划任务训练留待未来工作。



## 定位与知识库关联

### 与现有记忆表示的关系

EPM 的定位可以从 **Table 1** 的系统对比中清晰看出。现有具身记忆表示通常依赖多模型流水线或显式查询机制，EPM 则以单一可学习 VLM 统一了记忆的构建、更新与检索。

- **ConceptFusion**（Jatavallabhula et al., RSS 2023）与 **ConceptGraphs**（Gu et al., ICRA 2024）均支持开放词汇的对象识别与对象-家具关系编码，但两者都缺乏对动态环境（物体移动、增减）的原生支持，且不具备错误校正能力。ConceptFusion 需要显式查询才能检索信息，ConceptGraphs 同样如此。
- **3D-Mem**（Yang et al., CVPR 2025）引入了动态环境支持，但仍依赖多模型集成，且需要显式查询。
- **DynaMem**（Liu et al., arXiv 2024）是本文的主要对比基线，它支持开放词汇、动态更新，且无需显式查询。然而，其更新策略依赖启发式规则与阈值（如基于体素最后观测时间戳和查询对齐分数的探索前沿识别），重关联与校正并非端到端学习。此外，DynaMem 仍然采用多模型流水线，而非单一模型。
- **EPM** 在所有六个维度上均满足要求：开放词汇、对象关系编码、动态环境支持、错误校正、无需查询、单一模型。其核心差异在于将记忆更新建模为 VLM 的序列预测任务——通过 Add、Update、Remove、No updates 四种离散操作直接修改文本化的环境表示 $M^t$，使重关联与校正内化于模型学习中，避免了手工启发式规则。

### 与现有规划方法的关系

在规划层面，本文的对比基线包括零样本 LLM 规划器与仅基于人类演示微调的规划器。

- **PP（PARTNR-Pretrained）**（Chang et al., ICLR 2025）采用 Llama3.3-70B-Instruct 作为零样本规划器，使用 ReAct 框架在环境中执行动作。它依赖 EPM 提供的文本化环境表示进行推理，但未经任何微调。在 groundtruth 感知下，PP 的成功率为 0.51。
- **HD（Human Demonstrations）** 是本文提出的训练变体之一，使用 Llama3.1-8B-Instruct 在人类演示轨迹上进行监督微调。尽管模型规模远小于 PP（8B vs 70B），HD 在 groundtruth 感知下的成功率反超 PP 0.12（0.63 vs 0.51），证明了人类演示训练的有效性。
- **DDAFT（Dynamic Difficulty-Aware Fine-Tuning）** 是本文的核心 RL 训练方法。它是一种无价值函数的在线 RL 方法，通过动态调整采样难度（将采样空间向困难指令倾斜）来提高样本效率。在 groundtruth 感知下，DDAFT 将 PP 的成功率提升 0.15（至 0.66），将 HD 的成功率提升 0.05（至 0.68）。在 learned perception 设置下，PP+DDAFT 与 HD+DDAFT 均达到 0.58 成功率，证明 DDAFT 能够有效弥合感知噪声带来的性能损失。

### 适用边界

1. **环境规模与动态性**：EPM 在 PARTNR 基准的大规模室内场景中验证有效，且原生支持物体移动、增减等动态变化。但其训练数据完全来自仿真环境，在真实世界动态场景中进行完整规划任务训练尚未实现。
2. **感知模态**：EPM 目前仅输出文本化的对象表示（3D 坐标 + 自然语言描述），适合与 LLM 规划器无缝集成。但对于需要视觉推理的对象属性（如液体状态、材质纹理、精细几何形状），纯文本表示存在信息遗漏风险。
3. **动作执行**：当前系统的低层控制依赖特权技能策略（privileged skills），即假设导航、拾取、放置等技能已完美实现。实际部署时需替换为基于学习或视觉运动控制的技能模块。
4. **上下文长度**：随着场景规模增大，文本化记忆的 token 数量线性增长，可能引发长上下文问题，影响 LLM 规划器的推理效率与成本。

### 局限与开放问题

**已明确的局限**：
- 在真实世界测试中，EPM 的物体分类和重关联仍然存在错误（Figure 4 右侧显示真实场景中的分类错误），感知性能尚未饱和。
- 在 Spot-Indoor 真实数据集上，EPM 的 Node F1 仅为 0.24，低于 DynaMem 的 0.51（Table 2），表明在真实世界感知任务上的泛化能力仍有显著提升空间。
- 边缘 F1（捕捉对象间关系）在 PARTNR 上为 0.46，在 Spot-Indoor 上仅为 0.16，对象间关系建模是当前明显的短板。

**开放问题**：
- 如何将连续视觉特征融入 EPM，以捕捉文本难以描述的物体属性（如材质、精确形状、液体状态）？
- 能否将 EPM 与视觉-语言-动作（VLA）模块结合，实现从高层规划到低层控制的端到端学习，消除对特权技能的依赖？
- 在更长序列、更大规模的日常任务中，EPM 的记忆更新机制能否保持鲁棒？是否需要引入记忆压缩或选择性遗忘机制？
- 如何进一步提升边缘 F1，以改善对象间关系建模，从而提升规划质量？



## 原文 PDF

![[paperPDFs/ICLR_2026/Planning_with_an_Embodied_Learnable_Memory.pdf]]
