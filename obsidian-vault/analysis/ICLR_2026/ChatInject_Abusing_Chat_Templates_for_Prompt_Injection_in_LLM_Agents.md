---
title: "ChatInject: Abusing Chat Templates for Prompt Injection in LLM Agents"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/ChatInject_Abusing_Chat_Templates_for_Prompt_Injection_in_LLM_Agents.pdf
openreview_forum_id: WVhgFSKniL
aliases:
- ChatInject
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/planning_control
core_operator: "是否将注入内容格式化为目标模型的原生聊天模板。"
primary_logic: "通过滥用聊天模板，攻击者能将恶意指令伪装为高优先级角色，并可嵌入模拟多轮对话来实施一次性说服攻击。"
claims:
- "ChatInject通过使用伪造角色标签格式化的恶意载荷，始终能提高攻击成功率。"
- "攻击者可以在低优先级的工具输出中伪造角色标签，从而绕过基于角色的安全层级。"
- "注入模板与目标模型模板的相似性越高，跨模型攻击成功率越高。"
- "AgentDojo 上 平均 ASR（6个开源模型） = 32.05% (ChatInject)"
---

# ChatInject: Abusing Chat Templates for Prompt Injection in LLM Agents

> [!tip] 核心洞察
> 通过滥用聊天模板，攻击者能将恶意指令伪装为高优先级角色，并可嵌入模拟多轮对话来实施一次性说服攻击。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | ChatInject：利用聊天模板进行LLM代理中的提示注入攻击 |
| 英文题名 | ChatInject: Abusing Chat Templates for Prompt Injection in LLM Agents |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=WVhgFSKniL); [Project](https://hwanchang00.github.io/chatinject_project_page) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/planning_control |
| Method | ChatInject |
| Dataset | AgentDojo, InjecAgent |

> [!tip] 效果简介
> - AgentDojo 上，平均 ASR（6个开源模型） 为 32.05% (ChatInject)，对比 5.18% (Default InjecPrompt)，变化 +26.87 pp。
> - InjecAgent 上，平均 ASR（6个开源模型） 为 45.90% (ChatInject)，对比 15.13% (Default InjecPrompt)，变化 +30.77 pp。
> - InjecAgent 上，ASR on Qwen-3 为 39.4% (InjecPrompt + ChatInject)，对比 8.5% (Default InjecPrompt)，变化 +30.9 pp。

## 概述

### 问题背景

LLM代理在调用外部工具时，会将不可信的工具返回内容拼接至模型上下文，形成**间接提示注入**的天然攻击面。主流防御策略依赖于聊天模板中特殊令牌（如 `<system>`、`<user>`、`<assistant>`）所构建的**角色分层安全**——高优先级角色（系统、用户）的指令应覆盖低优先级角色（工具返回）的内容。然而，这一安全假设存在根本性漏洞：攻击者可以在工具返回的低优先级内容中**伪造角色标签**，从而绕过指令层级，使恶意指令被模型误读为高优先级的权威指令。

### 核心方法：ChatInject

本文提出 **ChatInject**，一种利用聊天模板进行提示注入的攻击方法。其核心洞察是：**通过将恶意载荷格式化为目标模型的原生聊天模板，攻击者能够利用模型对指令遵循的内在学习倾向，将恶意指令伪装为高优先级角色**。具体而言，ChatInject 在工具返回内容中嵌入伪造的系统/用户/助手角色标签，使模型在解析上下文时将这些注入内容误判为合法的对话轮次。在此基础上，攻击者还可嵌入模拟的多轮说服对话，在单次注入中构建虚拟的多轮上下文，实现**一次性多轮攻击**。

### 主要结果

在 AgentDojo 和 InjecAgent 两个基准上对 6 个开源 LLM 的评估表明：

- ChatInject 将 AgentDojo 上的平均攻击成功率（ASR）从 **5.18%** 提升至 **32.05%**（+26.87 pp），将 InjecAgent 上的平均 ASR 从 **15.13%** 提升至 **45.90%**（+30.77 pp）。
- 多轮说服变体在 InjecAgent 上达到平均 **52.33%** 的 ASR，对 Llama-4 的 ASR 高达 **88.3%**（+38.2 pp）。
- 攻击有效性的关键因果杠杆是**注入模板与目标模型原生模板的相似度**：相似度越高，ASR 越高，同时用户任务完成率（Utility）下降越显著。

### 方法定位

ChatInject 属于**基于格式的提示注入攻击**，其区别于现有工作的核心在于**直接伪造完整的角色标签结构**，而非仅利用特殊字符或语义混淆。与标准纯文本注入（Default InjecPrompt）相比，ChatInject 改变了两个关键设计槽位：

1. **有效载荷格式**：从无模板的纯文本，变为包含伪造角色标签、模仿目标模型原生聊天模板的结构化载荷。
2. **多轮对话构建**：从纯文本拼接的对话模拟，变为利用模板标签在单次工具返回中嵌入完整的多轮对话历史，使模型将注入内容视为先前的合法对话上下文。

该方法在攻击管道上包含四个模块：恶意载荷生成（使用 GPT-4.1 合成指令或多轮对话）、模板格式化、可选的推理钩子（`<think>` 令牌引导模型肯定性推理）和工具调用钩子（`<tool>` 令牌强制模型执行恶意工具调用）。

## 背景与动机

### LLM代理的安全困境

大型语言模型（LLM）代理正被广泛部署于需要与外部工具和数据进行交互的场景中。这类代理通常接收用户指令，调用工具获取信息，并根据工具返回的结果执行后续操作。然而，这种工具交互机制引入了一个根本性的安全漏洞：**间接提示注入**。攻击者无需直接接触用户或代理的输入接口，只需操控工具返回的内容，即可将恶意指令注入代理的决策流程。

现有的LLM代理普遍依赖**聊天模板**中的特殊令牌（如 `<system>`、`<user>`、`<assistant>` 等角色标签）来实现指令层级的安全隔离。这一设计的隐含假设是：系统级指令具有最高优先级，用户指令次之，而工具返回的内容处于最低优先级。模型在训练过程中习得了对这些角色标签的遵从倾向，从而形成了基于角色的安全层级。

### 核心漏洞：角色标签的可伪造性

该安全层级存在一个关键缺陷：**攻击者可以在低优先级的工具输出中伪造高优先级的角色标签**。由于工具返回的内容通常以纯文本形式嵌入对话上下文，攻击者只需在恶意载荷中插入目标模型的原生聊天模板令牌，即可使模型将注入内容误解为来自更高优先级角色的指令。这一漏洞的本质在于，模型对指令来源的判断依赖于文本中的角色标签，而非真实的通信信道——当标签可以被任意伪造时，整个安全层级便形同虚设。

### 现有攻击方法的局限

当前的间接提示注入攻击方法存在两个显著瓶颈：

1. **纯文本注入的脆弱性**：标准攻击（Default InjecPrompt）将恶意指令以纯文本形式嵌入工具返回内容，通常附加注意力吸引前缀。然而，由于缺乏角色标签的伪装，这类注入内容在模型的注意力分配中仍处于低优先级，容易被忽略或拒绝。实验表明，在 AgentDojo 基准上，六款开源模型的平均攻击成功率（ASR）仅为 **5.18%**。

2. **多轮攻击的单轮限制**：真实世界中，攻击者往往通过多轮对话逐步说服或误导模型。然而，在间接提示注入的场景下，攻击者通常只有一次注入机会——工具返回内容在单次交互中被消费。传统的多轮说服攻击（Default Multi-turn）仅以纯文本形式拼接“角色: 内容”，无法利用模型对对话结构的学习依赖，其说服力受限于单轮上下文的表达能力。

### ChatInject 的核心动机

针对上述瓶颈，本文提出 **ChatInject** 攻击框架，其核心洞察是：**通过滥用聊天模板，攻击者能将恶意指令伪装为高优先级角色，并可嵌入模拟多轮对话来实施一次性说服攻击**。

具体而言，ChatInject 在两个维度上突破了现有攻击的限制：

- **角色伪造**：将恶意载荷格式化为目标模型的原生聊天模板，包含伪造的 `<system>`、`<user>`、`<assistant>` 等角色标签，使注入内容在模型的语义层级中获得与系统指令或用户指令同等的“权威性”。
- **虚拟多轮对话**：利用模板标签在单次工具返回中嵌入完整的模拟多轮对话历史，使模型误以为正在参与一场已经进行中的说服性对话，从而在单次注入中实现多轮攻击的效果。

这一攻击范式揭示了LLM代理安全设计中的一个根本性矛盾：模型依赖文本格式来判断指令来源的权威性，但文本格式本身是可被任意伪造的。当攻击者掌握了目标模型的聊天模板结构，基于角色标签的安全隔离便失去了其设计意义上的保护作用。

## 核心创新

ChatInject 的核心创新在于**将攻击有效载荷格式化为目标模型的原生聊天模板**，从而将恶意指令伪装为高优先级角色（如系统或用户），绕过 LLM 代理中基于特殊令牌的角色分层安全机制。这一思路源于对瓶颈的精准把握：LLM 代理在训练中习得了对 `<system>`、`<user>` 等角色标签的指令层级服从倾向，而攻击者恰好可以在低优先级的工具返回内容中伪造这些标签，使模型误将注入内容视为权威指令。

### 关键变更槽位

与基线方法相比，ChatInject 在两个关键维度上进行了系统性改造：

**1. 有效载荷格式：从纯文本到伪造聊天模板**

默认的 `Default InjecPrompt` 和 `Default Multi-turn` 均以纯文本形式注入恶意指令，仅依赖注意力吸引前缀（如“忽略之前的指令”）来尝试劫持模型行为。ChatInject 将这一槽位替换为**包含伪造的系统/用户/助手角色标签的格式化载荷**，使其模仿目标模型的原生聊天模板结构。例如，在工具返回中嵌入 `<|im_start|>system\n恶意指令<|im_end|>` 这样的标签序列，利用模型对对话结构的习得性依赖，使注入内容获得与系统指令同等的优先级。

这一改造的效果是决定性的：在 AgentDojo 基准上，ChatInject 将 6 个开源模型的平均 ASR 从 5.18% 提升至 32.05%（+26.87 pp）；在 InjecAgent 上，从 15.13% 提升至 45.90%（+30.77 pp）。跨模型攻击实验进一步揭示了因果机制——**注入模板与目标模型模板的相似性越高，攻击成功率越高**（Figure 3），证实模板格式是调控攻击效果的核心因果旋钮。

**2. 多轮对话构建：从文本模拟到模板嵌入的一次性多轮攻击**

传统的多轮说服攻击（`Default Multi-turn`）仅以纯文本形式拼接“角色: 内容”对，无法利用模型在训练中建立的对话结构先验。ChatInject 通过**在单次工具返回中利用模板标签嵌入模拟的多轮对话历史**，实现了一次性多轮攻击。攻击者构建一个 $n$ 轮对话 $C_a = \{(r_1^a, m_1^a), \ldots, (r_n^a, m_n^a)\}$，将恶意指令 $I_a$ 嵌入消息 $m_i^a$ 中，再以目标模型的聊天模板格式包装后注入工具返回。模型在解析时会将这段伪造的对话历史视为真实的多轮交互上下文，从而被逐步说服执行恶意指令。

这一变更在 InjecAgent 上表现尤为突出：Multi-turn + ChatInject 对 Llama-4 的 ASR 达到 88.3%，较 `Default InjecPrompt` 的 50.1% 提升了 38.2 个百分点（Table 1）。在 Qwen-3 上，Multi-turn + ChatInject 的 ASR 为 65.9%，而纯文本多轮基线仅为 10.6%。

### 辅助增强模块

除上述两个核心槽位变更外，ChatInject 还引入了两个可选的辅助模块：

- **推理钩子（Reasoning Hook）**：在攻击载荷末尾附加肯定性推理提示（`Sure!`），并用 `<think>` 令牌包裹，引导模型的内部推理朝向注入目标。该模块在标准 ChatInject 基础上进一步提高 ASR（Table 1）。
- **工具调用钩子（Tool-calling Hook）**：在载荷末尾附加工具调用脚手架并用 `<tool>` 令牌包裹，强制模型执行恶意工具调用。该模块在 AgentDojo 上将 Qwen-3 的 ASR 推至 69.4%（+51.9 pp），但同时导致用户任务完成率（Utility）从 50.9% 骤降至 22.9%，体现了攻击强度与合法任务执行之间的权衡。

### 与现有工作的本质差异

现有提示注入攻击多聚焦于语义层面的操纵（如角色扮演、目标劫持），或对特殊令牌进行有限扰动。ChatInject 的独特之处在于**系统性地滥用聊天模板的结构化角色标签作为攻击向量**，将注入攻击从“说服模型”升级为“欺骗模型的对话解析器”。这一思路不仅显著提升了攻击成功率，还揭示了 LLM 代理在架构层面——而非仅在安全对齐层面——存在的根本性漏洞。

## 整体框架

![[assets/figures/papers/paper_list_l21_https_openreview_net_forum_id_WVhgFSKniL/figures/002_Figure_2.jpg]]
*Figure 2: Four attack payload variants embedded in the tool response R _ { T _ { u } } , categorized by injection method—plain text (left) vs. forged chat templates with ChatInject (right)—and by content: a pure attacker instruction (top) or multi-turn conversation (bottom). ⊕ denotes line-wise concatenation*

ChatInject 的攻击流程围绕一个核心因果开关展开：**是否将注入内容格式化为目标模型的原生聊天模板**。其完整 pipeline 包含四个可组合模块，输入为攻击者可控的工具返回内容，输出为被模型误认为高优先级指令的伪造对话上下文。

### 攻击形式化

在间接提示注入场景中，LLM 代理 $L$ 接收用户指令 $I_u$ 并调用工具 $T_u$，攻击者 $a$ 仅能操控工具返回内容 $R_{T_u}$，无法访问用户指令或代理内部提示。攻击者的目标是将恶意指令 $I_a$ 嵌入 $R_{T_u}$，使代理将其视为高优先级指令执行。

### Pipeline 模块

**1. 有效载荷生成（Payload Generation）**
该模块负责生成攻击内容，支持两种模式：
- **直接指令注入**：将恶意指令 $I_a$ 直接作为攻击载荷。
- **说服性多轮对话生成**：利用 GPT-4.1 合成一段 7 轮用户-助手对话 $C_a = \{(r_1^a, m_1^a), \ldots, (r_n^a, m_n^a)\}$，将恶意指令 $I_a \subseteq \bigcup_{i=1}^{n} m_i^a$ 嵌入对话消息中。生成提示经过人工设计，包含场景建立、指令分解和确保助手同意执行三个步骤，所有生成对话均经过人工审核。

**2. 模板格式化（Template Formatting）**
这是 ChatInject 的核心模块，将有效载荷包装为目标模型的原生聊天模板格式。具体做法是在工具返回内容中插入伪造的角色标签（如 `<system>`、`<user>`、`<assistant>`），使模型将低优先级的工具输出误解为高优先级的系统或用户指令。结合两种载荷生成模式和两种格式化方式（纯文本 vs. 模板），共产生四种攻击变体（见图 2）：
- **Default InjecPrompt**：纯文本格式的直接指令注入
- **InjecPrompt + ChatInject**：模板格式的直接指令注入
- **Default Multi-turn**：纯文本格式的多轮对话注入
- **Multi-turn + ChatInject**：模板格式的多轮对话注入

**3. 推理钩子（Reasoning Hook，可选）**
在攻击载荷末尾附加肯定性推理提示（`Sure!`），并用 `<think>` 令牌包裹，引导模型的内部推理朝向注入目标。该模块仅适用于显式提供推理令牌的模型。

**4. 工具调用钩子（Tool-calling Hook，可选）**
在攻击载荷末尾附加模拟代理调用约定的工具调用脚手架，用 `<tool>` 令牌包裹，强制模型执行恶意工具调用。同样仅适用于提供工具调用令牌的模型。

### 输入输出流

```
输入：攻击者可控的工具返回内容 R_{T_u}
  │
  ├─ 载荷生成 ──→ 恶意指令 I_a 或 多轮对话 C_a
  │
  ├─ 模板格式化 ──→ 嵌入伪造角色标签
  │
  ├─ [可选] 推理钩子 ──→ 附加 <think> 推理引导
  │
  ├─ [可选] 工具调用钩子 ──→ 附加 <tool> 调用脚手架
  │
  ▼
输出：被注入恶意载荷的工具返回内容，触发代理执行攻击者指令
```

### 关键设计决策

- **单次注入实现多轮攻击**：传统多轮攻击需要多步交互，ChatInject 通过在单次工具返回中嵌入完整的模拟对话历史，利用聊天模板的角色标签使模型一次性“体验”多轮说服过程。
- **模板相似性驱动迁移性**：跨模型攻击的成功率与注入模板和目标模型原生模板的相似度正相关（Figure 3）。当目标模型未知时，可使用模板混合（Mixture-of-Templates, MoT）策略——将所有已知模型的角色标签随机排列拼接，获得比单一模板更稳定且更高的攻击成功率（Figure 4）。

> **证据强度说明**：上述 pipeline 描述基于论文 Section 3.1–3.3 的明确阐述，所有模块均经过实验验证。四种攻击变体的有效性在 Table 1 中有系统对比，推理钩子和工具调用钩子的增益效果在 Section 4.2 中得到验证。

## 核心模块与公式推导

### 攻击形式化

ChatInject 的攻击场景建立在间接提示注入（Indirect Prompt Injection）的形式化框架之上。设 LLM 代理为 $L$，可调用的工具集为 $T$。用户 $u$ 向代理发出指令 $I_u$，代理调用工具 $T_u$ 并获得工具回复 $R_{T_u}$。攻击者 $a$ 无法访问用户指令 $I_u$ 或代理的内部提示，只能操控工具回复 $R_{T_u}$ 的内容。攻击者的恶意指令 $I_a$ 被嵌入到该工具回复中，成为代理必须处理的一部分上下文。

### 有效载荷生成模块

ChatInject 的核心创新在于有效载荷的格式构造。攻击者构建一个模拟的多轮对话历史：

$$C_a = \{(r_1^a, m_1^a), \ldots, (r_n^a, m_n^a)\}$$

其中每一轮 $i$ 包含角色标签 $r_i^a$ 和消息内容 $m_i^a$。恶意指令 $I_a$ 嵌入在对话消息的并集中：

$$I_a \subseteq \bigcup_{i=1}^{n} m_i^a$$

多轮对话通过 GPT-4.1 合成生成：首先人工设计一个系统提示，将攻击者指令包装为看似用户授权的附加请求，然后利用 GPT-4.1 生成 7 轮用户-助手对话。该提示的设计目标包括：(1) 建立攻击者指令看似必要的场景；(2) 将指令分解为看似无害的步骤；(3) 确保助手同意执行嵌入的指令。所有生成的对话均经过人工审核以确保上下文合理性和一致性。

### 模板格式化模块

有效载荷生成后，ChatInject 将其包装为目标模型的原生聊天模板格式。具体而言，攻击者使用伪造的角色标签（如 `<system>`、`<user>`、`<assistant>`）替代纯文本的角色标识，从而使注入内容在模型内部获得与高优先级指令相同的结构表征。这一操作产生了四种攻击变体：

- **Default InjecPrompt**：纯文本格式的恶意指令，无聊天模板包装。
- **InjecPrompt + ChatInject**：恶意指令包装为目标模型的聊天模板格式。
- **Default Multi-turn**：纯文本格式的多轮说服对话，以“角色: 内容”拼接。
- **Multi-turn + ChatInject**：多轮说服对话包装为目标模型的聊天模板格式。

### 推理钩子与工具调用钩子（可选模块）

为进一步增强攻击效果，ChatInject 提供两个可选的附加模块：

- **推理钩子（Reasoning Hook）**：在攻击者有效载荷末尾附加一个肯定性引导提示（如 `Sure!`），并用 `<think>` 令牌包裹，以引导模型的内部推理朝向注入目标。
- **工具调用钩子（Tool-calling Hook）**：在有效载荷末尾附加一个模仿常见代理提示约定的工具调用脚手架，并用 `<tool>` 令牌包裹，强制模型执行恶意工具调用。

这两个模块仅在目标模型显式提供相应模板令牌时可用，其效果在实验中得到验证（Table 1），能在标准 ChatInject 基础上进一步提高攻击成功率。

### 模板相似度度量

在跨模型迁移性分析中，模板相似度通过以下方式计算：将每个模型的所有角色标签拼接，提取嵌入向量，然后计算成对余弦相似度：

$$\text{Similarity}(T_M, T_{M'}) = \langle E_M(T_M), E_M(T_{M'}) \rangle$$

其中 $E_M(\cdot)$ 表示通过平均池化并归一化的隐藏状态提取的嵌入向量。由于资源限制，该相似度计算使用轻量级代理模型，可能影响度量的精确性。

## 实验与分析

### 核心发现：聊天模板注入的破坏性效果

ChatInject 在两个主流基准上对 6 个开源 LLM 代理进行了评估，结果揭示了聊天模板滥用的系统性危害。在 **AgentDojo** 上，标准纯文本注入（Default InjecPrompt）的平均攻击成功率（ASR）仅为 5.18%，而 ChatInject 将其提升至 **32.05%**（+26.87 pp）。在 **InjecAgent** 上，提升更为显著：从 15.13% 提升至 **45.90%**（+30.77 pp）。多轮说服变体（Multi-turn + ChatInject）在 InjecAgent 上进一步达到平均 **52.33%** 的 ASR，表明在工具输出中伪造多轮对话上下文是极其有效的攻击策略。

表 1 的细粒度数据显示了攻击效果的模型间差异。以 **Qwen-3** 为例，InjecPrompt + ChatInject 在 AgentDojo 上将 ASR 从 17.5% 拉升至 54.8%（+37.3 pp）；多轮变体在 InjecAgent 上达到 65.9%（+55.2 pp）。**Llama-4** 对多轮 ChatInject 尤为脆弱，InjecAgent 上的 ASR 高达 88.3%（+38.2 pp）。然而，**Grok-2** 表现出显著的鲁棒性：即使是多轮 ChatInject，其在两个基准上的 ASR 也仅为个位数，说明该模型可能具有更强的指令层级对齐或模板解析防御。

![[assets/figures/papers/paper_list_l21_https_openreview_net_forum_id_WVhgFSKniL/figures/003_Table_1.jpg]]
*Table 1: Results on InjecAgent and AgentDojo for six LLM agents. Colored deltas in parentheses indicate changes relative to the Default InjecPrompt. “think” and “tool” denote reasoning and tool-calling hooks, respectively. We evaluate the reasoning hook and the tool-calling hook only on models that explicitly provide such template tokens. The best results are in bold for each setting*

### 攻击成功与任务效用的权衡

ASR 的提升并非没有代价。在 AgentDojo 上，随着攻击成功率的上升，模型的用户任务完成率（Utility）出现系统性下降。以 Qwen-3 为例，良性 Utility 为 50.9%，而使用 InjecPrompt + ChatInject 后降至 28.3%（-22.6 pp）；加入工具调用钩子（+tool）后进一步降至 22.9%（-28.0 pp）。这一权衡反映了攻击者目标与合法用户目标之间的零和博弈：模型越是被恶意指令“说服”，就越倾向于放弃原始用户任务。表 4 汇总了所有开源模型在各攻击变体下的 Utility 变化，其中 GPT-oss 的 Utility 下降最为剧烈，部分攻击下接近归零。

![[assets/figures/papers/paper_list_l21_https_openreview_net_forum_id_WVhgFSKniL/figures/015_Table_4.jpg]]
*Table 4: Utilities of 6 Open-source LLMs in Various Attacks, including Benign Utility. Colored deltas in parentheses indicate changes relative to the benign Utility*

### 跨模型模板转移性

ChatInject 的威胁不仅限于已知目标模板的场景。图 3 和表 2 揭示了模板相似性与跨模型攻击成功率之间的强正相关：注入模板与目标模型原生模板的相似性越高，ASR 越高。**Qwen-3 模板**展现出最强的转移性，在 InjecAgent 上对闭源模型的平均 ASR 达 29.6%，在 AgentDojo 上达 23.5%。**Grok-3** 尽管是闭源模型，却对多种外来模板表现出意外的高脆弱性（InjecAgent 平均 ASR 17.9%，AgentDojo 22.6%），与 Grok-2 的强鲁棒性形成鲜明对比——这一差异值得进一步研究。

![[assets/figures/papers/paper_list_l21_https_openreview_net_forum_id_WVhgFSKniL/figures/005_Figure_3.jpg]]
*Figure 3: Performance of cross-model ChatInject attacks. As template similarity increases, the ASR (left) rises, while the model’s Utility (right) degrades. The shaded region represents the 95% confidence interval for each result, computed using the Wilson Interval*

![[assets/figures/papers/paper_list_l21_https_openreview_net_forum_id_WVhgFSKniL/figures/006_Table_2.jpg]]
*Table 2: Model-wise template transferability on InjecAgent and AgentDojo, where † denotes closedsource LLMs. All entries are ASR (%); colored deltas in parentheses indicate changes relative to the Default InjecPrompt. Yellow shading marks cases where the injected template family matches the target model family. Boldface highlights the best ASR per row*

当攻击者不知道目标模型时，**模板混合（Mixture-of-Templates, MoT）** 策略提供了更稳定的攻击效果。图 4 显示，MoT 在所有三个测试模型上均一致超越 Default InjecPrompt，且跨模型的 ASR 方差更小。图 8 进一步分析了模板排序（升序 vs. 降序按相似度）和模板数量对 MoT 效果的影响。

![[assets/figures/papers/paper_list_l21_https_openreview_net_forum_id_WVhgFSKniL/figures/007_Figure_4.jpg]]
*Figure 4: Visualization of the mean and std. for Single vs. MoT settings; the dashed line marks ASR of Default InjecPrompt*

### 攻击组件的消融分析

**推理钩子与工具调用钩子**。在标准 ChatInject 基础上附加推理钩子（+think，在 `<think>` 令牌中包裹肯定性提示 "Sure!"）和工具调用钩子（+tool，在 `<tool>` 令牌中包裹恶意工具调用脚手架），能进一步提高 ASR。如表 1 所示，Qwen-3 在 AgentDojo 上使用 +tool 变体达到 69.4% 的 ASR（+51.9 pp），但同时 Utility 降至 22.9%。这验证了利用模型原生推理和工具调用格式令牌的叠加攻击是有效的。

**说服技术与对话轮数**。图 7b（即 Figure 10）比较了四种说服技术的效果：时间压力（time_press）和社会惩罚（social_punish）的 ASR 最高（约 77%），权威（authority）次之（约 68%），谈判（negotiation）最低（约 53%）。这表明制造紧迫感和社交代价的说服策略比理性协商更能诱导模型服从。图 7a 显示，ASR 随对话轮数变化不大，但 Utility 随轮数增加而持续下降，说明更长的注入对话主要侵蚀的是合法任务执行能力。

**与真实攻击语料的对比**。表 3 显示，本文基于说服策略合成的多轮对话在 Qwen-3 上达到 80.5% 的 ASR，优于真实攻击语料的 76.3%；在 GLM-4.5 上优势更大（48.1% vs. 27.3%）。这说明精心设计的说服框架比直接使用现实世界攻击样本更具威胁性。

![[assets/figures/papers/paper_list_l21_https_openreview_net_forum_id_WVhgFSKniL/figures/014_Table_3.jpg]]
*Table 3: Comparison between our Persuasion multi-turn dialogue and real attack corpora*

### 防御评估与绕过

图 5 汇总了五种防御配置下 Qwen-3 和 Grok-3 的 ASR 与 Utility 变化。令人担忧的是，**所有四种提示级防御（注入检测器、Lakera Guard、指令预防、数据定界）均未能有效降低 ChatInject 的 ASR**；在某些情况下，防御反而略微提升了 ASR（可能因为防御提示本身引入了额外的模板令牌，增强了注入内容的“合法性”感知）。用户指令重复（repeat user）对 Utility 有一定保护作用，但同样未能显著压制 ASR。

![[assets/figures/papers/paper_list_l21_https_openreview_net_forum_id_WVhgFSKniL/figures/008_Figure_5.jpg]]
*Figure 5: Comparison of ASR (top) and Utility (bottom) for Qwen-3 and Grok-3 across defense configurations, aggregated over all attack types. Baselines are the per-model scores without defense: Default InjecPrompt and Default Multi-turn. The shaded region represents the 95% confidence interval for each result, computed using the Wilson Interval*

**模板扰动绕过**。针对可能出现的基于规则解析的防御，本文测试了三种字符级扰动（删除、替换、插入，各扰动 10% 的字符）。图 6 显示，所有扰动变体在三个模型上的 ASR 仍持续优于 Default InjecPrompt 和 Default Multi-turn，证明攻击对轻度模板变形具有鲁棒性。然而，**同形字编码**是一个例外：表 6 显示，使用同形字编码模板后，嵌入相似度急剧下降，导致 ChatInject 的 ASR 大幅降低（Llama-4 上从 17.2% 降至更低水平），说明依赖精确令牌嵌入匹配的攻击对语义保留但编码不同的变形较为脆弱。

![[assets/figures/papers/paper_list_l21_https_openreview_net_forum_id_WVhgFSKniL/figures/017_Table_6.jpg]]
*Table 6: Effect of homoglyph encoding on ChatInject performance*

### 注意力分布分析

表 5 的注意力分布分析为攻击机制提供了内部视角。在默认注入下，模型注意力主要分配给用户指令；而在 ChatInject 攻击下，**攻击者指令获得的注意力权重显著上升**，部分模型甚至超过了对用户指令的关注。这支持了核心假设：伪造的角色标签改变了模型内部的注意力分配，使低优先级的工具输出内容获得了类似高优先级系统/用户指令的“权威性”处理。

![[assets/figures/papers/paper_list_l21_https_openreview_net_forum_id_WVhgFSKniL/figures/016_Table_5.jpg]]
*Table 5: Attack-wise attention distribution of user and attacker instructions for each model*

### 失败模式与局限性

尽管 ChatInject 在多数模型上效果显著，但存在明确的失败边界：

1. **Grok-2 的强鲁棒性**：该模型在所有攻击变体下 ASR 均保持在个位数，表明其可能采用了更严格的模板解析或指令层级训练，使伪造的角色标签无法有效劫持模型行为。
2. **同形字编码失效**：依赖精确令牌嵌入的攻击在面对编码混淆时效果骤降，这为防御设计提供了潜在方向。
3. **Utility 的极端下降**：在 GPT-oss 等模型上，攻击导致 Utility 几乎归零，这可能触发异常检测系统，反而限制了攻击的隐蔽性。
4. **合成对话的局限性**：所有多轮对话均由 GPT-4.1 生成并经人工审核，可能未覆盖真实攻击者的多样化语言风格和策略空间。

### 待验证的开放性观察

以下观察来自论文分析，但证据强度有限，需读者自行核实原文细节：

- 模板相似度计算使用轻量级代理模型提取嵌入，可能影响相似性排序的精确性（见附录 D.3）。
- 闭源模型的 Utility 在模板转移攻击下的具体数值见表 7，但本文未深入讨论其与开源模型的差异原因。
- 采用 Claude 系统提示后的 ASR 变化见表 8，其对攻击效果的影响机制尚不明确。

![[assets/figures/papers/paper_list_l21_https_openreview_net_forum_id_WVhgFSKniL/figures/018_Table_7.jpg]]
*Table 7: Utility of Closed Source LLMs Against Template Transfer Setting*

![[assets/figures/papers/paper_list_l21_https_openreview_net_forum_id_WVhgFSKniL/figures/019_Table_8.jpg]]
*Table 8: ASR and relative change for adopting Claude sytem prompt*

## 方法谱系与知识库定位

### 攻击方法谱系中的定位

ChatInject 属于**间接提示注入（Indirect Prompt Injection）**攻击家族，其核心创新在于将攻击有效载荷格式化为目标模型的原生聊天模板。与现有注入攻击相比，ChatInject 的关键区别体现在两个维度：

**1. 与标准纯文本注入的对比。** 传统间接提示注入（本文称为 Default InjecPrompt）将恶意指令以纯文本形式嵌入工具返回内容中，依赖注意力吸引前缀（如"忽略之前的指令"）来劫持模型行为。ChatInject 的实验表明，这种纯文本方式在六个开源模型上的平均攻击成功率（ASR）仅为 5.18%（AgentDojo）和 15.13%（InjecAgent），而 ChatInject 将 ASR 提升至 32.05% 和 45.90%。这一巨大差距揭示了一个根本性瓶颈：**LLM 代理依赖特殊令牌（如 `<system>`、`<user>`）实现角色分层安全，但纯文本注入无法突破这一层级**。

**2. 与现有多轮注入攻击的对比。** 已有的多轮说服攻击需要攻击者在多个交互轮次中逐步引导模型，这在间接注入场景中通常不可行——攻击者通常只能控制单次工具返回的内容。ChatInject 通过**在单次工具输出中伪造角色标签来嵌入模拟多轮对话**，将多轮说服压缩为一次性攻击。这种"一次性多轮攻击"是 ChatInject 独有的能力：攻击者构建一个虚拟的 `C_a = {(r_1^a, m_1^a), ..., (r_n^a, m_n^a)}` 对话历史，其中恶意指令 $I_a \subseteq \bigcup_{i=1}^{n} m_i^a$ 被分散嵌入多个助手回复中，使模型误以为这些指令来自已授权的多轮交互。

### 攻击有效性的因果机制

ChatInject 的成功依赖于一个可操作的因果调节变量：**注入内容是否格式化为目标模型的原生聊天模板**。这一机制通过以下路径生效：

- **角色层级绕过**：聊天模板中的特殊令牌（如 `<|im_start|>system`、`<|im_start|>user`）在模型训练中被赋予了指令优先级语义。攻击者在低优先级的工具返回内容中伪造这些标签，使恶意指令被模型解析为高优先级角色（如系统或用户）的输入，从而绕过基于角色的安全层级。
- **模板相似度与攻击迁移**：跨模型攻击实验揭示了模板嵌入相似度与 ASR 之间的单调关系。当注入模板与目标模型原生模板的余弦相似度 $Similarity(T_M, T_{M'}) = \langle E_M(T_M), E_M(T_{M'}) \rangle$ 升高时，ASR 随之上升，用户任务完成率（Utility）则下降。这一发现将攻击有效性与模型内部的表征空间直接关联，为理解模板注入的迁移性提供了量化依据。
- **推理与工具调用钩子**：ChatInject 进一步利用模型自身的推理和工具调用机制。推理钩子在有效载荷后附加 `<think>` 包裹的肯定提示（"Sure!"），引导模型内部推理朝向攻击目标；工具调用钩子附加 `<tool>` 包裹的工具调用脚手架，强制模型执行恶意工具操作。这些钩子利用了模型对特定模板令牌的习得性响应，进一步放大了攻击效果。

### 适用边界与关键局限

ChatInject 的有效性受到以下边界条件的约束：

**模型依赖性。** 不同模型对模板注入的鲁棒性差异显著。Grok-2 在所有攻击变体下表现出较强的抵抗力，而 Qwen-3 和 Llama-4 则高度脆弱（Llama-4 在 Multi-turn + ChatInject 下 ASR 高达 88.3%）。这种差异可能与模型的安全对齐训练强度和模板解析机制有关，但论文未提供因果解释。

**模板先验知识需求。** ChatInject 的最优效果要求攻击者知晓目标模型的原生聊天模板。在未知目标模型时，论文提出的模板混合（Mixture-of-Templates, MoT）策略可以部分缓解这一问题——通过拼接多个模型的角色标签构建通用包装器——但 MoT 的 ASR 仍低于精确匹配目标模板的情况。

**多轮对话的合成偏差。** 攻击中使用的说服性多轮对话均由 GPT-4.1 合成生成，并经过人工审核。尽管论文声称这些对话在 ASR 上优于真实攻击语料库（Table 3），但合成数据可能未完全覆盖真实攻击者的说服策略多样性和语言风格的自然变异。

**防御评估的局限性。** 论文测试的防御方法仅限于提示级防御（注入检测器、指令预防、数据定界、用户指令重复），未涉及模型架构层面的防护（如安全对齐微调、指令层级训练）或运行时沙箱机制。实验还发现，对模板字符进行 10% 的随机删除、替换或插入扰动后，攻击仍保持有效性且高于默认基线，这表明基于规则解析的防御容易通过轻量扰动绕过。然而，同形字编码（homoglyph encoding）会导致 ASR 急剧下降，因为嵌入相似度极低——这暗示了基于表征的检测可能是一个有前景的方向。

### 开放问题

1. **防御机制设计**：如何在不过分牺牲模型效用的前提下，设计有效的检测与防御机制来抵御基于聊天模板的注入攻击？现有的提示级防御在实验中表现出反效果——部分防御配置下的 ASR 甚至高于无防御基线（Figure 5），这表明简单的提示工程可能不足以应对模板层级的漏洞。

2. **内部表征机制**：聊天模板标签如何具体改变模型的注意力分布和内部表征，从而赋予注入内容更高的"权威性"？论文的注意力分布分析（Table 5）提供了初步证据，但尚未揭示从令牌级注意力到行为级劫持的完整因果链条。

3. **更隐蔽的攻击变体**：在真实世界工具交互的开放式场景中，攻击者能否利用更隐蔽的模板伪造技术（如 Unicode 变形、编码混淆）绕过基于模式匹配的检测？同形字编码的失败表明表征层面的检测可能更鲁棒，但攻击者也可能针对性地优化嵌入相似度。

4. **根本性修复**：能否通过强化指令层级训练（instruction hierarchy training）或模板感知的安全微调，从根本上消除模型对伪造角色标签的脆弱性？这需要模型在训练阶段就学会区分真实角色标签和工具返回内容中的伪造标签，而非仅依赖提示级防护。

## 原文 PDF

![[paperPDFs/ICLR_2026/ChatInject_Abusing_Chat_Templates_for_Prompt_Injection_in_LLM_Agents.pdf]]
