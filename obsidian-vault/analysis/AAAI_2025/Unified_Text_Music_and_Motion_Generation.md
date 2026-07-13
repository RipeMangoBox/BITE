---
title: Unified Text Music and Motion Generation
type: paper
paper_level: A
venue: AAAI
year: 2025
pdf_ref: paperPDFs/AAAI_2025/Unified_Text_Music_and_Motion_Generation.pdf
project_link: https://hanyangclarence.github.io/unimumo
code_link: https://github.com/mubertai/
aliases:
- UTMMG
tags:
- AAAI_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
core_operator: 将运动序列通过冻结的音乐 VQ-VAE 码本映射到音乐特征空间的联合编码方案，以及音乐-运动并行生成的自回归训练策略。
primary_logic: 利用预训练的音乐生成模型和共享码本，可以在文本条件下同时生成节奏对齐的音乐和动作序列，并且无需为每个任务单独训练模型。
claims:
- 音乐-运动对齐后平均 L1 距离从 6.34 降至 1.78，显著提升节奏同步性。
- 在 MusicCaps 文本到音乐的任务中，UniMuMo 取得 5.93 FADvGG，与微调后的 MusicGen（5.81）相当，并优于其他多数基线。
- 在运动到音乐的任务上，节拍覆盖率和命中率达到 93.0/88.4，接近最优模型 CDCD（93.9/90.7）。
- 用户研究显示，对齐后的视频评分（3.95）明显高于随机配对（3.26），主观感知上验证了对齐有效性。
---

# Unified Text Music and Motion Generation

> [!tip] 核心洞察
> 利用预训练的音乐生成模型和共享码本，可以在文本条件下同时生成节奏对齐的音乐和动作序列，并且无需为每个任务单独训练模型。

| 字段 | 内容 |
|------|------|
| 中文题名 | 统一文本、音乐和动作生成 |
| 英文题名 | Unified Text Music and Motion Generation |
| 会议/期刊 | AAAI 2025 |
| Links | [Project](https://hanyangclarence.github.io/unimumo) · [Code](https://github.com/mubertai/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation |
| Method | UniMuMo |
| Dataset | MusicCaps, AIST++, MusicQA, HumanML3D |

> [!tip] 效果简介
> - MusicCaps 上，FADvGG↓ 5.93 vs 5.81 (MusicGen fine-tuned on our data) (-0.12 (comparable))。
> - AIST++ 上，Beats Coverage↑ 93.0 vs 93.9 (CDCD) (-0.9)。
> - AIST++ (dance) 上，Beat Align↑ 0.24 vs 0.27 (EDGE) (-0.03)。

## 概要

### 问题与瓶颈

跨模态生成领域长期面临一个根本性瓶颈：**缺乏同时包含音乐、动作和文本的成对多模态数据**。现有数据集往往是两两配对的（如音乐-动作、文本-音乐），而设计一个能够统一处理这三种模态生成任务的模型架构本身也极具挑战性——不同模态在表示空间、时间分辨率和语义粒度上存在显著差异。

### 核心思路

UniMuMo 的核心洞察在于：**利用预训练的音乐生成模型和共享码本，可以在文本条件下同时生成节奏对齐的音乐和动作序列，而无需为每个任务单独训练模型**。具体而言，该方法通过将运动序列映射到冻结的音乐 VQ-VAE 码本空间，实现了音乐与运动在统一特征空间中的联合编码；在此基础上，采用音乐-运动并行生成的自回归训练策略，使单一 Transformer 解码器能够同时预测两种模态的 token。

### 方法定位

UniMuMo 在方法谱系中处于**统一多模态生成框架**的交汇点。与 MusicGen（文本到音乐）、EDGE（音乐到动作）、CDCD（动作到音乐）等单向任务专用模型不同，UniMuMo 通过以下关键设计实现了多任务的统一：

- **共享码本编码**：将运动编码到冻结的 EnCodec RVQ 空间，替代独立的运动 VQ-VAE 码本；
- **并行生成方案**：音乐和运动 token 在交叉模态因果注意力下同步自回归生成；
- **模态特定组件**：引入独立的运动 token 嵌入层和额外的运动 FFN（类 MoE 结构）；
- **联合训练目标**：以加权损失（μ=0.85）同时优化音乐和运动的下一 token 预测。

### 主要结果概要

在多项基准测试上，UniMuMo 取得了与各领域最优方法相当甚至更优的性能：

- **文本到音乐**（MusicCaps）：FADvGG 达 5.93，与微调后的 MusicGen（5.81）持平，优于多数基线；
- **动作到音乐**（AIST++）：节拍覆盖率 93.0、命中率 88.4，接近最优模型 CDCD（93.9/90.7）；
- **音乐到舞蹈**（AIST++）：Beat Align 为 0.24，与 EDGE（0.27）接近；
- **音乐字幕**（MusicQA）：BLEU 达 0.261，超越 LTU（0.238）；
- **动作字幕**（HumanML3D）：R-Precision Top1 为 0.520，与 MotionGPT（0.534）相当。

消融实验进一步验证了共享码本编码、模态特定组件和预训练初始化的关键作用，而用户研究（对齐评分 3.95 vs 随机 3.26）则从主观感知层面确认了音乐-动作对齐的有效性。

### 局限与开放问题

尽管性能表现强劲，该方法仍存在若干局限：生成音乐的音频质量受限于去人声训练数据的伪影；合成文本描述缺乏特异性；音乐-动作对齐高度依赖节拍检测精度，对无清晰节奏的音乐可能失效。开放问题包括如何构建大规模高质量三模态数据集、如何将联合码本方法扩展到歌词或视频等更多模态，以及多任务训练方案为何不如联合生成任务等。



音乐、运动（舞蹈）和文本是人类表达与交流的三种核心模态。三者之间存在天然的语义耦合——一段音乐往往对应特定的舞蹈风格，而一段舞蹈又可以用自然语言描述。然而，构建能够在这三种模态之间自由转换的生成系统，面临着两个根本性瓶颈：

**数据瓶颈**：现有的大规模多模态数据集通常只覆盖两两模态配对，例如音频-文本对（如 MusicCaps）或音乐-舞蹈对（如 AIST++），缺乏同时包含音乐、动作和文本的成对数据。这迫使研究者要么依赖昂贵的人工标注，要么在模态缺失的条件下训练模型。

**架构瓶颈**：音乐（时序音频信号）、运动（骨骼关节序列）和文本（离散 token）在表示空间上差异巨大。现有方法通常为每个单向任务设计独立模型——例如 MusicGen 处理文本到音乐，EDGE 处理音乐到动作，CDCD 处理动作到音乐——这不仅导致模型碎片化，更无法利用模态间的互补信息进行联合学习。

UniMuMo 的核心动机正是突破上述双重瓶颈：**在无需成对多模态数据的前提下，构建一个统一的框架，能够处理文本、音乐和动作之间的任意生成任务**。其关键洞察在于，音乐的节拍结构与舞蹈的视觉节拍之间存在天然的节奏对应关系——这一对应关系可以被自动提取并用于对齐未配对的音乐和动作数据，从而在不依赖人工标注的情况下构建大规模对齐数据集。在此基础上，通过将运动序列映射到预训练音乐模型的共享码本空间，UniMuMo 实现了三种模态在统一特征空间中的联合建模，为跨模态生成提供了架构基础。



## 核心方法与创新机理

UniMuMo 的核心创新围绕一个根本瓶颈展开：**缺乏同时包含音乐、动作和文本的成对多模态数据**，以及如何设计一个能够统一处理这三种模态生成任务的模型架构。针对这一瓶颈，工作从数据构造、表示对齐和生成范式三个层面提出了系统性创新。

### 1. 基于节拍对齐的跨模态数据构造

音乐和动作数据通常以非配对形式存在。UniMuMo 提出了一种基于节拍对齐的数据流水线，将非配对的音乐和动作序列在时间维度上建立对应关系。

- **音乐节拍检测**：使用基于双向 LSTM 的模型从音频波形中提取音乐节拍位置。
- **视觉节拍检测**：将运动序列转换为运动直方图（directogram），再利用动态规划在运动学冲击强度和节拍等间距之间求最优解，定位视觉节拍。运动直方图的计算公式为：

$$M_d(t, \theta) = \sum_i \Delta M_t(j) \mathbf{1}_\theta(\angle M_t(j))$$

- **音乐-动作对齐**：在提取的节拍序列上应用动态时间规整（Dynamic Time Warping），寻找音乐与动作之间的最优时间对齐路径。实验表明，对齐后平均 L1 距离从 **6.34 降至 1.78**，节奏同步性显著提升（Section 5.1，置信度 0.95）。用户研究进一步验证了对齐的主观效果：对齐视频的平均评分为 **3.95**，显著高于随机配对的 **3.26**（Appendix E，置信度 0.95）。

- **文本描述合成**：利用模板填充、大语言模型生成和基于音乐的语言模型生成三种方式，从音乐和动作的元数据中构造文本描述，为后续文本条件生成提供监督信号。

### 2. 共享码本：将运动映射到音乐特征空间

这是 UniMuMo 最具标志性的设计决策。传统方法为每种模态训练独立的 VQ-VAE 和码本，导致模态间语义鸿沟。UniMuMo 提出：

- **冻结预训练的音乐 RVQ-VAE 码本**（基于 EnCodec），然后训练一个运动编码器-解码器，将运动序列编码到与音乐相同的嵌入空间，并复用该冻结的残差向量量化器（RVQ）将运动离散化为 token。
- 训练目标为运动重建损失与码本承诺损失的加权和：

$$\mathcal{L}_{\mathrm{total}} = \frac{1}{|\mathcal{D}|} \sum_{M \in \mathcal{D}} \left( \| M - \hat{M} \|_2 + \lambda \mathcal{L}_{\mathrm{commit}} \right)$$

消融实验（Table 6, Ablation 1-2）表明，使用独立的运动 VQ-VAE 编码会导致音乐生成 FADvGG 升高、运动生成质量下降，直接证明了共享码本编码的有效性（置信度 0.9）。

### 3. 音乐-运动并行生成的自回归范式

UniMuMo 以预训练的文本到音乐模型 **MusicGen** 为基础，将其改造为支持音乐和运动并行生成的统一 Transformer 解码器。

- **输入构造**：音乐 token 和运动 token 在时间维度上交错拼接，形成跨模态的因果注意力掩码，使得每个时间步的音乐 token 可以关注到当前及之前的运动 token，反之亦然。
- **联合训练损失**：采用加权预测下一个 token 损失，平衡音乐和运动两个模态：

$$\mathcal{L} = -\frac{1}{|\mathcal{D}|} \sum_{Q \in \mathcal{D}} \{ \mu \cdot \sum_{t=1}^{S} \log \mathbb{P}[Q_t^{\mathrm{music}} | Q_{<t}^{\mathrm{music}}, Q_{<t}^{\mathrm{motion}}] + (1-\mu) \cdot \sum_{t=1}^{S} \log \mathbb{P}[Q_t^{\mathrm{motion}} | Q_{<t}^{\mathrm{music}}, Q_{<t}^{\mathrm{motion}}] \}$$

其中 $\mu=0.85$，给予音乐生成稍高的权重。

- **并行采样**：推理时，在每个时间步同时预测下一个音乐 token 和运动 token，实现音乐与动作的同步生成：

$$\hat{Q}_t^{\mathrm{music}} = \underset{i \in \mathcal{M}}{\mathrm{argmax}} \mathbb{P}[Q_{t,i}^{\mathrm{music}} | \hat{Q}_{<t}^{\mathrm{music}}, \hat{Q}_{<t}^{\mathrm{motion}}]$$

$$\hat{Q}_t^{\mathrm{motion}} = \underset{i \in \mathcal{M}}{\mathrm{argmax}} \mathbb{P}[Q_{t,i}^{\mathrm{motion}} | \hat{Q}_{<t}^{\mathrm{music}}, \hat{Q}_{<t}^{\mathrm{motion}}]$$

这种并行生成方案使单一模型能够同时输出节奏对齐的音乐和动作序列，无需为每个任务单独训练模型。值得注意的是，消融实验（Table 6, Ablation 4）显示，采用多任务训练（分别训练音乐-运动生成、音乐到运动、运动到音乐）替代联合生成会导致性能下降，可能源于梯度冲突和任务难度差异（置信度 0.9）。

### 4. 模态特定组件的引入

在共享 Transformer 主干的基础上，UniMuMo 引入了模态特定的组件以处理音乐和运动的表示差异：

- **独立的运动 token 嵌入层**：与音乐 token 嵌入层分离，使模型能够学习运动 token 的专属表示。
- **额外的运动前馈网络（MoE 式 FFN）**：在 Transformer 层中为运动 token 增加一个独立的前馈网络，形成类似混合专家（MoE）的结构。
- **分离的位置编码**：音乐和运动使用各自的位置编码。

消融实验（Table 6, Ablation 3）表明，移除这些模态特定组件会使运动生成性能大幅下降，验证了它们在多模态融合中的关键作用（置信度 0.9）。

### 5. 统一的零样本跨模态生成能力

得益于共享码本和并行生成方案，UniMuMo 天然支持多种零样本跨模态生成任务。例如，在运动到音乐的任务中，模型自回归地根据给定运动序列生成对齐的音乐 token：

$$\hat{Q}_t^{\mathrm{motion}} = \underset{i \in \mathcal{M}}{\arg\max} \mathbb{P}[Q_{t,i}^{\mathrm{motion}} | Q_{<t}^{\mathrm{music}}, \hat{Q}_{<t}^{\mathrm{motion}}]$$

这种设计使 UniMuMo 成为首个能够**在文本、音乐和动作之间任意方向生成**的统一框架，覆盖文本到对齐音乐-动作、音乐到动作、动作到音乐、音乐字幕和动作字幕等全部任务。

### 创新总结：changed slots 一览

| 设计槽位 | 基线方案 | UniMuMo 方案 | 证据强度 |
|---------|---------|-------------|---------|
| 运动 token 化 | 独立运动 VQ-VAE，单独码本 | 冻结音乐 RVQ 码本，运动编码到同一空间 | Table 6 Ablation 1-2，置信度 0.95 |
| 生成范式 | 各任务独立模型（MusicGen、EDGE 等） | 单一 Transformer 解码器，音乐-运动并行生成 | Section 4.2，置信度 0.95 |
| 模态特定组件 | 共享嵌入和单一 FFN（MusicGen） | 独立运动嵌入、额外运动 FFN、分离位置编码 | Table 6 Ablation 3，置信度 0.9 |
| 训练目标 | 单模态预测下一个 token | 加权联合预测下一个 token（μ=0.85），支持零样本任务 | Equation 2，置信度 0.95 |



UniMuMo 的整体框架围绕一个核心瓶颈展开：**缺乏同时包含音乐、动作和文本的成对多模态数据**，以及**设计能够统一处理这三种模态生成任务的模型架构**。为解决这一问题，论文构建了一条“数据构造—联合编码—并行生成—跨模态理解”的完整流水线，如图 Figure 2 所示。

![[assets/figures/papers/paper_list_l1825_Unified_Text_Music_and_Motion_Generation/figures/002_Figure_2.jpg]]
*Figure 2: Overview: The training of UniMuMo consists of three stages: In stage 1, we train a motion RVQ-VAE using the frozen codebook from a pre-trained music RVQ-VAE to encode motion into the same space as music. In stage 2, we fine-tune a pre-trained music transformer decoder model on the text-to-music-motion task using the music-motion parallel generation scheme. In stage 3, we fine-tune a T5 decoder for music-motion captioning using the previous music-motion decoder as a feature extractor*

### 数据构造流水线

在模型训练之前，系统首先通过四个步骤将非配对音乐与动作数据转化为对齐的“文本-音乐-动作”三元组：

1. **音乐节拍检测**：使用基于双向 LSTM 的模型从音乐波形中提取节拍时间点。
2. **视觉节拍检测**：通过运动直方图（directogram）和动态规划算法，从动作序列中计算视觉节拍。运动直方图定义为：
   $$M_d(t, \theta) = \sum_i \Delta M_t(j) \mathbf{1}_\theta(\angle M_t(j))$$
   该公式将每一帧的运动幅度按运动角度分配到各个方向 bin 中，以刻画动作的视觉节奏特征。
3. **音乐-动作对齐**：在提取的节拍序列上应用动态时间规整（DTW），将非配对的音乐和动作按节奏模式对齐。对齐后，平均 L1 距离从 6.34 降至 1.78，显著提升了节奏同步性（Section 5.1）。
4. **文本描述合成**：利用模板填充、大语言模型生成和基于音乐的语言模型生成三种方式，从音乐和动作的元数据中构造文本描述（详见 Table 7–10）。

### 三阶段训练架构

UniMuMo 的训练分为三个递进阶段，对应 Figure 2 中 Stage 1–3：

**Stage 1：运动 RVQ-VAE 与共享码本**  
核心创新在于将运动序列映射到音乐的特征空间。具体而言，冻结预训练的音乐 RVQ-VAE（基于 EnCodec）的码本，训练一个运动编码器-解码器，使其复用相同的残差向量量化器（RVQ）将运动离散化为 token。训练损失为运动重建损失与码本承诺损失的加权和：
$$\mathcal{L}_{\mathrm{total}} = \frac{1}{|\mathcal{D}|} \sum_{M \in \mathcal{D}} \left( \| M - \hat{M} \|_2 + \lambda \mathcal{L}_{\mathrm{commit}} \right)$$
这使得音乐和运动 token 处于同一特征空间，为后续统一生成奠定基础。

**Stage 2：音乐-运动并行生成**  
以预训练的文本到音乐模型 MusicGen 为基础，将其改造为音乐-运动联合生成的 Transformer 解码器。关键设计包括：
- **并行生成方案**：音乐 token 和运动 token 在时间维度上交错拼接，通过交叉模态因果注意力（cross-modal causal attention）同时预测下一步的音乐 token 和运动 token。
- **模态特定组件**：为运动引入独立的 token 嵌入层和额外的 FFN（类似 MoE 结构），与音乐的嵌入和 FFN 分离，以处理模态差异。
- **加权训练损失**：联合预测下一个 token 的损失以权重 μ=0.85 偏向音乐生成：
  $$\mathcal{L} = -\frac{1}{|\mathcal{D}|} \sum_{Q \in \mathcal{D}} \{ \mu \cdot \sum_{t=1}^{S} \log \mathbb{P}[Q_t^{\mathrm{music}} | Q_{<t}^{\mathrm{music}}, Q_{<t}^{\mathrm{motion}}] + (1-\mu) \cdot \sum_{t=1}^{S} \log \mathbb{P}[Q_t^{\mathrm{motion}} | Q_{<t}^{\mathrm{music}}, Q_{<t}^{\mathrm{motion}}] \}$$
推理时，并行采样公式为：
$$\hat{Q}_t^{\mathrm{music}} = \underset{i \in \mathcal{M}}{\mathrm{argmax}} \mathbb{P}[Q_{t,i}^{\mathrm{music}} | \hat{Q}_{<t}^{\mathrm{music}}, \hat{Q}_{<t}^{\mathrm{motion}}]$$
$$\hat{Q}_t^{\mathrm{motion}} = \underset{i \in \mathcal{M}}{\mathrm{argmax}} \mathbb{P}[Q_{t,i}^{\mathrm{motion}} | \hat{Q}_{<t}^{\mathrm{music}}, \hat{Q}_{<t}^{\mathrm{motion}}]$$
该阶段还支持零样本任务，如仅给定音乐序列自回归生成对齐运动：
$$\hat{Q}_t^{\mathrm{motion}} = \underset{i \in \mathcal{M}}{\arg\max} \mathbb{P}[Q_{t,i}^{\mathrm{motion}} | Q_{<t}^{\mathrm{music}}, \hat{Q}_{<t}^{\mathrm{motion}}]$$

**Stage 3：音乐-运动描述生成**  
在 Stage 2 训练好的解码器之上，引入可训练的全自注意力模块（初始化为交叉模态因果注意力模块的权重），并连接一个 T5 解码器。仅微调新增的全自注意力模块和 T5 解码器，其余音乐-运动解码器部分保持冻结。该阶段赋予模型音乐描述和动作描述能力。

### 输入输出流

- **输入**：文本描述（由数据合成流水线生成或用户提供）、音乐波形、运动序列中的任意组合。
- **输出**：根据任务类型，可生成对齐的音乐和运动（文本到对齐音乐-运动）、仅运动（音乐到运动）、仅音乐（运动到音乐）、音乐描述或运动描述。
- **关键因果机制**：共享码本将异构模态统一到同一离散空间，并行生成方案利用交叉注意力在每一步显式建模音乐与运动的相互依赖，从而实现节奏对齐的联合生成，而无需为每个单向任务单独训练模型。

消融实验证实，共享码本和运动专用 FFN 等组件对生成质量至关重要（Table 6），而多任务训练替代联合生成方案会导致性能下降，可能源于梯度冲突和任务难度差异。

### 补充图表

![[assets/figures/papers/paper_list_l1825_Unified_Text_Music_and_Motion_Generation/figures/001_Figure_1.jpg]]
*Figure 1: UniMuMo is able to perform generation tasks on any combination of music, motion, and text. The tasks shown in the figure include text-to-aligned-music-motion, music-to-motion, motion-to-music, music-captioning, and motion-captioning*



UniMuMo 的训练分为三个顺序阶段，每个阶段引入一组关键模块，共同支撑统一的文本-音乐-动作生成框架。以下按数据对齐、联合编码、并行生成和跨模态描述的顺序，提取核心模块及其控制公式。

### 音乐-动作节拍对齐模块

由于不存在成对的音乐-动作-文本数据，UniMuMo 首先构建对齐的音乐-动作对。该流程包含四个子模块：

- **音乐节拍检测**：使用基于双向 LSTM 的模型从音频波形中提取音乐节拍位置。
- **视觉节拍检测**：从动作序列中计算视觉节拍。核心操作为运动直方图（directogram），将每一帧的运动幅度按运动角度分配到各角度 bin 中：

$$
M_d(t, \theta) = \sum_i \Delta M_t(j) \mathbf{1}_\theta(\angle M_t(j))
$$

其中 $\Delta M_t(j)$ 表示关节 $j$ 在时间 $t$ 的运动幅度，$\angle M_t(j)$ 为运动方向角度，$\mathbf{1}_\theta$ 为指示函数。随后通过动态规划在直方图序列上求解视觉节拍，目标函数为：

$$
V(\mathbf{m}) = \sum_{j=1}^{n} u(m_j) + \alpha \sum_{j=1}^{n-1} V_T(m_j, m_{j+1})
$$

其中 $u(m_j)$ 衡量运动学冲击强度，$V_T$ 惩罚节拍间距的不均匀性，$\alpha$ 为平衡系数。

- **音乐-动作对齐**：在提取的音乐节拍序列和视觉节拍序列上应用动态时间规整（DTW），将非成对的音乐和动作片段在节奏维度上对齐。对齐后平均 L1 距离从 6.34 降至 1.78，验证了节拍级对齐的有效性。

- **文本描述合成**：从音乐和动作的元数据出发，通过模板填充、大语言模型生成和基于音乐的语言模型生成三种方式混合构造文本描述，为后续条件生成提供监督信号。

### 阶段一：共享码本的动作 RVQ-VAE

该阶段的核心目标是将动作序列映射到与音乐相同的离散特征空间。具体而言，冻结预训练的音频分词器 EnCodec 的残差向量量化器（RVQ）码本，训练一个动作编码器-解码器，使其复用同一套码本。

- **动作编码器**将动作序列编码为与音乐嵌入同维度的连续表示。
- **冻结的音乐 RVQ** 将该连续表示量化为离散 token 序列。
- **动作解码器**从这些 token 重建原始动作。

训练损失为重建误差与码本承诺损失的加权和：

$$
\mathcal{L}_{\mathrm{total}} = \frac{1}{|\mathcal{D}|} \sum_{M \in \mathcal{D}} \left( \| M - \hat{M} \|_2 + \lambda \mathcal{L}_{\mathrm{commit}} \right)
$$

其中 $M$ 为原始动作序列，$\hat{M}$ 为重建动作，$\mathcal{L}_{\mathrm{commit}}$ 约束编码器输出靠近码本向量，$\lambda$ 为权重系数。该设计使音乐和动作在 token 层面共享同一语义空间，是后续统一生成的基础。

### 阶段二：音乐-动作并行生成 Transformer

阶段二以预训练的文本到音乐模型 MusicGen 为基础，将其改造为同时生成音乐和动作 token 的 Transformer 解码器。关键模块包括：

- **双模态嵌入与位置编码**：在原有音乐 token 嵌入的基础上，增加一个独立的可训练动作 token 嵌入层，并为音乐和动作分别设置位置编码。
- **MoE 式前馈网络**：为动作分支引入额外的 FFN 模块，与音乐分支的 FFN 构成类混合专家（MoE）结构，使不同模态在共享注意力的同时保留模态特化处理能力。
- **跨模态因果注意力**：音乐和动作 token 在时间维度上交错排列（遵循 MusicGen 的延迟模式），注意力掩码允许每个位置的 token 关注所有模态的历史 token，实现跨模态信息融合。

训练目标为音乐和动作的联合预测下一个 token 损失，通过加权系数 $\mu = 0.85$ 平衡两模态：

$$
\mathcal{L} = -\frac{1}{|\mathcal{D}|} \sum_{Q \in \mathcal{D}} \{ \mu \cdot \sum_{t=1}^{S} \log \mathbb{P}[Q_t^{\mathrm{music}} | Q_{<t}^{\mathrm{music}}, Q_{<t}^{\mathrm{motion}}] + (1-\mu) \cdot \sum_{t=1}^{S} \log \mathbb{P}[Q_t^{\mathrm{motion}} | Q_{<t}^{\mathrm{music}}, Q_{<t}^{\mathrm{motion}}] \}
$$

其中 $Q_t^{\mathrm{music}}$ 和 $Q_t^{\mathrm{motion}}$ 分别为第 $t$ 步的音乐和动作 token，$S$ 为序列长度，条件部分包含两模态的历史 token。

推理时采用**并行采样**策略，在每个时间步同时预测音乐和动作 token：

$$
\hat{Q}_t^{\mathrm{music}} = \underset{i \in \mathcal{M}}{\mathrm{argmax}} \mathbb{P}[Q_{t,i}^{\mathrm{music}} | \hat{Q}_{<t}^{\mathrm{music}}, \hat{Q}_{<t}^{\mathrm{motion}}]
$$

$$
\hat{Q}_t^{\mathrm{motion}} = \underset{i \in \mathcal{M}}{\mathrm{argmax}} \mathbb{P}[Q_{t,i}^{\mathrm{motion}} | \hat{Q}_{<t}^{\mathrm{music}}, \hat{Q}_{<t}^{\mathrm{motion}}]
$$

该方案使模型能从文本同时生成节奏对齐的音乐和动作，无需分别推理。消融实验（Table 6）表明，移除动作专用嵌入和 MoE FFN（消融 3）会导致动作生成质量大幅下降，验证了模态特定组件的必要性。

### 零样本跨模态生成

利用并行生成框架，UniMuMo 可零样本执行音乐到动作和动作到音乐任务。以运动到音乐为例，给定运动序列的 token $Q^{\mathrm{motion}}$，自回归地生成音乐 token：

$$
\hat{Q}_t^{\mathrm{motion}} = \underset{i \in \mathcal{M}}{\arg\max} \mathbb{P}[Q_{t,i}^{\mathrm{motion}} | Q_{<t}^{\mathrm{music}}, \hat{Q}_{<t}^{\mathrm{motion}}]
$$

此时音乐序列完全由模型生成，运动序列作为条件输入。该能力源于共享码本和跨模态注意力在训练阶段已隐式学习了两模态的对齐关系。

### 阶段三：音乐-动作描述生成器

阶段三在冻结的音乐-动作解码器之上，引入可训练的**全自注意力模块**和 T5 解码器，用于生成音乐或动作的文本描述。全自注意力模块由阶段二的跨模态因果注意力初始化，使模型能双向聚合音乐和动作特征。训练时仅更新新增的全自注意力层和 T5 解码器，保持底层特征提取器不变，从而在保护已学到的跨模态表示的同时获得描述生成能力。

### 补充图表

![[assets/figures/papers/paper_list_l1825_Unified_Text_Music_and_Motion_Generation/figures/012_Figure_3.jpg]]
*Figure 3: Illustrations on the technical details in our training process*

![[assets/figures/papers/paper_list_l1825_Unified_Text_Music_and_Motion_Generation/figures/013_Figure_4.jpg]]
*Figure 4: Illustrations on the technical details in the inference process*



## 实验与关键发现

### 核心实验结果

UniMuMo 在五个单向生成任务上进行了系统评估，涵盖文本到音乐、动作到音乐、音乐到动作、音乐字幕和动作字幕。所有对比方法的指标均从原始论文引用或在相同测试集上使用官方脚本重新评估，以保证公平性。

**文本到音乐生成。** 在 MusicCaps 基准上，UniMuMo（300M 参数）取得 FADvGG 5.93，与在其数据上微调后的 **MusicGen**（5.81）相当，并显著优于 **AudioLDM 2**（7.05）等基线（Table 1）。这表明共享码本和联合训练并未损害音乐生成质量，在保持竞争力的同时实现了多模态统一。

**动作到音乐生成。** 在 AIST++ 上，UniMuMo 的节拍覆盖率（Beats Coverage）达 93.0，节拍命中率（BeatsHit）达 88.4，接近当前最优模型 **CDCD**（93.9/90.7），并大幅超越 **D2M-GAN**（87.4/81.7）（Table 2）。该结果验证了运动特征通过冻结音乐码本映射到音乐空间后，能够有效驱动节奏对齐的音乐生成。

**音乐到动作生成。** 在舞蹈生成任务上，UniMuMo 的节拍对齐分数（Beat Align）为 0.24，略低于 **EDGE**（0.27）但优于 **Bailando**（0.22）（Table 3）。需要注意的是，物理脚接触分数（PFC）因官方脚本在作者提供的测试数据上无法产生正确分数而被排除，因此该维度的评估存在指标缺失。

**音乐与动作字幕。** 在 MusicQA 子集上，UniMuMo 的音乐字幕 BLEU 达到 0.261，超越 **LTU**（0.238）和 **MU-LLaMA**（0.225）（Table 4）。在 HumanML3D 上，动作字幕的 R-Precision Top1 为 0.520，与 **MotionGPT**（0.534）接近（Table 5）。字幕任务的表现表明，联合音乐-运动解码器提取的跨模态特征对理解任务同样有效。

**主观对齐评估。** 用户研究显示，经对齐算法处理后的音乐-动作配对平均评分为 3.95（满分 5），显著高于随机配对的 3.26（Appendix E），从主观感知层面验证了基于节拍的对齐方法的有效性。

### 消融实验分析

Table 6 和 Appendix G 报告了五项消融实验，揭示了各设计组件的因果贡献：

![[assets/figures/papers/paper_list_l1825_Unified_Text_Music_and_Motion_Generation/figures/008_Table_6.jpg]]
*Table 6: Comparisons of our full model with different ablation studies on MusicCaps for music generation and our Music4All for dance generation. Ablation 1-2 show the results of using an independent motion VQVAE for encoding motion sequences. Ablation 3 shows the results of model without the key structures of separate embedder and MoE. Ablation 4 shows the results of using a mixture of training tasks during training. Ablation 5 shows the result of training our model from scratch*

1. **共享码本编码的必要性（消融 1-2）。** 将运动编码替换为独立的运动 VQ-VAE 后，音乐生成的 FADvGG 升高，运动生成质量下降。这证明将运动映射到冻结的音乐 RVQ 空间是实现跨模态对齐和联合生成的关键，独立码本导致模态间语义鸿沟无法弥合。

2. **模态特定组件的作用（消融 3）。** 移除单独的运动嵌入层和额外的运动 FFN（MoE 式设计）后，运动生成性能大幅下降。这表明尽管共享码本提供了统一的离散空间，但音乐和运动在时序动态和语义粒度上仍存在差异，需要模态特定的前馈网络进行适配。

3. **联合生成 vs. 多任务训练（消融 4）。** 采用多任务训练方案（同时训练文本到音乐-动作、音乐到动作、动作到音乐）替代并行联合生成，结果不理想。论文推测原因包括任务间梯度冲突和任务难度差异——文本到音乐-动作是核心任务，而单向转换任务可能引入干扰信号。

4. **预训练初始化的收益（消融 5）。** 从头训练需要 30K 迭代才能收敛，而基于 MusicGen 微调仅需 15K 迭代，且最终性能仍略优于从头训练。这验证了预训练音乐生成模型提供的先验知识对加速收敛和提升最终质量的重要作用。

### 局限性与失败模式

尽管 UniMuMo 在统一多模态生成上取得了显著进展，但仍存在以下限制：

- **生成音乐的音质瓶颈。** 训练数据中的音乐经过人声分离处理，许多样本仍残留伪影，导致生成音乐的保真度低于当前最优的纯音乐生成模型。这是数据质量而非模型架构的根本性限制。
- **文本描述质量依赖合成。** 由于缺乏真实的多模态文本标注，文本描述通过模板填充、LLM 生成和音乐语言模型生成合成。这些合成描述可能缺乏特异性或包含事实错误（Table 7 展示了三种合成描述的示例），限制了条件生成的精确性和字幕任务的准确度上限。
- **节拍检测的鲁棒性。** 音乐-动作对齐算法高度依赖节拍检测的准确性。对于节拍模糊或无清晰节奏的音乐（如环境音乐、自由节奏乐曲），对齐质量可能显著下降。
- **领域泛化能力。** 模型主要在器乐和特定舞蹈风格（AIST++、DanceDB）上训练，对包含人声的音乐或多样化动作风格（如体育动作、日常手势）的泛化能力未经充分验证。
- **舞蹈评估指标不完善。** 现有指标（如 Beat Align）主要关注节奏同步性，无法全面捕捉舞蹈的艺术表现力和多样性。PFC 指标因环境不匹配无法使用，进一步削弱了评估的完整性。

![[assets/figures/papers/paper_list_l1825_Unified_Text_Music_and_Motion_Generation/figures/009_Table_7.jpg]]
*Table 7: Examples of three kinds of synthesized text descriptions*

### 开放问题

从实验分析和消融结果中，可以提炼出以下亟待探索的方向：

- 如何构建大规模、高质量、包含精确文本描述的真实多模态数据集，以替代当前的合成文本方案？
- 多任务训练为何劣于联合生成？梯度冲突的具体机制和任务权重的最优平衡策略需要更深入的理论分析。
- 如何在保证运动生成质量的前提下提升音乐生成的音质？更好的声源分离技术或高质量训练数据的获取是关键路径。
- 联合码本方法能否扩展到更多模态（如歌词、视频）或实现更精细的风格控制（如特定音乐流派的舞蹈生成）？

### 补充图表

![[assets/figures/papers/paper_list_l1825_Unified_Text_Music_and_Motion_Generation/figures/003_Table_1.jpg]]
*Table 1: Comparison of text-to-music generation on MusicCaps. Bold and underlined results are the best and second-best results*

![[assets/figures/papers/paper_list_l1825_Unified_Text_Music_and_Motion_Generation/figures/005_Table_2.jpg]]
*Table 2: Comparison of motion-conditioned music generation on AIST++*

![[assets/figures/papers/paper_list_l1825_Unified_Text_Music_and_Motion_Generation/figures/006_Table_3.jpg]]
*Table 3: Comparison of music-conditioned and text-conditioned dance generation*

![[assets/figures/papers/paper_list_l1825_Unified_Text_Music_and_Motion_Generation/figures/007_Table_4.jpg]]
*Table 4: Comparison of music captioning on MusicQA dataset*

![[assets/figures/papers/paper_list_l1825_Unified_Text_Music_and_Motion_Generation/figures/004_Table_5.jpg]]
*Table 5: Comparison of motion captioning on HumanML3D dataset*




## 定位与知识库关联

UniMuMo 的核心定位是**首个统一文本、音乐和动作三模态的生成框架**，其设计思路并非从零构建，而是在多个成熟单模态模型的基础上进行跨模态融合与扩展。理解其技术谱系，需要从三个关键维度展开：基座模型的继承关系、与各单模态/跨模态基线的对比定位，以及该方法固有的适用边界与未决问题。

### 基座模型继承与架构改造

UniMuMo 的方法论根植于两个预训练系统的深度复用与改造：

1. **音乐生成基座：MusicGen**。UniMuMo 的第二阶段直接以 MusicGen 的 Transformer 解码器为起点进行微调。MusicGen 本身采用延迟模式处理残差矢量量化码本的多个层级，UniMuMo 完整保留了这一机制，并在其基础上引入三个关键改造：为运动 token 增加独立的嵌入层、添加运动专用的前馈网络以形成类 MoE 结构、以及设计交叉模态因果注意力掩码以实现音乐与运动 token 的并行自回归生成。这种“冻结主干 + 模态特定扩展”的策略，使得 UniMuMo 在继承 MusicGen 文本到音乐生成能力的同时，获得了处理运动序列的能力。

2. **音频 tokenization 基座：EnCodec**。UniMuMo 最具创新性的设计是将运动序列映射到冻结的 EnCodec 残差矢量量化码本空间中。具体而言，Stage 1 训练一个运动编码器-解码器，其编码器将运动序列映射到与音乐相同的嵌入空间，然后直接复用 EnCodec 的冻结 RVQ 码本进行离散化，解码器再从该共享码本重建运动。这一“共享码本”策略是整个框架能够实现跨模态统一生成的关键——它使得音乐和运动 token 在语义空间中对齐，为后续 Transformer 的联合建模奠定了基础。消融实验（Table 6, Ablation 1-2）证实，若替换为独立的运动 VQ-VAE 码本，音乐生成的 FADvGG 会升高，运动生成质量也显著下降，验证了共享码本对跨模态融合的必要性。

### 与各任务基线的定位关系

UniMuMo 并非在每个单向任务上都追求超越专门模型，而是以“一个模型覆盖所有方向”为设计目标。从实验对比中可以清晰看到其在不同任务上的相对位置：

**文本到音乐生成**。在 MusicCaps 基准上，UniMuMo（300M 参数）取得 FADvGG 5.93，与在同一数据上微调后的 MusicGen（5.81）基本持平，优于 AudioLDM 2 等基线。这表明引入运动生成能力并未显著损害音乐生成质量，统一框架的代价可控。

**运动到音乐生成**。在 AIST++ 上，UniMuMo 的节拍覆盖率（Beats Coverage）达到 93.0，命中率（BeatsHit）88.4，接近该任务的最优专门模型 **CDCD**（93.9/90.7），并显著优于 **D2M-GAN**。值得注意的是，UniMuMo 在此任务上采用零样本推理——仅凭训练时学到的音乐-运动联合分布，无需额外微调即可从运动序列生成节奏对齐的音乐。

**音乐到舞蹈生成**。在 AIST++ 舞蹈生成评测中，UniMuMo 的 Beat Align 分数为 0.24，略低于 **EDGE**（0.27）和 **Bailando**（0.26），但差距较小。需要指出的是，物理脚接触分数因官方脚本在测试数据上无法产生正确结果而被排除，这意味着舞蹈物理合理性的对比尚不完整。

**音乐/运动字幕生成**。在 MusicQA 子集上，UniMuMo 的 BLEU 达到 0.261，超过 **LTU**（0.238）和 **MU-LLaMA**（0.229）；在 HumanML3D 运动字幕任务上，R-Precision Top1 为 0.520，与 **MotionGPT**（0.534）接近。Stage 3 的字幕模块通过引入可训练的全自注意力层（从交叉模态因果注意力初始化）并冻结音乐-运动解码器主体，实现了高效的字幕能力扩展。

### 关键设计选择的消融验证

Table 6 的消融实验揭示了几个关键设计选择的作用机制：

- **共享码本 vs. 独立码本**：如前所述，独立运动 VQ-VAE 导致音乐和运动生成质量双降，证明共享码本不仅是一个工程便利，更是跨模态语义对齐的核心使能器。
- **模态特定组件**：移除单独的运动嵌入层和 MoE 式运动 FFN（Ablation 3）后，运动生成性能大幅下降，说明即使共享码本空间，模态特定的处理路径对于融合质量至关重要。
- **并行生成 vs. 多任务训练**：尝试用多任务学习替代联合并行生成（Ablation 4）结果不理想，论文推测原因在于梯度冲突和任务难度差异——这一现象在多模态多任务学习中普遍存在，但具体机制仍需进一步研究。
- **预训练初始化**：从头训练（Ablation 5）需要 30K 迭代才能收敛，而微调仅需 15K，且最终性能仍略逊于微调版本，证实了 MusicGen 预训练权重对收敛速度和最终质量的双重贡献。

### 适用边界与局限

UniMuMo 的能力边界受限于以下几个结构性因素：

1. **训练数据质量**：音乐数据经过人声分离处理，许多样本仍残留伪影，导致生成音乐的音频保真度低于直接在高质量音乐上训练的专门模型。这是当前统一框架在音乐质量上难以超越 MusicGen 等模型的核心瓶颈。

2. **节拍对齐依赖**：数据对齐流程高度依赖音乐节拍检测和视觉节拍检测的准确性。对于节奏模糊或无清晰节拍的音乐（如环境音乐、自由节奏的古典乐），对齐质量可能显著下降，进而影响生成效果。

3. **文本描述质量**：文本描述通过模板填充、LLM 生成和音乐语言模型生成三种方式合成。这些合成描述缺乏特异性，可能包含事实错误，限制了条件生成的精度和字幕评估的上限。

4. **模态与风格泛化**：模型主要在器乐音乐和特定舞蹈风格（AIST++ 的街舞、DanceDB 的芭蕾等）上训练，对人声音乐或更广泛的动作风格（如日常手势、体育动作）的泛化能力尚未验证。

5. **评估体系不完整**：舞蹈生成的评估指标有限，Beat Align 等指标无法全面捕捉艺术质量和多样性；物理脚接触分数因环境不匹配而不可用，进一步削弱了评估的全面性。

### 开放问题

从 UniMuMo 的设计和实验结果中，可以提炼出以下尚未解决的关键问题：

- **大规模高质量三模态数据集的构建**：当前数据是通过对齐和合成构建的，如何获取天然包含精确文本描述的音乐-运动配对数据，是进一步提升统一模型性能的前提。
- **共享码本的多模态扩展**：当前的共享码本方案能否扩展到歌词、视频等更多模态？更细粒度的控制（如指定音乐风格与舞蹈情绪）如何在统一框架中实现？
- **多任务训练为何失效**：消融实验显示多任务训练不如并行生成，但梯度冲突的具体来源和任务权重的最优平衡策略仍不清楚，这可能是多模态统一模型训练中的一个普遍性问题。
- **音乐保真度的提升路径**：在不牺牲运动生成质量的前提下，如何通过更好的人声分离或更高质量的训练数据来提升生成音乐的保真度？
- **对齐精度与多样性的权衡**：数据对齐精度越高，模型越容易学习节奏对应关系，但过度对齐可能限制生成多样性。最优的对齐策略和数据配比仍有待探索。



## 原文 PDF

![[paperPDFs/AAAI_2025/Unified_Text_Music_and_Motion_Generation.pdf]]
