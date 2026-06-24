---
title: Dynamics-Aware Preference Optimization for Vision-Language Models
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Dynamics_Aware_Preference_Optimization_for_Vision_Language_Models.pdf
project_link: null
code_link: "https://github.com/jushengzhang/Dynamics-Aware-Preference-Optimization"
aliases:
- CDCWDPO
- DAPOVLM
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过对负样本梯度施加 competence-aware 冷却权重（cooling weight），动态抑制简单负样本的影响，同时在困难负样本上保留学习信号。
primary_logic: 对齐不应被视为静态优化问题，而应显式建模学习动态：先通过约束 SFT 平滑损失景观，再用动态冷却权重有针对性地调节梯度，从而缓解挤压效应，实现稳定高效的偏好优化。
claims:
- DPO 的“挤压效应”出现在简单负样本上：损失小但梯度大且未对齐，DPO 的隐式正则化 $(1-a)$ 不足以充分抑制梯度，导致不稳定（§3.2）。
- "所提出的冷却权重 $w_c$ 能够将简单负样本的权重降至接近 0（即 $\\bar{\\ell}_\\theta \\ll \\ell_{\\mathrm{floor}}$ 时 $w_c \\approx 0$），从而消除其梯度影响，而困难负样本仍保持全梯度（§4.2）。"
- CW-DPO 在 COCO 上 CIDEr 达到 142.6，比 vanilla DPO 提高 5.4，且分布偏移更小、后验更平滑（图 4），验证了减轻挤压效应的效果（§5.3）。
- COCO Test 上 CIDEr = 142.6
---

# Dynamics-Aware Preference Optimization for Vision-Language Models

> [!tip] 核心洞察
> 对齐不应被视为静态优化问题，而应显式建模学习动态：先通过约束 SFT 平滑损失景观，再用动态冷却权重有针对性地调节梯度，从而缓解挤压效应，实现稳定高效的偏好优化。

| 字段 | 内容 |
|------|------|
| 中文题名 | 视觉语言模型的动态感知偏好优化 |
| 英文题名 | Dynamics-Aware Preference Optimization for Vision-Language Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Zhang_Dynamics-Aware_Preference_Optimization_for_Vision-Language_Models_CVPR_2026_paper.html) · [Code](https://github.com/jushengzhang/Dynamics-Aware-Preference-Optimization) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | CW-DPO (Cooling-Weighted Direct Preference Optimization) |
| Dataset | COCO Test, MMMU |

> [!tip] 效果简介
> - COCO Test 上，CIDEr 142.6 vs 139.2 (PPO) (+3.4)；CIDEr 142.6 vs 137.2 (DPO) (+5.4)。
> - MMMU 上，Accuracy (%) 74.6 vs 72.2 (PPO) (+2.4%)。

## 概述

视觉语言模型（VLM）的偏好对齐面临一个被忽视的瓶颈：**简单负样本（easy negatives）产生大而无信息量的梯度，导致概率分布向主导模式挤压（squeezing effect），破坏模型校准并造成训练不稳定**。标准 DPO 的隐式正则化不足以充分抑制这些梯度，使得对齐过程在看似收敛的损失曲线下隐藏着分布退化。

本文提出 **CW-DPO（Cooling-Weighted Direct Preference Optimization）**，核心洞察在于：对齐不应被视为静态优化问题，而应**显式建模学习动态**。方法通过两阶段设计实现这一思想：

1. **约束 SFT（Stage 1）**：在标准正样本微调基础上，引入对负样本 NLL 的 ReLU 惩罚，防止模型对负样本过度自信，从而平滑损失景观。
2. **冷却加权 DPO（Stage 2）**：对负样本梯度施加 competence-aware 冷却权重 $w_c$，动态抑制简单负样本的梯度影响，同时保留困难负样本上的学习信号。

在 COCO 测试集上，CW-DPO 的 CIDEr 达到 **142.6**，比 vanilla DPO 提升 **+5.4**，比 PPO 提升 **+3.4**；在 MMMU 上准确率提升 **+2.4%**（74.6 vs 72.2）。消融实验证实，移除 Smooth SFT 阶段导致 CIDEr 下降约 5 个点，用固定常数替代自适应冷却权重同样损害性能，验证了动态建模与冷却机制的必要性。

**方法定位**：CW-DPO 在偏好优化方法谱系中独树一帜——它既不需要奖励模型（区别于 RLHF/PPO），又超越了标准 DPO 及其变体（如 V-DPO、OPA-DPO、GRPO），首次将学习动态建模与能力感知加权引入 VLM 对齐，实现了稳定高效的偏好优化。

## 背景与动机

视觉语言模型（VLMs）在图像描述、视觉问答等任务上取得了显著进展，但其生成质量与人类偏好之间仍存在明显差距。为使模型输出更符合人类期望，研究者广泛采用偏好对齐（preference alignment）技术，其中**直接偏好优化（DPO）**（Rafailov et al., NeurIPS 2023）因无需显式训练奖励模型而成为主流范式。然而，DPO 及其变体在 VLM 对齐中暴露出一个关键瓶颈：**训练不稳定与校准退化**。

### 挤压效应：DPO 的隐忧

论文通过梯度分析揭示了这一瓶颈的根源——**挤压效应（squeezing effect）**。在 DPO 训练中，当负样本 $y_l$ 是模型已能轻松拒绝的“简单负样本”（easy negative）时，其损失值很小，但对应的梯度分量 $G_t^l$ 却不成比例地大且充满噪声。标准 DPO 的隐式正则化因子 $(1-a)$ 不足以充分抑制这些无信息量的梯度，导致概率分布向主导模式挤压，破坏输出的多样性与校准性。简言之，**简单负样本产生了大而无用的梯度，成为训练不稳定的直接源头**。

### 现有方法的局限

现有偏好优化方法多将对齐视为静态优化问题，忽视了学习过程中的动态特性：

- **SFT**（Ouyang et al., 2022）仅利用正例训练，缺乏对负样本的显式建模，难以抑制不良生成。
- **RLHF (PPO)**（Kaufmann et al., 2024）依赖在线奖励模型，训练复杂且不稳定。
- **DPO 及其变体**（如 V-DPO, GRPO, OPA-DPO）虽简化了流程，但均未显式建模学习动态，未能针对性解决简单负样本带来的梯度失衡问题。

如 **Table 1** 所示，现有方法在学习动态建模（learning dynamics modeling）和能力感知加权（competence-aware weighting）两个维度上存在系统性缺失。

### 核心动机：从静态优化到动态感知

本文的核心洞察在于：**对齐不应被视为静态优化问题，而应显式建模学习动态**。具体而言，需要：

1. **平滑损失景观**：在偏好优化前，通过约束 SFT 减少模型对简单负样本的过度自信，为后续对齐提供稳定的初始条件。
2. **动态梯度调控**：在偏好优化阶段，根据模型对负样本的实际置信度自适应地缩放梯度，使简单负样本的更新被抑制，而困难负样本保留完整的学习信号。

基于这一动机，论文提出 **CW-DPO（Cooling-Weighted Direct Preference Optimization）**，通过两阶段策略——约束 SFT 与冷却加权 DPO——实现动态感知的偏好对齐，从根本上缓解挤压效应，提升训练的稳定性与生成质量。

## 核心创新

CW-DPO 的核心创新在于将偏好对齐从静态优化重新定义为**动态感知的学习过程**，通过两个高度耦合的 changed slots 解决标准 DPO 中简单负样本引发的“挤压效应”（squeezing effect）。

### 瓶颈洞察：简单负样本的梯度失衡

标准 DPO 损失对正负样本施加对称的隐式正则化 $(1-a)$，其梯度可分解为：

$$G_t^{\mathrm{DPO}} = \nabla_z \mathcal{L}_{\mathrm{DPO}} = \beta(1-a)\left((g_w - g_{\mathrm{ref}}^w) - (g_l - g_{\mathrm{ref}}^l)\right)$$

当 $y_l$ 为“简单负样本”（模型已能自信拒绝的样本）时，失败者分量 $G_t^l$ 变得不成比例地大且充满噪声。这些无信息量的梯度会将概率分布向主导模式挤压，破坏校准并导致训练不稳定。DPO 的隐式正则化不足以充分抑制这种梯度——这是现有偏好优化方法**普遍忽视的学习动态问题**。

### Changed Slot 1：约束 SFT 平滑损失景观（Stage 1）

标准 SFT 仅最小化正样本的负对数似然（NLL），容易导致模型对负样本过度自信，为后续偏好优化埋下梯度失衡的隐患。CW-DPO 将此 slot 替换为**约束 SFT 损失**：

$$\mathcal{L}_{\mathrm{SFT-C}} = \mathbb{E}_{\mathrm{batch}}[-\log \pi_{\theta}(y^+|x)] + \lambda \,\mathrm{ReLU}(C - \mathbb{E}_{\mathrm{batch}}[-\log \pi_{\theta}(y^-|x)])$$

该损失在优化正样本 NLL 的同时，通过 ReLU 惩罚项强制负样本 NLL 不低于阈值 $C$，防止模型对“温和负样本”（gentle negatives）产生过度自信。这一阶段不进行偏好对比，而是为后续优化铺设平滑的损失景观，从根本上缓解挤压效应的产生条件。

### Changed Slot 2：能力感知冷却权重调节负样本梯度（Stage 2）

DPO 对正负样本梯度施加对称权重，无法区分简单负样本与困难负样本。CW-DPO 将此 slot 替换为**非对称冷却权重**，作用于负样本的 log-概率差异 $\Delta_l$：

$$\mathcal{L}_{\mathrm{CW-DPO}} = - \mathbb{E}\big[ \log \sigma \big( \beta ( \Delta_w - w_c(\theta; y_l, \chi) \cdot \Delta_l ) \big) \big]$$

其中冷却权重 $w_c$ 基于模型对负样本的**平均 token 对数概率**自适应计算：

$$w_c(\theta; y_l, \chi) = \sigma\left( \frac{\bar{\ell}_{\theta}(y_l | \chi) - \ell_{\mathrm{floor}}}{\tau} \right)$$

$$\bar{\ell}_{\theta}(y \mid \chi) = \frac{1}{L} \sum_{l=1}^{L} \log \pi_{\theta}(y_{l} \mid \chi_{\leq l})$$

该设计的动力学效果是：当模型对负样本置信度极低（$\bar{\ell}_\theta \ll \ell_{\mathrm{floor}}$，即简单负样本）时，$w_c \approx 0$，梯度被近乎消除；当负样本处于模型能力边界（$\bar{\ell}_\theta \ge \ell_{\mathrm{floor}}$，即困难负样本）时，$w_c \approx 1$，保留完整学习信号。这实现了**基于模型当前能力的动态梯度调节**，而非固定常数抑制。

### 两阶段耦合的因果逻辑

两个 changed slots 并非独立改进，而是形成因果链条：Stage 1 的约束 SFT 通过抑制过度自信来**预处理损失景观**，使 Stage 2 的冷却权重能更准确地识别简单与困难负样本的边界；Stage 2 则利用这一平滑基础，通过能力感知加权**精准消除挤压效应的梯度源头**。消融实验验证了这一耦合的必要性：移除 Smooth SFT 导致 COCO CIDEr 下降约 5 个点（142.6 vs 137.6），而将自适应冷却权重替换为固定常数同样损害性能。

与现有偏好优化方法的属性对比（Table 1）进一步表明，CW-DPO 是首个**同时显式建模学习动态并引入能力感知加权**的 VLM 对齐方法，这一组合是其在多个基准上超越 **DPO**（Rafailov et al., NeurIPS 2023）、**PPO**（Kaufmann et al., 2024）和 **OPA-DPO**（Yang et al., CVPR 2025）等方法的根本原因。

## 整体框架

CW-DPO 采用两阶段优化范式，将偏好对齐显式建模为一个动力学感知的学习过程。其核心思想是：**先通过约束 SFT 平滑损失景观，再通过动态冷却权重有针对性地调节负样本梯度**，从而缓解标准 DPO 中简单负样本引起的“挤压效应”（squeezing effect）。

### 两阶段流水线

**Stage 1：约束 SFT (Constrained SFT)**
第一阶段在标准正样本监督之外，引入“温和负样本”（gentle negatives）构建平滑监督信号。具体而言，在最小化正样本 NLL 的同时，通过 ReLU 惩罚项约束负样本的 NLL 不低于阈值 $C$，防止模型对负样本区域产生过度自信。该阶段的损失函数为：

$$\mathcal{L}_{\mathrm{SFT-C}} = \mathbb{E}_{\mathrm{batch}}[-\log \pi_{\theta}(y^+|x)] + \lambda \mathrm{ReLU}(C - \mathbb{E}_{\mathrm{batch}}[-\log \pi_{\theta}(y^-|x)])$$

这一设计的作用是**为后续偏好学习铺设更平滑的损失景观**，避免模型过早地将概率质量挤向主导模式。实验验证（Figure 3）表明，SFT-C 相比标准 SFT 能维持更高的生成熵，CIDEr 和 SPICE 指标也更高，证实其有效缓解了早期压缩效应。

**Stage 2：冷却加权 DPO (Cooling-Weighted DPO)**
第二阶段在 DPO 框架基础上，对负样本的 log-概率差异 $\Delta_l$ 不对称地施加冷却权重 $w_c$，得到 CW-DPO 损失：

$$\mathcal{L}_{\mathrm{CW-DPO}} = -\mathbb{E}\big[\log \sigma(\beta(\Delta_w - w_c(\theta; y_l, \chi) \cdot \Delta_l))\big]$$

冷却权重 $w_c$ 基于模型对负样本的 **per-token 平均 log-概率** 自适应计算：

$$w_c(\theta; y_l, \chi) = \sigma\left(\frac{\bar{\ell}_{\theta}(y_l \mid \chi) - \ell_{\mathrm{floor}}}{\tau}\right)$$

其中 $\bar{\ell}_{\theta}(y_l \mid \chi) = \frac{1}{L}\sum_{l=1}^{L}\log \pi_{\theta}(y_l \mid \chi_{\leq l})$ 衡量模型对负样本序列的平均置信度。当模型对负样本置信度极低（$\bar{\ell}_{\theta} \ll \ell_{\mathrm{floor}}$，即“简单负样本”）时，$w_c \approx 0$，梯度被近乎清零；当置信度较高（$\bar{\ell}_{\theta} \ge \ell_{\mathrm{floor}}$，即“困难负样本”）时，$w_c \approx 1$，保留完整学习信号。

### 模块关系与数据流

整个流水线的数据流与模块关系如下：

1. **输入**：配对的偏好数据 $\mathcal{D} = \{(x, y^+, y^-)\}$，包含图像-文本上下文 $x$、正样本响应 $y^+$ 和负样本响应 $y^-$。
2. **Stage 1**：使用 75% 的数据进行约束 SFT，输出一个经过平滑预训练的模型 $\theta_{\mathrm{SFT-C}}$。此阶段仅使用温和负样本（包含微小错误的响应），避免强负样本过早引入尖锐梯度。
3. **Stage 2**：在剩余 25% 的数据上进行 CW-DPO 偏好对齐。对于每个偏好对，计算 $\Delta_w$ 和 $\Delta_l$，并通过冷却权重 $w_c$ 调节 $\Delta_l$ 的贡献。最终输出对齐后的模型 $\theta_{\mathrm{CW-DPO}}$。

### 与现有方法的本质区别

Table 1 将 CW-DPO 与代表性偏好优化方法进行了六项属性对比。CW-DPO 的独特之处在于**同时集成了学习动力学建模和基于能力的梯度加权**：标准 DPO (Rafailov et al., NeurIPS 2023) 对正负样本施加对称的隐式正则化 $(1-a)$，无法区分样本难度；PPO (Kaufmann et al., 2024) 需要在线采样和奖励模型，计算开销大；GRPO (Shao et al., 2024) 引入组正则化但未显式建模难度；OPA-DPO (Yang et al., CVPR 2025) 采用在线偏好增强，但同样缺乏对负样本梯度的精细控制。CW-DPO 通过两阶段设计——先平滑后冷却——实现了对学习轨迹的全程动态调控。

### 补充图表

![[assets/figures/papers/paper_list_l2655_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_Dynamics_Aware_P/figures/002_Figure_1.jpg]]
*Figure 1: Two-stage optimization process of CW-DPO. Stage*

## 核心模块与公式推导

CW-DPO 由两个顺序阶段构成：**第一阶段**通过约束 SFT 平滑损失景观，**第二阶段**通过冷却加权 DPO 实现动态感知的偏好优化。以下逐一展开关键模块与核心公式。

### 第一阶段：约束 SFT（Smooth SFT）

标准 SFT 仅最小化正样本的负对数似然（NLL），容易导致模型对负样本过度自信，使后续偏好优化的损失景观变得尖锐。第一阶段引入“温和负样本”（gentle negatives），对负样本的 NLL 施加下界约束，防止模型将概率质量过度集中于正例模式。

约束优化问题的原始形式为：

$$
\min_{\theta} \mathbb{E}_{(x,y^+)\sim\mathcal{D}}[-\log \pi_{\theta}(y^+|x)] \quad \text{s.t.} \quad \mathbb{E}_{(x,y^-)\sim\mathcal{D}}[-\log \pi_{\theta}(y^-|x)] \ge C
$$

其中 $C$ 是负样本 NLL 的下界阈值。通过拉格朗日松弛，得到可微的 **Smoothed SFT 损失**：

$$
\mathcal{L}_{\mathrm{SFT-C}} = \mathbb{E}_{\mathrm{batch}}[-\log \pi_{\theta}(y^+|x)] + \lambda \, \mathrm{ReLU}\!\left(C - \mathbb{E}_{\mathrm{batch}}[-\log \pi_{\theta}(y^-|x)]\right)
$$

- **变量含义**：$\pi_{\theta}$ 为当前策略模型；$y^+$ 为正样本，$y^-$ 为负样本；$\lambda$ 为惩罚系数；$\mathrm{ReLU}(\cdot)$ 仅在负样本 NLL 低于阈值 $C$ 时激活惩罚。
- **作用机制**：该损失在提升正样本似然的同时，抑制模型对负样本的过度自信，从而平滑损失景观，为第二阶段偏好优化奠定稳定基础。Figure 3 的验证曲线表明，SFT-C 相比标准 SFT 维持了更高的生成熵（更少的挤压效应）和整体质量。

![[assets/figures/papers/paper_list_l2655_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_Dynamics_Aware_P/figures/004_Figure_3.jpg]]
*Figure 3: Validation of Stage 1 Constrained SFT (SFT-C) vs. standard SFT on: (1) loss; (2) entropy; (3) CIDEr; and (4) SPICE for Top-5 generations. SFT-C sustains higher entropy (less squeezing) and overall quality*

### 第二阶段：冷却加权 DPO（CW-DPO）

第二阶段的核心创新在于对标准 DPO 损失的负样本梯度施加 **能力感知冷却权重**（competence-aware cooling weight），动态抑制简单负样本的梯度贡献，同时保留困难负样本的学习信号。

#### 标准 DPO 的梯度分解

标准 DPO 损失关于 logits $z$ 的梯度可分解为：

$$
G_t^{\mathrm{DPO}} = \nabla_z \mathcal{L}_{\mathrm{DPO}} = \beta(1-a)\left((g_w - g_{\mathrm{ref}}^w) - (g_l - g_{\mathrm{ref}}^l)\right)
$$

其中 $\beta$ 为温度系数，$a = \sigma(\beta(\Delta_w - \Delta_l))$ 为隐式正则化权重，$g_w$、$g_l$ 分别为正负样本的 logit 梯度，$g_{\mathrm{ref}}^w$、$g_{\mathrm{ref}}^l$ 为参考模型的对应项。**关键瓶颈**在于：当 $y_l$ 是简单负样本时，失败者分量 $(g_l - g_{\mathrm{ref}}^l)$ 变得不成比例地大且嘈杂，而隐式正则化因子 $(1-a)$ 不足以充分抑制该分量，从而产生“挤压效应”（squeezing effect），破坏概率分布的校准并导致训练不稳定。

#### 冷却权重 $w_c$

为解决上述问题，CW-DPO 引入基于模型对负样本平均置信度的冷却权重。首先定义 **每 token 平均对数概率**：

$$
\bar{\ell}_{\theta}(y \mid \chi) = \frac{1}{L} \sum_{l=1}^{L} \log \pi_{\theta}(y_{l} \mid \chi_{\leq l})
$$

该量衡量模型对序列 $y$ 的整体置信度：$\bar{\ell}_{\theta}$ 越低，表示模型越确信该样本为负例（即“简单负样本”）。基于此构建 **冷却权重**：

$$
w_{c}(\theta ; y_{l}, \chi) = \sigma\!\left( \frac{\bar{\ell}_{\theta}(y_{l} \mid \chi) - \ell_{\mathrm{floor}}}{\tau} \right)
$$

- **变量含义**：$\ell_{\mathrm{floor}}$ 为置信度下界阈值；$\tau$ 为温度参数控制过渡平滑度；$\sigma(\cdot)$ 为 sigmoid 函数。
- **行为特性**：
  - 当 $\bar{\ell}_{\theta} \ll \ell_{\mathrm{floor}}$（模型高度确信为负样本）时，$w_c \approx 0$，**完全消除**该负样本的梯度贡献。
  - 当 $\bar{\ell}_{\theta} \ge \ell_{\mathrm{floor}}$（模型对负样本不确定，即困难负样本）时，$w_c \approx 1$，**保留完整**学习信号。

#### CW-DPO 损失函数

将冷却权重不对称地施加于负样本的对数概率差 $\Delta_l$，得到 **CW-DPO 损失**：

$$
\mathcal{L}_{\mathrm{CW-DPO}} = - \mathbb{E} \big[ \log \sigma \big( \beta ( \Delta_{w} - w_{c}(\theta ; y_{l}, \chi) \cdot \Delta_{l} ) \big) \big]
$$

其中 $\Delta_w = \log\pi_{\theta}(y_w|x) - \log\pi_{\mathrm{ref}}(y_w|x)$，$\Delta_l = \log\pi_{\theta}(y_l|x) - \log\pi_{\mathrm{ref}}(y_l|x)$。通过 $w_c$ 对 $\Delta_l$ 的缩放，CW-DPO 实现了对负样本梯度的精确控制：简单负样本被有效冷却，困难负样本保持原有对比强度，从而缓解挤压效应、稳定训练并改善校准。

### 两阶段协同

两个阶段形成因果链条：**Stage 1** 通过约束 SFT 平滑损失景观，降低模型对负样本的初始过度自信；**Stage 2** 在此基础上利用冷却权重进一步精细化调节梯度，使偏好优化在稳定且校准良好的概率分布上进行。消融实验（Table 3）验证了两阶段的必要性：移除 Smooth SFT 导致 COCO CIDEr 下降约 5 个点，省略 CW-DPO 阶段则跨任务性能全面下降。

## 实验与分析

### 核心瓶颈验证：DPO 的“挤压效应”

CW-DPO 的设计动机源于对 DPO 训练动态的深入分析。研究发现，标准 DPO 在偏好对齐过程中存在一种**挤压效应（squeezing effect）**：当负样本 $y_l$ 是“简单负样本”（easy negative）时，模型已能轻松区分正负样本，此时 DPO 损失值很小，但负样本侧的梯度分量 $G_t^l$ 却异常大且充满噪声。这个不成比例的大梯度会将概率分布向主导模式挤压，破坏模型校准并导致训练不稳定。DPO 自带的隐式正则化因子 $(1-a)$ 不足以有效抑制这种梯度失衡。

### 主实验结果

CW-DPO 在多个视觉语言基准上取得了领先性能。**Table 2** 汇总了 COCO、Flickr30k、NoCaps 的图像描述任务以及 MMMU、MMBench 的多模态理解任务上的全面对比。

![[assets/figures/papers/paper_list_l2655_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_Dynamics_Aware_P/figures/005_Table_2.jpg]]
*Table 2: Performance comparison on vision-language benchmarks. For COCO, Flickr30k, and NoCaps, we report BLEU-4 (B@4), METEOR (M), CIDEr (C), and SPICE (S), with NoCaps split into In, Near, Out, and Entire. We also report accuracy on MMMU and MMBench1.1. Best results are in bold*

在 **COCO Test** 上，CW-DPO 取得了 **CIDEr 142.6** 的最佳成绩，相较于 PPO（139.2）提升 **+3.4**，相较于 vanilla DPO（137.2）提升 **+5.4**。这一显著提升直接验证了冷却加权机制对挤压效应的缓解作用。在 Flickr30k 和 NoCaps 上，CW-DPO 同样在 BLEU-4、METEOR、CIDEr、SPICE 四项指标上全面超越现有偏好优化方法。

在多模态理解任务上，CW-DPO 同样表现稳健：**MMMU 准确率达到 74.6%**，比 PPO（72.2%）提升 **+2.4%** 绝对准确率；MMBench 上也取得了具有竞争力的结果。这表明冷却加权策略在提升生成质量的同时，并未牺牲模型的通用理解能力。

### 挤压效应缓解的实证分析

**Figure 4** 从三个维度直观展示了 CW-DPO 对 DPO 挤压效应的缓解效果：

1. **分布偏移更小**（左图）：CW-DPO 在训练过程中引起的概率分布偏移显著小于 vanilla DPO，说明冷却权重有效抑制了简单负样本对分布的过度挤压。
2. **后验更平滑**（中图）：CW-DPO 产生的后验概率分布更加平滑，避免了 vanilla DPO 中出现的尖锐峰值，这意味着模型保留了更好的校准特性。
3. **生成质量提升且校准更好**（右图）：在 CIDEr 提升的同时，模型校准误差降低，证明了“抑制简单负样本梯度 → 缓解挤压 → 改善校准”这一因果链的有效性。

### Stage 1 约束 SFT 的效果

**Figure 3** 对比了 Stage 1 约束 SFT（SFT-C）与标准 SFT 在验证集上的表现。SFT-C 在训练过程中持续保持更高的熵值（更少的挤压），同时在 CIDEr 和 SPICE 指标上始终优于标准 SFT。这验证了通过 ReLU 惩罚约束负样本 NLL 下限的策略，确实能够在偏好学习之前平滑损失景观、防止过度自信，为 Stage 2 的冷却加权 DPO 奠定更稳定的基础。

### 消融实验

**Table 3** 的消融实验系统评估了 CW-DPO 各组件在 COCO Test、MMMU 和 MMBench 上的贡献：

- **移除 Smooth SFT 阶段**：COCO CIDEr 从 142.6 下降约 5 个点至 137.6，MMMU 准确率从 74.6 降至 72.9，MMBench 从 87.6 降至 86.7。这表明 Stage 1 的约束微调对于整体性能至关重要，仅靠 Stage 2 的冷却加权无法完全弥补损失景观不平滑带来的影响。
- **移除 CW-DPO 阶段（仅保留 SFT-C）**：CIDEr 降至 140.7，MMMU 降至 72.9，MMBench 降至 86.7。偏好优化阶段带来的负样本对比学习信号对性能提升有独立贡献。
- **用固定常数替代自适应冷却权重**：将 $w_c$ 固定为常数而非基于模型置信度自适应缩放，会导致性能下降。这验证了 competence-aware 的动态冷却机制——根据 $\bar{\ell}_\theta(y_l \mid \chi)$ 自适应调节梯度——是方法的核心创新，简单常数加权无法区分简单负样本与困难负样本。

### 方法特性对比

**Table 1** 将 CW-DPO 与代表性偏好优化方法在六项属性上进行系统对比。CW-DPO 独特地同时整合了**学习动态建模**（learning dynamics modeling）与**能力感知加权**（competence-aware weighting），这是现有方法（包括 DPO、V-DPO、GRPO、OPA-DPO 等）所不具备的。这种双重机制使得 CW-DPO 能够在稳定训练的同时实现高效的偏好对齐。

### 失败模式与局限性

尽管 CW-DPO 在主流基准上表现优异，仍需注意以下局限：

1. **数据依赖性**：当前框架假设可以获取配对的偏好数据（包含可靠的正负样本监督）。在无监督或弱标注场景下，方法适用性受限。
2. **超参数敏感性**：冷却权重引入了 $\tau$ 和 $\ell_{\mathrm{floor}}$ 两个超参数。消融实验表明自适应冷却优于固定常数，但最优参数可能需要针对不同数据集进行调优，尚未验证跨数据集的鲁棒性。
3. **任务范围限制**：目前仅在图像描述和多模态理解基准上验证，尚未探索 CW-DPO 在交互式或长序列多模态推理任务中的适用性。

### 补充图表

![[assets/figures/papers/paper_list_l2655_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_Dynamics_Aware_P/figures/006_Figure_4.jpg]]
*Figure 4: CW-DPO alleviates the squeezing effect of vanilla DPO. It yields smaller distribution shifts (left), smoother posteriors (middle), and improved generation quality with better calibration (right)*

![[assets/figures/papers/paper_list_l2655_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_Dynamics_Aware_P/figures/007_Table_3.jpg]]
*Table 3: Ablation study of CW-DPO on COCO Test, MMMU, and MMBench1.1*

![[assets/figures/papers/paper_list_l2655_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_Dynamics_Aware_P/figures/001_Table_1.jpg]]
*Table 1: Comparison with representative preference optimization methods. CW-DPO uniquely integrates learning dynamics modeling and competence-aware weighting for stable VLM alignment*

## 方法谱系与知识库定位

### 与现有偏好优化方法的关系

CW-DPO 处于视觉语言模型（VLM）偏好对齐的研究脉络中，其核心贡献在于首次将“学习动态建模”显式引入对齐过程。与现有方法的对比如下：

- **DPO** (Rafailov et al., NeurIPS 2023)：作为无需奖励模型的直接偏好优化基线，DPO 通过隐式正则化 $(1-a)$ 同时对正负样本梯度进行缩放。然而，本文的梯度分析揭示，当负样本为“简单负样本”（easy negatives）时，该隐式正则化不足以抑制失败者分量 $G_t^l$ 的过度增长，导致概率分布向主导模式挤压（squeezing effect），破坏校准并造成训练不稳定。CW-DPO 通过不对称地施加冷却权重 $w_c$，在负样本梯度上实现精确控制，从根本上缓解了这一问题。

- **RLHF (PPO)** (Kaufmann et al., 2024)：依赖独立奖励模型的在线对齐方法，需要额外的奖励建模和在线采样开销。CW-DPO 在 COCO 上 CIDEr 达到 142.6，比 PPO 的 139.2 高出 3.4 个点，同时在 MMMU 上准确率提升 2.4%（74.6 vs. 72.2），表明在无需奖励模型的前提下可获得更优性能。

- **V-DPO** (Xie et al., EMNLP 2024)：在 DPO 框架中引入视觉偏好信息，但未处理梯度不平衡问题。CW-DPO 的冷却权重机制与视觉偏好信息正交，可视为对 DPO 类方法的通用增强。

- **GRPO** (Shao et al., 2024)：通过组正则化稳定偏好优化，但缺乏对样本难度动态的显式建模。CW-DPO 的 competence-aware 冷却权重提供了更细粒度的样本级梯度调控。

- **OPA-DPO** (Yang et al., CVPR 2025)：在线偏好增强的 DPO 变体，侧重于偏好数据的在线扩充。CW-DPO 聚焦于训练动态本身，两阶段设计（约束 SFT + 冷却加权 DPO）与在线数据增强策略互补。

**Table 1** 从六个维度系统对比了 CW-DPO 与代表性方法：CW-DPO 是唯一同时整合“学习动态建模”和“能力感知加权”的方法，实现了 VLM 对齐的稳定性与高效性。

### 适用边界

CW-DPO 的设计基于以下前提假设，这些假设定义了其适用范围：

1. **配对偏好数据可获取**：方法假设训练数据包含可靠的正负样本对（$(y^+, y^-)$），其中负样本包含可辨识的细粒度错误。在无监督或仅弱标注的场景下，当前框架无法直接应用。

2. **两阶段训练范式**：Stage 1 使用 75% 数据进行约束 SFT，Stage 2 使用剩余 25% 数据进行偏好对齐。该数据划分策略的有效性依赖于数据集规模和质量，在小规模数据集上可能需要调整比例。

3. **冷却权重超参数敏感性**：冷却权重 $w_c(\theta; y_l, \chi) = \sigma\left(\frac{\bar{\ell}_\theta(y_l | \chi) - \ell_{\mathrm{floor}}}{\tau}\right)$ 引入了温度参数 $\tau$ 和置信度阈值 $\ell_{\mathrm{floor}}$。消融实验表明，用固定常数替代自适应冷却权重会损害性能，说明参数调优对方法效果至关重要，且可能需要针对不同数据集进行适配。

4. **VLM 特定场景**：当前验证集中在图像描述（COCO、Flickr30k、NoCaps）和多模态理解（MMMU、MMBench）任务上，尚未在交互式对话或长序列多模态推理任务中进行验证。

### 局限与开放问题

**已知局限**：

- 冷却权重引入了 $\tau$ 和 $\ell_{\mathrm{floor}}$ 两个额外超参数，增加了调参负担。消融实验证实移除自适应冷却（固定 $w_c$ 为常数）会损害性能，但未提供跨数据集的参数敏感性分析。
- 方法假设可获取配对的偏好数据，在无监督或弱标注场景下受限。
- 尚未探索 CW-DPO 在交互式或长序列多模态推理任务（如多轮 VQA、视频理解）中的适用性。

**开放问题**：

1. **无监督扩展**：如何将 CW-DPO 的冷却加权机制扩展到完全无监督或弱标记的设置中？例如，能否利用模型自身的置信度估计自动构建正负样本对？

2. **自适应冷却策略**：能否开发自适应调度或元学习的冷却策略（如根据训练进度动态调整 $\tau$ 和 $\ell_{\mathrm{floor}}$），以减少手动调参需求？

3. **长周期推理任务**：CW-DPO 在交互式、长周期多模态推理任务中的适用性如何？冷却权重机制是否需要针对序列级反馈进行重新设计？

4. **与在线对齐的结合**：CW-DPO 的两阶段静态训练能否与在线偏好采样（如 OPA-DPO 的策略）结合，实现训练过程中的动态负样本难度感知？

## 原文 PDF

![[paperPDFs/CVPR_2026/Dynamics_Aware_Preference_Optimization_for_Vision_Language_Models.pdf]]
