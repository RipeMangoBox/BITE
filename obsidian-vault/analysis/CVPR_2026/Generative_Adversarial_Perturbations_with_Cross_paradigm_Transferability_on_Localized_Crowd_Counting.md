---
title: Generative Adversarial Perturbations with Cross-paradigm Transferability on Localized Crowd Counting
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Generative_Adversarial_Perturbations_with_Cross_paradigm_Transferability_on_Localized_Crowd_Counting.pdf
project_link: null
code_link: "https://github.com/simurgh7/CrowdGen"
aliases:
- GAPCPTLCC
tags:
- CVPR_2026
- topic/generative_models_diffusion
- topic/representation_self_supervised_transfer
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 多任务损失函数，包含针对密度图模型的密度抑制损失和针对点回归模型的对数抑制损失，以及跨范式的频率约束、GradCAM注意力引导等感知约束。
primary_logic: 通过利用不同人群计数模型共享的骨干网络学到的相似潜在空间，并设计范式特定的攻击损失与通用的感知约束，可以实现跨架构的高效且隐蔽的对抗攻击。
claims:
- We introduce a novel adversarial framework that compromises both density map and point regression architectural paradigms through a comprehensive multi-task loss optimization.
- Our attack achieves on average a 7x increase in Mean Absolute Error compared to clean images while maintaining competitive visual quality, and successfully transferring across sev...
- HMoDE attacks achieve 69% higher effectiveness on P2PNet than on itself (TR = 1.69), demonstrating super-transferability.
- The full ensemble loss achieves the highest MR (60.89-60.90%) for density-map models, and attention-guided perturbations yield the best trade-off for point-regression models.
---

# Generative Adversarial Perturbations with Cross-paradigm Transferability on Localized Crowd Counting

> [!tip] 核心洞察
> 通过利用不同人群计数模型共享的骨干网络学到的相似潜在空间，并设计范式特定的攻击损失与通用的感知约束，可以实现跨架构的高效且隐蔽的对抗攻击。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向局部人群计数且跨范式可迁移的生成式对抗扰动 |
| 英文题名 | Generative Adversarial Perturbations with Cross-paradigm Transferability on Localized Crowd Counting |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.24821) · [Code](https://github.com/simurgh7/CrowdGen) |
| Topic | #topic/generative_models_diffusion #topic/representation_self_supervised_transfer #topic/generative_models_diffusion/diffusion_image_video |
| Method | CrowdGen (跨范式生成对抗扰动框架) |
| Dataset | SHHA, SHHA & UCF-QNRF |

> [!tip] 效果简介
> - SHHA (dense scenes) 上，MAE 1013.6 vs 128.0 (clean) (7.9× increase)。
> - SHHA & UCF-QNRF (cross-paradigm transfer) 上，Transfer Ratio (TR) up to 1.69 vs 1.0 (same-paradigm baseline) (up to 69% higher effectiveness on target model)。
> - SHHA (overall with FIDTM) 上，MAE / PSNR 259.76 / 19.25 dB vs DiffAttack: 1591.3 / 10.36 dB; PAP: 5.40 / 22.58 dB (balanced effectiveness (3.7× lower MAE than DiffAttack) and stealth (8.9 dB hig...)。

## 概要

### 1. 问题背景与瓶颈

人群计数是智能监控、公共安全与城市规划中的关键任务。当前主流方法可分为两大范式：**密度图回归**与**点回归**。尽管两类模型在精度上不断刷新基准，其对抗鲁棒性却鲜有系统性审视。现有针对人群计数的对抗攻击存在两个根本瓶颈：

1. **跨范式不可迁移**：已有攻击方法（如对抗补丁、优化型扰动）通常针对单一范式设计，无法在密度图模型与点回归模型之间有效迁移。
2. **攻击强度与隐蔽性失衡**：高强度的攻击往往引入显著的可察觉伪影，而隐蔽性较好的方法（如基于扩散模型的生成式攻击）又难以有效破坏计数精度。

### 2. 核心方法定位

本文提出 **CrowdGen**——首个面向局部人群计数的跨范式生成式对抗扰动框架。其核心洞察在于：不同范式的人群计数模型共享相似的骨干网络（如VGG、ResNet），因而学到的潜在空间具有高度一致性。通过利用这一共享表征，并设计范式特定的攻击损失与通用的跨范式感知约束，CrowdGen能够在单次前向传播中生成兼具攻击效能与视觉隐蔽性的对抗样本。

方法谱系上，CrowdGen区别于以下基线工作：

- **优化型攻击**（如DI²FGSM, Admix, L2T, SVRE, GRA, FIA）：依赖迭代梯度优化，计算开销大，且未针对人群计数的跨范式场景设计。
- **生成式攻击**（如DiffAttack, GE-AdvGAN）：虽支持单次生成，但未考虑密度图与点回归的范式差异，跨范式迁移能力有限。
- **人群计数专用攻击**（如PAP）：采用对抗补丁，攻击痕迹明显，隐蔽性差，且不可跨范式迁移。

### 3. 技术路线概要

CrowdGen采用**三级U-Net生成器**，输入原始图像，输出有界扰动$\delta$（$\|\delta\|_\infty \leq \epsilon$）。训练过程由多任务损失驱动：

$$\mathcal{L}_{\mathrm{attack}} = \underbrace{\mathcal{L}_{\mathrm{model}}}_{\mathrm{paradigm-specific}} + \underbrace{\mathcal{L}_{\mathrm{pert}}}_{\mathrm{cross-paradigm}}$$

其中，$\mathcal{L}_{\mathrm{model}}$根据代用模型类型自动切换：
- 对**点回归模型**：采用场景密度自适应的**对数抑制损失**（$\mathcal{L}_{\mathrm{logit}}$），压制高置信度检测头的输出。
- 对**密度图模型**：采用峰值导向的**密度图抑制损失**（$\mathcal{L}_{\mathrm{dmap}}$），同时削弱显著峰值与近阈值区域。

$\mathcal{L}_{\mathrm{pert}}$为跨范式感知约束，包含四项：
$$\mathcal{L}_{\mathrm{pert}} = \beta \cdot \mathcal{L}_{\mathrm{hinge}} + \gamma \cdot \mathcal{L}_{\mathrm{tv}} + \zeta \cdot \mathcal{L}_{\mathrm{freq}} + \kappa \cdot \mathcal{L}_{\mathrm{cam}}$$
分别控制扰动幅度（hinge loss）、空间平滑性（total variation）、频率分布（低频约束以匹配人群统计特征）与注意力区域集中度（GradCAM引导），从而在攻击强度与隐蔽性之间取得平衡。

### 4. 核心结论

实验表明，CrowdGen在多个维度上取得了突破性结果：

- **攻击效能**：在SHHA密集场景下，MAE从128.0飙升至1,013.6（**7.9倍增长**），同时保持18.81 dB的PSNR。
- **跨范式可迁移性**：在七种主流模型上的迁移比（Transfer Ratio）范围为0.55至1.69。其中，以HMoDE为代用模型生成的对抗样本，在P2PNet上的攻击效果比在自身模型上高出69%（TR=1.69），展现出**超可迁移性**。
- **效能-隐蔽性平衡**：相较于DiffAttack（MAE 1,591.3 / PSNR 10.36 dB）和PAP（MAE 5.40 / PSNR 22.58 dB），CrowdGen在FIDTM模型上以259.76 MAE和19.25 dB PSNR实现了**最优折衷**——攻击效能是高质量方法的3.7倍，同时PSNR高出8.9 dB。

### 5. 局限与待验证问题

- **物理域未验证**：当前攻击仅在数字域评估，其在物理世界（如监控摄像头拍摄场景）中的有效性与可迁移性尚待检验。
- **模型依赖性**：攻击生成需针对特定代用模型训练，对完全未知的模型架构可能无法保证最优迁移效果。
- **防御空白**：如何设计范式无关的防御机制以增强人群计数模型的鲁棒性，仍是一个开放问题。



### 人群计数任务的范式分裂与安全脆弱性

人群计数是公共安全与空间管理中的核心视觉任务，旨在从单张图像中估计场景内的总人数。当前主流方法分化为两种架构范式：**密度图回归（density-map regression）** 与 **点回归（point regression）**。密度图方法预测逐像素的人群密度热图，通过对热图求和获得最终计数；点回归方法则直接输出一组头部坐标及其置信度，计数即为高置信度预测点的数量。尽管两者在标准评测上均取得了显著进展，但它们共享一个被长期忽视的安全隐患——**深度神经网络对精心构造的对抗扰动高度敏感**。

在人群计数场景中，对抗攻击的现实威胁尤为突出：恶意行为者可能通过物理张贴对抗补丁或数字篡改监控画面，使系统严重低估人群规模，从而绕过容量管控、制造踩踏风险。然而，现有对抗攻击研究在该领域存在两个根本性缺口。

### 现有对抗攻击的跨范式盲区

第一个缺口是**范式不可知性（paradigm-agnosticism）的缺失**。通用对抗攻击方法——无论是基于迭代优化的 **DI²FGSM**（Xie et al., CVPR 2019）、**Admix**（Wang et al., ICCV 2021）、**L2T**（Zhu et al., CVPR 2024），还是基于生成式的 **DiffAttack**（Chen et al., TPAMI 2024）、**GE-AdvGAN**（Zhu et al., SDM 2024）——均假设攻击者已知目标模型的输出形式，并针对单一范式设计损失函数。当攻击在密度图模型上生成的对抗样本迁移至点回归模型时，攻击效能急剧衰减，反之亦然。这种范式间的不可迁移性源于两类模型在输出空间上的根本差异：密度图模型输出连续空间分布，而点回归模型输出离散位置集合，单一范式的攻击损失无法同时欺骗两者。

第二个缺口是**攻击强度与隐蔽性的失衡**。针对人群计数的专用攻击方法如 **PAP**（Liu et al., CCS 2022）采用物理对抗补丁，虽能有效干扰计数，但引入了高度可见的异常图案，极易被人眼或安防系统察觉。通用方法则通常仅依赖 $L_p$ 范数约束扰动幅度，忽略了人群场景特有的感知特性——自然人群统计呈现低频空间分布，而高频扰动不仅视觉突兀，还破坏了这一统计先验，降低了攻击的隐蔽性。

### 本文动机：跨范式可迁移的隐蔽对抗攻击

上述分析揭示了一个核心瓶颈：**现有攻击缺乏跨密度图与点回归范式的可迁移性，且无法在攻击效能与隐蔽性之间取得良好平衡**。本文的动机正是填补这一双重空白——设计一种对抗攻击框架，使其能够在不同架构范式的人群计数模型之间高效迁移，同时生成视觉上难以察觉的扰动。

实现这一目标的关键洞察在于：尽管密度图与点回归模型在输出层存在显著差异，它们通常共享相似的卷积骨干网络（如 VGG、ResNet），这些骨干网络在 ImageNet 预训练后学到的潜在空间具有高度相似性。通过利用这一共享表示空间，并设计**范式特定的攻击损失**与**通用的跨范式感知约束**，有望实现跨架构的高效且隐蔽的攻击。本文提出的 **CrowdGen** 框架正是基于这一洞察，通过多任务损失优化在攻击强度、可迁移性与视觉质量三者之间寻求最优折衷。



## 核心方法与创新机理

### 1. 问题瓶颈：跨范式可迁移性缺失与攻击-隐蔽失衡

现有针对人群计数的对抗攻击面临两个核心瓶颈。其一，**跨范式可迁移性缺失**：已有方法或针对密度图模型设计，或仅关注点回归模型，缺乏能够同时攻击两种主流计数范式的统一框架。其二，**攻击强度与隐蔽性的失衡**：基于迭代优化的攻击（如 **DI²FGSM**（Xie et al., CVPR 2019）、**Admix**（Wang et al., ICCV 2021））虽然攻击效果强，但扰动可见度较高；而生成式攻击（如 **DiffAttack**（Chen et al., TPAMI 2024））在视觉质量上有优势，却牺牲了攻击效能。本文的核心突破在于：**通过统一的生成式框架，首次实现了跨密度图与点回归范式的可迁移对抗攻击，并在攻击效能与隐蔽性之间取得了最优平衡**。

### 2. 关键创新：范式自适应多任务损失设计

本文的核心创新围绕一个**范式自适应的多任务损失函数**展开，该损失函数是驱动跨范式可迁移性的“因果旋钮”。其设计逻辑如下：

#### 2.1 范式特定的模型损失（$\mathcal{L}_{\mathrm{model}}$）

针对不同计数范式的输出特性，设计了差异化的攻击策略：

- **点回归模型**：采用**场景密度自适应的对数抑制损失**（Logit Suppression Loss）。对于密集场景，公式（4）对高置信度区域的 logit 进行最小化：
  $$\mathcal{L}_{\mathrm{dense}} = -\frac{1}{|\mathcal{P}_{\mathrm{high}}|} \sum_{i \in \mathcal{P}_{\mathrm{high}}} \left[ l_i^{(h)} - \log(1 - s_i^{(h)} + \epsilon) \right]$$
  并通过自适应置信度阈值 $\tau(t) = \max\left(\tau_{\min}, \tau_{\max} - \nu \cdot \frac{t}{T_{\max}}\right)$（公式 3）在训练过程中动态筛选被攻击的高置信度检测点。对于稀疏场景则采用对应的稀疏损失（公式 5），两者通过公式（6）根据真实人数阈值自适应切换。

- **密度图模型**：采用**峰值导向的密度图抑制损失**（Density Suppression Loss）。该方法同时攻击密度图中的**绝对强度**（峰值幅值）和**相对显著性**（峰值突出度）：
  $$\mathcal{L}_{\mathrm{hmap}} = \frac{1}{|\mathcal{Q}'|} \sum_{(x,y)\in\mathcal{Q}'} \mathcal{D}(x,y) + \frac{\eta_h}{|\mathcal{Q}^*|} \sum_{(x,y)\in\mathcal{Q}^*} \mathcal{D}(x,y)$$
  其中 $\mathcal{Q}'$ 为显著峰值区域，$\mathcal{Q}^*$ 为近阈值区域，实现了对密度图的多层次抑制。

#### 2.2 跨范式感知约束（$\mathcal{L}_{\mathrm{pert}}$）

为提升扰动的隐蔽性和跨范式可迁移性，设计了四个通用约束：

- **频率域约束**（$\mathcal{L}_{\mathrm{freq}}$）：抑制扰动的高频分量，使其符合自然人群统计的低频特征：
  $$\mathcal{L}_{\mathrm{freq}} = \frac{1}{|\Omega|} \sum_{\omega \in \Omega} |\mathcal{F}(\delta)(\omega)|$$

- **GradCAM 注意力引导**（$\mathcal{L}_{\mathrm{cam}}$）：将扰动集中在模型语义关注区域，最小化注意力区域之外的扰动：
  $$\mathcal{L}_{\mathrm{cam}} = \frac{1}{HW} \| |\delta| - \delta(\rho) \|_1$$

- **全变分平滑**（$\mathcal{L}_{\mathrm{tv}}$）与 **L2 幅度约束**（$\mathcal{L}_{\mathrm{hinge}}$）：共同构成完整的感知约束组合：
  $$\mathcal{L}_{\mathrm{pert}} = \beta \cdot \mathcal{L}_{\mathrm{hinge}} + \gamma \cdot \mathcal{L}_{\mathrm{tv}} + \zeta \cdot \mathcal{L}_{\mathrm{freq}} + \kappa \cdot \mathcal{L}_{\mathrm{cam}}$$

### 3. 生成范式变革：从迭代优化到单次前向传播

与传统的迭代优化型攻击不同，本文采用**基于 3 级 U-Net 的生成器 $G_\theta$**，将原始图像 $I$ 映射为有界扰动 $\delta = G_\theta(I)$（满足 $\|\delta\|_\infty \leq \epsilon$）。这一设计带来了两个关键优势：

1. **推理效率**：单次前向传播即可生成对抗样本，无需针对每张图像进行迭代优化。
2. **跨架构泛化**：通过利用不同计数模型共享骨干网络学到的相似潜在空间，生成器能够学习到范式无关的对抗模式，从而实现跨架构的可迁移攻击。

### 4. 与现有方法的本质差异

| 维度 | 现有方法 | 本文方法（CrowdGen） |
|------|----------|---------------------|
| 攻击范式 | 单一范式（密度图或点回归） | 跨范式自适应 |
| 点回归攻击 | 不支持 | 场景密度自适应的对数抑制 |
| 密度图攻击 | 无差别攻击 | 峰值导向的多层次抑制 |
| 感知约束 | 仅 Lp 范数 | 频率域 + GradCAM + 全变分 + L2 联合约束 |
| 生成方式 | 迭代优化或非自适应生成 | U-Net 单次前向生成 |

### 5. 创新有效性验证

消融实验证实了各创新组件的贡献。在密度图范式下，完整的损失组合（$\mathcal{L}_{\mathrm{hmap}}/\mathcal{L}_{\mathrm{peak}} + \mathcal{L}_{\mathrm{hinge}} + \mathcal{L}_{\mathrm{tv}} + \mathcal{L}_{\mathrm{freq}} + \mathcal{L}_{\mathrm{cam}}$）使漏检率（MR）达到 60.89–60.90%，PSNR 约 17.47 dB；单独添加频率域约束或 GradCAM 引导均可将 MR 提升至约 60%。在点回归范式下，基线（$\alpha\mathcal{L}_{\mathrm{logit}} + \beta\mathcal{L}_{\mathrm{hinge}}$）的 MR 为 45.15%，添加 $\mathcal{L}_{\mathrm{cam}}$ 后 MR 提升至 45.61% 且 PSNR 达 19.10 dB，达到最佳折衷。跨范式可迁移性方面，以 HMoDE 为代用模型生成的对抗样本在 P2PNet 上的攻击效果比在自身模型上高 69%（TR = 1.69），验证了“超可迁移性”的存在。

**需注意的局限**：攻击仅在数字域验证，尚未在物理世界测试；且攻击生成需要针对特定代用模型训练，对完全未知模型的最优迁移性无法保证。



CrowdGen 采用**生成式对抗扰动**范式，通过一个训练好的生成器实现单次前向传播即可产生对抗样本，无需在推理阶段进行迭代优化。其核心瓶颈在于：现有对抗攻击无法同时作用于密度图回归与点回归两种人群计数范式，且攻击强度与隐蔽性难以兼顾。CrowdGen 通过**范式特定的攻击损失**与**跨范式共享的感知约束**的组合，利用不同计数模型骨干网络学到的相似潜在空间，实现了跨架构的高效且隐蔽的对抗攻击。

**输入输出流**：给定一张 RGB 图像 $I \in \mathbb{R}^{H \times W \times 3}$，生成器 $G_\theta$ 输出一个有界扰动 $\delta = G_\theta(I)$，满足 $\|\delta\|_\infty \leq \epsilon$。对抗样本由 $I_{adv} = I + \delta$ 直接获得。生成器采用 **3 级 U-Net** 架构（Figure 2），训练时输入图像被缩放至 $512 \times 512$。

**训练损失的总框架**（Eq. 1）为：

$$\mathcal{L}_{\text{attack}} = \underbrace{\mathcal{L}_{\text{model}}}_{\text{范式特定}} + \underbrace{\mathcal{L}_{\text{pert}}}_{\text{跨范式}}$$

其中 **$\mathcal{L}_{\text{model}}$** 根据代用模型的范式类型自动切换（Eq. 2）：

$$\mathcal{L}_{\text{model}} = \begin{cases} \mathcal{L}_{\text{logit}} & \text{点回归模型 } M_p \\ \mathcal{L}_{\text{dmap}} & \text{密度图模型 } M_D \end{cases}$$

- **点回归模型**：采用场景密度自适应的对数抑制损失 $\mathcal{L}_{\text{logit}}$（Eq. 4–6），根据真实人数阈值 $C_{\text{sparse}}$ 在密集场景损失 $\mathcal{L}_{\text{dense}}$ 与稀疏场景损失 $\mathcal{L}_{\text{sparse}}$ 之间切换。训练过程中，置信度阈值 $\tau(t)$ 随时间衰减（Eq. 3），逐步减少被攻击的高置信度检测数量。
- **密度图模型**：采用峰值导向的密度图抑制损失 $\mathcal{L}_{\text{dmap}}$，包含热力图抑制损失 $\mathcal{L}_{\text{hmap}}$（Eq. 7）和峰值显著性损失 $\mathcal{L}_{\text{peak}}$（Eq. 8），同时攻击密度图的绝对强度与相对显著性。

**$\mathcal{L}_{\text{pert}}$** 是跨范式的感知约束项（Eq. 13）：

$$\mathcal{L}_{\text{pert}} = \beta \cdot \mathcal{L}_{\text{hinge}} + \gamma \cdot \mathcal{L}_{\text{tv}} + \zeta \cdot \mathcal{L}_{\text{freq}} + \kappa \cdot \mathcal{L}_{\text{cam}}$$

- **$\mathcal{L}_{\text{hinge}}$**：幅度约束，控制扰动在 $\epsilon$ 范围内。
- **$\mathcal{L}_{\text{tv}}$**：全变分平滑损失，抑制高频噪声。
- **$\mathcal{L}_{\text{freq}}$**（Eq. 9）：频率域约束，通过 FFT 抑制扰动的高频分量，使其符合自然人群统计的低频特征。
- **$\mathcal{L}_{\text{cam}}$**（Eq. 10）：GradCAM 注意力引导损失，最小化注意力区域之外的扰动，将攻击集中在语义重要区域，增强跨范式可迁移性。

**推理效率**：训练完成后，CrowdGen 仅需**单次前向传播**即可生成对抗样本，无需针对每个输入进行迭代优化，且能在不同架构和数据集之间泛化。

### 补充图表

![[assets/figures/papers/paper_list_l878_https_arxiv_org_abs_2603_24821/figures/002_Figure_2.jpg]]
*Figure 2: (i) Perturbation loss (GradCAM Perturbation & Frequency-Magnitude Reduction) in Sec. 3.3.3, and (ii) Paradigmspecific losses (Density & Logit suppression) in Secs. 3.3.1 and 3.3.2 are proposed for training the perturbation generator*



CrowdGen 框架的核心由三个功能模块构成：扰动生成器、范式特定损失模块和跨范式感知约束模块。整体攻击损失定义为：

$$\mathcal{L}_{\mathrm{attack}} = \underbrace{\mathcal{L}_{\mathrm{model}}}_{\mathrm{paradigm-specific}} + \underbrace{\mathcal{L}_{\mathrm{pert}}}_{\mathrm{cross-paradigm}}$$

其中 $\mathcal{L}_{\mathrm{model}}$ 根据代用模型的架构范式自动选择，$\mathcal{L}_{\mathrm{pert}}$ 则负责跨范式的扰动质量约束。

### 扰动生成器

框架采用一个3级U-Net作为生成器 $G_{\theta}$，将输入RGB图像 $I$ 映射为有界扰动 $\delta = G_{\theta}(I)$，满足 $\|\delta\|_{\infty} \leq \epsilon$。该生成器在推理时仅需单次前向传播即可生成对抗样本，无需迭代优化。

### 范式特定损失

模型损失根据代用模型类型自动切换：

$$\mathcal{L}_{\mathrm{model}} = \begin{cases} \mathcal{L}_{\mathrm{logit}} & \text{for point-regression models } M_p \\ \mathcal{L}_{\mathrm{dmap}} & \text{for density-map models } M_D \end{cases}$$

**对数抑制损失（点回归范式）**：针对点回归模型的高置信度logit进行抑制。训练过程中采用自适应阈值 $\tau(t)$，随时间逐步降低被攻击的高置信度检测数量：

$$\tau(t) = \max\left(\tau_{\min}, \tau_{\max} - \nu \cdot \frac{t}{T_{\max}}\right)$$

该损失根据场景密度自适应组合密集与稀疏两种形式。密集场景下，对高置信度区域 $\mathcal{P}_{\mathrm{high}}$ 的logit进行最小化：

$$\mathcal{L}_{\mathrm{dense}} = -\frac{1}{|\mathcal{P}_{\mathrm{high}}|} \sum_{i \in \mathcal{P}_{\mathrm{high}}} \left[ l_i^{(h)} - \log(1 - s_i^{(h)} + \epsilon) \right]$$

**密度图抑制损失（密度图范式）**：核心假设是有效的密度图攻击必须同时抑制绝对强度（峰值幅度）和相对显著性（峰值突出度）。损失函数同时作用于显著峰值区域 $\mathcal{Q}'$ 和近阈值区域 $\mathcal{Q}^*$：

$$\mathcal{L}_{\mathrm{hmap}} = \frac{1}{|\mathcal{Q}'|} \sum_{(x,y)\in\mathcal{Q}'} \mathcal{D}(x,y) + \frac{\eta_h}{|\mathcal{Q}^*|} \sum_{(x,y)\in\mathcal{Q}^*} \mathcal{D}(x,y)$$

### 跨范式感知约束

扰动损失 $\mathcal{L}_{\mathrm{pert}}$ 由四项约束组合而成，平衡攻击效能与隐蔽性：

$$\mathcal{L}_{pert} = \beta \cdot \mathcal{L}_{\mathrm{hinge}} + \gamma \cdot \mathcal{L}_{\mathrm{tv}} + \zeta \cdot \mathcal{L}_{\mathrm{freq}} + \kappa \cdot \mathcal{L}_{\mathrm{cam}}$$

**频率域约束**：通过抑制扰动的高频分量，使扰动符合自然人群统计的低频特征：

$$\mathcal{L}_{\mathrm{freq}} = \frac{1}{|\Omega|} \sum_{\omega \in \Omega} |\mathcal{F}(\delta)(\omega)|$$

其中 $\mathcal{F}(\delta)(\omega)$ 为扰动 $\delta$ 的傅里叶变换，$\Omega$ 为高频分量集合（排除直流分量）。

**GradCAM注意力引导**：最小化注意力区域之外的扰动，将攻击集中在语义重要区域以增强可迁移性：

$$\mathcal{L}_{\mathrm{cam}} = \frac{1}{HW} \| |\delta| - \delta(\rho) \|_1$$

其中 $\rho$ 为代用模型骨干网络提取的GradCAM注意力图。消融实验表明，在点回归范式下添加 $\mathcal{L}_{\mathrm{cam}}$ 可使MR从45.15%提升至45.61%，同时PSNR达到19.10 dB，实现最优折衷；而在密度图范式下，完整损失组合（含 $\mathcal{L}_{\mathrm{freq}}$ 和 $\mathcal{L}_{\mathrm{cam}}$）使MR达到60.89-60.90%，PSNR约17.47 dB。

### 补充图表

![[assets/figures/papers/paper_list_l878_https_arxiv_org_abs_2603_24821/figures/001_Figure_1.jpg]]
*Figure 1: Localized crowded counting predictions and density maps in clean and adversarial images designed in our work*

![[assets/figures/papers/paper_list_l878_https_arxiv_org_abs_2603_24821/figures/006_Figure_4.jpg]]
*Figure 4: GradCAM response of clean and adversarial images*



## 实验与关键发现

### 核心定量结果

CrowdGen 在密集场景下展现出显著的攻击效能。在 SHHA 数据集上，当使用 FIDTM 作为代用模型时，干净图像的 MAE 为 128.0，而对抗样本的 MAE 飙升至 1013.6，增幅约 **7.9 倍**，同时 PSNR 保持在 18.81 dB，表明攻击在实现高强度计数值破坏的同时维持了较好的视觉隐蔽性。

在跨范式可迁移性方面，CrowdGen 展现出独特的“超可迁移”现象。以 HMoDE 生成的对抗样本为例，其在点回归模型 P2PNet 上的攻击效果反而优于代用模型自身，**迁移比（TR）达到 1.69**，即目标模型上的 MAE 是代用模型的 1.69 倍。这一反直觉现象揭示了密度图范式与点回归范式之间共享的潜在空间存在可被系统性利用的脆弱性。整体而言，在七种主流人群计数模型上的迁移比范围为 0.55 至 1.69，验证了跨范式攻击的广泛有效性。

### 与现有攻击方法的对比

Table 3 汇总了不同攻击方法在 FIDTM 模型上跨密度区域的综合评估。与基于扩散模型的 **DiffAttack**（Chen et al., TPAMI 2024）和针对人群计数的对抗补丁攻击 **PAP**（Liu et al., CCS 2022）相比，CrowdGen 在攻击效能与隐蔽性之间取得了最优平衡：

![[assets/figures/papers/paper_list_l878_https_arxiv_org_abs_2603_24821/figures/007_Table_3.jpg]]
*Table 3: Evaluation of attacks using FIDTM model across density regimes (SHHA dataset), where ↑ indicates the higher the better*

- **DiffAttack** 的 MAE 高达 1591.3，PSNR 仅 10.36 dB，攻击强度虽高但视觉质量严重劣化；
- **PAP** 的 PSNR 为 22.58 dB，隐蔽性最佳，但 MAE 仅 5.40，几乎无攻击效果；
- **CrowdGen** 的 MAE 为 259.76，PSNR 为 19.25 dB——在保持比 PAP 低 3.7 倍 MAE（即攻击更有效）的同时，PSNR 比 DiffAttack 高出 8.9 dB。

这一结果验证了多任务损失设计中感知约束组件的关键作用：频率域约束和 GradCAM 注意力引导使得扰动集中在语义重要区域，避免了对背景的无差别破坏。

### 消融实验：损失函数组合的影响

Table 4 展示了各损失组件对漏检率（MR）和 PSNR 的影响，揭示了不同范式下最优约束组合的显著差异。

![[assets/figures/papers/paper_list_l878_https_arxiv_org_abs_2603_24821/figures/008_Table_4.jpg]]
*Table 4: Impact of combinations of loss functions on MR and PSNR for SHHA dataset*

**密度图范式下**，完整损失组合（$\mathcal{L}_{\mathrm{hmap}}/\mathcal{L}_{\mathrm{peak}} + \mathcal{L}_{\mathrm{hinge}} + \mathcal{L}_{\mathrm{tv}} + \mathcal{L}_{\mathrm{freq}} + \mathcal{L}_{\mathrm{cam}}$）使 MR 达到 **60.89–60.90%**，PSNR 约 17.47 dB。单独添加频率域约束或 GradCAM 注意力引导均可将 MR 提升至约 60%，表明这些感知约束对密度图模型的攻击具有叠加增益效应。

**点回归范式下**，消融结果呈现截然不同的规律。基线配置（$\alpha\mathcal{L}_{\mathrm{logit}} + \beta\mathcal{L}_{\mathrm{hinge}}$）的 MR 为 45.15%，添加 $\mathcal{L}_{\mathrm{cam}}$ 后 MR 提升至 **45.61%** 且 PSNR 达 19.10 dB，达到最佳折衷。然而，进一步引入频率或平滑约束反而**持续降低** MR。这一现象的可能解释是：点回归模型依赖稀疏的头部位置检测，频率约束和平滑约束会抑制扰动中的高频细节，而这些细节恰恰是破坏点定位精度的关键。

### 跨数据集可迁移性

Table 1 和 Table 2 分别展示了 SHHA 和 UCF-QNRF 数据集上的跨模型可迁移性结果。两个数据集上的迁移模式高度一致：以密度图模型为代用生成的对抗样本对点回归模型展现出更强的迁移攻击力，反之亦然。这种跨范式迁移的稳定性表明，CrowdGen 利用的共享潜在空间脆弱性并非特定数据集的偶然现象，而是人群计数模型架构层面的系统性缺陷。

![[assets/figures/papers/paper_list_l878_https_arxiv_org_abs_2603_24821/figures/004_Table_1.jpg]]
*Table 1: Transferability of our designed adversarial examples across crowd counting models (MAE/TR) on the SHHA dataset., where the highest and lowest values are indicated by bold and underline*

![[assets/figures/papers/paper_list_l878_https_arxiv_org_abs_2603_24821/figures/005_Table_2.jpg]]
*Table 2: Transferability of our designed adversarial examples across crowd counting models (MAE/TR) on UCF-QNRF dataset, where the highest and lowest values are indicated by bold and underline*

### 失败模式与局限性

尽管 CrowdGen 在数字域展现出强大的跨范式攻击能力，其仍存在以下局限：

1. **物理世界未验证**：当前所有实验均在数字域进行，对抗样本在物理场景（如监控摄像头拍摄后重新数字化）中的有效性和可迁移性尚未测试。物理域的噪声、光照变化和视角偏移可能显著削弱攻击效果。

2. **代用模型依赖性**：攻击生成器需要针对特定代用模型进行训练。对于架构完全未知的目标模型，迁移性可能无法达到最优——这一结论在 Table 1 和 Table 2 中部分 TR 值低于 1.0 的结果中得到印证（需人工核实具体模型对的 TR 值）。

3. **点回归范式下的约束冲突**：消融实验揭示，频率约束和平滑约束在点回归范式下反而降低攻击强度，说明当前统一的感知约束设计尚未完全适配两种范式的内在差异。



## 定位与知识库关联

### 1. 对抗攻击范式演进中的定位

CrowdGen 在生成式对抗攻击（generation-based attack）与优化型对抗攻击（optimization-based attack）的二分谱系中，明确属于**生成式**路线，但其设计融合了优化型攻击的可迁移性增强策略。理解这一谱系对把握 CrowdGen 的创新边界至关重要：

- **优化型攻击**通过迭代最大化代用模型损失来搜索扰动，典型范式为 $\delta^{*} = \max_{\delta} \mathcal{L}(f_s(T(x+\delta)), y)$，其中 $T$ 为输入变换，$\|\delta\|_{\infty} \le \epsilon$。此类方法包括 **DI²FGSM** (Xie et al., CVPR 2019)、**Admix** (Wang et al., ICCV 2021)、**SVRE** (Xiong et al., CVPR 2022)、**GRA** (Zhu et al., ICCV 2023)、**L2T** (Zhu et al., CVPR 2024) 和 **FIA** (Wang et al., ICCV 2021)。它们的共同瓶颈在于：每次攻击需要数百次梯度反传，且可迁移性高度依赖输入变换设计，无法天然适配人群计数特有的密度图与点回归双范式。

- **生成式攻击**通过训练一个前馈生成器 $\mathcal{G}_{\theta}$ 直接输出对抗样本或扰动，损失函数为 $\mathcal{L}(f_s(\mathcal{G}_{\theta}), y)$。此类方法包括 **DiffAttack** (Chen et al., TPAMI 2024) 和 **GE-AdvGAN** (Zhu et al., SDM 2024)。生成式攻击的优势在于推理时仅需单次前向传播，但现有工作均未考虑人群计数领域的范式差异。

- **针对人群计数的专用攻击**极为稀缺，唯一可比较的工作是 **PAP** (Liu et al., CCS 2022)，其采用对抗补丁（adversarial patch）策略，但仅针对密度图模型，且补丁的物理可见性限制了隐蔽性。

CrowdGen 的定位是将生成式攻击的推理效率与跨范式可迁移性需求结合：它采用 3-level U-Net 生成器，训练时通过多任务损失同时优化范式特定的攻击目标与跨范式的感知约束，推理时单次前向传播即可生成对抗样本。这一设计使其区别于上述所有基线工作。

### 2. 与基线方法的关键差异槽位

CrowdGen 相对于基线方法的核心改进可通过四个“差异槽位”来理解：

| 差异槽位 | 基线方法取值 | CrowdGen 取值 | 证据锚点 |
|---------|------------|-------------|---------|
| 攻击生成范式 | 迭代优化（DI²FGSM 等）或非自适应生成（DiffAttack 等） | 基于 U-Net 的生成器配合多任务损失 | "our framework employs a 3-level U-Net generator $G_{\theta}$ trained with a multi-task loss" |
| 点回归模型攻击损失 | 无（传统攻击不支持点回归输出） | 场景密度自适应的对数抑制损失 $\mathcal{L}_{\mathrm{logit}}$ (Eq.4-6) | "For point-regression models, we employ scene-density-specific high-confidence logit suppression" |
| 密度图模型攻击损失 | 无差别攻击（PAP 等） | 峰值导向的密度图抑制损失 $\mathcal{L}_{\mathrm{hmap}}$ (Eq.7-8)，同时抑制绝对强度与相对显著性 | "we hypothesize that effective density map attacks must target both absolute intensity (peak magnitude) and relative salience (peak prominence)" |
| 感知约束设计 | 仅采用 $L_p$ 范数约束 | 频率域约束 $\mathcal{L}_{\mathrm{freq}}$ + GradCAM 注意力引导 $\mathcal{L}_{\mathrm{cam}}$ + 全变分平滑 $\mathcal{L}_{\mathrm{tv}}$ + $L_2$ 幅度约束 (Eq.9-13) | "$\mathcal{L}_{\mathrm{pert}} = \beta \cdot \mathcal{L}_{\mathrm{hinge}} + \gamma \cdot \mathcal{L}_{\mathrm{tv}} + \zeta \cdot \mathcal{L}_{\mathrm{freq}} + \kappa \cdot \mathcal{L}_{\mathrm{cam}}$" |

其中，**频率域约束**和 **GradCAM 注意力引导**是两个最具原创性的感知约束设计。频率约束通过抑制扰动的高频分量使其符合自然人群统计的低频特征，而 GradCAM 引导则将扰动能量集中在模型语义关注区域，避免在背景区域浪费扰动预算——这两种约束共同构成了跨范式可迁移性的感知基础。

### 3. 适用边界与假设条件

CrowdGen 的有效性建立在以下关键假设之上，这些假设同时定义了其适用边界：

1. **共享潜在空间假设**：CrowdGen 的核心洞察是“不同人群计数模型共享的骨干网络学到相似的潜在空间”。这意味着攻击的可迁移性依赖于代用模型与目标模型在特征提取层面的结构相似性。对于使用完全不同骨干架构（如纯 Transformer vs. 纯 CNN）的模型，可迁移性可能下降——尽管论文在七种模型上的跨架构实验已部分验证了该假设的鲁棒性。

2. **代用模型可访问假设**：攻击生成需要针对特定代用模型进行训练。对于完全未知的模型，无法保证最优迁移性。论文通过跨模型迁移实验（Table 1, Table 2）展示了从密度图模型到点回归模型的“超迁移性”（Transfer Ratio 最高达 1.69），但这仍然是在已知目标模型的前提下评估的。

3. **数字域验证假设**：所有实验均在数字域进行，尚未在物理世界中测试攻击的有效性和可迁移性。物理攻击引入的光照变化、视角偏移、打印-拍摄失真等因素可能显著影响攻击效果。

4. **场景密度依赖假设**：对数抑制损失中的自适应阈值 $\tau(t) = \max(\tau_{\min}, \tau_{\max} - \nu \cdot t/T_{\max})$ 依赖于场景密度分类（密集 vs. 稀疏）。对于密度极度不均匀的场景，该二分策略可能存在边界效应。

### 4. 局限性与开放问题

**已识别的局限性**：

- **物理域未验证**：攻击仅在数字域验证，物理世界中的可迁移性和鲁棒性未知。这是对抗攻击研究中的普遍局限，但对于人群计数这类可能部署在物理监控场景中的系统，物理攻击验证尤为重要。

- **代用模型依赖性**：虽然跨范式可迁移性表现优异，但攻击生成仍需针对特定代用模型训练。对于完全未知的模型架构，无法保证攻击效果。

- **隐蔽性-攻击性权衡**：消融实验（Table 4）揭示了密度图范式与点回归范式对感知约束的不同响应——密度图模型受益于完整的约束组合（MR: 60.89-60.90%, PSNR: 17.46-17.47 dB），而点回归模型添加频率或平滑约束反而降低攻击强度（MR 从 45.15% 降至更低），仅 GradCAM 引导能实现最佳折衷（MR: 45.61%, PSNR: 19.10 dB）。这表明不存在“一刀切”的最优约束组合。

**开放问题**：

1. **物理攻击可复现性**：跨范式对抗攻击现象在物理世界中能在多大程度上复现？物理域中的频率约束和 GradCAM 引导是否仍然有效？

2. **范式无关的防御机制**：如何设计不依赖特定范式的防御机制以增强人群计数模型的鲁棒性？CrowdGen 的成功反过来说明现有防御可能过于范式特定。

3. **更广泛架构的可迁移性**：CrowdGen 在七种模型上验证了可迁移性，但这些模型均基于 CNN 骨干。对于基于 Vision Transformer 的人群计数模型（如 CCViT），共享潜在空间的假设是否仍然成立？

4. **攻击的定向性**：当前攻击目标是最大化计数误差（增加 MAE/MR）。是否存在定向攻击的可能，即诱导模型输出特定的错误计数值？这在对抗场景中可能具有更隐蔽的威胁。



## 原文 PDF

![[paperPDFs/CVPR_2026/Generative_Adversarial_Perturbations_with_Cross_paradigm_Transferability_on_Localized_Crowd_Counting.pdf]]
