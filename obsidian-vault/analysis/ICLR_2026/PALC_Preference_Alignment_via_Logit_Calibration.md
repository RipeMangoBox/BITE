---
title: "PALC: Preference Alignment via Logit Calibration"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/PALC_Preference_Alignment_via_Logit_Calibration.pdf
project_link: null
code_link: https://github.com/s4n9hyun/PALC
openreview_forum_id: 0cmuYj3WeG
aliases:
- PALC
tags:
- ICLR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: "在词汇空间（logit space）中施加学习到的校准向量，通过瓶颈架构和固定缩放因子实现参数高效、运行时可调的偏好控制。"
primary_logic: "将干预点从纠缠的隐藏空间转移到天然解纠缠的词汇空间，利用瓶颈压缩提取低维偏好信号，避免了隐藏状态操纵的副作用，同时以极少的额外参数实现了灵活的测试时对齐。"
claims:
- "隐藏空间中多个语义概念以叠加形式存在，直接操纵会引起级联副作用。"
- "词汇空间的每个维度唯一对应一个token，是自然解纠缠的接口。"
- "瓶颈架构（B=256）能够压缩偏好信号，实现极端参数效率（0.13% 额外参数）和近基线推理速度。"
- "单个缩放因子γ可在推理时连续调节对齐强度，无需重训。"
---

# PALC: Preference Alignment via Logit Calibration

> [!tip] 核心洞察
> 将干预点从纠缠的隐藏空间转移到天然解纠缠的词汇空间，利用瓶颈压缩提取低维偏好信号，避免了隐藏状态操纵的副作用，同时以极少的额外参数实现了灵活的测试时对齐。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | PALC：基于Logit校准的偏好对齐 |
| 英文题名 | PALC: Preference Alignment via Logit Calibration |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=0cmuYj3WeG) · [GitHub](https://github.com/s4n9hyun/PALC) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | PALC |
| Dataset | HH-RLHF |

> [!tip] 效果简介
> - HH-RLHF 上，Win+1/2 Tie (%) vs. Base Model 为 58.17%，对比 Base Model，变化 +8.17%。
> - HH-RLHF 上，Win+1/2 Tie (%) vs. DPO 为 41.17%，对比 DPO，变化 -8.83%。
> - HH-RLHF 上，Win+1/2 Tie (%) vs. CAA 为 77.17%，对比 CAA，变化 +27.17%。

## 概要

当前大语言模型的对齐方法主要分为两类：训练时对齐（如基于人类反馈的强化学习）和测试时对齐（如表征工程与引导解码）。测试时对齐因其无需重训、可即插即用的灵活性而备受关注，但现有方法面临两个核心瓶颈：**隐藏状态中的特征叠加**使得直接操纵隐藏空间会引发非预期的级联副作用；**外部奖励模型**的高计算开销则阻碍了高效部署。

PALC 提出了一种范式转换——将干预点从纠缠的隐藏空间转移到**天然解纠缠的词汇空间（logit space）**。其核心思路是：冻结基础语言模型，仅将其最终隐藏状态作为只读上下文，通过一个轻量级瓶颈架构（B=256）压缩偏好信号，生成位置敏感的校准向量，再以固定缩放因子注入原始 logits。这一设计带来了三个关键优势：

1. **极端参数效率**：仅需 9.2M 额外参数（占 7B 模型的 0.13%），无需通过基础模型反向传播。
2. **近基线推理速度**：仅引入 8% 的推理延迟（1.08×），远优于依赖 7B 奖励模型的 GenARM（5.96×）和需在线优化的 RE-Control（76.7×）。
3. **运行时可调可控**：单个缩放因子 γ 即可连续调节对齐强度，无需重训；负向缩放甚至可将模型推向反对齐方向。

实验表明，PALC 在 HH-RLHF 有益/无害偏好基准上对基础模型的综合胜率达到 58.17%（+8.17%），显著优于表征工程方法 CAA（77.17% 胜率）和 RE-Control（61.67% 胜率），与训练时对齐方法 DPO 的差距仅为 -8.83%。在外部基准 MT-Bench 上，PALC 的长度控制胜率（61.9%）超越了计算开销更高的 GenARM（58.7%）。消融实验进一步揭示：瓶颈维度 B=256 为最优，扩展至 B=4096 会导致胜率崩溃至 18.3%——谱分析验证了此时奇异值衰减指数 α=0.73<1，违反了稀疏学习的理论条件，从而解释了超宽瓶颈的性能退化机制。



大型语言模型（LLM）的对齐是确保其输出符合人类偏好的核心挑战。现有对齐范式大致分为两类：训练时对齐（如基于人类反馈的强化学习 RLHF 和直接偏好优化 DPO）通过微调模型参数来内化偏好，但计算成本高昂且对齐目标固化于模型权重中，无法在推理时灵活调整。测试时对齐方法试图解决这一灵活性缺口，通过在推理阶段干预模型行为来实现可控生成，但其有效性受制于两个根本性瓶颈。

**隐藏空间的特征叠加困境。** 当前主流的测试时对齐方法——包括表征工程（如 CAA、BiPO、RE-Control）和基于奖励模型的引导解码（如 ARGS、GenARM）——大多在隐藏状态空间中施加干预。然而，隐藏表示以叠加（superposition）形式存在：多个语义概念共享重叠的方向，直接操纵这一空间会引发非预期的级联副作用，损害生成质量。这一困境源于隐藏空间的内在纠缠特性，使得精准、可控的偏好注入极为困难。

**外部奖励模型的高计算开销。** 基于奖励模型的引导解码方法需要在每个生成步骤调用额外的奖励模型来评估候选token，引入数倍于基础模型的推理延迟（例如 GenARM 的延迟高达 5.08 倍）。这种计算负担严重限制了测试时对齐方法在实际部署中的可行性，尤其在需要低延迟响应的场景中。

**核心动机：寻找解纠缠的干预接口。** 上述瓶颈指向一个关键问题：是否存在一个天然解纠缠的空间，使得偏好干预既能避免隐藏空间操纵的副作用，又能以极低的计算开销实现灵活可控的对齐？PALC 的回答是将干预点从纠缠的隐藏空间转移到词汇空间（logit space）。词汇空间的每个维度唯一对应一个token，提供了天然解纠缠的接口——修改第 $i$ 个logit对第 $j$ 个token概率的影响由梯度关系 $\frac{\partial p_i}{\partial l_j} = p_i (\delta_{ij} - p_j)$ 精确刻画，使得干预效果可控且可解释。基于这一洞察，PALC 通过一个轻量级瓶颈架构从冻结的隐藏状态中提取低维偏好信号，在词汇空间生成校准向量，以仅 0.13% 的额外参数和近乎无开销的推理延迟，实现了运行时可调的偏好对齐。



## 核心方法与创新机理

PALC 的核心创新在于将偏好对齐的干预点从**纠缠的隐藏空间**迁移到**天然解纠缠的词汇空间**，并通过瓶颈架构实现参数高效、运行时可调的测试时对齐。

### 干预点的根本转变

现有测试时对齐方法（如 CAA、RE-Control、BiPO）普遍在隐藏状态空间中施加转向向量，但隐藏状态存在**特征叠加（superposition）**问题——多个语义概念共享重叠的方向，直接操纵会引发非预期的级联副作用。PALC 将干预点转移至词汇空间（logit space），其关键优势在于：词汇空间的每个维度唯一对应一个 token，是天然解纠缠的接口。修改第 $i$ 个 logit 对第 $j$ 个 token 概率的影响可通过梯度解析表达：

$$\frac{\partial p_i}{\partial l_j} = p_i (\delta_{ij} - p_j)$$

这意味着在词汇空间中的干预具有可控性和可解释性，避免了隐藏状态操纵的语义污染。

### 自包含的瓶颈校准模块

PALC 不依赖外部奖励模型（如 ARGS、GenARM）或静态转向向量（如 CAA），而是引入一个轻量级的**校准模块（Calibration Module）**，通过瓶颈架构从冻结基础模型的最终隐藏状态中提取偏好信号：

$$\mathbf{z}_t = \operatorname{ReLU}(W_{\mathrm{down}} \mathbf{h}_t), \quad \mathbf{m}_t = W_{\mathrm{up}} \mathbf{z}_t$$

其中 $W_{\mathrm{down}} \in \mathbb{R}^{B \times H}$ 将隐藏状态压缩至瓶颈维度 $B$，$W_{\mathrm{up}} \in \mathbb{R}^{V \times B}$ 将压缩后的信号投影回词汇空间，生成位置敏感的校准向量 $\mathbf{m}_t$。校准后的 logits 为：

$$\mathbf{l}_t' = \mathbf{l}_t + \gamma \cdot \mathbf{m}_t$$

训练采用无参考模型、无 KL 散度的简化偏好损失，直接最大化偏好响应与拒绝响应的概率差：

$$\mathcal{L} = -\mathbb{E}_{(x, y_w, y_l) \sim \mathcal{D}} \left[ \log \sigma \left( \log \pi_{\mathrm{PALC}}(y_w | x) - \log \pi_{\mathrm{PALC}}(y_l | x) \right) \right]$$

### 参数效率与运行时可控性

与各基线方法相比，PALC 在三个关键维度上实现了突破：

| 维度 | 基线方法 | PALC |
|------|---------|------|
| **干预点** | 隐藏状态（CAA、RE-Control、BiPO）或概率空间（ARGS） | 词汇空间（logit space） |
| **对齐机制** | 外部奖励模型（ARGS、GenARM）或固定/在线转向向量 | 自包含的位置敏感校准向量 + 瓶颈架构 |
| **参数开销** | LoRA 微调数十至数百M，或需加载 7B 奖励模型 | 仅 9.2M（0.13% of 7B） |

瓶颈维度 $B=256$ 时，PALC 仅增加 9.2M 可训练参数，推理延迟仅为基线的 1.08 倍，远低于需要加载额外 7B 奖励模型的 GenARM（5.68 倍延迟）。同时，单个缩放因子 $\gamma$ 可在推理时连续调节对齐强度，无需重新训练——$\gamma=1.0$ 时性能最优（58.2% 胜率），负值（$\gamma=-5.0$）则将模型推向反对齐方向，验证了校准向量的可逆控制能力。

### 瓶颈稀疏性的理论支撑

谱分析揭示了瓶颈架构的必要性：校准矩阵 $M = W_{\mathrm{up}} W_{\mathrm{down}}$ 的奇异值呈幂律衰减 $\sigma_i \sim i^{-\alpha}$。最优配置 $B=256$ 满足稀疏学习条件 $\alpha = 1.02 \pm 0.01 > 1$，而失败配置 $B=4096$ 违反此条件（$\alpha = 0.73 \pm 0.01$），导致胜率崩溃至 18.3%、响应质量降至 2.15/10.0。这表明瓶颈不仅是参数效率的手段，更是**架构层面的必要正则化器**，强制偏好信号集中在低维流形上。



![[assets/figures/papers/iclr26_0011_0cmuYj3WeG_PALC_Preference_Alignment_via_Logit_Calibration/figures/001_Figure_1.jpg]]
*Figure 1: Overview of the PALC framework. Unlike conventional representation steering methods that intervene in entangled hidden spaces, PALC treats the base model’s hidden states ht strictly as a read-only context. A lightweight Calibration Module (θ) extracts essential preference signals through a bottleneck architecture ( $\bar { W } _ { \mathrm { d o w n } } , W _ { \mathrm { u p } }$ ) to generate calibration vectors mt in the disentangled logit space. This decoupling ensures precise preference alignment with minimal computational overhead and preserves the base model’s general capabilities

PALC 的设计动机源于现有测试时对齐方法的两大瓶颈：**隐藏状态中的特征叠加（superposition）** 使得直接操纵隐藏空间会引发非预期的级联副作用；而依赖外部奖励模型的引导解码方法则面临高昂的计算开销。PALC 的核心洞察是将干预点从纠缠的隐藏空间转移到天然解纠缠的词汇空间（logit space），因为词汇空间的每个维度唯一对应一个 token，构成了天然的解纠缠接口。

整个 pipeline 由四个模块串联构成：

1. **冻结基础 LLM**：提供最终隐藏状态 $\mathbf{h}_t$ 和原始 logits $\mathbf{l}_t$，不参与梯度更新。
2. **校准模块（Calibration Module $\theta$）**：以瓶颈架构将 $\mathbf{h}_t$ 压缩至低维空间后投影回词汇空间，生成校准向量 $\mathbf{m}_t$：
   $$\mathbf{z}_t = \operatorname{ReLU}(W_{\mathrm{down}} \mathbf{h}_t), \quad \mathbf{m}_t = W_{\mathrm{up}} \mathbf{z}_t$$
3. **对数尺度缩放**：将校准向量乘以固定缩放因子 $\gamma$ 后注入原始 logits：
   $$\mathbf{l}_t' = \mathbf{l}_t + \gamma \cdot \mathbf{m}_t$$
4. **Softmax 与解码**：从校准后的 logits 生成下一个 token。

瓶颈维度 $B=256$ 是关键设计选择——仅引入 9.2M 额外参数（占 7B 模型的 0.13%），推理延迟仅为基线的 1.08 倍。单个缩放因子 $\gamma$ 可在推理时连续调节对齐强度，无需重新训练：$\gamma=1.0$ 时性能最优，$\gamma$ 取负值则可将模型推向反对齐方向。



### 3.1 词汇空间干预：从纠缠到解纠缠

PALC的核心设计动机源于对现有测试时对齐方法瓶颈的重新审视。隐藏状态中多个语义概念以叠加形式共存（superposition），直接操纵隐藏空间会引发不可控的级联副作用[Section 1]。PALC将干预点从纠缠的隐藏空间转移至天然解纠缠的词汇空间——每个维度唯一对应一个token，为偏好信号注入提供了可解释且可控的接口[Section 3.1]。

### 3.2 校准模块：瓶颈架构与Logit注入

PALC的校准模块（Calibration Module θ）遵循两条设计原则：一是以冻结基础LLM的最终隐藏状态 $\mathbf{h}_t$ 作为只读上下文，不在隐藏空间中施加任何修改；二是采用瓶颈架构（$B \ll H$）将偏好信号压缩至低维子空间，再投影至词汇空间生成校准向量[Section 3.1]。

具体计算流程如下：

**校准向量生成**（Equation 1）：

$$\mathbf{z}_t = \operatorname{ReLU}(W_{\mathrm{down}} \mathbf{h}_t), \quad \mathbf{m}_t = W_{\mathrm{up}} \mathbf{z}_t$$

其中，$W_{\mathrm{down}} \in \mathbb{R}^{B \times H}$ 将隐藏状态 $\mathbf{h}_t \in \mathbb{R}^H$ 压缩至瓶颈维度 $B$，$\operatorname{ReLU}$ 引入非线性，$W_{\mathrm{up}} \in \mathbb{R}^{V \times B}$ 将压缩表示投影至词汇空间（$V$ 为词表大小），生成校准向量 $\mathbf{m}_t \in \mathbb{R}^V$。该瓶颈架构仅引入 $B \times (H + V)$ 个可训练参数，在 $B=256$ 时仅占7B基础模型的0.13%（约9.2M参数）[Section 3.2, Section B.1]。

**校准后Logits**（Equation 2）：

$$\mathbf{l}_t' = \mathbf{l}_t + \gamma \cdot \mathbf{m}_t$$

原始logits $\mathbf{l}_t$ 加上缩放因子 $\gamma$ 调控的校准向量，得到校准后的logits $\mathbf{l}_t'$。$\gamma$ 作为单一标量控制对齐强度：$\gamma > 0$ 增强偏好对齐，$\gamma < 0$ 将模型推向反对齐方向，$\gamma = 0$ 等价于基础模型。这一设计使得推理时无需重训即可连续调节对齐行为[Abstract, Section 3.2]。

### 3.3 训练目标：无参考模型的简化偏好损失

PALC采用简化的偏好损失函数，无需参考模型约束和KL散度项，直接最大化偏好响应与拒绝响应的概率差（Equation 3）：

$$\mathcal{L} = -\mathbb{E}_{(x, y_w, y_l) \sim \mathcal{D}} \left[ \log \sigma \left( \log \pi_{\mathrm{PALC}}(y_w | x) - \log \pi_{\mathrm{PALC}}(y_l | x) \right) \right]$$

其中 $\sigma$ 为sigmoid函数，$\pi_{\mathrm{PALC}}$ 为校准后的策略分布。训练仅更新校准模块参数 $\theta = \{W_{\mathrm{down}}, W_{\mathrm{up}}\}$，基础LLM保持冻结，无需反向传播通过整个模型[Section 3.3, Section 4.1]。

### 3.4 Logit梯度的可解释性

词汇空间干预的关键优势在于其梯度行为的可控性。修改第 $i$ 个logit对第 $j$ 个token概率的影响由softmax导数精确刻画（Equation 4）：

$$\frac{\partial p_i}{\partial l_j} = p_i (\delta_{ij} - p_j)$$

其中 $\delta_{ij}$ 为Kronecker delta。该公式表明：提升某token的logit会压制所有其他token的概率（$j \neq i$ 时梯度为负），且压制的幅度与该token的当前概率 $p_j$ 成正比。这一性质确保了词汇空间中的干预行为是局部且可预测的，避免了隐藏空间操纵中常见的全局扰动[Section A.1.2]。

### 3.5 瓶颈稀疏性的理论条件

PALC的瓶颈架构并非简单的参数压缩，而是满足稀疏学习理论条件的必要正则化手段。对校准矩阵 $M = W_{\mathrm{up}} W_{\mathrm{down}}$ 进行奇异值分解，其奇异值呈幂律衰减（Equation 5）：

$$\sigma_i \sim i^{-\alpha}$$

理论分析表明，$\alpha > 1$ 是稀疏稳定学习的必要条件[Section H, Theorem 1]。实验验证：最优瓶颈配置 $B=256$ 满足 $\alpha = 1.02 \pm 0.01$，而失败配置 $B=4096$ 违反该条件（$\alpha = 0.73 \pm 0.01$），导致性能崩溃至18.3%获胜率[Figure 6, Section H.1]。有效维度（参与率）进一步量化了瓶颈空间的实际利用程度：

$$d_{\mathrm{eff}} = \frac{(\sum_{i=1}^B \sigma_i)^2}{\sum_{i=1}^B \sigma_i^2}$$

该指标验证了偏好信号确实集中在极低维流形上，为瓶颈架构提供了谱分析层面的理论支撑[Section A.1.1]。



## 实验与关键发现

### 主要结果：HH-RLHF 上的成对比较

PALC 在 HH-RLHF 数据集上与七种基线方法进行成对比较（Table 1），以 Win+½ Tie 作为综合胜率指标。结果表明，PALC 在测试时对齐方法中展现出显著的竞争力，同时保持极低的参数和计算开销。


![[assets/figures/papers/iclr26_0011_0cmuYj3WeG_PALC_Preference_Alignment_via_Logit_Calibration/figures/002_Table_1.jpg]]
*Table 1: Pairwise comparison results showing PALC’s performance against baseline methods on HH-RLHF*

**相对于基础模型**，PALC 取得 **58.17%** 的综合胜率，较随机基线（50%）提升 8.17 个百分点，验证了词汇空间校准向量能够有效引导模型朝向偏好方向生成。

**与训练时对齐方法 DPO 的对比**中，PALC 的胜率为 41.17%，低于 DPO 约 8.83 个百分点。这一差距是预期的：DPO 通过 LoRA 微调直接优化模型参数，而 PALC 仅以 0.13% 的额外参数在推理时施加轻量级干预。考虑到 PALC 无需反向传播通过基础模型、无需参考模型约束，这一性能折衷在参数效率与部署灵活性上具有显著优势。

**与表征工程方法的对比**揭示了词汇空间干预的核心优势：
- **vs. CAA**（静态转向向量）：PALC 胜率高达 **77.17%**，优势达 27.17 个百分点。CAA 在纠缠的隐藏空间中施加固定方向的干预，无法根据上下文动态调整，导致对齐效果不稳定。PALC 通过位置敏感的瓶颈架构生成依赖上下文的校准向量，从根本上避免了这一缺陷。
- **vs. RE-Control**（在线优化隐藏状态）：PALC 胜率为 **61.67%**，领先 11.67 个百分点。RE-Control 虽能动态优化隐藏状态，但每次生成需运行 100 轮 SGD 优化，计算开销极大（Table 2 显示其推理时间为 PALC 的 5 倍以上），且优化过程本身可能引入不稳定性。
- **vs. BiPO**（双向偏好优化）：PALC 胜率为 49.00%，基本持平（差距 -1.00%），表明两种方法在该任务上性能接近。


![[assets/figures/papers/iclr26_0011_0cmuYj3WeG_PALC_Preference_Alignment_via_Logit_Calibration/figures/003_Table_2.jpg]]
*Table 2: Computational efficiency of test-time alignment methods. Inference time measured for generating 128 tokens on a single NVIDIA H100 GPU, averaged over 10 runs*

**与基于奖励模型的引导解码方法对比**：
- **vs. ARGS**（外部奖励模型引导）：PALC 胜率 **55.50%**，领先 5.50 个百分点。ARGS 依赖独立的 7B 奖励模型，推理时需额外维护一个完整的前向传播，计算开销远高于 PALC。
- **vs. GenARM**（自回归奖励模型引导）：PALC 胜率 44.33%，落后 5.67 个百分点。GenARM 同样使用 7B 规模的奖励模型，虽然对齐效果略优，但其推理时间约为 PALC 的 5 倍（Table 2），在实际部署中面临严重的效率瓶颈。

### 计算效率分析

Table 2 系统比较了各测试时对齐方法的推理效率。在单张 NVIDIA H100 GPU 上生成 128 个 token 的测试中：

- **基础模型**推理时间为 1.78 秒。
- **PALC** 仅需 **1.93 秒**，额外延迟为 **1.08×**，增加的 9.2M 参数仅占 7B 模型的 0.13%。
- 相比之下，**GenARM** 需 9.27 秒（5.21× 延迟），**ARGS** 需 9.50 秒（5.34×），两者均需维护额外的 7B 奖励模型。
- **RE-Control** 因每步在线优化，推理时间显著更长（原文未给出精确数值，但指出其优化循环开销远高于其他方法）。

这一效率优势源于 PALC 的核心设计：瓶颈架构将 4096 维的隐藏状态压缩至 256 维，校准向量的生成仅涉及两个小型线性投影和一次 ReLU 激活，计算量几乎可忽略。

### 瓶颈维度消融：B=256 最优，B=4096 灾难性崩溃

Figure 2 展示了瓶颈维度 B 对 PALC 性能的影响，这是理解该方法工作机制的关键实验。


![[assets/figures/papers/iclr26_0011_0cmuYj3WeG_PALC_Preference_Alignment_via_Logit_Calibration/figures/005_Figure_2.jpg]]
*Figure 2: Effect of bottleneck dimension on PALC performance. Left: Win rate against the base model shows optimal performance at B = 256 (58.2%) with catastrophic failure at B = 4096 (18.3%). The gray dashed line indicates baseline performance (50%). Right: GPT-5 response quality scores remain stable from B = 1 6 to B = 1 0 2 4 but collapse at B = 4 0 9 6 (2.15/10.0)*

**胜率变化**（Figure 2 左）：当 B 从 16 逐步增加到 256 时，胜率从约 55% 单调上升至 **58.2%** 的峰值。B 继续增大到 1024 时，胜率仍维持在 56% 以上。然而，当 B 跃升至 **4096**（即瓶颈宽度等于隐藏状态维度，瓶颈退化为恒等映射）时，胜率**骤降至 18.3%**，远低于随机基线 50%。这一灾难性失败表明，瓶颈并非仅仅是参数效率的工程选择，而是方法正常工作的**必要条件**。

**响应质量变化**（Figure 2 右）：GPT-5 评判的响应质量分数在 B=16 至 B=1024 范围内稳定在 3.84–3.96/10.0 之间，但在 B=4096 时崩溃至 **2.15/10.0**，进一步确认了超宽瓶颈导致的生成质量退化。

**失败机制的理论解释**：附录 H 的谱分析（Figure 6）揭示了这一现象的根本原因。校准矩阵 $M = W_{\text{up}} W_{\text{down}}$ 的奇异值呈幂律衰减 $\sigma_i \sim i^{-\alpha}$。当 B=256 时，幂律指数 $\alpha = 1.02 \pm 0.01$，满足稀疏学习的理论条件（$\alpha > 1$），表明偏好信号集中在极低维流形上。而当 B=4096 时，$\alpha = 0.73 \pm 0.01$，违反 $\alpha > 1$ 条件，意味着学习到的结构缺乏稀疏性，噪声维度淹没有效信号，导致校准向量在词汇空间中产生无差别的干扰，破坏了原始语言建模能力。


![[assets/figures/papers/iclr26_0011_0cmuYj3WeG_PALC_Preference_Alignment_via_Logit_Calibration/figures/013_Figure_6.jpg]]
*Figure 6: (b) Failure Case ( B ~ = ~ 4 0 9 6 ) The exponent is ${ \alpha = \mathbf { 0 . 7 3 } \pm \mathbf { 0 . 0 1 } }$ (full range), violating the theoretical condition $\alpha$ > ${ \bf$ 1 } . This slow, gradual decay signifies that the learned structure lacks sparsity and explains the observed performance collapse (Section 4.4.1). Figure 6: Power-Law Exponent Analysis of Learned Matrices. The log-log scale plots confirm the necessity of the bottleneck constraint. The optimal model $\mathbf { ( B = 2 5 6 ) }$ satisfies $\alpha$ > ${ \bf$ 1 } , validating the condition for sparse, stable learning (Theorem 1), while the failure case $\mathbf { ( B = 4 0 9 6 ) }$ violates it

### 缩放因子 $\gamma$ 消融：可调的运行时控制旋钮

Figure 3 展示了缩放因子 $\gamma$ 对 PALC 性能的影响。$\gamma = 1.0$ 时胜率达到峰值 58.2%，响应质量分数为 3.96/10.0。$\gamma$ 增大到 3.0 时性能基本持平，但 $\gamma = 5.0$ 时响应质量开始下降至 3.79，$\gamma = 10.0$ 时进一步恶化至 **3.07/10.0**。这表明过大的校准强度会过度扭曲原始概率分布，损害生成质量。


![[assets/figures/papers/iclr26_0011_0cmuYj3WeG_PALC_Preference_Alignment_via_Logit_Calibration/figures/007_Figure_3.jpg]]
*Figure 3: Effect of scaling factor $\gamma$ on PALC performance. Left: Win rate peaks at $\gamma$ = 1 . 0 (58.2%) with gradual decline at extreme values. Right: Response quality shows similar pattern with degradation at $\gamma$ = 1 0 . 0

**负缩放因子的逆向对齐**（Figure 5）进一步验证了 $\gamma$ 作为可控旋钮的有效性。当 $\gamma = -5.0$ 时，校准向量以相反方向施加，将模型推向**反对齐方向**。在 HH-RLHF 上的头对头比较中，$\gamma = 5.0$ 对 $\gamma = -5.0$ 取得显著优势（原文报告胜率约 61.4%），证明单个标量参数即可在推理时**连续调节对齐强度**，甚至实现对齐方向的翻转，无需任何重新训练。

### MT-Bench 外部基准验证

Figure 4 展示了 PALC 在 MT-Bench 上的泛化性能。在长度控制（LC）Win+Tie 指标下——该指标校正了冗长偏差，确保评分反映内容质量而非生成长度——PALC 取得 **61.9%** 的 LC Win+Tie 率，超越计算密集型的 GenARM（58.7%），进一步验证了词汇空间校准方法的跨任务泛化能力和效率优势。

### 需要人工验证的局限性说明

以下结论基于论文提供的有限实验证据，建议在复现时进行独立验证：

1. **评估偏差风险**：所有主要结果均依赖 GPT-5 作为评判器，可能引入提示模板偏好和模型自身偏好偏差。论文未报告与人工评估的一致性验证。
2. **单一偏好维度**：实验仅针对有益/无害这一对偏好，未测试在其他对齐维度（如事实性、安全性、简洁性）上的表现。
3. **规模泛化未验证**：所有实验基于 7B 模型，PALC 的瓶颈稀疏性假设在大规模模型（如 70B）上是否依然成立尚待验证。
4. **$\gamma$ 的最优值依赖任务**：$\gamma = 1.0$ 的最优性是在 HH-RLHF 上确定的，不同任务可能需要不同的缩放强度，当前缺乏自适应调节机制。



## 定位与知识库关联

### 与现有方法的本质差异

PALC在测试时对齐方法谱系中的核心定位在于**干预点的转移**——从纠缠的隐藏空间转向天然解纠缠的词汇空间。这一设计选择直接回应了现有方法的根本瓶颈：隐藏状态中多个语义概念以叠加（superposition）形式共存，直接操纵会引起级联副作用。词汇空间的每个维度唯一对应一个token，构成了一个可解释且可控的干预接口。

与表征工程方法（CAA、BiPO、RE-Control）相比，PALC不直接修改隐藏状态。CAA使用固定的转向向量，BiPO通过双向偏好优化学习表征干预，RE-Control则在推理时在线优化隐藏状态——这些方法均在隐藏空间操作，面临叠加效应的固有风险。PALC将隐藏状态仅作为只读上下文，通过瓶颈架构提取偏好信号后，在词汇空间生成校准向量，从根本上规避了隐藏空间操纵的副作用。

与基于奖励模型的引导解码方法（ARGS、GenARM）相比，PALC无需外部奖励模型。ARGS依赖独立训练的奖励模型进行引导，GenARM使用自回归奖励模型——两者均需维护额外的7B级模型，导致显著的计算开销（GenARM的推理延迟约为基线的5.8倍，见Table 2）。PALC仅需9.2M参数的校准模块（0.13% of 7B），推理延迟仅为基线的1.08倍，在参数效率和推理速度上形成数量级优势。

与训练时对齐方法（DPO）相比，PALC属于测试时对齐范式，无需微调基础模型权重。DPO通过LoRA微调修改模型参数，而PALC在冻结的基础模型之上附加轻量校准模块，支持推理时的动态调节。

### 适用边界与已知局限

**数据与任务边界**。PALC目前仅在HH-RLHF单一偏好数据集上验证，训练目标聚焦于有益/无害这一对偏好维度。在其他偏好维度（如事实性、安全性、简洁性）及不同领域上的泛化能力尚未经实验检验。MT-Bench的外部评估（Figure 4）提供了初步的多任务证据，但评估范围仍局限于通用对话质量。

**模型规模边界**。实验仅基于7B规模的LLaMA-SFT模型，未在大规模模型（如70B）及更复杂部署场景中验证。瓶颈稀疏性假设（幂律衰减指数α>1）在更大模型上是否依然成立，是一个需要手动验证的开放问题。

**架构敏感性与失败模式**。瓶颈维度B的选择对性能影响极为敏感：B=256时性能最优（58.2%胜率），但B=4096时发生灾难性失败（胜率崩溃至18.3%，响应质量降至2.15/10.0）。SVD分析揭示了这一现象的深层机制——B=256时奇异值呈幂律衰减（α=1.02±0.01，满足稀疏学习条件α>1），而B=4096时衰减过缓（α=0.73±0.01），违反了稀疏学习的理论条件。这表明瓶颈架构不仅是参数效率的设计选择，更是**必要的架构正则化器**，其失效会导致学习到的偏好结构失去稀疏性。然而，这一失败是否纯粹源于过拟合，还是存在更根本的架构失效机制，目前尚不明确。

**缩放因子的固定性**。缩放因子γ的最优值（1.0）可能随任务和上下文变化，但当前设计缺乏自适应机制。极端γ值会导致性能退化（γ=10.0时响应质量降至3.07/10.0），而负缩放因子（γ=-5.0）可将模型推向反对齐方向，表明校准向量可逆向削弱偏好行为。这一特性虽展示了灵活性，但也意味着γ的手动调节需要领域知识。

**评估偏差风险**。主要评估使用GPT-5作为评判器，可能引入提示模板和模型偏好偏差。评估仅覆盖HH-RLHF数据集，未在不同数据分布、多语言环境或对抗性提示下测试公平性。

### 开放问题

1. **多目标对齐的组合性**。能否通过组合多个可插拔的校准模块实现多目标偏好对齐（如同时控制安全性、有帮助性、简洁性）？词汇空间的解纠缠特性理论上支持独立校准向量的叠加，但不同偏好维度之间的交互效应需要进一步研究。

2. **自适应缩放机制**。能否设计动态缩放机制，使γ根据prompt或生成上下文自适应调整？当前固定γ的设计限制了PALC在复杂对话场景中的灵活性，上下文感知的缩放策略可能进一步提升对齐精度。

3. **大规模验证与稀疏性假设的普适性**。在大规模模型（如70B）和更丰富的偏好数据集（如Anthropic HH、Red-Teaming prompts）上，瓶颈稀疏性假设（α>1）是否依然成立？如果成立，最优瓶颈维度B是否随模型规模变化？

4. **词汇空间校准的泛化能力**。词汇空间校准方法能否泛化到其他对齐范式（如针对事实性的校准、减少幻觉）？其可解释性优势——每个logit修改对应一个明确token——如何被进一步利用于对齐审计和调试？



## 原文 PDF

![[paperPDFs/ICLR_2026/PALC_Preference_Alignment_via_Logit_Calibration.pdf]]
