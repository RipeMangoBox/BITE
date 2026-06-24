---
title: Does YOLO Really Need to See Every Training Image in Every Epoch?
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Does_YOLO_Really_Need_to_See_Every_Training_Image_in_Every_Epoch.pdf
project_link: null
code_link: null
aliases:
- AFSSA
- DYRNSETIEE
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过定义图像级“学习充分性”（Learning Sufficiency）——即当前检测器在该图像上的精度与召回率的最小值——并以此为依据动态调整每张图像在每个epoch中的参与频次。充分学好的图像（简单）极低频次回顾；部分学好的图像（中等）保证短期窗口内的覆盖；未学好的图像（困难）则全量参与。这一调度直接决定了训练计算量的分配，从而加速或减缓整体训练进程。
primary_logic: AFSS的核心思想是将训练数据视为具有动态学习价值的资源：利用min(Precision, Recall)作为统一度量，将图像分为简单、中等、困难三种状态，并分别施加持续回顾、短期强制覆盖和全量参与三种互补采样策略。这种方法不仅大幅削减了简单样本的冗余计算，还通过精心设计的“反遗忘”机制（对长期未见的简单图像强制重访；对中等图像在3个epoch内保证至少出现一次）稳定保留已学知识，从而在显著加速训练的同时保持甚至提升精度。
claims:
- AFSS使YOLO11s在MS COCO上的训练加速1.54倍，同时AP从47.0提升至47.2，训练时间从43.9小时显著缩短。
- 在YOLOv8、YOLOv10、YOLO11、YOLO12等多个模型上，AFSS实现了超过1.43倍的训练加速，且准确率无损失或有所提升。
- 在遥感图像检测数据集DOTA-v1.0和DIOR-R上，AFSS为YOLOv8-OBB和YOLO11-OBB带来了超过1.63倍的训练加速，同时mAP一致提升。
- 消融实验证实，学习充分性度量（min(Prec, Rec)）、连续回顾（间隔10 epoch）、短期覆盖（间隔3 epoch）和状态更新（每5 epoch）四大组件协同作用，缺少任何组件都会导致加速比或准确率下降。
---

# Does YOLO Really Need to See Every Training Image in Every Epoch?

> [!tip] 核心洞察
> AFSS的核心思想是将训练数据视为具有动态学习价值的资源：利用min(Precision, Recall)作为统一度量，将图像分为简单、中等、困难三种状态，并分别施加持续回顾、短期强制覆盖和全量参与三种互补采样策略。这种方法不仅大幅削减了简单样本的冗余计算，还通过精心设计的“反遗忘”机制（对长期未见的简单图像强制重访；对中等图像在3个epoch内保证至少出现一次）稳定保留已学知识，从而在显著加速训练的同时保持甚至提升精度。

| 字段 | 内容 |
|------|------|
| 中文题名 | YOLO真的需要在每个epoch都看到所有训练图像吗？ |
| 英文题名 | Does YOLO Really Need to See Every Training Image in Every Epoch? |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.17684) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Anti-Forgetting Sampling Strategy (AFSS) |
| Dataset | MS COCO 2017, PASCAL VOC 2007, DOTA-v1.0 |

> [!tip] 效果简介
> - MS COCO 2017 上，AP (YOLO11s) 47.2 vs 47.0 (+0.2)；Training speedup (YOLO11s) 1.54× vs 1× (+0.54×)；Training speedup (YOLOv8n) 1.43× vs 1× (+0.43×)。
> - PASCAL VOC 2007 上，Training speedup (YOLOv8n) 1.60× vs 1× (+0.60×)。
> - DOTA-v1.0 上，Training speedup (YOLOv8-OBB / YOLO11-OBB) >1.63× vs 1× (>+0.63×)。

## 概述

YOLO系列检测器以极快的推理速度著称，但其训练过程却异常低效——标准训练范式要求每个epoch遍历全部训练图像，导致大量已被充分学习的简单样本被重复处理，产生巨大的冗余计算。这种“全覆盖”策略未考虑样本学习状态的动态变化，使得YOLO的训练时间远超Faster R-CNN等模型，成为制约其快速迭代和应用部署的核心瓶颈。

针对这一问题，本文提出**抗遗忘采样策略（Anti-Forgetting Sampling Strategy, AFSS）**，其核心思想是将训练数据视为具有动态学习价值的资源：通过定义图像级的“学习充分性”（Learning Sufficiency）度量，动态评估每张图像对当前检测器的学习价值，并据此自适应地调整其在每个epoch中的参与频次。具体而言，AFSS以检测精确率与召回率的最小值作为统一度量，将训练图像划分为简单、中等、困难三个等级，并分别施加持续回顾、短期强制覆盖和全量参与三种互补的采样策略。该方法不仅大幅削减了简单样本的冗余计算，还通过精心设计的“反遗忘”机制稳定保留已学知识。

实验结果表明，AFSS在多个YOLO系列模型和数据集上均取得了显著的训练加速效果，同时保持甚至提升了检测精度。在MS COCO 2017上，AFSS使YOLO11s的训练加速**1.54倍**，AP从47.0提升至**47.2**；在YOLOv8、YOLOv10、YOLO11、YOLO12等多个模型上实现了超过**1.43倍**的训练加速且精度无损；在遥感图像检测数据集DOTA-v1.0和DIOR-R上，为旋转目标检测器带来了超过**1.63倍**的训练加速，同时mAP一致提升。消融实验进一步证实，学习充分性度量、持续回顾、短期覆盖和状态更新四大组件协同作用，是AFSS取得上述性能的关键。

## 背景与动机

目标检测是计算机视觉的核心任务之一，YOLO系列检测器凭借其极快的推理速度在实时应用中占据主导地位。然而，YOLO的训练效率却远不如其推理效率那样令人满意——标准训练流程要求每个epoch遍历全部训练图像，导致训练时间异常冗长。以YOLO11s在MS COCO 2017上的训练为例，完整训练需耗时43.9小时，显著慢于Faster R-CNN等两阶段检测器。

这一效率瓶颈的根源在于**“全覆盖”训练范式对样本学习状态的漠视**。在训练初期，大量图像对模型而言是困难样本，需要充分学习；但随着训练推进，绝大多数图像逐渐被模型可靠检测，继续在每个epoch中全量使用这些“已学好”的图像只会产生冗余计算，对模型提升贡献甚微。标准YOLO训练未对图像的学习程度加以区分，等价处理所有样本，造成了严重的计算资源浪费。

现有研究已从多个角度尝试缓解训练冗余问题。**课程学习**（Self-Paced Learning, Kumar et al., NIPS 2010）通过从易到难的样本排序来组织训练，但未直接量化单张图像的学习完成度，且课程设计依赖启发式规则。**静态数据剪枝**方法（如Data Diet, Paul et al., NIPS 2021）在训练早期根据损失或梯度统计剔除“不重要”样本，然而一旦样本被丢弃便永久失去学习机会，无法适应模型能力的动态变化。**数据集蒸馏**（Fetch and Forge, Qi et al., NIPS 2024）试图合成少量代表图像替代原始训练集，但蒸馏过程本身计算代价高昂，且合成图像可能丢失细粒度检测信息。**损失加权方法**（如SuperLoss）通过样本损失值调节训练权重，但损失值仅反映当前batch内的相对难度，缺乏对检测任务中分类与定位双重目标的直接刻画。

上述方法的共同缺陷在于：**缺乏一个直接反映检测器对单张图像“学得如何”的统一度量，以及基于该度量的、能主动防止已学知识遗忘的动态调度机制**。检测任务要求模型同时准确分类和精确定位，仅靠损失或梯度等间接信号难以判断一张图像是否真正被“充分学习”。此外，简单地从训练集中丢弃样本或降低权重，可能引发灾难性遗忘——模型在长期未见某些图像后，其上的检测能力会逐渐退化。

本文的核心动机正是针对这一缺口：**设计一种能感知每张训练图像学习充分性、并据此动态调节其参与频次的训练调度策略，在显著削减冗余计算的同时，通过精心设计的“反遗忘”机制稳定保留已学知识，从而实现训练加速与精度保持的双赢**。

## 核心创新

AFSS 的核心创新在于将目标检测的训练数据从“静态资源”重新定义为“具有动态学习价值的资产”，并围绕这一理念构建了三个相互协同的 changed slot，从根本上改变了 YOLO 系列检测器的训练范式。

### 1. 学习充分性度量：从隐式损失到显式图像级信号

标准 YOLO 训练（Vanilla）对每张图像的学习状态缺乏显式建模——仅依靠 mini-batch 损失间接反映，且损失值受目标数量、尺度等因素污染，无法准确表征单张图像是否已被“充分学习”。AFSS 引入了 **Learning Sufficiency Metric (LSM)**，将图像 $\mathbf{I}_i$ 的学习充分性定义为检测精确率 $P_i$ 与召回率 $R_i$ 的最小值：

$$\mathrm{Learning\ sufficiency\ for\ } \mathbf{I}_i = \mathrm{min}(P_i, R_i).$$

这一设计的因果逻辑是：目标检测的性能瓶颈取决于分类与定位中**较弱的一方**。若一张图像上所有目标均被正确分类但定位框偏移严重（$P_i$ 高、$R_i$ 低），或所有目标均被找到但类别频繁误判（$R_i$ 高、$P_i$ 低），该图像对当前检测器而言仍具有显著的学习价值。$\min(P_i, R_i)$ 作为统一度量，直接暴露了检测器在该图像上的能力短板，为后续采样决策提供了可靠的信号基础。

消融实验证实了这一选择的有效性：在几乎相同的加速比下，$\min(P_i, R_i)$ 相比基于 Loss、Gradient 或 F1-score 的度量方式获得了更高的 AP（Table 5a）。基于此度量，AFSS 将训练图像动态划分为三个难度级别：

$$\left\{ \begin{array}{lll} \mathrm{Easy}, & \mathrm{if~} \operatorname*{min}(P_i, R_i) > 0.85, \\ \mathrm{Moderate}, & \mathrm{if~} 0.55 \leq \operatorname*{min}(P_i, R_i) \leq 0.85, \\ \mathrm{Hard}, & \mathrm{if~} \operatorname*{min}(P_i, R_i) < 0.55. \end{array} \right.$$

### 2. 差异化采样调度：从“全覆盖”到“按需参与”

Vanilla 训练在每个 epoch 使用全部训练图像进行前向和反向传播，所有图像被等价处理，导致大量已充分学习的简单样本产生冗余计算。AFSS 针对三种难度级别设计了**差异化、互补的采样策略**：

- **困难图像（Hard）**：全量参与每个 epoch 的训练。这些图像的学习充分性低于 0.55，检测器尚未可靠地完成分类和定位，需要密集的梯度更新来持续改进。

- **中等图像（Moderate）**：每 epoch 采样约 40% 的该组图像，并施加 **Short-Term Coverage (STC)** 约束——优先选取已有 3 个 epoch 以上未被使用的样本，即强制覆盖子集：

  $$\mathcal{B}_{\mathrm{f}}=\{(\mathbf{I}_{i},P_{i},R_{i},ep_{i})\in\mathcal{D}_{t-1}^{2}\mid t-1-ep_{i}\geq 3\}.$$

  这确保了所有中等图像在短时间窗口内都能被重新访问，防止因过疏参与导致的特征表征退化，同时将计算量削减约 60%。

- **简单图像（Easy）**：每 epoch 仅随机选取该组图像的 2%，并施加 **Continuous Review (CR)** 约束——从超过 10 个 epoch 未被使用的简单图像中强制挑选一部分进行回顾：

  $$E_{1}+E_{2}=0.02\times|\mathcal{D}_{t-1}^{1}|,\quad E_{1}\leq 0.5\times 0.02\times |\mathcal{D}_{t-1}^{1}|.$$

  其中 $E_1$ 为强制回顾样本数，上限为总采样数的一半；$E_2$ 为随机采样数。这种“稀疏但稳定”的回顾机制以极低计算代价防止已学知识的灾难性遗忘。

三种策略的协同效果在消融实验中得到了验证：完整 AFSS（包含 LSM、CR、STC、SU）在 YOLO11s 上取得 47.2 AP 和 1.54× 加速，去除任一组件均导致精度下降或加速比减小（Table 4）。

### 3. 自适应状态更新：从固定遍历到协同进化

Vanilla 训练的数据遍历顺序固定，不使用长期状态信息，模型能力提升与数据参与模式之间缺乏反馈闭环。AFSS 引入了 **State Update (SU)** 机制，使数据调度与模型能力协同进化：

- 每经过 5 个训练 epoch，使用当前检测器 $f_{\phi_t}$ 重新计算每张图像的精确率和召回率以更新其学习充分性：

  $$(P_{i}^{\prime},R_{i}^{\prime})=\big(\mathrm{Prec}(f_{\phi_{t}}(\mathbf{I}_{i})),\mathrm{Rec}(f_{\phi_{t}}(\mathbf{I}_{i}))\big) \quad \text{if } (t-\tau)\bmod 5=0.$$

- 其余 epoch 复用历史值，以较低的评估开销保持状态新鲜度。

- 同时更新每张图像的“最后使用 epoch”记录，为下一 epoch 的 CR 和 STC 调度提供准确的遗忘风险信息。

这一设计使得随着训练推进，越来越多的图像从“困难”迁移至“中等”乃至“简单”（Figure 3 展示了这一动态过程），AFSS 自动削减其参与频次，将计算资源集中于仍需学习的样本。消融实验表明，每 5 epoch 更新一次状态是最优选择——既能及时反映模型学习进展，又不会引入过多评估开销（Table 5d）。

## 整体框架

AFSS（Anti-Forgetting Sampling Strategy）的核心设计理念是将训练数据视为具有动态学习价值的资源，而非在每个epoch中无差别地全量遍历。其整体框架围绕一个闭环的“评估—分级—调度—更新”循环构建，如图2所示，在每个训练epoch中依次执行以下四个核心模块：

1. **学习充分性度量（Learning Sufficiency Metric, LSM）**：使用当前检测器对每张训练图像计算精确率 $P_i$ 和召回率 $R_i$，并取两者的最小值作为该图像的“学习充分性”分数——即 $\mathrm{min}(P_i, R_i)$。这一度量聚焦于检测器中较弱的预测维度，确保图像只有在分类和定位都可靠时才被视为充分学习。随后，根据该分数将图像动态划分为三个难度级别：简单（$>0.85$）、中等（$[0.55, 0.85]$）和困难（$<0.55$）。

2. **连续回顾（Continuous Review, CR）**：针对简单图像，每epoch仅随机选取该组总量的2%参与训练，并强制从超过10个epoch未被使用的图像中挑选一部分进行回顾。这种稀疏但稳定的重访机制以极低的计算代价防止已学知识的遗忘。

3. **短期覆盖（Short-Term Coverage, STC）**：针对中等图像，每epoch采样约40%的该组样本，优先选取已有3个epoch以上未被使用的图像，确保所有中等样本在短时间窗口内都能被重新访问，维持特征与类别边界的对齐。

4. **状态更新（State Update, SU）**：在每个epoch结束后，更新所有图像的学习充分性（每5个epoch用当前模型重新评估一次）和最后使用epoch记录，为下一epoch的调度决策提供最新的状态字典。

困难图像则始终全量参与训练，不施加任何采样约束。整个pipeline的输出是一个经过AFSS筛选的训练图像子集，该子集被送入标准的YOLO检测器（如YOLOv8、YOLOv10、YOLO11、YOLO12等）执行正常的前向和反向传播。四个模块协同作用，使得训练计算量从“全覆盖”范式转变为“按需分配”范式：简单样本的计算冗余被大幅削减，困难样本获得充分的学习机会，中等样本则通过强制覆盖机制避免表征退化。消融实验证实，缺少任一组件都会导致加速比下降或精度损失（Table 4）。

### 补充图表

![[assets/figures/papers/paper_list_l2120_https_arxiv_org_abs_2603_17684/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the proposed Anti-Forgetting Sampling Strategy (AFSS) at the t-th epoch of training*

## 核心模块与公式推导

AFSS 的核心由四个协同模块构成：**学习充分性度量（LSM）**、**连续回顾（CR）**、**短期覆盖（STC）** 和 **状态更新（SU）**。它们共同定义了“每张训练图像在每个 epoch 中是否应该参与训练”的动态调度策略。

### 3.1 学习充分性度量（Learning Sufficiency Metric, LSM）

LSM 是 AFSS 的决策基础。对于训练图像 $\mathbf{I}_i$，定义其学习充分性为当前检测器在该图像上的精确率 $P_i$ 与召回率 $R_i$ 的最小值：

$$\mathrm{Learning\ sufficiency\ for\ } \mathbf{I}_i = \mathrm{min}(P_i, R_i). \tag{1}$$

**设计动机**：取 $\mathrm{min}$ 而非均值或 F1-score，是因为它直接暴露检测器在分类与定位两个维度中较弱的那个。只有当两者都足够高时，图像才被视为“已充分学习”。消融实验证实，$\mathrm{min}(P, R)$ 在几乎相同的加速比下比基于 Loss、Gradient 或 F1-score 的度量获得了更高的 AP（Table 5a）。

基于该分数，图像被动态划分为三个难度级别：

$$\left\{ \begin{array}{lll} \mathrm{Easy}, & \mathrm{if~} \operatorname*{min}(P_i, R_i) > 0.85, \\ \mathrm{Moderate}, & \mathrm{if~} 0.55 \leq \operatorname*{min}(P_i, R_i) \leq 0.85, \\ \mathrm{Hard}, & \mathrm{if~} \operatorname*{min}(P_i, R_i) < 0.55. \end{array} \right. \tag{2}$$

这一分层是后续三种差异化采样策略的调度依据。训练过程中，随着模型能力提升，大量图像从 Hard/Moderate 迁移至 Easy，每 epoch 实际使用的图像数量自然递减（Figure 3）。

### 3.2 连续回顾（Continuous Review, CR）

CR 针对 Easy 图像，以极低频率维持对已学知识的“反遗忘”刺激。每 epoch 仅从 Easy 组 $\mathcal{D}_{t-1}^{1}$ 中采样 **2%** 的图像参与训练，且强制回顾长期未见的样本。

设 $E_1$ 为强制回顾子集（超过 10 个 epoch 未被使用的 Easy 图像），$E_2$ 为随机补充子集。调度约束为：

$$E_{1}+E_{2}=0.02\times|\mathcal{D}_{t-1}^{1}|,\quad E_{1}\leq0.5\times0.02\times|\mathcal{D}_{t-1}^{1}|. \tag{6}$$

**因果机制**：仅靠随机 2% 采样可能导致某些 Easy 图像长期“失联”，引发灾难性遗忘。强制回顾子集 $E_1$ 确保长期未激活的神经元通路被周期性唤醒，且其占比不超过 Easy 采样总量的一半，以保留一定的随机多样性。消融实验表明，回顾间隔设为 10 epoch 时，精度与训练时间的平衡最优（Table 5b）。

### 3.3 短期覆盖（Short-Term Coverage, STC）

STC 处理 Moderate 图像——它们尚未被充分学习，但也不像 Hard 图像那样需要全量参与。每 epoch 从 Moderate 组 $\mathcal{D}_{t-1}^{2}$ 采样约 **40%** 的图像，并优先选取已有 3 个 epoch 以上未被使用的样本。

强制覆盖子集定义为：

$$\mathcal{B}_{\mathrm{f}}=\{(\mathbf{I}_{i},P_{i},R_{i},ep_{i})\in\mathcal{D}_{t-1}^{2}\mid t-1-ep_{i}\geq3\}. \tag{7}$$

其中 $ep_i$ 记录图像 $\mathbf{I}_i$ 上次参与训练的 epoch。该条件确保任何 Moderate 图像在 **3 个 epoch 的滑动窗口内至少被访问一次**。

**因果机制**：Moderate 图像处于“部分学习”状态，其特征表示和类别边界尚不稳定。若参与间隔过长，模型可能遗忘已建立的弱关联；若全量参与，则损失加速收益。3-epoch 强制覆盖在两者间取得平衡——消融实验显示，该间隔能提供稳定的性能表现（Table 5c）。

### 3.4 状态更新（State Update, SU）

SU 负责维护每张图像的动态状态字典，使 AFSS 的调度策略与模型能力协同进化。在每个 epoch 结束后，SU 执行两项操作：

1. **更新最后使用 epoch**：对所有参与当前 epoch 训练的样本，记录 $ep_i = t$。
2. **周期性重评学习充分性**：每 **5 个 epoch**，用当前检测器 $f_{\phi_t}$ 重新计算所有训练图像的精确率和召回率：

$$(P_{i}^{\prime},R_{i}^{\prime})=\big(\mathrm{Prec}(f_{\phi_{t}}(\mathbf{I}_{i})),\mathrm{Rec}(f_{\phi_{t}}(\mathbf{I}_{i}))\big) \quad \text{if } (t-\tau)\bmod 5=0. \tag{13}$$

其余 epoch 复用历史值，以控制评估开销。更新后的 $(P_i, R_i)$ 重新计算学习充分性并更新难度标签，为下一 epoch 的 CR 和 STC 调度提供最新状态。

**因果机制**：5-epoch 更新间隔是精度与开销的折中——过短则评估成本侵蚀加速收益，过长则状态滞后导致调度失准。消融实验确认该间隔为最优选择（Table 5d）。

### 模块协同与整体调度

Figure 2 展示了 AFSS 在第 $t$ 个 epoch 的完整流程：

1. **SU 提供状态**：从状态字典读取每张图像的 $(P_i, R_i)$、难度标签和 $ep_i$。
2. **LSM 分层**：根据 $\mathrm{min}(P_i, R_i)$ 将图像分为 Easy / Moderate / Hard 三组。
3. **差异化采样**：Hard 图像全量使用；Moderate 图像经 STC 采样约 40%；Easy 图像经 CR 采样 2%。
4. **YOLO 训练**：采样后的子集送入检测器执行标准前向/反向传播。
5. **SU 更新**：epoch 结束后更新 $ep_i$，每 5 epoch 触发一次全量重评。

四个模块的协同作用在消融实验中得到了严格验证：完整 AFSS 在 YOLO11s 上取得 47.2 AP 和 1.54× 加速；去除任一组件均导致精度下降或加速比减小（Table 4）。

## 实验与分析

### 核心实验设置

AFSS 的实验验证覆盖了通用目标检测与遥感旋转目标检测两大场景。通用检测在 MS COCO 2017 和 PASCAL VOC 2007 上进行，评估指标为 COCO 上的 AP@[.5:.95] 和 VOC 上的 mAP@0.5；遥感检测在 DOTA-v1.0 和 DIOR-R 上进行，评估指标为 mAP@0.5。所有训练加速实验均在相同硬件配置（两块 NVIDIA RTX 4090 24GB）下完成，训练超参数与 baseline 保持一致，确保了比较的公平性。

### 主实验结果

AFSS 在多个 YOLO 模型上实现了超过 1.43 倍的训练加速，同时准确率无损失或有所提升。**Table 1** 汇总了 MS COCO 2017 和 PASCAL VOC 2007 上的详细对比：YOLOv8n 在 COCO 上训练时间从 30.3h 缩短至 21.2h（1.43× 加速），AP 保持 37.4；YOLO12x 训练时间从 260.1h 缩短至 154.8h（1.68× 加速），AP 保持 55.4；在 PASCAL VOC 2007 上，YOLOv8n 实现 1.60× 加速。**Table 2** 展示了遥感场景下的结果：在 DOTA-v1.0 和 DIOR-R 上，AFSS 为 YOLOv8-OBB 和 YOLO11-OBB 带来超过 1.63× 的训练加速，且 mAP 一致提升。

![[assets/figures/papers/paper_list_l2120_https_arxiv_org_abs_2603_17684/figures/003_Table_1.jpg]]
*Table 1: Accuracy and training efficiency of different models with and without AFSS on MS COCO 2017 and PASCAL VOC 2007 datasets, evaluated on two RTX 4090 GPUs (24 GB each). All subsequent results are obtained under the same hardware configuration*

![[assets/figures/papers/paper_list_l2120_https_arxiv_org_abs_2603_17684/figures/004_Table_2.jpg]]
*Table 2: Accuracy and training efficiency of different models with and without AFSS on DOTA-v1.0 and DIOR-R datasets*

最关键的结果来自 YOLO11s 在 MS COCO 2017 上的表现（**Table 3**）：AFSS 将训练时间从 43.9h 显著缩短，实现 1.54× 加速，同时 AP 从 47.0 提升至 47.2。这一“加速且提点”的现象表明，AFSS 并非简单地丢弃数据，而是通过动态调度将计算资源集中到更有价值的学习信号上。

![[assets/figures/papers/paper_list_l2120_https_arxiv_org_abs_2603_17684/figures/005_Table_3.jpg]]
*Table 3: Comparison of different training methods*

### 与相关方法的对比

**Table 3** 将 AFSS 与多种训练加速/数据选择方法进行了全面对比。与 **Self-Paced Learning**（Kumar et al., NIPS 2010）的课程学习策略、**Data Diet**（Paul et al., NIPS 2021）的静态数据剪枝、**Fetch and Forge**（Qi et al., NIPS 2024）的数据集蒸馏以及 **SuperLoss** 的损失加权方法相比，AFSS 在 YOLO11s 上取得了最高的训练加速比（1.54×）和最高的 AP（47.2）。这表明基于图像级学习充分性的动态调度策略，在目标检测场景下优于基于损失值或静态统计的数据选择方法。

### 消融实验

消融实验系统验证了 AFSS 四个核心组件的必要性和超参数选择的合理性。

**组件消融（Table 4）**：以 YOLOv11s 为基线，完整 AFSS 取得 47.2 AP 和 1.54× 加速。去除学习充分性度量（LSM）后，模型退化为无差别的随机采样，AP 显著下降；去除连续回顾（CR）后，简单样本的遗忘导致精度损失；去除短期覆盖（STC）后，中等样本因参与过疏产生性能退化；去除状态更新（SU）后，样本难度标签无法随模型能力进化，加速比与精度均受影响。四个组件协同作用，缺一不可。

**度量形式消融（Table 5a）**：采用 min(Precision, Recall) 作为学习充分性度量，在几乎相同的加速比下获得了比基于 Loss、Gradient 或 F1-score 的度量方式更高的 AP。这验证了聚焦检测器较弱维度（精确率与召回率中的最小值）的设计直觉。

**超参数消融（Table 5b–d）**：连续回顾间隔设为 10 epoch 时，AFSS 在精度和训练时间之间取得最佳平衡；短期覆盖间隔设为 3 epoch 能稳定地防止中等样本遗忘；状态更新间隔设为每 5 epoch 一次，既能及时反映模型学习进展，又不会引入过多额外评估开销。

### 训练动态可视化

**Figure 3** 展示了 YOLO11s 训练过程中被 AFSS 分类为简单、中等和困难的图像数量变化趋势。随着训练推进，简单样本数量持续增加，困难样本数量逐渐减少，直观反映了模型学习能力的提升和 AFSS 状态更新机制的有效性。

**Figure 4** 通过一个困难样本的可视化例子，对比了 YOLO11s 与 YOLO11s+AFSS 在第 100、300、600 个训练 epoch 的检测结果。标准训练在早期对困难样本检测效果不佳，而 AFSS 通过将困难图像全量参与训练，使模型在相同 epoch 下对该样本的检测质量明显更优，直观体现了 AFSS 对难样本的持续学习能力。

### 补充图表

![[assets/figures/papers/paper_list_l2120_https_arxiv_org_abs_2603_17684/figures/001_Figure_1.jpg]]
*Figure 1: Comparison of YOLO11s with and without AFSS in terms of the training images used and the corresponding training efficiency and accuracy on MS COCO 2017. (a) Training data used per epoch: AFSS adaptively selects the images used for training, progressively reducing the number of images utilized over time, whereas the vanilla YOLO11s employs the full training set in every epoch; (b) Training efficiency and accuracy: AFSS accelerates YOLO11s training by 1.54 × while improving detection accuracy*

![[assets/figures/papers/paper_list_l2120_https_arxiv_org_abs_2603_17684/figures/006_Table_4.jpg]]
*Table 4: Ablation of AFSS core components using YOLOv11s as the baseline. LSM: Learning Sufficiency Metric; CR: Continuous Review; STC: Short-Term Coverage; SU: State Update*

![[assets/figures/papers/paper_list_l2120_https_arxiv_org_abs_2603_17684/figures/007_Table_5.jpg]]
*Table 5: Ablation studies on learning sufficiency metric, continuous review interval, short-term coverage interval, and state update interval*

![[assets/figures/papers/paper_list_l2120_https_arxiv_org_abs_2603_17684/figures/009_Figure_4.jpg]]
*Figure 4: An example illustrating the learning performance of YOLO11s and YOLO11s+AFSS at the 100th, 300th, and 600th training epochs on the hard image*

![[assets/figures/papers/paper_list_l2120_https_arxiv_org_abs_2603_17684/figures/008_Figure_3.jpg]]
*Figure 3: Changes in the number of samples at easy, moderate, and hard levels during the training of YOLO11s with AFSS*

## 方法谱系与知识库定位

### 核心思想定位

AFSS 本质上是一种**动态数据调度策略**，而非检测器架构的改进。其核心思想是将训练数据视为具有动态学习价值的资源：通过定义图像级的“学习充分性”（Learning Sufficiency），在每个训练 epoch 自适应地决定每张图像是否参与前向/反向传播，从而将计算资源从已充分学习的简单样本转移到仍需学习的困难样本。这一思路与传统的目标检测训练范式形成鲜明对比——后者默认每个 epoch 遍历全部训练集，隐含假设所有图像在每个训练阶段具有同等的学习价值。

从知识库定位来看，AFSS 处于**高效训练（Efficient Training）**与**数据选择（Data Selection）**的交叉地带，但其独特之处在于引入了“反遗忘”机制，使方法兼具**持续学习（Continual Learning）**中的灾难性遗忘缓解思想。这使得 AFSS 区别于单纯的静态数据剪枝或课程学习方法。

### 与基线方法的关系与对比

#### 1. 标准 YOLO 训练（Vanilla Training）

标准 YOLO 训练流程是 AFSS 的直接对比基线。在每个 epoch 中，标准流程使用全部训练图像进行前向和反向传播，所有图像被等价处理。这种“全覆盖”范式导致了大量冗余计算——已充分学习的简单图像被反复处理，而模型能力提升后仍未学好的困难图像得不到额外的计算资源倾斜。AFSS 的改进在于打破了这种均匀遍历，通过学习充分性度量实现了差异化的图像参与频次。

#### 2. Self-Paced Learning（自步学习）

**Self-Paced Learning**（Kumar et al., NIPS 2010）是课程学习（Curriculum Learning）的经典代表，其核心思想是从简单样本开始训练，逐步引入困难样本。AFSS 与自步学习有表面相似性——都涉及对样本难度的区分——但存在根本差异：

- **难度定义不同**：自步学习通常基于损失值定义难度，损失大即为困难；AFSS 则使用 `min(Precision, Recall)` 作为学习充分性度量，聚焦检测器中较弱的预测维度，直接反映图像是否被可靠检测与定位。
- **调度机制不同**：自步学习在训练初期排除困难样本，后期逐步引入；AFSS 则始终保留困难样本的全量参与（Hard 图像 100% 使用），同时对简单和中等图像施加差异化的稀疏回顾策略，而非简单的时间延迟。
- **遗忘处理不同**：自步学习未显式处理已学知识的遗忘问题；AFSS 则通过连续回顾（CR）和短期覆盖（STC）机制主动防止遗忘。

实验对比（Table 3）显示，AFSS 在 YOLO11s 上取得 47.2 AP 和 1.54× 加速，而自步学习方法的加速比和精度均不及 AFSS，验证了仅靠课程调度不足以在检测任务中实现高效训练。

#### 3. Data Diet（数据节食）

**Data Diet**（Paul et al., NIPS 2021）是一种静态数据选择方法，通过早期训练阶段的损失或梯度统计来识别并剪枝“不重要”的训练样本，后续训练仅使用保留的子集。AFSS 与之的关键区别在于：

- **静态 vs 动态**：Data Diet 在训练早期一次性决定数据子集，后续不再调整；AFSS 则每 5 个 epoch 重新评估所有图像的学习充分性，使数据参与模式随模型能力协同进化。
- **遗忘风险**：静态剪枝可能导致被移除的样本所承载的知识逐渐遗忘；AFSS 的连续回顾机制确保即使是简单图像，也会以 2% 的极低比例持续参与训练，且强制回顾长期未见的样本。
- **适用性**：Data Diet 的剪枝决策依赖于早期模型的梯度信号，当早期模型尚未收敛时，剪枝决策可能不可靠；AFSS 的 min(Precision, Recall) 度量在训练全程均可稳定计算。

#### 4. Fetch and Forge（数据集蒸馏）

**Fetch and Forge**（Qi et al., NIPS 2024）通过数据集蒸馏技术合成少量代表性图像来替代原始训练集，属于训练加速的极端方案。AFSS 与之相比：

- AFSS 始终使用原始真实图像，不引入合成样本的分布偏差风险。
- 数据集蒸馏本身需要额外的计算开销来生成合成图像；AFSS 的额外开销仅来自定期的学习充分性评估（每 5 epoch 一次），开销极低。
- AFSS 在 YOLO11s 上的 1.54× 加速是在零精度损失（甚至提升 0.2 AP）的前提下实现的；数据集蒸馏方法通常面临精度-压缩率的权衡。

#### 5. SuperLoss

SuperLoss 是一种基于损失值的训练样本加权/选择方法，通过对高损失样本降权来抑制噪声样本的影响。AFSS 与之的差异在于：

- SuperLoss 关注的是样本的“噪声程度”或“有用性”，倾向于降低异常高损失样本的权重；AFSS 则将高学习充分性（即已学好）的样本视为冗余，降低其参与频次，而非基于损失大小做判断。
- 消融实验（Table 5a）直接对比了基于 Loss、Gradient、F1-score 和 min(Precision, Recall) 的度量方式，证实 min(Precision, Recall) 在几乎相同的加速比下获得了更高的 AP，说明检测任务中精度-召回率的联合度量比单一损失信号更适合评估学习充分性。

### 方法适用边界

基于论文提供的实验证据，AFSS 的适用边界可归纳如下：

| 维度 | 已验证范围 | 未验证/需注意 |
|------|-----------|--------------|
| **检测器架构** | YOLOv8, YOLOv10, YOLO11, YOLO12（Anchor-based 和 Anchor-free） | 非 YOLO 系列检测器（如 DETR、Faster R-CNN）未测试 |
| **任务类型** | 通用目标检测（COCO, VOC）、旋转目标检测（DOTA, DIOR-R） | 实例分割、关键点检测、3D 检测等未测试 |
| **数据集规模** | COCO（~118K）、VOC（~16K）、DOTA（~15K）、DIOR-R（~23K） | 超大规模数据集（如 Objects365）或极小数据集未测试 |
| **训练周期** | 标准 YOLO 训练周期（数百 epoch） | 极短训练（如 few-shot fine-tuning）场景未测试 |
| **硬件配置** | 双 RTX 4090 24GB | 单 GPU 或不同 GPU 架构下的加速比可能变化 |

**需要注意的潜在局限**（论文未明确讨论，需手动验证）：

1. **类别不平衡敏感性**：AFSS 的学习充分性度量是图像级的，未显式建模类别级的学习状态。在类别极度不平衡的数据集上，少数类样本可能因图像级指标不敏感而被错误分类为“简单”，导致对这些类别的学习不充分。论文未提供每类 AP 的分析。

2. **早期训练的冷启动问题**：训练初期，检测器的精度和召回率都很低，大量图像会被分类为“困难”（min(P, R) < 0.55），此时 AFSS 退化为接近全量训练，加速效果有限。随着训练推进，加速效果逐渐显现（Figure 1(a) 体现了这一趋势）。这意味着 AFSS 的加速收益集中在训练中后期。

3. **状态更新频率的通用性**：消融实验确定每 5 epoch 更新一次状态为最优，但这一频率可能依赖于具体的数据集规模和模型收敛速度。在其他配置下可能需要重新调整。

### 开放问题

1. **跨架构泛化性**：AFSS 在 YOLO 系列上验证充分，但其核心机制（min(Precision, Recall) 度量 + 三级调度）是否适用于基于 Transformer 的检测器（如 DETR、Deformable DETR）或两阶段检测器（如 Faster R-CNN）？这些架构的精度-召回率动态可能与 YOLO 不同。

2. **与数据增强的交互**：YOLO 训练中通常使用 Mosaic、MixUp 等强数据增强。AFSS 的学习充分性评估是在增强后的图像上进行的，增强策略的随机性可能影响状态评估的稳定性。论文未分析这种交互。

3. **更细粒度的调度**：当前 AFSS 在图像级做决策，是否可以将调度粒度细化到实例级（每个 GT 框的学习充分性）或类别级，以进一步提升效率？这需要额外的方法设计和实验验证。

4. **理论收敛性保证**：AFSS 改变了训练数据的采样分布，这种非均匀采样的理论收敛性质尚未被分析。是否存在某些条件下 AFSS 可能导致次优收敛？这是一个开放的理论问题。

## 原文 PDF

![[paperPDFs/CVPR_2026/Does_YOLO_Really_Need_to_See_Every_Training_Image_in_Every_Epoch.pdf]]
