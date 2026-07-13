---
title: "Dynamic Multi-sample Mixup with Gradient Exploration for Open-set Graph Anomaly Detection"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Dynamic_Multi_sample_Mixup_with_Gradient_Exploration_for_Open_set_Graph_Anomaly_Detection.pdf
project_link: null
code_link: https://github.com/yucy324/DEMO
openreview_forum_id: zefuSJ3nOg
aliases:
- DMSMGEOSGAD
tags:
- ICLR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/graph_neural_networks
core_operator: "通过动态多样本混合（mixup）生成合成样本以扩大决策边界，并利用能量梯度驱动的样本加权来优先优化高不确定性样本，从而提升对未见异常的检测能力。"
primary_logic: "将多样本混合与能量梯度反馈结合，能够在标签极少的开放集设定下有效生成多样化的异常表示并动态聚焦关键样本，显著增强图异常检测的泛化性能。"
claims:
- "DEMO 在所有小规模数据集上均取得最优 AUC-ROC 和 AUC-PR，大幅领先最强基线。"
- "在三个大规模数据集上，DEMO 同样取得最佳或接近最佳的 AUC-ROC，且是少数能成功在 ogbn-mag 上运行的方法。"
- "在仅测试未见异常类别的开放集设定下，DEMO 在全部六个数据集上均取得最优 AUC-ROC 和 AUC-PR，验证了其对未知异常的强泛化能力。"
- "在极端标签稀缺（如仅 10 个训练异常节点）条件下，DEMO 的 AUC-ROC 和 AUC-PR 依然显著优于所有基线。"
---

# Dynamic Multi-sample Mixup with Gradient Exploration for Open-set Graph Anomaly Detection

> [!tip] 核心洞察
> 将多样本混合与能量梯度反馈结合，能够在标签极少的开放集设定下有效生成多样化的异常表示并动态聚焦关键样本，显著增强图异常检测的泛化性能。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 面向开放集图异常检测的动态多样本混合与梯度探索方法 |
| 英文题名 | Dynamic Multi-sample Mixup with Gradient Exploration for Open-set Graph Anomaly Detection |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=zefuSJ3nOg) · [GitHub](https://github.com/yucy324/DEMO) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/graph_neural_networks |
| Method | DEMO |
| Dataset | Photo (small-scale), Computers (small-scale), CS (small-scale) |

> [!tip] 效果简介
> - Photo (small-scale) 上，AUC-ROC 为 0.9023，对比 NSReg 0.8360，变化 +0.0663 (absolute)。
> - Photo (small-scale) 上，AUC-PR 为 0.6330，对比 NSReg 0.4777，变化 +0.1553 (absolute)。
> - Computers (small-scale) 上，AUC-ROC 为 0.8439，对比 SpaceGNN 0.8296，变化 +0.0143 (absolute)。

## 概要

图异常检测（GAD）在现实应用中面临一个根本性瓶颈：训练数据中异常类别有限且多样性不足，同时标签稀缺与严重的类别不平衡并存，导致现有方法难以泛化到开放集场景中未见过的异常类型。针对这一挑战，本文提出 DEMO（Dynamic Multi-sample Mixup with Gradient Exploration），通过两个核心机制协同提升开放集图异常检测的泛化能力——

- **动态多样本混合（Dynamic Multi-sample Mixup）**：自适应融合多个已见异常样本，生成多样化的合成异常表示，以扩大模型的决策边界，模拟未见异常类别。
- **能量梯度驱动的样本加权（Energy Gradient-based Weighting）**：计算每个训练节点的能量对验证损失的边际影响，动态分配样本权重，引导模型优先优化高不确定性的关键样本。
- **记忆库引导的伪标签（Memory Bank-guided Pseudo-labeling）**：维护历史统计信息，动态调整类感知的置信度阈值，缓解标签稀缺和类别不平衡带来的训练偏差。

在六个数据集上的实验表明，DEMO 在所有小规模数据集（Photo、Computers、CS）上均取得最优 AUC-ROC 和 AUC-PR，大幅领先最强基线——例如 Photo 数据集上 AUC-ROC 达 0.9023（NSReg 为 0.8360），AUC-PR 达 0.6330（NSReg 为 0.4777）。在三个大规模数据集（Yelp、ogbn-arxiv、ogbn-mag）上，DEMO 同样取得最佳或接近最佳的 AUC-ROC，且是少数能成功在 ogbn-mag 上运行的方法。在仅测试未见异常类别的严格开放集设定下，DEMO 在全部六个数据集上均取得最优结果，验证了其对未知异常的强泛化能力。消融实验进一步证实，三个组件协同作用不可或缺，移除任一组件均会导致显著性能下降。



图异常检测（Graph Anomaly Detection, GAD）在金融风控、社交网络虚假账户识别、电商欺诈检测等场景中具有重要应用价值。其核心任务是识别图中显著偏离正常模式的节点。然而，现有方法普遍面临一个根本性瓶颈：**训练数据中异常类别有限且多样性不足，同时标签稀缺与严重的类别不平衡并存，导致模型难以泛化到训练阶段未出现的异常类型**。

这一瓶颈在现实场景中尤为突出。异常行为不断演化，新型欺诈手段、新型攻击模式层出不穷，而标注数据往往仅覆盖少数已知异常类别。当测试阶段出现未见异常时，传统方法倾向于将其误判为正常，造成严重的漏检风险。这正是**开放集图异常检测（Open-set GAD）**所要解决的核心挑战：模型不仅需要准确识别已见异常，更需具备对未知异常类型的判别能力。

现有方法在应对这一挑战时存在明显缺口：

- **无监督方法**（如 DOMINANT、CoLA、CONAD 等）完全不利用标签信息，虽能检测与多数节点模式偏离的样本，但缺乏对异常语义的建模能力，难以区分结构性噪声与真正的语义异常。
- **半监督方法**（如 GGAD、TAM、SpaceGNN 等）利用少量标签引导学习，但在开放集设定下，其决策边界受限于已见异常的分布范围，对未见异常的覆盖能力有限。
- **判别式开放集方法**（如 NSReg）尝试通过负能量正则化扩大异常与正常的间隔，但数据增强策略较为单一，未能充分模拟未见异常的多样性。

上述方法的共同缺陷在于：**训练数据的异常表示空间过于狭窄，且缺乏有效机制来动态聚焦对泛化至关重要的高不确定性样本**。这直接限制了模型在标签极少、异常类别不完全的开放集场景下的性能上限。

针对上述问题，本文提出的 DEMO 方法从两个关键维度进行突破：

1. **扩大决策边界**：通过动态多样本混合（Dynamic Multi-sample Mixup）自适应融合多个已见异常样本，生成具有丰富表示的合成异常节点，近似模拟未见异常类别，从而驱动模型学习更宽广的决策边界。
2. **聚焦关键样本**：引入能量梯度驱动的反馈机制，动态评估并重加权每个训练样本，使模型自动关注对验证损失影响大的高不确定性节点，提升泛化效率。

此外，DEMO 还通过记忆库引导的类感知动态阈值伪标签策略，缓解标签稀缺与类别不平衡带来的训练偏差。三者协同作用，使得 DEMO 能够在仅利用极少标注异常的条件下，显著提升对未见异常的检测能力。



## 核心方法与创新机理

### 创新总览

DEMO 针对开放集图异常检测中“训练异常类别有限且多样性不足”这一核心瓶颈，引入了三个相互协同的创新机制。与现有方法相比，其关键差异体现在训练数据增强策略、样本加权策略和伪标签生成策略三个维度上，每个维度都针对性地解决了开放集场景下的特定挑战。

### 关键创新点对比

**训练数据增强：从简单扰动到动态多样本混合**

现有方法（如 NSReg、GGAD 等）通常不使用数据增强，或仅采用简单的边丢弃（drop edge）等扰动策略。这些方法无法有效扩展决策边界以覆盖未见异常类型。DEMO 提出**动态多样本混合（Dynamic Multi-sample Mixup）**机制，自适应地融合多个已见异常样本的特征表示，生成具有丰富多样性的合成异常节点。其核心在于基于特征相似度的动态权重分配：

$$\alpha_{ij} = \frac{\exp\left(S\left((z_i^{\mathrm{train}})^\top \mathbf{w}_m, (z_j^{\mathrm{train}})^\top \mathbf{w}_n\right)\right)}{\sum_k \exp\left(S\left((z_i^{\mathrm{train}})^\top \mathbf{w}_m, (z_k^{\mathrm{train}})^\top \mathbf{w}_n\right)\right)}$$

这一设计使高相似度样本获得更大混合权重，确保合成样本在保持异常语义的同时逼近未见异常分布。为进一步防止合成表示过度偏向原始样本，DEMO 引入多样性正则化项：

$$\mathcal{L}_{\mathrm{div}} = -\frac{1}{N}\sum_i \left\| \frac{(z_i^{\mathrm{train}})^\top \mathbf{w}_m}{\|(z_i^{\mathrm{train}})^\top \mathbf{w}_m\|_2} - \frac{(z_i^{\mathrm{train}})^\top \mathbf{w}_n}{\|(z_i^{\mathrm{train}})^\top \mathbf{w}_n\|_2} \right\|^2$$

该正则化项通过最大化不同投影方向上的特征差异，抑制单一原始样本对合成表示的主导影响，从而提升合成异常的多样性。

**样本加权策略：从等权处理到能量梯度驱动的动态加权**

现有方法对所有训练样本等权处理，或仅依赖人工设定的固定阈值，无法区分样本对模型泛化的边际贡献。DEMO 提出**基于能量梯度的动态加权机制**，通过计算每个训练节点能量对验证损失的边际影响来评估其重要性：

$$\mathcal{T}_{v_j^{\mathrm{val}}}(v_i) = -\nabla_{\theta} \mathcal{L}(v_j^{\mathrm{val}}, y_j^{\mathrm{val}}; \hat{\theta})^\top H_{\hat{\theta}}^{-1} \nabla_{\theta} E_{\theta}(v_i)$$

基于此影响分数，模型为每个样本分配自适应权重系数：

$$\beta_{v_i} = - \frac{T_{\mathrm{val}}(v_i)}{\max_{v_k \in \mathcal{V}^{\mathrm{train}}} T_{\mathrm{val}}(v_k)}$$

该权重被整合到能量感知损失中，使高不确定性样本获得更大的正则化强度：

$$\mathcal{L}_{\mathrm{energy}} = \frac{1}{n} \sum_{i=1}^n \left[ \mathcal{L}(v_i, y_i; \theta) + \lambda_{\mathrm{eng}} \beta_{v_i} \cdot E_{\theta}(v_i) \right]$$

这一机制使模型自动聚焦于对验证性能影响大的关键样本，避免在简单样本上浪费容量。

**伪标签生成：从固定阈值到类感知动态阈值调整**

现有伪标签方法采用固定阈值策略，在类别严重不平衡的图异常检测场景下，容易导致多数类（正常节点）过度主导伪标签分配，而少数类（异常节点）被系统性忽略。DEMO 引入**基于记忆库的类感知动态阈值调整**机制，通过维护历史统计信息来动态更新各类别的置信度阈值：

$$\tau_t^{+/-} = \begin{cases} \rho_t(c) \cdot \tau^+, & c = \mathrm{anomaly}, \\ \tau^- \cdot (2 - \rho_t(c)), & c = \mathrm{normal} \end{cases}$$

其中 $\rho_t(c)$ 反映第 $t$ 次迭代中类别 $c$ 被选为伪标签的样本比例。这一非对称更新策略在异常类别被选中比例较低时自动降低异常阈值、提高正常阈值，从而缓解类别不平衡对伪标签质量的负面影响。

### 协同效应

三个创新点并非孤立运作。多样本混合生成的合成异常为能量梯度加权提供了更丰富的训练信号，而动态加权机制反过来确保模型优先学习那些对未见异常判别最具价值的合成样本。类感知伪标签则进一步扩充了训练数据，为混合模块提供更多样化的原始异常表示。消融实验（Table 3）证实，同时移除所有组件（w/o All）导致性能降至最低，验证了三者的协同不可或缺。



![[assets/figures/papers/iclr26_0009_zefuSJ3nOg_Dynamic_Multi-sample_Mixup_with_Gradient_Explora/figures/001_Figure_1.jpg]]
*Figure 1: An overview of the proposed DEMO. DEMO first expands the training data through two parallel augmentation techniques. Multi-Sample Mixup generates new synthetic anomalies, while Pseudo-Labeling assigns labels to reliable unlabeled nodes. This augmented training data, comprising original, mixup, and pseudo-labeled data, then proceeds to a dynamic weighting stage*

DEMO 的整体流程围绕一个核心瓶颈展开：训练数据中异常类别有限且多样性不足，同时面临标签稀缺与严重的类别不平衡，导致现有方法难以泛化到未见异常类型。为解决这一问题，DEMO 通过三条协同路径构建了端到端的开放集图异常检测框架（Figure 1）。

**输入与骨干网络。** 框架以属性图 $\mathcal{G} = (\mathcal{V}, \mathcal{E}, \mathbf{X})$ 为输入，其中仅少量节点带有异常/正常标签。采用 GraphSAGE 作为图神经网络骨干，将每个节点 $v_i$ 编码为嵌入表示 $z_i$，所有后续模块均在此嵌入空间上运作。

**两条并行的数据增强支路。** 训练数据扩展通过两个互补模块实现：
1. **动态多样本混合（Dynamic Multi-sample Mixup）**：自适应融合多个已见异常样本的嵌入，生成合成异常节点 $\hat{z}_i$。这些合成节点模拟未见异常类别的特征分布，从而推动模型学习更广泛的决策边界。混合权重由特征相似度动态计算，并引入多样性正则化 $\mathcal{L}_{\mathrm{div}}$ 防止合成表示过度偏向原始样本。
2. **记忆库引导的伪标签生成（Memory Bank-guided Pseudo-labeling）**：维护历史统计信息，动态调整类感知置信度阈值 $\tau_t^+$ / $\tau_t^-$。对异常类提升敏感度（$\rho_t(c) \cdot \tau^+$），对正常类抑制过度主导（$\tau^- \cdot (2 - \rho_t(c))$），从而在类别不平衡条件下为未标注节点生成可靠伪标签。

**动态加权阶段。** 增强后的训练数据（原始样本 + 合成样本 + 伪标签样本）进入能量梯度驱动的动态加权模块。该模块计算每个训练节点的能量梯度对验证损失的影响 $\mathcal{T}_{v_j^{\mathrm{val}}}(v_i)$，并将其归一化为自适应权重系数 $\beta_{v_i}$。高不确定性样本获得更大权重，引导模型优先优化对泛化性能影响最大的关键样本。

**输出与优化目标。** 最终损失函数整合三个分量：
$$\mathcal{L} = \mathcal{L}_{\mathrm{energy}} + \lambda_{\mathrm{mix}} \mathcal{L}_{\mathrm{mix}} + \lambda_{\mathrm{un}} \mathcal{L}_{\mathrm{un}}$$
其中 $\mathcal{L}_{\mathrm{energy}}$ 为带能量引导项的分类损失（Eq. 8），$\mathcal{L}_{\mathrm{mix}}$ 为混合一致性损失与多样性正则化的联合（Eq. 4），$\mathcal{L}_{\mathrm{un}}$ 为伪标签损失。模型输出每个节点的异常分数，对已见和未见异常均赋予高分，对正常节点赋予低分。

**模块间因果关系。** 多样本混合扩大了决策边界的覆盖范围，伪标签缓解了标注稀疏问题，而能量梯度加权则动态聚焦于对验证性能边际影响最大的样本——三者协同作用，使得在标签极少的开放集设定下，模型能够有效生成多样化的异常表示并动态聚焦关键样本。消融实验（Table 3, Table 8）证实，移除任一模块均导致显著性能下降，三者缺一不可。



DEMO 围绕三个核心模块构建：**动态多样本混合（Dynamic Multi-sample Mixup）**、**能量梯度驱动的样本加权（Energy Gradient-based Weighting）** 和 **记忆库引导的伪标签生成（Memory Bank-guided Pseudo-labeling）**。三个模块协同解决开放集图异常检测中训练异常多样性不足、标签稀缺和类别不平衡的瓶颈。

### 动态多样本混合

该模块自适应地融合多个已见异常样本，生成多样化的合成异常表示，从而扩大模型的决策边界以覆盖未见异常类型。给定训练异常节点 $v_i$ 的嵌入 $z_i^{\text{train}}$，通过两个可学习矩阵 $\mathbf{w}_m$ 和 $\mathbf{w}_n$ 将其投影到两个不同子空间，再基于特征相似度计算混合权重：

$$ \alpha_{ij} = \frac{\exp\left(S\left((z_i^{\text{train}})^\top \mathbf{w}_m, (z_j^{\text{train}})^\top \mathbf{w}_n\right)\right)}{\sum_k \exp\left(S\left((z_i^{\text{train}})^\top \mathbf{w}_m, (z_k^{\text{train}})^\top \mathbf{w}_n\right)\right)} \tag{Eq.1} $$

其中 $S(\cdot,\cdot)$ 为相似度函数，$\alpha_{ij}$ 表示样本 $j$ 对合成样本 $i$ 的贡献权重。高相似度样本获得更大权重，使合成表示保留原始异常的语义结构。

为防止合成表示过度偏向原始样本（退化情况），引入多样性正则化项：

$$ \mathcal{L}_{\text{div}} = -\frac{1}{N}\sum_i \left\| \frac{(z_i^{\text{train}})^\top \mathbf{w}_m}{\|(z_i^{\text{train}})^\top \mathbf{w}_m\|_2} - \frac{(z_i^{\text{train}})^\top \mathbf{w}_n}{\|(z_i^{\text{train}})^\top \mathbf{w}_n\|_2} \right\|^2 \tag{Eq.3} $$

该正则化通过最大化两个投影方向之间的差异，抑制原始样本对合成表示的主导影响。混合损失由一致性损失与多样性正则化联合构成：

$$ \mathcal{L}_{\text{mix}} = \mathcal{L}_{\text{cons}} + \lambda_{\text{div}} \mathcal{L}_{\text{div}} \tag{Eq.4} $$

### 能量梯度驱动的样本加权

该模块的核心思想是：并非所有训练样本对模型泛化同等重要，应优先关注那些对验证性能影响大的高不确定性节点。具体而言，定义节点 $v_i$ 的能量函数 $E_\theta(v_i)$，计算其能量梯度对验证损失的影响：

$$ \mathcal{T}_{v_j^{\text{val}}}(v_i) = -\nabla_{\theta} \mathcal{L}(v_j^{\text{val}}, y_j^{\text{val}}; \hat{\theta})^\top H_{\hat{\theta}}^{-1} \nabla_{\theta} E_{\theta}(v_i) \tag{Eq.6} $$

其中 $H_{\hat{\theta}}^{-1}$ 为 Hessian 矩阵的逆，$\mathcal{T}_{v_j^{\text{val}}}(v_i)$ 量化了训练节点 $v_i$ 的能量扰动对验证样本 $v_j^{\text{val}}$ 损失的边际影响。将所有验证样本的影响聚合后归一化，得到自适应权重系数：

$$ \beta_{v_i} = - \frac{T_{\text{val}}(v_i)}{\max_{v_k \in \mathcal{V}^{\text{train}}} T_{\text{val}}(v_k)} \tag{Eq.7} $$

$\beta_{v_i}$ 越大，表示该样本对验证损失的负面影响越强，应在训练中施加更大的正则化。最终能量感知损失为：

$$ \mathcal{L}_{\text{energy}} = \frac{1}{n} \sum_{i=1}^n \left[ \mathcal{L}(v_i, y_i; \theta) + \lambda_{\text{eng}} \beta_{v_i} \cdot E_{\theta}(v_i) \right] \tag{Eq.8} $$

该损失对高 $\beta_{v_i}$ 样本施加更强的能量正则化，引导模型聚焦于决策边界附近的高不确定性区域。

### 记忆库引导的伪标签生成

为缓解标签稀缺，该模块维护历史统计信息，动态调整类感知的置信度阈值。在第 $t$ 次迭代，统计各类别被选为伪标签的样本数量：

$$ \sigma_t(c) = \sum_{i=1}^M \mathbb{I} \left[ c = 1 \wedge \hat{p}_t(v_i) \geq \tau_t^+ \vee c = 0 \wedge \hat{p}_t(v_i) \leq \tau_t^- \right] \tag{Eq.9} $$

基于各类别的选择比例 $\rho_t(c)$，对异常类和正常类分别进行不对称阈值更新：

$$ \tau_t^{+/-} = \begin{cases} \rho_t(c) \cdot \tau^+, & c = \text{anomaly}, \\ \tau^- \cdot (2 - \rho_t(c)), & c = \text{normal} \end{cases} \tag{Eq.10} $$

当异常类被选中的比例较低时，$\tau_t^+$ 降低以提高敏感度；当正常类过度主导时，$\tau_t^-$ 收紧以抑制其影响。这种类感知的动态调整有效缓解了类别不平衡对伪标签质量的影响。

### 整体优化目标

三个模块的损失联合优化，最终训练目标为：

$$ \mathcal{L} = \mathcal{L}_{\text{energy}} + \lambda_{\text{mix}} \mathcal{L}_{\text{mix}} + \lambda_{\text{un}} \mathcal{L}_{\text{un}} \tag{Eq.11} $$

其中 $\mathcal{L}_{\text{un}}$ 为伪标签损失，$\lambda_{\text{mix}}$ 和 $\lambda_{\text{un}}$ 为平衡系数。消融实验（Table 3, Table 8）表明，移除任一组件均导致显著性能下降，三者协同作用对取得最优结果不可或缺。

> **注意**：上述公式均来自论文正文（Section 3.2–3.5），变量含义以原文为准。Hessian 逆矩阵在实际计算中采用近似方法，其可扩展性在大规模图上构成潜在瓶颈（见局限性分析）。



## 实验与关键发现

### 主实验结果

DEMO 在六个数据集上全面验证了其有效性，涵盖三个小规模数据集（Photo、Computers、CS）和三个大规模数据集（Yelp、ogbn-arxiv、ogbn-mag）。实验采用 AUC-ROC 和 AUC-PR 作为核心评价指标，所有基线方法使用与 DEMO 相同的训练/测试数据分割以保证公平比较。

在小规模数据集上，DEMO 在所有指标上均取得最优结果。如 Table 1 所示，DEMO 在 Photo 数据集上达到 AUC-ROC 0.9023，相比最强基线 NSReg 的 0.8360 提升了 6.63 个百分点；AUC-PR 达到 0.6330，较 NSReg 的 0.4777 提升了 15.53 个百分点。在 Computers 数据集上，DEMO 的 AUC-ROC 为 0.8439，领先 SpaceGNN 的 0.8296；CS 数据集上 AUC-ROC 达到 0.9448，显著优于 GGAD 的 0.9081。与无监督方法相比，DEMO 的平均 AUC-ROC 较 CoLA 提升了 80.99%，平均 AUC-PR 较 GAAN 提升了 368.11%，充分说明仅利用少量标注异常即可大幅超越无监督范式。


![[assets/figures/papers/iclr26_0009_zefuSJ3nOg_Dynamic_Multi-sample_Mixup_with_Gradient_Explora/figures/002_Table_1.jpg]]
*Table 1: AUC-ROC and AUC-PR on three small-scale datasets. The best performance is boldfaced, with the second-best underlined*

在大规模数据集上，DEMO 同样展现出强大的竞争力。如 Table 2 所示，DEMO 在 Yelp 上取得 AUC-ROC 0.7097，以 1.16% 的相对提升优于 NSReg；在 ogbn-arxiv 上 AUC-ROC 达到 0.6364，较 NSReg 的 0.6111 提升 2.33%；值得注意的是，DEMO 是少数能在 ogbn-mag 上成功运行的方法，而多个基线因显存不足（OOM）而失败。


![[assets/figures/papers/iclr26_0009_zefuSJ3nOg_Dynamic_Multi-sample_Mixup_with_Gradient_Explora/figures/003_Table_2.jpg]]
*Table 2: AUC-ROC and AUC-PR on three large-scale datasets. The best performance is boldfaced, with the second-best underlined. ‘OOM’ indicates out-of-memory*

### 开放集泛化能力

在仅测试未见异常类别的严格开放集设定下，DEMO 的优势更为突出。如 Table 5 和 Table 6 所示，DEMO 在全部六个数据集上均取得最优 AUC-ROC 和 AUC-PR。以 Photo 数据集为例，DEMO 在未见异常类别上的 AUC-ROC 达到 0.8202，较 NSReg 的 0.7369 提升了 8.33 个百分点，验证了多样本混合策略在生成未知异常表示、拓展决策边界方面的核心作用。


![[assets/figures/papers/iclr26_0009_zefuSJ3nOg_Dynamic_Multi-sample_Mixup_with_Gradient_Explora/figures/011_Table_5.jpg]]
*Table 5: AUC-ROC and AUC-PR on the unseen anomaly classes on three small-scale datasets. The best performance is boldfaced, with the second-best underlined*

![[assets/figures/papers/iclr26_0009_zefuSJ3nOg_Dynamic_Multi-sample_Mixup_with_Gradient_Explora/figures/012_Table_6.jpg]]
*Table 6: AUC-ROC and AUC-PR on the unseen anomaly classes on three large-scale datasets. The best performance is boldfaced, with the second-best underlined*

### 标签效率分析

在极端标签稀缺条件下，DEMO 依然保持显著优势。如 Figure 4 和 Figure 5 所示，当训练异常节点数量从全量逐步减少至仅 10 个时，DEMO 的 AUC-ROC 和 AUC-PR 在所有数据集上均持续优于各基线方法。这一结果归因于两个关键机制：基于记忆库的伪标签生成有效利用了未标注节点中的信息，缓解了标签稀缺；能量梯度驱动的动态加权使模型在样本极度有限时仍能聚焦于高价值样本。

### 消融实验

Table 3 和 Table 8 展示了各核心组件的消融结果。移除伪标签模块（w/o PL）导致所有数据集上性能大幅下降，尤其在复杂数据集上影响最为显著，说明在标签稀缺场景下伪标签机制对模型训练至关重要。移除多样本混合模块（w/o Mix）或能量梯度加权模块（w/o EG）同样明显削弱模型表现，验证了合成异常生成与动态样本聚焦的独立价值。同时移除所有组件（w/o All）导致性能降至最低，表明三个组件之间存在协同效应，共同构成了 DEMO 性能优势的基础。


![[assets/figures/papers/iclr26_0009_zefuSJ3nOg_Dynamic_Multi-sample_Mixup_with_Gradient_Explora/figures/008_Table_3.jpg]]
*Table 3: Ablation Study on two benchmarks*

### 可视化分析

Figure 3 的 t-SNE 特征可视化进一步佐证了 DEMO 的有效性。相比基线方法，DEMO 生成的节点嵌入中异常样本（蓝色）聚类更紧密，且与正常类别（其他颜色）的分离边界更清晰。这直观地反映了多样本混合策略在增强异常表示判别力方面的作用。

### 超参数敏感性

Figure 2(d) 展示了正常类伪标签阈值 τ⁻ 的敏感性分析。在 Photo 数据集上，AUC-ROC 在 τ⁻ ∈ [0.01, 0.10] 范围内稳定在约 90%；CS 数据集上 AUC-ROC 整体更高约 94%，但随 τ⁻ 增大从约 95% 下降至约 93%，呈现轻微下降趋势。总体而言，模型对阈值选择具有一定鲁棒性，但不同数据集的最优区间存在差异。

损失权重的敏感性分析（Figure 7、Figure 8）揭示了更复杂的依赖关系。在 Photo 数据集上，最佳 AUC-PR（未见类别）出现在 λ_un=0.5、λ_eng=0.1 的组合；Computers 数据集上，较低的 λ_un（0.1）配合中等 λ_eng 通常表现更优。这表明最优超参数在不同数据集间差异明显，限制了即插即用的部署能力，实际应用中可能需要针对具体数据集进行调参。

### 失败模式与局限

尽管 DEMO 在多个维度上表现优异，分析揭示了若干值得关注的局限。首先，多样本混合若比例过大可能引入分布偏移或生成过度模糊的特征，需要仔细调节混合权重与多样性正则化系数以维持训练稳定性。其次，损失权重（λ_un、λ_eng）的最优取值在不同数据集间差异显著，目前缺乏自动调整机制。此外，能量梯度加权涉及 Hessian 逆矩阵的近似计算，在大规模图上可能面临可扩展性瓶颈。最后，当前评估基于模拟的开放集划分，在真实世界中完全未知的异常场景下的鲁棒性仍需进一步验证。



## 定位与知识库关联

### 与现有基线的结构性差异

DEMO 在开放集图异常检测（Open-set GAD）领域引入了一条不同于主流范式的技术路径。现有方法可大致归为三类，DEMO 与每一类都存在根本性的设计差异：

**无监督 GAD 方法**（ANOMALOUS、DOMINANT、AnomalyDAE、GAAN、CoLA、CONAD）完全依赖正常样本的分布建模，通过重构误差或对比学习识别偏离常态的节点。这类方法的核心瓶颈在于缺乏对异常类别的显式建模——当测试集中出现与训练分布完全不同的未见异常类型时，模型无法区分“已知正常”与“未知异常”的边界。实验证据充分暴露了这一局限：在 Photo 数据集上，表现最好的无监督方法 CoLA 仅取得 0.5013 的 AUC-ROC（Table 1），远低于 DEMO 的 0.9023，差距达 80.99% 的相对提升。

**半监督 GAD 方法**（GGAD、TAM、OCGNN、SpaceGNN、NSReg 等）引入了少量异常标签，通过边界优化或异常生成来增强检测能力。然而，这些方法的异常生成策略通常是单样本扰动或固定规则的合成（如边界外推），缺乏对异常表示多样性的系统探索。以最强基线 NSReg 为例，其判别式开放集设计在 Photo 上取得 0.8360 AUC-ROC，但 DEMO 通过**动态多样本混合**将这一指标提升至 0.9023（+0.0663 绝对值），在 AUC-PR 上更是从 0.4777 跃升至 0.6330（+0.1553 绝对值，Table 1）。这一差距揭示了核心因果机制：单样本扰动无法充分覆盖未见异常的表示空间，而多样本自适应融合能够生成更具覆盖性的合成异常，从而扩大决策边界。

**开放集分类适应方法**（GNN+OpenMax）将图像领域的 OpenMax 机制迁移到图域，但其依赖对已知类别的激活向量建模，在标签极度稀缺的 GAD 场景下几乎失效——在 Photo 上仅取得 0.6638 AUC-ROC（Table 1），验证了直接迁移的局限性。

### 核心机制的有效性边界

DEMO 的三个关键模块——动态多样本混合（Mix）、能量梯度加权（EG）、记忆库引导伪标签（PL）——构成了一个协同系统，但其有效性存在明确的边界条件：

**多样本混合的适用前提**是训练集中至少存在少量已标注的异常样本，且这些样本的特征空间具有一定的连续性。当训练异常数量极端稀少（如仅 10 个）时，混合生成的合成样本可能过度集中在少数几个原始样本的凸组合区域内，难以有效覆盖未见异常的分布。Figure 4 和 Figure 5 显示，DEMO 在 10 个训练异常的条件下仍显著优于所有基线，但性能的绝对水平（尤其是 AUC-PR）随异常数量减少而下降，说明混合策略的收益与训练异常的多样性正相关。

**能量梯度加权的核心假设**是验证集能够代表目标分布中的困难样本。该机制通过 Hessian 逆矩阵近似计算训练节点能量对验证损失的影响（Eq. 6-7），对高不确定性样本施加更大的正则化。然而，这一机制的有效性依赖于验证集的质量——如果验证集中缺乏边界模糊的样本，能量梯度反馈可能无法准确识别真正需要关注的训练节点。此外，Hessian 逆矩阵的近似计算在大规模图上可能面临可扩展性瓶颈，这在 ogbn-mag 数据集上表现为 AUC-ROC 仅 0.4967（Table 2），虽优于所有能运行的基线，但绝对性能仍有较大提升空间。

**伪标签模块**在消融实验中表现出最大的单独贡献——移除 PL 后，Photo 上 AUC-ROC 从 0.9023 降至 0.8616（Table 3）。这验证了在标签稀缺条件下，利用未标注数据扩展训练集的关键作用。但该模块的类感知动态阈值调整（Eq. 10）依赖于对历史统计信息的准确估计，在训练初期或类别极度不平衡时可能出现阈值震荡，需要人工设定的初始阈值 τ⁺ 和 τ⁻（论文中设为 0.99 和 0.01）来稳定训练。

### 已知局限与开放问题

**分布偏移风险**：多样本混合若比例过大（由 λ_mix 控制），可能生成过度模糊或偏离真实异常分布的合成样本。论文通过多样性正则化 L_div（Eq. 3）抑制原始样本的主导影响，但不同数据集的最优 λ_div 差异显著（Table 7），限制了即插即用的部署能力。

**超参数敏感性**：λ_un 和 λ_eng 在不同数据集上的最优取值差异明显（Figure 7, Figure 8），当前需要针对每个数据集进行网格搜索，增加了实际应用的调参成本。

**评估场景的局限**：所有实验基于模拟的开放集划分（按类别留出未见异常），尚未在真实世界中完全未知的异常场景（如新型欺诈模式、突发网络攻击）下验证。Table 5 和 Table 6 的“未见类别”实验结果虽然全面领先，但划分方式仍基于已知的类别结构，与真正的开放世界设定存在差距。

**可扩展性瓶颈**：能量梯度计算涉及 Hessian 逆矩阵的近似，在大规模图（如 ogbn-mag）上虽能运行但性能提升有限（AUC-ROC 0.4967 vs NSReg 0.4888，Table 2），表明计算效率与检测性能之间存在权衡。

### 值得探索的开放方向

1. **自适应混合策略**：能否根据图的局部结构（如节点度、社区归属）自动调整混合权重和损失平衡系数，以减少人工调参需求？异质图中不同类型节点的异常模式差异显著，自适应机制可能带来更大的性能增益。

2. **能量梯度机制的泛化**：能量梯度驱动的样本加权本质上是一种基于验证反馈的重要性采样策略，该机制能否推广到其他图学习任务（如节点分类中的长尾分布处理、链接预测中的难负样本挖掘）？

3. **动态图场景适配**：DEMO 当前假设图结构静态不变，但在流式图或动态拓扑变化场景下，记忆库的历史统计信息可能快速失效，伪标签模块需要增量更新机制来维持有效性。

4. **图结构增强的融合**：Mixup 当前仅在特征空间生成合成节点，能否将合成节点进一步用于图结构增强（如生成连接边），使模型同时学习结构和特征的异常模式？这可能提升对结构性异常（如伪装成正常连接模式的恶意节点）的检测鲁棒性。

5. **真实开放世界验证**：需要在完全未知的异常类型（而非按类别留出）和更极端的标签稀缺条件（如仅 1-5 个标注异常）下评估 DEMO 的泛化能力，以更贴近实际部署场景。



## 原文 PDF

![[paperPDFs/ICLR_2026/Dynamic_Multi_sample_Mixup_with_Gradient_Exploration_for_Open_set_Graph_Anomaly_Detection.pdf]]
