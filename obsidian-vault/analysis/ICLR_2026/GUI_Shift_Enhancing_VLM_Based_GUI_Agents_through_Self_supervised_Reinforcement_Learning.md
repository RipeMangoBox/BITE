---
title: "GUI-Shift: Enhancing VLM-Based GUI Agents through Self-supervised Reinforcement Learning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/GUI_Shift_Enhancing_VLM_Based_GUI_Agents_through_Self_supervised_Reinforcement_Learning.pdf
project_link: null
code_link: https://github.com/UbiquitousLearning/GUI-Shift
openreview_forum_id: NakMHPljT7
aliases:
- GS
- GUI-Shift
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/vision_models_multimodal
core_operator: "K步GUI转移自监督任务与基于组相对策略优化(GRPO)的强化学习框架的结合，能够从无标注轨迹中学习GUI动态。"
primary_logic: "通过预测两个GUI截图之间的首个动作，并利用容忍功能等价操作的规则奖励，模型可以独立于文本指令学习GUI动态，从而实现可扩展的高效训练。"
claims:
- "GUI-Shift仅用2K无标注样本就匹配或超越了使用百万级标注样本训练的模型。"
- "使用未来状态S_{t+k}作为视觉目标优于使用文本指令训练。"
- "去除推理链将训练时间减半(17h→9h)且不损失性能。"
- "GRPO相比SFT在K步转移任务上提供显著性能提升，而SFT导致退化。"
---

# GUI-Shift: Enhancing VLM-Based GUI Agents through Self-supervised Reinforcement Learning

> [!tip] 核心洞察
> 通过预测两个GUI截图之间的首个动作，并利用容忍功能等价操作的规则奖励，模型可以独立于文本指令学习GUI动态，从而实现可扩展的高效训练。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | GUI-Shift：通过自监督强化学习增强VLM GUI代理 |
| 英文题名 | GUI-Shift: Enhancing VLM-Based GUI Agents through Self-supervised Reinforcement Learning |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=NakMHPljT7) · [GitHub](https://github.com/UbiquitousLearning/GUI-Shift) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal |
| Method | GUI-Shift |
| Dataset | AndroidControl-High, AndroidControl-Low, ScreenSpot-v2, ScreenSpot-Pro |

> [!tip] 效果简介
> - AndroidControl-High 上，EM 为 70.4 (GUI-Shift-Qwen, k=1)，对比 59.2 (Qwen2.5-VL-7B)，变化 +11.2%。
> - AndroidControl-Low 上，EM 为 93.2 (GUI-Shift-Mimo-SFT, k=3, filtered)，对比 85.7 (Mimo-VL-7B-SFT)，变化 +7.5%。
> - ScreenSpot-v2 上，Avg. 为 90.1 (GUI-Shift-Mimo-SFT, k=1)，对比 87.6 (Mimo-VL-7B-SFT)，变化 +2.5%。

## 概要

### 问题瓶颈

训练基于视觉语言模型（VLM）的GUI代理通常依赖大规模人工标注的数据集，每条训练样本需要将文本指令映射为精确的动作序列。这一收集过程劳动密集且易出错，严重限制了训练的可扩展性。同时，大量已有的无标注GUI交互轨迹（如离线探索记录）未被有效利用。

### 核心方法

GUI-Shift通过一个自监督强化学习框架解决上述瓶颈，其核心由三个关键设计构成：

- **K步GUI转移任务**：将训练目标从“文本指令→动作”重构为“状态对→首个动作”。给定两个截图 $S_t$ 和 $S_{t+k}$，模型需预测使界面从 $S_t$ 转移到 $S_{t+k}$ 的第一个动作。这本质上是一个逆动力学任务，完全摆脱了对文本标注的依赖。
- **组相对策略优化（GRPO）**：采用基于组的强化学习算法，为每个输入采样多个候选动作，通过组内归一化优势进行排序和优化，避免训练额外的价值网络。
- **容忍性规则奖励**：针对不同动作类型设计规则化奖励（如点击坐标落在目标边界框内即视为正确），容忍功能等价的操作差异。

三者协同的因果机制在于：K步转移任务提供了独立于文本指令的学习信号，GRPO通过探索多样化的动作候选并利用规则奖励进行筛选，使模型能够从无标注轨迹中高效学习GUI动态。

### 方法定位

GUI-Shift在方法谱系中处于自监督强化学习与GUI代理训练的交叉点。与依赖大规模标注的监督微调（SFT）方法（如**SeeClick** [Cheng et al., 2024]、**OS-Atlas-7B** [Wu et al., 2024b]）不同，GUI-Shift仅需无标注截图对即可训练。相较于同样探索强化学习的GUI代理方法（如**UI-R1-3B** [Lu et al., 2025]、**GUI-R1-7B** [Xia & Luo, 2025]），GUI-Shift的关键差异在于以未来视觉状态而非文本指令作为训练目标，并移除了显式推理链要求以提升训练效率。

### 主要结果

在仅使用2K无标注训练样本的条件下，GUI-Shift实现了显著的性能提升：

- **GUI任务自动化**：在AndroidControl-High基准上，GUI-Shift-Qwen达到70.4%的精确匹配率，较基础模型Qwen2.5-VL-7B提升11.2个百分点（Table 1）。
- **GUI接地**：在ScreenSpot-v2上平均准确率达90.1%，展现强泛化能力（Table 2）。
- **端到端控制**：在AndroidControl-Low端到端任务上，GUI-Shift-Mimo-SFT的成功率从48.4%提升至75.7%，增幅达27.3个百分点（Table 3）。
- **交互式任务**：在AndroidWorld基准上，GUI-Shift-Mimo-SFT将Pass@1成功率从6.0%提升至16.4%（Figure 2）。

消融实验进一步验证了框架各组件的有效性：GRPO在K步转移任务上显著优于SFT（Figure 4）；移除推理链使训练时间从17小时减半至9小时且不损失性能（Table 4）；模型特定的数据过滤策略在所有任务上一致提升性能（Figure 3）。

### 局限与开放问题

当前方法存在以下主要局限：训练数据仅来源于AndroidControl，可能引入移动端GUI偏差，对平板、桌面等平台的泛化有限；实验仅在7-8B参数规模VLM上进行；奖励函数依赖坐标和格式匹配，无法捕获语义正确性。开放问题包括：如何自动化收集大规模多样化无标注GUI轨迹、能否引入更细粒度的语义奖励、以及该方法在更大模型上的扩展性如何。



视觉语言模型（VLM）驱动的GUI代理旨在根据屏幕截图和用户指令，预测可执行的界面操作。这类代理的泛化能力高度依赖大规模、高质量的训练数据。然而，当前主流的数据构建范式存在一个根本性瓶颈：**训练VLM GUI代理通常依赖大规模人工标注的数据集，收集过程劳动密集且易出错，限制了可扩展性**。

具体而言，现有方法通常要求为每一步GUI操作提供精确的自然语言指令作为监督信号。这种范式面临三重约束：（1）人工标注成本高昂，难以覆盖多样化的应用场景和操作模式；（2）标注过程容易引入不一致性，不同标注者对同一屏幕状态的指令描述可能差异显著；（3）大量已收集的离线GUI轨迹数据（如自动化测试脚本产生的大量截图序列）因缺乏对应的文本标注而无法被有效利用。

与此同时，近期工作开始探索将强化学习引入GUI代理训练，但多数方法仍依赖文本指令作为输入，或需要在线交互环境，未能从根本上解决数据标注瓶颈。部分小样本RL模型（如**UI-R1-3B**，Lu et al., 2025；**GUI-R1-7B**，Xia & Luo, 2025）和两阶段SFT+RL模型（如**InfiGUI-R1-3B**，Liu et al., 2025）虽试图降低数据需求，但性能仍受限于标注数据的质量和规模。

本文的核心动机在于：**能否设计一种完全不依赖文本指令的自监督训练范式，使VLM从无标注的GUI轨迹中学习界面动态？** 这一思路的关键洞察是：GUI操作的本质是引起界面状态转移的动作序列，而两个截图之间的状态差异本身就蕴含了“该做什么”的丰富信息——模型只需学会回答“是什么动作导致了从状态S_t到状态S_{t+k}的变化”，即可习得GUI动态知识，无需任何人工文本标注。



## 核心方法与创新机理

GUI-Shift 的核心创新在于将 VLM GUI 代理的训练从**依赖文本指令的监督学习范式**转变为**基于状态转移的自监督强化学习范式**。这一转变通过三个相互耦合的机制实现，共同解决了大规模人工标注数据稀缺与训练效率低下的瓶颈。

### 1. 训练任务形式：从文本指令到 K 步 GUI 转移

传统方法将 GUI 代理训练形式化为“文本指令→动作”的映射，需要大量人工标注的指令-动作对。GUI-Shift 提出 **K 步 GUI 转移（K-step GUI Transition）** 自监督任务：给定当前截图 $S_t$ 和未来截图 $S_{t+k}$，模型预测从 $S_t$ 过渡到 $S_{t+k}$ 所需的**第一个动作**。

这一任务形式的关键优势在于：
- **数据构造零标注**：从离线 GUI 轨迹中自动抽取状态对 $(S_t, S_{t+k})$ 并记录真实动作序列，无需任何人工标注。一条 $N$ 帧轨迹可产生至多 $N-K$ 个训练样本，极大提升了数据利用率。
- **视觉目标替代文本指令**：未来状态 $S_{t+k}$ 作为视觉目标，隐式编码了任务意图。消融实验（Table 4）表明，使用 $S_{t+k}$ 作为视觉目标优于使用显式文本指令训练，即使文本指令包含更明确的目标信息。

### 2. 训练算法：从 SFT 到 GRPO 的强化学习

GUI-Shift 采用**组相对策略优化（Group Relative Policy Optimization, GRPO）** 替代传统的监督微调（SFT）。GRPO 的核心机制是：对每个输入采样 $G=8$ 个候选动作，计算组内归一化优势，并使用截断代理目标与 KL 散度正则项更新策略：

$$\mathcal{J}_{\mathrm{GRPO}}(\theta) = \mathbb{E} \left[ \frac{1}{G} \sum_{i=1}^{G} \left( \min\left( \rho_i A_i, \ \mathrm{clip}\left( \rho_i, 1-\epsilon, 1+\epsilon \right) A_i \right) - \beta \mathbb{D}_{\mathrm{KL}}\left( \pi_{\theta} \| \pi_{\mathrm{ref}} \right) \right) \right]$$

其中优势函数 $A_i$ 由组内奖励标准化得到，无需训练额外的价值网络，降低了计算开销。

**GRPO vs SFT 的关键差异**：在 K 步转移任务上，GRPO 相比 SFT 提供显著性能提升，而 SFT 反而导致模型退化——在部分设置下 SFT 准确率相对 GRPO 下降高达 65.1%（Figure 4）。这表明 K 步转移任务天然适合强化学习范式：模型需要探索多种可能的动作路径，而 SFT 的交叉熵损失仅鼓励复制单一真实动作，无法有效利用“容忍功能等价操作”的奖励信号。

### 3. 奖励设计：从精确匹配到容忍规则

传统 SFT 要求预测动作与真实动作精确匹配。GUI-Shift 设计了**基于规则的容忍奖励函数**，总奖励为格式奖励与动作奖励之和：

$$R = R_f + R_a$$

动作奖励 $R_a$ 根据动作类型采用不同的容忍策略：
- **点击/长按**：预测坐标落在目标边界框内即视为正确
- **文本类动作**（open_app、input_text、scroll）：要求动作类型和参数完全匹配
- **导航类动作**（navigate_back、navigate_home、wait）：仅要求动作类型匹配

这一设计容忍了功能等价的操作差异（如点击按钮的不同位置），使模型能够从多样的动作候选中学习 GUI 动态，而非死记硬背单一轨迹。

### 4. 推理需求：移除显式推理链

传统 VLM 训练常要求模型输出推理过程，消耗大量 token。GUI-Shift 移除了显式推理要求，仅输出最终动作答案。实验表明（Table 4），这一设计将训练时间减半（Qwen2.5-VL-7B 从 17 小时降至 9 小时），且维持甚至提升了性能。这说明 K 步转移任务本身已隐式编码了推理过程——模型通过对比两个状态来推断动作，无需额外的文本推理链。

### 5. 数据选择：模型特定过滤

GUI-Shift 提出基于模型自身能力的数据过滤策略：使用当前策略为每个样本生成多个候选动作，仅保留**同时含有正确与错误预测**的样本。这些“有区分度”的样本对齐了模型当前的学习边界，在所有任务和模型上一致提升性能（Figure 3）。这一策略无需外部标注，完全基于模型自身的奖励信号。

### 创新总结

| 设计槽位 | 基线方法 | GUI-Shift | 核心收益 |
|---------|---------|-----------|---------|
| 训练任务 | 文本指令→动作 | 状态对 $(S_t, S_{t+k})$→首个动作 | 零标注数据构造，视觉目标优于文本指令 |
| 训练算法 | SFT（交叉熵） | GRPO（组优势+KL正则） | 显著性能提升，SFT 反而退化 |
| 奖励设计 | 精确动作匹配 | 容忍规则（坐标容错、类型匹配） | 允许功能等价操作，增强探索 |
| 推理需求 | 显式推理链 | 仅输出动作 | 训练时间减半，性能不降 |
| 数据选择 | 全量使用 | 模型特定过滤 | 保留有区分度样本，一致提升性能 |



![[assets/figures/papers/paper_list_l33_https_openreview_net_forum_id_NakMHPljT7/figures/001_Figure_1.jpg]]
*Figure 1: Overview of the GUI-Shift framework. Left: K-step GUI Transition replaces annotated instructions with the target state S _ { t + k } , enabling scalable data construction through automated offline exploration. Middle: The model learns GUI dynamics by predicting the action that causes the transition. Right: GUI-Shift achieves self-supervised training by applying GRPO to GUI Transition*

GUI-Shift是一个自监督强化学习框架，其核心设计围绕一个关键洞察展开：**通过预测两个GUI截图之间的首个动作，并利用容忍功能等价操作的规则奖励，模型可以独立于文本指令学习GUI动态**。这从根本上绕过了传统VLM GUI代理训练对大规模人工标注的依赖。

### 框架总览

整个pipeline由四个紧密耦合的模块构成，形成“数据构造→数据过滤→GRPO训练→规则奖励”的闭环（参见Figure 1）：

1. **K步GUI转移数据构造**：从离线GUI轨迹中自动抽取状态对 $(S_t, S_{t+k})$ 及对应的真实动作序列，无需任何人工标注。一条包含 $N$ 张截图的轨迹可产生至多 $N-K$ 个训练对，最大化数据利用率。
2. **模型特定数据过滤**：使用当前策略为每个样本生成多个候选动作，依据奖励分布保留既有正确预测又有错误预测的“困难样本”，使训练数据与模型当前能力对齐。
3. **GRPO训练循环**：以过滤后的状态对作为输入，采样8个候选输出，计算组归一化优势，通过截断代理目标与KL散度正则项更新策略模型。
4. **规则化奖励计算**：根据动作类型检查格式和参数正确性，输出格式奖励 $R_f$ 与动作奖励 $R_a$ 之和作为总奖励 $R = R_f + R_a$。

### 输入输出流

- **输入**：一对GUI截图 $S_t$ 和 $S_{t+k}$，分别表示当前状态与 $k$ 步后的目标状态。
- **输出**：模型预测从 $S_t$ 过渡到 $S_{t+k}$ 所需的**第一个动作**（包含动作类型及参数，如点击坐标、输入文本等）。
- **奖励信号**：完全基于规则，无需人工判断。对于点击/长按类动作，只要预测坐标落在目标元素的边界框内即给正奖励；对于文本类动作则要求类型和参数完全匹配。

### 关键设计选择

框架有两个反直觉但经过验证的设计：
- **以视觉目标替代文本指令**：传统方法将任务描述文本作为输入，GUI-Shift则直接用未来状态 $S_{t+k}$ 作为视觉目标。实验表明，即使文本指令包含更明确的目标信息，视觉目标仍能带来更优性能（Table 4）。
- **移除显式推理链**：GUI-Shift不要求模型输出推理过程，仅输出最终动作。这不仅将训练时间减半（Qwen2.5-VL-7B从17小时降至9小时），还维持甚至提升了性能（Table 4）。



### 3.1 组相对策略优化（GRPO）

GUI-Shift采用组相对策略优化（GRPO）作为核心训练算法。GRPO是PPO的计算高效替代方案，其核心思想是对每个输入采样一组输出，利用组内奖励的相对排名计算优势，从而避免训练独立的价值网络。

对于每个输入问题 $q$，从旧策略 $\pi_{\theta_{old}}$ 中采样 $G$ 个输出 $\{o_i\}_{i=1}^G$，每个输出 $o_i$ 通过奖励函数获得分数 $r_i$。组内相对优势 $A_i$ 通过组归一化计算：

$$A_i = \frac{r_i - \operatorname{mean}(\{r_1, r_2, \cdots, r_G\})}{\operatorname{std}(\{r_1, r_2, \cdots, r_G\})}$$

策略优化的目标函数为：

$$\mathcal{J}_{\mathrm{GRPO}}(\theta) = \mathbb{E}\left[q \sim P(Q), \{o_i\}_{i=1}^G \sim \pi_{\theta_{old}}(O \mid q)\right] \frac{1}{G} \sum_{i=1}^{G} \left( \min\left(\rho_i A_i, \operatorname{clip}(\rho_i, 1-\epsilon, 1+\epsilon) A_i\right) - \beta \mathbb{D}_{\mathrm{KL}}(\pi_{\theta} \| \pi_{\mathrm{ref}}) \right)$$

其中 $\rho_i = \frac{\pi_\theta(o_i|q)}{\pi_{\theta_{old}}(o_i|q)}$ 为重要性采样比率，$\epsilon$ 控制截断范围，$\beta \mathbb{D}_{\mathrm{KL}}(\pi_{\theta} \| \pi_{\mathrm{ref}})$ 是向参考策略 $\pi_{\mathrm{ref}}$ 的KL散度正则项，防止策略偏离过远。

### 3.2 规则化奖励设计

总奖励 $R$ 由格式奖励 $R_f$ 和动作奖励 $R_a$ 两部分组成：

$$R = R_f + R_a$$

格式奖励 $R_f$ 检查模型输出是否符合预定义的动作格式模板。动作奖励 $R_a$ 根据动作类型采用容忍性规则判断：

$$R_a = \begin{cases} 1, & \text{if } x_1 \leq \hat{x} \leq x_2 \text{ and } y_1 \leq \hat{y} \leq y_2, \quad t \in \{\text{click}, \text{long\_press}\}; \\ 1, & \text{if } \hat{t} = t \text{ and } \hat{p} = p, \quad t \in \{\text{open\_app}, \text{input\_text}, \text{scroll}\}; \\ 1, & \text{if } \hat{t} = t, \quad t \in \{\text{navigate\_back}, \text{navigate\_home}, \text{wait}\}; \\ 0, & \text{otherwise}. \end{cases}$$

对于点击类动作（click、long\_press），只要预测坐标 $(\hat{x}, \hat{y})$ 落在目标元素的边界框 $[x_1, x_2] \times [y_1, y_2]$ 内即视为正确；对于带参数的动作（open\_app、input\_text、scroll），要求预测的动作类型 $\hat{t}$ 和参数 $\hat{p}$ 均与真实值完全匹配；对于无参数导航动作，仅需动作类型匹配。这种容忍性设计允许功能等价但坐标略有偏差的操作获得正向奖励。

### 3.3 K步GUI转移任务

K步GUI转移是GUI-Shift的核心自监督任务。给定一个GUI状态对 $(S_t, S_{t+k})$，模型需要预测从 $S_t$ 到 $S_{t+k}$ 的第一个动作 $a_t$。该任务将视觉目标状态 $S_{t+k}$ 作为隐式指令，替代传统基于文本指令的监督学习范式。

**数据构造**：从离线GUI交互轨迹中自动抽取。对于一条包含 $N$ 张截图的完整轨迹，对每个步长 $K$ 可生成最多 $N-K$ 个训练样本对 $(S_t, S_{t+k})$，每条样本的真实动作 $a_t$ 直接从轨迹中获取，无需任何人工标注。

**数据过滤**：为进一步提升训练效率，GUI-Shift引入模型特定数据过滤流程。对于每个候选样本，使用当前策略采样8个输出并计算奖励分数，仅保留那些预测结果中同时包含正确和错误输出的样本（即 $0 < \text{正确数} < 8$）。这类样本处于模型能力的“学习边缘”，具有更高的信息量和区分度。实验表明，过滤后的2K样本在多个基准上一致优于随机选取的2K样本（Figure 3, Tables 7, 9, 11）。

**训练效率**：由于K步转移任务仅要求模型输出最终动作，无需生成显式推理链，训练过程中避免了大量推理token的解码开销。以Qwen2.5-VL-7B为例，在2K样本上训练时间从含推理链的17小时降至9小时，且下游性能保持不变或略有提升（Table 4）。



## 实验与关键发现

### 核心瓶颈与因果机制

训练VLM GUI代理的传统范式依赖大规模人工标注数据集，收集过程劳动密集且易出错，严重限制了可扩展性。GUI-Shift通过两个关键设计打破这一瓶颈：**K步GUI转移自监督任务**将训练从“文本指令→动作”映射转变为“状态对$(S_t, S_{t+k})$→首个动作”的逆动力学预测，使模型无需文本标注即可从离线轨迹中学习GUI动态；**GRPO强化学习框架**利用组归一化优势和基于规则的容忍奖励，在无价值网络的情况下高效优化策略。这一因果链条的核心洞察是：未来截图本身携带了足够丰富的视觉目标信息，可以替代人工撰写的文本指令，且其信号质量甚至更优（Table 4证实使用$S_{t+k}$作为视觉目标优于使用文本指令训练）。

![[assets/figures/papers/paper_list_l33_https_openreview_net_forum_id_NakMHPljT7/figures/009_Table_4.jpg]]
*Table 4: Performance on GUI task automation under different training settings. GUI-Shift outperforms models trained with textual instructions or with explicit reasoning requirements. Bold: the best result. TM: type match; GR: grounding accuracy for clicks; EM: exact match*

### 主实验结果

#### GUI任务自动化（Table 1）

在AndroidControl和GUI Odyssey基准上，GUI-Shift仅使用**2K无标注样本**即实现显著提升：

- **GUI-Shift-Qwen (k=1)** 在AndroidControl-High上达到70.4% EM，较基座模型Qwen2.5-VL-7B的59.2%提升**+11.2%**，超越所有标注依赖的基线模型（包括使用百万级标注样本训练的SeeClick和OS-Atlas-7B）。
- **GUI-Shift-Mimo-SFT (k=3, filtered)** 在AndroidControl-Low上达到93.2% EM，较Mimo-VL-7B-SFT的85.7%提升**+7.5%**。
- 跨四个基座模型（Qwen2.5-VL-7B、InternVL3-8B、Mimo-VL-7B-SFT、Mimo-VL-7B-RL）的GUI-Shift变体在绝大多数设置下均超越其基座模型，且最佳K值因模型而异。

#### GUI接地泛化（Table 2）

GUI-Shift在接地任务上展现出强泛化能力：

- **GUI-Shift-Mimo-SFT (k=1)** 在ScreenSpot-v2上达到90.1%平均准确率，较Mimo-VL-7B-SFT的87.6%提升**+2.5%**。
- **GUI-Shift-Mimo-RL (k=1)** 在ScreenSpot-Pro上达到41.7%，较Mimo-VL-7B-RL的40.2%提升**+1.5%**，在所有对比模型中排名第二，仅次于UI-Venus-Ground-7B（50.8%）。

值得注意的是，GUI-Shift在接地任务上的提升幅度小于任务自动化任务，这可能因为接地任务更依赖精确的像素级定位，而K步转移任务主要建模动作序列的宏观动态。

#### 端到端GUI控制

在完整交互式任务上，GUI-Shift带来的提升更为显著：

- **AndroidControl端到端（Table 3）**：GUI-Shift-Mimo-SFT (k=3) 在AC-Low上达到75.7%成功率，较基座模型的48.4%提升**+27.3%**；在AC-High上从16.4%提升至34.1%。但InternVL3-8B在AC-Low上出现性能下降（68.3%→61.1%），提示该方法在不同基座模型上的端到端效果存在不一致性，需针对具体模型进行K值搜索。
- **AndroidWorld交互式基准（Figure 2）**：GUI-Shift-Mimo-SFT在Pass@1上从6.0%提升至16.4%（K=3），Pass@5上从18.1%提升至25.9%（K=4），在所有通过率指标上均一致改善。然而绝对成功率仍较低（最高~34% Pass@5），与人类水平存在较大差距。

![[assets/figures/papers/paper_list_l33_https_openreview_net_forum_id_NakMHPljT7/figures/007_Figure_2.jpg]]
*Figure 2: Performance on AndroidWorld of the base model Mimo-VL-7B-SFT and GUI-Shift-Mimo-SFT with different K. Evaluation follows the original M3A agent protocol. GUI-Shift consistently improves success rates across Pass@1, Pass@3, and Pass@5*

### 消融研究

#### 数据过滤机制（Figure 3, Tables 7/9/11）

模型特定数据过滤是GUI-Shift的关键组件。该机制使用当前策略为每个样本生成8个候选动作，仅保留同时包含正确和错误预测的样本——这类样本对模型学习最具区分度。消融实验表明：

- 过滤数据在所有任务和模型上一致优于未过滤数据。例如Mimo-VL-7B-SFT在K=3时获得高达4.8%的准确率提升（Figure 3(f)），ScreenSpot-v2上提升达2.3%（Figure 3(i)）。
- 过滤机制的有效性源于其对齐了数据难度与模型当前能力：过于简单（全对）或过于困难（全错）的样本对学习贡献有限。

![[assets/figures/papers/paper_list_l33_https_openreview_net_forum_id_NakMHPljT7/figures/008_Figure_3.jpg]]
*Figure 3: Impact of Data filtering. Each model is fine-tuned on 2K K-step GUI Transition samples. Filtered data are more informative and challenging, and outperform unfiltered ones*

#### 推理链移除（Table 4, Section 4.4）

GUI-Shift默认不要求模型输出显式推理过程，仅输出最终动作答案。消融显示：

- 去除推理链将训练时间从17小时减半至9小时（Qwen2.5-VL-7B, 2K样本），且通常维持或提高下游性能。
- 这一发现挑战了当前VLM训练中普遍要求推理输出的做法，表明对于逆动力学预测这类感知密集型任务，推理token可能引入噪声而非帮助。

#### 训练算法对比：GRPO vs SFT（Figure 4）

在K步GUI转移任务上，训练算法的选择至关重要：

- **GRPO在所有K值和模型上显著优于SFT**。SFT不仅未能提升性能，反而导致准确率大幅下降——相对GRPO最高下降65.1%（Figure 4(c), K=3）。
- 这一现象的根本原因在于：K步转移任务具有内在的一对多特性（多个动作可能导致相同的视觉结果），SFT的交叉熵损失强制模型拟合单一真实动作，造成严重的分布坍塌；而GRPO通过采样多个候选动作并利用容忍奖励进行相对排序，自然适应了这种多模态输出空间。

#### 视觉目标 vs 文本指令（Table 4）

使用未来状态$S_{t+k}$作为视觉目标优于使用文本指令训练，即使文本指令包含更明确的任务描述。这验证了核心假设：GUI截图本身编码了足够丰富的状态转移信息，且视觉目标避免了文本标注中的歧义和偏差。

### 数据规模缩放（Figure 6）

将训练样本从2K扩展至6K时，InternVL3-8B在AndroidControl上的准确率呈现整体上升趋势，仅有微小波动。这表明GUI-Shift框架具备良好的数据扩展性，更多无标注轨迹有望带来进一步增益。

### 失败模式与局限性

1. **平台偏差**：训练数据全部来自AndroidControl，在GUI Odyssey平板子集上表现下降，对桌面和Web平台的泛化有限。
2. **模型规模限制**：实验仅覆盖7-8B参数VLM，未验证在更大模型上的效果。
3. **端到端性能不足**：在AndroidWorld等复杂交互式任务上，Pass@1最高仅16.4%，远未达到实用水平。该方法仅学习单步动作预测，未建模多步规划和错误恢复。
4. **奖励函数粗糙**：规则奖励仅检查坐标和格式正确性，无法捕获语义错误（如输入了错误的文本内容仍可获得正奖励）。这可能在端到端任务中导致累积错误。
5. **K值选择缺乏自适应性**：最优K值需针对每个模型单独搜索，且不同任务（自动化vs接地）的最优K值可能不同，缺乏统一的自动选择机制。

### 关键图表结论汇总

| 图表 | 核心结论 |
|------|---------|
| Table 1 | 2K无标注样本训练的GUI-Shift匹配或超越百万级标注样本训练的模型 |
| Table 2 | GUI-Shift在接地任务上展现强泛化，ScreenSpot-Pro排名第二 |
| Table 3 | 端到端控制提升显著但存在模型不一致性 |
| Figure 2 | AndroidWorld上一致改善，但绝对成功率仍低 |
| Figure 3 | 数据过滤在所有设置下一致提升性能 |
| Table 4 | 视觉目标优于文本指令，去除推理链提升效率且不损性能 |
| Figure 4 | GRPO显著优于SFT，SFT导致严重性能退化 |

![[assets/figures/papers/paper_list_l33_https_openreview_net_forum_id_NakMHPljT7/figures/002_Table_1.jpg]]
*Table 1: Performance comparison on GUI task automation benchmarks: AndroidControl (AC-Low, AC-High) and GUI Odyssey. GUI-Shift achieves substantial improvements over base models. Bold: the best result; underlined: the second best result. TM: type match; EM: exact match*

![[assets/figures/papers/paper_list_l33_https_openreview_net_forum_id_NakMHPljT7/figures/003_Table_2.jpg]]
*Table 2: Performance comparison on GUI grounding benchmarks: ScreenSpot-v2 and ScreenSpot-Pro. GUI-Shift exhibits strong generalization and achieves the second best result on ScreenSpot-Pro. Bold: the best result; underlined: the second best result*



## 定位与知识库关联

### 1. 与基线工作的关系

GUI-Shift 处于 VLM GUI 代理训练方法的一个关键转折点：**从依赖大规模人工标注的监督学习，转向利用无标注轨迹的自监督强化学习**。其定位可通过与以下几类代表性工作的对比来理解。

**大规模标注 SFT 模型**：SeeClick (Cheng et al., 2024) 和 OS-Atlas-7B (Wu et al., 2024b) 代表了依赖百万级人工标注样本进行监督微调的路线。GUI-Shift 仅使用 2K 无标注样本即匹配或超越这些模型（见表 1、表 2），揭示了标注瓶颈并非不可逾越——GUI 动态本身蕴含了足够的监督信号。

**状态转移 SFT 模型**：UI-TARS-7B (Qin et al., 2025) 同样利用状态转移进行训练，但采用 SFT 范式。GUI-Shift 的关键区分在于训练算法：Figure 4 显示，在相同的 K 步转移任务上，SFT 导致准确率大幅下降（相对 GRPO 最高下降 65.1%），而 GRPO 提供显著提升。这表明**状态转移任务的形式本身并不足够，需要 GRPO 的探索-排序机制来有效学习**。

**小样本 RL 模型**：UI-R1-3B (Lu et al., 2025)、GUI-R1-7B (Xia & Luo, 2025) 和 InfiGUI-R1-3B (Liu et al., 2025) 也采用 RL 训练 VLM GUI 代理，但通常依赖文本指令或两阶段 SFT+RL 流程。GUI-Shift 的核心创新在于**用未来状态截图 S_{t+k} 替代文本指令作为视觉目标**，从而彻底摆脱对指令标注的依赖。Table 4 的消融实验直接验证了这一设计选择：使用 S_{t+k} 作为视觉目标优于使用文本指令，即使文本指令包含更明确的目标信息。

**大规模 RL 模型**：UI-Venus-Navi-7B (Gu et al., 2025) 在大规模数据上进行 RL 训练，在 ScreenSpot-Pro 上取得 50.8% 的领先结果。GUI-Shift-Mimo-RL 以 41.7% 位居第二（表 2），但需注意 GUI-Shift 的训练数据量和计算开销远小于前者，且完全不需要人工标注。

**基础 VLM 基线**：Qwen2.5-VL-7B (Bai et al., 2025)、InternVL3-8B (Chen et al., 2024) 和 Mimo-VL-7B (Xiaomi, 2025b) 作为未针对 GUI 任务专门训练的基础模型，在 AndroidControl-High 上的精确匹配率仅为 59.2%、51.2% 和 44.3%。GUI-Shift 分别将其提升至 70.4%、63.1% 和 54.6%（表 1），验证了方法的通用性——在三种不同架构的 VLM 上均有效。

### 2. 方法适用边界

**平台边界**：训练数据全部来自 AndroidControl 数据集，这引入了显著的移动 GUI 偏差。在 GUI Odyssey 的平板子集上，GUI-Shift 的性能提升幅度明显小于手机场景，表明方法对训练分布外的 GUI 布局和交互模式的泛化有限。桌面和 Web 平台的适用性尚未验证。

**模型规模边界**：实验仅覆盖 7-8B 参数规模的 VLM。GRPO 的组采样机制和 KL 正则化在更大模型上的行为未知——更大模型可能从更强的先验中受益更多，也可能因探索空间扩大而需要调整组大小 G 和 KL 系数 β。

**任务复杂度边界**：K 步转移任务本质上是单步动作预测，无法直接建模多步规划和错误恢复。在 AndroidWorld 交互式基准上，即使最佳配置（GUI-Shift-Mimo-SFT, K=3）的 Pass@1 成功率也仅为 16.4%，Pass@5 最高 25.9%（Figure 2），与人类水平差距显著。这表明**学会预测单步 GUI 动态是必要但不充分的能力**，复杂任务仍需显式的规划或在线交互学习。

**奖励信号边界**：规则化奖励函数仅检查动作格式和坐标正确性（公式 3），无法捕获语义正确性。例如，在文本输入任务中输入错误内容仍可获得正奖励。这意味着 GUI-Shift 训练出的模型可能在需要精确语义理解的动作上存在系统偏差。

### 3. 已知局限

1. **数据来源单一**：训练数据仅来自 AndroidControl，限制了跨平台泛化能力。在 GUI Odyssey 平板测试上已观察到性能下降。

2. **规模未充分探索**：实验仅在 7-8B 参数 VLM 上进行，数据规模缩放实验（Figure 6）显示从 2K 增至 6K 样本仅有微弱上升趋势，暗示当前方法可能已接近该规模下的性能瓶颈。

3. **端到端性能不足**：未与在线交互式强化学习结合，AndroidWorld 的绝对成功率仍然较低，Pass@1 最高仅 16.4%。

4. **奖励函数粗糙**：主要依赖坐标和格式匹配，未建模语义正确性，可能导致模型在需要精确文本理解的动作上表现不佳。

5. **K 值需手动搜索**：最优 K 值因模型和任务而异（如 Qwen2.5-VL-7B 在 K=1 时最优，而 Mimo-VL-7B-SFT 在 K=3 时最优），缺乏自适应选择机制。

### 4. 开放问题

1. **大规模无标注轨迹收集**：如何自动化收集覆盖多平台（iOS、桌面、Web）、多应用的多样化 GUI 轨迹，以进一步扩展训练规模和分布覆盖？

2. **跨应用泛化**：K 步转移任务能否扩展到需要跨应用切换、多模态约束的复杂场景？当前训练轨迹主要来自单一应用内操作。

3. **语义奖励建模**：能否在不引入人工标注的前提下，设计更细粒度的奖励函数来捕获动作的语义正确性（如输入文本内容是否正确）？

4. **推理与效率的平衡**：GUI-Shift 移除推理链后训练时间减半且性能不降（Table 4），但对于需要多步规划的复杂任务，推理能力仍可能必要。能否在保持训练效率的同时，选择性引入推理能力？

5. **更大模型的扩展性**：该方法在 13B、70B 或专有 VLM（如 GPT-4o）上的效果如何？更大模型可能从自监督 GUI 动态学习中获益更多，也可能因更强的先验而减少对 K 步转移任务的依赖。

6. **在线交互式扩展**：能否将 GUI-Shift 的自监督预训练与在线 RL 的交互式微调结合，在 AndroidWorld 等复杂环境中实现更显著的端到端性能提升？



## 原文 PDF

![[paperPDFs/ICLR_2026/GUI_Shift_Enhancing_VLM_Based_GUI_Agents_through_Self_supervised_Reinforcement_Learning.pdf]]
