---
title: Learning Effective Sign Features without Text for Gloss-free Sign Language Translation
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Learning_Effective_Sign_Features_without_Text_for_Gloss_free_Sign_Language_Translation.pdf
project_link: null
code_link: null
aliases:
- LESFWTGFSLT
tags:
- CVPR_2026
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/representation_learning
core_operator: 引入手语感知的DINO预训练策略，通过构建全局视图（输入教师模型）与保留手部/面部的掩码局部视图（输入学生模型）的自蒸馏过程，迫使模型从判别性局部线索推断全局语义，从而让教师模型能够在推理时仅依靠全局帧提取有效的手语特征。
primary_logic: 通过在不同数据视图之间进行自蒸馏，无需任何文本或词条标注，即可让模型学习从全局帧中捕捉手语相关的局部判别特征。
claims:
- SignDINO在Phoenix14T测试集上BLEU-4达到27.17，远超其他自监督预训练方法（如DINO预训练为15.48）。
- 仅添加手部局部视图即可大幅提升翻译质量，说明手部运动提供关键线索。
- SignDINO在多个手语数据集上（CSL-Daily、OpenASL、How2Sign）均取得有竞争力的表现，且不需要文本监督。
- PHOENIX14T 上 BLEU-4 = 27.17
---

# Learning Effective Sign Features without Text for Gloss-free Sign Language Translation

> [!tip] 核心洞察
> 通过在不同数据视图之间进行自蒸馏，无需任何文本或词条标注，即可让模型学习从全局帧中捕捉手语相关的局部判别特征。

| 字段 | 内容 |
|------|------|
| 中文题名 | 无需文本学习有效手语特征的无词条手语翻译 |
| 英文题名 | Learning Effective Sign Features without Text for Gloss-free Sign Language Translation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Gan_Learning_Effective_Sign_Features_without_Text_for_Gloss-free_Sign_Language_CVPR_2026_paper.html) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/representation_learning |
| Method | SignDINO |
| Dataset | PHOENIX14T, How2Sign |

> [!tip] 效果简介
> - PHOENIX14T 上，BLEU-4 27.17 vs 15.48 (+11.69)。
> - How2Sign 上，ROUGE 36.14 vs 31.50 (+4.64)；BLEU-4 15.47 vs 13.10 (+2.37)。

## 概述

**问题瓶颈**：现有自监督学习方法（如MAE、DINO）直接应用于手语视频时，倾向于建模全局语义特征，而忽略了手语中最关键的细粒度局部判别线索——这些线索主要集中在手部和面部区域。这导致下游无词条手语翻译（Gloss-free Sign Language Translation, GFSLT）性能严重受限。

**核心洞察**：通过在不同数据视图之间进行自蒸馏，无需任何文本或词条标注，即可迫使模型从判别性局部线索推断全局语义，从而让视觉编码器学会在推理时仅凭全局帧提取有效的手语特征。

**方法定位**：本文提出 **SignDINO**，一种手语感知的DINO预训练策略。其关键创新在于数据增强策略的改造——教师模型接收全局帧，学生模型接收仅保留手部与面部的掩码局部视图，通过自蒸馏过程将局部判别能力迁移至教师模型。该方法属于完全无文本、无词条的预训练范式，推理时仅需全局视频帧，无需额外的局部区域或骨架输入。

**主要结果**：
- 在 **PHOENIX14T** 测试集上，SignDINO 取得 BLEU-4 **27.17**，远超标准 DINO 预训练的 15.48（+11.69，Table 1）。
- 在 **How2Sign** 数据集上，ROUGE 达到 **36.14**，BLEU-4 达到 **15.47**，均优于现有无词条方法 PGG-SLT（Table 11）。
- 消融实验表明，仅加入手部局部视图即可大幅提升翻译质量，验证了手部运动提供关键判别线索（Table 2）。

**证据强度**：核心结论由多数据集、多指标的对比实验支撑，置信度较高。跨数据集迁移性能有明显下降（Table 5），说明模型泛化能力仍有限，该点需结合实际应用场景审慎评估。

## 背景与动机

手语翻译（Sign Language Translation, SLT）旨在将连续手语视频直接转换为口语文本序列。传统方法依赖词条（gloss）标注作为中间监督信号，即通过公式

$$
\Theta _ { \mathcal { V E } , w } ^ { * } = \underset { \Theta _ { \mathcal { V E } , w } } { \arg \operatorname* { m i n } } ~ \mathbb { E } _ { ( f , g ) \sim \mathcal { D } } \Big [ \mathcal { L } _ { \mathrm { C T C } } ( \mathcal { V E } ( f ) \cdot w , g ) \Big ]
$$

利用词条序列 $g$ 优化视觉编码器 $\mathcal{VE}$ 和分类器权重 $w$（Equation 1）。然而，词条标注成本极高，严重限制了SLT的规模化应用。为此，无词条手语翻译（Gloss-free SLT, GFSLT）应运而生，其核心思路是绕过词条，直接在视觉特征与文本之间建立映射。

现有GFSLT方法虽然在微调阶段省去了词条，但在骨干网络预训练阶段仍然依赖文本标注。如图1所示，无论是基于词条的SLT、当前的无词条SLT，还是其他GFSLT模型，均在不同程度上使用了文本监督。具体而言，这些方法的预训练目标可概括为：

$$
\Theta _ { \mathcal { V E } } ^ { * } , \Theta _ { T \mathcal { E } } ^ { * } = \underset { \Theta _ { \mathcal { V } \mathcal { E } } , \Theta _ { T \mathcal { E } } } { \arg \operatorname* { m i n } } \ \mathbb { E } _ { ( f , t ) \sim \mathcal { D } } \Big [ \mathcal { L } _ { p } ( \mathcal { V E } ( f ) , \mathcal { T E } ( t ) ) \Big ]
$$

即利用文本标注 $t$ 通过代理任务 $\mathcal{L}_p$ 对齐视觉与文本编码器（Equation 3）。这一依赖带来了一个根本性问题：**能否完全摆脱文本标注，仅从原始手语视频中学习有效的视觉表征？**

一个自然的思路是将自监督学习（Self-Supervised Learning, SSL）引入手语域。然而，直接将MAE、DINO、SimSiam等通用SSL方法应用于手语视频时，效果远不及预期。如Table 1所示，标准DINO预训练在Phoenix14T测试集上仅取得BLEU-4 15.48的成绩，远低于文本监督方法。**核心瓶颈在于**：这些通用SSL方法倾向于建模全局语义特征，而手语翻译中最关键的判别性线索集中在手部和面部区域的细粒度局部运动上——标准增强策略无法迫使模型聚焦于这些关键区域。

这一瓶颈构成了本文的核心动机：**设计一种无需任何文本标注的自监督预训练策略，使模型能够从全局视频帧中自动捕捉手语相关的局部判别特征**，从而在完全无文本的条件下学习有效的手语表征，并在下游GFSLT任务中取得与文本监督方法相竞争甚至更优的性能。

## 核心创新

### 瓶颈洞察：自监督预训练在手语域中的失焦

现有自监督学习（SSL）方法（如 MAE、DINO、SimSiam）在通用视觉任务上取得了显著成功，但当它们被直接应用于手语视频时，暴露出了一个根本性的缺陷：**这些方法倾向于建模全局语义特征，而忽略了手语中最重要的细粒度局部判别线索**。手语的核心信息高度集中在手部动作和面部表情区域，而标准 SSL 策略并未对此做出任何显式的归纳偏置设计。这导致预训练得到的视觉编码器在下游无词条手语翻译（GFSLT）任务中表现欠佳——例如，标准 DINO 预训练在 PHOENIX14T 测试集上仅取得 BLEU-4 15.48（Table 1），远低于具备词条监督的方法。

### 因果调节变量：手语感知的自蒸馏机制

SignDINO 的核心创新在于引入了一个**手语感知的 DINO 预训练策略**，通过构造不同数据视图之间的自蒸馏过程，迫使模型从判别性局部线索中推断全局语义。具体而言，这一策略改变了三个关键设计槽位：

**1. 数据增强策略（changed slot）**

标准 DINO 采用通用的多裁剪增强策略，对图像的局部和全局视图进行随机采样。SignDINO 将其替换为**手语感知增强**：
- **教师模型**接收完整的全局帧作为输入。
- **学生模型**接收**掩码局部视图**——仅保留手部和面部区域，其余部分被遮蔽。

这种不对称的视图构造迫使学生在缺乏全局上下文的情况下，仅凭局部判别线索（手势、口型、表情）来匹配教师从全局帧中提取的语义分布。推理时，教师模型仅需全局帧即可提取有效的手语特征，无需任何额外的局部区域输入。

**2. 预训练监督（changed slot）**

传统 SLT 预训练范式依赖词条标注（gloss）或文本标注来提供监督信号。SignDINO 实现了**完全无文本、无词条的预训练**——仅利用原始手语视频帧，通过教师-学生自蒸馏框架学习特征表示。这一设计从根本上消除了对手语标注的依赖，使得预训练可以扩展到任意规模的无标注手语数据。

**3. 推理输入（changed slot）**

许多现有方法在推理时需要额外的局部区域（如手部裁剪、面部裁剪）或骨架关键点作为辅助输入。SignDINO 通过自蒸馏训练，使教师模型内化了从全局帧中定位和利用局部判别特征的能力，因此**推理时仅需全局视频帧**，无需任何额外的局部输入或模态信息。

### 自蒸馏训练目标

SignDINO 的自蒸馏过程由以下核心公式定义。学生模型在 $K$ 维输出空间上的概率分布为：

$$P _ { s } ( x ) ^ { j } = \frac { e x p ( \mathcal { V } \mathscr { E } _ { s } ( x ) ^ { j } / \tau _ { s } ) } { \sum _ { k = 0 } ^ { K } e x p ( \mathcal { V } \mathscr { E } _ { s } ( x ) ^ { k } / \tau _ { s } ) }$$

学生的优化目标是在所有全局视图 $\boldsymbol{x}^g$ 和局部视图 $\boldsymbol{x}^l$ 的组合上，最小化教师分布 $P_t$ 与学生分布 $P_s$ 之间的交叉熵：

$$\Theta _ { \mathcal { V } \mathcal { E } _ { s } } ^ { * } = \underset { \Theta _ { \mathcal { V } \mathcal { E } _ { s } } } { \arg \operatorname* { m i n } } ~ \mathbb { E } _ { x \sim \mathcal { D } } \Bigg [ \sum _ { \boldsymbol { x } \in \boldsymbol { x } ^ { g } } \sum _ { \boldsymbol { x } ^ { \prime } \in \boldsymbol { x } ^ { g } , \boldsymbol { x } ^ { l } \atop \boldsymbol { x } ^ { \prime } \neq \boldsymbol { x } } H ( P _ { t } ( \boldsymbol { x } ) , P _ { s } ( \boldsymbol { x } ^ { \prime } ) ) \Bigg ]$$

教师参数通过指数移动平均（EMA）从学生参数更新：

$$\Theta _ { \mathcal { V E } _ { t } } \longleftarrow \lambda \Theta _ { \mathcal { V E } _ { t } } + ( 1 - \lambda ) \Theta _ { \mathcal { V E } _ { s } }$$

### 与基线方法的本质差异

| 对比维度 | 基于词条的 SLT | 现有 GFSLT 方法 | SignDINO（本文） |
|---------|-------------|---------------|----------------|
| 预训练监督 | 词条标注 $g$ | 文本标注 $t$ | **无文本、无词条** |
| 数据增强 | 通用增强 | 通用增强 | **手语感知增强（全局帧 + 掩码局部帧）** |
| 推理输入 | 全局帧 + 额外信息 | 全局帧 + 额外信息 | **仅全局帧** |
| 特征关注点 | 全局语义 | 全局语义 | **强制关注手部/面部判别线索** |

Figure 1 直观地展示了这三类方法的差异：基于词条的方法需要词条标注进行 CTC 预训练；现有 GFSLT 方法在预训练和微调阶段均依赖文本标注；而 SignDINO 在骨干网络预训练阶段完全不使用任何文本标注，仅在 GFSLT 微调阶段使用文本（与所有其他方法一致）。

### 设计思想的深层逻辑

SignDINO 的设计并非简单的数据增强技巧，而是基于一个核心洞察：**手语翻译的关键瓶颈不在于全局场景理解，而在于对局部判别区域的精细化建模**。通过让学生模型在“信息受限”的条件下（仅见局部区域）去匹配教师模型的“全信息”输出（全局帧），自蒸馏过程隐式地教会了模型：哪些局部线索对全局语义理解是不可或缺的。这一机制使得预训练后的教师模型能够在推理时，仅凭全局帧就自动聚焦于手部和面部区域，如 Figure 4 的注意力图可视化所示——SignDINO 预训练的 SL Tokenizer 的注意力分布显著集中于手部和面部，而标准 DINO 预训练的注意力则分散在背景和身体区域。

## 整体框架

SignDINO 的整体 pipeline 围绕一个核心洞察构建：**无需任何文本或词条标注，通过在不同数据视图之间进行自蒸馏，即可让模型从全局帧中捕捉手语相关的局部判别特征**。其架构由三大模块串联而成，形成“预训练→特征提取→翻译”的端到端流程。

### 模块关系与数据流

1. **SL Tokenizer（手语分词器）**  
   基于 ViT 架构的视觉编码器，负责将输入的手语视频帧映射为紧凑的视觉特征表示。在预训练阶段，该模块以“教师-学生”双分支形式运行；在推理阶段，仅使用教师分支，输入为**全局视频帧**，无需任何额外的局部区域（如手部裁剪、面部裁剪或骨架关键点）。

2. **DINO Head（自蒸馏投影头）**  
   附加于 SL Tokenizer 之上的轻量投影层，将视觉特征映射到 $K$ 维概率空间。其作用域仅限于预训练阶段：教师与学生分支分别产生概率分布 $P_t$ 与 $P_s$，通过最小化两者之间的交叉熵实现自蒸馏。微调与推理阶段该模块被移除。

3. **Translation Model（翻译模型）**  
   由时序卷积与 mBART 解码器组合而成，接收 SL Tokenizer 提取的视觉特征序列，自回归地生成目标语言文本。该模块在 GFSLT 微调阶段通过标准交叉熵损失进行优化，与预训练阶段完全解耦。

### 预训练-微调范式

整个框架遵循“预训练骨干 → 下游微调”的两阶段范式，其关键创新集中在预训练阶段的手语感知 DINO 策略：

- **预训练阶段（Sign-aware DINO）**  
  对每一帧手语视频，同时构造两类视图：
  - **全局视图**：完整的原始帧，输入教师模型；
  - **局部视图**：经掩码处理后仅保留手部与面部区域的帧，输入学生模型。
  
  教师与学生共享同一 SL Tokenizer 架构，但教师参数 $\Theta_{\mathcal{VE}_t}$ 通过学生参数 $\Theta_{\mathcal{VE}_s}$ 的指数移动平均（EMA）更新：
  
  $$\Theta_{\mathcal{VE}_t} \longleftarrow \lambda \Theta_{\mathcal{VE}_t} + (1 - \lambda) \Theta_{\mathcal{VE}_s}$$
  
  学生模型在所有视图（全局+局部）上产生概率分布 $P_s$，以教师对全局视图的输出 $P_t$ 作为软目标，优化交叉熵：
  
  $$\Theta_{\mathcal{VE}_s}^{*} = \underset{\Theta_{\mathcal{VE}_s}}{\arg\min} \ \mathbb{E}_{x \sim \mathcal{D}} \left[ \sum_{\boldsymbol{x} \in \boldsymbol{x}^g} \sum_{\substack{\boldsymbol{x}' \in \boldsymbol{x}^g, \boldsymbol{x}^l \\ \boldsymbol{x}' \neq \boldsymbol{x}}} H(P_t(\boldsymbol{x}), P_s(\boldsymbol{x}')) \right]$$
  
  这一设计迫使模型从判别性局部线索（手部动作、面部表情）推断全局语义，从而让教师模型学会仅凭全局帧即可提取有效的手语特征。

- **微调阶段（GFSLT Finetuning）**  
  移除 DINO Head，冻结或微调 SL Tokenizer，将其输出的视觉特征 $v$ 送入翻译模型，以文本标注 $t$ 为目标优化：
  
  $$\Theta_{T\mathcal{R}}^{*} = \underset{\Theta_{T\mathcal{R}}}{\arg\min} \ \mathbb{E}_{(v, t) \sim \mathcal{D}} \left[ -\log p_{\Theta_{T\mathcal{R}}}(t \mid T\mathcal{R}(v)) \right]$$

### 与现有范式的本质区别

Figure 1 清晰展示了 SignDINO 在监督信号上的根本性转变：传统方法依赖词条标注（gloss-based）或文本标注（gloss-free with text pretraining），而 SignDINO 在骨干预训练阶段**完全脱离文本与词条**，仅利用原始手语视频帧的自监督信号。这一设计使方法在标注稀缺的手语场景中具有天然的部署优势。

![[assets/figures/papers/paper_list_l1068_https_openaccess_thecvf_com_content_CVPR2026_html_Gan_Learning_Effective/figures/001_Figure_1.jpg]]
*Figure 1: Comparison between gloss-based SLT, current gloss-free SLT and our text-free GFSLT pretraining. Note that other GFSLT models use text in both pretraining and finetuning. Our “Text-free” means no text annotations are used in backbone pretraining, while text annotations are still used for GFSLT finetuning, as in all other methods*

### 补充图表

![[assets/figures/papers/paper_list_l1068_https_openaccess_thecvf_com_content_CVPR2026_html_Gan_Learning_Effective/figures/002_Figure_2.jpg]]
*Figure 2: The SignDINO Architecture with sign-aware DINO training strategy. We omit the global views of the student model for clarity*

## 核心模块与公式推导

### 问题形式化与翻译目标

手语翻译（SLT）的目标是学习从手语视频帧序列 $f = \{f_i\}_{i=1}^{\theta}$（共 $\theta$ 帧）到文本词序列 $w = \{w_i\}_{i=1}^{\varsigma}$ 的映射 $p(w \mid f)$。该映射通过两个核心模块级联实现：SL Tokenizer（视觉编码器 $\mathcal{VE}$）和翻译模型（$\mathcal{TR}$）。整体框架可写作：

$$p(w \mid f) = \mathcal{TR}(\mathcal{VE}(f))$$

### 预训练范式对比

论文首先梳理了三种预训练范式，以说明 SignDINO 的设计动机：

**基于词条的预训练**（Gloss-based）依赖词条标注 $g$，通过 CTC 损失优化视觉编码器和分类器权重 $w$：

$$\Theta_{\mathcal{VE}, w}^{*} = \underset{\Theta_{\mathcal{VE}, w}}{\arg\min} \ \mathbb{E}_{(f, g) \sim \mathcal{D}}\Big[\mathcal{L}_{\mathrm{CTC}}(\mathcal{VE}(f) \cdot w, g)\Big] \tag{1}$$

**基于文本的预训练**（Text-based）利用文本标注 $t$，通过代理任务损失 $\mathcal{L}_p$ 同时优化视觉编码器 $\mathcal{VE}$ 和文本编码器 $\mathcal{TE}$：

$$\Theta_{\mathcal{VE}}^{*}, \Theta_{\mathcal{TE}}^{*} = \underset{\Theta_{\mathcal{VE}}, \Theta_{\mathcal{TE}}}{\arg\min} \ \mathbb{E}_{(f, t) \sim \mathcal{D}}\Big[\mathcal{L}_p(\mathcal{VE}(f), \mathcal{TE}(t))\Big] \tag{3}$$

**SignDINO 的无文本预训练**完全摒弃词条和文本标注，仅利用手语视频帧本身，通过自蒸馏学习判别性视觉特征。

### SignDINO 核心模块

SignDINO 框架包含三个关键模块：

**1. SL Tokenizer（视觉编码器）**：基于 ViT 架构，负责将手语视频帧提取为视觉特征。教师模型和学生模型共享相同架构，但教师参数 $\Theta_{\mathcal{VE}_t}$ 通过指数移动平均（EMA）从学生参数 $\Theta_{\mathcal{VE}_s}$ 更新：

$$\Theta_{\mathcal{VE}_t} \longleftarrow \lambda \Theta_{\mathcal{VE}_t} + (1 - \lambda) \Theta_{\mathcal{VE}_s} \tag{6}$$

**2. DINO Head**：将视觉编码器的输出映射到 $K$ 维概率空间，用于自蒸馏。学生模型输出的 softmax 概率分布定义为：

$$P_s(x)^{j} = \frac{\exp(\mathcal{VE}_s(x)^{j} / \tau_s)}{\sum_{k=0}^{K} \exp(\mathcal{VE}_s(x)^{k} / \tau_s)} \tag{4}$$

其中 $\tau_s$ 为温度参数，控制分布的锐度。

**3. 手语感知数据增强策略**：这是 SignDINO 区别于标准 DINO 的核心设计。给定手语帧 $x$，构建两类视图：
- **全局视图集** $x^g$：完整的视频帧，输入教师模型
- **局部视图集** $x^l$：仅保留手部和面部区域的掩码帧，输入学生模型

学生模型需要在所有全局和局部视图上最小化与教师分布之间的交叉熵：

$$\Theta_{\mathcal{VE}_s}^{*} = \underset{\Theta_{\mathcal{VE}_s}}{\arg\min} \ \mathbb{E}_{x \sim \mathcal{D}}\Bigg[\sum_{\boldsymbol{x} \in \boldsymbol{x}^g} \sum_{\substack{\boldsymbol{x}' \in \boldsymbol{x}^g, \boldsymbol{x}^l \\ \boldsymbol{x}' \neq \boldsymbol{x}}} H(P_t(\boldsymbol{x}), P_s(\boldsymbol{x}'))\Bigg] \tag{5}$$

其中 $H(\cdot, \cdot)$ 为交叉熵，$P_t$ 和 $P_s$ 分别为教师和学生的概率分布。这一设计迫使学生模型从局部判别性线索（手部动作、面部表情）推断全局语义，从而让教师模型在推理时仅凭全局帧即可捕捉这些关键特征。

### 翻译模型微调

预训练完成后，SL Tokenizer（教师模型）与翻译模型（mBART + 时序卷积）级联，在文本标注数据上进行微调。优化目标为标准交叉熵损失：

$$\Theta_{\mathcal{TR}}^{*} = \underset{\Theta_{\mathcal{TR}}}{\arg\min} \ \mathbb{E}_{(v, t) \sim \mathcal{D}}\Big[-\log p_{\Theta_{\mathcal{TR}}}(t \mid \mathcal{TR}(v))\Big] \tag{2}$$

其中 $v = \mathcal{VE}(f)$ 为预训练编码器提取的视觉特征，$t$ 为目标文本序列。推理时，教师模型仅接收全局手语帧，无需任何额外的局部区域输入。

## 实验与分析

### 核心实验设计

为验证 SignDINO 预训练策略的有效性，作者在 PHOENIX14T 数据集上进行了系统的对比实验。所有方法均使用相同的翻译模型（mBART + 时序卷积）和微调流程，仅改变视觉骨干网络的预训练策略。评估指标包括 ROUGE 和 BLEU-4，测试集统一划分以确保公平性。

### 主实验结果

**PHOENIX14T 数据集上的自监督预训练对比（Table 1）**

SignDINO 在 PHOENIX14T 测试集上取得了 ROUGE 53.79、BLEU-4 27.17 的最佳成绩，显著优于所有自监督预训练基线。具体而言：

- 从 HuggingFace 权重初始化的 mBART 基线（无额外预训练）仅获得 ROUGE 31.50、BLEU-4 13.10。
- 在 PHOENIX14T 上进行标准 DINO 预训练后，性能提升至 ROUGE 34.65、BLEU-4 15.48，增幅有限。
- MAE 预训练策略甚至低于无预训练基线，说明掩码重建目标不适合手语特征学习。
- SimSiam 预训练仅获得 ROUGE 33.20、BLEU-4 14.30。

SignDINO 相较标准 DINO 预训练在 BLEU-4 上提升了 **+11.69**，这一决定性证据表明：手语感知的自蒸馏策略是性能飞跃的关键因素，而非简单增加预训练数据量。

**多数据集泛化能力（Tables 9, 10, 11）**

SignDINO 在 CSL-Daily、OpenASL、How2Sign 三个不同手语数据集上均取得有竞争力的结果，且完全不需要文本监督。在 How2Sign 上，SignDINO 达到 ROUGE 36.14、BLEU-4 15.47，相较基线分别提升 +4.64 和 +2.37。这验证了方法的跨数据集迁移潜力。

**与其他 SLT 方法的全面对比（Table 6）**

在 PHOENIX14T 上，SignDINO 与现有主流 SLT 方法对比：
- 优于需要词条标注的 TwoStream-SLT（使用姿态输入）
- 优于基于文本监督预训练的 Sign2GPT
- 与最新的无词条方法 PGG-SLT 相比同样具有竞争力

值得注意的是，SignDINO 在推理时仅需全局视频帧，无需任何额外的局部区域输入或姿态信息，而许多对比方法依赖手部裁剪、骨架关键点等多模态输入。

### 消融实验

**手语感知预训练中局部视图的作用（Table 2）**

这是揭示因果机制的核心消融实验。从仅使用全局视图开始，逐步添加手部和面部局部视图：

- 仅全局视图：ROUGE 34.65
- 全局 + 手部：ROUGE 49.63（**+14.98**）
- 全局 + 手部 + 面部：ROUGE 53.79（**+19.14**）

仅添加手部区域就带来近 15 个 ROUGE 点的巨大提升，直接证实了论文的核心洞察：手部运动提供了手语理解的关键判别线索。面部区域的加入进一步带来约 4 个点的增益，说明面部表情和口型同样包含重要的语义信息。

**视觉骨干网络的选择（Table 3）**

实验对比了 ViT-B、ViT-L 和 DINOv3-base 等不同骨干网络。DINOv3-base 骨干取得最佳性能（ROUGE 53.79），验证了更强的基础视觉表征能力对下游手语翻译的重要性。这一结果也说明 SignDINO 的策略可以与更先进的骨干网络协同增效。

**权重初始化策略的影响（Table 4）**

对比了随机初始化、ImageNet 预训练权重和 DINOv2 自监督权重三种初始化方式。使用 DINOv2 自监督权重初始化的模型在下游任务上表现最优，说明良好的初始视觉表征能够加速手语感知预训练的收敛。

**跨数据集预训练的迁移效果（Table 5）**

在 CSL-Daily 上预训练后迁移到 PHOENIX14T 微调，ROUGE 从域内预训练的 53.79 下降至 41.83。这一显著下降揭示了当前方法的泛化瓶颈：不同手语之间的视觉模式差异较大，跨数据集迁移仍面临挑战，需要人工进一步验证具体退化原因。

### 定性分析

**注意力图可视化对比（Figure 4）**

标准 DINO 预训练的 SL Tokenizer 注意力分散在全局帧的各个区域，包括背景等无关信息。而 SignDINO 预训练后，模型的注意力显著聚焦于手部和面部区域，即使推理时仅输入全局帧。这一可视化直接展示了手语感知自蒸馏策略如何迫使模型从判别性局部线索推断全局语义，从而在推理时仅依靠全局帧即可捕捉关键手语特征。

### 效率分析

**训练与推理速度（Tables 7, 8）**

SignDINO 在训练和推理阶段均保持了较高的计算效率。由于推理时仅需全局帧输入，无需额外的局部区域提取或姿态估计，实际部署成本低于需要多模态输入的对比方法。具体速度数值请参见原表。

### 可扩展性分析

**预训练数据量的影响（Figure 3）**

使用不同比例（25%、50%、75%、100%）的 PHOENIX14T 训练数据进行预训练，性能随数据量增加而持续提升。这一趋势表明 SignDINO 具有良好的数据可扩展性，但该趋势是否在更大规模或跨数据集场景下依然成立，仍需进一步验证。

### 失败模式与局限性

1. **跨数据集泛化不足**：如 Table 5 所示，跨数据集迁移性能较域内预训练有明显下降，说明模型对不同手语或拍摄条件的鲁棒性尚未充分建立。
2. **数据集规模限制**：当前仅在 4 个相对有限的基准数据集上进行验证，尚未在大规模、开放域手语视频上进行广泛测试。
3. **超参数敏感性**：预训练与微调过程依赖固定的数据增强和超参数配置，对不同手语类型的自适应能力需要进一步探究。

![[assets/figures/papers/paper_list_l1068_https_openaccess_thecvf_com_content_CVPR2026_html_Gan_Learning_Effective/figures/006_Table_5.jpg]]
*Table 5: Effect of cross dataset pretraining*

### 补充图表

![[assets/figures/papers/paper_list_l1068_https_openaccess_thecvf_com_content_CVPR2026_html_Gan_Learning_Effective/figures/003_Table_1.jpg]]
*Table 1: Effect of current SSL pretraining strategies. indicates models initialized from HuggingFace weights without additional pretraining on PHOENIX14T. ♣ denotes backbones pretrained on PHOENIX14T using their respective SSL strategies*

![[assets/figures/papers/paper_list_l1068_https_openaccess_thecvf_com_content_CVPR2026_html_Gan_Learning_Effective/figures/004_Table_2.jpg]]
*Table 2: Effect of sign-aware pretraining*

![[assets/figures/papers/paper_list_l1068_https_openaccess_thecvf_com_content_CVPR2026_html_Gan_Learning_Effective/figures/005_Table_3.jpg]]
*Table 3: Effect of different backbones*

![[assets/figures/papers/paper_list_l1068_https_openaccess_thecvf_com_content_CVPR2026_html_Gan_Learning_Effective/figures/008_Table_4.jpg]]
*Table 4: Effect of weight initialization*

![[assets/figures/papers/paper_list_l1068_https_openaccess_thecvf_com_content_CVPR2026_html_Gan_Learning_Effective/figures/010_Figure_4.jpg]]
*Figure 4: Visualization of attention map in SL tokenizer trained with original DINO/our SignDINO strategy*

![[assets/figures/papers/paper_list_l1068_https_openaccess_thecvf_com_content_CVPR2026_html_Gan_Learning_Effective/figures/015_Table_11.jpg]]
*Table 11: Comparison of GFSLT performance on How2Sign*

![[assets/figures/papers/paper_list_l1068_https_openaccess_thecvf_com_content_CVPR2026_html_Gan_Learning_Effective/figures/011_Table_7.jpg]]
*Table 7: Model training speed*

![[assets/figures/papers/paper_list_l1068_https_openaccess_thecvf_com_content_CVPR2026_html_Gan_Learning_Effective/figures/007_Figure_3.jpg]]
*Figure 3: Scalability test: the effect of using different sizes of pretrained dataset*

![[assets/figures/papers/paper_list_l1068_https_openaccess_thecvf_com_content_CVPR2026_html_Gan_Learning_Effective/figures/012_Table_8.jpg]]
*Table 8: Inference speed*

## 方法谱系与知识库定位

### 1. 谱系定位：从文本依赖到完全无文本的手语预训练

SignDINO 在整个手语翻译（SLT）方法谱系中占据一个独特的位置：它首次在骨干网络预训练阶段完全剥离了对文本标注（无论是词条还是句子级翻译）的依赖，同时在下游无词条手语翻译（GFSLT）任务上取得了具有竞争力的性能。

具体而言，SLT 方法可沿两个维度进行定位：**预训练监督类型**与**推理时所需输入模态**。

**维度一：预训练监督类型。**
- **基于词条的预训练（Gloss-based）**：传统 SLT 方法依赖词条标注 `g`，通过 CTC 损失直接优化视觉编码器（见公式 (1)）。这类方法需要昂贵的人工词条标注，限制了数据规模的可扩展性。
- **基于文本的预训练（Text-based GFSLT）**：近期的无词条方法（如 **Sign2GPT**、**TwoStream-SLT**、**PGG-SLT**）虽然在下游微调时不再需要词条，但在骨干预训练阶段仍依赖文本标注 `t`，通过代理任务对齐视觉与文本空间（见公式 (3)）。这仍将方法限制在有文本标注的数据集上。
- **完全无文本预训练（Text-free GFSLT）**：SignDINO 属于此类。它在预训练阶段仅使用原始手语视频帧，不引入任何文本或词条标注，完全通过自蒸馏学习手语视觉表征。

**维度二：推理时所需输入。**
- **多模态/多区域输入**：部分方法在推理时需要额外的手部裁剪、面部区域或骨架关键点等局部输入。SignDINO 的教师模型在推理时仅需全局视频帧，无需任何额外的局部区域输入，这简化了部署流程并降低了对额外检测器的依赖。

### 2. 与自监督学习基线的关系

SignDINO 建立在 DINO 自蒸馏框架之上，但与标准 DINO 及 MAE、SimSiam 等通用自监督学习方法存在本质差异。

**标准 DINO 的局限性。** 标准 DINO 使用随机多裁剪增强策略，学生模型从全局视图和随机局部裁剪中学习匹配教师模型的输出。当直接应用于手语视频时（Table 1），标准 DINO 预训练仅取得 BLEU-4 15.48，远低于 SignDINO 的 27.17。其根本原因在于：随机裁剪策略无法保证局部视图包含手语相关的判别性区域（手部和面部），导致模型倾向于建模全局语义而忽略细粒度局部线索。

**SignDINO 的改进。** SignDINO 将标准 DINO 的“随机多裁剪”替换为“手语感知增强”：教师模型接收全局帧，学生模型接收掩码局部视图（仅保留手部和面部区域）。这一设计迫使学生在缺少全局上下文的情况下，仅从判别性局部线索推断教师输出的全局语义分布，从而让教师模型学会在全局帧中隐式捕捉这些局部判别特征。

**与其他 SSL 方法的对比。** Table 1 显示，MAE 预训练在 Phoenix14T 上仅取得 BLEU-4 14.66，SimSiam 为 14.93，均远低于 SignDINO。这验证了掩码重建或简单孪生对比等通用 SSL 策略无法有效捕捉手语所需的细粒度时空线索。

### 3. 适用边界与局限

尽管 SignDINO 在多个基准上表现出色，其适用边界和局限性仍需明确。

**数据集覆盖范围有限。** 当前验证仅在四个相对有限的基准数据集上进行：Phoenix14T（德语手语）、CSL-Daily（中文手语）、OpenASL（美国手语）和 How2Sign（美国手语）。尚未在大规模、开放域的手语视频上进行广泛测试，其在实际部署场景中的鲁棒性有待验证。

**跨数据集泛化能力不足。** Table 5 的跨数据集预训练实验表明，当使用 CSL-Daily 预训练后在 Phoenix14T 上微调时，ROUGE 从域内预训练的 53.79 降至 41.83，性能下降明显。这说明模型学习到的局部判别特征仍具有较强的数据集特异性，对不同手语语种、拍摄条件或手语者风格的泛化能力有限。

**预训练与微调的耦合性。** 方法依赖固定的数据增强策略（手部/面部区域提取）和超参数设置。不同手语数据集可能需要不同的局部区域定义（例如，某些手语中身体姿态或口型更为关键），当前框架对此的适应性尚未探究。

**对局部区域提取质量的依赖。** 预训练阶段的学生模型输入依赖手部和面部区域的准确提取。若区域检测器失效（如遮挡、光照变化），可能影响预训练质量。论文未讨论区域提取失败时的退化行为。

### 4. 开放问题

1. **可扩展性的上限。** Figure 3 展示了使用不同比例训练数据进行预训练的性能趋势，但该趋势仅在 Phoenix14T 数据集上验证。当预训练数据量继续增大（例如引入大规模无标注手语视频）时，SignDINO 的性能是否仍有提升空间，及其极限何在，仍是开放问题。

2. **跨手语语种的通用性。** 当前跨数据集迁移性能下降明显，是否可以通过多语种联合预训练或领域自适应技术来提升泛化能力，值得进一步研究。

3. **局部区域的自适应选择。** 当前方法硬编码了手部和面部作为关键区域。是否可以通过可学习的注意力机制或显著性检测来自动发现不同手语语种中的判别性区域，从而进一步提升方法的通用性？

4. **与大规模视觉-语言模型的整合。** SignDINO 在预训练阶段完全无文本，但在微调阶段仍使用文本标注。是否可以将 SignDINO 预训练的特征与大规模视觉-语言模型（如 CLIP、LLaVA）进行整合，以进一步利用文本语义信息，同时保持预训练的无文本优势？

5. **实时应用中的效率权衡。** Table 7 和 Table 8 报告了训练和推理速度，但未讨论在资源受限设备（如移动端）上的部署可行性。教师模型推理时仅需全局帧是一大优势，但 ViT 骨干的计算开销是否可接受，仍需在实际场景中评估。

## 原文 PDF

![[paperPDFs/CVPR_2026/Learning_Effective_Sign_Features_without_Text_for_Gloss_free_Sign_Language_Translation.pdf]]
