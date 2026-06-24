---
title: "AlphaFlow: Understanding and Improving MeanFlow Models"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/AlphaFlow_Understanding_and_Improving_MeanFlow_Models.pdf
aliases:
- AlphaFlow
- "α-Flow"
tags:
- ICLR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/generative_models_and_autoencoders
core_operator: |
  将MeanFlow目标分解为轨迹流匹配L_TFM与轨迹一致性L_TC，提出α-Flow损失族和从α=1退火到α→0的课程训练来缓解梯度冲突。
primary_logic: |
  先用损失分解和梯度余弦相似度定位MeanFlow训练中的目标冲突，再用α参数统一轨迹流匹配、Shortcut Model和MeanFlow，并通过三阶段退火训练逐步从流匹配监督过渡到MeanFlow目标。
claims:
- "AlphaFlow将MeanFlow损失分解为L_TFM和L_TC，并指出两者在训练中梯度高度负相关。"
- "α-Flow损失族在α=1、α=1/2和α→0时分别对应轨迹流匹配、Shortcut Model和MeanFlow梯度。"
- "在ImageNet-1K 256×256上，α-Flow-XL/2+达到1-NFE FID 2.58和2-NFE FID 2.15，优于MeanFlow-XL/2*。"
---

# AlphaFlow: Understanding and Improving MeanFlow Models

> [!tip] 核心洞察
> 将MeanFlow目标分解为L_TFM和L_TC，发现两者梯度冲突。通过引入α-Flow损失族，采用从轨迹流匹配（α=1）平滑退火到MeanFlow（α→0）的课程策略，解耦了冲突目标，实现了更好的收敛，并减少了对边界情况流匹配监督（r=t）的依赖。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | AlphaFlow：理解与改进MeanFlow模型 |
| 英文题名 | AlphaFlow: Understanding and Improving MeanFlow Models |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=adacb4JTIv); [GitHub](https://github.com/snap-research/alphaflow) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/generative_models_and_autoencoders |
| Method | α-Flow |
| Dataset | ImageNet-1K 256×256 |

> [!tip] 效果简介
> - ImageNet-1K 256×256 上，FID (1-NFE) 为 2.58，对比 3.47 (MeanFlow-XL/2*)，变化 -0.89 (25.6% improvement)。
> - ImageNet-1K 256×256 上，FID (2-NFE) 为 2.15，对比 2.46 (MeanFlow-XL/2*)，变化 -0.31 (12.6% improvement)。
> - ImageNet-1K 256×256 上，FDD (1-NFE) 为 148.4，对比 185.8 (MeanFlow-XL/2*)，变化 -37.4 (20.1% improvement)。

## 概述

本文提出 **α-Flow**，一种用于改进少步流匹配生成模型（MeanFlow）训练的统一框架。核心发现是：MeanFlow的训练目标可分解为**轨迹流匹配（L_TFM）**和**轨迹一致性（L_TC）**两个分量，两者在优化过程中梯度高度负相关（余弦相似度通常低于-0.4），导致优化冲突和收敛缓慢。α-Flow通过引入超参数α，将轨迹流匹配（α=1）、Shortcut Model（α=1/2）和MeanFlow（α→0）统一在一个损失函数族中，并采用从α=1退火到α→0的课程学习策略，有效解耦了冲突目标。在ImageNet-1K 256×256上，α-Flow-XL/2+以1-NFE达到FID 2.58，2-NFE达到FID 2.15，均显著优于MeanFlow基线。

## 背景与动机

## 1 少步生成模型的发展

少步扩散和流匹配模型旨在通过少量函数评估（NFE）实现高质量生成。现有方法包括：

- **流匹配（Flow Matching）**：训练网络匹配沿轨迹的ground-truth向量场，损失函数为 $\mathcal{L}_{\mathtt{FM}}(\pmb{\theta}) = \mathbb{E}_{t, \pmb{x}, \pmb{z}_t}[||\pmb{v}_{\pmb{\theta}}(\pmb{z}_t, t) - \pmb{v}_t||^2]$（Equation 1）。
- **一致性模型（Consistency Models）**：通过离散一致性训练 $\mathcal{L}_{\mathtt{CT}_\mathtt{d}}(\pmb\theta) = \mathbb{E}_{t,s,z_t}\left[ \lVert \pmb f_\pmb\theta(z_t, t) - \pmb f_{\pmb\theta^-}(z_s, s) \rVert_2^2 \right]$（Equation 2）或连续一致性训练 $\mathcal{L}_{\mathrm{CT}_c}(\pmb{\theta}) = 2\mathbb{E}_{t,z_t}\left[ \pmb{f}_{\pmb{\theta}}^\top(z_t, t) \frac{\mathrm{d}\pmb{f}_{\pmb{\theta}^-}(z_t, t)}{\mathrm{d}t} \right]$（Equation 3）强制一致性属性。
- **Shortcut Model**：损失函数为 $\mathcal{L}_{\mathrm{SC}}(\theta) = \underset{t,r,z_t}{\mathbb{E}}\left[ \| u_\theta(z_t, r, t) - u_{\theta^-}(z_t, s, t)/2 - u_{\theta^-}(z_s, r, s)/2 \|_2^2 \right]$（Equation 4），强制单个捷径步与两个连续半尺寸步之间的一致性。
- **MeanFlow**：损失函数为 $\mathcal{L}_{\mathtt{MF}}(\theta) = \underset{t,r,z_t}{\mathbb{E}} \left[ \left\| u_\theta(z_t, r, t) - v_t + (t - r) \frac{\mathrm{d} u_{\theta^-}(z_t, r, t)}{\mathrm{d} t} \right\|_2^2 \right]$（Equation 5），训练模型估计区间[r, t]上的平均速度。

## 2 MeanFlow的瓶颈分析

本文的核心洞察来自对MeanFlow损失的分解。将MeanFlow损失展开可得（Equation 6）：

$\mathcal{L}_{\mathtt{MF}}(\theta) = \underbrace{\mathbb{E}_{t,r,z_t} \left[ \| u_\theta(z_t, r, t) - v_t \|_2^2 \right]}_{\mathcal{L}_{\mathtt{TFM}}} + \underbrace{\mathbb{E}_{t,r,z_t} \left[ 2(t-r) \cdot u_\theta^\top(z_t, r, t) \frac{\mathrm{d} u_{\theta^-}(z_t, r, t)}{\mathrm{d} t} \right]}_{\mathcal{L}_{\mathtt{TC}}} + C$

其中：
- **轨迹流匹配损失（L_TFM）**：$\mathcal{L}_{\mathtt{TFM}} \triangleq \underset{t,r,z_t}{\mathbb{E}} \left[ \| u_\theta(z_t, r, t) - v_t \|_2^2 \right]$（Equation 7），带有额外输入r的流匹配损失。
- **轨迹一致性损失（L_TC）**：强制模型输出在时间上的一致性。

梯度分析（Figure 3a）显示，L_TFM和L_TC的梯度在训练过程中高度负相关，余弦相似度通常低于-0.4。这种梯度冲突导致MeanFlow训练收敛缓慢，且需要75%的训练计算量用于边界情况监督（r=t），这并非MeanFlow的主要关注点。

## 核心创新

## 1 α-Flow损失函数族

本文提出α-Flow损失（Definition 1）：

$\mathcal{L}_{\alpha}(\theta) \triangleq \underset{t,r,z_t}{\mathbb{E}} \left[ \alpha^{-1} \cdot \| u_\theta(z_t, r, t) - (\alpha \cdot \tilde{v}_{s,t} + (1-\alpha) \cdot u_{\theta^-}(z_s, r, s)) \|_2^2 \right]$

其中α是核心超参数，控制中间时间步s在区间(r,t)内的相对位置。该损失统一了多种方法（Theorem 1）：
- **α=1**：等价于轨迹流匹配损失 L_TFM
- **α=1/2**：等价于Shortcut Model损失 L_SC = 1/2 L_{α=1/2}
- **α→0**：梯度等价于MeanFlow损失 ∇L_MF = ∇L_{α→0}
- **r≡0时**：离散CT为L_{α=δ}，连续CT梯度为∇L_{α→0}

## 2 课程学习策略

α-Flow采用三阶段课程学习策略，通过将α从1退火到0实现从轨迹流匹配到MeanFlow的平滑过渡：

1. **轨迹流匹配预训练（α=1）**：纯流匹配监督，为后续阶段提供良好的初始化。
2. **α-Flow过渡阶段（α∈(0,1)）**：α从1平滑退火到接近0，逐步引入一致性约束。
3. **MeanFlow微调阶段（α→0）**：α接近0，近似MeanFlow目标，进行最终优化。

α调度器使用Sigmoid函数：α = Sigmoid_{k_s→k_e, γ, η}(k)，温度γ=25，钳位值η=5×10⁻³。

## 3 自适应损失权重

从MeanFlow的自适应损失推导出α-Flow的自适应损失权重：$\bar{\omega} = \bar{\alpha} / (||\bar{\Delta}||_2^2 + c)$。

## 整体框架

α-Flow的训练框架包含以下模块：

| 模块 | 角色 | 证据锚点 |
|------|------|----------|
| 轨迹流匹配预训练 (α=1) | 训练第一阶段，纯流匹配监督 | Section 4.2 |
| α-Flow过渡阶段 (α∈(0,1)) | 第二阶段，α从1平滑退火到接近0 | Section 4.2 |
| MeanFlow微调阶段 (α→0) | 第三阶段，α接近0，近似MeanFlow目标 | Section 4.2 |
| α调度器 (Sigmoid函数) | 控制α从1到0的退火过程 | Section 4.2 |

训练算法（Algorithm 1）在每个迭代中采样t、r，从调度器获取α，然后根据α是否等于0选择使用L_MF或L_α。

## 核心模块与公式推导

## 1 MeanFlow损失分解

MeanFlow损失可分解为（Equation 6）：

$\mathcal{L}_{\mathtt{MF}}(\theta) = \mathcal{L}_{\mathtt{TFM}} + \mathcal{L}_{\mathtt{TC}} + C$

其中L_TFM提供边界条件，L_TC本身没有边界条件。在无限模型容量假设下（Assumption 1），L_TFM有唯一最优解（Equation 23）：

$\boldsymbol{u}_{\theta,\mathrm{TFM}}^*(\boldsymbol{z}_t, r, t) = \frac{1}{t} \left( \boldsymbol{z}_t - \frac{\mathbb{E}_{\boldsymbol{x} \sim p(\boldsymbol{x})} \left[ \mathcal{N}(\boldsymbol{z}_t; (1-t)\boldsymbol{x}, t^2 \boldsymbol{I}) \cdot \boldsymbol{x} \right]}{\mathbb{E}_{\boldsymbol{x} \sim p(\boldsymbol{x})} \left[ \mathcal{N}(\boldsymbol{z}_t; (1-t)\boldsymbol{x}, t^2 \boldsymbol{I}) \right]} \right)$

而L_TC是u_θ的线性函数，没有下界（Equation 24），任何满足$u_\theta^T \cdot du_{\theta^-}/dt \to -\infty$的函数都能最小化它。

## 2 α-Flow最优解

α-Flow的最优解满足递推关系：

$\boldsymbol{u}_{\theta,\alpha}^*(\boldsymbol{z}_t, \boldsymbol{r}, t) - (1-\alpha) \cdot \boldsymbol{u}_{\theta,\alpha}^*(\boldsymbol{z}_s, \boldsymbol{r}, s) = \alpha \cdot \boldsymbol{u}_{\theta,\mathrm{TH}}^*(\boldsymbol{z}_t, t)$

当α→0时，最优解收敛到MeanFlow最优解：

$\lim_{\alpha\to 0} \boldsymbol{u}_{\theta,\alpha}^*(\boldsymbol{z}_t, r, t) = \frac{1}{t-r} \int_r^t \boldsymbol{u}_{\theta,\mathrm{TFM}}^*(\boldsymbol{z}_t, t) dt = \boldsymbol{u}_{\theta,\mathrm{MF}}^*(\boldsymbol{z}_t, r, t)$

## 3 梯度差异上界

在Lipschitz假设下（Assumption 2），α-Flow与MeanFlow的梯度差异上界为（Equation 49）：

$\left\| \nabla_\theta \mathcal{L}_\alpha(\theta) - \nabla_\theta \mathcal{L}_{\mathrm{MF}}(\theta) \right\|_2 \leq \alpha \cdot C_1 \mathbb{E}_{t,r} \left[ \frac{1}{2} L_2 (t-r)^2 + C_2 (t-r) \right]$

该上界与α线性相关，当α→0时消失。

## 实验与分析

## 1 主要结果

在ImageNet-1K 256×256上的类条件生成结果（Table 1）：

| 方法 | 1-NFE FID | 1-NFE FDD | 2-NFE FID | 2-NFE FDD |
|------|-----------|-----------|-----------|-----------|
| MeanFlow-XL/2* | 3.47 | 185.8 | 2.46 | 108.7 |
| α-Flow-XL/2 | 2.95 | 164.6 | 2.32 | 103.4 |
| α-Flow-XL/2+ | **2.58** | **148.4** | **2.15** | **96.8** |

α-Flow-XL/2+在1-NFE上相比MeanFlow-XL/2*提升25.6%（FID从3.47降至2.58），在2-NFE上提升12.6%（FID从2.46降至2.15）。使用平衡类采样（Table 10）时，α-Flow-XL/2+达到1-NFE FID 2.44和2-NFE FID 1.95。

## 2 消融研究

**调度器消融（Table 2a）**：Sigmoid调度（0K→400K）在α-Flow-B/2上取得最佳FID 40.0（1-NFE）和37.1（2-NFE）。

**流匹配比例消融（Table 2b）**：α-Flow在25%流匹配比例下取得最佳1-NFE FID 40.0，而MeanFlow需要75%比例才能达到最佳FID 43.1。这表明α-Flow减少了对边界情况监督的依赖。

**采样方法对比（Figure 5）**：一致性采样对α-Flow模型效果更好，而ODE采样对MeanFlow-XL/2效果更好。

**α值消融（Table 5c）**：α = 5×10⁻³是最优的一致性步长比例，用作调度器的钳位值。

**自适应损失权重（Table 5b）**：α-Flow的自适应损失权重 ω = α/(||Δ||₂² + c) 优于原始MeanFlow自适应权重。

## 3 视频生成结果

在Kinetics-700视频生成上（Figure 7），α-Flow在所有指标上一致优于MeanFlow：
- 无CFG：NFE1 FID提升2.5，FDD提升21.5，FVD提升21.5
- 有CFG：NFE1 FID提升2.7，FDD提升69.2，FVD提升21.9

## 4 额外实验

- **蒸馏（Table 8）**：进一步提升了α-Flow在NFE 1和NFE 2上的性能。
- **微调（Table 7）**：从预训练流模型微调时，α-Flow在1-NFE上一致优于MeanFlow。
- **引导方法（Table 9）**：CFG引导显著优于u-target引导。
- **批量大小（Table 4）**：批量大小512取得最佳1-NFE FID 3.05。

## 5 公平性说明

- FID评估使用随机类标签采样（从0到999均匀采样），遵循EDM系列标准。
- 平衡类采样（每类50个样本，共1000类）可将FID降低多达10%，但FDD和FCD几乎不受影响。
- 论文建议社区从FID转向与人类感知更相关的指标，如FDD和FCD。

## 方法谱系与知识库定位

## 1 与现有方法的关系

α-Flow损失统一了以下方法：
- **流匹配（Flow Matching）**：α=1时等价
- **Shortcut Model**：α=1/2时等价
- **离散一致性训练（Discrete CT）**：r≡0且α=δ时等价
- **连续一致性训练（Continuous CT）**：α→0时梯度等价
- **MeanFlow**：α→0时梯度等价

## 2 局限性

1. α-Flow损失实现了离散MeanFlow模型的高质量训练，无需JVP计算，但连续目标（α→0）由于一致性目标固有的偏差-方差权衡仍然重要。
2. 梯度分析提供了可操作的见解，但仍然是经验性的，未能从理论角度完全解释为什么流匹配对一致性如此关键。
3. 观察到的更大批量大小的改进可能反映小批量对超参数更敏感，且批量大小缩放存在收益递减。
4. 一致性采样并未提供预期的改进；最优中点始终出现在≈0.5，与默认MeanFlow设置一致。
5. 对MeanFlow目标进行分解训练并单独调整权重函数，结果均差于默认的自适应损失启发式方法。
6. 额外的表示对齐损失带来的收益不足以证明增加训练框架复杂性的合理性。

## 3 开放问题

1. α-Flow与其他少步方法（如FACM）在相同基准上的详细计算成本比较如何？
2. α-Flow损失中shift velocity ṽ_{s,t}的精确定义是什么？
3. 附录E.3中非渐近界的完整证明是什么？
4. α-Flow在更大规模数据集（如ImageNet-512或更高分辨率）上的表现如何？
5. α-Flow框架是否可以扩展到其他生成模型范式（如文本到图像生成）？
6. 梯度冲突的理论解释是否可以进一步形式化，以指导未来更优训练目标的设计？

## 整体框架

![[assets/figures/papers/iclr26_generative_models_diffusion__generative_models_and_autoencoders__b001_adacb4JTIv_AlphaFlo/figures/001_Figure_1.jpg]]
*Figure 1: Uncurated samples (seeds 1-8) from the DiT-XL/2 model for MeanFlow Geng et al. (2025a) and α-Flow (our proposed method) produced with 1 (upper) and 2 (lower) sampling steps for ImageNet-1K 2562.*

## 实验与分析

### 补充图表

![[assets/figures/papers/iclr26_generative_models_diffusion__generative_models_and_autoencoders__b001_adacb4JTIv_AlphaFlo/figures/007_Table_1.jpg]]
*Table 1: Class-conditional generation on ImageNet-256×256. The table reports the results for few-step diffusion/flow matching-based methods trained from scratch.$^ { \ ' } \times 2 ^ { \ ' }$ indicates that FACM requires roughly twice the computation per epoch compared to other methods. For a direct ”epochto-epoch comparison,” α-Flow-XL/2, MeanFlow-XL/2 and FACM-XL/2 are each trained for 240 epochs. α-Flow-XL/2+ is a fine-tuned version of α-Flow-XL/2, trained for extra 60 epochs with a batch size of 1024. † FID scores are evaluated with the balanced class sampling (see Appendix J).*

![[assets/figures/papers/iclr26_generative_models_diffusion__generative_models_and_autoencoders__b001_adacb4JTIv_AlphaFlo/figures/008_Table_2.jpg]]

![[assets/figures/papers/iclr26_generative_models_diffusion__generative_models_and_autoencoders__b001_adacb4JTIv_AlphaFlo/figures/009_Table_2.jpg]]
*Table 2: (a) Consistency step ratio schedule. (b) Flow matching ratio. Table 2: Ablation study on ImageNet-1K 2562 for α-Flow-B/2.*

![[assets/figures/papers/iclr26_generative_models_diffusion__generative_models_and_autoencoders__b001_adacb4JTIv_AlphaFlo/figures/012_Figure_7.jpg]]
*Figure 7: Kinetics-700 1 7 $\times$ 2 5 $6 ^ { 2 }$ experiments.*

![[assets/figures/papers/iclr26_generative_models_diffusion__generative_models_and_autoencoders__b001_adacb4JTIv_AlphaFlo/figures/014_Table_3.jpg]]
*Table 3: Configurations on ImageNet 256 256. B/2-non-cfg is our ablation and analysis model in the main text.*

## 原文 PDF

![[paperPDFs/ICLR_2026/AlphaFlow_Understanding_and_Improving_MeanFlow_Models.pdf]]
