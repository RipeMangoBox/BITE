---
title: "Text-Driven 3D Hand Motion Generation from Sign Language Data"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Text_Driven_3D_Hand_Motion_Generation_from_Sign_Language_Data.pdf
code_link: null
project_link: "https://imagine.enpc.fr/~leore.bensabath/HandMDM/"
aliases:
- HHMDM
- TD3HMGFSLD
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "利用手语字典的语音学属性（SignBank）和基于规则的运动脚本（HandMotionScript），通过LLM自动生成海量手部动作文本描述，从而驱动模型训练。"
primary_logic: "手语数据库中的音系属性可经LLM转化为多样化的自然语言描述，与基于规则的运动特征提取相结合，能高效构建百万级“动作-文本”对，使文本条件扩散模型（HandMDM）获得跨手语和非手语域的零样本泛化能力。"
claims:
- "使用SignBank音系属性+HandMotionScript生成的文本训练HandMDM，在BOBSL3DT seen测试集上R@1达21.68%，unseen测试集上R@1达22.99%，远优于仅使用gloss或随机文本的基线。"
- "基于THMR的自动变体分配相比随机分配显著提升检索性能，seen R@1从18.77%提升至21.68%。"
- "训练数据量增加与R@1性能单调递增相关（图3），证实大规模数据对模型至关重要。"
- "零样本迁移至ASL-Text和MS-ZSSLR-W数据集时，BOBSL3DT训练的HandMDM大幅超越从零训练的小数据基线（ASL-Text: R@1 17.09% vs 基线；MS-ZSSLR-W: R@1 15.39% vs 基线）。"
---

# Text-Driven 3D Hand Motion Generation from Sign Language Data

> [!tip] 核心洞察
> 手语数据库中的音系属性可经LLM转化为多样化的自然语言描述，与基于规则的运动特征提取相结合，能高效构建百万级“动作-文本”对，使文本条件扩散模型（HandMDM）获得跨手语和非手语域的零样本泛化能力。

| 字段      | 内容                                                                                                                 |
| ------- | ------------------------------------------------------------------------------------------------------------------ |
| 中文题名    | 基于手语数据的文本驱动3D手部动作生成                                                                                                |
| 英文题名    | Text-Driven 3D Hand Motion Generation from Sign Language Data                                                      |
| 会议/期刊   | CVPR 2026                                                                                                          |
| Links | [paper](https://arxiv.org/abs/2508.15902) · [Project](https://imagine.enpc.fr/~leore.bensabath/HandMDM) |
| Topic   | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method  | HandMDM (Hand Motion Diffusion Model)                                                                              |
| Dataset | BOBSL3DT-Test (Seen), BOBSL3DT-Test (Unseen), ASL-Text (zero-shot transfer), BOTH57M (zero-shot transfer)          |

> [!tip] 效果简介
> - BOBSL3DT-Test (Seen) 上，R@1 为 21.68%，对比 1.00% (LLM(Gloss))，变化 +20.68%。
> - BOBSL3DT-Test (Unseen) 上，R@1 为 22.99%，对比 5.17% (LLM(Gloss))，变化 +17.82%。
> - ASL-Text (zero-shot transfer) 上，R@1 为 17.09%，对比 Baseline (trained on ASL-Text)，变化 superior。

## 概要

**核心问题**：文本驱动的3D手部动作生成长期受困于数据瓶颈——现有数据集（如ASL-Text、MS-ZSSLR-W）仅包含约10²~10⁴个动作-文本对，且文本标注稀疏、缺乏自然语言多样性，难以支撑高质量生成模型的训练。

**核心思路**：该工作提出了一条从手语数据中自动化构建大规模“动作-文本”对的流水线。其关键洞察在于：手语字典（BSL SignBank）中的音系属性（如手形、位置、方向）和基于规则的运动脚本（HandMotionScript）所提取的几何特征，可经由大语言模型（LLM）转化为丰富、自由形式的自然语言描述，从而将原本缺乏文本标注的手语视频转化为百万级训练数据。

**方法定位**：所提出的HandMDM（Hand Motion Diffusion Model）基于MDM扩散框架，采用SMPL-X表达性身体模型以包含完整的手部关节旋转参数，在上半身动作-文本对上训练条件扩散模型。该方法在方法谱系上属于“基于扩散模型的文本条件人体动作生成”分支，区别于仅依赖SMPL根手部参数的方案，其创新集中在数据构建策略而非模型架构本身。

**主要结果**：
- 在BOBSL3DT的手动标注测试集上，HandMDM在seen和unseen手语符号上的R@1分别达到21.68%和22.99%，远超基于gloss或随机文本的基线（Table 2）。
- 训练数据规模与检索性能呈单调递增关系（Figure 3），验证了大规模数据的核心作用。
- 零样本迁移至ASL-Text（R@1 17.09%）和MS-ZSSLR-W（R@1 15.39%）时，模型大幅超越在目标域小数据上从零训练的基线（Table 4）；在非手语数据集BOTH57M上也展现出优越的迁移能力（Table 5）。

**局限性**：伪标签和LLM生成描述存在噪声；单目3D重建对手部细节和接触动作的捕捉仍有不足；测试集规模较小（unseen仅87个符号），泛化评估的可靠性需进一步验证。

### 问题背景

文本驱动的人体动作生成近年来取得了显著进展，但**手部动作生成**仍是一个被严重忽视的领域。手部是人类表达中最精细、最高频的交互器官，尤其在**手语**场景中，手形、位置、运动轨迹和方向共同构成完整的语义系统。然而，现有文本-动作生成模型几乎完全聚焦于全身运动（如行走、舞蹈），对手部动作的建模停留在简单的全局旋转参数层面，缺乏对手指关节、手形变化等细粒度运动的刻画。

造成这一空白的根本瓶颈在于**数据**：文本驱动的手部动作生成需要大规模、高质量的动作-自然语言描述配对数据，而这类数据极其稀缺。从表1的数据集对比可以看出，现有手部动作数据集要么缺少文本描述（如手语视频数据集仅提供gloss类别标签），要么规模极小——例如ASL-Text和MS-ZSSLR-W仅包含数百到数千个样本，远不足以支撑现代生成模型的训练需求。手工标注手部动作的自然语言描述成本极高且难以规模化，这构成了领域发展的核心障碍。

### 现有方法的缺口

当前文本-动作生成方法存在三个关键缺口：

1. **数据规模缺口**：现有带手部描述的数据集（如ASL-Text、BOTH57M）规模仅为$10^2$~$10^4$级别，而全身动作生成领域的HumanML3D等数据集已达$10^4$~$10^5$规模。小数据导致模型难以学习手部动作的丰富变化和文本-动作的对齐关系。

2. **表示能力缺口**：主流方法采用SMPL身体模型，其手部仅用全局旋转参数表示，无法刻画手指关节的独立运动。SMPL-X模型虽然包含完整的手部关节参数，但现有文本-动作生成工作尚未有效利用这一表示。

3. **跨域泛化缺口**：手语数据蕴含丰富的手部运动模式，但如何将这些模式迁移到非手语领域（如日常手势、物体操作）仍是一个开放问题。现有方法缺乏从手语数据中提取通用手部运动先验的机制。

### 本文动机

针对上述缺口，本文的核心动机是**利用手语数据的大规模可用性来突破手部动作生成的数据瓶颈**。手语字典（如SignBank）提供了系统化的手语音系属性标注（手形、位置、运动、方向等），这些属性本质上是对手部动作的结构化描述。如果能将这些属性自动转化为多样化的自然语言描述，并与大规模手语视频中的3D动作配对，就能以极低的成本构建百万级训练数据。

这一思路的关键洞察在于：**手语音系属性经大语言模型（LLM）转化后，可以生成超越手语范畴的通用手部动作描述**，使模型获得跨手语和非手语域的零样本泛化能力。基于此，本文提出HandMDM——一个基于SMPL-X表示、在大规模自动生成的动作-文本对上训练的文本条件手部动作扩散模型。

## 核心方法与创新机理

HandMDM的核心创新并非提出全新的生成模型架构，而是构建了一套从手语数据中自动化、大规模挖掘“3D手部动作-自然语言描述”对的数据引擎，从而绕开了文本驱动手部动作生成领域长期面临的数据瓶颈。其关键创新点可概括为三个环环相扣的changed slots。

### 1. 文本描述来源：从稀疏标注到LLM驱动的音系学-运动脚本联合生成

传统方法（如ASL-Text、MS-ZSSLR-W）依赖人工标注，仅能提供约$10^2$至$10^4$量级的稀疏文本描述。HandMDM彻底改变了文本来源：它利用手语字典**SignBank**的音系学属性（如手形、位置、运动等）和自研的基于规则的运动特征提取器**HandMotionScript (HMS)**（可计算距离、方向等动态特征），通过大语言模型（Gemini 2.5 Pro）的少样本提示学习，将结构化的属性自动转化为多样化的自由形式自然语言描述（Sec 3.1, Fig 2）。这一设计使得文本描述不再受限于人工标注的规模和多样性，为后续模型训练提供了语义丰富的监督信号。

### 2. 训练数据规模：从万级到百万级的跨越

数据来源的创新直接推动了训练数据规模的质变。基线数据集（如ASL-Text、MS-ZSSLR-W）仅包含约$10^2$至$10^4$个动作-文本对，而HandMDM构建的**BOBSL3DT**数据集包含**120万个**动作-文本对（Table 1, Sec 3.1）。这一规模跨越是关键性能提升的因果杠杆：消融实验（Figure 3）证实，训练数据量与检索指标R@1呈单调递增关系，验证了大规模数据对模型的核心驱动作用。

### 3. 身体模型表示：从SMPL到SMPL-X的完整手部关节建模

基线方法多采用SMPL身体模型，其手部参数仅为根节点旋转，无法精细刻画手指关节运动。HandMDM将身体模型升级为**SMPL-X**，该模型包含完整的手部关节旋转参数（Sec 3.2）。这一改变使得扩散模型能够直接生成包含手指细节的上半身动作，为手语和非手语域的手部运动生成提供了必要的表示能力。在重建阶段，该方法通过轻量优化将HAMER的手部估计拼接到SMPLer-X的身体估计上，以获得更优的手部捕捉质量（Sec 3.1）。

### 4. 手语变体分配：从随机分配到基于动作相似度的自动匹配

手语字典中同一符号（gloss）常存在多个变体，如何将字典描述分配给具体的BOBSL视频动作是一个关键细节。随机分配会引入训练噪声，而HandMDM提出了基于**THMR**（Text-to-Hand-Motion Retrieval）动作嵌入的自动分配策略：利用k-medoids聚类和动作嵌入相似度，将字典描述精准分配给对应的动作变体（Sec 3.1）。消融实验（Table 3）表明，这一自动分配策略相比随机分配，将seen测试集的R@1从18.77%提升至21.68%，证实了其有效性。

综上，HandMDM的创新本质在于**数据优先**：通过手语字典音系学属性、HandMotionScript运动脚本和LLM的协同，将手语数据转化为大规模、高质量的动作-文本对，从而赋予文本条件扩散模型跨手语（BSL→ASL）和非手语域（BOTH57M）的零样本泛化能力。这一方法论为数据稀缺领域的文本驱动动作生成提供了可复用的范式。

![[assets/figures/papers/paper_list_l15_https_arxiv_org_abs_2508_15902/figures/003_Figure_2.jpg]]
*Figure 2: Our approach: We illustrate an overview for our data collection methodology, enabling to generate free-form textual descriptions via LLM prompting, given phonological attributes from a sign language dictionary (SignBank [21]), as well as those detected with our HandMotionScript. The generated hand motion descriptions are then assigned to video-based BOBSL [2] motions thanks to the automatic pseudo-glosses combined with our THMR-based assignment. We employ a combination of SMPLer-X [9] and HAMER [57] to extract 3D motions from SignBank and BOBSL videos*

HandMDM 的整体 pipeline 围绕一个核心瓶颈展开：**缺乏大规模、带自然语言描述的高质量 3D 手部动作数据集**。为此，该方法构建了一条从手语视频到文本条件扩散模型的自动化数据生成与训练流水线，其因果机制在于利用手语字典的语音学属性（SignBank）与基于规则的运动脚本（HandMotionScript），通过 LLM 自动生成海量手部动作文本描述，从而驱动模型训练。

### 数据生成管线

如图 Figure 2 所示，数据收集分为五个级联模块：

1. **视频-手语片段提取**：利用伪标注分类器（VideoSwin）对 BOBSL 视频进行帧级伪标注，过滤低置信度帧，保留至少 6 帧的连续片段，并合并间隔小于 6 帧的相邻片段，形成约 190 万个视频-手语对。

2. **3D 动作重建**：对每个视频片段，分别使用 HAMER 进行手部姿态估计、SMPLer-X 进行身体姿态估计，再通过轻量优化将 HAMER 的手部参数拼接到 SMPLer-X 的身体模型上，得到统一的 SMPL-X 表示。这一步骤将 2D 视频转化为包含完整手部关节旋转参数的 3D 上半身动作序列。

3. **属性提取**：从 BSL SignBank 手语字典中提取每个手语符号的语音学属性（如手形、位置、运动等），同时通过 HandMotionScript 规则引擎计算距离、方向、速度等运动特征，作为动作的结构化描述。

4. **LLM 描述生成**：以少样本提示学习方式，使用 Gemini 2.5 Pro 将上述结构化属性转化为自由形式的自然语言描述。这是整个 pipeline 的关键创新点——手语数据库中的音系属性经 LLM 转化为多样化的自然语言，使得原本仅有关键词标注的手语数据获得了丰富的文本条件。

5. **变体分配**：由于 SignBank 中一个手语符号可能对应多个变体描述，论文利用 THMR 模型提取动作嵌入，通过 k-medoids 聚类将字典描述自动分配给 BOBSL 中的具体动作实例。最终保留约 120 万个动作-文本对（BOBSL3DT），远超现有手部动作数据集（通常仅 10²~10⁴ 量级）。

### 模型训练

在生成的 BOBSL3DT 数据集上，HandMDM 采用基于 MDM 框架的条件扩散模型。模型以 SMPL-X 上半身动作表示作为生成目标，以 T5 编码的文本描述作为条件，通过均方误差损失学习预测加入动作的噪声：

$$\mathcal{L}_{MSE} = \mathbb{E}_{\mathbf{x}_0, \epsilon, t} \| \epsilon - \epsilon_\theta(\mathbf{x}_t, t, \mathbf{c}) \|^2$$

训练时以 5% 概率丢弃文本条件，以便测试时使用无分类器引导。扩散步数设为 100。

### 输入输出流

- **输入**：自由形式的自然语言文本描述（如 "the right hand forms a flat handshape and moves upward from the chest"）
- **输出**：SMPL-X 参数化的 3D 上半身动作序列，包含身体姿态、手部关节旋转等完整参数
- **关键变化**：相比基线使用 SMPL（仅含根手部参数），HandMDM 采用 SMPL-X 表示，能够刻画丰富的手部动作细节

### 方法定位

该框架的核心洞察在于：**手语数据库中的音系属性可经 LLM 转化为多样化的自然语言描述，与基于规则的运动特征提取相结合，能高效构建百万级“动作-文本”对**。这使得原本因数据稀缺而难以训练的文本驱动手部动作生成模型，获得了跨手语（BSL→ASL）和非手语域（BOTH57M）的零样本泛化能力。该方法属于“利用结构化知识库+LLM 进行大规模弱监督数据增强”的技术路线，与依赖人工标注或小数据集训练的基线方法形成显著差异。

### 3.1 数据生成流水线：从手语视频到文本-动作对

HandMDM 的核心贡献在于构建大规模文本-动作对的数据生成流水线，其瓶颈突破点在于利用手语字典的音系属性与规则化运动脚本，通过 LLM 自动生成多样化自然语言描述。流水线包含以下关键模块：

**视频-手语片段提取**
利用基于 VideoSwin 的伪标注分类器对 BOBSL 手语视频进行帧级 gloss 预测，过滤低置信度帧，保留至少 $m=6$ 帧的连续手语片段，并将间隔小于 $m$ 帧的相邻片段合并，最终获得约 190 万视频-手语片段对。

**3D 动作重建**
采用 HAMER 进行手部姿态估计，SMPLer-X 进行身体姿态估计，通过轻量优化将 HAMER 的手部估计拼接到 SMPLer-X 的身体模型上，得到统一的 SMPL-X 表示。该混合策略显著优于单独使用 SMPLer-X 的手部组件（见附录 Fig. A.3）。

**属性提取：SignBank + HandMotionScript**
从 BSL SignBank 手语字典中提取音系属性（如手形、位置、运动方向等），同时引入 HandMotionScript 规则引擎，计算手部间的距离（远/近/接触）、相对方向（上/下/左/右等）及运动轨迹特征。两者互补：SignBank 提供语言学结构化属性，HMS 补充动态运动的空间关系描述。

**LLM 描述生成**
使用 Gemini 2.5 Pro，通过少样本上下文学习将结构化属性转化为自由形式的自然语言描述。提示模板包含音系属性、HMS 特征以及示例描述，引导 LLM 生成多样化、覆盖手形和运动细节的文本。

**变体分配**
手语字典中同一 gloss 可能对应多个变体描述。本文利用 THMR 模型提取动作嵌入，通过 k-medoids 聚类将字典描述自动分配给 BOBSL 中的实际动作实例。相比随机分配，该策略显著降低训练噪声（Table 3）。

最终数据集 BOBSL3DT 包含约 120 万动作-文本对，远超现有手部动作数据集（Table 1）。

### 3.2 HandMDM 扩散模型

HandMDM 基于 MDM 框架，将扩散模型适配到 SMPL-X 上半身动作生成。模型以文本条件 $\mathbf{c}$ 和噪声动作 $\mathbf{x}_t$ 为输入，预测注入的噪声 $\epsilon$，训练目标为标准均方误差损失：

$$\mathcal{L}_{MSE} = \mathbb{E}_{\mathbf{x}_0, \epsilon, t} \| \epsilon - \epsilon_\theta(\mathbf{x}_t, t, \mathbf{c}) \|^2$$

其中 $\mathbf{x}_0$ 为干净动作，$\epsilon \sim \mathcal{N}(0, \mathbf{I})$ 为高斯噪声，$t$ 为扩散时间步，$\epsilon_\theta$ 为可学习的去噪网络。扩散步数设为 100，训练时以 5% 概率丢弃文本条件以支持测试时的无分类器引导。

## 实验与关键发现

### 核心实验结果：BOBSL3DT 基准上的文本条件生成与检索

HandMDM 在 BOBSL3DT 测试集上的表现，直接验证了“大规模自动标注数据+文本条件扩散模型”这一技术路线的有效性。实验将测试集划分为 **Seen Signs**（722个动作实例）和 **Unseen Signs**（87个动作实例），以分别考察模型对已知手语符号的拟合能力与对未知符号的泛化能力。评估指标采用运动-运动检索（motion-to-motion retrieval）的 R@1、R@3 和 FID。

**Table 2** 的核心结论如下：

![[assets/figures/papers/paper_list_l15_https_arxiv_org_abs_2508_15902/figures/004_Table_2.jpg]]
*Table 2: Effect of input control: We evaluate models trained with different input formats on the seen and unseen signs of the BOBSL3DT manually-glossed test set. There are 722 / 87 ground-truth motion instances in these seen/unseen sets (with one motion instance per gloss), and we report the motion-to-motion retrieval from our generation to the ground truth. Note that the first two rows use a different input at test time, strictly following the format used during training time (as opposed to the last three rows that are trained and tested with free-form text). For the three variants of LLM-generated descriptions, we test on text generated only from SignBank phonology attributes, as well as adding th...*

- **LLM(Phonology+HMS) 取得最佳综合性能**：当使用 SignBank 音系属性与 HandMotionScript（HMS）共同作为 LLM 输入生成文本描述时，模型在 Seen 测试集上 R@1 达到 **21.68%**，在 Unseen 测试集上 R@1 为 17.53%。这一结果表明，HMS 提供的动态运动特征（如距离、方向）有效补充了 SignBank 静态音系属性的不足，使文本描述更准确地捕捉了手部动作的时空特性。
- **LLM(Phonology) 在 Unseen 场景下意外领先**：仅使用 SignBank 音系属性的模型在 Unseen 测试集上 R@1 达到 **22.99%**，甚至略高于 Seen 场景。这可能暗示 HMS 引入的规则化描述在某些未见符号上反而限制了 LLM 的语义泛化空间，但该现象需要进一步验证。
- **基线方法的剧烈退化**：使用 Gloss（手语标注词）直接作为文本输入的模型 R@1 仅为 1.00%（Seen）和 5.17%（Unseen），使用随机文本则几乎完全失效。这从反面证明了自然语言描述的丰富语义空间对模型学习是不可或缺的，稀疏的类别标签无法提供足够的条件信号。

**FID 指标**进一步佐证了生成质量：LLM(Phonology+HMS) 在 Seen 测试集上 FID 低至 **0.16**，Unseen 测试集上为 0.40，表明生成动作的分布与真实动作高度一致。

### 消融实验：数据规模、输入控制与变体分配

**1. 训练数据规模的单调增益（Figure 3）**

![[assets/figures/papers/paper_list_l15_https_arxiv_org_abs_2508_15902/figures/007_Figure_3.jpg]]
*Figure 3: Training data size: We plot R@1 performance on the seen/unseen test sets of BOBSL3DT against different proportions of the training data, and observe a monotonic increase with larger training. Table 3. Assignment: We observe gains with our automatic sign variant assignment using THMR, as opposed to randomly assigning a variant during training*

Figure 3 展示了 R@1 性能随训练数据比例增加的变化曲线。结果显示，无论是 Seen 还是 Unseen 测试集，R@1 均随数据量增加而**单调递增**，未见饱和迹象。这一证据直接支撑了论文的核心主张：**大规模数据是文本驱动手部动作生成的关键瓶颈**，而本文提出的自动化数据收集管线正是突破该瓶颈的因果杠杆。

**2. HandMotionScript 的因果作用（Table 2）**

Table 2 中一个关键的对照实验揭示了 HMS 的因果机制：如果训练时**未使用** HMS 描述，而测试时**使用** HMS 描述，模型性能会从 21.68% 急剧下降至 **6.30%**（Seen R@1）。这说明 HMS 引入的规则化运动语言（如“手从胸前向外移动”）构成了一个独立的语义子空间，模型必须在训练阶段学习该子空间与运动特征的映射关系，否则在推理时无法理解此类描述。这一发现揭示了“训练-测试输入格式一致性”对于 LLM 生成文本训练的重要性。

**3. 基于 THMR 的自动变体分配优于随机分配（Table 3）**

手语字典中同一符号常存在多个变体（variants），如何将字典中的多个文本描述分配给 BOBSL 视频中提取的海量动作实例，直接影响训练数据的质量。Table 3 表明：

- 使用 **THMR 动作嵌入 + k-medoids 聚类** 进行自动分配，Seen R@1 达到 **21.68%**。
- 采用**随机分配**策略，Seen R@1 降至 18.77%。

这一增益的因果机制在于：THMR 通过动作嵌入的相似度将语义相近的变体描述分配给对应的运动实例，减少了训练数据中的“文本-动作”错配噪声，从而提升了条件扩散模型的映射精度。

### 零样本迁移：跨语言、跨域泛化能力

HandMDM 的核心价值不仅在于域内性能，更在于其**零样本迁移**能力——即在一个大规模数据集（BOBSL3DT）上训练后，直接泛化到其他小规模、不同语言或非手语域的数据集。

**Table 4 展示了向美国手语（ASL）数据集的迁移结果**：

- 在 **ASL-Text** 数据集上，BOBSL3DT 训练的 HandMDM（Phonology+HMS）取得 R@1 **17.09%**，显著优于在 ASL-Text 上从零训练的小数据基线（具体基线值未提供，但论文明确指出“superior overall performance”）。
- 在 **MS-ZSSLR-W** 数据集上，同样取得 R@1 **15.39%** 的零样本性能，再次超越基线。
- 值得注意的是，FID 指标在跨域评估时有所上升，论文将此归因于**数据集特定的运动风格差异**（如不同手语的动作速度、幅度习惯），这是域迁移中的可预期现象。

**Table 5 展示了向非手语数据集 BOTH57M 的迁移结果**：

- BOTH57M 包含全身动作中的手部描述，域差异更大。HandMDM 在此数据集上 R@3 达到 **44.19%**，同样优于在 BOTH57M 上从零训练的基线模型。
- 这一结果表明，从手语数据中学到的手部运动先验具有**跨域可迁移性**，不仅限于手语域，还能泛化到日常手部动作描述。

**定性结果（Figure 4, Figure 5）** 进一步印证了定量结论：在 ASL-Text、MS-ZSSLR-W 和 BOTH57M 的测试样例中，从零训练的基线模型生成的动作往往模糊或与文本描述不符，而 BOBSL3DT 训练的 HandMDM 能生成更准确、更具辨别性的手部形态和运动轨迹。在 BOBSL3DT Unseen 测试集上，模型对未见符号的生成结果与真实动作高度相似。

![[assets/figures/papers/paper_list_l15_https_arxiv_org_abs_2508_15902/figures/030_Figure_5.jpg]]
*Figure 5: Figure A.9. Qualitative results on the seen test set of BOBSL3DT-Test: We complement Fig. 5 of the main paper (which shows results on the unseen test set), with results on the seen signs. We display both single-frame and dynamic visualizations for each example*

### 公平性说明与评估局限

论文在实验设计上考虑了若干公平性因素，但仍存在需要关注的偏差：

- **域内评估偏差**：THMR 检索模型本身在 BOBSL3DT 上训练，用于评估 BOBSL3DT 测试集时可能存在域内偏好。跨域评估时，论文仅使用手臂和手部运动特征以避免不公平比较，但未完全消除该偏差。
- **ASL 测试集的语义修改**：ASL-Text 测试集中的 ASL 特定手形名称被替换为英文描述，可能部分改变了原始语义，影响评估的准确性。
- **伪标签与 LLM 噪声**：伪标注分类器的错误标签和 LLM 生成描述的不完美是训练数据的固有噪声源，论文采用“高规模-高噪声”策略来弥补，但噪声对特定符号的影响未做细粒度分析。
- **测试集规模有限**：Unseen 测试集仅包含 87 个手语符号，可能不足以充分评估模型对长尾符号的泛化能力，结论的外推需谨慎。

![[assets/figures/papers/paper_list_l15_https_arxiv_org_abs_2508_15902/figures/023_Figure_1.jpg]]
*Figure 1: Figure A.6. Dynamic visualization for Fig. 1 of the main paper: We display the same examples as in Fig. 1 with a dynamic style including 5 framesPush the bent middle finger of the right flat and The person extends their index finger on the left evenly sampled. The color coding denotes the temporal evolution, i.e., the last frame with blue, and the first frame with decreased transparency in pink.movement from in front of each shoulder. spread hand across the back of the left open hand, hand and curls the other fingers, while doing the same Figure A.7. Dynamic visualization for Fig. 4 of the main paper*

![[assets/figures/papers/paper_list_l15_https_arxiv_org_abs_2508_15902/figures/002_Table_1.jpg]]
*Table 1: 3D hand motion datasets: We summarize datasets that contain hand motions and various types of text annotations (e.g., speech, sign categories, hand descriptions). Sign language (SL) datasets capturing motions in studio [22] or estimating 3D motions from videos [4, 17, 88] do not come with hand descriptions. Those with hand descriptions are small [6, 7]. Full-body motion capture (mocap) datasets [38, 91] are less diverse on hand motions and smaller in size than our BOBSL3DT dataset. †We report the statistics of hand descriptions from the BOTH57M dataset, which contains 3,229 motions from a vocabulary of 3,539 words if body descriptions are also included. Note we calculate statistics upon dow...*

## 定位与知识库关联

### 1. 核心瓶颈与因果机制

本工作的根本瓶颈在于**文本驱动3D手部动作生成领域长期受困于数据稀缺**：现有带手部描述的数据集规模仅约10²~10⁴个样本（如ASL-Text、MS-ZSSLR-W、BOTH57M），远不足以训练出具备泛化能力的条件生成模型。这一瓶颈的因果根源在于手部动作标注成本极高——手语动作涉及精细的手指关节配置、手掌朝向、空间位置等多维属性，人工撰写自然语言描述几乎不可行。

论文的核心因果操纵杆（causal knob）是**利用手语字典的语言学属性作为“中间表示”**，将昂贵的人工标注问题转化为可自动化的属性提取与LLM描述生成问题。具体而言，BSL SignBank字典提供了每个手语符号的**音系属性**（如手形、位置、运动、朝向等），而作者设计的**HandMotionScript**（HMS）规则引擎则从3D动作中自动提取距离、方向等运动特征。这两类结构化属性通过**Gemini 2.5 Pro** LLM的少样本提示学习，被转化为多样化的自由形式自然语言描述，从而以极低成本构建了**120万动作-文本对**的BOBSL3DT数据集。

这一数据生成策略的核心洞察在于：**手语字典的音系属性经LLM可转化为具有足够语义多样性的自然语言描述**，使得在此数据上训练的条件扩散模型（HandMDM）能够学习到跨手语符号、乃至跨手语语种的手部动作-文本对齐能力，从而获得零样本迁移至ASL-Text、MS-ZSSLR-W等小数据集的能力。

### 2. 与基线方法的关系与关键改进槽位

HandMDM建立在**MDM**（Motion Diffusion Model）框架之上，但在以下关键槽位上进行了实质性改进：

| 改进槽位 | 基线做法 | 本工作做法 | 证据锚点 |
|---------|---------|-----------|---------|
| **文本描述来源** | 手工标注或小数据集中的稀疏文本说明 | LLM基于SignBank音系属性+HMS自动生成大规模自然语言描述 | Sec 3.1, Fig 2 |
| **训练数据规模** | ~10²~10⁴个动作-文本对 | 120万个动作-文本对 | Table 1, Sec 3.1 |
| **身体模型表示** | SMPL（仅含根手部参数） | SMPL-X（含完整手部关节旋转参数） | Sec 3.2 |
| **手语变体分配** | 随机分配描述给动作 | 基于THMR动作嵌入相似度的自动分配 | Table 3, Sec 3.1 |

在身体模型表示方面，本工作将MDM框架从SMPL扩展至**SMPL-X**，使得模型能够显式建模手指关节的旋转参数。3D动作重建采用**HAMER**（手部估计）与**SMPLer-X**（身体估计）的拼接策略，经轻量优化获得上半身SMPL-X表示。这一设计使得HandMDM能够生成比纯SMPL表示更精细的手部动作。

在训练策略上，HandMDM采用100步扩散过程，以5%概率丢弃文本条件以支持测试时的无分类器引导（classifier-free guidance），损失函数为标准的均方误差去噪损失：
$$\mathcal{L}_{MSE} = \mathbb{E}_{\mathbf{x}_0, \epsilon, t} \| \epsilon - \epsilon_\theta(\mathbf{x}_t, t, \mathbf{c}) \|^2$$

### 3. 适用边界与数据依赖

HandMDM的适用边界受到以下因素制约：

**数据来源依赖性**：该方法高度依赖手语字典（SignBank）提供的音系属性标注。对于没有类似语言学资源的手语语种，需要先构建字典才能复用该流程。论文在ASL上的零样本迁移（Table 4, R@1 17.09%）表明跨语种迁移可行，但性能仍低于域内训练。

**伪标签噪声容忍度**：BOBSL视频的手语片段提取依赖**VideoSwin伪标注分类器**，其预测本身存在噪声。论文采用“高规模-高噪声”策略——通过1.2M训练样本的规模优势来弥补单样本标注质量的不足。Figure 3的训练数据规模消融实验证实了R@1随数据量单调递增，验证了这一策略的有效性，但也暗示对伪标签质量极度敏感的场景可能不适用。

**3D重建精度限制**：单目视频的3D重建（HAMER+SMPLer-X拼接）对手部细节和接触动作的捕捉仍有不足，面部参数质量不足以刻画手语中的丰富面部表情。这限制了模型在需要高精度手指交互（如手语中的接触手形）或面部表情协同的场景中的表现。

**评估偏差**：用于检索评估的THMR模型在BOBSL3DT域内训练，跨域评估时可能存在域内偏差。论文在跨域数据集上仅使用手臂/手部运动特征来缓解此问题，但无法完全消除。

### 4. 已知局限与开放问题

**已确认的局限性**（来自论文讨论与消融实验）：

1. **训练-测试输入格式不匹配的脆弱性**：当模型训练时未使用HMS描述，但测试时使用HMS描述时，性能大幅下降（seen R@1从21.68%降至6.30%，Table 2）。这表明模型对输入文本的分布偏移敏感，泛化鲁棒性有限。

2. **测试集规模限制**：未见手语符号测试集仅含87个动作实例，可能影响泛化评估的统计可靠性。

3. **仅生成上半身动作**：当前模型未包含下半身，无法建模全身协同运动（如手语中涉及身体位移的符号）。

4. **变体分配策略的噪声**：用于变体分配的THMR模型本身使用随机分配训练，可能引入额外的噪声和偏差。

**开放问题**：

1. **字典扩展性**：该方法能否推广至其他手语字典（如ASL-LEX），以进一步增加训练数据的规模和语言多样性？这需要验证不同字典的属性体系是否兼容。

2. **精细接触动作生成**：如何提升手部接触、触摸等精细动作的生成精度？论文建议引入明确的接触检测与约束，但尚未实现。

3. **面部表情融合**：能否将面部表情生成融合进扩散模型，实现更完整的手语生成？这需要高质量的面部3D重建数据支持。

4. **扩散超参数探索**：引导系数、采样步数等超参数对生成多样性与质量的trade-off尚未充分探索，可能影响实际部署时的效果调优。

5. **全身动作扩展**：该方法能否从上半身手部动作生成推广至全身协同动作生成？这需要解决下半身动作与手部动作的协调建模问题。

### 5. 在知识库中的定位

本工作在文本驱动人体动作生成领域占据了一个独特的交叉位置：它**桥接了手语语言学资源与数据驱动的生成模型**。与直接从少量手工标注数据训练的方法（如ASL-Text上的从零训练基线）相比，HandMDM通过自动化数据收集流程实现了数量级的训练数据扩展。与使用gloss（手语符号标签）作为条件的方法相比，LLM生成的自然语言描述提供了更丰富的语义信息，使得模型能够泛化到未见手语符号和非手语手部动作。

该方法可视为**“语言学知识驱动的数据增强”范式**的一个实例，其核心思想——利用结构化领域知识（音系属性）通过LLM生成多样化训练数据——可能对数据稀缺的其他细粒度动作生成任务具有借鉴意义。但需要手动验证该方法在非手语领域的可迁移性，因为当前证据仅覆盖手语和有限的手部动作数据集（BOTH57M）。

## 原文 PDF

![[paperPDFs/CVPR_2026/Text_Driven_3D_Hand_Motion_Generation_from_Sign_Language_Data.pdf]]
