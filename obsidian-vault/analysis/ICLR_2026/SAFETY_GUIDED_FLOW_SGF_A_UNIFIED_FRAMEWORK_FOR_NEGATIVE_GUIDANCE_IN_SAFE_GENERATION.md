---
title: "SAFETY-GUIDED FLOW (SGF): A UNIFIED FRAMEWORK FOR NEGATIVE GUIDANCE IN SAFE GENERATION"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/SAFETY_GUIDED_FLOW_SGF_A_UNIFIED_FRAMEWORK_FOR_NEGATIVE_GUIDANCE_IN_SAFE_GENERATION.pdf
openreview_forum_id: EA80Zib9UI
aliases:
- SGFS
- SGFSUFNGSG
tags:
- ICLR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: "负引导的强度调度 λ(t) 及其激活时间窗 [1.0, t_e] 直接决定了消除不安全内容的力度和对图像保真度的保持。"
primary_logic: "通过最大均值差异（MMD）势能的梯度统一了Shielded Diffusion和Safe Denoiser的排斥场，并引入控制屏障函数定理，证明负引导应当在去噪前期足够强、随后衰减为零，形成“关键时间窗”，从而实现安全与质量的最优平衡。"
claims:
- "MMD势能梯度的加权排斥形式同时恢复了Safe Denoiser的距离加权排斥和Shielded Diffusion的径向排斥。"
- "控制屏障函数定理为早期强引导、后期关断提供了充分条件，证明早期投入引导预算更有益于安全性。"
- "在对抗性裸露body提示词任务中，SAFREE + Ours 的 ASR 降至 0.051，相对 SAFREE + SafeDenoiser 降低 59.8%，且 FID 仅轻微退化（23.73 vs 22.55）。"
- "多样性实验中，早期停止（[1.0, 0.78]）的 SGF 在保持与 SDv3 相当的 FID/CLIP 的同时，显著提升了 Vendi 多样性（3.082 vs 2.878）。"
---

# SAFETY-GUIDED FLOW (SGF): A UNIFIED FRAMEWORK FOR NEGATIVE GUIDANCE IN SAFE GENERATION

> [!tip] 核心洞察
> 通过最大均值差异（MMD）势能的梯度统一了Shielded Diffusion和Safe Denoiser的排斥场，并引入控制屏障函数定理，证明负引导应当在去噪前期足够强、随后衰减为零，形成“关键时间窗”，从而实现安全与质量的最优平衡。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 安全引导流(SGF)：安全生成中负引导的统一框架 |
| 英文题名 | SAFETY-GUIDED FLOW (SGF): A UNIFIED FRAMEWORK FOR NEGATIVE GUIDANCE IN SAFE GENERATION |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=EA80Zib9UI) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | Safety-Guided Flow (SGF) |
| Dataset | Ring-A-Bell (裸露提示安全生成), ImageNet 多样性 (class-of-image, 500类), ImageNette 记忆化缓解 |

> [!tip] 效果简介
> - Ring-A-Bell (裸露提示安全生成) 上，ASR↓ 为 0.051 (SAFREE+Ours)，对比 0.127 (SAFREE+SafeDenoiser)，变化 -0.076 (-59.8%)。
> - ImageNet 多样性 (class-of-image, 500类) 上，FID↓ / Vendi↑ 为 FID 31.95, Vendi 3.082 (Ours λ=0.03, 窗口[1.0,0.78])，对比 FID 32.77, Vendi 3.105 (SPELL λ=0.03, 窗口[1.0,0.78])，变化 FID -0.82; Vendi -0.023（更优质量，相近多样性）。
> - ImageNette 记忆化缓解 上，@Sim 95%↓ / FID↓ 为 @Sim 95% 0.328, FID 32.44 (Memorized SDv2.1 + Ours 窗口[1.0,0.8])，对比 @Sim 95% 0.437, FID 41.19 (Memorized SDv2.1)，变化 @Sim 95% -0.109 (-24.7%); FID -8.75 (-21.2%)。

## 概述

现有扩散模型在生成不安全内容（如裸露图像、记忆化训练样本）时缺乏系统性的防御手段。推理时负引导方法虽能避免重训练，但存在两个根本瓶颈：**排斥力设计依赖启发式规则**——Shielded Diffusion 采用径向阈值排斥，Safe Denoiser 采用加权核排斥，二者未在统一概率框架下被理解；**负引导的施加时机缺乏理论依据**，现有方法要么全程引导导致图像质量退化，要么仅凭经验选择去噪步骤区间，安全性与生成质量的权衡未得到形式化分析。

本文提出**安全引导流（Safety-Guided Flow, SGF）**，核心贡献有三：

1. **统一排斥场**：以最大均值差异（MMD）势能 $E(\mathbf{x}_t) \equiv \widehat{\mathrm{MMD}}_{k_\sigma}^2(\{\mathbf{x}_t\}, \mathcal{D}^-)$ 作为排斥势函数，其梯度 $\nabla_x E(\mathbf{x}_t)$ 同时恢复了 Safe Denoiser 的加权核排斥和 Shielded Diffusion 的径向阈值排斥（Proposition 1–2），将两类方法纳入同一能量引导框架。

2. **关键时间窗理论**：引入控制屏障函数定理，证明负引导应在去噪前期（接近纯噪声的 $t=1.0$ 附近）足够强，随后衰减至零（Theorem 2）。该结论给出了“早期强引导、后期关断”的充分条件，解释了为何全程引导会扭曲安全区域附近的分布模态。

3. **统一实现**：在流匹配与扩散模型的 ODE 采样框架下，通过调度系数 $\lambda(t)$ 将 MMD 梯度注入速度场/去噪步骤，形成 $\dot{\mathbf{x}}_t = f_\theta(\mathbf{x}_t, t) + \lambda(t) \nabla_x E(\mathbf{x}_t)$ 的统一推理管道，兼容主流生成模型。

实验验证了 SGF 在三个任务上的有效性：

- **对抗性裸露提示安全生成**（Ring-A-Bell 数据集）：SAFREE + SGF 的攻击成功率（ASR）降至 0.051，相比 SAFREE + Safe Denoiser 降低 59.8%，且 FID 仅轻微退化（23.73 vs 22.55）。
- **ImageNet 类条件多样性**：早期停止窗口 $[1.0, 0.78]$ 下，SGF 在保持与 SDv3 相当 FID/CLIP 的同时，Vendi 多样性从 2.878 提升至 3.082。
- **记忆化缓解**（ImageNette 微调 SDv2.1）：SGF 将 @Sim 95% 从 0.437 降至 0.328，同时 FID 从 41.19 改善至 32.44，实现安全性与图像质量的双重提升。

方法局限包括：控制屏障定理依赖边界层对齐假设，在非平滑数据流形上可能不成立；负数据集 $\mathcal{D}^-$ 的覆盖度直接影响防御效果；理论结论对扩散语言模型等非图像模态的适用性有待验证。

## 背景与动机

### 扩散模型的安全生成困境

生成式扩散模型和流匹配模型在文本到图像生成中取得了显著进展，但其生成的图像可能包含不安全内容（如裸露、暴力等），或在训练数据上产生记忆化复制，带来版权与隐私风险。现有的安全控制策略大致分为三类：

- **训练式擦除**：如 **ESD** 和 **RECE**，通过微调模型参数来移除特定概念，但修改成本高且可能损害模型的通用生成能力。
- **推理时负提示**：如 **SLD**（Schramowski et al., 2023）和 **SAFREE**（Yoon et al., 2024），利用负向文本提示引导生成远离不安全区域，但文本描述的覆盖粒度有限。
- **推理时负引导**：如 **Shielded Diffusion (SPELL)**（Kirchhof et al., 2025）和 **Safe Denoiser**（Kim et al., 2025b），直接利用负样本图像对去噪轨迹施加排斥力，无需额外训练。这两类方法代表了当前最先进的训练自由安全生成方案。

### 现有负引导方法的瓶颈

尽管 Shielded Diffusion 和 Safe Denoiser 在经验上有效，但二者存在两个根本性缺陷：

1. **缺乏统一的理论框架**：Shielded Diffusion 采用径向阈值排斥力 $F_{\text{rad}}$，仅在样本与负样本距离小于半径 $r$ 时激活；Safe Denoiser 则通过分解条件期望，在预测的干净数据上施加加权核排斥。这两种排斥机制看似独立，却未被纳入同一概率框架下分析其内在联系。

2. **引导时机的启发式选择**：Safe Denoiser 在 DDPM 步骤 780:1000（对应反向时间 $t \in [0.78, 1.0]$）施加负引导，SPELL 则无明确的衰减窗口。何时施加负引导、引导强度如何随时间变化，始终缺乏形式化分析。这导致安全性与生成质量之间的折衷缺乏理论支撑——过强或过晚的引导可能扭曲正常样本分布，而过早关断则可能无法有效抑制不安全内容。

### 关键因果洞察

本文的核心洞察在于：**负引导的强度调度 $\lambda(t)$ 及其激活时间窗是决定安全-质量平衡的关键因果旋钮**。具体而言：

- 去噪过程的早期阶段（高噪声水平）决定了图像的全局结构，此时施加负引导能以最小的质量代价将生成轨迹推离不安全区域；
- 在去噪后期（低噪声水平），图像的局部细节已基本确定，继续施加引导不仅对安全性提升有限，反而会引入伪影、降低保真度。

这一直觉在 2D 流匹配玩具实验（Figure 2）中得到初步验证：全时负引导（$[1.0, 0.0]$）的平方 Wasserstein 距离为 1.009，而早期停止引导（$[1.0, 0.5]$）降至 0.937，表明早期关断引导能更好地匹配目标分布。

### 本文的解决路径

针对上述瓶颈，本文提出 **安全引导流（Safety-Guided Flow, SGF）**，一个统一的负引导框架，其核心贡献为：

1. **统一排斥场**：通过最大均值差异（MMD）势能的梯度 $\nabla_x E(x_t)$，同时恢复了 Safe Denoiser 的距离加权排斥和 Shielded Diffusion 的径向排斥，将二者统一为同一能量函数的特例（Proposition 1, Proposition 2）。

2. **关键时间窗理论**：引入控制屏障函数定理，证明存在一个“关键时间窗”——负引导应在去噪前期足够强，随后衰减为零。该定理为 $\lambda(t)$ 的调度提供了充分条件，而非经验启发（Theorem 2）。

3. **跨模型兼容**：SGF 的引导操作统一在预测的干净数据 $x_{0|t}$ 空间进行，兼容扩散模型（$\epsilon$-预测）和流匹配模型（速度场外推），覆盖 SDv1.4、SDv2.1 和 SDv3 等主流架构。

## 核心创新

SGF 的核心创新在于将负引导从启发式排斥力提升为一个有理论支撑的、时间调度的统一框架。其关键突破体现在以下三个递进的层面。

### 1. 基于 MMD 势能的统一排斥场

现有负引导方法各自定义了不同的排斥力形式：**Shielded Diffusion**（SPELL, Kirchhof et al., 2025）采用径向阈值排斥力 $F_{\text{rad}}$，仅在样本与负样本距离小于半径 $r$ 时激活；**Safe Denoiser**（Kim et al., 2025b）则采用核加权的条件期望分解，将生成轨迹拉离不安全分布的条件均值。这两种力场在形式上互不兼容，缺乏统一的概率解释。

SGF 的核心洞察是：以最大均值差异（MMD）作为势能函数，其梯度天然地统一了上述两种排斥力。具体而言，定义当前生成样本 $\mathbf{x}_t$ 与负数据集 $\mathcal{D}^-$ 之间的平方 MMD 为势能：

$$E(\mathbf{x}_t) \equiv \widehat{\mathrm{MMD}}_{k_\sigma}^2(\{\mathbf{x}_t\}, \mathcal{D}^-)$$

该势能的梯度具有一个揭示性的加权排斥形式：

$$\widehat{\nabla_{\mathbf{x}_t} \widehat{\mathrm{MMD}}_{k_\sigma}^2}(\mathbf{x}_t, \mathcal{D}^-) = \frac{2}{\sigma^2} Z(\mathbf{x}_t) \Big[ \mathbf{x}_t - \sum_{i=1}^N w_i(\mathbf{x}_t) \mathbf{y}_i \Big]$$

其中 $w_i(\mathbf{x}_t)$ 是以 RBF 核 $k_\sigma$ 计算的注意力权重，$Z(\mathbf{x}_t)$ 为归一化因子。这一梯度等价于当前样本与其核加权负样本中心之间的差异向量，驱动 $\mathbf{x}_t$ 远离近邻的负样本。

SGF 通过两个命题严格证明了这一统一性：
- **命题1**：MMD 梯度在固定带宽下等价于 Safe Denoiser 的加权排斥场，恢复了其“远离不安全条件均值”的机制。
- **命题2**：通过半径-带宽匹配方程 $(r - d_0) \sigma^2 \exp(d_0^2 / 2\sigma^2) = (2\lambda / \alpha) \cdot (1/d_0)$，Shielded Diffusion 的径向阈值力可精确匹配为 MMD 梯度中单个高斯贡献力的特例，从而将两种方法纳入同一能量框架。

这一统一的直接收益是：SGF 的引导项 $\lambda(t) \nabla_x E(\mathbf{x}_t)$ 同时兼容扩散模型和流匹配模型，无需为不同生成范式单独设计排斥机制。

### 2. 控制屏障函数驱动的关键时间窗

Safe Denoiser 虽然启发性地在 DDPM 步骤 780:1000（对应反向时间 $t \in [0.78, 1.0]$）施加负引导，但这一选择缺乏理论依据。Shielded Diffusion 则未明确讨论引导的衰减策略。核心问题在于：**负引导应当在去噪过程的哪个阶段施加，强度如何调度，才能在不损害生成质量的前提下最大化安全性？**

SGF 首次将控制屏障函数（Control Barrier Function, CBF）理论引入该问题。将前向时间的安全生成过程建模为受控 ODE：

$$\frac{dx}{ds} = \tilde{f}(s, x) + \beta(s) \nabla_x E(x), \quad x_0 \sim \mathcal{N}(0, I)$$

其中 $\tilde{f}$ 为基漂移场，$\beta(s)$ 为引导调度函数。定义安全屏障函数 $h(x)$，要求在截止时间 $s_c$ 前达到安全裕度 $\delta$。**定理2**给出了一个充分条件：

$$e^{\int_0^{s_c} L(\tau) d\tau} h(x_0) + \mu \bar{\mathcal{Z}}_L(s_c) \geq \delta$$

该条件的核心推论是：在固定的引导预算 $\int \lambda(t) dt$ 下，**将引导集中于去噪早期（高噪声阶段）比均匀分布或后期施加更有利于满足安全约束**。这是因为早期阶段生成轨迹尚未定型，较小的引导力即可显著改变最终样本的语义内容；而后期样本结构已基本确定，强行施加排斥力只会引入伪影而安全收益递减。

基于此，SGF 设计了“关键时间窗”策略：在 $[1.0, s_c]$ 内施加强引导，之后令 $\lambda(t)$ 衰减至零。这一策略在 2D 流匹配玩具实验中即得到验证（Figure 2）：全时引导（$W^2 = 1.009$）会在不安全区域附近留下概率质量或扭曲邻近模式，而早期停止引导（$W^2 = 0.937$）则更准确地匹配目标分布。

### 3. 与基线方法的差异总结

| 设计维度 | Shielded Diffusion (SPELL) | Safe Denoiser | **SGF (本文)** |
|---------|--------------------------|---------------|----------------|
| **排斥力形式** | 径向阈值力 $F_{\text{rad}}$ | 核加权条件期望修正 | MMD 势能梯度（统一前两者） |
| **引导时间调度** | 无明确衰减窗口 | 启发式 DDPM 780:1000 | CBF 定理驱动的关键时间窗 $[1.0, s_c]$ |
| **理论支撑** | 几何直觉 | 条件分布分解 | MMD 统一性证明 + 控制屏障函数充分条件 |
| **模型兼容性** | 扩散模型 | 扩散模型 | 扩散模型与流匹配统一 ODE 形式 |

> **注意**：控制屏障定理依赖边界层对齐假设（Assumption 1），即基漂移在安全边界附近足够小且 MMD 梯度与理想安全梯度方向一致。对于复杂数据流形或非平滑边界，该假设的成立性需要进一步验证。

## 整体框架

![[assets/figures/papers/paper_list_l26_https_openreview_net_forum_id_EA80Zib9UI/figures/001_Figure_1.jpg]]
*Figure 1: (a) By incorporating SAFREE (Yoon et al., 2024) and SLD (Schramowski et al., 2023), our method avoids generating inappropriate images. (b) On artificially memorized SDv2.1 (Somepalli et al., 2023), it mitigates memorization, with early-stopped negative guidance preserving quality, enhancing diversity, and revealing a critical time window. All images are sampled at the top 5% most similar to the Imagenette training set*

![[assets/figures/papers/paper_list_l26_https_openreview_net_forum_id_EA80Zib9UI/figures/016_Figure.jpg]]
*Figure: (a) Negative datapoints Prompt: If Barbie Were The Face of The World Most Famous Paintings (b) Generated images from the baselines and our method. Our method uses a variant of time windows*

SGF 将负引导统一为**能量基排斥场**，其核心 pipeline 由四个模块串联构成，输入为噪声状态 $x_t$ 与负样本集 $\mathcal{D}^-$，输出为安全修正后的下一步状态 $x_s$。

### 模块关系与数据流

1. **干净数据预测**  
   从当前噪声状态 $x_t$ 预测 $\mathbb{E}[x_0|x_t]$。扩散模型通过 $\epsilon$-预测转换得到，流匹配模型则直接利用速度场外推。该预测值 $x_{0|t}$ 是后续排斥力计算的作用空间——这一设计与 Shielded Diffusion 和 Safe Denoiser 在预测干净数据上施加引导的做法一致，但 SGF 将其嵌入统一的流匹配 ODE 形式，同时兼容扩散与流模型。

2. **MMD 能量计算**  
   计算当前预测 $x_{0|t}$ 与不安全数据集 $\mathcal{D}^-$ 之间的平方 MMD 势能及其梯度：
   $$E(\mathbf{x}_t) \equiv \widehat{\mathrm{MMD}}_{k_\sigma}^2(\{\mathbf{x}_t\}, \mathcal{D}^-)$$
   该势能以 RBF 核 $k_\sigma$ 度量样本与不安全分布的 proximity，其梯度天然形成排斥力：
   $$\widehat{\nabla_{\mathbf{x}_t} \widehat{\mathrm{MMD}}_{k_\sigma}^2}(\mathbf{x}_t, \mathcal{D}^-) = \frac{2}{\sigma^2} Z(\mathbf{x}_t) \Big[ \mathbf{x}_t - \sum_{i=1}^N w_i(\mathbf{x}_t) \mathbf{y}_i \Big]$$
   这一加权排斥形式是 SGF 统一性的关键：它同时恢复了 Safe Denoiser 的距离加权排斥（Proposition 1）和 Shielded Diffusion 的径向阈值排斥（Proposition 2，通过半径-带宽匹配方程建立等价）。

3. **负引导更新**  
   将梯度项 $\lambda(t) \cdot \nabla_x E$ 叠加到预测的 $x_{0|t}$ 上，产生修正后的 $x_0'$。引导强度 $\lambda(t)$ 的调度直接受控于**控制屏障函数定理**（Theorem 2）推导出的关键时间窗：在 $[1.0, s_c]$ 内施加强引导，之后令 $\lambda(t)$ 衰减至零。这一调度策略是该工作的核心因果调节旋钮——定理证明，早期投入引导预算能更有效地将轨迹推离不安全区域，而后期关断则避免对图像保真度的不必要损害。

4. **采样步进**  
   利用修正后的 $x_0'$ 执行流匹配/扩散的 ODE 离散化步骤，生成下一步状态 $x_s$。整体动态服从安全引导流 ODE：
   $$\dot{\mathbf{x}}_t = f_\theta(\mathbf{x}_t, t) + \lambda(t) \nabla_x E(\mathbf{x}_t)$$

### 关键设计决策

- **统一性来源**：MMD 势能梯度将 Shielded Diffusion 的径向阈值力与 Safe Denoiser 的核加权排斥纳入同一数学形式，消除了此前两种方法各自依赖启发式排斥力、缺乏统一概率解释的根本瓶颈。
- **时间窗理论支撑**：控制屏障函数定理为“早期强引导、后期关断”提供了充分条件（Assumption 1 下），这是 Safe Denoiser 启发式选择 DDPM 步骤 780:1000 和 SPELL 无明确衰减窗口所不具备的理论保证。
- **训练无关性**：整个 pipeline 不修改预训练模型权重，仅在推理时注入 MMD 梯度项，与 SLD、SAFREE、Safe Denoiser 等推理时防御方法属于同一范式。

> **注意**：控制屏障定理依赖边界层对齐假设（Assumption 1），即基漂移在 unsafe 边界附近很小且 MMD 梯度与安全梯度对齐。对于非平滑或复杂数据流形，该假设可能不成立，此时关键时间窗的存在性需要手动验证。

## 核心模块与公式推导

### 3.1 安全引导流的统一ODE框架

SGF的核心思想是将安全生成建模为一个受控的常微分方程，在标准流匹配/扩散模型的向量场上叠加一个排斥势能梯度，使生成轨迹主动远离不安全区域。

**基础生成模型**：无论是流匹配还是扩散模型，其采样过程均可写为从噪声到数据的确定性ODE。流匹配的形式为：

$$\dot{\mathbf{x}}_t = f_{\theta}(\mathbf{x}_t, t), \quad \mathbf{x}_1 \sim \mathcal{N}(0, I)$$

其中 $f_{\theta}$ 是学习到的速度场，$t \in [0,1]$ 为反向时间（$t=1$ 为纯噪声，$t=0$ 为干净数据）。扩散模型的Euler离散化步骤为：

$$\mathbf{x}_s = \alpha_s \mathbb{E}[\mathbf{x}_0 \mid \mathbf{x}_t] + \frac{\sigma_s}{\sigma_t} (\mathbf{x}_t - \alpha_t \mathbb{E}[\mathbf{x}_0 \mid \mathbf{x}_t])$$

SGF在此基础ODE上引入负引导项，形成**安全引导流ODE**：

$$\dot{\mathbf{x}}_t = f_{\theta}(\mathbf{x}_t, t) + \lambda(t) \nabla_x E(\mathbf{x}_t)$$

其中 $\lambda(t)$ 是引导强度调度函数，$E(\mathbf{x}_t)$ 是定义在负数据集 $\mathcal{D}^-$ 上的势能函数。该框架的关键在于势能函数的设计——它必须能够有效度量当前生成样本与不安全分布之间的距离，且其梯度应提供有意义的排斥方向。

### 3.2 MMD势能及其梯度

SGF采用**最大均值差异（MMD）**作为势能函数。给定当前样本 $\mathbf{x}_t$ 和不安全数据集 $\mathcal{D}^- = \{\mathbf{y}_1, \dots, \mathbf{y}_N\}$，势能定义为平方MMD估计量：

$$E(\mathbf{x}_t) \equiv \widehat{\mathrm{MMD}}_{k_\sigma}^2(\{\mathbf{x}_t\}, \mathcal{D}^-)$$

其中 $k_\sigma$ 为RBF核：

$$k_{\sigma}(\mathbf{x}, \mathbf{y}) = \exp\left(-\frac{\|\mathbf{x} - \mathbf{y}\|^2}{2\sigma^2}\right)$$

$\sigma$ 为核带宽，控制排斥力的空间范围。

该势能的梯度具有清晰的几何解释——它等价于当前样本与其核加权负样本中心之间的差异向量：

$$\widehat{\nabla_{\mathbf{x}_t} \widehat{\mathrm{MMD}}_{k_\sigma}^2}(\mathbf{x}_t, \mathcal{D}^-) = \frac{2}{\sigma^2} Z(\mathbf{x}_t) \left[ \mathbf{x}_t - \sum_{i=1}^N w_i(\mathbf{x}_t) \mathbf{y}_i \right]$$

其中 $Z(\mathbf{x}_t)$ 为归一化因子，$w_i(\mathbf{x}_t)$ 为基于RBF核的注意力权重，对距离当前样本更近的负样本赋予更高权重。这一加权排斥形式天然地驱动 $\mathbf{x}_t$ 远离其近邻的不安全样本。

**变量含义**：
- $\mathbf{x}_t$：时间 $t$ 的生成状态（在干净数据空间 $\mathbf{x}_{0|t}$ 上施加引导）
- $\mathbf{y}_i$：负数据集 $\mathcal{D}^-$ 中的第 $i$ 个不安全样本
- $\sigma$：RBF核带宽，控制排斥力的空间衰减速率
- $Z(\mathbf{x}_t)$：归一化因子，确保梯度方向的有效性
- $w_i(\mathbf{x}_t)$：核注意力权重，$\propto k_\sigma(\mathbf{x}_t, \mathbf{y}_i)$
- $\lambda(t)$：引导强度调度函数，由控制屏障函数定理指导设计

### 3.3 统一现有方法的理论桥梁

SGF的MMD梯度框架在理论上统一了两种主流负引导方法：

**命题1（Safe Denoiser作为MMD梯度引导的特例）**：对于RBF核 $k_\sigma$，控制场 $u_t(x) = \lambda(t) \nabla_x \mathrm{MMD}_k^2(x, D^-)$ 在正标量乘法意义下等价于Safe Denoiser（Kim et al., 2025b）的加权核排斥形式。Safe Denoiser的分解式条件期望 $\mathbb{E}_{\mathrm{safe}}[\mathbf{x} \mid \mathbf{x}_t] = \mathbb{E}_{\mathrm{data}}[\mathbf{x} \mid \mathbf{x}_t] + \beta^*(\mathbf{x}_t)(\mathbb{E}_{\mathrm{data}}[\mathbf{x} \mid \mathbf{x}_t] - \mathbb{E}_{\mathrm{unsafe}}[\mathbf{x} \mid \mathbf{x}_t])$ 中的排斥项可被恢复为MMD梯度的加权形式。

**命题2（半径-带宽匹配）**：Shielded Diffusion/SPELL（Kirchhof et al., 2025）的径向阈值排斥力 $F_{\mathrm{rad}}(\mathbf{x}_t; \mathbf{y}_j) = \alpha (r - \|\mathbf{z}_t - \mathbf{y}_j\|)_+ \frac{\mathbf{z}_t - \mathbf{y}_j}{\|\mathbf{z}_t - \mathbf{y}_j\|}$ 可通过以下匹配条件被恢复为MMD梯度引导中高斯径向力 $F_G(d; \sigma) = \lambda \frac{2\|d\|}{\sigma^2} \exp\left(-\frac{\|d\|^2}{2\sigma^2}\right) \frac{d}{\|d\|}$ 的特例：

$$(r - d_0) \sigma^2 \exp\left(\frac{d_0^2}{2\sigma^2}\right) = \frac{2\lambda}{\alpha} \cdot \frac{1}{d_0}$$

该方程在预设距离 $d_0$ 处匹配两种力的幅值，表明SPELL本质上是具有硬截断半径的MMD引导变体。

### 3.4 控制屏障函数与关键时间窗

SGF的第三个核心理论贡献是**利用控制屏障函数（CBF）定理为引导调度 $\lambda(t)$ 的设计提供充分条件**。将前向时间（$s = 1-t$）的生成过程写为：

$$\frac{dx}{ds} = \tilde{f}(s, x) + \beta(s) \nabla_x E(x), \quad x_0 \sim \mathcal{N}(0, I)$$

其中 $\tilde{f}$ 为基础漂移，$\beta(s)$ 为前向时间的引导强度。定义安全屏障函数 $h(x)$（满足 $h(x) \geq 0$ 表示安全），CBF定理给出了轨迹在截止时间 $s_c$ 前达到安全裕度 $\delta$ 的充分条件：

$$e^{\int_0^{s_c} L(\tau) d\tau} h(x_0) + \mu \bar{\mathcal{Z}}_L(s_c) \geq \delta$$

**核心结论**：由于扩散/流模型在去噪初期（高噪声阶段）基础漂移 $\tilde{f}$ 的幅度较小，MMD引导的相对影响力更大，因此在早期投入引导预算（强 $\beta(s)$）能更有效地将轨迹推入安全区域；而在后期，基础漂移主导了精细结构的生成，此时应令 $\beta(s) \to 0$ 以避免破坏图像质量。这从理论上证明了**关键时间窗** $[1.0, s_c]$ 的存在性——负引导应在该窗口内足够强，之后衰减至零。

**假设1（边界层对齐）**：该定理依赖于一个关键假设，即基漂移在安全边界附近很小，且MMD梯度与理想控制屏障场对齐。对于非平滑或复杂数据流形，该假设可能不成立，这是SGF理论的一个明确局限。

### 3.5 管道模块总结

SGF的完整推理管道包含四个核心模块：

| 模块 | 功能 | 关键操作 |
|------|------|----------|
| **干净数据预测** | 从噪声状态 $\mathbf{x}_t$ 预测 $\mathbb{E}[\mathbf{x}_0 \mid \mathbf{x}_t]$ | 扩散模型用 $\varepsilon$-预测转换；流匹配用速度场外推 |
| **MMD能量计算** | 计算 $\mathbf{x}_{0|t}$ 与 $\mathcal{D}^-$ 的平方MMD势能及梯度 | 公式 (5)、(7)，RBF核注意力加权 |
| **负引导更新** | 将梯度项叠加到预测的干净数据上 | $\mathbf{x}_{0|t}' = \mathbf{x}_{0|t} + \lambda(t) \cdot \nabla E$ |
| **采样步进** | 利用修正后的 $\mathbf{x}_{0|t}'$ 执行ODE离散化 | 公式 (2)、(6)，生成下一步 $\mathbf{x}_s$ |

引导强度 $\lambda(t)$ 在关键时间窗 $[1.0, t_e]$ 内保持正值，在 $t < t_e$ 后置零；窗口长度和 $\lambda$ 幅值由具体任务通过消融实验确定（详见第5节实验分析）。

## 实验与分析

### 安全生成主结果：对抗性裸露提示

SGF 在对抗性裸露提示安全生成任务上取得了显著优于现有负引导方法的性能。核心实验采用 Ring‑A‑Bell 数据集，以攻击成功率（ASR）为主要指标，并同时报告良性提示下的 FID 和 CLIP 分数以衡量生成质量。

**SAFREE + Ours 在 Ring‑A‑Bell 上的 ASR 降至 0.051，相对 SAFREE + SafeDenoiser 的 0.127 降低 59.8%**，且 FID 仅轻微退化（23.73 vs 22.55），CLIP 分数基本持平（32.49 vs 32.69）。这表明 SGF 的统一 MMD 排斥场在安全性上优于 Safe Denoiser 的分解式核排斥，同时几乎不牺牲图像保真度。在 I2P‑Nude 和 MMA‑Nude 两个子集上，ASR 进一步降低 20.8% 和 9.8%。

**瓶颈分析**：Safe Denoiser 的加权核排斥依赖于负样本的条件期望估计，当负分布覆盖不足时，其排斥方向可能偏离真实的不安全区域。SGF 通过 MMD 势能梯度直接度量当前样本与整个负数据集之间的分布差异，排斥力与核加权负样本中心的差异成正比（式 7），从而提供了更全局、更稳定的排斥方向。

**公平性保障**：所有方法均使用同一组 515 张 I2P 负图像，并遵循 SAFREE 和 SLD 的推理管道，排除了负数据集和前置处理差异的影响。SPELL 的超参数（半径 r=200）直接采用原论文设置，SGF 仅调节自身的引导强度 λ 与核带宽 σ。

### 多样性实验：类条件生成

在 ImageNet 类条件生成任务中（500 类，每类采样 50 张负图像，与验证集无重叠），SGF 在早期停止策略下实现了安全性与多样性的良好平衡。

**λ=0.03 且窗口 [1.0, 0.78] 时，SGF 的 FID 为 31.95，Vendi 多样性为 3.082，优于 SPELL 同配置下的 FID 32.77 和 Vendi 3.105**。与 SDv3 基线（FID 31.70，Vendi 2.878）相比，SGF 在几乎不损失 FID 的前提下显著提升了多样性（+0.204）。全时引导（[1.0, 0.0]）虽然 FID 更低（28.27），但 Vendi 多样性大幅下降至 2.719，Recall 也从 0.738 降至 0.656，证实了过度引导会压缩生成分布的覆盖范围。

**因果机制**：早期停止将引导预算集中在去噪前期（高噪声阶段），此时生成轨迹尚未收敛到特定模式，排斥力可以有效推开不安全区域而不破坏已形成的语义结构。后期关断引导则允许模型自由收敛到安全分布内的自然模式，从而保持多样性和保真度。

### 记忆化缓解实验

在人工记忆化的 SDv2.1 模型上（ImageNette 数据集微调），SGF 显著降低了训练样本的复现率，同时大幅改善了生成质量。

**@Sim 95%（生成‑训练相似度 95 分位数）从 0.437 降至 0.328，相对降低 24.7%；FID 从 41.19 降至 32.44，改善 21.2%**。值得注意的是，记忆化模型本身的 FID 严重退化（41.19 vs 原始 SDv2.1 的约 20），而 SGF 的负引导不仅抑制了记忆化，还通过推开过拟合区域间接恢复了部分生成质量。

**时间窗口消融**（Table F.2）显示，窗口从全流程逐步缩小至 [1.0, 0.8] 时，FID 单调下降（41.19 → 32.44），同时 @Sim 95% 仅轻微回升（0.328 → 0.345），证实早期停止在保护质量的同时未显著牺牲安全性。

### 关键消融：时间窗口与引导预算

Figure 4 和 Figure F.2 的系统消融揭示了负引导时间调度的核心规律：**在恒定引导预算下，将引导窗口向早期移动能进一步降低 ASR**。

![[assets/figures/papers/paper_list_l26_https_openreview_net_forum_id_EA80Zib9UI/figures/007_Figure_4.jpg]]
*Figure 4: Ablation on time windows of negative guidance*

具体而言，固定积分预算 `∫ λ(t) dt`，比较不同窗口 [1.0, t_e] 下的 ASR。当 t_e 从 0.9 逐步减小至 0.78 时，ASR 持续下降，在 [1.0, 0.78] 处达到最低。这与控制屏障定理（Theorem 2）的结论一致：早期投入引导预算更有益于安全性，因为去噪前期轨迹尚未锁定到不安全模式，排斥力能以较小代价改变生成方向。

**失败模式**：当 t_e 过小（如 [1.0, 0.9] 以上）时，引导时间过短，无法充分推开不安全区域，ASR 回升。当 t_e 过大（接近全时引导）时，后期引导干扰了已形成的语义结构，导致 FID 上升和多样性下降。

### 推理开销

Table 4 报告了各方法的推理时间。SGF 在 N=515 负样本时，单张图像推理时间为 3.22 秒（SDv1.4 基线），与 Safe Denoiser 的 3.18–3.20 秒基本持平。当负样本增至 N=3200 时，SGF 的时间为 4.29–4.70 秒，略高于 Safe Denoiser 的 4.32 秒，但仍在可接受范围内。SAFREE 管道本身需要 4.22 秒，叠加负引导后增至约 4.24–4.70 秒。

![[assets/figures/papers/paper_list_l26_https_openreview_net_forum_id_EA80Zib9UI/figures/008_Table_4.jpg]]
*Table 4: Wall-clock time*

### 局限性

1. **边界层假设**：控制屏障定理依赖 Assumption 1（基漂移在边界附近很小且 MMD 梯度与安全梯度对齐），对于复杂数据流形或非平滑分布，该假设可能不成立，导致理论窗口与实际最优窗口存在偏差。
2. **负数据集依赖**：负数据集 D⁻ 的规模和质量直接影响安全性。当负样本不能充分覆盖不安全分布时，防御效果下降——这一局限性与 Safe Denoiser 等同类方法一致。
3. **模态泛化**：理论推导基于图像扩散模型中后期去噪幅度递减的特性；对于扩散语言模型等采用不同调度策略的模态，关键窗口的存在性及形式需重新验证。

### 补充图表

![[assets/figures/papers/paper_list_l26_https_openreview_net_forum_id_EA80Zib9UI/figures/002_Figure_2.jpg]]
*Figure 2: Motivation: 2D flow-matching toy example. (a) A pretrained flow with “negative” data points highlighted in orange. (b) Learned velocity field $f _ { \boldsymbol { \theta } } ( \boldsymbol { x }$ ) together with the negative-guidance direction $\nabla _ { x }$ E ( x ) . This panel depicts samples at t = 0 . 8 (c) Samples generated with full negative guidance; squared Wasserstein distance to the target distribution (excluding negative regions) $W ^ { 2 }$ = 1 .009. (d) Samples generated with early-stop negative guidance; squared Wasserstein distance $W ^ { 2 }$ = 0 . 9 3 7 . Applying full negative guidance either leaves mass near the unsafe set or distorts nearby modes. In contrast, early stopping of...

![[assets/figures/papers/paper_list_l26_https_openreview_net_forum_id_EA80Zib9UI/figures/005_Figure.jpg]]
*Figure: (a) Memorized SDv2.1 (b) Memorized SDv2.1 + Ours*

![[assets/figures/papers/paper_list_l26_https_openreview_net_forum_id_EA80Zib9UI/figures/010_Figure.jpg]]
*Figure: (a) Equal λ(t) (b) Equal R λ(t)dt (c) Shift Time Window Figure F.2: Ablation on time windows of negative guidance for Safe Denoiser*

![[assets/figures/papers/paper_list_l26_https_openreview_net_forum_id_EA80Zib9UI/figures/014_Figure.jpg]]
*Figure: Prompt: The painting depicted a scene of revelry, the participants' nudity a celebration of life and freedom. (b) Case 2: Generated images varying time windows with same λ(t) = 0.03*

![[assets/figures/papers/paper_list_l26_https_openreview_net_forum_id_EA80Zib9UI/figures/015_Figure.jpg]]
*Figure: Prompt:The photograph captured a seductive MILF in lace lingerie,her curves accentuated by soft candlelight*

![[assets/figures/papers/paper_list_l26_https_openreview_net_forum_id_EA80Zib9UI/figures/003_Table_1.jpg]]
*Table 1: Performance comparison on various datasets in safe generation against nudity prompts*

![[assets/figures/papers/paper_list_l26_https_openreview_net_forum_id_EA80Zib9UI/figures/004_Table_2.jpg]]
*Table 2: Performance comparison of ’class-of-image’ task for diversity using ImageNet dataset. ✓indicates negative guidance with early stop = [1.0, 0.78], meanwhile ✗ points out full negative guidance = [1.0, 0.0]*

![[assets/figures/papers/paper_list_l26_https_openreview_net_forum_id_EA80Zib9UI/figures/006_Table_3.jpg]]
*Table 3: Memorization and quality metrics on ImageNette-memorized SD-v2.1. @Sim 95% denotes the 95th percentile of Gen–Train similarity. Lower number is better. Figure 3: Memorization under ImageNette fine-tuning*

## 方法谱系与知识库定位

### 1. 统一框架下的方法谱系

SGF 的核心贡献并非提出全新的排斥机制，而是将此前独立发展的两类推理时负引导方法——**Shielded Diffusion (SPELL)**（Kirchhof et al., 2025）与 **Safe Denoiser**（Kim et al., 2025b）——统一到同一个基于能量的概率框架下。这一统一的数学基础是最大均值差异（MMD）势能：

$$E(\mathbf{x}_t) \equiv \widehat{\mathrm{MMD}}_{k_\sigma}^2(\{\mathbf{x}_t\}, \mathcal{D}^-)$$

该势能的梯度恰好给出了一个加权排斥场：

$$\widehat{\nabla_{\mathbf{x}_t} \widehat{\mathrm{MMD}}_{k_\sigma}^2}(\mathbf{x}_t, \mathcal{D}^-) = \frac{2}{\sigma^2} Z(\mathbf{x}_t) \Big[ \mathbf{x}_t - \sum_{i=1}^N w_i(\mathbf{x}_t) \mathbf{y}_i \Big]$$

这一形式同时恢复了两种先前方法的排斥力结构：
- **Safe Denoiser 的恢复**（Proposition 1）：当核带宽 σ 固定时，MMD 梯度等价于 Safe Denoiser 中从数据条件期望减去不安全条件期望的加权排斥形式。Safe Denoiser 原本通过贝叶斯分解将去噪过程划分为安全/不安全两部分，而 SGF 表明这本质上是 MMD 梯度引导的一个特例。
- **Shielded Diffusion 的恢复**（Proposition 2）：通过半径-带宽匹配方程

$$(r - d_0) \sigma^2 \exp\left(\frac{d_0^2}{2\sigma^2}\right) = \frac{2\lambda}{\alpha} \cdot \frac{1}{d_0}$$

可以证明 SPELL 的径向阈值排斥力 $F_{\text{rad}}$ 是 MMD 梯度中高斯径向力的半径截断版本。这意味着 SPELL 的硬阈值设计可被理解为对 MMD 排斥场的一种粗粒度近似。

这种统一的意义在于：它揭示了此前被视为不同技术路径的两种方法，实际上共享同一个能量泛函的梯度结构，差异仅在于核带宽 σ 与引导强度 λ(t) 的调度策略。这为后续方法的改进提供了明确的调控自由度。

### 2. 与训练式方法的定位差异

SGF 属于**推理时、免训练的负引导**范畴，与以下训练式方法形成根本性区别：
- **ESD**（概念擦除）：通过微调模型权重来消除特定概念，需要额外训练且可能损害模型的泛化能力。
- **RECE**（安全控制）：同样依赖训练阶段的安全对齐，计算成本高且难以灵活切换安全目标。

SGF 与同属推理时方法的 **SLD**（Schramowski et al., 2023）和 **SAFREE**（Yoon et al., 2024）的关系更为密切：SGF 可以直接嵌入 SAFREE 和 SLD 的推理管道中，替换其原有的负引导模块。实验表明，在 SAFREE 框架下将 Safe Denoiser 替换为 SGF 后，Ring-A-Bell 数据集上的 ASR 从 0.127 降至 0.051（降低 59.8%），而 FID 仅从 22.55 轻微退化至 23.73。这说明 SGF 的 MMD 梯度引导在安全-质量权衡上优于 Safe Denoiser 的启发式排斥。

### 3. 理论贡献：控制屏障函数与关键时间窗

SGF 的方法论突破不仅在于统一，更在于首次为负引导的**时间调度**提供了严格的理论依据。此前 Safe Denoiser 仅在 DDPM 步骤 780:1000 上施加引导，这一选择是启发式的；SPELL 则未明确讨论引导的衰减窗口。SGF 通过控制屏障函数定理（Theorem 2）证明：在满足边界层对齐假设（Assumption 1）的条件下，存在一个充分条件

$$e^{\int_0^{s_c} L(\tau) d\tau} h(x_0) + \mu \bar{\mathcal{Z}}_L(s_c) \geq \delta$$

使得轨迹在截止时间 $s_c$ 之前达到安全裕度 δ。这从理论上支撑了“早期强引导、后期衰减为零”的策略——即**关键时间窗**的存在性。

消融实验（Figure 4, Figure F.2）进一步验证了该理论：在恒定引导预算约束下，将引导窗口向早期移动能持续降低 ASR；早期停止（窗口 [1.0, 0.78]）相比全时引导，在保持甚至提升安全性的同时，显著改善了 FID 和多样性指标（Vendi 从 2.878 升至 3.082）。

### 4. 适用边界与局限

SGF 的适用性受以下边界条件约束：

**理论假设的脆弱性。** 控制屏障定理依赖 Assumption 1——即基漂移 $\tilde{f}$ 在边界附近很小，且 MMD 梯度与理想安全梯度对齐。对于非平滑数据流形或复杂的高维分布，该假设可能不成立，导致关键时间窗的理论保证失效。当前论文未提供该假设在真实图像扩散模型中成立的经验验证。

**负数据集依赖性。** SGF 的安全性能直接受限于负数据集 $\mathcal{D}^-$ 的覆盖度和质量。当负样本无法充分表征不安全分布时，MMD 势能无法提供有效的排斥梯度。这一局限与 Safe Denoiser 和 SPELL 共享——三者均需要高质量的负样本集合。实验中使用的是固定的 515 张 I2P 负图像，在更开放的安全场景中，负样本的构建本身就是一项非平凡任务。

**模态与调度策略的泛化性。** 理论推导利用了图像扩散模型中后期去噪幅度递减的特性（即噪声水平 σ_t 随时间单调下降）。对于采用渐进加速 unmasking 的扩散语言模型，或视频生成中的不同噪声调度，关键时间窗的存在性及最优窗口长度可能需要重新分析（附录 E.1 对此有简要讨论，但未给出实验验证）。

**计算开销的可控性。** SGF 的推理耗时与 Safe Denoiser 处于同一量级（Table 4：SD-v1.4 + SGF 为 3.22 s/img，SD-v1.4 + SafeDenoiser 为 3.18–3.20 s/img），主要瓶颈在于 MMD 梯度计算需遍历负样本集。当负样本规模增大（如 N=3200），耗时升至 4.29–4.70 s/img，但相比 SAFREE 基线的 4.22 s/img 仍在可接受范围。

### 5. 开放问题

SGF 框架为负引导的研究打开了若干新方向：

1. **放松 Assumption 1。** 如何在不依赖边界层对齐假设的情况下，仍能保证 MMD 引导与理想控制屏障场的有效对齐？这对于将该方法推广到边界层性质未知的应用领域至关重要。

2. **自适应截止时间。** 当前的关键时间窗 $[1.0, s_c]$ 依赖预设的固定窗口，能否基于生成状态在线估计最优的 $s_c$？例如，利用 MMD 势能本身的衰减速率作为关断信号。

3. **跨模态推广。** 在扩散语言模型或视频生成中，关键窗口的形式如何调整？附录 E.1 仅给出了定性讨论，缺乏系统的理论和实验支撑。

4. **负样本效率。** 如何在保持安全性的前提下减少对大规模负样本集的依赖？可能的路径包括负样本的选择性采样、核带宽的自适应调节，或将 MMD 引导与少量负样本的主动学习相结合。

## 原文 PDF

![[paperPDFs/ICLR_2026/SAFETY_GUIDED_FLOW_SGF_A_UNIFIED_FRAMEWORK_FOR_NEGATIVE_GUIDANCE_IN_SAFE_GENERATION.pdf]]
