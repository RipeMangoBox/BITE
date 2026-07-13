---
title: "Dance Across Shifts: Forward-Facilitation Continual Test-Time Adaptation through Dynamic Style Bridging"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Dance_Across_Shifts_Forward_Facilitation_Continual_Test_Time_Adaptation_through_Dynamic_Style_Bridging.pdf
project_link: null
code_link: "https://github.com/z1358/DAS"
aliases:
- DSBD
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过多级风格桥接机制动态地将合成知识库与当前目标域样本风格对齐，生成按需的可靠监督信号。
primary_logic: 由扩散模型预生成的语义纯净合成样本蕴含可靠类别信息；通过输入级（傅里叶频谱替换）、统计级（实例归一化）和表示级（监督对比学习）的多层次风格注入，将静态知识转化为与实时分布协同演化的动态监督，从而解耦可靠的语义内容与固有生成偏差。
claims:
- 在ImageNet-to-ImageNetC上，本文方法将平均分类错误率从Source的60.3%降至44.1%，显著优于所有基线方法。
- 消融实验表明逐步激活多级桥接组件可将错误率从50.0%降至44.1%，验证了各组件的有效性。
- 不同生成模型（BigGAN, SD 1.5, SD 3.0）下性能稳定，证明桥接机制对生成偏差具有解耦能力。
- 在混合领域、类不平衡以及小批量等挑战性场景下，方法保持稳定且优于DPCore等SOTA方法。
---

# Dance Across Shifts: Forward-Facilitation Continual Test-Time Adaptation through Dynamic Style Bridging

> [!tip] 核心洞察
> 由扩散模型预生成的语义纯净合成样本蕴含可靠类别信息；通过输入级（傅里叶频谱替换）、统计级（实例归一化）和表示级（监督对比学习）的多层次风格注入，将静态知识转化为与实时分布协同演化的动态监督，从而解耦可靠的语义内容与固有生成偏差。

| 字段 | 内容 |
|------|------|
| 中文题名 | 跨变化起舞：通过动态风格桥接实现前向促进的持续测试时间自适应 |
| 英文题名 | Dance Across Shifts: Forward-Facilitation Continual Test-Time Adaptation through Dynamic Style Bridging |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2605.18608) · [Code](https://github.com/z1358/DAS) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Dynamic Style Bridging (DAS) |
| Dataset | ImageNet-to-ImageNetC, CIFAR100-to-CIFAR100C, CIFAR10-to-CIFAR10C |

> [!tip] 效果简介
> - ImageNet-to-ImageNetC 上，Mean Error Rate (%) 44.1 vs 60.3 (Source) (-16.2)。
> - CIFAR100-to-CIFAR100C 上，Mean Error Rate (%) 29.8 vs 44.0 (Source) (-14.2)。
> - CIFAR10-to-CIFAR10C 上，Mean Error Rate (%) 9.1 vs 19.2 (Source) (-10.1)。

## 概要

**问题与瓶颈**：持续测试时自适应（CTTA）要求模型在推理阶段持续适应不断变化的分布偏移，而无需访问源域数据。现有方法普遍遵循“后向对齐”范式——依赖目标域噪声伪标签的自训练损失（如 **TENT**，Wang et al., ICLR 2021；**CoTTA**，Wang et al., CVPR 2022）或静态源域代理作为对齐锚点（如 **EATA**，Niu et al., ICML 2022；**RMT**，Döbler et al., CVPR 2023）。在连续分布偏移下，这些监督替代品无法提供可靠信号，导致错误累积与灾难性遗忘，构成该领域的核心瓶颈。

**核心思路**：本文提出一种全新的“前向促进”范式——**动态风格桥接（Dynamic Style Bridging, DAS）**。其核心洞见在于：由扩散模型预生成的语义纯净合成样本蕴含可靠的类别信息，但存在固有的生成偏差；通过输入级（傅里叶频谱替换）、统计级（实例归一化）和表示级（监督对比学习）的多层次风格注入，可将静态合成知识动态转化为与实时目标分布协同演化的定制监督信号，从而解耦可靠的语义内容与生成偏差，直接应对CTTA的中心挑战。

**方法定位**：DAS在监督信号来源上以“风格桥接后的合成代理交叉熵损失”取代传统“噪声伪标签自训练”，在领域知识使用方式上以“合成知识库动态演化”取代“静态源域代理对齐”，并在视觉风格适配层面引入多级桥接机制。该方法与多种自训练目标兼容，且对生成模型选择不敏感。

**主要结果**：在标准CTTA基准上，DAS将ImageNet-to-ImageNetC的平均分类错误率从Source的60.3%降至44.1%，显著优于所有基线方法（**Table 1**）。在CIFAR100-to-CIFAR100C和CIFAR10-to-CIFAR10C上分别降至29.8%和9.1%（**Table 2**）。消融实验证实多级桥接各组件的递进贡献（**Table 3**），且在不同生成模型（BigGAN、SD 1.5、SD 3.0）下性能稳定，验证了桥接机制对生成偏差的解耦能力（**Table 5**）。在混合域、类不平衡及小批量等挑战性场景下，方法保持鲁棒性并优于DPCore等SOTA方法（**Table 12, Table 13**）。代码已开源：https://github.com/z1358/DAS。

### 持续测试时自适应的核心挑战

深度神经网络在标准测试集上取得的优异性能，往往在真实部署场景中急剧退化——测试数据流随时间持续变化，分布偏移不可预测且不可逆。持续测试时自适应（Continual Test-Time Adaptation, CTTA）正是针对这一现实困境提出的任务设定：模型在未标注的、持续变化的目标数据流上逐批进行在线适应，既无法访问源域数据，也无法回访历史样本。

这一设定的核心挑战在于**监督信号的严重缺失**。模型必须在没有真实标签的条件下，仅凭当前到达的无标签样本调整参数。更严峻的是，由于目标分布持续漂移，先前累积的适应经验可能在新分布下失效，甚至产生误导——这构成了CTTA中错误累积与灾难性遗忘的根本原因。

### 后向对齐范式的困境

现有CTTA方法几乎全部遵循一种**后向对齐范式**：它们试图构建某种“锚点”作为稳定的参照系，然后将不断变化的目标分布对齐回该锚点。具体而言，这些方法可归为两类：

- **自训练代理监督**：以 **TENT**（Wang et al., ICLR 2021）为代表的熵最小化方法，利用模型对目标样本的预测置信度作为软监督信号。**CoTTA**（Wang et al., CVPR 2022）进一步引入教师-学生框架，通过历史模型平均提供更稳定的伪标签。然而，当分布偏移剧烈时，模型预测本身高度不可靠，基于噪声伪标签的自训练必然导致错误逐步放大。

- **静态源域锚点**：**EATA**（Niu et al., ICML 2022）、**RMT**（Döbler et al., CVPR 2023）等方法通过缓存少量源域样本或维护源域统计量作为对齐目标。但在持续变化的分布面前，静态锚点与实时目标域之间的鸿沟日益扩大，其提供的监督信号逐渐失去相关性。

这两种策略的共同缺陷在于：它们试图用**过去的信息**（源域锚点或历史预测）约束**当前的适应**，却无法为模型提供与实时分布真正匹配的可靠监督。当目标域从“雪天”切换到“雾天”再切换到“弹性变形”时，一个静态的源域代理或过时的教师模型无法告诉模型“当前样本的正确分类应该是什么”。

### 从“后向对齐”到“前向促进”

本文重新审视这一根本困境，提出一个关键洞察：**真正有效的监督信号应当与目标分布协同演化，而非僵化地回望过去**。

这一思考催生了全新的**前向促进范式**。其核心思路是：预先构建一个携带明确语义信息的合成知识库，然后在适应过程中，通过动态风格桥接机制将该知识库持续转化为与当前目标域风格匹配的定制化监督信号。换言之，我们不试图将目标域拉回源域，而是让可靠的知识主动走向目标域。

这一范式转换的可行性建立在以下观察之上：现代生成模型（如扩散模型）能够产生语义纯净的类别原型——这些合成样本虽在视觉风格上与真实域存在偏差，但其类别语义高度可靠。问题的关键不再是“如何获得类别信息”，而是“如何将静态的类别信息转化为与动态分布匹配的有效监督”。

### 本文动机与贡献逻辑

基于上述分析，本文的动机可概括为三个层次：

1. **诊断层面**：揭示后向对齐范式的结构性缺陷——静态锚点在连续分布偏移下的监督失效是CTTA性能瓶颈的根本原因。

2. **范式层面**：提出前向促进这一替代范式，将问题从“寻找稳定的回望锚点”重新定义为“让语义知识随分布协同演化”。

3. **实现层面**：设计多级风格桥接机制，在输入级（傅里叶频谱替换）、统计级（实例归一化）和表示级（监督对比学习）三个层次将合成知识库动态适配到当前目标域风格，从而在不牺牲语义可靠性的前提下提供按需的准确监督信号。

这一设计使得模型能够在测试时无需访问生成模型（知识库离线构建），仅通过轻量的风格注入操作即可持续获得与当前分布匹配的真实标签监督，从根本上缓解了CTTA中的错误累积问题。

## 核心方法与创新机理

### 范式转换：从后向对齐到前向促进

现有持续测试时自适应（CTTA）方法普遍遵循**后向对齐范式**——试图通过熵最小化、教师-学生一致性或源域代理将当前目标分布“拉回”已知领域。这一范式的根本瓶颈在于：当分布连续偏移时，噪声伪标签或静态锚点提供的监督信号可靠性急剧下降，导致错误累积与灾难性遗忘。

本文提出一种截然不同的**前向促进范式**：不再试图将目标域对齐到固定锚点，而是让监督信号本身与目标分布**协同演化**。核心思想是——由扩散模型预生成的语义纯净合成样本蕴含可靠的类别信息；通过多层次风格注入，将这一静态知识动态转化为与实时分布匹配的定制监督信号，从而直接为当前目标域提供准确的学习引导。

### 关键机制变更（Changed Slots）

相较于现有方法，DAS 在三个关键维度上进行了根本性重构：

**1. 监督信号来源：从噪声伪标签到代理真实标签**

基线方法（如 **TENT** (Wang et al., ICLR 2021)、**CoTTA** (Wang et al., CVPR 2022)）依赖目标域样本的熵最小化或教师模型伪标签作为自训练目标。在分布持续偏移下，这些伪标签的噪声水平不断上升，形成“错误自强化”循环。

DAS 引入**代理交叉熵损失** $\mathcal{L}_{PCE}$（Eq. 4），直接使用合成样本的**地面真值标签**进行监督：

$$\mathcal{L}_{PCE} = -\sum_{c=1}^{C} y_{i,c}^{K} \log p_{i,c}$$

这一变更的因果逻辑是：合成样本的语义内容由生成模型在受控条件下产生，其类别标签天然准确；通过风格桥接将其外观适配到目标域后，即可为模型提供“按需生成”的可靠监督，从根本上切断了伪标签噪声的累积链路。

**2. 领域知识使用方式：从静态锚点到动态演化**

**EATA** (Niu et al., ICML 2022)、**RMT** (Döbler et al., CVPR 2023) 等方法将源域代理或历史样本作为固定的对齐锚点。当目标分布远离这些锚点时，对齐信号逐渐失效。

DAS 将合成知识库 $\mathcal{M}$ 视为可动态变换的“语义种子”，而非固定参照物。通过多级桥接机制，每个目标批次到达时，合成代理的风格被实时注入当前目标域特征，使得监督信号始终与当前分布保持同步。这实现了知识使用的**状态依赖性**——代理不再是静态的“过去快照”，而是随数据流共同演化的“当下向导”。

**3. 视觉风格适配：从无到多级层次化注入**

现有 CTTA 方法几乎不涉及显式的视觉风格适配。DAS 首次引入覆盖**输入级—统计级—表示级**的三层风格桥接：

- **输入级**：通过傅里叶频谱替换，将目标样本的幅度谱注入合成图像，保留其相位谱（语义结构），实现外观风格迁移（Eq. 1）：
  $$\tilde{x}_{i}^{K} = \mathcal{F}^{-1}([\mathcal{F}^{A}(x_{j}^{t}), \mathcal{F}^{\mathcal{P}}(x_{i}^{K})])$$

- **统计级**：在浅层特征空间调整合成样本的均值和标准差以匹配目标样本（Eq. 2），消除纹理和色彩偏差：
  $$\tilde{z}(\tilde{x}_{i}^{K}) = \sigma_{j}^{t}\left(\frac{z(\tilde{x}_{i}^{K}) - \tilde{\mu}_{i}^{K}}{\tilde{\sigma}_{i}^{K}}\right) + \mu_{j}^{t}$$

- **表示级**：通过监督对比损失 $\mathcal{L}_{SCL}$（Eq. 3）在深层表示空间聚合跨域同类样本，强化语义不变性。

这三层注入形成从“像素外观”到“语义表示”的递进适配，确保合成监督不仅在视觉上可信，更在特征空间中与目标域对齐。

### 范式差异的因果机制

后向对齐范式的失效根源于一个**监督-分布错配**循环：分布偏移 → 伪标签质量下降 → 模型更新偏差 → 下一轮伪标签更差。DAS 的前向促进范式通过**解耦语义内容与视觉风格**打破这一循环——语义内容由合成知识库保障（固定且准确），视觉风格由桥接机制动态匹配（随分布演化）。两者的乘积效应使得监督信号的可靠性不再依赖于目标分布的稳定性，从而在连续偏移下保持鲁棒。

消融实验（Table 3）为这一因果逻辑提供了直接证据：逐步激活知识库、输入级注入、统计级归一化和对比学习，错误率从 50.0% 单调下降至 44.1%，验证了每级桥接的独立贡献。跨生成模型实验（Table 5）进一步表明，即使使用 BigGAN、SD 1.5、SD 3.0 等不同生成器，性能波动仅约 1.2%，证明桥接机制有效解耦了生成偏差——这是后向对齐范式无法实现的关键能力。

DAS 提出了一种与现有 CTTA 方法根本不同的**前向促进（forward-facilitation）范式**。传统方法普遍遵循后向对齐（backward-alignment）思路——要么依赖目标域噪声伪标签的自训练（如 **TENT**, Wang et al., ICLR 2021；**CoTTA**, Wang et al., CVPR 2022），要么使用静态源域代理作为对齐锚点（如 **EATA**, Niu et al., ICML 2022；**RMT**, Döbler et al., CVPR 2023）。这些策略在连续分布偏移下，监督信号的可靠性会持续衰减，导致错误累积与灾难性遗忘。

DAS 的核心洞察是：**由扩散模型预生成的语义纯净合成样本蕴含可靠的类别信息**，通过多层次的风格注入机制，可以将这些静态知识转化为与实时分布协同演化的动态监督信号，从而解耦可靠的语义内容与固有的生成偏差。

### 框架总览

整个框架（Figure 2）由三个关键阶段构成：

![[assets/figures/papers/paper_list_l1057_https_arxiv_org_abs_2605_18608/figures/002_Figure_2.jpg]]
*Figure 2: The illustration of our framework. We construct in advance a compact set of proxies containing synthetic knowledge that encapsulates explicit semantic information. During the CTTA process, our proposed multi-level bridging mechanism dynamically transforms the static knowledge in accordance with the evolving data stream, precisely delivering the reliable supervision signals required for the model adaptation, thereby robustly supporting the forward-facilitation paradigm*

1. **离线知识库构建**：利用预训练扩散模型（如 Stable Diffusion）为每个类别生成 $M$ 个语义纯净的合成样本，形成紧凑的知识库 $\mathcal{M} = (x_i^K, y_i^K)_{i=1}^{C \times M}$。这些样本具有清晰的背景和显著的主体对象，为后续适应提供带有真实标签的可靠语义锚点。

2. **多级风格桥接**：在测试时，对每个到来的目标域批次，通过三个层次将合成知识动态适配到当前分布：
   - **输入级**：通过傅里叶频谱替换，用目标样本的幅度谱替换合成样本的幅度谱，同时保留合成样本的相位谱以维持语义内容；
   - **统计级**：在浅层特征空间对齐合成样本与目标样本的通道均值和标准差；
   - **表示级**：通过监督对比学习在表示空间聚合同类跨域样本。

3. **联合优化**：模型通过三个损失项的加权和进行在线更新：
   $$\mathcal{L} = \mathcal{L}_{PCE} + \mathcal{L}_{SCL} + \mathcal{L}_{ST}$$
   其中 $\mathcal{L}_{PCE}$ 利用桥接后合成样本的真实标签提供准确监督，$\mathcal{L}_{SCL}$ 在表示空间强化类别内聚性，$\mathcal{L}_{ST}$ 通过教师-学生框架在无标签目标数据上保持预测一致性。

### 关键设计决策

- **合成知识库的紧凑性**：消融实验（Figure 4）表明，每类仅需 1 个合成样本即可达到优异性能，且对大于 2 的样本数不敏感，验证了框架对知识库规模的低依赖性。
- **生成偏差的解耦**：不同生成模型（BigGAN、SD 1.5、SD 3.0）下性能稳定（错误率分别为 45.0%、44.1%、43.8%，Table 5），证明桥接机制能有效缓解合成样本中的纹理过拟合等生成偏差。
- **损失权重统一性**：所有损失项在所有基准测试中均赋予相等权重（权重均为 1），未进行额外超参数调优，体现了方法的鲁棒性和易用性。

![[assets/figures/papers/paper_list_l1057_https_arxiv_org_abs_2605_18608/figures/001_Figure_1.jpg]]
*Figure 1: Illustration of the considered CTTA problem and comparison of different frameworks. (a) The pipeline and the central challenge of CTTA. (b)-(c) Existing methods primarily focus on the backward-alignment paradigm. (d) Our approach explores a completely different forward-facilitation paradigm. By co-evolving with the distribution, we continually transform static synthetic knowledge to the current target domain, directly addressing the central challenge*

DAS 框架的核心由三个紧密协作的模块构成：**合成知识库构建**（离线完成）、**多级风格桥接机制**（在线执行）和**优化目标**。以下逐一展开其关键设计与公式。

### 合成知识库构建

在测试时适应开始之前，利用预训练的文本到图像扩散模型为每个类别生成语义纯净的类别原型。形式化地，对于包含 $C$ 个类别的任务，每类生成 $M$ 个样本，构成紧凑的合成知识库：

$$\mathcal{M} \doteq (x_i^K, y_i^K)_{i=1}^{C \times M}$$

其中 $x_i^K$ 为合成图像，$y_i^K$ 为其对应的真实类别标签。与源域数据相比，合成样本具有更高的语义纯度（背景更干净、对象更显著），但其固有的生成偏差（如纹理过拟合）需要在后续桥接中主动解耦。

### 多级风格桥接机制

该机制将静态的合成知识库动态适配到当前目标域的数据流，从外观到表示层次递进地注入目标域风格。

**输入级：傅里叶风格注入。** 给定目标域样本 $x_j^t$ 和合成知识库样本 $x_i^K$，通过傅里叶变换将目标样本的幅度谱替换合成样本的幅度谱，同时保留合成样本的相位谱（蕴含语义结构）：

$$\tilde{x}_i^K = \mathcal{F}^{-1}([\mathcal{F}^A(x_j^t), \mathcal{F}^{\mathcal{P}}(x_i^K)]) \tag{1}$$

其中 $\mathcal{F}^A$ 和 $\mathcal{F}^{\mathcal{P}}$ 分别提取幅度谱和相位谱，$\mathcal{F}^{-1}$ 为逆傅里叶变换。此操作在保持语义内容不变的前提下，将目标域的低级纹理和颜色风格注入合成样本。

**统计级：特征统计归一化。** 在模型浅层特征空间中对齐合成样本与目标样本的统计分布。令 $z(\cdot)$ 表示浅层特征图，$\tilde{\mu}_i^K$ 和 $\tilde{\sigma}_i^K$ 为经傅里叶风格化后合成样本的逐通道均值和标准差，$\mu_j^t$ 和 $\sigma_j^t$ 为目标样本的对应统计量：

$$\tilde{z}(\tilde{x}_i^K) = \sigma_j^t \left( \frac{z(\tilde{x}_i^K) - \tilde{\mu}_i^K}{\tilde{\sigma}_i^K} \right) + \mu_j^t \tag{2}$$

该操作本质上执行实例归一化后以目标统计量重新缩放，使合成样本的浅层特征分布与当前目标域对齐。

**表示级：监督对比学习。** 在深层表示空间通过监督对比损失聚合同类跨域样本。基于伪标签定义正样本对集合 $P(i)$，损失函数为：

$$\mathcal{L}_{SCL} = -\sum_i \sum_{p \in P(i)} \log \frac{\exp(\text{sim}(h_i, h_p))}{\sum_j \exp(\text{sim}(h_i, h_j))} \tag{3}$$

其中 $h_i$ 为样本的归一化表示向量，$\text{sim}(\cdot,\cdot)$ 为余弦相似度。该损失在表示空间拉近同类样本（无论来自合成域还是目标域），进一步消解跨域风格差异。

### 优化目标

总损失由三项加权求和构成，所有项权重均设为 1，无需额外调参：

$$\mathcal{L} = \mathcal{L}_{PCE} + \mathcal{L}_{SCL} + \mathcal{L}_{ST} \tag{5}$$

**代理交叉熵损失 $\mathcal{L}_{PCE}$** 利用桥接后合成样本的真实标签提供准确监督信号：

$$\mathcal{L}_{PCE} = -\sum_{c=1}^{C} y_{i,c}^K \log p_{i,c} \tag{4}$$

其中 $p_{i,c}$ 为模型对桥接后合成样本的类别预测概率。这是整个框架中唯一使用真实标签的监督项，从根本上避免了伪标签的噪声累积问题。

**自训练损失 $\mathcal{L}_{ST}$** 采用教师-学生框架在无标签目标数据上维持预测一致性，具体为对称交叉熵形式：

$$\mathcal{L}_{ST} = -\sum_{c=1}^{C} q_c \log p_c - \sum_{c=1}^{C} p_c \log q_c$$

其中 $p_c$ 和 $q_c$ 分别为学生模型和教师模型对目标样本的预测概率。教师模型通过指数移动平均更新，提供稳定的自训练目标。

## 实验与关键发现

### 核心范式对比：从后向对齐到前向促进

现有CTTA方法（如**TENT** (Wang et al., ICLR 2021)、**CoTTA** (Wang et al., CVPR 2022)、**EATA** (Niu et al., ICML 2022)、**RMT** (Döbler et al., CVPR 2023)）普遍遵循后向对齐范式：依赖目标域噪声伪标签的自训练损失，或静态源域代理作为对齐锚点。在连续分布偏移下，这种范式面临根本性瓶颈——监督信号质量随偏移累积而恶化，导致错误累积与灾难性遗忘。**DAS**（Dynamic Style Bridging）提出前向促进范式：通过多级风格桥接机制，将离线构建的合成知识库动态演化至当前目标域风格，使静态语义知识转化为与实时分布协同演化的定制监督信号。图1（Table 6提供符号说明）展示了这一范式转换的核心逻辑。

### 主实验结果

**ImageNet-to-ImageNetC基准**（Table 1）：在最高严重级别（level 5）的在线评估中，DAS将平均分类错误率从Source模型的60.3%降至**44.1%**，显著优于所有对比方法。相比之下，基于扩散模型的**DDA**（Gao et al., CVPR 2023）为46.5%，**SDA**（Yang et al., CVPR 2025）为45.3%，而最新的分布无关方法**DPCore**（Jung et al., ICML 2025）为46.0%。DAS在gaussian noise、shot noise、impulse noise等高噪声场景下优势尤为突出（错误率分别降至17.0%、12.0%、11.3%），验证了合成监督信号在极端分布偏移下的鲁棒性。

**CIFAR基准**（Table 2）：在CIFAR100-to-CIFAR100C上，DAS达到29.8%的平均错误率（Source为44.0%）；在CIFAR10-to-CIFAR10C上达到9.1%（Source为19.2%），均取得最优结果。

**DPCore协议下的公平对比**（Table 8、Table 9）：遵循DPCore的实验协议（相同预训练权重、数据流生成方式），DAS在ImageNet-to-ImageNetC上进一步降至**36.1%**，较Source降低24.2个百分点，较DPCore的40.8%降低4.7个百分点。在CIFAR100-C和CIFAR10-C上同样保持领先。

**语义分割扩展**（Table 10）：在Cityscapes-to-ACDC任务上基于Segformer-B5架构，DAS在四个测试条件（fog、night、rain、snow）下均取得最优mIoU，验证了方法在密集预测任务上的可迁移性。

### 消融实验：多级桥接机制的组件贡献

Table 3通过逐步激活各组件的消融实验揭示了因果机制：

| 配置 | 平均错误率 (%) |
|------|---------------|
| Source-only | 60.3 |
| + 合成知识库（无桥接） | 50.0 |
| + 输入级傅里叶风格注入 | 47.2 |
| + 统计级特征归一化 | 45.8 |
| + 表示级监督对比学习 | **44.1** |

仅引入未桥接的合成知识库即可将错误率从60.3%降至50.0%，证明合成语义信息本身蕴含可靠类别知识。输入级傅里叶幅度谱替换（Eq. 1）和统计级实例归一化（Eq. 2）分别进一步降低2.8和1.4个百分点，表明视觉风格对齐是释放合成知识监督潜力的关键。表示级监督对比学习（Eq. 3）贡献最终1.7个百分点的提升，在特征空间聚合同类跨域样本。

### 生成模型鲁棒性与知识库规模敏感性

**跨生成模型稳定性**（Table 5）：使用BigGAN、Stable Diffusion 1.5、Stable Diffusion 3.0三种不同生成模型构建知识库，DAS分别取得45.0%、44.1%、43.8%的错误率，性能波动极小。这验证了多级桥接机制对生成偏差的解耦能力——即使合成样本存在纹理过拟合等生成伪影（Figure 6可视化揭示了考拉、孔雀等类别的纹理偏差），桥接机制仍能提取可靠语义并抑制偏差影响。

**知识库规模不敏感性**（Figure 4）：每类仅需1个合成样本即可达到优异性能，且对大于2的样本数不敏感。这一特性源于合成样本的语义纯净性（干净背景、显著主体），使得极少量样本即可提供充分类别信息，大幅降低了离线构建的计算开销。

### 效率分析

Figure 3和Table 4对比了各方法的延迟、GPU内存与错误率。DAS在保持最低错误率的同时，相对延迟约为Source模型的1.5倍，GPU内存开销与**CMAE**（Lee et al., CVPR 2024）、**OBAO**（Yang et al., ECCV 2024）相当。关键优势在于：多级桥接的傅里叶变换和统计归一化均为轻量操作，且测试时无需调用扩散模型，离线知识库仅需每类1-2个样本。

### 自训练目标兼容性

Table 7验证了DAS对自训练目标的通用性：无论采用熵最小化还是教师-学生对称交叉熵（Eq. 6），DAS均带来一致且显著的提升。这表明代理交叉熵损失（Eq. 4）提供的合成监督与自训练信号是互补的，而非相互替代。

### 挑战性场景鲁棒性

**混合域TTA**（Table 12）：在混合域场景下（5次运行平均），DAS保持稳定且优于DPCore等SOTA方法。

**类不平衡、CDC、变批量**（Table 13）：在类别不平衡、连续域变化（CDC）以及小批量（batch size=10）等挑战性设置下，DAS均表现鲁棒。这得益于合成知识库提供类别平衡的监督信号，且多级桥接不依赖大批量统计。

**统计可靠性**（Table 11）：5次运行的标准差分析表明DAS的性能波动可控，前向促进范式在随机性下保持稳定。

### 失败模式与局限性

尽管整体表现优异，DAS存在以下局限：

1. **合成数据多样性不足**：合成样本存在类别相关的外观和姿态偏差（如特定类别的纹理过拟合），可能限制对极端域外样本的泛化能力。Figure 6的可视化清晰展示了这一现象。

2. **对生成模型的离线依赖**：虽然测试时无需扩散模型，但知识库质量受限于预训练生成模型的能力和类别覆盖。不同生成模型实验（Table 5）虽显示鲁棒性，但BigGAN在ImageNet-1K上的类别覆盖天然受限。

![[assets/figures/papers/paper_list_l1057_https_arxiv_org_abs_2605_18608/figures/010_Table_5.jpg]]
*Table 5: Quantitative results using different generative models*

3. **密集预测任务的扩展限制**：在语义分割中，当前方法依赖外部合成数据集（UrbanSyn），无法直接利用文本到图像模型生成像素级标签，限制了方法的端到端可扩展性。

![[assets/figures/papers/paper_list_l1057_https_arxiv_org_abs_2605_18608/figures/004_Table_2.jpg]]
*Table 2: Comparison results of standard CIFAR100-to-CIFAR100C and CIFAR10-to-CIFAR10C CTTA tasks. We report the mean classification error rate (%, lower is better) across all 15 corrupted domains. All results are evaluated with the largest corruption severity level 5 in an online manner. Bold text indicates the best performance*

![[assets/figures/papers/paper_list_l1057_https_arxiv_org_abs_2605_18608/figures/006_Table_3.jpg]]
*Table 3: Ablation experiments on the standard ImageNet-to-ImageNetC CTTA task. Each component of our framework is progressively activated to analyze its contribution*

![[assets/figures/papers/paper_list_l1057_https_arxiv_org_abs_2605_18608/figures/009_Figure_4.jpg]]
*Figure 4: Ablation study on the size of the knowledge base*

## 定位与知识库关联

### 范式转换：从后向对齐到前向促进

现有持续测试时自适应（CTTA）方法主要围绕**后向对齐范式**展开，其核心思路是构建一个静态的源域代理或合成锚点，将不断偏移的目标分布“拉回”到已知空间。代表性工作包括：

- **TENT**（Wang et al., ICLR 2021）：通过熵最小化在测试时更新批归一化层参数，但缺乏对分布偏移的结构化建模，在连续偏移下易产生错误累积。
- **CoTTA**（Wang et al., CVPR 2022）：引入教师-学生框架和随机恢复机制以缓解遗忘，但教师模型的更新仍依赖目标域噪声伪标签，监督信号质量随偏移加剧而退化。
- **EATA**（Niu et al., ICML 2022）：通过样本选择与抗遗忘正则化提升效率，但其依赖的源域代理是固定锚点，无法随分布演化。
- **RMT**（Döbler et al., CVPR 2023）：采用记忆库回放机制，但回放样本来自历史目标域，同样受噪声伪标签影响。
- **CMAE**（Lee et al., CVPR 2024）：利用对比学习增强特征判别性，但仍以目标域自监督信号为主，缺乏可靠的类别级真值监督。
- **OBAO**（Yang et al., ECCV 2024）：通过在线批量聚合优化伪标签质量，本质上仍是对目标域噪声信号的再加工。
- **DPCore**（Jung et al., ICML 2025）：提出分布无关的核心集选择策略，在协议层面做了统一，但监督范式未发生根本改变。

上述方法的**共同瓶颈**在于：监督信号来源始终受限于目标域自身的噪声伪标签或静态源域代理，在连续分布偏移下无法提供稳定、可靠的类别级监督，导致错误累积与灾难性遗忘。

DAS 提出的**前向促进范式**从根本上改变了这一逻辑：不再试图将目标分布“拉回”源域，而是让合成知识**随分布共同演化**，将静态的语义纯净知识动态转化为与当前目标域风格对齐的按需监督信号。这一转变使得监督信号的可靠性不再依赖于目标域自身的噪声估计，而是建立在语义明确、标签真实的合成代理之上。

### 与基于扩散模型的 TTA 方法的区别

近年来，扩散模型被引入测试时自适应领域，形成了两条技术路线：

- **DDA**（Gao et al., CVPR 2023）：利用扩散模型对目标样本进行去噪，将损坏图像恢复至干净状态后再进行分类。该方法在每次自适应时都需要运行扩散模型的反向过程，计算开销极大，且去噪过程可能引入额外的生成伪影。
- **SDA**（Yang et al., CVPR 2025）：将目标样本投影至合成域，在合成域中进行分类。该方法同样依赖测试时的扩散模型推理，且投影过程可能丢失目标域的关键分布信息。

DAS 与上述方法的**本质区别**在于：扩散模型仅在**离线阶段**用于构建知识库，测试时无需任何生成模型推理。通过多级风格桥接机制（输入级傅里叶频谱替换、统计级实例归一化、表示级监督对比学习），合成知识库被动态适配到当前目标域风格，从而在保持低计算开销的同时，解耦了可靠的语义内容与固有的生成偏差。

### 适用边界与局限

**适用场景**：
- 分类任务的持续分布偏移场景（ImageNet-C、CIFAR-C 等标准基准）
- 混合域偏移、类不平衡、小批量等挑战性设置（Table 12、Table 13 验证了鲁棒性）
- 语义分割的域适应（Cityscapes-to-ACDC，Table 10），但目前仅能利用外部合成数据集（UrbanSyn），无法直接使用文本到图像模型生成像素级标签

**已知局限**：
1. **合成数据缺乏多样性**：知识库中的合成样本存在类别相关的外观和姿态偏差，特定类别（如考拉、孔雀）存在纹理过拟合等强生成偏差，可能限制泛化能力。尽管桥接机制在多种生成模型（BigGAN、SD 1.5、SD 3.0）下性能稳定（Table 5），但语义多样性的根本限制仍存在。
2. **对预训练生成模型的依赖**：离线知识库的构建依赖于预训练扩散模型的质量和类别覆盖。若生成模型对某些类别生成质量较差，知识库的语义纯净度将受到影响。
3. **密集预测任务的扩展限制**：在语义分割等像素级任务中，当前方法无法直接利用文本到图像模型生成带有像素级标签的合成数据，需要依赖外部合成数据集，限制了方法的通用性。

### 开放问题

1. **轻量化知识构建**：能否开发更轻量或无需生成模型的知识构建方式，降低对大规模扩散模型的依赖？例如，利用原型网络或数据增强技术构建类别代理。
2. **像素级扩展**：如何将动态风格桥接扩展到像素级半监督或自监督场景，直接利用文本到图像模型生成分割掩码？这需要解决生成模型的空间对齐和像素级标注问题。
3. **无终止长时适应**：在无终止的长时持续适应中，合成知识库或桥接机制是否会累积偏差并导致灾难性遗忘？当前方法在标准 CTTA 基准（15 种损坏类型循环）上表现稳定，但更长时间尺度的行为尚待研究。
4. **跨任务泛化**：前向促进范式能否推广到目标检测、实例分割等更复杂的视觉任务？这需要重新设计知识库构建和桥接机制的粒度。

## 原文 PDF

![[paperPDFs/CVPR_2026/Dance_Across_Shifts_Forward_Facilitation_Continual_Test_Time_Adaptation_through_Dynamic_Style_Bridging.pdf]]
