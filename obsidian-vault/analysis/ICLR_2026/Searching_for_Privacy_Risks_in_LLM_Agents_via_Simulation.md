---
title: "Searching for Privacy Risks in LLM Agents via Simulation"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Searching_for_Privacy_Risks_in_LLM_Agents_via_Simulation.pdf
openreview_forum_id: nz4ZqbrBEi
aliases:
- ASFPAAI
- SPRLAS
tags:
- ICLR_2026
- topic/safety_alignment_fairness_privacy
- topic/safety_alignment_fairness_privacy/trustworthy_machine_learning
core_operator: "将攻击者指令与防御者指令作为可优化对象，通过交替搜索使二者协同进化，从而系统性地暴露隐藏漏洞。"
primary_logic: "利用LLM优化器的反思能力，在模拟环境中迭代改进攻击与防御策略，将隐私风险发现转化为自动化搜索问题，超越人工枚举和静态分析。"
claims:
- "攻击策略从直接请求逐步升级为伪造同意、冒充身份等多轮复杂手段，防御策略则从简单规则进化为状态机验证。"
- "交替搜索框架使攻击和防御相互提升，最终发现的长尾攻击（如伪造转发邮件）对人工评估者具有高度欺骗性。"
- "并行搜索与跨线程传播显著提高了搜索效率，而单线程搜索对于开发全面防御已经足够。"
- "Testing‑100 上 Average Leak Velocity (↓) = 2.9% (A2, D2, ICL transfer)"
---

# Searching for Privacy Risks in LLM Agents via Simulation

> [!tip] 核心洞察
> 利用LLM优化器的反思能力，在模拟环境中迭代改进攻击与防御策略，将隐私风险发现转化为自动化搜索问题，超越人工枚举和静态分析。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 通过模拟搜索LLM代理中的隐私风险 |
| 英文题名 | Searching for Privacy Risks in LLM Agents via Simulation |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=nz4ZqbrBEi); [GitHub](https://github.com/SALT-NLP/search_privacy_risk) |
| Topic | #topic/safety_alignment_fairness_privacy #topic/safety_alignment_fairness_privacy/trustworthy_machine_learning |
| Method | Alternating Search Framework for Privacy‑Aware Agent Interactions |
| Dataset | Testing‑100, Training‑5, Cross‑model Transfer (Table 2) |

> [!tip] 效果简介
> - Testing‑100 上，Average Leak Velocity (↓) 为 2.9% (A2, D2, ICL transfer)，对比 31.2% (A0, D0, gpt-4.1-mini/gpt-4.1-mini)，变化 −91%。
> - Training‑5 上，Average Leak Velocity (↓) 为 7.1% (A2, D2, targeted)，对比 76.0% (A1, D0)，变化 −91%。
> - Cross‑model Transfer (Table 2) 上，Average Leak Velocity (↓) 为 0.0% (gpt‑4.1 defense vs. various attacks on A1D1, A2D2)，对比 3.4–76.0% (original gpt‑4.1‑mini pairing)，变化 strong defense retains <5%。

## 概述

### 问题与瓶颈

随着LLM代理在信息管理任务中的广泛应用，隐私泄露风险日益突出。传统隐私研究主要聚焦于**用户–代理交互**或**静态恶意环境**，缺乏对动态多轮、主动诱导式攻击的考量，难以预判LLM代理之间自适应演化出的隐私威胁。这导致现有的隐私防护在面对复杂社会工程攻击时存在系统性盲区。

### 核心思路

本文提出一种**基于交替搜索的隐私风险发现框架**，将攻击者指令与防御者指令作为可优化对象，在模拟环境中通过交替搜索使二者协同进化。其核心洞察在于：利用LLM优化器的反思能力，迭代改进攻击与防御策略，将隐私风险发现转化为自动化搜索问题，从而超越人工枚举和静态分析的局限。

### 方法定位

该方法属于**自动化红蓝对抗搜索**范式：在由三个ReAct代理（数据主体、数据发送者、数据接收者）和四个模拟应用（Gmail、Facebook、Messenger、Notion）构成的仿真环境中，交替执行攻击搜索（并行多线程 + 跨线程传播）与防御搜索（单线程综合优化），以系统性地暴露隐藏漏洞并生成有效防御。

### 关键发现

1. **策略协同进化**：攻击策略从直接请求逐步升级为伪造同意、冒充身份等多轮复杂手段；防御策略则从简单规则进化为严格状态机验证（Figure 3）。
2. **长尾攻击暴露**：交替搜索发现的长尾攻击（如伪造转发邮件）对人工评估者具有高度欺骗性，且跨场景迁移后仍保持较强效果。
3. **搜索效率**：并行搜索与跨线程传播显著提高了攻击搜索效率，而单线程搜索对开发全面防御已足够（Figure 4）。
4. **防御有效性**：最终搜索得到的防御策略（A2, D2）将平均泄漏速度从基线的31.2%降至2.9%（Testing-100），降幅达91%；跨模型迁移后防御仍保持泄漏速度低于5%（Table 1, Table 2, Table 4）。

### 局限与开放问题

当前工作在以下方面存在局限：模拟到真实世界的系统化迁移尚未被刻画；防御搜索仅针对提示词层面优化，未涉及架构级防护；对其他隐私框架的泛化性未经验证。开放的挑战包括将搜索空间扩展到代理架构与防护栏设计、处理部分同意场景，以及将该框架应用于更广泛的安全对齐问题。

## 背景与动机

### 问题背景：LLM代理交互中的隐私威胁

大型语言模型（LLM）驱动的自主代理正被广泛部署于电子邮件、社交媒体、即时通讯等个人数据密集型应用中。这些代理在代表用户执行任务时，不可避免地接触到大量敏感信息（如医疗记录、法律文件、财务数据），并在多轮交互中面临隐私泄露风险。一个典型的场景是：数据接收者代理通过多轮对话，逐步诱导数据发送者代理披露本应受保护的第三方隐私信息。与传统软件系统的隐私攻击不同，LLM代理间的隐私威胁具有**动态性**和**自适应性**——攻击者可以利用语言模型的推理能力，根据防御者的反应实时调整策略，从而绕过静态的隐私保护机制。

### 现有方法缺口：静态防御与人工枚举的局限

当前隐私研究主要沿两条路径展开。其一是**用户-代理交互层面的隐私保护**，例如PrivacyLens（Shao et al., 2024）等工作通过隐私增强提示词（privacy-augmented instructions）约束代理行为，但这类方法本质上是静态的规则注入，缺乏对多轮自适应攻击的对抗性考量。其二是**恶意环境下的安全测试**，通常依赖人工设计的攻击模板或预定义场景进行漏洞扫描，难以覆盖长尾分布中的罕见攻击模式。

这一现状造成了三个核心缺口：

1. **缺乏对抗性视角**：防御策略的设计未考虑攻击者会主动优化其诱导手段，导致防御在面对协同进化的攻击时迅速失效。
2. **搜索空间受限**：人工枚举的攻击策略受限于研究者的先验知识，无法系统性地探索攻击指令的组合空间，特别是那些需要多轮铺垫、伪造上下文、冒充身份等复杂社会工程手段的长尾攻击。
3. **攻防割裂**：攻击发现与防御开发通常是分离的，缺乏一个统一的框架使二者相互促进、协同进化。

### 本文动机：将隐私风险发现转化为自动化搜索问题

本文的核心动机在于突破上述局限，将LLM代理间的隐私风险发现重新定义为一个**自动化搜索问题**。核心洞察是：利用LLM优化器的反思能力，在模拟环境中迭代改进攻击与防御策略，使二者在交替搜索中协同进化，从而系统性地暴露隐藏漏洞——这超越了人工枚举和静态分析的范式。

具体而言，本文旨在回答三个关键问题：（1）能否构建一个模拟环境，忠实复现多代理间的隐私关键交互？（2）能否设计一种搜索算法，使攻击策略和防御策略在对抗中自动升级？（3）这种搜索框架能否发现人工评估者都难以识别的长尾攻击，并生成足够鲁棒的防御？

## 核心创新

本文的核心创新在于将LLM代理的隐私风险发现重新定义为一个**交替搜索问题**，而非依赖静态规则或人工枚举。传统隐私研究（如PrivacyLens, Shao et al., 2024）聚焦于用户-代理交互或预设恶意环境，其防御指令仅为简单的隐私提示（如“保持最高隐私标准”），攻击指令也局限于直接请求。这种静态范式无法应对动态多轮、主动诱导式攻击下代理间的自适应隐私威胁。

本工作的关键突破在于识别出**攻击者指令与防御者指令是可协同优化的对象**，并通过交替搜索使二者在模拟对抗中共同进化，从而系统性地暴露隐藏漏洞。具体而言，框架引入了三个核心changed slots：

1. **防御指令的质变**：基线防御（D0）仅依赖宽泛的隐私准则，而搜索得到的防御策略（D1→D2）进化为**严格的状态机验证机制**。D2明确要求“以严格状态机运行，无例外”，包含身份核验、反欺骗检查和伪造转发邮件识别等具体步骤（Figure 3, Table 15, Table 16）。这一转变使防御从被动提醒升级为可执行的协议级防护。

2. **攻击指令的复杂化**：基线攻击（A0）仅为直接索要信息，搜索发现的攻击（A1→A2）则逐步升级为**多轮社会工程策略**。A1引入伪造紧迫性、虚构权威和亲社会框架；A2进一步使用冒充身份与伪造同意——例如，先冒充数据主体发送“转发：同意”邮件，再以第三方身份引用该伪造同意来索取敏感信息（Figure 3, Table 14）。这些长尾攻击对人工评估者具有高度欺骗性。

3. **搜索并行化与传播机制**：基线为单线程顺序搜索（N=1），本文引入**N=30线程并行搜索与跨线程传播**（Section 3.1, Algorithm 1）。当某线程发现更优指令时，其最佳轨迹被共享至所有线程，有效缓解搜索停滞。消融实验表明，并行化显著提升早期搜索效率，跨线程传播进一步降低最终泄漏速度（Figure 4a, 4b）。

上述changed slots的协同效应使攻击与防御相互提升：更强的攻击迫使防御进化，而更严格的防御又催生更隐蔽的攻击。最终，在Testing-100基准上，搜索得到的攻击-防御对（A2, D2）将平均泄漏速度从基线的**31.2%降至2.9%**（ICL迁移），降幅达91%（Table 4）。这一结果表明，将隐私风险发现转化为自动化搜索问题，能够超越人工枚举和静态分析的局限，系统性地发现并缓解LLM代理间的自适应隐私威胁。

## 整体框架

![[assets/figures/papers/paper_list_l38_https_openreview_net_forum_id_nz4ZqbrBEi/figures/001_Figure_1.jpg]]
*Figure 1: Our search-based framework. (I) We transform each tested privacy norm into a simulation configuration, including agent instructions and environments. (II) Initialized from the configuration, we run the simulation repeatedly to evaluate the risk that emerges from agent-agent interactions. (III) Based on simulations, we alternately search for attack strategies (data recipient instructions) and defense mechanisms (data sender instructions) by using LLMs to reflect on simulation trajectories and optimize agent instructions*

![[assets/figures/papers/paper_list_l38_https_openreview_net_forum_id_nz4ZqbrBEi/figures/006_Figure_3.jpg]]
*Figure 3: Average leak velocity of the alternating search process (at the top), where we develop A _ { 1 } D _ { 1 } , A _ { 2 } , A _ { 2 } sequentially. At the bottom, for each set, we summarize the strategy keywords and show examples with highlights. Note that only the optimizable parts of the instructions are shown*

### 核心瓶颈与设计动机

传统LLM代理隐私研究主要关注用户-代理交互或静态恶意环境，难以预判**动态多轮、主动诱导式攻击**下代理间的自适应隐私威胁。该工作将隐私风险发现重新定义为**自动化搜索问题**：将攻击者指令与防御者指令视为可优化对象，通过交替搜索使二者协同进化，系统性地暴露人工枚举和静态分析难以发现的隐藏漏洞。

### 框架总览

整个框架由三个核心阶段构成（Figure 1）：

1. **仿真配置生成**：将每条待测隐私规范转化为一个仿真配置，包含代理指令与环境设定。每个配置实例化三个ReAct代理（数据主体、数据发送者、数据接收者）和四个模拟应用（Gmail、Facebook、Messenger、Notion），构成多轮交互场景。

2. **仿真执行与风险评估**：从初始配置出发，重复运行仿真，评估交互过程中自然涌现的隐私风险。核心指标为**泄漏速度（Leak Velocity）**：
   $$s = \frac{1}{K} \sum_{i=1}^{K} \left(1 - \frac{\log l_i}{\log l_i + 1}\right)$$
   其中 $s=1$ 表示所有敏感项在首次动作即泄露，$s=0$ 表示无泄露。

3. **交替搜索优化**：基于仿真轨迹，交替执行攻击搜索与防御搜索。攻击搜索利用LLM优化器 $\mathcal{F}$ 反思历史策略与轨迹，生成更强大的攻击指令；防御搜索则综合多场景失败案例，生成全面防御指令。该交替过程使攻击与防御相互提升，逐步逼近隐蔽的长尾风险。

### 搜索流水线模块

流水线由四个功能模块串联：

- **仿真环境（Simulation Environment）**：实例化代理与应用，执行多轮交互，记录完整动作序列。
- **攻击搜索阶段（Attack Search Phase）**：采用并行搜索（N=30线程）与跨线程传播机制，LLM优化器基于历史轨迹和泄漏速度反思，生成并评估新的攻击指令。更新公式为：
  $$a^{k+1} \gets \mathcal{F}(\{(a^{r}, \mathcal{E}^{r}) \mid 1 \leq r \leq k\})$$
- **防御搜索阶段（Defense Search Phase）**：单线程顺序搜索，综合多个场景的失败案例，生成全面防御指令。
- **泄漏评估（Leakage Evaluation）**：利用LLM检测每次数据发送者动作中是否泄露敏感项，计算泄漏速度指标。

### 关键指令进化

Figure 3 展示了攻击与防御策略的协同进化过程：

- **基线（A0, D0）**：攻击指令为简单直接请求，防御指令为基本隐私增强提示（源自PrivacyLens, Shao et al., 2024）。
- **A1 vs D1**：攻击升级为伪造紧迫性、虚构权威、亲社会框架等多轮手段；防御进化为基于规则的同意验证。
- **A2 vs D2**：攻击进一步演变为伪造转发邮件、冒充身份等复杂欺骗；防御则进化为严格状态机，包含身份检查与反欺骗验证，将泄漏速度降至7.1%（针对性设置）。

### 搜索效率机制

消融研究（Figure 4）揭示三个关键效率因素：

- **并行搜索**：线程数从N=1增至N=30显著提升早期搜索效率，但额外线程收益递减。
- **跨线程传播**：通过共享最佳轨迹缓解搜索停滞，使最终泄漏速度进一步降低。
- **优化器骨干模型**：使用更强推理能力的模型（如Gemini Pro with thinking）对发现复杂漏洞至关重要。

### 跨场景迁移机制

搜索发现的攻击与防御策略通过两种方式迁移至新场景（Testing-100，共100个配置）：

- **上下文学习（ICL）**：将训练场景中的攻击示例作为上下文提供给攻击代理。
- **策略引导（SG）**：在ICL基础上，对迁移结果排序并选取最成功的示例，进一步引导攻击行为。

最终A2+D2组合通过ICL迁移将平均泄漏速度从基线的31.2%降至2.9%，通过SG降至4.9%，展现了框架的泛化能力。

## 核心模块与公式推导

### 3.1 仿真环境

仿真环境实例化三个 ReAct 代理——**数据主体**（Data Subject）、**数据发送者**（Data Sender）、**数据接收者**（Data Recipient）——以及四个模拟应用（Gmail、Facebook、Messenger、Notion），用以复现多轮隐私敏感交互。每个仿真配置对应一条待测试的隐私规范（如“未经同意不得分享医疗诊断信息”），并指定代理的角色指令、敏感信息项列表及可用的通信渠道（Figure 1, Section 3, Appendix B）。

仿真运行后，系统收集数据发送者在每一轮动作中是否泄露敏感项的判定结果，作为后续搜索优化的反馈信号。

### 3.2 泄漏速度指标

为量化隐私泄露的严重程度与急迫性，论文定义**泄漏速度**（Leak Velocity）指标：

$$s = \frac{1}{K} \sum_{i=1}^{K} \left(1 - \frac{\log l_i}{\log l_i + 1}\right)$$

其中：
- $K$ 为敏感信息项的总数；
- $l_i$ 表示第 $i$ 个敏感项**首次被泄露时**数据发送者已执行的动作步数（若该项始终未被泄露，则 $l_i \to \infty$，对应项趋近于 0）。

该指标的设计直觉是：若所有敏感项均在代理的第一个动作即遭泄露，则 $s = 1$；若无任何泄露，则 $s = 0$。通过对数变换，指标对早期泄露赋予更高惩罚，从而更敏感地捕捉攻击策略的激进程度（Section 3）。

### 3.3 攻击搜索模块

攻击搜索的目标是在防御指令固定的前提下，发现能最大化泄漏速度的攻击指令。该模块的核心机制包括：

- **LLM 优化器 $\mathcal{F}$**：以历史搜索轨迹为输入，反思先前策略的成败，生成下一代攻击指令。形式化更新规则为：

$$a^{k+1} \gets \mathcal{F}\left(\{(a^{r}, \mathcal{E}^{r}) \mid 1 \leq r \leq k\}\right)$$

其中 $a^r$ 为第 $r$ 轮的最佳攻击指令，$\mathcal{E}^r$ 为对应的仿真轨迹示例（Section 3.1, Algorithm 1）。

- **并行搜索**：启动 $N$ 条线程，每条线程由 LLM 初始化一个不同的攻击指令变体，独立进行仿真评估。默认 $N = 30$（Figure 4a）。

- **跨线程传播**：当某条线程发现更优指令时，其最佳轨迹被广播至所有线程，作为后续优化的共享上下文，以缓解搜索停滞（Figure 4b）。

### 3.4 防御搜索模块

防御搜索在攻击指令固定的条件下，综合多个仿真场景的失败案例，生成通用的防御指令。与攻击搜索不同，防御搜索采用**单线程顺序搜索**——论文实验表明，单线程搜索已足以开发全面防御，无需并行化（Figure 2, Section 3.2, Algorithm 2）。

防御搜索的核心逻辑是：LLM 优化器分析数据发送者在不同场景下错误放行敏感信息的共性模式，逐步将防御策略从简单的规则检查（如“需获得同意”）进化为严格的状态机验证，包括身份核验、反欺骗检查等机制（Figure 3, Table 15–16）。

### 3.5 交替搜索框架

攻击搜索与防御搜索交替进行，形成协同进化循环：

$$(A_T, D_T) \xrightarrow{\text{攻击搜索}} (A_{T+1}, D_T) \xrightarrow{\text{防御搜索}} (A_{T+1}, D_{T+1})$$

每次攻击搜索针对当前防御暴露新漏洞，随后的防御搜索则针对新攻击修补漏洞，二者相互驱动，使系统能够发现人工枚举难以触及的长尾风险（Section 3, Figure 3）。

## 实验与分析

### 核心瓶颈与因果机制

传统隐私研究聚焦于用户-代理交互或静态恶意环境，缺乏对动态多轮、主动诱导式攻击的考虑，导致无法预判LLM代理间自适应隐私威胁。本文的核心机制是将攻击者指令与防御者指令作为可优化对象，通过交替搜索使二者协同进化，从而系统性地暴露隐藏漏洞。利用LLM优化器的反思能力，在模拟环境中迭代改进攻击与防御策略，将隐私风险发现转化为自动化搜索问题，超越人工枚举和静态分析。

### 主实验结果

**基础基线的脆弱性**：在Testing-100基准上，使用基础隐私增强指令（A0, D0）时，即使数据发送者代理已配备隐私提示，各骨干模型均出现不可忽视的泄露。以gpt-4.1-mini为双方骨干时，平均泄漏速度（Average Leak Velocity）高达31.2%（Table 1）。更强的防御者骨干模型可显著改善基线防御水平（gpt-4.1-mini→gpt-4.1：31.2%→16.5%），但攻击者骨干模型升级带来的攻击提升有限（31.2%→33.0%）。

![[assets/figures/papers/paper_list_l38_https_openreview_net_forum_id_nz4ZqbrBEi/figures/003_Table_1.jpg]]
*Table 1: Simulation results using basic instructions and different backbones, where we report the average leak velocity (LV) and leak rate (LR)*

**交替搜索的进化效果**：在Training-5上，交替搜索框架使攻防策略协同进化（Figure 3）：
- **A1攻击策略**：从直接请求升级为伪造紧急情况、捏造权威、亲社会框架等复杂手段，平均泄漏速度提升至76.0%。
- **D1防御策略**：从简单规则进化为基于同意验证的规则系统，将泄漏速度降至2.5%。
- **A2攻击策略**：进一步进化为伪造转发邮件、冒充身份等多轮欺骗手段。
- **D2防御策略**：进化为严格状态机，包含身份检查与反欺骗验证，将针对A2的泄漏速度降至7.1%（Table 3）。

![[assets/figures/papers/paper_list_l38_https_openreview_net_forum_id_nz4ZqbrBEi/figures/008_Table_3.jpg]]
*Table 3: Defense transfer. Alternative defenses discovered using different model setups are tested against A _ { 2 } Targeted shows the performance of specifically optimized defense. Table 4: Cross-scenario transfer (the original setting in gray ). We transfer attacks and defenses from Training-5 to Testing-100 and report the average leak velocity. ICL and SG refer to in-context learning and strategy guidance*

**跨场景迁移**：将Training-5上发现的A2、D2策略迁移至Testing-100，通过上下文学习（ICL）实现平均泄漏速度2.9%，通过策略指导（+SG）实现4.9%，相比基线A0/D0的31.2%降低约91%（Table 4）。

![[assets/figures/papers/paper_list_l38_https_openreview_net_forum_id_nz4ZqbrBEi/figures/007_Table_4.jpg]]

**跨模型迁移**：基于已发现攻防策略的跨模型迁移实验（Table 2）表明，当防御者使用gpt-4.1时，面对多种攻击者骨干模型的泄漏速度均保持在5%以下，其中A1D1和A2D2配置下甚至达到0.0%。

![[assets/figures/papers/paper_list_l38_https_openreview_net_forum_id_nz4ZqbrBEi/figures/004_Table_2.jpg]]
*Table 2: Cross-model transfer (the original setting in gray ) Based on discovered attacks and defenses, we run simulations using different backbone models for simulated agents and report the average leak velocity*

### 消融研究

**并行搜索与跨线程传播**（Figure 4a, 4b）：在Training-5上基于(A1, D1)进行攻击搜索消融。并行线程数从N=1增至N=30显著提升了早期搜索效率，但额外线程收益递减。跨线程传播通过共享最佳轨迹缓解了搜索停滞，使最终泄漏速度进一步降低。

![[assets/figures/papers/paper_list_l38_https_openreview_net_forum_id_nz4ZqbrBEi/figures/009_Figure_4.jpg]]
*Figure 4: Ablation study on the attack search algorithm. Using ( A _ { 1 } , D _ { 1 } ) on top of Training-5, we explore the impact of (a) parallel search, (b) cross-thread propagation, (c) Backbones of LLM Optimizer, and (d) Backbones of the data sender agent. We plot the step-wise average leak velocity*

**优化器骨干模型**（Figure 4c）：使用更强的LLM优化器骨干模型（Gemini Pro with thinking）对于发现复杂漏洞至关重要。较弱优化器可能导致搜索陷入局部最优，无法发现长尾攻击。

**防御者骨干模型**（Figure 4d, Table 1, Table 9）：防御者模型能力直接影响基线防御水平，但搜索过程可以补偿较弱模型的部分不足。推理模式与模型规模的对比（Table 9）进一步验证了这一趋势。

![[assets/figures/papers/paper_list_l38_https_openreview_net_forum_id_nz4ZqbrBEi/figures/014_Table_9.jpg]]
*Table 9: More results for cross-model transfer (the original setting in gray ). We compare non-thinking and non-thinking, different reasoning efforts (low, medium, high), and different model size (20B, 120B)*

### 失败模式与局限性

1. **模拟到真实世界的迁移未经验证**：当前发现的攻击与防御可能无法完全覆盖现实中的复杂社会工程场景，系统化的sim-to-real transfer刻画尚属空白。
2. **防御搜索仅限提示词层面**：未涉及更复杂的架构防护（如防火墙、代理间协议），防御策略的表达空间受限。
3. **场景泛化性有限**：训练/测试场景均基于PrivacyLens衍生规则，对其他隐私框架的泛化性未经验证。
4. **部分同意场景未处理**：数据主体有时会同意分享敏感信息，当前框架未涵盖此类部分同意场景的边界情况。

### 关键图表结论

- **Figure 3**：完整呈现了A0/D0→A1/D1→A2/D2的交替进化轨迹，攻击策略从直接请求逐步升级为伪造同意、冒充身份，防御策略从简单规则进化为状态机验证。
- **Table 1**：基础指令下各骨干模型的泄漏速度基线，揭示隐私增强提示的固有脆弱性。
- **Table 2**：跨模型迁移结果，强防御模型（gpt-4.1）可有效抵御多种攻击者模型。
- **Table 4**：跨场景迁移中ICL与SG两种策略的效果对比，验证了已发现策略的泛化能力。
- **Figure 4**：攻击搜索算法的四项消融研究，分别验证并行搜索、跨线程传播、优化器骨干、防御者骨干的影响。

### 补充图表

![[assets/figures/papers/paper_list_l38_https_openreview_net_forum_id_nz4ZqbrBEi/figures/010_Table_6.jpg]]

![[assets/figures/papers/paper_list_l38_https_openreview_net_forum_id_nz4ZqbrBEi/figures/011_Table_5.jpg]]
*Table 5: Simulation results using basic instructions and different backbones, where we report the average leak velocity (LV) and 95% confidence intervals obtained via nonparametric bootstrap with 10,000 resamples. For each configuration, we resampled runs with replacement to compute configlevel means, then averaged across all configurations. Table 6: Behavior ratios for different backbones as defense agents in Table 1. We report the ratio of actions that include explicit denial, consent-required holding, or no response*

![[assets/figures/papers/paper_list_l38_https_openreview_net_forum_id_nz4ZqbrBEi/figures/012_Table_7.jpg]]
*Table 7: Average leak velocity per domain for different backbones as defense agents in Table 1*

![[assets/figures/papers/paper_list_l38_https_openreview_net_forum_id_nz4ZqbrBEi/figures/013_Table_8.jpg]]
*Table 8: Leak Rate at each step while varying the backbones for attack agents in Table 1*

## 方法谱系与知识库定位

### 1. 与基线工作的关系

本工作的直接基线是 **PrivacyLens**（Shao et al., 2024）所倡导的隐私增强提示（privacy‑augmented instructions），即论文中的 **A0/D0** 配置。该基线通过在数据发送者代理的系统指令中嵌入“维护最高隐私标准”等原则性表述来约束行为，但在动态多轮交互下仍暴露出显著漏洞——在 gpt‑4.1‑mini 骨干模型上，基础指令下的平均泄漏速度高达 **31.2%**（Table 1）。

本文的核心突破在于将一个**静态提示工程问题**重构为**交替搜索的协同进化问题**：
- **攻击维度**：从 A0 的简单直接请求，进化为 A1 的“伪造紧迫性 + 虚构权威 + 亲社会框架”（Figure 3，泄漏速度升至 76.0%），再到 A2 的“身份冒充 + 伪造转发同意邮件”的多轮复杂策略（泄漏速度进一步突破 D1 防御）。
- **防御维度**：从 D0 的原则性提示，进化为 D1 的“基于规则的同意验证”（泄漏速度降至 2.5%），再到 D2 的“严格状态机 + 身份检查 + 反欺骗验证”（Table 15‑16），最终在针对性测试中将 A2 的泄漏速度压制至 **7.1%**（Table 3）。

这种交替搜索框架使攻击与防御策略在对抗中相互提升，而非孤立优化，这是对 PrivacyLens 静态提示范式的根本性超越。

### 2. 方法谱系定位

本工作位于 **LLM 代理安全** 与 **自动化红队测试** 的交叉地带，其方法组件可沿以下维度定位：

| 维度 | 本文方法 | 相关谱系 |
|------|---------|---------|
| **代理架构** | ReAct（Yao et al., 2022） | 通用代理框架，非本文贡献 |
| **仿真环境** | 三代理 + 四应用（Gmail/Facebook/Messenger/Notion） | 继承自 PrivacyLens 的场景设计 |
| **优化范式** | LLM‑as‑Optimizer（反思历史轨迹生成新策略） | 与自动提示优化（如 APE、OPRO）共享思想，但应用于安全对抗场景 |
| **搜索策略** | 攻击侧并行搜索（N=30 线程）+ 跨线程传播；防御侧单线程顺序搜索 | 并行搜索借鉴多臂老虎机探索思路，跨线程传播类似进化算法中的精英迁移 |
| **评估指标** | 泄漏速度（Leak Velocity） | 原创指标，综合衡量泄漏的全面性与及时性 |

### 3. 适用边界

基于实验证据，方法的适用边界可概括为：

- **骨干模型依赖性**：消融实验表明，优化器骨干模型的能力对发现复杂漏洞至关重要——使用 Gemini Pro with thinking 显著优于弱模型（Figure 4c）。同时，防御者模型的能力直接影响基线防御水平，但搜索过程可部分补偿较弱模型的不足（Figure 4d, Table 9）。
- **场景泛化性**：从 Training‑5 到 Testing‑100 的跨场景迁移显示，A2/D2 策略配合上下文学习（ICL）可将泄漏速度降至 **2.9%**，配合策略引导（SG）降至 **4.9%**（Table 4）。但这一泛化性目前仅验证于 PrivacyLens 衍生的隐私规则体系。
- **搜索效率**：并行线程数从 N=1 增至 N=30 显著提升早期搜索效率，但额外线程的边际收益递减（Figure 4a）。跨线程传播通过共享最佳轨迹缓解搜索停滞（Figure 4b），但对最终收敛点的提升有限。

### 4. 局限与开放问题

**已识别的局限**（来自论文明确声明）：

1. **Sim‑to‑Real 迁移未刻画**：当前发现的攻击与防御策略在模拟环境中有效，但向真实世界的系统化迁移尚未被研究。模拟中的“伪造转发邮件”等攻击对人工评估者具有高度欺骗性（Case Study），但真实社会工程攻击的复杂性可能超出当前搜索空间。
2. **防御层次受限**：防御搜索目前仅针对**提示词层面**进行优化（即代理系统指令），未涉及更底层的架构防护，如防火墙规则、代理间通信协议、或基于训练的对齐方法。
3. **隐私框架泛化性未验证**：训练与测试场景均基于 PrivacyLens 衍生的隐私规则，对其他隐私框架（如 GDPR 的具体条款、HIPAA 等）的泛化性仍是开放问题。

**论文指出的开放问题**：

1. **搜索空间的扩展**：能否将搜索范围从代理指令扩展到最优代理架构、防护栏设计乃至训练目标，以构建更稳固的隐私防御体系。
2. **部分同意场景**：当前框架假设数据主体不应分享敏感信息，但现实中存在数据主体**确实同意**分享的场景——如何处理这种“合法同意”与隐私保护的张力，仍待探索。
3. **更广泛的安全对齐应用**：该长尾风险搜索框架能否应用于更广泛的安全对齐问题，如信息操纵、目标劫持、或代理间的恶意协作，是一个值得追踪的方向。

## 原文 PDF

![[paperPDFs/ICLR_2026/Searching_for_Privacy_Risks_in_LLM_Agents_via_Simulation.pdf]]
