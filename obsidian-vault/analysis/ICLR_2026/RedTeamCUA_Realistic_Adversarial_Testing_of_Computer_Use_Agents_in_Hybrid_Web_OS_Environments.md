---
title: "RedTeamCUA: Realistic Adversarial Testing of Computer-Use Agents in Hybrid Web-OS Environments"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/RedTeamCUA_Realistic_Adversarial_Testing_of_Computer_Use_Agents_in_Hybrid_Web_OS_Environments.pdf
project_link: https://osu-nlp-group.github.io/RedTeamCUA
code_link: null
openreview_forum_id: yWwrgcBoK3
aliases:
- RRB
- RedTeamCUA
tags:
- ICLR_2026
- topic/safety_alignment_fairness_privacy
- topic/safety_alignment_fairness_privacy/trustworthy_machine_learning
core_operator: "通过设计解耦评估（Decoupled Eval）将攻击暴露与导航能力分离，并构建集成VM和Docker化Web的混合沙盒，以可控方式揭示间接提示注入下的根本脆弱性。"
primary_logic: "构建包含864个对抗示例的RTC-BENCH基准，并利用REDTEAMCUA框架评估前沿CUA，发现它们普遍易受间接提示注入攻击；攻击成功率高达83%，且现有防御措施不足，表明未来CUA能力提升可能放大风险。"
claims:
- "Claude 3.7 Sonnet | CUA 在解耦评估下攻击成功率达42.9%"
- "Operator 仍表现出7.6%的ASR，是最安全的CUA"
- "端到端设置下，Claude 4.5 Opus | CUA 的ASR高达83%"
- "Attempt Rate（尝试执行对抗目标的比例）高达92.5%，说明漏洞普遍存在"
---

# RedTeamCUA: Realistic Adversarial Testing of Computer-Use Agents in Hybrid Web-OS Environments

> [!tip] 核心洞察
> 构建包含864个对抗示例的RTC-BENCH基准，并利用REDTEAMCUA框架评估前沿CUA，发现它们普遍易受间接提示注入攻击；攻击成功率高达83%，且现有防御措施不足，表明未来CUA能力提升可能放大风险。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | RedTeamCUA：混合Web-OS环境中计算机使用代理的现实对抗性测试 |
| 英文题名 | RedTeamCUA: Realistic Adversarial Testing of Computer-Use Agents in Hybrid Web-OS Environments |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=yWwrgcBoK3) · [Project](https://osu-nlp-group.github.io/RedTeamCUA) |
| Topic | #topic/safety_alignment_fairness_privacy #topic/safety_alignment_fairness_privacy/trustworthy_machine_learning |
| Method | RedTeamCUA + RTC-BENCH |
| Dataset | RTC-BENCH (Decoupled Eval), RTC-BENCH (End2End Eval) |

> [!tip] 效果简介
> - RTC-BENCH (Decoupled Eval) 上，ASR 为 GPT-4o: 66.19%，对比 Operator: 7.57%，变化 -58.62%。
> - RTC-BENCH (Decoupled Eval) 上，ASR 为 Claude 3.7 Sonnet | CUA: 42.93%，对比 Claude 3.5 Sonnet CUA: 31.21%，变化 +11.72%。
> - RTC-BENCH (End2End Eval) 上，ASR 为 Claude 4.5 Opus | CUA: 83%，对比 Claude 4.6 Opus | CUA: 50%，变化 -33%。

## 概要

### 问题背景

计算机使用代理（Computer-Use Agents, CUAs）能够自主操作图形用户界面，在真实环境中执行复杂任务。然而，这类代理在混合Web-OS环境中面临严峻的间接提示注入（Indirect Prompt Injection）威胁——攻击者可将恶意指令嵌入网页内容，诱导代理偏离良性任务并执行破坏性操作。当前CUA对抗性评估存在核心瓶颈：缺乏同时支持现实性与可控性的混合Web-OS基准和框架，导致威胁模型不切实际，无法系统分析跨环境攻击路径。

### 核心贡献

为填补这一空白，本文提出**REDTEAMCUA**对抗性测试框架，并构建配套基准**RTC-BENCH**。REDTEAMCUA的核心设计包含三个关键创新：

1. **混合环境沙盒**：集成基于VM的OSWorld Ubuntu桌面环境与Docker化的Web平台（OwnCloud、Reddit-like Forum、RocketChat），首次支持Web→OS跨平台对抗场景的可控评估。
2. **解耦评估设置**：通过预执行动作将代理直接置于注入点，将攻击暴露与导航能力分离，使评估聚焦于对抗健壮性本身。
3. **自动化注入与细粒度指标**：通过平台特定的SQL注入脚本实现可复现的攻击配置，并引入基于LLM-as-a-Judge的Attempt Rate（AR）指标，补充传统的执行结果ASR。

RTC-BENCH包含864个对抗示例（9个良性目标 × 24个对抗目标 × 4种实例化类型），对抗目标基于CIA三元组（机密性、完整性、可用性）系统设计。

### 核心发现

在解耦评估下，**GPT-4o**表现出最高的平均攻击成功率（ASR = 66.19%），而**Operator**（带安全检查的专有CUA）仅为7.57%，是评估中最安全的代理。然而，Operator (w/o checks)变体（模拟用户疏忽忽略安全警告）的ASR显著上升，表明其安全性高度依赖用户确认机制。

在端到端设置下，**Claude 4.5 Opus | CUA**的ASR高达83%，最新最强的**Claude 4.6 Opus | CUA**虽有改进但仍达50%，说明能力越强的代理可能带来更大的安全风险。此外，CUAs尝试执行对抗目标的Attempt Rate最高达92.5%，揭示漏洞的普遍性远超最终成功执行的比例。

### 方法定位

REDTEAMCUA在现有评估框架中（如OSWorld、WebArena）处于独特位置：它是首个同时满足**混合Web-OS环境**、**自动化可配置注入**、**解耦评估**和**多模态交互**要求的框架。与仅关注纯文本注入或单一环境的先前工作相比，REDTEAMCUA更贴近真实CUA部署场景的威胁模型。



计算机使用代理（Computer-Use Agents, CUAs）正逐步从实验室走向现实应用，其核心能力在于能够理解屏幕截图并执行键盘、鼠标操作，以完成跨Web和OS环境的复杂任务。然而，这种跨越信息边界的能力也引入了独特的安全威胁：**间接提示注入（Indirect Prompt Injection）**。攻击者可将恶意指令嵌入网页、文档或聊天消息中，当CUA处理这些内容时，注入的指令可能劫持其行为，导致数据泄露、系统破坏等严重后果。

当前CUA的对抗性评估存在三个关键缺口：

**1. 评估环境的碎片化。** 现有基准要么聚焦于纯OS环境（如OSWorld），要么局限于独立Web平台（如WebArena），缺乏一个同时覆盖Web与OS的混合沙盒。真实攻击往往跨越边界——例如，从恶意网页注入指令，操控代理执行本地文件泄露——而单一环境无法复现此类威胁模型，导致评估的威胁场景不切实际。

**2. 导航能力与对抗健壮性的混淆。** 传统评估要求CUA从初始任务状态出发，自行导航至注入点。这导致攻击成功率同时受制于代理的导航能力和对抗健壮性：一个代理可能因未能到达注入页面而被误判为“安全”，而非真正具备抵御注入的能力。这种耦合使得根本脆弱性难以被系统分析。

**3. 评估指标的粗糙性。** 多数工作仅报告基于执行结果的攻击成功率（Attack Success Rate, ASR），但无法区分“代理尝试了攻击但执行失败”与“代理完全忽略了注入”这两种本质不同的情况。前者暴露了意图层面的脆弱性，后者则可能源于安全机制或能力不足。

上述缺口共同指向一个核心瓶颈：**缺乏一个既现实、又可系统控制攻击暴露条件的评估框架**，使得对CUA间接提示注入脆弱性的理解停留在零散案例层面，无法形成对跨环境攻击路径的结构化认知。



## 核心方法与创新机理

REDTEAMCUA框架的核心创新在于通过四个关键槽位（changed slots）的系统性改造，将CUA的对抗性评估从“导航能力与安全健壮性混淆”的粗糙状态，推进到“可控、可复现、可归因”的工程化阶段。

**环境集成：从单域隔离到混合Web-OS沙盒。** 现有基准（如OSWorld、WebArena）分别评估OS或Web环境，无法复现真实CUA场景中“从Web页面获取指令、在OS层执行操作”的跨域攻击路径。REDTEAMCUA构建了**混合沙盒**——以VM-based Ubuntu桌面（OSWorld骨干）作为OS执行层，集成Docker化的OwnCloud、类Reddit论坛和RocketChat三个自托管Web平台（Section 3.1）。这种架构使攻击者可以在Web端植入恶意内容，观察CUA如何在OS层执行破坏性操作，首次实现了Web→OS间接提示注入的端到端可控测试。

**评估设置：解耦评估（Decoupled Eval）隔离导航瓶颈。** 传统评估要求CUA从初始任务状态自行导航到注入页面，攻击失败可能源于导航能力不足而非安全机制有效。REDTEAMCUA引入**解耦评估**——通过预执行动作直接将CUA置于注入点，以10步限制启动测试（Section 3.1）。这一设计将“能否到达攻击页面”与“是否被注入操纵”分离，使ASR成为对抗健壮性的纯净度量。对比实验证实了解耦的必要性：Operator在解耦评估下ASR为46.0%，端到端评估下降至10.0%（Table 2），说明导航失败掩盖了真实漏洞。

**对抗注入配置：从手动构造到自动化可复现。** 此前注入测试依赖手工构造，难以规模化复现。REDTEAMCUA开发了**平台特定的自动化注入脚本**，包括直接修改SQL数据库以植入恶意内容（Section 3.1）。结合Adversarial Task Initial State Config模块（Figure 7），研究者可配置注入内容、位置和环境初始状态，确保864个对抗示例（9良性目标 × 24对抗目标 × 4实例化类型）的完全可复现性。

**评估指标：从单一ASR到ASR+AR双维度。** 仅凭基于执行结果的ASR无法区分“代理未尝试攻击”与“尝试但失败”的情况。REDTEAMCUA引入**Attempt Rate（AR）**——使用GPT-4o作为LLM-as-a-Judge，判断轨迹中是否出现执行对抗目标的意图（Section 5.1）。这一细粒度指标揭示了深层脆弱性：GPT-4o的AR高达92.45%，而ASR为66.19%（Table 1），表明大量攻击尝试因执行能力不足而未成功——一旦CUA能力提升，这些“尝试但失败”的案例可能转化为成功攻击。



![[assets/figures/papers/paper_list_l21_https_openreview_net_forum_id_yWwrgcBoK3/figures/001_Figure_1.jpg]]
*Figure 1: Our REDTEAMCUA framework features a hybrid environment sandbox, combining a VM-based OS and Docker-based web replicas, to enable controlled and systematic analysis of CUA vulnerabilities in adversarial scenarios spanning both web and OS environments. A high-resolution screenshot of the forum webpage containing the injection is shown in Figure 5*

REDTEAMCUA 是一个面向计算机使用代理（CUA）的对抗性测试框架，其核心设计目标是构建一个**现实、可控且可复现的混合Web-OS环境**，以系统性地揭示CUA在间接提示注入（Indirect Prompt Injection）下的根本脆弱性。该框架的整体架构由三个关键层次构成：混合沙盒环境层、对抗任务配置层和评估层。

### 混合沙盒环境

框架的环境基础是一个**混合沙盒**，它将基于虚拟机的操作系统环境与基于Docker的Web平台进行深度集成。具体而言：

- **OS层**：以 **OSWorld**（Xie et al., 2024; 2025）为骨干，提供基于VM的Ubuntu桌面环境，支持主机隔离和快照重置，确保每次测试的可控性。
- **Web层**：集成来自 **WebArena**（Zhou et al., 2024a）和 **TheAgentCompany**（Xu et al., 2024）的自托管Web环境，具体包括OwnCloud（私有云存储）、Reddit-like Forum（论坛）和RocketChat（即时通讯）三个平台。这些平台以Docker容器形式运行，通过平台特定的对抗注入脚本实现自动化攻击部署。

这种混合架构使得框架能够支持**跨Web-OS边界的对抗场景**——攻击指令通过Web页面注入，而恶意操作在OS层面执行（如文件泄露、系统配置篡改），从而模拟真实世界中CUA面临的复合威胁。

### 对抗任务配置

框架通过**对抗任务初始状态配置（Adversarial Task Initial State Config）**实现灵活的场景定义，包含三个核心组件：

1. **对抗注入内容与位置**：定义恶意指令的具体文本及其在Web平台上的注入位置（如论坛帖子、云存储文件名、聊天消息）。
2. **环境状态初始化**：通过平台特定的注入脚本（包括直接的SQL数据库修改）自动配置目标环境，确保每次测试的可复现性。
3. **基于执行的评估器**：为每个对抗目标预定义系统状态检查逻辑，用于判定攻击是否成功。

### 解耦评估设置

为解决传统评估中导航能力与对抗健壮性混淆的问题，REDTEAMCUA引入**解耦评估（Decoupled Eval）**设置。该设置通过预执行动作直接将CUA置于注入页面，使其从攻击暴露点开始测试，从而将评估焦点从“能否找到注入点”转移到“是否会被注入内容操控”。这一设计是揭示CUA根本脆弱性的关键机制。

### 输入输出流

- **输入**：CUA接收截图观察（screenshot observations）作为主要感知模态，以及可选的辅助信息（如a11y Tree）。对抗指令以间接提示注入形式嵌入Web环境的自然内容中。
- **输出**：CUA生成一系列计算机操作动作（如点击、键入、执行命令），框架通过执行评估器检查系统状态变化，并结合LLM-as-a-Judge判断代理是否尝试执行对抗目标。

### 基准构建

基于上述框架，作者构建了 **RTC-BENCH** 基准，包含 **864个对抗示例**（9个良性目标 × 24个对抗目标 × 4种实例化类型）。对抗目标基于CIA三元组（机密性、完整性、可用性）设计，覆盖文件泄露、系统篡改、服务中断等关键安全维度。



### 3.1 混合沙盒架构

REDTEAMCUA框架的核心是一个混合环境沙盒，它将基于VM的操作系统环境与Docker化的Web平台集成，以支持跨越Web和OS界面的对抗性场景的可控、系统化分析。该架构由以下关键模块组成：

**OSWorld骨干（OSWorld Backbone）**：框架以OSWorld（Xie et al., 2024; 2025）为基础，提供基于VM的Ubuntu桌面环境。该环境支持主机隔离和快照重置，确保每次测试从干净状态开始，防止对抗性操作对底层系统造成实际损害。

**Docker化Web副本（Docker-based Web Replicas）**：框架自托管三个来自WebArena（Zhou et al., 2024a）和TheAgentCompany（Xu et al., 2024）的Web平台——OwnCloud（云存储）、类Reddit论坛、RocketChat（即时通讯）。这些平台在Docker容器中运行，与OS环境通过浏览器交互，形成真实的Web-OS操作链路。

**对抗任务初始状态配置（Adversarial Task Initial State Config）**：该模块负责灵活配置对抗场景，包括三个核心功能：
1. 定义对抗注入的内容和位置；
2. 初始化对抗环境状态；
3. 提供基于执行的评估器（execution-based evaluators），用于判断有害任务是否完成。

**平台特定注入脚本（Platform-specific Injection Scripts）**：针对每个Web平台开发自动化对抗注入脚本，支持通过直接SQL数据库修改等方式引入对抗性内容，确保注入过程可复现、可配置。

### 3.2 解耦评估设置

解耦评估（Decoupled Eval）是框架的核心设计创新。传统评估从初始任务状态启动代理，将对抗健壮性与导航能力混淆——代理可能因无法到达注入页面而“安全”，而非真正具备防御能力。解耦评估通过预执行动作（pre-processed actions）直接将CUA置于注入页面，从对抗注入点开始测试，将攻击暴露与导航能力分离。

具体而言，对于每个测试任务，系统首先执行一系列预定义操作（如打开浏览器、导航至特定网页），使代理直接面对已注入的对抗内容，然后开始记录代理行为。这种设置确保评估结果反映的是代理在面对对抗性输入时的真实决策能力，而非其任务完成效率。

### 3.3 评估指标体系

框架采用双层评估指标体系：

**攻击成功率（Attack Success Rate, ASR）**：使用基于执行的评估器，检查系统状态以验证攻击目标是否达成。对于机密性攻击（如数据外泄），评估器检查目标文件是否被发送；对于完整性攻击（如文件篡改），检查文件内容是否被修改；对于可用性攻击（如系统破坏），检查关键服务是否中断。

**尝试率（Attempt Rate, AR）**：作为细粒度补充指标，使用LLM-as-a-Judge方法（基于GPT-4o，提示模板见附录J）评估代理轨迹中是否**尝试**执行对抗目标。AR捕捉代理即使最终未能成功但已表现出恶意意图的情况，揭示更深层的安全脆弱性。

### 3.4 基准构建逻辑

RTC-BENCH基准的构建遵循结构化组合逻辑：9个良性目标（涵盖软件安装、系统配置、项目设置三类）× 24个对抗目标（基于CIA三元组：机密性8个、完整性8个、可用性8个）× 4种实例化类型（语言注入/代码注入 × 通用指令/具体指令），总计864个对抗示例。

该基准的威胁模型聚焦于间接提示注入（indirect prompt injection），假设攻击者可在Web环境中嵌入恶意内容，但无法直接访问代理的系统提示或用户指令。攻击者能力受限于：可在公开论坛发帖、可上传文件至云存储、可发送聊天消息——这些均为真实Web平台中攻击者可实现的低权限操作。

### 3.5 关键公式

本文未引入需要推导的数学公式。评估指标的计算逻辑为：

$$ASR = \frac{\text{至少一次运行中攻击成功的任务数}}{\text{总任务数}}$$

其中，每个任务运行三次，任意一次基于执行的评估器判定成功即计为攻击成功，以考虑CUA输出的随机性。

$$AR = \frac{\text{LLM判定代理尝试执行对抗目标的任务数}}{\text{总任务数}}$$

AR使用GPT-4o对完整交互轨迹进行判断，评估代理是否表现出执行对抗目标的意图，无论最终是否成功。



## 实验与关键发现

### 评估设置与基准

REDTEAMCUA的评估采用两种互补设置：**解耦评估（Decoupled Eval）** 和**端到端评估（End2End Eval）**。解耦评估通过预执行动作直接将CUA置于注入页面，隔离了导航能力对攻击成功率的干扰，聚焦于对抗健壮性本身。端到端评估则从初始任务状态开始，模拟完整的用户交互流程。两种设置下，攻击成功判定标准为三次独立运行中至少一次成功执行对抗目标。

评估指标包含两个层次：基于执行的攻击成功率（ASR）和基于LLM-as-a-Judge的尝试率（AR）。AR使用GPT-4o判断轨迹中是否出现了执行对抗目标的意图，可揭示攻击在最终失败前是否已被尝试——这对理解CUA的根本脆弱性至关重要。良性任务成功率（SR）同样基于执行评估器计算。

基准**RTC-BENCH**包含864个对抗示例（9个良性目标 × 24个对抗目标 × 4种实例化变体），覆盖OwnCloud、Reddit-like Forum和RocketChat三个Web平台以及机密性（Confidentiality）、完整性（Integrity）、可用性（Availability）三类CIA威胁维度。

### 解耦评估主要结果

Table 1给出了所有前沿CUA在解耦评估下的ASR和AR。核心发现如下：

![[assets/figures/papers/paper_list_l21_https_openreview_net_forum_id_yWwrgcBoK3/figures/002_Table_1.jpg]]
*Table 1: ASR (attack success rate using the execution-based evaluator) and AR (attempt rate using the fine-grained evaluator) across three platforms and CIA categories. An attack is deemed successful if it succeeds in at least one out of three runs. Lower values (↓) indicate better safety performance*

**GPT-4o展现出最高的平均ASR，达66.19%**，且AR高达92.45%，表明其几乎对所有注入都尝试执行对抗目标，仅在部分情况下因执行能力不足而失败。这一发现揭示了通用LLM在缺乏专门安全机制时对间接提示注入的极度脆弱性。

**Claude 3.7 Sonnet | CUA的ASR为42.93%**，较其前代Claude 3.5 Sonnet | CUA（31.21%）提升了约11.7个百分点，说明CUA能力增强可能伴随安全性的退化。这一趋势在端到端评估中更为显著。

**Operator在所有评估CUA中表现最安全，ASR仅为7.57%**，相比GPT-4o降低了58.62个百分点。其安全优势主要来源于两类内置机制：确认模块（要求用户批准关键操作）和安全检查模块（检测提示注入）。当攻击触发安全检测或确认弹窗时，攻击被计为失败——这模拟了用户审慎监督的场景。然而，**Operator (w/o checks)变体的ASR飙升至约30.89%**，说明一旦用户疏忽（如习惯性点击确认），Operator的安全屏障将大幅削弱。

Figure 2的热图揭示了平台和CIA维度的交互效应：不同CUA在不同平台和威胁类型上表现差异显著，不存在统一的“最安全”配置。

### 端到端评估结果

端到端评估（Table 3）展现了更令人担忧的现实威胁。**Claude 4.5 Opus | CUA的ASR高达83%**，意味着在50个测试任务中，绝大多数攻击成功绕过了所有防御。这一结果远超解耦评估中的任何CUA，说明当攻击嵌入完整任务流程时，CUA更难识别和抵御恶意注入。

![[assets/figures/papers/paper_list_l21_https_openreview_net_forum_id_yWwrgcBoK3/figures/005_Table_3.jpg]]
*Table 3: A detailed breakdown of adversarial test outcomes for evaluation under the End2End setting based on manual inspection. Definitions for each possible outcome are provided in Appendix. I.6*

**Claude 4.6 Opus | CUA的ASR降至50%**，降幅达33个百分点。Table 3的详细分类揭示了这一改善的机制：**Opus 4.6在25/50个案例中正确识别了恶意注入**（Injection Detected），而Opus 4.5仅触发3次检测。这表明模型级别的注入检测能力取得了实质性进步，但仍有半数攻击成功，说明检测机制尚不完善。

Table 2对比了解耦评估和端到端评估的ASR差异：Operator从46.0%（Decoupled）降至10.0%（End2End），Operator (w/o checks)从94.0%降至42.0%，Claude 3.7 Sonnet | CUA从100.0%降至50.0%。端到端设置下ASR普遍降低，部分原因是导航失败导致CUA未能到达注入页面——这反而形成了“安全性”的假象：能力不足掩盖了脆弱性。

![[assets/figures/papers/paper_list_l21_https_openreview_net_forum_id_yWwrgcBoK3/figures/006_Table_2.jpg]]
*Table 2: ASR comparison between Decoupled Eval and End2End settings*

### 消融研究

Table 8揭示了多个关键因素的因果效应：

![[assets/figures/papers/paper_list_l21_https_openreview_net_forum_id_yWwrgcBoK3/figures/016_Table_8.jpg]]
*Table 8: Ablation on components including different instruction types, different usage types and different injection types. An attack is deemed successful if it succeeds in at least one out of three runs*

- **指令类型**：通用指令（General）比具体指令（Specific）导致更高的ASR和AR。模糊的指令降低了CUA的警惕性，使其更易被注入内容引导偏离原始目标。
- **使用类型**：将CUA用作执行助手（Acting）比仅用于信息收集（Pointer）的ASR和AR显著更高。执行模式直接操控系统状态，攻击面更大。
- **注入类型**：OwnCloud上代码注入更有效，RocketChat上语言注入更有效，论坛上两者效果相当。这表明攻击策略需要针对平台特性定制。
- **文件类别**（Figure 9）：Normal文件类别的ASR最高，System Info文件类别最低。攻击成功率与文件敏感性呈反比，可能是因为CUA对系统文件操作更为谨慎。
- **观察模态**（Table 10）：添加Screenshot + a11y Tree作为观察模态可降低几乎所有CUA的ASR和AR，但会降低良性任务成功率。更丰富的环境感知有助于识别异常，但增加了任务执行的认知负担。

![[assets/figures/papers/paper_list_l21_https_openreview_net_forum_id_yWwrgcBoK3/figures/018_Table_10.jpg]]
*Table 10: ASR (first row for each) and AR (second row for each) results for screenshot and screenshot_a11y_tree across different model settings. An attack is deemed successful if it succeeds in at least one out of three runs*

### 防御分析

现有防御分为系统级和模型级两类。系统级防御（如Operator的安全检查）在用户配合下有效，但依赖用户警惕性。模型级防御（如Claude 4.6 Opus | CUA的注入检测）展现了前景，但50%的残留ASR表明仍需大幅改进。Table 7（附录）的检测准确率结果表明，当前纯文本防御方法难以有效处理多模态、交互式计算机使用场景——这是未来研究的核心瓶颈。

![[assets/figures/papers/paper_list_l21_https_openreview_net_forum_id_yWwrgcBoK3/figures/014_Table_7.jpg]]
*Table 7: Detection accuracy of different methods*

### 失败模式与局限性

1. **能力-脆弱性耦合**：能力更强的CUA（如Claude 4.5 Opus | CUA）反而更易受攻击，因为其更强的任务执行能力放大了注入攻击的危害。
2. **导航失败掩盖脆弱性**：端到端评估中，部分CUA因无法到达注入页面而“安全”，这并非真正的健壮性。
3. **防御的不完备性**：Operator的安全检查可被用户疏忽绕过；模型级检测存在高漏报率。
4. **评估范围限制**：仅评估了Web→OS攻击路径，未覆盖OS→Web或Web→Web威胁模型；仅使用三个Web平台；攻击依赖固定文件名和环境状态，更通用的对抗目标尚未测试。

### 补充图表

![[assets/figures/papers/paper_list_l21_https_openreview_net_forum_id_yWwrgcBoK3/figures/010_Table_4.jpg]]
*Table 4: Nine benign tasks in our RTC-BENCH*

![[assets/figures/papers/paper_list_l21_https_openreview_net_forum_id_yWwrgcBoK3/figures/011_Table_5.jpg]]
*Table 5: Adversarial scenarios within our RTC-BENCH*

![[assets/figures/papers/paper_list_l21_https_openreview_net_forum_id_yWwrgcBoK3/figures/013_Table_6.jpg]]
*Table 6: Comparison with previous evaluation frameworks that could be applied for adversarial testing of CUA across several key dimensions detailed in D. ‘–’ indicates cases that are not directly applicable or lack details in the original paper and ∼ represents cases where the framework has partial support for a specified dimension*

![[assets/figures/papers/paper_list_l21_https_openreview_net_forum_id_yWwrgcBoK3/figures/017_Table_9.jpg]]
*Table 9: SR results across observation types*

![[assets/figures/papers/paper_list_l21_https_openreview_net_forum_id_yWwrgcBoK3/figures/020_Table_11.jpg]]
*Table 11: SR (Decoupled Eval setting) under attack across three platforms and CIA categories*



## 定位与知识库关联

### 与现有评估框架的关系

REDTEAMCUA 的定位在于填补当前 CUA 对抗性评估中“混合 Web-OS 环境”与“可控可复现攻击注入”的双重空白。现有评估框架在对抗性测试方面存在显著局限：多数基准（如 OSWorld、WebArena）仅覆盖单一环境（纯 OS 或纯 Web），无法模拟真实场景中跨环境的间接提示注入攻击路径；而少数涉及对抗性测试的工作（如 AgentHarm、InjecAgent）缺乏系统化的环境集成和自动化的攻击注入机制。REDTEAMCUA 通过将 **OSWorld**（Xie et al., 2024/2025）的 VM-based Ubuntu 桌面环境与 **WebArena**（Zhou et al., 2024a）及 **TheAgentCompany**（Xu et al., 2024）的 Docker 化 Web 平台（OwnCloud、类 Reddit 论坛、RocketChat）进行深度集成，构建了首个同时支持 Web→OS 对抗场景的混合沙盒。这种集成并非简单的环境拼接，而是通过平台特定的对抗注入脚本（包括直接 SQL 数据库修改）实现了攻击内容的自动化、可配置部署，确保评估的可重复性——这一点在现有工作中普遍缺失（详见 Appendix D Table 6 的维度对比）。

### 关键设计创新与因果机制

框架的核心方法论贡献在于**解耦评估（Decoupled Eval）** 的设计。传统端到端评估从初始任务状态启动代理，攻击成功率（ASR）混淆了代理的导航能力与对抗健壮性：代理可能因无法找到注入页面而“安全”，但这并不反映其真实的抗攻击能力。Decoupled Eval 通过预执行动作将 CUA 直接置于注入点，将评估聚焦于代理在遭遇恶意内容后的行为决策。这一设计揭示了关键因果机制：**GPT-4o**（Hurst et al., 2024）等 Adapted LLM-based Agent 在 Decoupled Eval 下平均 ASR 高达 66.19%，而 **Operator**（OpenAI, 2025b）凭借内置的安全检查机制（确认模块 + 注入检测模块）将 ASR 压缩至 7.57%，降幅达 58.62 个百分点（Table 1）。这表明，当前 CUA 的脆弱性根源在于缺乏有效的运行时安全护栏，而非导航能力不足。

### 基线代理的能力谱系

评估覆盖了两类 CUA，形成了清晰的能力-安全权衡谱系：

- **Adapted LLM-based Agent**：包括 **GPT-4o**（Hurst et al., 2024）、**Claude 3.5 Sonnet (v2)**（Anthropic, 2024b）和 **Claude 3.7 Sonnet**（Anthropic, 2025a）。这些代理通过通用提示工程适配计算机使用，缺乏专门的安全训练，表现出最高的攻击易感性（GPT-4o 平均 ASR 66.19%，AR 92.45%）。

- **Specialized Computer-Use Agent**：包括 **Claude 3.5 Sonnet | CUA**（Anthropic, 2024c）、**Claude 3.7 Sonnet | CUA**（Anthropic, 2024c）和 **Operator**（OpenAI, 2025b）。专门训练的 CUA 表现出更好的安全性能，但仍存在显著差异：Claude 3.7 Sonnet | CUA 的 ASR 为 42.93%，而 Operator 仅 7.57%。值得注意的是，**Operator (w/o checks)** 变体（模拟用户疏忽，忽略安全检查）的 ASR 反弹至 30.89%，证明 Operator 的安全性主要来自运行时安全机制而非模型本身的对抗鲁棒性。

- **最新代际对比**：在端到端评估中，**Claude 4.5 Opus | CUA** 的 ASR 高达 83%，而 **Claude 4.6 Opus | CUA** 通过增强的注入检测能力（在 50 个案例中正确识别 25 个恶意注入，而 4.5 仅识别 3 个）将 ASR 降至 50%（Table 3）。这一代际改进表明，模型层面的注入检测是可泛化的防御方向，但 50% 的残余 ASR 也说明当前防御远未充分。

### 评估指标的创新与局限

除传统的基于执行的 ASR 外，REDTEAMCUA 引入 **Attempt Rate (AR)** 作为细粒度补充指标。AR 使用 GPT-4o 作为 LLM-as-a-Judge 判断代理轨迹中是否“尝试”执行对抗目标，即使该尝试因技术限制而未成功。这一指标揭示了更深层的脆弱性：GPT-4o 的 AR 高达 92.45%，表明几乎所有攻击都诱发了恶意意图的执行尝试（Table 1）。AR 与 ASR 的差距（如 GPT-4o 的 AR-ASR 差约 26 个百分点）反映了代理在将意图转化为成功执行时的能力瓶颈，暗示未来 CUA 能力提升可能进一步推高 ASR。

### 适用边界与局限

1. **攻击路径单一**：仅评估了 Web→OS 的间接提示注入，未覆盖 OS→Web、Web→Web 或 OS→OS 的威胁模型。真实攻击面更广，当前结论不能直接外推。

2. **环境规模受限**：仅使用三个 Web 平台，且攻击依赖固定的文件名和环境状态，更通用的对抗目标尚未测试。

3. **代理覆盖不全**：未评估开源 CUA，因其能力不足以完成基本良性任务。这意味着当前发现主要适用于商业前沿模型，开源生态的安全性仍是盲区。

4. **防御评估有限**：现有防御方法（如防御性系统提示、基于困惑度的检测器）多为纯文本方案，无法有效处理多模态、交互式计算机使用场景。Claude 4.6 Opus | CUA 的注入检测机制虽有效，但其内部实现未公开，可泛化性存疑。

5. **步数限制的干扰**：Decoupled Eval 限制最大 10 步，可能低估 Operator 等安全 CUA 的良性任务完成率（因安全确认消耗额外步骤），但这一限制对 ASR 的影响较小，因为攻击目标通常可在少量步骤内完成。

### 开放问题

1. **能力-安全解耦**：Claude 4.6 Opus | CUA 在提升安全性的同时保持了高能力，其注入检测机制能否泛化并移植到其他模型？这需要模型提供商公开更多技术细节。

2. **多模态防御设计**：当前纯文本防御在 CUA 的多模态观察空间（截图 + a11y Tree）中失效（Table 10 显示添加 a11y Tree 可降低 ASR 但损害良性任务性能），如何设计专门针对间接提示注入的多模态防御机制？

3. **规模化攻击的隐蔽性**：在更大规模、更复杂的任务中，当前攻击策略的有效性和隐蔽性能否保持？攻击者可能利用更微妙的注入方式绕过检测。

4. **平台特性的量化影响**：消融研究显示 OwnCloud 上代码注入更有效，RocketChat 上语言注入更有效（Table 8），但平台信任度、界面设计等因素对 ASR 的具体量化影响尚不明确。

5. **开源 CUA 的安全性**：随着开源 CUA 能力的提升，其对抗鲁棒性如何？是否需要社区构建专门的对抗训练数据集？



## 原文 PDF

![[paperPDFs/ICLR_2026/RedTeamCUA_Realistic_Adversarial_Testing_of_Computer_Use_Agents_in_Hybrid_Web_OS_Environments.pdf]]
