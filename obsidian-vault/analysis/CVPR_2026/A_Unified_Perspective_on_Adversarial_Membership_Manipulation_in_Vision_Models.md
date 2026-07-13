---
title: A Unified Perspective on Adversarial Membership Manipulation in Vision Models
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/A_Unified_Perspective_on_Adversarial_Membership_Manipulation_in_Vision_Models.pdf
project_link: null
code_link: "https://github.com/Sjtubrian/Adversarial_Membership_Manipulation"
aliases:
- MMAM
- UPAMMVM
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 输入梯度范数的塌缩轨迹——伪造成员在优化过程中梯度范数显著下降，形成低梯度、高置信度的几何特征，可作为区分真实与伪造成员的可靠信号。
primary_logic: 利用梯度几何信号（梯度范数）区分真实成员与伪造成员，并以此为基础构建检测器与对抗鲁棒的成员推理攻击，从而在不改变现有MIA设计的前提下大幅提升抗操纵能力。
claims:
- 伪造成员与真实成员在语义特征空间中高度重叠，但梯度范数分布存在明显分离。
- 基于动量余弦退火的MFA在多个数据集和MIA上显著提高错误面积和等错误率，性能优于倒置攻击基线。
- MFD检测器利用梯度范数阈值实现AUC > 0.9，且优于基于Mahalanobis距离和LID的特征检测方法。
- AR-MIAs通过梯度范数加权将基线MIA的AUC从0.4-0.7提升至0.78-0.85，同时显著降低等错误率。
---

# A Unified Perspective on Adversarial Membership Manipulation in Vision Models

> [!tip] 核心洞察
> 利用梯度几何信号（梯度范数）区分真实成员与伪造成员，并以此为基础构建检测器与对抗鲁棒的成员推理攻击，从而在不改变现有MIA设计的前提下大幅提升抗操纵能力。

| 字段 | 内容 |
|------|------|
| 中文题名 | 视觉模型中对抗性成员操作的一个统一视角 |
| 英文题名 | A Unified Perspective on Adversarial Membership Manipulation in Vision Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2604.02780) · [Code](https://github.com/Sjtubrian/Adversarial_Membership_Manipulation) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | 统一框架：成员伪造攻击（MFA）、成员伪造检测（MFD）与对抗鲁棒成员推理攻击（AR-MIA） |
| Dataset | CIFAR-10, CINIC-10, CIFAR-100 |

> [!tip] 效果简介
> - CIFAR-10 (∥δ∥∞ ≤ 4.0/255) 上，AUC 0.7871 (AR-Attack R λ=20) vs 0.4019 (Attack R Baseline) (+0.3852)；EER 29.80% (AR-Attack R λ=20) vs 58.20% (Attack R Baseline) (-28.40%)。
> - CINIC-10 (∥δ∥∞ ≤ 4.0/255) 上，AUC 0.8504 (AR-RMIA λ=20) vs 0.7219 (RMIA Baseline) (+0.1285)。
> - CIFAR-100 (∥δ∥∞ ≤ 4.0/255) 上，AUC 0.7881 (AR-Attack R λ=35) vs 0.6881 (Attack R Baseline) (+0.1000)。

## 概要

### 问题背景与核心瓶颈

成员推理攻击（Membership Inference Attack, MIA）是评估机器学习模型隐私泄露风险的关键审计工具。现有MIA方法——包括基于损失的**Loss Attack**、基于置信度校准的**Attack R**、利用影子模型似然比的**LiRA**，以及基于密度比校准的**RMIA**——均依赖语义置信度信号（如损失值、似然比）来判定样本是否属于训练集。然而，这些语义信号对输入空间的微小扰动缺乏鲁棒性：攻击者可以通过向非成员样本施加不可察觉的扰动，将其推入高置信度区域，从而伪造其成员身份，从根本上破坏隐私审计的完整性与可信度。

本文揭示了这一此前未被充分研究的安全威胁，并提出了一个统一框架，从攻击、检测和防御三个维度系统性地应对成员伪造问题。

### 核心发现：梯度几何信号

研究的关键发现在于，尽管伪造成员与真实成员在语义特征空间中高度重叠（t-SNE可视化表明二者在倒数第二层和倒数第三层特征上几乎无法区分，见Figure 4），但它们在**梯度几何空间**中存在显著分离。具体而言，在优化非成员样本以最大化目标类别置信度的过程中，输入梯度的范数会呈现稳定的塌缩轨迹（Figure 5）：随着优化步数增加，梯度范数持续下降，最终形成“低梯度、高置信度”的几何指纹。这一现象在理论上得到了支撑——在步长足够小的条件下，符号梯度下降可被证明导致梯度范数严格减小（Theorem 1）。该几何特征构成了区分真实成员与伪造成员的可靠信号。

### 统一框架：MFA–MFD–AR-MIA

基于上述洞察，本文提出一个包含三个组件的统一框架：

1. **成员伪造攻击（Member Fabrication Attack, MFA）**：通过动量累积与余弦退火步长调度，在ℓ∞扰动球内最大化目标类别置信度，将非成员伪造成高置信度“成员”。与传统的对抗攻击（如I-FGSM、I-PGD、I-CW等倒置基线）不同，MFA的目标不是造成误分类，而是将样本推入高置信度的成员区域（Figure 3）。

2. **成员伪造检测（Member Fabrication Detection, MFD）**：利用输入梯度范数作为检测统计量，通过设定阈值区分真实成员与伪造成员。实验表明，MFD的检测AUC超过0.9，显著优于基于Mahalanobis距离和局部内在维度（LID）的语义特征检测方法（Figure 6）。

3. **对抗鲁棒成员推理攻击（Adversarially Robust MIA, AR-MIA）**：将梯度范数通过tanh函数加权后与现有MIA统计量（如损失、似然比）相乘，在不改变原有MIA设计的前提下赋予其抵抗伪造攻击的能力。该策略使基线MIA在伪造攻击下的AUC从0.4–0.7大幅提升至0.78–0.85，同时显著降低等错误率（EER）。

### 方法谱系与知识库定位

本研究位于对抗机器学习与隐私审计的交叉地带。与传统的**对抗攻击**（Goodfellow et al., ICLR 2015; Madry et al., ICLR 2018）旨在降低模型准确率不同，MFA的目标是操纵成员推理信号，属于一类新型的**隐私审计对抗攻击**。在检测层面，MFD区别于基于语义特征空间的异常检测方法（如利用Mahalanobis距离或LID），转而利用梯度这一几何原语作为检测信号。AR-MIA则提供了一种轻量级的“即插即用”鲁棒化策略，可与**Loss Attack**、**Attack R**、**LiRA**（Carlini et al., S&P 2022）、**RMIA**（Zarifzadeh et al., NeurIPS 2024）等主流MIA方法无缝集成。

### 主要实验结果摘要

实验在CIFAR-10、CIFAR-100、CINIC-10、SVHN和ImageNet-100五个数据集上系统验证了框架的有效性：

- **MFA攻击效能**：动量余弦退火策略（Strategy IV）在错误面积和等错误率上均优于固定步长、半衰启发式及纯余弦退火方案（Table 1）。MFA在多种MIA上均能显著提升错误面积和等错误率，性能超越I-FGSM、I-PGD等倒置攻击基线（Tables 3–6）。

- **MFD检测能力**：基于梯度范数的检测器在不同扰动水平下均保持AUC > 0.9，且对MFA的检测效果优于Mahalanobis距离和LID方法（Figure 7(d–f)）。

- **AR-MIA鲁棒性**：在CIFAR-10上，AR-Attack R（λ=20）将Attack R的AUC从0.4019提升至0.7871，EER从58.20%降至29.80%（Table 7）；在CINIC-10上，AR-RMIA（λ=20）将RMIA的AUC从0.7219提升至0.8504（Table 9）。AR-LiRA和AR-RMIA同样在多个数据集上表现出一致的鲁棒性增益（Tables 8–9）。

### 局限与开放问题

本框架存在若干值得注意的局限。首先，MFA和MFD/AR-MIA均需要白盒梯度访问，在黑盒场景下需通过有限差分估计梯度，会引入精度损失和计算开销。其次，实验主要限于标准训练的图像分类模型，未在差分隐私等更强防御机制下充分验证。此外，超参数λ需要根据数据集和MIA类型进行离线校准，缺乏统一的自动化选择机制。

值得进一步探索的开放问题包括：梯度范数塌缩特征能否被完全自适应的MFA（同时优化置信度和梯度范数）彻底绕过；MFD和AR-MIA在Vision Transformer等新架构及大规模预训练模型上的泛化性如何；以及成员伪造攻击与模型提取、数据投毒等其他威胁结合时会产生怎样的复合隐私风险。

### 成员推理攻击的隐私审计困境

机器学习模型在训练过程中会记忆训练数据，这一现象催生了成员推理攻击（Membership Inference Attack, MIA）这一重要的隐私审计工具。给定一个样本 $(x,y)$ 和目标模型 $f_\theta$，MIA 通过构建统计量 $S(x,y)$ 并与阈值 $\tau$ 比较来推断该样本是否属于训练集：

$$I(x,y) = \mathbf{1}[S(x,y) > \tau]$$

现有的 MIA 方法——包括基于损失的 **Loss Attack**、基于置信度校准的 **Attack R**、利用影子模型似然比的 **LiRA** 以及基于密度比校准的 **RMIA**——本质上都依赖于模型的语义置信度信号。这些信号对不可察觉的输入扰动缺乏鲁棒性，构成了一个被长期忽视的安全缺口。

### 被忽视的威胁：成员身份伪造

问题的核心在于：攻击者可以通过对非成员样本施加人眼不可察觉的扰动，将其推入模型的高置信度区域，从而伪造其成员身份。如 Figure 2 所示，在 ImageNet-100 上仅需 $\epsilon = 2/255$ 的 $\ell_\infty$ 扰动，原始非成员与扰动后的伪造成员在人眼视觉上几乎无法区分，但模型对其置信度已发生根本性改变。

这一威胁的现实意义在于：当 MIA 被用于隐私审计、模型窃取检测或数据版权验证时，恶意方可以通过成员伪造系统性地破坏审计结果的完整性，使得非训练数据被错误标记为成员，从而掩盖真实的隐私泄露或捏造虚假的侵权证据。

### 语义特征空间的盲区

Figure 4 的 t-SNE 可视化揭示了一个关键现象：伪造成员与真实成员在倒数第二层和倒数第三层的语义特征空间中高度重叠。这意味着，无论是基于最终分类置信度还是中间层语义特征的检测方法，都难以有效区分二者。传统对抗样本检测中常用的 **Mahalanobis 距离**和**局部内在维度（LID）** 等特征，在成员伪造检测场景下同样表现出有限的分辨能力（见 Figure 6 左侧与中间子图）。

### 梯度几何信号的发现

本文的核心洞察在于：尽管伪造成员在语义空间中可以完美模仿真实成员，但伪造过程本身会在输入梯度空间中留下不可消除的几何痕迹。如 Figure 5 所示，随着 MFA 优化步骤的增加，输入梯度范数呈现持续衰减的趋势。这一现象的理论基础在于：当沿符号梯度方向移动以最大化目标类别置信度时，在小步长条件下梯度范数严格减小：

$$\|\nabla_{x'} \ell(f(x'), y)\| < \|\nabla_x \ell(f(x), y)\|$$

这种“梯度范数塌缩”使得伪造成员最终驻留在低梯度、高置信度的损失景观盆地中，而真实成员则处于中等梯度强度的区域。Figure 6 右侧子图清晰展示了梯度范数分布在伪造与真实成员之间的显著分离，其区分能力远超 Mahalanobis 距离和 LID。

### 统一视角的提出

基于上述发现，本文从一个统一视角出发，系统性地研究对抗性成员操作问题，提出三个相互关联的技术组件：

- **成员伪造攻击（MFA）**：形式化不可察觉扰动下的成员身份伪造，揭示现有 MIA 的脆弱性；
- **成员伪造检测（MFD）**：利用梯度范数作为几何指纹，构建可靠的伪造检测器；
- **对抗鲁棒成员推理攻击（AR-MIA）**：将梯度几何信号与原始 MIA 统计量融合，在不改变现有 MIA 设计的前提下大幅提升抗操纵能力。

这一框架首次将成员伪造的攻击、检测与鲁棒推理纳入统一分析，为隐私审计的安全性研究提供了新的理论基础和实用工具。

## 核心方法与创新机理

### 问题发现：语义信号不可靠，梯度几何信号才是关键

现有成员推理攻击（MIA）的核心脆弱性在于：它们依赖的语义置信度信号（如损失值、似然比）在不可察觉的输入扰动下缺乏鲁棒性。攻击者只需将非成员样本推入高置信度区域，就能伪造其成员身份，从而彻底破坏隐私审计的完整性。如Figure 4所示，伪造成员与真实成员在语义特征空间中高度重叠，使得基于语义特征的检测手段几乎失效。

本工作的关键洞察在于：**伪造成员在优化过程中会经历梯度范数的塌缩**——随着置信度被逐步推高，输入梯度范数显著下降，形成“低梯度、高置信度”的几何特征。这一几何信号与真实成员所处的“中等梯度”区域形成天然分离（Figure 6），为检测提供了可靠指纹。

### 方法创新：统一框架下的攻防博弈

论文构建了一个包含三个核心模块的统一框架，系统性地覆盖了攻击、检测与鲁棒推理三个维度：

**成员伪造攻击（MFA）** 将传统对抗攻击的目标从“最小化置信度以制造误分类”反转为“最大化真实类别置信度以伪造成员身份”。其优化目标为：

$$\forall x' \in \mathcal{B}_\epsilon[x], \quad \bar{x} = \arg\max_{x'} (p_y(x'))$$

MFA采用动量累积与余弦退火步长调度相结合的优化策略，在ℓ∞约束球内实现平滑、稳定的置信度上升。消融实验（Table 1）表明，该方案在错误面积（Error Area）和等错误率（EER）上均显著优于固定步长、半衰启发式及纯余弦退火等替代策略。

**成员伪造检测（MFD）** 利用梯度范数塌缩这一几何签名构造检测器：

$$\mathbf{T}(x,y) = \mathbf{1}[ \| \nabla_x \ell(f(x), y) \| \le \tau' ]$$

当输入梯度范数低于阈值τ′时，样本被判定为伪造成员。与基于Mahalanobis距离和局部内在维度（LID）的检测方法相比，MFD在AUC上具有压倒性优势（Figure 6），验证了梯度几何信号在区分伪造与真实成员方面的独特价值。

**对抗鲁棒成员推理攻击（AR-MIA）** 将梯度范数权重与现有MIA统计量相结合，在不改变原始攻击设计的前提下大幅提升抗操纵能力：

$$w(x,y) = \mathrm{tanh}\left( \lambda \cdot \| \nabla_x \ell(f(x), y) \| \right)$$

$$I(x,y) = \mathbf{1}\left[ w(x,y) \cdot S(x,y) > \tau \right]$$

tanh函数将权重限制在合理范围内，防止非成员的异常大梯度破坏统计量的区分力。实验表明，AR-MIA可将基线MIA（如Attack R、LiRA、RMIA）的AUC从0.4–0.7提升至0.78–0.85，同时将EER降低20个百分点以上（Tables 7-9）。

### 与基线的本质差异

| 维度 | 基线方法 | 本工作 |
|------|---------|--------|
| 攻击目标 | 最小化分类损失以降低置信度（传统对抗攻击） | 最大化真实类别置信度以伪造成员身份（MFA） |
| 检测机制 | 无针对性检测或基于语义特征（Mahalanobis、LID） | 基于输入梯度范数塌缩的几何检测器（MFD） |
| MIA鲁棒性 | 直接使用原始统计量（损失、似然比） | 通过tanh加权的梯度范数将几何信号与统计量融合（AR-MIA） |

这一统一视角的核心贡献在于：**揭示了成员伪造与检测之间的几何博弈本质**，并证明梯度范数塌缩是可利用的可靠信号——它既是伪造过程的必然副产物，也是检测和鲁棒推理的天然锚点。

本文提出的统一框架围绕“对抗性成员操作”这一核心威胁构建，将攻击、检测与鲁棒推理三个环节纳入同一个形式化体系。框架的起点是一个已被观察到但未被系统化研究的瓶颈：现有成员推理攻击（MIA）——如 **Loss Attack**、**Attack R**、**LiRA**（Carlini et al., S&P 2022）和 **RMIA**——依赖损失值、置信度或似然比等语义统计量进行成员/非成员判别。这些统计量对输入空间的微小扰动缺乏结构鲁棒性，攻击者只需将非成员样本推入高置信度区域，即可伪造其成员身份，从而破坏隐私审计的完整性。

框架据此沿三条互补的技术路线展开，形成“攻击—检测—防御升级”的闭环。

### 模块一：成员伪造攻击（Member Fabrication Attack, MFA）

MFA 是攻击端的核心模块。其目标与传统的对抗攻击截然相反：传统对抗攻击（如 FGSM、PGD、CW）试图最小化真实类别的置信度以制造误分类，而 MFA 则通过最大化真实类别置信度 $p_y(x)$ 将非成员“推入”模型的高置信度成员区域。形式化地，给定非成员 $(x, y)$ 和 $\ell_\infty$ 扰动球 $\mathcal{B}_\epsilon[x]$，MFA 求解：

$$\bar{x} = \arg\max_{x' \in \mathcal{B}_\epsilon[x]} p_y(x')$$

这一优化通过动量累积与余弦退火步长调度的投影梯度上升实现。动量项 $m_{k+1} = \beta m_k + (1-\beta) \nabla_{x_k} \ell(f(x_k), y)$ 稳定了置信度上升轨迹，余弦退火步长 $\alpha_k = \alpha_0 (1 + \cos(\pi k / N))/2$ 使优化平稳收敛至 $\ell_\infty$ 球内的局部最优。消融实验（Table 1）证实，该动量余弦退火策略（Strategy IV）在错误面积（Error Area）和等错误率（EER）上均显著优于固定步长、半衰启发式和纯余弦退火方案。

### 模块二：成员伪造检测（Member Fabrication Detection, MFD）

MFA 的成功引出一个关键问题：伪造成员与真实成员在语义特征空间中高度重叠（Figure 4 的 t-SNE 可视化表明两者在倒数第二层和倒数第三层特征上几乎不可区分），使得基于语义特征的检测方法（如 Mahalanobis 距离、局部内在维度 LID）失效。本文的核心发现是，MFA 在优化过程中会留下一个不可消除的几何指纹——**输入梯度范数的塌缩**。理论分析（Theorem 1）证明，在单步符号梯度下降下，梯度范数严格减小：

$$\|\nabla_{x'} \ell(f(x'), y)\| < \|\nabla_x \ell(f(x), y)\|$$

实验观测（Figure 5, Figure 6）进一步验证，伪造成员在达到高置信度时，其输入梯度范数显著低于真实成员，形成“低梯度、高置信度”的几何特征。MFD 据此构建一个简洁的阈值检测器：

$$\mathbf{T}(x,y) = \mathbf{1}\left[ \|\nabla_x \ell(f(x), y)\| \le \tau' \right]$$

该检测器在多个数据集上实现 AUC > 0.9，且区分能力远超 Mahalanobis 距离和 LID（Figure 7(d-f)）。

### 模块三：对抗鲁棒成员推理攻击（Adversarially Robust MIA, AR-MIA）

检测模块为防御方提供了工具，但隐私审计的最终目标是在攻击存在的情况下仍能可靠地推断成员身份。AR-MIA 的设计思路是将梯度几何信号作为权重，与现有 MIA 的统计量 $S(x,y)$ 相乘，从而在不改变原有 MIA 设计的前提下赋予其抗操纵能力。为避免非成员天然的大梯度范数过度压制统计量，权重通过 tanh 函数进行有界压缩：

$$w(x,y) = \tanh\left(\lambda \cdot \|\nabla_x \ell(f(x), y)\|\right)$$

最终的鲁棒推理决策为：

$$I(x,y) = \mathbf{1}\left[ w(x,y) \cdot S(x,y) > \tau \right]$$

### 输入输出流与模块关系

框架的整体数据流如下：非成员样本 $x$ 首先经过 MFA 模块，在 $\ell_\infty$ 扰动约束下生成伪造成员 $\bar{x}$；随后，$\bar{x}$ 与真实成员样本一同进入 MFD 检测器，后者基于梯度范数阈值 $\tau'$ 输出伪造/真实的二值判定；在隐私审计场景中，AR-MIA 模块接收待测样本，计算梯度范数权重 $w(x,y)$ 并与原有 MIA 统计量 $S(x,y)$ 融合，最终输出成员身份推断。三个模块共享同一个白盒梯度访问假设，构成“攻击暴露漏洞—几何特征检测—加权鲁棒推理”的完整闭环。实验表明，AR-MIA 在 CIFAR-10/100、CINIC-10 和 SVHN 等多个数据集上将基线 MIA 的 AUC 从 0.4–0.7 提升至 0.78–0.85，同时将 EER 降低 10–28 个百分点（Tables 7–9）。

**需要手动验证的点**：框架目前仅在标准训练的图像分类模型上验证，其在差分隐私训练模型、Vision Transformer 架构及黑盒梯度估计场景下的有效性尚待进一步实验确认。

![[assets/figures/papers/paper_list_l2246_https_arxiv_org_abs_2604_02780/figures/001_Figure_1.jpg]]
*Figure 1: Overview of the Background and Our Proposed Research Problems*

本节围绕“对抗性成员操作”这一核心问题，依次构建三个关键模块：**成员伪造攻击（MFA）**、**成员伪造检测（MFD）** 与**对抗鲁棒成员推理攻击（AR-MIA）**。三者构成一个完整的攻防-推理闭环：MFA 揭示了现有成员推理攻击的结构性脆弱性，MFD 利用梯度几何特征检测伪造行为，AR-MIA 则将检测信号融入推理统计量以恢复攻击鲁棒性。

### 3.1 成员伪造攻击（MFA）

**攻击目标的形式化差异**。传统对抗攻击旨在诱导模型误分类，其目标是最小化真实类别的 logit 以跨越决策边界：

$$x^* = \arg\max_{x'} -(z_y(x') - \max_{i\neq y} z_i(x')) \quad \text{(Equation 3)}$$

而 MFA 的目标截然不同：攻击者并不需要改变模型的预测标签，而是将非成员样本推入高置信度的“成员区域”，从而欺骗基于置信度信号的成员推理攻击。其优化目标为在 $\ell_\infty$ 球内最大化真实类别的 softmax 概率：

$$\forall x' \in \mathcal{B}_\epsilon[x], \quad \bar{x} = \arg\max_{x'} (p_y(x')) \quad \text{(Equation 4)}$$

这一目标差异是理解整个攻击框架的起点：MFA 追求的是“置信度膨胀”而非“标签翻转”。

**动量余弦退火优化**。为使置信度平稳上升至目标区域，MFA 采用动量累积配合余弦退火步长的投影梯度上升策略。动量更新步骤为：

$$m_{k+1} = \beta m_k + (1-\beta) \nabla_{x_k} \ell(f(x_k), y) \quad \text{(Equation 5)}$$

随后沿动量符号方向进行投影梯度上升，并施加余弦退火步长调度 $\alpha_k = \alpha_0 \frac{1 + \cos(\pi k / N)}{2}$：

$$x_{k+1} = \Pi_{\mathcal{B}_\epsilon[x]} (x_k - \alpha_k \mathrm{sign}(m_{k+1})) \quad \text{(Equation 6)}$$

其中 $\Pi_{\mathcal{B}_\epsilon[x]}$ 为投影算子，确保扰动始终约束在 $\ell_\infty$ 球内。消融实验（Table 1）表明，该动量余弦退火策略（Strategy IV）在 Error Area 和 EER 上均显著优于固定步长、半衰启发式及纯余弦退火方案，验证了平稳收敛对伪造质量的关键作用。

### 3.2 梯度范数塌缩：从经验观察到理论分析

**核心瓶颈的发现**。伪造成员与真实成员在语义特征空间中高度重叠（Figure 4, t-SNE 可视化），使得基于语义特征的检测方法（如 Mahalanobis 距离、局部内在维度 LID）难以有效区分二者（Figure 6）。然而，在优化过程中观察到输入梯度范数持续衰减（Figure 5），伪造成员最终落入“低梯度、高置信度”的平坦区域，而真实成员则处于梯度强度适中的区域。

**理论保证**。在单步符号梯度下降的简化设定下：

$$x' = x - \alpha \cdot \mathrm{sign}(\nabla_x \ell(f(x), y)) \quad \text{(Equation 7)}$$

可以证明，在充分小的步长条件下，梯度范数严格减小：

$$\| \nabla_{x'} \ell(f(x'), y) \| < \| \nabla_x \ell(f(x), y) \| \quad \text{(Equation 8, Theorem 1)}$$

这一“梯度范数塌缩”现象构成了区分真实成员与伪造成员的可靠几何信号。置信度匹配实验（Table 2）进一步验证：在相同目标类别置信度区间内，伪造样本的梯度范数始终显著小于真实成员，排除了“梯度范数下降仅因置信度上升”的替代解释。

**MFD 检测器**。基于上述发现，MFD 将梯度范数与阈值 $\tau'$ 比较，构建二分类检测器：

$$\mathbf{T}(x,y) = \mathbf{1}[ \| \nabla_x \ell(f(x), y) \| \le \tau' ] \quad \text{(Equation 9)}$$

该检测器在多个数据集上实现 AUC > 0.9（Figure 7(d-f)），且显著优于基于 Mahalanobis 距离和 LID 的特征检测方法。

### 3.3 对抗鲁棒成员推理攻击（AR-MIA）

**设计思路**。现有 MIA 的决策函数为 $I(x,y) = \mathbf{1}[S(x,y) > \tau]$（Equation 2），其中 $S(x,y)$ 可以是损失值、似然比或置信度校准统计量。在 MFA 攻击下，非成员的 $S(x,y)$ 被人为推高，导致推理失效。AR-MIA 的核心思路是将梯度范数几何信号作为权重与原始统计量相乘，压低伪造成员的加权得分。

**权重函数设计**。为避免非成员中偶尔出现的极大梯度范数主导统计量，采用 tanh 函数将权重约束在 $(0,1)$ 区间：

$$w(x,y) = \mathrm{tanh}\left( \lambda \cdot \| \nabla_x \ell(f(x), y) \| \right) \quad \text{(Equation 10)}$$

其中 $\lambda$ 为控制权重陡峭程度的超参数。伪造成员因梯度范数极小，权重接近 0，加权后的统计量被大幅压低；真实成员保持适中梯度，权重接近 1，统计量基本不变。

**最终决策函数**：

$$I(x,y) = \mathbf{1}\left[ w(x,y) \cdot S(x,y) > \tau \right] \quad \text{(Equation 11)}$$

该设计具有即插即用的特点：不改变现有 MIA 的统计量 $S(x,y)$ 和阈值 $\tau$ 的校准方式，仅通过梯度范数加权增强抗操纵能力。实验表明，AR-MIA 可将 Attack R、LiRA、RMIA 等基线攻击在 MFA 下的 AUC 从 0.4–0.7 提升至 0.78–0.85，同时 EER 下降 20–30 个百分点（Tables 7–9）。

**超参数校准**。$\lambda$ 需要根据数据集和 MIA 类型离线调节：适当增大 $\lambda$ 可提升对伪造成员的抑制能力，但过大的 $\lambda$ 会过度压缩真实非成员的权重，削弱其与真实成员的区分度（Figure 7(g-i)）。目前缺乏统一的自动化选择机制，这是该方法的已知局限之一。

![[assets/figures/papers/paper_list_l2246_https_arxiv_org_abs_2604_02780/figures/004_Figure_4.jpg]]
*Figure 4: Visualization of the Distribution of Fabricated and True Members in Different Semantic Feature Spaces Using t-SNE [38]. The two subfigures represent the semantic features at the penultimate and antepenultimate layers, with perturbation constrained to*

## 实验与关键发现

### 核心发现：梯度几何信号揭示伪造与真实成员的分离

本工作的实验围绕一个核心洞察展开：**伪造成员在优化过程中梯度范数显著塌缩，形成低梯度、高置信度的几何特征，而真实成员则保持中等梯度强度**。Figure 6 对比了三种检测策略下伪造与真实成员的分布：Mahalanobis距离和局部内在维度（LID）几乎无法区分两类样本，而输入梯度范数呈现出明显的分离——伪造成员的梯度范数系统地低于真实成员。Table 2 进一步在相同目标类别置信度区间内进行匹配对比，证实了这一分离并非置信度差异的副产品，而是伪造过程固有的几何指纹。

![[assets/figures/papers/paper_list_l2246_https_arxiv_org_abs_2604_02780/figures/009_Table_2.jpg]]
*Table 2: Confidence-matched comparison of input-gradient norms. Fabricated samples consistently exhibit smaller gradient norms than true members within the same target-class confidence range*

这一几何信号构成了整个统一框架的基石：MFA利用它来实施攻击，MFD基于它构建检测器，AR-MIA则将其作为权重因子提升现有MIA的鲁棒性。

### 成员伪造攻击（MFA）性能评估

#### 步长策略消融

Table 1 展示了四种步长策略在 CIFAR-10、CIFAR-100、SVHN 和 CINIC-10 上的消融结果。策略 IV（动量余弦退火）在所有数据集上均取得最优 Error Area 和 EER：

![[assets/figures/papers/paper_list_l2246_https_arxiv_org_abs_2604_02780/figures/008_Table_1.jpg]]
*Table 1: Ablation study of MFA with four step size strategies*

- **CIFAR-10**: Error Area 0.9451, EER 87.60%
- **CIFAR-100**: Error Area 0.6136, EER 59.80%
- **SVHN**: Error Area 0.9618, EER 89.70%
- **CINIC-10**: Error Area 0.9324, EER 86.85%

动量累积（式5）配合余弦退火步长（$\alpha_k = \alpha_0 \frac{1 + \cos(\pi k / N)}{2}$）使优化过程更平稳地收敛到高置信度区域，而固定步长（策略 I）、半衰启发式（策略 II）和纯余弦退火（策略 III）在稳定性和最终攻击效果上均不及策略 IV。

#### 与基线方法的对比

Table 3 和 Table 6 系统对比了 MFA 与五种倒置攻击基线（I-FGSM、I-BIM、I-PGD、I-CW、I-APGD）在多个数据集上的 Error Area 和 EER。MFA 在所有数据集和 MIA 组合上均显著优于基线。Figure 7(a-c) 的 TNR-TPR 曲线显示，MFA 的曲线更接近左下角（理想伪造区域），表明其能更有效地将非成员推入高置信度成员区域。

![[assets/figures/papers/paper_list_l2246_https_arxiv_org_abs_2604_02780/figures/029_Table_3.jpg]]
*Table 3: The Comparison of Error Area between Our Member Fabrication Attack with Baselines across Diverse Datasets*

Table 4 和 Table 5 分别报告了 MFA 在 Loss Attack、Attack R、LiRA、RMIA 四种 MIA 上的 Error Area 和 EER。MFA 对各类 MIA 均表现出强伪造能力，但对不同攻击的敏感度存在差异：基于似然比的 LiRA 和 RMIA 相对更难被完全欺骗，这与它们利用影子模型分布信息的设计有关。

### 成员伪造检测（MFD）性能

Figure 7(d-f) 展示了 MFD 在不同扰动水平 $\epsilon$ 和数据集上的 ROC 曲线。基于梯度范数阈值 $\mathbf{T}(x,y) = \mathbf{1}[ \| \nabla_x \ell(f(x), y) \| \le \tau' ]$ 的检测器在多数设置下 AUC > 0.9，显著优于 Figure 6 中展示的 Mahalanobis 距离和 LID 方法。

检测性能对扰动大小敏感：当 $\epsilon$ 较小时，伪造样本的梯度范数塌缩不够充分，检测难度增加；当 $\epsilon$ 增大时，塌缩效应更显著，MFD 的区分能力随之提升。这一趋势在 CIFAR-10、CIFAR-100、CINIC-10、SVHN 和 ImageNet-100 上表现一致（见 Figure 18-22 的完整 ROC 对比）。

### 对抗鲁棒成员推理攻击（AR-MIA）性能

#### 主结果

Table 7-9 分别报告了 AR-Attack R、AR-LiRA 和 AR-RMIA 在 $\|\delta\|_\infty \le 4.0/255$ 下的性能。核心结果如下：

![[assets/figures/papers/paper_list_l2246_https_arxiv_org_abs_2604_02780/figures/033_Table_7.jpg]]
*Table 7: Comparison of Attack R and Our Adversarially Robust Attack R*

- **CIFAR-10 + Attack R**: AUC 从 0.4019 提升至 0.7871（$\lambda=20$），EER 从 58.20% 降至 29.80%
- **CIFAR-100 + Attack R**: AUC 从 0.6881 提升至 0.7881（$\lambda=35$）
- **CINIC-10 + RMIA**: AUC 从 0.7219 提升至 0.8504（$\lambda=20$）
- **SVHN + LiRA**: 同样观察到显著的 AUC 提升和 EER 下降

Figure 7(g-i) 的 ROC 曲线直观展示了加权策略的效果：AR-MIA 的曲线系统性地高于基线 MIA，尤其在低 FPR 区域提升更为明显。

#### 权重参数 $\lambda$ 的调节

消融实验表明，$\lambda$ 需要根据数据集和 MIA 类型进行校准。适当增大 $\lambda$ 可以增强梯度范数权重 $w(x,y) = \mathrm{tanh}(\lambda \cdot \| \nabla_x \ell(f(x), y) \|)$ 的区分能力，但过大的 $\lambda$ 会使 tanh 函数过早饱和，削弱对非成员异常梯度的抑制作用。Tables 7-9 中报告了不同 $\lambda$ 值下的性能变化，最优值通常在 20-35 之间。

### 自适应攻击下的鲁棒性

Appendix F 探索了自适应 MFA 场景：攻击者在优化目标中显式加入梯度范数惩罚项，试图同时最大化置信度和梯度范数以绕过 MFD。结果表明，自适应 MFA 确实降低了 MFD 的 AUC，但 AR-MIA 仍能保持显著优于基线 MIA 的性能。这一发现表明梯度范数信号具有一定的内在鲁棒性——即使攻击者试图掩盖这一几何指纹，加权策略仍能提取残余的区分信息。

### 失败模式与局限性

1. **黑盒场景下的退化**：MFD 和 AR-MIA 需要白盒梯度访问。在严格黑盒条件下，需通过有限差分估计梯度，这会引入精度损失和显著的计算开销。该场景下的性能退化程度尚未在实验中量化。

2. **自适应攻击的持续威胁**：虽然 AR-MIA 对当前自适应 MFA 保持一定鲁棒性，但完全自适应的攻击（同时优化置信度、梯度范数及可能的 Hessian 特征）是否能够彻底绕过检测，仍是一个开放问题。

3. **跨架构泛化未验证**：实验主要基于 ResNet 类卷积架构，对 Vision Transformer 等新型架构的泛化性尚无实验支撑。

4. **更强防御下的有效性未知**：所有实验均在标准训练模型上进行，未涉及差分隐私训练等更强隐私保护机制。在 DP-SGD 等场景下，梯度信号本身已被噪声化，MFD 和 AR-MIA 的性能可能受到显著影响。

5. **阈值依赖离线校准**：$\tau'$（MFD）和 $\lambda$（AR-MIA）需要根据具体数据集和 MIA 类型进行离线调优，缺乏统一的自动化选择机制，在实际部署中可能面临分布偏移的挑战。

## 定位与知识库关联

### 1. 问题定位：成员推理的操纵脆弱性

现有成员推理攻击（MIA）的核心假设是：成员样本比非成员样本具有更高的模型置信度或更低的损失值。基于这一假设，主流MIA方法——包括基于损失的 **Loss Attack**、基于置信度校准的 **Attack R**、利用影子模型似然比的 **LiRA**（Carlini et al., S&P 2022） 以及基于密度比校准的 **RMIA**——均依赖语义置信度信号（损失值、似然比、置信度分数）进行成员身份判别。

然而，这一依赖关系暴露了一个根本性漏洞：**攻击者可通过不可察觉的输入空间扰动，将非成员推入高置信度区域，从而伪造其成员身份**。论文将这一威胁形式化为“成员伪造”（Membership Fabrication），并指出传统对抗攻击的目标（最小化正确类别的置信度以引发误分类）与成员伪造的目标（最大化正确类别的置信度以伪装成成员）存在本质差异（Figure 3）。这一区分将成员推理的鲁棒性问题从“攻击者能否推断成员身份”提升为“攻击者能否操纵推断结果”，构成了本文的核心问题域。

### 2. 方法谱系：从倒置对抗攻击到梯度几何驱动

#### 2.1 基线伪造方法：倒置对抗攻击

在本文提出成员伪造攻击（MFA）之前，最自然的伪造基线是将传统对抗攻击的目标函数反转——即沿梯度上升方向而非下降方向优化。具体而言，基线方法包括：

- **I-FGSM**：反转快速梯度符号法（FGSM）方向
- **I-BIM**：反转基础迭代法（BIM）方向
- **I-PGD**：反转投影梯度下降（PGD）方向
- **I-CW**：反转Carlini-Wagner攻击方向
- **I-APGD**：反转自适应PGD方向

这些倒置方法共享一个核心特征：**直接沿符号梯度方向进行固定步长的迭代上升**，缺乏对优化动力学的精细控制。实验证据表明，这类方法在错误面积（Error Area）和等错误率（EER）两个关键指标上均显著劣于MFA（Table 3, Table 6），其根本原因在于固定步长策略难以在高维非凸的置信度景观中稳定收敛到高置信度区域。

#### 2.2 核心创新：动量余弦退火MFA

MFA的关键改进在于引入两个互补的优化机制：

1. **动量累积**（Equation 5）：通过指数滑动平均 $m_{k+1} = \beta m_k + (1-\beta) \nabla_{x_k} \ell(f(x_k), y)$ 平滑梯度方向，避免在尖锐的损失景观中震荡，使优化轨迹更稳定地指向高置信度盆地。

2. **余弦退火步长调度**（Equation 5 context）：步长 $\alpha_k = \alpha_0 \frac{1 + \cos(\pi k / N)}{2}$ 在迭代初期保持较大步长以快速探索，在后期逐步衰减以实现精细收敛，避免在最优解附近过冲。

消融实验（Table 1）系统对比了四种步长策略：固定步长（Strategy I）、半衰启发式（Strategy II）、纯余弦退火（Strategy III）以及动量+余弦退火（Strategy IV）。结果表明，Strategy IV在CIFAR-10上实现了0.9451的错误面积和87.60%的EER，显著优于其他三种策略。这验证了一个关键洞察：**成员伪造的优化难度不在于“找到高置信度方向”，而在于在ℓ∞约束下稳定地收敛到置信度景观的局部最大值**。

#### 2.3 从检测到鲁棒推理：梯度范数塌缩的几何信号

本文最具原创性的贡献在于识别出**梯度范数塌缩**作为伪造成员的几何指纹。理论分析（Theorem 1）证明：在小步长条件下，沿符号梯度下降方向移动后，输入梯度范数严格减小，即 $\| \nabla_{x'} \ell(f(x'), y) \| < \| \nabla_x \ell(f(x), y) \|$（Equation 8）。这一性质源于MFA优化过程将样本推向置信度景观的平坦高置信度盆地，导致梯度信号逐渐消失。

实验证据从三个层面支撑了这一发现：

- **语义特征空间的重叠**（Figure 4）：t-SNE可视化显示伪造成员与真实成员在倒数第二层和倒数第三层的语义特征空间中高度重叠，表明基于语义特征的检测方法（如Mahalanobis距离、局部内在维度LID）难以区分两者。

- **梯度范数的分布分离**（Figure 6）：在相同置信度区间内，伪造成员的梯度范数分布显著低于真实成员（Table 2），形成可操作的检测信号。基于梯度范数的检测器MFD（Equation 9）实现了AUC > 0.9，显著优于Mahalanobis距离和LID方法。

- **跨数据集和扰动水平的泛化性**（Figure 7(d-f), Figures 18-22）：MFD在CIFAR-10、CIFAR-100、CINIC-10、SVHN和ImageNet-100上均保持有效检测性能。

基于这一几何信号，论文进一步提出了对抗鲁棒成员推理攻击（AR-MIA），其核心设计是将梯度范数权重 $w(x,y) = \mathrm{tanh}(\lambda \cdot \| \nabla_x \ell(f(x), y) \|)$ 与原始MIA统计量相乘（Equation 10-11）。tanh函数的关键作用在于**限制权重范围**，防止某些非成员因异常大的梯度范数而获得过高权重，从而保持原始统计量的判别力。实验表明，AR-MIA将基线MIA的AUC从0.4-0.7提升至0.78-0.85，同时将EER降低20-30个百分点（Tables 7-9, Figure 7(g-i)）。

### 3. 适用边界与局限

#### 3.1 白盒假设与黑盒迁移

MFA、MFD和AR-MIA均需要白盒梯度访问，这是当前方法最核心的适用边界。在严格黑盒场景下，梯度需通过有限差分估计获得，这会引入精度损失和计算开销。论文未提供黑盒条件下的系统性实验验证，这一缺环需要后续工作填补。

#### 3.2 自适应攻击的威胁

附录F初步探讨了自适应MFA（在优化目标中加入梯度范数惩罚项）对MFD的绕过能力。结果表明，自适应MFA可降低MFD的AUC，但AR-MIA仍保持显著优于基线MIA的性能。然而，这一分析尚不充分：**是否存在能完全绕过梯度范数检测的伪造策略**（如同时优化置信度和梯度范数，或利用Hessian信息构造高置信度、高梯度范数的伪造成员）仍是开放问题。

#### 3.3 模型架构与训练范式的泛化性

实验主要限于ResNet架构和标准训练模型。以下场景的泛化性尚未验证：

- **Vision Transformer等新架构**：自注意力机制可能产生不同的梯度几何特征，梯度范数塌缩是否仍是可靠的伪造指纹需要重新审视。
- **差分隐私训练模型**：DP-SGD引入的梯度裁剪和噪声可能改变成员与非成员的梯度范数分布，进而影响MFD和AR-MIA的有效性。
- **大规模预训练模型**：CLIP、DINOv2等基础模型的成员推理攻击本身仍处于探索阶段，伪造与检测的相互作用更为复杂。

#### 3.4 超参数校准的自动化

AR-MIA中的权重参数λ需要根据数据集和MIA类型进行离线校准（Tables 7-9显示λ在不同设置下取值从10到35不等）。当前缺乏统一的自动化选择机制，在实际部署中可能成为瓶颈。

### 4. 开放问题与未来方向

1. **梯度几何指纹的完备性**：梯度范数塌缩是否是不可绕过的伪造副作用？是否存在其他几何或统计特征（如Hessian范数、局部内在维度、梯度方向一致性）可作为互补或替代的伪造指纹？

2. **复合威胁模型**：成员伪造攻击与模型提取、数据投毒、后门攻击等其他威胁结合时会产生怎样的复合隐私风险？例如，攻击者可能先通过模型提取获得白盒梯度访问权，再实施成员伪造。

3. **真实部署环境中的鲁棒性**：数据分布偏移、输入噪声、模型更新等因素如何影响MFD的检测阈值$\tau'$和AR-MIA的权重参数$\lambda$？是否需要在线自适应校准机制？

4. **差分隐私的交互效应**：差分隐私训练本身会降低MIA的准确率，但它是否同时增强了模型对成员伪造的抵抗力？梯度范数塌缩特征在DP模型上是否仍然存在？

5. **审计标准的重新定义**：如果成员伪造攻击是可行的，那么现有的MIA审计标准（如AUC、TPR@lowFPR）是否仍然有效？是否需要引入“操纵鲁棒性”作为MIA评估的新维度？

### 5. 知识库定位

本文处于**对抗机器学习**与**隐私审计**的交叉地带，其核心贡献在于将成员推理的安全性从“攻击有效性”拓展至“攻击完整性”。在方法谱系上：

- **上游**：继承了对抗攻击的优化框架（PGD、CW、APGD）和成员推理的统计检验框架（LiRA、RMIA），但通过目标函数的反转和梯度几何信号的引入，开辟了新的问题空间。
- **平行**：与基于差分隐私的防御方法（降低MIA准确率但无法检测伪造）和基于语义特征的异常检测方法（Mahalanobis、LID，在伪造检测上效果有限）形成互补。
- **下游**：为成员推理的鲁棒性评估提供了基准工具（MFA作为攻击基准，MFD作为检测基准），并为更广义的“对抗性隐私操纵”研究（如属性推理伪造、数据来源伪造）提供了方法论模板。

## 原文 PDF

![[paperPDFs/CVPR_2026/A_Unified_Perspective_on_Adversarial_Membership_Manipulation_in_Vision_Models.pdf]]
