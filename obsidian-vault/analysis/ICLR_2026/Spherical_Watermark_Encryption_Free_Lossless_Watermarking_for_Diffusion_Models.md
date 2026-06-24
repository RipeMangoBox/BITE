---
title: "Spherical Watermark: Encryption-Free, Lossless Watermarking for Diffusion Models"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Spherical_Watermark_Encryption_Free_Lossless_Watermarking_for_Diffusion_Models.pdf
openreview_forum_id: 2eAGrunxVz
aliases:
- SW
- SWEFLWDM
tags:
- ICLR_2026
- topic/safety_alignment_fairness_privacy
- topic/safety_alignment_fairness_privacy/trustworthy_machine_learning
core_operator: "一种加密无关的球形映射策略：先将水印比特与随机填充混合，通过单位球面投影和固定正交旋转构造球面3-设计，再乘以卡方分布半径，从而在不使用任何加密原语的情况下将任意二进制水印转化为与标准高斯噪声统计不可分的隐变量。"
primary_logic: "若将水印嵌入过程视为一个从离散二进制序列到连续高斯噪声的可逆映射，则只需保证映射后的分布精确匹配扩散先验的低阶矩，即可实现无损嵌入；同时，正交旋转将比特能量均匀分散并带来最优的抗加性噪声鲁棒性，而无需每图像动态密钥。"
claims:
- "在latent和image两级训练二分类器，PRC Watermark与本方法的检测准确率均接近随机猜测（50%），而Tree-Ring和Gaussian Shading在固定密钥下分别达到100%和97%的可检测准确率。"
- "本方法与PRC Watermark是仅有的两个在FID上与原图分布无明显差异的方案（FID ~46.8 vs. 46.8），其余方法均引起显著分布偏移。"
- "在对抗攻击条件下，本方法的追踪准确率（ACC）比有损方法提升超过10%，且TPR@1%FPR保持在99%以上，远超PRC Watermark（~87%）。"
- "本方法的提取耗时约0.01秒，比PRC Watermark快约四个数量级，消除了加密编码-解码的计算瓶颈。"
---

# Spherical Watermark: Encryption-Free, Lossless Watermarking for Diffusion Models

> [!tip] 核心洞察
> 若将水印嵌入过程视为一个从离散二进制序列到连续高斯噪声的可逆映射，则只需保证映射后的分布精确匹配扩散先验的低阶矩，即可实现无损嵌入；同时，正交旋转将比特能量均匀分散并带来最优的抗加性噪声鲁棒性，而无需每图像动态密钥。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 球形水印：面向扩散模型的免加密无损水印技术 |
| 英文题名 | Spherical Watermark: Encryption-Free, Lossless Watermarking for Diffusion Models |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=2eAGrunxVz) |
| Topic | #topic/safety_alignment_fairness_privacy #topic/safety_alignment_fairness_privacy/trustworthy_machine_learning |
| Method | Spherical Watermark |
| Dataset | COCO + SD v1.5, SDP + SD v2.1, SDP + SD v1.5, COCO + SD v2.1 |

> [!tip] 效果简介
> - COCO + SD v1.5 上，TPR@1%FPR (Post-Processing) 为 97.57%，对比 PRC Watermark: 87.51%，变化 +10.06%。
> - SDP + SD v2.1 上，TPR@1%FPR (Post-Processing) 为 97.69%，对比 PRC Watermark: 87.19%，变化 +10.50%。
> - SDP + SD v1.5 上，TPR@1%FPR (Adversarial) 为 99.81%，对比 PRC Watermark: 94.58%，变化 +5.23%。

## 概述

扩散模型生成内容的溯源与版权保护面临一个根本性矛盾：有损水印方法以牺牲图像保真度为代价换取可追溯性，而现有的无损方案——如 **Gaussian Shading**（Yang et al., 2024）和 **PRC Watermark**（Gunn et al., 2025）——虽能保持生成质量，却分别依赖流密码或复杂纠错码，导致每图像需唯一密钥或高昂的编解码开销，严重阻碍了在大规模API场景下的实际部署。

Spherical Watermark 针对上述瓶颈提出了一种**加密无关的球形映射策略**：将水印比特与随机填充混合后，通过单位球面投影和固定正交旋转构造球面3-设计，再乘以卡方分布半径，从而在不使用任何加密原语的情况下，将任意二进制水印转化为与标准高斯噪声在低阶矩上统计不可分的隐变量。其核心洞察在于，若将水印嵌入视为从离散二进制序列到连续高斯噪声的可逆映射，则只需保证映射后的分布精确匹配扩散先验的低阶矩，即可实现无损嵌入；同时，正交旋转将比特能量均匀分散，带来最优的抗加性噪声鲁棒性，且无需每图像动态密钥。

在方法谱系中，Spherical Watermark 属于**潜在空间无损水印**，与 PRC Watermark 和 Gaussian Shading 处于同一类别，但其关键区别在于完全消除了对加密或纠错码的依赖。与频域有损方法（如 **DwtDct**、**DwtDctSvd**）和神经网络水印（如 **RivaGAN**）相比，本方法不修改生成图像本身，因而在FID指标上与原图分布无显著差异（~46.8 vs. 46.8）。与仅支持检测的 **Tree-Ring**（Wen et al., NeurIPS 2023）相比，本方法支持任意二进制消息的精确嵌入与提取。

主要实验结果如下：

- **无损性**：在COCO和SDP数据集上，Spherical Watermark 与 PRC Watermark 是仅有的两个FID与原图无显著差异的方案；在潜在空间和图像空间训练的二分类器均无法区分水印样本与无痕样本（准确率接近50%），而 Tree-Ring 和 Gaussian Shading 在固定密钥下分别达到100%和97%的可检测准确率。
- **鲁棒性**：在对抗攻击条件下，追踪准确率（ACC）比有损方法提升超过10%，TPR@1%FPR保持在99%以上，远超 PRC Watermark 的约87%。
- **效率**：提取耗时约0.01秒，比 PRC Watermark 快约四个数量级，消除了加密编码-解码的计算瓶颈。
- **容量扩展性**：在高达2000比特的容量下仍保持高精度，而 PRC Watermark 在超过2000比特后迅速失效。

消融实验进一步揭示：球面映射模块（正交旋转与半径缩放）对鲁棒性至关重要，移除后所有攻击下的追踪准确率剧烈下降；增加水印重复次数可显著提升鲁棒性，而增加稀疏度则带来轻微下降，为无损性-鲁棒性权衡提供了明确控制。此外，本方案对ODE求解器类型和采样步数不敏感，并对反演误差表现出强容忍性（噪声增至1.5倍标准差时提取成功率仍超95%）。

**局限性**方面，高阶矩可能偏离真实高斯分布，在极端统计测试下存在被检测的风险；强反转破坏攻击（如大幅裁剪或涂鸦）可能导致DDIM反演失败，使水印提取完全失效；当前方案依赖扩散模型的反演过程，对非高斯先验或不支持精确反演的生成模型适用性受限。

## 背景与动机

扩散模型（Diffusion Models）的快速发展使得AI生成内容（AIGC）的版权追溯与内容溯源成为紧迫需求。在这一背景下，水印技术被广泛视为追踪生成图像来源的核心手段。然而，现有水印方法在图像质量与密钥管理之间存在着难以调和的矛盾，严重阻碍了其在大规模API场景下的实际部署。

**有损方法的保真度困境。** 传统水印方案，如基于频域的**DwtDct**（Al-Haj, 2007）和**DwtDctSvd**（Navas et al., 2008），以及基于神经网络的**RivaGAN**（Zhang et al., 2019），在嵌入水印时不可避免地修改图像内容，导致生成质量下降。即便是在潜空间中嵌入图案的**Tree-Ring**（Wen et al., NeurIPS 2023），也会引起显著的分布偏移——在COCO数据集上使用SD v2.1时，其FID从原始的46.81劣化至约50.82（Table 1），表明有损嵌入从根本上改变了生成图像的统计特性。

**无损方法的密钥管理瓶颈。** 为规避保真度损失，近期工作转向无损嵌入范式。**Gaussian Shading**（Yang et al., 2024）通过流密码将水印比特映射为高斯潜变量，但要求每张图像使用唯一的密钥/Nonce，否则在固定密钥下会丧失无损性——此时其二分类器检测准确率高达97%（Figure 2），证明其分布与真实高斯噪声存在可检测的偏差。**PRC Watermark**（Gunn et al., 2025）则依赖伪随机纠错码替代流密码，虽无需每图像动态密钥，但其编解码过程计算开销极大，单样本提取耗时约100秒（Figure 4），比本方法慢约四个数量级。这两种方案揭示了一个深层困境：要么牺牲无损性以简化密钥管理，要么承受高昂的计算延迟以维持无损性。

**核心瓶颈：加密依赖与分布匹配的冲突。** 上述困境的根源在于，现有无损方法必须借助加密原语（流密码或复杂纠错码）来保证水印潜变量与标准高斯噪声的统计不可区分性。这带来了密钥存储开销、编解码延迟和实现复杂度三重负担，使得扩散模型水印在实际API服务中难以高效部署。问题的本质可归结为：**能否在不使用任何加密机制的前提下，构造一个从离散二进制水印到连续高斯噪声的可逆映射，使得映射后的分布精确匹配扩散先验的低阶矩，同时赋予水印对后处理和对抗攻击的天然鲁棒性？**

本文提出的**Spherical Watermark**（球形水印）正是对这一问题的正面回答。其核心思想是：将水印嵌入视为一个纯粹的几何变换问题——通过球面投影、固定正交旋转和卡方半径缩放，将任意二进制水印转化为与标准高斯噪声统计不可分的隐变量。这一策略完全摒弃了加密原语，仅需一个固定的二进制混合矩阵和正交旋转矩阵，从根本上消解了密钥管理与无损性之间的张力，同时利用球面3-设计的最优距离特性，为水印提供了可证明的抗加性噪声鲁棒性。

## 核心创新

Spherical Watermark 的核心创新在于提出了一种**加密无关的无损水印映射策略**，从根本上解耦了水印保真度与密钥管理之间的矛盾。其关键设计可归结为两个相互配合的 changed slots：

### 1. 初始噪声生成策略：从高斯采样到球面构造映射

现有方法在生成水印化初始噪声时，或直接采样标准高斯分布后叠加扰动（有损），或依赖流密码/伪随机编码逐图像生成掩码（无损但密钥开销大）。Spherical Watermark 取而代之的是一条完全确定性的构造管线：

1. **二进制嵌入（Binary Embedding）**：将待嵌入的水印比特 $\mathbf{m}$ 重复 $N$ 次并与随机填充 $\mathbf{r}$ 拼接，通过 $\mathrm{GF}(2)$ 上的可逆矩阵 $\mathbf{T}$ 进行混合，得到 $3$-wise 独立的比特流 $\mathbf{z}^{(1)} = \mathbf{T}\mathbf{x}$（见 Eq. (9)）。这一步的核心作用是将水印能量均匀分散，消除比特间的统计相关性，为后续球面映射提供“平坦”的离散输入。
2. **球面映射（Spherical Mapping）**：将二进制向量 $\mathbf{z}^{(1)}$ 映射到单位球面 $\mathbf{z}^{(2)} = \mathbf{v}/\|\mathbf{v}\|_2$，施加**固定的**正交旋转矩阵 $\mathbf{C}$ 得到 $\mathbf{z}^{(3)} = \mathbf{C}\mathbf{z}^{(2)}$，最后乘以卡方分布半径 $r$（$r^2 \sim \chi^2(l_x)$）得到最终水印潜变量 $\mathbf{z}_w = r\mathbf{z}^{(3)}$（见 Eq. (10)）。

该管线的理论根基在于**多元高斯分布的极分解**（Lemma 3.4）：$\mathbf{n} = r \cdot \mathbf{u}$，其中 $r^2 \sim \chi^2(n)$，$\mathbf{u} \sim \mathrm{Uniform}(S^{n-1})$，且两者独立。因此，只要方向分量 $\mathbf{u}$ 在低阶矩上逼近球面均匀分布，乘以正确的卡方半径后，$\mathbf{z}_w$ 就与标准高斯噪声 $\mathcal{N}(0,\mathbf{I})$ 统计不可分。正交旋转 $\mathbf{C}$ 将 $\mathbf{z}^{(2)}$ 构造成**球面 $3$-设计**（Definition 3.1），使得其前三阶矩与球面均匀分布精确匹配，从而在无需任何加密原语的前提下实现了无损嵌入。

### 2. 密钥管理与加密需求：从动态密钥到固定签名

这一 changed slot 是上述噪声生成策略的直接推论：

- **Gaussian Shading**（Yang et al., 2024）需要为每张图像生成唯一的密钥/Nonce 以驱动流密码，否则在固定密钥下会丧失无损性——这在 Figure 2 中得到验证：固定密钥时其图像级检测准确率达 97%，水印样本与无痕样本高度可分。
- **PRC Watermark**（Gunn et al., 2025）虽无需逐图像密钥，但依赖预共享密钥配合复杂的伪随机纠错编解码，提取耗时约 100 秒（Figure 4），成为实际部署的计算瓶颈。

Spherical Watermark 将整个水印系统压缩为**一个固定的“签名”**：仅需存储二进制混合矩阵 $\mathbf{T}$ 和正交旋转矩阵 $\mathbf{C}$，在嵌入和提取时直接调用，无需任何加密操作。提取过程仅需约 0.01 秒，比 PRC Watermark 快约四个数量级（Figure 4），且提取精度对 ODE 求解器类型（Table 4）和采样步数（Table 5）不敏感，表明方案与扩散采样配置解耦。

### 创新本质：可逆映射 + 矩匹配

从方法论层面审视，Spherical Watermark 的突破在于将水印嵌入重新定义为**一个从离散二进制序列到连续高斯噪声的可逆映射问题**。只要该映射满足两个条件——（1）输出分布的低阶矩与扩散先验匹配，（2）映射本身可逆——即可同时保证无损性和可提取性。正交旋转 $\mathbf{C}$ 将比特能量均匀分散到所有维度，带来了最优的抗加性噪声鲁棒性（消融实验中移除球面映射后，亮度调整等攻击下的追踪准确率剧烈下降，见 Figure 6(c)）；而 $\mathbf{T}$ 矩阵的 $3$-wise 独立性则确保了比特间不产生可被检测的统计模式。这种“矩匹配 + 可逆构造”的范式，为扩散模型水印提供了一条摆脱加密依赖的新路径。

## 整体框架

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_2eAGrunxVz/figures/001_Figure_1.jpg]]
*Figure 1: The overall pipeline of our framework*

Spherical Watermark 的整体流水线由三个可逆模块串联构成：**二进制嵌入模块（B）**、**球面映射模块（S）** 和 **扩散集成模块（G）**。其核心设计思想是将离散的水印比特序列转化为与标准高斯噪声统计不可分的连续隐变量，从而在不使用任何加密原语的前提下实现无损嵌入。

### 流水线概览

整个框架分为**离线构建**和**在线嵌入-提取**两个阶段。离线阶段，模型开发者生成一个固定的“签名”——一组可逆变换，用于将任意二进制水印编码进扩散模型的初始噪声空间。在线阶段则沿两个方向运行：

- **嵌入方向**：水印消息 $ \mathbf{m} \in \{0,1\}^{l_m} $ 依次经过 B → S → G 三个模块，转化为水印隐变量 $ \mathbf{z}_w $，再送入扩散模型的 ODE 求解器生成水印图像 $ \mathbf{O}_w $。
- **提取方向**：对可疑图像 $ \hat{\mathbf{O}}_w $，依次应用 $ \mathbf{G}^{-1} \rightarrow \mathbf{S}^{-1} \rightarrow \mathbf{B}^{-1} $，通过 VAE 编码和反向 ODE 求解估计初始噪声，最终经多数投票恢复原始水印 $ \hat{\mathbf{m}} $。

Figure 1 给出了这一双向流程的完整示意。

### 模块功能与数据流

**二进制嵌入模块（B）** 负责将水印比特与随机填充混合，增强比特间的独立性。具体而言，输入向量 $ \mathbf{x} $ 由 $ N $ 次重复的水印消息 $ \mathbf{m} $ 与随机填充 $ \mathbf{r} $ 拼接而成：

$$ \mathbf{x} = [\mathbf{m} \; \mathbf{m} \; \cdots \; \mathbf{m} \; \mathbf{r}]^{\top} \in \{0,1\}^{l_x}, \quad l_x = N \times l_m + l_r $$

随后通过 $ \mathrm{GF}(2) $ 上的可逆矩阵 $ \mathbf{T} $ 进行线性混合：

$$ \mathbf{z}^{(1)} = \mathbf{T} \mathbf{x} $$

其中 $ \mathbf{T} $ 的构造为块矩阵 $ \mathbf{T} = \begin{bmatrix} \mathbf{I}_{l_{Nm}} & \mathbf{R} \\ \mathbf{0} & \mathbf{I}_{l_r} \end{bmatrix} $，$ \mathbf{R} $ 为行稀疏度为 $ s $ 的随机二元矩阵（见 Algorithm 1）。该设计确保输出比特具有 3-wise 独立性，为后续球面映射提供均匀分布的离散基底。

**球面映射模块（S）** 将二进制向量转化为与高斯噪声分布匹配的连续隐变量，分三步完成：

1. 将 $ \mathbf{z}^{(1)} $ 映射到单位球面：$ \mathbf{v} = 2\mathbf{z}^{(1)} - \mathbf{1} $，$ \mathbf{z}^{(2)} = \mathbf{v} / \|\mathbf{v}\|_2 $。
2. 施加固定的正交旋转矩阵 $ \mathbf{C} $：$ \mathbf{z}^{(3)} = \mathbf{C}\mathbf{z}^{(2)} $，使比特能量均匀分散，并构成球面 3-设计。
3. 乘以卡方分布半径以恢复高斯径向分布：$ \mathbf{z}_w = r \mathbf{z}^{(3)} $，其中 $ r^2 \sim \chi^2(l_x) $。

这一映射的核心理论依据是多元标准高斯向量的极分解（Lemma 3.4）：$ \mathbf{n} = r \cdot \mathbf{u} $，其中 $ r^2 \sim \chi^2(n) $，$ \mathbf{u} \sim \mathrm{Uniform}(S^{n-1}) $，且二者独立。因此，只要方向分量在低阶矩上与球面均匀分布不可区分（由球面 3-设计保证），合成向量 $ \mathbf{z}_w $ 就与标准高斯噪声计算不可区分。

**扩散集成模块（G）** 将水印隐变量接入预训练扩散模型的标准采样流程。嵌入时，以 $ \mathbf{z}_w $ 替代随机采样的初始噪声，通过概率流 ODE 求解得到干净隐变量：

$$ \mathbf{z}_0 = \mathrm{ODESolve}(\mathbf{z}_w; s_\theta, \text{cond}, T, 0) $$

提取时，对可疑图像先经 VAE 编码获得 $ \hat{\mathbf{z}}_0 $，再以空文本条件反向求解 ODE 以估计初始噪声：

$$ \hat{\mathbf{z}}_T = \mathrm{ODESolve}(\hat{\mathbf{z}}_0; s_\theta, \emptyset, 0, T) $$

随后依次应用 $ \mathbf{S}^{-1} $ 和 $ \mathbf{B}^{-1} $ 进行解码：

$$ \hat{\mathbf{z}}^{(2)} = \mathbf{C}^{\top} \hat{\mathbf{z}}_T, \quad \hat{\mathbf{z}}^{(1)} = \mathrm{round}\left(\frac{\hat{\mathbf{z}}^{(2)} + 1}{2}\right), \quad \hat{\mathbf{x}} = \mathbf{T}^{-1} \hat{\mathbf{z}}^{(1)} $$

最后对 $ \hat{\mathbf{x}} $ 的前 $ l_{Nm} $ 个比特按 $ N $ 个分组执行多数投票，得到最终的水印消息 $ \hat{\mathbf{m}} $。

### 关键设计优势

与现有方案相比，该框架的两个核心变化槽位直接解决了瓶颈问题：

| 设计槽位 | 基线方案 | 本方案 |
|---------|---------|--------|
| 初始噪声生成策略 | 从 $ \mathcal{N}(0,I) $ 直接采样 | 对水印施加 T 混合、球面投影、固定正交旋转 C 和卡方半径缩放 |
| 密钥管理与加密需求 | 每图像需唯一密钥/Nonce（Gaussian Shading）或预共享密钥加复杂纠错编解码（PRC Watermark） | 仅需一个固定的混合矩阵 T 和正交旋转矩阵 C，无加密原语 |

这一设计消除了每图像动态密钥管理的开销，同时通过球面映射的几何性质保证了无损性和鲁棒性。提取耗时约 0.01 秒，比 PRC Watermark 快约四个数量级（Figure 4），使方案在大规模 API 部署场景下具有实际可行性。

> **注意**：当前方案依赖扩散模型的反演过程，对于非高斯先验或不支持精确反演的生成模型，适用性受限。此外，高阶矩可能偏离真实高斯分布，在极端统计测试下存在被检测的风险。

## 核心模块与公式推导

Spherical Watermark 的核心在于将离散水印比特映射为与扩散模型先验统计不可分的连续隐变量，且全程无需加密原语。该映射由三个可逆模块串联构成：**Binary Embedding Module (B)**、**Spherical Mapping Module (S)** 和 **Diffusion Integration Module (G)**，整体流水线见 Figure 1。

### 问题形式化：无损可逆映射

设水印消息为 $\mathbf{m} \in \{0,1\}^{l_m}$，目标是将 $\mathbf{m}$ 映射为水印隐变量 $\mathbf{z}_w \in \mathbb{R}^{l_x}$，使其满足两个条件（Section 3.1）：

1. **不可检测性（无损性）**：对于任意概率多项式时间区分器 $A$，水印噪声与标准高斯噪声计算不可区分：
   $$\big| \Pr[A(\mathbf{z}_w)=1] - \Pr[A(\mathbf{z})=1] \big| \leq \mathsf{negl}(\rho)$$

2. **可追踪性（精确提取）**：通过扩散反演和逆映射，以可忽略的错误概率恢复原水印：
   $$\Pr\big[ \mathsf{Extract}(\mathcal{G}^{-1}(\mathbf{O}_w)) = \mathbf{m} \big] \geq 1 - \mathsf{negl}(\rho)$$

### 模块一：Binary Embedding Module (B)

该模块将水印比特与随机填充混合，增强比特间的独立性。

首先对水印消息进行预处理：将 $\mathbf{m}$ 重复 $N$ 次并与随机填充 $\mathbf{r}$ 拼接，形成长度为 $l_x = N \cdot l_m + l_r$ 的二进制向量：
$$\mathbf{x} = [\mathbf{m} \;\; \mathbf{m} \;\; \cdots \;\; \mathbf{m} \;\; \mathbf{r}]^{\top} \in \{0,1\}^{l_x}$$

随后在 $\mathrm{GF}(2)$ 上通过可逆矩阵 $\mathbf{T}$ 进行线性混合（Eq. 9）：
$$\mathbf{z}^{(1)} = \mathbf{T} \mathbf{x}, \quad \mathbf{T} = \begin{bmatrix} \mathbf{I}_{l_{Nm}} & \mathbf{R} \\ \mathbf{0} & \mathbf{I}_{l_r} \end{bmatrix}$$

其中 $\mathbf{R}$ 是按 Algorithm 1 构造的稀疏二元矩阵，行稀疏度为 $s$。$\mathbf{T}$ 的分块下三角结构保证了 $\mathrm{GF}(2)$ 上的可逆性，同时将水印比特与随机填充充分混合，使输出比特满足 3-wise 独立性。

### 模块二：Spherical Mapping Module (S)

该模块是保证无损性和鲁棒性的关键，其设计基于多元高斯分布的极分解原理（Lemma 3.4）：
$$\mathbf{n} = r \cdot \mathbf{u}, \quad r^2 \sim \chi^2(n), \quad \mathbf{u} \sim \mathrm{Uniform}(S^{n-1})$$
其中 $r$ 与 $\mathbf{u}$ 统计独立。这意味着若方向分量在低阶矩上与球面均匀分布一致，且径向分量服从卡方分布，则合成向量精确服从标准高斯分布。

球形映射的具体步骤（Eq. 10）：
1. 将二进制向量映射到单位球面：$\mathbf{v} = 2\mathbf{z}^{(1)} - \mathbf{1}$，$\mathbf{z}^{(2)} = \frac{\mathbf{v}}{\|\mathbf{v}\|_2}$
2. 施加固定的正交旋转矩阵 $\mathbf{C}$：$\mathbf{z}^{(3)} = \mathbf{C}\mathbf{z}^{(2)}$
3. 乘以卡方分布半径：$\mathbf{z}_w = r \cdot \mathbf{z}^{(3)}$，其中 $r^2 \sim \chi^2(l_x)$

正交旋转 $\mathbf{C}$ 的作用是将离散点集转化为球面 3-设计（Definition 3.1），使其前 3 阶矩与球面均匀分布一致，从而保证与高斯先验的统计不可分性。同时，$\mathbf{C}$ 将比特能量均匀分散到所有维度，赋予方案对加性噪声的最优鲁棒性。

### 模块三：Diffusion Integration Module (G)

将 $\mathbf{z}_w$ 作为初始噪声送入预训练扩散模型，通过概率流 ODE 生成水印图像（Eq. 8, Eq. 11）：
$$\frac{d\mathbf{z}_t}{dt} = f_t(\mathbf{z}_t) - \frac{1}{2} g_t^2 \nabla_{\mathbf{z}_t} \log p_t(\mathbf{z}_t)$$
$$\mathbf{z}_0 = \mathrm{ODESolve}(\mathbf{z}_w; s_\theta, \mathrm{cond}, T, 0)$$

**提取过程**则反向执行三个模块的逆变换（$G^{-1}, S^{-1}, B^{-1}$）：
1. 通过 VAE 编码器估计怀疑图像的隐变量 $\hat{\mathbf{z}}_0$，并以空文本条件反向求解 ODE 得到初始噪声估计（Eq. 12）：
   $$\hat{\mathbf{z}}_T = \mathrm{ODESolve}(\hat{\mathbf{z}}_0; s_\theta, \emptyset, 0, T)$$
2. 逆球形映射：$\hat{\mathbf{z}}^{(2)} = \mathbf{C}^{\top} \hat{\mathbf{z}}_T$，取整恢复二进制：$\hat{\mathbf{z}}^{(1)} = \mathrm{round}\left(\frac{\hat{\mathbf{z}}^{(2)}+1}{2}\right)$
3. 逆二元嵌入：$\hat{\mathbf{x}} = \mathbf{T}^{-1} \hat{\mathbf{z}}^{(1)}$，对 $N$ 个重复块进行多数投票得到最终水印 $\hat{\mathbf{m}}$（Eq. 13）。

整个框架仅需预先生成固定的 $\mathbf{T}$ 和 $\mathbf{C}$ 作为“签名”，无需每图像动态密钥，从根本上消除了流密码或纠错码带来的密钥存储与计算开销。

## 实验与分析

### 无损性与不可检测性验证

Spherical Watermark 在图像质量保真度上达到了与原图分布无显著差异的水平。Table 1 的 FID 对比显示，在 COCO 数据集配合 SD v2.1 的条件下，本方法的 FID 为 46.81 ± 1.10，与原始无痕图像的 46.81 ± 1.06 几乎一致；在所有数据集和模型组合中，仅 **PRC Watermark**（Gunn et al., 2025）与本方法能够维持这一无损特性，而 **Tree-Ring**（Wen et al., NeurIPS 2023）、**Gaussian Shading**（Yang et al., 2024）等方案均引起了显著的分布偏移。

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_2eAGrunxVz/figures/002_Table_1.jpg]]
*Table 1: FID value for different watermarking methods. Lower FID indicates higher image quality. MeanStd represents the mean value with 1-sigma error bar*

不可检测性方面，Figure 2 展示了在潜在空间和图像空间分别训练二分类器以区分水印样本与无痕样本的实验结果。在固定密钥设定下，Tree-Ring 和 Gaussian Shading 分别达到 100% 和 97% 的可检测准确率，而 PRC Watermark 与本方法的检测准确率均接近随机猜测水平（50%）。这一结果从统计不可区分性角度验证了本方案的无损嵌入设计——水印化后的初始噪声在低阶矩上与标准高斯分布不可区分，使得外部攻击者无法通过训练分类器来判定图像是否携带水印。

### 追踪准确率主结果

Table 2 给出了在 COCO 数据集和 SD v2.1 上的核心对比。在干净图像条件下，本方法与 PRC Watermark 均达到 100% 的追踪准确率（ACC）和 TPR@1%FPR。差距在后处理和对抗攻击条件下显著拉开：

- **后处理条件**：本方法的 TPR@1%FPR 为 97.57%（Table 12，SD v1.5），PRC Watermark 为 87.51%，提升 **+10.06%**；在 SDP 数据集配合 SD v2.1 上，本方法为 97.69%，PRC Watermark 为 87.19%，提升 **+10.50%**（Table 13）。
- **对抗攻击条件**：本方法在 SDP 数据集配合 SD v1.5 上的 TPR@1%FPR 达到 99.81%，PRC Watermark 为 94.58%，提升 **+5.23%**（Table 14）。在 COCO 数据集上，本方法的对抗攻击 ACC 比有损方法整体提升超过 10%（Table 2）。

传统有损方法（**DwtDct**、**DwtDctSvd**、**RivaGAN**）在后处理条件下 ACC 普遍低于 80%，对抗攻击下更是急剧下降，暴露了有损嵌入在鲁棒性上的根本缺陷。Tree-Ring 仅支持水印存在性检测，无法参与比特级 ACC 对比。

### 计算效率

Figure 4 以对数坐标展示了各潜在空间方案的水印嵌入与提取耗时。本方法的提取耗时约 **0.01 秒**，比 PRC Watermark（约 100 秒）快约四个数量级（**~10000×**）。这一差距源于本方案完全消除了加密编解码的计算瓶颈——PRC Watermark 依赖复杂的伪随机纠错码编解码，而 Spherical Watermark 仅需一次固定矩阵乘法即可完成提取。

### 消融实验

**模块消融**：Figure 6(c) 和 Figure 15 表明，移除球面映射模块（即省略正交旋转和卡方半径缩放）会导致所有攻击下的追踪准确率剧烈下降，验证了球面映射对鲁棒性的核心贡献。移除二进制嵌入模块则使潜在噪声变得可被轻易区分，破坏了不可检测性。

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_2eAGrunxVz/figures/031_Figure_15.jpg]]
*Figure 15: The ACC result of ablation on module B and S. (a-d) COCO dataset with SD v1.5. (e-h) COCO dataset with SD v2.1. (i-l) SDP dataset with SD v1.5. (m-p) SDP dataset with SD v2.1*

**参数消融**：Table 3 和 Table 15-17 系统探索了 sparsity $s$ 和重复次数 $N$ 的影响。增加 $N$ 可显著提升鲁棒性——重复编码提供了天然的冗余纠错能力；增加 $s$ 会轻微降低鲁棒性，但增强了比特间的混合独立性。这一对参数为无损性与鲁棒性之间的权衡提供了明确且可预测的控制手段。

**容量扩展性**：Figure 6(a) 和 Figure 16 显示，本方法在高达 2000 比特的水印容量下仍保持高追踪精度，而 PRC Watermark 在超过 2000 比特后迅速失效。这证明了球面设计在高维空间中的容量扩展优势——正交旋转将比特能量均匀分散到所有维度，避免了单维度信息过载。

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_2eAGrunxVz/figures/032_Figure_16.jpg]]
*Figure 16: The ACC and TPR of PRC Watermark and Ours under different watermark length l _ { m } . (a-d) COCO dataset with SD v1.5. (e-h) COCO dataset with SD v2.1. (i-l) SDP dataset with SD v1.5. (m-p) SDP dataset with SD v2.1*

**采样配置无关性**：Table 4 和 Table 5 分别验证了不同 ODE 求解器（DDIM、DPM-Solver 等）和采样步数对提取精度无明显影响，表明方案与扩散采样配置解耦，具有良好的即插即用特性。

**反演误差容忍性**：Figure 17 显示，即使在潜在空间注入噪声直至 1.5 倍标准差，提取成功率仍保持在 95% 以上，证明本方法对 DDIM 反演的不精确性具有强容忍能力。

### 失败模式与局限性

尽管整体性能优异，本方法存在以下已知失败模式：

1. **强反转破坏攻击**：大幅裁剪、涂鸦等极端操作可能导致 DDIM 反演完全失效，进而使水印提取失败。这是因为提取过程依赖从被怀疑图像到初始噪声的精确 ODE 反演。
2. **高阶矩偏差**：虽然前三阶矩与高斯分布精确匹配，但在极端统计测试下，高阶矩的微小偏差可能被检测到——这是球面 3-设计的理论边界。
3. **非高斯先验限制**：当前方案依赖扩散模型的高斯先验和可逆映射，对于基于流的模型或其他不具有高斯先验的生成框架，适用性受限。
4. **编辑与伪造场景**：本方法未专门评估在图像编辑和深度伪造场景下的水印持久性，这些场景下的鲁棒性仍需进一步探索（需人工验证）。

### 公平性说明

实验设计中采取了以下公平性保障措施：所有潜在空间方法均使用固定的 5 个不同密钥/签名并报告均值和标准差；在固定密钥设定下，Gaussian Shading 不再满足严格无损性；传统有损方法统一嵌入 32 比特，潜在空间方法配置为 512 比特；对抗攻击采用 WEvade 在白盒与黑盒设定下的平均结果，其中黑盒设定包含 JPEG 压缩预处理。Tree-Ring 仅参与 TPR 对比而不参与 ACC 对比，因其仅支持存在性检测。

### 补充图表

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_2eAGrunxVz/figures/003_Figure.jpg]]

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_2eAGrunxVz/figures/015_Figure.jpg]]

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_2eAGrunxVz/figures/016_Figure_9.jpg]]
*Figure 9: Visualized comparison of watermarked images under re-generation*

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_2eAGrunxVz/figures/021_Figure_11.jpg]]
*Figure 11: Training loss and test classification accuracy for watermark and unwatermarked samples classification. (a)(f) on the latent level. (b)(g) on the COCO dataset with SD v1.5. (c)(h) on the COCO dataset with SD v2.1. (d)(i) on the SDP dataset with SD v1.5. (e)(j) on the SDP dataset with SD v2.1. Top: Training loss. Bottom: Test classification accuracy*

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_2eAGrunxVz/figures/022_Figure.jpg]]
*Figure: (e) Image Level. (g) Image Level. (h) Image Level*

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_2eAGrunxVz/figures/023_Figure.jpg]]
*Figure: (d) Drop. (c) Brightness. (g) Median Filter*

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_2eAGrunxVz/figures/030_Figure_14.jpg]]
*Figure 14: Ablation on hyperparameters undetectability*

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_2eAGrunxVz/figures/007_Figure_5.jpg]]
*Figure 5: ACC and TPR values under Attacks, averaged over two datasets and two models. (a) Ablation on l _ { m }*

## 方法谱系与知识库定位

### 1. 与现有水印方法的关系

**Spherical Watermark** 在扩散模型水印领域处于一个独特的方法论交汇点：它同时实现了无损嵌入和加密无关的密钥管理，这在现有工作中是罕见的组合。

**与有损方法的对比**。传统频域水印方法如 **DwtDct** (Al-Haj, 2007) 和 **DwtDctSvd** (Navas et al., 2008) 通过修改图像变换域系数嵌入信息，不可避免地引入像素级失真。基于神经网络的有损方法如 **RivaGAN** (Zhang et al., 2019) 虽然提升了鲁棒性，但同样改变了生成分布。在扩散模型潜在空间方法中，**Tree-Ring** (Wen et al., NeurIPS 2023) 在初始噪声的傅里叶域刻入环形图案，仅支持存在性检测（单比特），且导致显著的分布偏移（Table 1 中 FID 明显偏离原始值）。Spherical Watermark 与这些方法的根本分歧在于：它将水印嵌入建模为从离散序列到连续高斯的分布保持映射，而非在生成过程中插入扰动信号。

**与无损方法的对比**。在无损水印阵营中，**Gaussian Shading** (Yang et al., 2024) 通过流密码将水印编码为高斯噪声，但每张图像需要唯一密钥/Nonce，在固定密钥设定下将丧失严格无损性（Figure 2 显示其可检测准确率达 97%）。**PRC Watermark** (Gunn et al., 2025) 采用伪随机纠错码实现无损嵌入，但其编解码依赖复杂的纠错算法，导致提取耗时约 100 秒，比 Spherical Watermark 慢约四个数量级（Figure 4）。Spherical Watermark 的核心改进在于：用球面 3-设计替代流密码，用可逆二进制混合矩阵替代纠错码，将密钥管理简化为一个固定的正交旋转矩阵 **C** 和混合矩阵 **T**，无需任何加密原语。

**方法论继承与突破**。Spherical Watermark 的理论基础可追溯至球面设计理论（Definition 3.1）和多元高斯分布的极分解（Lemma 3.4），但其关键创新在于将这两个经典工具组合为端到端的可逆映射管道：二进制嵌入模块（B）通过 GF(2) 上的可逆矩阵 **T** 实现比特间的 3-wise 独立性；球面映射模块（S）利用正交旋转将离散点集转化为球面 3-设计，再乘以卡方分布半径恢复高斯径向分布。这种“离散→球面→高斯”的映射链在已有水印文献中未见先例。

### 2. 适用边界与能力范围

**强适用场景**。该方法天然适配所有以标准高斯分布为先验的扩散模型，包括 Stable Diffusion v1.5/v2.1/v3、Guided Diffusion 等（Table 6 验证了跨模型的提取性能）。由于嵌入过程与扩散采样解耦，不同 ODE 求解器（DDIM、DPM-Solver 等）和采样步数对提取精度无明显影响（Table 4, Table 5），这意味着模型开发者无需为水印兼容性调整生成配置。

**边界条件**。方法的适用性受限于两个前提：（1）生成模型必须具有高斯先验和精确的反演能力——对于 Flow Matching 模型或 GAN 等非扩散架构，当前方案需要重新设计映射策略；（2）水印提取依赖 DDIM 反演的数值精度，当图像遭受极端破坏（如大面积裁剪超过 50% 或密集涂鸦）导致反演失败时，提取将完全失效。此外，当前方案未针对图像编辑和伪造场景进行设计，在这些场景下的水印持久性仍是开放问题。

**容量-鲁棒性可控性**。通过调节重复次数 N 和稀疏度 s，方法提供了明确的容量-鲁棒性权衡接口：增加 N 可显著提升抗攻击鲁棒性，增加 s 则轻微降低鲁棒性但减少计算开销（Table 3）。在 2000 比特容量下仍保持高提取精度，而 PRC Watermark 在相同容量下已迅速失效（Figure 6(a)），表明该方案具有优越的高容量扩展性。

### 3. 局限性与已知弱点

**统计不可区分性的理论边界**。虽然球面 3-设计保证了前三阶矩与均匀分布一致，但高阶矩可能偏离真实高斯分布。这意味着在极端统计测试（如基于四阶累积量的检测）下，水印噪声可能与真实高斯噪声可区分。当前实验仅通过训练二分类器验证了经验不可区分性（Figure 2），缺乏对高阶矩偏差的严格理论分析。

**反演脆弱性**。水印提取完全依赖扩散模型的反演过程。当图像经历强反转破坏攻击（如大幅裁剪、密集涂鸦或剧烈几何变换）时，DDIM 反演可能无法收敛到原始潜变量，导致水印提取完全失败。Figure 17 显示在潜在空间注入 1.5 倍标准差噪声仍保持 95% 以上成功率，但这一容忍度在图像空间可能被非线性变换放大。

**安全性假设的局限性**。当前方案假设攻击者无法获取固定的正交旋转矩阵 **C** 和混合矩阵 **T**。然而，一旦模型开发者部署水印系统，这些固定参数可能通过侧信道泄露或内部威胁暴露。针对反演攻击（adversarial reverse engineering）的安全性理论保障尚未建立，这是实际部署中的潜在风险。

**应用场景的盲区**。方法未考虑以下场景：（1）水印经过社交媒体多次有损压缩和格式转换后的可追踪性；（2）图像编辑（局部修改、风格迁移）和深度伪造场景下的水印持久性；（3）视频生成模型中的时域一致性水印嵌入。

### 4. 开放问题与后续工作方向

1. **高容量无损水印的理论极限**：在不增加存储开销的前提下，能否将水印容量提升至 10⁴ 比特级别而保持无损性？这需要更紧的球面设计构造和更高效的比特打包策略。

2. **非高斯先验模型的推广**：如何将球面映射策略推广至基于流的模型（如 Glow）或其他不具有高斯先验的生成框架？初步实验（Table 7）在 Glow 上显示了可行性，但理论框架仍需建立。

3. **反演攻击的形式化安全性**：针对已知固定变换参数的白盒攻击者，能否建立类似于密码学语义安全的水印不可伪造性理论？

4. **真实传播链的鲁棒性评估**：在模拟社交媒体传播链（多次 JPEG 压缩、缩放、截图）中的水印可追踪性尚未系统评估。

5. **动态长度水印方案**：当前方案要求预定义水印长度 $l_m$，能否设计一种无需事先定义长度的无损嵌入方案以支持动态信息长度？

6. **与内容认证的结合**：将 Spherical Watermark 与图像编辑检测、深度伪造溯源等任务结合，构建统一的生成内容溯源框架。

## 原文 PDF

![[paperPDFs/ICLR_2026/Spherical_Watermark_Encryption_Free_Lossless_Watermarking_for_Diffusion_Models.pdf]]
