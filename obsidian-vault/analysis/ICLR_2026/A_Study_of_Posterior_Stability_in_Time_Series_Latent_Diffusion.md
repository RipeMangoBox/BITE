---
title: "A Study of Posterior Stability in Time-Series Latent Diffusion"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/A_Study_of_Posterior_Stability_in_Time_Series_Latent_Diffusion.pdf
aliases:
- PSLDP
- SPSTSLD
tags:
- ICLR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/generative_models_and_autoencoders
core_operator: "移除KL正则化并将扩散过程视为变分推断，同时利用扩散末端模拟后验崩塌来惩罚解码器对潜在变量的不敏感性，从而恢复潜在变量的控制力。"
primary_logic: "将扩散过程的前几步解释为变分推断，消除危险的KL正则化，并用扩散过程的后期步骤模拟后验崩塌以强制解码器敏感，实现后验稳定。"
claims:
- "严格后验崩塌会使潜在扩散退化为弱VAE，丧失表达能力"
- "依赖性度量显示标准潜在扩散中潜在变量对解码器的影响随时间指数衰减为零"
- "PSLD框架在MIMIC、WARDS、Earthquakes上Wasserstein距离显著低于标准潜在扩散（2.13 vs 5.02等）"
- "PSLD框架消除后验崩塌症状：依赖性度量显示潜在变量影响稳定在约0.5，且无依赖性错觉"
---

# A Study of Posterior Stability in Time-Series Latent Diffusion

> [!tip] 核心洞察
> 将扩散过程的前几步解释为变分推断，消除危险的KL正则化，并用扩散过程的后期步骤模拟后验崩塌以强制解码器敏感，实现后验稳定。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 时间序列潜在扩散中后验稳定性的研究 |
| 英文题名 | A Study of Posterior Stability in Time-Series Latent Diffusion |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=UbL2Fo0IvV) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/generative_models_and_autoencoders |
| Method | Posterior-Stable Latent Diffusion (PSLD，后验稳定潜在扩散) |
| Dataset | MIMIC, WARDS, Earthquakes, Retail |

> [!tip] 效果简介
> - MIMIC 上，Wasserstein distance 为 2.13，对比 5.02 (Latent Diffusion)，变化 -2.89。
> - WARDS 上，Wasserstein distance 为 3.01，对比 7.46 (Latent Diffusion)，变化 -4.45。
> - Earthquakes 上，Wasserstein distance 为 2.49，对比 4.21 (Latent Diffusion)，变化 -1.72。

## 概述

时间序列潜在扩散模型存在严重的后验崩塌问题：由于KL正则化与自回归解码器的强表达能力，潜在变量 $\mathbf{z}$ 在生成过程中迅速失去对解码器的影响，导致整个模型退化为弱VAE，扩散过程的建模能力被浪费。本文通过理论分析和依赖性度量（Definition 3.2）定量证实了该崩塌现象：在标准潜在扩散中，$\mathbf{z}$ 对解码器的影响 $m_{t,0}$ 随时间指数衰减至零（Fig. 1）。针对这一问题，本文提出**后验稳定潜在扩散（PSLD）**框架，从三个关键设计上重构变分推断与扩散训练：（1）彻底移除KL正则化，允许自由形式的先验分布；（2）将扩散过程的前几步视为变分推断，通过从编码器输出 $\mathbf{z}^0$ 开始的早期扩散步骤采样作为潜在变量，无需KL项；（3）利用扩散后期的非信息性 $\mathbf{z}$ 模拟后验崩塌，并设计塌缩模拟惩罚 $\mathcal{L}^{\mathrm{CS}}$ 强制解码器对低信息量的潜在变量保持敏感，从而防止解码器忽视 $\mathbf{z}$。该框架同时保留了扩散模型对潜在空间分布的建模能力，仅增加可接受的计算开销（训练时间约多40分钟，推理时间基本持平）。

实验表明，PSLD框架在多个真实时间序列数据集上显著优于标准潜在扩散及KL退火、跳跃连接、互信息约束等缓解后验崩塌的强基线。以Transformer为骨干网络为例，在MIMIC、WARDS、Earthquakes上的Wasserstein距离分别为2.13、3.01、2.49，而标准潜在扩散的对应值为5.02、7.46、4.21（Table 1）；在Retail和Energy数据集上的MMD同样取得明显改进（Table 5）。依赖性度量分析进一步验证了框架的有效性：PSLD中 $\mathbf{z}$ 的全局影响 $m_{t,0}$ 稳定在约0.5附近，且在打乱时间序列上无虚假依赖，表明后验已保持稳定、解码器始终敏感于潜在变量（Fig. 2）。消融实验确认超参数 $N=50,\;M=100$ 为最优设置，且PSLD的性能提升并非简单源于增加计算量或跳跃连接（Table 3）。整体上，PSLD在几乎不增加推理开销的前提下，从根本上解决了时间序列潜在扩散的后验崩塌难题。

## 背景与动机

复杂时间序列的生成建模（如医疗监护、地震记录等）要求模型同时捕捉全局长期结构与局部时序依赖。标准变分自编码器虽能学习紧凑隐空间，但在高维时序上，其先验标准高斯假设与KL正则化常常导致解码器高度自回归，从而弱化或忽视来自潜在变量的信息。这一现象被称为**后验崩塌**（posterior collapse）。

潜在扩散模型试图结合二者的优势：用VAE编码器获得低维潜在表示$\mathbf{z}$，再在潜在空间训练扩散模型以丰富先验分布$p^{\mathrm{prior}}(\mathbf{z})$。然而，**时间序列潜在扩散中的后验崩塌问题却严重限制了模型表达能力**：一旦发生后验崩塌，潜在变量$\mathbf{z}$在测试时将退化为标准高斯噪声，扩散模型的去噪过程实质失效，整个框架退化成一个弱VAE（Proposition 3.1），无法发挥扩散先验应有的生成多样性。

依赖性度量$m_{t,0}$（Definition 3.2）的量化分析直接证实了上述退化：在标准潜在扩散中，潜在变量$\mathbf{z}$对解码器的影响随时间步$t$**指数衰减至零**。无论输入序列是有序还是打乱顺序，$m_{t,0}$均迅速收敛到零附近（Fig. 1），表明解码器几乎完全依赖于自回归前缀$\mathbf{X}_{1:t-1}$进行预测，而对$\mathbf{z}$完全忽视。打乱序列实验中$m_{t,0}$未见回升，排除了语义相关性导致的依赖错觉，进一步确证了真实后验崩塌的存在。

本文深入剖析了该崩塌的两大成因：**(i) KL正则化**迫使后验分布$q^{\mathrm{VI}}(\mathbf{z}|\mathbf{X})$近似先验$p^{\mathrm{prior}}(\mathbf{z})=\mathcal{N}(\mathbf{0},\mathbf{I})$，压制了$\mathbf{z}$携带的信息量；**(ii) 强力自回归解码器**本身即具备足够的时序预测能力，在KL约束下更容易“走捷径”而忽视$\mathbf{z}$。

为根治上述瓶颈，本文提出**后验稳定潜在扩散（PSLD）**框架，核心思路是**完全移除KL正则化，将扩散过程的前几步重新解释为变分推断，并用扩散过程的末步模拟后验崩塌以强制解码器对潜在变量保持敏感**。这一框架从根本上改变了时间序列潜在扩散的学习机制，使潜在变量能够在整条生成轨迹上持续施加控制力，从而充分释放扩散先验的表达潜力。

## 核心创新

标准潜在扩散在时间序列生成中面临的后验崩塌瓶颈是：解码器对潜在变量 $\mathbf{z}$ 的依赖性随时间指数衰减至零，扩散模型退化为弱 VAE（Proposition 3.1，后验崩塌使测试时的 $\mathbf{z}$ 成为高斯噪声，扩散分支完全冗余）。PSLD 框架通过三个因果上的关键 slot 变更，同时消除崩塌并恢复解码器对 $\mathbf{z}$ 的稳定敏感性。

1. **移除 KL 正则化** – 不再使用 $\mathrm{D}_{\mathrm{KL}}(q^{\mathrm{VI}}\|\mathcal{N}(0,I))$，从而避免了 KL 项将后验强行拉向无信息先验的崩塌驱动力。这允许先验分布 $p^{\mathrm{prior}}(\mathbf{z})$ 成为自由形式，完全由扩散模型学习（Sec. 4.2）。

2. **用早期扩散步骤作为变分推断** – 替代传统的重参数化技巧 $\mathbf{z}=\boldsymbol{\mu}+\mathrm{diag}(\boldsymbol{\sigma})\boldsymbol{\epsilon}$，PSLD 将编码器输出 $\mathbf{z}^0$ 通过前向扩散的前几步（$i\sim\mathcal{U}\{0,N\}$）采样得到 $\mathbf{z}=\mathbf{z}^i$，即 $\mathbf{z}\sim q^{\mathrm{forw}}(\mathbf{z}^i|\mathbf{z}^0)$。此时变分下界直接由早期扩散步的加权似然 $\mathcal{L}^{\mathrm{VI}} = \mathbb{E}_{i,\mathbf{z}^0}[-\bar{\alpha}^{\gamma i}\ln p^{\mathrm{gen}}(\mathbf{X}|\mathbf{z}^i)]$ 给出，无需 KL 项（Sec. 4.2）。这个设计同时构成了平滑的解码器正则化。

3. **引入后验崩塌模拟惩罚 $\mathcal{L}^{\mathrm{CS}}$** – 利用扩散过程的最后几步（噪声水平高，$\mathbf{z}^i$ 几近无信息）模拟崩塌场景。让解码器对这些非信息性 $\mathbf{z}$ 计算生成对数似然，并施加惩罚 $(1-\bar{\alpha}^{\lceil i/\eta\rceil})\ln p^{\mathrm{gen}}$，迫使解码器对输入潜变量保持高度敏感，即使潜变量被高度破坏也不能产生高置信度输出（Sec. 4.2）。该惩罚是逆转崩塌的关键因果 knob：它主动抑制了解码器过度依赖前缀而忽略 $\mathbf{z}$ 的倾向。

证据强度方面，依赖性度量 $m_{t,0}$ 在 PSLD 下对有序序列稳定收敛至约 0.5，对打乱序列始终≥1（无依赖性错觉），直接证明了解码器对潜变量的敏感性的恢复（Fig. 2）。同时，消融实验和对比实验（Table 1, Table 3）证实移除 KL 或缺失 $\mathcal{L}^{\mathrm{CS}}$ 时性能大幅下降，说明三个 slot 变更是因果充分且必要的。

## 整体框架

**后验稳定潜在扩散 (Posterior-Stable Latent Diffusion, PSLD)** 框架通过重构变分推断与扩散过程的耦合方式，在保留扩散模型生成能力的同时，消除时间序列潜在扩散中普遍存在的后验崩塌。该框架的因果机制体现在两个关键设计：(1) 完全移除标准 VAE 中的 KL 正则化项，代之以将扩散过程的前几步解释为变分推断，从而允许任意形式的先验分布；(2) 利用扩散过程的后期步骤显式模拟后验崩塌场景，并通过一个“塌缩惩罚”损失强制解码器对非信息性潜在变量保持敏感，阻止其退化为忽略$\mathbf{z}$的强自回归模型。下面按模块描述其整体流程与输入输出关系。

**编码器**  
给定时间序列 $\mathbf{X}$，编码器 $\mathbf{f}^{\mathrm{enc}}$ 将其映射为一个初始潜在向量 $\mathbf{v} \in \mathbb{R}^{D}$，该向量作为扩散过程的起点 $\mathbf{z}^{0} = \mathbf{v}$（$D$ 为潜在维度）。编码器输出本身不引入具有显式概率形式的变分后验，这与重参数化技巧下的高斯后验有本质区别。

**变分推断：早期扩散步骤采样**  
从 $\mathbf{z}^{0}$ 出发，通过前向扩散过程在时间步 $i \in \{0,\ldots,N\}$（$N$ 为预设阈值）处采样得到实际使用的潜在变量：
$$ \mathbf{z} = \mathbf{z}^{i} \sim q^{\mathrm{forw}}(\mathbf{z}^{i} \mid \mathbf{z}^{0}) = \mathcal{N}\bigl(\mathbf{z}^{i}; \sqrt{\bar{\alpha}^{i}}\,\mathbf{z}^{0},\,(1-\bar{\alpha}^{i})\mathbf{I}\bigr), \quad i \sim \mathcal{U}\{0,N\}. $$
这里 $\bar{\alpha}^{i}$ 是扩散方差调度对应的累积缩放系数。该步骤将前向扩散解释为一种变分推断过程，完全摒弃了对 KL 散度的依赖，使得潜在变量的边缘分布可以自由地由扩散模型学习，不再被强制拉向标准高斯先验。

**自回归解码器**  
解码器 $\mathbf{f}^{\mathrm{dec}}$ 是自回归结构（可采用 LSTM 或 Transformer 作为骨干网络），它根据潜在变量 $\mathbf{z}$（视作首步观测 $\mathbf{x}_{0}$）和已生成的前缀序列 $\mathbf{X}_{1:t-1} = [\mathbf{x}_{1}, \ldots, \mathbf{x}_{t-1}]$ 逐步预测下一时刻的观测 $\mathbf{x}_{t}$：
$$ \mathbf{h}_{t} = \mathbf{f}^{\mathrm{dec}}(\mathbf{X}_{0:t-1}), \quad \mathbf{X}_{0:t-1} = [\mathbf{z},\,\mathbf{x}_{1},\,\ldots,\,\mathbf{x}_{t-1}]. $$
隐状态 $\mathbf{h}_{t}$ 随后用于生成 $\mathbf{x}_{t}$ 的条件分布 $p^{\mathrm{gen}}(\mathbf{x}_{t}\mid\mathbf{h}_{t})$（详细实现见附录）。

**训练损失：加权似然与塌缩惩罚**  
训练过程联合优化两个与解码器相关的损失项，同时训练一个 DDPM 去噪网络以学习潜在变量的真实先验分布。

- **变分推断损失** $\mathcal{L}^{\mathrm{VI}}$：从早期扩散步 $i\sim\mathcal{U}\{0,N\}$ 采样 $\mathbf{z}=\mathbf{z}^{i}$，然后计算解码器在整个序列上的加权负对数似然，
  $$ \mathcal{L}^{\mathrm{VI}} = \mathbb{E}_{i,\mathbf{z}^{0}}\bigl[ -\bar{\alpha}^{\gamma i}\,\ln p^{\mathrm{gen}}(\mathbf{X}\mid\mathbf{z}=\mathbf{z}^{i}) \bigr], $$
  其中 $\gamma$ 为衰减系数，确保噪声越大的潜在变量对似然的惩罚越弱，鼓励解码器对干净和含噪的 $\mathbf{z}$ 均保持合理建模能力。

- **后验崩塌模拟损失** $\mathcal{L}^{\mathrm{CS}}$：在扩散的后期步骤（远超 $N$）处采样高度噪声化的 $\mathbf{z}^{i}$，并计算其生成对数似然，以惩罚解码器对非信息性潜在变量赋予高置信度预测：
  $$ \mathcal{L}^{\mathrm{CS}} = \mathbb{E}_{i,\mathbf{z}^{i}}\bigl[ (1-\bar{\alpha}^{\lceil i/\eta\rceil})\,\ln p^{\mathrm{gen}}(\mathbf{X}\mid\mathbf{z}=\mathbf{z}^{i}) \bigr], $$
  该项权重随噪声水平升高而增大，显式模拟了后验崩塌下的极端情形，强迫解码器不得不依赖 $\mathbf{z}$（否则会在无信息输入时产生低似然预测），从而阻止其在训练中逐渐忽略潜在变量。

- **扩散去噪损失**（未显式编号）：一个标准 DDPM 损失（如噪声预测均方误差）被同时优化，使模型能够从纯噪声开始，通过反向扩散生成与训练数据一致的潜在变量，支撑推理阶段的采样。

**推理流程**  
生成时，首先从纯噪声 $\mathbf{z}^{T}\sim\mathcal{N}(0,\mathbf{I})$ 出发，通过训练好的反向扩散过程去噪得到 $\mathbf{z}$；然后以该 $\mathbf{z}$ 为上下文，利用自回归解码器逐步生成完整序列。扩散步骤的“随机早停”机制进一步确保了与训练所用 $\mathbf{z}^{i}$ 分布的一致性（详见算法 2）。

**关键度量工具**  
为定量评估后验稳定性，论文引入了依赖度量 $m_{t,0}$（全局依赖）与 $m_{t,t-1}$（局部依赖），通过积分梯度方法量化解码器隐表示 $\mathbf{h}_{t}$ 在预测 $\mathbf{x}_{t}$ 时分别对 $\mathbf{z}$ 与对最近前缀 $\mathbf{x}_{t-1}$ 的依赖程度。该度量用于验证：标准潜在扩散中 $m_{t,0}$ 随时间指数衰减至零（即后验崩塌），而 PSLD 框架下 $m_{t,0}$ 稳定在约 0.5（有序序列）或始终高于 1（打乱序列，表明无依赖错觉），证明解码器始终有效利用 $\mathbf{z}$。

## 核心模块与公式推导

PSLD 框架通过 **六个关键模块** 替代传统扩散模型的 VAE 阶段，消除后验崩塌并恢复潜在变量的控制力。

### 模块构成

| 模块 | 角色 | 锚点 |
|------|------|------|
| 编码器 $f^{\mathrm{enc}}$ | 将原始时间序列映射为初始潜在向量 $\mathbf{v}$ | Sec. 2 Eq. (1) |
| 早期扩散（变分推断） | 从 $\mathbf{z}^0 = \mathbf{v}$ 经前向扩散 $q^{\mathrm{forw}}(\mathbf{z}^i \mid \mathbf{z}^0)$ 采样 $\mathbf{z} = \mathbf{z}^i,\ i\sim\mathcal{U}\{0,N\}$ 作为潜在变量，**移除 KL 正则化** | Sec. 4.2 |
| 自回归解码器 $f^{\mathrm{dec}}$ | 接收潜在变量 $\mathbf{z}$ 和已生成的观测 $\mathbf{X}_{1:t-1}$，逐步预测 $\mathbf{x}_t$ | Sec. 3.2 Eq. (6) |
| 变分推断损失 $\mathcal{L}^{\mathrm{VI}}$ | 对早期扩散步的潜在变量加权负对数似然，促进解码器对噪声潜在变量的平滑依赖性 | Sec. 4.2 Eq. ($\mathcal{L}^{\mathrm{VI}}$) |
| 扩散模型 (DDPM) | 以标准去噪目标学习潜在变量的真实分布，支持从纯噪声采样生成 | Sec. 2 Eq. (5), Eq. (3)–(4) |
| 塌缩模拟惩罚 $\mathcal{L}^{\mathrm{CS}}$ | 强制解码器对后期扩散步产生的非信息性 $\mathbf{z}$ 保持敏感性，惩罚解码器对潜在变量的忽视 | Sec. 4.2 Eq. ($\mathcal{L}^{\mathrm{CS}}$) |

### 关键公式与变量含义

#### 1. 自回归解码器
$$ \mathbf{h}_{t} = \mathbf{f}^{\mathrm{dec}}(\mathbf{X}_{0:t-1}), \quad \mathbf{X}_{0:t-1} = [\mathbf{x}_{0}(=\mathbf{z}), \mathbf{x}_{1}, \ldots, \mathbf{x}_{t-1}] $$
- $\mathbf{h}_t$：解码器在时间步 $t$ 的隐状态。
- $\mathbf{f}^{\mathrm{dec}}$：以潜在变量和前缀观测为输入的自回归解码器（LSTM 或 Transformer 骨干）。
- $\mathbf{z}$：潜在变量，作为序列的第 0 个输入。

#### 2. 变分推断损失（取代 KL 项）
$$ \mathcal{L}^{\mathrm{VI}} = \mathbb{E}_{i \sim \mathcal{U}\{0,N\},\ \mathbf{z}^{0}}\, \bigl[ - \bar{\alpha}^{\gamma i} \ln p^{\mathrm{gen}}(\mathbf{X} \mid \mathbf{z} = \mathbf{z}^{i}) \bigr] $$
- $N$：变分推断所覆盖的前向扩散步数上限（论文中取 $N=50$）。
- $\bar{\alpha}^i = \prod_{k=1}^{i} (1 - \beta^k)$，前向扩散边际系数。
- $\gamma$：控制权重衰减速率的超参数。
- $\mathbf{z}^i$：从编码器输出 $\mathbf{z}^0$ 经前向扩散 $i$ 步得到的带噪声潜在变量。
- 权重 $\bar{\alpha}^{\gamma i}$ 随噪声增大而衰减，鼓励解码器对不同程度模糊的潜在变量均保持敏感。

#### 3. 塌缩模拟惩罚
$$ \mathcal{L}^{\mathrm{CS}} = \mathbb{E}_{i,\ \mathbf{z}^{i}}\, \bigl[ (1 - \bar{\alpha}^{\lceil i/\eta \rceil}) \ln p^{\mathrm{gen}}(\mathbf{X} \mid \mathbf{z} = \mathbf{z}^{i}) \bigr] $$
- $\eta$ 与 $\lceil i/\eta \rceil$ ：将扩散后期步划分为更粗粒度的“塌缩模拟”阶段。
- 该损失迫使解码器对**接近纯噪声的 $\mathbf{z}$** 仍保持有限的生成密度，从而惩罚强解码器忽略潜在变量的行为。

### 模块协作与后验稳定机制
1. 编码器输出 $\mathbf{v}$ 作为 $\mathbf{z}^0$，不再使用重参数化技巧输出 $\boldsymbol{\mu}, \boldsymbol{\sigma}$；
2. **早期扩散** 直接采样 $\mathbf{z}$，无需 KL 项，形成变分推断的无偏估计；
3. 解码器接收来自不同噪声水平的 $\mathbf{z}$，通过 $\mathcal{L}^{\mathrm{VI}}$ 的加权似然保持依赖性；
4. **塌缩模拟** 进一步用后期扩散的高噪声样本惩罚解码器的“无视”倾向，使 $\mathbf{z}$ 对解码输出的影响稳定维持（如 Fig. 2 所示，$m_{t,0} \approx 0.5$）。

> 依赖性度量 $m_{t,j}$ 的定义见 Sec. 3.2，用于量化不同输入变量对解码输出的贡献，但并非 PSLD 框架的结构模块，此处仅列出其形式供参考：
> $$ m_{t,j} = \frac{1}{\lVert\mathbf{h}_{t} - \widetilde{\mathbf{h}}_{t}\rVert^{2}} \Bigl\langle \mathbf{h}_{t} - \widetilde{\mathbf{h}}_{t},\ \sum_{k} x_{j,k} \int_{0}^{1} \frac{\partial \mathbf{f}^{\mathrm{dec}}(\gamma(s))}{\partial \gamma_{j,k}(s)}\, ds \Bigr\rangle $$
> 其中 $\gamma(s)$ 是从零点基线到实际输入的线性路径，总和 $\sum_j m_{t,j} = 1$。

## 实验与分析

### 主实验结果

PSLD 在三个真实时间序列数据集上一致大幅优于标准潜在扩散及其变体。表 1 报告了 Wasserstein 距离：在 MIMIC 上，PSLD（Transformer）仅 2.13，而标准潜在扩散为 5.02；在 WARDS 上差距更大（3.01 vs 7.46）；Earthquakes 上从 4.21 降至 2.49。与通过 KL 退火或跳跃连接等缓解后验崩塌的强基线相比，PSLD 的优势依然显著——例如在 WARDS 上，PSLD 比加入跳跃连接的基础模型低 1.66。LSTM 与 Transformer 两种骨干网络下的趋势一致，表明方法具有通用性。


![[assets/figures/papers/iclr26_0004_UbL2Fo0IvV_A_Study_of_Posterior_Stability_in_Time-Series_La/figures/005_Table_1.jpg]]

表 2 进一步将 PSLD 与互信息约束、逆 Lipschitz 约束等近期针对性方法，以及 Neural Temporal Point Process、FreqDiff 等其他时间序列生成模型对比，PSLD 同样取得最低 Wasserstein 距离。在额外的 UCI 数据集（Retail、Energy）上，PSLD 在 MMD 指标下同样显著超过标准潜在扩散与跳跃连接基线（PSLD 在 Retail 上 MMD = 0.025，基线最优 0.033；Energy 上 0.031 对比 0.046），证实了其跨数据集和跨指标的稳健性。

这些性能提升的因果根源在于 PSLD 去除了危险的 KL 正则化，并通过扩散过程后期步骤模拟后验崩塌来强制解码器对潜在变量保持敏感，从而避免了 Proposition 3.1 所述的后验崩塌导致的扩散模型退化问题。

### 消融实验

表 3 的系统消融揭示了两个核心超参数的作用。扩散早期步骤数 N 与后验崩塌惩罚中使用的后期步骤数 M 的最优值分别为 N=50, M=100，任何偏离均导致 Wasserstein 距离上升。若将 M 设为 0（即完全移除坍缩模拟损失 $\mathcal{L}^{\mathrm{CS}}$），性能退化至与标准潜在扩散接近的水平，直接验证了该惩罚的必要性。为潜在扩散加入跳跃连接虽能改善性能（MIMIC 从 5.02 降至 3.75），但仍远远不及 PSLD（2.13），说明仅增强解码器结构无法根除后验崩塌，PSLD 的变分推断重构与惩罚机制更为根本。


![[assets/figures/papers/iclr26_0004_UbL2Fo0IvV_A_Study_of_Posterior_Stability_in_Time-Series_La/figures/007_Table_3.jpg]]
*Table 3: Ablation studies of the hyper-parameters N, M, which are respectively used in the estimations of likelihood loss $\boldsymbol { \mathcal { L } } ^ { \mathrm { V I } }$ and collapse penalty $\mathcal { L } ^ { \mathrm { C \ddot { S } } }$ . Here LD is short for latent diffusion and the symbol − means “Not Applicable”

关于训练与推理开销，表 4 显示 PSLD 的训练时间比标准潜在扩散长约 40 分钟（MIMIC 上 2 小时 50 分钟 vs 2 小时 10 分钟），但推理时间仅增加约 5 秒，性能提升完全可接受。


![[assets/figures/papers/iclr26_0004_UbL2Fo0IvV_A_Study_of_Posterior_Stability_in_Time-Series_La/figures/008_Table_4.jpg]]
*Table 4: Comparison of Training and Inference Times on the MIMIC dataset*

### 后验稳定性验证

PSLD 从根本上消除了后验崩塌，这由依赖性度量 $m_{t,0}$ 的定量变化直接佐证。标准潜在扩散中（Fig. 1），$m_{t,0}$ 随解码步数指数衰减至零，表明潜在变量对解码器的影响在预测早期即消失，扩散模型退化。而 PSLD 下（Fig. 2），对于有序时间序列，$m_{t,0}$ 迅速稳定在约 0.5，说明潜在变量在整个解码过程中始终保持实质性影响；对于打乱的时间序列，$m_{t,0}$ 始终大于等于 1，未出现标准潜在扩散中的“依赖性错觉”，表明解码器对潜在变量的敏感性源于真实结构依赖而非虚假相关。这一结果与 PSLD 的变分推断框架一致：早期扩散步骤提供含噪但信息充分的 $\mathbf{z}$，坍塌模拟惩罚则防止了解码器忽略潜在变量，二者协同实现了后验稳定。


![[assets/figures/papers/iclr26_0004_UbL2Fo0IvV_A_Study_of_Posterior_Stability_in_Time-Series_La/figures/002_Figure_1.jpg]]
*Figure 1: Dependency measures $m _ { t , 0 } , m _ { t , t - 1 }$ averaged over 500 multivariate time series, with 3 standard deviations as the error bars. We can see that the latent variable z of latent diffusion has a vanishing impact on the decoder $\mathbf { f } ^ { \mathrm { d e c } }$ . , a typical symptom of posterior collapse. We also observe a phenomenon of dependency illusion in the case of shuffled time series

![[assets/figures/papers/iclr26_0004_UbL2Fo0IvV_A_Study_of_Posterior_Stability_in_Time-Series_La/figures/004_Figure_2.jpg]]
*Figure 2: The results of averaged dependency measures and error bars for our framework, which should be compared with those (e.g., Fig. 1) of latent diffusion, showing that our framework has a stable posterior and is without dependency illusion*

### 失败模式与针对性局限

PSLD 在时间序列文本数据（ATIS、SNIPS）上同样显著优于基线（如带跳跃连接的潜在扩散），验证了该方法对一般离散序列潜在扩散的推广性。然而，在 CIFAR‑10 图像数据集上，PSLD 的 FID 仅从 3.91 降至 3.85，改善微小。这一现象恰从反面印证了本工作的核心论断：图像潜在扩散极少发生后验崩塌，因此 PSLD 的针对性改进在需要更强后验依赖性的时间序列领域才能体现显著作用。若任务本身已无严重后验崩塌，该方法不能带来额外增益。

### 补充图表

![[assets/figures/papers/iclr26_0004_UbL2Fo0IvV_A_Study_of_Posterior_Stability_in_Time-Series_La/figures/009_Table_5.jpg]]
*Table 5: Comparison on two new time-series datasets, with another metric: MMD*


## 方法谱系与知识库定位

本研究提出的后验稳定潜在扩散（PSLD）框架直接回应了时间序列潜在扩散中长期被忽视的后验崩塌问题。与标准潜在扩散（Latent Diffusion）及其各类缓解变体相比，PSLD并非渐进修补，而是从变分推断的机制上重置了潜在变量的角色：标准方法通过 KL 正则化迫使潜在变量服从高斯先验，与强自回归解码器形成对抗，极易导致潜在变量在解码环节影响力消失，扩散模型退化为弱 VAE（Proposition 3.1）。PSLD 则完全移除 KL 正则化，改用扩散过程的前若干步作为变分推断，使后验采样无需显式正则即可获得平滑且信息丰富的潜在表示；同时利用扩散后期步骤模拟后验崩塌，通过塌缩模拟惩罚（$\mathcal{L}^{\mathrm{CS}}$）强制解码器保持对非信息性潜在变量的敏感性。这一因果杠杆的设计使潜在变量的控制力在生成全程保持稳定，从根本上切断了后验崩塌的传导链。

在方法谱系中，PSLD 可以被视为对两类路线的整合与超越。第一类是直接针对后验崩塌的对抗手段，例如 KL 退火、跳跃连接增强、互信息约束以及逆 Lipschitz 约束。这些方法虽然能在一定程度上提升解码器对潜在变量的依赖，但普遍存在折衷代价或效果有限：KL 退火降低了正则化强度，却无法保证解码器长期敏感；跳跃连接虽然增强了信息通路，实验显示其仅能将 MIMIC 上的 Wasserstein 距离从 5.02 降至 3.75，仍远高于 PSLD 的 2.13（Table 3），说明该路径并未瓦解崩塌的根本机制。第二类是其他时间序列生成模型，如神经时间点过程（NTPP）和频率域扩散模型 FreqDiff等，它们在特定领域表现优异，但缺乏对潜在变量–解码器互动的结构性保障，难以稳定捕获长时序依赖。PSLD 在 Transformer 与 LSTM 两种骨干网络上均取得一致优势，Wasserstein 距离与 MMD 均显著优于上述所有基线（Table 1, 2, 5），且不需要领域特定的先验假设，展现出较强的通用性。

适用边界与局限性同样清晰。该框架的因果机制高度针对时间序列潜在扩散的后验崩塌，因此当任务本身不易发生崩塌时改善幅度有限。在图像生成实验（CIFAR-10，FID 指标）中，PSLD 仅将 FID 从 3.91 微降至 3.85，表明图像领域的潜在扩散后验通常已相对稳定，PSLD 的额外结构收益很小。训练时间比标准潜在扩散约长 40 分钟（2h50min vs 2h10min），推理时间仅增加 5 秒（Table 4），说明开销可控但需要批量训练时需权衡额外成本。超参数 $N$（用于早期扩散步骤）和 $M$（用于塌缩惩罚）对性能敏感，偏离最优配置（$N=50, M=100$）时 Wasserstein 距离会明显回升（Table 3），这要求在不同数据集上可能需要重新搜索，自动化调参仍是挑战。

本工作留下的开放问题同样值得关注。依赖度量 $m_{t,j}$ 中的路径积分（Definition 3.2）如何高效近似实现，论文未给出具体的数值近似算法，这可能影响该度量在大规模或高维序列上的泛化诊断能力。此外，当前框架仍假设扩散过程的前向与逆向均为高斯转移，对非高斯时序（如计数、事件序列）的适用性尚待验证。后验崩塌的惩罚策略是否可推广到更复杂的层次化潜在结构或条件扩散模型，也是未来一待探索的方向。最后，PSLD 在互信息约束、逆 Lipschitz 等强基线对比中虽已领先，但在极端稀疏观测或高缺失率时序场景下的鲁棒性仍需独立评估。

## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/A_Study_of_Posterior_Stability_in_Time_Series_Latent_Diffusion.pdf

![[paperPDFs/ICLR_2026/A_Study_of_Posterior_Stability_in_Time_Series_Latent_Diffusion.pdf]]
