---
title: Exploring Vision Transformers for 3D Human Motion-Language Models with Motion Patches
type: paper
paper_level: A
venue: CVPR
year: 2024
pdf_ref: paperPDFs/CVPR_2024/Exploring_Vision_Transformers_3D_Human_Motion_Language_Models_Motion_Patches.pdf
project_link: null
code_link: https://github.com/
aliases:
- MPVO
- EVT3HMLMMP
tags:
- CVPR_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 将运动序列按身体部位划分并插值成固定大小的“运动补丁”（motion patches），结合ImageNet预训练的ViT进行迁移学习。
primary_logic: 通过模拟图像补丁的形式构建运动补丁，可将运动数据映射到图像域，从而复用强大的视觉预训练模型，既解决数据稀缺问题，又实现跨骨架的统一表示。
claims:
- 使用预训练ViT和运动补丁的组合在HumanML3D文本到运动检索R@1上达到10.80%，显著优于无预训练（8.46%）和无补丁（8.36%）。
- 在KIT-ML数据集上，预训练+补丁的R@1为14.02%，而从头训练补丁模型仅10.41%，不使用补丁9.54%。
- 所提方法在所有评估协议下均优于先前最好的方法TMR，例如HumanML3D small batches协议R@1 71.61% vs 67.45%。
- 跨骨架zero-shot识别和迁移学习实验证明运动补丁可统一不同骨架，且迁移后KIT-ML R@1达15.28%，超过单独训练的最佳结果。
---

# Exploring Vision Transformers for 3D Human Motion-Language Models with Motion Patches

> [!tip] 核心洞察
> 通过模拟图像补丁的形式构建运动补丁，可将运动数据映射到图像域，从而复用强大的视觉预训练模型，既解决数据稀缺问题，又实现跨骨架的统一表示。

| 字段 | 内容 |
|------|------|
| 中文题名 | 利用视觉Transformer与运动补丁构建3D人体运动-语言模型 |
| 英文题名 | Exploring Vision Transformers for 3D Human Motion-Language Models with Motion Patches |
| 会议/期刊 | CVPR 2024 |
| Links | [Code](https://github.com/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Motion Patches + ViT (Ours) |
| Dataset | HumanML3D, KIT-ML |

> [!tip] 效果简介
> - HumanML3D (All protocol) 上，Text-motion R@1↑ 10.80 vs 8.92 (+1.88)。
> - HumanML3D (Small batches) 上，Text-motion R@1↑ 71.61 vs 67.45 (+4.16)。
> - KIT-ML (All protocol) 上，Text-motion R@1↑ 14.02 vs 10.05 (+3.97)。

## 概要

### 问题与瓶颈

3D人体运动-语言建模面临两个核心瓶颈：其一，高质量运动-文本配对数据远少于图像-文本数据，标注成本高昂；其二，不同数据集使用差异化的骨架结构，导致模型难以在异构骨架间泛化，现有方法通常只能针对单一骨架从头训练Transformer运动编码器，无法复用预训练知识。

### 核心方法与因果机制

本文提出**运动补丁（motion patches）** 这一新表示，作为将运动序列映射到图像域的关键纽带。具体而言，将人体骨架按身体部位（如躯干、四肢）划分为五个分区，对各分区内关节坐标进行插值采样得到固定数量（N=16）的采样点，再沿时间轴滑动窗口堆叠N个连续帧，最终构成N×N的二维补丁——其形式与图像补丁高度相似。这一设计使得**ImageNet-21k预训练的ViT-B/16**可直接作为运动编码器进行迁移学习，文本侧则采用DistilBERT提取嵌入，二者通过对称对比损失对齐到共享语义空间。

该设计的因果逻辑在于：运动补丁将异构骨架统一为固定尺寸的“类图像”表示，从而解锁了大规模视觉预训练模型的迁移能力，在数据稀缺条件下显著提升泛化性，并天然支持跨骨架的零样本识别。

### 主要结果

在HumanML3D和KIT-ML两个标准基准上，所提方法在所有评估协议下均超越此前最优方法**TMR**（Petrovich et al., ICCV 2023）：

- **HumanML3D**：Small batches协议下文本-运动检索R@1达到71.61%（TMR为67.45%），All协议下R@1为10.80%（TMR为8.92%）。
- **KIT-ML**：Small batches协议下R@1为53.55%（TMR为51.13%），All协议下R@1为14.02%（TMR为10.05%）。

消融实验证实两项设计缺一不可：移除预训练权重使HumanML3D R@1从10.80%降至8.46%，而将运动补丁替换为原始关节序列则进一步跌至8.36%。跨骨架迁移实验显示，在HumanML3D上预训练的模型迁移至KIT-ML后R@1可达15.28%，超越在KIT-ML上单独训练的最佳结果，验证了运动补丁的统一表示能力。

### 方法谱系与知识库定位

与现有运动-语言模型相比，**TEMOS**（Petrovich et al., ECCV 2022）、**T2M+**（Guo et al., CVPR 2022）和**TMR**均使用从零训练的Transformer编码原始关节序列，**MotionCLIP**（Tevet et al., ECCV 2022）虽引入CLIP视觉特征但仍依赖专用运动编码器。本文方法是首个将预训练ViT与统一运动补丁表示相结合的运动-语言模型，其核心贡献在于**表示层面的创新**——通过运动补丁弥合了3D运动数据与2D视觉预训练模型之间的模态鸿沟，而非提出新的对比学习范式或网络架构。

### 局限与开放问题

当前方法存在以下局限：运动-语言数据总量仍远小于图像-文本数据，限制了大模型潜力的充分释放；ViT-Large在KIT-ML等小数据集上出现性能退化，存在过拟合风险；零样本跨骨架识别的R@1仅为7.35%，跨域泛化仍有较大提升空间；运动补丁的语义可解释性有限，注意力图中的激活模式与具体运动语义的对应关系尚不明确。此外，该方法目前仅覆盖检索、分类和识别任务，尚未拓展至文本到运动生成。



### 3D 人体运动-语言建模的核心瓶颈

3D 人体运动-语言模型旨在建立文本描述与三维人体运动序列之间的语义对齐，其下游任务涵盖文本到运动检索、运动到文本检索、零样本运动分类等。然而，该领域长期受困于一个根本性矛盾：**数据稀缺与表示异构**。

一方面，3D 人体运动数据的采集和标注成本远高于图像或文本数据。主流基准数据集 HumanML3D 和 KIT-ML 的规模分别仅为约 14,000 和 3,900 个运动序列，与动辄数百万甚至数十亿规模的图像-文本数据集相比差距悬殊。这一数据瓶颈直接限制了从零开始训练大规模运动编码器的可能性，使得现有模型难以充分学习运动语义的丰富性。

另一方面，不同数据集的骨架结构（skeleton structure）存在显著差异——关节数量、关节定义、运动学链（kinematic chain）拓扑各不相同。例如，HumanML3D 使用 22 关节骨架，而 KIT-ML 使用 21 关节骨架，两者的关节映射并非简单的一一对应。这种异构性导致在某一数据集上训练的模型难以直接泛化到另一数据集，跨骨架的迁移学习面临严重的表示障碍。

### 现有方法的缺口

当前主流的运动-语言模型（如 **TEMOS**（Petrovich et al., ECCV 2022）、**T2M+**（Guo et al., CVPR 2022）、**TMR**（Petrovich et al., ICCV 2023）等）普遍采用以下技术路线：

- **输入表示**：直接使用原始关节坐标序列（形状为 T × J × 3，即时间帧 × 关节数 × 三维坐标），将其线性投影或通过轻量嵌入层输入 Transformer。
- **运动编码器**：从零开始训练的 Transformer 编码器，未利用任何预训练权重。

这一范式存在两个结构性缺陷。首先，从零训练的运动编码器受限于运动数据的有限规模，其学习到的运动表征在泛化能力和语义丰富度上均受到制约。其次，原始关节坐标序列作为输入，对骨架结构高度敏感——当骨架定义发生变化时，输入维度和语义含义均随之改变，模型必须从头重新训练，无法实现跨骨架的知识迁移。

值得关注的是，在计算机视觉领域，Vision Transformer（ViT）通过将图像划分为固定大小的图像补丁（image patches），成功实现了从大规模图像预训练到下游视觉任务的高效迁移学习。这一范式启发了本文的核心问题：**能否将运动序列转化为类似图像补丁的“运动补丁”（motion patches），从而复用强大的视觉预训练模型？**

### 本文动机

针对上述瓶颈，本文提出了一种全新的运动-语言建模框架，其核心动机体现在两个层面：

1. **通过运动补丁实现跨骨架的统一表示**：将运动序列按身体部位（body parts）进行划分，对每个部位沿时间轴插值采样，构建固定大小的二维运动补丁（如 16×16）。这一表示形式不仅消除了不同骨架结构之间的维度差异，还将运动数据映射到类似图像的二维网格空间，为复用图像域预训练模型奠定了基础。

2. **借助预训练 ViT 突破数据瓶颈**：以运动补丁作为输入，直接使用在 ImageNet-21k 上预训练的 ViT 作为运动编码器（迁移学习），将大规模视觉预训练中习得的特征提取能力迁移到运动域。这一策略有效缓解了运动数据稀缺对模型容量的限制，使模型能够在有限标注数据下学习到更丰富的运动-语言语义对齐。

简言之，本文方法的因果机制可概括为：**运动补丁（统一表示） + 预训练 ViT（迁移学习） → 跨骨架泛化 + 数据高效学习**。这一设计在 HumanML3D 和 KIT-ML 两个基准数据集上均取得了最优的文本-运动检索性能，并首次展示了跨骨架零样本识别和有效迁移学习的能力。



## 核心方法与创新机理

本文的核心创新在于提出了一种全新的3D人体运动表示方法——**运动补丁（Motion Patches）**，并以此为基础，将**视觉Transformer（ViT）**成功引入运动-语言跨模态学习领域。该方法通过两个关键“changed slots”实现了对现有范式的突破。

### 1. 从关节序列到运动补丁：输入表示的范式转变

现有方法（如TEMOS、TMR）直接将原始关节坐标序列 $T \times J \times 3$ 作为Transformer的输入，这种表示方式面临两大瓶颈：一是不同数据集的骨架结构（关节数量与拓扑）不一致，导致模型难以统一处理；二是3D运动数据本身标注稀缺，难以支撑大规模模型的有效训练。

本文提出的运动补丁表示从根本上改变了这一局面。其构建过程如Figure 3所示：
- **按身体部位分区**：将人体骨架关节按语义划分为五个部分（如躯干、左臂、右臂、左腿、右腿），打破了对特定骨架拓扑的依赖。
- **插值标准化**：在每个身体部位内对关节进行插值，采样固定数量（N=16）的样本点，使不同骨架结构的运动序列都能映射到统一的维度。
- **时空堆叠**：将N个连续帧的N个采样点堆叠，形成 $N \times N$ 的二维“运动补丁”，在形式上与图像补丁完全对齐。

这一设计的关键洞察在于：**运动补丁将3D运动数据映射到了图像域**。如Figure 4所示，将关节坐标视为RGB像素后，不同运动类别（如“行走”、“跳跃”）呈现出明显不同的纹理模式，验证了运动补丁的语义表达能力。更重要的是，这种统一表示天然具备跨骨架泛化的潜力——无论原始骨架结构如何，最终都转化为固定大小的补丁。

### 2. 从零训练到迁移学习：运动编码器的质变

现有方法（TEMOS、TMR、MotionCLIP）的运动编码器均需从零开始训练，这直接限制了模型在数据稀缺条件下的性能上限。本文的第二个关键创新是**将ImageNet-21k预训练的ViT-B/16直接用作运动编码器**，实现了从视觉域到运动域的迁移学习。

这一选择的因果逻辑链清晰：
- 运动补丁在形式上与图像补丁（16×16）完全一致，使得ViT可以“无感”接收运动数据。
- ViT在ImageNet上学习到的层次化特征提取能力（从边缘纹理到语义概念）可以被迁移到运动模式识别中。
- 预训练权重提供了强大的初始化先验，使得模型在小规模运动数据集上也能有效收敛。

Table 1的系统性对比凸显了这一创新的独特性：在已有工作中，**只有本文方法同时具备“预训练运动编码器”和“统一骨架表示”两个特性**。

### 3. 创新组合的因果验证

消融实验（Table 4）提供了因果推论的直接证据。在HumanML3D数据集上，当同时移除预训练权重和运动补丁时，模型退化为“从零训练的原始序列编码器”，文本到运动检索R@1从10.80%骤降至8.36%。单独移除预训练权重（保留补丁但从头训练）导致R@1降至8.46%，而单独移除补丁（使用预训练ViT但输入原始关节序列）则降至8.36%。这表明**两个创新组件存在协同效应**：补丁提供了图像化的统一接口，预训练权重则注入了可迁移的视觉先验，二者缺一不可。

在KIT-ML数据集上，同样的模式得到复现：预训练+补丁的R@1为14.02%，而从头训练补丁模型仅10.41%，不使用补丁则降至9.54%。跨数据集的证据一致性增强了结论的可靠性。



本方法的核心思路是将3D人体运动序列转化为一种类图像的“运动补丁”（motion patches）表示，从而能够直接复用在大规模图像数据上预训练的视觉Transformer（ViT）作为运动编码器，并与文本编码器进行跨模态对比学习。整体框架由四个关键模块串联构成。

**输入表示：从骨架序列到运动补丁**

传统方法直接将原始关节坐标序列 $T \times J \times 3$ 送入从零训练的Transformer。本工作则提出运动补丁构建模块（Motion Patch Construction），将运动序列映射为固定大小的二维补丁表示。具体而言，首先将人体骨架关节按身体部位划分为五个分区（如躯干、左臂、右臂、左腿、右腿），对每个分区内的关节进行插值采样得到 $N$ 个均匀分布的空间采样点；然后沿时间维度取连续 $N$ 帧，将各分区的采样点坐标堆叠排列，最终形成尺寸为 $N \times N$ 的运动补丁。默认设置 $N=16$，得到 $16 \times 16$ 的补丁，从形式上与ViT所期望的图像补丁输入完全一致（见Figure 3）。

**运动编码器：预训练ViT的迁移学习**

运动编码器模块采用在ImageNet-21k上预训练的ViT-B/16，其patch size为16，与运动补丁的尺寸天然匹配。ViT接收运动补丁序列，通过自注意力机制建模时空依赖关系，最终以[class] token的输出作为整个运动序列的嵌入向量 $\mathcal{F}_M(m_i)$。这一设计的因果机制在于：运动补丁将骨架运动数据“伪装”成图像域的信号，使得ViT在大规模自然图像上习得的底层特征提取能力（如边缘、纹理、局部模式）可以被迁移到运动理解任务中，从而有效缓解3D运动数据稀缺带来的训练困难。

**文本编码器：轻量级语言模型**

文本编码器采用DistilBERT，将文本描述映射为固定维度的嵌入向量 $\mathcal{F}_T(t_j)$。选择DistilBERT而非更大模型的原因在于其计算效率高，同时保留了足够的语义表达能力，适合与运动编码器进行联合对比学习。

**跨模态对齐：对称对比学习**

运动嵌入与文本嵌入之间的相似度通过余弦相似度计算：

$$s(m_i, t_j) = \frac{\mathcal{F}_M(m_i) \cdot \mathcal{F}_T(t_j)}{\lVert \mathcal{F}_M(m_i) \rVert \lVert \mathcal{F}_T(t_j) \rVert}$$

训练采用对称交叉熵损失，同时拉近匹配的运动-文本对、推远不匹配的对。运动到文本的损失为：

$$\mathcal{L}_{m2t} = -\frac{1}{B} \sum_i^B \log \frac{\exp(s(m_i, t_i) / \tau)}{\sum_{j=1}^B \exp(s(m_i, t_j) / \tau)}$$

文本到运动的损失为：

$$\mathcal{L}_{t2m} = -\frac{1}{B} \sum_i^B \log \frac{\exp(s(m_i, t_i) / \tau)}{\sum_{j=1}^B \exp(s(m_j, t_i) / \tau)}$$

总损失为两者之和 $\mathcal{L} = \mathcal{L}_{m2t} + \mathcal{L}_{t2m}$，其中 $\tau$ 为可学习的温度参数，$B$ 为批次大小。这一对称设计确保了检索任务中两个方向的性能均衡。

**数据流总结**

完整的pipeline数据流如Figure 2所示：原始运动序列 → 运动补丁构建 → ViT运动编码器 → 运动嵌入 → 与DistilBERT文本嵌入计算余弦相似度矩阵 → 对称对比损失反向传播。训练完成后，模型可直接用于文本到运动检索、运动到文本检索，以及零样本分类和跨骨架识别等下游任务，无需额外微调。

### 补充图表

![[assets/figures/papers/paper_list_l1848_Exploring_Vision_Transformers_3D_Human_Motion_Language_Models_Motion_Pat/figures/001_Figure_1.jpg]]
*Figure 1: Overview of the existing methods and the proposed method. The existing methods train an original Transformer with the joint information from the motion sequences directly, while the proposed method converts them into motion patches and then trains the ViT, which can be initialized with pre-trained weights*

![[assets/figures/papers/paper_list_l1848_Exploring_Vision_Transformers_3D_Human_Motion_Language_Models_Motion_Pat/figures/003_Figure_2.jpg]]
*Figure 2: Overview of the proposed framework, which consists of a motion encoder and a text encoder. We transform the raw motion sequences into motion patches as the input of the ViT-based motion encoder. We calculate the similarity matrix between text-motion pairs within a batch to train the model. To illustrate this concept, we provide an example batch containing three samples for clarity*



### 问题形式化与相似度度量

本工作旨在学习一个跨模态的共享潜在空间，使得语义匹配的运动序列与文本描述在该空间中彼此靠近。给定一批运动-文本对 $\{ (m_i, t_i) \}_{i=1}^B$，运动编码器 $\mathcal{F}_M$ 与文本编码器 $\mathcal{F}_T$ 分别将运动与文本映射为嵌入向量，二者之间的余弦相似度定义为：

$$s ( m_i , t_j ) = \frac{ \mathcal{F}_M ( m_i ) \cdot \mathcal{F}_T ( t_j ) }{ \lVert \mathcal{F}_M ( m_i ) \rVert \lVert \mathcal{F}_T ( t_j ) \rVert } \tag{Eq. 1}$$

其中 $\mathcal{F}_M(m_i)$ 为运动嵌入，$\mathcal{F}_T(t_j)$ 为文本嵌入，$\lVert \cdot \rVert$ 为 L2 范数。该相似度是后续对比学习损失的核心输入。

### 运动补丁构建模块

运动补丁（motion patches）是本文的核心表示创新，其构建过程（参见 Figure 3）将原始的骨架关节序列转化为类似图像补丁的二维网格结构，使 ViT 能够直接处理运动数据。具体流程如下：

![[assets/figures/papers/paper_list_l1848_Exploring_Vision_Transformers_3D_Human_Motion_Language_Models_Motion_Pat/figures/004_Figure_3.jpg]]
*Figure 3: Process of building the motion patches for each motion sequence. Given a skeleton, we mark different body parts in different colors. We show the method to construct the motion patch of the right leg. The same process is applied to other body parts*

1. **身体部位划分**：将人体骨架关节按语义分为五个身体部位（躯干、左臂、右臂、左腿、右腿），每个部位包含若干关节。
2. **插值采样**：对每个身体部位内的关节序列进行插值，在空间维度上均匀采样 $N$ 个点，获得该部位的连续空间表示。
3. **时序堆叠**：取 $N$ 个连续帧，将每帧的 $N$ 个采样点按身体部位排列，形成 $N \times N$ 的二维矩阵，即一个“运动补丁”。

通过这种方式，一段运动序列被转化为一系列 $N \times N$ 的补丁，每个补丁同时编码了空间结构（身体部位关节分布）与时序动态（连续帧的关节位移）。当 $N=16$ 时，运动补丁尺寸为 $16 \times 16$，与 ViT-B/16 的输入补丁尺寸完全匹配。

### ViT 运动编码器

运动编码器采用在 ImageNet-21k 上预训练的 ViT-B/16（12 层 Transformer，补丁大小 16）。运动补丁经过线性投影后输入 ViT，最终取 `[class]` token 对应的输出作为运动嵌入 $\mathcal{F}_M(m)$。预训练权重的迁移使得模型在运动数据稀缺的条件下仍能学习有效的表示。

### 文本编码器

文本编码器 $\mathcal{F}_T$ 采用冻结的 DistilBERT，将文本描述映射为固定维度的嵌入向量。消融实验（Table 9）表明，DistilBERT 与预训练 ViT 的组合优于 CLIP 文本/视觉编码器的替代方案。

### 对比学习损失

训练采用对称的对比学习目标，包含运动到文本（motion-to-text）和文本到运动（text-to-motion）两个方向的损失函数。

**运动到文本损失**：对于批次中的每个运动 $m_i$，将其匹配文本 $t_i$ 作为正样本，批次内其他文本作为负样本：

$$\mathcal{L}_{m2t} = -\frac{1}{B} \sum_i^B \log \frac{\exp ( s ( m_i , t_i ) / \tau )}{\sum_{j=1}^B \exp ( s ( m_i , t_j ) / \tau )} \tag{Eq. 2}$$

**文本到运动损失**：对称地，对于每个文本 $t_i$，将其匹配运动 $m_i$ 作为正样本：

$$\mathcal{L}_{t2m} = -\frac{1}{B} \sum_i^B \log \frac{\exp ( s ( m_i , t_i ) / \tau )}{\sum_{j=1}^B \exp ( s ( m_j , t_i ) / \tau )} \tag{Eq. 3}$$

**总损失**为两者之和：

$$\mathcal{L} = \mathcal{L}_{m2t} + \mathcal{L}_{t2m} \tag{Eq. 4}$$

其中 $B$ 为批次大小，$\tau$ 为可学习的温度参数，控制相似度分布的锐度。该对称设计强制运动与文本在两个方向上相互检索，使共享潜在空间的对齐更加紧密。

### 补充图表

![[assets/figures/papers/paper_list_l1848_Exploring_Vision_Transformers_3D_Human_Motion_Language_Models_Motion_Pat/figures/005_Figure_4.jpg]]
*Figure 4: Visualization of motion patches by regarding the joint coordinates as RGB pixels. We show the rendered motions and their text label on the left and the processed motion patches on the right. We can observe different motions reflected in different motion patches*



## 实验与关键发现

### 主结果：文本-运动检索

所提方法在两个标准基准（HumanML3D 和 KIT-ML）上均取得最优文本-运动检索性能，且在所有评估协议下一致优于先前方法。

在 HumanML3D 数据集上（Table 2），完整方法在 All 协议下文本-运动 R@1 达到 10.80%，较此前最优方法 **TMR**（Petrovich et al., ICCV 2023）的 8.92% 提升 1.88 个百分点；在 Small batches 协议下 R@1 达 71.61%，较 TMR 的 67.45% 提升 4.16 个百分点。运动-文本检索方向同样表现最优，Small batches 协议下 R@1 为 72.11%。

![[assets/figures/papers/paper_list_l1848_Exploring_Vision_Transformers_3D_Human_Motion_Language_Models_Motion_Pat/figures/006_Table_2.jpg]]
*Table 2: Results of text-to-motion and motion-to-text retrieval benchmark on HumanML3D. The results of methods marked with † are sourced from TMR [38]. Ours (scratch) denotes the proposed method trained from scratch without using pre-trained ViT weights*

在 KIT-ML 数据集上（Table 3），All 协议下文本-运动 R@1 为 14.02%，较 TMR 的 10.05% 提升 3.97 个百分点；Small batches 协议下 R@1 为 53.55%，较 TMR 的 51.13% 提升 2.42 个百分点。

![[assets/figures/papers/paper_list_l1848_Exploring_Vision_Transformers_3D_Human_Motion_Language_Models_Motion_Pat/figures/007_Table_3.jpg]]
*Table 3: Results of text-to-motion and motion-to-text retrieval benchmark on KIT-ML*

值得注意的是，即使不使用预训练权重（Ours scratch），仅凭运动补丁表示，在 HumanML3D All 协议下文本-运动 R@1 已达 8.46%，与 TMR 的 8.92% 接近，验证了运动补丁表示本身的有效性。

### 消融实验：核心设计验证

消融实验（Table 4）系统验证了两个核心设计的作用：

![[assets/figures/papers/paper_list_l1848_Exploring_Vision_Transformers_3D_Human_Motion_Language_Models_Motion_Pat/figures/009_Table_4.jpg]]
*Table 4: Results of ablation studies. We experiment with different settings (1) with/without the pre-trained ViT and (2) whether to use motion patches as the representation of the motion*

**预训练 ViT 的贡献**：移除 ImageNet-21k 预训练权重（从头训练）导致 HumanML3D 文本-运动 R@1 从 10.80% 降至 8.46%，MedR 从 9.00 升至 12.00；KIT-ML 上 R@1 从 14.02% 降至 10.41%。这表明视觉预训练知识的迁移对弥补运动数据稀缺至关重要。

**运动补丁的贡献**：将运动补丁替换为原始关节序列（即使保留预训练 ViT），HumanML3D R@1 进一步降至 8.36%，MedR 升至 12.00；KIT-ML R@1 降至 9.54%。这说明运动补丁不仅能适配 ViT 架构，其时空结构化表示本身优于原始关节序列。

**组合效应**：同时使用预训练 ViT 和运动补丁时，两个数据集的所有指标均达到最优，验证了两者之间存在协同增效——预训练权重提供了强特征提取能力，运动补丁提供了适合该能力的输入表示。

### 超参数与架构选择

附录中的扩展消融进一步揭示了关键设计选择的影响：

**运动补丁大小**（Table 10）：16×16 补丁在 HumanML3D 和 KIT-ML 上均取得最佳或接近最佳性能。8×8 补丁因空间分辨率不足导致性能下降，32×32 补丁在 KIT-ML 上略有提升但 HumanML3D 上稍降，且计算开销更大。16×16 与 ViT-B/16 的标准补丁大小一致，实现了最佳适配。

**编码器组合**（Table 9）：ViT-Base 预训练于 ImageNet 搭配 DistilBERT 文本编码器的组合优于 CLIP 文本/视觉编码器组合。这暗示 ImageNet 预训练的 ViT 与轻量文本编码器的配对更适合运动-语言对齐任务。

**ViT 骨干规模**（Table 8）：ViT-Base 在两个数据集上均优于 ViT-Small 和 ViT-Large。值得注意的是，ViT-Large 在 KIT-ML 上性能反而不如 Base，存在明显过拟合——KIT-ML 仅约 4000 个样本，不足以支撑大模型训练。

### 跨骨架泛化与迁移学习

运动补丁的核心优势之一是跨骨架结构的统一表示能力。Table 5 展示了跨骨架识别实验：直接用 HumanML3D 训练的模型在 KIT-ML 上进行零样本检索，文本-运动 R@1 仅 7.35%；但经迁移学习（在 KIT-ML 上微调）后，R@1 跃升至 15.28%，甚至超过仅在 KIT-ML 上单独训练的最佳结果（14.02%）。这证明运动补丁成功统一了不同骨架结构，使模型能跨数据集迁移知识。

![[assets/figures/papers/paper_list_l1848_Exploring_Vision_Transformers_3D_Human_Motion_Language_Models_Motion_Pat/figures/011_Table_5.jpg]]
*Table 5: Results of cross-skeleton recognition. We evaluate the text-to-motion and motion-to-text retrieval on the KIT-ML dataset with the HumanML3D model and the transferred model. The transfer learning method achieves better performance than the method of training only on KIT-ML*

### 其他任务验证

**零样本运动分类**（Table 6）：方法在无需微调的情况下对运动进行分类，性能与需要类别标签的有监督方法接近，验证了运动-文本联合嵌入空间的语义质量。

**人体交互识别**（Table 7）：通过拼接多人运动特征并投影，方法在交互识别任务上优于 TMR，表明运动补丁表示对多人生成场景同样有效。

### 定性分析

Figure 5 展示了文本到运动检索的定性结果，检索到的运动与查询文本在语义上高度一致。Figure 7 的 ViT 注意力图可视化显示，模型能关注到与文本描述相关的身体部位和时序片段，为运动补丁的可解释性提供了初步证据。

![[assets/figures/papers/paper_list_l1848_Exploring_Vision_Transformers_3D_Human_Motion_Language_Models_Motion_Pat/figures/008_Figure_5.jpg]]
*Figure 5: Qualitative results of text-to-motion retrieval. For each query, we show the retrieved motions ranked by text-motion similarity and their accompanying ground-truth text labels. Note that these descriptions are not used in the retrieval process. All motions in the gallery are from the test set and were unseen during training. For the first two examples, the text queries are sampled from the data. For the last example, we query with a free-form text*

![[assets/figures/papers/paper_list_l1848_Exploring_Vision_Transformers_3D_Human_Motion_Language_Models_Motion_Pat/figures/014_Figure_7.jpg]]
*Figure 7: Visualization of attention maps extracted from ViT*

### 失败模式与局限性

尽管整体性能优异，方法仍存在明确局限：

1. **数据规模瓶颈**：运动-语言数据总量远小于图像-文本数据，限制了更大模型（如 ViT-Large）潜力的发挥，在 KIT-ML 上尤为明显。
2. **零样本跨骨架性能不足**：零样本跨骨架识别 R@1 仅 7.35%，说明统一表示虽有效，但域间差异仍显著。
3. **任务覆盖有限**：当前模型仅支持检索、分类和识别，未扩展到文本到运动生成任务。
4. **语义可解释性有限**：运动补丁虽可类比频谱图进行可视化，但其像素级模式与高层运动语义的对应关系尚不清晰，注意力图仅提供间接解释。

### 公平性说明

所有实验使用 HumanML3D 和 KIT-ML 的官方训练/验证/测试划分，评估协议（All 和 Small batches）遵循 TMR 设定。TMR 的对比结果通过重新运行官方模型并使用相同评估代码获得，确保可比性。消融实验和超参数选择在附录中全面报告。

### 补充图表

![[assets/figures/papers/paper_list_l1848_Exploring_Vision_Transformers_3D_Human_Motion_Language_Models_Motion_Pat/figures/002_Table_1.jpg]]
*Table 1: Summary of recent related methods for motion-language models. Only our proposed method utilizes pre-trained motion encoders and a unified representation for various skeleton structures*

![[assets/figures/papers/paper_list_l1848_Exploring_Vision_Transformers_3D_Human_Motion_Language_Models_Motion_Pat/figures/010_Table_6.jpg]]
*Table 6: Results of zero-shot motion classification. Modality with motion only and motion language are denoted as M and M+L, respectively. When applying our proposed method for zeroshot classification, we achieve performance results that are closely aligned with those of the 2s-AGCN classifier trained with supervision on the BABEL-60 benchmark*



## 定位与知识库关联

### 1. 与先前工作的关系

本文提出的“运动补丁+ViT”框架直接回应了3D人体运动-语言建模领域长期存在的两个瓶颈：**数据稀缺**与**骨架异构**。现有主流方法均从零开始训练运动编码器，未能利用大规模预训练模型的迁移能力。

**与检索基线的对比。** 在文本-运动检索任务上，本文方法在HumanML3D和KIT-ML两个标准基准上全面超越先前最优方法**TMR**（Petrovich et al., ICCV 2023）。具体而言：
- HumanML3D Small batches协议下，文本-运动R@1从67.45%提升至71.61%（+4.16个百分点）；
- KIT-ML All协议下，文本-运动R@1从10.05%提升至14.02%（+3.97个百分点）。

相比**TEMOS**（Petrovich et al., ECCV 2022）和**T2M+**（Guo et al., CVPR 2022），本文方法的优势更为显著。这些方法均使用从零训练的Transformer处理原始关节坐标序列，而本文通过运动补丁将运动数据映射到图像域，从而复用ImageNet-21k预训练的ViT-B/16权重，实现了跨模态迁移学习。**MotionCLIP**（Tevet et al., ECCV 2022）虽也利用了预训练视觉模型（CLIP），但其运动编码仍需从零训练，且未解决跨骨架统一表示问题。

**关键差异化槽位。** 本文在以下两个核心维度上改变了方法范式（参见Table 1）：
1. **输入表示**：从原始关节坐标序列（T × J × 3）转变为按身体部位划分、插值至16×16的运动补丁；
2. **运动编码器**：从从零训练的Transformer转变为ImageNet-21k预训练的ViT-B/16。

这一转变使得本文方法成为该领域首个同时实现“预训练运动编码器”与“跨骨架统一表示”的工作。

### 2. 适用边界

**任务边界。** 当前方法聚焦于运动-语言对齐任务，包括文本-运动检索、零样本运动分类和人体交互识别。模型**未涉及文本到运动生成**，这是其与TEMOS等生成式方法的重要分界。

**数据规模边界。** 消融实验揭示了模型对数据量的敏感性：
- 在HumanML3D（约15k序列）上，预训练ViT带来显著增益（R@1从8.46提升至10.80）；
- 在KIT-ML（约4k序列）上，ViT-Large性能反而不如ViT-Base，表明小数据集上存在过拟合风险。

**骨架泛化边界。** 跨骨架zero-shot识别实验（Table 5）证明运动补丁可统一不同骨架结构，但零样本设定下KIT-ML的R@1仅为7.35%，说明骨架差异仍是实质性障碍。迁移学习可将该指标提升至15.28%，超过在KIT-ML上单独训练的最佳结果，但仍有较大改进空间。

### 3. 局限与开放问题

**已识别的局限性：**
1. **数据总量瓶颈**：运动-语言数据总量远小于图像-文本数据（如LAION-5B），限制了大模型潜力的进一步释放；
2. **小数据集过拟合**：ViT-Large在KIT-ML上性能低于Base，模型容量与数据规模的匹配需谨慎处理；
3. **语义可解释性有限**：运动补丁虽可类比于频谱图（Figure 4），但其内部激活模式与具体运动语义的对应关系尚不清晰；
4. **任务覆盖不全**：未探索文本到运动生成任务，模型能力限于判别式任务。

**待探索的开放问题：**
1. **数据扩展策略**：如何结合未标注运动数据或合成数据（如通过运动增强或物理仿真）进一步缓解数据稀缺？
2. **生成式扩展**：运动补丁表示能否作为文本到运动生成模型的输入？若能，预训练ViT的中间层特征是否可用于条件生成？
3. **注意力机制的可解释性**：Figure 7中的ViT注意力图激活模式与具体运动语义（如“跳跃”“挥手”）的对应关系是什么？能否通过探针任务量化分析？
4. **跨模态迁移的泛化性**：该迁移学习策略能否推广到其他骨架型数据，如手势识别、面部动作编码或动物运动分析？



## 原文 PDF

![[paperPDFs/CVPR_2024/Exploring_Vision_Transformers_3D_Human_Motion_Language_Models_Motion_Patches.pdf]]
