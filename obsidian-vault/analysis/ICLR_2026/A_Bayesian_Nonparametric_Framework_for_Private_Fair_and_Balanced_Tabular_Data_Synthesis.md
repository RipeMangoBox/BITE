---
title: "A Bayesian Nonparametric Framework for Private, Fair, and Balanced Tabular Data Synthesis"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/A_Bayesian_Nonparametric_Framework_for_Private_Fair_and_Balanced_Tabular_Data_Synthesis.pdf
project_link: null
code_link: null
aliases:
- CVCBNV
- BNFPFBTDS
tags:
- ICLR_2026
- topic/safety_alignment_fairness_privacy
- topic/safety_alignment_fairness_privacy/privacy_preserving_statistics_and_machine_learning
core_operator: "Dirichlet过程（DirP）的超参数 a 和互信息（MI）正则化系数 λ_F、类别平衡系数 λ_B。a 控制全局隐私预算与局部隐私的权衡；λ_F 控制生成结果与敏感属性之间的依赖程度；λ_B 控制非敏感分类属性的均匀程度。"
primary_logic: "利用贝叶斯非参数学习（BNPL）中的Dirichlet过程后验采样，将隐私噪声结构化地注入到重采样权重中（全局隐私），同时通过copula基测度对每个连续/离散列施加局部差分隐私；在此基础上，通过条件生成器最小化生成结果与敏感属性之间的互信息（DirPMINE）来实现公平性，并通过Dirichlet过程加权的KL散度（DirPKL）来实现类别平衡。三者统一在一个生成器-解码器框架（VAECGAN）中。"
claims:
- "Dirichlet过程权重满足 (ε, δ)-差分隐私，且当 a → ∞ 时达到完美隐私。"
- "所提方法在Adult数据集上，在公平性（MI和SP）和保真度（MMD）方面优于DECAF等基线方法。"
- "在COMPAS数据集上，当 λ_F=1 时，不同种族群体的条件概率 Pr(Y|S) 几乎相等，MI降至接近0。"
- "成员推断攻击的AUC值随 a 增大趋近0.5，表明隐私保护增强。"
---

# A Bayesian Nonparametric Framework for Private, Fair, and Balanced Tabular Data Synthesis

> [!tip] 核心洞察
> 利用贝叶斯非参数学习（BNPL）中的Dirichlet过程后验采样，将隐私噪声结构化地注入到重采样权重中（全局隐私），同时通过copula基测度对每个连续/离散列施加局部差分隐私；在此基础上，通过条件生成器最小化生成结果与敏感属性之间的互信息（DirPMINE）来实现公平性，并通过Dirichlet过程加权的KL散度（DirPKL）来实现类别平衡。三者统一在一个生成器-解码器框架（VAECGAN）中。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 面向隐私、公平与平衡的表格数据合成的贝叶斯非参数框架 |
| 英文题名 | A Bayesian Nonparametric Framework for Private, Fair, and Balanced Tabular Data Synthesis |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=j0czDrEnFc) |
| Topic | #topic/safety_alignment_fairness_privacy #topic/safety_alignment_fairness_privacy/privacy_preserving_statistics_and_machine_learning |
| Method | CBNP-VAECGAN (Conditional Bayesian Nonparametric VAECGAN) |
| Dataset | Adult, COMPAS |

> [!tip] 效果简介
> - Adult 上，MI (Mutual Information) 为 ≈0.0 (λ_F=1)，对比 0.0256 (True)，变化 降至接近0。
> - Adult 上，SP (Statistical Parity) 为 ≈0.0 (λ_F=1)，对比 0.198 (True)，变化 降至接近0。
> - COMPAS 上，MI 为 ≈0.0 (λ_F=1)，对比 0.0259 (True)，变化 降至接近0。

## 概要

该论文（CBNP-VAECGAN，ICLR 2026）针对表格数据合成中隐私保护、公平性与类别平衡三个相互冲突的目标，提出一个统一的贝叶斯非参数框架。核心瓶颈在于：在数据稀缺环境下，差分隐私噪声会扭曲少数群体的统计估计，而公平性约束又进一步限制了受噪声影响的优化过程，两者相互加剧，导致现有方法无法同时满足三个约束。

**核心方法**：利用Dirichlet过程（DirP）后验采样将隐私噪声结构化地注入到重采样权重中（全局隐私），同时通过copula基测度对每个连续/离散列施加局部差分隐私（AGM+RRM）。在此基础上，通过条件生成器最小化生成结果与敏感属性之间的互信息（DirPMINE）来实现公平性，并通过Dirichlet过程加权的KL散度（DirPKL）来实现类别平衡。三者统一在一个VAE+条件GAN（VAECGAN）的生成器-解码器框架中。关键超参数包括：DirP的超参数 $a$（控制全局隐私预算）、互信息正则化系数 $\lambda_F$（控制公平性强度）、类别平衡系数 $\lambda_B$。

**主要结果**：
- **隐私保证**：Dirichlet过程权重满足 $(\epsilon, \delta)$-差分隐私（Proposition 1），且当 $a \to \infty$ 时达到完美隐私（Corollary 1）。成员推断攻击的AUC值随 $a$ 增大趋近0.5（Figure 6），表明隐私保护增强。
- **公平性**：在Adult数据集上，$\lambda_F=1$ 时互信息（MI）和统计均等（SP）均降至接近0（Figure 3），优于DECAF等基线；在COMPAS数据集上，不同种族群体的条件概率 $\Pr(Y|S)$ 几乎相等（Table 1），MI降至接近0（Table 2）。
- **类别平衡**：在Adult数据集上，$\lambda_B=1$ 时非敏感分类属性的分布趋于均匀（Figure 4）。
- **理论保证**：Theorem 2在温和正则条件下证明了效用、公平性和类别平衡的联合一致性。

**局限性**：公平性定义仅限于统计均等（Statistical Parity），不支持基于分类器的公平性概念（如均等化赔率、机会均等）或条件统计均等；理论保证依赖于“良好设定”假设（所有目标差异为零），实际中可能不严格成立；实验仅在表格数据上进行，未验证在图像或文本等非结构化数据上的适用性。



合成表格数据生成在隐私保护、公平性与类别平衡三个维度上面临着相互加剧的瓶颈。现有方法通常仅解决其中一两个约束，且当三者同时施加时，隐私噪声会扭曲少数群体的统计估计，而公平性约束又进一步限制了受噪声影响的优化过程，导致两者相互恶化。具体而言：

- **隐私机制**：标准高斯机制（CGM）或DP-SGD在数据稀缺环境下对少数群体引入的噪声比例更高，使得下游公平性优化难以收敛。
- **公平性约束**：基于GAN的对抗性公平性（如TabFairGAN）无法处理非二元敏感属性，且与差分隐私机制缺乏协同设计。
- **类别平衡**：过采样（SMOTE）或线性插值方法无法与隐私和公平性约束联合优化，往往在保护隐私后加剧类别不平衡。

本文的动机在于设计一个**统一的贝叶斯非参数框架**，使隐私、公平与类别平衡三个约束在生成过程中相互协同而非对抗。核心洞察是：利用Dirichlet过程（DirP）的后验采样结构，将隐私噪声**结构化地注入**到重采样权重中（全局隐私），同时通过copula基测度对每个连续/离散列施加局部差分隐私；在此基础上，通过条件生成器最小化生成结果与敏感属性之间的互信息（DirPMINE）来实现公平性，并通过Dirichlet过程加权的KL散度（DirPKL）来实现类别平衡。三者统一在一个生成器-解码器框架（VAECGAN）中。

**因果机制**：该方法通过三个可控的超参数调节约束间的权衡——DirP的超参数 $a$ 控制全局隐私预算与局部隐私的权衡（$a \to \infty$ 时达到完美隐私，但效用降低）；互信息正则化系数 $\lambda_F$ 控制生成结果与敏感属性之间的依赖程度（$\lambda_F=1$ 时MI降至接近0）；类别平衡系数 $\lambda_B$ 控制非敏感分类属性的均匀程度。实验证据表明，更高的隐私（更大的 $a$）不会阻止公平性，但会减慢公平性优化的收敛速度（Figure 9），且仅使用类别平衡（$\lambda_B=1, \lambda_F=0$）不会改变生成数据中的不公平性（Figure 10(a)）。

**证据强度**：定理2在温和正则条件下证明了效用、公平性和类别平衡的联合一致性（置信度0.95），但该保证依赖于“良好设定”假设（所有目标差异为零），实际中可能不严格成立。消融实验（Figures 9-10）和成员推断攻击（Figure 6）提供了实证支持，但隐私与公平性之间的精确权衡关系仍需进一步理论刻画。



## 核心方法与创新机理

CBNP-VAECGAN 的核心创新在于将隐私、公平和类别平衡三个相互冲突的目标统一在一个贝叶斯非参数框架中，通过 **Dirichlet 过程 (DirP)** 作为连接三者的因果旋钮。与现有方法（如 DECAF、TabFairGAN、PF-WGAN）相比，该方法在四个关键槽位（changed slots）上做出了根本性改变：

**1. 隐私机制：从标准高斯机制到双层 Dirichlet 过程隐私**

基线方法（如 DP-SGD、CGM）通常将噪声直接注入梯度或数据。CBNP-VAECGAN 则采用双层结构：
- **全局隐私**：通过后验 Dirichlet 过程的有限近似（公式 3），从 $DP(a+n, H^*)$ 中采样重采样权重。这些权重本身满足 $(\epsilon, \delta)$-差分隐私（Proposition 1），且当浓度参数 $a \to \infty$ 时达到完美隐私（Corollary 1）。其核心机制是将隐私噪声结构化地注入到重采样权重中，而非直接扰动数据。
- **局部隐私**：通过 copula 基测度 $H^{\text{Pert}}$ 实现，对连续列使用 **加法高斯机制 (AGM)**，对离散列使用 **随机响应机制 (RRM)**，并通过高斯 copula 保持列间的依赖结构（Section 4.3）。

**2. 公平性约束：从对抗性公平到互信息最小化**

基线方法（如 TabFairGAN、DECAF）通常依赖 GAN 的对抗训练或分类器来强制公平性，难以处理非二元敏感属性。CBNP-VAECGAN 提出了 **DirPMINE**（Definition 1），通过 Dirichlet 过程加权的 Donsker-Varadhan 下界来近似生成结果 $\tilde{\mathbf{Y}}$ 与敏感属性 $\dot{\mathbf{S}}$ 之间的互信息，并将其作为正则项 $\lambda_F \mathcal{L}_{\text{Fair}}(G_\omega)$ 加入总损失。这使得公平性定义（统计均等，公式 1-2）可以直接通过优化互信息为零来实现，且自然地支持非二元敏感属性。

**3. 类别平衡：从过采样到 Dirichlet 过程 KL 散度正则化**

基线方法（如 SMOTE）通常通过数据层面的过采样或线性插值来处理类别不平衡。CBNP-VAECGAN 提出了 **DirPKL**，在生成分布上直接施加 KL 散度正则化，通过 Dirichlet 过程加权的 KL 估计器控制非敏感分类属性的均匀程度（Section 4.4.3, Eq. 9）。这使得平衡约束与生成过程一体化，而非独立的预处理步骤。

**4. 生成模型架构：从纯 GAN/VAE 到 VAECGAN 混合架构**

基线方法要么使用纯 GAN（如 CTGAN）要么使用纯 VAE（如 OVAE）。CBNP-VAECGAN 结合了两者：VAE 编码器 $E_\eta$ 和代码生成器 $CG_\tau$ 负责学习稳定的潜在表示，而条件生成器 $G_\omega$ 与判别器 $D_\theta$ 通过对抗训练提升生成质量。这种混合架构使得模型既能利用 VAE 的稳定性又能利用 GAN 的高保真度。

**核心因果机制**：Dirichlet 过程的超参数 $a$ 同时控制隐私预算和重采样权重的集中度，而互信息系数 $\lambda_F$ 和类别平衡系数 $\lambda_B$ 则分别控制公平性和平衡性的强度。三者通过统一的损失函数（Eq. 9）联合优化，使得隐私噪声不会独立地扭曲少数群体估计，而是通过 Dirichlet 过程的结构化注入来缓解隐私与公平之间的冲突。实验证据表明（Fig. 3, Table 2），在 Adult 和 COMPAS 数据集上，当 $\lambda_F=1$ 时，互信息（MI）和统计均等（SP）均降至接近 0，同时保真度（MMD、F1-score）与真实数据持平。成员推断攻击实验（Figure 6）显示，随着 $a$ 增大，AUC 趋近 0.5，证实了隐私保护的有效性。

**值得注意的局限**：公平性定义仅限于统计均等（Statistical Parity），不支持均等化赔率或机会均等等需要真实标签条件的公平性概念。理论保证（Theorem 2）依赖于“良好设定”假设，实际中可能不严格成立。



![[assets/figures/papers/iclr26_0001_j0czDrEnFc_A_Bayesian_Nonparametric_Framework_for_Private_F/figures/075_Figure_20.jpg]]
*Figure 20: Overview of the triple policies (Fair–Private–Balanced) enforced by our proposed approach to address potential attacks*

CBNP-VAECGAN 是一个在贝叶斯非参数学习（BNPL）框架下，通过单一生成器-解码器架构（VAECGAN）统一处理隐私、公平性和类别平衡三重约束的表格数据合成系统。其整体 pipeline 由三个层次构成：数据扰动层、生成建模层和约束优化层。

**数据扰动层** 执行双层隐私注入。首先，全局隐私通过 Dirichlet 过程（DirP）后验采样实现：从 DP(a+n, H*) 中采样重采样权重，这些权重本身满足 (ε, δ)-差分隐私（Proposition 1），且当超参数 a → ∞ 时达到完美隐私（Corollary 1）。其次，局部隐私通过 copula 基测度 H^Pert 注入：对连续列使用高斯机制（AGM），对离散列使用随机响应（RRM），再通过高斯 copula 保持属性间的依赖结构（Section 4.3, Algorithm 1）。该层输出带隐私保护的“后验”数据集，作为下游生成模块的输入。

**生成建模层** 采用 VAECGAN 架构，包含四个核心模块：编码器 E_η 将输入数据映射到潜在编码 c；代码生成器 CG_ω' 从噪声 ξ' 生成潜在编码 c̃；生成器 G_ω 以潜在编码 ℓ 和敏感属性 s 为条件生成合成数据；判别器 D_θ 区分真实数据和生成数据，驱动对抗训练（Algorithm 2, lines 7-10）。该架构结合了 VAE 的稳定编码能力和 GAN 的高保真生成能力，同时通过条件生成机制显式控制敏感属性的影响。

**约束优化层** 通过 DirPDV 网络 T_ν 同时估计两个正则化项：DirPMINE 用于估计生成结果与敏感属性之间的互信息（Section 4.4.2, Definition 1），DirPKL 用于估计非敏感分类属性的 KL 散度（Section 4.4.3）。总损失函数为 `L_Utility + λ_F L_Fair + Σ λ_B L_Balance`（Eq. 9），其中 L_Utility 包含生成器-编码器、判别器和代码生成器的对抗损失，λ_F 和 λ_B 分别控制公平性和类别平衡的强度。该方法的核心洞察在于：通过 Dirichlet 过程的后验权重将隐私噪声结构化地注入到重采样过程中，使得隐私机制与后续的公平性/平衡性优化在同一个概率框架下协同工作，避免了传统方法中隐私噪声与公平性约束相互加剧的问题。



CBNP-VAECGAN框架的核心在于通过贝叶斯非参数学习（BNPL）中的Dirichlet过程（DirP）将隐私、公平和类别平衡三个约束统一在一个生成器-解码器架构中。其关键模块和公式如下。

### 1. 隐私机制：双层隐私注入

隐私保护通过全局和局部两个层次实现。

**全局隐私** 基于后验Dirichlet过程的有限近似。给定原始数据集 $\mathscr{D}_{1:N}$，后验DirP的有限近似为：
$$F_{\pmb{\mathscr{D}}_{1:N}^{\mathrm{pos}}}^{\mathrm{pos}}(\cdot):=\sum_{i=1}^{N}J_{i,N^{-1}}^{(a+n)}\mathbb{I}_{\pmb{\mathscr{D}}_i^{\mathrm{pos}}}(\cdot)$$
其中权重向量 $(J_{1,N^{-1}}^{(a+n)}, \dots, J_{N,N^{-1}}^{(a+n)})$ 服从参数为 $(a+n)$ 和均匀权重的Dirichlet分布。该过程本质上是一个Dirichlet机制（Definition 2），其输出概率密度为：
$$\operatorname{Pr}[\mathcal{M}_{\mathrm{DirP}}^{(a+n)}(p_{1:N}; \epsilon_{\mathrm{glo}}, \delta_{\mathrm{glo}}) = x_{1:N}] = \frac{1}{B((a+n)p_{1:N})} \prod_{i=1}^{N-1} x_i^{(a+n)p_i - 1} (1 - \sum_{i=1}^{N-1} x_i)^{(a+n)p_N - 1}$$
其中 $B((a+n)p_{1:N})$ 是多变量Beta函数。**Proposition 1** 证明该机制满足 $(\epsilon_{\mathrm{glo}}, \delta_{\mathrm{glo}})$-差分隐私，且 **Corollary 1** 指出当 $a \to \infty$ 时达到完美隐私（$\epsilon_{\mathrm{glo}} = 0$）。超参数 $a$ 是控制全局隐私预算的关键旋钮：$a$ 越小，隐私保护越强，但统计效用损失越大。

**局部隐私** 通过构建基于copula的扰动基测度 $H^{\mathrm{Pert}}$ 实现：
$$H^{\mathrm{Pert}}(\mathbf{t}) = C_{\hat{R}}(F_{\mathrm{AGM},1}(t_1), \dots, F_{\mathrm{AGM},N_{\mathrm{C}}}(t_{N_{\mathrm{C}}}), F_{\mathrm{RRM},1}(t_{N_{\mathrm{C}}+1}), \dots, F_{\mathrm{RRM},N_{\mathrm{D}}}(t_d))$$
该测度对 $N_{\mathrm{C}}$ 个连续列使用高斯机制（AGM）进行扰动，对 $N_{\mathrm{D}}$ 个离散列使用随机响应机制（RRM），并通过高斯copula $C_{\hat{R}}$ 保持原始属性间的依赖结构。RRM的扰动概率为：
$$\operatorname{Pr}(\mathcal{M}_{\mathrm{RRM}}(X;\epsilon)=x)=\begin{cases} \frac{e^{\epsilon}}{e^{\epsilon}+K-1} & \text{if } x \text{ is the true value of } X, \\ \frac{1}{e^{\epsilon}+K-1} & \text{otherwise.} \end{cases}$$
**Remark 2** 指出，全局与局部隐私的组合满足 $(\epsilon, \delta + \delta_{\mathrm{glo}} + \delta_{\mathrm{loc}})$-差分隐私。

### 2. 公平性约束：Dirichlet过程互信息估计（DirPMINE）

公平性基于统计均等（Statistical Parity）定义，要求：
$$\operatorname*{Pr}(Y=1\mid S=0)=\operatorname*{Pr}(Y=1\mid S=1)$$
该条件等价于结果 $Y$ 与敏感属性 $S$ 之间的互信息为零：
$$\mathrm{MI}(Y,S)=\mathrm{D}_{\mathrm{KL}}(F_{Y,S},F_Y\otimes F_S)=H(Y)-H(Y\mid S)=0$$

为了在生成过程中最小化MI，论文提出 **DirPMINE**（Definition 1），利用Dirichlet过程加权的Donsker-Varadhan（DV）下界来近似互信息：
$$\frac{\mathcal{L}_{\mathrm{Fair}}(G_\omega)}{\mathrm{MI}^{\mathrm{DirPDV}}(\tilde{\mathbf{Y}}_{1:N}^{\mathrm{Pos}}, \dot{\mathbf{S}}_{1:N}^{\mathrm{Pos}})} = \max_{v \in \mathbf{T}} \left\{ \sum_{r=1}^N J_{r,N^{-1}}^{(a+n)} T_v(\tilde{\mathbf{Y}}_r^{\mathrm{Pos}}, \dot{\mathbf{S}}_r^{\mathrm{Pos}}) - \ln \sum_{r=1}^N J_{r,N^{-1}}^{(a+n)} e^{T_v(\tilde{\mathbf{Y}}_r^{\mathrm{Ro}}, \dot{\mathbf{S}}_{\pi(r)}^{\mathrm{Ro}})} \right\}$$
其中 $T_v$ 是一个神经网络（DirPDV网络），$J_{r,N^{-1}}^{(a+n)}$ 是来自后验DirP的权重，$\pi(r)$ 是随机排列索引。该公式通过最大化DV下界来逼近MI，并将其作为生成器的正则化项 $\lambda_F \mathcal{L}_{\mathrm{Fair}}(G_\omega)$ 加入到总损失中。超参数 $\lambda_F$ 控制公平性的强度：$\lambda_F=0$ 时不施加公平性，$\lambda_F=1$ 时MI降至接近0。

### 3. 类别平衡约束：Dirichlet过程KL散度（DirPKL）

类别平衡通过最小化生成分布与均匀分布之间的KL散度来实现。论文使用类似的Dirichlet过程加权方法（DirPKL）来估计KL散度，并将其作为正则化项 $\sum_{i_D=1}^{N_D-2} \lambda_{B_{i_D}} \mathcal{L}_{\mathrm{Balance}_{i_D}}(G_\omega)$ 加入总损失。超参数 $\lambda_B$ 控制类别平衡的强度。

### 4. 总损失函数

整个框架的训练目标是将效用、公平性和类别平衡统一在一个损失函数中：
$$\mathcal{L}_{\mathrm{Utility}}(G_\omega, E_\eta, D_\theta, CG_\tau) + \lambda_F \mathcal{L}_{\mathrm{Fair}}(G_\omega) + \sum_{i_D=1}^{N_D-2} \lambda_{B_{i_D}} \mathcal{L}_{\mathrm{Balance}_{i_D}}(G_\omega)$$
其中效用损失 $\mathcal{L}_{\mathrm{Utility}}$ 包含编码器-生成器损失、判别器损失和代码生成器损失，采用VAECGAN架构实现。**定理2** 在温和正则条件下证明了该联合框架的一致性：随着样本量增加，效用、公平性和类别平衡同时得到改善。

### 5. 关键超参数与变量含义

| 符号 | 含义 | 作用 |
|------|------|------|
| $a$ | Dirichlet过程的浓度参数 | 控制全局隐私预算，$a \to \infty$ 时隐私消失 |
| $\lambda_F$ | 公平性正则化系数 | 控制生成结果与敏感属性之间的依赖程度 |
| $\lambda_B$ | 类别平衡正则化系数 | 控制非敏感分类属性的均匀程度 |
| $J_{i,N^{-1}}^{(a+n)}$ | 后验Dirichlet过程权重 | 对重采样数据点进行加权，注入全局隐私 |
| $T_v$ | DirPDV网络 | 估计互信息和KL散度的神经网络 |
| $H^{\mathrm{Pert}}$ | 基于copula的扰动基测度 | 注入局部隐私并保持属性间依赖结构 |



## 实验与关键发现

### 主结果：公平性与保真度

CBNP-VAECGAN 在三个基准数据集（Adult、COMPAS、Bank Marketing）上同时评估了生成数据的公平性、保真度和隐私性。公平性通过生成结果 Y 与敏感属性 S 之间的互信息（MI）量化，保真度通过 F1 分数和准确率衡量。

**Adult 数据集**是核心对比场景。图 3 展示了在隐私参数 a=5、λ_F=1（最大公平性约束）下，CBNP-VAECGAN 将 MI 从真实数据的 0.0256 降至接近 0，同时将统计均等（SP）从真实数据的 0.198 降至接近 0。相比之下，DECAF 等基线方法在公平性指标上显著落后，其生成数据的 MI 和 SP 仍明显偏离零。这一结果验证了 DirPMINE 正则化项能有效消除 Y 与 S 之间的依赖关系——不仅直接依赖，还包括通过混杂变量产生的间接相关。

**COMPAS 数据集**上，表 2 给出了定量结果：真实数据的 MI(Y,S)=0.0259，F1=0.913，准确率=0.901。当 λ_F=1 时，生成数据的 MI 降至接近 0，而 F1 和准确率几乎不受影响（与真实数据持平）。表 1 进一步展示了条件概率 Pr(Y|S) 在不同种族群体间的分布：无公平性政策时，非裔美国人群体获得高风险评分的概率远高于其他群体；施加 λ_F=1 后，各群体的条件概率几乎完全相等。这表明公平性机制在消除群体间差异方面是有效的。


![[assets/figures/papers/iclr26_0001_j0czDrEnFc_A_Bayesian_Nonparametric_Framework_for_Private_F/figures/009_Table_1.jpg]]
*Table 1: Pr(Y = “Score Text” | $\mathbf { S } = ^ { 6 4 } \mathbf { E t h m i c } ^ { 3 9 }$ ) for the generated samples. As shown in red, the generated data exhibits disparities in score text across ethnic groups without a fairness policy. For instance, African-Americans are classified as “High” risk with probability 0.146, compared to only 0.058 for Asians. These probabilities become nearly equal in the blue portions

![[assets/figures/papers/iclr26_0001_j0czDrEnFc_A_Bayesian_Nonparametric_Framework_for_Private_F/figures/010_Table_2.jpg]]
*Table 2: COMPAS: $\mathbf { M } _ { \mathrm { T r u e } } ( \mathbf { Y } , \mathbf { S }$ ) = 0.0259, $\mathrm { F 1 } _ { \mathrm { T r u e } }$ = 0.913, and $\operatorname { A c c } _ { \operatorname { T r u e } }$ = 0.901 over 10 runs

**Bank Marketing 数据集**（表 17）进一步验证了方法的泛化能力。真实数据的 MI(Y,S)=0.0264，F1=0.540，准确率=0.884。当 λ_F=1 时，生成数据的 MI 降至 1e-5，同时 F1 提升至 0.851-0.858，准确率保持在 0.884 附近。F1 的显著提升（从 0.540 到 0.851）表明，公平性约束不仅没有损害效用，反而通过消除敏感属性（联系月份）引入的噪声，提高了分类器的预测性能。这是一个值得注意的副效应：当敏感属性与结果之间存在虚假相关时，强制公平性可以迫使模型学习更稳健的特征。

### 隐私保护与隐私-公平-效用权衡

隐私保护通过两个层次实现：全局隐私（Dirichlet 过程重采样权重）和局部隐私（copula 基测度中的 AGM+RRM）。图 2 展示了不同隐私预算下的效用权衡。

图 2a 表明，当全局隐私参数 a 较小时（如 a=10^-6），即使局部隐私预算很强，效用仍然保持良好。这是因为小 a 对应较强的隐私注入，但 Dirichlet 过程的后验采样仍能保留数据的整体分布结构。随着 a 增大（如 a=100），隐私保护减弱，但效用提升有限——这揭示了隐私-效用的边际递减效应。

图 2b 显示，在高全局隐私（a=100）下，增加更多受隐私保护的属性会导致准确率和 F1 下降。这是因为每个额外属性都引入了局部隐私噪声，累积效应扭曲了生成分布。这一发现对实际部署有指导意义：应仅对必要的敏感列施加局部隐私，而非对所有列无差别处理。

**成员推断攻击**（图 6）验证了隐私保护的有效性。随着 a 增大，攻击者 AUC 趋近 0.5（随机猜测水平）。当 a=10^-6 时，AUC 接近 0.5，表明强隐私保护下攻击者无法区分成员与非成员。当 a=1300 时，AUC 上升至约 0.7，表明隐私保护减弱。图 7 的预测置信度直方图进一步展示了这一趋势：小 a 下成员与非成员的置信度分布几乎重合，大 a 下两者分离。

### 消融实验与机制隔离

消融实验揭示了三个正则化项的独立作用和交互效应。

**公平性与类别平衡的隔离影响**（图 10）：仅使用类别平衡（λ_B=1, λ_F=0）不会改变生成数据中的不公平性——MI 和 SP 与无约束时相似。这表明类别平衡不能替代公平性约束，因为它只调整非敏感属性的边际分布，不影响 Y 与 S 的依赖关系。仅使用公平性约束（λ_F=1, λ_B=0）能有效消除 MI 和 SP，但可能导致某些非敏感类别出现不平衡。两者联合使用时，公平性和平衡性同时得到满足。

**隐私对公平性优化的影响**（图 9）：更高的隐私（更大的 a）不会阻止公平性约束的最终收敛，但会减慢收敛速度。具体而言，当 a=10^-6（强隐私）时，MI 需要更多训练轮次才能降至接近 0；当 a=1300（弱隐私）时，MI 快速收敛。这一发现揭示了隐私与公平性之间的非竞争性但非独立关系：隐私噪声干扰了 DirPMINE 估计器的梯度信号，从而减慢了公平性优化的速度。实际应用中，需要根据隐私预算调整训练轮次以确保公平性收敛。

**MNIST 极端测试**（图 11-12）：在 MNIST 上构造了敏感属性 S 与标签 Y 之间存在完美依赖的场景。无公平性机制（λ_F=0）时，生成器完全复制了这种依赖；施加公平性机制（λ_F=1）后，生成图像在不同 S 条件下均匀分布，完全消除了依赖。这证明了方法在极端条件下的鲁棒性。

### 一致性验证

图 16 展示了随着样本量增加，效用（MMD）、公平性（MI）和平衡性（KL 散度）均得到改善。这一趋势验证了定理 2 的预测：在温和正则条件下，三个目标具有联合一致性。当样本量从 1000 增至 10000 时，MMD 下降约 50%，MI 下降至接近 0，KL 散度也显著降低。这表明方法在大样本下能同时逼近真实分布、公平性和平衡性目标。

### 失败模式与局限性

1. **公平性定义的局限**：方法仅支持统计均等（Statistical Parity），不支持均等化赔率（Equalized Odds）或机会均等（Equal Opportunity）。这是因为后者需要条件互信息估计器，当前框架未实现。在需要条件公平性的场景（如医疗诊断中不同人口组应保持相同的假阳性率）中，该方法不适用。

2. **理论保证的弱假设**：定理 2 的联合一致性依赖于“良好设定”假设——所有目标差异（效用、公平性、平衡性）在真实分布下为零。实际中，真实数据本身可能就不满足完美公平性或平衡性，此时理论保证不严格成立。实验中的 MI 降至接近 0 而非严格 0 也反映了这一点。

3. **隐私-公平性权衡的机制未完全解释**：高隐私下公平性收敛变慢的现象已被观察到，但其精确机制（隐私噪声如何通过 DirPMINE 梯度传播影响公平性优化）尚未被理论刻画。这需要进一步的梯度分析或信息论解释。

4. **仅适用于表格数据**：方法依赖 copula 基测度和类别变量的显式处理，未验证在图像、文本等非结构化数据上的适用性。将 Dirichlet 过程隐私机制扩展到 Transformer 或 CNN 架构需要重新设计隐私注入点。

5. **全局隐私预算的复杂性**：Proposition 1 给出的全局隐私预算表达式（涉及多个超参数 η, η̄, γ, b）在实际使用中需要近似或数值计算，增加了部署难度。

### 补充图表

![[assets/figures/papers/iclr26_0001_j0czDrEnFc_A_Bayesian_Nonparametric_Framework_for_Private_F/figures/011_Table_3.jpg]]

![[assets/figures/papers/iclr26_0001_j0czDrEnFc_A_Bayesian_Nonparametric_Framework_for_Private_F/figures/012_Table_4.jpg]]

![[assets/figures/papers/iclr26_0001_j0czDrEnFc_A_Bayesian_Nonparametric_Framework_for_Private_F/figures/013_Table_5.jpg]]




## 定位与知识库关联

### 与基线方法的对比

CBNP-VAECGAN在现有表格数据生成方法的基础上，通过贝叶斯非参数学习（BNPL）的Dirichlet过程（DirP）统一了隐私、公平性和类别平衡三个目标。与基线方法的本质区别体现在三个核心机制上：

- **隐私机制**：基线方法（如PF-WGAN、PreFair）依赖标准高斯机制（CGM）或DP-SGD，而CBNP-VAECGAN采用双层隐私结构——全局隐私通过Dirichlet过程后验采样注入（Proposition 1），局部隐私通过copula基测度对连续列使用AGM、对离散列使用RRM。这一设计的因果逻辑在于：隐私噪声被结构化地注入到重采样权重中，避免了直接扰动生成过程的梯度，从而减少对后续公平性优化的干扰。

- **公平性约束**：TabFairGAN、FairGAN等基于GAN的对抗性公平性方法无法处理非二元敏感属性；DECAF作为最先进的公平性基线，但其公平性机制与隐私机制独立运作。CBNP-VAECGAN通过DirPMINE（互信息估计器）将公平性形式化为生成结果与敏感属性之间的互信息最小化，支持非二元敏感属性（如种族、关系状态）。关键洞察在于：互信息归零等价于统计均等（Statistical Parity），而DirPMINE利用Dirichlet过程权重对DV下界进行加权，使其自然地与隐私框架兼容。

- **类别平衡**：基线方法（如SMOTE）采用过采样或线性插值，可能改变数据分布。CBNP-VAECGAN通过DirPKL（KL散度正则化）直接控制生成分布中非敏感分类属性的均匀程度，与公平性约束共享相同的Dirichlet过程加权结构。

### 适用边界与条件

该方法在以下条件下表现最佳：
1. **敏感属性为离散变量**：公平性约束基于互信息，自然适用于类别型敏感属性。对于连续敏感属性，需要额外的离散化步骤。
2. **统计均等作为公平性概念**：该方法不支持基于分类器的公平性概念（如均等化赔率、机会均等），因为这些概念需要真实标签条件，而生成场景中标签本身也是生成目标。
3. **隐私预算适中**：实验表明，当全局隐私参数 `a` 较小时（高隐私），公平性优化的收敛速度会减慢，但不会阻止公平性的最终达成（Figure 9）。当 `a → ∞` 时，达到完美隐私（Corollary 1），但生成数据的效用下降。
4. **样本量充足**：定理2的理论一致性保证依赖于样本量增加（Figure 16验证了这一点），在小样本场景下的可靠性需谨慎评估。

### 已知局限

1. **公平性定义范围有限**：仅支持统计均等，不支持条件统计均等（Conditional Statistical Parity），因为后者需要条件互信息估计器，超出了当前工作范围。
2. **理论保证的假设强度**：定理2（一致性）依赖于“良好设定”假设（所有目标差异为零），实际中可能不严格成立。实验验证（Figure 16）仅展示了趋势而非严格收敛。
3. **隐私分析的复杂性**：全局隐私预算表达式（Proposition 1的推导）涉及多个参数（`η, η̄, γ, b`），实际使用中需要近似或数值计算。
4. **数据模态限制**：方法仅在表格数据上验证，未测试在图像或文本等非结构化数据上的适用性。MNIST实验仅用于验证公平性机制的有效性，而非完整框架。

### 开放问题

1. **公平性概念的扩展**：如何通过条件DirPMINE估计器支持均等化赔率（Equalized Odds）等更细粒度的公平性概念？这需要估计 `Pr(Y|S, Y_true)`，在生成场景中面临标签不可知的问题。
2. **隐私-公平性权衡机制**：高隐私预算下公平性优化收敛变慢的精确机制是什么？是隐私噪声增加了互信息估计的方差，还是Dirichlet过程权重限制了优化步长？当前工作仅观测到现象（Figure 9），未给出理论解释。
3. **架构迁移**：如何将Dirichlet过程整合到自回归架构（如LLM）中？这需要解决序列生成中隐私预算分配和公平性约束的时序依赖问题。
4. **连续敏感属性**：该方法能否扩展到连续敏感属性（如年龄、收入）？需要构造连续版本的互信息估计器，同时保持差分隐私保证。



## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/A_Bayesian_Nonparametric_Framework_for_Private_Fair_and_Balanced_Tabular_Data_Synthesis.pdf

![[paperPDFs/ICLR_2026/A_Bayesian_Nonparametric_Framework_for_Private_Fair_and_Balanced_Tabular_Data_Synthesis.pdf]]
