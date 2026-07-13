---
title: All-in-One Slider for Attribute Manipulation in Diffusion Models
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/All_in_One_Slider_for_Attribute_Manipulation_in_Diffusion_Models.pdf
project_link: null
code_link: null
aliases:
- AOS
- AOSAMDM
tags:
- CVPR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 在文本编码器的中间层表征上构建属性稀疏自编码器（Attribute Sparse Autoencoder），通过Top‑k稀疏激活强制将稠密、纠缠的嵌入空间分解为共享的、语义可解耦的稀疏潜在空间（Attribute Latent Space），使不同属性对应独立且可复用的方向。
primary_logic: 以“先分解、再重构”的理念，利用单次训练的稀疏自编码器构建一个所有属性共享的高维稀疏可解释潜在空间；该空间中的方向天然解耦，仅通过调整对应方向的激活系数即可用同一轻量模块实现多属性的连续、组合操控以及零样本泛化。
claims:
- 在单属性设置中，本方法在 Old 和 Makeup 的 IS（身份一致性）上分别达到 0.7155 和 0.7423，均高于 ConceptSlider 和 AttControl。
- 在多属性组合（Old+Smile、Old+Makeup、Smile+Makeup）下，本方法的 QS（语义对齐分数）均为最高（4.2124、4.4281、4.2973），展现了强大的组合控制能力。
- SAE 导出的稀疏方向在所有属性上均优于直接添加原始文本嵌入，平均 QS 从 3.990 提升至 4.202，平均 IS 从 0.502 提升至 0.698。
- 几何编辑的线性度 R² 达 0.973，高于 ConceptSlider（0.966）和 AttControl（0.962），证实更精确的连续控制。
---

# All-in-One Slider for Attribute Manipulation in Diffusion Models

> [!tip] 核心洞察
> 以“先分解、再重构”的理念，利用单次训练的稀疏自编码器构建一个所有属性共享的高维稀疏可解释潜在空间；该空间中的方向天然解耦，仅通过调整对应方向的激活系数即可用同一轻量模块实现多属性的连续、组合操控以及零样本泛化。

| 字段 | 内容 |
|------|------|
| 中文题名 | 扩散模型中属性操控的一体式滑块 |
| 英文题名 | All-in-One Slider for Attribute Manipulation in Diffusion Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2508.19195) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | All-in-One Slider |
| Dataset | 52 种面部属性的 T2I 生成（Old, Smile, Makeup 等）, 多属性组合（Old+Smile, Old+Makeup, Smile+Makeup）, 原始嵌入 vs 稀疏方向（Old, Smile, Makeup） |

> [!tip] 效果简介
> - 52 种面部属性的 T2I 生成（Old, Smile, Makeup 等） 上，QS (Action Fidelity) / IS (Identity Consistency) Old QS/IS: 4.0490/0.7155; Smile QS/IS: 4.2647/0.6366; Makeup QS/IS: 4.2908/0.74... vs ConceptSlider Old QS/IS: 3.7941/0.4336; AttControl Old QS/IS: 4.0392/0.6005 (IS 提升 0.115 ~ 0.2819)。
> - 多属性组合（Old+Smile, Old+Makeup, Smile+Makeup） 上，QS / IS Old+Smile QS/IS: 4.2124/0.6882; Old+Makeup QS/IS: 4.4281/0.6277; Smile+Makeup Q... vs ConceptSlider Old+Smile QS/IS: 4.1503/0.4993; AttControl Old+Smile QS/IS: 3.666... (QS 提升 0.0621 ~ 0.3726，IS 明显提升)。
> - 原始嵌入 vs 稀疏方向（Old, Smile, Makeup） 上，QS ↑ / IS ↑ Avg QS: 4.202; Avg IS: 0.698 vs Embraw Avg QS: 3.990; Avg IS: 0.502 (QS +0.212, IS +0.196)。

## 概要

扩散模型在文本到图像生成中展现了卓越的能力，但对生成图像中的特定属性进行**连续、精细且可组合的操控**仍是一个核心挑战。现有主流方法遵循**“一对一”（One-for-One）范式**：为每个目标属性（如“微笑”“衰老”）单独训练一个轻量级适配模块（如 LoRA 或方向向量），再将缩放后的嵌入注入生成过程。这一范式存在三个结构性瓶颈：

1. **参数冗余与不可扩展性**：每新增一个属性都需要重新训练一个独立模块，导致模型库快速膨胀。
2. **语义纠缠**：文本嵌入空间中不同属性的语义高度耦合，直接在该空间施加方向向量难以实现纯净、无冲突的操控。
3. **组合操控困难**：多个独立训练的模块在同时作用时缺乏协调机制，容易产生身份漂移或属性冲突。

针对上述问题，本文提出 **All-in-One Slider**，一个**轻量、统一、可复用**的属性操控框架。其核心思想是**“先分解、再重构”**：在文本编码器的中间层表征上训练一个**属性稀疏自编码器（Attribute Sparse Autoencoder）**，通过 Top‑k 稀疏激活将稠密、纠缠的嵌入空间强制分解为一个共享的、语义可解耦的**属性潜在空间（Attribute Latent Space）**。在该空间中，不同属性天然对应独立且可复用的稀疏方向，仅需调整对应方向的激活系数，即可用**同一个模块**实现多属性的连续操控、组合操控以及零样本泛化。

该方法的核心贡献可概括为三点（参见 Figure 1）：

- **细粒度连续控制**：通过缩放因子 λ 在属性潜在空间中平滑插值，实现从“无编辑”到“充分表达”的连续过渡，且对身份和其他属性干扰极小。
- **多属性组合操控**：同一稀疏空间中的不同方向天然解耦，可同时激活多个属性方向而互不冲突，实现连贯的组合编辑。
- **零样本泛化**：稀疏自编码器学习到的分解能力不绑定于特定属性词——对训练中未见过的属性（如特定种族、名人身份），只需提供其文本描述即可直接导出操控方向，无需任何额外训练。

在方法谱系上，All-in-One Slider 区别于 ConceptSlider 和 AttControl 等“一对一”滑块方法，通过**共享的稀疏潜在空间**替代了为每个属性独立训练模块的方案。其技术路线融合了稀疏自编码器在语言模型可解释性中的成功经验，将其迁移至扩散模型的文本条件空间，构建了一个参数高效、语义可解释的属性操控基座。

实验在 52 种面部属性的文本到图像生成任务上进行验证。定量结果表明：在单属性设置中，All-in-One Slider 在身份一致性（IS）上显著优于对比方法——例如在“衰老”属性上 IS 达到 0.7155，较 AttControl 提升约 0.115，较 ConceptSlider 提升约 0.282（Table 1）。在多属性组合场景下，本方法在所有组合上的语义对齐分数（QS）均为最高，展现了强大的组合控制能力。稀疏方向与原始嵌入的对比实验进一步证实，SAE 导出的稀疏方向平均 QS 提升 0.212、IS 提升 0.196（Table 3），验证了稀疏解耦提取了更纯净的语义信号。几何编辑线性度评估中，本方法的 R² 达 0.973，优于对比方法，证实了更精确的连续控制能力（Figure 14）。

方法的局限性同样值得关注：训练稀疏自编码器需要覆盖多样化属性的文本提示语料，引入新属性仍需构造提示集；潜在维度高达 32768，训练约需 400M 词元，对计算资源有一定要求；目前验证主要集中于面部属性和有限摄影风格，对更通用的物体属性或复杂场景编辑的泛化性尚未充分评估。



扩散模型在文本到图像（T2I）生成领域取得了显著进展，使高质量、多样化的图像合成成为可能。然而，对这些模型进行**精细、连续且可组合的属性操控**仍是一个核心挑战。用户往往希望在不影响主体身份和其他无关属性的前提下，对生成图像中的特定语义属性（如面部年龄、表情、妆容，或摄影风格）进行平滑调节。

现有方法普遍遵循**“一对一”（One-for-One）范式**：为每一个目标属性独立训练一个操控模块，例如学习特定的低秩适配器（LoRA）、属性向量或方向。这种范式存在三个根本性瓶颈：

1. **参数冗余与不可扩展性**：每新增一个属性就需要重新训练一个专用模块，导致参数量的线性增长，无法支持大规模属性集的灵活操控。
2. **零样本操控的缺失**：一对一方法天然无法泛化到训练中未见过的属性，限制了其在开放场景中的应用。
3. **语义纠缠与组合困难**：文本编码器的嵌入空间本质上是稠密且高度纠缠的。直接在该空间中学习属性方向，难以保证不同属性之间的解耦，导致多属性组合操控时出现语义冲突、身份漂移或编辑效果相互干扰。

上述瓶颈的根源在于，现有方法缺乏一个**共享的、语义可解耦的潜在空间**来统一表征和操控多样化的属性。因此，本文的核心动机是：**能否构建一个一次性训练、即可支持任意属性连续操控的统一框架，从根本上打破“一对一”范式的限制？** 这要求在文本嵌入空间中实现属性的稀疏解耦，使得不同属性对应独立且可复用的方向，从而支持灵活的连续调节、多属性组合以及零样本泛化。



## 核心方法与创新机理

### 瓶颈洞察：从“一对一”到“一体式”的范式跃迁

现有基于扩散模型的属性操控方法普遍遵循 **One-for-One** 范式：为每一个属性（如“微笑”、“衰老”）独立训练一个专用的滑块模块（LoRA、适配器或方向向量）。这一范式存在三个根本性缺陷：其一，**参数冗余且不可扩展**——每新增一个属性都需要重新训练，导致模型规模随属性数量线性增长；其二，**不支持零样本操控**——训练时未见过的属性完全无法编辑；其三，**组合操控能力薄弱**——独立训练的多个属性方向在语义空间中相互纠缠，叠加使用时极易产生冲突或非预期的外观变化。

上述问题的深层根源在于**文本嵌入空间的语义纠缠**。扩散模型的条件编码器（如 CLIP 文本编码器）将属性语义压缩在稠密、高维的连续向量中，不同属性的信息高度耦合，缺乏显式的解耦结构。直接在该空间中学习属性方向，本质上是在一个“黑箱”中进行启发式搜索，难以保证方向的纯净性和独立性。

### 因果机制：属性稀疏自编码器构建解耦潜在空间

本工作的核心创新在于提出 **All-in-One Slider**，通过**属性稀疏自编码器（Attribute Sparse Autoencoder, SAE）** 在文本编码器的中间层表征上构建一个共享的、语义可解耦的稀疏潜在空间（称为 Attribute Latent Space）。其因果机制可概括为“先分解、再重构”：

1. **稀疏分解**：SAE 的编码器将稠密的文本嵌入 $x$ 映射到高维稀疏潜在空间，通过 ReLU 激活和 Top‑k 选择仅保留激活最强的 $k$ 个神经元，强制将纠缠的语义信息分解为稀疏、独立的特征分量：
   $$z_{\mathrm{ALS}} = \mathrm{Top}{-}k\left( \mathrm{ReLU}( W_{\mathrm{enc}} (x - b_{\mathrm{pre}}) + b_{\mathrm{enc}} ) \right) \tag{1}$$

2. **解耦重构**：解码器从稀疏代码 $z_{\mathrm{ALS}}$ 重建原始嵌入 $\hat{x}$，并通过 MSE 重建损失与辅助损失（复活“死亡神经元”）联合训练：
   $$\hat{x} = W_{\mathrm{dec}} z_{\mathrm{ALS}} + b_{\mathrm{pre}} \tag{2}$$
   $$\mathcal{L} = \| x - \hat{x} \|_2^2 + \alpha \mathcal{L}_{\mathrm{aux}} \tag{5}$$

3. **属性操控**：推理时，将目标属性的文本 $x_{\mathrm{A}}$ 输入 SAE 得到稀疏代码，缩放后解码并与原提示嵌入相加，实现连续控制：
   $$x_{\mathrm{manipulated}} = x + W_{\mathrm{dec}} \big( \lambda \times \mathrm{ENC}(x_{\mathrm{A}}) \big) \tag{6}$$

该机制的核心因果杠杆在于：**Top‑k 稀疏激活强制每个属性仅激活潜在空间中极少数特定的神经元**，从而自然形成独立、可复用的属性方向。不同属性的方向在稀疏空间中互不干扰，叠加时也不会产生冲突——这正是组合操控和零样本泛化的结构基础。

### 与 Baseline 的关键差异（Changed Slots）

| 设计维度 | One-for-One 基线（ConceptSlider / AttControl） | All-in-One Slider（本方法） |
|:---|:---|:---|
| **属性表征方案** | 为每个属性独立训练 LoRA、适配器或方向向量；单次操控仅针对一个属性。 | 训练一个统一的属性稀疏自编码器，以 Top‑k 稀疏激活在共享的高维潜在空间中建立所有属性的解耦方向。 |
| **操控机制** | 将缩放后的原始文本嵌入或学习到的属性向量直接注入提示。 | 将目标属性文本编码为稀疏代码，缩放后通过解码器解码，再与原始提示嵌入相加（公式 6）。 |
| **可扩展性** | 属性数量增加需要重新训练新模块，参数线性增长。 | 单次训练即可覆盖所有已见属性，并支持未见属性的零样本操控。 |
| **组合操控** | 多属性叠加时方向相互干扰，语义冲突明显。 | 稀疏解耦方向天然兼容，叠加操控连贯且无冲突。 |

### 创新层级的定位

本方法并非对现有滑块方法的增量改进，而是在**表征层面**进行了范式重构：将属性操控问题从“在稠密嵌入空间中搜索方向”转化为“在稀疏解耦空间中激活方向”。这一转变使得原本需要 $N$ 次训练的 $N$ 个属性操控任务，被统一为一次 SAE 训练即可完成的基础设施构建。由此衍生出的零样本泛化能力（如操控训练未见过的种族属性）和组合操控能力（如同时编辑“衰老+微笑”），在 One-for-One 范式下是难以实现的。

> **需注意**：当前分析基于论文提供的实验证据和架构描述。零样本泛化的边界（对生僻或长尾属性的退化程度）以及稀疏空间的可解释性（每个维度对应的具体视觉特征）仍需进一步验证。



All-in-One Slider 的整体框架遵循“先分解、再重构”的两阶段范式，其核心瓶颈在于文本嵌入空间的高度语义纠缠导致现有 One-for-One 方法无法实现可扩展的多属性操控。该方法通过一个统一的**属性稀疏自编码器**（Attribute Sparse Autoencoder）在单次训练中构建所有属性共享的稀疏可解释潜在空间，从而将稠密纠缠的嵌入分解为独立且可复用的语义方向。

### 两阶段流水线

如图 3 所示，框架由两个关键阶段构成：

**阶段一：属性稀疏自编码器的无监督训练。** 该阶段从 SDXL 双文本编码器的中间层（第 11 层和第 29 层）提取隐藏状态作为训练输入。编码器通过线性变换、ReLU 激活和 Top‑k 稀疏选择将嵌入映射到高维稀疏潜在空间，解码器则从稀疏代码重建原始嵌入。训练目标结合了重建损失与辅助损失，以缓解死神经元问题并强制稀疏性。

**阶段二：基于稀疏编码的属性操控。** 推理时，将目标属性的文本提示输入训练好的自编码器，得到其稀疏潜在代码；对该代码施加缩放因子 λ 后通过解码器解码为嵌入空间的偏移向量，再与原始提示嵌入相加，最终输入扩散模型（SDXL）的交叉注意力层以指导图像生成。这一机制使得同一轻量模块仅通过调整对应方向的激活系数即可实现多属性的连续、组合操控。

### 模块关系与数据流

框架包含以下核心模块，按数据流顺序串联：

1. **文本嵌入提取模块**：从 SDXL 双编码器的残差流中截取中间层词元嵌入，作为自编码器的输入特征。
2. **属性稀疏自编码器**：
   - **线性编码器 + Top‑k 稀疏选择**：将输入嵌入 $x$ 映射为稀疏潜在代码 $z_{\mathrm{ALS}} = \mathrm{Top}{-}k( \mathrm{ReLU}( W_{\mathrm{enc}} (x - b_{\mathrm{pre}}) + b_{\mathrm{enc}} ) )$，仅保留激活最强的 $k$ 个神经元。
   - **线性解码器**：从稀疏代码重建嵌入 $\hat{x} = W_{\mathrm{dec}} z_{\mathrm{ALS}} + b_{\mathrm{pre}}$。
   - **训练损失**：$\mathcal{L} = \mathcal{L}_{\mathrm{mse}} + \alpha \mathcal{L}_{\mathrm{aux}}$，其中 $\mathcal{L}_{\mathrm{mse}} = \| x - \hat{x} \|_2^2$，辅助损失 $\mathcal{L}_{\mathrm{aux}}$ 通过额外的 Top‑k 选择复活欠活跃神经元。
3. **属性操控模块**：对目标属性 $A$ 的文本嵌入 $x_A$ 执行编码-缩放-解码操作，生成操控后的嵌入 $x_{\mathrm{manipulated}} = x + W_{\mathrm{dec}} ( \lambda \times \mathrm{ENC}(x_A) )$。
4. **扩散图像生成器**（SDXL）：以操控后的嵌入作为条件，通过交叉注意力指导 50 步采样过程（分类器自由引导尺度 7.5），生成最终编辑图像。

### 关键设计决策

- **中间层表征的选择**：消融实验（Table 2）表明，选择编码器第 10/28 层在所有属性上取得最佳整体平衡，深层对语义和身份信息的保存更有利。
- **稀疏性的因果作用**：Top‑k 稀疏激活是属性解耦的核心机制——它强制将稠密嵌入空间分解为语义可分离的稀疏方向，使得不同属性对应独立且可复用的潜在维度。Table 3 的对比证实，SAE 导出的稀疏方向在所有属性上均显著优于直接添加原始文本嵌入（平均 QS 从 3.990 提升至 4.202，平均 IS 从 0.502 提升至 0.698）。
- **操控强度的连续控制**：缩放因子 λ 在 0.15~0.30 范围内可实现从欠编辑到充分表达属性的平滑过渡（Figure 11），且几何编辑的线性度 R² 达 0.973（Figure 14），证实了更精确的连续控制能力。

该框架的参数效率极高——仅需训练一个轻量的线性自编码器（潜在维度 32768，约 400M 词元训练），即可替代传统 One-for-One 范式下为每个属性单独训练的多个 LoRA 或适配器模块。

### 补充图表

![[assets/figures/papers/paper_list_l2439_https_arxiv_org_abs_2508_19195/figures/001_Figure_1.jpg]]
*Figure 1: Our All-in-One Slider shows advantages in: (1) Finegrained and continuous control over desired attribute, without affecting other attributes (e.g., subject identity and appearance). (2) Combination of multiple facial attributes (e.g., smile and age) for consistent and conflict-free transformations. (3) Zero-shot generalization to unseen attributes, without multiple and cumbersome training processes*

![[assets/figures/papers/paper_list_l2439_https_arxiv_org_abs_2508_19195/figures/002_Figure_2.jpg]]
*Figure 2: (1) Existing One-for-One slider methods require training a specific slider module for each attribute. (2) Our All-in-One slider only needs training once to obtain a unified and disentangled latent space for various attributes, supporting the flexible manipulation of multiple diverse attributes*

![[assets/figures/papers/paper_list_l2439_https_arxiv_org_abs_2508_19195/figures/003_Figure_3.jpg]]
*Figure 3: An overview of our All-in-One Slider framework. Stage 1: Unsupervised training of Attribute Sparse Autoencoder, which takes intermediate token embeddings from the residual stream in the text encoder as input and aims to reconstruct them with sparse features. Stage 2: Applying the trained Attribute Sparse Autoencoder to flexibly manipulate specific attributes during the image generation process*

![[assets/figures/papers/paper_list_l2439_https_arxiv_org_abs_2508_19195/figures/006_Figure_6.jpg]]
*Figure 6: Real image editing. We apply our method to edit Smile (top) and Old (bottom) attributes using the ReNoise inversion framework [15]. Compared to AttControl, our method better preserves identity details like eyeglasses and facial structure*

![[assets/figures/papers/paper_list_l2439_https_arxiv_org_abs_2508_19195/figures/011_Figure_10.jpg]]
*Figure 10: (a) Framework for fine-tuning multi-subject manipulation. The Attribute Sparse Autoencoder is fine-tuned using paired sentences combined the diffusion model, and we introduce an Attpooling Aggregator (AAg) module to locate the target subject for manipulation. (b) Qualitative results of applying attributes to the targeted subject (e.g., old to the man, smile to the woman)*



### 整体框架

All-in-One Slider 的核心架构是一个高度参数高效的**属性稀疏自编码器（Attribute Sparse Autoencoder）**，整体分为两个阶段（Figure 3）：

1. **阶段一：无监督训练**——从文本编码器中间层的词元嵌入中学习稀疏潜在表征；
2. **阶段二：属性操控**——通过修改稀疏潜在编码来操控扩散生成过程。

### 文本嵌入提取

训练输入并非文本编码器的最终输出，而是从 SDXL 双文本编码器的**残差流中间层**提取隐藏状态。具体选取第一个编码器的第 11 层和第二个编码器的第 29 层（Table 2 消融证实该组合在所有属性上取得最佳整体平衡）。深层表征对语义和身份信息的保存更有利。

### 属性稀疏自编码器

自编码器由**线性编码器**和**线性解码器**组成，核心机制是通过 Top‑k 稀疏激活将稠密、纠缠的嵌入空间强制分解为共享的、语义可解耦的稀疏潜在空间（Attribute Latent Space）。

#### 稀疏编码（Sparse Encoding）

给定提取的文本嵌入 $x$，编码器首先减去预置偏置 $b_{\text{pre}}$，经线性变换 $W_{\text{enc}}$ 和偏置 $b_{\text{enc}}$ 后，通过 ReLU 激活并仅保留激活最强的 $k$ 个神经元：

$$z_{\text{ALS}} = \text{Top-}k\left( \text{ReLU}( W_{\text{enc}} (x - b_{\text{pre}}) + b_{\text{enc}} ) \right) \tag{1}$$

- $x$：从文本编码器中间层提取的原始嵌入向量
- $W_{\text{enc}}$：编码器权重矩阵
- $b_{\text{pre}}$：预置偏置（pre-encoder bias）
- $b_{\text{enc}}$：编码器偏置
- $z_{\text{ALS}}$：稀疏潜在代码（Attribute Latent Space 中的表征）
- $\text{Top-}k(\cdot)$：仅保留激活值最大的 $k$ 个维度，其余置零

#### 解码器重构（Decoder Reconstruction）

解码器将稀疏代码 $z_{\text{ALS}}$ 映射回原始嵌入空间：

$$\hat{x} = W_{\text{dec}} z_{\text{ALS}} + b_{\text{pre}} \tag{2}$$

- $W_{\text{dec}}$：解码器权重矩阵
- $\hat{x}$：重构后的嵌入向量
- 注意解码器同样使用 $b_{\text{pre}}$ 作为偏置，与编码器的预置偏置共享

#### 重建损失（Reconstruction Loss）

最小化原始嵌入与重建嵌入的均方误差：

$$\mathcal{L}_{\text{mse}} = \| x - \hat{x} \|_2^2 \tag{3}$$

#### 辅助稀疏损失（Auxiliary Loss）

为缓解训练中神经元“死亡”（长期不被激活）的问题，引入辅助 Top‑k 机制。使用较小的 $k_{\text{aux}}$ 选择当前欠活跃的神经元，以其重建残差：

$$\hat{z}_{\text{ALS}} = \text{Top-}k_{\text{aux}}\left( \text{ReLU}( W_{\text{enc}} (x - b_{\text{pre}}) + b_{\text{enc}} ) \right) \tag{4}$$

辅助损失 $\mathcal{L}_{\text{aux}}$ 同样基于 MSE，但作用于残差重建，促使死亡神经元复活。

#### 最终训练目标

$$\mathcal{L} = \mathcal{L}_{\text{mse}} + \alpha \mathcal{L}_{\text{aux}} \tag{5}$$

- $\alpha$：控制辅助损失权重的超参数

### 属性操控模块（推理阶段）

训练完成后，自编码器中的稀疏方向天然解耦——不同属性对应独立且可复用的方向。推理时，将目标属性 $A$ 的文本描述输入编码器得到稀疏代码，经缩放因子 $\lambda$ 缩放后解码，再与原始提示嵌入相加：

$$x_{\text{manipulated}} = x + W_{\text{dec}} \big( \lambda \times \text{ENC}(x_A) \big) \tag{6}$$

- $x_A$：目标属性 $A$ 对应文本的嵌入
- $\text{ENC}(\cdot)$：编码器前向过程（含 Top‑k 稀疏选择）
- $\lambda$：操控强度，控制属性表达程度
- $x_{\text{manipulated}}$：操控后的文本嵌入，作为扩散模型的条件输入

消融实验表明（Figure 11），$\lambda$ 在 $0.15 \sim 0.30$ 范围内可实现从欠编辑到充分表达属性的平滑过渡。几何编辑连续性对比（Figure 14）显示该机制的线性度 $R^2 = 0.973$，高于 **ConceptSlider** 的 0.966 和 **AttControl** 的 0.962，证实其更精确的连续控制能力。

### 多主体微调损失（扩展）

在多主体场景下，需额外引入 AttPooling Aggregator（AAg）定位目标主体，并在 SAE 损失基础上加入一致性损失 $\mathcal{L}_{\text{cons}}$ 以约束非目标区域保持不变：

$$\mathcal{L}_{\text{multi}} = \mathcal{L}_{\text{sae}} + \eta \mathcal{L}_{\text{cons}}$$

- $\eta$：一致性损失权重
- $\mathcal{L}_{\text{sae}}$：原始 SAE 训练损失（式 5）
- $\mathcal{L}_{\text{cons}}$：约束操控仅作用于目标主体的正则项



## 实验与关键发现

### 核心定量结果

All-in-One Slider 在单属性操控与多属性组合操控两个维度上均展现出对基线方法的显著优势。Table 1 报告了在 52 种面部属性上的定量对比，评估指标为语义对齐分数（QS，由 Qwen2.5-VL 计算）和身份一致性分数（IS，基于 ArcFace）。

**单属性操控**：在 Old 属性上，本方法取得 QS 4.0490 / IS 0.7155，IS 较 **ConceptSlider**（0.4336）和 **AttControl**（0.6005）分别提升 0.2819 和 0.1150。在 Makeup 属性上，IS 达到 0.7423，同样为三者最高。这表明稀疏自编码器导出的操控方向在实现语义编辑的同时，更有效地保持了主体身份信息。

**多属性组合操控**：在 Old+Smile、Old+Makeup、Smile+Makeup 三种组合下，本方法的 QS 分别为 4.2124、4.4281、4.2973，均列第一；IS 分别为 0.6882、0.6277、0.6351，显著优于 ConceptSlider（如 Old+Smile IS 仅 0.4993）和 AttControl（Old+Smile IS 仅 0.3755）。这一结果验证了统一属性潜在空间（Attribute Latent Space）中不同属性方向的解耦性——多个稀疏方向可线性叠加而不产生语义冲突。

### 消融分析

**编码器层选择**：Table 2 系统评估了从 SDXL 双文本编码器不同中间层提取嵌入对操控性能的影响。实验表明，选择第一编码器第 10 层和第二编码器第 28 层（记为 10/28）在所有属性上取得最佳整体平衡。深层表征保留了更完整的语义和身份信息，有利于稀疏自编码器的解耦重建。

**稀疏方向 vs. 原始嵌入**：Table 3 直接对比了 SAE 解码方向与直接添加原始文本嵌入的效果。在 Old、Smile、Makeup 三个属性上，SAE 方向的平均 QS 从 3.990 提升至 4.202（+0.212），平均 IS 从 0.502 提升至 0.698（+0.196）。这为“稀疏自编码器提取了更纯净语义信号”的核心主张提供了直接证据——原始嵌入空间中的属性信息高度纠缠，直接操控会引入噪声并损害身份保持。

**操控强度 λ**：Figure 11 展示了 λ 在 0.15 至 0.30 区间内可实现从欠编辑到充分属性表达的平滑过渡。超出此范围会导致编辑不足或身份退化，该参数为实际使用提供了标定参考。

**几何编辑连续性**：Figure 14 对比了不同方法在连续操控下的编辑轨迹线性度。本方法的 R² 达到 0.973，高于 ConceptSlider（0.966）和 AttControl（0.962），证实了稀疏潜在空间中属性方向的线性可加性，支持更精确的连续控制。

### 定性结果与泛化能力

**细粒度面部编辑**（Figure 4）：方法可同时处理语义级编辑（微笑、妆容、年龄）和物理属性修改（眼镜、帽子、发型、肤色），编辑效果自然且未改变无关属性。

**多属性组合**（Figure 5）：在同时施加多个属性时，编辑结果保持连贯且无冲突，验证了潜在空间中不同方向的独立性。

**零样本泛化**（Figure 7）：在未参与训练的种族属性（如 African、Chinese、Indian）上，模型可实现连续操控，无需额外训练。该能力源于属性被分解为 Attlatentspace 中的细粒度解耦分量，预训练文本编码器对未见属性的语义理解支撑了泛化。

**跨模型迁移**（Figure 8, Figure 13）：方法在 SD v1.4、SDXL-Turbo 和 FLUX 上均能有效执行属性调制，表明稀疏自编码器学到的操控方向具有模型架构无关的可迁移性。

**真实图像编辑**（Figure 6）：结合 ReNoise 反演框架，本方法在编辑微笑和年龄时比 AttControl 更好地保留了眼镜等身份细节和面部结构。

**风格操控**（Figure 9, Figure 18）：方法可扩展至摄影风格连续操控（黑白、金色时刻、粉彩色调、霓虹灯光），在保持核心内容和构图的同时实现风格过渡。

**多主体操控**（Figure 10, Figure 19）：通过引入 AttPooling Aggregator（AAg）模块和微调，方法可将属性精确施加到多主体场景中的目标人物，同时保持其他主体不变。微调损失为 $\mathcal{L}_{\mathrm{multi}} = \mathcal{L}_{\mathrm{sae}} + \eta \mathcal{L}_{\mathrm{cons}}$，其中一致性损失约束非目标区域不被修改。

### 失败模式与局限

1. **属性覆盖依赖提示语料**：训练需收集覆盖 52 种属性的多样化文本提示，引入新属性仍需构造提示语料，无法完全摆脱数据准备。
2. **计算开销**：潜在维度高达 32768，训练约需 400M 词元，对资源有一定要求。
3. **场景泛化未充分验证**：目前主要验证于面部属性和有限摄影风格，对通用物体属性或复杂场景编辑的可控性尚未评估。
4. **长尾属性退化风险**：零样本操控依赖预训练编码器的语义理解，对生僻或长尾属性可能退化，需人工验证。
5. **多主体流程复杂度**：多主体操控需额外引入 AAg 模块并进行微调，增加了配对数据需求和流程复杂度。

### 补充图表

![[assets/figures/papers/paper_list_l2439_https_arxiv_org_abs_2508_19195/figures/016_Table_3.jpg]]
*Table 3: Comparison with raw attribute embedding*

![[assets/figures/papers/paper_list_l2439_https_arxiv_org_abs_2508_19195/figures/012_Table_2.jpg]]
*Table 2: Evaluation for attributes across different Manipulation Layer (X/Y) of SDXL’s dual text encoders, where X is the selected layer index in the first encoder and Y in the second*

![[assets/figures/papers/paper_list_l2439_https_arxiv_org_abs_2508_19195/figures/017_Figure_14.jpg]]
*Figure 14: Geometric edit continuity and linearity comparison*

![[assets/figures/papers/paper_list_l2439_https_arxiv_org_abs_2508_19195/figures/013_Figure_11.jpg]]
*Figure 11: Effect of manipulating strength λ on attribute expression (QS) and identity preservation (IS) for various attributes*

![[assets/figures/papers/paper_list_l2439_https_arxiv_org_abs_2508_19195/figures/004_Figure_4.jpg]]
*Figure 4: Qualitative results of face attribute manipulation. Our All-in-One slider can perform both fine-grained semantic edits (e.g., smile, makeup, and age) and physical changes (e.g., eyeglasses, hat, hair style, and skin tone)*

![[assets/figures/papers/paper_list_l2439_https_arxiv_org_abs_2508_19195/figures/005_Figure_5.jpg]]
*Figure 5: Qualitative results of compositional multi-attributes manipulation. Our All-in-One slider achieves coherent manipulation while preserving the original identity*

![[assets/figures/papers/paper_list_l2439_https_arxiv_org_abs_2508_19195/figures/008_Figure_7.jpg]]
*Figure 7: Continuous zero-shot generalization to different racial attributes. The model progressively manipulates facial features across varying strengths of the racial attribute*



## 定位与知识库关联

### 与现有工作的关系

**One‑for‑One 范式的瓶颈。** 现有扩散模型中的属性操控方法，如 **ConceptSlider** 和 **AttControl**，普遍遵循“一个属性一个模块”的独立训练范式——每个目标属性（如“微笑”“年龄”）都需要单独训练一个 LoRA 适配器、偏移向量或轻量编码器，将学习到的方向直接注入文本嵌入空间。这一范式带来三重局限：（1）**参数冗余且不可扩展**：属性数量增加时，必须反复训练并存储多个模块；（2）**不支持零样本操控**：未见过的属性（如特定种族、名人身份）无法被操控；（3）**组合能力弱**：多个属性方向在同一稠密嵌入空间中叠加时，语义纠缠导致编辑冲突或身份退化。

**All‑in‑One Slider 的结构性突破。** 本文提出的 All‑in‑One Slider 将上述“为每个属性训练独立模块”的范式替换为“单次训练构建共享的解耦潜在空间”。核心机制是在文本编码器的中间层表征上引入**属性稀疏自编码器（Attribute Sparse Autoencoder）**，通过 Top‑k 稀疏激活将原本稠密、高度纠缠的嵌入空间强制分解为高维稀疏的**属性潜在空间（Attlatentspace）**。在此空间中，不同属性天然对应独立且可复用的稀疏方向，从而仅用一个轻量模块即可实现多属性的连续操控、组合操控以及零样本泛化（见 Figure 2 的范式对比）。

**与稀疏自编码器流派的关系。** 稀疏自编码器在语言模型可解释性领域已被用于从稠密激活中提取单义特征，但将其迁移到扩散模型的文本嵌入空间并用于属性操控，是本工作的独特贡献。与典型 SAE 仅追求重建不同，本文的 Attribute Sparse Autoencoder 将稀疏性作为**解耦机制**：训练时只保留激活最强的 k 个神经元，迫使每个属性方向仅占据潜在空间中少数几个维度，从而在解码后形成“纯净”的语义编辑信号。这一设计与 ConceptSlider 等直接缩放原始嵌入的做法形成根本差异——后者缺乏显式的解耦约束，编辑信号中不可避免地混入无关语义，导致身份一致性下降（Table 3：稀疏方向使平均 IS 从 0.502 提升至 0.698）。

**在扩散模型可控生成版图中的位置。** 当前扩散模型的可控编辑方法大致分为三类：基于文本提示的工程方法（无需训练但控制粗糙）、基于微调的个性化方法（如 DreamBooth，需要少量图像但无法泛化属性）、以及基于潜在空间操控的滑块方法。All‑in‑One Slider 属于第三类，但通过引入稀疏解耦机制，将滑块方法从“属性专用”推进到“属性通用”阶段。其训练仅需非配对的文本提示（52 种属性 × 1000 条提示），无需属性标签或配对图像，比需要配对监督的方法更具可扩展性。

### 适用边界

**已验证的适用域。** 实验覆盖了 52 种面部属性（语义类如微笑、年龄、妆容，物理类如眼镜、帽子、发型、肤色）的 T2I 生成操控，以及有限摄影风格（黑白、金色时刻、粉彩色调、霓虹灯光）的连续迁移。在 SDXL 上取得 SOTA 结果，并验证了向 SD v1.4 和 SDXL‑Turbo 的跨架构泛化能力（Figure 8），以及向 FLUX 模型的初步迁移（Figure 13）。真实图像编辑方面，结合 ReNoise 反演框架可对微笑和年龄属性进行操控（Figure 6）。

**已知局限与未验证边界。**
- **属性覆盖的依赖**：训练依赖精心构造的 52 种属性提示语料，引入新属性仍需构造相应提示集合。对于生僻或长尾属性（如特定疾病的面部表征、罕见表情），预训练文本编码器的语义理解可能不足，导致零样本操控退化。
- **场景泛化未评估**：当前验证集中于面部属性和摄影风格，对更通用的物体属性编辑（如“让汽车更运动”“让房间更温馨”）、前景‑背景关系修改、或复杂场景中的多对象交互编辑，尚未提供定量或定性证据。
- **计算资源门槛**：潜在维度高达 32768，训练需约 400M 词元，对消费级 GPU 不够友好。
- **多主体场景的额外复杂度**：多主体操控需要额外引入 AttPooling Aggregator 并进行微调，增加了配对数据需求和流程复杂度（Figure 10），尚未实现与单主体场景同等的“开箱即用”体验。
- **评估指标的生态位**：定量评估采用 Qwen2.5‑VL 的 QwenScore（QS）和基于 ArcFace 的 ID 一致性（IS），前者虽与人类判断对齐较好，但尚未成为领域标准指标，跨论文的绝对数值比较需谨慎。

### 开放问题

1. **自适应稀疏度**：当前 k 值固定（Top‑k 选择），但不同属性的语义复杂度差异显著——粗粒度属性（如“性别”）可能仅需极少数维度，而细粒度属性（如“微妙的年龄变化”）可能需要更多维度。能否设计自适应 k 值机制，根据属性复杂度动态分配稀疏容量？

2. **轻量化部署**：潜在维度 32768 的训练和推理开销限制了在资源受限场景的应用。是否可与 TinyCLIP 等更轻量的文本编码器结合，在不损失解耦能力的前提下压缩潜在空间规模？

3. **稀疏维度的可解释性验证**：当前通过编辑效果间接证明稀疏方向的解耦性，但缺乏对单个维度语义的系统可视化（例如，维度 #1234 是否稳定对应“嘴角上扬幅度”？）。更系统的可解释性分析将增强对稀疏空间结构的理解。

4. **非人物场景的泛化**：该方法的核心假设——文本嵌入空间中存在可被稀疏分解的属性方向——在非人物、非面部场景（如室内物体、自然景观、抽象概念）中是否仍然成立？需要更广泛的场景验证。

5. **弱监督微调的可能性**：当前训练完全无监督，若能利用少量标注数据（如属性‑维度匹配对）进行微调，是否能进一步提升稀疏空间的语义纯净度和编辑线性度（当前 R²=0.973，仍有提升空间）？

6. **与基于注意力操控的方法融合**：近期工作探索了通过修改交叉注意力图来实现属性编辑，这类方法与基于嵌入空间操控的 All‑in‑One Slider 在机制上互补。两者能否结合以同时获得稀疏解耦的语义纯净度和注意力级别的空间精度？



## 原文 PDF

![[paperPDFs/CVPR_2026/All_in_One_Slider_for_Attribute_Manipulation_in_Diffusion_Models.pdf]]
