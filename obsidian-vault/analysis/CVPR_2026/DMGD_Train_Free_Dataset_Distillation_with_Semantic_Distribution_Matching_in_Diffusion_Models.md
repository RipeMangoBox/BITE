---
title: "DMGD: Train-Free Dataset Distillation with Semantic-Distribution Matching in Diffusion Models"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/DMGD_Train_Free_Dataset_Distillation_with_Semantic_Distribution_Matching_in_Diffusion_Models.pdf
project_link: null
code_link: "https://github.com/solomonWQC/DMGD"
aliases:
- DDMGD
- DMGD
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
- topic/benchmarks_datasets_evaluation
core_operator: 解耦语义匹配与分布匹配，并在扩散采样过程中引入动态软标签引导和最优传输分布对齐，无需任何额外训练即可同时提升多样性与分布对齐。
primary_logic: 在语义对齐的前提下，替代数据集与原始数据集之间的最优传输距离是风险差异的上界；因此，通过无训练的引导优化语义匹配（动态软标签）和分布匹配（最优传输损失），就能有效蒸馏大规模数据集。
claims:
- 提出的 DMGD 框架在 ImageNet-Woof、ImageNet-Nette 和 ImageNet-1K 上无需微调即达到 SOTA，平均精度提升分别为 2.1%、5.4% 和 2.4%。
- 定理 1 证明在语语义对齐下，风险差异由最优传输距离界定，为解耦的两个目标提供了理论依据。
- 动态软标签引导能够在不破坏语义的条件下显著提升生成多样性，并在高 IPC 下获得额外收益。
- 基于 K-means 的分布近似匹配和贪婪渐进匹配策略使得大规模数据集上的最优传输计算可行，同时保持性能。
---

# DMGD: Train-Free Dataset Distillation with Semantic-Distribution Matching in Diffusion Models

> [!tip] 核心洞察
> 在语义对齐的前提下，替代数据集与原始数据集之间的最优传输距离是风险差异的上界；因此，通过无训练的引导优化语义匹配（动态软标签）和分布匹配（最优传输损失），就能有效蒸馏大规模数据集。

| 字段 | 内容 |
|------|------|
| 中文题名 | DMGD：基于语义分布匹配的无训练数据集蒸馏 |
| 英文题名 | DMGD: Train-Free Dataset Distillation with Semantic-Distribution Matching in Diffusion Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2605.03877) · [Code](https://github.com/solomonWQC/DMGD) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video #topic/benchmarks_datasets_evaluation |
| Method | DMGD (Dual Matching Guided Diffusion) |
| Dataset | ImageNet-Woof, ImageNet-Nette, ImageNet-1K |

> [!tip] 效果简介
> - ImageNet-Woof 上，Top-1 accuracy (ResNet10-AP) IPC-10: 41.6, IPC-20: 50.2, IPC-50: 60.1 vs MGD3: IPC-10: 41.2, IPC-20: 47.1, IPC-50: 56.5 (IPC-10: +0.4, IPC-20: +3.1, IPC-50: +3.6)。
> - ImageNet-Nette 上，Top-1 accuracy (ResNet10-AP) IPC-10: 68.8, IPC-20: 76.2, IPC-50: 80.6 vs MGD3: IPC-10: 66.8, IPC-20: 74.8, IPC-50: 79.5 (IPC-10: +2.0, IPC-20: +1.4, IPC-50: +1.1)。
> - ImageNet-1K (soft-label) 上，Top-1 accuracy (ResNet-18) IPC-10: 46.3, IPC-50: 61.4 vs RDED: IPC-10: 42.0; Minimax: IPC-10: 44.3; MGD3: IPC-50: 61.3 (IPC-10: +4.3 相对于 RDED; IPC-50: +0.1 相对于 MGD3)。

## 概述

数据集蒸馏旨在将大规模数据集压缩为极小的替代集，使在该替代集上训练的模型逼近原始数据集的性能。近年来，扩散模型因其强大的生成先验被引入蒸馏流程，但现有方法面临效率与分布建模的双重瓶颈：**Minimax** 等方案需要在目标数据集上额外微调扩散模型，计算开销高昂；而 **MGD3** 等方法虽避免了微调，却忽视数据分布的整体结构与样本间多样性，导致蒸馏性能受限。

本文提出 **DMGD (Dual Matching Guided Diffusion)**，一个完全无训练的扩散蒸馏框架。其核心洞察在于：在语义对齐的前提下，替代数据集与原始数据集之间的最优传输距离构成了风险差异的上界（定理 1）。基于此，DMGD 将数据集蒸馏解耦为两个可独立优化的引导模块——**语义匹配**与**分布匹配**——并在扩散采样过程中协同施加，无需任何模型训练即可同时提升生成多样性与分布对齐质量。

在 ImageNet-Woof、ImageNet-Nette 和 ImageNet-1K 三个基准上，DMGD 以无训练的方式超越所有需要额外训练的 SOTA 方法，平均精度提升分别为 2.1%、5.4% 和 2.4%，验证了“解耦语义与分布、以最优传输桥接二者”这一技术路线的有效性。

## 背景与动机

### 数据集蒸馏的核心目标

数据集蒸馏（Dataset Distillation）旨在将大规模原始数据集 $\mathcal{T}$ 压缩为一个小型合成数据集 $\mathcal{S}$，使得在 $\mathcal{S}$ 上训练的模型能够获得与在 $\mathcal{T}$ 上训练相近的泛化性能。其核心优化目标可形式化为：

$$\mathbb{E}_{(x,y)\sim \mathcal{T}}[\ell(x,y;\theta_{\mathcal{S}}^\star)] \simeq \mathbb{E}_{(x,y)\sim \mathcal{T}}[\ell(x,y;\theta_{\mathcal{T}}^\star)]$$

其中 $\theta_{\mathcal{S}}^\star$ 和 $\theta_{\mathcal{T}}^\star$ 分别表示在合成数据集和原始数据集上训练得到的最优模型参数。这一目标要求蒸馏集在信息密度和分布结构上都能有效替代原始数据。

### 扩散模型时代的范式演进与瓶颈

近年来，扩散模型因其强大的生成先验被引入数据集蒸馏领域，形成了多种技术范式。**GLaD**、**Minimax** 等方法率先探索了基于扩散模型的蒸馏路径，但存在根本性效率瓶颈：Minimax 需要在目标数据集上对扩散模型进行额外微调，计算开销巨大（约 10 小时级别），且微调过程与蒸馏目标之间的耦合限制了方法的灵活性。**D4M** 通过聚类方式利用扩散模型生成样本，但忽视了样本间的分布结构和多样性。**MGD3** 采用预测模式点进行孤立引导，虽然避免了微调，却未考虑目标数据集的整体分布结构，导致生成样本缺乏多样性。**DiT** 等直接使用预训练扩散模型生成的方法，则完全缺乏与目标数据集的适配机制。

这些方法的共同缺陷可归结为两个维度：**语义维度**上，现有方法使用硬标签的静态分类器引导或聚类模式点，无法在保证语义对齐的同时充分释放扩散模型的多样性潜力；**分布维度**上，均值匹配（如 **DM**）或单纯聚类中心匹配仅能捕捉分布的一阶统计量，丢失了类内细粒度模式和样本间结构信息。更为关键的是，这两个维度的优化在现有方法中往往是耦合的——例如微调扩散模型同时改变了语义表征和分布特性，使得无法独立调控多样性与分布对齐之间的权衡。

### 本文的理论切入点与动机

本文从理论层面重新审视了数据集蒸馏的风险控制问题。核心洞察在于：**在语义对齐的前提下，替代数据集与原始数据集之间的最优传输距离构成了风险差异的上界**。具体而言，定理 1 建立了如下风险界：

$$|R_{\mathcal{T}}(\theta_{\mathcal{T}}^*) - R_{\mathcal{T}}(\theta_S^*)| \le 2L \cdot W(P_{\mathcal{T}}, P_S)$$

其中 $L$ 为损失函数的 Lipschitz 常数，$W(P_{\mathcal{T}}, P_S)$ 为原始分布与蒸馏分布之间的 Wasserstein 距离。这一定理揭示了数据集蒸馏的本质结构：**语义匹配确保条件分布对齐，而分布匹配通过最小化边缘分布的最优传输距离来控制泛化风险上界**。两者可以解耦为独立的目标，分别优化后再协同作用。

基于这一理论洞察，本文提出 **DMGD（Dual Matching Guided Diffusion）** 框架，核心动机在于：**无需任何额外训练，仅在扩散采样过程中施加解耦的语义引导和分布引导，即可同时实现多样性提升和分布对齐**。语义匹配方面，通过分类器自由引导和动态软标签机制，在扩散过程的不同阶段注入可控的随机探索与语义精炼；分布匹配方面，通过最优传输损失引导采样过程向目标分布靠拢，并借助 K-means 分布近似和贪婪渐进匹配策略解决大规模数据集上的计算可行性和多样性保持问题。这一无训练、解耦的范式从根本上绕开了现有方法在效率与性能之间的折衷困境。

## 核心创新

DMGD 的核心创新在于将数据集蒸馏解耦为**语义匹配**与**分布匹配**两个独立且可协同的引导目标，并在扩散采样过程中以**完全无训练**的方式实现二者的联合优化。相较于现有基于扩散模型的蒸馏范式，该方法在三个关键维度上实现了机制性突破。

### 训练范式的根本转变：从微调依赖到训练免费

现有基于扩散模型的蒸馏方法普遍依赖额外训练。**Minimax** 需要在目标数据集上对扩散模型进行微调，**MGD3** 则需训练辅助分类器以预测模式点。这些训练步骤不仅引入显著的计算开销（例如 Minimax 在 ImageNet-1K 上的训练时间约 10 小时），还限制了方法在大规模场景下的可扩展性。

DMGD 将蒸馏完全迁移至扩散模型的**采样过程**，通过梯度引导而非参数更新来实现语义与分布的联合控制。其单步引导扩散过程定义为：

$$z_{t-1} = D_{\theta}(z_t, t, y) - \rho_t \nabla_{z_t} E(z_t, c)$$

其中 $E(z_t, c)$ 为可微分的条件函数，引导梯度直接作用于采样轨迹，无需修改预训练扩散模型的权重。这一设计使得 DMGD 在 ImageNet-1K 上的总计算时间仅约 0.5 小时，同时取得与训练依赖方法相当甚至更优的性能。

### 语义匹配：从硬标签静态引导到动态软标签多阶段控制

传统语义引导依赖固定的硬标签或静态分类器输出，导致生成样本过度集中于高密度区域，丧失类别内多样性。DMGD 提出了**动态软标签机制**，将语义引导分解为三个时间依赖的阶段：

1. **随机探索阶段**（$t \ge 45$）：在采样早期引入各向异性噪声，促使样本逃离高密度模式点，扩大语义空间的覆盖范围。
2. **动态软标签引导阶段**（$t \in [25, 45]$）：构造时间依赖的混合标签分布 $\widetilde{f_Y}(y) = \sqrt{\sigma_t} f_Y(y) + (1-\sqrt{\sigma_t})(\beta_s f_Y(y^\star) + \beta_n n)$，在真实标签编码与随机标签编码之间平滑过渡，平衡语义保真度与多样性。
3. **语义精炼阶段**（$t \le 25$）：恢复标准分类器自由引导，确保最终生成样本的语义准确性。

这一设计的理论基础源于 **Lemma 1** 对分类器自由引导梯度的近似：

$$\nabla_{z_t} \log p(y|z_t) \approx \omega (\epsilon_{\theta}(z_t, t, \emptyset) - \epsilon_{\theta}(z_t, t, y))$$

该近似使得 DMGD 无需训练额外分类器即可实现条件似然的梯度估计，而动态软标签的引入则在不破坏该近似的前提下，通过时间依赖的标签扰动扩展了条件空间的有效支撑集。消融实验证实，仅使用硬标签引导时 IPC-10 精度为 31.2%，引入动态软标签与语义精炼后提升至 42.0%，验证了多阶段控制的必要性。

### 分布匹配：从均值匹配到最优传输驱动的结构对齐

传统分布匹配方法（如 **DM**）仅匹配类别均值，忽视了分布的内部结构与样本间相关性。DMGD 基于 **Theorem 1** 建立了分布匹配的理论必要性：

$$|R_{\mathcal{T}}(\theta_{\mathcal{T}}^*) - R_{\mathcal{T}}(\theta_S^*)| \le 2L \cdot W(P_{\mathcal{T}}, P_S)$$

该定理表明，在语义对齐的前提下，蒸馏数据集与原始数据集之间的风险差异由二者边缘分布的 Wasserstein 距离上界所控制。因此，最小化该距离是降低蒸馏性能损失的充分条件。

基于此，DMGD 引入**最优传输引导损失**：

$$\mathcal{L}_{\mathrm{OT}}(P_S^t, P_{\mathcal{T}}) = W_{\varepsilon}(P_S^t, P_{\mathcal{T}}) = \langle \gamma^*, \mathbf{C} \rangle$$

通过 Sinkhorn 算法计算熵正则化最优传输距离，并在扩散采样的关键时间窗口 $t \in [30, 45]$ 内施加引导梯度。为应对大规模数据集上最优传输计算的高复杂度，DMGD 进一步提出两项效率优化策略：

- **分布近似匹配**：使用类内 K-means 聚类将目标分布压缩为少量支持点，**Corollary 1** 证明该近似的误差上界严格小于均值匹配方法。
- **贪婪渐进匹配**：逐个优化合成样本并冻结已生成样本，防止所有样本收敛至分布均值，从而保持样本间多样性。

消融实验表明，K-means 近似在 IPC-50 下取得 60.1% 精度，显著优于均值匹配的 58.6% 和基于密度的聚类方法 DBS 的 59.6%；全阶段分布匹配（40.4%）反而劣于仅在关键窗口施加引导（40.8%），证实了时间窗口选择的重要性。

### 双目标协同的解耦理论框架

DMGD 的核心理论贡献在于将数据集蒸馏形式化为两个可解耦目标的联合优化问题。**Theorem 1** 为这一解耦提供了严格的理论支撑：只要语义对齐成立，风险差异的上界仅取决于分布距离，因此语义匹配与分布匹配可以作为独立模块分别设计。Figure 4 中记录的渐进蒸馏过程中最优传输损失的变化进一步验证了双目标之间不存在优化冲突——损失随蒸馏进程单调递减，表明两个引导模块能够协同工作而非相互干扰。

## 整体框架

DMGD 提出了一种**完全无训练**的双匹配引导扩散框架，将数据集蒸馏解耦为语义匹配（Semantic Matching）与分布匹配（Distribution Matching）两个协同模块，全部作用于预训练扩散模型的采样过程。其核心逻辑源于定理 1 所揭示的理论保证：在语义对齐条件下，替代数据集与原始数据集之间的风险差异由它们边缘分布的最优传输距离所界定，即

$$|R_{\mathcal{T}}(\theta_{\mathcal{T}}^*) - R_{\mathcal{T}}(\theta_S^*)| \le 2L \cdot W(P_{\mathcal{T}}, P_S)$$

这为“先保证语义对齐，再最小化分布距离”的两阶段优化提供了理论依据。

框架的整体流程如图 2 所示。给定一个预训练的潜扩散模型（LDM），DMGD 在反向扩散采样过程中同时施加两类引导：

1. **语义匹配模块**：利用分类器自由引导（Classifier-Free Guidance）实现条件生成，无需额外训练分类器。其核心创新是**动态软标签机制**，将采样过程划分为三个阶段——随机探索（$t \ge 45$）、动态软标签引导（$t \in [25, 45]$）和语义精炼（$t \le 25$）。在每个阶段，软标签由原始标签编码、随机标签编码和各向异性噪声按时间依赖的权重混合而成：

   $$\widetilde{f_Y}(y) = \sqrt{\sigma_t} f_Y(y) + (1-\sqrt{\sigma_t})(\beta_s f_Y(y^\star) + \beta_n n)$$

   这一设计在不破坏语义对齐的前提下显著提升了生成样本的多样性，尤其在高 IPC 设置下，随机探索的引入可带来额外收益（如 IPC-50 时从 59.6% 提升至 60.1%）。

2. **分布匹配模块**：通过最小化合成数据集与目标数据集之间的熵正则化最优传输距离来对齐整体分布结构：

   $$\mathcal{L}_{\mathrm{OT}}(P_S^t, P_{\mathcal{T}}) = W_{\varepsilon}(P_S^t, P_{\mathcal{T}}) = \langle \gamma^*, \mathbf{C} \rangle$$

   该引导仅在关键时间窗口 $t \in [30, 45]$ 内施加——消融实验表明，全阶段施加分布匹配反而会损害性能（IPC-10 下从 40.8 降至 40.4）。为应对大规模数据集上的计算挑战，框架引入两个效率优化策略：
   - **分布近似匹配**：使用类内 K-means 聚类将目标分布压缩为少量支持点，理论上证明了其误差不大于均值匹配（Proposition 2），且计算时间仅约 0.5 小时，相比 Minimax 的约 10 小时大幅缩减。
   - **贪婪渐进匹配**：逐个优化合成样本并冻结已生成的样本，防止所有样本收敛到分布均值，从而保持样本间多样性。

两个模块在采样过程中协同工作：语义匹配确保每个样本携带正确的类别语义，分布匹配确保合成数据集整体与目标数据集的分布结构对齐。这种解耦设计使得 DMGD 无需任何微调即可在 ImageNet-Woof、ImageNet-Nette 和 ImageNet-1K 上达到 SOTA 性能。

### 补充图表

![[assets/figures/papers/paper_list_l2671_https_arxiv_org_abs_2605_03877/figures/002_Figure_2.jpg]]
*Figure 2: Framework of our DMGD method. Our method establishes two guidance modules during the sampling process: semantic matching and distribution matching. In semantic matching, we propose a dynamic soft label mechanism to unlock the potential of diffusion models for diversified generation while ensuring semantic alignment. In distribution matching, we optimize optimal transport computation through distribution approximation and greedy progressive matching to enable optimal transport-based distribution alignment guidance. We present the corresponding pseudocode in the Appendix A3 Algorithm 1*

## 核心模块与公式推导

### 理论根基：风险差异的最优传输上界

DMGD 将数据集蒸馏解耦为语义匹配与分布匹配两个目标，其理论依据来自定理 1：在语义对齐条件下，原始数据集 $\mathcal{T}$ 与蒸馏数据集 $\mathcal{S}$ 之间的风险差异由它们边缘分布的最优传输距离上界所控制：

$$|R_{\mathcal{T}}(\theta_{\mathcal{T}}^*) - R_{\mathcal{T}}(\theta_S^*)| \le 2L \cdot W(P_{\mathcal{T}}, P_S)$$

其中 $L$ 为损失函数的 Lipschitz 常数，$W(P_{\mathcal{T}}, P_S)$ 为两分布间的 Wasserstein 距离。该定理揭示了一个因果机制：**只要保证语义对齐（使 $\theta_S^*$ 在语义上与 $\theta_{\mathcal{T}}^*$ 可比），最小化分布间的最优传输距离即可直接收紧泛化风险上界**，无需在目标数据集上微调扩散模型。

---

### 模块一：语义匹配——动态软标签引导

语义匹配的目标是在扩散采样过程中注入类别语义，同时提升生成多样性。DMGD 摒弃了传统方法中依赖辅助分类器或硬标签静态引导的做法，转而利用**分类器自由引导**的梯度近似实现无分类器的条件生成：

$$\nabla_{z_t} \log p(y|z_t) \approx \omega (\epsilon_{\theta}(z_t, t, \emptyset) - \epsilon_{\theta}(z_t, t, y))$$

其中 $\omega$ 为引导强度，$\epsilon_{\theta}(z_t, t, \emptyset)$ 和 $\epsilon_{\theta}(z_t, t, y)$ 分别为无条件与条件噪声预测。这一近似使得语义信号可直接从预训练扩散模型中提取。

在此基础上，DMGD 提出**动态软标签机制**，将采样过程划分为三个阶段：

1. **随机探索阶段**（$t \ge 45$）：注入各向异性噪声，促使采样轨迹跳出高密度区域，提升初始多样性；
2. **动态软标签引导阶段**（$t \in [25, 45]$）：使用时间依赖的软标签 $\widetilde{f_Y}(y)$ 替代硬标签，其构造方式为：

$$\widetilde{f_Y}(y) = \sqrt{\sigma_t} f_Y(y) + (1-\sqrt{\sigma_t})(\beta_s f_Y(y^\star) + \beta_n n)$$

其中 $f_Y(y)$ 为目标类别编码，$f_Y(y^\star)$ 为随机类别编码，$n$ 为各向异性噪声，$\sigma_t$ 为噪声调度参数，$\beta_s$ 和 $\beta_n$ 控制软标签与噪声的混合比例。该设计使模型在保持语义方向的同时获得类间探索能力；

3. **语义精炼阶段**（$t \le 25$）：切换回硬标签引导，确保最终生成样本的类别语义精确。

动态软标签下的分类器自由引导公式为：

$$\hat{\epsilon}_{\theta}(z_t, t, \widetilde{y}_t) = (1 + \omega) \epsilon_{\theta}(z_t, t, \widetilde{y}_t) - \omega \epsilon_{\theta}(z_t, t, \emptyset)$$

---

### 模块二：分布匹配——最优传输引导

分布匹配的目标是使合成数据集的整体分布结构与目标数据集对齐。DMGD 采用熵正则化最优传输距离作为引导损失，仅在关键时间窗口 $t \in [30, 45]$ 内施加：

$$\mathcal{L}_{\mathrm{OT}}(P_S^t, P_{\mathcal{T}}) = W_{\varepsilon}(P_S^t, P_{\mathcal{T}}) = \langle \gamma^*, \mathbf{C} \rangle$$

其中 $\gamma^*$ 为 Sinkhorn 算法求解的最优传输计划，$\mathbf{C}$ 为代价矩阵。该损失通过梯度引导采样过程向目标分布的结构靠拢。

**关键设计：单样本渐进匹配**。为避免所有合成样本收敛到分布均值而丧失多样性，DMGD 采用**贪婪渐进匹配**策略——逐个优化合成样本，冻结已生成样本，使每个样本覆盖分布的不同区域。

---

### 模块三：分布近似匹配——大规模高效计算

在大规模数据集上直接计算最优传输距离计算代价过高。DMGD 通过**分布近似匹配**解决这一问题：对每个类别内部使用 K-means 聚类，将目标分布压缩为 $K$ 个支持点，以聚类质心作为近似分布的支撑集，并以聚类占比作为质量系数 $m_i = \frac{c_i}{\sum_{j=1}^K c_j}$。

该近似策略的理论保证由推论 1 给出：

$$|R_{\mathcal{T}}(\theta_{\mathcal{T}}^*) - R_{\mathcal{T}}(\theta_S^*)| \le 2L \cdot \big( W(P_S, \widetilde{P}_{\mathcal{T}}) + W(P_{\mathcal{T}}, \widetilde{P}_{\mathcal{T}}) \big)$$

其中 $\widetilde{P}_{\mathcal{T}}$ 为近似分布。误差由上界中的两项控制：合成分布与近似分布的对齐误差，以及近似分布对原始分布的逼近误差。命题 2 进一步证明，K-means 近似的 Wasserstein 误差不大于均值匹配方法，即 $W(P_T, \widetilde{P}_T^{(2)}) \leq W(P_T, \widetilde{P}_T^{(1)})$，从理论上解释了 K-means 近似优于传统均值匹配的原因。消融实验（Table 6）验证了这一结论：K-means 在 IPC-10/50/100 设置下均取得最高精度，且计算时间仅约 0.5 小时，远低于 Minimax 的约 10 小时。

## 实验与分析

### 主实验结果

DMGD 在多个 ImageNet 基准上以无训练方式取得 SOTA 性能。Table 1 报告了 ImageNet-Woof 和 ImageNet-Nette 的硬标签评估结果。在 Woof 上，DMGD 在 IPC-10/20/50 下分别达到 41.6%、50.2%、60.1%，相比此前最优的 **MGD3** 分别提升 0.4、3.1、3.6 个百分点，其中高 IPC 场景的增益尤为显著。在 Nette 上，DMGD 以 68.8%（IPC-10）、76.2%（IPC-20）、80.6%（IPC-50）全面领先，平均精度提升达 5.4%。Table 2 展示了 ImageNet-1K 软标签协议下的结果：DMGD 在 IPC-10 下以 46.3% 超越 **RDED**（42.0%）和 **Minimax**（44.3%）达 4.3 个百分点；IPC-50 下以 61.4% 与 **MGD3**（61.3%）持平，验证了无训练框架在大规模数据集上的竞争力。

![[assets/figures/papers/paper_list_l2671_https_arxiv_org_abs_2605_03877/figures/003_Table_1.jpg]]
*Table 1: Performance comparison between our method and state-of-the-art methods across different ImageNet subsets, evaluated under the hard-label protocol. Results are reported as Top-1 accuracy on ResNet-10 with average pooling (Resnet10-AP). The best performance is highlighted in bold, while the second-best is underlined*

![[assets/figures/papers/paper_list_l2671_https_arxiv_org_abs_2605_03877/figures/006_Table_2.jpg]]
*Table 2: Performance comparison between our method and stateof-the-art methods on ImageNet-1k, evaluated under the soft-label protocol. Results are reported as Top-1 accuracy on ResNet-18 and ResNet-101. The best performance is highlighted in bold, while the second-best is underlined. Missing values are due to the original paper not reporting them*

扩展评估（Figure 3a-b）进一步表明，DMGD 在 ResNet-18 和更高 IPC（100）设置下持续保持优势，且在 ConvNet-6 等小架构上同样有效（Table 4），说明蒸馏集具有良好的跨架构泛化能力。

### 消融实验

**组件贡献**（Table 3）。仅使用动态软标签的语义匹配（SM）在 IPC-10 下达到 38.9%，加入分布匹配（DM）后提升至 40.8%；IPC-50 下从 59.3% 提升至 60.1%。分布匹配的增益在高 IPC 下更为突出，这与高 IPC 需要更强分布对齐的直觉一致。

**动态标签构建**（Table 5）。对比了硬标签、纯软标签、噪声注入及其组合。结果表明，软标签与噪声协同使用（Soft label with Noise+OT）在 IPC-10 和 IPC-50 下均取得最优（40.8% / 60.1%），单独使用软标签或噪声均导致性能下降，验证了动态混合机制的必要性。

**分布近似方法**（Table 6）。K-means 聚类近似在所有 IPC 设置下均优于均值匹配（Mean）和基于密度的聚类质心方法（DBS）。例如 IPC-50 下 K-means 达到 60.1%，相比 Mean 的 58.6% 提升 1.5 个百分点。同时，K-means 近似将最优传输计算时间从 Minimax 的约 10 小时压缩至约 0.5 小时，实现了效率与性能的平衡。

**引导阶段分析**（Table 7）。语义精炼阶段（t ≤ 25）对性能至关重要：仅动态软标签+随机探索在 IPC-10 下仅 31.2%，加入语义精炼后跃升至 42.0%。分布匹配仅在关键时间窗口 t ∈ [30, 45] 内施加时效果最佳（40.8%），全阶段分布匹配反而降至 40.4%，说明早期采样阶段的分布约束会损害多样性。

**超参数敏感性**（Table 8，Figure 3c-d）。随机探索强度 β_n 在低 IPC 时取较小值（0.01 得 42.7%）更优，此时代表性优先；高 IPC 时较大值（0.04-0.1）更优，此时多样性优先。分布匹配引导系数 ρ 和支持点数 K 在较宽范围内表现稳定，表明方法对超参数不敏感。

### 质量评估与可视化

Table 4 从覆盖度（Coverage）、最优传输数据集距离（OTDD）、多样性指标和 FID 四个维度量化了蒸馏集质量。DMGD 在 OTDD 和 FID 上均取得最优，表明其生成样本与目标分布的 Wasserstein 距离最小且视觉质量最高；多样性指标同样领先，验证了动态软标签对多样性的促进作用。

分布可视化（Figure 3 distribution）通过 t-SNE 对比了不同方法生成样本与原始数据集的分布对齐程度。DMGD 的样本分布与原始数据高度重合，而 **MGD3** 和 **GLaD** 的样本则呈现明显的分布偏移或坍缩。OT 距离可视化（Figure 4）进一步显示，在贪婪渐进蒸馏过程中，每个样本的最优传输损失逐步下降，且语义匹配与分布匹配之间未出现优化冲突，验证了双匹配框架的协同性。

![[assets/figures/papers/paper_list_l2671_https_arxiv_org_abs_2605_03877/figures/004_Figure_3.jpg]]
*Figure 3: Evaluation results: (a-b) Evaluation of our method’s performance across different architectures and higher IPC settings: Results are reported as Top-1 accuracy on (a) ResNet10-AP and (b) ResNet-18. (c-d) Evaluation of our method’s performance under different hyperparameters: (c) distribution matching guidance coefficient*

![[assets/figures/papers/paper_list_l2671_https_arxiv_org_abs_2605_03877/figures/019_Figure_3.jpg]]
*Figure 3: Distribution Visualization: Visualization results of sample distributions for surrogate datasets generated by different methods and the original dataset: top row corresponds to ImageNet-Woof under IPC-100 setting, bottom row corresponds to ImageNet-Nette under IPC-50 setting*

![[assets/figures/papers/paper_list_l2671_https_arxiv_org_abs_2605_03877/figures/021_Figure_4.jpg]]
*Figure 4: OT Distance Visualization: We systematically recorded the final optimal transport (OT) distance loss for each sample during progressive distillation. A randomly selected category from ImageNet-Woof was visualized to illustrate the results*

![[assets/figures/papers/paper_list_l2671_https_arxiv_org_abs_2605_03877/figures/005_Figure_4.jpg]]
*Figure 4: Generated Samples Visualization: the visual comparison of Golden Retriever in ImageNet-WOOF, we present the generated samples from different methods under the IPC-10 setting. The method names are marked at the left of each row*

### 失败模式与局限

尽管 DMGD 在 ImageNet 系列数据集上表现突出，其设计依赖预训练扩散模型的语义先验，因此**局限于具有明确语义边界的数据集**。对于完全开放的场景或语义模糊的数据集，动态软标签机制可能无法提供有效的语义引导。此外，由于扩散模型的固有模态限制，该方法**无法直接泛化至音频、视频、时间序列或具身 AI 数据**。

超参数 β_n 的调节目前依赖手动搜索，缺乏形式化为 IPC 函数的自动化机制。在高 IPC 下，随机探索与语义精炼的权衡需要更精细的理论指导。

### 补充图表

![[assets/figures/papers/paper_list_l2671_https_arxiv_org_abs_2605_03877/figures/008_Table_3.jpg]]
*Table 3: Ablation study on the components of our method. Results are reported as Top-1 accuracy on ResNet10-AP. The best performance is highlighted in bold, while the second-best is underlined*

![[assets/figures/papers/paper_list_l2671_https_arxiv_org_abs_2605_03877/figures/017_Table_5.jpg]]
*Table 5: Ablation study on different dynamic label construction methods. Results are reported as Top-1 accuracy on ResNet-10 with average pooling in ImageNet-Woof. The best performance is highlighted in bold*

![[assets/figures/papers/paper_list_l2671_https_arxiv_org_abs_2605_03877/figures/015_Table_6.jpg]]
*Table 6: Ablation study on different distribution approximation methods. Results are reported as Top-1 accuracy on ResNet-10 with average pooling in Imagenet-Woof. The best performance is highlighted in bold, while the second-best is underlined*

![[assets/figures/papers/paper_list_l2671_https_arxiv_org_abs_2605_03877/figures/016_Table_7.jpg]]
*Table 7: Ablation study on different guidance mechanism. Results are reported as Top-1 accuracy on ResNet-10 with average pooling in Imagenet-Woof. The best performance is highlighted in bold, while the second-best is underlined*

![[assets/figures/papers/paper_list_l2671_https_arxiv_org_abs_2605_03877/figures/018_Table_8.jpg]]
*Table 8: Evaluation of different parameter. Results are reported as Top-1 accuracy on ResNet-10 with average pooling in ImageNet-Woof*

## 方法谱系与知识库定位

### 1. 问题定位与基线对比

DMGD 所解决的核心瓶颈在于：现有基于扩散模型的数据集蒸馏方法要么需要额外的微调步骤，要么在生成过程中忽视了目标数据集的分布结构与样本间多样性。这一瓶颈在两类代表性基线中体现得尤为明显：

- **Minimax**：需要在目标数据集上对扩散模型进行额外微调，虽然能提升蒸馏质量，但计算开销巨大（约10小时），且微调过程与蒸馏目标之间的耦合限制了方法的灵活性。
- **MGD3**：采用预测模式点进行孤立引导，虽然避免了微调，但忽略了数据分布的底层结构和样本间多样性，导致生成样本集中在高密度区域，蒸馏集的代表性和多样性不足。

DMGD 的关键洞察在于将数据集蒸馏解耦为两个可独立优化的子目标——**语义匹配**与**分布匹配**——并通过理论分析（定理1）证明：在语义对齐的前提下，原始数据集与蒸馏数据集之间的风险差异由它们边缘分布的最优传输距离所界定。这一理论结果直接驱动了方法设计：语义匹配确保类别信息的准确传递，分布匹配则通过最小化最优传输距离来对齐整体分布结构，两者协同作用而无需任何额外训练。

### 2. 方法谱系中的位置

在基于扩散模型的数据集蒸馏方法谱系中，DMGD 占据了一个独特的位置——**完全无训练的双引导范式**。与现有方法的对比如下：

| 方法 | 训练需求 | 语义对齐方式 | 分布对齐方式 | 多样性机制 |
|------|----------|-------------|-------------|-----------|
| **GLaD** | 需微调 | 条件生成 | 隐式（通过微调） | 有限 |
| **Minimax** | 需微调 | 条件生成+对抗 | 隐式（通过微调） | 有限 |
| **D4M** | 无训练 | 聚类中心引导 | 聚类质心匹配 | 聚类内有限 |
| **MGD3** | 无训练 | 预测模式点引导 | 无显式分布匹配 | 不足 |
| **DMGD** | **无训练** | **动态软标签引导** | **最优传输分布匹配** | **三阶段随机探索** |

DMGD 的突破在于：它是首个将**最优传输理论**系统性地引入扩散采样引导过程的方法，同时通过**动态软标签机制**在不破坏语义的条件下显著提升生成多样性。这使得 DMGD 在计算效率（约0.5小时 vs. Minimax的约10小时）和蒸馏性能上同时取得优势。

### 3. 与经典蒸馏范式的理论关联

DMGD 的理论框架与经典分布匹配方法（如 **DM**）存在深层联系。DM 方法通过匹配合成集与目标集在特征空间中的均值来实现分布对齐，而 DMGD 证明了均值匹配实际上是最优传输分布近似的一个特例（命题2）。具体而言：

- 当分布近似中每个类仅使用一个支持点（即类均值）时，最优传输退化为均值匹配。
- DMGD 通过 K-means 聚类使用多个支持点来逼近真实分布，理论上证明其 Wasserstein 距离不大于均值匹配的逼近误差（推论1）。

这一理论递进关系表明 DMGD 并非对现有方法的简单改进，而是在分布匹配的理论基础上进行了实质性拓展。

### 4. 适用边界与局限

尽管 DMGD 在多个基准上取得了显著提升，其适用边界仍需明确：

**已验证的有效范围**：
- 数据集类型：具有明确类别语义的图像分类数据集（ImageNet-Woof、ImageNet-Nette、ImageNet-1K）
- 分辨率：256×256
- 评估协议：硬标签（子集）与软标签（ImageNet-1K）
- IPC 范围：10-100

**已知局限**：
1. **语义范围受限**：当前方法局限于具有有限语义范围的数据集蒸馏，对于通用语义的扩散模型和更复杂的开放场景数据集探索不足。论文明确指出这一局限，意味着在细粒度分类、长尾分布或跨域场景中的表现尚待验证。
2. **模态限制**：由于依赖扩散模型的固有特性，方法无法直接泛化到音频、视频、时间序列或具身 AI 数据等其他模态。这一局限源于扩散模型本身的设计假设，而非方法设计的缺陷。
3. **超参数敏感性**：动态软标签中的随机探索强度（β_n）需要根据 IPC 手动调节——低 IPC 时较小值更优（代表性优先），高 IPC 时较大值更优（多样性优先）。缺乏自适应的参数选择机制。

### 5. 开放问题与未来方向

从 DMGD 的当前设计出发，以下开放问题值得关注：

1. **自适应多样性权衡**：如何将 β_n 等多样性相关超参数形式化为 IPC 的函数，实现自动权衡而非手动调节？这需要建立 IPC 与最优多样性水平之间的理论关系。

2. **联合分布的最优传输**：当前方法仅在样本空间上应用最优传输，标签信息通过语义匹配独立处理。如何将最优传输同时应用于样本和标签的联合分布，以更全面地蒸馏语义和分布信息，是一个理论上有趣的拓展方向。

3. **跨域泛化**：在更复杂的跨域数据集或无条件生成场景中，DMGD 的双匹配框架是否仍然有效？这需要验证动态软标签机制在语义边界模糊时的鲁棒性。

4. **与其他生成先验的兼容性**：DMGD 目前基于 Latent Diffusion Model，其核心思想（解耦语义匹配与分布匹配）是否可迁移到其他生成范式（如自回归模型、流匹配模型）仍有待探索。

## 原文 PDF

![[paperPDFs/CVPR_2026/DMGD_Train_Free_Dataset_Distillation_with_Semantic_Distribution_Matching_in_Diffusion_Models.pdf]]