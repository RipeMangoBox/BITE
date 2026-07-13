---
title: "MCP Security Bench (MSB): Benchmarking Attacks Against Model Context Protocol in LLM Agents"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/MCP_Security_Bench_MSB_Benchmarking_Attacks_Against_Model_Context_Protocol_in_LLM_Agents.pdf
project_link: null
code_link: https://github.com/dongsenzhang/MSB
openreview_forum_id: irxxkFMrry
aliases:
- MMSB
- MSBMBAAMCPLA
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/planning_control
core_operator: "通过构建覆盖MCP工作流三个阶段的12种攻击分类体系，并基于真实MCP服务器执行攻击而非模拟，系统性地暴露全流程脆弱性；同时引入净弹性性能（NRP）度量在安全与性能之间取得平衡。"
primary_logic: "MCP特有的攻击（如用户模拟UI、虚假错误FE）比传统函数调用攻击（如提示注入PI）更具侵略性；能力越强的模型反而越脆弱；NRP指标揭示安全与性能的反向关系，提升模型易用性可能同时增加安全风险。"
claims:
- "所有攻击方法的平均ASR为40.35%，其中越界参数攻击OP效果最强（平均ASR 76.5%），名称碰撞-虚假错误NC-FE效果最弱（14.62%）。"
- "MCP新增攻击UI和FE的平均ASR（45.69%和39.21%）显著高于传统函数调用攻击PI和RI（20.21%和20%）。"
- "混合攻击展现协同增强效应：PI-UI平均ASR（56.07%）高于单一攻击PI（20.21%）和UI（45.69%）。"
- "强模型性能与安全性之间存在反向关系：启用思维链模式的Qwen3 8B，PUA从51.15%升至64.97%，但ASR也从47.23%升至57.08%。"
---

# MCP Security Bench (MSB): Benchmarking Attacks Against Model Context Protocol in LLM Agents

> [!tip] 核心洞察
> MCP特有的攻击（如用户模拟UI、虚假错误FE）比传统函数调用攻击（如提示注入PI）更具侵略性；能力越强的模型反而越脆弱；NRP指标揭示安全与性能的反向关系，提升模型易用性可能同时增加安全风险。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | MCP安全基准（MSB）：针对LLM智能体中模型上下文协议的攻击基准测试 |
| 英文题名 | MCP Security Bench (MSB): Benchmarking Attacks Against Model Context Protocol in LLM Agents |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=irxxkFMrry) · [GitHub](https://github.com/dongsenzhang/MSB) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/planning_control |
| Method | MSB (MCP Security Bench) |
| Dataset | MSB全攻击类型（12种）, 防御实验（MCIP）, Qwen3 8B 思维链模式影响 |

> [!tip] 效果简介
> - MSB全攻击类型（12种） 上，平均ASR 为 40.35%，对比 N/A（无防御基准为攻击原始成功率），变化 N/A。
> - 防御实验（MCIP） 上，平均ASR 为 28.69%，对比 40.35%，变化 -11.66%。
> - 防御实验（MCIP） 上，平均NRP 为 34.88%，对比 33.70%，变化 +1.18%。

## 概要

随着大语言模型（LLM）智能体在工具调用场景中的广泛部署，**模型上下文协议（MCP）** 作为标准化的工具交互接口，在提升互操作性的同时，也显著扩展了攻击面。现有安全基准（如 **ASB**、**AgentDojo**、**InjecAgent**）局限于传统的函数调用范式，仅覆盖部分攻击阶段，且多依赖仿真环境，无法真实反映 MCP 生态下全流水线的安全风险。**MSB（MCP Security Bench）** 针对这一瓶颈，构建了覆盖任务规划、工具调用、响应处理三个阶段的 **12 种攻击分类体系**，并在真实 MCP 服务器上执行攻击，系统性地暴露了 MCP 特有的脆弱性。

核心发现表明：MCP 特有的攻击类型（如用户模拟 UI、虚假错误 FE）比传统函数调用攻击（如提示注入 PI、检索注入 RI）更具侵略性；能力越强的模型往往越脆弱；新引入的 **净弹性性能（NRP）** 指标揭示了安全性与性能之间的反向关系——提升模型易用性可能同时增加安全风险。

在方法定位上，MSB 相较于现有基准实现了四个关键槽位的改变：将工具调用协议从函数调用升级为 **MCP 真实协议调用**；将攻击覆盖从单阶段扩展为 **全流程 12 种攻击**；将评估环境从仿真输出转为 **实际工具执行与工作区状态检查**；将安全性衡量从 ASR/PUA 扩展为包含 **NRP** 的三维指标体系。

实验覆盖 10 种主流 LLM 骨干，基于 2,000 个攻击实例的评估显示：所有攻击方法的平均 ASR 达 **40.35%**，其中越界参数攻击（OP）效果最强（平均 ASR **76.5%**），名称碰撞-虚假错误（NC-FE）最弱（14.62%）。混合攻击展现出协同增强效应（PI-UI 平均 ASR 56.07%，高于单一攻击）。防御方案 MCIP 可将平均 ASR 降至 28.69%，但 NRP 仅微增 1.18%，且伴随 PUA 下降 7.59%，表明现有防御在安全-性能平衡上仍有显著不足。

### 模型上下文协议（MCP）与新兴攻击面

大语言模型（LLM）驱动的智能体正在快速进入生产环境，其核心能力之一是调用外部工具完成复杂任务。模型上下文协议（Model Context Protocol, MCP）作为一种标准化的工具调用协议，通过统一的接口规范连接LLM与外部工具服务器，显著降低了集成成本并推动了智能体应用的规模化部署。然而，MCP在提升互操作性的同时，也系统性地扩展了攻击面：攻击者可以在**任务规划**、**工具调用**和**响应处理**三个关键阶段注入恶意载荷，而传统安全评估无法覆盖这一完整流水线。

具体而言，MCP工作流的脆弱性体现在四个攻击向量上：**工具签名攻击**（篡改工具名称与描述以诱导错误选择）、**工具参数攻击**（通过越界参数实现信息泄露）、**工具响应攻击**（在工具返回结果中嵌入恶意指令），以及**检索注入攻击**（污染外部知识库以传播恶意内容）。这些攻击向量贯穿智能体与工具交互的全过程，构成了MCP特有的安全威胁。

### 现有基准的缺口

当前LLM智能体安全评估主要依赖以下基准，但它们均存在关键局限：

- **ASB**（Zhang et al., 2025a）和**AgentDojo**（Debenedetti et al., 2025）基于传统的**函数调用（Function Calling）范式**，仅覆盖部分攻击类型，且采用仿真环境而非真实工具执行，无法复现MCP协议下的实际攻击行为。
- **InjecAgent**（Zhan et al., 2024）专注于**提示注入**单一攻击类型，缺乏对全流水线攻击的系统覆盖。
- **MCPTox**（Wang et al., 2025a）虽在MCP环境下评估工具描述注入攻击，但攻击类型较少，尚未建立完整的威胁分类体系。

这些基准的共同缺陷在于：**未能覆盖MCP特有的攻击类型**（如用户模拟UI、虚假错误FE），**缺乏真实工具执行环境**，且**评估指标单一**——仅使用攻击成功率（ASR）和攻击下性能（PUA），无法综合衡量智能体在安全与性能之间的权衡关系。

### 本文动机与核心思路

针对上述缺口，本文提出**MCP安全基准（MCP Security Bench, MSB）**，旨在系统性地评估LLM智能体在MCP环境下的安全性。MSB的核心设计思路包括三个层面：

1. **全流水线攻击分类**：建立覆盖MCP三个工作流阶段的12种攻击分类体系，包含MCP特有的用户模拟（UI）、虚假错误（FE）等攻击类型，以及多阶段协同的混合攻击。

2. **真实执行环境**：基于Smithery.ai平台收集304个经过功能验证的良性工具，通过定向变异生成405个攻击工具，在真实MCP服务器上执行攻击并检查工作区状态，而非依赖仿真输出。

3. **韧性度量指标**：引入**净弹性性能（Net Resilient Performance, NRP）**，定义为 $\mathrm{NRP} = \mathrm{PUA} \cdot (1 - \mathrm{ASR})$，综合衡量智能体在抵抗攻击的同时维持任务完成能力的整体韧性，弥补了ASR和PUA单独使用的不足。

通过MSB，本文旨在回答一个核心问题：**在标准化的MCP协议下，当前主流LLM智能体究竟有多脆弱，以及安全性与性能之间存在怎样的根本性权衡？**

## 核心方法与创新机理

MSB的核心创新在于将LLM智能体安全评估从传统的函数调用范式迁移至**MCP真实协议栈**，并围绕MCP全流水线暴露的攻击面构建了系统性的攻击分类、执行与度量体系。其关键创新点体现在以下四个维度。

### 1. 从函数调用模拟到MCP真实协议执行

现有工具安全基准（如**ASB** (Zhang et al., 2025a)、**AgentDojo** (Debenedetti et al., 2025)）普遍依赖函数调用范式下的仿真工具选择或模拟输出，无法覆盖MCP协议引入的完整交互链路。MSB将评估环境切换为**真实MCP服务器上的工具执行**：攻击工具在真实服务器上运行，评估引擎通过检查工作区状态和工具调用日志来判定攻击成功与否，而非依赖模拟输出（Sec. 5.1, Tab. 10）。这一改变使得攻击效果能够反映MCP协议特有的交互脆弱性，而非函数调用范式下的简化假设。

### 2. 全流水线攻击分类体系

现有基准的攻击覆盖范围有限：**InjecAgent** (Zhan et al., 2024) 仅关注提示注入，**MCPTox** (Wang et al., 2025a) 仅覆盖MCP环境下的工具描述注入。MSB建立了覆盖**任务规划、工具调用、响应处理**三个关键阶段的12种攻击分类体系（Tab. 1），包括：
- **工具签名攻击**（名称碰撞NC、推广性描述PM、工具劫持TT）
- **工具参数攻击**（越界参数OP）
- **工具响应攻击**（用户模拟UI、虚假错误FE）
- **检索注入攻击**（RI）
- **提示注入攻击**（PI）
- **混合攻击**（PI-UI、PI-FE、NC-FE、PM-FE、PM-UI、PM-OP）

这一分类体系首次系统性地覆盖了MCP工作流中所有可被利用的攻击向量（工具名称、描述、参数、响应及外部检索数据）。

### 3. 净弹性性能（NRP）度量

传统安全评估仅使用攻击成功率（ASR）和攻击下性能（PUA）两个独立指标，无法综合衡量智能体在安全与性能之间的权衡。MSB引入**净弹性性能（NRP）**：

$$\mathrm{NRP} = \mathrm{PUA} \cdot (1 - \mathrm{ASR})$$

NRP在对抗环境中同时衡量智能体维持性能与抵抗攻击的整体能力（Eq. 10, Sec. 5.2）。实验表明，NRP能揭示ASR和PUA无法单独反映的关键关系：例如，启用思维链模式使Qwen3 8B的PUA从51.15%升至64.97%，但ASR也从47.23%升至57.08%，NRP仅微增0.87%（Tab. 13, Sec. E.4）。这说明**提升模型易用性可能同时增加安全风险**，而NRP正是捕捉这一反向关系的核心指标。

### 4. 混合攻击的协同效应验证

MSB首次系统性地评估了跨阶段混合攻击的协同增强效应。实验显示，将诱导恶意工具调用的攻击（NC、PM、TT）与造成实际损害的攻击（FE、UI、OP）组合后，ASR显著高于单一攻击：PI-UI的平均ASR达56.07%，远超PI的20.21%和UI的45.69%（Tab. 3, Sec. 6.2）。这一发现揭示了MCP多阶段攻击面的叠加脆弱性——攻击者可通过组合不同阶段的攻击向量，显著提高绕过模型安全层的概率（Sec. E.3）。

**总结**：MSB的创新本质在于将安全评估从“函数调用范式下的攻击模拟”升级为“MCP真实协议栈下的全流水线攻击执行与弹性度量”，从而暴露了传统基准无法覆盖的MCP特有脆弱性。

![[assets/figures/papers/paper_list_l31_https_openreview_net_forum_id_irxxkFMrry/figures/001_Figure_1.jpg]]
*Figure 1: Overview of the MCP-specific attacking framework, including Tool Signature Attack, Tool Parameters Attack, Tool Response Attack, and Retrieval Injection Attack, which cover the full tool-use pipeline stages: task planning, tool calling and response handling*

![[assets/figures/papers/paper_list_l31_https_openreview_net_forum_id_irxxkFMrry/figures/002_Table_1.jpg]]
*Table 1: Attack types in MSB. s denotes the suffix, p denotes the promotional statement, u denotes the imitated user query, e denotes the fabricated error message, g denotes the guiding message, d denotes the external data. Other notations are the same as those in Sec. 4*

![[assets/figures/papers/paper_list_l31_https_openreview_net_forum_id_irxxkFMrry/figures/003_Table_2.jpg]]
*Table 2: Overview of the statistics of MCP Security Bench (MSB)*

MSB（MCP Security Bench）是一个面向MCP协议下LLM智能体工具调用安全性的动态评估基准。其设计核心在于覆盖MCP工作流的三个关键阶段——任务规划、工具调用与响应处理，并基于真实MCP服务器执行攻击，而非依赖仿真输出。

### 攻击面与分类体系

MCP工作流中，LLM智能体通过工具签名（名称与描述）、参数和响应与工具交互，这三者均构成攻击向量（Figure 1）。MSB据此建立了12种攻击类型的分类体系（Table 1），覆盖三个阶段及多阶段混合攻击：

- **任务规划阶段**：攻击者利用工具签名注入恶意工具，包括名称碰撞（NC）、前缀匹配（PM）、工具劫持（TT）。
- **工具调用阶段**：攻击者利用工具参数实施越界参数攻击（OP）。
- **响应处理阶段**：攻击者利用工具响应实施用户模拟（UI）和虚假错误（FE）。
- **检索注入**（RI）：攻击者通过污染外部数据库注入恶意指令。
- **混合攻击**：将诱导恶意工具调用的攻击（NC、PM、TT）与造成具体损害的攻击（FE、UI、OP）组合，形成NC-FE、PM-FE、PM-UI、PM-OP、TT-OP五类混合攻击。

### 基准构建流水线

MSB的构建包含五个核心模块：

1. **良性工具收集与任务设计**：从MCP集成平台Smithery.ai收集高频工具，经功能验证与去重后保留304个行为一致的良性工具，并构造65个覆盖10个场景的用户任务（Table 2, Table 7）。

2. **攻击工具生成**：对良性工具的名称、描述、参数、响应进行定向变异，生成405个攻击工具。每种攻击类型采用特定的修改策略（例如，FE工具将原始响应替换为错误消息并嵌入恶意指令）。

3. **攻击任务与实例构建**：设计6种攻击任务，与攻击工具组合形成2000个测试实例，覆盖全流水线攻击（Figure 5展示了各攻击类型的实例分布）。

4. **动态评估引擎**：在真实MCP环境下执行攻击，通过检查工作区状态和工具调用日志来判定攻击成功与否及用户任务完成情况，而非依赖模拟的工具选择或输出。

5. **鲁棒性度量计算**：基于攻击实例结果计算三个指标：

   - **攻击成功率（ASR）**：
     $$\mathrm{ASR} = \frac{\mathrm{Number\ of\ successful\ attack\ instances}}{\mathrm{Number\ of\ total\ attack\ instances}}$$
     衡量攻击目标被实现的实例比例。

   - **攻击下性能（PUA）**：
     $$\mathrm{PUA} = \frac{\mathrm{Number\ of\ completed\ user\ tasks\ under\ attack}}{\mathrm{Number\ of\ total\ user\ tasks}}$$
     衡量对抗环境下用户任务完成的比例。

   - **净弹性性能（NRP）**：
     $$\mathrm{NRP} = \mathrm{PUA} \cdot (1 - \mathrm{ASR})$$
     综合衡量智能体在抵抗攻击的同时维持性能的整体能力，数值越高表示越具韧性。

### 与现有基准的关键差异

相较于现有基准（如**ASB**（Zhang et al., 2025a）、**AgentDojo**（Debenedetti et al., 2025）、**InjecAgent**（Zhan et al., 2024）、**MCPTox**（Wang et al., 2025a）），MSB在以下维度实现了根本性转变：

| 维度 | 现有基准 | MSB |
|------|---------|-----|
| 工具调用协议 | 函数调用（Function Calling） | MCP真实协议调用，工具在真实服务器上执行 |
| 攻击覆盖阶段 | 仅覆盖响应处理或部分阶段 | 覆盖任务规划、工具调用、响应处理全流程 |
| 评估环境 | 仿真输出或函数调用模拟 | 实际运行工具并检查工作区状态 |
| 安全性衡量指标 | 仅ASR与PUA | 新增NRP，在对抗环境中综合衡量性能与安全性 |

这些差异使得MSB能够暴露MCP特有的全流水线脆弱性——尤其是工具调用阶段（该阶段平均ASR超过70%，见Figure 3）和MCP新增的攻击类型（UI和FE），这些在传统函数调用范式的基准中无法被覆盖。

### 攻击形式化框架

MSB将MCP工具调用工作流抽象为三个关键阶段——任务规划、工具调用、响应处理——并针对每个阶段定义攻击面。智能体的基础目标函数为：

$$\mathbb{E}_{q \sim \pi_q} \left[ \mathbb{1} \left( \mathrm{Agent}( \mathrm{LLM}( p_{sys} \oplus \mathcal{T}, q, \mathcal{O} ), \mathcal{T}, \mathcal{D} ) = a \right) \right]$$

其中 $p_{sys}$ 为系统提示，$\mathcal{T}$ 为工具列表，$q$ 为用户查询，$\mathcal{O}$ 为观察序列，$\mathcal{D}$ 为外部知识库，$a$ 为正确动作。攻击者的目标则是最大化智能体执行恶意动作 $a_m$ 的期望概率：

$$\mathbb{E}_{q \sim \pi_q} \left[ \mathbb{1} \left( \mathrm{Agent}( q, \theta_m ) = a_m \right) \right]$$

其中 $\theta_m$ 表示攻击者对MCP工作流各组件的对抗性修改。攻击者的能力包括：修改恶意工具的全部组件、部署多个协同恶意工具、向系统提示注入指令、以及向外部资源注入恶意内容。

### 12种攻击类型分类

MSB基于攻击向量（工具签名、参数、响应、检索注入）与交互阶段，构建了12种攻击的分类体系（Table 1），覆盖全流水线：

**任务规划阶段——工具签名攻击：** 攻击者利用工具名称 $\tau_n^m$ 或描述 $\tau_d^m$ 作为攻击向量，诱导智能体调用恶意工具。其目标函数为：

$$\mathbb{E}_{q \sim \pi_q} \left[ \mathbb{1} \left( \mathrm{Agent}( \mathrm{LLM}( p_{sys} \oplus T \oplus T^m, q, \mathcal{O} ), \mathcal{T} + T^m ) = a_m \right) \right]$$

具体包括三种攻击：**名称碰撞（NC）** 将恶意工具名设置为与目标工具名相似；**前缀匹配（PM）** 利用前缀相似性诱导误选；**类型伪装（TT）** 通过描述伪装工具功能类别。

**工具调用阶段——工具参数攻击：** 攻击者利用工具参数 $\tau_p^m$ 作为攻击面，诱导智能体提供越界输入，导致信息泄露。其目标函数为：

$$\mathbb{E}_{q \sim \pi_q} \left[ \mathbb{1} \left( \mathrm{Agent}( \mathrm{LLM}( p_{sys} \oplus \mathcal{T}^m, q, \mathcal{O} ), \mathcal{T}^m ) = a_m( \tau^m( \tau_p^m = i^m ) ) \right) \right]$$

其中 **越界参数攻击（OP）** 是最具代表性的实现，恶意工具声明一个看似合法但实际用于窃取信息的参数 $i^m$。

**响应处理阶段——工具响应攻击：** 攻击者利用工具响应 $\tau_r^m$ 作为攻击面，在响应中嵌入恶意指令 $x^m$，误导智能体执行非预期操作。其目标函数为：

$$\mathbb{E}_{q \sim \pi_q} \left[ \mathbb{1} \left( \mathrm{Agent}( \mathrm{LLM}( p_{sys} \oplus T^m, q, \mathcal{O} + \tau_r^m ), T^m ) = a_m [ x^m ] \right) \right]$$

具体包括：**用户模拟（UI）** 在响应中冒充用户身份嵌入恶意指令；**虚假错误（FE）** 提供伪造的工具执行错误消息，要求智能体按恶意指令操作才能“成功”调用工具。

**检索注入攻击（RI）：** 攻击者污染外部知识库 $\mathcal{D}_p$，使检索结果中包含恶意指令。其目标函数为：

$$\mathbb{E}_{q \sim \pi_q} \left[ \mathbb{1} \left( \mathrm{Agent}( \mathrm{LLM}( p_{sys} \oplus \mathcal{T}, q, \mathcal{O} + \tau_r ), \mathcal{T}, \mathcal{D}_p ) = a_m [ x^m ] \right) \right]$$

**混合攻击：** 将诱导恶意工具调用的攻击（NC、PM、TT）与造成实际损害的攻击（FE、UI、OP）组合，形成多阶段协同攻击，如NC-FE、PM-FE、PM-UI、PM-OP、TT-OP。

### 评估指标推导

MSB引入三个核心指标，从攻击有效性、操作稳定性和整体韧性三个维度进行评估：

**攻击成功率（ASR）：** 衡量攻击目标的实现程度。

$$\mathrm{ASR} = \frac{\mathrm{Number~of~successful~attack~instances}}{\mathrm{Number~of~total~attack~instances}}$$

通过检查工作区环境状态和工具调用日志判定攻击是否成功，而非依赖模拟输出。

**攻击下性能（PUA）：** 衡量对抗环境中智能体完成用户任务的能力。

$$\mathrm{PUA} = \frac{\mathrm{Number~of~completed~user~tasks~under~attack}}{\mathrm{Number~of~total~user~tasks}}$$

需注意：UI和FE攻击中的恶意工具不提供正常功能，因此其PUA指标无评估意义。

**净弹性性能（NRP）：** MSB新提出的综合性指标，在对抗环境中同时衡量性能维持与攻击抵抗能力。

$$\mathrm{NRP} = \mathrm{PUA} \cdot (1 - \mathrm{ASR})$$

NRP基于对抗环境中的PUA计算（而非良性环境性能），因为模型在对抗与良性环境下的行为差异显著且无法简单外推。该指标直接揭示了安全性与性能之间的反向关系——提升模型易用性可能同时增加安全风险。

## 实验与关键发现

### 核心发现：MCP全流水线攻击的有效性与脆弱性分布

MSB在10个主流LLM智能体上对12种攻击类型进行了系统评估。**所有攻击方法的平均ASR达40.35%**，验证了MCP范式下工具调用全流程存在真实且广泛的安全脆弱性。攻击效果呈现显著分化：

- **越界参数攻击（OP）是最具威胁的单一攻击向量**，平均ASR高达76.5%（Tab. 3）。其攻击意图不包含显式恶意指令，而是通过诱导模型提供越界参数实现信息泄露，构成一种**语义欺骗**——模型的上下文难以识别此类攻击的恶意本质。
- **名称碰撞-虚假错误（NC-FE）效果最弱**，平均ASR仅14.62%，表明单纯依赖工具名称混淆配合虚假错误响应的攻击链在多数模型上难以奏效。

![[assets/figures/papers/paper_list_l31_https_openreview_net_forum_id_irxxkFMrry/figures/004_Table_3.jpg]]
*Table 3: Attack Success Rates (ASR ↓) for the LLM agents with different LLM backbones*

![[assets/figures/papers/paper_list_l31_https_openreview_net_forum_id_irxxkFMrry/figures/010_Table_4.jpg]]
*Table 4: Defense (Jing et al., 2025) results. The result is the average of 12 attack types in Tab. 3. Baseline denotes the performance without defense. ∆ denotes change compared to Baseline*

**MCP引入的新型攻击面展现出比传统攻击更强的侵略性**。用户模拟（UI）和虚假错误（FE）的平均ASR分别为45.69%和39.21%，显著高于传统函数调用范式下的提示注入（PI, 20.21%）和检索注入（RI, 20%）。这一差距揭示了MCP标准化工具交互在扩展功能的同时，也实质性扩大了攻击面——攻击者可以利用工具响应通道伪造用户指令或系统错误，而模型对此类通道的信任度明显高于对用户输入的警惕。

### 混合攻击的协同增强效应

混合攻击的实验结果揭示了多阶段协同的显著威胁放大效应。**PI-UI的平均ASR达56.07%，远超单一PI（20.21%）和单一UI（45.69%）**（Tab. 3）。类似地，PI-FE同样展现出高于各自单独攻击的ASR。

这种协同增强的机制在于：**多阶段入侵增加了绕过模型安全层的概率**。当提示注入诱导模型调用恶意工具后，工具响应中的用户模拟或虚假错误进一步引导模型执行有害操作，形成攻击链的级联放大。这表明，仅防御单一攻击阶段不足以保障MCP系统的整体安全性。

### 能力与安全性的反向关系

实验揭示了模型能力与安全性之间的深层矛盾。以Qwen3 8B的思维链模式消融为例（Tab. 13）：

| 模式 | PUA | ASR | NRP |
|------|-----|-----|-----|
| 关闭思维链 | 51.15% | 47.23% | 26.95% |
| 开启思维链 | 64.97% | 57.08% | 27.82% |
| **变化（∆）** | **+13.82%** | **+9.85%** | **+0.87%** |

开启思维链模式后，模型的工具使用能力显著提升（PUA增加13.82%），但攻击成功率同步攀升（ASR增加9.85%），**净弹性性能NRP仅微增0.87%**。这意味着更强的推理能力在提升任务完成率的同时，也使模型更容易被攻击者操纵——模型对指令的更好遵循反而成为攻击者可利用的弱点。

Figure 2的散点图进一步可视化这一反向关系：PUA与ASR呈正相关趋势，而NRP作为两者的综合度量，在不同模型间差异显著，揭示了**安全性与性能的权衡是MCP智能体设计的核心挑战**。

![[assets/figures/papers/paper_list_l31_https_openreview_net_forum_id_irxxkFMrry/figures/007_Figure_2.jpg]]
*Figure 2: Visual comparisons between PUA vs ASR, NRP vs ASR and NRP vs PUA*

### 分阶段脆弱性分析

Figure 3展示了不同MCP工作流阶段的ASR对比。**工具调用阶段（Invocation）是安全最薄弱的环节**，平均ASR超过70%。该阶段对应越界参数攻击（OP），攻击者通过操控工具参数定义即可实现高成功率的信息窃取，无需复杂的社会工程或响应伪造。

相比之下，任务规划阶段（Planning）和响应处理阶段（Response）的ASR相对较低，但混合攻击可以跨越阶段边界形成攻击链，从而突破单阶段防御。

### 防御评估：MCIP的局限

采用基于检测的防御方案MCIP（Jing et al., 2025）后（Tab. 4）：

- **平均ASR从40.35%降至28.69%**（降幅11.66%），证明基于对话风险分类的检测方法对部分攻击类型有效。
- 然而，**PUA同步下降7.59%**，表明防御机制存在过度拦截问题——正常工具调用也被误判为攻击行为。
- **NRP仅从33.70%微升至34.88%**（增幅1.18%），说明当前防御方案在安全增益与性能损失之间尚未取得有意义的净收益。

这一结果暴露了静态检测方案的固有局限：**缺乏上下文感知能力的防御难以区分恶意工具调用与合法但复杂的工具使用模式**，导致拒绝服务式的性能退化。

### 指标有效性的边界说明

需注意PUA指标在部分攻击类型上的适用性限制。UI和FE攻击中的恶意工具不提供正常功能，其工具响应始终返回恶意指令，因此**PUA指标对UI、FE及包含它们的混合攻击（PI-UI、PI-FE）无评估意义**——模型无法通过这些工具完成用户任务，PUA值反映的是攻击设计而非模型能力。NRP的计算同样受此影响，在解读上述攻击类型的NRP时需考虑这一约束。

### 失败模式与攻击无效场景

NC-FE的低ASR（14.62%）揭示了攻击链断裂的典型失败模式：当名称碰撞未能成功诱导模型选择恶意工具时，后续的虚假错误响应无从触发，整条攻击链失效。这表明**工具选择阶段的攻击成功率是混合攻击有效性的瓶颈**——若初始诱导失败，后续攻击向量完全无法发挥作用。

此外，部分模型对特定攻击类型展现出较强鲁棒性。例如，Claude 4 Sonnet在多种攻击下的ASR低于平均水平，但其PUA也相对较低，再次印证了安全性与性能的权衡关系。

## 定位与知识库关联

### 1. 与现有基准的关系

MSB的定位是对现有LLM智能体安全基准的**协议级扩展**，其核心差异在于从函数调用范式迁移至MCP真实协议环境。

**函数调用范式的基准**构成了MSB的前置工作。**ASB**（Zhang et al., 2025a）和**AgentDojo**（Debenedetti et al., 2025）均基于函数调用范式评估工具使用安全性，但两者仅覆盖部分攻击类型，且依赖仿真工具输出而非真实执行。**InjecAgent**（Zhan et al., 2024）则专注于提示注入（PI）这一单一攻击维度。MSB将这些工作统一纳入其攻击分类体系中的PI和RI类别，但将评估范围从响应处理阶段扩展至任务规划、工具调用、响应处理的**全流水线**。

**MCP原生基准**方面，**MCPTox**（Wang et al., 2025a）是MSB最直接的前置工作，在MCP环境下评估工具描述注入攻击。然而，MCPTox的攻击类型较为有限，未覆盖工具参数、响应注入及混合攻击。MSB在此基础上将攻击类型扩展至12种，并引入真实MCP服务器执行环境。

MSB的方法论贡献体现在三个**关键设计变更**：

- **工具调用协议**：从函数调用模拟迁移至MCP真实协议调用，工具在真实服务器上执行（Sec. 5.1, Tab. 10）。
- **攻击覆盖阶段**：从仅覆盖响应处理扩展至任务规划、工具调用、响应处理全流程（Tab. 1, Sec. 4）。
- **评估环境**：从仿真输出改为实际运行良性/恶意工具并检查工作区状态（Sec. 5.1）。
- **安全性度量**：在ASR和PUA之外新增NRP指标，在对抗环境中综合衡量性能与安全性（Sec. 5.2）。

### 2. 适用边界

MSB的适用性受以下边界条件约束：

**协议依赖性**：MSB专为MCP协议设计，其攻击分类学中的工具签名攻击（NC、PM、TT）、工具参数攻击（OP）和工具响应攻击（UI、FE）均依赖于MCP的工具描述、参数规范和响应格式。对于非MCP的工具调用范式（如原生函数调用），这些攻击的迁移性尚未验证。

**攻击类型覆盖**：MSB定义了12种人工设计的攻击类型，覆盖了MCP工作流的三个关键阶段，但未包含零日漏洞、供应链攻击或服务器端漏洞利用。攻击工具的生成基于对良性工具的名称、描述、参数和响应的定向变异（Sec. 5.1, Appendix D.2），这意味着攻击模式受限于预定义的变异策略。

**模型覆盖**：评估覆盖10种LLM骨干（DeepSeek-V3.1、GPT-4o-mini、GPT-5、Claude 4 Sonnet、Gemini 2.5 Flash、Qwen3 8B/30B、Llama3.1 8B/70B、Llama3.3 70B），但可能无法完全代表所有MCP系统的安全性特征。

**防御评估的局限性**：防御实验仅测试了**MCIP**（Jing et al., 2025）这一基于检测的方法——训练Llama-xLAM-2-8B分类器识别工具交互中的安全风险（Sec. 6.3）。该方法将平均ASR从40.35%降至28.69%，但NRP仅从33.70%微升至34.88%，且PUA下降7.59%（Tab. 4），表明简单的检测式防御在安全与性能的权衡上效果有限。

### 3. 关键局限

**NRP指标的公平性约束**：NRP基于对抗环境中的PUA计算，忽略了模型在无攻击时的基线性能差异。此外，PUA指标对UI、FE及混合攻击PI-UI、PI-FE无意义，因为这些攻击工具不提供正常功能，无法通过其完成用户任务（Tab. 11, 12注释）。

**攻击生成的静态性**：攻击工具通过预定义变异策略生成，未探索自动化攻击向量生成。随着MCP生态演进，新的攻击面可能出现，而MSB缺乏持续更新攻击类型的机制。

**防御探索的不充分性**：仅评估了基于检测的简单防御方案，未探索上下文感知的参数白名单、动态沙箱或基于行为异常的检测等更先进的防御策略。

### 4. 开放问题

MSB揭示的瓶颈指向以下开放方向：

1. **动态防御设计**：如何设计上下文感知的参数校验机制，以减少误拒并提升NRP？当前MCIP防御导致PUA下降7.59%，表明简单拒绝策略的代价过高。

2. **攻击普适性验证**：MSB中发现的攻击模式（尤其是MCP特有的UI和FE攻击，平均ASR分别达45.69%和39.21%）在其他MCP应用领域（如多智能体协作、代码执行沙箱）中的普适性如何？

3. **自动化攻击生成**：能否利用LLM自动生成新的MCP攻击向量，使基准能够持续更新以覆盖新兴威胁？

4. **安全-性能权衡的深层机制**：实验揭示了一个矛盾现象——启用思维链模式使Qwen3 8B的PUA从51.15%升至64.97%，但ASR也从47.23%升至57.08%，NRP仅微增0.87%（Tab. 13, Sec. E.4）。这表明更强的指令遵循能力可能同时放大攻击面。如何在模型层面解耦这一反向关系，是MCP安全研究的核心挑战。

## 原文 PDF

![[paperPDFs/ICLR_2026/MCP_Security_Bench_MSB_Benchmarking_Attacks_Against_Model_Context_Protocol_in_LLM_Agents.pdf]]
