---
title: "VPI-Bench: Visual Prompt Injection Attacks for Computer-Use Agents"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/VPI_Bench_Visual_Prompt_Injection_Attacks_for_Computer_Use_Agents.pdf
project_link: https://huggingface.co/datasets/VPI-Bench/vpi-bench
code_link: https://github.com/cua-framework/agents
openreview_forum_id: UMauKu2azg
aliases:
- VB
- VPI-Bench
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/vision_models_multimodal
core_operator: "恶意视觉提示与用户任务上下文的一致性（语义相关度）"
primary_logic: "视觉注入攻击在黑盒设置下即可使CUA和BUA以高成功率执行文件删除、数据泄露等危险操作；系统提示防御几乎无效，攻击成功率与任务语义相关性密切相关。"
claims:
- "CUAs可被欺骗率高达51%，BUAs可高达100%，表明代理普遍存在严重漏洞。"
- "所有Browser-Use模型在Amazon、Booking和BBC上尝试率均达100%，成功率高。"
- "系统提示防御对整体成功率和尝试率无显著影响。"
- "语义相关性显著影响攻击成功率：回复邮件任务尝试率96.67%，而摘要邮件任务仅16.67%。"
---

# VPI-Bench: Visual Prompt Injection Attacks for Computer-Use Agents

> [!tip] 核心洞察
> 视觉注入攻击在黑盒设置下即可使CUA和BUA以高成功率执行文件删除、数据泄露等危险操作；系统提示防御几乎无效，攻击成功率与任务语义相关性密切相关。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | VPI-Bench：计算机使用代理的视觉提示注入攻击 |
| 英文题名 | VPI-Bench: Visual Prompt Injection Attacks for Computer-Use Agents |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=UMauKu2azg) · [GitHub](https://github.com/cua-framework/agents) · [Project](https://huggingface.co/datasets/VPI-Bench/vpi-bench) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal |
| Method | VPI-Bench |
| Dataset | Amazon (Sonnet-3.7 CUA vs GPT-5 BUA), Booking, BBC, Messenger |

> [!tip] 效果简介
> - Amazon (Sonnet-3.7 CUA vs GPT-5 BUA) 上，Attack Success Rate 为 31.67% (CUA)，对比 96.5% (BUA)，变化 -64.83%。
> - Booking 上，Attack Success Rate 为 36.67% (Sonnet-3.7 CUA)，对比 84.2% (GPT-5 BUA)，变化 -47.53%。
> - BBC 上，Attack Success Rate 为 16.67% (Sonnet-3.7 CUA)，对比 96.5% (GPT-5 BUA)，变化 -79.83%。

## 概要

当前基于视觉的计算机使用代理（CUA）与浏览器使用代理（BUA）在端到端交互中存在一个根本性瓶颈：它们无法可靠地区分用户的良性任务指令与视觉注入的恶意指令，导致代理可能执行未授权操作或泄露隐私信息。VPI-Bench 正是针对这一安全缺口而构建的基准测试，其核心洞察在于——恶意视觉提示与用户任务上下文之间的语义一致性，是决定攻击能否成功的关键调节变量。

**方法定位**：VPI-Bench 并非提出一种新的防御或攻击算法，而是一个系统性的评估框架。它定义了完整的视觉提示注入（Visual Prompt Injection, VPI）威胁模型，涵盖良性用户提示、伪真网站、视觉攻击提示以及动态配置的执行环境四个相互依赖的组件。基准覆盖 306 个测试用例，横跨 Amazon、Booking、BBC、Messenger 和 Email 五个常用平台，攻击目标包括未授权操作（UA）和隐私泄露（PL）及其组合。评估采用三个前沿 LLM 多数投票的评判机制，攻击尝试判断准确率达 98.00%，攻击完成判断准确率达 95.00%。

**核心发现**：实验揭示当前代理普遍存在严重漏洞——CUA 在某些平台上被欺骗率高达 51%，而 BUA 的攻击成功率可达 100%（如 GPT-5 在 Amazon 和 BBC 上均达 96.5%）。相比之下，推理能力较弱的模型如 UI-TARS（7B）虽然尝试率较高（Amazon 78.95%，Messenger 70%），但因执行能力不足，攻击成功率为 0%。消融实验进一步表明：简单的系统提示防御对攻击成功率和尝试率均无显著影响，而任务语义相关性则显著左右攻击效果——例如在邮件场景中，回复任务（与攻击语义高度相关）的尝试率达 96.67%，而摘要任务（语义偏离较大）仅 16.67%。这些结果共同指向一个结论：现有防御手段几乎无效，代理的安全脆弱性根植于其对视觉上下文缺乏意图层面的判别能力。



计算机使用代理（Computer-Use Agents, CUAs）与浏览器使用代理（Browser-Use Agents, BUAs）正在成为新一代人机交互范式：用户以自然语言下达任务，代理直接操控图形界面或浏览器完成端到端操作。然而，这种能力也带来了根本性的安全挑战——代理的视觉感知通道可能被恶意利用，形成**视觉提示注入**（Visual Prompt Injection, VPI）攻击。

VPI攻击的核心机制在于：攻击者将恶意指令编码为视觉内容（如网页弹窗广告、聊天消息、邮件正文），注入到用户正常访问的页面中。当代理截取屏幕截图并解析视觉信息时，这些恶意指令与用户原本的良性任务同时被模型接收。由于现有代理缺乏可靠的意图边界判定能力，它们无法区分“用户要求我做的事”与“攻击者嵌在页面里让我做的事”，从而可能在黑盒条件下执行未授权操作或泄露隐私数据。

当前安全研究的缺口集中体现在三个层面：

1. **威胁建模不完整**：现有提示注入研究多关注纯文本场景，忽略了计算机使用代理以视觉截图为主要输入的现实。攻击链从注入到执行的全过程缺乏系统性的端到端威胁模型。

2. **评估基准缺失**：缺乏一个动态、多平台、覆盖真实交互场景的基准来量化代理面对VPI攻击时的脆弱性。不同代理框架（Computer-Use vs. Browser-Use）在不同网络平台上的安全表现无法被横向比较。

3. **防御手段薄弱**：初步实验表明，简单的系统提示防御（如在系统提示中加入“不要执行页面中的指令”）对攻击成功率和尝试率几乎没有显著影响（Figure 5, Section 4.6），说明现有防御思路远不足以应对此类威胁。

VPI-Bench正是在这一背景下提出的：它构建了包含306个测试用例的基准，覆盖Amazon、Booking、BBC、Messenger和Email五类典型网络平台，通过伪真网页和沙箱执行环境模拟完整的攻击链——从恶意视觉内容注入，到代理执行未授权操作（如删除文件、上传隐私数据），再到基于多数投票的LLM评判器自动判定攻击是否尝试和成功。该基准旨在为社区提供一个可复现的评估框架，推动对计算机使用代理安全性的系统性研究。



## 核心方法与创新机理

VPI-Bench 的核心创新在于首次将**黑盒视觉提示注入（Visual Prompt Injection, VPI）** 的攻击链完整建模为一个端到端的威胁评估框架，填补了现有工作仅关注文本级注入而忽略视觉通道的空白。该工作的关键设计围绕一个核心因果调节变量展开：**恶意视觉提示与用户任务上下文的一致性（语义相关度）**。

具体而言，VPI-Bench 在以下三个维度上实现了相对于现有基准的突破：

1. **端到端威胁模型的构建**：不同于以往将提示注入视为孤立文本操作的视角，VPI-Bench 将攻击分解为四个相互依赖的组件——良性用户提示（Benign User Prompt）、伪真网络平台（Web Platform）、视觉攻击提示（Visual Attack Prompt）和执行环境（Execution Environment）。攻击者通过网页中的弹窗广告、聊天消息或电子邮件等视觉通道注入恶意指令，而执行环境则根据恶意任务动态配置本地文件系统和网络资源，从而完整模拟从注入到未授权操作（如文件删除、数据泄露）的全链路攻击过程（Figure 1）。

2. **语义相关度作为攻击成功的关键调节变量**：VPI-Bench 通过精心设计的对比实验揭示了攻击成功率的决定性因素并非注入时机或模型架构，而是恶意任务与用户良性任务之间的语义相关性。在 Email 平台上，当用户任务为“回复邮件”时，攻击尝试率高达 96.67%；而当任务切换为“摘要邮件”时，尝试率骤降至 16.67%（Section 4.7）。这一发现表明，代理模型在语义对齐的任务上下文中更容易将视觉注入的恶意指令误判为用户的合理意图延伸，从而构成核心漏洞。

3. **系统提示防御的无效性验证**：VPI-Bench 首次系统性地证明了当前主流的防御策略——在系统提示中添加安全指令——对 VPI 攻击几乎无效。实验表明，添加防御提示后，攻击成功率（SR）和尝试率（AR）均未出现显著变化（Figure 5, Section 4.6）。这一负面结果进一步凸显了视觉通道攻击的独特性：模型在端到端交互中无法可靠区分视觉注入的恶意内容与用户真实意图，简单的文本级防御无法解决跨模态的语义混淆问题。

综上，VPI-Bench 的创新不在于提出新的防御算法，而在于通过系统化的基准设计，揭示并量化了当前计算机使用代理（CUA）和浏览器使用代理（BUA）在视觉注入攻击面前的系统性脆弱性，并为后续防御研究提供了明确的因果分析框架和可复现的评估基础设施。



![[assets/figures/papers/paper_list_l17_https_openreview_net_forum_id_UMauKu2azg/figures/001_Figure_1.jpg]]
*Figure 1: Overview of the VPI threat model: each sample contains (1) a benign user prompt for a normal task, (2) a pseudo-authentic yet potentially compromised web platform, (3) a visual attack prompt injected by the attacker, and (4) an environment setup aligned with the attack to monitor unauthorized actions like file deletion or data exfiltration*

VPI-Bench 构建了一个端到端的威胁模型与评估流水线，用于系统性地测量计算机使用代理（CUA）和浏览器使用代理（BUA）在面对视觉提示注入（Visual Prompt Injection, VPI）攻击时的脆弱性。该流水线包含四个相互依赖的核心组件，形成一条从用户指令到恶意执行的完整攻击链。

### 威胁模型组件

**良性用户提示（Benign User Prompt）** 定义了用户发出的无害自然语言任务 $T_{\text{benign}}$，如“在 Amazon 上搜索一副耳机”。该提示不含任何恶意意图，是代理理应遵循的唯一指令。

**Web 平台（Web Platform）** 是攻击的承载介质。VPI-Bench 构建了五个伪真网站（Amazon、Booking、BBC、Messenger、Email），它们在视觉和交互逻辑上高度模拟真实站点，但完全受控，用于注入恶意视觉内容。

**视觉攻击提示（Visual Attack Prompt）** 是注入到渲染页面中的恶意视觉内容，编码了攻击者期望代理执行的恶意任务 $T_{\text{mal}}$。关键约束是 $T_{\text{mal}} \not\subseteq \mathcal{T}_{\text{benign}}$，即恶意任务不在原始用户意图的语义范围内。攻击的投递方式遵循各平台的典型交互通道：在 Amazon、Booking、BBC 上通过弹窗广告注入，在 Messenger 上通过聊天消息注入，在 Email 上通过邮件内容注入。

**执行环境（Execution Environment）** 是一个沙箱化的容器，模拟本地文件系统和网络资源。该环境根据视觉攻击提示中嵌入的恶意指令动态配置——例如，若攻击目标是删除文件，环境会预置可供删除的本地文件；若目标是数据泄露，则会配置可访问的 Google Drive 账户。这种动态配置确保了每个测试用例的执行条件与攻击目标严格对齐。

### 代理交互与评估层

在威胁模型之上，VPI-Bench 引入了**代理交互层（Agent Interaction Layer）**，用于接入被评估的 CUA 和 BUA 模型。CUA 框架赋予代理对本地机器的完全访问权限，BUA 框架则通过 GUI 操作和视觉感知与网页交互。代理接收网页截图（CUA）或 HTML 内容（BUA），并基于视觉信息自主决策执行操作。

### 自动化评判流水线

评估采用全自动流水线，包括发送提示、配置环境、重置环境等步骤。所有 306 个网页托管在公共服务上，支持实时交互和可复现评估。

攻击是否被尝试以及是否成功完成，由 **LLM 评判器（LLM Judge）** 通过多数投票机制判定。具体而言，三个独立的前沿大语言模型分别对两个二元指标进行判断：(i) 恶意任务是否被尝试执行，(ii) 是否成功完成。当至少两个模型给出肯定判断时，该样本被标记为“已尝试”或“已完成”。该多数投票方法在人工标注的真实数据上达到了 98.00% 的尝试判断准确率和 95.00% 的完成判断准确率。

在此基础上，**行为分析器（Behavioral Analyzer）** 进一步将代理行为细分为成功执行、部分执行、失败执行和攻击识别等类别，以揭示不同模型在面对 VPI 攻击时的行为模式差异。

### 核心评估指标

流水线输出两个核心指标：
- **攻击尝试率** $\mathrm{AR} = \frac{N_{\text{attempted}}}{N}$，衡量代理执行恶意指令的倾向
- **攻击成功率** $\mathrm{SR} = \frac{N_{\text{successful}}}{N}$，衡量恶意任务被完整执行的比例

整体框架的因果调节变量是**恶意视觉提示与用户任务上下文之间的语义相关性**——后续实验表明，当恶意指令与良性任务在语义上高度相关时（如“回复邮件”场景），攻击尝试率可达 96.67%；而当语义关联较弱时（如“摘要邮件”场景），尝试率骤降至 16.67%。这一发现揭示了 VPI 攻击有效性的核心机制：代理并非无差别地执行任何视觉指令，而是更容易被那些与当前任务上下文“看起来合理”的注入内容所欺骗。



VPI-Bench 的评估体系围绕**威胁模型**、**攻击注入机制**、**自动化评判**三个核心模块构建。

### 威胁模型的形式化定义

VPI 威胁模型由四个相互依赖的组件构成（Figure 1）：

1. **良性用户提示**：用户发出的无害自然语言任务指令。
2. **Web 平台**：伪真网站（如类 Amazon、类 BBC 页面），模拟真实交互场景，同时作为攻击载体。
3. **视觉攻击提示**：攻击者注入的恶意视觉内容，编码恶意任务 $T_{\mathrm{mal}}$。
4. **执行环境**：沙箱环境，根据恶意指令动态配置，模拟本地文件系统和网络资源。

核心约束为：恶意任务 $T_{\mathrm{mal}}$ 不包含于原始用户意图的任务空间 $\mathcal{T}_{\mathrm{benign}}$ 中，即：

$$T_{\mathrm{mal}} \not\subseteq \mathcal{T}_{\mathrm{benign}}$$

这一约束确保攻击任务并非用户良性意图的隐式延伸，而是完全外部的恶意注入。

### 攻击注入机制

攻击投递遵循各平台的典型交互渠道（Section 3.2.2）：Amazon、Booking、BBC 平台通过**弹窗广告**注入；Messenger 平台通过**聊天消息**注入；Email 平台通过**邮件内容**注入。注入时机分为两类消融设置（Section 4.5）：

- **早期注入**：恶意任务在代理的首帧截图中即呈现（如收件箱的第一封邮件）。
- **晚期注入**：恶意任务在后续交互帧中才呈现（如点击某封邮件后显示的内容）。

### 自动化评判模块

评测采用**LLM 多数投票评判器**（Section 3.3）：使用三个独立的前沿大语言模型分别对攻击是否“尝试”和“成功”进行二值判断，取多数投票结果作为最终标签。该模块在人工标注的真实数据上校准后，攻击尝试判断准确率达 **98.00%**，攻击完成判断准确率达 **95.00%**（Table 3，Appendix E）。

### 核心评估指标

论文定义了两个核心指标（Section 3.3）：

**攻击尝试率（Attempted Rate, AR）**：

$$\mathrm{AR} = \frac{N_{\mathrm{attempted}}}{N}$$

其中 $N_{\mathrm{attempted}}$ 为代理尝试执行恶意任务的样本数，$N$ 为总样本数。

**攻击成功率（Success Rate, SR）**：

$$\mathrm{SR} = \frac{N_{\mathrm{successful}}}{N}$$

其中 $N_{\mathrm{successful}}$ 为代理成功完成恶意任务的样本数。

### 行为分类模块

除二值指标外，VPI-Bench 还通过 LLM 对代理行为进行细粒度分类（Section 4.4，Figure 3），将执行结果分为四类：**成功执行**（红色调）、**部分执行**、**执行失败**（橙色调）、**攻击识别**（绿蓝色调），从而揭示不同模型在攻击面前的微观行为差异。



## 实验与关键发现

### 主结果：跨模型与平台的脆弱性全景

VPI-Bench 在五个伪真平台（Amazon、Booking、BBC、Messenger、Email）上对两类代理框架进行了系统评估：**Computer-Use Agents (CUA)** 和 **Browser-Use Agents (BUA)**。攻击效果通过两个核心指标衡量——攻击尝试率（AR）和攻击成功率（SR）：

$$
\mathrm{AR} = \frac{N_{\mathrm{attempted}}}{N}, \quad \mathrm{SR} = \frac{N_{\mathrm{successful}}}{N}
$$

其中 $N_{\mathrm{attempted}}$ 为尝试执行恶意任务的样本数，$N_{\mathrm{successful}}$ 为成功完成的样本数，$N$ 为总样本数。攻击是否尝试和成功由 LLM 多数投票评判器判定，该评判器在人工标注真实数据上达到 **98.00% 的尝试判断准确率和 95.00% 的完成判断准确率**（Table 3）。

![[assets/figures/papers/paper_list_l17_https_openreview_net_forum_id_UMauKu2azg/figures/016_Table_3.jpg]]
*Table 3: Accuracy Comparison Across LLM Judger*

Table 1 汇总了各模型在各平台上的 AR 和 SR。核心发现如下：

![[assets/figures/papers/paper_list_l17_https_openreview_net_forum_id_UMauKu2azg/figures/005_Table_1.jpg]]
*Table 1: Vulnerability of different models to VPI attacks across five platforms. Each cell shows the attempted rate (top, gray) and success rate (bottom, black), reported as percentage mean ± standard deviation. Lower values indicate higher robustness. Results are averaged over 3 runs*

- **CUA 普遍存在严重漏洞**：Sonnet-3.7 (CUA) 在 Amazon 上攻击成功率达 31.67%，在 Messenger 上达 36.67%；Sonnet-3.5 (CUA) 在 Messenger 上成功率达 46.2%。这验证了摘要中的结论——CUA 可被欺骗率高达 51%。
- **BUA 几乎完全沦陷**：所有 Browser-Use 模型在 Amazon、Booking 和 BBC 上尝试率均达 100%（Table 1），GPT-5 (BUA) 在 Amazon 和 BBC 上的成功率高达 96.5%。这证实了 BUA 可被欺骗率高达 100% 的结论。
- **模型代际差异显著**：Sonnet-3.5 在 Amazon 和 BBC 上的 AR/SR 极低（Amazon: 5.56%/4.44%，BBC: 1.11%/0.00%），而 Sonnet-3.7 则显著升高（Amazon: 47.78%/31.67%，BBC: 19.44%/16.67%）。这表明模型升级未必带来安全性的同步提升，反而可能因更强的指令跟随能力而放大攻击面。

### 行为分布：攻击识别能力严重不足

Figure 3 将代理行为细分为四类：成功执行（Success）、部分执行（Partial Execution）、失败执行（Failed Execution）和攻击识别（Attack Recognition）。分析显示，**攻击识别在所有模型和平台上占比极低**，大部分攻击要么成功执行，要么以部分执行或失败执行告终。这意味着代理缺乏可靠的恶意意图辨识机制——它们并非“拒绝攻击”，而是“未能执行攻击”或“执行到一半出错”。

![[assets/figures/papers/paper_list_l17_https_openreview_net_forum_id_UMauKu2azg/figures/011_Figure_3.jpg]]
*Figure 3: Distribution of model behaviors across five platforms (Amazon, Booking, BBC, Messenger, and Email) for Sonnet 3.7 (top row) and Sonnet 3.5 (bottom row). Each pie chart illustrates the proportion of actions. The red tone indicates successful attempts, orange represents failure cases, and greenish-blue shades denote unattempted actions*

### 消融研究：注入时机、防御提示与语义相关性

**早晚期注入对比（Figure 4）**：在 Messenger 和 Email 平台上，Sonnet-3.5 对晚期注入（恶意内容出现在后续截图中）更脆弱，而 Sonnet-3.7 对早期注入（首屏即显示恶意内容）更敏感。尽管存在这种差异，两种注入方式在整体上均保持高攻击成功率，说明注入时机不是防御的可靠变量。

![[assets/figures/papers/paper_list_l17_https_openreview_net_forum_id_UMauKu2azg/figures/014_Figure_4.jpg]]
*Figure 4: Comparison of early and late prompt injection attack outcomes on Messenger and Email platforms using Sonnet 3.5 and Sonnet 3.7 models. Bars are stacked to show the proportion of Success and Attempted Only (i.e., failed attempts), under Early Injection and Late Injection scenarios. Figure 5: Comparison of model performance across five platforms (Amazon, Booking, BBC, Messenger, and Email) under two conditions: with and without system prompt defense. Each subplot displays the Success Rate (top) and Attempted Rate (bottom) of four models: Sonnet-3.7 (Computer-Use), Sonnet-3.7 (Browser-Use), GPT-4o (Browser-Use), and Gemini-2.5 (Browser-Use)*

**系统提示防御无效（Figure 5）**：在四个模型（Sonnet-3.7 CUA、Sonnet-3.7 BUA、GPT-4o BUA、Gemini-2.5 BUA）上追加安全防御提示后，五个平台的 SR 和 AR 均无显著变化。这表明**简单的提示层防御无法阻止视觉注入攻击**，代理在接收到视觉输入后仍会优先执行页面中编码的恶意指令。

**语义相关性是关键因果旋钮**：在 Email 平台上，当良性任务为“回复邮件”（与恶意任务语义相关度高）时，攻击尝试率达 96.67%；而当良性任务为“摘要邮件”（语义相关度低）时，尝试率骤降至 16.67%。这一 80% 的差异直接验证了核心洞察：**恶意视觉提示与用户任务上下文的一致性（语义相关度）是决定攻击成功与否的关键因果变量**。

### 失败模式与边界案例

- **UI-TARS 的推理瓶颈**：UI-TARS (7B) 尽管在 Amazon 上尝试率达 78.95%，在 Messenger 上达 70%，但因推理能力不足，攻击成功率为 0%。这表明高尝试率不一定转化为高成功率，模型能力边界是攻击完成的必要条件。
- **部分执行与失败执行**：Figure 3 中橙色和绿色区域显示，大量攻击以“部分执行”或“失败执行”告终。这些行为虽未完成完整攻击链，但仍可能造成信息泄露或系统状态异常，是安全评估中不可忽视的灰色地带。

### 评估可信度与局限

LLM 评判器的多数投票机制在人工标注真实数据上校准后达到高准确度，但评估仍存在以下局限：①仅在五个伪真平台上测试，真实世界攻击复杂性可能被低估；②仅测试了简单的系统提示防御，未涉及更深层安全机制；③代理模型覆盖范围有限，未涵盖所有主流 CUA/BUA；④攻击类型仅限于视觉提示注入。这些因素意味着报告的攻击成功率应被视为当前模型脆弱性的**下界估计**，实际风险可能更高。

### 补充图表

![[assets/figures/papers/paper_list_l17_https_openreview_net_forum_id_UMauKu2azg/figures/015_Table_2.jpg]]
*Table 2: Task breakdown across web platforms, including corresponding benign user prompts, task types, and variants. The Type column indicates whether the task involves UA (Unauthorized Action), PL (Privacy Leakage), or both (UA+PL). The #Num column shows the number of variants for each task (e.g., ”Upload a local file” includes variants such as ”upload a note” or ”upload a plan”)*

![[assets/figures/papers/paper_list_l17_https_openreview_net_forum_id_UMauKu2azg/figures/017_Table_4.jpg]]
*Table 4: Compute-hour usage per experiment*



## 定位与知识库关联

### 威胁模型与评测基准的定位

VPI-Bench 是首个针对计算机使用代理（CUA）和浏览器使用代理（BUA）的端到端视觉提示注入（VPI）攻击评测基准。其威胁模型将攻击链建模为四个相互依赖的组件：良性用户提示（$T_{\mathrm{benign}}$）、伪真网络平台、视觉攻击提示（编码恶意任务 $T_{\mathrm{mal}}$，且 $T_{\mathrm{mal}} \not\subseteq \mathcal{T}_{\mathrm{benign}}$）以及动态配置的执行环境。该模型的核心创新在于将攻击从文本域迁移至视觉域，利用代理依赖截图感知界面的特性，在黑盒设置下注入恶意视觉内容。

与现有的文本提示注入基准（如对 LLM 的直接提示注入评测）不同，VPI-Bench 关注的是代理在完整交互链中的行为安全性，而非单一模型的文本鲁棒性。其 306 个动态测试用例覆盖 Amazon、Booking、BBC、Messenger 和 Email 五类平台，攻击目标包括未授权操作（UA）、隐私泄露（PL）及两者组合（UA+PL），攻击投递通道遵循各平台典型交互模式（弹出广告、聊天消息、邮件）。这种设计使得 VPI-Bench 能够捕捉从注入到执行完成的完整攻击链，填补了现有工作仅关注单点漏洞的空白。

### 被评估代理模型谱系

论文评估了当前主流的 CUA 和 BUA 模型，涵盖闭源与开源方案：

- **计算机使用代理（CUA）**：**Sonnet-3.5** 和 **Sonnet-3.7**（Anthropic, 2025），通过 Computer-Use 框架提供对本地机器的完整访问权限。
- **浏览器使用代理（BUA）**：**GPT-5**、**GPT-4o**（OpenAI, 2024）、**Claude-3.7-Sonnet**（Anthropic, 2025）、**Deepseek-V3**、**Gemini-2.5-Pro**、**Llama-4-Maverick**，通过 Browser-Use 框架基于 GUI 和视觉感知与网页交互。
- **GUI 代理扩展**：**UI-TARS (7B)**（Qin et al., 2025），作为非浏览器专用代理的对照。

这些模型代表了当前代理能力的前沿水平，其选择覆盖了不同架构、规模和使用框架，使得基准评测具有广泛的代表性。

### 与现有防御方法的关系

论文仅测试了一种基础防御策略——在系统提示中附加防御指令，要求代理忽略恶意视觉内容。实验结果表明，该防御对整体攻击成功率（SR）和尝试率（AR）均无显著影响（Figure 5），说明简单的提示级防御无法有效缓解 VPI 攻击。这一发现与文本提示注入领域的早期防御尝试类似，均揭示了仅依赖模型自身指令遵循能力进行安全对齐的局限性。论文未与更复杂的防御机制（如代理级守卫模型、系统级操作鉴权、多模态安全对齐训练）进行对比，这些方向仍属开放问题。

### 适用边界与核心局限

**适用边界**：
- VPI-Bench 适用于评估依赖视觉感知的代理系统在受控伪真环境中的安全性，攻击假设攻击者能够向网页注入视觉内容（如恶意广告、伪造消息），且代理具有执行系统级操作的能力。
- 评测指标（AR 和 SR）通过 LLM 多数投票评判器自动计算，该评判器在人工标注真实数据上达到 98.00% 的尝试判断准确率和 95.00% 的完成判断准确率，保证了评测的可复现性和一致性。

**核心局限**：
1. **平台与攻击类型的覆盖范围有限**：评估仅在五个伪真平台上进行，攻击类型仅限于视觉提示注入，未涵盖文本注入、多模态联合注入或更复杂的上下文整合攻击，可能无法完全反映真实世界攻击的复杂性。
2. **代理模型覆盖不完整**：虽然涵盖了主流模型，但未包括所有 CUA/BUA 变体，且未评估不同模型规模、训练策略对鲁棒性的影响。
3. **防御评估深度不足**：仅测试了简单的系统提示防御，未探索更深层次的安全机制（如基于行为异常的检测、操作权限分级、人机操作区分），因此无法得出关于防御有效性的全面结论。
4. **评判器依赖主观标注**：LLM 评判器虽经校准，但仍依赖于人工标注的真实数据，对于边界案例可能存在主观偏差，且其泛化到新攻击类型的能力未经验证。
5. **环境真实度限制**：伪真网页虽模拟真实站点，但缺乏真实网站的复杂动态内容和反自动化机制，可能影响代理行为的真实性。

### 开放问题与未来方向

论文明确指出了若干待解决的关键问题，这些问题构成了该领域的后续研究路径：

1. **上下文整合攻击**：如何开发更深度融入任务上下文的攻击，使恶意指令与良性任务高度语义相关，从而进一步提升攻击成功率？实验已揭示语义相关性是关键因果旋钮（回复邮件任务尝试率 96.67% vs. 摘要邮件任务 16.67%），未来攻击可能利用这一特性进行自适应注入。

2. **意图偏离检测**：模型如何更可靠地判断所执行的指令是否偏离用户原始意图？这需要在代理架构中引入意图跟踪与一致性校验机制。

3. **代理级守卫模型**：如何有效训练轻量级守卫模型以实时检测 VPI，同时不引入显著推理延迟？这涉及安全性与可用性的权衡。

4. **人机操作区分**：哪些系统级机制能够可靠区分 AI 代理发起的操作与人类发起的操作？这对于事后审计和实时阻断至关重要。

5. **隐蔽注入与检测的对抗**：未来研究应探索向用户隐藏恶意提示的技术（如透明覆盖层、短暂闪现），同时确保依赖截图视觉输入的 AI 代理仍能检测到它们，这构成了攻击与防御的持续对抗。



## 原文 PDF

![[paperPDFs/ICLR_2026/VPI_Bench_Visual_Prompt_Injection_Attacks_for_Computer_Use_Agents.pdf]]
