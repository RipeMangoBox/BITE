---
title: Spatial-Spectral Residuals Informed Diffusion Neural Operator for Pan-sharpening
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Spatial_Spectral_Residuals_Informed_Diffusion_Neural_Operator_for_Pan_sharpening.pdf
project_link: null
code_link: null
aliases:
- SSRIDNOPS
tags:
- CVPR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 利用Galerkin型神经算子近似注意力（降低到O(N d_v^2)）构建扩散去噪网络，并将像素级空间-光谱一致性残差直接注入每一逆扩散步，替代外部梯度引导，实现闭环动态校准。
primary_logic: 将扩散过程提升到连续函数空间，通过神经算子学习分辨率无关的生成先验，并通过空间-光谱残差的内部反馈驱动纹理丰富和光谱真实的高分辨率多光谱图像生成。
claims:
- 所提神经算子去噪框架相比传统注意力框架，FLOPs和内存占用显著降低，且在大尺度上避免内存溢出，推理速度提升数倍。
- SRINO在WorldView-3、GF-2、QuickBird等基准数据集上取得最佳的全锐化质量（PSNR、SAM、ERGAS、Q2^n等指标），全面超越同类扩散方法。
- 消融实验证明同时使用空间和光谱一致性残差能取得最佳性能，且残差引导策略优于传统梯度引导策略。
- WorldView-3 reduced resolution 上 PSNR↑ = 39.305 ± 2.882
---

# Spatial-Spectral Residuals Informed Diffusion Neural Operator for Pan-sharpening

> [!tip] 核心洞察
> 将扩散过程提升到连续函数空间，通过神经算子学习分辨率无关的生成先验，并通过空间-光谱残差的内部反馈驱动纹理丰富和光谱真实的高分辨率多光谱图像生成。

| 字段 | 内容 |
|------|------|
| 中文题名 | 空间-光谱残差引导的扩散神经算子全色锐化方法 |
| 英文题名 | Spatial-Spectral Residuals Informed Diffusion Neural Operator for Pan-sharpening |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Huang_Spatial-Spectral_Residuals_Informed_Diffusion_Neural_Operator_for_Pan-sharpening_CVPR_2026_paper.html) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | SRINO |
| Dataset | WorldView-3 reduced resolution, GF-2 reduced resolution, QuickBird reduced resolution, WorldView-3 full resolution |

> [!tip] 效果简介
> - WorldView-3 reduced resolution 上，PSNR↑ 39.305 ± 2.882 vs 最佳对比方法 (e.g., PanDiff) (显著提升)；SAM↓ 2.869 ± 0.589 vs 最佳对比方法 (降低)；ERGAS↓ 2.111 ± 0.524 vs 最佳对比方法 (降低)。
> - GF-2 reduced resolution 上，PSNR↑ 44.228 vs 最佳对比方法 (最优)。
> - QuickBird reduced resolution 上，PSNR↑ 38.864 vs 最佳对比方法 (最优)。

## 概要

全色锐化（Pan-sharpening）旨在将低分辨率多光谱图像（LRMS）与高分辨率全色图像（PAN）融合，生成高分辨率多光谱图像（HRMS）。现有基于扩散模型的方法虽然生成质量优异，但其去噪骨干普遍依赖自注意力机制，计算复杂度高达 $O(N^2)$，导致在大尺度场景下内存溢出、推理速度严重受限，难以部署于资源受限的卫星平台（Figure 1）。

针对这一瓶颈，本文提出**空间-光谱残差引导的扩散神经算子（SRINO）**。核心思路是将扩散过程从离散像素空间提升到连续函数空间，利用 **Galerkin 型神经算子** 替代传统注意力骨干，将计算复杂度降至 $O(N d_v^2)$；同时，在每一逆扩散步中注入**像素级空间一致性残差与光谱一致性残差**作为内部动态条件，替代传统的外部梯度引导，形成闭环校准机制。

在 WorldView-3、GF-2 和 QuickBird 等多个基准数据集上，SRINO 在 PSNR、SAM、ERGAS 等指标上全面超越包括 **PanDiff**（Meng et al., IEEE TGRS 2023）、**U-Know-DiffPan**（Kim et al., CVPR 2025）和 **SSDiff**（Zhong et al., NeurIPS 2024）在内的 SOTA 方法（Table 1, Table 2）。消融实验证实，空间与光谱残差的联合引导是关键设计，且残差引导策略优于传统梯度引导（Table 3, Figure 7）。



全色锐化（Pan-sharpening）旨在将高空间分辨率的全色（PAN）图像与低空间分辨率的多光谱（LRMS）图像融合，生成高空间分辨率的多光谱（HRMS）图像。这一任务是遥感图像处理中的基础性难题，其核心挑战在于如何在注入空间细节的同时保持光谱信息的保真度。

近年来，扩散概率模型（Diffusion Probabilistic Models）在图像生成领域展现出强大的先验建模能力，并开始被引入全色锐化任务。代表性工作如 **PanDiff**（Meng et al., IEEE TGRS 2023）、**SSDiff**（Zhong et al., NeurIPS 2024）以及 **U-Know-DiffPan**（Kim et al., CVPR 2025）等，均尝试利用扩散过程的迭代去噪机制来恢复高分辨率图像。然而，现有扩散式全色锐化方法面临两个关键瓶颈：

**瓶颈一：注意力骨干的计算效率危机。** 当前扩散模型普遍采用基于自注意力（Self-Attention）的Transformer架构作为去噪网络骨干。自注意力的计算复杂度为 $\mathcal{O}(N^2)$（其中 $N$ 为像素数），在处理高分辨率遥感图像时，FLOPs和内存占用急剧膨胀。如 Figure 1 所示，在大尺度输入下，传统注意力架构甚至遭遇内存溢出（Out-of-Memory），严重制约了其在星载等资源受限平台上的部署可行性。

**瓶颈二：外部梯度引导的优化困境。** 为将无条件扩散模型适配到全色锐化这一条件生成任务，现有方法通常采用梯度引导策略——在逆扩散过程中，利用无监督损失项（如空间一致性、光谱一致性损失）的梯度来修正噪声预测。然而，如 Figure 2 所示，这种外部引导方式存在多损失项之间的梯度冲突风险，且需要繁琐的权重调谐，难以实现精细、稳定的闭环控制。

上述瓶颈的根源在于：现有方法将扩散过程局限在离散像素空间，去噪网络缺乏对连续函数空间的建模能力，同时引导机制是外挂式的，未能与去噪过程深度融合。这引出了本文的核心动机：**能否将扩散模型提升到连续函数空间，通过神经算子学习分辨率无关的生成先验，并以内部反馈的方式实现空间-光谱一致性约束的动态校准？**

具体而言，本文试图回答以下问题：（1）如何构建一个计算高效的扩散去噪骨干，使其复杂度远低于自注意力机制？（2）如何设计一种内嵌的引导范式，替代外部梯度引导，实现像素级空间细节与光谱保真度的闭环动态优化？这两个问题的解决，将推动扩散式全色锐化方法向高效、高保真和可部署化方向迈出关键一步。



## 核心方法与创新机理

SRINO 的核心创新在于将全色锐化任务中的扩散生成过程从离散像素空间提升到**连续函数空间**，并以此为基础构建了两项关键改进：**高效神经算子去噪骨干**和**空间-光谱一致性残差内部引导机制**。

### 从注意力到神经算子的去噪骨干跃迁

标准扩散模型通常采用基于自注意力的 Transformer 架构作为去噪网络，其计算复杂度为 $O(N^2)$（$N$ 为图像像素数）。这一瓶颈导致大尺度遥感图像处理时资源消耗激增，甚至出现内存溢出（Figure 1）。SRINO 将去噪骨干替换为 **Galerkin 型神经算子**，通过线性注意力近似将复杂度降至 $O(N d_v^2)$，其中 $d_v$ 为特征维度且远小于 $N$。具体而言，该方法将注意力核参数化为查询-键-值内积形式：

$$\kappa(\phi(\xi),\phi(\eta_i)) = \frac{\exp\left(\frac{\langle W_q\phi(\xi), W_k\phi(\eta_i)\rangle}{\sqrt{d_v}}\right)}{\sum_{k=1}^{N}\exp\left(\frac{\langle W_q\phi(\eta_k), W_k\phi(\eta_i)\rangle}{\sqrt{d_v}}\right)} W_v$$

并利用 Galerkin 投影将其转化为线性形式 $\phi_{\mathrm{out}} = Q(\tilde{K}^{\top}\tilde{V})/N$，在保持全局交互能力的同时大幅降低计算开销。这一设计使得扩散模型能够在连续函数空间学习**分辨率无关**的生成先验，为后续的轻量适配奠定基础。

### 从外部梯度引导到内部残差引导的范式转变

此前扩散全色锐化方法（如 **SSDiff**（Zhong et al., NeurIPS 2024）和 **PanDiff**（Meng et al., IEEE TGRS 2023））多采用**外部梯度引导**策略：通过无监督损失项的梯度来修正噪声预测，面临梯度冲突和权重调优困难。SRINO 提出**三重引导适配**（Triple Guidance Adaptation, TGA），将像素级空间一致性残差和光谱一致性残差直接注入每一逆扩散步，构建闭环动态校准：

- **空间一致性残差** $\mathbf{R}_{\mathrm{spa}}^{(t)}$：当前预测 HRMS 与 PAN 降通道版本的像素级差异，驱动空间纹理的精细注入；
- **光谱一致性残差** $\mathbf{R}_{\mathrm{spe}}^{(t)}$：当前预测 HRMS 模糊下采样后与原始 LRMS 的差异，确保光谱信息保真。

这两类残差通过通道注意力调制后送入冻结的神经算子层，实现“空间-光谱”协同优化。消融实验（Table 3, Figure 7）表明，联合使用两类残差显著优于单一残差或传统梯度引导策略，验证了内部残差反馈机制的有效性。

### 两阶段训练流水线

上述创新通过两阶段训练实现（Figure 3）：
1. **函数空间条件扩散预训练**：在连续函数空间用 Galerkin 神经算子去噪网络学习高分辨率图像的通用空间-光谱先验；
2. **三重引导适配**：冻结去噪骨干，通过轻量辅助网络注入跨模态特征及像素级空间-光谱残差，微调生成器以适应全色锐化任务。

这种“预训练-适配”范式使得模型既能继承函数空间的强泛化能力，又能以极低的计算代价完成下游任务特化，在 WorldView-3、GF-2、QuickBird 等主流基准上均取得最优性能。



SRINO 采用**两阶段训练流水线**，将扩散过程从离散像素空间提升到连续函数空间，并通过内部残差反馈替代传统的外部梯度引导。如图3所示，第一阶段在函数空间预训练条件扩散模型，学习分辨率无关的高质量空间-光谱先验；第二阶段通过三重引导适配将冻结的去噪骨干注入全色锐化任务。

**第一阶段：函数空间条件扩散预训练。** 去噪网络由级联的 Galerkin 型神经算子层构建，其核心是将标准自注意力近似为线性注意力形式，使计算复杂度从 $O(N^2)$ 降至 $O(N d_v^2)$。扩散目标定义为高分辨率多光谱图像与低分辨率多光谱图像的残差 $\mathbf{X}_0 = \mathbf{H} - \mathbf{L}$，前向过程按 $\mathbf{X}_t = \sqrt{\bar{\alpha}_t}\mathbf{X}_0 + \sqrt{1-\bar{\alpha}_t}\varepsilon$ 逐步加噪。逆向去噪步参数化为高斯分布 $p_{\theta}(\mathbf{X}_{t-1} \mid \mathbf{X}_t, \mathbf{H}) = \mathcal{N}(\mu_{\theta}(\mathbf{X}_t, \mathbf{H}, t), \sigma_t^2 \mathbf{I})$，网络直接预测干净残差 $\widehat{\mathbf{X}}_0 = \mathcal{G}_{\theta}(\mathbf{X}_t, \mathbf{H}, t)$，并以 $\mathcal{L}_{\mathrm{I}} = \mathbb{E}_{t, \mathbf{X}_0, \varepsilon} \|\mathbf{X}_0 - \mathcal{G}_{\theta}(\mathbf{X}_t, \mathbf{H}, t)\|_1$ 进行训练。此阶段仅使用 $\mathbf{H}$ 作为条件输入，使神经算子学习到分辨率无关的生成先验。

**第二阶段：三重引导适配。** 冻结第一阶段的去噪骨干，引入轻量辅助模块实现三类引导：
1. **跨模态特征引导**：辅助预测器 $\Phi$ 接收全色图像 $\mathbf{P}$、低分辨率多光谱图像 $\mathbf{L}$ 及其伪全色纹理残差 $\mathbf{P} - f_{\mathrm{M2P}}(\mathbf{L})$ 的拼接，生成融合特征 $\mathbf{V}$ 和伪高分辨率多光谱图像 $\widehat{\mathbf{H}}$。
2. **空间一致性残差引导**：在每一逆扩散步，计算当前预测 HRMS 与降通道版本的像素级差异 $\mathbf{R}_{\mathrm{spa}}^{(t)}$，直接注入网络以强化空间细节。
3. **光谱一致性残差引导**：将当前预测 HRMS 经模糊核下采样后与原始 LRMS 比较，得到光谱残差 $\mathbf{R}_{\mathrm{spe}}^{(t)} = (f_{\mathrm{KE}}([\mathbf{P},\mathbf{L}]) \circledast \widehat{\mathbf{Y}}^{(t+1)}) - \mathbf{L}$，经投影后与空间特征拼接，再通过全局池化和 MLP 生成的通道注意力权重进行调制，最终送入冻结的算子层。

两阶段的衔接逻辑是：第一阶段提供强大的生成先验和高效的算子去噪骨干，第二阶段以极低的额外参数（仅辅助预测器和残差投影模块）将该先验适配到全色锐化任务，形成“预测-残差计算-特征调制”的闭环动态校准机制。

### 补充图表

![[assets/figures/papers/paper_list_l2597_https_openaccess_thecvf_com_content_CVPR2026_html_Huang_Spatial_Spectral/figures/003_Figure_3.jpg]]
*Figure 3: Framework overview of the proposed SRINO, which is implemented through a two-stage training pipeline. Firstly, we pretrain a conditional diffusion model built with Galerkin-type operator layers on high-resolution references to learn high-quality spatial and spectral representations. Subsequently, we introduce a triple guidance adaptation (TGA) strategy, including cross-modality feature V, pixel-wise spatial and spectral consistency residuals, R(t)spa and R(t)spe , to fine-tune the model for generating corresponding HRMS images*



SRINO 的核心由两个技术模块构成：**Galerkin 型神经算子去噪骨干**（Stage I）与**三重引导适配机制**（Stage II）。前者将扩散过程提升到连续函数空间，以线性注意力替代标准自注意力，实现分辨率无关的生成先验；后者通过像素级空间-光谱一致性残差的内部反馈，驱动纹理丰富和光谱真实的高分辨率多光谱图像生成。

### 神经算子去噪骨干

去噪网络 $\mathcal{G}_{\theta}$ 由投影层与算子层级联构成，其参数化形式为：

$$\mathcal{G}_{\theta} = \mathrm{P}_{\mathrm{out}} \circ \mathrm{M}_{L} \circ \ldots \circ \mathrm{M}_{2} \circ \mathrm{M}_{1} \circ \mathrm{P}_{\mathrm{in}} \tag{1}$$

其中 $\mathrm{P}_{\mathrm{in}}$ 和 $\mathrm{P}_{\mathrm{out}}$ 为输入/输出投影层，$\mathrm{M}_l$ 为第 $l$ 个算子层。每一算子层的更新遵循残差形式：

$$\phi_{l+1}(\xi) = \phi_{l}(\xi) + \mathcal{O}\left(\mathcal{K}_{l}(\phi_{l})(\xi) + \phi_{l}(\xi)\right) \tag{2}$$

式中 $\phi_l(\xi)$ 为位置 $\xi$ 处的特征表示，$\mathcal{K}_l$ 为核积分算子，$\mathcal{O}$ 为逐点前馈网络。核积分算子在连续域上建模全局交互：

$$\mathcal{K}(\phi)(\xi) = \int_{\Omega} \kappa(\phi(\xi),\phi(\eta))\phi(\eta)\,\mathrm{d}\eta \tag{3}$$

在离散网格 $\Omega_{h_f}$ 上近似为：

$$\mathcal{K}(\phi)(\xi) \approx \sum_{i=1}^{N} \kappa(\phi(\xi),\phi(\eta_i))\phi(\eta_i),\quad \forall \xi \in \Omega_{h_f} \tag{4}$$

标准注意力核通过查询-键-值内积参数化：

$$\kappa(\phi(\xi),\phi(\eta_i)) = \frac{\exp\left(\frac{\langle W_q\phi(\xi), W_k\phi(\eta_i)\rangle}{\sqrt{d_v}}\right)}{\sum_{k=1}^{N}\exp\left(\frac{\langle W_q\phi(\eta_k), W_k\phi(\eta_i)\rangle}{\sqrt{d_v}}\right)} W_v \tag{5}$$

该形式的计算复杂度为 $O(N^2)$。SRINO 采用 **Galerkin 型线性注意力** 进行近似：

$$\phi_{\mathrm{out}} = Q(\tilde{K}^{\top}\tilde{V})/N \tag{6}$$

其中 $Q = W_q\phi$，$\tilde{K} = W_k\phi$，$\tilde{V} = W_v\phi$。复杂度从 $O(N^2)$ 降至 $O(N d_v^2)$，在大尺度输入下避免了内存溢出（见 Figure 1）。

![[assets/figures/papers/paper_list_l2597_https_openaccess_thecvf_com_content_CVPR2026_html_Huang_Spatial_Spectral/figures/001_Figure_1.jpg]]
*Figure 1: Comparison of FLOPs, Memory Usage, and Inference Time between our neural operator-based denoising framework and the conventional attention-based counterpart [25]. Our approach significantly reduces both FLOPs and memory usage, particularly at larger scales where the attention-based architecture encounters out-of-memory issues. During inference, we achieve a several-fold speedup*

### 扩散过程与训练目标

扩散目标定义为高分辨率多光谱图像 $\mathbf{H}$ 与低分辨率多光谱图像 $\mathbf{L}$ 的残差：

$$\mathbf{X}_0 = \mathbf{H} - \mathbf{L} \tag{7}$$

前向加噪过程为：

$$\mathbf{X}_t = \sqrt{\bar{\alpha}_t}\mathbf{X}_0 + \sqrt{1-\bar{\alpha}_t}\varepsilon \tag{8}$$

逆向去噪步参数化为高斯分布：

$$p_{\theta}(\mathbf{X}_{t-1} \mid \mathbf{X}_t, \mathbf{H}) = \mathcal{N}(\mu_{\theta}(\mathbf{X}_t, \mathbf{H}, t), \sigma_t^2 \mathbf{I}) \tag{9}$$

网络直接预测干净残差 $\widehat{\mathbf{X}}_0 = \mathcal{G}_{\theta}(\mathbf{X}_t, \mathbf{H}, t)$，均值 $\mu_{\theta}$ 由 $\widehat{\mathbf{X}}_0$ 和 $\mathbf{X}_t$ 解析给出。Stage I 训练损失为 L1 损失：

$$\mathcal{L}_{\mathrm{I}} = \mathbb{E}_{t, \mathbf{X}_0, \varepsilon} \|\mathbf{X}_0 - \mathcal{G}_{\theta}(\mathbf{X}_t, \mathbf{H}, t)\|_1 \tag{10}$$

### 三重引导适配

Stage II 冻结去噪骨干，通过轻量辅助网络 $\Phi$ 注入三类引导信号。

**跨模态特征提取**：辅助预测器 $\Phi$ 利用光谱-空间映射 $f_{\mathrm{M2P}}$ 提取伪全色纹理残差，并与全色图像 $\mathbf{P}$、低分辨率多光谱 $\mathbf{L}$ 拼接后生成融合特征 $\mathbf{V}$ 及伪高分辨率多光谱 $\widehat{\mathbf{H}}$：

$$\mathbf{V} = \Phi([\mathbf{P}, \mathbf{L}, (\mathbf{P} - f_{\mathrm{M2P}}(\mathbf{L}))]), \quad \widehat{\mathbf{H}} = \operatorname{Conv}_{3\times3}(\mathbf{V}) + \mathbf{L} \tag{11}$$

**空间一致性残差**：当前预测的 HRMS $\widehat{\mathbf{Y}}^{(t+1)}$ 与降通道版本逐像素比较，强化空间细节注入：

$$\mathbf{R}_{\mathrm{spa}}^{(t)} = \widehat{\mathbf{Y}}^{(t+1)} - \frac{1}{s}\sum_{i=1}^{s} \widehat{\mathbf{Y}}^{(t+1)}_i \tag{14-15}$$

其中 $s$ 为光谱通道数。

**光谱一致性残差**：将当前预测 HRMS 经模糊核下采样后与原始 LRMS 比较，保证光谱保真度：

$$\mathbf{R}_{\mathrm{spe}}^{(t)} = (f_{\mathrm{KE}}([\mathbf{P},\mathbf{L}]) \circledast \widehat{\mathbf{Y}}^{(t+1)}) - \mathbf{L} \tag{16}$$

其中 $f_{\mathrm{KE}}$ 为核估计网络，$\circledast$ 为卷积操作。

**通道特征调制**：将光谱残差投影后与空间特征拼接，通过全局池化与 MLP 生成通道注意力权重，调制后送入冻结的算子层：

$$\widetilde{\mathbf{Z}}_{t}^{l} = \operatorname{Conv}_{1\times1}([\mathbf{Z}_{t}^{l}, \operatorname{Proj}(\mathbf{R}_{\mathrm{spe}}^{(t)})]),\quad \omega_{t}^{l+1} = \sigma(\operatorname{MLP}([\operatorname{GAP}(\widetilde{\mathbf{Z}}_{t}^{l}), \operatorname{GMP}(\widetilde{\mathbf{Z}}_{t}^{l})])),\quad \mathbf{F}_{t}^{l+1} = \mathrm{M}_{l}(\mathbf{Z}_{t}^{l} \odot \omega_{t}^{l+1} + \mathbf{Z}_{t}^{l}) \tag{17}$$

Stage II 联合残差引导的损失函数为：

$$\mathcal{L}_{\mathrm{II}} = \mathbb{E}_{t, \mathbf{X}_0, \varepsilon} \| \mathbf{X}_0 - \mathcal{G}_{\theta}(\mathbf{X}_t, \mathbf{P}, \mathbf{L}, \mathbf{R}_{\mathrm{spa}}^{(t)}, \mathbf{R}_{\mathrm{spe}}^{(t)}, t) \|_1 \tag{18}$$

### 关键设计要点

- **复杂度瓶颈突破**：Galerkin 线性注意力将复杂度从 $O(N^2)$ 降至 $O(N d_v^2)$，在大尺度输入下避免内存溢出，推理速度提升数倍（Figure 1）。
- **内部残差引导 vs. 外部梯度引导**：传统梯度引导需手动平衡无监督损失权重，存在梯度冲突风险；SRINO 将空间-光谱残差直接注入每一逆扩散步，形成闭环动态校准（Figure 2）。
- **两阶段训练策略**：Stage I 在连续函数空间学习高质量先验，Stage II 冻结骨干仅微调轻量适配模块，兼顾生成质量与任务适配效率。

![[assets/figures/papers/paper_list_l2597_https_openaccess_thecvf_com_content_CVPR2026_html_Huang_Spatial_Spectral/figures/002_Figure_2.jpg]]
*Figure 2: Schematic illustration of the previous gradient-guided strategy and our spatial-spectral residuals informed paradigm. The former uses the gradients of unsupervised losses to update the noise prediction, risking gradient conflicts and requiring tedious weight tuning. Instead, our approach directly incorporates the element-wise spatial-spectral residuals as additional inputs to the denoising network, enabling directed generation of texture-rich and spectrally realistic products*



## 实验与关键发现

### 主实验结果

SRINO 在 WorldView-3、GF-2 和 QuickBird 三个基准数据集上均取得了最优的全色锐化质量，全面超越包括 **PanDiff** (Meng et al., IEEE TGRS 2023) 和 **U-Know-DiffPan** (Kim et al., CVPR 2025) 在内的所有对比方法。

在 **WorldView-3 降分辨率** 测试中（Table 1），SRINO 的 PSNR 达到 39.305 ± 2.882，SAM 降至 2.869 ± 0.589，ERGAS 降至 2.111 ± 0.524，Q2^n 达到 0.922 ± 0.084，HQNR 达到 0.950 ± 0.017，五项指标均列第一。在 **全分辨率** 评估中，SRINO 同样取得 D_lambda 0.019 ± 0.008 和 D_s 0.032 ± 0.012 的最优结果，表明方法在无参考真值的情况下仍能保持优异的光谱保真度和空间细节注入能力。

![[assets/figures/papers/paper_list_l2597_https_openaccess_thecvf_com_content_CVPR2026_html_Huang_Spatial_Spectral/figures/004_Table_1.jpg]]
*Table 1: Quantitative results for reduced and full resolution WV3 samples, comparing several representative state-of-the-art methods. Bold: Best; Underline: Second best*

在 **GF-2** 和 **QuickBird** 数据集上（Table 2），SRINO 继续领跑所有参考指标：GF-2 上 PSNR 44.228、SAM 0.646、ERGAS 0.573、Q2^n 0.985；QuickBird 上 PSNR 38.864、SAM 4.351、ERGAS 3.542、Q2^n 0.940。定性结果（Figure 4）进一步显示，SRINO 生成的图像在均质区域和细纹理区域均具有最低的绝对误差响应，结构更锐利且光谱伪影更少。

![[assets/figures/papers/paper_list_l2597_https_openaccess_thecvf_com_content_CVPR2026_html_Huang_Spatial_Spectral/figures/006_Table_2.jpg]]
*Table 2: Quantitative results for reduced resolution GF2 and QB samples, comparing several representative state-of-the-art methods. Bold: Best; Underline: Second best*

![[assets/figures/papers/paper_list_l2597_https_openaccess_thecvf_com_content_CVPR2026_html_Huang_Spatial_Spectral/figures/005_Figure_4.jpg]]
*Figure 4: The visual results (top) and mean absolute error maps (bottom) of DL-based methods on a reduced resolution WV3 sample*

### 效率分析

Figure 1 展示了所提 Galerkin 型神经算子去噪框架与传统注意力架构（以 PanDiff 为代表）在 FLOPs、内存占用和推理时间上的对比。结果表明，神经算子框架的 FLOPs 和内存占用显著降低，且在大尺度输入下注意力架构出现内存溢出时，所提方法仍能正常运行，推理速度实现数倍提升。这验证了将扩散去噪骨干从 $O(N^2)$ 自注意力降为 $O(N d_v^2)$ 线性注意力的关键设计动机。

### 消融实验

**空间与光谱一致性残差的作用**（Table 3）：同时使用空间残差和光谱残差时性能最优。单独移除空间残差或光谱残差均导致 PSNR、SAM、ERGAS 等指标出现不同程度的下降。Figure 6 的特征图和频谱分析进一步揭示，空间残差的缺失会导致高频纹理模糊，光谱残差的缺失则引入光谱偏移。

**残差引导 vs. 梯度引导**（Figure 7）：与传统梯度引导策略（不同强度 α=1, 10, 100）相比，本文的像素级空间-光谱残差内部引导范式能够避免梯度冲突，在所有强度设置下均稳定取得更优性能。

**去噪骨干对比**（Figure 8）：将 Galerkin 神经算子替换为 CNN 或 FNO 均导致性能下降，验证了所选去噪骨干在建模全局交互和分辨率无关先验方面的有效性。

### 实现细节与公平性说明

所有实验基于统一的数据划分和训练设置：批次大小 32，patch 尺寸 64×64，AdamW 优化器（动量系数 0.9/0.999），初始学习率 4×10⁻⁵ 且每 10,000 次迭代衰减 0.5 倍。扩散步数设为 500，推理时采用 25 步 DDIM 采样。所有对比方法在相同条件下复现或使用原作者提供的模型，确保比较的公平性。

### 补充图表

![[assets/figures/papers/paper_list_l2597_https_openaccess_thecvf_com_content_CVPR2026_html_Huang_Spatial_Spectral/figures/009_Table_3.jpg]]
*Table 3: Ablation study on the core spatial consistency residual*

![[assets/figures/papers/paper_list_l2597_https_openaccess_thecvf_com_content_CVPR2026_html_Huang_Spatial_Spectral/figures/011_Figure_7.jpg]]
*Figure 7: Ablation study on conventional gradient-guided strategy with varying intensities (α=1, α=10, α=100) and our spatialspectral residual-informed paradigm*

![[assets/figures/papers/paper_list_l2597_https_openaccess_thecvf_com_content_CVPR2026_html_Huang_Spatial_Spectral/figures/008_Figure_8.jpg]]
*Figure 8: Ablation study on different denoising backbones*

![[assets/figures/papers/paper_list_l2597_https_openaccess_thecvf_com_content_CVPR2026_html_Huang_Spatial_Spectral/figures/010_Figure_6.jpg]]
*Figure 6: Feature maps and frequency amplitude spectra for the ablation study of the spatial and spectral consistency residuals*

![[assets/figures/papers/paper_list_l2597_https_openaccess_thecvf_com_content_CVPR2026_html_Huang_Spatial_Spectral/figures/007_Figure_5.jpg]]
*Figure 5: Feature maps across different denoiser layers*



## 定位与知识库关联

### 1. 扩散全色锐化的演进脉络与SRINO的定位

全色锐化方法的范式演进经历了从传统分量替换/多分辨率分析，到深度学习驱动的卷积/Transformer架构，再到扩散生成模型的三个阶段。SRINO处于第三阶段的前沿，但其核心贡献并非简单地引入扩散模型，而是针对现有扩散全色锐化方法的两大结构性瓶颈——**计算效率**与**引导机制**——进行了根本性重构。

在扩散全色锐化这一子领域中，**PanDiff**（Meng et al., IEEE TGRS 2023）率先建立了条件扩散模型在全色锐化任务上的基线范式，采用标准自注意力作为去噪骨干，并通过无监督损失函数的梯度进行外部引导。**SSDiff**（Zhong et al., NeurIPS 2024）进一步探索了空间-光谱集成的扩散策略。**U-Know-DiffPan**（Kim et al., CVPR 2025）则在扩散框架中引入不确定性建模，代表了该方向的最新进展。

SRINO与上述工作的根本区别体现在两个维度：

**（1）去噪骨干的范式跃迁：从注意力到神经算子。** 现有扩散方法普遍采用基于自注意力的Transformer架构作为去噪网络，其计算复杂度为 $O(N^2)$（$N$ 为像素数），在大尺度遥感图像上面临严重的内存瓶颈（Figure 1证实注意力架构在大尺度下出现内存溢出）。SRINO将去噪骨干替换为Galerkin型神经算子（Galerkin-type Neural Operator），通过线性注意力近似将复杂度降至 $O(N d_v^2)$（$d_v$ 为值向量维度，通常远小于 $N$），实现了从“离散像素空间生成”到“连续函数空间生成”的范式跃迁。这一设计使得扩散过程学习的是分辨率无关的算子映射，而非特定分辨率的像素映射。

**（2）引导机制的闭环重构：从外部梯度到内部残差。** 传统扩散全色锐化方法（如PanDiff）依赖无监督损失函数的梯度对噪声预测进行外部修正，存在梯度冲突风险和权重调参负担（Figure 2对比了两种范式）。SRINO提出“三重引导适配”（Triple Guidance Adaptation, TGA）机制，将像素级的空间一致性残差和光谱一致性残差直接注入每一逆扩散步的中间特征层，形成闭环动态校准。这一设计将引导信号内化为网络结构的一部分，避免了外部梯度引导的不稳定性。

### 2. 与神经算子相关工作的关系

SRINO的去噪骨干借鉴了神经算子（Neural Operator）领域的思想，特别是Fourier神经算子（FNO）和Galerkin型注意力机制。神经算子的核心优势在于学习函数空间之间的映射，天然支持不同分辨率输入。SRINO将这一特性与扩散模型的生成能力融合，构建了“函数空间条件扩散”框架。

值得注意的是，消融实验（Figure 8）表明，直接用CNN或标准FNO替换Galerkin神经算子均导致性能下降，说明Galerkin型线性注意力在建模遥感图像中的长程空间-光谱依赖关系方面具有独特优势。这一结果暗示，神经算子的选择并非任意——核积分算子的形式（此处为Galerkin注意力核）需要与任务的数据特性相匹配。

### 3. 适用边界与局限性

**适用场景：** SRINO在WorldView-3、GF-2、QuickBird三个主流卫星数据集上均取得最优结果（Table 1, Table 2），覆盖了不同空间分辨率和光谱配置的全色锐化场景。其计算效率优势在大尺度图像上尤为突出（Figure 1），适合需要在星载或边缘设备上部署的应用场景。

**潜在局限（需人工验证）：**
- 扩散模型固有的推理延迟问题：虽然SRINO通过DDIM采样将推理步数压缩至25步，但相比单步前馈的CNN/Transformer方法仍存在推理时间开销。论文未直接对比与传统方法（如FusionNet、LAGConv等）的推理速度差异。
- 两阶段训练流程增加了训练复杂度：第一阶段需在高分辨率参考图像上预训练条件扩散模型，对训练数据的数量和质量有一定要求。
- 论文未讨论对极端地物覆盖（如大面积水体、浓密云层遮挡）的鲁棒性。
- 全分辨率评估依赖无参考指标（$D_\lambda$、$D_s$），其与真实全锐化质量的对应关系在遥感领域仍存在争议。

### 4. 开放问题

1. **神经算子架构的进一步优化空间：** Galerkin型注意力是否是最优的核积分算子形式？是否存在更适合多光谱遥感图像的核函数设计？
2. **扩散步数的理论下界：** 当前25步DDIM采样是经验选择，是否存在理论保证的更少步数方案？
3. **跨传感器泛化能力：** 论文实验限于单一传感器内的训练-测试划分，SRINO学习到的算子映射能否泛化到未见过的传感器配置？
4. **与物理模型的融合：** 空间和光谱残差目前基于像素级差异计算，是否可引入传感器成像的物理退化模型（如MTF、光谱响应函数）来增强残差的物理可解释性？



## 原文 PDF

![[paperPDFs/CVPR_2026/Spatial_Spectral_Residuals_Informed_Diffusion_Neural_Operator_for_Pan_sharpening.pdf]]
