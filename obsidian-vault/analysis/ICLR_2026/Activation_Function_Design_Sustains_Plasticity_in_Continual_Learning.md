---
title: "Activation Function Design Sustains Plasticity in Continual Learning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Activation_Function_Design_Sustains_Plasticity_in_Continual_Learning.pdf
aliases:
- SLRSLBPRS
- AFDSPCL
tags:
- ICLR_2026
- topic/optimization_theory_probabilistic
- topic/optimization_theory_probabilistic/domain_adaptation_and_transfer_learning
core_operator: "激活函数的负半轴导数和死区宽度设计。适度非零的负斜率（Goldilocks区间0.6–0.9）与避免双侧饱和是控制塑性保持的关键。"
primary_logic: "通过设计符合三原则（严格非零导数地板、适度负半轴响应、C1光滑过渡）的激活函数（如Smooth-Leaky及其随机化变体），可在不增加容量的前提下，为类增量监督学习和非平稳强化学习提供轻量级、领域通用的塑性保持手段。"
claims:
- "在I.I.D.与类增量对比中，激活函数排名差异在类增量下急剧扩大（Table 1）。"
- "当负斜率处于Goldilocks区间（0.6 ≤ s̄ ≤ 0.9）时，最终准确率达到峰值且死单元比例显著降低（Figure 1A, 1B）。"
- "具备严格非零导数地板的激活函数在分布冲击下几乎全部恢复（非恢复率<5%），而零地板类型几乎全部丧失恢复能力（Figure 2）。"
- "死区宽度评分与饱和恢复指标（平均AUSC, SF非恢复率）呈强正相关（r=0.81, r=0.84），定量解释了不同激活函数的冲击敏感性（Figure 4）。"
---

# Activation Function Design Sustains Plasticity in Continual Learning

> [!tip] 核心洞察
> 通过设计符合三原则（严格非零导数地板、适度负半轴响应、C1光滑过渡）的激活函数（如Smooth-Leaky及其随机化变体），可在不增加容量的前提下，为类增量监督学习和非平稳强化学习提供轻量级、领域通用的塑性保持手段。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 激活函数设计在持续学习中维持可塑性 |
| 英文题名 | Activation Function Design Sustains Plasticity in Continual Learning |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=XZf6wObHX4) |
| Topic | #topic/optimization_theory_probabilistic #topic/optimization_theory_probabilistic/domain_adaptation_and_transfer_learning |
| Method | Smooth-Leaky 与 Randomized Smooth-Leaky（及其扩展 Bo-PReLU、R-SeLU） |
| Dataset | Permuted MNIST (continual supervised), Split-CIFAR-100 Class-Incremental, Scaling Shock Stress Test (γ=2.0) |

> [!tip] 效果简介
> - Permuted MNIST (continual supervised) 上，Total Average Online Task Accuracy (%) 为 Rand. Smooth-Leaky 84.26 ± 0.02，对比 ReLU (vanilla) 78.85，变化 +5.41 百分点。
> - Split-CIFAR-100 Class-Incremental 上，Final Average Accuracy (%) 为 RReLU (leaky family) 32.95 ± 0.12，对比 ReLU 24.41 ± 0.75，变化 +8.54 百分点。
> - Scaling Shock Stress Test (γ=2.0) 上，Non-recovery Rate (%) 为 Non-zero-floor activations (incl. Smooth-Leaky) ~0%，对比 Zero-floor (ReLU, Tanh, Sigmoid) ~50%，变化 降低约50个百分点。

## 概述

持续学习中，标准激活函数（如ReLU）的饱和与零导数区域会导致模型逐渐丧失学习新数据的能力，具体表现为死单元比例升高、梯度消失、权重表示的有效秩下降。在i.i.d.联合训练下表现相近的激活函数，在类增量学习场景中性能差异急剧扩大（Split-CIFAR-100 类增量学习，Table 1），表明激活函数的可塑性保持能力是该范式下的核心瓶颈。

本文通过分析激活函数负半轴导数和饱和特性，揭示维持可塑性的关键设计原则：**严格非零的导数地板**（避免神经元永久失活）、**适度的负半轴响应**（有效负斜率 $\bar s \in [0.6, 0.9]$ 达到精度峰值，死单元比例显著降低，Figure 1），以及**C¹ 光滑过渡**（避免分段线性的优化陡坎）。在此基础上提出 **Smooth‑Leaky** 与 **Randomized Smooth‑Leaky** 两种即插即用的激活函数：前者通过 sigmoid 调制在原点实现光滑连接，后者进一步在训练期随机采样负斜率，以极低成本引入探索，测试时固定为均值。

主要结果：（1）在 Split‑CIFAR‑100 类增量设定中，leaky 家族激活函数（RReLU）相较 ReLU 最终准确率提升 **8.54 个百分点**；（2）在 Permuted MNIST 等监督持续学习基准上，Randomized Smooth‑Leaky 显著优于普通 ReLU（+5.41 个百分点）；（3）在分布冲击压力测试下，具备非零导数地板的激活函数（含本文方法）恢复率接近 **100%**，而零地板类型（ReLU、Tanh、Sigmoid）几乎不可恢复（非恢复率约 50%）。死区宽度评分与饱和恢复指标呈强正相关（r=0.81–0.84），定量证实激活函数的内在响应范围直接决定了冲击后的恢复能力。在非平稳强化学习场景中，Randomized Smooth‑Leaky 同样展现出最高的可塑性分数，且能有效抑制训练‑测试泛化差距的扩大。

该方法仅替换激活层，不增加模型容量，为类增量监督学习和非平稳强化学习提供了一种轻量、领域通用的可塑性维持手段。

## 背景与动机

深度神经网络在非平稳数据流中持续学习时，会面临**可塑性丧失（loss of plasticity）**这一瓶颈：模型逐渐失去拟合新任务的能力，尽管容量充足。通过对多种激活函数的属性分析，该问题具体表现为三个相互耦合的现象：

1. **死单元（dead units）比例攀升** —— 在类增量学习（class-incremental learning, C-IL）的后期，大量神经元对任何输入均输出零或常值，梯度恒为零，导致有效容量萎缩。
2. **梯度消失与权重空间秩损失** —— 标准整流器（如 ReLU）在负半轴导数为零，使得反向传播中的梯度流被硬性截断，权重矩阵的有效秩（effective rank）随任务推进会持续衰减。
3. **分布冲击下饱和失恢复** —— 当数据分布发生剧烈漂移（模拟非平稳环境）时，双侧饱和激活（如 Tanh、Sigmoid）及零导数地板（zero derivative floor）的激活函数会进入大范围饱和状态，且几乎无法自行恢复，造成网络对新数据完全"失聪"。

然而，已有持续学习研究多数聚焦于网络架构扩展、重放策略或参数正则化，**激活函数的形状设计对可塑性的影响长期被忽视**。在独立同分布（i.i.d.）联合训练下，不同激活函数的性能差异甚微，但一旦进入类增量学习场景，排名急剧扩大：表 1 显示，在 Split‑CIFAR‑100 上，标准 ReLU 的最终准确率仅约 24.4%，而具有随机负斜率的 RReLU 达到约 33.0%，差距超过 8 个百分点。这一对比揭示出，**激活函数的负半轴响应特性是非平稳学习中的一个隐藏杠杆**。

进一步的系统性属性研究指向了一条核心因果链（Figure 1A, 1B）：
- 激活函数的**有效负斜率（effective negative slope）** $\bar{s}$ 直接决定死单元比例与最终准确率。当 $\bar{s} \to 0$ 时，死单元比例高达约 45%；当 $\bar{s}$ 处于中等泄漏的 **"Goldilocks" 区间（约 0.6 ≤ $\bar{s}$ ≤ 0.9）** 时，准确率达到峰值且死单元比例大幅降低。
- 通过定量的缩放冲击（scaling shock）实验（Figure 2, Figure 3），具备**严格非零导数地板**的激活函数（如 Leaky‑ReLU、RReLU、PReLU）在强烈冲击下依然能几乎 100% 恢复，非恢复率 < 5%；而零地板整流器及饱和激活的非恢复率约 50%。死区宽度评分（Dead‑Band Width, DBW）与平均饱和曲线下面积（AUSC）及饱和恢复非恢复率呈强正相关（Pearson r = 0.81, r = 0.84，p < 0.002，Figure 4），量化了激活函数内在死区宽度对冲击敏感性的决定性作用。

上述发现表明：**激活函数的负半轴导数和死区宽度，是控制持续学习中可塑性的两个低维抓手**。但目前常用的激活函数并未系统满足以下保持可塑性的设计原则：① 严格非零的导数地板（避免不可逆的死亡神经元）；② 适中而非极端的负半轴响应（处于 Goldilocks 区间）；③ 在原点的光滑过渡（C¹ 连续性，减少不连续带来的优化不稳定性）。

因此，本文的动机在于：**通过属性级别的分析与设计，提出轻量级、即插即用的激活函数，在不增加网络容量的前提下，为类增量监督学习和非平稳强化学习提供通用的可塑性保持解决方案**。新激活函数围绕上述三原则构建，并引入训练时的随机化负斜率以实现廉价的探索，从而进一步提升对分布漂移的鲁棒性。该方案颠覆了"只需通过架构或正则化对抗灾难性遗忘"的惯性思维，将激活函数的形状设计提升为持续学习的关键优化维度。

## 核心创新

当任务分布由独立同分布（i.i.d.）切换到类增量持续学习时，激活函数的性能排序被急剧放大（Table 1），表明**激活函数的负半轴响应直接决定模型持续学习新数据的能力**。基线 ReLU、Sigmoid、Tanh 等存在零导数地板或双侧饱和的设计，在持续学习中会累积大量死单元（死单元比例可达 ~45%，Figure 1B），并通过梯度消失与权重空间秩损失导致塑性丧失。

本工作将瓶颈定位到激活函数**负半轴的导数行为与死区宽度**，提出两条相互耦合的改进规则：
1. **严格非零的导数地板**——避免负半轴导数趋向零，防止不可逆饱和；
2. **负斜率保持在"Goldilocks"区间**——经验最优区间 $0.6 \lesssim \bar{s} \lesssim 0.9$（Figure 1A），偏离此区间则准确率下降、死单元比例上升。

基于上述规则，作者构造了两种即插即用的激活函数（Section 5.1）：
- **Smooth‑Leaky**：通过 sigmoid 调制实现原点附近的 C¹ 光滑过渡，避免分段线性（C⁰）拐点引起的梯度不连续性，同时保持负半轴非零导数地板；
- **Randomized Smooth‑Leaky**：训练时从均匀分布随机采样负斜率，测试时固定为均值（$r_{\text{test}} = (l+u)/2$），以极轻量的探索机制扩大有效负斜率覆盖范围，进一步缓解塑性衰退。

两个关键设计 slot 形成对基线方法的根本性改造：

| 设计维度 | 基线模型（ReLU/Leaky‑ReLU/PReLU） | 提出方法 |
|----------|-----------------------------------|----------|
| 原点过渡光滑性 | 分段线性（C⁰），存在导数不连续点 | C¹ 光滑过渡，使用 sigmoid 调制实现平滑连接（Eq.(1)） |
| 负斜率选取方式 | 固定常数或可学习标量 | 训练期间从均匀分布随机采样，测试时使用均值，引入结构化噪声（Eq.(2)） |

上述改变不增加网络层宽或容量，仅在激活层替换函数形式。在分布冲击的脱饱和测试中，具备严格非零地板激活函数（含 Smooth‑Leaky 族）的非恢复率降至 5% 以下，而零地板类型（ReLU, Tanh, Sigmoid）几乎完全丧失恢复能力（Figure 2）。死区宽度评分（DBW）与饱和严重程度（AUSC）及非恢复率均呈强正相关（Pearson r=0.81, r=0.84；Figure 4），从机制上定量解释了不同激活函数对冲击的脆弱性根源。

最终，在类增量监督学习（Split‑CIFAR‑100）中，泄露族激活（如 RReLU）将最终准确率从 ReLU 的 24.41% 提升至 32.95%（+8.54 百分点）；在 Permuted MNIST 上，Rand. Smooth‑Leaky 相较普通 ReLU 获得 +5.41 百分点的总平均在线准确率增益。这些结果确认：**从激活函数负半轴形状和死区宽度出发的系统设计，是一种轻量、领域通用且能即插即用的塑性保持手段**。

## 整体框架

该工作的核心是一个即插即用的激活函数替换方案，无需修改网络容量、层宽或训练流程，即可在持续学习中维持模型可塑性。整体流程可概括为：标准神经网络的每一隐藏层在得到预激活值 $z$ 后，通过所设计的激活函数 $\varphi(\cdot)$ 产生输出，随后进入下一层。关键在于激活函数的形状选择——特别是负半轴的响应特性与原点附近的光滑过渡——直接决定了网络在序列任务中能否持续学习。

框架围绕两条设计主线展开：
1. **光滑且保持非零导数的负半轴过渡**：提出 Smooth‑Leaky，通过 sigmoid 调制实现原点处的 C¹ 光滑连接，避免 ReLU 类函数的 C⁰ 拐点，从而消除硬死区。其表达式为 $f(x) = \alpha x + (1 - \alpha) x \cdot \sigma(c x / p)$，其中 $\alpha$ 控制负斜率均值，$c$ 和 $p$ 调节过渡平滑度（Section 5.1）。
2. **随机化负斜率注入轻量探索**：Randomized Smooth‑Leaky 在训练时从均匀分布中采样负斜率 $r \sim U(l, u)$，测试时固定为均值 $(l + u)/2$。这种随机化在不增加优化超参数的前提下，使激活函数覆盖更丰富的响应区间，从而增强对非平稳分布的鲁棒性（Section 5.1，Table 2）。

输入输出流与常规网络无异：输入数据经若干全连接或卷积层、批归一化等模块后，到达激活层；激活层仅对每个神经元独立应用上述函数，输出保留原维度，直接传递至下一层。因此，该框架可嵌入任何监督学习或强化学习网络，替换掉默认的 ReLU、GeLU 等激活，而保持其余部分不变。

设计动机直接源于对塑性丧失瓶颈的实证诊断：标准激活函数（如 ReLU）的零导数区域导致大量死单元（在 Split-CIFAR-100 类增量场景下可达约 45%，Figure 1B），并使权重矩阵有效秩下降。Smooth‑Leaky 家族的三项原则——严格非零导数地板、适度的 Goldilocks 负斜率区间（$0.6 \lesssim \bar{s} \lesssim 0.9$）、C¹ 光滑过渡——正是为了同时避免死区饱和与双侧饱和带来的去饱和困难（见 Section 3–4，Figure 2–4）。在分布冲击测试中，具备非零导数地板的激活函数（包括 Smooth‑Leaky）的非恢复率几乎为 0%，而零地板类型高达约 50%（Figure 2）。这为整体框架提供了直接因果依据：通过设计激活函数的局部形状即可控制全局的塑性保持能力。

## 核心模块与公式推导

### 2.1 激活函数设计三原则

通过对负半轴形状与饱和行为的分层分析，该工作凝练出维持持续学习可塑性的三条激活函数设计原则：

1. **严格非零导数地板（Derivative floor）** – 对于所有 $x<0$，保证导数 $\varphi'(x) > 0$，避免产生永久无法更新的死单元。
2. **适度负半轴响应（Moderate negative‑side responsiveness）** – 有效负斜率 $\bar{s}$ 落入 **Goldilocks 区间 $0.6\lesssim \bar{s}\lesssim 0.9$**，在防止梯度消失与抑制权重不稳定之间取得平衡。
3. **C¹ 光滑过渡（Smooth transition）** – 在原点附近由负支到正支的连接须一阶连续（C¹），以消除分段线性拐点带来的优化不稳定。

遵循上述原则设计的激活函数可在不增加模型容量的前提下，作为即插即用的轻量组件恢复持续学习中的可塑性。

### 2.2 Smooth‑Leaky 激活函数

为同时满足 C¹ 光滑性与可调的负斜率，提出 **Smooth‑Leaky**：

$$
f(x)=\alpha x+(1-\alpha)\,x\cdot\sigma\!\left(\frac{c\,x}{p}\right)。 \tag{1}
$$

- $\alpha\in(0,1)$ 控制负斜率基线：当 $x\ll0$ 时 $\sigma(\cdot)\to0$，$f(x)\approx\alpha x$（接近 Leaky‑ReLU 行为）；当 $x\gg0$ 时 $\sigma(\cdot)\to1$，$f(x)\approx x$（接近恒等/ReLU 正支）。
- $\sigma(\cdot)$ 采用 logistic sigmoid 调制，参数 $c$、$p$ 共同决定原点附近的弯曲程度，确保 $\varphi\in C^1$ 且不存在硬拐点。
- Eq.(1) 通过 sigmoid 的软开关机制替代分段线性拼接，消除分段点处的高曲率，从而减轻梯度噪声与死区扩展。

### 2.3 Randomized Smooth‑Leaky

为进一步提升对非平稳分布的鲁棒性，引入 **随机化负斜率** 变体 **Randomized Smooth‑Leaky**：

$$
r\sim U(l,u),\qquad r_{\text{test}}=\frac{l+u}{2}, \tag{2}
$$

其中 $l$ 与 $u$ 界定负斜率的均匀采样区间。训练期间每 batch 随机抽取 $r$ 替代 $\alpha$，使网络在"适度泄漏"区间内进行轻量探索；测试时固定为区间中点，避免随机性影响稳定性。该设计在多数持续学习基准上（Permuted MNIST、Random Label CIFAR、CIFAR 5+1、Continual ImageNet）均表现出相比固定坡度版本的统计显著提升（Mann‑Whitney U，$p<10^{-4}$）。

### 2.4 有效负斜率度量

为量化激活函数在负半轴的整体响应强度，定义 **有效负斜率** $\bar{s}$：

$$
\bar{s}=\mathbb{E}_{x<0}\bigl[\varphi'(x)\bigr].
$$

该度量在合成 Leaky‑ReLU 时退化为底斜率，在光滑激活函数下反映负输入区域的平均导数值。实验显示，$\bar{s}$ 偏离 Goldilocks 区间 $[0.6,0.9]$ 会导致死单元比例急剧上升（$\bar{s}\to0$ 时死单元占比≈45%）或权重秩退化为 1，最终准确率显著下降（Figure 1）。因此 $\bar{s}$ 是衔接激活函数形状与持续可塑性的核心桥梁指标。

## 实验与分析

### 激活函数稳态属性：死单元、负斜率与塑性损失黄金区间

研究首先在Split-CIFAR-100类增量场景下揭示了激活函数对塑性维持的根本差异。Table 1 的核心结论确立了分析动机：**在I.I.D.联合训练下，11种激活函数的最终准确率差异被压缩至极窄范围（如RReLU 73.71%，最差函数约62%），但切换到类增量学习后排名急剧分化，最优与最差函数差距扩大至约8.5个百分点**。这一分离现象表明，激活函数的设计缺陷在非平稳数据流中被系统性放大，而非单纯由优化难度差异造成。

![[assets/figures/papers/iclr26_0006_XZf6wObHX4_Activation_Function_Design_Sustains_Plasticity_i/figures/001_Table_1.jpg]]
*Table 1: Why focus on continual learning? Under identical models and training budgets on Split-CIFAR-100, activation function rankings compress in i.i.d. joint training but separate sharply in class-incremental (C-IL) settings (Van de Ven et al., 2022). This motivates probing how negative-branch behavior affects plasticity under shift. Unless noted, all case studies use the same 4-layer CNN backbone, the Adam optimizer (Kingma, 2014), and training budget (full details in App. B), isolating activation effects from architectural or optimization confusion. Values for Split-CIFAR-100 are reported as average accuracy (standard deviation) for 5 independent runs with identical architecture...*

为定位导致塑性丧失的机制瓶颈，研究扫描了线性泄漏族（Leaky-ReLU, RReLU, PReLU）的有效负斜率$\bar{s} = \mathbb{E}_{x<0}[\varphi'(x)]$。Figure 1A 揭示了非单调的倒U形关系：当$\bar{s}$处于**0.6–0.9的"Goldilocks区间"**时，最终准确率可靠地达到峰值；过大的负斜率（$\bar{s} > 1$）导致性能显著下降，过小的负斜率则使网络陷入**死单元主导的失效模态**——Figure 1B 显示，$\bar{s} \to 0$时约45%的神经元永久失活，相应的平均准确率降至仅约20%。这一死单元比例阈值（约8%）在Figure C1中与最终准确率呈显著负相关（$r=-0.51$, $p=8.2\times10^{-28}$），说明**死单元累积是塑性丧失的直接表征而非附带现象**。

![[assets/figures/papers/iclr26_0006_XZf6wObHX4_Activation_Function_Design_Sustains_Plasticity_i/figures/005_Figure_1.jpg]]
*Figure 1: A: Final accuracy vs. effective negative slope s̄. B: Dead-unit fraction vs. s̄. Linear-leak families peak for $\bar{s} \in$ [0.6, 0.9]$. Smooth-tailed activations are plotted on the same s̄ axis; they underperform within the 'Goldilocks zone' and only approach the linear-leak peak when $\bar{s}$ > 1$, reflecting concentrated near-zero responsiveness and vanishing tails. C: Effective rank of the gradient Gram matrix. D: Dominant $\lambda_{\max}$. Smooth-tailed activations show spikes at large s̄, while constant-slope leaks remain comparatively stable

光滑尾激活函数（Swish, GeLU等）在相同$\bar{s}$轴上系统性低于线性泄漏族，其"有效负斜率"掩盖了双侧饱和导致的梯度退化——这是仅控制负半轴导数无法修复的二次损伤，为后续设计原则中的"避免双侧饱和"提供了定量依据。

### 冲击恢复实验：非零导数地板是一阶决定因子

为分离激活函数在分布骤变下的动态解饱和能力，研究者设计了可调强度的缩放冲击协议（Scaling Shock, $\gamma=0.5$–$2.0$），同时监控两项互补指标：**饱和分数恢复时间（$\tau_{50}^{SF}$）**和**饱和分数非恢复率**（SF non-recovery rate），辅以功能性能恢复时间$\tau_{95}$。

Figure 2 的结果揭示了一阶决定因子："非零导数地板"（Non-Zero Floor）的存在性。**具备严格非零导数地板的激活函数（Leaky-ReLU, RReLU, PReLU, CReLU）即使在最强冲击下（$\gamma=2.0$）的非恢复率仍接近零（<5%），而零地板类型（ReLU, Tanh, Sigmoid）的非恢复率攀升至约50%**——近半神经元永久陷入饱和。在功能恢复方面，Figure D1 证实非零地板组的$\tau_{95}$稳定在约1–2个epoch，而零地板组随$\gamma$增加迅速恶化至3.4 epochs以上。

![[assets/figures/papers/iclr26_0006_XZf6wObHX4_Activation_Function_Design_Sustains_Plasticity_i/figures/006_Figure_2.jpg]]
*Figure 2: Desaturation under scaling shocks γ. Left: mean AUSC (lower is better). Middle: SF recovery time (epochs to halve the saturated fraction after the shock; successful recoveries only). Right: SF non-recovery rate (%). Groups: Zero-floor = ReLU, Tanh, Sigmoid; Non-zero-floor = Leaky-ReLU, RReLU, PReLU; Effective non-zero-floor = ELU, CELU, SELU, GELU, Swish. See App. D.2 for details*

Figure 4 的因果关系强度得到定量验证：死区宽度评分（DBW）与平均AUSC（area under the saturation curve）呈强正相关（Pearson $r=0.81$, $p=0.0016$），与SF非恢复率同样强相关（$r=0.84$, $p=0.0013$）。这确证了**激活函数内在的负半轴响应范围（死区宽度）直接决定了冲击后解饱和的能力边界**。Figure 3 进一步剖析饱和度效应：双侧饱和激活函数的峰值饱和分数最高，且SF恢复的非恢复率达49.83%，而单侧拐点激活仅为13.30%，说明双侧边界对可恢复性构成额外惩罚。

![[assets/figures/papers/iclr26_0006_XZf6wObHX4_Activation_Function_Design_Sustains_Plasticity_i/figures/012_Figure_4.jpg]]
*Figure 4: Correlation of Dead-Band Width Score with Saturation Recovery Metrics (All Gammas Aggregated). (Left): Average Area Under Saturation Curve (Avg. AUSC) vs. Dead-Band Width Score. A strong positive correlation (Pearson $r = 0.81$, $p = 0.0016$) is observed. (Middle): Average Saturation Fraction (SF) Recovery Time (for successful recoveries, measured by epochs) vs. Dead-Band Width Score. No significant correlation is found (Pearson $r = -0.25$, $p = 0.45$). (Right): Average SF Non-Recovery Rate (%) vs. Dead-Band Width Score. A strong positive correlation (Pearson $r = 0.84$, $p = 0.0013$) is observed, indicating functions more prone to saturation are more likely to fail SF recovery*

由此凝练出三条塑性友好设计原则：**(1) 严格非零导数地板**（排除零梯度区域）；**(2) 适度的负半轴响应**（目标Goldilocks区间0.6–0.9）；**(3) C1光滑过渡**（避免原点拐点引入的训练不稳定，为原则1提供平滑实现路径）。

### 监督持续学习主结果：增量学习下的链路级优势

遵循上述设计原则构建的Smooth-Leaky与Randomized Smooth-Leaky（Rand. Smooth-Leaky），在多个类增量基准和塑性压力测试上进行了系统验证。Table 2 汇总了五个代表性基准的主要结果：

![[assets/figures/papers/iclr26_0006_XZf6wObHX4_Activation_Function_Design_Sustains_Plasticity_i/figures/014_Table_2.jpg]]

**在极端塑性压力任务Random Label CIFAR上**，Rand. Smooth-Leaky取得84.26±0.02%的总体平均在线任务准确率（Total Average Online Task Accuracy），相较于标准ReLU（78.85%）提升**5.41个百分点**，相较于GeLU（79.50%）提升4.76个百分点。**在较接近真实分布偏移的CIFAR 5+1任务上**，Rand. Smooth-Leaky（75.69%）相较ReLU（72.43%）和GeLU（74.62%）仍有持续增益，表明优势不局限于纯噪声标签情形。

在Continual ImageNet这一规模更大的基准上（1000类持续到达），Rand. Smooth-Leaky（33.19%）较ReLU（29.84%）提升3.35个百分点，较Leaky-ReLU（30.19%）和GeLU（29.19%）保持稳健领先。值得关注的是，**随机化变体（Rand. Smooth-Leaky）在大多数基准上均优于固定斜率的Smooth-Leaky**，如Random Label CIFAR上差异为1.63个百分点，证实轻量探索机制在非平稳环境中的边际增益是实质性的。

**预算公平性是评估严格性的关键保障**。Table B1 的Bootstrap最优-N配置、单侧Mann-Whitney U检验表明，Rand. Smooth-Leaky在Permuted MNIST、Random Label MNIST、Random Label CIFAR、CIFAR 5+1和Continual ImageNet共五个数据集上，对ReLU、GeLU、Swish、eLU、CReLU等15个基线中的绝大多数**以$p<10^{-4}$水平达到统计显著优势**。两个例外是Permuted MNIST上的Smooth-Leaky（$p=1.00$，小型网络+稳定分布使优势压缩）和CIFAR 5+1上的CeLU（$p=1.00$），这些边界案例提示设计原则在低塑性压力下贡献趋于饱和。

**与持续学习算法的叠加效应**进一步强化了激活函数的独立价值。Table E4 和 Table E5 显示，在vanilla（无额外策略）、EWC、Online EWC、SI四种算法设置下，激活函数替换带来的准确性提升保持一致模式：在Permuted MNIST上，Rand. Smooth-Leaky在vanilla设定中比ReLU高出5.41个百分点，而在EWC/SI组合下增益依然保持在+4.5至+6.5个百分点范围，表明**激活层设计与正则化/回放策略近似正交加成**。

### 持续强化学习主结果：可塑性与泛化缺口的双重度量

为验证激活函数领域的通用性，研究在非平稳MuJoCo序列（HalfCheetah-v5→Hopper-v5→Walker2D-v5→Ant-v5重复三循环）上对PPO策略网络进行激活层替换评估，引入两项精细指标：可塑性分数与泛化缺口变化。

**可塑性分数**（Plasticity Score）定义为最后循环稳态期（后15%步长）的平均episodic return经Min-Max归一化后的四分位间均值（IQM），将跨环境评分统一到[0,1]尺度。Table 3 列出的排名中，**Rand. Smooth-Leaky以0.3875±0.038的IQM位居首位**，超过ReLU（0.3612±0.047）和GeLU（0.3220±0.049），验证了在三原则指导下，激活函数对非平稳探索型训练的鲁棒增益。Smooth-Leaky（0.3612±0.043）与ReLU接近，提示在RL探索噪声下，随机化版本的扰动抗性是关键差异来源。

![[assets/figures/papers/iclr26_0006_XZf6wObHX4_Activation_Function_Design_Sustains_Plasticity_i/figures/016_Table_3.jpg]]
*Table 3: Average Plasticity Score across 5 seeds (higher is better). We only report the top-performing activations. See Table F1 for a full comparison of all activations. † Values are reported as Min-Max Normalized IQM mean ± 95% CI half-width. Figure 6: Plasticity Score across 5 seeds (95% bootstrap CIs) showing a complete sequence of 3 cycles across all 4 environments. The table reports the Min-Max Normalized IQM of this score across seeds, only showing the top-performing activations to avoid clutter*

**泛化缺口变化**（$\Delta \mathrm{GAP}_e = \mathrm{GAP}_{3,e} - \mathrm{GAP}_{1,e}$）衡量训练-测试性能gap在三个循环间的变化方向。Table 4 报告的跨环境结果揭示了两种失效模式的对立：ReLU在四个环境中均显示泛化缺口扩大（正$\Delta$值），如HalfCheetah-v5上$\Delta\mathrm{GAP}=127.51\%$；而**Rand. Smooth-Leaky在Ant-v5上呈负$\Delta$（−336.13±971.75%），表明训练-测试gap随时间收窄**，这同时意味着分布内可塑性与分布外鲁棒性得到了兼顾。这一结果回应了持续学习场景中"高可塑性导致过拟合"的担忧，初步证明适当激活函数解耦了两者间的部分张力。

### 失败模式与局限

尽管三原则激活在绝大多数压力测试中表现稳健，仍需指出以下边界失效模态：

1. **Goldilocks区间依赖任务特异性**。$\bar{s} \in [0.6, 0.9]$的结论提取自Split-CIFAR-100的固定超参数扫描（Table B4），在非平稳RL末端返回值的噪声条件下，该区间是否最优尚未经系统验证。固定斜率的Smooth-Leaky在RL上的增益明显衰减，说明**任务噪声谱的异质性不可完全被静态参数吸收**。

2. **随机化版本对超调参数敏感**。Rand. Smooth-Leaky从均匀分布$U(l,u)$中采样，该区间的选取目前依赖与固定版本相近的启发式设定；附录中未见自动调节区间宽度的尝试，限制了在更广泛的非平稳流（如概念漂移速率变化）中的部署灵活性。

3. **双侧饱和的间接惩罚未充分隔离**。冲击实验中的饱和度分析将双侧饱和激活归为最差组，但并未从机制上区分"双侧边界对优化曲面曲率的破坏"与"死区宽度对梯度质量的破坏"——两条因果链可能在更深层网络上纠缠，影响对更复杂激活函数（如SeLU）失效根源的精确归因。

4. **所有benchmark均为中等规模**。在Split-CIFAR-100、Continual ImageNet和四任务MuJoCo序列上得到的结论，尚需在更大模型或更长任务序列上验证，以确认死单元比例的阈值（~8%）和Goldilocks区间是否保持尺度不变性。

## 方法谱系与知识库定位

### 激活函数设计作为塑性维持的因果杠杆

本研究在持续学习的激活函数设计空间中占据一个特定的因果节点：**激活函数的负半轴导数形状与死区宽度是控制塑性丧失的独立可操纵变量**。这一主张建立在两个关键发现之上。其一，在独立同分布联合训练与类增量学习的对照实验中，激活函数之间的性能差异在类增量设定下急剧扩大（Table 1），表明非平稳数据分布放大了激活函数选择的重要性——这正是多数基准测试中被掩盖的系统性效应。其二，固定负斜率的Leaky-ReLU与RReLU在有效负斜率 $\bar{s} \in [0.6, 0.9]$ 的"Goldilocks区间"内达到峰值准确率，且死单元比例显著降低（Figure 1A, 1B）；当 $\bar{s} \to 0$ 时，死单元比例飙升至约45%。这构成了一个清晰的因果图像：负半轴导数的适度非零取值直接抑制了死单元的累积，从而维持了权重空间的有效秩和梯度流。

本文提出的Smooth-Leaky与Randomized Smooth-Leaky并非全新的激活函数家族，而是对现有"leaky"类激活函数的**光滑化与随机化改造**。其设计变更局限于两个精确的插槽：（1）将分段线性的C0拐点替换为基于sigmoid调制的C1光滑过渡（$f(x)=\alpha x+(1-\alpha)x \cdot \sigma(cx/p)$），消除原点处的导数不连续；（2）在训练期间从均匀分布随机采样负斜率（$r \sim U(l,u)$），测试时固定为均值，以极低的计算代价引入负斜率空间的轻量探索。这两个变更不改变层宽、不增加可训练参数数量，属于即插即用的激活层替换。

### 相对于基线方法的增量贡献与边界

与标准ReLU相比，Smooth-Leaky的核心增量在于**赋予负半轴严格非零的导数地板**。这是塑性维持的充分条件：在分布冲击实验中，具备非零导数地板的激活函数（Leaky-ReLU、RReLU、PReLU及本文提出的变体）几乎全部恢复性能（非恢复率<5%），而零地板类型（ReLU、Tanh、Sigmoid）约50%无法恢复（Figure 2）。这里的关键因果机制是：零地板激活在遭遇强分布冲击时导致大量单元永久饱和，梯度流被阻断，而即使很小的负斜率也足以在后续训练中重新打开这些单元的梯度通道。

与可学习负斜率的PReLU相比，Smooth-Leaky/Randomized Smooth-Leaky避免了自适应参数在持续学习中的漂移风险。附录证据显示，PReLU-N（逐神经元可学习 $\alpha$）在类增量训练后期，大量 $\alpha$ 趋近于零（Figure C2），实质上退化为ReLU。这提示了一个重要的方法论边界：**可学习参数的引入并未自动解决塑性维持问题，反而在非平稳数据流下暴露了元学习层面的不稳定性**。随机化采样（Rand. Smooth-Leaky）通过强制负斜率在Goldilocks区间内均匀探索，规避了这一漂移陷阱，同时以预算公平的最优-N配置Bootstrap检验（Mann-Whitney U）在多个基准上取得统计显著优势（$p < 10^{-4}$）。

与光滑非单调激活函数（Swish/SiLU、GeLU）相比，Smooth-Leaky在"Goldilocks区间"内表现出系统性优势（Figure 1A）。光滑尾激活函数在该区间内表现不佳，仅在 $\bar{s} > 1$ 时追平——但此时负半轴实际已变为正斜率，丧失了非线性本身的意义。这表明光滑性本身不解决塑性问题，**负半轴的响应范围（而非函数的光滑程度）才是第一性因素**。

### 适用边界与证据强度分层

本文的证据强度呈现清晰的层级结构。**最强证据**（置信度0.95–1.0）来自于控制良好的消融与压力测试：Goldilocks区间的存在性、非零导数地板对分布冲击恢复的决定性作用、以及死区宽度评分（DBW）与饱和恢复指标（平均AUSC，$r=0.81$；SF非恢复率，$r=0.84$）的强正相关性（Figure 4）。这些发现通过激活函数的底层属性（导数地板、死区宽度）建立了从设计参数到塑性指标的因果链条。

**中等强度证据**（置信度0.90–0.95）来自跨域泛化：Randomized Smooth-Leaky在监督持续学习（Permuted MNIST、Random Label CIFAR、CIFAR 5+1、Continual ImageNet）和非平稳强化学习（MuJoCo四任务循环）中均取得领先的塑性评分（Plasticity Score 0.3875 ± 0.038 IQM），且在Ant-v5环境中展现出负的泛化差距变化（$\Delta\text{GAP} = -336.13 \pm 971.75$），意味着训练-测试差距随时间收缩而非扩大。然而，这些结果依赖于Adam优化器的选择（作者有意为之，以"压力测试"塑性），且只在单一网络架构上进行验证，跨架构（如Transformer、图神经网络）的适用性仍为开放问题。

**需人工验证的弱证据**（置信度<0.90）涉及与经验回放、正则化等标准持续学习方法的交互效应（文中仅将其列为未来工作），以及"死区宽度评分"作为一种通用塑性预测指标的跨任务稳定性。

### 局限与开放问题

本文的局限集中体现在三个维度。**第一，Goldilocks区间的固定性**。当前设计在固定区间内均匀采样负斜率，但不同任务、不同网络深度对"适度泄漏"的定义可能存在系统性差异。文中明确指出未来方向为"从固定的Goldilocks区间斜率转向自适应、逐神经元的自调节"。**第二，架构交互的空白**。实验局限于卷积网络（监督学习）和MLP-策略网络（RL），未探索与归一化层（BatchNorm、LayerNorm）、残差连接、注意力机制的协同或冲突。特别是，归一化层的存在可能部分缓解或掩盖激活函数的饱和效应，当前的孤立分析可能高估了激活函数在完整管线中的效应量。**第三，理论与实践的间隙**。尽管DBW评分在统计上高度相关于饱和恢复，它本质上仍是描述性指标而非规范性设计准则。如何从"解释塑性丧失"跨越到"以DBW为约束进行激活函数自动搜索"，是实现自动化塑性友好设计的关键瓶颈——文中对此仅以"尚未调和表达性与鲁棒自动化"作结，未提供技术路径。

开放问题方面，最紧迫的是**可学习参数在非平稳数据流下的漂移动力学研究**。PReLU-N的负斜率向零坍塌并非个例，而是揭示了更深层的元学习问题：当超参数本身需要通过梯度下降适应时，其更新信号来自非平稳数据分布，天然缺乏收敛保证。随机化采样避开了这一问题，但以牺牲精细调节能力为代价。如何解耦超参数的更新时机与主训练循环，使负斜率在更慢的时间尺度上演化——例如仅在任务边界或检测到塑性下降信号时更新——可能是一条未探索但有希望的路径。此外，激活函数设计与容量扩展（如动态添加神经元、模块化网络）的互补性尚未被评估，两者可能作用于塑性维持的不同阶段或不同类型的遗忘。

## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/Activation_Function_Design_Sustains_Plasticity_in_Continual_Learning.pdf

![[paperPDFs/ICLR_2026/Activation_Function_Design_Sustains_Plasticity_in_Continual_Learning.pdf]]
