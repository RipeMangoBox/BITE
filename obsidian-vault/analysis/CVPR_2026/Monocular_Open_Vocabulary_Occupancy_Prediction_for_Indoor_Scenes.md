---
title: Monocular Open Vocabulary Occupancy Prediction for Indoor Scenes
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Monocular_Open_Vocabulary_Occupancy_Prediction_for_Indoor_Scenes.pdf
project_link: null
code_link: "https://github.com/JuIvyy/LegoOcc"
aliases:
- MOVOPIS
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 将每个高斯体元的有效不透明度（α_i p_i(x)）视为泊松过程的事件强度，并将体素占用建模为“至少发生一次事件”的概率（1-exp(-Σ α_i p_i)），使得占用聚合与图像渲染的不透明度一致且稳定；同时通过训练过程中渐进衰减sigmoid温度（Progressive Temperature Decay），逐步锐化不透明度，减少渲染时沿光线的特征混合，...
primary_logic: 利用泊松过程重新形式化高斯到占用的聚合规则，避免了Bernoulli聚合在多个高斯重叠时迅速饱和导致的不透明度退化问题，并且与渲染所用的不透明度自然衔接；同时，以指数温度衰减取代离散Top-k选取，既能持续提供梯度，又能渐进提升特征渲染的判别性，最终在无需语义标注的情况下实现有效的开放词汇3D占用预测。
claims:
- 泊松聚合（Poisson G2O）在闭集和开放词汇设置下均取得最高IoU和mIoU，显著优于Bernoulli和GaussianFormer2。
- Progressive Temperature Decay（指数衰减，T_min=1e-3）使得mIoU从基线的大幅提升至21.05。
- 在Occ-ScanNet开放词汇设定中，LegoOcc的mIoU达到21.05，超越此前最好的开放词汇方法（LOcc 9.25）超过2倍。
- Occ-ScanNet (开放词汇) 上 mIoU = 21.05
---

# Monocular Open Vocabulary Occupancy Prediction for Indoor Scenes

> [!tip] 核心洞察
> 利用泊松过程重新形式化高斯到占用的聚合规则，避免了Bernoulli聚合在多个高斯重叠时迅速饱和导致的不透明度退化问题，并且与渲染所用的不透明度自然衔接；同时，以指数温度衰减取代离散Top-k选取，既能持续提供梯度，又能渐进提升特征渲染的判别性，最终在无需语义标注的情况下实现有效的开放词汇3D占用预测。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向室内场景的单目开放词汇占用预测 |
| 英文题名 | Monocular Open Vocabulary Occupancy Prediction for Indoor Scenes |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2602.22667) · [Code](https://github.com/JuIvyy/LegoOcc) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | LegoOcc |
| Dataset | Occ-ScanNet |

> [!tip] 效果简介
> - Occ-ScanNet (开放词汇) 上，mIoU 21.05 vs POP-3D (5.96) (+15.09)；mIoU 21.05 vs LOcc (9.25) (+11.80)；IoU 59.50 vs POP-3D (35.32) (+24.18)。

## 概述

### 1. 问题与瓶颈

现有开放词汇占用预测方法主要面向室外驾驶场景，直接迁移至室内环境时面临双重挑战：室内几何结构更密集、布局更复杂，而语义类别更细粒度。更关键的是，在仅有二进制占用标签（occupied vs. free）的弱监督条件下，同时学习几何与语义十分困难。具体表现为两个瓶颈：

- **高斯到占用的映射不稳定**：现有基于Bernoulli的聚合规则在多个高斯重叠时迅速饱和，导致不透明度退化，无法可靠地将高斯几何转换为体素占用。
- **渲染特征混合破坏语言对齐**：多类别高斯沿光线重叠时，渲染特征产生混合，削弱了体素嵌入与自然语言之间的对齐质量。

### 2. 核心方法

针对上述瓶颈，LegoOcc提出两条因果性改进：

- **泊松高斯到占用算子（Poisson G2O）**：将每个高斯体元的有效不透明度 $\alpha_i p_i(\mathbf{x})$ 视为泊松过程的事件强度，体素占用建模为“至少发生一次事件”的概率 $p(\mathbf{x}) = 1 - \exp(-\sum \alpha_i p_i(\mathbf{x}))$。该形式化避免了Bernoulli聚合的饱和退化，且与渲染所用不透明度自然衔接。
- **渐进式温度衰减（Progressive Temperature Decay）**：训练过程中以指数调度 $\tau(r) = \max\{T_{\min}, T_{\max}(T_{\min}/T_{\max})^r\}$ 逐步降低sigmoid温度，锐化不透明度，减少渲染时的特征混合，从而增强高斯体元的语言对齐能力。

整个框架以**语言嵌入高斯（Language-Embedded Gaussians）**为统一中间表示，仅依赖二进制占用标签和训练无关的开放词汇分割器（Trident）提供的2D特征对齐监督，无需任何语义体素标注。

### 3. 方法谱系与知识库定位

LegoOcc处于**单目3D占用预测**与**开放词汇3D场景理解**的交叉点，其方法谱系可定位如下：

- **闭集占用预测**：继承自ISO（Yu et al., ECCV 2024）等基于体素的有监督方法，以及EmbodiedOcc（Wu et al., arXiv 2024）等基于高斯的占用表示，但LegoOcc将监督信号从语义体素标签缩减为二进制占用标签。
- **开放词汇占用预测**：在POP-3D（Vobecký et al., NeurIPS 2023）和LOcc（Yu et al., ICCV 2025）的基础上，LegoOcc用泊松聚合替代了原有的GaussianFormer2概率叠加或Bernoulli聚合，并以指数温度衰减取代了Dr. Splat的离散Top-k选取，从而在无需语义标注的条件下实现有效的开放词汇3D占用。
- **知识库贡献**：提供了“泊松过程形式化高斯到占用聚合”和“渐进温度衰减锐化渲染不透明度”两个可迁移的技术组件，前者解决了弱几何监督下的不透明度建模稳定性问题，后者为高斯泼溅渲染中的特征判别性提供了连续梯度优化方案。

### 4. 主要结果

在Occ-ScanNet开放词汇设定中，LegoOcc取得**59.50 IoU**和**21.05 mIoU**，相较此前最好的开放词汇方法LOcc（9.25 mIoU）提升超过2倍（+11.80 mIoU），相较POP-3D（5.96 mIoU）提升逾3倍。消融实验证实：泊松G2O贡献了IoU从52.65到59.50、mIoU从17.80到21.05的提升；指数温度衰减（$T_{\min}=10^{-3}$）使mIoU达到最优。所有开放词汇基线均采用相同的深度估计主干（DepthAnythingv2）、输入分辨率和训练配方重新实现，确保公平比较。

### 5. 局限与开放问题

尽管几何占用预测已接近闭集方法水平，开放词汇语义准确度仍有较大差距（21.05 vs. 45.15 mIoU）。温度调度超参数可能需针对不同数据集调整，低温区训练存在数值不稳定性风险。此外，泊松G2O算子向室外场景的泛化性、对更强开放词汇分割器的兼容性，以及语言嵌入在下游具身任务中的直接可用性，均为待探索的开放问题。

## 背景与动机

### 室内开放词汇占用预测的需求

3D 语义占用预测是具身智能与场景理解的核心任务，它要求模型不仅重建三维几何结构，还要为每个体素赋予语义标签。然而，现有方法大多采用闭集范式——训练时预先定义固定的语义类别集合，推理时只能识别这些已知类别。这一限制在真实室内环境中尤为突出：家庭、办公室等场景包含大量细粒度物体（如“咖啡机”“乐高积木”“盆栽”），闭集模型无法泛化到训练时未见过的物体类别，严重制约了机器人在开放世界中的部署能力。

开放词汇占用预测旨在打破这一封闭假设，使模型能够通过自然语言查询任意类别的三维占用分布。但该任务面临双重挑战：既要保证几何重建的精度，又要实现体素级语言对齐，而室内场景的密集几何结构、复杂布局和细粒度语义使得这一目标更加困难。

### 现有方法的瓶颈

当前开放词汇占用预测方法主要存在以下结构性缺陷：

**1. 室外场景的路径依赖。** 主流开放词汇占用工作（如 **POP-3D** (Vobecký et al., NeurIPS 2023)）针对自动驾驶场景设计，依赖 LiDAR 点云生成的伪占用标签进行几何监督。当迁移到室内场景时，由于缺乏 LiDAR 数据且室内几何结构更为密集，这些方法在几何精度和语义对齐上均出现严重退化。

**2. 高斯到占用的聚合不稳定。** 基于 3D Gaussian Splatting 的占用预测方法需要将高斯体元的几何参数映射为体素占用概率。现有聚合规则存在根本性问题：GaussianFormer2 的概率叠加忽略了不透明度建模，导致占用估计与渲染过程不一致；而 Bernoulli 聚合虽然引入有效不透明度 $\alpha_i p_i(\mathbf{x})$，但在多个高斯重叠时迅速饱和，使得体素占用概率趋近于 1，丧失了区分不同占用密度的能力。这种不稳定性在仅依赖二进制占用标签的弱监督条件下被进一步放大。

**3. 渲染特征混合破坏语言对齐。** 在将高斯体元的语言嵌入特征渲染到图像平面时，标准 alpha 混合会沿光线累积多个类别的特征。当多个语义类别的高斯重叠时，渲染出的像素特征成为不同类别语言嵌入的混合体，导致与真实像素特征的语言对齐被破坏。现有方法（如 Dr. Splat）通过离散 Top-k 选择来锐化不透明度，但这种方式切断了梯度传播，使模型难以端到端优化。

**4. 对语义标注的强依赖。** 闭集占用预测方法需要密集的体素级语义标注，而室内场景的语义标注成本极高。开放词汇方法 **LOcc** (Yu et al., ICCV 2025) 虽然尝试利用语言模型驱动开放词汇学习，但其几何监督仍依赖 LiDAR 伪标签，且语义对齐机制在室内场景中的有效性有限——在 Occ-ScanNet 开放词汇设定中，LOcc 的 mIoU 仅为 9.25，远低于闭集方法的 45.15。

### 本文动机与核心思路

针对上述瓶颈，**LegoOcc** 提出了一种全新的单目开放词汇占用预测框架，其核心设计原则是：**仅使用二进制占用标签（occupied vs. free）作为几何监督，无需任何体素级语义标注**。这一设计使得框架可以直接利用现有的室内占用数据集（如 Occ-ScanNet），无需额外的语义标注成本。

LegoOcc 的关键洞察在于：将 3D Language-Embedded Gaussians 作为统一的中间表示，同时支撑几何学习和语义学习两条路径。在几何侧，通过**基于泊松过程的占用聚合算子**（Poisson G2O），将每个高斯体元的有效不透明度 $\alpha_i p_i(\mathbf{x})$ 视为非齐次泊松过程的事件强度，体素占用概率建模为“至少发生一次事件”的概率：

$$p(\mathbf{x}) = 1 - \exp\!\left(-\sum_{i=1}^{N} \alpha_i p_i(\mathbf{x})\right)$$

这一形式化避免了 Bernoulli 聚合的饱和问题，且与渲染所用的不透明度自然衔接。在语义侧，通过**渐进式温度衰减**（Progressive Temperature Decay）逐步锐化不透明度 sigmoid 的温度参数 $\tau$，从高温度平滑训练过渡到低温度判别推理，减少渲染过程中的特征混合，从而增强语言对齐质量。

在 Occ-ScanNet 开放词汇设定中，LegoOcc 以 59.50 IoU 和 21.05 mIoU 显著超越此前最佳开放词汇方法（LOcc 的 9.25 mIoU），提升超过 2 倍，验证了该框架在弱监督条件下同时学习几何与开放词汇语义的有效性。

## 核心创新

LegoOcc 的核心创新在于，它通过两个相互耦合的机制，解决了在仅有二进制占用标签的弱监督条件下，同时学习密集室内场景的几何结构与开放词汇语义这一瓶颈问题。

### 创新一：基于泊松过程的高斯到占用聚合（Poisson G2O）

**问题根因**：现有的高斯到占用（Gaussian-to-Occupancy, G2O）映射方法存在不稳定性。例如，基于 Bernoulli 聚合的公式 $p(\mathbf{x}) = 1 - \prod_{i=1}^{N} (1 - \alpha_i p_i(\mathbf{x}))$ 在多个高斯重叠时，其有效不透明度会迅速饱和，导致梯度回传受阻，并且会迫使网络学习到极小的不透明度值（$\alpha_i$）来避免过饱和。这进一步拉大了渲染特征与逐高斯嵌入之间的差距，破坏了语言对齐。

**核心机制**：LegoOcc 将每个高斯体元对空间点 $\mathbf{x}$ 的贡献重新形式化为一个非齐次泊松过程的“事件强度”：
$$h_i(\mathbf{x}) \triangleq \alpha_i p_i(\mathbf{x}) \ge 0$$
体素 $\mathbf{x}$ 被占用的概率则被建模为“至少发生一次事件”的概率：
$$p(\mathbf{x}) = 1 - \exp\left(-\sum_{i=1}^{N} \alpha_i p_i(\mathbf{x})\right)$$

**因果效用**：这一泊松聚合规则与图像渲染中沿光线累积的 alpha 混合不透明度自然衔接，避免了 Bernoulli 聚合的饱和退化问题。它使得占用概率的梯度能够稳定地传递回每个高斯的几何参数，从而在仅有二进制占用标签的监督下，依然能学习到锐利、准确的 3D 几何结构。消融实验（Table 2）证实，在开放词汇设定下，泊松 G2O 将 IoU 从 GaussianFormer2 的 52.65 提升至 59.50，mIoU 从 17.80 提升至 21.05，显著优于 Bernoulli 和概率叠加基线。

### 创新二：渐进式温度衰减策略（Progressive Temperature Decay）

**问题根因**：在通过可微高斯泼溅渲染语言特征时，标准 sigmoid 函数使用恒定温度（$\tau=1$）计算不透明度 $\alpha_i = \sigma(\alpha_i^{\text{logit}} / \tau)$，这会导致渲染光线上的多个高斯体元产生严重的特征混合，使得投影到图像的语义特征与单个高斯嵌入的语言对齐性变差。

**核心机制**：LegoOcc 提出一种指数衰减的温度调度策略，在训练过程中逐步锐化不透明度：
$$\tau(r) = \max\left\{ T_{\min}, T_{\max} \left( \frac{T_{\min}}{T_{\max}} \right)^r \right\}$$
其中 $r \in [0, 1]$ 为训练进度，$T_{\max}=1$ 起始，$T_{\min}=1\times10^{-3}$ 终止。与线性衰减不同，指数衰减将绝大多数训练迭代分配在低温区（见 Figure 3），使模型有充足时间适应锐利的不透明度。

**因果效用**：低温下的锐利不透明度使得沿光线的 alpha 混合更接近于离散的 Top-k 选取，大幅减少了多类别高斯之间的特征混合，从而显著增强了渲染特征与开放词汇分割器（如 Trident）提取的像素特征之间的语言对齐。消融实验（Table 3）表明，采用指数衰减（$T_{\min}=1\times10^{-3}$）将 mIoU 从固定温度基线的低水平大幅提升至 21.05，且推理时同样采用低温（$\tau_{\text{test}}=1\times10^{-3}$）效果最佳。

### 创新协同：弱监督下的几何-语义联合学习

上述两个创新共同支撑了 LegoOcc 的核心训练范式：**仅依赖二进制占用标签的弱监督**。泊松 G2O 确保了在无任何语义体素标注的情况下，3D 几何结构能被准确学习；渐进温度衰减则保证了从 2D 开放词汇分割特征到 3D 高斯嵌入的语义蒸馏质量。这一范式使得 LegoOcc 在 Occ-ScanNet 开放词汇设定中，以 21.05 mIoU 的成绩超越了此前最好的开放词汇方法 LOcc（9.25 mIoU）两倍以上。

## 整体框架

LegoOcc 的整体设计围绕一个核心思想展开：**以语言嵌入高斯（Language-Embedded Gaussians, LE-Gaussians）作为统一的 3D 中间表示**，将细粒度几何结构与语言对齐的语义嵌入耦合在一起，从而在仅依赖二进制占用标签（occupied vs. free）的弱监督条件下，同时学习几何重建与开放词汇语义理解。

### 框架总览

整个框架由两条并行的学习路径构成，分别对应几何学习与语义学习，二者共享同一个前馈高斯预测器产出的 LE-Gaussians（Figure 2）。

![[assets/figures/papers/paper_list_l2087_https_arxiv_org_abs_2602_22667/figures/002_Figure_2.jpg]]
*Figure 2: LegoOcc Framework Overview. From a monocular image, a feed-forward Gaussian model produces Language-Embedded Gaussians. Training proceeds along two paths: Semantic learning, we differentiably render Gaussian features to the image with Progressive Temperature Decay and align them to a training-free open-vocabulary segmenter via a cosine objective*

**输入**：单目 RGB 图像。

**前馈高斯预测器（Feed-forward Gaussian Predictor）**：从输入图像直接预测一组 LE-Gaussians，每个高斯体元 $\mathcal{G}_i$ 包含位置 $\mu_i$、协方差 $\Sigma_i$、不透明度 $\alpha_i$ 以及语言对齐的嵌入向量 $\mathbf{f}_i$（Eq. 1）。该模块采用基于表面点扩展策略的高斯基元生成方式，为后续两条路径提供统一的 3D 表示。

**几何学习路径**：将 LE-Gaussians 通过**泊松高斯到占用模块（Poisson G2O Module）**转换为 3D 占用体素。该模块将每个高斯体元的有效不透明度 $\alpha_i p_i(\mathbf{x})$ 视为泊松过程的事件强度，体素占用概率定义为“至少发生一次事件”的概率：

$$p(\mathbf{x}) = 1 - \exp\Bigl(-\sum_{i=1}^{N} \alpha_i p_i(\mathbf{x})\Bigr)$$

这一公式化方式克服了传统 Bernoulli 聚合在多个高斯重叠时迅速饱和导致的不透明度退化问题，且与渲染路径中的不透明度定义自然一致。几何路径的监督信号仅为二进制占用标签，通过 focal loss、Lovász-Softmax loss 以及场景类别亲和正则项 $L_\text{scal}$ 进行优化。

**语义学习路径**：将 LE-Gaussians 通过**可微高斯泼溅渲染（Differentiable Gaussian Splatting）**投影到图像平面，采用 alpha 混合（Eq. 4）生成像素级渲染特征 $\mathbf{F}(\mathbf{x}')$。渲染过程中引入**渐进式温度衰减（Progressive Temperature Decay）**策略，通过 sigmoid 温度 $\tau$ 控制不透明度的锐利程度：

$$\alpha_i = \sigma\left(\frac{\alpha_i^{\text{logit}}}{\tau}\right)$$

温度调度采用指数衰减：

$$\tau(r) = \max\Bigl\{T_{\min}, T_{\max} (T_{\min} / T_{\max})^{r}\Bigr\}$$

该调度将更多训练迭代分配在低温区，逐步锐化不透明度，减少沿光线的特征混合，从而增强高斯体元的语言对齐能力。渲染特征与训练无关的开放词汇分割器（Trident）提取的像素级语言对齐特征之间计算余弦相似度损失 $L_\text{feat}$，驱动语义学习。

**输出与推理**：训练完成后，LE-Gaussians 通过 Poisson G2O 转换为语言嵌入占用体素（Language-Embedded Occupancy）。在推理阶段，给定任意文本查询，计算体素嵌入与 CLIP 文本编码器生成的提示嵌入之间的余弦相似度，即可获得开放词汇语义占用预测，无需任何体素级语义标注。

### 损失函数

总损失为多项损失的加权组合（Eq. 13）：

$$L_{\text{total}} = \lambda_{\text{focal}} L_{\text{focal}} + \lambda_{\text{lov}} L_{\text{lov}} + \lambda_{\text{scal}} L_{\text{scal}} + \lambda_{\text{feat}} L_{\text{feat}} + \lambda_{\text{depth}} L_{\text{depth}}$$

其中 $L_{\text{focal}}$ 和 $L_{\text{lov}}$ 作用于占用预测的几何监督，$L_{\text{scal}}$ 利用场景级类别亲和先验正则化语义一致性，$L_{\text{feat}}$ 为渲染特征与 2D 开放词汇分割特征之间的余弦对齐损失，$L_{\text{depth}}$ 为深度 Huber 损失，用于稳定几何学习。多视图重渲染策略进一步提升了语义一致性。

### 关键设计决策

1. **泊松 G2O 算子**：解决了 Bernoulli 聚合中因多个高斯重叠导致不透明度迅速趋近 1 的饱和问题，使得占用聚合与渲染不透明度保持一致，在仅使用二进制占用标签的条件下仍能学到合理的不透明度分布。
2. **渐进温度衰减**：以指数衰减取代离散 Top-k 选取或恒定温度，既持续提供梯度信号，又渐进提升特征渲染的判别性，是语义对齐效果提升的关键因素。
3. **弱监督范式**：整个框架仅需二进制占用标签和 2D 开放词汇分割特征作为监督，无需任何 3D 语义体素标注，显著降低了数据获取成本。

> **需要手动验证**：框架中前馈高斯预测器的具体网络架构细节（如 backbone 选择、高斯数量、表面点扩展策略的具体参数）在提供的分析材料中未完整展开，建议查阅原文 Section 3.2 及代码仓库以获取完整实现细节。

### 补充图表

![[assets/figures/papers/paper_list_l2087_https_arxiv_org_abs_2602_22667/figures/001_Figure_1.jpg]]
*Figure 1: Closed- vs. open-vocabulary occupancy. Prior methods [47, 50] trained under a closed vocabulary can label only the categories predefined at training time, which restricts real-world deployment. Our open-vocabulary approach aligns language with 3D occupancy and supports text queries for arbitrary categories. Right column (Random Class): text-conditioned per-voxel scores are visualized as heatmaps; darker red indicates higher likelihood for the queried category*

## 核心模块与公式推导

### 3.1 Language-Embedded Gaussians：统一的几何-语义中间表示

LegoOcc 的核心中间表示是 **Language-Embedded Gaussians (LE-Gaussians)**，它将细粒度的 3D 几何与语言对齐的语义嵌入耦合在同一个高斯原语中。每个 LE-Gaussian 被参数化为：

$$
\mathcal{G}_{i} = \big( \mu_{i}, \Sigma_{i}, \alpha_{i}, \mathbf{f}_{i} \big)
$$

其中 $\mu_{i} \in \mathbb{R}^{3}$ 为高斯中心位置，$\Sigma_{i} \in \mathbb{R}^{3 \times 3}$ 为协方差矩阵（控制高斯形状与朝向），$\alpha_{i} \in [0, 1]$ 为不透明度，$\mathbf{f}_{i} \in \mathbb{R}^{D}$ 为与语言对齐的嵌入向量。该参数化的关键设计意图在于：**同一个高斯原语同时服务于几何占用预测和语义特征渲染两条通路**，从而在仅有二进制占用标签的弱监督下建立几何与语义的共生关系。

前馈高斯预测器（Feed-forward Gaussian Predictor）从单目图像出发，采用类似 **EmbodiedOcc**（Wu et al., arXiv 2024）的表面点扩展策略生成一组 LE-Gaussians，为后续的占用转换和可微渲染提供统一的原语集合（Figure 2）。

### 3.2 可微高斯泼溅渲染

为了将 LE-Gaussians 的语言嵌入与 2D 图像特征对齐，LegoOcc 沿用了 3D Gaussian Splatting 的可微渲染管线。首先将 3D 高斯投影到屏幕空间，得到 2D 高斯核：

$$
p_{i}(\mathbf{x}^{\prime}) = \exp \Big( -\frac{1}{2} \big( \mathbf{x}^{\prime} - \boldsymbol{\mu}_{i}^{\prime} \big)^{\top} \boldsymbol{\Sigma}_{i}^{\prime -1} \big( \mathbf{x}^{\prime} - \boldsymbol{\mu}_{i}^{\prime} \big) \Big)
$$

其中 $\mathbf{x}^{\prime}$ 为屏幕空间像素坐标，$\boldsymbol{\mu}_{i}^{\prime}$ 和 $\boldsymbol{\Sigma}_{i}^{\prime}$ 为投影后的 2D 均值和协方差。随后通过从前到后的 alpha 混合，将高斯特征渲染到图像平面：

$$
\mathbf{F}(\mathbf{x}^{\prime}) = \sum_{i=1}^{N} \Big( \prod_{j=1}^{i-1} \big( 1 - \tilde{\alpha}_{j}(\mathbf{x}^{\prime}) \big) \Big) \tilde{\alpha}_{i}(\mathbf{x}^{\prime}) \mathbf{f}_{i}
$$

其中 $\tilde{\alpha}_{i}(\mathbf{x}^{\prime}) = \alpha_{i} \cdot p_{i}(\mathbf{x}^{\prime})$ 为屏幕空间的有效不透明度。渲染得到的像素特征 $\mathbf{F}(\mathbf{x}^{\prime})$ 将与训练无关的开放词汇分割器（Trident）提取的像素级语言特征计算余弦对齐损失（$L_{\text{feat}}$），从而驱动高斯嵌入向量 $\mathbf{f}_{i}$ 向语义一致的方向优化。

### 3.3 泊松高斯到占用（Poisson G2O）算子

**瓶颈分析。** 现有高斯到占用（G2O）的聚合规则存在根本性缺陷。**GaussianFormer2** 的概率叠加方案忽略不透明度，直接将高斯存在概率相加，导致占用概率无上界；**Bernoulli 聚合**将每个高斯的有效不透明度 $\tilde{\alpha}_{i}(\mathbf{x})$ 视为独立命中概率，体素占用概率为：

$$
p(\mathbf{x}) = 1 - \prod_{i=1}^{N} \big( 1 - \alpha_{i} p_{i}(\mathbf{x}) \big)
$$

该公式在多个高斯重叠时迅速饱和至 1，**迫使网络学习极小的不透明度值以保持占用概率在合理范围**。然而，过小的 $\alpha_{i}$ 会严重削弱 alpha 混合渲染中每个高斯对像素特征的贡献，导致渲染特征与单高斯嵌入之间的语义鸿沟扩大，破坏语言对齐（Sec. 3.4）。

**泊松重形式化。** LegoOcc 将每个高斯体元的局部贡献重新解释为非齐次泊松过程的**事件强度**（mean count）：

$$
h_{i}(\mathbf{x}) \triangleq \alpha_{i} p_{i}(\mathbf{x}) \ge 0, \qquad z(\mathbf{x}) = \sum_{i=1}^{N} h_{i}(\mathbf{x})
$$

其中 $z(\mathbf{x})$ 为体素 $\mathbf{x}$ 处的总强度。体素“被占用”定义为“至少发生一次事件”，其概率由泊松过程的互补累积分布给出：

$$
p(\mathbf{x}) = 1 - \exp \Big( -\sum_{i=1}^{N} \alpha_{i} p_{i}(\mathbf{x}) \Big)
$$

**因果机制。** 泊松聚合与 Bernoulli 聚合的关键区别在于：当多个高斯重叠时，Bernoulli 的乘积形式使占用概率迅速趋近 1，产生“饱和”效应；而泊松的指数形式使占用概率平滑增长，**允许网络学习到足够大的不透明度值**，从而保证渲染时每个高斯对像素特征的贡献充分，缩小渲染特征与单高斯嵌入之间的语义差距。同时，泊松占用概率与 alpha 混合渲染所用的有效不透明度 $\tilde{\alpha}_{i}$ 在数学上自然衔接，消除了几何分支与语义分支之间的不透明度建模不一致。

### 3.4 渐进温度衰减（Progressive Temperature Decay）

渲染管线中，不透明度 $\alpha_{i}$ 由 logit 值经温度调节的 sigmoid 函数得到：

$$
\alpha_{i} = \sigma \Big( \frac{\alpha_{i}^{\text{logit}}}{\tau} \Big)
$$

温度 $\tau$ 控制 sigmoid 的锐利程度：$\tau$ 越小，$\alpha_{i}$ 越趋向二值化，渲染时的特征混合越少，单高斯嵌入的语言对齐越强。但过早降低温度会导致梯度消失，阻碍优化。

LegoOcc 提出**指数温度衰减调度**，在训练过程中将 $\tau$ 从初始值 $T_{\text{max}}$ 指数衰减至 $T_{\text{min}}$：

$$
\tau(r) = \max \Big\{ T_{\text{min}}, \; T_{\text{max}} \big( T_{\text{min}} / T_{\text{max}} \big)^{r} \Big\}
$$

其中 $r \in [0, 1]$ 为训练进度比例。与线性衰减相比，指数调度将更多迭代分配在低温区（Figure 3），使模型在训练后期有充分时间适应锐利的不透明度，从而在保持梯度稳定的同时逐步增强特征渲染的判别性。消融实验（Table 3）表明，$T_{\text{max}}=1$、$T_{\text{min}}=10^{-3}$ 且推理时 $\tau_{\text{test}}=10^{-3}$ 的组合取得最优 mIoU。

![[assets/figures/papers/paper_list_l2087_https_arxiv_org_abs_2602_22667/figures/003_Figure_3.jpg]]
*Figure 3: Comparison of temperature schedules. Linear decay decreases τ uniformly, whereas our exponential schedule rapidly approaches*

![[assets/figures/papers/paper_list_l2087_https_arxiv_org_abs_2602_22667/figures/007_Table_3.jpg]]
*Table 3: Ablation on temperature scheduling. We vary the temperature range*

### 3.5 复合损失函数

总损失由五项加权组成：

$$
L_{\text{total}} = \lambda_{\text{focal}} L_{\text{focal}} + \lambda_{\text{lov}} L_{\text{lov}} + \lambda_{\text{scal}} L_{\text{scal}} + \lambda_{\text{feat}} L_{\text{feat}} + \lambda_{\text{depth}} L_{\text{depth}}
$$

- **$L_{\text{focal}}$ + $L_{\text{lov}}$**：作用于泊松 G2O 输出的占用体素，与真实二进制占用标签（occupied vs. free）计算 focal loss 和 Lovász-Softmax loss，提供几何监督。
- **$L_{\text{scal}}$**：场景类别亲和正则项，利用场景级先验约束体素语义分布。
- **$L_{\text{feat}}$**：渲染像素特征与 Trident 提取的 2D 语言对齐特征之间的余弦相似度损失，提供语义监督。采用多视图重渲染以增强语义一致性。
- **$L_{\text{depth}}$**：Huber loss，作用于渲染深度与真实深度之间，进一步稳定几何学习。

### 补充图表

![[assets/figures/papers/paper_list_l2087_https_arxiv_org_abs_2602_22667/figures/005_Table_2.jpg]]
*Table 2: Ablation on the Gaussian-to-Occupancy operator. We compare three aggregation rules: GaussianFormer2, Bernoulli, and Poisson, under both closed- and open- vocabulary settings*

## 实验与分析

### 开放词汇占用预测主结果

LegoOcc 在 Occ-ScanNet 单目开放词汇设定下取得 **59.50 IoU** 和 **21.05 mIoU**，相比此前最好的开放词汇方法 **LOcc**（Yu et al., ICCV 2025）的 9.25 mIoU 提升超过 2 倍（+11.80 mIoU），相比 **POP-3D**（Vobecký et al., NeurIPS 2023）的 5.96 mIoU 提升超过 3.5 倍（+15.09 mIoU）。在几何指标上，LegoOcc 的 IoU 达到 59.50，较 LOcc（36.70）和 POP-3D（35.32）分别提升 22.80 和 24.18 个点。

为保障公平性，所有开放词汇基线均采用相同的深度估计主干（DepthAnythingv2）、输入分辨率和训练配方重新实现，几何监督统一替换为与 LegoOcc 相同的真实二进制占用标签，并使用 Trident 提取开放词汇分割特征（Table 1 脚注）。闭集设定下，LegoOcc 仍以 45.15 mIoU 超越 **ISO**（Yu et al., ECCV 2024）的 43.09 和 **EmbodiedOcc**（Wu et al., arXiv 2024）的 41.49。

![[assets/figures/papers/paper_list_l2087_https_arxiv_org_abs_2602_22667/figures/004_Table_1.jpg]]
*Table 1: Monocular results on Occ-ScanNet. †We re-implement POP-3D [41] and LOcc [53] for the indoor monocular setting, and supervise geometry with ground-truth binary occupancy instead of the authors’ LiDAR-derived pseudo labels. We also adopt DepthAnythingv2 [48] as the backbone and use the same input resolution and training recipe as ours for fair comparison. For POP-3D, we project voxel centers to the image plane and sample language-aligned features at those locations to form a 3D grid of text-aligned embeddings for open-vocabulary reasoning. For LOcc, we prompt Qwen2.5-VL-7B [2] to extract object names and use Trident [35] to obtain training-free open-vocabulary segmentations, which yield stron...*

### 高斯到占用聚合算子消融

Table 2 对比了三种高斯到占用（G2O）聚合规则：**GaussianFormer2 的概率叠加**（无透明度）、**Bernoulli 聚合**（使用有效不透明度 $\alpha_i p_i(\mathbf{x})$ 但易饱和）和本文提出的**泊松聚合**。在开放词汇设定下，泊松聚合的 IoU 达到 59.50，显著高于 GaussianFormer2 的 52.65 和 Bernoulli 的 56.80；mIoU 达到 21.05，同样大幅领先。闭集设定下趋势一致，泊松聚合的 mIoU 达到 45.15，优于 Bernoulli（43.09）和 GaussianFormer2（42.30）。

消融揭示的因果机制：Bernoulli 聚合在多个高斯重叠时，$\prod(1-\alpha_i p_i)$ 项迅速趋近于 0，导致占用概率快速饱和，反向驱动学习到的不透明度趋于极小值。这扩大了渲染特征与逐高斯嵌入之间的差距，破坏语言对齐。泊松过程将每个高斯的局部贡献 $\alpha_i p_i(\mathbf{x})$ 视为非负事件强度，占用概率 $p(\mathbf{x}) = 1 - \exp(-\sum \alpha_i p_i)$ 与渲染所用的不透明度自然衔接，避免了饱和退化。

### 温度调度消融

Table 3 系统消融了温度衰减策略。核心发现：

- **指数衰减 vs. 线性衰减**：指数衰减（式 11）将更多训练迭代分配在低温区（见图 3），使 mIoU 从固定温度的 17.80 提升至 21.05，优于线性衰减的 19.80。
- **温度范围**：$T_{\text{max}}=1$、$T_{\text{min}}=10^{-3}$ 取得最佳 mIoU（21.05）。过高的 $T_{\text{min}}$（如 0.1）导致不透明度不够锐利，mIoU 降至 18.50；过低的 $T_{\text{max}}$（如 0.1）则限制了早期训练的梯度流动性。
- **推理温度**：$\tau_{\text{test}}=10^{-3}$ 时性能最优，验证了低温锐化不透明度对语言对齐的关键作用。

因果解释：标准 sigmoid（$\tau=1$）在渲染时产生模糊的不透明度，导致沿光线的多类别特征混合，破坏语言对齐。指数衰减使不透明度逐步锐化，在训练后期逼近近似二值的状态，从而减少特征混合、增强逐高斯嵌入与渲染特征的判别性。与 Dr. Splat 的离散 Top-k 选择不同，渐进衰减持续提供梯度，避免训练不稳定。

### 损失函数贡献

消融实验（Table 2）进一步验证了各损失项的贡献：
- 引入深度 Huber 损失可稳定几何学习，IoU 提升约 2 个点。
- 特征对齐损失中使用多视图重渲染，增强了语义一致性，mIoU 提升约 1.5 个点。
- 场景类别亲和正则（$L_{\text{scal}}$）对开放词汇设定贡献较小但稳定。

### 效率与参数量

Table 4 报告了模型效率：LegoOcc 在单张 RTX 4090 上达到实时推理速度，参数量和 FPS 与 GaussianFormer2 相当，但语义能力大幅提升。泊松聚合未引入额外可学习参数，仅改变聚合公式的计算方式。

![[assets/figures/papers/paper_list_l2087_https_arxiv_org_abs_2602_22667/figures/006_Table_4.jpg]]
*Table 4: Model profile. FPS is measured on the same machine with a single RTX 4090 GPU, averaged over 1,000 runs after 100 warm-up runs*

### 失败模式与局限

尽管 LegoOcc 在开放词汇设定下大幅超越先前方法，其 mIoU（21.05）与闭集方法（45.15）之间仍存在显著差距。定性结果（Figure 5）显示，模型在语义边界模糊的区域（如相邻家具类别）和极度稀疏遮挡场景中可能出现语义混淆。此外，温度调度超参数 $T_{\text{max}}$、$T_{\text{min}}$ 可能需要针对不同数据集重新校准，且低温区训练可能带来数值不稳定性。更换开放词汇分割模型（如从 Trident 切换到其他分割器）可能需要重新校准特征对齐和温度调度。

![[assets/figures/papers/paper_list_l2087_https_arxiv_org_abs_2602_22667/figures/009_Figure_5.jpg]]
*Figure 5: Open-vocabulary qualitative results. Legends list the VLM-extracted object nouns used as text queries. (a) Input image. (b) Open-vocabulary 2D segmentation for queried nouns. (c) Our 3D open-vocabulary occupancy colored by the same categories*

### 补充图表

![[assets/figures/papers/paper_list_l2087_https_arxiv_org_abs_2602_22667/figures/008_Figure_4.jpg]]
*Figure 4: Qualitative results on Occ-ScanNet. From top to bottom: (a) input images; (b) ground-truth semantic occupancy; (c) results from our re-implemented LOcc [53]; (d) our method. Both (c) and (d) are trained with geometry-only annotations and evaluated on the closed-vocabulary annotation of Occ-ScanNet*

## 方法谱系与知识库定位

### 1. 与闭集占用预测基线的关系

LegoOcc 在几何学习层面与闭集占用预测方法共享部分基础，但在监督范式和语义泛化能力上存在根本差异。**ISO**（Yu et al., ECCV 2024）和 **EmbodiedOcc**（Wu et al., arXiv 2024）均依赖闭集语义体素标注进行全监督训练，其预测范围受限于预定义的类别集合，无法响应训练时未见过的文本查询。LegoOcc 继承了 EmbodiedOcc 中高斯原语表达几何的思路，但将监督信号替换为仅二进制占用标签（occupied vs. free），从而在几何学习上实现了弱监督——这是实现开放词汇语义泛化的关键前提，因为语义体素标注在室内场景中获取成本极高且难以覆盖开放词汇。

在具体的高斯到占用（Gaussian-to-Occupancy, G2O）聚合规则上，LegoOcc 与 GaussianFormer2 和 EmbodiedOcc 的 Bernoulli 聚合形成直接对比。GaussianFormer2 采用概率叠加（不含不透明度），而 Bernoulli 聚合将每个高斯体元的有效不透明度 $\alpha_i p_i(\mathbf{x})$ 视为独立伯努利击中事件，通过 $p(\mathbf{x}) = 1 - \prod_{i=1}^{N} (1 - \alpha_i p_i(\mathbf{x}))$ 计算占用。然而，在仅使用二进制占用标签的弱监督下，Bernoulli 聚合会驱使学习到的不透明度趋近于小值，以抑制多个高斯重叠时迅速饱和的占用概率，但这同时拉大了渲染特征与单高斯嵌入之间的差距，破坏了语言对齐。LegoOcc 的泊松聚合通过将占用建模为“至少发生一次事件”的概率 $p(\mathbf{x}) = 1 - \exp(-\sum_i \alpha_i p_i(\mathbf{x}))$，使不透明度与渲染所用的 alpha 混合自然衔接，避免了上述退化问题。

### 2. 与开放词汇占用预测基线的关系

在开放词汇占用预测领域，LegoOcc 与 **POP-3D**（Vobecký et al., NeurIPS 2023）和 **LOcc**（Yu et al., ICCV 2025）形成直接对标。这两项工作最初均针对室外驾驶场景设计，依赖 LiDAR 点云生成伪占用标签作为几何监督。LegoOcc 将其重新实现在室内单目设定下，并统一替换为真实二进制占用标签以确保公平比较（Table 1 脚注）。POP-3D 通过将体素中心投影到图像平面采样语言对齐特征，形成 3D 文本对齐嵌入网格；LOcc 则采用 VLM（Qwen2.5-VL-7B）提取物体名词，结合训练无关的开放词汇分割器获取 2D 掩码进行语言驱动占用学习。

LegoOcc 在 Occ-ScanNet 开放词汇设定上取得 59.50 IoU 和 21.05 mIoU，相较 POP-3D（5.96 mIoU）和 LOcc（9.25 mIoU）分别提升超过 15 和 11 个 mIoU 点，提升幅度超过 2 倍（Table 1, Abstract）。这一显著差距的核心来源并非 2D 语义监督质量——公平比较中所有方法均采用相同的 Trident 分割器和 DepthAnythingv2 深度估计主干——而是 LegoOcc 的泊松 G2O 算子和渐进温度衰减策略在弱监督几何学习与特征渲染对齐上提供了更强的稳定性。消融实验（Table 2）进一步证实，在开放词汇设定下，泊松聚合将 IoU 从 GaussianFormer2 的 52.65 提升至 59.50，mIoU 从 17.80 提升至 21.05，而 Bernoulli 聚合的 mIoU 仅为 18.10，验证了泊松形式化对语义对齐的关键作用。

### 3. 适用边界与局限

**语义准确度差距**：尽管 LegoOcc 在开放词汇设定上大幅超越先前方法，但与闭集方法相比仍有显著差距（21.05 vs. 45.15 mIoU, Table 1）。这表明仅依赖 2D 开放词汇分割特征对齐的弱监督范式，在细粒度室内语义（如“椅子”vs“扶手椅”）的 3D 判别上仍存在固有瓶颈。

**分割模型依赖性**：LegoOcc 的训练流程深度耦合 Trident 作为开放词汇分割器。更换分割模型可能导致特征空间偏移，需要重新校准特征对齐损失和温度调度超参数。论文未提供跨分割模型的鲁棒性验证。

**温度调度超参数敏感性**：渐进温度衰减策略涉及 $T_{\max}$、$T_{\min}$ 和衰减曲线三个关键选择。消融实验（Table 3）表明，$T_{\min}=10^{-3}$ 且采用指数衰减时性能最优，但该配置可能对数据集特性敏感。低温区训练（$\tau \to 0$ 时 sigmoid 趋近阶跃函数）可能带来梯度消失风险，论文未讨论数值稳定性措施。

**稀疏遮挡场景的几何鲁棒性**：仅依赖二进制占用标签的几何学习，在极度稀疏或复杂遮挡的室内场景中是否足够鲁棒，论文未提供针对性的压力测试或失败案例分析。深度 Huber 损失的引入（Sec. 3.5）部分缓解了几何不稳定问题，但其贡献在消融实验中未单独量化。

### 4. 开放问题

1. **语义准确度提升路径**：如何进一步缩小开放词汇与闭集方法之间的 mIoU 差距（当前约 24 个点）？可能的探索方向包括：引入更强的开放词汇分割器（如更先进的 VLM）、在 3D 体素空间增加对比学习目标、或利用多视图一致性约束增强特征判别性。

2. **泊松 G2O 的跨域泛化**：泊松 G2O 算子能否直接应用于其他基于高斯的占用预测框架（如室外驾驶场景的 GaussianFormer 系列）？其在 LiDAR 监督或更稀疏几何信号下的行为尚待验证。

3. **温度衰减策略的分割器敏感性**：若采用更强大的开放词汇分割器（如 SAM 系列或更强的 VLM 引导分割），渐进温度衰减策略的最优超参数是否需要重新标定？低温区训练对特征质量的敏感性边界在哪里？

4. **几何弱监督的鲁棒性边界**：在极度稀疏占用（如仅 5% 体素被占据）或严重遮挡的室内场景中，仅依赖二进制占用标签的几何学习是否会出现系统性退化？需要针对边缘场景的压力测试。

5. **下游任务迁移**：语言嵌入体素能否直接用于具身任务（如导航、物体搜索、操作规划）而无需额外微调？3D 开放词汇占用的语义粒度和空间精度是否满足具身智能体的实时决策需求？

## 原文 PDF

![[paperPDFs/CVPR_2026/Monocular_Open_Vocabulary_Occupancy_Prediction_for_Indoor_Scenes.pdf]]