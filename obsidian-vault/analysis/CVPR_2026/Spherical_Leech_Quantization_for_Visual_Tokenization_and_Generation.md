---
title: Spherical Leech Quantization for Visual Tokenization and Generation
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Spherical_Leech_Quantization_for_Visual_Tokenization_and_Generation.pdf
project_link: "https://zhaoyue-zephyrus.github.io/npq/"
code_link: null
aliases:
- SLQ2S
- SLQVTG
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 基于网格编码（lattice coding）的几何视角，选择具有最高球体堆积密度（densest sphere packing）的网格作为码本，从而天然实现熵最大化，无需显式正则化。
primary_logic: 通过将非参数量化统一解释为网格编码，并将熵最大化等效为超球面上的最分散点配置（Tammes问题），采用24维Leech网格的第一壳层向量作为固定码本，实现了一种简单、高效、无需熵惩罚的量化方法，显著提升了图像重建与生成的质量-压缩比权衡。
claims:
- A24-SQ将码本最小距离δ_min从BSQ的0.471提升至0.866（提升超过80%），表明其码本点分布更分散，更接近理想球面堆积。
- 基于A24-SQ的自编码器仅需ℓ1、GAN和LPIPS三种损失即可训练，无需承诺损失和熵惩罚，且rFID从BSQ的1.14降至0.83。
- 在ImageNet-1k上，使用19.6万码本的视觉自回归生成模型达到FID 1.82，接近验证集预言机(1.78)，首次在无额外技巧下实现如此大规模码本的高质量生成。
- COCO2017 val (256x256) 上 rFID = 2.02
---

# Spherical Leech Quantization for Visual Tokenization and Generation

> [!tip] 核心洞察
> 通过将非参数量化统一解释为网格编码，并将熵最大化等效为超球面上的最分散点配置（Tammes问题），采用24维Leech网格的第一壳层向量作为固定码本，实现了一种简单、高效、无需熵惩罚的量化方法，显著提升了图像重建与生成的质量-压缩比权衡。

| 字段 | 内容 |
|------|------|
| 中文题名 | 球形Leech量化用于视觉标记化与生成 |
| 英文题名 | Spherical Leech Quantization for Visual Tokenization and Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.14697) · [Project](https://zhaoyue-zephyrus.github.io/npq/) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Spherical Leech Quantization (Λ24-SQ) |
| Dataset | COCO2017 val, ImageNet-1k val, Kodak, ImageNet-1k |

> [!tip] 效果简介
> - COCO2017 val (256x256) 上，rFID 2.02 vs 2.85 (BSQ d=18) (-0.83)。
> - ImageNet-1k val (256x256) 上，rFID 0.83 vs 1.14 (BSQ d=18) (-0.31)。
> - Kodak (compression) 上，PSNR / MS-SSIM / BPP 29.632 / .9637 / 0.2747 vs 28.86 / .9561 / 0.2788 (BSQ d=18) (+0.77 / +0.0076 / -0.0041)。

## 概要

### 研究问题与瓶颈

视觉标记化（visual tokenization）是将连续图像信号转换为离散符号的核心环节，直接影响后续自回归生成模型的质量与效率。近年来，非参数量化方法（如 **LFQ** (Yu et al., ICLR 2024)、**BSQ** (Zhao et al., ICLR 2025)、**FSQ** (Mentzer et al., 2023)）因其无需维护可学习码本的特性而受到关注。然而，这些方法面临一个共同瓶颈：它们依赖启发式的熵正则化项来防止码本崩溃（codebook collapse），缺乏统一的理论基础，导致训练过程复杂且码本利用率的控制不够精确。

### 核心思想

本文从**网格编码（lattice coding）** 的几何视角出发，对现有非参数量化方法进行了统一形式化，并将熵最大化问题重新解释为超球面上的**最分散点配置问题**（即Tammes问题）。基于这一洞察，作者提出了一种全新的量化方法——**球形Leech量化（Spherical Leech Quantization, Λ24-SQ）**。该方法直接采用24维Leech网格的第一壳层向量作为固定码本。Leech网格是已知具有最高球体堆积密度（densest sphere packing）的网格结构，其码本点天然具备最大化的最小间距（δ_min），从而在无需任何显式熵惩罚或承诺损失（commitment loss）的情况下，即可实现理想的码本利用率。

### 方法定位与知识库定位

Λ24-SQ在非参数量化方法谱系中占据了一个独特位置。与BSQ的启发式二值超立方体码本或FSQ的各维独立标量量化不同，Λ24-SQ的码本设计植根于深刻的几何优化理论——球体堆积与网格编码。它将量化器的设计从“训练技巧”层面提升到了“几何结构选择”层面，使得仅需 ℓ1、GAN 和 LPIPS 三种基本损失即可完成自编码器训练，大幅简化了训练流程。

在知识库定位上，本文桥接了三个领域：
- **信息论与编码理论**：将视觉标记化纳入网格编码框架；
- **离散几何**：利用Leech网格这一24维空间中的最优球体堆积结构；
- **视觉生成模型**：将上述几何结构应用于大规模自回归生成。

### 主要结果

Λ24-SQ在图像重建与生成任务上均展现出显著优势：

- **重建质量**：在ImageNet-1k 256×256验证集上，基于Λ24-SQ的自编码器将rFID从BSQ的1.14降至**0.83**，同时有效比特率略低（17.58 vs. 18 bits）。在COCO2017上，rFID从2.85降至**2.02**。
- **图像压缩**：在Kodak数据集上，Λ24-SQ在更低的码率（0.2747 BPP）下实现了更高的PSNR（29.632 dB）和MS-SSIM（0.9637）。
- **自回归生成**：首次成功训练了码本规模达**19.6万**的视觉自回归生成模型（Infinity-CC），在ImageNet-1k上达到FID **1.82**，极为接近验证集预言机的1.78，且无需索引分组、多头预测等额外技巧。

### 关键证据

- **Table 4**：Λ24-SQ的码本最小间距δ_min为**0.866**，相比BSQ的0.471提升超过80%，直接验证了其码本点分布更接近理想球面堆积。
- **Table 8**：消融实验表明，更高的δ_min与更好的重建质量呈正相关，且移除熵惩罚对Λ24-SQ影响极小，而对BSQ则导致性能大幅下降，证实了网格几何自身的正则化能力。
- **Figure 7**：扩大码本尺寸在大模型上持续改善gFID和Precision-Recall前沿，展示了方法的可扩展性。

### 局限与开放问题

当前工作主要验证了类条件图像生成，尚未探索文本条件生成等更复杂场景。Leech网格码本是固定的，可能无法适应特定数据分布，其微调空间未被探索。超大码本在较小模型上存在利用率不均衡的问题。此外，自回归生成中的采样策略仍依赖启发式调整。这些方向为后续研究留下了空间，例如将Λ24-SQ扩展至视频或音频领域，或设计可学习的轻量级变形以适应特定域。



### 视觉标记化的核心挑战

视觉标记化（visual tokenization）旨在将连续图像信号转换为离散的符号序列，是连接图像与语言模型、实现统一多模态生成的关键桥梁。其核心流程可表示为：

$$I \xrightarrow{\mathcal{E}(\cdot)} Z \in \mathbb{R}^{(\frac{H}{p} \times \frac{W}{p}) \times d} \xrightarrow{\mathcal{Q}_{VQ}(\cdot)} \hat{Z} \xrightarrow{\mathcal{G}(\cdot)} \hat{I}$$

其中编码器 $\mathcal{E}$ 将图像映射为 $d$ 维潜在表示 $Z$，量化器 $\mathcal{Q}$ 将其离散化为 $\hat{Z}$，解码器 $\mathcal{G}$ 再重建图像。量化器的设计直接决定了信息压缩的效率与重建质量之间的权衡——码本过小则表达能力不足，码本过大则面临利用率崩溃和训练不稳定的困境。

### 非参数量化方法的困境：熵正则化的理论缺失

传统可学习矢量量化（VQ）依赖梯度反向传播更新码本，面临码本崩溃（codebook collapse）和维度灾难。近年来，**非参数量化**（non-parametric quantization）方法通过固定码本避开了学习问题，成为主流方向：

- **LFQ**（Lookup-Free Quantization, Yu et al., ICLR 2024）：将潜在向量分解为二值维度，码本由超立方体顶点构成。
- **FSQ**（Finite Scalar Quantization, Mentzer et al., 2023）：在各维度独立进行有界标量量化，无需熵正则化但设计启发式。
- **BSQ**（Binary Spherical Quantization, Zhao et al., ICLR 2025）：将二值超立方体投影至单位超球面，是目前性能最强的非参数方法。

这些方法的共同瓶颈在于：**为防止码本利用率崩溃，必须引入熵正则化损失**：

$$\mathcal{L}_{\mathrm{entropy}} = \mathbb{E}[H[q(\boldsymbol{z})]] - \gamma H[\mathbb{E}[q(\boldsymbol{z})]]$$

该损失通过最大化码字分配的边际熵来强制均匀使用码本，但其权重 $\gamma$ 需要精细调参，缺乏统一的理论基础。正如论文所指出的，这种启发式正则化使训练过程复杂且控制不佳，本质上是在“打补丁”而非从根源解决问题。

### 几何视角的缺失与本文动机

现有方法的设计逻辑停留在“如何防止码本崩溃”的工程层面，而忽略了量化过程本身的几何本质：**量化本质上是在高维空间中选择一组代表点（码本），使得任意输入向量都能被最近邻点充分近似**。从这个角度看，码本设计的核心问题转化为：如何在高维超球面上配置尽可能分散的点集，以最大化码本的最小距离（$\delta_{\min}$）——这正是经典的**球体堆积问题**（sphere packing problem）和 **Tammes 问题**。

论文由此提出核心洞察：**将非参数量化统一解释为网格编码（lattice coding），并将熵最大化等效为超球面上的最分散点配置**。这一几何视角不仅揭示了现有方法的本质联系（如 Figure 1 中的 Venn 图所示），更自然引出一个根本性解决方案：直接采用已知具有最高球体堆积密度的网格作为码本，从而天然实现熵最大化，无需任何显式正则化。

在此基础上，论文选择了 **24 维 Leech 网格的第一壳层向量**作为码本——该网格在 24 维空间中实现了已知最优的球体堆积密度，其第一壳层包含 196,560 个向量，恰好构成一个规模可观且几何性质极佳的固定码本。这一方法被命名为 **球形 Leech 量化（Λ24-SQ）**，其核心优势在于：将码本设计的理论根基从“经验调参”提升至“最优几何”，以极简的训练范式（仅需 ℓ1、GAN 和 LPIPS 三种损失，无需承诺损失和熵惩罚）实现了显著的质量提升——在 ImageNet-1k 上 rFID 从 BSQ 的 1.14 降至 0.83，并在自回归生成中首次以约 20 万码本规模达到接近验证集预言机的 FID（1.82 vs. 1.78）。



## 核心方法与创新机理

### 从熵正则化到球面堆积：量化方法的几何统一

现有非参数量化方法面临一个共同瓶颈：**缺乏统一的理论基础**。LFQ（Yu et al., ICLR 2024）和BSQ（Zhao et al., ICLR 2025）等方法依赖启发式的熵正则化项来防止码本崩溃，训练过程复杂且控制不佳；FSQ（Mentzer et al., 2023）虽无需熵正则化，但其设计本质上也是启发式的。本文的核心洞察在于：**将这些方法统一解释为网格编码（lattice coding），并将熵最大化问题等价为超球面上的最分散点配置——Tammes问题**。

具体而言，论文揭示了非参数量化方法都可描述为带约束的网格码：

$$\mathbb{\Lambda}_d = \{ \lambda \in \mathbb{R}^d \mid \lambda = G b, f(\lambda) = c_1, h(\lambda) \le c_2 \}$$

其中LFQ对应生成矩阵 $G = I_d$ 且约束 $\|\lambda\|_0 = d, \|\lambda\|_1 = d$（即 $\lambda_i = \pm 1$），BSQ则在此基础上引入正交矩阵旋转。这一统一视角自然引出一个关键问题：**什么样的网格结构能天然实现熵最大化？**

答案是：**具有最高球体堆积密度（densest sphere packing）的网格**。在 $d$ 维单位超球面 $\mathbb{S}^{d-1}$ 上配置 $N$ 个点，最大化最小成对距离的优化问题为：

$$\operatorname*{max}_{\pmb{c}_1,\cdots,\pmb{c}_N \in \mathbb{S}^{d-1}} \operatorname*{min}_{1 \leq j < k \leq N} distance(\pmb{c}_j, \pmb{c}_k)$$

该问题的解天然保证了码本点的最均匀分布——**无需任何显式熵惩罚**。

### 关键设计变更：四个 changed slots

相较于主要基线BSQ，Λ24-SQ在四个关键维度上实现了根本性改进：

| 设计维度 | BSQ（基线） | Λ24-SQ（本文） | 改进机制 |
|---------|------------|---------------|---------|
| **码本设计原理** | 启发式二值超立方体 | 24维Leech网格第一壳层向量 | 最优球面堆积，$\delta_{min}$ 从0.471提升至0.866（提升>80%） |
| **训练损失函数** | 需要熵正则化项 | 仅使用 $\ell_1$, GAN, LPIPS三损失 | 网格几何天然保证码本利用率 |
| **码本规模** | $d=18$, 262,144码本 | $d=24$, 196,560固定码本 | 有效比特率17.58 bits，略低于BSQ但质量更优 |
| **自回归预测头** | 18路独立二元分类头（bitwise） | 24路9元分类头（d-itwise） | 每维独立预测可能值 $\{-4,...,4\}$，配合交叉熵损失 |

### 为什么选择Leech网格？

在已知的球体堆积结果中（Table 2），24维Leech网格 $\Lambda_{24}$ 具有独特地位：它是唯一已知的在24维实现最优球体堆积的网格，其第一壳层包含196,560个向量，恰好构成一个规模适中、分布极度均匀的码本。如Figure 2所示，在 $d=24$ 高维空间中，$\Lambda_{24}$-SQ的 $\delta_{min}(|C|)$ 远优于Fibonacci网格、随机投影等其他候选方案。

这一选择的因果链条清晰：**Leech网格的几何结构 → 码本点天然最大化最小距离 → 熵自动最大化 → 无需熵惩罚 → 训练简化且质量提升**。消融实验（Table 8）直接验证了这一逻辑：移除熵惩罚项对Λ24-SQ影响极小，而对BSQ则导致性能大幅下降。

### 大规模码本生成的关键支撑

Λ24-SQ的19.6万码本规模接近前沿语言模型，但超大码本带来训练不均衡问题（Figure 4显示使用频率比约37:1）。为此，本文引入两项关键技术：

- **Z-loss**：$\mathcal{L}_Z = \alpha |\log Z|^2 = \alpha \left|\log\left(\sum_i^V \exp(z_i)\right)\right|^2$，防止输出logit爆炸，$\alpha=10^{-4}$
- **Dion优化器**：对>1D权重张量使用Dion，1D张量和嵌入层使用Lion

Figure 3的训练曲线表明，这两项技术使梯度范数稳定、损失曲线平滑，最终达到更低的训练损失。

### VF对齐：缓解重建-生成困境

一个反直觉的发现是：使用DINOv2特征进行VF对齐虽略微降低重建指标（rFID从0.83升至0.92），却显著提升生成结果的FID、IS和召回率（Figure 5, Figure 6）。这揭示了量化表示在“忠实重建”与“语义生成”之间的根本张力，而VF对齐通过引入语义先验有效缓解了这一困境。



本文提出的球形Leech量化（Spherical Leech Quantization，**Λ24-SQ**）构建了一套从图像标记化到视觉生成的全流水线。该框架以**网格编码（lattice coding）**为统一视角，将非参数量化方法重新解释为网格上的编码问题，并借助高维球体堆积理论设计码本，从而在无需熵正则化的条件下实现高质量图像重建与生成。

### 视觉标记化流水线

图像标记化过程遵循标准的编码-量化-解码范式。输入图像 $I$ 首先经过编码器 $\mathcal{E}$ 映射为潜在表示 $Z \in \mathbb{R}^{(H/p \times W/p) \times d}$，随后由量化器 $\mathcal{Q}$ 将连续向量离散化为 $\hat{Z}$，最终由解码器 $\mathcal{G}$ 重建图像 $\hat{I}$：

$$I \xrightarrow{\mathcal{E}(\cdot)} Z \in \mathbb{R}^{(\frac{H}{p} \times \frac{W}{p}) \times d} \xrightarrow{\mathcal{Q}_{VQ}(\cdot)} \hat{Z} \xrightarrow{\mathcal{G}(\cdot)} \hat{I}$$

传统可学习向量量化（VQ）方法依赖码本学习和承诺损失（commitment loss），而非参数量化方法（如 **LFQ**（Yu et al., ICLR 2024）、**FSQ**（Mentzer et al., 2023）、**BSQ**（Zhao et al., ICLR 2025））则通过固定码本结构回避了码本学习，但普遍需要熵正则化项来防止码本崩溃：

$$\mathcal{L}_{\mathrm{entropy}} = \mathbb{E}[H[q(\boldsymbol{z})]] - \gamma H[\mathbb{E}[q(\boldsymbol{z})]]$$

其中第一项鼓励输入靠近码字，第二项最大化码本分配的均匀性。这种启发式正则化缺乏统一的理论基础，导致训练复杂且控制不佳。

### 网格编码统一视角

本文的核心贡献之一是将所有非参数量化方法统一纳入网格编码框架。一个 $d$ 维网格 $\Lambda_d$ 由生成矩阵 $G$ 和整数向量 $b$ 定义：

$$\Lambda_d = \{ \lambda \in \mathbb{R}^d \mid \lambda = G b \}$$

在此视角下，**LFQ** 对应于生成矩阵为单位阵 $G = I_d$ 且约束 $\lambda_i = \pm 1$ 的网格；**BSQ** 则通过二值超立方体顶点构造码本；**FSQ** 通过对齐边界函数和取整实现量化：

$$z \xrightarrow{f(\cdot)} \bar{z} = \lfloor L/2 \rfloor \tanh(z) \xrightarrow{Q_{FSQ}(\cdot)} \hat{z} = \mathrm{round}(\bar{z})$$

这一统一表述揭示了现有方法的本质差异在于网格的几何结构，而非损失函数的设计。

### 球形网格量化流水线

基于上述洞察，本文提出将量化问题从欧氏空间迁移到单位超球面 $\mathbb{S}^{d-1}$ 上。具体而言，编码器输出 $z$ 首先经过L2归一化投影至单位球面，再由球形网格量化器 $\mathcal{Q}_{\wedge}$ 进行最近邻搜索：

$$z \in \mathbb{R}^d \xrightarrow{\mathrm{norm}(\cdot)} \tilde{z} = \frac{z}{\|z\|} \xrightarrow{Q_{\wedge}(\cdot)} \hat{z} = \mathcal{Q}_{\wedge}(\tilde{z})$$

码本设计目标转化为**Tammes问题**——在 $d$ 维球面上放置 $N$ 个点以最大化最小成对距离：

$$\operatorname*{max}_{\pmb{c}_1,\cdots,\pmb{c}_N \in \mathbb{S}^{d-1}} \operatorname*{min}_{1 \leq j < k \leq N} \mathrm{distance}(\pmb{c}_j, \pmb{c}_k)$$

### 模块组成与数据流

整个框架由以下核心模块串联构成：

1. **编码器 $\mathcal{E}$**：将输入图像编码为 $d=24$ 维的潜在表示 $Z$。
2. **归一化层**：对编码器输出进行L2归一化，投影至24维单位超球面。
3. **Λ24-SQ量化器**：在超球面上利用Leech网格 $\Lambda_{24}$ 的第一壳层向量（共196,560个码字）进行最近邻量化。该码本固定不变，无需学习或熵惩罚。
4. **解码器 $\mathcal{G}$**：从量化后的球面表示重建图像。
5. **自回归生成模型（Infinity-CC）**：基于VAR架构的视觉自回归模型，采用24路9元分类头（d-itwise预测）逐维预测码字坐标，并通过Z-loss和Dion优化器稳定大规模码本下的训练。
6. **采样策略**：在推理阶段采用无分类器引导（CFG）、top-p/top-k采样及线性缩放等技巧控制生成质量。

与BSQ等基线相比，Λ24-SQ在训练时仅需 $\ell_1$、GAN和LPIPS三种损失函数，完全移除了承诺损失和熵正则化项。这一简化直接源于Leech网格作为已知最优24维球体堆积的几何特性——其码本点天然具有最大化的最小距离（$\delta_{\min}=0.866$，较BSQ的0.471提升超80%），从而无需额外的熵控制机制即可保证码本利用率。

### 补充图表

![[assets/figures/papers/paper_list_l934_https_arxiv_org_abs_2512_14697/figures/001_Figure_1.jpg]]
*Figure 1: Upper left: A Venn Diagram that contains all definitions and quantization methods covered in this paper. We provide a unified formulation of various non-parametric quantization methods [56, 86, 91] from a lattice-coding perspective in Section 3.1. The geometric interpretation of the entropy penalties in Section 3.2 then leads to a family of densest hypersphere packing lattices (Section 3.3). Based on the spherical Leech lattice, a 24-d case of the densest hypersphere packing lattices, we instantiate Spherical Leech Quantization*



### 视觉标记化的统一网格编码视角

本文的核心贡献在于将非参数量化方法统一为**网格编码（Lattice Coding）**的数学框架。一个 $d$ 维网格 $\Lambda_d$ 由生成矩阵 $\pmb{G}$ 和整数向量 $\pmb{b}$ 定义：

$$\Lambda_d = \{ \pmb{\lambda} \in \mathbb{R}^d \mid \pmb{\lambda} = \pmb{G b} \}$$

配合约束条件 $f(\pmb{\lambda}) = c_1$ 和 $h(\pmb{\lambda}) \leq c_2$，即可描述所有非参数量化变体。例如，**LFQ**（Yu et al., ICLR 2024）的生成矩阵为单位阵 $\pmb{G} = \pmb{I}_d$，约束为 $\|\pmb{\lambda}\|_0 = d$ 和 $\|\pmb{\lambda}\|_1 = d$，强制 $\lambda_i = \pm 1$。

视觉标记化的标准流水线为：

$$I \xrightarrow{\mathcal{E}(\cdot)} Z \in \mathbb{R}^{(\frac{H}{p} \times \frac{W}{p}) \times d} \xrightarrow{\mathcal{Q}_{VQ}(\cdot)} \hat{Z} \xrightarrow{\mathcal{G}(\cdot)} \hat{I}$$

其中 $\mathcal{E}$ 为编码器，$\mathcal{Q}_{VQ}$ 为量化器，$\mathcal{G}$ 为解码器。传统方法依赖熵正则化损失来防止码本崩溃：

$$\mathcal{L}_{\mathrm{entropy}} = \mathbb{E}[H[q(\boldsymbol{z})]] - \gamma H[\mathbb{E}[q(\boldsymbol{z})]]$$

该损失鼓励码本利用率，但缺乏统一的理论基础，导致训练复杂且控制不佳。

### 球面网格量化的几何原理

本文的**核心洞察**是将熵最大化重新解释为超球面上的**最分散点配置问题（Tammes问题）**。量化流水线变为：

$$z \in \mathbb{R}^d \xrightarrow{\mathrm{norm}(\cdot)} \tilde{z} = \frac{z}{\|z\|} \xrightarrow{Q_{\wedge}(\cdot)} \hat{z} = \mathcal{Q}_{\wedge}(\tilde{z})$$

即先将编码器输出归一化至单位超球面 $\mathbb{S}^{d-1}$，再利用球面网格量化器 $Q_{\wedge}$ 进行最近邻量化。熵最大化的目标等价于最大化 $N$ 个码本点之间的最小成对距离：

$$\operatorname*{max}_{\pmb{c}_1,\cdots,\pmb{c}_N \in \mathbb{S}^{d-1}} \operatorname*{min}_{1 \leq j < k \leq N} \mathrm{distance}(\pmb{c}_j, \pmb{c}_k)$$

这一几何视角直接导向**球体堆积（Sphere Packing）**理论：选择具有最高堆积密度的网格作为码本，即可天然实现熵最大化，无需显式熵正则化。

### Λ24-SQ：Leech网格的码本实例化

在24维空间中，**Leech网格**（$\Lambda_{24}$）是已知的最密球体堆积网格。$\Lambda_{24}$-SQ使用Leech网格的**第一壳层向量**（共196,560个点）作为固定码本，具体构造为：

$$\frac{1}{\sqrt{32}} \bigcup_{s \in \{2,3,4\}} \Lambda_{24}^{(2)}_s$$

其中 $\Lambda_{24}^{(2)}_s$ 表示Leech网格中范数为 $2s$ 的壳层向量。该码本的关键几何特性是**最小码本距离** $\delta_{\min}$ 达到 **0.866**，相比BSQ的0.471提升超过80%（Table 4），表明码本点分布更接近理想球面堆积。

![[assets/figures/papers/paper_list_l934_https_arxiv_org_abs_2512_14697/figures/006_Table_4.jpg]]
*Table 4: Comparison between the proposed Spherical Leech Quantization*

### 自回归预测的因子化设计

对于自回归生成模型，$\Lambda_{24}$-SQ采用**d-itwise因子化预测**，将24维码字的联合对数概率分解为各维度对数概率之和：

$$\log p(\pmb{c}^{(1:d)}) \approx \sum_{i}^{d} \log p(\pmb{c}^{(i)})$$

由于Leech网格第一壳层向量的每个维度取值仅限于 $\{-4, -2, -1, 0, 1, 2, 4\}$ 等9个可能值，因此预测头设计为24路独立的9元分类器，而非BSQ的18路二元分类器（Table 4）。该设计在计算效率与预测精度之间取得了良好平衡。

### 训练稳定性模块

超大码本（~196K）在较小模型上存在利用率不均衡问题（Figure 4），本文引入两项关键技巧：

![[assets/figures/papers/paper_list_l934_https_arxiv_org_abs_2512_14697/figures/008_Figure_4.jpg]]
*Figure 4: Codebook usage histogram. The imbalance in a huge codebook calls for dedicated training tricks in §4.2. Usage is computed on IN-1k val-50k over 10 VAR levels. y-axis in log scale. ⋆: 4,096 VQ codebook indices and density are normalized for illustrative purposes*

- **Z-loss**：防止输出logits爆炸，定义为 $\mathcal{L}_Z = \alpha |\log Z|^2 = \alpha \left|\log\left(\sum_i^V \exp(z_i)\right)\right|^2$，其中 $\alpha = 10^{-4}$。
- **Dion优化器**：对大于1D的权重张量使用Dion优化器，对1D张量和嵌入层使用Lion优化器，有效抑制梯度范数爆炸（Figure 3）。

![[assets/figures/papers/paper_list_l934_https_arxiv_org_abs_2512_14697/figures/007_Figure_3.jpg]]
*Figure 3: Training curve for a 16-layer ∞-CC model. The Dion optimizer addresses the problem of exploding gradient norm. Z-loss effectively regularizes | log*

### 与FSQ的对比

作为参考，**FSQ**（Mentzer et al., 2023）的量化过程为：

$$z \xrightarrow{f(\cdot)} \bar{z} = \lfloor L/2 \rfloor \tanh(z) \xrightarrow{Q_{FSQ}(\cdot)} \hat{z} = \mathrm{round}(\bar{z})$$

该方法通过有界缩放和取整实现量化，设计启发式，缺乏球面堆积的几何最优性保证。

### 补充图表

![[assets/figures/papers/paper_list_l934_https_arxiv_org_abs_2512_14697/figures/004_Figure_2.jpg]]



## 实验与关键发现

### 核心瓶颈与因果机制

现有非参数量化方法（BSQ、LFQ）的核心瓶颈在于：它们依赖启发式熵正则化来防止码本崩溃，缺乏统一的理论基础，导致训练复杂且码本利用率控制不佳。本文提出的**球形Leech量化（Λ24-SQ）** 通过网格编码（lattice coding）的几何视角，将熵最大化等效为超球面上的最分散点配置问题（Tammes问题），并选择24维Leech网格的第一壳层向量作为固定码本——该网格具有已知最高的球体堆积密度，天然实现熵最大化，无需显式熵惩罚项。

**决定性证据**：
- **Table 4**：Λ24-SQ将码本最小距离 δ_min 从BSQ的0.471提升至0.866（提升超过80%），表明其码本点分布更分散，更接近理想球面堆积。
- **Section 1 & Figure 1**：基于Λ24-SQ的自编码器仅需 ℓ1、GAN 和 LPIPS 三种损失即可训练，无需承诺损失和熵惩罚，且 rFID 从 BSQ 的 1.14 降至 0.83。
- **Table 7 & Section 5.2**：在 ImageNet-1k 上，使用 19.6 万码本的视觉自回归生成模型达到 FID 1.82，接近验证集预言机（1.78），首次在无额外技巧下实现如此大规模码本的高质量生成。

### 主要重建结果

**Table 5** 展示了在 COCO2017 和 ImageNet-1k（256×256）上的图像重建对比。Λ24-SQ 在所有指标上均优于 BSQ（d=18），且有效比特率更低（d* ≈ 17.58 vs. d=18）：

| 数据集 | 指标 | Λ24-SQ | BSQ (d=18) | 提升 |
|--------|------|--------|------------|------|
| COCO2017 val | rFID | **2.02** | 2.85 | -0.83 |
| ImageNet-1k val | rFID | **0.83** | 1.14 | -0.31 |

在图像压缩任务上（**Table 6**），Λ24-SQ 在 Kodak 数据集上以更低的比特率（0.2747 BPP vs. 0.2788 BPP）实现了更高的 PSNR（29.632 vs. 28.86）和 MS-SSIM（0.9637 vs. 0.9561），验证了其在压缩质量-比特率权衡上的优势。

![[assets/figures/papers/paper_list_l934_https_arxiv_org_abs_2512_14697/figures/010_Table_6.jpg]]
*Table 6: Image compression on Kodak*

### 自回归生成结果

**Table 7** 报告了基于 VAR 架构的 Infinity-CC 模型在 ImageNet-1k 256×256 上的类条件生成结果。使用 Λ24-SQ 的 2.8B 参数模型达到 **FID 1.82**，与验证集预言机 FID 1.78 仅差 0.04，显著优于此前基于 BSQ 的方法。这是首次在不依赖索引分组、多头预测等额外技巧的情况下，使用约 20 万码本实现接近预言机水平的生成质量。

**Figure 7** 进一步揭示了码本大小的缩放效应：
- 在大模型（0.49B）上，增大码本持续改善 gFID。
- 增大码本将 Precision-Recall Pareto 前沿推向验证集衍生的预言机 Precision-Recall 曲线。

### 消融实验

#### 1. 码本最小距离与重建质量的正相关

**Table 8** 系统比较了不同量化器（不同 δ_min）的重建性能。结果表明，更高的 δ_min 与更好的重建质量正相关，而 Λ24-SQ 在所有方法中表现最优。关键发现：
- 移除熵惩罚项对 Λ24-SQ 影响极小，而对 BSQ 则导致性能大幅下降（**Section 3.2 & Table 8**），验证了 Leech 网格几何的自身正则化能力。
- 随机投影初始化（PN-）和可学习 VQ 均无法达到 Λ24-SQ 的性能上限。

![[assets/figures/papers/paper_list_l934_https_arxiv_org_abs_2512_14697/figures/013_Table_8.jpg]]
*Table 8: Quantizer with higher*

#### 2. 预测头设计对自回归生成的影响

**Table 9** 比较了不同预测头在自回归生成中的效果：
- 交叉熵分类头（CCE）比比特级二元分类头（BCE）效果更好。
- 配合 d-itwise 预测（每维独立预测 9 个可能值 {-4,…,4}）和高级采样技巧（线性缩放 CFG/top-k），可进一步降低 FID。

**Figure 8** 提供了不同预测头与超参数的网格搜索结果，显示 CCE + d-itwise 组合在温度和 top-p 参数变化下保持稳定优势。

#### 3. VF 对齐缓解重建-生成困境

**Figure 5 & Figure 6** 展示了使用 DINOv2 特征进行 VF 对齐的效果：
- 虽然略微降低重建指标（rFID 从 0.83 升至 0.92），但显著提升生成结果的 FID、IS 和召回率。
- VF 对齐加速了生成模型的收敛，并改善了 Precision-Recall 前沿，有效缓解了重建-生成困境。

#### 4. 训练稳定性技巧

**Figure 3** 展示了 Z-loss 和 Dion 优化器对训练稳定性的影响：
- Dion 优化器解决了梯度范数爆炸问题。
- Z-loss（$ \mathcal{L}_Z = \alpha |\log Z|^2 $，α=10⁻⁴）有效正则化 logit 的规模，平滑损失和梯度曲线，降低最终训练损失。

**Figure 4** 揭示了超大码本的使用不均衡问题：Λ24-SQ 的码本使用频率比（最频繁/最少使用索引）约为 37，远高于标准 VQ 的约 5.6，这需要 Z-loss 等专用技巧来缓解。

### 失败模式与局限性

1. **任务范围受限**：当前仅验证了类条件图像生成，尚未探索文本条件生成等更复杂场景。
2. **码本固定不可学习**：Leech 网格码本是固定的，可能无法适应特定数据分布，尽管实验中性能优越，但潜在的微调空间未被探索。
3. **小模型上的码本利用不均衡**：超大码本在较小模型上利用率不均衡（Figure 4），需要额外的训练技巧支撑，增加了实现复杂性。
4. **采样策略依赖启发式**：自回归生成中的线性缩放 CFG/top-k 等采样策略依赖启发式调整，缺乏理论指导（Table 13）。

### 方法谱系与知识库定位

Λ24-SQ 在非参数量化方法谱系中占据独特位置（**Table 1** 提供完整对比）：

| 方法 | 码本设计原理 | 熵正则化需求 | 码本大小 |
|------|-------------|-------------|---------|
| **LFQ** (Yu et al., ICLR 2024) | 二值超立方体（各维独立 ±1） | 需要 | 2^d |
| **FSQ** (Mentzer et al., 2023) | 各维独立标量量化 | 不需要（启发式边界） | 各维独立 |
| **BSQ** (Zhao et al., ICLR 2025) | 二值超球面（d=18） | 需要 | 262,144 |
| **Λ24-SQ** (本文) | 24维 Leech 网格第一壳层 | **不需要** | 196,560 |

关键区分点：Λ24-SQ 是首个将球体堆积理论系统引入视觉标记化的方法，通过选择已知最优网格实现天然的熵最大化，在理论上统一了非参数量化方法的网格编码解释，在实践上以更简单的训练流程（无熵惩罚、无承诺损失）实现了更优的重建-生成权衡。

### 补充图表

![[assets/figures/papers/paper_list_l934_https_arxiv_org_abs_2512_14697/figures/009_Table_5.jpg]]
*Table 5: Image reconstruction results on COCO2017 and ImageNet-1k*

![[assets/figures/papers/paper_list_l934_https_arxiv_org_abs_2512_14697/figures/011_Figure_5.jpg]]
*Figure 5: VAR Tokenizer*

![[assets/figures/papers/paper_list_l934_https_arxiv_org_abs_2512_14697/figures/012_Figure_6.jpg]]
*Figure 6: VF alignment improves convergence and final generation results, especially recall. The model has 12 layers (240M)*

![[assets/figures/papers/paper_list_l934_https_arxiv_org_abs_2512_14697/figures/014_Table_9.jpg]]
*Table 9: ∞-CC with different prediction heads*

![[assets/figures/papers/paper_list_l934_https_arxiv_org_abs_2512_14697/figures/015_Figure_7.jpg]]
*Figure 7: Scaling effect of the codebook size. Left: Increasing the codebook size improves gFID when the model is large (0.49B). Right: Increasing the codebook size pushes the Precision-Recall Pareto frontier towards the oracle precision-recall derived from the validation set (see the zoom-in at the bottom left)*



## 定位与知识库关联

### 1. 非参数量化的统一视角：从启发式到网格编码

本文的核心贡献之一是将现有非参数量化方法统一到**网格编码（lattice coding）**框架下。在Λ24-SQ之前，非参数量化领域已发展出多条技术路线：

- **LFQ**（Lookup-Free Quantization; Yu et al., ICLR 2024）：最早提出无查找量化的概念，通过将编码器输出投影到二值超立方体顶点 $\{-1, +1\}^d$ 实现离散化。在网格编码视角下，LFQ可描述为生成矩阵 $G = I_d$ 的网格，约束条件为 $\|\lambda\|_0 = d$ 且 $\|\lambda\|_1 = d$（即各维取值 $\pm 1$）。

- **FSQ**（Finite Scalar Quantization; Mentzer et al., 2023）：在各维度上独立进行有界标量量化，通过 $\lfloor L/2 \rfloor \tanh(z)$ 映射和取整操作实现。该方法无需熵正则化，但码本设计依赖启发式边界选择。

- **BSQ**（Binary Spherical Quantization; Zhao et al., ICLR 2025）：将FSQ的二值化思想推广到超球面，在 $d=18$ 维空间构建 $2^{18} = 262,144$ 个码本点。BSQ在重建质量上显著优于LFQ，但仍需要熵正则化项来防止码本崩溃。

这些方法的共同困境在于：**缺乏统一的理论基础来解释为何某些码本设计优于其他设计**。LFQ和BSQ依赖熵正则化损失 $\mathcal{L}_{\mathrm{entropy}} = \mathbb{E}[H[q(\boldsymbol{z})]] - \gamma H[\mathbb{E}[q(\boldsymbol{z})]]$ 来强制码本利用率，但这引入了额外的超参数和训练不稳定性。FSQ虽然避免了熵惩罚，但其各维独立的标量量化设计缺乏几何最优性保证。

### 2. 几何视角的关键突破：熵最大化即球面最分散配置

Λ24-SQ的方法论突破在于将**熵最大化重新解释为超球面上的Tammes问题**——在 $d$ 维单位球面 $\mathbb{S}^{d-1}$ 上放置 $N$ 个点，使得任意两点间的最小距离最大化：

$$
\operatorname*{max}_{\boldsymbol{c}_1,\cdots,\boldsymbol{c}_N \in \mathbb{S}^{d-1}} \operatorname*{min}_{1 \leq j < k \leq N} \mathrm{distance}(\boldsymbol{c}_j, \boldsymbol{c}_k)
$$

这一视角转换具有深远意义：**码本点越分散，天然熵越高，无需显式正则化**。传统方法（LFQ、BSQ）通过损失函数间接追求码本利用的均匀性，而Λ24-SQ直接从几何结构上保证最优分散性。

基于此，论文系统考察了已知最优球体堆积（densest sphere packing）网格（Table 2），包括 $E_8$ 格（$d=8$）和Leech格 $\Lambda_{24}$（$d=24$）。在低维（$d=3$）下，Fibonacci网格已能接近最优分散配置；而在高维（$d=24$）下，Leech格展现出远超其他候选方案的 $\delta_{\min}$ 优势（Figure 2）。

### 3. Λ24-SQ的设计决策与适用边界

**码本选择**：Λ24-SQ采用Leech格 $\Lambda_{24}$ 的第一壳层向量（共196,560个），归一化至单位球面后作为固定码本。这一设计的关键参数对比如下（Table 4）：

| 方法 | 维度 $d$ | 码本大小 | $\delta_{\min}$ | 有效比特率 |
|------|----------|----------|-----------------|------------|
| BSQ | 18 | 262,144 | 0.471 | 18.00 |
| Λ24-SQ | 24 | 196,560 | **0.866** | 17.58 |

$\delta_{\min}$ 从0.471提升至0.866（**提升超过80%**），同时有效比特率略低（17.58 vs 18.00），表明Λ24-SQ在更紧凑的信息表示下实现了更优的码本分散性。

**训练简化**：由于Leech格的几何结构天然保证熵最大化，Λ24-SQ的自编码器训练**仅需 $\ell_1$、GAN和LPIPS三种损失**，完全移除了承诺损失（commitment loss）和熵惩罚项。消融实验证实，移除熵惩罚对Λ24-SQ影响极小，而对BSQ则导致性能大幅下降——这验证了网格几何的“自身正则化”能力。

**适用边界与局限**：

1. **维度刚性**：当前仅验证了 $d=24$ 的Leech格，其他维度（如 $d=8$ 的 $E_8$ 格）的有效性未被充分探索。对于需要不同码本大小的场景，缺乏灵活的维度适配方案。

2. **固定码本的非适应性**：Leech格码本是固定的，无法像可学习VQ码本那样适应特定数据分布。尽管实验表明固定几何码本已足够优越，但在领域差异极大的数据上可能存在性能瓶颈。

3. **大码本利用不均衡**：Figure 4显示，196,560个码本点的使用频率极不均衡（最频繁与最少使用之比约37，而标准VQ仅约5.6）。这需要Z-loss和Dion优化器等额外技巧来稳定训练（Figure 3），增加了实现复杂性。

4. **任务范围受限**：当前仅验证了类条件图像生成（ImageNet-1k），尚未探索文本条件生成、视频标记化、音频编码等更广泛场景。

### 4. 自回归生成的技术定位

在生成侧，Λ24-SQ配合**Infinity-CC**（基于VAR架构的自回归模型）实现了若干技术创新：

- **d-itwise预测头**：区别于BSQ的18路独立二元分类头，Λ24-SQ采用24路9元分类头（每维预测可能值 $\{-4, -3, \dots, 4\}$），通过 $\log p(\boldsymbol{c}^{(1:d)}) \approx \sum_{i}^{d} \log p(\boldsymbol{c}^{(i)})$ 实现因子化预测。消融表明，交叉熵分类头（CCE）优于比特级预测（BCE），配合d-itwise预测和采样技巧可进一步降低FID（Table 9, Table 13）。

- **训练稳定性**：Z-loss（$\mathcal{L}_Z = \alpha |\log Z|^2$，$\alpha=10^{-4}$）防止logit爆炸，Dion优化器处理高维权重的梯度爆炸问题（Figure 3）。

- **采样策略**：采用线性缩放CFG（$z_g = z_u + s(z_c - z_u)$）和top-p/top-k组合采样，但如论文自述，这些策略依赖启发式调整，缺乏理论指导。

### 5. 开放问题与未来方向

1. **跨维度与跨模态泛化**：Leech格在其他维度（如 $E_8$ 在 $d=8$）或非图像模态（视频、音频）中的有效性如何？Fibonacci网格在低维的优势能否推广？

2. **可学习变形**：能否设计轻量级的可学习变形模块，使码本在保持球面堆积优越性的同时适应特定领域？这类似于可变形卷积对固定网格的扩展思路。

3. **文本条件生成**：当前无文本条件下的生成FID已达1.82，接近验证集预言机1.78（Table 7）。引入文本引导后，码本分散性的优势是否仍能保持？

4. **与扩散模型的结合**：Λ24-SQ作为离散标记器，能否与连续扩散模型结合，实现更高质量的生成或更高效的压缩？

5. **理论完备性**：采样策略（CFG线性缩放、top-p/top-k组合）的启发式本质表明，自回归生成侧的理论基础仍落后于量化侧的几何理论，需要更系统的研究。



## 原文 PDF

![[paperPDFs/CVPR_2026/Spherical_Leech_Quantization_for_Visual_Tokenization_and_Generation.pdf]]
