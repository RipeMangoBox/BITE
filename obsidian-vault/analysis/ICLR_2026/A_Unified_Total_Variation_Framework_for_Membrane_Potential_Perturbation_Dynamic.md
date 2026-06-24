---
title: "A Unified Total Variation Framework for Membrane Potential Perturbation Dynamic"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/A_Unified_Total_Variation_Framework_for_Membrane_Potential_Perturbation_Dynamic.pdf
aliases:
- MT
- UTVFMPPD
- "MPPD-TV-ℓ₁"
tags:
- ICLR_2026
- topic/safety_alignment_fairness_privacy
- topic/safety_alignment_fairness_privacy/trustworthy_machine_learning
core_operator: "将MPPD的正则化项从平方和（ℓ₂）替换为绝对值全变分（ℓ₁），利用共面积公式和更大的L¹函数空间实现更稳健的扰动抑制。"
primary_logic: "将膜电位扰动重新解读为全变分（TV），并基于共面积公式建立MPPD-TV-ℓ₁框架，使正则化更贴合脉冲网络的稀疏动态，从而在对抗攻击下保留块状特征并有效去除噪声。"
claims:
- "MPPD是总变分（TV），其动力学方程(3)天然具备TV的差分形式。"
- "现有MS-MPPD正则化模型是标准的TV-ℓ₂框架。"
- "TV-ℓ₁利用共面积公式比TV-ℓ₂在对抗扰动下具有更好的鲁棒信号重建能力。"
- "MPPD-TV-ℓ₁在CIFAR-10/100和Tiny ImageNet上多数情况下优于所有竞争者（包括MPPD-TV-ℓ₂和Non-MPPD）。"
---

# A Unified Total Variation Framework for Membrane Potential Perturbation Dynamic

> [!tip] 核心洞察
> 将膜电位扰动重新解读为全变分（TV），并基于共面积公式建立MPPD-TV-ℓ₁框架，使正则化更贴合脉冲网络的稀疏动态，从而在对抗攻击下保留块状特征并有效去除噪声。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 膜电位扰动动力学的统一全变分框架 |
| 英文题名 | A Unified Total Variation Framework for Membrane Potential Perturbation Dynamic |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=LDo9numrx6) |
| Topic | #topic/safety_alignment_fairness_privacy #topic/safety_alignment_fairness_privacy/trustworthy_machine_learning |
| Method | MPPD-TV-ℓ₁ |
| Dataset | CIFAR-10 (VGG11, AT训练) |

> [!tip] 效果简介
> - CIFAR-10 (VGG11, AT训练) 上，训练时间 (小时) 为 9.95，对比 10.01 (MPPD-TV-ℓ₂) / 33.89 (SR)，变化 -0.06 vs ℓ₂, -23.94 vs SR。
> - CIFAR-10 (VGG11, AT训练) 上，清洁准确率 (%) 为 84.01 (α=3.5)，对比 83.47 (α=0, 无TV)，变化 +0.54。

## 概述

现有脉冲神经网络（SNN）中，膜电位扰动动态（MPPD）被广泛用于提升网络的对抗鲁棒性，但其正则化处理长期停留在启发式阶段：一方面，MPPD 定义中丢弃了神经元重置部分，缺乏严谨的理论解释；另一方面，基于均方惩罚的 MS‑MPPD 本质上是 **TV‑ℓ₂ 框架**，其函数空间（L²）较小，对尖锐的对抗噪声的抑制能力有限。这些瓶颈限制了扰动正则化的表达上限。

本文的核心发现是：Membrane Potential Perturbation Dynamic 天然是 **总变分（Total Variation, TV）**，并通过共面积公式建立了统一的数学视角。在此基础上，作者将原有 MS‑MPPD 重新识别为标准的 TV‑ℓ₂ 框架，并进一步提出 **MPPD‑TV‑ℓ₁ 框架**——将正则化项从平方和（ℓ₂）替换为绝对值全变分（ℓ₁）。这一改变直接受益于 L¹ 函数空间更大的表达能力，使得网络能够更稳健地在对抗扰动下保留块状信号特征、有效滤除噪声。论文同时给出了 MPPD 的局部变分定义、被支配 TV 性质（膜电位 TV 被权重 1‑范数和脉冲 TV 控制）以及 TV 项的闭式次梯度，为基于替代梯度的反向传播提供了理论保障。

实验部分覆盖 CIFAR‑10/100 和 Tiny ImageNet 三个基准，在 AT（对抗训练）和 AT+Reg（对抗训练加额外正则）方案下，MPPD‑TV‑ℓ₁ 在多种攻击（APGD、FGSM、PGD、C&W、AutoAttack 等）下的清洁准确率和鲁棒准确率大多优于所有竞争者，包括原生的 MPPD‑TV‑ℓ₂ 及其他不含 TV 的鲁棒 SNN 方法。消融研究表明，正则化强度 α ≈ 2.5 ~ 3.0 时鲁棒性最优，且 α > 0 始终优于 α = 0（无 TV）；同时，AT+Reg 对 MPPD‑TV‑ℓ₁ 的额外提升有限，证实其已隐式实现了鲁棒正则化效果。在训练效率方面，MPPD‑TV‑ℓ₁ 的训练时间显著低于 SR 等方法，并具有最低的梯度范数，验证了其优化的稳定性。

综合来看，MPPD‑TV‑ℓ₁ 通过将膜电位扰动纳入严格的 TV‑ℓ₁ 理论框架，既给出了对已有启发式方法的统一解释，又实现了鲁棒性的实质性提升。当前工作主要基于 LIF 神经元推导，在图像分类任务上验证，将其扩展到更一般的脉冲神经元模型及真实场景中的神经形态系统，是下一步值得探索的问题。

## 背景与动机

脉冲神经网络（SNN）在功耗和计算效率上具有天然优势，但其对抗扰动时的鲁棒性提升仍是一个关键挑战。近期研究引入膜电位扰动动态（MPPD）作为正则化手段来约束网络对输入扰动的敏感性。作者发现，原本被用于正则化的MPPD（丢弃神经元重置部分后）在数学上等价于总变分（TV），即

$$\epsilon_i^l[t] = \lambda \epsilon_i^l[t-1] + \sum_j w_{ij}^l \,\Delta s_j^{l-1}[t]$$

这一迭代差分关系天然对应TV的离散形式（公式(3)）。在此基础上，进一步证明现有的均方正则化膜电位扰动训练模型（MS‑MPPD）本质上是 **TV‑ℓ₂** 框架：其惩罚项为膜电位局部变化的平方和（公式(20)），对应能量范数下的正则化。

**现有方法的瓶颈** 在于，TV‑ℓ₂ 所使用的平方函数空间（L²）规模较小，对尖锐、稀疏的对抗噪声重建能力不足。同时，原MPPD定义中包含的神经元重置项（见完整定义中的 $- \lambda(v_i^l[t-1] s_i^l[t-1] - \tilde{v}_i^l[t-1] \tilde{s}_i^l[t-1])$ 部分）在实际正则化中被启发式地丢弃，缺少统一的理论解释和优化框架。这些因素限制了SNN在强对抗攻击下保留块状信号特征并有效去除噪声的能力。

**本文的动机** 正是克服上述局限。作者将MPPD重新解读为定义在统一维度 $(i,t)$（层‑时间）上的膜电位局部变分 $\nabla_{(i,\mathrm{t})} v(i,t,x)$（公式(14)-(15)），并基于共面积公式（coarea formula）提出一个全新的 **TV‑ℓ₁** 框架（MPPD‑TV‑ℓ₁）。其核心是将正则化项由平方和替换为绝对值全变分：

$$\int_{\Theta} \big|\nabla_{(\mathrm{i},\mathrm{t})} v(i,t,x)\big| \,\mathrm{d}\mu$$

（公式(23)）。ℓ₁惩罚对应更大的 L¹ 函数空间，理论上对带有尖锐边界的对抗扰动具有更强的鲁棒信号重建能力（“Based on the coarea formula, TV‑ℓ1 performs better than TV‑ℓ2 in robust signal reconstruction”）。通过这一变革，MPPD‑TV‑ℓ₁ 能够更自然地贴合脉冲网络的稀疏动态，在抑制扰动的同时保持关键的块状特征，从而在清洁准确率和对抗鲁棒性之间达到更优的平衡。后续实验证据也表明，在 CIFAR‑10/100 和 Tiny ImageNet 上，MPPD‑TV‑ℓ₁ 在多种攻击下均与现有方法相比具备显著优势。

## 核心创新

现有脉冲神经网络（SNN）的膜电位扰动动态（MPPD）正则化方案存在一个关键瓶颈：它依赖丢弃神经元重置部分的启发式处理，且其均方正则项本质上对应一个 TV-ℓ₂ 框架。该框架所嵌入的 $L^2$ 函数空间较小，对尖锐的对抗噪声的鲁棒性不足，难以充分表征和抑制脉冲动态中的扰动。这一瓶颈直接催生了本文的核心创新——**将 MPPD 的正则化核从 ℓ₂ 替换为 ℓ₁，构建一个基于全变分（TV）的统一框架 MPPD‑TV‑ℓ₁**。

该创新的因果机制由三个递进的步骤构成：

1. **重新发现与严格证明：MPPD 就是全变分**。  
   论文首先证明，描述膜电位纯净值与扰动值之差的动态方程 $\epsilon_i^l[t]$（丢弃神经元重置后）天然具有 TV 的差分形式。通过定义统一的 $(i,t)$ 维局部变分算子 $\nabla_{(\mathrm{i},\mathrm{t})} v(i,t,x) \triangleq v(i,t,x) - v(i,t,x+\delta(i,t))$，MPPD 被严谨地重新表述为膜电位的局部变分。这一发现将原本零散的正则化设计提升为有严格数学基础的变分问题。

2. **从 TV-ℓ₂ 到 TV-ℓ₁ 的泛函替换**。  
   在该统一的 TV 视角下，原有的 MS‑MPPD 正则项立刻退化为标准的 TV‑ℓ₂ 项（即对局部变分取平方和）。而本文则进一步提出用 ℓ₁ 范数替代 ℓ₂，定义出 MPPD‑TV‑ℓ₁ 的正则项：
   
$$
\int_{\Theta} |\nabla_{(\mathrm{i},\mathrm{t})} v(i,t,x)| \, \mathrm{d}\mu
   = \int_{\Theta} \left| \sum_{k=0}^{t-1} \lambda^{k} \int_{\mathcal{I}(i)} \nabla_{(\mathrm{j},\mathrm{t})} s(j,t-k,x) \, \mathrm{d}w(i,j(i)) \right| \mathrm{d}\mu 。
$$

   这一替换利用了 **共面积公式** 赋予 LT¹ 函数空间更大的容量（对于同等的总变分值，$L^1$ 空间比 $L^2$ 空间能容纳更多“块状”信号），从而使 TV‑ℓ₁ 框架在对抗扰动下具有更强的信号重建能力——它能保留脉冲的块状稀疏结构，同时有效去除噪声。

3. **支配 TV 性质与闭式次梯度保障可训练性**。  
   为填补从泛函定义到梯度反传的鸿沟，论文建立了两个关键保障：  
   - **支配 TV 性质（Theorem 4）**：证明了膜电位 TV 被突触权重的 1‑范数和脉冲 TV 所控制，即
     
$$
\int_1^{N^l} \int_1^T |\nabla_{(\mathrm{i},\mathrm{t})} v(i,t,x)| \, \mathrm{d}t \mathrm{d}i
     \leqslant \|w_l\|_1 \log_{\lambda}(1/e) \int_{\mathcal{I}} \int_1^T |\nabla_{(\mathrm{j},\mathrm{t})} s(j,t,x)| \, \mathrm{d}t \mathrm{d}j，
$$

     这一不等式解释了为何 ℓ₁ 惩罚天然与脉冲的稀疏动态匹配。  
   - **次梯度闭式解（Proposition 5）**：TV‑ℓ₁ 项关于权重的不可微性被显式处理，给出了基于符号函数的简洁次梯度表达式，使得基于时空反传（STBP）的梯度优化得以无缝衔接。

上述 changed slot（正则化项由 ℓ₂ 变为 ℓ₁）是**唯一**的结构性改动。整个训练管线其余部分（LIF 神经元前传、利用扰动动态计算 MPPD、STBP 反传）均与基线保持一致，确保了公平对比。实验证据显示，这一单一改动在 CIFAR‑10/100、Tiny ImageNet 上多次对抗攻击下带来了全面的鲁棒性提升（Table 1，Table 2），且几乎无需额外训练时间（Table A1，MPPD‑TV‑ℓ₁ 比 TV‑ℓ₂ 基线甚至略快）。正则化强度 α 的消融实验进一步证实，α>0 始终优于无正则化的 α=0，且最优区间落在 2.5–3.0 附近（Table 3），同时梯度稳定性显著优于 TV‑ℓ₂ 和 Non‑MPPD 基线（Figure A1）。

**证据强度**：MPPD 就是 TV 的证明（Theorem 1）与 TV‑ℓ₂ 的等价关系具有高置信度（anchor 直接声明 “we discover and prove” 并给出对应公式），核心的 ℓ₁ 优势基于共面积公式的论证亦为确定性推导。优势的实验验证覆盖多个数据集和网络结构，置信度较高，但需注意所有提升均在 LIF 神经元与标准对抗攻击设定下取得，框架向其他神经元模型（如 Izhikevich）和真实物理噪声场景的泛化仍待验证（附录未见对应实验）。此外，所有训练时间对比在统一硬件下进行，但公平性仅停留于运行效率，未涉及数据集偏差等维度。

综上，MPPD‑TV‑ℓ₁ 的核心创新在于用一个更强的 ℓ₁ TV 范数替代原有 ℓ₂ 惩罚，并配以变分定义、支配不等式和闭式次梯度的完整理论铺陈，将 MPPD 从一个启发式正则化提升为一个与 SNN 稀疏脉冲动态内在统一的鲁棒泛函。

## 整体框架

该框架将脉冲神经网络中的膜电位扰动动态（MPPD）重新表述为统一的总变分（TV），并据此构建了以 ℓ₁ 范数为正则化惩罚的训练管道。管道由四个核心模块串联而成：LIF 神经元前向传播、MPPD 计算、TV‑ℓ₁ 正则化注入损失、以及基于时空反向传播（STBP）与次梯度的权重更新。输入为干净的图像样本或对抗样本，输出为鲁棒分类结果，管道内部的数据流如下图所示（示意）：

1. **LIF 神经元前向传播**  
   对每一时间步 $t$ 和层 $l$，膜电位 $v_i^l[t]$ 按衰减系数 $\lambda$ 更新，超过发放阈值 $u_{\text{th}}$ 时产生脉冲 $s_i^l[t] = H(v_i^l[t] - u_{\text{th}})$（式 (2)）。这一过程同时为干净的输入 $x$ 和被扰动后的输入 $x+\delta(i,t)$ 分别计算膜电位 $v$ 与 $\tilde{v}$，以及脉冲 $s$ 与 $\tilde{s}$，从而为后续扰动动态提供基础量。

2. **MPPD 计算**  
   原初的膜电位差值 $\vartheta_i^l[t]$（式 (1)）包含了神经元重置部分，但实践上将该部分丢弃可避免启发式处理带来的不稳定。因此，管道采用简化形式：
   
$$
\epsilon_i^l[t] = \lambda \epsilon_i^l[t-1] + \sum_j w_{ij}^l \Delta s_j^{l-1}[t]
$$

   即式 (3) 的 MPPD 动态，其中 $\Delta s_j^{l-1}[t] = s_j^{l-1}[t] - \tilde{s}_j^{l-1}[t]$。关键的重解释在于将该动态视为膜电位在统一维度 $(i,t)$ 上的局部变分：
   
$$
\nabla_{(i,\mathfrak{t})} v(i,t,x) := v(i,t,x) - v(i,t,x+\delta(i,t)) \quad \text{(式 (14), (15))}
$$

   定理 1（式 (19)）进一步给出了该局部变分沿网络拓扑的递推关系，将膜电位的 TV 与脉冲函数的路径积分联系起来。

3. **TV‑ℓ₁ 正则化**  
   此前的工作（MS‑MPPD）等价于对局部变分施加平方积分惩罚，即 TV‑ℓ₂ 框架（式 (20)），其函数空间较小，对尖锐的对抗噪声鲁棒性不足。本框架将惩罚替换为 ℓ₁ 型总变分（式 (23)）：
   
$$
\int_{\Theta} \left| \nabla_{(\mathrm{i},\mathrm{t})} v(i,t,x) \right| \mathrm{d}\mu
   = \int_{\Theta} \left| \sum_{k=0}^{t-1} \lambda^k \int_{\mathcal{I}(i)} \nabla_{(\mathrm{j},\mathrm{t})} s(j,t-k,x) \,\mathrm{d}w(i,j(i)) \right| \mathrm{d}\mu
$$

   这一 TV‑ℓ₁ 项通过共面积公式使其正则化效果与脉冲的稀疏动态更吻合，从而在抑制扰动时更有效地保留块状结构并去除噪声。正则化项乘以强度系数 $\alpha$ 后加入分类损失的损失函数中。

4. **基于 STBP 的反向传播与次梯度计算**  
   由于 TV‑ℓ₁ 项不可微，管道利用其闭式次梯度（命题 5，式 (26)）进行参数更新。对每个权重 $w(i,j(i))$，次梯度为 $\operatorname{sign}(\cdots) \cdot \sum_{k=0}^{t-1} \lambda^k \nabla_{(\mathrm{j},\mathrm{t})} s(j,t-k,x)$ 在时间‑神经元维度的积分，该公式可直接嵌入基于替代梯度的 STBP 框架（式 (6)），实现端到端的鲁棒训练。理论分析（定理 4，式 (24)）证明膜电位的 ℓ₁‑TV 被脉冲的 ℓ₁‑TV 与权重 1‑范数的乘积所控制，从而保证了梯度的稳定性，实验证据表明该方法在训练中具有最快的梯度衰减和最低的梯度范数（Figure A1）。

通过以上四个模块，MPPD‑TV‑ℓ₁ 框架将扰动动态的启发式处理替换为有理论保证的 TV‑ℓ₁ 正则化，输入为图片和扰动方向，输出为干净与对抗样本的准确率。整个管道在 VGG11 和 WRN16 等架构下，对 CIFAR‑10/100 及 Tiny ImageNet 数据集的多数攻防场景均表现出优于 TV‑ℓ₂ 基线和无 TV 基线的鲁棒性（Table 1, Table 2）。

## 核心模块与公式推导

现有膜电位扰动动态（MPPD）正则化依赖丢弃神经元重置的启发式处理，其本质为平方全变分（TV-ℓ₂）框架；该框架对应的函数空间较小，对尖锐对抗噪声的鲁棒性不足。本文的因果调节器是将惩罚项由平方和（ℓ₂）替换为绝对值全变分（ℓ₁），借助共面积公式获得更大的 L¹ 函数空间，从而更贴合脉冲网络的稀疏动态并有效抑制扰动。下面给出支撑这一调节的核心模块及关键公式，变量含义随公式解释。

### 1. LIF 神经元前向传播与 MPPD 计算

对于泄漏积分发放（LIF）神经元，膜电位动态在纯信号与扰动信号间的差值定义为完整 MPPD：

$$
\vartheta_i^l[t] = \lambda \vartheta_i^l[t-1] + \sum_j w_{ij}^l (s_j^{l-1}[t] - \tilde{s}_j^{l-1}[t]) - \lambda (v_i^l[t-1] s_i^l[t-1] - \tilde{v}_i^l[t-1] \tilde{s}_i^l[t-1]) \tag{1}
$$

其中，$l$ 为层索引，$i$ 为神经元索引，$t$ 为时间步，$\lambda$ 为膜电位泄漏因子，$w_{ij}^l$ 为突触权重，$s$ 和 $\tilde{s}$ 分别为纯净和扰动下的脉冲输出，$v$ 和 $\tilde{v}$ 为对应膜电位。由于式 (1) 中神经元重置部分难以解析，实际正则化中使用丢弃重置的简化 MPPD：

$$
\epsilon_i^l[t] = \lambda \epsilon_i^l[t-1] + \sum_j w_{ij}^l \Delta s_j^{l-1}[t] \tag{3}
$$

$\Delta s_j^{l-1}[t] = s_j^{l-1}[t] - \tilde{s}_j^{l-1}[t]$ 为前一层的脉冲扰动。式 (3) 表征了扰动沿时间和网络层的传播，构成了 TV 分析的起点。

为了将 MPPD 统一为 TV，论文将神经元和时间维度合并为 (i,t)，并定义膜电位的局部变分：

$$
\epsilon(i,t,x) \coloneqq \nabla_{(i,\mathrm{t})} v(i,t,x) \coloneqq v(i,t,x) - v(i,t,x+\delta(i,t)) \tag{14,15}
$$

其中 $v(i,t,x)$ 表示受样本 $x$ 和扰动 $\delta(i,t)$ 影响的膜电位，（14）（15）将逐元素的扰动动态转换为空间‑时间梯度形式，是后续 TV 构造的核心。

### 2. TV‑ℓ₁ 正则化项的建立

基于 LIF 动态，局部变分满足以下递推关系（定理 1）：

$$
\nabla_{(i,\mathfrak{t})} v(i,t,x) = \lambda \nabla_{(i,\mathfrak{t})} v(i,t-1,x) + \int_{\mathcal{I}(i)} \nabla_{(j,\mathfrak{t})} s(j,t,x) \mathrm{d}w(i,j(i)) \tag{19}
$$

其中 $\mathcal{I}(i)$ 为与神经元 $i$ 相连的突触前神经元索引集，$\nabla_{(j,\mathfrak{t})} s$ 是脉冲信号的局部变分。该关系显式地将膜电位 TV 表达为历史脉冲 TV 的加权累积。

利用上式，现有 MS‑MPPD 正则化可直接写为 TV‑ℓ₂ 形式：

$$
\int_1^{N^L} \int_1^T |\nabla_{(i,\mathfrak{t})} v(i,t,x)|^2 \mathrm{d}t \mathrm{d}i = \int_1^{N^L} \int_1^T \left| \lambda \nabla_{(\mathfrak{i},\mathfrak{t})} v(i,t-1,x) + \int_{\mathcal{I}(i)} \nabla_{(\mathfrak{j},\mathfrak{t})} s(j,t,x) \mathrm{d}w(i,j(i)) \right|^2 \mathrm{d}t \mathrm{d}i \tag{20}
$$

$N^L$ 为输出层神经元数，$T$ 为总时间步。该式对膜电位变化的平方惩罚，对应 TV‑ℓ₂ 框架。

本文提出的 TV‑ℓ₁ 框架则惩罚绝对变化，定义如下：

$$
\int_{\Theta} \left| \nabla_{(i,\mathrm{t})} v(i,t,x) \right| \mathrm{d}\mu = \int_{\Theta} \left| \sum_{k=0}^{t-1} \lambda^k \int_{\mathcal{I}(i)} \nabla_{(j,\mathrm{t})} s(j,t-k,x) \mathrm{d}w(i,j(i)) \right| \mathrm{d}\mu \tag{23}
$$

式中 $\Theta$ 是整合神经元索引与时间的统一空间，$\mathrm{d}\mu$ 为对应测度。该 TV 形式对过去所有时刻的脉冲扰动累积取绝对值，比 ℓ₂ 更契合 SNN 的稀疏、突发特性。

### 3. 受制全变分界（定理 4）

以下不等式揭示了膜电位 TV 被脉冲 TV 与权重范数控制的关系，从理论上说明 TV‑ℓ₁ 对权重的稀疏性更敏感。

ℓ₁ 界：

$$
\int_1^{N^l} \int_1^T |\nabla_{(i,\mathrm{t})} v(i,t,x)| \mathrm{d}t \mathrm{d}i \leqslant \|w_l\|_1 \log_{\lambda}\!\left(\frac{1}{e}\right) \int_{\mathcal{I}} \int_1^T |\nabla_{(j,\mathrm{t})} s(j,t,x)| \mathrm{d}t \mathrm{d}j \tag{24}
$$

ℓ₂ 界（对应原 TV‑ℓ₂ 框架）：

$$
\int_1^{N^l} \int_1^T |\nabla_{(i,\mathrm{t})} v(i,t,x)|^2 \mathrm{d}t \mathrm{d}i \leqslant \|w_l\|_F^2 \log_{\lambda}^2\!\left(\frac{1}{e}\right) \int_{\mathcal{T}} \int_1^T |\nabla_{(j,\mathrm{t})} s(j,t,x)|^2 \mathrm{d}t \mathrm{d}j \tag{25}
$$

式中 $\|w_l\|_1$ 为权重矩阵的 1‑范数，$\|w_l\|_F$ 为 Frobenius 范数，$\log_{\lambda}(1/e)$ 源自泄漏因子的衰减累积。ℓ₁ 界使用 1‑范数，当权重稀疏时上界更小，与脉冲网络的稀疏性高度相容。

### 4. 基于 STBP 的次梯度计算与权重更新

TV 项对权重不可微，通过次梯度实现反向传播。Proposition 5 给出了闭式次梯度：

$$
\int_{\Theta} \partial_{w(i,j(i))} \left| \sum_{k=0}^{t-1} \lambda^k \int_{\mathcal{I}(i)} \nabla_{(j,\mathrm{t})} s(j,t-k,x) \mathrm{d}w(i,j(i)) \right| \mathrm{d}\mu = \int_{\Theta} \operatorname{sign}(\cdots) \cdot \left( \sum_{k=0}^{t-1} \lambda^k \nabla_{(j,\mathrm{t})} s(j,t-k,x) \right) \mathrm{d}\mu \tag{26}
$$

$\operatorname{sign}(\cdot)$ 为绝对值函数在非零处的导数，零处取值属于 $[-1,1]$；该次梯度结合替代梯度技术（如脉冲函数导数的代理）即可在时空反向传播（STBP）框架下完成权重更新。这一闭式形式保证了训练的计算稳定性与梯度量级控制（实际训练中梯度范数最低且收敛最快）。

**证据强度**：  
- “MPPD 即为 TV”得到严格证明（置信度 0.99），定理 1 和局部变分定义直接将扰动动态与 TV 联系起来。  
- TV‑ℓ₁ 表达式 (23) 与 ℓ₂ 的差异基于共面积公式，理论证明（定理 4）与实验均支持 ℓ₁ 在对抗扰动下鲁棒信号重建的优越性（置信度 0.99）。  
- 次梯度公式 (26) 是论文的推导结果，为训练提供了可实现性；梯度稳定性（图 A1）进一步验证了 TV‑ℓ₁ 的低梯度范数特性。  
- 需注意，本框架仅基于 LIF 神经元推导，对其余脉冲神经元模型的适用性尚待验证。

## 实验与分析

我们在 CIFAR‑10/100 和 Tiny ImageNet 三个基准上，采用 VGG11 与 WRN16 两种架构，系统比较了 MPPD‑TV‑ℓ₁ 与多种 SNN 鲁棒训练方法的表现，包括 MPPD‑TV‑ℓ₂、Non‑MPPD 以及具有固有鲁棒性或使用对抗训练的 SNN‑BP、HIRE‑SNN、SNN‑RAT、FEEL、SR 等（Table 1、Table 2）。MPPD‑TV‑ℓ₁ 在所有数据集和攻击类型（APGD、FGSM、PGD⁷/¹⁰/²⁰/⁴⁰、CW 以及 AutoAttack）下均取得了最优或极具竞争力的对抗准确率，且在清洁样本上未出现明显退化。例如，在 CIFAR‑10 上 VGG11 的清洁准确率达到 92.230%，在 Tiny ImageNet 上 WRN16 的清洁准确率为 52.990%，均优于同类方法。值得注意的是，即使仅加入高斯扰动（Gaussian Perturbation），MPPD‑TV‑ℓ₁ 依然保持了最高的鲁棒准确率，表明该方法不仅能防御有目的对抗攻击，对一般性有害噪声也同样有效。


![[assets/figures/papers/iclr26_0004_LDo9numrx6_A_Unified_Total_Variation_Framework_for_Membrane/figures/001_Table_1.jpg]]
*Table 1: Classification accuracies (%) of different methods on CIFAR 10 and CIFAR 100*

![[assets/figures/papers/iclr26_0004_LDo9numrx6_A_Unified_Total_Variation_Framework_for_Membrane/figures/002_Table_2.jpg]]
*Table 2: Classification accuracies (%) of different methods on Tiny ImageNet*

### 正则化强度与消融分析

我们在 AT 训练方案下对 MPPD‑TV‑ℓ₁ 的正则化系数 α 进行了消融（Table 3）。从 α=0（等价于 Non‑MPPD）到 α=4.0，最优鲁棒窗口出现在 α=2.5~3.0 附近，该范围内各攻击下的准确率均显著优于 α=0 的基线。例如，CIFAR‑10 上 α=3.5 时清洁准确率为 84.01%，比 α=0 时的 83.47% 提升 0.54 个百分点，且在 PGD 系列攻击下的提升更为明显。这表明通过控制总变分惩罚强度，可以有效平衡清洁精度与鲁棒性，而取消惩罚（α=0）则会导致对抗鲁棒性急剧下降。


![[assets/figures/papers/iclr26_0004_LDo9numrx6_A_Unified_Total_Variation_Framework_for_Membrane/figures/003_Table_3.jpg]]
*Table 3: Classification accuracies (%) of $\mathbf { M P P D - T V - } \boldsymbol { \ell } _ { 1 }$ with different regularization strengths

此外，我们在 Table 2 中比较了 AT 与 AT+Reg 两种训练方案。MPPD‑TV‑ℓ₁ 在 AT+Reg 下的额外提升极小，与 MPPD‑TV‑ℓ₂ 形成鲜明对比——后者在加入 Reg 后仍需外部正则化来维持鲁棒性。这一现象说明 MPPD‑TV‑ℓ₁ 已在训练过程中隐式地实现了所需的鲁棒正则化效果，额外显式惩罚对其边际效益有限，进一步印证了 TV‑ℓ₁ 框架的内在优势。

### 梯度稳定性和计算效率

从梯度范数（Figure A1）观察，WRN16 在 Tiny ImageNet 上的 AT 训练过程中，MPPD‑TV‑ℓ₁ 的梯度 ℓ₂ 范数在大约第 400 次迭代后迅速下降并稳定在极低水平（~0.5），远低于 MPPD‑TV‑ℓ₂（~2.5）和 Non‑MPPD（~6.0）。这种低梯度范数有效抑制了参数更新中的尖锐振荡，使优化过程更稳定且收敛更快。与之对应的是训练时间对比（Table A1）：在 VGG11 + AT 设定下，MPPD‑TV‑ℓ₁ 在 CIFAR‑10 上仅需 9.95 小时，比 MPPD‑TV‑ℓ₂（10.01 小时）略快，但比 SR（33.89 小时）减少了近 24 小时；在 Tiny ImageNet 上也仅为 22.38 小时，远低于 SR（82.82 小时）。由此可见，MPPD‑TV‑ℓ₁ 不仅在统计鲁棒性上占优，同时还具有显著的计算效率优势。

### 局限与待验证问题

需要指出的是，当前验证均基于 LIF 神经元模型和图像分类任务，所得到的理论框架是否能直接迁移至 Izhikevich、HH 等更复杂的脉冲神经元模型仍需实验确认。此外，虽然已覆盖 CIFAR 和 Tiny ImageNet，但在更大规模数据集（如 ImageNet‑1K）上的可扩展性以及在实际神经形态硬件上的在线训练效率尚未涉及。目前也未测试该方法对补丁攻击、物理域攻击等非 ℓp 型对抗威胁的鲁棒性，这些方向可作为后续研究重点。

### 补充图表

![[assets/figures/papers/iclr26_0004_LDo9numrx6_A_Unified_Total_Variation_Framework_for_Membrane/figures/007_Figure_1.jpg]]
*Figure 1: Accuracies and actual TV values of $\mathbf { M P P D - T V - } \boldsymbol { \ell } _ { 1 }$ (α = 1) and Non-MPPD (α = 0)

![[assets/figures/papers/iclr26_0004_LDo9numrx6_A_Unified_Total_Variation_Framework_for_Membrane/figures/008_Table_4.jpg]]
*Table 4: Table A1: Runtimes (in hours) of different methods with VGG11 architecture and AT training scheme on CIFAR 10, CIFAR 100, and Tiny ImageNet*

![[assets/figures/papers/iclr26_0004_LDo9numrx6_A_Unified_Total_Variation_Framework_for_Membrane/figures/009_Figure_5.jpg]]
*Figure 5: Figure A1: $\ell _ { 2 }$ norms of gradients for different methods with WRN16 architecture and AT training scheme on Tiny ImageNet*


## 方法谱系与知识库定位

MPPD‑TV‑ℓ₁ 的研究起点是对现有膜电位扰动动态正则化的重新审视：先前被广泛采用的是均方膜电位扰动（MS‑MPPD），本文通过将扰动重新表述为全变分（TV），严格证明 MS‑MPPD 即标准 TV‑ℓ₂ 框架（详见定理 1 与公式 (20)）。这一发现揭示了原有方法的内在局限——TV‑ℓ₂ 的函数空间较小，且对尖锐对抗噪声的鲁棒性不足。为此，本文提出的 MPPD‑TV‑ℓ₁ 将正则化项由平方和（ℓ₂ 惩罚）替换为绝对值全变分（ℓ₁ 惩罚），利用共面积公式和更大的 L¹ 函数空间构造了一个新的鲁棒正则化机制。从因果操纵的角度看，正则化范数的改变直接调控了模型对膜电位扰动的抑制模式：ℓ₁ 惩罚天然偏好稀疏梯度，使得训练过程快速收敛且梯度范数维持在极低水平（Figure A1），同时带来显著的计算效率提升（在 CIFAR‑10 上，MPPD‑TV‑ℓ₁ 训练仅需 9.95 小时，远低于 SR 的 33.89 小时，见 Table A1）。

在方法谱系中，MPPD‑TV‑ℓ₁ 与以下关键基线的关系如下：
- **vs. Non‑MPPD（无 TV 正则化）**：MPPD‑TV‑ℓ₁ 在几乎所有攻击场景下均获得更高的鲁棒准确率，即使仅使用对抗训练（AT）而不叠加额外正则化，其表现也显著优于无 TV 的基线（Table 3 中 α>0 的准确率普遍高于 α=0）。这表明 TV 惩罚本身即提供了关键的鲁棒性增益。
- **vs. MPPD‑TV‑ℓ₂（均方 TV）**：两者唯一差异在于正则化函数空间的范数选择。定理 4 给出的受制 TV 界显示，膜电位 TV 在 ℓ₁ 版本下由权重的 1‑范数控制，而在 ℓ₂ 版本下由 Frobenius 范数控制；ℓ₁ 界通常更紧，因而模型对扰动的抑制更稳健。实验证据表明，MPPD‑TV‑ℓ₁ 在 CIFAR‑10/100 和 Tiny ImageNet 上采用 VGG11 与 WRN16 架构时，多数情况下准确率优于 MPPD‑TV‑ℓ₂（confidence 0.95），验证了范数替换带来的实际优势。
- **vs. 其他 SNN 对抗训练方法**：与 SNN‑RAT 的显式对抗训练正则化、HIRE‑SNN 的固有鲁棒性利用、SR 的梯度稀疏正则化等方法相比，MPPD‑TV‑ℓ₁ 不仅在对抗攻击下保持领先或持平，更重要的是它展现出“隐式鲁棒正则化”效应：在 AT+Reg 训练方案下，MPPD‑TV‑ℓ₁ 未获得额外显著提升（identified analyzed claim，confidence 0.95），说明其自身已通过 TV‑ℓ₁ 惩罚实现了类似显式鲁棒正则化的功能。这种机制上的自足性简化了训练流程，同时避免了因额外正则化项引入的超参数敏感性问题。

**适用边界与局限**（均为从现有证据推导所得，部分条目需后续实验验证）：
- **神经元模型限定**：框架的全部理论推导基于 LIF 神经元动态（公式 (2)–(3)），包括局部变分关系和受制 TV 界（定理 4）。将其推广至 Izhikevich、Hodgkin‑Huxley 等更复杂的神经元模型时，膜电位方程的非线性重置机制可能破坏当前线性递推结构，适用性未知。
- **任务与数据规模**：实验仅在图像分类任务（CIFAR‑10/100, Tiny ImageNet）上验证，未涉及真实噪声环境或物理世界干扰。在大规模数据集（如 ImageNet‑1K）上的可扩展性尚未评估；从 Tiny ImageNet 训练时间（22.38 小时）与 CIFAR‑10（9.95 小时）的差异推断，直接扩展可能面临计算开销瓶颈。
- **攻击覆盖盲区**：目前评估的攻击方法包括 APGD、FGSM、PGD、C&W、AutoAttack 等基于梯度的对抗攻击，但未覆盖补丁攻击、物理攻击、黑盒迁移攻击等更现实的威胁模型。TV‑ℓ₁ 罚项可能对特定脉冲模式的依赖导致在面对分布外攻击时产生新的脆弱性，需进一步测试。
- **理论界的保守性**：受制 TV 性质（定理 4）和次梯度可计算性（命题 5）依赖于扰动传播过程的线性近似与替代梯度假设。当网络深度或时间步长增加时，近似误差累积可能使实际 TV 界的控制力下降，鲁棒性保证需要更保守的评估。

**开放问题**：
1. **安全关键场景落地**：将 MPPD‑TV‑ℓ₁ 的鲁棒脉冲扰动抑制理论应用于自动驾驶、工业控制等神经形态系统，并验证其在持续在线学习下的鲁棒性维持能力。
2. **对抗攻击深度**：系统研究模型在面对 patch 攻击、物理攻击以及针对 TV 正则化专门构造的自适应攻击时的行为，厘清其鲁棒性上限与可能的失效模式。
3. **硬件‑算法协同**：评估 TV‑ℓ₁ 正则化在神经形态硬件（如 Loihi、TrueNorth）上进行原位训练的可行性与能效优势，利用其稀疏梯度特性进一步降低功耗。
4. **模型与模态泛化**：将 TV‑ℓ₁ 框架扩展至其他脉冲编码方式（时间编码、群体编码）和非视觉模态（语音、事件相机数据），测试其作为通用神经形态计算鲁棒性基石的潜力。

## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/A_Unified_Total_Variation_Framework_for_Membrane_Potential_Perturbation_Dynamic.pdf

![[paperPDFs/ICLR_2026/A_Unified_Total_Variation_Framework_for_Membrane_Potential_Perturbation_Dynamic.pdf]]
