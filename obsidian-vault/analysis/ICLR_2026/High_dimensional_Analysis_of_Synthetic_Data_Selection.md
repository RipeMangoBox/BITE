---
title: "High-dimensional Analysis of Synthetic Data Selection"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/High_dimensional_Analysis_of_Synthetic_Data_Selection.pdf
project_link: null
code_link: null
openreview_forum_id: Y54P2BBPPh
aliases:
- CM
- HDASDS
tags:
- ICLR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/generative_models_and_autoencoders
core_operator: "合成数据的协方差结构（相对于目标分布的协方差）是控制泛化误差的可调节旋钮，匹配协方差即可接近最优性能。"
primary_logic: "在高维线性回归的极限下，最小范数插值器的测试误差仅依赖于训练数据与合成数据的协方差之比，而均值差异的影响渐近消失；因此，通过协方差匹配选择合成数据可以最小化泛化误差。"
claims:
- "在混合训练中，测试误差的确定性等价仅依赖于协方差矩阵Σ_t, Σ_s，与均值μ_t, μ_s无关。"
- "当仅用合成数据训练时，测试误差同时依赖于协方差和均值，突显混合训练中均值无关性的特殊性。"
- "在under-parameterized regime，匹配协方差（Σ_s ∝ Σ_t）是最优的。"
- "在CIFAR-10上，协方差匹配在三种训练范式下均优于所有基线（如DS3），提升约1.2–3.9个百分点。"
---

# High-dimensional Analysis of Synthetic Data Selection

> [!tip] 核心洞察
> 在高维线性回归的极限下，最小范数插值器的测试误差仅依赖于训练数据与合成数据的协方差之比，而均值差异的影响渐近消失；因此，通过协方差匹配选择合成数据可以最小化泛化误差。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 合成数据选择的高维分析 |
| 英文题名 | High-dimensional Analysis of Synthetic Data Selection |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=Y54P2BBPPh) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/generative_models_and_autoencoders |
| Method | Covariance Matching |
| Dataset | CIFAR-10 (StyleGAN2-Ada truncated generators), CIFAR-10 (T2I generative models) |

> [!tip] 效果简介
> - CIFAR-10 (StyleGAN2-Ada truncated generators) 上，Accuracy (Scratch) % 为 54.00 ± 1.89，对比 DS3 52.83 ± 2.19，变化 +1.17。
> - CIFAR-10 (StyleGAN2-Ada truncated generators) 上，Accuracy (Distillation) % 为 59.77 ± 0.61，对比 DS3 55.91 ± 2.80，变化 +3.86。
> - CIFAR-10 (StyleGAN2-Ada truncated generators) 上，Accuracy (Pretrained) % 为 69.20 ± 0.56，对比 DS3 67.13 ± 0.97，变化 +2.07。

## 概要

合成数据已成为缓解真实数据稀缺的重要途径，但盲目扩充合成样本往往引入分布偏移，反而损害模型泛化。本文从高维线性回归的渐近理论出发，系统分析合成数据选择问题：**协方差偏移是控制泛化误差的关键瓶颈，而均值偏移在混合训练中渐近无关紧要**。

核心发现可概括为三条：

1. **均值无关性**：在真实与合成数据混合训练最小范数插值器时，测试误差的确定性等价仅依赖于协方差矩阵 $\Sigma_t, \Sigma_s$，与均值 $\mu_t, \mu_s$ 完全无关（Theorem 4.1）。这一结论在欠参数化和过参数化两种范式下均成立（Theorem 4.1, 4.4）。相比之下，仅用合成数据训练时，风险同时依赖均值和协方差（Proposition 4.2），突显混合训练的特殊性。

2. **协方差匹配即最优**：在约束迹下，最优协方差比的奇异值全为1，即 $\Sigma_s \propto \Sigma_t$（Theorem 4.3）。这为合成数据选择提供了明确的可操作准则——使所选样本的协方差结构尽可能逼近目标分布。

3. **实践有效且鲁棒**：基于上述理论，本文提出**协方差匹配（Covariance Matching）** 选择算法——在真实样本拟合的32维PCA子空间中，以贪心方式逐类最小化所选合成样本协方差与目标协方差的Frobenius距离。在CIFAR-10上，该方法在从头训练、知识蒸馏、预训练微调三种范式下均优于DS3等基线方法，提升幅度约1.2–3.9个百分点（Table 1）；在ImageNet-100、RxRx1等数据集及多种生成模型（StyleGAN、文生图模型）和架构（ResNet、ViT、Swin-T）上同样保持竞争力（Tables 2–4）。消融实验进一步表明，协方差匹配对特征提取器（CLIP/DINO-v2）不敏感，贪心近似与直接优化理论目标的Alpha matching性能相当，且所选样本在FID、KID等分布匹配指标上全面领先（Tables 6–10）。

**方法定位**：协方差匹配区别于以单个样本相似度或聚类多样性为准则的现有方法（如Center matching、DS3），转而从分布的二阶统计量出发，直接优化泛化误差的理论等价形式，属于**理论驱动的分布匹配型选择范式**。其计算流程为：预训练特征提取 → PCA降维 → 贪心协方差匹配 → 下游分类器训练。

**局限与开放问题**：当前理论限于线性模型和高斯假设，向深度非线性模型的推广仍在探索中；选择过程逐类独立，未考虑多类联合优化；此外，在合成数据与真实数据存在模型偏移（$\beta$不同）时，如何扩展协方差匹配准则仍待研究。



### 合成数据在机器学习中的角色与瓶颈

现代机器学习系统越来越多地依赖合成数据来缓解真实数据稀缺、隐私限制或标注成本高昂的问题。合成数据通常由生成模型（如StyleGAN、文生图扩散模型）产生，并被用于增强训练集，以提升下游模型的泛化能力。然而，并非所有合成样本对训练都有同等贡献——低质量或分布偏离的样本可能引入噪声，甚至损害模型性能。

这就引出了一个核心问题：**如何从海量合成数据池中筛选出对下游任务最有价值的子集？** 现有的数据选择方法大多基于个体样本的质量评估，例如利用CLIP相似度修剪低质量样本的**Center matching**（He et al., 2023）、基于聚类增强多样性的**K-means**（Lin et al., 2023），或通过聚类嵌入多样性进行选择的**DS3**（Hulkund et al., 2025）。这些方法的共同缺陷在于：它们缺乏对合成数据分布与目标分布之间**系统性偏移**的理论理解，因而无法从本质上回答“什么样的合成数据能最小化泛化误差”。

### 现有方法的缺口：从样本级筛选到分布级匹配

上述基线方法隐含地假设：只要挑选出“看起来好”的个体样本，组合起来就能构成好的训练集。但这一假设忽略了**协方差结构**在统计学习中的关键作用。在高维线性回归的框架下，训练数据的协方差矩阵直接决定了最小范数插值器的泛化行为。如果所选合成样本的协方差与目标分布存在显著偏移，即使每个样本单独看起来质量很高，整体训练集仍可能导致次优的泛化性能。

本文正是从这一缺口出发，将合成数据选择问题从“样本级质量筛选”提升到“分布级协方差匹配”的层面。

### 核心动机：协方差偏移是泛化误差的关键旋钮

本文的理论分析揭示了一个简洁而深刻的结论：在真实数据与合成数据混合训练的高维线性模型中，**测试误差的渐近行为仅依赖于合成数据与真实数据的协方差之比，而与均值差异渐近无关**。具体而言：

- 在欠参数化（$n > p$）和过参数化（$n < p$）两种机制下，最小范数最小二乘估计器的条件测试误差均收敛到一个确定性等价量，该量仅由协方差矩阵 $\Sigma_t$、$\Sigma_s$ 以及样本比例决定（Theorem 4.1, Theorem 4.4）。
- 均值 $\mu_t$、$\mu_s$ 在混合训练的渐近极限中**完全消失**。这一结论在仅用合成数据训练时并不成立——此时风险同时依赖于均值和协方差（Proposition 4.2），从而凸显了混合训练场景下均值无关性的特殊性。

基于这一理论洞察，合成数据选择问题被归约为一个关于协方差 $\Sigma_s$ 的优化问题：**匹配协方差（$\Sigma_s \propto \Sigma_t$）是在约束迹下的最优策略**（Theorem 4.3, Theorem 4.5）。换言之，协方差结构是控制泛化误差的可调节“旋钮”——旋紧它（使合成协方差逼近目标协方差），即可接近最优性能。

### 方法概览与实证动机

基于上述理论，本文提出了**协方差匹配（Covariance Matching）** 方法：在预训练视觉模型提取的特征空间中，通过贪心算法逐类选择合成样本，使所选子集的协方差矩阵在Frobenius范数下逼近目标分布的协方差。该方法在CIFAR-10、ImageNet-100、RxRx1等多个基准上，跨越从零训练、知识蒸馏到预训练微调三种训练范式，一致地优于或持平于所有基线方法（Table 1–3），提升幅度达1.2–3.9个百分点。更重要的是，协方差匹配对特征提取器（CLIP或DINO-v2）、生成模型类型（StyleGAN或文生图模型）以及下游架构（ResNet或Transformer）均表现出鲁棒性，验证了其作为通用选择原则的有效性。



## 核心方法与创新机理

本文的核心创新在于将合成数据选择问题从传统的“样本级质量评估”范式转向“分布级结构匹配”范式。其关键洞察源于高维线性回归的渐近分析：当真实数据与合成数据混合训练最小范数插值器时，测试误差的确定性等价仅依赖于协方差矩阵 $\Sigma_t$ 与 $\Sigma_s$，而与均值 $\mu_t, \mu_s$ 无关（Theorem 4.1, 4.4）。这一发现揭示了一个反直觉的结论——合成数据的**协方差结构**是控制泛化误差的可调节旋钮，而均值偏移在混合训练中渐近无关紧要。

基于此理论，论文提出了 **Covariance Matching（协方差匹配）** 选择策略，其核心 changed slots 如下：

### 选择准则：从样本评分到协方差对齐

现有方法普遍采用**样本级评分机制**：Center matching（He et al., 2023）基于 CLIP 相似度修剪低质量样本，Center sampling / Text sampling（Lin et al., 2023）按相似度采样，DS3（Hulkund et al., 2025）通过聚类嵌入度量多样性，K-means（Lin et al., 2023）以聚类增强覆盖。这些方法的共同局限在于孤立地评估每个样本，无法显式控制所选子集的整体分布结构。

Covariance Matching 将选择准则替换为**分布级协方差对齐**：贪婪地最小化所选合成样本的协方差与目标协方差之间的 Frobenius 距离：

$$\min_{x} \|\hat{\Sigma}(\mathcal{S} \cup \{x\}) - \hat{\Sigma}_t\|_F$$

该目标直接编码了理论最优条件——当 $\Sigma_s \propto \Sigma_t$ 时，风险函数的奇异值全为 1，泛化误差达到下界（Theorem 4.3, 4.5）。实验验证了这一准则的有效性：在 CIFAR-10 上，协方差匹配在三种训练范式下均优于所有基线，相比最强的 DS3 提升约 1.2–3.9 个百分点（Table 1）；在 ImageNet-100 和 RxRx1 上同样保持竞争力（Table 3）。

### 特征表示：PCA 降维加速

基线方法通常在完整的高维特征空间（如 512 维 CLIP 或 DINO 特征）中操作。Covariance Matching 引入了一个关键的工程优化：在真实参考特征上拟合 **32 维 PCA 子空间**，将协方差计算和匹配过程投影到低维流形中。这一设计既保留了数据的主要变化方向，又显著降低了贪婪选择中协方差矩阵估计的计算开销（从 $\mathcal{O}(p^2)$ 降至 $\mathcal{O}(32^2)$）。

### 理论贡献：均值无关性的严格证明

与仅用合成数据训练时风险同时依赖均值和协方差（Proposition 4.2）形成鲜明对比，本文在欠参数化（Theorem 4.1）和过参数化（Theorem 4.4）两种 regime 下严格证明了混合训练中均值差异的渐近消失。这一结论通过合成实验得到验证：改变训练数据与合成数据的均值余弦相似度，超额风险保持不变（Figure 1a）。该发现从根本上挑战了“合成数据应尽可能逼近真实数据的所有分布矩”的直觉，将优化焦点精确锁定在协方差结构上。

### 方法谱系定位

Covariance Matching 在合成数据选择的方法谱系中开辟了一条新路径：它不是对现有样本评分方法的改进，而是将选择问题重新表述为**协方差子集的组合优化**。与 Alpha matching（直接优化 Theorem 4.1 的理论目标）的性能相当（Table 8），证明贪婪近似有效地捕获了理论最优解的本质特征。该方法对特征提取器（CLIP/DINO-v2）和生成模型（StyleGAN/T2I）均表现出鲁棒性（Tables 6–7），表明协方差匹配原则具有跨模态和跨架构的泛化能力。



本文提出了一种基于协方差匹配的合成数据选择方法，其整体流程由四个核心模块串联构成：**预训练特征提取**、**PCA降维与投影**、**贪婪协方差匹配**、以及**下游分类器训练**。各模块的输入输出关系与设计动机如下。

### 模块一：预训练特征提取

给定一个真实训练集（目标分布）和一个由生成模型（如截断的 StyleGAN2-Ada 或多种文生图模型）产生的合成样本池，首先使用预训练的视觉模型将每张图像映射为嵌入向量。默认特征提取器为 **CLIP ViT-B/16**，消融实验表明替换为 **DINO-v2** 后结论不变（Table 6–7）。该模块的输出是真实特征矩阵与合成特征矩阵，分别记为 $\hat{X}_t$ 与 $\hat{X}_s$。

### 模块二：PCA降维与投影

为降低后续协方差计算与贪婪搜索的开销，在真实参考特征上拟合一个 32 维的 PCA 子空间，并将所有真实与合成特征投影至此子空间。这一步保留了数据的主要变化方向，使得协方差矩阵的规模从原始特征维度（如 512 维）降至 $32 \times 32$，从而显著加速选择过程。

### 模块三：贪婪协方差匹配

这是整个方法的核心选择引擎。对于每一类别独立执行以下贪心过程：

1. 初始化已选集合 $\mathcal{S} = \emptyset$。
2. 在每一步，从该类别的合成样本池中选取一个样本 $x$，使得加入 $\mathcal{S}$ 后的样本协方差与目标协方差（由真实样本估计）之间的 Frobenius 距离最小：
   $$\min_{x} \|\hat{\Sigma}(\mathcal{S} \cup \{x\}) - \hat{\Sigma}_t\|_F$$
3. 重复步骤 2，直至 $|\mathcal{S}| = n_s$（预设的合成样本数量）。

该贪心算法的理论依据来自高维线性回归的渐近分析：在混合训练（真实+合成）的欠参数化与过参数化情形下，最小范数插值器的测试误差仅依赖于训练协方差 $\Sigma_t$ 与合成协方差 $\Sigma_s$，而与均值 $\mu_t, \mu_s$ 无关（Theorem 4.1, Theorem 4.4）。因此，选择合成数据的问题可归结为对 $\Sigma_s$ 的优化，而最优解正是 $\Sigma_s \propto \Sigma_t$（Theorem 4.3, Theorem 4.5）。贪心匹配通过逐样本最小化协方差距离来逼近这一理论最优条件。

### 模块四：下游分类器训练

将选定的 $n_t$ 个真实样本与 $n_s$ 个合成样本合并，形成增强训练集 $(X_t \cup X_s, y_t \cup y_s)$。在此增强集上训练下游分类模型，覆盖三种训练范式：

- **从头训练（Scratch）**：随机初始化 ResNet-18 或 ViT 并完整训练。
- **蒸馏（Distillation）**：以更大模型的预测作为软标签进行训练。
- **预训练微调（Pretrained）**：在 ImageNet 预训练权重上微调线性分类头。

### 输入输出流总览

| 阶段 | 输入 | 输出 |
|------|------|------|
| 特征提取 | 真实图像、合成图像池 | 真实特征 $\hat{X}_t$、合成特征 $\hat{X}_s$ |
| PCA降维 | $\hat{X}_t$, $\hat{X}_s$ | 32维投影特征 |
| 协方差匹配 | 投影特征、目标样本数 $n_s$ | 选定的合成样本索引集 $\mathcal{S}$ |
| 分类器训练 | $X_t \cup X_{\mathcal{S}}$ | 训练好的分类模型 |

该框架的关键设计决策在于**选择准则的替换**：传统方法依赖个体样本的 CLIP 相似度或聚类多样性评分（如 DS3 的簇嵌入多样性），而本文方法将选择准则替换为**集合级别的协方差匹配**，从而在理论上保证了泛化误差的最优性。实验表明，这一框架对生成模型类型（StyleGAN、T2I、MorphGen）、特征提取器（CLIP/DINO）、数据集（CIFAR-10、ImageNet-100、RxRx1）和下游架构（ResNet、ViT、Swin-T）均具有鲁棒性。



### 问题建模：线性高维回归框架

论文将合成数据增强训练建模为一个高维线性回归问题。真实训练数据 $(X_t, y_t)$ 和合成数据 $(X_s, y_s)$ 共享同一回归系数 $\beta$：

$$y_{(i)} = X_{(i)} \beta + \varepsilon_{(i)}, \quad (i) \in \{t, s\}$$

其中 $\varepsilon_{(i)}$ 为独立同分布噪声，方差为 $\sigma^2$。特征矩阵的生成过程为：

$$X_{(i)} = Z^{(i)} (\Sigma_{(i)})^{1/2} + \mathbf{1}_{n_{(i)}} \mu_{(i)}^\top$$

这里 $Z^{(i)}$ 的各元素独立同分布，$\Sigma_{(i)}$ 和 $\mu_{(i)}$ 分别控制第 $i$ 类数据的协方差结构和均值。这一分解将分布偏移明确地参数化为**协方差偏移**（$\Sigma_s \neq \Sigma_t$）和**均值偏移**（$\mu_s \neq \mu_t$）两个可分离的维度。

### 估计器：最小范数插值

模型采用最小 $\ell_2$ 范数最小二乘估计器，对应从零初始化梯度下降的收敛解：

$$\hat{\beta} = \operatorname{argmin}\{\|\beta\|_2 : \beta \text{ minimizes } \|y - X b\|_2^2\} = (X^\top X)^+ X^\top y$$

其中 $X = [X_t; X_s]$ 和 $y = [y_t; y_s]$ 为拼接后的增广数据集，$(\cdot)^+$ 表示 Moore-Penrose 伪逆。

### 泛化误差分解：偏差-方差结构

在测试分布（以 $\Sigma_t, \mu_t$ 为特征的分布）上，超额风险可精确分解为偏差项和方差项：

$$R_X(\hat{\beta}; \beta) = \|\mathbb{E}[\hat{\beta} \mid X] - \beta\|_{\Sigma_t + \mu_t \mu_t^\top}^2 + \operatorname{Tr}[\operatorname{Cov}(\hat{\beta} \mid X)(\Sigma_t + \mu_t \mu_t^\top)]$$

权重矩阵 $\Sigma_t + \mu_t \mu_t^\top$ 是测试分布的二阶矩，它同时惩罚偏差和方差。这一分解是后续所有渐近分析的基础。

### 核心理论结果：均值无关性与协方差决定论

**欠参数化情形**（$n > p$，Theorem 4.1）：当同时使用真实和合成数据训练时，测试误差的确定性等价仅依赖于协方差矩阵：

$$\lim_{n \to \infty} \left| R_X(\hat{\beta}; \beta) - \frac{\sigma^2}{n} \operatorname{Tr}\left[\left(\alpha_1 M^\top M + \alpha_2 I_p\right)^{-1}\right] \right| = 0$$

其中 $M = \Sigma_s^{1/2} \Sigma_t^{-1/2}$ 是协方差比矩阵，$\alpha_1, \alpha_2$ 由样本比例和 $M$ 的谱通过固定点方程确定。**关键洞察**：该极限与均值 $\mu_t, \mu_s$ 完全无关。

**仅合成数据训练**（Proposition 4.2）：作为对比，当仅用合成数据训练时，风险同时依赖于协方差和均值：

$$\lim_{n \to \infty} \left| R_X(\hat{\beta}; \beta) - \frac{\sigma^2}{n} \frac{\gamma}{\gamma-1} \left[ \operatorname{Tr}[\Sigma_t \Sigma_s^{-1}] + \|\Sigma_s^{-1/2} \mu_t\|_2^2 - \left( \frac{\mu_t^\top \Sigma_s^{-1} \mu_s}{\|\Sigma_s^{-1/2} \mu_s\|_2} \right)^2 \right] \right| = 0$$

这一对比凸显了混合训练中均值无关性的特殊性——真实样本的存在使得均值偏移的影响被渐近消除。

**过参数化情形**（$n < p$，Theorem 4.4）：在同时对角化假设下，风险收敛到方差项 $\mathcal{V}(\Sigma_s, \Sigma_t)$ 和偏差项 $\mathcal{B}(\Sigma_s, \Sigma_t, \beta)$ 之和，两者均通过谱分布和固定点方程依赖于 $\Sigma_s, \Sigma_t$，仍与均值无关：

$$\lim_{n \to \infty} \left| R_X(\hat{\beta}; \beta) - \mathcal{V}(\Sigma_s, \Sigma_t) - \mathcal{B}(\Sigma_s, \Sigma_t, \beta) \right| = 0$$

### 协方差匹配的最优性条件

基于上述理论，合成数据选择问题被归约为对协方差 $\Sigma_s$ 的优化。在迹约束下，风险函数 $\mathcal{R}_u(M)$ 的最小化条件为：

$$\lambda_i(M_{\text{opt}}^\top M_{\text{opt}}) = 1, \quad \forall i \in \{1,\dots,p\}$$

即最优协方差比的奇异值全为 1，等价于 $\Sigma_s \propto \Sigma_t$——**协方差匹配**。此外，对于任意满秩 $M$ 和缩放因子 $\eta > 1$，有 $\mathcal{R}_u(\eta M) \leq \mathcal{R}_u(M)$，表明合成数据协方差的**尺度放大**（增加多样性）可进一步降低风险。

### 贪心协方差匹配算法

实践中，协方差匹配通过贪心算法实现。给定真实参考特征集（用于估计目标协方差 $\hat{\Sigma}_t$）和合成样本池，每次选择使当前已选样本协方差与目标协方差 Frobenius 距离最小的样本：

$$\min_{x} \|\hat{\Sigma}(\mathcal{S} \cup \{x\}) - \hat{\Sigma}_t\|_F$$

算法按类别独立执行：初始化空集 $\mathcal{S}$，迭代添加样本直至达到预设数量 $n_s$。为加速计算，协方差在真实特征拟合的 32 维 PCA 子空间中计算，有效降低了高维特征（如 CLIP ViT-B/16 的 512 维）带来的计算开销，同时保留了主要变化方向。



## 实验与关键发现

### 核心实验设置

实验围绕三个训练范式展开：**从头训练（Scratch）**、**知识蒸馏（Distillation）** 和 **预训练线性探测（Pretrained）**。合成数据由多种生成模型产生，包括截断的 StyleGAN2-Ada、StyleGAN-XL 以及文生图（T2I）扩散模型。协方差匹配在真实参考特征上拟合的 32 维 PCA 子空间中执行贪心选择，特征提取器默认使用 CLIP ViT-B/16，消融中替换为 DINO-v2。下游分类器以 ResNet-18 为主，架构消融中扩展至 ViT 和 Swin-T。

### 主结果：CIFAR-10 上的全面优势

**Table 1** 汇总了使用五个截断 StyleGAN2-Ada 模型生成合成数据时，协方差匹配在三种训练范式下均显著优于所有基线方法：


![[assets/figures/papers/paper_list_l23_https_openreview_net_forum_id_Y54P2BBPPh/figures/004_Table_1.jpg]]
*Table 1: Covariance matching outperforms all baselines across three training paradigms on CIFAR-10, when the synthetic data is generated via five truncated StyleGAN2-Ada models*

- **Scratch**：协方差匹配达到 54.00 ± 1.89%，较最强基线 DS3（52.83 ± 2.19%）提升 **+1.17 个百分点**。
- **Distillation**：协方差匹配 59.77 ± 0.61%，较 DS3（55.91 ± 2.80%）提升 **+3.86 个百分点**，优势最为突出。
- **Pretrained**：协方差匹配 69.20 ± 0.56%，较 DS3（67.13 ± 0.97%）提升 **+2.07 个百分点**。

这一结果直接验证了理论核心洞察：**匹配协方差可最小化泛化误差**。值得注意的是，协方差匹配倾向于从高截断（truncation=0.6）的生成器中选取更多样本（分别选取 3692 和 3462 个），而从低截断（0.2）的生成器中仅选取 268、245、333 个样本，表明该方法天然偏好多样性更高的合成样本。

**Table 2** 将场景切换至多种 T2I 生成模型，协方差匹配的 Scratch 精度为 54.45 ± 2.11%，与最佳基线持平（DS3 为 52.94 ± 2.52%，提升 +1.51 个百分点），证明该方法对生成源类型具有鲁棒性。


![[assets/figures/papers/paper_list_l23_https_openreview_net_forum_id_Y54P2BBPPh/figures/005_Table_2.jpg]]
*Table 2: Covariance matching performs on par with the best baseline across three training paradigms on CIFAR-10, when the synthetic data is generated via various T2I generative models*

### 跨数据集与跨架构泛化

**Table 3** 将实验扩展到更大规模场景：


![[assets/figures/papers/paper_list_l23_https_openreview_net_forum_id_Y54P2BBPPh/figures/006_Table_3.jpg]]
*Table 3: Covariance matching performs on par with the best baselines for two additional datasets. In (a), we train a ResNet-18 from scratch on ImageNet-100 with synthetic images from StyleGAN-XL and T2I models. In (b), we train a linear model on top of an ImageNet-pretrained ResNet for perturbation classification on a small subset of RxRx1 (Sypetkowski et al., 2023) augmented with synthetic images from MorphGen (Demirel et al., 2025). (a) ImageNet-100 dataset*

- **ImageNet-100 + StyleGAN-XL**：协方差匹配 Scratch 精度 57.52 ± 0.36%，较 DS3（56.61 ± 0.56%）提升 +0.91 个百分点。
- **ImageNet-100 + T2I**：53.07 ± 0.89%，与最佳基线持平。
- **RxRx1 + MorphGen**：线性探测精度 90.00 ± 1.86%，保持竞争力。

**Table 4** 进一步验证了协方差匹配在 Transformer 架构（ViT、Swin-T）上的有效性，表明该方法不依赖于特定的卷积架构设计。


![[assets/figures/papers/paper_list_l23_https_openreview_net_forum_id_Y54P2BBPPh/figures/007_Table_4.jpg]]
*Table 4: Covariance matching outperforms all baselines when fully training a transformer model on a mix of real and synthetic data*

### 关键消融实验

**特征提取器不敏感性**（Table 6–7）：将 CLIP 特征替换为 DINO-v2 后，协方差匹配的优势保持不变。在截断生成器场景下，三种训练范式的精度分别为 55.30 ± 1.45%、58.35 ± 0.93%、69.78 ± 0.32%，均优于所有基线。这表明协方差匹配的核心机制——分布二阶矩对齐——对特征空间的选择具有鲁棒性。



![[assets/figures/papers/paper_list_l23_https_openreview_net_forum_id_Y54P2BBPPh/figures/011_Table_7.jpg]]
*Table 7: Covariance matching performs on par with the best baseline across three training paradigms on CIFAR-10, when the synthetic data is generated via text-to-image (T2I) generative models and features are extracted with DINO-v2. matching. As in Covariance matching, we first fit PCA on the real samples and project all features, then iteratively add the sample that yields the smallest value of (4.1). Without loss of generality, we drop the noise variance term since it scales all candidates equally. The results of Table 8 show that Alpha matching performs similarly to Covariance matching*

![[assets/figures/papers/paper_list_l23_https_openreview_net_forum_id_Y54P2BBPPh/figures/010_Table_6.jpg]]
*Table 6: Covariance matching outperforms all baselines across three training paradigms on CIFAR-10, when the synthetic data is generated via truncated generative models and features are extracted with DINO-v2*

**理论目标的有效近似**（Table 8）：比较贪心协方差匹配与直接优化 Theorem 4.1 目标的 Alpha matching，两者性能相当（Scratch 54.00 vs 54.14，Distillation 59.77 vs 59.58，Pretrained 69.20 vs 68.62），证明贪心近似是理论最优解的高效替代方案。


![[assets/figures/papers/paper_list_l23_https_openreview_net_forum_id_Y54P2BBPPh/figures/012_Table_8.jpg]]
*Table 8: Covariance matching performs on par with Alpha matching across the experiments on CIFAR-10. Over-parameterized setting. We repeat the setup of Table 1 taking n _ { s } = 2 0 0 (instead of n _ { s } = 8 0 0 ) This gives a total of n _ { s } + n _ { t } = 4 0 0 samples, which is less than the number of features p = 5 1 2 . , thus placing us in an over-parameterized regime. As shown in Table 9, the quantitative trends mirror those in the under-parameterized case*

**过参数化设置**（Table 9）：当训练样本和合成样本各仅 200 个（总计 400 < 模型参数量）时，协方差匹配在 Scratch（43.92 ± 1.73% vs DS3 42.50 ± 1.57%）、Distillation（50.18 ± 1.73% vs DS3 47.97 ± 1.32%）和 Pretrained（62.92 ± 1.09% vs DS3 61.40 ± 0.94%）三种范式下均保持领先，验证了 Theorem 4.4 在过参数化情形的理论预测。


![[assets/figures/papers/paper_list_l23_https_openreview_net_forum_id_Y54P2BBPPh/figures/013_Table_9.jpg]]
*Table 9: Covariance matching outperforms all baselines across three training paradigms on CIFAR-10, when the synthetic data is generated via truncated StyleGAN2-Ada models (Karras et al., 2019) in the over-parameterized regime with 200 training and 200 augmenting synthetic samples*

**分布匹配质量**（Table 10）：协方差匹配所选样本在 FID（42.53 vs DS3 47.36）、KID（0.033 vs 0.040）和协方差偏移（0.047 vs 0.068）等指标上全面优于其他方法，Recall 也最高（0.58 vs 0.55），从分布层面解释了分类性能提升的根源。


![[assets/figures/papers/paper_list_l23_https_openreview_net_forum_id_Y54P2BBPPh/figures/014_Table_10.jpg]]
*Table 10: Covariance matching selects samples that better match the target distribution according to various evaluation metrics*

**样本量鲁棒性**（Table 11）：变动真实与合成样本数量时，协方差匹配始终保持优势，表明方法对数据规模变化不敏感。


![[assets/figures/papers/paper_list_l23_https_openreview_net_forum_id_Y54P2BBPPh/figures/015_Table_11.jpg]]
*Table 11: An ablation on the size of the real and synthetic datasets used for training shows results consistent with those reported in Table 1*

**选择策略变体**（Table 12）：前瞻搜索（look-ahead, k=50/100）和匈牙利算法与贪心协方差匹配性能相当，说明贪心策略已足够逼近全局最优。

**零多样性生成器**（Table 5）：当生成器多样性极低时，协方差匹配与最佳基线持平，未出现性能崩塌，但优势缩小——这符合理论预期：当合成池本身缺乏多样性时，协方差匹配的选择空间受限。


![[assets/figures/papers/paper_list_l23_https_openreview_net_forum_id_Y54P2BBPPh/figures/008_Table_5.jpg]]
*Table 5: Covariance matching performs on par with the best baselines across three training paradigms on CIFAR-10, when the synthetic data is generated via a StyleGAN2-Ada model and two zerodiversity generators*

**跨模态验证**（Table 13）：在文本分类任务（讽刺推文检测）上，协方差匹配同样优于所有基线，暗示该原则可能适用于更广泛的模态。

### 泄露实验：选择机制的直观验证

**Figure 2** 设计了一个诊断性实验：将真实分布图像混入合成样本池中，测试各方法选择真实样本的比例。协方差匹配最高效地从混合池中挑选出真实分布图像，证明其选择机制确实倾向于匹配目标分布，而非仅仅挑选“看起来好”的个体样本。这一结果与理论中“均值无关、协方差决定泛化”的结论高度一致。


![[assets/figures/papers/paper_list_l23_https_openreview_net_forum_id_Y54P2BBPPh/figures/009_Figure_2.jpg]]
*Figure 2: The portion of samples chosen from the set of leaked images shows that our proposed algorithm reliably selects real samples among the pool of generated examples*

### 失败模式与局限

实验揭示了几个值得注意的边界条件：

1. **生成器多样性依赖**：Table 5 显示，当生成器多样性极低时，协方差匹配的优势缩小至与基线持平。这是因为选择池本身缺乏足够的协方差变化空间，优化目标退化为在贫瘠空间中做无差别选择。
2. **T2I 场景优势收窄**：Table 2 中协方差匹配虽优于多数基线，但与最佳基线的差距较 StyleGAN 场景缩小，可能源于 T2I 生成样本的协方差结构本身更接近真实分布，留给协方差匹配的优化余地更小。
3. **逐类独立选择的局限**：当前方法在每个类别内独立执行协方差匹配，未考虑类别间的联合优化。在多类别边界模糊的场景下，这可能不是全局最优策略。


## 定位与知识库关联

### 核心思想与理论根基

本文的核心贡献在于将“合成数据选择”这一经验性问题形式化为一个可优化的协方差匹配问题。作者从高维线性回归的渐近理论出发，证明了一个关键结论：在混合训练（真实数据+合成数据）的极限下，最小范数插值器的测试误差仅依赖于训练数据与合成数据的协方差之比，而均值差异的影响渐近消失。这一发现将选择问题从“哪些样本更好”的启发式判断，转化为“如何让所选样本的协方差逼近目标协方差”的确定性优化目标。

理论分析在两个关键区域均给出了刻画：
- **欠参数化区域**（Theorem 4.1）：测试误差的确定性等价仅通过矩阵 $M = \Sigma_s^{1/2} \Sigma_t^{-1/2}$ 依赖于协方差，与均值无关。
- **过参数化区域**（Theorem 4.4）：风险分解为方差项 $\mathcal{V}(\Sigma_s, \Sigma_t)$ 和偏差项 $\mathcal{B}(\Sigma_s, \Sigma_t, \beta)$，同样仅依赖于协方差和回归系数，与均值无关。

基于此，最优选择条件被精确刻画为 $\Sigma_s \propto \Sigma_t$，即协方差匹配（Theorem 4.3, 4.5）。这一理论洞见构成了后续所有实验设计的可调节旋钮。

### 与基线方法的本质差异

现有合成数据选择方法大多基于个体样本的质量或多样性评估，可归纳为以下几类范式：

- **相似度驱动选择**：**Center matching**（He et al., 2023）和 **Center sampling**（Lin et al., 2023）利用CLIP特征空间中的余弦相似度来修剪或采样合成样本，其隐含假设是“与类中心越近的样本越有用”。这种方法忽略了样本间的协方差结构，倾向于选择高度集中的样本，牺牲了多样性。
- **多样性增强选择**：**K-means**（Lin et al., 2023）通过聚类来保证所选样本覆盖不同的特征区域，**DS3**（Hulkund et al., 2025）则利用聚类嵌入的多样性度量进行选择。这些方法试图显式地提升多样性，但缺乏对“何种多样性结构最优”的理论指导。
- **文本引导选择**：**Text matching** 和 **Text sampling**（Lin et al., 2023）借助文本提示的相似度进行筛选，适用于文生图场景，但依赖提示质量且与下游训练目标脱节。

本文提出的**协方差匹配**与上述方法的根本区别在于：它不是评估单个样本的“好坏”，而是评估所选子集的**整体分布属性**与目标分布的匹配程度。具体而言，其选择准则为最小化所选合成样本的协方差与目标协方差之间的Frobenius距离：

$$\min_{x} \|\hat{\Sigma}(\mathcal{S} \cup \{x\}) - \hat{\Sigma}_t\|_F$$

这一准则直接由理论推导得出，而非经验性设计。实验证据表明，这种分布级匹配策略在多个维度上优于样本级策略：协方差匹配选择的样本在FID、KID、协方差偏移等分布匹配指标上全面优于其他方法（Table 10），且在泄露实验中最高效地从合成池中挑选出真实分布图像（Figure 2）。

### 方法变体与理论近似验证

为验证贪心协方差匹配是否有效逼近理论最优解，作者设计了**Alpha matching**——直接优化定理4.1中的渐近风险目标函数。实验表明，两者性能相当（Table 8），证明贪心近似是理论目标的有效实现。

在选择算法层面，作者还比较了前瞻搜索（look-ahead with $k \in \{50, 100\}$）和匈牙利算法等变体，发现它们与贪心协方差匹配效果相当（Table 12）。这表明，在协方差匹配这一准则下，选择算法的具体实现形式并非性能瓶颈，关键在于准则本身的正确定义。

### 适用边界与关键假设

该方法的高效性建立在一系列假设之上，理解这些边界对于正确使用和推广至关重要：

1. **线性模型假设**：理论分析严格限定在线性回归和高斯混合假设下。向非线性深度模型的推广目前仅通过实验验证（在ResNet-18、ViT、Swin-T上均有效），但缺乏理论保证。这是该方法谱系中最关键的开放性缺口。

2. **无模型偏移假设**：理论推导假设合成数据与真实数据共享相同的回归系数 $\beta$，即不存在模型偏移（model shift）。当合成数据的条件标签分布与真实数据不同时，协方差匹配的最优性可能不再成立。

3. **逐类独立操作**：协方差匹配在每一类内部独立执行，未考虑多类之间的交互与联合优化。在多类别高斯混合模型下，逐类匹配协方差未必等价于联合优化整体风险，这构成了一个明确的理论开放问题。

4. **特征提取器依赖**：实验中的协方差计算依赖预训练视觉模型（CLIP ViT-B/16或DINO-v2）提取的特征。消融实验表明该方法对特征提取器不敏感（Tables 6-7），但特征空间的质量仍会间接影响选择效果。在零多样性生成器场景下，协方差匹配倾向于选择更多样化的生成模型输出，避免选择崩塌样本（Table 5），这进一步说明该方法依赖于生成池中存在足够的多样性。

5. **计算开销**：贪心协方差匹配的复杂度略高于简单的相似度筛选方法。作者通过将特征投影到32维PCA子空间来加速计算，在大规模样本池中可能需要进一步优化。

### 开放问题与未来方向

基于上述分析，以下几个方向值得进一步探索：

- **多类联合优化**：如何将协方差匹配原则从逐类独立操作扩展到多类别联合优化，使选择策略直接最小化整体分类风险而非各类独立匹配？
- **模型偏移下的鲁棒选择**：当合成数据与真实数据的条件分布存在偏移时，如何结合协方差偏移和均值偏移设计最优选择策略？Proposition 4.2已揭示了仅用合成数据训练时均值依赖性的存在，这为模型偏移场景提供了分析起点。
- **非线性推广**：理论结果是否可以推广到深度网络的特征空间中？高维随机特征或神经正切核（NTK）框架可能是连接线性理论与深度实践的桥梁。
- **跨领域应用**：协方差匹配的核心思想——通过匹配二阶统计量来优化分布级选择——是否可应用于差分隐私合成数据筛选、因果推断中的预测驱动推断、或持续学习中的数据重放策略？
- **全局优化算法**：能否设计比贪心匹配更高效的全局优化算法（如基于行列式点过程或次模优化的方法），在保持或提升性能的同时降低计算复杂度？



## 原文 PDF

![[paperPDFs/ICLR_2026/High_dimensional_Analysis_of_Synthetic_Data_Selection.pdf]]
