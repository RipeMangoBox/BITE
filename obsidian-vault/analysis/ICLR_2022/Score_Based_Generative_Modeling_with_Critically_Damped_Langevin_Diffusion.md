---
title: "Score-Based Generative Modeling with Critically-Damped Langevin Diffusion"
type: paper
paper_level: A
venue: ICLR
year: 2022
pdf_ref: paperPDFs/ICLR_2022/Score_Based_Generative_Modeling_with_Critically_Damped_Langevin_Diffusion.pdf
code_link: null
project_link: https://research.nvidia.com/labs/toronto-ai/CLD-SGM/
aliases:
- CDLDCSSCSS
- SBGMCDLD
tags:
- ICLR_2022
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: "通过引入临界阻尼朗之万扩散（CLD），在联合数据-速度空间中运行扩散，噪声仅注入速度变量，使模型只需学习条件速度得分而非直接数据得分，从而简化学习任务。"
primary_logic: "基于统计力学，CLD利用哈密顿动力学实现更平滑的扩散，使得分函数更接近正态分布，进而可以设计更高效的SDE积分器（SSCS）进行采样，整体提升生成质量。"
claims:
- "CLD-based SGM在CIFAR-10上实现了FID 2.25（概率流ODE）和2.23（生成SDE），优于先前扩散模型。"
- "SSCS采样器在有限NFE预算下显著优于Euler-Maruyama。"
- "CLD学习的得分函数比VPSDE更接近正态分布，且训练得到的神经网络更平滑。"
- "混合得分参数化和HSM训练对CLD性能至关重要（FID从3.56提升至3.14）。"
---

# Score-Based Generative Modeling with Critically-Damped Langevin Diffusion

> [!tip] 核心洞察
> 基于统计力学，CLD利用哈密顿动力学实现更平滑的扩散，使得分函数更接近正态分布，进而可以设计更高效的SDE积分器（SSCS）进行采样，整体提升生成质量。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 基于临界阻尼朗之万扩散的得分生成建模 |
| 英文题名 | Score-Based Generative Modeling with Critically-Damped Langevin Diffusion |
| 会议/期刊 | ICLR 2022 |
| Links | [paper](https://arxiv.org/abs/2112.07068) · [Project](https://nv-tlabs.github.io/CLD-SGM) · [Project](https://research.nvidia.com/labs/toronto-ai/CLD-SGM/) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | Critically-Damped Langevin Diffusion (CLD) with Symmetric Splitting CLD Sampler (SSCS) |
| Dataset | CIFAR-10 (unconditional) |

> [!tip] 效果简介
> - CIFAR-10 (unconditional) 上，FID 为 2.25 (Prob. Flow ODE)，对比 4.60 (LSGM-100M)，变化 -2.35。
> - CIFAR-10 (unconditional) 上，FID 为 2.23 (Generative SDE, EM-QS)，对比 2.20 (reported by Song et al., 2021c for VPSDE)，变化 +0.03。
> - CIFAR-10 (unconditional) 上，FID 为 3.07 (SSCS-QS, n=150)，对比 7.00 (EM-QS, n=150)，变化 -3.93。

## 概要

**核心问题**：现有得分生成模型（Score-based Generative Models, SGMs）普遍采用过于简化的扩散过程（如 Variance-Preserving SDE, VPSDE），导致前向扩散与逆向去噪之间的任务复杂度不匹配——模型需要直接学习高维数据空间的得分函数，使得训练和采样均面临不必要的困难。

**核心发现**：本文提出**临界阻尼朗之万扩散（Critically-Damped Langevin Diffusion, CLD）**，将扩散过程从数据空间拓展到联合数据-速度空间。关键机制在于：噪声仅注入速度变量，数据仅通过哈密顿耦合间接受到扰动，从而将得分学习任务从“学习数据得分 $\nabla_{\mathbf{x}_t} \log p_t(\mathbf{x}_t)$”简化为“学习条件速度得分 $\nabla_{\mathbf{v}_t} \log p_t(\mathbf{v}_t|\mathbf{x}_t)$”。统计力学分析表明，CLD 的得分函数更接近正态分布的得分，使得神经网络更平滑、更易训练。

**方法定位**：CLD 属于扩散生成模型谱系中的**扩散过程设计**分支，与 VPSDE（Song et al., 2021c）等过阻尼朗之万动力学方法形成对比。其配套技术包括：
- **混合得分匹配（Hybrid Score Matching, HSM）**：解析处理初始速度分布，避免 $t \to 0$ 时得分无界问题；
- **混合得分参数化（Mixed Score Parameterization）**：将得分模型分解为正态基项与残差校正；
- **对称分裂 CLD 采样器（Symmetric Splitting CLD Sampler, SSCS）**：利用 Fokker-Planck 算子分裂实现高效积分，在有限 NFE 预算下显著优于 Euler-Maruyama。

**主要结果**：在 CIFAR-10 无条件生成任务上，CLD-SGM 使用概率流 ODE 达到 FID 2.25，使用生成 SDE 达到 FID 2.23，优于同等参数量（约 100M）的 LSGM 基线（FID 4.60）。消融实验证实：混合得分参数化将 FID 从 3.56 降至 3.14，HSM 训练是稳定训练的关键要素，而质量参数 $M^{-1}$ 和初始速度方差 $\gamma$ 在合理范围内对性能影响较小（FID 波动 ≤ 0.13）。

**局限与展望**：当前验证限于图像生成任务；SSCS 仅支持固定步长；尚未与 DDIM 等非马尔可夫加速采样技术结合。未来方向包括引入其他统计力学恒温器方法、扩展自适应步长积分器，以及探索 CLD 在最大似然训练和跨模态生成中的应用。



### 得分生成模型的范式与瓶颈

得分生成模型（Score-based Generative Models, SGMs）通过逐步向数据注入高斯噪声构建扩散过程，并学习逆转该过程以生成新样本。其核心思想是训练一个神经网络来逼近不同噪声水平下扰动数据的得分函数 $\nabla_{\mathbf{x}_t} \log p_t(\mathbf{x}_t)$，而后通过求解逆向随机微分方程（SDE）实现采样。

现有 SGM 框架普遍采用**过阻尼朗之万动力学**所对应的扩散过程，其中最具代表性的是 **VPSDE**（variance-preserving SDE, Song et al., 2021c）。该过程直接在数据空间 $\mathbf{x}_t$ 中演化，噪声同时作用于数据的所有维度。这种设计虽然简洁，却导致了一个根本性问题：**去噪任务被不必要地复杂化**。随着扩散进行，数据分布逐渐趋近于正态分布，但在 VPSDE 框架下，网络需要学习完整数据空间的得分函数 $\nabla_{\mathbf{x}_t} \log p_t(\mathbf{x}_t)$，这一目标在低噪声阶段尤为困难——得分函数在 $t \to 0$ 时可能出现无界行为，使训练不稳定。

### 从统计力学视角审视扩散设计

上述瓶颈的根源在于扩散过程本身的选择。统计力学中，朗之万动力学描述了粒子在热浴中的运动，其阻尼系数决定了系统的收敛特性：

- **过阻尼**（overdamped）：速度变量被绝热消除，系统仅在一阶数据空间中演化，对应 VPSDE 等现有扩散过程。
- **欠阻尼**（underdamped）：数据与速度耦合振荡，收敛缓慢。
- **临界阻尼**（critically-damped）：系统以最快速度收敛至平衡态，无振荡。

作者观察到，**临界阻尼朗之万扩散（CLD）** 在哈密顿力学框架下，将数据 $\mathbf{x}_t$ 与辅助速度变量 $\mathbf{v}_t$ 耦合，在联合空间 $(\mathbf{x}_t, \mathbf{v}_t)$ 中运行扩散过程，且**噪声仅注入速度通道**。这一设计具有双重优势：一方面，哈密顿项 $\beta M^{-1} \mathbf{v}_t$ 和 $-\beta \mathbf{x}_t$ 提供数据与速度之间的确定性耦合，使扩散轨迹更平滑；另一方面，噪声仅作用于速度变量意味着联合得分函数可简化为条件速度得分：

$$\nabla_{\mathbf{v}_t} \log p_t(\mathbf{u}_t) = \nabla_{\mathbf{v}_t} \log p_t(\mathbf{v}_t | \mathbf{x}_t)$$

神经网络只需学习条件分布 $p_t(\mathbf{v}_t | \mathbf{x}_t)$ 的得分，而非直接估计数据得分。由于该条件分布在 CLD 扩散下更接近正态分布，学习任务被显著简化。实证分析（Figure 2）表明：CLD 学习的得分函数与正态分布得分之间的差异 $\xi(t)$ 在所有时间步 $t \in [0, T]$ 上均小于 VPSDE，且训练所得神经网络的雅可比矩阵 Frobenius 范数更低，即网络本身更平滑、更易训练。

### 本文动机与核心主张

基于上述观察，本文提出将**临界阻尼朗之万扩散**作为 SGMs 的新型扩散过程，并围绕这一选择构建完整的训练与采样框架。核心动机可归纳为三点：

1. **简化学习目标**：利用 CLD 的条件速度得分特性，将高维数据空间的得分估计问题转化为更低复杂度的条件分布建模问题。
2. **提升生成质量**：通过更平滑的扩散轨迹和更接近正态的得分函数，使模型在相同架构和采样预算下获得更优的生成性能。
3. **设计高效采样器**：基于 CLD 的 Fokker-Planck 算子结构，开发对称分裂积分器（SSCS），充分利用可解析的哈密顿-OU 部分，在有限 NFE 预算下显著优于通用 Euler-Maruyama 方法。

这一思路将统计力学中成熟的动力学理论引入深度生成模型，为扩散过程的设计空间提供了新的自由度——阻尼系数、质量参数、初始速度分布等均可作为可调节的归纳偏置，而非局限于传统过阻尼范式。



## 核心方法与创新机理

本工作针对得分生成模型（SGM）中扩散过程设计过于简单、导致去噪任务不必要的复杂化这一瓶颈，提出**临界阻尼朗之万扩散（Critically-Damped Langevin Diffusion, CLD）**作为新的前向扩散过程。核心创新体现在以下四个紧密耦合的维度：

### 1. 扩散空间升维：从数据空间到联合数据-速度空间

传统 SGM（如 VPSDE，Song et al., 2021c）直接在数据空间 $\mathbf{x}_t \in \mathbb{R}^d$ 上运行过阻尼朗之万扩散，噪声直接注入数据变量。CLD 的核心操作是将数据变量 $\mathbf{x}_t$ 与辅助速度变量 $\mathbf{v}_t \in \mathbb{R}^d$ 耦合，在 $2d$ 维联合空间 $\mathbf{u}_t = (\mathbf{x}_t, \mathbf{v}_t)$ 中运行扩散过程，且**噪声仅注入速度通道**：

$$
\begin{array}{rl}
\left( d \mathbf{x}_t \\ d \mathbf{v}_t \right) = \underbrace{\left( \begin{array}{c} M^{-1} \mathbf{v}_t \\ -\mathbf{x}_t \end{array} \right) \beta dt}_{\text{Hamiltonian component}} + \underbrace{\left( \begin{array}{c} \mathbf{0}_d \\ -\Gamma M^{-1} \mathbf{v}_t \end{array} \right) \beta dt + \left( \begin{array}{c} 0 \\ \sqrt{2\Gamma\beta} \end{array} \right) d\mathbf{w}_t}_{\text{Ornstein-Uhlenbeck process}}
\end{array}
$$

该 SDE 由哈密顿项（数据与速度的保守耦合）和奥恩斯坦-乌伦贝克项（速度的耗散与随机驱动）组成。设定阻尼满足 $\Gamma^2 = 4M$ 即得到临界阻尼条件，此时系统以最快且无振荡的方式收敛到稳态（见 Figure 5）。数据变量仅通过哈密顿耦合间接受到扰动，避免了直接噪声注入带来的分布畸变。

### 2. 学习目标简化：从数据得分到条件速度得分

扩散空间的变化直接改变了得分模型需要学习的目标。由于噪声仅作用于 $\mathbf{v}_t$，联合分布的得分函数退化为条件速度得分：

$$
\nabla_{\mathbf{v}_t} \log p_t(\mathbf{u}_t) = \nabla_{\mathbf{v}_t} \log p_t(\mathbf{v}_t|\mathbf{x}_t)
$$

这意味着神经网络 $s_\theta(\mathbf{u}_t, t)$ 只需学习给定数据的条件速度分布得分，而非直接学习数据空间的得分函数。实证分析（Figure 2）表明：CLD 下的条件速度得分与正态分布得分的差异 $\xi(t)$ 显著小于 VPSDE 下数据得分与正态得分的差异；同时，CLD 训练的得分网络雅可比矩阵 Frobenius 范数在大部分时间步上更低，表明网络更平滑、更易训练。

### 3. 训练方法创新：混合得分匹配与混合得分参数化

为稳定训练 CLD-SGM，作者提出了两项互补技术：

**混合得分匹配（Hybrid Score Matching, HSM）**：标准去噪得分匹配（DSM）在 $t \to 0$ 时面临得分无界问题（见 Figure 6 中 $\ell_t^{\text{DSM}}$ 的发散行为）。HSM 通过解析地边际化初始速度分布 $p(\mathbf{v}_0|\mathbf{x}_0) = \mathcal{N}(\mathbf{0}, \gamma M I_d)$，将训练目标重写为：

$$
\operatorname*{min}_{\theta} \mathbb{E}_{t\in[0,T]} \mathbb{E}_{\mathbf{x}_0\sim p_0(\mathbf{x}_0)} \mathbb{E}_{\mathbf{u}_t\sim p_t(\mathbf{u}_t|\mathbf{x}_0)} \left[ \lambda(t) \| s_{\theta}(\mathbf{u}_t, t) - \nabla_{\mathbf{v}_t} \log p_t(\mathbf{u}_t|\mathbf{x}_0) \|_2^2 \right]
$$

这使得 $\ell_t^{\text{HSM}}$ 在 $t \to 0$ 时保持有界（Figure 6 绿线），避免了训练不稳定。

**混合得分参数化（Mixed Score Parameterization）**：将得分模型显式分解为正态得分基项与可训练的残差校正：

$$
s_\theta(\mathbf{u}_t, t) = -\ell_t \, \alpha_\theta(\mathbf{u}_t, t)
$$

其中 $\ell_t$ 由解析协方差矩阵导出，$\alpha_\theta$ 为神经网络预测的残差。该参数化使网络只需学习与正态分布的偏差，进一步降低了学习难度。消融实验表明：使用混合得分参数化将 CIFAR-10 FID 从 3.56 提升至 3.14（Table 4 上下文）。

### 4. 采样器创新：对称分裂 CLD 采样器（SSCS）

CLD 的逆向合成 SDE 可分解为可解析求解的 $\mathcal{L}_A^*$（哈密顿 + OU 项）和需要近似的 $\mathcal{L}_S^*$（得分项）。SSCS 采用对称 Strang 分裂策略：

$$
e^{t(\hat{\mathcal{L}}_A^* + \hat{\mathcal{L}}_S^*)} \approx \left[ e^{\frac{\delta t}{2}\hat{\mathcal{L}}_A^*} e^{\delta t\hat{\mathcal{L}}_S^*} e^{\frac{\delta t}{2}\hat{\mathcal{L}}_A^*} \right]^N
$$

其中 $\mathcal{L}_A^*$ 的传播子具有闭式解（线性高斯系统），$\mathcal{L}_S^*$ 通过单步欧拉近似处理。相比 Euler-Maruyama（EM）对整个 SDE 做一阶近似，SSCS 将精确可解部分与近似部分分离，在有限 NFE 预算下显著提升采样质量：在 CIFAR-10 上，SSCS-QS（n=150）FID 为 3.07，而 EM-QS 为 7.00（Table 2）。

### 创新点间的因果链路

上述四个创新形成闭环：**CLD 扩散过程**（创新 1）使学习目标退化为条件速度得分（创新 2），降低了得分函数的固有复杂度；**HSM 训练与混合得分参数化**（创新 3）解决了该目标在 $t \to 0$ 时的无界问题并进一步简化网络学习任务；**SSCS 采样器**（创新 4）利用 CLD 扩散的线性可解结构，实现了比通用 EM 方法更高效的逆向积分。这一设计链条最终使 CLD-SGM 在 CIFAR-10 上达到 FID 2.25（概率流 ODE）和 2.23（生成 SDE），优于同等参数量下的先前扩散模型。



CLD-SGM 的整体框架围绕“在联合数据-速度空间中扩散”这一核心思想构建，由四个紧密耦合的模块构成：**临界阻尼朗之万扩散过程（CLD）**、**混合得分匹配训练（HSM）**、**混合得分参数化** 以及 **对称分裂 CLD 采样器（SSCS）**。

### Pipeline 总览

整个生成建模流程分为训练与采样两个阶段，其数据流与模块关系如下：

**训练阶段**：从数据分布 $p_0(\mathbf{x}_0)$ 采样真实数据 $\mathbf{x}_0$，同时从初始速度分布（通常为高斯分布 $\mathcal{N}(\mathbf{0}, \gamma M \mathbf{I}_d)$）采样初始速度 $\mathbf{v}_0$，构成联合状态 $\mathbf{u}_0 = (\mathbf{x}_0, \mathbf{v}_0)$。前向 CLD 扩散过程将 $\mathbf{u}_0$ 演化为 $\mathbf{u}_t = (\mathbf{x}_t, \mathbf{v}_t)$，其核心特性是**噪声仅注入速度变量**，数据变量仅通过与速度的哈密顿耦合间接受到扰动。HSM 训练目标以解析方式处理初始速度分布的期望，避免了标准去噪得分匹配（DSM）在 $t \to 0$ 时出现的无界得分问题。神经网络 $s_\theta(\mathbf{u}_t, t)$ 通过混合得分参数化——由一个正态得分基项与可训练的残差校正 $\alpha_\theta$ 组成——学习条件速度得分 $\nabla_{\mathbf{v}_t} \log p_t(\mathbf{v}_t|\mathbf{x}_t)$。

**采样阶段**：从先验分布 $p_T(\mathbf{u}_T)$（近似为高斯分布）采样初始联合状态，然后通过逆向 SDE 逐步去噪。SSCS 采样器利用 Fokker-Planck 算子的对称 Trotter/Strang 分裂，将可解析求解的哈密顿项与 OU 项（A 部分）与需要神经网络近似的得分项（S 部分）交替组合，以固定步长高效积分逆向 SDE，最终从 $\mathbf{x}_0$ 的边际分布生成样本。

### 关键设计决策与因果机制

框架设计的核心因果链可概括为：**扩散过程的物理启发性选择 → 得分学习任务的简化 → 采样器的高效设计 → 生成性能的整体提升**。

1. **临界阻尼条件（$\Gamma^2 = 4M$）** 是连接统计力学与生成建模的关键设计。在此条件下，朗之万动力学以最快且无振荡的方式收敛至平衡态，使得扩散轨迹更为平滑，进而导致条件速度得分 $\nabla_{\mathbf{v}_t} \log p_t(\mathbf{v}_t|\mathbf{x}_t)$ 更接近正态分布的得分。实证证据表明，CLD 的得分与正态分布得分的差异 $\xi(t)$ 显著低于 VPSDE，且得分网络的雅可比 Frobenius 范数更小（Figure 2），验证了“神经网络更平滑、学习任务更简单”的核心洞察。

2. **HSM 训练目标** 是 CLD 稳定训练的使能器。标准 DSM 在 $t \to 0$ 时面临得分无界的问题，而 HSM 通过对初始速度分布解析求期望，将训练目标转化为可重参数化的噪声预测形式。消融实验证实，HSM 对 CLD 性能至关重要（FID 从 3.56 提升至 3.14），且混合得分参数化进一步贡献了约 0.4 的 FID 增益。

3. **SSCS 采样器** 利用 CLD 逆向 SDE 的结构特性——哈密顿项与 OU 项可解析求解，仅得分项需神经网络近似——通过算子分裂实现高效积分。在有限 NFE 预算下，SSCS 显著优于 Euler-Maruyama（例如在 150 步时 FID 为 3.07 vs 7.00），这源于 SSCS 对可解析部分的精确处理避免了 EM 的离散化误差累积。

### 模块间的输入输出关系

| 模块 | 输入 | 输出 | 关键约束 |
|------|------|------|----------|
| CLD 扩散过程 | 初始联合状态 $(\mathbf{x}_0, \mathbf{v}_0)$，时间 $t$ | 扩散后的联合状态 $(\mathbf{x}_t, \mathbf{v}_t)$ | 噪声仅作用于 $\mathbf{v}_t$；临界阻尼条件 $\Gamma^2=4M$ |
| HSM 训练 | 扩散状态 $\mathbf{u}_t$，噪声 $\epsilon_{2d}$，时间 $t$ | 损失值（噪声预测误差） | 权重 $\lambda(t) = \ell_t^{-2}$ 用于高质量生成 |
| 混合得分参数化 | 联合状态 $\mathbf{u}_t$，时间 $t$ | 得分 $s_\theta(\mathbf{u}_t, t) = -\ell_t \alpha_\theta(\mathbf{u}_t, t)$ | 正态得分基项解析给定，残差由网络学习 |
| SSCS 采样器 | 先验样本 $\mathbf{u}_T$，得分网络 $s_\theta$，步数 $N$ | 生成样本 $\mathbf{x}_0$ | 固定步长 $\delta t = T/N$；对称分裂保证二阶精度 |

### 与基线方法的根本差异

与 VPSDE（Song et al., 2021c）相比，CLD-SGM 的框架差异体现在三个层面：**扩散空间** 从纯数据空间 $\mathbb{R}^d$ 扩展至联合空间 $\mathbb{R}^{2d}$；**学习目标** 从直接数据得分 $\nabla_{\mathbf{x}_t} \log p_t(\mathbf{x}_t)$ 简化为条件速度得分 $\nabla_{\mathbf{v}_t} \log p_t(\mathbf{v}_t|\mathbf{x}_t)$；**采样动力学** 从过阻尼朗之万方程升级为临界阻尼哈密顿动力学与 OU 过程的耦合。这些设计共同实现了更平滑的扩散轨迹和更高效的采样，使 CLD-SGM 在 CIFAR-10 上以概率流 ODE 达到 FID 2.25，优于参数量相近的 LSGM-100M（FID 4.60）。



### 1. 临界阻尼朗之万扩散（CLD）前向过程

CLD 的核心创新在于将扩散空间从纯数据空间扩展到**数据-速度联合空间**。定义联合状态 $\mathbf{u}_t = (\mathbf{x}_t, \mathbf{v}_t)$，其中 $\mathbf{x}_t \in \mathbb{R}^d$ 为数据变量，$\mathbf{v}_t \in \mathbb{R}^d$ 为辅助速度变量。前向扩散由以下随机微分方程（SDE）描述（见 Eq. (5)）：

$$
\begin{array}{rl}
\left( \begin{array}{c} d \mathbf{x}_t \\ d \mathbf{v}_t \end{array} \right) = &
\underbrace{\left( \begin{array}{c} M^{-1} \mathbf{v}_t \\ -\mathbf{x}_t \end{array} \right) \beta dt}_{\text{Hamiltonian component}} \\
& + \underbrace{\left( \begin{array}{c} \mathbf{0}_d \\ -\Gamma M^{-1} \mathbf{v}_t \end{array} \right) \beta dt + \left( \begin{array}{c} 0 \\ \sqrt{2\Gamma\beta} \end{array} \right) d\mathbf{w}_t}_{\text{Ornstein-Uhlenbeck process}}
\end{array}
$$

**变量含义**：
- $M$：质量参数，控制数据与速度的耦合强度。
- $\Gamma$：摩擦系数，决定速度的耗散速率。
- $\beta$：扩散时间尺度因子。
- $\mathbf{w}_t$：标准维纳过程。
- **哈密顿项**：实现数据 $\mathbf{x}_t$ 与速度 $\mathbf{v}_t$ 的无耗散耦合，使得数据仅通过速度间接受到扰动。
- **奥恩斯坦-乌伦贝克（OU）项**：仅向速度变量注入噪声并施加摩擦耗散，数据变量本身不直接受噪声污染。

**临界阻尼条件**：设定 $\Gamma^2 = 4M$，使系统处于临界阻尼状态。在此条件下，联合分布 $p_t(\mathbf{x}_t, \mathbf{v}_t)$ 的演化轨迹最为平滑，既避免欠阻尼振荡，也避免过阻尼缓慢收敛（见 Figure 5 的阻尼行为对比）。

**关键性质**：由于噪声仅注入速度通道，联合得分函数 $\nabla_{\mathbf{u}_t} \log p_t(\mathbf{u}_t)$ 中数据得分 $\nabla_{\mathbf{x}_t} \log p_t(\mathbf{u}_t)$ 的复杂度被大幅降低。模型仅需学习**条件速度得分**：

$$
\nabla_{\mathbf{v}_t} \log p_t(\mathbf{u}_t) = \nabla_{\mathbf{v}_t} \log p_t(\mathbf{v}_t | \mathbf{x}_t) \quad \text{(Eq. (7))}
$$

实证分析（Figure 2）表明，CLD 的得分函数比 VPSDE 更接近正态分布，且训练得到的神经网络雅可比矩阵 Frobenius 范数显著更低，验证了学习任务的简化。

---

### 2. 混合得分匹配（HSM）训练目标

传统去噪得分匹配（DSM）在 $t \to 0$ 时面临得分函数无界的问题（见 Figure 6 中 $\ell_t^{\text{DSM}}$ 的发散行为），导致训练不稳定。为此，作者提出**混合得分匹配（Hybrid Score Matching, HSM）**，以解析方式处理初始速度分布 $p_0(\mathbf{v}_0 | \mathbf{x}_0) = \mathcal{N}(\mathbf{v}_0; \mathbf{0}_d, \gamma M^{-1} I_d)$，避免对 $\mathbf{v}_0$ 的蒙特卡洛采样及其带来的梯度方差。

HSM 训练目标为（Eq. (8)）：

$$
\operatorname*{min}_{\theta} \mathbb{E}_{t \in [0,T]} \mathbb{E}_{\mathbf{x}_0 \sim p_0(\mathbf{x}_0)} \mathbb{E}_{\mathbf{u}_t \sim p_t(\mathbf{u}_t | \mathbf{x}_0)} \left[ \lambda(t) \| s_{\theta}(\mathbf{u}_t, t) - \nabla_{\mathbf{v}_t} \log p_t(\mathbf{u}_t | \mathbf{x}_0) \|_2^2 \right]
$$

**关键区别**：HSM 的条件得分 $\nabla_{\mathbf{v}_t} \log p_t(\mathbf{u}_t | \mathbf{x}_0)$ 具有闭式解，其方差因子 $\ell_t^{\text{HSM}}$ 在 $t \to 0$ 时保持有界（Figure 6 绿色曲线），从根本上避免了 DSM 的数值不稳定问题。消融实验证实，HSM 是 CLD-SGM 稳定训练的关键要素。

---

### 3. 混合得分参数化（Mixed Score Parameterization）

为进一步提升训练稳定性和生成质量，得分模型 $s_{\theta}(\mathbf{u}_t, t)$ 采用**混合得分参数化**：

$$
s_{\theta}(\mathbf{u}_t, t) = -\ell_t \, \alpha_{\theta}(\mathbf{u}_t, t)
$$

其中 $\ell_t$ 为条件速度分布 $p_t(\mathbf{v}_t | \mathbf{x}_t, \mathbf{x}_0)$ 的标准差因子，$\alpha_{\theta}$ 为神经网络输出的残差校正项。该参数化将得分函数分解为**正态得分基项**（由 $\ell_t$ 编码）与**可训练的残差**（由 $\alpha_{\theta}$ 建模），使得网络只需学习偏离正态分布的部分。

结合 HSM 与重参数化技巧，最终训练目标简化为预测注入速度的噪声分量（Eq. (9)）：

$$
\operatorname*{min}_{\theta} \mathbb{E}_{t \sim \mathcal{U}[0,T]} \mathbb{E}_{\mathbf{x}_0 \sim p_0(\mathbf{x}_0)} \mathbb{E}_{\epsilon_{2d} \sim \mathcal{N}(\mathbf{0}_{2d}, I_{2d})} \left[ \lambda(t) \ell_t^2 \| \epsilon_{d;2d} - \alpha_{\theta}(\mu_t(\mathbf{x}_0) + L_t \epsilon_{2d}, t) \|_2^2 \right]
$$

消融实验表明，混合得分参数化将 CIFAR-10 的 FID 从 3.56 降至 3.14，验证了其有效性。

---

### 4. 对称分裂 CLD 采样器（SSCS）

逆向生成过程需要求解逆向 SDE。CLD 的逆向 SDE 可分解为三个算子（Eq. (10) 上下文）：

- **$\hat{\mathcal{L}}_A^*$**：包含哈密顿项和 OU 项的线性部分，可解析求解。
- **$\hat{\mathcal{L}}_S^*$**：包含得分函数 $\nabla_{\mathbf{v}_t} \log p_t(\mathbf{v}_t | \mathbf{x}_t)$ 的非线性部分，需通过训练好的网络近似。

SSCS 采用**对称 Trotter/Strang 分裂**近似传播子：

$$
e^{t(\hat{\mathcal{L}}_A^* + \hat{\mathcal{L}}_S^*)} \approx \left[ e^{\frac{\delta t}{2}\hat{\mathcal{L}}_A^*} e^{\delta t\hat{\mathcal{L}}_S^*} e^{\frac{\delta t}{2}\hat{\mathcal{L}}_A^*} \right]^N \quad \text{(Eq. (10))}
$$

**算法流程**（Algorithm 1）：
1. 对每一步，先应用半步 $\hat{\mathcal{L}}_A^*$（解析更新数据与速度的线性耦合及 OU 耗散）。
2. 再应用整步 $\hat{\mathcal{L}}_S^*$（仅更新速度，沿得分方向移动）。
3. 最后再应用半步 $\hat{\mathcal{L}}_A^*$。

**优势**：相比 Euler-Maruyama（EM）方法，SSCS 通过解析处理线性部分，在有限 NFE（Number of Function Evaluations）预算下显著降低离散化误差。实验表明，在 NFE=150 时，SSCS-QS 的 FID 为 3.07，而 EM-QS 高达 7.00（Table 2），性能差距随 NFE 减少而急剧扩大。当前 SSCS 仅支持固定步长，自适应步长扩展留待未来工作。



## 实验与关键发现

### 主要生成性能

CLD-SGM 在 CIFAR-10 无条件生成任务上取得了当时领先的 FID 指标。使用概率流 ODE 采样时，CLD-SGM 达到 FID **2.25**；使用生成 SDE 配合自适应步长求解器（EM-QS）时，FID 为 **2.23**（Table 1, Table 3）。这一结果显著优于参数量相近的潜在得分生成模型 LSGM-100M（FID 4.60），并在生成 SDE 模式下与当时最优的 VPSDE 方法（FID 2.20）基本持平。在负对数似然（NLL）方面，CLD-SGM 获得了 ≤3.31 bpd 的上界估计，略高于 LSGM-100M 的 2.96 bpd，但考虑到 CLD 未针对最大似然进行专门优化，这一差距在合理范围内。

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2112_07068/figures/004_Table_1.jpg]]
*Table 1: Unconditional CIFAR-10 generative performance*

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2112_07068/figures/006_Table_2.jpg]]
*Table 2: (right) Performance using adaptive stepsize solvers (ODE is based on probability flow, GGF simulates generative SDE). †: taken from Jolicoeur-Martineau et al. (2021a). LSGM corresponds to the small LSGM-100M model for fair comparison (details in App. E.2.7). Error tolerances were chosen to obtain similar NFEs. Table 3: (bottom) Performance using non-adaptive stepsize solvers (for PC, QS performed poorly). †: 2.23 FID is our evaluation, Song et al. (2021c) reports 2.20 FID. See Tab. 9 in App. F.2 for extended results*

### 采样效率与 SSCS 采样器

SSCS（Symmetric Splitting CLD Sampler）在有限函数评估次数（NFE）预算下展现出对 Euler-Maruyama（EM）方法的显著优势。在非自适应步长设定下，当 NFE=150 时，SSCS-QS 取得 FID **3.07**，而 EM-QS 仅为 7.00，性能差距达 **3.93** 个 FID 单位（Table 2）。这一结果表明，基于 Fokker-Planck 算子对称分裂的 SSCS 能够更高效地利用得分函数评估，在低 NFE 场景下大幅提升采样质量。目前 SSCS 仅支持固定步长，但其在固定步长设定下的表现已足够优秀，自适应步长扩展留待未来工作。

### 消融实验与关键组件验证

**混合得分参数化（Mixed Score）** 是 CLD 性能的关键贡献因素。消融实验表明，使用混合得分参数化将 FID 从 **3.56** 提升至 **3.14**，验证了将得分模型分解为正态得分基项与可训练残差的有效性（Table 4 相关分析）。

**混合得分匹配（HSM）** 被证明是 CLD 稳定训练的必需组件。当使用标准去噪得分匹配（DSM）时，CLD 在 $t \to 0$ 时会出现无界得分问题；HSM 通过解析处理初始速度分布，避免了这一数值不稳定性，是训练成功的关键要素。

**质量参数 $M^{-1}$** 在 1 到 16 范围内对 FID 影响较小（3.23~3.16），表明 CLD 对质量超参数不敏感，具有良好的鲁棒性（Table 4）。**初始速度分布宽度 $\gamma$** 从 0.04 增至 1 时，FID 仅从 3.14 微升至 3.27，进一步验证了方法对先验分布选择的稳健性（Table 5）。

### 得分复杂性与网络平滑性分析

实证分析（Figure 2）揭示了 CLD 优于 VPSDE 的深层原因：CLD 学习的条件速度得分 $\nabla_{\mathbf{v}_t} \log p_t(\mathbf{v}_t|\mathbf{x}_t)$ 与正态分布得分之间的差异 $\xi(t)$ 显著小于 VPSDE 的数据得分对应差异；同时，CLD 训练的得分网络雅可比矩阵 Frobenius 范数在大部分时间步 $t$ 上明显低于 VPSDE，表明 CLD 学习到的神经网络更加平滑简单。这验证了核心假设——将扩散过程从数据空间移至联合数据-速度空间，并使噪声仅作用于速度变量，能够有效降低学习任务的复杂度。

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2112_07068/figures/002_Figure.jpg]]

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2112_07068/figures/021_Figure.jpg]]

### 局限性与失败模式

当前 CLD 的验证范围主要局限于图像生成任务，尚未在语音、视频等其他模态上进行测试。SSCS 采样器目前仅支持固定步长，缺乏自适应步长策略。在最大似然训练场景下，高维图像生成的 CLD 性能尚未充分探索。此外，CLD 尚未与基于 DDIM 等非马尔可夫方法的加速采样技术结合，这可能是进一步提升采样效率的方向。

### 补充图表

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2112_07068/figures/007_Table_5.jpg]]
*Table 5: Initial velocity distribution width*

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2112_07068/figures/008_Figure_5.jpg]]
*Figure 5: Langevin dynamics in different damping regimes. Each pair of visualizations corresponds to the (coupled) evolution of data xt and velocities $\mathbf { v } _ { t }$ . . We show the marginal (red) probabilities and the projections of the (green) trajectories. The probabilities always correspond to the same optimal setting√ $\Gamma = \Gamma _ { \mathrm { c r i t i c a l } } ^ { - }$ (recall that $\Gamma _ { \mathrm { c r i t i c a l } }$ = 2 $\sqrt { M }$ and $\Gamma _ { \mathrm { m a x } }$ = M / ( $\beta$ ( t ) $\delta$ t ) ; see Sec. A.2). The trajectories correspond to different Langevin trajectories run in the different regimes with indicated friction coefficients Γ. We see in (b), that for critical d...

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2112_07068/figures/012_Figure_9.jpg]]
*Figure 9: (a) Difference ξ(t) (via L2 norm) between score of (b) Frobenius norm of Jacobian $\mathcal { I } _ { F }$ ( t ) of the neural diffused data and score of Normal distribution. network defining the score function for different t. Figure 9: Toy experiments for mixture of Normals dataset*

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2112_07068/figures/003_Figure_3.jpg]]
*Figure 3: CIFAR-10 samples. Figure 4: CelebA-HQ-256 samples*

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2112_07068/figures/011_Figure_8.jpg]]
*Figure 8: Conceptual visualization of our new SSCS sampler and comparison to Euler-Maruyama (for image synthesis): (a) In EM-based sampling, in each integration step the entire SDE is integrated using an Euler-based approximation. This can be formally expressed as solving the full-step propagator exp $\left\{ \delta$ t ( $\hat { \mathcal { L } } _ { A } ^ { * } + \hat { \mathcal { L } } _ { S } ^ { * } ) \right\}$ via Euler-based approximation for N small steps of size δt (see red steps; for simplicity, this visualization assumes constant $\delta$ t ) . (b): In contrast, in our SSCS the propagator is partitioned into an analytically tractable component exp $\left\{ \frac { \delta t } { 2 } \hat { \mathcal {...$

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2112_07068/figures/040_Figure_17.jpg]]
*Figure 17: Samples generated by our model on the CelebA-HQ-256 dataset using a Runge–Kutta 4(5) adaptive ODE solver to solve the probability flow ODE. We show the effect of the ODE solver error tolerance on the quality of samples ((a), (b), (c) and (d) were generated using the same prior samples). Little visual differences can be seen between 1 0 ^ { - 5 } and 1 0 ^ { - 4 } . Low frequency artifacts can be observed at 1 0 ^ { - 3 } . Deterioration starts to set in at 1 0 ^ { - 2 }*

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2112_07068/figures/005_Table_4.jpg]]
*Table 4: and, for example, potentially test our method within a framework like GGF. Our current SSCS only allows for fixed step sizes—nevertheless, it achieves excellent performance. Table 4: Mass hyperpa*

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2112_07068/figures/018_Table_6.jpg]]
*Table 6: Model architectures as well as SDE and training setups for our experiments on CIFAR-10 and CelebA-HQ-256*



## 定位与知识库关联

### 1. 方法谱系：从过阻尼到临界阻尼的范式迁移

**核心瓶颈与因果转折**。先前得分生成模型（SGM）普遍采用**过阻尼朗之万动力学**的扩散过程，如VPSDE（Song et al., 2021c）直接在数据空间注入噪声。这种做法导致两个深层问题：其一，模型必须学习完整的数据得分函数 ∇_{x_t} log p_t(x_t)，这是一个高度复杂且远离正态分布的目标；其二，扩散轨迹的平滑性受限，限制了后续采样器的积分效率。CLD的提出正是针对这一瓶颈的因果干预——通过引入**临界阻尼朗之万扩散**，将扩散过程从数据空间迁移到联合数据-速度空间，噪声仅注入速度变量，从而将学习目标简化为条件速度得分 ∇_{v_t} log p_t(v_t|x_t)。这一转变的物理直觉来自统计力学中的哈密顿动力学：数据与速度通过耦合项相互演化，噪声仅作用于速度通道，使扩散轨迹更平滑，得分函数更接近正态分布。

**与VPSDE的结构性对比**。在VPSDE框架下，前向扩散直接扰动数据，逆向去噪需要神经网络拟合高度非线性的数据得分。CLD则通过增广变量改变了这一学习范式：前向SDE由哈密顿项和Ornstein-Uhlenbeck项组成，前者描述数据与速度的保守耦合，后者向速度注入噪声并施加阻尼。临界阻尼条件 Γ² = 4M 确保了轨迹以最快且无振荡的方式收敛至稳态，这一定性差异在Figure 5中通过不同阻尼条件下的轨迹行为得到直观展示。实证上，Figure 2提供了关键证据：CLD的得分函数与正态分布得分的L2距离 ξ(t) 显著低于VPSDE，且得分网络雅可比矩阵的Frobenius范数更小，表明学习到的神经网络更平滑、更简单。

**与LSGM的关系**。LSGM-100M作为潜在空间得分生成模型的代表，在CIFAR-10上以约100M参数量实现了FID 4.60。CLD-SGM在相近参数量下将FID推至2.25（概率流ODE）和2.23（生成SDE），降幅达2.35，表明在数据空间直接改进扩散过程比迁移至潜在空间更具生成质量优势。这一对比验证了扩散过程设计本身的关键性，而非仅依赖模型容量或潜在空间压缩。

### 2. 方法组件与知识库锚定

**混合得分匹配（HSM）**。标准去噪得分匹配（DSM）直接应用于CLD时面临t→0时刻得分无界的严重问题，这是因为初始速度分布的条件得分在扩散初期具有奇异性。HSM通过解析地边际化初始速度分布，将训练目标改写为对条件分布 p_t(u_t|x_0) 的得分匹配，从根本上避免了无界得分问题。Figure 6对比了HSM与DSM中 ℓ_t 因子的行为，显示HSM在t接近0时保持有界。消融实验证实HSM是CLD稳定训练的“关键元素”：使用HSM时FID为3.14，而标准DSM仅为3.56。

**混合得分参数化**。将得分模型分解为正态得分基项与可训练的残差校正项 s_θ(u_t, t) = -ℓ_t α_θ(u_t, t)，这一参数化策略进一步利用了CLD得分接近正态分布的特性。消融实验表明，混合得分参数化将FID从3.56提升至3.14，与HSM共同构成CLD训练稳定性和性能的双重保障。

**SSCS采样器**。基于Fokker-Planck算子的对称Trotter/Strang分裂，SSCS将逆向SDE分解为可解析求解的A部分（哈密顿+OU）和需近似的S部分（得分项），通过交替积分实现高效采样。与广泛使用的Euler-Maruyama（EM）方法相比，SSCS在有限NFE预算下展现出压倒性优势：在n=150的非自适应步长设定下，SSCS-QS的FID为3.07，而EM-QS高达7.00。这一差距源于SSCS对线性动力学部分的精确处理，避免了EM在耦合系统中累积的离散化误差。Figure 8提供了两种采样器的概念可视化对比。

### 3. 适用边界与鲁棒性

**超参数鲁棒性**。CLD展现出对关键超参数的显著不敏感性。质量参数 M⁻¹ 在1到16范围内变化时，FID仅在3.23至3.16之间波动（Table 4），表明临界阻尼条件的精确满足并非性能的刚性约束。初始速度分布宽度 γ 从0.04增至1，FID仅从3.14微升至3.27（Table 5），说明方法对初始条件的选择具有高度的灵活性。这种鲁棒性降低了实际部署中的调参负担。

**当前局限**。CLD的探索目前主要局限在图像生成任务（CIFAR-10和CelebA-HQ-256），尚未在语音、视频等时序模态上进行验证。SSCS采样器仅支持固定步长，缺乏自适应步长策略，这限制了其在计算资源动态分配场景下的应用潜力。此外，CLD在最大似然训练场景下的高维图像生成尚未充分研究，NLL上界≤3.31虽具竞争力，但与LSGM-100M的2.96 bpd仍有差距。

### 4. 开放问题与未来方向

**统计力学方法的拓展**。CLD的成功表明统计力学中的恒温器（thermostat）概念可为SGMs提供新的扩散过程设计空间。能否将Nosé-Hoover恒温器、随机恒温器等其他物理机制引入SGMs，以进一步提升生成质量或加速采样，是一个值得探索的方向。

**采样器的进化**。SSCS目前受限于固定步长和二阶分裂格式。将其扩展至自适应步长策略，以及与高阶积分方法（如Runge-Kutta类格式）的结合，有望在更少的NFE下实现同等或更优的生成质量。此外，SSCS与DDIM等非马尔可夫加速采样技术的适配尚属空白，将CLD的连续时间框架与离散时间跳跃步骤结合可能开辟新的效率前沿。

**似然界的改进**。当前CLD的NLL上界受限于速度编码器的设计。通过引入可学习的速度编码器网络，或探索CLD与归一化流的混合架构，有望进一步收紧似然界，缩小与自回归模型和潜在变量模型的差距。

**跨模态与跨范式迁移**。CLD在图像生成上的成功引发了一个自然问题：该框架能否迁移至文本、蛋白质结构、分子构象等具有天然“位置-动量”耦合结构的数据模态？此外，CLD与GAN的对抗训练、与能量模型的MCMC采样之间的结合可能性，构成了生成模型统一框架探索的新维度。



## 原文 PDF

![[paperPDFs/ICLR_2022/Score_Based_Generative_Modeling_with_Critically_Damped_Langevin_Diffusion.pdf]]
