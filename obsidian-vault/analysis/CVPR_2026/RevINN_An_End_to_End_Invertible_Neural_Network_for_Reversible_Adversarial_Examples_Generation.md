---
title: "RevINN: An End-to-End Invertible Neural Network for Reversible Adversarial Examples Generation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/RevINN_An_End_to_End_Invertible_Neural_Network_for_Reversible_Adversarial_Examples_Generation.pdf
project_link: null
code_link: "https://github.com/WongJaylen/RevINN"
aliases:
- RevINN
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: RevINN利用可逆神经网络在小波域内对图像自身的高低频分量进行交叉动态调制，将对抗扰动生成与可逆恢复统一在单阶段网络中，从而消除了额外嵌入导致的质量退化。
primary_logic: 通过可逆信息交换机制，在图像低频（结构）和高频（细节）子带间建立双向调制：CFMA模块实现粗粒度的交叉频率攻击，HFPE模块对三个高频子带进行细粒度三支路增强，最终经由逆小波变换生成RAE；整个过程不依赖外部代理模型信息，仅利用图像内在频率特性，因此既能保证攻击强度，又可通过逆过程无损恢复原始图像。
claims:
- RevINN在PSNR vs ASR空间中同时达到高视觉质量和高攻击成功率，显著优于所有两阶段方法。
- 在VGG19上非目标攻击成功率高达95.3%，在DenseNet121上达98.3%，远超其他对比方法。
- RAE的平均PSNR达到46.39dB，超过其他方法6dB以上。
- 恢复图像的SSIM接近1，PSNR高达58.94dB，表明近乎无损的复原。
---

# RevINN: An End-to-End Invertible Neural Network for Reversible Adversarial Examples Generation

> [!tip] 核心洞察
> 通过可逆信息交换机制，在图像低频（结构）和高频（细节）子带间建立双向调制：CFMA模块实现粗粒度的交叉频率攻击，HFPE模块对三个高频子带进行细粒度三支路增强，最终经由逆小波变换生成RAE；整个过程不依赖外部代理模型信息，仅利用图像内在频率特性，因此既能保证攻击强度，又可通过逆过程无损恢复原始图像。

| 字段 | 内容 |
|------|------|
| 中文题名 | RevINN：一种用于可逆对抗样本生成的端到端可逆神经网络 |
| 英文题名 | RevINN: An End-to-End Invertible Neural Network for Reversible Adversarial Examples Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Huang_RevINN_An_End-to-End_Invertible_Neural_Network_for_Reversible_Adversarial_Examples_CVPR_2026_paper.html) · [Code](https://github.com/WongJaylen/RevINN) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | RevINN |
| Dataset | ImageNet, VGG19, ImageNet, DenseNet121, ImageNet, RAEs average, ImageNet, recovered images |

> [!tip] 效果简介
> - ImageNet, VGG19 (untargeted) 上，ASR (%) 95.3 vs other RAE methods (e.g., W-RAE 88.6) (~+6.7% over best competitor)。
> - ImageNet, DenseNet121 (targeted) 上，ASR (%) 90.2 vs other methods (≤80.2) (≥10% higher)。
> - ImageNet, RAEs average 上，PSNR (dB) 46.39 vs other RAE methods (max ~40.39) (>6 dB over next best)。

## 概要

**问题瓶颈**：现有可逆对抗样本（Reversible Adversarial Example, RAE）方法普遍采用两阶段范式——先独立生成对抗样本，再通过额外嵌入步骤保存扰动信息以支持恢复。然而，该额外嵌入操作会引入噪声，破坏原有对抗样本的扰动分布与视觉结构，导致最终RAE在攻击有效性与视觉质量之间出现显著退化（见 Figure 1 中各方法从AE到RAE的性能下滑）。

**核心思路**：RevINN提出一种端到端的单阶段可逆神经网络，利用图像自身的小波频率信息直接生成RAE。其关键洞察在于：通过在图像低频（结构）与高频（细节）子带之间建立可逆信息交换机制，将对抗扰动生成与可逆恢复统一在同一网络中，从而消除两阶段方法中额外嵌入带来的质量退化。

**方法定位**：RevINN属于单阶段、基于频率调制的可逆对抗样本生成方法。与依赖外部代理模型梯度优化的传统对抗攻击不同，RevINN仅利用图像内在的频率特性进行交叉调制，不引入外部类别特定信息。其核心模块包括：
- **CFMA（Cross-Frequency Modulation Attack）**：在低频分量与高频分量之间进行双向缩放-平移调制，实现粗粒度交叉频率攻击；
- **HFPE（High-Frequency Perturbation Enhancement）**：采用三支路结构对三个高频子带（LH、HL、HH）进行细粒度定向增强。

整个变换过程具有严格的双射性质，逆过程通过共享参数即可近乎无损地恢复原始图像，无需额外嵌入数据或密钥。

**主要结果**：
- **攻击性能**：在ImageNet数据集上，RevINN对VGG19的非目标攻击成功率达95.3%，对DenseNet121的目标攻击成功率达90.2%，均显著超越现有RAE方法（Table 1）。
- **视觉质量**：生成的RAE平均PSNR达46.39 dB，超过其他方法6 dB以上，SSIM达0.992；恢复图像的PSNR高达58.94 dB，SSIM接近1（0.998），实现近乎无损的复原（Table 2）。
- **鲁棒性**：在位深度缩减、翻转、缩放、裁剪、JPEG压缩等多种图像操作下，RevINN展现出比RAE-YUV更强的攻击鲁棒性（Figure 5）。
- **消融验证**：CFMA模块主攻攻击强度，HFPE模块主攻视觉质量，二者缺一不可（Table 3）。

**局限性**：当前RevINN主要面向白盒攻击设计，尚未在完全黑盒或转移攻击场景下评估；恢复图像并非绝对无损，在大对抗预算下可能存在轻微细节损失；在自监督模型上的攻击成功率和泛化性有待进一步验证；论文未报告模型大小、推理延迟等部署相关指标。

### 对抗样本与可逆性需求

深度神经网络在图像分类等任务中取得了显著成功，但极易受到对抗样本的攻击——攻击者通过对原始图像施加人眼难以察觉的微小扰动，即可使模型产生错误预测。这一脆弱性引发了学术界对对抗攻击与防御的广泛研究。在对抗样本的诸多研究方向中，**可逆对抗样本（Reversible Adversarial Examples, RAE）** 提出了一个独特且具有实际价值的目标：生成的对抗样本不仅要能成功攻击目标模型，还必须能够被授权用户无损或近无损地恢复为原始图像。这种可逆性在军事图像传输、医学影像共享、隐私保护等场景中具有重要应用前景。

### 两阶段范式的结构性缺陷

现有RAE生成方法普遍采用**两阶段范式**：第一阶段独立生成对抗样本（通常通过PGD等基于梯度的攻击方法），第二阶段通过额外的信息嵌入步骤将扰动信息或恢复密钥隐藏到对抗样本中，以支持后续的原始图像恢复。典型的代表方法包括：

- **RAE-RDH**（Liu et al., Pattern Recognition 2023）：基于可逆数据隐藏技术嵌入扰动信息；
- **RAE-YUV**（Yin et al., Pattern Recognition Letters 2023）：在YUV颜色空间中进行扰动嵌入；
- **RIT-RAE**（Yin et al., arXiv 2019）：利用可逆图像变换实现恢复；
- **SRAE**（Zhang et al., TCSVT 2022）：基于可恢复生成对抗网络；
- **W-RAE**（Xiong et al., Pattern Recognition 2023）：面向黑盒场景的可逆对抗样本方法；
- **DP-RAE**（Zhu et al., ACM MM 2024）：双阶段合并策略；
- **INN-RAE**（Huang et al., Image and Vision Computing 2024）：利用可逆神经网络进行扰动嵌入。

这一范式存在一个根本性瓶颈：**额外嵌入操作引入的噪声会破坏原有对抗样本的扰动分布与视觉结构**。具体而言，第二阶段的信息嵌入本质上是对已生成的对抗样本进行二次修改，这种修改不可避免地干扰了第一阶段精心优化的对抗扰动，导致最终RAE的攻击有效性下降；同时，嵌入操作本身也会在图像中留下可见痕迹，造成视觉质量的退化。如Figure 1所示，现有两阶段方法生成的RAE在PSNR-ASR空间中普遍偏离其原始对抗样本（AE）的性能点，表现为攻击成功率和视觉质量的双重损失。

### 本文动机与核心思路

针对上述瓶颈，本文提出一个关键问题：**能否在单一阶段内同时完成对抗扰动的生成与可逆恢复能力的构建，从而彻底消除两阶段范式中的二次退化？**

RevINN的核心洞察在于：**利用图像自身的频率特性，通过可逆信息交换机制直接生成RAE，无需依赖外部代理模型优化，也无需额外的嵌入步骤。** 具体而言，RevINN将图像经离散小波变换（DWT）分解为低频（LL）和高频（LH、HL、HH）子带后，通过两个关键模块——**交叉频率调制攻击模块（CFMA）** 和**高频扰动增强模块（HFPE）**——在不同频率分量之间建立双向调制关系。CFMA实现低频与高频间的粗粒度交叉攻击，HFPE对三个高频子带进行细粒度三支路增强。整个过程通过可逆神经网络的双射性质保证：前向过程生成RAE，逆向过程通过共享参数精确恢复原始图像。

这一设计的优势在于：扰动的来源是图像自身的高低频信息交换，而非外部梯度信号，因此既保持了攻击强度，又通过逆小波变换与逆调制过程实现了近乎无损的恢复。如Figure 1中红色星标所示，RevINN在PSNR-ASR空间中实现了显著优于所有两阶段方法的综合性能。

## 核心方法与创新机理

### 问题瓶颈：两阶段范式的固有缺陷

现有可逆对抗样本（RAE）方法普遍采用两阶段流水线：首先生成传统对抗样本（AE），随后通过额外嵌入步骤将扰动信息注入图像以支持恢复。这一范式存在一个根本性瓶颈——**额外嵌入操作引入的噪声会破坏原有对抗样本的扰动分布与视觉结构**。如 Figure 1 所示，两阶段方法（如 **RAE-RDH** (Liu et al., Pattern Recognition 2023)、**RAE-YUV** (Yin et al., Pattern Recognition Letters 2023)、**W-RAE** (Xiong et al., Pattern Recognition 2023) 等）从 AE 到 RAE 的转换过程中，攻击成功率（ASR）和视觉质量（PSNR）均出现不同程度的退化。其根本原因在于：嵌入过程与对抗生成过程相互独立，嵌入操作在空间域或颜色空间引入的修改会稀释原始对抗扰动，导致最终 RAE 既无法保持原有攻击强度，又损失了视觉保真度。

### 核心洞察：频率交叉调制的单阶段生成

RevINN 的核心创新在于**将对抗扰动生成与可逆恢复统一到端到端单阶段网络中**，从根本上消除了两阶段范式中的嵌入退化问题。其关键洞察可概括为：

> **通过可逆信息交换机制，在图像低频（结构）和高频（细节）子带间建立双向调制，利用图像内在频率特性生成对抗扰动，无需依赖外部代理模型信息。**

具体而言，RevINN 利用可逆神经网络（INN）的双射性质，在小波域内对图像自身的频率分量进行交叉动态调制。这一设计带来了三个层面的范式转变：

| 设计维度 | 两阶段方法 | RevINN（本方法） |
|---------|-----------|-----------------|
| **生成范式** | 先独立生成 AE，再嵌入扰动信息以支持恢复 | 在小波域通过频率交叉调制直接生成 RAE |
| **对抗扰动来源** | 依赖外部代理模型梯度优化，引入类别特定扰动 | 利用图像自身低频与高频信息通过可逆变换相互调制 |
| **可逆恢复机制** | 额外嵌入扰动信息（或密钥）以支持提取与恢复 | 网络双射性质保证逆过程通过共享参数直接恢复 |

### 关键模块设计

RevINN 通过两个核心模块实现上述洞察：

**（1）交叉频率调制攻击模块（CFMA）**：在低频分量 $x_{LL}$ 与高频分量 $x_{HC}$ 之间进行双向缩放-平移调制，实现粗粒度的交叉频率攻击。其前向传播公式为：

$$
\begin{array}{rl} x_{LL}^{1} &= x_{LL} + \sigma(x_{HC}) \\ x_{HC}^{1} &= x_{HC} \cdot \exp(\alpha(\mu(x_{LL}^{1}))) + \omega(x_{LL}^{1}) \end{array}
$$

其中 $\sigma$、$\mu$、$\omega$ 均为可学习子网络，$\alpha$ 为缩放因子。该设计使得低频结构信息与高频细节信息相互渗透，扰动自然融入图像内容而非简单叠加。

**（2）高频扰动增强模块（HFPE）**：创新性地采用三支路结构，对三个高频子带（LH、HL、HH）进行细粒度定向调制。与传统的二分支耦合层不同，HFPE 以 HH 子带作为引导，分别对 LH 和 HL 子带进行条件调制，再将二者合并特征反哺 HH 子带，形成三向交互。这一设计大幅提升了对抗扰动的语义丰富度，消融实验证实：移除 CFMA 导致攻击性能骤降，移除 HFPE 则使 RAE 视觉质量严重恶化（Table 3）。

### 与已有工作的本质区别

与同样使用可逆神经网络的 **INN-RAE** (Huang et al., Image and Vision Computing 2024) 不同，后者仍然遵循两阶段范式——将 INN 仅作为扰动嵌入工具，对抗扰动本身仍依赖外部代理模型生成。RevINN 则将整个生成过程内化于 INN 的前向传播中，扰动来源于图像自身频率分量的交叉调制，无需任何外部模型参与。这一设计使得 RevINN 在 PSNR vs ASR 空间中同时达到了高视觉质量（RAE 平均 PSNR 46.39 dB，超过其他方法 6 dB 以上）和高攻击成功率（VGG19 非目标攻击 ASR 95.3%，DenseNet121 目标攻击 ASR 90.2%），显著优于所有两阶段方法。

### 信息交换的统一视角

论文进一步将 CFMA 和 HFPE 的调制过程抽象为统一的信息交换框架：两支路间丢弃判别信息 $\tau$ 并注入信息 $\gamma$，形式化为 $x_{1}' = x_{1} - \tau + \gamma$ 和 $x_{2}' = x_{2} + \tau - \gamma$。这一抽象揭示了 RevINN 生成 RAE 的本质机制——通过可逆变换在不同频率分量间重新分配图像信息，而非引入外部噪声，从而在保证攻击强度的同时维持了近乎无损的恢复能力（恢复图像 PSNR 58.94 dB，SSIM 0.998）。

RevINN 是一种端到端的单阶段可逆对抗样本生成框架，其核心思路是在小波域内通过可逆信息交换直接生成可逆对抗样本（Reversible Adversarial Example, RAE），从而绕开现有两阶段方法中“先攻击、后嵌入”所引入的质量退化瓶颈。

### 整体流程

RevINN 的前向攻击过程由四个串联模块组成（见 Figure 2）：

![[assets/figures/papers/paper_list_l926_https_openaccess_thecvf_com_content_CVPR2026_html_Huang_RevINN_An_End_to/figures/002_Figure_2.jpg]]
*Figure 2: The overall architecture of the proposed RevINN. Note that it only depicts the forward attack process of RevINN*

1. **离散小波变换（DWT）**：输入原始图像 $x$ 首先经由 DWT 分解为四个子带——一个低频分量 $x_{LL}$ 和三个高频分量 $x_{HL}, x_{LH}, x_{HH}$。低频分量承载图像的结构信息，高频分量承载纹理与边缘细节。
2. **交叉频率调制攻击模块（CFMA）**：在低频分量 $x_{LL}$ 与合并后的高频分量 $x_{HC}$ 之间执行双向缩放-平移调制。该模块从图像自身的高低频信息中提取对抗扰动，并将其交替注入对方分量，实现粗粒度的交叉频率攻击。
3. **高频扰动增强模块（HFPE）**：对三个高频子带进行三支路细粒度调制。以 $x_{HH}$ 子带作为引导，分别对 $x_{LH}$ 和 $x_{HL}$ 施加缩放-平移变换，同时 $x_{HH}$ 自身也受前两者合并特征的调制，从而显著增强高频扰动语义。
4. **逆离散小波变换（IWT）**：将调制后的低频与高频分量通过 IWT 重构为空间域的可逆对抗样本 $x_{RAE}$。

整个前向过程可抽象为 $x_{RAE} = f(x)$，其中 $f$ 是由 CFMA 和 HFPE 构成的可逆变换。

### 反向恢复过程

授权用户可通过逆向执行上述模块恢复原始图像。具体而言，反向过程按照前向的逆序依次执行 HFPE 逆运算、CFMA 逆运算，最后通过 IWT 重建恢复图像 $x_{cover}$。由于 CFMA 与 HFPE 均设计为精确的双射（bijection），反向过程仅需共享前向参数即可实现近乎无损的复原，无需额外嵌入任何扰动信息或密钥。

### 输入输出规范

- **输入**：原始图像 $x$ 及其真实标签 $y$。
- **前向输出**：可逆对抗样本 $x_{RAE}$，需满足 $C(x_{RAE}) \neq y$（即被分类器 $C$ 错误分类）。
- **反向输出**：恢复图像 $x_{cover}$，目标为 $x_{cover} \approx x$。

### 训练目标

RevINN 的优化目标是最小化联合损失函数：

$$\mathcal{L} = \lambda_{1}\mathcal{L}_{freq} + \lambda_{2}\mathcal{L}_{adv} + \lambda_{3}\mathcal{L}_{rev}$$

其中 $\mathcal{L}_{freq}$ 约束 RAE 与原始图像在低频子带上的结构一致性，$\mathcal{L}_{adv}$ 驱动 RAE 的对抗攻击效果，$\mathcal{L}_{rev}$ 保证恢复图像与原始图像逐像素一致。三项损失的加权联合使得网络在攻击强度、视觉保真度和可逆性之间取得平衡。

### 与两阶段范式的本质区别

现有两阶段方法（如 RAE-RDH、RAE-YUV、INN-RAE 等）先独立生成对抗样本，再通过额外嵌入步骤保存扰动信息。这一额外操作会破坏原有对抗样本的扰动分布，导致 RAE 的攻击有效性和视觉质量双双下降。RevINN 将对抗扰动生成与可逆恢复统一在单阶段网络内，利用图像内在频率信息进行交叉调制，从机制上消除了额外嵌入带来的退化。Figure 1 直观展示了这一优势：两阶段方法的 RAE 在 PSNR-ASR 空间中相对其原始 AE 出现明显退化，而 RevINN 以红色星标指示的位置同时达到高视觉质量和高攻击成功率。

RevINN 的核心架构由四个关键模块串联构成，在小波域内完成从原始图像到可逆对抗样本（RAE）的端到端生成。整体流程见 Figure 2。

### 离散小波变换（DWT）

前向攻击过程的第一步是将输入图像 $x$ 通过离散小波变换分解为四个子带：低频分量 $x_{LL}$ 和三个高频分量 $x_{LH}$、$x_{HL}$、$x_{HH}$。低频分量承载图像的主体结构信息，高频分量编码边缘、纹理等细节。这种频率解耦为后续的交叉调制攻击提供了物理基础——扰动注入高频子带可改变分类器对局部细节的感知，而低频子带的约束则维持整体视觉结构。

### 交叉频率调制攻击模块（CFMA）

CFMA 是 RevINN 实现粗粒度对抗攻击的核心。它将所有高频分量拼接为 $x_{HC} = [x_{LH}, x_{HL}, x_{HH}]$，然后在 $x_{LL}$ 与 $x_{HC}$ 之间执行双向缩放‑平移调制。

**前向传播**的数学形式为：

$$
\begin{array}{rl}
x_{LL}^{1} &= x_{LL} + \sigma(x_{HC}) \\[4pt]
x_{HC}^{1} &= x_{HC} \cdot \exp(\alpha(\mu(x_{LL}^{1}))) + \omega(x_{LL}^{1})
\end{array}
$$

其中 $\sigma(\cdot)$、$\mu(\cdot)$、$\omega(\cdot)$ 均为轻量卷积网络，$\alpha(\cdot)$ 为缩放因子函数。该公式的物理解释是：首先将高频信息 $\sigma(x_{HC})$ 作为加性扰动注入低频分量，得到调制后的 $x_{LL}^{1}$；随后，以调制后的低频分量 $x_{LL}^{1}$ 为条件，对高频分量施加缩放 $\exp(\alpha(\mu(x_{LL}^{1})))$ 和平移 $\omega(x_{LL}^{1})$ 变换。这种交替耦合机制使得低频结构信息与高频细节信息相互渗透，产生的扰动同时具备全局结构感知和局部细节攻击能力。

**后向传播**（恢复过程）利用可逆神经网络的双射性质，通过精确逆运算恢复原始频率分量：

$$
\begin{array}{rl}
x_{HC} &= (x_{HC}^{1} - \omega(x_{LL}^{1})) \div \exp(\alpha(\mu(x_{LL}^{1}))) \\[4pt]
x_{LL} &= x_{LL}^{1} - \sigma(x_{HC})
\end{array}
$$

由于 $\sigma$、$\mu$、$\omega$ 等子网络在前向和后向中共享参数，恢复过程无需额外嵌入信息即可实现精确求逆。

### 高频扰动增强模块（HFPE）

CFMA 将三个高频子带合并为 $x_{HC}$ 统一处理，损失了子带间的细粒度差异。HFPE 模块创新性地扩展为三支路结构，对 $x_{LH}^{1}$、$x_{HL}^{1}$、$x_{HH}^{1}$ 分别进行定向调制。

**前向传播**公式为：

$$
\begin{array}{rl}
x_{LH}^{2} &= x_{LH}^{1} \cdot \exp(\alpha(\psi(x_{HH}^{1}))) + \varphi(x_{HH}^{1}) \\[4pt]
x_{HL}^{2} &= x_{HL}^{1} \cdot \exp(\alpha(\pi(x_{HH}^{1}))) + \delta(x_{HH}^{1}) \\[4pt]
x_{HH}^{2} &= x_{HH}^{1} \cdot \exp(\alpha(\rho(x_{concat}))) + \eta(x_{concat})
\end{array}
$$

其中 $x_{concat} = [x_{LH}^{1}, x_{HL}^{1}]$，$\psi$、$\pi$、$\rho$、$\varphi$、$\delta$、$\eta$ 均为小型卷积网络。设计逻辑是：$x_{HH}$ 子带包含最丰富的对角高频细节，因此作为引导信息，通过 $\psi$ 和 $\pi$ 分别控制 $x_{LH}$ 和 $x_{HL}$ 的缩放因子，通过 $\varphi$ 和 $\delta$ 提供加性扰动；而 $x_{HH}$ 自身的调制则以拼接后的 $x_{LH}$ 和 $x_{HL}$ 为条件。这种交叉引导使得三个高频子带的扰动语义相互增强，大幅提升了对抗样本的攻击强度。

**后向传播**同样通过逆运算恢复：

$$
\begin{array}{rl}
x_{HH}^{1} &= (x_{HH}^{2} - \eta(x_{concat})) \div \exp(\alpha(\rho(x_{concat}))) \\[4pt]
x_{LH}^{1} &= (x_{LH}^{2} - \varphi(x_{HH}^{1})) \div \exp(\alpha(\psi(x_{HH}^{1}))) \\[4pt]
x_{HL}^{1} &= (x_{HL}^{2} - \delta(x_{HH}^{1})) \div \exp(\alpha(\pi(x_{HH}^{1})))
\end{array}
$$

### 逆离散小波变换（IWT）

调制后的频率分量 $x_{LL}^{1}$、$x_{LH}^{2}$、$x_{HL}^{2}$、$x_{HH}^{2}$ 通过逆离散小波变换重构为空间域的 RAE $x_{RAE}$。由于所有变换均在小波域完成，扰动自然地融入图像的多尺度结构中，而非直接叠加在像素空间，这是 RevINN 生成 RAE 视觉质量显著优于两阶段方法的关键原因。

### 统一信息交换抽象

论文将 CFMA 和 HFPE 的操作统一抽象为两支路间的信息交换范式：

$$
\begin{array}{r}
x_{1}' = x_{1} - \tau + \gamma \\
x_{2}' = x_{2} + \tau - \gamma
\end{array}
$$

其中 $\tau$ 表示从一支路丢弃的判别性信息，$\gamma$ 表示从另一支路注入的信息。该抽象揭示了 RevINN 各模块的双射本质：只要 $\tau$ 和 $\gamma$ 由共享参数的子网络从前一层变量计算得到，逆过程即可精确还原。这为理解整个网络的可逆性提供了统一视角。

### 损失函数设计

RevINN 的总损失函数由三项加权构成：

$$
\mathcal{L} = \lambda_{1}\mathcal{L}_{freq} + \lambda_{2}\mathcal{L}_{adv} + \lambda_{3}\mathcal{L}_{rev}
$$

**低频小波损失** $\mathcal{L}_{freq}$ 约束 RAE 与原始图像在低频子带上的结构一致性：

$$
\mathcal{L}_{freq} = \ell_{MSE}(T(x_{RAE})_{LL}, T(x)_{LL})
$$

其中 $T(\cdot)_{LL}$ 表示 DWT 分解后的低频分量。该项确保 RAE 保持原始图像的主体结构，是维持高 PSNR 和 SSIM 的机制保障。

**对抗损失** $\mathcal{L}_{adv}$ 采用标准交叉熵损失，要求分类器 $C$ 对 $x_{RAE}$ 的预测偏离真实标签 $y$。在目标攻击设定下，则要求预测趋近于目标类别。

**可逆损失** $\mathcal{L}_{rev}$ 直接约束恢复图像与原始图像的逐像素一致性：

$$
\mathcal{L}_{rev} = \ell_{MSE}(x_{cover}, x)
$$

由于 CFMA 和 HFPE 的双射性质，该损失在训练中可快速收敛至极小值，使恢复图像的 SSIM 接近 1、PSNR 高达 58.94 dB，实现近乎无损的复原。

## 实验与关键发现

### 实验设置

实验基于 **ImageNet** 数据集进行，评估覆盖白盒非目标攻击与目标攻击两种设定。目标模型包括 **VGG19**、**ResNet50**、**DenseNet121** 等主流分类器。对比方法涵盖现有两阶段RAE方案：**RAE-RDH**（Liu et al., Pattern Recognition 2023）、**RAE-YUV**（Yin et al., Pattern Recognition Letters 2023）、**RIT-RAE**（Yin et al., arXiv 2019）、**SRAE**（Zhang et al., TCSVT 2022）、**W-RAE**（Xiong et al., Pattern Recognition 2023）、**DP-RAE**（Zhu et al., ACM MM 2024）和 **INN-RAE**（Huang et al., Image and Vision Computing 2024），以及自监督场景下的 **RAEncoder**（Xing et al., CVPR 2025）。评估指标包括攻击成功率（ASR）、RAE与恢复图像的 **PSNR** 和 **SSIM**。

### 攻击性能主结果

Table 1 给出了目标与非目标攻击设定下各方法的ASR对比。RevINN在多个模型上取得了最优攻击效果：

![[assets/figures/papers/paper_list_l926_https_openaccess_thecvf_com_content_CVPR2026_html_Huang_RevINN_An_End_to/figures/003_Table_1.jpg]]
*Table 1: Attack comparison of our RevINN and other RAE schemes across different models in the untargeted and targeted attack setting. ’-’ denotes experiments not conducted. The bold indicates the best result*

| 模型 | 攻击类型 | RevINN ASR | 最强对比方法 ASR | 提升幅度 |
|------|----------|------------|------------------|----------|
| VGG19 | 非目标 | **95.3%** | W-RAE 88.6% | +6.7% |
| DenseNet121 | 非目标 | **98.3%** | — | 显著领先 |
| DenseNet121 | 目标 | **90.2%** | 其他方法 ≤80.2% | ≥10% |
| ResNet50 | 目标 | **81.6%** | — | 最优 |

关键观察：在 DenseNet121 目标攻击中，RevINN 的 ASR 达到 90%，比所有对比方法高出至少 10 个百分点。这一优势源于 RevINN 的单阶段生成范式——两阶段方法在独立生成对抗样本后，额外嵌入扰动信息的过程会破坏原有扰动分布，导致 RAE 攻击有效性下降；而 RevINN 在小波域通过频率交叉调制直接生成 RAE，避免了该退化。

### 视觉质量主结果

Table 2 对比了各方法生成的 RAE 及其恢复图像的视觉质量。RevINN 在保真度上实现了跨代领先：

![[assets/figures/papers/paper_list_l926_https_openaccess_thecvf_com_content_CVPR2026_html_Huang_RevINN_An_End_to/figures/004_Table_2.jpg]]
*Table 2: Visual comparison of RAEs and their recovered images generated by our RevINN and other RAE schemes under the untargeted attack setting. ’-’ denotes experiments not conducted. The bold indicates the best result*

- **RAE 平均 PSNR**：RevINN 达到 **46.39 dB**，超过其他方法 **6 dB 以上**（次优方法约 40.39 dB）。
- **RAE 平均 SSIM**：RevINN 为 **0.992**，显著高于所有两阶段方法。
- **恢复图像 PSNR**：RevINN 达到 **58.94 dB**，恢复 SSIM 为 **0.998**，接近无损复原。

Figure 3 和 Figure 4 分别展示了 RAE 和恢复图像的可视化对比。RevINN 生成的 RAE 在视觉上几乎与原始图像无异，而 RAE-YUV 和 W-RAE 的 RAE 存在可见的色彩偏移或纹理伪影。在恢复图像方面，SRAE 和 W-RAE 的恢复结果残留明显噪声，RevINN 的恢复图像则与原始图像无法区分。

![[assets/figures/papers/paper_list_l926_https_openaccess_thecvf_com_content_CVPR2026_html_Huang_RevINN_An_End_to/figures/005_Figure_3.jpg]]
*Figure 3: Visual comparison of RAEs generated by RAE-YUV, W-RAE and our RevINN*

![[assets/figures/papers/paper_list_l926_https_openaccess_thecvf_com_content_CVPR2026_html_Huang_RevINN_An_End_to/figures/007_Figure_4.jpg]]
*Figure 4: Visual comparison of recovered images obtained by SRAE, W-RAE and our RevINN*

### PSNR-ASR 权衡分析

Figure 1 以 PSNR 为横轴、ASR 为纵轴，展示了各方法从原始对抗样本（AE）到可逆对抗样本（RAE）的质量退化轨迹。每条虚线连接同一方法的 AE 与 RAE 性能点：

- 所有两阶段方法的 RAE 点均相对于其 AE 点发生明显的 **右下偏移**，即攻击有效性和视觉质量同时下降。
- RevINN 的红色星标位于 **右上角**，同时实现了高视觉质量和高攻击成功率，证明单阶段频率调制机制从根本上消除了两阶段嵌入引入的质量退化。

### 消融实验

Table 3 报告了模块消融与对抗预算消融结果，揭示了 CFMA 和 HFPE 模块的功能分工：

![[assets/figures/papers/paper_list_l926_https_openaccess_thecvf_com_content_CVPR2026_html_Huang_RevINN_An_End_to/figures/008_Table_3.jpg]]
*Table 3: Ablation experiments on different modules of RevINN and different perturbation budgets*

- **移除 CFMA**：攻击成功率大幅下降，但 RAE 视觉质量保持。这表明 CFMA 是攻击强度的主要来源，其交叉频率调制机制负责将扰动注入到对分类器敏感的频率分量中。
- **移除 HFPE**：RAE 视觉质量严重恶化，PSNR 显著降低。这说明 HFPE 的三支路高频增强对维持视觉保真度不可或缺——它通过对 LH、HL、HH 子带的细粒度调制，确保扰动在语义上合理分布，而非随机噪声。

两个模块形成功能互补：CFMA 提供粗粒度的交叉频率攻击，HFPE 进行细粒度的高频语义增强，二者协同才能同时实现高 ASR 和高 PSNR。

对抗预算 ε 消融（1/255 至 8/255）显示，RevINN 在不同扰动强度下均能保持可接受的 ASR 与视觉保真度，表明方法对扰动预算具有良好的适应性。

### 鲁棒性分析

Figure 5 对比了 RAE-YUV 与 RevINN 在多种图像操作下的攻击鲁棒性：

- **常规图像变换**（Figure 5a）：包括水平/垂直翻转、2×放大、0.5×缩小、90%中心裁剪、JPEG 压缩（质量因子 70）。RevINN 在所有操作下均保持高于 RAE-YUV 的 ASR，展现出更强的扰动结构稳定性。
- **位深度缩减**（Figure 5b）：在 2-bit 位深度缩减下，RAE-YUV 的 ASR 降至 15% 以下，而 RevINN 仍保持 **23%** 的 ASR。这是因为 RevINN 的扰动嵌入在小波域，对像素域的量化操作具有天然鲁棒性。

### 自监督学习场景

Table 4 将 RevINN 与 RAEncoder 在自监督学习模型（Barlow Twins 等）上进行对比。RevINN 在 RAE 视觉质量（PSNR）上优于 RAEncoder，达到 **49.76 dB**。然而，在自监督模型上的攻击成功率相对有监督场景有所下降，且仅与 RAEncoder 做了对比，泛化性待进一步验证。

### 失败模式与局限性

1. **恢复并非完全无损**：尽管恢复 SSIM 接近 1，但当对抗预算 ε 较大时，小波域的信息交换可能导致轻微的图像细节损失。CFMA 和 HFPE 虽设计为双射，但数值精度和变换过程中的信息丢弃（见 Eq. 7 的 τ-γ 交换抽象）使得恢复图像与原始图像并非逐像素完全一致。
2. **白盒假设限制**：当前 RevINN 主要针对白盒攻击设计，未在完全黑盒或转移攻击场景下评估。其扰动生成依赖图像自身频率信息，不利用代理模型梯度，理论上具备黑盒扩展潜力，但缺乏实验验证。
3. **自监督场景性能下降**：在自监督模型上攻击成功率相对有监督场景有所下降，说明频率调制策略对自监督特征空间的适应性有待提升。
4. **部署指标缺失**：论文未报告模型大小、推理延迟等部署相关指标，对不同分辨率图像的适应性尚不明确。

### 开放问题

- 为什么随着对抗预算 ε 的增加，恢复图像的质量反而提高？这一反直觉现象可能与更大扰动提供了更强的可逆性学习信号有关，但论文未给出解释。
- 在三支路 HFPE 中，为何选择 HH 子带作为 LH 和 HL 的引导，而非其他组合？该设计选择的消融验证尚不充分。
- RevINN 如何扩展到黑盒攻击并保持可逆性？频率调制机制不依赖代理模型信息，理论上可自然迁移，但需实验证实。

## 定位与知识库关联

### 两阶段范式及其固有瓶颈

现有可逆对抗样本（RAE）方法普遍遵循两阶段范式：第一阶段独立生成对抗样本（AE），第二阶段通过额外嵌入操作将扰动信息隐藏到图像中，以支持后续恢复。这一范式衍生出多种技术路线，包括：

- **基于可逆数据隐藏**：**RAE-RDH**（Liu et al., Pattern Recognition 2023）在生成AE后，利用可逆数据隐藏技术将扰动嵌入载体图像，但嵌入过程引入的噪声会破坏原有AE的扰动分布。
- **基于颜色空间变换**：**RAE-YUV**（Yin et al., Pattern Recognition Letters 2023）将扰动嵌入YUV颜色空间，试图减少视觉质量损失，但颜色空间转换本身会改变对抗扰动的语义结构。
- **基于可逆图像变换**：**RIT-RAE**（Yin et al., arXiv 2019）通过可逆图像变换实现扰动隐藏，但变换域与对抗攻击域的不匹配导致攻击有效性下降。
- **基于生成对抗网络**：**SRAE**（Zhang et al., TCSVT 2022）利用可恢复GAN生成RAE，但GAN的训练不稳定性和模式坍塌问题限制了RAE质量。
- **面向黑盒场景**：**W-RAE**（Xiong et al., Pattern Recognition 2023）通过水印嵌入实现可逆性，但在白盒攻击下性能受限。
- **双阶段合并**：**DP-RAE**（Zhu et al., ACM MM 2024）尝试将两阶段合并优化，但仍未从根本上消除额外嵌入操作。
- **基于可逆神经网络**：**INN-RAE**（Huang et al., Image and Vision Computing 2024）引入INN进行扰动嵌入，但仍沿袭两阶段框架，INN仅用于第二阶段的信息隐藏。
- **数据集IP保护**：**RAEncoder**（Xing et al., CVPR 2025）面向无标签场景设计RAE编码器，但其优化目标与通用RAE生成存在差异。

两阶段范式的核心瓶颈在于：**额外嵌入操作引入的噪声会破坏原有对抗样本的扰动分布与视觉结构**。从Figure 1可以清晰观察到，所有两阶段方法的RAE（虚线终点）相比其原始AE（虚线起点），在攻击成功率（ASR）和视觉质量（PSNR）两个维度上均出现不同程度的退化。这种退化源于嵌入过程在图像中引入了与对抗扰动无关的冗余信息，既稀释了攻击语义，又降低了视觉保真度。

### RevINN的方法论跃迁：从两阶段到端到端频率调制

RevINN的方法论创新体现在四个关键维度的根本性转变：

**1. 生成范式：从两阶段串行到单阶段统一**

RevINN将对抗扰动生成与可逆恢复统一在单个可逆神经网络中，消除了两阶段方法中“先攻击、后嵌入”的串行依赖。通过可逆神经网络的双射性质（bijection），前向过程直接生成RAE，反向过程通过共享参数 $\theta$ 即可恢复原始图像，无需额外嵌入任何扰动信息或密钥。这一设计从根本上规避了嵌入噪声对RAE质量的破坏。

**2. 对抗扰动来源：从外部代理模型到图像内在频率**

传统方法依赖外部代理模型（surrogate model）的梯度优化来生成类别特定的对抗扰动，这不仅增加了计算开销，还使扰动分布受限于代理模型的特征空间。RevINN转而利用图像自身的频率信息：通过小波变换将图像分解为低频（LL）和高频（HL, LH, HH）子带，在频率域内通过交叉调制生成扰动。扰动信息来源于不同频率分量之间的信息交换，而非外部模型的梯度信号，这使得RevINN在保持攻击强度的同时，摆脱了对特定代理模型的依赖。

**3. 可逆恢复机制：从额外嵌入到网络双射**

两阶段方法需要在图像中嵌入额外的恢复信息（如扰动残差、密钥等），这些嵌入数据不可避免地占用图像容量并引入失真。RevINN利用可逆神经网络的双射性质，前向变换 $f$ 和逆变换 $f^{-1}$ 共享参数 $\theta$，仅需优化 $f$ 即可同时获得RAE及其恢复版本。逆过程通过精确逆转CFMA和HFPE的操作实现近乎无损的恢复，恢复图像的SSIM接近1，PSNR高达58.94dB。

**4. 高频处理粒度：从二分支耦合到三支路细粒度调制**

传统可逆神经网络通常采用二分支耦合层（coupling layer）结构，无法充分利用小波域三个高频子带（LH, HL, HH）的差异化信息。RevINN的HFPE模块创新性地扩展为三支路结构，对三个高频子带进行细粒度定向调制：LH和HL子带分别受HH子带引导进行缩放-平移变换，HH子带则受LH和HL合并特征的引导。这种三支路设计大幅提升了对抗扰动的语义丰富性和攻击强度，消融实验证实移除HFPE会导致RAE视觉质量大幅恶化。

### 核心机制：交叉频率调制与信息交换原理

RevINN的核心机制可抽象为一种**可逆信息交换**过程。在CFMA模块中，低频分量 $x_{LL}$ 和高频分量 $x_{HC}$ 之间进行双向缩放-平移调制：

$$x_{LL}^{1} = x_{LL} + \sigma(x_{HC})$$
$$x_{HC}^{1} = x_{HC} \cdot \exp(\alpha(\mu(x_{LL}^{1}))) + \omega(x_{LL}^{1})$$

这一过程可理解为：低频分量从高频分量中获取细节扰动信息（通过 $\sigma(x_{HC})$），高频分量则从调制后的低频分量中获取结构引导（通过 $\mu(x_{LL}^{1})$ 和 $\omega(x_{LL}^{1})$）。这种双向信息交换在频率域内形成了对抗扰动，同时保持了频率分量之间的内在关联。

HFPE模块进一步将这一机制扩展到三个高频子带之间，形成更精细的交叉调制网络。论文将这一过程抽象为统一的信息交换框架：

$$x_{1}' = x_{1} - \tau + \gamma$$
$$x_{2}' = x_{2} + \tau - \gamma$$

其中 $\tau$ 表示从一支路丢弃的判别信息，$\gamma$ 表示注入另一支路的信息。这一抽象揭示了RevINN的本质：通过在不同频率分量之间进行信息丢弃与注入，在不依赖外部类别信息的情况下，利用图像内在频率特性生成对抗扰动。

### 适用边界与局限

**适用场景**：RevINN目前主要针对白盒攻击场景设计，在ImageNet数据集上对VGG19、ResNet50、DenseNet121等主流分类模型展现出优异的攻击性能与视觉质量。其端到端的单阶段设计使其特别适用于对RAE视觉保真度有严格要求的场景，如对抗样本的合法分发与可控恢复。

**已知局限**：

1. **黑盒攻击未验证**：当前RevINN未在完全黑盒或转移攻击场景下评估，其频率调制策略是否能在未知模型结构和参数的情况下保持攻击有效性尚待验证。

2. **恢复并非完全无损**：尽管恢复图像的PSNR高达58.94dB，SSIM接近1，但当对抗预算 $\varepsilon$ 较大时，小波域的信息交换可能导致轻微的图像细节损失。论文未深入分析这种损失的来源与上界。

3. **自监督模型性能下降**：在自监督学习模型（如Barlow Twins）上，RevINN的攻击成功率相对有监督场景有所下降，且仅与RAEncoder做了对比，泛化性待进一步验证。

4. **部署指标缺失**：论文未报告模型大小、推理延迟、内存占用等部署相关指标，对不同分辨率图像的适应性尚不明确。

### 开放问题

1. **恢复质量与对抗预算的反直觉关系**：实验观察到随着对抗预算 $\varepsilon$ 的增加，恢复图像的质量反而提高。这一现象与直觉相悖——更大的扰动通常意味着更多的信息丢失。其背后的机制需要进一步的理论分析。

2. **双射设计的非完美性**：尽管CFMA和HFPE设计为精确可逆的双射变换，但恢复图像与原始图像并非完全一致。这种微小差异的来源（数值精度、小波变换边界效应、网络训练的近似性）需要系统研究。

3. **黑盒扩展路径**：RevINN如何在不依赖代理模型梯度的情况下扩展到黑盒攻击，同时保持可逆性？可能的路径包括利用查询反馈优化频率调制参数，或与转移攻击策略结合。

4. **计算效率与实时性**：RevINN的多级小波变换和三支路HFPE模块的计算复杂度是否适合实时或资源受限环境？与其他方法的推理速度对比数据缺失。

5. **三支路设计的理论依据**：在HFPE中，为何选择HH子带作为LH和HL的引导，而非其他组合（如LH引导HL和HH）？这一设计选择的频率域理论依据值得深入探讨。

6. **与其他防御机制的交互**：RevINN生成的RAE在面对对抗训练、输入变换、检测器等防御机制时的鲁棒性尚未评估，这对其实际应用至关重要。

## 原文 PDF

![[paperPDFs/CVPR_2026/RevINN_An_End_to_End_Invertible_Neural_Network_for_Reversible_Adversarial_Examples_Generation.pdf]]
