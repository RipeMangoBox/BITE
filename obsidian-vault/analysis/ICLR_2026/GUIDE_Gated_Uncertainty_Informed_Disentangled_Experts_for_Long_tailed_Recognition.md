---
title: "GUIDE: Gated Uncertainty-Informed Disentangled Experts for Long-tailed Recognition"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/GUIDE_Gated_Uncertainty_Informed_Disentangled_Experts_for_Long_tailed_Recognition.pdf
project_link: null
code_link: null
openreview_forum_id: jY21fwcrjr
aliases:
- GUIDE
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/classification_and_understanding
core_operator: "通过层次化解耦强制专家特征与预测多样性、对不确定性进行认知/偶然分解并以此驱动自适应门控、将元策略与主任务优化分离为快慢双时间尺度更新。"
primary_logic: "只有在表示层面构建真正多样的专家委员会，才能将专家分歧转化为可靠的不确定性分解信号，进而支撑稳定的元策略优化，最终形成自我组织的鲁棒长尾学习系统。"
claims:
- "竞争性专门化目标通过特征去相关和最大化预测JSD强制多样性，防止同质化崩溃。"
- "分解预测不确定性为认知和偶然分量，驱动动态专家细化模块进行针对性资源分配。"
- "采用双时间尺度更新（θ 快速，ϕ 缓慢）解耦主任务和元策略优化，确保策略稳定收敛。"
- "层次化解耦的各层依次引入可累积提升性能，最终完整 GUIDE 在 CIFAR-100-LT (IR=100) 达到 56.4%，远超基线。"
---

# GUIDE: Gated Uncertainty-Informed Disentangled Experts for Long-tailed Recognition

> [!tip] 核心洞察
> 只有在表示层面构建真正多样的专家委员会，才能将专家分歧转化为可靠的不确定性分解信号，进而支撑稳定的元策略优化，最终形成自我组织的鲁棒长尾学习系统。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | GUIDE：面向长尾识别的门控不确定性解耦专家框架 |
| 英文题名 | GUIDE: Gated Uncertainty-Informed Disentangled Experts for Long-tailed Recognition |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=jY21fwcrjr) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/classification_and_understanding |
| Method | GUIDE |
| Dataset | CIFAR-100-LT (IR=100), ImageNet-LT, iNaturalist 2018 |

> [!tip] 效果简介
> - CIFAR-100-LT (IR=100) 上，Top-1 Accuracy 为 56.4，对比 54.9 (LOS)，变化 +1.5。
> - ImageNet-LT 上，Top-1 Accuracy 为 62.5，对比 60.8 (PRL)，变化 +1.7。
> - iNaturalist 2018 上，Top-1 Accuracy 为 76.1，对比 75.1 (PRL)，变化 +1.0。

## 概要

长尾识别（Long‑tailed Recognition, LTR）的核心挑战在于模型在少样本类别上的性能崩溃。现有主流方法——尤其是多专家架构——虽然通过多个专家分支试图弥补尾部类别的学习不足，却普遍陷入一个深层的结构性陷阱：**表示‑决策纠缠导致的专家同质化崩溃**。当多个专家共享高度相似的表示空间时，预测分歧退化为噪声，系统无法真正形成“专家委员会”应有的功能分工。在此基础上，“原因‑症状纠缠”（将数据固有歧义与模型知识不足混为一谈）和“元学习‑主任务优化纠缠”（自适应策略与主网络同步更新导致训练震荡）进一步破坏了自适应机制的可靠性与稳定性。

GUIDE（Gated Uncertainty‑Informed Disentangled Experts）针对上述瓶颈，提出了一个**层次化解耦框架**，其核心洞察可概括为：**只有在表示层面构建真正多样的专家委员会，才能将专家分歧转化为可靠的不确定性分解信号，进而支撑稳定的元策略优化，最终形成自我组织的鲁棒长尾学习系统**。该框架通过三个递进的解耦层次实现这一目标：

1. **表示‑决策解耦（Level ❶）**：通过特征余弦去相关损失与最大化预测分布 Jensen‑Shannon 散度（JSD），主动强制专家在特征子空间和预测行为上形成竞争性专门化，从根本上防止同质化崩溃。
2. **不确定性分解与自适应资源分配（Level ❷）**：将专家间的预测分歧分解为**认知不确定性**（模型知识不足）和**偶然不确定性**（数据固有歧义），并以此驱动一个可学习的类级门控控制器，对动态专家细化模块（DERM）进行针对性资源分配——对高认知不确定性的少样本类别增强细化，对高偶然不确定性的噪声类别抑制过拟合。
3. **优化时间尺度解耦（Level ❸）**：采用双时间尺度更新规则，主任务参数 $\theta$ 每步以较大学习率快速更新，元策略参数 $\phi$ 每 epoch 以极小学习率缓慢更新，将元策略优化与主任务学习分离，确保自适应策略的稳定收敛。

在三个主流长尾基准上的实验验证了这一设计的有效性：GUIDE 在 CIFAR‑100‑LT（IR=100）达到 56.4%（+1.5% vs. LOS），在 ImageNet‑LT 达到 62.5%（+1.7% vs. PRL），在 iNaturalist 2018 达到 76.1%（+1.0% vs. PRL），均刷新了当前最优结果。消融实验进一步表明，**三个解耦层次各自带来可累积的性能提升**，且组合特征去相关与预测分歧损失相比单一多样性损失带来 +4.6% 的显著增益，基于分解不确定性的门控策略显著优于仅用总不确定性的不可知门控（56.4% vs. 54.9%），验证了各层次设计的必要性。



### 长尾识别的核心挑战

现实世界的视觉数据普遍呈现长尾分布——少数头部类别占据绝大多数样本，而大量尾部类别仅有极少样本。这种极端不均衡导致标准深度模型在训练时被头部类别主导，尾部类别因监督信号稀疏而难以充分学习，最终在少样本类别上表现急剧退化。因此，长尾识别的本质挑战在于：如何在头部类别充分拟合与尾部类别充分泛化之间取得有效平衡。

### 多专家架构的“表示同质化崩溃”困境

为应对这一挑战，多专家方法（如 RIDE、SADE）通过构建多个分类器分支来增强尾部类别的学习能力。然而，现有方法普遍陷入一个被忽视的深层瓶颈：**表示‑决策纠缠导致的专家同质化崩溃**。由于专家共享高度重叠的特征表示，且缺乏显式的多样性约束，各专家的预测分布趋于一致，最终退化为单一模型的简单复制。这直接削弱了多专家架构的核心优势——委员会多样性。

在此基础上，进一步衍生出两种次生纠缠：

- **原因‑症状纠缠**：现有方法将高训练损失作为“困难样本”的一刀切信号，无法区分困难来源于模型知识不足（认知不确定性）还是数据固有歧义（偶然不确定性），导致资源分配策略盲目且低效。
- **元学习‑主任务优化纠缠**：自适应策略（如门控控制器）与主任务网络使用相同或相近的学习率同步更新，使得元策略在噪声中震荡，难以稳定收敛到最优资源分配方案。

这些纠缠共同构成了传统多专家系统的结构性缺陷：**表示同质化使专家分歧无法可靠提取，进而使不确定性分解失去信号基础，最终使自适应策略的元优化失去稳定支撑**。

### 本文动机与核心思路

针对上述瓶颈，本文提出 GUIDE 框架，其动机源于一个核心洞察：**只有在表示层面构建真正多样的专家委员会，才能将专家分歧转化为可靠的不确定性分解信号，进而支撑稳定的元策略优化，最终形成自我组织的鲁棒长尾学习系统**。

GUIDE 通过三个层次化解耦来实现这一目标：

1. **表示‑决策解耦（Level ❶）**：引入竞争性专门化目标，通过特征余弦去相关损失和最大化专家预测分布 Jensen-Shannon 散度，强制专家在特征子空间和预测行为上保持多样性，从根本上防止同质化崩溃。
2. **原因‑症状解耦（Level ❷）**：将专家委员会的预测分歧分解为认知不确定性（模型知识不足）和偶然不确定性（数据固有歧义），并以此驱动动态专家细化模块进行针对性资源分配——对高认知不确定性的尾部类别加强细化，对高偶然不确定性的噪声类别抑制过拟合。
3. **优化时间尺度解耦（Level ❸）**：采用双时间尺度更新规则——主任务参数 θ 每步以较大学习率快速更新，元策略参数 ϕ 每 epoch 在验证集上以极小学习率缓慢更新，确保策略在稳定信号下收敛。

通过这一层次化解耦设计，GUIDE 将多专家系统从被动应对长尾分布的模式，转变为主动诊断并自我组织资源分配的鲁棒学习框架。



## 核心方法与创新机理

GUIDE 的核心创新在于对多专家长尾学习系统进行了**层次化解耦**，从根本上解决了传统多专家架构中因表示‑决策纠缠导致的专家同质化崩溃问题。该框架通过三个递进层次的解耦设计，将专家多样性构建、不确定性自适应策略和元学习优化分离为相互独立又协同增强的子系统。

### 创新一：竞争性专门化目标强制专家多样性

传统多专家方法（如 RIDE、SADE）依赖间接的决策级调整来维持专家差异，但在共享骨干网络下，专家特征表示仍趋于同质化。GUIDE 在表示层面引入了显式的竞争性专门化目标，从两个维度强制专家分化：

- **特征去相关**：通过最小化专家间特征向量的余弦相似度 $\mathcal{L}_{\mathrm{decouple}}$，迫使不同专家学习互补的特征子空间。
- **预测分歧最大化**：显式最大化专家预测分布的 Jensen-Shannon 散度（JSD），确保专家在决策层面产生实质性分歧。

消融实验（Table 5 左）证实，单独使用任一损失提升有限，而组合特征去相关和预测 JSD 损失相比基线带来 **+4.6%** 的显著增益。t‑SNE 可视化（Figure 4）和 CKA/Q‑Statistic 定量分析（Table 12）进一步验证，GUIDE 的专家委员会在表示层面实现了真正的多样性，而非表面的参数扰动。

### 创新二：认知/偶然不确定性分解驱动的自适应门控

现有方法对困难样本采用基于高训练损失的一刀切反应，无法区分样本困难的根源——是模型知识不足（认知不确定性）还是数据固有歧义（偶然不确定性）。GUIDE 将专家间的预测分歧分解为两类不确定性信号：

- **偶然不确定性** $\mathrm{Ale}_T(x)$：专家预测分布的平均熵，反映数据本身的不可约歧义。
- **认知不确定性** $\mathrm{Epi}_T(x)$：平均预测的熵减去偶然不确定性，衡量模型对该样本的知识缺口。

基于这一分解，动态专家细化模块（DERM）通过类级门控控制器学习不确定性到细化强度的映射。门控函数被设计为对认知不确定性单调递增、对偶然不确定性单调递减，从而对真正需要模型能力提升的尾部类别分配更多计算资源，同时避免对噪声样本的过拟合。Table 5（右）显示，基于分解不确定性的 GUIDE 门控策略（56.4%）显著优于仅用总不确定性的不可知门控（54.9%），验证了分解的必要性。

### 创新三：双时间尺度优化解耦主任务与元策略学习

传统方法中，主任务学习和自适应策略优化使用相同或相近的学习率同步更新，导致元策略在未充分收敛的表示上进行优化，引发训练不稳定和次优策略。GUIDE 引入双时间尺度更新规则：

- **快速变量 $\theta$**（骨干网络、DERM 路径参数）：以较大学习率每步更新，快速学习有效表示。
- **慢速变量 $\phi$**（门控控制器参数）：以极小学习率每个 epoch 在验证集上更新，在稳定表示基础上缓慢调整自适应策略。

该设计满足双时间尺度随机逼近的理论条件，确保元策略在准静态表示下安全收敛。收敛曲线（Figure 6）表明，GUIDE 不仅在最终精度上领先，训练过程也更为稳定。

### 创新四：层次化协同的累积增益

三个解耦层次并非孤立设计，而是形成递进依赖关系：只有 Level ❶ 构建了真正多样的专家委员会，Level ❷ 才能将专家分歧转化为可靠的不确定性分解信号；只有 Level ❷ 提供了稳定的自适应策略，Level ❸ 的元学习才能在无灾难性干扰的条件下收敛。消融实验（Table 4）证实，各层依次引入可累积提升性能，完整 GUIDE 在 CIFAR‑100‑LT（IR=100）达到 **56.4%**，远超基线方法。



![[assets/figures/papers/iclr26_0010_jY21fwcrjr_GUIDE_Gated_Uncertainty-Informed_Disentangled_Ex/figures/002_Figure_2.jpg]]
*Figure 2: The Hierarchical Disentanglement architecture of GUIDE. An input is processed via a shared backbone and a committee of experts. Level ❶ enforces diversity by penalizing feature and decision overlap. This enables Level ❷, where expert disagreement is decomposed into epistemic (model) and aleatoric (data) uncertainty. These signals drive a gate controller to modulate the Dynamic Expert Refinement Module (DERM). Finally, Level ❸ decouples optimization into a fast inner loop for task parameters (θ) and a slow outer loop for the meta-policy (ϕ), which closes the meta-learning loop by updating the gate controller*

GUIDE 的核心设计理念是**层次化解耦**——将传统多专家系统中纠缠在一起的三个关键维度（表示与决策、原因与症状、元策略与主任务优化）逐一分离，从而构建一个自我组织的鲁棒长尾学习系统。整个框架由共享骨干网络、专家委员会、动态专家细化模块和元策略门控控制器四个核心模块构成，通过三层递进的解耦机制协同工作。

### 数据流与模块关系

如 Figure 2 所示，输入样本 $x$ 首先经过一个**共享骨干网络**提取基础视觉特征 $F_{\text{found}}(x)$。该特征随后被送入一个包含 $E=3$ 个并行分类分支的**专家委员会**，每个专家独立产生预测 logit $z_e(x)$ 和经过 logit 调整后的预测分布 $p_{e,T}(\cdot|x)$。

三个层次化解耦机制沿数据流依次施加：

- **Level ❶（竞争性专门化）**：在特征层面通过余弦去相关损失 $\mathcal{L}_{\text{decouple}}$ 强制专家学习互不重叠的表示子空间，在决策层面通过最大化 Jensen-Shannon 散度（JSD）迫使专家产生分歧预测。这一层从源头防止专家同质化崩溃，为后续不确定性分解提供必要的多样性基础。

- **Level ❷（不确定性引导自适应）**：基于专家间的预测分歧，将总预测不确定性分解为**认知不确定性** $\text{Epi}_T(x)$（反映模型知识不足）和**偶然不确定性** $\text{Ale}_T(x)$（反映数据固有歧义）。这些分解后的信号驱动**元策略门控控制器**（参数 $\phi$）生成类级门控强度 $g_{e,c}$，进而控制**动态专家细化模块（DERM）**中的自适应残差混合：
  $$\mathbf{f}_e(x; c) = F_{\text{found}}(x) + g_{e,c} \cdot (F_{\text{refine},e}(F_{\text{found}}(x)) - F_{\text{found}}(x))$$
  该残差设计使得基础路径始终保留原始特征，细化分支仅在门控信号引导下进行针对性增强，从而对高认知不确定性的困难样本（通常来自少样本类别）分配更多细化资源，同时对高偶然不确定性的噪声样本保持克制。

- **Level ❸（双时间尺度优化）**：主网络参数 $\theta$（包括骨干网络和 DERM 通路）每步以较大学习率 $\eta_\theta$ 快速更新，负责学习有效的表示和分类能力；元策略参数 $\phi$（门控控制器）每个 epoch 在验证集上以极小学习率 $\eta_\phi \ll \eta_\theta$ 缓慢更新，确保自适应策略稳定收敛而不会干扰主任务学习。

### 推理流程

GUIDE 采用两步推理策略：首先执行单次前向传播获取初步预测，据此确定候选类别；随后仅对候选类别进行精炼推理，利用 DERM 的类级自适应残差混合产生最终预测。这一设计在控制计算开销的同时，显著提升了少样本类别的识别精度（Table 6 显示两步推理在 CIFAR-100-LT 上以约 1.8 倍延迟代价换取约 2% 的少样本准确率提升）。

### 框架的新颖性定位

需要指出的是，GUIDE 的核心新颖性不在于单个组件（如特征去相关、不确定性分解或元学习本身），而在于**层次化解耦这一顶层设计原则**——它将已有技术按因果逻辑重新组织，使多样性强制、不确定性诊断和稳定优化三者形成闭环，从而实现各层依次累积的性能增益（Table 4 消融实验证实，逐层引入三个解耦机制后性能从基线 45.8% 持续提升至完整 GUIDE 的 56.4%）。



GUIDE 的核心创新在于**层次化解耦**——通过三个递进层级，分别解决多专家架构中的表示‑决策纠缠、原因‑症状纠缠、以及元学习‑主任务优化纠缠。以下逐一展开各层级的关键模块与公式。

---

### 第一层：竞争性专门化（Competitive Specialization）

传统多专家系统因共享表示而陷入**同质化崩溃**：所有专家学习相似的决策边界，无法形成有效互补。GUIDE 通过两个显式正则项强制专家间在特征与预测两个层面产生分歧。

**主协作损失**首先保证专家委员会的基础分类能力。对于输入 $x$，专家 $e$ 的 Logit 调整后得分 $\tilde{z}_e(x)_c$ 经聚合后计算交叉熵：

$$
\mathcal{L}_{\mathrm{main}} = -\log \frac{\exp(\sum_{e=1}^{E} \tilde{z}_e(x)_y)}{\sum_{c=1}^{C} \exp(\sum_{e=1}^{E} \tilde{z}_e(x)_c)} \tag{1}
$$

其中 Logit 调整 $\tilde{z}_e(x)_c = z_e(x)_c + \tau_e \log \pi_{\mathrm{train}}(c)$（式 11），利用训练类先验 $\pi_{\mathrm{train}}(c)$ 缓解长尾偏差。

**特征解耦损失**直接作用于表示空间，最小化任意两专家特征向量间的余弦相似度：

$$
\mathcal{L}_{\mathrm{decouple}} = \frac{2}{E(E-1)} \sum_{1 \leq i < j \leq E} \frac{f_i(x)^\top f_j(x)}{\|f_i(x)\|_2 \cdot \|f_j(x)\|_2 + \varepsilon} \tag{2}
$$

其中 $f_e(x)$ 为专家 $e$ 提取的特征向量，$\varepsilon$ 防止除零。

**预测分歧损失**最大化专家预测分布的 Jensen‑Shannon 散度（JSD），强制决策层面差异化：

$$
\mathrm{JSD}\big(\{p_{e,T}(\cdot|x)\}\big) = H\!\left(\frac{1}{E}\sum_{e=1}^{E} p_{e,T}(\cdot|x)\right) - \frac{1}{E}\sum_{e=1}^{E} H\big(p_{e,T}(\cdot|x)\big)
$$

其中 $p_{e,T}(\cdot|x)$ 为温度 $T$ 缩放后的专家预测分布，$H(\cdot)$ 为熵。JSD 值越大，专家间预测分歧越显著。

第一层总损失将协作与竞争统一：

$$
\mathcal{L}_{\mathrm{total}}^{(1)} = \mathcal{L}_{\mathrm{main}} + \lambda_{\mathrm{dec}} \mathcal{L}_{\mathrm{decouple}} - \lambda_{\mathrm{div}} \mathrm{JSD}\big(\{p_{e,T}(\cdot|x)\}\big) \tag{3}
$$

**因果机制**：$\mathcal{L}_{\mathrm{decouple}}$ 迫使专家在特征子空间上正交化，而 JSD 最大化则确保这些差异化表示转化为可区分的预测行为。消融实验（Table 5 左）证实：单独使用任一损失提升有限，二者协同带来 $+4.6\%$ 的显著增益，且 t‑SNE 可视化（Figure 4）显示 GUIDE 专家特征空间明显分离，基线方法则严重重叠。

---

### 第二层：不确定性分解与动态专家细化（DERM）

第一层产生的专家分歧为第二层提供了**可靠的不确定性信号**。GUIDE 将预测不确定性分解为两个正交分量：

**偶然不确定性**（Aleatoric Uncertainty）衡量数据固有歧义，定义为各专家预测熵的均值：

$$
\mathrm{Ale}_T(x) = \frac{1}{E} \sum_{e=1}^{E} H\big(p_{e,T}(\cdot|x)\big) \tag{4}
$$

**认知不确定性**（Epistemic Uncertainty）反映模型知识不足，由平均预测的熵减去偶然不确定性得到：

$$
\mathrm{Epi}_T(x) = H\big(\bar{p}_T(\cdot|x)\big) - \mathrm{Ale}_T(x) \tag{5}
$$

其中 $\bar{p}_T(\cdot|x) = \frac{1}{E}\sum_{e=1}^{E} p_{e,T}(\cdot|x)$ 为专家平均预测。当专家对某样本高度一致时，认知不确定性低；分歧大时则高。

**动态专家细化模块（DERM）** 基于上述分解信号，通过自适应残差混合为每个类分配差异化的计算资源：

$$
\mathbf{f}_e(x; c) = F_{\mathrm{found}}(x) + g_{e,c} \cdot \big(F_{\mathrm{refine},e}(F_{\mathrm{found}}(x)) - F_{\mathrm{found}}(x)\big) \tag{6}
$$

其中 $F_{\mathrm{found}}$ 为基础特征提取路径，$F_{\mathrm{refine},e}$ 为专家 $e$ 的细化分支，$g_{e,c} \in [g_{\mathrm{min}}, g_{\mathrm{max}}]$ 为类级门控强度。当 $g_{e,c}=0$ 时退化为基础路径，$g_{e,c}=1$ 时完全启用细化。

**门控控制器**将类级不确定性 EMA 映射为门控值：

$$
\tilde{g}_{e,c} = \alpha_e \cdot \overline{\mathrm{Epi}}_{T,c}^{(t)} - \beta_e \cdot \overline{\mathrm{Ale}}_{T,c}^{(t)} + \gamma_e \tag{7}
$$

$$
g_{e,c} = \sigma(\tilde{g}_{e,c}) \cdot (g_{\mathrm{max}} - g_{\mathrm{min}}) + g_{\mathrm{min}} \tag{8}
$$

其中 $\overline{\mathrm{Epi}}_{T,c}^{(t)}$ 和 $\overline{\mathrm{Ale}}_{T,c}^{(t)}$ 分别为类 $c$ 在第 $t$ 个 epoch 的认知和偶然不确定性指数移动平均，$\{\alpha_e, \beta_e, \gamma_e\}$ 为可学习参数（即慢变量 $\phi$），$\sigma(\cdot)$ 为 sigmoid 函数。

**单调性保证**：由式 (7)–(8) 可证，$g_{e,c}$ 对 $\overline{\mathrm{Epi}}_{T,c}^{(t)}$ 单调递增，对 $\overline{\mathrm{Ale}}_{T,c}^{(t)}$ 单调递减——这确保了门控策略的**可解释性**：数据稀缺类（高认知不确定性）获得更多细化资源，高噪声类（高偶然不确定性）则抑制细化以防过拟合噪声。Figure 5 在 ImageNet‑LT 上验证了这一预期行为。

---

### 第三层：双时间尺度优化

若主任务参数 $\theta$（骨干网络、DERM 路径）与元策略参数 $\phi$（门控控制器）以相同速率更新，将导致**优化纠缠**：策略尚未收敛就被主任务梯度干扰。GUIDE 采用双时间尺度更新解耦二者：

**快速更新**（每步，$\theta$）：

$$
\theta_{k+1} = \theta_k - \eta_\theta \nabla_\theta \mathcal{L}_{\mathrm{GUIDE}}(x_k, y_k; \theta_k, \phi_t) \tag{9}
$$

**慢速更新**（每 epoch，$\phi$，在验证集 $\mathcal{V}$ 上）：

$$
\phi_{t+1} = \phi_t - \eta_\phi \nabla_\phi \mathbb{E}_{(x_v,y_v)\in\mathcal{V}} [\mathcal{L}_{\min}(x_v, y_v; \theta_t, \phi_t)] \tag{10}
$$

其中 $\eta_\theta$ 采用大学习率调度（如初始 0.1 并衰减），$\eta_\phi$ 固定为极小值（如 $10^{-4}$），满足 $\eta_\phi \ll \eta_\theta$。

**收敛性理论支撑**：该方案构成有效的双时间尺度随机逼近（TTSA）算法——快变量 $\theta$ 在给定策略下快速收敛到有效表示，慢变量 $\phi$ 则基于稳定信号逐步优化策略，避免灾难性干扰。Figure 6 的收敛曲线显示 GUIDE 训练过程比对比方法更稳定。

---

### 模块间依赖关系

三层解耦形成**因果链**：第一层构建的多样化专家委员会（式 2–3）是第二层不确定性分解（式 4–5）的前提——若专家同质化，认知不确定性将退化为零，门控策略失效；第二层产生的稳定不确定性信号为第三层元策略优化（式 9–10）提供可靠的优化目标。Table 4 的逐层消融证实：每引入一层解耦，性能持续累积提升，完整 GUIDE 达到最优 56.4%。



## 实验与关键发现

### 主要结果

GUIDE 在三个主流长尾基准上均取得最优性能，验证了层次化解耦框架的有效性。如 Table 1 所示，在 CIFAR-100-LT (IR=100) 上，GUIDE 以 ResNet-32 为骨干网络达到 56.4% Top-1 准确率，超越此前最优方法 LOS（54.9%）1.5 个百分点。在更大规模的 ImageNet-LT 上，GUIDE 以 ResNet-50 取得 62.5%，优于 PRL（60.8%）1.7 个百分点。在类别数最多的 iNaturalist 2018 上，GUIDE 以 ResNet-50 达到 76.1%，同样超越 PRL（75.1%）1.0 个百分点。

![[assets/figures/papers/iclr26_0010_jY21fwcrjr_GUIDE_Gated_Uncertainty-Informed_Disentangled_Ex/figures/003_Table_1.jpg]]
*Table 1: Comparison of Top-1 accuracy (%) with state-of-the-art methods. Dashed underline indicates results reproduced by us using the official codebases of the respective authors. Best results are in bold, second best are underlined*

性能优势的核心来源可从 Table 2 的类别分组分析中定位：GUIDE 在少数样本（Few-shot）类别上实现了显著增益。在 CIFAR-100-LT IR=100 设置下，GUIDE 的 Few-shot 准确率达到 36.0%，远超 PRL（31.2%）和 LOS（33.2%），同时在中样本（Medium）类别上也保持了竞争力（51.8% vs. LOS 51.0%）。这表明层次化解耦——特别是竞争性专门化带来的专家多样性——有效缓解了长尾识别的核心瓶颈，即尾部类别的表示学习不足。

### 分布偏移鲁棒性

为评估模型在未知测试分布下的泛化能力，Table 3 报告了 CIFAR-100-LT (IR=100) 在多种测试类分布上的结果。测试分布包括前向长尾（Forward-LT，IR=50/25/10/5/2）、均匀分布（IR=1）和后向长尾（Backward-LT，IR=2/5/10/25/50）。GUIDE 在所有测试分布上均取得最高准确率，尤其在最具挑战性的 Backward-LT 设置下优势明显。值得注意的是，GUIDE 不依赖测试类先验进行后验调整，而部分对比方法（如 LADE）需要此类先验信息，这进一步凸显了 GUIDE 元策略学习到的自适应门控具有内在的分布鲁棒性。

### 消融实验

**层次解耦的逐级贡献。** Table 4 展示了三个解耦层次依次引入的效果。基线多专家模型（仅含 Level ❶ 的主协作损失）准确率为 45.8%。引入竞争性专门化目标（特征去相关 + 预测 JSD 最大化）后提升至 50.4%（+4.6%）。进一步加入 Level ❷ 的不确定性分解与 DERM 动态细化，准确率达到 52.8%（+2.4%）。最终引入 Level ❸ 的双时间尺度优化，完整 GUIDE 达到 56.4%（+3.6%）。每一层的增益可累积且显著，证实了层次化解耦设计的必要性。

![[assets/figures/papers/iclr26_0010_jY21fwcrjr_GUIDE_Gated_Uncertainty-Informed_Disentangled_Ex/figures/006_Table_4.jpg]]
*Table 4: Ablation study on the contribution of each disentanglement level. Performance consistently improves as each level of disentanglement is introduced, culminating in our final reported performance*

**多样性损失的协同效应。** Table 5（左）分析了 Level ❶ 中两个多样性损失各自的作用。单独使用特征去相关损失（$\mathcal{L}_{\mathrm{decouple}}$）或预测分歧损失（$\mathcal{L}_{\mathrm{div}}$）仅带来有限提升，而二者组合产生 +4.6% 的显著增益。这表明在表示层面和决策层面同时强制多样性是防止专家同质化崩溃的关键——仅靠单一层面的约束不足以构建真正多样的专家委员会。

![[assets/figures/papers/iclr26_0010_jY21fwcrjr_GUIDE_Gated_Uncertainty-Informed_Disentangled_Ex/figures/007_Table_5.jpg]]
*Table 5: Analysis of individual mechanisms. (Left) The synergistic effect of diversity losses in Level ❶. (Right) Comparison of different gating policies for the DERM in Level ❷*

**不确定性门控策略对比。** Table 5（右）比较了不同门控策略对 DERM 的影响。基于分解的 GUIDE 策略（56.4%）显著优于仅使用总不确定性的不可知门控（54.9%），验证了认知/偶然不确定性分解的必要性。去除 DERM 模块或采用静态门控均导致性能下降（见 Table 16），完整自适应残差混合方案达到最优。

**专家数量的影响。** Figure 3(b) 显示，专家数量从 1 增加到 3 大幅提升少样本类别性能，3 专家配置达到最佳整体精度 56.4%。当专家数增至 4 时收益递减，表明 3 个专家已能在多样性与计算开销之间取得良好平衡。

### 专家多样性的定量验证

为客观衡量专家多样性，Table 12 报告了 CKA（Centered Kernel Alignment）和 Q-Statistic 两个指标。在 CIFAR-100-LT (IR=100) 上，GUIDE 的专家间 CKA 相似度（越低越多样）和 Q-Statistic（越低越多样）均显著低于 RIDE、SADE、BalPoE 等强基线方法。Figure 4 的 t-SNE 可视化进一步提供了定性证据：基线多专家模型在尾部类别上特征高度重叠，而 GUIDE 的竞争性专门化目标成功学习到去相关的特征子空间。

![[assets/figures/papers/iclr26_0010_jY21fwcrjr_GUIDE_Gated_Uncertainty-Informed_Disentangled_Ex/figures/015_Figure_4.jpg]]
*Figure 4: t-SNE visualization of feature representations from three experts for selected tail classes on CIFAR-100-LT. (Left) A baseline multi-expert model exhibits significant feature overlap, indicating homogeneity collapse. (Right) Our GUIDE framework, with its competitive specialization objective, successfully learns decorrelated feature subspaces for each expert, confirming effective representation disentanglement*

### 门控策略的可解释性

Figure 5 可视化了 ImageNet-LT 上学习到的类级门控策略。每个点代表一个类别，横轴为认知不确定性（$\mathrm{Epi}$），纵轴为门控值（$g_c$）。结果显示，数据稀缺类别（高认知不确定性）被分配了更高的细化强度，而高偶然不确定性类别（数据固有歧义大）则获得较低的门控值。这与设计预期一致：门控策略正确地将计算资源导向模型知识不足的类别，而非简单地对噪声数据过拟合。

![[assets/figures/papers/iclr26_0010_jY21fwcrjr_GUIDE_Gated_Uncertainty-Informed_Disentangled_Ex/figures/018_Figure_5.jpg]]
*Figure 5: Visualization of the learned gating policy on ImageNet-LT, where each point represents a class. The policy correctly allocates high refinement strength (large gate value g _ { c } ) to data-scarce classes, which exhibit high epistemic uncertainty (model ignorance). Conversely, classes with high aleatoric uncertainty (data ambiguity) receive lower refinement, preventing the model from overfitting to noise. This confirms our policy operates as intended*

### 收敛性分析

Figure 6 展示了 CIFAR-100-LT (IR=100) 上的训练收敛曲线。与多个代表性方法相比，GUIDE 不仅最终性能更优，而且训练过程更加稳定。这归功于双时间尺度优化：快变量 $\theta$（主网络参数）每步更新以高效学习表示，慢变量 $\phi$（元策略控制器参数）每 epoch 以极小学习率更新，避免了元策略与主任务优化之间的灾难性干扰。

### 计算开销分析

Table 14 报告了成本-收益权衡。GUIDE 的参数量和推理延迟高于轻量级方法 RIDE 和 SADE，但换来了显著的尾部性能提升。两步推理策略（Table 6）在约 1.8 倍延迟代价下，将少样本类别准确率提升约 2-2.5%，这一可控开销在多数应用场景下是可接受的。

### 局限性与注意事项

尽管 GUIDE 在标准长尾基准上表现优异，以下局限性值得关注：

1. **两步推理的潜在风险**：DERM 的细化路径依赖初始预测结果，理论上存在错误级联的可能。尽管实证表明该策略具有较强的错误校正能力（Table 11），在极端错误预测场景下仍需进一步验证。
2. **细粒度场景的瓶颈**：在类别间高度相似或纹理混淆的细粒度数据集上，GUIDE 的性能受限于共享骨干网络对极细微特征的提取能力，层次化解耦无法完全弥补这一底层限制。
3. **损坏鲁棒性未验证**：尽管分布偏移实验（Table 3）展示了良好的先验偏移鲁棒性，GUIDE 尚未在基于损坏的基准（如 CIFAR-100-C）上进行系统性评估，其对图像损坏的泛化边界仍是开放问题。
4. **计算开销**：相比 RIDE、SADE 等轻量级多专家方法，GUIDE 的计算和内存开销更高，在资源严重受限的场景下需权衡取舍。



## 定位与知识库关联

### 长尾识别方法谱系中的定位

长尾识别的主流技术路线可归纳为三类：数据重采样、损失重加权、以及多专家架构。GUIDE 属于第三类，但其核心贡献不在于引入全新的独立模块，而在于通过**层次化解耦**原则重构多专家系统的内部组织方式，解决了此前方法中普遍存在的表示‑决策纠缠问题。

与经典多专家方法 RIDE 相比，GUIDE 的关键差异体现在三个维度：

- **专家多样性机制**：RIDE 等早期方法依赖间接的决策级调整（如不同 Logit 调整强度）来诱导专家分化，这种被动策略容易导致表示同质化崩溃。GUIDE 引入显式的竞争性专门化目标——特征余弦去相关损失（Eq. 2）与最大化专家预测分布 JSD（Eq. 3）——在表示和决策两个层面主动强制多样性。定量证据（Table 12）表明，GUIDE 的专家间 CKA 相似度和 Q‑Statistic 均显著低于 RIDE、SADE 等强基线，确认了更彻底的解耦效果。

- **困难样本自适应策略**：SADE 等方法基于高训练损失对困难样本做一刀切式反应，无法区分困难来源于模型无知（认知不确定性）还是数据固有歧义（偶然不确定性）。GUIDE 将专家分歧分解为认知/偶然两个不确定性分量（Eqs. 4‑5），并通过类级门控动态调整专家细化强度（Eqs. 7‑8），使高认知不确定性的少样本类别获得更多细化资源，而高偶然不确定性的噪声类别则被抑制。消融实验（Table 5 Right）显示，分解不确定性门控策略（56.4%）显著优于仅用总不确定性的不可知门控（54.9%）。

- **优化时间尺度**：BalPoE 等贝叶斯专家混合方法的主任务和自适应策略使用相近学习率同步更新，元策略优化易受主任务梯度噪声干扰。GUIDE 采用双时间尺度更新——主网络参数 θ 每步以较大学习率快更新（η_θ 起始 0.1 并衰减），元策略参数 ϕ 每 epoch 以极小固定学习率慢更新（η_ϕ = 1e‑4）——将二者解耦为快慢两个优化回路（Eqs. 9‑10）。附录中的 TTSA 框架分析证明了该方案满足双时间尺度随机逼近的收敛条件。

### 适用边界与已知局限

GUIDE 在标准长尾基准（CIFAR‑100‑LT、ImageNet‑LT、iNaturalist 2018）和分布偏移场景（Forward/Backward‑LT，Table 3）上均展现了 SOTA 性能，但其适用边界存在以下约束：

1. **两步推理的固有风险**：GUIDE 的推理策略依赖初始预测结果进行第二轮细化，存在初始错误被放大的理论风险。尽管实证表明该策略具有较强的错误校正能力（Table 11 显示细化步骤显著提升精度），但在极端类别混淆场景下仍需警惕。作者将此列为开放问题，建议未来探索基于 Top‑k 预测的自一致性机制。

2. **细粒度场景的表示瓶颈**：在类别间高度相似或纹理混淆的细粒度场景下，GUIDE 的性能受限于共享骨干网络对极细微特征的提取能力。层次化解耦主要作用于专家层面的特征组织，无法弥补底层表示的根本性不足。

3. **计算开销权衡**：相较于轻量级多专家方法（RIDE、SADE），GUIDE 的动态专家细化模块（DERM）和元策略控制器引入了额外的计算和内存开销。Table 14 的成本‑收益分析显示，这一开销换来了显著的尾部性能提升，但在资源严格受限的场景下需要权衡。

4. **损坏鲁棒性未验证**：尽管分布偏移实验（Table 3）展示了 GUIDE 对先验偏移的良好鲁棒性，但尚未在基于损坏的分布外基准（如 CIFAR‑100‑C）上进行系统性评估，其对图像损坏、噪声扰动等实际退化类型的泛化边界仍属开放问题。

### 开放问题与后续方向

GUIDE 框架揭示了两条值得深入探索的研究路径：

- **推理时策略的增强**：当前两步推理策略可视为一种朴素的测试时自适应形式。未来可探索更先进的推理时策略，如基于 Top‑k 预测的自一致性机制或多轮迭代细化，以进一步增强对初始预测错误的鲁棒性。

- **解耦原则的泛化验证**：GUIDE 的层次化解耦原则在长尾识别任务上取得了显著成功，但其在更广泛的分布外泛化场景（如领域自适应、开集识别）中的有效性尚未得到验证。在 CIFAR‑100‑C 等损坏基准上的系统性评估将是重要的下一步工作。



## 原文 PDF

![[paperPDFs/ICLR_2026/GUIDE_Gated_Uncertainty_Informed_Disentangled_Experts_for_Long_tailed_Recognition.pdf]]
