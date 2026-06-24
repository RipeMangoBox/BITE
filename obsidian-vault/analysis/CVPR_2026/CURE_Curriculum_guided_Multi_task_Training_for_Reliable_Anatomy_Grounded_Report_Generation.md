---
title: "CURE: Curriculum-guided Multi-task Training for Reliable Anatomy Grounded Report Generation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/CURE_Curriculum_guided_Multi_task_Training_for_Reliable_Anatomy_Grounded_Report_Generation.pdf
project_link: null
code_link: "https://github.com/PabloMessina/CURE"
huggingface_link: "https://huggingface.co/pamessina/medgemma-4bit-cure"
aliases:
- CURE
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 引入错误感知的课程学习，在数据集间和类别内动态调整采样权重；用解剖学基础报告生成（AGRG）替代传统发现生成目标，促使模型同时学习定位与正常/异常描述。
primary_logic: 无需额外数据，通过课程引导的多任务训练，使医学 VLM 学会定位并描述解剖区域，同时平衡正常与异常样本，大幅提升定位准确性和报告可信度。
claims:
- CURE 在 Chest ImaGenome 上将定位 IoU 提升 0.35，是 MAIRA-2 的两倍。
- CURE 将平均异常发现幻觉率从 26.50% 降至 8.78%，矛盾率减半，蕴含率翻倍。
- 在锁骨区域，CURE 的异常幻觉率仅为 1%，而 MAIRA-2 高达 59% 以上。
- CURE 在未见过的 VinDr-CXR 上零样本短语定位微平均 IoU 达到 0.243，远超 MAIRA-2 的 0.161。
---

# CURE: Curriculum-guided Multi-task Training for Reliable Anatomy Grounded Report Generation

> [!tip] 核心洞察
> 无需额外数据，通过课程引导的多任务训练，使医学 VLM 学会定位并描述解剖区域，同时平衡正常与异常样本，大幅提升定位准确性和报告可信度。

| 字段 | 内容 |
|------|------|
| 中文题名 | CURE：课程引导的多任务训练用于可靠的解剖学基础报告生成 |
| 英文题名 | CURE: Curriculum-guided Multi-task Training for Reliable Anatomy Grounded Report Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2601.15408) · [Code](https://github.com/PabloMessina/CURE) · [HuggingFace](https://huggingface.co/pamessina/medgemma-4bit-cure) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | CURE |
| Dataset | MS-CXR, Chest ImaGenome, PadChest-GR, VinDr-CXR |

> [!tip] 效果简介
> - MS-CXR 上，Phrase Grounding Micro IoU 0.552 vs 0.495 (MAIRA-2) (+0.057)。
> - Chest ImaGenome (AGRG) 上，IoU 0.601 vs 0.249 (MAIRA-2) (+0.352)；CXRFEScore 0.549 vs 0.357 (MAIRA-2) (+0.192)。
> - PadChest-GR (GRG) 上，IoU 0.265 vs 0.256 (MAIRA-2) (+0.009)。

## 概述

医学视觉语言模型（VLM）在胸部X光片报告生成中面临一个关键瓶颈：标准多任务训练的数据分布严重不均，且传统发现生成目标侧重异常描述，导致视觉定位能力薄弱，模型产生大量与图像证据不一致的虚假异常（幻觉）。**CURE** 针对这一问题，提出了一种**错误感知的课程引导多任务训练框架**，在不引入任何额外数据的前提下，通过三个核心机制实现突破：

1. **用解剖学基础报告生成（AGRG）替代传统发现生成目标**，要求模型同时学习定位解剖区域并描述其正常/异常状态。
2. **引入错误感知的课程学习**，在数据集间和类别内动态调整采样权重，主动平衡正常与异常样本。
3. **在 Chest ImaGenome 上进行定位-描述预训练**，使基础模型获得初始视觉定位能力。

**核心结论**：CURE 将定位 IoU 大幅提升 0.35（是基线模型 MAIRA-2 的两倍），平均异常发现幻觉率从 26.50% 降至 8.78%，矛盾率减半，蕴含率翻倍。在锁骨等易产生幻觉的区域，CURE 的异常幻觉率仅为 1%，而 MAIRA-2 高达 59% 以上。在零样本短语定位任务上，CURE 同样显著超越基线。

**方法定位**：CURE 属于**课程学习引导的多任务指令微调范式**，将异构监督信号统一为图像-指令-响应对，在预训练医学 VLM（MedGemma-4B-IT）基础上进行微调。与现有方法相比，其核心差异在于用 AGRG 目标替代传统发现生成，并引入错误感知的动态采样策略。

**主要结果概览**（详见实验与分析部分）：

| 基准测试 | 指标 | CURE | MAIRA-2 | 提升 |
|---------|------|------|---------|------|
| Chest ImaGenome (AGRG) | IoU | 0.601 | 0.249 | +0.352 |
| Chest ImaGenome (AGRG) | CXRFEScore | 0.549 | 0.357 | +0.192 |
| MS-CXR (PG) | Micro IoU | 0.552 | 0.495 | +0.057 |
| VinDr-CXR (Zero-Shot PG) | Micro IoU | 0.243 | 0.161 | +0.082 |
| 异常幻觉率（平均） | % | 8.78 | 26.50 | −17.72 |

**方法谱系与知识库定位**：CURE 建立在 **MAIRA-2**（开放式医学 VLM，联合学习定位与报告生成）和 **MedGemma-4B-IT**（预训练基础医学 VLM，缺乏视觉定位能力）之上。其课程学习策略借鉴了动态采样重加权的思想，但创新性地将其应用于医学多任务场景的数据集间和类别内两个粒度，并通过验证集错误率驱动采样概率更新。在评估层面，CURE 综合使用 IoU、CXRFEScore、CheXbert F1 等指标，并引入基于自然语言推理的幻觉分析框架，为医学报告生成的可信度评估提供了新视角。

## 背景与动机

医学视觉-语言模型（VLM）在胸部 X 光片自动报告生成领域取得了显著进展，但当前最先进的方法面临一个核心瓶颈：**视觉定位能力薄弱，报告产生大量与图像证据不一致的虚假异常（幻觉）**。以 MAIRA-2 为代表的开放式医学 VLM 虽能联合学习定位与报告生成，但其标准多任务训练中数据分布严重不均，且传统发现生成目标侧重异常描述，导致模型在未见过的解剖区域上频繁产生虚假阳性检测——例如，在锁骨区域，MAIRA-2 的异常幻觉率高达 59% 以上，而实际图像中并无异常。

这一问题的深层原因在于训练范式的双重缺陷。一方面，多任务训练中各数据源按数据集大小比例均匀采样，使小规模但关键的定位数据集在训练中被边缘化；另一方面，传统的发现生成目标鼓励模型输出异常发现，却未强制其与视觉证据对齐，导致“描述”与“定位”之间的因果链路断裂。

CURE 的核心动机正是针对上述缺口：**无需额外数据，通过课程引导的多任务训练，使医学 VLM 学会定位并描述解剖区域，同时平衡正常与异常样本**。该方法引入错误感知的课程学习策略，在数据集间和类别内动态调整采样权重，并用解剖学基础报告生成（AGRG）替代传统发现生成目标，促使模型同时学习定位与正常/异常描述。这一设计从根本上重塑了模型的优化方向——从“倾向于生成异常描述”转向“生成与图像证据一致的解剖学基础描述”，从而大幅提升定位准确性和报告可信度。

## 核心创新

CURE 的核心创新在于**通过课程引导的多任务训练，在不引入任何额外数据的前提下，系统性解决医学 VLM 在视觉定位和报告生成中的两个相互纠缠的瓶颈：数据分布严重不均，以及传统发现生成目标导致的定位能力薄弱与虚假异常幻觉**。

### 1. 从发现生成到解剖学基础报告生成（AGRG）

当前最先进的方法（如 **MAIRA-2**）采用短语定位（Phrase Grounding, PG）和标准报告生成（Report Generation, RG）的联合训练范式，其报告生成目标侧重于描述异常发现。这一设计存在根本性缺陷：模型被鼓励生成异常描述，却未学习如何将描述与图像中的具体解剖区域对齐，导致大量“无中生有”的幻觉——报告声称某解剖结构存在异常，但图像中并无对应证据。

CURE 将核心监督任务替换为**解剖学基础报告生成（Anatomy-Grounded Report Generation, AGRG）**，并将其拆解为三个互补子任务：

- **Locate**：给定解剖结构名称，输出其边界框坐标；
- **Describe**：给定解剖结构名称和边界框，生成该区域的正常/异常描述；
- **Locate and Describe**：仅给定解剖结构名称，同时输出边界框和描述。

这一任务重构的因果逻辑在于：模型必须**先学会“在哪里”，再学会“是什么”**，从而将视觉定位能力内化为报告生成的先决条件，而非可选的辅助目标。

### 2. 错误感知的课程学习策略

标准多任务训练按数据集大小比例均匀采样，导致大数据集（如 MIMIC-CXR 的 RG 任务）主导训练，而小数据集（如 PadChest-GR 的 GRG 任务）和长尾解剖类别被严重欠采样。CURE 引入**错误感知的课程学习**，在两级粒度上动态调整采样权重：

- **数据集级（Dataset-level）**：在每个课程阶段结束时，对验证集评估各数据源的综合性能评分 $s_i = \alpha \cdot \text{IoU}_i + (1 - \alpha) \cdot \text{CXRFEScore}_i$，计算归一化错误率 $p_i = \frac{e_i}{\sum_{j=1}^{K} e_j}$，错误率越高的数据源在下一阶段获得越高的采样概率；
- **类别级（Class-level）**：在解剖结构类别维度上进行类似的错误感知重加权，确保困难解剖区域获得更多训练曝光。

这一策略使模型能够**自适应地聚焦于当前最薄弱的数据源和类别**，而非依赖固定的启发式采样。消融实验证实：课程学习（v13）相比统一采样（v12）在 GRG 任务上取得更高 IoU（PadChest 0.272 vs 0.263），而纯自然采样（v15）直接导致 GRG 任务完全崩溃（IoU 0.000），凸显了主动平衡数据分布的必要性。

### 3. 专用预训练与高学习率的关键作用

CURE 的第三个关键设计是在 Chest ImaGenome 上对基础模型 **MedGemma-4B-IT** 进行 3000 步的**定位-描述预训练**，使原本缺乏视觉定位能力的预训练模型获得初始的空间感知能力。消融实验表明：引入预训练使 AGRG IoU 从 0.378 提升至 0.430（低学习率），而将学习率从 $2\times10^{-5}$ 提高到 $2\times10^{-4}$ 后，AGRG IoU 进一步跃升至 0.601，PG MS-CXR IoU 从 0.495 升至 0.552。高学习率在此场景下的显著增益，可能源于预训练阶段需要更激进的参数更新来克服基础模型对定位任务的初始不适应。

### 4. 创新点的协同效应

上述三个创新并非孤立生效，而是形成正向反馈循环：AGRG 任务设计为课程学习提供了可优化的定位-描述联合目标；课程学习确保预训练和多任务微调阶段的数据分布持续适应模型弱点；专用预训练则为课程学习提供了更优的初始化起点。这一协同机制使得 CURE 在 Chest ImaGenome 上将定位 IoU 提升 **+0.352**（是 MAIRA-2 的两倍），平均异常发现幻觉率从 26.50% 降至 **8.78%**，矛盾率减半（17.44% vs 33.22%），蕴含率翻倍（39.50% vs 15.94%）。

## 整体框架

CURE 是一个**课程引导的多任务训练框架**，无需额外数据即可同时提升医学视觉语言模型的视觉定位准确性和报告生成可信度。其核心瓶颈在于：标准多任务训练中数据分布严重不均，且传统“发现生成”目标侧重异常描述，导致视觉定位能力薄弱，报告产生大量与图像证据不一致的虚假异常（幻觉）。CURE 通过三个关键机制解决这一问题：(1) 将异构监督信号统一为细粒度指令格式；(2) 引入错误感知的课程学习，在数据集间和类别内动态调整采样权重；(3) 用**解剖学基础报告生成（AGRG）**替代传统发现生成目标，促使模型同时学习定位与正常/异常描述。

### 整体流程

框架（图2）按迭代阶段运行，每个阶段包含三步闭环：

1. **训练**：从统一指令池中按当前采样权重抽取训练实例，对基础模型进行多任务微调。
2. **评估**：每隔 $N$ 步在验证子集上计算各任务、各类别的性能指标（IoU 和 CXRFEScore）。
3. **重加权**：根据评估误差动态更新数据集级和类别级的采样概率，使模型在下一阶段更关注当前表现较差的数据源和类别。

### 核心模块

**统一指令格式化**：CURE 将短语定位（PG）、接地报告生成（GRG）和 AGRG 三类任务统一为图像-指令-响应三元组。AGRG 进一步细分为三个子任务——Locate（仅定位解剖区域）、Describe（仅描述该区域正常/异常状态）、Locate and Describe（同时定位并描述）——使模型在统一框架下获得细粒度定位与描述能力。

**错误感知课程学习**：采样概率由加权性能评分驱动。对每个数据源 $i$，计算聚合性能得分 $s_i = \alpha \cdot \mathbf{IoU}_i + (1 - \alpha) \cdot \mathbf{CXRFEScore}_i$，其中 $\alpha$ 控制定位精度与语义质量的权衡。误差率 $e_i = 1 - s_i$ 经归一化 $p_i = \frac{e_i}{\sum_{j=1}^{K} e_j}$ 后作为下一阶段的采样概率——误差越大的数据源被采样越多。此机制在数据集间（如 Chest ImaGenome vs. PadChest-GR）和解剖类别内（如左锁骨 vs. 右肺）两级粒度上同时运作。

**Chest ImaGenome 预训练**：基础模型 MedGemma-4B-IT 本身缺乏视觉定位能力。CURE 在多任务微调前，先在 Chest ImaGenome 上进行 3000 步的定位-描述预训练，使模型获得初始定位能力。消融实验表明，引入该预训练阶段使 AGRG IoU 从 0.378 提升至 0.430（低学习率），配合高学习率（$2 \times 10^{-4}$）可达 0.596。

**边界框感知的数据增强**：训练中应用空间变换和 CLAHE 增强时，同步修改边界框坐标以保持监督信号一致性，确保定位任务不受图像增强干扰。

### 输入输出流

- **输入**：胸部 X 光图像 + 任务指令（如“Ground the phrase: left clavicle”或“Locate and Describe: left clavicle”）。
- **输出**：根据任务类型，模型输出边界框坐标（定位）、文本描述（报告），或二者的组合（接地报告）。输出格式统一为指令遵循的文本响应，边界框以坐标序列形式嵌入其中。

### 关键设计决策

课程学习的权重参数 $\alpha=0.8$ 被证明最优——优先强化空间定位能力，在预训练 3000 步后 AGRG IoU 达到峰值 0.616。纯自然采样策略（按数据集原始大小比例采样）导致小数据集任务（如 GRG）完全崩溃（IoU 0.000），验证了主动平衡数据分布的必要性。

### 补充图表

![[assets/figures/papers/paper_list_l2070_https_arxiv_org_abs_2601_15408/figures/003_Figure_2.jpg]]
*Figure 2: Overview of CURE, our Curriculum-guided Multi-task Training Framework. During training, the model is periodically evaluated every N steps on validation subsets from each task. Performance metrics (IoU, CXRFEScore) are calculated to identify task-level and category-level errors, which are then used to update the sampling weights in the training sampler. The cycle then resumes, allowing the model to focus more heavily on the data it finds most challenging. Evaluation of the RG task uses the official MIMIC-CXR test set, while VinDr-CXR is assessed in a zero-shot setting*

## 核心模块与公式推导

CURE 围绕三个核心模块构建：**细粒度任务统一表示**、**错误感知课程学习**、以及**边界框感知的数据增强与预训练**。这些模块协同解决了标准多任务训练中数据分布严重不均和视觉定位能力薄弱的核心瓶颈。

### 细粒度任务统一表示

CURE 将异构监督信号统一为图像-指令-响应对 `(image, instruction, response)`。针对不同任务，采用不同的指令模板：

- **短语定位 (PG)**：指令为 `"Ground the phrase: {phrase}"`，响应为边界框坐标。
- **接地报告生成 (GRG)**：指令为 `"Generate a grounded report"`，响应为带定位锚点的报告文本。
- **解剖学基础报告生成 (AGRG)**：进一步细分为三个子任务：
  - **Locate**：`"Locate the anatomical region: {anatomical_name}"`
  - **Describe**：`"Describe the anatomical region: {anatomical_name}"`
  - **Locate and Describe**：`"Locate and describe the anatomical region: {anatomical_name}"`

AGRG 替代了传统发现生成目标，迫使模型同时学习定位与正常/异常描述，这是 CURE 降低幻觉率的关键机制。

### 错误感知课程学习

课程学习在 $n$ 个迭代阶段中进行，每阶段包含训练、评估和采样重加权三个步骤。每 $N$ 步在验证集上评估各数据源的性能，计算聚合性能评分：

$$s_i = \alpha \cdot \mathbf{IoU}_i + (1 - \alpha) \cdot \mathbf{CXRFEScore}_i$$

其中 $\alpha$ 控制定位精度（IoU）与语义质量（CXRFEScore）的权衡。消融实验表明，$\alpha=0.8$ 时预训练 3000 步后 AGRG IoU 达到峰值 0.616（Table 12）。

错误率 $e_i = 1 - s_i$ 经归一化后得到下一阶段的采样概率：

$$p_i = \frac{e_i}{\sum_{j=1}^{K} e_j}$$

该策略在**数据集间**和**类别内**两个粒度上动态调整采样权重，使模型在困难数据源（如小样本的 GRG 任务）上获得更多训练机会。消融实验（Table 7）证实：课程学习（v13）比统一采样（v12）在 PadChest-GR 上取得更高 IoU（0.272 vs 0.263），而纯自然采样（v15）导致 GRG 完全崩溃（IoU 0.000）。

### 边界框感知数据增强与预训练

训练管线是边界框感知的：对图像应用空间变换和 CLAHE 增强时，同步更新边界框坐标以保持监督信号一致性。

此外，CURE 在 Chest ImaGenome 上进行 3000 步的定位-描述预训练，使基础模型 **MedGemma-4B-IT** 获得初始视觉定位能力。消融实验（Table 13）显示，引入预训练（v6→v8）使 IoU 从 0.378 提升至 0.430（低学习率），配合高学习率（$2 \times 10^{-4}$）可达 0.596。将学习率从 $2 \times 10^{-5}$ 提高到 $2 \times 10^{-4}$ 是性能跃升的关键——AGRG IoU 从 0.486 跃升至 0.601，PG MS-CXR IoU 从 0.495 升至 0.552。

![[assets/figures/papers/paper_list_l2070_https_arxiv_org_abs_2601_15408/figures/018_Table_13.jpg]]
*Table 13: Detailed Results for Anatomy-Grounded Report Generation (AGRG). Performance of baseline models, pre-training-only checkpoints, and the full set of multi-task fine-tuning ablation variants (v1–v15) on the Chest ImaGenome test subset. We report mean Intersection-over-Union (IoU$, \delimiter$ "3222378 ), CheXbert F1 (Micro/Macro averages$, \delimiter$ "3222378 ), CheXbert cosine similarity (Cos.$, \delimiter$ "3222378 ), and CXRFEScore (CXS$, \delimiter$ "3222378 ). Bold indicates the best result per column; underlined indicates the second best*

### 补充图表

![[assets/figures/papers/paper_list_l2070_https_arxiv_org_abs_2601_15408/figures/001_Figure_1.jpg]]
*Figure 1: False Positive Detection of Pathologies. Given the same chest X-ray input from the MIMIC-CXR test set, both models approximate the location of the left clavicle. However, the baseline model (MAIRA-2) hallucinates a fracture (there is no fracture in the image), whereas our proposed model (CURE) generates a clinically correct and visually grounded description*

## 实验与分析

### 核心瓶颈与因果机制

标准多任务训练面临两个深层矛盾：其一，不同任务的数据集规模差异悬殊（如 MIMIC-CXR 报告生成任务拥有数十万实例，而 PadChest-GR 接地报告生成仅数千例），均匀采样导致小数据集任务被淹没；其二，传统发现生成目标天然偏向异常描述，使模型在正常解剖区域频繁产生虚假异常（幻觉）。CURE 通过**错误感知的课程学习**在数据集间和类别内动态调整采样权重，同时以**解剖学基础报告生成（AGRG）** 替代传统发现生成目标，迫使模型同时学习定位与正常/异常描述，从而在不引入额外数据的前提下大幅提升定位准确性和报告可信度。

### 主实验结果

#### 视觉定位：短语接地与零样本泛化

CURE 在三个短语接地（PG）测试集上全面超越当前最先进的开放式医学 VLM **MAIRA-2**（表 2）。在域内 MS-CXR 上，CURE 的 Micro IoU 达到 0.552（MAIRA-2 为 0.495），Macro IoU 为 0.495（MAIRA-2 为 0.453）。在 PadChest-GR 上，CURE 的 Micro/Macro IoU 分别为 0.453/0.438，而 MAIRA-2 仅为 0.280/0.288，提升幅度超过 50%。更关键的是，在**完全未见过的 VinDr-CXR 数据集**上，CURE 的零样本 Micro IoU 达到 0.243，远超 MAIRA-2 的 0.161，证明其定位能力具有跨数据集泛化性。

#### 解剖学基础报告生成：定位与语义双重提升

在 Chest ImaGenome 的 AGRG 任务上（表 3），CURE 取得了**质的飞跃**：IoU 从 MAIRA-2 的 0.249 跃升至 0.601（+0.352），定位精度翻倍有余。语义质量同样大幅提升，CXRFEScore 从 0.357 提升至 0.549（+0.192）。值得注意的是，CheXbert F1 指标提升相对温和（Micro F1 从 0.504 到 0.551），这反映了当前课程学习策略的一个固有限制：采样权重主要基于定位误差，未直接优化临床发现的分布不平衡。

#### 接地报告生成：小数据集上的稳健性

在 PadChest-GR 的接地报告生成（GRG）任务上（表 4），CURE 的 IoU 为 0.265，略高于 MAIRA-2 的 0.256（+0.009），CXRFEScore 从 0.331 提升至 0.377。虽然绝对提升幅度不如 AGRG 显著，但在仅数千训练实例的极端数据稀缺条件下，这一结果验证了课程学习策略对小数据集任务的保护作用。

#### 标准报告生成：语义质量保持

在 MIMIC-CXR 标准报告生成任务上（表 5），CURE 在 CheXbert F1、RadGraph F1、RaTEScore 等语义指标上与专门微调的报告生成模型 **MedGemma-FT (RG)** 持平或略优，证明引入定位能力并未牺牲报告文本质量。

### 幻觉分析：从 26.50% 到 8.78% 的质变

幻觉分析（表 6）揭示了 CURE 最关键的临床价值。在 Chest ImaGenome 子集的六个关键解剖区域上，CURE 将平均异常发现幻觉率从 MAIRA-2 的 **26.50% 降至 8.78%**，降幅达 18.6 个百分点。基于自然语言推理（NLI）的一致性评估进一步证实：CURE 的矛盾率（Contradiction）从 MAIRA-2 的 33.22% 降至 17.44%，几乎减半；蕴含率（Entailment）从 15.94% 提升至 39.50%，翻了一倍有余。在锁骨区域，MAIRA-2 的异常幻觉率高达 59% 以上，而 CURE 仅为 1%，这一对比直观展示了 AGRG 目标在抑制虚假异常方面的根本性优势。

### 消融研究：各组件的贡献解耦

消融实验（表 7）系统拆解了 CURE 各组件的作用：

**预训练的关键性**：引入 Chest ImaGenome 预训练是定位能力从无到有的转折点。无预训练时（v6），AGRG IoU 仅为 0.378；预训练 3000 步后（v8）提升至 0.430（低学习率设置下）。当学习率从 $2 \times 10^{-5}$ 提高到 $2 \times 10^{-4}$（v9），AGRG IoU 跃升至 0.596，PG MS-CXR IoU 从 0.495 升至 0.552，说明基础模型需要足够大的学习率才能有效吸收预训练阶段注入的定位知识。

**课程学习的双重作用**：课程学习变体（v13）在 GRG 任务上取得最高 IoU（PadChest 0.272 vs 统一采样 v12 的 0.263），同时在 AGRG 上保持竞争力。但**纯自然采样策略（v15）导致 GRG 完全崩溃（IoU 0.000）**，这一失败模式深刻揭示了多任务学习中主动平衡数据分布的必要性——当采样完全由数据集原始大小决定时，小数据集任务会被完全忽略。

**损失权重 α 的调节效应**：α=0.8 的设置优先强化空间定位，在预训练 3000 步后 AGRG IoU 达到峰值 0.616，验证了在早期阶段侧重定位能力对最终性能的决定性影响。

### 数据组成与训练动态

训练数据（表 1）涵盖四个任务：MIMIC-CXR 报告生成（RG）拥有 270,790 训练实例，Chest ImaGenome 的 AGRG 任务有 158,226 实例，MS-CXR 和 PadChest-GR 的 PG/GRG 任务分别仅有 1,049 和 4,180 实例。这种极端的规模差异正是课程学习发挥作用的场景。训练动态可视化（图 4）展示了数据集间采样权重随训练进程的自适应变化：初期各数据集权重接近均匀，随着模型在某些任务上快速收敛，其采样概率逐渐降低，错误率高的任务获得更多采样机会，形成负反馈闭环。

### 失败模式与局限性

尽管 CURE 在定位和幻觉抑制上取得了显著突破，仍存在明确的改进空间：

1. **语义指标的瓶颈**：课程学习的采样权重基于 IoU 和 CXRFEScore 的组合评分，未直接建模临床发现的分布，导致 CheXbert F1 等纯文本指标提升有限。这提示需要设计多维重新加权策略，在平衡解剖区域的同时兼顾罕见或长尾临床发现。

2. **数据利用率的约束**：受计算资源限制，训练中仅利用了 Chest ImaGenome 约 1.74% 的实例，可能低估了该方法的性能上限。

3. **小数据集任务的脆弱性**：纯自然采样（v15）的失败表明，当前的课程学习框架对采样策略选择敏感，需要人工设定合理的更新频率和初始权重。

4. **评估的模态局限**：所有实验均基于胸部 X 光片，泛化至 CT、MRI 等其他医学影像模态尚未验证。幻觉评估依赖外部大型语言模型（Gemini 2.5 Flash Lite），可能引入评估噪声。

### 补充图表

![[assets/figures/papers/paper_list_l2070_https_arxiv_org_abs_2601_15408/figures/005_Table_3.jpg]]
*Table 3: Results for Anatomy-Grounded Report Generation (AGRG) on Chest ImaGenome (CIG). We report mean IoU $(\delimiter$ "3222378 ), CheXbert F1 (micro/macro) $(\delimiter$ "3222378 ), CheXbert cosine similarity $(\delimiter$ "3222378 ), and CXRFEScore $(\delimiter$ "3222378 ). Bold values indicate the best performance for each metric*

![[assets/figures/papers/paper_list_l2070_https_arxiv_org_abs_2601_15408/figures/004_Table_2.jpg]]
*Table 2: Results for Phrase Grounding (PG). We report Micro-Average IoU (IoU Mi. $\delimiter$ "3222378 ) and Macro-Average IoU (IoU Ma. $\delimiter$ "3222378 ) on three test sets: MS-CXR, PadChest-GR, and zero-shot VinDr-CXR. CURE consistently improves localization performance across all metrics and datasets, including VinDr-CXR, which was not seen during training*

![[assets/figures/papers/paper_list_l2070_https_arxiv_org_abs_2601_15408/figures/009_Table_7.jpg]]
*Table 7: Ablation Study. We evaluate the contribution of each component across three grounding tasks. CXRS denotes the CXRFEScore metric. For Phrase Grounding (PG), we report Micro-Averaged IoU on MS-CXR (MS), PadChest-GR (PC), and VinDr-CXR (VD). Note that: CL(f ) indicates curriculum learning with a reweighting frequency of f steps, CIG(s) denotes a Chest ImaGenome pre-training stage of s steps, HPS refers to hyperparameter search. Bold and underlined values indicate the best and second-best models per metric, respectively*

![[assets/figures/papers/paper_list_l2070_https_arxiv_org_abs_2601_15408/figures/002_Table_1.jpg]]
*Table 1: Dataset composition and statistics. Number of instances for each task across the training, validation, and test splits. The MIMIC-CXR dataset serves as a superset, providing the Chest ImaGenome (CIG) and MS-CXR subsets for training and its official test split for report-generation evaluation. Evaluation-only datasets are used to assess generalization performance. AGRG refers to Anatomy Grounded Report Generation, PG to Phrase Grounding, and GRG to Grounded Report Generation*

![[assets/figures/papers/paper_list_l2070_https_arxiv_org_abs_2601_15408/figures/006_Table_4.jpg]]
*Table 4: Results for Grounded Report Generation (GRG) on PadChest-GR and zero-shot VinDr-CXR. We report mean IoU $(\delimiter$ "3222378 ), CheXbert F1 (micro/macro) $(\delimiter$ "3222378 ), CheXbert cosine similarity $(\delimiter$ "3222378 ), and CXRFEScore $(\delimiter$ "3222378 ). Bold values indicate the best score for each metric*

![[assets/figures/papers/paper_list_l2070_https_arxiv_org_abs_2601_15408/figures/007_Table_5.jpg]]
*Table 5: Results for Report Generation (RG) on the MIMIC-CXR test set. We report CheXbert F1 (F1-Ma/Mi) $(\delimiter$ "3222378 ), Precision (P-Ma/Mi) $(\delimiter$ "3222378 ), and Recall (R-Ma/Mi) $(\delimiter$ "3222378 ), each macro (Ma) and micro (Mi) averaged together with CheXbert Cosine Similarity (Cos.) $(\delimiter$ "3222378 ), CXRFEScore (CXRFES) $(\delimiter$ "3222378 ), RaTEScore (RaTES) $(\delimiter$ "3222378 ), and RadGraph F1 (RadF1) $(\delimiter$ "3222378 ). Bold and underlined values indicate the best and second-best models per metric, respectively*

![[assets/figures/papers/paper_list_l2070_https_arxiv_org_abs_2601_15408/figures/010_Figure_3.jpg]]
*Figure 3: Qualitative Examples. Qualitative phrase grounding (PG) results on challenging examples from the VinDr-CXR and PadChest-GR datasets. The left panels show the detection of a “Nodule or mass” (VinDr-CXR), while the right panels demonstrate the grounding of “Surgical staples” (PadChest-GR). Ground-truth regions are shown in green for reference, and model predictions from MAIRA-2 and CURE are shown in red*

![[assets/figures/papers/paper_list_l2070_https_arxiv_org_abs_2601_15408/figures/012_Figure_4.jpg]]
*Figure 4: Visualization of Inter-Dataset Weight Dynamics. This plot illustrates the curriculum’s adaptation from an experiment with frequent updates (every 500 steps). It shows how sampling probabilities for each data source evolve over time in response to the model’s performance*

![[assets/figures/papers/paper_list_l2070_https_arxiv_org_abs_2601_15408/figures/017_Table_12.jpg]]
*Table 12: Sensitivity Analysis of the Curriculum Weighting Term (α). Performance metrics on the Chest ImaGenome dataset (AGRG task) after 3000 training steps across different values of α. Higher values of α heavily weight the IoU metric during curriculum updates, while lower values prioritize the text-based semantic metric (CXRFEScore). We report mean Intersection-over-Union (IoU$, \delimiter$ "3222378 ), CheXbert F1 (Micro/Macro averages$, \delimiter$ "3222378 ), CheXbert cosine similarity (Cos.$, \delimiter$ "3222378 ), and CXRFEScore (CXS$, \delimiter$ "3222378 ). Bold indicates the best result per column*

## 方法谱系与知识库定位

### 核心瓶颈与设计动机

标准多任务训练在医学视觉-语言模型（VLM）中面临双重困境：**数据分布严重不均**（不同数据集和类别间样本量悬殊），且传统发现生成目标天然偏向异常描述，导致模型**视觉定位能力薄弱**，生成的报告包含大量与图像证据不一致的虚假异常（幻觉）。CURE 的因果调控旋钮在于：用**错误感知的课程学习**在数据集间和类别内动态调整采样权重，同时以**解剖学基础报告生成（AGRG）**替代传统发现生成目标，迫使模型同时学习“定位”与“正常/异常描述”。核心洞察是：无需额外数据，仅通过课程引导的多任务训练即可让医学 VLM 学会定位并描述解剖区域，同时平衡正常与异常样本，大幅提升定位准确性和报告可信度。

### 与基线方法的关系

CURE 建立在两个关键基线之上：

- **MAIRA-2**：当前最先进的开放式医学 VLM，联合学习短语定位（PG）和标准报告生成（RG）。CURE 将其作为直接对比对象，在**不引入额外数据**的前提下，通过以下四个关键槽位变化实现超越：
  - **核心监督任务**：从“PG + RG”替换为 AGRG 的三个子任务（Locate / Describe / Locate and Describe），将定位与描述深度耦合。
  - **数据采样策略**：从按数据集大小比例均匀采样，改为错误感知课程学习，在数据集间和类别内动态调整采样概率。
  - **基础模型预训练**：从无专门预训练改为在 Chest ImaGenome 上进行 3000 步的定位-描述预训练，使 MedGemma-4B-IT 获得初始视觉定位能力。
  - **学习率**：从 $2 \times 10^{-5}$ 提升至 $2 \times 10^{-4}$，在预训练和多任务微调阶段均适用，带来最显著的性能跃升。

- **MedGemma-4B-IT**：作为预训练基础医学 VLM，本身缺乏视觉定位能力。CURE 在其上通过 LoRA（rank=16，4-bit 精度）微调，证明了课程学习和 AGRG 任务设计能够“激活”基础模型的定位潜能。

### 方法谱系中的定位

CURE 的方法论贡献可分解为三个相互协同的模块：

1. **细粒度任务统一化**：将异构监督信号（PG、GRG、AGRG）统一为图像-指令-响应对，使多任务训练在统一格式下进行，降低了任务间的表示冲突。

2. **错误感知课程学习**：训练过程分为 $n$ 个迭代阶段，每阶段结束时在验证集上评估各数据源和类别的性能，计算加权评分 $s_i = \alpha \cdot \text{IoU}_i + (1 - \alpha) \cdot \text{CXRFEScore}_i$，并基于归一化错误率 $p_i = e_i / \sum_{j=1}^K e_j$ 更新采样概率——错误率越高的数据源在下一阶段被采样的概率越大。这一机制迫使模型集中攻克薄弱环节，而非在已掌握的任务上浪费算力。

3. **边界框感知的数据增强**：应用空间变换和 CLAHE 增强时同步修改边界框坐标，保证监督信号一致性，避免增强破坏定位标注。

在知识库层面，CURE 填补了“**课程学习 × 医学 VLM 多任务训练**”的交叉空白。现有课程学习方法多用于单任务场景或简单多任务组合，CURE 首次将错误感知的课程学习引入医学影像的定位-描述联合训练，并在数据集级和类别级两个粒度上同时运作。

### 适用边界与局限

- **数据利用率受限**：由于计算资源限制，训练中仅能利用 Chest ImaGenome 约 1.74% 的实例，可能制约模型性能上限。
- **文本语义指标提升有限**：课程学习策略未直接优化临床发现的分布不平衡，导致 CheXbert F1 等文本语义指标的提升相对定位指标不够显著。
- **小数据集任务脆弱性**：纯自然采样策略（v15）使小数据集任务（如 GRG）完全崩溃（IoU 0.000），凸显了在多任务学习中主动平衡数据分布的必要性——课程学习正是对此的解决方案。
- **模态泛化未验证**：评估局限于胸部 X 光片，泛化至其他医学影像模态（如 CT、MRI）尚未验证。
- **评估噪声风险**：幻觉与一致性评估依赖外部大型语言模型（Gemini 2.5 Flash Lite），可能引入评估噪声，需人工抽检确认结论稳健性。

### 开放问题

1. **多维重新加权策略**：如何设计同时平衡解剖区域和罕见/长尾临床发现的采样策略，在维持定位精度的前提下进一步提升语义报告质量？
2. **跨模态课程学习**：课程学习策略能否扩展至其他医学影像模态及多模态输入，并保持类似的提升效果？
3. **细粒度发现平衡**：能否通过更细粒度的正面/负面发现平衡策略，在定位精度和报告文本指标之间取得更好的帕累托前沿？

## 原文 PDF

![[paperPDFs/CVPR_2026/CURE_Curriculum_guided_Multi_task_Training_for_Reliable_Anatomy_Grounded_Report_Generation.pdf]]
