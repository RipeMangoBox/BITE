---
title: "MaskDiME: Adaptive Masked Diffusion for Precise and Efficient Visual Counterfactual Explanations"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/MaskDiME_Adaptive_Masked_Diffusion_for_Precise_and_Efficient_Visual_Counterfactual_Explanations.pdf
project_link: "https://clguo.github.io/MaskDiME/"
code_link: null
aliases:
- MaskDiME
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 自适应双掩码机制——基于分类器梯度动态生成噪声级掩码M^z和清洗级掩码M^x，在反向扩散每一步控制更新范围，迫使编辑集中到决策相关像素并保留原图背景。
primary_logic: 将扩散模型的反向过程与分类器梯度引导相结合，通过动态空间掩码替代全局更新，以单步线性复杂度和无训练方式实现高保真、决策驱动的局部图像编辑。
claims:
- 与DiME和FastDiME的全局/散乱编辑相比，MaskDiME能够生成聚焦于决策相关区域的局部修改（如图1所示）。
- 热力图可视化证明自适应双掩码使扩散更新逐步集中在面部表情等因果区域，而像素差掩码或固定掩码则产生分散或不适应语义演变的更新（如图3所示）。
- 在CelebA、BDD100K、ImageNet等多领域数据集上，MaskDiME均取得100%的Flip Rate、最低FID及最优或次优的结构一致性指标（表1-3）。
- 消融实验显示，移除自适应掩码和梯度缩放后FID升至95.76、FR降至55.2%；恢复双掩码可将FID降至0.71、COUT升至0.81，而进一步细化清洗掩码（ρ=0.5）使COUT提升至0.87（表4）。
---

# MaskDiME: Adaptive Masked Diffusion for Precise and Efficient Visual Counterfactual Explanations

> [!tip] 核心洞察
> 将扩散模型的反向过程与分类器梯度引导相结合，通过动态空间掩码替代全局更新，以单步线性复杂度和无训练方式实现高保真、决策驱动的局部图像编辑。

| 字段 | 内容 |
|------|------|
| 中文题名 | MaskDiME: 自适应掩码扩散实现精准高效的视觉反事实解释 |
| 英文题名 | MaskDiME: Adaptive Masked Diffusion for Precise and Efficient Visual Counterfactual Explanations |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2602.18792) · [Project](https://clguo.github.io/MaskDiME/) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | MaskDiME |
| Dataset | CelebA Smile |

> [!tip] 效果简介
> - CelebA Smile 上，推理速度提升 >30× vs DiME，>2.5× vs FastDiME vs 1× (DiME, FastDiME) (>30×)；多样性 σ_L 0.0395 vs 0.2139 (DiME)；0.0174 (ACE l1) (-0.1744 vs DiME)；GPU内存占用 ~1/10 of ACE and RCSB vs ACE, RCSB (全量) (约 90% 减少)。

## 概要

视觉反事实解释旨在回答“如果输入图像的某部分不同，模型决策是否会改变”这一关键问题。现有基于扩散模型的反事实生成方法面临两个结构性瓶颈：**计算成本高昂**与**空间编辑精度不足**。以 **DiME**（Jeanneret et al., ACCV 2022）为代表的早期工作采用嵌套去噪，导致推理复杂度高达 $O(T^2)$，难以实用化；而后续方法（如 **FastDiME**，Weng et al., ECCV 2024）虽将复杂度降至线性，却依赖静态像素差掩码，无法在反向扩散过程中自适应聚焦于决策关键区域，产生全局或散乱的编辑，缺乏对因果机制的精确刻画。

**MaskDiME** 针对上述瓶颈提出了一种无训练的扩散框架，其核心机制是**自适应双掩码**（Adaptive Dual-mask）：在反向扩散的每一步，基于分类器损失梯度动态生成噪声级掩码 $M^z$ 和清洗级掩码 $M^x$，将梯度引导的更新严格限制在决策相关像素上，同时保留原图背景的语义一致性。这一设计将传统扩散反事实的全局更新转化为**决策驱动的局部编辑**，在保持单步线性复杂度 $O(T)$ 的同时，实现了空间聚焦的精准修改。

在 CelebA、BDD100K 和 ImageNet 等多领域基准上，MaskDiME 取得了 100% 的 Flip Rate 和最低的 FID（CelebA Smile 上仅 0.71），推理速度较 DiME 提升超过 30 倍，GPU 显存占用仅为 ACE 和 RCSB 的约十分之一。消融实验进一步证实，移除自适应掩码后 FID 飙升至 95.76、Flip Rate 骤降至 55.2%，而恢复双掩码机制可将决策一致性指标 COUT 从 −0.16 提升至 0.87，验证了动态空间约束是性能突破的关键因果杠杆。

### 视觉反事实解释的需求与矛盾

深度神经网络在关键决策场景（如医疗诊断、自动驾驶、身份验证）中的广泛应用，催生了对模型决策可解释性的迫切需求。视觉反事实解释（Visual Counterfactual Explanations, VCE）通过生成“若输入特征发生何种最小改变，模型决策将翻转为目标类别”的修改图像，为理解分类器的决策边界提供了直观手段。然而，生成高质量反事实解释面临三重核心矛盾：**修改必须足够显著以翻转决策**（有效性），**同时保持原图语义结构和视觉真实性**（保真度），**且修改应聚焦于分类器实际依赖的因果区域**（决策相关性）。

### 扩散模型在反事实生成中的进展与瓶颈

近年来，扩散模型因其强大的图像生成能力被引入反事实解释任务。以 **DiME**（Jeanneret et al., ACCV 2022）为代表的早期工作，通过分类器梯度引导扩散反向过程，实现了无需额外训练的决策翻转编辑。然而，这类方法存在两个根本性瓶颈：

**计算效率瓶颈。** DiME 采用嵌套去噪策略，每次采样需递归重构清洗图像，导致推理复杂度高达 $O(T^2)$（其中 $T$ 为扩散步数），生成单张反事实图像耗时极长。后续 **FastDiME**（Weng et al., ECCV 2024）虽将复杂度降至线性 $O(T)$，但引入了像素差掩码（pixel-difference mask）来约束编辑区域，这种静态掩码无法随扩散过程自适应调整，限制了编辑精度。

**空间编辑精度瓶颈。** 全局梯度引导（DiME）使扩散更新遍布整幅图像，产生与决策无关的背景修改（如图1所示，DiME 在翻转“微笑”属性时改变了发型、肤色等非因果区域）。静态像素差掩码（FastDiME）虽限制了编辑范围，但其掩码基于初始图像与当前输出的差异计算，缺乏对分类器决策机制的语义理解，导致编辑区域分散且不适应反向扩散过程中逐步演变的语义需求。**RCSB**（Sobieski et al., ICLR 2025）尝试使用积分梯度生成固定掩码，但掩码一旦确定便在整个扩散过程中保持不变，无法响应中间步骤的梯度信号变化。

上述方法的共同缺陷在于：**掩码策略与分类器决策机制脱节**。它们要么不使用掩码（全局编辑），要么使用静态或非自适应的掩码，未能利用扩散过程每一步的分类器梯度信息来动态定位决策关键区域。这导致生成的反事实图像要么修改过度（破坏背景一致性），要么修改不足（翻转失败），难以在高效推理的同时实现语义一致且聚焦决策的局部修改。

### 本文动机与核心思路

针对上述瓶颈，本文提出 **MaskDiME**——一个自适应掩码扩散框架，核心动机是将扩散模型的反向过程与分类器梯度引导深度耦合，通过动态空间掩码替代全局更新。其关键洞察在于：**分类器关于输入图像的损失梯度天然编码了决策关键区域的空间信息**，在反向扩散的每一步提取该梯度信号并构建自适应掩码，可以迫使编辑集中到决策相关像素，同时保留原图背景。

具体而言，MaskDiME 设计了**自适应双掩码机制**：基于分类器梯度动态生成噪声级掩码 $M^z$ 和清洗级掩码 $M^x$，分别在去噪更新和背景保留两个层面控制编辑范围。噪声级掩码约束梯度引导的去噪过程仅在决策关键区域进行，清洗级掩码则将非编辑区域与原图混合以保持结构一致性。配合基于 Tweedie 公式的一步清洗图像估计，MaskDiME 以单步线性复杂度 $O(T)$ 和无训练方式，实现了高保真、决策驱动的局部图像编辑。

## 核心方法与创新机理

### 瓶颈定位：扩散反事实生成的效率-精度困境

现有基于扩散模型的反事实解释方法面临双重瓶颈。其一，**计算成本高昂**：以 **DiME**（Jeanneret et al., ACCV 2022）为代表的经典方法采用嵌套去噪架构，每步反向采样需递归重构清洗图像，导致 O(T²) 的采样复杂度，推理速度极慢。其二，**空间编辑精度不足**：**DiME** 的全局梯度引导使得整幅图像参与更新，而 **FastDiME**（Weng et al., ECCV 2024）虽将复杂度降至 O(T)，却依赖静态像素差掩码，无法随扩散步骤自适应调整编辑区域，导致修改分散或偏离决策关键像素。

### 因果调控旋钮：自适应双掩码机制

MaskDiME 的核心创新在于将扩散反向过程与分类器梯度引导解耦为**空间选择性更新**。其调控旋钮是**自适应双掩码机制**——在反向扩散的每一步，基于分类器损失的空间梯度动态生成两个二进制掩码：

- **噪声级掩码 M^z**：约束从 z_t 到 z_{t-1} 的去噪更新范围，仅允许梯度幅值位于 top-k% 的像素参与采样。
- **清洗级掩码 M^x**：在 M^z 基础上进一步收缩（top-ρk%，ρ∈(0,1]），控制估计的清洗图像与原图的混合边界，保留背景一致性。

这一机制将传统的“全局更新”转化为“决策驱动局部编辑”，使扩散过程自主聚焦于面部表情、驾驶动作等因果属性区域，无需额外训练或人工标注。

### 关键改进槽位

| 改进维度 | 基线方法局限 | MaskDiME 方案 | 证据强度 |
|---------|-------------|--------------|---------|
| **采样复杂度** | O(T²) 嵌套去噪（DiME） | O(T) 单步 Tweedie 估计（Eq.4） | 高：推理速度 >30× vs DiME，>2.5× vs FastDiME（Fig.4） |
| **空间更新方式** | 全局梯度引导（DiME）/ 静态像素差掩码（FastDiME） | 每步基于分类器梯度计算的自适应双掩码 M^z, M^x（Eq.3, Eq.5） | 高：热力图显示更新逐步聚焦决策区域（Fig.3） |
| **梯度引导强度控制** | 多个超参数 λ_c, λ_p, λ_l 需反复调节 | 统一缩放因子 s 控制整体引导强度（Eq.7） | 高：消融实验证实 s 增大使编辑逐步聚焦（Fig.6） |
| **清洗图像获取** | DiME 递归重构 | Tweedie 公式一步估计（Eq.4） | 高：线性复杂度保证，无精度损失 |

### 从梯度到掩码：空间约束的实现路径

MaskDiME 的空间约束并非外部注入，而是从分类器自身的决策信号中提取。具体流程为：

1. **提取分类损失的空间梯度**：计算联合损失关于当前噪声图像 z_t 的梯度，并通过重参数化转换为关于清洗图像 x_t 的梯度（Eq.7-8）。
2. **构建梯度幅值图**：对通道维度取绝对值后平均，得到单通道空间梯度图 G_t（Eq.9），反映每个像素对分类决策的敏感度。
3. **阈值化生成双掩码**：对 G_t 取 top-k% 像素构成 M^z，再取 top-ρk% 构成 M^x，并施加形态学膨胀以平滑边界。
4. **掩码约束的更新与混合**：M^z 约束去噪采样仅修改关键区域（Eq.3），M^x 控制清洗图像估计与原图的混合比例（Eq.5），确保未编辑区域与原图完全一致。

### 与现有掩码策略的本质区别

Figure 3 的热力图可视化揭示了 MaskDiME 自适应双掩码与现有策略的根本差异：
- **像素差掩码**（如 FastDiME）在整个扩散过程中固定不变，无法适应语义演变，导致更新分散。
- **固定掩码**（如 RCSB 的区域约束）缺乏与分类决策的动态关联，可能遗漏或误包含编辑区域。
- **自适应双掩码**随扩散步骤逐步收缩和聚焦，从早期步骤的粗粒度定位演进到后期步骤的精细语义编辑，实现“由粗到精”的决策驱动修改。

消融实验（Table 4）量化了这一创新的贡献：移除自适应掩码和梯度缩放后，方法退化为全局扩散，FID 飙升至 95.76，Flip Rate 仅 55.2%；恢复双掩码（ρ=1）将 FID 降至 0.71，决策一致性 COUT 升至 0.81；进一步细化清洗掩码混合比（ρ=0.5）使 COUT 提升至 0.87，同时保持 FID 不变。

MaskDiME 将视觉反事实生成建模为**训练无关的图像编辑任务**，其核心 pipeline 由四个紧密耦合的模块构成，整体流程如图2所示。

**输入与初始化**：给定原始图像 $x$、目标类别 $y$ 和预训练分类器 $C$，首先通过前向扩散过程将 $x$ 加噪至起始时间步 $\tau$，得到噪声图像 $z_\tau = \tilde{z}_\tau$，同时保留完整的前向噪声轨迹 $\{\tilde{z}_t\}_{t=1}^\tau$ 作为后续反向去噪的参考基准。

**梯度引导反向去噪**：从 $z_\tau$ 开始，在每一步 $t$ 计算联合损失 $L(x_t; y, x)$ 关于当前噪声图像 $z_t$ 的梯度，并通过重参数化技巧将梯度从清洗图像空间映射到噪声空间：

$$\nabla z_t = s \frac{1}{\sqrt{\bar{\alpha}_t}} \nabla_{x_t} L(x_t; y, x)$$

其中 $s$ 为统一的梯度缩放因子，控制整体引导强度。该梯度用于调整后验均值，使采样过程朝向目标类别 $y$ 偏移。联合损失由分类损失、感知损失和 L1 损失加权组合：

$$L(x_t; y, x) = \lambda_c L_{\mathrm{class}}(C(y|x_t)) + \lambda_p L_{\mathrm{perc}}(x_t, x) + \lambda_l L_{\mathrm{L1}}(x_t, x)$$

**自适应双掩码生成**：在每个去噪步，从分类器损失的空间梯度中提取决策关键区域。具体而言，先计算分类损失关于 $z_t$ 的梯度，再对通道维度取绝对值平均，得到单通道空间梯度图：

$$G_t = \left| \nabla_{z_t}^{\mathrm{class}} \right|_{\mathrm{avg}} \in \mathbb{R}^{1 \times H \times W}$$

基于 $G_t$ 按 top-$k\%$ 阈值生成噪声级掩码 $M_t^z$，并在 $M_t^z$ 内部按 top-$\rho k\%$ 阈值生成清洗级掩码 $M_t^x$（$\rho \in (0,1]$），满足 $M_t^x \subseteq M_t^z$。掩码经形态学膨胀后用于约束后续更新。

**空间约束更新与混合**：噪声级掩码 $M_t^z$ 控制从 $z_t$ 到 $z_{t-1}$ 的去噪更新范围，仅在掩码区域内应用梯度引导采样，其余区域回退到原始前向轨迹：

$$z_{t-1} = M_t^z \odot \mathcal{N}(\mu_\theta(z_t) - \Sigma_\theta(z_t) \nabla_{z_t}, \Sigma_\theta(z_t)) + (1 - M_t^z) \odot \tilde{z}_{t-1}$$

随后通过 Tweedie 公式从 $z_{t-1}$ 一步估计当前清洗图像：

$$\hat{x}_0^{(t-1)} = \frac{z_{t-1} - \sqrt{1 - \bar{\alpha}_{t-1}} \epsilon_\theta(z_{t-1})}{\sqrt{\bar{\alpha}_{t-1}}}$$

清洗级掩码 $M_t^x$ 进一步将估计的清洗图像与原始图像 $x$ 混合，保留背景一致性：

$$x_{t-1} = M_t^x \odot \hat{x}_0^{(t-1)} + (1 - M_t^x) \odot x$$

**输出**：经过 $\tau$ 步迭代后，最终生成的反事实图像 $x_0$ 仅在决策关键区域发生语义修改，同时保持原始图像的全局结构和背景不变。

**关键设计优势**：与传统扩散反事实方法相比，该 pipeline 实现了三个根本性改进：（1）通过 Tweedie 公式的一步估计替代 **DiME**（Jeanneret et al., ACCV 2022）的嵌套去噪，将采样复杂度从 $O(T^2)$ 降至 $O(T)$；（2）自适应双掩码替代 **FastDiME**（Weng et al., ECCV 2024）的静态像素差掩码，使空间约束随扩散步骤动态演化；（3）统一缩放因子 $s$ 替代多超参数调节，简化了引导强度的控制。

### 补充图表

![[assets/figures/papers/paper_list_l897_https_arxiv_org_abs_2602_18792/figures/002_Figure_2.jpg]]
*Figure 2: Overview of MaskDiME. We illustrate a complete counterfactual generation process (No*

MaskDiME 将反事实生成建模为一种受空间约束的图像编辑任务。其核心由四个紧密协作的模块构成：前向扩散加噪、梯度引导反向去噪、自适应双掩码生成，以及清洗图像估计与混合。整体流程遵循从原图到反事实图像的线性时间推理范式。

### 前向扩散加噪

给定原始图像 $x$，前向扩散过程按照预定义的噪声调度将其逐步加噪至时间步 $\tau$，生成噪声样本轨迹：

$$\tilde{z}_t = \sqrt{\bar{\alpha}_t} x + \sqrt{1 - \bar{\alpha}_t} \epsilon, \quad \epsilon \sim \mathcal{N}(0, I) \tag{1}$$

其中 $\bar{\alpha}_t$ 为累积噪声调度系数，$\epsilon$ 为标准高斯噪声。该轨迹为后续反向去噪提供未受引导的参照路径。

### 梯度引导反向去噪

在反向扩散的每一步，MaskDiME 利用分类器损失梯度调整后验均值，引导采样朝向目标类别 $y$。标准的梯度引导采样分布为：

$$\tilde{z}_{t-1} \sim \mathcal{N}\big(\mu_\theta(\tilde{z}_t) - \Sigma_\theta(\tilde{z}_t) \nabla_{\tilde{z}_t} L(\tilde{z}_t; y), \Sigma_\theta(\tilde{z}_t)\big) \tag{2}$$

其中 $\mu_\theta$ 与 $\Sigma_\theta$ 为预训练扩散模型的均值与方差函数，$L$ 为联合损失。

为将全局更新转化为决策驱动的局部编辑，MaskDiME 引入噪声级掩码 $M_t^z$ 对去噪更新进行空间约束：

$$z_{t-1} = M_t^z \odot \mathcal{N}(\mu_\theta(z_t) - \Sigma_\theta(z_t) \nabla_{z_t}, \Sigma_\theta(z_t)) + (1 - M_t^z) \odot \tilde{z}_{t-1} \tag{3}$$

该式将引导更新限制在 $M_t^z$ 标记的决策关键区域内，其余区域则回退至原始前向轨迹 $\tilde{z}_{t-1}$，从而保留背景一致性。

### 清洗图像估计与混合

传统方法（如 DiME）需递归重构清洗图像，计算开销大。MaskDiME 采用 Tweedie 公式实现一步估计：

$$\hat{x}_0^{(t-1)} = \frac{z_{t-1} - \sqrt{1 - \bar{\alpha}_{t-1}} \epsilon_\theta(z_{t-1})}{\sqrt{\bar{\alpha}_{t-1}}} \tag{4}$$

其中 $\epsilon_\theta$ 为预训练噪声预测网络。随后，通过清洗级掩码 $M_t^x$ 将估计的清洗图像与原始图像混合：

$$x_{t-1} = M_t^x \odot \hat{x}_0^{(t-1)} + (1 - M_t^x) \odot x \tag{5}$$

$M_t^x \subseteq M_t^z$，其空间范围更小，用于精确控制哪些像素接受编辑，其余像素直接保留原图信息，从而在语义一致性与结构保真度之间取得平衡。

### 联合损失与梯度重参数化

引导反向去噪的梯度来源于联合损失函数，该损失组合了分类损失、感知损失与 L1 损失：

$$L(x_t; y, x) = \lambda_c L_{\mathrm{class}}(C(y|x_t)) + \lambda_p L_{\mathrm{perc}}(x_t, x) + \lambda_l L_{\mathrm{L1}}(x_t, x) \tag{6}$$

其中 $C(y|x_t)$ 为目标分类器对当前图像 $x_t$ 预测类别 $y$ 的置信度，$L_{\mathrm{perc}}$ 与 $L_{\mathrm{L1}}$ 分别约束感知相似度和像素级一致性。

由于损失定义在清洗图像 $x_t$ 上，而反向采样操作于噪声图像 $z_t$，需通过重参数化将梯度传递至噪声空间。MaskDiME 引入统一缩放因子 $s$ 控制整体引导强度：

$$\nabla z_t = s \frac{1}{\sqrt{\bar{\alpha}_t}} \nabla_{x_t} L(x_t; y, x) \tag{7}$$

该设计将 DiME 中多个需反复调节的超参数（$\lambda_c, \lambda_p, \lambda_l$）简化为单一控制变量，显著降低了调参复杂度。

### 自适应双掩码生成

自适应双掩码是 MaskDiME 的核心创新。掩码的构建基于分类损失关于噪声图像的空间梯度：

$$\nabla_{z_t}^{\mathrm{class}} = \frac{1}{\sqrt{\bar{\alpha}_t}} \nabla_{x_t} L_{\mathrm{class}}\big(C(y|x_t)\big) \tag{8}$$

对通道维度取绝对值后平均，得到单通道空间梯度幅值图：

$$G_t = \left| \nabla_{z_t}^{\mathrm{class}} \right|_{\mathrm{avg}} \in \mathbb{R}^{1 \times H \times W} \tag{9}$$

基于 $G_t$，按 top-$k\%$ 和 top-$\rho k\%$ 阈值分别生成噪声级掩码 $M_t^z$ 和清洗级掩码 $M_t^x$（$\rho \in (0,1]$），并施加形态学膨胀以平滑掩码边界。由于 $G_t$ 在每一步根据当前分类器梯度动态计算，掩码的空间焦点随扩散进程自适应演化，始终锁定与决策最相关的像素区域。

### 补充图表

![[assets/figures/papers/paper_list_l897_https_arxiv_org_abs_2602_18792/figures/003_Figure_3.jpg]]
*Figure 3: Heatmap visualization of diffusion trajectories with different masking strategies. Each column shows noisy samples*

## 实验与关键发现

### 主要定量结果

**人脸属性编辑（CelebA / CelebA-HQ）。** 在 Table 1 的 smile 与 age 两个属性上，MaskDiME 均取得 **100% Flip Rate (FR)**，即所有生成样本均被目标分类器判定为目标类别。在视觉真实性指标上，MaskDiME 的 FID 达到 **0.71 (smile)** 和 **0.77 (age)**，为所有对比方法中最低；结构一致性指标 COUT 分别达到 **0.87 (smile)** 和 **0.84 (age)**，处于最优或次优水平。相比之下，全局编辑的 DiME 在同一 benchmark 上 FID 为 24.36 (smile)，FastDiME 为 1.18 (smile)，说明自适应双掩码在维持图像自然度方面作用显著。

**驾驶场景决策（BDD100K / BDD-OIA）。** Table 2 显示，MaskDiME 在 BDD 系列数据集上同样保持 100% FR，且 FID 指标显著优于基于 GAN 的 STEEX 和两阶段对抗方法 ACE。在衡量决策一致性的 COUT 指标上，MaskDiME 取得最优或次优结果，表明生成的驾驶反事实不仅改变了分类器决策，同时保留了与原始场景的结构对应关系。

**通用图像分类（ImageNet）。** Table 3 的多类对反事实任务中，MaskDiME 在多个类别对上取得最优 FID 与 COUT，验证了该方法在自然图像域上的泛化能力。需要注意的是，部分 baseline 结果（标记为 †）直接引用自 RCSB 原文，非本文复现，跨方法比较时需考虑实验设置差异。

### 效率与资源消耗

Figure 4 以散点图形式将各方法的 FID、推理时间与 GPU 显存峰值进行联合对比。在 CelebA smile 任务上（batch size = 5），MaskDiME 的推理速度比 DiME 快 **30 倍以上**，比 FastDiME 快 **2.5 倍以上**，同时 GPU 显存占用仅为 ACE 和 RCSB 的 **约十分之一**。这一效率优势源于两个设计：一是用 Tweedie 公式一步估计清洗图像，消除了 DiME 的嵌套去噪（O(T²) → O(T)）；二是自适应双掩码将去噪更新限制在局部区域，避免了全图梯度计算与存储。

![[assets/figures/papers/paper_list_l897_https_arxiv_org_abs_2602_18792/figures/005_Figure_4.jpg]]
*Figure 4: Comparison of methods on the CelebA smile attribute by FID (from Tab. 1), runtime (batch size = 5). The area of the circles indicates the peak GPU memory allocated during the sampling process. MaskDiME is significantly faster than previous methods, while also achieving the lowest FID, and sustaining low GPU usage—approximately one-tenth of that required by ACE and RCSB. See Supplementary Tab. 7 for quantitative results*

### 消融实验

Table 4 系统拆解了 MaskDiME 各组件的贡献，所有实验在 CelebA smile 上进行：

![[assets/figures/papers/paper_list_l897_https_arxiv_org_abs_2602_18792/figures/010_Table_4.jpg]]
*Table 4: Ablation study of MaskDiME on Smile of CelebA*

- **移除梯度缩放与自适应掩码（s=1 & w/o mask）：** 方法退化为全局扩散编辑，FID 飙升至 **95.76**，COUT 跌至 **-0.16**，FR 仅为 **55.2%**。此时生成图像几乎完全破坏原图结构，且过半样本未能成功翻转分类器决策。
- **引入自适应双掩码（+ mask, ρ=1）：** FID 骤降至 **0.71**，COUT 回升至 **0.81**，FR 恢复至 100%。这表明掩码机制成功将编辑约束在决策关键区域，避免了无关背景的退化。
- **细化清洗掩码混合比（MaskDiME, ρ=0.5）：** 在保持 FID 0.71 的前提下，COUT 进一步从 0.81 提升至 **0.87**。更严格的清洗掩码 Mˣ 使背景保留更完整，从而提高了结构一致性。
- **增大梯度缩放因子 s：** Figure 6 的视觉消融显示，随着 s 增大，扩散更新沿时间步逐步聚焦到面部表情区域，生成的反事实样本从模糊散乱过渡到语义一致、视觉逼真的局部编辑。

![[assets/figures/papers/paper_list_l897_https_arxiv_org_abs_2602_18792/figures/009_Figure_6.jpg]]
*Figure 6: Ablation study on the No Smile → Smile sample of CelebA. Increasing the gradient scaling (s) and introducing Adaptive Dual-mask (M ) progressively improve MaskDiME’s results, localizing edits to decision-relevant regions and yielding realistic, semantically consistent counterfactuals*

### 定性分析

Figure 5 将 MaskDiME 与 ACE l₁ 进行定性对比。ACE 的像素差掩码倾向于产生散乱的、覆盖全图的修改，而 MaskDiME 的编辑集中在与决策相关的局部区域（如嘴唇、眼部），同时完好保留发型、背景等非因果区域。Figure 3 的热力图可视化进一步揭示了不同掩码策略下的扩散轨迹：固定掩码和像素差掩码的更新在扩散早期即扩散至全图，而自适应双掩码使更新逐步收敛到分类器梯度的峰值区域，实现了“先探索、后聚焦”的语义编辑过程。

![[assets/figures/papers/paper_list_l897_https_arxiv_org_abs_2602_18792/figures/008_Figure_5.jpg]]
*Figure 5: Qualitative results. Compared with ACE l1, MaskDiME effectively preserves the overall image structure and produces more pronounced counterfactual explanations, with superior performance in semantic consistency, visual realism, and modification precision*

### 失败模式与待验证问题

本文未系统报告失败案例。从方法机理推断，当分类器梯度在空间上噪声较大或分散时（如 ImageNet 多类场景），自适应掩码可能无法准确定位决策关键区域，导致编辑效果下降——这一推测需要手动验证。此外，所有评估依赖感知相似度指标（FID、LPIPS）和分类器一致性指标（COUT），当反事实修改区域占比较小时，这些指标可能因大范围未修改背景而偏向乐观，实际编辑质量仍需人工评判佐证。

## 定位与知识库关联

### 扩散反事实生成的技术演进

MaskDiME 立足于基于扩散模型的反事实解释（Counterfactual Explanation, CE）这一新兴方向。该方向的奠基性工作是 **DiME**（Jeanneret et al., ACCV 2022），它首次将分类器引导的扩散模型引入 CE 生成，通过嵌套去噪（nested denoising）在每一步反向采样中递归估计清洗图像并计算梯度。这一设计虽然开创性地实现了高保真反事实生成，却带来 $O(T^2)$ 的计算复杂度和极高的推理延迟，严重限制了其实际部署。

随后，**FastDiME**（Weng et al., ECCV 2024）将复杂度降至 $O(T)$，通过像素差掩码（pixel-difference mask）约束更新区域，在保持线性时间的同时试图实现局部编辑。然而，其掩码基于静态的像素差异，无法随扩散步骤动态调整空间焦点，导致编辑区域分散或偏离决策关键语义。**RCSB**（Sobieski et al., ICLR 2025）进一步引入积分梯度构建固定掩码，但掩码在整个反向过程中保持不变，难以适应语义的逐步演化。**ACE**（Jeanneret et al., CVPR 2023）则采用两阶段对抗式框架，虽能生成局部修改，但训练成本高且 GPU 显存占用大。

MaskDiME 在上述谱系中的核心定位是：**以无训练（training-free）方式，在 $O(T)$ 线性复杂度下，将全局扩散更新转化为决策驱动的自适应局部编辑**。其关键突破在于将掩码的生成从“静态预定义”升级为“每步基于分类器梯度动态构建”，使空间约束与语义演化同步。

### 与其他范式的边界

除扩散方法外，CE 生成还存在多种技术范式。**DiVE**（Rodriguez et al., ICCV 2021）基于 VAE 的潜在空间遍历，编辑能力受限于潜在空间的解耦程度。**STEEX**（Jacob et al., ECCV 2022）使用 GAN 生成驾驶场景反事实，但依赖特定域的生成器训练。**LDCE**（Farid et al., arXiv 2023）在潜在扩散模型（LDM）的潜在空间中操作，牺牲了像素级编辑精度。**TiME**（Jeanneret et al., WACV 2024）利用文本到图像模型实现黑盒反事实生成，但缺乏对编辑区域的空间精细控制。

MaskDiME 与这些方法的根本差异在于：它不依赖额外训练或特定域的生成器，而是直接复用预训练的无条件 DDPM 和目标分类器权重，通过梯度引导和自适应掩码实现跨域泛化。这一设计使其在 CelebA（人脸属性）、BDD100K（驾驶决策）和 ImageNet（通用物体分类）三个截然不同的视觉域上均取得领先或次优性能，验证了其作为通用框架的适用边界。

### 可迁移的机制贡献

MaskDiME 的若干设计选择具有跨方法迁移价值：

1. **Tweedie 一步清洗图像估计**：替代 DiME 的递归重构，以 $O(1)$ 代价获取当前清洗图像估计，该技巧可推广至任何需要中间清洗图像引导的扩散编辑任务。
2. **统一梯度缩放因子 $s$**：将 DiME 中需分别调节的多个超参数 $\lambda_c, \lambda_p, \lambda_l$ 简化为单一缩放因子，降低了方法在新数据集上的调参负担。论文报告 $s$ 按数据集经验设定（CelebA: 8, CelebA-HQ: 10, BDD100K/BDD-OIA: 14, ImageNet: 6.5），但未提供自动调参策略。
3. **双掩码分层约束**：噪声级掩码 $M^z$ 控制去噪更新范围，清洗级掩码 $M^x$ 控制背景保留程度，二者通过超参数 $\rho$（$M^x$ 取 $M^z$ 的 top-$\rho k\%$ 区域）耦合。这种分层设计为其他需同时控制编辑强度和背景一致性的任务提供了模板。

### 局限与开放问题

尽管 MaskDiME 在多个基准上表现优异，论文未明确列出局限性，但从实验设置和方法设计中可推断以下边界：

1. **梯度信号质量依赖分类器**：自适应掩码完全依赖分类器损失的空间梯度 $G_t$（Eq. 9）定位决策关键区域。在多类别数据集（如 ImageNet）上，梯度信号可能噪声较大或空间不一致，论文将此列为开放问题，但未提供定量分析或缓解方案。
2. **缺乏因果真值验证**：所有评估均基于代理指标（FR, FID, COUT 等），缺乏对反事实修改是否真正对应因果特征的 ground-truth 标注。这一问题在该领域普遍存在，论文亦将其列为开放挑战。
3. **感知相似度指标的评估偏差**：当大量背景区域被掩码保留时，FID 等全局感知指标可能因未修改区域的主导而高估生成质量。论文意识到这一偏差，但未提出校正方案。
4. **超参数 $\tau$ 和 $s$ 的手动设定**：反向过程的起始时间步 $\tau=60$ 和梯度缩放因子 $s$ 需按数据集手动调节，缺乏自动化或自适应机制，可能限制在全新域上的即插即用能力。

综合来看，MaskDiME 在扩散反事实生成的方法谱系中占据“高效、精准、无训练”的节点，其自适应双掩码机制为后续工作提供了可复用的设计范式，但在梯度鲁棒性、因果验证和自动化调参方面仍留有明确的改进空间。

## 原文 PDF

![[paperPDFs/CVPR_2026/MaskDiME_Adaptive_Masked_Diffusion_for_Precise_and_Efficient_Visual_Counterfactual_Explanations.pdf]]
