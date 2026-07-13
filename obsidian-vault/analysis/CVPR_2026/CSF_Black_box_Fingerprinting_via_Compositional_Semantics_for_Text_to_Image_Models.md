---
title: "CSF: Black-box Fingerprinting via Compositional Semantics for Text-to-Image Models"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/CSF_Black_box_Fingerprinting_via_Compositional_Semantics_for_Text_to_Image_Models.pdf
project_link: null
code_link: null
aliases:
- CSFC
- CSF
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过构造由常见语义组件组合而成的稀有提示（compositional prompts），这些提示在微调数据中几乎不存在，从而保留基础模型固有的语义偏见；同时利用组合爆炸防止攻击者枚举所有可能的提示。
primary_logic: 将文本到图像模型抽象为语义类别生成器，而非像素级合成器。通过探测模型对欠指定组合提示的类别解释分布（使用CLIP零样本分类），可以在黑盒条件下提取出对视觉风格变化鲁棒、且在微调后仍保留的模型指纹。
claims:
- 在6个基础模型家族（FLUX, Kandinsky, SD1.5/2.1/3.0/XL）和13个微调变体上，所有模型均满足优势检验（Dominance test），后验归属准确率超过50%。
- 用户研究中，CSF提示的人类归属准确率达到71%，而使用朴素提示的准确率仅为18%，远低于随机水平。
- 与Jensen-Shannon散度相比，Wasserstein距离提供了更高的归属置信度，置信度差距最高达54.5%。
- 即使在对抗性概念移除（UCE）后，CSF方法仍能维持0.714-0.857的归属后验均值。
---

# CSF: Black-box Fingerprinting via Compositional Semantics for Text-to-Image Models

> [!tip] 核心洞察
> 将文本到图像模型抽象为语义类别生成器，而非像素级合成器。通过探测模型对欠指定组合提示的类别解释分布（使用CLIP零样本分类），可以在黑盒条件下提取出对视觉风格变化鲁棒、且在微调后仍保留的模型指纹。

| 字段 | 内容 |
|------|------|
| 中文题名 | CSF：基于组合语义的文本到图像模型黑盒指纹识别 |
| 英文题名 | CSF: Black-box Fingerprinting via Compositional Semantics for Text-to-Image Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2604.16363) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Compositional Semantic Fingerprinting (CSF) |
| Dataset | 6 base model families with 13 fine-tuned variants, Human perceptual study, Attribution confidence comparison, Adversarial concept removal |

> [!tip] 效果简介
> - 6 base model families with 13 fine-tuned variants 上，Posterior mean attribution accuracy All >50% (Dominance test passed) vs Random chance 16.7% (Significant above chance and dominance)。
> - Human perceptual study 上，Identification accuracy 71% vs 18% (naive prompts) (+53%)。
> - Attribution confidence comparison 上，Confidence gap (Wasserstein vs JSD) Wasserstein provides higher confidence vs JSD (Up to +54.5%)。

## 概要

**问题瓶颈**：现有文本到图像（T2I）模型的指纹识别方法面临根本性局限——水印方案需要预部署阶段注入触发器，传统指纹依赖权重或激活等白盒/灰盒内部访问（图1）。在商业API仅提供“查询即所得”的黑盒条件下，微调会显著改变生成图像的视觉风格、色彩与构图，使得基于像素空间或视觉特征的方法失效（图3），无法可靠地将微调模型归属到其基础模型谱系。

**核心洞察**：CSF将T2I模型抽象为**语义类别生成器**而非像素级合成器。通过构造由常见语义组件组合而成的欠指定稀有提示（compositional underspecified prompts），这些提示在微调数据中几乎不存在，从而保留基础模型固有的语义偏见；同时利用组合爆炸防止攻击者枚举所有可能的提示。对每个提示采样多次生成，经CLIP零样本分类映射为类别分布，以Wasserstein距离比较分布差异，最终通过贝叶斯聚合框架进行统计推断。

**方法定位**：CSF在四个关键维度上区别于基线方案——探针类型从随机自然提示变为组合欠指定提示；表征空间从视觉嵌入或文本描述转为语义类别分布；距离度量从Jensen-Shannon散度（JSD）替换为Wasserstein-2距离；决策框架从确定性匹配升级为Beta-Binomial贝叶斯聚合与受控风险推断。

**主要结果**：
- 在6个基础模型家族（FLUX, Kandinsky, SD1.5/2.1/3.0/XL）和13个微调变体上，所有模型均满足优势检验（后验归属均值>50%），而随机概率基线仅为16.7%（Table 1）。
- 用户研究中，CSF提示的人类归属准确率达71%，朴素提示仅18%，低于随机水平（Figure 4）。
- Wasserstein距离相比JSD提供更高的归属置信度，置信度差距最高达54.5%（Table 2）。
- 在对抗性概念移除（UCE）后，CSF仍维持0.714–0.857的归属后验均值（Table 3）。

**局限与开放问题**：当模型无法准确遵循组合提示（如生成对象不属于目标类别）时方法可能失败（Figure 6）；更激进的语义擦除或对抗性微调是否能够彻底消除指纹仍待探索。



### 文本到图像生成模型的激增与溯源困境

近年来，以扩散模型（Diffusion Models）为核心的文本到图像（T2I）生成模型经历了爆发式增长。从开源的 **Stable Diffusion** 系列（v1.5、v2.1、XL、v3）到 **FLUX**（Black Forest Labs, 2024）、**Kandinsky** 等，大量基础模型被发布并广泛部署于商业API中。这些模型随后通过风格迁移、LoRA微调、模型融合、DPO对齐等方式衍生出海量微调变体，形成了一个庞大而复杂的模型谱系。

然而，这一生态的繁荣也带来了严峻的溯源挑战：当某个微调模型被用于生成侵权、有害或违规内容时，如何仅通过API查询将其归属到正确的基础模型家族？这一问题在真实侵权场景中至关重要，因为版权持有者和监管机构通常只能以“仅查询”的黑盒方式访问嫌疑模型，无法获取模型权重、激活值或训练数据。

### 现有方法的根本性缺口

当前主流的模型溯源方法存在两类结构性缺陷，使其无法应对上述黑盒归属场景。

**水印方法（Watermarking）需要预部署访问。** 水印技术要求模型发布者在训练或微调阶段向基础模型中注入特定触发器（trigger），以便事后通过检测该触发器来验证模型身份（Figure 1a）。然而，对于未经水印处理的第三方微调模型，这一方法完全失效——攻击者没有动机、也没有义务在非法微调时保留或注入水印。

**传统指纹方法依赖白盒或灰盒内部访问。** 传统指纹识别方法通常需要提取模型权重、中间层激活值或梯度等内部表征来构建模型指纹（Figure 1b）。在商业API仅返回生成图像的黑盒约束下，这些内部信息不可获取，使得传统指纹方法从根本上不可行。

### 朴素黑盒指纹的失败：视觉与文本空间的坍塌

一个直观的替代方案是直接使用生成图像的视觉特征进行指纹识别：向嫌疑模型发送提示（prompt），生成图像，然后通过CLIP等视觉编码器提取嵌入向量，比较不同模型生成图像的相似度。然而，这一思路在微调场景下全面失败。

**视觉空间失效。** 微调会显著改变生成图像的视觉风格、色彩调色板和构图方式。如图3a所示，对来自6个基础模型及其微调变体的生成图像进行CLIP嵌入的t-SNE可视化，结果显示图像完全按视觉风格聚类，而非按基础模型家族聚类。风格差异淹没了模型谱系信号。

**文本空间同样失效。** 即使将生成图像通过图像到文本（I2T）模型转换为描述文字，再在文本空间进行比较，问题依然存在。风格信息会泄漏到生成的描述文字中——例如，不同基础模型家族的微调变体可能因为都产生了“暗色调、高对比度”的风格描述而被聚类到一起（Figure 3b），导致跨家族的虚假相似性。

### 核心瓶颈：像素级合成器 vs. 语义类别生成器

上述失败的根源在于现有方法将T2I模型视为**像素级合成器**（pixel-level synthesizer），试图从视觉外观中提取指纹。然而，微调恰恰改变了视觉外观，使得基于像素或视觉特征的指纹变得不可靠。

CSF方法的核心洞察在于一个根本性的视角转换：将T2I模型重新抽象为**语义类别生成器**（semantic category generator）。当给定一个欠指定的提示（如“一只危险的夜行性城市动物”）时，不同基础模型会展现出不同的**语义偏见**——即它们倾向于生成哪种具体类别的动物（狗、猫、蝙蝠等）。这种语义层面的解释偏好深植于模型的训练数据分布中，且在视觉风格的微调过程中得以保留，从而构成了一种对风格变化鲁棒的模型指纹。

### 组合语义提示的稀有性保障

为了可靠地提取这种语义偏见，CSF采用**组合语义提示**（compositional underspecified prompts）：将多个在训练数据中各自常见的语义组件（如“危险的”+“夜行性”+“城市”+“动物”）组合成指数级稀有的组合。这种组合在微调数据中几乎不存在，因此微调过程无法针对性地修改模型对这些提示的语义解释，从而保留了基础模型固有的语义偏见。同时，组合爆炸效应使得攻击者无法枚举所有可能的提示来进行对抗性规避。

### 本文动机与贡献框架

综上所述，本文的核心动机在于填补黑盒条件下T2I模型谱系归属的方法论空白。具体而言，CSF方法通过以下设计实现这一目标：

1. **组合语义探测**：构造稀有组合提示，探测模型对欠指定语义的类别解释分布；
2. **语义分布距离度量**：使用Wasserstein距离比较模型间的语义类别分布，保留类别间的联合结构；
3. **贝叶斯统计推断**：跨多个提示聚合证据，提供具有统计显著性检验和可信区间的归属决策。



## 核心方法与创新机理

CSF 的核心贡献在于将文本到图像模型的指纹识别从像素/视觉空间迁移到**语义类别分布空间**，并以此为基础构建了一套完整的黑盒归属框架。相对于现有方法，CSF 在四个关键维度上实现了根本性的改变：

### 1. 探测方式：从朴素提示到组合语义提示

现有指纹方法通常使用从 LAION-2B 等数据集中随机采样的自然提示，或单一概念提示。这些提示在微调数据中频繁出现，导致微调模型可以轻易“覆盖”基础模型的原始行为。CSF 转而构造**组合性欠指定提示（compositional underspecified prompts）**，将多个单独常见的语义组件（如“危险的”“城市”“夜行”“动物”）组合成指数级稀有的组合。这些组合在微调数据中几乎不存在，因此基础模型固有的语义偏见得以保留，成为稳定的指纹信号。

提示设计遵循受控的三组件结构：欠指定语义属性 + 上级类别 + 特定场景条件（如“a dangerous urban nocturnal animal in a dimmed studio”）。这种设计利用了语言模型解析模糊描述时的**欠指定原理**——模型必须根据其预训练分布“脑补”缺失的细节，而不同基础模型的“脑补”方式存在系统性差异。

### 2. 表征空间：从视觉/文本空间到语义类别分布

传统方法在 CLIP 图像嵌入空间或图像描述文本空间中操作。如 Figure 3 所示，视觉空间中不同模型家族的嵌入完全混杂，无法形成有效聚类；文本空间则因风格信息泄漏导致跨家族模型错误聚合。CSF 将模型抽象为**语义类别生成器**，通过 CLIP 零样本分类将每张生成图像映射到预定义类别集合上的概率分布：

$$\phi_i = \mathrm{softmax}(\mathrm{CLIP}_{\mathrm{visual}}(I_i) \cdot \mathrm{CLIP}_{\mathrm{text}}(\{y_1, \dots, y_K\}))$$

这一转换将风格、色彩、构图等微调中剧烈变化的视觉因素剥离，仅保留模型对“应该生成什么类别对象”的语义决策。模型指纹定义为 $N$ 次生成的经验类别向量分布：

$$\phi = \frac{1}{N} \sum_{i=1}^N \delta_{\mathbf{p}_i}$$

### 3. 距离度量：从 JSD/LPIPS 到 Wasserstein-2 距离

基线方法使用 Jensen-Shannon 散度（JSD）或 LPIPS 等度量比较模型差异。CSF 采用 **Wasserstein-2 距离**：

$$W_2(\phi_1, \phi_2) = \left( \inf_{\gamma \in \Gamma(\phi_1, \phi_2)} \mathbb{E}_{(i,j)\sim\gamma}[\|\mathbf{p}_i - \mathbf{p}_j\|_2^2] \right)^{\frac{1}{2}}$$

这一选择具有关键的因果优势：Wasserstein 距离保留了类别间的联合结构和几何关系，能够捕捉语义偏差的**组合模式**，而 JSD 仅比较边缘分布的差异。实验证实（Table 2），Wasserstein 距离提供的归属置信度比 JSD 高出 15.9% 至 54.5%，验证了其对语义组合结构更强的敏感性。

### 4. 决策框架：从确定性匹配到贝叶斯聚合推理

CSF 将单次提示的归属决策（基于最近邻 Wasserstein 距离）作为一次“试验”，跨多个组合提示聚合证据，构建 **Beta-Binomial 贝叶斯推断框架**：

$$\theta \sim \mathrm{Beta}(\alpha, \beta), \quad \theta \mid s, f \sim \mathrm{Beta}(\alpha + s, \beta + f)$$

使用无信息先验 $\mathrm{Beta}(1,1)$，从成功/失败计数中获得归属准确率 $\theta$ 的后验分布和 95% 可信区间。框架包含两层统计检验：**显著性检验**（可信区间下界 > 随机水平 16.7%）和**优势检验**（可信区间下界 > 50%），确保归属结论在统计上可靠且具有实际决策价值。这比简单的多数投票或确定性匹配提供了更严谨的风险控制。

### 创新总结

| 维度 | 基线方法 | CSF 方法 | 因果机制 |
|------|---------|---------|---------|
| 探测类型 | 随机自然提示/单一概念提示 | 组合性欠指定提示 | 组合稀有性使微调无法覆盖基础模型语义偏见 |
| 表征空间 | 视觉嵌入（CLIP）/文本描述 | 语义类别分布（CLIP 零样本分类） | 剥离风格变化，仅保留语义决策信号 |
| 距离度量 | Jensen-Shannon 散度 / LPIPS | Wasserstein-2 距离 | 保留类别间联合结构，捕捉组合偏差模式 |
| 决策框架 | 确定性匹配/简单投票 | Beta-Binomial 贝叶斯聚合 | 提供置信区间和风险控制，支持统计推断 |

这四个 changed slots 协同作用，使得 CSF 能够在仅通过 API 查询的严格黑盒条件下，可靠地将微调模型归属到其基础模型谱系——这是现有水印方法（需预部署注入）和白盒/灰盒指纹方法（需权重或激活访问）均无法实现的能力。



CSF将文本到图像模型重新抽象为**语义类别生成器**（semantic category generator），而非传统的像素级合成器。这一抽象层的转换是方法的核心：它使指纹提取过程天然隔离了微调引入的视觉风格、色彩和构图变化，仅保留基础模型对语义组合的固有解释偏差。

### 核心假设与形式化条件

CSF建立在两个形式化条件之上（见Problem Formulation）：
- **可区分性条件**（Discriminability）：不同基础模型必须具有不同的语义标识符，即 $\phi_{M_i} \neq \phi_{M_j}$。
- **鲁棒性条件**（Robustness）：微调变体的标识符应接近其基础模型，即 $\phi_{M'} \approx \phi_{M}$。

这两个条件共同保证了在黑盒查询限制下，通过探测语义偏差既能区分不同模型家族，又能将微调变体正确归属到其基础模型谱系。

### Pipeline模块与数据流

CSF的完整工作流由五个顺序模块构成，形成从提示设计到统计推断的闭环：

**1. 组合提示构建（Compositional Prompt Construction）**
- 输入：预定义的上级类别（superordinate category）、语义属性（semantic attributes）和场景上下文（scene context）。
- 操作：将常见语义组件组合成欠指定的稀有提示，遵循三组件结构：`[欠指定属性] + [上级类别] + [特定条件]`（如“a dangerous urban nocturnal animal”）。
- 设计原理：利用组合爆炸使提示在微调数据中几乎不存在，从而保留基础模型固有的语义偏见；同时防止攻击者枚举所有可能提示。
- 输出：42个组合提示（见表A8），覆盖动物、烘焙食品、热带花卉等类别，每个类别系统性地变化语义属性和视觉上下文。

**2. 图像生成（Image Generation with Multiple Seeds）**
- 输入：单个组合提示 $C$。
- 操作：使用不同的随机种子生成 $N=30$ 张图像，以捕获模型对同一欠指定提示的多种语义解释。
- 输出：图像集合 $\{I_1, I_2, ..., I_N\}$。

**3. CLIP零样本分类（CLIP Zero-shot Classification）**
- 输入：生成图像 $I_i$ 和预定义的下属类别文本标签集合 $\{y_1, ..., y_K\}$。
- 操作：通过CLIP将每张图像映射到 $K$ 个类别上的概率分布：
  $$\phi_i = \mathrm{softmax}(\mathrm{CLIP}_{\mathrm{visual}}(I_i) \cdot \mathrm{CLIP}_{\mathrm{text}}(\{y_1, \dots, y_K\}))$$
- 输出：类别概率向量 $\mathbf{p}_i \in \Delta^{K-1}$。

**4. Wasserstein距离计算（Wasserstein Distance Computation）**
- 输入：两个模型的经验类别向量分布——待检测模型的经验指纹 $\phi = \frac{1}{N} \sum_{i=1}^N \delta_{\mathbf{p}_i}$ 与候选基础模型指纹。
- 操作：计算两个经验分布之间的2-Wasserstein距离：
  $$W_2(\phi_1, \phi_2) = \left( \inf_{\gamma \in \Gamma(\phi_1, \phi_2)} \mathbb{E}_{(i,j)\sim\gamma}[\|\mathbf{p}_i - \mathbf{p}_j\|_2^2] \right)^{\frac{1}{2}}$$
- 设计原理：Wasserstein距离保留类别间的联合结构，相比Jensen-Shannon散度能更忠实地捕捉语义偏差的组合结构（消融实验表明置信度差距最高达+54.5%，见表2）。
- 输出：单个提示下的距离度量，用于基础模型分类：$\hat{M}_{\mathrm{base}}(C) = \arg\min_{M_i} W_2(M'(C), M_i(C))$。

**5. 贝叶斯归属框架（Bayesian Attribution Framework）**
- 输入：跨多个组合提示的单次试验成功/失败计数 $(s, f)$。
- 操作：使用Beta-Binomial模型聚合证据，以无信息先验 $\mathrm{Beta}(1,1)$ 获得归属准确率 $\theta$ 的后验分布：
  $$\theta \mid s, f \sim \mathrm{Beta}(1 + s, 1 + f)$$
- 推断：基于95%可信区间进行显著性检验（CI low > 0.167 为显著高于随机水平）和优势检验（CI low > 0.5 为后验归属准确率超过50%）。
- 输出：归属决策及统计置信度。

### 与传统方法的对比

CSF在三个关键维度上与传统指纹方法形成对比（见Figure 1）：
- **水印方法**：需要预部署阶段向基础模型注入触发器，CSF无需任何模型访问。
- **传统白盒/灰盒指纹**：依赖权重或激活等内部访问，CSF仅需API查询。
- **朴素提示指纹**：使用LAION-2B随机采样提示，缺乏组合性和稀有性，人类归属准确率仅18%（vs. CSF的71%，见Figure 4）；在视觉空间（CLIP嵌入t-SNE）和文本空间（I2T字幕）上均无法形成模型家族聚类（见Figure 3）。

### 补充图表

![[assets/figures/papers/paper_list_l2301_https_arxiv_org_abs_2604_16363/figures/001_Figure_1.jpg]]
*Figure 1: Comparison of model identification scenarios. (a) Watermarking requires pre-deployment access to inject a trigger into the base model. (b) Traditional Fingerprinting relies on white-box or gray-box ‘Internal Access’ (e.g., weights or activations), which is not available in commercial API. (c) Our approach (CSF) is designed for the most restrictive ‘Query Only’ black-box setting, where the defender only has access to the final T2I generation API, reflecting realworld infringement scenarios*



### 方法总览：从像素到语义的抽象

CSF的核心洞察在于将文本到图像（T2I）模型重新抽象为**语义类别生成器**（semantic category generators），而非像素级合成器。这一抽象将指纹从易受微调影响的视觉风格空间中解耦，转而捕捉模型在解析欠指定（underspecified）语义组合时的固有偏见。方法包含两条并行管线：**指纹注册管线**（对已知基础模型建立参考指纹）与**指纹验证管线**（对嫌疑模型进行归属推断），二者共享相同的提示构造、生成和分类模块，仅在最终的距离计算与贝叶斯聚合阶段分叉。

### 模块一：组合语义提示构造

该模块是整个方法的因果调节旋钮。其设计基于两个语言学原理：**欠指定性**（underspecification）与**组合稀有性**（compositional rarity）。

每个提示遵循受控的三组件结构：
1. **欠指定语义属性**：如“危险的”（dangerous）、“夜行的”（nocturnal），这些属性在训练数据中高频出现，但本身不唯一确定一个下位类别。
2. **上级类别**：如“动物”（animal）、“烘焙食品”（baked goods），定义了语义搜索空间。
3. **具体场景条件**：如“在昏暗的工作室中”（in a dimmed studio）、“在木地板上”（on a wooden floor），提供视觉上下文约束。

形式化地，提示 $C$ 由一组语义组件 $\{a_1, a_2, \dots, a_m\}$ 和一个上级类别 $Y_{\text{super}}$ 组合而成。每个组件在训练数据中独立常见，但其**组合**在微调数据中几乎不存在——这利用了组合爆炸原理，使得攻击者无法枚举所有可能的提示。Table A8展示了完整的42个提示的组合结构，涵盖5个上级类别，每个类别系统性地变化语义属性和视觉场景。

### 模块二：CLIP零样本类别提取

对于给定提示 $C$ 和模型 $M$，生成 $N=30$ 张图像（使用不同随机种子）。每张图像 $I_i$ 通过CLIP零样本分类映射到一个预定义下位类别集合 $\{y_1, \dots, y_K\}$ 上的概率分布：

$$\phi_i = \mathrm{softmax}\big(\mathrm{CLIP}_{\mathrm{visual}}(I_i) \cdot \mathrm{CLIP}_{\mathrm{text}}(\{y_1, \dots, y_K\})\big) \tag{6}$$

其中 $\mathrm{CLIP}_{\mathrm{visual}}(\cdot)$ 和 $\mathrm{CLIP}_{\mathrm{text}}(\cdot)$ 分别为CLIP的图像和文本编码器，$K$ 为上级类别下的下位类别数量（如“动物”下包含狗、猫、鸟等）。输出 $\phi_i \in \Delta^{K-1}$ 是 $K$ 维概率单纯形上的一个点。

### 模块三：经验指纹构建

模型 $M$ 在提示 $C$ 下的指纹定义为其诱导的类别向量分布 $P(\mathbf{p} \mid C, M)$。通过 $N$ 次独立生成，获得经验分布作为该分布的蒙特卡洛近似：

$$\phi_M(C) = \frac{1}{N} \sum_{i=1}^N \delta_{\mathbf{p}_i} \tag{7}$$

其中 $\delta_{\mathbf{p}_i}$ 是位于点 $\mathbf{p}_i$ 的狄拉克测度。这一经验分布构成了模型在给定提示下的**语义指纹**——它捕捉了模型对欠指定提示的类别解释倾向，而非生成图像的表面视觉特征。

### 模块四：Wasserstein距离度量

两个模型 $M_1$ 和 $M_2$ 在提示 $C$ 下的指纹差异通过 **2-Wasserstein距离** 衡量：

$$W_2(\phi_1, \phi_2) = \left( \inf_{\gamma \in \Gamma(\phi_1, \phi_2)} \mathbb{E}_{(i,j)\sim\gamma}\left[\|\mathbf{p}_i - \mathbf{p}_j\|_2^2\right] \right)^{\frac{1}{2}} \tag{8}$$

其中 $\Gamma(\phi_1, \phi_2)$ 是所有边缘分布为 $\phi_1$ 和 $\phi_2$ 的联合分布（couplings）的集合。与Jensen-Shannon散度（JSD）相比，Wasserstein距离的关键优势在于它**保留类别间的几何结构**：它不仅衡量两个分布对同一类别赋予的概率差异，还考虑概率质量在类别空间中的移动成本。消融实验（Table 2）证实，Wasserstein距离提供的归属置信度比JSD高出15.9%至54.5%。

### 模块五：贝叶斯归属推断框架

单次试验的归属决策通过最小化嫌疑模型 $M'$ 与所有候选基础模型 $\{M_i\}$ 之间的Wasserstein距离完成：

$$\hat{M}_{\mathrm{base}}(C) = \operatorname*{argmin}_{M_i \in \{\text{base models}\}} W_2\big(M'(C), M_i(C)\big) \tag{9}$$

为跨多个提示聚合证据并控制统计风险，CSF采用**Beta-Binomial贝叶斯模型**。将归属准确率 $\theta$ 建模为随机变量，赋予无信息先验 $\mathrm{Beta}(1,1)$。在观察到 $s$ 次成功和 $f$ 次失败后，后验分布为：

$$\theta \mid s, f \sim \mathrm{Beta}(1 + s, 1 + f) \tag{10}$$

基于此后验，框架进行两类统计检验：
- **显著性检验**：检查95%可信区间下限是否高于随机概率 $1/K$（其中 $K$ 为基础模型数量，实验中为6，随机概率约16.7%）。
- **优势检验**（Dominance test）：检查95%可信区间下限是否超过50%，确保归属结果不仅是非随机的，而且在实际决策中占主导地位。

这一框架将单次试验的硬决策转化为概率推断，允许在任意数量的提示上增量聚合证据，并以可控的风险阈值做出最终归属判断。

### 补充图表

![[assets/figures/papers/paper_list_l2301_https_arxiv_org_abs_2604_16363/figures/004_Figure_3.jpg]]
*Figure 3: Challenges in naive fingerprinting approaches. (a) Visual space: t-SNE visualization of CLIP embeddings shows no family clustering. (b) Text space: Even when images are converted to captions via I2T models, style information leaks into the text, causing models from different families (e.g., SD1.5 DPO and SD2.1) to cluster together due to similar style descriptors*

![[assets/figures/papers/paper_list_l2301_https_arxiv_org_abs_2604_16363/figures/002_Figure_2.jpg]]
*Figure 2: The “Name That Dataset” game [52] in Diffusion Fingerprinting. Image (a) is from a fine-tuned model (SD1.5- DreamShaper). One of the images (b, c, d) is its base model. This figure illustrates how difficult it is to identify the base model using a naive prompt (right column, randomly sampled from LAION-2B [46]), compared to our CSF prompt (left column). All images are uncurated results generated with different random seeds. Can you specify which model (b, c, or d) is the base model for (a)? Answer: (a) SD1.5-DreamShaper (fine-tuned), (b) SD2.1-DPO (fine-tuned), (c) SD1.5 Base, and (d) SDXL Base. The correct base model for (a) is (c)*

![[assets/figures/papers/paper_list_l2301_https_arxiv_org_abs_2604_16363/figures/024_Table.jpg]]
*Table: A8. Compositional structure of fingerprinting prompts. Each category systematically varies semantic attributes and visual contexts, yielding 42 total prompts (9+9+6+9+9). The dimmed studio setting appears across all categories to enable cross-category comparison*



## 实验与关键发现

### 核心实验设置

CSF在6个基础模型家族（FLUX、Kandinsky、SD1.5、SD2.1、SD3.0、SDXL）和13个微调变体上进行了评估，微调类型覆盖风格迁移、LoRA、模型合并和DPO等主流范式。指纹提示库包含42个精心设计的组合提示，每个提示遵循“欠指定属性 + 上级类别 + 具体场景条件”的三组件结构（Table A8）。对于每个提示，使用30个不同随机种子生成图像，通过CLIP零样本分类映射到预定义类别集合上的概率分布，以Wasserstein-2距离衡量模型间语义分布的差异，最后通过Beta-Binomial贝叶斯框架聚合跨提示的归属证据。

### 主结果：微调变体的归属准确率

Table 1展示了所有13个微调变体的后验归属均值。核心发现如下：

- **所有模型均通过优势检验（Dominance test）**：95%可信区间下界均超过50%，表明CSF能够以高于随机猜测（16.7%）的置信度将微调模型正确归属到其基础模型。
- **高置信度归属案例**：FLUX-Turbo-Alpha和SD1.5-1.4-Base的后验均值达到0.977，FLUX-LoRA为0.932，Kandinsky-Naruto为0.977，这些结果的可信区间下界远超0.5，表明归属判断具有统计显著性。
- **跨微调范式的鲁棒性**：无论是风格迁移（DreamShaper）、LoRA微调还是DPO对齐，CSF均能维持有效的归属能力，验证了组合语义指纹对视觉风格变化的鲁棒性。

### 用户研究：组合提示的人类可解释性

Figure 4展示了“命名数据集”游戏的用户研究结果。参与者使用CSF组合提示识别基础模型的准确率达到**71%**，而使用从LAION-2B随机采样的朴素提示时准确率仅为**18%**，低于随机猜测水平。这一53%的性能差距表明：组合提示不仅对机器有效，其揭示的语义偏见在人类感知层面同样可辨识，而朴素提示因缺乏组合性和稀有性，无法暴露模型间的系统性差异。

### 距离度量的消融：Wasserstein vs. JSD

Table 2对比了Wasserstein距离与Jensen-Shannon散度（JSD）的归属置信度。Wasserstein距离在所有模型上提供了更高的归属置信度，置信度差距范围为**+15.9%至+54.5%**。这一差异的根源在于：Wasserstein距离保留了类别间的几何结构（如“哈士奇”与“狼”在语义空间中的邻近关系），而JSD将类别视为独立维度，丢失了组合语义中的联合分布信息。Table A5-A7的补充分析进一步验证了Wasserstein在跨提示一致性上的优势。

![[assets/figures/papers/paper_list_l2301_https_arxiv_org_abs_2604_16363/figures/017_Table.jpg]]
*Table: A5. 95% Confidence Interval Lower Bound of the Derived Models with our method*

### 组合提示设计的消融

Figure 5揭示了场景上下文对生成类别分布的系统性影响。以“dimmed-studio”为基准设置，当场景切换为“dish”或“wooden-floor”时，生成的类别混合分布发生实质性偏移和扩展。这一现象验证了组合提示设计的核心假设：通过系统性地变化语义属性和视觉上下文，可以探测模型对不同语义组件的解释偏好，而这些偏好构成了模型特有的指纹。

移除组合特征的消融实验显示：仅使用基础提示（不含组合约束）会导致归属性能大幅下降，出现显著的模型间混淆。这证实了组合稀有性对于指纹判别力的关键作用——单个常见语义组件在微调数据中广泛存在，无法提供足够的模型区分度。

### 对抗性鲁棒性：概念移除后的归属能力

Table 3展示了在对抗性概念移除（UCE）后的归属结果。使用9个动物特异性探针，在移除动物相关概念后，CSF仍能维持**0.714至0.857**的后验归属均值，所有结果均显著高于随机水平。这表明组合语义指纹不仅依赖于单一概念的存在，而是编码在模型对语义组合的整体解释模式中——即使特定概念被擦除，模型在相关类别上的残余偏见仍可被组合探针捕获。

### 失败模式分析

Figure 6展示了CSF的典型失败案例。当模型无法准确遵循组合提示时（例如，提示要求生成“brick wall前的烘焙食品”但模型未能生成可识别的目标类别对象），CLIP零样本分类无法提取有意义的语义分布，导致指纹失效。这一失败模式揭示了方法的核心前提：模型必须能够基本理解并执行组合提示的语义约束。对于生成能力较弱的模型或过于复杂的组合约束，指纹质量会显著下降。

### 层次聚类基线对比

Table A3和A4显示，在原始指纹向量上直接应用层次聚类无法实现可靠的模型家族识别，进一步验证了CSF方法中Wasserstein距离度量和贝叶斯聚合框架的必要性——简单的距离聚类无法有效捕捉高维语义分布中的细微但系统性的模型间差异。

### 补充图表

![[assets/figures/papers/paper_list_l2301_https_arxiv_org_abs_2604_16363/figures/005_Table_1.jpg]]
*Table 1: Posterior Mean of the Derived Models. In this table, indicates significance a (Confidence Interval (CI) low > 0.167), indicates Not significant (CI includes 0.167), and indicates Sig. below chance (CI high*

![[assets/figures/papers/paper_list_l2301_https_arxiv_org_abs_2604_16363/figures/006_Figure_4.jpg]]
*Figure 4: User study results for the “Name That Dataset” game (Fig. 2). Participants attempted to identify the correct base model using naive prompts (LAION-2B [46]) vs. our CSF prompts*

![[assets/figures/papers/paper_list_l2301_https_arxiv_org_abs_2604_16363/figures/009_Table_2.jpg]]
*Table 2: Attribution confidence: Wasserstein vs. JSD*

![[assets/figures/papers/paper_list_l2301_https_arxiv_org_abs_2604_16363/figures/010_Table_3.jpg]]
*Table 3: Attribution results under adversarial concept removal. Posterior mean attribution scores computed from 9 animalspecific probes after removing animal-related concepts using UCE*

![[assets/figures/papers/paper_list_l2301_https_arxiv_org_abs_2604_16363/figures/007_Figure_5.jpg]]
*Figure 5: Generated category distributions vary substantially with scene context. Compared with the dimmed-studio setting, the dish and wooden-floor settings produce broader and systematically shifted category mixtures. Each donut summarizes 40 samples, and the same color denotes the same category across scenes*

![[assets/figures/papers/paper_list_l2301_https_arxiv_org_abs_2604_16363/figures/008_Figure_6.jpg]]
*Figure 6: Failure cases of CSF. Top: prompts for baked goods in front of a brick wall. Bottom: prompts for tropical flowers on a pot. In both cases, models failed to generate identifiable objects within the target categories*

![[assets/figures/papers/paper_list_l2301_https_arxiv_org_abs_2604_16363/figures/012_Table.jpg]]
*Table: A2. Average Normalized Wasserstein Distance Matrix across all prompts. Each value is the mean of column-normalized distances across all 42 prompts. Short, Medium-low, Medium-high, Long distance*



## 定位与知识库关联

### 问题定位：黑盒指纹识别的瓶颈

CSF方法针对的是一个此前未被充分解决的**黑盒归属问题**：在仅能通过API查询目标模型（“Query Only”）的条件下，判断一个微调后的文本到图像模型来源于哪一个基础模型家族。现有方案在此场景下均存在根本性限制：

- **水印方法**需要在模型部署前注入触发器，无法应对已部署模型的侵权归属需求。
- **传统指纹方法**依赖白盒或灰盒内部访问（权重、激活值），而商业API通常不提供此类接口。
- **基于视觉特征的方法**（如直接使用CLIP图像嵌入聚类）在微调后失效，因为微调会显著改变生成图像的视觉风格、色彩和构图，导致不同家族模型因风格相似而错误聚类（Figure 3a）。
- **基于文本描述的方法**同样不可靠：即使通过Image-to-Text模型将图像转换为描述，风格信息会泄漏到文本中，导致不同家族模型因共享风格描述符而混淆（Figure 3b）。

上述挑战构成了CSF方法设计的核心动机：需要一种对视觉风格变化鲁棒、且仅需黑盒查询即可提取的模型指纹。

### 核心洞察：从像素合成器到语义类别生成器

CSF的关键方法论转向在于**重新抽象文本到图像模型的本质**。现有方法将模型视为像素级合成器，试图在视觉空间或文本空间寻找不变特征。CSF则将模型抽象为**语义类别生成器**（semantic category generator）：给定一个提示，模型本质上是在一个语义类别空间上诱导出一个概率分布，这个分布反映了模型对提示中欠指定成分的**解释性偏见**（interpretive biases）。

这一抽象的合理性基于以下观察：基础模型在预训练过程中习得了特定的语义关联模式（例如，“危险的夜间城市动物”更倾向于生成狗还是浣熊），这些模式构成了模型的“语义指纹”。微调主要改变视觉风格，但底层语义偏见在很大程度上得以保留——这正是CSF能够跨微调变体进行归属的根本原因。

### 方法组件与基线对比

CSF由四个关键组件构成，每个组件都对应一个相对于基线方法的改进槽位：

**探针设计**（Probe type）。基线方法使用从LAION-2B中随机采样的朴素提示（naive prompts），这些提示在微调数据中常见，且缺乏对模型语义偏见的针对性探测。CSF转而构造**组合语义提示**（compositional prompts），将常见的语义组件（如“危险的”、“夜间”、“城市”、“动物”）组合成在微调数据中几乎不存在的稀有组合。这种设计利用组合爆炸防止攻击者枚举所有可能提示，同时确保提示的稀有性使其在微调数据中不存在，从而保留基础模型的固有偏见。

**表征空间**（Representation space）。基线方法在视觉空间（CLIP图像嵌入）或文本空间操作，这些空间对风格变化敏感。CSF将生成图像通过CLIP零样本分类映射到**语义类别分布**（semantic categorical distribution），即一个预定义类别集合上的概率向量：
$$\phi_i = \mathrm{softmax}(\mathrm{CLIP}_{\mathrm{visual}}(I_i) \cdot \mathrm{CLIP}_{\mathrm{text}}(\{y_1, \dots, y_K\}))$$
这一映射将像素级输出抽象为语义级信号，有效隔离了风格变化的影响。

**距离度量**（Distance metric）。基线方法使用Jensen-Shannon散度（JSD）或LPIPS等度量。CSF采用**Wasserstein-2距离**来衡量两个模型的经验类别分布之间的差异：
$$W_2(\phi_1, \phi_2) = \left( \inf_{\gamma \in \Gamma(\phi_1, \phi_2)} \mathbb{E}_{(i,j)\sim\gamma}[\|\mathbf{p}_i - \mathbf{p}_j\|_2^2] \right)^{\frac{1}{2}}$$
实验表明，Wasserstein距离比JSD提供了显著更高的归属置信度，置信度差距最高达+54.5%（Table 2）。这是因为Wasserstein距离能够保留类别间的联合结构，而JSD将分布视为独立类别上的简单概率质量比较。

**决策框架**（Decision framework）。基线方法采用确定性匹配或简单多数投票。CSF使用**贝叶斯聚合框架**，通过Beta-Binomial模型跨多个提示聚合单次试验结果：
$$\theta \sim \mathrm{Beta}(\alpha, \beta), \quad \theta \mid s, f \sim \mathrm{Beta}(\alpha + s, \beta + f)$$
该框架使用无信息先验Beta(1,1)，计算归属准确率θ的后验分布和95%可信区间，并基于此进行显著性检验（与随机水平16.7%比较）和优势检验（后验均值是否超过50%），从而提供统计上可控的归属决策。

### 与相关工作的关系

CSF在方法谱系中填补了**黑盒语义指纹识别**的空白。与需要白盒访问的传统指纹方法（如基于权重或激活特征的方法）形成互补关系；与需要预部署的水印方法形成替代关系。在概念层面，CSF借鉴了形式语义学中的**欠指定**（underspecification）原理——即语言模型如何解析模糊描述——将其应用于生成模型的探测设计。

### 适用边界与失效模式

CSF的有效性依赖于以下前提条件，这些条件定义了其适用边界：

1. **模型必须能够遵循组合提示**。当模型无法生成目标类别内的可识别对象时（例如，提示要求生成“砖墙前的烘焙食品”，但模型输出无法被CLIP分类为任何目标类别），方法失效（Figure 6）。这意味着CSF对基础模型的生成能力有一定要求。

2. **语义偏见在微调后必须保留**。CSF假设微调主要改变视觉风格而非语义偏见。当微调方式直接针对语义概念进行操作时（如对抗性概念移除UCE），归属置信度会下降，尽管实验表明仍维持在随机水平以上（后验均值0.714-0.857，Table 3）。更激进的语义擦除方法可能构成更强的威胁。

3. **组合提示的设计依赖人工领域知识**。当前方法需要人工设计语义类别和属性组合（Table A8展示了42个提示的组合结构），这限制了方法的可扩展性。

### 开放问题

1. **对抗鲁棒性的上限**：更强大的对抗性攻击（如针对语义概念的adversarial fine-tuning）能否彻底消除CSF指纹？UCE实验表明当前方法具有一定鲁棒性，但该方向仍需系统研究。

2. **跨模型家族的泛化**：CSF在扩散模型家族（Stable Diffusion系列、Flux、Kandinsky）上得到验证，但其是否适用于非扩散架构的生成模型（如自回归模型、GAN）尚待探索。

3. **自动化提示发现**：能否自动化地发现最优组合提示，而无需人工设计？这涉及对模型语义偏见空间的自动探索。

4. **大规模部署的可行性**：在涉及数十个基础模型家族的场景中，CSF的统计推断框架是否仍能维持可接受的置信度水平，需要进一步验证。



## 原文 PDF

![[paperPDFs/CVPR_2026/CSF_Black_box_Fingerprinting_via_Compositional_Semantics_for_Text_to_Image_Models.pdf]]
