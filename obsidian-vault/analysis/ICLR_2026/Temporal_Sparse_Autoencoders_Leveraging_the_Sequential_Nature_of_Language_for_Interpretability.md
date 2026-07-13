---
title: "Temporal Sparse Autoencoders: Leveraging the Sequential Nature of Language for Interpretability"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Temporal_Sparse_Autoencoders_Leveraging_the_Sequential_Nature_of_Language_for_Interpretability.pdf
project_link: null
code_link: null
openreview_forum_id: bojVI4l9Kn
aliases:
- TSATS
- TSALSNLI
tags:
- ICLR_2026
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/representation_learning
core_operator: "在训练中引入时间对比损失，强制高层特征在相邻令牌上保持激活一致性，同时让低层特征拟合残差，实现语义与句法的自监督分离。"
primary_logic: "语言数据中高级语义变量具有时间平稳性（相邻令牌共享语义），而低级句法变量具有局部性；将该先验嵌入字典学习，可无监督地使SAE解耦语义与句法特征。"
claims:
- "在语义和上下文的探测任务上，T-SAEs显著优于现有SAEs。"
- "T-SAE高层特征在长序列上展现出清晰的语义阶段转换，而Matryoshka特征噪声较多且跨序列一致激活。"
- "T-SAEs在保持重构质量的同时，其高层特征更平滑且具有更好的自动可解释性。"
- "在模型操控任务中，T-SAE的高层特征帕累托支配现有SAE，能改变语义同时保持连贯性。"
---

# Temporal Sparse Autoencoders: Leveraging the Sequential Nature of Language for Interpretability

> [!tip] 核心洞察
> 语言数据中高级语义变量具有时间平稳性（相邻令牌共享语义），而低级句法变量具有局部性；将该先验嵌入字典学习，可无监督地使SAE解耦语义与句法特征。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 时序稀疏自编码器：利用语言的序列性质实现可解释性 |
| 英文题名 | Temporal Sparse Autoencoders: Leveraging the Sequential Nature of Language for Interpretability |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=bojVI4l9Kn) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/representation_learning |
| Method | Temporal Sparse Autoencoders (T-SAEs) |
| Dataset | Pythia-160m (Pile), Gemma2-2b (Pile) |

> [!tip] 效果简介
> - Pythia-160m (Pile) 上，FVE 为 0.94，对比 0.95 (Matryoshka)，变化 -0.01。
> - Pythia-160m (Pile) 上，Smoothness (High) 为 0.09，对比 0.12 (Matryoshka)，变化 -0.03。
> - Gemma2-2b (Pile) 上，FVE 为 0.75，对比 0.75 (Matryoshka)，变化 0.00。

## 概要

### 问题背景

当前主流稀疏自编码器（Sparse Autoencoders, SAEs）在从语言模型激活中恢复可解释特征时，普遍忽视语言序列的时间结构。语言生成本质上是时序过程：高层语义变量（如主题、意图）在相邻令牌间保持平稳，而低层句法变量（如词性、局部搭配）则逐令牌快速变化。现有SAE将每个令牌的表示独立编码，导致恢复的特征空间被局部句法噪声主导，难以捕捉平滑变化的高层语义概念——这正是可解释性研究最关心的对象。

### 核心方法

**时序稀疏自编码器（Temporal Sparse Autoencoders, T-SAEs）** 将上述时间平稳性先验嵌入字典学习框架，实现语义与句法特征的自监督分离。其核心设计包括三个关键组件：

1. **特征空间显式划分**：将SAE的隐空间按维度切分为高层特征（前20%）和低层特征（后80%），为后续分工奠定结构基础。
2. **分层重构目标**：高层特征负责重构原始输入，低层特征负责拟合高层重构后的残差——这迫使高层特征捕获信号的主要成分，低层特征补充局部细节。
3. **时间对比损失**：仅施加于高层特征，鼓励相邻令牌的高层表征在余弦相似度上彼此靠近，同时将批次内其他样本作为负例推开。该损失使高层特征在序列上保持激活一致性，自然涌现出语义级别的平滑表征。

整体训练目标结合了分层重构损失与时间对比损失，仅通过一个超参数 $\alpha$ 平衡二者。

### 方法定位

T-SAEs 在方法谱系上处于**结构化字典学习**与**自监督表征解耦**的交汇点。与标准 BatchTopK SAE 相比，它引入了时间维度上的归纳偏置；与 Matryoshka SAE 相比，它在分层重构的基础上进一步通过对比损失强制高层特征的时序一致性。不同于需要外部标注的探测方法，T-SAEs 的解耦完全由数据生成过程的先验驱动，无需语义或句法标签。

### 核心结论

实验证据表明，T-SAEs 在保持与现有 SAE 相当的重构质量（FVE 指标差异不超过 0.01）的前提下，实现了显著的语义-句法解耦：

- **语义与上下文恢复**：在 Gemma2-2b 的探测任务中，T-SAE 高层特征在语义标签和上下文标签上的探测准确率显著优于 Matryoshka SAE 和 BatchTopK SAE（Figure 3）。t-SNE 可视化进一步显示，高层特征按语义类别和序列上下文形成清晰聚类，而低层特征则按词性聚集（Figure 2）。
- **序列语义阶段检测**：在拼接多种文本的长序列上，T-SAE 最活跃的 8 个特征展现出清晰的语义阶段转换，而 Matryoshka 特征则噪声较大且跨序列一致激活（Figure 4, Figure 1）。
- **平滑性提升**：高层特征的平滑度指标（Lipschitz、Fourier、Wavelet、多尺度）均优于基线，证实了时间对比损失的有效性（Table 1, Table 9）。
- **模型操控能力**：在操控实验中，T-SAE 高层特征帕累托支配基线：能在改变生成语义的同时保持文本连贯性，而 Matryoshka SAE 则因特征过于局部而导致灾难性的令牌重复（Figure 5, Table 7）。

### 局限与展望

当前 T-SAE 仅探索了单层高低特征划分，未建模多层时间层次结构（如文档-段落-句子-词）。时间对比损失增加了计算开销，在相同内存预算下需减小批次大小。此外，高层特征在不同语义区域间存在一定泄漏，吸收指标（absorption）略高于 Matryoshka 但仍在可接受范围。未来方向包括：将多层时间层次显式纳入训练、探索更适合非负稀疏特征的对比损失形式，以及将该框架拓展到视频、语音等其他序列模态。

### 语言模型可解释性中的稀疏自编码器

大型语言模型的内部表征高度叠加，单个神经元往往对多个不相关概念同时响应，这为理解模型决策机制带来了根本性挑战。稀疏自编码器（Sparse Autoencoders, SAEs）通过将稠密的模型激活分解为一组稀疏、可解释的特征，已成为当前主流的一类无监督可解释性工具。其核心思路是训练一个过完备的字典，使得少量活跃特征即可高保真地重构原始表征，从而将“叠加”的隐空间解耦为更易理解的单义特征。

### 现有SAE的结构性盲区：忽视语言的时序属性

尽管现有SAE在特征提取和重构质量上取得了显著进展，但它们存在一个共同的结构性盲区：**将语言序列中的每个token视为独立样本，完全忽视了语言天然的时序结构**。这一设计选择与语言本身的生产过程存在根本性张力——人类在生成语言时，高层语义变量（如主题、意图、上下文）在相邻token之间具有时间平稳性，而低层句法变量（如词性、局部搭配）则在token级别快速变化。

该盲区直接导致现有SAE恢复的特征存在严重的质量偏差。实验证据表明，无论是标准的**BatchTopK SAE**还是分层设计的**Matryoshka SAE**，其提取的特征大多为局部句法噪声，难以捕捉平滑变化的高层语义概念。在跨语义段落的拼接文本上，Matryoshka SAE的特征激活几乎在每个token上都剧烈波动，无法清晰呈现语义阶段的转换（Figure 1）。这一缺陷从根本上限制了SAE在语义理解、模型操控等下游任务中的实用价值。

### 核心洞察：将时序先验嵌入字典学习

本工作基于一个简洁而深刻的洞察：**语言数据中高级语义变量具有时间平稳性（相邻token共享语义），而低级句法变量具有局部性；将该先验显式嵌入字典学习过程，可使SAE在无监督条件下自驱动地解耦语义与句法特征**。

具体而言，作者将语言生成过程形式化为一个包含高层隐变量 $\mathbf{h}_t$（语义/上下文）和低层隐变量 $\mathbf{l}_t$（句法/词选择）的生成模型，其中高层变量满足 $\|g(\mathbf{h}_t, \mathbf{0}) - \mathbf{x}_t\| \leq \epsilon$，即仅凭高层变量已可近似重构输入，低层变量则拟合残差。基于此框架，本文提出**时序稀疏自编码器（Temporal Sparse Autoencoders, T-SAEs）**，通过在训练中引入时间对比损失，强制高层特征在相邻token上保持激活一致性，同时让低层特征自动拟合高层重构后的残差，实现语义与句法的自监督分离。

### 本文动机与研究问题

本文的核心动机在于弥补现有SAE对语言时序结构的系统性忽视，探索以下关键问题：
- 能否通过简单的时序对比约束，使SAE在保持重构质量的同时，自发地将特征空间解耦为语义和句法两个功能层次？
- 这种解耦能否在语义探测、上下文识别、模型操控等下游任务中带来可验证的性能提升？
- 时序先验的引入是否会带来新的特征泄漏或计算开销问题？

通过系统的实验设计和多维度评估，本文旨在为“将结构化先验嵌入字典学习”这一方向提供原理验证和实用基准。

## 核心方法与创新机理

Temporal Sparse Autoencoders (T-SAEs) 的核心创新在于将语言序列的**时间平稳性先验**显式嵌入稀疏自编码器的字典学习过程，从而在无监督条件下实现语义特征与句法特征的解耦。这一设计直击现有 SAE 的瓶颈：忽视序列的时间结构，导致恢复的特征以局部、句法噪声为主，难以捕捉平滑变化的高层语义概念。

### 创新一：特征空间的显式层级划分

T-SAEs 将 SAE 的特征空间**显式划分为高层特征（前 20% 维度）和低层特征（后 80% 维度）**（Section 3.2）。这与 Matryoshka SAE 的层级重构损失形成对比——后者虽也使用高低层重构，但并未从语义/句法分离的角度对特征空间进行结构性划分。T-SAEs 的划分建立在语言生成过程的建模之上：高层隐变量 $\mathbf{h}_t$ 编码语义等全局信息，具有时间不变性；低层隐变量 $\mathbf{l}_t$ 编码句法等局部信息，随 token 快速变化（Section 3.1）。该建模假设可形式化为：

$$\boldsymbol{\tau}_t = \phi(\tau^{t-1}, \mathbf{h}_t, \mathbf{l}_t)$$

其中高层变量能够以较小误差 $\epsilon$ 重构模型表示，但低层变量包含额外的残差信号：$0 = \|g(\mathbf{h}_t, \mathbf{l}_t) - \mathbf{x}_t\| \leq \|g(\mathbf{h}_t, \mathbf{0}) - \mathbf{x}_t\| \leq \epsilon$。

### 创新二：时间对比损失驱动的语义一致性约束

在训练目标上，T-SAEs 在 Matryoshka 重构损失的基础上引入了**时间对比损失 $\mathcal{L}_{\mathrm{contr}}$**，且该损失**仅施加于高层特征**（Section 3.2）。其核心机制是：将相邻 token 对 $(t, t-1)$ 的高层表征 $\mathbf{z}_t = \mathbf{W}_{0:h}^{\mathrm{enc}} \mathbf{x}_t$ 视为正样本，批次内其他样本作为负样本，通过对称对比损失强制高层特征在相邻 token 上保持激活一致性：

$$\mathcal{L} = \sum_{i=1}^N \mathcal{L}_{\mathrm{matr}}(\mathbf{x}_t^{(i)}) + \alpha \mathcal{L}_{\mathrm{contr}}$$

$$\mathcal{L}_{\mathrm{contr}} = -\frac{1}{N} \sum_{i=1}^N \log \frac{\exp(s(\mathbf{z}_t^{(i)}, \mathbf{z}_{t-1}^{(i)}))}{\sum_{j=1}^N \exp(s(\mathbf{z}_t^{(i)}, \mathbf{z}_{t-1}^{(j)}))} - \frac{1}{N} \sum_{j=1}^N \log \frac{\exp(s(\mathbf{z}_t^{(j)}, \mathbf{z}_{t-1}^{(j)}))}{\sum_{i=1}^N \exp(s(\mathbf{z}_t^{(i)}, \mathbf{z}_{t-1}^{(j)}))}$$

这一设计的因果机制清晰：对比损失迫使高层特征学习跨 token 稳定的表示，从而自然捕获语义和上下文信息；而低层特征不受此约束，仅通过 Matryoshka 损失中的残差拟合项 $\mathcal{L}_L$ 自动捕获高层重构后的局部波动，从而自监督地实现语义与句法的分离。

### 创新三：对比采样策略的灵活性

T-SAEs 默认使用相邻 token $(t, t-1)$ 作为对比正样本，但该设计具备可扩展性。消融实验（Table 2）表明，**将正样本替换为随机历史 token** 可进一步提升上下文探测性能（+0.11），但会降低句法性能（-0.10）。这揭示了对比采样窗口长度在高层次语义与低层次句法特征学习之间的权衡关系，为任务特定的优化提供了调节旋钮。此外，消融实验证实，若将对比损失替换为简单的 L2 距离损失 $\ell_i = \alpha \|\mathbf{z}_t^{(i)} - \mathbf{z}_{t-1}^{(i)}\|_2^2$，语义和上下文性能会显著下降（语义 -0.07，上下文 -0.1），说明对比形式的必要性。

### 与基线方法的关键差异总结

| 设计维度 | BatchTopK SAE | Matryoshka SAE | **T-SAEs** |
|---------|--------------|----------------|-----------|
| 特征空间划分 | 无划分 | 隐式层级（仅重构损失分层） | **显式语义/句法划分（20/80）** |
| 训练目标 | 重构 + 稀疏性 | 重构 + 稀疏性 + 层级重构 | **重构 + 稀疏性 + 层级重构 + 时间对比损失** |
| 时序建模 | 无 | 无 | **对比损失强制高层特征时间一致性** |
| 语义-句法解耦 | 无机制 | 弱（依赖层级重构） | **强（时间先验 + 残差拟合自监督分离）** |

这些创新的综合效果在实验中得到了系统性验证：T-SAE 高层特征在语义和上下文探测任务上显著优于基线（Figure 3），在长序列上展现出清晰的语义阶段转换（Figure 4），且在模型操控任务中帕累托支配现有 SAE，能在改变语义的同时保持生成连贯性（Figure 5）。

### 设计动机与核心思路

现有稀疏自编码器（SAE）在训练时仅依赖重构损失与稀疏性损失，将语言模型中每个 token 的激活视为独立样本，完全忽略了语言序列的时间结构。这一设计导致 SAE 恢复的特征以局部、句法噪声为主，难以捕捉平滑变化的高层语义概念。T-SAEs 的核心洞察在于：**语言数据中高级语义变量具有时间平稳性（相邻 token 共享语义），而低级句法变量具有局部性**。将该先验嵌入字典学习过程，可在无监督条件下实现语义与句法特征的解耦。

### 整体 Pipeline

T-SAEs 的整体框架由五个核心模块构成，数据流从语言模型隐藏状态出发，经编码器映射到稀疏特征空间，再通过显式的特征空间划分与多目标损失实现语义-句法分离，最终由解码器完成重构。

**模块 1：Encoder（$W^{enc}, b^{enc}$）**
将语言模型在位置 $t$ 的激活 $x_t$ 映射到稀疏特征空间：
$$\mathbf{f}(x_t) = \sigma(W^{enc} x_t + b^{enc})$$
其中 $\sigma$ 为 ReLU 激活函数，保证特征的非负稀疏性。

**模块 2：特征空间划分**
将编码器输出的 $m$ 维特征向量显式划分为两部分：前 $h$ 个维度为**高层特征** $f_{0:h}(x_t)$，后 $m-h$ 个维度为**低层特征** $f_{h:m}(x_t)$。默认采用 20/80 划分比例，即高层特征占 20%，低层特征占 80%（Section 4.1）。这一划分是后续所有损失函数设计的基础。

**模块 3：高层特征重构模块（$W^{dec}_{0:h}$）**
仅使用高层特征进行重构，计算高层重构损失：
$$\mathcal{L}_H = \| x_t - W^{dec}_{0:h} f_{0:h}(x_t) + b^{dec} \|_2^2$$
该损失强制高层特征承载足以近似原始输入的信息，从而捕获语义层面的表征。

**模块 4：低层特征残差拟合模块**
低层特征自动拟合高层重构后的残差，计算完整重构损失：
$$\mathcal{L}_L = \| x_t - W^{dec} f(x_t) + b^{dec} \|_2^2$$
由于高层特征已承担主要重构任务，低层特征自然被迫捕获高层无法解释的局部波动——即句法、词汇选择等低层信息。这一设计源自 Matryoshka SAE 的层级分解思路，但 T-SAEs 在此基础上增加了时间对比约束。

**模块 5：时间对比损失模块**
这是 T-SAEs 的核心创新。对高层特征 $z_t = W^{enc}_{0:h} x_t$ 施加对称对比损失，鼓励相邻 token 的高层表征相似：
$$\mathcal{L}_{contr} = -\frac{1}{N}\sum_{i=1}^N \log \frac{\exp(s(z_t^{(i)}, z_{t-1}^{(i)}))}{\sum_{j=1}^N \exp(s(z_t^{(i)}, z_{t-1}^{(j)}))} - \frac{1}{N}\sum_{j=1}^N \log \frac{\exp(s(z_t^{(j)}, z_{t-1}^{(j)}))}{\sum_{i=1}^N \exp(s(z_t^{(i)}, z_{t-1}^{(j)}))}$$
其中 $s(\cdot,\cdot)$ 为余弦相似度。默认正样本为相邻 token 对 $(t, t-1)$，批次内其他样本作为负样本。对比损失仅作用于高层特征，低层特征不受此约束，从而保持其对局部变化的敏感性。

**总损失函数**为上述模块的组合：
$$\mathcal{L} = \sum_{i=1}^N \mathcal{L}_{matr}(x_t^{(i)}) + \alpha \mathcal{L}_{contr}$$
其中 $\mathcal{L}_{matr} = \mathcal{L}_H + \mathcal{L}_L$，$\alpha$ 为时间对比损失的正则化系数，默认取 1.0（Section 4.1）。

### 输入输出流

- **输入**：语言模型在序列位置 $t$ 的隐藏状态 $x_t \in \mathbb{R}^d$。
- **编码**：经 $W^{enc}$ 映射为稀疏特征 $f(x_t) \in \mathbb{R}^m$。
- **特征划分**：前 $h$ 维为高层特征，后 $m-h$ 维为低层特征。
- **重构**：高层特征单独重构 $\hat{x}_H$，完整特征重构 $\hat{x}$。
- **损失计算**：$\mathcal{L}_H$ 衡量高层重构质量，$\mathcal{L}_L$ 衡量完整重构质量，$\mathcal{L}_{contr}$ 约束高层特征的时间一致性。
- **输出**：训练完成后的 SAE 特征空间，其中高层特征捕获语义与上下文，低层特征捕获句法信息。

### 与基线的关键差异

| 设计维度 | BatchTopK SAE | Matryoshka SAE | T-SAEs |
|---------|--------------|----------------|--------|
| 特征空间划分 | 无划分 | 隐式层级（通过不同维度重构） | 显式划分为高层/低层（20/80） |
| 训练目标 | 重构损失 + 稀疏性损失 | 高层重构 + 完整重构 | 增加时间对比损失（仅作用于高层） |
| 对比采样 | 无 | 无 | 默认相邻 token 对 $(t, t-1)$，可扩展为随机历史 token |

Matryoshka SAE 已具备层级分解能力（高层特征重构输入、低层特征重构残差），但由于缺乏时间约束，其高层特征仍以句法噪声为主（Figure 1, Figure 8）。T-SAEs 通过时间对比损失将“语义平稳性”先验注入高层特征的学习过程，使语义与句法的分离从偶然变为必然。

### 数据生成过程与层次化假设

T-SAE 的设计建立在一个简化的语言数据生成过程之上。假设说话者根据历史上下文 $\tau^{t-1}$、高层隐变量 $\mathbf{h}_t$ 和低层隐变量 $\mathbf{l}_t$ 生成当前 token：

$$\boldsymbol{\tau}_t = \phi(\tau^{t-1}, \mathbf{h}_t, \mathbf{l}_t)$$

其中，高层变量 $\mathbf{h}_t$ 编码语义、主题等时间平稳的全局信息，低层变量 $\mathbf{l}_t$ 编码句法、词选择等局部波动信息。模型隐藏状态 $\mathbf{x}_t$ 被假设为这两个隐变量的函数 $g(\mathbf{h}_t, \mathbf{l}_t)$，且满足层次重构约束：

$$0 = \| g(\mathbf{h}_t, \mathbf{l}_t) - \mathbf{x}_t \| \leq \| g(\mathbf{h}_t, \mathbf{0}) - \mathbf{x}_t \| \leq \epsilon$$

即高层变量可近似重构 $\mathbf{x}_t$（误差在 $\epsilon$ 内），而低层变量提供额外的残差信号。这一先验直接驱动了后续的特征空间划分与损失函数设计。

### 核心模块：特征空间划分与层级重构

T-SAE 在标准稀疏自编码器架构上引入显式的特征空间划分。给定编码器输出 $\mathbf{f}(\mathbf{x}_t) = \sigma(\mathbf{W}^{\mathrm{enc}} \mathbf{x}_t + \mathbf{b}^{\mathrm{enc}})$，将前 $h$ 维指定为高层特征 $\mathbf{f}_{0:h}(\mathbf{x}_t)$，后 $m-h$ 维为低层特征 $\mathbf{f}_{h:m}(\mathbf{x}_t)$。默认比例为 20/80。

重构采用 Matryoshka 风格的层级损失，使高层特征负责重构原始输入，低层特征自动拟合残差：

$$\mathcal{L}_{\mathrm{matr}}(\mathbf{x}_t) = \mathcal{L}_H + \mathcal{L}_L$$

$$\mathcal{L}_H = \| \mathbf{x}_t - \mathbf{W}_{0:h}^{\mathrm{dec}} \mathbf{f}_{0:h}(\mathbf{x}_t) + \mathbf{b}^{\mathrm{dec}} \|_2^2$$

$$\mathcal{L}_L = \| \mathbf{x}_t - \mathbf{W}^{\mathrm{dec}} \mathbf{f}(\mathbf{x}_t) + \mathbf{b}^{\mathrm{dec}} \|_2^2$$

这一设计形成自监督的语义-句法分离机制：高层特征被迫捕获足以近似完整输入的信息（语义），低层特征则自然吸收高层无法解释的局部波动（句法）。

### 核心模块：时间对比损失

T-SAE 的关键创新在于对高层特征施加时间对比损失。令 $\mathbf{z}_t = \mathbf{W}_{0:h}^{\mathrm{enc}} \mathbf{x}_t$ 为高层表征，采用对称的批次内对比形式：

$$\mathcal{L}_{\mathrm{contr}} = -\frac{1}{N} \sum_{i=1}^{N} \log \frac{\exp(s(\mathbf{z}_t^{(i)}, \mathbf{z}_{t-1}^{(i)}))}{\sum_{j=1}^{N} \exp(s(\mathbf{z}_t^{(i)}, \mathbf{z}_{t-1}^{(j)}))} - \frac{1}{N} \sum_{j=1}^{N} \log \frac{\exp(s(\mathbf{z}_t^{(j)}, \mathbf{z}_{t-1}^{(j)}))}{\sum_{i=1}^{N} \exp(s(\mathbf{z}_t^{(i)}, \mathbf{z}_{t-1}^{(j)}))}$$

其中 $s(\cdot, \cdot)$ 为余弦相似度。该损失以相邻 token 对 $(t, t-1)$ 作为正样本、批次内其他样本作为负样本，强制高层特征在时间上保持激活一致性。这一设计直接编码了“语义变量具有时间平稳性”的核心洞察。

总损失函数为：

$$\mathcal{L} = \sum_{i=1}^{N} \mathcal{L}_{\mathrm{matr}}(\mathbf{x}_t^{(i)}) + \alpha \mathcal{L}_{\mathrm{contr}}$$

其中 $\alpha$ 为时间损失的正则化系数，所有实验中使用 $\alpha = 1.0$。

### 消融中的对比变体

消融实验验证了对比形式的关键性。将对比损失替换为朴素的逐样本 L2 时间相似性损失 $\ell_i = \alpha \| \mathbf{z}_t^{(i)} - \mathbf{z}_{t-1}^{(i)} \|_2^2$，会导致语义和上下文探测性能显著下降（语义 -0.07，上下文 -0.1），尽管重构 FVE 略有提升（+0.01）。这表明批次内对比的判别性形式对于分离语义特征至关重要。

此外，将对比的正样本从固定的 $t-1$ token 改为随机历史 token，可提升上下文探测性能（+0.11）但降低句法性能（-0.10），揭示了对比采样策略对特征分布的直接调控作用。

### 平滑度量化指标

为量化特征的时间平稳性，T-SAE 引入平滑度指标。对每个特征 $i$ 在序列上的最大归一化波动定义为：

$$\Delta_s = \frac{1}{n'} \sum_{i=1}^{n'} \max_{t \in [1...T]} |\mathbf{f}_i(\mathbf{x}_t) - \mathbf{f}_i(\mathbf{x}_{t-1})| / \|\mathbf{x}_t - \mathbf{x}_{t-1}\|_2$$

整体平滑度得分为多个序列的平均：

$$S = \frac{1}{n} \sum_{s}^{n} \Delta_s$$

该指标衡量特征激活相对于模型隐层变化的波动程度，值越低表示特征越平滑。实验表明 T-SAE 高层特征的平滑度显著优于 Matryoshka SAE（Pythia-160m 上：0.09 vs 0.12；Gemma2-2b 上：0.10 vs 0.15）。

## 实验与关键发现

### 核心性能评估

T-SAEs在保持重构质量的前提下，显著提升了高层特征的平滑度和可解释性。表1汇总了在Pythia-160m和Gemma2-2b两个模型上的核心指标对比。

![[assets/figures/papers/paper_list_l20_https_openreview_net_forum_id_bojVI4l9Kn/figures/006_Table_1.jpg]]
*Table 1: Core Performance Metrics. We report smoothness on feature splits when applicable and standard deviations for autointerpretability scores*

在Pythia-160m上，T-SAE的FVE达到0.94，与Matryoshka SAE（0.95）基本持平；在Gemma2-2b上两者均为0.75，表明时序对比损失的引入并未损害重构能力。关键的差异体现在平滑度指标上：T-SAE的高层特征平滑度在Pythia-160m上为0.09，低于Matryoshka的0.12；在Gemma2-2b上为0.10，显著低于Matryoshka的0.15。平滑度越低，说明特征在相邻token间的激活变化越小，即高层特征成功捕获了时间上稳定的语义信息。

自动可解释性得分方面，T-SAE同样表现出优势，且标准差更小，说明其高层特征的语义一致性更好。多尺度平滑度分析（表9）进一步从Lipschitz、Fourier、Wavelet等多个角度验证了这一趋势：T-SAE的高层特征在所有尺度上均比低层特征和基线更平滑。

![[assets/figures/papers/paper_list_l20_https_openreview_net_forum_id_bojVI4l9Kn/figures/021_Table_9.jpg]]
*Table 9: Lipschitz, Fourier, Wavelet, and Multiscale smoothness metrics across high and low splits*

### 语义与句法的自监督分离

T-SAE的核心设计目标是实现语义与句法特征的无监督解耦。图2的t-SNE可视化直观展示了这一效果：在Pythia-160m的MMLU问题上，T-SAE高层特征的激活按问题类别（语义）和问题编号（上下文）形成清晰聚类，而低层特征则按词性（句法）聚类。相比之下，Matryoshka SAE和BatchTopK SAE的特征主要反映句法信息，语义聚类能力较弱。

探测任务（图3）提供了定量证据。在Gemma2-2b上，T-SAE在语义标签和上下文标签的探测准确率上显著优于所有基线SAE，尤其在稀疏探测设置下优势更加明显。当仅使用少量特征时，T-SAE的高层特征能以更高精度恢复语义类别和序列上下文信息。这一优势在Pythia-160m的三个数据集（FineFineWeb、MMLU、Wikipedia）上同样成立（图11），在Wikipedia和FineFineWeb上的Gemma2-2b实验（图10）也验证了跨数据分布的鲁棒性。

图7进一步将探测结果按高低层分割展示：T-SAE的高层特征在语义和上下文探测上远优于其低层特征，而低层特征在句法探测上表现更好，形成清晰的“高层-语义/上下文、低层-句法”分工。Matryoshka SAE的高低层分割则没有这种明确的功能分化。

### 序列级语义转移检测

图4展示了T-SAE在拼接文本上的特征激活模式。当输入序列由三段不同语义的文本（牛顿《原理》、MMLU遗传学问题、《薄伽梵歌》）拼接而成时，T-SAE最活跃的8个高层特征展现出清晰的阶段转换——每个特征仅在语义相关的段落内激活，段落边界处激活强度发生突变。特征的自动解释标签（如“mathematical physics”、“genetics and heredity”、“spiritual and religious texts”）与对应段落的真实语义高度吻合。

相比之下，基线SAE的特征（图8）要么在整个序列上持续激活、无法区分语义段落，要么噪声极大、在几乎每个token上都波动。这一对比直接验证了时序对比损失的有效性：通过强制相邻token的高层特征保持一致，T-SAE学会了忽略局部的句法波动，仅在有语义变化时才调整特征激活。

### 模型操控与可解释性应用

在HH-RLHF偏好数据集上，T-SAE展现出更强的可解释性价值（图5左）。Matryoshka SAE发现的特征较为随机，而T-SAE能捕获与安全性相关的特征。同时，T-SAE还揭示了数据集中存在的虚假长度相关性：被拒绝的回答通常比被偏好的回答更长，且“transition words and phrases”和“legal and formal language”等特征在被拒绝回答上的激活显著更高（表3-5）。图6进一步显示，语义相关特征与长度差异的相关性较低，而虚假特征与长度差异高度相关，说明T-SAE有助于区分真正的偏好信号和数据伪影。

![[assets/figures/papers/paper_list_l20_https_openreview_net_forum_id_bojVI4l9Kn/figures/011_Table_3.jpg]]
*Table 3: Chosen and rejected examples with maximal difference (rejected−chosen) in feature activations for feature transition words and phrases. In all cases, the rejected example is much longer*

在模型操控任务中（图5右），T-SAE的高层特征帕累托支配现有SAE。以医学和文学特征为例（表7），T-SAE在不同操控强度下都能成功改变生成文本的语义，同时保持连贯性；而Matryoshka SAE需要精确调整操控强度，且容易因特征的局部性而灾难性地重复token。

![[assets/figures/papers/paper_list_l20_https_openreview_net_forum_id_bojVI4l9Kn/figures/016_Table_7.jpg]]
*Table 7: Examples of steering with medical and literature features. T-SAEs respond to high-level feature steering at various strengths and properly change the semantics of generation while retaining coherence. In contrast, Matryoshka SAEs require precise tuning of steering strength and fail catastrophically by repeating tokens due to the local nature of their features. Outputs are colored green if they achieve at least a score of 2 (out of 3) for both intervention success and coherence*

### 消融实验

表2报告了在Pythia-160m上的消融结果，揭示了几个关键设计选择的影响：

![[assets/figures/papers/paper_list_l20_https_openreview_net_forum_id_bojVI4l9Kn/figures/010_Table_2.jpg]]
*Table 2: Difference in performance between ablation and normal Pythia-160m Temporal SAEs*

**高层/低层特征比例**：将比例从默认的20/80调整为10/90后，语义性能略微下降（-0.01），但句法性能提升（+0.01），上下文性能也有改善（+0.01）。这说明更小的高层特征比例迫使模型将更多语义信息压缩到更少的维度中，同时为句法特征腾出更多容量。

**对比采样策略**：用随机历史token替代固定的t-1作为正样本时，上下文探测性能大幅提升（+0.11），但句法性能显著下降（-0.10）。这表明更长的时序依赖有助于捕获跨句子的上下文信息，但可能削弱对局部句法结构的建模。

**对比损失形式**：将对比损失替换为简单的L2距离损失（$\ell_i = \alpha \| \mathbf{z}_t^{(i)} - \mathbf{z}_{t-1}^{(i)} \|_2^2$）后，语义和上下文性能均大幅下降（分别为-0.07和-0.10），尽管FVE略有改善（+0.01）。这证明对比损失中的负样本排斥机制对于学习有区分性的语义特征至关重要，单纯的平滑约束不足以实现有效的语义-句法分离。

**吸收分析**：表10显示T-SAE的吸收指标与Matryoshka SAE相当，且分割特征更少，表明时序约束没有引入额外的特征冗余。

![[assets/figures/papers/paper_list_l20_https_openreview_net_forum_id_bojVI4l9Kn/figures/023_Table_10.jpg]]
*Table 10: Absorption*

### 可扩展性与局限性

T-SAE在Llama-3.1-8b-Instruct上的t-SNE结果（图9）显示，即使在8B参数规模的模型上，高层特征仍能保持语义-句法分离的趋势，证明方法具有良好的可扩展性。

需要指出的是，T-SAE的高层特征并非完美隔离：图4中某些特征在非相关段落中仍有微弱激活，表明存在一定的语义泄漏。这可能是因为语言模型本身在不同语义区域之间保留了上下文信息，导致特征空间无法完全解耦。此外，时间对比损失增加了计算开销，在相同内存预算下需要使用更小的批次大小，这可能影响训练效率。

### 补充图表

![[assets/figures/papers/paper_list_l20_https_openreview_net_forum_id_bojVI4l9Kn/figures/012_Table_4.jpg]]
*Table 4: Chosen and rejected examples with maximal difference (rejected−chosen) in feature activations for feature legal and formal language. In all cases, the rejected example is much longer*

![[assets/figures/papers/paper_list_l20_https_openreview_net_forum_id_bojVI4l9Kn/figures/014_Table_6.jpg]]
*Table 6: Top 15 features with greatest difference in mean sequence activation between rejected and chosen completions, averaged over the dataset (HH-RLHF (Bai et al., 2022))*

![[assets/figures/papers/paper_list_l20_https_openreview_net_forum_id_bojVI4l9Kn/figures/017_Table_8.jpg]]
*Table 8: Features used for steering interventions on Gemma2-2b*

## 定位与知识库关联

### 方法谱系：从标准SAE到时序感知的字典学习

T-SAEs 的核心贡献在于将语言序列的时间平稳性先验嵌入稀疏字典学习框架，其方法谱系可沿两条主线追溯。

**主线一：稀疏自编码器用于模型可解释性。** 标准SAE通过在语言模型激活上施加稀疏性约束来发现可解释特征，但其训练目标仅包含重构损失与稀疏性损失（如BatchTopK SAE）。Matryoshka SAE在此基础上引入层级重构损失，将特征空间划分为高层与低层两部分：高层特征直接重构原始输入，低层特征拟合高层重构后的残差，从而实现层级分解。T-SAEs 继承了Matryoshka SAE的特征空间划分与层级重构框架，但发现单纯的重构约束不足以使高层特征自发捕获语义——因为语言模型残差流中语义与句法信号高度纠缠，稀疏性先验本身无法区分时间尺度上的平稳性差异。

**主线二：对比学习与时间不变性表征。** 对比学习在自监督表征学习中已被广泛用于学习不变性表征。T-SAEs 将这一思想适配到SAE的非负稀疏特征空间：在高层表征 $z_t = W_{0:h}^{enc} x_t$ 上施加对称对比损失，以相邻token对 $(t, t-1)$ 为正样本、批次内其他样本为负样本，鼓励高层特征在相邻token上保持激活一致性。这一设计的关键洞见在于：语言的高级语义变量（如主题、意图）具有跨token的时间平稳性，而低级句法变量（如词性、局部搭配）则随token快速变化。通过将时间对比损失仅施加于高层特征，T-SAEs 实现了语义与句法的自监督解耦——高层特征被迫学习时间一致的模式，低层特征则自动拟合残差中快速波动的句法信号。

**与基线方法的关键差异。** 相较于BatchTopK SAE，T-SAEs 增加了特征空间划分与时间对比损失两个核心模块。相较于Matryoshka SAE，T-SAEs 唯一的架构差异是时间对比损失项；消融实验（Table 2）表明，单纯移除对比损失（即退化为Matryoshka SAE）会导致语义探测准确率下降0.07、上下文探测下降0.10，证实了时间对比损失是语义-句法解耦的因果操纵变量。若将对比损失替换为简单的L2距离损失 $\ell_i = \alpha \| z_t^{(i)} - z_{t-1}^{(i)} \|_2^2$，语义与上下文性能同样显著下降，表明对比形式的损失对于学习有判别力的高层表征至关重要。

### 适用边界

T-SAEs 的适用性受以下因素约束：

1. **序列模态依赖。** 时间对比损失的有效性建立在数据具有时间平稳性结构的前提上。语言天然满足这一条件，但将其迁移至其他序列模态（如视频帧、语音频谱）时，高层变量的时间尺度可能与语言不同，需要重新校准对比采样的窗口大小。

2. **特征空间划分的单一层次性。** 当前T-SAEs仅将特征空间划分为高层（前20%）与低层（后80%）两个层次。这对应了“语义 vs. 句法”的粗粒度二分，但语言存在更丰富的时间层次结构（文档主题 > 段落主旨 > 句子语义 > 短语结构 > 词汇选择）。消融实验显示，将高层比例调整为10%或50%会导致语义/句法性能的此消彼长（Table 2），表明单一划分比例是一个任务相关的超参数，而非普适最优解。

3. **计算开销与批次大小的权衡。** 时间对比损失需要维护批次内的负样本对，增加了显存占用。在相同内存预算下，T-SAEs 需要比Matryoshka SAE更小的批次大小，可能影响稀疏性约束的统计效率。

4. **特征泄漏现象。** 高层特征并非完全纯净的语义表征——Figure 4中可见部分高层特征在语义无关的文本段上仍有弱激活，表明模型保留了跨区域的上下文信息。这种泄漏对下游可解释性任务的实际影响尚未量化。

### 局限与开放问题

**已识别的局限。** 吸收分析（Table 10）显示T-SAEs的吸收指标与Matryoshka SAEs相当，且分割特征更少，表明时间对比损失并未引入额外的特征碎片化问题。但以下局限值得关注：首先，论文仅在Pythia-160m、Gemma2-2b和Llama-3.1-8b-Instruct三个模型上验证，更大规模模型（如70B+）上的扩展性虽有初步正面信号（Figure 9），仍需系统评估。其次，论文未提供专门的公平性评估——作者在伦理声明中承认该方法可能揭示数据中的偏颇相关性，但未测量或缓解这一风险。

**开放问题。**

- **多层时间层次结构建模。** 如何将文档、段落、句子、词的多层时间层次显式纳入T-SAE训练？一个可能的方向是设计多层级的对比损失，在不同特征子集上施加不同时间尺度的平稳性约束。

- **对比损失形式的适配。** 当前使用的标准余弦相似度对比损失是否最适合SAE的非负稀疏特征空间？针对稀疏表征设计专用对比目标可能进一步提升解耦质量。

- **特征泄漏的量化与控制。** 高层特征在语义无关区域泄漏的机制是什么？是否可以通过改进训练策略（如更激进的稀疏性约束或对抗性去相关）来抑制泄漏？

- **任务特定的语义-句法平衡。** 消融实验表明，通过调节高层特征比例可以在语义与句法性能之间权衡。是否可以在推理时动态调整这一平衡，使同一T-SAE适应不同的下游可解释性任务？

- **跨模态迁移。** 时间对比先验能否拓展到其他序列模态的字典学习？视频中的“场景”与“运动”、语音中的“说话人身份”与“音素”可能呈现类似的时间平稳性层级，值得探索。

## 原文 PDF

![[paperPDFs/ICLR_2026/Temporal_Sparse_Autoencoders_Leveraging_the_Sequential_Nature_of_Language_for_Interpretability.pdf]]
