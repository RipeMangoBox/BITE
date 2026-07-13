---
title: "Iterative Training of Physics-Informed Neural Networks with Fourier-enhanced Features"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Iterative_Training_of_Physics_Informed_Neural_Networks_with_Fourier_enhanced_Features.pdf
project_link: null
code_link: null
aliases:
- IPITPFEF
- ITPINNFEF
tags:
- ICLR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/algorithms
core_operator: "引入随机傅里叶特征（Random Fourier Features, RFF）扩展特征空间，并将训练解耦为上层特征基生成和下层线性回归，从而打破耦合，使线性PDE的下层问题成为凸优化，保证全局最优。"
primary_logic: "通过在隐藏层输出上施加RFF映射，生成一个与网络宽度解耦的大规模扩展基，使下层回归问题可凸优化；迭代交替训练保证收敛，并显著提升对高频成分的逼近能力。"
claims:
- "IFeF-PINN通过随机傅里叶特征扩展基函数，有效缓解PINN的谱偏差问题。"
- "对于线性PDE，下层回归问题构成凸二次规划，存在唯一全局最优解，这是实现精确拟合的关键。"
- "迭代训练算法在标准假设下收敛到稳定点，保证学习过程的鲁棒性。"
- "在高频PDE基准测试中，IFeF-PINN显著优于现有方法，多数基线无法收敛，同时通过频谱分析显示高频分量得以有效恢复。"
---

# Iterative Training of Physics-Informed Neural Networks with Fourier-enhanced Features

> [!tip] 核心洞察
> 通过在隐藏层输出上施加RFF映射，生成一个与网络宽度解耦的大规模扩展基，使下层回归问题可凸优化；迭代交替训练保证收敛，并显著提升对高频成分的逼近能力。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 基于傅里叶增强特征的物理信息神经网络迭代训练方法 |
| 英文题名 | Iterative Training of Physics-Informed Neural Networks with Fourier-enhanced Features |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=ybffyf7LE7) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/algorithms |
| Method | IFeF-PINN (Iterative training of PINNs with Fourier-enhanced Features) |
| Dataset | Low-frequency Helmholtz (a1=1,a2=4), Viscous Burgers (nonlinear), Low-frequency benchmarks (Helmholtz, Convection, Reaction) |

> [!tip] 效果简介
> - Low-frequency Helmholtz (a1=1,a2=4) 上，Relative L² error (std) 为 0.0003 (IFeF)，对比 0.0088 (End-to-End training)，变化 -0.0085。
> - Viscous Burgers (nonlinear) 上，Relative L² error 为 0.0024 (IFeF)，对比 0.0049 (End-to-End training)，变化 -0.0025。
> - Low-frequency benchmarks (Helmholtz, Convection, Reaction) 上，Relative L² error (log10 boxplot) 为 IFeF-PD/IFeF median ~10^{-4} (详见Figure 2)，对比 所有基线方法误差中位数普遍高于10^{-3}，变化 显著降低 1-2 个数量级。

## 概要

标准物理信息神经网络（PINN）在逼近偏微分方程（PDE）解时存在严重的谱偏差（spectral bias）：网络倾向于优先拟合低频成分，导致高频振荡、多尺度等特征的捕捉能力极差，数值精度难以满足要求。针对这一瓶颈，本文提出 **IFeF-PINN**（Iterative training of PINNs with Fourier-enhanced Features），核心思想是将随机傅里叶特征（Random Fourier Features, RFF）映射到隐藏层输出上，生成一个与网络宽度解耦的高维扩展基，并将训练过程分解为**上层特征基生成**与**下层线性回归**的双级联优化。对于线性PDE，下层回归问题自然约化为一个凸二次规划，存在唯一全局最优解（Proposition 1），从而在结构上突破了传统端到端PINN的非凸训练困境。理论分析进一步表明，迭代算法在适当假设下收敛到稳定点（Theorem 1），且RFF扩展基构成的特征空间严格包含原始特征空间（Theorem 2），增强了模型对高频的函数逼近能力。

在实验层面，IFeF-PINN在低频谱基准上相较标准PINN、NTK、PINNsformer等基线方法取得压倒性优势：中位数相对 $L^2$ 误差普遍低至 $10^{-4}$ 量级，比端到端训练降低约两个数量级。更具说服力的高频与多尺度PDE实验中，多数基线方法无法收敛，而IFeF-PINN成功恢复高频解，例如在亥姆霍兹方程（$a_1=a_2=100$）上相对 $L^2$ 误差仅 $0.0156 \pm 0.0055$。消融分析证实，去除RFF基扩展或改为单阶段端到端训练均导致性能严重退化，而增大傅里叶特征数量 $D$ 能直接提升网络的高频表达能力。主要局限包括：非线性PDE下层优化不再保证凸性，性能提升幅度受限；算法对随机特征维度 $D$ 和缩放参数 $\sigma$ 敏感，且内存占用较高，需针对具体问题调优。



物理信息神经网络（PINN）将偏微分方程（PDE）作为软约束嵌入损失函数，使PDE求解转化为参数优化问题（Section 2.1）。考虑一般线性PDE
$$
\begin{array}{rl}
\mathfrak{F}[u](x) = f(x),\quad x\in\Omega,
$$
2pt]
\mathfrak{B}[u](s) = g(s),\quad s\in\Gamma\subseteq\partial\Omega,
\end{array}
$$
标准PINN通过蒙特卡洛采样近似边界残差与内部方程残差，最小化如下损失：
$$
\hat{\mathfrak{L}}_\lambda(u_\omega)=\frac{1}{N_u}\sum_{i=1}^{N_u}\|g(x_u^i)-\mathfrak{B}[u_\omega](x_u^i)\|^2+\frac{\lambda}{N_f}\sum_{i=1}^{N_f}\|\mathfrak{F}[u_\omega](x_f^i)\|^2 .
$$
尽管该框架在诸多问题上取得进展，一个根本瓶颈在于神经网络的**谱偏差（spectral bias）**：网络训练倾向于优先学习低频成分，对高频振荡解的捕捉能力严重不足，导致数值精度随频率升高而急剧退化（ABSTRACT, 1 INTRODUCTION）。

现有方法试图从不同角度缓解此问题，例如基于神经正切核的NTK变体、Transformer结构的PINNsformer、物理信息高斯过程PIG等。然而，这些方法大多沿用单阶段端到端联合优化，损失曲面高度非凸，无法提供全局最优性保证；特征表示仅依赖隐藏层输出，缺少显式的高频基表达，致使高频PDE场景下多数基线无法收敛（Table 2）。

为突破上述局限，本文提出**IFeF-PINN（Iterative Training of PINNs with Fourier-enhanced Features）**。其核心动机来自三条关键设计：
- **引入随机傅里叶特征（RFF）扩展特征空间**：在隐藏层输出 $h_\omega(x)$ 上施加RFF映射 $\psi_D(x)=\gamma_D(h_\omega(x))$（Section 3.1），生成维度为 $2D$ 的扩展基函数集，显著增强网络对高频模式的表达能力。理论上，该扩展特征空间严格包含原始特征空间（Theorem 2, Section 4.2），为高频逼近提供更丰富的假设类。
- **解耦训练为双级联优化**：将参数分离为控制特征基的 $\omega$ 与线性输出系数 $\theta$。对于线性PDE，下层问题退化为关于 $\theta$ 的凸二次规划 $\min_\theta \frac12\theta^\top Q(\omega)\theta + c(\omega)^\top\theta$，存在唯一全局最优解（Proposition 1, Section 3.2），从根本上消除联合训练时的非凸困境。
- **保证收敛性与稳定性**：迭代交替更新 $\omega$ 与 $\theta$，在标准假设下收敛至稳定点（Theorem 1, Section 4.1），确保训练过程鲁棒。

通过上述机制，IFeF-PINN旨在克服谱偏差，实现高频PDE的高精度求解，并在线性PDE情形下获得可证的全局最优逼近，为PINN在科学计算中的实用化提供重要增强。



## 核心方法与创新机理

IFeF‑PINN 的核心创新在于将 PINN 的训练解耦为可独立优化的两级结构：上层通过随机傅里叶特征（RFF）映射生成一个与网络宽度解耦的扩展基函数集，下层在该基上求解线性回归系数。这一设计直接针对标准 PINN 的谱偏差瓶颈——多层感知机天然倾向于优先拟合低频分量，导致高频振荡解被严重平滑。通过引入可显式控制频率覆盖的 RFF 基，IFeF‑PINN 将原始网络的隐式谱表示转化为显式频率增强的线性组合，同时利用线性偏微分方程（PDE）的结构将下层问题转化为凸二次规划，从而保证全局最优系数的求解。该机制构成了四个关键 **changed slots**，分别对应特征生成、训练信息流、最优性保证与非线性扩展。

**1. 特征增强方式：从隐层输出到 RFF 扩展基。**  
标准 PINN 仅将隐藏层末端的输出 $h_\omega(x)$ 直接送入线性层，其频率特性完全由网络深度和参数 $\omega$ 隐式决定，无法避免谱偏差。IFeF‑PINN 在 $h_\omega(x)$ 后插入固定的 RFF 映射 $\psi_D(x) = \frac{1}{\sqrt{D}}[\cos(2\pi \mathbf{B}_D h_\omega(x)); \sin(2\pi \mathbf{B}_D h_\omega(x))]$（Section 3.1, Equation (5)），其中 $\mathbf{B}_D$ 的每个元素从高斯分布 $\mathcal{N}(0,\sigma^2)$ 采样且训练中保持固定。这一映射将 $p$ 维的隐层特征膨胀为 $2D$ 维的傅里叶基，使基函数的数量独立于网络宽度（可任意增大 $D$）。由于正弦/余弦核天然包含高频成分，RFF 基在源头上为网络注入了捕捉剧烈振荡的能力，频谱分析（Figure 5）直接显示扩展基中高频分量的幅度随 $D$ 增加而显著提升。消融实验中，移除 RFF 映射后模型在低频对流方程上的相对 $L^2$ 误差飙升至 $1.49\times10^{-2}$（Section 6.1），证实该映射是缓解谱偏差的**必要条件**。

**2. 训练信息流：从单级联耦合优化到双级联迭代。**  
传统 PINN 的损失函数 $\hat{\mathfrak{L}}_\lambda(u_\omega)$ 同时依赖所有权重参数，梯度下降必须在一个高度非凸的联合空间中进行，导致优化困难与收敛缓慢。IFeF‑PINN 将参数拆分为 $\omega$（特征基生成）与 $\theta$（线性回归系数），并形成双层结构：上层以 $\omega$ 为变量最小化损失，下层以 $\theta$ 为变量在给定 $\omega$ 下求解最优回归。这一解耦使两个子问题在性质上截然不同：上层负责学习符合 PDE 的隐式流形映射，下层负责在该流形上进行系数拟合。训练时交替执行上、下层更新（Algorithm 1），打破了原始端到端训练中参数间的强耦合，形成一种“特征提取—回归”的协同演化。

**3. 线性 PDE 的最优性保证：下层问题转化为凸二次规划。**  
对于线性 PDE，微分算子 $\mathfrak{F}$ 和边界算子 $\mathfrak{B}$ 在 $u_{\omega,\theta}$ 上保持线性，因此离散损失 $\hat{\mathfrak{L}}_\lambda(u_{\omega,\theta})$ 展开后是 $\theta$ 的二次型 $\frac{1}{2}\theta^\top Q(\omega)\theta + c(\omega)^\top\theta$（Proposition 1, Section 3.2）。由于 $Q(\omega)$ 是半正定矩阵，下层问题成为凸二次规划，存在**唯一全局最优解** $\theta^* = -Q^{-1}c$。这一性质是端到端训练无法企及的——后者不仅在非凸曲面上仅能获得局部极小，且常因条件数差而停滞。在消融实验中，线性 Helmholtz 方程的端到端训练相对误差为 $8.8\times10^{-3}$，而 IFeF‑PINN 利用凸优化获得 $3.0\times10^{-4}$（Table 3），误差下降超一个数量级，凸性带来的增益极为显著。

**4. 非线性 PDE 的局部双级联扩展。**  
对于非线性 PDE，损失对 $\theta$ 不再保持二次型，因此无法保证全局最优。IFeF‑PINN 采用一种局部双级联策略（Algorithm 2, Section 3.4）：在下层内部进行 $N_{lower}$ 步梯度下降或直至收敛来更新 $\theta$，再在上层更新 $\omega$。虽然下层问题非凸，但固定 $\omega$ 后其维度相对较低，交替迭代仍能收敛到**局部稳定点**。实验表明该扩展在粘性 Burgers 方程上相对 $L^2$ 误差从端到端的 $4.9\times10^{-3}$ 降至 $2.4\times10^{-3}$（Table 3），说明即使放弃全局最优性，解耦训练依然优于联合优化。理论分析（Theorem 1, Section 4.1）进一步证明了在标准假设下双级联算法收敛到稳定点，赋予该方法统一的收敛框架。

**理论支撑与表达空间扩展。**  
除了上述工程改变，IFeF‑PINN 还带来表达能力的理论提升：Theorem 2（Section 4.2）证明 RFF 扩展后的函数空间 $\mathcal{H}_{\text{RFF}}$ 严格包含原始隐藏层特征空间 $\mathcal{H}_f$，即 $\mathcal{H}_f \subsetneq \mathcal{H}_{\text{RFF}}$。也就是说，任何由原始网络能表示的函数均可在扩展基上表达，而 RFF 基还能额外表示大量包含高频成分的函数，这从根本上解释了为何该方法能突破标准 PINN 的表示瓶颈。值得注意的是，该优势的实现依赖于超参数 $D$ 和 $\sigma$ 的精细调节：Table 4 显示，若 $\sigma$ 取值过小（如 $\sigma=0.1$），Helmholtz 方程误差从 $2.1\times10^{-4}$ 升至 $1.5\times10^{-3}$，暗示实际部署时需针对问题域调整频率带宽与基数量。

综上，IFeF‑PINN 的创新点构成了一个**结构—优化—理论**三位一体的增强框架：RFF 引入显式高频基解决表示缺陷，双级联训练提供优化层次的解耦与凸性保证，理论分析则严格证明了收敛性与表达空间的扩充。这些改变使该方法在多项高频、多尺度 PDE 基准上（Table 2）成为唯一能够收敛并获得高精度的方案，而同类基线多因谱偏差彻底失效（标记为“-”）。



![[assets/figures/papers/iclr26_0013_ybffyf7LE7_Iterative_Training_of_Physics-Informed_Neural_Ne/figures/001_Figure_1.jpg]]
*Figure 1: Architecture of IFeF-PINN. The first part (in yellow) generates the nominal basis vectors, which are then extended via $\gamma _ { D }$ generating random Fourier features $\psi _ { D }$ (in green), and a linear combination of the extended basis (in blue) forms the approximated solution $u _ { \omega , \theta }$

![[assets/figures/papers/iclr26_0013_ybffyf7LE7_Iterative_Training_of_Physics-Informed_Neural_Ne/figures/002_Table_1.jpg]]
*Table 1: Representative methods for approximating solutions to PDE, highlighting application domain, key idea, high-frequency handling (HF), limitations, and optimality*

IFeF‑PINN 的架构遵循“名义基生成 → 随机傅里叶特征扩展 → 线性组合”的三阶段前向流，配合解耦的双级联迭代训练，如 Figure 1 所示。其输入是定义域内的采样坐标 $x$，输出是 PDE 的近似解 $u_{\omega,\theta}(x)$，具体流程如下：

1. **名义基生成**（Figure 1 黄色部分）  
   多层前馈网络 $h_{\omega}$ 以坐标 $x$ 为输入，输出低维非线性特征 $h_{\omega}(x)$。这部分充当基函数的“原型”，其参数 $\omega$ 属于上层优化变量。

2. **随机傅里叶特征扩展**（Figure 1 绿色部分）  
   在 $h_{\omega}(x)$ 上施加随机傅里叶特征映射 $\gamma_D$，生成扩展基向量
   $$\psi_D(x) = \gamma_D\!\left(h_{\omega}(x)\right)$$
   （详见 Section 3.1）。该映射通过高维随机投影 $\mathbf{B}_D$ 将特征维度提升至 $2D$，使扩展基直接包含高频成分，从而缓解标准 PINN 的谱偏差。

3. **线性组合求解**（Figure 1 蓝色部分）  
   以 $\psi_D(x)$ 为基底，通过线性系数 $\theta$ 加权组合得到近似解
   $$u_{\omega,\theta}(x) = \psi_D(x)^{\top}\theta$$
   （见 Section 3.2）。$\theta$ 的优化对应下层问题。

### 输入‑输出流与双级联优化

训练损失采用边界残差与内部 PDE 残差的蒙特卡洛近似（Section 2.1 的离散损失 $\hat{\mathfrak{L}}_\lambda$）。IFeF‑PINN 将其训练分解为两个交替优化的子问题（Section 3.3）：

- **上层（基生成）**：固定 $\theta$，优化隐藏层参数 $\omega$，使网络学习更适配解空间的基函数。
- **下层（线性回归）**：固定 $\omega$，优化系数 $\theta$ 以最小化损失。对于**线性 PDE**，下层损失 $\mathfrak{L}_{\mathrm{lower}}(\theta\mid\omega)$ 具有二次形式
  $$\mathfrak{L}_{\mathrm{lower}}(\theta\mid\omega) = \frac{1}{2}\theta^{\top}Q(\omega)\theta + c(\omega)^{\top}\theta + b,$$
  因此是凸问题，直接求得全局最优解 $\theta^{\star}(\omega) = -Q(\omega)^{-1}c(\omega)$（Proposition 1），从根本上避免下层训练陷入局部最优。对于**非线性 PDE**，下层问题非凸，则采用梯度下降近似求解，并将更新与上层交替进行（Algorithm 2）。

这种解耦使得隐藏层宽度与扩展基维度 $D$ 独立，允许通过增大 $D$ 灵活提升模型对高频分量的表达能力，而无需增加网络宽度。Table 1 将该框架置于现有方法的全景对比中，突显其在处理高频 PDE 时的理论保证与能力优势。



### 模块架构与因果机制

IFeF-PINN 由四个关键模块串联构成，形成完整的因果链以突破标准 PINN 面临的 **谱偏差瓶颈**（模型倾向于优先学习低频成分，难以捕捉高频振荡解）。

1. **隐藏层特征生成 $h_\omega$**  
   充当“名义基生成器”。输入坐标 $x\in\Omega$ 后，隐藏层输出低维非线性特征向量 $h_\omega(x)\in\mathbb{R}^p$，由参数 $\omega$ 控制。它为后续扩展提供基础非线性映射能力，但其固有的频率偏好仍未解决。

2. **随机傅里叶特征（RFF）扩展 $\psi_D$**  
   这是整个方法的核心因果干预模块。在 $h_\omega(x)$ 上通过映射 $\gamma_D$ 构造高维随机傅里叶特征：
   \[
   \psi_D(x) = \gamma_D\bigl(h_\omega(x)\bigr)
   = \frac{1}{\sqrt{D}}
   \begin{bmatrix}
   \cos\bigl(2\pi \mathbf{B}_D\, h_\omega(x)\bigr) \\[2pt]
   \sin\bigl(2\pi \mathbf{B}_D\, h_\omega(x)\bigr)
   \end{bmatrix},
$$

   其中 $\mathbf{B}_D\in\mathbb{R}^{D\times p}$ 的行向量独立采样自 $\mathcal{N}(0,\sigma^2 I)$。该操作将 $p$ 维特征扩展至 $2D$ 维，通过随机投影将隐藏特征显式转化为大规模高频基函数集合，有效抑制谱偏差，使网络具备逼近高频分量的能力。

3. **线性回归层 $\theta$**  
   解耦训练的核心环节。近似解由扩展基的线性组合给出：
   
$$
u_{\omega,\theta}(x) = \psi_D(x)^\top \theta,\qquad \theta\in\mathbb{R}^{2D}.
$$

   上层（$\omega$）决定基函数空间，下层（$\theta$）仅进行线性回归。对于线性 PDE，下层问题化为凸二次规划，存在唯一全局最优解（Proposition 1），从而避免了传统 PINN 端到端非凸训练的不稳定性和局部最优陷阱。

4. **蒙特卡洛损失函数 $\hat{\mathfrak{L}}_\lambda$**  
   驱动整体架构训练的离散损失：
   
$$
\hat{\mathfrak{L}}_\lambda(u_\omega)
   = \frac{1}{N_u}\sum_{i=1}^{N_u} \big\| g(x_u^i) - \mathfrak{B}[u_\omega](x_u^i) \big\|^2
   + \frac{\lambda}{N_f}\sum_{i=1}^{N_f} \big\| \mathfrak{F}[u_\omega](x_f^i) \big\|^2,
$$

   其中 $N_u$、$N_f$ 分别为边界和内部配点的数量，$\lambda$ 平衡边界与残差损失。

### 双级优化与下层二次形式

上述模块自然引导出迭代交替的双级优化策略：

$$
\omega^\star(\theta) = \arg\min_\omega \hat{\mathfrak{L}}_\lambda(u_{\omega,\theta}),\qquad
\theta^\star(\omega) = \arg\min_\theta \hat{\mathfrak{L}}_\lambda(u_{\omega,\theta}).
$$

上层通过梯度下降更新特征基参数 $\omega$，下层对固定基寻找最优线性回归系数 $\theta$。对于线性 PDE，下层的损失函数恰可整理为 $\theta$ 的二次型：

$$
\mathfrak{L}_{\mathrm{lower}}(\theta \mid \omega)
= \hat{\mathfrak{L}}_\lambda(u_{\omega,\theta})
= \frac{1}{2}\theta^\top Q(\omega)\,\theta + c(\omega)^\top \theta + b,
$$

其中矩阵 $Q(\omega)$ 和向量 $c(\omega)$ 完全由 PDE 的线性微分算子与离散配点生成，常数项 $b$ 与 $\theta$ 无关。下层最优解可通过直接求解线性系统 $Q(\omega)\,\theta = -c(\omega)$ 获得**全局最优**，保证线性 PDE 的逼近精度和训练稳定性（Proposition 1, Theorem 1）。

对于非线性 PDE，$Q$ 将依赖于 $\theta$，下层损失不再保持严格的二次形式，此时仍可借助局部交替优化（Algorithm 2）进行有效求解，只是理论上仅提供局部收敛保证。

### 变量符号速查

- $x$：空间/时间输入坐标，$x\in\Omega$。
- $h_\omega(x)$：隐藏层输出向量，维度 $p$。
- $\mathbf{B}_D$：$D\times p$ 随机矩阵，每行 $\sim \mathcal{N}(0,\sigma^2 I)$；$\sigma$ 控制核的频率带宽。
- $\psi_D(x)\in\mathbb{R}^{2D}$：RFF 扩展后的特征向量（扩展基）。
- $\theta\in\mathbb{R}^{2D}$：线性回归系数。
- $u_{\omega,\theta}(x)$：最终近似解。
- $\mathfrak{F}[u]$、$\mathfrak{B}[u]$：PDE 微分算子与边界/初值算子。
- $N_u, N_f$：边界、内部配点数；$\lambda$：损失平衡权重。
- $Q(\omega), c(\omega)$：下层二次损失的系统矩阵与向量，线性 PDE 下与 $\theta$ 无关，可精确计算。



## 实验与关键发现

实验围绕谱偏差缓解这一核心瓶颈展开验证：标准 PINN 倾向于优先拟合低频分量，导致高频振荡解精度低下。IFeF-PINN 通过在隐藏层输出上施加随机傅里叶特征（RFF）映射 $\psi_D$，将学习解耦为上层基生成与下层凸回归，理论上为线性 PDE 提供全局最优的下层解（Proposition 1）。本节从主结果、消融、高频频谱恢复以及失败模式四个维度考察该机制的有效性。

### 主结果：低频与高频 PDE 的对比

在三个低频基准（Helmholtz、Convection、Reaction）上，IFeF-PINN 及其变体 IFeF-PD 的中位相对 $L^2$ 误差比传统 PINN、PINNsformer 与 NTK 低约 1–2 个数量级（Figure 2）。例如，IFeF-PD 在低频 Helmholtz 方程上取得 $3.5\times10^{-5}$ 的中位误差，而多数基线方法的中位数高于 $10^{-3}$。Figure 3 进一步显示，IFeF 的绝对误差在整个空间域呈现均匀低值，而基线方法在边界或振荡区域残存明显偏差。

高频场景更能揭示谱偏差的破坏性：Table 2 报告了三类高频 PDE 的平均相对 $L^2$ 误差。对于 $a_1=a_2=100$ 的高频 Helmholtz 方程，IFeF 达到 $0.0156 \pm 0.0055$，而 Vanilla PINN、PINNsformer 和 NTK 均无法收敛（标记为‘-’）。在 $\beta=200$ 的高频 Convection 方程与多尺度 Convection-Diffusion 方程上，IFeF 分别取得 $0.0027 \pm 0.0010$ 和 $0.0009 \pm 0.0003$，相较于收敛的 PIG 基线也具备显著优势。Figure 4 的可视化证实，IFeF 能较好地重建高频波形细节，而其他方法的预测要么失稳发散，要么过度平滑。


![[assets/figures/papers/iclr26_0013_ybffyf7LE7_Iterative_Training_of_Physics-Informed_Neural_Ne/figures/005_Table_2.jpg]]
*Table 2: Average relative L ^ { 2 } . -error with corresponding standard deviation for each baseline on three high-frequency PDEs. A dash ’-’ denotes that the baseline failed to converge*

### 消融实验

**RFF 基扩展的必要性**：移除 $\psi_D$ 映射（即将上层隐藏层输出直接作为 $\theta$ 的线性回归特征）导致低频 Convection 方程的相对 $L^2$ 误差升至 $1.4923\times10^{-2}$（Section 6.1），远高于 IFeF 的 $4.3\times10^{-5}$。这表明单独依赖网络隐藏层特征不足以对抗谱偏差，RFF 高维投影带来的频率扩容是关键。

**两阶段训练 vs. 端到端训练**：Table 3 对比了 IFeF 双级联训练与端到端联合优化（均保留 $\psi_D$）。在线性 Helmholtz 方程（$a_1=1,a_2=4$）上，端到端训练的误差为 $8.8\times10^{-3}$，而 IFeF 降至 $3.0\times10^{-4}$，改善逾一个数量级；对于 $a_1=1,a_2=15$ 的设置，端到端方法直接无法收敛。非线性 Burgers 方程中，两阶段训练仍将误差从 $4.9\times10^{-3}$ 压低至 $2.4\times10^{-3}$。在线性 PDE 上获得的巨大收益来源于下层凸二次规划能给出全局最优系数 $\theta=-Q^{-1}c$，而端到端梯度下降易陷入非凸景观的局部极小。


![[assets/figures/papers/iclr26_0013_ybffyf7LE7_Iterative_Training_of_Physics-Informed_Neural_Ne/figures/008_Table_3.jpg]]
*Table 3: tions. This ablation validates the necessity of two-stage training, as IFeF-PINN significantly outperforms end-to-end training in linear PDEs through guaranteed lower-level optimality of θ, while showing modest improvements in nonlinear PDEs where the lower-level becomes non-convex. Table 3: Average relative $L ^ { 2 } { \mathrm { - e r r o r } }$ with corresponding standard deviation for end-to-end training and IFeF-PINN on three benchmarks. A dash ’-’ denotes that the baseline failed to converge*

**超参数 $D$ 和 $\sigma$ 的影响**：Table 4 展示了 RFF 维度 $D$ 与随机投影尺度 $\sigma$ 在两类 Helmholtz 问题上的消融。低频情况下，$\sigma=1$ 且 $D=400$ 获取最低误差 $2.1\times10^{-4}$；若 $\sigma$ 降至 $0.1$，误差急剧恶化至 $1.5\times10^{-3}$。高频情形下，需增大 $D$（如 $1600$）并选择合适 $\sigma$ 才能维持精度。频谱分析（Figure 5）从频域角度佐证：随着 $D$ 从 $200$ 增至 $800$，网络在高频区间的归一化幅度逐渐提升，说明 RFF 基的扩充有效增强了网络对高频分量的表达能力，从而直接缓解谱偏差。


![[assets/figures/papers/iclr26_0013_ybffyf7LE7_Iterative_Training_of_Physics-Informed_Neural_Ne/figures/007_Figure_5.jpg]]
*Figure 5: Prediction of the network spectrum with an increasing number of Fourier features. The x-axis represents frequency, and the colorbar shows the normalized magnitude of the predicted solution at t = 0 . . The colorbar is scaled accordingly from 0 to 1*

![[assets/figures/papers/iclr26_0013_ybffyf7LE7_Iterative_Training_of_Physics-Informed_Neural_Ne/figures/009_Table_4.jpg]]
*Table 4: Average relative $L ^ { 2 } \mathrm { - e r r o r }$ for hyperparameter ablation for D and σ on Helmholtz equations*

### 失败模式与讨论

尽管 IFeF-PINN 在多数基准中表现优异，其有效性受制于若干内部条件：

- **非线性 PDE 的下层非凸性**：对于非线性方程，$\hat{\mathfrak{L}}_{\lambda}$ 不再是 $\theta$ 的二次型，双级联优化只能收敛至局部稳定点，性能提升有限（如 Burgers 方程上仅将误差减半）。无法保证全局最优是方法向非线性问题泛化的主要障碍。
- **计算开销**：精确求解线性 PDE 的下层问题需计算矩阵逆 $Q^{-1}$，内存和计算量随 $D$ 二次增长，限制了其在极大规模问题上的应用。
- **超参数敏感性**：$\sigma$ 和 $D$ 需针对问题单独调优，尤其在高频或强非线性情形下，不当选择可导致发散或严重退化。实验未提供自动选取策略。
- **未融合自适应采样**：当前方法依赖固定均匀采样，当解存在局部陡峭区域时，样本效率不足可能削弱收敛性。

综上，IFeF-PINN 通过 RFF 基扩展与双级联凸回归，显著缓解了标准 PINN 的谱偏差，在线性 PDE 上获得接近数值方法的精度，并在高频基准上将无法收敛的基线转变为可解问题。其失效主要源于非线性 PDE 的非凸下层、高内存占用以及超参数选择挑战，这些方向仍有待进一步研究。



## 定位与知识库关联

### 与现有方法的关系及优势

标准物理信息神经网络 (PINN) 在训练时存在**谱偏差 (spectral bias)**，即倾向于优先学习低频成分，难以拟合高频振荡解，导致数值精度不足。本文提出的 IFeF-PINN 通过在隐藏层输出上施加随机傅里叶特征 (Random Fourier Features, RFF) 映射，将特征空间扩展为高维基 $\psi_D$，并采用双层级联优化训练（上层学习基函数参数 $\omega$，下层求解线性回归系数 $\theta$），有效缓解谱偏差，显著提升对高频成分的逼近能力 (ABSTRACT, Section 1)。

相较于既有方法，IFeF-PINN 的方案有三处**关键区别**（详见 Table 1 的方法对比）：

- **特征增强方式**：标准 PINN 仅利用神经网络隐藏层输出作为特征；IFeF-PINN 在最后一层隐藏层后插入 RFF 映射 $\psi_D(x)=\gamma_D\left(h_\omega(x)\right)$，生成与网络宽度解耦的大规模扩展基，从而为下层提供丰富的基函数集合 (Section 3.1, Equation (5))。
- **训练优化架构**：传统端到端训练对所有参数进行联合梯度下降，损失函数非凸；IFeF-PINN 解耦为上层（非线性参数 $\omega$）和下层（线性参数 $\theta$）。对于线性 PDE，下层问题构成**凸二次规划** $\mathfrak{L}_{\mathrm{lower}}(\theta\mid\omega) = \frac12 \theta^\top Q(\omega)\theta + c(\omega)^\top\theta + b$，可求得**全局最优解** $\theta = -Q^{-1}c$ (Proposition 1, Section 3.2)，避免了非凸优化的次优解。
- **对非线性 PDE 的适应**：面对非线性 PDE，下层问题非凸，方法改用基于梯度下降的局部双层迭代 (Algorithm 2)，交替更新 $\theta$ 和 $\omega$，在实际中仍能获得优于端到端训练的精度 (Table 3)。

在实验基准上，IFeF-PINN 与多个基线方法进行了系统对比。在低频 Helmholtz、对流和反应方程上，IFeF 及 IFeF-PD 的相对 $L^2$ 误差中位数约在 $10^{-4}$ 量级，比 Vanilla PINN、PINNsformer、NTK、PIG 等方法低 1–2 个数量级 (Figure 2)。高频基准 (Table 2) 进一步凸显优势：当标准 PINN、PINNsformer 和 NTK 在 $a_1=a_2=100$ 的 Helmholtz、$\beta=200$ 的对流以及多尺度对流‑扩散方程上无法收敛时，IFeF-PINN 依然能以平均相对 $L^2$ 误差 0.0156、0.0027 和 0.0009 稳定求解。消融实验 (Table 3) 验证了双级联训练的必要性：去除 RFF 扩展后，端到端训练在低频对流上误差升至 $1.49\times10^{-2}$，远高于 IFeF 的结果；而在线性 PDE 上双级联训练因下层最优性保证了大幅领先。

### 适用边界与局限

IFeF-PINN 的设计在以下方面存在明确边界：

- **线性 PDE vs. 非线性 PDE**：全局最优性仅在线性 PDE 下层构成凸二次规划时成立 (Proposition 1)。对非线性 PDE，下层为非凸优化，可能陷入局部极小，导致性能提升有限，且缺乏理论收敛保证 (Section 3.4, limitations)。
- **超参数敏感度**：RFF 的特征维度 $D$ 和映射超参数 $\sigma$ 对结果影响显著。消融实验 (Table 4) 表明，在低频 Helmholtz 方程上，$\sigma=0.1$ 时误差为 $1.5\times10^{-3}$，而 $\sigma=1$ 时降至 $2.1\times10^{-4}$；高频场景对 $\sigma$ 更为敏感，需针对具体问题仔细调参。
- **计算和内存开销**：扩展基的维度 $D$ 通常较大，导致内存占用高，尤其当 $D$ 增大以捕捉更高频成分时 (Figure 5)。另外，线性 PDE 的精确求解涉及矩阵求逆，限制了在极大维度问题上的可扩展性。
- **训练效率与自适应采样**：目前方法未整合自适应重采样技术，训练点均匀随机采样，可能在某些区域浪费计算，整体训练效率有待提升 (limitations)。
- **几何与维度**：实验均在规则域上开展，对于复杂几何或高维 PDE（如 100 维以上），RFF 扩展基的有效性和内存可行性尚不明确。

### 开放问题

基于当前工作的限制，可提炼出若干值得推进的方向：

- **非线性 PDE 的双层收敛理论**：如何将凸性的优势通过二阶信息或全局优化策略引入非线性下层，从理论上保证收敛到更优解，是核心挑战 (open questions, Section 7)。
- **与自适应采样结合**：将 IFeF-PINN 与自适应采样方法（如 PINNACLE）融合，针对高残差区域动态加密采样点，有望进一步提升训练效率和求解精度。
- **高维扩展**：该方法能否直接应用于高维偏微分方程，以及如何应对维度灾难，需要理论和实验验证。
- **内存优化**：通过特征选择、低秩近似或稀疏回归等技术降低 $D$ 的规模，可使方法在更大规模问题上实用。
- **非规则域上的泛化**：针对复杂几何或含异构边界条件的问题，RFF 扩展基是否仍保持有效表达能力，有待进一步研究。

综上，IFeF-PINN 在缓解 PINN 谱偏差方面展现了清晰的机理和有效的实践方案，但其适用边界和限制也为后续改进指明了方向。对于线性 PDE，它提供了目前最优的精度保证；对于非线性情形，该框架提供了一个灵活且可扩展的基线，亟待更深入的优化技术来释放其全部潜力。



## 原文 PDF

![[paperPDFs/ICLR_2026/Iterative_Training_of_Physics_Informed_Neural_Networks_with_Fourier_enhanced_Features.pdf]]
