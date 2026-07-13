---
title: "Towards GUI Agents: Vision-Language Diffusion Models for GUI Grounding"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Towards_GUI_Agents_Vision_Language_Diffusion_Models_for_GUI_Grounding.pdf
project_link: null
code_link: null
aliases:
- HMLVGG
- TGAVLDMGG
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 通过引入混合掩码调度（线性掩码 + 全确定性掩码），强制模型以锚点坐标 (x1,y1) 为条件预测边界框范围 (x2,y2)，从而显式建模空间几何依赖，提升边界框一致性。
primary_logic: 将离散扩散VLM（LLaDA-V）首次应用于GUI定位，并提出“粗定位（线性掩码）→ 精定位（全确定性掩码）”的混合掩码调度，利用扩散模型的迭代去噪与双向注意力捕获锚点-范围的层次结构，在不使用定位专有预训练的情况下逼近自回归基线。
claims:
- LLaDA-V 8B仅用7k Mind2Web样本微调即可达到80.67% SSR，证明离散扩散模型有能力完成GUI定位。
- 混合掩码相比线性掩码在多个数据集上将SSR提升1.3～6.1个百分点，最高达6.1%（VisualWebArena），同时维持接近饱和的动作类型F1。
- 将训练数据从7k扩展到120k多域GUI样本，平均SSR提升17～20点，推理延迟降低1～1.5秒，收敛步数减少8～9步。
- Mind2Web 上 SSR (%) = 83.90
---

# Towards GUI Agents: Vision-Language Diffusion Models for GUI Grounding

> [!tip] 核心洞察
> 将离散扩散VLM（LLaDA-V）首次应用于GUI定位，并提出“粗定位（线性掩码）→ 精定位（全确定性掩码）”的混合掩码调度，利用扩散模型的迭代去噪与双向注意力捕获锚点-范围的层次结构，在不使用定位专有预训练的情况下逼近自回归基线。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向GUI智能体的视觉-语言扩散模型用于GUI定位 |
| 英文题名 | Towards GUI Agents: Vision-Language Diffusion Models for GUI Grounding |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.26211) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | Hybrid Masking LLaDA-V for GUI Grounding |
| Dataset | Mind2Web, ScreenSpot-Web-Icon, ScreenSpot-Web-Text, VisualWebArena |

> [!tip] 效果简介
> - Mind2Web 上，SSR (%) 83.90 vs 82.40 (+1.50)。
> - ScreenSpot-Web-Icon (SWI) 上，SSR (%) 63.10 vs 57.80 (+5.30)。
> - ScreenSpot-Web-Text (SWT) 上，SSR (%) 74.80 vs 73.50 (+1.30)。

## 概要

GUI 智能体的核心能力之一是**GUI 定位**（GUI Grounding）——根据自然语言指令，在界面截图中准确定位目标元素并预测操作动作。当前主流方案几乎完全依赖**自回归视觉语言模型**（AR VLM），但这类模型受限于顺序解码与单向注意力，难以显式建模“锚点-范围”的空间几何依赖。离散扩散视觉语言模型（DVLM）具备双向注意力与迭代去噪的天然优势，却在 GUI 定位领域从未被探索。

本文首次将离散扩散 VLM **LLaDA-V** 引入 GUI 定位任务，并提出**混合掩码调度**（Hybrid Masking Schedule）来克服直接迁移面临的挑战。核心瓶颈在于：标准线性掩码无法强制模型学习“以锚点坐标 $(x_1, y_1)$ 为条件预测边界框范围 $(x_2, y_2)$”的结构化依赖。混合掩码通过两阶段设计解决这一问题——**线性掩码阶段**进行粗定位，预测动作类型与锚点；**全确定性掩码阶段**则锚定已知锚点，强制模型推断完整的边界框范围，从而显式建模空间层次关系。

在仅使用 7k Mind2Web 样本微调的情况下，LLaDA-V 8B 即达到 **80.67% 的步成功率**（SSR），证明了离散扩散模型完成 GUI 定位的可行性。混合掩码在此基础上进一步将 SSR 提升 **1.3～6.1 个百分点**（最高增益出现在 VisualWebArena 上），同时维持接近饱和的动作类型 F1。将训练数据从 7k 扩展到 120k 多域 GUI 样本后，平均 SSR 再提升 **17～20 点**，推理延迟降低 **1～1.5 秒**，收敛所需扩散步数减少 **8～9 步**。

值得注意的是，该方法**未使用任何定位专有预训练**，而对比的自回归基线（如 Qwen2.5-VL）通常受益于大规模定位预训练。这凸显了扩散模型在结构化视觉定位任务中的潜力，同时也揭示了当前方法在零样本泛化、多步动作预测以及推理延迟方面仍存在的显著差距。

### 1. GUI 智能体的核心挑战：视觉定位

GUI 智能体的核心能力之一是**视觉定位**（GUI Grounding）——根据自然语言指令，在 GUI 截图中准确定位目标元素并预测相应的交互动作。形式化地，给定一张 GUI 截图和一条任务指令，模型需要输出一个动作预测 $a = [a_{\mathrm{type}}, B]$，其中 $a_{\mathrm{type}}$ 为动作类型（如点击、悬停、输入），$B = (x_1, y_1, x_2, y_2)$ 为归一化至 $[0,1000]$ 的边界框坐标。$(x_1, y_1)$ 锚定交互位置，$(x_2, y_2)$ 定义元素的空间范围。这一任务要求模型同时具备视觉理解、指令解析和精确的空间坐标推理能力。

### 2. 自回归视觉语言模型的结构性瓶颈

当前主流的 GUI 定位方法几乎全部建立在**自回归视觉语言模型**（AR VLM）之上，如 **Qwen2.5-VL** 和 **Phi-3-Vision**。这些模型以从左到右的顺序逐 token 生成坐标序列，其架构存在两个根本性的结构限制：

- **顺序解码**：坐标 token 必须严格按序生成，无法并行化，导致推理延迟与序列长度线性相关。
- **单向注意力**：每个 token 只能关注其左侧的上下文，无法利用右侧信息进行双向推理。在预测 $(x_2, y_2)$ 时，模型无法显式地以 $(x_1, y_1)$ 为条件进行反向校验，这限制了边界框的空间一致性。

这些限制在 GUI 定位场景中尤为突出：边界框的四个坐标之间存在天然的几何依赖关系，而自回归架构只能通过隐式的单向序列建模来捕捉这种依赖。

### 3. 离散扩散模型：一个未被探索的替代方案

**离散扩散视觉语言模型**（Discrete Diffusion VLM, DVLM）提供了一种潜在的替代范式。与自回归模型不同，离散扩散模型通过**迭代去噪**过程生成文本——从完全掩码的序列开始，逐步预测被掩码的 token，最终恢复完整输出。其核心优势在于：

- **双向注意力**：每个 token 可以同时关注序列中的所有其他位置，天然适合建模坐标之间的双向几何约束。
- **并行解码**：理论上支持同时预测多个 token，有望降低推理延迟。

然而，在本文工作之前，**离散扩散 VLM 在 GUI 定位任务中的可行性与潜力尚未被探索**。这一空白构成了本文的核心研究动机：扩散模型的迭代去噪与双向注意力机制是否能够有效捕获 GUI 定位中的空间结构依赖？

### 4. 本文动机与研究问题

基于上述背景，本文提出以下核心研究问题：

1. **可行性验证**：离散扩散 VLM 能否在 GUI 定位任务上达到可用精度？是否存在根本性的架构障碍？
2. **结构化建模**：如何设计掩码策略，使扩散模型显式地学习锚点坐标 $(x_1, y_1)$ 与范围坐标 $(x_2, y_2)$ 之间的层次依赖关系？
3. **性能边界**：在不使用定位专有预训练的前提下，扩散模型与自回归基线的差距有多大？数据扩展和推理优化能否缩小这一差距？

为回答这些问题，本文选择 **LLaDA-V** 作为基础离散扩散 VLM，将其首次适配到 GUI 定位任务，并提出一种**混合掩码调度**策略，通过“粗定位→精定位”的两阶段掩码设计，引导模型显式建模锚点-范围的几何依赖。

## 核心方法与创新机理

本工作的核心创新在于将**离散扩散视觉语言模型（DVLM）**首次引入GUI定位任务，并通过**混合掩码调度（Hybrid Masking Schedule）**显式建模GUI动作的结构化几何依赖，从而在无需定位专有预训练的情况下逼近自回归基线。

### 瓶颈与动机：自回归架构的结构性限制

自回归视觉语言模型（AR VLM）在GUI定位中面临两个根本性约束：**顺序解码**导致推理延迟随序列长度线性增长，**单向注意力**则限制了模型对空间坐标间双向依赖的建模能力。对于一个典型的GUI动作预测 `a = [a_type, x1, y1, x2, y2]`，AR模型必须逐token生成，无法在生成锚点 `(x1, y1)` 时利用尚未生成的边界框范围 `(x2, y2)` 信息——而这种**锚点-范围的双向几何约束**恰恰是准确定位的关键。

离散扩散模型（如LLaDA-V）天然具备**双向注意力**和**迭代去噪**能力，理论上更适合捕获这种结构化依赖，但其在GUI定位任务中的可行性与潜力此前完全未被探索。

### 核心因果机制：混合掩码调度

本文的核心操作变量（causal knob）是**掩码调度策略**。基线LLaDA-V使用默认的**线性掩码**：每个token被替换为 `[M]` 的概率随扩散时间步线性增长，即 $p_{\text{mask}} = (1 - \varepsilon) t + \varepsilon$，其中 $t \sim \mathcal{U}(0,1)$。这种策略对所有token一视同仁，无法区分动作类型、锚点坐标与范围坐标的不同语义角色。

提出的**混合掩码调度**将训练过程分为两个互补阶段：

- **阶段一：线性掩码（粗定位）**。与基线一致，对完整动作序列 `[a_type, x1, y1, x2, y2]` 施加随机掩码，迫使模型学习从视觉上下文和自然语言指令中恢复被掩码的token。此阶段确保模型获得基本的动作类型识别和粗略空间定位能力。

- **阶段二：全确定性掩码（精定位）**。将边界框范围坐标 `(x2, y2)` 确定性、全部替换为 `[M]`，同时保持动作类型和锚点 `(x1, y1)` 完全可见。这强制模型以已知的锚点坐标为条件，预测边界框的空间范围，显式建模 **“给定锚点，推断范围”** 的几何依赖关系。

两个阶段在训练中交替执行，使模型同时掌握两种推理模式：去噪重建完整动作序列的能力，以及从锚点推导边界框范围的条件生成能力。

### 核心洞察：扩散架构与GUI定位的结构性适配

这一设计的深层洞察在于：**离散扩散模型的迭代去噪过程天然适配GUI定位的层次化结构**。边界框的锚点 `(x1, y1)` 定义了交互的“位置”，而范围 `(x2, y2)` 定义了交互的“尺度”——两者之间存在明确的几何约束（如 `x2 > x1`, `y2 > y1`）和语义关联（如按钮的锚点通常位于其左上角，范围取决于按钮尺寸）。混合掩码通过将这种先验结构注入训练信号，使扩散模型的双向注意力能够同时感知锚点与范围的全局约束，从而生成更一致、更准确的边界框。

### 与基线方法的差异定位

| 维度 | 线性掩码基线 | 混合掩码（本文） |
|------|-------------|-----------------|
| 掩码策略 | 所有token等概率随机掩码 | 阶段一随机掩码 + 阶段二确定性掩码 `(x2,y2)` |
| 几何依赖建模 | 隐式，依赖模型自主发现 | 显式，强制锚点→范围的条件生成 |
| 训练信号 | 纯重建损失 | 重建 + 条件推理的双重信号 |
| 推理行为 | 通用去噪 | 可分离的粗-精两阶段推理 |

### 证据强度与边界

决定性证据表明混合掩码在多个基准上一致提升步成功率（SSR），最高达+6.1个百分点（VisualWebArena），同时维持接近饱和的动作类型F1（Table 4/Table 7）。然而，这一创新的有效性边界同样明确：**零样本性能极差（SSR接近0%）**，说明混合掩码调度本质上是一种**任务特定的结构化先验注入**，而非通用的泛化能力增强——它依赖于训练数据中GUI动作的结构化格式，无法自动迁移到未见过的输出模式。此外，混合掩码引入的串行依赖（先锚点后范围）在推理时带来了额外的顺序计算开销，需要通过减少扩散步数进行精度-延迟权衡。

### 任务形式化

GUI 定位被建模为一个条件文本生成问题。给定自然语言指令 $N$ 和 GUI 截图 $I$，模型需要学习映射 $M: (N, I) \to a$，其中 $a = [a_{\mathrm{type}}, B]$ 包含动作类型（如 `lclick`、`hover`、`type_in`）和边界框 $B = (x_1, y_1, x_2, y_2)$。坐标归一化至 $[0, 1000]$，$(x_1, y_1)$ 锚定动作位置，$(x_2, y_2)$ 定义空间范围。预测成功的判据为：动作类型匹配真值，且预测框中心落入真值框内（即 Step Success Rate, SSR），而非 IoU 阈值。

### 基础架构：LLaDA-V 的 GUI 适配

本工作以离散扩散视觉语言模型 **LLaDA-V** 为基座，将其从通用多轮对话适配为单轮 GUI 定位。LLaDA-V 的核心组件包括：

- **视觉编码器**：SigLIP-2，提取 GUI 截图的视觉特征。
- **语言模型**：LLaDA，作为离散扩散语言模型，负责多模态条件生成。
- **MLP 投影器**：两层 MLP，将视觉嵌入对齐到语言模型的 token 空间。

原始 LLaDA-V 采用两轮对话的离散扩散训练目标（见公式 1），对掩码 token 进行重建。为适配 GUI 定位，本工作将其简化为单轮训练目标：

$$L(\theta) = -\mathbb{E}_{v,p_0^1,r_0^1,r_t^1,t} \left[ \frac{1}{t} \sum_{i=1}^{L_{r1}} \mathbf{1}[r_t^{1,i}=[M]] \times \log p_\theta(r_0^{1,i} \mid v, p_0^1, r_t^1) \right]$$

其中 $v$ 为视觉特征，$p_0^1$ 为指令 prompt，$r_0^1$ 为完整动作序列，$r_t^1$ 为掩码后的序列。模型从视觉和指令条件中恢复被掩码的动作 token。

### 混合掩码调度：粗定位到精定位

这是本工作的核心创新。标准 LLaDA-V 使用线性掩码调度（masking probability 随扩散步数线性增长），但在 GUI 定位中，该方法无法显式建模锚点 $(x_1, y_1)$ 与范围 $(x_2, y_2)$ 之间的空间几何依赖。为此，提出**混合掩码调度**，分为两个互补阶段：

1. **线性掩码阶段（粗定位）**：与默认调度一致，每个 token 被替换为 `[M]` 的概率为 $p_{\mathrm{mask}} = (1 - \varepsilon) t + \varepsilon$，其中 $t \sim \mathcal{U}(0,1)$，$\varepsilon$ 防止完全掩码。该阶段使模型学习从部分可见的动作序列中恢复完整结构。

2. **全确定性掩码阶段（精定位）**：以线性掩码阶段预测的锚点 $(x_1, y_1)$ 为条件，将 $(x_2, y_2)$ 的全部 token 确定性掩码，强制模型基于已知锚点推理边界框范围。这显式建模了“锚点→范围”的层次空间依赖。

训练时两阶段交替执行，推理时先通过迭代去噪生成锚点，再以锚点为条件生成范围。这一设计利用扩散模型的**双向注意力**和**迭代去噪**能力，在不引入定位专有预训练的前提下，逼近自回归基线的精度（见 Table 7，混合掩码在四个基准上将 SSR 提升 1.3～6.1 个百分点）。

### 数据流与训练配置

训练数据从 Mind2Web 的 7k 样本扩展至覆盖 web、mobile、desktop 三域的 120k 样本（Mind2Web、WebLinX、OS-Atlas、Rico Widget Caption），并采用随机裁剪与 OCR 文本标注提升标注质量（Table 3 显示该策略带来 2.68 点 SSR 提升和 0.38 秒延迟降低）。数据扩展使平均 SSR 提升 17～20 点，推理延迟降低 1～1.5 秒，收敛步数减少 8～9 步（Figure 3）。

![[assets/figures/papers/paper_list_l2349_https_arxiv_org_abs_2603_26211/figures/001_Figure_1.jpg]]
*Figure 1: Overview of Hybrid Masking Adaptation of LLaDA-V for GUI Grounding. (a) The adapted framework takes a naturallanguage instruction and a GUI screenshot (either from web, desktop, or mobile interfaces) as input. LLaDA-V trained with the linear masking predicts the action type, optional type in text, and anchor coordinates*

### 4.1 单轮 GUI 定位的离散扩散建模

LLaDA-V 原本面向两轮对话设计，其扩散损失对两轮回复中所有掩码 token 进行重建（见公式 1）。为适配单轮 GUI 定位，作者将任务简化为：给定自然语言指令 $N$ 和 GUI 截图 $I$，模型直接预测动作字符串 $a = [a_{\mathrm{type}}, B]$，其中 $B = (x_1, y_1, x_2, y_2)$ 为归一化到 $[0,1000]$ 的边界框坐标。

单轮训练目标（公式 2）仅对回复序列 $r^1$ 中被掩码的 token 求负对数似然：

$$L(\theta) = -\mathbb{E}_{v,p_0^1,r_0^1,r_t^1,t} \left[ \frac{1}{t} \sum_{i=1}^{L_{r1}} \mathbf{1}[r_t^{1,i}=[M]] \times \log p_\theta(r_0^{1,i} \mid v, p_0^1, r_t^1) \right]$$

其中 $v$ 为视觉特征，$p_0^1$ 为指令 prompt，$r_0^1$ 为真实动作 token 序列，$r_t^1$ 为扩散步 $t$ 时被部分掩码的序列，$[M]$ 表示掩码 token。

### 4.2 混合掩码调度

核心创新在于将训练过程划分为两个互补阶段，显式建模锚点坐标 $(x_1,y_1)$ 与边界框范围 $(x_2,y_2)$ 之间的空间几何依赖。

**阶段一：线性掩码（粗定位）**

沿用 LLaDA-V 默认的线性掩码策略，每个 token 被替换为 $[M]$ 的概率为：

$$p_{\mathrm{mask}} = (1 - \varepsilon) t + \varepsilon, \quad t \sim \mathcal{U}(0,1)$$

其中 $\varepsilon$ 为防止完全掩码的小常数。此阶段强制模型从任意掩码比例中恢复完整动作序列，学习动作类型与边界框的联合分布。

**阶段二：全确定性掩码（精定位）**

在给定锚点 $(x_1,y_1)$ 的条件下，将边界框范围 $(x_2,y_2)$ 对应的所有 token 确定性掩码为 $[M]$，而动作类型和锚点坐标保持可见。模型必须基于已知锚点推理出合理的空间范围，从而显式捕获“锚点→范围”的层次依赖。

训练时交替使用两种掩码策略，推理时则采用串行流程：先以线性掩码扩散解码生成完整动作序列（含粗略边界框），再以全确定性掩码对 $(x_2,y_2)$ 进行精修。

### 4.3 流水线模块

| 模块 | 功能 |
|---|---|
| Vision Encoder (SigLIP-2) | 提取 GUI 截图的视觉特征 |
| MLP Projector | 两层 MLP，将视觉特征对齐到语言模型的 token 空间 |
| Language Model (LLaDA) | 离散扩散语言模型，以双向注意力进行多模态条件生成 |
| Hybrid Masking Scheduler | 训练时交替调度线性掩码与全确定性掩码，引导模型学习锚点-范围依赖 |

### 4.4 评估指标公式

**步成功率 (Step Success Rate, SSR)**：预测框中心落入真值框内的实例比例。

$$\mathrm{SSR} = \frac{1}{N} \sum_{i=1}^{N} \mathbf{1}[c_p^{(i)} \in B_g^{(i)}], \quad c_p = \left( \frac{x_1^p+x_2^p}{2}, \frac{y_1^p+y_2^p}{2} \right)$$

其中 $c_p$ 为预测框中心坐标，$B_g$ 为真值框。该判据比 IoU 更贴近 GUI 操作场景——只要点击位置落入目标元素区域即视为成功。

**动作类型 F1**：衡量对 `lclick`、`hover`、`type_in` 三类动作的分类精度，采用宏平均计算：

$$\mathrm{F1} = \frac{2 \times \mathrm{Precision} \times \mathrm{Recall}}{\mathrm{Precision} + \mathrm{Recall}}$$

## 实验与关键发现

### 核心发现：离散扩散VLM的GUI定位能力验证

本工作首次将离散扩散视觉语言模型（DVLM）LLaDA-V引入GUI定位任务。在仅使用Mind2Web训练集（约7k样本）进行微调的条件下，LLaDA-V 8B即可在测试集上达到**80.67%的步成功率（SSR）**和**99%的动作类型F1**（Table 2），证明离散扩散范式有能力完成结构化坐标预测，而非自回归模型的专属领地。

![[assets/figures/papers/paper_list_l2349_https_arxiv_org_abs_2603_26211/figures/004_Table_2.jpg]]
*Table 2: LLaDA-V 8B fine-tuned only on the Mind2Web training set (7k samples) without cropping and OCR-based target annotation, trained for 10 epochs. The fine-tuned model was evaluated on the Mind2Web test set*

这一结果背后的机制在于扩散模型的**双向注意力**：与自回归模型只能从左到右顺序解码不同，LLaDA-V在去噪过程中可以同时关注所有token，使动作类型（`lclick`/`hover`/`type_in`）、锚点坐标 $(x_1, y_1)$ 和范围坐标 $(x_2, y_2)$ 之间实现联合推理。然而，默认线性掩码调度下，模型仅以随机掩码率重建token，并未显式利用GUI动作的层次结构——锚点定义交互位置，范围定义空间延展——这为后续改进留下了空间。

### 混合掩码调度：从粗定位到精定位的结构化引导

针对上述瓶颈，我们提出**混合掩码调度（Hybrid Masking Schedule）**，将训练过程分为两个互补阶段：

- **阶段一（线性掩码，粗定位）**：以概率 $p_{\text{mask}} = (1 - \varepsilon)t + \varepsilon$（$t \sim \mathcal{U}(0,1)$）随机掩码动作序列中的token，强制模型从视觉和指令上下文重建完整的动作字符串 $a = [a_{\text{type}}, x_1, y_1, x_2, y_2]$。此阶段建立“指令→动作类型→大致位置”的映射。
- **阶段二（全确定性掩码，精定位）**：固定保留锚点 $(x_1, y_1)$ 和动作类型，仅掩码范围坐标 $(x_2, y_2)$，迫使模型以已知锚点为条件预测边界框的右下角。这显式建模了 $(x_1, y_1) \rightarrow (x_2, y_2)$ 的空间几何依赖。

Table 4（主结果表）展示了混合掩码在四个基准上的增益：

![[assets/figures/papers/paper_list_l2349_https_arxiv_org_abs_2603_26211/figures/007_Table_4.jpg]]
*Table 4: AR vs. NAR GUI grounding comparison. The table reports GUI grounding performance on four benchmarks across the listed evaluation metrics. The rightmost column (in grey) highlights our proposed LLaDA-V variant trained with the hybrid linear and deterministic masking schedule*

| 基准 | 线性掩码 SSR (%) | 混合掩码 SSR (%) | Δ SSR |
|------|-----------------|-----------------|-------|
| Mind2Web | 82.40 | **83.90** | +1.50 |
| ScreenSpot-Web-Icon | 57.80 | **63.10** | +5.30 |
| ScreenSpot-Web-Text | 73.50 | **74.80** | +1.30 |
| VisualWebArena | 61.40 | **67.50** | +6.10 |

混合掩码在所有基准上均取得正向增益，其中**VisualWebArena提升最为显著（+6.1点）**，ScreenSpot-Web-Icon次之（+5.3点）。这两个基准的共性在于需要精确定位图标级UI元素，说明确定性掩码阶段对细粒度空间推理尤为关键。定性对比（Figure 2, Figure 5）进一步证实：混合掩码模型预测的边界框更紧凑、更贴合真值，而纯线性掩码模型倾向于产生偏移或过大的框。

值得注意的是，动作类型F1在所有设置下均接近饱和（>98%），说明SSR的瓶颈不在动作分类，而在**坐标精度**——这正是混合掩码着力解决的问题。

### 推理参数与延迟的消融分析

扩散模型的推理成本由三个关键参数控制：**扩散步数（diffusion steps）**、**生成长度（generation length）**和**块长度（block length）**。Table 2给出了在Mind2Web 7k微调设定下的消融结果：

- 将三个参数从32增至64，SSR提升**2.5点**（从约78%升至80.5%），但平均推理延迟**接近翻倍**。
- 继续增大参数（如128步），精度趋于饱和（~80%），收益递减。

这表明扩散步数在32–64区间内是精度-延迟的有效调控旋钮。Table 7进一步展示了混合掩码下的延迟-精度权衡：通过减少扩散步数，可在**极小精度损失**下大幅降低延迟（例如从Table 7中间列降至最右列），使扩散模型在部署场景中更具竞争力。

### 数据规模与标注质量的扩展效应

数据扩展实验（Figure 3, Table 1）揭示了两个关键规律：

![[assets/figures/papers/paper_list_l2349_https_arxiv_org_abs_2603_26211/figures/005_Figure_3.jpg]]
*Figure 3: GUI Data Scaling behavior of LLaDA-V 8B trained with Linear Masking: Comparison between LLaDA-V 8B trained on 7k web GUI samples from Mind2Web and 120k mobile, web and desktop GUI samples across four GUI grounding datasets. M2W: Mind2Web, SWT: ScreenSpot-Web-Text, SWI: ScreenSpot-Web-Icon, VWA: Visual Web Arena. Left plot shows Step Sucess Rate (SSR), the center plot shows the number of Converged Steps, and right shows average Inference Latency measured in seconds. Training with large-scale GUI multi-domain data improves SSR, reduces the number of Converged Steps required to produce a highly confident output while reducing Inference Latency, demonstrating better generalization and efficienc...*

![[assets/figures/papers/paper_list_l2349_https_arxiv_org_abs_2603_26211/figures/002_Table_1.jpg]]
*Table 1: Training data composition for data scaling experiments. The dataset spans web, mobile, and desktop domains, totaling 120K samples*

1. **规模效应**：将训练数据从7k（纯Mind2Web网页域）扩展至**120k多域混合数据**（覆盖web、mobile、desktop），平均SSR提升**17–20点**，推理延迟降低**1–1.5秒**，收敛所需扩散步数减少**8–9步**。这说明多域GUI数据不仅提升精度，还使扩散去噪过程更高效——模型学到了更泛化的GUI先验，减少了迭代修正需求。

2. **标注质量效应**：Table 3显示，在Mind2Web 7k设定下，引入**随机裁剪**和**OCR引导的目标标注**使SSR提升**2.68点**，延迟降低**0.38秒**。OCR标注提供了更精确的文本元素边界框，减少了训练目标中的噪声；随机裁剪则增强了模型对局部区域的鲁棒性。Figure 4的定性对比直观展示了这一改善。

### 与自回归基线的差距分析

尽管混合掩码LLaDA-V在四个基准上均逼近自回归基线（Table 4），但差距仍然存在。在Mind2Web上，Qwen2.5-VL 7B的SSR高出约10–15点。这一差距的核心原因在于：

- **定位预训练的缺失**：自回归VLM（如Qwen2.5-VL）通常经过大规模GUI定位专有预训练，而LLaDA-V仅使用通用多模态预训练权重，未接触任何定位任务。
- **零样本能力极弱**：Table 5显示LLaDA-V 8B在Mind2Web上的零样本SSR**接近0%**，说明当前模型完全依赖微调，缺乏泛化到全新GUI环境的能力。

### 失败模式与局限性

综合实验证据，当前方法存在以下明确失败模式：

1. **单步动作局限**：所有评估仅涉及单步动作预测（给定指令→输出动作），未覆盖多步规划、工具调用等真实GUI智能体场景。混合掩码的串行依赖（先锚点后范围）在多轮交互中可能累积延迟。

2. **评估指标的局部对齐偏差**：SSR以“预测框中心落入真值框”为成功判据（公式见附录D），而非IoU。这更贴近GUI点击操作的实用需求，但可能高估局部对齐——一个过大的预测框只要中心正确即算成功。

3. **混合掩码的额外计算开销**：确定性掩码阶段引入的串行依赖（必须先生成锚点再生成范围）增加了顺序计算负担，在低扩散步数下仍比纯线性掩码略慢（Table 7）。

![[assets/figures/papers/paper_list_l2349_https_arxiv_org_abs_2603_26211/figures/010_Table_7.jpg]]
*Table 7: Accuracy–Latency Trade-Off with Hybrid Masking. The table compares LLaDA-V trained with default linear masking (third column) and our hybrid masking (fourth and fifth columns) across four benchmarks. The hybrid model achieves higher SSR but with slightly higher latency, while reducing diffusion steps lowers latency with minimal loss in accuracy*

4. **数据集覆盖有限**：虽然120k数据覆盖三域，但未在动态网页、跨应用操作等真实交互环境中验证，泛化性存疑。

## 定位与知识库关联

### 方法定位：离散扩散 VLM 首次进入 GUI 定位

本文的工作处于**离散扩散视觉语言模型（DVLM）**与**GUI 智能体感知**的交叉点。在本文之前，GUI 定位任务几乎完全由自回归视觉语言模型（AR VLM）主导，离散扩散模型在该任务上的可行性与潜力从未被探索。作者将 **LLaDA-V**（一种基于离散扩散的 VLM）首次适配到 GUI 定位任务，填补了这一空白。

从模型架构谱系看，LLaDA-V 本身继承了两条技术路线：
- **离散扩散语言模型**：LLaDA 的非自回归生成机制，通过迭代去噪从完全掩码的序列恢复目标文本，天然具备双向注意力能力。
- **多模态对齐范式**：采用视觉编码器（SigLIP-2）+ MLP 投影器 + 语言模型的经典架构，与 LLaVA 系列等主流 VLM 共享相似的视觉-语言桥接设计。

### 与自回归基线的关系

本文的核心对比对象是自回归 VLM，包括 **Qwen2.5-VL**（3B/7B）和 **Phi-3-Vision**。这些模型代表当前 GUI 定位的主流技术路线，通常受益于大规模定位专有预训练（如 UI 元素检测、OCR 关联等）。

关键对比结论：
- **未使用定位专有预训练时**，LLaDA-V 8B 仅用 7k Mind2Web 样本微调即可达到 80.67% SSR（Table 2），证明离散扩散模型具备完成 GUI 定位的基本能力。
- **引入混合掩码调度后**，在四个基准上 SSR 提升 1.3～6.1 个百分点（Table 4/Table 7），将扩散模型与自回归模型的差距从约 25 点缩小至 15 点以内。
- **但差距依然显著**：自回归模型凭借单向注意力的顺序解码优势，在精度和推理延迟上仍整体领先，尤其在需要精确定位的场景中。

### 与其他非自回归/扩散方法的隐性对话

虽然本文未直接对比其他非自回归定位方法，但其技术选择与以下方向形成隐性对话：
- **Masked Generative Models**（如 MaskGIT、MAGE）：混合掩码调度中的“线性掩码”阶段与掩码生成模型的随机掩码训练策略具有相似性，但本文将其嵌入扩散框架，并通过“全确定性掩码”阶段引入了结构化的空间条件依赖。
- **目标检测中的扩散模型**（如 DiffusionDet）：这些工作将扩散用于连续坐标空间，而本文在离散 token 空间中对坐标进行建模，避免了连续-离散转换的精度损失。

### 适用边界与局限

本文方法的适用边界由以下因素共同界定：

**任务边界**：
- 仅支持**单步动作预测**（action type + bounding box），未扩展到多步规划、工具调用或交互流程。这意味着当前方法适用于“给定指令，定位并执行一步操作”的场景（如点击某个按钮），但无法处理“搜索航班 → 选择日期 → 填写表单”的复合任务。
- 评估采用 **SSR（预测框中心落入真值框）** 而非 IoU，这更贴近 GUI 操作的实际需求，但也意味着局部对齐即可判定成功，可能高估模型在需要精确边界框的场景（如拖拽操作）中的表现。

**数据边界**：
- 训练数据覆盖 Web（Mind2Web、WebLinX）、移动端（OS-Atlas mobile、Rico Widget Caption）和桌面端（OS-Atlas desktop）三个域，总计 120k 样本。但数据集仍有限，未在动态网页、跨应用操作等真实交互环境中验证。
- **零样本性能极差**（SSR 接近 0%，Table 5），表明当前模型严重依赖域内微调，缺乏泛化到全新 GUI 环境的能力。

**架构边界**：
- 混合掩码调度引入了**串行依赖**：模型必须先预测锚点 $(x_1, y_1)$，再以此为基础预测范围 $(x_2, y_2)$。这种设计虽然提升了空间一致性，但也带来了额外的顺序计算开销，与扩散模型本应具备的并行生成优势形成张力。
- 推理延迟虽然可通过减少扩散步数进行折中（Table 7），但混合掩码的精度优势在高延迟预算下才充分体现，低延迟场景下优势收窄。

### 开放问题与后续方向

本文打开的开放问题包括：

1. **多步扩散式 GUI 智能体**：如何将离散扩散模型从单步动作预测扩展到多步规划与交互？这需要解决扩散模型在序列决策中的信用分配和长期规划问题，可能的路径包括将扩散过程与强化学习或规划算法结合。

2. **GUI 定位专有预训练**：当前扩散模型与自回归模型的差距主要源于后者的大规模定位预训练。能否设计针对 GUI 的扩散预训练任务（如大规模 UI 元素定位、OCR-坐标关联、跨界面元素匹配）来缩小这一差距？这类似于目标检测中 DETR 类方法的预训练策略。

3. **结构化约束与高效采样**：是否可以在扩散解码中引入针对 GUI 动作的结构化约束（如坐标单调性、有效区域限制）或高效采样策略（如针对坐标 token 的自适应步数分配），进一步降低延迟？

4. **混合掩码调度的泛化性**：混合掩码的核心思想——“先粗后精”的两阶段空间依赖建模——是否适用于其他结构化视觉定位任务？例如文档版面分析（先定位段落锚点再确定边界）、目标检测（先确定物体中心再回归边界框）等场景。这需要验证锚点-范围分解在其他任务中的适用性。

5. **零样本泛化机制**：当前模型的零样本性能极差，说明扩散模型的去噪过程高度依赖训练分布。如何通过 Prompt 设计、测试时适应或元学习策略提升跨域泛化能力，是实用化的关键瓶颈。

## 原文 PDF

![[paperPDFs/CVPR_2026/Towards_GUI_Agents_Vision_Language_Diffusion_Models_for_GUI_Grounding.pdf]]
