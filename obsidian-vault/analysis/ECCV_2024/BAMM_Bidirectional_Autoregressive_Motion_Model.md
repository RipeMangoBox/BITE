---
title: "BAMM: Bidirectional Autoregressive Motion Model"
type: paper
paper_level: A
venue: ECCV
year: 2024
pdf_ref: paperPDFs/ECCV_2024/BAMM_Bidirectional_Autoregressive_Motion_Model.pdf
aliases:
- BAMM
tags:
- ECCV_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 混合注意力掩码策略（同时使用单向和双向因果掩码）
primary_logic: 通过训练时随机应用单向和双向因果掩码，并在推理时采用级联解码（先单向自回归生成长度与粗运动，再双向掩码精炼），统一了生成掩码建模与自回归建模，使模型既能动态预测运动长度，又能利用双向上下文依赖提升生成质量并获得零样本运动编辑能力。
claims:
- BAMM通过混合注意力掩码整合了自回归与掩码生成建模。
- 双向因果掩码使模型能同时关注过去和未来未掩码令牌。
- 级联解码隐式预测运动长度并细化生成质量。
- BAMM零样本支持多种运动编辑任务。
---

# BAMM: Bidirectional Autoregressive Motion Model

> [!tip] 核心洞察
> 通过训练时随机应用单向和双向因果掩码，并在推理时采用级联解码（先单向自回归生成长度与粗运动，再双向掩码精炼），统一了生成掩码建模与自回归建模，使模型既能动态预测运动长度，又能利用双向上下文依赖提升生成质量并获得零样本运动编辑能力。

| 字段 | 内容 |
|------|------|
| 中文题名 | BAMM：双向自回归运动模型 |
| 英文题名 | BAMM: Bidirectional Autoregressive Motion Model |
| 会议/期刊 | ECCV 2024 |
| Links | [paper](https://arxiv.org/abs/2403.19435) · [Project](https://exitudio.github.io/BAMM-page) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | BAMM |
| Dataset | HumanML3D, KIT-ML |

> [!tip] 效果简介
> - HumanML3D 上，FID↓ 0.055±.002 vs 0.045±.002 (MoMask) (+0.010)；Top-1 R-Precision↑ 0.525±.002 vs 0.521±.002 (MoMask) (+0.004)；MM-Dist↓ 2.919±.008 vs 2.926±.007 (MMM) (-0.007)。
> - KIT-ML 上，FID↓ 0.183±.013 vs 0.204±.011 (MoMask§) (-0.021)；Top-1 R-Precision↑ 0.438±.009 vs 0.433±.007 (MoMask§) (+0.005)。

## 概述

### 问题瓶颈

现有文本驱动的人体运动生成方法在三个关键维度上存在严重的权衡困境：**生成质量**、**无需长度先验的可用性**以及**运动编辑能力**。基于去噪的扩散模型（如 **MDM**，Tevet et al., ArXiv 2022）和掩码生成模型（如 **MoMask**、**MMM**，Pinyoanuntapong et al., CVPR 2024）虽然能产出高质量运动，但必须预先指定运动序列长度才能保证效果；而自回归模型（如 **T2M-GPT**，Zhang et al., CVPR 2023）虽可隐式预测运动终点、摆脱长度先验依赖，却因单向因果依赖导致生成质量下降，且难以支持灵活的运动编辑。

### 核心方法

**BAMM**（Bidirectional Autoregressive Motion Model）通过一个关键机制统一了自回归建模与掩码生成建模——**混合注意力掩码策略**。训练时，模型以等概率随机采用单向因果掩码或双向因果掩码，使同一Transformer既能学习从左到右的序列依赖，又能捕获双向上下文信息。推理时则采用**级联解码**：第一轮使用单向自回归解码，隐式预测运动长度并生成粗粒度运动序列；第二轮切换为双向掩码精炼，对低置信度令牌进行掩码重预测，充分利用全局上下文提升生成质量。这一设计使BAMM同时获得了动态长度预测能力、高保真运动生成质量，以及零样本运动编辑能力。

### 方法定位

在方法谱系上，BAMM位于自回归生成模型与掩码生成模型的交叉点。与替换令牌为`[MASK]`的传统掩码方法不同，BAMM直接在注意力矩阵上施加因果掩码，不修改输入令牌本身。其训练目标为单向与双向因果掩码下的混合负对数似然损失（权重λ=0.5），推理时则通过分类器自由指导进一步增强文本-运动对齐。此外，BAMM引入残差向量量化与精炼Transformer，对运动令牌进行多层量化以提升细节表现力。

### 关键结果

在HumanML3D和KIT-ML两个主流基准上，BAMM取得了具有竞争力的生成质量：HumanML3D上FID达到0.055，Top-1 R-Precision达到0.525；KIT-ML上FID为0.183，Top-1 R-Precision为0.438。更重要的是，BAMM在**不依赖外部长度估计器**的前提下实现了这些指标，而依赖预测长度的MMM和MoMask在FID上分别退化至0.080和0.090。此外，BAMM零样本支持运动补全、外推、前后缀预测及长序列合成等多种编辑任务，在生成质量、长度灵活性与编辑能力三者之间实现了此前方法未能达成的统一。

## 背景与动机

### 问题背景：文本驱动的3D人体运动生成

文本驱动的3D人体运动生成旨在根据自然语言描述合成逼真的人体动作序列，在动画制作、虚拟现实、人机交互等领域具有广泛的应用前景。近年来，该领域涌现出大量基于深度生成模型的方法，主要包括三类范式：**扩散模型**（如MDM，Tevet et al., ArXiv 2022）、**掩码生成模型**（如MoMask、MMM，Pinyoanuntapong et al., CVPR 2024）和**自回归模型**（如T2M-GPT，Zhang et al., CVPR 2023）。

### 现有方法的权衡困境

尽管上述方法在生成质量上取得了显著进展，但它们在三个关键能力维度上存在严重的权衡：

1. **运动长度预测 vs. 生成质量**：扩散模型和掩码生成模型通常需要预先指定运动序列的长度才能保证生成质量。当使用预测的长度估计器作为输入时，这些方法的性能会显著下降——例如，MMM在HumanML3D上的FID从使用真实长度时的0.080恶化至使用多类别采样预测长度时的0.099，MoMask则从0.090恶化至0.120（Table 7）。自回归模型虽然能够隐式预测序列终止位置，但其单向依赖结构限制了生成质量的上限。

2. **生成质量 vs. 运动编辑能力**：扩散模型通过迭代去噪过程生成高质量运动，但缺乏原生的编辑接口；自回归模型受限于单向因果注意力，难以利用全局上下文进行运动修复或补全；掩码生成模型虽然天然支持双向上下文建模，但其编辑能力受限于固定的序列长度假设。

3. **可用性 vs. 灵活性**：实际应用中，用户往往无法准确预知所需运动的帧数，而需要模型根据文本语义自动确定运动时长。与此同时，用户也希望模型能接受长度约束以精确控制输出，并支持对已生成运动进行局部编辑（如修复、外推、前后缀预测等）。现有方法难以同时满足这些需求。

### 核心瓶颈与本文动机

上述权衡的根源在于**生成掩码建模与自回归建模之间的范式割裂**。自回归模型以单向因果依赖逐令牌生成序列，天然支持长度预测但缺乏双向上下文建模能力；掩码生成模型以双向注意力并行预测被掩码令牌，能够利用丰富上下文但需要预设序列长度。这两种范式在训练目标和推理策略上的根本差异，使得现有方法不得不在长度预测能力、生成质量和编辑灵活性之间做出取舍。

BAMM的动机正是打破这一范式壁垒：**能否设计一个统一的框架，在训练时同时学习单向和双向的令牌依赖关系，在推理时灵活组合两种解码策略，从而同时获得长度预测、高质量生成和零样本运动编辑三项能力？** 这一思路的核心洞见在于：通过混合注意力掩码策略，使同一个Transformer能够根据不同的因果掩码模式在自回归生成和掩码生成之间无缝切换，进而在推理阶段通过级联解码将两者的优势有机结合。

## 核心创新

BAMM 的核心创新在于**通过混合注意力掩码策略，将自回归生成与掩码生成建模统一到单一 Transformer 框架中**，从而一举解决了现有文本驱动运动生成方法中“生成质量—长度预测—编辑能力”三者不可兼得的根本矛盾。

### 问题诊断：三类方法的固有权衡

现有主流方法各自存在结构性缺陷：

- **扩散模型**（如 **MDM**，Tevet et al., ArXiv 2022）和**掩码生成模型**（如 **MoMask**、**MMM**，Pinyoanuntapong et al., CVPR 2024）需要预设运动长度才能保证生成质量，对长度估计器的精度高度敏感。
- **自回归模型**（如 **T2M-GPT**，Zhang et al., CVPR 2023）虽能隐式预测运动长度，但单向因果依赖限制了模型对全局上下文的感知能力，导致生成质量下降且缺乏编辑能力。

BAMM 的设计目标即打破这一权衡三角，使单一模型同时具备：无需长度先验的自主长度预测能力、高质量运动生成能力，以及零样本运动编辑能力。

### 核心机制：混合注意力掩码

BAMM 的关键技术手段是**混合注意力掩码（hybrid attention mask）**，其核心洞察在于：**训练时随机切换单向与双向因果掩码，推理时级联使用两种掩码模式**，从而将自回归建模（预测下一个 token）与掩码生成建模（基于双向上下文预测被掩码 token）统一到同一参数空间中。

具体而言，BAMM 的掩码自注意力 Transformer 并不像传统掩码生成模型（如 MoMask、MMM）那样用 `[MASK]` token 替换输入，而是**直接修改注意力分数矩阵**：

$$
\text{Attention} = \text{Softmax}\left( \frac{Q K^T}{\sqrt{d_k}} + M \right) \cdot V
$$

其中因果掩码 $M$ 在训练时以概率 $\lambda = 0.5$ 在两种模式间随机切换：

1. **单向因果掩码 $M^{uc}$**：标准自回归掩码，token $i$ 只能关注 $j \leq i$ 的位置，实现从左到右的序列预测。
2. **双向因果掩码 $M^{bc}$**：允许 token $i$ 同时关注过去位置和未来未掩码位置：
   $$M_{ij} = \begin{cases} 0, & \text{where } (i \geq j \wedge i \not\in U) \vee (j \in U) \\ -\infty, & \text{otherwise} \end{cases}$$
   其中 $U$ 为未掩码 token 集合。这使得被掩码位置可以充分利用双向上下文依赖进行预测。

训练目标为混合负对数似然损失：

$$\mathcal{L}_{\mathrm{hybrid}} = - \underset{\mathbf{x} \in p(\mathbf{X})}{\mathbb{E}} \left[ \lambda \sum_{\forall i \in [1,t]} \log p_\theta(x_i \mid M^{uc}) + (1-\lambda) \sum_{\forall i \in [1,t]} \log p_\theta(x_i \mid M^{bc}) \right]$$

实验表明 $\lambda = 0.5$ 取得最优性能（Table 6, confidence=0.95）。

### 推理创新：级联解码

推理阶段，BAMM 采用**双迭代级联解码（cascaded motion decoding）**，将两种掩码模式的优势分阶段释放：

1. **第一轮——单向自回归解码**：使用单向因果掩码，从 `[START]` token 开始自回归生成运动 token 序列，直至模型预测出 `[END]` token，从而**隐式确定运动长度**并生成粗粒度运动序列。
2. **第二轮——双向掩码精炼**：切换到双向因果掩码，识别第一轮生成的低置信度 token 并将其掩码，然后基于双向上下文重新预测这些 token，实现**运动质量的精细化提升**。

消融实验证实，两轮迭代显著优于单轮（FID 从 0.064 降至 0.055），三轮迭代则无显著增益（Table 6, confidence=0.95）。

### 辅助创新：残差运动精炼

为进一步提升运动细节质量，BAMM 引入了**残差向量量化（RVQ）** 机制：将运动序列编码为多层离散 token 序列，第一层（base token）由掩码自注意力 Transformer 通过级联解码生成，随后由一个独立的**精炼 Transformer（refinement transformer）** 基于 base token 预测其余层的残差 token 序列，最终合并解码为高质量运动。精炼 Transformer 与主 Transformer 共享架构但使用全注意力掩码（Figure 4）。

### 编辑能力的来源

BAMM 的零样本运动编辑能力直接源于其双向因果掩码机制：将需要编辑的运动片段对应 token 设为掩码状态，模型即可基于周围上下文 token 和文本描述双向推理生成编辑内容，支持**时间域填充（inpainting）、外推（outpainting）、前缀预测、后缀补全**以及**任意长运动序列合成**等五类编辑任务（Figure 7, Figure 11）。

### 与基线方法的关键差异总结

| 技术槽位 | 基线方法 | BAMM 方案 |
|---------|---------|----------|
| 掩码策略 | 用 `[MASK]` token 替换输入（MoMask, MMM） | 直接修改注意力矩阵，不替换 token |
| 训练目标 | 单一自回归或掩码建模损失 | 混合单向/双向掩码损失，$\lambda=0.5$ |
| 推理方式 | 单次自回归解码或固定长度迭代去噪 | 双迭代级联解码（单向生成长度+粗运动，双向精炼） |
| 残差精炼 | 单层矢量量化 | 残差矢量量化 + 精炼 Transformer |

### 待验证的开放问题

- $\lambda=0.5$ 的最优性在不同数据集和任务上的普适性尚待验证。
- 第二轮精炼中低置信度 token 的鉴别标准和掩码比例的敏感度未作详细消融。
- RVQ 层数和码本大小对生成质量与推理速度的具体权衡关系需要进一步探索。

## 整体框架

BAMM 的整体框架由两个核心组件级联构成，形成“压缩—生成—精炼”的流水线。

**运动分词器（Motion Tokenizer）** 作为流水线的前端，负责将原始 3D 人体运动序列压缩为离散令牌序列。该模块基于 VQ-VAE 架构预训练，通过编码器将运动 $\mathbf{M}$ 映射到隐空间嵌入 $\mathbf{z}$，再经可学习码本量化为离散编码 $\mathbf{c}$。训练目标为矢量量化损失：

$$L_{VQ} = \| \operatorname{sg}(\mathbf{z}) - \mathbf{e} \|_2^2 + \beta \| \mathbf{z} - \operatorname{sg}(\mathbf{e}) \|_2^2$$

其中 $\operatorname{sg}$ 为停止梯度操作，$\beta$ 为承诺损失权重。这一量化过程将连续运动表示转化为离散令牌，为后续的生成式建模提供统一的符号空间。

**条件掩码自注意力 Transformer** 是流水线的核心生成模块，采用标准多层 Transformer 架构。其输入序列由三类令牌拼接而成：运动令牌、来自 CLIP 模型的文本嵌入，以及专门的 `[END]` 令牌。该模块的关键创新在于**不替换输入令牌为 `[MASK]`**，而是通过因果注意力掩码 $M$ 直接调控注意力矩阵：

$$\text{Attention} = \mathrm{Softmax}\left( \frac{Q K^T}{\sqrt{d_k}} + M \right) \cdot V$$

掩码 $M$ 中允许注意力的位置置为 0，否则置为 $-\infty$，从而在 softmax 后强制注意力权重归零。训练时，模型随机应用两种掩码模式：**单向因果掩码**（仅允许关注历史令牌）模拟自回归生成，**双向因果掩码**（允许关注所有未掩码令牌）模拟掩码生成建模。这种混合策略使单一模型同时习得两种生成范式。

**残差运动精炼（Residual Motion Refinement）** 作为流水线的后端，进一步提升生成质量。该模块引入残差向量量化（RVQ），将原始运动编码为多层令牌序列。基础层令牌由前述 Transformer 通过级联解码生成，随后送入一个共享架构的**精炼 Transformer**（使用全注意力掩码），逐层预测残差量化器的令牌序列。最终合并所有层令牌，经分词器解码器还原为完整运动。

**推理时的数据流**采用双迭代级联解码策略（详见后续章节）：第一轮使用单向掩码自回归生成粗运动并隐式预测序列长度，第二轮使用双向掩码对低置信度令牌进行掩码重预测，实现质量精炼。整个流水线从文本描述出发，无需预设运动长度，端到端输出高质量 3D 运动序列。

### 补充图表

![[assets/figures/papers/BAMM_Bidirectional_Autoregressive_Motion_Model_1dd6989b8f26/figures/003_Figure_2.jpg]]
*Figure 2: Overall architecture of BAMM. (a) Motion Tokenizer encodes the raw motion sequence into discrete motion tokens according to a learned codebook. (b) Masked Self-attention Transformer learns to sequentially predict next tokens conditioned on text embedding from CLIP model and future unmasked tokens. Masked self-attention mechanism unifies autoregressive model and generative masked motion via bidirectional and unidirectional causal masks*

## 核心模块与公式推导

BAMM 的生成能力建立在三个紧密协作的核心模块之上：**运动分词器**、**掩码自注意力变换器**和**残差细化变换器**。整个框架通过混合注意力掩码策略统一了自回归与掩码生成建模，并在推理时采用级联解码实现长度预测与质量精炼。

### 运动分词器

运动分词器基于 VQ-VAE 构建，负责将原始 3D 人体运动序列压缩为离散的潜在令牌序列。其训练目标由矢量量化损失驱动：

$$L_{VQ} = \| \operatorname{sg}(\mathbf{z}) - \mathbf{e} \|_2^2 + \beta \| \mathbf{z} - \operatorname{sg}(\mathbf{e}) \|_2^2$$

其中 $\mathbf{z}$ 为编码器输出的连续潜在嵌入，$\mathbf{e}$ 为码本中最近邻的离散码向量，$\operatorname{sg}(\cdot)$ 表示停止梯度操作。第一项将码向量拉向编码器输出，第二项为承诺损失，约束编码器输出靠近所选码向量，$\beta$ 为承诺损失权重。通过该分词器，原始运动序列被量化为离散令牌 $c$，为后续变换器提供紧凑的离散表示空间。

### 掩码自注意力变换器

掩码自注意力变换器是 BAMM 的核心生成模块，采用标准多层变换器架构。输入序列由运动令牌、来自 CLIP 模型的文本嵌入以及 `[END]` 令牌拼接而成。其关键创新在于**不替换输入令牌为 `[MASK]` 令牌**，而是通过因果掩码 $M$ 直接调整注意力分数矩阵：

$$Attention = \mathrm{Softmax}\left( \frac{Q K^T}{\sqrt{d_k}} + M \right) \cdot V$$

掩码 $M$ 中允许注意力的位置赋值为 $0$，禁止注意力的位置赋值为 $-\infty$，在 softmax 后强制对应注意力权重为零。BAMM 在训练时随机使用两种因果掩码：

- **单向因果掩码 $M^{uc}$**：仅允许令牌关注自身及左侧（过去）令牌，实现标准自回归预测。
- **双向因果掩码 $M^{bc}$**：允许令牌同时关注过去令牌和未来未掩码令牌，其形式化定义为：

$$M_{ij} = \begin{cases} 0, & \text{where } (i \geq j \wedge i \not\in U) \vee (j \in U) \\ -\infty, & \text{otherwise} \end{cases}$$

其中 $U$ 为未掩码令牌的索引集合。该设计使得被掩码位置可以同时利用左右两侧的未掩码上下文进行预测，从而捕捉丰富的双向依赖关系。

训练目标为混合负对数似然损失，以概率 $\lambda$ 使用单向掩码、概率 $(1-\lambda)$ 使用双向掩码：

$$\mathcal{L}_{\mathrm{hybrid}} = - \underset{\mathbf{x} \in p(\mathbf{X})}{\mathbb{E}} \left[ \lambda \sum_{\forall i \in [1,t]} \log p_\theta(x_i \mid M^{uc}) + (1-\lambda) \sum_{\forall i \in [1,t]} \log p_\theta(x_i \mid M^{bc}) \right]$$

实验表明 $\lambda = 0.5$ 时性能最优。推理时采用分类器自由指导，通过线性组合条件 logits $\ell_c$ 和无条件 logits $\ell_u$ 增强文本对齐：

$$\ell_g = (1 + s) \cdot \ell_c - s \cdot \ell_u$$

其中 $s$ 为指导尺度。

### 残差运动细化

为进一步提升运动质量，BAMM 引入残差向量量化（RVQ）。RVQ 将原始运动序列编码为多层令牌序列（不同颜色表示不同量化层）。第一层量化器生成的基令牌序列由掩码自注意力变换器通过级联解码产生，随后作为细化变换器的输入，预测其余量化层的残差令牌序列。细化变换器与掩码自注意力变换器共享相同架构，但使用全注意力掩码。最终，合并后的多层令牌序列送入分词器解码器，重建高质量运动序列。

### 级联解码机制

推理时的双迭代级联解码是 BAMM 实现长度预测与质量精炼的关键：

1. **第一迭代**：采用单向因果掩码进行自回归解码，逐令牌生成粗粒度运动序列，并隐式预测 `[END]` 令牌以确定运动长度。
2. **第二迭代**：切换为双向因果掩码，对第一迭代中置信度较低的令牌进行掩码和重新预测，利用双向上下文依赖精炼运动质量。

该机制使 BAMM 无需预设运动长度即可生成高质量运动，同时获得了零样本运动编辑能力——通过将待编辑区域视为掩码令牌，模型可基于周围上下文和文本描述进行预测。

### 补充图表

![[assets/figures/papers/BAMM_Bidirectional_Autoregressive_Motion_Model_1dd6989b8f26/figures/004_Figure_3.jpg]]
*Figure 3: Inference: Dual-iteration Cascaded Motion Decoding. In the first iteration, autoregressive decoding is applied by adopting unidirectional causal mask to generate coarse-grained motion and predict motion sequence length. In the second iteration, bidirectional autoregressive decoding is performed via bidirectional causal mask to removing and repredicting low-confidence motion tokens autoregressively*

![[assets/figures/papers/BAMM_Bidirectional_Autoregressive_Motion_Model_1dd6989b8f26/figures/005_Figure_4.jpg]]
*Figure 4: Residual Motion Refinement. The residual vector quantization encodes the raw motion sequence into multiple token sequences in different colors (left). The base token sequence from the first vector quantizer is generated via cascaded decoding by masked self-attention transformer. The base token sequence is used as the input of the refinement transformer to predict the residual token sequences from other quantizers. The combined sequences are fed into tokenizer’s decoder for motion generation. The refinement transformer shares the same architecture as the masked self-attention transformer with a full attention mask(right)*

![[assets/figures/papers/BAMM_Bidirectional_Autoregressive_Motion_Model_1dd6989b8f26/figures/018_Figure_11.jpg]]
*Figure 11: Visualization of masking and conditional tokens for five temporal motion editing tasks: inpainting (in-betweening), outpainting, prefix, suffix, and long motion sequence. ■ indicates masked positions/areas*

## 实验与分析

### 核心定量结果

BAMM在HumanML3D和KIT-ML两个标准基准上进行了系统评估，评估指标包括FID（生成运动整体质量）、R-Precision Top-1（文本-运动对齐精度）和MM-Dist（多模态距离）。Table 2和Table 3分别报告了主要对比结果。

在HumanML3D上，BAMM在不依赖真实运动长度输入的设定下取得了具有竞争力的性能：FID达到0.055±.002，Top-1 R-Precision为0.525±.002，MM-Dist为2.919±.008。与需要真实长度的强基线相比，BAMM在FID上略逊于MoMask（0.045±.002），但在Top-1 R-Precision上超越了MoMask（0.521±.002）和MMM（0.504±.002），表明其文本-运动语义对齐能力更优。当BAMM也使用真实长度输入时（BAMM§），FID进一步降至0.041±.001，达到与MoMask§（0.040±.001）几乎持平的水平，验证了其生成质量的上限。

在KIT-ML上，BAMM取得了最优FID（0.183±.013），优于MoMask§（0.204±.011），同时Top-1 R-Precision（0.438±.009）也超越了所有对比方法。这一结果表明BAMM在小规模数据集上的泛化能力突出。

**关键结论**：BAMM在无需预设运动长度的前提下，实现了与需要真实长度的掩码生成模型相当甚至更优的文本-运动对齐精度，成功打破了“生成质量-长度预测可用性”之间的既有权衡。

### 长度预测与采样鲁棒性

BAMM的核心优势之一在于其隐式长度预测能力。Table 4和Table 7系统分析了这一特性对生成质量的影响。

Table 4对比了使用预测长度与真实长度的性能差异。对于MMM和MoMask等需要外部长度估计器的模型，使用预测长度会导致FID显著恶化（MMM从0.063升至0.080，MoMask从0.045升至0.090）。相比之下，BAMM无需外部长度估计器，其级联解码过程天然完成了长度预测，避免了这一性能退化。

Table 7进一步揭示了不同长度采样策略下的鲁棒性差异。当采用Multinomial采样（从预测分布中随机采样长度）而非Top-1采样时，MMM的FID从0.080退化为0.099，MoMask从0.090退化为0.120，而BAMM始终保持0.055的稳定性能。这说明BAMM的长度预测机制对采样策略不敏感，在实际部署中具有更高的可靠性。

Figure 10通过定性可视化佐证了这一结论：对于“the person crouches and walks forward”的提示，在不同输入长度约束下，MMM和MoMask的生成质量波动显著，而BAMM能生成与各种长度一致的高质量运动。

### 运动编辑能力评估

BAMM的零样本运动编辑能力是其区别于其他方法的关键特性。Table 5报告了五种时序编辑任务的定量评估结果，包括补全（inpainting）、外推（outpainting）、前缀预测、后缀补全和长序列合成。BAMM在所有编辑任务上均保持了较低的FID和较高的R-Precision，证明了其双向因果掩码机制能够有效利用周围上下文信息进行条件生成。

Figure 7展示了时序编辑的可视化效果（蓝色为条件帧，红色为生成部分），Figure 11详细说明了每种编辑任务对应的掩码方案。Figure 12进一步展示了长序列合成能力——BAMM能够在不同文本提示驱动的运动片段之间生成连贯的过渡帧，保持时序一致性。

### 消融实验

Table 6报告了关键设计选择的消融结果，揭示了以下因果机制：

**分类器自由指导（CFG）尺度**：第一迭代CFG=4、第二迭代CFG=3的组合取得了最优性能（Top-1 0.525, FID 0.055）。单一CFG尺度或非对称设置均导致性能下降，表明两阶段解码对指导强度有不同的需求——粗生成阶段需要更强的条件约束，精炼阶段则需要适度的多样性。

**掩码策略**：在双向精炼阶段，每隔一个令牌进行掩码（stride=2）优于随机掩码和连续掩码策略。这一发现表明，均匀分布的掩码模式能最大化双向上下文信息的利用效率。

**解码迭代次数**：两次迭代明显优于一次迭代（FID从0.064降至0.055），但三次迭代未带来显著增益（FID 0.054）。这表明级联解码的收益在两次迭代后趋于饱和，额外的精炼轮次增加了推理成本却未带来成比例的质量提升。

### 推理速度与局限性

尽管BAMM在生成质量和可用性上表现优异，其推理速度慢于纯并行解码方法（如MMM、MoMask）。级联解码过程包括单向自回归解码、双向掩码精炼和残差运动细化三个阶段，在NVIDIA RTX A5000上平均生成时间约为0.411秒/样本。这一速度虽远快于扩散模型（如MDM），但与纯掩码生成模型相比仍有差距，构成了当前方法的主要工程瓶颈。

此外，级联解码中的低置信度令牌选取标准、掩码比例等超参数仍需手动调优，其在不同数据分布下的最优设定尚未被系统研究。残差向量量化（RVQ）的层数和码本大小对生成质量与速度的精确权衡关系也值得进一步探索。

### 补充图表

![[assets/figures/papers/BAMM_Bidirectional_Autoregressive_Motion_Model_1dd6989b8f26/figures/002_Table_1.jpg]]
*Table 1: Comparison of quality and capability of generation on text-to-motion to state-of-the-art models on the largest text-to-motion dataset [16]. ‘✓’ means capability while ‘✗’ is not. "Predict Length" denotes the ability to generate motion without prior knowledge of motion length. "Input Length" refers to the ability to take input length as a constraint, while "Edit" indicates motion editability. Since MMM and MoMask require ground-truth motion length as input, we use predicted motion length from pretrained length estimator by [16]. The lowest FID score means the best overall quality of the generated motion, ensuring that its authenticity and naturalness is very close to the ground-truth human m...*

![[assets/figures/papers/BAMM_Bidirectional_Autoregressive_Motion_Model_1dd6989b8f26/figures/006_Table_2.jpg]]
*Table 2: Comparison of text-conditional motion synthesis on HumanML3D [16] test set. We repeat the evaluation 20 times for each metric and report the average with 95% confidence interval. Red and Blue indicate the best and the second best result. Methods with gray highlight § report motion generation results using the ground-truth motion length*

![[assets/figures/papers/BAMM_Bidirectional_Autoregressive_Motion_Model_1dd6989b8f26/figures/013_Table_6.jpg]]
*Table 6: Ablation Study*

![[assets/figures/papers/BAMM_Bidirectional_Autoregressive_Motion_Model_1dd6989b8f26/figures/016_Table_7.jpg]]
*Table 7: Comparison of text-conditional motion synthesis using different length samping stategies on HumanML3D [16] dataset*

![[assets/figures/papers/BAMM_Bidirectional_Autoregressive_Motion_Model_1dd6989b8f26/figures/010_Figure_7.jpg]]
*Figure 7: Visualization of temporal editing tasks, inpainting (in-betweening), outpainting, prefix, and suffix where blue indicates conditioned motion and red refers to generated parts*

![[assets/figures/papers/BAMM_Bidirectional_Autoregressive_Motion_Model_1dd6989b8f26/figures/014_Figure_8.jpg]]
*Figure 8: Generate motion with length constrain by input [END] as a condition and remove [END] output prediction*

![[assets/figures/papers/BAMM_Bidirectional_Autoregressive_Motion_Model_1dd6989b8f26/figures/015_Figure_9.jpg]]
*Figure 9: Histogram of motion token lengths. 1000 motions are generated for each textual description to calculate the estimated probability density of the token length. The corresponding lengths from the dataset HumanML3D [16] are called Real Length and highlighted in blue text. The length of motion is four times the token length*

![[assets/figures/papers/BAMM_Bidirectional_Autoregressive_Motion_Model_1dd6989b8f26/figures/019_Figure_12.jpg]]
*Figure 12: Visualization of Long Motion Sequence where blue frames represent individual motion segments prompted by textual descriptions. Red frames depict the intermediate transitions between these prompted segments, ensuring temporal coherence across the entire sequence*

## 方法谱系与知识库定位

### 1. 与基线方法的关系

BAMM 直接回应了当前文本驱动运动生成领域中三大范式——扩散模型、掩码生成模型和自回归模型——之间的根本性权衡。这一权衡体现在**生成质量、无需长度先验的可用性、以及运动编辑能力**三个维度上，现有方法难以同时兼顾。

**与扩散模型的对比（以 MDM 为代表）**：扩散模型（如 **MDM**，Tevet et al., ArXiv 2022）通过在连续空间中的迭代去噪实现高质量生成，但必须预设固定的运动长度作为输入。这一长度先验的依赖使其对长度估计器的精度高度敏感，且推理速度极慢。BAMM 通过级联解码中的单向自回归阶段隐式预测运动终点，从根本上消除了对外部长度先验的需求。

**与掩码生成模型的对比（以 MoMask、MMM 为代表）**：掩码生成模型（如 **MoMask**；**MMM**，Pinyoanuntapong et al., CVPR 2024）通过并行预测被掩码的令牌实现快速推理，且生成质量优异（MoMask 在 HumanML3D 上 FID 达到 0.045），但它们同样需要预设运动长度才能保证质量。当使用预测长度替代真实长度时，性能显著下降（MMM 的 FID 从 0.080 升至 0.099，MoMask 从 0.090 升至 0.120，见 Table 7）。BAMM 通过级联解码中第一阶段的长度预测和第二阶段的掩码精炼，在无需长度先验的条件下达到了与需要真实长度的 MoMask 可比甚至更优的质量。

**与自回归模型的对比（以 T2M-GPT 为代表）**：自回归模型（如 **T2M-GPT**，Zhang et al., CVPR 2023）天然支持长度预测，但其单向因果依赖限制了模型对全局上下文的利用，导致生成质量和编辑能力受限。BAMM 通过混合注意力掩码策略，在训练时同时学习单向和双向依赖，使模型保留了自回归的长度预测能力，同时获得了双向上下文建模带来的质量提升和零样本编辑能力。

### 2. 核心差异机制

BAMM 与上述方法的本质差异不在于架构层面的颠覆，而在于**训练和推理中注意力掩码策略的重新设计**。传统掩码生成模型通过替换令牌为 `[MASK]` 来实现条件预测，而 BAMM 直接操作注意力分数矩阵，通过单向因果掩码 $M^{uc}$ 和双向因果掩码 $M^{bc}$ 来控制信息流。双向因果掩码的定义（Equation 3）允许每个令牌同时关注其左侧的所有令牌和右侧的未掩码令牌，这为模型提供了比纯单向自回归更丰富的上下文，同时保留了逐令牌自回归预测的形式。

推理阶段的级联解码是另一关键差异。第一阶段的单向自回归解码生成粗粒度运动并隐式预测长度（通过预测 `[END]` 令牌），第二阶段则对低置信度令牌进行掩码和双向精炼。这种“先生成后精炼”的策略将长度预测与质量优化解耦，避免了单一阶段中二者的相互干扰。

### 3. 适用边界与能力定位

**长度预测的适用边界**：BAMM 的长度预测能力源于训练时单向掩码分支对序列终止条件的学习。在 HumanML3D 数据集上，BAMM 预测的长度分布与真实长度分布高度吻合（Figure 9），但这一能力依赖于训练数据中运动长度分布的覆盖范围。对于显著超出训练分布的超长或超短运动，长度预测的准确性需要进一步验证。

**编辑能力的适用边界**：BAMM 的零样本编辑能力源于双向因果掩码允许模型基于所有方向的上下文进行预测。这使其天然支持五种时序编辑任务：中间补全（inpainting）、外推（outpainting）、前缀预测、后缀补全和长序列合成（Figure 7, Figure 11）。然而，编辑质量依赖于被编辑区域周围上下文的信息量——当上下文稀疏或与目标编辑区域的语义关联较弱时，生成质量可能下降。

**长度约束生成的灵活性**：尽管 BAMM 的核心优势在于无需长度先验，它同样支持以长度作为约束条件的生成。通过将 `[END]` 令牌作为输入条件而非预测目标（Figure 8），BAMM 可以生成指定长度的运动，这使其在需要精确控制运动时长的应用场景中同样适用。

### 4. 局限与开放问题

**推理效率的固有局限**：BAMM 的级联解码过程包括单向自回归解码、双向掩码精炼和残差运动细化三个阶段，平均生成时间约为 0.411 秒/样本（NVIDIA RTX A5000）。虽然远快于扩散模型，但显著慢于并行解码的掩码生成方法（如 MMM 或 MoMask）。这一速度差距源于自回归解码的序列依赖性，是方法设计的内在权衡——以推理时间为代价换取长度预测和编辑能力。

**超参数敏感性与调优需求**：级联解码中的迭代次数、掩码策略和低置信度令牌的选取标准均需手动调优。消融实验（Table 6）表明，两次迭代优于一次（FID 从 0.064 降至 0.055），但三次迭代无显著增益；每隔一个令牌的掩码策略（stride=2）效果最佳。这些发现在 HumanML3D 上得到验证，但其在不同数据集或运动风格上的普适性尚不明确。低置信度令牌的鉴别标准（如基于预测概率的阈值选择）在论文中未作详细说明，这为复现和调优带来了不确定性。

**混合训练权重的最优性**：训练目标中单向和双向掩码的混合权重 $\lambda = 0.5$ 被实验证明在 HumanML3D 上最优，但该值是否在不同数据分布、不同运动粒度或不同下游任务上保持最优，仍是一个开放问题。$\lambda$ 本质上控制着模型在“长度预测能力”和“双向上下文建模能力”之间的资源分配，其最优值可能与目标应用中二者的相对重要性有关。

**残差量化的扩展性**：残差向量量化（RVQ）的引入提升了运动质量，但 RVQ 的层数和码本大小对生成质量与推理速度的具体权衡关系未被系统探索。更多的量化层可能捕获更精细的运动细节，但也会增加细化变压器的推理负担。

**长序列生成的连贯性**：BAMM 支持通过拼接多个运动片段生成任意长的运动序列（Figure 12），片段间的过渡令牌由模型自动生成。然而，当片段间的语义差异较大或缺乏明确的过渡逻辑时，跨片段连贯性可能下降。是否可以通过额外的条件信号（如音乐节奏、场景上下文）来引导过渡生成，是一个值得探索的方向。

**数据集偏差的潜在影响**：所有实验均在 HumanML3D 和 KIT-ML 上进行，这两个数据集以日常动作为主。BAMM 在更具挑战性的运动类型（如体育动作、舞蹈、交互式运动）上的泛化能力尚未得到验证。

## 原文 PDF

![[paperPDFs/ECCV_2024/BAMM_Bidirectional_Autoregressive_Motion_Model.pdf]]