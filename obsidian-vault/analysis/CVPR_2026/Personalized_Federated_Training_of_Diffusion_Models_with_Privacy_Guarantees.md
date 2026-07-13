---
title: Personalized Federated Training of Diffusion Models with Privacy Guarantees
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Personalized_Federated_Training_of_Diffusion_Models_with_Privacy_Guarantees.pdf
project_link: null
code_link: null
aliases:
- PPFDM
- PFTDMPG
tags:
- CVPR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 将扩散过程分解为客户端个性化去噪与共享去噪，并通过控制前向扩散步数 t0 调节添加噪声的强度，从而平衡隐私与效用。
primary_logic: 利用扩散模型的粗到细生成特性：客户端对私人数据施加校准的高斯噪声后仅共享扩散后的数据，共享模型学习粗粒度通用结构，而客户端本地模型恢复个性化细节，实现既保护隐私又提升少数类生成质量的协作训练。
claims:
- 定理5.1给出了基于扩散噪声的本地差分隐私保证，隐私参数ε由t0和裁剪参数C控制。
- 定理5.2在高斯混合模型上证明协作训练能显著降低2-Wasserstein距离，尤其当全局样本量远大于本地时。
- 实验表明，本方法在CIFAR-10、Colorized MNIST和CelebA上对少数类FID有大幅改善，且成员推理攻击AUC接近随机（~50%），重建攻击得分低，无记忆样本。
- CIFAR-10 上 FID (平均) = 27.82
---

# Personalized Federated Training of Diffusion Models with Privacy Guarantees

> [!tip] 核心洞察
> 利用扩散模型的粗到细生成特性：客户端对私人数据施加校准的高斯噪声后仅共享扩散后的数据，共享模型学习粗粒度通用结构，而客户端本地模型恢复个性化细节，实现既保护隐私又提升少数类生成质量的协作训练。

| 字段 | 内容 |
|------|------|
| 中文题名 | 具有隐私保障的个性化联邦扩散模型训练 |
| 英文题名 | Personalized Federated Training of Diffusion Models with Privacy Guarantees |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Patel_Personalized_Federated_Training_of_Diffusion_Models_with_Privacy_Guarantees_CVPR_2026_paper.html) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | PFDM (Personalized Federated Diffusion Model) |
| Dataset | CIFAR-10, Colorized MNIST, CelebA, MNIST |

> [!tip] 效果简介
> - CIFAR-10 上，FID (平均) 27.82 vs 28.16 (Non-collaborative) (-0.34)。
> - Colorized MNIST 上，FID (平均) 3.26 vs 4.09 (Non-collaborative) (-0.83)。
> - CelebA 上，FID (平均) 23.10 vs 32.40 (Non-collaborative) (-9.30)。

## 概要

**核心问题**：现有的联邦扩散模型训练方案缺乏形式化隐私保障。全局扩散模型存在严重的记忆风险，可能泄露客户端私有数据；同时，单一全局模型无法为不同客户端提供个性化生成能力。直接对扩散模型施加差分隐私训练（如 **DPDM**，Dockhorn et al., arXiv 2022）会严重损害生成质量，导致效用与隐私难以兼得。

**核心思路**：本文提出 **PFDM（Personalized Federated Diffusion Model）**，利用扩散模型“粗到细”的生成特性，将去噪过程分解为**客户端个性化去噪**与**共享全局去噪**两部分。客户端对本地数据进行裁剪后，施加 $t_0$ 步前向扩散噪声，仅将加噪后的数据集 $\tilde{D}_m$ 上传至服务器；共享模型仅学习各客户端加噪数据的混合分布（粗粒度通用结构），而客户端本地模型负责从中间噪声状态恢复个性化细节。这一设计使共享模型始终无法接触原始数据，从根本上降低了记忆风险。

**隐私保障**：定理5.1给出了基于扩散噪声的本地差分隐私（LDP）保证，隐私参数 $\varepsilon$ 由扩散步数 $t_0$ 和裁剪参数 $C$ 共同控制。每个样本在上传前即获得独立的隐私保护，无需信任服务器。

**理论支撑**：定理5.2在高斯混合模型（GMM）上证明，协作训练能够显著降低生成分布与真实分布之间的 2-Wasserstein 距离，尤其当全局样本量远大于本地样本量时，协作带来的效用增益更为突出。

**实验验证**：在 CIFAR-10、Colorized MNIST 和 CelebA 三个数据集上，PFDM 对少数类样本的 FID 有大幅改善（CelebA 上从 32.40 降至 23.10），且成员推理攻击 AUC 接近随机猜测（~50%），重建攻击恢复分数极低，全局模型输出无法还原可辨认的原始信息，表明方法在提升生成质量的同时提供了强有力的隐私保护。



扩散模型已成为当前最先进的生成模型之一，在图像合成、视频生成、分子设计等领域展现出卓越的生成能力。然而，扩散模型的训练通常需要将大规模数据集中到单一服务器，这在医疗影像、金融记录、个人照片等隐私敏感场景下构成严重障碍。联邦学习允许多个客户端在不共享原始数据的前提下协作训练模型，为解决上述隐私困境提供了自然框架。

**现有联邦扩散模型训练的缺口。** 直接将联邦学习范式应用于扩散模型面临三重挑战。其一，现有联邦扩散模型训练方法（如 FedDM，Vora et al., arXiv 2024）缺乏形式化隐私保障——客户端上传的模型更新或中间表示仍可能泄露训练数据信息。其二，全局扩散模型存在记忆风险：训练后的模型可能重现训练样本，构成隐私泄露。其三，全局单一模型无法提供个性化控制——不同客户端的数据分布各异，全局模型对少数类样本的生成质量往往显著劣于多数类。

**直接应用差分隐私的困境。** 一个直观的补救方案是在扩散模型训练中引入差分隐私（DP）。然而，现有工作（如 DPDM，Dockhorn et al., arXiv 2022）表明，直接对扩散模型施加 DP 训练会严重降低生成质量。其根本原因在于，扩散模型的去噪网络需要学习高维数据分布中的精细结构，而 DP 噪声会破坏这些关键信息，导致生成样本模糊或失真。这一隐私-效用权衡在联邦场景下尤为突出：客户端本地数据量有限，DP 噪声的相对影响更大。

**核心动机与解决思路。** 本文的动机在于设计一种既能提供形式化隐私保障、又能保持高生成质量、同时支持个性化生成的联邦扩散模型训练框架。关键洞察源于扩散模型本身的粗到细生成特性：前向扩散过程向数据注入高斯噪声，早期扩散步骤主要破坏细粒度细节而保留粗粒度结构。这意味着，若客户端仅共享经过充分扩散的噪声数据，服务器只能学习到粗粒度的通用结构，而无法恢复可辨认的个人信息；与此同时，客户端保留的本地去噪器则负责从粗粒度结构中恢复个性化细节。这一设计天然地将隐私保护（通过扩散噪声实现）与个性化生成（通过本地去噪器实现）解耦，同时利用多客户端数据的聚合提升少数类的生成质量。

基于上述洞察，本文提出 **PFDM（Personalized Federated Diffusion Model）**，将扩散模型的逆向去噪过程分解为客户端个性化去噪与共享全局去噪两部分，并通过控制前向扩散步数 $t_0$ 精确调节添加噪声的强度，从而在隐私与效用之间建立可量化的权衡机制。



## 核心方法与创新机理

### 问题瓶颈：联邦扩散模型的隐私与效用双重困境

当前联邦扩散模型训练面临三个相互交织的挑战。第一，现有方法缺乏形式化隐私保障——无论是集中式训练还是 **FedDM**（Vora et al., arXiv 2024）等联邦方法，均未提供可证明的差分隐私保证，使模型暴露于成员推理、记忆和重建攻击之下。第二，直接应用差分隐私训练（如 **DPDM**，Dockhorn et al., arXiv 2022）会严重降低生成质量，在 MNIST 两客户端场景下 FID 从 6.96 飙升至 33.73。第三，独立训练（Non-collaborative）虽天然保护隐私，但在数据量不足的少数类上生成质量极差——例如 CelebA 上 Non-collaborative 的 FID 达 32.40，远高于本文方法的 23.10。

### 核心洞察：扩散过程的粗到细分解

PFDM 的核心洞察源于扩散模型的一个基本特性：**前向扩散逐步破坏数据的细粒度信息，而粗粒度结构在较大噪声水平下仍可保留**。具体而言，当对私人样本施加 $t_0$ 步高斯噪声后，所得加噪样本在保留类别级颜色和布局信息的同时，已丧失可辨识的个人细节（见 Figure 3）。这启发了一种自然的分工：

- **客户端**在本地训练个性化去噪器 $z_{\theta_m}$，掌握从加噪状态恢复精细细节的能力；
- **共享全局去噪器** $z_w$ 仅学习从纯噪声生成加噪样本的粗粒度分布，无需接触原始数据。

这一分解使协作训练成为可能：客户端上传的是经裁剪和 $t_0$ 步扩散后的加噪数据集 $\tilde{D}_m$，而非原始数据或模型参数，从根本上切断了全局模型接触隐私敏感信息的路径。

### 变更槽位一：模型架构从单一去噪器到双组件分解

传统扩散模型使用单一全局去噪器（通常为 UNet）完成从噪声到完整样本的端到端生成。PFDM 将其拆分为两个功能互补的组件：

| 组件 | 训练位置 | 功能 | 隐私属性 |
|------|----------|------|----------|
| 客户端去噪器 $z_{\theta_m}$ | 各客户端本地 | 从 $t_0$ 步加噪状态恢复个性化细节 | 不共享，完全本地化 |
| 共享去噪器 $z_w$ | 服务器 | 从纯噪声生成加噪样本的混合分布 | 仅接触加噪数据，可安全分发 |

这一架构变更（Algorithm 1, Section 4）实现了“粗粒度共享、细粒度本地化”的隐私-效用平衡。

### 变更槽位二：数据共享方式从原始数据到扩散加噪数据

传统联邦学习直接共享原始数据或模型更新，存在严重的隐私泄露风险。PFDM 引入了一个关键的数据预处理流程（Algorithm 1 lines 3-8）：

1. **裁剪**：对本地数据施加范数约束，限制单个样本对加噪分布的影响；
2. **$t_0$ 步前向扩散**：施加受控量的高斯噪声，将数据转化为 $\tilde{D}_m$；
3. **上传加噪数据集**：服务器仅接收这些加噪样本。

这一设计的隐私保障由 **Theorem 5.1** 形式化：每个上传样本满足 $(\varepsilon, \delta)$-本地差分隐私，其中 $\varepsilon = \frac{2C^2}{\sigma^2} + C\sqrt{\frac{8\log(1/\delta)}{\sigma^2}}$，噪声方差 $\sigma^2 = (1 - \bar{\alpha}_{t_0}) / \bar{\alpha}_{t_0}$ 由扩散步数 $t_0$ 和裁剪参数 $C$ 联合控制。$t_0$ 成为调节隐私-效用权衡的核心旋钮：增大 $t_0$ 增强隐私但损失信息，减小 $t_0$ 保留更多细节但降低隐私保护。

### 变更槽位三：生成流程从单阶段到两阶段级联

PFDM 的采样过程（Algorithm 2）将传统扩散模型的单阶段去噪扩展为两阶段级联：

1. **全局粗生成**：共享模型 $z_w$ 从纯噪声 $x_T \sim \mathcal{N}(0,I)$ 出发，执行 $T - t_0$ 步去噪，得到中间加噪样本 $x_{t_0}$，该样本仅包含粗粒度结构；
2. **本地精炼**：客户端个性化去噪器 $z_{\theta_m}$ 从 $x_{t_0}$ 出发，执行 $t_0$ 步去噪，恢复精细的个性化细节，得到最终样本 $x_0$。

这一级联设计确保：即使攻击者获取共享模型，也只能生成模糊的加噪样本，无法还原可辨识的个人信息（Figure 3 中全局模型输出数字形状不可辨认）；而完整生成能力仅存在于同时拥有两个组件的合法客户端。

### 理论支撑：高斯混合模型下的效用保证

**Theorem 5.2** 在高斯混合模型（GMM）假设下，给出了 PFDM 生成分布与真实分布之间 2-Wasserstein 距离的上界：

$$\mathbb{E}_{\tilde{D},D_m}\Big[W_2^2(q; p_{\tilde{D},D_m}^m) \mid y=k\Big] = O\Big(\frac{2}{2+3\sigma^2} \cdot \frac{d^2}{N_k} + \frac{3\sigma^2}{2+3\sigma^2} \cdot \frac{d^2}{n_k^m}\Big)$$

该上界揭示了协作训练的双重收益来源：第一项由全局样本量 $N_k$ 主导，第二项由本地样本量 $n_k^m$ 主导。当全局样本量远大于本地时（$N_k \gg n_k^m$），协作训练显著降低误差。进一步，**Equation (9)** 量化了相对于独立训练的效用增益：

$$\mathbb{E}_{\tilde{D},D_m}\Big[W_2^2(q; p_{D_m}^m) - W_2^2(q; p_{\tilde{D},D_m}^m) \mid y=k\Big] = \Omega\Big(\frac{\sigma^2+1}{(2\sigma^2+1)^2} \cdot \frac{d^2}{n_k^m}\Big)$$

该增益在本地样本量 $n_k^m$ 较小时尤为显著，从理论上解释了 PFDM 在少数类上的优异表现。

### 与现有方法的本质区别

相较于 **FedDM**（仅实现联邦训练而无隐私保障），PFDM 通过扩散噪声注入提供了可证明的本地差分隐私保证，且全局模型本身无法生成可辨识样本。相较于 **DPDM**（直接对训练过程施加差分隐私），PFDM 避免了在模型训练中注入噪声导致的严重质量退化——实验表明 DPDM+FL 在 MNIST 上的 FID 高达 33.73，而 PFDM 仅为 6.96。相较于 **Non-collaborative**（完全独立训练），PFDM 通过共享加噪数据实现了跨客户端的知识迁移，在少数类上获得显著质量提升。

### 方法局限性

需要指出，当前理论分析局限于高斯混合模型，尚未推广到通用扩散模型架构；隐私参数 $\varepsilon=10$ 的本地差分隐私虽在实践中提供强保护（成员推理攻击 AUC 接近 50%），但理论上仍可进一步收紧；实验主要在中低分辨率数据集上进行，高分辨率扩展仍是开放挑战。此外，方法假设标签公开，不保护标签隐私，且未考虑恶意客户端的投毒攻击。



PFDM 将扩散模型的生成过程拆分为**客户端个性化去噪**与**共享全局去噪**两个阶段，通过控制前向扩散步数 $t_0$ 来调节添加噪声的强度，从而在隐私保护与生成效用之间取得平衡。整个框架包含四个核心模块，形成“本地训练—加噪上传—全局聚合—协作采样”的闭环。

### 模块一：客户端个性化去噪器训练

各客户端 $m$ 在本地使用标准 DDPM 训练目标独立训练一个个性化去噪器 $z_{\theta_m}$，该模型始终保留在本地，不参与任何共享。训练损失为：

$$\mathbb{E}_{t \sim \mathcal{U}(1,T), \boldsymbol{x}_{0}, \boldsymbol{z}_{t}} \left[ \lVert \boldsymbol{z}_{t} - \boldsymbol{z}_{\boldsymbol{\theta}}(\boldsymbol{x}_{t}, t) \rVert_{2}^{2} \right]$$

这一步骤确保每个客户端捕获自身数据的细粒度特征，为后续个性化生成奠定基础（Algorithm 1 lines 1–2）。

### 模块二：加噪数据集构造

客户端对本地数据先进行裁剪以限制数据范数，然后施加 $t_0$ 步前向扩散过程，生成加噪数据集 $\tilde{D}_m$ 并上传至服务器。前向扩散过程由下式定义：

$$x_{t} = \sqrt{\bar{\alpha}_{t}} x_{0} + \sqrt{1 - \bar{\alpha}_{t}} z_{t},\; z_{t} \sim \mathcal{N}(0, I)$$

经 $t_0$ 步扩散后，客户端 $m$ 的数据分布变为：

$$q_{m}(x_{t_{0}}) := \int q_{0}^{m}(x_{0}) q(x_{t_{0}} | x_{0}) dx_{0}$$

其中 $q(x_{t} | x_{0}) := \mathcal{N}(x_{t}; \sqrt{\bar{\alpha}_{t}} x_{0}, (1 - \bar{\alpha}_{t}) I)$。扩散噪声的强度由 $t_0$ 控制——$t_0$ 越大，噪声越强，隐私保护越好，但共享模型可利用的结构信息越少。这一设计利用了扩散模型“粗到细”的生成特性：客户端仅共享严重加噪后的数据，共享模型只能学到粗粒度的通用结构（如颜色、布局），而无法还原可辨认的个体信息（Algorithm 1 lines 3–7）。

### 模块三：共享全局去噪器训练

服务器聚合所有客户端上传的加噪数据集，训练一个共享全局去噪器 $z_w$。该模型学习从标准高斯噪声到加噪客户端数据混合分布的映射，即学习“噪声到噪声”的转换。由于训练数据本身已高度加噪，全局模型无法生成客户端特定的可辨认样本，从而天然具备隐私保护能力（Algorithm 1 lines 9–10）。训练完成后，该共享模型可安全分发给所有客户端。

### 模块四：协作采样生成

采样阶段采用两阶段去噪流程（Algorithm 2）：首先由共享全局去噪器 $z_w$ 执行 $T$ 步去噪，将标准高斯噪声映射为中间样本；然后由客户端个性化去噪器 $z_{\theta_m}$ 执行 $t_0$ 步去噪，将中间样本精炼为最终的高质量生成样本。这一设计使得共享模型负责粗粒度结构生成，而客户端模型负责恢复个性化细节，实现了“全局结构共享、局部细节保留”的协作生成范式。

### 隐私-效用调控机制

整个框架的核心调控旋钮是前向扩散步数 $t_0$。定理 5.1 给出了基于扩散噪声的本地差分隐私保证，隐私参数 $\varepsilon$ 由噪声方差 $\sigma^2 = (1 - \bar{\alpha}_{t_0}) / \bar{\alpha}_{t_0}$ 和裁剪参数 $C$ 共同决定。定理 5.2 则在高斯混合模型上证明，当全局样本量远大于本地样本量时，协作训练能显著降低生成分布与真实分布之间的 2-Wasserstein 距离，尤其对少数类样本的改善幅度可达 $\Omega\big(\frac{\sigma^2+1}{(2\sigma^2+1)^2} \cdot \frac{d^2}{n_k^m}\big)$。实验表明，在 CIFAR-10、Colorized MNIST 和 CelebA 上，该方法对少数类 FID 有大幅改善，同时成员推理攻击 AUC 接近随机猜测（~50%），重建攻击得分低，且无记忆样本（Table 1, Table 2, Table 3, Figure 3）。



### 4.1 方法总览与模块划分

PFDM 将扩散模型的训练与采样过程分解为两个核心阶段，对应四个关键模块：

**阶段一：客户端个性化去噪器训练**
- **模块1 — 客户端个性化去噪器训练**：各客户端 $m$ 在本地使用标准 DDPM 目标训练专属去噪网络 $z_{\theta_m}$，该网络**永不共享**，保留客户端特有的数据分布知识。

**阶段二：共享全局去噪器训练**
- **模块2 — 加噪数据集构造**：客户端对本地数据施加裁剪操作以限制数据范数，随后执行 $t_0$ 步前向扩散过程，生成加噪数据集 $\tilde{D}_m$ 并上传至服务器。这一步是整个框架的**隐私控制旋钮**——$t_0$ 越大，添加的噪声越强，隐私保护越强，但保留的原始信息越少。
- **模块3 — 共享全局去噪器训练**：服务器聚合所有客户端上传的加噪数据集，训练全局去噪网络 $z_w$。该模型仅见过加噪样本，可安全分发给所有客户端。
- **模块4 — 采样生成**：推理时先使用全局去噪器 $z_w$ 进行 $T$ 步去噪得到中间样本，再由客户端个性化去噪器 $z_{\theta_m}$ 进行 $t_0$ 步精细去噪得到最终样本。

### 4.2 关键公式与变量含义

#### 前向扩散过程（加噪数据集构造的理论基础）

$$x_t = \sqrt{\bar{\alpha}_t} x_0 + \sqrt{1 - \bar{\alpha}_t} z_t, \quad z_t \sim \mathcal{N}(0, I)$$

其中 $\bar{\alpha}_t = \prod_{s=1}^{t} (1 - \beta_s)$，$\beta_s$ 为预定义的噪声调度参数。该公式描述了从原始样本 $x_0$ 逐步添加高斯噪声得到潜在变量 $x_t$ 的过程。在 PFDM 中，客户端在 $t = t_0$ 处截断该过程，生成上传至服务器的加噪样本。

#### 扩散后分布

$$q_m(x_{t_0}) := \int q_0^m(x_0) q(x_{t_0} | x_0) dx_0$$

其中 $q_0^m$ 为客户端 $m$ 的原始数据分布，$q(x_{t_0} | x_0) = \mathcal{N}(x_{t_0}; \sqrt{\bar{\alpha}_{t_0}} x_0, (1 - \bar{\alpha}_{t_0}) I)$ 为前向扩散转移核。该积分刻画了经过 $t_0$ 步扩散后客户端数据的边缘分布——这是服务器实际观察到的数据分布。

#### DDPM 训练目标（客户端与全局去噪器共享的损失函数）

$$\mathbb{E}_{t \sim \mathcal{U}(1,T), \boldsymbol{x}_0, \boldsymbol{z}_t} \left[ \lVert \boldsymbol{z}_t - \boldsymbol{z}_{\boldsymbol{\theta}}(\boldsymbol{x}_t, t) \rVert_2^2 \right]$$

神经网络 $z_\theta$ 学习预测添加到样本中的噪声 $\boldsymbol{z}_t$。客户端去噪器 $z_{\theta_m}$ 和全局去噪器 $z_w$ 均使用此损失训练，区别在于训练数据：前者使用原始本地数据，后者使用加噪数据集 $\tilde{D}_m$。

#### 局部差分隐私保证

$$\left( \frac{2 C^2}{\sigma^2} + C \sqrt{ \frac{8 \log(1/\delta)}{\sigma^2} }, \delta \right)\text{-LDP}$$

其中 $\sigma^2 = (1 - \bar{\alpha}_{t_0}) / \bar{\alpha}_{t_0}$ 为有效噪声方差，$C$ 为数据裁剪范数上界。该定理（Theorem 5.1）量化了每个上传样本的隐私保护强度：隐私参数 $\varepsilon$ 由 $t_0$（通过 $\sigma^2$）和裁剪参数 $C$ 共同控制。$t_0$ 增大 → $\sigma^2$ 增大 → $\varepsilon$ 减小 → 隐私保护增强。

#### 效用保证（高斯混合模型下的理论分析）

$$\mathbb{E}_{\tilde{D},D_m} \Big[ W_2^2 \big( q ; p_{\tilde{D},D_m}^m \big) \mid y = k \Big] = O \bigg( \frac{2}{2 + 3\sigma^2} \cdot \frac{d^2}{N_k} + \frac{3\sigma^2}{2 + 3\sigma^2} \cdot \frac{d^2}{n_k^m} \bigg)$$

该定理（Theorem 5.2）在高斯混合模型假设下，给出了生成分布与真实分布之间 2-Wasserstein 距离的上界。其中 $N_k$ 为所有客户端中类别 $k$ 的总样本量，$n_k^m$ 为客户端 $m$ 中类别 $k$ 的本地样本量，$d$ 为数据维度。公式揭示了协作的核心增益机制：第一项随全局样本量 $N_k$ 增大而减小，第二项取决于本地样本量 $n_k^m$ 和噪声强度 $\sigma^2$。

#### 相对非协作训练的效用提升

$$\mathbb{E}_{\tilde{D},D_m} \Big[ W_2^2 \big( q ; p_{D_m}^m \big) - W_2^2 \big( q ; p_{\tilde{D},D_m}^m \big) \mid y = k \Big] = \Omega \bigg( \frac{\sigma^2 + 1}{(2\sigma^2 + 1)^2} \cdot \frac{d^2}{n_k^m} \bigg)$$

该公式定量刻画了 PFDM 相对于独立非协作训练的**理论增益**。增益大小与本地样本量 $n_k^m$ 成反比——本地数据越稀缺（少数类），协作带来的提升越显著。这从理论上解释了为何 PFDM 在少数类上表现尤为突出。

### 4.3 理论分析的去噪网络参数化

为便于理论推导，文中在高斯混合模型分析中采用分段线性去噪网络：

$$\epsilon_{\theta}(x, y) = \sum_{k=1}^{K} \mathbf{1}_{y=k} \left[ W^{k} x + V^{k} c(y) \right]$$

其中 $y$ 为类别标签，$c(y)$ 为标签的条件嵌入，$W^k$ 和 $V^k$ 为类别特定的参数矩阵。该参数化假设标签 $y$ 是公开可用的（方法不保护标签隐私），使得分析可解。

> **注意**：上述效用保证（Theorem 5.2）和相对提升公式均基于高斯混合模型的简化假设，尚未推广到一般扩散模型架构，这是本文明确指出的理论局限。



## 实验与关键发现

### 生成质量主结果

PFDM 在三个标准数据集上与无隐私集中式训练（上限）、非隐私联邦扩散模型基线 **FedDM**（Vora et al., arXiv 2024）、无协作独立训练（隐私极限）以及直接差分隐私扩散基线 **DPDM**（Dockhorn et al., arXiv 2022）进行了全面对比。Table 1 汇总了 FID 分数（越低越好）。

![[assets/figures/papers/paper_list_l909_https_openaccess_thecvf_com_content_CVPR2026_html_Patel_Personalized_Fed/figures/001_Table_1.jpg]]
*Table 1: FID scores for different methods on different datasets (lower is better)*

在 CIFAR-10 上，PFDM 平均 FID 为 **27.82**，优于非协作训练的 28.16（Δ = -0.34），接近无隐私集中式的 24.84。在 Colorized MNIST 上，PFDM 达到 **3.26**，相比非协作的 4.09 有显著改善（Δ = -0.83）。在 CelebA 上的提升最为突出：PFDM 的 FID 为 **23.10**，而非协作训练高达 32.40（Δ = -9.30），说明协作机制对复杂人脸数据中少数类的生成质量改善尤为关键。

在无彩色的 MNIST 两客户端场景下，PFDM 的 FID 仅为 **6.96**，而 DPDM+FL 基线高达 33.73（Δ = -26.77），表明直接对扩散模型施加差分隐私训练会严重损害生成质量，而 PFDM 通过扩散噪声提供隐私保护的同时几乎不牺牲效用。

Figure 1 的定性对比进一步印证了上述结论：在 CelebA 的多数类（黑发男性）和少数类（非黑发女性）上，PFDM 生成的样本均保持了高保真度，而非协作训练在少数类上出现明显退化。

![[assets/figures/papers/paper_list_l909_https_openaccess_thecvf_com_content_CVPR2026_html_Patel_Personalized_Fed/figures/003_Figure_1.jpg]]
*Figure 1: CelebA samples generated by different methods. (a), (b) correspond to samples generated for majority class group: Black Hair and Male. (c), (d) correspond to samples generated for minority class group: NonBlack Hair and Female. We report the results for the model trained by the first client*

### 隐私保护实证

PFDM 的隐私保护效果通过三类攻击进行评估。

**成员推理攻击（MIA）**：Table 2 报告了全局模型（训练 300 轮）的 MIA 结果。在 CIFAR-10、Colorized MNIST 和 CelebA 上，AUC 均接近 **50%**（随机猜测水平），TPR@1%FPR 极低。作为对比，标准非隐私集中式模型在相同数据集上的 AUC 分别高达 82.13%、99.62% 和 99.59%（见附录 D Table 6），证明 PFDM 的全局模型几乎不泄露成员信息。

**重建攻击**：Table 3 展示了不同攻击场景下的恢复分数（分数越低表示重建越好，0 表示完美重建）。在无攻击（None）场景下恢复分数接近 1（无法重建）；使用协作训练的全局模型（Global）攻击和使用在相似数据集上预训练的去噪器（Pretrained）攻击，恢复分数均远高于 0，说明上传的加噪图像有效抵抗重建。Figure 4 直观展示了 CelebA 上的重建结果：客户端上传的加噪图像、原始干净图像、预训练模型攻击者的重建以及全局模型攻击者的重建，后两者均无法还原可辨认的人脸细节。

**记忆攻击**：Figure 3 展示了全局模型生成的样本——仅保留了颜色和布局信息，数字形状完全无法辨认，直观验证了全局模型未记忆客户端特定样本。

### 可扩展性消融

Figure 2 展示了客户端数量从 4 增加到 128 时，协作方法与非协作方法的 FID 差距变化。随着客户端数量增加，数据异构性增强，协作方法的优势持续扩大，表明 PFDM 在高度分散的数据场景下具有更强的鲁棒性和可扩展性。

### 方法公平性与局限性

PFDM 在少数类上的生成质量提升尤为显著，有助于缓解联邦学习中的数据不平衡问题。采用的本地差分隐私 ε=10 看似较大，但为每个样本提供的是本地 DP 保证，其保护强度远高于同等 ε 的中心化 DP，且在实际攻击评估中仍表现出强保护效果。需要注意的是，该方法假设标签是公开的，不保护标签隐私。

### 待验证与开放问题

理论分析目前局限于高斯混合模型，尚未推广到更一般的模型类别；实验主要在中低分辨率数据集上进行，扩展到高分辨率图像生成是一大挑战；隐私保证可能通过更先进的差分隐私记账技术进一步收紧。此外，在存在恶意客户端（如投毒攻击）时方法的鲁棒性仍需进一步研究。以上局限性在原文中已明确标注，读者可据此评估方法的适用边界。

### 补充图表

![[assets/figures/papers/paper_list_l909_https_openaccess_thecvf_com_content_CVPR2026_html_Patel_Personalized_Fed/figures/002_Figure.jpg]]
*Figure: (a)Ours (c) Ours (b) Non-collaborative DMs (d) Non-collaborative DMs*

![[assets/figures/papers/paper_list_l909_https_openaccess_thecvf_com_content_CVPR2026_html_Patel_Personalized_Fed/figures/005_Figure_4.jpg]]
*Figure 4: Reconstruction results on CelebA. The four rows show: (1) the noisy images uploaded by the client, (2) the original clean images, (3) reconstructions produced by the pretrained-model attacker, and (4) reconstructions produced by the global-model attacker*

![[assets/figures/papers/paper_list_l909_https_openaccess_thecvf_com_content_CVPR2026_html_Patel_Personalized_Fed/figures/006_Table_2.jpg]]
*Table 2: MIA results for our method (global model used in our framework trained for 300 epochs). 50% AUC/ASR means the random guess. Lower TPR@1% FPR indicates stronger privacy protection. MIA on a standard nonprivate model (centralized method) achieves 82.13%,99.62%,99.59% AUC for CIFAR-10, Colorized MNIST, and CelebA (see Table 6 in Appendix D)*

![[assets/figures/papers/paper_list_l909_https_openaccess_thecvf_com_content_CVPR2026_html_Patel_Personalized_Fed/figures/007_Table_3.jpg]]
*Table 3: Recovery score for various reconstruction attacks on the noisy image received by the server: “None” (no attack), “Global” (attack using the collaboratively trained global model in our framework), and “Pretrained” (attack using a denoiser pretrained on a similar dataset). Lower recovery score indicate better reconstructions (0 means perfect reconstruction). Reconstruction examples appear in Figure 4, also see Figures 8, 9 in Appendix D*

![[assets/figures/papers/paper_list_l909_https_openaccess_thecvf_com_content_CVPR2026_html_Patel_Personalized_Fed/figures/004_Figure_3.jpg]]
*Figure 3: Samples generated by the global model used in our framework with red digits 0 to 9. The output digit shapes remain unrecognizable, indicating strong privacy protection of our method*



## 定位与知识库关联

### 1. 与现有基线的结构性区别

PFDM 的核心创新在于将扩散模型的生成过程分解为**客户端个性化去噪**与**共享全局去噪**两个阶段，这与现有方法在数据共享方式和模型架构上存在根本性差异。

| 方法 | 数据共享方式 | 模型架构 | 隐私保障 | 个性化能力 |
|------|------------|---------|---------|-----------|
| 集中式训练（上限） | 原始数据集中 | 单一全局去噪器 | 无 | 无 |
| **FedDM** (Vora et al., arXiv 2024) | 共享模型更新 | 单一全局去噪器 | 无形式化保证 | 无 |
| 独立训练（隐私极限） | 不共享 | 各自独立去噪器 | 完美隔离 | 完全个性化 |
| **DPDM** (Dockhorn et al., arXiv 2022) | 共享模型更新 | 单一去噪器+DP噪声 | 中心化DP | 无 |
| **PFDM（本文）** | 共享加噪数据集 | 客户端去噪器+共享去噪器 | 本地差分隐私 | 完全个性化 |

**关键区别**：

1. **与 FedDM 的区别**：FedDM 通过拆分 UNet 为共享和本地模块实现联邦训练，但客户端仍需共享模型更新，缺乏形式化隐私保障。PFDM 则完全避免共享模型参数或原始数据——客户端仅上传经过 $t_0$ 步前向扩散的加噪样本，服务器无法从这些样本中恢复可辨认的原始信息。

2. **与 DPDM 的区别**：DPDM 在训练过程中直接注入差分隐私噪声（如 DP-SGD），这会严重降低生成质量。PFDM 利用扩散过程本身的噪声作为隐私保护机制，通过控制前向扩散步数 $t_0$ 来调节噪声强度，在隐私与效用之间取得更优平衡。实验显示，在 MNIST 两客户端场景下，PFDM 的 FID 为 6.96，而 DPDM+FL 为 33.73，差距达 26.77。

3. **与独立训练的区别**：独立训练提供最强的隐私隔离，但在数据量有限（尤其是少数类）时生成质量差。PFDM 通过共享加噪数据实现协作，使全局模型学习粗粒度通用结构（如颜色、布局），而客户端本地模型恢复个性化细节。实验表明，在 CelebA 少数类上，PFDM 的 FID 为 23.10，而独立训练为 32.40，改善幅度达 9.30。

### 2. 适用边界与前提假设

**适用条件**：

- **标签公开假设**：方法假设类别标签是公开信息，不保护标签隐私。这在许多实际场景中合理（如医疗诊断中疾病类型已知），但在标签本身敏感的场景下不适用。
- **客户端诚实假设**：当前设计未考虑恶意客户端可能发起的投毒攻击或策略行为。
- **中低分辨率数据**：实验主要在 CIFAR-10（32×32）、Colorized MNIST（28×28）和 CelebA（64×64）上进行，扩展到高分辨率图像面临计算和通信开销挑战。

**不适用场景**：

- 标签与数据同样敏感的场景（如某些金融或医疗记录）。
- 存在恶意客户端的对抗性联邦学习环境。
- 需要极高隐私预算（$\varepsilon \ll 1$）的场景——本文的本地差分隐私 $\varepsilon=10$ 看似较大，但需注意这是**本地 DP**，其保护强度远高于同等 $\varepsilon$ 的中心化 DP。实验表明，即使在此设置下，成员推理攻击 AUC 仍接近随机猜测（~50%），显示出强实际保护。

### 3. 理论保证的局限

**定理 5.1** 给出了基于扩散噪声的本地差分隐私保证，隐私参数 $\varepsilon$ 由 $t_0$ 和裁剪参数 $C$ 控制：

$$\left( \frac{2 C^{2}}{\sigma^{2}} + C \sqrt{ \frac{8 \log(1/\delta)}{\sigma^{2}} }, \delta \right)\text{-LDP}$$

其中 $\sigma^2 = (1 - \bar{\alpha}_{t_0}) / \bar{\alpha}_{t_0}$。该保证的局限性在于：

- 仅考虑高斯机制，未利用更先进的差分隐私记账技术（如 Rényi DP、zCDP），隐私界可能仍有收紧空间。
- 理论分析假设数据经过裁剪，裁剪参数 $C$ 的选择直接影响隐私-效用权衡，但文中未提供 $C$ 的自适应选择策略。

**定理 5.2** 在高斯混合模型（GMM）上证明了协作训练能显著降低 2-Wasserstein 距离：

$$\mathbb{E}_{\tilde{D},D_{m}} \Big[ W_{2}^{2} \big( q ; p_{\tilde{D},D_{m}}^{m} \big) \mid y = k \Big] = O \bigg( \frac{2}{2 + 3\sigma^{2}} \cdot \frac{d^{2}}{N_{k}} + \frac{3\sigma^{2}}{2 + 3\sigma^{2}} \cdot \frac{d^{2}}{n_{k}^{m}} \bigg)$$

该上界表明，当全局样本量 $N_k$ 远大于本地样本量 $n_k^m$ 时，第一项主导误差的降低，协作优势显著。但该分析局限于 GMM 和特定的分段线性去噪网络参数化：

$$\epsilon_{\theta}(x, y) = \sum_{k=1}^{K} \mathbf{1}_{y=k} \left[ W^{k} x + V^{k} c(y) \right]$$

尚未推广到更一般的扩散模型架构（如基于 UNet 的深度去噪器），这是理论上的主要开放问题。

### 4. 开放问题与未来方向

1. **理论扩展**：如何将效用分析从高斯混合模型推广到更广泛的扩散模型类别？能否为非参数或深度去噪器建立类似的收敛保证？

2. **隐私-效用边界**：能否在不显著牺牲效用的情况下实现更强的隐私保护（如 $\varepsilon < 1$）？更先进的差分隐私记账技术（如基于采样的隐私放大）是否能收紧隐私界？

3. **高分辨率扩展**：当前方法在 CelebA 64×64 上有效，但扩展到 256×256 或更高分辨率时，加噪数据集的传输开销和全局模型的训练成本将急剧增加。潜在方案包括潜空间扩散模型或分层联邦聚合。

4. **鲁棒性保障**：在存在恶意客户端（如投毒攻击、搭便车攻击）时，如何保证方法的鲁棒性和隐私性？可能需要引入拜占庭容错聚合机制或客户端信誉系统。

5. **标签隐私**：当前方法假设标签公开，如何扩展到标签也需保护的场景？一种可能方向是将条件生成扩展为无条件的隐私保护联邦扩散训练。

6. **与其他隐私技术的结合**：本方法可与安全多方计算、同态加密等技术结合，在服务器端对加噪数据进行更安全的聚合训练，进一步降低信息泄露风险。



## 原文 PDF

![[paperPDFs/CVPR_2026/Personalized_Federated_Training_of_Diffusion_Models_with_Privacy_Guarantees.pdf]]
