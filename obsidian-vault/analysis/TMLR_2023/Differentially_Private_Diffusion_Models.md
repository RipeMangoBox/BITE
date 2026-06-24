---
title: "Differentially Private Diffusion Models"
type: paper
paper_level: A
venue: TMLR
year: 2023
pdf_ref: paperPDFs/TMLR_2023/Differentially_Private_Diffusion_Models.pdf
project_link: https://github.com/nv-tlabs/DPDM
aliases:
- DPDMD
- DPDM
tags:
- TMLR_2023
- topic/generative_models_diffusion
- topic/generative_models_diffusion/generative_models_and_autoencoders
core_operator: "噪声多重性（K值）通过降低目标方差来调节训练效率；DM配置（训练噪声分布p(σ)的权重）影响模型对全局结构的学习；随机采样器的选择（如Churn采样器）通过增加随机性提升感知质量。"
primary_logic: "扩散模型的去噪网络结构简单平滑，因此在DP训练中比GAN更容易优化；噪声多重性通过对每个样本的多个噪声扰动取平均，在不增加隐私成本的前提下有效降低损失方差；赋予高噪声水平更多训练权重有助于在强隐私条件下捕捉数据宏观结构，从而提升生成质量和下游效用。"
claims:
- "噪声多重性在不增加隐私成本的情况下，将DM训练目标方差降低1/K。"
- "在MNIST数据集上，DPDM在隐私预算ε=1时，将最优FID从56.2降至23.4，下游CNN分类准确率从81.5%提升至95.3%。"
- "在强隐私（ε=0.2）下，采用v-prediction噪声分布配置相比EDM配置显著提升FID和下游准确率。"
- "随机采样（Churn采样器）对于DP训练扩散模型的感知质量（FID）至关重要。"
---

# Differentially Private Diffusion Models

> [!tip] 核心洞察
> 扩散模型的去噪网络结构简单平滑，因此在DP训练中比GAN更容易优化；噪声多重性通过对每个样本的多个噪声扰动取平均，在不增加隐私成本的前提下有效降低损失方差；赋予高噪声水平更多训练权重有助于在强隐私条件下捕捉数据宏观结构，从而提升生成质量和下游效用。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 差分隐私扩散模型 |
| 英文题名 | Differentially Private Diffusion Models |
| 会议/期刊 | TMLR 2023 |
| Links | [paper](https://arxiv.org/abs/2210.09929); [Project](https://nv-tlabs.github.io/DPDM); [GitHub](https://github.com/nv-tlabs/DPDM) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/generative_models_and_autoencoders |
| Method | Differentially Private Diffusion Models (DPDMs) |
| Dataset | MNIST (class-conditional) |

> [!tip] 效果简介
> - MNIST (class-conditional) 上，FID ↓ 为 23.4，对比 56.2，变化 -32.8。
> - MNIST (class-conditional) 上，CNN accuracy ↑ 为 95.3%，对比 81.5%，变化 +13.8%。

## 概述

在差分隐私（Differential Privacy, DP）约束下训练生成模型面临一个根本性瓶颈：DP-SGD 的梯度剪裁与噪声注入导致训练目标具有高方差，使得模型在有限隐私预算内难以有效学习数据的全局结构。这一问题在高噪声水平下的扩散模型训练中尤为突出。本文提出**差分隐私扩散模型（Differentially Private Diffusion Models, DPDMs）**，通过三个关键设计突破上述瓶颈：

1. **噪声多重性（Noise Multiplicity）**：对每个训练样本采样 $K$ 个噪声扰动并取平均，在不增加隐私成本的前提下将训练目标方差降低至 $1/K$（Theorem 1），从而显著提升训练效率。
2. **训练噪声分布重加权**：赋予高噪声水平 $\sigma$ 更多训练权重（如 v-prediction 配置），使模型在强隐私约束下优先捕捉数据宏观结构，而非陷入细节噪声。
3. **随机采样器**：采用 Churn 采样器（SDE）替代确定性 DDIM（ODE），通过引入受控随机性弥补 DP 训练导致的感知质量损失。

**核心洞察**：扩散模型的去噪网络结构简单平滑（其雅可比范数显著低于 GAN 生成器），天然适配 DP-SGD 的低复杂度优化特性；噪声多重性则利用扩散过程的固有扰动机制，在不消耗额外隐私预算的前提下有效抑制梯度方差。

**主要结果**：在 MNIST 数据集上，DPDM 在隐私预算 $\varepsilon=1$ 时将最优 FID 从 56.2 降至 23.4，下游 CNN 分类准确率从 81.5% 提升至 95.3%；在 Fashion-MNIST、CelebA 等数据集上同样取得显著提升。该方法在强隐私（$\varepsilon=0.2$）下仍能保持合理的生成质量与下游效用。

**方法定位**：DPDM 属于差分隐私生成模型谱系中的扩散模型分支，相较于 DP-GAN 系列方法（如 DP-CGAN、GS-WGAN、DataLens、G-PATE）和一次性私有化方法（如 DP-MERF、PEARL），其优势在于利用扩散过程的多步去噪机制和 L2 损失的平滑性，在同等隐私预算下实现更优的分布学习。

## 背景与动机

### 差分隐私生成建模的核心矛盾

在敏感数据（如医疗记录、金融交易、个人图像）上训练生成模型时，差分隐私（Differential Privacy, DP）提供了严格的隐私保障——它确保任意单个训练样本的存在与否不会显著改变模型输出。形式化地，一个随机机制 $\mathcal{M}$ 满足 $(\varepsilon, \delta)$-DP，当且仅当对所有相邻数据集 $d, d'$ 和输出子集 $S$，有：

$$\mathbf{Pr}[\mathcal{M}(d) \in S] \le e^{\varepsilon}\mathbf{Pr}[\mathcal{M}(d') \in S] + \delta$$

然而，将这一约束施加到深度生成模型上，暴露了一个根本性的张力：**隐私保护要求对梯度进行剪裁和加噪，这直接导致训练信号的高方差，而生成模型恰恰需要从数据中捕捉精细的全局结构。** 在有限的隐私预算（$\varepsilon$ 较小）下，这种高方差使得模型难以收敛到有意义的解。

### 现有方法的困境

此前，差分隐私生成建模的主流范式集中在生成对抗网络（GAN）上。代表性工作包括 **DP-CGAN**（Torkzadehmahani et al., 2019）、**G-PATE**（Long et al., 2019）、**GS-WGAN**（Chen et al., 2020）、**DataLens**（Wang et al., 2021）和 **DPGANr**（Bie et al., 2022）等。这些方法在 DP 框架下对 GAN 的训练过程进行适配，但在强隐私约束下（如 $\varepsilon=1$）普遍面临生成质量急剧下降的问题。以 MNIST 数据集为例，此前最优的 DP 生成模型 FID 仍高达 56.2，下游分类准确率仅 81.5%，与无隐私模型之间存在巨大鸿沟。

另一类方法走“一次性私有化”（one-shot privatization）路线，如 **DP-MERF**（Harder et al., 2021）和 **PEARL**（Liew et al., 2022），它们在单次数据发布阶段注入噪声，随后在私有化表示上训练模型。这类方法虽然计算高效，但生成质量通常受限于私有化过程中的信息损失。此外，**DP-MEPF**（Harder et al., 2022）引入了额外的公开数据辅助训练，这在许多实际场景中并不可行。

### 为什么扩散模型适合 DP 训练？

本文的核心动机源自一个关键观察：**扩散模型（Diffusion Models, DMs）的去噪网络本质上比 GAN 的生成器“更简单”。** 具体而言，DM 训练使用的是回归式的 L2 损失：

$$\mathbb{E}_{\mathbf{x} \sim p_{\mathrm{data}}(\mathbf{x}), (\sigma, \mathbf{n}) \sim p(\sigma, \mathbf{n})} \left[ \lambda_{\sigma} \| D_{\theta}(\mathbf{x} + \mathbf{n}, \sigma) - \mathbf{x} \|_2^2 \right]$$

这一目标函数平滑且稳定，而去噪网络 $D_\theta$ 只需学习从噪声图像到干净图像的映射——这是一个局部、增量式的任务。相比之下，GAN 生成器必须一次性从随机噪声映射到完整图像，其函数复杂度显著更高。

作者通过雅可比矩阵的 Frobenius 范数量化了这一差异（Figure 2）：在二维玩具分布（高斯混合）上，DM 去噪器 $D(\cdot, \sigma)$ 的雅可比范数 $I_F(\sigma)$ 在不同噪声水平 $\sigma$ 下均显著低于 GAN 生成器的对应值。这意味着去噪网络学到的函数更平滑、更简单，因此在 DP-SGD 的梯度扰动下更不易崩溃。

### 核心瓶颈：高方差与全局结构学习的冲突

尽管 DM 架构本身对 DP 训练友好，但直接将 DP-SGD 应用于标准 DM 训练仍面临严峻挑战。DP-SGD 的参数更新规则为：

$$\pmb{\theta} \gets \pmb{\theta} - \frac{\eta}{B} \left( \sum_{i \in \mathbb{B}} \mathsf{clip}_C(\nabla_{\pmb{\theta}} l_i(\pmb{\theta})) + C \mathbf{z} \right)$$

其中梯度剪裁（常数 $C$）和高斯噪声 $\mathbf{z}$ 共同限制了每个样本对模型更新的影响。问题在于，标准 DM 训练中每个样本仅使用一个噪声扰动：

$$l_i = \lambda(\sigma_i) \lVert D_{\pmb{\theta}}(\mathbf{x}_i + \mathbf{n}_i, \sigma_i) - \mathbf{x}_i \rVert_2^2$$

这导致单次梯度估计的方差极高——尤其是在高噪声水平 $\sigma$ 下，去噪目标本身的不确定性就很大。当隐私预算收紧时，DP-SGD 注入的额外噪声与这种固有方差叠加，使得模型几乎无法从数据中学习到全局结构。**这就是本文所要解决的核心瓶颈：在 DP 约束下，如何降低训练目标的高方差，从而让扩散模型在有限隐私预算内有效捕捉数据的宏观分布。**

## 核心创新

DPDM 的核心创新并非提出全新的模型架构，而是通过三个低成本、高回报的“改造槽位”（changed slots），将差分隐私训练与扩散模型的固有特性深度耦合，从而在有限隐私预算下大幅释放扩散模型的生成潜力。其本质是**在 DP-SGD 的刚性约束下，通过降低训练目标方差和引导模型学习全局结构，绕开扩散模型高噪声训练阶段的脆弱性**。

### 1. 噪声多重性：零隐私成本下的方差压缩

这是 DPDM 最关键的创新。标准非隐私扩散模型对每个数据点仅采样一次噪声扰动（Eq. 6），但在 DP-SGD 下，该目标的梯度方差极大，导致训练信号被隐私噪声淹没。DPDM 提出**噪声多重性**（noise multiplicity）：对每个数据点 $\mathbf{x}_i$，独立采样 $K$ 组噪声扰动 $(\sigma_{ik}, \mathbf{n}_{ik})$，计算平均损失作为该样本的代理目标：

$$\widetilde{l}_i = \frac{1}{K} \sum_{k=1}^{K} \lambda(\sigma_{ik}) \| D_{\theta}(\mathbf{x}_i + \mathbf{n}_{ik}, \sigma_{ik}) - \mathbf{x}_i \|_2^2$$

这一操作的因果机制在于：**DP-SGD 的隐私保证仅作用于单个数据点的梯度贡献边界**。对同一样本的多次扰动取平均，并未增加隐私成本（每个样本仍贡献一个梯度向量），但通过蒙特卡洛平均将目标的方差降低了 $1/K$（Theorem 1，置信度 0.98）。这直接缓解了扩散模型在高噪声水平下训练信号极弱的核心瓶颈。消融实验表明，在 MNIST 上 $K$ 从 1 增至 32 时，FID 和下游分类准确率持续改善（Table 11），梯度估计方差呈对数级下降（Figure 3/6）。

### 2. 训练噪声分布重加权：引导模型捕捉全局结构

非隐私扩散模型的噪声分布 $p(\sigma)$ 通常采用 VP/VE 配置，对高噪声水平（大 $\sigma$）赋予较低权重。DPDM 发现，**在强隐私约束下（如 $\varepsilon=0.2$），这一配置是灾难性的**——模型在高噪声阶段几乎无法获得有效学习信号，导致全局结构坍塌。DPDM 的解决方案是采用 **v-prediction 配置**，显著增加高噪声水平的采样权重（Figure 4），迫使模型在有限的隐私预算内优先学习数据的宏观结构（如数字轮廓、人脸布局）。在 MNIST $\varepsilon=0.2$ 的消融中，v-prediction 配置在 FID 和下游准确率上均显著优于 EDM 配置（Table 3，置信度 0.95）。这一设计利用了扩散模型的去噪网络在不同噪声水平上参数共享的特性，使得高噪声阶段的学习能够正向迁移到低噪声阶段。

### 3. 随机采样器：弥补 DP 训练的去噪偏差

DP-SGD 训练的去噪网络倾向于产生平滑、保守的预测，这在确定性采样（如 DDIM）下会导致生成样本缺乏细节和多样性。DPDM 引入 **Churn 随机采样器**（Karras et al., 2022），在去噪过程中注入受控的朗之万扩散噪声，有效提升了感知质量。Table 6 显示，Churn 采样器在 FID 上大幅优于 DDIM，而经过专门调参的 DDIM 则在下游分类准确率上更有优势——这表明**采样策略的选择本质上是感知质量与语义保真度之间的权衡**，且该权衡在 DP 训练下被放大。

### 4. 网络架构的隐性适配：小网络反直觉的优势

与 GAN 追求大容量生成器的趋势相反，DPDM 在 MNIST 上仅使用约 1.75M 参数的小型去噪网络（DDPM++）。这一设计的逻辑链是：DP-SGD 注入的噪声量与模型参数维度正相关，**小网络直接降低了隐私噪声的绝对量级**。同时，Figure 2 的雅可比范数分析证实，扩散模型的去噪器网络函数复杂度远低于 GAN 生成器，因此即使在 DP 训练下也不易陷入模式坍塌。这与“噪声多重性降低方差”形成互补——前者控制噪声来源的规模，后者压缩噪声对梯度的相对影响。

### 创新之间的因果联动

上述四个槽位并非孤立改进，而是形成了一条因果链：**噪声多重性降低高噪声水平的梯度方差 → 重加权噪声分布确保该阶段的训练信号被有效利用 → 随机采样器在推理时补偿 DP 训练的去噪偏差 → 小网络为整个流程提供可承受的隐私噪声基底**。这一联动机制解释了为何 DPDM 能在 $\varepsilon=1$ 时将 MNIST 的 FID 从 56.2 降至 23.4，下游分类准确率从 81.5% 提升至 95.3%（置信度 0.95）。

## 整体框架

DPDM的训练与生成流程由四个核心模块串联构成，整体遵循“数据扰动→去噪预测→差分隐私优化→迭代采样”的信息流，如Figure 1所示。

**模块1：数据与噪声采样（Data & noise sampling）**  
对每个训练样本 $\mathbf{x}_i$，从噪声分布 $p(\sigma)$ 中独立采样 $K$ 组噪声水平 $\sigma_{ik}$ 和对应的高斯噪声 $\mathbf{n}_{ik} \sim \mathcal{N}(\mathbf{0}, \sigma_{ik}^2\mathbf{I})$，构造 $K$ 个扰动版本 $\mathbf{x}_i + \mathbf{n}_{ik}$。这 $K$ 个扰动输入共享同一个干净目标 $\mathbf{x}_i$，构成噪声多重性（noise multiplicity）机制的核心——其理论依据为Theorem 1所证明的方差降低效应：DM训练目标的方差随 $K$ 增大以 $1/K$ 的比例衰减，而隐私成本不增加。

**模块2：去噪器网络 $D_\theta$（Denoiser network）**  
采用DDPM++架构的去噪器网络 $D_\theta(\mathbf{x}+\mathbf{n}, \sigma)$ 接收扰动图像和噪声水平 $\sigma$，预测对应的干净图像。该网络是DPDM中唯一需要学习的组件。与GAN生成器相比，去噪器网络的雅可比Frobenius范数 $\mathcal{I}_F(\sigma)$ 显著更低（Figure 2），表明其函数复杂度更小、映射更平滑，这一特性使其在DP-SGD的梯度剪裁和噪声注入下更易优化，构成扩散模型天然适合差分隐私训练的关键动机。

**模块3：DP-SGD优化器（DP-SGD optimizer）**  
训练使用差分隐私随机梯度下降。对每个样本，先计算其噪声多重性损失：
$$\widetilde{l}_i = \frac{1}{K} \sum_{k=1}^{K} \lambda(\sigma_{ik}) \| D_\theta(\mathbf{x}_i + \mathbf{n}_{ik}, \sigma_{ik}) - \mathbf{x}_i \|_2^2$$
然后对每个样本的梯度 $\nabla_\theta \widetilde{l}_i$ 进行范数剪裁（剪裁常数 $C=1$），在批次内求和后注入高斯噪声，完成参数更新：
$$\theta \gets \theta - \frac{\eta}{B} \left( \sum_{i \in \mathbb{B}} \mathsf{clip}_C(\nabla_\theta \widetilde{l}_i) + C\mathbf{z} \right)$$
其中 $\mathbf{z} \sim \mathcal{N}(\mathbf{0}, \sigma_{\text{DP}}^2\mathbf{I})$ 的方差由隐私预算 $(\varepsilon, \delta)$ 决定。关键超参数选择包括：极大批次大小（MNIST/Fashion-MNIST上为4096，CelebA上为2048）以降低噪声相对幅度；固定剪裁常数 $C=1$；以及使用Adam作为底层优化器。

**模块4：采样器（Sampler）**  
训练完成后，从随机高斯噪声出发，利用训练好的去噪器 $D_\theta$ 迭代去噪生成图像。DPDM支持两种采样范式：
- **确定性采样**：基于概率流ODE（Eq. (1)），对应DDIM采样器，生成过程完全确定。
- **随机采样**：基于SDE的Churn采样器，在去噪过程中注入额外随机性。实验表明，随机采样对DP训练扩散模型的感知质量（FID）至关重要——Table 6显示Churn采样器在FID指标上显著优于确定性DDIM，而针对下游分类准确率可独立调优采样策略。

**训练噪声分布 $p(\sigma)$ 的关键作用**  
噪声水平的采样分布 $p(\sigma)$ 是连接模块1和模块3的隐式调控旋钮。Figure 4展示了不同DM配置下的 $p(\sigma)$ 差异：v-prediction配置赋予高噪声水平（大 $\sigma$）更大采样权重，这有助于模型在强隐私约束下优先捕捉数据的全局结构。Table 3的消融实验证实，在严格隐私预算（$\varepsilon=0.2$）下，v-prediction配置相比EDM配置在FID和下游分类准确率上均有显著提升——这是因为高噪声水平下的训练信号更关注宏观模式，对DP噪声的鲁棒性更强。

整体而言，DPDM通过噪声多重性降低训练目标方差、通过小容量去噪器网络适配DP-SGD的噪声缩放特性、通过重尾噪声分布引导模型学习全局结构，三者协同实现了差分隐私约束下扩散模型的有效训练。

### 补充图表

![[assets/figures/papers/paper_list_l42_https_arxiv_org_abs_2210_09929/figures/031_Figure_18.jpg]]
*Figure 18: Additional experiments on CelebA at higher resolution (64x64). Samples from our method and DataLens (Wang et al., 2021)*

## 核心模块与公式推导

### 3.1 差分隐私扩散模型的训练架构

DPDM的训练流程由四个核心模块串联构成，如**Figure 1**所示：

**模块一：数据与噪声多重采样**
对每个训练样本 $\mathbf{x}_i$，从噪声分布 $p(\sigma)$ 中独立采样 $K$ 对扰动参数 $(\sigma_{ik}, \mathbf{n}_{ik})$，其中 $\mathbf{n}_{ik} \sim \mathcal{N}(\mathbf{0}, \sigma_{ik}^2 \mathbf{I})$。这 $K$ 个噪声扰动共享同一干净图像，构成**噪声多重性**（noise multiplicity）机制。

**模块二：去噪网络 $D_\theta$**
采用DDPM++架构的去噪器，输入为加噪图像 $\mathbf{x}_i + \mathbf{n}_{ik}$ 和噪声水平 $\sigma_{ik}$，输出对干净图像的预测 $D_\theta(\mathbf{x}_i + \mathbf{n}_{ik}, \sigma_{ik})$。网络同时接收类别嵌入以实现条件生成。

**模块三：DP-SGD优化器**
对每个样本的 $K$ 个扰动损失取平均后，计算梯度并按范数 $C$ 剪裁，再注入高斯噪声 $\mathbf{z} \sim \mathcal{N}(\mathbf{0}, C^2 \mathbf{I})$，以Adam更新参数。训练使用极大批次（MNIST/Fashion-MNIST为4096，CelebA为2048）和固定剪裁常数 $C=1$。

**模块四：采样器**
从初始高斯噪声出发，利用训练好的 $D_\theta$ 迭代去噪。支持确定性ODE采样（DDIM）和随机SDE采样（Churn采样器），可结合无分类器引导提升质量。

### 3.2 关键公式

**标准去噪损失（非隐私）**

$$
l_i = \lambda(\sigma_i) \lVert D_{\boldsymbol{\theta}}(\mathbf{x}_i + \mathbf{n}_i, \sigma_i) - \mathbf{x}_i \rVert_2^2 \tag{6}
$$

其中 $\lambda(\sigma_i)$ 为噪声水平相关的权重函数，$\mathbf{n}_i \sim \mathcal{N}(\mathbf{0}, \sigma_i^2 \mathbf{I})$ 为单次噪声采样。该损失对每个样本仅使用一个噪声扰动。

**噪声多重性损失**

$$
\widetilde{l}_i = \frac{1}{K} \sum_{k=1}^{K} \lambda(\sigma_{ik}) \| D_{\boldsymbol{\theta}}(\mathbf{x}_i + \mathbf{n}_{ik}, \sigma_{ik}) - \mathbf{x}_i \|_2^2 \tag{7}
$$

**变量含义**：$K$ 为噪声多重数；$\sigma_{ik} \sim p(\sigma)$ 为第 $k$ 个噪声水平；$\mathbf{n}_{ik} \sim \mathcal{N}(\mathbf{0}, \sigma_{ik}^2 \mathbf{I})$ 为对应的噪声扰动。该公式通过对 $K$ 个独立噪声扰动下的去噪损失取平均，在不增加隐私成本的前提下将目标方差降低至原来的 $1/K$（**Theorem 1**）。

**DP-SGD参数更新**

$$
\boldsymbol{\theta} \gets \boldsymbol{\theta} - \frac{\eta}{B} \left( \sum_{i \in \mathbb{B}} \mathsf{clip}_C(\nabla_{\boldsymbol{\theta}} \widetilde{l}_i(\boldsymbol{\theta})) + C \mathbf{z} \right) \tag{5}
$$

**变量含义**：$\eta$ 为学习率；$B$ 为批次大小；$\mathbb{B}$ 为当前批次索引集；$\mathsf{clip}_C(\cdot)$ 将梯度范数剪裁至 $C$；$\mathbf{z} \sim \mathcal{N}(\mathbf{0}, \mathbf{I})$ 为标准高斯噪声。该更新规则是DP-SGD的标准形式，将式(7)的噪声多重性损失代入后即构成DPDM的完整优化过程。

**概率流ODE（确定性采样）**

$$
d\mathbf{x} = -\dot{\sigma}(t) \sigma(t) \nabla_{\mathbf{x}} \log p(\mathbf{x}; \sigma(t)) dt \tag{1}
$$

该常微分方程定义了扩散模型从噪声到数据的确定性映射，其中 $\nabla_{\mathbf{x}} \log p(\mathbf{x}; \sigma(t))$ 为分数函数，可通过训练好的去噪器 $D_\theta$ 间接获得。

### 3.3 方差缩减机制

噪声多重性的核心理论保证由**Theorem 1**给出：在固定数据集和噪声分布 $p(\sigma)$ 的条件下，式(7)的方差随 $K$ 增大以 $1/K$ 的速率衰减。**Figure 3**（放大版见**Figure 6**）的实验验证显示，参数梯度估计的方差随 $K$ 增加呈对数线性下降，与理论预测一致。这一机制使得DPDM在有限隐私预算下仍能获得低方差的训练信号，是其在强隐私约束下显著优于GAN类方法的关键原因。

## 实验与分析

### 核心实验设置

DPDM 在三个数据集上评估：MNIST（类条件）、Fashion-MNIST（类条件）和 CelebA（无条件，32×32）。隐私预算覆盖 ε ∈ {10, 1, 0.2}，其中 MNIST/Fashion-MNIST 使用 δ = 10⁻⁵，CelebA 使用更严格的 δ = 10⁻⁶。训练采用 DP-SGD，统一使用梯度剪裁常数 C = 1，大批量尺寸（MNIST/Fashion-MNIST 为 4096，CelebA 为 2048），噪声多重性默认 K = 32。网络架构为 DDPM++，MNIST 上仅约 1.75M 参数，远小于非隐私扩散模型的典型配置，以适应 DP-SGD 的内存和噪声放大效应（Table 8）。

![[assets/figures/papers/paper_list_l42_https_arxiv_org_abs_2210_09929/figures/013_Table_8.jpg]]
*Table 8: Model hyperparameters and training details*

### 主结果：图像生成质量

**Table 1** 汇总了类条件 DP 图像生成性能。在 MNIST 上，DPDM 在 ε = 1 时将 FID 从先前最优的 56.2 降至 23.4（降幅 58.4%），在 ε = 10 时达到 9.8。Fashion-MNIST 上同样取得显著提升：ε = 1 时 FID 为 23.6，ε = 10 时降至 10.1。对比基线包括 DP-CGAN（Torkzadehmahani et al., 2019）、DP-MERF（Harder et al., 2021）、DataLens（Wang et al., 2021）、G-PATE（Long et al., 2019）、GS-WGAN（Chen et al., 2020）、DP-Sinkhorn（Cao et al., 2021）、PEARL（Liew et al., 2022）和 DPGANr（Bie et al., 2022）。其中 PEARL 的结果由作者使用官方代码复现以确保公平比较；DP-MEPF（Harder et al., 2022）因使用额外公开数据训练，仅作参考列出。

**公平性说明**：G-PATE 和 DataLens 在 CelebA 上使用 δ = 10⁻⁵（隐私性弱于 DPDM 的 δ = 10⁻⁶）且处理 64×64 图像，而 DPDM 处理 32×32，因此直接数值对比需谨慎。部分基线结果直接取自原论文，评估协议可能存在差异。

### 主结果：下游分类效用

**Table 2** 展示了生成数据用于下游分类器训练的效果。在 MNIST 上，DPDM 合成数据训练的 CNN 在 ε = 1 时达到 95.3% 的分类准确率，显著优于先前最优的 81.5%，甚至超过直接在真实数据上用 DP-SGD 训练的分类器（92.1%）。Fashion-MNIST 上同样观察到一致优势：DPDM 合成数据训练的准确率（78.1%）超过 DP-SGD 直接训练（76.0%）和所有其他 DP 生成基线。这表明 DPDM 生成的样本不仅视觉质量更高，而且保留了更多对下游任务有用的类别判别信息。

### 无条件 CelebA 结果

**Table 4** 显示，在 CelebA 32×32 无条件生成任务上，DPDM 在 ε = 10 时 FID 为 23.8，优于 DP-MERF（37.9）和 PEARL（28.6）。在更强隐私 ε = 1 下，FID 为 38.2。值得注意的是，DPDM 在 CelebA 上的优势幅度小于 MNIST/Fashion-MNIST，且生成图像仍主要捕捉肤色、光照等全局统计信息，尚未产生清晰的面部特征（见 Figure 5 的 Fashion-MNIST 定性对比，CelebA 样本见附录）。

### 消融实验

#### 噪声多重性 K 的影响

**Table 11** 系统消融了噪声多重性 K 的作用。在 MNIST ε = 1 下，K 从 1 增至 32 时，FID 单调下降，CNN 准确率单调上升，最佳结果在 K = 32 取得。这与 **Theorem 1** 的理论预测一致：目标方差随 K 增加以 1/K 的速率降低。**Figure 6**（Figure 3 的放大版）从梯度估计方差角度提供了直接证据——训练过程中参数梯度估计的方差随 K 增加呈对数尺度显著下降。K 的增大不消耗额外隐私预算，因为所有 K 个噪声扰动共享同一数据点的梯度剪裁和噪声注入。

#### DM 配置（训练噪声分布）的影响

**Table 3** 对比了四种 DM 配置在强隐私 ε = 0.2 下的表现。v-prediction 配置显著优于 EDM 配置和其他方案：FID 从 EDM 的 83.5 降至 47.9，CNN 准确率从 61.5% 提升至 82.4%。这验证了 **Figure 4** 揭示的机制：v-prediction 的噪声分布 p(σ) 赋予高噪声水平 σ 更大权重，使模型在有限隐私预算下优先学习数据的全局结构（低频信息），而非被 DP 噪声淹没的细节。在宽松隐私（ε = 10）下，配置间差异缩小，因为模型有足够容量学习所有噪声水平。

#### 采样器的选择

**Table 6** 比较了 Churn 随机采样器（Karras et al., 2022）与确定性 DDIM（Song et al., 2021a）。在 MNIST ε = 1 下，Churn 采样器针对 FID 调参时，FID 为 23.4，远优于 DDIM 的 41.1；但 CNN 准确率（92.1%）低于 DDIM（95.3%）。当 Churn 采样器针对下游准确率调参时，准确率可达 95.3%，与 DDIM 持平，但 FID 升至 30.8。这表明随机采样通过注入额外噪声有效提升了感知质量（FID），但对分类保真度有轻微负面影响，两者存在权衡。该发现与 DP 训练的特殊性相关：DP-SGD 训练的模型输出分布可能欠拟合，随机采样有助于补偿这种欠拟合导致的模式坍塌。

### 失败模式与局限

1. **高分辨率场景**：DPDM 在 CelebA 32×32 上已能捕捉肤色和光照统计信息，但无法生成清晰的面部特征。扩展到更高分辨率（如 64×64 或 ImageNet）时，所需网络容量增大，而 DP-SGD 下参数增加会引入更多噪声，形成根本性挑战。

2. **照片级逼真度**：当前所有 DP 生成模型（包括 DPDM）均无法生成照片级逼真的内容。DPDM 的优势主要体现在结构化简单数据集（MNIST/Fashion-MNIST）上，对复杂自然图像的生成仍停留在纹理统计层面。

3. **群隐私处理**：实验中使用固定群隐私转换，未深入探讨个体拥有多张图像的场景（如 CelebA 中同一人的多张照片），这需要在 DP 分析中更精细地处理。

4. **网络规模约束**：Table 8 显示 DPDM 使用的网络极小（MNIST 上约 1.75M 参数），而大网络在 DP-SGD 下性能衰减严重。这限制了模型容量，成为表达能力的瓶颈。

### 重要图表结论

- **Figure 2**：扩散模型去噪器的雅可比 Frobenius 范数 I_F(σ) 在所有噪声水平 σ 下均显著低于 GAN 生成器的雅可比范数，且远低于端到端 DM 采样函数的整体复杂度。这从函数光滑性角度解释了 DMs 为何比 GANs 更适合 DP-SGD 训练——更简单的函数需要更少的梯度信息即可有效优化。

- **Figure 5**：Fashion-MNIST 生成样本的定性对比直观展示了 DPDM 相对于所有基线的视觉质量优势，在 ε = 10 下生成的服饰图像类别特征清晰、形状完整，而多数基线方法产生模糊或坍塌的样本。

- **Table 9**：所有实验中 DP 噪声标准差 σ_DP 的配置表，反映了不同隐私预算和数据集下的噪声注入量级，为复现提供关键参考。

### 补充图表

![[assets/figures/papers/paper_list_l42_https_arxiv_org_abs_2210_09929/figures/027_Figure_14.jpg]]
*Figure 14: Additional images generated by DPDM on CelebA for ε=10 using Churn (top), stochastic DDIM (middle), and deterministic DDIM (bottom)*

![[assets/figures/papers/paper_list_l42_https_arxiv_org_abs_2210_09929/figures/028_Figure_15.jpg]]
*Figure 15: Additional images generated by DPDM on CelebA for ε=1 using Churn (top), stochastic DDIM (middle), and deterministic DDIM (bottom)*

![[assets/figures/papers/paper_list_l42_https_arxiv_org_abs_2210_09929/figures/029_Figure_16.jpg]]
*Figure 16: CelebA images generated by DataLens (1st row), DP-MEPF (2nd row), DP-Sinkhorn (3rd row), and our DPDM (4th row) for DP-ε=10*

![[assets/figures/papers/paper_list_l42_https_arxiv_org_abs_2210_09929/figures/005_Table_1.jpg]]
*Table 1: Class-conditional DP image generation performance (MNIST & Fashion-MNIST). For PEARL (Liew et al., 2022), we train models and compute metrics ourselves (App. F.1). All other results taken from the literature. DP-MEPF (†) uses additional public data for training (only included for completeness)*

![[assets/figures/papers/paper_list_l42_https_arxiv_org_abs_2210_09929/figures/007_Table_2.jpg]]
*Table 2: Class prediction accuracy on real test data. DP-SGD: Classifiers trained directly with DP-SGD and real training data. DPDM: Classifiers trained non-privately on synthesized data from DP-SGD-trained DPDMs (using 60,000 samples, following Cao et al. (2021))*

![[assets/figures/papers/paper_list_l42_https_arxiv_org_abs_2210_09929/figures/008_Table_3.jpg]]
*Table 3: DM config ablation on MNIST for ε=0.2. See Tab. 12 for extended results*

![[assets/figures/papers/paper_list_l42_https_arxiv_org_abs_2210_09929/figures/009_Table_4.jpg]]
*Table 4: Unconditional CelebA generative performance. G-PATE and DataLens (†) use $\delta$ = 1 $0 ^ { - 5 }$ (less privacy) and model images at 64x64 resolution*

![[assets/figures/papers/paper_list_l42_https_arxiv_org_abs_2210_09929/figures/010_Table_6.jpg]]
*Table 6: Sampler comparison on MNIST (see Tab. 13 for results on Fashion-MNIST). We compare the Churn sampler (Karras et al., 2022) to DDIM (Song et al., 2021a)*

![[assets/figures/papers/paper_list_l42_https_arxiv_org_abs_2210_09929/figures/011_Table.jpg]]

![[assets/figures/papers/paper_list_l42_https_arxiv_org_abs_2210_09929/figures/012_Table_7.jpg]]
*Table 7: Four popular DM configs from the literature*

## 方法谱系与知识库定位

### 1. 与差分隐私生成模型基线的关系

DPDM 处于差分隐私图像生成的研究脉络中。在 DPDM 之前，该领域的主流范式是 DP GAN 及其变体，以及基于一次性私有化（one-shot privatization）的方法。DPDM 的提出建立在对这些基线方法局限性的分析之上。

**相对于 DP GAN 系列**：DP GAN 方法通过在训练过程中向判别器或生成器的梯度注入噪声来实现隐私保护。代表性工作包括 **DP-CGAN** (Torkzadehmahani et al., 2019)、**GS-WGAN** (Chen et al., 2020)、**G-PATE** (Long et al., 2019) 和 **DataLens** (Wang et al., 2021) 等。DPDM 的核心洞见在于，GAN 的生成器网络需要一步完成从噪声到高维图像的映射，其函数复杂度（以雅可比矩阵的 Frobenius 范数量化）远高于扩散模型的去噪器网络（Figure 2 提供了实证支持）。扩散模型将生成过程分解为多步去噪，每步只需学习一个简单的回归任务（L2 损失），这使得其在 DP-SGD 训练下天然具有更低的优化难度和更高的稳定性。实验表明，在 MNIST 上 ε=1 时，DPDM 将最优 FID 从 56.2 降至 23.4，下游 CNN 分类准确率从 81.5% 提升至 95.3%，显著超越了此前所有 DP GAN 基线。

**相对于一次性私有化方法**：**DP-MERF** (Harder et al., 2021) 和 **PEARL** (Liew et al., 2022) 等方法通过对数据统计量（如随机傅里叶特征或特征函数）进行一次性的私有化处理，再从中采样生成数据。这类方法避免了迭代训练中的隐私成本累积，但受限于统计量对数据分布的近似能力。DPDM 则通过 DP-SGD 端到端训练去噪网络，能够更灵活地学习数据分布，在 FID 和下游任务效用上均展现出优势。值得注意的是，**DP-MEPF** (Harder et al., 2022) 使用了额外的公开数据进行训练，而 DPDM 及多数其他基线方法仅使用私有数据，因此比较时需注意这一不对等条件。

### 2. 方法适用边界

DPDM 在当前实验设置下的有效范围存在明确边界：

- **数据复杂度**：在 MNIST 和 Fashion-MNIST 上取得了显著提升，在 CelebA (32×32) 上也能生成具有人脸结构特征的图像。但在更大规模、更高分辨率的数据集（如 ImageNet）上，DPDM 目前仅能捕捉图像的宏观统计信息，尚无法生成清晰的物体结构。这是当前 DP 生成模型面临的共同挑战。
- **网络容量约束**：DPDM 使用了较小的网络（MNIST 上约 1.75M 参数），这既是 DP-SGD 内存开销的实用考量，也是因为 DP-SGD 的噪声幅度随参数数量增加而加剧。当数据点数量固定时，扩展到高分辨率图像需要更大的网络，但更大网络在 DP-SGD 下会因参数增多导致梯度噪声放大，形成根本性挑战。
- **隐私预算下限**：在极强隐私（ε=0.2）下，DPDM 仍能保持优于基线的性能，但此时 DM 配置的选择（如 v-prediction 噪声分布）变得至关重要，且生成质量与无隐私训练之间仍存在显著差距。
- **群隐私处理**：实验中使用固定的群隐私转换（group privacy conversion），未深入探讨个体身份出现多张图像的场景（如 CelebA 中同一人有多张照片），这需要更精细的隐私分析。

### 3. 核心局限

1. **无法生成照片级逼真内容**：即使在中等隐私预算下，DPDM 生成的图像仍与无隐私扩散模型存在明显质量差距，模型容量受限是主要瓶颈。
2. **高分辨率扩展困难**：DP-SGD 的噪声随网络参数增长而加剧，与高分辨率图像对大网络的需求形成矛盾。当前方法在固定数据量下难以突破这一限制。
3. **训练效率**：噪声多重性（K 值）虽然在不增加隐私成本的前提下降低梯度方差，但增加了每步训练的计算开销（每样本需前向传播 K 次）。实验中 K=32 达到最佳效果，但更大的 K 值带来的边际收益递减。
4. **公平比较的复杂性**：不同 DP 生成方法在隐私参数（δ 值）、图像分辨率、是否使用公开数据等方面存在差异。例如，G-PATE 和 DataLens 在 CelebA 上使用 δ=10⁻⁵（隐私保护弱于 DPDM 的 δ=10⁻⁶）且处理 64×64 图像，这使得直接数值比较需要谨慎解读。

### 4. 开放问题

- **规模化路径**：如何将 DPDM 扩展到更大规模、更高分辨率的数据集？可能的路径包括结合公开数据进行预训练或混合训练、探索参数高效的网络架构、或改进 DP-SGD 的噪声机制。
- **跨模态泛化**：DPDM 框架能否应用于图像之外的数据模态（如文本、音频、表格数据）？去噪网络的简单回归特性和噪声多重性机制在理论上具有模态无关性，但需实证验证。
- **群隐私的精细处理**：在个体拥有多张图像的场景下（如人脸数据集），如何更精确地实现群隐私保护，而非简单套用群隐私转换？
- **采样策略的进一步优化**：当前发现随机采样（Churn 采样器）对 FID 至关重要，而确定性采样（DDIM）在下游准确率上有优势。是否存在统一的采样策略能在两个指标上同时达到最优？
- **隐私-效用理论分析**：噪声多重性降低方差的 1/K 关系已由 Theorem 1 给出，但 DM 配置、网络架构与隐私预算之间的更精细理论关系仍有待建立，以指导不同隐私需求下的方法选择。

## 原文 PDF

![[paperPDFs/TMLR_2023/Differentially_Private_Diffusion_Models.pdf]]
