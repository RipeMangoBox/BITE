---
title: "Decentralized Attention Fails Centralized Signals: Rethinking Transformers for Medical Time Series"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Decentralized_Attention_Fails_Centralized_Signals_Rethinking_Transformers_for_Medical_Time_Series.pdf
project_link: null
code_link: https://github.com/Levi-Ackman/TeCh
openreview_forum_id: oZJFY2BQt2
aliases:
- DAFCSRTMTS
tags:
- ICLR_2026
- topic/time_series_dynamical_systems
- topic/time_series_dynamical_systems/time_series_forecasting
core_operator: "引入全局核心令牌（core token）作为代理，通过集中式的聚合-再分布机制替代去中心化的注意力，使所有通道的信息先汇聚到核心令牌再分发回各通道，实现符合生理机制的通道交互。"
primary_logic: "借鉴分布式系统中星型拓扑（中央服务器）的集中式通信思想，用轻量级MLP实现核心令牌的聚合与再分布（CoTAR），既对齐了医学时间序列的中心化生成机制，又将令牌交互的计算复杂度从平方阶降为线性阶，同时提升了模型性能和效率。"
claims:
- "CoTAR模块在五个医学时间序列数据集上均优于标准注意力模块，且内存占用降至33%，推理时间降至20%。"
- "EEG和ECG信号的集中化指数（SCI/DIC）显著高于能源和气候等去中心化系统数据集，验证了医学信号的中心化特性。"
- "TeCh在APAVA数据集上相对此前最佳方法Medformer在全部指标平均值上提升12.13%。"
- "自适应双重令牌化（同时使用时间和通道嵌入）在所有数据集中普遍优于单一令牌化，消融实验中APAVA准确率提升11%。"
---

# Decentralized Attention Fails Centralized Signals: Rethinking Transformers for Medical Time Series

> [!tip] 核心洞察
> 借鉴分布式系统中星型拓扑（中央服务器）的集中式通信思想，用轻量级MLP实现核心令牌的聚合与再分布（CoTAR），既对齐了医学时间序列的中心化生成机制，又将令牌交互的计算复杂度从平方阶降为线性阶，同时提升了模型性能和效率。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 去中心化注意力与中心化信号失配：重新思考基于Transformer的医学时间序列模型 |
| 英文题名 | Decentralized Attention Fails Centralized Signals: Rethinking Transformers for Medical Time Series |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=oZJFY2BQt2) · [GitHub](https://github.com/Levi-Ackman/TeCh) |
| Topic | #topic/time_series_dynamical_systems #topic/time_series_dynamical_systems/time_series_forecasting |
| Method | TeCh |
| Dataset | ADFTD (3-class EEG), APAVA (2-class EEG), TDBrain (2-class EEG) |

> [!tip] 效果简介
> - ADFTD (3-class EEG) 上，Accuracy 为 54.54±0.70，对比 53.27±1.54 (Medformer)，变化 +1.27。
> - APAVA (2-class EEG) 上，F1-Score 为 86.30±1.06，对比 76.31±0.71 (Medformer)，变化 +9.99。
> - TDBrain (2-class EEG) 上，Accuracy 为 95.07±0.29，对比 90.81±0.60 (Medformer)，变化 +4.26。

## 概要

医学时间序列（如脑电图 EEG、心电图 ECG）的通道信号并非独立随机游走，而是由大脑或心脏等单一生理中枢统一调控产生的——这是一种**中心化**的生成机制。然而，当前主流的时间序列 Transformer 模型普遍采用标准的多头自注意力机制，其本质是**去中心化**的：每个令牌与其他所有令牌进行平等的成对交互。这种结构与生理信号的中心化特性之间存在根本性失配，限制了对通道间全局同步与统一波形特征的捕获能力。

针对这一瓶颈，本文提出 **TeCh**（Temporal-Channel Transformer with Centralized Core Token），其核心创新是**核心令牌聚合-再分布模块 CoTAR**（Core Token Aggregation-Redistribution）。CoTAR 借鉴分布式系统中星型拓扑的集中式通信思想，引入一个全局核心令牌作为代理：先将所有通道令牌的信息聚合到核心令牌，再从核心令牌分发回各通道，从而以集中式交互替代去中心化的注意力。这一设计不仅对齐了医学时间序列的生理生成机制，还将令牌交互的计算复杂度从平方阶 $O(S^2 D)$ 降至线性阶 $O(S D D_c)$。

TeCh 同时采用**自适应双重令牌化**策略，分别生成时间令牌（捕获时序依赖）和通道令牌（保留通道语义），并通过可调数量的 Transformer 编码器灵活适配不同数据集。

在五个医学时间序列分类数据集上的实验表明：
- TeCh 在 APAVA 数据集上相对此前最佳方法 **Medformer**（Wang et al., 2024b）在全部指标平均值上提升 **12.13%**（Table 2）；
- CoTAR 模块在全部数据集上均优于标准注意力机制，且内存占用降至 **33%**、推理时间降至 **20%**（Figure 4a）；
- 对通道高斯噪声的鲁棒性显著强于注意力机制，高噪声下 F1-Score 下降幅度远小于注意力变体（Figure 4b）。

通过谱中心化指数（SCI）和动态影响中心化指数（DIC）的量化分析（Table 11），本文进一步验证了 EEG/ECG 信号的中心化程度显著高于能源、气候等去中心化系统数据集，为 CoTAR 的设计提供了经验支撑。

### 医学时间序列分析的独特挑战

医学时间序列（Medical Time Series, MedTS），如脑电图（EEG）和心电图（ECG），是多变量时间序列分析的重要分支，广泛应用于疾病诊断、脑机接口和健康监测等场景。与能源、气候、交通等通用多变量时序数据不同，医学信号承载着独特的生理生成机制：EEG各通道的电位波动源自大脑皮层的全局神经调控，ECG各导联的波形形态统一受心脏窦房结的节律支配。这意味着，**医学时间序列的通道间依赖本质上是中心化的**——存在一个生理上的“中央控制器”协调所有通道的活动。

### Transformer在医学时序中的结构失配

近年来，Transformer架构凭借其强大的序列建模能力，在通用时间序列分析中取得了显著成功。其核心组件——多头自注意力机制——通过让每个令牌（token）平等地与所有其他令牌交互，实现了灵活的全连接信息融合。然而，这种**去中心化的通信模式**与医学信号的**中心化生成机制**之间存在着根本性的结构失配：

- **注意力机制**：每个令牌独立地向所有令牌查询信息，形成完全对等的交互图，计算复杂度为 $O(S^2 D)$（$S$ 为令牌数，$D$ 为维度）。这种设计隐含假设所有令牌之间的依赖关系是任意且对称的。
- **医学信号本质**：通道间的功能耦合并非任意，而是受单一生理源（脑/心脏）的全局调控。强行用去中心化的注意力去拟合这种中心化的依赖结构，不仅引入了冗余的自由度，还可能引入与生理机制无关的虚假关联。

为了量化这一直觉，本文引入了两个集中化度量指标：**谱集中化指数（SCI）**和**动态影响集中化指数（DIC）**。如 Table 11 所示，EEG和ECG数据集的SCI和DIC值显著高于能源、气候等去中心化系统数据集，从实证层面验证了医学信号的中心化特性。

### 现有方法的局限

当前面向医学时间序列的Transformer变体主要沿两个方向改进：

1. **时序依赖增强**：如 PatchTST（Nie et al., 2023）通过补丁嵌入捕获局部时序模式，iTransformer（Liu et al., 2024b）反转嵌入维度以建模变量间关系。但这些方法本质上仍沿用去中心化的注意力机制，未从结构层面适配医学信号的生成特性。
2. **通道依赖建模**：部分工作（如 Medformer, Wang et al., 2024b）尝试显式建模通道间依赖，但依然依赖注意力机制的隐式交互，未能利用信号源的中心化先验。

此外，标准注意力的平方级复杂度在处理高通道数、长序列的医学数据时面临严重的效率瓶颈，限制了模型在实际部署中的可扩展性。

### 核心动机与设计思路

本文的核心洞察是：**医学时间序列的中心化生成机制应当被显式地编码进模型架构中，而非依赖通用注意力机制去隐式学习**。借鉴分布式系统中星型拓扑的集中式通信思想，我们提出用**全局核心令牌（core token）**作为代理，替代去中心化的令牌间直接交互。所有通道的信息先汇聚到核心令牌，再由核心令牌统一分发回各通道，形成“聚合-再分布”的集中式通信范式。

这一设计同时解决了两个关键问题：
- **结构对齐**：集中式的令牌交互天然匹配医学信号的生理调控机制，使模型能够更高效地捕获通道间的全局同步和统一波形特征。
- **效率提升**：令牌交互的计算复杂度从 $O(S^2 D)$ 降至 $O(S D D_c)$（$D_c$ 为核心令牌维度，远小于 $S$），实现了线性复杂度。

Figure 1 直观对比了去中心化注意力与集中式CoTAR在令牌交互模式上的本质差异，以及它们与医学信号生理调控机制的对应关系。

## 核心方法与创新机理

本工作围绕一个核心发现展开：**标准Transformer的注意力机制与医学时间序列的信号本质之间存在结构性失配**。注意力本质上是去中心化的——每个令牌平等地与所有其他令牌交互；然而，EEG/ECG等医学信号源自脑/心脏的全局调控，其通道间依赖天然具有中心化特征（Table 11中SCI/DIC指数验证了这一特性）。TeCh框架通过两个关键的**changed slots**系统性地解决这一矛盾。

### 创新一：集中式令牌交互机制 CoTAR（替代去中心化注意力）

**基线值**：标准多头自注意力（Multi-Head Self-Attention），每个令牌通过$Q,K,V$投影与所有令牌计算注意力权重，复杂度为$O(S^2 D)$（Formula 1）。

**提出值**：核心令牌聚合-再分布模块CoTAR（Core Token Aggregation-Redistribution），引入一个全局核心令牌作为代理，实现集中式的信息流转。具体而言，CoTAR首先通过两层MLP将所有令牌信息聚合为一个核心令牌$\tilde{C}_o$，再将该核心令牌广播回每个令牌并拼接，最后通过另一组MLP完成交互输出（Formula 2）。这一设计的复杂度降为$O(S D D_c)$（$D_c$为核心令牌维度，通常设为$D/4$）。

**因果机制**：CoTAR模仿了分布式系统中星型拓扑的集中式通信模式——所有通道的信息先汇聚到“中央节点”（核心令牌），再由中央节点统一分发。这恰好对齐了医学信号由单一生理中枢（脑/心脏）全局调控的生成机制（Figure 1(b,d)），使模型能更有效地捕获通道间的全局同步与统一波形特征。

**证据强度**（高置信度，置信度0.95–0.98）：
- 消融实验中，CoTAR在所有五个医学数据集上持续优于标准注意力机制和去除令牌交互的变体，如ADFTD准确率提升4.02%（Table 5/Table 8）。
- 效率分析显示，CoTAR在APAVA数据集上内存占用仅为Medformer的33%，推理时间仅20%，同时准确率提升8%（Figure 4(a)）。
- 噪声鲁棒性测试表明，CoTAR对通道高斯噪声的鲁棒性显著优于注意力——即使噪声标准差$\beta=20$时F1下降幅度远小于注意力机制（Figure 4(b)）。

### 创新二：自适应双重令牌化策略（替代单一令牌化）

**基线值**：现有方法主要依赖单一令牌化策略——或仅使用时序嵌入（如PatchTST、iTransformer），或仅使用通道嵌入，导致只能捕获时序依赖或通道依赖之一。

**提出值**：自适应双重令牌化（Adaptive Dual Tokenization），同时构建时序令牌和通道令牌两个分支。时序令牌按补丁长度$L$将多通道时序片段扁平化并线性投影（Formula 3）；通道令牌将单个通道的完整序列投影为令牌，保留通道语义（Formula 4）。两个分支的输出通过平均后求和进行融合（Formula 5），且可通过调节编码器数量$M$和$N$灵活控制各分支的深度。

**因果机制**：时序令牌捕获跨通道的局部时序模式，通道令牌保留单通道的全局语义，二者互补。双重令牌化使模型能同时建模**时序依赖性**（同一通道内不同时刻的关联）和**通道依赖性**（同一时刻不同通道的关联），而后者正是医学信号中心化特性的直接体现。

**证据强度**（高置信度，置信度0.95–0.98）：
- 消融实验中，双重令牌化在所有数据集上普遍优于单一令牌化策略，APAVA数据集准确率提升约11%、F1提升约13%（Table 4/Table 7）。
- 该策略在通用人类活动识别数据集UCI-HAR上也表现出泛化优势，验证了其通用性（Table 4）。

### 方法谱系与知识库定位

TeCh的核心贡献在于**首次将医学信号的生理中心化先验系统性地融入Transformer架构设计**。与采用双依赖建模的**Leddam**（Yu et al., 2024b）和使用全局/辅助令牌的**TimeXer**（Wang et al., 2024e）相比，TeCh的区别在于：（1）CoTAR的集中式设计直接由生理机制驱动，而非通用的工程优化；（2）双重令牌化可自适应调节，而非固定的双分支结构。Table 9的对比验证了TeCh相对这些相似工作的优势。与医学时间序列SOTA **Medformer**（Wang et al., 2024b）相比，TeCh在APAVA数据集上全部指标平均值提升12.13%，同时大幅降低了计算开销。


TeCh 的整体架构遵循“双重令牌化 → 集中式编码 → 分支融合”的流水线设计，其核心动机来自一个关键观察：医学时间序列（如 EEG/ECG）的信号生成机制本质上是**中心化的**（由脑/心脏全局调控），而标准 Transformer 的注意力机制却是**去中心化的**（每个令牌平等交互）。这种结构失配使得传统注意力难以有效捕获通道间的全局同步与统一波形特征。

为对齐这一生理先验，TeCh 引入了一个**即插即用的集中式令牌交互模块 CoTAR**（Core Token Aggregation-Redistribution），用以替换 Transformer 编码器中的标准多头注意力。CoTAR 通过一个全局核心令牌作为代理，先将所有令牌的信息汇聚到核心令牌（聚合），再将核心令牌广播回各令牌（再分布），从而以线性复杂度实现集中式的通道依赖建模。

整体数据流如下（参见 Figure 3）：

**1. 输入与双重令牌化**

给定一个医学时间序列样本 $X \in \mathbb{R}^{T \times C}$（$T$ 个时间步，$C$ 个通道），TeCh 同时构造两类令牌：

- **时间令牌**：按补丁长度 $L$ 将多通道时序片段扁平化，经线性投影与位置嵌入得到 $E \in \mathbb{R}^{P \times D}$，其中 $P = \lceil T/L \rceil$，$D$ 为模型维度。每个时间令牌聚合了 $L$ 个时间步上所有通道的信息。
- **通道令牌**：将每个通道的完整序列 $X_{:,j}$ 单独投影为 $H \in \mathbb{R}^{C \times D}$，保留通道级别的语义完整性。

这种**自适应双重令牌化**策略使模型能够同时捕获时序依赖（通过时间令牌）和通道依赖（通过通道令牌），且编码器数目 $M$（时间分支）和 $N$（通道分支）可按数据集灵活调节——设置 $M=0$ 或 $N=0$ 即可退化为单一令牌化模式。

**2. 集中式编码器**

时间令牌 $E$ 和通道令牌 $H$ 分别送入 $M$ 层和 $N$ 层 Transformer 编码器，每层编码器中的注意力模块被 CoTAR 替换。CoTAR 的运算流程为：

$$\tilde{O} = \mathrm{GELU}(O W_1 + b_1) W_2 + b_2$$

$$O_w = \mathrm{Softmax}(\tilde{O}, \dim=0)$$

$$\tilde{C}_o = \mathrm{Sum}(\tilde{O} \odot O_w, \dim=0)$$

$$C_o = \mathrm{Repeat}(\tilde{C}_o, \mathrm{time}=S, \dim=0)$$

$$O_{Co} = \mathrm{Concat}([O, C_o], \dim=1)$$

$$A = \mathrm{GELU}(O_{Co} W_3 + b_3) W_4 + b_4$$

其中 $O \in \mathbb{R}^{S \times D}$ 为输入令牌序列，$S$ 为令牌数。CoTAR 首先通过两层 MLP 生成各令牌的重要性权重 $O_w$，加权求和得到全局核心令牌 $\tilde{C}_o$，再将其复制并拼接到每个令牌上，最后通过另一 MLP 完成信息再分布。整个过程仅涉及矩阵乘法与逐元素操作，复杂度为 $O(S D D_c)$（$D_c$ 为核心令牌维度，设为 $D/4$），远低于标准注意力的 $O(S^2 D)$。

**3. 分支融合与分类**

两分支编码器的输出 $\tilde{O}_{te}$ 和 $\tilde{O}_{ch}$ 分别沿通道维度取平均，得到各自的分支表示后直接相加，经线性层投影为 $K$ 类预测 logits：

$$\hat{Y} = (\tilde{O}_{te} + \tilde{O}_{ch}) W_y + b_y$$

这一简洁的融合设计避免了复杂的门控或注意力融合机制，同时保持了时间与通道信息的互补性。

**架构设计的因果逻辑链**：医学信号的中心化生成机制 → 需要集中式通道交互 → CoTAR 以核心令牌代理实现聚合-再分布 → 双重令牌化同时捕获时序与通道依赖 → 分支平均融合整合两类表示 → 线性复杂度保证效率。这一设计在五个医学时间序列数据集上均取得优于标准注意力的性能，同时将内存占用降至 33%、推理时间降至 20%（Figure 4a），验证了“结构对齐生理先验”这一核心假设的有效性。

### 问题形式化

给定医学时间序列样本 $\mathbf{X} \in \mathbb{R}^{T \times C}$（$T$ 个时间戳，$C$ 个通道），目标是预测其类别标签 $\hat{\mathbf{Y}} \in \mathbb{R}^{K}$。TeCh 的核心设计围绕两个关键模块展开：**CoTAR（Core Token Aggregation-Redistribution）** 和 **自适应双重令牌化（Adaptive Dual Tokenization）**。

### CoTAR：集中式令牌交互模块

#### 设计动机

标准多头自注意力机制（Formula 1）本质上是去中心化的——每个令牌平等地与其他所有令牌交互：

$$Q = O W_Q + b_q,\quad K = O W_K + b_k,\quad V = O W_V + b_v,\quad A = \mathrm{Softmax}\left(\frac{Q K^T}{\sqrt{D}}\right) V$$

其中 $O \in \mathbb{R}^{S \times D}$ 为输入令牌序列，$S$ 为序列长度，$D$ 为隐层维度。该操作的计算复杂度为 $O(S^2 D)$。

然而，医学时间信号（如 EEG/ECG）的通道间交互本质上是中心化的——所有通道信号均由大脑或心脏这一全局中枢调控。去中心化的注意力结构与这一生理机制存在结构性失配。

#### CoTAR 计算流程

CoTAR 通过引入一个全局核心令牌（core token）作为代理，实现集中式的聚合-再分布通信。其完整计算流程（Formula 2）如下：

**步骤 1：令牌信息投影**

$$\tilde{O} = \mathrm{GELU}(O W_1 + b_1) W_2 + b_2$$

其中 $W_1 \in \mathbb{R}^{D \times D_c}$，$W_2 \in \mathbb{R}^{D_c \times 1}$，将每个令牌从 $D$ 维压缩为标量权重。$D_c$ 为核心令牌维度，通常设为 $D/4$。

**步骤 2：自适应权重与核心令牌聚合**

$$O_w = \mathrm{Softmax}(\tilde{O}, \dim=0)$$

$$\tilde{C}_o = \mathrm{Sum}(\tilde{O} \odot O_w, \dim=0)$$

通过 Softmax 归一化获得各令牌的贡献权重，加权求和得到聚合后的核心令牌 $\tilde{C}_o \in \mathbb{R}^{1}$。

**步骤 3：核心令牌广播与拼接**

$$C_o = \mathrm{Repeat}(\tilde{C}_o, \text{time}=S, \dim=0)$$

$$O_{Co} = \mathrm{Concat}([O, C_o], \dim=1)$$

将核心令牌复制 $S$ 份，与原始令牌沿特征维拼接，得到 $O_{Co} \in \mathbb{R}^{S \times (D+1)}$。

**步骤 4：信息再分布**

$$A = \mathrm{GELU}(O_{Co} W_3 + b_3) W_4 + b_4$$

其中 $W_3 \in \mathbb{R}^{(D+1) \times D_c}$，$W_4 \in \mathbb{R}^{D_c \times D}$，将集中后的信息重新分发回各令牌，得到最终输出 $A \in \mathbb{R}^{S \times D}$。

#### 关键特性

- **计算复杂度**：CoTAR 的核心操作均为矩阵乘法，复杂度为 $O(S D D_c)$，当 $D_c \ll S$ 时为线性阶，显著低于注意力的平方阶 $O(S^2 D)$。
- **即插即用**：CoTAR 可直接替换 Transformer 编码器中的标准注意力模块，无需改动其他组件。
- **集中式归纳偏置**：核心令牌充当全局信息枢纽，强制所有通道信息先汇聚后分发，天然对齐医学信号的中心化生成机制。

### 自适应双重令牌化

TeCh 同时构建时间令牌和通道令牌，以捕获时序依赖和通道依赖两种模式。

#### 时间嵌入（Temporal Embedding）

将原始序列按补丁长度 $L$ 切分为 $P = \lceil T/L \rceil$ 个片段，每个片段跨通道扁平化后投影：

$$E_{i,:} = \mathrm{vec}(X_{(i-1)L:iL,:}) W_t + b_t + W_{i,:}^{tpos},\quad i=1,\dots,P$$

其中 $W_t \in \mathbb{R}^{LC \times D}$，$b_t \in \mathbb{R}^{D}$，$W^{tpos} \in \mathbb{R}^{P \times D}$ 为可学习位置嵌入。当 $L=1$ 时退化为逐时间点嵌入。

#### 通道嵌入（Channel Embedding）

将每个通道的完整时序独立投影，保留通道语义：

$$H_{j,:} = X_{:,j}^{\top} W_c + b_c + W_{j,:}^{cpos},\quad j=1,\dots,C$$

其中 $W_c \in \mathbb{R}^{T \times D}$，$b_c \in \mathbb{R}^{D}$，$W^{cpos} \in \mathbb{R}^{C \times D}$ 为通道位置嵌入。

#### 分支融合与预测

时间分支和通道分支分别经过 $M$ 和 $N$ 个配备 CoTAR 的 Transformer 编码器处理后，对输出进行通道维平均并求和：

$$\hat{Y} = (\tilde{O}_{te} + \tilde{O}_{ch}) W_y + b_y$$

其中 $\tilde{O}_{te}, \tilde{O}_{ch} \in \mathbb{R}^{D}$ 分别为两分支平均后的表示，$W_y \in \mathbb{R}^{D \times K}$，$b_y \in \mathbb{R}^{K}$。当 $M=0$ 或 $N=0$ 时，对应分支输出置零，实现单分支模式。

### 集中化量化指标

为量化数据集的内在中心化程度，论文引入两个指标（Formula 6）：

**谱集中化指数（SCI）**：基于协方差矩阵 $\frac{1}{T-1}(\mathbf{X}-\bar{\mathbf{X}})(\mathbf{X}-\bar{\mathbf{X}})^\top$ 的最大特征值占比，衡量通道间能量的集中程度。值越高表示越中心化。

**动态影响集中化指数（DIC）**：基于一阶向量自回归模型，计算各通道出强度 $s_i = \sum_j |A_{ji}|$ 的归一化失衡程度，捕捉动态交互中的中心化倾向。

在 Table 11 中，EEG/ECG 数据集的 SCI 和 DIC 值显著高于能源、气候等去中心化系统数据集，定量验证了医学信号的中心化特性。

## 实验与关键发现

### 核心瓶颈验证：医学信号的中心化本质

TeCh 的核心动机建立在“医学时间序列信号本质上是中心化生成的”这一假设之上。为量化验证该假设，作者提出了两种中心化指数：**谱中心化指数 (Spectral Centralization Index, SCI)** 和 **动态影响中心化指数 (Dynamic Influence Centralization, DIC)**。

SCI 通过计算通道间协方差矩阵的最大特征值占总方差的比值来衡量能量集中程度：

$$
\operatorname{SCI}(\mathbf{X}) = \frac{\lambda_{\max}\left(\frac{1}{T-1}(\mathbf{X}-\bar{\mathbf{X}})(\mathbf{X}-\bar{\mathbf{X}})^\top\right)}{\operatorname{Tr}\left(\frac{1}{T-1}(\mathbf{X}-\bar{\mathbf{X}})(\mathbf{X}-\bar{\mathbf{X}})^\top\right)}
$$

DIC 则基于一阶向量自回归模型，通过出强度的失衡程度捕捉动态交互中的中心化程度：

$$
\mathrm{DIC}(\mathbf{X}) = \frac{\max_i s_i - \bar{s}}{\bar{s}},\quad s_i = \sum_j |A_{ji}|
$$

**Table 11** 的结果直接支撑了核心假设：EEG 和 ECG 数据集的 SCI 和 DIC 值显著高于能源、气候等去中心化系统数据集。这一量化证据表明，医学信号确实存在单一主导源（脑/心脏）的全局调控特性，而标准 Transformer 的去中心化注意力机制与这一结构特性存在根本性失配。

![[assets/figures/papers/paper_list_l34_https_openreview_net_forum_id_oZJFY2BQt2/figures/017_Table_11.jpg]]
*Table 11: Quantitative comparison of the centralized property. We measure centralization using: (1) Spectral Centralization Index (SCI), the ratio of the largest eigenvalue to total variance, and (2) Dynamic Influence Centralization (DIC), the normalized out-strength imbalance of a first-order VAR model. Higher values indicate stronger centralized behavior*

### 主要结果：TeCh 在医学时间序列上的性能优势

**Table 2** 展示了 TeCh 在五个医学时间序列数据集上的全面对比结果（Subject-Independent 设置），对比基线包括 Medformer（医学时序 SOTA）、Autoformer、FEDformer、Informer、iTransformer、PatchTST 等 10 个模型。

关键结论：

- **APAVA (2-class EEG)**：TeCh 在所有指标上均大幅领先。F1-Score 达到 **86.30±1.06**，相比此前最佳方法 Medformer（76.31±0.71）提升 **+9.99**；相比原始 Transformer（73.08±0.47）提升超过 13 个百分点。该数据集上 TeCh 相对 Medformer 的全部指标平均值提升 **12.13%**（见 Abstract）。

- **TDBrain (2-class EEG)**：TeCh 准确率达到 **95.07±0.29**，超越 Medformer（90.81±0.60）达 **+4.26**，且标准差更小，稳定性更优。

- **ADFTD (3-class EEG)**：TeCh 准确率为 **54.54±0.70**，以 **+1.27** 的优势超越 Medformer（53.27±1.54）。该数据集类别更多、难度更高，绝对提升虽小但一致。

- **PTB-XL (5-class ECG)**：TeCh 准确率 **73.53±0.07**，优于 Medformer（72.87±0.23）和所有其他基线。值得注意的是，Autoformer（61.68±2.72）和 FEDformer（57.20±9.47）在此数据集上表现极差，表明频率增强策略可能不适合多类 ECG 分类。

- **PTB (2-class ECG)**：TeCh 未取得最优（Informer 以 80.45±1.87 领先），但该数据集上各方法差距较小，需结合具体指标综合判断。

**Table 3** 展示了在两个人类活动识别（HAR）数据集上的泛化测试。TeCh 在 FLAAP（10-class）和 UCI-HAR（6-class）上均取得最佳结果（FLAAP 准确率 80.60%，UCI-HAR 准确率 96.52%），说明 CoTAR 的集中式交互机制在具有潜在通道相关性的通用时序数据上也具备迁移能力。

### 效率与鲁棒性分析

**Figure 4 (a)** 在 APAVA 数据集上对比了 TeCh 与各基线的效率-有效性权衡。以 batch size B=128 为基准：

- TeCh 的内存占用仅为 Medformer 的 **33%**，推理时间仅为 **20%**，同时准确率提升 **8%**。
- 这一效率优势源于 CoTAR 将令牌交互的计算复杂度从 $O(S^2 D)$ 降为 $O(S D D_c)$，其中核心令牌维度 $D_c$ 设为 $D/4$。

**Figure 4 (b)** 在 PTB 数据集上测试了通道噪声鲁棒性。实验在最后一个通道上逐步注入标准差 $\beta$ 从 0.0 到 20.0 的高斯噪声：

- 使用 CoTAR 时，F1-Score 在高噪声下下降幅度远小于标准注意力机制。
- 这一现象可从机制上解释：CoTAR 通过核心令牌的聚合步骤天然具备信息去噪能力——所有通道的信息先汇聚到核心令牌，噪声在聚合过程中被平均稀释；而注意力机制中每个令牌直接与其他所有令牌交互，噪声通道可直接污染所有令牌的表示。

### 消融实验：双重令牌化与 CoTAR 的必要性

**Table 4** 和 **Table 7** 消融了双重令牌化策略。对比四种配置：(i) w/o（无令牌化，直接线性分类）、(ii) Temporal-only、(iii) Channel-only、(iv) Dual（时间+通道）。

![[assets/figures/papers/paper_list_l34_https_openreview_net_forum_id_oZJFY2BQt2/figures/009_Table_4.jpg]]
*Table 4: Ablation result of the proposed Dual Tokenization strategy. We include a general Human Activity dataset, UCI-HAR, to test its generalizability. (i) w/o: No tokenization is performed and directly uses the raw series as input-without representation learning, a single linear projection as classifier. (ii) Temporal: Only Temporal embedding is used. (iii) Channel: Only Channel embedding is used. (iv) Dual: Both Temporal and Channel embedding are used. The best is Bolded*

![[assets/figures/papers/paper_list_l34_https_openreview_net_forum_id_oZJFY2BQt2/figures/013_Table_7.jpg]]
*Table 7: Full ablation result of the proposed Dual Tokenization strategy. (i) w/o: No tokenization is performed and directly uses the raw series as input-without representation learning, a single linear projection as classifier. (ii) Temporal: Only Temporal embedding. (iii) Channel: Only Channel embedding. (iv) Dual: Both Temporal and Channel. The best is Bolded*

核心发现：双重令牌化在所有数据集上均优于单一令牌化。以 APAVA 为例，Dual 相比 Temporal-only 准确率提升约 **11%**，F1 提升约 **13%**。这一结果验证了医学时序中时间依赖和通道依赖的互补性——仅建模时间模式或仅建模通道模式都会丢失关键信息，而自适应双重令牌化通过可调的时间编码器数量 $M$ 和通道编码器数量 $N$（详见 Table 6 的超参数配置）实现了两者的灵活平衡。

![[assets/figures/papers/paper_list_l34_https_openreview_net_forum_id_oZJFY2BQt2/figures/012_Table_6.jpg]]
*Table 6: Critical hyperparameters for TeCh by dataset. We listed the model dimension (D), patch length of Temporal embedding (L), number of temporal encoders (M ), number of channel encoders (N ), and learning rate (lr)*

**Table 5** 和 **Table 8** 消融了 CoTAR 模块。对比三种配置：(i) w/o（直接移除令牌交互）、(ii) Attention（替换为标准注意力）、(iii) CoTAR。

![[assets/figures/papers/paper_list_l34_https_openreview_net_forum_id_oZJFY2BQt2/figures/010_Table_5.jpg]]
*Table 5: Ablation result of the proposed ‘Core Token Aggregate-Redistribut’ (CoTAR) module. (i) w/o: No Token interaction is performed, which means directly removing the CoTAR module. (ii) Attention: Replacing CoTAR with the Attention module. (iii) CoTAR: baseline with the CoTAR module. The best is Bolded*

![[assets/figures/papers/paper_list_l34_https_openreview_net_forum_id_oZJFY2BQt2/figures/014_Table_8.jpg]]
*Table 8: Full ablation result of the proposed ‘Core Token Aggregate-Redistribut’ (CoTAR) module. (i) w/o: No Token interaction is performed, which means directly removing the CoTAR module. (ii) Attention: Replacing CoTAR with the Attention module. (iii) CoTAR: baseline with the CoTAR module. The best is Bolded*

核心发现：CoTAR 在所有数据集上持续优于标准注意力和无交互变体。在 ADFTD 上，CoTAR 相比 Attention 准确率提升 **+4.02%**；在 APAVA 上提升 **+2.37%**。值得注意的是，“无交互”配置在某些数据集上甚至优于注意力，这反直觉地暗示：当信号本质是中心化的时候，去中心化的全连接注意力可能引入有害的跨通道噪声，而 CoTAR 的集中式结构恰好规避了这一问题。

### 可视化分析：核心令牌的集中代表性

**Figure 5** 通过 T-SNE 可视化了 CoTAR 生成的核心令牌与其他令牌在嵌入空间中的分布。核心令牌位于令牌簇的中心位置，验证了其作为全局信息聚合体的代表性。这一可视化从几何角度支撑了 CoTAR 的设计直觉：通过聚合-再分布机制，核心令牌确实捕获了所有通道的共享信息，并作为“中央服务器”将其分发回各令牌——这与星型拓扑的集中式通信思想完全一致。

### 与类似设计的对比

**Table 9** 将 TeCh 与两个采用类似设计思路的通用时序模型进行了对比：(i) **Leddam**（Yu et al., 2024b），同样采用双依赖建模结构；(ii) **TimeXer**（Wang et al., 2024e），使用全局/辅助令牌聚合再分发信息。TeCh 在医学时序数据集上优于两者，说明 CoTAR 的集中式设计并非简单的“全局令牌”技巧，而是针对医学信号中心化特性的专用归纳偏置。

### 稳健性验证

**Table 10** 展示了基于 Subject ID 的五折交叉验证结果，验证了 TeCh 在不同数据划分下的性能稳定性。此外，**Table 12** 与 WWW 2025 的最新医学时序分类器 MedGNN 进行了对比，进一步确认了 TeCh 的竞争力。

### 局限性与失败模式提示

1. **非中心化信号的适用性存疑**：CoTAR 的集中化假设本质上是归纳偏置。对于无明显单一中心源的时序系统（如部分分布式传感器网络），CoTAR 可能劣于灵活的全连接注意力。当前仅在医学时序和少量 HAR 数据上验证，金融、交通等其他多变量时序的适用性尚待探索。

2. **超参数依赖手动调节**：核心令牌维度 $D_c$ 固定为 $D/4$，时间/通道编码器数量 $M$ 和 $N$ 需按数据集手动调参（Table 6），缺乏自适应选择机制。这在实际部署中增加了调参成本。

3. **PTB 数据集上未全面领先**：在 PTB（2-class ECG）上，TeCh 未取得最优准确率，提示 ECG 的中心化程度或信号特征可能与 EEG 存在差异，CoTAR 的设计可能需要针对 ECG 进一步适配。

## 定位与知识库关联

### 核心创新与基线关系

TeCh 的核心贡献在于**用集中式令牌交互（CoTAR）替代去中心化的多头自注意力**，以对齐医学时间序列（EEG/ECG）的生理中心化生成机制。这一设计在方法谱系中处于两条路线的交汇点：

**（1）高效 Transformer 路线。** 自 **Transformer**（Vaswani et al., NeurIPS 2017）引入序列建模以来，去中心化的全对全注意力因其平方阶复杂度 $O(S^2 D)$ 而催生大量效率改进工作。**Reformer**（Kitaev et al., ICLR 2020）通过局部敏感哈希将复杂度降至 $O(S \log S)$；**Informer**（Zhou et al., AAAI 2021）利用稀疏自注意力蒸馏；**Autoformer**（Wu et al., NeurIPS 2021）和 **FEDformer**（Zhou et al., ICML 2022）分别引入自相关机制和频率增强注意力；**PatchTST**（Nie et al., ICLR 2023）通过补丁化减少令牌数量；**iTransformer**（Liu et al., ICLR 2024）反转嵌入维度以捕获通道间依赖。这些方法虽降低了计算开销，但**均保留了去中心化的令牌交互范式**——每个令牌仍平等地与其他所有令牌交互。TeCh 的 CoTAR 模块则从根本上转向集中式拓扑，将复杂度降至线性 $O(S D D_c)$，其效率提升源自结构简化而非稀疏化或近似。

**（2）通道依赖建模路线。** 多变量时间序列的通道间关系建模是近年来的研究热点。**Leddam**（Yu et al., 2024）采用双依赖建模结构（时间依赖 + 通道依赖），与 TeCh 的自适应双重令牌化设计思路相似；**TimeXer**（Wang et al., 2024）使用全局/辅助令牌聚合信息后再分发，与 CoTAR 的核心令牌机制在形式上接近。但关键差异在于：Leddam 和 TimeXer 均为通用时间序列设计，未针对医学信号的**生理中心化特性**进行归纳偏置设计。TeCh 的 CoTAR 明确将核心令牌视为脑/心脏的代理，通过“聚合→再分布”模拟生理调控路径，这是其与通用方法的本质区别。Table 9 的直接对比显示，TeCh 在医学数据集上显著优于 Leddam 和 TimeXer，验证了领域特定归纳偏置的价值。

**（3）医学时间序列 SOTA 路线。** **Medformer**（Wang et al., 2024）是此前医学时间序列分类的最佳方法，仍采用 Transformer 架构的注意力机制。TeCh 在五个医学数据集上全面超越 Medformer（Table 2），尤其在 APAVA 数据集上 F1-Score 提升 9.99 个百分点，同时内存占用降至 33%、推理时间降至 20%（Figure 4a）。与 WWW 2025 最新的 **MedGNN** 对比（Table 12），TeCh 同样保持优势。

### 适用边界

CoTAR 的集中化设计基于一个核心假设：**多变量时间序列的通道间交互存在单一主导中心源**。这一假设在以下场景中成立：
- **脑电（EEG）信号**：各通道电位变化由脑区全局神经活动调控；
- **心电（ECG）信号**：各导联波形由心脏电活动统一支配；
- **部分人体活动识别（HAR）数据**：如 UCI-HAR 和 FLAAP 数据集，身体各部位传感器信号受中枢神经系统协调。

Table 11 的定量分析为这一假设提供了实证支撑：EEG 和 ECG 数据集的**谱集中化指数（SCI）**和**动态影响集中化指数（DIC）**显著高于能源、气候等去中心化系统数据集，验证了医学信号的中心化特性与 CoTAR 设计的匹配性。

然而，对于**无明显单一中心源的分布式系统**（如交通传感器网络、分布式气象站、金融多资产联动），CoTAR 的集中式归纳偏置可能成为限制。在此类场景中，灵活的全连接注意力或图神经网络可能更优。论文仅在 HAR 数据集上进行了泛化测试（Table 3），尚未在金融、交通等典型多变量时序基准上验证。

### 局限性与开放问题

**已知局限：**
1. **超参数依赖手动调节**：核心令牌维度 $D_c$ 固定为 $D/4$，时间/通道编码器数量 $M$ 和 $N$ 需按数据集分别调参（Table 6），缺乏自适应选择机制。在 APAVA 上 $M=0$（纯通道分支），而在 TDBrain 上 $M=6, N=2$，最优配置差异显著。
2. **验证域有限**：仅在 EEG、ECG 和 HAR 数据上验证，其他类型多变量时序的适用性尚待探索。
3. **集中化假设是归纳偏置**：对不符合该假设的数据分布，CoTAR 可能劣于全连接注意力（Table 5 中 Attention 变体在某些指标上差距较小）。

**开放问题：**
1. **自适应分支选择**：能否自动学习最优的 $M$ 和 $N$，甚至动态决定是否需要时间/通道分支？这可通过可微架构搜索或门控机制实现。
2. **跨任务迁移**：CoTAR 模块能否应用于时间序列预测、异常检测等需要建模多变量依赖的其他任务？
3. **理论指导设计**：集中化指数（SCI/DIC）与模型性能之间是否存在定量关系？能否基于数据集的 SCI/DIC 值预先判断 CoTAR 的适用性，形成理论指导的架构选择框架？
4. **多中心扩展**：对于存在多个子中心源的复杂生理系统（如多模态神经影像），能否将单一核心令牌扩展为多核心令牌层次结构？

## 原文 PDF

![[paperPDFs/ICLR_2026/Decentralized_Attention_Fails_Centralized_Signals_Rethinking_Transformers_for_Medical_Time_Series.pdf]]
