---
title: Diffusion-Based Native Adversarial Synthesis for Enhanced Medical Segmentation Generalization
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Diffusion_Based_Native_Adversarial_Synthesis_for_Enhanced_Medical_Segmentation_Generalization.pdf
project_link: null
code_link: null
aliases:
- AM
- DBNASEMSG
tags:
- CVPR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 对抗性挖掘器（Adversariality Miner）通过重新选取扩散模型的初始噪声，将采样先验偏移至高对抗性区域，从而在不变的原始采样轨迹下生成固有对抗性样本。
primary_logic: 合成数据泛化增益可分解为生成质量（梯度方向夹角余弦）与对抗性（梯度范数）的乘积；只有当对抗性来自模型难以拟合的流形内样本（固有对抗性）时，才能有效提升泛化，而攻击产生的非流形扰动（人工对抗性）则适得其反。
claims:
- 泛化增益与合成数据梯度范数和夹角余弦的乘积成正比（Eq.4），对抗性（范数）是主导因素。
- 扩散模型生成的合成数据中，对抗性分布高度偏斜，仅有约7.62%的高对抗性样本贡献了约66.7%的总泛化增益（Tab.1）。
- 攻击式对抗引导（AdvDiffuser, P2P, Diff-PGD）虽然提升对抗性，但导致泛化增益下降，因为其生成的样本偏离真实流形，增加了生成质量偏差（Fig.3, Fig.5）。
- 所提出的对抗性挖掘器在不改变扩散模型和采样过程的情况下，通过重选初始噪声放大固有对抗性，使泛化增益显著提升，且合成样本保持在流形内（Fig.3, Fig.5, Tab.2,5）。
---

# Diffusion-Based Native Adversarial Synthesis for Enhanced Medical Segmentation Generalization

> [!tip] 核心洞察
> 合成数据泛化增益可分解为生成质量（梯度方向夹角余弦）与对抗性（梯度范数）的乘积；只有当对抗性来自模型难以拟合的流形内样本（固有对抗性）时，才能有效提升泛化，而攻击产生的非流形扰动（人工对抗性）则适得其反。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于扩散的固有对抗合成增强医学分割泛化 |
| 英文题名 | Diffusion-Based Native Adversarial Synthesis for Enhanced Medical Segmentation Generalization |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Zhang_Diffusion-Based_Native_Adversarial_Synthesis_for_Enhanced_Medical_Segmentation_Generalization_CVPR_2026_paper.html) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | Adversariality Miner |
| Dataset | Polyps, Synapse, Polyps→EndoScene |

> [!tip] 效果简介
> - Polyps (in-domain, nnU-Net with SegDiff) 上，DSC Gain (∆DSC↑) +5.88 vs 0 (Baseline without synth) (+5.88)。
> - Synapse (in-domain, nnU-Net with DiffBoost) 上，DSC Gain (∆DSC↑) +9.12 vs 0 (+9.12)。
> - Polyps→EndoScene (cross-device, nnU-Net with SiameseDiff) 上，DSC Gain (∆DSC↑) +10.25 vs 0 (+10.25)。

## 概要

**核心问题**：基于扩散模型（Diffusion Model, DM）的合成数据已成为提升医学图像分割泛化能力的关键手段，但现有方法面临一个被忽视的瓶颈——扩散模型生成的合成数据中，高对抗性（adversariality）样本极度稀疏，占比不足10%，而这些稀有样本却贡献了超过六成的泛化增益。与此同时，攻击式对抗引导（Adversarial Guidance, AG）虽能提升样本对抗性，却引入偏离真实流形的扰动，反而损害下游泛化能力。根本瓶颈在于缺乏有效手段，在保持流形内生成的前提下放大**固有对抗性**（native adversariality）。

**核心洞察**：本文将合成数据的泛化增益分解为两个可量化的因子——生成质量（合成-真实梯度方向夹角余弦）与对抗性（合成梯度范数）的乘积。这一分解揭示：只有当对抗性来自模型难以拟合的流形内样本（即固有对抗性）时，才能有效提升泛化；而攻击产生的非流形扰动（人工对抗性）则适得其反。

**方法定位**：本文提出**对抗性挖掘器**（Adversariality Miner），一种轻量级即插即用模块。其核心创新在于**不修改扩散模型权重、不改变采样轨迹**，仅通过重新选取扩散模型的初始噪声，将采样先验偏移至高对抗性区域，从而在保持流形内生成的前提下放大固有对抗性。该方法可无缝集成至现有医学扩散模型（如SegDiff、FairDiff、DiffBoost等），无需重新训练基础模型。

**主要结果**：
- 在息肉分割（Polyps）域内场景下，集成对抗性挖掘器带来 **+5.88 DSC** 的泛化增益。
- 在跨设备偏移（Polyps→EndoScene）场景下，增益达到 **+10.25 DSC**。
- 在跨模态偏移（CT↔MRI）场景下同样取得显著且一致的提升。
- 消融实验表明，随着合成预算增大，该方法持续放大高对抗性合成，避免冗余，保持一致的泛化增益，而基准方法的增益则迅速衰减。



### 医学图像分割中的数据稀缺与合成增强

医学图像分割模型的性能高度依赖大规模、高质量标注数据，然而在临床场景中，获取像素级标注的成本极高，且数据常受限于单一设备、单一模态，导致模型在未见目标域上的泛化能力不足。近年来，扩散模型（Diffusion Models, DMs）在医学图像合成领域展现出强大的生成能力，研究者开始利用预训练的医学扩散模型合成额外训练数据，以增强下游分割模型的泛化性能。典型的范式是 **Mask-to-Image（M2I）**：先通过条件掩码采样器生成分割掩码，再以掩码为条件通过扩散模型合成对应医学图像，从而构建合成数据集 $\mathcal{U}_{\mathrm{syn}}$ 用于扩充真实训练集。

### 核心瓶颈：高对抗性样本极度稀疏

尽管合成数据增强在实践中有效，但并非所有合成样本对泛化的贡献均等。本文通过将泛化增益 $\mathcal{G}_{\vartheta}(\mathcal{U}_{\mathrm{syn}})$ 定义为引入合成数据后模型在真实未见数据上分割损失的降低量，并利用一阶泰勒展开推导出关键分解：

$$\mathcal{G}_{\vartheta}(\mathcal{U}_{\mathrm{syn}}) \propto \|\nabla_{\vartheta} \ell_{\mathrm{seg}}(\mathcal{U}_{\mathrm{syn}}; \vartheta)\|_2 \cos \zeta$$

其中 $\|\nabla_{\vartheta} \ell_{\mathrm{seg}}(\mathcal{U}_{\mathrm{syn}}; \vartheta)\|_2$ 为合成数据损失梯度的范数（衡量**对抗性**，即样本对当前模型的难度），$\cos \zeta$ 为合成梯度与真实梯度之间的夹角余弦（衡量**生成质量**，即合成数据与真实流形的一致性）。该分解揭示：泛化增益取决于对抗性与生成质量的乘积。

然而，对多个主流医学扩散模型（SegDiff、FairDiff 等）合成数据的实证分析表明，对抗性分布高度偏斜：**仅约 7.62% 的高对抗性样本贡献了约 66.7% 的总泛化增益**（见表 1 和图 1(a)）。绝大多数合成样本的对抗性极低，对提升模型鲁棒性几乎无贡献，形成“冗余合成”问题。

### 现有方案缺口：攻击式对抗引导的“人工对抗性”陷阱

为提升合成数据的对抗性，已有工作借鉴对抗攻击思想，在扩散采样过程中引入偏好项（preference term）以引导生成高损失样本，代表方法包括 **AdvDiffuser**（Chen et al., ICCV 2023）、**P2P**（Medghalchi et al., CVPR 2025）和 **Diff-PGD**（Xue et al., NeurIPS 2023）。这类**攻击式对抗引导（Adversarial Guidance, AG）** 虽能有效提升样本的对抗性指标，却导致下游泛化增益**不升反降**（见图 3(b)）。

根本原因在于 AG 引入的是**人工对抗性（artificial adversariality）**：通过偏离原始采样轨迹的方式增加扰动，使合成样本脱离真实数据流形。t-SNE 可视化（图 5）显示 AG 样本在特征空间中偏离真实流形，FID 指标恶化，即 $\cos \zeta$ 显著下降。尽管 $\|\nabla_{\vartheta} \ell_{\mathrm{seg}}\|$ 增大，但生成质量的退化抵消甚至超过了对抗性的增益（见图 4(a) 的残差可视化，AG 扰动为非语义的不可察觉噪声）。

### 本文动机：挖掘流形内的“固有对抗性”

上述分析引出核心研究问题：**如何在保持合成样本位于真实流形内的前提下，放大其对抗性？** 本文将这种源自流形内、由模型拟合困难本身驱动的对抗性定义为**固有对抗性（native adversariality）**。

与 AG 修改采样轨迹不同，本文提出在**不改变扩散模型和采样过程**的条件下，通过**重新选取扩散模型的初始噪声**来偏移采样先验，使采样轨迹天然地导向高对抗性区域。这一思路的核心洞察在于：初始噪声 $\mathbf{\hat{x}}_T$ 的选择决定了去噪轨迹的起点，而扩散模型固有的采样轨迹本身已覆盖流形内不同对抗性水平的区域；只需将采样先验从标准高斯 $\mathcal{N}(\mathbf{0}, \mathbf{I})$ 偏移至高对抗性噪声区域，即可在不引入流形外扰动的情况下放大固有对抗性（见图 4(b)）。



## 核心方法与创新机理

### 问题定位：合成数据泛化的对抗性瓶颈

现有扩散模型在医学图像分割的数据增强中面临一个被忽视的结构性瓶颈：**合成数据中真正驱动泛化增益的高对抗性样本极度稀疏**。如 Figure 1(a) 所示，在多个医学扩散模型（SegDiff、FairDiff 等）生成的合成数据中，对抗性分布高度偏斜——仅有约 7.62% 的高对抗性样本贡献了约 66.7% 的总泛化增益（Table 1）。这意味着绝大多数合成样本对下游分割模型的泛化贡献微乎其微，构成了合成数据利用效率的根本性限制。

对此，已有的对抗引导（Adversarial Guidance, AG）方法——如 **AdvDiffuser**（Chen et al., ICCV 2023）、**P2P**（Medghalchi et al., CVPR 2025）和 **Diff-PGD**（Xue et al., NeurIPS 2023）——试图通过在采样过程中注入对抗信号来提升合成数据的难度。然而，这些方法引入的扰动偏离了真实数据流形，产生了所谓的“人工对抗性”（artificial adversariality），反而损害了下游泛化能力（Figure 3(b), Figure 5）。根本原因在于：**缺乏一种在保持流形内生成的前提下放大“固有对抗性”（native adversariality）的有效机制**。

### 核心洞察：泛化增益的几何分解

本文的核心理论贡献在于将合成数据的泛化增益分解为两个可独立操控的因子。通过一阶泰勒展开，合成数据 $\mathcal{U}_{\mathrm{syn}}$ 带来的泛化增益可表示为：

$$\mathcal{G}_{\vartheta}(\mathcal{U}_{\mathrm{syn}}) \propto \left\| \nabla_{\vartheta} \ell_{\mathrm{seg}}(\mathcal{U}_{\mathrm{syn}}; \vartheta) \right\|_{2} \cos \zeta$$

其中，**梯度范数** $\|\nabla_{\vartheta} \ell_{\mathrm{seg}}\|_2$ 量化了合成数据的对抗性（即对下游模型的难度），而**夹角余弦** $\cos\zeta$ 衡量合成梯度与真实梯度方向的一致性（即生成质量）。这一分解揭示了关键洞察：泛化增益的提升可以通过放大对抗性来实现，但前提是该对抗性必须来自流形内的固有样本——否则 $\cos\zeta$ 的下降将抵消范数增长带来的收益。

Figure 2 给出了该分解的几何解释：泛化增益正比于合成梯度在真实梯度方向上的投影长度。AG 方法虽然增大了梯度范数，却因偏离流形而减小了投影夹角，导致净增益下降。这为“如何在不损害生成质量的前提下放大对抗性”提供了明确的理论指引。

### 关键创新：对抗性挖掘器（Adversariality Miner）

基于上述洞察，本文提出了**对抗性挖掘器**（Adversariality Miner）$\mathcal{M}_\xi$，其设计遵循一个简洁而关键的原则：**不修改扩散模型的采样轨迹，仅通过重新选取初始噪声来偏移采样先验**。具体而言，该方法在以下四个关键维度上区别于现有方案：

| 设计维度 | baseline 做法 | 本文方案 | 创新本质 |
|---------|-------------|---------|---------|
| **初始噪声分布** | 标准高斯 $\mathcal{N}(\mathbf{0},\mathbf{I})$ | 偏移高斯 $\mathcal{N}^r(\Delta_\mu, \mathbf{I}+\Delta_\Sigma)$，由 Miner 预测 | 将采样先验偏移至高对抗性区域 |
| **对抗信号注入** | 无（纯随机采样） | 基于冻结下游模型的分割损失优化初始噪声，配合时序 stop-gradient | 在采样起点而非轨迹中途注入对抗性 |
| **采样轨迹** | 完整 DDIM 逆过程 $T \to 0$ | 相同的 DDIM 过程，仅初始噪声被重选 | 保持流形内生成，不引入额外引导项 |
| **Miner 训练目标** | 不适用 | 带裁剪的对抗性最大化 + KL 散度正则化 | 在对抗性增益与分布对齐间取得平衡 |

Miner 的核心工作机制如下：首先从标准高斯中采样候选初始噪声 $\hat{\mathbf{x}}_T$，计算其在冻结扩散模型下的初始去噪得分 $S_\phi^{\mathrm{Init}}$（通过 stop-gradient 阻断梯度回传至扩散模型）；然后 Miner 根据该得分预测噪声分布的偏移量 $(\Delta_\mu, \Delta_\Sigma)$，构造偏移分布 $\mathcal{N}^r$；最后从 $\mathcal{N}^r$ 中重选初始噪声 $\hat{\mathbf{x}}_T^r$，以标准 DDIM 过程完成采样。整个过程可形式化为：

$$(\Delta_{\mu}, \Delta_{\Sigma}) \leftarrow \mathcal{M}_{\xi}(S_{\phi}^{\mathrm{Init}}), \quad S_{\phi}^{\mathrm{Init}} = \mathrm{sg}(s_{\phi}(\widehat{\mathbf{x}}_{T}, T \mid \widehat{\mathbf{y}}_{s}, \cdot))$$

$$\hat{\mathbf{x}}_T^r \sim \mathcal{N}^r(\Delta_\mu, \mathbf{I} + \Delta_\Sigma)$$

Miner 的训练目标在最大化对抗性的同时通过 KL 散度约束噪声偏移，防止偏离先验过远导致样本退化：

$$\boldsymbol{\xi}^{*} = \underset{\boldsymbol{\xi}}{\arg\max} \, \mathbb{E}\left[ \min(\kappa_{\mathrm{up}}, \ell_{\mathrm{seg}}(f_{\vartheta}(\hat{\mathbf{x}}_s^r), \hat{\mathbf{y}}_s)) - \beta \cdot \mathrm{KL}(\mathcal{N}^r \parallel \mathcal{N}(\mathbf{0}, \mathbf{I})) \right]$$

其中 $\kappa_{\mathrm{up}}$ 为对抗性上界（裁剪项），防止个别极端样本主导优化；$\beta$ 控制分布对齐强度。

### 与攻击式对抗引导的本质区别

Figure 4 直观展示了人工对抗性与固有对抗性的差异。AG 方法生成的对抗样本与基础样本在视觉上几乎无法区分，其残差主要表现为不可感知的非语义扰动——这些扰动虽能提升对抗性，却将样本推离了真实流形（Figure 5 的 t-SNE 可视化证实了这一点，AG 样本的 FID 显著劣化）。相比之下，对抗性挖掘器通过重选初始噪声，在相同的条件掩码和扩散模型下生成了语义上明显不同的样本——这些样本仍然是流形内的合理医学图像，但对下游分割模型构成了更大的挑战。

Figure 3 的定量对比进一步验证了这一差异：AG 方法虽然提升了对抗性分布的上尾，却导致测试 DSC 和泛化增益下降；而本文方法同时实现了更高的对抗性和更大的 DSC 增益，且合成样本保持在流形内。

### 方法优势总结

对抗性挖掘器的核心优势可归纳为三点：

1. **即插即用**：Miner 作为轻量级模块，无需修改或重新训练扩散模型，可直接集成到现有的 Mask-to-Image 医学扩散模型中（如 SegDiff、FairDiff、DiffBoost、SiameseDiff 等），如 Table 2 所示。

2. **保持流形内生成**：通过仅偏移初始噪声而不修改采样轨迹，确保合成样本始终位于扩散模型所刻画的真实数据流形上，从根本上避免了 AG 方法中的人工对抗性问题。

3. **计算高效**：通过将优化时的 DDIM 步数截断至 10 步，可在几乎不损失泛化增益的情况下大幅降低显存和时间开销（Figure 9(c)），使得方法在实际部署中具有可行性。



本文提出的对抗性挖掘器（Adversariality Miner）是一个轻量级即插即用模块，其核心目标是在不修改或重新训练扩散模型（DM）的前提下，通过重选初始噪声来放大合成数据的固有对抗性（native adversariality），从而提升下游分割模型的泛化能力。整体pipeline由五个协同模块构成，遵循“掩码采样→噪声重选→图像生成→对抗性优化”的闭环流程。

**工作流概述**：首先，条件掩码采样器 $q_\omega$ 从真实掩码出发，通过随机翻转和缩放操作生成多样化的条件分割掩码 $\hat{\mathbf{y}}_s$（§4.1）。随后，对抗性挖掘器 $\mathcal{M}_\xi$ 接收冻结扩散模型在初始时刻的去噪得分 $S_\phi^{\mathrm{Init}}$，预测噪声先验的偏移量 $(\Delta_\mu, \Delta_\Sigma)$，将标准高斯先验 $\mathcal{N}(\mathbf{0},\mathbf{I})$ 偏移为 $\mathcal{N}^r(\Delta_\mu, \mathbf{I}+\Delta_\Sigma)$，并从中重选初始噪声 $\hat{\mathbf{x}}_T^r$（Eq.9）。该噪声随后进入冻结扩散模型（如 SegDiff、FairDiff 等），在条件掩码和文本提示的引导下，通过标准的 DDIM 去噪过程生成合成图像 $\hat{\mathbf{x}}_s^r$——整个过程不引入额外的偏好项，也不改变采样轨迹（§3.3）。最后，冻结的下游分割器 $f_\vartheta$（nnU-Net 或 SwinUNETR）对合成图像计算分割损失 $\ell_{\mathrm{seg}}$，该损失同时作为对抗性信号反馈给挖掘器进行优化。

**模块间的因果链路**：挖掘器的训练目标（Eq.10）是在 KL 散度正则化的约束下最大化合成样本的对抗性——具体而言，最大化裁剪后的分割损失 $\min(\kappa_{\mathrm{up}}, \ell_{\mathrm{seg}})$，同时通过 $\beta \cdot \mathrm{KL}(\mathcal{N}^r \parallel \mathcal{N}(\mathbf{0},\mathbf{I}))$ 约束重选噪声不过度偏离原始先验，从而保证合成样本保持在数据流形内。这一设计直接回应了核心洞察：泛化增益 $\mathcal{G}_\vartheta$ 正比于合成梯度范数（对抗性）与梯度方向夹角余弦（生成质量）的乘积（Eq.4），而攻击式对抗引导（AG）方法虽然提升了梯度范数，却因引入偏离流形的扰动而恶化了夹角余弦项，导致泛化增益反而下降（Fig.3, Fig.5）。

**与基线方法的本质区别**：相较于 **AdvDiffuser**（Chen et al., ICCV 2023）、**P2P**（Medghalchi et al., CVPR 2025）和 **Diff-PGD**（Xue et al., NeurIPS 2023）等对抗引导方法在采样过程中注入偏好梯度来“攻击”生成过程，对抗性挖掘器将干预点前移至初始噪声的选择阶段，使得后续采样完全遵循原始扩散模型的流形内轨迹。这一设计使得合成样本既具备高对抗性（梯度范数大），又保持高生成质量（夹角余弦接近1），从而在息肉分割基准上实现 +5.88 ∆DSC 的即插即用增益（Tab.2），在跨设备泛化场景（Polyps→EndoScene）中增益达 +10.25 ∆DSC（Tab.5）。

### 补充图表

![[assets/figures/papers/paper_list_l856_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_Diffusion_Based/figures/002_Figure_2.jpg]]
*Figure 2: Geometric view of generalization gain, which is proportional to the projection of loss gradients from synthetic data*



### 泛化增益的解耦：对抗性与生成质量

合成数据对下游分割模型泛化能力的贡献可被严格分解为两个正交因子。给定一个在真实训练集 $\mathcal{U}_{\mathrm{train}}$ 上预训练的下游分割模型 $f_\vartheta$，合成数据集 $\mathcal{U}_{\mathrm{syn}}$ 带来的泛化增益 $\mathcal{G}_{\vartheta}(\mathcal{U}_{\mathrm{syn}})$ 定义为：合成数据训练后，模型在未见真实集 $\mathcal{U}_{\mathrm{real}}$ 上分割损失的下降量。通过对损失函数进行一阶泰勒展开，该增益可近似为合成梯度在真实梯度方向上的投影：

$$\mathcal{G}_{\vartheta}(\mathcal{U}_{\mathrm{syn}}) \propto \left\| \nabla_{\vartheta} \ell_{\mathrm{seg}}(\mathcal{U}_{\mathrm{syn}}; \vartheta) \right\|_2 \cos \zeta$$

其中，$\nabla_{\vartheta} \ell_{\mathrm{seg}}(\mathcal{U}_{\mathrm{syn}}; \vartheta)$ 是合成数据上的分割损失梯度，$\zeta$ 为合成梯度与真实梯度之间的夹角。这一分解将泛化增益拆解为两个可独立分析的因素：

- **梯度范数** $\|\nabla_{\vartheta} \ell_{\mathrm{seg}}(\mathcal{U}_{\mathrm{syn}}; \vartheta)\|_2$：量化合成数据对当前模型的“难度”，即**对抗性**（adversariality）。范数越大，表明合成样本越能暴露模型的决策边界弱点。
- **夹角余弦** $\cos \zeta$：度量合成梯度与真实梯度方向的一致性，反映合成数据的**生成质量**——即合成样本是否位于真实数据流形之上。

这一分解揭示了核心洞察：**仅当对抗性来源于流形内的固有困难样本时，才能有效提升泛化；若对抗性由偏离流形的人工扰动引入，则 $\cos \zeta$ 下降，泛化增益反而受损。**

### 对抗性的度量与分布偏斜

基于上述分解，论文将单个合成样本 $\hat{\mathbf{x}}_s$ 的对抗性操作化定义为：在冻结的下游分割模型 $f_\vartheta$ 下，该样本的分割损失值：

$$\ell_{\mathrm{seg}}(f_\vartheta(\hat{\mathbf{x}}_s), \hat{\mathbf{y}}_s)$$

按此度量，可按阈值 $\tau$ 筛选高对抗性子集：

$$\mathcal{U}_{\mathrm{syn}}^{\tau} := \{ (\hat{\mathbf{x}}_s, \hat{\mathbf{y}}_s) \in \mathcal{U}_{\mathrm{syn}} \mid \ell_{\mathrm{seg}}(f_\vartheta(\hat{\mathbf{x}}_s), \hat{\mathbf{y}}_s) > \tau \}$$

实证分析揭示了一个关键瓶颈：扩散模型生成的合成数据中，对抗性分布高度偏斜。如 Table 1 所示，仅约 **7.62%** 的高对抗性样本贡献了约 **66.7%** 的总泛化增益，而绝大多数样本的对抗性极低，对泛化贡献微弱。这意味着，标准的随机采样策略大量浪费了生成预算于低效样本上。

### 对抗性挖掘器：通过噪声先验偏移放大固有对抗性

为解决上述瓶颈，论文提出**对抗性挖掘器**（Adversariality Miner）$\mathcal{M}_\xi$，其核心思想是：**不修改扩散模型的采样轨迹，仅通过重新选取初始噪声，将采样先验偏移至高对抗性区域，从而在保持流形内生成的前提下放大固有对抗性。**

#### 模块架构与工作流程

对抗性挖掘器是一个轻量级即插即用模块，其输入输出如下：

1. **输入**：从标准高斯分布 $\mathcal{N}(\mathbf{0}, \mathbf{I})$ 采样的初始噪声 $\hat{\mathbf{x}}_T$，以及条件掩码 $\hat{\mathbf{y}}_s$。
2. **初始得分提取**：计算冻结扩散模型在 $T$ 时刻的去噪得分，并通过 stop-gradient 操作阻断梯度回传：
   $$S_{\phi}^{\mathrm{Init}} = \mathrm{sg}\left(s_{\phi}(\hat{\mathbf{x}}_T, T \mid \hat{\mathbf{y}}_s, \cdot)\right)$$
3. **偏移预测**：挖掘器 $\mathcal{M}_\xi$ 根据初始得分预测噪声先验的偏移量 $(\Delta_\mu, \Delta_\Sigma)$：
   $$(\Delta_\mu, \Delta_\Sigma) \leftarrow \mathcal{M}_\xi(S_{\phi}^{\mathrm{Init}})$$
4. **噪声重选**：从偏移后的高斯分布中重新采样初始噪声：
   $$\hat{\mathbf{x}}_T^r \sim \mathcal{N}^r(\Delta_\mu, \mathbf{I} + \Delta_\Sigma)$$
5. **标准采样**：使用重选的初始噪声 $\hat{\mathbf{x}}_T^r$，通过**未修改的 DDIM 反向过程**生成最终图像。整个过程不引入额外的引导项，不改变采样轨迹。

#### 挖掘器训练目标

挖掘器 $\mathcal{M}_\xi$ 的参数 $\xi$ 通过最大化以下目标函数进行优化：

$$\xi^{*} = \arg\max_{\xi} \mathbb{E}\left[ \min(\kappa_{\mathrm{up}}, \ell_{\mathrm{seg}}(f_\vartheta(\hat{\mathbf{x}}_s^r), \hat{\mathbf{y}}_s)) - \beta \cdot \mathrm{KL}(\mathcal{N}^r \parallel \mathcal{N}(\mathbf{0}, \mathbf{I})) \right]$$

目标函数由两项构成：

- **裁剪对抗性最大化项** $\min(\kappa_{\mathrm{up}}, \ell_{\mathrm{seg}})$：鼓励挖掘器选取使下游分割模型产生高损失的初始噪声，但通过上界 $\kappa_{\mathrm{up}}$ 进行裁剪，防止对抗性过度放大导致样本退化。
- **KL 散度正则化项** $\beta \cdot \mathrm{KL}(\mathcal{N}^r \parallel \mathcal{N}(\mathbf{0}, \mathbf{I}))$：约束偏移后的噪声分布 $\mathcal{N}^r$ 不偏离标准高斯先验过远，从而确保重选的噪声仍处于扩散模型的有效采样区域内，维持流形内生成。

#### 关键设计选择

| 设计槽位 | 基准方法（随机采样） | 对抗性挖掘器 |
|---------|-------------------|------------|
| 初始噪声分布 | 标准高斯 $\mathcal{N}(\mathbf{0}, \mathbf{I})$ | 偏移高斯 $\mathcal{N}^r(\Delta_\mu, \mathbf{I}+\Delta_\Sigma)$ |
| 对抗性信号注入 | 无 | 基于冻结下游模型的 $\ell_{\mathrm{seg}}$ 优化初始噪声，配合时序 stop-gradient |
| 采样轨迹 | 完整 DDIM 过程 $T \to 0$ | 相同的 DDIM 过程，无额外引导或轨迹修改 |
| 训练目标 | 不适用 | 裁剪对抗性最大化 + KL 正则化 |

### 与对抗性引导的本质区别

对抗性引导（Adversarial Guidance, AG）方法（如 **AdvDiffuser** (Chen et al., ICCV 2023)、**P2P** (Medghalchi et al., CVPR 2025)、**Diff-PGD** (Xue et al., NeurIPS 2023)）通过在采样过程中注入偏好项 $\exp(\lambda \ell_{\mathrm{seg}})$ 来提升对抗性。然而，这种训练无关的偏好注入难以精确校准，导致生成的样本携带非语义的人工扰动，偏离真实流形（如 Figure 5 的 t-SNE 可视化所示，AG 样本散布于真实流形之外）。其后果是：虽然对抗性（梯度范数）上升，但 $\cos \zeta$ 显著下降，最终泛化增益反而低于低对抗性的随机采样基线（Figure 3）。

![[assets/figures/papers/paper_list_l856_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_Diffusion_Based/figures/004_Figure_3.jpg]]
*Figure 3: (a) Adversariality distribution of the synthetic sets produced by AG and our method on Polyps. (b) Test DSC (↑) during synthetic-data training, together with the final generalization gain*

![[assets/figures/papers/paper_list_l856_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_Diffusion_Based/figures/006_Figure_5.jpg]]
*Figure 5: t-SNE visualization of synthetic data (red) from each method overlaid on the real manifold (blue), estimated from all available data in the dataset. FID (↓) measures generation fidelity*

相比之下，对抗性挖掘器通过**在采样开始前重选初始噪声**，将搜索空间限制在扩散模型固有的采样轨迹族内，从而天然保证生成样本位于流形之上。这实现了对抗性与生成质量的解耦优化：对抗性由噪声先验偏移控制，生成质量由扩散模型自身保证。

### 补充图表

![[assets/figures/papers/paper_list_l856_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_Diffusion_Based/figures/005_Figure_4.jpg]]
*Figure 4: Artificial vs. Native adversariality. (a) AG increases adversariality but produces visually indistinguishable outputs*



## 实验与关键发现

### 核心实验设置

实验在多种医学图像分割基准上展开，覆盖域内泛化、采集设备偏移和模态偏移三类场景。下游分割模型采用 **nnU-Net** 和 **SwinUNETR**，基础扩散模型包括 **SegDiff**、**FairDiff**、**DiffBoost** 和 **SiameseDiff** 等主流医学扩散模型。所有主要实验均使用 3 个随机种子报告均值和标准差。对抗性挖掘器 $\mathcal{M}_\xi$ 作为轻量即插即用模块接入，不修改或重训练基础扩散模型，DDIM 采样步数固定为 50 步。

### 主实验结果

#### 即插即用泛化增益

Table 2 展示了对抗性挖掘器集成到多种 SOTA 医学扩散模型后的泛化增益。以仅使用真实训练集的 nnU-Net 作为基线（∆DSC = 0），在 **Polyps** 数据集上，SegDiff + Ours 带来 **+5.88** 的 DSC 增益；在 **Synapse** 数据集上，DiffBoost + Ours 带来 **+9.12** 的 DSC 增益。所有集成场景下，对抗性挖掘器均一致地产生正向泛化增益，验证了方法的即插即用特性。

![[assets/figures/papers/paper_list_l856_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_Diffusion_Based/figures/007_Table_2.jpg]]
*Table 2: Integration of our method into SOTA medical DMs. †: Baseline trained only on*

#### 跨设备泛化

Table 3 报告了采集设备偏移下的泛化结果：在 Polyps 上训练，在 **EndoScene**、**ColonDB** 和 **ETIS** 三个未见设备上测试。SiameseDiff + Ours 在 EndoScene 上取得 **+10.25** 的 DSC 增益，显著优于仅使用真实数据的基线。这一结果说明固有对抗性样本能够有效覆盖设备间不可预见的分布偏移。

![[assets/figures/papers/paper_list_l856_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_Diffusion_Based/figures/008_Table_3.jpg]]
*Table 3: Evaluation under acquisition device shift: trained on Polyps [2, 25], tested on unseen EndoScene [58], ColonDB [56], and ETIS [50]. †denotes absolute performance; others report gains ∆ over Baseline as mean±std*

#### 模态偏移泛化

Table 4 报告了 CT ↔ MRI 双向模态偏移的结果（MMWHS 数据集）。对抗性挖掘器在两个方向上均产生正向增益，证明固有对抗性不局限于单一模态或设备，对更剧烈的分布偏移同样有效。

![[assets/figures/papers/paper_list_l856_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_Diffusion_Based/figures/009_Table_4.jpg]]
*Table 4: Evaluation under modality shift on MMWHS [72]. Arrows denote the “training→testing” direction. †denotes absolute performance; others report gains ∆ over Baseline as mean±std*

#### 与现有方法的对比

Table 5 将对抗性挖掘器与多种扩散增强方法及对抗攻击方法进行了系统对比。对抗性引导方法（**AdvDiffuser**，Chen et al., ICCV 2023；**P2P**，Medghalchi et al., CVPR 2025；**Diff-PGD**，Xue et al., NeurIPS 2023）虽然在提升对抗性指标上有一定效果，但在下游泛化增益上表现不佳甚至为负（见 Fig. 3b）。其他扩散增强方法如 **DiffAug**（Sastry et al., NeurIPS 2024）、**SDEdit**（Meng et al., ICLR 2022）、**InitNo**（Guo et al., CVPR 2024）、**NoiseCtrl**（Dai et al., CVPR 2025）和 **Inpainting**（Hu et al., arXiv 2025）的泛化增益均低于本文方法。对抗性挖掘器在多个基准上取得最优或次优结果，且保持合成样本在真实流形内（Fig. 5）。

![[assets/figures/papers/paper_list_l856_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_Diffusion_Based/figures/014_Table_5.jpg]]
*Table 5: Comparative evaluation. All results are reported as performance gains over the Baseline in Tab. 2. Best and second-best results are highlighted in red and green, respectively*

### 消融研究

#### 对抗性分布与增益的关系

Table 1 通过对抗性阈值划分揭示了合成数据泛化增益的偏斜本质：仅 **7.62%** 的高对抗性样本（$\ell_{\mathrm{seg}} > \tau$）贡献了约 **66.7%** 的总泛化增益，每样本增益从低对抗性子集的 $4.48 \times 10^{-3}$ 单调递增至高对抗性子集的 $45.20 \times 10^{-3}$。这直接验证了 Eq. (4) 中对抗性（梯度范数）作为泛化增益主导因素的论断。

![[assets/figures/papers/paper_list_l856_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_Diffusion_Based/figures/003_Table_1.jpg]]
*Table 1: Generalization gain*

#### 人工对抗性与固有对抗性的对比

Fig. 3 和 Fig. 4 揭示了对抗性引导方法的根本缺陷：AG 方法虽能提升对抗性指标，但生成的样本与基样本在视觉上几乎不可区分，差异主要来自非语义的不可感知扰动（Fig. 4a）。这些扰动使样本偏离真实流形，导致生成质量项 $\cos \zeta$ 下降，最终泛化增益不升反降。Fig. 5 的 t-SNE 可视化进一步证实：AG 样本（红色）明显偏离真实数据流形（蓝色），FID 升高；而对抗性挖掘器通过重选初始噪声，使合成样本保持在流形内，FID 与基方法相当。

#### KL 正则化系数 β

Fig. 8 展示了 KL 正则化强度 β 的影响。**β = 0.001** 在对抗性增益与分布对齐之间取得最佳平衡：β 过小导致噪声偏离先验 $\mathcal{N}(\mathbf{0},\mathbf{I})$，产生退化样本；β 过大则抑制对抗效应，泛化增益下降。

#### 对抗性上界 κ_up

Fig. 10 分析了对抗性上界 κ_up 的影响。**κ_up = 0.5** 在实践中提供稳定且显著的增益：过高的上界会导致样本质量下降（FID 升高）和增益饱和。论文建议以 κ_up = 0.5 作为初始默认值。

#### DDIM 截断步数

Fig. 9(c) 展示了优化时 DDIM 步数截断的影响。将步数截断至 **10 步**，可在几乎不损失泛化增益（∆DSC↑）的情况下大幅降低显存和时间开销；超过 25 步后性能反而下降。Fig. 9(a)(b) 进一步说明对抗性信号主要集中在去噪早期（高时间步长），后期去噪对对抗性贡献有限。

![[assets/figures/papers/paper_list_l856_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_Diffusion_Based/figures/013_Figure_9.jpg]]
*Figure 9: (a) Variation of adversariality*

#### 合成预算与增益饱和

Fig. 7 展示了合成预算 N_s 与泛化增益的关系。随着合成预算增大，对抗性挖掘器通过持续放大高对抗性合成，避免冗余，保持一致的泛化增益；而基准方法（随机采样）的增益迅速衰减。这表明对抗性挖掘器有效解决了合成数据冗余问题。

![[assets/figures/papers/paper_list_l856_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_Diffusion_Based/figures/010_Figure_7.jpg]]
*Figure 7: Synthetic budget*

### 失败模式与局限性

1. **掩码空间的对抗性缺失**：当前方法仅挖掘图像域中的对抗性，但 Eq. (4) 表明分割掩码同样影响泛化增益。扩展到掩码空间实现图像-掩码联合优化是未来的方向。

2. **对基础扩散模型质量的依赖**：方法假设扩散模型能生成高质量、流形内的样本。若基础模型质量差（如训练不充分、数据覆盖不足），对抗性增强的效果可能下降，甚至放大模型本身的偏差。

3. **对抗性增益的上限未知**：对抗性增益如何随下游模型容量和训练数据规模变化，目前缺乏理论刻画，实践中需要针对具体场景调参。

### 需要人工验证的要点

- Table 5 中部分对比方法（如 NoiseCtrl、Inpainting）的引用信息在分析 JSON 中标注为预印本，建议核实其最终出版状态。
- Fig. 7 和 Fig. 10 的具体数值（如饱和点、FID 数值）需从原图读取，本文仅给出趋势性结论。

### 补充图表

![[assets/figures/papers/paper_list_l856_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_Diffusion_Based/figures/001_Figure_1.jpg]]
*Figure 1: (a) Adversariality distribution of fixed-size synthetic sets sampled from medical DMs [32, 41, 70] across multiple benchmarks, measured under downstream segmentation models (cf. § 2.3). (b) Overview of the proposed adversariality miner, which reselects high-potential initial noise from a frozen DM to enhance synthetic adversariality and downstream generalization*



## 定位与知识库关联

### 问题定位：合成数据的泛化增益从何而来

本文的核心贡献在于对**扩散模型合成数据用于下游分割泛化**这一范式进行了因果解耦。此前的工作——无论是基于扩散模型的增强方法如 **DiffAug**（Sastry et al., NeurIPS 2024）、**SDEdit**（Meng et al., ICLR 2022）、**InitNo**（Guo et al., CVPR 2024）、**NoiseCtrl**（Dai et al., CVPR 2025），还是基于修补的 **Inpainting**（Hu et al., arXiv 2025）——普遍将合成数据的价值归因于“视觉保真度”或“分布覆盖”，却未追问一个更根本的问题：**合成数据中究竟是什么在驱动泛化增益？**

本文通过一阶泰勒展开将泛化增益 $\mathcal{G}_\vartheta(\mathcal{U}_{\mathrm{syn}})$ 分解为两个可量化因子的乘积：

$$\mathcal{G}_\vartheta(\mathcal{U}_{\mathrm{syn}}) \propto \|\nabla_\vartheta \ell_{\mathrm{seg}}(\mathcal{U}_{\mathrm{syn}}; \vartheta)\|_2 \cos \zeta$$

其中梯度范数 $\|\nabla_\vartheta \ell_{\mathrm{seg}}\|_2$ 刻画**对抗性**（合成样本对下游模型的“难度”），夹角余弦 $\cos\zeta$ 刻画**生成质量**（合成梯度与真实梯度方向的一致性）。这一分解揭示了一个被先前工作忽略的事实：合成数据的泛化价值由对抗性与生成质量**共同决定**，且经验证据表明，对抗性是主导因素——仅占总量约 7.62% 的高对抗性样本贡献了约 66.7% 的总泛化增益（Table 1）。

### 方法谱系中的位置：对抗性引导 vs. 对抗性挖掘

在方法谱系上，本文与两类工作形成直接对话：

**第一类是攻击式对抗引导（Adversarial Guidance, AG）方法**，包括 **AdvDiffuser**（Chen et al., ICCV 2023）、**P2P**（Medghalchi et al., CVPR 2025）和 **Diff-PGD**（Xue et al., NeurIPS 2023）。这些方法通过在扩散采样过程中注入偏好项（preference term）来提升合成样本的对抗性，可视为对式（6）中倾斜分布 $q_\phi^{\mathrm{adv}}$ 的训练无关实例化。然而，本文通过系统实验揭示了一个关键缺陷：AG 方法虽然能有效提升对抗性，但其提升的是**人工对抗性**（artificial adversariality）——通过偏离真实流形的不可感知扰动实现的“作弊式”难度提升。如图 4(a) 所示，AG 生成的样本与基础样本在视觉上几乎不可区分，差异仅在于非语义的扰动残差；t-SNE 可视化（Figure 5）进一步证实这些样本偏离了真实数据流形，FID 显著劣化。其后果是：尽管对抗性数值上升，但 $\cos\zeta$ 项（生成质量）的恶化抵消甚至超过了范数项的增益，导致下游泛化增益**不升反降**（Figure 3(b)）。

**第二类是扩散增强方法**，如 **DiffAug**、**SDEdit**、**InitNo** 等。这些方法专注于提升合成数据的视觉质量或多样性，却未显式建模对抗性。从本文的解耦框架来看，它们主要优化的是 $\cos\zeta$ 项，而对 $\|\nabla_\vartheta \ell_{\mathrm{seg}}\|_2$ 项缺乏主动控制，导致合成数据中高对抗性样本极度稀疏（Figure 1(a)），大量合成预算被低效消耗。

本文提出的 **Adversariality Miner** 在谱系中占据了一个独特位置：它既不修改扩散模型的采样轨迹（区别于 AG 方法），也不依赖对生成质量的额外约束（区别于增强方法），而是通过**重新选取初始噪声**，将采样先验从标准高斯 $\mathcal{N}(\mathbf{0}, \mathbf{I})$ 偏移至高对抗性区域 $\mathcal{N}^r(\Delta_\mu, \mathbf{I}+\Delta_\Sigma)$，从而在**不改变去噪过程**的前提下放大**固有对抗性**（native adversariality）。这种方法的关键洞察在于：对抗性应当来自模型难以拟合的流形内样本，而非攻击产生的流形外扰动。Figure 4(b) 和 Figure 5 表明，Adversariality Miner 生成的样本在保持流形内位置（FID 与基础方法相当）的同时，显著提升了对抗性分布的上尾密度。

### 适用边界与假设条件

本方法的有效性建立在以下前提之上：

1. **扩散模型能够生成高质量、流形内的样本**。若基础扩散模型本身质量较差（如训练数据不足、条件控制失效），则即使通过噪声重选也无法保证合成样本保持在流形内，对抗性增强的效果将大打折扣。这一假设在论文使用的医学分割扩散模型（SegDiff、FairDiff、DiffBoost、SiameseDiff）上成立，但在更弱的基础模型上需要手动验证。

2. **下游分割模型 $f_\vartheta$ 能够提供可靠的对抗性信号**。Adversariality Miner 的训练依赖于冻结的下游模型（如 nnU-Net 或 SwinUNETR）计算分割损失 $\ell_{\mathrm{seg}}$ 作为对抗性度量。若下游模型本身在目标域上表现极差（例如在极端域偏移下），则其损失信号可能无法有效区分高/低对抗性样本，从而削弱挖掘器的优化效果。

3. **对抗性仅来源于图像空间**。当前方法仅挖掘图像域中的对抗性，而分割掩码同样影响对抗性（Eq. (4) 中的梯度同时依赖于输入图像和标签）。将对抗性挖掘扩展至掩码空间是论文明确指出的未来方向。

### 关键局限与开放问题

**局限一：掩码空间的对抗性未被利用。** 如论文自身所指出的，Eq. (4) 中泛化增益同时依赖于合成图像和合成掩码，但 Adversariality Miner 仅优化图像生成的初始噪声，掩码仍由条件掩码采样器 $q_\omega$ 通过随机翻转和缩放真实掩码生成。这意味着掩码空间的对抗性潜力尚未被充分挖掘。如何在图像-掩码联合空间中实现端到端的固有对抗性放大，是一个开放且有价值的方向。

**局限二：对基础扩散模型质量的依赖。** 当扩散模型无法保证流形内生成时（例如在数据极度稀缺的医学场景中），如何可靠地放大固有对抗性？一个可能的思路是将对抗性挖掘与生成质量约束联合优化，但这会引入额外的复杂度权衡。

**局限三：对抗性增益的上限未探明。** 论文在多个基准上展示了显著的泛化增益（Polyps 上 +5.88 ∆DSC，Synapse 上 +9.12 ∆DSC），但对抗性增益的理论上限如何随下游模型容量、训练数据规模和任务复杂度变化？Figure 7 显示随着合成预算增大，基准方法的增益迅速衰减而本文方法保持稳定，但这是否意味着存在一个与模型容量相关的饱和点？这一问题对于将该方法推广至更大规模场景具有实际指导意义。

**开放问题一：跨任务普适性。** 本文聚焦于医学图像分割，但固有对抗性的概念及其与泛化增益的因果关系是否适用于其他任务（如目标检测、图像分类）和其他领域（如自然图像、遥感图像）？这需要进一步的理论和实证验证。

**开放问题二：对抗性挖掘器的架构设计空间。** 当前 Adversariality Miner 采用轻量级设计，仅根据初始去噪得分预测噪声分布的偏移量。是否存在更优的架构选择（如引入条件掩码信息、时序建模）？消融实验中 DDIM 截断步数的最优值（10 步）和 KL 正则化系数的最优值（$\beta=0.001$）是否在不同任务和数据规模下保持稳定？这些问题指向了方法工程化落地的实际考量。

**开放问题三：与对抗训练的深层关联。** 本文的固有对抗性概念与传统对抗训练中的“对抗样本”有何本质区别？两者都涉及提升模型在困难样本上的表现，但本文强调困难必须来自流形内的自然变异而非人工扰动。这一区分是否能为对抗训练社区提供新的理论视角，值得深入探讨。



## 原文 PDF

![[paperPDFs/CVPR_2026/Diffusion_Based_Native_Adversarial_Synthesis_for_Enhanced_Medical_Segmentation_Generalization.pdf]]
