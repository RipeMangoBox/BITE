---
title: "DIVA-GRPO: Enhancing Multimodal Reasoning through Difficulty-Adaptive Variant Advantage"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/DIVA_GRPO_Enhancing_Multimodal_Reasoning_through_Difficulty_Adaptive_Variant_Advantage.pdf
openreview_forum_id: qKXYEg00eH
aliases:
- DG
- DIVA-GRPO
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/vision_models_multimodal
core_operator: "通过动态评估问题难度并自适应生成变体（简单问题增强图像/文本扰动、中等难度提供多样化释义、困难问题引入分步推理提示），调整问题组内的奖励分布，使优势信号持续有效。"
primary_logic: "将难度评估与变体生成结合，设计难度加权的局部-全局优势计算框架：利用批归一化平衡局部与全局优势的尺度，再通过相对难度加权和奖励范围重标定，缓解奖励稀疏与优势消失，同时保持优化方向无偏并提升训练稳定性。"
claims:
- "DIVA-GRPO-7B在六个多模态推理基准上平均达到54.58分，远超同规模模型并逼近更大模型与商业系统。"
- "消融实验表明：自适应变体生成、难度加权、RRB重标定和全局-局部平衡每个组件均有贡献，全模型表现最佳。"
- "RRB-Rescaling可独立用于标准GRPO，平均提升约2个百分点，验证了其泛化性。"
- "DIVA-GRPO相较GRPO将训练所需步数减少至多2.55倍，端到端时间加速1.76倍。"
---

# DIVA-GRPO: Enhancing Multimodal Reasoning through Difficulty-Adaptive Variant Advantage

> [!tip] 核心洞察
> 将难度评估与变体生成结合，设计难度加权的局部-全局优势计算框架：利用批归一化平衡局部与全局优势的尺度，再通过相对难度加权和奖励范围重标定，缓解奖励稀疏与优势消失，同时保持优化方向无偏并提升训练稳定性。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | DIVA-GRPO：通过难度自适应变体优势增强多模态推理 |
| 英文题名 | DIVA-GRPO: Enhancing Multimodal Reasoning through Difficulty-Adaptive Variant Advantage |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=qKXYEg00eH); [GitHub](https://github.com/Siaaaaaa1/DIVA-GRPO) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal |
| Method | DIVA-GRPO |
| Dataset | MathVista, MathVerse, MathVision, OlympiadBench |

> [!tip] 效果简介
> - MathVista 上，Accuracy 为 74.2，对比 Qwen-2.5-VL-7B: 68.2，变化 +6.0。
> - MathVerse 上，Accuracy 为 57.6，对比 Qwen-2.5-VL-7B: 47.9，变化 +9.7。
> - MathVision 上，Accuracy 为 32.1，对比 Qwen-2.5-VL-7B: 25.4，变化 +6.7。

## 概述

多模态推理任务中，基于组相对策略优化（GRPO）的强化学习方法面临一个根本性瓶颈：问题难度分布不均导致组内奖励方差过小或过大，使得优势信号稀疏甚至消失，优化信号不稳定，训练效率低下。现有方案要么选择性利用部分数据，造成样本浪费；要么无差别地增强样本，反而加剧优势稀疏。

**DIVA-GRPO** 针对上述问题，提出了一种难度自适应的变体优势增强方法。其核心洞察是：将动态难度评估与自适应变体生成相结合，设计难度加权的局部-全局优势计算框架——利用批归一化平衡局部与全局优势的尺度，再通过相对难度加权和奖励范围重标定，缓解奖励稀疏与优势消失，同时保持优化方向无偏并提升训练稳定性。

具体而言，DIVA-GRPO 包含三个关键机制：

1. **动态难度评估**：根据历史 rollout 准确率实时更新每个问题的难度系数，使难度评估随模型能力提升而自适应调整。
2. **自适应变体生成**：依据难度等级，为简单问题添加图像/文本扰动以提升挑战性，为中等难度生成多样化释义变体，为困难问题引入分步推理提示以降低门槛，从而扩大有效奖励方差。
3. **难度加权的局部-全局优势计算**：同时在问题内部（局部）和问题跨变体组（全局）计算标准化优势，通过批归一化平衡两者尺度，再根据相对难度进行指数加权，并引入奖励范围重标定防止小差异被夸大。

在方法谱系上，DIVA-GRPO 以 **GRPO**（Shao et al., 2024）为基础框架，以 **Qwen-2.5-VL-7B-Instruct**（Bai et al., 2025）为骨架模型，在标准 GRPO 的优势计算流程中插入了难度评估、变体生成、难度加权和奖励重标定四个可插拔模块。相比仅做监督微调的 **SFT-7B** 基线，DIVA-GRPO 通过强化学习进一步释放了模型的多模态推理潜力。

实验表明，DIVA-GRPO-7B 在 MathVista、MathVerse、MathVision、OlympiadBench、WeMath 和 MMK12test 六个多模态数学推理基准上平均准确率达到 **54.58%**，远超同规模模型（基础模型 Qwen-2.5-VL-7B 为 46.23%），并逼近更大模型与商业系统。消融实验证实，自适应变体生成、难度加权、奖励范围重标定和全局-局部平衡每个组件均有正向贡献。在效率方面，DIVA-GRPO 相较标准 GRPO 将训练所需步数减少至多 **2.55 倍**，端到端时间加速 **1.76 倍**。此外，奖励范围重标定模块可独立应用于标准 GRPO，平均提升约 2 个百分点，验证了其泛化性。

该方法目前仅在多模态数学推理任务上得到验证，对纯文本或不同奖励结构任务的泛化能力仍有待探索；困难问题的变体生成依赖外部语言模型，可能引入模型偏差；难度加权中的超参数需针对任务调优，降低了开箱即用的便利性。

## 背景与动机

### 多模态推理中的强化学习瓶颈

多模态大语言模型在数学推理、科学问答等任务上取得了显著进展，但进一步提升推理能力仍面临挑战。基于强化学习的后训练方法，特别是**GRPO**（Group Relative Policy Optimization，Shao et al., 2024），通过组内相对优势估计为策略优化提供了有效的梯度信号，已成为提升模型推理能力的主流范式。

然而，GRPO在多模态推理场景中暴露出一个根本性问题：**奖励稀疏性与优势消失**。其原因在于，训练数据中问题的难度分布极不均匀——简单问题组内所有回应几乎全对、困难问题组内几乎全错，导致组内奖励方差趋近于零。此时，GRPO计算的优势函数

$$A ( y _ { i } ) = \frac { r ( y _ { i } ) - \mu _ { r } } { \sigma _ { r } + \epsilon }$$

因分母 $\sigma_r$ 过小而失效，优化信号近乎消失，训练效率急剧下降。

### 现有方法的局限性

针对上述瓶颈，现有工作主要沿两条路径展开：

- **选择性样本利用**：仅保留模型能产生混合正确/错误回应的“中等难度”样本进行训练，丢弃极端简单或困难的数据。这种方式虽然保证了优势信号的有效性，但造成大量训练数据的浪费，模型无法从简单样本中巩固能力、也无法从困难样本中探索突破。
- **无差别样本增强**：通过对所有问题统一生成文本或图像变体来扩充数据。这种无难度感知的增强策略反而可能加剧优势稀疏——简单问题经过增强后仍然过易，困难问题依然过难，无法从根本上改善组内奖励的多样性。

### 核心动机：难度自适应变体优势

DIVA-GRPO的核心洞察在于：**问题的难度并非静态属性，而应作为动态调控优化信号的关键杠杆**。通过实时评估每个问题的历史准确率，自适应地为其生成不同难度等级的变体，可以主动塑造组内奖励分布，使优势信号持续有效。

具体而言，该方法遵循三条设计原则：
1. **难度感知的变体生成**：对简单问题施加图像/文本扰动以增加挑战性，对中等难度问题提供多样化释义以保持信号质量，对困难问题引入分步推理提示以降低门槛，从而将每个问题的变体组调整到“约50%正确率”的最优信号区间。
2. **局部-全局联合优势估计**：同时在原始问题内部（局部）和问题-变体扩展组（全局）计算优势，通过批归一化平衡两者尺度，避免单一范围估计的偏差。
3. **难度加权与奖励重标定**：根据问题相对难度对优势进行指数加权，困难问题的正确回应获得放大信号、错误回应减轻惩罚；同时引入基于奖励范围的重标定机制，防止组内奖励差异过小时优势被标准化过度放大。

这些设计共同指向一个目标：**在保持优化方向无偏的前提下，降低梯度估计方差，提升训练稳定性与效率**。理论分析（附录B）表明，难度加权和归一化可有效降低梯度方差并保持无偏估计，而50/50的正确-错误比例提供最强的优化信号。

## 核心创新

DIVA-GRPO针对GRPO在多模态推理中面临的**奖励稀疏与优势消失**瓶颈，提出了一套以“难度自适应变体生成”为核心的优化框架。其根本问题在于：问题难度分布不均导致组内奖励方差过小（困难问题所有回应均错误）或过大（简单问题所有回应均正确），使得标准化优势信号趋于零或噪声主导，优化方向不稳定，训练效率低下。

为解决这一问题，DIVA-GRPO引入了四个相互协同的changed slots，形成从问题空间扩展到信号估计再到信号校准的完整链路：

**1. 难度自适应的变体生成策略**
标准GRPO仅对原始问题采样回应，无变体生成。DIVA-GRPO则根据实时评估的问题难度，自适应地生成语义一致的变体以扩大有效奖励方差：对简单问题添加图像/文本扰动增加挑战性，对中等难度问题生成多样化释义变体，对困难问题引入分步推理提示降低难度。这一策略的核心在于**动态调整问题组内的难度分布**，使奖励信号从“全对”或“全错”的极端状态回归到具有区分度的中间状态，从而为后续优势计算提供有效方差。

**2. 局部-全局联合优势计算**
标准GRPO仅在单个问题内部（局部）计算标准化优势。DIVA-GRPO将优势计算扩展到两个范围：对原始问题的回应组计算局部优势，对包含变体的扩展组计算全局优势。随后通过批归一化（z-score）平衡两者尺度，解决局部与全局优势数值范围不一致的问题。这一设计使得模型既能利用问题内部的相对比较信号，又能从跨变体的全局视角获取更丰富的奖励差异信息。

**3. 难度加权的优势缩放**
标准GRPO对所有问题平等对待，无难度相关加权。DIVA-GRPO根据变体难度与组平均难度的相对差异进行指数加权：
$$\hat{A}(y_i \mid q^{(i)}) = \exp\Big( k \cdot (D_q^{(i)} - \bar{D}_q) \cdot \operatorname{sgn}(\tilde{A}(y_i)) \Big) \cdot \tilde{A}(y_i)$$
其核心逻辑是：困难问题的正确回应应获得更强的正向激励，而错误回应则减轻惩罚（因为困难本身是合理的失败原因）；简单问题则相反。这种难度感知的缩放机制在保持优化方向无偏的前提下，放大了高信息量样本的梯度信号。

**4. 奖励范围重标定**
标准GRPO无此机制，当组内奖励范围极小时，标准化操作会将微小的奖励差异过度放大，导致优势估计失真。DIVA-GRPO引入基于奖励范围的重标定：
$$\Delta r_q = (\max(\mathcal{R}_q) - \min(\mathcal{R}_q)) / R_{\max}, \quad \hat{A}_{\mathrm{range}}(y_i) = \Delta r_q \cdot \tilde{A}(y_i)$$
当组内奖励全为0或全为1时，$\Delta r_q$趋近于0，优势信号被自动压缩至接近零，避免了对无意义差异的过度优化。该模块可独立应用于标准GRPO，消融实验表明仅添加RRB-Rescaling即可将平均准确率从60.23%提升至62.17%（Table 3），验证了其作为通用组件的泛化能力。

**创新点之间的因果联动**：难度评估模块（Section 3.1）通过历史rollout准确率动态更新每个问题的难度系数，驱动变体生成策略选择合适难度的变体；变体生成扩展了奖励空间，使全局优势计算成为可能；批归一化平衡了局部与全局优势的尺度；难度加权和奖励范围重标定则分别从“问题难度”和“奖励差异可信度”两个维度对优势信号进行精细校准。四者协同作用，从根本上缓解了奖励稀疏与优势消失问题，同时将训练所需步数减少至多2.55倍，端到端时间加速1.76倍（Figure 3c, Section 4.3 RQ4）。

## 整体框架

![[assets/figures/papers/paper_list_l48_https_openreview_net_forum_id_qKXYEg00eH/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the proposed DIVA-GRPO method. For a given question, we dynamically assess its difficulty based on past rollout rewards and adaptively sample variants of different difficulty levels. As shown, when the original question is hard, easier variants are sampled to ensure reward diversity. We then compute local (the question itself) and global (the question with its variants) advantages, and obtain the final advantage through difficulty-aware reweighting and reward-range rescaling to update the policy model*

DIVA-GRPO 的整体流程围绕一个核心设计展开：**通过动态难度评估驱动变体生成，在局部与全局两个粒度上构造优势信号，并通过难度加权与奖励范围重标定稳定优化方向**。图2给出了端到端的流水线示意。

**输入与初始化。** 系统接收多模态数学问题 $q = (I_q, T_q)$，其中 $I_q$ 为图像、$T_q$ 为文本。所有问题的难度系数 $D_q$ 初始化为中间值 $5$（范围 $[1, 9]$）。文本变体与推理提示由 GPT-o3 离线预生成，图像扰动在训练时在线施加。

**流水线模块与执行顺序。** 每个训练轮次中，流水线按以下步骤执行：

1. **难度评估模块**（Section 3.1）：根据上一轮历史 rollout 的经验准确率 $\alpha$，按规则 $D^{\mathsf{new}} = \mathrm{clip}(D^{\mathsf{old}} + \eta \cdot (0.5 - \alpha), D_{\min}, D_{\max})$ 更新每个问题的难度。该规则将难度向 $0.5$ 准确率方向收敛——准确率高于 $0.5$ 则难度上升，反之下降，确保问题始终处于“有区分力”的难度区间。

2. **自适应变体生成模块**（Section 3.2）：根据当前难度等级，为每个原始问题生成语义一致的变体 $q^{(i)}$：
   - **简单问题**（$D_q < D_{\text{low}}$）：施加复杂图像扰动（如旋转、遮挡、颜色抖动）和文本扰动，增加识别难度以扩大奖励方差。
   - **中等难度**（$D_{\text{low}} \leq D_q \leq D_{\text{mid}}$）：生成多样化文本释义变体，保持语义等价但表述不同。
   - **困难问题**（$D_q > D_{\text{mid}}$）：引入分步推理提示 $R_q^{(i)}$，将变体构造为 $q^{(i)} = (I_q, T_q \oplus R_q^{(i)})$，通过提供部分推理引导降低有效难度，使模型有机会获得正奖励。

   这一策略的核心因果逻辑是：**困难问题需要“降级”变体以引入成功样本，简单问题需要“升级”变体以引入失败样本**，从而在问题组内维持足够的奖励方差，避免优势消失。

3. **局部与全局优势计算**（Section 3.3）：对每个原始问题及其变体分别采样 $k$ 个回应，计算两组标准化优势：
   - **局部优势** $A_{\mathrm{local}}$：仅在原始问题的 $k$ 个回应组内计算标准化奖励。
   - **全局优势** $A_{\mathrm{global}}$：在原始问题及其所有变体的联合回应组内计算标准化奖励。
   
   两组优势分别经过批级 z-score 归一化，得到 $\tilde{A}_{\mathrm{local}}$ 和 $\tilde{A}_{\mathrm{global}}$，以平衡两者尺度。

4. **难度加权**（Section 3.3）：将归一化后的优势按相对难度进行指数缩放：
   $$\hat{A}(y_i \mid q^{(i)}) = \exp\Big(k \cdot (D_q^{(i)} - \bar{D}_q) \cdot \operatorname{sgn}(\tilde{A}(y_i))\Big) \cdot \tilde{A}(y_i)$$
   其中 $\bar{D}_q$ 为问题组的平均难度。当变体难度高于组均值时，正确样本的优势被放大（强化正向信号），错误样本的优势被压缩（减轻惩罚）；难度低于均值时则相反。这种非对称缩放使困难变体的成功经验得到充分激励，同时避免简单变体的偶然错误被过度惩罚。

5. **奖励范围重标定模块**（Section 3.4）：当组内奖励范围极小时（如所有回应均正确或均错误），标准化操作可能将微小差异放大为虚假强信号。RRB-Rescaling 通过归一化奖励范围进行二次缩放：
   $$\Delta r_q = (\max(\mathcal{R}_q) - \min(\mathcal{R}_q)) / R_{\max}, \quad \hat{A}_{\mathrm{range}}(y_i) = \Delta r_q \cdot \tilde{A}(y_i)$$
   当组内奖励完全一致时 $\Delta r_q = 0$，优势被置零，避免无意义更新。该模块可独立应用于标准 GRPO，具有泛化价值。

**输出与策略更新。** 最终优势 $\hat{A}_{\mathrm{range}}$ 替代原始 GRPO 中的标准化奖励，驱动策略模型 $\pi_\theta$ 的参数更新。整个流水线在 EasyR1 框架上实现，基础模型为 Qwen-2.5-VL-7B-Instruct。

**模块间的因果依赖。** 难度评估是整个流程的“调度器”——它决定了变体生成的方向，进而影响全局优势的奖励分布；难度加权和 RRB-Rescaling 则是对已计算优势的“后处理校准”，两者互补：前者解决难度差异导致的信号尺度失衡，后者解决奖励范围过窄导致的信噪比恶化。消融实验表明，移除任一模块均导致性能下降，全模型组合达到最优（Table 2）。

## 核心模块与公式推导

### 3.1 难度评估模块

DIVA-GRPO 首先为每个问题维护一个动态难度系数 $D_q$，该系数基于历史 rollout 的准确率在每个训练 epoch 重新校准。具体而言，对于问题 $q$，统计其所有变体 $m$ 和每个变体的 $k$ 次 rollout 的经验准确率：

$$\alpha = \frac{1}{mk} \sum_{i=1}^{m} \sum_{j=1}^{k} \mathbb{I}[y_{i,j} \text{ is correct}]$$

然后按如下规则更新难度：

$$D^{\sf new} = \mathrm{clip}\left( D^{\sf old} + \eta \cdot (0.5 - \alpha), D_{\mathrm{min}}, D_{\mathrm{max}} \right)$$

其中 $\eta$ 为学习率，$D_{\mathrm{min}}$ 和 $D_{\mathrm{max}}$ 为难度边界（论文设定 $D_{\min}=1$，$D_{\max}=9$，$\eta=4$，初始值 $\bar{D}=5$）。该规则的核心机制是：当模型对某问题的准确率 $\alpha$ 偏离 0.5 时，难度系数向 0.5 方向调整——准确率过高则难度上升，准确率过低则难度下降。这种设计使得难度分布始终围绕 0.5 的“最优信号点”波动，为后续的优势计算提供稳定的方差基础。

### 3.2 自适应变体生成模块

根据问题的难度等级，模块生成不同性质的变体以扩大有效奖励方差：

- **简单问题** ($D_q < D_{\mathrm{mid}}$)：对图像施加扰动（如旋转、裁剪、噪声注入）并对文本进行复杂改写，增加问题难度。
- **中等难度问题** ($D_{\mathrm{mid}} \leq D_q \leq D_{\mathrm{high}}$)：生成多样化的文本释义变体，保持语义一致但表述不同。
- **困难问题** ($D_q > D_{\mathrm{high}}$)：引入分步推理提示，将原始问题 $q = (I_q, T_q)$ 扩展为 $q^{(i)} = (I_q, T_q \oplus R_q^{(i)})$，其中 $R_q^{(i)}$ 为预生成的推理引导文本。

文本变体和推理序列均通过 GPT-o3 离线预生成，图像扰动则在训练时在线施加，从而在不显著增加训练开销的前提下实现难度自适应的样本空间扩展。

### 3.3 局部-全局优势计算与难度加权

#### 局部优势

对每个原始问题的 $k$ 个回应，沿用标准 GRPO 的优势计算：

$$A_{\mathrm{local}}(y_i) = \frac{r(y_i) - \mu_r}{\sigma_r + \epsilon}$$

其中 $\mu_r$ 和 $\sigma_r$ 为该问题组内回应的奖励均值和标准差。

#### 全局优势

将原始问题与其变体合并为一个扩展组，计算跨变体的标准化优势：

$$A_{\mathrm{global}}(y_i^{(j)}) = \frac{r(y_i^{(j)}) - \mu_q}{\sigma_q + \epsilon}$$

其中 $\mu_q$ 和 $\sigma_q$ 为该问题及其所有变体的全部回应的奖励均值和标准差。

#### 批归一化

由于局部和全局优势的尺度可能不平衡，对整批数据分别进行 z-score 归一化：

$$\tilde{A}_{\mathrm{local}}(y) = \frac{A_{\mathrm{local}}(y) - \mu_{\mathrm{local}}}{\sigma_{\mathrm{local}} + \epsilon}$$

$$\tilde{A}_{\mathrm{global}}(y) = \frac{A_{\mathrm{global}}(y) - \mu_{\mathrm{global}}}{\sigma_{\mathrm{global}} + \epsilon}$$

#### 难度加权缩放

在归一化后的优势上，根据变体难度 $D_q^{(i)}$ 与组平均难度 $\bar{D}_q$ 的相对差异进行指数加权：

$$\hat{A}(y_i \mid q^{(i)}) = \exp\Big( k \cdot (D_q^{(i)} - \bar{D}_q) \cdot \operatorname{sgn}(\tilde{A}(y_i)) \Big) \cdot \tilde{A}(y_i)$$

其中 $k$ 为温度系数，$\operatorname{sgn}(\cdot)$ 为符号函数。该公式的机制是：当变体比组平均更难时 ($D_q^{(i)} > \bar{D}_q$)，正确样本 ($\tilde{A}>0$) 的优势被放大、错误样本 ($\tilde{A}<0$) 的惩罚被减轻；反之，当变体更容易时，正确样本的优势被抑制、错误样本的惩罚被加强。这种设计使得困难问题的正向信号和简单问题的负向信号都能得到有效利用，缓解了奖励稀疏与优势消失问题。

### 3.4 奖励范围重标定

当组内奖励范围极小时（如所有回应均正确或均错误），即使标准化后的优势也可能因分母 $\sigma_r$ 过小而被过度放大。为解决这一问题，引入基于奖励范围的重标定：

$$\Delta r_q = (\max(\mathcal{R}_q) - \min(\mathcal{R}_q)) / R_{\max}$$

$$\hat{A}_{\mathrm{range}}(y_i) = \Delta r_q \cdot \tilde{A}(y_i)$$

其中 $\mathcal{R}_q$ 为组内所有回应的奖励集合，$R_{\max}$ 为奖励的最大可能值。当组内奖励完全一致时，$\Delta r_q = 0$，优势被完全压缩为零，避免对无意义差异的过度优化。该模块可独立应用于标准 GRPO，消融实验表明其单独使用即可将平均准确率从 60.23% 提升至 62.17%（Table 3）。

### 整体优化目标

最终的优势信号由难度加权后的局部和全局优势联合构成，代入策略梯度更新：

$$\nabla_{\boldsymbol{\theta}} \mathcal{L}(\boldsymbol{\theta}) = \mathbb{E}_{\boldsymbol{q} \sim \mathcal{Q}, \boldsymbol{y} \sim \pi_{\boldsymbol{\theta}}} \left[ \hat{A}(\boldsymbol{y}) \cdot \nabla_{\boldsymbol{\theta}} \log \pi_{\boldsymbol{\theta}}(\boldsymbol{y} \mid \boldsymbol{q}) \right]$$

理论分析（Appendix B, C）证明，难度加权和批归一化可在保持梯度估计无偏的前提下降低梯度方差，且 50/50 的正确-错误比例能够提供最强的优化信号。

## 实验与分析

### 核心瓶颈与实验动机

GRPO在多模态推理中面临的核心困境是**奖励稀疏性与优势消失**：问题难度分布不均导致组内奖励方差过小（简单问题全对、困难问题全错），标准化后的优势信号趋近于零，优化方向丧失。DIVA-GRPO的实验设计围绕三个递进问题展开：(1) 难度自适应变体生成能否恢复有效优势信号？(2) 各组件（难度加权、RRB重标定、全局-局部平衡）分别贡献多少？(3) 方法能否提升训练效率？

### 主要结果：7B规模的SOTA性能

Table 1展示了DIVA-GRPO-7B在六个多模态数学推理基准上的全面对比。该方法以**54.58**的平均准确率在所有7B模型中取得最优，相较基础模型Qwen-2.5-VL-7B-Instruct（46.23）提升**+8.35**个百分点，并逼近甚至超越部分更大规模模型与商业系统。

![[assets/figures/papers/paper_list_l48_https_openreview_net_forum_id_qKXYEg00eH/figures/003_Table_1.jpg]]
*Table 1: Performance comparison across multimodal mathematical benchmarks. Bold denotes the best performance among 7B models, and underline marks the best overall performance. Evaluation is conducted with VLMEvalKit (Duan et al., 2024), while results for other models are taken from Meng et al. (2025) and Yao et al. (2025). For each entry, the score before “/” is our re-evaluation using the officially released checkpoints, and the score after “/” is reported in the original paper*

| 基准 | DIVA-GRPO-7B | Qwen-2.5-VL-7B | 提升幅度 |
|------|-------------|----------------|---------|
| MathVista | 74.2 | 68.2 | +6.0 |
| MathVerse | 57.6 | 47.9 | +9.7 |
| MathVision | 32.1 | 25.4 | +6.7 |
| OlympiadBench | 23.1 | 20.2 | +2.9 |
| WeMath | 69.3 | 62.1 | +7.2 |
| MMK12test | 70.2 | 53.6 | +16.6 |
| **平均** | **54.58** | **46.23** | **+8.35** |

**关键观察**：MMK12test上的+16.6增幅最为显著，该基准涵盖数学、物理、化学、生物四学科（见Table 6，DIVA-GRPO在各学科分别达到78.3/62.2/69.6/70.7），说明难度自适应策略对跨学科、难度差异大的场景尤为有效。OlympiadBench提升最小（+2.9），符合预期——竞赛级问题即使引入变体也难以稳定获得正反馈，这是方法的固有局限。

### 消融实验：各组件的独立贡献

Table 2的消融实验逐一移除四个核心组件，验证了每个设计的必要性：

![[assets/figures/papers/paper_list_l48_https_openreview_net_forum_id_qKXYEg00eH/figures/013_Table_2.jpg]]
*Table 2: Ablation study of DIVA-GRPO, showing that each component provides gains and the full model achieves the best performance (accuracy, %)*

- **移除自适应变体生成**（含全局-局部优势与平衡）：MathVista下降3.2分，MathVerse下降1.2分。这直接印证了变体生成是恢复奖励多样性的关键——没有变体时，困难问题的组内方差依旧为零。
- **移除难度加权**：MMK12test大幅下降7.7分，说明难度自适应权重对该基准的跨难度分布至关重要。简单问题的正确样本被过度奖励、困难问题的错误样本被过度惩罚时，优化信号失真。
- **移除RRB-Rescaling或G-L Balance**：平均准确率分别下降约1-2个百分点，影响虽小于前两者，但累积效应明显——全模型在所有指标上均取得最优。

**因果链条**：变体生成扩大了奖励方差（必要条件），难度加权确保信号方向正确（充分条件），RRB重标定防止小差异被标准化放大（稳定条件），三者协同才能最大化性能。

### RRB-Rescaling的独立泛化性

Table 3验证了奖励范围重标定模块可独立应用于标准GRPO。在MathVista、MathVerse、MMK12test三个基准上，GRPO+RRB将平均准确率从60.23%提升至62.17%（+1.94个百分点）。这表明**奖励范围重标定是一个即插即用的通用改进**，其原理——当组内奖励极差过小时自动缩小优势幅度——适用于任何基于组相对优势的RL框架。

![[assets/figures/papers/paper_list_l48_https_openreview_net_forum_id_qKXYEg00eH/figures/014_Table_3.jpg]]
*Table 3: Evaluation of RRB-Rescaling on standard GRPO*

### 训练效率：至多2.55倍步数缩减

Figure 3c展示了训练步数与验证集性能的关系。DIVA-GRPO（N=3）仅需约75步即达到GRPO约190步才能达到的性能水平，**步数加速2.55倍**，端到端时间加速1.76倍。Figure 4进一步解释：DIVA-GRPO每步训练时间仅略微增加（主要因变体导致输出长度增大），但所需总步数大幅减少，净效率提升显著。

![[assets/figures/papers/paper_list_l48_https_openreview_net_forum_id_qKXYEg00eH/figures/006_Figure_3.jpg]]
*Figure 3: Effect of Training Steps on Model Performance on the Validation Set*

效率提升的机制在于：变体生成使每步采样的奖励信号更丰富，策略梯度估计的方差更低（附录B、C的理论分析证明了难度加权和归一化可降低梯度方差并保持无偏估计），因此模型能以更少步数收敛。

### 训练动态：难度-优势联合分布的演化

Figure 5通过3D核密度估计展示了训练过程中问题难度与全局优势的联合分布变化：
- **早期阶段**：样本尚未形成清晰的难度分布，优势信号集中在零附近。
- **中期阶段**：难度分布开始分化，优势信号随难度呈现结构化分布——中等难度问题的优势方差最大，提供最强优化信号。
- **后期阶段**：分布趋于稳定，各难度区间均有有效的非零优势信号，说明方法成功维持了持续的学习动力。

![[assets/figures/papers/paper_list_l48_https_openreview_net_forum_id_qKXYEg00eH/figures/012_Figure_5.jpg]]
*Figure 5: 3D kernel density estimation (KDE) surfaces of the joint distribution between problem difficulty and global advantage across different training stages. The surface height reflects the sample density, illustrating how the model’s learning dynamics evolve with respect to difficulty and advantage*

这与附录中“50/50的正确-错误比例给出最强优化信号”的理论结论一致：难度更新规则（$D^{\sf new} = \mathrm{clip}( D^{\sf old} + \eta \cdot (0.5 - \alpha), D_{\mathrm{min}}, D_{\mathrm{max}} )$）天然将问题难度向0.5准确率收敛，确保多数问题处于信息量最大的区间。

### 跨模型泛化与外部模型依赖

Table 4（附录C.2）在Qwen3-VL-4B和Qwen3-VL-8B上验证了DIVA-GRPO的跨模型泛化性，在数学、物理、化学、生物四学科上均一致优于GRPO基线。Table 5（附录D.3）对比了使用GPT-o3与Qwen-Plus生成变体的效果差异，GPT-o3整体略优（+0.3平均分），但差距不大，说明方法对变体生成模型的选择具有一定鲁棒性。

### 局限与需人工验证的声明

- 相对难度加权与绝对难度加权的消融（Figure 15/附录D.5）显示两者最终性能相近，论文从逻辑一致性角度选择相对加权，但该结论的置信度较低（0.9），建议人工核实。
- 所有变体生成依赖外部模型GPT-o3离线预生成，论文未验证完全脱离外部模型（如使用模型自身生成变体）的可行性。
- 超参数$k$（难度加权指数）和$\eta$（难度更新步长）需针对任务调优，开箱即用的鲁棒性未充分验证。

## 方法谱系与知识库定位

### 与基线方法的关系

DIVA-GRPO 的核心出发点是解决 **GRPO**（Shao et al., 2024）在多模态推理场景中面临的奖励稀疏性与优势消失问题。GRPO 通过对单个问题内的回应组进行标准化来计算优势函数：

$$A ( y _ { i } ) = \frac { r ( y _ { i } ) - \mu _ { r } } { \sigma _ { r } + \epsilon }$$

然而，当问题难度分布不均时，组内奖励方差过小（简单问题全部正确）或过大（困难问题近乎随机），导致优化信号不稳定、训练效率低下。DIVA-GRPO 在 GRPO 的基础上引入了四个关键改进槽位：

- **变体生成策略**：将 GRPO 的“仅对原始问题采样回应”扩展为“根据实时评估的难度自适应生成图像扰动、文本改写或分步推理提示等变体”，从而扩大有效奖励方差。
- **优势计算范围**：将 GRPO 的“仅局部组内标准化”扩展为“同时在问题内部（局部）和问题跨变体组（全局）计算优势，并通过批归一化平衡两者尺度”。
- **优势加权方式**：将 GRPO 的“无难度加权”扩展为“根据问题难度相对系数进行指数加权”——困难问题的正确样本放大信号、错误样本减轻惩罚，反之亦然。
- **奖励范围重标定**：引入奖励范围重标定（RRB-Rescaling），当组内奖励范围极小时自动缩小优势幅度，避免高估微小差异。该模块可独立应用于标准 GRPO，消融实验表明仅添加 RRB-Rescaling 即可将平均准确率从 60.23% 提升至 62.17%（Table 3）。

实验以 **Qwen-2.5-VL-7B-Instruct**（Bai et al., 2025）为基础骨架模型，采用相同的 RL 训练框架 EasyR1 进行公平对比。DIVA-GRPO-7B 在六个多模态推理基准上平均达到 54.58 分，远超同规模模型（Table 1）。此外，还对比了直接使用 GPT-o3 推理轨迹进行监督微调的 **SFT-7B** 基线，验证了 RL 优化相对于 SFT 的优势。

### 适用边界与局限

尽管 DIVA-GRPO 在多模态数学推理任务上表现突出，其适用边界和局限值得审慎评估：

1. **外部模型依赖**：困难问题的变体生成依赖 GPT-o3 提供推理提示，文本变体和推理序列均离线预生成。这引入了外部模型偏差，且增加了方法对特定 API 的耦合度。对于无法访问同等能力外部模型的场景，方法效果可能下降。

2. **超参数敏感性**：难度加权涉及超参数 $k$ 和 $\eta$，难度更新规则中的 $\eta$ 控制难度向 0.5 收敛的速度。实验设置中 $\eta=4$、难度初始化为 5、范围 $[1, 9]$，但不同任务可能需要重新调优，降低了开箱即用的便利性。消融实验也表明，移除难度加权导致 MMK12test 大幅下降 7.7 分（Table 2），说明该模块对性能贡献显著且敏感。

3. **任务泛化性未验证**：目前仅在多模态数学推理任务（MathVista、MathVerse、MathVision、OlympiadBench、WeMath、MMK12test）上验证，对纯文本推理、代码生成或不同奖励结构的任务泛化性未知。虽然附录 C 展示了在科学领域（数学、物理、化学、生物）的跨基础模型实验（Qwen3-VL-4B/8B），但仍限于多模态场景。

4. **复杂问题的根本困难**：对于高度复杂或结果难以验证的问题，即便提供分布调整也难以稳定获得正反馈。困难问题的变体生成策略（引入分步推理提示）本质上降低了问题难度，可能无法真正提升模型对核心推理能力的掌握。

### 开放问题

1. **跨模态与跨任务泛化**：如何将难度自适应变体生成和优势重标定推广到文本推理、代码生成等非多模态任务？这些场景中“图像扰动”等变体策略需要重新设计，奖励结构也可能从二值正确/错误变为连续信号。

2. **去外部依赖的变体生成**：能否在不依赖 GPT-o3 等外部大模型的情况下生成高质量的困难变体？例如使用模型自身生成推理提示（自举式训练）或基于规则的小型系统。这将降低方法的外部耦合度并提高可复现性。

3. **连续奖励信号的适配**：当前方法假设奖励为二值（正确/错误），难度更新规则也基于此设计。对于连续奖励信号（如 BLEU、ROUGE 或人工评分）的环境，难度评估和优势加权机制应如何调整？奖励范围重标定中的 $R_{\max}$ 归一化可能需要重新定义。

4. **难度评估的理论最优性**：当前难度更新规则使准确率向 0.5 收敛，理论分析表明 50/50 的正确-错误比例给出最强优化信号。但在实际训练中，不同阶段的最优难度分布是否应动态变化？训练初期可能需要更多简单样本以稳定学习，后期则需要更多困难样本以突破瓶颈。

## 原文 PDF

![[paperPDFs/ICLR_2026/DIVA_GRPO_Enhancing_Multimodal_Reasoning_through_Difficulty_Adaptive_Variant_Advantage.pdf]]
