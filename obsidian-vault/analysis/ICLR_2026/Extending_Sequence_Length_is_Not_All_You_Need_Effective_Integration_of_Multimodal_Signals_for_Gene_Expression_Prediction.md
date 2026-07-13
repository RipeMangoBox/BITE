---
title: "Extending Sequence Length is Not All You Need: Effective Integration of Multimodal Signals for Gene Expression Prediction"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Extending_Sequence_Length_is_Not_All_You_Need_Effective_Integration_of_Multimodal_Signals_for_Gene_Expression_Prediction.pdf
project_link: null
code_link: null
openreview_forum_id: wwPSfcf5Pj
aliases:
- PPRISMELP
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "背景染色质状态 C，由多种表观遗传信号的高维特征组合构成，作为混杂因子同时影响表观遗传特征 H 和基因表达 Y。"
primary_logic: "通过学习多个背景染色质状态的权重向量，并执行后门调整（因果干预）以消除背景信号的混杂效应，使模型仅依赖短序列和近端信号就能精确预测基因表达。"
claims:
- "Caduceus 在输入长度超过 2k 后性能持续下降；Seq2Exp 在 200k 输入时的表现与 500 bp 相当。"
- "使用全部信号训练的模型，测试时移除背景信号（DNase‑seq、Hi‑C）导致性能严重退化，尤其是移除 H3K27ac 使 MAE 上升 22.3%。"
- "Prism 在 K562 和 GM12878 上全面超越 Seq2Exp‑soft，仅用 2k 输入达到 SOTA，参数仅增加 11K。"
- "K562 上 MSE ↓ = 0.1789 ± 0.0041"
---

# Extending Sequence Length is Not All You Need: Effective Integration of Multimodal Signals for Gene Expression Prediction

> [!tip] 核心洞察
> 通过学习多个背景染色质状态的权重向量，并执行后门调整（因果干预）以消除背景信号的混杂效应，使模型仅依赖短序列和近端信号就能精确预测基因表达。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 扩展序列长度并非全部所需：多模态信号在基因表达预测中的有效整合 |
| 英文题名 | Extending Sequence Length is Not All You Need: Effective Integration of Multimodal Signals for Gene Expression Prediction |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=wwPSfcf5Pj) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Prism (Proximal regulatory integration of signals for mRNA expression levels prediction) |
| Dataset | K562, GM12878 |

> [!tip] 效果简介
> - K562 上，MSE ↓ 为 0.1789 ± 0.0041，对比 Seq2Exp‑soft: 0.1856 ± 0.0032，变化 ↓0.0067。
> - GM12878 上，Pearson ↑ 为 0.9016 ± 0.0024，对比 Seq2Exp‑soft: 0.8951 ± 0.0038，变化 ↑0.0065。

## 概要

基因表达预测的核心挑战在于整合多模态表观遗传信号，而非单纯扩展输入序列长度。本文发现，现有长序列建模方法（如基于状态空间模型的 **Caduceus** 和 **Seq2Exp**）存在根本性瓶颈：Caduceus 在输入长度超过 2k 后性能持续下降；Seq2Exp 虽能处理 200k 序列，但其表现与仅使用 500 bp 相当（Figure 1(d)）。进一步分析表明，在测试时缩短序列长度几乎不影响性能（Figure 2），说明长序列模型并未真正利用远端调控信息。

问题的本质在于，背景染色质状态 C 作为混杂因子，同时影响表观遗传特征 H 和基因表达 Y。简单拼接多模态信号使模型对背景染色质模式产生虚假关联，掩盖了近端前景信号的预测价值。例如，使用全部信号训练的模型在测试时移除 H3K27ac 会导致 MAE 上升 22.3%（Table 7），而移除背景信号（DNase-seq、Hi-C）同样造成严重性能退化（Figure 1(f)）。

为此，本文提出 **Prism（Proximal regulatory integration of signals for mRNA expression levels prediction）**，通过学习多个背景染色质状态的权重向量，并执行后门调整（因果干预）以消除背景信号的混杂效应。Prism 仅需 2k 输入序列即可在 K562 和 GM12878 两个细胞系上全面超越 SOTA 方法 Seq2Exp-soft（MSE 降低 0.0067，Pearson 提升 0.0065），而参数仅增加 11K（Table 1, Table 3）。



### 基因表达调控与多模态表观遗传信号

基因表达受染色质状态和三维基因组折叠的精密调控。远端的增强子通过染色质环化与启动子形成空间邻近，从而激活转录（Figure 1a）。这种长程调控机制意味着，仅依赖DNA序列本身不足以准确预测基因表达水平。细胞类型特异性的表观遗传信号——如DNase‑seq、Hi‑C、H3K27ac等——提供了关键的调控信息（Figure 1c），将它们整合到预测模型中成为自然的选择。

### 长序列建模的性能悖论

直觉上，更长的输入序列能捕获更远的调控互作，应当带来更好的预测性能。然而，实证证据揭示了相反的趋势。Figure 1(d) 显示，基于状态空间模型的 **Caduceus** 在输入长度超过2k bp后性能持续下降；而当前SOTA方法 **Seq2Exp**（Su et al., 2025）在使用200k输入时的表现，与仅使用500 bp时基本相当。更直接的证据来自 Figure 2：在200k序列上训练的Seq2Exp模型，测试时将输入截断至2.5k，性能几乎不变。这表明长序列模型并未真正利用远端信息，其性能瓶颈另有根源。

### 背景信号的混杂效应

问题的关键在于多模态信号本身的特性。Figure 1(f) 和 Table 7 的消融实验揭示了一个关键现象：使用全部信号训练的模型，在测试时移除特定信号会导致性能严重退化——尤其是移除H3K27ac时，MAE从0.3078飙升至0.5653（上升22.3%）。H3K27ac是活跃增强子和启动子的标志，属于**前景信号**。相比之下，移除Hi‑C仅导致4.7%的MAE上升。

这一不对称性指向一个深层问题：DNase‑seq和Hi‑C等信号在全基因组范围内广泛分布，构成了**背景染色质状态**。Table 8显示，约99%的基因拥有大量长程Hi‑C互作伙伴（中位数近200,000个），但其中绝大多数并不驱动转录激活。当模型简单拼接所有信号时，会对这些背景模式产生虚假关联，掩盖了近端前景信号（如H3K27ac）的真实预测价值。

### 因果视角下的问题重构

上述现象可通过结构因果模型（SCM，Figure 3）来理解：背景染色质状态 $C$ 作为**混杂因子**，同时影响表观遗传特征 $H$ 和基因表达 $Y$。简单拼接信号使模型学习到 $H$ 与 $Y$ 之间的混杂关联，而非真正的因果效应。现有长序列建模方法（如状态空间模型）因固定隐状态和近因偏差，非但无法解决这一混杂问题，反而随序列增长引入更多噪声，导致性能退化。

因此，核心挑战不在于“扩展序列长度以捕获更多信号”，而在于**有效解耦前景信号与背景信号的混杂效应**。这要求模型能够识别并消除背景染色质状态的干扰，使预测仅依赖于具有因果调控作用的前景特征。



## 核心方法与创新机理

### 问题瓶颈的重新定位：从长序列建模到混杂因子消除

现有基因表达预测方法普遍遵循“更长序列→更全调控信息→更高预测精度”的直觉，采用状态空间模型（如 **Caduceus**）或可学习掩码策略（如 **Seq2Exp**）对长达 200k bp 的 DNA 序列进行建模。然而，本文通过系统性的初步分析揭示了一个反直觉现象：

- **长序列建模的性能退化**：Caduceus 在输入长度超过 2k bp 后性能持续下降；Seq2Exp 在 200k bp 输入下的表现与仅使用 500 bp 时相当（Figure 1d）。进一步地，将 Seq2Exp 在测试时的输入从 200k 缩短至 2.5k，性能几乎不变（Figure 2），证明长序列模型并未真正利用远端调控信息。
- **背景信号的虚假关联**：使用全部表观遗传信号训练的模型，在测试时移除背景信号（如 DNase-seq、Hi-C）会导致性能严重退化——尤其是移除 H3K27ac 使 MAE 上升 22.3%（Table 7）。这表明模型对背景染色质模式产生了虚假依赖，而非学习到因果调控关系。

本文将这些观察归结为一个因果推断问题：背景染色质状态 $C$（由多种表观遗传信号的高维特征组合构成）作为混杂因子，同时影响表观遗传特征 $H$ 和基因表达 $Y$（Figure 3）。简单拼接多模态信号使预测模型通过后门路径 $H \leftarrow C \rightarrow Y$ 产生虚假关联，掩盖了近端前景信号的真实预测价值。

### 核心方法创新：基于后门调整的因果干预框架

针对上述瓶颈，Prism 的核心创新在于**将因果干预引入多模态基因表达预测**，通过三个关键设计实现混杂因子的消除：

**1. 双编码器架构与混杂因子建模**

与基线方法直接拼接原始信号不同，Prism 引入两个并行编码器（Figure 4）：
- **信号编码器** $g_\theta$：将原始表观遗传信号 $S$ 映射到高维特征空间 $H = g_\theta(S)$，保留完整的调控信息。
- **混杂因子编码器** $g_\omega$：学习 $n$ 个不同的权重向量 $A = [a_1, a_2, ..., a_n]$，每个向量代表一种背景染色质状态 $C_i$。该编码器被设计为轻量化模块，仅增加约 11K 参数（Table 3）。

**2. 后门调整的干预预测**

基于结构因果模型，Prism 通过后门调整公式消除混杂因子的影响：

$$\hat{Y}_{\mathrm{do}} = \frac{1}{n} \sum_{i=1}^{n} h_{\phi} ( X , H \odot a_i )$$

该操作对特征 $H$ 执行元素级加权（$\odot$），在 $n$ 种背景染色质状态下分别预测并取平均，等价于因果推断中的 $do(H)$ 操作。这迫使模型仅依赖序列 $X$ 与加权后的前景特征进行预测，切断后门路径。

**3. 联合训练目标的约束设计**

Prism 的训练目标在标准 smooth L1 损失 $\mathcal{L}_1$ 基础上引入两项关键正则化：

- **干预正则化损失** $\mathcal{L}_2$：直接约束干预预测 $\hat{Y}_{\mathrm{do}}$ 与真实表达 $Y$ 的误差，确保后门调整后的预测保持准确性。消融实验证实，干预权重 $\alpha = 0$ 时性能显著下降（Table 2b），验证了因果干预的必要性。

- **均匀多样性损失** $\mathcal{L}_3$：通过最大化权重向量间的距离，防止 $n$ 个背景状态坍缩为单一模式：

$$\mathcal{L}_3 = \log \left( \sum_{i,j} \exp ( 2t \cdot \tilde{a}_{i}^{T} \tilde{a}_{j} - 2t ) \right)$$

总训练目标为 $\mathcal{L} = \mathcal{L}_1 + \alpha \mathcal{L}_2 + \beta \mathcal{L}_3$。$\beta$ 在较宽范围内表现鲁棒（Table 2c），说明多样性约束主要起稳定作用。

### 与基线方法的差异总结

| 创新维度 | Seq2Exp 等基线 | Prism |
|---------|---------------|-------|
| 信号整合策略 | 简单拼接表观遗传信号与 DNA 序列 | 先编码为高维特征 $H$，再通过混杂编码器生成背景权重，执行后门调整 |
| 训练目标 | 仅 smooth L1 损失 | 加入干预正则化 $\mathcal{L}_2$ 和均匀多样性损失 $\mathcal{L}_3$ |
| 输入长度 | 200k bp | 仅需 2k bp，达到 SOTA |
| 因果机制 | 无因果建模，依赖相关性学习 | 明确建模混杂因子 $C$，通过 $do(H)$ 切断虚假关联 |

这一框架的核心洞察在于：**通过学习多个背景染色质状态的权重向量并执行因果干预，模型仅依赖短序列和近端信号就能精确预测基因表达**，从根本上绕过了长序列建模的技术瓶颈。



![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_wwPSfcf5Pj/figures/004_Figure_4.jpg]]
*Figure 4: Architecture of Prism. Epigenomic signals S are processed by two encoders: a signal encoder gθ extracts high-dimension epigenomic features H, while a confounder encoder $g _ { \omega }$ learns n distinct weights representing the confounder C. A final predictor $h _ { \phi }$ uses these weighted features along with the DNA sequence X to make a prediction

Prism 的整体流程围绕一个核心洞察展开：**背景染色质状态 C 作为混杂因子，同时影响表观遗传特征 H 和基因表达 Y**，简单拼接多模态信号会使模型学到虚假关联。为此，Prism 采用“双编码器 + 后门调整”的架构，将因果干预嵌入预测 pipeline。

### 输入与信号编码

模型接收两类输入：

- **DNA 序列** $X \in \mathbb{R}^{L \times 4}$，长度为 $L$（Prism 默认仅使用 2k bp，远小于基线方法的 200k bp）。
- **原始表观遗传信号** $S \in \mathbb{R}^{L \times d}$，包含多种细胞类型特异的多模态数据（如 DNase-seq、Hi-C、H3K27ac 等）。

信号 $S$ 首先经过**信号编码器** $g_\theta: \mathbb{R}^{L \times d} \to \mathbb{R}^{L \times d'}$，映射到高维特征空间 $H = g_\theta(S)$。这一步将原始信号的维度从 $d$ 扩展到 $d'$，为后续的背景状态建模提供更丰富的表示能力。

### 双分支处理与因果干预

高维特征 $H$ 随后进入两条并行的处理路径，分别对应标准预测和因果干预预测：

1. **标准预测分支**：特征 $H$ 直接与 DNA 序列 $X$ 一同送入**预测器** $h_\phi$（基于 Caduceus 的骨干网络），输出基因表达预测值。该分支的损失函数为 smooth L1 损失：
   $$\mathcal{L}_1 = \ell_{\mathrm{H}}\big(h_\phi(X, g_\theta(S)), Y\big)$$

2. **因果干预分支**：特征 $H$ 经过**混杂因子编码器** $g_\omega: \mathbb{R}^{L \times d} \to \mathbb{R}^{n \times d'}$，从原始信号 $S$ 中学习 $n$ 个背景染色质状态的权重向量 $A = [a_1, a_2, \dots, a_n]$。每个权重向量 $a_i$ 代表一种背景染色质状态，用于对高维特征 $H$ 进行元素级加权（$\odot$）。随后执行后门调整，在 $n$ 个背景状态下分别预测并取平均：
   $$\hat{Y}_{\mathrm{do}} = \frac{1}{n} \sum_{i=1}^{n} h_\phi(X, H \odot a_i)$$

   该分支的损失同样为 smooth L1 损失：
   $$\mathcal{L}_2 = \ell_{\mathrm{H}}\left(\frac{1}{n} \sum_{i=1}^{n} h_\phi(X, H \odot a_i), Y\right)$$

### 多样性约束与联合训练

为防止 $n$ 个权重向量坍缩为单一模式，Prism 引入**均匀多样性损失** $\mathcal{L}_3$，通过惩罚权重向量间的相似度来鼓励多样性：
$$\mathcal{L}_3 = \log\left(\sum_{i,j} \exp(2t \cdot \tilde{a}_i^T \tilde{a}_j - 2t)\right)$$

其中 $\tilde{a}_i$ 为归一化后的权重向量，$t$ 为温度参数。

最终训练目标为三部分损失的加权和：
$$\mathcal{L} = \mathcal{L}_1 + \alpha \mathcal{L}_2 + \beta \mathcal{L}_3$$

其中 $\alpha$ 控制干预正则化的强度（最优取 1.0），$\beta$ 控制多样性约束（对取值不敏感，0.1 至 1.0 均表现稳定）。

### 关键设计特点

- **轻量化**：混杂因子编码器 $g_\omega$ 设计极为轻量，Prism 相比 Seq2Exp-soft 仅增加约 11K 参数（Table 3），却实现了全面的性能超越。
- **短序列高效**：整个 pipeline 仅需 2k bp 输入即可达到 SOTA，从根本上规避了长序列建模中的隐状态固化和近因偏差问题。
- **端到端可学习**：背景权重向量 $A$ 并非预设的离散状态，而是通过训练数据端到端学习得到，使模型能自适应地发现数据中的背景染色质模式。



### 3.1 标准预测框架

Prism 的预测流程从多模态表观遗传信号的编码开始。给定 DNA 序列 $X \in \mathbb{R}^{L \times 4}$ 和原始表观遗传信号 $S \in \mathbb{R}^{L \times d}$（其中 $L$ 为序列长度，$d$ 为信号通道数），模型首先通过**信号编码器** $g_\theta: \mathbb{R}^{L \times d} \to \mathbb{R}^{L \times d'}$ 将原始信号映射到高维特征空间 $H = g_\theta(S)$。随后，**预测器** $h_\phi: (\mathbb{R}^{L \times 4}, \mathbb{R}^{L \times d'}) \to \mathbb{R}$ 整合序列信息和编码后的表观遗传特征，输出基因表达预测值 $\hat{Y}$。

标准训练目标为预测值与真实表达 $Y$ 之间的 smooth L1 损失（Huber loss）：

$$\mathcal{L}_{1} = \ell_{\mathrm{H}} \big( h_{\phi} ( X , g_{\theta} ( S ) ) , Y \big ) \tag{1}$$

其中 $\ell_{\mathrm{H}}$ 为 smooth L1 损失函数。该框架构成了后续因果干预模块的基础。

### 3.2 因果视角下的核心瓶颈

初步实验揭示了一个关键矛盾：尽管长序列模型理论上能捕获远端调控相互作用，但 **Caduceus** 在输入长度超过 2k 后性能持续下降，**Seq2Exp** 在 200k 输入时的表现与仅使用 500 bp 相当（Figure 1d）。进一步分析表明，简单拼接多种表观遗传信号会使模型对背景染色质模式产生虚假关联——测试时移除背景信号（如 DNase-seq、Hi-C）导致性能严重退化，尤其是移除 H3K27ac 使 MAE 上升 22.3%（Table 7）。

这指向一个因果推断问题：背景染色质状态 $C$ 作为混杂因子，同时影响表观遗传特征 $H$ 和基因表达 $Y$。标准预测 $P(Y|X, H)$ 会通过后门路径 $H \leftarrow C \rightarrow Y$ 引入虚假关联，使模型过度依赖非因果性的背景信号模式。

### 3.3 混杂因子编码器与后门调整

为解决上述问题，Prism 引入**混杂因子编码器** $g_\omega: \mathbb{R}^{L \times d} \to \mathbb{R}^{n \times d'}$，从原始表观遗传信号 $S$ 中学习 $n$ 个不同的权重向量 $A = [a_1, a_2, \ldots, a_n]$，每个 $a_i \in \mathbb{R}^{d'}$ 代表一种背景染色质状态 $C = C_i$。

基于后门调整准则，对 $H$ 进行因果干预（$do(H)$）后的预测为：

$$\hat{Y}_{\mathrm{do}} = \frac{1}{n} \sum_{i=1}^{n} h_{\phi} ( X , H \odot a_i ) \tag{2}$$

其中 $H \odot a_i$ 表示高维特征 $H$ 与第 $i$ 个背景权重向量的元素级加权。该公式的因果含义是：切断 $C \to H$ 的边，在 $n$ 个背景染色质状态下分别进行预测并平均，从而消除背景信号的混杂效应。

### 3.4 干预正则化损失

将干预预测作为正则化项引入训练目标，形成第二个损失分量：

$$\mathcal{L}_{2} = \ell_{\mathrm{H}} \left( \frac{1}{n} \sum_{i=1}^{n} h_{\phi} ( X , H \odot a_i ) , Y \right) \tag{3}$$

该损失强制模型在多个背景染色质状态下均能准确预测，从而学习对混杂因子鲁棒的特征表示。

### 3.5 均匀多样性损失

为防止 $n$ 个权重向量坍缩为单一模式，引入均匀多样性损失（借鉴 Wang & Isola, 2020）：

$$\mathcal{L}_{3} = \log \left( \sum_{i,j} \exp ( 2t \cdot \tilde{a}_{i}^{T} \tilde{a}_{j} - 2t ) \right) \tag{4}$$

其中 $\tilde{a}_i$ 为归一化后的权重向量，$t$ 为温度参数。该损失惩罚向量间的相似性，鼓励学习多样化的背景染色质状态表示。

### 3.6 联合训练目标

最终训练目标为三个损失分量的加权组合：

$$\mathcal{L} = \mathcal{L}_{1} + \alpha \mathcal{L}_{2} + \beta \mathcal{L}_{3} \tag{5}$$

其中 $\alpha$ 控制干预正则化的强度（消融实验表明 $\alpha = 1.0$ 最优，$\alpha = 0$ 时性能显著下降），$\beta$ 控制多样性约束的强度（在合理范围内表现鲁棒）。所有模块——信号编码器 $g_\theta$、混杂因子编码器 $g_\omega$ 和预测器 $h_\phi$——通过该联合损失端到端训练。



## 实验与关键发现

### 核心发现：短序列 + 因果干预 = SOTA

Prism 在 K562 和 GM12878 两种细胞系上全面超越了现有方法，且仅使用 2k bp 的输入序列，而基线方法通常需要 200k bp。具体而言，在 K562 细胞系上，Prism 的 MSE 达到 0.1789 ± 0.0041，优于 **Seq2Exp‑soft** 的 0.1856 ± 0.0032（↓0.0067）；在 GM12878 上，Pearson 相关系数达到 0.9016 ± 0.0024，同样超过 Seq2Exp‑soft 的 0.8951 ± 0.0038（↑0.0065）（Table 1）。这一性能优势在仅增加约 11K 参数的前提下实现（Table 3），证明了因果干预框架的高效性。

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_wwPSfcf5Pj/figures/005_Table_1.jpg]]
*Table 1: Performance on Gene Expression CAGE Prediction with Standard Deviation for Both Cell Types. Table 2: Hyperparameter sensitivity analysis for Prism on the K562 cell line. We evaluate the model’s performance while varying (a) the number of background states n, (b) the intervention loss weight α, and (c) the diversity loss weight $\beta$ . (b) Sensitivity on α*

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_wwPSfcf5Pj/figures/008_Table_3.jpg]]
*Table 3: Parameter comparison between models*

值得注意的是，**Caduceus** 和 **Seq2Exp** 等长序列模型在输入长度超过 2k bp 后性能持续下降（Figure 1d），而 Seq2Exp 在 200k 输入时的表现与仅使用 500 bp 相当。进一步地，在测试时将 200k 训练的 Seq2Exp 输入缩短至 2.5k，性能几乎不变（Figure 2），说明这些模型并未真正利用远端调控信息。这一现象的根本原因在于：长序列模型（如状态空间模型）因固定隐状态和近因偏差，难以有效捕获远端信号，反而引入了背景染色质信号的混杂效应。

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_wwPSfcf5Pj/figures/001_Figure_1.jpg]]
*Figure 1: (a) Long-range regulatory interactions through chromatin looping. (b) Current longsequence models suffer from technical limitations. (c) Multimodal epigenomic signals provide cell-type specific regulatory information. (d) Performance of Seq2Exp (Su et al., 2025) and Caduceus (Schiff et al., 2024) with varying input sequence lengths. (e) Different signals show varying contributions. (f) Performance degradation when specific signals are removed during testing from a model trained with all signals*

### 因果干预的必要性

消融实验直接验证了因果干预的核心地位。当干预损失权重 α = 0 时（即关闭后门调整），模型性能显著下降（Table 2b），证实仅靠标准预测损失无法消除背景信号的混杂效应。α = 1.0 时性能最优，过高（α = 10.0）反而导致轻微退化。

背景染色质状态数 n 的设置也呈现清晰的规律：n = 0（无干预）时性能最差，n ≥ 2 时显著提升，n = 4 时 MSE 达到最低的 0.1762 ± 0.0071（Table 2a）。作者最终选择 n = 2 作为默认设置，在性能与计算效率之间取得平衡。多样性损失权重 β 表现出较强的鲁棒性，β = 0.1 和 β = 1.0 时性能几乎相同，仅 β = 10.0 时略有下降（Table 2c）。

### 前景信号的关键性

信号移除实验揭示了模型对前景信号的严重依赖。使用全部信号训练的模型，在测试时移除 H3K27ac 导致 MAE 从 0.3078 急剧上升至 0.5653（↑22.3%），远高于移除其他信号的影响（Table 7）。这印证了 H3K27ac 作为活性增强子标志的核心预测价值。相比之下，移除背景信号（如 DNase‑seq、Hi‑C）同样造成性能退化（Figure 1f），但程度较轻——这些信号在训练过程中被模型错误地关联为预测线索，形成了虚假依赖。

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_wwPSfcf5Pj/figures/013_Table_7.jpg]]
*Table 7: Performance degradation from signal removal (trained with all signals)*

### 学习权重的生物学意义

Prism 学习到的混杂权重向量并非简单的特征丢弃。实验表明，学习到的权重平均仅保留约 35% 的特征，但其性能优于随机丢弃 90% 特征的模型（Table 16），证明权重具有明确的生物学选择性。对三个采样基因的可视化显示，权重向量在基因内部呈现多样性（不同区域激活不同的背景状态），而在基因间则表现出结构相似性（Figure 5），暗示学习到的背景状态可能对应不同的染色质环境类别。

一个代表性案例进一步支持了混杂因子假说：在 ENSG00000080561 位点，DNase 和 Hi‑C 信号广泛活跃，但 H3K27ac 无富集，基因表达保持低水平（0.6021）（Figure 6）。这说明仅凭染色质开放性和空间接触不足以驱动转录，背景信号确实充当了混杂因子而非因果调控因子。

### 信号组合与预训练的效果边界

单信号实验显示，H3K27ac 单独使用即可带来最显著的性能提升（Table 11），而额外引入 H3K4me3 等信号可进一步改善 Prism 的预测（Table 12），表明方法具有良好的信号扩展性。长上下文预训练虽然能缓解长序列模型的性能退化，但无法使长序列模型超越短序列模型（Table 10），这进一步强化了“扩展序列长度并非全部所需”的核心论点。

### 实验公平性说明

所有基线结果直接引用 Seq2Exp（Su et al., 2025），在相同数据划分和五个随机种子（{2, 22, 222, 2222, 22222}）上运行五轮取平均，确保比较的公平性。评估指标涵盖 MSE、MAE 和 Pearson 相关系数，训练细节（如 smooth L1 损失、基于验证集 MSE 选择最佳模型）与 Seq2Exp 保持一致。

### 补充图表

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_wwPSfcf5Pj/figures/006_Table.jpg]]
*Table: (a) Sensitivity on n*

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_wwPSfcf5Pj/figures/009_Table_4.jpg]]
*Table 4: Performance of Seq2Exp (Su et al., 2025) when testing with shortened input sequences on the K562 cell line*

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_wwPSfcf5Pj/figures/010_Table_5.jpg]]
*Table 5: Performance comparison with varying input lengths (left: Seq2Exp (Su et al., 2025), right: Caduceus (Schiff et al., 2024))*

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_wwPSfcf5Pj/figures/011_Table.jpg]]

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_wwPSfcf5Pj/figures/012_Table_6.jpg]]
*Table 6: Caduceus performance with different epigenomic signal configurations*

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_wwPSfcf5Pj/figures/014_Table_8.jpg]]
*Table 8: Statistical Summary of Hi-C Long-Range Interactions in K562 and GM12878 Cell Lines*

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_wwPSfcf5Pj/figures/016_Table_9.jpg]]
*Table 9: Hyperparameter values following Seq2Exp (Su et al., 2025)*



## 定位与知识库关联

### 1. 与基线方法的关系

Prism 的核心贡献在于**信号整合策略**和**训练目标**两个维度上的改进，其与各基线方法的关系可总结如下：

**与 Seq2Exp 的关系。** Prism 直接以 **Seq2Exp**（Su et al., 2025）为最强基线，两者共享相同的 Caduceus 骨干网络、数据划分和随机种子（{2, 22, 222, 2222, 22222}）以进行公平比较。Seq2Exp 的核心创新是在 Caduceus 上引入可学习掩码（hard/soft 变体），但仍沿用简单拼接表观遗传信号与 DNA 序列的策略。Prism 在这一关键槽位上进行了根本性替换：不再将信号简单拼接后送入预测器，而是先通过信号编码器 $g_\theta$ 映射到高维特征空间 $H$，再通过混杂因子编码器 $g_\omega$ 学习 $n$ 个背景染色质状态的权重向量，执行后门调整干预。此外，Prism 将训练目标从单一的 smooth L1 损失扩展为包含干预正则化损失 $\mathcal{L}_2$ 和均匀多样性损失 $\mathcal{L}_3$ 的联合损失。实验结果表明，Prism 仅用 2k 输入序列即全面超越 Seq2Exp-soft（K562 上 MSE 从 0.1856 降至 0.1789，GM12878 上 Pearson 从 0.8951 升至 0.9016），参数仅增加约 11K（Table 3）。

**与 Caduceus 的关系。** **Caduceus**（Schiff et al., 2024）作为基于状态空间模型（SSM）的长序列建模骨干网络，是 Prism 预测器 $h_\phi$ 的基础架构。然而，本文的关键发现之一正是 Caduceus 这类长序列模型存在根本性局限：其性能在输入长度超过 2k 后持续下降（Figure 1d），且即使预训练也只能缓解而无法超越短上下文模型的性能（Table 10）。Prism 并未试图改进 SSM 架构本身，而是通过因果干预框架使短序列模型也能达到 SOTA，从而绕开了长序列建模的技术瓶颈。

**与 Enformer 的关系。** **Enformer** 是基于 CNN-Transformer 的预测模型，使用 128 倍下采样来覆盖长距离调控区域。Prism 与 Enformer 的根本差异在于：Enformer 试图通过扩大感受野来捕获远端调控信号，而 Prism 的因果分析表明，远端信号中混杂了大量背景染色质模式的虚假关联，简单扩大感受野反而引入噪声。Prism 选择从因果角度消除混杂效应，而非从架构角度扩大感受野。

**与 EPInformer 的关系。** **EPInformer** 利用 DNase-seq peaks 定义潜在调控区域并应用注意力机制，其核心思路是通过生物学先验筛选前景区域。Prism 的因果干预框架可视为一种更系统的替代方案：不依赖预定义的峰值区域，而是通过学习多个背景染色质状态的权重向量，自动区分前景信号与背景混杂信号。

**与 HyenaDNA 和 Mamba 的关系。** **HyenaDNA**（基于 Hyena 算子）和 **Mamba**（状态空间模型）均致力于长序列的线性复杂度建模。Prism 的实验分析（Figure 1d, Figure 2）表明，这类长序列模型在实际基因表达预测任务中并未真正利用远端信息——Seq2Exp 在 200k 输入时的表现与 500 bp 相当，且测试时缩短序列长度几乎不影响性能。这从经验上质疑了继续追求更长序列建模的必要性，转而支持 Prism 所代表的“短序列+因果去混杂”路线。

### 2. 适用边界

Prism 的适用边界由以下条件限定：

- **细胞类型限制。** 当前仅评估了 K562 和 GM12878 两种细胞系，对其他细胞类型（如原代细胞、组织样本）和更复杂的生物系统中的泛化能力有待验证。
- **信号组合依赖。** Prism 依赖预选的表观遗传信号组合（DNase-seq、Hi-C、H3K27ac 等），未探索自动化信号选择或更大规模的信号集合。扩展信号实验（Table 12）表明加入 H3K4me3 可进一步提升性能，但 ChIA-PET 等功能性远程交互数据反而降低了预测性能，说明信号的选择对框架效果有显著影响。
- **混杂因子状态数的可解释性。** 混杂因子状态数 $n$ 及学习到的权重向量缺乏直接的生物学注释，目前仅能通过可视化（Figure 5）观察到基因内多样性和基因间结构相似性，但无法与已知染色质状态注释（如 ChromHMM）显式对齐。
- **任务范围。** 当前框架聚焦于 CAGE 基因表达预测任务，其在其他多模态生物学预测任务（如蛋白质表达预测、染色质状态预测）上的适用性尚待探索。

### 3. 局限与开放问题

**已知局限：**

1. **细胞系泛化不足。** 仅在两种细胞系上验证，对组织特异性调控的建模能力未知。
2. **信号选择依赖人工。** 预选信号组合的策略限制了框架在更大规模信号集合上的可扩展性。
3. **混杂因子缺乏生物学锚定。** 学习到的权重向量虽在消融实验中表现出生物学意义（Table 16 显示学习权重仅保留约 35% 特征，优于随机丢弃 90% 特征），但缺乏与已知染色质状态注释的直接对应。

**开放问题：**

1. **混杂权重的生物学对齐。** 学习到的混杂权重是否能与已知的染色质状态（如 ChromHMM 注释）显式对齐？若能建立映射，将大幅提升框架的可解释性和生物学可信度。
2. **ChIA-PET 的负向贡献。** 为什么 ChIA-PET 作为功能性远程交互数据反而降低了预测性能？这暗示并非所有远程交互信号都具有因果调控意义，部分可能本身就是混杂因子。
3. **长序列预训练的潜力上限。** 长上下文预训练是否有可能使长序列模型超越短序列模型，还是只能减轻退化？Table 10 的证据倾向于后者，但更大规模的预训练实验可能改变这一结论。
4. **因果干预框架的跨任务推广。** Prism 的因果干预框架能否推广到其他多模态生物学预测任务？其核心假设——背景信号作为混杂因子同时影响特征和标签——在蛋白质表达预测、药物响应预测等任务中是否同样成立？



## 原文 PDF

![[paperPDFs/ICLR_2026/Extending_Sequence_Length_is_Not_All_You_Need_Effective_Integration_of_Multimodal_Signals_for_Gene_Expression_Prediction.pdf]]
