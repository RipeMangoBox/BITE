---
title: "D$^2$-FOSA: Dual-Diffusion Guided EEG-to-Image Reconstruction with Frequency-Oriented Semantic Alignment"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/D_2_FOSA_Dual_Diffusion_Guided_EEG_to_Image_Reconstruction_with_Frequency_Oriented_Semantic_Alignment.pdf
project_link: null
code_link: null
aliases:
- DF
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
- topic/representation_self_supervised_transfer
core_operator: 在状态空间模型中显式植入可学习的振荡模式（FOMamba），并结合双向扩散循环一致性正则（DDLG）强化EEG-图像潜空间对齐。
primary_logic: 通过结构化状态矩阵建模神经振荡的衰减与旋转，同时用生成式循环一致性约束替代纯判别式对比学习，可大幅提升EEG到图像的语义对齐与重建质量。
claims:
- FOMamba选择性放大Beta (13-30 Hz)和Gamma (30-60 Hz)频段，而标准Mamba抑制这些高频成分。
- 完整的双向DDLG将FOMamba的检索Top-1从31.18%提升至37.96%，相对提升约6.8个百分点。
- 在THINGS-EEG重建任务上，D2-FOSA比MB2C降低超过17 FID。
- THINGS-EEG 上 200-way zero-shot retrieval Top-1 (intra-subject avg) = 38.0
---

# D$^2$-FOSA: Dual-Diffusion Guided EEG-to-Image Reconstruction with Frequency-Oriented Semantic Alignment

> [!tip] 核心洞察
> 通过结构化状态矩阵建模神经振荡的衰减与旋转，同时用生成式循环一致性约束替代纯判别式对比学习，可大幅提升EEG到图像的语义对齐与重建质量。

| 字段 | 内容 |
|------|------|
| 中文题名 | D²-FOSA：双扩散引导的脑电图到图像重建与频率导向语义对齐 |
| 英文题名 | D$^2$-FOSA: Dual-Diffusion Guided EEG-to-Image Reconstruction with Frequency-Oriented Semantic Alignment |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Yu_D2-FOSA_Dual-Diffusion_Guided_EEG-to-Image_Reconstruction_with_Frequency-Oriented_Semantic_Alignment_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion #topic/representation_self_supervised_transfer |
| Method | D2-FOSA |
| Dataset | THINGS-EEG, THINGS-MEG, EEGImageNet |

> [!tip] 效果简介
> - THINGS-EEG 上，200-way zero-shot retrieval Top-1 (intra-subject avg) 38.0 vs 37.2 (VE-SDN) (+0.8)。
> - THINGS-MEG 上，200-way zero-shot retrieval Top-1 (intra-subject avg) 27.5 vs 26.7 (UBP) (+0.8)。
> - EEGImageNet 上，Top-1 retrieval accuracy 31.05 vs 19.15 (NICE) (+11.9)。

## 概要

**问题瓶颈**：传统脑电图（EEG）到图像的重建方法存在两个关键缺陷。其一，标准EEG编码器（如Mamba或Transformer）忽略频率特定的神经振荡动态，无法有效捕捉Beta（13–30 Hz）和Gamma（30–60 Hz）等与视觉感知密切相关的节律信息。其二，跨模态对齐通常仅依赖对比损失（如InfoNCE），缺乏生成式约束，导致语义一致性弱、重建保真度差。

**核心方法**：本文提出D²-FOSA（Dual-Diffusion Guided EEG-to-Image Reconstruction with Frequency-Oriented Semantic Alignment），通过两个关键设计解决上述瓶颈：
1. **频率感知时序编码器FSTDE**：以FOMamba为核心，将状态空间模型的状态矩阵参数化为块对角2×2振荡子块，显式建模阻尼振荡模式，选择性放大Beta和Gamma频段的神经信号（Figure 4、Figure 5）。
2. **双向扩散循环一致性对齐DDLG**：在EEG-图像共享潜空间中，通过EEG到图像（E2I-DLG）和图像到EEG（I2E-DLG）的双向条件扩散，以生成式循环一致性正则替代纯判别式对比学习，强化跨模态语义对齐（Figure 2）。

**方法定位**：D²-FOSA属于EEG到图像检索与重建任务线，与**BraVL**（Du et al., TPAMI 2023）、**NICE**系列（Song et al., ICLR 2024）、**ATM**（Li et al., NeurIPS 2024）、**MB2C**（Wei et al., ACM MM 2024）、**UBP**（Wu et al., CVPR 2025）等一脉相承，但在编码器骨干（状态空间振荡建模）和对齐机制（扩散循环一致性）两个关键位上做出实质性改进。

**主要结果**：
- 在THINGS-EEG基准上，200路零样本检索Top-1准确率达**38.0%**，略优于VE-SDN的37.2%（Table 1）；重建FID为**146.33**，较MB2C降低超过17个点（Abstract, Table 3）。
- 在THINGS-MEG和EEGImageNet上，检索Top-1分别达**27.5%**和**31.05%**，较最强基线分别提升0.8和11.9个百分点（Table 2）。
- 消融实验表明，FOMamba单独使用即达31.18% Top-1，显著优于标准Mamba（27.75%）和Transformer（25.35%）；完整DDLG进一步将Top-1推升至**37.96%**，相对提升约6.8个百分点（Table 4, Section 4.7）。

### 问题背景：从脑信号中解码视觉感知

从非侵入式脑信号（如EEG、MEG）中解码人类视觉体验，是神经科学与人工智能交叉领域的核心挑战。这一任务不仅有助于理解大脑的视觉表征机制，也为脑机接口、神经康复等应用提供了技术基础。近年来，随着大规模脑信号数据集的建立，如**THINGS-EEG**、**THINGS-MEG**和**EEGImageNet**，EEG到图像的重建与检索研究取得了显著进展。

### 现有方法的瓶颈

当前主流的EEG到图像重建方法通常遵循两阶段范式：首先通过对比学习将EEG特征与预训练视觉模型（如CLIP）的图像嵌入对齐，然后利用扩散模型从对齐后的嵌入生成图像。然而，这一范式存在两个关键瓶颈：

**瓶颈一：EEG编码器忽略频率特定的神经振荡动态。** 神经科学证据表明，不同的视觉刺激会诱发特定频段的神经振荡——Beta频段（13-30 Hz）与视觉注意和特征绑定密切相关，Gamma频段（30-60 Hz）则参与视觉感知的整合与意识形成。然而，现有的EEG编码器（如标准Mamba或Transformer）采用通用的时序建模策略，未显式建模这些频率特定的振荡模式。如Figure 4和Figure 5所示，标准Mamba实际上会抑制Beta和Gamma频段的信号功率，而FOMamba则选择性地放大这些关键频段，揭示了现有方法在频率感知上的结构性缺陷。

**瓶颈二：跨模态对齐仅依赖对比损失，语义一致性弱。** 现有方法普遍采用InfoNCE对比损失将EEG嵌入拉向图像嵌入空间。这种纯判别式对齐策略虽然简单，但缺乏对跨模态语义一致性的显式约束——它只要求配对样本在嵌入空间中接近，却无法保证EEG嵌入能够忠实地重建出对应的图像语义。这导致生成阶段容易出现语义漂移，重建保真度受限。

### 本文动机与核心思路

针对上述瓶颈，D²-FOSA提出两个核心改进：

1. **频率导向的时序编码**：设计频率感知的FOMamba模块，在状态空间模型（SSM）框架中显式植入可学习的振荡模式。通过将传统Mamba的对角状态矩阵替换为块对角$2 \times 2$振荡子块（见Eq. (2)），每个子块以阻尼因子$\rho_k$和角频率$\omega_k$参数化，使模型能够自适应地捕捉并放大Beta和Gamma等关键频段的神经振荡动态。

2. **生成式循环一致性对齐**：引入双扩散潜变量生成器（DDLG），包含EEG到图像嵌入（E2I-DLG）和图像到EEG嵌入（I2E-DLG）两个对称的条件扩散过程。这一设计将传统的单向对比对齐扩展为双向生成式循环一致性约束，迫使EEG嵌入不仅与图像嵌入接近，更能通过反向扩散过程精确重建对方模态的嵌入，从而在潜空间中建立更紧密、更一致的语义对应关系。

消融实验（Table 4）验证了这两项设计的有效性：FOMamba单独使用即达到31.18%的Top-1检索准确率，显著优于标准Mamba的27.75%；完整的双向DDLG进一步将FOMamba的性能提升至37.96%，相对提升约6.8个百分点，充分证明了生成式循环一致性对齐对跨模态检索的关键作用。

## 核心方法与创新机理

D²-FOSA 的创新核心在于对 EEG 到图像跨模态对齐中两个根本瓶颈的系统性突破：**频率盲区的时序建模**与**纯判别式对齐的语义脆弱性**。传统方法将 EEG 视为通用时序信号，使用标准 Transformer 或 Mamba 编码，忽略了神经振荡中 Beta (13–30 Hz) 和 Gamma (30–60 Hz) 等频段承载的丰富语义信息；同时仅依赖对比损失（InfoNCE）拉近跨模态嵌入，缺乏生成式约束，导致语义一致性弱、重建保真度差。

### 1. 频率感知的振荡状态空间模型（FOMamba）

标准 Mamba 的状态矩阵 $A$ 为对角形式，仅能建模单调衰减，本质上是频率盲的。FOMamba 将 $A$ 重构为块对角矩阵，每个 $2 \times 2$ 子块显式参数化一个阻尼振荡模式：

$$A _ { k } = \left[ { \begin{array} { l l } { - \rho _ { k } } & { - \omega _ { k } } \\ { \omega _ { k } } & { - \rho _ { k } } \end{array} } \right]$$

其中 $\rho_k$ 为阻尼因子，$\omega_k$ 为角频率，对应复共轭特征值 $-\rho_k \pm i\omega_k$。这一参数化使模型具备频率选择性——每个子块天然倾向于放大特定频段的信号。为进一步增强频率自适应能力，FOMamba 引入可学习的对数频率偏置 $F_{\mathrm{log},k}$，通过 softplus 激活动态调整振荡器频率：

$$\tilde { \omega } _ { k } = \mathrm { s o f t p l u s } ( \omega _ { k } + F _ { \mathrm { l o g } , k } )$$

离散化时，通过矩阵指数闭合解精确保留旋转与衰减动态：

$$A _ { d , k } = e ^ { - \rho _ { k } \Delta t } \left[ \begin{array} { c c } { \cos ( \tilde { \omega } _ { k } \Delta t ) } & { - \sin ( \tilde { \omega } _ { k } \Delta t ) } \\ { \sin ( \tilde { \omega } _ { k } \Delta t ) } & { \cos ( \tilde { \omega } _ { k } \Delta t ) } \end{array} \right]$$

**实验证据**：功率谱密度分析（Figure 4）和时频分析（Figure 5）证实，FOMamba 选择性放大 Beta 和 Gamma 频段信号功率，而标准 Mamba 抑制这些高频成分。消融实验中，FOMamba 单独使用即达到 31.18% 的 Top-1 检索准确率，显著优于标准 Mamba 的 27.75% 和 Transformer 的 25.35%（Table 4）。

### 2. 双向扩散循环一致性对齐（DDLG）

传统方法仅依赖对比损失拉近 EEG 嵌入 $\mathbf{X}_e$ 与图像嵌入 $\mathbf{X}_i$：

$$\mathcal { L } _ { \mathrm { a l i g n } } = - \log \frac { \exp ( \sin ( \mathbf { X } _ { e } , \mathbf { X } _ { i } ) / \tau ) } { \sum _ { j } \exp ( \sin ( \mathbf { X } _ { e } , \mathbf { X } _ { i } ^ { j } ) / \tau ) }$$

这种纯判别式对齐缺乏生成式约束，无法保证嵌入空间的语义一致性。D²-FOSA 提出 DDLG 模块，包含两个对称的条件扩散过程：

- **E2I-DLG**：以 EEG 嵌入为条件，通过反向扩散生成图像嵌入，实现前向跨模态翻译。
- **I2E-DLG**：以图像嵌入为条件，通过反向扩散重建 EEG 嵌入，构成循环一致性约束。

两个扩散过程的去噪步骤统一为：

$$p_{\theta}(\mathbf{z}_{t-1} \vert \mathbf{z}_t, \mathbf{c}) = \mathcal{N}(\mathbf{z}_{t-1}; \mu_{\theta}(\mathbf{z}_t, \mathbf{c}, t), \sigma_t^2 \mathbf{I})$$

总训练目标联合优化对比损失和双扩散损失：

$$\mathcal { L } _ { \mathrm { t o t a l } } = \mathcal { L } _ { \mathrm { a l i g n } } + \lambda _ { \mathrm { E 2 I } } \mathcal { L } _ { \mathrm { E 2 I } } + \lambda _ { \mathrm { I 2 E } } \mathcal { L } _ { \mathrm { I 2 E } }$$

其中 $\lambda_{\mathrm{E2I}}$ 和 $\lambda_{\mathrm{I2E}}$ 均设为 0.5。

**实验证据**：完整的双向 DDLG 将 FOMamba 的检索 Top-1 从 31.18% 提升至 37.96%，相对提升约 6.8 个百分点（Table 4），证明生成式循环一致性约束对跨模态语义对齐至关重要。

### 3. 与 baseline 的关键差异（Changed Slots）

| 模块 | Baseline 方案 | D²-FOSA 方案 | 创新本质 |
|------|-------------|-------------|---------|
| EEG 编码器骨干 | 标准 Mamba 或 Transformer | FSTDE（FOMamba + 神经图提取器 + 时空特征提取器） | 从频率盲区到振荡感知 |
| 跨模态对齐损失 | 纯 InfoNCE 对比损失 | 对比损失 + DDLG 双向扩散循环一致性 | 从判别式到生成式约束 |
| 状态矩阵参数化 | SSM 中对角状态矩阵 | 块对角 $2 \times 2$ 振荡模式 + 可学习对数频率偏置 | 从单调衰减到频率选择性 |
| 图像生成骨干 | 解码器端扩散（如 MinD-Vis 风格） | DDLG 反向过程 + 冻结 SDXL + IP-Adapter | 从端到端训练到预训练先验复用 |

### 4. 阻尼因子的关键作用

FOMamba 中阻尼因子 $\rho_k$ 的上下界对性能有显著影响。敏感性分析（Figure 11）表明：
- 上界 $\rho_{\max}=0.995$ 时性能最优，过低的 $\rho_{\max}$ 会过度抑制慢衰减模式。
- 下界 $\rho_{\min} \approx 0.7$ 时增益明显，说明保留适当的慢衰减模式有利于建模 EEG 信号中的长程依赖。

这一发现揭示了神经振荡建模中“衰减速率”作为关键控制旋钮的作用——过快衰减丢失长程信息，过慢衰减则引入噪声。

D²-FOSA 提出了一套**双扩散引导的 EEG‑到‑图像重建框架**，其核心设计思想是将 EEG 信号编码、跨模态语义对齐与图像生成统一在一个**双向循环一致性**的潜空间中。整个框架在训练与推理阶段呈现不同的信息流，但共享相同的编码器与对齐模块。

### 训练阶段：双向潜空间对齐

训练阶段的目标是建立一个 EEG 嵌入与图像嵌入之间**语义一致且可双向翻译**的共享潜空间。该阶段包含三条并行的信息通路：

1. **EEG 编码通路**：原始 EEG 信号首先经过**频率‑时空动态编码器（FSTDE）**，依次通过频率导向 Mamba（FOMamba）捕获神经振荡动态、神经图结构提取器建模电极拓扑、时空特征提取器融合局部模式，最终经投影 MLP 得到 EEG 嵌入 $\mathbf{X}_e$。
2. **图像编码通路**：对应图像经冻结的 CLIP ViT 编码后通过投影 MLP 得到图像嵌入 $\mathbf{X}_i$。
3. **跨模态对齐与生成正则**：$\mathbf{X}_e$ 与 $\mathbf{X}_i$ 之间同时施加**对比对齐损失** $\mathcal{L}_{\mathrm{align}}$（InfoNCE 形式）和**双扩散潜变量生成器（DDLG）的循环一致性约束**。DDLG 由对称的 EEG‑到‑图像扩散模块（E2I‑DLG）和图像‑到‑EEG 扩散模块（I2E‑DLG）组成：E2I‑DLG 以 $\mathbf{X}_e$ 为条件通过反向扩散重建图像嵌入，I2E‑DLG 以 $\mathbf{X}_i$ 为条件重建 EEG 嵌入，二者共同构成生成式正则项。

总训练目标为三者的加权联合优化：

$$\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{align}} + \lambda_{\mathrm{E2I}} \mathcal{L}_{\mathrm{E2I}} + \lambda_{\mathrm{I2E}} \mathcal{L}_{\mathrm{I2E}}$$

其中 $\lambda_{\mathrm{E2I}}$ 和 $\lambda_{\mathrm{I2E}}$ 均设为 0.5，以平衡对比判别与生成循环一致性。

### 推理阶段：EEG 到像素图像的生成流水线

推理阶段的目标是从一段 EEG 信号直接合成对应的视觉图像。其流程如下：

1. **EEG 编码**：测试 EEG 信号经训练好的 FSTDE 编码为 EEG 嵌入 $\mathbf{X}_e$。
2. **潜空间翻译**：$\mathbf{X}_e$ 通过 E2I‑DLG 的条件反向扩散过程翻译为图像嵌入 $\mathbf{X}_i$，该过程由训练阶段学到的跨模态映射关系驱动。
3. **像素级图像生成**：翻译得到的 $\mathbf{X}_i$ 作为条件输入送入**冻结的 SDXL 管线**，通过 IP‑Adapter 引导预训练扩散模型完成从潜空间到像素空间的解码，最终输出重建图像。

### 模块间的依赖关系

从架构角度看，整个系统的关键模块依赖关系如下：

- **FSTDE** 是整个框架的感知基础，其内部的 FOMamba 通过块对角 $2 \times 2$ 振荡子块显式建模 Beta/Gamma 频段的神经振荡动态，为后续对齐提供频率感知的时序表示。
- **DDLG** 是连接 EEG 域与图像域的生成式桥梁，它不依赖额外的判别器，而是通过双向扩散的循环一致性直接在潜空间内强化跨模态语义对齐。
- **SDXL + IP‑Adapter** 作为冻结的解码器，仅负责将已对齐的图像嵌入转化为高保真像素图像，不参与跨模态训练。

这种“编码器‑对齐器‑解码器”的解耦设计使得各模块可独立优化与替换，同时**双向扩散的循环一致性约束**是连接 EEG 编码与图像生成的核心因果机制——消融实验表明，完整的双向 DDLG 将 FOMamba 的检索 Top‑1 从 31.18% 提升至 37.96%（相对提升约 6.8 个百分点），验证了生成式对齐对语义一致性的决定性作用。

![[assets/figures/papers/paper_list_l2459_https_openaccess_thecvf_com_content_CVPR2026_html_Yu_D2_FOSA_Dual_Diffus/figures/002_Figure_2.jpg]]
*Figure 2: Overall architecture of D2-FOSA. During training (top), EEG signals and images are projected into a shared latent space via contrastive learning. Meanwhile, two symmetric diffusion latent modules (E2I-DLG and I2E-DLG) reconstruct cross-modal embeddings to enforce generative consistency. In inference (bottom), EEG signals are encoded and translated to image embeddings*

### 3.1 频率导向状态空间模型（FOMamba）

传统状态空间模型（SSM）采用对角状态矩阵，无法显式建模神经振荡的衰减与旋转特性。FOMamba将状态矩阵 $\mathbf{A}$ 重新参数化为块对角结构，每个 $2 \times 2$ 子块显式表示一个阻尼振荡模式：

$$
\mathbf{A}_k = \begin{bmatrix} -\rho_k & -\omega_k \\ \omega_k & -\rho_k \end{bmatrix}
$$

其中 $\rho_k > 0$ 为阻尼因子，控制振荡衰减速率；$\omega_k$ 为角频率，决定振荡快慢。该矩阵的特征值为 $-\rho_k \pm i\omega_k$，天然对应复共轭对，恰好捕捉EEG信号中Beta（13-30 Hz）与Gamma（30-60 Hz）等节律的动态特性。

为赋予模型频率自适应能力，FOMamba引入可学习的对数频率偏置 $F_{\log,k}$，通过softplus激活动态调整振荡器频率：

$$
\tilde{\omega}_k = \mathrm{softplus}(\omega_k + F_{\log,k})
$$

连续时间状态空间方程 $\dot{\mathbf{h}}(t) = \mathbf{A}\mathbf{h}(t) + \mathbf{B}\mathbf{x}(t)$ 需离散化以适应序列处理。FOMamba利用矩阵指数精确求解离散状态矩阵 $\mathbf{A}_{d,k}$，完整保留旋转与指数衰减动态：

$$
\mathbf{A}_{d,k} = e^{-\rho_k \Delta t} \begin{bmatrix} \cos(\tilde{\omega}_k \Delta t) & -\sin(\tilde{\omega}_k \Delta t) \\ \sin(\tilde{\omega}_k \Delta t) & \cos(\tilde{\omega}_k \Delta t) \end{bmatrix}
$$

该闭合解由衰减因子 $e^{-\rho_k \Delta t}$ 与旋转矩阵相乘构成，避免了近似离散化带来的动态失真。实验验证：Figure 4与Figure 5显示FOMamba选择性放大Beta/Gamma频段功率，而标准Mamba抑制这些高频成分（置信度0.95）；阻尼因子上界 $\rho_{\max}=0.995$ 时性能最优，说明保留慢衰减模式对长程依赖建模至关重要（Figure 11，置信度0.9）。

### 3.2 频率-时空动态编码器（FSTDE）

FSTDE由三个层次化子模块级联构成，将原始EEG信号压缩为紧凑的语义嵌入 $\mathbf{X}_e$：

1. **FOMamba模块**：对多通道EEG时间序列进行频率感知的时序动态建模，选择性增强Beta/Gamma频段响应。
2. **神经图结构提取器**：基于图卷积网络（GCN）建模电极间的空间拓扑关系，聚合邻域信息产生空间增强特征 $\mathbf{H}_s$。
3. **时空特征提取器**：采用深度可分离卷积堆叠提取局部时空模式，最终经投影MLP输出EEG嵌入 $\mathbf{X}_e$。

### 3.3 双扩散潜空间生成器（DDLG）

DDLG在共享潜空间内施加生成式循环一致性约束，包含两个对称的条件扩散模块：

- **E2I-DLG**：以EEG嵌入 $\mathbf{X}_e$ 为条件，通过反向扩散过程 $p_\theta(\mathbf{z}_{t-1} | \mathbf{z}_t, \mathbf{X}_e)$ 生成图像嵌入 $\hat{\mathbf{X}}_i$。
- **I2E-DLG**：以图像嵌入 $\mathbf{X}_i$ 为条件，通过反向扩散过程生成EEG嵌入 $\hat{\mathbf{X}}_e$。

条件反向扩散的标准形式为：
$$
p_\theta(\mathbf{z}_{t-1} | \mathbf{z}_t, \mathbf{c}) = \mathcal{N}(\mathbf{z}_{t-1}; \boldsymbol{\mu}_\theta(\mathbf{z}_t, \mathbf{c}, t), \sigma_t^2 \mathbf{I})
$$

其中 $\mathbf{c}$ 为条件嵌入，$\boldsymbol{\mu}_\theta$ 为可学习的去噪均值函数。

### 3.4 联合优化目标

模型训练采用多目标联合优化。对比对齐损失基于InfoNCE拉近配对EEG-图像嵌入：

$$
\mathcal{L}_{\mathrm{align}} = -\log \frac{\exp(\sin(\mathbf{X}_e, \mathbf{X}_i) / \tau)}{\sum_j \exp(\sin(\mathbf{X}_e, \mathbf{X}_i^j) / \tau)}
$$

其中 $\sin(\cdot,\cdot)$ 为余弦相似度，$\tau$ 为可学习温度参数。DDLG的双向扩散损失 $\mathcal{L}_{\mathrm{E2I}}$ 与 $\mathcal{L}_{\mathrm{I2E}}$ 分别约束前向与反向生成的一致性。总损失为：

$$
\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{align}} + \lambda_{\mathrm{E2I}} \mathcal{L}_{\mathrm{E2I}} + \lambda_{\mathrm{I2E}} \mathcal{L}_{\mathrm{I2E}}
$$

权重 $\lambda_{\mathrm{E2I}}$ 与 $\lambda_{\mathrm{I2E}}$ 均设为0.5以平衡各方目标。消融实验证实：FOMamba单独使用即达31.18% Top-1检索准确率，完整双向DDLG将其提升至37.96%，相对提升约6.8个百分点（Table 4，置信度0.95），表明生成式循环一致性对齐对跨模态语义绑定具有决定性作用。

![[assets/figures/papers/paper_list_l2459_https_openaccess_thecvf_com_content_CVPR2026_html_Yu_D2_FOSA_Dual_Diffus/figures/003_Figure_3.jpg]]
*Figure 3: Architecture of our FSTDE. (a) The FOMamba core, where 2×2 blocks defined by frequency (ωk) and damping*

![[assets/figures/papers/paper_list_l2459_https_openaccess_thecvf_com_content_CVPR2026_html_Yu_D2_FOSA_Dual_Diffus/figures/004_Figure_4.jpg]]
*Figure 4: Power Spectral Density (PSD) comparison. Our FO-Mamba (red) selectively enhances signal power in the crucial Beta and Gamma frequency bands compared to the raw EEG and a baseline Mamba (blue)*

## 实验与关键发现

### 零样本检索主结果

D²-FOSA 在多个基准上进行了严格的零样本检索评估，所有对比方法均按统一条件重新实现和训练，并遵循留一被试交叉验证或单被试训练测试协议。

**THINGS-EEG 200路检索**（Table 1）：在受试者内平均 Top-1 准确率上，D²-FOSA 达到 **38.0%**，超越此前最优的 **VE-SDN**（Chen et al., arXiv 2024）的 37.2% 以及 **UBP**（Wu et al., CVPR 2025）的 37.0%。Top-5 准确率达到 70.7%，同样处于领先水平。这表明 FSTDE 的频率感知编码与 DDLG 的生成式循环一致性对齐能够有效捕获 EEG 信号中的细粒度视觉语义信息。

**THINGS-MEG 跨模态泛化**（Table 2）：在 MEG 数据的 200 路检索中，D²-FOSA 取得受试者内平均 Top-1 **27.5%**、Top-5 **55.7%**，均优于 UBP（26.7%/54.3%）和 VE-SDN（26.0%/53.0%）。MEG 信号具有与 EEG 不同的时空特性，该结果表明 FOMamba 的振荡模式建模具有一定的模态泛化能力。

**EEGImageNet 检索**（Table 2）：在更大规模类别空间下，D²-FOSA 的 Top-1 达到 **31.05%**，相较 **NICE**（Song et al., ICLR 2024）的 19.15% 提升 **约 11.9 个百分点**，相对提升幅度超过 60%。这一跨数据集的大幅领先说明 FSTDE 的频率选择性表示在更丰富的视觉语义空间中也具有显著优势。

### 图像重建质量评估

在 THINGS-EEG 数据集上（Table 3），D²-FOSA 取得了 **146.33** 的 FID，相比 **MB2C**（Wei et al., ACM MM 2024）的约 163.33 降低 **超过 17 个 FID**，相对改善约 10.4%。这一提升验证了 DDLG 通过双向扩散循环一致性将 EEG 嵌入更准确地对齐到 CLIP 语义空间，从而为 SDXL 生成管线提供更高质量的条件信号。定性结果（Figure 10）显示，D²-FOSA 能够从 EEG 信号中重建出与真实图像语义类别高度一致的多样本图像，成功捕获关键视觉属性。

![[assets/figures/papers/paper_list_l2459_https_openaccess_thecvf_com_content_CVPR2026_html_Yu_D2_FOSA_Dual_Diffus/figures/012_Table_3.jpg]]
*Table 3: Quantitative evaluation of EEG-to-image reconstruction quality on the ThingsEEG dataset*

### 频率选择性分析

Figure 4 的功率谱密度（PSD）对比揭示了 FOMamba 的核心工作机制：与原始 EEG 和标准 Mamba（蓝色）相比，FOMamba（红色）选择性地增强了 **Beta（13–30 Hz）和 Gamma（30–60 Hz）频段**的信号功率。标准 Mamba 实际上抑制了这些高频成分，而 FOMamba 通过 2×2 振荡子块的可学习阻尼-频率参数化，实现了对这些神经振荡相关频段的显式放大。

Figure 5 的时频分析进一步佐证了这一发现：FOMamba 输出的时频图在 Beta/Gamma 频段呈现更强的能量集中，差异图（Figure 5f）清晰显示了相对于原始信号的增强区域。这为“结构化状态矩阵建模神经振荡衰减与旋转”的核心洞察提供了直接的频谱证据。

### 消融实验

Table 4 的消融实验系统解耦了各模块的贡献（THINGS-EEG 数据集）：

![[assets/figures/papers/paper_list_l2459_https_openaccess_thecvf_com_content_CVPR2026_html_Yu_D2_FOSA_Dual_Diffus/figures/014_Table_4.jpg]]
*Table 4: Ablation study on the THINGS-EEG dataset. We evaluate the impact of the temporal selective module and our DDLG. ‘×‘ denotes no DDLG, ‘†‘ denotes using only the EEG-to-Image (E2I) part of DDLG, and*

**时序建模模块对比**：FOMamba 单独使用（无 DDLG）即达到 **31.18%** Top-1，显著优于标准 Mamba 的 27.75%（+3.43 个百分点）和 Transformer 的 25.35%（+5.83 个百分点）。这证明频率导向的振荡模式建模是性能提升的关键瓶颈突破，而非单纯的状态空间模型带来的增益。

**DDLG 的生成式对齐贡献**：完整的双向 DDLG（E2I-DLG + I2E-DLG）将 FOMamba 的 Top-1 从 31.18% 提升至 **37.96%**，相对提升约 **6.8 个百分点**（约 21.7% 相对增幅）。仅使用单向 E2I-DLG（† 标记）仅提升至 34.21%，表明 I2E-DLG 的反向循环一致性约束对语义对齐具有不可替代的作用。这一结果直接支撑了“用生成式循环一致性替代纯判别式对比学习”的核心主张。

**阻尼因子敏感性**（Figure 11）：阻尼因子上界 $\rho_{\max}=0.995$ 时模型性能最优，下界 $\rho_{\min}\approx 0.7$ 时增益明显。过小的 $\rho_{\max}$ 会过早衰减历史信息，而过大的 $\rho_{\min}$ 则无法有效滤除噪声——这验证了“保留慢衰减模式有利于建模长程依赖”的假设，同时也说明需要仔细约束衰减率以平衡记忆与遗忘。

### 潜在空间质量分析

t-SNE（Figure 7）和 UMAP（Figure 8）可视化显示，D²-FOSA 的 EEG 嵌入与对应图像嵌入在共享语义空间中形成了高度重叠的聚类结构。跨模态表示相似性矩阵（Figure 9a）呈现清晰的对角块结构，零样本检索混淆矩阵（Figure 9b）也展现出较强的对角线集中性。这些可视化结果从几何角度佐证了 DDLG 循环一致性约束对语义对齐的强化效果。

![[assets/figures/papers/paper_list_l2459_https_openaccess_thecvf_com_content_CVPR2026_html_Yu_D2_FOSA_Dual_Diffus/figures/008_Figure_7.jpg]]
*Figure 7: t-SNE visualization of latent features on the ThingsEEG dataset*

### 需人工验证的边界说明

- Table 3 中 MB2C 的 FID 值（约 163.33）基于摘要中“超过 17 FID 提升”反推，原文 Table 3 的精确数值需对照确认。
- 跨被试泛化性能的具体数值未在提供的分析中呈现，该方向属于论文提出的开放问题之一，实际跨被试表现需查阅原文完整结果表。

## 定位与知识库关联

### 1. 与基线方法的关系

D²-FOSA 处于 EEG-to-image 重建与检索这一新兴交叉领域，其核心贡献在于对 EEG 编码器和跨模态对齐机制的双重改造。为厘清其技术定位，以下从编码器架构和对齐策略两个维度，将 D²-FOSA 与代表性基线进行对比。

**EEG 编码器架构的演进。** 早期工作多采用纯 Transformer 或标准 SSM 作为时序编码骨干。例如 **BraVL**（Du et al., TPAMI 2023）和 **NICE** 系列（Song et al., ICLR 2024）使用 Transformer 编码 EEG 嵌入，但 Transformer 的自注意力机制对长序列 EEG 信号的计算开销较大，且不具备频率选择性建模能力。**ATM**（Li et al., NeurIPS 2024）引入了 Mamba 架构以提升长程依赖建模效率，但其状态矩阵采用对角参数化，本质上等价于独立的一维指数衰减模式，无法捕捉神经振荡中固有的旋转动态。D²-FOSA 的 FOMamba 模块通过将状态矩阵重构为块对角 $2 \times 2$ 振荡子块（Eq. 2），显式建模阻尼振荡模式，从而在架构层面赋予了频率选择性。实验表明，FOMamba 单独使用即可在 THINGS-EEG 200-way 检索上达到 31.18% Top-1，显著优于标准 Mamba 的 27.75% 和 Transformer 的 25.35%（Table 4），证实了结构化振荡建模的有效性。

**跨模态对齐策略的转变。** 从对齐损失的角度看，**BraVL**、**NICE**、**EEGClip**（Singh et al., WACV 2024）等方法均采用纯对比损失（InfoNCE）将 EEG 嵌入拉向 CLIP 图像空间。这种判别式对齐虽然简洁，但缺乏生成式约束，导致语义一致性较弱。**MB2C**（Wei et al., ACM MM 2024）和 **UBP**（Wu et al., CVPR 2025）在对比学习基础上加入了生成式组件，但未形成双向循环一致性。D²-FOSA 的关键创新在于引入 Dual Diffusion Latent Generator（DDLG），通过 E2I-DLG 和 I2E-DLG 两个对称的条件扩散模块，在共享潜空间中强制执行生成式循环一致性正则。消融实验（Table 4）直接量化了这一设计的贡献：完整的双向 DDLG 将 FOMamba 的检索 Top-1 从 31.18% 提升至 37.96%（相对提升约 6.8 个百分点），而仅使用单向 E2I-DLG 的提升幅度明显较小。这一证据链表明，生成式循环一致性约束是 D²-FOSA 性能增益的核心因果旋钮，而非单纯的编码器改进。

**图像生成骨干的差异。** 在重建端，早期方法如 MinD-Vis 风格的工作使用解码器端扩散模型直接从 EEG 嵌入生成图像。D²-FOSA 则采用 DDLG 将 EEG 嵌入翻译为图像嵌入后，通过冻结的 SDXL 管线配合 IP-Adapter 完成像素级生成（Figure 2）。这种“翻译+条件生成”的解耦设计使得 EEG 编码器的训练目标更聚焦于语义对齐，而图像生成质量可受益于大规模预训练扩散模型的先验知识。定量结果上，D²-FOSA 在 THINGS-EEG 重建任务上比 MB2C 降低超过 17 FID（Abstract, Table 3），验证了该设计选择的优势。

### 2. 适用边界与泛化能力

D²-FOSA 在多个基准上展现了跨数据集、跨模态的泛化潜力，但其适用边界也受限于若干因素。

**跨数据集表现。** 在 THINGS-EEG 的 200-way 零样本检索中，D²-FOSA 的受试者内平均 Top-1 达到 38.0%，略优于 **VE-SDN**（Chen et al., arXiv 2024）的 37.2%（Table 1）。在 THINGS-MEG 上，Top-1 为 27.5%，略高于 **UBP** 的 26.7%（Table 2）。值得注意的是，在 EEGImageNet 数据集上，D²-FOSA 的 Top-1 达到 31.05%，相比 **NICE** 的 19.15% 提升了约 11.9 个百分点（Table 2），显示出在更具挑战性的多类别场景下的显著优势。然而，这些结果均基于受试者内（intra-subject）训练-测试协议，跨受试者泛化能力尚未得到充分验证，是论文明确列出的开放问题之一。

**频率选择性的物理可解释性。** FOMamba 的频率选择性增强并非黑箱效应。功率谱密度分析（Figure 4）和时频分析（Figure 5）直接证实，FOMamba 选择性放大了 Beta（13-30 Hz）和 Gamma（30-60 Hz）频段的信号功率，而标准 Mamba 对这些高频成分表现为抑制。这与神经科学中 Beta/Gamma 节律与视觉感知、注意加工密切相关的认知一致，为方法的物理可解释性提供了支撑。阻尼因子的敏感性分析（Figure 11）进一步揭示了关键超参数的作用边界：上界 $\rho_{\max}=0.995$ 时性能最优，下界 $\rho_{\min}\approx 0.7$ 时增益明显，说明保留慢衰减模式有利于建模 EEG 信号中的长程依赖。

### 3. 局限与开放问题

尽管 D²-FOSA 在检索和重建指标上取得了显著提升，论文和实验证据暴露了以下局限和待解问题。

**计算效率。** DDLG 模块包含两个对称的条件扩散过程，训练和推理时的计算开销显著高于纯对比学习方法。论文将“如何提升计算效率”列为开放问题之一，但未提供具体的复杂度分析或加速方案。在实际部署中，双扩散的迭代去噪步骤可能成为实时 BCI 应用的瓶颈，需要手动验证具体延迟数据。

**跨被试泛化。** 所有报告结果均基于受试者内协议，即训练和测试数据来自同一被试。EEG 信号的个体差异性极强（电极位置、阻抗、认知状态等），FOMamba 学习到的频率模式是否能在新被试上直接迁移，尚无实验证据。论文将“更好的跨被试泛化”列为第二个开放问题，但未给出初步探索或失败案例分析。

**低频与高频的权衡。** 虽然 FOMamba 对 Beta/Gamma 频段的增强是优势，但 Delta（0.5-4 Hz）和 Theta（4-8 Hz）频段在情感加工、记忆编码等任务中同样携带重要信息。当前设计是否过度抑制了低频成分，以及这种抑制在不同认知任务下是否鲁棒，缺乏消融分析。

**重建质量的语义保真度。** 尽管 FID 指标显著优于 MB2C，但 146.33 的绝对值仍偏高，表明重建图像与真实图像在低级纹理和细节上存在较大差距。定性结果（Figure 10）显示模型能捕获语义类别和大致视觉属性，但精细结构和背景细节的还原能力有限。这与 SDXL 管线以语义条件而非像素级监督的方式生成图像有关，本质上是一种语义重建而非像素重建。

**对比基线的公平性。** 论文声明所有对比方法均按统一条件重新实现和训练（Section 4.2），且遵循标准交叉验证协议，这在一定程度上保证了实验公平性。但部分基线（如 MB2C 的 FID 值标注为“estimated”）的具体复现细节需要手动核实原始论文以确认比较的严格对等性。

## 原文 PDF

![[paperPDFs/CVPR_2026/D_2_FOSA_Dual_Diffusion_Guided_EEG_to_Image_Reconstruction_with_Frequency_Oriented_Semantic_Alignment.pdf]]
