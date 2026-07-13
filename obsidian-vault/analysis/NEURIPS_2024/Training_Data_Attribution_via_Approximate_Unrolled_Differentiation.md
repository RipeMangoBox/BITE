---
title: "Training Data Attribution via Approximate Unrolled Differentiation"
type: paper
paper_level: A
venue: NeurIPS
year: 2024
pdf_ref: paperPDFs/NEURIPS_2024/Training_Data_Attribution_via_Approximate_Unrolled_Differentiation.pdf
code_link: https://github.com/pomonam/kronfluence
project_link: https://github.com/pomonam/kronfluence
aliases:
- SSSUCE
- TDAAUD
tags:
- NEURIPS_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/robotics
core_operator: "通过将训练过程划分为多个平稳段并在各段内近似Hessian和梯度的统计分布，Source将展开微分的计算简化为仅需少量检查点，从而在保持反事实预测准确性的同时大幅降低计算负担。"
primary_logic: "分段平稳性近似使Source能够在不需要存储全部中间状态的情况下，利用类似影响函数的公式高效计算归因分数，同时保留了优化轨迹的信息（学习率、优化器选择和训练阶段效应）。"
claims:
- "Source在FashionMNIST单模型和多模型设置下的LDS分别为0.46和0.53，显著优于影响函数的0.30和0.45。"
- "在非收敛和多阶段训练（RotatedMNIST、FashionMNIST-N）等挑战性设置中，Source始终优于所有隐式微分基线方法。"
- "在子集移除反事实评估中，Source只需移除更少的训练样本即可翻转测试预测，优于其他TDA方法。"
- "在未完全收敛的线性模型上，Source的LDS显著高于影响函数，且优势随训练迭代次数减少而增大。"
---

# Training Data Attribution via Approximate Unrolled Differentiation

> [!tip] 核心洞察
> 分段平稳性近似使Source能够在不需要存储全部中间状态的情况下，利用类似影响函数的公式高效计算归因分数，同时保留了优化轨迹的信息（学习率、优化器选择和训练阶段效应）。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 基于近似展开微分的训练数据归因 |
| 英文题名 | Training Data Attribution via Approximate Unrolled Differentiation |
| 会议/期刊 | NeurIPS 2024 |
| Links | [paper](https://arxiv.org/abs/2405.12186) · [GitHub](https://github.com/pomonam/kronfluence) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/robotics |
| Method | Source (Segmented statiOnary UnRolling for Counterfactual Estimation) |
| Dataset | FashionMNIST (single model), FashionMNIST (multiple models), CIFAR-10, FashionMNIST (subset removal) |

> [!tip] 效果简介
> - FashionMNIST (single model) 上，LDS at α=0.5 为 0.46 ± 0.01，对比 0.30 ± 0.01 (Influence Functions)，变化 +0.16。
> - FashionMNIST (multiple models) 上，LDS at α=0.5 为 0.53 ± 0.01，对比 0.45 ± 0.01 (Influence Functions)，变化 +0.08。
> - CIFAR-10, FashionMNIST (subset removal) 上，fraction of test examples flipped after removing top-k influential points 为 higher fraction flipped (better)，对比 lower fraction flipped (worse) for other methods，变化 qualitative improvement。

## 概要

**核心问题：训练数据归因的根本性权衡。** 训练数据归因（TDA）旨在量化单个训练样本对模型行为的影响，但现有方法存在根本性权衡。隐式微分方法（如影响函数，**Influence Functions** (Koh and Liang, 2017)）依赖模型收敛到唯一最优解的假设，无法处理非收敛训练、多阶段训练和优化器细节；而展开微分方法虽能处理这些情况，却需存储全部中间变量，计算和内存成本过高。

**核心洞察：分段平稳性近似。** 本文提出的 **Source**（Segmented statiOnary UnRolling for Counterfactual Estimation）通过将训练轨迹划分为多个平稳段，并在各段内近似Hessian和梯度的统计分布，将展开微分的计算简化为仅需少量检查点（如6个），从而在保持反事实预测准确性的同时大幅降低计算负担。其归因分数最终通过类似影响函数的公式高效计算，同时保留了优化轨迹的信息（学习率、优化器选择和训练阶段效应）。

**方法定位。** Source处于隐式微分与展开微分的交叉地带：它兼具展开微分对训练动态的建模能力，但仅需C个检查点（C ≪ 总迭代数T），而非全部中间状态（Table 1）。这一设计使其填补了现有TDA方法谱系中的空白。

**主要结果。** 在FashionMNIST数据集上，Source在单模型和多模型设置下的线性数据建模分数（LDS）分别达到0.46和0.53，显著优于影响函数的0.30和0.45（Table 2）。在非收敛和多阶段训练（RotatedMNIST、FashionMNIST-N）等挑战性设置中，Source始终优于所有隐式微分基线方法（Figure 7）。在子集移除反事实评估中，Source只需移除更少的训练样本即可翻转测试预测，优于其他TDA方法（Figure 8）。消融实验进一步表明，增加分段数可持续提升归因准确性，而在未完全收敛的线性模型上，Source相对于影响函数的优势随训练迭代次数减少而扩大（Figure 10）。



### 训练数据归因的核心问题

现代机器学习模型的行为深受其训练数据的影响。当模型产生错误预测、偏见输出或意外行为时，一个根本性的问题是：**哪些训练样本对此负责？** 训练数据归因（Training Data Attribution, TDA）正是为了回答这一问题而生的技术方向。其核心目标是量化每个训练样本对模型在特定查询样本上预测结果的贡献，从而为数据调试、模型解释和可信AI提供基础工具。

从形式上看，TDA试图估计一个反事实量：如果将某个训练样本 $z_m$ 从训练集 $\mathcal{D}$ 中移除并重新训练模型，查询样本 $z_q$ 的模型输出会发生多大变化。这一理想化的留一法分数定义为：

$$\tau _ { \mathrm { L O O } } ( z _ { q } , z _ { m } , \mathcal { D } ) : = f ( z _ { q } , \pmb { \theta } ^ { \star } ( \mathcal { D } \setminus \{ z _ { m } \} ) ) - f ( z _ { q } , \pmb { \theta } ^ { \star } )$$

然而，对每个训练样本执行完整的模型重训练在计算上不可行。因此，TDA方法的核心挑战在于**高效且准确地近似这一反事实效应**。

### 现有方法的根本权衡

当前主流的TDA方法可大致分为两类，它们在理论基础和实际适用性之间存在根本性的权衡。

**隐式微分方法**以影响函数（Influence Functions, **IF**; Koh and Liang, 2017）为代表。这类方法假设模型已收敛到经验风险的唯一最优解，并利用隐函数定理在最优解处进行一阶泰勒展开，从而将留一法效应近似为：

$$\tau _ { \mathrm { I F } } ( z _ { q } , z _ { m } , \mathcal { D } ) : = \nabla _ { \boldsymbol { \theta } } f ( z _ { q } , \boldsymbol { \theta } ^ { \star } ) ^ { \top } \mathbf { H } ^ { - 1 } \nabla _ { \boldsymbol { \theta } } \mathcal { L } ( z _ { m } , \boldsymbol { \theta } ^ { \star } )$$

这一公式只需最终模型参数和Hessian信息，计算效率高。但其有效性严格依赖于三个假设：(1) 模型已收敛到唯一最优解；(2) 损失函数在该最优解附近足够平滑；(3) 移除单个样本的效应可以通过一阶近似捕获。在真实深度学习场景中，这些假设常常不成立——模型可能未完全收敛、训练过程包含多个阶段（如预训练-微调）、优化器状态（动量、自适应学习率等）对最终参数有显著影响，而这些信息在隐式微分框架中被完全忽略。

**展开微分方法**则通过显式地沿优化轨迹反向传播梯度来估计训练样本的影响。这类方法不需要收敛假设，能够自然地处理任意优化器、学习率调度和多阶段训练。但其代价是巨大的：展开微分需要存储训练过程中**所有中间变量**（参数、梯度、优化器状态），对于现代深度学习模型而言，这一存储需求在内存和时间上都不可接受。

### 核心瓶颈与本文动机

上述分析揭示了一个清晰的瓶颈：**隐式微分方法计算高效但依赖强假设，在非收敛、多阶段训练等实际场景中失效；展开微分方法理论上更通用，但计算和内存成本过高，难以应用于真实规模的模型训练。**

本文的核心洞察是：这一权衡并非不可调和。通过将训练过程划分为多个**平稳段**（stationary segments），并在每个段内近似梯度和Hessian的统计分布，可以将展开微分的计算简化为仅需少量检查点（checkpoints）的影响函数式公式。这一思路既保留了展开微分对优化轨迹信息的建模能力（学习率、优化器选择、训练阶段效应），又避免了存储全部中间变量的巨大开销。

基于这一洞察，本文提出了**Source**（Segmented statiOnary UnRolling for Counterfactual Estimation）方法，旨在以可接受的计算成本，在更广泛的训练场景下提供比隐式微分方法更准确的反事实预测。



## 核心方法与创新机理

Source 的核心创新在于**通过分段平稳性近似，将展开微分（unrolled differentiation）的计算成本降低到与隐式微分方法可比的程度**，同时保留了展开微分对训练过程细节的建模能力。这一创新直接打破了现有 TDA 方法在“计算可行”与“反事实准确”之间的根本权衡。

### 问题瓶颈：隐式微分与展开微分的两难

现有基于梯度的 TDA 方法分为两大范式，各自存在严重局限：

- **隐式微分方法**（如影响函数，Koh and Liang, 2017）：假设模型参数收敛到经验风险的唯一最优解，从而可以使用逆 Hessian 向量积高效估计数据移除的影响。然而，这一假设在非收敛训练、多阶段训练（如预训练-微调）、使用复杂优化器（如 Adam）时失效，导致归因偏差。
- **展开微分方法**：通过对整个训练过程的计算图进行反向传播，精确计算数据移除对最终参数的影响。这种方法不依赖收敛假设，能捕捉学习率调度、优化器隐式偏差等训练细节，但需要存储所有中间变量，计算和内存成本随训练步数线性增长，在实际深度学习中不可行。

### 核心机制：分段平稳性近似

Source 的关键洞察是：**训练过程可以划分为多个平稳段，在每个段内梯度和 Hessian 的统计分布近似不变**。基于这一假设，Source 将展开微分的复杂反向累积计算简化为仅需少量检查点的矩阵运算。

具体而言，Source 的创新体现在以下三个层面：

**1. 分段 Jacobian 的矩阵指数近似**

在平稳段 $\ell$ 内，Hessian 近似为常数 $\bar{\mathbf{H}}_\ell$，学习率近似为常数 $\bar{\eta}_\ell$。该段内 $K_\ell$ 步 SGD 的期望 Jacobian 可近似为矩阵指数：

$$\mathbb{E}[\mathbf{S}_\ell] \approx \left(\mathbf{I} - \bar{\eta}_\ell \bar{\mathbf{H}}_\ell\right)^{K_\ell} \approx \exp(-\bar{\eta}_\ell K_\ell \bar{\mathbf{H}}_\ell) := \bar{\mathbf{S}}_\ell$$

这一近似将原本需要逐步展开的 $K_\ell$ 次矩阵乘法压缩为单次矩阵指数运算，大幅降低了计算复杂度。

**2. 分段残差的阻尼逆 Hessian 近似**

该段内数据移除对参数的影响（残差）同样可在平稳假设下近似为：

$$\mathbb{E}[\mathbf{r}_\ell] \approx \frac{1}{N}(\mathbf{I} - \exp(-\bar{\eta}_\ell K_\ell \bar{\mathbf{H}}_\ell)) \bar{\mathbf{H}}_\ell^{-1} \bar{\mathbf{g}}_\ell := \bar{\mathbf{r}}_\ell$$

其中 $\bar{\mathbf{g}}_\ell$ 为该段内的平均梯度。这一形式与影响函数的逆 Hessian 向量积高度相似，但通过矩阵指数因子 $(\mathbf{I} - \exp(-\bar{\eta}_\ell K_\ell \bar{\mathbf{H}}_\ell))$ 编码了优化轨迹的信息。

**3. 段间独立假设下的归因合成**

假设不同段的 Jacobian 统计独立，最终归因分数可表示为各段贡献的组合：

$$\tau_{\mathrm{SOURCE}}(z_q, z_m, \mathcal{D}; \lambda) := \nabla_\theta f(z_q, \theta^s)^\top \left(\sum_{\ell=1}^{L} \left(\prod_{\ell'=L}^{\ell+1} \bar{\mathbf{S}}_{\ell'}\right) \bar{\mathbf{r}}_\ell\right)$$

这一公式在形式上类似影响函数，但通过分段结构自然地编码了训练动态：早期段的残差会经过后续段 Jacobian 的衰减传播，这与影响函数仅依赖最终 Hessian 的单点近似有本质区别。

### 相对基线的方法特性变化

Source 在方法特性上相对隐式微分基线产生了以下关键变化：

| 特性 | 隐式微分（如影响函数） | Source |
|------|----------------------|--------|
| 所需检查点数量 | 1（仅最终参数） | C（例如 6），远小于总迭代数 T |
| 支持非收敛训练 | 否（假设收敛到唯一最优解） | 是（不依赖收敛假设） |
| 支持多阶段训练 | 否（无法区分不同阶段的数据） | 是（通过分段框架支持多阶段） |
| 计算成本 | 低（单次逆 Hessian 向量积） | 约为影响函数的 C 倍 |

### 创新边界与局限

需要指出的是，Source 的分段平稳性假设并非在所有场景下都成立。当 Hessian 或梯度在训练过程中剧烈变化时，需要更多分段来修正近似误差，但这会增加计算成本。如何自动确定分段点仍是待解决的问题。此外，快速版本 Fast-Source 通过直接平均段内参数来进一步降低计算量，但归因准确性有所下降（见消融实验 Figure 9）。



Source 的核心设计思想是将完整的训练轨迹划分为若干个**平稳段（segments）**，并在每个段内近似梯度和 Hessian 的统计分布为平稳的，从而将展开微分（unrolled differentiation）的计算简化为仅需少量模型检查点的影响函数式公式。这一设计从根本上解决了现有方法的两难困境：隐式微分方法（如影响函数）依赖最优解假设，无法处理非收敛或多阶段训练；而标准展开微分方法需要存储所有中间变量，计算和内存成本过高。

### 方法流程

Source 的归因计算流程由五个模块串联构成：

1. **Segment Training Trajectory（划分训练轨迹）**  
   将包含 $T$ 次参数更新的完整训练过程划分为 $L$ 个连续段（例如 $L=3$），每个段包含 $K_\ell$ 步更新。分段边界可以基于训练阶段自然划分（如学习率衰减点），也可均匀划分。

2. **Compute Segment Statistics（计算段统计量）**  
   在每个段内，从 $C$ 个等间距的检查点中采集参数快照，计算该段的**平均 Hessian** $\bar{\mathbf{H}}_\ell$、**平均梯度** $\bar{\mathbf{g}}_\ell$ 以及**平均学习率** $\bar{\eta}_\ell$。这些统计量是对段内优化动态的压缩表征。

3. **Approximate Segment Jacobian（近似段期望 Jacobian）**  
   利用段内的平稳性假设，将段 $\ell$ 的期望 Jacobian 近似为矩阵指数形式：
   $$\mathbb{E}[\mathbf{S}_\ell] \approx \left(\mathbf{I} - \bar{\eta}_\ell \bar{\mathbf{H}}_\ell\right)^{K_\ell} \approx \exp(-\bar{\eta}_\ell K_\ell \bar{\mathbf{H}}_\ell) := \bar{\mathbf{S}}_\ell$$
   这一近似将 $K_\ell$ 步逐次矩阵乘积累积为单次矩阵指数运算，大幅降低了计算复杂度。

4. **Approximate Segment Residual（近似段期望残差）**  
   类似地，将段 $\ell$ 的期望残差近似为阻尼逆 Hessian 向量积：
   $$\mathbb{E}[\mathbf{r}_\ell] \approx \frac{1}{N}(\mathbf{I} - \exp(-\bar{\eta}_\ell K_\ell \bar{\mathbf{H}}_\ell)) \bar{\mathbf{H}}_\ell^{-1} \bar{\mathbf{g}}_\ell := \bar{\mathbf{r}}_\ell$$
   该残差刻画了段内训练数据对参数更新的累积贡献。

5. **Compose Attribution Scores（组合归因分数）**  
   将各段的 Jacobian 和残差按训练顺序反向累积，得到最终归因分数：
   $$\tau_{\mathrm{SOURCE}}(z_q, z_m, \mathcal{D}; \lambda) := \nabla_\theta f(z_q, \theta^s)^\top \left(\sum_{\ell=1}^{L} \left(\prod_{\ell'=L}^{\ell+1} \bar{\mathbf{S}}_{\ell'}\right) \bar{\mathbf{r}}_\ell\right)$$
   其中 $\prod_{\ell'=L}^{\ell+1} \bar{\mathbf{S}}_{\ell'}$ 将后续段的 Jacobian 传播到当前段，$\bar{\mathbf{r}}_\ell$ 捕获当前段内训练点 $z_m$ 的贡献。

### 输入输出与关键设计选择

- **输入**：训练数据集 $\mathcal{D}$、查询样本 $z_q$、少量中间检查点（实验中 $C=6$，远小于总迭代数 $T$）、训练超参数（学习率调度、段划分）。
- **输出**：每个训练样本 $z_m$ 对查询样本 $z_q$ 的归因分数 $\tau_{\mathrm{SOURCE}}(z_q, z_m, \mathcal{D})$，正值表示该训练样本对正确预测有正向贡献，负值表示负向贡献。
- **关键设计选择**：
  - **分段数 $L$**：消融实验表明，从 $L=1$ 增加到 $L=3$ 可持续提升 LDS 评分，更细粒度的分段能更好地捕捉训练动态（Figure 5）。
  - **检查点数 $C$**：仅需 $C$ 个检查点而非全部 $T$ 步中间状态，这是 Source 计算效率的核心来源（Table 1）。
  - **快速变体 Fast-Source**：直接对段内参数取平均以进一步降低计算量，虽然归因准确性略有下降，但仍优于影响函数和 TracIn 等基线（Figure 9）。

### 方法谱系与知识库定位

Source 位于梯度归因方法谱系中展开微分与隐式微分的交汇点：

| 方法类别 | 代表方法 | 核心假设 | 计算代价 | 适用场景 |
|---------|---------|---------|---------|---------|
| 隐式微分 | **Influence Functions** (Koh & Liang, ICML 2017) | 模型收敛到唯一最优解 | 低（仅需最终参数） | 凸优化、充分收敛训练 |
| 投影式 | **TRAK** (Park et al., ICML 2023) | 集成模型可替代 Hessian 求逆 | 中（需训练多个模型） | 大规模模型、非凸优化 |
| 梯度检查点 | **TracIn** (Pruthi et al., NeurIPS 2020) | 梯度内积可近似归因 | 中（需多个检查点） | 非收敛训练 |
| 展开微分 | **Hydra** (Chen et al., NeurIPS 2021) | 完整展开训练图 | 极高（需存储所有中间状态） | 精确反事实估计 |
| **分段平稳展开** | **Source**（本文） | 段内梯度/Hessian 平稳 | 中（$C$ 倍于影响函数） | 非收敛、多阶段训练 |

Source 通过分段平稳性近似，保留了展开微分对优化轨迹信息（学习率、优化器选择、训练阶段效应）的敏感性，同时将计算和存储需求降至与隐式微分方法可比拟的水平。实验表明，当模型未完全收敛时，Source 相对影响函数的 LDS 优势随训练迭代次数减少而扩大（Figure 10 Right），验证了其在不完全优化场景下的独特价值。



### 问题形式化

Source 的目标是估计**留一法（LOO）归因分数**——移除单个训练样本 $z_m$ 后，查询样本 $z_q$ 上模型输出 $f$ 的变化量：

$$\tau _ { \mathrm { L O O } } ( z _ { q } , z _ { m } , \mathcal { D } ) : = f ( z _ { q } , \pmb { \theta } ^ { \star } ( \mathcal { D } \setminus \{ z _ { m } \} ) ) - f ( z _ { q } , \pmb { \theta } ^ { \star } )$$

其中 $\pmb{\theta}^\star$ 是在完整训练集 $\mathcal{D}$ 上训练得到的最优参数，$\pmb{\theta}^\star(\mathcal{D}\setminus\{z_m\})$ 是移除 $z_m$ 后重新训练得到的最优参数。直接计算该分数需要为每个训练样本重新训练模型，计算代价不可接受。

### 核心洞察：从展开微分到分段平稳近似

展开微分（unrolled differentiation）通过沿训练轨迹反向累积梯度信息来估计 $\frac{\mathrm{d}\pmb{\theta}_T}{\mathrm{d}\epsilon}$，能够精确捕捉学习率调度、优化器选择、训练阶段效应等细节。然而，展开微分需要存储**所有中间变量**，对现代深度学习模型而言计算和内存成本过高。

Source 的核心洞察是：**将训练轨迹划分为多个平稳段（stationary segments），在每个段内近似 Hessian 和梯度的统计分布，从而将展开微分的计算简化为仅需少量检查点的类影响函数公式**。具体而言，Source 假设在每个段 $\ell$ 内，Hessian 和梯度的分布近似平稳，因此可以用段内的期望值 $\bar{\mathbf{H}}_\ell$ 和 $\bar{\mathbf{g}}_\ell$ 替代逐迭代的计算。

### 关键公式推导

#### 1. SGD 更新规则与数据权重参数化

考虑带动量的小批量 SGD 更新：

$$\pmb { \theta } _ { k + 1 } = \pmb { \theta } _ { k } - \frac { \eta _ { k } } { B } \sum _ { i = 1 } ^ { B } \nabla _ { \pmb { \theta } } \mathcal { L } ( z _ { k i } , \pmb { \theta } _ { k } )$$

为建模移除训练样本 $z_m$ 的效应，引入权重扰动参数 $\epsilon$（当 $\epsilon=-1$ 时对应完全移除）：

$$\pmb{\theta}_{k+1}(\epsilon) = \pmb{\theta}_k(\epsilon) - \frac{\eta_k}{B} \sum_{i=1}^B (1 + \delta_{ki} \epsilon) \nabla_{\theta} \mathcal{L}(z_{ki}, \pmb{\theta}_k(\epsilon))$$

其中 $\delta_{ki}$ 是指示 $z_{ki}=z_m$ 的示性函数。

#### 2. 分段 Jacobian 的期望近似

将训练过程划分为 $L$ 个段，第 $\ell$ 段包含 $K_\ell$ 次迭代。该段的 Jacobian $\mathbf{S}_\ell$ 描述了段内参数变换对初始参数的敏感度。在分段平稳假设下，段内 Hessian 近似为常数 $\bar{\mathbf{H}}_\ell$，学习率近似为常数 $\bar{\eta}_\ell$，则段 Jacobian 的期望可近似为矩阵指数：

$$\mathbb { E } [ \mathbf { S } _ { \ell } ] \approx \left( \mathbf { I } - \bar { \eta } _ { \ell } \bar { \mathbf { H } } _ { \ell } \right) ^ { K _ { \ell } } \approx \exp ( - \bar { \eta } _ { \ell } K _ { \ell } \bar { \mathbf { H } } _ { \ell } ) : = \bar { \mathbf { S } } _ { \ell }$$

**变量含义**：$\bar{\eta}_\ell$ 是第 $\ell$ 段的平均学习率，$K_\ell$ 是该段的迭代次数，$\bar{\mathbf{H}}_\ell$ 是该段内 Hessian 的期望。矩阵指数形式使得计算可通过 Krylov 子空间方法高效实现，无需显式构造完整矩阵。

#### 3. 分段残差的期望近似

第 $\ell$ 段的残差 $\mathbf{r}_\ell$ 表示移除 $z_m$ 对该段参数更新的直接影响。在平稳假设下，其期望近似为阻尼逆 Hessian 向量积：

$$\mathbb { E } [ \mathbf { r } _ { \ell } ] \approx \frac { 1 } { N } ( \mathbf { I } - \exp ( - \bar { \eta } _ { \ell } K _ { \ell } \bar { \mathbf { H } } _ { \ell } ) ) \bar { \mathbf { H } } _ { \ell } ^ { - 1 } \bar { \mathbf { g } } _ { \ell } : = \bar { \mathbf { r } } _ { \ell }$$

**变量含义**：$N$ 是训练集大小，$\bar{\mathbf{g}}_\ell$ 是第 $\ell$ 段内 $z_m$ 上梯度的期望，$\bar{\mathbf{H}}_\ell^{-1}$ 是逆 Hessian（实际计算中使用阻尼版本以保证数值稳定性）。因子 $(\mathbf{I} - \exp(-\bar{\eta}_\ell K_\ell \bar{\mathbf{H}}_\ell))$ 反映了段内训练对该样本影响的衰减程度。

#### 4. Source 归因估计器

将各段的 Jacobian 视为统计独立，最终归因分数通过链式组合各段贡献得到：

$$\tau _ { \mathrm { S O U R C E } } ( z _ { q } , z _ { m } , \mathcal { D } ; \lambda ) : = \nabla _ { \theta } f ( z _ { q } , \theta ^ { s } ) ^ { \top } \left( \sum _ { \ell = 1 } ^ { L } \left( \prod _ { \ell ^ { \prime } = L } ^ { \ell + 1 } \bar { \mathbf { S } } _ { \ell ^ { \prime } } \right) \bar { \mathbf { r } } _ { \ell } \right)$$

**变量含义**：$\nabla_\theta f(z_q, \theta^s)$ 是查询样本在起始参数 $\theta^s$ 处的梯度；乘积 $\prod_{\ell'=L}^{\ell+1} \bar{\mathbf{S}}_{\ell'}$ 将第 $\ell$ 段的残差效应通过后续所有段的 Jacobian 传播到最终参数；$\bar{\mathbf{r}}_\ell$ 是第 $\ell$ 段的期望残差。该公式在形式上与影响函数 $\tau_{\mathrm{IF}} = \nabla_\theta f^\top \mathbf{H}^{-1} \nabla_\theta \mathcal{L}$ 相似，但通过分段机制自然地融入了训练轨迹信息。

### 关键实现模块

1. **训练轨迹分段**：将完整训练过程划分为 $L$ 个段（典型值 $L=3$），分段点可根据训练 epoch 或迭代数均匀划分。

2. **段内统计量计算**：在每个段内，基于少量检查点（例如 6 个，远小于总迭代数 $T$）计算平均 Hessian $\bar{\mathbf{H}}_\ell$、平均梯度 $\bar{\mathbf{g}}_\ell$ 和平均学习率 $\bar{\eta}_\ell$。Hessian 使用 EK-FAC 近似以降低存储和计算开销。

3. **段 Jacobian 近似**：通过矩阵指数 $\exp(-\bar{\eta}_\ell K_\ell \bar{\mathbf{H}}_\ell)$ 近似段 Jacobian 的期望，利用 Krylov 子空间方法高效计算矩阵指数与向量的乘积。

4. **段残差近似**：通过阻尼逆 Hessian 向量积 $(\mathbf{I} - \exp(-\bar{\eta}_\ell K_\ell \bar{\mathbf{H}}_\ell)) \bar{\mathbf{H}}_\ell^{-1} \bar{\mathbf{g}}_\ell$ 近似段残差的期望。

5. **归因分数合成**：按公式链式组合各段贡献，得到最终训练数据归因分数。



## 实验与关键发现

### 核心实验设置

实验评估围绕**线性数据建模分数（LDS）** 和**子集移除反事实评估**两个核心指标展开。LDS衡量TDA方法预测的归因分数与实际重训练模型输出变化之间的Spearman秩相关系数，数值越高表示归因越准确。实验在FashionMNIST、CIFAR-10、RotatedMNIST、RTE和WikiText-2等多个数据集上，覆盖图像分类、文本分类和语言建模等任务。

所有TDA方法均使用相同的6个模型检查点进行评估，确保比较公平性。在多模型融合设置中，除TRAK使用其特定的50%数据子集集成程序外，其他方法直接平均多个在全量数据上训练的模型的归因分数。

### 主要结果

**Source在FashionMNIST上显著优于所有基线方法。** 在单模型设置下，Source（L=3）的LDS达到0.46±0.01，而影响函数仅为0.30±0.01（Table 2）。在多模型融合设置下，Source的LDS进一步提升至0.53±0.01，影响函数为0.45±0.01。这一结果验证了分段平稳性近似在捕捉训练动态方面的有效性。

**Source在非收敛和多阶段训练设置中表现突出。** 在RotatedMNIST（多阶段训练）和FashionMNIST-N（非收敛训练）等挑战性设置中，Source始终优于所有隐式微分基线方法（Figure 7）。这些设置正是影响函数等传统方法的根本弱点——它们依赖模型收敛到唯一最优解的假设。Source通过分段框架，能够区分不同训练阶段的数据贡献，并处理未完全收敛的参数状态。

**子集移除反事实评估进一步验证了Source的实用性。** 在CIFAR-10和FashionMNIST上，Source预测的最具正面影响训练样本被移除后，能更有效地翻转测试预测结果（Figure 8）。这意味着Source识别的关键训练样本在实际数据移除场景中具有更强的因果效应，对于数据调试和模型行为理解具有直接应用价值。

### 消融实验

**分段数的影响。** 将分段数从L=1增加到L=3可以持续提高LDS评分（Figure 5），表明更细粒度的分段能更好地捕捉训练过程中的Hessian和梯度分布变化。这一趋势在多个α值下保持一致，验证了分段策略的有效性。

**Fast-Source的权衡。** 快速版本Fast-Source通过直接对分段内参数取平均来避免Hessian计算，虽然性能稍弱于标准Source，但仍优于影响函数和TracIn等基线（Figure 9）。这为计算资源受限的场景提供了一种实用的折中方案。

**非收敛程度的影响。** 在未完全收敛的线性模型上，Source相对于影响函数的LDS优势随训练迭代次数减少而扩大（Figure 10 Right）。当训练仅进行少量epoch时，影响函数的LDS急剧下降，而Source保持相对稳定。这直接验证了Source不依赖收敛假设的核心优势。

**收敛到最优解时的退化。** 当模型完全收敛到最优解时，影响函数本身的LDS很高，而Source和TracIn等基于中间检查点的方法则相对不适用（Figure 11）。这一现象符合理论预期：在最优解处，隐式微分的局部二次近似非常准确，而引入中间检查点的噪声反而降低了归因精度。

### 定性分析

Source在RTE文本蕴含任务中识别的正负影响样本具有可解释性（Table 3）。正面影响样本通常包含与查询样本相似的逻辑结构或关键词，而负面影响样本则呈现相反的蕴含关系或误导性语言模式。

在FashionMNIST和CIFAR-10图像分类任务中，Source识别的正面影响训练图像与查询图像在类别、纹理和形状上高度一致，而负面影响图像则来自不同类别或具有混淆特征（Figure 12-15）。与基线方法相比，Source的归因结果在视觉上更具判别性。

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2405_12186/figures/008_Figure.jpg]]

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2405_12186/figures/021_Figure.jpg]]

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2405_12186/figures/022_Figure.jpg]]

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2405_12186/figures/024_Figure.jpg]]

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2405_12186/figures/026_Figure.jpg]]

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2405_12186/figures/027_Figure.jpg]]

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2405_12186/figures/028_Figure.jpg]]

### 局限性与失败模式

**计算成本。** 相比同样使用EK-FAC近似的影响函数，Source的计算成本约为其C倍（C为所选检查点数量）。当C=6时已有明显额外开销，在大型模型上可能成为瓶颈。

**对训练过程信息的依赖。** Source需要访问训练过程中的中间检查点及相应的超参数（学习率、迭代次数等）。在无法获取训练细节的场景中（如仅提供最终模型权重），隐式微分方法（如TRAK或影响函数）可能更适用。

**分段平稳性假设的边界。** 当训练过程中Hessian或梯度发生剧烈变化时，分段平稳性假设可能不准确，需要更多分段来修正。如何自动确定分段点仍需进一步研究——当前方法依赖人工设定分段数和分段位置。

### 补充图表

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2405_12186/figures/007_Figure_6.jpg]]
*Figure 6: Linear datamodeling scores (LDS) at α = 0.5 for Source (L = 3) and baseline TDA techniques on regression, image classification, text classification, and language modeling tasks. The error bars represent 95% bootstrap confidence intervals. (Results for Trak on WikiText-2 are omitted due to the lack of publicly available implementations for language modeling tasks.)*

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2405_12186/figures/013_Figure_10.jpg]]
*Figure 10: (Left & Middle) Linear datamodeling scores (LDS) for various values of data sampling ratios α on linear regression and logistic regression tasks trained for 3 epochs. (Right) The LDS at $\alpha$ = 0 . 9 for models trained with varying numbers of epochs. The error bars show 95% bootstrap confidence intervals*

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2405_12186/figures/014_Figure_11.jpg]]
*Figure 11: Linear datamodeling scores (LDS) on linear regression and logistic regression tasks for influence functions when TDA is performed on the optimal solution*

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2405_12186/figures/017_Figure.jpg]]
*Figure: Top Positively Influential Images Top Negatively Influential Images*

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2405_12186/figures/018_Figure.jpg]]
*Figure: Top Negatively Influential Images*



## 定位与知识库关联

### 1. 问题域定位：训练数据归因的两条技术路径

训练数据归因（Training Data Attribution, TDA）的核心目标是估计单个训练样本对模型在特定测试样本上预测的影响。现有方法可大致分为两条技术路径：**隐式微分**（implicit differentiation）和**展开微分**（unrolled differentiation）。Source 的提出正是为了在这两条路径的根本权衡中找到一个可操作的平衡点。

**隐式微分路径**以影响函数（**Influence Functions**, Koh and Liang, ICML 2017）为代表。该方法假设训练收敛到损失函数的唯一最优解，利用最优性条件（梯度为零）推导出移除一个训练样本对最优参数的一阶近似，从而避免了对整个训练轨迹的显式求导。其核心公式为：

$$\tau _ { \mathrm { I F } } ( z _ { q } , z _ { m } , \mathcal { D } ) : = \nabla _ { \boldsymbol { \theta } } f ( z _ { q } , \boldsymbol { \theta } ^ { \star } ) ^ { \top } \mathbf { H } ^ { - 1 } \nabla _ { \boldsymbol { \theta } } \mathcal { L } ( z _ { m } , \boldsymbol { \theta } ^ { \star } )$$

这一路径的优势在于计算高效——仅需最终模型参数和一次逆Hessian向量积计算。然而，其根本局限在于**依赖收敛假设**：当模型未完全收敛、使用多阶段训练策略、或优化器的隐式偏差对最终解有显著影响时，最优性条件不再成立，影响函数的估计会产生系统性偏差。

**展开微分路径**则通过对整个训练过程的计算图进行反向自动微分，精确计算最终参数对训练数据权重变化的敏感度。这类方法能够完整捕捉学习率调度、优化器选择和训练阶段效应等信息。但代价是**需要存储所有中间变量**，计算和内存成本随训练步数线性增长。**Hydra**（Chen et al., NeurIPS 2021）试图通过近似展开来加速这一过程，但仍未从根本上解决存储瓶颈。

### 2. Source 的方法学定位：分段平稳近似下的展开-隐式融合

Source 的核心洞察在于：**通过将训练轨迹划分为若干平稳段，可以在段内用统计量（平均梯度、平均Hessian、平均学习率）近似展开微分的计算，从而将存储需求从全部中间检查点降至仅需少量段边界检查点**。

具体而言，Source 将训练过程划分为 $L$ 个段，在每个段 $\ell$ 内假设梯度和Hessian的分布平稳，进而用矩阵指数近似该段的期望Jacobian：

$$\mathbb { E } [ \mathbf { S } _ { \ell } ] \approx \left( \mathbf { I } - \bar { \eta } _ { \ell } \bar { \mathbf { H } } _ { \ell } \right) ^ { K _ { \ell } } \approx \exp ( - \bar { \eta } _ { \ell } K _ { \ell } \bar { \mathbf { H } } _ { \ell } ) : = \bar { \mathbf { S } } _ { \ell }$$

以及期望残差：

$$\mathbb { E } [ \mathbf { r } _ { \ell } ] \approx \frac { 1 } { N } ( \mathbf { I } - \exp ( - \bar { \eta } _ { \ell } K _ { \ell } \bar { \mathbf { H } } _ { \ell } ) ) \bar { \mathbf { H } } _ { \ell } ^ { - 1 } \bar { \mathbf { g } } _ { \ell } : = \bar { \mathbf { r } } _ { \ell }$$

最终归因分数通过组合各段贡献得到：

$$\tau _ { \mathrm { S O U R C E } } ( z _ { q } , z _ { m } , \mathcal { D } ; \lambda ) : = \nabla _ { \theta } f ( z _ { q } , \theta ^ { s } ) ^ { \top } \left( \sum _ { \ell = 1 } ^ { L } \left( \prod _ { \ell ^ { \prime } = L } ^ { \ell + 1 } \bar { \mathbf { S } } _ { \ell ^ { \prime } } \right) \bar { \mathbf { r } } _ { \ell } \right)$$

这一公式在形式上与影响函数类似，但通过分段结构保留了优化轨迹的关键信息。

从方法谱系看，Source 占据了一个独特的中间位置：
- **相比隐式微分方法**（影响函数、**TRAK** (Park et al., ICML 2023)），Source 不依赖收敛假设，能够处理非收敛训练和多阶段训练场景。
- **相比纯展开微分方法**，Source 仅需 $C$ 个检查点（实验中 $C=6$），远小于总迭代数 $T$，大幅降低了存储和计算成本。
- **相比基于中间检查点的启发式方法**（如 **TracIn** (Pruthi et al., NeurIPS 2020) 直接使用检查点梯度内积），Source 有更严格的理论推导，能够正确组合各段的贡献。

### 3. 与具体基线工作的关系

- **TracIn**（Pruthi et al., NeurIPS 2020）：该方法通过累加多个检查点处查询样本梯度与训练样本梯度的内积来计算归因分数。Source 与 TracIn 同样使用了中间检查点，但 Source 通过分段平稳近似推导出了Jacobian链式组合的闭合形式，而非简单的梯度内积累加。消融实验（Figure 9）表明，Source 显著优于 TracIn。

- **TRAK**（Park et al., ICML 2023）：该方法通过随机投影和模型集成来估计归因分数，本质上也属于隐式微分范式。TRAK 的优势在于不需要访问训练中间状态，适用于无法获取训练细节的场景。但实验表明，在可获取检查点的设置下，Source 的归因准确性更高。

- **Downsampling**（Feldman and Zhang, NeurIPS 2020）：通过在不同数据子集上重训练来经验性地估计数据影响，可视为归因的“黄金标准”近似。Source 在 FashionMNIST 上的 LDS 与 Downsampling 可比（Table 2），但计算成本远低于后者。

- **RepSim**（Caruana et al., 1999）：基于表示相似度的简单基线，在复杂任务上通常显著弱于基于梯度的方法。

### 4. 适用边界与局限

**适用场景**：
- 可访问训练过程中的中间检查点及超参数（学习率、批大小、迭代数）。
- 训练未完全收敛或多阶段训练（如持续学习、课程学习）。
- 需要反事实预测准确性较高的归因分析。

**不适用或需谨慎使用的场景**：
- 无法获取训练中间状态的场景（此时 TRAK 或影响函数更适用）。
- 模型已完全收敛到唯一最优解时，影响函数本身已有较高准确性，Source 的额外计算开销可能不划算（Figure 11 显示此时影响函数的 LDS 很高）。
- Hessian 或梯度在训练过程中剧烈变化时，分段平稳性假设可能不准确，需要更多分段来修正，但会增加计算成本。如何自动确定分段点仍是开放问题。

**计算成本**：相比同样使用 EK-FAC 近似的影响函数，Source 的计算成本约为其 $C$ 倍（$C$ 为所选检查点数量）。当 $C=6$ 时已有明显额外开销，在大型模型上可能成为瓶颈。

### 5. 开放问题

1. **自适应分段**：如何根据 Hessian 或梯度的变化自动确定分段点，以平衡归因准确度与计算成本？
2. **大规模预训练模型**：Source 在 LLaMA、GPT 等大型预训练模型上的可扩展性如何？分段平稳性假设在预训练-微调范式中是否仍然成立？
3. **与随机投影结合**：能否将 Source 与 TRAK 所用的随机投影技术结合，进一步降低高维参数空间中的存储和计算需求？
4. **自适应优化器**：在 Adam 等自适应学习率优化器下，平稳性近似引起的偏差有多大？如何针对自适应优化器改进近似方案？
5. **快速版本的理论分析**：Fast-Source 通过直接平均参数来减少计算，但归因准确性有所下降（Figure 9）。其理论误差界尚待建立。



## 原文 PDF

![[paperPDFs/NEURIPS_2024/Training_Data_Attribution_via_Approximate_Unrolled_Differentiation.pdf]]
