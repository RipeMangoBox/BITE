---
title: "TTP: Test-Time Padding for Adversarial Detection and Robust Adaptation on Vision-Language Models"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/TTP_Test_Time_Padding_for_Adversarial_Detection_and_Robust_Adaptation_on_Vision_Language_Models.pdf
project_link: null
code_link: "https://github.com/lizhiwei23/TTP"
aliases:
- TTPT
- TTP
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 图像空间填充操作能够部分恢复因对抗扰动而破坏的注意力模式，进而使原始嵌入与填充后嵌入之间的余弦相似度在干净样本和对抗样本上呈现显著差异，可作为一种通用、跨模型跨数据集的检测信号。
primary_logic: 通过计算填充前后 CLIP 视觉嵌入的余弦相似度漂移，可以高精度区分干净与对抗样本；对检测出的对抗样本采用可训练的单步填充优化和基于相似度的加权集成，能在不牺牲干净准确率的前提下大幅提升对抗鲁棒性。
claims:
- TTP 通过空间填充前后的 CLIP 特征嵌入余弦相似度偏移来识别对抗样本，得到一个跨架构和数据集通用的检测阈值。
- 干净样本在填充后特征变化极小，而对抗样本则产生显著偏移。
- 对于检测到的对抗样本，可训练的测试时填充通过单步熵最小化来优化参数，并结合相似度感知集成策略得到更鲁棒的最终预测。
- 8 fine-grained classification datasets (Caltech101, Pets, Cars, Flower102, Airc... 上 Adversarial Accuracy (PGD, ε=4.0, 100 iters) = 39.7% (ViT-B/32 avg)
---

# TTP: Test-Time Padding for Adversarial Detection and Robust Adaptation on Vision-Language Models

> [!tip] 核心洞察
> 通过计算填充前后 CLIP 视觉嵌入的余弦相似度漂移，可以高精度区分干净与对抗样本；对检测出的对抗样本采用可训练的单步填充优化和基于相似度的加权集成，能在不牺牲干净准确率的前提下大幅提升对抗鲁棒性。

| 字段 | 内容 |
|------|------|
| 中文题名 | 测试时填充：面向视觉-语言模型的对抗检测与鲁棒适配 |
| 英文题名 | TTP: Test-Time Padding for Adversarial Detection and Robust Adaptation on Vision-Language Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.16523) · [Code](https://github.com/lizhiwei23/TTP) |
| Topic | #topic/vision_multimodal_applications #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Test-Time Padding (TTP) |
| Dataset | 8 fine-grained classification datasets, Same 8 datasets, fine-grained datasets under CLIP backbones |

> [!tip] 效果简介
> - 8 fine-grained classification datasets (Caltech101, Pets, Cars, Flower102, Airc... 上，Adversarial Accuracy (PGD, ε=4.0, 100 iters) 39.7% (ViT-B/32 avg) vs 35.3% (R-TPT) (+4.4%)。
> - Same 8 datasets (ViT-B/16) 上，Adversarial Accuracy 42.9% (avg)。
> - Same 8 datasets (ViT-L/14) 上，Adversarial Accuracy 51.6% (avg)。

## 概要

视觉-语言模型（尤其是 CLIP）在测试时极易受到对抗扰动攻击，而现有测试时防御方法普遍缺乏可靠的对抗样本检测机制，只能对所有输入进行统一适配，导致干净准确率与对抗鲁棒性难以兼得。**TTP（Test-Time Padding）** 提出了一种轻量级、无需训练的对抗检测与鲁棒适配框架，其核心发现是：图像空间填充操作能够部分恢复因对抗扰动而破坏的注意力模式，使得原始嵌入与填充后嵌入之间的余弦相似度在干净样本和对抗样本上呈现显著差异——干净样本变化极小，对抗样本则产生大幅度偏移。基于这一因果机制，TTP 构建了一个跨架构、跨数据集通用的检测器，并通过可训练的单步填充优化与相似度感知集成策略，仅对检测出的对抗样本进行针对性适配，从而在不牺牲干净准确率的前提下大幅提升对抗鲁棒性。

在方法定位上，TTP 区别于 **TTC**（Xing et al., CVPR 2025）的噪声扰动检测和 **R-TPT**（Sheng et al., CVPR 2025）、**TAPT**（Wang et al., CVPR 2025）等统一文本提示调优方法，首次将输入空间的填充操作同时用于对抗检测与对抗适配。实验表明，TTP 在 8 个细粒度分类数据集上，以 ViT-B/32 为骨干网络时平均对抗准确率达 39.7%，较 R-TPT 提升 4.4%；在 ViT-L/14 上进一步提升至 51.6%。其检测准确率在所有设置下均显著优于 TTC，接近 100%。



视觉-语言基础模型（以 CLIP 为代表）在零样本分类等任务上展现出强大的泛化能力，但其对对抗扰动的极端脆弱性已成为其安全部署的核心瓶颈。在测试时，微小的、人眼不可察觉的像素扰动即可导致 CLIP 产生完全错误的预测，这严重限制了其在安全敏感场景中的实际应用。

为应对这一挑战，研究者已提出多种测试时防御策略。**TPT** 及其变体通过测试时提示调优（test-time prompt tuning）来适应输入分布，但这类方法对所有输入进行统一适配，缺乏对抗样本检测机制。**TTC**（Xing et al., CVPR 2025）引入了两阶段检测与对抗策略，但其检测准确率在不同数据集和模型架构上波动较大，可靠性不足。**R-TPT**（Sheng et al., CVPR 2025）和 **TAPT**（Wang et al., CVPR 2025）同样采用统一适配范式，在提升对抗鲁棒性的同时不可避免地牺牲了干净样本的准确率。这种“干净-鲁棒”的折中困境源于一个根本性的缺陷：现有方法无法精确区分干净样本与对抗样本，因而无法对二者实施差异化处理。

本文的核心动机正是打破这一困境。其关键洞察在于：**图像空间填充操作能够部分恢复因对抗扰动而破坏的注意力模式**，进而使原始嵌入与填充后嵌入之间的余弦相似度在干净样本和对抗样本上呈现显著差异——干净样本的填充前后特征变化极小，而对抗样本则产生大幅偏移。这一现象为构建通用、可靠的对抗检测信号提供了可能，也为后续的差异化鲁棒适配奠定了基础。



## 核心方法与创新机理

### 从统一适配到检测驱动的差异化防御

现有测试时防御方法（如 **R-TPT**（Sheng et al., CVPR 2025）、**TAPT**（Wang et al., CVPR 2025））对所有输入样本执行统一适配，缺乏区分干净样本与对抗样本的检测机制。这种“一刀切”策略存在根本性矛盾：适配操作虽然能提升对抗鲁棒性，却往往以牺牲干净样本的分类准确率为代价。**TTC**（Xing et al., CVPR 2025）虽然引入了对抗检测，但其基于小噪声扰动下特征嵌入 L2 距离的检测方案可靠性不足，检测准确率在不同架构和数据集上波动较大（见 Figure 2）。

TTP 的核心创新在于将**检测**与**适配**解耦为两个独立且协同的阶段，形成“先检测、后适配”的差异化防御范式。这一设计的关键瓶颈突破在于：干净样本无需任何适配即可直接预测，从而完整保留其原始准确率；仅对检测出的对抗样本触发适配流程，实现鲁棒性的定向提升。

### 三个关键机制槽位的重新设计

TTP 相对于 baseline 的核心改进体现在三个紧密耦合的机制槽位上：

**1. 对抗检测机制：从 L2 距离到填充诱导的余弦相似度漂移**

Baseline 方法 TTC 通过在输入上叠加小噪声，计算扰动前后特征嵌入的 L2 距离作为检测信号。TTP 提出了一种全新的检测范式——利用空间填充操作诱导的特征漂移进行检测。具体而言，对输入图像施加固定填充后，干净样本的 CLIP 视觉嵌入变化极小，而对抗样本则因对抗扰动破坏的注意力模式被填充操作部分恢复，导致填充前后嵌入产生显著的余弦相似度偏移。这一现象构成了一个跨架构、跨数据集通用的检测信号，仅需一个统一阈值 $\tau = 0.8$ 即可实现高精度二分类（检测准确率接近 100%，见 Figure 2 和 Table 4）。

**2. 对抗适配方法：从统一文本提示调优到实例级可训练填充**

R-TPT 和 TAPT 等 baseline 方法通过调整文本提示（prompt tuning）来提升鲁棒性，这是一种在文本空间操作的统一适配策略。TTP 则将适配操作完全转移到**输入空间**，提出了**可训练的测试时填充**（trainable test-time padding）。该方法仅对检测为对抗的样本生效：首先生成多个增强视图，然后通过最小化高置信度视图的预测熵，对填充参数执行**单步梯度更新**。这一设计使得适配过程具有实例特异性——每个对抗样本获得定制化的填充参数，从而更精准地恢复被对抗扰动破坏的注意力模式（见 Figure 1 中 trainable padding 对注意力图的精细化修正效果）。

**3. 集成策略：从简单平均到相似度感知加权**

传统的数据增强集成方法（如 Ensemble baseline）对所有增强视图的预测进行简单平均，忽略了不同视图在恢复对抗样本语义信息方面的质量差异。TTP 提出了**相似度感知集成**（similarity-aware ensemble），利用增强视图与对抗样本在填充前后嵌入的余弦相似度差异来量化每个视图的可靠性。具体地，对于增强视图 $x_i$，计算其填充嵌入与对抗样本填充嵌入的相似度 $\alpha_i$，以及其填充嵌入与对抗样本原始嵌入的相似度 $\beta_i$，以差值 $s_i = \alpha_i - \beta_i$ 作为该视图的质量评分，再通过 softmax 归一化得到自适应权重 $w_i$。这一机制有效抑制了低质量增强视图的噪声贡献，放大了高质量视图在最终预测中的影响。

### 创新点的因果关联

上述三个槽位并非孤立设计，而是形成了因果闭环：**填充诱导的相似度漂移**同时支撑了检测（区分干净与对抗）和集成（评估增强视图质量）两个模块；**可训练填充**仅在检测模块判定为对抗样本时激活，避免了干净样本上的无效计算；**相似度感知集成**则进一步放大了可训练填充的恢复效果。三者协同使得 TTP 在 8 个细粒度分类数据集上，以 ViT-B/32 为骨干网络时，达到 39.7% 的平均对抗准确率，相较 R-TPT 提升 4.4 个百分点，同时完整保持了干净样本的分类准确率（见 Table 1）。



TTP 的整体 pipeline 遵循“检测—适配—集成”的三阶段范式，所有操作均在测试时完成，无需修改预训练的 CLIP 模型参数。其核心设计动机源于一个关键观察：空间填充操作能够部分恢复因对抗扰动而破坏的注意力模式，使得干净样本与对抗样本在填充前后的特征嵌入余弦相似度上呈现显著差异——干净样本填充后特征变化极小，而对抗样本则产生明显偏移。基于这一因果机制，TTP 将对抗防御拆解为三个松耦合模块，按条件执行，从而在保持干净样本零精度损失的前提下，大幅提升对抗鲁棒性。

### Pipeline 总览

给定一个测试样本 $x$，TTP 首先将其送入对抗检测模块。该模块对 $x$ 施加固定的空间填充操作，分别提取原始嵌入 $z = F(x)$ 与填充后嵌入 $z^{\mathrm{pad}} = F(P^{\mathrm{fix}}(x))$，计算二者的余弦相似度 $s = \frac{z \cdot z^{\mathrm{pad}}}{\|z\| \|z^{\mathrm{pad}}\|}$，并与一个通用阈值 $\tau = 0.8$ 进行比较。若 $s \geq \tau$，则判定为干净样本，直接使用原始 CLIP 零样本分类器输出预测，无需任何适配。若 $s < \tau$，则判定为对抗样本，触发后续的可训练填充适配模块和相似度感知集成模块。

### 可训练填充适配模块

对于被检测为对抗的样本，TTP 生成多个增强视图 $\{x_i\}$，并对每个视图施加参数化的可训练填充 $P_\theta$。适配目标是通过最小化高置信度视图的预测熵来单步更新填充参数 $\theta$：

$$\mathcal{L}_{\mathrm{ent}} = \frac{1}{|B|} \sum_{i \in B} H_i^{\mathrm{pad}}, \quad \theta \gets \theta - \eta \nabla_\theta \mathcal{L}_{\mathrm{ent}}$$

其中 $B$ 为低熵（高置信度）视图的子集。这一单步熵最小化策略引导填充参数恢复被对抗扰动破坏的注意力模式，使模型重新聚焦于正确的判别区域。

### 相似度感知集成模块

为抑制增强过程中引入的噪声，TTP 不采用简单平均，而是设计了一种相似度感知的自适应加权机制。对于每个增强视图 $x_i$，计算其填充嵌入与对抗样本填充嵌入的余弦相似度 $\alpha_i = \cos(z_i^{\mathrm{pad}}, z_{\mathrm{adv}}^{\mathrm{pad}})$，以及其填充嵌入与对抗样本原始嵌入的余弦相似度 $\beta_i = \cos(z_i^{\mathrm{pad}}, z_{\mathrm{adv}})$。视图得分定义为二者之差 $s_i = \alpha_i - \beta_i$，经 softmax 归一化得到权重 $w_i = \frac{\exp(s_i)}{\sum_{j \in B} \exp(s_j)}$。最终预测为所有增强视图预测的加权集成：

$$p_{\mathrm{final}} = \arg\max_c \sum_{i \in B} w_i \, p_c(P_\theta(x_i))$$

该设计使与对抗样本填充嵌入相似、同时与对抗样本原始嵌入相异的视图获得更高权重，有效抑制了低质量增强视图的干扰。

### 模块间的条件依赖与解耦优势

三个模块之间存在明确的条件依赖关系：检测模块的输出决定了后续模块是否激活。这种解耦设计带来两个关键优势：其一，干净样本完全绕过适配流程，保证了原始 CLIP 的零样本精度不受任何折损（Table 6 显示 TTP 在各骨干网络上保持了最优的干净准确率）；其二，检测器本身具有跨架构、跨数据集的通用性——实验表明，TTP 在 ViT-B/32、ViT-B/16、ViT-L/14 三种骨干及多个细粒度数据集上均达到了接近 100% 的检测准确率（Figure 2），而同期检测方法 **TTC**（Xing et al., CVPR 2025）的检测准确率则在不同设置下波动较大且整体偏低。此外，TTP 的检测模块可无缝嵌入任何现有的测试时适配方法中，为其提供对抗样本感知能力，进一步扩展了框架的适用范围。

### 补充图表

![[assets/figures/papers/paper_list_l795_https_arxiv_org_abs_2512_16523/figures/003_Figure_3.jpg]]
*Figure 3: Overview of the proposed Test-Time Padding (TTP) pipeline. Given an input sample, CLIP image encoder features are extracted before and after applying padding. Their cosine similarity difference is compared with a universal threshold to distinguish clean versus adversarial inputs. Clean samples are directly recognized without adaptation. For adversarial examples, trainable test-time padding is activated to optimize padding parameters by entropy minimization using augmented views with low entropy. A similarityaware ensemble then aggregates predictions across selected high-confidence views, ensuring a more reliable final prediction. Together, TTP enables accurate adversarial detection and adap...*



### 3.1 问题形式化与 CLIP 零样本分类

给定一个测试图像 $x_i$，CLIP 模型通过图像编码器 $F$ 和文本编码器 $G$ 分别提取视觉与文本特征。对于 $C$ 个类别，每个类别 $c$ 的文本特征通过将类别名嵌入提示模板后经文本编码器得到：

$$g_c = G(\mathrm{prompt}(t_c)), \quad c = 1, \ldots, C$$

图像特征直接由图像编码器提取：

$$f_i = F(x_i)$$

基于余弦相似度与温度参数 $\tau$，零样本分类概率为：

$$p_c(x_i) = \frac{\exp(\cos(f_i, g_c) / \tau)}{\sum_{j=1}^{C} \exp(\cos(f_i, g_j) / \tau)}$$

上述公式构成了 TTP 方法的基础推理框架。对抗攻击通过在 $x_i$ 上叠加精心设计的微小扰动 $\delta$，使模型对 $p_c$ 的预测发生错误。

### 3.2 对抗检测模块：基于固定填充的余弦相似度漂移

TTP 的核心洞察在于：空间填充操作能够部分恢复对抗扰动破坏的注意力模式，且这种恢复效果在干净样本与对抗样本上呈现出显著差异。

**检测原理。** 给定测试样本 $x$，首先提取其原始嵌入 $z$ 与固定填充后的嵌入 $z^{\mathrm{pad}}$：

$$z = F(x), \quad z^{\mathrm{pad}} = F(P^{\mathrm{fix}}(x))$$

其中 $P^{\mathrm{fix}}$ 为固定参数的填充操作（如 0 填充或 255 填充）。计算两者之间的余弦相似度作为检测指标：

$$s = \frac{z \cdot z^{\mathrm{pad}}}{\|z\| \|z^{\mathrm{pad}}\|}$$

干净样本在填充前后特征变化极小，$s$ 值接近 1；而对抗样本因扰动破坏了原始注意力模式，填充操作可部分恢复该模式，导致 $s$ 值显著降低。通过设定统一阈值 $\tau = 0.8$，即可实现跨架构、跨数据集的二分类检测。消融实验表明，0 填充和 255 填充的检测准确率分别达到 98.5% 和 98.7%，均优于随机填充的 95.8%（Table 4）。

### 3.3 可训练填充适配模块：单步熵最小化

对于检测为对抗的样本，TTP 引入可训练填充参数 $\theta$，通过单步优化恢复被破坏的注意力模式。

**训练策略。** 对对抗样本生成多个增强视图，仅保留低熵（高置信度）视图构成集合 $B$。以最小化这些视图的平均熵为目标，对 $\theta$ 执行单步梯度更新：

$$\mathcal{L}_{\mathrm{ent}} = \frac{1}{|B|} \sum_{i \in B} H_i^{\mathrm{pad}}, \quad \theta \gets \theta - \eta \nabla_\theta \mathcal{L}_{\mathrm{ent}}$$

其中 $H_i^{\mathrm{pad}}$ 为第 $i$ 个增强视图经可训练填充后的预测熵。单步更新的设计在保证适配效果的同时，避免了测试时多步优化的计算开销。

### 3.4 相似度感知集成模块：自适应加权预测

为抑制增强视图中的噪声并突出与对抗样本语义一致的视图，TTP 设计了相似度感知集成策略。

**权重计算。** 对每个增强视图 $x_i$，计算其填充嵌入 $z_i^{\mathrm{pad}}$ 与对抗样本填充嵌入 $z_{\mathrm{adv}}^{\mathrm{pad}}$ 的余弦相似度 $\alpha_i$，以及 $z_i^{\mathrm{pad}}$ 与对抗样本原始嵌入 $z_{\mathrm{adv}}$ 的余弦相似度 $\beta_i$：

$$\alpha_i = \cos(z_i^{\mathrm{pad}}, z_{\mathrm{adv}}^{\mathrm{pad}}), \quad \beta_i = \cos(z_i^{\mathrm{pad}}, z_{\mathrm{adv}})$$

视图得分定义为两者之差，反映该视图与“恢复后”对抗样本的相似程度：

$$s_i = \alpha_i - \beta_i$$

通过 softmax 归一化得到各视图权重：

$$w_i = \frac{\exp(s_i)}{\sum_{j \in B} \exp(s_j)}$$

**最终预测。** 对所有增强视图的类别预测进行加权集成：

$$p_{\mathrm{final}} = \arg\max_c \sum_{i \in B} w_i \, p_c(P_\theta(x_i))$$

该策略使与对抗样本填充嵌入高度相似（$\alpha_i$ 大）且与原始对抗嵌入差异明显（$\beta_i$ 小）的视图获得更高权重，有效抑制了对抗噪声对集成结果的干扰。消融实验证实，移除相似度感知集成或可训练填充均导致对抗准确率显著下降。

### 补充图表

![[assets/figures/papers/paper_list_l795_https_arxiv_org_abs_2512_16523/figures/001_Figure_1.jpg]]
*Figure 1: Visualization of attention maps for clean sample, adversarially perturbed sample, randomly padded sample, and samples processed with trainable test-time padding. The adversarial attack causes a noticeable shift in attention, leading to incorrect predictions. Applying random padding helps restore the original attention focus, while trainable padding further refines the attention to the correct regions and suppresses noise, resulting in more accurate predictions*



## 实验与关键发现

### 对抗鲁棒性主结果

TTP 在 8 个细粒度分类数据集（Caltech101、Pets、Cars、Flower102、Aircraft、DTD、EuroSAT、UCF101）上，以 PGD 攻击（ε=4/255，100 步迭代）评估对抗鲁棒性。核心发现是：**TTP 在显著提升对抗准确率的同时，保持了与冻结 CLIP 相当的干净样本准确率**。

在 ViT-B/32 骨干下，TTP 达到平均对抗准确率 **39.7%**，比当时最强的测试时防御方法 **R-TPT**（Sheng et al., CVPR 2025）高出 **4.4 个百分点**（Table 1）。更值得关注的是跨架构的泛化表现：ViT-B/16 下平均对抗准确率升至 **42.9%**（Table 2），ViT-L/14 下进一步达到 **51.6%**（Table 3），这表明 TTP 的填充策略能有效利用更大模型的更强表征能力。

![[assets/figures/papers/paper_list_l795_https_arxiv_org_abs_2512_16523/figures/004_Table_1.jpg]]
*Table 1: Clean (Acc.) and adversarial (Rob.) accuracy (%) on fine-grained classification datasets with pre-trained CLIP-ViT-B/32 (ϵ = 4.0). The best results of clean accuracy are bolded, and the best results of robustness are bolded*

![[assets/figures/papers/paper_list_l795_https_arxiv_org_abs_2512_16523/figures/005_Table_2.jpg]]
*Table 2: Adversarial (Rob.) and Clean (Acc.) accuracy (%) on fine-grained classification datasets with pre-trained CLIP-ViT-B/16 (ϵ = 4.0). The best results of clean accuracy are bolded, and the best results of robustness are bolded*

![[assets/figures/papers/paper_list_l795_https_arxiv_org_abs_2512_16523/figures/006_Table_3.jpg]]
*Table 3: Adversarial (Rob.) and Clean (Acc.) accuracy (%) on fine-grained classification datasets with pre-trained CLIP-ViT-L/14 (ϵ = 4.0). The best results of clean accuracy are bolded, and the best results of robustness are bolded*

在干净准确率方面，TTP 在三种骨干下的平均干净准确率均与零样本 CLIP 持平或略优（Table 6），验证了其检测机制的有效性——干净样本被正确识别后直接通过冻结 CLIP 预测，避免了不必要的适配带来的性能退化。这与 **TTC**（Xing et al., CVPR 2025）、**R-TPT** 等方法形成对比：后者对所有输入统一适配，导致干净准确率出现不同程度的下降。

![[assets/figures/papers/paper_list_l795_https_arxiv_org_abs_2512_16523/figures/009_Table_6.jpg]]
*Table 6: Average clean accuracy (Acc.) of various test-time defenses across fine-grained classification datasets under various CLIP architectures. The best results of clean accuracy are bolded*

### 跨攻击类型的鲁棒性

TTP 的鲁棒性不局限于 PGD 攻击。在 CW、DeepFool 和 FGSM 三种不同范式的攻击下，TTP 在 Flower102 和 DTD 两个数据集上均取得最高的对抗准确率（Table 5）。具体而言，Flower102 上三种攻击的平均对抗准确率为 **54.1%**，DTD 上为 **38.7%**，均显著优于对比方法。这表明填充操作所恢复的注意力模式具有攻击类型无关的特性，而非针对特定梯度方向的过拟合。

![[assets/figures/papers/paper_list_l795_https_arxiv_org_abs_2512_16523/figures/008_Table_5.jpg]]
*Table 5: Adversarial accuracies (%) under CW, DeepFool (DF), and FGSM attacks on two fine-grained datasets. TTP achieves more robust performance. The best results of robustness are bolded*

### 检测性能分析

TTP 的核心创新在于通过固定填充前后的嵌入余弦相似度漂移实现对抗样本检测。实验表明，该检测器在 ViT-B/32、ViT-B/16、ViT-L/14 三种骨干下，跨 8 个数据集均达到**接近 100% 的检测准确率**（Figure 2）。相比之下，**TTC** 的检测准确率在不同数据集和骨干间波动剧烈且整体偏低。

![[assets/figures/papers/paper_list_l795_https_arxiv_org_abs_2512_16523/figures/002_Figure_2.jpg]]
*Figure 2: Detection accuracy of TTP (ours) and TTC [46] across fine-grained classification datasets under three CLIP backbones (ViT-B/32, ViT-B/16, and ViT-L/14). All experiments are performed under the same attack strength of*

检测机理的定量支撑来自填充前后的余弦相似度统计：干净样本的填充前后嵌入高度一致，而对抗样本因注意力模式被破坏，填充后嵌入发生显著偏移（Figure 4a）。这种差异在填充尺寸为 20–30 像素时最为显著，对应的检测准确率达到峰值（Figure 4b），同时对抗准确率也在该区间达到最优（Figure 4c），验证了检测与适配之间的协同关系。

### 填充模式与参数消融

Table 4 对比了三种填充模式在 ViT-B/32 下的检测准确率：0 填充（黑色边框）达到 **98.5%**，255 填充（白色边框）达到 **98.7%**，均显著优于随机填充的 **95.8%**。这表明检测信号来源于空间结构的引入本身，而非填充值的具体分布——固定值填充为模型提供了稳定的空间参考，使被对抗扰动破坏的注意力得以部分恢复。

![[assets/figures/papers/paper_list_l795_https_arxiv_org_abs_2512_16523/figures/007_Table_4.jpg]]
*Table 4: Detection accuracy (%) of TTP using different padding patterns on fine-grained classification datasets with pre-trained CLIP-ViT-B/32 (ϵ = 4.0). The best results are (bolded)*

完整的组件消融（Table 7）进一步揭示：
- 移除可训练填充（仅保留检测 + 固定填充）导致对抗准确率大幅下降；
- 移除相似度感知集成（改用简单平均）同样造成显著性能损失；
- 三个组件（检测、可训练填充、相似度感知集成）缺一不可，共同构成 TTP 的完整防御链路。

### 与测试时适配方法的集成

TTP 的检测模块可以作为即插即用的前置组件，与任意测试时适配方法集成。实验表明，将 TTP 检测器与现有适配方法结合后，干净样本直接通过冻结 CLIP 预测，对抗样本交由适配方法处理，既能保持干净准确率不下降，又能获得适配方法带来的鲁棒性增益。这种模块化设计使 TTP 具有高度的实用灵活性。

### 失败模式与局限性

当前分析中未提供 TTP 在更强攻击（如 AutoAttack、多步自适应攻击）或更大扰动幅度下的性能数据，其在极端对抗场景下的检测可靠性需要进一步验证。此外，可训练填充的单步熵最小化依赖于高置信度视图的筛选，当对抗样本使模型对所有增强视图都产生低置信度时，优化信号可能不足，这一点在现有实验中尚未充分讨论，需要手动验证。

### 补充图表

![[assets/figures/papers/paper_list_l795_https_arxiv_org_abs_2512_16523/figures/010_Figure.jpg]]
*Figure: (a) Average cosine similarity. (b) Detection accuracy. (c) Adversarial Accuracy (Rob.) on DTD dataset*

![[assets/figures/papers/paper_list_l795_https_arxiv_org_abs_2512_16523/figures/011_Figure_4.jpg]]
*Figure 4: Impact of padding size on adversarial detection and robust adaptation. ViT-B/32 is used as the CLIP backbone. The figure comprises three subplots: (a) average cosine similarities on fine-grained classification datasets of CLIP embeddings before and after padding across varying padding sizes, (b) detection accuracy for both adversarial and clean inputs, and (c) adversarial accuracy on the DTD dataset*



## 定位与知识库关联

### 测试时防御的两阶段范式分化

TTP 的提出源于对现有测试时防御方法一个关键瓶颈的识别：**缺乏可靠的对抗样本检测机制**。当前主流的测试时防御方法——包括测试时提示微调（Test-Time Prompt Tuning）和测试时增强集成（Test-Time Augmentation）——对所有输入样本统一施加适配操作，这一“无差别对待”策略导致干净准确率与对抗鲁棒性之间存在根本性冲突。

具体而言，现有方法可沿两个维度进行定位：

**统一适配范式**（无检测机制）：
- **R-TPT**（Sheng et al., CVPR 2025）和 **TAPT**（Wang et al., CVPR 2025）属于测试时提示微调路线，通过在推理阶段优化文本提示来提升对抗鲁棒性，但所有样本（包括干净样本）均需经过优化过程，导致干净准确率下降。
- **MTA**（Zanella and Ben Ayed, CVPR 2024）和简单的 **Ensemble** 方法通过多增强视图集成来提升鲁棒性，同样对所有输入统一处理，未区分干净与对抗样本。

**两阶段检测-适配范式**：
- **TTC**（Xing et al., CVPR 2025）率先提出检测+对抗的两阶段框架，通过在输入上施加小噪声并计算特征嵌入的 L2 距离来检测对抗样本。然而，TTC 的检测准确率在不同数据集和模型架构上表现不稳定且波动较大（见 Figure 2），限制了其实际部署的可靠性。

TTP 在 TTC 的两阶段框架基础上实现了关键突破：**将检测机制从 L2 距离替换为填充前后的余弦相似度漂移**。这一改变使检测准确率从 TTC 的低波动状态跃升至接近 100%（跨架构、跨数据集通用），为两阶段范式提供了首个可靠的检测基础。

### 因果机制的差异化

TTP 与现有方法的本质区别在于其操作的“因果杠杆”位置：

- **R-TPT / TAPT** 在文本提示空间操作，通过对抗性优化文本嵌入来间接影响分类决策。这种方法依赖梯度信号在文本-图像跨模态空间中的传递，优化过程黑箱且缺乏对注意力破坏的直接修复。
- **MTA / Ensemble** 在增强视图空间操作，通过多视图平均来抑制对抗噪声，但未主动恢复被破坏的注意力模式，本质上是一种被动防御。
- **TTP** 直接在**图像输入空间**操作，通过空间填充操作部分恢复因对抗扰动而破坏的注意力模式（如 Figure 1 所示）。其核心因果机制是：对抗扰动导致注意力显著偏移，而填充操作能够将注意力重新引导至正确区域——这一机制在干净样本上几乎不产生特征变化，从而天然地将检测与适配解耦。

### 适用边界与组件贡献

TTP 的适用边界由其三个模块的协同关系定义：

1. **对抗检测模块**：依赖固定填充（0 填充或 255 填充）产生的余弦相似度漂移信号。在 ViT-B/32 上，0 填充和 255 填充的检测准确率分别达到 98.5% 和 98.7%，显著优于随机填充的 95.8%（Table 4）。该模块的通用性使得 TTP 可以“无缝集成到任何现有测试时适配方法中”（原文 claim），为其作为防御前置模块的生态定位提供了依据。

2. **可训练填充适配模块**：仅对检测为对抗的样本激活，通过单步熵最小化优化填充参数。消融实验（Table 7）表明，移除该模块将导致对抗准确率显著下降，验证了其不可替代性。

3. **相似度感知集成模块**：利用增强视图与对抗样本在填充前后嵌入的余弦相似度差异（$s_i = \alpha_i - \beta_i$）计算自适应权重，抑制低置信度视图的噪声贡献。该模块与可训练填充形成互补——前者恢复注意力，后者过滤残余噪声。

### 跨攻击泛化能力

TTP 在 PGD 攻击（100 步迭代，$\epsilon = 4/255$）之外，对 CW、DeepFool 和 FGSM 攻击同样展现出一致的鲁棒性优势（Table 5），表明其防御机制并非针对特定攻击类型的过拟合，而是源于对注意力破坏这一通用对抗效应的修复。

### 局限与开放问题

尽管 TTP 在检测准确率和对抗鲁棒性上取得了显著提升，以下问题仍需进一步验证（原文未提供明确结论，需手动核实）：

1. **自适应攻击的鲁棒性**：TTP 的检测机制依赖填充操作产生的特征漂移，若攻击者将填充操作纳入攻击目标（即构造能绕过余弦相似度检测的对抗样本），TTP 的检测准确率是否仍能维持接近 100% 的水平，原文未提供相关实验。

2. **填充大小的敏感性**：Figure 4 展示了填充大小对检测和鲁棒性的影响，但最优填充大小是否跨数据集和架构保持稳定，以及是否存在统一的自动选择策略，原文未给出明确结论。

3. **计算开销的量化**：TTP 对检测为对抗的样本进行单步优化和集成推理，其相对于统一适配方法（如 R-TPT）的实际推理延迟增加量，原文未提供详细的耗时对比数据。

4. **非 CLIP 架构的迁移性**：TTP 的所有实验均基于 CLIP 视觉-语言模型，其在纯视觉模型（如标准 ViT、ResNet）上的检测与适配效果尚未验证，填充操作对注意力恢复的因果机制是否依赖于 CLIP 的跨模态训练范式仍是开放问题。



## 原文 PDF

![[paperPDFs/CVPR_2026/TTP_Test_Time_Padding_for_Adversarial_Detection_and_Robust_Adaptation_on_Vision_Language_Models.pdf]]
