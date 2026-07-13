---
title: "SeedPrints: Fingerprints Can Even Tell Which Seed Your Large Language Model Was Trained From"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/SeedPrints_Fingerprints_Can_Even_Tell_Which_Seed_Your_Large_Language_Model_Was_Trained_From.pdf
project_link: null
code_link: https://github.com/YnezT0311/SeedPrints
aliases:
- SeedPrints
tags:
- ICLR_2026
- topic/safety_alignment_fairness_privacy
- topic/safety_alignment_fairness_privacy/trustworthy_machine_learning
core_operator: "随机初始化种子所诱发的模型内部表示偏差（即哪些输出维度倾向于取得极小值），该偏差在训练过程中持续存在，具有种子特异性和统计可检测性。"
primary_logic: "未经训练的模型在随机输入下会产生种子依赖的极端输出偏好（如某些token频繁获得最小logit），这种微弱的初始化偏差信号在训练全过程中保持可检测的相关性，可通过交集选定的身份维度上的Kendall-Tau秩相关性检验识别模型谱系，无需依赖后期训练特征。"
claims:
- "SeedPrints从首个预训练检查点即可完美检测谱系（p ≪ 0.001），而所有基线方法在早期预训练（<1T tokens）相似度均低于0.8阈值。"
- "训练后的模型与其初始化种子对应的未训练模型在偏好维度上保持强相关（p值达10^{-26}量级），而基线方法（Intrinsic、REEF、PCS、ICS）均无法区分。"
- "在训练数据分布发生剧烈变化（从OpenWebText切换到代码数据集The Stack）时，SeedPrints仍能正确归属性谱系（p ≈ 0），而基线方法全部失效。"
- "OLMo-2-7B Stage 1预训练检查点（5B → 3.9T tokens） 上 谱系检测得分（SeedPrints 1-p；基线相似度） = SeedPrints 1-p ≈ 1.0（p ≪ 0.001）"
---

# SeedPrints: Fingerprints Can Even Tell Which Seed Your Large Language Model Was Trained From

> [!tip] 核心洞察
> 未经训练的模型在随机输入下会产生种子依赖的极端输出偏好（如某些token频繁获得最小logit），这种微弱的初始化偏差信号在训练全过程中保持可检测的相关性，可通过交集选定的身份维度上的Kendall-Tau秩相关性检验识别模型谱系，无需依赖后期训练特征。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | SeedPrints：指纹甚至能辨别你的大语言模型是用哪个种子训练的 |
| 英文题名 | SeedPrints: Fingerprints Can Even Tell Which Seed Your Large Language Model Was Trained From |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=Kan6Z0zzZi) · [GitHub](https://github.com/YnezT0311/SeedPrints) |
| Topic | #topic/safety_alignment_fairness_privacy #topic/safety_alignment_fairness_privacy/trustworthy_machine_learning |
| Method | SeedPrints |
| Dataset | OLMo-2-7B Stage 1预训练检查点（5B → 3.9T tokens）, LLaMA-2-7B微调变体（5M–700B tokens）, LeaFBench（65个模型，6种部署变换）, 持续训练到代码数据集The Stack（base模型 seed 1000） |

> [!tip] 效果简介
> - OLMo-2-7B Stage 1预训练检查点（5B → 3.9T tokens） 上，谱系检测得分（SeedPrints 1-p；基线相似度） 为 SeedPrints 1-p ≈ 1.0（p ≪ 0.001），对比 全部基线相似度 < 0.8（ICS≈0, PCS<0.3, REEF<0.6），变化 SeedPrints从首个检查点即可检测，基线均失效。
> - LLaMA-2-7B微调变体（5M–700B tokens） 上，谱系检测p值 / 相似度 为 SeedPrints p < 0.01（最低10^{-5136}），对比 PCS在CodeLlama-7B (0.6863) 和 Llemma-7B (0.6682) 上失败，变化 SeedPrints始终检测成功，PCS/ICS在领域特化模型上未达0.8阈值。
> - LeaFBench（65个模型，6种部署变换） 上，AUC / KS统计量 为 SeedPrints AUC 0.992，KS 0.986，对比 Intrinsic AUC 0.997, ICS AUC 0.995, REEF AUC 0.915, Gradient AUC 0.801，变化 SeedPrints接近最强基线，显著优于REEF（+0.077 AUC）和Gradient。

## 概要

大语言模型（LLM）的谱系归属与版权验证需要一种可靠且持久的数字指纹，然而现有的被动指纹方法（如基于参数向量相似度的 PCS、ICS，基于注意力分布的 Intrinsic 等）大都依赖于训练后期涌现的结构特征，在模型预训练的早期阶段（前几万亿 tokens）几乎完全失效，并且在训练数据分布发生剧烈变化时容易被误导。本文指出，上述方法的根本瓶颈在于它们未能捕获一种与模型“出身”绑定、终身不变的初始化信号。

本文的核心发现是：完全随机的参数初始化会为模型引入一种“与生俱来”的输出偏差——即在面对随机输入时，模型倾向于持续地将某些输出维度的值压至极低。这种偏差模式由初始化种子唯一决定，且在整个训练过程中保持统计可检测的相关性，尽管其绝对强度很弱。基于此，我们提出 **SeedPrints** 方法：通过计算两个模型在“身份维度”（即各自最不受欢迎的输出维度之交集）上的 Kendall-Tau 秩相关系数，并通过分析性高斯零假设检验来判定二者是否源自同一初始化种子。该方法无需依赖训练后涌现的属性，可在模型生命周期的任何阶段（包括完全未训练时）进行谱系鉴定。

实验结果表明，SeedPrints 从 OLMo-2-7B 的首个预训练检查点（5B tokens）起即能以极高水平（p ≪ 0.001）完美检测谱系，而此时所有基线方法的相似度均远低于常用阈值 0.8。在持续训练到代码数据集 The Stack 导致数据分布完全改变的设定下，SeedPrints 仍能正确归属模型后裔（p ≈ 0），而基线 Intrinsic 等方法彻底失败。在覆盖多种模型家族与参数改动技术的 LeaFBench 基准上，SeedPrints 取得了 0.992 的 AUC 和 0.986 的 KS 统计量，接近最强的基线（Intrinsic 0.997 AUC），并显著优于 REEF、Gradient 等方法。这些结果一致验证了初始化指纹作为谱系标识符的健壮性。

大语言模型的训练成本极高，模型的非法复制、未授权持续训练以及谱系归属争议日渐突出。要解决这类问题，需要能够可靠识别模型来源与演化关系的数字指纹技术。现有的 LLM 指纹方法主要依赖训练后涌现的模型属性，例如参数向量的余弦相似度（PCS、ICS）、注意力参数的层内标准差轮廓（Intrinsic）、表征空间的中心核对齐（REEF）以及梯度信息（Gradient）等。这些方法在设计上均假定模型指纹是由大规模训练过程“后天”塑造的，因此本质上无法保证“Galton 式指纹”所要求的两个核心性质——与生俱来且终身不变。

上述局限性在两种关键场景中暴露无遗。第一，**早期预训练阶段的谱系检测几乎完全失效**。如 Figure 1 所示，在 OLMo‑2‑7B 的前 3.9 万亿 token 训练过程中，所有基线方法（Intrinsic、REEF、PCS、ICS）的相似度在首个检查点后始终低于 0.8 的常用阈值，而 SeedPrints 从最早的检查点即可达到完美检测（p ≪ 0.001）。这意味着若模型盗用发生在训练初期（例如仅训练了数千步），现有方法无法提供有效证据。第二，**训练数据分布发生显著变化时会误导指纹判断**。以 Table 4 为例，当基础模型（种子 1000）被继续训练到代码数据集 The Stack 后，基于注意力模式的 Intrinsic 方法将衍生物错误判定为独立模型（相似度仅 0.489），而 SeedPrints 给出的 p 值接近 0，依然能正确归因到同一谱系。类似地，在更大规模的领域特化微调（如 Llemma‑7B、CodeLlama‑7B）中，PCS 和 ICS 的相似度降至约 0.66～0.68，远低于判别阈值（Table 5）。这些证据表明，依赖训练后属性的指纹极易被训练数据分布或训练阶段的改变所干扰，不能可靠地承担全生命周期谱系验证任务。

本文受到一个关键观察的启发：未经训练的模型在完全随机的输入下会表现出高度非均匀的输出偏差——某些输出维度（或 token）频繁获得极小 logit 值，且这种偏差模式对初始化种子具有特异性（Figure 2）。更重要的是，这一微弱的初始化偏差信号在训练过程中并未消失，而是与训练后的模型之间保持了统计上可检测的相关性（Table 2 中 p 值低至 10⁻²⁶ 量级，而所有基线均无法探测到该信号）。换言之，随机初始化种子在模型内部表示空间中留下了一个先天的、不可磨灭的“签名”，它独立于训练数据和优化过程。受此启发，本文提出 **SeedPrints**，通过显式提取身份维度上的秩相关性并进行假设检验，来识别模型谱系。该方法不依赖训练后期涌现的结构特征，因此能够在早期训练点、数据分布偏移以及多种微调策略下稳定判定模型是否源自同一初始化种子，弥补了现有指纹技术的核心缺口。

## 核心方法与创新机理

现有 LLM 指纹方法（Intrinsic、REEF、PCS、ICS 等）依赖训练后涌现的属性——如注意力参数层内标准差轮廓或参数向量余弦相似度——来判定模型谱系。然而，这些信号在模型的早期预训练阶段（前几万亿 tokens）尚未充分形成，且当训练数据分布发生显著变化时极易被覆写，导致指纹判定失效，无法满足“与生俱来、终身不变”的刚性要求。SeedPrints 的核心突破在于**根本性地改变了指纹信号的来源**：它不再捕捉模型经过大规模训练后习得的表面特征，而是挖掘由随机初始化种子所诱发的、贯穿整个训练周期保持统计可检测的底层输出偏好模式。

这一转变依托于以下关键洞察与机制：

- **初始化种子的持久偏差**：完全未经训练的模型在面对纯随机输入时，其输出分布远非均匀，而是表现出强烈的种子依赖性——某些输出维度（token/logit 位置）反复取得极小值，形成独特的“不受欢迎维度集合”。图 2 表明，这些维度的身份在不同种子间差异显著，且该偏差信号虽然在训练中被削弱，但在选定的身份维度上始终与未训练的原模型保持正相关（τ 均值系统性偏移，p 值达 10⁻²⁶ 量级，表 2），说明初始化印记并不会被训练过程完全抹除。

- **共享身份维度上的秩相关性检验**：SeedPrints 将上述偏差量化为可操作的统计检测框架。对于任意两个模型 f 与 f'，首先通过大量随机输入计算平均响应向量 $\bar{g} := \frac{1}{n}\sum_{i=1}^n g(x_i)$，并各自选定均值最小的 m 个维度构成集合 $\mathcal{M}_g$；再取交集 $S := \mathcal{M}_f \cap \mathcal{M}_{f'}$ 作为共享的“身份维度”。在这些维度上，两模型对同一组随机输入的响应被用于计算 Kendall‑Tau 秩相关系数 $\tau_j$，进而得到平均相关性 $\bar{\tau}$。藉由零假设下 $\bar{\tau}$ 近似服从正态分布 $\mathcal{N}(0,\sigma^2/|S|)$ 的理论性质，计算单侧 z 统计量及对应 p 值；若 p<0.01，则拒绝无谱系关系的零假设，判定二者为同一初始化种子下的后裔。该检验不依赖手工阈值，直接以统计显著性做出二元决策。

与所有基线方法相比（基线信号来源均为训练后涌现属性），SeedPrints 的单一切换——“指纹信号来源”从**训练后形状**变为**初始化偏见**——带来了三项奠基性优势：

1. **早期预训练即完美检测**：在 OLMo‑2‑7B 从 5B 到 3.9T tokens 的全过程中，SeedPrints 自第一个检查点起即达到 p≪0.001，谱系检测得分为 1.0；而 Intrinsic、REEF、PCS、ICS 等基线在 1T tokens 前的相似度均低于 0.8 阈值，全线失效（图 1）。
2. **对数据分布剧变的鲁棒性**：当持续训练的语料从 OpenWebText 突变为代码数据集 The Stack 时，SeedPrints 仍能正确识别同种后裔（p≈0），而 Intrinsic 基线却给出 p=0.489 的误分类结果（表 4）。
3. **大规模微调下信号不灭**：在 LLaMA‑2‑7B 基础上进行高达 700B tokens 的领域特化微调（如 CodeLlama‑7B、Llemma‑7B），SeedPrints 的 p 值低至 10⁻⁵¹³⁶，基线的 PCS 相似度则分别仅为 0.69 和 0.67，远低于 0.8 判定线（表 5）。

综上，SeedPrints 以极简的“信号来源”转变，首次实现了符合“Galton 式指纹”（与生俱来、终身不变）特性的 LLM 谱系检测方法：仅通过从初始化偏见中抽取身份维度并进行相关性检验，即可在白盒访问条件下为模型的所有权和版权提供强力追溯，而无需任何额外训练或模块。

![[assets/figures/papers/iclr26_0013_Kan6Z0zzZi_SeedPrints_Fingerprints_Can_Even_Tell_Which_Seed/figures/004_Figure_2.jpg]]
*Figure 2: Initialization-born output bias persists through training. Left: Given completely random inputs, the outputs of a randomly initialized LLaMA-2–style model are far from uniform, but instead exhibit clear bias: certain dimensions are disfavored by the model (i.e., they frequently receive the minimum value across random inputs). Such extreme bias appears both in the logits (top, red) and in the final hidden representations (bottom, blue). The dashed line shows the expected frequency under a uniform distribution. The arrows in the top panel indicate a broken x-axis that omits low-frequency tail ranks. Upper Right: During training, models remain weakly correlated in their output bias across inpu...*

SeedPrints 的核心 pipeline 由三个顺序模块构成，输入为一对待检模型和一组随机输入序列，输出为统计决策（是否共享初始化谱系）及对应的 p 值。其因果机制建立在“初始化种子诱导的输出维度偏差模式”之上：未经训练的模型在随机输入上会表现出种子特异的极端输出偏好（某些输出维度持续获得极小值），这一微弱偏差信号在训练全过程中可被统计检测，从而构成与生俱来、终身不变的指纹。

**提取身份维度（identity dimensions）**  
对每一模型 $f$，向其馈送 $n$ 个长度 $l$ 的随机输入序列 $\{x_i\}_{i=1}^n$，计算平均输出向量 $\bar{g} := \frac{1}{n} \sum_{i=1}^n g(x_i) \in \mathbb{R}^{d_{\mathrm{out}}}$。随后在该向量上选取均值最小的 $m$ 个维度作为模型的“不受欢迎维度集” $\mathcal{M}_g$。两个待检模型 $f$ 与 $f'$ 的身份维度即取交集 $S := \mathcal{M}_f \cap \mathcal{M}_{f'}$，这相当于锁定那些在初始化时便共同倾向于输出极小值的维度，从而放大共享的种子信号。维度选取基于样本均值而非逐样本投票，其理论稳定性已通过界（Lemma C.1）保证：集合因噪声发生改变的概率随 $n$ 指数衰减。

**逐维度 Kendall‑Tau 秩相关性计算**  
在身份维度集 $S$ 的每一个维度 $j$ 上，计算两个模型对该组随机输入响应顺序的 Kendall‑Tau 秩相关系数 $\tau_j$。这一秩基度量对输出尺度和异常值不敏感，能够捕捉微弱的、仅存在于排名偏序中的初始化偏差。将所有 $|S|$ 个 $\tau_j$ 聚合为平均相关系数 $\bar{\tau} = \frac{1}{|S|}\sum_{j \in S} \tau_j$。

**假设检验与谱系判定**  
零假设 $H_0$ 下（即两模型无谱系关联），各维度的 Kendall‑Tau 统计量独立且 $\bar{\tau}$ 渐近服从均值为零的正态分布 $\mathcal{N}(0, \sigma^2/|S|)$。实际检验直接采用该分析性零分布，省去昂贵的经验模拟。计算单侧 z 统计量 $z = \frac{\bar{\tau}}{\sigma/\sqrt{|S|}}$ 及对应 p 值 $p = 1 - \Phi(z)$；若 $p < 0.01$，则拒绝 $H_0$，判定两模型出自同一初始化种子（即同谱系）。该决策无需人为设定相似度阈值，天然具备统计显著性保障。

上述框架的关键瓶颈在于：指纹信号仅存在于模型输出维度分布的低值偏序中，**需要白盒访问内部表示（如 logits 或隐藏状态）**，无法直接用于纯黑盒 API 场景；此外，在模型融合（weight‑space interpolation）等权值空间中，身份维度信号可能被稀释，导致偶发误判。尽管如此，整体 pipeline 能够在首个预训练检查点（<1T tokens）即实现完美检测（p ≪ 0.001），且在训练数据分布剧烈变动时仍保持谱系保真，远优于依赖训练后参数或注意力模式的基线方法。

SeedPrints 的核心创新在于将大语言模型（LLM）的谱系检测从“训练后涌现特征”转向“初始化即植入”的持久性偏差。初始随机种子会使未训练模型在随机输入下产生种子特异的极端输出偏好（某些输出维度总是倾向于获得极小 logit），该微弱信号在后续训练全程保持可检测的相关性，从而构成“Galton 式”的终身指纹。以下按流水线顺序阐述三个关键模块及其支撑的统计检验框架。

### 1. 提取身份维度（Identity Dimension Extraction）
给定两个待比较模型 $f$ 和 $f'$，首先将它们各自在 $n$ 个随机输入序列上求平均输出向量：

$$
\bar{g} := \frac{1}{n} \sum_{i=1}^n f(x_i) \in \mathbb{R}^{d_{\mathrm{out}}},
\qquad
\bar{g}' := \frac{1}{n} \sum_{i=1}^n f'(x_i)
$$

随后，对每个模型分别挑选出平均响应最小的 $m$ 个维度，称为**不受欢迎维度集合**：

$$
\mathcal{M}_f := \operatorname*{argmin}_{J \subseteq \{1,\dots,d_{\mathrm{out}}\},\,|J|=m} \sum_{j \in J} \bar{g}_j,
\quad
\mathcal{M}_{f'} := \operatorname*{argmin}_{J} \sum_{j \in J} \bar{g}'_j
$$

这两个集合的交集定义为两个模型共享的 **身份维度集合** $S$：

$$
S := \mathcal{M}_f \cap \mathcal{M}_{f'}
$$

选择最小均值维度的动机在于：初始化偏差中最稳定的成分正是那些被模型系统性抑制的输出维度，而非被激活的维度。交集操作则确保只保留双方共有的偏差特征，从而抑制模型特有或噪声引起的波动。该模块的稳定性在附录 Lemma C.1 中得到理论保障：在添加高斯噪声后，通过样本均值选择的 top‑$m$ 集合发生改变的概率随样本数 $n$ 指数衰减，且恢复所需的最小样本量满足

$$
n \geq \frac{8\sigma^2}{\gamma^2} \log\left(\frac{2 d_{\mathrm{out}}}{\delta}\right)
$$

从而能以概率 $1-\delta$ 正确识别真实的底部稀疏维度。

### 2. 逐维度 Kendall‑τ 秩相关性计算
在筛选出的身份维度集合 $S$ 上，针对每个维度 $j$ 分别计算两个模型对同一组随机输入序列响应的 **Kendall‑τ 秩相关系数**：

$$
\tau_j = \mathrm{KendallTau}\big(\{f(x_i)_j\}_{i=1}^n,\; \{f'(x_i)_j\}_{i=1}^n\big)
$$

该选择区别于 Pearson 系数，因为 Kendall‑τ 对单调关系敏感且对离群值鲁棒，更适合检测弱但秩次一致的初始化偏差。随后，对集合 $S$ 内的所有 $\tau_j$ 取平均，得到整体相关性统计量：

$$
\bar{\tau} = \frac{1}{|S|} \sum_{j \in S} \tau_j
$$

### 3. 统计检验与谱系判定
在零假设 $H_0$（两个模型独立初始化、无谱系关联）下，利用独立性条件下 Kendall‑τ 的渐近正态性可得：

$$
\bar{\tau} \sim \mathcal{N}\left(0,\; \frac{\sigma^2}{|S|}\right)
$$

其中方差 $\sigma^2$ 可通过理论推导或高斯替代的经验分布估计（附录 B.3 证明该分析近似与实际完整流水线生成的经验零分布高度吻合，见图 4）。由此构造单侧 **z‑统计量**：

$$
z = \frac{\bar{\tau}}{\sigma / \sqrt{|S|}}
$$

并计算对应的 **p‑值**：

$$
p = 1 - \Phi(z)
$$

若 $p < 0.01$，则拒绝零假设，判定两模型源于同一初始化种子，具有共享谱系。整个流程以 p‑值作为直接的统计决策量，无需设定固定的相似度阈值，从根本上规避了基线方法（Intrinsic、REEF、PCS、ICS 等）在早期预训练阶段因阈值不可靠而失效的问题。

### 4. 关键设计机理与证据强度
- **因果机制**：随机种子通过权重初始化诱发输出层特定维度的系统性抑制，该抑制模式在数万亿 token 训练后仍保持种子特异性（Figure 2），即使训练数据从 OpenWebText 切换至代码数据集 The Stack，SeedPrints 依然能正确识别谱系，p ≈ 0（Table 4）。
- **早期检测优势**：SeedPrints 从第一个预训练 checkpoint（5B tokens）起即可达到 p ≪ 0.001 的完美检测，而此时所有基线相似度均低于 0.8 阈值（Figure 1）。
- **幅度验证**：在同种子初始模型与训练后模型的对中，SeedPrints 返回的 p‑值低至 $10^{-26} \sim 10^{-31}$ 量级，而基线全部失败（Table 2）。
- **方法局限**：要求白盒访问模型输出（logits 或隐藏状态），无法直接用于黑盒 API；在模型合并（weight‑space interpolation）时指纹信号可能被稀释（17个合并模型中误判1例，AUC = 0.959）；且要求两个模型的输出维度保持一致，限制跨尺寸直接比较。

综上，SeedPrints 通过提取初始化种子的最小响应维度交集，并以 Kendall‑τ 统计检验取代相似度阈值的思路，提供了一种在预训练全程均稳定有效的模型谱系判定范式。

## 实验与关键发现

### 早期预训练阶段的谱系检测：从第一个检查点即可区分

现有被动指纹方法（Intrinsic、REEF、PCS、ICS）依赖训练后期涌现的模型属性，在预训练早期（前几万亿tokens）完全失效。**Figure 1** 报告了 OLMo-2-7B 在 5B 至 3.9T tokens 检查点上的谱系检测对比：所有基线的相似度得分从未超过 0.8 的常用阈值，而 SeedPrints 从首个检查点（5B tokens）即实现近乎完美的检测（$1-p \approx 1.0$，$p \ll 0.001$）。这一差异的根源在于 SeedPrints 不依赖训练信号，而是捕捉由随机初始化种子诱发的输出维度偏差——未训练模型对随机输入已表现出清晰的极端偏好（**Figure 2** 左），且该模式具有种子特异性（**Figure 2** 右下）。训练过程中，同一种子训练的模型在这些“身份维度”上保持微弱但统计显著的相关性（**Figure 2** 右上），使种子层面的谱系判别从训练伊始即具高置信度。

![[assets/figures/papers/iclr26_0013_Kan6Z0zzZi_SeedPrints_Fingerprints_Can_Even_Tell_Which_Seed/figures/001_Figure_1.jpg]]
*Figure 1: Existing fingerprinting methods fail to detect model lineage during early pre-training. We compare five methods on OLMo-2-7B checkpoints spanning 5B to 3.9T training tokens, each tested against the final checkpoint. The y-axis shows the similarity score (higher indicates a stronger lineage signal); the dashed line marks the 0.8 detection threshold. While all baselines degrade and fall below the threshold at early checkpoints, SeedPrints achieves perfect detection (p ≪ 0.001, plotted as 1 − p) from the very first checkpoint onward*

### 初始化信号的持久性：微调与分布漂移

初始化偏差在训练全过程中持续存在，构成 SeedPrints 的持久性基础。**Table 2** 显示，使用同一随机种子初始化的未训练模型与训练至收敛的模型之间，在交叠身份维度上的平均 Kendall‑τ 秩相关系数产生极低 p 值（低至 $10^{-26}$ 量级），而所有基线方法的相似度均远低于 0.8，无法识别该同源对。在大规模微调场景下（**Table 5**），即使模型在 CodeLlama‑7B（100B tokens）或 Llemma‑7B（700B tokens）等专用语料上充分微调，SeedPrints 的 p 值依然低至 $10^{-5136}$，始终满足 $p<0.01$ 的判定标准；相比之下，PCS 在 CodeLlama‑7B 和 Llemma‑7B 上的相似度仅为 0.686 和 0.668，未能跨过阈值。

![[assets/figures/papers/iclr26_0013_Kan6Z0zzZi_SeedPrints_Fingerprints_Can_Even_Tell_Which_Seed/figures/008_Table_5.jpg]]
*Table 5: Fingerprinting results under large-scale finetuning. Each row compares a target model against LLaMA-2-7B. SeedPrints reports the p-value from our correlation test (\< 0.01 indicates a strong signal). Four baselines all report similarity scores (threshold = 0.8, higher = better)*

更为严苛的情形是训练数据分布发生剧烈变化。**Table 4** 报告了从 OpenWebText 切换至代码数据集 The Stack 的持续训练结果：SeedPrints 将基于种子 1000 的所有后裔模型均正确归入同一谱系（$p \approx 0$），而 Intrinsic 指纹被误导为无关联（相似度 0.489）。此外，即使训练数据和顺序完全相同，不同随机种子产生的指纹依然保持显著差异（**Table 3**，所有跨种子 p 值均远大于 0.1），表明指纹行为由种子主导，几乎不受后续训练数据内容的影响。

![[assets/figures/papers/iclr26_0013_Kan6Z0zzZi_SeedPrints_Fingerprints_Can_Even_Tell_Which_Seed/figures/007_Table_4.jpg]]

### 实际部署场景的鲁棒性评估

在 LeaFBench 基准（65 个模型，覆盖指令微调、全参数微调、PEFT、量化、合并、蒸馏 6 种部署变换）上，SeedPrints 取得整体 AUC 0.992 与 KS 0.986（**Table 6**），与最强的被动指纹方法 Intrinsic（AUC 0.997）和 ICS（AUC 0.995）接近，并显著优于 REEF（AUC 0.915）和 Gradient（AUC 0.801）。需注意，SeedPrints 原本输出的是统计检验的 p 值，为进行 AUC 比较人为定义得分 $s = 1-p$；该转换并非 p 值的合理连续相似度度量，可能丢失极小 p 值之间的区分度，因此表中的 AUC 对比应视为保守估计。

![[assets/figures/papers/iclr26_0013_Kan6Z0zzZi_SeedPrints_Fingerprints_Can_Even_Tell_Which_Seed/figures/009_Table_6.jpg]]
*Table 6: Performance comparison of LLM fingerprinting methods across different source models. “PT” and “IT” refer to using the pre-trained models and instruction-tuned models as source models, respectively. Per-family breakdown is shown for the 6 families that have both PT and IT models. Note that the "Overall" scores are computed over all test model pairs, not averaged across families. a direct statistical test. Given any pair of models, our approach outputs a p-value that enables a definitive decision on whether they share the same lineage, without relying on tunable thresholds, ensuring reliable verification in practice*

按部署变换类型细分（**Table 7**），SeedPrints 在指令微调、微调、PEFT 和量化场景下均保持较高 AUC（>0.99），但在模型合并（Merge）上 AUC 下降至 0.959：17 个合并模型中出现 1 例误判。这表明权值空间插值可能导致部分初始化偏差信号被稀释，是当前方法最主要的鲁棒性短板。

### 消融实验与超参数选择

SeedPrints 依赖三个关键超参数：随机输入序列数量 $n$、每条序列长度 $l$、身份维度数量 $m$。在显著性水平 $\alpha=0.01$ 下的消融实验（**Table 8**）表明：

- 增大 $n$ 和 $l$ 一致提升检测准确率：$n=200$ 时准确率 0.7368，$n=2000$ 时升至 0.9375；$l=1024$ 时达到完美准确率 1.0000。
- 身份维度数 $m$ 的影响呈非单调性：$m=400$ 达到最优准确率，进一步增大至 $m=800$ 时准确率下降至 0.8750，且经验假阳性率（FPR）飙升至 0.1463。过多的维度引入了噪声，削弱了统计检验的有效样本量。

对维度选择的进一步理论分析（附录 C.1，Lemma C.1）表明，基于样本均值的聚合策略比逐样本投票具有明显优势：在加性高斯噪声下，错误恢复真实 bottom‑m 集合的概率随查询数 $n$ 指数衰减，与消融实验中 $n$ 增大带来性能提升的趋势一致。

### 统计检验框架的有效性

SeedPrints 的谱系判决依赖于在身份维度上平均 Kendall‑τ 统计量偏离零假设的显著性。**Figure 4** 展示了分析性高斯零分布（$\bar{\tau} \sim \mathcal{N}(0, \sigma^2/|S|)$）与通过高斯替代输出运行完整流水线获得的经验分布高度吻合。该吻合验证了零假设下独立性假设近似成立，从而保证 $z$ 统计量与 $p$ 值计算的准确性，且无需为每一对模型单独构建经验零分布，大幅降低了计算开销。

### 失败模式与局限性

尽管 SeedPrints 在多数场景下表现稳健，仍存在若干明确局限：

1. **白盒依赖**：指纹提取需要获取模型的内部表示（logits 或隐藏状态），无法直接应用于仅提供文本生成服务的黑盒 API。
2. **模型合并脆弱性**：权值空间插值可能减弱初始化偏差信号，导致偶发误判（Merge 场景下 1/17 误分类），需探索更鲁棒的身份维度选择或加权方案。
3. **p 值转换失真**：将 p 值转化为 $1-p$ 得分以计算 AUC 的做法可能低估极端显著性之间的差异，统计特性和传统相似度度量之间的不一致可能混淆与基线的公平比较。
4. **架构与输出维度限制**：现实验证集中在 LLaMA 式与 Qwen 式架构；方法要求两个待比较模型具有相同的输出维度 $d_{\text{out}}$，难以直接用于跨尺寸或跨架构的谱系查询。
5. **对抗鲁棒性未评估**：攻击者可刻意过滤某些随机输入或添加扰动以掩盖偏差，防御场景下的安全性尚待验证。

![[assets/figures/papers/iclr26_0013_Kan6Z0zzZi_SeedPrints_Fingerprints_Can_Even_Tell_Which_Seed/figures/005_Table_1.jpg]]
*Table 1: Comparison of finger- Table 2: Trained models share the same fingerprint behaviors as print behaviors between models their initialization (p-value \< 0.01). initialized with different seeds*

## 定位与知识库关联

### 与现有模型指纹方法的谱系关系
当前主流的大语言模型指纹方法——包括Intrinsic（基于注意力参数层内标准差轮廓相似度）、REEF（基于表征的中心核对齐相似度）、PCS（基于参数展平后的余弦相似度）、ICS（基于参数不变量的余弦相似度）以及Gradient（基于梯度信息的指纹）——均依赖训练**后**涌现的属性构建签名，本质上属于“后天”指纹。这类方法的共有瓶颈在于：当模型尚处预训练早期（训练 token 量 < 1T）时，其训练后特征尚未充分形成，导致指纹检测全面失效；此外，这些方法在训练数据分布发生剧烈变化时容易被误导，无法满足“与生俱来、终身不变”的 Galton 式指纹要求。

SeedPrints 通过**信号来源的根本性切换**打破了上述瓶颈。它将指纹从训练后才固化的宏观参数分布或表征相似度，**下移至由初始化种子直接诱发的输出维度偏差模式**——即模型在纯随机输入下倾向于让哪些输出维度取得极小值的偏好。该偏差在训练全程持续存在且具有种子特异性（Figure 1；Table 2），从而使 SeedPrints 能够在首个预训练检查点即完美检测模型谱系（p ≪ 0.001），而所有基线方法在同期相似度均低于常规阈值 0.8（Figure 1）。在训练后阶段，同种子初始模型与最终训练模型之间在交集选定的“身份维度”上仍保持高度显著的 Kendall‑Tau 秩相关（p 达 $10^{-26}$ 量级），五种基线方法却无一成功区分（Table 2）。即使训练数据从 OpenWebText 突然切换到代码数据集 The Stack，SeedPrints 依然能正确归属谱系（p ≈ 0），而基线如 Intrinsic 则完全失效（误判相似度 0.489；Table 4）。这一根本机制差异使 SeedPrints 具有“初始化即形成、训练不磨灭”的特性，使其在功能谱系上区别于所有现有被动指纹方法。

在实际部署层面的综合基准 LeaFBench 上（65 个模型，涵盖 6 种参数改动技术），SeedPrints 的整体 AUC 达 0.992，显著优于 REEF（+0.077 AUC）和 Gradient（+0.191 AUC），虽略低于 Intrinsic（0.997）和 ICS（0.995），但其核心价值在于对早期预训练与分布偏移场景的鲁棒性，而非在标准副本检测上的微小差距（Table 6；Table 7）。

### 适用边界
SeedPrints 的最佳适用场景为**白盒或可获取内部表示**（logits 或隐藏状态）的模型身份验证，尤其擅长覆盖从预训练早期到大规模微调全生命周期的谱系追踪。其统计检验框架可直接输出显著性决策（p < 0.01 即判定同谱系），无需依赖外部阈值，决策规则统一。

现实部署中存在若干适用限制：
- **访问模式限制**：该方法必须获取模型内部输出，无法直接用于仅提供文本生成的黑盒 API 场景。
- **结构匹配要求**：待比较的两个模型需具有相同的输出维度（即 $d_{\mathrm{out}}$ 相同），因此无法直接应用于跨尺寸（如 7B ↔ 13B）或结构差异显著的模型族之间的谱系判断。
- **模型合并带来的信号衰减**：当存在权值空间插值（模型合并）时，初始化指纹信号可能被稀释，导致个别误判发生（17 个合并模型中误判 1 例，AUC 降至 0.959；Table 7）。
- **架构泛化未充分验证**：当前实验数据主要基于 LLaMA 式和 Qwen 式系列模型，SeedPrints 在非 Transformer、混合专家（MoE）或其他异质架构上的性能仍缺乏系统评估。
- **统计量转换的局限**：为与基于相似度的基线方法进行 AUC 比较，人为将 p 值转换为 $s = 1-p$ 得分，这种转换并非 p 值的合理连续相似度度量，可能低估极小 p 值之间的区分度（Section 5.3）。

### 已知局限
除上述适用边界中提到的限制外，方法还存在以下已知薄弱环节：
- **对抗防御的脆弱性**：指纹提取依赖的随机输入（纯随机 token 序列或高斯噪声）可被防御者刻意检测并过滤；攻击者也可通过修改初始化指纹信号来规避检测，目前方法缺乏对抗鲁棒性设计（Section Limitations）。
- **指纹尺寸与样本超参数敏感性**：指纹尺寸 $m$ 对性能的影响非单调，实验表明 $m=400$ 最优，而 $m=800$ 时准确率下降且引入假阳性（FPR=0.1463；Table 8），实际部署中需针对模型规模与架构仔细调参。
- **种子指纹的法律地位未明**：初始化种子作为单纯的技术要素，其是否能构成法律意义上的“数字指纹”并具备版权追溯效力，仍需跨学科探讨。

### 开放问题与研究展望
1. **黑盒扩展**：如何在仅能获取文本生成的条件下，利用外部行为观测间接提取初始化指纹信号，避免性能严重退化（当前黑盒方法尚存在巨大性能差距）。
2. **融合鲁棒性增强**：能否设计解耦策略或辅助信号，使 SeedPrints 在模型合并、权值混叠等场景下仍保持稳定的假阳性控制，减少偶发误判。
3. **跨架构与跨尺度泛化**：探索初始化指纹与模型架构组件（归一化层、激活函数、注意力头数等）的耦合关系，开发结构对齐或投影技术，使指纹验证可跨不同架构和不同尺度的模型。
4. **全生命周期统一指纹**：将初始化指纹与训练中后期涌现的指纹有机结合，形成“出生－成长－部署”全阶段可追溯的模型谱系框架，在早期预训练阶段即建立起不可伪造的身份印记。
5. **自动化阈值与统计决策**：在大型模型家族中，研究如何基于模型族内分布自适应设定显著性水平，以自动平衡假阳性与漏检率。
6. **安全与法律双重背书**：从技术层面增强指纹的防篡改能力，同时明确初始化指纹在模型审计、版权保护和责任认定中的法律定位，推动技术标准与法律规范的协同演进。

## 原文 PDF

![[paperPDFs/ICLR_2026/SeedPrints_Fingerprints_Can_Even_Tell_Which_Seed_Your_Large_Language_Model_Was_Trained_From.pdf]]
