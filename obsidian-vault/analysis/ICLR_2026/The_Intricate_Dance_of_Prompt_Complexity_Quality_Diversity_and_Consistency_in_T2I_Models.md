---
title: "The Intricate Dance of Prompt Complexity, Quality, Diversity and Consistency in T2I Models"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/The_Intricate_Dance_of_Prompt_Complexity_Quality_Diversity_and_Consistency_in_T2I_Models.pdf
project_link: null
code_link: https://github.com/facebookresearch/synthetic_data_utility_prompt_complexity
openreview_forum_id: RBIBMCdw7y
aliases:
- TPCEF
- IDPCQDCTM
tags:
- ICLR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: "提示复杂度（通过提示长度和概念特异性量化），可直接影响合成图像在质量、多样性和一致性三个效用轴上的表现。"
primary_logic: "增加提示复杂度会降低合成数据的条件多样性并削弱提示一致性，但有助于缩小合成数据与真实数据之间的分布差距；反之，向更简单提示泛化更加困难，这源于扩散模型无法在学习得分函数时获取条件似然，而通过组合高级引导与提示扩展可以获得最佳的多样性-保真度权衡。"
claims:
- "在合成高斯混合实验中，当模型用细粒度提示训练并尝试生成一般提示（如“猫”）且CFG尺度>1时，生成样本严重偏向分布均值并落入低密度区域，导致KL散度高达23.78、FD为14.41，多样性极低。"
- "在CC12M和ImageNet-1k上，随着提示长度（复杂性）增加，所有模型和干预方法的多样性（Vendi指数）均下降，但提示扩展在低复杂度时可使多样性超越真实数据。"
- "在DCI数据集上，当提示长度超过约30词时，多样性下降趋势趋于平缓，而一致性持续下降，说明模型对过长约束的遵循能力有限。"
- "提示扩展和高级引导（尤其是APG与提示扩展组合）在提升多样性的同时维持了可比的质量和FDD，但会降低精确度和密度，表明生成样本偏离了真实数据支撑集。"
---

# The Intricate Dance of Prompt Complexity, Quality, Diversity and Consistency in T2I Models

> [!tip] 核心洞察
> 增加提示复杂度会降低合成数据的条件多样性并削弱提示一致性，但有助于缩小合成数据与真实数据之间的分布差距；反之，向更简单提示泛化更加困难，这源于扩散模型无法在学习得分函数时获取条件似然，而通过组合高级引导与提示扩展可以获得最佳的多样性-保真度权衡。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 文本到图像模型中提示复杂度、质量、多样性与一致性的复杂交互 |
| 英文题名 | The Intricate Dance of Prompt Complexity, Quality, Diversity and Consistency in T2I Models |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=RBIBMCdw7y) · [GitHub](https://github.com/facebookresearch/synthetic_data_utility_prompt_complexity) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | T2I合成数据提示复杂度评估框架 (Prompt Complexity Evaluation Framework) |
| Dataset | CC12M, ImageNet-1k |

> [!tip] 效果简介
> - CC12M 上，Vendi diversity score 为 Prompt expansion + CFG (LDMv1.5)，对比 Vanilla CFG (LDMv1.5)，变化 提升约 +5.85 点（复杂度1：9.23 -> 15.07）。
> - CC12M 上，Aesthetic quality 为 Prompt expansion + CFG (LDMv3.5L)，对比 Vanilla CFG (LDMv3.5L)，变化 提升约 +0.2 点（复杂度4：4.98 -> 5.18，估算）。
> - CC12M 上，DSG consistency 为 Vanilla CFG，对比 Prompt expansion or advanced guidance，变化 提示扩展和高级引导均导致一致性下降（-0.05~0.1）。

## 概要

文本到图像（T2I）生成模型在合成数据增强、创意设计等领域展现出巨大潜力，但**提示（prompt）的复杂度如何系统性影响合成数据的效用**——包括质量、多样性和一致性——仍是一个未被充分探索的核心问题。本文揭示了扩散模型的一个根本性瓶颈：**模型无法直接估计条件似然**，导致在向更一般（即更简单、更宽泛）的提示泛化时，生成样本出现严重的分布偏移和模式坍缩；而现有的推理干预方法在试图提升多样性时，往往以牺牲提示一致性和分布保真度为代价。

论文的核心洞察是：**提示复杂度是调节合成数据效用的关键因果旋钮**。具体而言，增加提示复杂度（通过提示长度和概念特异性量化）会降低条件多样性并削弱提示一致性，但有助于缩小合成数据与真实数据之间的分布差距。反之，从细粒度提示向一般提示泛化极为困难——这一现象可通过扩散模型得分函数的“OR算子”结构得到理论解释：一般提示的得分函数是各细粒度提示得分的加权和，但其权重（即条件似然）并未被模型学习，导致模型倾向于生成各模态的均值区域样本，落入低密度区。相比之下，向更具体提示泛化（“AND算子”）则相对容易，因为其得分函数可近似为各一般提示得分差之和，与分类器免引导（CFG）在形式上有天然对应。

为系统研究这一现象，论文提出了一套**提示复杂度评估框架**，通过“复杂度量化—配对—对齐—采样—生成”五步流水线，在不同复杂度级别上构建可比的图像-提示配对，并在多个常用视觉数据集（CC12M、ImageNet-1k、DCI）上对主流T2I模型（LDMv1.5、LDMv3.5L等）及多种推理干预方法（提示扩展、CADS、Interval Guidance、APG）进行了全面评估。

主要发现包括：
- **多样性随复杂度增加而下降**：在CC12M和ImageNet-1k上，所有模型和干预方法的Vendi多样性指数均随提示长度增加而降低，但提示扩展在低复杂度时可使多样性超越真实数据水平。
- **一致性持续恶化**：当提示长度超过约30词时，多样性下降趋于平缓，但提示一致性（DSG分数）持续下降，表明模型对过长约束的遵循能力有限。
- **高级引导与提示扩展的最优组合**：APG与提示扩展的组合在提升多样性的同时，维持了可比的质量和分布距离（FDD），但会牺牲精确度和密度，表明生成样本偏离了真实数据支撑集。
- **模型代际差异显著**：LDMv3.5L的审美质量最佳但多样性最低，LDMv1.5的FDD最佳但一致性最差，不同模型在效用轴上存在根本性的权衡。

这些发现为T2I模型的提示设计、推理干预选择以及合成数据的下游应用提供了重要的指导原则。



文本到图像（T2I）生成模型近年来取得了显著进展，以 Stable Diffusion（LDM 系列）为代表的扩散模型能够根据自然语言描述合成高质量、高保真度的图像。然而，随着这些模型被广泛应用于大规模合成数据生成以训练下游视觉模型，一个根本性问题逐渐浮现：**提示（prompt）的复杂度如何影响合成数据的效用？**

### 核心瓶颈：向一般提示泛化的困难

扩散模型的一个关键局限在于，其学习的是数据的得分函数（score function）$s_\theta(x_t|c)$，而非条件似然 $p_\theta(x_t|c)$。这导致模型在向更一般的提示泛化时面临严重的分布偏移和模式坍缩。具体而言，对于一个一般提示 $c_{\mathbf{g}}$（如“猫”），其得分函数可分解为细粒度提示得分的加权和：

$$s_{\theta}(x_t | c_{\mathbf{g}}) = \sum_{i \in \{1, 2, \dots, K\}} \left( \underbrace{p_{\theta}(x_t | c_{\mathbf{f}}^i)}_{\mathrm{not~learned~by~the~diffusion~model}} s_{e}(x_t | c_{\mathbf{f}}^i) \right)$$

其中权重 $p_{\theta}(x_t | c_{\mathbf{f}}^i)$ 正是模型未能学习的条件似然。当使用分类器免引导（Classifier-Free Guidance, CFG）且引导尺度 $\omega > 1$ 时，生成样本会严重偏向各参考分布的均值，落入低密度区域，导致多样性急剧下降。合成高斯混合实验（Figure 1b）定量印证了这一点：用细粒度提示训练的模型在生成“猫”时，KL 散度高达 23.78，FD 为 14.41，生成多样性（VS_gen=1.03）远低于真实分布（VS_ref=1.82）。

相反，向更细粒度提示泛化（AND 算子）则相对容易——其得分函数可近似为无条件得分与各一般提示得分差之和，这恰好与 CFG 在 $\omega \approx M$ 时的形式相似。这意味着模型天然具备零样本组合生成能力，但反向操作（从具体到一般）却构成了根本性挑战。

### 现有方法的缺口

当前提升合成数据多样性的干预方法主要沿两条路径展开：**提示扩展**（Prompt Expansion，通过预训练语言模型丰富提示内容）和**高级引导方法**（如 CADS、Interval Guidance、APG 等，通过修改采样过程中的条件信号来增加多样性）。然而，这些方法存在一个共同的盲区：

- **缺乏对提示复杂度这一因果变量的系统控制**。现有评估往往在固定提示集上进行，无法揭示提示本身的信息量如何调节合成数据在多样性、质量和一致性三个效用轴上的表现。
- **多样性提升的代价不明确**。初步证据表明，高级引导和提示扩展虽然能提高多样性，但往往以牺牲提示一致性和分布保真度（如精度和密度）为代价，而不同方法之间的权衡曲线尚未被系统刻画。
- **模型代际差异被忽视**。从 LDMv1.5 到 LDMv3.5L，模型架构和训练数据的演变如何改变其对提示复杂度的响应模式，缺乏横向比较。

### 本文动机

针对上述缺口，本文提出一个以**提示复杂度**为核心控制变量的评估框架，旨在系统回答以下问题：

1. 提示复杂度（通过长度和概念特异性量化）如何因果性地影响合成数据的多样性、质量和一致性？
2. 不同的推理干预方法（提示扩展、高级引导）在何种复杂度区间内有效，其效用提升的边界在哪里？
3. 如何通过组合策略获得最佳的多样性-保真度权衡？

该框架通过在已有图像-文本数据集上构建多复杂度提示并进行配对对齐，使跨复杂度的公平比较成为可能，为理解 T2I 模型的泛化行为提供了新的分析视角。



## 核心方法与创新机理

本文的核心创新并非提出一种新的生成模型或采样算法，而是构建了一个**面向提示复杂度的系统性评估框架**，并基于此框架揭示了文本到图像扩散模型中一个此前未被充分量化的根本性瓶颈：**向更一般（低复杂度）提示的泛化困难**。

### 1. 瓶颈发现：OR 算子的泛化困境

扩散模型的核心局限在于，其学习的得分函数无法直接获取条件似然。这一缺陷在数学上表现为：当模型需要根据一个一般性提示（如“猫”）生成图像时，其得分函数理论上应是对所有相关细粒度提示（如“白猫”、“黑猫”）得分的加权求和（OR 算子）：

$$s_{\theta}(x_t | c_{\mathbf{g}}) = \sum_{i \in \{1, 2, \dots, K\}} \left( \underbrace{p_{\theta}(x_t | c_{\mathbf{f}}^i)}_{\mathrm{not~learned~by~the~diffusion~model}} s_{e}(x_t | c_{\mathbf{f}}^i) \right)$$

然而，上式中的权重——即各细粒度提示的条件似然 $p_{\theta}(x_t | c_{\mathbf{f}}^i)$——并未被扩散模型所学习。这导致在常见的 CFG 尺度（$\omega > 1$）下，向一般提示的泛化产生严重的分布偏移：生成样本被拉向各子分布的均值，落入低密度区域，造成**模式坍缩和多样性崩溃**。

相比之下，向更细粒度提示的泛化（AND 算子）则相对容易，因为其得分函数可近似为无条件得分与各一般提示得分差之和，这与 CFG 在 $\omega \approx M$ 时的形式高度相似：

$$s_{\theta}(x_t | c_{\mathrm{f}}) = s_{\theta}(x_t) + \sum_{i \in \{1, 2, \ldots, M\}} \left( s_{\theta}(x_t | c_{\mathrm{g}}^i) - s_{\theta}(x_t) \right)$$

这一理论分析在高斯混合合成实验中得到了严格验证：当用细粒度提示训练模型并以一般提示“猫”进行推理时（$\omega > 1$），KL 散度高达 23.78，FD 为 14.41，生成多样性极低（Figure 1b）。这为理解真实 T2I 模型中的多样性退化提供了因果性解释。

### 2. 框架创新：提示复杂度评估体系

为将上述理论发现拓展到大规模真实场景，论文设计了一个五步数据策展流程，以提示复杂度为可控变量，系统评估生成数据的效用：

- **复杂度量化**：为每个样本创建 $K$ 个不同复杂度的文本描述。
- **配对**：对每个标题检索语义相似的图像集合，仅保留集合大小 $\geq 20$ 者。
- **对齐**：迭代移除非共享图像，确保不同复杂度下的图像集合具有可比性。
- **采样**：从对齐后的标题中随机抽取相同数量，最大化语义覆盖并保持复杂度间一致性。
- **生成**：使用 T2I 模型为每个采样提示生成 $N_{\mathrm{gen}}$ 张图像，$N_{\mathrm{gen}}$ 取所有复杂度下真实图像集合大小的最小值，以确保代表性。

该框架的独特价值在于：它不依赖任何单一模型或干预方法，而是将**提示复杂度作为因果调节旋钮**，在质量、多样性和一致性三个效用轴上同时观测生成行为的变化。这使得不同模型（LDMv1.5、LDMv3.5L）和不同干预方法（CFG、提示扩展、CADS、Interval Guidance、APG）之间的比较具有统一的参照系。

### 3. 干预组合：多样性-保真度权衡的最优解

在框架评估的基础上，论文进一步发现：**提示扩展与高级引导方法的组合**——尤其是提示扩展与 APG 的结合——可以在不牺牲质量和分布保真度（FDD）的前提下，显著提升多样性。这一发现超越了单独使用任一干预方法的效果，为实际合成数据生成提供了可操作的策略选择。



![[assets/figures/papers/paper_list_l16_https_openreview_net_forum_id_RBIBMCdw7y/figures/003_Figure_1.jpg]]
*Figure 1: Generalization to prompts of different complexities during inference. 1a shows the training data distribution. 1b presents the generated samples using the general prompt cat with the model trained with fine-grained prompts. 1c shows the generated samples using the fine-grained prompt black dog with the model trained with general prompts. ω is the classifier-free guidance scale. With $\omega$ > 1 , generalization towards more general prompts is harder in this synthetic setting*

### 核心瓶颈与设计动机

扩散模型在文本到图像（T2I）生成中的一个根本性瓶颈在于：模型无法直接估计条件似然 $p_{\theta}(x_t | c_{\mathbf{f}}^i)$，导致在向更一般提示（如“猫”）泛化时，生成样本严重偏向分布均值并落入低密度区域，产生分布偏移和模式坍缩（Figure 1b, Section 2）。具体而言，一般提示的得分函数可表示为细粒度提示得分函数的加权和（Equation 1）：

$$s_{\theta}(x_t | c_{\mathbf{g}}) = \sum_{i \in \{1, 2, \dots, K\}} \left( \underbrace{p_{\theta}(x_t | c_{\mathbf{f}}^i)}_{\mathrm{not~learned~by~the~diffusion~model}} s_{e}(x_t | c_{\mathbf{f}}^i) \right)$$

其中权重项 $p_{\theta}(x_t | c_{\mathbf{f}}^i)$ 未被扩散模型学习，使得该分解难以在实际推理中实现。相反，细粒度提示的得分函数可近似为无条件得分与各一般提示得分差之和（Equation 2），与 CFG 在 $\omega \approx M$ 时的形式类似，因此向更具体提示泛化相对容易：

$$s_{\theta}(x_t | c_{\mathrm{f}}) = s_{\theta}(x_t) + \sum_{i \in \{1, 2, \ldots, M\}} \left( s_{\theta}(x_t | c_{\mathrm{g}}^i) - s_{\theta}(x_t) \right)$$

基于这一理论洞察，本文提出**提示复杂度评估框架**，以提示复杂度为可操控的因果调节变量，系统评估其对合成数据在质量、多样性和一致性三个效用轴上的影响。

### 框架流水线

整个评估框架由五个顺序模块构成，从已有图像-文本数据集出发，构建不同复杂度级别的提示-图像配对，最终生成并评估合成数据。

**1. Captioning（复杂度量化）**  
为数据集中的每个样本创建 $K$ 个不同复杂度的文本描述。复杂度通过提示长度和概念特异性量化——低复杂度对应简短、一般性描述（如“猫”），高复杂度对应冗长、细粒度描述（如“一只坐在窗台上的黑色波斯猫”）。不同复杂度级别的词汇统计量见表1。

**2. Pairing（配对）**  
对于每个复杂度级别的每个标题，检索语义相似的图像集合 $\bar{\mathcal{T}}^{ik}$，并仅保留集合大小 $\geq 20$ 者，以确保统计显著性。

**3. Alignment（对齐）**  
迭代移除非共享图像，确保不同复杂度下的图像集合具有可比性。这一步对齐了图像模态，避免因不同复杂度对应不同图像子集而引入混淆。

**4. Sampling（采样）**  
从对齐后的标题中随机抽取相同数量，以最大化语义覆盖并保持复杂度间一致性。

**5. Generation（生成）**  
使用 T2I 模型为每个采样的提示生成 $N_{\mathrm{gen}}$ 张图像，其中：

$$N_{\mathrm{gen}} = \min_{i \in \mathcal{N}_k^{\mathrm{s}}, k \in \{1,2,\ldots,K\}} |\bar{\mathcal{Z}}^{ik}|$$

即取所有复杂度级别中相似图像集合的最小基数，确保生成样本的代表性。

### 评估维度与干预方法

框架在三个效用轴上评估合成数据：
- **多样性**：Vendi 指数（参考免）
- **质量**：审美评分（参考免）
- **一致性**：DSG 评分（参考免）
- **分布保真度**：FDD、精度、密度、覆盖率（参考基础，在可用真实图像时）

被评估的生成器包括 **Stable Diffusion v1.5**（LDMv1.5）和 **Stable Diffusion v3.5 Large**（LDMv3.5L），干预方法涵盖基础 **Classifier-Free Guidance**（CFG）（Ho & Salimans, 2022）、**Prompt Expansion**（Datta et al., 2024）、以及三种高级引导方法：**CADS**（Sadat et al., 2024）、**Interval Guidance**（Kynkaanniemi et al., 2024）和 **APG**（Sadat et al., 2025）。各高级引导方法的超参数配置见表2-4。

### 关键发现预览

框架揭示了提示复杂度与合成数据效用之间的复杂交互：增加提示复杂度会降低条件多样性并削弱提示一致性，但有助于缩小合成数据与真实数据之间的分布差距（FDD 改善）；提示扩展和高级引导（尤其是 APG 与提示扩展的组合）可在提升多样性的同时维持可比的质量和 FDD，但会牺牲精确度和密度，表明生成样本偏离了真实数据支撑集。



### 提示复杂度评估框架

本文提出一个五步数据管护框架，用于系统评估不同提示复杂度下T2I合成数据的效用。其核心模块如下：

1. **复杂度量化 (Captioning)**：为数据集中每个样本创建 $K$ 个不同复杂度的文本描述，复杂度由提示长度和概念特异性共同定义。
2. **配对 (Pairing)**：对于给定复杂度下的每个标题，检索语义相似的图像集合，仅保留集合大小 $\geq 20$ 者，确保统计可靠性。
3. **对齐 (Alignment)**：迭代移除非共享图像，使不同复杂度下的图像集合具有可比性。
4. **采样 (Sampling)**：从对齐后的标题中随机抽取相同数量，最大化语义覆盖并维持复杂度间一致性。
5. **生成 (Generation)**：使用T2I模型为每个采样提示生成 $N_{\text{gen}}$ 张图像，其中

$$N _ { \mathrm { g e n } } = \operatorname* { m i n } _ { i \in \mathcal { N } _ { k } ^ { \mathrm { s } } , k \in \{ 1 , 2 , \ldots , K \} } | \bar { \mathcal { Z } } ^ { i k } |$$

该公式取所有复杂度和提示下真实图像集合的最小基数，以确保生成样本的代表性。

### 核心公式：泛化困难的数学根源

扩散模型向不同复杂度提示泛化的不对称性，源于得分函数的结构差异。

**OR算子——向一般提示泛化**：当模型用细粒度提示训练，需生成一般提示 $c_{\mathbf{g}}$ 对应的样本时，其得分函数为

$$s_{\theta}(x_t | c_{\mathbf{g}}) = \sum_{i \in \{1, 2, \dots, K\}} \left( \underbrace{p_{\theta}(x_t | c_{\mathbf{f}}^i)}_{\mathrm{not~learned~by~the~diffusion~model}} s_{e}(x_t | c_{\mathbf{f}}^i) \right)$$

其中 $c_{\mathbf{f}}^i$ 为第 $i$ 个细粒度提示，$s_e(x_t | c_{\mathbf{f}}^i)$ 为对应得分函数，$p_{\theta}(x_t | c_{\mathbf{f}}^i)$ 为条件似然。**关键瓶颈**：扩散模型在学习得分函数时无法获取该条件似然，导致生成过程严重偏向各细粒度分布的均值，当CFG尺度 $\omega > 1$ 时尤其落入低密度区域。合成高斯混合实验中，该效应导致KL散度高达23.78、FD为14.41、多样性极低（Figure 1b）。

**AND算子——向细粒度提示泛化**：当模型用一般提示训练，需生成细粒度提示 $c_{\mathrm{f}}$ 对应的样本时，其得分函数可近似为

$$s_{\theta}(x_t | c_{\mathrm{f}}) = s_{\theta}(x_t) + \sum_{i \in \{1, 2, \ldots, M\}} \left( s_{\theta}(x_t | c_{\mathrm{g}}^i) - s_{\theta}(x_t) \right)$$

其中 $s_{\theta}(x_t)$ 为无条件得分，$c_{\mathrm{g}}^i$ 为第 $i$ 个一般提示。该形式与CFG $s_{\theta}(x_t) + \omega(s_{\theta}(x_t|c) - s_{\theta}(x_t))$ 在 $\omega \approx M$ 时相似，因此向更具体提示泛化相对容易，且具备零样本组合生成能力（Figure 1c）。

**因果机制总结**：提示复杂度通过上述OR/AND算子的不对称性影响合成数据效用——增加复杂度（向细粒度方向）缩小了与真实数据的分布差距，但降低了条件多样性和提示一致性；向更简单提示泛化则因缺少条件似然而产生严重分布偏移和模式坍缩。



## 实验与关键发现

### 核心发现：提示复杂度对合成数据效用的三重影响

本文通过构建一个系统性的提示复杂度评估框架，在CC12M、ImageNet-1k和DCI三个数据集上，对Stable Diffusion v1.5（LDMv1.5）和Stable Diffusion v3.5 Large（LDMv3.5L）两个代际模型进行了全面评估。实验揭示了提示复杂度对合成数据效用三个轴——多样性（Diversity）、质量（Quality）和一致性（Consistency）——的差异化影响。

**多样性随复杂度单调下降。** 如图2所示，无论使用基础分类器免引导（CFG）、提示扩展还是高级引导方法，随着提示长度（复杂度）增加，所有模型在CC12M和ImageNet-1k上的Vendi多样性得分均呈现下降趋势。值得注意的是，提示扩展在低复杂度时（如复杂度1）可使多样性超越真实数据——LDMv1.5的Vendi得分从CFG基线的9.23提升至15.07（提升约5.85点，Table 8），而真实数据多样性约为13。然而，当提示长度超过约30词后（DCI数据集），多样性下降趋于平缓，不再随长度增加而持续恶化（Figure 2c）。


![[assets/figures/papers/paper_list_l16_https_openreview_net_forum_id_RBIBMCdw7y/figures/006_Figure_2.jpg]]
*Figure 2: Reference-free diversity metric. Diversity (Vendi) of LDMv1.5 and LDMv3.5L generations with CC12M and ImageNet-1k prompts when using: 1) vanilla guidance (CFG), 2) prompt expansion, and 3) advanced guidance methods, for which transparent markers correspond to different methods and the solid marker is the average over methods. Both advanced guidance methods and prompt expansion lead to improved diversity over the vanilla guidance. Prompt expansion from shorter captions can surpass the real data diversity. We further extend to much longer DCI prompts. Diversity of all models first decreases then plateaus which is not observed within shorter prompt length ranges*

**质量呈现先升后降的非单调趋势。** 在较短提示范围内（CC12M和ImageNet-1k），审美质量相对稳定，提示扩展可带来约+0.2点的质量提升（LDMv3.5L，复杂度4：4.98→5.18，估算，Figure 3a, Table 9）。但当扩展至DCI超长提示时，所有模型的质量呈现先上升后下降的趋势，这一现象在短提示范围内未被观察到（Figure 3c）。高级引导方法（CADS、Interval Guidance、APG）则普遍略微损害审美质量。

**一致性持续下降，模型对过长约束的遵循能力有限。** 图4显示，DSG一致性得分在所有模型和方法下均随提示复杂度增加而下降。提示扩展和高级引导方法进一步加剧了这一趋势：相比CFG基线，一致性下降约0.05-0.1（Figure 4a, Figure 16c）。在DCI数据集上，当提示长度超过约30词时，一致性仍持续下降，说明模型对过长文本约束的遵循能力存在瓶颈。


![[assets/figures/papers/paper_list_l16_https_openreview_net_forum_id_RBIBMCdw7y/figures/012_Figure_4.jpg]]
*Figure 4: Reference-free consistency metric. Consistency (DSG) metrics of LDMv1.5 and LDMv3.5L generations with CC12M and ImageNet-1k prompts when using: 1) vanilla guidance (CFG), 2) prompt expansion, and 3) advanced guidance methods, for which transparent markers correspond to different methods and the solid marker is the average over methods. Both advanced guidance methods and prompt expansion lead to lower consistency scores compared to vanilla guidance. We further extend to much longer DCI prompts. Consistency of all models decreases when the prompt lengths increases, which is the same as in the shorter prompt ranges*

### 合成数据分布保真度的权衡

参考基础指标（FDD、精度、密度、覆盖率）揭示了合成数据分布与真实数据分布之间的结构性偏离。如图5所示，增加提示复杂度可提升精度、密度和覆盖率，即合成数据更贴近真实数据的支撑集。然而，提示扩展和高级引导方法虽然改善了FDD（分布距离），却以牺牲精度和密度为代价——这意味着生成样本偏离了真实数据的高密度区域，进入了分布的低概率区域。


![[assets/figures/papers/paper_list_l16_https_openreview_net_forum_id_RBIBMCdw7y/figures/017_Figure_5.jpg]]
*Figure 5: Reference-based utility metrics of synthetic data using CC12M prompts. FDD, precision, density and coverage for LDMv1.5 and LDMv3.5L generations with: (1) vanilla guidance (CFG), (2) prompt expansion, and (3) advanced guidance methods, for which transparent markers correspond to different methods and the solid marker is the average over methods. Both advanced guidance methods and prompt expansion lead to better FDD. Although prompt expansion improves coverage and advanced guidance methods match coverage for LDMv3.5, they both sacrifice precision and density. LDMv1.5 has thus better overall performance (lower FDD) than LDMv3.5L. (a) Diversity*

这一现象与第2节合成高斯混合实验的结论一致：当模型用细粒度提示训练并尝试生成一般提示（如“猫”）且CFG尺度>1时，生成样本严重偏向分布均值并落入低密度区域，导致KL散度高达23.78、FD为14.41，多样性极低（Figure 1b）。该实验从理论上证明，扩散模型无法学习条件似然$p_\theta(x_t | c_{\mathbf{f}}^i)$，导致向更一般提示泛化时产生严重的分布偏移和模式坍缩。

### 干预方法的效用权衡与最佳组合

在所有高级引导方法中，APG对提示一致性的负面影响最小，而CADS和Interval因更激进地移除条件信息导致一致性下降更多（Figure 16c）。消融实验表明，将提示扩展与APG组合可获得最佳的多样性-质量-一致性权衡：多样性进一步提升，同时质量和一致性与CFG基线相当，FDD表现也具竞争力（Figure 6, Section 4.4）。这验证了“组合高级引导与提示扩展可获得最佳多样性-保真度权衡”的核心洞察。


![[assets/figures/papers/paper_list_l16_https_openreview_net_forum_id_RBIBMCdw7y/figures/020_Figure_6.jpg]]
*Figure 6: Effect of combining prompt expansion and guidance methods on the utility of synthetic data from LDMv3.5L using CC12M prompts. This can further boost the diversity of synthetic images, with comparable quality, consistency, and FDD (expecially with APG)*

### 模型代际差异与引导尺度效应

不同LDM模型在效用轴上存在显著差异（Figure 14, Figure 15）：LDMv3.5L的审美质量最佳但多样性最低，而LDMv1.5的FDD最佳但一致性最差。这反映了模型代际更新在效用轴上的取舍——更新近的模型倾向于牺牲多样性以换取更高的质量和一致性。

关于引导尺度的消融实验（Figure 17）揭示了有趣的反常现象：多样性通常随CFG引导尺度升高而下降（LDMv1.5），但LDMv3.5L在尺度为9.0时多样性出现回升。推测这由过饱和导致DINOv2特征对颜色敏感所致，需进一步验证（置信度0.9）。

### 人工评估验证

人工评估结果（Table 6）与自动指标Vendi得分方向一致：人类判断的多样性胜率与Vendi得分差异呈正相关，验证了自动评估指标的可靠性。

### 失败模式与局限性

1. **长提示泛化瓶颈**：当提示超过约30词时，多样性下降趋于平缓但一致性持续恶化，表明模型对超长约束的遵循能力有限，且DCI数据集规模较小（7805对）可能不足以充分评估超长提示行为。
2. **分布保真度与多样性的固有冲突**：提升多样性的干预方法（提示扩展、高级引导）必然导致精度和密度下降，生成样本偏离真实数据支撑集。
3. **提示扩展的社会偏见风险**：提示扩展使用的LLM先验可能内嵌社会偏见（如性别、种族），在扩展“医生”或“CEO”等提示时可能放大刻板印象；当用户本意是寻求通用表达时，强制性具体化可能违背用户意图。
4. **模型覆盖范围有限**：实验仅限于开源T2I模型（LDM系列、Flux、Infinity），未涵盖闭源模型如DALL-E 3，结论的泛化性需要进一步验证。

### 补充图表

![[assets/figures/papers/paper_list_l16_https_openreview_net_forum_id_RBIBMCdw7y/figures/021_Table_1.jpg]]
*Table 1: Statistics on word lengths of different prompt complexities*




## 定位与知识库关联

### 1. 核心问题的理论刻画

本工作将T2I模型向不同复杂度提示泛化的困难，形式化为扩散模型得分函数的“OR算子”与“AND算子”问题。

- **向更一般提示泛化（OR算子）**：一般提示 $c_{\mathbf{g}}$ 的得分函数可分解为细粒度提示得分的加权和，但其权重 $p_{\theta}(x_t | c_{\mathbf{f}}^i)$（即条件似然）并未被扩散模型学习（Equation 1）。因此，当使用CFG且引导尺度 $\omega > 1$ 时，生成样本会严重偏向分布均值，落入低密度区域，导致模式坍缩和分布偏移。合成高斯混合实验定量地验证了这一点：用细粒度提示训练的模型生成“猫”时，KL散度高达23.78，FD为14.41，多样性极低（Figure 1b）。

- **向更细粒度提示泛化（AND算子）**：细粒度提示 $c_{\mathrm{f}}$ 的得分函数可近似为无条件得分与各一般提示得分差之和（Equation 2），其形式与CFG在 $\omega \approx M$ 时相似。这使得模型能够零样本组合多个一般概念来生成细粒度样本，泛化相对容易（Figure 1c）。

这一理论框架揭示了扩散模型在条件生成中的根本性瓶颈：模型学习的是条件得分函数而非条件似然，导致向更宽泛条件泛化时缺乏正确的加权机制。

### 2. 与现有引导方法的关系

本工作系统性地评估了四类推理干预方法在提示复杂度变化下的行为，并将其置于统一的效用评估框架中：

- **Classifier-Free Guidance (CFG)**（Ho & Salimans, 2022）：作为基础基线，CFG通过混合条件与无条件得分来增强条件一致性。本工作表明，CFG在 $\omega > 1$ 时加剧了向一般提示泛化的困难，多样性随引导尺度升高而下降（Figure 17）。

- **Prompt Expansion**（Datta et al., 2024）：通过预训练语言模型将短提示扩展为更详细的描述。该方法在低复杂度时可显著提升多样性，甚至超越真实数据多样性，但以牺牲提示一致性为代价（Figure 2, Figure 4）。

- **高级引导方法**：
  - **CADS**（Sadat et al., 2024）：通过退火条件信号提升多样性，但更激进地移除条件信息导致一致性下降更多（Figure 16c）。
  - **Interval Guidance**（Kynkaanniemi et al., 2024）：仅在特定噪声区间施加条件引导，但在长提示下审美质量和一致性均受损（Section 4.4）。
  - **APG**（Sadat et al., 2025）：通过投影减少过饱和，在所有高级引导方法中对一致性的负面影响最小，且与提示扩展组合可获得最佳的多样性-保真度权衡（Figure 6, Figure 16c）。

### 3. 方法定位与适用边界

本工作提出的**提示复杂度评估框架**并非一种新的生成方法，而是一个系统性的诊断工具，其核心贡献在于：

- **评估维度**：在质量、多样性、一致性三个效用轴上，同时使用参考免指标（Vendi、审美评分、DSG）和参考基础指标（FDD、精度、密度、覆盖率），揭示不同干预方法之间的权衡关系。

- **数据集构建**：通过Captioning → Pairing → Alignment → Sampling → Generation五步流程，在CC12M、ImageNet-1k和DCI数据集上构建了不同复杂度的提示-图像配对，使得跨复杂度评估成为可能。

- **适用边界**：
  - 框架依赖已有图像-文本数据集的质量和规模，其结论的泛化性受限于数据集覆盖范围。
  - DCI数据集规模较小（7805对），对于超长提示的泛化行为研究可能不够充分。
  - 实验仅限于开源T2I模型（LDMv1.5、LDMv3.5L、Flux、Infinity），未涵盖闭源模型（如DALL-E 3），结论可能不适用于所有模型架构。

### 4. 关键发现与权衡机制

- **复杂度-效用权衡**：增加提示复杂度会降低条件多样性并削弱提示一致性，但有助于缩小合成数据与真实数据之间的分布差距（提高精度、密度和覆盖率，Figure 5）。当提示长度超过约30词时，多样性下降趋于平缓，而一致性持续下降（Figure 2c, Figure 4c）。

- **干预方法的权衡**：提示扩展和高级引导在提升多样性的同时，会降低精确度和密度，表明生成样本偏离了真实数据支撑集（Figure 5）。组合APG与提示扩展可在维持可比质量和FDD的前提下最大化多样性（Figure 6）。

- **模型代际差异**：LDMv3.5L的审美质量最佳但多样性最低，而LDMv1.5的FDD最佳但一致性最差（Figure 14, Figure 15），说明模型架构选择对效用轴存在显著影响。

### 5. 局限性与开放问题

**已知局限**：
- 提示扩展使用的LLM先验可能内嵌社会偏见（如性别、种族），在扩展“医生”或“CEO”等提示时可能放大刻板印象。
- 当用户本意是寻求通用或图标式表达时，提示扩展的强制性具体化可能违背用户意图。
- 自动评估指标（Vendi、DSG、审美评分）虽经人工验证，但其偏差和局限性仍需进一步检验。

**开放问题**：
- 如何为长提示构建大规模、高多样性的图像-提示配对数据集，以突破当前评估的瓶颈？
- 是否能在扩散模型中引入对条件似然的近似，从而改善向更一般提示的泛化？
- 不同的文本编码器（如CLIP vs. T5）如何影响提示复杂度的泛化行为？
- 在实际下游任务（如医学图像合成）中，如何在不牺牲安全性和公平性的前提下利用高级引导和提示扩展带来的多样性提升？



## 原文 PDF

![[paperPDFs/ICLR_2026/The_Intricate_Dance_of_Prompt_Complexity_Quality_Diversity_and_Consistency_in_T2I_Models.pdf]]
