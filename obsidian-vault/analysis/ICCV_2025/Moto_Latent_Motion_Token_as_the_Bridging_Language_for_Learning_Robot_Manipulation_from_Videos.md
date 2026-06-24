---
title: "Moto: Latent Motion Token as the Bridging Language for Learning Robot Manipulation from Videos"
type: paper
paper_level: A
venue: ICCV
year: 2025
pdf_ref: paperPDFs/ICCV_2025/Moto_Latent_Motion_Token_as_the_Bridging_Language_for_Learning_Robot_Manipulation_from_Videos.pdf
aliases:
- Moto
tags:
- ICCV_2025
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/representation_learning
core_operator: "将帧间变化压缩为离散的“潜在运动令牌”（Latent Motion Tokens），以此作为桥接语言进行自回归预训练，并通过共同微调将运动先验注入动作预测。"
primary_logic: "通过VQ-VAE以无监督方式从视频中提取紧凑的运动令牌，利用GPT模型自回归预测运动令牌序列来学习通用运动先验；在微调时引入可学习的动作查询令牌，并与运动令牌共同预测，既保留了预训练的运动知识，又实现了向精确机器人动作的平滑迁移。"
claims:
- "潜在运动令牌能以极低维度（每帧8令牌）捕捉视觉运动语义，在CALVIN 34类任务分类中准确率达79.7%，接近使用完整图像特征的82.8%。"
- "在SIMPLER基准上，Moto-GPT的整体平均成功率达到61.4%，而未经运动预训练的基线（Moto w/o Motion Token）仅为48.0%。"
- "在CALVIN ABC→D长期任务上，Moto-GPT的平均任务长度达到3.10，优于代表性预训练模型GR-1（3.06）和SuSIE（2.69）。"
- "仅使用1%的动作标注数据时，Moto-GPT仍能达到52.5%的成功率，而从头训练变体成功率为0%，凸显了运动先验在低资源场景下的巨大价值。"
---

# Moto: Latent Motion Token as the Bridging Language for Learning Robot Manipulation from Videos

> [!tip] 核心洞察
> 通过VQ-VAE以无监督方式从视频中提取紧凑的运动令牌，利用GPT模型自回归预测运动令牌序列来学习通用运动先验；在微调时引入可学习的动作查询令牌，并与运动令牌共同预测，既保留了预训练的运动知识，又实现了向精确机器人动作的平滑迁移。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Moto：以潜在运动令牌为桥接语言从视频中学习机器人操作 |
| 英文题名 | Moto: Latent Motion Token as the Bridging Language for Learning Robot Manipulation from Videos |
| 会议/期刊 | ICCV 2025 |
| Links | [paper](https://arxiv.org/abs/2412.04445v4); [Project](https://chenyi99.github.io/moto/) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/representation_learning |
| Method | Moto |
| Dataset | SIMPLER, CALVIN (ABC→D), Real-world, CALVIN (ABC→D) with 1% labeled data |

> [!tip] 效果简介
> - SIMPLER 上，Overall Average Success Rate 为 0.614，对比 0.480 (Moto w/o Motion Token)，变化 +0.134。
> - CALVIN (ABC→D) 上，Average Length (Avg. Len.) 为 3.10，对比 3.06 (GR-1)，变化 +0.04。
> - Real-world 上，Average Success Rate 为 0.60，对比 0.233 (Moto w/o Motion Token)，变化 +0.367。

## 概述

### 问题瓶颈

机器人操作策略的学习长期受限于高昂的动作标注成本。现有的视频预训练方法——无论是基于掩码自编码器还是视频语言模型——普遍聚焦于静态帧的纹理、物体身份等外观细节，却忽略了帧间**运动动态**这一与低层动作控制直接相关的信息。这种忽略导致预训练表示难以有效迁移到精确的动作预测任务上。因此，核心瓶颈在于：**缺乏一种能够从海量无标注视频中高效捕获运动知识、并将其平滑注入机器人动作策略的表示与预训练范式**。

### 核心方法

Moto 提出以 **潜在运动令牌（Latent Motion Tokens）** 作为桥接语言来解决上述瓶颈。其核心思路分为三步：

1. **运动压缩**：通过 VQ-VAE 架构的 Latent Motion Tokenizer，以无监督方式将连续两帧之间的视觉变化压缩为一组离散令牌（每帧仅 8 个令牌），实现对运动信息的紧凑编码。
2. **运动先验学习**：Moto-GPT 以语言指令和初始帧为条件，自回归地预测运动令牌序列，从而在大规模视频数据上习得通用运动先验。
3. **共同微调**：在下游机器人数据上微调时，引入可学习的动作查询令牌（Action Query Tokens），与运动令牌共同输入 GPT 模型，同时保留运动令牌预测损失（$\mathcal{L}_{motion}$）和动作损失（$\mathcal{L}_{action}$），实现运动先验向精确动作控制的平滑迁移。

该方法的关键因果调节变量在于**运动令牌这一中间表示**：它将硬件无关的运动语义从具体实施例中解耦，使得人类视频中的运动模式也能为机器人策略提供有效先验。

### 方法谱系与知识库定位

Moto 位于机器人基础模型、视频预训练和序列建模的交叉点。与现有工作相比，其差异化体现在以下三个关键维度：

| 维度 | 基线方法 | Moto 的改进 |
|------|----------|-------------|
| **预训练表示** | 使用原始图像块或像素预测/对比学习作为自监督目标（如 GR-1 预测未来帧像素） | 使用 VQ-VAE 从帧间变化中学习离散的潜在运动令牌，并以此作为自回归预测目标 |
| **微调策略** | 丢弃预训练令牌或仅附加动作头，仅使用动作损失训练 | 保留运动令牌预测损失，同时通过可学习的动作查询令牌生成真实动作，实现共同微调 |
| **跨域迁移机制** | 无特定的知识桥接，或直接复用图像特征到新实施例 | 以潜在运动令牌作为硬件无关的运动“语言”，使人类视频运动也能驱动机器人动作 |

在具体基线对比中，**GR-1** 通过预测未来帧像素进行预训练，但其表示仍与像素级外观强耦合；**SuSIE** 依赖预训练图像编辑模型生成子目标图像，未直接建模运动动态；**RT-1-X**、**RT-2-X**、**OpenVLA** 等基于大规模 VLM 的方法虽具备强大的视觉语言理解能力，但其预训练目标未显式捕获帧间运动信息。Moto 的运动令牌范式填补了这一空白，在 CALVIN 长期任务（ABC→D）上以平均任务长度 3.10 超越了 GR-1（3.06）和 SuSIE（2.69）。

### 主要结果

Moto 在多个基准上展现出显著的性能优势：

- **SIMPLER 基准**：Moto-GPT 整体平均成功率达 **61.4%**，较未使用运动令牌的从头训练基线（Moto w/o Motion Token，48.0%）提升 **13.4 个百分点**。
- **CALVIN ABC→D 长期任务**：平均任务长度达 **3.10**，优于代表性预训练模型 GR-1（3.06）和 SuSIE（2.69）。
- **真实世界实验**：平均成功率达 **60%**，远超 Moto w/o Motion Token 的 23.3%。
- **低数据场景**：仅使用 **1% 的动作标注数据**时，Moto-GPT 仍能达到 52.5% 的成功率，而从头训练变体成功率为 0%，凸显运动先验在数据效率上的巨大价值。
- **消融验证**：联合微调策略（保留 $\mathcal{L}_{motion}$）显著优于忽略运动令牌预测损失（Moto-IML）或完全丢弃运动令牌（Moto-DM）的变体，证实了运动先验有效迁移的必要性。

### 证据强度与局限

上述结论由多维度实验支撑：潜在运动令牌在 CALVIN 34 类任务分类中达到 79.7% 的准确率（接近使用完整图像特征的 82.8%），验证了其语义表达能力（Table 1）；SIMPLER 和 CALVIN 上的对比实验覆盖了多个强基线，置信度较高。但需注意，部分基线（如 RoboFlamingo）可能使用了额外的夹爪摄像头视图和本体感受状态，构成不完全公平的比较因素。此外，人类到机器人运动的迁移目前仅在初步实验中验证，大规模多样化人类活动视频上的泛化能力仍待进一步检验。

## 背景与动机

机器人学习面临一个根本性瓶颈：**高质量动作标注数据的获取成本极高**。要让机器人学会精确的操作技能，通常需要大量带有动作标签的专家示教数据，而这类数据的采集耗时、昂贵，且难以跨不同硬件平台复用。与此同时，互联网上存在着海量的无标注视频数据——包括人类活动视频和机器人操作视频——它们天然蕴含着丰富的运动动态信息，却长期未被有效利用。

现有视频预训练方法试图填补这一缺口，但它们的设计重心普遍偏向**静态帧的细节重建或对比学习**，例如预测未来帧的像素值（如 **GR-1**）或学习视觉表征的对比目标（如 **R3M**）。这些方法的核心缺陷在于：它们捕获的是视觉外观层面的变化，而非与低层动作控制直接相关的**运动动态**。外观变化受光照、纹理、背景等因素干扰，而运动动态——物体的位移方向、速度、旋转幅度——才是决定机器人动作的关键信号，且具有天然的硬件无关性。

这一缺口导致了一个尴尬的局面：即便在大规模视频上预训练了强大的视觉编码器，在迁移到具体机器人策略时，仍需依赖大量标注数据来“重新学习”运动与动作之间的映射关系。**核心瓶颈在于缺乏一种能够高效捕获视频运动知识、并将其平滑迁移到精确动作控制的表示形式与预训练范式**。

Moto 正是针对这一瓶颈提出的解决方案。其核心动机是：**将帧间变化压缩为一种紧凑、离散的“潜在运动令牌”（Latent Motion Tokens），并以此作为桥接语言，连接视频预训练与机器人动作学习**。通过自回归地预测运动令牌序列，模型可以在无动作标注的视频上学习通用运动先验；在微调阶段，这些运动令牌又可直接与动作预测模块协同优化，实现运动知识向精确控制信号的迁移。这一设计使得机器人可以从纯视频中学习“如何运动”，而仅需少量标注数据即可学会“如何行动”。

## 核心创新

Moto的核心创新在于构建了一个以**潜在运动令牌（Latent Motion Tokens）**为桥接语言的视频预训练范式，解决了机器人学习中将无动作标签的视频运动知识迁移到精确动作控制这一瓶颈。其关键设计围绕三个紧密耦合的“changed slots”展开。

### 1. 预训练表示：从静态帧到离散运动令牌

传统视频预训练方法（如GR-1预测未来像素、SuSIE生成目标图像）聚焦于静态帧的细节重建或对比学习，忽视了与低层动作直接相关的帧间运动动态。Moto提出了一种全新的预训练表示：

- **Latent Motion Tokenizer**（M-Former + VQ Codebook + ViT Decoder）：以无监督VQ-VAE架构，将连续两帧的视觉变化压缩为一组离散的潜在运动令牌。该分词器通过联合优化重建损失、向量量化损失和承诺损失进行训练（Section 3.2）。
- **紧凑性与语义性**：每帧仅需**8个令牌**即可捕捉核心运动语义。在CALVIN的34类任务分类中，使用运动令牌的准确率达到**79.7%**，接近使用完整图像特征的82.8%（Table 1），验证了其信息保真度。同时，Figure 4显示，同一运动令牌在不同初始帧下可产生语义一致的视觉效果，证实了其作为“运动语言”的潜力。

这一设计将预训练目标从“重建像素”转变为“预测运动令牌”，使模型专注于学习硬件无关的运动动态。

### 2. 跨域迁移机制：以运动令牌作为统一桥接语言

现有方法缺乏将人类视频或异构机器人视频中的运动知识有效迁移到目标实施例的机制。Moto的关键创新在于：

- **硬件无关的运动表示**：潜在运动令牌仅编码帧间变化，不包含实施例的绝对外观或关节状态，天然具有跨形态迁移能力。
- **人类到机器人的运动翻译**：Figure 10可视化了人类视频运动令牌与机器人动作之间的语义对齐。实验证据表明，在OXE数据之外加入人类视频（SSV2）进行预训练后，Moto在SIMPLER的Move Near任务上成功率显著提升（Figure 9），初步验证了跨形态运动迁移的可行性。

这一机制使得Moto成为首个在视频预训练中明确构建“运动语言”以桥接人类与机器人操作的工作。

### 3. 微调策略：从丢弃预训练令牌到共同微调

传统微调策略通常丢弃预训练令牌或仅附加动作头，仅使用动作损失训练，导致预训练阶段学到的运动先验被灾难性遗忘。Moto引入了**共同微调（Co-Fine-Tuning）**策略：

- **可学习的动作查询令牌**：在微调阶段，向Moto-GPT输入中插入一组特殊的动作查询令牌，通过MLP动作头从隐藏状态预测位移、旋转和夹爪状态。
- **联合损失函数**：微调总损失为运动令牌预测损失与动作损失之和：
  $$\mathcal{L}_{ft} = \mathcal{L}_{motion} + \mathcal{L}_{action}$$
  其中 $\mathcal{L}_{motion}$ 保留自回归运动令牌预测目标，$\mathcal{L}_{action}$ 为位移/旋转的Smooth-L1损失与夹爪二元交叉熵损失之和（Eq. 1-3）。

消融实验（Figure 12）严格验证了这一策略的必要性：保留运动令牌预测损失的Moto-GPT显著优于忽略该损失的Moto-IML和完全丢弃运动令牌的Moto-DM。在仅使用**1%动作标注数据**的极端低资源场景下，Moto-GPT仍能达到**52.5%**的成功率，而从头训练变体成功率为0%（Figure 11），证明共同微调有效保留了运动先验并实现了高效迁移。

## 整体框架

![[assets/figures/papers/paper_list_l26_https_arxiv_org_abs_2412_04445v4/figures/002_Figure_2.jpg]]
*Figure 2: Overview of Moto’s three training stages: (1) The Latent Motion Tokenizer encodes key visual motions between video frames into compact latent tokens in an unsupervised manner using pure video data. (2) Moto-GPT is pre-trained with autoregressive motion token prediction to learn motion priors from video-instruction pairs. (3) Moto-GPT is co-fine-tuned on action-labeled trajectories to predict robot actions based on the output of learnable action query tokens while maintaining the next-motion-token prediction objective*

Moto 的整体设计围绕一个核心思路展开：将视频中连续的帧间变化压缩为离散的“潜在运动令牌”（Latent Motion Tokens），并以此作为桥接语言，实现从视频预训练到机器人动作控制的平滑迁移。整个框架由三个顺序衔接的训练阶段构成（Figure 2），各阶段之间通过统一的运动令牌表示传递知识。

**阶段一：潜在运动分词器（Latent Motion Tokenizer）的无监督训练。** 该模块的目标是从纯视频数据中学习一个紧凑、离散的运动表示。其输入为连续的两帧 RGB 图像，输出为一组离散的运动令牌。具体而言，分词器首先利用一个冻结的预训练 ViT 编码器提取两帧的 patch 特征，随后通过一个多层 Transformer 模块 **M-Former** 对帧间变化进行建模，再经 VQ-VAE 架构中的向量量化码本（codebook）将连续的运动特征量化为离散令牌。最后，一个基于 ViT 的解码器根据初始帧和运动令牌重建后续帧，以重建损失、向量量化损失和承诺损失联合优化整个分词器。经过此阶段，任意两帧之间的运动动态被压缩为极低维度的令牌序列（每帧仅 8 个令牌），为后续生成式预训练提供了紧凑的预测目标。

**阶段二：Moto-GPT 的自回归运动预训练。** 在获得潜在运动令牌后，Moto-GPT 以 GPT 架构为基础，在视频-指令对上进行自回归预训练。其输入条件包括语言指令（通过冻结的 T5 文本编码器编码）和初始帧的视觉特征（通过冻结的 ViT 编码器编码），预测目标为真实运动令牌序列的逐令牌似然最大化：

$$\mathcal { L } _ { m o t i o n } = - \sum _ { i = 1 } ^ { M } \log P ( m _ { i } | l , v , m _ { < i } ; \boldsymbol { \Theta } )$$

这一阶段的核心价值在于：GPT 模型通过预测“下一运动令牌”的任务，隐式地学习了跨实施例、跨场景的通用运动先验——物体如何移动、机械臂如何接近目标、抓取前后的典型变化模式等。由于运动令牌本身是硬件无关的紧凑表示，这种先验天然具备向不同机器人形态迁移的潜力。

**阶段三：面向动作策略的共同微调。** 预训练完成后，Moto-GPT 在带有动作标签的机器人演示数据上进行微调，以输出可执行的真实动作。微调阶段的关键设计是引入一组可学习的**动作查询令牌**（Action Query Tokens），将其与运动令牌序列拼接后送入 GPT 模型。动作查询令牌对应的隐藏状态被送入一个 MLP 动作头，分别预测末端执行器的位移、旋转和夹爪状态，其损失函数为：

$$\mathscr { L } _ { a c t i o n } = \mathscr { L } ( \Delta x ) + \mathscr { L } ( \Delta \theta ) + \mathscr { L } ( \Delta g r i p )$$

其中位移和旋转采用 Smooth-L1 损失，夹爪状态采用二元交叉熵损失。微调的总损失同时保留了运动令牌预测损失，以强制模型在适应具体动作空间的同时不遗忘预训练阶段学到的运动先验：

$$\mathcal { L } _ { f t } = \mathcal { L } _ { m o t i o n } + \mathcal { L } _ { a c t i o n }$$

**输入输出流总结。** 在推理阶段，Moto-GPT 接收语言指令和当前观测帧，自回归地预测运动令牌序列，同时通过动作查询令牌并行输出每一步的真实动作。这种设计使得运动令牌成为连接“视频理解”与“动作生成”的中间表示层：上游的视觉运动知识通过令牌编码注入，下游的动作策略通过共同微调从令牌中解码出精确控制信号。消融实验（Figure 12）证实，若在微调时丢弃运动令牌预测损失（Moto-IML）或完全移除输入中的运动令牌（Moto-DM），性能均显著下降，验证了共同微调对保留运动先验的必要性。

## 核心模块与公式推导

Moto 的核心架构由三个级联模块构成，分别对应无监督运动令牌化、自回归运动先验预训练和动作策略共同微调（Figure 2）。

**1. 潜在运动分词器（Latent Motion Tokenizer）**

该模块以无监督方式将连续两帧间的视觉动态压缩为离散令牌序列。其结构包含三个子组件：
- **冻结的 ViT 编码器**：提取当前帧 $o_t$ 与前序帧 $o_{t-1}$ 的最后一层 patch 特征。
- **M-Former**：一个多层 Transformer，以两帧的 ViT 特征为输入，提取运动特征。
- **VQ 码本与 ViT 解码器**：通过向量量化将运动特征映射到离散码本索引，再由解码器重建未来帧。

分词器采用标准 VQ-VAE 目标进行联合优化，包含重建损失、向量量化损失和承诺损失（Section 3.2）。其关键性质是：每帧仅需 8 个令牌即可捕捉视觉运动语义，在 CALVIN 34 类任务分类中达到 79.7% 准确率，接近使用完整图像特征的 82.8%（Table 1）。

**2. Moto-GPT 预训练**

Moto-GPT 是一个 GPT 架构的 Transformer，以冻结的 T5 文本编码器输出的语言指令 $l$ 和初始帧视觉特征 $v$ 为条件，自回归预测运动令牌序列。预训练损失为运动令牌的负对数似然：

$$\mathcal{L}_{motion} = -\sum_{i=1}^{M} \log P(m_i \mid l, v, m_{<i}; \boldsymbol{\Theta})$$

其中 $m_i$ 为第 $i$ 个真实运动令牌，$m_{<i}$ 为前序令牌，$\boldsymbol{\Theta}$ 为模型参数。该阶段仅使用视频-指令对，无需动作标注，使模型学习通用的、硬件无关的运动先验（Section 3.3）。

**3. 动作查询令牌与共同微调**

在微调阶段，Moto-GPT 的输入中插入可学习的**动作查询令牌**（Action Query Tokens），与运动令牌序列拼接。这些查询令牌的隐藏状态经 MLP 动作头映射为机器人动作（位移 $\Delta x$、旋转 $\Delta \theta$、夹爪状态 $\Delta grip$）。动作损失为：

$$\mathscr{L}_{action} = \mathscr{L}(\Delta x) + \mathscr{L}(\Delta \theta) + \mathscr{L}(\Delta grip)$$

其中位移和旋转使用 Smooth-L1 损失，夹爪状态使用二元交叉熵损失。微调总损失联合保留运动令牌预测损失和动作损失：

$$\mathcal{L}_{ft} = \mathcal{L}_{motion} + \mathcal{L}_{action}$$

这一共同微调策略是运动先验有效迁移的关键：消融实验（Figure 12）表明，保留 $\mathcal{L}_{motion}$ 的 Moto-GPT 显著优于忽略该损失（Moto-IML）或完全丢弃运动令牌（Moto-DM）的变体。

## 实验与分析

### 核心实验设置

Moto的训练与评估遵循三阶段范式：首先在Open-X-Embodiment（OXE）的109k轨迹视频上无监督训练Latent Motion Tokenizer；随后在相同视频数据上自回归预训练Moto-GPT；最后在RT-1 Robot-Action数据集的73k动作标注轨迹上进行共同微调。真实世界评估使用90个遥操作演示（每任务30个）。所有模型仅使用静态摄像头RGB图像作为视觉输入，部分对比基线可能使用了夹爪摄像头视图或本体感受状态，这构成潜在的不公平比较因素。

### 潜在运动令牌的表达能力

Table 1的结果验证了运动令牌的核心设计前提：以每帧仅8个令牌的极低维度，在CALVIN 34类任务分类中达到79.7%的语义准确率，接近使用完整ViT图像特征的82.8%。Figure 4进一步展示了令牌的可解释性——同一初始帧配不同运动令牌可解码出语义一致的视觉运动，同一令牌在不同初始帧下也保持运动语义的判别性。这表明VQ-VAE成功将帧间变化压缩为紧凑且语义保真的离散表示。

![[assets/figures/papers/paper_list_l26_https_arxiv_org_abs_2412_04445v4/figures/008_Table_1.jpg]]
*Table 1: Video classification accuracy with varied representations*

### SIMPLER基准主结果

Table 2报告了SIMPLER环境下的整体平均成功率。Moto-GPT达到61.4%，较从头训练的Moto w/o Motion Token（48.0%）提升13.4个百分点，验证了运动令牌预训练带来的增益。在与其他大规模预训练模型的对比中，Moto-GPT超越了RT-1-X、RT-2-X、Octo-Base和OpenVLA等基线。值得注意，OpenVLA（fine-tuned）可能已在其预训练数据中包含了测试领域分布，而Moto-GPT仅使用静态RGB输入即取得竞争性表现。

![[assets/figures/papers/paper_list_l26_https_arxiv_org_abs_2412_04445v4/figures/009_Table_2.jpg]]
*Table 2: SIMPLER evaluation results of models pre-trained on Open-X-Embodiment [52] datasets. The “Overall” column reports the success rate averaged across the sub-tasks of all task types*

### CALVIN长期任务结果

在CALVIN ABC→D基准上（Table 3），Moto-GPT的平均任务长度达到3.10，优于代表性视频预训练模型GR-1（3.06）和SuSIE（2.69）。考虑到Moto-GPT仅依赖静态RGB图像，而GR-1和SuSIE可能使用了更丰富的视觉输入，这一结果凸显了运动令牌作为通用运动先验的有效性。MT-R3M（GR-1变体，使用R3M编码器）达到3.18，略高于Moto-GPT，但其使用了预训练的机器人专用视觉编码器。

![[assets/figures/papers/paper_list_l26_https_arxiv_org_abs_2412_04445v4/figures/010_Table_3.jpg]]
*Table 3: Comparison of models adopting different pre-training techniques on CALVIN (ABC−→D). Avg. Len. is a comprehensive metric indicating the average number of tasks accomplished in a row across 1,000 trial sequences. “Static RGB” and “Gripper RGB” denote the RGB images from a static camera or a gripper view, respectively. “Proprio” is short for the proprioceptive robot state*

### 真实世界实验

Figure 8展示了真实世界三个任务（Pick Up、Move Near、Knock Over）的评估结果。Moto-GPT平均成功率达到60%，而Moto w/o Motion Token仅为23.3%。Move Near任务上，Moto-GPT成功率为70%，远超基线的16.7%，说明运动先验对空间位移类任务尤为重要。

### 数据效率与低资源场景

Figure 11揭示了运动预训练最显著的价值：仅使用1%的动作标注数据时，Moto-GPT仍能达到52.5%的成功率，而从头训练变体成功率为0%。随着标注数据比例增加，两者差距逐渐缩小，但Moto-GPT始终维持优势。这证明通过视频预训练获得的运动先验大幅降低了对昂贵动作标注的依赖。

### 微调策略消融

Figure 12对比了三种微调变体：Moto-GPT（保留运动令牌预测损失）、Moto-IML（忽略运动损失，仅用动作损失）和Moto-DM（完全丢弃运动令牌输入）。Moto-GPT显著优于两种变体，Moto-IML和Moto-DM虽因预训练运动先验而优于从头训练，但仍落后于共同微调策略。这确证了在微调中保留$\mathcal{L}_{motion}$对于运动先验的有效迁移至关重要。

### 跨形态运动迁移

Figure 9展示了在OXE数据之外加入人类活动视频（SSV2）预训练的效果。Moto（OXE+SSV2）在SIMPLER的Move Near任务上显著优于仅用OXE预训练的Moto（OXE）和Moto w/o Motion Token，验证了潜在运动令牌可作为硬件无关的运动“语言”，实现从人类视频到机器人动作的跨形态迁移。Figure 10可视化了这一迁移过程：人类视频的运动令牌序列可驱动生成语义对齐的机器人运动轨迹。

### 轨迹合理性评估

Figure 7展示了Moto-GPT的附加能力：通过计算轨迹的对数似然，可有效区分成功轨迹、失败轨迹和随机轨迹。这暗示预训练的运动先验可作为隐式的奖励信号或轨迹质量评估器，为强化学习等下游应用提供潜在价值。

### 局限性与待验证点

当前实验存在以下局限：人类视频预训练仅在Move Near单一任务上验证，对复杂操作的泛化能力尚不明确；模型最大处理3帧视频，可能限制在更长时序任务中的适用性；运动分词器主要在机器人视频上训练，在大规模多样化人类活动视频上的表现有待进一步验证。

### 补充图表

![[assets/figures/papers/paper_list_l26_https_arxiv_org_abs_2412_04445v4/figures/001_Figure.jpg]]

![[assets/figures/papers/paper_list_l26_https_arxiv_org_abs_2412_04445v4/figures/017_Figure_13.jpg]]
*Figure 13: Illustration of the evaluation tasks in SIMPLER [31]*

![[assets/figures/papers/paper_list_l26_https_arxiv_org_abs_2412_04445v4/figures/024_Figure_16.jpg]]
*Figure 16: Predicted video trajectories by the pre-trained Moto-GPT for CALVIN tasks reflecting delicate robot actions*

![[assets/figures/papers/paper_list_l26_https_arxiv_org_abs_2412_04445v4/figures/018_Table_4.jpg]]
*Table 4: Implementation details of the Latent Motion Tokenizer*

![[assets/figures/papers/paper_list_l26_https_arxiv_org_abs_2412_04445v4/figures/019_Table_5.jpg]]
*Table 5: Training hyperparameters for Latent Motion Tokenizer*

![[assets/figures/papers/paper_list_l26_https_arxiv_org_abs_2412_04445v4/figures/021_Table_6.jpg]]
*Table 6: Implementation details of Moto-GPT*

![[assets/figures/papers/paper_list_l26_https_arxiv_org_abs_2412_04445v4/figures/022_Table_7.jpg]]
*Table 7: Training hyperparameters for Moto-GPT*

![[assets/figures/papers/paper_list_l26_https_arxiv_org_abs_2412_04445v4/figures/023_Table_8.jpg]]
*Table 8: Top-K motion token prediction accuracy of Moto-GPT in predicting ground-truth latent motion tokens from a 128-size codebook on the validation splits of the pre-training datasets*

## 方法谱系与知识库定位

### 核心差异：从“静态外观”到“动态运动”的预训练范式转移

Moto 的立论基础在于识别出当前机器人视频预训练的一个根本性瓶颈：主流方法——无论是基于对比学习的视觉表示（如 R3M、VIP），还是预测未来像素的视频模型（如 GR-1）——其自监督目标均侧重于静态帧的细节或像素级重建，忽视了与低层动作控制紧密相关、且天然跨硬件共享的**运动动态**。这一偏差导致预训练表示向精确动作控制的迁移效率低下，尤其在高昂的动作标注成本下，数据效率问题被急剧放大。

Moto 通过一个因果性设计扭转了这一范式：它将帧间变化压缩为离散的“潜在运动令牌”，并以此作为自回归预训练的唯一预测目标。这一转变的本质在于，预训练阶段不再强迫模型学习场景纹理或物体外观，而是专注于理解“物体如何移动”这一与动作语义直接对齐的抽象知识。随后的共同微调策略则通过保留运动令牌预测损失，确保这一运动先验在策略学习过程中不被灾难性遗忘，从而实现了从视频运动知识到精确机器人动作的平滑注入。

### 与代表性基线的方法论对比

Moto 与现有预训练机器人策略的方法差异，集中体现在预训练表示、微调策略和跨域迁移机制三个关键维度上。

**预训练表示的选择**是分水岭。**GR-1**（Wu et al., 2023）采用 GPT 架构直接预测未来单帧的像素值，其学习目标混杂了外观与运动信息，且像素级重建的计算开销巨大。**SuSIE**（Black et al., 2023）则绕开了动作预测，转而利用预训练图像编辑模型生成目标子图，再交由低层策略执行，其高层规划与低层执行之间存在语义断层。相比之下，Moto 的潜在运动令牌以每帧仅 8 个离散令牌的极低维度，在 CALVIN 34 类任务分类中达到 79.7% 的准确率，接近使用完整图像特征的 82.8%（Table 1），证明运动信息可以被高度压缩且不失语义保真度。基于 VLM 的路线如 **RT-2-X**（基于 PaLI-X 55B）和 **OpenVLA**（基于 Prismatic-7B）虽具备强大的语义理解能力，但其预训练目标并非为运动控制设计，动作空间通常被文本化处理，与连续控制之间存在表示鸿沟。

**微调策略**决定了预训练知识能否有效保留。Moto 的消融实验（Figure 12）提供了决定性证据：联合微调（Moto-GPT）显著优于仅使用动作损失（Moto-IML）或完全丢弃运动令牌输入（Moto-DM）的变体。这验证了一个关键因果机制——在微调阶段持续预测运动令牌，充当了正则化约束，防止策略网络在有限的标注数据上过拟合到特定实施例的低层动作模式，从而保留了通用的运动理解能力。这一设计直接解释了为何在仅使用 1% 动作标注数据时，Moto-GPT 仍能达到 52.5% 的成功率，而从头训练变体成功率为 0%（Figure 11）。

**跨域迁移机制**是 Moto 最具前瞻性的贡献。通过将运动令牌定义为硬件无关的“桥接语言”，Moto 实现了人类视频运动向机器人动作的语义对齐。当在 OXE 机器人数据之外加入人类活动视频（SSV2）进行预训练后，Moto 在 SIMPLER 的 Move Near 任务上成功率进一步提升（Figure 9），且可视化显示人类与机器人的运动令牌在潜在空间中具有语义一致性（Figure 10）。这一能力是现有基线所不具备的——无论是基于 VLM 的策略还是像素预测模型，均缺乏将人类运动抽象为可迁移控制信号的显式机制。

### 适用边界与局限

尽管 Moto 在实验上展现了显著优势，其适用边界需审慎界定。

**数据分布与泛化能力**。潜在运动分词器的训练主要依赖机器人视频（OXE 子集），虽展示了跨实施例的语义一致性，但尚未在大规模、多样化的互联网人类活动视频上充分验证。当前仅在 SSV2 的有限子集上进行了初步探索，对于涉及精细手指操作、快速动态或多人交互的复杂人类活动，运动令牌的编码能力和迁移效果仍待检验。

**时序建模的深度限制**。Moto 当前最大处理 3 帧视频，这一设计虽降低了计算开销，但可能限制了在更长时序、多步骤任务中的适用性。对于需要长程运动规划的复杂操作（如“打开抽屉→放入物体→关闭抽屉”），3 帧的运动上下文可能不足以捕获任务级别的时序依赖。

**任务范式的局限性**。Moto 目前仅应用于模仿学习场景，其作为通用运动先验的潜力尚未在强化学习或模型预测控制等范式中得到验证。尽管 Figure 7 展示了 Moto-GPT 的 log-likelihood 可有效区分成功、失败和随机轨迹，暗示其可作为奖励信号，但这一方向尚未被系统探索。

**与基线的公平比较问题**。需注意，Moto-GPT 仅使用静态摄像头 RGB 图像，而部分基线（如 RoboFlamingo）可能使用了夹爪摄像头视图和本体感受状态。此外，OpenVLA（fine-tuned）等模型可能在预训练阶段已接触测试领域的数据分布，这使得直接数值比较存在一定的不公平因素。

### 开放问题

Moto 开辟了以运动为中心的预训练路线，但以下问题构成了该方向的关键挑战：

1. **规模化运动令牌的普适性**：能否通过融合互联网规模的人类活动视频，训练出覆盖更广泛运动模式的通用运动分词器？这需要解决人类运动与机器人运动在动力学、视角和运动幅度上的域差异。

2. **时序扩展与计算效率的平衡**：如何设计更优的令牌化策略和序列长度，在运动表达的完整性与计算效率之间取得平衡？可能的路径包括分层运动令牌（粗粒度任务级+细粒度动作级）或自适应帧率采样。

3. **从运动先验到环境模拟器**：Moto 的预训练表示能否作为通用的环境模拟器或奖励生成器，增强强化学习的样本效率？Figure 7 的初步证据表明这一方向具有潜力，但需要更系统的验证。

4. **缩小人类-机器人运动域差异**：如何进一步缩小人类运动令牌与机器人动作空间之间的域差异，实现更少标注下的高效微调？可能的方案包括域对抗训练或运动重定向模块。

5. **任务范式的横向扩展**：能否将 Moto 扩展到导航、移动操作等更广泛的机器人任务，形成统一的运动驱动策略？这需要验证运动令牌在非操作场景下的语义表达能力。

## 原文 PDF

![[paperPDFs/ICCV_2025/Moto_Latent_Motion_Token_as_the_Bridging_Language_for_Learning_Robot_Manipulation_from_Videos.pdf]]
