---
title: "Erasing Thousands of Concepts: Towards Scalable and Practical Concept Erasure for Text-to-Image Diffusion Models"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Erasing_Thousands_of_Concepts_Towards_Scalable_and_Practical_Concept_Erasure_for_Text_to_Image_Diffusion_Models.pdf
project_link: null
code_link: "https://github.com/GantMan/nsfw_model"
huggingface_link: "https://huggingface.co/black-forest-labs/FLUX.1-dev"
aliases:
- ETCE
- ETCTSPCETIDM
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 通过Student's t分布混合模型（tMM）建模概念嵌入分布，利用仿射最优传输（AOT）实现锚点无关的精确概念映射，并采用混合专家（MoE）模块MoEraser结合噪声注入-恢复（NIR）训练，达成大规模、无锚点且防移除的擦除。
primary_logic: 概念嵌入在上下文变化下呈现低秩重尾分布，tMM可有效建模该分布；从分布的高概率区域采样目标嵌入、低概率区域采样锚嵌入，消除了人工锚点选择；AOT将目标分布映射到融合的匿名概念，安全高效；MoE架构天生适应异构领域，NIR通过破坏权重并恢复使模块不可移除。
claims:
- tMM建模在擦除与保留的平衡上显著优于GMM（Table 4）。
- 从目标分布边界采样的锚嵌入性能与人工锚点相当甚至更好（Table 5）。
- ETC成功擦除2,072个概念并保持图像质量，在用户研究中CRSt最低、QS最高（Table 2）。
- ETC在50位名人擦除任务中取得最优H0=0.943（Table 3）。
---

# Erasing Thousands of Concepts: Towards Scalable and Practical Concept Erasure for Text-to-Image Diffusion Models

> [!tip] 核心洞察
> 概念嵌入在上下文变化下呈现低秩重尾分布，tMM可有效建模该分布；从分布的高概率区域采样目标嵌入、低概率区域采样锚嵌入，消除了人工锚点选择；AOT将目标分布映射到融合的匿名概念，安全高效；MoE架构天生适应异构领域，NIR通过破坏权重并恢复使模块不可移除。

| 字段 | 内容 |
|------|------|
| 中文题名 | 可扩展的文本到图像扩散模型概念擦除：迈向擦除数千概念 |
| 英文题名 | Erasing Thousands of Concepts: Towards Scalable and Practical Concept Erasure for Text-to-Image Diffusion Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2604.16481) · [Code](https://github.com/GantMan/nsfw_model) · [HuggingFace](https://huggingface.co/black-forest-labs/FLUX.1-dev) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | Erasing Thousands of Concepts (ETC) |
| Dataset | Celebrities, Artistic Style, 50 Celebrities |

> [!tip] 效果简介
> - Celebrities (SDv1.4, 949 target / 325 remain) 上，CRSt↓ 0.099 vs 0.164 (CPE) (↓0.065)。
> - Celebrities (SDv1.4) 上，H0↑ 0.780 vs 0.659 (CPE) (↑0.121)。
> - Artistic Style (SDv1.4, 693 target / 430 remain) 上，CRSt↓ 0.130 vs 0.224 (CPE) (↓0.094)。

## 概要

文本到图像（T2I）扩散模型在创意生成领域展现出强大能力，但也带来了版权侵犯、肖像权滥用和不良内容生成等风险。概念擦除旨在从预训练模型中移除特定概念，同时保持其余概念的生成质量。然而，现有方法面临三个核心瓶颈：**可扩展性不足**——难以同时擦除数千个异构概念；**依赖人工锚点**——需要为每个目标概念手动指定替代概念或锚点；**鲁棒性缺失**——擦除模块可被轻易移除（白盒攻击），导致防护失效。

本文提出 **Erasing Thousands of Concepts (ETC)** 框架，从三个层面系统解决上述问题。其核心洞察在于：概念嵌入在上下文变化下呈现**低秩重尾分布**，传统的单向量操作或高斯混合模型（GMM）无法准确刻画这一特性。ETC 通过以下机制实现大规模、无锚点且防移除的精确擦除：

1. **Student's t 混合模型（tMM）** 对每个概念的低秩嵌入分布进行建模，从高概率区域采样目标嵌入、低概率区域采样锚嵌入，消除了人工锚点选择。
2. **仿射最优传输（AOT）** 将目标概念分布映射到多个概念融合而成的匿名分布，生成安全的新颖特征，避免映射到现有概念可能引发的隐私或质量风险。
3. **混合专家擦除模块（MoEraser）** 采用 GLU 专家和 Top-K 路由，天然适应异构领域的大规模概念擦除；配合**噪声注入-恢复（NIR）训练**，使擦除模块与模型权重深度耦合，移除模块即导致生成能力崩溃。

在覆盖名人、艺术风格、角色等**超过 2,000 个概念**的大规模实验中，ETC 在用户研究中取得了**最低的目标概念保留率（CRSt）和最高的图像质量评分（QS）**，调和指标 $H_0$ 显著优于 CPE、MACE、UCE 等基线方法。在 50 位名人的小规模精确评估中，ETC 达到 $H_0 = 0.943$ 的最优表现。消融实验验证了 tMM 优于 GMM、AOT 优于直接代理映射、结构化噪声在 NIR 中优于全秩/低秩噪声等关键设计选择。

文本到图像扩散模型（如 Stable Diffusion、FLUX）能够根据自然语言描述生成高质量图像，但其强大的生成能力也带来了版权侵犯、肖像权滥用和有害内容生成等风险。例如，模型可以轻易生成名人肖像、模仿受版权保护的艺术风格，或创建特定虚构角色。因此，**概念擦除**（concept erasure）——在不影响无关概念生成质量的前提下，移除模型对特定概念的生成能力——成为安全部署扩散模型的关键技术。

### 现有方法的瓶颈

当前概念擦除方法面临三个核心瓶颈：

**1. 可扩展性不足。** 现有方法（如 FMN、ESD、UCE、MACE、CPE、SAFREE、SPEED）通常针对少量同质概念设计，无法有效扩展到数千个异构概念。当擦除规模增大时，这些方法要么擦除不彻底，要么严重损害无关概念的生成质量。Table 1 从可扩展性、是否可移除、是否需要锚概念三个维度对比了现有方法的属性差异。

**2. 依赖人工锚点选择。** 多数方法需要为每个目标概念人工指定一个“替代概念”（anchor concept）作为擦除后的映射目标。这种启发式选择不仅耗时，而且难以保证替代概念的语义恰当性——选择不当会导致擦除失败或引入新的偏差。

**3. 缺乏防移除鲁棒性。** 现有方法通常将擦除逻辑封装为可插拔模块或微调权重，但面对白盒攻击（如直接移除安全模块），模型会恢复原始生成能力。这使得擦除效果在恶意用户面前形同虚设。

### 本文动机

针对上述瓶颈，本文提出 **Erasing Thousands of Concepts (ETC)** 框架，核心动机包含三个层面：

- **大规模精确擦除**：设计一种能够同时处理数千个异构概念（如名人、艺术风格、虚构角色）的擦除方法，在彻底移除目标概念的同时保持无关概念的生成质量。
- **无锚点擦除**：消除对人工锚点概念的依赖，通过统计建模自动确定擦除边界，实现“精确擦除”（pin-point erasure）。
- **防移除鲁棒性**：构建一种机制，使得擦除模块被移除后模型输出被破坏而非恢复，从根本上抵御白盒攻击。

ETC 的核心洞察在于：概念嵌入在上下文变化下呈现**低秩重尾分布**，利用 Student's t 混合模型（tMM）可有效建模该分布，从而从高概率区域采样目标嵌入、低概率区域采样锚嵌入，实现无锚点的精确擦除。

## 核心方法与创新机理

ETC 的核心创新围绕一个瓶颈展开：**现有概念擦除方法无法扩展到数千个异构概念，且在保持精确擦除（不影响无关概念）的同时缺乏应对白盒攻击（如移除安全模块）的鲁棒性**。为此，ETC 在四个关键维度上对 baseline 进行了系统性改造，形成了一条从“概念分布建模→分布映射→锚点采样→擦除模块训练→鲁棒性加固”的完整因果链。

### 概念分布建模：从点操作到 tMM 分布建模

Baseline 方法（如 **ESD**、**UCE**、**MACE**）通常直接操作单点嵌入向量或线性模块，忽略了概念在上下文变化下呈现的分布特性。ETC 发现概念嵌入在 PCA 降维后呈现**低秩重尾分布**，并首次引入 **Student's t 混合模型（tMM）** 对其进行建模（Eq. 1）：

$$P_c(z) = \sum_{i=1}^{k} \pi_{c,i} \cdot t(z | \mu_{c,i}, \Sigma_{c,i}, \nu_{c,i})$$

这一选择并非随意：与 Gaussian 混合模型（GMM）相比，tMM 的重尾特性更准确地捕捉了概念嵌入在低概率区域的分布形态（Figure 2）。消融实验直接验证了这一点——在 50 位名人擦除任务中，tMM 的 Acc_t 为 0.24，而 GMM 高达 8.96（Table 4），表明 GMM 无法有效区分目标与剩余概念的分布边界，导致擦除精度严重退化。

### 概念映射：从人工锚点对到仿射最优传输（AOT）

传统方法依赖**人工指定目标-替代概念对**（如“特朗普”→“总统”），这不仅需要领域知识，且在大规模场景下不可扩展。ETC 提出**仿射最优传输（AOT）**，将目标概念分布直接映射到一个**融合的匿名概念分布**（由多个随机概念的嵌入合并而成），消除了人工锚点依赖。

AOT 的数学形式为（Eq. 2-3）：

$$T_{p \mapsto q}(z, V_{pq}) = A V_{pq} z + b, \quad z \sim P_p$$

$$(A^*, b^*) \in \arg\min_{A,b} W_2\big( (A V_{pq} z + b)_{\#} P_p, P_q \big)$$

其中 $V_{pq} = V_q V_p^T$ 确保源和目标分布在同一低秩子空间中对齐。相比常规最优传输（OT），AOT 生成的映射特征具有**新颖性和匿名性**——它不是将目标概念映射到某个已知概念，而是映射到一个“不存在”的融合概念，安全性更高（Figure 3）。消融实验证实，AOT 映射在保留剩余概念方面显著优于直接代理映射（Table 4）。

### 锚点选择：从启发式挑选到分布边界采样

Baseline 方法需要**启发式或人工挑选锚点概念**来界定擦除边界。ETC 利用 tMM 的概率密度特性，**从目标分布的高概率区域采样目标嵌入 $z_{\mathrm{tar}}$，从低概率区域采样锚嵌入 $z_{\mathrm{anc}}$**（Eq. 4），无需预设任何锚点概念：

$$z_{\mathrm{tar}} \sim P_{\mathrm{tar}}^{\mathrm{(high)}}, \; z_{\mathrm{anc}} \sim P_{\mathrm{tar}}^{\mathrm{(low)}}, \; z_{\mathrm{map}} = T_{\mathrm{tar \mapsto map}}(z_{\mathrm{tar}})$$

Table 5 的消融表明，从分布边界采样的锚嵌入（fang）或甚至高斯噪声，即可达到与人工锚点相当甚至更优的性能。这一发现从根本上解耦了锚点选择与人工先验的依赖。

### 擦除模块架构：从线性层到 MoEraser（MoE + GLU）

面对数千个异构概念（名人、艺术风格、角色等），单一线性层或前馈网络（FFN）难以同时处理不同领域的擦除需求。ETC 设计了 **MoEraser**——一个基于**混合专家（MoE）** 的擦除模块，每个专家采用 **GLU（Gated Linear Unit）** 激活（Figure 5a），训练目标为（Eq. 5）：

$$\mathcal{L}_{\mathrm{Erase}} = \| W_{\mathrm{proj.}} (\mathrm{MoEraser}(f_{\mathrm{tar}}) + f_{\mathrm{tar}}) - W_{\mathrm{proj.}} f_{\mathrm{map}} \|_2^2 + \lambda \| W_{\mathrm{proj.}} (\mathrm{MoEraser}(f_{\mathrm{anc}}) + f_{\mathrm{anc}}) - W_{\mathrm{proj.}} f_{\mathrm{anc}} \|_2^2$$

消融实验（Table A.5-A.7）显示，MoE 架构在擦除-保留平衡上优于线性层和 FFN（ReLU/GLU），且专家数为 8、Top-6 选择时效果最优。Figure 8 的专家负载热力图进一步证实，不同领域的专家利用均衡，验证了 MoE 对异构概念的天然适应性。

### 鲁棒性策略：从无防护到噪声注入-恢复（NIR）训练

现有方法**缺乏防移除机制**——攻击者可直接删除擦除模块恢复原始模型。ETC 提出**噪声注入-恢复（NIR）训练**：首先向文本嵌入投影矩阵注入沿目标主成分方向的结构化噪声，破坏生成能力（Eq. 6）：

$$W_{\mathrm{cor.}} = W_{\mathrm{proj.}} + \alpha_{\mathrm{noise}} \cdot e p_{\mathrm{tar}}^{\top}$$

随后以冻结的预训练 MoEraser* 为教师，微调模块使其在损坏权重下仍能输出与原始一致的嵌入（Eq. 7）：

$$\mathcal{L}_{\mathrm{NIR}} = \| W_{\mathrm{cor.}} (\mathbf{MoEraser}(f) + f) - W_{\mathrm{proj.}} (\mathbf{MoEraser}^*(f) + f) \|_2^2$$

Figure 4 直观展示了效果：损坏权重后模型无法正常生成图像，必须依赖 MoEraser 恢复。Table 6 的消融表明，结构化噪声在保留剩余概念方面优于全秩和低秩噪声。这一设计使得**移除模块即损坏模型**，从根本上提高了白盒攻击下的鲁棒性。

ETC（Erasing Thousands of Concepts）的整体流程由四个核心阶段构成，形成一条从概念嵌入建模到鲁棒擦除模块部署的完整流水线。框架的输入为目标概念集（如名人、艺术风格、角色）和预训练的文本到图像扩散模型，输出是一个经过微调的擦除模块，该模块插入模型的文本嵌入投影层之后，在推理时实时将目标概念映射为匿名概念，同时保持无关概念的生成质量。

**阶段一：概念分布建模（tMM Concept Distribution Modeler）**。对每个目标概念，首先通过模板提示词（如“a photo of [concept]”）从扩散模型的文本编码器提取嵌入向量，经PCA降维至低秩子空间后，拟合Student's t分布混合模型（tMM），以捕捉概念嵌入在上下文变化下的重尾分布特性（见Eq.(1)）。该阶段输出每个概念的概率密度函数，为后续采样提供精确的分布描述。

**阶段二：仿射最优传输映射（AOT Mapper）**。将多个目标概念分布合并为统一的“映射概念分布”，通过最小化2-Wasserstein距离求解仿射最优传输映射（见Eq.(2)-(3)），将目标分布推前至该匿名融合分布。AOT的关键优势在于生成与任何真实概念均不相似的新颖特征，避免了传统方法中人工指定替代概念的局限。

**阶段三：目标/锚点嵌入采样（Target/Anchor Embedding Sampler）**。从tMM的高概率区域采样目标嵌入$z_{\mathrm{tar}}$，从低概率区域（即分布边界）采样锚嵌入$z_{\mathrm{anc}}$；同时通过AOT将目标嵌入映射为映射嵌入$z_{\mathrm{map}}$（见Eq.(4)）。该采样策略消除了对预定义锚点概念的依赖，使擦除边界自然由目标分布自身划定。

**阶段四：MoEraser训练与NIR鲁棒化**。擦除模块MoEraser采用混合专家（MoE）架构，每个专家为GLU激活的前馈网络，通过Top-K路由机制自适应处理异构领域的概念（见Figure 5a）。训练分两步：首先以擦除损失（Eq.(5)）训练模块，使目标嵌入经过残差连接后逼近映射嵌入，同时保持锚嵌入不变；随后进入噪声注入-恢复（NIR）阶段，向文本嵌入投影矩阵注入沿目标主成分方向的结构化噪声以破坏生成能力（Eq.(6)），再冻结预训练模块作为教师，微调MoEraser使其在损坏权重下仍能恢复原始输出（Eq.(7)）。NIR训练后的模块与模型权重深度耦合，一旦移除模块，模型将无法正常生成图像（见Figure 4），从而抵御白盒移除攻击。

整个流水线的输出是一个轻量级的MoEraser模块，可直接插入扩散模型的文本嵌入投影层之后，在推理时以极小的计算开销实现数千概念的精确擦除。

### 3.1 概念分布建模：Student's t混合模型（tMM）

文本到图像扩散模型中，一个概念（如某位名人、某种艺术风格）通过一系列模板提示（如“a photo of [concept]”）嵌入到文本编码器输出的嵌入空间中。ETC的核心观察是：**概念嵌入在上下文变化下呈现低秩、重尾分布**，传统高斯混合模型（GMM）难以捕捉这种重尾特性，导致擦除与保留的平衡恶化。

为此，ETC对每个概念 $c$ 采用 **Student's t混合模型（tMM）** 建模其嵌入分布：

$$P_c(z) = \sum_{i=1}^{k} \pi_{c,i} \cdot t(z | \mu_{c,i}, \Sigma_{c,i}, \nu_{c,i}) \tag{1}$$

其中：
- $z$ 为经PCA降维后的概念嵌入向量；
- $k$ 为混合成分数；
- $\pi_{c,i}$ 为第 $i$ 个成分的混合权重，满足 $\sum_i \pi_{c,i} = 1$；
- $t(\cdot|\mu, \Sigma, \nu)$ 为多元Student's t分布，$\mu_{c,i}$ 为位置参数，$\Sigma_{c,i}$ 为尺度矩阵，$\nu_{c,i}$ 为自由度参数，控制尾部厚度。

**设计动机**：Student's t分布相较高斯分布具有更厚的尾部，能更准确地刻画概念嵌入在低概率区域的扩散行为。这一性质对后续锚点采样至关重要——低概率区域的嵌入将作为“锚点”，用于界定擦除边界、保护无关概念。消融实验（Table 4）证实，tMM在擦除准确率（Acc_t 0.24）上远优于GMM（Acc_t 8.96），表明GMM建模不足会导致擦除失败。

### 3.2 概念映射：仿射最优传输（AOT）

传统概念擦除方法需人工指定“目标概念→替代概念”的映射对（如将“Taylor Swift”映射到“a person”），这不仅依赖领域知识，且替代概念可能与目标概念存在语义关联，带来安全隐患。ETC通过 **仿射最优传输（AOT）** 实现自动化的匿名概念映射。

给定目标概念分布 $P_{\text{tar}}$ 和一组融合的匿名映射概念分布 $P_{\text{map}}$（通过合并多个无关概念分布并降采样构建），AOT寻找一个仿射变换 $T_{\text{tar} \mapsto \text{map}}$，使推前分布尽可能接近 $P_{\text{map}}$：

$$T_{p \mapsto q}(z, V_{pq}) = A V_{pq} z + b, \quad z \sim P_p \tag{2}$$

$$(A^*, b^*) \in \arg\min_{A,b} W_2\big( (A V_{pq} z + b)_{\#} P_p, P_q \big) \tag{3}$$

其中：
- $V_{pq} = V_q V_p^\top$ 为基变换矩阵，$V_p$、$V_q$ 分别为 $P_p$、$P_q$ 的PCA主成分矩阵，确保两个分布在同一低维子空间中对齐；
- $W_2(\cdot, \cdot)$ 为2-Wasserstein距离，度量两个概率分布之间的最优传输代价；
- $(A V_{pq} z + b)_{\#} P_p$ 表示将 $P_p$ 经仿射变换后的推前分布。

**关键优势**：
1. **安全性**：映射目标 $P_{\text{map}}$ 是多个概念的融合分布，经AOT映射后的嵌入对应一个“匿名”概念，不指向任何真实实体，从根源上杜绝了敏感语义残留（Figure 3定性展示）。
2. **计算高效**：AOT仅需求解仿射参数 $(A, b)$，无需迭代的Sinkhorn算法，适合大规模概念映射。
3. **锚点无关**：映射仅依赖分布自身的统计特性，无需人工指定替代概念。

### 3.3 训练采样与擦除损失

基于tMM和AOT，ETC的训练数据采样完全自动化：

$$z_{\text{tar}} \sim P_{\text{tar}}^{\text{(high)}}, \quad z_{\text{anc}} \sim P_{\text{tar}}^{\text{(low)}}, \quad z_{\text{map}} = T_{\text{tar} \mapsto \text{map}}(z_{\text{tar}}) \tag{4}$$

- **目标嵌入 $z_{\text{tar}}$**：从目标概念tMM的高概率区域采样，代表需被擦除的典型嵌入；
- **锚嵌入 $z_{\text{anc}}$**：从同一tMM的低概率区域（分布边界）采样，代表与目标概念相邻但不应被擦除的嵌入；
- **映射嵌入 $z_{\text{map}}$**：通过AOT将 $z_{\text{tar}}$ 映射到匿名概念分布。

擦除模块 **MoEraser**（混合专家架构，采用GLU激活的专家网络）接收目标/锚嵌入，输出残差向量，训练目标为：

$$\mathcal{L}_{\text{Erase}} = \| W_{\text{proj.}} (\text{MoEraser}(f_{\text{tar}}) + f_{\text{tar}}) - W_{\text{proj.}} f_{\text{map}} \|_2^2 + \lambda \| W_{\text{proj.}} (\text{MoEraser}(f_{\text{anc}}) + f_{\text{anc}}) - W_{\text{proj.}} f_{\text{anc}} \|_2^2 \tag{5}$$

其中：
- $f_{\text{tar}}, f_{\text{anc}}, f_{\text{map}}$ 分别为目标、锚点、映射嵌入的文本编码器输出；
- $W_{\text{proj.}}$ 为文本嵌入到扩散模型条件空间的投影矩阵；
- 第一项强制目标嵌入经MoEraser后接近映射嵌入（擦除），第二项强制锚嵌入经模块后保持不变（保留）；
- $\lambda$ 为保留项权重，平衡擦除与保留。

消融实验（Table 5）表明，从分布边界采样的锚嵌入（记为“fang”）即可达到与人工锚点相当的性能，验证了无锚点设计的有效性。

### 3.4 鲁棒性策略：噪声注入-恢复（NIR）训练

为防止恶意用户直接移除擦除模块以恢复生成能力，ETC引入 **噪声注入-恢复（Noise Injection-Restore, NIR）** 训练。核心思想是：向文本嵌入投影层注入结构化噪声，破坏模型的正常生成能力，然后微调MoEraser以恢复原始输出。这样，移除模块将导致模型输出损坏，无法正常生成。

首先，向投影矩阵注入沿目标概念主成分方向的噪声：

$$W_{\text{cor.}} = W_{\text{proj.}} + \alpha_{\text{noise}} \cdot e p_{\text{tar}}^{\top} \tag{6}$$

其中 $e$ 为随机噪声向量，$p_{\text{tar}}$ 为目标概念嵌入的PCA第一主成分方向，$\alpha_{\text{noise}}$ 控制噪声强度。Figure 4 定性展示：使用损坏权重 $W_{\text{cor.}}$ 后，模型无法生成正常图像。

![[assets/figures/papers/paper_list_l2219_https_arxiv_org_abs_2604_16481/figures/005_Figure_4.jpg]]
*Figure 4: Qualitative rationale on NIR. We generated images with the prompt “a photo of Morgan Freeman” using the original text-embedding projection*

然后，以冻结的预训练MoEraser* 作为教师，微调模块使其在损坏权重下仍能恢复原始输出：

$$\mathcal{L}_{\text{NIR}} = \| W_{\text{cor.}} (\mathbf{MoEraser}(f) + f) - W_{\text{proj.}} (\mathbf{MoEraser}^*(f) + f) \|_2^2 \tag{7}$$

消融实验（Table 6）证实，结构化噪声（沿主成分方向）在保留剩余概念能力上优于全秩噪声和低秩噪声，验证了NIR设计的有效性。

![[assets/figures/papers/paper_list_l2219_https_arxiv_org_abs_2604_16481/figures/006_Figure_5.jpg]]
*Figure 5: MoEraser architecture and training. (a) A MoE with GLU experts scales to heterogeneous domain concepts; training maps*

## 实验与关键发现

### 评估体系设计

ETC 的评估面临一个核心矛盾：自动化指标（如 CLIP Score）在主观性强的领域（艺术风格、角色）可能误判过度擦除或生成质量下降。为此，论文构建了分层评估体系：

- **大规模用户研究**：针对 Celebrities（949 目标/325 剩余）、Artistic Style（693 目标/430 剩余）、Characters（430 目标/261 剩余）三个异构领域，招募 203 名评估者进行 8,120 次判断。每位评估者随机看到 40 张图像，回答两个二元问题——目标概念是否被擦除（CRSt↓ 越好）、剩余概念是否保留（CRSr↑ 越好），以及图像质量是否可接受（QS↑ 越好）。
- **小规模标准化评估**：选取 MACE 公开名单中的 50 位名人，使用 GCD 检测器测量目标/剩余概念的分类准确率（Acc_t↓ / Acc_r↑），辅以 COCO-30K 上的 FID/KID 评估分布级图像质量。
- **联合指标 H₀**：为平衡擦除与保留，定义调和平均 $H_0 = \frac{2}{(1 - \mathrm{CRS}_t)^{-1} + (\mathrm{CRS}_r)^{-1}}$，单一数值反映综合性能。

概念池构建确保目标、映射、剩余三类概念互斥，避免评估偏差。

### 大规模异构概念擦除（主结果）

**Table 2 (Top)** 展示了 SDv1.4 上跨领域大规模擦除的用户研究结果。ETC 在 Celebrities 领域取得 **CRSt=0.099**（CPE 为 0.164，↓0.065），在 Artistic Style 领域取得 **CRSt=0.130**（CPE 为 0.224，↓0.094），擦除能力显著优于所有基线。同时，ETC 在剩余概念保留（CRSr）和图像质量（QS）上匹配或超越免优化的 SAFREE：Celebrities 领域 CRSr=0.688、QS=0.936，Characters 领域 CRSr=0.719、QS=0.919。

综合指标 H₀ 进一步验证了 ETC 的均衡优势——Celebrities 领域 **H₀=0.780**（CPE 为 0.659，↑0.121），Artistic Style 领域 H₀=0.735（CPE 为 0.596），Characters 领域 H₀=0.806（CPE 为 0.728）。值得注意的是，CPE 虽在 Characters 领域 CRSt 最低（0.071），但其 CRSr 和 QS 均大幅落后，表明其擦除以牺牲保留为代价，而 ETC 实现了更精准的靶向擦除。

**Table 2 (Bottom)** 显示 ETC 在 SDv3.5-L 上同样保持优势，验证了方法对先进扩散模型的泛化能力。

### 小规模名人擦除（标准化验证）

**Table 3** 报告了 50 位名人擦除的标准化指标。ETC 取得 **Acc_t=0.24**（CPE 为 0.37，↓0.13），**H₀=0.943**（CPE 为 0.936），在目标擦除和综合平衡上均为最优。在图像质量方面，ETC 的 FID=13.51（CPE 为 14.14）、KID=0.14（CPE 为 0.08），KID 略高于 CPE 但仍属低值，且其他指标全面领先，说明 ETC 在更强擦除的同时保持了可比的生成质量。

### 消融实验

#### 分布建模与映射策略（Table 4）

![[assets/figures/papers/paper_list_l2219_https_arxiv_org_abs_2604_16481/figures/012_Table_4.jpg]]
*Table 4: Ablation on distribution modeling and AOT mapping. Direct mapping effectively removes target concepts but fails to preserve remaining ones. GMM performs poorly in both erasure and preservation, suggesting its modeling is ill-suited for this task. While the surrogate mapping achieves strong erasure but weak preservation, combining tMM with AOT yields the best overall*

**Table 4** 揭示了两个关键设计选择的效果：

- **tMM vs GMM**：将 tMM 替换为 GMM 后，Acc_t 从 0.24 飙升至 8.96，擦除能力几乎完全丧失。这表明高斯混合模型无法捕捉概念嵌入的重尾特性，导致目标分布建模失真。
- **AOT vs 直接代理映射**：直接映射虽能有效擦除目标（Acc_t=0.14），但 Acc_r 大幅下降，说明其破坏了剩余概念的嵌入空间。AOT 通过将目标分布映射到融合的匿名概念，在擦除与保留间取得更优平衡。

#### 锚点采样策略（Table 5）

![[assets/figures/papers/paper_list_l2219_https_arxiv_org_abs_2604_16481/figures/014_Table_5.jpg]]
*Table 5: Ablation study on the type of anchor samples. We conducted ablation studies on several variants used as anchors and confirm that using embeddings sampled from the distribution boundary or Gaussian noise achieves performance comparable to or better than that obtained with anchor concepts*

**Table 5** 消融了锚嵌入的来源。从目标分布边界（低概率区域）采样的嵌入（记为 fang）或直接使用高斯噪声，均能达到与人工指定锚概念相当甚至更好的性能。这一结果验证了 tMM 建模使锚点选择自动化的核心主张——无需预设“安全”概念即可界定擦除边界。

#### MoEraser 架构（Table A.5–A.7）

附录消融表明：MoE 架构显著优于等参数量线性层、ReLU-FFN 和 GLU-FFN；专家数设为 8、Top-6 路由选择在性能与效率间取得最佳平衡。**Figure 8** 的专家负载热力图显示跨域负载均衡，说明 MoE 天生适应异构领域。

![[assets/figures/papers/paper_list_l2219_https_arxiv_org_abs_2604_16481/figures/013_Figure_8.jpg]]
*Figure 8: Load heatmap of experts. We visualize the frequency ratio of selection of each expert for three domains where each column represents an expert, and each row corresponds to a domain. The relatively uniform load distribution across experts suggests that the router network effectively balances expert utilization*

#### NIR 噪声结构（Table 6）

**Table 6** 对比了全秩、低秩和结构化噪声在 NIR 中的效果。三种噪声在移除 MoEraser 后对目标概念的破坏程度相近，但结构化噪声（沿目标主成分方向注入）在保留剩余概念上显著优于全秩/低秩噪声。这解释了为何 ETC 选择 $W_{\mathrm{cor.}} = W_{\mathrm{proj.}} + \alpha_{\mathrm{noise}} \cdot e p_{\mathrm{tar}}^{\top}$ 的注入方式——它精准破坏目标相关通路，最小化对无关概念的附带损伤。

### 失败模式与局限性

尽管 ETC 在规模化擦除上表现突出，仍存在以下边界：

1. **提示级对抗攻击**：tMM 建模提供的分布鲁棒性主要针对权重级攻击（移除模块），面对精心设计的对抗性提示可能被绕过，需要手动验证具体攻击场景下的表现。
2. **映射概念选择依赖启发式**：当前基于余弦相似度和方差的筛选方法缺乏理论保证，映射概念的质量直接影响擦除效果——若映射概念与目标概念嵌入空间过近，可能导致擦除不彻底。
3. **安全关键领域泛化未验证**：实验聚焦于版权/肖像权敏感概念（名人、风格、角色），对暴力、仇恨等显式安全内容的有效性尚待独立研究。
4. **KID 指标的轻微劣势**：在 50 位名人擦除中，ETC 的 KID 略高于 CPE（0.14 vs 0.08），提示在极端保留要求下可能需要额外校准。

![[assets/figures/papers/paper_list_l2219_https_arxiv_org_abs_2604_16481/figures/007_Table_2.jpg]]
*Table 2: Quantitative results across diverse domains using SDv1.4 (Top) and SDv3.5 (Bottom). We report the user study “Yes” rate for concept preservation (CRS) and image quality (QS) for both target and remaining concepts on three domains - Celebrities, Artistic Styles, and Characters. To jointly evaluate target concept removal and preservation of remaining concepts, we provide the harmonic mean metric H0. Numbers in parentheses indicate the number of concepts. ↑ / ↓ indicates that higher/lower values correspond to better performance*

## 定位与知识库关联

### 1. 问题瓶颈与ETC的因果杠杆

现有概念擦除方法面临三个核心瓶颈：（1）**可扩展性不足**——多数方法针对少量同质概念设计，面对数千个异构概念时擦除精度和保留能力急剧下降；（2）**依赖人工锚点**——需要预设“目标-替代”概念对或启发式选择锚概念，限制了大规模自动化部署；（3）**缺乏防移除鲁棒性**——擦除模块可被用户直接删除或替换，导致擦除失效。ETC通过三个因果杠杆系统性地解决了上述问题：**Student's t混合模型（tMM）** 建模概念嵌入的低秩重尾分布，消除了对固定嵌入向量的依赖；**仿射最优传输（AOT）** 将目标分布映射到融合的匿名概念分布，无需人工指定替代概念；**噪声注入-恢复（NIR）训练** 使擦除模块与模型权重深度耦合，移除模块即损坏生成能力。

### 2. 方法谱系中的定位

ETC在概念擦除方法谱系中占据“大规模、无锚点、防移除”的独特位置。Table 1的系统对比揭示了这一差异：

- **FMN**和**ESD**通过操作交叉注意力或对齐嵌入实现擦除，但缺乏可扩展性且依赖锚概念；
- **UCE**引入封闭形式更新提升效率，但仍需锚概念且不可防移除；
- **MACE**和**CPE**分别采用LoRA模块和非线性擦除模块提升可扩展性，但MACE依赖锚概念，CPE虽无需锚概念却不可防移除；
- **SAFREE**和**SPEED**作为免优化方法，虽无需训练但擦除精度在大规模场景下显著下降。

ETC是唯一同时满足“可扩展至数千概念”、“无需锚概念”、“防移除”三个属性的方法。其核心差异源于方法论的范式转换：从“操作嵌入向量”转向“建模概念分布”，从“点对点映射”转向“分布间最优传输”，从“附加模块”转向“耦合权重”。

### 3. 关键设计选择的消融证据

**tMM vs. GMM（Table 4）**：在50位名人擦除任务中，tMM建模使目标识别准确率（Acc_t）从GMM的8.96骤降至0.24，同时保留概念准确率（Acc_r）从83.21提升至95.83。这一显著差异源于概念嵌入在上下文变化下呈现重尾分布（Figure 2），GMM的高斯假设无法准确捕捉低概率区域的锚嵌入，导致保留能力受损。

**AOT vs. 直接代理映射（Table 4）**：AOT映射在保留能力上显著优于直接映射（Acc_r 95.83 vs. 91.56），因为AOT生成的匿名特征（Figure 3）位于多个映射概念分布的融合区域，既避免了与剩余概念的冲突，又防止了通过逆向工程恢复目标概念。

**锚点采样策略（Table 5）**：从目标分布低概率区域采样的锚嵌入（fang）与人工锚点性能相当（Acc_t 0.24 vs. 0.24, Acc_r 95.83 vs. 95.67），甚至高斯噪声采样也表现接近（Acc_t 0.22, Acc_r 95.37）。这验证了“分布边界即天然锚点”的核心洞察，使大规模擦除无需人工制定锚概念。

**MoE架构选择（Table A.5-A.7）**：MoEraser采用GLU专家的MoE架构，在擦除-保留平衡上优于线性层和前馈网络。专家数为8、Top-6选择时达到最佳均衡，且跨域专家负载热力图（Figure 8）显示各专家利用均衡，验证了MoE对异构领域的天然适应性。

**NIR噪声结构（Table 6）**：结构化噪声（沿目标主成分方向注入）在保留剩余概念能力上优于全秩和低秩噪声，因为结构化噪声精准破坏目标概念相关的投影方向，而NIR训练强制MoEraser学习恢复这些方向，形成不可分离的耦合。

### 4. 适用边界与局限

尽管ETC在大规模概念擦除上表现优异，其适用边界需谨慎界定：

**概念类型边界**：当前验证集中于名人、艺术风格、角色等版权/肖像权敏感概念。对于暴力、仇恨等显式安全内容，概念嵌入的分布特性可能不同，tMM建模的有效性尚待验证。此外，映射概念的选择对擦除效果至关重要，当前基于余弦相似度和方差的启发式方法缺乏理论最优性保证。

**攻击鲁棒性边界**：NIR训练使物理移除模块不可行，但面对基于提示的对抗性攻击（如精心设计的提示工程绕过擦除）仍可能失效。tMM建模本身提供一定统计鲁棒性，但未针对梯度逆向等自适应攻击进行专门防御。

**规模边界**：已验证规模为2,072个概念（SDv1.4）和515个概念（SDv3.5-L）。扩展到数万概念时，tMM的自由度、成分数等超参数是否需要逐概念优化，以及MoEraser的推理效率是否仍可保持，尚缺乏实验证据。

**潜在滥用风险**：该方法可能被恶意用于移除关键信息或不加区分地擦除导致模型性能下降，需要在实际部署中引入使用控制机制。

### 5. 开放问题

1. **跨安全领域泛化**：能否将分布建模-最优传输-NIR训练框架扩展到显式内容、暴力、仇恨等安全关键领域？这些领域的概念嵌入分布是否同样呈现低秩重尾特性？

2. **映射概念自适应选择**：如何实现映射概念的自动化、自适应选择？当前需要预设映射概念池，未来可探索基于语义空间密度估计或主动学习的映射概念发现方法。

3. **更强攻击下的鲁棒性**：面对梯度逆向、模型窃取等更强自适应攻击时，NIR训练的防移除能力是否仍然有效？是否需要引入对抗训练或密码学级别的保护机制？

4. **超大规模效率**：在数万概念规模下，tMM的逐概念拟合、AOT的分布间映射、MoEraser的专家路由是否仍能保持可接受的训练与推理效率？是否需要引入层次化概念分组或分布式训练策略？

5. **tMM超参数自适应**：当前tMM的自由度ν和成分数k可能需针对每个概念独立优化，是否存在数据驱动的自适应选择策略，或跨概念的参数共享机制？

## 原文 PDF

![[paperPDFs/CVPR_2026/Erasing_Thousands_of_Concepts_Towards_Scalable_and_Practical_Concept_Erasure_for_Text_to_Image_Diffusion_Models.pdf]]
