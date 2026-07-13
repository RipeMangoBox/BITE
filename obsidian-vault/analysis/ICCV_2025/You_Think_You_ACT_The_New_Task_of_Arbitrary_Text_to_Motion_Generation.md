---
title: "You Think, You ACT: The New Task of Arbitrary Text to Motion Generation"
type: paper
paper_level: A
venue: ICCV
year: 2025
pdf_ref: paperPDFs/ICCV_2025/You_Think_You_ACT_The_New_Task_of_Arbitrary_Text_to_Motion_Generation.pdf
project_link: null
code_link: null
aliases:
- TAFATT
- YTYANTATMG
tags:
- ICCV_2025
- topic/motion_animation
- topic/motion_animation/human_motion_generation
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 通过LLM将场景文本转换为多个可能的动作指令（思考阶段），再将动作指令输入自回归Transformer生成离散动作（行动阶段），从而解耦场景理解与动作生成，使模型能处理多解输入。
primary_logic: 场景到动作生成可被建模为一个多解问题：LLM首先从场景语境中推理出多个合理的动作序列，再由基于VQ-VAE离散动作表示的Transformer网络确定性地执行这些动作，克服了传统单解对齐的局限性。
claims:
- 现有评估指标在场景文本任务上对真值动作的误判率近40%，表明单解指标已失效。
- TAAT在场景文本到动作任务上取得最佳Hit Accuracy (79.9) 和Mean Hit Distance (1.075)，显著优于所有基线模型。
- TAAT在零样本场景中取得最佳FID (0.488)，表明其泛化能力。
- TAAT在动作文本任务上也保持竞争力，FID为0.461，并具备优越的多动作序列生成能力。
---

# You Think, You ACT: The New Task of Arbitrary Text to Motion Generation

> [!tip] 核心洞察
> 场景到动作生成可被建模为一个多解问题：LLM首先从场景语境中推理出多个合理的动作序列，再由基于VQ-VAE离散动作表示的Transformer网络确定性地执行这些动作，克服了传统单解对齐的局限性。

| 字段      | 内容                                                                                                                                                                                                                 |
| ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 中文题名    | 思考即行动：任意文本到动作生成的新任务                                                                                                                                                                                                |
| 英文题名    | You Think, You ACT: The New Task of Arbitrary Text to Motion Generation                                                                                                                                            |
| 会议/期刊   | ICCV 2025                                                                                                                                                                                                          |
| Links   | [paper](https://arxiv.org/abs/2404.14745)                                                                                                                                                                          |
| Topic   | #topic/motion_animation #topic/motion_animation/human_motion_generation #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method  | Think and Act framework for Arbitrary Text (TAAT)                                                                                                                                                                  |
| Dataset | HUMANML3D++ Scene Text to Motion, HUMANML3D++ Action Texts to Motion                                                                                                                                               |

> [!tip] 效果简介
> - HUMANML3D++ Scene Text to Motion 上，Hit Accuracy ↑ 79.9 (TAAT Trained) vs best baseline: see Table 3 (significantly outperforms all baselines)；Mean Hit Distance ↓ 1.075 (TAAT Trained) vs best baseline: see Table 3 (lowest among all baselines)。
> - HUMANML3D++ Scene Text to Motion (Zero-shot) 上，FID ↓ 0.488 (TAAT Zero-shot) vs best baseline: see Table 3 (best FID, demonstrates superior zero-shot capability)。
> - HUMANML3D++ Action Texts to Motion 上，FID ↓ 0.461 (TAAT Trained) vs best baseline: see Table 4 (competitive FID, and best multi-action generation quality)。

## 概要

**问题瓶颈。** 现有文本到动作（Text-to-Motion, T2M）方法——包括扩散模型 **MDM**（Tevet et al., arXiv 2022）、**MoDiffuse**（Zhang et al., arXiv 2022）、**MLD**（Chen et al., CVPR 2023），自回归模型 **T2M-GPT**（Zhang et al., CVPR 2023），以及掩码建模方法 **Momask**（Guo et al., CVPR 2024）——均依赖包含显式动作标签的“动作文本”作为输入。当面对不包含直接动作指令的任意场景文本（如“日落时分，一个人站在山顶”）时，这些方法缺乏场景理解能力，且其单解生成范式无法应对场景文本天然具备的多解性。

**核心洞察与因果机制。** 本文的核心主张是将场景文本到动作生成建模为多解问题：首先由大语言模型（LLM）从场景语境中推理出多个合理的动作序列（Think 阶段），再由基于 VQ-VAE 离散动作表示的自回归 Transformer 逐段执行这些动作指令（Act 阶段）。这一“思考-行动”解耦设计使得模型能够从模糊的语义描述中产生多样且语境合理的运动响应，克服了传统单解对齐的局限。

**方法定位。** 提出的 **TAAT**（Think and Act framework for Arbitrary Text）在方法谱系上位于 LLM 驱动的语义理解与离散动作生成模型的交汇处。与直接将文本映射到连续动作空间的扩散或自回归方案不同，TAAT 引入了一个显式的语义推理层，将场景理解与动作执行分离。同时，为适配多解输出，TAAT 引入了新的评估指标 Hit Accuracy 和 Mean Hit Distance，替代传统单解度量（如 R-Precision、MM-Dist）——实验表明，后者在场景文本任务上对真值动作的误判率接近 40%。

**主要结果。** 在 HUMANML3D++ 数据集的场景文本到动作任务上，TAAT 取得最佳 Hit Accuracy（79.9）和最低 Mean Hit Distance（1.075），显著优于所有基线模型。在零样本场景中，TAAT 取得最佳 FID（0.488），展现出较强的泛化能力。在传统动作文本任务上，TAAT 亦保持竞争力（FID 0.461），并在多动作序列生成中表现出优越的时序完整性和顺序正确性。

**局限与开放问题。** TAAT 的 Think 阶段依赖 LLM，可能产生不准确的动作指令；数据集由 LLM 生成，虽经人工检验（准确率 > 95%），仍可能存在与真实人类描述风格不一致的偏差。多解评估指标依赖距离阈值的选择。未来方向包括将框架扩展到包含物体交互或多人交互的场景，以及探索以更轻量模型替代 LLM 以适应实时应用。

### 问题定义：从动作文本到任意文本的范式跃迁

文本驱动的人体动作生成旨在根据自然语言描述合成逼真的三维人体运动序列。该领域经历了从**动作标签到动作**（Action Label to Motion）到**动作文本到动作**（Action Text to Motion）的演进。动作标签仅提供离散的动作类别，而动作文本则包含显式的动作指令（如“一个人向前走然后坐下”），为生成提供了更丰富的语义约束。

然而，现实应用中大量的文本输入并不包含直接的动作指令，而是描述**场景、事件或情境**的任意文本（Arbitrary Text），例如“日落时分，站在山顶远眺”。这类**场景文本**（Scene Text）要求模型首先理解语境，再推理出合理的反应动作——这本质上是一个**多解问题**：同一场景可以对应多种合理的动作响应（如远眺时可以“指向日落”、“拿出相机拍照”或“双手叉腰深呼吸”）。现有方法直接建立“文本-动作”的单解映射，无法处理这种一对多的生成需求，构成了当前技术的关键瓶颈。

### 现有方法的局限性

当前主流的文本到动作生成方法可归纳为三类范式：

- **扩散模型**：如 **MDM**（Tevet et al., arXiv 2022）、**MoDiffuse**（Zhang et al., arXiv 2022）、**MLD**（Chen et al., CVPR 2023），通过迭代去噪在连续动作空间生成运动序列。
- **自回归Transformer**：如 **T2M-GPT**（Zhang et al., CVPR 2023），将动作量化为离散令牌后逐令牌预测。
- **掩码建模与双向生成**：如 **Momask**（Guo et al., CVPR 2024）、**TM2T**（Guo et al., ECCV 2022），利用掩码重建或双向编解码实现动作生成。

这些方法的共同缺陷在于**输入处理环节**：它们假设输入文本包含明确、单一的动作语义，直接将文本嵌入映射到动作空间。当面对不含动作指令的场景文本时，模型缺乏从语境中推理出合理动作的认知能力，导致生成的动作与场景脱节或完全失效。此外，现有评估指标（如R-Precision、MM-Dist）基于“生成动作与单一真值动作的匹配度”设计，在场景文本任务上对真值动作的误判率接近40%（见Table 2），进一步印证了单解范式的根本局限。

### 本文动机与核心思路

针对上述问题，本文提出**思考即行动（Think and Act for Arbitrary Text, TAAT）**框架，核心洞察是：**场景到动作的生成应被建模为“场景理解→多动作推理→动作执行”的解耦过程**。具体而言：

1. **思考阶段（Think）**：利用大语言模型（LLM）的认知能力，从场景文本中推理出多个合理的动作指令序列，将多解问题显式化。
2. **行动阶段（Act）**：基于VQ-VAE离散动作表示和自回归Transformer，将每条动作指令确定性地转化为运动序列，并通过前一动作段的尾部索引实现段间语义衔接。

这一设计将“场景理解”与“动作生成”解耦，使模型既能利用LLM的零样本推理能力处理任意文本，又能通过离散动作空间的确定性生成保证动作质量。为支撑该任务，本文还构建了首个同时包含动作文本和场景文本的**双文本数据集HUMANML3D++**，并引入了**Hit Accuracy**和**Mean Hit Distance**两项多解评估指标，以替代失效的单解度量。

## 核心方法与创新机理

TAAT的核心创新在于将任意文本到动作生成重新建模为一个“思考-行动”双阶段多解问题，从而突破现有方法对显式动作标签的依赖。

### 问题重定义：从单解对齐到多解推理

现有文本到动作（T2M）方法——包括扩散模型基线**MDM**（Tevet et al., arXiv 2022）、**MoDiffuse**（Zhang et al., arXiv 2022）、**MLD**（Chen et al., CVPR 2023），自回归基线**T2M-GPT**（Zhang et al., CVPR 2023），以及掩码建模基线**Momask**（Guo et al., CVPR 2024）——均假设输入文本包含明确的动作指令（Action Text），生成唯一对应的动作序列。然而，当输入为不包含直接动作标签的场景文本（Scene Text，如“日落时分站在山顶”）时，该假设失效：同一场景可对应多种合理动作（指向日落、拍照、感叹等），单解对齐无法捕捉这种多解性。

TAAT的关键洞察是：**场景到动作的映射本质上是一个多解问题**。场景文本首先需要被“理解”以推理出多个可能的动作响应，然后再由动作生成器“执行”这些响应。这一“思考-行动”解耦使模型能够处理任意文本输入，而非局限于动作标签。

### 核心架构创新：Think-Act 双阶段框架

TAAT由两个功能互补的模块构成，分别对应场景理解与动作生成：

**Think阶段（LLM场景解析）**：采用经LoRA微调的LLaMA模型，将场景文本 $c$ 转换为一组可能的动作指令集合 $A = \theta_{\mathrm{LLM}}(c, P) = (a_1, a_2, \ldots, a_x)$。该阶段利用LLM的因果推理与零样本泛化能力，从场景语境中提取多个合理的动作序列，而非单一输出。微调损失为交叉熵：

$$\mathcal{L}_{\mathrm{token}} = \mathrm{CE}(\mathcal{A}, \mathcal{A}^{\mathrm{gt}}) = -\sum_{i=1}^{n} \mathcal{A}_{i}^{\mathrm{gt}} \log(\mathcal{A}_{i})$$

**Act阶段（VQ-VAE + 自回归Transformer）**：动作生成采用离散化表示——通过VQ-VAE将连续动作编码为码本索引，量化过程为 $\hat{z}_i = \arg\min_{c_k \in C} \|z_i - c_k\|_2$。随后由18层Transformer（隐藏维度1024，16个注意力头）自回归预测下一索引，训练损失为：

$$\mathcal{L}_{\mathrm{trans}} = \mathbb{E}_{\mathbf{I} \sim p(\mathbf{I})} [-\log p(\mathbf{I} \mid \theta_{\mathrm{LLM}}(c))]$$

关键在于**分段拼接生成策略**：对Think阶段输出的动作指令集合 $(a_1, a_2, \ldots, a_x)$，逐段生成对应的索引序列，并将前一动作的最后 $n$ 个索引作为语义连接输入下一段：

$$\mathbf{I}_x = \begin{cases} f(\{a_x, \mathrm{null}\}) & \text{if } x=1, \\ f(\{a_x, \mathbf{I}_{x-1}[-n:]\}) & \text{if } x>1, \end{cases}$$

这一设计确保多动作序列间的平滑过渡，同时保持各动作的独立性。

### 评估体系创新：多解度量

传统指标（R-Precision、MM-Dist）对场景文本任务的失效是TAAT的立论基础之一。真值动作在场景文本上的R-Precision仅为0.665（动作文本为0.797），误判率接近40%（Table 2），表明单解度量无法评估多解生成质量。

TAAT引入两项新指标：
- **Hit Accuracy (HA)**：$\mathrm{Hit Accuracy} = \frac{1}{M} \sum_{i=1}^{M} \max_{j=1,\dots,N} \delta(R_i^{(j)}, G_i)$，衡量至少有一个生成响应命中的样本比例。
- **Mean Hit Distance (MHD)**：计算所有命中响应的平均特征距离，无命中时使用全局最小距离。

### 与基线的关键差异总结

| 维度 | 基线方法 | TAAT |
|------|---------|------|
| 输入处理 | 直接将单一动作文本输入生成器 | LLM从任意文本提取多组动作指令（Think） |
| 动作表示 | 连续空间或序列令牌，单步/扩散生成 | VQ-VAE离散编码，自回归预测，分段拼接 |
| 评估指标 | R-Precision、MM-Dist等单解度量 | Hit Accuracy、Mean Hit Distance多解度量 |
| 适用场景 | 仅动作文本 | 动作文本 + 场景文本（任意文本） |

### 需人工验证的细节

- LLM在Think阶段的具体推理机制（如是否使用了思维链）在现有材料中未详细说明，建议查阅原文Section 4.1获取完整提示策略。
- 分段拼接策略中语义连接长度 $n$ 的最优值（Figure 8显示为7）的具体选取实验细节需确认。

TAAT 遵循“思考—行动”两阶段流水线，将任意文本到动作生成建模为一个多解问题。流水线由三个核心模块串联构成：Think Model（LLM 场景解析器）、Act Model（VQ‑VAE 编码器 + 自回归 Transformer 生成器）以及 Multi‑Solution Evaluator（多解评估器）。整体输入为不含显式动作标签的任意场景文本，输出为一组合理的动作序列。

**输入输出流**：给定一个场景文本 $c$，Think Model 首先利用微调后的大语言模型将其映射为一组可能的动作指令集合 $A = \theta_{\mathrm{LLM}}(c, P) = (a_1, a_2, \ldots, a_x)$。随后，Act Model 对每个动作指令 $a_x$ 独立生成离散动作令牌序列 $\mathbf{I}_x$，并通过前一动作的最后 $n$ 个令牌作为语义连接，按公式

$$
\mathbf{I}_x = \begin{cases}
f(\{a_x, \mathrm{null}\}) & \text{if } x=1, \\
f(\{a_x, \mathbf{I}_{x-1}[-n:]\}) & \text{if } x>1,
\end{cases}
$$

逐段生成并拼接，最终解码为连续动作。Multi‑Solution Evaluator 则基于新引入的 Hit Accuracy 和 Mean Hit Distance 指标，衡量生成的多组动作对真值的覆盖程度与距离。

**模块关系与设计意图**：Think 阶段将场景理解与动作生成解耦，利用 LLM 的推理能力从语境中提取多组合理的动作假设，克服传统单解对齐的局限性。Act 阶段采用 VQ‑VAE 将动作离散化为码本索引，再通过自回归 Transformer 确定性地执行这些假设，从而在保持生成质量的同时实现对多解输入的覆盖。两阶段之间仅通过动作指令文本传递信息，结构清晰且易于扩展。

> **注意**：Think Model 的具体微调策略（LLaMA + LoRA）和 Act Model 的网络配置（18 层 Transformer，隐藏维度 1024，16 注意力头）详见实现细节部分。

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2404_14745/figures/004_Figure_3.jpg]]
*Figure 3: Pipeline overview. (Dataset) We extend HUMANML3D [9] to the novel HUMANML3D++ with Scene Texts. (TAAT) We utilize a fine-tuned LLM to generate multiple reasonable response action instructions for a single Scene Text. And we generate each action in an action instruction individually and utilize the code generated in the previous stage to guide the generation in the subsequent stage. (Evaluation) We introduce two new metrics, Hit Accuracy and Mean Hit Distance, to measure this multi-solution task*

TAAT框架由两个核心模块构成：**Think Model（思考模型）** 负责场景文本解析与动作指令提取，**Act Model（行动模型）** 负责离散动作编码与自回归动作生成。二者通过动作指令序列实现解耦：LLM先“思考”出多组可能的动作描述，再由Transformer“执行”这些描述。

### Think Model：场景文本到动作指令

Think Model采用微调的大语言模型，将任意场景文本 $c$ 映射为一组动作指令集合：

$$A = \theta_{\mathrm{LLM}}(c, P) = (a_1, a_2, \ldots, a_x)$$

其中 $P$ 为因果上下文引导提示，$x$ 为提取的动作指令数量。微调数据集 $\mathcal{D} = \{ (Q_i, A_i) \}_{i=1}^{N}$ 由场景文本 $Q$ 和对应动作文本真值 $A$ 配对组成。微调损失函数为：

$$\mathcal{L}_{\mathrm{LLM}} = \sum_{(Q,A) \in \mathcal{D}} \mathbb{E}_{Q} [\log p(A \mid \theta_{\mathrm{LLM}}(Q))]$$

实际训练中使用交叉熵损失约束预测的动作令牌分布：

$$\mathcal{L}_{\mathrm{token}} = \mathrm{CE}(\mathcal{A}, \mathcal{A}^{\mathrm{gt}}) = -\sum_{i=1}^{n} \mathcal{A}_{i}^{\mathrm{gt}} \log(\mathcal{A}_{i})$$

### Act Model：离散动作编码与自回归生成

Act Model由VQ-VAE编码器和自回归Transformer组成。VQ-VAE将连续动作序列离散化为码本索引，量化过程为：

$$\hat{z}_i = \arg\min_{c_k \in C} \|z_i - c_k\|_2$$

即将潜在特征 $z_i$ 映射到码本 $C$ 中最近邻向量 $c_k$。Transformer以自回归方式预测下一个索引，训练目标为最大化给定动作指令 $c$ 下索引序列 $\mathbf{I}$ 的对数似然：

$$\mathcal{L}_{\mathrm{trans}} = \mathbb{E}_{\mathbf{I} \sim p(\mathbf{I})} [-\log p(\mathbf{I} \mid \theta_{\mathrm{LLM}}(c))]$$

### 分段生成与语义拼接

对于Think Model输出的多动作指令序列 $(a_1, a_2, \ldots, a_x)$，Act Model逐段生成并拼接。第 $x$ 段的索引序列 $\mathbf{I}_x$ 生成方式为：

$$\mathbf{I}_x = \begin{cases} f(\{a_x, \mathrm{null}\}) & \text{if } x=1, \\ f(\{a_x, \mathbf{I}_{x-1}[-n:]\}) & \text{if } x>1, \end{cases}$$

其中 $f$ 为自回归生成函数，$\mathbf{I}_{x-1}[-n:]$ 表示前一动作生成的最后 $n$ 个索引。这一设计使相邻动作段之间保持语义连续性，避免了动作切换时的突兀断裂。消融实验表明，最优索引长度 $n=7$ 时生成质量最高；过短会导致动作不连续，过长则引入重复和额外计算开销。

### 多解评估指标

为适配场景文本的多解特性，TAAT引入两个新指标。命中指示函数定义为：

$$\delta_{ij} = \begin{cases} 1, & \text{if } \mathrm{dist}(R_i^{(j)}, G_i) \leq \theta, \\ 0, & \text{otherwise.} \end{cases}$$

即生成响应 $R_i^{(j)}$ 与真值 $G_i$ 的距离小于阈值 $\theta$ 时视为命中。**Hit Accuracy (HA)** 衡量至少有一个生成响应命中的样本比例：

$$\mathrm{Hit\ Accuracy} = \frac{1}{M} \sum_{i=1}^{M} \max_{j=1,\dots,N} \delta(R_i^{(j)}, G_i)$$

**Mean Hit Distance (MHD)** 计算所有命中响应的平均距离，若无命中则使用全局最小距离：

$$\mathrm{MHD} = \frac{\sum_{i=1}^{M} \sum_{j=1}^{N} \delta_{ij} \cdot d_{ij} + \sum_{i=1}^{M} \left( \mathbb{I}(\sum_{j=1}^{N} \delta_{ij} = 0) \cdot \min d_{ij} \right)}{\sum_{i=1}^{M} \sum_{j=1}^{N} \delta_{ij} + \sum_{i=1}^{M} \mathbb{I}(\sum_{j=1}^{N} \delta_{ij} = 0)}$$

这两个指标直接回应了现有单解度量（如R-Precision）在场景文本任务上的失效问题——真值动作的R-Precision从动作文本的0.797骤降至0.665，误判率近40%，表明传统指标无法公平评估多解生成质量。

## 实验与关键发现

### 核心瓶颈验证：现有指标在场景文本任务上的失效

在分析模型性能之前，必须先审视评估体系本身的有效性。Table 2 揭示了关键问题：在动作文本（Action Texts）任务上，真值（GT）动作的 R-Precision 为 0.797，而在场景文本（Scene Texts）任务上骤降至 0.665；MM-Dist 则从 2.974 恶化至 3.945。这意味着现有单解评估指标对场景文本任务的真值动作误判率接近 40%，已无法可靠衡量生成质量。这一发现直接验证了本文的核心瓶颈论断——传统 T2M 范式及其评估体系在任意文本场景下已失效，多解评估势在必行。

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2404_14745/figures/006_Table_2.jpg]]
*Table 2: Comparison of metrics for GT motion in two tasks reveals poor accuracy, highlighting the failure of current metric reliability*

### 主实验结果：场景文本到动作生成

Table 3 汇总了零样本与训练后场景文本到动作任务的核心结果。

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2404_14745/figures/007_Table_3.jpg]]
*Table 3: Experiment Results on Model Zero-Shot Ability and Scene Text to Motion. Our model demonstrates optimal performance with new scene texts in Zero-Shot experiment. After being trained on HUMANML3D++ (Trained row), models show improved results on scene texts. Our TAAT excels in both Hit Accuracy and Mean Hit Distance, indicating a superior understanding of scene texts. Furthermore, the achieved FID and Diversity metrics suggest that we can generate high-quality motions that align well with real-world motions*

**零样本泛化能力**：TAAT 在零样本设置下取得最佳 FID（0.488），显著优于所有基线模型。这表明 TAAT 的 Think 阶段（LLM 场景解析）赋予了模型对未见场景文本的理解能力，而纯动作生成模型（如 **MDM**（Tevet et al., arXiv 2022）、**T2M-GPT**（Zhang et al., CVPR 2023））因缺乏场景语义解析模块，零样本泛化能力明显受限。

**训练后性能**：在 HUMANML3D++ 上训练后，TAAT 取得最佳 Hit Accuracy（79.9）和最佳 Mean Hit Distance（1.075），在所有模型中遥遥领先。这一结果直接验证了“Think + Act”双阶段架构的有效性：LLM 将场景文本转化为多组动作指令（Think），再由 VQ-VAE + Transformer 逐段生成并拼接动作（Act），使模型能够覆盖场景文本的多解空间。此外，TAAT 在 Diversity 指标上也达到最高，FID 和 MModality 排名第二，表明其生成的动作既多样又接近真实分布。

**定性分析**：Figure 5 直观展示了 TAAT 的优势——对于“日落场景”文本，TAAT 生成了“指向日落”“拍照”等语境合理动作，而其他模型则生成了“低头看”或“静止站立”等无关动作。Figure 6 进一步展示了 TAAT 对同一场景文本生成多种合理动作的多样性能力。

### 动作文本任务上的竞争力验证

Table 4 和 Figure 7 验证了 TAAT 在传统动作文本任务上的表现。TAAT 取得 FID 0.461，与专为动作文本设计的基线模型具有竞争力。更重要的是，在多动作序列生成场景中（Figure 7），只有 TAAT 能够按正确顺序执行全部动作，而 **MDM**、**MLD**（Chen et al., CVPR 2023）存在动作遗漏，**T2M-GPT** 出现顺序错乱，**MLD** 还存在空间关系错误。这得益于 TAAT 的逐段生成与语义拼接机制（公式 (6)），前一动作的最后 n 个索引为后续动作提供了语义连接。

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2404_14745/figures/012_Table_4.jpg]]
*Table 4: Experiment on Action Texts to Motion. Our TAAT works well in FID, Diversity, demonstrating that our model can generate realistic and diverse motions that are close to real human motions. Furthermore, TAAT is suitable for multi-action generation in fig 7*

### 鲁棒性分析：跨任务 FID 稳定性

Table 5 分析了各模型在零样本场景文本、训练后场景文本、动作文本三种设置间的 FID 变化。TAAT 的 FID 波动最小，表明其对输入文本类型变化具有较强鲁棒性——无论输入是场景文本还是动作文本，生成质量保持稳定。相比之下，其他模型在输入类型切换时 FID 波动较大，暴露了其对特定文本格式的过拟合。

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2404_14745/figures/014_Table_5.jpg]]
*Table 5: FID variation across three experiments. Our model exhibits minimal variation in FID across different tasks. (A) shows each model’s FID change from Zero-shot to Action Text; (B) from Scene Text to Action Text*

### 消融实验

**数据过滤的影响**：Table 3 显示，应用数据过滤（filter）可提升 Hit Accuracy 并降低 Mean Hit Distance，验证了 HUMANML3D++ 构建流程中后过滤步骤的必要性。

**索引长度选择**：Figure 8 展示了索引长度对生成质量的影响。最优索引长度为 7，此时生成质量最高；过短的索引（如 3）导致动作不连续，过长的索引（如 11）则引起动作重复和额外计算开销。这一消融实验为 Act 阶段的超参数选择提供了经验依据。

**LLM 选择**：Table 6 对比了不同 LLM 生成场景文本的质量，Gemini 在质量与成本间取得最优权衡，最终被选定为数据生成和 Think 阶段的基础模型。需注意，该选择可能引入 Gemini 特有的语言偏好，尽管经过人工交叉验证（准确率 >95%），数据集仍可能存在与真实人类描述风格的偏差。

**提示策略消融**：Table 7 对比了不同提示策略的效果。因果上下文引导策略（Causality）优于仅添加动词限制（w/ Verb）、数量要求（Quantity）或少量示例（Few-shot）的策略，验证了在场景文本生成中引入因果关系描述的重要性。

### 失败模式与局限性

1. **LLM 推理偏差**：Think 阶段依赖 LLM 的场景解析能力，当场景文本高度抽象或反事实时，LLM 可能生成不准确的动作指令，导致 Act 阶段生成的动作与语境不匹配。Figure 5 中虽未展示此类失败案例，但这是该框架的固有风险。

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2404_14745/figures/008_Figure_5.jpg]]
*Figure 5: Visual comparisons on scene texts. Our model generates context-appropriate responses (pointing to the sunset, taking a photo), while other models display irrelevant actions (looking down) or remain inactive (standing still)*

2. **数据集偏差**：HUMANML3D++ 由 LLM 生成，虽经人工校验，其语言风格和动作分布可能与真实人类描述存在系统性差异。零样本实验仅限于 HUMANML3D++，未在完全独立的动作数据集上验证泛化性。

3. **阈值敏感性**：多解评估指标 Hit Accuracy 和 Mean Hit Distance 依赖距离阈值 θ 的选择，阈值设定直接影响命中判定结果。论文未系统分析阈值敏感性，该点需要手动验证。

4. **计算开销**：双阶段架构引入 LLM 推理开销，可能限制实时应用场景。论文未讨论是否可用更轻量的模型替代 LLM 进行场景解析。

### 开放问题

1. TAAT 框架能否扩展到包含物体交互或多人交互的更复杂场景文本？
2. 是否可以用更轻量的模型替代 LLM 进行场景解析，以适应实时应用？
3. 多解评估指标 Hit Accuracy 和 Mean Hit Distance 是否可推广到其他生成任务（如图像或音频生成）？
4. 如何进一步提升 TAAT 对高度抽象或反事实场景文本的推理能力？

## 定位与知识库关联

### 任务定义的边界重划

TAAT的核心贡献在于将文本到动作生成的任务空间从“显式动作文本”拓展至“任意场景文本”。传统T2M方法（如 **MDM** (Tevet et al., arXiv 2022)、**T2M-GPT** (Zhang et al., CVPR 2023)、**MLD** (Chen et al., CVPR 2023) 等）的输入文本中必然包含可直接映射的动作标签（如“一个人向前走”），其本质是单解对齐问题。TAAT首次明确定义了Scene Text to Motion任务：输入为不含显式动作指令的场景描述（如“夕阳西下”），模型需从中推理出多个合理的人体反应动作。这一边界重划使得动作生成从确定性映射变为多解推理问题，直接导致了评估体系的范式转换——传统R-Precision在场景文本任务上对真值动作的误判率接近40%（Table 2），已丧失可靠性。

### 与基线方法的结构性差异

TAAT与现有方法的核心差异体现在三个维度：

**输入处理层**。所有基线方法（MDM、T2M-GPT、**MoDiffuse** (Zhang et al., arXiv 2022)、**TM2T** (Guo et al., ECCV 2022)、MLD、**Momask** (Guo et al., CVPR 2024)）均将单一文本直接输入动作生成器，缺乏对文本中动作语义的显式解析。TAAT引入独立的Think阶段，通过微调LLM从场景文本中提取多组动作指令集 $A = \theta_{\mathrm{LLM}}(c, P) = (a_1, a_2, \ldots, a_x)$，实现场景理解与动作生成的解耦。

**动作表示与生成方式**。基线方法多采用连续动作空间上的扩散过程（MDM、MoDiffuse、MLD）或掩码建模（Momask）。TAAT采用VQ-VAE将动作离散化为码本索引序列，并通过自回归Transformer逐索引预测，再根据动作指令序列逐段生成并拼接（Equation 6）。这种离散化表示天然适配多动作序列的逐段控制，使得TAAT在动作文本任务上能够正确按序生成全部动作，而其他模型存在遗漏动作（MDM、MLD）、顺序错乱（T2M-GPT）等问题（Figure 7）。

**评估指标**。传统指标（R-Precision、MM-Dist）假设生成结果与真值一一对应。TAAT引入多解度量Hit Accuracy和Mean Hit Distance，借鉴问答任务中“命中”概念，评估模型是否覆盖参考动作空间。这一指标设计使得多解生成能力可被量化比较。

### 适用边界与局限

TAAT的有效性建立在一系列前提条件之上，偏离这些条件时性能可能显著下降：

**LLM推理可靠性**。Think阶段依赖LLM的场景理解能力，当场景文本高度抽象、反事实或包含复杂物理常识时，LLM可能产生不准确的动作指令，进而导致Act阶段生成的动作不合理。论文未提供LLM推理失败的具体案例和比例。

**数据集偏差**。HUMANML3D++的场景文本由LLM（最终选择Gemini模型，权衡质量与成本）通过因果上下文引导提示生成，虽经人工交叉验证（准确率>95%），仍可能与真实人类描述风格存在系统性偏差。这种偏差可能使TAAT在真实场景文本上表现弱于实验报告值，需人工验证。

**多解评估的阈值敏感性**。Hit Accuracy和Mean Hit Distance均依赖于距离阈值 $\theta$ 的选择（$\delta_{ij}$ 的定义），阈值设定直接影响命中判定。论文未充分讨论阈值的选取依据及其对排名的敏感性。

**零样本泛化范围有限**。零样本实验仅限于HUMANML3D++内部的场景文本划分，未在完全不同的动作数据集（如KIT-ML或其他域外数据）上验证泛化性。TAAT在其他动作风格、骨架结构或文化背景下的表现尚不明确。

**计算开销**。双阶段架构引入LLM推理的额外时延，论文未提供推理速度的定量分析，对实时应用（如交互式虚拟人）的适用性需进一步评估。

### 开放问题

TAAT框架打开了若干值得探索的方向：

1. **复杂交互扩展**：能否将Think-Act框架扩展到包含物体交互或多人协作的场景文本？此时动作指令集需包含交互对象和时序协调信息，对LLM推理和动作生成均提出更高要求。

2. **轻量化场景解析**：是否可以用更轻量的模型（如小型T5或蒸馏后的LLM）替代当前LLM进行场景解析，以降低推理时延适应实时应用？论文在数据生成阶段比较了不同LLM的质量（Table 6），但未在推理阶段进行类似消融。

3. **多解评估的泛化**：Hit Accuracy和Mean Hit Distance的设计思想是否可推广到其他多解生成任务（如图像生成中的多样性评估、音频生成中的风格覆盖）？其阈值选择策略的普适性需要跨任务验证。

4. **反事实与抽象推理**：如何进一步提升TAAT对高度抽象（如“时间流逝的感觉”）或反事实（如“如果重力消失”）场景文本的推理能力？这可能需要引入物理模拟或常识知识库作为Think阶段的辅助信息源。

## 原文 PDF

![[paperPDFs/ICCV_2025/You_Think_You_ACT_The_New_Task_of_Arbitrary_Text_to_Motion_Generation.pdf]]
