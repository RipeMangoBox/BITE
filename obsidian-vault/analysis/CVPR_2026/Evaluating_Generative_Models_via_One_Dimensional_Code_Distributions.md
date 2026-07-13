---
title: Evaluating Generative Models via One-Dimensional Code Distributions
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Evaluating_Generative_Models_via_One_Dimensional_Code_Distributions.pdf
project_link: null
code_link: "https://github.com/zexiJia/1d-Distance"
aliases:
- CCHDCCMMS
- EGMODCD
tags:
- CVPR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 将评估空间从连续识别特征切换到离散视觉token的统计分布，利用1D图像标记器将图像量化为紧凑的离散token序列，直接比较token的直方图和空间共现统计。
primary_logic: 现代1D图像标记器在重建目标指导下学习，保留了丰富的语义和外观信息。离散token的统计属性（如频率、共现、熵）自然反映图像的感知质量：高质量图像产生结构化、低熵的token模式，而退化图像产生随机、高熵的模式。因此，通过token空间中的非参数分布比较（CHD）和自监督质量回归（CMMS），可以实现与人类判断高度一致的评估。
claims:
- Token分布对图像退化高度敏感：随着失真程度增加，CHD单调递增（图2）。
- CHD在约1000张图像时收敛，而FID需要超过10000张，样本效率高（图5）。
- CHD和CMMS在AGIQA、HPDv2/3和VisForm基准上均取得与人类判断的最先进相关性，超越FID等传统指标（表1-3）。
- CMMS仅使用合成退化训练，无需人类标注，即达到甚至超过需要人工标注的偏好模型（表3）。
---

# Evaluating Generative Models via One-Dimensional Code Distributions

> [!tip] 核心洞察
> 现代1D图像标记器在重建目标指导下学习，保留了丰富的语义和外观信息。离散token的统计属性（如频率、共现、熵）自然反映图像的感知质量：高质量图像产生结构化、低熵的token模式，而退化图像产生随机、高熵的模式。因此，通过token空间中的非参数分布比较（CHD）和自监督质量回归（CMMS），可以实现与人类判断高度一致的评估。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于一维编码分布的生成模型评估 |
| 英文题名 | Evaluating Generative Models via One-Dimensional Code Distributions |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.08064) · [Code](https://github.com/zexiJia/1d-Distance) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | CHD（Codebook Histogram Distance）和 CMMS（Code Mixture Model Score） |
| Dataset | AGIQA, HPDv3 |

> [!tip] 效果简介
> - AGIQA 上，Spearman相关系数 ↑ / N-MSE ↓ CHD: ρ=0.829; CMMS: ρ=0.943, N-MSE=0.050 vs FID: ρ≈0.6 (图中估计); MUSIQ: ρ≈0.8; ImageReward: ρ≈0.85 (显著优于FID等传统指标，CMMS达到最高)。
> - HPDv3 上，Spearman相关系数 ↑ / Kendall ↑ / N-MSE ↓ CHD: ρ=0.867, τ=0.778, N-MSE=0.017; CMMS: ρ=0.872, τ=0.778, N-MSE=0.018 vs FID: ρ≈0.6; CLIP-FID, DINO-FID较低; Q-Align: ρ≈0.85 (在所有指标上领先，尤其N-MSE较低)。
> - 人类偏好基准 (HPDv2, AGIQA, HPDv3, VisForm) 上，成对偏好准确率 Acc ↑ CMMS: 74.9 (HPDv2), 71.5 (AGIQA), 61.3 (HPDv3), 66.7 (VisForm) vs ImageReward: ≤70; PickScore: ≤73.2; Q-Align: ≤73.2 (CMMS在所有基准上达到最高准确率)。

## 概要

**问题瓶颈**：现有生成模型评估指标（如FID、IS）依赖连续识别特征（InceptionV3、CLIP、DINO），假设特征分布为高斯，并采用全局平均池化——这导致它们对纹理、清晰度、局部伪影等外观细节不敏感，在艺术图像、医学图像等非高斯分布场景下不可靠。

**核心洞察**：现代1D图像标记器（如TiTok）在重建目标指导下学习，将图像量化为紧凑的离散token序列，同时保留了丰富的语义和外观信息。离散token的统计属性（频率、共现、熵）自然反映图像的感知质量：高质量图像产生结构化、低熵的token模式，退化图像则产生随机、高熵的模式。

**方法定位**：本文提出将评估空间从连续识别特征切换到离散视觉token的统计分布，并基于此引入两个互补指标：
- **CHD（Codebook Histogram Distance）**：无需训练，通过比较真实与生成图像token的一元频率直方图和空间共现直方图，衡量视觉词汇使用和局部结构是否匹配。
- **CMMS（Code Mixture Model Score）**：无参考质量分数，仅使用合成退化（均匀token注入、语义片段交换、像素空间增强）训练轻量Transformer，无需任何人类标注。

**主要结果**：
- CHD对图像退化高度敏感，随失真程度增加单调递增（Figure 2）。
- CHD在约1,000张图像时即收敛，而FID需要超过10,000张，样本效率提升约一个数量级（Figure 5）。
- 在AGIQA、HPDv2/3和VisForm等多个基准上，CHD和CMMS均取得与人类判断的最先进相关性，显著超越FID、CLIP-FID、CMMD等传统指标（Table 1–3）。
- CMMS仅使用合成退化训练，在人类偏好预测准确率上达到甚至超过需要人工标注的偏好模型（如ImageReward、PickScore）（Table 3）。

### 生成模型评估的核心瓶颈

现代生成模型已能合成高度逼真的图像，但如何可靠地评估其质量仍是一个未解难题。当前主流的分布度量指标——以 **FID**（Heusel et al., NeurIPS 2017）为代表——依赖连续识别特征（如 InceptionV3、CLIP、DINO），假设特征空间服从高斯分布，并采用全局平均池化聚合信息。这一范式存在两个根本性缺陷：

**外观细节的不可见性**。识别编码器在训练中最大化语义信息的保留，却系统性地丢弃了外观信息。信息论分解表明，图像 $x$ 与其特征 $\phi(x)$ 之间的互信息可拆分为语义与外观两部分：

$$I(x_s, x_a; \phi(x)) = I(x_s; \phi(x)) + I(x_a; \phi(x) \mid x_s)$$

其中 $x_s$ 为语义内容，$x_a$ 为外观属性（纹理、清晰度、局部结构）。识别任务鼓励最大化第一项，却使第二项趋近于零。根据数据处理不等式 $I(q; x) \ge I(q; \phi(x))$，任何未针对质量 $q$ 优化的编码器都必然丢失质量相关信息。这解释了为何 FID 对纹理模糊、JPEG 伪影、局部噪声等感知退化高度不敏感。

**高斯假设的脆弱性**。FID 通过拟合高斯分布并计算 Fréchet 距离来衡量真实与生成图像特征分布的差异：

$$\mathrm{FID} = \Vert \mu_r - \mu_g \Vert_2^2 + \mathrm{Tr}\Big(\Sigma_r + \Sigma_g - 2(\Sigma_r \Sigma_g)^{1/2}\Big)$$

这一参数化假设在自然图像上尚可接受，但在艺术图像、医学影像等非高斯分布域中完全失效。后续工作如 **CMMD**（Jayasumana et al., CVPR 2024）以核最大均值差异替代高斯假设：

$$\mathrm{MMD}_k^2 = \mathbb{E}_{x,x'}[k(x,x')] + \mathbb{E}_{y,y'}[k(y,y')] - 2\mathbb{E}_{x,y}[k(x,y)]$$

但核方法仍运行于连续特征空间，未能解决外观信息丢失的结构性问题。**CLIP-FID**（Kynkäänniemi et al., ICML 2022）和 **DINO-FID**（Stein et al., NeurIPS 2023）通过替换特征提取器来增强语义覆盖，但同样受限于连续空间的全局池化范式。

### 无参考质量评估的标注依赖

另一条技术路线是无参考图像质量评估（NR-IQA），直接预测图像的质量分数。代表性方法包括 **MUSIQ**（Ke et al., ICCV 2021）和 **Q-Align**（Chen et al., ICML 2024），以及偏好学习模型 **ImageReward**（Xu et al., NeurIPS 2023）和 **PickScore**（Kirstain et al., NeurIPS 2023）。这些方法虽然在特定基准上取得了与人类判断较高的相关性，但普遍依赖大规模人类标注数据进行训练，标注成本高昂且难以覆盖无限多样的生成模型和视觉域。

### 本文动机：从连续特征到离散Token统计

上述分析揭示了传统评估范式的根本矛盾：**评估空间（连续识别特征）与评估目标（感知质量）之间的错配**。本文提出一个根本性的视角转换——将评估从连续特征空间迁移到离散视觉token的统计空间。

这一转换的核心洞察在于：现代1D图像标记器（如 TiTok）在重建目标的驱动下，将图像量化为紧凑的离散token序列，其学习过程自然保留了丰富的语义和外观信息。离散token的统计属性——频率、共现模式、熵——直接反映图像的感知质量：高质量图像产生结构化、低熵的token模式，而退化图像产生随机、高熵的模式。离散编码还使联合分布分析变得可处理：给定大小为 $K$ 的码本 $\mathcal{V}$，token序列的联合分布可分解为低阶统计量的乘积，使得非参数分布比较成为可能。

基于这一范式，本文提出两个互补的评估指标：**CHD**（Codebook Histogram Distance），一种无需训练的分布度量，通过比较真实与生成图像token的一元直方图和空间共现直方图来衡量分布差异；**CMMS**（Code Mixture Model Score），一种无参考质量评分器，仅通过合成token退化训练即可达到甚至超越需要人类标注的偏好模型。两者共同构成了一个从分布评估到单张质量预测的完整评估框架，在多个基准上实现了与人类判断的最先进一致性。

## 核心方法与创新机理

### 从连续特征分布到离散Token统计：评估空间的根本切换

现有生成模型评估指标的核心瓶颈在于**评估空间**的选择。以 **FID**（Heusel et al., NeurIPS 2017）为代表的分布度量方法，操作于连续识别特征（如InceptionV3、CLIP、DINO）之上，并假设特征分布服从高斯分布。这一范式存在两个结构性缺陷：

1. **信息瓶颈**：识别编码器的训练目标是最小化语义信息损失，但同时压缩外观信息。从信息分解的角度，编码器输出的互信息可分解为 $I(x_s, x_a; \phi(x)) = I(x_s; \phi(x)) + I(x_a; \phi(x) \mid x_s)$，其中 $x_s$ 为语义信息，$x_a$ 为外观信息。识别任务天然鼓励保留 $x_s$ 而丢弃 $x_a$，因此连续特征空间对纹理、清晰度、局部伪影等外观细节**天然不敏感**。

2. **分布假设脆弱性**：高斯假设在自然图像特征上近似成立，但在艺术图像、医学图像等非高斯分布数据上失效。**CMMD**（Jayasumana et al., CVPR 2024）虽以核最大均值差异替代了高斯假设，但仍在同一受限特征空间中操作，未能从根本上解决信息丢失问题。

本工作将评估空间从连续识别特征**切换为离散视觉token的统计分布**，构成方法谱系中的根本性位移。现代1D图像标记器（如TiTok）在重建目标指导下学习，保留了丰富的语义和外观信息。离散token的统计属性——频率、共现、熵——自然反映图像的感知质量：高质量图像产生结构化、低熵的token模式，而退化图像产生随机、高熵的模式。

### Changed Slots：五个关键维度的系统性创新

相对于以FID为代表的传统评估范式，本工作在下述五个维度上进行了系统性替换：

| 维度 | 基线方案 | 本工作方案 | 核心机制 |
|------|---------|-----------|---------|
| **评估空间** | 连续识别特征（InceptionV3/CLIP/DINO） | 离散视觉token序列（TiTok，词汇量4096） | 保留外观信息，实现可分解的分布分析 |
| **分布假设** | 高斯分布（FID）或核方法（CMMD） | 非参数直方图统计（CHD） | 无需参数假设，直接比较经验分布 |
| **空间信息利用** | 全局平均池化，忽略空间结构 | 2D空间共现直方图（CHD-2D） | 保留token邻接关系，捕捉局部语法 |
| **质量评估监督** | 需要人类标注训练偏好模型 | 自监督合成退化训练（CMMS） | 零人类标注成本，泛化至任意域 |
| **距离度量** | Fréchet距离或核MMD | Hellinger距离 | 对离散直方图比较更具判别力 |

### 创新机制一：CHD——训练无关的离散分布度量

**CHD（Codebook Histogram Distance）** 将生成模型评估转化为token空间中两个经验分布的比较，由两个互补组件构成：

- **CHD-1D**（一元直方图距离）：衡量生成模型是否学会了正确的视觉词汇。计算真实图像集 $\mathcal{R}$ 与生成图像集 $\mathcal{G}$ 之间token一元频率直方图的Hellinger距离：
  $$h_{\mathcal{S}}^{(1)}(v) = \frac{1}{|\mathcal{S}| \cdot N} \sum_{I \in \mathcal{S}} \sum_{i=1}^{N} \mathbb{I}[c_i(I) = v], \quad v \in \mathcal{V}$$
  $$\mathrm{CHD-1D}(\mathcal{R}, \mathcal{G}) = \frac{1}{\sqrt{2}} \big\| \sqrt{h_{\mathcal{R}}^{(1)}} - \sqrt{h_{\mathcal{G}}^{(1)}} \big\|_2 \in [0, 1]$$

- **CHD-2D**（空间共现距离）：衡量token是否以正确的局部语法组合。计算位移 $\Delta$ 下邻接token对 $(u, v)$ 的定向共现直方图，经对称化和旋转平均后比较Hellinger距离：
  $$h_{S}^{(2)}(u, v; \Delta) = \frac{1}{Z_{S, \Delta}} \sum_{I \in \mathcal{S}} \sum_{\substack{\mathbf{p} \in \Omega_I \\ \mathbf{p}+\Delta \in \Omega_I}} \mathbb{I}[c(\mathbf{p}) = u, c(\mathbf{p}+\Delta) = v]$$

- **CHD**取两者的算术平均，提供平衡的全局与局部评价：
  $$\mathrm{CHD}(\mathcal{R}, \mathcal{G}) = \frac{1}{2}\big(\mathrm{CHD-1D}(\mathcal{R}, \mathcal{G}) + \mathrm{CHD-2D}(\mathcal{R}, \mathcal{G})\big)$$

CHD的**因果有效性**在图2中得到验证：随着失真程度增加（高斯噪声、块混洗等10级渐进退化），CHD呈现鲁棒的单调递增趋势，证明token分布对感知退化高度敏感。

### 创新机制二：CMMS——自监督Token空间质量回归

**CMMS（Code Mixture Model Score）** 解决了无参考质量评估中的人类标注依赖问题。其核心思路是：在token空间中合成退化序列，训练回归器将退化程度映射为质量分数，**全程无需人类标注**。

退化引擎包含三类操作（图3）：
1. **均匀token注入**：以概率 $p$ 将token替换为随机词汇，模拟局部伪影：
   $$\tilde{c}_i \sim \begin{cases} c_i & \text{with probability } 1-p, \\ \mathcal{U}(\mathcal{V}) & \text{with probability } p. \end{cases}$$
2. **语义片段交换**：随机交换token序列中的片段，破坏语义连贯性。
3. **像素空间增强**：对原始图像施加模糊、JPEG压缩、噪声、遮挡、光度变化后重新标记化。

质量映射采用指数衰减函数 $q(p) = \exp(-20p), \; p \in [0, 0.3]$，将腐败概率映射为质量分数。回归器为轻量Transformer编码器+MLP，仅在ImageNet-1K上训练，在所有下游基准上**零样本评估**。

### 创新三：高样本效率与收敛性

CHD的另一关键创新在于**样本效率**。如图5所示，CHD在约1,000张图像时即收敛至稳定值，而FID需要超过10,000张样本才能稳定。这一特性源于离散token空间的低维结构化特性（词汇量4096，序列长度128），使得直方图统计在小样本下即可可靠估计，大幅降低了评估成本。

本文提出了一种将生成模型评估从连续特征空间迁移到离散视觉token空间的新范式。其核心洞察在于：现代1D图像标记器在重建目标的驱动下，能够紧凑地编码语义与外观信息，而图像质量会自然地表现为token统计规律——高质量图像产生结构化、低熵的token模式，退化图像则呈现随机、高熵的分布。基于这一洞察，整个框架围绕“标记化→分布度量/质量回归”两条主线展开。

### 框架总览

整体pipeline由两个互补的评估组件构成，共享同一个离散token化前端：

1. **CHD（Codebook Histogram Distance）**：无需训练的分布度量，通过比较真实图像集与生成图像集的token直方图来评估生成质量。
2. **CMMS（Code Mixture Model Score）**：无参考质量评分器，在合成退化的token序列上自监督训练，直接输出单张图像的质量分数。

两者的输入输出流如下：

- **CHD**：输入为真实图像集 $\mathcal{R}$ 和生成图像集 $\mathcal{G}$，输出为 $[0,1]$ 范围内的标量距离，值越小表示分布越接近。
- **CMMS**：输入为单张图像的token序列，输出为该图像的质量分数，分数越高表示质量越好。

### 模块关系与数据流

整个框架包含五个核心模块，按数据流顺序为：

#### 1. 图像标记化（共享前端）

使用预训练的**TiTok** 1D图像标记器将每张 $256\times256$ 图像量化为 $N=128$ 个离散token，词汇表大小 $|\mathcal{V}|=4096$。该标记器在DataComp的1亿张图像上重新训练，以覆盖更广泛的视觉域。标记化后的token序列 $\mathbf{c} = (c_1, c_2, \dots, c_{128})$ 是后续所有分析的基础。

#### 2. CHD-1D（一元直方图距离）

计算真实图像集与生成图像集之间token一元频率的Hellinger距离，衡量模型是否学会了正确的视觉词汇使用。对于图像集 $\mathcal{S}$，其一元直方图定义为：

$$h_{\mathcal{S}}^{(1)}(v) = \frac{1}{|\mathcal{S}| \cdot N} \sum_{I \in \mathcal{S}} \sum_{i=1}^{N} \mathbb{I}[c_i(I) = v], \quad v \in \mathcal{V}$$

CHD-1D取两者直方图平方根的L2距离：

$$\mathrm{CHD\text{-}1D}(\mathcal{R}, \mathcal{G}) = \frac{1}{\sqrt{2}} \big\| \sqrt{h_{\mathcal{R}}^{(1)}} - \sqrt{h_{\mathcal{G}}^{(1)}} \big\|_2 \in [0, 1]$$

#### 3. CHD-2D（空间共现距离）

在CHD-1D的基础上引入空间结构信息，计算token空间邻接对的共现直方图Hellinger距离，衡量模型是否学会了正确的局部“语法”（token组合方式）。对位移 $\Delta$，定向共现分布为：

$$h_{\mathcal{S}}^{(2)}(u, v; \Delta) = \frac{1}{Z_{\mathcal{S},\Delta}} \sum_{I \in \mathcal{S}} \sum_{\substack{\mathbf{p} \in \Omega_I \\ \mathbf{p}+\Delta \in \Omega_I}} \mathbb{I}[c(\mathbf{p}) = u, c(\mathbf{p}+\Delta) = v]$$

通过对称化和旋转平均得到 $\bar{h}^{(2)}$，CHD-2D计算其向量化形式的Hellinger距离：

$$\mathrm{CHD\text{-}2D}(\mathcal{R}, \mathcal{G}) = \frac{1}{\sqrt{2}} \big\| \sqrt{\mathrm{vec}(\bar{h}_{\mathcal{R}}^{(2)})} - \sqrt{\mathrm{vec}(\bar{h}_{\mathcal{G}}^{(2)})} \big\|_2$$

#### 4. CHD（综合分布度量）

取CHD-1D和CHD-2D的算术平均，提供平衡的全局词汇匹配与局部结构匹配：

$$\mathrm{CHD}(\mathcal{R}, \mathcal{G}) = \frac{1}{2}\big(\mathrm{CHD\text{-}1D}(\mathcal{R}, \mathcal{G}) + \mathrm{CHD\text{-}2D}(\mathcal{R}, \mathcal{G})\big)$$

CHD完全无需训练，仅依赖预训练的标记器和非参数直方图统计。

#### 5. CMMS（自监督质量回归器）

CMMS包含退化引擎和回归器两个子模块：

- **退化引擎**（Figure 3）：对自然图像的token序列施加三类合成退化——均匀token注入（以概率 $p$ 将token替换为随机词汇，模拟局部伪影）、语义片段交换（打乱token序列的局部块）、像素空间增强（模糊、JPEG压缩、噪声、遮挡、光度变化）。
- **质量回归器**：轻量Transformer编码器+MLP，将退化后的token序列映射为质量分数。训练使用指数质量映射 $q(p) = \exp(-20p)$，其中 $p \in [0, 0.3]$ 为腐败概率。

$$\tilde{c}_i \sim \begin{cases} c_i & \text{with probability } 1-p, \\ \mathcal{U}(\mathcal{V}) & \text{with probability } p \end{cases}$$

CMMS仅在ImageNet-1K上训练，无需任何人类标注，在所有下游基准上零样本评估。

### 与传统方法的范式对比

Figure 1 概括了本框架与以FID为代表的传统方法的核心差异。传统方法（左）在连续识别特征空间操作，假设特征服从高斯分布并进行全局池化；本方法（右）则切换到离散token空间，直接比较经验token统计。这一范式转换带来了三个关键优势：

![[assets/figures/papers/paper_list_l748_https_arxiv_org_abs_2603_08064/figures/001_Figure_1.jpg]]
*Figure 1: From feature distributions to token statistics. Conventional metrics such as Frechet Inception Distance (FID) operate on ´ continuous semantic features and assume a Gaussian distribution in feature space (left), which makes them insensitive to appearance details (e.g., texture, style) and unreliable on non-Gaussian data such as artistic or medical images. Our approach (right) quantizes images into a discrete vocabulary of 1D tokens and compares empirical token statistics directly*

- **外观敏感性**：token分布对纹理、清晰度、局部伪影等外观细节高度敏感（Figure 2），而连续特征在识别任务训练中倾向于丢弃这些信息。
- **分布假设自由**：非参数直方图比较无需高斯假设，在艺术、医学等非高斯分布图像上同样可靠。
- **高样本效率**：CHD约在1,000张图像时收敛，而FID需要超过10,000张（Figure 5）。

### 整体范式转换

本文的核心创新在于将生成模型评估从**连续特征空间**迁移到**离散视觉token空间**。传统指标（如FID）在InceptionV3等识别编码器的连续特征上操作，假设特征服从高斯分布：

$$ \mathrm{FID} = \Vert \mu_r - \mu_g \Vert_2^2 + \operatorname{Tr}\Big( \Sigma_r + \Sigma_g - 2(\Sigma_r \Sigma_g)^{1/2} \Big) $$

其中 $\mu_r, \mu_g$ 和 $\Sigma_r, \Sigma_g$ 分别为真实与生成图像特征的均值向量和协方差矩阵。该框架的根本瓶颈在于：识别编码器通过训练鼓励保留语义信息而抑制外观信息，其信息分解为：

$$ I(x_s, x_a; \phi(x)) = I(x_s; \phi(x)) + I(x_a; \phi(x) \mid x_s) $$

其中 $x_s$ 为语义变量，$x_a$ 为外观变量，$\phi(x)$ 为编码特征。由于分类训练目标仅优化语义判别，条件互信息 $I(x_a; \phi(x) \mid x_s)$ 被最小化，导致特征对纹理、清晰度、局部伪影等外观细节不敏感。此外，全局平均池化丢弃了空间结构信息。

替代方案CMMD（Jayasumana et al., CVPR 2024）用核最大均值差异取代高斯假设：

$$ \mathrm{MMD}_k^2 = \mathbb{E}_{x,x'} [k(x,x')] + \mathbb{E}_{y,y'} [k(y,y')] - 2\mathbb{E}_{x,y} [k(x,y)] $$

但仍依赖连续特征，未解决外观信息丢失的根本问题。

### 模块一：图像标记化

使用预训练**TiTok编码器**将 $256 \times 256$ 图像 $I$ 量化为 $N=128$ 个离散token序列 $\mathbf{c} = (c_1, c_2, \ldots, c_N)$，词汇量 $K=4096$。TiTok通过重建目标训练，保留了丰富的语义和外观信息。为覆盖多样化视觉域，编码器在DataComp的1亿张图像上重新训练。

### 模块二：CHD-1D（一元直方图距离）

CHD-1D衡量生成模型是否学习了正确的**视觉词汇**。对图像集 $\mathcal{S}$，其一元token频率直方图定义为：

$$ h_{\mathcal{S}}^{(1)}(v) = \frac{1}{|\mathcal{S}| \cdot N} \sum_{I \in \mathcal{S}} \sum_{i=1}^{N} \mathbb{I}[c_i(I) = v], \quad v \in \mathcal{V} $$

其中 $\mathbb{I}[\cdot]$ 为指示函数，$\mathcal{V}$ 为词汇表。真实图像集 $\mathcal{R}$ 与生成图像集 $\mathcal{G}$ 之间的一元直方图Hellinger距离为：

$$ \mathrm{CHD\text{-}1D}(\mathcal{R}, \mathcal{G}) = \frac{1}{\sqrt{2}} \big\| \sqrt{h_{\mathcal{R}}^{(1)}} - \sqrt{h_{\mathcal{G}}^{(1)}} \big\|_2 \in [0, 1] $$

Hellinger距离对低频token的变化敏感，能有效捕捉罕见视觉元素的分布偏移。

### 模块三：CHD-2D（空间共现距离）

CHD-2D衡量token是否以正确的**局部语法**组合。对位移 $\Delta$，定向共现分布为：

$$ h_{\mathcal{S}}^{(2)}(u, v; \Delta) = \frac{1}{Z_{\mathcal{S}, \Delta}} \sum_{I \in \mathcal{S}} \sum_{\substack{\mathbf{p} \in \Omega_I \\ \mathbf{p}+\Delta \in \Omega_I}} \mathbb{I}[c(\mathbf{p}) = u, c(\mathbf{p}+\Delta) = v] $$

其中 $\Omega_I$ 为图像 $I$ 的token网格，$Z_{\mathcal{S}, \Delta}$ 为归一化常数。通过对称化 $h_{\mathcal{S}}^{(2)}(u,v) = h_{\mathcal{S}}^{(2)}(u,v;\Delta) + h_{\mathcal{S}}^{(2)}(v,u;-\Delta)$ 并对四个方向旋转平均得到 $\bar{h}_{\mathcal{S}}^{(2)}$，最终2D距离为：

$$ \mathrm{CHD\text{-}2D}(\mathcal{R}, \mathcal{G}) = \frac{1}{\sqrt{2}} \big\| \sqrt{\mathrm{vec}(\bar{h}_{\mathcal{R}}^{(2)})} - \sqrt{\mathrm{vec}(\bar{h}_{\mathcal{G}}^{(2)})} \big\|_2 $$

### 模块四：CHD（综合分布度量）

CHD取上述两个距离的算术平均，平衡全局词汇使用与局部结构评估：

$$ \mathrm{CHD}(\mathcal{R}, \mathcal{G}) = \frac{1}{2}\big(\mathrm{CHD\text{-}1D}(\mathcal{R}, \mathcal{G}) + \mathrm{CHD\text{-}2D}(\mathcal{R}, \mathcal{G})\big) $$

消融实验（Table 4）证实该组合优于单独使用任一组件，且Hellinger距离优于余弦距离和L1距离。

### 模块五：CMMS退化引擎与质量回归器

CMMS通过自监督合成退化训练，无需人类标注。退化引擎包含三类操作：

1. **均匀token注入**：以概率 $p$ 将token替换为随机词汇，模拟局部伪影：
   $$ \tilde{c}_i \sim \begin{cases} c_i & \text{with probability } 1-p, \\ \mathcal{U}(\mathcal{V}) & \text{with probability } p. \end{cases} $$

2. **语义片段交换**：随机交换token序列中的连续片段，破坏空间连贯性。

3. **像素空间增强**：对原始图像施加模糊、JPEG压缩、噪声、遮挡和光度变化后重新标记化。

质量分数通过指数映射从腐败概率 $p$ 转换：
$$ q(p) = \exp(-20p), \quad p \in [0, 0.3] $$

质量回归器采用轻量**Transformer编码器+MLP**架构，将退化token序列映射为标量质量分数。消融实验（Table 4）表明：(1) 以离散token作为输入显著优于像素输入；(2) 指数质量映射 $\exp(-20p)$ 为最优选择；(3) token腐败与像素增强组合训练最有效。

## 实验与关键发现

### 评估基准与实验设置

本文在四个互补的图像质量与人类偏好基准上系统验证了CHD和CMMS的有效性：**AGIQA**（多生成模型质量评估）、**HPDv2/v3**（大规模人类偏好标注）、**VisForm**（跨域生成模型评估，含210,000张图像、62个视觉域、12个生成模型）。

**实现细节**：所有分布度量（CHD、FID、CMMD等）均使用5,000张真实/生成图像进行评估。CHD采用在DataComp-100M上重新训练的TiTok编码器（256×256分辨率，128个token，词汇量4096）进行图像标记化。CMMS仅在ImageNet-1K（128万张图像）上使用合成退化训练，在所有下游基准上零样本评估，无需微调或人类标注。

### 质量评估主结果

**AGIQA基准**（Table 1）：CHD取得Spearman相关系数ρ=0.829，显著超越FID（ρ≈0.6）和MUSIQ（ρ≈0.8）等传统指标。CMMS进一步提升至ρ=0.943，N-MSE低至0.050，在所有比较方法中达到最高人类一致性。

**HPDv3基准**（Table 2）：CHD取得ρ=0.867、Kendall τ=0.778、N-MSE=0.017的三项指标全面领先。CMMS表现相当（ρ=0.872, τ=0.778, N-MSE=0.018），两者均显著优于FID、CLIP-FID、DINO-FID等基于连续特征的度量，以及Q-Align等需要人类标注的偏好模型。

**人类偏好预测**（Table 3）：CMMS在HPDv2（74.9%）、AGIQA（71.5%）、HPDv3（61.3%）和VisForm（66.7%）四个基准上均取得最高的成对偏好准确率，超越ImageReward（≤70%）、PickScore（≤73.2%）和Q-Align（≤73.2%）等需要大规模人类偏好标注训练的模型。

**跨域泛化**（Figure 4）：在VisForm的12个生成模型和21个视觉域上，CHD和CMMS与人类判断的相关性均稳定领先，验证了离散token空间评估在不同域和生成范式下的鲁棒性。

### 关键消融实验

Table 4系统消融了CHD和CMMS的设计选择：

**CHD消融**：
- **一元+2D共现组合**取得最优N-MSE（0.017），单独使用一元或2D直方图均导致性能下降，验证了两者互补：一元直方图衡量视觉词汇使用，2D共现直方图衡量局部空间语法。
- **Hellinger距离**显著优于余弦距离、L1距离和KL散度，证实了直方图概率分布比较中平方根变换的有效性。
- **标记器配置**：128 token、256px分辨率、4096词汇量为最优选择。减少token数或降低分辨率会丢失空间细节，减小词汇量则限制语义表达能力。

**CMMS消融**：
- **离散token输入**显著优于像素输入，验证了token空间对质量感知的优势。
- **指数质量映射**$q(p) = \exp(-20p)$（$p \in [0, 0.3]$）效果最佳，该映射将腐败概率非线性压缩到质量分数，使模型对轻微退化更敏感。
- **组合退化策略**（均匀token注入+语义片段交换+像素空间增强）优于任何单一退化类型，表明多层次的合成退化能更全面地覆盖真实生成伪影。

### 样本效率分析

Figure 5揭示了CHD相比FID的显著样本效率优势：CHD仅需约1,000张图像即可收敛到稳定值，而FID需要超过10,000张样本。这一差异源于离散token直方图估计的低维特性——词汇量4096的一元直方图仅需少量样本即可准确估计，而连续高维特征空间的高斯拟合需要大量样本才能稳定。

### 退化敏感性验证

Figure 2通过10级渐进失真实验（高斯噪声、块混洗等）定量验证了token分布对图像退化的敏感性：随着失真程度增加，CHD单调递增，且对不同失真类型均保持一致的响应模式。中间面板显示，仅少量“感知敏感token”的分布偏移即可有效捕获退化信号，解释了为何低维离散统计能高效反映感知质量变化。

![[assets/figures/papers/paper_list_l748_https_arxiv_org_abs_2603_08064/figures/002_Figure_2.jpg]]
*Figure 2: Sensitivity of Token Distributions to Image Degradation. To demonstrate how our discrete token space captures perceptual degradations, we apply 10 levels of progressive distortion to a set of 1,000 images and analyze the resulting shifts in their token distributions. As the severity of distortions like Gaussian noise or block shuffling increases (left), a small subset of perceptually-sensitive tokens exhibits consistent and predictable shifts in their distribution (middle). Our Codebook Histogram Distance (CHD) effectively aggregates these subtle changes, showing a robust, monotonic increase with the degradation level across all distortion types (right)*

![[assets/figures/papers/paper_list_l748_https_arxiv_org_abs_2603_08064/figures/004_Table_1.jpg]]
*Table 1: Evaluation of different generative models on AGIQA [35]*

![[assets/figures/papers/paper_list_l748_https_arxiv_org_abs_2603_08064/figures/005_Table_2.jpg]]
*Table 2: Evaluation of different generative models on HPDv3 [18]*

![[assets/figures/papers/paper_list_l748_https_arxiv_org_abs_2603_08064/figures/008_Table_3.jpg]]
*Table 3: Preference prediction on human preference benchmarks*

![[assets/figures/papers/paper_list_l748_https_arxiv_org_abs_2603_08064/figures/009_Table_4.jpg]]
*Table 4: Ablation study of CHD (N-MSE↓) and CMMS (Acc↑)*

## 定位与知识库关联

### 从连续特征到离散Token：评估范式的根本转换

本文的核心贡献在于将生成模型评估的“语言”从连续识别特征切换为离散视觉token统计，这一转换直接回应了现有分布度量方法的结构性缺陷。传统评估指标——从 **FID**（Heusel et al., NeurIPS 2017）到 **CLIP-FID**（Kynkäänniemi et al., ICML 2022）和 **DINO-FID**（Stein et al., NeurIPS 2023）——共享一个隐含假设：特征空间中的分布是高斯或近似高斯的，可通过均值和协方差充分刻画。这一假设在自然图像的主流生成任务中近似成立，但在艺术图像、医学图像等非高斯分布场景下系统性失效。

更深层的问题在于信息瓶颈。识别编码器（如InceptionV3、CLIP、DINO）的训练目标鼓励保留语义信息 $I(x_s; \phi(x))$ 而抑制外观信息 $I(x_a; \phi(x) \mid x_s)$。根据数据处理不等式 $I(q; x) \ge I(q; \phi(x))$，未针对质量优化的编码器必然丢失与感知质量相关的信息。此外，全局平均池化操作进一步丢弃了空间结构，使得这些指标对纹理模糊、局部伪影、清晰度退化等外观细节不敏感。

**CMMD**（Jayasumana et al., CVPR 2024）通过核最大均值差异 $\mathrm{MMD}_k^2$ 替代了FID的高斯假设，但仍依赖连续特征空间，未解决信息丢失的根本问题。本文的CHD通过将评估空间迁移到离散token统计，从根本上绕过了这些限制：离散词汇表允许对联合分布进行因子化 $p(\mathbf{c}) = \prod_{i=1}^N p(c_i \mid c_{<i})$，使得分布分析在计算上可行，且token统计天然保留外观信息。

### 与人类偏好模型的互补与超越

在无参考质量评估维度上，CMMS与现有基于人类偏好的模型形成了有趣的对比。**ImageReward**（Xu et al., NeurIPS 2023）、**PickScore**（Kirstain et al., NeurIPS 2023）和 **Q-Align**（Chen et al., ICML 2024）均依赖大规模人类标注数据训练偏好或质量回归模型。这些方法在标注覆盖的领域内表现良好，但标注成本高、覆盖范围有限。

CMMS的核心创新在于完全自监督的训练范式：仅在ImageNet-1K上使用合成退化训练，无需任何人类标注，在所有下游基准（AGIQA、HPDv2、HPDv3、VisForm）上零样本评估。Table 3显示CMMS在成对偏好预测准确率上超越了所有需要人类标注的偏好模型——在HPDv2上达到74.9%，在AGIQA上达到71.5%，在VisForm上达到66.7%。这一结果具有方法论意义：它表明token空间的统计规律足以编码人类感知质量判断，无需显式学习偏好。

**MUSIQ**（Ke et al., ICCV 2021）和 **DeQA**（Wu et al., CVPR 2025）代表了另一条技术路线——通过多尺度特征或分解式质量评估来处理无参考质量评估。CMMS与之不同之处在于，它不依赖像素空间的复杂特征工程，而是直接在离散token序列上操作，使用轻量Transformer-MLP回归器，训练和推理效率更高。

### 适用边界与局限

**领域覆盖的依赖**：CHD和CMMS的性能依赖于1D标记器（TiTok）的领域覆盖能力。本文通过在DataComp的1亿张图像上重新训练TiTok编码器来缓解这一问题，但对于与训练数据分布差异极大的特定领域（如医学影像中的罕见模态），token词汇表可能无法充分表达关键视觉特征。这一点在论文中未进行系统消融，需要手动验证。

**高阶统计量的缺失**：当前CHD-2D仅利用邻接token对的共现统计，相当于二阶马尔可夫依赖。论文在开放问题中明确指出，“如何利用更高阶的token统计量进一步改善空间建模”是值得探索的方向。这意味着对于需要长程空间一致性判断的场景（如全局结构扭曲），当前方法可能不够敏感。

**视频与3D扩展**：论文将“基于token的评估框架扩展到视频和3D生成任务”列为开放问题。这并非当前方法的缺陷，而是明确的能力边界。视频的时间维度、3D的多视角一致性都会引入新的统计依赖结构，需要相应的高阶token交互建模。

**CMMS的退化假设**：CMMS的合成退化引擎覆盖了均匀token注入、语义片段交换和像素空间增强（模糊、JPEG、噪声、遮挡、光度变化），但这些退化类型的组合未必能穷举所有真实世界的质量退化模式。对于与训练退化分布差异较大的质量缺陷类型，CMMS的泛化能力需要进一步验证。

### 知识库定位

本文在生成模型评估的知识体系中处于“范式转换”的位置。它将评估从“特征工程”问题重新定义为“统计建模”问题，其核心洞见——现代1D图像标记器在重建目标指导下学习，保留了丰富的语义和外观信息——连接了生成模型评估与离散表示学习两个领域。

从技术谱系看，CHD继承了分布度量的传统（FID → CMMD → CHD），但通过离散化实现了非参数统计比较；CMMS继承了无参考质量评估的传统（MUSIQ → Q-Align → CMMS），但通过自监督退化训练摆脱了对人类标注的依赖。两者的组合提供了一个完整的评估框架：CHD用于分布层面的模型比较，CMMS用于实例层面的质量评分。

在样本效率方面，Figure 5显示CHD在约1000张图像时收敛，而FID需要超过10000张。这一优势使得CHD特别适合计算资源受限或生成成本高的场景，如高分辨率图像生成或扩散模型的快速迭代评估。

## 原文 PDF

![[paperPDFs/CVPR_2026/Evaluating_Generative_Models_via_One_Dimensional_Code_Distributions.pdf]]
