---
title: "World-In-World: World Models in a Closed-Loop World"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/World_In_World_World_Models_in_a_Closed_Loop_World.pdf
project_link: https://world-in-world.github.io/
code_link: null
openreview_forum_id: yDmb7xAfeb
aliases:
- WWA
- World-In-World
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "世界模型对行动条件的响应精度（可控制性）"
primary_logic: "世界模型在具身任务中的效用取决于其对行动条件的精确响应（可控制性），而非生成图像的视觉质量。"
claims:
- "高视觉质量并不一定转化为强任务成功率。"
- "细粒度可控制性比视觉质量对任务成功更重要。"
- "扩展后训练比升级预训练视频生成器更有效。"
- "Active Recognition (AR) 上 SR% = 64.79 (Runway Gen4)"
---

# World-In-World: World Models in a Closed-Loop World

> [!tip] 核心洞察
> 世界模型在具身任务中的效用取决于其对行动条件的精确响应（可控制性），而非生成图像的视觉质量。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 闭环世界中的世界模型：基准测试与分析 |
| 英文题名 | World-In-World: World Models in a Closed-Loop World |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=yDmb7xAfeb) · [Project](https://world-in-world.github.io/) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | World-In-World（统一闭环在线规划与标准化动作API） |
| Dataset | Active Recognition (AR), Image-Goal Navigation (ImageNav), Active Embodied Question Answering (A-EQA), Robotic Manipulation |

> [!tip] 效果简介
> - Active Recognition (AR) 上，SR% 为 64.79 (Runway Gen4)，对比 50.27 (VLM w/o WM)，变化 +14.52。
> - Image-Goal Navigation (ImageNav) 上，SR% 为 46.53 (Wan2.2† A14B)，对比 35.42 (VLM w/o WM)，变化 +11.11。
> - Active Embodied Question Answering (A-EQA) 上，Ans. Score 为 48.2 (Wan2.1†)，对比 45.7 (VLM w/o WM)，变化 +2.5。

## 概要

**瓶颈**：当前生成式世界模型普遍以开放环视觉质量为优化目标，但缺乏对行动条件的精确响应能力，导致其生成的“未来”在具身决策任务中无法被有效利用。这一可控制性鸿沟是阻碍世界模型从图像/视频生成器进化为具身智能体“内部模拟器”的关键瓶颈。

**核心洞见**：世界模型在具身任务中的效用取决于其对行动条件的精确响应（即可控制性），而非生成图像的视觉质量。高视觉质量并不自动转化为高任务成功率（Figure 2）。

**方法定位**：本文提出 **World-In-World** 框架，包含三个协同组件：
- **统一闭环在线规划策略**：通过“提议—模拟—修订”循环，将世界模型嵌入决策过程，使智能体在行动前推演候选计划的未来结果并择优执行。
- **标准化动作API**：将异构动作空间（文本指令、相机轨迹、低层控制）统一映射为世界模型的控制输入，实现跨模型、跨任务的即插即用。
- **轻量后训练协议**：利用少量行动–观察数据对预训练视频生成器进行领域适配，显著提升其可控制性，成本远低于全量重训练（Table 10）。

**方法谱系与知识库定位**：World-In-World 区别于以视觉质量为导向的图像/视频生成世界模型（如 **PathDreamer** [Koh et al., 2021]、**SE3DS** [Koh et al., 2023]、**NWM** [Bar et al., 2025]）和零样本视频生成器（如 **SVD** [Blattmann et al., 2023]、**Wan2.1/2.2** [Wan et al., 2025]、**Cosmos-Predict2** [Agarwal et al., 2025]），其核心创新在于将评估范式从开放环视觉质量转向闭环任务成功，并通过后训练和统一动作接口弥合“生成”与“控制”之间的鸿沟。

**主要结果**：在主动识别（AR）、图像目标导航（ImageNav）、主动具身问答（A-EQA）和机器人操纵四项任务上，引入视觉世界模型一致提升了基础策略的性能。例如，AR 任务中 **Runway Gen4** 达到 64.79% 成功率（VLM 基线 50.27%），ImageNav 任务中 **Wan2.2† A14B** 达到 46.53%（基线 35.42%）。消融实验进一步确认：后训练数据扩展和推理时计算扩展均能持续提升任务成功率（Figure 6, Figure 7），而细粒度可控制性比视觉质量对成功率的预测力更强（Figure 5）。



### 世界模型的角色错位：从视觉生成到行动决策

世界模型（World Model）的核心承诺在于让智能体能够在心智中“想象”行动的后果，从而在不实际执行动作的情况下进行规划与推理。近年来，基于扩散模型和自回归Transformer的视频生成器在视觉质量上取得了惊人进展，催生了一批以图像/视频生成为核心的世界模型，如**PathDreamer**（Koh et al., 2021）、**SE3DS**（Koh et al., 2023）、**NWM**（Bar et al., 2025），以及一系列零样本视频生成器如**SVD**（Blattmann et al., 2023）、**LTX-Video**（HaCohen et al., 2024）、**Hunyuan**（Kong et al., 2024）、**Wan2.1/2.2**（Wan et al., 2025）和**Cosmos-Predict2**（Agarwal et al., 2025）。

然而，这些模型的发展轨迹暴露出一个根本性的角色错位：评估体系长期以开放环（open-loop）的视觉质量指标（如FVD、IS、美学评分）为导向，而世界模型在具身智能中的真正价值应体现在闭环（closed-loop）任务成功率上。这一错位导致了一个关键瓶颈：**现有的生成式世界模型专注于视觉质量，但缺乏对行动控制的精确响应，无法支持具身智能体的有效决策**。

### 核心因果机制：可控制性与视觉质量的分离

本文的核心洞察在于识别出决定世界模型效用的关键因果旋钮——**世界模型对行动条件的响应精度（即可控制性，controllability）**，而非生成图像的视觉质量。这一洞察由三个决定性证据支撑：

1. **高视觉质量并不必然转化为强任务成功率**（Figure 2）。散点图显示，生成质量评分与闭环任务成功率之间不存在单调正相关关系，某些视觉质量极高的模型在任务中表现平平。
2. **细粒度可控制性比视觉质量对任务成功更重要**（Section 3.2, Figure 5）。通过将可控制性量化为预测观测与真实观测之间的1−LPIPS距离，分析表明可控制性与成功率的相关性显著强于视觉质量与成功率的相关性。
3. **扩展后训练比升级预训练视频生成器更有效**（Section 3.2, Figure 6）。使用行动-观察数据进行领域后训练带来的性能增益，远超更换更大规模预训练模型的效果。

这一发现颠覆了“更好的生成质量意味着更好的世界模型”的直觉假设，揭示出世界模型在具身任务中的效用取决于其对行动条件的精确响应，而非生成图像的逼真度。

### 现有评估协议的系统性缺陷

传统世界模型评估存在三个结构性缺陷，共同构成了本文的动机基础：

- **评估协议错配**：开放环评估仅衡量生成内容与参考分布的统计相似性，完全忽略了世界模型在闭环交互中是否能为决策提供有效信息。这导致模型在基准上表现优异，却在真实任务中失效。
- **动作接口碎片化**：不同世界模型采用各自特定的动作输入格式（文本描述、相机参数、图像目标等），缺乏统一的动作API，使得跨模型比较和集成变得极为困难。
- **规划策略缺失**：现有工作多将世界模型视为“视图生成器”，而非将其嵌入完整的规划闭环中。缺乏系统性的提议-模拟-修订机制，世界模型的预测能力未能转化为决策优势。

### 本文的应对策略

针对上述缺口，本文提出**World-In-World框架**，在三个维度上重构世界模型的评估与使用范式：

- **评估协议转换**：从开放环视觉质量评估转向闭环任务成功评估，在主动识别（AR）、图像目标导航（ImageNav）、主动具身问答（A-EQA）和机器人操纵四类任务上建立统一基准。
- **统一动作API**：设计标准化的动作接口，支持文本指令、相机轨迹和低层动作等多种控制模式，使不同架构的世界模型能够在同一框架下被调用和比较。
- **闭环在线规划**：引入“提议-模拟-修订”策略，由提议策略生成候选动作序列，世界模型模拟未来观测，修订策略评估模拟轨迹并选择最优决策，形成完整的感知-规划-执行闭环。

此外，本文提出轻量级后训练协议，使用少量行动-观察数据微调预训练视频生成器，使其对齐目标领域的分布和动作空间，从而在不重新训练的情况下显著提升可控制性。



## 核心方法与创新机理

本文的核心创新不在于提出一个新的世界模型架构，而在于**重新定义了世界模型的评估范式与使用方式**，并据此构建了一套完整的闭环基准与适配框架。其关键创新通过以下四个“changed slots”得以体现：

### 从视觉质量到任务成功的评估范式转移

现有世界模型研究普遍以生成图像的视觉质量（如FID、美学评分）作为核心评价指标，但本文通过 Figure 2 的散点图揭示了这一范式的根本缺陷：**高视觉质量并不必然转化为高任务成功率**。多个零样本视频生成器在VBench上获得相近的视觉评分，却在主动识别（AR）任务中表现出从50%到65%的显著成功率差异。这一发现构成了全文的因果杠杆——世界模型在具身任务中的效用取决于其对行动条件的精确响应（可控制性），而非生成图像的视觉保真度。基于此，论文建立了首个以闭环任务成功率为核心的开放基准，覆盖主动识别、图像目标导航、主动具身问答和机器人操纵四类任务（Figure 4）。

### 统一动作API：桥接异构世界模型与具身任务

不同世界模型（从文本条件视频生成器到相机轨迹条件的扩散模型）接受截然不同的控制输入格式，这阻碍了它们在统一闭环协议下的公平比较。本文提出**统一动作API**（Unified Action API），将任意候选动作序列映射为世界模型所需的控制输入，支持三种控制模式：文本提示、相机轨迹/视点、低层动作。这一抽象层使得从零样本视频生成器（如SVD、LTX-Video、Hunyuan、Wan2.1/2.2、Cosmos-Predict2）到专有模型（Runway Gen4）的十余种世界模型能够在同一闭环协议下直接比较（Table 1-3），消除了接口异构带来的评估偏差。

### 提议-模拟-修订的闭环在线规划策略

传统使用世界模型的方式往往局限于开环的视图生成，缺乏与决策的深度耦合。本文提出统一的**闭环在线规划策略**，其核心流程为：提议策略 $\pi_{\mathrm{proposal}}$ 从当前观测 $\mathbf{o}_t$ 和目标 $\mathbf{g}$ 中采样 $M$ 个候选动作序列 $\hat{\mathbf{A}}_t^{(m)}$；统一动作API将其转换为控制输入 $I_t^{(m)}$；世界模型 $g_{\theta}$ 据此预测未来观测序列 $\hat{\mathbf{O}}_t^{(m)}$；修订策略 $\pi_{\mathrm{revision}}$ 评估所有候选计划及其模拟结果，选择最优决策 $\mathbf{D}_t^{\star}$。这一“提议-模拟-修订”循环使世界模型从被动的观察预测器转变为主动的决策支撑器。实验表明，仅添加世界模型即可使VLM基础策略在AR任务上的成功率从50.27%提升至64.79%（Runway Gen4），在ImageNav上从35.42%提升至46.53%（Wan2.2† A14B）。

### 后训练适配：以轻量微调替代大规模预训练

零样本视频生成器虽然具备强大的视觉先验，但缺乏对特定具身领域行动-观察动力学的精确建模。本文引入**后训练协议**，使用与下游任务相同动作空间的少量行动-观察数据（约40K片段）对预训练视频生成器进行微调。这一策略的效果远超直觉预期：Wan2.1†经后训练后，AR准确率从58.26%提升至62.61%，ImageNav成功率从38.19%提升至45.14%（Table 1）。更具启发性的是，**扩展后训练比升级预训练生成器更有效**——Wan2.2†（A14B）尽管拥有更大规模的网络视频预训练，经过同等后训练后仅达到与Wan2.1†近乎相同的性能（Figure 2, Section 3.2）。这揭示了一条清晰的扩展规律：在具身效用维度上，行动条件数据的规模扩展比视觉生成器容量的扩展更具杠杆效应。后训练的计算开销也远低于完整重训练（Table 10），使其具备实用可部署性。

### 细粒度可控制性优于视觉质量

通过对比分析，Figure 5 进一步量化了上述创新背后的因果机制：任务成功率与生成视觉质量（美学评分+图像质量评分）之间缺乏明确的正相关（Figure 5a），而与可控制性（以 $1 - \mathrm{LPIPS}$ 量化预测观测与真实观测的差异）之间呈现清晰的正相关（Figure 5b）。这直接验证了论文的核心洞察——世界模型在具身任务中的价值取决于其对行动的精确响应能力，而非生成图像的视觉完美程度。这一发现为后续世界模型研究指明了优化方向：应将资源投向提升行动条件的细粒度可控性，而非单纯追求视觉生成质量。



![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_yDmb7xAfeb/figures/017_Figure_9.jpg]]
*Figure 9: Overview of our embodied closed-loop evaluation for A-EQA. For each question, the high-level planner proposes multiple candidate action plans and queries the world model to generate the corresponding future observations. The agent then evaluates each plan together with its predicted observations and selects the plan that maximizes the expected reward before executing it in the environment*

World-In-World 提出了一套统一的**闭环在线规划框架**，将视觉世界模型作为具身智能体的内部模拟器，通过“提议—模拟—修订”的循环实现决策优化。其核心设计理念是：世界模型的效用取决于其对行动条件的精确响应（可控制性），而非生成图像的视觉质量。

### 闭环在线规划流程

框架在每一时间步 $t$ 执行四个阶段的迭代，如图 3 所示：

1. **提议 (Proposal)**：给定当前观测 $\mathbf{o}_t$ 和任务目标 $\mathbf{g}$，提议策略 $\pi_{\mathrm{proposal}}$ 采样 $M$ 个候选动作序列：

   $$\hat{\mathbf{A}}_t^{(m)} \sim \pi_{\mathrm{proposal}}(\mathbf{A} \mid \mathbf{o}_t, \mathbf{g}), \quad m = 1, \ldots, M.$$

2. **动作转换 (Unified Action API)**：通过统一动作接口 $\mathcal{C}$ 将每个候选动作序列转换为世界模型所需的控制输入：

   $$I_t^{(m)} = \mathcal{C}(\hat{\mathbf{A}}_t^{(m)}).$$

   该 API 支持三类控制信息：**文本提示**、**相机轨迹/视点**、以及**低层动作**，使得不同输入模态的世界模型能够无缝接入同一评估协议。

3. **模拟推演 (World Model Rollout)**：视觉世界模型 $g_{\theta}$ 基于当前观测和控制输入，预测未来的观测序列：

   $$\hat{\mathbf{O}}_t^{(m)} \sim g_{\theta}(\mathbf{O} \mid \mathbf{o}_t, I_t^{(m)}), \quad \hat{\mathbf{O}}_t^{(m)} = [\hat{\mathbf{o}}_{t+1}^{(m)}, \hat{\mathbf{o}}_{t+2}^{(m)}, \dots, \hat{\mathbf{o}}_{t+L}^{(m)}].$$

4. **修订决策 (Revision)**：修订策略 $\pi_{\mathrm{revision}}$ 评估所有候选计划及其模拟结果，选择最优决策：

   $$\mathbf{D}_t^{\star} = \pi_{\mathrm{revision}}\biggl(\{(\hat{\mathbf{A}}_t^{(m)}, \hat{\mathbf{O}}_t^{(m)})\}_{m=1}^M, \mathbf{o}_t, \mathbf{g}\biggr).$$

   实际实现中，通常采用**评分-选择 (Score-and-Select)** 策略，通过评分函数 $S$ 为每个候选计划打分，选取得分最高者：

   $$\mathbf{D}_t^{\star} = \hat{\mathbf{A}}_t^{(m^{\star})}, \quad \text{where} \quad m^{\star} = \operatorname*{argmax}_{m \in \{1, \ldots, M\}} S\Big(\hat{\mathbf{A}}_t^{(m)}, \hat{\mathbf{O}}_t^{(m)} \mid \mathbf{o}_t, \mathbf{g}\Big).$$

所选决策在真实环境中执行，完成交互闭环，随后进入下一时间步。

### 世界模型的后训练适应

为使预训练视频生成器适配具身任务，框架引入**轻量级后训练协议**：使用与下游任务相同动作空间的动作-观测数据对预训练模型进行微调。对于 Habitat-Sim 任务（AR、A-EQA、ImageNav），后训练数据来自 HM3D 训练集的**全景动作-观测数据集**；对于 CoppeliaSim 操纵任务，数据来自 RLBench 的**任务演示**。后训练过程仅需约 40K 域内片段，计算成本远低于完整重训练（见表 10）。

### 模块关系与数据流

四个核心模块形成端到端的数据流：**提议策略**产生候选动作 → **统一动作 API** 进行格式转换 → **世界模型**执行前向推演 → **修订策略**综合评估并输出最终决策。其中，世界模型是整个框架的瓶颈所在——其预测精度直接决定了模拟推演的可靠性，进而影响修订策略的决策质量。框架的设计使得任何符合统一动作 API 的世界模型均可即插即用，支持从零样本视频生成器到后训练专用模型的公平对比。



World-In-World 框架的核心是一个统一的闭环在线规划策略，其运转由三个关键模块构成：提议策略（Proposal Policy）、统一动作API（Unified Action API）和修订策略（Revision Policy），三者围绕视觉世界模型形成“提议—模拟—修订”的决策循环（Figure 3）。

### 提议策略：生成候选动作序列

在时间步 $t$，给定当前观测 $\mathbf{o}_t$ 和任务目标 $\mathbf{g}$，提议策略 $\pi_{\mathrm{proposal}}$ 采样 $M$ 个候选动作序列，作为未来候选计划：

$$
\hat{\mathbf{A}}_t^{(m)} \sim \pi_{\mathrm{proposal}}(\mathbf{A} \mid \mathbf{o}_t, \mathbf{g}), \quad m = 1, \ldots, M.
$$

该模块的核心作用是产生多样化的行动假设，供世界模型在模拟中评估。提议策略的具体实现可以是视觉语言模型（VLM）或基于规则的探索策略，其质量直接影响搜索空间的上限。

### 统一动作API：桥接策略与世界模型

候选动作序列 $\hat{\mathbf{A}}_t^{(m)}$ 随后通过统一动作API $\mathcal{C}$ 转换为世界模型所需的控制输入：

$$
I_t^{(m)} = \mathcal{C}(\hat{\mathbf{A}}_t^{(m)}).
$$

该API支持三种控制信息类型——文本提示、相机轨迹/视点、低层动作——使得不同架构的世界模型（如基于文本条件的视频生成器与基于相机位姿的视图合成模型）能够在同一闭环协议下被调用。这一标准化接口是框架能够集成多种异构世界模型的关键设计。

### 世界模型推演：预测未来观测

视觉世界模型 $g_{\theta}$ 基于当前观测 $\mathbf{o}_t$ 和控制输入 $I_t^{(m)}$，预测长度为 $L$ 的未来观测序列：

$$
\hat{\mathbf{O}}_t^{(m)} \sim g_{\theta}(\mathbf{O} \mid \mathbf{o}_t, I_t^{(m)}), \quad \hat{\mathbf{O}}_t^{(m)} = [\hat{\mathbf{o}}_{t+1}^{(m)}, \hat{\mathbf{o}}_{t+2}^{(m)}, \dots, \hat{\mathbf{o}}_{t+L}^{(m)}].
$$

世界模型在此扮演“想象引擎”的角色，将候选动作计划转化为可视化的未来状态推演，为后续的决策评估提供依据。

### 修订策略：评估并选择最优决策

修订策略 $\pi_{\mathrm{revision}}$ 接收所有候选计划及其模拟结果，结合当前观测与目标，输出最终决策 $\mathbf{D}_t^{\star}$：

$$
\mathbf{D}_t^{\star} = \pi_{\mathrm{revision}}\biggl(\{(\hat{\mathbf{A}}_t^{(m)}, \hat{\mathbf{O}}_t^{(m)})\}_{m=1}^M, \mathbf{o}_t, \mathrm{g}\biggr).
$$

论文给出了一种常用的实例化方式——评分选择（Score-and-Select）：通过评分函数 $S$ 对每个候选计划及其模拟轨迹打分，选择得分最高的计划：

$$
\mathbf{D}_t^{\star} = \hat{\mathbf{A}}_t^{(m^{\star})}, \quad \mathrm{where} \quad m^{\star} = \operatorname*{argmax}_{m \in \{1, \ldots, M\}} S\Big(\hat{\mathbf{A}}_t^{(m)}, \hat{\mathbf{O}}_t^{(m)} \mid \mathbf{o}_t, \mathbf{g}\Big).
$$

评分函数 $S$ 通常由VLM实现，评估模拟轨迹与任务目标的一致性。这一模块决定了世界模型的“想象”能否转化为有效的行动选择。

### 后训练适配：对齐领域分布与动作空间

除了上述在线规划模块，框架还包含一个离线后训练协议（Section 2.4），使用少量动作-观测数据对预训练视频生成器进行微调。后训练的核心目的是将通用视频生成器对齐到目标环境的领域分布和动作空间，从而提升世界模型对控制输入的响应精度（即可控制性）。后训练数据与评估场景不相交，确保泛化性评估的公平性。



## 实验与关键发现

### 主要结果

World-In-World 在四项具身任务上系统评估了多种视觉世界模型，涵盖零样本视频生成器、后训练变体及专有模型。核心结论如下：

**主动识别（Active Recognition, AR）与图像目标导航（Image-Goal Navigation, ImageNav）**：Table 1 汇总了各模型在两项导航密集型任务上的表现。引入视觉世界模型一致且显著地提升了基础 VLM 提议策略的性能。在 AR 任务上，Runway Gen4 达到最高的 64.79% 成功率（SR），将基线（无世界模型的 VLM）的 50.27% 提升了 14.52 个百分点，同时平均轨迹长度从 6.24 步缩短至 4.06 步。在 ImageNav 任务上，后训练的 Wan2.2† A14B 取得 46.53% 的 SR，较基线 35.42% 提升 11.11 个百分点。值得注意的是，后训练（以 † 标记）对所有模型均带来实质性增益：Wan2.1† 的 AR 准确率从零样本的 58.26% 跃升至 62.61%，ImageNav 的 SR 从 38.19% 提升至 45.14%。

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_yDmb7xAfeb/figures/006_Table_1.jpg]]
*Table 1: Active Recognition (AR) and Image-Goal Navigation (ImageNav) performance across various models and base policies. Higher success rate (SR%), success weighted by path length (SPL%), and lower mean trajectory length (Mean Traj.) are better. “†” denotes our post-trained video generators. “A14B” denotes a mixture-of-experts configuration of Wan2.2 with an effective model size of 14B during inference*

**主动具身问答（A-EQA）**：Table 2 显示，Wan2.2† A14B 取得 48.4 的回答得分和 31.9 的 SPL，超越 VLM 基线的 45.7 分和 29.6 SPL。世界模型的增益在此任务上相对温和（+2.5 分），但方向一致。

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_yDmb7xAfeb/figures/007_Table_2.jpg]]
*Table 2: Active Embodied Question Answering (A-EQA) performance*

**机器人操纵**：Table 3 揭示了当前视觉世界模型的瓶颈。后训练的 SVD† 达到 46.5% 的 SR，仅略高于基线的 44.5%（+2.0 个百分点）。这一微弱增益表明，精确建模接触丰富的物理交互和细粒度物体运动仍是视频生成式世界模型的核心短板。

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_yDmb7xAfeb/figures/008_Table_3.jpg]]
*Table 3: Robotic manipulation performance across various models and base policies*

### 视觉质量与可控性的解耦分析

Figure 2 的散点图揭示了一个反直觉的关键发现：**高视觉质量并不必然转化为高任务成功率**。以 VBench 的生成质量（美学得分与图像质量得分的均值）为横轴、任务成功率为纵轴，数据点呈现出弱相关甚至无关的分布模式。例如，某些零样本视频生成器虽能产出视觉上逼真的预测帧，但其 AR 成功率却显著低于经过后训练但视觉质量相仿的模型。

Figure 5 进一步将这一现象归因于**可控制性**（controllability）——即世界模型对动作条件的响应精度。图 5(a) 展示 SR 与生成质量之间缺乏清晰的正相关；而图 5(b) 以 $1 - \text{LPIPS}$（预测帧与真值帧之间的感知相似度）量化可控制性，则呈现出明显的正向关联。这表明，对于具身决策而言，模型是否精确地“听从”动作指令，远比其生成图像的视觉保真度更为关键。

### 扩展规律：后训练数据规模与推理计算量

**后训练数据扩展**：Figure 6 展示了后训练数据量对 AR 性能的单调正向影响。以 Wan2.1† 为例，随着训练样本从约 10K 增加至 40K，SR 从 60.25% 持续攀升至 63.34%；SVD† 同样从 56.80% 提升至 60.98%。这一趋势表明，面向特定领域的动作-观察数据后训练仍远未饱和。

**预训练规模 vs. 后训练**：一个值得注意的对比来自 Wan2.2† A14B 与 Wan2.1†。前者拥有显著更大的网页视频预训练规模和 14B 有效参数的混合专家架构，但在经过同等 40K 后训练样本后，两者性能几乎持平。这暗示在当前的具身任务设定下，**扩展动作条件后训练比升级预训练生成器本身更有效**。

**推理时扩展**：Figure 7 揭示了推理计算量的扩展效应。对于 SVD†，将每集平均世界模型推理次数从 3 次增加至 11 次，SR 从 53.36% 单调提升至 60.98%。这一正相关关系验证了“提议-模拟-修订”框架中通过增加候选计划采样和模拟来提升决策质量的有效性。

### 消融实验

**输入上下文**：Table 4 比较了前视视图与全景视图作为世界模型输入的影响。结果显示，全景输入并未始终带来显著增益，在某些配置下甚至略逊于前视视图。这可能是因为当前视频生成器对全景图像的畸变和拼接伪影更为敏感。

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_yDmb7xAfeb/figures/013_Table_4.jpg]]
*Table 4: Post-training with different input contexts: front view vs. panorama*

**世界模型增强与修订策略**：Table 5 在 ImageNav 上消融了世界模型增强和修订策略各自的贡献。结果表明，两者均为性能提升的必要组件，缺一不可。

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_yDmb7xAfeb/figures/014_Table_5.jpg]]
*Table 5: Effect of world-model augmentation and revision policy on ImageNav. SR and SPL are higheris-better; mean trajectory length is lower-is-better*

**跨域泛化**：Table 6 考察了在 HSSD 数据集上后训练、在 HM3D/MP3D 上评估的跨域迁移能力。后训练于目标域（HM3D）的模型在 ImageNav 上取得 45.14% SR，高于在 HSSD 上后训练的 42.36%，但仍显著优于无世界模型基线（35.42%）。这表明后训练具有一定的泛化性，但域间差距仍是限制因素。

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_yDmb7xAfeb/figures/015_Table_6.jpg]]
*Table 6: Cross-domain post-training: WMs post-trained on HSSD or HM3D and evaluated on HM3D/MP3D (val) for AR and ImageNav*

**VLM 策略变体**：Table 7 对比了不同 InternVL3 变体在有/无世界模型下的表现，确认世界模型的增益在不同规模的 VLM 策略上均稳健存在。

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_yDmb7xAfeb/figures/020_Table_7.jpg]]
*Table 7: Task performance for InternVL3 variants with and without a world model. Higher SR%, SPL%, and Ans. Score are better; lower Mean Traj. is better*

### 失败模式与局限

1. **物理不一致推演**：在长程规划中，视觉世界模型可能生成物理上不合理或不一致的预测帧（如物体瞬移、视角跳变），导致修订策略被误导，选择次优动作。
2. **操纵任务瓶颈**：当前视频生成器难以精确建模接触力学和精细运动，使得世界模型在机器人操纵任务上的增益十分有限（Table 3），这是将生成式世界模型应用于具身操作的核心障碍。
3. **推理成本**：尽管后训练资源需求相对轻量（Table 10），但推理时每步需执行多次世界模型前向传播，计算开销高，难以满足实时部署需求。
4. **跨域泛化不足**：后训练对特定场景分布存在过拟合倾向，跨域迁移时性能下降明显，泛化能力仍需系统性提升。

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_yDmb7xAfeb/figures/022_Table_9.jpg]]
*Table 9: All the world models and their details in World-In-World. “†” denotes post-trained (actionconditioned) variants. In Table 10, we summarize the computational resources required to post-train each world model on ∼40k domain-specific clips collected from Habitat-Sim. This post-training stage is intentionally lightweight and is several orders of magnitude less expensive than full pretraining. For 14B-parameter variants, we adopt LoRA fine-tuning to reduce GPU memory usage, while all other models are fine-tuned with full weights*

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_yDmb7xAfeb/figures/023_Table_10.jpg]]
*Table 10: Post-training resources for ∼40k domain clips per model. The procedure is lightweight and substantially cheaper than full retraining*

### 补充图表

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_yDmb7xAfeb/figures/021_Table_8.jpg]]
*Table 8: Post-trained (action-conditioned) world models used in our experiments, with repositories and training configurations*

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_yDmb7xAfeb/figures/024_Table_11.jpg]]



## 定位与知识库关联

### 1. 在生成式世界模型谱系中的位置

World-In-World 针对的是**具身决策场景下的视觉世界模型**，其核心贡献不在于提出新的生成架构，而在于**重新定义评估协议与集成范式**。它将现有的视频/图像生成器统一纳入一个闭环在线规划框架，并通过标准化动作API和后训练协议赋予这些模型可控制性。

**与现有世界模型的对比：**

- **图像生成世界模型**（如 **PathDreamer** (Koh et al., 2021)、**SE3DS** (Koh et al., 2023)）仅生成单帧未来视图，缺乏对动作序列的时序建模能力。World-In-World 的视频生成骨干天然支持时序推演，且统一动作API使其能接收文本、相机轨迹和低层动作等多种控制信号，远超图像生成模型的单步视图合成范式。

- **视频生成世界模型**（如 **NWM** (Bar et al., 2025)）虽支持视频预测，但其评估仍依赖开放环的视觉质量指标，且动作接口通常为模型特定设计。World-In-World 的关键突破在于：将评估从“生成的视频是否好看”转向“生成的视频能否支撑任务成功”，并证明两者之间不存在必然正相关（Figure 2）。

- **零样本视频生成器**（**SVD** (Blattmann et al., 2023)、**LTX-Video** (HaCohen et al., 2024)、**Hunyuan** (Kong et al., 2024)、**Wan2.1/Wan2.2** (Wan et al., 2025)、**Cosmos-Predict2** (Agarwal et al., 2025)、**Runway Gen4**）本身并非为具身决策设计。World-In-World 通过后训练协议将这些通用视频生成器适配为具身世界模型，并证明**扩展后训练数据比升级预训练生成器更有效**——Wan2.2† (A14B) 尽管拥有更大规模的网络视频预训练，在40K后训练样本后性能与 Wan2.1† 几乎持平（Section 3.2, Figure 6）。

### 2. 核心方法槽位对比

World-In-World 在四个关键方法槽位上与基线方案形成系统性差异：

| 方法槽位 | 基线方案 | World-In-World | 证据锚点 |
|---------|---------|----------------|---------|
| **评估协议** | 开放环视觉质量评估（FVD、LPIPS、美学分数） | 闭环任务成功评估（SR%、SPL%、Ans. Score） | Abstract, Section 1 |
| **动作接口** | 模型特定的文本或图像条件 | 统一动作API（文本提示、相机轨迹、低层动作） | Section 2.2 |
| **规划策略** | 无世界模型或仅用世界模型生成单步视图 | 提议-模拟-修订的在线规划（M个候选序列并行推演） | Section 2.1, Figure 3 |
| **世界模型适应** | 零样本使用预训练视频生成器 | 使用动作-观察数据进行领域后训练 | Section 2.4 |

**评估协议的根本转变**是该工作的核心贡献。传统世界模型评估（如 VBench）关注生成图像的感知质量，但 Figure 2 的散点图揭示：高美学/图像质量分数并不必然转化为高任务成功率。这从根本上挑战了“更好的视觉质量意味着更好的世界模型”这一隐含假设。

**统一动作API** 解决了异构世界模型集成中的接口碎片化问题。通过将动作序列 $\mathbf{A}$ 映射为控制输入 $\mathbf{I} = C(\mathbf{A})$，该API支持三种控制模式：(1) 文本提示（如“向前移动”），(2) 相机轨迹/视点（如位姿变换），(3) 低层动作（如关节角度），使不同架构的生成器能在同一框架下公平比较（Section 2.2）。

### 3. 适用边界与失败模式

**适用边界：**

- **导航与主动感知任务**（AR、ImageNav、A-EQA）是当前框架的优势场景。世界模型主要用于预测视点变化后的观测，对物理交互精度要求相对宽松。在这些任务上，添加世界模型一致提升基础策略性能：AR 上 Runway Gen4 达到 64.79% SR（VLM 基线 50.27%），ImageNav 上 Wan2.2† A14B 达到 46.53% SR（VLM 基线 35.42%）（Table 1）。

- **后训练数据与评估场景不相交**是泛化性的基本保障。后训练数据来自 HM3D 训练集，评估在 HM3D 验证集和 MP3D 上进行，确保性能增益来自世界模型的可控制性提升而非数据泄露。

**失败模式：**

- **精细物理交互场景**表现受限。在机器人操纵任务上，最佳后训练模型 SVD† 仅达到 46.5% SR，相比 VLM 基线（44.5%）提升仅 2.0 个百分点（Table 3）。这表明当前视觉世界模型在建模接触动力学、精确物体运动和力交互方面存在根本性不足。

- **长程规划中的物理不一致性**是已知风险。视觉世界模型在长时间推演中可能产生不符合物理规律的预测（如物体穿透、不合理的相机运动），这些幻觉会误导修订策略的决策。跨域后训练实验（Table 6）显示：在 HSSD 上后训练的模型迁移到 HM3D/MP3D 时，ImageNav SR 从 45.14% 降至 42.36%，说明领域偏移会加剧物理不一致问题。

- **推理计算成本**制约实时部署。Figure 7 显示推理时扩展（平均每集推理次数从 3 增加到 11）可将 SVD† 的 SR 从 53.36% 提升至 60.98%，但代价是约 3.7 倍的计算开销。对于需要实时响应的机器人场景，这一成本目前难以承受。Table 10 报告了各模型后训练约 40K 领域片段所需的资源，虽比全量重训练轻量，但仍需一定计算投入。

### 4. 关键开放问题

基于上述局限，该工作揭示了以下待解决的核心问题：

1. **精细物理建模**：如何使视频生成器准确建模接触丰富的交互（如抓取、推动）和物体动力学，是视觉世界模型从导航走向操纵的关键瓶颈。

2. **跨域泛化**：后训练仅针对特定领域分布，如何提升世界模型在未见具身环境中的推演可靠性，避免物理不一致的预测，需要更好的分布外泛化机制。

3. **推理效率**：当前视觉世界模型的推理计算成本与任务性能正相关（Figure 7），如何在有限计算预算下实现高效规划，是实时部署的前提。

4. **长程依赖编码**：如何有效编码和利用长期依赖性进行长程规划，避免推演误差的累积放大，是提升复杂任务性能的上限因素。

5. **提议与修订策略的上限**：当前框架的性能受限于提议策略的多样性和修订策略的判别能力。Table 5 显示世界模型增强和修订策略对 ImageNav 的影响显著，但如何设计更强的规划策略以充分释放世界模型的潜力，仍是开放方向。



## 原文 PDF

![[paperPDFs/ICLR_2026/World_In_World_World_Models_in_a_Closed_Loop_World.pdf]]
