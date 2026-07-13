---
title: "Fg-T2M++: LLMs-Augmented Fine-Grained Text Driven Human Motion Generation"
type: paper
paper_level: A
venue: IJCV
year: 2025
pdf_ref: paperPDFs/IJCV_2025/Fg_T2M_LLMs_Augmented_Fine_Grained_Text_Driven_Human_Motion_Generation.pdf
project_link: null
code_link: null
aliases:
- FT
- FTLAFGTDHMG
tags:
- IJCV_2025
- topic/generative_models_diffusion
- topic/generative_models_diffusion/generative_models_and_autoencoders
core_operator: "将全身动作生成分解为可组合的四肢与躯干子关节运动，并利用LLM进行细粒度身体部位解析与超文本句法结构编码，在条件扩散框架中实现由粗到精的多模态融合。"
primary_logic: "通过LLM语义解析将文本提示转化为六个身体部位的运动描述及词性语义，并构建依赖解析树嵌入双曲空间以保留句法层次，再通过句子级与词级分层特征融合，使扩散模型能够生成与复杂文本高度对齐的精确动作。"
claims:
- "Fg-T2M++在KIT-ML数据集上的FID达到0.135，相较前工作Fg-T2M的0.571降低0.436，MM-Dist从3.114降至2.696。"
- "在HumanML3D数据集上，Fg-T2M++取得R-Precision Top2 0.702、Top3 0.801和MultiModal Dist 2.925，全面超越所有现有最优方法。"
- "消融实验证实，移除LLM语义解析、超文本图卷积或分层融合模块均导致指标显著下降，尤其在长句和罕见文本条件下。"
- "KIT-ML 上 FID = 0.135"
---

# Fg-T2M++: LLMs-Augmented Fine-Grained Text Driven Human Motion Generation

> [!tip] 核心洞察
> 通过LLM语义解析将文本提示转化为六个身体部位的运动描述及词性语义，并构建依赖解析树嵌入双曲空间以保留句法层次，再通过句子级与词级分层特征融合，使扩散模型能够生成与复杂文本高度对齐的精确动作。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Fg-T2M++: 大语言模型增强的细粒度文本驱动人体动作生成 |
| 英文题名 | Fg-T2M++: LLMs-Augmented Fine-Grained Text Driven Human Motion Generation |
| 会议/期刊 | IJCV 2025 |
| Links | [paper](https://arxiv.org/abs/2502.05534) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/generative_models_and_autoencoders |
| Method | Fg-T2M++ |
| Dataset | KIT-ML |

> [!tip] 效果简介
> - KIT-ML 上，FID 为 0.135，对比 0.571 (Fg-T2M)，变化 -0.436。
> - KIT-ML 上，MM-Dist 为 2.696，对比 3.114 (Fg-T2M)，变化 -0.418。

## 概要

**核心问题**：现有文本驱动人体动作生成方法难以解析文本中关于身体部位的细粒度语义线索，且未能充分建模词间语言结构，导致生成的动作无法精确捕捉文本指定的空间关系与动作细节。这一瓶颈在长句、复杂描述和稀有动作组合场景中尤为突出。

**方法定位**：Fg-T2M++ 将全身动作生成分解为可组合的四肢与躯干子关节运动，通过**大语言模型（LLM）语义解析**提取六个身体部位的动作描述与词性语义，并构建**依赖解析树嵌入双曲空间**以保留句法层次结构。在条件扩散框架中，通过**句子级与词级分层特征融合**实现从粗到精的多模态交互，最终生成与复杂文本高度对齐的精确动作。

**方法谱系**：Fg-T2M++ 属于条件扩散模型家族，其直接前作为 **Fg-T2M**（Wang et al., ICCV 2023），后者仅进行粗粒度句法建模。与扩散基线 **MDM**（Tevet et al., ICLR 2023）和 **MotionDiffuse**（Zhang et al., TPAMI 2024）相比，Fg-T2M++ 的关键差异在于引入 LLM 驱动的细粒度语义解析和双曲空间句法编码；与检索增强的 **ReMoDiffuse**（Zhang et al., 2023）和自回归方法 **T2M-GPT**（Zhang et al., CVPR 2023）相比，Fg-T2M++ 通过分层融合机制实现了更精细的文本-运动对齐。

**核心结论**：在 KIT-ML 数据集上，Fg-T2M++ 的 FID 达到 0.135，较 Fg-T2M 的 0.571 降低 0.436；MM-Dist 从 3.114 降至 2.696。在 HumanML3D 数据集上，R-Precision Top2 为 0.702、Top3 为 0.801，MultiModal Dist 为 2.925，全面超越现有最优方法。消融实验证实，移除 LLM 语义解析、超文本图卷积或分层融合模块均导致指标显著下降，尤其在长句和罕见文本条件下退化明显。

**文本驱动的人体动作生成**旨在根据自然语言描述合成逼真的三维人体动作序列，在动画制作、虚拟现实与人机交互等领域具有重要应用价值。该任务的核心挑战在于建立文本语义与人体运动之间的精确映射关系。

近年来，扩散模型与自回归模型在该领域取得了显著进展。然而，现有方法存在一个**关键瓶颈**：它们通常将整个文本提示编码为单一全局表示，未能有效解析文本中关于身体部位的详细语义线索，也无法充分建模词与词之间的句法结构关系。这导致生成的动作往往无法精确捕捉文本指定的细粒度关系——例如，“左手举起的同时右脚向前迈步”这类涉及多部位协调的复杂描述。

具体而言，现有工作的局限性体现在三个层面：

1. **粗粒度文本解析**：以 **MDM**（Tevet et al., ICLR 2023）、**MotionDiffuse**（Zhang et al., TPAMI 2024）和 **T2M-GPT**（Zhang et al., CVPR 2023）为代表的扩散与自回归方法，依赖CLIP等预训练模型提取整个句子的单一特征，丢失了身体部位级别的语义信息。作者前工作 **Fg-T2M**（Wang et al., ICCV 2023）虽引入了句法建模，但仍停留在粗粒度层面。

2. **句法结构建模不足**：文本中的依赖关系（如主语-谓语-宾语结构）蕴含了动作执行者与被作用对象之间的层次信息。现有方法在欧氏空间中进行特征编码，难以有效保留这种树形层次结构。

3. **多模态融合粗糙**：文本特征与运动特征的交互通常仅通过简单拼接或单级交叉注意力实现，缺乏从全局语义到局部细节的渐进式融合机制。

针对上述缺口，**Fg-T2M++** 提出了一套系统性的解决方案：利用大语言模型（LLM）将文本提示解析为六个身体部位的细粒度运动描述及词性语义，通过双曲空间中的超文本图卷积编码句法层次结构，并在条件扩散框架内实现由粗到精的多模态分层融合。该方法在HumanML3D和KIT-ML两个基准数据集上均取得了最优性能，尤其在长句和罕见文本条件下展现出显著优势。

## 核心方法与创新机理

### 瓶颈与因果杠杆

现有文本驱动动作生成方法的根本瓶颈在于：它们通常将整个文本句子编码为单一全局表示，无法有效解析文本中关于身体部位的详细语义线索，也难以充分建模词间的语言结构关系，导致生成的动作未能精确捕捉文本指定的细粒度关系。Fg-T2M++ 的核心因果杠杆是将全身动作生成分解为可组合的四肢与躯干子关节运动，并利用大语言模型（LLM）进行细粒度身体部位解析与超文本句法结构编码，在条件扩散框架中实现由粗到精的多模态融合。

### 关键创新点（Changed Slots）

与现有方法相比，Fg-T2M++ 在以下三个关键维度上进行了根本性改造：

**1. 文本特征提取：从单一全局表示到LLM增强的细粒度语义与句法联合编码**

- **基线做法**：现有方法（如 **MDM**、**MotionDiffuse**、**T2M-GPT** 等）主要使用预训练模型（如 CLIP）提取整个句子的单一向量表示，丢失了词间关系与身体部位的对应信息。
- **Fg-T2M++ 的做法**：引入 **LLM语义解析模块（LSP）** 和 **超文本表示模块（HTP）** 两条互补路径：
  - **LSP** 利用 GPT-3.5/GPT-4 将文本提示解析为六个身体部位（头、躯干、左/右臂、左/右腿）的动作描述，同时提取名词、形容词、副词等词性语义，形成细粒度的部位级运动标注（Figure 3）。
  - **HTP** 通过依赖解析构建文本句法树，将词嵌入映射到庞加莱球（Poincaré ball）双曲空间中进行超文本图卷积（Hyperbolic Graph Convolution, HGC），利用双曲空间对层次结构的天然适配性，低失真地编码句法层次关系（Figure 4, Eq. 4）。
  - 进一步通过**交叉感知模块**（Cross-Perception Module）融合 LSP 解析特征与 HTP 句法特征，使两类互补语义信息相互增强（Eq. 5）。

**2. 多模态融合机制：从简单拼接/单级注意力到分层由粗到精融合**

- **基线做法**：多数方法采用简单拼接或单级交叉注意力将文本条件注入运动生成过程，缺乏对全局语义与局部细节的分层建模。
- **Fg-T2M++ 的做法**：提出 **多模态分层融合模块（MMF）**，包含两个递进层级（Figure 5）：
  - **句子级特征融合**：首先将 LSP 解析的全局语义与文本提示的整体语义进行融合，通过句子级注意力图对运动特征进行通道级加权增强，使运动编码获得全局语义引导（Eq. 8）。
  - **词级混合注意力融合**：在句子级融合基础上，进一步将运动特征、LLM 解析词特征与提示词特征进行词级混合注意力交互，通过统一键值张量实现文本-运动在细粒度词级别的迭代细化（Eq. 10）。

**3. 条件生成框架：标准扩散模型 + 精细化文本条件注入**

- **基线做法**：标准扩散模型或自回归模型使用粗粒度文本条件。
- **Fg-T2M++ 的做法**：在扩散模型的每个去噪步骤中，均使用经过 LSP 和 HTP 处理后的精细文本条件，并结合分类器自由引导（classifier-free guidance, Eq. 2）控制生成质量与文本对齐度。这使得模型能够在从噪声到干净运动的整个恢复过程中持续接收细粒度语义约束。

### 方法谱系与知识库定位

Fg-T2M++ 建立在条件扩散生成范式之上，与以下工作形成明确的方法演进关系：

- **前工作 Fg-T2M**（Wang et al., ICCV 2023）：仅做粗粒度句法建模，Fg-T2M++ 在此基础上引入 LLM 语义解析与双曲空间句法编码，实现了从粗粒度到细粒度的跨越。
- **扩散模型基线**：**MDM**（Tevet et al., ICLR 2023）和 **MotionDiffuse**（Zhang et al., TPAMI 2024）提供了条件扩散框架的基础，Fg-T2M++ 在其上构建了分层多模态融合机制。
- **检索增强方法**：**ReMoDiffuse**（Zhang et al., 2023）通过检索相似样本来增强生成，Fg-T2M++ 则通过 LLM 解析和句法编码直接从文本中提取精细语义，无需外部检索库。
- **自回归方法**：**T2M-GPT**（Zhang et al., CVPR 2023）和 **TM2T**（Guo et al., ECCV 2022）采用 VQ-VAE 与自回归生成，Fg-T2M++ 的扩散框架在细粒度控制上展现了更强的文本对齐能力。

### 证据强度总结

- **强证据**：定量实验表明，Fg-T2M++ 在 HumanML3D 和 KIT-ML 两个标准数据集上全面超越所有现有方法（Table 1, Table 2）。消融实验（Table 4, Figure 7, Figure 11）系统验证了 LSP、HTP 和 MMF 三个模块的独立贡献，移除任一模块均导致指标显著下降，尤其在长句和罕见文本条件下退化明显。
- **需注意的局限**：模型在处理超长句子（超过 196 帧对应的时间跨度）时可能遗漏某些特定动作组合（Figure 15），且未能建模人与环境的交互。这些场景下的创新有效性仍需进一步验证。

![[assets/figures/papers/paper_list_l28_https_arxiv_org_abs_2502_05534/figures/002_Figure_2.jpg]]
*Figure 2: Overview of Fg-T2M++: Given a text prompt c , the reverse denoising process of the diffusion model starts from noisy motion data X _ { T } and produces clean motion data X _ { 0 } . . Initially, the text prompt undergoes LLMs semantic parsing to generate LLMs-parsed fine-grained descriptions. Then, both the text prompt and its parsed descriptions are input into the hyperbolic text representation module, which captures precise representations of text features. Finally, the noisy motion data X _ { t } , along with the two fine-grained text features, are fed into the multi-modal fusion module to obtain the clean motion data X _ { t - 1 } ·*

Fg-T2M++ 采用条件扩散概率模型作为生成主干，将文本驱动的全身动作生成分解为三个协同模块的级联处理。给定文本提示 $c$，整个框架从随机噪声运动数据 $\mathbf{X}_T$ 开始，通过 $T$ 步迭代去噪，逐步恢复出与文本语义精确对齐的干净运动序列 $\mathbf{X}_0$。其逆扩散过程建模为：

$$p_{\theta}(\mathbf{x}_{0:T} \mid c) = p(\mathbf{x}_T) \prod_{t=1}^{T} p_{\theta}(\mathbf{x}_{t-1} \mid \mathbf{x}_t, c)$$

在每个去噪步骤中，模型使用分类器自由引导（classifier-free guidance）来平衡条件与无条件预测，通过尺度参数 $s$ 控制生成的可控性：

$$\epsilon = s \, \epsilon_{\theta}(\mathbf{x}_t, t, c) + (1 - s) \, \epsilon_{\theta}(\mathbf{x}_t, t, \mathcal{O})$$

训练目标为最小化预测运动与实际运动之间的 L2 距离：

$$\mathcal{L} = \mathbb{E}\left[\|\mathbf{x}_0 - \epsilon_{\theta}(\mathbf{x}_t, t, c)\|_2^2\right]$$

### 模块架构与数据流

框架的核心创新在于三个模块的串联设计，实现了从粗粒度句法到细粒度身体部位的层次化语义提取与融合（图 2）：

1. **LLMs 语义解析模块（LSP）**：首先将文本提示送入大语言模型（GPT-3.5/GPT-4），通过精心设计的提示策略，将原始文本解析为六个身体部位（头、躯干、左臂、右臂、左腿、右腿）的动作描述，同时提取名词、形容词、副词等词性语义（图 3）。这一步将全局文本分解为可组合的局部运动描述，为细粒度控制提供先验知识。

2. **超文本表示模块（HTP）**：同时接收原始文本提示和 LSP 解析后的细粒度描述。模块首先通过依赖解析（dependency parsing）构建文本的句法关系树，将每个词作为节点、依赖关系作为边（图 4a）。随后，将词嵌入通过指数映射投影到庞加莱球（Poincaré ball）双曲空间，在该流形上进行超文本图卷积（Hyperbolic Graph Convolution, HGC），利用莫比乌斯变换和双曲非线性激活 $\sigma^H$ 编码句法层次结构，再通过对数映射投影回欧氏空间：

   $$\mathbf{W}^{h} = \mathrm{Log}\left(\sigma^{H}\left(\mathcal{M}\ddot{\mathrm{o}}\mathrm{bius}\left(\mathrm{Exp}(\mathbf{W}^{E})\right)\right)\right)$$

   最后，通过交叉感知模块（Cross-Perception Module）将双曲编码的句法特征与 LSP 解析的语义特征进行注意力融合，生成全局上下文特征 $\mathbf{F}$：

   $$\mathbf{F} = \mathrm{softmax}\left(\mathbf{Key}[\mathbf{W}^{l}; \mathbf{W}^{t}]\right) \otimes \left(\mathbf{Value}[\mathbf{W}^{l}; \mathbf{W}^{t}]\right)$$

   其中 $\mathbf{W}^{l}$ 和 $\mathbf{W}^{t}$ 分别为 LLM 解析特征和文本提示特征。

3. **多模态融合模块（MMF）**：执行从粗到精的两级特征融合（图 5）。首先在句子级融合中，将 HTP 输出的全局语义特征通过通道注意力机制加权注入当前噪声运动 $\mathbf{X}_t$，获得交叉模态运动特征 $\mathbf{X}_t'$：

   $$\mathbf{X}_t' = \mathbf{X}_t + \lambda_l (\mathbf{X}_t \odot \sigma(\mathbf{A}_l)) + \lambda_p (\mathbf{X}_t \odot \sigma(\mathbf{A}_p))$$

   随后在词级融合中，将运动特征、LLM 解析词特征及提示词特征与各自的参考表示拼接，构建统一的键值张量进行混合注意力计算：

   $$\mathbf{Key} = [\mathbf{K}^{m} \mathbf{X}_t'; \mathbf{K}^{l} [\mathbf{W}^{l}; \mathbf{R}^{t}]; \mathbf{K}^{t} [\mathbf{W}^{t}; \mathbf{R}^{l}]]$$

   通过迭代细化文本-运动交互，最终输出去噪后的运动数据 $\mathbf{X}_{t-1}$。

### 关键设计逻辑

整个 pipeline 的核心因果机制在于：**将全身动作生成问题分解为“语义解析 → 句法编码 → 层次融合”三步**。LSP 利用 LLM 的先验知识解决细粒度身体部位语义的提取瓶颈；HTP 在双曲空间中编码依赖解析树，相比欧氏空间能更有效地保留句法层次结构，从而捕捉词间关系；MMF 通过句子级和词级的分层融合，使扩散模型在每一步去噪中都能同时利用全局语义和局部细节。消融实验证实，移除任一模块（LSP、HGC 或交叉感知）均会导致 FID 和 R-Precision 显著恶化（表 4），尤其在长句和稀有文本条件下退化更为明显（图 7、图 10）。

Fg-T2M++ 在条件扩散框架内集成了三个核心模块，构成“LLM解析→双曲句法编码→分层多模态融合”的级联管线（图2）。整体逆扩散过程建模为：

$$p _ { \theta } ( x _ { 0 : T } | c ) = p ( x _ { T } ) \prod _ { t = 1 } ^ { T } p _ { \theta } ( x _ { t - 1 } | x _ { t } , c ) \quad \text{(Eq. 1)}$$

其中 $c$ 为文本条件，$x_T$ 为初始噪声，$x_0$ 为生成的运动序列。训练目标为最小化预测噪声与真实噪声的 L2 损失：

$$\mathcal { L } = \mathrm { E } [ \| \mathbf { x } _ { 0 } - \epsilon _ { \theta } ( \mathbf { x } _ { t } , t , c ) \| _ { 2 } ^ { 2 } ] \quad \text{(Eq. 3)}$$

推理时采用分类器自由引导，通过尺度 $s$ 混合条件与无条件预测：

$$\epsilon = s \epsilon _ { \theta } ( x _ { t } , t , c ) + ( 1 - s ) \epsilon _ { \theta } ( x _ { t } , t , \mathcal { O } ) \quad \text{(Eq. 2)}$$

以下展开三个核心模块的机制与关键公式。

---

### 4.2 LLM语义解析模块（LSP）

该模块利用 GPT-3.5/GPT-4 将文本提示 $c$ 解析为两类细粒度表示：
- **六部位动作描述**：将全身运动分解为躯干（torso）、头部（head）、左/右臂（left/right arm）、左/右腿（left/right leg）六个身体部位的动作语义；
- **词性语义标注**：提取文本中的名词（nouns）、形容词（adjectives）、副词（adverbs）等词性信息，形成 $\mathbf{W}^l$。

解析策略通过精心设计的提示模板实现（图3），使 LLM 输出结构化的细粒度描述，为后续模块提供部位级语义先验。

---

### 4.3 超文本表示模块（HTP）

HTP 模块解决两个瓶颈：**句法结构编码**和**LLM解析特征的融合**。

**（1）文本树构建与双曲图卷积**

首先通过依存解析（dependency parsing）将文本提示构建为句法树，其中词为节点、依存关系为边（图4a）。为保留句法树的层次结构，将词嵌入 $\mathbf{W}^E$ 通过指数映射 $\mathrm{Exp}(\cdot)$ 投影到庞加莱球模型，经莫比乌斯变换（Möbius transformation）和双曲非线性激活 $\sigma^H$ 后，再通过对数映射 $\mathrm{Log}(\cdot)$ 投影回欧氏空间：

$$\mathbf { W } ^ { h } = \mathrm { L o g } ( \sigma ^ { H } ( \mathcal { M } \ddot { \mathrm { o b i u s } } ( \mathrm { E x p } ( \mathbf { W } ^ { E } ) ) ) ) \quad \text{(Eq. 4)}$$

该操作以低失真编码句法层次，得到句法增强的文本提示特征 $\mathbf{W}^t$。

**（2）交叉感知模块**

为充分利用 LLM 解析的细粒度描述 $\mathbf{W}^l$，交叉感知模块通过键值注意力计算全局上下文特征 $\mathbf{F}$：

$$\mathbf { F } = \mathrm { s o f t m a x } ( \mathbf { K e y } [ \mathbf { W } ^ { l } ; \mathbf { W } ^ { t } ] ) \otimes ( \mathbf { V a l u e } [ \mathbf { W } ^ { l } ; \mathbf { W } ^ { t } ] ) \quad \text{(Eq. 5)}$$

随后通过交叉注意力更新两种特征：

$$\mathbf{W}^{l} = \mathbf{W}^{l} + \operatorname{softmax}(\mathbf{Q}^{l}\mathbf{W}^{l}) \otimes \mathbf{F}$$

$$\mathbf{W}^{t} = \mathbf{W}^{t} + \operatorname{softmax}(\mathbf{Q}^{t}\mathbf{W}^{t}) \otimes \mathbf{F}$$

该机制使句法特征与部位语义相互增强，形成互补的文本表示对。

---

### 4.4 多模态分层融合模块（MMF）

MMF 模块在扩散去噪的每一步执行从粗到精的两级融合（图5）。

**（1）句子级特征融合**

首先，将 LLM 解析特征 $\mathbf{W}^l$ 和文本提示特征 $\mathbf{W}^t$ 经线性投影生成句子级注意力图 $\mathbf{A}_l$ 和 $\mathbf{A}_p$，用于通道级增强运动噪声 $\mathbf{X}_t$：

$$\mathbf { X } _ { t } ^ { \prime } = \mathbf { X } _ { t } + \lambda _ { l } ( \mathbf { X } _ { t } \odot \sigma ( \mathbf { A } _ { l } ) ) + \lambda _ { p } ( \mathbf { X } _ { t } \odot \sigma ( \mathbf { A } _ { p } ) ) \quad \text{(Eq. 8)}$$

其中 $\lambda_l$、$\lambda_p$ 为可学习权重，$\sigma$ 为 sigmoid 激活。该步骤将全局语义注入运动表示。

**（2）词级混合注意力融合**

将句子级特征经投影矩阵生成参考表示 $\mathbf{R}^l = \mathbf{M}^l \mathbf{S}^l$、$\mathbf{R}^t = \mathbf{M}^t \mathbf{S}^t$，并与词级特征拼接构建统一的键值张量：

$$\mathbf { K e y } = [ \mathbf { K } ^ { m } \mathbf { X } _ { t } ^ { \prime } ; \mathbf { K } ^ { l } [ \mathbf { W } ^ { l } ; \mathbf { R } ^ { t } ] ; \mathbf { K } ^ { t } [ \mathbf { W } ^ { t } ; \mathbf { R } ^ { l } ] ] \quad \text{(Eq. 10)}$$

$$\mathbf { V a l u e } = [ \mathbf { V } ^ { m } \mathbf { X } _ { t } ^ { \prime } ; \mathbf { V } ^ { l } [ \mathbf { W } ^ { l } ; \mathbf { R } ^ { t } ] ; \mathbf { V } ^ { t } [ \mathbf { W } ^ { t } ; \mathbf { R } ^ { l } ] ]$$

通过查询 $\mathbf{Query}$ 与全局模板 $\mathbf{G}$ 的注意力计算输出：

$$\mathbf{Y} = \operatorname{softmax}(\mathbf{Query}) \mathbf{G}$$

词级融合使每个运动帧能够精确关注文本中对应的细粒度词，实现部位级运动控制。

---

**因果机制总结**：LSP 将文本分解为部位级语义，HTP 在双曲空间编码句法层次并通过交叉感知融合 LLM 解析特征，MMF 以句子级→词级的分层方式将文本条件注入扩散去噪过程。消融实验证实，移除任一模块均导致 FID、R-Precision 和 MM-Dist 显著恶化（表4），尤其在长句和罕见文本条件下退化更为突出（图7、图10）。

## 实验与关键发现

### 核心性能：Fg-T2M++在两大基准上全面刷新最优指标

Fg-T2M++在HumanML3D和KIT-ML两个标准数据集上均取得最优结果，验证了LLM增强的细粒度文本解析与双曲空间句法建模的有效性。

在HumanML3D数据集上，Fg-T2M++的R-Precision Top2达到0.702、Top3达到0.801，MultiModal Dist降至2.925，全面超越包括**MDM**（Tevet et al., ICLR 2023）、**MotionDiffuse**（Zhang et al., TPAMI 2024）、**T2M-GPT**（Zhang et al., CVPR 2023）和**ReMoDiffuse**（Zhang et al., 2023）在内的所有对比方法（Table 1）。在KIT-ML数据集上，Fg-T2M++的FID从作者前工作**Fg-T2M**（Wang et al., ICCV 2023）的0.571大幅降至0.135，降幅达0.436；MM-Dist从3.114降至2.696，降幅0.418（Table 2）。这一性能跃升直接归因于三大模块的协同：LLM语义解析将文本分解为六个身体部位的动作描述，超文本表示在双曲空间中编码句法树的层次结构，多模态分层融合则实现从句子级到词级的逐步精细化控制。

![[assets/figures/papers/paper_list_l28_https_arxiv_org_abs_2502_05534/figures/007_Table_1.jpg]]
*Table 1: Quantitative evaluation on the HumanML3D (Guo et al., 2022a) test set. We run all the evaluation 20 times and ± indicates the 95% confidence interval. Red indicates the best result. Table 2: Quantitative evaluation on the KIT-ML (Plappert et al., 2016) test set*

### 消融实验：每个模块都不可或缺

消融实验在KIT-ML数据集上系统验证了各组件的贡献（Table 4）。移除LLM语义解析模块（LSP）后，模型在稀有文本条件下的FID大幅恶化（Fig. 7），证实LLM的先验知识是处理长尾语义的关键。将超文本图卷积（HGC）替换为标准欧氏空间GCN，R-TOP、FID和MM-Dist三项指标均显著变差（Table 4），双曲空间对句法树层次结构的保真度优势通过特征可视化得到直观印证（Fig. 9）：Fg-T2M++在庞加莱球中嵌入的文本特征呈现出清晰的层次聚类，而欧氏空间投影则丢失了这种结构。移除交叉感知模块或仅使用句子级融合同样导致性能下降（Table 4），表明LLM解析特征与句法特征的互补融合以及词级交互对细粒度控制至关重要。

![[assets/figures/papers/paper_list_l28_https_arxiv_org_abs_2502_05534/figures/010_Table_4.jpg]]
*Table 4: Ablation of the proposed components. All results are reported on the KIT-ML (Plappert et al., 2016) test set*

定性消融可视化（Fig. 11）进一步揭示了各模块缺失时的典型失败模式：无多模态融合模块时，动作与文本的全局语义对齐丧失；无超文本表示模块时，句法关系理解退化；无LLM语义解析模块时，身体部位的精细运动完全无法区分。

### LLM版本的影响：GPT-4带来进一步提升

将LLM语义解析模块中的GPT-3.5替换为GPT-4后，R-Precision Top3从0.75提升至0.77，FID从0.73降至0.68，MM-Dist从3.26降至3.15（Table 6）。这表明更强的语言模型能产生更准确的细粒度身体部位描述，从而直接提升运动生成质量。可视化对比（Fig. 22）也显示GPT-4的解析结果在语义准确性和细节丰富度上均优于GPT-3.5。

![[assets/figures/papers/paper_list_l28_https_arxiv_org_abs_2502_05534/figures/027_Table_6.jpg]]
*Table 6: The quantitative performance differences between GPT-3.5 and GPT-4*

![[assets/figures/papers/paper_list_l28_https_arxiv_org_abs_2502_05534/figures/028_Figure_22.jpg]]
*Figure 22: The visualization performance differences between GPT-3.5 and GPT-4*

### 细粒度与长难句评估：难度越大优势越明显

为进一步验证方法在复杂语义条件下的鲁棒性，论文设计了分层难度评估。按文本中细粒度词性（POS）数量将测试样本分为四个难度等级（0-25%至75-100%），Fg-T2M++在所有等级上的MM-Dist均优于对比方法，且在高难度区间优势更为显著（Fig. 6a）。按句子长度分层的R-TOP评估（Fig. 10）显示类似趋势：句子越长，Fg-T2M++相对于基线的提升越大。这表明LLM解析与双曲句法建模的组合策略有效缓解了长文本和复杂语义带来的对齐困难。

### 失败模式与局限性

尽管整体性能优越，Fg-T2M++仍存在明确的失败模式。处理长序列复杂动作组合时，模型可能遗漏某些特定动作（Fig. 15中红框标注的错误帧）。当前运动序列长度限制为196帧，无法生成更长时间跨度的连贯运动，也难以建模需要跨动作平滑过渡的场景。此外，模型未涉及人与环境（其他人物、场景物体）的交互建模，这限制了其在复杂场景中的应用。这些局限性指向了三个开放问题：如何扩展序列长度、如何实现动作间平滑过渡、以及如何引入环境交互先验。

![[assets/figures/papers/paper_list_l28_https_arxiv_org_abs_2502_05534/figures/021_Figure_16.jpg]]
*Figure 16: Visualization of more text samples’ features in hyperbolic space and Euclidean space. a) Text 1 feature projection of ReMoDiffuse (Zhang et al., 2023b) into Euclidean space. b) Text 1 feature projection of Fg-T2M++ into Euclidean space. c) Text 2 feature projection of ReMoDiffuse (Zhang et al., 2023b) into Euclidean space. d) Text 2 feature projection of Fg-T2M++ into Euclidean space*

## 定位与知识库关联

### 核心瓶颈与因果机制

Fg-T2M++ 瞄准的核心瓶颈在于：现有文本驱动动作生成方法无法有效解析文本中关于身体部位的详细语义线索，且未能充分建模词间语言结构，导致生成的动作未能精确捕捉文本指定的关系。其因果调节变量是将全身动作生成分解为可组合的四肢与躯干子关节运动，并利用LLM进行细粒度身体部位解析与超文本句法结构编码，在条件扩散框架中实现由粗到精的多模态融合。核心洞察在于：通过LLM语义解析将文本提示转化为六个身体部位的运动描述及词性语义，并构建依赖解析树嵌入双曲空间以保留句法层次，再通过句子级与词级分层特征融合，使扩散模型能够生成与复杂文本高度对齐的精确动作。

### 方法谱系定位

Fg-T2M++ 位于文本驱动人体动作生成这一研究脉络中，其直接前身是作者前工作 **Fg-T2M** (Wang et al., ICCV 2023)，后者仅做粗粒度句法建模。Fg-T2M++ 在此基础上引入了三个关键改进槽位：

1. **文本特征提取**：基线方法（如 **MDM** (Tevet et al., ICLR 2023)、**MotionDiffuse** (Zhang et al., TPAMI 2024)）通常使用预训练模型（如CLIP）提取整个句子的单一表示。Fg-T2M++ 则通过LLM语义解析生成六部位动作描述和词性语义，构建依赖树并嵌入庞加莱球进行超文本图卷积，再通过交叉感知模块融合句法和解析特征。

2. **多模态融合机制**：基线方法多采用简单拼接或单级交叉注意力。Fg-T2M++ 提出多模态分层融合（MMF），先经句子级特征融合获得全局语义，再通过词级混合注意力迭代细化文本-运动交互。

3. **条件生成框架**：在标准扩散模型基础上结合分类器自由引导，每个去噪步骤使用精细文本条件。

与该方向其他代表性工作相比：**T2M-GPT** (Zhang et al., CVPR 2023) 和 **TM2T** (Guo et al., ECCV 2022) 采用自回归范式；**TEMOS** (Petrovich et al., ECCV 2022) 和 **Temporal VAE** (Guo et al., 2022) 基于VAE框架；**ReMoDiffuse** (Zhang et al., 2023) 则引入检索增强机制。Fg-T2M++ 的独特贡献在于将LLM的语义解析能力与双曲空间的句法结构保持能力系统性注入扩散生成过程。

### 适用边界与局限

Fg-T2M++ 在以下场景展现出显著优势：
- 包含丰富身体部位描述和词性修饰的细粒度文本提示；
- 长句子和罕见文本条件下的动作生成（消融实验证实，移除LLM语义解析模块在稀有文本条件下FID大幅恶化）；
- 需要精确捕捉文本中身体部位间关系的场景。

其适用边界和局限包括：
- **长序列动作组合遗漏**：处理长句子时可能遗漏某些特定动作，如复杂的长序列动作组合（Figure 15 失败案例所示）。
- **帧数限制**：当前运动序列长度限制在196帧，难以生成更长时间跨度或需要跨动作平滑过渡的连贯运动。
- **环境交互缺失**：未能建模人与环境（如其他人物、场景）的交互，限制了在复杂场景中的应用。
- **LLM依赖性**：当LLM生成的细粒度描述与真实运动存在歧义或不一致时，模型缺乏缓解这种错配的机制。

### 开放问题

1. 如何将运动序列长度扩展至超过196帧，以支持更长时域的动作生成？
2. 如何在长动作序列中实现动作间的平滑过渡，避免片段式的不连贯？
3. 如何有效建模人与环境的交互（其他人物、场景），以拓展至更复杂的应用场景？
4. 当LLM生成的细粒度描述与真实运动存在歧义或不一致时，如何缓解这种错配？
5. 能否通过增加任务先验来增强LLM提示，以避免运动解析中的常识性错误？

## 原文 PDF

![[paperPDFs/IJCV_2025/Fg_T2M_LLMs_Augmented_Fine_Grained_Text_Driven_Human_Motion_Generation.pdf]]
