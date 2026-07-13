---
title: "Don't Generate Me: Training Differentially Private Generative Models with Sinkhorn Divergence"
type: paper
paper_level: A
venue: NeurIPS
year: 2021
pdf_ref: paperPDFs/NEURIPS_2021/Don_t_Generate_Me_Training_Differentially_Private_Generative_Models_with_Sinkhorn_Divergence.pdf
code_link: null
project_link: https://research.nvidia.com/labs/toronto-ai/DP-Sinkhorn/
aliases:
- DS
- DTGMTDPGMSD
tags:
- NEURIPS_2021
- topic/generative_models_diffusion
- topic/generative_models_diffusion/generative_models_and_autoencoders
core_operator: "利用最优传输（OT）原形式中的Sinkhorn散度替代对抗损失，并引入可调控偏差-方差权衡的半去偏Sinkhorn损失来稳定梯度估计。"
primary_logic: "通过直接最小化Sinkhorn散度避免对抗训练的不稳定性；同时，半去偏损失在隐私噪声下提供更鲁棒的梯度估计，使得生成模型在严格DP下可以实现稳定训练和高质量的图像合成。"
claims:
- "DP-Sinkhorn使用Sinkhorn散度而非对抗目标，从而避免训练不稳定性。"
- "半去偏Sinkhorn损失通过插值控制梯度估计的偏差-方差折衷，是方法的核心创新。"
- "在MNIST和Fashion-MNIST上，以(10,10^{-5})-DP达到领先的FID和下游分类准确率，超越GS-WGAN、DP-MERF等现有方法。"
- "隐私机制（按图像梯度裁剪加噪）满足(α,2αn/σ²)-RDP，且在合成数据梯度上不加噪以节省隐私预算。"
---

# Don't Generate Me: Training Differentially Private Generative Models with Sinkhorn Divergence

> [!tip] 核心洞察
> 通过直接最小化Sinkhorn散度避免对抗训练的不稳定性；同时，半去偏损失在隐私噪声下提供更鲁棒的梯度估计，使得生成模型在严格DP下可以实现稳定训练和高质量的图像合成。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 别生成我：使用Sinkhorn散度训练差分隐私生成模型 |
| 英文题名 | Don't Generate Me: Training Differentially Private Generative Models with Sinkhorn Divergence |
| 会议/期刊 | NeurIPS 2021 |
| Links | [paper](https://arxiv.org/abs/2111.01177) · [Project](https://nv-tlabs.github.io/DP-Sinkhorn) · [Project](https://research.nvidia.com/labs/toronto-ai/DP-Sinkhorn/) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/generative_models_and_autoencoders |
| Method | DP-Sinkhorn |
| Dataset | MNIST, Fashion-MNIST |

> [!tip] 效果简介
> - MNIST 上，FID 为 48.4，对比 61.3 (GS-WGAN)，变化 降低 12.9。
> - MNIST 上，CNN Accuracy (%) 为 83.2，对比 80.0 (GS-WGAN)，变化 +3.2%。
> - Fashion-MNIST 上，FID 为 128.3，对比 131.3 (GS-WGAN)，变化 降低 3.0。

## 概要

在差分隐私（DP）约束下训练生成模型面临一个根本性瓶颈：基于GAN的对抗训练本身即存在不稳定性和模式崩溃，而梯度加噪进一步放大了这些困难；现有方法依赖大量判别器网络，内存消耗大，且超参数调优与隐私原则相冲突。针对这一问题，**DP-Sinkhorn** 提出以最优传输（OT）原形式中的Sinkhorn散度替代对抗损失，从根本上避开生成器-判别器博弈的不稳定性。其核心创新在于引入**半去偏Sinkhorn损失**，通过可调参数 $p$ 精细控制梯度估计的偏差-方差权衡，使模型在隐私噪声下获得更鲁棒的梯度信号。隐私保护通过仅对与真实数据交互的生成图像梯度进行裁剪并注入高斯噪声实现，而非在参数梯度上加噪，从而利用图像梯度的低维特性与Poisson子采样的隐私放大效应。

在 $(10, 10^{-5})$-DP 设定下，DP-Sinkhorn 在 MNIST 上取得 **FID 48.4**（对比 GS-WGAN 的 61.3），下游 CNN 分类准确率达 **83.2%**（+3.2%）；在 Fashion-MNIST 上 FID 为 **128.3**（对比 GS-WGAN 的 131.3），分类准确率达 **71.1%**（+6.1%），在图像质量和数据效用两项指标上均超越 GS-WGAN、DP-MERF、DataLens 等现有方法。消融实验确认，半去偏参数 $p=0.4$ 是偏差-方差的最佳平衡点，混合 L1/L2 成本函数可兼顾图像锐度与下游分类性能，且 DP-Sinkhorn 对学习率和优化器不敏感，训练过程稳定收敛，无需像 GAN 那样依赖提前停止。然而，该方法仍需针对不同数据集进行耗时的超参数网格搜索，训练迭代数随隐私预算收紧而急剧增加（如 CelebA 需约 1.7M 步），且仅在小尺寸低分辨率数据集上得到验证，高分辨率生成能力及对成员推断攻击的防御强度尚待进一步评估。

### 差分隐私生成模型的核心困境

生成模型在数据共享、数据增强等场景中具有重要价值，但当训练数据包含敏感信息（如医疗影像、人脸图像）时，直接发布模型参数或合成样本可能导致隐私泄露。差分隐私（Differential Privacy, DP）为这一场景提供了严格的数学保障，但将其应用于生成模型训练时面临根本性挑战：**隐私噪声与训练稳定性之间的冲突**。

当前主流的差分隐私生成方法大多基于生成对抗网络（GAN）框架，通过在训练过程中注入噪声来实现隐私保护。然而，这类方法存在三个深层瓶颈：

1. **对抗训练的不稳定性**：GAN本身存在模式崩溃（mode collapse）和训练不收敛的问题，而差分隐私所需的梯度加噪进一步放大了这种不稳定性。生成器与判别器之间的博弈在噪声干扰下更容易失衡，导致合成质量急剧下降。

2. **隐私机制的设计困境**：现有方法如 **DP-CGAN** 和 **G-PATE** 依赖大量判别器网络或复杂的梯度聚合策略来分摊隐私预算，内存消耗大且超参数调优困难。更关键的是，超参数搜索本身若在私有数据上进行，会消耗额外的隐私预算，与隐私保护原则形成矛盾。

3. **梯度估计的偏差-方差权衡被忽视**：基于最优传输（Optimal Transport, OT）的生成方法虽然避免了对抗训练，但其经验Sinkhorn损失存在固有的偏差-方差困境——使用同一批样本计算自相关项会引入偏差，而使用独立批次虽可消除偏差却显著增大方差。在差分隐私的噪声环境下，这种权衡变得更加尖锐，但现有方法未能提供有效的控制手段。

### 最优传输方法的潜力与局限

最优传输理论为度量概率分布间的距离提供了坚实的数学基础。其中，Sinkhorn散度（Sinkhorn divergence）通过熵正则化使得Wasserstein距离的计算在计算上可行，同时通过引入自相关项消除了熵偏（entropic bias），成为生成模型训练中对抗损失的理想替代方案。其核心优势在于：

- **无需判别器**：直接最小化生成分布与真实分布之间的距离，避免了对抗训练的博弈过程。
- **训练稳定**：损失函数的优化目标明确，梯度信号一致，不易出现模式崩溃。

然而，将Sinkhorn散度直接应用于差分隐私场景面临关键障碍：经验Sinkhorn损失的自相关项计算需要真实数据的配对比较，这在隐私约束下意味着梯度必须经过隐私处理。如何设计既能保护隐私又能保持梯度估计质量的损失函数，是本文的核心动机。

### 本文的切入点

本文提出 **DP-Sinkhorn**，核心思路是将半去偏Sinkhorn损失与图像级梯度隐私机制相结合，从根本上重构差分隐私生成模型的训练范式。关键创新在于：

- **用Sinkhorn散度替代对抗损失**，从根源上消除训练不稳定性。
- **引入半去偏（semi-debiased）Sinkhorn损失**，通过一个可调参数 $p$ 精细控制梯度估计的偏差-方差折衷，使模型在隐私噪声下仍能获得鲁棒的梯度信号。
- **在生成图像梯度层面施加隐私保护**，而非在参数梯度或判别器输出上加噪，利用图像梯度的低维特性减少隐私预算消耗。

这一设计使得DP-Sinkhorn能够在严格差分隐私约束下实现稳定训练，并在图像合成质量上超越现有方法。

## 核心方法与创新机理

DP-Sinkhorn 的核心创新在于**用最优传输（OT）距离替代对抗博弈，从根本上规避了差分隐私下 GAN 训练的不稳定性**，并通过**半去偏 Sinkhorn 损失**和**生成图像级梯度隐私保护**两个关键设计，在严格隐私预算下实现了稳定训练和高质量的图像合成。

### 从对抗博弈到最优传输：训练范式的根本转变

传统基于 GAN 的差分隐私生成模型（如 **GS-WGAN**、**DP-CGAN**、**G-PATE**）依赖生成器与判别器之间的对抗训练。在差分隐私约束下，梯度加噪进一步破坏了原本就脆弱的纳什均衡，导致训练不稳定、模式崩溃和对超参数的极度敏感。DP-Sinkhorn 彻底抛弃了这一范式：它直接最小化生成分布与真实分布之间的 Sinkhorn 散度 $S_{c,\lambda}(\mu,\nu)$——一种计算高效的熵正则化 Wasserstein 距离的无偏变体：

$$S_{c,\lambda}(\mu,\nu) = 2W_{c,\lambda}(\mu,\nu) - W_{c,\lambda}(\mu,\mu) - W_{c,\lambda}(\nu,\nu)$$

这一损失函数无需判别器网络，训练过程是端到端的直接距离最小化，从根本上消除了对抗训练的不稳定性来源。如 Figure 4a 所示，DP-Sinkhorn 对学习率和优化器不敏感，训练过程稳定收敛，无需像 GAN 那样依赖提前停止（early stopping）。

### 半去偏 Sinkhorn 损失：偏差-方差的可控权衡

直接使用经验 Sinkhorn 损失面临一个关键困境：**有偏估计**（使用同一批生成数据计算自相关项）引入系统性偏差但方差较小；**无偏估计**（使用独立批次）消除偏差但方差显著增大。在差分隐私的梯度噪声环境下，高方差估计会严重损害训练质量。

DP-Sinkhorn 提出了**半去偏 Sinkhorn 损失**（Definition 4.3），通过混合样本比例 $p \in [0,1]$ 在偏差与方差之间进行精细插值：

$$\hat{S}_{c,\lambda,p}(\mathbf{X},\mathbf{Y}) = 2\hat{W}_{\lambda}(\mathbf{X}^{[0:n]},\mathbf{Y}) - \hat{W}_{\lambda}(\mathbf{X}^{[0:n]},\mathbf{X}^{[n':n+n']})$$

其中 $n' = \lfloor p \cdot n \rfloor$ 控制自相关项中独立样本的混合比例。当 $p=0$ 时退化为有偏经验损失，$p=1$ 时为完全无偏损失。消融实验（Table 2, Figure 5）表明，$p=0.4$ 在 MNIST 和 Fashion-MNIST 上均达到最优的 FID 和下游分类准确率，验证了偏差-方差折衷设计的有效性。

### 生成图像级梯度隐私保护：更精准的隐私注入

与 DPSGD 在参数梯度上全局加噪不同，DP-Sinkhorn 将隐私屏障置于**生成器输出的图像层面**（Figure 1 中的 Privacy Barrier）。具体而言，仅对与真实数据交互的生成图像梯度进行裁剪和高斯噪声注入：

$$\tilde{\mathbf{G}}^{[i]} = \mathbf{G}^{[i]} \cdot \min\left(\frac{\Delta}{\|\mathbf{G}^{[i]}\|_2}, 1\right) + \gamma,\quad \gamma \sim \mathcal{N}(0,\Delta^2\sigma^2)$$

而仅用于去偏的合成数据梯度只做裁剪不加噪声。这一设计有两重优势：其一，生成图像梯度的维度远低于参数梯度，噪声影响更可控；其二，结合 Poisson 子采样，该方法满足 $(\alpha, 2\alpha n/\sigma^2)$-RDP（Theorem 4.1），在同等隐私预算下保留了更多有效梯度信息。消融实验（Table 2）证实，图像级扰动（perturb image）在 FID 和分类准确率上均优于参数级扰动（perturb param）。

### 混合成本函数的像素级优化

为平衡生成图像的平滑性与锐度，DP-Sinkhorn 采用混合 $L_1$ 和 $L_2$ 的像素级成本函数：

$$c_m(\mathbf{x},\mathbf{y}) = L_2(\mathbf{x},\mathbf{y})^2 + m L_1(\mathbf{x},\mathbf{y})$$

消融实验（Table 2）表明，引入 $L_1$ 分量（$m=1$ 或 $m=3$）相比纯 $L_2$ 成本能同时提升图像锐度和下游分类性能，这为 OT 距离在差分隐私图像生成中的应用提供了有效的感知质量调控手段。

DP-Sinkhorn 是一种基于最优传输（Optimal Transport, OT）的差分隐私生成模型训练框架，其核心设计思想是用 **Sinkhorn 散度** 取代传统 GAN 的对抗训练目标，从而从根本上规避对抗训练的不稳定性与模式崩溃问题。整体训练流程是一个端到端的迭代损失最小化过程，无需判别器网络，也无需在参数梯度上进行传统的 DPSGD 式加噪。

### 核心瓶颈与设计动机

在差分隐私约束下训练生成模型面临双重挑战：一方面，GAN 本身的对抗训练存在不稳定性和模式崩溃，梯度加噪会进一步放大这些问题；另一方面，现有基于 PATE 框架或集成判别器的方法（如 **G-PATE**、**GS-WGAN**）需要维护大量判别器网络，内存消耗大，且超参数调优与隐私原则相冲突。DP-Sinkhorn 的因果调节旋钮在于：**利用最优传输原形式中的 Sinkhorn 散度替代对抗损失，并引入可调控偏差-方差权衡的半去偏 Sinkhorn 损失来稳定梯度估计**。

### 单次训练迭代的完整数据流

单次训练迭代的数据流如 Figure 1 所示，包含以下关键步骤：

1. **数据采样与生成**：从潜空间采样噪声向量，通过生成器 $G_\theta$ 生成一批合成图像 $\mathbf{X}$；同时通过 Poisson 子采样从私有数据集中抽取一批真实图像 $\mathbf{Y}$。

2. **批次拆分**：将生成的合成图像 $\mathbf{X}$ 拆分为两组：前 $n$ 个样本 $\mathbf{X}^{[0:n]}$ 用于计算与真实数据的交叉项（cross term），额外的 $n'$ 个样本 $\mathbf{X}^{[n':n+n']}$ 用于计算合成数据的自相关项（self term）。这种拆分策略是实现半去偏损失的关键。

3. **成本矩阵构建**：计算生成图像与真实图像之间的逐像素成本矩阵。成本函数采用混合形式：
   $$c_m(\mathbf{x}, \mathbf{y}) = L_2(\mathbf{x}, \mathbf{y})^2 + m L_1(\mathbf{x}, \mathbf{y})$$
   其中 $L_2^2$ 提供平滑性，$L_1$ 增强图像锐度，超参数 $m$ 控制两者的平衡。对于条件生成任务，类别嵌入也被融入成本矩阵。

4. **Sinkhorn 迭代**：通过 Sinkhorn 算法在成本矩阵上计算熵正则化的最优传输计划，得到经验 Wasserstein 距离 $\hat{W}_\lambda$。该步骤是计算 Sinkhorn 散度的核心，具体算法见 Algorithm 3。

5. **半去偏 Sinkhorn 损失计算**：按如下公式组合交叉项和自相关项：
   $$\hat{S}_{c,\lambda,p}(\mathbf{X},\mathbf{Y}) = 2\hat{W}_{\lambda}(\mathbf{X}^{[0:n]},\mathbf{Y}) - \hat{W}_{\lambda}(\mathbf{X}^{[0:n]},\mathbf{X}^{[n':n+n']})$$
   其中去偏比率 $p = n'/(n+n')$ 控制偏差-方差折衷：$p=0$ 对应完全有偏损失（方差低但偏差高），$p=1$ 对应完全去偏损失（无偏但方差大），$p=0.4$ 是实验验证的最佳平衡点。

6. **隐私梯度清洗**：在反向传播时，对与真实数据 $\mathbf{Y}$ 交互的生成图像 $\mathbf{X}^{[0:n]}$ 的梯度进行裁剪并注入高斯噪声：
   $$\tilde{\mathbf{G}}^{[i]} = \mathbf{G}^{[i]} \cdot \min\left(\frac{\Delta}{||\mathbf{G}^{[i]}||_2}, 1\right) + \gamma,\quad \gamma \sim \mathcal{N}(0,\Delta^2\sigma^2)$$
   而仅用于去偏的合成数据 $\mathbf{X}^{[n':n+n']}$ 的梯度只做裁剪，不加噪声——因为这些梯度不包含真实数据信息，加噪只会无谓消耗隐私预算。这一隐私注入位置（生成图像梯度而非参数梯度）是 DP-Sinkhorn 区别于 DPSGD 类方法的关键设计，其优势在于图像梯度维度远低于参数梯度，且天然利用了子采样的隐私放大效应。

7. **参数更新**：将清洗后的梯度反传至生成器参数，使用 Adam 优化器更新。

### 隐私保障机制

隐私分析基于 Rényi 差分隐私（RDP）框架：对裁剪常数 $\Delta$ 和噪声尺度 $\sigma$，释放清洗后的梯度满足 $(\alpha, 2\alpha n/\sigma^2)$-RDP（Theorem 4.1）。通过 Poisson 子采样和 RDP 到 $(\varepsilon,\delta)$-DP 的转换，最终实现端到端的差分隐私保障。隐私屏障被精确地放置在生成器输出端（生成图像梯度处），而非传统的参数梯度处，这一设计使得隐私预算的消耗与生成图像数量而非模型参数量挂钩。

### 训练范式的根本转变

与 GAN 的生成器-判别器博弈范式相比，DP-Sinkhorn 的训练范式发生了根本性转变：**从对抗训练转向直接最小化最优传输距离**。这一转变带来的直接收益包括：
- 训练过程稳定收敛，无需提前停止（Figure 4a 验证了对学习率和优化器的不敏感性）；
- 无需维护判别器网络，显著降低内存开销；
- 损失函数直接度量分布间的几何距离，为梯度估计提供了更清晰的信号。

### 关键超参数与模块关系

框架中涉及的关键超参数及其作用域：
| 超参数 | 作用模块 | 功能 |
|--------|----------|------|
| $p$ | 半去偏损失计算 | 控制偏差-方差折衷 |
| $m$ | 成本矩阵构建 | 平衡 L1/L2 成本权重 |
| $\lambda$ | Sinkhorn 迭代 | 熵正则化强度 |
| $\Delta, \sigma$ | 隐私梯度清洗 | 控制隐私保护强度 |
| 学习率、批次大小 | 参数更新 | 影响收敛速度与隐私预算 |

这些超参数之间存在耦合关系，不同数据集需要独立的网格搜索（Table 4、Table 5 展示了 MNIST 和 Fashion-MNIST 上的搜索空间）。这一调优过程若直接在私有数据上反复实验会消耗隐私预算，是该方法的一个实际部署限制。

DP-Sinkhorn 的训练流程由六个关键模块串联构成，其核心创新在于用半去偏 Sinkhorn 损失替代对抗损失，并在生成图像梯度层面注入隐私噪声。

### 1. 数据采样与生成

生成器 $G_\theta$ 从潜空间采样噪声 $\mathbf{z}$，映射为生成图像 $\tilde{\mathbf{x}} = G_\theta(\mathbf{z})$。私有数据通过 Poisson 子采样抽取真实批次 $\mathbf{Y}$（Algorithm 1 lines 3-6）。生成批次被划分为两组：交叉组 $\mathbf{X}^{[0:n]}$ 与真实数据计算交叉项，自相关组 $\mathbf{X}^{[n':n+n']}$ 用于去偏自相关项（Figure 1）。

### 2. 成本矩阵构建

生成图像与真实图像之间的逐像素差异通过混合成本函数度量：

$$c_m(\mathbf{x}, \mathbf{y}) = L_2(\mathbf{x}, \mathbf{y})^2 + m L_1(\mathbf{x}, \mathbf{y})$$

其中 $L_2(\mathbf{x}, \mathbf{y})^2$ 为逐像素平方 $\ell_2$ 距离，$L_1(\mathbf{x}, \mathbf{y})$ 为逐像素 $\ell_1$ 距离，$m$ 控制 $\ell_1$ 项的权重。混合成本在图像平滑性与锐度之间取得平衡（Section 4.4）。对于条件生成，类别嵌入被融入成本矩阵。

### 3. Sinkhorn 迭代

基于成本矩阵，通过 Sinkhorn 算法计算熵正则化 Wasserstein 距离的经验估计 $\hat{W}_\lambda$。该算法迭代归一化传输矩阵的行与列，逼近最优传输计划（Algorithm 3）。熵正则化 Wasserstein 距离定义为：

$$W_{c,\lambda}(\boldsymbol{\mu},\boldsymbol{\nu}) = \operatorname*{min}_{\pi\in\Pi} \int c(\mathbf{x},\mathbf{y}) d\pi(\mathbf{x},\mathbf{y}) + \lambda \int \log\left(\frac{d\pi(\mathbf{x},\mathbf{y})}{d\boldsymbol{\mu}(\mathbf{x}) d\nu(\mathbf{y})}\right) d\pi(\mathbf{x},\mathbf{y})$$

其中 $\lambda$ 控制熵正则化强度（Eq. 1）。

### 4. 半去偏 Sinkhorn 损失计算

Sinkhorn 散度通过自相关项消除熵偏，是分布匹配的无偏度量：

$$S_{c,\lambda}(\mu,\nu) = 2W_{c,\lambda}(\mu,\nu) - W_{c,\lambda}(\mu,\mu) - W_{c,\lambda}(\nu,\nu)$$

然而，基于有限样本的经验估计存在偏差-方差困境：完全有偏估计 $\hat{S}_{c,\lambda}(\mathbf{X},\mathbf{Y})$（使用同一批生成数据计算自相关项）方差低但偏差大；完全去偏估计（使用独立批次 $\mathbf{X}'$）无偏但方差高。DP-Sinkhorn 的核心创新是**半去偏 Sinkhorn 损失**，通过混合样本比例 $p \in [0,1]$ 在两者之间插值：

$$\hat{S}_{c,\lambda,p}(\mathbf{X},\mathbf{Y}) = 2\hat{W}_{\lambda}(\mathbf{X}^{[0:n]},\mathbf{Y}) - \hat{W}_{\lambda}(\mathbf{X}^{[0:n]},\mathbf{X}^{[n':n+n']})$$

其中 $n' = \lfloor pn \rfloor$。当 $p=0$ 时退化为有偏损失，$p=1$ 时为去偏损失。可调参数 $p$ 直接控制梯度估计的偏差-方差折衷（Definition 4.3, Eq. 6）。

### 5. 隐私梯度清洗

隐私保护通过**在生成图像梯度层面**裁剪并加噪实现，而非传统的参数梯度加噪（DPSGD）。对于与真实数据交互的交叉组图像梯度 $\mathbf{G}^{[i]}$：

$$\tilde{\mathbf{G}}^{[i]} = \mathbf{G}^{[i]} \cdot \operatorname*{min}\left(\frac{\Delta}{||\mathbf{G}^{[i]}||_2}, 1\right) + \gamma,\quad \gamma \sim \mathcal{N}(0,\Delta^2\sigma^2),\quad i \in [0,n-1]$$

其中 $\Delta$ 为裁剪阈值，$\sigma$ 为噪声乘数。仅用于去偏的自相关组梯度只做裁剪不加噪，因为它们不包含真实数据信息：

$$\tilde{\mathbf{G}}^{[i]} = \mathbf{G}^{[i]} \cdot \operatorname*{min}\left(\frac{\Delta}{||\mathbf{G}^{[i]}||_2}, 1\right),\quad i \in [n,n+n'-1]$$

此机制满足 $(\alpha, 2\alpha n/\sigma^2)$-RDP（Theorem 4.1），且因图像梯度维度远低于参数梯度，隐私-效用权衡更优。

### 6. 反向传播与参数更新

清洗后的梯度反传至生成器，使用 Adam 优化器更新参数 $\theta$。整个流程为端到端的直接距离最小化，无需判别器网络或对抗训练（Algorithm 1 lines 12-13）。

## 实验与关键发现

### 主要结果：图像生成质量与下游效用

DP-Sinkhorn 在 MNIST 和 Fashion-MNIST 上以 (10, 10⁻⁵)-DP 的隐私预算下，在 FID 和下游分类准确率两个维度上均超越现有方法。Table 1 给出了系统对比：


- **MNIST**：DP-Sinkhorn 取得 FID 48.4，相比此前最优的 **GS-WGAN**（FID 61.3）降低 12.9；以合成数据训练的 CNN 分类准确率达 83.2%，高于 GS-WGAN 的 80.0%。其他对比方法包括 **G-PATE**（FID 150.6 / Acc 58.0%）、**DP-CGAN**（FID 179.2 / Acc 60.0%）、**DP-MERF**（FID 121.4 / Acc 63.0%）和 **DataLens**（FID 57.8 / Acc 80.0%），DP-Sinkhorn 在所有指标上均占优。
- **Fashion-MNIST**：DP-Sinkhorn 取得 FID 128.3，优于 GS-WGAN 的 131.3；CNN 准确率 71.1%，显著高于 GS-WGAN 的 65.0%。DP-MERF 的 FID 为 161.7、准确率 61.0%，DataLens 的 FID 为 167.7、准确率 65.0%，差距更为明显。

在更具挑战性的 CelebA 32×32 数据集上，DP-Sinkhorn 结合 BigGAN 生成器在 (10, 10⁻⁶)-DP 下取得 CNN 准确率 75.79%（Table 6），展示了该方法在 RGB 人脸图像上的可行性。需注意，Table 3 中 DataLens 的结果基于 64×64 分辨率和更大的 δ（10⁻⁵），不可直接对比。

![[assets/figures/papers/paper_list_l18_https_arxiv_org_abs_2111_01177/figures/006_Table_3.jpg]]
*Table 3: DP image generation results on downsampled CelebA. We include results from [14] for context, but note that their experiment uses a 64x64 resolution and a larger δ of 1 0 ^ { - 5 }*

![[assets/figures/papers/paper_list_l18_https_arxiv_org_abs_2111_01177/figures/010_Table_6.jpg]]
*Table 6: Differentially private image generation results on downsampled CelebA*

**Figure 2** 的生成图像可视化进一步印证了定量结果：DP-Sinkhorn 生成的 MNIST 数字和 Fashion-MNIST 服饰在类内一致性和边缘清晰度上明显优于 GS-WGAN 和 DP-MERF。

### 消融实验：损失函数设计的因果验证

Table 2 针对 MNIST 进行了系统的消融分析，验证了三个核心设计选择的因果作用：

![[assets/figures/papers/paper_list_l18_https_arxiv_org_abs_2111_01177/figures/005_Table_2.jpg]]
*Table 2: Ablating loss functions, debiasing, and gradient perturbation mechanism on MNIST*

**1. 半去偏 Sinkhorn 损失的偏差-方差折衷**

对比三种损失变体在相同隐私预算下的表现：
- 完全有偏损失（p=0，即经验 Sinkhorn 损失）：FID 53.9
- 完全去偏损失（p=1，使用独立样本批量的无偏估计）：FID 51.0
- **半去偏损失（p=0.4）**：FID 48.4，为最优

这一结果验证了核心论断：完全去偏损失虽然消除了估计偏差，但引入较大方差，在差分隐私噪声下梯度估计不稳定；完全有偏损失方差小但偏差大，导致生成分布偏离真实分布。半去偏损失通过插值在两者之间取得平衡，p=0.4 是偏差-方差的最佳折衷点。Figure 5 进一步展示了 p 在 MNIST 和 Fashion-MNIST 上的系统性影响：p 从 0 增至 0.4 时 FID 和分类错误率同步改善，超过 0.4 后性能开始退化。

![[assets/figures/papers/paper_list_l18_https_arxiv_org_abs_2111_01177/figures/007_Figure_5.jpg]]
*Figure 5: Effect of p on DP-Sinkhorn performance. Left: performance on MNIST. Right: performance on Fashion MNIST. The performance is reported in terms of image quality (FID) and utility (error rate)*

**2. 混合成本函数的作用**

使用纯 L2 平方成本（m=0）时 FID 为 57.1，引入 L1 混合项（m=1 时 FID 48.4，m=3 时 FID 49.5）显著提升图像质量。混合成本 $c_m(\mathbf{x}, \mathbf{y}) = L_2(\mathbf{x}, \mathbf{y})^2 + m L_1(\mathbf{x}, \mathbf{y})$ 中，L2 项提供平滑梯度信号，L1 项保留边缘锐度，二者的协同作用是 Sinkhorn 散度在像素空间有效工作的关键。

**3. 隐私注入位置：图像梯度 vs 参数梯度**

Table 2 直接对比了两种梯度扰动策略：
- 在生成**图像梯度**上裁剪加噪（DP-Sinkhorn 默认方案）：FID 48.4
- 在生成器**参数梯度**上加噪（类 DPSGD 方案）：FID 57.1

图像梯度加噪的优势在于：生成图像的维度远低于参数空间，梯度裁剪的敏感度范数更小，且可以利用 Poisson 子采样的隐私放大效应。这一结果从实验上验证了 Theorem 4.1 的隐私机制设计的有效性。

### 训练稳定性与超参数敏感性

DP-Sinkhorn 展现出 GAN 类方法难以比拟的训练稳定性。**Figure 4a** 显示，在相同超参数设置下，DP-Sinkhorn 的训练损失平稳下降并收敛，无需像 GAN 那样依赖提前停止（early stopping）或精细的生成器-判别器平衡。方法对学习率和优化器选择不敏感，这在差分隐私约束下尤为重要——因为超参数调优本身会消耗隐私预算。

然而，超参数搜索仍是实际部署的瓶颈。Table 4 和 Table 5 分别展示了 MNIST 和 Fashion-MNIST 上的网格搜索结果，涉及噪声乘数 σ、去偏比率 p、混合系数 m 和正则化强度 λ 的组合。每个数据集需要独立搜索，且文中未明确说明调优是否使用独立隐私预算或代理数据，这在实际应用中可能违反差分隐私原则。

![[assets/figures/papers/paper_list_l18_https_arxiv_org_abs_2111_01177/figures/008_Table_4.jpg]]
*Table 4: DP-Sinkhorn ( = 10) hyperparameter search on MNIST*

![[assets/figures/papers/paper_list_l18_https_arxiv_org_abs_2111_01177/figures/009_Table_5.jpg]]
*Table 5: DP-Sinkhorn ( = 10) hyperparameter search on Fashion MNIST*

### 失败模式与局限性

**1. 高分辨率场景的缺失**：所有实验均在低分辨率数据集上进行（MNIST 28×28，Fashion-MNIST 28×28，CelebA 32×32）。方法在更高分辨率（如 64×64 或 128×128）下的表现未经验证，像素级 L1/L2 成本函数在高维空间的适用性存疑。

**2. 训练成本随隐私预算收紧而急剧增长**：CelebA 实验需约 1.7M 训练步、约 40 GPU 小时，隐私预算收紧时所需迭代数进一步增加，限制了方法在资源受限场景下的应用。

**3. 生成质量与非隐私基线差距显著**：即使在最优设置下，MNIST 的 FID 48.4 仍远高于非隐私 Sinkhorn 生成模型（消融中提及但未给出具体数值）。生成图像可能保留可识别的训练样本特征，存在成员推断攻击风险，论文未对此进行系统评估。

**4. 超参数调优与隐私原则的冲突**：网格搜索若直接在私有数据上反复实验，会累积隐私损失；文中未讨论如何在不消耗额外隐私预算的前提下完成超参数选择。

## 定位与知识库关联

### 1. 问题瓶颈与因果杠杆

在差分隐私（DP）下训练生成模型面临一个核心瓶颈：基于GAN的对抗训练范式本身存在训练不稳定和模式崩溃问题，而梯度加噪进一步放大了这些困难。现有DP生成方法依赖大量判别器网络（如**G-PATE**的教师-学生集成）或复杂的梯度聚合机制（如**DataLens**的TopAgg），导致内存消耗大，且超参数调优与隐私预算的严格约束形成根本冲突。

DP-Sinkhorn的因果杠杆在于**用最优传输（OT）原形式中的Sinkhorn散度替代对抗损失**，从根本上避免了生成器-判别器博弈的不稳定性。更关键的是，该方法引入**半去偏Sinkhorn损失**（Definition 4.3, Eq. 6），通过一个可调的去偏比率 $p$ 精细控制梯度估计的偏差-方差折衷——这在隐私噪声叠加的条件下尤为关键，因为高方差估计会淹没梯度信号，而高偏差则导致生成质量退化。

### 2. 方法谱系中的位置

DP-Sinkhorn处于**差分隐私生成模型**与**最优传输生成模型**的交叉点。从DP生成模型谱系看，其前驱包括：

- **DP-CGAN**：将DPSGD直接应用于条件GAN的参数梯度，但继承了GAN的训练不稳定问题。
- **G-PATE**：基于PATE框架，用多个教师判别器的噪声聚合投票训练生成器，避免了直接访问数据，但需要大量判别器网络。
- **GS-WGAN**：在生成图像梯度层面施加高斯机制，利用了图像梯度维度远低于参数梯度的特点，是DP-Sinkhorn隐私机制的直接前驱。
- **DP-MERF**：用最大均值差异（MMD）和随机傅里叶特征替代对抗损失，属于非对抗训练路线，但MMD在高维空间中判别力有限。
- **DataLens**：通过TopAgg梯度压缩与聚合实现DP生成，但依赖复杂的内存管理策略。

DP-Sinkhorn继承并超越了上述方法：它保留了GS-WGAN在图像梯度层面加噪的高效隐私机制（Theorem 4.1），但用Sinkhorn散度替代了GAN的对抗目标，从而继承了DP-MERF等非对抗方法的训练稳定性优势。与DP-MERF的固定核MMD不同，Sinkhorn散度通过最优传输计划自动学习分布间的几何对应关系，提供了更强的判别信号。

从最优传输生成模型谱系看，非隐私的Sinkhorn散度生成模型（如Genevay et al., 2018）已在理论上被证明是Wasserstein距离的忠实近似，但直接将其应用于DP场景面临两个挑战：(1) 经验Sinkhorn损失的有偏性在隐私噪声下被放大；(2) 无偏估计需要独立样本批次，导致方差过大。DP-Sinkhorn的半去偏损失正是针对这两个挑战的创新解决方案。

### 3. 核心技术创新：半去偏损失

DP-Sinkhorn的方法创新集中在一个关键设计选择上。经验Sinkhorn散度存在三种估计形式：

- **有偏估计**（Definition 4.1, Eq. 4）：使用同一批生成数据计算自相关项 $\hat{W}_{\lambda}(\mathbf{X}, \mathbf{X})$，偏差大但方差小。
- **无偏估计**（Definition 4.2, Eq. 5）：使用独立批次 $\mathbf{X}'$ 计算自相关项，偏差为零但方差大。
- **半去偏估计**（Definition 4.3, Eq. 6）：通过混合样本比例 $p$ 在两者间插值，公式为：
  $$\hat{S}_{c,\lambda,p}(\mathbf{X},\mathbf{Y}) = 2\hat{W}_{\lambda}(\mathbf{X}^{[0:n]},\mathbf{Y}) - \hat{W}_{\lambda}(\mathbf{X}^{[0:n]},\mathbf{X}^{[n':n+n']})$$

其中 $n' = \lfloor (1-p)n \rfloor$，交叉项使用全部 $n$ 个生成样本与真实数据计算，自相关项则混合使用部分生成样本。当 $p=0$ 时退化为有偏估计，$p=1$ 时为无偏估计。

消融实验（Table 2, Figure 5）证实了该设计的有效性：$p=0.4$ 在MNIST上达到最佳FID和分类准确率，显著优于完全有偏（$p=0$）和完全无偏（$p=1$）的配置。Figure 4c进一步展示了梯度估计的偏差-方差随 $p$ 变化的曲线，验证了理论预期。

### 4. 隐私机制设计

DP-Sinkhorn的隐私保护遵循一个精确的边界：**仅对与真实数据交互的生成图像梯度施加裁剪和加噪**，而仅用于去偏的合成数据自相关项梯度只做裁剪不加噪（Section 4.3, Algorithm 1 lines 9-11）。这一设计的理论依据是：自相关项 $\hat{W}_{\lambda}(\mathbf{X}, \mathbf{X}')$ 不包含真实数据信息，对其加噪只会无谓消耗隐私预算。

隐私分析基于RDP框架（Theorem 4.1）：对于裁剪常数 $\Delta$ 和噪声 $\gamma \sim \mathcal{N}(0, \Delta^2\sigma^2)$，释放 $\tilde{\mathbf{G}}$ 满足 $(\alpha, 2\alpha n/\sigma^2)$-RDP。配合Poisson子采样，可进一步转换为 $(\epsilon, \delta)$-DP保证。

消融实验（Table 2）对比了“perturb image”（在图像梯度加噪）与“perturb param”（在参数梯度加噪）两种策略，前者显著优于后者，这与图像梯度维度远低于参数梯度的直观一致。

### 5. 适用边界与局限

**适用场景**：
- 低分辨率图像生成（28×28至32×32），在MNIST、Fashion-MNIST和降采样CelebA上验证有效。
- 中等隐私预算（$\epsilon=10$ 量级），在严格DP下（$\delta=10^{-5}$）仍能生成可辨识的图像。
- 需要稳定训练过程的场景，DP-Sinkhorn对学习率和优化器不敏感（Figure 4a），无需像GAN那样提前停止。

**已知局限**：
- **高分辨率未验证**：仅在低分辨率数据集上实验，高分辨率生成能力未知。
- **训练成本高**：CelebA上需约1.7M步、约40 GPU小时，且迭代数随隐私预算收紧急剧增加。
- **超参数敏感**：$p$、$m$、$\lambda$、$\sigma$ 等需针对每个数据集进行网格搜索（Table 4, Table 5），若直接在私有数据上反复实验会消耗隐私预算，论文未明确说明调优是否使用独立预算或代理数据。
- **生成质量差距**：FID仍远低于非隐私生成模型，且生成图像可能包含可被利用的训练样本特征，存在成员推断攻击风险，论文未系统评估此种攻击下的隐私鲁棒性。
- **成本函数局限**：当前使用像素级混合L1/L2成本 $c_m(\mathbf{x}, \mathbf{y}) = L_2(\mathbf{x}, \mathbf{y})^2 + m L_1(\mathbf{x}, \mathbf{y})$，在感知质量上不如对抗特征距离。

### 6. 开放问题

1. **生成器架构升级**：能否用扩散模型或Transformer替代当前DCGAN/BigGAN生成器，在保持DP的同时提升复杂数据集上的生成质量？
2. **自适应成本函数**：能否用感知损失（如LPIPS）或对抗特征距离替代像素级成本，在不牺牲隐私的前提下提高视觉保真度？
3. **跨模态扩展**：DP-Sinkhorn在医学影像、金融表格等非图像数据以及多模态生成任务中的隐私-效用权衡如何？
4. **超参数自动调优**：能否通过元学习或在线贝叶斯优化自动调整 $p$ 等关键超参数，避免额外的手动调优和隐私预算消耗？
5. **隐私鲁棒性强化**：如何增强对成员推断攻击的防御能力，并在理论RDP保证与实际攻击成功概率之间建立更紧密的联系？

## 原文 PDF

![[paperPDFs/NEURIPS_2021/Don_t_Generate_Me_Training_Differentially_Private_Generative_Models_with_Sinkhorn_Divergence.pdf]]
