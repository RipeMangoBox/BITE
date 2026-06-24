---
title: Prompt-Anchored Vision-Text Distillation for Lifelong Person Re-identification
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Prompt_Anchored_Vision_Text_Distillation_for_Lifelong_Person_Re_identification.pdf
project_link: null
code_link: "https://github.com/zu-zi/PAD"
aliases:
- PPAVTD
- PAVTDLPRI
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 利用预训练视觉-语言模型的冻结文本编码器作为跨域稳定的语义锚点，并通过非对称蒸馏机制（弱文本蒸馏 + 强EMA视觉蒸馏）解耦语义保持与域适应。
primary_logic: 将文本模态的语义稳定性引入终身学习：冻结的文本编码器提供隐式对齐锚点，配合轻量文本蒸馏抑制语义漂移，同时通过自适应视觉提示池和选择性解冻骨干实现增量可塑性。
claims:
- PAD在AKA-order1和AKA-order2的已见域和未见域上均取得了最优平均性能。
- 消融实验中，完整PAD（包含VA-Prompt、TEXKD和VISKD）相比仅使用VA-Prompt在已见域上提升显著。
- 弱文本蒸馏（T1–T3）比强文本蒸馏（T4–T5）性能更稳定，过强约束导致性能下降。
- VA-Prompt的激活相似度与域间特征相似度相关系数达0.77，验证了提示分配对域关系的捕捉。
---

# Prompt-Anchored Vision-Text Distillation for Lifelong Person Re-identification

> [!tip] 核心洞察
> 将文本模态的语义稳定性引入终身学习：冻结的文本编码器提供隐式对齐锚点，配合轻量文本蒸馏抑制语义漂移，同时通过自适应视觉提示池和选择性解冻骨干实现增量可塑性。

| 字段 | 内容 |
|------|------|
| 中文题名 | 提示锚定的视觉-文本蒸馏终身行人重识别 |
| 英文题名 | Prompt-Anchored Vision-Text Distillation for Lifelong Person Re-identification |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2605.05027) · [Code](https://github.com/zu-zi/PAD) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | PAD (Prompt-Anchored vision–text Distillation) |
| Dataset | AKA-order1 |

> [!tip] 效果简介
> - AKA-order1 (Market→CUHK-SYSU→Duke→MSMT17→CUHK03) 上，Seen-Avg mAP 70.7 vs 65.6 (DAFC) (+5.1)。
> - AKA-order1 上，Seen-Avg R1 81.0 vs 75.9 (DAFC) (+5.1)；Unseen-Avg mAP 78.6 vs 65.7 (DKP++) (+12.9)。

## 概述

终身行人重识别（Lifelong Person Re-identification, LReID）要求模型在顺序到达的多个监控域上持续学习，同时保持对已见身份的判别力，并泛化至未见域。现有免样本（exemplar-free）方法仅依赖视觉知识蒸馏来抑制遗忘，但在域累积过程中，视觉特征空间缺乏跨域稳定的参照系，导致已学习的身份语义逐渐漂移，这一**语义漂移**构成了当前范式的核心瓶颈。

本文提出**PAD（Prompt-Anchored vision–text Distillation）**，将预训练视觉-语言模型中的冻结文本编码器引入终身ReID，作为跨域稳定的语义锚点。核心思路是构建**非对称的双提示蒸馏机制**：在文本侧，通过可学习的TA-Prompt与固定文本教师之间的弱蒸馏，将视觉特征拉向稳定的文本语义坐标；在视觉侧，通过EMA动量的视觉教师进行多层次特征与logit蒸馏，保持域适应能力。同时，视觉自适应提示池（VA-Prompt）为每个新域分配专家提示槽位并冻结旧域提示，选择性解冻骨干最后几层Transformer块，实现增量可塑性与记忆保持的解耦。

**主要结果**：在AKA-order1（Market→CUHK-SYSU→Duke→MSMT17→CUHK03）上，PAD的已见域平均mAP达到70.7，相比此前最优方法DAFC（65.6）提升5.1个百分点；未见域平均mAP达到78.6，相比DKP++（65.7）提升12.9个百分点。消融实验证实，完整的双蒸馏组合相比仅使用VA-Prompt在已见域mAP上从65.3提升至70.7，弱文本蒸馏策略优于强蒸馏，选择性解冻最后4个Transformer块在性能与效率间取得最佳平衡。

## 背景与动机

终身行人重识别（Lifelong Person Re-identification, LReID）要求模型在连续到达的监控域流上逐步学习，同时保持对已见身份的判别能力并泛化至未见域。与标准ReID不同，LReID面临**稳定性-可塑性困境**：模型必须在不访问旧数据的前提下，既吸收新域知识，又防止已学语义被覆盖。

现有免样本回放（exemplar-free）方法主要依赖**视觉知识蒸馏**来维持旧知识：基于原型的策略存储类中心或分布信息，通过视觉特征蒸馏约束当前模型的漂移。然而，这一范式存在根本性瓶颈——**仅依赖视觉模态的蒸馏难以阻止语义漂移**。随着域累积，视觉特征空间中的身份语义逐渐混淆，已学习的判别结构被新域覆盖，导致已见域性能持续退化。

本文提出**PAD（Prompt-Anchored vision–text Distillation）**，核心动机在于将**文本模态的语义稳定性**引入终身学习。关键洞察是：预训练视觉-语言模型（如CLIP-ReID）中的**冻结文本编码器**天然构成一个跨域不变的语义坐标系统——无论视觉域如何变化，“穿着红色上衣的行人”这一文本描述对应的语义锚点始终固定。PAD利用这一属性，将文本空间作为全局锚点，配合非对称蒸馏机制（弱文本蒸馏 + 强EMA视觉蒸馏），解耦**语义保持**与**域适应**两个子问题，从而在无样本回放约束下实现更稳定的终身学习。

## 核心创新

PAD 的核心创新在于**将文本模态的语义稳定性引入终身行人重识别**，通过“冻结文本锚点 + 非对称双重蒸馏”机制，从根本上改变了免样本终身学习的语义保持方式。

### 从单一视觉蒸馏到视觉-文本双重蒸馏

传统免样本终身 ReID 方法（如 **LwF** (Li & Hoiem, PAMI 2017)、**PAEMA**、**DKP**、**DAFC**）仅依赖视觉模态的知识蒸馏来抑制灾难性遗忘。然而，视觉特征高度敏感于域分布偏移，仅靠视觉蒸馏难以阻止**语义漂移**——随着域累积，已学身份语义逐渐混乱（verified_analysis: real_bottleneck）。

PAD 的关键突破在于**引入预训练视觉-语言模型的冻结文本编码器作为跨域稳定的语义坐标系统**。该文本编码器在训练过程中完全不参与更新，为所有域提供统一的语义参照系。在此基础上，PAD 设计了两套非对称的提示机制和蒸馏策略：

| 创新维度 | 基线方法 | PAD 方法 | 作用 |
|---------|---------|---------|------|
| 模态利用 | 仅视觉蒸馏 | 视觉+文本双重蒸馏 | 文本锚点抑制语义漂移 |
| 文本编码器 | 无或可训练 | 冻结 | 提供跨域稳定语义坐标 |
| 文本侧提示 | 无 | TA-Prompt（可学习，弱蒸馏） | 对齐视觉-文本表征 |
| 视觉侧提示 | 无或单域提示 | VA-Prompt（域自适应扩展+冻结旧域） | 增量可塑性 |
| 视觉蒸馏策略 | 无或常规蒸馏 | EMA教师+多层次蒸馏 | 平滑视觉知识传递 |
| 骨干微调范围 | 全微调或无微调 | 选择性解冻最后几层 | 平衡可塑性与记忆保持 |

### 非对称蒸馏设计：弱文本蒸馏 + 强视觉蒸馏

PAD 的蒸馏策略体现了对两种模态本质差异的深刻理解：

- **弱文本蒸馏（TEXKD）**：文本侧仅对可学习的 TA-Prompt 施加轻量 KL 散度约束，教师为固定文本编码器。消融实验（Table 4）证实，弱文本蒸馏（T1–T3）性能显著优于强文本蒸馏（T4–T5），过强的文本正则化反而导致已见域和未见域性能下降。这表明文本锚点的作用是提供“语义引导”而非“严格约束”。

- **强视觉蒸馏（VISKD）**：视觉侧采用 EMA 动量更新的教师网络，同时在特征层和 logit 层施加蒸馏损失（$\mathcal{L}_{\mathrm{featKD}} + \mathcal{L}_{\mathrm{logitKD}}$），以应对视觉特征对域偏移的高敏感性。

### 域自适应提示池（VA-Prompt）

PAD 的视觉侧采用**自适应提示池**机制，灵感来源于 **DualPrompt** (Wang et al., ECCV 2022)。VA-Prompt 包含通用提示（G-Prompt）和专家提示（E-Prompt），当新域到达时分配新的提示槽位，同时冻结已有域的提示参数。实验表明，VA-Prompt 的激活相似度与域间特征相似度的相关系数达 **ρ = 0.77**（Section 4.4.1），验证了提示分配能有效捕捉域关系，实现结构化的增量学习。

### 选择性解冻骨干

区别于全微调或无微调的极端策略，PAD 仅解冻最后几个 Transformer 块及分类头。消融实验（Table S6）表明，解冻最后 4 个块在性能和效率间取得最佳平衡（已见域 mAP 70.7，可训练参数占比仅 26.07%），有效平衡了增量可塑性与旧知识保持。

### 因果逻辑链

冻结文本编码器 → 建立跨域稳定语义坐标 → TA-Prompt 弱蒸馏提供语义锚定 → 抑制语义漂移；VA-Prompt + 选择性解冻骨干 → 保留增量可塑性；EMA 视觉蒸馏 → 平滑视觉知识传递。两条路径协同，实现了**语义保持与域适应的解耦**——这是 PAD 相比纯视觉蒸馏方法的核心优势所在。

## 整体框架

PAD的整体架构由**非对称的双分支设计**构成：左侧为冻结的文本分支，提供跨域稳定的语义锚点；右侧为部分可训练的视觉分支，负责域自适应增量学习。两个分支通过**对称监督对比损失**和**多层次知识蒸馏**实现隐式与显式的语义对齐。图2展示了完整的框架结构。

### 文本分支：冻结编码器 + 可学习TA-Prompt

文本分支的核心是一个从预训练视觉-语言模型继承而来的**冻结文本编码器**。该编码器在终身学习全过程中参数保持不变，从而定义了一个稳定的语言语义坐标系。为了在保持稳定性的同时赋予一定的对齐灵活性，PAD引入了一组可学习的**文本锚点提示（TA-Prompt）**。TA-Prompt是唯一在文本侧参与训练的模块，其优化目标是通过对称监督对比损失将视觉特征拉向文本锚点，同时接受来自固定文本教师的**弱蒸馏**约束。

文本分支的设计遵循“弱蒸馏”原则：教师（冻结编码器输出的原始文本特征）在域内保持固定，不对其应用EMA更新。蒸馏强度通过温度缩放和KL散度控制，仅施加轻度正则化，避免过度约束对语义对齐的破坏。

### 视觉分支：选择性解冻骨干 + VA-Prompt池

视觉分支采用**选择性解冻策略**：仅解冻骨干网络最后几层Transformer块及分类头，其余层保持冻结。这一设计在可塑性与记忆保持之间取得平衡——解冻部分提供足够的域适应能力，冻结部分保留已学习的通用视觉知识。

为支持域增量学习，视觉分支配备了一个**视觉自适应提示池（VA-Prompt）**，其设计灵感源自DualPrompt（Wang et al., ECCV 2022）。VA-Prompt由两类互补的提示组成：

- **通用提示（G-Prompt）**：在所有域之间共享，捕获跨域不变的视觉模式。
- **专家提示（E-Prompt）**：为每个新域分配独立的提示槽位，学习域特定的视觉特征。当新域到达时，PAD扩展E-Prompt池并冻结旧域的专家提示，从而在增量学习过程中保护已学知识。

VA-Prompt的激活相似度与域间特征相似度呈强正相关（相关系数ρ=0.77），验证了提示分配机制有效捕捉了域间关系。

### 视觉蒸馏：EMA教师 + 多层次对齐

视觉分支的知识蒸馏采用**EMA动量更新的教师网络**。教师网络参数通过指数移动平均从学生网络平滑更新：

$$\theta_{\mathrm{tea}} \leftarrow \alpha \theta_{\mathrm{tea}} + (1 - \alpha) \theta_{\mathrm{stu}}$$

视觉蒸馏由两个层次组成：

- **特征蒸馏**（$\mathcal{L}_{\mathrm{featKD}}$）：将学生网络三层输出与EMA教师对应层特征对齐，使用均方误差损失。
- **Logit蒸馏**（$\mathcal{L}_{\mathrm{logitKD}}$）：基于文本特征锚点计算视觉特征的相似度分布，通过KL散度对齐学生与教师的分布。

由于视觉表征处于更细的粒度且对域分布偏移高度敏感，视觉蒸馏采用相对较强的权重。

### 跨模态对齐与训练目标

PAD的总体训练目标为四项损失的加权和：

$$\mathcal{L}_{\mathrm{overall}} = \mathcal{L}_{\mathrm{supcon}} + \mathcal{L}_{\mathrm{ID}} + \mathcal{L}_{\mathrm{triplet}} + \mathcal{L}_{\mathrm{KD}}$$

其中，$\mathcal{L}_{\mathrm{supcon}}$为**对称图像-文本监督对比损失**，实现视觉特征与文本特征的双向拉近；$\mathcal{L}_{\mathrm{ID}}$和$\mathcal{L}_{\mathrm{triplet}}$为行人重识别标准损失；$\mathcal{L}_{\mathrm{KD}}$为知识蒸馏损失，由文本侧logit蒸馏、视觉特征蒸馏和视觉logit蒸馏三部分加权组成：

$$\mathcal{L}_{\mathrm{KD}} = \lambda_{\mathrm{text}} \mathcal{L}_{\mathrm{TEXKD}} + \lambda_{\mathrm{feat}} \mathcal{L}_{\mathrm{featKD}} + \lambda_{\mathrm{logit}} \mathcal{L}_{\mathrm{logitKD}}$$

### 推理流程

推理阶段仅保留视觉分支：冻结的文本编码器和TA-Prompt在训练完成后被丢弃，仅使用视觉编码器进行特征提取和检索。这一设计确保了推理效率不受文本模态开销的影响。

### 补充图表

![[assets/figures/papers/paper_list_l776_https_arxiv_org_abs_2605_05027/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the proposed PAD framework. The framework consists of a textual branch (left) and a visual branch (right) that evolve across domains. On the textual side, we use a frozen text encoder and distill the learnable textual prompts (TA-Prompt). On the visual side, we construct a visual prompt (VA-Prompt) pool and train last layers of the image encoder with a two-term visual distillation loss. The textual branch provides semantic guidance during training, while only the image encoder is kept for inference*

## 核心模块与公式推导

PAD 的整体框架由两条非对称路径构成：**冻结的文本分支**提供跨域稳定的语义锚点，**部分可训练的视觉分支**负责域自适应学习。两条路径通过 TA-Prompt 和 VA-Prompt 两个提示机制协同工作。

### 2.1 双分支非对称架构

**文本分支（语义锚定）**：继承自预训练视觉-语言模型的文本编码器被完全冻结，仅维护一组可学习的 **TA-Prompt**（Text-Anchor Prompts）。TA-Prompt 通过对称监督对比损失与视觉特征对齐，并在域内通过固定的文本教师进行弱蒸馏，从而在不改变语义空间的前提下抑制漂移。

**视觉分支（域自适应）**：视觉编码器采用选择性解冻策略——仅解冻最后几层 Transformer 块和分类头，其余层保持冻结。同时，**VA-Prompt**（Visual-Adaptation Prompts）池为每个新域分配新的提示槽位，并冻结旧域提示，实现域增量学习。VA-Prompt 由通用提示（G-Prompt）和专家提示（E-Prompt）两部分组成，设计灵感源自 DualPrompt（Wang et al., ECCV 2022）。

**推理阶段**：仅保留视觉编码器，文本分支不参与推理，因此不引入额外推理开销。

### 2.2 训练目标

总体训练目标由四项损失加权构成：

$$\mathcal{L}_{\mathrm{overall}} = \mathcal{L}_{\mathrm{supcon}} + \mathcal{L}_{\mathrm{ID}} + \mathcal{L}_{\mathrm{triplet}} + \mathcal{L}_{\mathrm{KD}} \quad (1)$$

其中：
- $\mathcal{L}_{\mathrm{supcon}}$：对称图像-文本监督对比损失，将视觉特征与文本锚点双向拉近
- $\mathcal{L}_{\mathrm{ID}}$：身份分类损失
- $\mathcal{L}_{\mathrm{triplet}}$：三元组损失
- $\mathcal{L}_{\mathrm{KD}}$：知识蒸馏损失，是 PAD 的核心设计

### 2.3 知识蒸馏损失

PAD 的知识蒸馏采用非对称设计——文本侧弱蒸馏 + 视觉侧强 EMA 蒸馏：

$$\mathcal{L}_{\mathrm{KD}} = \lambda_{\mathrm{text}} \mathcal{L}_{\mathrm{TEXKD}} + \lambda_{\mathrm{feat}} \mathcal{L}_{\mathrm{featKD}} + \lambda_{\mathrm{logit}} \mathcal{L}_{\mathrm{logitKD}} \quad (2)$$

**文本蒸馏（TEXKD）——弱约束**：文本教师保持固定（不应用 EMA），仅对学生 TA-Prompt 施加轻量 KL 散度约束。温度缩放后的相似度分布对齐公式为：

$$q(v, t, \tau, \gamma) = \frac{\exp(\gamma (v \cdot t_{+}) / \tau)}{\sum_{i=1}^{K} \exp(\gamma (v \cdot t_{i}) / \tau)}$$

$$\mathcal{L}_{\mathrm{TEXKD}} = \tau^{2} D_{\mathrm{KL}}\big(q(v, t^{\mathrm{tea}}, \tau, \gamma) \| q(v, t^{\mathrm{stu}}, \tau, \gamma)\big) \quad (5)$$

其中 $\tau$ 为温度系数，$\gamma$ 为缩放因子，$t^{\mathrm{tea}}$ 为固定文本教师编码，$t^{\mathrm{stu}}$ 为 TA-Prompt 输出。

**视觉蒸馏（VISKD）——强约束**：视觉侧采用 EMA 教师，动量更新公式为：

$$\theta_{\mathrm{tea}} \leftarrow \alpha \theta_{\mathrm{tea}} + (1 - \alpha) \theta_{\mathrm{stu}} \quad (6)$$

视觉蒸馏包含两个层次：
- **特征蒸馏**：将学生网络三层输出与 EMA 教师的多层级特征对齐：

$$\mathcal{L}_{\mathrm{featKD}} = \frac{1}{3} \sum_{i=1}^{3} \| v_{i}^{\mathrm{stu}} - v_{i}^{\mathrm{tea}} \|_{2}^{2} \quad (7)$$

- **Logit 蒸馏**：基于文本特征锚点，对学生和教师视觉特征的相似度分布进行 KL 蒸馏：

$$\mathcal{L}_{\mathrm{logitKD}} = \tau^{2} D_{\mathrm{KL}}\big(q(\mathbf{v}^{\mathrm{tea}}, \mathbf{t}, \tau) \| q(\mathbf{v}^{\mathrm{stu}}, \mathbf{t}, \tau)\big) \quad (8)$$

**非对称设计的关键**：文本侧仅用弱蒸馏（小权重 $\lambda_{\mathrm{text}}$），因为文本空间本身已通过冻结编码器保持稳定；视觉侧则用强蒸馏（较大 $\lambda_{\mathrm{feat}}$ 和 $\lambda_{\mathrm{logit}}$），以对抗视觉分布漂移。消融实验证实，过强的文本蒸馏（如强 KL 约束）反而导致已见域和未见域性能下降（Table 4），验证了“弱文本 + 强视觉”非对称设计的必要性。

### 2.4 对称监督对比学习

TA-Prompt 通过双向 SupCon 损失实现隐式语义对齐：

$$\mathcal{L}_{\mathrm{supcon}} = \mathrm{SupCon}(\mathbf{v} \to \mathbf{t}) + \mathrm{SupCon}(\mathbf{t} \to \mathbf{v}) \quad (3)$$

该损失使视觉特征向文本锚点聚集，同时文本锚点也向视觉特征靠拢，形成双向语义约束。与显式蒸馏不同，这一隐式对齐不依赖教师模型，而是通过标签引导的对比学习建立视觉-文本联合空间。

### 补充图表

![[assets/figures/papers/paper_list_l776_https_arxiv_org_abs_2605_05027/figures/008_Figure_5.jpg]]
*Figure 5: Trainable parameter composition across domains. The textual side (a) updates only the TA-Prompt, while the visual side (b) trains the VA-Prompt, classifier head, and a small portion of the backbone. Ratios are normalized within trainable modules, excluding the frozen text encoder*

## 实验与分析

### 主实验结果

PAD在两种终身ReID评测协议（AKA-order1和AKA-order2）上均取得最优综合性能。在AKA-order1（Market-1501→CUHK-SYSU→DukeMTMC→MSMT17→CUHK03）下，PAD的已见域平均mAP达70.7，较此前最优方法DAFC（65.6）提升+5.1，已见域平均R1达81.0（DAFC为75.9）；未见域平均mAP达78.6，较DKP++（65.7）提升+12.9（Table 1）。在AKA-order2（DukeMTMC→MSMT17→Market-1501→CUHK-SYSU→CUHK03）下，PAD同样在已见域和未见域上取得最佳平均值（Table 2）。采用7个随机种子的统计结果显示，最终阶段已见域平均mAP为70.30±0.49、R1为80.98±0.31，验证了性能的统计可靠性。

![[assets/figures/papers/paper_list_l776_https_arxiv_org_abs_2605_05027/figures/004_Table_1.jpg]]
*Table 1: Performance comparison with state-of-the-art methods on AKA-order1. The optimal and suboptimal values are highlighted in red and blue, respectively. AKA-order1 is Market-1501→CUHK-SYSU→ DukeMTMC→MSMT17→CUHK03*

![[assets/figures/papers/paper_list_l776_https_arxiv_org_abs_2605_05027/figures/005_Table_2.jpg]]
*Table 2: Performance comparison with state-of-the-art methods on AKA-order2. The optimal and suboptimal values are highlighted in red and blue, respectively. AKA-order2 is DukeMTMC→MSMT17→Market-1501→ CUHK-SYSU→ CUHK03*

在LPW替换协议（将CUHK-SYSU替换为LPW数据集）下，PAD在两种训练顺序上仍保持最优或次优性能（Table S1、Table S2），表明方法对域组合变化具有鲁棒性。

![[assets/figures/papers/paper_list_l776_https_arxiv_org_abs_2605_05027/figures/010_Table_S.1.jpg]]
*Table S.1: Performance comparison with LReID methods on Training Order-1: Market-1501 → CUHK-SYSU → LPW → MSMT17 → CUHK03. The optimal and suboptimal values are highlighted in red and blue*

![[assets/figures/papers/paper_list_l776_https_arxiv_org_abs_2605_05027/figures/011_Table_S.2.jpg]]
*Table S.2: Performance comparison with LReID methods on Training Order-2: LPW → MSMT17 → Market-1501 → CUHK-SYSU → CUHK03. The optimal and suboptimal values are highlighted in red and blue*

从阶段性能趋势看，PAD在已见域上保持稳定，未见域性能随任务数增加而持续提升（Figure 3、Figure 4），体现了良好的稳定性-可塑性平衡。

![[assets/figures/papers/paper_list_l776_https_arxiv_org_abs_2605_05027/figures/003_Figure_3.jpg]]
*Figure 3: Performance tendency on seen domains (AKAorder1). After each training step, the model is evaluated on the already-seen domains*

![[assets/figures/papers/paper_list_l776_https_arxiv_org_abs_2605_05027/figures/006_Figure_4.jpg]]
*Figure 4: Performance tendency on unseen domains (AKAorder1). After each training step, the performance of all unseen domains is evaluated*

### 消融实验

#### 模块消融

Table 3在AKA-order1上逐模块验证PAD各组件的贡献。基线配置S1（全微调+无提示+无蒸馏）已见域mAP仅58.6。引入VA-Prompt（S2）后提升至65.3。在此基础上加入文本蒸馏TEXKD（S3）提升至67.7，加入视觉蒸馏VISKD（S4）提升至69.2。完整PAD（S5：冻结骨干+VA-Prompt+TEXKD+VISKD）取得最优已见域mAP 70.7，验证了各模块的协同增益。

#### 文本蒸馏强度

Table 4和Table S3考察文本蒸馏强度的影响。弱文本蒸馏（T1–T3）在已见域和未见域上性能稳定且优于无文本蒸馏配置；强文本蒸馏（T4–T5）导致性能下降，表明过强的文本侧正则化会损害模型的域适应能力。这一发现验证了PAD“弱文本蒸馏”设计原则的合理性。

#### 视觉蒸馏强度

Table S4考察视觉蒸馏强度（V1–V5，仅改变特征和logit蒸馏权重）。适度视觉蒸馏（V3）取得最佳性能，过强蒸馏（V5）导致性能饱和甚至下降，说明视觉侧需要相对强但不过度的蒸馏以平衡记忆保持与新域学习。

#### 骨干解冻范围

Table S6考察选择性解冻Transformer块数的影响。解冻最后4个块在性能和效率间取得最佳平衡（已见域mAP 70.7，可训练参数占比26.07%），验证了PAD“选择性解冻”策略的有效性。

### 提示机制分析

VA-Prompt的激活相似度与域间特征相似度呈强正相关（ρ=0.77），表明提示分配有效捕捉了域间关系（Section 4.4.1）。Figure 5展示了各域可训练参数的构成：文本侧仅更新TA-Prompt，视觉侧更新VA-Prompt、分类头及少量骨干层，总可训练参数控制在较低水平。

### 失败模式与局限性

尽管PAD在已见域和未见域上均取得最优平均性能，但在个别域上仍有提升空间。例如在AKA-order1中，DukeMTMC域的mAP为64.9、MSMT17域的mAP为46.9（Table 1），相比其他域明显偏低。这可能与这些域的数据分布差异较大、域间语义漂移更严重有关。

文本蒸馏强度目前依赖人工调节（λ_text权重的网格搜索），缺乏自适应机制。在域序列变化时，固定强度可能无法适配不同域间的语义距离差异。此外，当前方法仅处理图像模态与文本的对齐，尚未扩展到视频或换装ReID场景，在这些场景下冻结文本编码器的语义锚定能力有待验证。

### 补充图表

![[assets/figures/papers/paper_list_l776_https_arxiv_org_abs_2605_05027/figures/007_Table_3.jpg]]
*Table 3: Ablation study on AKA-order1. Columns indicate modules: Freeze—PAD freezing scheme, VA—Visual Adaptive Prompt, TEXKD—textual fixed distillation, VISKD—visual EMA distillation*

![[assets/figures/papers/paper_list_l776_https_arxiv_org_abs_2605_05027/figures/009_Table_4.jpg]]
*Table 4: Effect of textual distillation strength on AKA-order1. Weak/Strong differ only when TEXKD is enabled; for “No KD” and “VISKD only”, both columns are identical*

![[assets/figures/papers/paper_list_l776_https_arxiv_org_abs_2605_05027/figures/012_Table_S.4.jpg]]
*Table S.4: Effect of visual distillation strength (V1–V5). We report final stage average performance on both seen and unseen domains. Each configuration varies only in the feature- and logitlevel weights*

![[assets/figures/papers/paper_list_l776_https_arxiv_org_abs_2605_05027/figures/015_Table_S.6.jpg]]
*Table S.6: Effect of the number of unfrozen blocks. We report the final-stage seen-domain average, Market1501 performance, and trainable parameters. 4 blocks corresponds to the configuration used in the main paper*

## 方法谱系与知识库定位

### 1. 在终身行人重识别中的定位

PAD属于**免样本回放（exemplar-free）的终身行人重识别**方法。与基于回放的方法（如**LwF**，Li & Hoiem, PAMI 2017）存储原始样本不同，PAD不保留任何历史数据，仅通过知识蒸馏维持旧知识。在此范式内，PAD与三类近期工作形成对比：

- **基于原型的视觉蒸馏方法**：如PAEMA、DKP、DAFC等，通过存储类别中心或分布信息进行视觉侧知识蒸馏。PAD在此基础上的核心突破是将蒸馏从纯视觉模态扩展到**视觉-文本双模态**，利用冻结文本编码器提供跨域稳定的语义锚点。
- **基于提示的终身学习方法**：VA-Prompt的设计灵感源自**DualPrompt**（Wang et al., ECCV 2022），但PAD将其从通用终身分类场景适配到行人重识别，并引入了域自适应扩展与旧提示冻结机制。
- **视觉-语言预训练模型的应用**：PAD以**CLIP-ReID**为基础视觉-语言模型，但将其文本编码器冻结作为全局语义锚点，而非参与训练，这与常规微调策略形成根本差异。

### 2. 方法谱系中的关键创新点

PAD的独特性体现在以下设计决策的耦合：

| 设计维度 | 基线方法典型做法 | PAD的做法 |
|---------|----------------|----------|
| 模态利用 | 仅视觉蒸馏 | 视觉+文本双重蒸馏（非对称设计） |
| 文本编码器 | 无或可训练 | 冻结，作为稳定语义坐标系统 |
| 文本侧提示 | 无 | TA-Prompt（可学习，弱蒸馏） |
| 视觉侧提示 | 无或单域提示 | VA-Prompt（域自适应扩展+冻结旧域） |
| 视觉蒸馏策略 | 无或常规蒸馏 | EMA教师+多层次（特征+logit）蒸馏 |
| 骨干微调范围 | 全微调或无微调 | 选择性解冻最后几层Transformer块及分类头 |

这种设计的因果逻辑链为：**冻结文本编码器 → 提供跨域语义锚点 → 通过弱文本蒸馏抑制语义漂移 → 同时通过强EMA视觉蒸馏保持域适应能力 → 选择性解冻骨干平衡可塑性与记忆保持**。

### 3. 适用边界与约束条件

PAD的有效性依赖于以下前提：

1. **预训练视觉-语言模型的可用性**：PAD要求具备在大规模图像-文本数据上预训练的视觉-语言模型（如CLIP），以提供有意义的文本语义锚点。若预训练模型的文本-视觉对齐质量不足，锚点的稳定性将受到削弱。

2. **域序列中的身份非重叠假设**：遵循终身ReID的标准设定，各域的身份类别互不重叠。PAD未处理跨域身份重叠或增量身份扩展的场景。

3. **文本蒸馏强度的手工调节**：弱文本蒸馏（T1–T3配置）优于强文本蒸馏（T4–T5配置），但当前缺乏自适应调节机制，需针对不同域序列手工选择蒸馏强度。

4. **模态限制**：目前仅处理图像模态与文本的对齐，尚未扩展到视频ReID、红外-可见光跨模态ReID或换装ReID场景。

### 4. 已知局限

- **域间性能不均衡**：在AKA-order1上，DukeMTMC（mAP 64.9）和MSMT17（mAP 46.9）的性能明显低于Market-1501（mAP 81.2）和CUHK-SYSU（mAP 92.6），表明PAD对大规模或高难度域的适应仍有提升空间。
- **蒸馏强度缺乏自适应性**：文本蒸馏和视觉蒸馏的强度系数（$\lambda_{\text{text}}$、$\lambda_{\text{feat}}$、$\lambda_{\text{logit}}$）需人工设定，无法根据域间差异自动调整。
- **专家槽位分配需手工预设**：VA-Prompt中的E-Prompt槽位数量需提前指定，缺乏基于域复杂度的自动分配机制。
- **视觉蒸馏的饱和效应**：消融实验显示，过强的视觉蒸馏（V5配置）导致性能饱和甚至下降，表明当前蒸馏策略在强度上限方面存在约束。

### 5. 开放问题

1. **自适应蒸馏强度调节**：能否根据域间分布差异、模型遗忘程度或文本-视觉对齐质量，自动调节$\lambda_{\text{text}}$、$\lambda_{\text{feat}}$、$\lambda_{\text{logit}}$的权重，以优化稳定性-可塑性权衡？

2. **多模态扩展**：PAD的文本锚定机制能否扩展到视频ReID（利用时序文本描述）、红外ReID（利用跨模态语义对齐）或换装ReID（利用服装无关的文本语义）？

3. **VA-Prompt的自动化槽位分配**：能否基于域间相似度（当前已观察到激活相似度与域特征相似度的相关系数$\rho=0.77$）实现专家槽位的动态增长与合并，而非手工预设？

4. **文本锚点的质量依赖性**：当预训练视觉-语言模型的行人语义理解有限时（如对细粒度衣着、姿态属性的区分能力不足），文本锚点的稳定性是否会退化？如何量化并补偿这种退化？

5. **与基于回放方法的混合策略**：在允许少量样本回放的宽松设定下，PAD的非对称蒸馏机制能否与回放策略互补，进一步压缩遗忘？

## 原文 PDF

![[paperPDFs/CVPR_2026/Prompt_Anchored_Vision_Text_Distillation_for_Lifelong_Person_Re_identification.pdf]]
