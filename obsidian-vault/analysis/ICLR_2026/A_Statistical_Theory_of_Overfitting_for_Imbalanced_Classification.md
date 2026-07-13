---
title: "A Statistical Theory of Overfitting for Imbalanced Classification"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/A_Statistical_Theory_of_Overfitting_for_Imbalanced_Classification.pdf
project_link: null
code_link: null
aliases:
- SMRS
- STOIC
tags:
- ICLR_2026
- topic/optimization_theory_probabilistic
- topic/optimization_theory_probabilistic/learning_theory
core_operator: "边际重平衡超参数τ（margin-rebalancing hyperparameter），通过调整少数类和多数类的边际权重来平衡两类错误率。"
primary_logic: "高维线性可分数据中，训练集logit分布收敛到截断高斯分布（max{κ, N(0,1)}），测试集logit分布保持N(0,1)；这种截断完全解释了过拟合现象，且少数类因截断损失更多质量而表现更差。边际重平衡通过调整τ来对齐两类错误率，从而缓解少数类精度下降。"
claims:
- "训练集logit分布为截断高斯，测试集logit分布为高斯"
- "边际重平衡可缓解少数类精度下降"
- "高维性导致logit分布的截断或偏斜效应"
- "两类共享一个共同的过拟合预算，不成比例地移动少数类边界"
---

# A Statistical Theory of Overfitting for Imbalanced Classification

> [!tip] 核心洞察
> 高维线性可分数据中，训练集logit分布收敛到截断高斯分布（max{κ, N(0,1)}），测试集logit分布保持N(0,1)；这种截断完全解释了过拟合现象，且少数类因截断损失更多质量而表现更差。边际重平衡通过调整τ来对齐两类错误率，从而缓解少数类精度下降。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 不平衡分类过拟合的统计理论 |
| 英文题名 | A Statistical Theory of Overfitting for Imbalanced Classification |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=cKthi6QfUr) |
| Topic | #topic/optimization_theory_probabilistic #topic/optimization_theory_probabilistic/learning_theory |
| Method | 边际重平衡SVM（Margin-Rebalanced SVM） |
| Dataset | 2-GMM合成数据, IFNB单细胞RNA-seq |

> [!tip] 效果简介
> - 2-GMM合成数据 上，少数类错误率 Err_+ 为 随τ增大而下降，对比 τ=1时随π减小趋近1，变化 τ>1可显著降低Err_+。
> - 2-GMM合成数据 上，多数类错误率 Err_- 为 随τ增大而上升，对比 τ=1时随π减小趋近0，变化 τ>1以牺牲多数类精度换取少数类精度。
> - 2-GMM合成数据 上，平衡错误率 Err_b 为 在最优τ下最小化，对比 τ=1时随π减小趋近1/2，变化 最优τ可显著降低平衡错误率。

## 概要

本文《不平衡分类过拟合的统计理论》（ICLR 2025）系统研究了高维线性分类器在不平衡数据上的过拟合现象。核心发现是：**训练集logit分布收敛到截断高斯分布（rectified Gaussian），而测试集logit分布保持标准高斯分布**——这一截断效应完全解释了高维下的过拟合行为，且少数类因共享的“过拟合预算”不成比例地损失更多质量，导致其精度下降更严重。

方法上，论文提出**边际重平衡SVM**（Margin-Rebalanced SVM），通过超参数τ调整少数类的边际权重（τ>1），从而对齐两类错误率。理论分析表明，在比例极限（n,d→∞, n/d→δ）下，存在三个信号强度区间：高信号下无需重平衡，中等信号下重平衡至关重要，低信号下无法优于随机猜测。实验在合成2-GMM数据以及IFNB单细胞RNA-seq、CIFAR-10（ResNet-18）、IMDb（BERT base）、TruthfulQA（Llama-3-8B-Instruct）等真实数据上验证了截断现象的普遍存在，并展示了边际重平衡有效降低少数类错误率与平衡错误率。此外，论文还分析了校准误差与Brier分数随不平衡加剧而恶化的单调性。



不平衡分类（imbalanced classification）是机器学习的核心挑战之一：当少数类样本比例极低时，标准分类器（如SVM、逻辑回归）倾向于将几乎所有样本预测为多数类，导致少数类精度趋近于零。现有工作多从重采样、代价敏感学习等工程角度出发，但缺乏对**高维空间中过拟合如何被不平衡加剧**这一根本机制的严格理论理解。本文（ICLR 2025）正是针对这一缺口展开系统分析。

**问题的根源在于高维特征空间中的logit分布截断效应**。作者发现，在可分离的高维线性分类问题中，训练集logit分布收敛到截断高斯分布 $\max\{\kappa, N(0,1)\}$，而测试集logit分布保持标准高斯分布 $N(0,1)$。这种截断效应源于两类共享一个共同的“过拟合预算”（overfitting budget），该预算**不成比例地移动了少数类的边界**，导致少数类的截断损失更多概率质量，从而表现更差（Figure 1）。这一现象在表格数据（IFNB单细胞RNA-seq）、图像数据（CIFAR-10 + ResNet-18）、文本数据（IMDb + BERT）甚至LLM激活探测（TruthfulQA + Llama-3-8B-Instruct）中均被复现（Figure 2, 3），表明其具有跨模态的普遍性。

**现有方法的缺口**在于：标准SVM（$\tau=1$）和逻辑回归在高维不平衡场景下均无法缓解少数类的精度崩溃。Table 1定性对比了低维与高维下二元分类的差异，指出高维性导致logit分布的偏斜或截断，而低维下不存在此效应。作者进一步通过2-GMM合成数据实验（Figure 4）展示：当少数类比例 $\pi$ 减小时，标准SVM的少数类错误率趋近1，而多数类错误率趋近0——这正是过拟合预算被不成比例分配的直接后果。

**本文的核心动机**是提出并严格论证一个简单的补救机制：**边际重平衡（margin rebalancing）**。通过引入超参数 $\tau$ 对少数类的边际约束施加更大权重（即 $\tilde{y}_i = \tau \cdot y_i$ 对少数类，$y_i$ 对多数类），可以系统性调整决策边界偏移 $\beta_0^*(\tau) = \beta_0^*(1) + \frac{\tau-1}{\tau+1} \kappa^*(1)$ 和边际大小 $\kappa^*(\tau) = \frac{2}{\tau+1} \kappa^*(1)$（Proposition C.1）。这一机制在合成数据（Figure 4）和真实数据（Figure 2）上均能显著降低少数类错误率，尽管以牺牲多数类精度为代价——即存在固有的公平性权衡。

**理论贡献的独特之处**在于：作者不仅刻画了过拟合的统计机制（截断高斯分布），还提供了可操作的相变条件（Theorem 3.2）：在高信号强度下无需边际重平衡，中等信号下边际重平衡至关重要，低信号下无法优于随机猜测。这为实际应用中的 $\tau$ 选择提供了理论指导，而此前缺乏此类基于渐近极限的定量分析。

**值得注意的局限性**包括：理论分析主要基于高斯混合模型（2-GMM），对非高斯数据的适用性仅通过t分布实验初步验证（Figure 16）；边际重平衡的最优 $\tau$ 表达式依赖于渐近极限，在有限样本下可能不精确；多类分类的扩展仅给出猜想，缺乏严格证明；校准误差的单调性仅在 $\pi \leq 0.25$ 时成立（Claim D.10），更极端的 $\pi$ 行为未完全刻画。此外，本文仅分析线性探测（linear probing）场景，未考虑端到端特征学习的复杂交互——后者在深度神经网络中可能引入额外的过拟合源。



## 核心方法与创新机理

本文的核心创新在于揭示并理论化了一个此前未被系统解释的现象：**高维线性可分分类中，过拟合的根源是训练集logit分布的截断效应，而非传统的偏差-方差权衡**。在此基础上，论文提出了一个简洁且可理论分析的补救措施——边际重平衡。

### 瓶颈与因果机制

论文识别出的根本瓶颈是：在高维（$n, d \to \infty$，$n/d \to \delta$）且线性可分的设定下，训练集和测试集上的logit分布呈现根本性差异。具体而言，训练集上的经验logit分布（ELD）收敛到一个**截断高斯分布**（rectified Gaussian），形式为 $\max\{\kappa^*, \rho^*\|\mu\|_2 + G + Y\beta_0^*\}$，其中 $G \sim N(0,1)$，$\kappa^*$ 是最大边际；而测试集上的logit分布（TLD）则保持为完整的高斯分布 $N(\rho^*\|\mu\|_2 + \beta_0^*, 1)$（对于正类）或 $N(\rho^*\|\mu\|_2 - \beta_0^*, 1)$（对于负类）。这种截断完全解释了过拟合：训练集上所有点都被“推到”边际边界之外，实现零训练误差；但测试集上高斯分布的重叠区域直接导致了正测试误差。

因果机制的关键在于**两类共享一个共同的“过拟合预算”**（overfitting budget）。这个预算不成比例地移动了少数类的决策边界，导致少数类的边际边界 $\beta_0^*$ 随不平衡加剧而向多数类方向偏移，最终使少数类错误率趋近于1。论文通过最优传输理论严格证明了从TLD到ELD的映射是一个简单的截断操作 $\mathrm{T}^*(x) = \max\{\kappa^*, x\}$，从而将过拟合归因于这一确定的分布变换。

### 核心改变：边际重平衡

针对上述瓶颈，论文提出的核心干预是**边际重平衡超参数 $\tau$**。相比标准SVM（$\tau=1$，两类权重相同），边际重平衡SVM（Margin-Rebalanced SVM）对少数类样本施加更大的边际权重 $\widetilde{y}_i = \tau \cdot y_i$（对于少数类），优化问题变为：
$$
\operatorname{maximize}_{\beta,\beta_0,\kappa} \kappa \quad \mathrm{subject\ to} \quad \widetilde{y}_i(\langle{\pmb x}_i,{\pmb\beta}\rangle + \beta_0) \geq \kappa, \forall i\in[n], \quad \|\beta\|_2 \leq 1.
$$

该改变通过三个关键参数的调整实现效果：
1. **边际约束权重 $\tau$**：从 $\tau=1$（两类相同）变为 $\tau>1$（少数类更大边际）。
2. **决策边界偏移 $\beta_0$**：从 $\beta_0^*(1)$（标准SVM）变为 $\beta_0^*(\tau) = \beta_0^*(1) + \frac{\tau-1}{\tau+1} \kappa^*(1)$，即向多数类方向平移以补偿过拟合预算的不对称分配。
3. **边际大小 $\kappa$**：从 $\kappa^*(1)$ 变为 $\kappa^*(\tau) = \frac{2}{\tau+1} \kappa^*(1)$，整体边际缩小以平衡两类错误率。

### 理论洞察与相变

论文最重要的理论洞察是揭示了高不平衡区间下的**三阶段相变**（Theorem 3.2）：
- **高信号**（$a - c < b$）：无需边际重平衡，任意 $\tau$ 均可获得低错误率。
- **中等信号**（$b < a - c < 2b$）：边际重平衡至关重要。若采用 $\tau_d \asymp 1$ 的朴素方案，少数类错误率趋近1；但若选择 $\tau_d \gg d^{a-b-c}$，则可同时降低两类错误率。
- **低信号**（$a - c > 2b$）：任何 $\tau$ 都无法优于随机猜测（平衡错误率 $\geq 1/2$）。

这一相变直接指导了实际应用：在不平衡分类中，边际重平衡并非总是必要，其价值取决于信号强度与维度、样本量的相对关系。

### 证据强度与验证

论文提供了多层次的证据支持其核心主张：
- **合成数据**（Figure 1, 4）：2-GMM模拟精确复现了ELD截断高斯、TLD高斯的分布形态，并展示了边际重平衡对错误率的系统影响。
- **真实数据**（Figure 2）：在IFNB单细胞RNA-seq（表格）、CIFAR-10+ResNet-18（图像）、IMDb+BERT（文本）三种模态上，逻辑回归的ELD/TLD均呈现一致的截断模式，证明该现象并非合成数据特例。
- **LLM探测**（Figure 3）：在Llama-3-8B-Instruct的TruthfulQA激活探测中，同样观察到训练集logit截断和测试集logit扭曲，表明该理论可扩展至大语言模型的内部表示分析。
- **校准分析**（Figure 6, Table 2）：论文进一步证明不平衡加剧了概率校准退化，且边际重平衡的最优 $\tau$ 可最小化平衡错误率。

### 局限与开放问题

论文明确指出其理论主要基于高斯混合模型（2-GMM），对非高斯数据的适用性仅通过t分布实验初步验证。多类分类（$K \geq 3$）的扩展仅给出猜想（联合logit分布渐近为投影到凸多面体的多元高斯），缺乏严格证明。此外，理论仅分析线性探测（linear probing）场景，未涉及端到端深度神经网络的特征学习。校准误差的单调性也仅在 $\pi \leq 0.25$ 时成立，更极端不平衡下的行为未完全刻画。



本文的pipeline围绕“特征提取 → 线性分类 → 边际重平衡”三层结构展开，核心目标是揭示并缓解高维不平衡分类中的过拟合现象。

**特征提取器** 采用预训练深度神经网络（如ResNet-18、BERT base、Llama-3-8B-Instruct），从原始数据（图像、文本、表格）中提取高维特征，并在下游任务中冻结参数（即线性探测模式）。这一设计将分析焦点锁定在最后一层线性分类器的行为上，排除了特征学习带来的干扰。

**线性分类器** 在提取的特征上训练，输出logit并预测类别。论文同时分析了两类标准方法：逻辑回归（Logistic Regression）和支撑向量机（SVM）。在可分离数据上，逻辑回归的梯度下降迭代方向收敛到最大边际解，与硬间隔SVM等价；因此SVM成为理论分析的首选（因其解的定义清晰），而逻辑回归则因其计算效率被用于大规模真实数据分析。

**边际重平衡模块** 是本文提出的核心因果干预模块。它通过一个超参数τ调整少数类和多数类的边际权重，从而改变决策边界。具体地，边际重平衡SVM的优化问题为：

`maximize κ subject to ̃y_i(⟨x_i,β⟩+β_0) ≥ κ, ∀i∈[n], ‖β‖_2 ≤ 1, where ̃y_i = τ·y_i for minority and y_i for majority`

其解与标准SVM（τ=1）的解存在简单的后验调整关系：方向β不变，边界偏移β₀*(τ) = β₀*(1) + (τ-1)/(τ+1)·κ*(1)，边际大小κ*(τ) = 2/(τ+1)·κ*(1)。这一性质使得边际重平衡可以高效实现，无需重新求解优化问题。

**输入输出流** 的因果链条为：原始数据 → 预训练特征提取器（冻结）→ 高维特征向量 → 线性分类器（SVM或逻辑回归）→ logit → 边际重平衡模块（调整τ）→ 最终预测。整个pipeline中，特征提取器是固定的，仅线性分类器的参数受τ影响，这使得论文能够严格分析高维性如何通过截断logit分布来导致过拟合，以及τ如何通过移动少数类边界来缓解这一效应。

**关键瓶颈** 在于：高维特征导致训练集logit分布被截断为rectified Gaussian（max{κ, N(0,1)}），而测试集logit保持高斯分布N(0,1)；这种截断效应在少数类上更严重，因为两类共享一个共同的“过拟合预算”，该预算不成比例地移动了少数类的边界。边际重平衡正是通过调整τ来对齐两类错误率，从而缓解少数类精度下降。



### 数据生成模型

论文采用双成分高斯混合模型（2-GMM）生成训练数据，作为理论分析的基准：

$$\mathbb{P}(y_i = +1) = \pi, \quad \mathbb{P}(y_i = -1) = 1 - \pi, \quad \mathbf{x}_i | y_i \sim \mathsf{N}(y_i \boldsymbol{\mu}, \mathbf{I}_d)$$

其中 $\pi$ 为少数类（正类）的先验概率，$\boldsymbol{\mu} \in \mathbb{R}^d$ 为信号向量，协方差为单位矩阵 $\mathbf{I}_d$。该模型的瓶颈在于：高维特征空间（$d$ 大）使得训练集logit分布被截断，而测试集logit保持高斯分布，这一截断效应在少数类上更严重。

### 线性分类器目标函数

**逻辑回归**的优化问题为：

$$\operatorname*{minimize}_{\beta \in \mathbb{R}^d, \beta_0 \in \mathbb{R}} \quad \frac{1}{n} \sum_{i=1}^n \ell\big(y_i(\langle x_i, \beta\rangle + \beta_0)\big)$$

其中 $\ell$ 为严格凸递减损失函数（如logistic损失）。在可分离数据上，梯度下降迭代的方向收敛到最大边际解。

**硬间隔SVM**的优化问题为：

$$\begin{array}{rl} \mathrm{(SVM)} \quad & \underset{\beta \in \mathbb{R}^d, \beta_0, \kappa \in \mathbb{R}}{\mathrm{maximize}} \quad \kappa, \\ & \mathrm{~subject~to~} \quad y_i(\langle \mathbf{x}_i, \beta\rangle + \beta_0) \geq \kappa, \quad \forall i \in [n], \\ & \|\beta\|_2 \leq 1. \end{array}$$

其中 $\kappa$ 为训练集上的最小边际（margin），$\|\beta\|_2 \leq 1$ 约束保证解的唯一性。在可分离数据上，逻辑回归与SVM在方向上等价。

### 边际重平衡SVM

核心因果旋钮是边际重平衡超参数 $\tau$，通过调整少数类和多数类的边际权重来平衡两类错误率：

$$\operatorname{maximize}_{\beta\in\mathbb{R}^d,\beta_0\in\mathbb{R},\kappa\in\mathbb{R}} \kappa \quad \mathrm{subject\ to} \quad \widetilde{y}_i(\langle{\pmb x}_i,{\pmb\beta}\rangle + \beta_0) \geq \kappa, \forall i\in[n], \quad \|\beta\|_2 \leq 1$$

其中 $\widetilde{y}_i = \tau \cdot y_i$ 对少数类，$\widetilde{y}_i = y_i$ 对多数类。$\tau > 1$ 对少数类施加更大边际。该问题与标准SVM的解存在简单关系（Proposition C.1）：

$$\widehat{\beta}(\tau) = \widehat{\beta}(1), \quad \widehat{\beta}_0(\tau) = \widehat{\beta}_0(1) + \frac{\tau-1}{\tau+1}\widehat{\kappa}(1), \quad \widehat{\kappa}(\tau) = \frac{2}{\tau+1}\widehat{\kappa}(1)$$

即边际重平衡仅通过平移决策边界 $\beta_0$ 和缩放边际 $\kappa$ 来调整，方向 $\beta$ 不变。

### Logit分布的渐近极限

这是论文的核心理论贡献。训练集logit分布（ELD）和测试集logit分布（TLD）的极限分别为：

$$\nu_*^{\mathrm{train}} := \mathtt{Law}\left(Y, Y\operatorname{max}\{\kappa^*, \rho^*\|\mu\|_2 + G + Y\beta_0^*\}\right)$$

$$\nu_*^{\mathrm{test}} := \mathtt{Law}\left(Y, Y(\rho^*\|\pmb{\mu}\|_2 + G + Y\beta_0^*)\right)$$

其中 $G \sim \mathsf{N}(0,1)$ 为标准正态随机变量，$\rho^*$ 和 $\beta_0^*$ 为极限参数，$\kappa^*$ 为极限边际。**关键机制**：TLD保持高斯分布 $\mathsf{N}(\rho^*\|\mu\|_2 + Y\beta_0^*, 1)$，而ELD被截断在 $\kappa^*$ 处（即 $\max\{\kappa^*, \cdot\}$）。这种截断完全解释了高维过拟合现象——训练集logit被"推"到边际边界之外，导致训练误差为零，但测试集logit仍有重叠区域产生正测试误差。

从TLD到ELD的最优传输映射为 $\mathrm{T}^*(x) = \max\{\kappa^*, x\}$（Proposition D.2），揭示了训练集logit分布是测试集logit分布经过截断变换的结果。

### 错误率极限

少数类和多数类的测试错误率渐近极限为：

$$\mathrm{Err}_+ \to \Phi\left(-\rho^*\|\pmb{\mu}\|_2 - \beta_0^*\right), \quad \mathrm{Err}_- \to \Phi\left(-\rho^*\|\pmb{\mu}\|_2 + \beta_0^*\right)$$

其中 $\Phi$ 为标准正态累积分布函数。两类共享一个共同的"过拟合预算"（由 $\rho^*\|\mu\|_2$ 和 $\beta_0^*$ 决定），该预算不成比例地移动少数类的边界，导致少数类错误率随不平衡加剧而趋近1。

### 最优边际比

最小化平衡错误率的最优 $\tau$ 表达式为：

$$\tau^{\mathrm{opt}} = \frac{g_1^{-1}\left( \frac{\rho^*}{2 \pi \|\boldsymbol{\mu}\|_2 \delta} \right) + \rho^* \|\boldsymbol{\mu}\|_2}{g_1^{-1}\left( \frac{\rho^*}{2 (1-\pi) \|\boldsymbol{\mu}\|_2 \delta} \right) + \rho^* \|\boldsymbol{\mu}\|_2}$$

其中 $\delta = n/d$ 为宽高比，$g_1$ 为某单调函数。该公式依赖于渐近极限参数，在实际有限样本下需谨慎使用。

### 误校准指标

论文定义了三种不确定性量化指标：

**校准误差**：$\mathrm{CalErr}(\widehat{p}) := \mathbb{E}\left[\left(\widehat{p}(\mathbf{x}) - \mathbb{P}(y=1|\widehat{p}(\mathbf{x}))\right)^2\right]$

**均方误差（Brier分数）**：$\operatorname{MSE}(\widehat{p}) := \mathbb{E}\left[\left(\mathbb{1}\{y=1\} - \widehat{p}(\mathbf{x})\right)^2\right]$

**置信估计误差**：$\mathrm{ConfErr}(\widehat{p}) := \mathbb{E}\left[\left(\widehat{p}(\mathbf{x}) - p^*(\mathbf{x})\right)^2\right]$

其中 $p^*(\mathbf{x})$ 为贝叶斯最优概率。这些指标在定理4.1中证明关于不平衡比 $\pi$、信号强度 $\|\mu\|_2$ 和宽高比 $\delta$ 单调递减。校准误差的单调性仅在 $\pi \leq 0.25$ 时成立（Claim D.10），更极端的 $\pi$ 行为未完全刻画。

### 高不平衡区间的相变

定理3.2刻画了高不平衡区间（$\pi \asymp d^{-a}, \|\mu\|_2 \asymp d^{b/2}, \delta \asymp d^{-c}$）的三个相：

- **高信号**（$a - c < b$）：无需边际重平衡，两类错误率均趋于0。
- **中等信号**（$b < a - c < 2b$）：边际重平衡至关重要，需 $\tau \gg d^{a-b-c}$ 才能使少数类错误率趋于0；若 $\tau \asymp 1$，则少数类错误率趋近1。
- **低信号**（$a - c > 2b$）：无论 $\tau$ 如何选择，平衡错误率不低于 $1/2$，无法优于随机猜测。



## 实验与关键发现

### 核心发现：logit分布的截断效应

本文的核心实证发现是，在高维线性可分数据上，训练集logit分布（ELD）收敛到**截断高斯分布**，而测试集logit分布（TLD）保持标准高斯分布。具体地，对于SVM（最大边际分类器），训练集logit满足 $y_i \hat{f}(\mathbf{x}_i) \geq \hat{\kappa}_n$，因此ELD的支撑集被截断在边际阈值 $\hat{\kappa}_n$ 处，分布形式为 $\max\{\kappa^*, \rho^*\|\boldsymbol{\mu}\|_2 + G + Y\beta_0^*\}$；而TLD则为无截断的 $\rho^*\|\boldsymbol{\mu}\|_2 + G + Y\beta_0^*$（Theorem 2.1）。这一截断效应直接解释了高维过拟合：训练集上密度被“推”到边际边界右侧（零训练误差），而测试集上密度在决策边界附近存在重叠（正测试误差）。**该截断现象在合成2-GMM数据（Figure 1）、IFNB单细胞RNA-seq表格数据、CIFAR-10图像数据（ResNet-18特征）、IMDb文本数据（BERT特征）中均被复现（Figure 2）**，表明该机制跨越多种数据模态。在Llama-3-8B-Instruct的激活探测中（TruthfulQA数据集），除第一方向截断外，第二方向还出现扭曲效应（Figure 3），暗示LLM内部表征的过拟合更为复杂。

### 不平衡的加剧效应与边际重平衡

截断效应在少数类上更为严重，因为两类共享一个共同的“过拟合预算”（overfitting budget），该预算不成比例地移动了少数类的决策边界。在标准SVM（$\tau=1$）下，随着不平衡比 $\pi$ 减小（少数类比例降低），少数类错误率 $\mathrm{Err}_+$ 趋近1，多数类错误率 $\mathrm{Err}_-$ 趋近0，平衡错误率趋近1/2（Figure 4虚线）。**边际重平衡SVM**通过超参数 $\tau$ 对少数类施加更大边际（$\tilde{y}_i = \tau \cdot y_i$ for minority），其解与标准SVM解存在简单关系（Proposition C.1）：$\hat{\beta}_0(\tau) = \hat{\beta}_0(1) + \frac{\tau-1}{\tau+1} \hat{\kappa}(1)$，$\hat{\kappa}(\tau) = \frac{2}{\tau+1} \hat{\kappa}(1)$。Figure 4实线显示，适当选择 $\tau$ 可显著降低少数类错误率，但以牺牲多数类精度为代价。最优 $\tau^{\mathrm{opt}}$ 由平衡两类错误率的解析表达式给出（Eq. 38），依赖于信号强度、不平衡比和宽高比。

### 相变现象

Theorem 3.2刻画了高不平衡区间的三个相区（Figure 5）：
- **高信号**（$a - c < b$）：任意 $\tau$ 下两类精度均高，无需边际重平衡。
- **中等信号**（$b < a - c < 2b$）：边际重平衡至关重要。若 $\tau_d \gg d^{a-b-c}$，两类精度均高；若 $\tau_d \asymp 1$，少数类精度趋近0。
- **低信号**（$a - c > 2b$）：任意 $\tau$ 下平衡错误率不低于1/2，无法优于随机猜测。

该相变由信号强度 $\|\boldsymbol{\mu}\|_2$、维度 $d$、样本量 $n$ 和边际预算 $\tau$ 的缩放关系决定，为实践中何时需要重平衡提供了理论指导。

### 不确定性量化退化

不平衡不仅恶化分类精度，还严重损害概率校准。Figure 6的可靠性图显示，随着 $\pi$ 减小（不平衡加剧），SVM预测的置信度被系统性高估（预测概率膨胀）。校准误差 $\mathrm{CalErr}(\widehat{p})$ 和均方误差 $\mathrm{MSE}(\widehat{p})$（Brier分数）随不平衡比、信号强度和宽高比增大而单调下降（Table 2, Theorem 4.1），但校准误差的单调性仅在 $\pi \leq 0.25$ 时成立（Claim D.10），更极端不平衡下的行为未被完全刻画。


![[assets/figures/papers/iclr26_0004_cKthi6QfUr_A_Statistical_Theory_of_Overfitting_for_Imbalanc/figures/002_Table_2.jpg]]
*Table 2: Monotonicity of test errors and miscalibration metrics on model parameters*

### 消融与单调性

Table 2总结了测试错误率和误校准指标关于模型参数的单调性：所有指标（$\mathrm{Err}_+^*$、$\mathrm{Err}_-^*$、$\mathrm{Err}_b^*$、$\mathrm{CalErr}^*$、$\mathrm{MSE}^*$）均随不平衡比 $\pi$、信号强度 $\|\boldsymbol{\mu}\|_2$ 和宽高比 $\delta = n/d$ 增大而下降。这表明**数据量越大、信号越强、类别越平衡，过拟合和误校准越轻**。但需注意，该单调性基于高斯混合模型假设，对非高斯数据（如t分布）虽表现出鲁棒性（Figure 16），但实际数据分布可能更复杂。

### 多类扩展

对于 $K \geq 3$ 类，经验logit的联合分布被推测为投影到凸多面体的多元高斯分布（Figure 7）。在3-GMM合成数据和CIFAR-10数据上，联合ELD热图显示高斯密度被多个超平面截断，验证了该猜想的合理性，但严格证明仍为开放问题。

### 失败模式与局限性

1. **非可分离情况**：当 $\delta > \delta_c$（数据不可分）时，过拟合行为通过非线性收缩（nonlinear shrinkage）刻画，但本文主要聚焦可分离情况。
2. **最优τ的有限样本精度**：最优τ表达式依赖于渐近极限，在实际有限样本下可能不精确。
3. **异方差协方差**：当两类协方差不同（$\boldsymbol{\Sigma}_+ \neq \boldsymbol{\Sigma}_-$）时，logit分布出现不同缩放效应，仅给出猜想。
4. **特征学习**：本文仅分析线性探测（linear probing）场景，未考虑端到端深度神经网络的特征学习影响。

### 补充图表

![[assets/figures/papers/iclr26_0004_cKthi6QfUr_A_Statistical_Theory_of_Overfitting_for_Imbalanc/figures/001_Table_1.jpg]]
*Table 1: Qualitative comparison between low/high dimensions for binary classification, where a linear classifier $\hat { y } ( \pmb { x } ) \overset { - } { \underset { - } { = } }$ 2 $\mathbb { 1 } \hat { \{ f ( \pmb { x } ) > 0 \} }$ - 1 with $\hat { f } ( \hat { \pmb x }$ ) = $\langle \pmb { x } _ { \lambda } \hat { \beta } \rangle + \hat { \beta _ { 0 } }$ is trained on $\{ ( \pmb { x } _ { i } , y _ { i } ) \} _ { i = 1 } ^ { n } { \overset { \underset { \mathrm { 1 . 1 . 0 . } } { \mathrm { 1 . 1 . 0 . } } } { \sim } } P _ { \pmb { x } , y }$ . bHere, the logits $\{ { \hat { f } } ( \pmb { x } _ { i } ) \} _ { i = 1 } ^ { n }$ 1 are obtained by evaluating f on the training set

![[assets/figures/papers/iclr26_0004_cKthi6QfUr_A_Statistical_Theory_of_Overfitting_for_Imbalanc/figures/022_Table_3.jpg]]
*Table 3: Comparison of empirical behaviors of logistic regression and SVM on separable data*

![[assets/figures/papers/iclr26_0004_cKthi6QfUr_A_Statistical_Theory_of_Overfitting_for_Imbalanc/figures/046_Table_4.jpg]]
*Table 4: Comparison of logit distributions on separable and non-separable data ( $\tau$ = 1 )*




## 定位与知识库关联

### 与基线方法的关系

本文提出的边际重平衡SVM（Margin-Rebalanced SVM）直接针对标准SVM（τ=1）在高维不平衡分类中的核心失效模式进行修正。标准SVM的瓶颈在于：训练集logit分布收敛为截断高斯（rectified Gaussian）分布，而测试集logit分布保持为高斯分布；这种截断效应完全解释了高维下的过拟合现象。更重要的是，两类共享一个共同的“过拟合预算”，该预算不成比例地移动了少数类的边界，导致少数类错误率随不平衡加剧而趋近1。

边际重平衡通过引入超参数τ（对少数类施加更大边际）来调整两类错误率的平衡。其关键机制是：最优τ可以显式表达为信号强度、宽高比和先验概率的函数（Eq. 38），从而在理论上指导如何选择τ来最小化平衡错误率。这一方法在合成数据（2-GMM）上验证有效：τ>1可显著降低少数类错误率，但以牺牲多数类精度为代价（Figure 4）。

### 适用边界

本文的理论分析基于严格假设：数据来自双成分高斯混合模型（2-GMM），且处于可分离的高维比例极限（n,d→∞, n/d→δ）。在此边界内，理论给出了清晰的相变图景（Theorem 3.2）：
- **高信号**（a-c < b）：无需边际重平衡，两类错误率均可忽略；
- **中等信号**（b < a-c < 2b）：边际重平衡至关重要，否则少数类错误率趋近1；
- **低信号**（a-c > 2b）：任何τ都无法优于随机猜测。

实验验证了该理论在真实数据上的适用性：IFNB单细胞RNA-seq（表格）、CIFAR-10+ResNet-18（图像）、IMDb+BERT（文本）三类数据均复现了ELD的截断高斯形状（Figure 2）。非高斯t分布数据下截断现象仍然存在（Figure 16），表明理论对分布假设具有一定鲁棒性。

### 局限

1. **理论框架的严格限制**：核心分析基于高斯混合模型，对非高斯数据的适用性仅通过t分布实验初步验证，缺乏理论保证。异方差非各向同性协方差（heterogeneous non-isotropic covariance）的扩展仅为猜想。

2. **有限样本下的精度**：最优τ的表达式依赖渐近极限，在实际有限样本下可能不精确。校准误差的单调性仅在π≤0.25时成立，更极端的不平衡行为未完全刻画。

3. **场景覆盖不足**：仅分析线性探测（linear probing）场景，未考虑端到端深度神经网络的特征学习。多类分类（K≥3）的扩展仅给出猜想——经验logit的联合分布渐近为投影到凸多面体的多元高斯，但缺乏严格证明。

4. **公平性权衡**：边际重平衡以牺牲多数类精度换取少数类精度，存在固有的公平性权衡。校准误差随不平衡加剧而恶化（Figure 6），表明少数类的概率预测更不可靠。

### 开放问题

论文留下了若干关键挑战：
- **少数类过拟合的更深层机制**：截断效应解释了现象，但更根本的因果机制仍待探索。
- **特征学习场景的扩展**：如何将理论推广到端到端深度神经网络，特别是模型发现虚假特征（spurious features）的严重不平衡场景。
- **非可分离情况的刻画**：当δ>δ_c时，过拟合行为如何通过非线性收缩（nonlinear shrinkage）刻画？
- **校准退化的理论刻画**：Figure 6中观察到的校准退化能否作为不平衡比π的函数进行精确理论描述？
- **多类分类的严格理论**：对于一般K≥3类，经验logit的联合分布是否渐近为投影到凸多面体的多元高斯？



## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/A_Statistical_Theory_of_Overfitting_for_Imbalanced_Classification.pdf

![[paperPDFs/ICLR_2026/A_Statistical_Theory_of_Overfitting_for_Imbalanced_Classification.pdf]]
