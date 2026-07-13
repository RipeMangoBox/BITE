---
title: "Cross-Domain Lossy Compression via Rate- and Classification-Constrained Optimal Transport"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Cross_Domain_Lossy_Compression_via_Rate_and_Classification_Constrained_Optimal_Transport.pdf
project_link: null
code_link: null
openreview_forum_id: mUIGdUTtk2
aliases:
- RCCOTR
- CDLCRCCOT
tags:
- ICLR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/generative_models_and_autoencoders
core_operator: "引入独立于源信号的共享随机性（U），将编码和传输解耦为两步：先由 (X,U) 确定性生成 Y，再对 Y 进行无损压缩；同时通过约束 H(S|Y) 直接控制分类不确定性。"
primary_logic: "将跨域有损压缩形式化为约束最优传输问题，通过优化传输计划在维持目标边际分布 p_Y 的同时满足率、失真和分类约束，在伯努利和高斯信源下导出闭式权衡关系，揭示了率、失真与分类性能之间的明确三重边界。"
claims:
- "问题被形式化为带压缩率和分类损失约束的最优传输"
- "单次设定下，共享公共随机性使系统退化为确定性传输计划，编码与压缩解耦"
- "渐近情况下，DRC 和 DRPC 函数均具有单字母（single-letter）表征"
- "伯努利和高斯信源下导出闭式 DRC/RDC 表达式，且实验曲线与理论预测高度吻合"
---

# Cross-Domain Lossy Compression via Rate- and Classification-Constrained Optimal Transport

> [!tip] 核心洞察
> 将跨域有损压缩形式化为约束最优传输问题，通过优化传输计划在维持目标边际分布 p_Y 的同时满足率、失真和分类约束，在伯努利和高斯信源下导出闭式权衡关系，揭示了率、失真与分类性能之间的明确三重边界。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 基于率和分类约束最优传输的跨域有损压缩 |
| 英文题名 | Cross-Domain Lossy Compression via Rate- and Classification-Constrained Optimal Transport |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=mUIGdUTtk2) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/generative_models_and_autoencoders |
| Method | Rate- and Classification-Constrained Optimal Transport (RCOT) |
| Dataset | KODAK 高斯去噪 (σ=25) |

> [!tip] 效果简介
> - KODAK 高斯去噪 (σ=25) 上，LPIPS 为 0.1987，对比 0.2235 (BM3D)，变化 −0.0248。
> - KODAK 高斯去噪 (σ=25) 上，DISTS 为 0.1638，对比 0.1967 (DeCompress)，变化 −0.0329。
> - KODAK 高斯去噪 (σ=25) 上，PI 为 2.1670，对比 2.6503 (BM3D)，变化 −0.4833。

## 概要

经典率失真理论假设重建信号的分布与源分布一致，无法直接处理**跨域映射**与**下游分类约束**并存的场景。当输入为退化信号（如噪声图像、低分辨率图像）且重建目标分布不同于源分布时，传统压缩框架难以在重建保真度、压缩率和分类精度之间进行联合优化。

本文的核心贡献在于将跨域有损压缩形式化为**率和分类约束最优传输（Rate- and Classification-Constrained Optimal Transport, RCOT）**问题。其关键洞察是引入独立于源信号的**共享随机性 $U$**，将编码与压缩解耦为两步：先由 $(X,U)$ 确定性生成重建 $Y$，再对 $Y$ 进行无损压缩；同时通过约束条件熵 $H(S|Y) \le C$ 直接控制分类不确定性。这一形式化使得问题退化为在满足率、失真和分类三重约束下优化传输计划，从而维持目标边际分布 $p_Y$。

在理论上，本文为伯努利信源（汉明失真）和高斯信源（均方误差）导出了**闭式失真-率-分类（DRC）函数**，揭示了率、失真与分类性能之间的明确三重边界。渐近情况下，DRC 函数和加入感知散度约束的 DRPC 函数均具有**单字母（single-letter）表征**，由互信息 $I(X;Y)$ 和条件熵 $H(S|Y)$ 共同刻画。

实验层面，本文构建了一个包含随机编码器、通用量化、熵瓶颈、WGAN 判别器和分类头的端到端框架，在 MNIST 超分辨、SVHN/CIFAR-10/ImageNet/KODAK 去噪以及 SVHN 修复等任务上验证了理论预测。消融实验表明，分类约束强度 $\lambda_c$ 存在最优权衡区域——过弱则分类精度不足，过强则导致重建质量崩溃。在 KODAK 高斯去噪（$\sigma=25$）上，该方法在感知指标 LPIPS（0.1987）、DISTS（0.1638）和 PI（2.1670）上均优于 BM3D 和 DeCompress 等基线。闭合解与经验估计的高度吻合（Figure 17）进一步验证了理论框架的正确性。

**方法定位**：RCOT 在约束最优传输（如 Liu et al., 2022 的熵约束 OT）基础上增加了分类约束 $H(S|Y) \le C$，并将训练目标扩展为 MSE + 率项 + Wasserstein-1 感知损失 + 交叉熵分类损失的联合优化，从而在统一框架下同时处理跨域重建、压缩效率和下游任务性能。当前闭式解限于伯努利和高斯分布，推广到更一般分布以及大规模真实图像压缩中的高效训练仍是开放问题。



### 经典率失真理论的跨域局限

经典率失真理论为数据压缩提供了坚实的数学基础，其核心目标是在给定码率约束下最小化源信号与重建信号之间的失真。然而，这一理论框架隐含了一个关键假设：重建信号的分布与源信号的分布一致。在许多实际场景中，这一假设并不成立。例如，当输入是受噪声污染的退化图像时，期望的输出是干净的高质量图像，二者分属不同的分布域。这种**跨域映射**需求超出了经典率失真理论的建模能力。

更进一步的挑战在于，许多压缩系统并非以“人眼观看”为最终目的，而是为**下游机器任务**（如图像分类）服务。传统的压缩方法仅关注重建的保真度，忽略了重建结果对后续分类器性能的影响。这种“压缩-分类”分离的流水线可能导致压缩过程中丢失对分类至关重要的语义信息，即使重建质量在感知上可接受，分类精度也可能显著下降。

### 现有方法的缺口

当前解决上述问题的方法大致可分为两类，但均存在明显不足：

1. **基于最优传输的无监督恢复**：以 **Liu et al. 的熵约束最优传输框架**为代表，这类方法通过约束传输计划的互信息来实现压缩，能够有效对齐源分布与目标分布。然而，该框架仅包含率约束，**缺乏对下游分类性能的显式建模**，无法保证重建结果对分类任务有用。

2. **传统压缩与去噪基线**：如 **JPEG-2K** (Taubman et al., 2002)、**BM3D** (Dabov et al., 2007) 等经典方法，以及 **OTDenoising**、**DeCompress** 等基于最优传输或压缩的去噪框架。这些方法或仅追求重建保真度，或仅考虑无监督分布对齐，均未将分类约束纳入优化目标。

### 核心瓶颈与本文动机

上述缺口指向一个根本性的理论瓶颈：**如何在一个统一的数学框架内，同时处理跨域映射、压缩率约束和下游分类性能约束？** 这要求我们超越经典率失真理论和现有最优传输框架，寻找一种能够联合优化重建保真度、压缩效率和分类精度的新范式。

本文的核心动机正是填补这一空白。作者观察到，跨域有损压缩本质上可以形式化为一个**带约束的最优传输问题**：在源分布 $p_X$ 和目标分布 $p_Y$ 之间寻找一个传输计划，使其在满足压缩率约束和分类损失约束的前提下，最小化期望失真。这一形式化不仅统一了率、失真和分类三个维度，还为推导理论边界和设计实用算法提供了严格的数学基础。



## 核心方法与创新机理

### 问题重构：从率失真到约束最优传输

经典率失真理论隐含假设重建分布与源分布一致，无法同时处理跨域映射与下游任务约束。本工作将跨域有损压缩重新形式化为**带率和分类约束的最优传输问题**（Definition 2），其核心瓶颈在于：退化输入 $X \sim p_X$ 需被重建为满足目标分布 $p_Y$ 的输出 $Y$，同时受限于压缩率 $R$ 和分类不确定性 $C$。这一形式化将压缩、传输与下游任务统一在同一优化框架下，突破了传统方法仅关注信号保真度的局限。

### 关键机制：共享随机性与编码-压缩解耦

本方法引入独立于源信号的**共享随机变量 $U$**（$I(X;U)=0$），将系统解耦为两个阶段：
1. **确定性传输**：编码器利用 $(X,U)$ 直接生成满足目标分布 $p_Y$ 的重建 $Y$，满足 $H(Y|X,U)=0$；
2. **无损压缩**：对 $Y$ 进行无损压缩，平均码率逼近 $H(Y|U) \le R$。

这一解耦（Theorem 1）使问题退化为在传输计划 $p_{Y|X,U}$ 上同时优化失真、率和分类约束，避免了传统联合编码-传输的耦合复杂性。

### 分类约束的直接引入

与 Liu et al. (2022) 的熵约束最优传输仅含率约束 $H(Y|U) \le R$ 不同，本工作**显式引入分类约束 $H(S|Y) \le C$**，直接控制重建 $Y$ 对下游分类标签 $S$ 的条件不确定性。这一约束在渐近情况下被纳入单字母表征（Theorem 3, Theorem 5），使得率、失真与分类性能之间的三重权衡得以精确刻画。

### 损失函数层面的差异化设计

实验实现中，训练目标从传统 MSE + 率项扩展为三部分松弛损失（Section 5.1）：
$$\mathcal{L} = \mathbb{E}[\|X-\tilde{Y}\|^2] + \lambda_p W_1(p_Y, p_{\tilde{Y}}) + \lambda_c \mathbf{CE}(S, \hat{S})$$
其中：
- **Wasserstein-1 感知损失**通过 WGAN 判别器对齐重建分布与目标分布 $p_Y$，替代部分方法中的 GAN 损失；
- **交叉熵分类损失**由联合训练的 ResNet 分类头计算，作为 $H(S|Y)$ 的可微代理。消融实验（Figures 18-19）证实交叉熵与直接最小化条件熵在率-精度权衡曲线上高度一致。

### 理论可解释性的突破

在伯努利（Theorem 2）和高斯（Theorem 4）信源下，本工作导出了**闭式 DRC 函数**，明确给出失真-率-分类的三重边界。实验估计的 DRC 曲线与闭式理论曲线高度吻合（Figure 17），验证了框架的理论一致性。这一可解释性是以往基于深度学习的压缩方法所不具备的。



![[assets/figures/papers/paper_list_l31_https_openreview_net_forum_id_mUIGdUTtk2/figures/005_Figure_5.jpg]]
*Figure 5: Experimental architecture: a stochastic autoencoder with classifier and WGAN discriminator, conditioned on shared randomness U*

![[assets/figures/papers/paper_list_l31_https_openreview_net_forum_id_mUIGdUTtk2/figures/002_Figure_2.jpg]]
*Figure 2: System architecture of Theorem 1*

### 问题形式化：从率失真到约束最优传输

经典率失真理论隐含假设重建分布与源分布一致，无法直接处理跨域映射（如退化图像恢复至干净目标域）与下游分类约束的联合优化。本文的核心推进在于将跨域有损压缩重新定义为**带率和分类约束的最优传输问题**（Definition 2）。给定源分布 $p_X$、目标分布 $p_Y$ 和分类标签 $S$，系统需寻找一个传输计划，在满足压缩率约束 $H(Z|U) \le R$ 和分类不确定性约束 $H(S|Y) \le C$ 的前提下，最小化期望失真 $\mathbb{E}[d(X,Y)]$。

这一形式化的关键瓶颈突破在于引入**独立于源信号的共享随机性 $U$**（$I(X;U)=0$），将编码与压缩解耦为两步：首先由 $(X,U)$ 确定性生成重建 $Y$（即 $H(Y|X,U)=0$），再对 $Y$ 进行无损压缩，其平均码率逼近 $H(Y|U)$。定理 1 将原问题简化为仅涉及条件分布 $p_{Y|X,U}$ 的等价形式，使得传输计划在给定 $U$ 时退化为确定性映射，$U$ 成为系统唯一的随机性来源。

### 系统架构与模块关系

实验系统（Figure 5）将上述理论框架具象化为一个**随机自编码器 + 分类器 + 判别器**的联合架构，各模块的输入输出流如下：

```
X (退化输入) ─┬─► 编码器 f(·,U) ─► 通用量化 Q(·) ─► 解码器 g(·) ─► Ỹ (重建)
              │        ▲                │                  │
              │        │                ▼                  │
              │   共享随机性 U    熵瓶颈/率估计           ▼
              │                      (H(Y|U) ≤ R)    分类器头 ─► Ŝ (预测标签)
              │                                           │
              └─────────────────────────────────────► WGAN 判别器 d(·)
                                                       (W₁(p_Y, p_Ỹ))
```

**模块职责与数据流：**

1. **共享随机性注入 $U$**：作为编码器和解码器共享的独立噪声源，通过通用量化（universal quantization）实现，使传输计划在给定 $U$ 时确定化，同时为率约束提供可微的熵估计基础。

2. **编码器 $f(X,U)$**：接收退化输入 $X$ 与共享随机性 $U$，输出潜在表示。该映射实现了从源域到潜在空间的确定性传输（条件于 $U$）。

3. **通用量化 $Q(\cdot)$**：对潜在表示进行量化，其离散化输出直接关联率约束。量化后的表示进入熵瓶颈模块计算对数似然，提供可微的率项估计 $H(Y|U) \le R$。

4. **解码器 $g(\cdot)$**：将量化潜在表示重建为满足目标分布 $p_Y$ 的输出 $\tilde{Y}$，完成跨域映射。

5. **WGAN 判别器 $d(\cdot)$**：通过 Wasserstein-1 距离对齐重建分布 $p_{\tilde{Y}}$ 与目标分布 $p_Y$，以感知损失项 $\lambda_p W_1(p_Y, p_{\tilde{Y}})$ 的形式纳入训练目标。

6. **分类器头**：一个联合训练的 ResNet 分类分支，对重建图像 $\tilde{Y}$ 预测分类标签 $\hat{S}$，其交叉熵损失 $\lambda_c \mathbf{CE}(S, \hat{S})$ 作为条件熵约束 $H(S|Y) \le C$ 的松弛代理。

### 训练目标与约束松弛

完整的训练损失函数将理论框架中的硬约束松弛为可微的加权组合：

$$\mathcal{L} = \mathbb{E}[\|X - \tilde{Y}\|^2] + \lambda_p W_1(p_Y, p_{\tilde{Y}}) + \lambda_c \mathbf{CE}(S, \hat{S})$$

其中三项分别对应失真（MSE）、感知分布对齐（Wasserstein-1 距离）和分类性能（交叉熵）。率约束通过熵瓶颈模块内嵌于架构中，无需显式损失项。消融实验（Tables 1–5）通过调节 $\lambda_c$ 验证了率-失真-分类之间的三重权衡关系：过小的 $\lambda_c$ 导致分类精度不足，过大的 $\lambda_c$ 则因过度压缩分类相关信息而使重建质量与准确率同时崩溃，存在明确的最优权衡区域。

### 理论保证与实验验证的闭环

理论部分在伯努利（Theorem 2）和高斯（Theorem 4）信源下导出了闭式的失真-率-分类（DRC）函数，揭示了三个约束之间的显式边界。实验通过从闭式分布中抽样估算经验 DRC 曲线，与理论预测高度吻合（Figure 17），验证了框架的数学一致性。在真实图像任务（MNIST 超分辨、SVHN/CIFAR-10/ImageNet/KODAK 去噪）中，系统表现出符合理论预期的行为：更高的码率持续改善重建质量和分类精度，且通过调节分类约束强度可在率-失真平面上刻画清晰的等率线（Figure 16）。



### 问题形式化：从经典最优传输到约束最优传输

跨域有损压缩的核心挑战在于：源分布 $p_X$（如噪声图像）与目标分布 $p_Y$（如干净图像）不一致，且重建结果需同时满足压缩率约束和下游分类精度约束。经典最优传输仅最小化传输代价：

$$D(p_X, p_Y) = \inf_{p_{X,Y} \in \Gamma(p_X, p_Y)} \mathbb{E}[d(X,Y)]$$

其中 $\Gamma(p_X, p_Y)$ 为具有给定边际的联合分布集合，$d(\cdot,\cdot)$ 为失真度量。该形式无法纳入率约束和分类约束，因此本文将其扩展为**率和分类约束最优传输（RCOT）**：

$$D(R,C,p_X,p_Y) = \inf_{p_{U,X,Z,Y} \in \mathcal{M}} \mathbb{E}[d(X,Y)] \quad \text{s.t. } H(Z|U) \le R,\; H(S|Y) \le C$$

其中 $Z$ 为压缩表示，$U$ 为编解码器共享的独立随机性（$I(X;U)=0$），$S$ 为分类标签，$H(S|Y)$ 直接约束重建结果相对于真实标签的条件熵，$C$ 越小则分类不确定性越低。

### 关键洞察：共享随机性解耦编码与压缩

**定理 1** 揭示了共享随机性 $U$ 的核心作用：在单次设定下，系统可退化为两步过程——编码器将 $(X,U)$ 确定性映射为 $Y$（满足 $H(Y|X,U)=0$），随后对 $Y$ 进行无损压缩，平均码率逼近 $H(Y|U)$。这等价于以下简化问题：

$$D(R,C,p_X,p_Y) = \inf_{p_{U,X,Y} \in \mathcal{Q}} \mathbb{E}[d(X,Y)] \quad \text{s.t. } H(Y|X,U)=0,\; I(X;U)=0,\; H(Y|U) \le R,\; H(S|Y) \le C$$

**因果机制**：$U$ 作为独立随机源注入编码器和解码器，使传输计划在给定 $U$ 时退化为确定性映射，从而将“编码—压缩”联合优化解耦为“传输—压缩”两步。这一解耦是后续所有闭式解和实验架构的理论基石。

### 渐近情况：单字母表征

当处理长块信号时，RCOT 函数收敛于简洁的单字母形式（**定理 3**）：

$$D^{(\infty)}(R,C,p_X,p_Y) = \inf_{p_{X,Y} \in \Gamma(p_X,p_Y)} \mathbb{E}[d(X,Y)] \quad \text{s.t. } I(X;Y) \le R,\; H(S|Y) \le C$$

此时率约束由条件熵 $H(Y|U)$ 退化为互信息 $I(X;Y)$，与经典率失真理论一致，但额外保留了分类约束项。若进一步引入感知散度约束 $\phi(p_X,p_Y) \le P$，则得到 DRPC 函数的单字母表征（**定理 5**）：

$$D^{(\infty)}(R,P,C) = \inf_{p_{Y|X}} \mathbb{E}[d(X,Y)] \quad \text{s.t. } I(X;Y) \le R,\; H(S|Y) \le C,\; \phi(p_X,p_Y) \le P$$

### 伯努利与高斯信源的闭式解

在特定分布下，上述理论框架可导出显式的率-失真-分类权衡边界。

**伯努利信源**（汉明失真，**定理 2**）：设 $X \sim \text{Bern}(q_X)$，$Y \sim \text{Bern}(q_Y)$，分类变量 $S = X \oplus S_1$ 且 $S_1 \sim \text{Bern}(q_{S_1})$，则 DRC 函数为分段闭式：

$$D^{(B)}(R,C,q_X,q_Y) = \begin{cases} \frac{-2(1-q_X)q_X(H_b(m)-C)}{H_b(m)-H_b(q_{S_1})} + D_{\mathrm{ind}}^{(B)}, & \text{中间 } C \text{ 区域} \\ \frac{-2(1-q_X)q_X R}{H_b(q_X)} + D_{\mathrm{ind}}^{(B)}, & \text{松弛 } C \text{ 区域} \\ D_{\mathrm{min}}^{(B)}, & R>H_b(q_X),\, C>H_b(q_S) \end{cases}$$

其中 $H_b(\cdot)$ 为二元熵函数，$m = q_X(1-q_Y) + (1-q_X)q_Y$ 为独立联合分布下的错误概率，$D_{\mathrm{ind}}^{(B)}$ 为无约束时的最小失真。该分段结构揭示了三个工作区：分类约束紧时失真随 $C$ 线性变化；分类约束松弛时失真仅由率 $R$ 决定；两者均松弛时达到无约束最优传输下界。

**高斯信源**（MSE 失真，**定理 4**）：设 $X,Y,S$ 联合高斯，则渐近 DRC 函数为：

$$D^{(G)}(R,C,q_X,q_Y) = \begin{cases} (\mu_X-\mu_Y)^2+\sigma_X^2+\sigma_Y^2-\frac{2\sigma_S\sigma_X^2\sigma_Y}{\theta_1}\sqrt{1-e^{-2h(S)+2C}}, & C \text{ 有效} \\ (\mu_X-\mu_Y)^2+\sigma_X^2+\sigma_Y^2-2\sigma_X\sigma_Y\sqrt{1-2^{-2R}}, & C \text{ 无效} \\ 0, & C>h(S),\, R>h(X) \end{cases}$$

其中 $\theta_1 = \text{Cov}(X,S)$ 刻画源与分类标签的相关强度。当分类约束 $C$ 有效时，失真随 $C$ 减小而增大，且增大速率由 $\theta_1$ 调控——相关性越强，分类约束对失真惩罚越小。当 $C$ 足够大时，分类约束失效，退化为经典高斯率失真函数。

### 实验中的松弛训练目标

实际训练中，硬约束 $H(S|Y) \le C$ 和分布匹配 $p_Y = p_{\tilde{Y}}$ 难以直接优化，因此采用拉格朗日松弛：

$$\mathcal{L} = \mathbb{E}[\|X-\tilde{Y}\|^2] + \lambda_p W_1(p_Y, p_{\tilde{Y}}) + \lambda_c \mathbf{CE}(S, \hat{S})$$

三项分别对应：MSE 失真、Wasserstein-1 感知距离（通过 WGAN 判别器实现）、交叉熵分类损失（通过联合训练的 ResNet 分类头估计）。其中交叉熵损失被证明是条件熵 $H(S|Y)$ 的有效替代——消融实验（Figure 18–19）显示直接最小化 $H(S|Y)$ 与使用 CE 损失产生一致的率-精度权衡曲线。

### 模块化流水线

实验架构（Figure 5）由七个核心模块串联：

1. **共享随机性注入 $U$**：通过通用量化实现，为编解码器提供独立噪声源。
2. **编码器 $f(\cdot, U)$**：将退化输入 $X$ 与 $U$ 映射为潜在表示。
3. **通用量化 $Q(\cdot)$**：对潜在表示量化，实现可微压缩。
4. **熵瓶颈/率估计**：对量化表示计算对数似然，提供可微率项 $H(Q(f(X,U)))$。
5. **解码器 $g(\cdot)$**：将量化表示重建为 $\tilde{Y}$。
6. **WGAN 判别器**：通过 $W_1(p_Y, p_{\tilde{Y}})$ 对齐重建分布与目标分布。
7. **分类器头**：对 $\tilde{Y}$ 预测标签 $\hat{S}$，计算交叉熵损失。

整个流水线的理论根基在于定理 1 的解耦原理：$U$ 使传输确定化，量化与熵瓶颈处理压缩，判别器和分类器分别施加感知与分类约束。



## 实验与关键发现

### 核心实验设定

实验将 RCOT 框架实例化为一个随机自编码器，其结构如 Figure 5 所示：共享随机性 $U$ 通过通用量化（universal quantization）注入编码器 $f(\cdot, U)$，编码器将退化输入 $X$ 与 $U$ 映射为潜在表示，经量化 $Q(\cdot)$ 后由解码器 $g(\cdot)$ 重建为 $\tilde{Y}$。率约束通过熵瓶颈对量化表示计算对数似然实现；分布对齐采用 WGAN 判别器，以 Wasserstein-1 距离 $W_1(p_Y, p_{\tilde{Y}})$ 匹配目标分布；分类约束通过一个联合训练的 ResNet 分类头对重建图像预测标签 $\hat{S}$，以交叉熵 $\mathbf{CE}(S, \hat{S})$ 近似条件熵 $H(S|Y)$。训练目标为松弛损失：

$$\mathcal{L} = \mathbb{E}[\|X - \tilde{Y}\|^2] + \lambda_p W_1(p_Y, p_{\tilde{Y}}) + \lambda_c \mathbf{CE}(S, \hat{S})$$

其中 $\lambda_p$ 和 $\lambda_c$ 分别控制感知对齐与分类约束的强度。实验覆盖 MNIST 超分辨、SVHN/CIFAR-10/ImageNet/KODAK 高斯去噪、SVHN 修复等任务。

### 主要定量结果

**KODAK 高斯去噪 ($\sigma=25$) 对比。** Table 15 给出了与经典基线的全面比较。RCOT 在感知质量指标上取得一致优势：LPIPS 达到 0.1987，优于 BM3D（0.2235）和 DeCompress（0.2168）；DISTS 为 0.1638，低于 DeCompress（0.1967）和 BM3D（0.2109）；感知指数 PI 为 2.1670，显著优于 BM3D（2.6503）和 OTDenoising（2.7093）。这些结果表明，引入分类约束并未损害感知重建质量，反而在感知-失真权衡上获得了更优解。


![[assets/figures/papers/paper_list_l31_https_openreview_net_forum_id_mUIGdUTtk2/figures/067_Table_15.jpg]]
*Table 15: Comparison of denoising performance on the KODAK dataset with Gaussian noise $\mathcal { N }$ ( 0 , $\sigma ^ { 2 }$ ) , $\sigma = \bar { 2 5 }$ . Best values are in bold and second-best values are underlined

**跨任务率-失真-精度权衡。** Table 11–12 展示了 MNIST 超分辨和 SVHN 去噪的细粒度定量结果。在 MNIST 4× 超分辨中，当率从 0.15 bpp 增至 1.36 bpp 时，MSE 从 0.0064 降至 0.0051，分类准确率从 0.8404 升至 0.9670。SVHN 去噪 ($\sigma=20$) 呈现类似趋势：率从 0.12 bpp 增至 2.71 bpp 时，准确率从 0.6130 升至 0.8292。Figure 6 的可视化结果进一步证实，低率下重建仅捕获粗略结构，高率下细节和清晰度显著提升。

**RDC 函数与等率线。** Figure 16 绘制了 MNIST 和 SVHN 上的率-失真-分类（RDC）函数，并在 $R(D,C)$ 平面上叠加等率线。该可视化清晰揭示了固定率约束下失真与分类性能之间的明确权衡边界：在任一固定率下，降低失真必然牺牲分类精度，反之亦然，且该边界随率增大向外扩展。


![[assets/figures/papers/paper_list_l31_https_openreview_net_forum_id_mUIGdUTtk2/figures/058_Figure_16.jpg]]
*Figure 16: The RDC functions on the MNIST and SVHN datasets, together with the equi-rate lines plotted on R ( D , C ) , highlight the tradeoff between distortion and classification performance at any fixed rate constraint*

### 消融实验：分类约束强度的影响

Tables 1–5 系统考察了分类损失权重 $\lambda_c$ 对率-失真-精度三元权衡的调控作用。核心发现如下：


![[assets/figures/papers/paper_list_l31_https_openreview_net_forum_id_mUIGdUTtk2/figures/044_Table_3.jpg]]
*Table 3: Performance across λ values for denoising on CIFAR-10 with Gaussian noise, ${ \mathcal { N } }$ ( 0 , $\sigma ^ { 2 }$ ) with σ = 25 (Fig. 8(a), Fig. 8(b))

![[assets/figures/papers/paper_list_l31_https_openreview_net_forum_id_mUIGdUTtk2/figures/045_Table_4.jpg]]
*Table 4: Performance across λ values for denoising on ImageNet with Gaussian noise, ${ \mathcal { N } }$ ( 0 , $\sigma ^ { 2 }$ ) with σ = 25 (Fig. 8(d), Fig. 8(e))

![[assets/figures/papers/paper_list_l31_https_openreview_net_forum_id_mUIGdUTtk2/figures/046_Table_5.jpg]]
*Table 5: Performance across λ values for denoising on KODAK with Gaussian noise, ${ \mathcal { N } }$ ( 0 , $\sigma ^ { 2 }$ ) with σ = 25 (Fig. 10)

**MNIST 超分辨（Table 1）。** $\lambda_c=0$（无分类约束）时准确率最高（0.9670），MSE 最低（0.0055），但率也最高（1.36 bpp）。$\lambda_c=1000$ 时准确率降至 0.8404，MSE 略升至 0.0064，率大幅降至 0.15 bpp。$\lambda_c=50000$ 时准确率崩溃至 0.3477，表明过度强调分类约束会破坏重建质量。存在一个最优权衡区间（$\lambda_c \in [100, 1000]$），在此区间内率显著降低而精度损失可控。


![[assets/figures/papers/paper_list_l31_https_openreview_net_forum_id_mUIGdUTtk2/figures/042_Table_1.jpg]]
*Table 1: Performance across λ values for 4× super-resolution on MNIST (Fig. 7(a), Fig. 7(b))*

**SVHN 去噪（Table 2）。** $\lambda_c=200$ 时达到最佳折衷：MSE 最低（0.0048），准确率 0.7702，率 0.5237 bpp。$\lambda_c$ 继续增大至 20000 时，准确率骤降至 0.2000，MSE 升至 0.0141，表明分类约束过强时系统会牺牲重建保真度来满足分类条件，反而损害整体性能。


![[assets/figures/papers/paper_list_l31_https_openreview_net_forum_id_mUIGdUTtk2/figures/043_Table_2.jpg]]
*Table 2: Performance across λ values for denoising on SVHN with Gaussian noise, ${ \mathcal { N } }$ ( 0 , $\sigma ^ { 2 }$ ) with σ = 25 (Fig. 7(d), Fig. 7(e))

**CIFAR-10/ImageNet/KODAK 去噪（Tables 3–5）。** 趋势一致：适中的 $\lambda_c$（CIFAR-10 上约 50–100，ImageNet 上约 5–50，KODAK 上约 100）可在保持可接受失真的前提下有效降低率并维持分类精度；$\lambda_c$ 过大时所有指标均恶化。

### 噪声水平对分类性能的影响

Figure 9 展示了 CIFAR-10 和 ImageNet 去噪中噪声水平 $\sigma$ 从 15 增至 50 时的性能变化。随噪声增强，分类准确率显著下降，符合理论预期——更强的噪声增大了 $H(S|X)$，在固定分类约束 $C$ 下可达到的准确率上限降低。这一结果验证了 RCOT 框架中分类约束 $H(S|Y) \leq C$ 的合理性：当输入信息本身不足以支持高精度分类时，任何重建方法都无法突破该信息论极限。

### 条件熵与交叉熵损失的等价性验证

Figures 18–19 对比了直接最小化 $H(S|Y)$ 与使用交叉熵损失的效果。在 MNIST 超分辨和 SVHN 去噪上，两种方法产生几乎一致的率-精度权衡曲线。这一消融验证了实验中以交叉熵替代条件熵的合理性，同时也表明分类器头对 $H(S|Y)$ 的估计足够可靠。

### 理论-实验一致性

Figure 17 将伯努利分布（Theorem 2）和高斯分布（Theorem 4）下的闭式 DRC 曲线与从实验样本估算的经验曲线进行对比。理论预测与实验估计高度吻合，表明即使在有限样本和神经网络近似下，RCOT 框架导出的率-失真-分类三重边界仍具有强预测力。

### 修复任务的扩展验证

Tables 7–8 和 Figures 12–13 展示了 SVHN 修复（inpainting）任务的结果。有监督设定下（Table 7），率从 0.04 bpp 增至 1.19 bpp 时准确率从 0.4840 升至 0.8190，MSE 从 0.0328 降至 0.0109。无监督设定下（Table 8）呈现类似趋势，尽管缺乏干净目标，自监督模型仍能在更高率下产生更连贯的数字结构和更高分类精度。这表明 RCOT 框架对不同的退化类型（去噪、超分辨、修复）和不同的监督范式（有监督、无监督）均具有泛化能力。

### 补充图表

![[assets/figures/papers/paper_list_l31_https_openreview_net_forum_id_mUIGdUTtk2/figures/048_Table_7.jpg]]
*Table 7: Supervised inpainting on SVHN across λ values (Figure 12)*

![[assets/figures/papers/paper_list_l31_https_openreview_net_forum_id_mUIGdUTtk2/figures/049_Table_8.jpg]]
*Table 8: Unsupervised inpainting on SVHN across λ values (Figure 13)*

![[assets/figures/papers/paper_list_l31_https_openreview_net_forum_id_mUIGdUTtk2/figures/050_Table_8.jpg]]



## 定位与知识库关联

### 核心定位：约束最优传输框架下的跨域有损压缩

本工作将跨域有损压缩形式化为**约束最优传输（Constrained Optimal Transport）**问题，其理论根基可追溯至经典率失真理论（Shannon, 1959）与最优传输理论（Villani, 2009）的交汇处。与经典率失真理论假设重建分布与源分布一致不同，RCOT 显式允许源分布 $p_X$ 与目标分布 $p_Y$ 不同，从而覆盖退化图像恢复（去噪、超分辨、修复）等跨域场景。

框架的核心创新在于在传输计划中同时嵌入两个约束：
1. **率约束** $H(Y|U) \leq R$（单次设定）或 $I(X;Y) \leq R$（渐近设定），控制压缩代价；
2. **分类约束** $H(S|Y) \leq C$，直接限制重建信号 $Y$ 关于下游分类标签 $S$ 的条件熵，确保压缩后的表示对分类任务有用。

这一双重约束结构使 RCOT 区别于仅关注感知－失真权衡的工作（如 Blau & Michaeli, 2018 的 DRP 框架），后者未引入分类约束，也未在率约束下展开系统分析。

### 与基线方法的区别

**Liu et al. (2022) 的熵约束最优传输** 是 RCOT 最直接的理论前驱。该工作将率约束引入最优传输，但仅约束 $H(Y|U) \leq R$，未包含分类项。RCOT 在此基础上增加了 $H(S|Y) \leq C$，将问题从“率－失真”二元权衡扩展为“率－失真－分类”三元权衡，并在伯努利和高斯信源下导出了闭式权衡边界（Theorem 2, Theorem 4），这是 Liu et al. 未涉及的。

在实验层面，传统基线包括：
- **JPEG-2K**（Taubman et al., 2002）：经典有损压缩方法，未针对跨域映射设计，无分类感知能力。
- **BM3D**（Dabov et al., 2007）：经典去噪算法，在 KODAK 高斯去噪（$\sigma=25$）上 LPIPS 为 0.2235，RCOT 达到 0.1987（Table 15）。
- **OTDenoising** 和 **DeCompress**：分别代表无监督最优传输去噪和基于压缩的去噪框架，RCOT 在 KODAK 上的 DISTS（0.1638 vs. 0.1967）和 PI（2.1670 vs. 2.6503）均优于两者（Table 15）。

RCOT 在架构层面引入三个区别于上述基线的关键模块：
1. **共享随机性注入 U**：通过通用量化（Ziv, 1985; Theis & Agustsson, 2021）实现，使编码/解码共享噪声源，将系统简化为确定性传输计划（Theorem 1），编码与压缩解耦。
2. **WGAN 判别器**：通过 Wasserstein-1 距离对齐重建分布与目标分布 $p_Y$，替代传统 GAN 损失。
3. **联合训练的分类器头**：一个 ResNet 分类分支直接估计交叉熵，用于近似条件熵约束 $H(S|Y)$（Figures 18-19 验证了 CE 替代 $H(S|Y)$ 的合理性）。

### 适用边界

RCOT 的理论闭式解目前仅限于两类分布：
- **伯努利信源**（Theorem 2）：汉明失真下，分类变量 $S = X \oplus S_1$ 的简单生成模型。
- **高斯信源**（Theorem 4, 6, 7）：MSE 失真下，$X, Y, S$ 联合高斯，感知约束支持 $W_2^2$ 或 KL 散度（Theorem 6）。

实验验证覆盖 MNIST（4×超分辨）、SVHN/CIFAR-10/ImageNet/KODAK（高斯去噪）和 SVHN（修复），均在低分辨率或中等分辨率图像上展开。对于高分辨率自然图像的大规模压缩任务，论文未提供实验证据，端到端训练包含判别器、分类器和率估计器的复杂框架的可行性仍需验证。

### 局限与开放问题

1. **分布假设的局限性**：闭式解仅限于伯努利和高斯分布。能否推广到混合分布、重尾分布或更一般的信源模型，是理论扩展的核心开放问题。
2. **分类器不完美估计的影响**：实验中用交叉熵损失近似 $H(S|Y)$，但实际分类器的不完美估计会引入偏差。如何自适应地调整约束强度 $\lambda_c$ 以应对不同任务和噪声水平，尚未系统研究。
3. **感知散度的选择空间**：当前实验使用 Wasserstein-1 距离，理论分析覆盖 $W_2^2$ 和 KL 散度（Theorem 6-7）。是否存在更优的感知散度（如最大均值差异 MMD）能在更广泛场景中产生更好的 DRPC 边界，仍是开放问题。
4. **分类约束的扩展性**：当前分类约束针对单一标签 $S$。能否扩展到多任务、结构化输出（如语义分割、目标检测），需要重新定义条件熵约束的形式。
5. **大规模训练的可行性**：框架涉及自动编码器、判别器、分类器和率估计器的联合优化，在大规模真实图像压缩中的训练稳定性和计算效率尚未验证。

### 知识库定位

RCOT 处于**信息论、最优传输和深度学习**的交叉点：
- 在信息论侧，它将 Shannon 的率失真函数推广为率－失真－分类函数（DRC），并进一步引入感知约束（DRPC），提供了单字母表征（Theorem 3, 5）。
- 在最优传输侧，它将经典 Monge-Kantorovich 问题扩展为带信息论约束的传输问题，揭示了传输计划、压缩率和分类不确定性之间的内在耦合。
- 在深度学习侧，它提供了一个原则性的损失设计框架：MSE 失真 + Wasserstein 感知损失 + 交叉熵分类损失，三者通过拉格朗日松弛统一优化。



## 原文 PDF

![[paperPDFs/ICLR_2026/Cross_Domain_Lossy_Compression_via_Rate_and_Classification_Constrained_Optimal_Transport.pdf]]
