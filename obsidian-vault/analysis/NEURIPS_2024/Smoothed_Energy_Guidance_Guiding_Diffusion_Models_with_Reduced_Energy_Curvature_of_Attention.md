---
title: "Smoothed Energy Guidance: Guiding Diffusion Models with Reduced Energy Curvature of Attention"
type: paper
paper_level: A
venue: NEURIPS
year: 2024
pdf_ref: paperPDFs/NeurIPS_2024/Smoothed_Energy_Guidance_Guiding_Diffusion_Models_with_Reduced_Energy_Curvature_of_Attention.pdf
project_link: null
code_link: https://github.com/SusungHong/SEG-SDXL
aliases:
- SEGS
- SEGGDMRECA
tags:
- NEURIPS_2024
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 自注意力权重的高斯模糊程度（通过调节高斯核标准差σ）控制能量景观的曲率，从而影响生成效果。
primary_logic: 将自注意力操作视为能量最小化步骤，通过对注意力权重进行高斯模糊来平滑底层能量函数的曲率，然后将平滑后的预测作为负向引导信号，实现无需训练、无条件且无饱和的引导，并可通过固定引导尺度下调节σ来控制效果。
claims:
- SEG定义了自注意力的能量，通过减少能量景观的曲率并将输出用作无条件预测。
- 高斯模糊注意力权重可以减弱底层能量函数的高斯曲率（定理3.1）。
- 在无条件生成中，SEG (σ→∞) 的FID为88.215，显著优于vanilla SDXL (129.496) 和PAG (105.271)，同时LPIPS相似，实现了Pareto改进。
- 随着σ增加，图像质量（FID和CLIP Score）持续改善，而无饱和现象。
---

# Smoothed Energy Guidance: Guiding Diffusion Models with Reduced Energy Curvature of Attention

> [!tip] 核心洞察
> 将自注意力操作视为能量最小化步骤，通过对注意力权重进行高斯模糊来平滑底层能量函数的曲率，然后将平滑后的预测作为负向引导信号，实现无需训练、无条件且无饱和的引导，并可通过固定引导尺度下调节σ来控制效果。

| 字段 | 内容 |
|------|------|
| 中文题名 | 平滑能量引导：通过降低注意力能量曲率引导扩散模型 |
| 英文题名 | Smoothed Energy Guidance: Guiding Diffusion Models with Reduced Energy Curvature of Attention |
| 会议/期刊 | NEURIPS 2024 |
| Links | [paper](https://openreview.net/forum?id=JK728xy8G7) · [Code](https://github.com/SusungHong/SEG-SDXL) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | Smoothed Energy Guidance (SEG) |
| Dataset | MS-COCO 2014验证集（30k张图像，无条件生成）, MS-COCO 2014验证集（文本条件生成） |

> [!tip] 效果简介
> - MS-COCO 2014验证集（30k张图像，无条件生成） 上，FID↓ 88.215 (SEG σ→∞) vs 129.496 (Vanilla SDXL) (-41.281)。
> - 同上 上，LPIPS_vgg↓ (与vanilla SDXL对比的偏离度) 0.536 (SEG σ→∞) vs 1 (Vanilla SDXL, 自身对比) (-0.464)。
> - MS-COCO 2014验证集（文本条件生成） 上，FID↓ 26.169 (SEG σ→∞) vs 53.423 (Vanilla SDXL, 无CFG) (-27.254)。

## 概要

扩散模型的无条件生成长期以来面临质量瓶颈：分类器自由引导（CFG）需要条件信息，而现有的无条件引导方法——如自注意力引导（SAG）和扰动注意力引导（PAG）——依赖启发式规则，缺乏明确的数学基础，且常伴随细节平滑、色彩饱和或颜色偏移等副作用。

本文提出**平滑能量引导（Smoothed Energy Guidance, SEG）**，核心洞察是将自注意力操作视为能量函数最小化步骤，通过对注意力权重施加高斯模糊来降低底层能量景观的曲率，并将平滑后的预测作为负向引导信号。该方法无需训练、不依赖条件输入，且通过调节高斯核标准差σ即可控制引导效果，在固定引导尺度下避免了传统方法的饱和问题。

在MS-COCO 2014验证集的无条件生成任务上，SEG（σ→∞）将FID从vanilla SDXL的129.496降至88.215，同时LPIPS偏离度仅为0.536，实现了质量与副效应减少的Pareto改进。在文本条件生成中，SEG同样显著优于无CFG的基线（FID: 26.169 vs. 53.423），且CLIP Score有所提升。

### 扩散模型引导的瓶颈

扩散模型通过逐步去噪将随机噪声转换为高质量图像，其采样过程由反向随机微分方程（SDE）描述：

$$d \mathbf{x} = [\mathbf{f}(\mathbf{x}, t) - g(t)^2 \nabla_{\mathbf{x}} \log p_t(\mathbf{x})] dt + g(t) d\bar{\mathbf{w}}$$

其中得分函数 $\nabla_{\mathbf{x}} \log p_t(\mathbf{x})$ 由神经网络 $s_\theta(\mathbf{x}, t)$ 近似。然而，直接从此分布采样往往产生质量平庸的结果，因此引导技术成为提升生成质量的关键手段。

**无分类器引导（CFG）** 是当前最主流的条件引导方法，其核心思想是通过线性外推增强条件信号：

$$d \mathbf { x } = [ \mathbf { f } ( \mathbf { x } , t ) - g ( t ) ^ { 2 } ( \gamma _ { \mathrm { c f g } } \mathbf { s } _ { \theta } ( \mathbf { x } , t , c ) - ( \gamma _ { \mathrm { c f g } } - 1 ) \mathbf { s } _ { \theta } ( \mathbf { x } , t ) ) ] d t + g ( t ) d \bar { \mathbf { w } }$$

CFG通过调节引导尺度 $\gamma_{cfg}$ 在保真度和多样性之间取得平衡，但它存在一个根本性限制：**CFG需要一个条件信号 $c$，无法应用于无条件生成场景**。这意味着当用户不提供文本提示或其他条件时，CFG完全失效。

### 现有无条件引导方法的缺陷

为填补这一空白，研究者提出了无需外部条件的引导方法，主要包括两类：

- **自注意力引导（SAG）**：通过对注意力图进行模糊处理来扰动输入，将原始预测与扰动预测的差异作为引导信号。
- **扰动注意力引导（PAG）**：用恒等注意力图替换原始自注意力图，利用这种结构性扰动产生引导信号。

这些方法虽然实现了无条件引导，但存在明显的**副作用**：生成图像出现细节平滑、色彩饱和度过高、整体色调偏移等问题。更重要的是，这些方法依赖**启发式设计**，缺乏明确的数学基础和理论解释，导致生成质量次优，难以系统性地控制引导效果。

### 核心动机：从能量视角重新理解注意力

本文的核心洞察在于重新审视自注意力机制的本质。将自注意力操作视为一个**能量最小化步骤**——注意力权重矩阵 $\mathbf{A} = \mathbf{QK}^\top$ 定义了一个底层能量景观，而softmax操作恰好对应于在该能量景观上执行梯度下降。基于这一视角，可以为自注意力定义明确的能量函数：

$$E ( \mathbf { A } ) : = \sum _ { i = 1 } ^ { H } \sum _ { j = 1 } ^ { W } E ^ { \prime } ( \mathbf { a } _ { : ( i , j ) } ) , \quad E ^ { \prime } ( \mathbf { a } ) : = - \mathrm { l s e } \left( \mathbf { a } \right) = - \log \left( \sum _ { k = 1 } ^ { H } \sum _ { l = 1 } ^ { W } e ^ { a _ { ( k , l ) } } \right)$$

该能量函数使用负log-sum-exp形式，为每个查询位置量化其注意力分布的能量状态。

### SEG的动机与目标

基于上述能量视角，本文提出一个自然的问题：**能否通过操控自注意力的能量景观来产生有效的引导信号？**

具体而言，本文的方法论动机是：通过对自注意力权重施加高斯模糊，可以**系统性地降低底层能量函数的曲率**，从而产生一个“能量平滑”版本的预测。将原始预测与平滑预测之间的差异作为引导信号，即可实现：

1. **无需训练的引导**：不修改模型权重，仅在推理时介入注意力计算。
2. **无条件生成支持**：不依赖任何外部条件信号（如文本提示）。
3. **无饱和效应**：与CFG不同，增大引导强度不会导致图像过饱和或色彩偏移。
4. **可解释的控制机制**：通过调节高斯核标准差 $\sigma$ 来控制能量曲率的降低程度，从而精细调控生成效果，而非简单增大引导尺度。

这一设计将无条件引导从启发式工程提升为具有明确数学基础的框架，为扩散模型的引导技术开辟了新的理论路径。

## 核心方法与创新机理

SEG 的核心创新在于为扩散模型的无条件引导提供了一个**有理论可解释的操作机制**：将自注意力操作形式化为一个能量最小化步骤，通过高斯模糊降低该能量景观的曲率，并将曲率降低后的预测作为负向引导信号。这与现有无条件引导方法（**SAG**、**PAG**）形成根本性差异——后者依赖启发式扰动（模糊输入像素或替换为恒等注意力图），缺乏对引导效果的理论解释，且易产生细节平滑、颜色偏移等副作用。

### 关键改变槽位

从方法论角度看，SEG 相对于现有基线改变了两个核心组件：

**1. 自注意力权重的计算方式**

- **基线做法**：标准缩放点积注意力 $\mathbf{A} = \text{softmax}(\mathbf{Q}\mathbf{K}^\top / \sqrt{d})$，权重矩阵直接由查询-键内积经 softmax 归一化得到。
- **SEG 做法**：对注意力权重施加二维高斯模糊 $(\mathbf{Q}\mathbf{K}^\top)_{\text{seg}} = G \ast (\mathbf{Q}\mathbf{K}^\top)$，其中 $G$ 是标准差为 $\sigma$ 的二维高斯滤波器。根据 **Proposition 3.1**，这等价于先模糊查询矩阵再计算注意力权重：$(G \ast \mathbf{Q})\mathbf{K}^\top$，从而避免了直接对 $HW \times HW$ 注意力矩阵做卷积的二次复杂度。

**2. 引导信号的来源**

- **CFG**：利用条件预测与无条件预测之差进行外推，无法应用于无条件生成场景。
- **SAG/PAG**：利用原始预测与模糊/扰动预测之差，但缺乏对“扰动为何有效”的机理解释。
- **SEG**：利用原始得分网络 $\mathbf{s}_\theta(\mathbf{x}, t)$ 与能量曲率降低后的平滑得分网络 $\tilde{\mathbf{s}}_\theta(\mathbf{x}, t)$ 之差进行引导，采样过程遵循：
  $$d\mathbf{x} = [\mathbf{f} - g^2(\gamma_{\text{seg}} \mathbf{s}_\theta - (\gamma_{\text{seg}}-1)\tilde{\mathbf{s}}_\theta)]dt + g d\bar{\mathbf{w}}$$
  其中 $\tilde{\mathbf{s}}_\theta$ 由模糊注意力权重生成，引导强度由 $\gamma_{\text{seg}}$ 控制。

### 核心理论支撑

SEG 的独特之处在于它为上述操作提供了严格的数学解释。论文将自注意力权重 $\mathbf{A}$ 的能量定义为逐查询位置的负 log-sum-exp：
$$E(\mathbf{A}) := \sum_{i=1}^{H}\sum_{j=1}^{W} E'(\mathbf{a}_{:(i,j)}), \quad E'(\mathbf{a}) := -\text{lse}(\mathbf{a}) = -\log\left(\sum_{k=1}^{H}\sum_{l=1}^{W} e^{a_{(k,l)}}\right)$$
在此框架下，**Theorem 3.1** 证明：对注意力权重施加高斯模糊可以减弱底层能量函数的高斯曲率。这意味着模糊操作并非任意扰动，而是有方向地“平滑”了能量景观，使模型在采样时摆脱局部尖锐的极小值，从而生成更合理、更高质量的图像。

### 控制机制的解耦

另一个关键创新在于**效果控制参数的重新分配**。在 CFG 和 PAG 中，引导强度（$\gamma_{\text{cfg}}$ 或 $\gamma_{\text{pag}}$）是唯一可调参数，增大引导尺度往往带来质量提升与副作用（如饱和、过饱和）的耦合。SEG 将控制权从引导尺度转移到高斯核标准差 $\sigma$：固定 $\gamma_{\text{seg}} = 3.0$（与 PAG 一致），通过增大 $\sigma$ 来持续改善图像质量（FID 和 CLIP Score），而无饱和现象（Table 2, Figure 6）。这种解耦使得 SEG 在无条件生成中实现了对 vanilla SDXL 的 **Pareto 改进**——FID 从 129.496 降至 88.215（$\sigma \to \infty$），同时 LPIPS 偏离度保持相似水平（Table 1）。

Smoothed Energy Guidance (SEG) 是一种训练无关、条件无关的扩散模型引导方法。其核心思想是将自注意力操作重新解释为能量最小化步骤，通过高斯模糊降低注意力能量景观的曲率，并将平滑后的预测作为负向引导信号。整体框架由三个关键模块串联构成：高斯模糊查询模块、平滑得分网络、以及引导外推模块。

**高斯模糊查询模块** 是整个流水线的入口。给定扩散模型中间层的查询矩阵 $\mathbf{Q}$ 和键矩阵 $\mathbf{K}$，标准自注意力权重通过 $\mathbf{A} = \text{softmax}(\mathbf{Q}\mathbf{K}^\top / \sqrt{d})$ 计算。SEG 在此处引入一个 2D 高斯滤波器 $G$，其标准差 $\sigma$ 是可调节的核心超参数。根据 Proposition 3.1，对注意力权重矩阵 $\mathbf{Q}\mathbf{K}^\top$ 进行高斯模糊等价于对查询矩阵 $\mathbf{Q}$ 进行模糊后再与 $\mathbf{K}$ 计算内积：$G \ast (\mathbf{Q}\mathbf{K}^\top) = (G \ast \mathbf{Q})\mathbf{K}^\top$。这一等价性使 SEG 避免了直接模糊整个 $HW \times HW$ 注意力矩阵的二次复杂度，只需对 $\mathbf{Q}$ 做空间卷积即可。

**平滑得分网络 $\tilde{\mathbf{s}}_\theta$** 接收模糊后的注意力权重，生成能量曲率降低的预测。形式上，$\tilde{\mathbf{s}}_\theta$ 与原始得分网络 $\mathbf{s}_\theta$ 共享所有参数，唯一的差异在于自注意力计算中使用了 $(\mathbf{Q}\mathbf{K}^\top)_{\text{seg}} = G \ast (\mathbf{Q}\mathbf{K}^\top)$。从能量视角看，原始注意力权重定义了一个逐查询位置的能量函数 $E(\mathbf{A}) = \sum_{i,j} -\text{lse}(\mathbf{a}_{:(i,j)})$，其中 $\text{lse}$ 为 log-sum-exp 算子。高斯模糊通过保持均值、减小方差（Lemma 3.1）来平滑该能量函数的曲率（Theorem 3.1），使得 $\tilde{\mathbf{s}}_\theta$ 输出更“平坦”的预测。

**引导外推模块** 将原始预测与平滑预测线性组合，形成最终的采样方向。SEG 引导的反向 SDE 为：

$$d\mathbf{x} = \big[\mathbf{f}(\mathbf{x}, t) - g(t)^2 \big(\gamma_{\text{seg}} \mathbf{s}_\theta(\mathbf{x}, t) - (\gamma_{\text{seg}} - 1) \tilde{\mathbf{s}}_\theta(\mathbf{x}, t)\big)\big] dt + g(t) d\bar{\mathbf{w}}$$

其中 $\gamma_{\text{seg}}$ 是引导尺度。与 Classifier-Free Guidance (CFG) 将无条件预测作为负向信号不同，SEG 将平滑预测 $\tilde{\mathbf{s}}_\theta$ 置于负向位置。当 $\gamma_{\text{seg}} > 1$ 时，采样过程沿远离能量平滑区域的方向推进，从而增强图像的细节和结构。论文固定 $\gamma_{\text{seg}} = 3.0$（与 PAG 一致），通过调节 $\sigma$ 来控制引导效果：增大 $\sigma$ 持续改善 FID 和 CLIP Score，而不会像单纯增大引导尺度那样引入饱和或颜色偏移等副作用（见 Table 2 和 Figure 6 的消融实验）。

**输入输出流**：输入为纯噪声 $\mathbf{x}_T \sim \mathcal{N}(0, \mathbf{I})$（无条件生成）或噪声加条件嵌入（条件生成）。在每个去噪步骤中，得分网络执行两次前向传播——一次使用原始注意力权重得到 $\mathbf{s}_\theta$，一次使用模糊查询得到 $\tilde{\mathbf{s}}_\theta$。两者经引导外推模块组合后更新 $\mathbf{x}_t$，最终输出生成的图像 $\mathbf{x}_0$。该流水线无需任何额外训练，可直接应用于预训练的 SDXL 等扩散模型，且与 CFG、ControlNet 等条件控制方法兼容（通过 Eq. (10) 联合引导）。Figure 7 直观展示了原始采样过程与 SEG 修改后采样过程的对比，包括注意力权重和对应能量景观的变化。

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_JK728xy8G7/figures/008_Figure_7.jpg]]
*Figure 7: Pipeline of SEG. (a) Original sampling process, self-attention weights, and the corresponding energy landscape. (b) Our modified sampling process with blurred queries where*

### 3.1 自注意力作为能量最小化

SEG 的理论起点是将扩散模型中的自注意力操作重新解释为能量最小化步骤。给定注意力权重矩阵 $\mathbf{A} = \mathbf{Q}\mathbf{K}^\top$，对每个查询位置 $(i,j)$ 定义其能量函数：

$$E'(\mathbf{a}) := -\mathrm{lse}(\mathbf{a}) = -\log\left(\sum_{k=1}^{H}\sum_{l=1}^{W} e^{a_{(k,l)}}\right)$$

其中 $\mathrm{lse}$ 为 log-sum-exp 算子。整个注意力图的能量为所有位置能量之和：

$$E(\mathbf{A}) := \sum_{i=1}^{H}\sum_{j=1}^{W} E'(\mathbf{a}_{:(i,j)})$$

该能量函数的一阶导数正是 softmax 操作，而 softmax 是自注意力计算的核心步骤，因此注意力操作可被视为在该能量景观上的最小化步骤。

### 3.2 高斯模糊降低能量曲率

SEG 的核心操作是对注意力权重施加二维高斯模糊。高斯核定义为：

$$G(x,y) = \frac{1}{2\pi\sigma^2} e^{-\frac{(x-\mu_x)^2 + (y-\mu_y)^2}{2\sigma^2}}$$

模糊后的注意力权重为卷积结果：

$$\tilde{a}_{(i,j)} = \sum_{m=-k}^{k}\sum_{n=-k}^{k} G(m,n) \cdot a_{(i+m,j+n)}$$

该操作具有两个关键性质：

- **方差单调减小**（Lemma 3.1）：$\mathrm{Var}_{i,j}[\tilde{a}_{(i,j)}] \le \mathrm{Var}[a_{(i,j)}]$，即高斯模糊保持注意力权重的均值不变，同时降低其方差。
- **能量值增大**（Lemma 3.2）：高斯模糊增加注意力权重的 $\mathrm{lse}$ 项，使能量函数值上升。

这两条性质共同导致能量景观的高斯曲率减弱（Theorem 3.1），其直观含义是：模糊后的注意力对局部细节的敏感性降低，能量函数变得更加平滑。

### 3.3 平滑得分网络与引导采样

基于上述理论，SEG 构建了一个平滑得分网络 $\tilde{\mathbf{s}}_\theta$。与原始网络 $\mathbf{s}_\theta$ 的区别仅在于自注意力权重的计算方式——对 $\mathbf{Q}\mathbf{K}^\top$ 施加高斯模糊：

$$(\mathbf{Q}\mathbf{K}^\top)_{\mathrm{seg}} = G \ast (\mathbf{Q}\mathbf{K}^\top)$$

为高效实现，论文证明了模糊查询矩阵等价于模糊整个注意力权重矩阵（Proposition 3.1）：

$$G \ast (\mathbf{Q}\mathbf{K}^\top) = (G \ast \mathbf{Q})\mathbf{K}^\top$$

这一等价性避免了在 $H \times W \times H \times W$ 空间上的直接卷积，将计算复杂度从二次降为线性。

SEG 的引导采样通过线性外推组合原始预测与平滑预测，其反向 SDE 为：

$$d\mathbf{x} = [\mathbf{f}(\mathbf{x}, t) - g(t)^2(\gamma_{\mathrm{seg}}\mathbf{s}_\theta(\mathbf{x}, t) - (\gamma_{\mathrm{seg}}-1)\tilde{\mathbf{s}}_\theta(\mathbf{x}, t))]dt + g(t)d\bar{\mathbf{w}}$$

其中 $\gamma_{\mathrm{seg}}$ 为引导尺度（论文中固定为 3.0，与 PAG 一致），$\tilde{\mathbf{s}}_\theta$ 为平滑得分网络。当 $\gamma_{\mathrm{seg}} = 1$ 时退化为无引导采样；$\gamma_{\mathrm{seg}} > 1$ 时，模型被推向与平滑预测相反的方向，从而增强细节和结构。

SEG 还可与 CFG 联合使用，组合采样公式为：

$$d\mathbf{x} = [\mathbf{f}(\mathbf{x}, t) - g(t)^2((1-\gamma_{\mathrm{cfg}}+\gamma_{\mathrm{seg}})\mathbf{s}_\theta(\mathbf{x}, t) + \gamma_{\mathrm{cfg}}\mathbf{s}_\theta(\mathbf{x}, t, c) - \gamma_{\mathrm{seg}}\tilde{\mathbf{s}}_\theta(\mathbf{x}, t))]dt + g(t)d\bar{\mathbf{w}}$$

### 3.4 控制机制的关键差异

与 SAG 和 PAG 等基线方法不同，SEG 的引导效果不通过 $\gamma_{\mathrm{seg}}$ 调节，而是通过高斯核标准差 $\sigma$ 控制。增大 $\sigma$ 意味着更强的模糊程度、更低的能量曲率，从而产生更强的引导效应。消融实验证实：增大 $\gamma_{\mathrm{seg}}$ 并不普遍改善 FID 和 CLIP Score，而增大 $\sigma$ 倾向于持续提升样本质量且无饱和现象（Figure 6）。这一机制解耦了引导强度与质量退化风险，是 SEG 实现 Pareto 改进的关键。

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_JK728xy8G7/figures/013_Figure_12.jpg]]
*Figure 12: Comparison between query and key blur across different values of σ*

## 实验与关键发现

### 无条件生成：Pareto 改进的量化证据

SEG 在无条件生成任务上实现了对 vanilla SDXL 以及现有无条件引导方法的显著超越，且不引入典型的副作用。Table 1 汇总了 MS-COCO 2014 验证集 30k 图像上的核心指标对比。

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_JK728xy8G7/figures/004_Table_1.jpg]]
*Table 1: Quantitative comparison of SEG with vanilla SDXL [35], SAG [17], and PAG [1] for unconditional generation*

**瓶颈突破**：Vanilla SDXL 在无条件设置下 FID 高达 129.496，生成质量极差。现有方法 **SAG** 和 **PAG** 分别将 FID 降至 106.683 和 105.271，但代价是与原始输出的 LPIPS 偏离度较大（SAG 的 LPIPS_vgg 为 0.706），表明这些启发式引导方法引入了明显的分布偏移和伪影。

**SEG 的 Pareto 改进**：当 $\sigma \to \infty$ 时，SEG 将 FID 大幅降至 88.215，同时 LPIPS_vgg 仅为 0.536——在显著提升图像质量的同时，保持了与 vanilla SDXL 原始输出更高的相似度。这构成了对 SAG 和 PAG 的严格 Pareto 改进：FID 更低且 LPIPS 更低（偏离更小）。在 $\sigma = 10$ 的实用设置下，FID 为 95.316，LPIPS_vgg 进一步降至 0.522，同样优于所有基线。

**机制解读**：这一 Pareto 改进源于 SEG 的核心设计——通过高斯模糊降低注意力能量景观的曲率，而非像 SAG/PAG 那样直接扰动或替换注意力图。曲率降低使得引导信号更加平滑，避免了过度锐化或饱和等副作用。

### 文本条件生成：σ 控制质量，γ 保持固定

Table 2 展示了在文本条件生成下，不同 $\sigma$ 对生成指标的影响（固定 $\gamma_{\text{seg}} = 3.0$，与 PAG 相同）。

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_JK728xy8G7/figures/006_Table_2.jpg]]
*Table 2: Text-conditional sampling with different σ*

**单调改善趋势**：随着 $\sigma$ 从 1.0 增大到 $\infty$，FID 从 53.423（vanilla，无 CFG）单调下降至 26.169，CLIP Score 从 0.271 提升至 0.292。这表明增大高斯模糊程度持续改善图像的真实性和文本对齐度。

**代价与权衡**：LPIPS_alex 从 0.295 上升至 0.440，说明更强的平滑引导会导致输出与原始分布的偏离增大。但这一偏离是有益的——它对应着质量的提升，而非 SAG/PAG 中出现的细节平滑或颜色偏移等有害副作用。

**关键设计验证**：论文强调，图像质量应由 $\sigma$ 而非 $\gamma_{\text{seg}}$ 控制。这一设计选择使得 SEG 的调参空间更加正交：$\gamma_{\text{seg}}$ 固定为合理值（3.0），用户仅通过调节 $\sigma$ 即可在保真度和质量之间进行可控权衡。

### 消融研究：γ_seg 与 σ 的作用解耦

Figure 6 的消融实验验证了 SEG 中两个关键超参数的不同角色。

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_JK728xy8G7/figures/007_Figure_6.jpg]]
*Figure 6: Ablation study on*

**γ_seg 的非单调效应**：增大引导尺度 $\gamma_{\text{seg}}$ 并不普遍改善 FID 和 CLIP Score。这与 CFG 中增大引导尺度通常提升质量但引入饱和的行为不同，也与 PAG 中需要精细调节引导尺度的经验形成对比。

**σ 的单调控制**：增大 $\sigma$ 倾向于单调改善样本质量和合理性。这支持了论文的核心主张——能量曲率的降低程度（由 $\sigma$ 控制）是影响生成质量的主导因素，而非引导信号的强度（由 $\gamma_{\text{seg}}$ 控制）。

**实践指导**：基于消融结果，论文在所有实验中将 $\gamma_{\text{seg}}$ 固定为 3.0，仅通过 $\sigma$ 控制效果。这简化了 SEG 的实际使用，避免了多维超参数搜索。

### SEG 与 CFG 的协同效应

SEG 可以与 CFG 联合使用，进一步提升条件生成的质量。联合引导的反向 SDE 为：

$$d \mathbf{x} = [ \mathbf{f} ( \mathbf{x} , t ) - g ( t )^{2} ( ( 1 - \gamma_{\text{cfg}} + \gamma_{\text{seg}} ) \mathbf{s}_{\theta} ( \mathbf{x} , t ) + \gamma_{\text{cfg}} \mathbf{s}_{\theta} ( \mathbf{x} , t , c ) - \gamma_{\text{seg}} \tilde{\mathbf{s}}_{\theta} ( \mathbf{x} , t ) ) ] d t + g ( t ) d \bar{\mathbf{w}}$$

Figure 15–19 展示了 SEG 与 CFG 组合的实验结果。SEG 在 CFG 的基础上进一步改善了图像的真实性和细节丰富度，表明两种引导机制具有互补性——CFG 利用条件信息进行引导，而 SEG 通过平滑能量景观提升无条件预测的质量。

### 定性对比：副效应的消除

Figure 5 的定性对比揭示了 SEG 相对于 SAG 和 PAG 的关键优势：

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_JK728xy8G7/figures/005_Figure_5.jpg]]
*Figure 5: Qualitative comparison of SEG with vanilla SDXL [35], SAG [17], and PAG [1]*

- **SAG** 生成的图像存在明显的细节平滑和纹理丢失，这与 SAG 直接模糊输入像素的操作一致。
- **PAG** 虽然改善了结构，但倾向于引入颜色偏移和过度饱和，源于其用恒等注意力图替换原始注意力的粗暴策略。
- **SEG** 在提升结构合理性和细节丰富度的同时，保持了自然的色彩和纹理，无明显的饱和或平滑伪影。这归因于 SEG 仅在注意力权重层面进行高斯平滑，而非直接操作像素或替换注意力图。

### 失败模式与局限性

尽管 SEG 在多数场景下表现优异，论文指出了以下局限：

1. **基线依赖**：SEG 的效果依赖于基线模型（SDXL）的能力。若基线模型本身存在严重缺陷，SEG 的平滑引导可能无法根本性地修复这些问题。
2. **时序注意力未验证**：SEG 尚未在视频生成或多视图扩散模型的时序注意力机制上进行验证，其在时序维度上的行为仍是开放问题。
3. **偏见放大风险**：论文明确指出，SEG 提升生成质量的同时，可能无意中放大基线模型中已存在的社会偏见或有害刻板印象。目前缺乏专门的公平性或偏见评估实验，这一风险需要在实际部署中谨慎对待。
4. **计算开销**：虽然通过模糊查询矩阵（Proposition 3.1）避免了直接模糊注意力权重的二次复杂度，但额外的模糊操作和双前向传播（原始预测 + 平滑预测）仍会带来一定的计算开销。论文未提供详细的推理时间对比数据。

## 定位与知识库关联

### 无条件引导方法的演进与SEG的定位

扩散模型的无条件引导（unconditional guidance）旨在提升生成质量，同时避免分类器自由引导（CFG）对文本条件的依赖。SEG之前的代表性工作主要包括两条技术路线：

- **Self-Attention Guidance (SAG)**：通过对注意力图进行模糊处理来扰动输入像素，并将模糊前后的预测差异作为引导信号。该方法缺乏明确的数学基础，且容易引入细节平滑和颜色偏移等副作用。
- **Perturbed-Attention Guidance (PAG)**：用恒等注意力图替换原始注意力图，构造扰动预测用于引导。PAG同样属于启发式设计，在无条件生成中FID为105.271，较vanilla SDXL（129.496）有所改善，但仍存在饱和与质量次优的问题。

SEG与上述方法的核心差异在于**数学基础的建立**。SEG首次将自注意力操作形式化为能量最小化步骤——定义自注意力权重矩阵 $A = QK^\top$ 的能量函数为逐查询位置的负log-sum-exp：

$$E ( \mathbf { A } ) : = \sum _ { i = 1 } ^ { H } \sum _ { j = 1 } ^ { W } E ^ { \prime } ( \mathbf { a } _ { : ( i , j ) } ) , \quad E ^ { \prime } ( \mathbf { a } ) : = - \mathrm { l s e } \left( \mathbf { a } \right) = - \log \left( \sum _ { k = 1 } ^ { H } \sum _ { l = 1 } ^ { W } e ^ { a _ { ( k , l ) } } \right)$$

基于此能量视角，SEG揭示了高斯模糊注意力权重可以减弱底层能量函数的高斯曲率（Theorem 3.1），从而将模糊后的预测作为曲率降低的“无条件”预测，用于构造引导信号。这一理论框架使得SEG在无条件生成中实现了FID 88.215，较PAG（105.271）和SAG（106.683）均有显著提升，同时LPIPS偏离度更低（0.536 vs. PAG的0.542），实现了Pareto改进。

### 控制机制的创新：从引导尺度到能量曲率

现有引导方法（包括CFG和PAG）通常通过调节引导尺度参数 $\gamma$ 来控制效果，但增大 $\gamma$ 往往导致饱和、颜色偏移等副作用。SEG引入了一个独立的控制维度——高斯模糊的标准差 $\sigma$，用于调节能量景观的曲率。

消融实验（Figure 6）表明：增大引导尺度 $\gamma_{seg}$ 并不普遍改善FID和CLIP分数；而增大 $\sigma$ 则持续提升样本质量且无饱和现象。因此，SEG将图像质量的控制权从引导尺度转移到 $\sigma$，固定 $\gamma_{seg}=3.0$（与PAG相同），仅通过调节 $\sigma$ 来控制效果。这一解耦设计使得SEG在文本条件生成中，随着 $\sigma \to \infty$，FID从53.423降至26.169，CLIP Score从0.271提升至0.292，同时保持可控的LPIPS偏离。

### 计算效率与实现兼容性

SEG的高斯模糊操作若直接作用于 $QK^\top$ 矩阵将引入二次复杂度。论文通过Proposition 3.1证明了模糊查询矩阵 $Q$ 等价于模糊整个注意力权重矩阵：

$$G \ast ( \mathbf { Q K } ^ { \top } ) = ( G \ast \mathbf { Q } ) \mathbf { K } ^ { \top }$$

这一等价性使得SEG仅需对查询矩阵执行2D高斯模糊，计算开销极低。此外，SEG与PAG共享相同的注意力层选择（mid-blocks）和引导尺度，可直接替换现有无条件引导方法。SEG还可与CFG联合使用，组合采样公式为：

$$d \mathbf { x } = [ \mathbf { f } ( \mathbf { x } , t ) - g ( t ) ^ { 2 } ( ( 1 - \gamma _ { \mathrm { c f g } } + \gamma _ { \mathrm { s e g } } ) \mathbf { s } _ { \theta } ( \mathbf { x } , t ) + \gamma _ { \mathrm { c f g } } \mathbf { s } _ { \theta } ( \mathbf { x } , t , c ) - \gamma _ { \mathrm { s e g } } \tilde { \mathbf { s } } _ { \theta } ( \mathbf { x } , t ) ) ] d t + g ( t ) d \mathbf { \bar { w } }$$

### 适用边界与已知局限

1. **基线依赖**：SEG的效果依赖于基线扩散模型的能力。论文所有实验基于SDXL，若基线模型（如SD 1.5）的生成能力有限，SEG的提升幅度可能受限。这一依赖关系尚未在不同规模的模型上进行系统性验证。

2. **注意力类型的覆盖范围**：当前SEG仅应用于空间自注意力（spatial self-attention），尚未在时序注意力（temporal attention）上进行验证。视频生成和多视图扩散模型中的时序注意力机制是否同样受益于能量曲率平滑，属于开放问题。

3. **架构普适性**：SEG的理论建立在自注意力的能量函数定义之上，对于其他注意力变体（如线性注意力、FlashAttention）或非注意力架构（如纯卷积扩散模型）的适用性未经验证。此外，DiT等基于Transformer的扩散模型架构是否兼容SEG的查询模糊策略，也需要进一步研究。

4. **社会偏见放大的风险**：论文明确指出，SEG在提升生成质量的同时，可能无意中放大基线模型中已存在的刻板印象或有害偏见。目前未进行专门的公平性或偏见评估实验，这一风险需要在使用中加以警惕。

### 开放问题

- SEG是否可以扩展应用于视频扩散模型中的时序注意力机制，以提升时序一致性和视觉质量？
- 对于不同结构（如DiT）或不同任务（如NLP中的注意力模型），SEG的能量曲率平滑框架是否具有普适性？
- 能否设计更精细的能量函数或自适应模糊策略，以进一步解耦质量提升与副作用，并量化偏见放大的风险？
- 在更广泛的扩散模型规模（从SD 1.5到SDXL再到更大模型）上，SEG的性能增益是否具有单调性？

## 原文 PDF

![[paperPDFs/NeurIPS_2024/Smoothed_Energy_Guidance_Guiding_Diffusion_Models_with_Reduced_Energy_Curvature_of_Attention.pdf]]
