---
title: "EpiAgent: An Agent-Centric System for Ancient Inscription Restoration"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/EpiAgent_An_Agent_Centric_System_for_Ancient_Inscription_Restoration.pdf
project_link: null
code_link: "https://github.com/blackprotoss/EpiAgent"
aliases:
- EpiAgent
tags:
- CVPR_2026
- topic/other_unclear
- topic/other_unclear/general
core_operator: 将碑刻修复建模为分层规划问题，并模拟人类金石学家的闭环工作流（观察-构思-执行-再评估），利用LLM中央规划器动态协调多模态分析、历史经验、专业工具组合和多角度自优化。
primary_logic: 通过多模态感知建立结构化碑刻状态记录，蒸馏历史执行经验以引导工具的选择与编排，在字符级按需组合去噪、补全、模仿与检索工具，并通过文本真实性、风格一致性及专家反馈的迭代评估，在修复中实现视觉保真与语义真实的平衡。
claims:
- EpiAgent将碑刻修复形式化为分层规划问题，并遵循观察-构思-执行-再评估范式。
- 在真实退化碑刻测试集S上，EpiAgent在PSNR、SSIM、LPIPS、字符识别准确率等多个指标上全面超越所有基线方法。
- 人类专家偏好研究中，EpiAgent获得最高的Top-1排名比例（59.66%），显著优于其他方法。
- 消融实验证实，多模态分析、经验引导的自适应规划与多角度评估（含专家反馈）协同作用，共同构成EpiAgent卓越性能的支柱。
---

# EpiAgent: An Agent-Centric System for Ancient Inscription Restoration

> [!tip] 核心洞察
> 通过多模态感知建立结构化碑刻状态记录，蒸馏历史执行经验以引导工具的选择与编排，在字符级按需组合去噪、补全、模仿与检索工具，并通过文本真实性、风格一致性及专家反馈的迭代评估，在修复中实现视觉保真与语义真实的平衡。

| 字段 | 内容 |
|------|------|
| 中文题名 | EpiAgent：一种以智能体为中心的古代碑刻修复系统 |
| 英文题名 | EpiAgent: An Agent-Centric System for Ancient Inscription Restoration |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2604.09367) · [Code](https://github.com/blackprotoss/EpiAgent) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | EpiAgent |
| Dataset | Testing Set S, Testing Set R-I |

> [!tip] 效果简介
> - Testing Set S 上，PSNR 22.14 vs 21.15 (IR3) (+0.99)；SSIM 0.9684 vs 0.9599 (MambaIR) (+0.0085)；LPIPS 0.0254 vs 0.0361 (DocDiff) (-0.0107)。
> - Testing Set R-I 上，CLIP-IQA 0.9393 vs 0.9375 (DocDiff) (+0.0018)；End-to-End 1-NED 0.5766 vs 0.5539 (IR3) (+0.0227)。

## 概要

古代碑刻修复长期受困于一个核心瓶颈：**现有AI修复方法依赖固定pipeline，无法适应碑刻异构、多尺度、空间耦合的退化，且缺乏对文本语义真实性与书法风格一致性的考量，导致修复失真和过度/不足修复**。EpiAgent 针对这一问题，将碑刻修复重新建模为**分层规划问题**，模拟人类金石学家“观察—构思—执行—再评估”的闭环工作流，以LLM中央规划器动态协调多模态分析、历史经验、专业工具组合与多角度自优化。

在真实退化碑刻测试集S上，EpiAgent取得 **PSNR 22.14、SSIM 0.9684、LPIPS 0.0254**，字符识别Top-1准确率达 **0.9889**，End-to-End 1-NED达 **0.9069**，全面超越包括 **IR3**（Zhu et al., ACM Multimedia 2024）、**DocDiff**（Yang et al., ACM Multimedia 2023）、**MambaIR**（Guo et al., ECCV 2024）等在内的所有基线方法。人类专家偏好研究中，EpiAgent获得最高的Top-1排名比例 **59.66%**。消融实验进一步证实，多模态分析、经验引导的自适应规划与多角度评估（含专家反馈）的协同作用，共同构成其卓越性能的支柱。

古代碑刻是承载历史、文化与书法艺术的核心物质载体。然而，历经千年风化、侵蚀与人为损坏，现存碑刻普遍呈现高度异构、多尺度且空间耦合的退化模式——同一块石碑上可能同时存在表面噪声、笔划断裂、局部缺失乃至整字毁损。这种复杂的退化分布使得修复任务远非通用图像增强所能覆盖。

现有AI修复方法大多遵循**固定pipeline的单次前馈范式**，将修复视为从退化图像到干净图像的端到端映射。尽管在特定场景下取得了进展，但这类方法面临三个根本性缺口：

1. **退化适应性不足**：单一模型难以同时应对从轻微噪声到严重缺失的退化谱系，容易产生过度修复（抹去真实笔划）或修复不足（残留噪声与断裂）。
2. **语义与风格盲区**：像素级优化目标缺乏对文本语义真实性和书法风格一致性的显式建模，导致修复后的字符可能出现错字、形近字混淆或风格漂移。
3. **缺乏闭环校验**：现有方法缺少对修复结果的再评估与迭代修正机制，无法像人类金石学家那样通过“观察-构思-执行-再评估”的闭环逐步逼近最优修复。

值得注意的是，碑刻修复专用基线 **IR3**（Zhu et al., ACM Multimedia 2024）虽已尝试全局-局部框架，但仍受限于固定pipeline，在字符识别准确率（Top-1 Acc. 0.9626）和端到端1-NED（0.8855）等语义关键指标上存在明显天花板。

上述缺口共同指向一个核心瓶颈：**碑刻修复需要一种能够动态感知退化状态、按需调度专业化工具、并在语义与视觉双重约束下迭代自优化的智能系统**。这正是EpiAgent的设计动机——将碑刻修复重新建模为分层规划问题，以LLM中央规划器驱动多模态分析、历史经验蒸馏、可组合工具调用与多角度自优化，在视觉保真与语义真实之间寻求平衡。

## 核心方法与创新机理

### 1. 修复范式的根本转变：从单次前馈到分层闭环规划

现有碑刻修复方法（如 **IR3** (Zhu et al., ACM Multimedia 2024)、**DocDiff** (Yang et al., ACM Multimedia 2023)、**GSDM** (Zhu et al., AAAI 2024) 等）均采用**单次前馈的图像到图像转换 pipeline**：输入退化碑刻图像，直接输出修复结果。这种固定范式隐含两个脆弱假设——退化模式可被单一模型充分建模，且修复是一次性完成的确定性过程。然而，古代碑刻的退化具有**异构、多尺度、空间耦合**的特点，同一碑面上可能同时存在表面噪声、笔划断裂、区域缺失和严重风化，单一模型难以在所有退化类型上同时达到最优。

EpiAgent 的核心范式转变在于将碑刻修复**形式化为分层规划问题**，并模拟人类金石学家的**观察-构思-执行-再评估（Observe–Conceive–Execute–Reevaluate）闭环工作流**。具体而言：

- **观察（Observe）**：通过多模态感知建立结构化的碑刻状态记录，而非直接进行像素映射；
- **构思（Conceive）**：由 LLM 中央规划器（**Kimi-K2**）根据观察记录与蒸馏的历史经验先验，动态生成每个字符的有序工具序列计划；
- **执行（Execute）**：按计划调用可组合的专业化工具包，逐字符进行修复；
- **再评估（Reevaluate）**：从文本真实性、风格一致性和专家反馈多角度评估修复结果，识别失败字符并触发重规划。

这一范式的关键突破在于：**修复策略在推理过程中动态更新，而非由静态先验固定**（"the strategy is dynamically updated during inference rather than fixed by a static prior"）。这使得系统能够根据每个字符的实际退化程度和修复反馈自适应调整工具组合，从根本上解决了固定 pipeline 在面对异构退化时的"一刀切"问题。

### 2. 工具使用的质变：从单一模型到可组合的专业化工具包

基线方法依赖单一图像修复模型处理所有退化类型。例如，**Restormer** (Zamir et al., CVPR 2022) 和 **MambaIR** (Guo et al., ECCV 2024) 虽在通用图像修复上表现优异，但缺乏对碑刻文本语义和书法结构的专门建模；**CharFormer** (Shi et al., ACM Multimedia 2022) 虽针对字符级去噪，但无法处理严重缺失和跨字符风格一致性问题。

EpiAgent 将修复能力**解耦为四个专业化工具**，由规划器按需动态调度：

- **背景去噪（Background Denoising, $f_{\text{den}}$）**：以退化分割掩码 $S_d$ 为条件，通过掩蔽扩散去除表面噪声，同时保护笔划结构；
- **笔划补全（Stroke Completion, $f_{\text{inp}}$）**：针对 $S_d$ 标识的缺失或严重退化区域进行定向修复；
- **字体模仿（Font Imitation, $f_{\text{imi}}$）**：从同一碑刻的高质量范例中学习风格先验，合成风格一致的字形；
- **字符检索（Character Retrieval, $f_{\text{ret}}$）**：作为后备机制，在碑刻内部搜索相同字符以替换不可修复的字符，避免引入风格漂移。

这一设计的核心洞察在于：**不同退化类型需要不同的修复策略，而同一字符可能需要多种工具的组合**。规划器为每个字符 $c$ 生成有序的工具序列 $P_c = \pi(T_r, T_e, c) = (f_1^{(c)}, f_2^{(c)}, ..., f_{N_c}^{(c)})$，然后按序执行：

$$\hat{I}^{(k)}[c] = f_{N_c}^{(c)} \circ \cdots \circ f_{1}^{(c)}(\hat{I}^{(k-1)}[c]), \quad \forall c \in \mathcal{C}$$

消融实验（Table 4）证实，这种**经验引导的自适应规划**在 PSNR（22.14）、SSIM（0.9684）、LPIPS（0.0254）和 1-NED（0.9069）上全面优于随机工具调用和两种固定方案（Scheme A: 去噪-补全；Scheme B: 去噪-补全-模仿），说明工具组合的动态编排而非工具本身的数量是性能提升的关键。

### 3. 评估维度的拓展：从像素级质量到多角度语义-视觉协同

基线方法的评估（和训练目标）局限于**像素级图像质量**（如 PSNR、SSIM），这无法捕捉碑刻修复的两个核心需求：**文本语义的真实性**（修复后的字符是否可正确识别）和**书法风格的一致性**（修复后的字形是否与同碑其他字符风格协调）。

EpiAgent 在每次执行后引入**多角度评估**，包含三个维度：

- **文本真实性度量**：$M_t^{(k)}(c) = 1 - \text{CER}(\text{OCR}(\hat{I}^{(k)}[c]), \hat{\mathcal{H}}[c]) \in [0,1]$，通过 OCR 识别结果与校正文本之间的字符错误率量化语义准确性；
- **风格一致性度量**：$M_s^{(k)}(c) = \text{CosSim}(\phi(\hat{I}^{(k)}[c]), \phi_{\text{ref}}) \in [0,1]$，计算当前字符特征与参考风格特征的余弦相似度；
- **专家反馈**：引入人类金石学家的审查意见作为最高层级的质量判断。

失败字符集合 $\mathcal{F}^{(k)}$ 由未通过幻觉检查、文本真实性低于阈值 $\tau_t$ 或风格一致性低于阈值 $\tau_s$ 的字符构成，规划器据此生成聚焦于失败字符的修订计划 $\mathcal{P}^{(k+1)}$。消融实验（Table 5）表明，逐一增加文本真实性、风格一致性和专家反馈均带来增益，其中加入专家反馈后修复质量达到最高，证实了多维度协同评估对闭环优化的关键作用。

### 4. 创新总结

EpiAgent 的三项 changed slots 构成了一个**相互增强的创新链条**：闭环范式提供了动态调度的框架，可组合工具包提供了精细化的执行能力，多角度评估提供了超越像素的反馈信号。这一链条的核心驱动是**LLM 作为中央规划器**对多模态感知、历史经验和专业工具的协调能力，使得系统能够在视觉保真与语义真实之间取得平衡——这正是现有方法长期未能解决的瓶颈。

EpiAgent 将古代碑刻修复形式化为一个**分层规划问题**，并模拟人类金石学家“观察—构思—执行—再评估”的闭环工作流。整个系统围绕一个基于 LLM 的中央规划器构建，动态协调多模态感知、历史经验蒸馏、专业化工具组合与迭代自优化，从而应对碑刻退化中异构、多尺度、空间耦合的复杂挑战。

### 四阶段闭环范式

系统遵循 **Observe → Conceive → Execute → Reevaluate** 四个阶段，并在满足终止条件前迭代执行：

1. **Observe（观察）**：通过多模态大语言模型（MLLM）与专用视觉/文本精炼模块，构建结构化的碑刻状态记录 $T_r$，包括初始布局、文本假设、精确字符位置、像素级退化分割掩码及严重程度分级。
2. **Conceive（构思）**：中央规划器 $\pi$（基于 Kimi-K2 LLM）综合观察记录 $T_r$ 与蒸馏的历史经验先验 $T_e$，为每个字符 $c$ 动态生成有序的工具序列计划：
   $$P_{c} = \pi(T_{r}, T_{e}, c) = (f_{1}^{(c)}, f_{2}^{(c)}, ..., f_{N_{c}}^{(c)})$$
3. **Execute（执行）**：按计划对每个字符依次调用可组合的专业化工具包（背景去噪、笔划补全、字体模仿、字符检索），生成当前迭代的修复结果：
   $$\hat{I}^{(k)}[c] = f_{N_{c}}^{(c)} \circ \cdots \circ f_{1}^{(c)}(\hat{I}^{(k-1)}[c]), \quad \forall c \in \mathcal{C}$$
4. **Reevaluate（再评估）**：引入多角度评估——文本真实性（$M_t^{(k)}$，基于 OCR 字符错误率）、风格一致性（$M_s^{(k)}$，基于特征余弦相似度）及专家反馈——识别失败字符集合 $\mathcal{F}^{(k)}$，并触发下一轮重规划。

### 核心模块与数据流

Figure 2 展示了 EpiAgent 的整体框架，其关键模块与输入输出流如下：

![[assets/figures/papers/paper_list_l2476_https_arxiv_org_abs_2604_09367/figures/002_Figure_2.jpg]]
*Figure 2: Illustration of the EpiAgent framework, which mimics the restoration workflow of human epigraphers*

- **多模态感知层**：MLLM 生成初始布局与文本假设；CLM（校正语言模型）结合 RAG 检索大规模中文语料库，纠正识别结果；LRM（布局修正模块）预测精确字符位置，处理缺失区域；DAM（退化评估模块）输出像素级退化掩码与严重程度分级。
- **中央规划器**：以观察记录 $T_r$ 和经验先验 $T_e$ 为输入，输出每字符的工具序列计划，并在再评估阶段根据失败字符集 $\mathcal{F}^{(k)}$ 动态更新策略。
- **专业化工具包**：包含背景去噪（掩蔽扩散，保护笔划结构）、笔划补全（定向修复严重退化区域）、字体模仿（学习同一碑刻高质量范例的风格先验）、字符检索（回溯搜索相同字符作为后备，避免风格漂移）。
- **多角度评估与经验存储**：文本真实性度量、风格一致性度量与专家审查共同构成终止判断依据；成功的修复经验与反思经验被存储，用于后续规划的引导与效率提升。

### 与传统方法的本质区别

与现有依赖单次前馈图像到图像转换的固定 pipeline 不同，EpiAgent 的核心突破在于将修复过程从“静态模型推理”转变为“**LLM 驱动的动态规划与工具编排**”。这种范式转换使得系统能够根据每个字符的具体退化类型与严重程度，按需组合去噪、补全、模仿与检索操作，并在文本语义真实性与书法风格一致性之间取得平衡——这正是传统像素级修复方法所缺失的关键能力。

### 3.1 观察阶段：多模态感知与结构化记录

EpiAgent将碑刻修复形式化为分层规划问题，其观察阶段通过**两步方案**构建全面的结构化记录 $T_r$，为下游规划提供信息基础。

**第一步：通用多模态感知。** 采用多模态大语言模型（MLLM）对输入的退化碑刻图像 $I$ 进行全局感知，生成初始布局 $O$ 与文本假设 $\mathcal{H}$。这一步获取碑刻的整体空间结构和对文字内容的初步理解。

**第二步：专业化视觉与文本精炼。** 在MLLM的粗粒度感知基础上，引入三个专用模块进行精细化修正：
- **布局修正模块（LRM）**：消费 $O$ 与校正后的文本假设 $\hat{\mathcal{H}}$，预测精确的字符位置，并处理因严重退化导致的缺失区域。
- **退化评估模块（DAM）**：生成像素级退化分割掩码 $S_d$，并对每个字符区域赋予离散的严重程度分级（L1–L3），为后续工具选择提供退化程度的量化依据。
- **校正语言模型（CLM）与检索增强生成（RAG）**：CLM经微调后，结合RAG机制查询大规模中文语料库，对MLLM的初始文本识别结果进行语义校正，输出修正后的文本假设 $\hat{\mathcal{H}}$。

观察阶段最终产出的结构化记录 $T_r$ 包含布局信息、退化掩码与严重程度、校正后的文本假设，共同构成规划器进行决策的“碑刻状态描述”。

### 3.2 构思阶段：经验引导的自适应规划

规划的核心由一个基于LLM的中央规划器 $\pi$ 完成，具体实现为**Kimi-K2**。规划器接收观察记录 $T_r$ 和历史经验先验 $T_e$，为每个字符 $c$ 动态生成有序的工具调用序列：

$$P_c = \pi(T_r, T_e, c) = (f_1^{(c)}, f_2^{(c)}, \ldots, f_{N_c}^{(c)})$$

其中：
- $T_r$ 为观察阶段产出的结构化记录（布局、退化掩码、校正文本）；
- $T_e$ 为从历史修复案例中蒸馏的经验先验，引导工具的选择与编排；
- $P_c$ 为字符 $c$ 的工具序列，$f_i^{(c)}$ 为序列中第 $i$ 个被调用的专业化工具，$N_c$ 为该字符的工具数量。

经验先验 $T_e$ 的核心作用在于：根据退化严重程度和字符特征，蒸馏出最优的工具组合模式，避免盲目调用所有工具或采用固定流水线。当面对严重退化（L3）的字符时，规划器倾向于调用更完整的工具链（去噪→补全→模仿或检索）；而对轻微退化（L1）的字符，则仅需少量工具即可完成修复。

### 3.3 执行阶段：专业化工具包与逐字符迭代

执行阶段将规划 $P$ 实例化为可组合的工具包 $\mathcal{F}$，包含四类专业化工具：

| 工具 | 符号 | 功能 |
|------|------|------|
| 背景去噪 | $f_{den}$ | 以退化掩码 $S_d$ 为条件，通过掩蔽扩散去除表面噪声，同时保护笔划结构 |
| 笔划补全 | $f_{inp}$ | 针对 $S_d$ 指示的缺失或严重退化区域进行定向修复 |
| 字体模仿 | $f_{imi}$ | 从同一碑刻的高质量范例中学习风格先验，合成风格一致的字形 |
| 字符检索 | $f_{ret}$ | 在图像 $I$ 内部回溯搜索相同字符，替换无法修复的字符以避免风格漂移 |

在第 $k$ 次迭代中，对每个字符 $c \in \mathcal{C}$ 按其工具序列依次应用操作：

$$\hat{I}^{(k)}[c] = f_{N_c}^{(c)} \circ \cdots \circ f_{1}^{(c)}\big(\hat{I}^{(k-1)}[c]\big), \quad \forall c \in \mathcal{C}$$

其中 $\hat{I}^{(k-1)}$ 为上一轮迭代的修复结果，$\hat{I}^{(k)}$ 为当前轮次的输出。工具按序复合，前一个工具的输出作为后一个工具的输入，形成级联修复流水线。

### 3.4 再评估阶段：多角度度量与失败字符重规划

为同时保证文本真实性与视觉和谐，每次执行后引入多角度评估指标：

**文本真实性度量：**
$$M_t^{(k)}(c) = 1 - \text{CER}\big(\text{OCR}(\hat{I}^{(k)}[c]), \hat{\mathcal{H}}[c]\big) \in [0,1]$$

通过OCR识别当前修复字符，与校正文本 $\hat{\mathcal{H}}[c]$ 计算字符错误率（CER），量化语义准确性。值越接近1表示文本还原越准确。

**风格一致性度量：**
$$M_s^{(k)}(c) = \text{CosSim}\big(\phi(\hat{I}^{(k)}[c]), \phi_{ref}\big) \in [0,1]$$

计算当前修复字符的特征嵌入 $\phi(\hat{I}^{(k)}[c])$ 与参考风格特征 $\phi_{ref}$ 之间的余弦相似度，衡量书法风格的一致性。

**失败字符集合：**
$$\mathcal{F}^{(k)} = \big\{ c \in \mathcal{C} \mid (M_h^{(k)}(c) = 0) \vee (M_t^{(k)}(c) < \tau_t) \vee (M_s^{(k)}(c) < \tau_s) \big\}$$

其中 $M_h^{(k)}(c)$ 为幻觉检查（检测生成内容是否与原文无关），$\tau_t$ 和 $\tau_s$ 分别为文本真实性与风格一致性的预设阈值。任一条件不满足的字符被归入失败集 $\mathcal{F}^{(k)}$。

规划器 $\pi$ 使用 $\mathcal{F}^{(k)}$、$T_r$ 和 $T_e$ 生成针对失败字符的修正计划 $\mathcal{P}^{(k+1)}$，触发下一轮迭代。该闭环机制使修复策略在推理过程中动态更新，而非受限于静态先验。

![[assets/figures/papers/paper_list_l2476_https_arxiv_org_abs_2604_09367/figures/008_Figure_6.jpg]]
*Figure 6: Exemplary comparison between different tool invocation sequences faced with (a) severely degraded (L3) and (b) slightly degraded (L1) character blocks. The green lines mark the optimal restoring sequence*

## 实验与关键发现

### 主实验结果

EpiAgent 在三个不同退化程度的碑刻测试集（Testing Set S, R-I, R-II）上，与八种最新的基线方法进行了全面定量比较，涵盖像素级保真度、感知质量和字符识别准确率多个维度。基线方法包括通用图像修复模型 **Restormer**（Zamir et al., CVPR 2022）、**MambaIR**（Guo et al., ECCV 2024）、**PromptIR**（Potlapalli et al., NeurIPS 2023）、**MoCE-IR**（Zamfir et al., CVPR 2025），文档/文本图像修复模型 **CharFormer**（Shi et al., ACM Multimedia 2022）、**DocDiff**（Yang et al., ACM Multimedia 2023）、**GSDM**（Zhu et al., AAAI 2024），以及碑刻修复专用方法 **IR3**（Zhu et al., ACM Multimedia 2024）。

在真实退化碑刻测试集 S 上，EpiAgent 在所有指标上均取得最优结果，如表1所示。具体而言，PSNR 达到 22.14，较次优方法 IR3（21.15）提升 0.99 dB；SSIM 为 0.9684，超过 MambaIR（0.9599）；LPIPS 降至 0.0254，显著优于 DocDiff（0.0361）。在语义层面，字符识别 Top-1 准确率高达 0.9889，端到端 1-NED 达到 0.9069，分别领先 IR3 0.0263 和 0.0214。这表明 EpiAgent 不仅在像素重建上更精确，在保持文本可读性方面也具有显著优势。

在模拟退化测试集 R-I 和 R-II 上，EpiAgent 同样展现出领先性能。在 R-I 上，CLIP-IQA 达到 0.9393，端到端 1-NED 为 0.5766；在 R-II 上，各指标也保持稳定优势。值得注意的是，在无参考感知质量指标（CLIP-IQA、MUSIQ、MANIQA、NIMA）上，EpiAgent 的优势虽不如像素级指标显著，但依然保持领先或次优，说明其修复结果在人类感知层面同样具有竞争力。

### 人类专家偏好研究

为评估修复结果的主观质量，研究邀请了 18 位具有书法或碑刻知识的人类专家进行盲评，按 Top-1 排名统计偏好。如表2所示，EpiAgent 获得了 59.66% 的 Top-1 排名比例，远超所有基线方法。这一结果表明，EpiAgent 的修复结果在视觉保真度和书法风格一致性上更符合人类金石学家的审美标准。

### 消融实验

消融实验从三个维度系统验证了 EpiAgent 各核心组件的贡献。

**多模态分析模块。** 观察阶段的分析能力是整个系统的基础。如表3所示，逐步添加 MLLM 通用感知、CLM 文本校正和 RAG 检索增强模块，字符识别准确率（1-NED）在三个测试集上持续提升。其中，添加 RAG 后 1-NED 在 Set S、R-I、R-II 上分别达到 0.9742、0.9694、0.9606，均为最优。这验证了检索增强的文本校正对碑刻内容理解的关键作用——古代碑刻常含生僻字和异体字，通用 OCR 模型容易出错，RAG 通过查询大规模中文语料库有效纠正了识别结果。

**规划策略。** 构思阶段的工具调度策略对修复质量影响显著。如表4所示，经验引导的自适应规划（Experience-guided）在 PSNR（22.14）、SSIM（0.9684）、LPIPS（0.0254）和 1-NED（0.9069）上全面优于随机工具调用和两种固定方案（Scheme A：去噪-补全；Scheme B：去噪-补全-模仿）。这一结果表明，蒸馏历史执行经验来引导工具的选择与编排，能够根据字符的具体退化状态动态调整修复策略，避免固定流水线带来的过度修复或修复不足。

**多角度评估。** 再评估阶段的多角度反馈机制对修复质量的迭代提升至关重要。如表5所示，逐一引入文本真实性度量、风格一致性度量和专家反馈，修复指标逐步提高。当三者全部启用时，PSNR、SSIM 等指标达到最高。这说明仅靠像素级损失函数无法保证语义正确性和风格和谐性，多角度评估为规划器提供了精准的重规划信号。

此外，移除反思经验存储机制会明显增加平均修复时间并降低修复质量（CLIP-IQA），如图8所示。这表明累积的反思经验具有可复用价值，能够加速后续修复并提升效果。

### 定性分析

图5展示了不同方法在真实退化碑刻上的修复结果对比。在严重退化区域（如大面积剥落、笔划断裂），固定流水线方法往往产生模糊或失真的修复，而 EpiAgent 通过自适应工具组合（如对严重退化字符调用字体模仿或字符检索）能够生成清晰且风格一致的笔划。图6进一步揭示了规划策略的适应性：对于严重退化（L3）字符，最优序列为“去噪→补全→模仿”；对于轻微退化（L1）字符，仅需“去噪”即可。图7对比了不同退化程度下各修复工具的输出，EpiAgent 选择的工具与人类专家偏好高度一致（紫色边框标记），验证了经验引导规划的有效性。

![[assets/figures/papers/paper_list_l2476_https_arxiv_org_abs_2604_09367/figures/005_Table_1.jpg]]
*Table 1: Inscription image restoration results on Testing Set S, R-I, and R-II. Comparison with state-of-the-art methods. The best and the second-best results are highlighted and underlined*

![[assets/figures/papers/paper_list_l2476_https_arxiv_org_abs_2604_09367/figures/009_Table_3.jpg]]
*Table 3: Ablation studies of the analysis modules used in the Observation stage. The best and the second-best results are highlighted and underlined*

![[assets/figures/papers/paper_list_l2476_https_arxiv_org_abs_2604_09367/figures/010_Table_4.jpg]]
*Table 4: Ablation study of different planning strategies for inscription restoration. “Random” refers to random tool invocation from the toolkit. “Fixed” denotes predefined Scheme A (Denoising-Completion) and Scheme B (Denoising-Completion-Imitation). “Experience-guided” customizes the restoration scheme based on distilled experience priors. The best and the second best results are highlighted and underlined*

![[assets/figures/papers/paper_list_l2476_https_arxiv_org_abs_2604_09367/figures/011_Table_5.jpg]]
*Table 5: Ablation studies of multi-perspective evaluation module. The best and the second best results are highlighted and underlined*

## 定位与知识库关联

### 1. 核心范式转换：从固定管线到智能体闭环

EpiAgent 与现有基线方法之间存在一条清晰的范式分界线。所有基线方法——无论是通用图像修复模型还是碑刻专用方法——均遵循**单次前馈图像到图像转换**范式：输入退化碑刻图像，输出修复后图像，整个流程由固定的神经网络参数决定，不具备对退化类型、字符语义或书法风格的动态感知与自适应能力。具体而言：

- **通用修复模型**（**Restormer**，Zamir et al., CVPR 2022；**MambaIR**，Guo et al., ECCV 2024；**PromptIR**，Potlapalli et al., NeurIPS 2023；**MoCE-IR**，Zamfir et al., CVPR 2025）将碑刻修复视为与自然图像去噪/超分同质的像素映射问题，缺乏对古文字结构与语义的专门建模。
- **文档/文本图像修复模型**（**CharFormer**，Shi et al., ACM Multimedia 2022；**DocDiff**，Yang et al., ACM Multimedia 2023；**GSDM**，Zhu et al., AAAI 2024）引入了文本感知或结构引导，但仍以单模型端到端映射为核心，无法处理碑刻中常见的异构退化（风化、剥落、污损）在空间上的耦合分布。
- **碑刻专用方法** **IR3**（Zhu et al., ACM Multimedia 2024）采用全局-局部框架，是基线中最具针对性的工作，但其修复策略仍是静态的，无法根据每个字符的实际退化状态动态调整工具组合。

EpiAgent 的范式转换体现在将碑刻修复重新定义为**分层规划问题**，并模拟人类金石学家的**观察-构思-执行-再评估（Observe–Conceive–Execute–Reevaluate）**闭环工作流。这一转换的实质是将修复过程从“模型参数决定”升级为“LLM中央规划器动态决策”，使系统具备了对异构退化的自适应能力和对修复质量的迭代自优化能力。

### 2. 方法谱系中的位置：多智能体与多模态修复的交汇点

EpiAgent 处于以下几条研究脉络的交汇处：

**脉络一：LLM驱动的智能体系统。** EpiAgent 以 Kimi-K2 作为中央规划器，将LLM的推理与规划能力引入图像修复领域。这与近期利用LLM进行视觉任务规划的工作一脉相承，但EpiAgent的独特之处在于将规划粒度细化到**字符级**，并为每个字符生成有序的工具调用序列 $P_{c} = \pi(T_{r}, T_{e}, c) = (f_{1}^{(c)}, f_{2}^{(c)}, ..., f_{N_{c}}^{(c)})$。

**脉络二：可组合的专业化工具包。** 与依赖单一修复模型的方法不同，EpiAgent 构建了包含背景去噪（$f_{den}$）、笔划补全（$f_{inp}$）、字体模仿（$f_{imi}$）和字符检索（$f_{ret}$）四种专业化工具的工具包。这些工具按需组合，由规划器根据退化评估模块（DAM）生成的像素级退化分割掩码 $S_d$ 和严重程度分级动态调度，实现了“对症下药”的修复策略。

**脉络三：多模态感知与文本语义闭环。** EpiAgent 在观察阶段通过 MLLM、CLM（带RAG的校正语言模型）和 LRM 建立结构化的碑刻状态记录，将视觉感知与中文语料库检索相融合。这一设计使系统能够在修复过程中保持文本语义的真实性——这是所有纯视觉修复基线方法所不具备的能力。

### 3. 适用边界与局限

基于论文提供的证据和分析，EpiAgent 的适用边界和潜在局限可归纳如下：

**已知优势边界：**
- 在真实退化碑刻测试集上，EpiAgent 在PSNR（22.14）、SSIM（0.9684）、LPIPS（0.0254）和字符识别准确率（Top-1 Acc. 0.9889）上全面超越所有基线方法（Table 1）。
- 人类专家偏好研究中，EpiAgent 获得59.66%的Top-1排名比例，显著优于其他方法（Table 2），表明其修复结果在视觉保真度和书法风格一致性上更符合金石学家的审美标准。
- 消融实验证实，多模态分析、经验引导的自适应规划与多角度评估（含专家反馈）三者协同作用，共同构成系统卓越性能的支柱（Tables 3-5）。

**需要人工验证的潜在局限：**
- 论文未报告EpiAgent在完全陌生的刻石或罕见古文字变体上的泛化表现，其对分布外退化类型的鲁棒性尚待验证。
- 历史经验先验 $T_e$ 的跨碑刻迁移能力未被系统评估——当前经验蒸馏是否依赖于同一碑刻或同一书体的高质量范例，需要进一步确认。
- 系统依赖专家反馈作为多角度评估的组成部分，在无专家可用的场景下，如何替代人类评审以维持修复质量，仍是一个开放问题。
- 移除反思经验存储机制会明显增加平均修复时间并降低修复质量（Fig. 8），但论文未讨论该机制在大规模部署时的存储与检索开销。

### 4. 开放问题与后续方向

EpiAgent 开辟了智能体驱动的文化遗产修复新范式，同时揭示了若干值得后续探索的方向：

1. **跨碑刻迁移与零样本泛化：** 当面对与训练数据书体、时代、刻工风格迥异的碑刻时，现有的经验先验和字体模仿模块能否保持稳定规划？这需要构建跨碑刻的测试基准进行系统验证。

2. **自主化专家反馈：** 能否训练一个模拟金石学家审美判断的评估模型，替代人类专家反馈，使EpiAgent实现完全自主的闭环修复？这涉及书法风格度量的细粒度建模和专家知识的系统化编码。

3. **罕见字与异体字处理：** 当字符检索模块（$f_{ret}$）无法在同一碑刻中找到相同字符，且字体模仿缺乏足够范例时，系统如何处理罕见字或异体字的修复？这可能需要引入跨碑刻的字体风格解耦与迁移技术。

4. **效率与可部署性：** EpiAgent 的迭代式闭环修复和LLM推理引入了显著的计算开销。如何在保持修复质量的前提下压缩规划与评估的推理成本，是实际部署中必须解决的问题。

## 原文 PDF

![[paperPDFs/CVPR_2026/EpiAgent_An_Agent_Centric_System_for_Ancient_Inscription_Restoration.pdf]]
