---
title: "Text Motion Translator: A Bi-Directional Model for Enhanced 3D Human Motion Generation from Open-Vocabulary Descriptions"
type: paper
paper_level: A
venue: ECCV
year: 2024
pdf_ref: paperPDFs/ECCV_2024/Text_Motion_Translator_A_Bi_Directional_Model_for_Enhanced_3D_Human_Motion_Generation_from_Open_Vocabulary_Descriptions.pdf
project_link: null
code_link: null
aliases:
- TTMT
tags:
- ECCV_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 引入大规模伪标签运动数据集LaViMo和LLM文本语义增强技术，将Text2Motion转化为语言翻译任务并通过多任务学习强化泛化能力。
primary_logic: 将3D人体运动表示为离散token序列，利用序列到序列的Transformer架构实现文本与运动间的双向翻译，并通过LLM增强文本描述覆盖开放词汇，从而无需独立时长输入即可生成自然连贯的运动。
claims:
- TMT在BABEL上的APE和AVE指标平均比第二名（EMS）高出33%。
- 多任务训练（Text2Motion、Motion2Text等）相比单任务训练为未见动作带来13%的提升。
- 使用LLM增强文本描述并配合启发式后处理过滤，平均性能提升17.3%。
- 模型具备双向生成能力，既能从文本生成运动（Text2Motion），也能从运动生成文本描述（Motion2Text）。
---

# Text Motion Translator: A Bi-Directional Model for Enhanced 3D Human Motion Generation from Open-Vocabulary Descriptions

> [!tip] 核心洞察
> 将3D人体运动表示为离散token序列，利用序列到序列的Transformer架构实现文本与运动间的双向翻译，并通过LLM增强文本描述覆盖开放词汇，从而无需独立时长输入即可生成自然连贯的运动。

| 字段 | 内容 |
|------|------|
| 中文题名 | 文本运动翻译器：面向开放词汇描述的增强3D人体运动生成双向模型 |
| 英文题名 | Text Motion Translator: A Bi-Directional Model for Enhanced 3D Human Motion Generation from Open-Vocabulary Descriptions |
| 会议/期刊 | ECCV 2024 |
| Links |  |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | TMT (Text Motion Translator) |
| Dataset | BABEL, HumanML3D |

> [!tip] 效果简介
> - BABEL 上，APE & AVE TMT (ours) vs Runner-up (EMS) (平均降低33%（更好）)；R-Precision@3 0.53 vs N/A (N/A)；FID 0.72 vs N/A (N/A)。
> - HumanML3D 上，R-Precision@3 0.528 vs N/A (N/A)；FID 0.184 vs N/A (N/A)；Diversity 9.437 vs N/A (N/A)。

## 概要

本文提出**TMT (Text Motion Translator)**，一个面向开放词汇描述的3D人体运动生成双向模型。其核心动机在于：现有Text2Motion方法受限于稀缺的3D运动-文本配对数据，且通常需要用户额外输入动作时长，导致对未见过的复杂描述泛化能力差、使用不友好。

**核心瓶颈**：3D人体运动数据及其对应文本描述稀缺，现有模型需额外输入动作时长，导致泛化能力差且用户不友好，尤其难以处理未见过的开放词汇描述。

**核心思路**：将文本条件3D人体运动生成转化为**语言翻译问题**。具体而言，通过VQ-VAE将3D运动编码为离散token序列，与文本token一起送入基于T5的序列到序列Transformer框架，实现文本与运动间的双向翻译。同时，引入大规模伪标签运动数据集**LaViMo**（约140k运动片段、130小时运动数据，规模约为现有数据集的4倍）和基于GPT-4的**LLM文本语义增强**技术，配合启发式后处理过滤，大幅提升开放词汇覆盖能力。

**方法定位**：TMT属于**序列到序列翻译范式**，区别于主流的条件VAE或扩散模型路线。其关键设计包括：(1) 运动VQ-VAE离散化表示；(2) 多任务联合训练（Text2Motion、Motion2Text、Text2Text、Motion2Motion）；(3) 无需独立时长输入的自回归生成。

**主要结果**：
- 在**BABEL**数据集上，TMT的APE和AVE指标平均比第二名**EMS** (Qian et al., ICCV 2023) 高出**33%**。
- 多任务训练相比单任务训练，为未见动作带来**13%**的提升，为已见动作带来**8%**的提升。
- LLM文本增强配合启发式后处理过滤，平均性能提升**17.3%**；若不进行后处理，已见动作质量下降，但仍有助于未见动作。

**局限与待解决问题**：模型对预训练数据集之外的全新动作描述仍面临挑战；LaViMo基于RGB视频估计的3D姿态可能引入噪声；LLM增强的质量依赖GPT-4和启发式规则的准确性。如何进一步提升开放词汇泛化能力、扩大预训练数据规模与多样性，是后续研究的关键方向。



3D人体运动生成旨在从自然语言描述中合成逼真的人体动作序列，在动画制作、虚拟现实和人机交互等领域具有重要应用价值。然而，该领域长期受困于一个核心瓶颈：**高质量3D人体运动数据及其对应的文本描述极度稀缺**。现有数据集规模有限，难以覆盖现实世界中丰富多样的动作语义，导致模型在面对开放词汇（open-vocabulary）描述时泛化能力严重不足。

现有方法在解决这一问题时存在两个显著缺口。其一，多数主流方法（如条件VAE或扩散模型）将运动建模为连续潜在向量或原始关节位置，缺乏对运动语义的离散化结构表示，难以建立文本与运动之间的细粒度对应关系。其二，许多模型要求用户额外输入动作时长作为生成条件——这一设计不仅降低了用户体验的自然性，更在根本上限制了模型对未见描述的自适应能力。以当前最优方法**EMS**（Qian et al., ICCV 2023）为例，其虽在精细化描述条件下取得了进展，但在开放词汇场景下仍面临明显的性能退化。

本文的核心动机在于**重新审视文本条件运动生成的本质**：如果将3D人体运动表示为离散token序列，那么Text2Motion问题是否可以转化为一个序列到序列的语言翻译任务？这一视角转换带来了两个关键优势：（1）可以利用成熟的序列翻译架构（如T5 Transformer）捕捉文本与运动之间的长程依赖；（2）可以通过多任务学习（文本到运动、运动到文本、文本到文本、运动到运动）对模型进行联合正则化，强化跨模态语义对齐。

此外，针对数据稀缺这一根本性瓶颈，本文提出从两个维度进行突破：**数据规模的扩展**与**文本语义的增强**。前者通过构建大规模伪标签运动数据集LaViMo（约14万段运动片段，130小时运动数据），将可用训练数据扩大约4倍；后者则利用大语言模型（GPT-4）对现有文本描述进行语义增强，生成覆盖更广泛表达方式的变体描述，从而提升模型对开放词汇的理解能力。

综上所述，本文的出发点是：通过“翻译框架+离散token化+多任务学习+数据增强”的组合策略，从根本上提升3D人体运动生成在开放词汇场景下的鲁棒性和泛化性，同时消除对时长输入等额外条件的需求。



## 核心方法与创新机理

TMT 的核心创新在于将文本条件的 3D 人体运动生成重新定义为**序列到序列的语言翻译问题**，并通过三个紧密耦合的“changed slots”系统性地突破现有方法的瓶颈。

### 1. 运动离散化：从连续潜变量到共享码本

现有方法（如基于 VAE 或扩散模型的方案）通常将运动建模为连续潜向量，或直接操作原始关节位置，这导致生成的运动缺乏结构约束，且难以与离散的文本 token 对齐。

TMT 引入了一个**运动 VQ-VAE**，将 3D 人体运动编码为离散的 token 序列。具体而言，该模块通过一个包含 $B$ 个嵌入向量的共享码本 $\breve{Z} = \{z_1, z_2, \ldots, z_B\} \in \mathbb{R}^{B \times \breve{D}}$，将连续运动映射为离散索引，并可从这些 token 重建运动。这一设计使得运动与文本在统一的离散表示空间中被处理，为后续的翻译框架奠定了基础。运动 VQ-VAE 在 LaViMo 和 AMASS 数据集的联合数据上预训练，其训练目标由三项损失驱动：重建损失 $\mathcal{L}_{rec}$、嵌入损失 $\mathcal{L}_{emb}$ 和承诺损失 $\mathcal{L}_{com}$，其中重建损失同时约束运动本身及其速度的平滑 L1 误差。

### 2. 文本语义增强：LLM 驱动的开放词汇覆盖

传统方法仅使用数据集中有限的原始文本描述进行训练，导致模型在面对训练集未见的开放词汇描述时泛化能力骤降。TMT 通过引入 **LLM 语义增强** 策略解决了这一瓶颈。

具体而言，TMT 利用 GPT-4 为原子动作的文本描述生成语义相似的变体，从而大幅扩展文本空间的覆盖范围。但直接使用所有 LLM 生成的描述会导致性能下降——分析表明，未经后处理的增强描述会引入误导性信息。为此，TMT 设计了一套**启发式后处理过滤规则**，专门剔除身体部位不匹配、静/动态状态混淆、方向错误等不合理描述。消融实验证实，LLM 增强配合后处理过滤带来了平均 **17.3%** 的性能提升（Table 4），而若去除过滤步骤，已见动作的质量会显著退化。

### 3. 多任务翻译框架：无需时长输入的联合学习

现有方法（如 **EMS**，Qian et al., ICCV 2023）通常需要额外输入动作时长，且仅执行单一的 Text2Motion 任务，导致用户交互不友好，且语义理解能力受限。

TMT 将生成框架构建于 **T5 Transformer** 的编码器-解码器架构之上，同时执行四个任务：**Text2Motion、Motion2Text、Text2Text 和 Motion2Motion**。在训练中，文本 token 和运动 token 被拼接为联合序列，并根据任务自适应地遮蔽不同部分，解码器自回归地预测被遮蔽的 token。这一多任务联合学习无需独立的时长输入，模型从数据中隐式学习动作的时序边界。消融实验（Table 4）表明，多任务训练相比单任务（Sin）训练，在未见动作上带来 **13%** 的提升，在已见动作上带来 **8%** 的提升，证明多任务正则化显著增强了模型对未见过动作的泛化能力。

### 4. 双向生成能力

作为翻译框架的自然延伸，TMT 具备**双向生成能力**：既可以从文本描述生成 3D 运动（Text2Motion），也可以从运动生成文本描述（Motion2Text）。Motion2Text 任务的损失函数为：

$$L_{M2T}^{j} = - \sum_{s=1}^{g} \sum_{i=0}^{L-1} \log p(t_{s;i}^{j} \mid \{ t_{r|r<s}^{j} \}, Z_{seg}^{j})$$

即给定运动 token 序列 $Z_{seg}^{j}$ 和已预测的文本 token，自回归地预测当前文本 token。这一能力在现有 Text2Motion 方法中尚属首次，为运动理解与描述生成提供了新的可能性。

### 创新总结

三个 changed slots 形成了一条清晰的因果链路：**LLM 文本增强** 解决了开放词汇覆盖不足的问题，**运动 VQ-VAE 离散化** 为统一表示提供了基础，而**多任务翻译框架** 则利用这些离散 token 实现了无需时长输入的鲁棒双向生成。三者协同作用，使 TMT 在 BABEL 数据集上的 APE 和 AVE 指标平均比第二名高出 **33%**。



TMT（Text Motion Translator）将文本条件3D人体运动生成重新定义为**序列到序列的语言翻译问题**。其核心思路是将连续的人体运动与自然语言描述统一表示为离散token序列，并通过一个共享的Transformer主干网络实现文本与运动之间的双向翻译。整个pipeline由三个关键阶段构成：**大规模伪标签运动数据集构建**、**运动离散化与文本增强**，以及**多任务翻译训练**。

### 数据准备阶段

为缓解3D人体运动-文本配对数据稀缺的瓶颈，TMT首先构建了**LaViMo（Large-scale Video Motion）数据集**。该数据集从互联网RGB视频中通过3D姿态估计流水线提取运动序列，规模约为现有数据集的4倍，包含约140k个运动片段，对应130小时的运动数据。姿态估计流水线结合了**HybrIK模块**进行快速初始化，以及**HuMoR**的测试时优化来提升精度，将单段2秒视频的处理时间从超过5分钟压缩至约30秒。这一大规模数据集为后续运动VQ-VAE的预训练提供了关键的数据基础。

### 运动离散化与文本增强

在运动侧，TMT引入一个**Motion VQ-VAE**，将连续的3D人体运动序列编码为离散的嵌入token，并能够从这些token重建原始运动。VQ-VAE在LaViMo与现有AMASS数据集的联合数据上进行预训练，学习一个包含$B$个离散嵌入向量的共享码本$\breve{Z} = \{z_1, z_2, \ldots, z_B\} \in \mathbb{R}^{B \times \breve{D}}$。输入运动$M_i$经编码器产生连续潜在嵌入$\hat{Z}_i$后，通过最近邻查找量化为码本中的离散token，再由解码器重建运动$\hat{M}_i$。

在文本侧，为覆盖开放词汇描述，TMT利用**LLM（GPT-4）**对原始动作文本描述进行语义增强，生成多样化的语义相似变体。增强后的描述经过**启发式后处理过滤**，剔除身体部位不匹配、静动态混淆、方向错误等不合理描述，确保增强文本的质量。

### 多任务翻译训练

TMT的核心生成模块基于**T5 Transformer**的编码器-解码器架构。训练时，来自同一原子动作的运动token序列$Z_{seg}^j = (z_1^j, z_2^j, \ldots, z_h^j)$与文本token序列$T_{seg}^j = (t_1^j, t_2^j, \ldots, t_g^j)$被拼接为联合输入。根据不同的任务目标，对联合序列施加不同的自适应mask模式，T5解码器自回归地预测被遮蔽部分。

TMT通过四个任务进行联合正则化：
- **Text2Motion**：给定文本token和运动历史上下文，自回归预测运动token序列，实现文本到运动的生成。
- **Motion2Text**：给定运动token序列，自回归预测文本token序列，实现运动到文本描述的生成。
- **Text2Text**和**Motion2Motion**：作为自监督辅助任务，分别对文本和运动token序列进行掩码预测，增强模型对各自模态内部语义的理解。

整个框架**无需独立输入动作时长**，模型在生成过程中自动确定运动的起止。多任务联合训练使得模型在已见动作和未见动作上均获得显著的泛化能力提升：相比单任务训练，多任务训练为未见动作带来13%的提升，为已见动作带来8%的提升。

### 补充图表

![[assets/figures/papers/paper_list_l1880_Text_Motion_Translator_A_Bi_Directional_Model_for_Enhanced_3D_Human_Moti/figures/002_Figure_2.jpg]]
*Figure 2: Model Structure Overview: We pretrain our Motion VQ-VAE on the combination of our LaViMo and existing AMASS datasets, then train our generation module on motion-text paired dataset*



TMT 将文本条件 3D 人体运动生成形式化为一个语言翻译问题。其核心架构由三个关键模块构成：运动 VQ-VAE（Motion VQ-VAE）、文本分词（Text Tokenization）以及基于 T5 的翻译骨干网络（T5 Translation Backbone）。以下逐一阐述各模块的设计逻辑与关键公式。

### 运动 VQ-VAE：连续运动到离散 Token 的桥梁

为解决 3D 人体运动数据的连续性与语言模型所需的离散符号之间的鸿沟，TMT 首先预训练一个运动 VQ-VAE。该模块将一段 3D 人体运动 $M_i = (m_1, m_2, \ldots, m_n)$（其中每帧姿态 $m_j \in \mathbb{R}^{D}$）编码为连续的潜在嵌入序列 $\hat{Z}_i = (\hat{z}_1, \hat{z}_2, \ldots, \hat{z}_n)$，随后通过查找一个可学习的离散码本 $\breve{Z} = \{z_1, z_2, \ldots, z_B\} \in \mathbb{R}^{B \times \breve{D}}$ 将其量化为离散 token 序列 $Z_i$。码本包含 $B$ 个维度为 $\breve{D}$ 的嵌入向量，每个运动帧被映射到码本中距离最近的嵌入向量，从而将连续运动转化为离散符号序列。

运动 VQ-VAE 的训练目标由三项损失构成：

$$
\mathcal{L}_{vqvae}^i = \mathcal{L}_{rec}^i + \mathcal{L}_{emb}^i + \mathcal{L}_{com}^i
$$

其中，**重建损失** $\mathcal{L}_{rec}^i$ 同时约束运动姿态及其速度的平滑 L1 损失，确保解码器能从离散 token 中准确重建原始运动：

$$
\mathcal{L}_{rec}^i = \mathcal{L}1(M_i - \hat{M}_i) + \alpha \mathcal{L}1(\mathcal{V}(M_i) - \mathcal{V}(\hat{M}_i))
$$

**嵌入损失** $\mathcal{L}_{emb}^i$ 推动码本向量向编码器输出靠拢（编码器输出停止梯度）：

$$
\mathcal{L}_{emb}^i = \Vert sg(Z_i) - \hat{Z}_i \Vert_2
$$

**承诺损失** $\mathcal{L}_{com}^i$ 则约束编码器输出不要偏离所选码本向量过远（码本向量停止梯度）：

$$
\mathcal{L}_{com}^i = \Vert Z_i - sg(\hat{Z}_i) \Vert_2
$$

该 VQ-VAE 在 LaViMo 与 AMASS 数据集的联合数据上预训练，为后续翻译模型提供稳定的离散运动表征。

### 文本分词与序列构建

文本侧的处理相对直接：经过 LLM 语义增强与启发式后处理过滤后的文本描述，直接利用 T5 骨干网络自带的文本嵌入表 $T$ 转换为文本 token 序列。对于第 $j$ 个原子动作，其运动 token 序列记为 $Z_{seg}^j = (z_1^j, z_2^j, \ldots, z_h^j)$（共 $h$ 个 token），对应的文本 token 序列记为 $T_{seg}^j = (t_1^j, t_2^j, \ldots, t_g^j)$（共 $g$ 个 token）。运动 token 与文本 token 被拼接为统一的联合序列，送入 T5 的 Transformer 编码器-解码器架构。

### T5 翻译骨干与多任务训练目标

T5 骨干网络接收带任务自适应掩码（task-adaptive masking）的联合 token 序列，其解码器以自回归方式预测被遮蔽的部分。TMT 设计了四个独特的监督或自监督任务来联合训练该翻译模块：

**Text2Text（自监督）**：随机遮蔽部分文本 token，要求模型基于未遮蔽的文本 token 预测被遮蔽部分。其损失为被遮蔽位置的标准交叉熵：

$$
L_{T2T}^j = -\sum_{p \in masked} \sum_{i=0}^{L-1} \log p(t_{p;i}^j | \{ t_{q \notin masked}^j \})
$$

**Text2Motion（核心生成任务）**：给定完整的文本 token 序列 $T_{seg}^j$、前一个原子动作的历史运动上下文 $\{ z_{p-k;k}^{j-1} \}$ 以及当前动作已生成的运动 token $\{ z_{r|r<s}^j \}$，自回归地预测当前原子动作的每个运动 token。其损失为：

$$
L_{T2M}^j = -\sum_{s=1}^{h} \sum_{i=0}^{B-1} \log p(z_{s;i}^j | \{ z_{p-k;k}^{j-1} \}, \{ z_{r|r<s}^j \}, T_{seg}^j)
$$

**Motion2Text（反向翻译任务）**：遮蔽所有文本 token，要求模型基于运动 token 序列 $Z_{seg}^j$ 和已预测的文本 token $\{ t_{r|r<s}^j \}$ 自回归地预测文本 token。这一任务赋予模型从运动生成语言描述的能力，同时强化了运动与文本之间的语义对齐：

$$
L_{M2T}^j = -\sum_{s=1}^{g} \sum_{i=0}^{L-1} \log p(t_{s;i}^j | \{ t_{r|r<s}^j \}, Z_{seg}^j)
$$

**Motion2Motion（自监督）**：类似于 Text2Text，对运动 token 序列进行随机遮蔽与预测，增强模型对运动序列内在动力学的建模能力。

这四个任务共享 T5 骨干网络的参数，通过多任务联合训练实现双向翻译能力与跨模态语义对齐的正则化。值得注意的是，该框架无需额外输入动作时长——运动 token 序列的长度自然编码了时序信息，模型通过自回归生成自行决定何时终止。

### 补充图表

![[assets/figures/papers/paper_list_l1880_Text_Motion_Translator_A_Bi_Directional_Model_for_Enhanced_3D_Human_Moti/figures/003_Figure_3.jpg]]
*Figure 3: 3D pose estimation pipeline overview: we balance the trade-off between performance and time spent by combining Hybrik Module and test-time optimization of HuMoR*



## 实验与关键发现

### 主实验结果

TMT 在两个主流基准 BABEL 和 HumanML3D 上均取得了领先性能，尤其在语义对齐与生成多样性方面表现突出。

**BABEL 数据集。** 如 Table 1 所示，TMT 在 R-Precision@3 上达到 0.53，FID 降至 0.72，Diversity 为 8.33，MultiModal-Dist 为 5.88。更重要的是，在 APE 与 AVE 指标上，TMT 平均比第二名方法 **EMS**（Qian et al., ICCV 2023）高出 33%（Table 3）。这表明模型不仅在整体分布匹配上占优，在逐样本的语义-运动对齐精度上也有显著优势。

**HumanML3D 数据集。** 如 Table 2 所示，TMT 的 R-Precision@3 为 0.528，FID 为 0.184，Diversity 为 9.437，MultiModal-Dist 为 3.091。与 BABEL 上的结果一致，TMT 在更规整的 HumanML3D 基准上同样保持了竞争力。

> 注：上述表格数据来自验证分析中的 Table 1–3，具体数值需对照原文确认。

![[assets/figures/papers/paper_list_l1880_Text_Motion_Translator_A_Bi_Directional_Model_for_Enhanced_3D_Human_Moti/figures/004_Table_1.jpg]]
*Table 1: Comparing ours against previous SOTAs on BABEL*

### 消融实验分析

消融实验（Table 4）系统拆解了各模块对已见动作（S）和未见动作（U）的贡献，揭示了三个关键因果路径：

**1. LLM 文本增强与后处理过滤的协同效应。** 使用 LLM（GPT-4）生成语义相似的增强描述，平均带来 17.3% 的性能提升。但若不加后处理过滤（即直接使用所有 LLM 生成描述），已见动作的生成质量会出现明显下降——LLM 可能引入身体部位不匹配、动静混淆等错误描述。启发式后处理规则（过滤部位不一致、静态/动态误判、方向错误等）是这一增益的必要条件：它既保留了 LLM 对开放词汇覆盖的扩展能力，又抑制了幻觉引入的噪声。

**2. 多任务训练的正则化效应。** 相比仅训练 Text2Motion 的单任务基线，多任务联合训练（Text2Motion + Motion2Text + Text2Text + Motion2Motion）为未见动作带来 13% 的提升，为已见动作带来 8% 的提升。Motion2Text 任务迫使模型学习从运动 token 重建文本语义，Text2Text 和 Motion2Motion 则分别强化了文本和运动模态的内部一致性——这些辅助任务共同构成了一个跨模态语义对齐的正则化器，尤其对训练集中未出现的动作描述泛化效果显著。

**3. 预训练数据的选择性影响。** 在 AMASS 上预训练对已见动作更有利，而在 LaViMo 上预训练对未见动作影响更大。这一现象符合直觉：AMASS 覆盖的动作类型与 BABEL/HumanML3D 的已见动作分布更接近，而 LaViMo 的大规模多样性（约 140k 运动片段，130 小时运动数据）为模型提供了更丰富的运动先验，使其在面对未见动作时具备更强的泛化基础。

### 定性分析与失败模式

定性比较（Figure 4）进一步佐证了定量结论：

![[assets/figures/papers/paper_list_l1880_Text_Motion_Translator_A_Bi_Directional_Model_for_Enhanced_3D_Human_Moti/figures/008_Figure_4.jpg]]
*Figure 4: Qualitative Results (a) Comparing between EMS and our Model. (b) Comparing between models trained with LLM augmentation (w LLM) and without LLM augmentation (w/o LLM). (c)Comparing between models trained with LLM augmentation with post-processing (w PP) and without post-processing (w/o PP)*

- **与 EMS 的对比（Figure 4a）：** TMT 生成的运功在语义一致性和自然度上均优于 EMS，尤其对于复合动作描述（如“边走边挥手”），TMT 的动作过渡更连贯。
- **LLM 增强的消融（Figure 4b）：** 去掉 LLM 增强后，模型对开放词汇描述（如“像企鹅一样摇摆行走”）的生成质量明显下降，表现为动作语义丢失或姿态僵硬。
- **后处理的消融（Figure 4c）：** 去掉后处理过滤后，部分生成动作出现不自然的肢体扭曲或节奏异常，印证了 LLM 增强文本中噪声对运动生成的直接干扰。

**已知局限与失败模式：**
1. **超出分布的动作描述泛化不足：** 对于预训练数据中完全未覆盖的动作类型（如极端体育技巧或罕见舞蹈），模型仍难以生成合理运动。这是离散 token 表示与有限码本容量的固有瓶颈。
2. **LaViMo 数据噪声的传导：** LaViMo 基于 RGB 视频的 3D 姿态估计（HybrIK + HuMoR 优化）虽将处理时间从 >5 分钟压缩至约 30 秒/片段，但估计结果仍可能包含关节抖动、遮挡导致的姿态错误，这些噪声通过 VQ-VAE 训练传导至运动 token 的码本质量。
3. **LLM 增强的语义偏差：** 尽管后处理过滤了大部分不合理描述，LLM 本身可能对特定动作类别存在系统性偏见（如过度简化复杂动作），导致增强文本的多样性在部分类别上不足。
4. **评估指标的感知差距：** FID 和 R-Precision 等指标主要衡量分布匹配和检索准确率，可能无法完全反映人类对运动自然度、物理合理性及细粒度语义对齐的感知判断。

### 重要图表结论

- **Figure 1：** 展示了 TMT 的双向生成能力——从文本生成运动（Text2Motion），再从生成的运动反向输出文本描述（Motion2Text），验证了翻译框架的语义闭环特性。
- **Figure 2：** 模型结构概览，明确了两阶段训练流程：Motion VQ-VAE 在 LaViMo + AMASS 上预训练以构建离散运动码本，随后在多任务框架下训练 T5 翻译骨干。
- **Figure 3：** 3D 姿态估计流水线，通过 HybrIK 初始化 + HuMoR 测试时优化的组合，在估计精度与处理时间之间取得平衡，是 LaViMo 数据集构建的关键工程基础。
- **Table 3：** APE/AVE 指标的核心对比表，TMT 比第二名 EMS 平均优 33%，是全文最决定性的定量证据。
- **Table 4：** 消融实验的完整矩阵，清晰展示了预训练数据选择、LLM 增强、后处理过滤及多任务训练各自对已见/未见动作的量化贡献。

![[assets/figures/papers/paper_list_l1880_Text_Motion_Translator_A_Bi_Directional_Model_for_Enhanced_3D_Human_Moti/figures/006_Table_3.jpg]]
*Table 3: Comparing ours against previous SOTAs on BABEL dataset under APE & AVE metrics. PP represents post-processing*

### 补充图表

![[assets/figures/papers/paper_list_l1880_Text_Motion_Translator_A_Bi_Directional_Model_for_Enhanced_3D_Human_Moti/figures/005_Table_2.jpg]]
*Table 2: Comparing ours against previous SOTAs on HumanML3D*

![[assets/figures/papers/paper_list_l1880_Text_Motion_Translator_A_Bi_Directional_Model_for_Enhanced_3D_Human_Moti/figures/007_Table.jpg]]



## 定位与知识库关联

### 1. 技术路线与关键差异

TMT 将文本条件 3D 人体运动生成重新定义为**语言翻译问题**，这与现有主流方法存在根本性范式差异。具体而言，现有方法可归为以下几类，TMT 在每一维度上均做出了不同的设计选择：

**（1）运动表示方式**

传统方法多采用连续潜在向量（如条件 VAE）或原始关节位置表示运动。例如 **EMS**（Qian et al., ICCV 2023）等 SOTA 方法通常依赖连续潜在空间进行运动生成。TMT 则引入 **Motion VQ-VAE**，将 3D 人体运动编码为离散 token 序列，并通过共享码本实现运动与文本的统一离散表示。这一设计使得运动生成可以复用语言模型中成熟的序列到序列架构。

**（2）文本条件机制**

现有方法通常直接使用数据集中原始的简短文本描述作为条件输入。TMT 则构建了 **LLM 语义增强流水线**：利用 GPT-4 为原子动作描述生成语义相似的变体描述，再通过启发式规则过滤身体部位不一致、动静混淆等不合理生成结果。消融实验表明，LLM 增强配合后处理过滤带来平均 **17.3%** 的性能提升；若不进行后处理，已见动作质量下降，但仍有助于未见动作的泛化。

**（3）训练范式**

主流方法通常采用**单任务训练**（仅 Text2Motion），且多数模型需要额外输入动作时长参数。TMT 采用**多任务联合学习**框架，同时训练 Text2Motion、Motion2Text、Text2Text 和 Motion2Motion 四个任务，且**无需独立时长输入**。消融实验证实，多任务训练相比单任务训练，在未见动作上提升 **13%**，在已见动作上提升 **8%**。

**（4）数据规模与来源**

现有方法多基于 AMASS 等动作捕捉数据集进行训练，数据规模有限。TMT 构建了 **LaViMo 大规模伪标签运动数据集**，包含约 14 万个运动片段（约 130 小时运动数据），规模约为现有数据集的 4 倍。该数据集通过 HybrIK + HuMoR 的混合 3D 姿态估计流水线从互联网 RGB 视频中提取，将单段 2 秒视频的处理时间从 5 分钟以上压缩至约 30 秒。

### 2. 适用边界与局限

尽管 TMT 在多个基准上取得了显著提升，其适用边界和局限同样明确：

**（1）数据依赖与泛化边界**

TMT 的性能高度依赖于预训练数据的覆盖范围。对于超出 LaViMo 和 AMASS 数据集分布的全新动作描述，模型仍面临挑战。论文明确指出，与文本条件图像/视频生成等成熟领域相比，运动生成的鲁棒性和泛化性仍有较大差距。消融实验揭示了预训练数据选择的分化效应：在 AMASS 上预训练对已见动作更有利，而在 LaViMo 上预训练对未见动作影响更大——这表明当前方案尚未实现两类收益的统一。

**（2）LLM 增强的质量风险**

LLM 文本增强的质量依赖于 GPT-4 的生成能力和启发式规则的准确性。论文承认，LLM 可能引入语言模型本身的偏见或幻觉，尤其在不常见动作描述上。启发式过滤规则的具体设计及其各自对生成质量的量化贡献尚不明确，存在过滤不足或过度过滤的风险。

**（3）伪标签噪声传播**

LaViMo 数据集虽大幅增加了数据量，但其 3D 姿态源自 RGB 视频估计，可能包含不可预见的姿态估计噪声和动作分布偏差。这些噪声通过 Motion VQ-VAE 的训练过程可能传播至下游生成任务，影响运动重建质量和生成自然度。

**（4）评估指标的局限性**

论文采用的 FID、R-Precision、Diversity、MultiModal-Dist 等指标可能无法完全反映人类感知的运动自然度与语义准确性。尤其在开放词汇场景下，文本与运动之间的细粒度语义对齐尚未有成熟的自动评估方案。

### 3. 开放问题

以下问题在论文中未被充分回答，构成该方向的后续研究空间：

1.  **多任务正则化的作用机制**：多任务训练（Text2Motion、Motion2Text 等）具体如何提升文本-运动语义对齐？是否可以通过额外的对比学习或显式语义对齐损失进一步增强跨模态理解？
2.  **LLM 增强的精细控制**：启发式过滤规则中，身体部位一致性检查、动静状态判断、方向约束等各自对生成质量的量化贡献有多大？能否训练自动评分模型替代人工设计的规则？
3.  **全新动作的鲁棒泛化**：如何进一步提高模型对预训练数据集之外全新动作描述的鲁棒性？是否需要引入持续学习机制或外部知识库（如动作知识图谱）？
4.  **数据规模与码本表达力的关系**：扩大预训练数据规模和多样性（如利用海量 RGB 视频）能在多大程度上提升 Motion VQ-VAE 的码本表达能力与泛化性？是否存在码本容量饱和点？
5.  **双向生成的评估体系**：Motion2Text 方向目前缺乏系统的定量评估标准，如何建立运动到文本生成质量的可靠自动度量？



## 原文 PDF

![[paperPDFs/ECCV_2024/Text_Motion_Translator_A_Bi_Directional_Model_for_Enhanced_3D_Human_Motion_Generation_from_Open_Vocabulary_Descriptions.pdf]]
