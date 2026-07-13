---
title: "See through Gradients: Image Batch Recovery via GradInversion"
type: paper
paper_level: A
venue: CVPR
year: 2021
pdf_ref: paperPDFs/CVPR_2021/See_through_Gradients_Image_Batch_Recovery_via_GradInversion.pdf
project_link: null
code_link: null
aliases:
- STGIBRG
tags:
- CVPR_2021
- topic/optimization_theory_probabilistic
- topic/optimization_theory_probabilistic/optimization_methods
core_operator: "标签恢复的准确性（基于全连接层梯度的列最小值）、梯度匹配损失（ℓ2距离）与保真度正则化（BN统计先验、TV、ℓ2范数）以及组一致性正则化（多随机种子配准平均）的协同作用，使得优化过程能够从平均梯度中逐步提取并融合个体图像信息，克服梯度平均带来的信息混淆和空间平移不变性。"
primary_logic: "梯度平均化并未完全抹除个体样本的判别特征；通过将图像恢复形式化为输入噪声到自然图像的优化过程，利用全连接层梯度的符号信息恢复批次标签，并借助网络内BN统计量的强先验和基于图像配准的多路径联合正则化，可以从ResNet-50的ImageNet训练梯度中恢复出高质量的真实图像，即使批量大小高达48。"
claims:
- "在ImageNet训练集批大小为8时，标签恢复准确率达到99.56%，远超先前方法的95.89%。"
- "加入组一致性正则化的完整方法在ImageNet梯度反转上实现LPIPS 0.484、PSNR 12.929、FFT2D 0.175，显著优于先前方法。"
- "在批量大小为48时，仍有约28%的样本可以通过反转重建被正确识别（Image Identifiability Precision）。"
- "GradInversion可视化结果示出在高分辨率图像上恢复出丰富的细节，优于DLG、Geiping等先前方法。"
---

# See through Gradients: Image Batch Recovery via GradInversion

> [!tip] 核心洞察
> 梯度平均化并未完全抹除个体样本的判别特征；通过将图像恢复形式化为输入噪声到自然图像的优化过程，利用全连接层梯度的符号信息恢复批次标签，并借助网络内BN统计量的强先验和基于图像配准的多路径联合正则化，可以从ResNet-50的ImageNet训练梯度中恢复出高质量的真实图像，即使批量大小高达48。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 透过梯度：基于GradInversion的图像批次恢复 |
| 英文题名 | See through Gradients: Image Batch Recovery via GradInversion |
| 会议/期刊 | CVPR 2021 |
| Links | [paper](https://arxiv.org/abs/2104.07586) |
| Topic | #topic/optimization_theory_probabilistic #topic/optimization_theory_probabilistic/optimization_methods |
| Method | GradInversion |
| Dataset | ImageNet1K batch label restoration (10K random samples, batch size 8), ImageNet1K ResNet-50 gradient inversion (batch size 8, exact BN), Ablation: effect of fidelity regularization (batch size 8, approx BN), ImageNet1K ResNet-50 (MOCO V2) gradient inversion (batch size 8) |

> [!tip] 效果简介
> - ImageNet1K batch label restoration (10K random samples, batch size 8) 上，Label Restoration Accuracy (%) 为 99.56，对比 95.89 (summation rule extension)，变化 +3.67%。
> - ImageNet1K ResNet-50 gradient inversion (batch size 8, exact BN) 上，LPIPS ↓ 为 0.484，对比 Geiping et al. (see Table 4)，变化 lower (improvement)。
> - Ablation: effect of fidelity regularization (batch size 8, approx BN) 上，PSNR ↑ / LPIPS ↓ 为 PSNR 12.058, LPIPS 0.655，对比 PSNR 10.753, LPIPS 0.919 (without fidelity)，变化 +1.305 PSNR, -0.264 LPIPS。

## 概要

### 1. 问题背景与瓶颈

联邦学习等分布式训练范式通过共享模型梯度而非原始数据来保护隐私，其核心假设是：**批次平均梯度会掩盖单个样本的信息**，使得攻击者无法从平均梯度中恢复出个体训练样本。然而，现有的梯度反转攻击方法仅在极为受限的条件下有效——单一样本、浅层网络、低分辨率图像——无法扩展到复杂深度网络（如ResNet-50）和大批量（8–48）的高分辨率（224×224）ImageNet图像。这一瓶颈使得“梯度平均化即隐私保护”的假设面临严峻挑战。

### 2. 核心洞见

本文提出的**GradInversion**方法揭示了一个关键发现：**梯度平均化并未完全抹除个体样本的判别特征**。通过将图像恢复形式化为从随机噪声到自然图像的优化过程，GradInversion利用以下三个协同机制突破了先前方法的限制：

- **标签恢复**：基于全连接层梯度列最小值的符号信息，从平均梯度中准确恢复批次内所有样本的标签；
- **保真度正则化**：借助网络内BN统计量的强先验，结合总变差（TV）和ℓ2范数约束，引导优化生成逼真图像；
- **组一致性正则化**：通过多随机种子联合优化与基于RANSAC-flow图像配准的共识平均，克服梯度平均带来的信息混淆和空间平移不变性。

### 3. 方法定位

GradInversion在梯度反转攻击的方法谱系中处于关键跃迁位置：

- **DLG**（Zhu et al., NeurIPS 2019）首次提出通过梯度匹配联合优化输入与伪标签，但仅适用于单样本、浅层网络；
- **iDLG**（Zhao et al., arXiv 2020）改进了单样本标签恢复，但无法处理批次场景；
- **Geiping et al.**（NeurIPS 2020）首次将梯度反转推向ImageNet规模的单图像重建，使用余弦相似度作为梯度匹配损失；
- **DeepInversion**（Yin et al., CVPR 2020）利用BN统计量进行无数据图像合成，其BN正则化思想被GradInversion采纳为保真度正则化的一部分。

GradInversion在此基础上实现了三个关键跃迁：**(1)** 从单样本到大批次的标签恢复（列最小值规则替代求和规则）；**(2)** 从余弦相似度到ℓ2距离的梯度匹配损失，提升优化信号质量；**(3)** 引入多路径联合优化与图像配准驱动的组一致性正则化，显著提升大批量恢复的保真度。

### 4. 主要结果

GradInversion在ImageNet-1K数据集上使用ResNet-50架构取得了突破性成果：

- **标签恢复**：批大小为8时，标签恢复准确率达到**99.56%**，远超先前方法的95.89%（Table 1）；
- **图像重建质量**：完整方法（含组一致性正则化）实现LPIPS **0.484**、PSNR **12.929**、FFT2D **0.175**，显著优于所有先前方法（Table 4）；
- **大批量扩展性**：在批量大小高达**48**时，仍有约28%的样本可通过反转重建被正确识别（Image Identifiability Precision, Figure 8）；
- **可视化保真度**：GradInversion恢复的高分辨率图像展现出丰富的纹理和结构细节，远超DLG、Geiping et al.等方法的模糊重建结果（Figure 4, Figure 5）。

### 5. 局限与开放问题

尽管取得显著进展，GradInversion仍存在若干局限：(1) 最优重建质量依赖目标批次的精确BN统计量，该信息在标准联邦学习设置中通常不可得；(2) 标签恢复假设批次内无重复标签，在小类别任务中可能受限；(3) 人脸恢复存在特征空间错位问题；(4) 文字与数字虽可检测但细节模糊；(5) 多种子联合优化与配准步骤带来额外计算开销。开放问题包括：梯度到原始数据的信息传输机制尚待量化分析；如何在不依赖BN统计量的前提下实现相似重建保真度；以及防御技术（如差分隐私梯度扰动）对GradInversion的抵御效果。



### 分布式训练中的梯度隐私假设

联邦学习与分布式训练场景中，模型更新通常以批次平均梯度的形式在节点间传输。一个被普遍接受的安全假设是：梯度平均化操作会混淆单个样本的信息，使得攻击者无法从平均梯度中反推出原始训练数据。这一假设构成了许多隐私保护框架的理论基础——训练数据本身不出域，仅共享梯度信号，似乎足以防止数据泄漏。

然而，近年来一系列梯度反转攻击工作开始动摇这一假设。**Deep Leakage from Gradients (DLG)**（Zhu et al., NeurIPS 2019）首次证明，在浅层网络和小分辨率图像的设定下，可以通过优化合成输入来精确匹配目标梯度，从而近乎完美地恢复单个训练样本。随后，**Geiping et al.**（NeurIPS 2020）将梯度反转推向了ImageNet规模的单张图像重建，利用余弦相似度作为梯度匹配损失，在ResNet等深层网络上取得了初步成功。

### 现有方法的根本局限

尽管上述工作揭示了梯度泄漏的风险，但它们存在一个关键瓶颈：**所有成功的方法都局限于单一样本或极小批量（batch size ≈ 1）的梯度反转**。在实际联邦学习中，客户端通常使用批量数据进行本地训练，上传的是多张图像的平均梯度。平均化带来的信息混淆使得现有方法在以下维度上迅速失效：

- **批量大小扩展困难**：DLG和Geiping et al.的方法在批量大小超过4时，重建质量急剧下降，几乎无法恢复有意义的视觉特征。
- **网络深度受限**：在ResNet-50等深层网络上，单路径优化面临严重的局部极值问题，不同随机种子产生差异巨大的重建结果（见Figure 2），缺乏稳定收敛机制。
- **高分辨率场景失效**：224×224像素的ImageNet图像包含丰富的纹理和结构信息，平均梯度中的信号稀释使得直接优化难以收敛到自然图像流形。

### 核心动机与研究问题

本文的核心动机直指上述假设的脆弱性：**梯度平均化是否真的能保护批次中个体样本的隐私？** 如果攻击者能够设计一种方法，从平均梯度中系统性地提取并解耦个体图像信息，那么当前联邦学习的安全边界就需要被重新审视。

具体而言，GradInversion试图回答一个此前被认为极其困难的问题：**能否从ResNet-50在ImageNet上批量大小为8乃至48的平均梯度中，恢复出高保真度的原始图像？** 这要求方法同时解决三个相互耦合的子问题：

1. **标签盲恢复**：在仅知晓平均梯度、不知晓任何样本标签的条件下，如何准确恢复批次中所有样本的真实标签？
2. **信息解耦**：如何从多张图像叠加的平均梯度信号中，分离并重建出每一张个体图像？
3. **优化稳定性**：如何克服深层网络优化地形的高度非凸性，使重建过程稳定收敛到自然图像而非噪声模式？

GradInversion的提出，正是为了在这些维度上实现突破，从而揭示梯度平均化隐私假设的潜在风险。



## 核心方法与创新机理

GradInversion的核心突破在于**将批次梯度反转从单样本、低分辨率、浅层网络的受限场景，推进到大批量（8–48）、高分辨率（224×224）、深层网络（ResNet-50）的ImageNet级真实图像恢复**。这一跨越的实现并非依赖单一技术，而是通过**标签恢复、梯度匹配损失、保真度正则化、组一致性正则化**四个关键模块的协同作用，从平均梯度中逐步解耦并融合个体图像信息。

### 关键创新点与Changed Slots

#### 1. 批次标签恢复：从求和到列最小值

先前方法**iDLG**（Zhao et al., arXiv 2020）仅能处理单张图像的标签推断，其扩展的求和规则在批次场景下准确率仅为95.89%。GradInversion提出基于全连接层梯度**列最小值（column-wise minimum）**的标签恢复方法：

$$\hat{\mathbf{y}} = \arg \operatorname{sort}\left( \operatorname*{min}_{m} \nabla_{\mathbf{W}_{m,n}^{(\mathrm{FC})}} \mathcal{L}(\mathbf{x}^*, \mathbf{y}^*) \right)[:K]$$

其核心洞察在于：对于正确类别的FC层权重梯度，其对应列的符号具有一致性，而列最小值操作能有效抑制跨样本的梯度噪声。在ImageNet批大小为8时，该方法将标签恢复准确率从95.89%提升至**99.56%**（Table 1），为后续图像重建提供了近乎完美的标签条件。该方法假设批次内无重复标签，在类别数远大于批量大小时成立。

#### 2. 梯度匹配损失：余弦相似度到ℓ2距离

**Geiping et al.**（NeurIPS 2020）首次将梯度反转推至ImageNet规模，但其使用的**余弦相似度**损失在批次梯度匹配中存在信息损失。GradInversion改用跨层求和的**ℓ2距离**：

$$\mathcal{L}_{\mathrm{grad}}(\hat{\mathbf{x}}; \mathbf{W}, \Delta \mathbf{W}) = \alpha_{\mathrm{G}} \sum_{l} || \nabla_{\mathbf{W}^{(l)}} \mathcal{L}(\hat{\mathbf{x}}, \hat{\mathbf{y}}) - \Delta \mathbf{W}^{(l)} ||_2$$

消融实验（Appendix Table 5）证实ℓ2距离在所有指标上均优于余弦相似度：ℓ2距离3.835 vs 5.965，符号匹配率80.9% vs 79.0%，余弦距离0.110 vs 0.139。ℓ2损失对梯度幅度的敏感性使其能更精确地约束合成图像的梯度方向与强度。

#### 3. 保真度正则化：引入BN统计先验

**DLG**（Zhu et al., NeurIPS 2019）和Geiping et al.的方法缺乏有效的图像先验约束，重建结果常呈现噪声或伪影。GradInversion引入由TV、ℓ2范数和**BN统计匹配**组成的保真度正则化：

$$\mathcal{R}_{\mathrm{fidelity}}(\hat{\mathbf{x}}) = \alpha_{\mathrm{tv}} \mathcal{R}_{\mathrm{TV}}(\hat{\mathbf{x}}) + \alpha_{\ell_2} \mathcal{R}_{\ell_2}(\hat{\mathbf{x}}) + \alpha_{\mathrm{BN}} \mathcal{R}_{\mathrm{BN}}(\hat{\mathbf{x}})$$

其中BN正则化项借鉴**DeepInversion**（Yin et al., CVPR 2020）的思想，惩罚合成图像在BN层的均值与方差偏离网络存储的统计量。消融实验（Table 2）表明，仅添加保真度正则化即可将PSNR从10.753提升至**12.058**，LPIPS从0.919降至**0.655**，说明BN统计量作为强先验能有效引导图像向自然分布收敛。

#### 4. 组一致性正则化：多路径配准平均

这是GradInversion最具原创性的贡献。作者观察到单路径优化因随机种子不同而产生显著的重建差异（Figure 2），不同种子捕获了原始图像的不同空间平移版本。组一致性正则化通过**多随机种子联合优化**，利用RANSAC-flow配准构建共识图像，并惩罚各路径偏离：

$$\mathcal{R}_{\mathrm{group}}(\hat{\mathbf{x}}, \hat{\mathbf{x}}_{g \in G}) = \alpha_{\mathrm{group}} || \hat{\mathbf{x}} - \mathbb{E}(\hat{\mathbf{x}}_{g \in G}) ||_2$$

其中期望图像通过配准后的像素平均计算：

$$\mathbb{E}(\hat{\mathbf{x}}_{g \in G}) = \frac{1}{|G|} \sum_{g} \mathbf{F}_{\hat{\mathbf{x}}_{g} \to \frac{1}{|G|}\sum_{g}\hat{\mathbf{x}}_{g}} (\hat{\mathbf{x}}_{g})$$

该设计的关键在于**克服了梯度平均带来的空间平移不变性**——不同种子的重建在空间上存在偏移，直接平均会模糊细节，而配准后平均能保留高频信息。实验表明，加入组一致性正则化（配准版本）将PSNR进一步提升至**12.929**，LPIPS降至**0.484**（Table 2），实现了从“可辨识轮廓”到“可识别细节”的质变。

#### 5. 噪声注入：Langevin动力学启发的优化

GradInversion在每次迭代中向合成图像添加像素级高斯噪声：

$$\hat{\mathbf{x}}^{(t)} = \hat{\mathbf{x}}^{(t-1)} + \lambda(t)\Delta_{\hat{\mathbf{x}}^{(t)}} + \lambda(t)\alpha_n \eta$$

这一设计的动机源于Langevin动力学，旨在帮助优化过程逃离局部极小值，增强对梯度匹配空间中非凸性的鲁棒性。

### 创新协同机制

上述创新并非孤立生效，而是形成了**层级递进的信息提取管道**：标签恢复提供准确的类别锚点→ℓ2梯度匹配约束合成图像的梯度信号→保真度正则化引入自然图像先验→组一致性正则化通过多路径配准融合互补信息。消融实验（Table 2）清晰展示了这一递进关系：仅梯度匹配（PSNR 10.753, LPIPS 0.919）→添加保真度（PSNR 12.058, LPIPS 0.655）→添加组一致性lazy版本（PSNR 12.524, LPIPS 0.554）→添加组一致性配准版本（PSNR 12.929, LPIPS 0.484），每一步均带来显著的定量与定性提升。

值得注意的是，**最优重建质量依赖目标批次的精确BN统计量**（Table 4中BN_exact vs BN_approx的差异），这意味着在标准联邦学习设置中，若服务器无法获取批次级BN统计量，恢复保真度将有所下降。这一依赖关系既是方法有效性的关键支撑，也是其实际攻击场景中的限制因素。



![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2104_07586/figures/001_Figure_1.jpg]]
*Figure 1: (a) Inverting averaged gradients to recover original image batches (b) Overview of our proposed GradInversion method Figure 1: We propose (a) GradInversion to recover hidden training image batches with high fidelity via inverting averaged gradients. GradInversion formulates (b) an optimization process that transforms noise to input images (Sec. 3.1). It starts with label restoration from the gradient of the fully connected layer (Sec. 3.2), then optimizes inputs to match target gradients under fidelity regularization (Sec. 3.3) and registration-based group consistency regularization (Sec. 3.4) to improve reconstruction quality. This enables recovery of 224 ˆ 224 pixel ImageNet samples from...*

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2104_07586/figures/003_Figure_3.jpg]]
*Figure 3: Overview of group consistency regularization*

GradInversion 将批次图像恢复建模为一个从随机噪声到自然图像的优化问题。其核心流程由五个紧密协作的模块构成，输入为目标批次的平均梯度 $\Delta \mathbf{W}$ 和网络权重 $\mathbf{W}$，输出为恢复的图像批次 $\hat{\mathbf{x}}^*$。

### 优化目标

整个框架围绕以下总体目标函数展开（Eqn. 1）：

$$\hat{\mathbf{x}}^* = \underset{\hat{\mathbf{x}}}{\mathrm{argmin}} \ L_{\mathrm{grad}}(\hat{\mathbf{x}}; \mathbf{W}, \Delta \mathbf{W}) + \mathcal{R}_{\mathrm{aux}}(\hat{\mathbf{x}})$$

其中 $L_{\mathrm{grad}}$ 为梯度匹配损失，$\mathcal{R}_{\mathrm{aux}}$ 为辅助正则化项，由保真度正则化 $\mathcal{R}_{\mathrm{fidelity}}$ 和组一致性正则化 $\mathcal{R}_{\mathrm{group}}$ 组成（Eqn. 2）：

$$\mathcal{R}_{\mathrm{aux}}(\hat{\mathbf{x}}) = \mathcal{R}_{\mathrm{fidelity}}(\hat{\mathbf{x}}) + \mathcal{R}_{\mathrm{group}}(\hat{\mathbf{x}})$$

优化过程从高斯噪声初始化开始，在梯度匹配损失的引导下逐步逼近真实图像分布，同时通过双重正则化克服梯度平均化带来的信息混淆和空间平移不变性。

### 模块流程与依赖关系

整个 pipeline 按以下顺序执行，各模块之间存在明确的数据依赖：

**1. 随机噪声初始化** — 合成输入批次 $\hat{\mathbf{x}}$ 的每个像素独立地从 $\mathcal{N}(0,1)$ 中采样（Sec. 3.1, 4. Experiments）。这一阶段不依赖任何梯度信息，仅提供优化的起始点。

**2. 批次标签恢复** — 在图像优化开始之前，先从全连接层的平均梯度中恢复批次内各样本的真实标签 $\hat{\mathbf{y}}$。核心机制是利用 FC 层梯度的列最小值特性：对于每个类别对应的梯度列，取特征维度上的最小值，然后排序选取最小的 $K$ 个列索引作为恢复标签（Eqn. 8）：

$$\hat{\mathbf{y}} = \arg \operatorname{sort}\left( \operatorname*{min}_{m} \nabla_{\mathbf{W}_{m,n}^{(\mathrm{FC})}} \mathcal{L}(\mathbf{x}^*, \mathbf{y}^*) \right)[:K]$$

该模块的输出 $\hat{\mathbf{y}}$ 是后续梯度匹配损失计算的必要输入。在 ImageNet 训练集批大小为 8 时，标签恢复准确率达 99.56%（Table 1）。需注意该方法假设批次内无重复标签，在类别数远大于批量大小时该假设通常成立。

**3. 梯度匹配损失** — 利用恢复的标签 $\hat{\mathbf{y}}$ 计算合成图像梯度与目标平均梯度之间的 ℓ2 距离，在所有网络层上求和（Eqn. 3）：

$$\mathcal{L}_{\mathrm{grad}}(\hat{\mathbf{x}}; \mathbf{W}, \Delta \mathbf{W}) = \alpha_{\mathrm{G}} \sum_{l} || \nabla_{\mathbf{W}^{(l)}} \mathcal{L}(\hat{\mathbf{x}}, \hat{\mathbf{y}}) - \Delta \mathbf{W}^{(l)} ||_2$$

消融实验表明，ℓ2 距离在梯度符号匹配率（80.9% vs 79.0%）和余弦距离（0.110 vs 0.139）上均优于先前方法采用的余弦相似度（Appendix Table 5）。该损失是驱动图像内容恢复的主要信号。

**4. 保真度正则化** — 在梯度匹配的基础上，引入三项图像先验约束（Eqn. 9）：

$$\mathcal{R}_{\mathrm{fidelity}}(\hat{\mathbf{x}}) = \alpha_{\mathrm{tv}} \mathcal{R}_{\mathrm{TV}}(\hat{\mathbf{x}}) + \alpha_{\ell_2} \mathcal{R}_{\ell_2}(\hat{\mathbf{x}}) + \alpha_{\mathrm{BN}} \mathcal{R}_{\mathrm{BN}}(\hat{\mathbf{x}})$$

- **总变差正则化** $\mathcal{R}_{\mathrm{TV}}$：抑制高频噪声，促进图像平滑。
- **ℓ2 范数正则化** $\mathcal{R}_{\ell_2}$：约束像素值范围，防止发散。
- **BN 统计匹配** $\mathcal{R}_{\mathrm{BN}}$：惩罚合成图像批次的均值与方差偏离网络存储的 BN 统计量（Eqn. 10），这是从 **DeepInversion**（Yin et al., CVPR 2020）借鉴的关键技术。消融实验显示，加入保真度正则化使 PSNR 从 10.753 提升至 12.058，LPIPS 从 0.919 降至 0.655（Table 2）。

**5. 组一致性正则化** — 针对单路径优化中不同随机种子产生显著视觉差异的问题（Figure 2），引入多种子联合优化机制。使用 $|G|$ 个随机种子并行优化（论文中 $|G|=8$），每个种子独立初始化并添加像素级扰动。核心操作是计算配准后的期望图像作为共识目标（Eqn. 12）：

$$\mathbb{E}(\hat{\mathbf{x}}_{g \in G}) = \frac{1}{|G|} \sum_{g} \mathbf{F}_{\hat{\mathbf{x}}_{g} \to \frac{1}{|G|}\sum_{g}\hat{\mathbf{x}}_{g}} (\hat{\mathbf{x}}_{g})$$

其中 $\mathbf{F}$ 为 RANSAC-flow 配准操作，将每个种子的重建图像对齐到像素均值后再平均。正则化项惩罚各候选图像与共识图像的 ℓ2 距离（Eqn. 11）：

$$\mathcal{R}_{\mathrm{group}}(\hat{\mathbf{x}}, \hat{\mathbf{x}}_{g \in G}) = \alpha_{\mathrm{group}} || \hat{\mathbf{x}} - \mathbb{E}(\hat{\mathbf{x}}_{g \in G}) ||_2$$

配准从 5000 次迭代后开始，每 100 次迭代执行一次。最终配准平均（Rgroup.reg）在 Table 2 中达到最佳指标：PSNR 12.929，LPIPS 0.484。

**6. Langevin 动力学噪声注入** — 在每次迭代更新中，向像素添加高斯噪声，帮助优化过程逃离局部极小值（Sec. 3.5）：

$$\hat{\mathbf{x}}^{(t)} = \hat{\mathbf{x}}^{(t-1)} + \lambda(t)\Delta_{\hat{\mathbf{x}}^{(t)}} + \lambda(t)\alpha_n \eta, \quad \eta \sim \mathcal{N}(0,1)$$

优化器使用 Adam，初始学习率 0.1 配合余弦衰减，前 50 次迭代作为预热阶段。损失权重设置为 $\alpha_{\mathrm{tv}}=1\times10^{-4}$，$\alpha_{\ell_2}=1\times10^{-6}$，$\alpha_{\mathrm{BN}}=0.1$，$\alpha_{\mathrm{G}}=0.001$，$\alpha_{\mathrm{group}}=0.01$，$\alpha_n=0.2$。

### 信息流与关键瓶颈

整个框架的信息流可总结为：**平均梯度 → 标签恢复 → 梯度匹配驱动内容重建 → 保真度正则化约束图像自然性 → 组一致性正则化融合多路径信息**。其中，标签恢复的准确性是梯度匹配有效性的前提条件；而组一致性正则化是克服梯度平均化导致的空间模糊和个体信息混淆的关键瓶颈突破——它通过多视角配准平均，从不同初始化路径中提取并融合一致的个体图像特征，使得批量大小高达 48 时仍有约 28% 的样本可被正确辨识（Figure 8）。

需要注意的是，最优重建质量依赖于目标批次的精确 BN 统计量（BN_exact），该信息在标准联邦学习设置中通常不可得。此外，优化过程因多种子联合训练和迭代配准而具有较高的计算开销。



GradInversion将批次图像恢复形式化为一个从随机噪声到自然图像的优化过程。其核心由五个模块级联构成，每个模块对应一个关键公式。

### 3.1 整体优化目标

整个方法的优化目标为：

$$\hat{\mathbf{x}}^* = \underset{\hat{\mathbf{x}}}{\mathrm{argmin}} \ L_{\mathrm{grad}}(\hat{\mathbf{x}}; \mathbf{W}, \Delta \mathbf{W}) + \mathcal{R}_{\mathrm{aux}}(\hat{\mathbf{x}})$$

其中 $\hat{\mathbf{x}}$ 为待优化的合成输入批次，$\mathbf{W}$ 为网络参数，$\Delta \mathbf{W}$ 为目标平均梯度。辅助正则化项 $\mathcal{R}_{\mathrm{aux}}$ 进一步分解为保真度正则化与组一致性正则化之和：

$$\mathcal{R}_{\mathrm{aux}}(\hat{\mathbf{x}}) = \mathcal{R}_{\mathrm{fidelity}}(\hat{\mathbf{x}}) + \mathcal{R}_{\mathrm{group}}(\hat{\mathbf{x}})$$

### 3.2 梯度匹配损失

梯度匹配损失采用各层梯度之间的 $\ell_2$ 距离，而非先前工作（如Geiping et al., NeurIPS 2020）使用的余弦相似度。消融实验（Appendix Table 5）证实 $\ell_2$ 距离在梯度距离、符号匹配率和余弦距离上均优于余弦相似度：

$$\mathcal{L}_{\mathrm{grad}}(\hat{\mathbf{x}}; \mathbf{W}, \Delta \mathbf{W}) = \alpha_{\mathrm{G}} \sum_{l} || \nabla_{\mathbf{W}^{(l)}} \mathcal{L}(\hat{\mathbf{x}}, \hat{\mathbf{y}}) - \Delta \mathbf{W}^{(l)} ||_2$$

其中 $\alpha_{\mathrm{G}}$ 为梯度损失的缩放系数（实验中设为 $0.001$），$l$ 遍历网络所有层，$\nabla_{\mathbf{W}^{(l)}} \mathcal{L}(\hat{\mathbf{x}}, \hat{\mathbf{y}})$ 为合成批次在恢复标签 $\hat{\mathbf{y}}$ 下的梯度，$\Delta \mathbf{W}^{(l)}$ 为第 $l$ 层的目标平均梯度。

### 3.3 批次标签恢复

批次平均梯度由各样本梯度均值构成：

$$\nabla_{\mathbf{W}} \mathcal{L}(\mathbf{x}^*, \mathbf{y}^*) = \frac{1}{K} \sum_k \nabla_{\mathbf{W}} \mathcal{L}(x_k, y_k)$$

对于全连接层，每样本梯度可通过链式法则分解为损失对logit的偏导与logit对权重的偏导之积。基于此结构，GradInversion提出对平均FC层梯度沿特征维度取列最小值，再排序取前 $K$ 个作为恢复标签：

$$\hat{\mathbf{y}} = \arg \operatorname{sort}\left( \operatorname*{min}_{m} \nabla_{\mathbf{W}_{m,n}^{(\mathrm{FC})}} \mathcal{L}(\mathbf{x}^*, \mathbf{y}^*) \right)[:K]$$

其中 $m$ 为输入特征维度索引，$n$ 为类别索引，$K$ 为批次大小。该方法假设批次内无重复标签，在ImageNet 1000类任务中该假设通常成立。相比将iDLG（Zhao et al., arXiv 2020）的求和规则直接扩展到批次的基线方法（准确率95.89%），列最小值法在批大小为8时达到99.56%的标签恢复准确率（Table 1）。

### 3.4 保真度正则化

保真度正则化由三项组成，分别约束图像的平滑性、幅度和统计分布：

$$\mathcal{R}_{\mathrm{fidelity}}(\hat{\mathbf{x}}) = \alpha_{\mathrm{tv}} \mathcal{R}_{\mathrm{TV}}(\hat{\mathbf{x}}) + \alpha_{\ell_2} \mathcal{R}_{\ell_2}(\hat{\mathbf{x}}) + \alpha_{\mathrm{BN}} \mathcal{R}_{\mathrm{BN}}(\hat{\mathbf{x}})$$

其中 $\alpha_{\mathrm{tv}}=10^{-4}$、$\alpha_{\ell_2}=10^{-6}$、$\alpha_{\mathrm{BN}}=0.1$。BN统计匹配项（源自DeepInversion, Yin et al., CVPR 2020）惩罚合成批次的逐层均值与方差偏离网络存储的BN统计量：

$$\mathcal{R}_{\mathrm{BN}}(\hat{\mathbf{x}}) = \sum_{l} || \mu_l(\hat{\mathbf{x}}) - \mathbf{BN}_l(\mathrm{mean}) ||_2 + \sum_{l} || \sigma_l^2(\hat{\mathbf{x}}) - \mathbf{BN}_l(\mathrm{variance}) ||_2$$

消融实验（Table 2）表明，添加保真度正则化使PSNR从10.753提升至12.058，LPIPS从0.919降至0.655。

### 3.5 组一致性正则化

单路径优化因随机种子不同而产生显著的重建差异（Figure 2）。组一致性正则化通过联合优化多个随机种子，并惩罚各候选图像与组共识图像的偏差来解决此问题：

$$\mathcal{R}_{\mathrm{group}}(\hat{\mathbf{x}}, \hat{\mathbf{x}}_{g \in G}) = \alpha_{\mathrm{group}} || \hat{\mathbf{x}} - \mathbb{E}(\hat{\mathbf{x}}_{g \in G}) ||_2$$

其中 $\alpha_{\mathrm{group}}=0.01$。组共识图像 $\mathbb{E}(\hat{\mathbf{x}}_{g \in G})$ 并非简单的像素平均，而是先计算像素均值作为配准目标，再通过RANSAC-flow将各组内图像配准后取平均：

$$\mathbb{E}(\hat{\mathbf{x}}_{g \in G}) = \frac{1}{|G|} \sum_{g} \mathbf{F}_{\hat{\mathbf{x}}_{g} \to \frac{1}{|G|}\sum_{g}\hat{\mathbf{x}}_{g}} (\hat{\mathbf{x}}_{g})$$

其中 $\mathbf{F}_{A \to B}$ 表示将图像 $A$ 向目标 $B$ 配准的RANSAC-flow变换。实验中使用8个随机种子，在5000次初始迭代后启动配准，之后每100次迭代更新一次。配准平均（Rgroup.reg）相比简单平均（Rgroup.lazy）进一步将PSNR从12.524提升至12.929，LPIPS从0.554降至0.484（Table 2）。

### 3.6 优化过程与噪声注入

优化采用Adam优化器，学习率0.1配合余弦衰减，前50次迭代为预热阶段。受Langevin动力学启发，每次更新时注入像素级高斯噪声以帮助逃离局部极小：

$$\hat{\mathbf{x}}^{(t)} = \hat{\mathbf{x}}^{(t-1)} + \lambda(t) \Delta_{\hat{\mathbf{x}}^{(t)}} + \lambda(t) \alpha_n \eta$$

其中 $\lambda(t)$ 为当前学习率，$\Delta_{\hat{\mathbf{x}}^{(t)}}$ 为Adam更新方向，$\eta \sim \mathcal{N}(0,1)$ 为标准高斯噪声，噪声缩放系数 $\alpha_n=0.2$。



## 实验与关键发现

### 核心实验设置与评估协议

GradInversion的实验主要在ImageNet1K数据集上展开，目标网络为ResNet-50。合成图像批次从独立同分布的高斯噪声 $\mathcal{N}(0,1)$ 初始化，使用Adam优化器，初始学习率0.1，配合余弦衰减策略，前50次迭代作为预热阶段。损失权重配置为：$\alpha_{tv}=1\times10^{-4}$，$\alpha_{\ell_2}=1\times10^{-6}$，$\alpha_{BN}=0.1$，$\alpha_G=0.001$，$\alpha_{group}=0.01$，噪声尺度 $\alpha_n=0.2$。组一致性正则化采用8个随机种子联合优化，每个种子对应不同的高斯初始化和像素级扰动；图像配准在5K次初始优化迭代后启动，此后每100次迭代执行一次RANSAC-flow配准，以像素均值作为配准目标。

评估指标覆盖像素空间、感知空间和频域三个维度：PSNR（峰值信噪比）、LPIPS（学习感知图像块相似度）和FFT2D（二维傅里叶变换距离）。此外，引入图像可辨识精度（Image Identifiability Precision, IIP）作为安全性度量，定义为原始图像与其重建结果在avgpool特征空间余弦相似度最近邻中精确匹配的比例。

### 主结果：标签恢复与图像重建

**标签恢复精度。** Table 1报告了在10K个随机ImageNet样本上、不同批量大小下的标签恢复准确率。在批量大小为8时，GradInversion的列最小值方法达到99.56%的准确率，显著优于基于求和规则扩展的先前方法（95.89%）。随着批量增大，标签恢复准确率自然下降，但即使在批量大小为48时仍保持较高水平，验证了全连接层梯度符号信息在批量场景下的鲁棒判别能力。需要指出的是，该方法假设批次内无重复标签——在ImageNet的1000类设定下，批量大小远小于类别数，这一假设通常成立。

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2104_07586/figures/005_Table_1.jpg]]
*Table 1: Average restoration accuracy over 10K random samples of different batch size from the ImageNet training/validation sets without label repeats. :: the original method [53] only works for single image - we extend it by adopting its sum rule for Eqn. 7 and then show improvements*

**图像重建质量。** Table 4给出了GradInversion与现有方法在ResNet-50 ImageNet梯度反转任务上的定量对比。使用精确BN统计量（$\text{BN}_\text{exact}$）的完整方法取得最优指标：LPIPS 0.484，PSNR 12.929，FFT2D 0.175。相比之下，先前方法在批量场景下几乎无法恢复有意义的视觉内容。Figure 4的定性对比进一步印证了这一优势：GradInversion恢复的图像展现出清晰的物体轮廓、纹理细节和合理的色彩分布，而DLG和Geiping等人的方法仅能产生模糊的色块或噪声模式。在批量大小为1的挑战性样本上（Figure 5），GradInversion同样优于先前方法，能够恢复出更丰富的结构信息。

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2104_07586/figures/010_Figure_5.jpg]]
*Figure 5: Comparison with prior art on ResNet-50 (ImageNet) gradient inversion at batch size 1 for a “challenging” sample from [13]*

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2104_07586/figures/009_Table_4.jpg]]
*Table 4: Comparison of GradInversion with state-of-the-art methods for ResNet-50 gradient inversion on ImageNet1K. BNapprox. denotes regularizing towards BN statistics in the network learnt from the original dataset; $\mathtt { B N } _ { \mathrm { e x a c t } }$ denotes the BN statistics of target batch shared (or leaked) in distributed setup for global BN updates, e.g., Synchronized Batch Normalization [49]

**特征提取器强度的影响。** Table 3比较了不同骨干网络下的重建质量。使用MOCO V2自监督预训练的ResNet-50产生的梯度比标准监督训练的ResNet-50泄漏更多信息，重建指标更优。这一现象表明，更强的特征提取器在梯度中编码了更丰富的输入信号，从而放大了隐私风险。

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2104_07586/figures/007_Table_2.jpg]]
*Table 2: Ablation study when each proposed loss to optimization objective function - quantitative (up) and qualitative (bottom) comparison. Original batch contains 8 samples - we show 4 samples visually here amid space limit, see Appendix for entire batch. Table 3: Reconstruction under varying feature extraction strength*

### 消融实验：各组件的贡献

Table 2系统性地拆解了各损失项对重建质量的贡献，消融基线为仅使用梯度匹配损失 $\mathcal{L}_{grad}$ 的版本：

- **基线（仅 $\mathcal{L}_{grad}$）**：PSNR 10.753，LPIPS 0.919。重建图像呈现粗糙的色块，物体轮廓模糊，几乎无法辨识语义内容。
- **+保真度正则化（$\mathcal{R}_{fidelity}$）**：PSNR提升至12.058（+1.305），LPIPS降至0.655（-0.264）。TV正则化抑制了高频噪声，BN统计匹配引导合成图像向自然图像分布靠拢，使得物体形状和纹理显著改善。
- **+组一致性正则化-惰性平均（$+\mathcal{R}_{group.lazy}$）**：PSNR进一步提升至12.524，LPIPS降至0.554。多种子联合优化通过惩罚各路径与像素均值的偏差，有效抑制了单路径优化中的空间错位和模式崩溃。
- **+组一致性正则化-配准平均（$+\mathcal{R}_{group.reg}$）**：完整方法达到PSNR 12.929，LPIPS 0.484。RANSAC-flow配准校正了不同种子间的空间平移，使得共识图像更加锐利，细节保真度显著提升。

Table 5（附录）进一步比较了梯度匹配损失函数的选择：ℓ2距离在梯度距离（3.835 vs 5.965）、符号匹配率（80.9% vs 79.0%）和余弦距离（0.110 vs 0.139）三个维度上全面优于余弦相似度，为损失函数设计提供了实证依据。


### 批量大小与安全边界

Figure 6展示了批量大小对重建质量的影响：随着批量从1增大到48，恢复图像的视觉细节逐渐减少，但即使在批量大小为48时，物体类别和大致形状仍然可辨。Figure 8以图像可辨识精度（IIP）量化了这一趋势——批量大小为48时，约28%的样本仍可通过重建被正确识别。这一发现直接挑战了“大批量梯度平均化足以保护隐私”的普遍假设，揭示了当前联邦学习框架中梯度共享机制的系统性脆弱性。

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2104_07586/figures/012_Figure_6.jpg]]
*Figure 6: Reduced amount of restored original visual features as batch size increases*

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2104_07586/figures/011_Figure_7.jpg]]
*Figure 7: Varying level of information leakage at batch size 48 on ImageNet validation set. Each block containing a pair of (left) original sample and its (right) reconstruction by GradInversion. Figure 8: The Image Indentifiability Precision (IIP) curve of Grad-Inversion on ImageNet validation set, as a function of increasing batch size. Each point averaged per 256 randomly selected samples of varying batch sizes (240 samples for batch size 48). Nearest neighbors measured in avgpool feature space cosine similarity*

### 失败模式与局限性

尽管GradInversion在自然图像上取得了突破性进展，但仍存在明确的失败模式：

1. **人脸重建的语义错位**：人脸图像的重建存在严重的特征空间错位问题，无法恢复正确的人脸结构。这源于人脸识别任务对空间对齐的高度敏感性，而当前的组一致性正则化尚不足以校正此类细粒度几何变形。
2. **文字与数字的细节丢失**：虽然文字和数字区域能够被检测到，但重建结果模糊，无法精准重现具体字符。这表明高频细节信息在梯度平均化过程中被不可逆地稀释。
3. **精确BN统计的依赖**：最优重建质量依赖于目标批次的精确BN统计量（$\text{BN}_\text{exact}$），而在标准联邦学习设置中，服务器通常只能访问全局BN统计量（$\text{BN}_\text{approx}$）。使用近似BN统计量会导致重建质量下降，这限制了该方法在实际攻击场景中的直接适用性。
4. **计算开销**：8种子联合优化配合周期性RANSAC-flow配准显著增加了计算负担，使得该方法在实时攻击场景中的应用受限。
5. **泛化性待验证**：实验主要局限于ImageNet和ResNet-50架构，对于其他数据分布（如医学影像、文本嵌入）和更深网络（如ResNet-101）的泛化性能尚未得到充分检验。







## 定位与知识库关联

### 梯度反转攻击的技术演进与GradInversion的定位

GradInversion的提出建立在一个清晰的瓶颈突破之上：联邦学习等分布式训练中，模型梯度由批次数据平均计算而来，平均化操作长期被认为可以掩盖单个样本的信息。然而，此前的梯度反转方法仅能在极其受限的条件下（单一样本、浅层网络、低分辨率）恢复图像，无法扩展到复杂网络和大批量高分辨率场景。

**DLG**（Zhu et al., NeurIPS 2019）首次证明了从共享梯度中恢复训练数据的可能性，但其方法需要联合优化伪标签和输入，且仅在小批量浅层网络上有效。**iDLG**（Zhao et al., arXiv 2020）改进了单图像场景下的标签恢复，通过全连接层梯度的符号信息直接推断标签，但该方法无法直接处理批次数据。**Geiping et al.**（NeurIPS 2020）首次将梯度反转推进到ImageNet尺度的单图像重建，采用余弦相似度作为梯度匹配损失，但其方法在大批量场景下性能急剧退化。

GradInversion的核心突破在于识别并解耦了批次梯度反转的三个因果环节：**标签恢复**、**梯度匹配**和**保真度约束**。通过将全连接层梯度的列最小值与排序操作结合（Eqn. 8），GradInversion实现了鲁棒的多标签恢复，在ImageNet批大小为8时准确率达到99.56%，远超扩展求和规则的95.89%（Table 1）。在梯度匹配层面，GradInversion改用ℓ2距离替代余弦相似度，实验表明ℓ2距离在梯度距离、符号匹配率和余弦距离三个维度上均更优（Appendix Table 5）。在保真度层面，GradInversion整合了来自**DeepInversion**（Yin et al., CVPR 2020）的BN统计匹配思想，将其与TV正则化和ℓ2范数结合，形成系统的保真度正则化项（Eqn. 9），使PSNR提升1.305、LPIPS降低0.264（Table 2消融实验）。

### 组一致性正则化的创新机制

GradInversion最具特色的贡献是组一致性正则化。该方法观察到：不同随机种子初始化的单路径优化会产生空间平移和局部细节差异（Figure 2），但这些差异可以通过多路径联合优化来弥合。具体而言，GradInversion同时优化多个随机种子初始化的输入，利用RANSAC-flow图像配准将各路径的重建结果对齐到像素均值，形成共识图像，再以此作为正则化目标惩罚偏离（Eqn. 11-12）。这一设计使得完整方法在ImageNet梯度反转上达到LPIPS 0.484、PSNR 12.929、FFT2D 0.175（Table 2），显著优于所有先前方法。值得注意的是，即使使用简单的懒惰平均（lazy mean）而非配准平均，组一致性正则化仍能带来可观的性能提升，这验证了多路径联合优化本身的价值。

### 适用边界与关键假设

GradInversion的有效性依赖于几个关键假设，这些假设定义了其适用边界：

1. **标签不重复假设**：批次标签恢复算法假设批次内不存在重复标签。在ImageNet（1000类）等类别数远大于批量大小的场景下，该假设通常成立；但在小规模类别任务中可能失效。
2. **BN统计量的可得性**：最优重建质量依赖目标批次的精确BN统计量（BN_exact），这在实际联邦学习设置中通常不可得。使用网络预训练时的近似BN统计量（BN_approx）会导致性能下降。
3. **网络架构依赖性**：实验表明，更强的特征提取器（如MOCO V2预训练的ResNet-50）会泄漏更多信息（Table 3），这意味着梯度反转的风险与模型表达能力正相关。

### 已知局限与失败模式

尽管GradInversion在大批量高分辨率场景下取得了突破性进展，其局限性同样值得关注：

- **人脸重建的失败**：人脸恢复存在特征空间错位问题，难以重建正确的人脸结构。这源于组一致性正则化中的空间配准无法处理人脸这类对精确空间对齐要求极高的结构。
- **文字与数字的模糊**：文字与数字虽能被检测，但细节模糊，无法精准重现。这表明梯度信息对高频细节的保留能力有限。
- **计算开销**：优化过程需要多个随机种子（实验中为8个）的联合优化，并需在每100次迭代后执行RANSAC-flow配准，计算开销显著高于单路径方法。
- **批量大小的限制**：在批量大小为48时，仅有约28%的样本可以通过反转重建被正确识别（Image Identifiability Precision, Figure 8），表明信息泄漏程度随批量增大而显著衰减。
- **泛化性未充分验证**：评估主要基于ImageNet和ResNet-50，对不同数据分布（如医学图像、文本）和网络结构（如ViT、ResNet-101）的泛化性尚待验证。

### 开放问题与后续研究方向

GradInversion揭示的深层问题为后续研究指明了方向：

1. **信息传输机制的理论理解**：梯度到原始数据的底层信息传输机制是什么？能否通过特征空间分析量化信息泄漏程度？这一理论问题的解决将为防御策略设计提供基础。
2. **不依赖BN统计量的重建**：是否可能在不依赖BN统计量的前提下实现相似级别的重建保真度？这对于推广到无BN的网络架构（如Transformer）至关重要。
3. **防御技术的有效性评估**：梯度扰动、差分隐私等防御技术对GradInversion的效果影响如何？需要系统性的攻防对抗研究。
4. **更大规模场景的扩展**：对于更深的网络（如ResNet-101）和更大批量（如128+），恢复性能能否保持或进一步提升？这决定了该方法对实际联邦学习系统的威胁程度。
5. **结构化先验的引入**：在人脸识别等重视空间对齐的任务上，能否通过结构先验（如人脸关键点、3D形变模型）改进组一致性正则化以提升重建质量？

### 知识库定位总结

GradInversion在梯度反转攻击的知识谱系中占据关键位置：它首次证明了在复杂深度网络和大批量高分辨率场景下，梯度平均化不足以提供有效的隐私保护。该方法将此前分散在单图像反转（DLG/iDLG）、ImageNet尺度重建（Geiping et al.）和数据自由合成（DeepInversion）中的技术要素系统整合，并通过创新的组一致性正则化突破了批量场景的核心瓶颈。其成功不仅推动了攻击技术的发展，更对联邦学习等分布式训练框架的隐私保护假设提出了根本性质疑。



## 原文 PDF

![[paperPDFs/CVPR_2021/See_through_Gradients_Image_Batch_Recovery_via_GradInversion.pdf]]
