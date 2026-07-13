---
title: "F-HOI: Toward Fine-grained Semantic-Aligned 3D Human-Object Interactions"
type: paper
paper_level: A
venue: ECCV
year: 2024
pdf_ref: paperPDFs/ECCV_2024/F_HOI_Toward_Fine_grained_Semantic_Aligned_3D_Human_Object_Interactions.pdf
project_link: https://f-hoi.github.io
code_link: https://github.com/tatsu-lab/stanford\_alpaca
aliases:
- FH
- F-HOI
tags:
- ECCV_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 引入状态级别的细粒度文本描述（包括当前状态、下一状态及运动变化描述），并通过多模态指令微调驱动模型学习2D、3D与语言空间之间的一致性表示。
primary_logic: 利用多模态大语言模型的语言理解与语义先验，结合多种模态编码器和任务特定的投影头，可以在有限的对齐数据上实现HOI状态的细粒度语义对齐，并通过联合多任务训练激发任务间的相互增益。
claims:
- 构建Semantic-HOI数据集，为每个HOI状态和状态间转换提供解耦的细粒度文本描述。
- F-HOI统一框架整合二维图像、三维物体网格、HOI-Pose和文本，并在不同任务指令下训练，学习跨模态一致表征。
- 在理解、推理、生成和重建任务上，F-HOI均显著超越经调整的多模态基线模型。
- Semantic-HOI 理解任务 上 BLEU-4 ↑ = 26.78
---

# F-HOI: Toward Fine-grained Semantic-Aligned 3D Human-Object Interactions

> [!tip] 核心洞察
> 利用多模态大语言模型的语言理解与语义先验，结合多种模态编码器和任务特定的投影头，可以在有限的对齐数据上实现HOI状态的细粒度语义对齐，并通过联合多任务训练激发任务间的相互增益。

| 字段 | 内容 |
|------|------|
| 中文题名 | F-HOI：迈向细粒度语义对齐的三维人-物交互 |
| 英文题名 | F-HOI: Toward Fine-grained Semantic-Aligned 3D Human-Object Interactions |
| 会议/期刊 | ECCV 2024 |
| Links | [Project](https://f-hoi.github.io) · [Code](https://github.com/tatsu-lab/stanford\_alpaca) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | F-HOI |
| Dataset | Semantic-HOI 理解任务 |

> [!tip] 效果简介
> - Semantic-HOI 理解任务 上，BLEU-4 ↑ 26.78 vs 20.09 (+6.69)。
> - Semantic-HOI 推理任务 上，BLEU-4 ↑ 25.56 vs 19.51 (+6.05)。
> - Semantic-HOI 生成任务 上，平均 Chamfer 距离 (↓) 22.9 vs 44.4 (-21.5)。

## 概要

**问题瓶颈**：现有三维人-物交互（3D HOI）数据集与模型仅使用粗粒度的全局动作描述（如“拿起杯子”），缺乏对中间状态及状态间转换的细粒度语义标注。这导致模型难以在细粒度语义空间中精确对齐HOI状态，无法支持“从抓握到举起再到倾斜”这类状态级别的理解与生成。

**核心洞察**：通过将多模态大语言模型（MLLM）的语言理解与语义先验引入3D HOI建模，并结合二维图像、三维物体网格、三维HOI-Pose与文本等多种模态编码器，可以在有限的对齐数据上实现HOI状态的细粒度语义对齐。联合多任务训练能够激发理解、推理、生成与重建任务之间的相互增益。

**方法定位**：F-HOI是一个统一的多模态框架，整合了CLIP图像编码器、Uni3D点云编码器、HOI-Pose投影层与Vicuna-7B大语言模型骨干，通过图像-姿态与文本-姿态对齐预训练及多任务指令微调（含偏移回归），学习2D、3D与语言空间之间的一致性表示。在方法谱系上，F-HOI将通用多模态大语言模型（如LLaVA-1.5V-7B, Liu et al., NeurIPS 2023）扩展至细粒度3D HOI领域，首次引入状态级语义对齐能力。

**主要结果**：在Semantic-HOI数据集的四项任务上，F-HOI均显著超越经微调的LLaVA-1.5V-7B + 3D HOI-Pose嵌入基线。理解任务BLEU-4从20.09提升至26.78（+6.69），推理任务BLEU-4从19.51提升至25.56（+6.05），生成任务平均Chamfer距离从44.4降至22.9（-21.5），物体条件重建任务平均Chamfer距离从45.1降至24.7（-20.4）。消融实验证实偏移回归、对齐预训练与多任务联合训练均为关键设计选择。



### 问题背景

三维人-物交互（3D Human-Object Interaction, HOI）建模是具身智能与场景理解的核心问题，要求系统同时理解人体动作、物体状态以及二者之间的语义关联。现有的HOI研究主要关注粗粒度的全局动作分类或描述，例如“拿起杯子”或“坐在椅子上”，而忽略了交互过程中多个中间状态及其转换的细粒度语义。这种粗粒度建模导致两个关键缺陷：其一，模型无法区分同一动作类别下的不同执行方式与状态演变；其二，语言、三维姿态与二维视觉之间的语义对齐停留在全局层面，难以支撑需要精确状态感知的下游任务。

### 现有方法的缺口

当前三维HOI数据集与模型存在以下瓶颈：

1. **标注粒度不足**：主流数据集（如BEHAVE、InterCap、GRAB）仅提供动作类别标签或单一全局描述，缺乏对交互过程中每个时间步的状态级语义标注。模型因此只能学习从输入到全局动作的映射，而无法捕捉状态间的因果转换关系。

2. **模态对齐粗放**：现有工作（如**MPGD**（He et al., CVPR 2023））尝试将文本描述与人体姿态关联，但其关联方式停留在动作序列级别，未解耦人体姿态、物体状态与交互状态的独立语义。这导致模型在需要区分“手已接触物体”与“手正接近物体”等细粒度状态时表现不佳。

3. **任务定义单一**：已有方法通常将HOI建模为单任务问题（如动作识别或姿态生成），缺乏一个统一框架来同时支撑理解、推理、生成与重建等多维度能力。这种碎片化的任务定义使得不同模态之间的语义对齐无法形成相互增强的闭环。

### 本文动机

针对上述缺口，本文提出核心主张：**通过构建状态级别的细粒度语义标注，并设计多模态统一框架在二维、三维与语言空间之间建立一致性表示，可以显著提升三维HOI的语义对齐精度与任务泛化能力。**

具体而言，本文的动机源于一个关键观察——多模态大语言模型（MLLM）具备强大的语言理解与跨模态语义先验，但在三维HOI领域尚未被充分利用于细粒度状态对齐。本文认为，如果将HOI交互过程拆解为离散状态序列，并为每个状态提供解耦的人体姿态描述、物体状态描述与交互状态描述，再通过多模态指令微调驱动MLLM学习这些细粒度语义与多模态输入之间的对应关系，就有可能在有限的对齐数据上实现高精度的状态级语义对齐。

这一思路面临三个核心挑战：（1）如何系统性地构建包含细粒度状态描述的数据集；（2）如何设计能够同时编码二维图像、三维物体网格、三维HOI-Pose与文本的统一架构；（3）如何定义多样化的下游任务以验证细粒度对齐的实际效果。本文后续章节将围绕这三个挑战展开。



## 核心方法与创新机理

针对现有三维人-物交互（HOI）研究仅依赖粗粒度全局动作描述、缺乏对中间状态及状态间转换的细粒度语义标注这一核心瓶颈，F-HOI 提出了一套从数据构建到模型训练的系统性创新方案。

### 1. 细粒度语义对齐数据集：Semantic-HOI

F-HOI 首先构建了 Semantic-HOI 数据集，首次为每个 HOI 状态和状态间转换提供解耦的细粒度文本描述。具体而言，每条标注包含三个组成部分：
- **解耦的人体姿态描述**：描述当前状态下人体的具体姿态。
- **物体状态描述**：描述物体在当前状态下的位姿与状态。
- **交互状态描述**：描述人与物体之间的交互关系。

标注通过向 GPT-4V 输入二维 HOI 图像自动生成，并经人工过滤，最终从三个现有数据集中收集了 20,441 对样本，按 70%/30% 划分训练集与测试集。这一细粒度标注策略使得模型能够在状态级别而非动作级别上进行语义对齐。

### 2. 多模态统一架构与输入扩展

与仅使用二维图像和文本的基线模型（LLaVA-1.5V-7B）相比，F-HOI 在输入模态上进行了关键扩展，将四种模态整合到统一架构中：

| 模态 | 编码器 | 处理方式 |
|------|--------|----------|
| 二维图像 | 冻结的 CLIP 图像编码器 | 经可训练投影层映射至 LLM 隐藏空间 |
| 三维物体网格 | 冻结的 Uni3D 点云编码器 | 经可训练投影层对齐至 LLM 空间 |
| 三维 HOI-Pose | 独立的投影层 | 人体姿态与物体位姿分别投影为 token |
| 文本描述 | SentencePiece 分词器 | 编码为 LLM 语言空间 token |

LLM 骨干采用 Vicuna-7B，并通过 LoRA 进行高效微调。任务特定的反投影头将特殊 token（`<Human>` / `<Object>`）解码为人体姿态参数和物体位姿。

### 3. 任务形式创新：状态级别的四任务体系

F-HOI 将粗粒度的通用视觉问答/描述转化为四个状态级别的 HOI 任务，各自由特定任务指令驱动：
- **理解任务**：根据输入模态描述当前 HOI 状态。
- **推理任务**：预测下一状态的细粒度描述。
- **生成任务**：从当前状态生成下一状态的 HOI-Pose。
- **物体条件重建任务**：给定物体网格，从文本描述重建 HOI-Pose。

这一任务体系迫使模型在二维、三维和语言空间之间学习一致的 HOI 表示，实现细粒度语义对齐。

### 4. 训练策略创新：对齐预训练 + 偏移回归

F-HOI 采用两阶段训练策略，与直接微调形成鲜明对比：

**第一阶段：对齐预训练。** 在 COCO 和 PoseScript 数据集上进行图像-姿态与文本-姿态对齐预训练，总损失为 $\mathcal{L} = \mathcal{L}_{\mathrm{text}} + \mathcal{L}_{\mathrm{pose}}$，其中姿态损失 $\mathcal{L}_{\mathrm{pose}} = \| \theta_{\mathrm{gt}} - \theta_{\mathrm{pred}} \|$ 为人体姿态参数的 L1 损失。该阶段为后续细粒度对齐奠定了跨模态基础。

**第二阶段：多任务指令微调。** 在 Semantic-HOI 上进行多任务联合训练，总损失为 $\mathcal{L} = \mathcal{L}_{\mathrm{text}} + \mathcal{L}_{\mathrm{hoi}}$。关键创新在于引入**偏移回归**（offset regression），即从起始状态预测人体与物体姿态的偏移量，而非绝对姿态：

$$\mathcal{L}_{\mathrm{hoi}} = \Delta \theta_{\mathrm{gt}} - \Delta \theta_{\mathrm{pred}} + \Delta O_{\mathrm{gt}} - \Delta O_{\mathrm{pred}}$$

这一设计使模型聚焦于状态间的相对变化，显著提升了生成和重建任务的精度。

### 5. 创新有效性验证

消融实验证实了上述创新的关键作用：
- **偏移回归**使生成任务的 Chamfer 距离从 27.9 降至 22.9，重建任务从 48.3 降至 24.7。
- **图像-姿态与文本-姿态对齐预训练**将理解任务的 BLEU-4 从 21.21 提升至 26.78，对所有四个任务均有显著增益。
- **多任务联合训练**使各任务之间产生相互增强效应，全部任务联合训练时所有指标均优于单独训练任一任务。

综上，F-HOI 的核心创新在于通过细粒度数据集构建、多模态输入扩展、状态级任务设计和两阶段对齐训练，首次实现了三维人-物交互在细粒度语义空间中的对齐。



F-HOI 是一个统一的多模态框架，旨在学习二维图像、三维几何与语言空间之间一致的细粒度人-物交互表示。其核心设计思路是：将异构输入模态分别编码为 token 序列，送入一个冻结后经 LoRA 微调的大语言模型骨干进行序列建模，再通过任务特定的反投影头将隐藏表示解码为文本描述或 HOI-Pose 参数。整个框架由三个组件构成：**多模态编码器**、**大语言模型骨干**、**任务特定投影头**（Fig. 4）。

![[assets/figures/papers/paper_list_l1759_F_HOI_Toward_Fine_grained_Semantic_Aligned_3D_Human_Object_Interactions/figures/006_Figure_4.jpg]]
*Figure 4: Overview of our F-HOI framework, which contains the three components: multimodal encoders, a large language model, and task-specific projectors. Based on different task instructions, F-HOI could support multi-modal inputs and complete diverse HOI tasks, covering understanding, reasoning, generation, and reconstruction tasks*

**输入流**。框架接收四类模态输入：
1. **文本**：包括任务指令、当前状态描述、下一状态描述及运动变化描述。文本通过 SentencePiece 分词器编码为语言空间的 token。
2. **二维图像**：HOI 场景的 RGB 图像，通过冻结的 CLIP 图像编码器提取特征，再经一个可训练的投影层映射到 LLM 隐藏空间。
3. **三维物体网格**：交互物体的三维网格，通过冻结的 Uni3D 点云编码器提取几何特征，同样经可训练投影层对齐到 LLM 空间。
4. **三维 HOI-Pose**：由人体姿态参数（SMPL 的 θ 和 β）和物体六自由度位姿 O 组成。人体姿态与物体位姿分别通过独立的投影层映射为 LLM 隐藏空间中的 token，并以特殊 token `<Human>` 和 `<Object>` 标记。

**骨干网络**。多模态 token 拼接后送入 LLM 骨干。F-HOI 采用 Vicuna-7B 作为 LLM 骨干，并通过 LoRA 进行高效参数微调，而 CLIP 图像编码器和 Uni3D 点云编码器在训练期间保持冻结。这种设计既保留了大语言模型的语义先验，又通过 LoRA 适配了 HOI 领域的特定知识。

**输出流**。LLM 输出的隐藏表示根据任务类型分流解码：
- **文本响应**：语言 token 通过 SentencePiece 反分词器解码为自然语言描述，用于理解和推理任务。
- **HOI-Pose 响应**：特殊 token `<Human>` 和 `<Object>` 的隐藏表示分别通过可训练的人体姿态投影层和物体位姿投影层，解码为姿态参数。在生成和重建任务中，模型预测的是从起始状态到目标状态的**偏移量**（Δθ 和 ΔO），而非绝对姿态——这一策略称为偏移回归，被消融实验证明能显著提升生成与重建精度（Table 7）。

**训练策略**。F-HOI 采用两阶段训练：
1. **对齐预训练**：在 COCO 和 PoseScript 数据集上进行图像-姿态对齐和文本-姿态对齐预训练，使用总损失 $\mathcal{L} = \mathcal{L}_{\mathrm{text}} + \mathcal{L}_{\mathrm{pose}}$，其中 $\mathcal{L}_{\mathrm{pose}} = \| \theta_{\mathrm{gt}} - \theta_{\mathrm{pred}} \|$ 为人体姿态参数的 L1 损失。消融实验表明，该预训练对所有四个下游任务均有明显增益（Table 8）。
2. **多任务指令微调**：在 Semantic-HOI 数据集上进行多任务联合训练，总损失为 $\mathcal{L} = \mathcal{L}_{\mathrm{text}} + \mathcal{L}_{\mathrm{hoi}}$，其中 $\mathcal{L}_{\mathrm{hoi}} = \Delta \theta_{\mathrm{gt}} - \Delta \theta_{\mathrm{pred}} + \Delta O_{\mathrm{gt}} - \Delta O_{\mathrm{pred}}$ 为人体姿态偏移与物体位姿偏移的 L1 损失之和。多任务联合训练使各任务之间产生相互增益，全部任务联合训练时所有指标均优于单独训练任一任务（Table 9）。

**模块关系总结**。整个框架的信息流是单向的：多模态编码器将异构输入统一为 token 序列 → LLM 骨干进行跨模态序列建模 → 任务特定投影头根据指令类型选择性解码。这种设计使得同一套模型权重可以支持理解、推理、生成和重建四类任务，仅需切换任务指令即可。



### 3.1 HOI 状态的形式化表示

F-HOI 将三维人-物交互建模为状态级别的序列。在时刻 $t$，一个 HOI 状态被形式化定义为：

$$\mathbf{s}_t = (M(\theta, \beta), O)$$

其中 $M(\theta, \beta)$ 表示由姿态参数 $\theta$ 和形状参数 $\beta$ 驱动的 SMPL 人体网格模型，$O$ 表示物体的 6 自由度位姿（3 自由度平移 + 3 自由度旋转）。这一表示将人体与物体的空间配置统一在同一状态向量中，为后续的细粒度语义对齐提供了结构化的几何载体。

### 3.2 多模态编码器模块

F-HOI 框架包含三个核心组件：多模态编码器、大语言模型骨干和任务特定的投影头。多模态编码器负责将异构输入统一映射到语言模型的隐藏空间，具体包括：

- **SentencePiece 分词器**：将文本描述（任务指令、当前状态描述、运动变化描述）编码为 LLM 语言空间的 token 序列。
- **CLIP 图像编码器（冻结）**：对二维 HOI 图像进行编码，通过一个可训练的投影层将视觉特征映射到 LLM 隐藏空间。
- **Uni3D 点云编码器（冻结）**：对三维物体网格进行编码，通过另一个可训练的投影层对齐到 LLM 空间。
- **HOI-Pose 投影层**：人体姿态参数和物体位姿分别通过独立的投影层被映射为 LLM 隐藏空间中的 token，以特殊标记 `<Human>` 和 `<Object>` 作为占位符。

这种设计使得四种模态（2D 图像、3D 物体网格、3D HOI-Pose、文本）能够在统一的语义空间中交互，为跨模态一致性学习奠定基础。

### 3.3 大语言模型骨干与高效微调

F-HOI 采用 **Vicuna-7B** 作为 LLM 骨干，接收来自各模态编码器的 token 序列并执行序列建模。为在有限计算资源下高效适配新任务，模型使用 **LoRA**（Low-Rank Adaptation）对 LLM 进行参数高效微调，而 CLIP 图像编码器和 Uni3D 点云编码器在训练过程中保持冻结。模型权重由 **LLaVA-1.5V-7B** 初始化，继承了其多模态对话能力。

### 3.4 任务特定的反投影头

LLM 输出的隐藏状态需要通过任务特定的反投影头解码为可执行的输出：

- **人体姿态反投影头**：将 `<Human>` 特殊 token 的隐藏状态解码为 SMPL 姿态参数 $\theta$。
- **物体位姿反投影头**：将 `<Object>` 特殊 token 的隐藏状态解码为物体 6 自由度位姿 $O$。
- **文本反分词器**：文本 token 通过 SentencePiece 反分词器解码为自然语言描述。

### 3.5 两阶段训练损失函数

F-HOI 采用两阶段训练策略，各阶段对应不同的损失函数组合。

**阶段一：对齐预训练**

预训练阶段的目标是建立图像-姿态和文本-姿态之间的初步对齐。总损失由文本生成损失和姿态回归损失组成：

$$\mathcal{L} = \mathcal{L}_{\text{text}} + \mathcal{L}_{\text{pose}}$$

其中 $\mathcal{L}_{\text{text}}$ 为文本交叉熵损失，用于监督语言描述的生成质量；姿态损失定义为预测人体姿态参数与真值之间的 L1 距离：

$$\mathcal{L}_{\text{pose}} = \| \theta_{\text{gt}} - \theta_{\text{pred}} \|$$

此阶段在 COCO 和 PoseScript 数据集上进行，使模型获得从图像和文本推断人体姿态的基本能力。

**阶段二：多任务指令微调**

指令微调阶段引入 HOI 特定的偏移回归机制。总损失为：

$$\mathcal{L} = \mathcal{L}_{\text{text}} + \mathcal{L}_{\text{hoi}}$$

核心创新在于 $\mathcal{L}_{\text{hoi}}$ 采用**偏移回归**策略——不直接预测目标状态的绝对姿态，而是预测从起始状态到目标状态的变化量：

$$\mathcal{L}_{\text{hoi}} = \| \Delta \theta_{\text{gt}} - \Delta \theta_{\text{pred}} \| + \| \Delta O_{\text{gt}} - \Delta O_{\text{pred}} \|$$

其中 $\Delta \theta = \theta_{t+1} - \theta_t$ 表示人体姿态参数的偏移，$\Delta O = O_{t+1} - O_t$ 表示物体位姿的偏移。这种设计将生成任务转化为学习状态间的相对变化，显著降低了预测空间的学习难度，是 F-HOI 在生成和重建任务上取得大幅提升的关键机制。消融实验证实，偏移回归使生成任务的 Chamfer 距离从 27.9 降至 22.9，重建任务从 48.3 降至 24.7。

### 补充图表

![[assets/figures/papers/paper_list_l1759_F_HOI_Toward_Fine_grained_Semantic_Aligned_3D_Human_Object_Interactions/figures/001_Figure_1.jpg]]
*Figure 1: Illustration of three state-level tasks to achieve fine-grained semantic alignment*



## 实验与关键发现

### 主实验结果

F-HOI在Semantic-HOI数据集上定义的四项状态级HOI任务中，均显著超越经微调的基线模型**LLaVA-1.5V-7B + 3D HOI-Pose embedding**（Liu et al., NeurIPS 2023）。基线模型在LLaVA-1.5V-7B的基础上添加了HOI-Pose嵌入以适应新任务，但缺乏对细粒度语义对齐的专门设计。

**理解任务**（Table 3）：给定二维图像、物体网格、HOI-Pose和任务指令，模型需生成当前HOI状态的细粒度文本描述。F-HOI取得BLEU-4为26.78，较基线20.09提升+6.69。该任务验证了模型将多模态观测映射到语义空间的能力。

**推理任务**（Table 4）：给定当前状态和运动变化描述，模型需推理下一状态的细粒度描述。F-HOI取得BLEU-4为25.56，较基线19.51提升+6.05。这表明模型能够利用语言描述中的运动语义进行状态推演。

**生成任务**（Table 5）：给定起始状态和运动变化描述，模型需生成下一状态的三维HOI-Pose。以平均Chamfer距离（↓）评估，F-HOI取得22.9，较基线44.4降低21.5，相对改善约48.4%。该任务直接检验模型在语义引导下的姿态生成精度。

**物体条件重建任务**（Table 6）：给定起始状态、物体网格和运动变化描述，模型需重建下一状态的HOI-Pose。F-HOI取得平均Chamfer距离24.7，较基线45.1降低20.4。该任务模拟了物体信息已知时的人体姿态重建场景。

四项任务的结果共同表明：通过整合多模态编码器并在任务指令驱动下进行多任务微调，F-HOI成功学习了二维、三维与语言空间之间的一致性HOI表示，实现了细粒度语义对齐。

### 消融实验分析

#### 偏移回归的作用（Table 7）

![[assets/figures/papers/paper_list_l1759_F_HOI_Toward_Fine_grained_Semantic_Aligned_3D_Human_Object_Interactions/figures/011_Table_7.jpg]]
*Table 7: Effect of offset regression on different HOI tasks. We adopt the BLUE-4 to evaluate understanding and reasoning tasks and use the averaged Chamfer distance for generation and reconstruction tasks*

将绝对姿态预测替换为从起始状态预测偏移量（偏移回归），对生成和重建任务产生了决定性影响。在生成任务中，使用偏移回归将Chamfer距离从27.9降至22.9；在重建任务中，从48.3降至24.7。偏移回归将学习目标从“预测绝对位姿”转化为“预测状态间变化量”，降低了学习难度，并使模型更关注于运动变化语义与姿态增量之间的对应关系。对理解和推理任务影响较小，因为这两项任务主要依赖文本生成能力。

#### 图像-姿态与文本-姿态对齐预训练的作用（Table 8）

![[assets/figures/papers/paper_list_l1759_F_HOI_Toward_Fine_grained_Semantic_Aligned_3D_Human_Object_Interactions/figures/013_Table_8.jpg]]
*Table 8: Effect of image-to-pose and text-to-pose alignment on different HOI tasks*

在COCO/PoseScript上的预训练为模型提供了关键的跨模态对齐先验。消融显示：仅使用文本-姿态对齐时，理解任务BLEU-4从21.21提升至24.15；同时使用图像-姿态和文本-姿态对齐时，进一步提升至26.78。推理、生成和重建任务也呈现一致的增益趋势。这一结果说明，预训练阶段建立的视觉-姿态和语言-姿态映射，为后续的细粒度语义对齐提供了有效的初始化。

#### 多任务联合训练的作用（Table 9）

![[assets/figures/papers/paper_list_l1759_F_HOI_Toward_Fine_grained_Semantic_Aligned_3D_Human_Object_Interactions/figures/014_Table_9.jpg]]
*Table 9: Effect of joint training across multiple tasks on each HOI task*

单独训练任一任务时，各项指标均显著低于全部任务联合训练。以理解任务为例：仅训练理解任务时BLEU-4为21.21，联合全部任务后提升至26.78。生成任务的Chamfer距离从单独训练的27.9降至联合训练的22.9。这表明四项任务之间存在相互增益效应——理解任务强化的语义编码能力有助于生成任务的条件建模，而生成任务对姿态空间的精细建模也反哺了理解和推理任务对空间关系的感知。

### 定性分析

**生成任务可视化**（Figure 5）：F-HOI能够根据起始状态和运动变化描述，生成语义合理的下一状态HOI-Pose。生成的人体姿态与物体位姿在空间关系上保持了交互的一致性。

**逐状态序列生成潜力**（Figure 6）：F-HOI展示了利用状态级细粒度描述进行逐状态序列生成的潜力。模型可以以前一状态的输出作为下一状态的输入，逐步生成完整的交互序列。但论文指出，长序列生成时状态间的过渡可能不够平滑，缺乏显式的时序一致性建模。

### 失败模式分析（Figure 7）

![[assets/figures/papers/paper_list_l1759_F_HOI_Toward_Fine_grained_Semantic_Aligned_3D_Human_Object_Interactions/figures/016_Figure_7.jpg]]
*Figure 7: We show three types of failure cases in our method*

论文归纳了三类典型失败案例：

1. **手部姿态预测误差**：手部关节的自由度较高且标注数据稀疏，导致模型对细粒度手部操作的预测精度有限，影响抓取等精细交互的对齐质量。

2. **物体位姿估计偏差**：在物体条件重建任务中，当物体几何形状复杂或与人体存在严重遮挡时，预测的物体位姿与真值存在明显偏差。

3. **语义理解不准确**：模型依赖大语言模型的先验知识，在使用有限对齐数据时，对罕见交互或模糊描述的语义理解可能出现偏差，导致生成或推理结果与真值不一致。

### 实验设置摘要

模型权重由LLaVA-1.5V-7B初始化，CLIP图像编码器和Uni3D点云编码器冻结，LLM骨干（Vicuna-7B）通过LoRA进行高效微调。评估指标方面，理解和推理任务采用BLEU-4和ROUGE，生成和重建任务采用平均Chamfer距离。Semantic-HOI数据集按70%/30%划分训练集和测试集，共包含20,441对HOI样本（Table 1）。

![[assets/figures/papers/paper_list_l1759_F_HOI_Toward_Fine_grained_Semantic_Aligned_3D_Human_Object_Interactions/figures/002_Table_1.jpg]]
*Table 1: Statistics of Semantic-HOI collected from three existing datasets*

### 补充图表

![[assets/figures/papers/paper_list_l1759_F_HOI_Toward_Fine_grained_Semantic_Aligned_3D_Human_Object_Interactions/figures/007_Table_3.jpg]]
*Table 3: Understanding Task*

![[assets/figures/papers/paper_list_l1759_F_HOI_Toward_Fine_grained_Semantic_Aligned_3D_Human_Object_Interactions/figures/008_Table_4.jpg]]
*Table 4: Reasoning Task*

![[assets/figures/papers/paper_list_l1759_F_HOI_Toward_Fine_grained_Semantic_Aligned_3D_Human_Object_Interactions/figures/009_Table_5.jpg]]
*Table 5: Generation Task*

![[assets/figures/papers/paper_list_l1759_F_HOI_Toward_Fine_grained_Semantic_Aligned_3D_Human_Object_Interactions/figures/010_Table_6.jpg]]
*Table 6: Object-conditioned Reconstruction Task*

![[assets/figures/papers/paper_list_l1759_F_HOI_Toward_Fine_grained_Semantic_Aligned_3D_Human_Object_Interactions/figures/012_Figure_5.jpg]]
*Figure 5: Qualitative results of F-HOI on generation task*



## 定位与知识库关联

### 1. 方法沿革与基线对比

F-HOI 的提出源于对现有三维人-物交互（3D HOI）建模中**语义粒度不足**这一瓶颈的突破。此前的工作主要停留在粗粒度的全局动作描述层面，缺乏对交互中间状态及其转换的细粒度语义标注，导致模型难以在语义空间中对齐具体的 HOI 状态。F-HOI 通过构建 **Semantic-HOI** 数据集并设计统一的多模态框架，首次将细粒度语义对齐引入 3D HOI 任务。

在基线选择上，论文将 F-HOI 与经过适配的 **LLaVA-1.5V-7B**（Liu et al., NeurIPS 2023）进行对比。该基线在 LLaVA 的基础上额外加入了 3D HOI-Pose 嵌入，并在 Semantic-HOI 数据集上进行微调，以使其具备处理新模态和任务的能力。F-HOI 相对于该基线的关键改进体现在四个维度：

| 对比维度 | LLaVA-1.5V-7B + 3D HOI-Pose | F-HOI（本文方法） |
|---------|---------------------------|-----------------|
| **输入模态** | 二维图像 + 文本 | 二维图像 + 三维物体网格 + 三维 HOI-Pose（人体与物体位姿）+ 文本 |
| **任务形式** | 通用视觉问答/描述 | 四个状态级 HOI 任务（理解、推理、生成、重建），各自由特定任务指令驱动 |
| **训练策略** | 在目标数据集上直接微调 | 先在 COCO/PoseScript 上进行图像-姿态与文本-姿态对齐预训练，再进行多任务指令微调（含偏移回归） |
| **姿态预测方式** | 绝对姿态预测 | 从起始状态预测人体与物体姿态的偏移（偏移回归） |

这种设计差异带来了显著的性能提升：在理解任务上，F-HOI 的 BLEU-4 达到 26.78（基线 20.09，提升 33.3%）；在生成任务上，平均 Chamfer 距离降至 22.9（基线 44.4，降低 48.4%）。消融实验进一步表明，**偏移回归**使生成 Chamfer 距离从 27.9 降至 22.9，重建从 48.3 降至 24.7；**图像-姿态与文本-姿态对齐预训练**使理解 BLEU-4 从 21.21 提升至 26.78；**多任务联合训练**则使所有任务指标均优于单独训练任一任务，验证了任务间的相互增益效应。

从更广的谱系来看，F-HOI 处于**多模态大语言模型（MLLM）**与**三维视觉理解**的交叉地带。其架构继承了 LLaVA 系列的视觉-语言对齐范式，同时引入了 Uni3D 点云编码器（Zhou et al., 2023）以处理三维物体几何信息，并通过任务特定的投影头将 LLM 的隐藏表示解码为结构化的 HOI-Pose 参数。这种设计使 F-HOI 能够同时处理文本生成和姿态回归两类异质输出。

### 2. 适用边界

F-HOI 的适用性受以下条件约束：

- **模态依赖**：推理时需要同时提供二维图像、三维物体网格、HOI-Pose 和文本描述作为输入。这一严格的模态要求限制了其在仅具备部分模态信息的实际场景（如单目视频理解）中的部署便捷性。
- **闭集假设**：模型在 Semantic-HOI 数据集上训练和评估，该数据集源自三个现有 3D HOI 数据集（BEHAVE、InterCap、GRAB），覆盖的物体类别和交互类型有限。在开放场景下对未见物体和交互的泛化能力尚未验证。
- **状态级建模的时序局限**：F-HOI 聚焦于成对 HOI 状态（当前状态与下一状态）的细粒度对齐，但在长序列逐状态生成时，状态间的过渡可能不够平滑，缺乏显式的时序一致性建模。
- **数据规模与质量**：Semantic-HOI 包含 20,441 对样本（70% 训练 / 30% 测试），其细粒度描述由 GPT-4V 生成并经人工过滤。尽管采取了质量控制措施，仍可能引入语言模型偏见和不准确的描述，影响模型在边界案例上的表现。

### 3. 局限与开放问题

论文明确指出的局限包括：手部姿态参数预测仍存在误差，限制了细粒度操作对齐的精度；模型依赖大语言模型的先验知识，在仅使用少量对齐数据时，理解和推理的准确率可能不稳定。

由此衍生的开放问题包括：

1. **输入模态的松弛**：如何放宽或消除对物体网格、HOI-Pose 等结构化输入的依赖，使模型能够从更易获取的模态（如单张 RGB 图像或视频）中实现细粒度 HOI 理解？
2. **开放场景泛化**：如何将细粒度语义对齐能力泛化到训练分布之外的物体类别和交互类型？这可能需要引入更强的基础模型先验或设计域适应策略。
3. **时序一致性建模**：能否结合物理先验或显式时序模型（如状态空间模型或扩散策略），提升长序列状态生成的一致性与物理合理性？
4. **评估指标的语义贴合度**：当前使用的 BLEU-4、ROUGE（文本任务）和 Chamfer 距离（姿态任务）主要衡量表面匹配度，能否设计更贴合细粒度语义理解质量的评估指标，例如考虑动作语义保留度的姿态相似度度量？
5. **规模化对齐**：如何利用更大规模的自监督或弱监督数据（如互联网视频中的隐式交互信号）进一步强化跨模态对齐能力，减少对昂贵人工标注的依赖？

### 4. 知识库定位

F-HOI 的核心贡献在于**首次将状态级细粒度语义对齐引入 3D HOI 建模**，其知识贡献可定位于以下坐标：

- **任务定义**：提出了理解、推理、生成、重建四类状态级 HOI 任务，为细粒度 3D HOI 评估建立了基准。
- **数据构建**：Semantic-HOI 数据集提供了解耦的人体姿态、物体状态和交互状态描述，填补了现有数据集的语义粒度空白。
- **方法设计**：验证了“多模态编码器 + LLM 骨干 + 任务特定投影头”的统一架构在处理异质 HOI 任务上的有效性，以及偏移回归、跨模态对齐预训练、多任务联合训练三项关键设计的作用。
- **局限性认知**：明确了当前方法在模态依赖、泛化能力、时序建模和评估指标等方面的不足，为后续工作指明了改进方向。

对于后续研究，F-HOI 可作为细粒度 3D HOI 任务的强基线，其消融发现（偏移回归的增益、对齐预训练的必要性、多任务联合训练的相互增强效应）为相关方法设计提供了可复用的经验。同时，其开放问题列表为社区提供了明确的研究议程。



## 原文 PDF

![[paperPDFs/ECCV_2024/F_HOI_Toward_Fine_grained_Semantic_Aligned_3D_Human_Object_Interactions.pdf]]
