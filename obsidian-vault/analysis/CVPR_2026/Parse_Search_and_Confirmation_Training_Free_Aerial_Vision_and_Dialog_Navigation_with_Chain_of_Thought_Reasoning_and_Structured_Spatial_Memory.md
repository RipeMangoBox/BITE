---
title: "Parse, Search, and Confirmation: Training-Free Aerial Vision-and-Dialog Navigation with Chain-of-Thought Reasoning and Structured Spatial Memory"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Parse_Search_and_Confirmation_Training_Free_Aerial_Vision_and_Dialog_Navigation_with_Chain_of_Thought_Reasoning_and_Structured_Spatial_Memory.pdf
project_link: null
code_link: "https://github.com/QY6616/PSC-AVDN"
aliases:
- PSCTFAVDNCTR
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过三阶段解析-搜索-确认流程将方向理解与高空目标定位解耦，并结合结构化空间记忆补充空间上下文。
primary_logic: 将模糊的对话指令解析为明确的几何方向与目标描述，通过思维链逐步搜索候选区域，再利用细粒度确认消除视觉歧义，并利用多尺度视觉观察、空间视觉记忆和结构化几何记忆为推理提供全局空间上下文和长期一致性。
claims:
- PSC-AVDN在ANDH和ANDH-Full数据集上达到训练免设置下的最优性能，匹配或超过多个微调方法。
- 消融实验表明三阶段推理逐步提升性能，SSM模块各组件均有贡献。
- GPT-4o naive baseline在ANDH Unseen Val上SPL仅3.4，SR 3.9，而PSC-AVDN达到SPL 17.8，SR 22.6。
- ANDH Unseen Val 上 SPL = 17.8
---

# Parse, Search, and Confirmation: Training-Free Aerial Vision-and-Dialog Navigation with Chain-of-Thought Reasoning and Structured Spatial Memory

> [!tip] 核心洞察
> 将模糊的对话指令解析为明确的几何方向与目标描述，通过思维链逐步搜索候选区域，再利用细粒度确认消除视觉歧义，并利用多尺度视觉观察、空间视觉记忆和结构化几何记忆为推理提供全局空间上下文和长期一致性。

| 字段 | 内容 |
|------|------|
| 中文题名 | 解析、搜索与确认：基于思维链推理和结构化空间记忆的训练免空中视觉对话导航 |
| 英文题名 | Parse, Search, and Confirmation: Training-Free Aerial Vision-and-Dialog Navigation with Chain-of-Thought Reasoning and Structured Spatial Memory |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Qi_Parse_Search_and_Confirmation_Training-Free_Aerial_Vision-and-Dialog_Navigation_with_Chain-of-Thought_CVPR_2026_paper.html) · [Code](https://github.com/QY6616/PSC-AVDN) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | PSC-AVDN |
| Dataset | ANDH Unseen Val, ANDH-Full Unseen Val |

> [!tip] 效果简介
> - ANDH Unseen Val 上，SPL 17.8 vs 3.4 (+14.4)；SR 22.6 vs 3.9 (+18.7)；GP 39.2 vs -11.8 (+51.0)。
> - ANDH-Full Unseen Val 上，SPL 12.4 vs N/A (GPT-4o not reported) (N/A)；SR 15.4 vs N/A (N/A)；GP 62.3 vs N/A (N/A)。

## 概述

空中视觉对话导航（Aerial Vision-and-Dialog Navigation, AVDN）要求无人机在对话交互中理解人类指令，在高空遥感影像中定位并导航至目标区域。现有方法面临两个核心瓶颈：其一，**多模态大语言模型（MLLM）在高空视角下缺乏鲁棒的空间定位和场景理解能力**，难以将模糊的方向短语（如“10点钟方向”）转化为精确的几何约束；其二，**模型缺乏全局空间理解与时间状态跟踪**，导致导航过程不可靠，容易误停或漏检。

针对上述问题，本文提出 **PSC-AVDN**，一个训练免的空中视觉对话导航框架。其核心洞察在于：将模糊的对话指令解析为明确的几何方向与目标描述，通过思维链逐步搜索候选区域，再利用细粒度确认消除视觉歧义；同时，利用多尺度视觉观察、空间视觉记忆和结构化几何记忆为推理提供全局空间上下文和长期一致性。具体而言，PSC-AVDN 耦合了一个**三阶段解析-搜索-确认（Parsing-Search-Confirmation）推理流水线**与一个**结构化空间记忆模块（Structured Spatial Memory, SSM）**：

- **解析阶段**：利用大语言模型将模糊对话指令转换为稳定的几何方向与目标描述，通过航向解析模块统一为绝对角度表示。
- **搜索阶段**：通过搜索思维链（S-CoT）逐步分析目的地、理解场景、生成参考网格地图并定位候选区域，逐步缩小搜索范围。
- **确认阶段**：通过确认思维链（C-CoT）对候选区域进行细粒度验证，检查空间与关系约束，消除视觉歧义并锁定唯一目标位置。
- **SSM 模块**：集成多尺度视觉观察（MVO）、空间视觉记忆（SVM）和结构化几何记忆（SGM），为搜索和确认阶段补充全局空间上下文与历史信息。

在 ANDH 和 ANDH-Full 数据集上，PSC-AVDN 在训练免设置下达到最优性能，匹配甚至超过多个监督微调方法（如 **FELA w/ attn**（Su et al., AAAI 2025）、**NavAgent**（Liu et al., arXiv 2024）和 **OpenFly**（Gao et al., arXiv 2025））。以 ANDH Unseen Val 为例，PSC-AVDN 的 SPL 达到 17.8、SR 达到 22.6、GP 达到 39.2，相较 GPT-4o 朴素基线（SPL 3.4, SR 3.9, GP -11.8）有大幅提升。消融实验表明，三阶段推理各步骤逐步提升性能，SSM 模块中 SVM、MVO 和 SGM 三者联合贡献显著，5×5 参考网格尺寸与缩放因子组合 (3,5,7) 为最优配置。

## 背景与动机

空中视觉对话导航（Aerial Vision-and-Dialog Navigation, AVDN）要求无人机根据自然语言对话指令，在高空遥感视角下定位并导航至指定目标区域。与传统地面视觉导航不同，AVDN面临两个核心挑战：其一，对话指令中常包含模糊的方向描述（如“10点钟方向”），缺乏精确的几何参照；其二，高空俯视影像与地面训练数据之间存在显著的域差异，导致依赖地面数据训练的模型难以迁移。

现有方法主要依赖监督微调策略。例如，**FELA w/ attn**（Su et al., AAAI 2025）和**NavAgent**（Liu et al., arXiv 2024）通过任务特定训练数据学习导航策略，**OpenFly**（Gao et al., arXiv 2025）则在仿真环境中进行端到端监督训练。这些方法虽然取得了一定效果，但需要大量标注数据，且泛化能力受限于训练场景。在训练免（training-free）设置下，直接使用多模态大语言模型（MLLM）的基线方法（如GPT-4o）表现极差：在ANDH Unseen Val上，GPT-4o仅取得SPL 3.4、SR 3.9、GP -11.8（Table 1），几乎无法完成有效导航。

MLLM基线失效的根本原因可归结为三个层面：**方向理解歧义**——模型无法将“10点钟方向”等口语化描述可靠地转换为无人机当前航向下的绝对角度；**空间定位不可靠**——高空影像缺乏地面特征，模型难以建立精确的空间对应关系；**缺乏全局上下文与历史记忆**——模型孤立处理每帧图像，无法利用历史轨迹和已探索区域的全局空间信息，导致导航决策缺乏时间一致性。

针对上述瓶颈，PSC-AVDN提出了一条训练免的技术路径，其核心洞察是：将模糊的对话指令解析为明确的几何方向与目标描述，通过思维链逐步搜索候选区域，再利用细粒度确认消除视觉歧义，并利用多尺度视觉观察、空间视觉记忆和结构化几何记忆为推理提供全局空间上下文和长期一致性。这一设计使得模型无需任何任务特定训练数据，即可在ANDH和ANDH-Full数据集上达到甚至超越多个监督微调方法的性能水平（Table 1）。

## 核心创新

PSC-AVDN的核心创新在于将空中视觉对话导航分解为“解析—搜索—确认”三阶段推理流程，并与结构化空间记忆（SSM）深度耦合，从而在训练免（training-free）设置下解决了MLLM在高空视角下的三个根本性缺陷：方向歧义、缺乏结构化搜索策略、以及空间上下文缺失。

### 从模糊指令到几何方向：解析阶段的结构化映射

MLLM基线（如GPT-4o）直接解释“10 o'clock”等模糊方向短语时，由于高空影像与地面训练数据之间存在领域鸿沟，定位精度极低（ANDH Unseen Val上SPL仅3.4，SR仅3.9）。PSC-AVDN在解析阶段引入航向解析模块，将LLM提取的方向与目标描述转换为统一的绝对角度表示（如237°），并通过相对航向公式 $\delta = \mathrm{wrap}(\alpha - \phi)$ 将绝对方向角与UAV当前方位角关联，归一化至$[0, 2\pi)$。这一设计消除了方向歧义，为后续搜索提供了稳定的几何约束。

### 从盲目迭代到思维链引导：搜索阶段的逐步候选缩小

基线方法在每帧孤立地执行迭代搜索，缺乏全局推理。PSC-AVDN提出搜索思维链（S-CoT），包含四个显式推理步骤：目的地分析、场景理解、参考网格地图生成、目标定位。通过这一逐步推理机制，模型能够有逻辑地缩小候选区域，而非盲目扫描。消融实验（Table 2）表明，完整的解析+搜索+确认三阶段推理将SR从单阶段的基线水平提升至22.6，验证了结构化搜索的必要性。

### 从单次决策到细粒度确认：消除视觉歧义的验证机制

基线方法无单独确认步骤，可能在候选区域存在多个相似目标时误停或漏检。PSC-AVDN引入确认思维链（C-CoT），在搜索阶段锁定的候选区域周围进行细粒度验证，检查空间关系与语义约束，通过可解释的推理链消除视觉歧义。这一设计将“找到”与“确认”解耦，使最终决策更加可靠。

### 从孤立帧到全局上下文：结构化空间记忆的三重补充

MLLM基线缺乏全局空间理解与历史状态跟踪，无法利用已探索区域的信息。PSC-AVDN的SSM模块通过三个组件补充空间上下文：

- **多尺度视觉观察（MVO）**：通过缩放因子$(3,5,7)$对全局遥感图像$\mathbb{Z}$进行重采样，获得多尺度裁剪$\mathcal{V}_t^i = \mathrm{Resample}(\mathbb{Z}, s^i)$，拼接后形成$\{\mathcal{V}_t\}$，使模型同时获取不同粒度的视觉信息。
- **空间视觉记忆（SVM）**：通过$\mathcal{M}_t = (\mathcal{M}_{t-1} \oplus \mathcal{V}_t) \oplus (\mathcal{T}_t \oplus \theta_t)$将历史记忆、当前视图、轨迹和方向信息融合，保证时序与空间连续性。
- **结构化几何记忆（SGM）**：引导模型生成参考网格地图$\bar{\mathcal{R}}_t = [r_1, r_2, \ldots, r_{N^2}]$，每个单元格$r_j = (p_j, c_j)$包含空间坐标与语义标签，通过$\mathcal{R}_t = \mathrm{Update}(\mathcal{R}_{t-1}, \bar{\mathcal{R}}_t)$持续更新，为推理提供显式的空间感知锚点。

消融实验（Table 3）表明，SVM、MVO、SGM三者联合使用时达到最优性能（SPL 17.8, SR 22.6, GP 39.2），任一组件的移除均导致性能下降，验证了全局空间上下文与历史信息对空中导航的关键作用。

### 关键参数的自适应选择

网格尺寸消融（Table 4）显示$5\times5$参考网格取得最佳性能，过大或过小的网格均会损害空间感知精度。多尺度裁剪缩放因子消融（Table 5）表明$(3,5,7)$组合优于其他配置，说明同时覆盖局部细节与全局上下文对高空目标定位至关重要。需注意，这些超参数目前需根据场景手动调整，自适应选择机制尚缺。

## 整体框架

PSC-AVDN 构建了一个训练免（training-free）的三阶段推理流水线，将空中视觉对话导航形式化为一个跨模态映射问题。给定第 $l$ 轮对话指令 $\mathcal{U}_l$，模型需要在时间窗口 $[t_l^s, t_l^e]$ 内逐步推理，最终输出目标边界框 $\mathcal{B}_l$。整个框架的核心映射关系为：

$$\mathcal{F} : ( \mathcal{U}_l , \{ \mathcal{V}_t \}_{t=t_l^s}^{t_l^e} , \mathcal{M}_{t_l^e} , \mathcal{R}_{t_l^e} ) \rightarrow \mathcal{B}_l$$

其中 $\{\mathcal{V}_t\}$ 为多尺度视觉观测序列，$\mathcal{M}_t$ 为空间视觉记忆，$\mathcal{R}_t$ 为结构化几何记忆。这三个空间上下文组件由**结构化空间记忆模块（SSM）**统一维护，按时间步递归更新：

$$\mathcal{M}_{t+1}, \mathcal{R}_{t+1} = \mathrm{SSM}(\mathcal{M}_t, \mathcal{R}_t)$$

### 三阶段推理流水线

框架将导航任务解耦为三个串行阶段，每个阶段承担不同的认知功能：

1. **解析阶段（Parsing Stage）**：利用 LLM（论文采用 DeepSeek-V3）将对话中的模糊方向短语（如 “10 o’clock direction”）和目标描述转换为结构化的几何方向线索与目标语义描述。航向解析模块进一步将方向线索统一为绝对角度表示（如 237°），消除自然语言的方向歧义。

2. **搜索阶段（Search Stage）**：通过**搜索思维链（S-CoT）** 进行四步递进推理——目的地分析、场景理解、参考网格地图生成、目标定位——逐步缩小候选区域。S-CoT 的核心机制是让 MLLM 显式地输出中间推理步骤，将高空大范围的目标搜索分解为可解释的逐步决策过程。

3. **确认阶段（Confirmation Stage）**：通过**确认思维链（C-CoT）** 对候选区域进行细粒度验证，检查空间关系与语义约束是否满足指令要求，消除视觉歧义并最终确定唯一目标位置。C-CoT 的核心价值在于弥补搜索阶段可能产生的误匹配，避免误停或漏检。

### 结构化空间记忆模块（SSM）

SSM 为搜索和确认阶段提供全局空间上下文与时间连续性，包含三个协同组件：

- **多尺度视觉观测（MVO）**：通过对全局遥感图像 $\mathbb{Z}$ 以不同缩放因子 $s^i$ 进行重采样，获得多尺度图像裁剪 $\mathcal{V}_t^i = \mathrm{Resample}(\mathbb{Z}, s^i)$，并拼接形成最终观测 ${\mathcal{V}}_t = [{\mathcal{V}}_t^1, {\mathcal{V}}_t^2, \ldots, {\mathcal{V}}_t^M]$。多尺度信息使模型同时获取粗粒度空间布局和细粒度目标特征。

- **空间视觉记忆（SVM）**：通过拼接历史记忆图、当前视图、轨迹 $\mathcal{T}_t$ 和方向 $\theta_t$ 信息更新记忆状态 $\mathcal{M}_t = (\mathcal{M}_{t-1} \oplus \mathcal{V}_t) \oplus (\mathcal{T}_t \oplus \theta_t)$，确保推理过程的时间与空间连续性。

- **结构化几何记忆（SGM）**：引导模型生成参考网格地图 $\bar{\mathcal{R}}_t = [r_1, r_2, \ldots, r_{N^2}]$，每个单元格 $r_j = (p_j, c_j)$ 包含空间坐标 $p_j$ 和语义标签 $c_j$，并通过 $\mathcal{R}_t = \mathrm{Update}(\mathcal{R}_{t-1}, \bar{\mathcal{R}}_t)$ 融合历史几何信息，为空间感知和推理提供显式的结构化空间参照。

### 输入输出流

整个流水线的数据流为：对话指令首先进入解析阶段，输出结构化的方向与目标描述；搜索阶段接收解析结果、当前多尺度视觉观测及 SSM 提供的空间记忆，通过 S-CoT 逐步逼近目标区域；确认阶段对候选区域进行 C-CoT 验证，最终输出目标边界框。SSM 模块在每个时间步更新记忆状态，为后续推理提供累积的空间上下文。这种设计将方向理解、空间搜索和视觉确认三者解耦，使 MLLM 在缺乏高空导航训练数据的情况下仍能进行可靠的空间推理。

### 补充图表

![[assets/figures/papers/paper_list_l2182_https_openaccess_thecvf_com_content_CVPR2026_html_Qi_Parse_Search_and_Co/figures/002_Figure_2.jpg]]
*Figure 2: The overall architecture of our proposed Parsing-Search-Confirmation framework for Aerial Vision-and-Dialog Navigation (PSC-AVDN). (a) The three-stage reasoning process first parses the destination and direction, followed by navigation through the stepwise reasoning chain (S-CoT and C-CoT), gradually searching and confirming the target location. (b) The Structured Spatial Memory (SSM) module provides multi-scale visual observation (MVO), spatial visual memory (SVM), and structured geometric memory (SGM) to enhance the search-confirmation process*

## 核心模块与公式推导

### 3.1 跨模态映射形式化

PSC-AVDN将每轮导航形式化为一个跨模态映射问题：给定第 $l$ 轮对话指令 $\mathcal{U}_l$，系统需要在时间窗口 $[t_l^s, t_l^e]$ 内，基于多尺度视觉观测 $\{\mathcal{V}_t\}$、空间视觉记忆 $\mathcal{M}_{t_l^e}$ 和结构化几何记忆 $\mathcal{R}_{t_l^e}$，预测目标边界框 $\mathcal{B}_l$：

$$\mathcal{F} : (\mathcal{U}_l, \{\mathcal{V}_t\}_{t=t_l^s}^{t_l^e}, \mathcal{M}_{t_l^e}, \mathcal{R}_{t_l^e}) \rightarrow \mathcal{B}_l$$

其中，空间视觉记忆和结构化几何记忆通过SSM模块在每一步更新：

$$\mathcal{M}_{t+1}, \mathcal{R}_{t+1} = \mathrm{SSM}(\mathcal{M}_t, \mathcal{R}_t)$$

该映射的核心挑战在于：MLLM缺乏对高空遥感图像的空间理解能力，且无法有效追踪历史导航状态。PSC-AVDN通过三阶段推理（解析-搜索-确认）将这一复杂映射解耦为可管理的子任务，并由SSM模块提供全局空间上下文。

### 3.2 解析阶段：航向解析模块

解析阶段的关键在于将模糊的自然语言方向描述（如"10点钟方向"）转换为统一的几何角度表示。航向解析模块的核心操作为相对航向计算：

$$\delta = \mathrm{wrap}(\alpha - \phi)$$

其中，$\alpha$ 为从指令中提取的绝对方向角（通过LLM解析得到），$\phi$ 为无人机当前方位角，$\mathrm{wrap}(\cdot)$ 将角度归一化至 $[0, 2\pi)$。这一转换消除了MLLM基线中因方向歧义导致的定位错误（见Figure 1）。

### 3.3 搜索与确认阶段：思维链推理

搜索思维链（S-CoT）包含四个显式推理步骤：目的地分析、场景理解、参考网格地图生成、目标定位。通过逐步缩小候选区域，S-CoT将复杂的空中目标搜索任务分解为可解释的子任务。

确认思维链（C-CoT）在候选区域进行细粒度验证，检查空间关系约束（如目标是否位于特定地标附近），消除视觉歧义并确认唯一目标位置。消融实验（Table 2）表明，完整的解析-搜索-确认三阶段推理相比简化版本显著提升性能，验证了逐阶段推理的必要性。

### 3.4 结构化空间记忆模块（SSM）

SSM是PSC-AVDN的空间上下文引擎，由三个协同组件构成：

**多尺度视觉观测（MVO）**：在每一步 $t$，通过重采样全局遥感图像 $\mathbb{Z}$ 和缩放因子 $s^i$ 获得第 $i$ 尺度的图像裁剪：

$$\mathcal{V}_t^i = \mathrm{Resample}(\mathbb{Z}, s^i)$$

将 $M$ 个尺度的裁剪拼接形成最终的多尺度视觉观测：

$$\{\mathcal{V}_t\} = [\mathcal{V}_t^1, \mathcal{V}_t^2, \ldots, \mathcal{V}_t^M]$$

消融实验（Table 5）表明，缩放因子组合 $(3,5,7)$ 取得最优性能。

**空间视觉记忆（SVM）**：通过拼接历史记忆、当前视图、轨迹和方向信息更新记忆图：

$$\mathcal{M}_t = (\mathcal{M}_{t-1} \oplus \mathcal{V}_t) \oplus (\mathcal{T}_t \oplus \theta_t)$$

其中 $\mathcal{T}_t$ 为轨迹信息，$\theta_t$ 为历史方向。该机制确保推理过程的时间连续性和空间一致性。

**结构化几何记忆（SGM）**：引导模型生成参考网格地图，将空间划分为 $N \times N$ 的单元格：

$$\bar{\mathcal{R}}_t = [r_1, r_2, \ldots, r_{N^2}], \quad \text{where } r_j = (p_j, c_j)$$

每个单元格 $r_j$ 包含空间坐标 $p_j$ 和语义标签 $c_j$。结构化几何记忆通过融合当前参考网格地图更新：

$$\mathcal{R}_t = \mathrm{Update}(\mathcal{R}_{t-1}, \bar{\mathcal{R}}_t)$$

消融实验（Table 4）表明，$5 \times 5$ 网格尺寸取得最佳性能。Table 3的消融进一步证实，SVM、MVO和SGM三者联合使用达到最优效果（SPL 17.8, SR 22.6, GP 39.2），验证了各组件对全局空间理解和长期一致性的贡献。

### 补充图表

![[assets/figures/papers/paper_list_l2182_https_openaccess_thecvf_com_content_CVPR2026_html_Qi_Parse_Search_and_Co/figures/001_Figure_1.jpg]]
*Figure 1: Motivation of our method. (a) The MLLM baseline suffers from ambiguous directional descriptions and the domain gap between high-altitude imagery and ground-level training data, leading to inaccurate localization. (b) Our PSC-AVDN eliminates directional ambiguity through instruction parsing, performs structured search via chain-of-thought reasoning, and conducts finegrained confirmation around the candidate region to achieve more reliable navigation. In addition, a structured spatial memory is introduced to provide clearer spatial context for reasoning*

![[assets/figures/papers/paper_list_l2182_https_openaccess_thecvf_com_content_CVPR2026_html_Qi_Parse_Search_and_Co/figures/003_Figure_3.jpg]]
*Figure 3: SSM Module diagram. A concrete case is presented to demonstrate how the SSM module operates within the CoT process. The module consists of three main parts: (a) Multi-scale Visual Observation (MVO): Visual inputs at different scales help the model acquire various levels of visual information. (b) Spatial Visual Memory (SVM): Historical information is fused with the current CoT to ensure temporal and spatial continuity and consistency in the reasoning process. (c) Structured Geometric Memory (SGM): The model is guided to generate a reference grid map to assist in spatial perception and reasoning*

## 实验与分析

### 主实验结果

PSC-AVDN在ANDH和ANDH-Full两个数据集上均取得了训练免设置下的最优性能，验证了解析-搜索-确认框架结合结构化空间记忆的有效性。Table 1展示了与监督微调方法和训练免基线的全面对比。

在ANDH Unseen Val上，PSC-AVDN达到SPL 17.8、SR 22.6、GP 39.2，而直接使用GPT-4o的训练免基线仅取得SPL 3.4、SR 3.9、GP -11.8，性能提升幅度显著（SPL +14.4，SR +18.7，GP +51.0）。这一巨大差距揭示了核心瓶颈：MLLM在高空视角下缺乏鲁棒的空间定位能力，无法有效理解模糊方向描述，且高空遥感图像与地面训练数据之间存在严重的域差异。

在更具挑战性的ANDH-Full Unseen Val上，PSC-AVDN取得SPL 12.4、SR 15.4、GP 62.3，同样在训练免方法中表现最佳。值得注意的是，PSC-AVDN的性能不仅远超训练免基线，还匹配甚至超越了多个需要任务特定训练的监督微调方法，如**FELA w/ attn**（Su et al., AAAI 2025）和**NavAgent**（Liu et al., arXiv 2024），表明结构化推理流程可以弥补甚至替代标注数据的依赖。

### 三阶段推理框架消融

Table 2展示了解析-搜索-确认三阶段推理的消融结果。逐步加入各阶段后，性能持续提升：仅使用解析阶段时SR为12.1、GP为24.7；加入搜索阶段（S-CoT）后SR提升至16.8、GP提升至31.2；再加入确认阶段（C-CoT）后达到完整的SR 19.3、GP 35.7。这一渐进式提升验证了因果机制的有效性——解析阶段消除方向歧义，搜索阶段通过思维链逐步缩小候选区域，确认阶段通过细粒度验证消除视觉歧义，三者缺一不可。

### 结构化空间记忆模块消融

Table 3展示了SSM模块各组件的贡献。基线（无SSM）的SPL为12.1、SR为15.3、GP为28.4。单独加入空间视觉记忆（SVM）后，SPL提升至14.7、SR提升至18.1；单独加入多尺度视觉观察（MVO）后，SPL为14.2、SR为17.8；单独加入结构化几何记忆（SGM）后，SPL为13.8、SR为17.2。三者联合使用时达到最佳性能SPL 17.8、SR 22.6、GP 39.2，表明多尺度感知、历史状态跟踪和结构化空间理解之间存在协同效应，共同为推理过程提供了全局空间上下文和时间连续性。

### 超参数消融

Table 4展示了参考网格地图中不同网格尺寸的影响。5×5网格取得最佳性能，过小的网格（如3×3）空间分辨率不足，无法精确定位目标；过大的网格（如7×7）则增加了推理复杂度，可能导致定位分散。

Table 5展示了多尺度裁剪中不同缩放因子组合的影响。缩放因子组合(3,5,7)取得最优性能，相比单一尺度或更少尺度的组合，该设置在不同空间粒度上提供了互补的视觉信息，使模型既能捕捉全局场景结构，又能关注局部目标细节。

### 可视化分析

Figure 4展示了PSC-AVDN在两轮对话和单轮指令场景下的导航轨迹。黄色虚线表示导航路径，红色矩形标记目标区域。可视化结果表明，PSC-AVDN能够在复杂高空场景中生成合理且高效的导航轨迹，逐步逼近目标位置。在两轮对话场景中，模型能有效利用对话历史修正导航方向；在单轮指令场景中，模型直接从解析的几何方向出发，通过搜索-确认流程定位目标。

### 失败模式与局限性

尽管PSC-AVDN取得了显著性能提升，仍存在若干值得关注的局限。首先，解析阶段依赖LLM（DeepSeek-V3）的指令理解能力，对于极其模糊或新颖的表达可能解析失败，导致后续搜索方向错误。其次，多尺度裁剪的缩放因子和参考网格尺寸需要根据场景手动调整，缺乏自适应选择机制。此外，论文未在真实无人机平台上验证，模拟器到实际环境的迁移性能未知；在高空复杂动态场景（如移动障碍物）下的有效性也尚未探讨。这些开放问题为后续研究指明了方向。

### 补充图表

![[assets/figures/papers/paper_list_l2182_https_openaccess_thecvf_com_content_CVPR2026_html_Qi_Parse_Search_and_Co/figures/004_Table_1.jpg]]
*Table 1: Comparison results on the ANDH and ANDH-Full datasets. Higher values indicate better performance. Underline and bold indicate the best results among supervised finetuning and training-free methods, respectively. Our PSC-AVDN achieves state-of-the-art performance in the training-free setting, comparable to or even surpassing several supervised finetuning methods*

![[assets/figures/papers/paper_list_l2182_https_openaccess_thecvf_com_content_CVPR2026_html_Qi_Parse_Search_and_Co/figures/006_Table_2.jpg]]
*Table 2: Ablation results of our three-stage reasoning framework*

![[assets/figures/papers/paper_list_l2182_https_openaccess_thecvf_com_content_CVPR2026_html_Qi_Parse_Search_and_Co/figures/005_Table_3.jpg]]
*Table 3: Ablation results of SVM (Spatial Visual Memory), MVO (Multi-scale Visual Observation), and SGM (Structured Geometric Memory) components in our SSM module*

![[assets/figures/papers/paper_list_l2182_https_openaccess_thecvf_com_content_CVPR2026_html_Qi_Parse_Search_and_Co/figures/007_Table_4.jpg]]
*Table 4: Ablation results of different grid sizes in the Reference Grid Map of our SSM module*

![[assets/figures/papers/paper_list_l2182_https_openaccess_thecvf_com_content_CVPR2026_html_Qi_Parse_Search_and_Co/figures/009_Table_5.jpg]]
*Table 5: Ablation results across different scaling factor combinations in the Multi-Scale Crop of our SSM module*

![[assets/figures/papers/paper_list_l2182_https_openaccess_thecvf_com_content_CVPR2026_html_Qi_Parse_Search_and_Co/figures/008_Figure_4.jpg]]
*Figure 4: Visualization of navigation trajectories from our PSC-AVDN. (a) represents a two-round dialogue case, and (b) represents a single-round instruction case. The yellow dashed line indicates the navigation trajectory, while the red rectangle denotes the target area*

## 方法谱系与知识库定位

### 任务定位与基线谱系

PSC-AVDN 面向**空中视觉对话导航**（Aerial Vision-and-Dialog Navigation, AVDN），该任务要求无人机根据自然语言对话指令在高空遥感图像中定位并导航至目标区域。与传统的室内/室外地面视觉导航（如 VLN）不同，AVDN 的核心挑战在于：高空视角带来的域差异、模糊方向表达（如“10点钟方向”）的解析困难，以及缺乏全局空间上下文导致的长程推理不可靠。

在方法谱系上，现有工作可分为两条主线：

- **监督微调方法**：代表工作包括 **FELA w/ attn**（Su et al., AAAI 2025）、**NavAgent**（Liu et al., arXiv 2024）和 **OpenFly**（Gao et al., arXiv 2025）。这些方法在 ANDH 数据集上进行任务特定训练，性能较强但依赖标注数据，泛化到新场景的成本高。
- **训练免方法**：直接使用 MLLM（如 **GPT-4o**）进行零样本导航。论文揭示，GPT-4o 在 ANDH Unseen Val 上 SPL 仅 3.4、SR 仅 3.9（Table 1），暴露了 MLLM 在高空场景下空间定位能力的严重不足。

PSC-AVDN 属于训练免路线，但通过引入结构化推理和空间记忆，在 ANDH Unseen Val 上达到 SPL 17.8、SR 22.6，不仅大幅超越 GPT-4o baseline（SPL +14.4，SR +18.7），更匹配甚至超越了多个监督微调方法（Table 1），首次证明了训练免框架在 AVDN 任务上可以媲美监督方法。

### 核心因果机制

PSC-AVDN 的性能跃升源于对瓶颈的精准拆解与针对性干预：

1. **瓶颈诊断**：MLLM 在高空视角下缺乏鲁棒的空间定位能力，具体表现为：(a) 无法准确理解模糊方向短语；(b) 缺乏逐步缩小搜索区域的推理机制；(c) 无全局空间理解与时间状态跟踪，导致导航不可靠。
2. **因果旋钮**：将导航过程解耦为**解析-搜索-确认**三阶段，分别处理方向理解、目标定位和歧义消除，并通过**结构化空间记忆**（SSM）补充空间上下文。
3. **核心洞察**：通过思维链将模糊对话指令逐步转化为可执行的几何约束，利用多尺度视觉观察、空间视觉记忆和结构化几何记忆为推理提供全局空间上下文和长期一致性。

具体而言，每个阶段解决了基线的一个关键缺陷：

- **解析阶段**：GPT-4o 直接解释“10 o'clock”等模糊表达时易出错；PSC-AVDN 使用 LLM（DeepSeek-V3）提取方向与目标描述，通过航向解析模块转换为统一绝对角度（如 237°），消除了方向歧义。
- **搜索阶段**：基线方法孤立处理每帧，缺乏结构化搜索；PSC-AVDN 的搜索思维链（S-CoT）包含目的地分析、场景理解、参考网格地图生成和目标定位四步，逐步缩小候选区域。
- **确认阶段**：基线无单独验证机制，易误停或漏检；PSC-AVDN 的确认思维链（C-CoT）进行细粒度空间与关系约束验证，消除视觉歧义。
- **空间记忆**：基线缺乏全局空间理解；SSM 模块通过多尺度视觉观察（MVO）、空间视觉记忆（SVM）和结构化几何记忆（SGM）提供多粒度空间上下文和历史信息融合。

### 适用边界与局限

尽管 PSC-AVDN 在 ANDH 和 ANDH-Full 数据集上取得了训练免设置下的最优性能，其适用边界和潜在局限需要审慎评估：

1. **模拟器到现实的迁移差距**：所有实验均在 ANDH 模拟器上进行，论文未在真实无人机平台上验证。高空实飞场景中的光照变化、大气扰动、传感器噪声等因素可能导致性能下降，实际部署可行性未知。
2. **动态场景适应性未验证**：ANDH 数据集假设静态高空场景，PSC-AVDN 在存在移动障碍物或动态目标的复杂环境下的有效性未探讨。结构化空间记忆的更新机制是否能应对快速变化的场景仍需验证。
3. **解析阶段的鲁棒性上限**：解析阶段依赖 LLM 的指令理解能力。对于极其模糊、多义或新颖的表达（如隐喻性方向描述），LLM 可能提取错误的方向或目标线索，错误会级联传播至后续搜索和确认阶段。
4. **超参数敏感性**：多尺度裁剪的缩放因子组合（最优为 (3,5,7)）和参考网格尺寸（最优为 5×5）需要根据场景调整。论文通过消融实验确定了当前数据集上的最优配置（Table 4, Table 5），但缺乏自适应选择机制，跨场景迁移时可能需要重新调参。
5. **计算开销**：三阶段推理涉及多次 LLM/VLM 调用，且 SSM 模块需要维护和更新空间记忆，相比简单的端到端基线方法，推理延迟和计算成本更高。论文未讨论实时性约束下的性能表现。

### 开放问题与后续方向

基于上述局限，以下开放问题值得后续工作关注：

- **真实无人机验证**：将 PSC-AVDN 部署至真实无人机平台，评估 sim-to-real gap 的具体影响，并探索域适应策略。
- **动态场景扩展**：引入时序建模或动态记忆更新机制，使框架能处理移动障碍物和动态目标。
- **自适应超参数选择**：设计场景感知的缩放因子和网格尺寸自动选择策略，提升跨场景泛化能力。
- **鲁棒指令理解**：探索在解析阶段引入不确定性量化或多轮澄清机制，应对模糊或歧义指令。
- **效率优化**：通过模型蒸馏、推理缓存或早停策略降低多阶段推理的计算开销，满足实时导航需求。

*注：以上开放问题均来自论文未覆盖的维度，具体影响程度需通过后续实验验证。*

## 原文 PDF

![[paperPDFs/CVPR_2026/Parse_Search_and_Confirmation_Training_Free_Aerial_Vision_and_Dialog_Navigation_with_Chain_of_Thought_Reasoning_and_Structured_Spatial_Memory.pdf]]
