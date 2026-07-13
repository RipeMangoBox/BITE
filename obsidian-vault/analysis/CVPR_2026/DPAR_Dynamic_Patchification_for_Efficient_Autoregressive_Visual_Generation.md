---
title: "DPAR: Dynamic Patchification for Efficient Autoregressive Visual Generation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/DPAR_Dynamic_Patchification_for_Efficient_Autoregressive_Visual_Generation.pdf
project_link: null
code_link: null
aliases:
- DPAR
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 基于下一令牌预测熵的动态令牌聚合：根据信息内容将低信息区域令牌合并为更大补丁，同时在高信息区域保持原有令牌粒度。
primary_logic: 下一令牌预测熵能够有效衡量图像区域的信息量，可作为指导自回归生成中自适应令牌合并的可靠准则，从而在保持生成质量的同时显著降低计算成本。
claims:
- 在 ImageNet 256×256 上，DPAR 将令牌数量降低 1.81 倍，同时最高提升 FID 达 27.1%（相对基线）。
- 在 ImageNet 384×384 上，DPAR 将训练 FLOPs 降低最高 40%，并且收敛更快。
- 动态补丁化比静态固定长度补丁取得更好的 FID（3.32 vs 3.58），且在推理时对补丁长度变化具有鲁棒性。
- ImageNet 256×256 上 FID↓ = 3.98 (DPAR-B), 2.93 (DPAR-L), 2.67 (DPAR-XL)
---

# DPAR: Dynamic Patchification for Efficient Autoregressive Visual Generation

> [!tip] 核心洞察
> 下一令牌预测熵能够有效衡量图像区域的信息量，可作为指导自回归生成中自适应令牌合并的可靠准则，从而在保持生成质量的同时显著降低计算成本。

| 字段 | 内容 |
|------|------|
| 中文题名 | DPAR：用于高效自回归视觉生成的动态分块 |
| 英文题名 | DPAR: Dynamic Patchification for Efficient Autoregressive Visual Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.21867) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | DPAR |
| Dataset | ImageNet 256×256, ImageNet 384×384 |

> [!tip] 效果简介
> - ImageNet 256×256 上，FID↓ 3.98 (DPAR-B), 2.93 (DPAR-L), 2.67 (DPAR-XL) vs 5.46 (LlamaGen-B), 3.80 (LlamaGen-L), 3.39 (LlamaGen-XL) (相对提升最高 27.1%)。
> - ImageNet 384×384 (resized to 256) 上，FID↓ 4.29 (DPAR-384-B), 2.79 (DPAR-384-L), 2.60 (DPAR-384-XL) vs 6.09 (LlamaGen-384-B), 3.07 (LlamaGen-384-L), 2.62 (LlamaGen-384-XL) (所有模型均取得更低 FID)。
> - 训练效率 (384×384) 上，Training FLOPs 258.5 GFLOPs (DPAR-XL) vs 433.6 GFLOPs (LlamaGen-XL) (减少 40%)。

## 概要

### 1. 问题与瓶颈

解码器仅自回归（Decoder-only AR）图像生成模型，如 **LlamaGen**（Sun et al., arXiv 2024），将图像编码为固定长度的一维令牌序列，并通过因果注意力逐令牌预测。该范式面临一个核心瓶颈：令牌数量随图像分辨率呈二次增长，导致自注意力的计算开销与内存占用急剧膨胀，严重制约了训练与推理效率。

### 2. 核心方法

**DPAR（Dynamic Patchification for Autoregressive Visual Generation）** 提出了一种动态令牌聚合策略，其核心洞察是：**下一令牌预测熵能够有效衡量图像区域的信息含量**。具体而言，DPAR 引入一个轻量级无条件熵模型，计算每个令牌的下一令牌预测熵；在生成过程中，根据熵值动态地将低信息区域的连续令牌合并为更大的“补丁”，而在高信息区域保持原有令牌粒度。最终，解码器仅需在数量显著减少的补丁序列上执行自回归生成，从而大幅降低计算成本。

### 3. 主要结果

在 ImageNet 类条件生成任务上，DPAR 在保持甚至提升生成质量的同时，实现了显著的计算削减：

- **质量提升**：在 256×256 分辨率下，DPAR 各变体（B/L/XL）的 FID 相较于同量级 LlamaGen 基线**相对提升最高达 27.1%**（如 DPAR-B FID 3.98 vs. LlamaGen-B 5.46）。
- **效率增益**：在 384×384 分辨率下，DPAR-XL 的令牌数量降低 **2.06 倍**，训练 FLOPs 降低 **最高 40%**，且收敛速度更快。
- **鲁棒性**：动态补丁化在推理时对补丁长度变化具有高度鲁棒性，FID 保持稳定（3.31–3.39），而静态固定长度补丁模型在相同扰动下 FID 急剧崩溃（3.58→25.59）。

### 4. 方法谱系与知识库定位

DPAR 属于**自适应令牌压缩**路线，区别于以下两类工作：

- **固定令牌缩减**：如使用静态补丁化或固定下采样因子，无法根据图像内容动态分配计算资源。
- **多尺度/随机顺序生成**：如 VAR 等通过改变生成顺序或尺度来提升效率，而 DPAR 保持标准光栅顺序，仅通过动态调整序列长度实现加速，对现有解码器架构的修改极小，兼容性强。

DPAR 的核心贡献在于首次将**下一令牌预测熵**确立为自回归图像生成中指导自适应令牌合并的可靠准则，为高效视觉生成提供了一种轻量、即插即用的范式。

### 自回归视觉生成的效率瓶颈

自回归（Autoregressive, AR）模型在语言建模领域取得了巨大成功，近年来被广泛迁移至视觉生成任务。解码器仅（decoder-only）架构将图像量化为离散令牌序列，通过逐令牌预测实现高保真图像生成。然而，这一范式面临一个根本性的效率瓶颈：**令牌数量随图像分辨率呈二次增长**。对于一张分辨率为 $H \times W$ 的图像，经 VQ-VAE 下采样后产生的令牌数 $T$ 与像素数成正比，导致 Transformer 自注意力的计算开销与内存占用急剧膨胀。以 **LlamaGen**（Sun et al., arXiv 2024）为代表的基线方法在固定长度的一维令牌序列上执行全局自注意力，其计算复杂度为 $O(T^2)$，使得高分辨率生成在训练和推理阶段都面临严重的资源约束。

### 现有方法的局限性

针对上述瓶颈，现有工作主要沿两条路径展开：

1. **高效注意力机制**：通过稀疏注意力、线性注意力或分块注意力降低单层计算量，但未从根本上减少序列长度，内存占用仍与 $T$ 成正比。
2. **固定长度补丁化**：将连续令牌按固定步长合并为补丁，以压缩序列长度。然而，图像不同区域的信息密度差异显著——平滑背景区域仅需少量令牌即可描述，而纹理丰富的物体边界则需要细粒度令牌保留细节。固定补丁化无法适应这种空间异质性，导致信息密集区域细节丢失或信息稀疏区域计算冗余。

### 核心动机：信息内容驱动的自适应压缩

DPAR 的核心洞察在于：**下一令牌预测熵（next-token prediction entropy）能够有效衡量图像区域的信息量**。如图 Figure 2 所示，高熵区域对应物体边界和纹理细节，低熵区域对应平滑背景。这一信号天然适合作为自适应令牌合并的指导准则——在高信息区域保持原有令牌粒度，在低信息区域将多个令牌合并为更大补丁。

基于此，DPAR 提出了一种**动态补丁化（Dynamic Patchification）**策略：通过轻量级无条件熵模型实时计算每个位置的下一令牌预测熵，据此将固定长度令牌序列动态聚合为可变长度补丁序列。补丁级 Transformer 仅在压缩后的 $M$ 个补丁（$M < T$）上执行自注意力，从而在保持生成质量的同时显著降低计算成本。该方法对标准解码器架构的修改极小，确保了与现有多模态生成框架的兼容性。

## 核心方法与创新机理

DPAR 的核心创新在于将**下一令牌预测熵**作为信息量的代理信号，驱动自回归图像生成中的**动态令牌聚合**，从而在保持生成质量的前提下大幅降低序列长度与计算开销。其设计围绕四个关键“变更槽”（changed slots）展开，每个槽位相对于基线 **LlamaGen**（Sun et al., arXiv 2024）的固定长度令牌序列生成范式进行了针对性重构。

### 序列表示：从固定令牌到可变补丁

基线方法将图像经 VQ-VAE 分词后展平为固定长度的一维令牌序列 $T$，该长度随分辨率呈二次增长，导致注意力计算开销急剧膨胀。DPAR 将这一固定序列替换为**可变长度的一维补丁序列** $M$（$M < T$），每个补丁是连续令牌的跨度。补丁的边界由轻量级熵模型预测的下一令牌预测熵决定：低熵区域（如背景、平滑纹理）的令牌被合并为更大的补丁，高熵区域（如物体边界、细节丰富处）则保持较短的补丁长度。这一机制使得序列长度不再由分辨率固定，而是由图像的信息内容自适应决定——在 ImageNet 256×256 上令牌数量降低 1.81 倍，在 384×384 上降低 2.06 倍。

### 注意力计算域：从全令牌自注意力到补丁级自注意力

基线 LlamaGen 的 Transformer 解码器在全部 $T$ 个令牌上执行因果自注意力，其计算复杂度为 $O(T^2)$。DPAR 将注意力计算域从令牌级提升至补丁级：**补丁 Transformer** 仅在 $M$ 个补丁表示上执行自注意力，而令牌与补丁之间的信息交换通过**补丁编码器**和**补丁解码器**中的交叉注意力完成。补丁编码器以补丁表示为查询、以补丁内令牌为键/值，将令牌信息聚合为单个补丁表示；补丁解码器则通过复制、归一化和线性投影将补丁表示映射回原始令牌。这一“聚合-生成-分解”的流程使自注意力的计算瓶颈从 $O(T^2)$ 降至 $O(M^2)$，是训练 FLOPs 降低 40% 的直接原因。

### 位置编码：从 2D RoPE 到 Dynamic RoPE

基线使用标准 2D RoPE 编码每个令牌的 $(x, y)$ 坐标。由于补丁的跨度可变，简单的 2D 坐标无法描述补丁的空间范围。DPAR 提出 **Dynamic RoPE**，在标准 2D RoPE 的基础上扩展维度，编码每个补丁的起始 $y$ 坐标 $y_{s_m}$ 和结束 $y$ 坐标 $y_{e_m}$，并包含冗余的 $y_s$ 维度以增强表示能力。消融实验表明，含冗余的 Dynamic Embedding 取得 FID 3.31，优于普通 2D Embedding（3.32）和无冗余版本（3.42），验证了可变长度补丁对专用位置编码的需求。

### 辅助模块：熵模型与编解码器的引入

基线仅包含一个解码器 Transformer。DPAR 引入了三个轻量级辅助模块：**(1) 熵模型**，一个无条件自回归模型，独立计算每个令牌的下一令牌预测熵，作为信息量的无监督度量；**(2) 补丁编码器**，将同一补丁内的令牌聚合为补丁表示；**(3) 补丁解码器**，将生成的补丁表示恢复为令牌序列。值得注意的是，DPAR 保持与同量级 LlamaGen 模型**相同的总层数**，仅将部分令牌级层替换为补丁级层（如编码器-解码器采用浅编码器、深解码器 E1D4 配置），确保公平比较的同时实现了架构的最小侵入性修改。

### 因果机制总结

核心因果链条可概括为：**下一令牌预测熵 → 动态补丁边界 → 可变长度序列 → 补丁级注意力 → 计算开销降低**。熵作为信息量的可靠准则（Figure 2 直观展示了熵图与补丁边界的一致性），使得模型能够在低信息区域“粗读”、高信息区域“精读”，从而在 FID 提升最高 27.1% 的同时将训练 FLOPs 降低 40%。消融实验进一步证实，同时启用熵门控、最大补丁长度限制和行边界重置三种策略时 FID 最优（3.32），且 DPAR 学到的表示对推理时的补丁长度变化具有鲁棒性（FID 在 3.31–3.39 之间稳定），而静态固定长度补丁模型在相同变化下 FID 从 3.58 崩溃至 25.59。

DPAR 的整体管线围绕“先度量信息，再动态聚合，最后在压缩空间自回归”这一思路展开。其核心目标是在保持生成质量的前提下，大幅降低自回归图像生成中因令牌数量二次增长带来的计算与内存开销。

### 问题根源与解决思路

传统解码器仅自回归图像生成（如 **LlamaGen**，Sun et al., arXiv 2024）将图像经 VQ‑VAE 分词为一维令牌序列 $x_0, x_1, \dots, x_{T-1}$，并通过自回归似然建模：

$$P ( I _ { \mathrm { t o k } } \mid C ) = \prod _ { t = 0 } ^ { T - 1 } P _ { \theta } ( x _ { t } \mid C , x _ { < t } )$$

其中 $T$ 随图像分辨率平方增长，导致 Transformer 自注意力的计算量与内存占用急剧膨胀。DPAR 的因果调节变量是**下一令牌预测熵**：图像中低信息区域（如背景、均匀纹理）的下一令牌预测熵低，可以被合并为更大的补丁；高信息区域（如物体边界、细节纹理）的熵高，则保留较细粒度的令牌。基于此，DPAR 将固定长度的令牌序列 $T$ 转换为可变长度的补丁序列 $M$（$M < T$），后续的自回归生成仅在 $M$ 个补丁上进行，从而从根本上降低了计算规模。

### 模块组成与数据流

DPAR 由四个主要模块串联构成，数据流严格遵循“令牌 → 补丁 → 补丁级自回归 → 令牌”的闭环。

1. **熵模型 (Entropy Model)**  
   一个轻量级的无条件自回归模型 $\mathcal{E}_\phi$，以光栅顺序逐令牌计算下一令牌预测熵：
   $$e_i = \mathrm{ENTROPY}(\boldsymbol{x}_{<i}, \mathcal{E}_\phi) = -\sum_{c=0}^{V-1} \mathcal{E}_\phi(x_i=c \mid \boldsymbol{x}_{<i}) \log \mathcal{E}_\phi(x_i=c \mid \boldsymbol{x}_{<i})$$
   熵值 $e_i$ 直接作为令牌 $x_i$ 所在位置信息含量的度量。熵模型仅用于提供补丁化准则，不参与主生成模型的梯度反传。

2. **补丁编码器 (Patch Encoder)**  
   接收完整的令牌序列，根据熵模型给出的补丁边界，将同一补丁内的连续令牌通过因果自注意力与交叉注意力聚合成单个补丁表示。具体而言，每个编码器块首先在令牌间执行因果自注意力（带 2D RoPE），再以补丁表示为 Query、令牌为 Key/Value 进行交叉注意力，最终输出固定维度的补丁特征序列。

3. **补丁 Transformer (Patch Transformer)**  
   一个仅解码器模型，在可变长度的补丁序列上执行自回归生成。其架构遵循 LLaMA 设计，但引入了 **Dynamic RoPE** 位置编码，以编码每个补丁的起始与结束 y 坐标（并包含冗余维度以增强表示）：
   $$\mathrm{P}_{(x, y_s, y_e)} = [\mathrm{P}_x, \mathrm{P}_{y_s}, \mathrm{P}_{y_e}, \mathrm{P}_{y_s}]$$
   这一步是计算节省的关键所在——注意力仅在 $M$ 个补丁上进行，而非 $T$ 个令牌。

4. **补丁解码器 (Patch Decoder)**  
   将补丁 Transformer 生成的补丁表示映射回原始令牌空间。每个解码器块首先将补丁表示复制到其包含的所有令牌位置，经归一化与线性投影后与令牌残差相加，再执行令牌间的因果自注意力，最终输出恢复后的令牌序列用于下一令牌预测。

### 训练与推理流程

训练时，DPAR 遵循 Algorithm 1 的流程：对每张图像，先由熵模型计算所有令牌的下一令牌预测熵并确定补丁边界；补丁编码器将令牌聚合为补丁；补丁 Transformer 在补丁上执行自回归生成；补丁解码器将补丁表示还原为令牌；最终以标准的交叉熵损失优化：
$$\mathcal { L } _ { C E } = - \sum _ { t = 0 } ^ { T - 1 } \log \hat { p } _ { t } ( x _ { t } )$$

推理时，熵模型同样先确定补丁边界，随后补丁 Transformer 以自回归方式逐补丁生成，补丁解码器实时将生成的补丁展开为令牌。DPAR 对标准解码器架构的修改极小，仅增加了轻量的编码器/解码器模块，确保了与现有多模态生成框架的兼容性。

### 补充图表

![[assets/figures/papers/paper_list_l861_https_arxiv_org_abs_2512_21867/figures/003_Figure_3.jpg]]
*Figure 3: Overview of DPAR. (a) Conventional AR image generation employs decoder-only transformers operating on a fixed number of tokens per image, where the token count increases quadratically with image resolution. (b) DPAR dynamically aggregates image tokens based on information content, generating a variable number of patches per image. Decoder-only transformers then operate on a smaller number of patches, reducing computational and memory overhead. DPAR makes minimal modifications to the standard decoder architecture, ensuring compatibility with multimodal generation frameworks*

### 3.1 问题形式化

标准自回归图像生成将图像通过 VQ‑VAE 编码为离散令牌序列 $I_{\mathrm{tok}} = (x_0, x_1, \dots, x_{T-1})$，在给定条件 $C$（如类别标签）下最大化似然：

$$
P ( I _ { \mathrm { t o k } } \mid C ) = \prod _ { t = 0 } ^ { T - 1 } P _ { \theta } ( x _ { t } \mid C , x _ { < t } )
$$

训练时最小化交叉熵损失：

$$
\mathcal { L } _ { C E } = - \sum _ { t = 0 } ^ { T - 1 } \log \hat { p } _ { t } ( x _ { t } )
$$

其中 $\hat{p}_t$ 为模型对位置 $t$ 的预测分布。该范式的核心瓶颈在于：令牌数量 $T$ 随分辨率平方增长，导致 Transformer 自注意力的计算与内存开销急剧膨胀。

### 3.2 DPAR 核心模块

DPAR 在标准解码器仅架构中插入四个轻量模块，将固定长度令牌序列转换为可变长度补丁序列进行生成。

#### 3.2.1 熵模型与动态补丁化

**熵模型** 是一个轻量级无条件自回归 Transformer $\mathcal{E}_\phi$，独立于主生成模型训练。对于位置 $i$，它基于前序令牌 $\boldsymbol{x}_{<i}$ 计算下一令牌预测分布，并输出其熵作为信息含量的度量：

$$
e_i = \mathrm{ENTROPY}(\boldsymbol{x}_{<i}, \mathcal{E}_\phi) = -\sum_{c=0}^{V-1} \mathcal{E}_\phi(x_i=c \mid \boldsymbol{x}_{<i}) \log \mathcal{E}_\phi(x_i=c \mid \boldsymbol{x}_{<i})
$$

其中 $V$ 为码本大小。高熵区域对应高信息内容（如物体边界、纹理细节），低熵区域对应低信息内容（如平滑背景）。

**动态补丁化** 将一维令牌序列按光栅扫描顺序划分为可变长度补丁。划分遵循三条规则：
1. **熵门控**：当累积熵超过阈值 $E_{Th}$ 时触发补丁边界；
2. **最大补丁长度约束** $P_{max}$：防止单个补丁过长导致信息过度压缩；
3. **行边界重置**：在每行结束时强制重置补丁，保持二维空间一致性。

最终得到 $M$ 个补丁（$M < T$），每个补丁 $P_m$ 包含连续令牌索引的跨度。

#### 3.2.2 补丁编码器

补丁编码器将同一补丁内的令牌聚合成单个补丁表示。每个编码器块依次执行：
1. **令牌因果自注意力**（带 2D RoPE）：捕获补丁内令牌间的依赖；
2. **交叉注意力**：以可学习的补丁查询向量为 Query，补丁内令牌为 Key/Value，将令牌信息压缩为补丁表示。

#### 3.2.3 补丁 Transformer

补丁 Transformer 是核心生成模块，采用 LLaMA 架构，在可变长度补丁序列上执行自回归生成。关键设计是 **动态旋转位置编码（Dynamic RoPE）**，它扩展了标准 2D RoPE 以编码可变长度补丁的空间信息：

- 标准 2D RoPE 编码每个令牌的 $(x, y)$ 坐标；
- Dynamic RoPE 编码补丁的起始 $y_s$ 和结束 $y_e$ 坐标，并包含冗余维度以增强表示能力。

位置编码构造如下：

$$
\omega_i = 10000^{-4(i-1)/d}, \quad i = 1, \dots, \frac{d}{4}
$$
$$
\alpha_i = 10000^{-16(i-1)/d}, \quad i = 1, \dots, \frac{d}{16}
$$
$$
\mathrm{P}_x = [\sin(\omega_i x), \cos(\omega_i x)]_{i=1}^{d/4}
$$
$$
\mathrm{P}_{y_s} = [\sin(\alpha_i y_{s_m}), \cos(\alpha_i y_{s_m})]_{i=1}^{d/16}
$$
$$
\mathrm{P}_{y_e} = [\sin(\alpha_i y_{e_m}), \cos(\alpha_i y_{e_m})]_{i=1}^{d/16}
$$
$$
\mathrm{P}_{(x, y_s, y_e)} = [\mathrm{P}_x, \mathrm{P}_{y_s}, \mathrm{P}_{y_e}, \mathrm{P}_{y_s}]
$$

其中 $d$ 为嵌入维度，$x$ 为补丁内令牌的列坐标，$(y_{s_m}, y_{e_m})$ 为补丁 $m$ 的起始和结束行坐标。末尾 $\mathrm{P}_{y_s}$ 的重复提供了冗余信息，消融实验表明该设计将 FID 从 3.42 降至 3.31。

#### 3.2.4 补丁解码器

补丁解码器将生成的补丁表示映射回原始令牌空间。每个解码器块包含：
1. **复制与归一化投影**：将补丁表示复制到其包含的每个令牌位置，经 LayerNorm 和线性投影后与原始令牌表示相加：
   $$
   h_{x_i} = h_{x_i} + \mathrm{Linear}(\mathrm{Norm}(h_{P_m})), \quad i \in P_m
   $$
2. **令牌因果自注意力**（带 2D RoPE）：在恢复的令牌序列上进一步精炼表示。

### 3.3 架构配置

DPAR 保持与同量级 LlamaGen 相同的总层数，仅将部分令牌级层替换为补丁级层。Table 1 给出各变体的编码器层数、补丁 Transformer 层数和解码器层数。消融实验表明浅编码器（1 层）搭配深解码器（4 层）的 E1D4 配置取得最优 FID（3.32），说明将更多容量分配给解码器有利于令牌重建质量。

### 补充图表

![[assets/figures/papers/paper_list_l861_https_arxiv_org_abs_2512_21867/figures/002_Figure_2.jpg]]
*Figure 2: Images (first row) and their corresponding next-token prediction entropy maps (second row) with increasing information content. Images with lower information content produce fewer high-entropy tokens, allowing the model to merge them into larger patches for efficient AR generation. Entropy heatmaps are computed over 256 tokens for 256×256 images, with black outlines indicating the final patch boundaries*

## 实验与关键发现

### 瓶颈与调控机制回顾

自回归图像生成的核心计算瓶颈在于：解码器仅架构下，令牌数量随图像分辨率呈二次增长，导致注意力计算与内存开销急剧膨胀。DPAR 的调控旋钮是**基于下一令牌预测熵的动态令牌聚合**——利用轻量级熵模型计算每个令牌的信息含量，将低信息区域合并为更大的补丁，而高信息区域保持细粒度令牌，从而在保持生成质量的同时大幅压缩序列长度。

### 主要结果：ImageNet 类别条件生成

**Table 2** 汇总了 DPAR 在 ImageNet 256×256 基准上的核心指标。与基线 **LlamaGen**（Sun et al., arXiv 2024）相比，DPAR 在所有模型规模上均取得显著更优的 FID：

- DPAR-B 将 FID 从 5.46 降至 3.98（相对提升 27.1%）；
- DPAR-L 从 3.80 降至 2.93；DPAR-XL 从 3.39 降至 2.67。

在 384×384 分辨率（评估时缩放至 256×256）上，DPAR-384 系列同样全面超越对应 LlamaGen-384 模型：DPAR-384-B 的 FID 为 4.29（基线 6.09），DPAR-384-L 为 2.79（基线 3.07），DPAR-384-XL 为 2.60（基线 2.62）。这一趋势表明，动态补丁化带来的序列压缩效应在高分辨率场景下更为显著——Abstract 中报告令牌数量在 256×256 上降低 1.81 倍，在 384×384 上降低 2.06 倍。

**训练效率**方面，**Figure 1(b)** 和 **Table 8** 显示 DPAR-XL 在 384×384 上的训练 FLOPs 为 258.5 GFLOPs，相比 LlamaGen-XL 的 433.6 GFLOPs 降低约 40%。**Figure 4** 进一步表明，DPAR 在训练过程中收敛更快，全程保持更低的 FID 曲线。

### 消融实验：补丁化策略的因果拆解

**Table 3** 对补丁化策略进行了系统消融。同时启用三个关键设计——熵门控（entropy-gated merging）、最大补丁长度限制（$P_{\text{max}}$）和行边界重置（row-boundary resets）——可获得最优 FID 3.32。单独移除任一组件的退化幅度清晰：禁用行边界重置时 FID 升至 3.42，移除最大长度限制升至 3.38，而完全禁用熵门控（即均匀补丁化）则导致 FID 恶化至 3.58。这确立了“下一令牌预测熵”作为信息度量准则的因果必要性。

超参数搜索（**Table 4** 和 **Table 5**）给出了最优配置：熵阈值 $E_{Th}=7.8$ 且最大补丁长度 $P_{\text{max}}=4$ 时 FID 达到 3.32。阈值过低会导致过度合并、丢失细节；过高则退化为接近原始令牌序列，压缩收益消失。

![[assets/figures/papers/paper_list_l861_https_arxiv_org_abs_2512_21867/figures/009_Table_4.jpg]]
*Table 4: Ablation on entropy threshold*

![[assets/figures/papers/paper_list_l861_https_arxiv_org_abs_2512_21867/figures/011_Table_5.jpg]]
*Table 5: Ablation on maximum patch length*

**推理鲁棒性**是 DPAR 相对于静态补丁化的一项关键优势。**Table 6** 显示，在推理时调整熵阈值以改变补丁长度，DPAR-L 的 FID 仅在 3.31–3.39 之间波动，保持高度稳定；而静态固定补丁长度模型在偏离训练时的 $P_{\text{static}}=1.81$ 后，FID 从 3.58 急剧崩溃至 25.59。这表明 DPAR 学到的表示对补丁边界变化具有内在鲁棒性。

### 架构设计消融

**Table 9** 对比了位置编码方案：Dynamic Embedding（含冗余开始/结束位置）取得 FID 3.31，略优于标准 2D Embedding 的 3.32，并显著优于无冗余 Dynamic Embedding 的 3.42。冗余位置信息为补丁 Transformer 提供了更强的空间表示能力。

**Table 10** 探索了编码器-解码器深度分配：浅编码器搭配深解码器（E1D4）取得最佳 FID 3.32，表明将更多容量分配给补丁解码器（负责将压缩表示恢复为令牌级细节）比分配给编码器更有利。

### 表示质量验证

**Table 7** 的线性探测实验提供了表示质量的独立验证：在 DPAR-L 补丁 Transformer 倒数第二层特征上训练的线性分类器，其 ImageNet top-1/top-5 准确率与 LlamaGen-L 相当或略优。这证实动态补丁化并未损害所学表示的判别能力，压缩后的补丁级特征仍保留了充分的语义信息。

### 公平性说明

所有 DPAR 变体保持与同量级 LlamaGen 模型相同的总层数，仅将部分 token-level 层替换为 patch-level 层。实验使用相同的 VQ-VAE 分词器（下采样因子 16，码本大小 16384）和训练超参数（300 epochs，batch size 256，学习率 $1\times10^{-4}$）。补丁 Transformer 采用打包策略（packed implementation via xformers）以避免变长序列的填充开销，确保 FLOPs 比较的公平性。

### 待验证与开放问题

- 论文未提供在高分辨率（>1024）或多模态文本到图像场景下的实验结果，引入的补丁编码器-解码器模块对推理延迟的实际影响需要进一步量化。
- 熵模型的选择空间（更大模型、不同训练目标）是否影响补丁化质量尚未探索。
- 动态补丁化在医学影像、遥感等低信息区域分布不同的领域中的泛化性有待验证。

### 补充图表

![[assets/figures/papers/paper_list_l861_https_arxiv_org_abs_2512_21867/figures/006_Table_2.jpg]]
*Table 2: DPAR model comparisons on class-conditional ImageNet 256×256 benchmark. We report FID [14], Inception Score(IS) [47], and precision/recall [23] and the average number of sampling steps used for generation. DPAR model outperforms prior raster-order autoregressive models with similar parameter counts, achieving significantly better FID scores. Models containing ‘-384’ in their names are trained on 384 × 384 and resized to 256 × 256 for evaluation*

![[assets/figures/papers/paper_list_l861_https_arxiv_org_abs_2512_21867/figures/007_Table_3.jpg]]
*Table 3: Ablation of Patchification strategies. Entropy-based patchification with patch length constraint and row-boundary resets leads to the best FID score on ImageNet 256×256 benchmark*

![[assets/figures/papers/paper_list_l861_https_arxiv_org_abs_2512_21867/figures/008_Table_6.jpg]]
*Table 6: Adaptive Patch Length at Inference. We compare a static model trained with fixed patch length*

![[assets/figures/papers/paper_list_l861_https_arxiv_org_abs_2512_21867/figures/005_Figure_4.jpg]]
*Figure 4: Comparative analysis of converge of DPAR with LLamaGen on ImageNet-384. We plot FID vs training epochs for various model sizes. DPAR consistently achieves lower FID scores, demonstrating faster convergence and better image fidelity*

![[assets/figures/papers/paper_list_l861_https_arxiv_org_abs_2512_21867/figures/012_Table_8.jpg]]
*Table 8: Compute comparison across all LlamaGen and DPAR variants. DPAR consistently reduces FLOPs across both 256×256 and 384×384 model families*

![[assets/figures/papers/paper_list_l861_https_arxiv_org_abs_2512_21867/figures/013_Table_9.jpg]]
*Table 9: Comparison of positional embedding schemes. Dynamic Embedding achieves the best FID on ImageNet 256×256*

![[assets/figures/papers/paper_list_l861_https_arxiv_org_abs_2512_21867/figures/014_Table_10.jpg]]
*Table 10: Ablation on encoder–decoder depth*

## 定位与知识库关联

### 1. 与基线工作的关系

DPAR 直接建立在解码器仅自回归（decoder-only AR）图像生成这一范式之上，其最直接的基线是 **LlamaGen**（Sun et al., arXiv 2024）。LlamaGen 将 Llama 架构适配到图像生成，使用固定长度的二维 VQ-VAE 令牌序列，通过标准的因果自注意力进行逐令牌预测。DPAR 在以下关键维度上对这一范式进行了改造：

- **序列表示**：LlamaGen 使用固定长度的 T 个令牌的一维序列；DPAR 将其替换为可变长度的 M 个补丁序列（M < T），每个补丁是连续令牌的跨度。这一改动直接削减了自注意力计算的序列长度。
- **注意力计算域**：LlamaGen 在整个令牌序列上执行全局自注意力；DPAR 将自注意力迁移到补丁层级，同时在补丁编码器/解码器中引入交叉注意力来完成令牌与补丁之间的信息聚合与分解。
- **位置编码**：LlamaGen 使用标准的 2D RoPE 编码每个令牌的 (x, y) 坐标；DPAR 提出 Dynamic RoPE，编码补丁的起始与结束 y 坐标，并引入冗余维度以增强表示能力。
- **辅助模块**：LlamaGen 无额外辅助模型；DPAR 引入轻量级熵模型（计算下一令牌预测熵）、补丁编码器和补丁解码器三个新组件。

值得注意的是，DPAR 对标准解码器架构的修改被刻意控制在最小范围。补丁 Transformer 本身仍采用 Llama 架构，仅将部分令牌层级的层替换为补丁层级的层，总层数保持不变。这种设计确保了与现有多模态生成框架的兼容性。

### 2. 方法谱系中的位置

从方法谱系来看，DPAR 处于**动态令牌聚合**与**自回归图像生成效率优化**的交汇点。与以下方向存在关联或潜在结合空间：

- **静态补丁化/令牌合并**：如 ViT 中的补丁嵌入或 Token Merging（ToMe）等方法在推理时进行令牌合并，但通常采用固定的合并策略或基于注意力相似度的准则。DPAR 的创新在于将合并准则锚定在**下一令牌预测熵**这一信息论度量上，并在训练过程中学习动态补丁化。
- **多尺度自回归生成**：如 VAR 等工作通过多尺度预测来提升生成效率。DPAR 的动态补丁化本质上也是一种自适应尺度的策略——低信息区域对应大补丁（粗尺度），高信息区域对应小补丁（细尺度）。两者是否可以结合（例如在多尺度框架内使用熵驱动的补丁化）是一个开放问题。
- **非因果顺序生成**：随机顺序生成（如 MaskGIT）等方法通过改变生成顺序来提升效率。DPAR 目前仍遵循光栅扫描顺序，但动态补丁化框架是否可推广到其他生成顺序，值得探索。

### 3. 适用边界与局限性

基于现有证据，DPAR 的适用边界和局限可归纳如下：

- **分辨率扩展性**：DPAR 在 256×256 和 384×384 分辨率上已验证有效，令牌数量分别降低 1.81 倍和 2.06 倍。理论上，分辨率越高，低信息区域的占比越大，补丁化的收益应更显著。但在极高分辨率（>1024）下的表现尚未验证，额外引入的编码器-解码器模块对推理延迟的影响也需要评估。
- **领域泛化性**：当前实验集中在 ImageNet 自然图像上。在医学影像、遥感图像等低信息区域分布与自然图像不同的领域中，熵模型的补丁化准则是否仍然有效，尚需验证。
- **熵模型的依赖性**：补丁化的质量依赖于熵模型的预测精度。当前使用的是轻量级无条件自回归模型，更大的熵模型或不同的训练目标（如条件熵估计）是否会影响最终生成效果，文中未进行消融。
- **多模态扩展**：DPAR 声称对解码器架构的修改最小，因此与多模态框架兼容，但尚未在文本到图像等实际多模态任务上进行验证。

### 4. 开放问题

基于上述分析，以下问题值得进一步探索：

1. **与其他效率优化方法的协同**：DPAR 的动态补丁化是否可与 VAR 的多尺度预测或随机顺序生成策略结合，以在保持质量的同时进一步降低计算成本？
2. **熵模型的选择与优化**：熵模型的容量、训练目标和架构选择如何影响补丁化质量？条件熵（如类别条件或文本条件）是否比无条件熵提供更精准的信息量度量？
3. **高分辨率与实时场景**：在高分辨率（>1024）或实时生成场景下，补丁编码器/解码器的额外计算开销是否会被补丁化带来的注意力节省所抵消？需要端到端的延迟分析。
4. **跨领域迁移**：动态补丁化策略在医学影像、遥感图像、视频帧等不同数据分布下的有效性如何？是否需要领域特定的熵模型或补丁化策略调整？

## 原文 PDF

![[paperPDFs/CVPR_2026/DPAR_Dynamic_Patchification_for_Efficient_Autoregressive_Visual_Generation.pdf]]
