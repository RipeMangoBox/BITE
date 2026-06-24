---
title: "AutoTraces: Autoregressive Trajectory Forecasting via Multimodal Large Language Models"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/AutoTraces_Autoregressive_Trajectory_Forecasting_via_Multimodal_Large_Language_Models.pdf
project_link: null
code_link: null
aliases:
- AutoTraces
tags:
- CVPR_2026
- topic/other_unclear
- topic/other_unclear/general
core_operator: 引入 <point> token 作为航点统一表示，配合 Point Encoder 将坐标嵌入 LLM 隐空间，Point Head 将隐向量解码回坐标，在 LLM 原生自回归机制中实现航点的逐步生成。
primary_logic: 将每个航点抽象为单个特殊 <point> token，通过编码器-解码器在 LLM 内部无缝融合轨迹、视觉和文本多模态信息，既保留了预训练 LLM 的推理能力，又实现了物理空间中的高精度自回归预测；自动化思维链进一步增强了模型对复杂社会交互的理解。
claims:
- "AutoTraces 在 SCAND 数据集上的 L2 误差显著低于所有基线（T=5: 0.674, T=8: 0.923, T=10: 1.089），其中相对于 CityWalker 在 T=10 时降低 22.6%。"
- 在跨场景泛化实验中，AutoTraces 在 GoStanford 和 RECON 上均优于基础模型 LLaVa-Video，尤其在 RECON 上 T=8 和 T=10 的 L2 误差分别降低 30.0% 和 32.6%。
- 长周期预测（T=12-20）时，AutoTraces 的指令执行准确率（IEAcc）高达 99.92%，远超 LLaVa-Video 的 40.34%，且每条路径仅需 25.00 个 token（LLaVa-Video 需 375.64）。
- SCAND 上 L2 (m)↓ = 1.089 (T=10)
---

# AutoTraces: Autoregressive Trajectory Forecasting via Multimodal Large Language Models

> [!tip] 核心洞察
> 将每个航点抽象为单个特殊 <point> token，通过编码器-解码器在 LLM 内部无缝融合轨迹、视觉和文本多模态信息，既保留了预训练 LLM 的推理能力，又实现了物理空间中的高精度自回归预测；自动化思维链进一步增强了模型对复杂社会交互的理解。

| 字段 | 内容 |
|------|------|
| 中文题名 | AutoTraces：基于多模态大语言模型的自回归轨迹预测 |
| 英文题名 | AutoTraces: Autoregressive Trajectory Forecasting via Multimodal Large Language Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.07989) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | AutoTraces |
| Dataset | SCAND, GoStanford, RECON |

> [!tip] 效果简介
> - SCAND 上，L2 (m)↓ 1.089 (T=10) vs 1.407 (CityWalker) (-22.6%)；L2 (m)↓ 0.923 (T=8) vs 1.548 (LLaVa-Video) (-40.4%)。
> - GoStanford 上，L2 (m)↓ 1.772 (T=10) vs 2.141 (LLaVa-Video) (-17.2%)。
> - RECON 上，L2 (m)↓ 2.837 (T=10) vs 4.211 (LLaVa-Video) (-32.6%)。

## 概述

轨迹预测是移动机器人和自动驾驶系统中的关键能力，要求模型根据历史观测和场景上下文推断未来路径。现有方法通常将轨迹预测转化为文本生成任务，每个坐标需用多个文本 token 表示，导致 token 效率低下且时空建模能力受限；非自回归方法一次性生成完整未来序列，无法捕捉时间动态，也难以灵活调整预测长度。AutoTraces 针对这一瓶颈，提出以 **<point> token** 作为航点的统一表示，将每个二维航点抽象为单个特殊 token，通过 Point Encoder 将坐标嵌入大语言模型（LLM）的隐空间，并由 Point Head 将隐向量解码回物理坐标，从而在 LLM 原生自回归机制中实现航点的逐步生成。

该方法的核心洞察在于：通过编码器-解码器架构在 LLM 内部无缝融合轨迹、视觉和文本多模态信息，既保留了预训练 LLM 的推理能力，又实现了物理空间中的高精度自回归预测。同时，AutoTraces 引入自动化思维链（CoT）生成机制，利用辅助视觉语言模型结合轨迹曲率分析，自动为训练数据生成推理标注，使模型能够理解复杂的社会交互场景。

在 SCAND 数据集上，AutoTraces 的 L2 误差显著低于所有基线方法（T=5: 0.674 m，T=8: 0.923 m，T=10: 1.089 m），其中在 T=10 时相对于 CityWalker（Liu et al., CVPR 2025）降低 22.6%，相对于基础模型 LLaVa-Video（Zhang et al., TMLR 2025）降低 40.4%。在跨场景泛化实验中，AutoTraces 在未见过的 GoStanford（室内）和 RECON（室外）数据集上均优于 LLaVa-Video，尤其在 RECON 上 T=8 和 T=10 的 L2 误差分别降低 30.0% 和 32.6%。在长周期预测（T=12–20）中，AutoTraces 的指令执行准确率高达 99.92%，远超 LLaVa-Video 的 40.34%，且每条路径仅需 25.00 个 token（LLaVa-Video 需 375.64 个），token 效率提升约 15 倍。

## 背景与动机

轨迹预测是自主导航与机器人交互的核心能力，要求模型在动态环境中根据历史观测推断未来路径。近年来，多模态大语言模型（MLLM）凭借强大的视觉理解和推理能力，在各类具身任务中展现出显著潜力。然而，将 MLLM 应用于密集轨迹预测仍面临两个根本性瓶颈。

**坐标表示的效率困境。** 现有基于 LLM 的轨迹预测方法将航点坐标转化为文本 token 序列，每个坐标需多个 token 表示。这种文本化方案不仅造成 token 消耗膨胀，更关键的是割裂了坐标数值与 LLM 隐空间之间的语义对齐——模型需通过语言建模间接“猜测”连续物理量，导致空间精度损失和推理效率低下。

**生成范式的结构缺陷。** 主流方法采用非自回归范式，一次性输出完整未来序列。该设计虽然简洁，却从根本上剥夺了模型对时间动态的感知能力：每个预测步独立生成，无法利用已生成航点作为后续推理的条件信息。这导致预测序列缺乏时序一致性，且难以灵活调整预测长度以适应不同任务需求。

上述瓶颈在长周期预测场景下尤为突出。当预测步长从常规的 5-10 步扩展到 12-20 步时，文本化方案的单条路径 token 消耗可达数百量级，而非自回归范式则因误差累积而严重偏离真实轨迹。此外，现有方法普遍缺乏对社会交互的显式推理——转弯避让、人群穿行等复杂行为需要模型理解场景语义而非简单拟合运动模式。

AutoTraces 正是针对这两大瓶颈提出：通过引入 `<point>` 特殊 token 作为航点的统一表示单元，配合 Point Encoder-Point Head 的编码-解码架构，将连续坐标无缝嵌入 LLM 隐空间；同时利用 LLM 原生的自回归机制，实现航点逐帧生成与反馈闭环，使每一步预测都以前序输出为条件。在此基础上，通过自动化思维链（CoT）生成机制，模型被赋予对环境障碍和社会交互的显式推理能力。这一设计既保留了预训练 MLLM 的语义理解和推理能力，又在物理空间中实现了高精度、高效率的自回归轨迹预测。

## 核心创新

AutoTraces 的核心创新在于将轨迹预测从“文本生成”范式重构为“航点自回归生成”范式，通过三个相互耦合的 **changed slots** 解决了现有 LLM-based 方法的两大瓶颈：坐标文本化表示的低效性，以及非自回归生成对时间动态的建模不足。

---

### 1. 航点表示：从多 token 文本坐标到单 `<point>` token

现有方法（如 **LLaVa-Video**，Zhang et al., TMLR 2025）将 2D 坐标序列化为文本 token（例如 `(x, y)` 需占用多个 token），导致 token 效率低下，且坐标数值信息在 LLM 的离散 token 空间中难以被精确建模。

AutoTraces 提出 **点分词方案（Point Tokenization）**：将每个 2D 航点抽象为一个特殊的 `<point>` token，并配套设计 **Point Encoder** 和 **Point Head** 构成编码器-解码器架构：

- **Point Encoder** 将历史航点坐标映射为 LLM 隐空间中的连续嵌入：

  $$\mathbf{e}_{t-i} = \mathrm{PointEncoder}(\mathbf{x}_{t-i}), \quad i = L,\ldots,0$$

- **Point Head** 在 LLM 自回归生成 `<point>` token 后，将其隐状态解码回物理坐标：

  $$\hat{\mathbf{x}}_{t+k} = \mathrm{PointHead}(\hat{\mathbf{e}}_{t+k}), \quad k = 1,\ldots,T$$

这一设计使得每个航点仅占用 **1 个 token**，与文本化方案（每坐标需多个 token）相比，token 效率提升一个数量级。在长周期预测（T=12–20）中，AutoTraces 每条路径仅需 **25.00 个 token**，而 LLaVa-Video 需要 **375.64 个 token**，效率提升约 93%（Table 3）。同时，连续嵌入空间中的坐标表示使得 L1 回归损失可以直接作用于物理空间，避免了离散 token 解码带来的量化误差。

---

### 2. 生成范式：从非自回归一次生成到航点级自回归预测

现有 LLM-based 方法通常采用非自回归（non-autoregressive）方式，一次性输出完整的未来轨迹序列。这种方式无法捕捉航点间的时间依赖关系，也难以灵活调整预测长度。

AutoTraces 利用 LLM 原生的自回归机制，实现 **航点级自回归生成**：每生成一个 `<point>` token，经 Point Head 解码为坐标后，通过 Point Encoder 重新编码并反馈到 LLM 的输入序列中，作为下一航点预测的条件。这一闭环反馈机制（Section 3.4）确保了：

- **时间动态建模**：每个航点的预测显式依赖于先前已生成的航点，形成因果链。
- **预测长度灵活性**：模型可在推理时动态决定生成长度，无需为不同预测步长分别训练专用模型。Table 1 中，AutoTraces 以单一模型评估 T=5/8/10 所有步长，而部分基线（灰色背景行）需针对每个步长分别训练。

在 SCAND 数据集上，AutoTraces 在 T=10 时的 L2 误差为 **1.089**，较非自回归基线 **CityWalker**（Liu et al., CVPR 2025）的 1.407 降低 **22.6%**，较基础模型 LLaVa-Video 的 1.548 降低 **40.4%**（Table 1）。

---

### 3. 推理融合：从无推理到自动化思维链（CoT）

传统轨迹预测方法缺乏对场景语义和社会交互的显式推理能力。AutoTraces 引入 **自动化 CoT 生成机制**（Section 3.3）：利用辅助 VLM（Qwen-VL-Max）结合轨迹曲率分析，自动生成包含环境障碍分析和可执行动作推导的两阶段推理文本，无需人工标注。

这些 CoT 文本在 **第一阶段 QLoRA 预训练**中注入模型（Figure 2），使 LLM 学会在预测航点前进行“思考”。消融实验（Figure 4）表明，去除 CoT 推理（w/o CoT）会导致 SCAND T=10 上的 L2 误差从 **1.089 增至 1.145**，验证了推理能力对复杂社会交互场景下预测精度的增益。

---

### 4. 训练策略：两阶段 QLoRA 微调

为高效适配预训练 LLM，AutoTraces 采用 **两阶段 QLoRA 微调**（Section 3.4）：

- **第一阶段（CoT 预训练）**：在视频-文本对上训练模型的推理能力。
- **第二阶段（轨迹微调）**：冻结 LLM 主体，仅更新 LoRA 层、Text Head、Point Encoder 和 Point Head，通过联合损失进行优化：

  $$\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{point}} + \mathcal{L}_{\mathrm{LLM}}$$

  其中 $\mathcal{L}_{\mathrm{point}} = \frac{1}{F} \sum_{i=t+1}^{t+F} \| \mathbf{x}_i - \hat{\mathbf{x}}_i \|_1$ 为航点 L1 回归损失，$\mathcal{L}_{\mathrm{LLM}}$ 为文本交叉熵损失。

这一策略使得参数更新量极小，同时保留了预训练 LLM 的视觉理解和语言推理能力，在跨场景泛化实验中（Table 2）显著优于基础模型 LLaVa-Video：在室外数据集 RECON 上，T=8 和 T=10 的 L2 误差分别降低 **30.0%** 和 **32.6%**。

---

### 创新总结

| 维度 | 基线做法 | AutoTraces 创新 |
|------|---------|----------------|
| 航点表示 | 文本化坐标（多 token） | `<point>` token + Point Encoder/Head |
| 生成范式 | 非自回归一次生成 | 航点级自回归 + 闭环反馈 |
| 推理机制 | 无 CoT 或人工标注 | 自动化 CoT 生成与注入 |
| 训练策略 | 单阶段微调 | 两阶段 QLoRA（CoT 预训练 + 轨迹微调） |

三个 changed slots 形成协同效应：点分词方案使自回归生成在 token 效率上可行，自回归机制为 CoT 推理提供了逐航点的决策上下文，而 CoT 推理又增强了自回归预测在社会交互场景下的准确性。

## 整体框架

AutoTraces 是一个以 **LLaVa-Video**（Zhang et al., TMLR 2025）为基座的自回归视觉-语言-轨迹模型，核心目标是在复杂社会场景中实现高精度、可推理的密集轨迹预测。其整体 pipeline 围绕一个关键设计展开：将每个二维航点抽象为单一的特殊 **`<point>` token**，通过编码器-解码器架构在 LLM 内部无缝融合轨迹、视觉与文本多模态信息，既保留了预训练 LLM 的推理能力，又实现了物理空间中的逐步自回归预测。

### 模块组成与数据流

AutoTraces 的框架由以下核心模块构成（参见 Figure 2）：

![[assets/figures/papers/paper_list_l2295_https_arxiv_org_abs_2603_07989/figures/002_Figure_2.jpg]]
*Figure 2: The overall framework of our AutoTraces built upon LLaVa-Video [47] for socially compliant trajectory forecasting. In the first stage, the model is pre-trained on video-text pairs with reasoning prompts to acquire thinking knowledge. The second stage fine-tunes the model using trajectory waypoints (via a Point Encoder), aligning visual observations (via a Vision Encoder) and goal locations (via a Point Encoder). During inference, the model generates future trajectory waypoints as \<point> tokens, enabling autoregressive predictions*

1. **Vision Encoder**：接收时刻 $t$ 的 RGB 观测 $\mathbf{o}_t \in \mathbb{R}^{H \times W \times 3}$，将其编码为视觉嵌入 $\mathbf{V}_t$，注入 LLM 的输入序列。
2. **Point Encoder**：将历史航点坐标 $\mathbf{x}_{t-i} \in \mathbb{R}^2$（$i = L,\dots,0$）编码为 LLM 兼容的嵌入向量：
   $$\mathbf{e}_{t-i} = \mathrm{PointEncoder}(\mathbf{x}_{t-i})$$
   由此将连续的物理坐标映射到 LLM 的隐空间。
3. **LLM（LLaVa-Video）**：作为多模态自回归核心，接收历史航点嵌入 $\mathbf{E}_t$、视觉嵌入 $\mathbf{V}_t$ 以及文本提示嵌入 $\mathbf{P}_t$（包含指令与自动化思维链），逐 token 生成未来航点嵌入：
   $$\{\hat{\mathbf{e}}_{t+1}, \dots, \hat{\mathbf{e}}_{t+T}\} = \mathrm{LLM}(\mathbf{E}_t, \mathbf{V}_t, \mathbf{P}_t)$$
4. **Point Head**：将 LLM 输出的每个 `\<point\>` token 对应的隐状态解码回物理坐标：
   $$\hat{\mathbf{x}}_{t+k} = \mathrm{PointHead}(\hat{\mathbf{e}}_{t+k}), \quad k = 1,\ldots,T$$
5. **Text Head**：解码文本 token，用于生成 CoT 推理过程和结构化输出。

### 自回归预测回路

AutoTraces 的自回归机制并非仅依赖 LLM 原生的逐 token 生成，而是在航点级别形成显式的反馈回路：每生成一个 `\<point\>` token，Point Head 立即将其解码为物理坐标 $\hat{\mathbf{x}}_{t+k}$，该坐标随后经 Point Encoder 重新编码，并拼接到 LLM 的输入序列中，作为下一航点预测的历史条件。这一设计确保了预测序列中相邻航点之间的时空连续性，是 AutoTraces 在长周期预测中保持高精度和高指令执行准确率的结构性优势。

### 训练策略

AutoTraces 采用两阶段 **QLoRA** 参数高效微调策略，仅更新 LoRA 层、Text Head、Point Encoder 和 Point Head 的参数，冻结 LLM 主体与 Vision Encoder：

- **第一阶段（CoT 预训练）**：在视频-文本对上训练模型，使其获得社会场景下的推理知识。思维链由辅助 VLM 自动生成，遵循“环境障碍分析 → 可执行动作推导”的两阶段范式。
- **第二阶段（轨迹微调）**：使用航点数据对模型进行微调，对齐视觉观测、目标位置与历史轨迹，使模型学会在自回归框架下生成符合社会规范的未来航点序列。

训练损失为航点回归损失与 LLM 交叉熵损失的组合：
$$\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{point}} + \mathcal{L}_{\mathrm{LLM}}, \quad \mathcal{L}_{\mathrm{point}} = \frac{1}{F} \sum_{i=t+1}^{t+F} \| \mathbf{x}_i - \hat{\mathbf{x}}_i \|_1$$

### 与先前 LLM 方案的关键差异

相比将轨迹预测转化为纯文本生成任务的先前方案（需多个文本 token 表示单个坐标），AutoTraces 通过 `\<point\>` token 的引入，将每个航点的表示压缩为单一 token，大幅降低了 token 消耗（长周期预测中每条路径仅需 25.00 个 token，而 LLaVa-Video 需 375.64 个）。同时，非自回归方法一次生成完整未来序列，无法捕捉时间动态，而 AutoTraces 的航点级自回归设计使其能够灵活调整预测长度，并在逐步生成过程中持续利用历史信息进行条件更新。

## 核心模块与公式推导

AutoTraces 的整体架构建立在 **LLaVa-Video**（Zhang et al., TMLR 2025）之上，通过引入三个关键模块——**Point Encoder**、**Point Head** 和**自动化思维链（CoT）生成机制**——将多模态大语言模型改造为自回归轨迹预测器。以下逐一解析各模块的设计逻辑与核心公式。

---

### Point Encoder：航点坐标到 LLM 隐空间的映射

传统方法将 2D 坐标文本化（如 “(x, y)”），导致单个航点需消耗多个 token，效率低下且数值精度受限。AutoTraces 的核心创新在于引入特殊 token `<point>` 作为航点的统一表示，并设计 Point Encoder 将连续坐标值嵌入 LLM 可理解的隐空间。

给定历史航点序列 $\mathbf{x}_{t-L}, \dots, \mathbf{x}_t \in \mathbb{R}^2$，Point Encoder 将其逐点映射为嵌入向量：

$$\mathbf{e}_{t-i} = \mathrm{PointEncoder}(\mathbf{x}_{t-i}), \quad i = L,\ldots,0$$

该模块本质上是一个可学习的映射网络，将 2 维物理坐标投影到与 LLM 隐空间维度一致的向量。这些嵌入随后与视觉嵌入 $\mathbf{V}_t$（由 Vision Encoder 从 RGB 观测 $\mathbf{o}_t \in \mathbb{R}^{H \times W \times 3}$ 提取）和文本嵌入 $\mathbf{P}_t$ 拼接，形成多模态输入序列 $\mathbf{E}_t$，送入 LLM 进行自回归解码。

---

### Point Head：隐向量到物理坐标的解码

LLM 自回归生成的每个未来航点同样以 `<point>` token 的隐状态形式输出。Point Head 负责将这些隐向量解码回可执行的物理坐标：

$$\hat{\mathbf{x}}_{t+k} = \mathrm{PointHead}(\hat{\mathbf{e}}_{t+k}), \quad k = 1,\ldots,T$$

其中 $\hat{\mathbf{e}}_{t+k}$ 为 LLM 在时刻 $t+k$ 输出的隐状态，$\hat{\mathbf{x}}_{t+k} \in \mathbb{R}^2$ 为预测的航点坐标。Point Head 与 Point Encoder 构成一对“编码器-解码器”，确保坐标信息在 LLM 内部以紧凑的单一 token 形式流转，同时保持数值精度。

---

### 自回归生成与反馈闭环

AutoTraces 的生成过程严格遵循自回归范式。LLM 基于历史嵌入 $\mathbf{E}_t$、视觉嵌入 $\mathbf{V}_t$ 和文本嵌入 $\mathbf{P}_t$，逐 token 生成未来序列：

$$\{\hat{\mathbf{e}}_{t+1}, \dots, \hat{\mathbf{e}}_{t+T}\} = \mathrm{LLM}(\mathbf{E}_t, \mathbf{V}_t, \mathbf{P}_t)$$

关键设计在于**反馈闭环**：每生成一个 `<point>` token，Point Head 立即将其解码为坐标 $\hat{\mathbf{x}}_{t+k}$，该坐标经 Point Encoder 重新编码后追加到输入序列末尾，作为下一步预测的条件上下文。这一机制使得模型能够利用已预测的航点信息动态调整后续输出，从根本上区别于一次生成完整序列的非自回归方法。

---

### 自动化思维链（CoT）生成

为增强模型对复杂社会交互的理解，AutoTraces 引入自动化 CoT 生成机制。该过程借助辅助 VLM（Qwen-VL-Max）分析历史轨迹的曲率变化与视觉场景中的障碍物分布，自动生成推理文本。推理遵循两阶段范式：**环境障碍分析** → **可执行动作推导**，确保每个导航决策在视觉上可追溯、逻辑上可解释。

CoT 文本以自然语言形式嵌入 $\mathbf{P}_t$，与视觉和轨迹信息联合输入 LLM，使模型在预测航点前先进行“思考”。这一设计无需人工标注推理链，实现了推理能力的规模化获取。

---

### 训练目标

训练采用两阶段 QLoRA 策略，参数更新仅限 LoRA 层、Text Head、Point Encoder 和 Point Head。总损失由两部分组成：

$$\mathcal{L}_{\mathrm{point}} = \frac{1}{F} \sum_{i=t+1}^{t+F} \| \mathbf{x}_i - \hat{\mathbf{x}}_i \|_1$$

$$\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{point}} + \mathcal{L}_{\mathrm{LLM}}$$

其中 $\mathcal{L}_{\mathrm{point}}$ 为未来 $F$ 步航点的 L1 回归损失，$\mathcal{L}_{\mathrm{LLM}}$ 为文本 token 的标准交叉熵损失（用于监督 CoT 推理和结构化输出）。第一阶段在视频-文本对上进行 CoT 预训练，第二阶段引入轨迹数据联合微调，使模型同时掌握推理知识与精确预测能力。

### 补充图表

![[assets/figures/papers/paper_list_l2295_https_arxiv_org_abs_2603_07989/figures/001_Figure_1.jpg]]
*Figure 1: Comparison between our AutoTraces and previous LLM solutions. Our method introduces point tokens and embeddings for waypoint representation, enabling autoregressive prediction*

![[assets/figures/papers/paper_list_l2295_https_arxiv_org_abs_2603_07989/figures/003_Figure_3.jpg]]
*Figure 3: Illustration of the CoT generation for AutoTraces, incorporating visual observations and trajectory analysis. Red points and lines denote the historical trajectory, while blue points and lines denote the ground-truth trajectory. Action annotations (R: right, L: left, S: straight) are marked along the trajectory*

## 实验与分析

### 主实验结果：SCAND 数据集

AutoTraces 在 SCAND 数据集上以单模型统一设置全面超越所有基线方法。Table 1 报告了预测步长 T=5、8、10（每步间隔 1s）下的 L2 和 L1 误差。核心结果如下：

![[assets/figures/papers/paper_list_l2295_https_arxiv_org_abs_2603_07989/figures/004_Table_1.jpg]]
*Table 1: Performance evaluation of trajectory prediction over 5 to 10 steps on SCAND dataset [20], with an interval of 1s per step. Baselines with gray background are specifically trained and tested on fixed trajectory lengths. In contrast, “Single Model” variants are predominantly trained on T=10 sequences (except NoMad trained on T=8) and evaluated across all horizons under truncated-length settings*

- **T=10 时 L2 误差 1.089 m**，相比最强基线 CityWalker 的 1.407 m 降低 **22.6%**，相比基础模型 LLaVa-Video 的 1.548 m 降低 **40.4%**。
- 在更短预测步长下优势同样显著：T=5 时 L2 仅 0.674 m，T=8 时为 0.923 m。
- L1 指标呈现一致趋势：T=10 时 AutoTraces 为 1.384 m，CityWalker 为 1.759 m（降低 21.3%）。

值得注意的是，Table 1 中灰色背景行标注的基线模型（GNM、ViNT、NoMaD 等）为固定预测长度分别训练和评估，而 AutoTraces 使用单一模型评测所有预测长度。即便在这种对 AutoTraces 相对不利的设定下，其单模型性能仍全面领先。

### 跨场景泛化：GoStanford 与 RECON

Table 2 展示了在未见场景上的泛化能力。AutoTraces 在两个数据集上均一致优于其基础模型 LLaVa-Video：

![[assets/figures/papers/paper_list_l2295_https_arxiv_org_abs_2603_07989/figures/005_Table_2.jpg]]
*Table 2: Performance evaluation of cross-scene trajectory prediction on unseen GoStanford dataset [17] for indoor and RECON dataset [39] for outdoor scenarios with prediction horizon ranging from 5 to 10 steps, with an interval of 1s per step*

- **GoStanford（室内）**：T=10 时 L2 误差 1.772 m，LLaVa-Video 为 2.141 m，相对降低 17.2%。
- **RECON（室外）**：T=8 时 L2 从 3.557 m 降至 2.490 m（降低 **30.0%**），T=10 时从 4.211 m 降至 2.837 m（降低 **32.6%**）。

这一结果表明，AutoTraces 的航点分词方案和自回归生成机制并非对训练场景过拟合，而是学到了可迁移的时空推理能力。室外场景（RECON）的相对增益更大，暗示点分词在复杂、长距离预测中优势更为突出。

### 长周期预测效率与指令执行准确率

Table 3 将预测步长扩展至 T=12–20，同时引入指令执行准确率（IEAcc）和每条路径的 token 消耗（TPR）两个效率指标：

![[assets/figures/papers/paper_list_l2295_https_arxiv_org_abs_2603_07989/figures/006_Table_3.jpg]]
*Table 3: Performance Comparison of Extended Trajectory Prediction on SCAND [20] with prediction horizon over 12-20 steps (1s/step)*

- **IEAcc 达到 99.92%**，而 LLaVa-Video 仅 40.34%。这表明 AutoTraces 的 `<point>` token 机制几乎完全消除了文本化坐标表示中常见的格式错误和数值漂移。
- **Token 效率提升 15 倍**：AutoTraces 每条路径仅需 25.00 个 token，LLaVa-Video 则需 375.64 个（降低 93.3%）。这一差距源于文本化方案需多个 token 表示单个坐标，而 AutoTraces 每个航点仅消耗 1 个 `<point>` token。
- 在 L2 误差上，T=12–20 的长周期预测中 AutoTraces 同样保持显著优势。

### 消融研究：点分词方案与 CoT 推理

Figure 4 报告了两项关键消融实验（SCAND 数据集）：

![[assets/figures/papers/paper_list_l2295_https_arxiv_org_abs_2603_07989/figures/007_Figure_4.jpg]]
*Figure 4: Ablation study of our learnable waypoint tokenization scheme and CoT reasoning on SCAND [20] dataset*

1. **去除 CoT 推理（w/o CoT）**：T=10 时 L2 误差从 1.089 增至 1.145，性能下降约 5.1%。这验证了自动化思维链对复杂社会交互理解的贡献——模型通过显式分析环境障碍和行人行为，生成了更符合社会规范的轨迹。
2. **文本化坐标表示（w/o Point Tokenization）**：Table 3 的对比已充分说明点分词方案在 token 效率和预测精度上的双重优势。文本化方案不仅 token 消耗激增，且因数值精度损失导致 L2 误差显著上升。

此外，单阶段训练（无 CoT 预训练）的消融表明，直接进行轨迹微调会使模型难以捕获社会推理知识，最终性能劣于两阶段策略。这印证了先通过视频-文本对注入推理能力、再进行轨迹对齐的两阶段 QLoRA 微调设计的必要性。

### 自回归 vs. 单次生成

Figure 6 对比了自回归（逐航点生成并反馈）与单次生成（一次性输出完整序列）的预测质量。自回归机制的优势体现在两方面：

![[assets/figures/papers/paper_list_l2295_https_arxiv_org_abs_2603_07989/figures/009_Figure_6.jpg]]
*Figure 6: Comparison between autoregressive and one-pass predictions on SCAND [20] and RECON [39] datasets*

- **时间动态建模**：每个预测航点基于前序航点逐步生成，能捕捉轨迹的连续性和转向意图，避免单次生成中常见的轨迹突变。
- **灵活预测长度**：自回归生成可随时终止，无需为不同预测步长训练多个模型，这与 Table 1 中单模型评测多步长的设定一致。

### 定性分析

Figure 5 展示了 AutoTraces 与基线方法在 SCAND 上的预测轨迹可视化。AutoTraces 生成的轨迹更平滑、更贴近真实路径，尤其在行人密集或转向频繁的场景中，其社会合规性明显优于 CityWalker 和 LLaVa-Video。CoT 推理的可解释性输出（Figure 3）进一步表明，模型能够识别环境障碍并推导出合理的避让动作（如“左转绕过行人”），而非仅进行几何外推。

![[assets/figures/papers/paper_list_l2295_https_arxiv_org_abs_2603_07989/figures/008_Figure_5.jpg]]
*Figure 5: Visualizations of predicted trajectory from our AutoTraces and other baselines on SCAND [20] dataset*

### 公平性说明

部分基线模型（Table 1 灰色行）使用固定预测长度分别训练和评估，而 AutoTraces 以单模型评测所有长度。尽管存在这一设定差异，AutoTraces 在单模型设置下仍全面超越所有基线。在跨场景泛化实验中，对比基础模型 LLaVa-Video 时，两者使用相同的视觉编码器和 LLM 架构，差异仅来自点分词方案、自回归机制和 CoT 训练策略，对比公平性较好。

## 方法谱系与知识库定位

### 1. 问题定位：LLM 轨迹预测中的表征瓶颈与生成范式缺陷

AutoTraces 的出发点是对现有 LLM-based 轨迹预测方法两个结构性缺陷的纠正。第一个缺陷是**坐标文本化表征**：此前方法将连续 2D 航点坐标转化为文本 token 序列（如 `(x, y)` 字符串），每个坐标需消耗多个 token，导致 token 效率极低，且 LLM 难以在离散 token 空间中精确建模连续物理量。第二个缺陷是**非自回归生成范式**：主流 LLM 轨迹预测方案采用单次前向生成完整未来序列，无法捕捉轨迹的时间动态演化，也难以灵活调整预测长度——预测不同步长往往需要训练多个独立模型。

### 2. 与基线工作的关系

#### 2.1 导航基线（GNM / ViNT / NoMaD）

**GNM**（Shah et al., ICRA 2023）、**ViNT**（Shah et al., CoRL 2023）和 **NoMaD**（Sridhar et al., ICRA 2024）构成了通用导航模型基线。这些方法在固定预测长度下训练和评估（如 NoMaD 在 T=8 训练），缺乏灵活的自回归预测能力。AutoTraces 与它们的关键差异在于：(1) 单一模型可评估所有预测长度（T=5/8/10），无需为每个步长训练独立模型；(2) 引入 CoT 推理机制，使模型具备对社会交互场景的理解能力，而非单纯的几何路径规划。

#### 2.2 城市导航基线（CityWalker）

**CityWalker**（Liu et al., CVPR 2025）是面向城市环境的导航基线。在 SCAND 数据集 T=10 设定下，CityWalker 的 L2 误差为 1.407 m，AutoTraces 降至 1.089 m，相对降低 22.6%。该增益的核心来源是 AutoTraces 的点分词方案与自回归机制，而非更强大的视觉 backbone——CityWalker 同样使用视觉输入，但其文本化坐标表征限制了 LLM 对物理空间的精确建模。

#### 2.3 基础模型（LLaVa-Video）

**LLaVa-Video**（Zhang et al., TMLR 2025）是 AutoTraces 的 backbone 模型，也是最重要的内部基线。AutoTraces 在 LLaVa-Video 基础上仅新增了 Point Encoder、Point Head 和 LoRA 适配层，参数更新量极小。性能增益来自架构创新而非模型规模：SCAND T=8 时 L2 从 1.548 m 降至 0.923 m（-40.4%）；跨场景泛化中，RECON T=10 时 L2 从 4.211 m 降至 2.837 m（-32.6%）。更重要的是，在长周期预测（T=12-20）中，LLaVa-Video 的指令执行准确率仅 40.34%，而 AutoTraces 达到 99.92%，且每条路径仅需 25.00 个 token（LLaVa-Video 需 375.64），token 效率提升约 15 倍。

### 3. 方法谱系中的定位

AutoTraces 处于三个研究方向的交叉点：

- **LLM-based 轨迹预测**：继承了将轨迹预测转化为序列生成任务的基本思路，但通过 `<point>` token 机制解决了坐标表征的 token 效率问题。
- **多模态大语言模型应用**：利用 LLaVa-Video 的预训练视觉-语言对齐能力，通过 Point Encoder/Head 将轨迹模态无缝注入 LLM 隐空间，避免了对预训练权重的破坏性微调。
- **自动化思维链推理**：区别于依赖人工标注推理步骤的方法，AutoTraces 使用辅助 VLM（Qwen-VL-Max）结合轨迹曲率分析自动生成 CoT 标注，使推理知识获取可规模化。

### 4. 适用边界

- **场景依赖**：AutoTraces 依赖视觉观测（RGB 图像）作为输入，无法直接应用于纯轨迹预测（无视觉观测）场景。其视觉编码器与 Point Encoder 的联合训练使得模型对视觉-轨迹对齐有强依赖。
- **平台绑定**：当前实现基于 LLaVa-Video 的特定架构，Point Encoder/Head 和 LoRA 适配层针对该 backbone 设计，迁移到其他 LLM 需要重新训练这些模块。
- **CoT 质量依赖**：自动化 CoT 生成的质量取决于辅助 VLM 的能力边界。在极端复杂或罕见的社会交互场景中，自动生成的推理链可能存在偏差，但论文未对此进行系统评估。

### 5. 局限与开放问题

**已确认的局限**：
- 论文未报告在完全无视觉输入（纯轨迹坐标预测）条件下的性能，无法判断 Point Encoder/Head 机制在纯几何推理任务上的有效性。
- 自动化 CoT 生成流程依赖外部 VLM（Qwen-VL-Max），增加了训练管线的复杂度和外部依赖，但论文未提供 CoT 质量的人工评估或消融不同辅助 VLM 的影响。

**开放问题**：
- **CoT 生成的自监督化**：能否通过更轻量的方法（如基于轨迹几何特征的规则引擎）产生有效推理，从而摆脱对大型辅助 VLM 的依赖？
- **跨平台泛化**：AutoTraces 的点分词方案和自回归机制能否推广到其他机器人平台（如无人机、机械臂），是否需要针对不同运动学约束重新设计 Point Encoder/Head？
- **实时性约束**：自回归逐点生成虽然保证了预测质量，但在需要高频实时预测的场景中，逐 token 解码的延迟是否满足要求，论文未提供推理延迟数据。

> **注意**：上述适用边界和开放问题中关于“纯轨迹预测性能”“CoT 质量人工评估”“推理延迟”等论断，在已验证分析中未找到直接实验证据支撑，属于从方法设计出发的合理推断，需读者结合自身场景手动验证。

## 原文 PDF

![[paperPDFs/CVPR_2026/AutoTraces_Autoregressive_Trajectory_Forecasting_via_Multimodal_Large_Language_Models.pdf]]
