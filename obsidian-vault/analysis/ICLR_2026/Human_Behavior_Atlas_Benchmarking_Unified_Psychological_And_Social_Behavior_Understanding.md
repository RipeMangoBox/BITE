---
title: "Human Behavior Atlas: Benchmarking Unified Psychological And Social Behavior Understanding"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Human_Behavior_Atlas_Benchmarking_Unified_Psychological_And_Social_Behavior_Understanding.pdf
project_link: null
code_link: https://github.com/MIT-MI/human_behavior_atlas
aliases:
- HBAO7SBR
- HBABUPSBU
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/vision_multimodal
core_operator: "通过构建一个大规模、多模态、标准化的统一基准（HUMAN BEHAVIOR ATLAS），并在其上进行多任务联合训练（SFT、RL）以及灵活的迁移学习，使得模型能够获取跨任务的通用行为理解能力。"
primary_logic: "将13个异构的多模态行为数据集统一为prompt-target格式，并提取行为描述符作为辅助信号，不仅解决了数据互操作性问题，还使同一基础模型在多个任务上超越现有模型；预训练于该基准能显著提高向新行为数据集的迁移效率，而行为描述符的残差式集成（BAM）可在不破坏主干表示的前提下有针对性地增强微弱行为信号的感知。"
claims:
- "在多任务训练中，OMNISAPIENS-7B SFT和BAM在10个行为任务中的8个上优于通用多模态LLM。"
- "在迁移学习设置下，OMNISAPIENS-7B SFT在MUStARD（讽刺检测）上相对未预训练的相同架构（Qwen 2.5-Omni-7B SFT）提升39.1%（0.658 vs 0.473）。"
- "集成行为描述符的BAM模块显著提升了非言语沟通（NVC +33%）和讽刺检测（SAR +29%）的性能。"
- "移除原始音频/视频特征（ABL）后，NVC性能下降50.41%（从0.16降至0.06），证明了行为描述符的重要性。"
---

# Human Behavior Atlas: Benchmarking Unified Psychological And Social Behavior Understanding

> [!tip] 核心洞察
> 将13个异构的多模态行为数据集统一为prompt-target格式，并提取行为描述符作为辅助信号，不仅解决了数据互操作性问题，还使同一基础模型在多个任务上超越现有模型；预训练于该基准能显著提高向新行为数据集的迁移效率，而行为描述符的残差式集成（BAM）可在不破坏主干表示的前提下有针对性地增强微弱行为信号的感知。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 人类行为图谱：面向统一心理与社会行为理解的基准 |
| 英文题名 | Human Behavior Atlas: Benchmarking Unified Psychological And Social Behavior Understanding |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=ZKE23BBvlQ) · [GitHub](https://github.com/MIT-MI/human_behavior_atlas) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_multimodal |
| Method | HUMAN BEHAVIOR ATLAS + OMNISAPIENS-7B (SFT / BAM / RL) |
| Dataset | CMU-MOSEI (SEN), MUStARD (SAR), MELD (EMO), PTSD-in-the-Wild (PTSD) |

> [!tip] 效果简介
> - CMU-MOSEI (SEN) 上，Binary Weighted F1 为 OMNISAPIENS-7B SFT finetuned: 0.724，对比 Qwen 2.5-Omni-7B SFT (no Atlas pretrain): 0.612，变化 +0.112。
> - MUStARD (SAR) 上，Weighted F1 为 OMNISAPIENS-7B SFT finetuned: 0.658，对比 Qwen 2.5-Omni-7B SFT (no Atlas pretrain): 0.473，变化 +0.185 (+39.1%)。
> - MELD (EMO) 上，Mean Weighted Accuracy 为 OMNISAPIENS-7B SFT 0.711，对比 Qwen 2.5-Omni-7B 0.661，变化 +0.050。

## 概要
现有心理与社会行为理解系统多为单任务专用设计，数据集格式和评估协议高度异构，难以支撑能够全面覆盖情感、认知、病理、社交等多维度行为的通用基础模型。为此，本文提出《人类行为图谱》（Human Behavior Atlas）基准，通过统一13个公开多模态数据集的样本格式和评估协议，消除数据互操作性瓶颈，并基于该基准训练OMNISAPIENS‑7B系列模型（SFT/BAM/RL）。核心思路是：将异构数据重写为prompt‑target规范格式，并提取行为描述符（姿势、声学、转录）作为辅助信号，通过残差适配器（BAM）增强模型对微弱行为线索的感知。在多任务训练中，OMNISAPIENS‑7B SFT/BAM在10项行为任务中的8项超越通用多模态大语言模型；在迁移学习设置下，图谱预训练使讽刺检测（MUStARD）F1由0.473提升至0.658（+39.1%），BAM则进一步带来非言语沟通任务（NVC）+33%、讽刺检测（SAR）+29%的增益。消融研究证实，移除原始音视频特征后NVC性能骤降50.41%，凸显了行为描述符的关键性。这些结果验证了统一基准与适配器方法在构建通用行为理解模型上的有效性。



理解人类心理与社会行为的复杂性——涵盖情感、意图、精神状态及人际交互——是构建高人际智能AI的核心瓶颈。这些行为本质上是多模态的（融合言语、声调、面部表情和肢体动作），高度个性化，且往往依赖微妙、转瞬即逝的非言语线索。尽管多模态大语言模型（MLLM）已在一般视觉-语言任务上取得突破，将其扩展至全面的行为理解仍面临根本性障碍。

**现有方法缺口：数据孤岛与协议碎片化**  
当前的心理与社会行为分析生态主要由单任务专用系统主导。每个数据集围绕一个细分行为（如情感识别、抑郁筛查、讽刺检测）独立构建，采集设备、标注模式、输出格式和评价指标均高度异构（如连续评分、多类标签、自由文本）。这种碎片化带来了三重困境：  
- **互操作性缺失**：异构数据难以合并为统一训练语料，阻碍了跨任务知识共享与迁移学习。  
- **评估不可比**：不同数据集采用各自的特异性指标（如加权F1、均方误差、人工评判），无法横向比较同一模型在多种行为维度的综合能力。  
- **基础模型训练受阻**：通用MLLM即便在多任务设置下，也因缺乏标准化输入-输出接口而难以从分散的行为数据中习得鲁棒的行为表征。  

**动机：构建统一行为图谱，驱动通用行为基础模型**  
论文的动机在于颠覆这一单任务范式：通过构建一个大规模、多模态、标准化、覆盖多行为维度的统一基准（HUMAN BEHAVIOR ATLAS），为训练“通用心理与社会行为基础模型”提供可能性。该基准将13个公开多模态数据集按情感、认知、病理、社会四维行为分类（Section 3.1），并将所有样本重塑为统一的 prompt–target 格式（Section 3.2），同时定义了一套跨数据集的统一评估协议（Section 3.3）。更进一步，论文引入行为描述符（MediaPipe 姿态、OpenSMILE 声学特征、Whisper 转录）作为额外的符号化辅助信号，以弥补原始音视频难以捕捉的微表情和声学模式。  

这一整合性设计旨在实现三大关键因果效应：  
1. **多任务联合训练下的泛化增益**：在同一基准上混合训练，使单模型能够同时处理情感分析、意图推理、非言语沟通等10类行为任务，并超越同等规模的通用MLLM（在8/10任务上领先，Figure 2）。  
2. **强迁移能力**：Atlas 预训练后的模型仅需极少微调即可大幅提升在“陌生”行为数据集（如 MUStARD 讽刺检测、CMU-MOSEI 情感分析）上的表现，相较无预训练的同架构模型获得最高+39.1%的绝对提升（Table 5）。  
3. **即插即用的行为信号增强**：通过残差适配器（BAM）向冻结主干引入行为描述符，可在不损害原有多任务能力的前提下，针对性地增强微弱行为信号的感知（如 NVC 提升33%、SAR 提升29%，Table 6），为未来按需插入行为知识提供了高效通道。  

综上，本文的动机并非提出单一任务模型，而是通过构建标准化、高密度、可扩展的行为数据基础，推动心理与社会行为理解从“特设专用”迈向“统一基础模型”的新范式。



## 核心方法与创新机理

现有心理与社会行为分析系统的根本瓶颈在于各任务长期处于单任务专门化设计，其数据格式、标注目标和评估协议存在巨大差异，导致无法训练出一个能够全面理解多种行为维度的通用基础模型。HUMAN BEHAVIOR ATLAS 及配套的 OMNISAPIENS-7B 系列模型的核心创新，正是通过一系列“changed slots”系统性地打破这一碎片化壁垒，使异构数据交织为可联合训练的统一基准，从而在多任务学习、迁移学习与细粒度行为感知三个层面产生显著增益。

### 1. 从单任务孤立数据到多任务统一基准（训练数据与任务定义）

基线方法通常针对单一任务（如情感识别、讽刺检测）使用对应的特定数据集进行独立训练，模型无法共享行为理解知识。该工作将覆盖情感、认知、病理、社会四个行为维度共13个公开多模态数据集（涵盖10类行为任务）重新整合为一个**统一基准**（HUMAN BEHAVIOR ATLAS），并在其上进行**多任务联合训练**（SFT/RL）[Section 3.1; Section 4.1]。这使同一模型实例能够同时接触多种行为信号，学习跨任务的通用行为表征，从而在多任务测试中大幅超越以相同架构训练但无 Atlas 预训练的模型。

### 2. 从异构原始格式到标准化 Prompt-Target 对（数据格式）

以往数据集的输入输出格式高度异构——有的依赖预提取特征，有的采用连续评分，有的直接给出分类标签。该工作将所有样本重新构造为**统一的 prompt–target 格式**：prompt 显式引用可用模态（文本转录、音频、视频等），target 则统一为离散标签集或自由文本答案 [Section 3.2; Table 3]。这一格式转换是联合训练的数据互操作性基础，使异构来源的样本能够被同一模型所消费，且无须针对每个数据集定制预处理流程。

### 3. 从杂乱评估指标到统一评估协议

基线中各数据集分别使用加权准确率、F1、LLM 评判等不同指标，难以跨任务比较模型能力。该工作为每个行为任务指定**单一标准化指标**并全基准统一应用：SEN 用二元加权 F1，EMO 用平均每类加权准确率，一般分类任务用加权 F1，自由文本回答任务由 LLM-Judge 准确率评估 [Section 3.3; Table 2]。该统一评估框架不仅简化了实验分析，也为未来行为基础模型的公平比较提供了可靠、可复现的标准。

### 4. 从被动依赖原始信号到主动注入行为描述符（特征工程）

基线方法大多仅将原始视频/音频或手工特征作为额外输入单独处理，难以捕捉微弱的非言语线索。该工作可选地引入**行为描述符提取**——利用 MediaPipe 提取身体/面部特征、OpenSMILE 提取声学特征、Whisper 进行语音转录，从时间序列中生成静态全局行为向量 $$\mu_f, \sigma_f$$，并通过一个轻量的**行为适配器模块（Behavioral Adapter Module, BAM）**以残差方式集成到冻结的主干模型倒数第二层隐藏状态上：

$$
\Delta h_f = \alpha \cdot z_f, \quad h_{\mathrm{adapt}} = h_{\mathrm{penult}} + \Delta h_f
$$

其中 $$z_f$$ 是两层 MLP 对归一化行为向量的映射输出，$$\alpha$$ 为可学习缩放标量 [Section 3.6]。这种**即插即用**的残差设计使得在不破坏预训练主干表示的前提下，有针对性地增强模型对细微行为信号（如转瞬即逝的微笑）的感知，而无需修改或微调主模型。

### 5. 从单一输出头到混合架构（模型输出头）

多数基线使用单一任务特定的分类头或生成式解码器。OMNISAPIENS-7B 系列则提供两种互补设计：
- **SFT 混合架构**：对结构化分类任务采用任务特定分类头，对开放生成任务采用 LLM 解码头，同时优化两种输出形式；
- **RL 纯解码器架构**：所有任务均通过单一解码器输出，利用 GRPO 强化学习优化回答准确度、格式合规性和语义相似度的复合奖励 [Section 3.5, 3.7; Appendix B.2]。

混合头设计保障了结构化识别任务（如情感分类）的高精度，而 RL 纯解码器为需要社会推理或意图推断的开放式任务带来了更强的推理能力。

### 创新有效性验证

上述 changed slots 的联合效果在实验中得到了充分证实：
- **多任务性能**：OMNISAPIENS-7B SFT 在 10 个行为任务中的 8 个上超越通用多模态 LLM（如 Gemma-3-4B、HumanOmniV2-7B 等），且在 7 个任务上领先于 HumanOmniV2-7B [Figure 2; Section 4.1]。
- **迁移能力**：在零样本和少样本迁移设置下，经过 Atlas 预训练的 OMNISAPIENS-7B SFT 在 MUStARD 讽刺检测上相比未预训练的同一架构（Qwen 2.5-Omni-7B SFT）提升 **+39.1%**（0.658 vs 0.473），在其他保留数据集上同样呈现系统性增益 [Table 5; Section 4.2]。
- **行为描述符的定向增强**：BAM 模块使得非言语沟通（NVC）性能相对 SFT 基线提升 **+33%**，讽刺检测（SAR）提升 **+29%**，且当移除原始音频/视频特征后 NVC 性能暴跌 **50.41%**，证明行为描述符对细粒度非言语任务不可或缺 [Table 6; Table 10; Section 4.3 & Appendix D.4]。

综上，HUMAN BEHAVIOR ATLAS 的创新并非单一算法改进，而是通过系统性地重构数据、任务、评估与模型接口这五个关键“槽位”，将行为理解从割裂的单任务训练范式推进到可扩展、可迁移的多任务基础模型范式。



![[assets/figures/papers/iclr26_0013_ZKE23BBvlQ_Human_Behavior_Atlas_Benchmarking_Unified_Psycho/figures/006_Figure_1.jpg]]
*Figure 1: Overview of HUMAN BEHAVIOR ATLAS. (a) Selection criteria and preprocessing pipeline of datasets. (b) Dataset distribution across 10 behavior related tasks. Inner circle indicates the modality combination of the input data, where T=Text, A=Audio and V=Video. Middle ring describes the tasks of the dataset, as defined in Sec. 3.1. The outer ring and bars lists the datasets and its sample sizes respectively. (c) Distribution of data modalities. Our dataset has a focus on video understanding as it comprises both vision and audio modalities, with 83.6% of samples containing video data. (d) Distribution of sample durations. Both short and long videos/audio tasks are covered, with 29.2% of video/au...*

为克服现有心理与社会行为理解领域“数据格式异构、评估协议割裂、模型单任务孤立”的根本瓶颈，**HUMAN BEHAVIOR ATLAS** 提出了一套以标准化多任务联合训练为核心的统一基准与建模范式。整体框架由**基准构建、行为信号增强、多任务联合训练**三个层次构成，各模块之间形成清晰的输入‑输出流，共同支撑从多模态感知到细粒度行为理解的通用基础模型。

### 1. 基准构建与数据统一
整个流程的入口是 **13 个公开多模态数据集**，覆盖视频、音频、文本及其组合。这些数据集首先被按“情感状态、认知状态、病理状态、社会过程”四个行为维度进行分类与整理（Section 3.1），随后全部被重构为**统一的 prompt‑target 格式**（Section 3.2）。具体而言，每个样本被重写为一个 prompt（显式引用可用的模态，如视频、音频、文本转录）和一个 target（离散标签集或自由文本）。例如，MELD 中的原始数据被转换为“给定视频、音频和转录，判断情感类别”的对话式指令（Table 3）。这一标准化消除了跨数据集的互操作障碍。

与此同时，框架为每个行为任务**指定了单一的标准化评估指标**（Section 3.3）：情感分析采用二元加权 F1，多类别情绪识别采用平均每类加权准确率，分类任务采用加权 F1，自由文本问答则通过 LLM‑Judge 准确率衡量。所有指标被统一应用于关联的所有数据集，确保了跨实验、跨任务的可比性。

### 2. 行为描述符提取与增强
在原始多模态输入之外，框架透过多款专家工具提取**符号级行为描述符**作为辅助信号，以补偿深度神经网络对微弱行为线索（如微表情、声学韵律）的感知不足（Section 3.4）。具体流程如下：
- 使用 **MediaPipe** 从视频中提取面部关键点、姿势与微表情；
- 使用 **OpenSMILE** 从音频中提取声学特征（如基频、能量、MFCC）；
- 使用 **Whisper** 获取精确的文本转录。
这些原始时序特征 $\mathbf{f}_{\mathrm{raw}} \in \mathbb{R}^{T \times D_{\mathrm{raw}}}$ 随后通过均值‑标准差池化压缩为静态全局向量 $\mathbf{f} = [\mu_{f}, \sigma_{f}]$，并作为后续模型的可选增补信息。

### 3. 多任务联合建模与训练范式
在统一基准之上，框架构建了三类基于 **Qwen‑2.5‑Omni‑7B** 的多模态模型变体，分别采用不同的训练策略与输出头，以兼顾结构化识别与开放生成任务。

#### (a) OMNISAPIENS‑7B SFT（监督微调基线）
这是框架的**核心联合训练版本**（Section 3.5）。模型接受标准化 prompt‑target 对的输入，采用**混合架构**：对于离散标签的分类任务，使用专门的分类头进行输出；对于自由文本的生成任务，则利用解码器直接生成答案。所有任务的数据被同时送入一个模型实例进行多任务监督微调（SFT），迫使骨干网络学习跨任务、跨模态的通用行为表示。

#### (b) OMNISAPIENS‑7B BAM（行为适配器增强）
为在不破坏已学习通用表示的前提下有针对性地增强对微弱行为信号的感知，框架设计了 **行为适配器模块 BAM**（Section 3.6）。BAM 冻结已训练好的 SFT 模型参数，仅在其上附加一个轻量的残差式前馈网络。该网络首先对池化后的行为描述符 $\mathbf{f}$ 进行归一化与 Dropout，再透过两层 MLP 得到适配输出 $z_{f}$，最后以可学习标量 $\alpha$ 缩放并作为残差 $\Delta h_{f} = \alpha \cdot z_{f}$ 加至主干网络倒数第二层的隐藏状态上：$h_{\mathrm{adapt}} = h_{\mathrm{penult}} + \Delta h_{f}$。这一“即插即用”机制在仅引入边际计算开销（均延迟 +0.016s，显存 +26MB）的前提下，对非言语沟通（NVC）等任务带来显著性能提升。

#### (c) OMNISAPIENS‑7B RL（强化学习推理变体）
面向需要复杂推理的社会推断等任务，框架还开发了**纯解码器版本的 OMNISAPIENS‑7B RL**（Section 3.7）。该变体去掉所有分类头，统一用解码器生成答案，并采用 **GRPO（Group Relative Policy Optimization）** 进行强化学习优化。奖励函数由答案准确度、格式合规性和语义相似度三部分加权组成，使模型在保持推理能力的同时适应行为理解任务。

### 4. 端到端输入输出流与模块关系
最终，整个框架的**端到端数据流**可以概括为：
- **输入**：原始视频/音频/文本 → 统一 prompt（显式模态引用） + 可选的行为描述符向量。
- **模型处理**：多模态骨干（Qwen‑2.5‑Omni）提取融合表示；若启用 BAM，则额外注入残差行为特征。
- **输出**：根据任务类型，分类头输出离散标签（如情绪类别），或解码器生成自由文本（如意图回答）。
- **评估**：所有输出依照预定的统一指标进行，实现跨数据集的直接比较。

这种层次化、模块化的设计使得 **HUMAN BEHAVIOR ATLAS** 不仅能直接训练出在 13 个异构数据集上超越通用多模态 LLM 的基础模型，还能通过冻结或轻量适配器的方式向全新行为数据集高效迁移（如 MUStARD 讽刺检测任务性能提升 39.1%），为解决心理与社会行为理解的规模化、通用化问题提供了一套完整的基准与建模方案。



OMNISAPIENS‑7B 以 Qwen 2.5‑Omni‑7B 多模态主干为基础，引入两种互补的范式：**SFT 混合架构**（分类头 + 解码头）与 **RL 纯解码器架构**。其关键创新在于通过**行为适配器模块（BAM）**将符号化的行为描述符无损地注入冻结的主干，并在 RL 阶段用 GRPO 优化统一格式的多任务目标。下面重点展开行为描述符的提取‑集成公式及 RL 优化目标。

### 行为描述符的提取与时序池化
原始行为描述符由 MediaPipe（姿态、微表情）和 OpenSMILE（声学特征）从视频‑音频流中逐帧提取，形成时间步长 $T$、特征维度 $D_{\text{raw}}$ 的张量：

$$
\mathbf{f}_{\mathrm{raw}} \in \mathbb{R}^{T \times D_{\mathrm{raw}}}
$$

为获得定长的全局表征，沿时间轴计算均值和标准差并拼接：

$$
\mu_{f} = \frac{1}{T} \sum_{t=1}^{T} \mathbf{f}_{\mathrm{raw}}[t], \qquad
\sigma_{f} = \sqrt{\frac{1}{T} \sum_{t=1}^{T} (\mathbf{f}_{\mathrm{raw}}[t] - \mu_{f})^{2}}, \qquad
\mathbf{f} = [\mu_{f}, \; \sigma_{f}] \in \mathbb{R}^{2D_{\text{raw}}}
$$

这一静态向量 $\mathbf{f}$ 将时序动态压缩为可被适配器处理的输入的统计摘要。

### BAM 残差集成公式
行为适配器模块（BAM）在冻结的 SFT 模型上插入轻量前向网络，通过残差方式更新倒数第二层的隐藏状态，从而在不破坏原有表征的前提下增强对微弱行为信号的感知。

首先对池化后的描述符向量 $\mathbf{f}$ 做归一化与 Dropout：

$$
x_{f} = \mathrm{Dropout}(\mathrm{Norm}(\mathbf{f}))
$$

随后送入两层 MLP（激活函数 $\phi$）产生适配信号 $z_{f}$：

$$
z_{f} = \phi(W_{2} \; \phi(W_{1} x_{f} + b_{1}) + b_{2})
$$

梯度更新的核心是残差注入，由一个可学习标量 $\alpha$ 控制适配强度：

$$
\Delta h_{f} = \alpha \cdot z_{f}, \qquad
h_{\mathrm{adapt}} = h_{\mathrm{penult}} + \Delta h_{f}
$$

这里 $h_{\mathrm{penult}}$ 是主干倒数第二层的原始隐藏状态。该设计保证了：
- **无扰集成**：主干参数冻结，仅更新适配器，避免灾难性遗忘；
- **任务自适应**：$\alpha$ 可微调，使同一主干在不同行为任务上获得差异化增益（如非言语沟通 NVC 提升 33%，讽刺检测 SAR 提升 29%）；
- **极低开销**：额外延迟仅 0.016 s，显存增加 26 MB，具备即插即用特性。

### GRPO 奖励设计与优化目标
在 OMNISAPIENS‑7B RL 阶段，模型放弃分类头，将所有任务统一于单解码器，采用群组相对策略优化 (GRPO)。其奖励函数由三部分加权构成：

$$
r_{(q,i,t)} = r_{\mathrm{acc}} + \lambda_{\mathrm{format}} \, r_{\mathrm{format}} + \lambda_{\mathrm{sim}} \, r_{\mathrm{sim}}
$$

其中 $r_{\mathrm{acc}}$ 衡量答案准确度，$r_{\mathrm{format}}$ 约束输出格式合规性，$r_{\mathrm{sim}}$ 保证语义相似度；$\lambda_{\text{format}}$ 与 $\lambda_{\text{sim}}$ 为权重超参数。

GRPO 优化目标在保持策略稳定性的同时最大化裁剪后的优势函数：

$$
J_{\mathrm{GRPO}}(\theta) = \mathbb{E}_{q \sim \mathcal{D},\, \{o\} \sim \pi_{\mathrm{old}}} \left[ \frac{1}{|G|} \sum_{i} \frac{1}{n_{o}} \sum_{k} \tilde{A}_{k} - \beta D_{\mathrm{KL}}(\pi_{\theta} \| \pi_{\mathrm{ref}}) \right]
$$

这里 $\tilde{A}_{k}$ 是组内相对优势，$D_{\mathrm{KL}}$ 为当前策略 $\pi_{\theta}$ 与参考策略 $\pi_{\mathrm{ref}}$ 的 KL 散度，$\beta$ 控制惩罚强度。这一复合奖励与 KL 约束机制使 RL 模型在保持通用文本质量的同时，在意图理解（INT）等开放式推理任务上大幅超越 SFT 基线。



## 实验与关键发现

### 主实验：多任务统一训练

我们在 HUMAN BEHAVIOR ATLAS 的全部 13 个数据集上以多任务方式联合训练 OMNISAPIENS-7B 的三个变体（SFT、RL、BAM），并用统一指标评估 10 个行为任务。与通用多模态大语言模型及大规模人类行为预训练模型相比，经过 Atlas 训练后的模型展现出更强的跨任务泛化能力。

综合结果（Table 4, Figure 2）显示：**OMNISAPIENS-7B SFT 和 BAM 在 10 个行为任务中的 8 个上超越了所有对比基线**（包括 Gemma-3-4B、Qwen-2.5-VL-7B 以及专门用于人类行为理解的 HumanOmniV2-7B），而 OMNISAPIENS-7B RL 也在 7 个任务上取得了领先。在结构化分类任务上，SFT 变体优势突出：情感识别（EMO）任务平均每类加权准确率达到 0.711，比 Qwen 2.5-Omni-7B 高出 0.05；情感极性（SEN）的二元加权 F1 达到 0.724，较未预训练基线（0.612）提升 0.112；PTSD 检测则达到满分 1.00，比 HumanOmniV2-7B 高 0.176。开放生成任务（INT、SOC）上，采用 GRPO 强化学习的 RL 变体显著更优：IntentQA 的 LLM-Judge 准确率从 0.254 提升至 0.486（+0.232），社会推理 (SOC) 也从 0.282 提升至 0.304。**这表明统一格式下的多任务联合训练使模型掌握了跨维度的行为理解能力，且 SFT 和 RL 分别在模式识别和推理任务上各具优势**。

![[assets/figures/papers/iclr26_0013_ZKE23BBvlQ_Human_Behavior_Atlas_Benchmarking_Unified_Psycho/figures/009_Figure_2.jpg]]
*Figure 2: Multitask results across tasks for each model. Each result reports the average score across all datasets for that task. Best to worst = dark green → yellow → dark red. Upon training on HUMAN BEHAVIOR ATLAS, OMNISAPIENS-7B SFT & RL outperform existing pretrained models across most behavioral tasks*

![[assets/figures/papers/iclr26_0013_ZKE23BBvlQ_Human_Behavior_Atlas_Benchmarking_Unified_Psycho/figures/008_Table_4.jpg]]
*Table 4: Results grouped by behavioral tasks (headers) and relevant datasets (sub-headers). Best results are bolded, second best are underlined. Following the unified metrics (Sec. 3.3), we use binary weighted F1 for SEN; mean per-class weighted accuracy for EMO; weighted F1 for HUM, SAR, ANX, DEP, PTSD; and LLM-Judge accuracy for SOC, INT, NVC. *MMPSY uses text-only input and excludes BAM; as the backbone is preserved, results are equivalent to OMNISAPIENS-7B SFT*

需要注意的是，OMNISAPIENS-7B RL 在 EMO、HUM 等离散分类任务上落后于 SFT，暴露出纯解码器优化在结构化输出上的固有缺陷。

### 迁移学习：预训练的迁移效率

为进一步验证 Atlas 预训练带来的跨任务迁移能力，我们在 6 个 held-out 数据集上进行极小样本微调（1 epoch，极少量数据如 DAIC-WOZ 使用 2 epochs）。Table 5 的结果显示 **OMNISAPIENS-7B SFT 在所有 held-out 任务上均显著优于相同架构但未在 Atlas 预训练的 Qwen 2.5-Omni-7B SFT**。在讽刺检测（MUStARD，SAR 任务）上，预训练模型的加权 F1 达到 0.658，相比未预训练基线的 0.473 提升了 **39.1%**；在 CMU-MOSEI（SEN 任务）上提升 0.112；在其他 held-out 数据集上也有稳定提高。这种大幅增益在零样本设置下同样存在（Table 8）。由此可以推断，**多任务联合预训练让模型学到了通用的人类行为表示，该表示能够高效迁移至新数据分布，即使在极小训练开销下也能快速适应**。定性示例（Figure 3）亦佐证了这一点：对于需要理解微妙语境与社会期待的讽刺话语，Atlas 预训练模型能够正确判别，而未预训练模型则倾向于字面误判。

![[assets/figures/papers/iclr26_0013_ZKE23BBvlQ_Human_Behavior_Atlas_Benchmarking_Unified_Psycho/figures/010_Table_5.jpg]]
*Table 5: Transfer to held-out datasets after minimal epoch fine-tuning (1 epoch). Bold denotes best score. DAIC-WOZ∗ involves 2 epochs as it has only 107 training samples. MUStARD† presents a novel behavioral task of SAR (sarcasm detection). ‡ Other held-out datasets that have tasks represented during pretraining*

### 行为描述符与 BAM 消融

我们引入行为适配器模块（BAM），通过残差方式注入 MediaPipe/OpenSMILE 提取的姿势、声学等行为描述符，以增强微弱行为信号的感知。Table 6 展示了 BAM 相对于 SFT 基线的性能变化：

![[assets/figures/papers/iclr26_0013_ZKE23BBvlQ_Human_Behavior_Atlas_Benchmarking_Unified_Psycho/figures/012_Table_6.jpg]]
*Table 6: ∆ highlights the change in performance from OMNISAPIENS-7B SFT to OMNISAPIENS-7B BAM, shown as percentage (%) and absolute (Abs). BAM provides notable performance gains for a considerable number of behavioral tasks, although its benefits are not consistent across all tasks*

- **非语言交流（NVC）性能从 0.12 提升至 0.16（+33%）；讽刺检测（SAR）提升 29%；幽默检测（HUM）提升 21%**。这些任务高度依赖微表情、声调变化等非言语线索，行为描述符为之提供了有效补充。
- 但在社会推理（SOC）和意图理解（INT）上，BAM 反而造成显著下降（-23% 至 -31%）。这表明基于表面行为特征的描述符对需要深层次认知推理的任务非但无益，还可能引入噪声。
- 进一步消融：若完全移除原始音频/视频特征，仅保留行为描述符（ABL 设置），NVC 性能从 0.16 剧降至 0.06（-50.41%），其余受影响的情绪和幽默任务亦明显衰退（Table 10）。这可证明行为描述符无法替代原始多模态信息，但其作为补充信号在特定模态缺失或信号微弱时仍具有关键作用。
- 将 BAM 适配器的隐藏维度从 256 增加到 512 后，部分任务（尤其是 SOC）加剧过拟合，性能从 0.20 跌至 0.15（-41.63%）（Table 11）。这说明轻量适配器对于保留通用行为表示、避免破坏主干模型至关重要。
- 模态组合消融（Table 12）显示：音频+视觉联合特征在 EMO 和 SEN 上产生协同增益，但在 HUM、SAR 上单模态（仅音频或仅视觉）反而更优。这再次强调了行为描述符的有效性高度依赖任务属性。
- BAM 带来的计算开销极小：平均推理延迟增加仅 0.016 s，峰值显存增加约 26 MB（Table 13），具备明显的即插即用优势。

![[assets/figures/papers/iclr26_0013_ZKE23BBvlQ_Human_Behavior_Atlas_Benchmarking_Unified_Psycho/figures/017_Table_10.jpg]]
*Table 10: ∆ highlights the change in performance from OMNISAPIENS-7B SFT to OMNISAPIENS-7B BAM and OMNISAPIENS-7B BAM (ABL), shown as percentage (%) and absolute (Abs). Behavioral adapters (BAM, ABL) provide notable performance gains for several behavioral tasks, although benefits are not consistent across all tasks*

综上，**BAM 以极低代价可针对性增强依赖低层感知信号的行为任务，但对高阶社会认知任务需谨慎使用，且其效果对适配器容量和模态组合敏感。**

### RL 训练参数消融

对于 OMNISAPIENS-7B RL，我们对比了 GRPO 和 RLOO 两种强化学习算法以及不同 rollout 数和学习率的影响。Table 20 显示，**使用 GRPO、rollout=5、学习率 5e-7 的设置在大部份任务上性能最优**。更大的 rollout 数可能导致训练不稳定，而学习率过高或过低均会损害效果。这些发现为后续统一行为模型与 RL 的结合提供了基准配置参考。

### 失败模式与局限性

1. **行为描述符的双刃性**：如前述，BAM 在 SOC、INT 上的下降表明低层行为特征可能干扰模型对语境、意图等高级语义的建模，未来需设计更智能的融合机制（例如基于注意力的时序动态加权）。
2. **RL 的分类短板**：OMNISAPIENS-7B RL 在多数离散分类任务上不如 SFT 或 BAM，反映出当前强化学习与生成式训练在结构化输出上的冲突。混合训练策略（如 RL for reasoning + SFT for recognition）是待解决的方向。
3. **数据规模与性能反常关联**：Spearman 相关性分析（Table 15）显示，数据集样本量与模型性能呈弱负相关（SFT ρ≈−0.135，RL ρ≈−0.480），暗示模型在极小数据集（如 DAIC-WOZ 107 训练样本）上可能过拟合，而大样本数据集尚不能使模型充分发挥其容量。这值得在数据配比、采样策略上进一步研究。
4. **模型规模局限**：目前仅基于 7B 参数的 Qwen 2.5-Omni，更大模型（30B+）是否会在统一行为理解上涌现出更强的抽象能力尚未知。
5. **数据模态偏态**：部分数据集（如 MMPsy）主要依赖文本，缺乏音频/视频，导致模型在某些任务上无法充分利用多模态行为信息。
6. **评估指标的简化**：例如使用二元加权 F1 可能掩盖情感强度的连续变化，LLM-Judge 虽与人类判断有高一致性（Cohen’s κ=0.78），但仍非完美替代。

### 重要图表结论

- **Figure 2 热力图**：系统呈现了 OMNISAPIENS 三变体与四个基线在 10 个任务上的平均得分梯度。Atlas 训练后的模型在整体上呈现明显的深绿色（高分），尤其在 SEN、HUM、PTSD 等任务上大规模领先，直观证实了统一多任务预训练的全局收益。
- **Table 5 迁移学习**：定量证实了 Atlas 预训练在极小样本微调下对全新数据的快速适应能力，突出跨任务行为表示的强可迁移性。
- **Table 6 与 Figure 4**：BAM 对 NVC、SAR 的显著提升与 Figure 4 的定性案例（捕捉到微笑的细微线索而纠正情感预测）相呼应，说明结构化描述符能捕捉主干模型可能忽略的瞬间行为信号。同时，Table 6 中负增长条目直接标示了当前方法的适用边界，为后续研究提供了故障分析依据。

总体而言，实验表明 HUMAN BEHAVIOR ATLAS 作为统一基准成功推动了通用心理与社会行为理解模型的构建。多任务学习和行为描述符增强分别从训练范式和特征层面带来了互补增益，但遗留的挑战也为未来工作指明了改进路径。



## 定位与知识库关联

心理与社会行为理解领域长期面临系统“孤岛化”：每个任务依赖专门设计的模型、异构的数据格式和独立的评估协议，难以训练通用的行为基础模型（核心瓶颈）。**HUMAN BEHAVIOR ATLAS** 将涵盖情感、认知、病理及社会四个维度的13个多模态数据集统一为 prompt–target 格式（Table 3），并提取行为描述符（MediaPipe、OpenSMILE）作为附加信号，从而构建了首个面向统一行为理解的大规模基准。在此基础上，**OMNISAPIENS‑7B** 模型系列——包括监督微调版（SFT）、行为适配器增强版（BAM）与强化学习版（RL）——通过多任务联合训练与灵活的迁移学习，实现了从单任务专用向通用行为感知的范式转移。相较于该领域的代表性多模态大模型（Gemma‑3‑4B、HumanOmniV2‑7B、Qwen 2.5‑Omni‑7B 等），OMNISAPIENS‑7B SFT 与 BAM 在10种行为任务中的8种上取得最优或次优成绩（Figure 2），印证了统一基准预训练带来的跨任务泛化优势。尤其在迁移学习场景下，仅经过极少微调（1～2个epoch），Atlas 预训练模型即大幅超越未预训练的相同架构基线：在 CMU‑MOSEI 情感检测上达到 0.724（基线 0.612），在 MUStARD 讽刺检测上更实现 **+39.1%** 的绝对提升（0.658 vs 0.473，Table 5）。行为适配器模块（BAM）以残差方式注入行为描述符（$\Delta h_f = \alpha z_f$），在不损害主干表示的前提下，使非言语交流（NVC）与讽刺检测（SAR）的性能分别提升 **33%** 和 **29%**（Table 6）；消融实验表明，若剥离原始音视频信号仅保留行为描述符，NVC 得分从 BAM 的 0.16 骤降至 0.06（−50.41%），可见原始多模态感知仍是基石，而 BAM 的设计则能在完整信号流上实现针对性增强。但 BAM 的增益并非恒正：在社会推理（SOC）与意图理解（INT）等依赖长篇语境推理的任务上，反而造成 23%～31% 的性能衰减，显示静态池化的行为特征可能引入噪声或干扰高层语义（Table 6）。与此同时，纯解码器结构的 OMNISAPIENS‑7B RL 凭借 GRPO 优化的推理链，在意图问答（IntentQA）等开放式生成任务上大幅领先 SFT 基线（LLM‑Judge 准确率 0.486 vs 0.254），却在情感分类（EMO）、幽默检测（HUM）等离散分类任务上落后，暴露了强化学习与监督微调在不同任务形态上的互补失败模式（Table 4）。

当前方法体系的适用边界受若干因素制约。其一，模型规模固于7B参数，更大体量（如30B+）是否能涌现更稳健的抽象行为理解仍未可知，且性能与数据集样本量之间呈现弱负相关（Spearman ≈ −0.13 ～ −0.48），提示极小数据集（如 DAIC‑WOZ 仅189条）上过拟合风险较高，大模型的表征潜力有待更充分的数据挖掘。其二，基准中部分数据集单向依赖文本或缺乏音频/视频模态（如 MMPsy），导致行为描述符的利用不充分，BAM 的优势在纯文本任务上难以发挥。其三，评估协议虽已统一，但二元加权 F1、LLM‑Judge 等简化指标可能掩盖情感强度、讽刺程度等细粒度差异；不过作为补偿，LLM‑Judge 与人类判断的 Cohen’s κ 达到0.78且对提示改写鲁棒，保障了开放生成评估的科学性，同时继续训练 Atlas 后模型的通用文本质量（流畅度、连贯性、困惑度）未出现退化，证明基准训练未牺牲底座模型的泛化能力。

综合而言，HUMAN BEHAVIOR ATLAS 与 OMNISAPIENS 模型确立了行为理解从单任务专精到统一基础模型的技术路径，但仍留有若干开放问题：  
1) 如何设计 RL 与 SFT 的混合训练策略，以兼得推理链与结构识别之长，实现全任务谱系均衡？  
2) 能否引入动态时序注意力机制替代简单的均值‑标准差池化，更精准地融合行为描述符，从而避免高级认知任务上的性能衰退？  
3) 跨文化、低资源语言场景下的迁移泛化如何保证？  
4) 模型规模扩张是否会涌现更深层的心理感知能力，使统一基准的价值进一步放大？这些问题的推进将决定通用心理与社会行为智能的下一阶段突破。



## 原文 PDF

![[paperPDFs/ICLR_2026/Human_Behavior_Atlas_Benchmarking_Unified_Psychological_And_Social_Behavior_Understanding.pdf]]
