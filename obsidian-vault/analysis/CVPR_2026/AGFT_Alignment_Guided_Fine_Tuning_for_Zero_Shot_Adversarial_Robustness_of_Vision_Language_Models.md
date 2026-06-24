---
title: "AGFT: Alignment-Guided Fine-Tuning for Zero-Shot Adversarial Robustness of Vision-Language Models"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/AGFT_Alignment_Guided_Fine_Tuning_for_Zero_Shot_Adversarial_Robustness_of_Vision_Language_Models.pdf
project_link: null
code_link: "https://github.com/YuboCui/AGFT"
aliases:
- AGFTA
- AGFT
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/representation_self_supervised_transfer
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 以预训练CLIP模型自身的概率预测（软对齐分布）作为监督信号进行文本引导对抗训练，并引入温度缩放分布一致性校准，使鲁棒模型在学习对抗不变性的同时保持原始图文语义对应关系。
primary_logic: 文本引导的对抗训练与分布一致性校准相结合，能够在提升零样本对抗鲁棒性的同时最大限度地保留预训练视觉-文本语义结构，从而在多个零样本基准上同时取得更高的鲁棒和清洁准确率。
claims:
- 在15个零样本数据集上，AGFT平均鲁棒准确率达到46.57%，比最强基线GLADIATOR（43.46%）高出3.1个百分点，同时平均清洁准确率61.35%也优于所有基线。
- 在更强的白盒攻击（C&W和AutoAttack）以及不同扰动预算下，AGFT均一致优于已有方法，展现出更好的攻击泛化性。
- 消融实验表明，温度缩放参数γ能够平衡鲁棒性与准确性，且分布一致性校准显著提升了对抗样本上的Top-5预测重叠率（IoU）。
- AGFT在ViT-B/16和RN50×4等不同架构上均取得最优鲁棒性，证明方法具有良好的架构通用性。
---

# AGFT: Alignment-Guided Fine-Tuning for Zero-Shot Adversarial Robustness of Vision-Language Models

> [!tip] 核心洞察
> 文本引导的对抗训练与分布一致性校准相结合，能够在提升零样本对抗鲁棒性的同时最大限度地保留预训练视觉-文本语义结构，从而在多个零样本基准上同时取得更高的鲁棒和清洁准确率。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于对齐引导微调的视觉语言模型零样本对抗鲁棒性 |
| 英文题名 | AGFT: Alignment-Guided Fine-Tuning for Zero-Shot Adversarial Robustness of Vision-Language Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.29410) · [Code](https://github.com/YuboCui/AGFT) |
| Topic | #topic/vision_multimodal_applications #topic/representation_self_supervised_transfer #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Alignment-Guided Fine-Tuning (AGFT) |
| Dataset | 15个零样本数据集（平均）, 15个零样本数据集（平均），ε=1/255 |

> [!tip] 效果简介
> - 15个零样本数据集（平均） 上，Robust Accuracy (PGD-20, ε=1/255) 46.57 vs 43.46 (GLADIATOR) (+3.11%)；Clean Accuracy 61.35 vs 60.34 (GLADIATOR) (+1.01%)。
> - 15个零样本数据集（平均），ε=1/255 上，Robust Accuracy (AutoAttack) 42.81 vs 41.91 (GLADIATOR) (+0.90%)。
> - 15个零样本数据集（平均），不同推理ε 上，Average Robust Accuracy 25.46 vs 23.47 (TGA-ZSR) (+1.99%)。

## 概述

**核心问题**：现有的视觉-语言模型（VLM）零样本对抗鲁棒性微调方法普遍采用分类引导范式，即使用硬标签（独热向量）作为监督信号。这种策略强制图像特征向单一文本原型靠拢，破坏了预训练阶段建立的跨模态相对相似性结构，导致零样本泛化能力显著下降——鲁棒性与清洁准确率之间存在难以调和的冲突。

**核心思路**：本文提出**对齐引导微调（Alignment-Guided Fine-Tuning, AGFT）**，其关键洞察在于：以预训练CLIP模型自身的概率预测（软对齐分布）替代硬标签作为监督信号，并引入温度缩放的分布一致性校准机制。这一设计使模型在学习对抗不变性的同时，保持原始图文语义对应关系，从而在提升鲁棒性的同时最大限度地保留零样本泛化能力。

**方法定位**：AGFT属于文本引导对抗训练范式的改进，与现有方法的关键差异体现在两个可替换模块上：(1) 监督信号从硬标签切换为预训练模型的软对齐分布；(2) 引入温度缩放校准（温度比 $\gamma$），对目标分布进行一致性调整。该方法在TeCoA、PMG-AFT（Wang et al., CVPR 2024）、TGA-ZSR（Yu et al., NeurIPS 2024）和GLADIATOR等基线工作的基础上，重新定义了对抗微调的目标分布构造方式。

**主要结果**：在15个零样本数据集上，AGFT平均鲁棒准确率达到46.57%，比最强基线GLADIATOR（43.46%）高出3.1个百分点，同时平均清洁准确率61.35%也优于所有对比方法。在更强的白盒攻击（C&W、AutoAttack）及不同扰动预算下，AGFT均一致优于已有方法。消融实验证实，温度缩放参数 $\gamma=0.4$ 时取得最佳鲁棒-清洁平衡，分布一致性校准使对抗样本上的Top-5预测重叠率从47.32%提升至56.12%，验证了其保持语义结构的能力。该方法在ViT-B/16和RN50×4等不同架构上均取得最优鲁棒性，展现了良好的架构通用性。

**局限性**：当前评估仅限于 $\ell_\infty$ 范数约束下的对抗样本，尚未验证在 $\ell_2$ 扰动、文本级别攻击或联合图文攻击下的有效性；实验主要在CLIP系列模型上完成，未扩展到BLIP、SigLIP等其他跨模态架构；目前仅针对零样本图像分类任务，尚未在视觉问答、图像描述等更复杂的多模态下游任务中验证迁移效果。

## 背景与动机

### 零样本对抗鲁棒性的核心矛盾

视觉-语言模型（VLMs）如CLIP通过大规模图文对比预训练，在零样本图像分类任务上展现了强大的泛化能力。然而，这些模型对对抗扰动极为脆弱——微小的、人眼不可察觉的像素扰动即可导致模型做出完全错误的预测。为提升鲁棒性，对抗训练（adversarial training）被广泛采用，其标准形式为最小-最大鞍点优化：

$$\min_{\theta} \mathbb{E}_{(x,y) \sim \mathcal{D}} \left[ \max_{x+\delta \in B(x,\epsilon)} L(f(x+\delta, \theta), y) \right]$$

在传统监督学习场景中，该范式以硬标签 $y$（独热向量）作为监督信号，通过在多步PGD攻击生成的对抗样本上最小化分类损失来学习对抗不变性。

然而，当这一范式被直接迁移到VLMs的零样本对抗微调时，一个根本性的矛盾浮现：**硬标签监督强制图像特征向单一文本原型靠拢，破坏了预训练模型精心构建的跨模态相对相似性结构**。该结构是零样本泛化的基石——模型并非简单地判断图像属于哪个类别，而是通过计算图像与所有候选文本描述的余弦相似度分布来进行推理。当对抗训练以独热标签强行拉近对抗图像特征与正确类文本特征、同时推远与其他类文本特征的距离时，预训练的图文语义对应关系被扭曲，导致零样本迁移能力显著下降。

### 现有方法的局限

近期工作尝试将对抗训练适配到VLMs的零样本场景。**TeCoA**率先提出文本引导的对比对抗训练，以文本嵌入替代硬标签作为监督锚点。在此基础上，**PMG-AFT**（Wang et al., CVPR 2024）引入预训练模型辅助监督以缓解过拟合；**TGA-ZSR**（Yu et al., NeurIPS 2024）通过注意力优化与约束增强文本引导的鲁棒性；**GLADIATOR**则通过最大化特征有效秩与注入特征噪声来增强鲁棒性。

尽管这些方法在零样本对抗鲁棒性上取得了进展，但它们共享一个深层缺陷：**监督信号本质上仍是“分类引导”的**——无论是硬标签还是文本嵌入，都试图将对抗图像特征驱动到某个单一的“正确”目标上。这种点对点的对齐方式忽略了预训练模型输出的**分布性信息**：原始CLIP模型对每张图像给出的并非一个确定的类别判断，而是一个跨越所有类别的概率分布，该分布编码了丰富的类间语义关系（例如“豹”与“猫”的相似度高于“豹”与“汽车”）。分类引导的对抗微调恰恰丢弃了这一关键信息，导致鲁棒性与零样本泛化能力之间的严重权衡。

### 本文动机

基于上述分析，本文提出一个核心洞察：**零样本对抗微调应以预训练模型自身的概率预测（软对齐分布）作为监督信号，而非外部注入的硬标签或单一文本锚点**。这一思路将对抗训练的目标从“分类正确”转变为“对齐保持”——使鲁棒模型在对抗样本上的预测分布与原始预训练模型的预测分布保持一致。由此，模型在学习对抗不变性的同时，能够最大限度地保留预训练的视觉-文本语义结构，从而在提升鲁棒性的同时维持零样本泛化能力。

然而，直接使用原始预训练分布作为目标面临一个技术挑战：预训练模型的输出分布可能过于“尖锐”（高置信度），导致对抗训练过程中的梯度信号不足或过拟合。为此，本文进一步引入**分布一致性校准**机制，通过对预训练分布的logits进行温度缩放，生成一个适度平滑的目标分布，在语义结构保持与训练有效性之间取得平衡。

基于上述动机，本文提出**AGFT（Alignment-Guided Fine-Tuning）**——一种以对齐引导为核心范式的零样本对抗微调方法，其整体流程如图2所示：首先获取预训练模型的概率预测作为软对齐分布，经温度缩放校准后作为对抗训练的目标分布，最终在对抗样本上最小化与该分布的交叉熵损失。

## 核心创新

### 问题瓶颈：硬标签监督破坏跨模态语义结构

现有面向视觉语言模型（VLM）零样本对抗鲁棒性的方法——包括 **TeCoA**、**PMG-AFT**（Wang et al., CVPR 2024）、**TGA-ZSR**（Yu et al., NeurIPS 2024）和 **GLADIATOR**——均采用**分类引导对抗微调**范式：以独热编码（hard label）作为监督信号，强制对抗图像特征向单一文本原型靠拢。这一策略的根本缺陷在于，它破坏了预训练阶段建立的**图文跨模态相对相似性结构**——即图像与所有候选文本之间的软对齐分布。当模型被迫将扰动图像映射到唯一正确的文本嵌入时，其在开放词汇场景下的零样本泛化能力显著下降，表现为清洁准确率与鲁棒准确率之间的严重失衡。

### 核心创新机制：从硬标签到软对齐分布

**AGFT（Alignment-Guided Fine-Tuning）** 将监督信号从硬标签替换为**预训练CLIP模型自身的概率预测**（即软对齐分布 $p_{orig}$），实现从“分类引导”到“对齐引导”的范式转换。具体而言，AGFT包含两个紧密耦合的创新模块：

**1. 文本引导对抗训练（Text-Guided Adversarial Training）**

传统方法以类别标签 $y$ 为目标，优化 $\min_{\theta} \mathbb{E}_{(x,y)}[\max_{x_{adv}} L(f(x_{adv}), y)]$。AGFT则使用冻结的原始CLIP图像编码器 $f_{\theta_{orig}}$ 计算图像与所有文本提示的余弦相似度，经温度参数 $\tau$ 缩放后得到软对齐分布：

$$p_{orig}^{i,j} = \frac{ \exp\left( \cos\left( f_{\theta_{orig}}(x^i), f_{\phi}(t^j) \right) / \tau \right) }{ \sum_{k} \exp\left( \cos\left( f_{\theta_{orig}}(x^i), f_{\phi}(t^k) \right) / \tau \right) }$$

该分布保留了预训练模型对图像-文本语义关系的完整建模，而非将其压缩为单一标签。对抗训练的目标随之变为：在对抗样本上最小化模型输出分布与 $p_{rob}$（校准后的目标分布）之间的交叉熵损失。

**2. 分布一致性校准（Distribution Consistency Calibration）**

直接使用 $p_{orig}$ 作为目标分布存在一个问题：预训练模型的预测置信度与鲁棒模型在对抗样本上的特征分布之间存在偏差。AGFT引入**温度缩放校准机制**，通过温度缩放比 $\gamma \in (0, 1]$ 调整原始logits的锐度，生成校准后的目标分布：

$$p_{rob}^{i,j} = \frac{ \exp\left( \cos\left( f_{\theta_{orig}}(x^i), f_{\phi}(t^j) \right) / (\tau/\gamma) \right) }{ \sum_{k} \exp\left( \cos\left( f_{\theta_{orig}}(x^i), f_{\phi}(t^k) \right) / (\tau/\gamma) \right) }$$

校准后的温度 $\tau/\gamma$ 大于原始温度 $\tau$，使得目标分布更加平滑，为对抗训练提供更柔和的监督信号。最终的AGFT优化目标为：

$$\min \mathbb{E}_{\pmb{x} \in \mathcal{D}} \left[ \max_{{\pmb x}_{adv} \in B({\pmb x},\epsilon)} L({\pmb x}_{adv}, {\pmb t}, {\pmb p}_{rob}, \tau) \right]$$

其中损失函数 $L$ 以 $p_{rob}$ 为目标分布计算交叉熵：

$$L(\boldsymbol{x}_{adv}, t, \boldsymbol{p}_{rob}, \tau) = -\mathbb{E}_{i,j} \left[ p_{rob}^{i,j} \log \frac{ \exp( \cos( f_{\theta}(x_{adv}^i), f_{\phi}(t^j) ) / \tau ) }{ \sum_{k} \exp( \cos( f_{\theta}(x_{adv}^i), f_{\phi}(t^k) ) / \tau ) } \right]$$

### 创新效果：鲁棒性与清洁度同步提升

这一范式转换带来了可量化的性能增益。在15个零样本数据集的平均评测中，AGFT的鲁棒准确率达到 **46.57%**，比最强基线GLADIATOR（43.46%）高出 **+3.11个百分点**；同时，清洁准确率 **61.35%** 也优于所有对比方法（Table 1, Table 2）。这验证了核心假设：**保持预训练语义结构是实现零样本对抗鲁棒性的关键**，而非单纯追求对抗不变性。

消融实验进一步揭示了两个模块的协同作用。温度缩放比 $\gamma=0.4$ 时取得鲁棒性与清洁度的最佳平衡（Table 8）；分布一致性校准使对抗样本上的Top-5预测重叠率（IoU）从47.32%提升至56.12%，直接证明了其保持语义结构的能力（Table 9）。此外，AGFT在ViT-B/16和RN50×4等不同架构上均取得最优鲁棒性（Table 5, Table 14, Table 15），表明该方法具有良好的架构通用性。

## 整体框架

AGFT的整体框架围绕一个核心矛盾展开：如何在对抗微调中提升鲁棒性的同时，避免破坏预训练CLIP模型已建立的跨模态语义对齐。为此，AGFT设计了一条“对齐引导”的对抗训练流水线，由四个关键模块串联构成。

### 流水线总览

如Figure 2所示，AGFT的流水线包含以下步骤：

1. **预训练概率分布获取**：对于每张干净图像，使用冻结的原始CLIP图像编码器 $f_{\theta_{orig}}$ 和文本编码器 $f_{\phi}$ 计算图像与所有候选文本提示之间的余弦相似度，经softmax归一化后得到软对齐分布 $\boldsymbol{p}_{orig}$（见公式(6)）。该分布编码了预训练模型对“该图像与各文本类别匹配程度”的完整认知，而非仅保留最高概率的单一类别标签。

2. **温度缩放校准**：对 $\boldsymbol{p}_{orig}$ 的logits施加温度调整，将原始温度 $\tau$ 替换为校准温度 $\tau/\gamma$（其中 $\gamma \in (0,1]$ 为温度缩放比），生成校准后的目标分布 $\boldsymbol{p}_{rob}$（见公式(8)）。这一步是AGFT区别于已有方法的关键创新——通过降低温度（即增大logits的尺度），使目标分布的峰值更尖锐，从而在训练中强化对正确类别的引导信号，同时保留类别间的相对相似性结构。

3. **对抗样本生成**：以校准分布 $\boldsymbol{p}_{rob}$ 为监督信号，通过PGD攻击在干净图像上生成扰动样本（见公式(2)）。与传统的硬标签监督攻击不同，这里的攻击梯度来自于与软分布对齐的损失，使得生成的对抗样本更贴近预训练模型的语义边界。

4. **文本引导对抗微调**：在对抗样本上最小化模型输出分布与 $\boldsymbol{p}_{rob}$ 之间的交叉熵损失（见公式(9)），更新图像编码器参数。最终的优化目标是一个最小-最大鞍点问题（见公式(10)）：内层最大化对抗样本上的损失，外层最小化期望损失。

### 模块间的因果关联

上述四个模块构成了一个闭环的因果链条：

- **瓶颈定位**：已有分类引导对抗微调方法（如TeCoA、PMG-AFT、TGA-ZSR）使用独热硬标签作为监督信号，强制对抗图像特征向单一文本原型靠拢。这虽然能提升鲁棒性，但破坏了预训练模型在图像-文本空间中建立的相对相似性结构，导致零样本泛化能力显著下降。

- **因果调节变量**：AGFT将监督信号从硬标签替换为预训练模型自身的概率预测（软对齐分布），使模型在学习对抗不变性的同时，保持原始图文语义对应关系。温度缩放校准进一步调节了这一信号的“软硬程度”——$\gamma$ 越小，目标分布越接近硬标签；$\gamma$ 越大，越接近原始软分布。

- **机制解释**：分布一致性校准通过温度调整，在“保持语义结构”和“强化对抗鲁棒性”之间建立了可控的权衡。消融实验（Table 8）表明，$\gamma=0.4$ 时取得最佳平衡；而增大分布温度（即增大 $1/\tau$）可进一步提升鲁棒准确率，但可能牺牲部分清洁准确率。实证分析（Table 9）进一步验证了校准的有效性：对抗样本上的Top-5预测重叠率（IoU）从47.32%提升至56.12%，说明校准后的目标分布确实更好地保留了预训练的语义结构。

### 输入输出规范

- **输入**：干净图像 $\boldsymbol{x}$、对应文本提示集合 $\boldsymbol{t}$、预训练CLIP模型参数（图像编码器 $f_{\theta_{orig}}$ 和文本编码器 $f_{\phi}$ 冻结）。
- **输出**：微调后的图像编码器 $f_{\theta}$，在对抗样本上具有鲁棒性的同时，保持与文本编码器的语义对齐。
- **推理阶段**：仅使用微调后的图像编码器与冻结的文本编码器进行零样本分类，无需额外的校准步骤。

### 补充图表

![[assets/figures/papers/paper_list_l2760_https_arxiv_org_abs_2603_29410/figures/002_Figure_2.jpg]]
*Figure 2: The overall pipeline of AGFT. First, we obtain the probabilistic predictions of the pre-trained model and use the resulting distribution as the target for adversarial fine-tuning to encourage adversarial visual features to align with textual embeddings. To mitigate the discrepancies in visual–textual semantic structure, we calibrate the pre-trained output distribution through temperature adjustment, while maintaining the cross-modal similarity structure across images and textual descriptions*

## 核心模块与公式推导

AGFT 的核心由两个紧密耦合的模块构成：**文本引导对抗训练**与**分布一致性校准**。前者将监督信号从硬标签替换为预训练模型的概率预测，后者通过温度缩放修正该分布与鲁棒模型之间的语义偏差，二者共同保证对抗不变性学习过程中跨模态对齐结构不被破坏。

### 文本引导对抗训练

传统分类引导的对抗微调以独热向量 $y$ 为监督，强制对抗图像特征向单一文本原型靠拢。AGFT 改用冻结的原始 CLIP 图像编码器 $f_{\theta_{orig}}$ 计算图像与所有类别文本提示的相似度，得到软对齐分布 $p_{orig}$：

$$p_{orig}^{i,j} = \frac{ \exp\left( \cos\left( f_{\theta_{orig}}(x^i), f_{\phi}(t^j) \right) / \tau \right) }{ \sum_{k} \exp\left( \cos\left( f_{\theta_{orig}}(x^i), f_{\phi}(t^k) \right) / \tau \right) } \tag{6}$$

其中 $f_{\phi}(t^j)$ 为第 $j$ 个类别的文本嵌入，$\tau$ 为原始 CLIP 的温度参数。该分布编码了预训练模型对图像-文本相对相似性的完整认知，而非仅保留最高概率的单一类别。

### 分布一致性校准

直接以 $p_{orig}$ 作为目标分布会导致鲁棒模型在对抗样本上过度锐化预测，破坏语义结构。AGFT 引入温度缩放比 $\gamma \in (0,1]$，将原始 logits 除以 $\tau/\gamma$ 后重新归一化，得到校准目标分布 $p_{rob}$：

$$p_{rob}^{i,j} = \frac{ \exp\left( \cos\left( f_{\theta_{orig}}(x^i), f_{\phi}(t^j) \right) / (\tau/\gamma) \right) }{ \sum_{k} \exp\left( \cos\left( f_{\theta_{orig}}(x^i), f_{\phi}(t^k) \right) / (\tau/\gamma) \right) } \tag{8}$$

$\gamma$ 控制校准强度：$\gamma=1$ 时退化为原始分布；$\gamma<1$ 时温度升高，分布更平滑，为鲁棒模型提供更宽容的对齐目标。消融实验表明 $\gamma=0.4$ 时鲁棒性与清洁准确率达到最佳平衡（Table 8）。

### 对抗训练损失与最终优化目标

以 $p_{rob}$ 为监督，AGFT 在对抗样本上最小化交叉熵损失：

$$L(\boldsymbol{x}_{adv}, t, \boldsymbol{p}_{rob}, \tau) = -\mathbb{E}_{i,j} \left[ p_{rob}^{i,j} \log \frac{ \exp( \cos( f_{\theta}(x_{adv}^i), f_{\phi}(t^j) ) / \tau ) }{ \sum_{k} \exp( \cos( f_{\theta}(x_{adv}^i), f_{\phi}(t^k) ) / \tau ) } \right] \tag{9}$$

对抗样本 $x_{adv}$ 由 PGD 攻击生成，其更新规则为：

$$x_{s+1} = x_s + \alpha \cdot \mathrm{sign}(\nabla_{x_s} L(x_s, t)), \quad x_{s+1} = \Pi_{B(x,\epsilon)}(x_{s+1}) \tag{2}$$

最终形成对齐引导的 min-max 优化问题：

$$\min \mathbb{E}_{\pmb{x} \in \mathcal{D}} \left[ \max_{{\pmb x}_{adv} \in B({\pmb x},\epsilon)} L({\pmb x}_{adv}, {\pmb t}, {\pmb p}_{rob}, \tau) \right] \tag{10}$$

该框架的核心机制在于：内层最大化生成对抗扰动，外层最小化使鲁棒图像特征与校准后的文本分布对齐，从而在提升对抗鲁棒性的同时保留预训练的跨模态语义结构。分布一致性校准的实证效果由 Table 9 验证——引入校准后对抗样本上的 Top-5 预测重叠率（IoU）从 47.32% 提升至 56.12%，证明语义保持能力显著增强。

## 实验与分析

### 核心性能对比

AGFT 在 15 个零样本数据集上进行了全面评估。Table 1 报告了 PGD-20 攻击（ε=1/255）下的零样本鲁棒准确率，Table 2 报告了清洁准确率。AGFT 的平均鲁棒准确率达到 **46.57%**，比最强基线 GLADIATOR（43.46%）高出 **3.11 个百分点**；平均清洁准确率为 **61.35%**，同样优于所有对比方法，比 GLADIATOR 高出 1.01 个百分点。这一结果验证了核心洞察：文本引导的对抗训练与分布一致性校准相结合，能够在提升零样本对抗鲁棒性的同时最大限度地保留预训练视觉-文本语义结构。

![[assets/figures/papers/paper_list_l2760_https_arxiv_org_abs_2603_29410/figures/003_Table_1.jpg]]
*Table 1: Zero-shot robust accuracy (%). Adversarial examples are generated by PGD-20 attack with the perturbation budget*

![[assets/figures/papers/paper_list_l2760_https_arxiv_org_abs_2603_29410/figures/004_Table_2.jpg]]
*Table 2: Zero-shot clean accuracy (%). Clean images from 15 datasets are evaluated on adversarially fine-tuned CLIP models*

从单数据集表现看，AGFT 在 15 个数据集中的 12 个上取得了最优鲁棒准确率，在 8 个数据集上取得了最优清洁准确率。值得注意的是，分类引导方法 TeCoA 虽然在某些数据集上鲁棒性尚可，但其平均清洁准确率仅为 56.93%，比 AGFT 低 4.42 个百分点，揭示了硬标签监督对零样本泛化能力的破坏性影响。

### 不同攻击场景下的鲁棒性

**扰动预算泛化性**：Table 3 展示了推理阶段使用不同扰动预算（ε=1/255, 2/255, 4/255）时的平均鲁棒准确率。AGFT 在所有预算下均保持最优，平均鲁棒准确率 **25.46%**，比第二名 TGA-ZSR（23.47%）高出 1.99 个百分点。这表明软对齐监督使模型学习到的对抗不变性具有更好的跨强度泛化能力。

**强攻击下的表现**：Table 4 评估了 PGD、C&W 和 AutoAttack 三种强攻击下的性能。在标准设置（ε=1/255）下，AGFT 在 AutoAttack 攻击下的鲁棒准确率为 **42.81%**，比 GLADIATOR（41.91%）高 0.90 个百分点。Table 12 和 Table 13 的逐数据集结果显示，AGFT 在 C&W 和 AutoAttack 下对大多数数据集均保持优势，证明其对抗鲁棒性并非针对特定攻击的过拟合。

**未见攻击的迁移性**：Table 6 测试了多种未见过的非目标攻击和目标攻击（包括随机目标 ATT_T 和最不可能目标 ATT_TL）。AGFT 在所有攻击类型下均优于基线，尤其在目标攻击场景下优势更为明显，说明软对齐监督保留了更丰富的类别间语义关系，使得模型在面对蓄意误导时更难以被欺骗。

### 架构通用性

Table 5 报告了 ViT-B/32、ViT-B/16 和 RN50×4 三种 CLIP 架构上的平均性能。AGFT 在所有架构上均取得最优鲁棒准确率，在 ViT-B/16 上达到 **49.52%**（Table 14），在 RN50×4 上达到 **44.36%**（Table 15），分别比第二名高出 2.3 和 1.5 个百分点。这证明 AGFT 不依赖于特定视觉编码器的归纳偏置，具有良好的架构通用性。

![[assets/figures/papers/paper_list_l2760_https_arxiv_org_abs_2603_29410/figures/005_Table_5.jpg]]
*Table 5: Average performance (%) of different CLIP architectures with the perturbation budget*

### 分布外泛化

Table 7 评估了在 ImageNet 变体（ImageNet-A, ImageNet-R, ImageNet-Sketch, ImageNet-V2）上的分布外性能。AGFT 在鲁棒准确率上全面领先，在 ImageNet-A 上达到 **29.18%**，比 GLADIATOR 高 3.57 个百分点。同时清洁准确率也保持竞争力，表明温度缩放校准有效防止了模型在对抗训练中对源分布的结构性遗忘。

![[assets/figures/papers/paper_list_l2760_https_arxiv_org_abs_2603_29410/figures/010_Table_7.jpg]]
*Table 7: Out-of-distribution performance on ImageNet variants under PGD-20 attack with perturbation budget*

### 消融实验

**温度缩放参数 γ**：Table 8 展示了 γ 和温度倒数 1/τ 的消融结果。预训练 CLIP 的原始设置对应 (γ=1.0, 1/τ=100)。实验发现 **γ=0.4** 时取得鲁棒性与清洁度的最佳平衡——此时校准温度 τ/γ 增大，使目标分布更加平滑，为对抗训练提供了更宽容的监督信号。进一步减小 γ 会过度平滑分布，导致鲁棒准确率下降；增大 γ 则趋近于原始硬分布，清洁度提升但鲁棒性降低。

**分布一致性校准的有效性**：Table 9 从多个维度验证了校准机制的作用。引入校准后，对抗样本上的 **Top-5 预测重叠率（IoU）从 47.32% 提升至 56.12%**，表明校准有效保持了对抗样本与原始样本在语义空间中的相对关系。同时，预测置信度和最大/平均余弦相似度的变化也证实校准缓解了对抗扰动导致的特征偏移。

### Pareto 前沿分析

Figure 3 展示了不同方法在鲁棒性与清洁准确率之间的权衡。AGFT 的 Pareto 前沿明显优于其他方法——在相同清洁准确率下，AGFT 可提供更高的鲁棒性；在相同鲁棒准确率下，AGFT 的清洁度损失更小。这说明对齐引导范式从根本上改变了鲁棒性与泛化性之间的折中关系，而非简单的超参数调优所能达到的。

![[assets/figures/papers/paper_list_l2760_https_arxiv_org_abs_2603_29410/figures/009_Figure_3.jpg]]
*Figure 3: Trade-off between robust and clean accuracy across different methods. Each marker type denotes one method, and each point corresponds to a different trade-off configuration*

### 特征空间可视化

Figure 4 使用 T-SNE 可视化了预训练模型、AGFT 和 TeCoA 在 7 个类别上的特征分布。预训练模型在清洁图像上呈现出清晰的类别聚类结构（Figure 4a）。AGFT 在对抗样本上仍能保持较好的类别分离度（Figure 4b），而 TeCoA 的特征分布则明显更加混乱，类别边界模糊（Figure 4c）。这直观地验证了硬标签监督对跨模态对齐结构的破坏，以及 AGFT 软对齐策略的保护作用。

![[assets/figures/papers/paper_list_l2760_https_arxiv_org_abs_2603_29410/figures/012_Figure_4.jpg]]
*Figure 4: T-SNE visualization of 7 image categories. (a) The original pre-trained CLIP evaluated on clean images. Both (b) AGFT and (c) TeCoA are evaluated on adversarial examples*

### 计算开销

Table 10 比较了各方法的计算开销。AGFT 需要额外的前向传播来获取预训练模型的概率分布，因此每轮训练时间略高于 TeCoA，但仍远低于需要复杂注意力优化的 TGA-ZSR。考虑到显著的性能提升，这一开销是可接受的。

### 失败模式与局限性

1. **扰动类型受限**：当前评估仅限于 ℓ∞ 范数约束下的对抗样本，尚未验证在 ℓ2 扰动、文本级别攻击或联合图文攻击下的有效性。
2. **模型架构局限**：实验主要在 CLIP 系列模型上完成，未扩展到 BLIP、SigLIP 等其他跨模态架构。
3. **任务范围局限**：目前仅针对零样本图像分类任务，尚未在视觉问答、图像描述等更复杂的多模态下游任务中验证 AGFT 的迁移效果。
4. **超参数敏感性**：γ 的最优值可能需要根据具体模型和数据集进行调优，Table 8 显示不同 γ 值对性能有明显影响。

![[assets/figures/papers/paper_list_l2760_https_arxiv_org_abs_2603_29410/figures/011_Table_8.jpg]]
*Table 8: Ablation study of hyperparameters. The original pretrained CLIP setting corresponds to*

### 公平性说明

所有对比方法均采用相同的 CLIP ViT-B/32 骨干，并在 ImageNet 上使用相同的对抗训练配置（PGD-20, ε=1/255, 步长 1/255）。对于 PMG-AFT 和 TGA-ZSR，作者进行了学习率调优以使其适应本任务的设置，具体超参数搜索见 Table 11。GLADIATOR 由于代码未开源，直接引用其原始论文中报告的性能。

### 补充图表

![[assets/figures/papers/paper_list_l2760_https_arxiv_org_abs_2603_29410/figures/013_Table_9.jpg]]
*Table 9: Empirical study of distribution consistency calibration. conf*

![[assets/figures/papers/paper_list_l2760_https_arxiv_org_abs_2603_29410/figures/007_Table_4.jpg]]
*Table 4: Average accuracy (%) under strong attacks with different perturbation budgets used during both fine-tuning and inference*

![[assets/figures/papers/paper_list_l2760_https_arxiv_org_abs_2603_29410/figures/006_Table_3.jpg]]
*Table 3: Average zero-shot robust accuracy (%) under PGD-20 attacks with varying perturbation budgets during inference*

![[assets/figures/papers/paper_list_l2760_https_arxiv_org_abs_2603_29410/figures/008_Table_6.jpg]]
*Table 6: Zero-shot robust accuracy (%) under diverse unseen untargeted and targeted attacks with the perturbation budget*

## 方法谱系与知识库定位

### 与现有基线的关系

AGFT 直接回应了当前视觉语言模型零样本对抗鲁棒性（ZSAR）研究中的核心瓶颈：**分类引导的对抗微调破坏了预训练的跨模态语义对齐结构**。现有方法可沿两条技术路线进行定位。

**文本引导对抗微调路线**：该路线始于 **TeCoA**（文本引导对比对抗训练），首次将对抗训练从硬标签监督迁移到文本嵌入引导，为 VLMs 的零样本对抗鲁棒性奠定了基础。然而 TeCoA 仍依赖独热编码形式的硬标签来构建文本监督信号，本质上未能完全摆脱分类引导范式的约束。**PMG-AFT**（Wang et al., CVPR 2024）在此基础上引入预训练模型辅助监督以缓解过拟合，但其监督信号仍以硬标签为主导。**TGA-ZSR**（Yu et al., NeurIPS 2024）通过注意力优化与约束增强文本引导的鲁棒性，但同样未触及监督信号形式的根本变革。**GLADIATOR** 则另辟蹊径，通过最大化特征有效秩与注入特征噪声来增强鲁棒性，在 15 个零样本数据集上取得了 43.46% 的平均鲁棒准确率，成为 AGFT 之前的最强基线。

AGFT 的关键突破在于将监督信号从**硬标签（独热编码）替换为预训练 CLIP 模型自身的概率预测（软对齐分布）**。这一转变使得对抗微调不再强制图像特征向单一文本原型靠拢，而是保留了原始模型对各个文本提示的相对相似性结构。这构成了方法谱系中的范式跃迁：从“分类引导”到“对齐引导”。

**分布校准路线**：在 AGFT 之前，尚无工作将温度缩放的分布一致性校准引入对抗微调。AGFT 提出的校准模块（温度缩放比 $\gamma \in (0,1]$，校准后温度 $\tau/\gamma$）独立于监督信号类型，可视为对文本引导对抗训练的正交增强。消融实验表明，该模块使对抗样本上的 Top-5 预测重叠率（IoU）从 47.32% 提升至 56.12%，验证了其保持语义结构的能力。

### 适用边界与架构通用性

当前验证的适用边界如下：

- **扰动类型**：仅在 $\ell_\infty$ 范数约束下的对抗样本上进行了系统评估（PGD-20、C&W、AutoAttack），尚未覆盖 $\ell_2$ 扰动或文本级别攻击。
- **模型架构**：实验在 CLIP 的三个变体上完成——ViT-B/32（主实验）、ViT-B/16 和 RN50×4。Table 5 显示 AGFT 在 ViT-B/16 和 RN50×4 上均取得最优鲁棒性，证明方法对 Vision Transformer 和 ResNet 两种异构编码器架构具有良好的通用性。但尚未扩展到其他跨模态架构（如 BLIP-2、SigLIP、LLaVA）或纯 Transformer 模型。
- **任务范围**：目前仅针对零样本图像分类任务。在分布外 ImageNet 变体（Table 7）和多种未见过的迁移攻击（Table 6，包括非目标攻击 ATT 和目标攻击 ATT_T/ATT_TL）上已验证鲁棒性的迁移能力，但尚未在视觉问答、图像描述等生成式多模态任务中验证。

### 已知局限

1. **对抗威胁模型单一**：所有实验均在 $\ell_\infty$ 范数约束下进行（$\epsilon = 1/255$ 为主设置），对 $\ell_2$ 扰动、联合图文攻击或物理世界对抗样本的有效性尚不明确。
2. **架构覆盖有限**：虽然 ViT-B/16 和 RN50×4 的结果显示了架构通用性，但更大规模的模型（如 ViT-L/14）或异构跨模态架构（BLIP-2、LLaVA）上的表现未经验证。
3. **任务泛化未探索**：AGFT 的文本引导监督形式依赖图像-文本匹配的相似度分布，如何适配生成式多模态任务（如零样本 VQA、图像描述）的监督形式仍是开放问题。
4. **计算开销**：Table 10 显示 AGFT 需要额外的预训练模型前向传播来获取 $p_{orig}$，相比 TeCoA 增加了约 15% 的训练时间。在资源受限场景下可能成为瓶颈。

### 开放问题

1. **扰动范数扩展**：AGFT 在 $\ell_2$ 限制下的对抗鲁棒性表现如何？分布一致性校准机制是否同样适用于 $\ell_2$ 攻击生成的对抗样本？
2. **跨模型泛化**：该方法泛化到 BLIP-2、LLaVA 等更复杂的视觉语言模型时的有效性和效率如何？这些模型的预训练对齐空间与 CLIP 存在差异，温度缩放校准的适用性需要重新验证。
3. **生成式任务适配**：AGFT 是否适用于零样本下的视觉问答、图像描述等生成式多模态任务？如何调整文本引导的监督形式——例如，将图像-文本匹配分布替换为图像-答案/描述的条件分布？
4. **对抗攻击的对称性**：当前仅考虑图像侧的对抗扰动。若同时考虑文本提示的对抗扰动（或图文联合攻击），对齐引导范式能否提供比分类引导更强的鲁棒性？这需要重新定义“零样本对抗鲁棒性”的威胁模型。
5. **温度缩放的自动化选择**：当前 $\gamma$ 和 $1/\tau$ 通过网格搜索确定（Table 8，$\gamma=0.4$ 为最优平衡点）。是否存在基于数据特性或模型状态的自动化校准策略，以减少超参数调优成本？

## 原文 PDF

![[paperPDFs/CVPR_2026/AGFT_Alignment_Guided_Fine_Tuning_for_Zero_Shot_Adversarial_Robustness_of_Vision_Language_Models.pdf]]
