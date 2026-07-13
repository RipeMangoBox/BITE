---
title: "HalluGen: Synthesizing Realistic and Controllable Hallucinations for Evaluating Image Restoration"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/HalluGen_Synthesizing_Realistic_and_Controllable_Hallucinations_for_Evaluating_Image_Restoration.pdf
project_link: null
code_link: null
aliases:
- HalluGen
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: HalluGen通过扩散后验采样结合可控制的梯度扰动，自动生成带有真值掩码的真实感幻觉。
primary_logic: 利用扩散模型的流形先验与精心设计的梯度上升信号，可以在保持视觉真实性的同时，按需合成两类幻觉（内在/外在），从而为系统化的幻觉基准测试和检测器训练提供可扩展的数据基础。
claims:
- 现有指标（PSNR、SSIM、LPIPS）对幻觉预测的评分高于语义正确但模糊的图像，暴露其对感知锐度的偏好。
- 专业标注者之间的幻觉区域一致性极低（Cohen's κ=0.30），远低于可接受阈值。
- HalluGen生成的幻觉使分割IoU从0.86骤降至0.36，同时维持较低的FID，证明其兼具真实感与语义错误。
- 提出的SHAFE指标将幻觉检测AUC提升约0.25，并减少24个百分点的假阴性。
---

# HalluGen: Synthesizing Realistic and Controllable Hallucinations for Evaluating Image Restoration

> [!tip] 核心洞察
> 利用扩散模型的流形先验与精心设计的梯度上升信号，可以在保持视觉真实性的同时，按需合成两类幻觉（内在/外在），从而为系统化的幻觉基准测试和检测器训练提供可扩展的数据基础。

| 字段 | 内容 |
|------|------|
| 中文题名 | HalluGen：合成真实可控的幻觉用于评估图像复原 |
| 英文题名 | HalluGen: Synthesizing Realistic and Controllable Hallucinations for Evaluating Image Restoration |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.03345) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | HalluGen |
| Dataset | HCP脑MRI（低场增强模拟）, HalluGen数据集（内在/外在）, 幻觉指标基准（SHAFE vs 传统指标） |

> [!tip] 效果简介
> - HCP脑MRI（低场增强模拟） 上，分割IoU（幻觉区域内） 0.363 (HalluGen+MedSAM) vs 0.861 (DPS) (-0.498)。
> - HalluGen数据集（内在/外在） 上，AUC-ROC（无参考幻觉检测器） 0.91 (内在) / 0.77 (外在) vs 0.51 (LPIPS内在) / 0.50 (LPIPS外在) (+0.40 / +0.27)。
> - 幻觉指标基准（SHAFE vs 传统指标） 上，AUC-ROC 0.82 (SHAFE-ResNet50内在) vs 0.52 (PSNR内在) (+0.30)。

## 概要

图像复原模型在高风险场景中会产生语义错误但视觉逼真的**幻觉**，然而评估这些幻觉面临一个闭环困境：可靠的幻觉分析依赖标注数据，但人工标注不仅成本高昂，且专家间一致性极低（Cohen's κ = 0.30），远低于可接受阈值；同时，现有图像质量指标（PSNR、SSIM、LPIPS）对幻觉不敏感——它们对幻觉预测的评分反而高于语义正确但模糊的图像（Figure 2），暴露了其对感知锐度的系统性偏好。

针对这一瓶颈，本文提出 **HalluGen**，一种基于扩散后验采样的可控幻觉生成框架。其核心思路是：利用扩散模型的流形先验，在逆向扩散过程中对选定区域施加精心设计的梯度扰动，从而按需合成**内在幻觉**（违反测量一致性）和**外在幻觉**（保持测量一致性但语义错误），并自动获得精确的真值掩码。HalluGen 使幻觉的**类型、空间位置、强度和粒度**均可独立调节，为系统化的幻觉基准测试和检测器训练提供了可扩展的数据基础。

在方法谱系上，HalluGen 以 **Diffusion Posterior Sampling (DPS)**（Chung et al., 2022）为基础采样引擎，关键改动在于将全局数据一致性梯度下降替换为**掩码区域梯度上升**，并引入熵基补丁选择、幻觉验证模块（HVM）和流形正则化早期停止等组件，确保生成样本兼具真实感与分类合规性。基于此，本文进一步构建了包含 4,350 张标注图像的 HalluGen 数据集，并提出 **SHAFE** 指标——一种结合低通滤波与加权软基聚合的无参考幻觉检测度量。

核心实验结果确立了方法的有效性：HalluGen 在保持低 FID（与 DPS 相当）的同时，使分割 IoU 从 0.86 骤降至 0.36（Table 1），证明其生成幻觉兼具真实感与语义破坏力；SHAFE 指标将幻觉检测 AUC 提升约 0.25–0.30，并减少 24 个百分点的假阴性（Table 3）；仅用 HalluGen 数据训练的无参考检测器在内在/外在幻觉上分别达到 0.91/0.77 的 AUC（Table 4），验证了合成数据的训练价值。

### 图像复原中的幻觉问题

图像复原旨在从退化的观测 $y$ 中恢复真值图像 $x$，其正向退化过程可表述为 $y = \mathcal{A}(x) + n$，其中 $\mathcal{A}$ 为前向退化算子，$n$ 为加性噪声。然而，当复原模型在信息不足的区域“填补”出看似合理但语义错误的内容时，便产生了**幻觉**——这些生成内容在视觉上高度逼真，却缺乏真值依据。

幻觉对安全关键领域构成严重威胁。在医学影像中，模型可能在低场MRI重建时凭空生成肿瘤特征；在工业检测中，可能“修复”出并不存在的产品缺陷。这类错误直接危及诊断与决策的可靠性。

### 幻觉评估的闭环困境

当前对图像复原幻觉的评估陷入了一个根本性的闭环：

**标注困境**：可靠的幻觉分析需要标注数据来识别哪些区域被错误生成。然而，幻觉区域的标注高度依赖专家判断，且标注者之间的一致性极低——专业标注者在幻觉区域的标注上仅达到 Cohen's κ = 0.30，远低于可接受阈值。这使得人工标注既昂贵又不可靠。

**指标困境**：现有图像质量指标（PSNR、SSIM、LPIPS）对幻觉不敏感，甚至表现出**锐度偏好**——它们倾向于给包含幻觉的预测图像打出高于语义正确但略微模糊图像的分数（Figure 2）。这一现象在MVTec AD工业检测和BraTS脑肿瘤分割两个领域均得到验证，暴露了传统指标将感知锐度置于语义正确性之上的系统性偏差。

这两个困境相互强化：缺乏可靠标注数据使得无法开发幻觉敏感的评估指标，而指标的不敏感又使得无法自动筛选或验证标注质量，形成恶性循环。

### 现有方法的缺口

当前应对幻觉的策略存在明显局限：

- **人工标注**：成本高昂、一致性差，无法规模化。
- **传统全参考指标**（PSNR、SSIM）：对局部语义错误不敏感，主要衡量全局信号保真度。
- **感知指标**（LPIPS、DISTS）：虽能捕捉感知差异，但对锐度的偏好使其在幻觉检测中表现不佳，AUC仅约0.50–0.52，接近随机猜测。
- **无参考检测器**：缺乏大规模、带有真值掩码的幻觉训练数据，无法有效训练。

核心缺口在于：**缺乏一种可扩展的方法来生成带有自动真值标注的真实感幻觉数据**，以支撑系统化的基准测试和检测器训练。

### 本文动机与核心思路

本文提出**HalluGen**框架，旨在打破上述闭环。其核心洞察是：扩散模型学习到的流形先验蕴含了自然图像的分布知识，通过在扩散后验采样过程中引入**可控制的梯度扰动**，可以在保持视觉真实性的同时，按需合成特定类型的幻觉，并自动获得精确的像素级真值掩码。

具体而言，HalluGen将幻觉分为两类（内在/外在），通过梯度上升信号在选定区域破坏或扭曲数据一致性，从而生成可验证的幻觉样本。这一思路使得大规模幻觉数据集的构建成为可能，为后续的指标基准测试和检测器训练提供了数据基础。

## 核心方法与创新机理

### 闭环困境与突破路径

图像复原中的幻觉评估长期陷入一个循环依赖：可靠的幻觉分析需要标注数据，但人工标注不仅昂贵，而且专家间一致性极低（Cohen's κ = 0.30，远低于可接受阈值）；与此同时，现有图像质量指标（PSNR、SSIM、LPIPS）对感知锐度的偏好使其对幻觉不敏感——**Figure 2** 显示，这些指标对幻觉预测的评分反而高于语义正确但略微模糊的图像。HalluGen 的核心创新在于打破这一闭环：通过扩散后验采样结合可控梯度扰动，自动生成带有真值掩码的真实感幻觉，从而为系统化的幻觉基准测试和检测器训练提供可扩展的数据基础。

### 关键机制：梯度上升 + 流形先验

HalluGen 以 **Diffusion Posterior Sampling (DPS)**（Chung et al., 2022）为基础采样引擎，在以下几个关键维度上进行了创新性改造：

**1. 数据一致性梯度的方向翻转**

DPS 的标准更新步骤通过全局梯度下降使重建逼近测量 $y$（式 5），以增强数据一致性。HalluGen 的核心操作是在选定掩码 $m$ 内**反转梯度方向**——从梯度下降切换为梯度上升，从而在局部区域主动破坏测量一致性，生成内在幻觉（式 6）。对于外在幻觉，则保持全局一致性约束，同时在像素空间和特征空间对掩码区域施加梯度上升，产生语义偏差但不违反测量一致性（式 7）。这种“梯度上升 + 梯度下降”的双向调度机制是 HalluGen 区别于所有现有扩散逆求解器的根本差异。

**2. 初始化与区域插值策略**

不同于 DPS 从高斯噪声开始完整逆扩散过程，HalluGen 支持从预计算的非幻觉基线 $x_{\text{base}}$ 在中间时间步 $t_{\text{skip}}$ 启动，并在逆向每一步对掩码外区域进行插值，将幻觉严格限制在补丁内出现。这一设计使得幻觉生成与真实背景的融合更加自然，同时避免了全局语义的意外漂移。

**3. 流形正则化与早期停止**

在逆向时间步 $t_{\text{stop}}$ 之后，HalluGen 将所有上升权重置零，仅保留去噪步骤，让扩散先验平滑补丁边界。这一“早期停止”策略利用扩散模型的流形先验作为隐式正则化器，确保生成结果在视觉上保持真实感，而非产生突兀的人工痕迹。

### 辅助模块：自动化与验证

HalluGen 还集成了两个关键辅助模块以提升自动化程度和生成质量：

- **熵基补丁选择**：利用香农熵在无标注条件下自动选取信息丰富的区域作为幻觉注入位置，避免落在背景或均匀区域（式 10）。消融实验（**Table 5**）表明，去除该模块会降低内在幻觉的偏差量。
- **幻觉验证模块 (HVM)**：在扩散终步计算掩码区域内的 Cohen's d，拒绝不符合分类定义的样本并重新生成（式 8、9）。HVM 使内在幻觉的测量空间和图像空间误差分别增加约 7% 和 20%，确保生成样本严格满足分类定义。

### 创新总结

HalluGen 的本质创新在于将扩散模型的流形先验与精心设计的梯度上升信号相结合，在保持视觉真实性的同时按需合成两类幻觉。其 changed slots 可归纳为：**梯度方向从全局下降到掩码内上升**、**初始化从全噪声到中间时间步插值启动**、**引入早期停止实现流形正则化**。这三个维度的协同作用使得 HalluGen 能够以可控的方式生成兼具真实感与语义错误的图像，从而为幻觉评估提供了前所未有的数据基础。

HalluGen 的核心设计围绕一个闭环困境展开：可靠的幻觉评估需要标注数据，但人工标注不可靠（Cohen's κ=0.30）且昂贵，而现有图像质量指标又对幻觉不敏感（Figure 2）。HalluGen 通过**可控幻觉合成**打破这一循环，其整体流程可分为四个串联模块：熵基补丁选择、内在/外在幻觉生成分支、幻觉验证模块（HVM）、以及流形正则化与早期停止。

### 输入输出流

系统输入为真值图像 $x_{gt}$、观测 $y$（经退化算子 $\mathcal{A}$ 和噪声 $n$ 产生，$y = \mathcal{A}(x_{gt}) + n$），以及一个预训练扩散模型作为流形先验。输出为幻觉图像 $\hat{x}$ 及其对应的真值二值掩码 $m$，二者构成自动标注的幻觉样本。

### 模块关系与 Pipeline

**熵基补丁选择**：在无标注条件下，利用香农熵 $H(p) = -\sum_i p_i \log p_i$ 自动选取信息丰富的区域作为幻觉注入位置，避免落在背景或均匀区（Section 3.3, Eq 10）。补丁尺寸随机抽取自 16–24 像素，未通过熵或背景比例阈值的补丁被拒绝并重采样。

**内在/外在幻觉生成分支**：在扩散后验采样（DPS）框架（Chung et al., 2022）的基础上，HalluGen 对数据一致性梯度方向进行关键改造。标准 DPS 对所有像素施加梯度下降以逼近测量 $y$（Equation 5）。HalluGen 则在选定掩码 $m$ 内施加**梯度上升**以破坏一致性，生成内在幻觉（Equation 6）；对于外在幻觉，保持全局测量一致性，同时在像素空间和特征空间对掩码区域施加梯度上升，产生语义偏差但不违反测量约束（Equation 7）。

**幻觉验证模块（HVM）**：在扩散逆向过程的终步，计算掩码区域内的 Cohen's d 效应量，拒绝不符合内在/外在分类定义的样本并重新生成（Equations 8, 9）。消融实验表明，HVM 使内在幻觉的测量空间和图像空间误差分别增加约 7% 和 20%，确保生成样本严格满足分类定义（Table 5）。

**流形正则化与早期停止**：在逆向时间步 $t_{stop}$ 之后，将所有梯度上升权重置零，仅保留去噪步骤，让扩散先验平滑边界以维持整体真实感（Section 3.3, Section 6.1）。初始化方面，可从高斯噪声开始完整逆扩散过程，也可从预计算的非幻觉基线 $x_{base}$ 在中间时间步 $t_{skip}$ 启动，并在逆向每一步对掩码外区域进行插值，以限制幻觉仅在补丁内出现（Section 6.1, Algorithm 1/2）。

### 下游验证闭环

HalluGen 生成的幻觉数据直接支撑两个下游任务：（1）**无参考幻觉检测器训练**——以预测图像和测量图像为输入，经低通滤波后由 ResNet50 等简单 CNN 分类（Figure 13），在合成数据上训练即可在真实预测上达到 AUC 0.91（内在）/ 0.77（外在）（Table 4）；（2）**幻觉感知指标 SHAFE 开发**——利用软基聚合补丁余弦距离，通过温度控制的加权机制突出稀疏的局部偏差（Equation 11），将幻觉检测 AUC 从传统指标的 0.52 提升至 0.82（Table 3）。

![[assets/figures/papers/paper_list_l753_https_arxiv_org_abs_2512_03345/figures/020_Figure_13.jpg]]
*Figure 13: Network architecture of reference-free hallucination detector. Prediction and measurement images are fed into the model, applied low-pass filter to remove high-frequency noise and then classified using a simple CNN architecture such as ResNet50*

### 补充图表

![[assets/figures/papers/paper_list_l753_https_arxiv_org_abs_2512_03345/figures/001_Figure_1.jpg]]
*Figure 1: Circular dependency in hallucination evaluation and our proposed HalluGen solution. Top: Reliable hallucination analysis requires labeled data, but obtaining labels demands expert annotation with high disagreement. Bottom: HalluGen breaks this loop by generating controllable hallucinations with automatic labels, enabling systematic benchmarking, and perceptual studies across domains*

### 3.1 幻觉的形式化定义

图像复原任务可统一建模为逆问题：观测图像 $y$ 由真值 $x$ 经前向退化算子 $\mathcal{A}$ 并叠加噪声 $n$ 产生：

$$y = \mathcal{A}(x) + n \quad \text{(Eq. 1)}$$

基于此框架，HalluGen 将幻觉按测量一致性分为两类：

- **内在幻觉 (Intrinsic Hallucination)**：重建 $\hat{x}$ 违反测量一致性，即 $\mathcal{A}(\hat{x}) \neq \mathcal{A}(x_{gt})$（Eq. 2）。此类幻觉在测量空间即可检测，表现为重建与观测之间的数据一致性被破坏。
- **外在幻觉 (Extrinsic Hallucination)**：重建满足测量一致性 $\mathcal{A}(\hat{x}) = \mathcal{A}(x_{gt})$，但逆映射结果不同：$\mathcal{A}^{-1}(\mathcal{A}(\hat{x})) \neq \mathcal{A}^{-1}(\mathcal{A}(x_{gt}))$（Eq. 3）。此类幻觉在测量空间不可见，仅在图像空间呈现语义偏差，检测难度更高。

### 3.2 扩散后验采样基础

HalluGen 以 **Diffusion Posterior Sampling (DPS)**（Chung et al., 2022）为采样引擎。DPS 在逆向扩散的每一步中，将数据一致性梯度下降引入更新过程：

$$x_{t-1} = \mu_{\theta}(x_t, t) - \lambda_t \nabla_{x_t} \| y - \mathcal{A}(\hat{x}_0(x_t)) \|^2 + \sigma_t \epsilon \quad \text{(Eq. 5)}$$

其中 $\mu_{\theta}$ 为预训练扩散模型的去噪均值，$\hat{x}_0(x_t)$ 为从当前噪声状态 $x_t$ 估计的干净图像，$\lambda_t$ 控制梯度步长。该更新通过全局梯度下降使重建逼近测量 $y$，从而保证数据一致性——这正是 DPS 作为非幻觉参考重建的基础。

### 3.3 核心模块：可控幻觉生成

HalluGen 的核心创新在于将 DPS 的全局梯度下降改造为**空间选择性梯度扰动**，在保持整体真实感的同时注入可控制的幻觉。

#### 3.3.1 空间掩码与补丁选择

HalluGen 在补丁级别操作，采样二值掩码 $m \in \{0,1\}^{H \times W}$ 定义幻觉注入区域。为避免在背景或均匀区域生成弱幻觉，采用**熵基补丁选择模块**：利用香农熵自动选取信息丰富的区域：

$$H(p) = -\sum_i p_i \log p_i \quad \text{(Eq. 10)}$$

其中 $p$ 为补丁内归一化强度直方图。未通过熵阈值或背景比例阈值的补丁将被拒绝并重新采样，补丁尺寸在 16–24 像素间随机抽取以匹配典型幻觉范围。

#### 3.3.2 内在幻觉生成

对于内在幻觉，在掩码区域内施加梯度上升以破坏数据一致性，掩码外区域保持梯度下降：

$$x_{t-1} = \mu_{\theta}(x_t, t) - \lambda_t \nabla_{x_t} \| (1-m) \odot (y - \mathcal{A}(\hat{x}_0)) \|^2 + \gamma_t \nabla_{x_t} \| m \odot (y - \mathcal{A}(\hat{x}_0)) \|^2 \quad \text{(Eq. 6)}$$

其中 $\gamma_t$ 为梯度上升强度，$\odot$ 表示逐元素乘法。该公式实现了“推离一致性”与“保持一致性”的空间解耦：掩码外区域受扩散先验和梯度下降双重约束维持真实感，掩码内区域通过梯度上升主动偏离测量值。

#### 3.3.3 外在幻觉生成

外在幻觉需保持全局测量一致性，同时在像素空间和语义特征空间产生偏差。HalluGen 在全局梯度下降基础上，对掩码区域施加像素空间和特征空间的双重梯度上升：

$$x_{t-1} = \mu_{\theta}(x_t, t) - \lambda_t \nabla_{x_t} \| y - \mathcal{A}(\hat{x}_0) \|^2 + \gamma_{1,t} \nabla_{x_t} \| m \odot (\hat{x}_0 - x_{gt}) \|^2 + \gamma_{2,t} \nabla_{x_t} \| m \odot (F(\hat{x}_0) - F(x_{gt})) \|^2 \quad \text{(Eq. 7)}$$

其中 $F(\cdot)$ 为预训练视觉编码器提取的多层浅层特征，$\gamma_{1,t}$ 和 $\gamma_{2,t}$ 分别控制像素空间和特征空间的上升强度。特征损失的引入使幻觉在语义层面偏离真值，同时全局数据一致性项确保测量空间误差保持低位。

#### 3.3.4 幻觉验证模块 (HVM)

为确保生成样本严格符合分类定义，在扩散终步对掩码区域计算 Cohen's d 效应量：

- 内在幻觉验证：测量空间误差需显著高于 DPS 基线（Eq. 8）
- 外在幻觉验证：测量空间误差需接近 DPS 基线，同时图像空间误差显著增大（Eq. 9）

不满足条件的样本被拒绝并重新生成。消融实验（Table 5）表明，HVM 使内在幻觉的测量空间和图像空间误差分别增加约 7% 和 20%，确保生成质量。

#### 3.3.5 流形正则化与早期停止

在逆向时间步 $t_{stop}$ 之后，将所有梯度上升权重置零，仅保留去噪步骤。扩散先验在最后阶段平滑补丁边界并维持整体流形一致性，避免梯度上升导致的视觉伪影。此外，HalluGen 支持从预计算的非幻觉基线 $x_{base}$ 在中间时间步 $t_{skip}$ 启动，并在逆向每一步对掩码外区域进行插值，进一步限制幻觉仅在补丁内出现。

### 3.4 SHAFE 幻觉评估指标

SHAFE 通过补丁级特征差异的软基聚合实现无参考幻觉检测。其计算流程为：

1. **低通滤波**：对输入图像对施加低通滤波，抑制高频噪声并突出结构内容
2. **多层特征提取**：通过预训练视觉编码器（如 ResNet50 或 DINOv3）提取浅层特征，计算补丁级余弦距离 $\delta_{\cos,i}$
3. **温度控制软基聚合**：

$$\mathrm{SHAFE} = \sum_i w_i \delta_{\cos,i}, \quad w_i = \frac{\exp(\delta_{\cos,i}/\tau)}{\sum_j \exp(\delta_{\cos,j}/\tau)} \quad \text{(Eq. 11)}$$

温度参数 $\tau$ 控制聚合的锐度：小 $\tau$ 近似最大池化，突出稀疏的局部偏差；大 $\tau$ 平滑权重分布。消融实验（Table 6）表明，低通滤波与加权软基聚合的组合使 AUC 从 0.52 提升至 0.78，证明抑制高频噪声和自适应空间加权的互补性。特征层选择实验（Table 7）进一步表明，浅层特征组合比单层或深层特征获得更高 AUC，深层特征因 ImageNet 预训练的语义偏差而降低对幻觉的敏感度。

## 实验与关键发现

### 核心实验设计

HalluGen的实验验证围绕三个层次展开：（1）生成样本的真实感与语义偏差的定量验证；（2）幻觉分类定义的合规性检验；（3）下游幻觉检测基准的构建与评估。数据集基于1,450张健康成人大脑MRI构建，经HalluGen生成4,350张带真值掩码的标注图像，内在/外在类别与补丁数量（1-3个）均衡分布，幻觉空间位置均匀覆盖四个象限以确保解剖多样性。

#### 真实感与语义偏差的分离验证

Table 1的核心结论是：HalluGen成功解耦了感知真实感与语义正确性。以**DPS**（Chung et al., 2022）作为非幻觉参考重建，HalluGen+MedSAM的FID为0.41，与DPS的0.32接近，表明生成样本在分布层面保持真实感。然而，幻觉区域内的分割IoU从0.861骤降至0.363（降幅约50个百分点），且该降幅在不同特征提取器（MedSAM、SAM、UNet）间一致，证明语义偏差并非特定模型过拟合所致，而是幻觉注入的系统性效果。

这一“低FID、低IoU”的模式是整篇论文最关键的定量证据——它直接回应了Figure 2揭示的核心矛盾：现有指标（PSNR、SSIM、LPIPS）对幻觉预测的评分高于语义正确但模糊的图像。HalluGen生成的样本恰好填补了这一评估盲区：它们视觉真实但语义错误，传统指标无法有效区分。

#### 幻觉分类合规性验证

Table 2通过掩码区域内的均方误差验证生成样本是否严格符合内在/外在幻觉的分类定义。内在幻觉的测量空间损失约为DPS的7倍（0.039 vs 0.006），同时图像空间误差也显著升高；外在幻觉则维持极低的测量损失（0.003），与DPS相当，但图像空间误差显著存在。这一结果证明HalluGen的两个梯度上升分支能够忠实地生成两类不同机制的幻觉，而非产生模糊的中间状态。

### 幻觉基准测试：传统指标的失效与SHAFE的改进

Table 3构建了全面的幻觉指标基准，从效应量（Cohen's d）、检测AUC、锐度偏差曲线和严重度相关性四个维度评估像素级和特征级指标。核心发现：

- **传统指标对幻觉不敏感**：PSNR、SSIM、LPIPS的AUC均在0.50-0.52附近，接近随机猜测水平。LPIPS虽在效应量上略优于像素指标，但绝对检测能力仍然薄弱。
- **SHAFE显著提升检测性能**：SHAFE-ResNet50在内在幻觉检测上达到AUC 0.82，较PSNR提升约0.30；假阴性率降低24个百分点。这一提升来源于两个关键设计：低通滤波抑制高频噪声，以及温度控制的软基聚合突出稀疏的局部偏差。

Table 4进一步验证了HalluGen生成数据作为检测器训练集的价值：仅在HalluGen合成数据上训练的CNN，在真实复原输出的幻觉检测上达到AUC 0.91（内在）和0.77（外在），而LPIPS仅约0.50-0.51。这证明了合成幻觉与真实幻觉在特征空间中的分布一致性，以及HalluGen打破标注闭环的实用价值。

### 消融实验

#### HalluGen组件消融（Table 5）

![[assets/figures/papers/paper_list_l753_https_arxiv_org_abs_2512_03345/figures/014_Table_5.jpg]]
*Table 5: Effects of HVM, Entropy-based selection and Feature loss on hallucination taxonomy compliance using mean squared error within masked region (N=250)*

- **幻觉验证模块（HVM）**：移除HVM后，内在幻觉的测量空间和图像空间误差分别下降约7%和20%，说明HVM通过Cohen's d阈值拒绝不符合分类定义的样本，对保证生成质量至关重要。
- **熵基补丁选择**：替换为随机补丁选择会降低内在幻觉的偏差程度，验证了香农熵在自动定位信息丰富区域方面的有效性。
- **特征损失（外在幻觉）**：去除特征空间梯度上升后，外在幻觉的图像空间偏差减少超过一倍，证明像素空间梯度上升单独不足以产生充分的语义偏差，特征损失的加入是外在幻觉生成的关键。

#### SHAFE设计消融（Table 6 & Table 7）

![[assets/figures/papers/paper_list_l753_https_arxiv_org_abs_2512_03345/figures/016_Table_6.jpg]]
*Table 6: Ablation of low-pass filtering (LP) and weightedsoftmax aggregation in SHAFE, evaluated using AUC on hallucination detection (N=300). Both components improve detection sensitivity, and their combination yields the highest performance, indicating that suppressing high-frequency noise while adaptively weighting salient patches is crucial for detecting hallucinations*

![[assets/figures/papers/paper_list_l753_https_arxiv_org_abs_2512_03345/figures/015_Table_7.jpg]]
*Table 7: Impact of feature-layer selection on SHAFE hallucination detection (AUC, N=300) using SHAFE-ResNet50. Deep layers alone degrade performance due to semantic bias from ImageNet pretraining, whereas combining shallow layers provides the highest AUC, supporting the use of multi-layer early features for hallucination sensitivity*

Table 6显示，低通滤波与加权软基聚合的组合使AUC从0.52提升至0.78，两者具有互补性：低通滤波抑制非语义高频噪声，软基聚合自适应加权突出稀疏异常区域。Table 7的特征层选择实验表明，仅使用ResNet50深层特征会因ImageNet预训练的语义偏差导致性能下降，而组合浅层特征获得最高AUC（0.78），支持了SHAFE采用多层早期特征的设计选择。

温度参数τ的敏感性分析（Figure 9）显示，小温度（τ→0，近似最大池化）性能最优，在τ≤0.02范围内保持稳定；较大温度平滑了补丁权重，逐渐降低判别力，但SHAFE在所有测试温度下仍优于次优指标。

### 可控性分析

Figure 4验证了HalluGen的三维可控性：
- **强度控制**：梯度上升权重γ从0.0005增至0.01时，幻觉区域平方误差从718单调增至767，FID保持稳定。
- **空间范围控制**：补丁数量从1增至5时，总平方误差近似线性增长（150→810），FID始终低于0.45。
- **粒度控制**：补丁尺寸从16×16到64×64范围内，FID保持稳定，证明扩散流形先验在不同尺度下均能维持真实感。

### 跨域与跨任务泛化

Figure 5和Figure 6展示了HalluGen的泛化能力：在ImageNet自然图像上生成真实感幻觉（CLIP分数较DPS提升）；在MVTec AD工业图像上同样有效；在超分辨率（×6）和去模糊（σ=3.0）任务上维持低FID与高语义偏差。这表明HalluGen的梯度扰动机制不依赖于特定前向退化模型或图像域。

### 失败模式与局限

Figure 8揭示了HalluGen的主要失败模式：在平滑或同质区域（如脑壳核、背景），扩散先验主导逆向过程，抑制梯度上升信号，导致生成的幻觉视觉强度弱。这一局限源于扩散模型的流形约束——在低信息密度区域，先验倾向于维持平滑，梯度扰动难以积累足够的语义偏差。

SHAFE的局限体现在两个方面（Figure 11）：（1）低通滤波设计使其对高频伪影（如周期性网格噪声）敏感度较低；（2）可能高亮语义无关的大梯度边界区域。这些局限源于SHAFE对结构语义偏差的偏好设计，而非通用图像质量评估。

### 关键图表索引

- **Table 1**：真实感与语义偏差的分离验证（FID vs IoU）
- **Table 2**：内在/外在幻觉分类合规性（测量损失 vs 图像损失）
- **Table 3**：多指标幻觉基准测试（效应量、AUC、锐度偏差、严重度相关性）
- **Table 4**：无参考幻觉检测器的跨域泛化AUC
- **Table 5**：HVM、熵基选择、特征损失的组件消融
- **Table 6**：SHAFE低通滤波与软基聚合的消融
- **Table 7**：SHAFE特征层选择的影响
- **Figure 4**：强度、补丁数量、尺寸的可控性曲线
- **Figure 8**：同质区域生成弱幻觉的失败案例
- **Figure 9**：温度参数τ的敏感性曲线

![[assets/figures/papers/paper_list_l753_https_arxiv_org_abs_2512_03345/figures/003_Table_1.jpg]]
*Table 1: Comparisons of perceptual realism and semantic deviation of HalluGen and other baselines. For HalluGen, FID is low, comparable to DPS, confirming realism, while segmentation IoU within hallucinated regions drops sharply across different feature extractors, verifying semantic deviation*

![[assets/figures/papers/paper_list_l753_https_arxiv_org_abs_2512_03345/figures/004_Table_2.jpg]]
*Table 2: Hallucination taxonomy compliance of HalluGen using Mean Squared Error within masked region. Intrinsic sustains high measurement loss while extrinsic maintains low measurement loss despite semantic errors in image space. This validation confirms HalluGen faithfully generates both taxonomy types*

![[assets/figures/papers/paper_list_l753_https_arxiv_org_abs_2512_03345/figures/007_Figure_4.jpg]]
*Figure 4: Controllability of HalluGen. Left: Severity increases with gradient strength γ. Middle: Severity scales linearly with number of patches while FID stays low. Right: Stable realism across patch sizes (16×16 – 64×64). HalluGen provides fine-grained control over severity, spatial extent, and granularity while preserving realism*

![[assets/figures/papers/paper_list_l753_https_arxiv_org_abs_2512_03345/figures/011_Table_3.jpg]]
*Table 3: Comprehensive hallucination benchmark across metrics. Comparison of pixel- and feature-based metrics on effect size (discrimination), AUC (detection), Sharpenss Bias Curve (sharpness bias), and severity correlation (spearman rank correlation). The rightmost column shows AUC on raw predictions with manually labeled (binary) hallucinations. Baseline metrics show weak hallucination sensitivity, whereas SHAFE improve detection and interpretability. FPR/FNR are calculated using the optimal threshold from AUC curve*

![[assets/figures/papers/paper_list_l753_https_arxiv_org_abs_2512_03345/figures/012_Table_4.jpg]]
*Table 4: Reference-free hallucination detection. CNN trained only on HalluGen; thresholds selected on validation*

### 补充图表

![[assets/figures/papers/paper_list_l753_https_arxiv_org_abs_2512_03345/figures/002_Figure_2.jpg]]
*Figure 2: Existing metrics fail to penalize hallucinations. Across MVTec AD (left) and BraTS (right), PSNR, SSIM, and LPIPS assign higher scores to hallucinated predictions than to slightly blurred but correct images, reflecting a bias toward perceptual sharpness over correctness*

## 定位与知识库关联

### 1. 方法继承与核心突破

HalluGen 的方法根基建立在扩散后验采样（Diffusion Posterior Sampling, DPS）框架之上。DPS（Chung et al., 2022）通过在逆向扩散过程中引入数据一致性梯度下降项，将扩散模型用作求解病态逆问题的生成式先验。HalluGen 继承了 DPS 的采样引擎，但对其梯度信号进行了根本性的重构：**从全局一致性约束转向选择性一致性破坏**。

这一转变的技术瓶颈在于：如何在破坏数据一致性的同时，维持扩散流形先验所保证的视觉真实感。HalluGen 的因果调节旋钮（causal knob）是**掩码引导的梯度上升**——在选定的空间补丁内反转 DPS 的梯度方向，同时保留补丁外的标准梯度下降。这种“推—拉”机制使模型在局部区域偏离测量一致性（内在幻觉）或偏离语义真值（外在幻觉），而流形正则化（早期停止策略）确保扩散先验在后期步骤平滑边界，防止生成伪影。

### 2. 幻觉评估的知识库定位

在图像复原幻觉评估领域，现有工作面临一个闭环困境（Figure 1）：可靠的幻觉分析需要标注数据，但人工标注不仅昂贵且一致性极低（Cohen's κ = 0.30，Section 3.2）。HalluGen 的定位在于**打破这一循环**，通过可控合成提供自动标注的幻觉样本，为系统化的基准测试和检测器训练建立数据基础。

与现有的图像质量评估指标相比，HalluGen 揭示了更深层的问题：PSNR、SSIM、LPIPS 等指标对感知锐度的偏好超过语义正确性（Figure 2），使其在幻觉检测中表现接近随机猜测（AUC ≈ 0.50–0.52，Table 3）。HalluGen 提出的 SHAFE 指标通过浅层多尺度特征的低通滤波与温度加权软基聚合，将幻觉检测 AUC 提升至 0.78–0.82（Table 3），在方法层面填补了“语义偏差敏感度”与“高频噪声鲁棒性”之间的权衡空白。

### 3. 适用边界与跨域泛化能力

HalluGen 的适用边界由三个维度界定：

**正向退化模型的可微性**：HalluGen 依赖退化算子 $\mathcal{A}$ 的可微性来计算数据一致性梯度。当前验证覆盖了下采样（SR ×6）、高斯模糊（σ = 3.0）和低场 MRI 模拟（Figure 6），但对不可微或黑箱退化（如 JPEG 压缩）需要代理模型近似，这构成一个待验证的边界。

**扩散先验的领域覆盖**：HalluGen 在脑 MRI（HCP 数据集）、工业检测（MVTec AD）和自然图像（ImageNet）上展示了跨域泛化能力（Figure 3, Figure 5, Figure 6），但当前数据集仅基于健康成人大脑 MRI 构建（4,350 张标注图像，源自 1,450 张原始图像），未覆盖病理或不同人群的幻觉特征。扩散先验在多类别场景下的表现存在已知局限：强梯度上升可能导致跨物体流形的伪影。

**空间区域的纹理依赖性**：HalluGen 在平滑或同质区域（如脑部壳核、背景）难以生成明显幻觉，因为扩散先验会抑制梯度上升信号（Figure 8）。熵基补丁选择策略（Equation 10）通过自动筛选信息丰富区域部分缓解了这一问题，但无法完全克服流形先验的结构性约束。

### 4. 可控性的粒度与局限

HalluGen 提供三个维度的细粒度控制（Figure 4）：
- **强度**：通过梯度上升权重 γ 调节，幻觉严重程度随 γ 单调增加
- **空间范围**：补丁数量与总平方误差呈近似线性关系，同时 FID 保持稳定
- **粒度**：补丁尺寸在 16×16 至 64×64 范围内均维持真实感

然而，HalluGen 的控制是**统计性而非确定性**的。它无法指定幻觉的具体形态或拓扑变化，只能提供空间定位和强度调节。这一局限源于扩散采样的随机性本质——梯度上升信号与去噪过程相互作用，产生的幻觉结构受流形先验支配而非显式编程。

### 5. 幻觉验证模块的保障机制

HalluGen 内置的幻觉验证模块（HVM）在扩散终步计算掩码区域内的 Cohen's d（Equations 8, 9），拒绝不符合分类定义的样本并重新生成。消融实验（Table 5）表明，HVM 使内在幻觉的测量空间和图像空间误差分别增加约 7% 和 20%，确保生成样本严格满足分类定义。这一自检机制是 HalluGen 区别于简单对抗扰动生成的关键——它保证了合成数据的标注质量，使后续的基准测试和检测器训练建立在可靠的监督信号之上。

### 6. SHAFE 指标的方法定位

SHAFE 在设计哲学上与 LPIPS、DISTS 等特征空间指标共享“预训练特征提取”的思路，但引入了两个关键创新：
- **低通滤波**：抑制高频非语义噪声（如网格伪影），使指标聚焦于结构层面的语义偏差
- **温度加权软基聚合**：通过 $\tau$ 控制的 softmax 权重突出稀疏的局部偏差，而非全局平均

消融实验（Table 6）证实这两个组件的互补性：单独使用低通滤波或加权聚合仅将 AUC 从 0.52 提升至中等水平，而组合使用达到 0.78。特征层选择实验（Table 7）进一步表明，浅层特征的组合优于深层特征——深层特征因 ImageNet 预训练的语义偏差而降低幻觉敏感度，这为幻觉评估指标的特征工程提供了重要指导。

### 7. 开放问题与未来方向

基于 HalluGen 的当前边界，以下开放问题值得关注：

1. **退化模型的扩展**：如何将 HalluGen 适配到不可微退化（如 JPEG 压缩、去噪）或其他安全关键领域（如遥感、自动驾驶），需要设计可微代理或替代的梯度估计策略。

2. **结构感知的幻觉先验**：当前方法无法确定性控制幻觉的形态。能否引入结构先验（如解剖形状约束、物体部件模型）来实现拓扑可控的幻觉生成？

3. **多类别先验的稳定化**：针对多类别扩散先验，自适应或类别感知的梯度调度可能缓解跨流形伪影问题，但具体机制尚待探索。

4. **端到端鲁棒训练**：HalluGen 生成的幻觉数据能否直接用于优化幻觉感知的复原模型？这需要解决合成—真实幻觉的域差距问题。

5. **指标的时间维度扩展**：SHAFE 当前针对静态图像设计，其低通滤波和特征聚合策略是否可扩展为视频或 3D 医学影像的幻觉评估指标，需要验证时序一致性和体积特征提取的适配性。

6. **SHAFE 的已知局限**：SHAFE 对高频伪影（如周期性网格噪声）敏感度较低，且可能高亮语义无关的边界区域（Figure 11）。这些局限源于低通滤波的设计取舍——在抑制非语义噪声的同时，也丢失了部分高频结构信息。如何在频率选择性与语义敏感性之间取得更优平衡，是一个开放的设计问题。

---

**注意**：本文未提供 HalluGen 与其他幻觉生成方法（如对抗攻击、GAN 基编辑）的直接对比实验，因此无法在方法谱系中定位其相对优势。上述分析主要基于 HalluGen 与 DPS 基线的对比及其内部消融实验。如需补充与更广泛方法的谱系关系，建议查阅原始论文的 related work 部分或后续跟进工作。

## 原文 PDF

![[paperPDFs/CVPR_2026/HalluGen_Synthesizing_Realistic_and_Controllable_Hallucinations_for_Evaluating_Image_Restoration.pdf]]
