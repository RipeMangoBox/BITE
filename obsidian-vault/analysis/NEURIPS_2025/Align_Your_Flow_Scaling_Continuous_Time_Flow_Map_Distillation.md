---
title: "Align Your Flow: Scaling Continuous-Time Flow Map Distillation"
type: paper
paper_level: A
venue: NeurIPS
year: 2025
pdf_ref: paperPDFs/NEURIPS_2025/Align_Your_Flow_Scaling_Continuous_Time_Flow_Map_Distillation.pdf
project_link: https://research.nvidia.com/labs/toronto-ai/AlignYourFlow/
code_link: null
aliases:
- AYFAAEL
- AYFSCTFMD
tags:
- NEURIPS_2025
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: "将一致性模型推广为流映射（Flow Map），允许网络建模从任意噪声时间 t 到任意目标时间 s 的映射，配合新的连续时间蒸馏损失（AYF-EMD）、教师自引导（autoguidance）和切线稳定技术，从根本上解耦了一致性条件，消除了误差累积的病态特性。"
primary_logic: "流映射通过单步连接 PF-ODE 上任意两个噪声级别，统一了一致性模型（s=0）和流匹配（s→t）的范式。新提出的 AYF-EMD 损失在连续时间极限下自然归纳了标准一致性损失和流匹配损失，并借助停止梯度和切线归一化实现稳定训练，使得蒸馏模型在所有采样步数下均能保持低 FID，且可通过自引导和对抗微调进一步提升生成质量，同时维持样本多样性。"
claims:
- "一致性模型在多步采样中因误差积累而性能恶化：定理3.1证明增加步数会增加Wasserstein-2距离，Figure 8显示CM的FID随步数上升。"
- "AYF流映射在ImageNet 512×512上以4步采样达到FID 1.70（AYF-S）和1.64（+adversarial），显著优于所有非对抗蒸馏方法，且多步性能保持稳定。"
- "AYF-EMD目标将标准连续时间一致性模型和流匹配损失统一为特例，并保留了停止梯度设计，对训练稳定性至关重要。"
- "在文本到图像用户研究中，AYF（基于FLUX.1）显著优于LCM和TCD，体现了更高的图像质量和提示遵循度。"
---

# Align Your Flow: Scaling Continuous-Time Flow Map Distillation

> [!tip] 核心洞察
> 流映射通过单步连接 PF-ODE 上任意两个噪声级别，统一了一致性模型（s=0）和流匹配（s→t）的范式。新提出的 AYF-EMD 损失在连续时间极限下自然归纳了标准一致性损失和流匹配损失，并借助停止梯度和切线归一化实现稳定训练，使得蒸馏模型在所有采样步数下均能保持低 FID，且可通过自引导和对抗微调进一步提升生成质量，同时维持样本多样性。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 对齐你的流：扩展连续时间流映射蒸馏 |
| 英文题名 | Align Your Flow: Scaling Continuous-Time Flow Map Distillation |
| 会议/期刊 | NeurIPS 2025 |
| Links | [paper](https://arxiv.org/abs/2506.14603) · [Project](https://research.nvidia.com/labs/toronto-ai/AlignYourFlow/) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | Align Your Flow (AYF) with AYF-EMD loss |
| Dataset | ImageNet 512x512, Text-to-image (User study, FLUX.1-based) |

> [!tip] 效果简介
> - ImageNet 512x512 上，FID 为 1.70 (AYF-S, 4-step)，对比 1.84 (sCD-S, 4-step, reproduced)，变化 -0.14。
> - ImageNet 512x512 上，FID 为 1.64 (AYF-S + adversarial finetuning, 4-step)，对比 1.84 (sCD-S, 4-step, reproduced)，变化 -0.20。
> - ImageNet 512x512 上，FID 为 1.92 (AYF-S + adversarial finetuning, 1-step)，对比 3.32 (AYF-S, 1-step)，变化 -1.40。

## 概要

扩散模型和流匹配模型在图像生成领域取得了显著成功，但其采样过程通常需要数十甚至上百次神经网络前向传播，计算成本高昂。一致性模型（Consistency Models, CM）通过将 PF-ODE 轨迹上的任意点直接映射到干净数据（s=0），实现了少步甚至单步生成。然而，**标准一致性模型在多步采样中存在根本性的缺陷：随着采样步数增加，误差会逐步累积，导致生成质量反而下降**（Theorem 3.1, Figure 5, Figure 8）。这一现象使得一致性模型无法通过增加计算预算来稳定提升生成质量，限制了其在高保真场景中的应用。

本文提出 **Align Your Flow (AYF)**，一种扩展的连续时间流映射蒸馏框架，从根本上解决了上述问题。其核心思想是将一致性模型推广为**流映射（Flow Map）**——一个能够连接 PF-ODE 上任意两个噪声级别（从时间 t 到任意目标时间 s）的神经网络 $f_\theta(\mathbf{x}_t, t, s)$。这一推广统一了一致性模型（s=0 的特例）和流匹配（s→t 的极限）两种范式（Figure 2, Figure 9），并从根本上解耦了一致性条件，消除了多步误差累积的病态特性。

配合流映射，本文提出了新的连续时间蒸馏损失 **AYF-EMD**（Eulerian Map Distillation），该损失在连续时间极限下自然归纳了标准一致性损失和流匹配损失，并通过停止梯度与切线归一化技术实现稳定训练（Theorem 3.2）。此外，AYF 引入了**教师自引导（autoguidance）**机制——利用弱教师模型在蒸馏过程中增强分布锐度，以及可选的短期**对抗微调**阶段，进一步提升生成质量。

在 ImageNet 512×512 上，AYF 以 4 步采样达到 **FID 1.70**（AYF-S），经对抗微调后进一步降至 **FID 1.64**，显著优于所有非对抗蒸馏方法，且多步性能保持稳定而不恶化（Table 4, Table 5, Figure 8）。在基于 FLUX.1 的文本到图像任务中，AYF 在用户偏好研究中明显优于 LCM 和 TCD（Figure 7）。值得注意的是，AYF 的 4 步采样速度与先前工作的单步生成相当甚至更快（Figure 6），在效率与质量之间取得了优异的平衡。

### 扩散模型与流匹配的少步生成困境

现代生成模型，特别是扩散模型和流匹配模型，在图像、视频等领域的生成质量上取得了显著进展。这类模型的核心在于学习一个从噪声分布到数据分布的概率流常微分方程（PF-ODE），通过逐步去噪实现样本生成。然而，高质量的生成通常需要数十甚至上百个采样步骤，每个步骤都需要一次完整的神经网络前向传播，这严重制约了推理效率。

为了突破这一瓶颈，**知识蒸馏**成为主流策略：将一个预训练的多步教师模型压缩为少步学生模型。其中，**一致性模型**（Consistency Models, CM）是最具代表性的方法之一。一致性模型学习从任意噪声时间 $t$ 直接映射到干净数据（$s=0$），从而在单步或两步采样中取得极具竞争力的结果。

### 一致性模型的核心缺陷：多步误差累积

尽管一致性模型在极低步数下表现出色，但它存在一个根本性的弱点：**在多步采样中性能反而恶化**。这一现象与直觉相悖——通常增加采样步数应当提升生成质量，但一致性模型却呈现相反的趋势。

本文通过理论分析揭示了这一问题的本质。**定理3.1**（见原文）证明，对于一致性模型，增加采样步数会导致生成样本与真实数据分布之间的 Wasserstein-2 距离增加。Figure 5 可视化了这一现象：当数据为高斯分布时，最优一致性模型的多步采样误差随步数单调上升。Figure 8 进一步在 ImageNet 512×512 上验证了这一点——标准一致性模型的 FID 随采样步数增加而恶化。

这一误差累积的病态特性源于一致性模型的输出目标设定：网络被强制要求直接预测洁净图像（$s=0$），而在多步采样中，每一步的微小预测误差会在后续步骤中传播和放大，使得生成样本逐渐偏离真实数据分布。

### 现有方法的局限与流映射的契机

在一致性模型之外，**流匹配**（Flow Matching）提供了另一种视角：它学习任意两个噪声级别之间的速度场，天然支持多步采样，但缺乏单步生成能力。**一致性轨迹模型**（CTM/TCD）尝试连接任意两个噪声级别，初步探索了流映射（Flow Map）的概念，但在大规模图像生成上的稳定性和性能仍不理想。

这些方法的根本张力在于：**一致性模型牺牲了多步性能换取单步效率，流匹配则需要大量步骤才能收敛，而早期的流映射方法未能有效平衡两者**。一个统一的框架应当能够：
- 在单步中连接任意两个噪声级别（$t \to s$），而非仅限于 $s=0$；
- 在多步采样中保持稳定，避免误差累积；
- 训练目标在数学上自然统一现有范式。

### 本文动机

基于上述分析，本文的核心动机是**从根本上解耦一致性条件，消除误差累积的病态特性**。具体而言，本文提出将一致性模型推广为真正的**流映射**（Flow Map），允许网络建模从任意噪声时间 $t$ 到任意目标时间 $s$ 的映射，并设计相应的连续时间蒸馏损失和训练稳定化技术。这一框架统一了一致性模型（$s=0$）和流匹配（$s \to t$）的特例，同时使蒸馏模型在所有采样步数下均能保持低 FID，从根本上解决了多步性能恶化的问题。

## 核心方法与创新机理

AYF 的核心创新在于将标准一致性模型（CM）推广为**流映射（Flow Map）**范式，从根本上解决了 CM 在多步采样中因误差累积导致性能恶化的瓶颈。Theorem 3.1 从理论上证明，对于非最优一致性模型，增加采样步数反而会增大生成样本与真实分布之间的 Wasserstein-2 距离——Figure 5 和 Figure 8 的实验结果直接验证了这一病理特性：CM 的 FID 随步数增加而上升，最佳性能仅出现在极少数步数（如两步）处。

AYF 通过以下关键设计实现了范式突破：

### 1. 输出目标的根本泛化：从 s=0 到任意 s∈[0,1]

标准一致性模型仅学习从噪声时间 t 到干净数据 s=0 的映射 f(x_t, t)，这本质上强制网络承担极端的去噪跨度，导致多步累积误差无法避免。AYF 将输出目标扩展为**从任意时间 t 到任意目标时间 s 的映射 f_θ(x_t, t, s)**（Section 3.2, Figure 2）。这一泛化统一了三个范式：
- **s=0**：退化为标准一致性模型
- **s→t**：等价于流匹配模型
- **任意 s**：流映射的完整能力空间

这种解耦使得网络可以在 PF-ODE 轨迹上以任意粒度进行跳跃，彻底消除了 CM 中“必须直接预测洁净图像”所带来的病态约束。

### 2. AYF-EMD 损失：统一连续时间蒸馏框架

AYF 提出了**欧拉地图蒸馏（AYF-EMD）**损失（Section 3.2, Algorithm 1），其核心特性在于：

- **连续时间极限下的统一性**（Theorem 3.2）：当步长 ε→0 时，AYF-EMD 的梯度自然归纳为标准连续时间一致性损失和流匹配损失。这意味着 AYF-EMD 不是简单的工程拼接，而是具有严格理论基础的统一框架。
- **停止梯度设计**：保留了目标网络 f_{θ^-} 的停止梯度，这对训练稳定性至关重要（Section 3.4）。
- **切线归一化与预热**：通过切线归一化（tangent normalization）和正则化切线预热策略（r_max=0.99, Section 3.4, Equation 4-5），避免了直接计算切向导数时的梯度爆炸问题。Equation 5 进一步揭示，切线预热项的梯度等价于鼓励流映射保持线性的正则化项，为训练稳定性提供了理论解释。

消融实验（Table 5）提供了决定性证据：在 ImageNet 512×512 4-step 设置下，AYF-EMD 达到 FID 1.70，而 AYF-LMD（拉格朗日地图蒸馏）仅为 6.70——后者虽然在 2D 玩具数据上更稳定（Figure 11），但在高维图像生成中导致严重过度平滑。

### 3. 教师自引导替代 CFG

传统蒸馏方法依赖分类器自由引导（CFG）来增强生成锐度，但 CFG 需要额外的条件模型或复杂的引导尺度调参。AYF 引入**自引导（autoguidance）**机制（Section 3.3, Equation 3）：通过结合强教师模型 v_φ 和弱教师模型 v_φ^weak 的加权速度场来锐化蒸馏目标的分布。消融实验（Table 5）表明，自引导的 AYF-S 4-step FID 为 1.70，而使用 CFG 的版本为 2.32，验证了自引导在蒸馏场景下的显著优势。

### 4. 对抗微调：弥补单步性能差距

AYF 在单步生成上相比专门为单步优化的方法（如 sCD）略有不足，但通过蒸馏后的短期对抗微调（Algorithm 2），结合 AYF-EMD 和 RpGAN 损失，单步 FID 从 3.32 大幅降至 1.92（Table 4），同时多步性能也进一步提升至 1.64。Figure 8 显示，对抗微调后的 AYF 在所有采样步数下均保持低 FID，且多样性损失极小。

### 方法谱系与知识库定位

AYF 在方法谱系中处于**一致性蒸馏与流匹配的交汇点**（Figure 9）。它将以下工作的核心思想统一并超越了各自的局限：

- **连续时间一致性模型（sCM/sCD）**：继承了其连续时间蒸馏框架和切线归一化技术，但通过流映射推广消除了多步退化问题。
- **一致性轨迹模型（CTM/TCD）**：早期探索了轨迹一致性蒸馏，但未建立 AYF-EMD 的统一理论框架，且在高分辨率图像上的性能不及 AYF。
- **流匹配模型（EDM2, FLUX.1）**：作为教师模型提供 PF-ODE 轨迹，AYF 将其多步采样能力蒸馏为高效的少步流映射。
- **LCM**：基于 SDXL 的一致性模型，在文本到图像用户研究（Figure 7）中被 AYF（基于 FLUX.1）显著超越。

> **需要人工验证**：sCM/sCD、CTM/TCD、LCM 等基线方法的具体作者/年份/会议信息未在分析数据中提供，建议在最终版本中补充完整引用。

AYF（Align Your Flow）的整体框架围绕**流映射蒸馏**构建，其核心思想是将预训练的流匹配或扩散教师模型的能力压缩到一个学生网络中，该学生网络能够以任意步数（包括极少的步数）进行高质量采样，且性能不会因步数增加而退化。

### 核心组件与数据流

整个 pipeline 由以下关键模块组成，数据在它们之间沿 PF-ODE 轨迹流动：

**1. 预训练教师模型 $v_\phi$**
- **角色**：提供 PF-ODE 速度场，生成训练所需的噪声-数据轨迹。
- **输入/输出**：给定噪声样本 $\mathbf{x}_t$ 和时间 $t$，输出速度方向 $v_\phi(\mathbf{x}_t, t)$，用于沿 ODE 推进或回退。
- **来源**：基于 EDM2（ImageNet）或 FLUX.1（文本到图像）等成熟的流匹配/扩散模型。

**2. 弱引导模型 $v_\phi^{\text{weak}}$**
- **角色**：为自引导（autoguidance）提供低质量参考模型。
- **机制**：教师的自引导速度由强教师和弱教师的凸组合构成：
  $$ \mathbf{v}_{\phi}^{\text{guided}}(\mathbf{x}_t, t) = \lambda \mathbf{v}_{\phi}(\mathbf{x}_t, t) + (1 - \lambda) \mathbf{v}_{\phi}^{\text{weak}}(\mathbf{x}_t, t) $$
  其中 $\lambda$ 控制引导强度，通过放大强教师与弱教师之间的差异来锐化生成分布。

**3. 流映射学生网络 $f_\theta$**
- **角色**：学习从任意噪声时间 $t$ 到任意目标时间 $s$ 的直接映射 $f_\theta(\mathbf{x}_t, t, s)$。
- **参数化**：采用跳跃连接形式 $c_{\text{skip}} \mathbf{x}_t + c_{\text{out}} F_\theta$，确保在 $s \to t$ 时退化为恒等映射。
- **关键创新**：相比传统一致性模型仅能映射到 $s=0$（干净图像），流映射支持任意 $(t, s)$ 对，从根本上解耦了一致性条件，消除了多步误差累积的病态特性。

**4. AYF-EMD 蒸馏损失**
- **角色**：训练学生网络的核心目标函数。
- **原理**：在 PF-ODE 轨迹上取相邻时间点 $t$ 和 $t' = t + \varepsilon(s - t)$，要求学生从 $\mathbf{x}_t$ 到 $\mathbf{x}_s$ 的预测与从 $\mathbf{x}_{t'}$ 到 $\mathbf{x}_s$ 的预测一致。当 $\varepsilon \to 0$ 时，其梯度极限为：
  $$ \nabla_{\theta} \mathbb{E}_{\mathbf{x}_t, t, s} \left[ w'(t, s) \cdot \text{sign}(t - s) \cdot \mathbf{f}_{\theta}^{\top}(\mathbf{x}_t, t, s) \cdot \frac{\mathrm{d} \mathbf{f}_{\theta^{-}}(\mathbf{x}_t, t, s)}{\mathrm{d} t} \right] $$
  该形式统一了连续时间一致性模型（$s=0$）和流匹配（$s \to t$）作为特例，并通过停止梯度 $\theta^{-}$ 保证训练稳定性。

**5. 切线归一化与预热**
- **角色**：稳定训练的关键技巧。
- **机制**：AYF-EMD 需要计算切向导数 $\frac{\mathrm{d}\mathbf{f}_{\theta^{-}}}{\mathrm{d}t}$，将其分解为：
  $$ \frac{\mathrm{d}\mathbf{f}_{\theta^{-}}(\mathbf{x}_t, t, s)}{\mathrm{d}t} = \left(\frac{\mathrm{d}\mathbf{x}_t}{\mathrm{d}t} - \mathbf{F}_{\theta^{-}}(\mathbf{x}_t, t, s)\right) + (s - t) \times \frac{\mathrm{d}\mathbf{F}_{\theta^{-}}(\mathbf{x}_t, t, s)}{\mathrm{d}t} $$
  切线归一化对导数项进行缩放（$c=0.1$），切线预热通过系数 $r \in [0, 1]$ 渐进引入高阶导数项，且 $r_{\max}=0.99$ 确保始终保留一定的直线正则化。

**6. 对抗微调（可选）**
- **角色**：进一步提升生成锐度和单步性能。
- **机制**：蒸馏完成后，引入 StyleGAN2 判别器，结合 AYF-EMD 和 RpGAN 损失进行短期对抗训练（约 3000 次迭代），在几乎不损失多样性的前提下显著降低 FID。

### 训练与推理流程

- **训练阶段**：从教师模型采样轨迹 $\{\mathbf{x}_t\}$，随机选取 $(t, s)$ 对，计算自引导速度，通过 AYF-EMD 损失更新学生网络。切线预热系数 $r$ 从 0 逐渐增加到 $r_{\max}$。
- **推理阶段**：给定噪声 $\mathbf{x}_1 \sim \mathcal{N}(0, I)$ 和目标步数 $N$，将时间区间 $[0, 1]$ 划分为 $N$ 段，依次应用流映射 $f_\theta(\mathbf{x}_{t_i}, t_i, t_{i+1})$ 完成采样。由于流映射支持任意 $(t, s)$，多步采样不会像一致性模型那样出现性能恶化。

### 补充图表

![[assets/figures/papers/paper_list_l36_https_arxiv_org_abs_2506_14603/figures/002_Figure_2.jpg]]
*Figure 2: Overview of Flow Maps. Flow maps generalize both consistency models and flow matching by connecting any two noise levels (s, t) in a single step. When s = 0, flow maps reduce to consistency models; when s → t they’re equivalent to standard flow matching models. Our proposed EMD objective (see Theorem 3.2) similarly generalizes the continuous-time consistency and flow matching losses. For detailed derivations, please see the Appendix*

### 3.1 一致性模型的误差累积定理

标准一致性模型（CM）在多步采样中存在根本性缺陷。AYF 通过定理 3.1 给出了严格证明：对于高斯数据分布，最优一致性模型的闭式解为

$$
\mathbf{f}^*(\mathbf{x}_t, t) = \frac{c \cdot \mathbf{x}_t}{\sqrt{t^2 + (1-t)^2 c^2}}
$$

在此设定下，当采样步数超过某个阈值后，增加步数反而会增大生成样本与真实分布之间的 Wasserstein-2 距离。Figure 5 的可视化结果表明，在 $c=0.5$ 时，两步采样达到最优，继续增加步数导致性能恶化。这一现象的根本原因在于：CM 的训练目标强制网络直接预测洁净图像（$s=0$），多步迭代时每一步的微小误差会沿采样链累积放大，使样本逐渐偏离数据流形。

### 3.2 流映射（Flow Map）框架

为解决 CM 的误差累积问题，AYF 提出流映射 $f_\theta(\mathbf{x}_t, t, s)$，将输出目标从固定的 $s=0$ 泛化到任意目标噪声水平 $s \in [0,1]$。流映射通过单步连接 PF-ODE 轨迹上任意两个噪声级别，统一了两类范式：当 $s=0$ 时退化为一致性模型，当 $s \to t$ 时等价于流匹配模型（见 Figure 2）。

流映射网络采用跳跃连接参数化：

$$
f_\theta(\mathbf{x}_t, t, s) = c_{\text{skip}}(t,s) \cdot \mathbf{x}_t + c_{\text{out}}(t,s) \cdot F_\theta(\mathbf{x}_t, t, s)
$$

其中 $F_\theta$ 为神经网络主体，$c_{\text{skip}}$ 和 $c_{\text{out}}$ 为时间相关的缩放系数。

### 3.3 AYF-EMD 损失函数

AYF 提出两种连续时间蒸馏目标，其中 **AYF-EMD**（Euler Map Distillation）是实际图像生成中采用的损失函数。其离散形式为：

$$
\mathbb{E}_{\mathbf{x}_t, t, s} \left[ w(t, s) \| \mathbf{f}_\theta(\mathbf{x}_t, t, s) - \mathbf{f}_{\theta^-}(\mathbf{x}_{t'}, t', s) \|_2^2 \right]
$$

其中 $\mathbf{x}_{t'}$ 是从 $\mathbf{x}_t$ 沿 PF-ODE 前进一步到达的中间状态，$\theta^-$ 为停止梯度版本的学生网络参数。当步长 $\varepsilon \to 0$ 时，该损失的梯度收敛为（定理 3.2）：

$$
\nabla_{\theta} \mathbb{E}_{\mathbf{x}_t, t, s} \left[ w'(t, s) \cdot \mathrm{sign}(t - s) \cdot \mathbf{f}_{\theta}^{\top}(\mathbf{x}_t, t, s) \cdot \frac{\mathrm{d} \mathbf{f}_{\theta^{-}}(\mathbf{x}_t, t, s)}{\mathrm{d} t} \right]
$$

其中 $w'(t,s) = w(t,s) \cdot |t-s|$。该梯度形式自然地统一了连续时间一致性模型损失（$s=0$ 时）和流匹配损失（$s \to t$ 时）作为特例。**停止梯度**（$\theta^-$）的设计对训练稳定性至关重要，避免了类似于 GAN 训练中的震荡问题。

### 3.4 教师自引导（Autoguidance）

AYF 采用自引导替代传统的分类器自由引导（CFG），在蒸馏阶段增强生成分布的锐度。自引导教师速度定义为：

$$
\mathbf{v}_{\phi}^{\mathrm{guided}}(\mathbf{x}_t, t) = \lambda \mathbf{v}_{\phi}(\mathbf{x}_t, t) + (1 - \lambda) \mathbf{v}_{\phi}^{\mathrm{weak}}(\mathbf{x}_t, t)
$$

其中 $\mathbf{v}_{\phi}$ 为强教师模型，$\mathbf{v}_{\phi}^{\mathrm{weak}}$ 为弱引导模型（通常为训练不充分的同架构模型），$\lambda > 1$ 为引导强度。消融实验（Table 5）表明，自引导（FID 1.70）显著优于同等条件下的 CFG（FID 2.32），且无需额外的条件输入。

### 3.5 切线归一化与预热

AYF-EMD 损失需要计算学生网络输出的切向导数 $\frac{\mathrm{d} \mathbf{f}_{\theta^{-}}(\mathbf{x}_t, t, s)}{\mathrm{d} t}$。该导数可分解为：

$$
\frac{\mathrm{d}\mathbf{f}_{\theta^{-}}(\mathbf{x}_t, t, s)}{\mathrm{d}t} = \left(\frac{\mathrm{d}\mathbf{x}_t}{\mathrm{d}t} - \mathbf{F}_{\theta^{-}}(\mathbf{x}_t, t, s)\right) + (s - t) \times \frac{\mathrm{d}\mathbf{F}_{\theta^{-}}(\mathbf{x}_t, t, s)}{\mathrm{d}t}
$$

其中第一项为直线正则化项，第二项为高阶修正项。为稳定训练，AYF 采用两项关键技术：

- **切线归一化**：对切向导数进行归一化处理，防止梯度爆炸。
- **切线预热**：引入系数 $r \in [0,1]$ 渐进引入高阶导数项。当 $r < 1$ 时，预热损失的梯度等价于：

$$
\nabla_{\theta} \left[ \mathrm{sign}(t - s) \mathbf{f}_{\theta}^{\top}(\mathbf{x}_t, t, s) \times \left( \frac{\mathrm{d}\mathbf{x}_t}{\mathrm{d}t} - \mathbf{F}_{\theta^{-}}(\mathbf{x}_t, t, s) \right) \right] \propto \nabla_{\theta} \left[ \| \mathbf{F}_{\theta}(\mathbf{x}_t, t, s) - \mathbf{v}_{\phi}(\mathbf{x}_t, t) \|_2^2 \right]
$$

即预热阶段等价于鼓励流映射保持线性的正则化，有助于训练初期稳定收敛。实践中设置 $r_{\max} = 0.99$ 以确保始终保留少量正则化。

### 3.6 对抗微调

蒸馏完成后，AYF 可选进行短期对抗微调以进一步提升锐度。该阶段交替优化生成器（流映射学生网络）和判别器（StyleGAN2 架构），损失函数结合 AYF-EMD 蒸馏损失与 RpGAN 对抗损失。对抗微调仅需约 3000 次迭代（约 4 小时），即可在所有采样步数上显著降低 FID，同时保持样本多样性（Table 4, Figure 8）。

### 3.7 流水线模块总结

完整的 AYF 蒸馏流水线包含以下核心模块：

| 模块 | 功能 | 关键设计 |
|------|------|----------|
| 预训练教师模型 $v_\phi$ | 提供 PF-ODE 速度场 | 基于 EDM2 或 FLUX.1 |
| 流映射学生网络 $f_\theta$ | 学习跨噪声级别映射 | 跳跃连接参数化 |
| 弱引导模型 $v_\phi^{\text{weak}}$ | 提供自引导信号 | 训练不充分的同架构模型 |
| AYF-EMD 损失 | 连续时间蒸馏目标 | 停止梯度 + 切线归一化 |
| 切线预热 | 稳定训练 | $r_{\max}=0.99$ |
| 对抗判别器 | 对抗微调提升锐度 | StyleGAN2 + RpGAN 损失 |

## 实验与关键发现

### 核心性能瓶颈：一致性模型的多步退化

本研究首先通过理论分析和实验验证了标准一致性模型（CM）的一个根本性缺陷：多步采样中的误差累积。**定理3.1**证明，对于高斯数据下的最优一致性模型，增加采样步数反而会增大生成样本与真实分布之间的Wasserstein-2距离。这一反直觉现象在**Figure 5**中得到可视化展示（c=0.5时，两步采样达到最优），并在**Figure 8**的ImageNet 512×512实验中进一步验证——CM的FID随步数增加而上升，与扩散模型“步数越多质量越高”的常识背道而驰。该瓶颈的根源在于：一致性模型的目标函数强制网络直接预测洁净图像（s=0），多步累积误差使生成样本逐渐偏离真实数据流形。

![[assets/figures/papers/paper_list_l36_https_arxiv_org_abs_2506_14603/figures/016_Figure_12.jpg]]
*Figure 12: Four-step samples from distilled AYF flow maps using no guidance, autoguidance, and CFG (scale 3) for a 2D distribution. Table 5: Ablation study on ImageNet 512x512. ∗ indicates our reproduction of prior methods. Also see Fig. 8 for a visualization of the key results*

### 主要实验结果

#### ImageNet 512×512：流映射的跨步数稳定性

**Table 2**和**Table 4**展示了ImageNet 512×512上的核心结果。AYF流映射在4步采样下达到FID 1.70（AYF-S），显著优于所有非对抗蒸馏方法。加入对抗微调后（AYF-S + adversarial），4步FID进一步降至1.64，单步FID从3.32大幅降至1.92（**Table 4**）。**Figure 8**直观展示了AYF的关键优势：FID在所有采样步数（1-8步）上保持低值且稳定，而一致性模型在超过2-4步后性能恶化，扩散模型则需要数十步才能达到可比质量。

#### ImageNet 64×64：全面领先

**Table 1**显示AYF在ImageNet 64×64上同样取得最优结果，Recall指标也一并报告，表明方法在保持样本多样性的同时提升了质量。

#### 文本到图像：用户偏好验证

基于FLUX.1蒸馏的AYF模型在4步采样下进行用户研究（**Figure 7**），结果明确优于LCM和TCD，体现了更高的图像质量和提示遵循度。**Figure 3**的定性对比进一步佐证了这一结论。

![[assets/figures/papers/paper_list_l36_https_arxiv_org_abs_2506_14603/figures/009_Figure_7.jpg]]
*Figure 7: User preferences comparing LoRA-based consistency and flow map models (4-step samples). LCM and TCD use SDXL and AYF uses FLUX.1 [dev] as base model, respectively*

#### 采样效率

**Figure 6**以FID-墙钟时间曲线展示了AYF的效率优势：4步AYF采样的速度与先前工作的单步生成相当或更快，同时保持更低的FID。

### 消融实验

**Table 5**在ImageNet 512×512上进行了系统消融，揭示了以下关键结论：

**AYF-EMD vs AYF-LMD**：AYF-EMD在4步下达到FID 1.70，而AYF-LMD仅为6.70，后者导致生成样本过度平滑。这与**Figure 11**的2D玩具实验形成有趣对比：在低维数据上AYF-LMD更稳定且模式覆盖更好，但在高维图像上却严重失效。这一现象被列为开放问题。

**自引导 vs CFG**：使用自引导（autoguidance）的AYF-S达到FID 1.70，而使用CFG的版本为2.32，证明了自引导在蒸馏场景下的显著优势。**Figure 12**在2D分布上可视化对比了无引导、自引导和CFG（scale 3）的效果差异。

**一致性蒸馏基线**：即使加入自引导，复现的sCD-S基线（FID 1.84）也不及AYF-EMD（1.70），验证了AYF损失函数和稳定性技术的综合优势。

**对抗微调**：在所有采样步数上均显著提升性能（**Figure 8**），且多样性损失极小。该阶段仅需约3000次迭代（约4小时），超参数公开。

### 失败模式与局限性

1. **单步性能差距**：AYF在单步生成上略弱于专门为单步优化的方法（如sCD、SiDA），尽管对抗微调大幅缩小了该差距（FID从3.32降至1.92）。

2. **与教师模型的残差**：即使使用多步采样，AYF模型与原始多步教师模型之间仍存在性能差距，无法完全匹敌教师质量（**Figure 8**）。

3. **AYF-LMD的高维失效**：尽管在2D玩具数据中更稳定，AYF-LMD在图像生成中导致严重模糊和细节丢失，需进一步研究其高维行为机制。

4. **对抗微调的额外开销**：需额外训练阶段，增加实现复杂度。

### 采样超参数

**Table 3**报告了最优采样超参数配置，为实际部署提供了参考。

### 补充图表

![[assets/figures/papers/paper_list_l36_https_arxiv_org_abs_2506_14603/figures/008_Figure_6.jpg]]
*Figure 6: FID ↓ as function of wall clock time*

![[assets/figures/papers/paper_list_l36_https_arxiv_org_abs_2506_14603/figures/018_Figure.jpg]]
*Figure: LCM TCD AYF (ours) "Cute jumping spider in pirate hat on ayellow daisy”*

![[assets/figures/papers/paper_list_l36_https_arxiv_org_abs_2506_14603/figures/015_Figure_11.jpg]]
*Figure 11: Four-step samples from distilled AYF flow maps trained using the AYF-EMD and AYF-LMD objectives for a 2D distribution*

![[assets/figures/papers/paper_list_l36_https_arxiv_org_abs_2506_14603/figures/029_Figure_25.jpg]]
*Figure 25: Selected one-step samples generated by our ImageNet512 AYF-S model, shown for classes 89 (sulphur-crested cockatoo) and 985 (daisy)*

![[assets/figures/papers/paper_list_l36_https_arxiv_org_abs_2506_14603/figures/006_Table_1.jpg]]
*Table 1: Sample quality on classconditional ImageNet 64x64. Recall metric is also included*

![[assets/figures/papers/paper_list_l36_https_arxiv_org_abs_2506_14603/figures/012_Table_3.jpg]]
*Table 3: Optimal sampling hyperparameters*

![[assets/figures/papers/paper_list_l36_https_arxiv_org_abs_2506_14603/figures/013_Table_4.jpg]]
*Table 4: Sample quality on class-conditional ImageNet 512×512. This is an extension of Tab. 2 with further baseline methods*

## 定位与知识库关联

### 1. 核心瓶颈：一致性模型的多步误差积累

标准一致性模型（CM）在少步生成（1–2步）中表现优异，但其设计存在一个根本性缺陷：**目标函数要求网络直接预测洁净图像（s=0），导致多步采样中误差逐次累积**。本文通过定理3.1严格证明了这一现象：对于高斯数据分布，当采样步数超过最优值后，Wasserstein-2距离随步数增加而单调上升。Figure 5和Figure 8的实验证据进一步验证了该理论——CM的FID在步数增加时不仅不下降，反而显著恶化。

这一瓶颈的因果根源在于：CM的蒸馏目标强制网络学习从任意噪声水平到洁净图像的单步映射，但多步采样时，前一步的预测误差会作为下一步的输入噪声，而网络从未被训练去处理这种“偏离PF-ODE轨迹”的中间状态。因此，**CM的少步优势与多步稳定性之间存在不可调和的结构性矛盾**。

### 2. 方法谱系：从一致性模型到流映射的统一

AYF的核心创新在于将一致性模型推广为**流映射（Flow Map）**，允许网络建模从任意噪声时间 $t$ 到任意目标时间 $s$ 的映射 $\mathbf{f}_\theta(\mathbf{x}_t, t, s)$。这一推广在方法谱系中占据关键位置，统一了多个先前工作：

- **当 $s=0$ 时**，流映射退化为标准一致性模型（Continuous-time Consistency Models, sCM/sCD），仅预测洁净图像。
- **当 $s \to t$ 时**，流映射等价于流匹配模型（Flow Matching），学习瞬时速度场。
- **当 $s$ 为任意值时**，流映射覆盖了Consistency Trajectory Models（CTM/TCD）的设计空间，但AYF通过连续时间蒸馏损失提供了更统一的理论框架。

Figure 9明确展示了这一谱系关系：AYF可视为Flow Matching、Continuous-time Consistency Models、Flow Map Matching、Consistency Trajectory Distillation以及并行的MeanFlow Models的泛化形式。

### 3. 关键技术槽位对比

AYF在以下五个关键槽位上对基线方法进行了系统性改进：

| 技术槽位 | 基线方法 | AYF方案 | 改进效果 |
|---------|---------|---------|---------|
| **输出目标** | 仅映射到 $s=0$（CM） | 映射到任意 $s \in [0,1]$（流映射） | 消除多步误差积累的病态特性 |
| **训练损失** | 连续时间一致性损失或流匹配损失 | AYF-EMD损失，统一两者并引入停止梯度与切线归一化 | 4步FID从1.84降至1.70（ImageNet 512×512） |
| **教师引导** | 无引导或CFG | 自引导（autoguidance）：$\mathbf{v}_\phi^{\text{guided}} = \lambda \mathbf{v}_\phi + (1-\lambda)\mathbf{v}_\phi^{\text{weak}}$ | 相比CFG的FID 2.32，自引导降至1.70 |
| **时间参数化** | 对数噪声嵌入 $c_{\text{noise}}(\sigma)=\log(\sigma)$ | 直接使用 $t$ 作为噪声嵌入，学生时间嵌入与教师对齐 | 避免梯度爆炸，提升训练稳定性 |
| **对抗微调** | 无 | 蒸馏后短期对抗微调（约3000次迭代），结合AYF-EMD与RpGAN损失 | 单步FID从3.32降至1.92，4步从1.70降至1.64 |

### 4. AYF-EMD损失的理论统一性

AYF-EMD（欧拉地图蒸馏）损失是本文最重要的理论贡献之一。定理3.2证明，在连续时间极限（步长 $\varepsilon \to 0$）下，AYF-EMD的梯度收敛为：

$$\nabla_{\theta} \mathbb{E}_{\mathbf{x}_t, t, s} \left[ w'(t, s) \operatorname{sign}(t - s) \cdot \mathbf{f}_{\theta}^{\top}(\mathbf{x}_t, t, s) \cdot \frac{\mathrm{d} \mathbf{f}_{\theta^{-}}(\mathbf{x}_t, t, s)}{\mathrm{d} t} \right]$$

这一形式自然归纳了两个特例：
- **当 $s=0$ 时**，退化为连续时间一致性模型的梯度。
- **当 $s \to t$ 时**，退化为流匹配损失的梯度。

更重要的是，AYF-EMD保留了停止梯度（stop-gradient）设计，这对训练稳定性至关重要。消融实验（Table 5）显示，使用AYF-LMD（拉格朗日地图蒸馏）替代AYF-EMD会导致FID从1.70急剧恶化至6.70，产生严重过度平滑——尽管AYF-LMD在2D玩具数据上更稳定（Figure 11），但在高维图像生成中完全失效。

### 5. 切线稳定性技术的因果机制

AYF的训练稳定性依赖于两项关键技术：

**切线归一化**：将切向导数分解为直线正则化项与高阶项：
$$\frac{\mathrm{d}\mathbf{f}_{\theta^{-}}(\mathbf{x}_t, t, s)}{\mathrm{d}t} = \left(\frac{\mathrm{d}\mathbf{x}_t}{\mathrm{d}t} - \mathbf{F}_{\theta^{-}}(\mathbf{x}_t, t, s)\right) + (s - t) \times \frac{\mathrm{d}\mathbf{F}_{\theta^{-}}(\mathbf{x}_t, t, s)}{\mathrm{d}t}$$

**切线预热**：通过系数 $r \in [0, 1]$ 渐进引入高阶导数项。当 $r < 1$ 时，预热损失的梯度等价于鼓励流映射保持线性的正则化项：
$$\nabla_{\theta} \left[ \operatorname{sign}(t-s) \mathbf{f}_{\theta}^{\top}(\mathbf{x}_t, t, s) \times \left( \frac{\mathrm{d}\mathbf{x}_t}{\mathrm{d}t} - \mathbf{F}_{\theta^{-}}(\mathbf{x}_t, t, s) \right) \right] \propto \nabla_{\theta} \left[ \| \mathbf{F}_{\theta}(\mathbf{x}_t, t, s) - \mathbf{v}_{\phi}(\mathbf{x}_t, t) \|_2^2 \right]$$

设置 $r_{\max}=0.99$ 确保始终保留少量正则化，有效避免了梯度爆炸。

### 6. 适用边界与局限

尽管AYF在少步生成中取得了显著优势，但其适用边界和局限同样明确：

1. **单步性能弱于专用方法**：AYF在单步生成上略弱于专门为单步优化的sCD等方法（FID 3.32 vs. 更低的单步FID），需依赖对抗微调缩小差距（降至1.92）。

2. **与教师模型的性能差距**：即使使用多步采样，AYF模型仍无法完全匹敌原始多步教师模型的质量，存在不可消除的蒸馏误差。

3. **AYF-LMD的维度敏感性**：AYF-LMD在2D玩具数据上更稳定、模式覆盖更好，但在高维图像上导致严重模糊——这一维度依赖的失效机制尚不明确，是重要的开放问题。

4. **对抗微调的额外成本**：对抗微调虽时间较短（约4小时），但仍增加了训练流程的复杂度和计算开销。

5. **框架依赖性**：目前主要针对连续时间流匹配框架设计，扩展到离散扩散等其他范式需进一步适配。

### 7. 开放问题与未来方向

基于本文的分析和实验，以下开放问题值得进一步探索：

- **AYF-LMD的失效机制**：为何在低维稳定而在高维导致过度平滑？能否通过改进损失函数或正则化策略使其在图像生成中也有效？

- **蒸馏后训练的潜力**：是否能通过variational score distillation等更精细的蒸馏后训练阶段进一步缩小与教师模型的差距？

- **从头训练的可能性**：AYF-EMD损失理论上可直接用于从头训练流映射（不依赖教师蒸馏），这种直接训练方式能否达到蒸馏级别的性能？

- **跨领域迁移**：将AYF应用于视频生成模型蒸馏、药物发现中的分子构象生成等领域的可行性和效果如何？

- **对抗微调与多样性的平衡**：如何在保持对抗微调带来的锐度提升的同时，确保生成样本的多样性不受任何影响？

### 8. 知识库定位总结

AYF在生成模型蒸馏领域的方法谱系中占据**从一致性模型到流匹配的统一桥梁**位置。其核心贡献在于：通过流映射推广和AYF-EMD损失的连续时间统一，从根本上解耦了一致性条件，消除了多步误差积累的病态特性。这使得AYF成为首个在所有采样步数下均保持低FID的蒸馏方法，并通过自引导和对抗微调进一步提升了生成质量。在ImageNet 512×512上，AYF以4步采样达到FID 1.70（非对抗）和1.64（+对抗微调），显著优于所有非对抗蒸馏方法，确立了少步生成的新基准。

## 原文 PDF

![[paperPDFs/NEURIPS_2025/Align_Your_Flow_Scaling_Continuous_Time_Flow_Map_Distillation.pdf]]
