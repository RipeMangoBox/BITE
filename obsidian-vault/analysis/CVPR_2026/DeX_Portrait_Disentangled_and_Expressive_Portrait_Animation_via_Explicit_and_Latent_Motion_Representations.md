---
title: "DeX-Portrait: Disentangled and Expressive Portrait Animation via Explicit and Latent Motion Representations"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/DeX_Portrait_Disentangled_and_Expressive_Portrait_Animation_via_Explicit_and_Latent_Motion_Representations.pdf
aliases:
- DP
- DeX-Portrait
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 显式全局姿态变换(RTS) + 隐式表情编码，通过双分支姿态注入（射线图与参考变形）和渐进式混合CFG实现精准解耦。
primary_logic: 将头部姿态建模为低维显式变换（旋转、平移、缩放）以避免表情泄漏，将表情建模为高维隐式编码以保证表现力；通过GAN运动训练器的3D变形和AdaIN，以及扩散模型中的射线图、参考特征变形和交叉注意力，实现对姿态与表情的独立精准控制。
claims:
- DeX-Portrait achieves best CSIM (0.623 cross, 0.631 disentangled), AED, and APD compared to X-NeMo, HunyuanPortrait, etc.
- Ablation shows that removing ray map, reference warping, or augmentations degrades identity consistency and pose accuracy.
- Qualitative comparisons demonstrate superior disentangled control over head pose and expression, enabling expression-only and pose-only editing.
- Progressive hybrid CFG with S=5 preserves identity consistency better than standard CFG under large pose changes.
---

# DeX-Portrait: Disentangled and Expressive Portrait Animation via Explicit and Latent Motion Representations

> [!tip] 核心洞察
> 将头部姿态建模为低维显式变换（旋转、平移、缩放）以避免表情泄漏，将表情建模为高维隐式编码以保证表现力；通过GAN运动训练器的3D变形和AdaIN，以及扩散模型中的射线图、参考特征变形和交叉注意力，实现对姿态与表情的独立精准控制。

| 字段 | 内容 |
|------|------|
| 中文题名 | 解耦且富有表现力的肖像动画：基于显式与隐式运动表示 |
| 英文题名 | DeX-Portrait: Disentangled and Expressive Portrait Animation via Explicit and Latent Motion Representations |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Shi_DeX-Portrait_Disentangled_and_Expressive_Portrait_Animation_via_Explicit_and_Latent_CVPR_2026_paper.html) · [Project](https://syx132.github.io/DeX-Portrait/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | DeX-Portrait |
| Dataset | Self-Reenactment, Cross-Reenactment, Disentangled-Reenactment |

> [!tip] 效果简介
> - Self-Reenactment 上，PSNR 28.590 vs best among baselines (N/A)。
> - Cross-Reenactment 上，CSIM 0.623 vs best among baselines (N/A)；AED 0.0515 vs best among baselines (N/A)；APD 0.145 vs best among baselines (N/A)。
> - Disentangled-Reenactment 上，CSIM 0.631 vs best among baselines (N/A)。

## 概述

**核心问题**：现有扩散模型在肖像动画中难以实现头部姿态与面部表情的高保真解耦控制。主流方法通常将姿态与表情信息纠缠在隐式特征中，导致无法独立编辑——例如，仅改变表情时姿态也会发生偏移，反之亦然。这一瓶颈严重限制了仅表情编辑、仅姿态编辑等精细应用。

**核心思路**：DeX-Portrait 提出将头部姿态建模为低维显式全局变换（旋转、平移、缩放，即 RTS），将表情建模为高维隐式编码，从根本上避免信息泄漏。通过 GAN 运动训练器的 3D 变形与 AdaIN 调制，以及扩散模型中的双分支姿态注入（射线图与参考特征变形）和渐进式混合 CFG，实现对姿态与表情的独立精准控制。

**方法定位**：DeX-Portrait 采用两阶段流水线——首先训练解耦的姿态与表情编码器，再驯化一个潜扩散模型进行解耦动画生成。与 **X-NeMo**（Zhao et al., arXiv 2025）、**HunyuanPortrait**（Xu et al., CVPR 2025）等依赖隐式纠缠表示的方法相比，DeX-Portrait 在姿态-表情解耦控制上具有本质优势。

**主要结果**：在自重建、交叉重建和解耦重建三种设定下，DeX-Portrait 在身份一致性（CSIM）、表情准确度（AED）和姿态准确度（APD）等指标上均达到最优（Table 1）。消融实验证实，射线图、参考变形、增强策略和渐进式混合 CFG 各自对解耦质量有显著贡献（Table 2）。定性结果展示出优越的仅表情/仅姿态编辑能力（Figure 1, Figure 8）。

**局限与展望**：当前方法依赖人脸解析与关键点检测，无法处理卡通、素描等非真实风格，对多人场景和严重遮挡的鲁棒性不足。扩散推理效率尚未优化，实时应用受限。未来可探索向非真实风格扩展、提升多人场景鲁棒性，以及将显式姿态控制与音频等其他模态结合。

## 背景与动机

肖像动画（portrait animation）旨在根据驱动信号（如面部表情、头部姿态）生成与源肖像身份一致的真实感视频，在虚拟主播、远程社交、数字人等应用中需求迫切。该任务的核心挑战在于**同时实现高保真身份保持、准确的表情传递和精准的头部姿态控制**，且三者之间不能相互泄漏干扰。

### 现有方法的瓶颈

当前主流方法可大致分为两类。一类基于显式运动表示，如2D关键点或骨架图（skeleton map），虽然直观可控，但信息密度低，难以捕捉细腻的表情变化；另一类采用隐式编码，将姿态和表情压缩为统一的潜在特征，虽然表现力更强，但**姿态与表情高度纠缠**，导致无法实现“仅改变表情而保持姿态不变”或“仅转动头部而保持表情不变”的精细解耦控制。以最新的扩散式肖像动画方法 **X-NeMo**（Zhao et al., arXiv 2025）和 **HunyuanPortrait**（Xu et al., CVPR 2025）为例，它们均使用隐式条件编码，虽然生成质量出色，但在解耦重建（disentangled reenactment）场景下，改变驱动表情时头部姿态也会发生非预期的偏移，反之亦然。

这一瓶颈的根源在于：**头部姿态本质上是低维的全局刚体变换（旋转、平移、缩放），而面部表情是高维的局部非刚性形变**。将二者混入同一隐空间，模型难以自动分离这两类性质迥异的运动模式。

### 本文动机与核心思路

针对上述问题，DeX-Portrait 提出**显式姿态与隐式表情的混合运动表示**，从根源上阻断信息泄漏。具体而言：

- **头部姿态**被建模为显式的全局 RTS（Rotation, Translation, Scale）变换矩阵，具有6自由度，低维且精确，避免表情信息混入姿态编码。
- **面部表情**被编码为512维隐式向量，由 FAN（Facial Action Network）编码器提取，并通过精心设计的姿态增强策略（如随机旋转、缩放源图像）强制其对姿态变化不敏感，从而保证表情编码的纯净性。

在此基础上，方法通过两阶段流水线实现解耦动画：第一阶段使用基于 GAN 的运动训练器，借助3D变形（3D warping）和自适应实例归一化（AdaIN），在生成对抗训练中显式分离姿态编码器和表情编码器；第二阶段将解耦后的运动表示注入潜扩散模型（Latent Diffusion Model），通过**射线图（ray map）与参考特征变形（reference warping）双分支注入**以及**渐进式混合分类器自由引导（progressive hybrid CFG）**，实现对姿态和表情的独立精准控制，同时保持身份一致性。

这一设计使得 DeX-Portrait 首次在扩散式肖像动画框架中实现了真正意义上的解耦编辑——用户可独立操控头部姿态（旋转、平移、缩放）或面部表情，而另一维度保持与源图像完全一致（如 Figure 1 所示），为后续仅表情编辑、仅姿态编辑等精细应用奠定了基础。

## 核心创新

DeX-Portrait 的核心创新在于将**头部姿态**与**面部表情**分别建模为**显式低维变换**与**隐式高维编码**，并通过双分支注入机制和渐进式混合 CFG 实现二者的高保真解耦控制。这一设计从根本上解决了现有扩散模型（如 **X-NeMo**（Zhao et al., arXiv 2025）、**HunyuanPortrait**（Xu et al., CVPR 2025））中姿态与表情相互泄漏的问题，使仅表情编辑、仅姿态编辑等精细化应用成为可能。

### 关键设计变更

| 设计维度 | 基线方法 | DeX-Portrait 方案 | 证据锚点 |
|---------|---------|-------------------|---------|
| **头部姿态表示** | 2D 关键点/骨架图（显式但不精确）或纠缠的隐式特征 | 显式全局变换 $\mathbf{P} = [s\mathbf{R} \ \mathbf{t}]$，包含旋转、平移、缩放（6 DoF） | Section 3.2, Equation (2) |
| **表情表示** | 3DMM blendshape（表现力有限）或与姿态纠缠的隐式编码 | 512 维隐式编码，由 FAN 编码器提取，通过增强策略训练为姿态无关 | Section 3.2 |
| **姿态注入扩散模型** | 2D 骨架/球面图与噪声潜变量拼接 | 双分支：(1) 射线图拼接；(2) 参考 UNet 特征经 3D 变形后注入去噪 UNet | Section 3.3, Figure 2(b), Figure 4 |
| **CFG 策略** | 标准 CFG，所有去噪步统一施加 | 渐进式混合 CFG：前 S=5 步排除表情条件，随后 5 步线性混合，剩余步全条件 | Section 3.4, Equation (5), Figure 5, Figure 6 |

### 创新机制解析

**1. 显式姿态与隐式表情的表示解耦**

低维显式变换（RTS）天然避免表情信息泄漏到姿态通道，而高维隐式编码则保留了面部表情的丰富表现力。运动训练器通过 3D 变形和 AdaIN 调制，在 GAN 框架下强制两个编码器学习解耦表示；姿态增强（随机扰动 RTS 参数）和表情增强（同身份不同表情配对）进一步消除相互泄漏（Figure 3）。

**2. 双分支姿态注入**

射线图（Ray Map）将头部姿态转换为每个像素从标准姿态到目标姿态的 Plücker 向量，与噪声潜变量拼接，提供长程姿态对应关系。消融实验表明，移除射线图会导致大姿态变化下的身份一致性（CSIM）和姿态准确度（APD）显著下降（Table 2, Figure 10）。

参考变形注入则将源参考 UNet 特征通过姿态变换矩阵进行 3D 变形后加入去噪 UNet，为仅表情编辑场景提供稳定的恒等姿态信号，避免边缘错位（Figure 9）。

**3. 渐进式混合 CFG**

标准 CFG 在去噪早期同时施加姿态和表情条件，容易在大姿态变化下破坏身份一致性。渐进式混合 CFG 在前 5 步仅使用姿态条件（排除表情），随后 5 步线性混合表情条件，最终 25 步使用全部条件。实验表明 S=5 在身份一致性与表情准确度之间取得最佳平衡（Figure 5, Figure 6）。

### 创新效果的定量验证

在解耦重建（Disentangled-Reenactment）设定下，DeX-Portrait 取得 CSIM 0.631、AED 0.0546、APD 0.100 的最优成绩，显著优于不支持解耦控制的基线方法（Table 1）。消融实验确认，完整的双分支注入、增强策略和渐进式 CFG 组合带来一致的性能提升（Table 2）。

> **注意**：论文未提供模型参数量、推理速度或计算资源的对比数据，效率维度的创新性需人工补充验证。

## 整体框架

DeX-Portrait 采用**两阶段流水线**，核心思路是将头部姿态与面部表情分别编码为异质表示，再通过扩散模型实现解耦动画生成。整体架构如 Figure 2 所示。

![[assets/figures/papers/paper_list_l16_https_openaccess_thecvf_com_content_CVPR2026_html_Shi_DeX_Portrait_Disen/figures/002_Figure_2.jpg]]
*Figure 2: Our pipeline consists of two stages: (a) Training a disentangled pose and expression encoder using a motion trainer. (b) Taming a latent diffusion model for disentangled and expressive portrait animation*

**第一阶段：运动训练器（Motion Trainer）**

该阶段基于 GAN 框架，目标是学习**解耦的姿态编码器与表情编码器**。给定源肖像与驱动帧，系统通过显式姿态编码器（ConvNeXt）提取头部姿态的全局 RTS 变换矩阵 $\mathbf{P} = [s\mathbf{R} \; \mathbf{t}]$（6 自由度：旋转、平移、缩放），同时通过隐式表情编码器（FAN）将面部表情压缩为 512 维的隐式编码。为阻止姿态信息泄漏到表情编码中，训练时引入姿态与表情增强策略（Figure 3），使表情编码器对姿态变化不敏感。生成器内部采用 3D 变形与 AdaIN 调制，以 RTS 变换驱动源特征的几何对齐，再以表情编码调节外观风格，从而在 GAN 重建损失的约束下实现姿态与表情的分离。

**第二阶段：扩散解耦动画器（Diffusion-based Disentangled Animator）**

该阶段将预训练潜扩散模型改造为解耦动画生成器，接收三类条件信号：

1. **姿态注入（双分支）**：
   - *射线图注入*：将 RTS 姿态矩阵转换为 Plücker 射线图 $\text{RayMap}(u,v) = \mathbf{P}[u,v,0,0]^\top - [u,v,0,0]^\top$（见 Figure 4），与噪声潜变量在通道维拼接，提供源姿态到目标姿态的长程对应关系。
   - *参考特征变形注入*：将参考 UNet 的中间特征按姿态变换进行 3D 变形后，逐层注入到去噪 UNet 的对应层，实现边缘对齐的精确姿态控制。

2. **表情注入**：全局表情隐式编码通过交叉注意力（Cross-Attention）注入去噪 UNet，控制面部表情的生成。

3. **渐进混合分类器自由引导（Progressive Hybrid CFG）**：推理时采用分阶段 CFG 调度——前 $S=5$ 步排除表情条件（仅以姿态和身份为条件），随后 5 步线性混合表情条件，剩余步骤使用全部条件。该策略在保持身份一致性的同时，避免因表情信号过早介入而破坏源肖像的面部结构（见 Figure 5、Figure 6）。

最终，在时序模块的加持下，系统可生成连贯的肖像动画视频。整个流水线的输入为单张源肖像、驱动姿态序列与驱动表情序列，输出为姿态与表情可独立控制的动画帧。

## 核心模块与公式推导

DeX-Portrait 的核心架构由两个阶段级联构成：**解耦运动训练器** 与 **基于扩散的解耦动画器**。其设计目标是将头部姿态与面部表情编码为相互独立的表示，并在扩散生成过程中分别注入，从而实现精准的独立控制。

### 运动训练器：显式姿态与隐式表情的联合解耦

第一阶段通过 GAN 框架训练一对解耦的编码器。其核心设计在于表示形式的选择：

- **头部姿态** 被建模为低维显式全局变换矩阵 $\mathbf{P} \in \mathbb{R}^{3 \times 4}$，包含旋转 $\mathbf{R}$、平移 $\mathbf{t}$ 和缩放 $s$（RTS），共 6 自由度。这种显式参数化从根本上避免了高维隐式编码中常见的表情信息泄漏。

  $$\mathbf{P} = \left[ s \mathbf{R} \; \mathbf{t} \right]$$

- **面部表情** 则由 FAN 编码器提取为 512 维隐式编码。为保证该编码对姿态不敏感，训练中施加了姿态增强策略：对同一表情在不同姿态下的样本，强制编码器输出一致的隐式向量。

训练过程利用 3D 变形与 AdaIN 调制实现解耦：首先通过 $\mathbf{P}$ 对源肖像的 3D 特征进行显式变形以对齐驱动姿态，再由表情隐式编码经 AdaIN 调制生成器的风格参数，从而独立控制表情。姿态与表情增强策略是防止互泄漏的关键——若移除增强，生成质量显著下降。

### 扩散动画器：双分支条件注入

第二阶段将预训练的潜扩散模型改造为解耦动画器。其条件注入采用双分支设计，分别对应姿态与表情：

- **射线图注入**：将头部姿态变换 $\mathbf{P}$ 转换为 Plücker 射线图，与噪声潜变量在通道维拼接后送入去噪 UNet。射线图提供了源姿态与目标姿态之间的长程对应关系，对大幅姿态变化下的身份一致性至关重要。

  $$RayMap(u,v) = \mathbf{P} [u, v, 0, 0]^{\top} - [u, v, 0, 0]^{\top}$$

- **参考特征变形注入**：将源肖像在参考 UNet 中提取的多尺度特征，通过 $\mathbf{P}$ 进行 3D 变形后，以残差方式加至去噪 UNet 对应层。该机制在仅表情编辑场景中尤为关键——它提供了由姿态变换导出的恒等映射信号，确保背景与头部轮廓保持稳定，仅修改表情。

- **交叉注意力注入**：512 维表情隐式编码作为全局条件，通过交叉注意力层注入去噪 UNet，与现有扩散动画方法类似。

### 渐进混合分类器自由引导

标准 CFG 在所有去噪步骤中均匀施加条件，在大姿态变化下容易导致身份漂移。DeX-Portrait 提出渐进混合 CFG，分阶段调度条件强度：

$$\widetilde{\epsilon}_{\theta}^{*}(z_t, c; t) \triangleq \begin{cases} \widetilde{\epsilon}_{\theta}(z_t, c|_{\mathrm{exp}}; t), & 30 < t \le 35 \\ \widetilde{\epsilon}_{\theta}(z_t, c|_{\mathrm{exp}}; t) \frac{t-25}{5} + \widetilde{\epsilon}_{\theta}(z_t, c; t) \frac{30-t}{5}, & 25 < t \le 30 \\ \widetilde{\epsilon}_{\theta}(z_t, c; t), & t \le 25 \end{cases}$$

其中 $t$ 为扩散时间步，$c|_{\mathrm{exp}}$ 表示排除表情的条件。前 5 步仅使用姿态条件建立整体结构，随后 5 步线性混合引入表情，剩余 25 步使用全部条件。消融实验表明 $S=5$ 在身份一致性与表情准确度之间取得最佳平衡。

### 训练目标

扩散模型训练沿用标准潜扩散损失：

$$L_{\theta} = \mathbb{E}_{\epsilon \sim \mathcal{N}(0,1), t} \left[ \lVert \epsilon_t - \hat{\epsilon}_{\theta} \bigl( z_t, \pmb{c}; t \bigr) \rVert_2^2 \right]$$

其中 $z_t$ 为时间步 $t$ 的噪声潜变量，$\pmb{c}$ 为解耦条件（射线图、变形特征、表情隐式编码），$\hat{\epsilon}_{\theta}$ 为预测噪声。

### 补充图表

![[assets/figures/papers/paper_list_l16_https_openaccess_thecvf_com_content_CVPR2026_html_Shi_DeX_Portrait_Disen/figures/004_Figure_4.jpg]]
*Figure 4: Illustration of the ray map of head pose*

![[assets/figures/papers/paper_list_l16_https_openaccess_thecvf_com_content_CVPR2026_html_Shi_DeX_Portrait_Disen/figures/003_Figure_3.jpg]]
*Figure 3: Illustration of the pose and expression augmentation*

![[assets/figures/papers/paper_list_l16_https_openaccess_thecvf_com_content_CVPR2026_html_Shi_DeX_Portrait_Disen/figures/005_Figure_5.jpg]]
*Figure 5: Compared with the original CFG, our method achieves better consistency with the source portrait (e.g., facial shapes) in scenarios involving significant pose and expression variations*

![[assets/figures/papers/paper_list_l16_https_openaccess_thecvf_com_content_CVPR2026_html_Shi_DeX_Portrait_Disen/figures/006_Figure_6.jpg]]
*Figure 6: Our chosen S = 5 delivers animation results with both consistent identity and accurate expression*

## 实验与分析

### 实验设定

DeX-Portrait 采用两阶段训练策略：第一阶段训练基于 GAN 的运动编码器，第二阶段训练基于扩散模型的解耦动画器。运动训练阶段使用多视角与 in-the-wild 数据集，批量大小为 112，学习率为 $1 \times 10^{-4}$，共迭代 200k 步。扩散模型阶段在 512×512 分辨率下进行训练，并引入时序注意力层以在视频序列上微调，保证视频连贯性。

评估覆盖三种设定：**自重建（Self-Reenactment）**、**交叉重建（Cross-Reenactment）** 和 **解耦重建（Disentangled-Reenactment）**。指标包括 PSNR、LPIPS（自重建），以及身份一致性 CSIM、表情准确度 AED 和姿态准确度 APD（交叉与解耦重建）。基线方法涵盖 X-NeMo、HunyuanPortrait、HelloMeme、LIA、FantasyPortrait、DreamActor-M1 等代表性工作，其中多数不支持解耦重建（在 Table 1 中标记为 “N/A”）。

![[assets/figures/papers/paper_list_l16_https_openaccess_thecvf_com_content_CVPR2026_html_Shi_DeX_Portrait_Disen/figures/009_Table_1.jpg]]
*Table 1: Quantitative comparisons between our method and baselines. “N/A” means these methods do not support disentangled reenactment. We highlight the best scores with orange shading, and the second best with light orange*

### 主实验结果

**Table 1** 汇总了 DeX-Portrait 与各基线在三种设定下的定量对比。在自重建任务上，DeX-Portrait 取得最优 PSNR（28.590）和 LPIPS，表明其重建保真度领先。在交叉重建任务上，DeX-Portrait 在 CSIM（0.623）、AED（0.0515）和 APD（0.145）三项指标上均达到最优，说明模型在保持身份一致性的同时，能精准迁移驱动视频的姿态与表情。在解耦重建任务上，DeX-Portrait 同样全面领先：CSIM 为 0.631，AED 为 0.0546，APD 为 0.100，验证了显式姿态与隐式表情解耦表示的有效性。

定性对比中，**Figure 7** 展示了交叉重建场景下 DeX-Portrait 相较基线在身份保持和表情迁移上的优势；**Figure 8** 则聚焦解耦重建，DeX-Portrait 能够独立控制头部姿态或面部表情，而其他方法在仅编辑表情时姿态发生明显漂移，或在仅编辑姿态时表情出现泄漏。**Figure 1** 的 teaser 对比进一步表明，DeX-Portrait 在旋转、平移和缩放三个自由度上均提供比 X-NeMo 更精细的姿态控制。

![[assets/figures/papers/paper_list_l16_https_openaccess_thecvf_com_content_CVPR2026_html_Shi_DeX_Portrait_Disen/figures/007_Figure_7.jpg]]
*Figure 7: Qualitative comparison on cross-reenactment*

![[assets/figures/papers/paper_list_l16_https_openaccess_thecvf_com_content_CVPR2026_html_Shi_DeX_Portrait_Disen/figures/008_Figure_8.jpg]]
*Figure 8: Qualitative comparison on disentangled-reenactment*

### 消融实验

**Table 2** 给出了各组件消融的定量结果，**Figure 9–11** 提供了对应的定性可视化。核心发现如下：

- **头部姿态射线图（Ray Map）**：移除射线图后，CSIM 和 APD 均显著下降，尤其在姿态变化较大的场景中身份一致性恶化明显（Figure 10）。射线图通过 Plücker 坐标在像素级建立源姿态与目标姿态的长程对应关系，是稳定身份保持的关键。
- **参考特征变形注入（Reference Warping）**：移除该分支后，仅表情编辑场景中出现边缘错位和姿态漂移（Figure 9）。参考变形利用显式姿态变换矩阵对源 UNet 特征进行 3D 变形，为表情编辑提供刚性的身份参考信号。
- **增强策略（Augmentations）**：移除姿态与表情增强后，姿态编码器与表情编码器之间发生相互泄漏，导致生成质量下降（Figure 11）。增强策略通过随机扰动训练样本中的姿态或表情维度，强制编码器学习解耦表示。
- **渐进混合 CFG**：标准 CFG 在姿态变化较大时倾向于牺牲身份一致性以匹配表情条件。DeX-Portrait 提出的渐进混合 CFG（前 S=5 步排除表情条件，随后 5 步线性混合，剩余步骤使用全部条件）在身份一致性与表情准确度之间取得更优平衡。**Figure 5** 显示，渐进 CFG 在大姿态变化下保持更稳定的面部形状；**Figure 6** 的 S 值扫描实验确认 S=5 为最佳选择。
- **完整模型**：同时包含射线图、参考变形、增强策略和渐进 CFG 的完整模型在交叉重建与解耦重建的所有指标上均取得最优，验证了各组件的协同增益。

![[assets/figures/papers/paper_list_l16_https_openaccess_thecvf_com_content_CVPR2026_html_Shi_DeX_Portrait_Disen/figures/010_Figure_9.jpg]]
*Figure 9: Qualitative ablation study of reference warping on the expression-only editing scenario*

![[assets/figures/papers/paper_list_l16_https_openaccess_thecvf_com_content_CVPR2026_html_Shi_DeX_Portrait_Disen/figures/012_Figure_10.jpg]]
*Figure 10: Qualitative ablation of the head pose ray map*

![[assets/figures/papers/paper_list_l16_https_openaccess_thecvf_com_content_CVPR2026_html_Shi_DeX_Portrait_Disen/figures/013_Figure_11.jpg]]
*Figure 11: Qualitative ablation of the augmentations*

### 失败模式与局限性

**Figure 12** 展示了典型失败案例，揭示了以下局限：

1. **非真实人脸风格**：模型依赖人脸解析和关键点检测（如 MediaPipe），对卡通、素描等非真实人脸风格无法正常工作。
2. **多人场景与遮挡**：当画面包含多人肖像或存在严重遮挡时，运动编码器的检测与解耦能力显著下降。
3. **极端姿态**：在极端头部姿态下，外部检测器可能失效，导致姿态编码错误并级联影响生成质量。
4. **推理效率**：扩散模型的推理速度未进行优化，论文未展示实时应用能力，也未提供参数量或推理延迟的对比数据。

### 小结

DeX-Portrait 通过显式 RTS 姿态表示与隐式表情编码的双分支注入设计，在交叉重建和解耦重建任务上全面超越现有方法。消融实验系统验证了射线图、参考变形、增强策略和渐进 CFG 的必要性。当前局限主要集中在非真实风格泛化、多人/遮挡鲁棒性和推理效率方面，为后续工作指明了方向。

### 补充图表

![[assets/figures/papers/paper_list_l16_https_openaccess_thecvf_com_content_CVPR2026_html_Shi_DeX_Portrait_Disen/figures/011_Table_2.jpg]]
*Table 2: Quantitative ablation studies*

## 方法谱系与知识库定位

### 1. 问题定位：扩散肖像动画中的姿态-表情耦合瓶颈

当前基于扩散模型的肖像动画方法在生成质量上取得了显著进展，但普遍面临一个核心瓶颈：**头部姿态与面部表情的高保真解耦控制**。现有工作要么使用2D关键点/骨架图等显式表示，虽直观但精度不足且易与表情信号混淆；要么采用隐式特征编码，虽富有表现力却难以实现仅姿态或仅表情的独立编辑。这一耦合限制直接阻碍了细粒度肖像编辑、跨身份重演等应用场景的灵活性。

DeX-Portrait 的切入点正是打破这一耦合：将头部姿态建模为低维显式全局变换（旋转、平移、缩放），将表情建模为高维隐式编码，并通过精心设计的训练策略和注入机制确保二者在信息传递路径上互不泄漏。

### 2. 与现有工作的关系与差异

#### 2.1 显式姿态控制路线

传统方法普遍采用2D关键点、骨架图或3DMM参数作为姿态条件。这类表示虽然显式，但存在两个缺陷：一是2D投影丢失深度信息，难以处理大幅度旋转；二是关键点位置本身受表情影响，造成姿态与表情的信号串扰。DeX-Portrait 保留了显式控制的优势，但将表示升级为具有6自由度的 RTS 变换矩阵，并配合射线图（Ray Map）注入，在扩散模型的潜空间中提供长程姿态对应关系，从而在保持可解释性的同时显著提升姿态控制精度。

#### 2.2 隐式运动编码路线

以 **X-NeMo**（Zhao et al., arXiv 2025）和 **HunyuanPortrait**（Xu et al., CVPR 2025）为代表的近期工作采用隐式运动编码，通过交叉注意力将驱动信号注入扩散UNet，在生成质量上表现出色。然而，其运动编码器将姿态与表情信息混合压缩为单一隐变量，导致无法独立操控二者。DeX-Portrait 借鉴了交叉注意力注入表情的思路，但关键差异在于：表情编码器通过数据增强策略被显式训练为对姿态不敏感，从源头上切断了泄漏路径。

#### 2.3 参考特征注入路线

**HelloMeme**（Zhang et al., arXiv 2024）和 **DreamActor-M1**（Luo et al., ICCV 2025）等工作探索了将参考图像特征注入去噪网络以保持身份一致性。DeX-Portrait 的参考变形注入（Reference Warping Injection）在此基础上引入了3D几何约束：利用显式姿态变换对参考UNet特征进行3D变形后再与去噪UNet特征相加，使得姿态控制信号与源图像在几何上对齐。这一设计在仅表情编辑场景中尤为关键——当姿态应与源图像保持一致时，变形后的参考特征提供了稳定的身份锚点。

#### 2.4 GAN运动训练路线

**LIA**（Wang et al., arXiv 2022）和 **FantasyPortrait**（Wang et al., arXiv 2025）采用GAN框架学习运动表示。DeX-Portrait 的运动训练器同样基于GAN，但引入了两项关键创新：一是通过3D变形和AdaIN调制将姿态与表情的解耦结构性地嵌入生成器架构；二是设计了专门的姿态/表情增强策略（如图3所示），在训练过程中主动打破二者之间的统计相关性，迫使编码器学习真正解耦的表示。

### 3. 核心贡献的知识定位

DeX-Portrait 的方法论贡献可归纳为三个层面，每一层面对应一个知识缺口：

| 贡献层面 | 具体设计 | 填补的知识缺口 |
|---------|---------|---------------|
| **表示解耦** | 显式RTS姿态 + 隐式512维表情编码 | 扩散模型中姿态与表情的表示层面分离 |
| **注入解耦** | 双分支注入：射线图（姿态）+ 参考变形（姿态）+ 交叉注意力（表情） | 姿态与表情信号在去噪网络中的独立传递路径 |
| **训练解耦** | GAN运动训练器 + 增强策略 + 渐进混合CFG | 训练和推理阶段防止姿态-表情互泄漏的机制 |

其中，渐进混合CFG（Progressive Hybrid CFG）是一项精巧的推理时设计：在去噪的前5步排除表情条件，使模型先建立粗粒度的姿态结构；随后5步线性混合表情信号；剩余步骤使用全部条件。这一调度策略在身份一致性与表情准确度之间取得了平衡（S=5为最优，如图6所示），其背后的直觉是：扩散模型的早期步骤主要决定全局结构，此时引入表情信号容易干扰身份特征的建立。

### 4. 适用边界与局限

尽管 DeX-Portrait 在解耦控制上取得了显著进展，其适用边界受以下因素制约：

1. **人像风格的依赖**：方法依赖 MediaPipe 等外部检测器进行人脸解析和关键点提取，因此无法处理卡通、素描等非真实人脸风格。图12中的失败案例印证了这一点。

2. **多人及遮挡场景**：当前设计假设输入为单人正面肖像，对多人画面或严重遮挡场景的鲁棒性不足。这源于运动训练器和扩散注入机制均未考虑多实例交互或部分可见性。

3. **极端姿态下的检测失效**：显式姿态编码器依赖外部检测器提供的初始姿态估计，在极端侧脸或俯仰角下，MediaPipe 等工具的精度下降会传导至整个管线。

4. **推理效率未优化**：论文未报告模型参数量、推理速度或计算资源消耗，仅从生成质量角度评估性能。扩散模型的迭代去噪特性使其难以满足实时应用需求。

### 5. 开放问题

基于上述局限和方法设计，以下开放问题值得后续工作关注：

- **跨风格泛化**：如何将显式-隐式混合表示扩展到卡通、油画等非真实人脸风格？可能需要替换人脸解析前端，或引入风格无关的身份保持机制。
- **多人场景支持**：能否通过实例级姿态变换和注意力掩码将框架扩展到多人肖像动画？这需要解决实例间遮挡和身份混淆问题。
- **效率与解耦的权衡**：渐进混合CFG增加了推理调度的复杂度，能否通过蒸馏或一步生成模型在保持解耦能力的同时减少扩散步数？
- **多模态扩展**：显式姿态控制为与其他模态（如音频驱动、文本描述）的结合提供了接口，如何将RTS变换与音频节奏或语义描述对齐是一个有前景的方向。
- **评估体系的完善**：当前解耦重建的评估依赖于CSIM、AED和APD三个指标，但缺乏对解耦完备性的直接度量（如姿态操控时表情的不变程度）。设计更细粒度的解耦评估基准将有助于推动该方向的发展。

---

**本节小结**：DeX-Portrait 在扩散肖像动画的方法谱系中占据了“显式-隐式混合解耦”这一独特位置。它继承了显式姿态控制的直观性和隐式表情编码的表现力，同时通过双分支注入、增强训练和渐进CFG等机制解决了二者的耦合问题。其核心洞察——用低维显式变换避免表情泄漏，用高维隐式编码保证表现力——为后续工作提供了清晰的设计范式。当前的主要局限集中在非真实风格、多人场景和推理效率上，这些也是该方向最自然的延伸路径。

## 原文 PDF

![[paperPDFs/CVPR_2026/DeX_Portrait_Disentangled_and_Expressive_Portrait_Animation_via_Explicit_and_Latent_Motion_Representations.pdf]]