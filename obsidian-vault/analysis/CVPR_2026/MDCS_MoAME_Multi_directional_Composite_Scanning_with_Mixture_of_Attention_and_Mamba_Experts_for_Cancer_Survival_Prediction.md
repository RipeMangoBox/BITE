---
title: "MDCS-MoAME: Multi-directional Composite Scanning with Mixture of Attention and Mamba Experts for Cancer Survival Prediction"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/MDCS_MoAME_Multi_directional_Composite_Scanning_with_Mixture_of_Attention_and_Mamba_Experts_for_Cancer_Survival_Prediction.pdf
project_link: null
code_link: null
aliases:
- MM
- MDCS-MoAME
tags:
- CVPR_2026
- topic/benchmarks_datasets_evaluation
- topic/benchmarks_datasets_evaluation/benchmarking
core_operator: 引入多方向复合扫描（MDCS）扩大WSI与基因序列的感受野，结合混合注意力与Mamba专家（MoAME）动态选择融合策略，并通过跨模态对齐和模态内冗余损失减少表示冗余。
primary_logic: 通过多方向扫描充分挖掘模态内信息，利用动态专家机制灵活建模模态间交互，并辅以对齐约束抑制冗余，从而学习更具判别力的生存相关表征，显著提升预测性能。
claims:
- 在五个TCGA数据集上，MDCS-MoAME的c-index性能明显优于所有对比方法，较PAM和SurvMamba分别提升14.61%和5.70%。
- 多方向复合扫描模块对性能贡献最大：将其替换为原始Mamba扫描后，LUAD和UCEC上的c-index分别下降5.42%和7.03%。
- 组合CroMamFusion和CroAttFusion专家（M+A）效果最优，验证了注意力与Mamba在模态融合中的互补优势。
- 引入跨模态对齐损失L_cro和模态内冗余损失L_intra后，在LUAD上c-index分别提升3.13%和1.78%，在UCEC上提升1.68%和4.04%，证明对齐约束有效减少了特征冗余。
---

# MDCS-MoAME: Multi-directional Composite Scanning with Mixture of Attention and Mamba Experts for Cancer Survival Prediction

> [!tip] 核心洞察
> 通过多方向扫描充分挖掘模态内信息，利用动态专家机制灵活建模模态间交互，并辅以对齐约束抑制冗余，从而学习更具判别力的生存相关表征，显著提升预测性能。

| 字段 | 内容 |
|------|------|
| 中文题名 | MDCS-MoAME：多方向复合扫描与注意力-Mamba专家混合的癌症生存预测 |
| 英文题名 | MDCS-MoAME: Multi-directional Composite Scanning with Mixture of Attention and Mamba Experts for Cancer Survival Prediction |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Qu_MDCS-MoAME_Multi-directional_Composite_Scanning_with_Mixture_of_Attention_and_Mamba_CVPR_2026_paper.html) |
| Topic | #topic/benchmarks_datasets_evaluation #topic/benchmarks_datasets_evaluation/benchmarking |
| Method | MDCS-MoAME |
| Dataset | Five TCGA datasets |

> [!tip] 效果简介
> - Five TCGA datasets (平均) 上，c-index improvement MDCS-MoAME vs PAM (Mamba-based WSI) (+14.61%)；c-index improvement MDCS-MoAME vs SurvMamba (+5.70%)；c-index improvement MDCS-MoAME vs MoME (+10.31%)。

## 概要

癌症生存预测的核心挑战在于如何从全切片病理图像（WSIs）和高维稀疏基因组数据中提取具有判别力的预后特征，并有效融合两种异构模态。现有方法存在三个关键瓶颈：**（1）感受野受限**——WSIs仅采用水平扫描、基因组仅采用正向序列化，难以捕获多方向长程依赖与稀疏基因间的远距离关联；**（2）融合策略僵化**——跨模态交互依赖单一注意力或Mamba机制，无法灵活建模复杂的异构关系；**（3）缺乏显式冗余抑制**——模态内与模态间特征冗余未被有效约束，限制了表征的判别力。

针对上述问题，本文提出**MDCS-MoAME**（Multi-directional Composite Scanning with Mixture of Attention and Mamba Experts），其核心思路是：通过多方向复合扫描充分挖掘模态内信息，利用动态专家机制灵活建模模态间交互，并辅以对齐约束抑制冗余，从而学习更具判别力的生存相关表征。具体而言，该方法在三个层面进行了创新设计：

- **多方向复合扫描（MDCS）**：对WSI的区域和补丁层级分别施加水平、垂直、左斜、右斜、回环五种扫描方向，对基因组引入间隔扫描策略，显著扩大感受野。
- **混合注意力与Mamba专家（MoAME）**：设计CroAttFusion、CroMamFusion和StackedMamFusion三个融合专家，由门控网络根据输入动态选择最优融合策略，兼顾注意力机制的全局建模能力与Mamba的高效长程依赖捕获能力。
- **跨模态对齐与模态内冗余损失**：通过跨模态对齐损失（$\mathcal{L}_{\mathrm{cro}}$）和模态内冗余损失（$\mathcal{L}_{\mathrm{intra}}$）显式约束表示学习，减少冗余、增强互补性。

在五个TCGA数据集（BLCA、BRCA、GBMLGG、LUAD、UCEC）上的实验表明，MDCS-MoAME的c-index性能显著优于所有对比方法：**较PAM提升14.61%，较SurvMamba提升5.70%，较MoME提升10.31%**。消融实验进一步揭示，多方向复合扫描模块对性能贡献最大——将其替换为原始Mamba扫描后，LUAD和UCEC上的c-index分别下降5.42%和7.03%；组合CroAttFusion与CroMamFusion专家（M+A）效果最优，验证了注意力与Mamba在模态融合中的互补优势；引入对齐损失后，LUAD上c-index分别提升3.13%（$\mathcal{L}_{\mathrm{cro}}$）和1.78%（$\mathcal{L}_{\mathrm{intra}}$），UCEC上提升1.68%和4.04%，证明冗余抑制的有效性。Kaplan-Meier生存分析（Figure 6）显示，模型在LUAD（Log-rank p=5.02e-07）和UCEC（p=5.29e-04）上均实现了稳健的风险分层。

**方法定位**：MDCS-MoAME属于多模态生存预测框架，其设计延续了Mamba在WSI分析中的应用脉络（如**PAM**, Huang et al., IEEE TMI 2025；**SurvMamba**, Chen et al., arXiv 2024），但通过多方向扫描突破了单向序列化的局限；同时借鉴了混合专家（MoE）思想（如**MoME**, Xiong et al., MICCAI 2024），但引入注意力-Mamba混合专家和动态门控选择，实现了更灵活的跨模态融合。与基于协同注意力的方法（如**MCAT**, Chen et al., ICCV 2021；**CMTA**, Zhou and Chen, ICCV 2023）相比，本方法在融合策略上具有更强的自适应能力。

**局限性**：当前仅在TCGA五个癌种上验证，泛化至其他癌种或真实临床队列的能力尚未可知；模型仅整合病理图像与基因组两个模态，未纳入放射影像、临床报告等数据；专家选择机制虽具动态性，但可能存在次优选择，且计算开销略高于简单融合方法（Table 5）；特征提取器固定为预训练ResNet-50和简单全连接层，可能限制表示能力的进一步提升。

癌症生存预测是计算病理学中的核心任务，其目标是根据全切片病理图像（Whole Slide Images, WSIs）和基因组等多模态数据，估计患者在给定时间点之前存活的条件概率。该任务面临两大根本性挑战：**模态内信息挖掘不充分**与**跨模态融合机制单一**。

在模态内建模方面，现有方法存在明显的感受野局限。对于WSIs，主流方法仅采用水平方向扫描（Mamba默认的行扫描策略），无法捕获图像在垂直、对角等多方向上的长程依赖关系；对于基因组数据，现有方法仅采用正向序列化，难以发现远距离、稀疏分布的基因群之间的潜在关联。这种单一扫描范式导致模态内特征表示的信息量受限，成为制约生存预测性能的瓶颈。

在跨模态融合方面，现有方法通常采用固定的融合策略——要么基于注意力机制，要么基于Mamba状态空间模型——缺乏对不同模态间复杂交互关系的动态建模能力。病理图像与基因组数据在尺度、语义和稀疏性上存在本质差异，单一的融合机制难以有效适配这种异构性。此外，现有方法普遍缺乏显式的特征冗余抑制机制，导致跨模态表示中存在大量重复信息，进一步削弱了预测模型的判别力。

针对上述缺口，本文提出**MDCS-MoAME**（Multi-directional Composite Scanning with Mixture of Attention and Mamba Experts），核心动机体现为三个递进层次：

1. **扩大感受野**：通过多方向复合扫描（MDCS）策略，对WSIs引入水平、垂直、左斜、右斜和回环五方向扫描，对基因组序列引入正向扫描与间隔扫描，从多个视角充分挖掘模态内信息。
2. **动态融合建模**：设计混合注意力与Mamba专家（MoAME）模块，通过门控网络从CroAttFusion、CroMamFusion和StackedMamFusion三个专家中动态选择融合策略，灵活应对异构跨模态关系。
3. **冗余抑制**：引入跨模态对齐损失$\mathcal{L}_{\mathrm{cro}}$和模态内冗余损失$\mathcal{L}_{\mathrm{intra}}$，在训练过程中显式约束特征表示，减少模态间和模态内的信息冗余。

在五个TCGA数据集上的实验表明，MDCS-MoAME的c-index性能较PAM（Huang et al., IEEE TMI 2025）和SurvMamba（Chen et al., arXiv 2024）分别提升14.61%和5.70%，验证了多方向扫描与动态专家融合在癌症生存预测中的关键作用。

## 核心方法与创新机理

MDCS-MoAME 围绕“扩大感受野—动态融合—冗余抑制”三条主线，对现有癌症生存预测框架进行了系统性重构。其核心创新可归结为四个紧密耦合的 changed slots，分别针对图像扫描方向、基因组序列化方式、跨模态融合机制与特征冗余抑制。

### 1. 多方向复合扫描（MDCS）：打破单一方向感受野瓶颈

现有 Mamba-based 方法（如 **PAM**，Huang et al., IEEE TMI 2025；**SurvMamba**，Chen et al., arXiv 2024）对 WSI 仅采用默认的水平扫描，对基因组仅采用正向序列化，导致模型感受野单一，难以捕获多方向长程依赖与稀疏基因间关联。MDCS-MoAME 将扫描策略从“单向”扩展为“多向复合”：

- **WSI 五方向扫描**：在区域（region）和补丁（patch）两个层级上，同时施加水平（ho）、垂直（ve）、左斜（lo）、右斜（ro）和回环（lb）五种扫描方向（Figure 1(c)）。各方向序列经 RegionMam/PatchMam（基于 Mamba2）独立编码后，通过索引对齐求和、PPEG 与注意力池化获得增强的模态内表示。
- **基因组间隔扫描**：在传统正向扫描之外，引入间隔扫描策略，通过索引重排操作 $\mathcal{T}(i)$ 以间隔长度 $\Delta$ 重新组织基因群序列，显式挖掘远距离、稀疏基因群之间的潜在关联（Figure 1(e)）。

消融实验提供了强因果证据：将 MDSFE 模块替换为原始 Mamba 后，LUAD 和 UCEC 上的 c-index 分别下降 **5.42%** 和 **7.03%**（Table 2），在所有消融项中降幅最大，直接验证了多方向扫描是模型性能的首要驱动因素。

### 2. 混合注意力与 Mamba 专家（MoAME）：从固定融合到动态专家选择

现有方法多采用单一注意力或单一 Mamba 机制进行跨模态融合，无法灵活适配异构模态间的复杂交互模式。MDCS-MoAME 提出混合注意力与 Mamba 专家（MoAME）模块，由门控网络根据当前多模态输入动态选择融合专家：

- **三类专家**：CroAttFusion（交叉注意力，logit=0）、CroMamFusion（交叉 Mamba，logit=1）、StackedMamFusion（堆叠交叉 Mamba，logit=2）。
- **门控机制**：由 GELU 激活和均值池化计算 logits'，经温度 $\tau$ 的 softmax 后取 argmax 决定激活的专家。
- **互补优势**：消融实验表明，组合 CroMamFusion 与 CroAttFusion（M+A）的性能优于其他双专家及单专家方案（Figure 4），证实了注意力与 Mamba 在模态融合中的互补性——注意力擅长细粒度对齐，Mamba 擅长长程序列建模。

移除整个 EDIMI 模块后，LUAD 和 UCEC 上 c-index 分别下降 **2.61%** 和 **4.60%**（Table 2），进一步确认了专家驱动跨模态交互的关键作用。

### 3. 跨模态对齐与模态内冗余损失：显式冗余抑制

此前方法普遍缺乏对跨模态和模态内表示冗余的显式约束。MDCS-MoAME 引入两类对齐损失，形成“拉近跨模态、推远模态内”的约束机制：

- **跨模态对齐损失 $\mathcal{L}_{\mathrm{cro}}$**：以 L1 距离对齐图像区域/补丁与基因的跨模态表示，减少跨模态冗余。
- **模态内冗余损失 $\mathcal{L}_{\mathrm{intra}}$**：以负 L1 距离鼓励区域和补丁特征保持差异，降低模态内冗余。

增量添加 $\mathcal{L}_{\mathrm{cro}}$ 在 LUAD 和 UCEC 上分别带来 **3.13%** 和 **1.68%** 的 c-index 提升；进一步添加 $\mathcal{L}_{\mathrm{intra}}$ 分别额外提升 **1.78%** 和 **4.04%**（Table 2），证明对齐约束有效减少了特征冗余，且两种损失具有叠加增益。

### 4. 创新协同效应

上述三个 changed slots 并非孤立改进，而是形成了一条因果链路：**MDCS 扩大感受野 → 提供更丰富的模态内表示 → MoAME 动态选择最优融合策略 → 对齐损失抑制冗余 → 最终生存预测性能显著提升**。在五个 TCGA 数据集上，MDCS-MoAME 的平均 c-index 较 PAM 提升 **14.61%**，较 SurvMamba 提升 **5.70%**，较 MoME 提升 **10.31%**（Table 1），以充分的实验证据支撑了这一创新链路的有效性。

> **需手动验证**：论文未开源代码，部分对比方法（如 PAM、PAMoE）由作者依据原论文复现（Table 1 以 ⋆ 标记），复现保真度需结合原论文自行评估。

MDCS-MoAME 的整体架构围绕一个核心瓶颈展开：现有方法对全切片病理图像（WSI）仅采用水平扫描、对基因组仅采用正向序列化，导致感受野单一，难以捕获多方向长程依赖和稀疏基因间关联；同时模态融合使用固定策略，无法有效建模异构跨模态关系，且缺乏显式冗余抑制。MDCS-MoAME 通过三个关键设计——多方向复合扫描（MDCS）、混合注意力与 Mamba 专家（MoAME）、以及跨模态与模态内对齐约束——系统性地解决了上述问题。

### 架构总览

模型由四个主要模块串联构成，形成从原始输入到生存风险预测的端到端管线（Figure 2）：

![[assets/figures/papers/paper_list_l2131_https_openaccess_thecvf_com_content_CVPR2026_html_Qu_MDCS_MoAME_Multi_di/figures/002_Figure_2.jpg]]
*Figure 2: Overall architecture of our proposed MDCS-MoAME. (a) Feature Extraction. (b) Multi-directional Scanning and Feature Enhancement (MDSFE) module. (c) Expert-driven Inter-modal Interaction (EDIMI) module. (d) Feature Alignment and Prediction. (e) RegionMam (PatchMam and GeneMam are similar). (f) Mixture of Attention and Mamba Expert (MoAME) module, consisting of a (g) Gating Network and three experts: (h) CroAttFusion, (i) CroMamFusion, and (j) StackedMamFusion*

1. **特征提取**：使用预训练 ResNet-50 提取 WSI 的 patch 级和 region 级特征，全连接层将基因组通路映射为六组基因 embedding。
2. **多方向扫描与特征增强（MDSFE）**：对图像特征施加水平、垂直、左斜、右斜、回环五方向扫描，对基因组序列施加正向扫描与间隔扫描，随后通过 RegionMam/PatchMam/GeneMam（基于 Mamba2）处理多方向序列，经 PPEG 和注意力池化获得增强的模态内表示。
3. **专家驱动的跨模态交互（EDIMI）与 MoAME**：门控网络从 CroAttFusion、CroMamFusion、StackedMamFusion 三个专家中动态选择融合策略，生成图像-基因跨模态表示。
4. **特征对齐与预测**：通过跨模态对齐损失 $\mathcal{L}_{\mathrm{cro}}$ 和模态内冗余损失 $\mathcal{L}_{\mathrm{intra}}$ 抑制表示冗余，拼接平均后的图像区域、补丁、基因组特征及其跨模态表示，由 MLP 输出生存风险预测。

### 输入输出流

- **输入**：一张 WSI 图像 $I$ 和基因组表达谱 $G$。
- **特征提取后**：图像被组织为 region 序列 $I_{\mathrm{r}} \in \mathbb{R}^{M \times d}$ 和 patch 序列 $I_{\mathrm{p}} \in \mathbb{R}^{N \times d}$；基因组被映射为基因组序列 $G_{\mathrm{g}} \in \mathbb{R}^{K \times d}$。
- **MDSFE 处理后**：输出增强的图像区域表示 $\overline{I}_{\mathrm{r}}$、补丁表示 $\overline{I}_{\mathrm{p}}$ 和基因组表示 $\overline{G}_{\mathrm{g}}$。
- **EDIMI 处理后**：生成三组跨模态表示——$I_{\mathrm{r\&g}}$、$I_{\mathrm{p\&g}}$、$G_{\mathrm{g\&r}}$ 和 $G_{\mathrm{g\&p}}$。
- **最终预测**：将模态内与跨模态表示按公式平均拼接后送入 MLP，得到风险预测 $\hat{Y}$。

### 关键公式

生存预测基于离散时间风险建模。给定图像 $I$ 和基因组 $G$，风险函数定义为：

$$f_{\mathrm{hazard}}(t) = f_{\mathrm{hazard}}(T = t \mid T \geq t, (I, G)) \in [0,1]$$

生存函数由累积风险之积计算：

$$f_{\mathrm{sur}}(T \leq t, (I, G)) = \prod_{u=1}^{t} \left(1 - f_{\mathrm{hazard}}(T = u)\right)$$

总损失为生存负对数似然损失与对齐约束的加权和：

$$\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{sur}} + \alpha \mathcal{L}_{\mathrm{cro}} + \beta \mathcal{L}_{\mathrm{intra}}$$

其中跨模态对齐损失 $\mathcal{L}_{\mathrm{cro}}$ 以 L1 距离约束跨模态表示与原始模态表示的一致性，模态内冗余损失 $\mathcal{L}_{\mathrm{intra}}$ 以负 L1 距离鼓励 region 与 patch 特征保持差异。

### 设计动机与因果机制

整个框架的设计逻辑遵循一条清晰的因果链：**扩大感受野 → 丰富模态内表征 → 动态融合异构信息 → 抑制冗余 → 提升生存预测判别力**。多方向扫描使模型能够从不同空间方向感知 WSI 的组织结构，间隔扫描则帮助发现基因组中远距离稀疏基因群之间的潜在关联。MoAME 的门控网络根据输入特征动态选择最适配的融合专家，避免了固定融合策略对异构跨模态关系建模的不足。而 $\mathcal{L}_{\mathrm{cro}}$ 和 $\mathcal{L}_{\mathrm{intra}}$ 则从跨模态和模态内两个层面校准表示空间，减少信息冗余，使最终拼接特征更具判别力。消融实验证实，移除 MDSFE 模块后 LUAD 和 UCEC 上 c-index 分别下降 5.42% 和 7.03%，移除 EDIMI 模块后分别下降 2.61% 和 4.60%，验证了各模块在因果链中的关键作用。

### 3.1 问题形式化与特征提取

给定全切片图像（WSI）$I$ 和基因组数据 $G$，癌症生存预测的目标是估计风险函数 $f_{\mathrm{hazard}}(t)$ 和生存函数 $f_{\mathrm{sur}}(T \leq t, (I, G))$：

$$f_{\mathrm{hazard}}(t) = f_{\mathrm{hazard}}(T = t \mid T \geq t, (I, G)) \in [0,1]$$

$$f_{\mathrm{sur}}(T \leq t, (I, G)) = \prod_{u=1}^{t} \left(1 - f_{\mathrm{hazard}}(T = u)\right)$$

其中 $f_{\mathrm{hazard}}(t)$ 表示在存活至时刻 $t$ 的条件下发生事件的瞬时风险，$f_{\mathrm{sur}}$ 通过累积 $1-$ 风险函数之积计算患者存活超过 $t$ 的概率。

**特征提取**：使用预训练 ResNet-50 提取 WSI 的 patch 级和 region 级嵌入特征；基因组数据则通过全连接层映射为六组基因 embedding $G = \{x_{\mathbf{g}, i}\}_{i=1}^{K}$（遵循 **CMTA** (Zhou and Chen, ICCV 2023) 的分组策略）。

---

### 3.2 多方向复合扫描与特征增强（MDSFE）

MDSFE 模块是本文的核心创新之一，其设计动机在于：现有方法仅对 WSI 采用水平扫描、对基因组仅采用正向序列化，导致感受野单一，难以捕获多方向长程依赖和稀疏基因间关联。

#### 3.2.1 WSI 多方向扫描

对 region 级特征，除原始水平（ho）扫描外，引入垂直（ve）、左斜（lo）、右斜（ro）、回环（lb）四个额外方向，生成五组扫描序列：

$$\hat{I}_{\mathrm{r}}^{\mathrm{ho}} = I_{\mathrm{reg}}, \quad \hat{I}_{\mathrm{r}}^{j} = \{ x_{\mathrm{r}, \phi_{\mathrm{r}, j}(i)} \}_{i=1}^{M}, \; j \in \{\mathrm{ve}, \mathrm{lo}, \mathrm{ro}, \mathrm{lb}\}$$

其中 $\phi_{\mathrm{r}, j}$ 记录相对于水平扫描的索引重排映射。patch 级特征采用相同的五方向扫描策略。

#### 3.2.2 基因组间隔扫描

针对基因组数据中远距离稀疏基因群之间的潜在关联，引入间隔（iv）扫描策略。设间隔长度为 $\Delta$，索引重排操作定义为：

$$\mathcal{T}(i) = \lceil \frac{i \times \Delta}{\hat{K}} \rceil + \left( (i-1) \bmod \frac{\hat{K}}{\Delta} \right) \times \Delta$$

该操作按间隔 $\Delta$ 重新排列基因群索引，并通过补零确保维度整除，从而暴露正向扫描难以捕获的非局部基因交互。

#### 3.2.3 特征增强与聚合

多方向扫描后的序列分别送入 RegionMam、PatchMam 和 GeneMam（均基于 Mamba2）。以 RegionMam 为例，各方向序列经 Mamba2 处理后重排对齐并求和，再通过 PPEG（位置感知增强）和注意力池化获得增强表示：

$$\overline{I}_{\mathrm{r}} = \left\{ \mathrm{Norm}\left(\mathrm{Linear}\left(\overline{x}_{\mathrm{r},i}^{\mathrm{ho}} + \sum_{j} \overline{x}_{\mathrm{r},\phi_{\mathrm{r},j}^{-1}(i)}^{j}\right)\right) \right\}_{i=1}^{M}$$

其中 $\phi_{\mathrm{r},j}^{-1}$ 将各方向输出映射回原始空间位置，确保多方向信息在相同空间坐标上对齐融合。

---

### 3.3 专家驱动的跨模态交互（EDIMI）与 MoAME

为灵活建模异构跨模态关系，本文提出混合注意力与 Mamba 专家（MoAME）机制，由门控网络动态选择融合策略。

#### 3.3.1 门控网络

给定多模态输入特征 $F_1$ 和 $F_2$，门控网络计算专家选择 logits：

$$logits' = \sum_{j=1}^{2} \big( (\mathbf{Mean}(\mathbf{GELU}(\mathbf{Norm}(F_j W_j)))) W \big)$$

随后通过温度 $\tau$ 的 Softmax 和 argmax 确定所选专家：

$$logit = \mathbf{argmax}\left( \frac{\mathbf{Softmax}(logits')}{\tau} \right)$$

#### 3.3.2 三专家融合

MoAME 包含三个专家，根据 $logit$ 取值动态选择：

$$F_{1\&2} = \begin{cases} \mathrm{Cross\text{-}Attention}(F_1, F_2), & logit = 0 \\ \mathrm{Cross\text{-}Mamba}(F_1, F_2), & logit = 1 \\ \mathrm{Cross\text{-}Mamba}(F_1, \mathrm{Cross\text{-}Mamba}(\mathcal{B}, F_2)), & logit = 2 \end{cases}$$

- **CroAttFusion**（logit=0）：基于交叉注意力的融合，擅长捕获局部精细交互。
- **CroMamFusion**（logit=1）：基于交叉 Mamba 的融合，擅长建模长程依赖。
- **StackedMamFusion**（logit=2）：双层交叉 Mamba 堆叠，通过可学习瓶颈 $\mathcal{B}$ 进行更深度的跨模态交互。

---

### 3.4 特征对齐与生存预测

#### 3.4.1 跨模态对齐损失

为减少跨模态表示冗余，引入 L1 距离对齐图像与基因的跨模态表示：

$$\mathcal{L}_{\mathrm{cro}} = \|I_{\mathrm{r\&g}} - I_{\mathrm{r}}\|_1 + \|I_{\mathrm{p\&g}} - I_{\mathrm{p}}\|_1 + \left\|\frac{1}{2}(G_{\mathrm{g\&r}} + G_{\mathrm{g\&p}}) - G_{\mathrm{g}}\right\|_1$$

三项分别对齐 region-基因、patch-基因的跨模态表示，以及基因侧双路跨模态表示的均值与原始基因特征。

#### 3.4.2 模态内冗余损失

通过负 L1 距离鼓励 region 和 patch 特征保持差异，降低模态内冗余：

$$\mathcal{L}_{\mathrm{intra}} = -\|I_{\mathrm{r}} - I_{\mathrm{p}}\|_1$$

#### 3.4.3 预测与总损失

将各模态特征及其跨模态表示平均后拼接，送入 MLP 得到风险预测：

$$\hat{Y} = \mathbf{MLP}\left(\frac{I_{\mathrm{r}} + I_{\mathrm{r\&g}}}{2} \oplus \frac{I_{\mathrm{p}} + I_{\mathrm{p\&g}}}{2} \oplus \frac{I_{\mathrm{g}} + I_{\mathrm{g}} + I_{\mathrm{g\&r}} + I_{\mathrm{g\&p}}}{4}\right)$$

总损失为生存负对数似然损失与对齐、冗余损失的加权和：

$$\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{sur}} + \alpha \mathcal{L}_{\mathrm{cro}} + \beta \mathcal{L}_{\mathrm{intra}}$$

消融实验（Table 2）表明，添加 $\mathcal{L}_{\mathrm{cro}}$ 在 LUAD 和 UCEC 上分别提升 c-index 3.13% 和 1.68%，添加 $\mathcal{L}_{\mathrm{intra}}$ 分别提升 1.78% 和 4.04%，验证了对齐约束在抑制特征冗余方面的关键作用。

## 实验与关键发现

### 主实验结果

MDCS-MoAME 在五个 TCGA 数据集（BLCA、BRCA、GBMLGG、LUAD、UCEC）上进行了系统评估，对比方法涵盖基于集合的方法（**DeepSets**，Zaheer et al., NIPS 2017）、基因组引导协同注意力方法（**MCAT**，Chen et al., ICCV 2021）、生物通路令牌融合方法（**SurvPath**，Jaume et al., CVPR 2024）、跨模态转换对齐方法（**CMTA**，Zhou and Chen, ICCV 2023）、Mamba-based WSI 方法（**PAM**，Huang et al., IEEE TMI 2025）、多粒度 Mamba 交互方法（**SurvMamba**，Chen et al., arXiv 2024）、混合多模态专家方法（**MoME**，Xiong et al., MICCAI 2024）以及仅使用基因组数据的 **SNN** 基线（Klambauer et al., NIPS 2017）等。

表1 汇总了各方法在五个数据集上的 c-index（均值±标准差）。MDCS-MoAME 在所有数据集上均取得最优性能，平均 c-index 较基于 Mamba 的 WSI 方法 **PAM** 提升 **14.61%**，较 **SurvMamba** 提升 **5.70%**，较 MoE-based 方法 **MoME** 和 **PAMoE** 分别提升 **10.31%** 和 **16.34%**。与仅使用基因组模态的方法（MLP、SNN、SNNTrans）相比，MDCS-MoAME 的平均 c-index 分别高出 **7.81%**、**11.61%** 和 **6.48%**。值得注意的是，对于未开源代码的方法（以 ⋆ 标记），作者依据原论文进行了复现，确保了对比的公平性。

上述性能提升的核心驱动力在于：多方向复合扫描策略显著扩大了对 WSI 和基因组序列的感受野，而混合注意力与 Mamba 专家机制则灵活捕获了异构模态间的复杂关联。

### 消融实验

为验证各模块的独立贡献，作者在 LUAD 和 UCEC 两个数据集上进行了系统的消融实验，结果见表2。

**多方向扫描与特征增强模块（MDSFE）的关键作用。** 将 MDSFE 模块替换为原始 Mamba 扫描后，性能下降最为显著：LUAD 上 c-index 降低 **5.42%**，UCEC 上降低 **7.03%**。这表明多方向复合扫描是模型性能的最大贡献者，单一方向扫描无法充分捕获 WSI 的多角度长程依赖和基因组的稀疏关联。

**专家驱动跨模态交互模块（EDIMI）的必要性。** 移除 EDIMI 模块后，LUAD 和 UCEC 上的 c-index 分别下降 **2.61%** 和 **4.60%**，验证了动态专家选择机制对于建模跨模态关系的重要性。

**对齐损失的有效性。** 引入跨模态对齐损失 $\mathcal{L}_{\mathrm{cro}}$ 后，LUAD 和 UCEC 上的 c-index 分别提升 **3.13%** 和 **1.68%**；添加模态内冗余损失 $\mathcal{L}_{\mathrm{intra}}$ 后，分别提升 **1.78%** 和 **4.04%**。两项损失联合使用进一步提升了性能，证明对齐约束有效减少了跨模态和模态内的表示冗余。

**专家组合的互补优势。** 图4 展示了不同专家组合的性能比较。组合 CroMamFusion 和 CroAttFusion 专家（M+A）的效果最优，优于其他双专家组合及单专家方案（仅 A、仅 M、仅 S）。这体现了注意力机制与 Mamba 在模态融合中的互补优势：注意力擅长捕获全局跨模态依赖，而 Mamba 在线性复杂度下高效建模长序列交互。

**多方向扫描策略的有效性。** 表3 进一步验证了 MDCS 中各扫描方向的贡献。逐步增加扫描方向可稳定提升性能，五方向组合（水平+垂直+左斜+右斜+回环）达到最优，表明不同方向捕获了互补的空间上下文信息。

**层次化 WSI 特征的必要性。** 表4 显示，仅使用 patch 级或 region 级特征均会导致性能显著下降，验证了同时利用 WSI 的局部细节和区域上下文对生存预测至关重要。

### 计算复杂度分析

表5 对比了 MoE-based 方法的参数量和 FLOPs。MDCS-MoAME 在保持可接受计算开销的前提下，取得了显著的性能提升。专家选择机制虽引入了额外的门控网络计算，但通过动态激活单个专家进行推理，实际计算量得到有效控制。

### 生存分析与特征可视化

**Kaplan-Meier 生存分析。** 图6 展示了基于预测风险分层的 Kaplan-Meier 曲线。在 LUAD 和 UCEC 数据集上，高风险组与低风险组之间存在显著差异（Log-rank p 值均远小于 0.05），表明模型能够有效区分不同预后风险的患者群体。

**特征分布可视化。** 图5 利用 t-SNE 对五方向扫描特征和两级聚合特征进行可视化。不同扫描方向产生的特征在嵌入空间中呈现互补分布，而两级聚合后的特征形成了更紧凑且判别性更强的簇结构，直观验证了多方向扫描和层次化聚合的有效性。

### 补充图表

![[assets/figures/papers/paper_list_l2131_https_openaccess_thecvf_com_content_CVPR2026_html_Qu_MDCS_MoAME_Multi_di/figures/004_Table_1.jpg]]
*Table 1: The c-index (mean ± std) performances on five datasets. The best and second-best results are highlighted in bold and underlined, respectively. The ⋆ mark indicates that the code has not been released, and we have reproduced their work*

![[assets/figures/papers/paper_list_l2131_https_openaccess_thecvf_com_content_CVPR2026_html_Qu_MDCS_MoAME_Multi_di/figures/005_Table_2.jpg]]
*Table 2: Results of ablation experiments on main modules*

![[assets/figures/papers/paper_list_l2131_https_openaccess_thecvf_com_content_CVPR2026_html_Qu_MDCS_MoAME_Multi_di/figures/007_Table_3.jpg]]
*Table 3: Effectiveness of the MDCS strategy*

![[assets/figures/papers/paper_list_l2131_https_openaccess_thecvf_com_content_CVPR2026_html_Qu_MDCS_MoAME_Multi_di/figures/008_Table_4.jpg]]
*Table 4: Effectiveness of hierarchical information*

![[assets/figures/papers/paper_list_l2131_https_openaccess_thecvf_com_content_CVPR2026_html_Qu_MDCS_MoAME_Multi_di/figures/006_Table_5.jpg]]
*Table 5: Computational complexity for MoE-based methods*

## 定位与知识库关联

### 多模态癌症生存预测的方法演进

癌症生存预测的核心挑战在于如何从高分辨率的全切片病理图像（WSI）和稀疏高维的基因组图谱中提取具有判别力的预后表征，并有效建模两者之间的复杂交互。该领域的方法演进大致经历了三个阶段：

**早期集合与注意力融合阶段。** 以 **DeepSets**（Zaheer et al., NIPS 2017）为代表的早期工作将WSI建模为实例集合，通过排列不变算子聚合patch特征，但忽略了patch间的空间拓扑关系。**MCAT**（Chen et al., ICCV 2021）引入基因组引导的协同注意力机制，使基因组信号可以指导图像关键区域的筛选，首次实现了模态间的信息交互。**SurvPath**（Jaume et al., CVPR 2024）进一步利用生物通路知识图谱将基因组数据组织为结构化令牌，增强了融合的生物学可解释性。然而，这些方法依赖注意力机制进行跨模态建模，其平方级计算复杂度在处理WSI的长序列时存在效率瓶颈，且感受野受限于单方向扫描。

**状态空间模型驱动的序列化阶段。** Mamba架构的引入为WSI建模提供了线性复杂度的替代方案。**CMTA**（Zhou and Chen, ICCV 2023）通过跨模态Transformer实现对齐，但未触及扫描方向问题。**PAM**（Huang et al., IEEE TMI 2025）采用局部感知扫描结合双向Mamba编码WSI，首次将Mamba应用于病理生存预测，但其扫描策略仍局限于水平方向，无法捕获垂直、对角等方向上的组织病理结构依赖。**SurvMamba**（Chen et al., arXiv 2024）探索了多粒度Mamba交互，但同样未突破单方向扫描的局限。对于基因组模态，现有方法普遍采用正向序列化策略，忽略了远距离基因群之间可能存在的稀疏关联。

**混合专家融合阶段。** 为应对模态融合的复杂性，**MoME**（Xiong et al., MICCAI 2024）和**PAMoE**等工作将混合专家（Mixture of Experts）引入多模态生存预测，通过多个融合专家增强模型容量。但这些方法的专家设计缺乏对注意力与Mamba两种融合范式互补优势的系统利用，且未引入显式的特征冗余抑制机制。

### MDCS-MoAME的创新定位

MDCS-MoAME在上述演进脉络中的核心贡献在于**同时解决了三个被现有工作独立忽视的瓶颈**：

| 瓶颈维度 | 现有方法局限 | MDCS-MoAME改进 |
|----------|-------------|----------------|
| 图像扫描方向 | 仅水平扫描（PAM, SurvMamba） | 水平、垂直、左斜、右斜、回环五方向复合扫描 |
| 基因组序列化 | 仅正向扫描 | 正向+间隔扫描，捕获远距离稀疏基因关联 |
| 跨模态融合 | 单一注意力或Mamba融合 | 混合注意力与Mamba专家（MoAME），门控动态选择 |
| 特征冗余 | 无显式约束 | 跨模态对齐损失L_cro + 模态内冗余损失L_intra |

从因果机制看，MDCS-MoAME的性能提升路径是：多方向扫描扩大感受野 → 充分挖掘模态内信息 → 动态专家灵活建模模态间交互 → 对齐约束抑制冗余 → 学习更具判别力的生存相关表征。消融实验为这一因果链提供了强证据：移除MDSFE模块（用原始Mamba替换）导致LUAD和UCEC上c-index分别下降5.42%和7.03%，是性能下降最显著的单模块消融（Table 2）；添加L_cro和L_intra分别带来1.68%–3.13%和1.78%–4.04%的提升。

### 适用边界与局限

**已验证的适用场景：** 当前方法在五个TCGA数据集（BLCA、BRCA、GBMLGG、LUAD、UCEC）上进行了系统验证，涵盖膀胱癌、乳腺癌、脑胶质瘤、肺腺癌和子宫内膜癌等不同癌种。在这些数据集上，MDCS-MoAME较PAM和SurvMamba分别平均提升14.61%和5.70%的c-index（Table 1），表现出跨癌种的稳定优势。

**明确的局限与未验证边界：**

1. **癌种泛化能力未知。** 当前验证仅限于TCGA五个数据集，该方法在其他癌种（如消化道肿瘤、血液肿瘤）或真实临床队列（可能存在数据质量差异、批次效应）上的表现尚未可知。

2. **模态覆盖有限。** 模型仅整合病理图像与基因组两个模态。临床实践中，放射影像（CT/MRI/PET）、临床报告文本、实验室检验等多模态数据同样蕴含预后信息，当前框架未纳入这些模态。

3. **特征提取器的固定性。** WSI特征提取依赖预训练ResNet-50，基因组特征通过简单全连接层映射。更强大的基础模型（如病理基础模型UNI、CONCH，或基因组大语言模型）可能进一步提升表示能力，但当前框架未对此进行探索。

4. **专家选择的次优风险。** MoAME的门控网络通过argmax进行离散专家选择，虽然具备动态性，但硬选择机制可能导致某些样本的次优路由，且训练过程中门控网络可能偏向某一专家。

5. **计算开销的权衡。** 与简单融合方法相比，多方向扫描和多专家机制引入了额外计算开销。Table 5提供了MoE-based方法的复杂度对比，但未与非MoE方法（如SurvPath、MCAT）进行直接比较。

6. **监督范式限制。** 当前方法聚焦于全监督生存分析，在自监督预训练或弱监督（如仅有整体生存标签而无精细标注）场景下的表现有待探索。

### 开放问题与未来方向

从方法谱系的角度，MDCS-MoAME开启了以下值得探索的方向：

- **多模态扩展的效率挑战。** 将多方向扫描策略推广至放射影像、临床文本等模态时，不同模态的序列化方式和扫描策略需要针对性设计，同时保持计算效率是一个非平凡问题。

- **扫描策略的通用性。** 多方向复合扫描的核心思想——通过改变序列化方向扩大感受野——是否可以推广至其他长序列建模任务（如视频帧序列分析、全基因组序列预测、长文档理解）值得探索。

- **专家选择的进一步优化。** 当前的门控网络采用简单的argmax选择，引入强化学习或贝叶斯优化可能实现更优的专家路由，同时降低训练不稳定性。

- **真实场景鲁棒性。** 在数据极度稀疏（如罕见癌种）、标签噪声较大（如随访数据不完整）的真实临床场景下，模型的鲁棒性需要进一步验证。

- **可解释性的深化。** 多方向扫描捕获的各类方向特征是否对应不同的组织病理学意义（如水平方向捕获基底膜方向性、垂直方向捕获腺体极性），以及专家选择是否具有可解释的模式，是连接模型机制与临床知识的重要桥梁。

## 原文 PDF

![[paperPDFs/CVPR_2026/MDCS_MoAME_Multi_directional_Composite_Scanning_with_Mixture_of_Attention_and_Mamba_Experts_for_Cancer_Survival_Prediction.pdf]]
