---
title: "CASIM: Composite Aware Semantic Injection for Text to Motion Generation"
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: "paperPDFs/arxiv_2025/CASIM:_Composite_Aware_Semantic_Injection_for_Text_to_Motion_Generation.pdf"
project_link: "https://cjerry1243.github.io/casim_t2m"
code_link: null
aliases:
- CCASIM
- CASIM
tags:
- arxiv_2025
- topic/motion_animation
- topic/motion_animation/human_motion_generation
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: CASIM 由两个核心模块构成：组合感知文本编码器（保留词元级嵌入）和文本-运动对齐器（基于多头注意力的动态对齐）。该机制将全局注入替换为 Token 级别的动态对齐，使每个运动帧可以自适应地关注所有文本词元，从而在生成过程中建立细粒度的语义控制。
primary_logic: 动态的、词元级的语义注入比固定长度的全局语义注入更优越，因为它能够保留文本的组合结构和时序因果性，并允许模型学习文本-运动之间的软性、动态对应关系，从而显著提升生成运动的可控性与文本-运动对齐度。
claims:
- CASIM 在所有基线模型（MDM、T2MGPT、CoMo、MoMask 等）上均一致提升 R-Precision 并降低 MM-Dist，验证了方法的通用性。
- 在 HumanML3D 上，CASIM 使 MDM 的 Top1 R-Precision 从 0.471 提升至 0.502，FID 从 0.325 降至 0.165。
- 注意力可视化显示 CASIM 能够根据文本语义动态调整关注区域：早期帧关注“wave arms”，后期帧关注“sit down”，验证了复合感知对齐的有效性。
- CASIM 在无额外关键词的情况下，即超越了使用 GPT-4 增强关键词的 CoMo 基线，证明动态对齐比静态语义增强更有效。
---

# CASIM: Composite Aware Semantic Injection for Text to Motion Generation

> [!tip] 核心洞察
> 动态的、词元级的语义注入比固定长度的全局语义注入更优越，因为它能够保留文本的组合结构和时序因果性，并允许模型学习文本-运动之间的软性、动态对应关系，从而显著提升生成运动的可控性与文本-运动对齐度。

| 字段 | 内容 |
|------|------|
| 中文题名 | CASIM：面向文本到运动生成的组合感知语义注入 |
| 英文题名 | CASIM: Composite Aware Semantic Injection for Text to Motion Generation |
| 会议/期刊 | arXiv 2025 |
| Links | [paper](https://arxiv.org/abs/2502.02063) · [Project](https://cjerry1243.github.io/casim_t2m) |
| Topic | #topic/motion_animation #topic/motion_animation/human_motion_generation #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | CASIM (Composite Aware Semantic Injection Mechanism) |
| Dataset | HumanML3D, KIT-ML |

> [!tip] 效果简介
> - HumanML3D 上，R-Precision Top1 ↑ 0.502 (CASIM-MDM) vs 0.471 (MDM) (+0.031)；FID ↓ 0.165 (CASIM-MDM) vs 0.325 (MDM) (-0.160)；R-Precision Top1 ↑ 0.539 (CASIM-T2MGPT) vs 0.484 (T2MGPT) (+0.055)。
> - KIT-ML 上，R-Precision Top1 ↑ 0.448 (CASIM-MDM) vs 0.164 (MDM) (+0.284)；FID ↓ 0.354 (CASIM-MDM) vs 0.497 (MDM) (-0.143)。

## 概要

现有文本到运动生成方法普遍采用 CLIP 的固定长度 [CLS] 嵌入作为全局语义条件。这种设计在本质上面临一个结构性瓶颈：它将整个文本提示压缩为单一向量，无法捕捉人类运动的复合特性——包括顺序动作的时序因果、左右肢体的空间差异，以及文本词元与运动帧之间的细粒度对应关系。其直接后果是，不同文本提示可能生成高度相似的运动，模型对长文本和罕见描述的可控性与泛化能力均受限制（Figure 1）。

CASIM 的核心思路，是将上述“全局语义注入”替换为**词元级的动态对齐**。该方法由两个模块构成：组合感知文本编码器（保留词元级嵌入）与文本-运动对齐器（基于多头注意力的动态对齐）。在生成过程中，每个运动帧可以自适应地关注所有文本词元，从而建立细粒度的语义控制。这一设计的关键因果机制在于：动态对齐保留了文本的组合结构与时序信息，使模型能够学习文本与运动之间软性的、动态的对应关系，而非依赖单一向量的静态压缩。

CASIM 具有模型与表示无关的特性，可同时集成到自回归生成（如 T2MGPT）和扩散式生成（如 MDM）两类主流范式中。在 HumanML3D 和 KIT-ML 两个标准基准上，CASIM 一致提升了多个基线模型的文本-运动对齐度（R-Precision）与运动质量（FID），且无需额外的关键词增强。注意力可视化进一步证实，CASIM 能够根据文本语义动态调整关注区域——例如对“wave arms”和“sit down”在不同帧上分配差异化的注意力权重，验证了复合感知对齐的有效性。

同时，该方法也存在明确的边界条件：对于使用固定长度运动表示的模型（如 MLD），CASIM 的改进有限，因为压缩后的运动编码本身已丢失时序细节，限制了动态对齐的作用空间。此外，在长序列生成中，短交叠过渡段可能出现局部不稳定性，提示需要在时序平滑与语义注入之间寻求更精细的平衡。

文本到运动生成（Text-to-Motion Generation）旨在根据自然语言描述合成逼真的三维人体运动序列，在动画制作、虚拟现实和人机交互等领域具有广泛应用。近年来，扩散模型和自回归模型在该任务上取得了显著进展，代表性工作包括 **MDM**（Tevet et al., ICLR 2023）、**T2MGPT**（Zhang et al., CVPR 2023）、**MoMask**（Guo et al., 2023）和 **MLD**（Chen et al., CVPR 2023）等。然而，现有方法在语义理解层面存在一个共性瓶颈：**固定长度的全局语义注入无法捕捉人类运动的复合特性**。

具体而言，当前主流方法大多依赖 CLIP 文本编码器的 `[CLS]` 嵌入作为全局条件信号。这种固定长度的向量表示将整个文本提示压缩为单一语义表征，不可避免地丢失了词元级别的细粒度信息。由此导致三个层面的问题：

1. **复合语义的坍塌**：人类运动往往包含顺序动作（如“先挥手再坐下”）、空间参照（如“左手”与“右手”）和程度修饰（如“快速行走”）。全局嵌入将这些差异化的语义信息混合为单一向量，模型无法区分不同词元对运动生成的差异化贡献。如 Figure 1 所示，仅替换文本中的“left”与“right”，固定长度注入方法会生成几乎相同的运动序列。

2. **文本-运动对齐的弱化**：全局条件在生成过程中以静态方式注入，每一帧运动接收相同的文本表示，无法建立文本词元与运动帧之间的动态对应关系。这使得模型难以学习“哪些词控制哪些帧”的因果映射，导致生成的运动与文本描述之间存在语义偏差。

3. **长文本与罕见描述的泛化困难**：当文本描述较长或包含罕见动作组合时，固定长度的全局嵌入面临更严重的信息压缩损失，模型生成的运动质量显著下降。

CASIM 的核心洞察在于：**动态的、词元级的语义注入比固定长度的全局语义注入更优越**，因为它能够保留文本的组合结构和时序因果性，并允许模型学习文本-运动之间的软性、动态对应关系。这一设计理念从根本上改变了文本条件作用于运动生成的方式，为提升生成运动的可控性与文本-运动对齐度提供了新的技术路径。

## 核心方法与创新机理

CASIM 的核心创新在于将文本到运动生成中的**语义注入方式**从固定长度的全局嵌入替换为**词元级动态对齐**。这一改变直接针对现有方法的根本瓶颈：CLIP 的 [CLS] token 嵌入将整个文本提示压缩为单一向量，无法捕捉人类运动的复合特性——包括顺序动作、左右肢体差异以及文本词元与运动帧之间的细粒度对应关系。

### 改变的关键槽位：语义注入方式

| 维度 | 基线做法 | CASIM 做法 |
|------|----------|------------|
| 文本表示 | 固定长度的 CLIP [CLS] token 全局嵌入 | 词元级嵌入序列，保留组合语义 |
| 注入机制 | 全局条件向量，所有帧共享 | 动态对齐：每帧自适应关注所有文本词元 |
| 对应关系 | 隐式、静态 | 显式、软性、动态 |

这一改变由两个核心模块实现：

**组合感知文本编码器** 放弃仅使用 [CLS] token，转而保留 CLIP（或 BERT）最后一层或潜层的完整词元级输出。这使得“left hand”与“right hand”等细微语义差异得以保留，为后续的动态对齐提供信息基础。

**文本-运动对齐器** 通过多头注意力机制建立运动帧与文本词元之间的动态对应。在自回归生成中，文本与已生成的运动 Token 拼接后经多头自注意力（MHSA）处理；在扩散生成中，编码器式架构使用 MHSA，解码器式架构则以运动序列为查询对文本嵌入进行多头交叉注意力（MHCA）。公式上，自回归的下一 Token 概率为：

$$P(m_i | m_{<i}, C) = \sigma(\mathrm{MHSA}(C \oplus M^{<i}))$$

解码器式扩散去噪则通过交叉注意力实现：

$$\hat{X^{0}} = \mathrm{MHCA}(X^{\tau}, C + TE(\tau))$$

### 为什么动态对齐更优越

注意力可视化（Figure 5）提供了直接的因果证据：对于“a person wave his arms and then sit down”这样的复合描述，CASIM 的早期帧主要关注“wave arms”，后期帧则转向“sit down”，实现了**时序因果性的自动学习**。词云分析（Figure 4）进一步显示，CASIM 的注意力自然聚焦于动作动词、运动修饰词和空间参照词，无需额外关键词标注。

这一机制的关键优势在于**通用性**：CASIM 是模型无关和表示无关的，可即插即用地集成到自回归（T2MGPT）和扩散式（MDM、MotionDiffuse）等多种运动生成范式中。实验表明，CASIM 在无额外关键词的情况下，即超越了使用 GPT-4 增强关键词的 CoMo 基线，证明**动态对齐比静态语义增强更有效**。

### 局限：对运动表示形式的依赖

消融实验揭示了方法有效性的边界条件：对于使用固定长度潜向量的 MLD 模型，CASIM 的提升有限（FID 仅从 0.532 降至 0.502），因为其运动编码本身已压缩并丢失了时序细节。这表明 CASIM 的动态对齐机制**依赖于运动表示保持时序信息的能力**——这一发现为后续改进指明了方向。

CASIM 的整体设计围绕一个核心观察展开：现有文本到运动生成方法普遍使用 CLIP 的固定长度 `[CLS]` 嵌入作为全局条件，这种压缩表示无法捕捉人类运动的复合特性——包括顺序动作、左右肢体差异以及文本词元与运动帧之间的细粒度对应关系。CASIM 将这一全局语义注入范式替换为**词元级的动态语义注入**，使每个运动帧可以自适应地关注所有文本词元，从而在生成过程中建立细粒度的语义控制。

框架由两个核心模块串联构成（图 2）：

1. **组合感知文本编码器（Composite Aware Text Encoder）**：负责从文本中提取保留词元级语义的嵌入序列。与仅输出单个 `[CLS]` 向量的做法不同，该编码器保留 CLIP（或 BERT）最后一层或潜层的全部词元输出，使下游模块能够访问每个单词的独立表示。这一设计直接回应了瓶颈问题——固定长度嵌入无法区分 “wave left hand” 与 “wave right hand” 中 “left” 和 “right” 的语义差异（图 1）。

2. **文本-运动对齐器（Text-Motion Aligner）**：负责在运动生成过程中建立文本词元与运动帧之间的动态对应。其实现方式取决于底层运动生成器的架构：
   - 在自回归生成器中，对齐器采用**多头自注意力（MHSA）**，将文本词元序列与已生成的运动词元序列拼接后共同编码，使下一个运动词元的预测能够同时条件于全部文本上下文和运动历史。
   - 在扩散式生成器中，对齐器根据编码器或解码器架构分别采用**多头自注意力（MHSA）或交叉注意力（MHCA）**：编码器式变体将时间步增强的文本嵌入与当前噪声运动拼接后通过 MHSA 预测干净运动；解码器式变体则以运动序列为查询，对文本嵌入进行交叉注意力，显式建模运动帧到文本词元的依赖关系。

3. **运动生成器（Motion Generator）**：底层运动生成模型，接收对齐器输出的文本-运动联合表示并生成最终运动序列。CASIM 被设计为模型无关和表示无关的插件，可集成到自回归式（如 T2MGPT、CoMo、MoMask）和扩散式（如 MDM、MotionDiffuse）等多种生成范式中，无需修改底层生成器的核心结构。

整体数据流为：文本输入 → 组合感知文本编码器（词元级嵌入） → 文本-运动对齐器（动态注意力） → 运动生成器（运动序列输出）。这一流程将因果控制点从“全局条件注入”转移到“词元级动态对齐”，使模型能够根据文本的组合语义和时序结构，在不同生成阶段自适应地调整对各个词元的关注权重。

CASIM 由两个核心模块构成：**组合感知文本编码器**（Composite Aware Text Encoder）与**文本-运动对齐器**（Text-Motion Aligner），二者协同实现从固定长度全局语义注入到词元级动态对齐的范式转换。

### 组合感知文本编码器

现有方法普遍使用 CLIP 的 `[CLS]` token 嵌入作为全局文本条件，将整个提示压缩为单一固定长度向量。这种压缩不可避免地丢失了复合语义——例如 "wave left hand then sit down" 中 "left" 与 "right" 的差异、"wave" 与 "sit" 的时序因果——导致不同文本生成高度相似的运动（Figure 1）。

CASIM 的文本编码器保留完整的词元级嵌入序列。给定文本提示 $T = [t_1, t_2, \dots, t_N]$，编码器输出 $C = [c_1, c_2, \dots, c_N]$，其中每个 $c_i$ 对应一个词元的上下文表示。默认使用 CLIP 的潜层输出，消融实验表明也可替换为 BERT 以获得更强的双向上下文编码（Table 7：BERT 将 R-Precision Top1 从 0.478 提升至 0.511，MM-Dist 从 3.272 降至 2.938）。

### 文本-运动对齐器

对齐器是 CASIM 的关键创新。它将文本条件注入从"全局向量拼接"改造为"动态注意力交互"，使每个运动帧可以自适应地关注所有文本词元。

**自回归生成**（如 T2MGPT）采用 GPT 式 Transformer，通过多头自注意力（MHSA）实现对齐。运动 Token 序列 $M$ 与文本 Token 序列 $C$ 拼接后送入 MHSA 块：

$$P(m_i \mid m_{<i}, C) = \sigma(\mathrm{MHSA}(C \oplus M^{<i}))$$

其中 $\oplus$ 表示序列拼接，$\sigma$ 为 softmax 函数。文本 Token 与运动 Token 在注意力矩阵中自由交互，模型学习哪些词元对当前帧的生成最为关键。

**扩散生成**（如 MDM）则根据架构类型采用不同对齐策略。扩散去噪的基础步骤为：

$$X^{\tau-1} \sim \mathcal{N}(\mu_{\theta}(X^{\tau}, \tau, C), \Sigma(\tau))$$

其中 $X^{\tau}$ 为当前噪声运动，$\tau$ 为扩散时间步，$\Sigma(\tau)$ 为固定方差。CASIM 在此框架下提供两种集成方式：

- **编码器式**（Encoder-based）：将时间步编码 $TE(\tau)$ 加到文本嵌入后与当前运动拼接，通过 MHSA 直接预测干净运动：
  $$\hat{X^{0}} = \mathrm{MHSA}((C + TE(\tau)) \oplus X^{\tau})$$

- **解码器式**（Decoder-based）：以运动序列为 Query，对时间步增强的文本嵌入进行多头交叉注意力（MHCA）：
  $$\hat{X^{0}} = \mathrm{MHCA}(X^{\tau}, C + TE(\tau))$$

消融实验表明，解码器式架构的提升更为显著（Table 5：Top3 R-Precision 从 0.608 提升至 0.793，FID 从 0.767 降至 0.165），因为交叉注意力天然地将文本作为外部条件源，避免了拼接式自注意力中运动噪声对文本表示的干扰。

### 关键设计选择

1. **文本编码器选择**：CLIP 提供视觉-语言对齐的先验，BERT 提供更强的双向上下文建模。CLIP 最终层嵌入虽能提升文本-运动对齐（R-Precision Top1 0.517 vs 0.478），但会牺牲运动质量（FID 0.410 vs 0.303，Table 8），表明深层语义特征可能过拟合于视觉判别任务，不利于运动生成。

2. **运动表示要求**：CASIM 的有效性依赖于运动表示保留时序信息。对于使用固定长度潜向量的 MLD 模型，CASIM 提升有限（FID 0.532→0.502，Top1 R-Precision 0.469→0.452，Table 9），因为压缩后的运动编码已丢失帧级细节，限制了动态对齐的作用空间。

## 实验与关键发现

### 主实验结果

CASIM 在两个主流文本-运动生成基准上均表现出对多种基线模型的一致提升。在 HumanML3D 数据集上，CASIM-MDM 将 Top1 R-Precision 从 0.471 提升至 **0.502**，FID 从 0.325 降至 **0.165**；CASIM-T2MGPT 将 Top1 R-Precision 从 0.484 提升至 **0.539**，FID 从 0.117 降至 **0.105**（Table 3）。在 KIT-ML 数据集上，提升更为显著：CASIM-MDM 将 Top1 R-Precision 从 0.164 提升至 **0.448**（+0.284），FID 从 0.497 降至 **0.354**（Table 4）。

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2502_02063/figures/005_Table_3.jpg]]
*Table 3: Quantitative results for various text-to-motion methods with CASIM on HumanML3D dataset*

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2502_02063/figures/006_Table_4.jpg]]
*Table 4: Quantitative results for various text-to-motion methods with CASIM on KIT-ML dataset*

CASIM 的通用性体现在其对不同架构基线的适配能力。无论是扩散式方法（**MDM**，Tevet et al., ICLR 2023）、自回归方法（**T2MGPT**，Zhang et al., CVPR 2023），还是基于掩码运动建模的方法（**MoMask**，Guo et al., 2023），集成 CASIM 后均在 R-Precision 和 MM-Dist 指标上获得一致提升（Table 3）。值得注意的是，CASIM 在无额外关键词增强的情况下，即超越了使用 GPT-4 增强关键词的 **CoMo**（Huang et al., 2024）基线，表明动态对齐机制比静态语义增强更有效地利用了文本信息。

定性结果（Figure 3）进一步验证了这一结论：对于包含“wave arms then sit down”等复合动作描述的提示，CASIM 增强模型生成的运动序列在动作时序和空间细节上与真实运动（GT）更为接近，而基线模型往往遗漏或混淆子动作。

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2502_02063/figures/007_Figure_3.jpg]]
*Figure 3: Qualitative comparison between two baselines, their CASIM-enhanced models, and ground truth (GT) on HumanML3D test prompts. Action verbs and their modifiers are highlighted in red, with motion sequences shown in color gradients (light to dark) and root trajectories in black. CASIM-MDM and CASIM-T2MGPT generate the motions that better match the descriptions, showing stronger text-motion correspondence and better controllability*

### 消融实验

**文本编码器选择**：将 CLIP 替换为 BERT 作为文本编码器，可将 Top1 R-Precision 从 0.478 进一步提升至 **0.511**，MM-Dist 从 3.272 降至 **2.938**（Table 7）。这表明 BERT 的双向上下文编码能力更有利于捕捉运动相关的语义信息。然而，论文主要实验仍以 CLIP 为主，BERT 的结论需要手动验证其在不同训练配置下的稳定性。

**嵌入层深度**：使用 CLIP 最终层（而非潜层）嵌入可将 Top1 R-Precision 从 0.478 提升至 **0.517**，但代价是 FID 从 0.303 恶化至 **0.410**（Table 8）。这说明深层嵌入虽能增强文本-运动对齐，但可能因过拟合或语义压缩而损害运动质量。这一权衡需要在具体应用中根据对齐精度与运动自然度的优先级进行调参。

**扩散架构变体**：CASIM 在解码器式扩散架构上的提升远大于编码器式架构。解码器变体将 Top3 R-Precision 从 0.608 提升至 **0.793**，FID 从 0.767 降至 **0.165**（Table 5）。解码器架构中运动序列作为查询（query）对文本嵌入进行交叉注意力，天然更适合 CASIM 的动态对齐机制；而编码器架构的拼接式自注意力在信息流动上相对受限。

**长序列生成**：在长序列运动生成任务中，CASIM 仍保持优势，但当过渡段重叠帧数较短（20 帧）时，过渡段的 FID 略有升高（Table 6）。这表明动态注意力在局部过渡区域可能引入不稳定性，增加重叠帧数可以缓解此问题。

### 失败模式与局限性

**固定长度运动表示的限制**：对于使用固定长度潜向量的 **MLD**（Chen et al., CVPR 2023），CASIM 的提升微乎其微——FID 仅从 0.532 降至 0.502，Top1 R-Precision 甚至从 0.469 降至 0.452（Table 9）。这是因为 MLD 的运动编码器将运动序列压缩为固定维度向量，丢失了时序细节，使 CASIM 的词元级动态对齐失去了作用对象。这一失败模式揭示了 CASIM 有效性的前提条件：**运动表示必须保留足够的时序信息**，以便注意力机制能够建立帧级对应关系。

**编码器依赖**：CASIM 的性能与预训练文本编码器的质量直接相关。若编码器对特定领域词汇（如专业运动术语）理解不佳，动态对齐将无法建立正确的文本-运动对应。当前实验仅覆盖英文文本，对多语言或其他运动风格的泛化能力尚未验证。

**过渡段稳定性**：如前所述，在长序列生成中，短重叠帧数会导致过渡段质量下降，说明动态注意力在片段边界处需要更充分的上下文来维持运动平滑性。

### 注意力分析

注意力可视化（Figure 5）提供了 CASIM 工作机制的直接证据。对于提示“a person wave his arms and then sit down”，不同注意力头展现出互补的关注模式：早期运动帧主要关注“wave arms”，后期帧则转向“sit down”，验证了动态对齐能够根据运动时序自适应调整语义关注区域。词云分析（Figure 4）进一步表明，CASIM 的注意力集中在动作动词、运动修饰语和空间参照词上，而非均匀分布于所有词元，证实了其对复合语义的选择性关注能力。

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2502_02063/figures/014_Figure_5.jpg]]
*Figure 5: Visualization of attention weights in CASIM-MDM. Top: Generated motion sequence for the prompt ”a person wave his arms and then sit down”. Bottom: Attention heatmaps for four attention heads and their average from the last layer*

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2502_02063/figures/008_Table_5.jpg]]
*Table 5: Additional quantiative results on HumanML3D with varying architectures and configuration settings*

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2502_02063/figures/011_Table_7.jpg]]
*Table 7: Quantitative results with different text encoder for CASIM on HumanML3D dataset*

## 定位与知识库关联

### 1. 核心瓶颈：从全局嵌入到组合感知

现有文本到运动生成方法普遍采用 CLIP 的固定长度 `[CLS]` 嵌入作为全局语义条件。这一范式存在根本性局限：它将整个文本提示压缩为单一向量，无法捕捉人类运动的复合特性——顺序动作（先挥手再坐下）、左右肢体差异、动作修饰词（缓慢地、大幅度地）等细粒度语义。其直接后果是，不同文本提示可能生成高度相似的运动，且对长文本或罕见描述泛化能力差。

CASIM 的核心洞察在于：**动态的、词元级的语义注入比固定长度的全局语义注入更优越**，因为它能够保留文本的组合结构和时序因果性，并允许模型学习文本-运动之间的软性、动态对应关系。

### 2. 方法定位：模型无关的语义注入层

CASIM 并非一个独立的运动生成模型，而是一种**模型无关的语义注入机制**，可集成到自回归和扩散两大类运动生成框架中。其两个核心模块——组合感知文本编码器与文本-运动对齐器——构成了从“全局条件”到“词元级动态对齐”的范式转换：

- **组合感知文本编码器**：保留词元级嵌入，替代传统的 `[CLS]` 单一向量。可使用 CLIP 或 BERT 的最后一层或潜层输出。
- **文本-运动对齐器**：通过多头自注意力（自回归生成）或多头交叉注意力（扩散生成）建立运动帧与文本词元之间的动态对应，使每个运动帧可以自适应地关注所有文本词元。

在自回归框架中，文本 Token 序列与已生成的运动 Token 序列拼接后通过 MHSA 获得下一个 Token 的概率：

$$P(m_i | m_{<i}, C) = \sigma(\mathrm{MHSA}(C \oplus M^{<i}))$$

在扩散框架中，编码器式去噪将时间步增强的文本嵌入与当前运动拼接后通过 MHSA 预测干净运动：

$$\hat{X^{0}} = \mathrm{MHSA}((C + TE(\tau)) \oplus X^{\tau})$$

解码器式去噪则以运动序列为查询，对文本嵌入进行交叉注意力：

$$\hat{X^{0}} = \mathrm{MHCA}(X^{\tau}, C + TE(\tau))$$

### 3. 基线关系与改进幅度

CASIM 在多个代表性基线上验证了通用性，基线覆盖了主流生成范式：

| 基线模型 | 范式 | 出处 |
|---------|------|------|
| **MDM** | 扩散式运动生成 | Tevet et al., ICLR 2023 |
| **MotionDiffuse** | 扩散式文本-运动生成 | Zhang et al., arXiv 2022 |
| **T2MGPT** | 自回归运动生成 | Zhang et al., CVPR 2023 |
| **CoMo** | 结合姿态码的自回归生成 | Huang et al., 2024 |
| **MoMask** | 基于掩码运动建模 | Guo et al., 2023 |
| **MLD** | 潜空间扩散运动生成 | Chen et al., CVPR 2023 |

**关键改进幅度**（HumanML3D 数据集）：

- **CASIM-MDM**：Top1 R-Precision 从 0.471 提升至 0.502（+0.031），FID 从 0.325 降至 0.165（-0.160）
- **CASIM-T2MGPT**：Top1 R-Precision 从 0.484 提升至 0.539（+0.055），FID 从 0.117 降至 0.105

在 KIT-ML 数据集上，CASIM-MDM 的改进更为显著：Top1 R-Precision 从 0.164 跃升至 0.448（+0.284），FID 从 0.497 降至 0.354。

值得注意的是，CASIM 在无额外关键词的情况下，即超越了使用 GPT-4 增强关键词的 CoMo 基线（Table 3），证明**动态对齐比静态语义增强更有效**——这一发现挑战了“更强的文本编码即更好”的直觉。

### 4. 适用边界与架构敏感性

消融实验揭示了 CASIM 有效性的关键条件：

**架构依赖性**：解码器式扩散架构上 CASIM 的提升远大于编码器式。解码器变体将 Top3 R-Precision 从 0.608 提升至 0.793，FID 从 0.767 降至 0.165；而编码器式的改进幅度明显较小（Table 5）。这表明交叉注意力机制（MHCA）比自注意力拼接（MHSA）更适合文本-运动的动态对齐。

**运动表示的时序保真度要求**：对于使用固定长度潜向量的 **MLD**（Chen et al., CVPR 2023），CASIM 的提升极为有限——FID 仅从 0.532 降至 0.502，Top1 R-Precision 甚至从 0.469 微降至 0.452（Table 9）。这是因为 MLD 的运动编码本身已将时序信息压缩为单一向量，丢失了帧级细节，使得词元级动态对齐失去了作用支点。这一负结果反向验证了 CASIM 的核心机制：**其有效性依赖于运动表示保持时序信息的能力**。

**文本编码器选择**：使用 BERT 替代 CLIP 可将 Top1 R-Precision 从 0.478 提升至 0.511，MM-Dist 从 3.272 降至 2.938（Table 7），表明双向上下文编码更有利于捕获运动相关语义。此外，CLIP 最终层嵌入虽能提升文本-运动对齐（Top1 R-Precision 0.517 vs 0.478），但会牺牲运动质量（FID 0.410 vs 0.303）（Table 8），提示潜层特征保留了更多对生成质量有益的细节信息。

### 5. 已知局限

1. **固定长度运动表示的兼容性差**：如前所述，MLD 等压缩时序信息的方法无法有效利用 CASIM 的动态对齐优势。
2. **长序列过渡段的不稳定性**：在长序列运动生成中，短手部交叠（20 帧）时过渡段的 FID 略有升高（Table 6），表明动态注意力可能引入局部过渡的不稳定，需要更长的重叠帧数来平衡。
3. **数据集与语言限制**：所有实验基于 HumanML3D 和 KIT-ML 两个英文数据集，对复杂场景、多语言或其他运动风格（如舞蹈、体育）的泛化能力尚未验证。
4. **编码器质量依赖**：CASIM 的性能与预训练文本编码器（CLIP/BERT）的质量耦合，若编码器对特定领域词汇（如专业运动术语）理解不佳，可能影响最终的文本-运动对齐。

### 6. 开放问题

- **过渡平滑性**：在扩散式过渡生成中，语义注入如何平衡局部运动质量与不同片段间的平滑衔接？当前的手部交叠策略仍存在局部 FID 升高的问题。
- **更强语言模型的潜力**：能否利用大语言模型作为文本编码器，进一步提升对复合语义及长描述的理解？当前仅探索了 CLIP 和 BERT。
- **任务拓展**：CASIM 的动态对齐机制是否可以拓展到场景感知、多人交互等更复杂的运动生成任务？其“词元级动态条件注入”的范式可能具有更广泛的适用性。
- **固定表示方法的适配**：对于 MLD 等固定长度运动表示的方法，如何改造运动编码器（如引入时序分解或层次化潜变量）以使 CASIM 也能充分发挥作用？这是一个值得探索的架构改进方向。

## 原文 PDF

![[paperPDFs/arxiv_2025/CASIM:_Composite_Aware_Semantic_Injection_for_Text_to_Motion_Generation.pdf]]
