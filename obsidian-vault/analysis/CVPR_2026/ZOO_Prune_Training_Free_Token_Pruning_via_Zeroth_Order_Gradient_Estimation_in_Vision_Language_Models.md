---
title: "ZOO-Prune: Training-Free Token Pruning via Zeroth-Order Gradient Estimation in Vision-Language Models"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/ZOO_Prune_Training_Free_Token_Pruning_via_Zeroth_Order_Gradient_Estimation_in_Vision_Language_Models.pdf
project_link: "https://aim-skku.github.io/ZOO-Prune"
code_link: null
aliases:
- ZP
- ZOO-Prune
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 在轻量级投影层使用零阶扰动估计每个令牌的敏感度，并将其与多样性得分相乘得到融合选择分数，从而在推理时无训练地挑选出信息量高且互补的视觉令牌。
primary_logic: 通过零阶梯度估计在投影层近似令牌敏感度，可获得与完整视觉编码器高度相关的重要性排序，且计算代价极低；将敏感度与多样性结合，既能优先保留对输出影响大的令牌，又能避免冗余，实现鲁棒的高压缩比令牌剪枝。
claims:
- 投影层敏感度排序与视觉编码器排序的斯皮尔曼秩相关性在MMMU上为0.55，在POPE上为0.49，表明投影层可可靠地代理视觉编码器的令牌重要性。
- 在LLaVA-NeXT-7B上，ZOO-Prune剪枝77.8%的令牌后仍保持98.3%的平均性能，优于所有基线方法。
- 在Qwen2.5-VL-7B上，仅保留20%令牌时，ZOO-Prune达到96.2%的平均性能，超越VisionZip和DivPrune。
- ZOO敏感度指标始终优于文本-视觉注意力（T2V Attn）和视觉-视觉注意力（V2V Attn），甚至在融合多样性后仍保持领先。
---

# ZOO-Prune: Training-Free Token Pruning via Zeroth-Order Gradient Estimation in Vision-Language Models

> [!tip] 核心洞察
> 通过零阶梯度估计在投影层近似令牌敏感度，可获得与完整视觉编码器高度相关的重要性排序，且计算代价极低；将敏感度与多样性结合，既能优先保留对输出影响大的令牌，又能避免冗余，实现鲁棒的高压缩比令牌剪枝。

| 字段 | 内容 |
|------|------|
| 中文题名 | ZOO-Prune：基于零阶梯度估计的无训练视觉-语言模型令牌剪枝 |
| 英文题名 | ZOO-Prune: Training-Free Token Pruning via Zeroth-Order Gradient Estimation in Vision-Language Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2509.24837) · [Project](https://aim-skku.github.io/ZOO-Prune) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | ZOO-Prune |
| Dataset | LLaVA-1.5-7B, LLaVA-NeXT-7B, Qwen2.5-VL-7B |

> [!tip] 效果简介
> - LLaVA-1.5-7B (9 benchmarks) 上，平均性能保持率 95.20% (64 tokens, 88.9%剪枝) vs DivPrune 94.42% (+0.78%)。
> - LLaVA-NeXT-7B (9 benchmarks) 上，平均性能保持率 (77.8%剪枝) 98.3% vs VisionZip 97.5% (+0.8%)。
> - Qwen2.5-VL-7B 上，平均性能保持率 (20%令牌保留) 96.2% vs DivPrune 96.0% (+0.2%)。

## 概要

大型视觉-语言模型（VLMs）在推理时需要处理大量视觉令牌，导致预填充和端到端延迟显著增加。现有的训练自由令牌剪枝方法主要分为两类：基于注意力的方法（如 **FastV**, ECCV 2024; **VisionZip**, CVPR 2025）利用注意力分数选择令牌，但容易保留冗余令牌簇；基于多样性的方法（如 **DivPrune**, CVPR 2025）追求特征覆盖最大化，却可能丢弃语义关键区域的令牌。在激进剪枝下，两者均难以维持稳定的多模态理解性能。

**ZOO-Prune** 提出了一种统一的训练自由剪枝框架，核心思想是：在轻量级投影层上通过零阶梯度估计量化每个视觉令牌的敏感度，再将敏感度与多样性得分相乘，形成融合选择分数。这一设计的因果机制在于——投影层的零阶敏感度排序与完整视觉编码器的重要性排序具有显著秩相关性（MMMU上斯皮尔曼相关系数0.55，POPE上0.49），使得投影层可以可靠地代理令牌重要性，而无需昂贵的反向传播或全编码器扰动。敏感度优先保留对输出影响大的令牌，多样性则抑制冗余，二者互补实现了鲁棒的高压缩比剪枝。

在方法谱系中，ZOO-Prune 区别于纯注意力剪枝和纯多样性剪枝，属于**敏感度-多样性联合剪枝**范式。其关键创新槽位在于：（1）令牌重要性评分从注意力分数或特征距离转变为投影层零阶敏感度与多样性的乘积；（2）选择策略从贪心最远距离选择转变为首令牌按最高敏感度选取、后续令牌按乘积得分贪心选择；（3）敏感度计算位置从全编码器下沉至轻量级投影层，仅需前向扰动计算。

实验表明，ZOO-Prune 在多个VLM架构上实现了领先的性能-效率权衡：在 LLaVA-NeXT-7B 上剪枝77.8%令牌后仍保持98.3%的平均性能，超越 VisionZip（97.5%）和 DivPrune；在 Qwen2.5-VL-7B 上仅保留20%令牌时达到96.2%的平均性能；在 LLaVA-NeXT-7B 上实现了2.59倍预填充加速和2.30倍端到端延迟降低。消融实验证实，敏感度与多样性的乘法融合优于单独使用任一准则，且方法对超参数不敏感。

当前方法的主要局限在于：极低令牌预算下难以区分类似概念的细粒度属性差异，在视觉杂乱的场景中易产生对象混淆，且尚未扩展到 Omni 风格统一多模态模型或视频、3D 场景等复杂输入形态。



### 视觉令牌冗余：大型视觉-语言模型的推理瓶颈

大型视觉-语言模型（Large Vision-Language Models, LVLMs）在视觉问答、图像描述等多模态任务中取得了显著进展，但其推理效率受制于一个核心瓶颈：视觉编码器生成的视觉令牌数量庞大。以 LLaVA-NeXT-7B 为例，当输入分辨率提升至 672×672 时，单张图像可产生多达 2,880 个视觉令牌，虽然带来 6.0% 的性能增益，却付出了约 3.5 倍的计算开销。这些令牌被送入 LLM 解码器进行自注意力计算时，预填充阶段的复杂度与令牌数量的平方成正比，导致推理延迟急剧上升。

然而，并非所有视觉令牌对最终输出具有同等贡献。自然图像中存在大量背景区域、重复纹理和语义冗余——例如一片天空或一面白墙可能占据数十个令牌，但其中仅少数对“描述图像中的主要物体”这一任务至关重要。因此，在推理前筛选出最具信息量的视觉令牌子集，成为降低计算开销而不显著牺牲性能的关键途径。

### 现有无训练剪枝方法的困境

为规避微调或校准数据的依赖，研究者提出了两类主流的训练自由令牌剪枝范式：

- **基于注意力的方法**（如 **FastV**, ECCV 2024; **ToMe**, ICLR 2023; **PyramidDrop**, CVPR 2025; **SparseVLM**, ICML 2025; **VisionZip**, CVPR 2025）：利用视觉-文本或视觉-视觉注意力分数作为令牌重要性指标，保留注意力权重高的令牌。然而，注意力分数往往呈现位置偏置（positional bias）——模型倾向于关注图像中心或边缘区域，导致选中的令牌在空间上高度聚集，保留了冗余信息而遗漏了其他关键区域。

- **基于多样性的方法**（如 **DivPrune**, CVPR 2025）：通过最大化所选令牌之间的特征距离来保证空间覆盖，从距离最远的令牌开始贪心选择。这种方法虽能避免聚类冗余，却可能丢弃语义敏感区域——例如，在“显示器屏幕”附近的令牌可能因特征与已选令牌相似而被排除，尽管它们对回答“屏幕上显示什么内容”至关重要。

图 1 直观地展示了这两类方法的局限：注意力剪枝（图 1a）在显著性区域保留了大量冗余令牌，多样性剪枝（图 1b）虽覆盖广泛却丢失了语义关键区域（如显示器周围的黄色高亮区域）。这一困境在激进剪枝下尤为突出——当需要保留的令牌比例极低时，单一准则难以同时兼顾信息量和互补性。

### 核心动机：敏感度与多样性的统一

上述困境揭示了一个根本需求：令牌选择需要同时回答两个问题——“这个令牌对输出有多重要？”以及“这个令牌是否提供了已有令牌之外的新信息？”前者要求一个可靠的令牌级重要性信号，后者要求对所选集合的互补性约束。

ZOO-Prune 的动机正是将这两个维度统一到一个训练自由的框架中。其核心洞察在于：**通过零阶梯度估计在轻量级投影层近似每个令牌的敏感度，可以获得与完整视觉编码器高度相关的重要性排序，且计算代价极低**。如图 2 所示，投影层敏感度排序与视觉编码器排序的斯皮尔曼秩相关性在 MMMU 上达到 0.55，在 POPE 上达到 0.49，证实了投影层可作为视觉编码器令牌重要性的可靠代理。将这一敏感度信号与多样性目标相乘融合，即可在推理时无训练地挑选出信息量高且互补的视觉令牌子集（图 1c），从而在激进压缩比下实现鲁棒的性能保持（图 1d）。



## 核心方法与创新机理

ZOO-Prune 的核心创新在于将**零阶梯度估计**引入训练自由令牌剪枝，并在**轻量级投影层**而非完整视觉编码器上计算令牌敏感度，从而以极低的计算代价获得与模型输出高度相关的重要性信号。该方法通过两个关键设计变更（changed slots）重塑了令牌选择机制。

### 变更槽一：令牌重要性评分——从注意力/多样性到“敏感度 × 多样性”

现有训练自由剪枝方法对令牌重要性的定义存在结构性缺陷：**基于注意力的方法**（如 **VisionZip**，CVPR 2025；**FastV**，ECCV 2024；**ToMe**，ICLR 2023）依赖注意力分数选取令牌，但注意力分数存在位置偏置，容易保留冗余令牌簇；**基于多样性的方法**（如 **DivPrune**，CVPR 2025）通过最大化特征覆盖来避免冗余，却可能丢弃语义关键区域的令牌（如物体边界附近）。

ZOO-Prune 将重要性评分重新定义为两项互补信号的乘积：

$$ \operatorname{Score}(i) = \widehat{S}(i) \cdot \operatorname{Div}(i, \mathcal{P}) $$

其中 $\widehat{S}(i)$ 为归一化零阶敏感度，$\operatorname{Div}(i, \mathcal{P})$ 为令牌 $i$ 相对已选集合 $\mathcal{P}$ 的多样性得分。敏感度确保优先保留对模型输出影响大的令牌，多样性则避免冗余，两者形成互补——消融实验表明，乘法融合在 LLaVA-NeXT-7B 上保留 22.2% 令牌时达到 98.3% 平均性能，优于单独使用任一准则，且无需额外超参数（Table 4）。

**零阶敏感度的计算**是该评分的核心。对每个视觉令牌 $x_i$，通过 $m$ 个随机高斯扰动方向 $u_j \sim \mathcal{N}(0, I_d)$ 和步长 $h$ 构造对称有限差分：

$$ \delta_{i,j} = \frac{M(x_i + h u_j) - M(x_i - h u_j)}{2h} $$

令牌敏感度定义为所有扰动方向上投影层响应幅度的均值：

$$ S(i) = \frac{1}{m} \sum_{j=1}^{m} \|\delta_{i,j}\|_2 $$

这一设计的理论依据在于：$S(x)$ 近似为雅可比矩阵在随机方向上的期望范数 $\mathbb{E}_u[\|J(x)u\|_2] + O(h^2)$（Proposition 3.1），即令牌对投影层输出的局部影响幅度。与依赖启发式注意力分数的方法相比，零阶敏感度直接度量令牌对模型输出的因果效应，信号更稳定且架构无关。

### 变更槽二：敏感度计算位置——从完整编码器到轻量投影层

另一个关键创新是将敏感度估计的位置从视觉编码器移至**投影层**。直觉上，视觉编码器各中间层的表示尚未与语言空间对齐，其令牌重要性排序与最终多模态输出的相关性较弱；而完整编码器的前向计算代价又过高。

ZOO-Prune 选择在投影层（多模态对齐层）进行零阶扰动估计，理由有二：

1. **排序相关性验证**：在 MMMU 和 POPE 数据集上，投影层与视觉编码器的令牌重要性排序的斯皮尔曼秩相关系数分别为 0.55 和 0.49（Figure 2），表明投影层可作为视觉编码器重要性的可靠代理。
2. **性能优势**：消融实验（Table D, Figure B）显示，以投影层计算敏感度的性能始终优于视觉编码器各中间层，尤其在激进剪枝下优势更明显——保留 160 令牌时，投影层平均性能达 94.3%，而视觉编码器 Layer 1 仅 89.1%。

这一设计使得敏感度估计仅需轻量级前向计算，无需反向传播，也无需访问完整的视觉编码器内部状态。

### 变更槽三：选择策略——从纯贪心到敏感度引导的多样性选择

DivPrune 的选择策略是从特征空间中距离最远的令牌开始贪心选择，虽能最大化覆盖，但首个令牌的选择是任意的，可能导致语义关键令牌被遗漏。ZOO-Prune 修改了这一策略：**首个令牌按最高敏感度选择**，确保语义核心区域被优先保留；**后续令牌按敏感度与多样性的乘积得分贪心选择**，在保持覆盖的同时持续偏向高影响力令牌（Algorithm 1）。

这一策略调整的实质是将敏感度作为“锚点”，引导多样性选择向语义关键区域集中，而非均匀散布。定性对比（Figure 5）显示，ZOO-Prune 的选择模式在语义聚焦与空间覆盖之间取得了平衡，而纯注意力方法倾向于聚集在位置偏置区域，纯多样性方法则缺乏语义焦点。

### 方法谱系与知识库定位

ZOO-Prune 属于**训练自由、无校准数据的 VLM 令牌剪枝**方法，其技术路线融合了零阶优化与多样性选择两个独立脉络。相比 **VisionZip**（注意力剪枝）、**DivPrune**（纯多样性剪枝）、**FastV**（层级注意力剪枝）、**PyramidDrop**（CVPR 2025，层级丢弃）和 **SparseVLM**（ICML 2025，稀疏注意力），ZOO-Prune 首次将零阶梯度估计引入令牌重要性度量，提供了注意力分数之外的第三条信号通路。该方法目前验证于编码器-解码器架构的 VLM（LLaVA 系列、Qwen2.5-VL），尚未扩展到 Omni 风格统一多模态模型或视频/3D 输入。



ZOO-Prune 是一个训练自由、无需校准数据的视觉令牌剪枝框架，其核心设计思想是在轻量级投影层通过零阶梯度估计量化每个令牌的敏感度，并将其与多样性得分融合，从而在推理时无训练地挑选出信息量高且互补的视觉令牌子集。整个流程由五个模块串联构成，如图 Figure 3 所示。

![[assets/figures/papers/paper_list_l812_https_arxiv_org_abs_2509_24837/figures/003_Figure_3.jpg]]
*Figure 3: Overview of ZOO-Prune. Given visual tokens from the vision encoder, we estimate token sensitivity via zeroth-order gradient approximation at the projection layer by adding Gaussian perturbations*

**Pipeline 总览**

1. **视觉编码器**：输入图像首先经过冻结的视觉编码器（如 CLIP-ViT），提取得到原始的视觉令牌集合 $\{x_i\}_{i=1}^{N}$。这些令牌承载了图像的空间语义信息，但数量庞大（例如 LLaVA-NeXT-7B 中可达 2880 个），是推理计算开销的主要来源。

2. **投影层**：视觉令牌通过一个轻量级的多模态投影层 $M(\cdot)$，被映射到与大语言模型（LLM）嵌入空间对齐的表示 $Z_i = M(x_i)$。该投影层在 ZOO-Prune 中承担双重角色——既是常规的多模态对齐模块，又是令牌敏感度估计的代理。

3. **ZOO 敏感度估计**：这是框架的核心创新模块。对每个视觉令牌 $x_i$，在投影层输入侧施加 $m$ 个随机高斯扰动 $u_j \sim \mathcal{N}(0, I_d)$，通过对称有限差分计算响应：
   $$\delta_{i,j} = \frac{M(x_i + h u_j) - M(x_i - h u_j)}{2h}$$
   令牌 $i$ 的敏感度定义为所有扰动方向上响应幅度的均值：
   $$S(i) = \frac{1}{m} \sum_{j=1}^{m} \|\delta_{i,j}\|_2$$
   该过程仅需纯前向计算，无需反向传播，计算代价极低。理论分析表明（Proposition 3.1），$S(x) = \mathbb{E}_u[\|J(x)u\|_2] + O(h^2)$，即敏感度近似为投影层雅可比矩阵在随机方向上的期望范数，反映了令牌对投影层输出的局部影响力。

4. **敏感度感知多样性选择**：将敏感度线性归一化到 $[0,1]$ 后，与多样性得分相乘得到融合选择分数：
   $$\operatorname{Score}(i) = \widehat{S}(i) \cdot \operatorname{Div}(i, \mathcal{P})$$
   其中多样性得分 $\operatorname{Div}(i, \mathcal{P}) = 1 - \max_{j \in \mathcal{P}} \cos(Z_i, Z_j)$ 衡量令牌 $i$ 与已选集合 $\mathcal{P}$ 的最大余弦相似度的补数。首个令牌按最高敏感度选择，后续令牌按融合得分贪心选择，确保所选子集既对输出影响大，又彼此互补、避免冗余。

5. **LLM 解码器**：筛选后的视觉令牌子集与文本查询拼接，送入冻结的 LLM 进行多模态推理。由于令牌数量大幅减少，预填充和端到端推理的延迟显著降低。

**关键设计选择**

- **为何在投影层而非视觉编码器计算敏感度**：实验表明，投影层与视觉编码器的令牌重要性排序具有中等偏上的斯皮尔曼秩相关性（MMMU 上 0.55，POPE 上 0.49，Figure 2），且投影层作为敏感度代理的性能始终优于视觉编码器各中间层，尤其在激进剪枝下优势更为显著（如保留 160 令牌时投影层平均性能 94.3%，而编码器 Layer 1 仅 89.1%，Table D）。
- **敏感度与多样性的乘法融合**：消融实验（Table 4）证实，乘法融合优于单独使用任一准则，且无需额外超参数。在 LLaVA-NeXT-7B 上保留 22.2% 令牌时达到 98.3% 的平均性能保持率。
- **超参数鲁棒性**：扰动方向数 $m$ 在 16–160 范围内、步长 $h$ 在 $10^{-4}$ 到 1 范围内对性能影响很小（Figure 4），方法对超参数不敏感，便于实际部署。



### 3.1 零阶梯度估计基础

ZOO-Prune 的核心计算工具是**随机梯度估计器**（Randomized Gradient Estimator, RGE）。对于函数 $f: \mathbb{R}^d \to \mathbb{R}$，其在点 $x$ 处的梯度可通过 $m$ 个随机方向上的对称有限差分近似：

$$\widehat{\nabla} f(x) = \frac{1}{m} \sum_{j=1}^{m} \frac{f(x + h u_j) - f(x - h u_j)}{2h} u_j \tag{1}$$

其中 $u_j \sim \mathcal{N}(0, I_d)$ 为从标准多元正态分布采样的随机方向向量，$h$ 为差分步长。该估计器仅需 $2m$ 次前向传播，无需反向传播，计算代价远低于精确梯度。

### 3.2 令牌敏感度估计模块

给定视觉编码器输出的令牌集合 $\{x_i\}_{i=1}^N$，ZOO-Prune 在**投影层**（projection layer）而非完整视觉编码器上进行敏感度估计。投影层 $M(\cdot)$ 是多模态对齐的轻量级模块，其输出对令牌扰动的响应可作为令牌重要性的可靠代理（见 Figure 2：投影层与视觉编码器的斯皮尔曼秩相关性在 MMMU 上为 0.55，在 POPE 上为 0.49）。

![[assets/figures/papers/paper_list_l812_https_arxiv_org_abs_2509_24837/figures/002_Figure_2.jpg]]
*Figure 2: Kernel density estimate (KDE) of Spearman rank correlations between token-importance rankings from the Vision encoder and the Projection layer on the MMMU and POPE datasets. Each dataset shows Spearman correlation of 0.55 and 0.49, respectively. Detailed setting is described in Appendix A*

对每个令牌 $x_i$，施加 $m$ 对高斯扰动 $x_i \pm h u_j$，计算**对称有限差分响应**：

$$\delta_{i,j} = \frac{M(x_i + h u_j) - M(x_i - h u_j)}{2h} \tag{3}$$

令牌 $i$ 的**敏感度**定义为 $m$ 个扰动方向上响应幅度的均值：

$$S(i) = \frac{1}{m} \sum_{j=1}^{m} \|\delta_{i,j}\|_2 \tag{4}$$

**理论依据**（Proposition 3.1）：敏感度 $S(x)$ 近似为雅可比矩阵 $J(x)$ 在随机方向上的期望范数，即 $S(x) = \mathbb{E}_u[\|J(x)u\|_2] + O(h^2)$，反映了令牌局部扰动对投影层输出的影响幅度。

### 3.3 敏感度感知的多样性选择模块

ZOO-Prune 采用贪心选择策略，将敏感度与多样性统一为融合得分，逐步构建剪枝后的令牌子集 $\mathcal{P}$。

**归一化敏感度**：首先对敏感度进行 min-max 归一化至 $[0, 1]$ 区间：

$$\widehat{S}(i) = \frac{S(i) - \min_j S(j)}{\max_j S(j) - \min_j S(j)}$$

**多样性得分**：对于候选令牌 $i$ 和已选集合 $\mathcal{P}$，多样性得分定义为 $i$ 与 $\mathcal{P}$ 中令牌的最大余弦相似度的补数：

$$\operatorname{Div}(i, \mathcal{P}) = 1 - \max_{j \in \mathcal{P}} \cos(Z_i, Z_j) \tag{6}$$

其中 $Z_i$ 为令牌 $i$ 经投影层后的特征表示。

**融合得分与选择策略**：首个令牌直接选择敏感度最高的令牌；后续令牌按敏感度与多样性的乘积得分贪心选择：

$$\operatorname{Score}(i) = \widehat{S}(i) \cdot \operatorname{Div}(i, \mathcal{P}) \tag{7}$$

该策略的因果机制在于：敏感度优先保留对输出影响大的令牌，多样性避免选取冗余令牌，二者互补且无需额外超参数。消融实验（Table 4）证实，乘法融合在 LLaVA-NeXT-7B 上保留 22.2% 令牌时达到 98.3% 平均性能，优于单独使用任一准则。

### 3.4 超参数鲁棒性

ZOO-Prune 涉及两个关键超参数：扰动方向数 $m$ 和差分步长 $h$。Figure 4 显示，$m$ 在 16–160 范围内、$h$ 在 $10^{-4}$ 到 1 范围内对 POPE 性能影响极小，方法对超参数不敏感，具备良好的开箱即用特性。

![[assets/figures/papers/paper_list_l812_https_arxiv_org_abs_2509_24837/figures/005_Figure_4.jpg]]
*Figure 4: Hyperparameter sensitivity on POPE with LLaVA-1.5-7B: (a) small step size h, (b) number of perturbation directions m*



## 实验与关键发现

### 主实验结果

ZOO-Prune在三个主流视觉-语言模型上进行了系统评估，涵盖LLaVA-1.5-7B、LLaVA-NeXT-7B和Qwen2.5-VL-7B，共涉及9个多模态基准测试（详见Table A）。所有对比方法均为训练自由且无需校准数据，实验在统一的lmms-eval框架和4×NVIDIA A6000 GPU环境下完成，确保比较的公平性。

**LLaVA-1.5-7B上的表现。** 在LLaVA-1.5-7B上，ZOO-Prune展现出显著的性能保持能力（Table 1）。当仅保留64个视觉令牌（剪枝率88.9%）时，ZOO-Prune达到95.20%的平均性能保持率，超越DivPrune（CVPR 2025）的94.42%。在更宽松的预算下（192 tokens），ZOO-Prune的平均性能保持率进一步提升至98.27%。这一结果表明，即使在极度压缩的条件下，ZOO敏感度与多样性的融合选择策略仍能有效保留关键视觉信息。

**LLaVA-NeXT-7B上的表现。** 在更高分辨率的LLaVA-NeXT-7B上，ZOO-Prune的优势更加突出（Table 3）。当剪枝77.8%的令牌（保留640个）时，ZOO-Prune达到98.3%的平均性能保持率，显著优于VisionZip（CVPR 2025）的97.5%。值得注意的是，随着令牌预算的减少，ZOO-Prune相对于基线的优势持续扩大：在160令牌时，ZOO-Prune的平均性能为94.3%，而VisionZip降至91.2%。

**Qwen2.5-VL-7B上的泛化能力。** 为验证方法的跨架构泛化性，ZOO-Prune在Qwen2.5-VL-7B上进行了测试（Table 2）。仅保留20%令牌时，ZOO-Prune达到96.2%的平均性能保持率，超越DivPrune的96.0%和VisionZip的95.5%。这一结果证实了ZOO敏感度估计不依赖于特定视觉编码器架构，具备良好的泛化能力。

### 消融实验

**敏感度与多样性的协同效应。** Table 4展示了在LLaVA-NeXT-7B上不同令牌选择指标的消融结果。单独使用ZOO敏感度（Sens only）在640令牌时达到97.5%的平均性能，单独使用多样性（Div only）达到97.7%，而两者的乘法融合（Multiply）达到98.3%。这一趋势在不同令牌预算下保持一致：在160令牌时，乘法融合达到95.4%，显著优于单独使用敏感度（93.8%）或多样性（94.3%）。实验表明，敏感度与多样性是互补的——敏感度确保高影响力令牌被优先保留，多样性避免冗余令牌的重复选择，二者联合使用无需额外超参数即可实现最优性能。

**投影层作为敏感度代理的优越性。** Table D和Figure B对比了使用投影层与视觉编码器各中间层作为敏感度计算位置的效果。结果表明，投影层的敏感度排序始终优于视觉编码器的任意中间层，尤其在激进剪枝下优势更加明显：在160令牌时，投影层的平均性能为94.3%，而视觉编码器Layer 1仅89.1%。这一现象可归因于投影层直接参与多模态对齐，其输出更直接地影响LLM解码器的输入表示，因此能更准确地反映令牌对最终输出的影响。

**超参数鲁棒性。** Figure 4展示了ZOO-Prune对两个关键超参数的敏感度分析。在LLaVA-1.5-7B的POPE基准上，扰动方向数m在16到160范围内变化时，F1分数波动极小；步长h在1e-4到1的宽范围内同样保持稳定。这一鲁棒性源于对称有限差分估计的统计性质——多个随机方向的平均效应平滑了单次扰动的方差，使得方法在实际部署中无需精细调参。

### 定性分析

**令牌选择模式对比。** Figure 5展示了GQA基准上不同方法的令牌选择可视化。基于注意力的方法（如VisionZip）倾向于保留位置偏置的令牌簇，导致冗余；基于多样性的方法（如DivPrune）虽然覆盖广泛，但可能丢失语义关键区域（如显示器周围的令牌）。ZOO敏感度能够捕获对输出影响大的令牌，但单独使用时可能忽略空间覆盖。ZOO-Prune通过联合优化敏感度与多样性，在不同压缩比下实现了均衡的选择模式——既聚焦语义相关区域，又保持充分的空间覆盖。

**ZOO敏感度与注意力剪枝的对比。** Figure 6系统对比了ZOO敏感度与文本-视觉注意力（T2V Attn）和视觉-视觉注意力（V2V Attn）作为剪枝准则的效果。ZOO敏感度指标在所有令牌预算下始终优于两种注意力基线，即使在与多样性结合后仍保持领先。这一优势源于注意力分数反映的是令牌间的交互强度，而非令牌对最终输出的因果影响——高注意力令牌可能是被其他令牌“查询”的被动信息源，而非主动驱动输出的关键令牌。

### 推理效率

Figure 7展示了LLaVA-NeXT-7B在POPE基准上的推理效率对比。ZOO-Prune在预填充阶段实现了2.59倍加速，端到端延迟降低2.30倍，同时仅损失极少精度。与其他方法相比，ZOO-Prune在精度-效率权衡曲线上处于帕累托前沿：在相近的延迟下，ZOO-Prune的F1分数显著高于VisionZip和DivPrune；在相近的精度下，ZOO-Prune的延迟更低。这一优势得益于ZOO敏感度估计的轻量级特性——仅需投影层的前向扰动计算，无需反向传播或完整的视觉编码器评估。

### 失败模式分析

尽管ZOO-Prune在多数场景下表现优异，Figure E揭示了两种典型的失败模式：

1. **细粒度属性混淆。** 在极低令牌预算下，模型难以区分相似概念间的细微差异，例如将“boy”误判为“baby”。这表明当视觉信息被极度压缩时，年龄等细粒度属性的判别线索可能丢失。

2. **视觉杂乱场景中的对象混淆。** 在包含多个干扰对象的复杂场景中，模型可能混淆不同物品，例如将“mug”误判为“glass”。这反映出当场景中存在多个语义相似或空间邻近的对象时，有限的令牌预算难以同时覆盖所有关键判别区域。

这些失败模式指向了ZOO-Prune的固有限制：令牌选择基于投影层输出的全局敏感度，缺乏对细粒度语义差异和对象间关系的显式建模。

### 补充图表

![[assets/figures/papers/paper_list_l812_https_arxiv_org_abs_2509_24837/figures/004_Table_1.jpg]]
*Table 1: Performance Comparison on LLaVA-1.5-7B*

![[assets/figures/papers/paper_list_l812_https_arxiv_org_abs_2509_24837/figures/007_Table_3.jpg]]
*Table 3: Performance Comparison on LLaVA-NeXT-7B*

![[assets/figures/papers/paper_list_l812_https_arxiv_org_abs_2509_24837/figures/006_Table_2.jpg]]
*Table 2: Performance comparison on Qwen2.5-VL-7B*

![[assets/figures/papers/paper_list_l812_https_arxiv_org_abs_2509_24837/figures/008_Table_4.jpg]]
*Table 4: Ablation on Token Selection Metrics with LLaVA-NeXT-7B*

![[assets/figures/papers/paper_list_l812_https_arxiv_org_abs_2509_24837/figures/011_Figure_6.jpg]]
*Figure 6: ZOO Sensitivity vs. Attention Pruning. ZOObased sensitivity (Sens) metric consistently outperforms both text-visual (T2V Attn) and visual-visual (V2V Attn) attentionbased pruning, even when combined with diversity (Div)*

![[assets/figures/papers/paper_list_l812_https_arxiv_org_abs_2509_24837/figures/010_Figure_7.jpg]]
*Figure 7: Inference efficiency on the POPE benchmark relative to the LLaVA-NeXT-7B baseline. The left scatter plot reports prefilling time, and the right scatter plot shows end-to-end (E2E) latency. Each point represents a method–token-count pair, illustrating the trade-off between computation cost and F1 score performance*

![[assets/figures/papers/paper_list_l812_https_arxiv_org_abs_2509_24837/figures/009_Figure_5.jpg]]
*Figure 5: Qualitative comparison on the GQA benchmark. Attention-based methods suffer from positional bias or redundant token clusters. Diversity-based pruning spreads tokens broadly but lacks semantic focus. The ZOO-based sensitivity captures output-related tokens but overlooks spatial coverage. Our ZOO-Prune jointly optimizes sensitivity and diversity for balanced selection across compression ratios*

![[assets/figures/papers/paper_list_l812_https_arxiv_org_abs_2509_24837/figures/016_Table.jpg]]
*Table: D. Performance comparison between the projector and vision encoder layers as sensitivity proxies. The projector consistently provides the strongest accuracy across pruning ratios*

![[assets/figures/papers/paper_list_l812_https_arxiv_org_abs_2509_24837/figures/001_Figure_1.jpg]]
*Figure 1: Illustration of training-free VLM token pruning methods. (a) Attention-based methods select tokens using attention scores, but often retain redundant tokens. (b) Diversity-based methods select tokens with different features to maximize coverage but may lose tokens located in semantically relevant regions (e.g., around the monitor, highlighted in yellow). (c) Our method employs zeroth-order gradient estimation to quantify token sensitivity and integrates these scores into a diversity objective. (d) Accuracy comparison with LLaVA-NeXT-7B across 9 benchmarks, showing that ours outperforms both VisionZip (attention-based) and DivPrune (diversity-based)*



## 定位与知识库关联

### 与现有方法的关系

ZOO-Prune 属于**训练自由（training‑free）的视觉令牌剪枝**这一研究脉络，该方向的核心目标是：在不进行任何微调或校准数据适配的前提下，于推理时直接丢弃冗余视觉令牌，以降低大型视觉‑语言模型（VLM）的计算开销。根据令牌重要性信号的不同来源，现有方法可大致分为两类：

**基于注意力的剪枝**利用 VLM 内部已有的注意力分数来评估令牌重要性。典型工作包括 **FastV**（ECCV 2024），它通过分析视觉令牌的注意力分布来识别并剪除低响应区域；**ToMe**（ICLR 2023）通过令牌合并减少冗余；**PyramidDrop**（CVPR 2025）采用层间递进式丢弃策略；**VisionZip**（CVPR 2025）和 **SparseVLM**（ICML 2025）则进一步结合文本‑视觉注意力（T2V Attn）或视觉‑视觉注意力（V2V Attn）进行剪枝。这类方法的共同瓶颈在于：注意力分数天然存在位置偏置和令牌聚类效应，容易保留空间上相邻但语义冗余的令牌，在激进剪枝下性能退化明显。

**基于多样性的剪枝**以特征空间中的最大最小距离为准则，旨在最大化所选令牌的语义覆盖。代表性工作是 **DivPrune**（CVPR 2025），它从特征距离最远的令牌开始贪心选择，有效避免了令牌聚类。然而，纯多样性准则完全忽略令牌对最终输出的因果影响，可能丢弃位于语义关键区域（如问题所指物体周围）的高信息量令牌。

ZOO-Prune 在这两条线索之上做出了**关键融合与信号源创新**：它将令牌重要性信号从“注意力分数”替换为“投影层零阶敏感度”，并将该敏感度与多样性得分相乘，形成统一的融合选择分数。这一设计使得剪枝既保留了高输出影响力的令牌，又维持了空间覆盖的互补性，在方法谱系中处于**注意力方法与多样性方法的交汇点**，同时在敏感度估计上开辟了“轻量投影层代理”这一新路径。

### 适用边界与局限

ZOO-Prune 的适用边界由以下因素界定：

1. **架构边界**：当前验证集中于编码器‑解码器架构的 VLM，包括 LLaVA‑1.5‑7B/13B、LLaVA‑NeXT‑7B 和 Qwen2.5‑VL‑7B。这些模型的共同特征是具备独立的视觉编码器、投影层和 LLM 解码器。方法尚未在 Omni 风格的统一多模态模型（如同时处理图像、音频、文本的单一 Transformer）上进行验证，因此其跨架构泛化性仍属开放问题。

2. **输入模态边界**：所有实验均在静态图像‑文本任务上进行。对于视频、3D 场景或可穿戴设备（egocentric）数据等具有时空结构或几何约束的输入，现有令牌选择策略未考虑帧间时序关联或三维空间关系，直接迁移可能失效。

3. **细粒度属性区分**：在极低令牌预算下，ZOO-Prune 难以区分相似概念间的细微差异。失败案例分析显示，当图像涉及“boy”与“baby”的年龄区分，或视觉杂乱场景中“mug”与“glass”的物体混淆时，模型容易出错。这表明敏感度‑多样性准则在语义边界模糊、需要精细视觉判别的情境中存在分辨力不足的问题。

4. **对投影层的依赖**：方法的核心假设是投影层可作为视觉编码器的可靠敏感度代理。消融实验证实，投影层的敏感度排序与视觉编码器的斯皮尔曼秩相关性在 MMMU 上为 0.55、POPE 上为 0.49，且在激进剪枝下投影层代理的性能始终优于编码器各中间层。然而，这一代理关系是否在所有 VLM 架构中一致成立，尚需更多验证。

### 开放问题

1. **跨架构扩展**：如何将 ZOO-Prune 的敏感度估计与多样性选择机制适配到 Omni 风格统一多模态模型中？这类模型可能缺乏独立的投影层，需要重新定义敏感度计算的代理位置。

2. **时空与几何结构建模**：在视频理解、3D 场景感知或 egocentric 数据中，令牌选择应如何融入时间一致性、深度信息和几何约束？简单的逐帧独立剪枝可能破坏时序连贯性。

3. **任务自适应剪枝**：能否将 ZOO-Prune 整合到视觉‑语言‑动作（VLA）智能体中，通过自适应保留与当前任务目标最相关的视觉线索，提升长期决策的稳定性？这需要将敏感度信号与任务奖励或目标条件动态关联。

4. **敏感度代理的理论理解**：投影层为何能作为视觉编码器敏感度的有效代理？其与雅可比矩阵近似（Proposition 3.1）之间的理论联系是否可推广到更一般的多模态对齐层？深入理解这一代理机制可能为更高效的剪枝策略提供指导。



## 原文 PDF

![[paperPDFs/CVPR_2026/ZOO_Prune_Training_Free_Token_Pruning_via_Zeroth_Order_Gradient_Estimation_in_Vision_Language_Models.pdf]]
