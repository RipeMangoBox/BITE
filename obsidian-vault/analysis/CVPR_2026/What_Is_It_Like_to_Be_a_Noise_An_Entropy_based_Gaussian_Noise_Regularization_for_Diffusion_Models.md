---
title: What Is It Like to Be a Noise? An Entropy-based Gaussian Noise Regularization for Diffusion Models
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/What_Is_It_Like_to_Be_a_Noise_An_Entropy_based_Gaussian_Noise_Regularization_for_Diffusion_Models.pdf
project_link: null
code_link: null
aliases:
- EBGNRE
tags:
- CVPR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 通过施加显式的基于熵的高斯性正则项，控制噪声的1D边缘分布、2D空间关联以及多尺度统计，使其保持在高斯典型集内，从而稳定生成质量并防止过拟合。
primary_logic: 不应将高斯性视为逐点概率，而应看作分布性质；将单个样本提升为其统计量诱导的经验分布，并用成对马尔可夫随机场建模，通过Bethe-Kikuchi逼近将KL散度分解为可微的1D边际熵、2D空间熵和多尺度项，实现对任意噪声样本的有效高斯化投影。
claims:
- 提出的正则化器通过对齐样本局部统计量与典型高斯实现来定义高斯性，而非逐点似然。
- 通过将样本建模为成对MRF并应用Bethe-Kikuchi展开，得到包含1D边际熵和2D空间熵的可计算KL目标。
- 在美学分数优化和亮度最小化任务上，该方法产生无伪影且更自然的图像，防止了奖励攻击。
- 不应将高斯性视为逐点概率，而应看作分布性质；将单个样本提升为其统计量诱导的经验分布，并用成对马尔可夫随机场建模，通过Bethe-Kikuchi逼近将KL散度分解为可微的1D边际熵、2D空间熵和多尺度项，实现对任意噪声样本的有效高斯化投影。
---

# What Is It Like to Be a Noise? An Entropy-based Gaussian Noise Regularization for Diffusion Models

> [!tip] 核心洞察
> 不应将高斯性视为逐点概率，而应看作分布性质；将单个样本提升为其统计量诱导的经验分布，并用成对马尔可夫随机场建模，通过Bethe-Kikuchi逼近将KL散度分解为可微的1D边际熵、2D空间熵和多尺度项，实现对任意噪声样本的有效高斯化投影。

| 字段 | 内容 |
|------|------|
| 中文题名 | 成为噪声是怎样的？一种基于熵的高斯噪声正则化用于扩散模型 |
| 英文题名 | What Is It Like to Be a Noise? An Entropy-based Gaussian Noise Regularization for Diffusion Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Chang_What_Is_It_Like_to_Be_a_Noise_An_Entropy-based_CVPR_2026_paper.html) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | Entropy-based Gaussian Noise Regularization (EGNR) |
| Dataset | Synthetic latent/image-to-noise optimization tasks, SDXL-Turbo reward-optimization prompts |
> [!tip] 效果简介
> - 通过将样本建模为成对MRF并应用Bethe-Kikuchi展开，得到包含1D边际熵和2D空间熵的可计算KL目标。

## 概要

扩散模型在推理时对噪声潜变量进行优化（如奖励引导生成、图像反演）会使其偏离真实高斯噪声的统计结构，导致模型被迫对分布外样本去噪，产生过饱和色彩、伪影和脆性行为——即“奖励攻击”。现有正则化方法多依赖逐点概率密度约束或简单全局矩匹配，未能有效刻画和保持高斯噪声的分布性质。

本文提出 **Entropy-based Gaussian Noise Regularization (EGNR)**，核心思想是将高斯性视为分布性质而非逐点似然：将单个噪声样本提升为其局部统计量诱导的经验分布，通过成对马尔可夫随机场（MRF）建模，并利用Bethe-Kikuchi逼近将KL散度分解为可微的1D边际熵、2D空间熵和多尺度项，实现对任意噪声样本的有效高斯化投影。

该方法在美学分数优化和亮度最小化等奖励对齐任务上产生无伪影且更自然的图像，防止了奖励攻击；同时支持模型无关的图像到噪声匹配，在保持分布内特性的前提下实现跨模型迁移。消融实验证实，1D熵、2D熵、Bethe校正和多尺度监督四个组件缺一不可。主要局限在于KDE差分熵估计的计算开销较高，以及成对MRF假设对严重偏离高斯的输入（如干净图像潜变量）可能无法解析复杂长程结构。

方法定位上，EGNR属于扩散模型推理时正则化方法，与 **ReNO** (Eyring et al., 2024)、**ReNoise** (Garibi et al., ECCV 2024) 等基于范数或频谱约束的基线形成对比，其独特之处在于通过信息论框架系统性地约束噪声的1D边缘分布和2D空间关联，而非仅施加ℓ₂距离约束。

扩散模型通过逐步向数据添加高斯噪声并学习反向去噪过程来生成数据，其核心假设是：**推理时的初始潜变量严格服从标准高斯分布**。这一假设在标准采样中自然成立——只需从高斯分布中随机抽取即可。然而，近年来涌现的大量应用场景打破了这一前提：无论是扩散模型反演（inversion）、奖励对齐（reward alignment），还是对抗攻击与可编辑生成，都需要对推理噪声进行**显式优化**，使其在满足特定任务目标的同时仍能生成高质量图像。

**核心瓶颈**：对扩散噪声潜变量进行优化会使其偏离真实高斯噪声的统计结构，导致模型被迫对分布外（out-of-distribution）样本去噪，从而产生伪影、脆性行为和奖励攻击（reward hacking）。具体表现为：过度饱和的色彩、不自然的斑点状纹理，以及整体图像质量的退化。

现有方法试图通过各种手段约束优化后的噪声保持“高斯性”，但其测度方式存在根本性局限：

- **逐点概率密度方法**（如 $-\\log G(\\mathbf{x})$）将高斯性视为单点的似然值，忽略了噪声作为**分布**的整体统计特征。一个样本可以具有高似然却完全不具备高斯噪声的典型空间结构。
- **全局矩匹配方法**仅约束一阶或二阶统计量，无法捕捉空间关联和多尺度结构，导致约束过弱。
- **ℓ₂距离约束**（如 **Pix2Pix-Zero**，Parmar et al., 2023；**ReNO**，Eyring et al., 2024）和频谱匹配方法（如 **ReNoise**，Garibi et al., ECCV 2024）虽然提供了正则化，但无法精确刻画高斯分布的完整统计特性，在强优化压力下仍会出现分布偏移。

**本文动机**：不应将高斯性视为逐点概率，而应看作**分布性质**。核心洞察是：将单个样本提升为其统计量诱导的经验分布，并用KL散度度量该经验分布与标准高斯分布之间的差异。通过成对马尔可夫随机场（MRF）建模像素间的局部依赖，并利用Bethe-Kikuchi逼近将KL散度分解为可微的1D边际熵、2D空间熵和多尺度项，实现对任意噪声样本的**有效高斯化投影**。这一正则化器能够在保持任务目标优化的同时，将噪声牢牢约束在高斯典型集内，从根本上防止分布外退化的发生。

## 核心方法与创新机理

### 从逐点似然到分布级高斯性度量

现有扩散模型在推理时对噪声潜变量进行优化（如奖励引导生成、图像反演等）时，普遍依赖逐点概率密度约束——例如直接最小化 $-\log G(\mathbf{x})$ 或简单的 $\ell_2$ 范数约束——来维持噪声的“高斯性”。这些方法（如 **ReNO** (Eyring et al., 2024)、**ReNoise** (Garibi et al., ECCV 2024)、**Hwang et al.** (2025) 等）将高斯性视为单个样本点的属性，忽略了高斯分布作为**分布**的统计结构特征。其根本缺陷在于：一个样本即使逐点似然很高，其局部统计量（如相邻像素的相关性、多尺度能量分布）仍可能严重偏离高斯典型集，导致扩散模型被迫对分布外样本去噪，产生伪影、过饱和色彩或“奖励攻击”行为。

本文的核心范式转换在于：**将高斯性从逐点概率重新定义为样本统计量诱导的经验分布与目标高斯分布之间的 KL 散度**。具体而言，对于任意待优化的噪声样本 $\hat{\mathbf{x}}$，不直接评估其在高斯密度函数下的似然值，而是将其“提升”为由局部统计量构建的经验分布 $P_{\hat{\mathbf{x}}}$，然后度量该经验分布与标准高斯 $G$ 的差异：

$$\mathcal{D}_G(\hat{\mathbf{x}}) = D_{\mathrm{KL}}(P_{\hat{\mathbf{x}}} \parallel G) \tag{3}$$

这一测度的关键优势在于：它天然捕获了样本的**统计结构**（包括像素值的边际分布、相邻像素的联合分布以及多尺度相关性），而非仅关注单个像素的数值大小。Figure 1 直观展示了这一差异——对于图像像素、潜变量、棋盘纹理和高斯噪声四种输入，1D 熵（Value Entropy）仅反映像素值的边际分布，而 2D 熵（Spatial Entropy）则能有效区分具有空间结构的输入与真正的高斯噪声。

### 成对 MRF 建模与 Bethe-Kikuchi 可微分解

将 KL 散度直接应用于高维样本面临两个核心挑战：(1) 如何从单个样本构建有意义的经验分布；(2) 如何使该度量端到端可微。

针对第一个挑战，本文提出将样本 $\hat{\mathbf{x}}$ 的像素网格建模为**成对马尔可夫随机场（Pairwise MRF）**，将其联合密度分解为节点势函数（捕获单像素统计）和边势函数（捕获相邻像素对统计）的乘积：

$$p_{\hat{\mathbf{x}}}(\mathbf{x}) = \frac{1}{Z} \prod_{i \in \mathcal{V}} \psi_i(x_i) \prod_{(i,j) \in \mathcal{E}} \psi_{ij}(x_i, x_j) \tag{4}$$

基于此因子化形式，应用 **Bethe-Kikuchi 团簇展开**将全局 KL 散度近似为节点团簇和边团簇上熵的加权和，得到最终的正则化目标：

$$D_{\mathrm{KL}}(P_{\hat{\mathbf{x}}} \parallel G) \approx \underbrace{D_{\mathrm{KL}}(P_{\hat{\mathbf{x}}, S^{(2)}} \parallel G_{S^{(2)}})}_{\text{Spatial Entropy Term}} + \gamma \underbrace{D_{\mathrm{KL}}(P_{\hat{\mathbf{x}}, S^{(1)}} \parallel G_{S^{(1)}})}_{\text{Value Entropy Term}} \tag{5}$$

其中 **Spatial Entropy Term** 度量相邻像素对的 2D 联合经验分布与 2D 高斯之间的 KL 散度，捕获空间相关性；**Value Entropy Term** 度量单像素值的 1D 经验分布与 1D 高斯之间的 KL 散度，捕获边际分布；$\gamma$ 为 Bethe 修正因子，用于补偿低分辨率直方图中因过分计数引入的偏差。

针对第二个挑战，本文将每个 KL 散度项进一步分解为交叉熵与差分熵之差：

$$D_{\mathrm{KL}}(P_{\hat{\mathbf{x}}} \parallel G) = \underbrace{H(P_{\hat{\mathbf{x}}}, G)}_{\text{Cross-Entropy}} - \underbrace{H(P_{\hat{\mathbf{x}}})}_{\text{Differential Entropy}} \tag{6}$$

其中交叉熵通过蒙特卡洛采样结合目标高斯的解析对数密度 $\log G(\mathbf{v}) = -\frac{d}{2}\log(2\pi) - \frac{1}{2}\|\mathbf{v}\|_2^2$ 进行估计；差分熵则通过**高斯核密度估计（KDE）**从样本点集近似连续密度后计算，整个流程对原始像素值 $\hat{\mathbf{x}}$ 端到端可微。

### 多尺度金字塔扩展与全局统计约束

成对 MRF 假设天然只能捕获局部邻域的空间相关性，对于长程结构（如大尺度纹理、全局布局）的约束能力有限。为此，本文引入**多尺度金字塔策略**：对样本执行方差保持的下采样（$2\times 2$ 均值池化后乘以 $\sqrt{n}$ 以保持方差），将正则化损失施加于多个分辨率层级：

$$\mathcal{L}_{\mathrm{full}}(\hat{\mathbf{x}}) = \sum_{k=0}^{L-1} \alpha_k D_{\mathrm{KL}}(P_{\hat{\mathbf{x}}_k} \parallel G)$$

这一设计使得原本局部的边团簇约束在低分辨率下覆盖更大的感受野，从而间接惩罚长程空间关联。实验表明（Figure 2），多尺度监督与任意配置（1D 熵、2D 熵、Bethe 修正）结合均能进一步改善噪声向高斯分布的投影质量。

### 与 baseline 的关键差异总结

| 维度 | 现有方法 | 本文方法 (EGNR) |
|------|----------|-----------------|
| **高斯性定义** | 逐点概率密度（$-\log G(\mathbf{x})$）或全局矩匹配 | 样本统计量诱导的经验分布与高斯的 KL 散度 |
| **空间结构建模** | 无显式建模或仅频谱约束 | 成对 MRF 因子化 + 2D 空间熵项捕获邻域相关性 |
| **可微性实现** | 解析梯度或简单范数 | KDE + 蒙特卡洛实现端到端可微熵估计 |
| **多尺度约束** | 通常缺失 | 方差保持下采样金字塔，局部约束延伸至全局 |
| **理论框架** | 启发式或变分下界 | Bethe-Kikuchi 团簇展开提供系统逼近 |

消融实验（Figure 2）明确证实：**仅使用 1D 熵或多尺度 1D 熵无法产生高质量噪声**，必须引入 2D 空间熵来捕获空间相关性；Bethe 修正细化了低分辨率直方图的 KL 估计；所有组件（1D 熵、2D 熵、Bethe 修正、多尺度监督）对最终的高质量噪声投影均不可或缺。

EGNR 的整体 pipeline 围绕一个核心目标展开：将任意候选噪声潜变量 $\hat{\mathbf{x}}$ 投影到标准高斯分布 $G$ 的典型集内，同时保持与原始输入 $\mathbf{x}_0$ 的语义关联或满足特定奖励函数 $R$ 的要求。该框架由五个紧密协作的模块构成，形成从样本到高斯化投影的端到端可微计算图。

### 输入输出流

框架接受两类输入场景：(1) **数据保真场景**——给定初始潜变量 $\mathbf{x}_0$，寻找其最近的高斯对应样本；(2) **奖励引导场景**——以奖励函数 $R$ 为目标，在满足高斯性约束的前提下优化噪声潜变量。两种场景共享同一正则化核心，仅在顶层目标函数上有所区分：

- **数据保真目标**：$\mathbf{x}^* = \arg\min_{\hat{\mathbf{x}}} \lambda_S \mathcal{D}_S(\mathbf{x}_0, \hat{\mathbf{x}}) + \lambda_G \mathcal{D}_G(\hat{\mathbf{x}})$
- **奖励引导目标**：$\mathbf{x}^* = \arg\min_{\hat{\mathbf{x}}} -R(\hat{\mathbf{x}}) + \lambda \mathcal{L}_{\mathrm{full}}(\hat{\mathbf{x}})$

其中 $\mathcal{D}_G(\hat{\mathbf{x}})$ 即本文提出的高斯性测度，$\mathcal{L}_{\mathrm{full}}$ 为其多尺度扩展形式。输出为优化后的噪声潜变量 $\mathbf{x}^*$，可直接馈入扩散模型生成图像。

### 五大核心模块

**模块一：经验分布构建。** 将单个输入样本 $\hat{\mathbf{x}}$ 提升为其统计量诱导的经验分布 $P_{\hat{\mathbf{x}}}$。具体而言，将像素网格视为图结构 $\mathcal{G}=(\mathcal{V}, \mathcal{E})$，从样本中提取所有像素值集合（用于1D边际统计）和所有相邻像素对集合（用于2D空间统计），以此构建经验分布的支持集。这一“样本到分布”的升维操作是整个框架的基石，使得高斯性的度量不再依赖逐点概率密度，而是基于样本的局部统计行为与典型高斯实现的对齐程度。

**模块二：成对MRF密度建模。** 在像素网格上假设成对马尔可夫随机场结构，将经验分布的联合密度函数因子化为节点势函数和边势函数的乘积形式：
$$p_{\hat{\mathbf{x}}}(\mathbf{x}) = \frac{1}{Z} \prod_{i \in \mathcal{V}} \psi_i(x_i) \prod_{(i,j) \in \mathcal{E}} \psi_{ij}(x_i, x_j)$$
这一因子化使得全局KL散度可以通过局部团簇的熵来近似，为后续的可微计算铺平道路。

**模块三：Bethe-Kikuchi KL逼近。** 将全局KL散度 $D_{\mathrm{KL}}(P_{\hat{\mathbf{x}}} \parallel G)$ 在团簇展开中截断至节点和边，得到两项可分别计算的熵项：
$$D_{\mathrm{KL}}(P_{\hat{\mathbf{x}}} \parallel G) \approx \underbrace{D_{\mathrm{KL}}(P_{\hat{\mathbf{x}}, S^{(2)}} \parallel G_{S^{(2)}})}_{\text{空间熵项}} + \gamma \underbrace{D_{\mathrm{KL}}(P_{\hat{\mathbf{x}}, S^{(1)}} \parallel G_{S^{(1)}})}_{\text{值熵项}}$$
其中空间熵项（Spatial Entropy Term）度量相邻像素对的2D联合经验分布与目标2D联合高斯之间的KL散度，捕获空间相关性；值熵项（Value Entropy Term）度量单像素值的1D边际分布与标准高斯之间的KL散度，约束一阶统计量。$\gamma$ 为Bethe校正因子，用于修正低分辨率直方图中因过分计数引入的估计偏差。

**模块四：可微熵估计。** 将每项KL散度进一步分解为交叉熵与差分熵之差：
$$D_{\mathrm{KL}}(P_{\hat{\mathbf{x}}} \parallel G) = H(P_{\hat{\mathbf{x}}}, G) - H(P_{\hat{\mathbf{x}}})$$
交叉熵 $H(P_{\hat{\mathbf{x}}}, G)$ 通过蒙特卡洛采样结合目标高斯的解析对数密度 $\log G(\mathbf{v}) = -\frac{d}{2}\log(2\pi) - \frac{1}{2}\|\mathbf{v}\|_2^2$ 进行估计；差分熵 $H(P_{\hat{\mathbf{x}}})$ 则通过高斯核密度估计（KDE）从样本点集近似连续密度后计算。整个估计过程对原始像素值 $\hat{\mathbf{x}}$ 端到端可微，支持基于梯度的优化。

**模块五：多尺度金字塔。** 为惩罚长程空间关联，对样本执行方差保持的下采样（$2\times2$ 均值池化后乘以 $\sqrt{n}$ 以保持方差），在多个分辨率层级上分别施加KL散度约束：
$$\mathcal{L}_{\mathrm{full}}(\hat{\mathbf{x}}) = \sum_{k=0}^{L-1} \alpha_k D_{\mathrm{KL}}(P_{\hat{\mathbf{x}}_k} \parallel G)$$
实际使用前三个尺度（1, 1/2, 1/4），使得局部成对约束通过金字塔结构延伸至全局范围，迫使样本在统计和视觉上更接近真实高斯噪声。

### 模块间依赖关系

经验分布构建（模块一）为后续所有模块提供数据基础；MRF建模（模块二）为KL逼近（模块三）提供因子化结构；Bethe-Kikuchi逼近（模块三）将不可解的全局KL散度转化为可计算的两项熵目标；可微熵估计（模块四）为这两项目标提供具体的数值实现；多尺度金字塔（模块五）在前四个模块的基础上扩展空间感受野。五个模块依次依赖，共同构成从单个样本到高斯典型集投影的完整计算通路。

### 与基线方法的本质区别

传统正则化方法（如VAE式KL先验、ReNO、ReNoise等）要么依赖逐点概率密度 $-\log G(\mathbf{x})$，要么仅匹配全局矩或频谱特性。EGNR 的根本不同在于：它将高斯性定义为样本局部统计量的经验分布与目标高斯之间的KL散度，并通过MRF团簇展开将其分解为1D边际熵、2D空间熵和多尺度项的可微组合。这一设计使得正则化器能够同时约束一阶值分布、二阶空间相关性和多尺度统计结构，从而更完整地刻画“成为高斯噪声”所需的分布性质。

### 3.1 从逐点概率到分布性高斯测度

传统方法将高斯性视为逐点概率密度（如 $-\log G(\mathbf{x})$），而EGNR的核心洞察在于：**高斯性应当被理解为一种分布性质，而非单个样本点的似然**。为此，方法将每个候选潜变量 $\hat{\mathbf{x}}$ 提升为由其统计量诱导的经验分布 $P_{\hat{\mathbf{x}}}$，并用该经验分布与目标高斯分布 $G$ 之间的KL散度作为高斯性测度：

$$\mathcal{D}_G(\hat{\mathbf{x}}) = D_{\mathrm{KL}}(P_{\hat{\mathbf{x}}} \parallel G) \tag{3}$$

这一形式化使得正则化器能够通过对齐样本的局部统计量与典型高斯实现来定义高斯性，而非依赖逐点似然。由此，噪声投影问题被转化为在数据保真度与高斯兼容性之间寻求平衡的优化：

$$\mathbf{x}^{\star} = \underset{\hat{\mathbf{x}}}{\arg\min}\; \lambda_S \mathcal{D}_S(\mathbf{x}_0, \hat{\mathbf{x}}) + \lambda_G \mathcal{D}_G(\hat{\mathbf{x}})$$

其中 $\mathcal{D}_S$ 为数据保真项（如 $\ell_2$ 距离），$\lambda_S$ 和 $\lambda_G$ 为平衡权重。

### 3.2 成对MRF建模与Bethe-Kikuchi逼近

直接计算高维经验分布与高斯分布之间的KL散度在计算上不可行。为解决这一问题，EGNR假设像素网格上的样本服从**成对马尔可夫随机场（MRF）**，将联合密度分解为节点势函数和边势函数的乘积：

$$p_{\hat{\mathbf{x}}}(\mathbf{x}) = \frac{1}{Z} \prod_{i \in \mathcal{V}} \psi_i(x_i) \prod_{(i,j) \in \mathcal{E}} \psi_{ij}(x_i, x_j) \tag{4}$$

其中 $\mathcal{V}$ 为像素节点集合，$\mathcal{E}$ 为相邻像素对构成的边集合，$Z$ 为配分函数。基于这一因子化形式，应用**Bethe-Kikuchi团簇展开**将全局KL散度近似为节点团簇（1D边际）和边团簇（2D联合）熵的加权和，得到最终的正则化目标：

$$D_{\mathrm{KL}}(P_{\hat{\mathbf{x}}} \parallel G) \approx \underbrace{D_{\mathrm{KL}}(P_{\hat{\mathbf{x}}, S^{(2)}} \parallel G_{S^{(2)}})}_{\text{空间熵项}} + \gamma \underbrace{D_{\mathrm{KL}}(P_{\hat{\mathbf{x}}, S^{(1)}} \parallel G_{S^{(1)}})}_{\text{值熵项}} \tag{5}$$

- **空间熵项（Spatial Entropy Term）**：度量相邻像素对的2D联合经验分布 $P_{\hat{\mathbf{x}}, S^{(2)}}$ 与目标2D联合高斯 $G_{S^{(2)}}$ 之间的相对熵，捕获空间相关性。
- **值熵项（Value Entropy Term）**：度量单个像素值的1D边际经验分布 $P_{\hat{\mathbf{x}}, S^{(1)}}$ 与标准高斯 $G_{S^{(1)}}$ 之间的相对熵，约束边缘统计。
- **Bethe校正因子 $\gamma$**：用于修正低分辨率直方图中因团簇重叠导致的过分计数问题，细化KL估计。

### 3.3 可微熵估计

为实现端到端优化，式(5)中的KL散度被分解为交叉熵与差分熵之差：

$$D_{\mathrm{KL}}(P_{\hat{\mathbf{x}}} \parallel G) = \underbrace{H(P_{\hat{\mathbf{x}}}, G)}_{\text{交叉熵}} - \underbrace{H(P_{\hat{\mathbf{x}}})}_{\text{差分熵}} \tag{6}$$

- **交叉熵 $H(P_{\hat{\mathbf{x}}}, G)$**：通过蒙特卡洛采样从 $P_{\hat{\mathbf{x}}}$ 中抽取样本点，并利用目标高斯分布的解析对数密度进行计算：

$$\log G(\mathbf{v}) = -\frac{d}{2}\log(2\pi) - \frac{1}{2}\|\mathbf{v}\|_2^2 \tag{7}$$

其中 $d$ 为维度（1D值熵项中 $d=1$，2D空间熵项中 $d=2$）。

- **差分熵 $H(P_{\hat{\mathbf{x}}})$**：由于 $P_{\hat{\mathbf{x}}}$ 没有解析形式，采用**高斯核密度估计（KDE）**从样本点集 $\{\mathbf{v}_j\}_{j=1}^{N}$ 逼近连续密度：

$$P_{\hat{\mathbf{x}}}(\mathbf{v}) \approx \hat{p}(\mathbf{v}) = \frac{1}{N}\sum_{j=1}^{N} \mathcal{K}_\sigma(\mathbf{v} - \mathbf{v}_j) \tag{9}$$

其中 $\mathcal{K}_\sigma$ 为带宽 $\sigma$ 的高斯核。差分熵进而通过 $\hat{p}(\mathbf{v})$ 的蒙特卡洛积分估计。整个公式链对原始像素值 $\hat{\mathbf{x}}$ 端到端可微。为降低计算复杂度，实际实现中使用固定分箱（如128个bins）计算成对距离，将复杂度从 $O(N^2)$ 降至 $O(N)$。

### 3.4 多尺度金字塔扩展

成对MRF假设仅捕获局部邻域的空间相关性。为惩罚长程关联，EGNR引入**多尺度优化方案**：对样本执行方差保持的下采样（$2\times2$ 块均值池化后乘以 $\sqrt{n}$ 以保持方差，其中 $n$ 为聚合像素数），并在多个分辨率层级上施加KL散度损失：

$$\mathcal{L}_{\mathrm{full}}(\hat{\mathbf{x}}) = \sum_{k=0}^{L-1} \alpha_k D_{\mathrm{KL}}(P_{\hat{\mathbf{x}}_k} \parallel G)$$

其中 $\hat{\mathbf{x}}_k$ 为第 $k$ 级下采样结果，$\alpha_k$ 为层级权重。实际使用前三层尺度（1, 1/2, 1/4），使得局部成对约束通过金字塔结构延伸为对全局统计特性的隐式约束，迫使样本在统计和视觉上更接近真实高斯噪声。

### 3.5 奖励引导生成中的正则化

在奖励对齐任务中，EGNR的正则化器与任务奖励 $R(\hat{\mathbf{x}})$ 联合优化，形成带约束的奖励最大化目标：

$$\mathbf{x}^* = \underset{\hat{\mathbf{x}}}{\arg\min} -R(\hat{\mathbf{x}}) + \lambda \mathcal{L}_{\mathrm{full}}(\hat{\mathbf{x}}) \tag{12}$$

其中 $\lambda$ 控制正则化强度。该目标在驱动噪声向高奖励方向优化的同时，通过 $\mathcal{L}_{\mathrm{full}}$ 将其约束在高斯典型集内，有效防止奖励攻击导致的分布外退化。

### 补充图表

![[assets/figures/papers/paper_list_l2628_https_openaccess_thecvf_com_content_CVPR2026_html_Chang_What_Is_It_Like/figures/001_Figure_1.jpg]]
*Figure 1: Value and Spatial Entropy Visualization. We show the 1D and 2D entropy as estimated with KDE for four different common inputs: image scaled to [-1,1], latent vector, a checkerboard texture, and a Gaussian noise*

## 实验与关键发现

### 核心瓶颈验证：噪声偏离高斯典型集

扩散模型在推理时对噪声潜变量进行优化（如奖励引导、图像反演等）会使其偏离真实高斯噪声的统计结构，导致模型被迫对分布外样本去噪，产生伪影、过饱和色彩和非自然斑块等脆性行为。EGNR 的核心假设是：**高斯性不应被视为逐点概率，而应作为分布性质来约束**。实验设计围绕三个层次验证该假设：（1）正则化器能否将任意输入投影回高斯典型集；（2）各组件对投影质量的贡献；（3）在下游奖励对齐任务中能否防止奖励攻击。

### 高斯噪声投影能力对比

Figure 3 展示了各基线方法将混合 50% 噪声的蛋糕图像潜变量优化为高斯噪声的能力。为确保公平，作者为每个基线单独调优了学习率，所有方法均优化 5000 步至收敛。结果显示：

![[assets/figures/papers/paper_list_l2628_https_openaccess_thecvf_com_content_CVPR2026_html_Chang_What_Is_It_Like/figures/004_Figure_3.jpg]]
*Figure 3: Baseline Comparisons. We evaluate baseline methods on optimizing an input latent towards Gaussian noise. The input is a cake image latent mixed with 50% noise to reflect typical use cases containing both noise and hidden structure. Rows display the input/optimized latent, multiscale 1D/2D densities, and the final generated image (A photo of a house). To ensure we isolate the loss function’s projection capability from optimizer-induced stochasticity, we individually tuned the learning rate (ω) for each baseline to a value that both stabilizes the noise and maximizes output quality. All methods were optimized for 5000 steps to ensure convergence. Our method yields a more accurate Gaussian noi...*

- **KL (VAE-style prior)** 和 **Pix2Pix-Zero** 仅施加逐点概率约束，无法有效消除图像结构残留。
- **ReNO** 和 **ReNoise** 通过范数约束或频谱匹配部分改善了统计特性，但在 2D 空间相关性上仍存在明显偏差。
- **EGNR** 产生的噪声样本在 1D 边际分布和 2D 空间联合分布上均与真实高斯噪声高度一致，其生成图像质量接近使用完美随机噪声的结果。

这验证了核心洞察：**逐点似然约束不足以刻画高斯性，必须通过经验分布的统计对齐来实现有效投影**。

### 消融实验：各组件的必要性

Figure 2 以棋盘格纹理为输入，系统消融了 EGNR 的四个组件（学习率 ω=0.05）：

1. **仅 1D 熵 + 1D 多尺度**：匹配一阶统计量无法产生高质量噪声，潜变量中仍保留明显的空间结构伪影，证明 **2D 熵对捕获空间相关性是不可或缺的**。
2. **加入 2D 熵**：显著改善了空间统计特性，但低分辨率直方图的 KL 估计存在偏差。
3. **加入 Bethe 校正**：细化了低分辨率下的 KL 估计，改善了投影质量——这归因于 Bethe-Kikuchi 展开中对边团簇的计数修正因子 γ。
4. **加入多尺度监督**：与任意配置结合均能进一步惩罚长程空间关联，迫使样本在统计和视觉上更接近真实高斯噪声。

**结论**：所有组件（1D 熵、2D 熵、Bethe 校正、多尺度）对最终高质量噪声投影都是必要的。损失仅施加于前三个尺度（1, 1/2, 1/4），1/8 尺度仅用于可视化。

### 奖励对齐任务：防止奖励攻击

在美学分数优化和亮度最小化两个任务上，EGNR 展示了其防止奖励攻击的关键能力（Figure 4, Table 2）。

![[assets/figures/papers/paper_list_l2628_https_openaccess_thecvf_com_content_CVPR2026_html_Chang_What_Is_It_Like/figures/005_Figure_4.jpg]]
*Figure 4: Reward Alignment Image Generation. We show some qualitative comparisons between various regularization techniques on two reward alignment tasks: aesthetic score optimization (top) and brightness minimization (bottom). By better preserving the Gaussian distribution, our optimized noise generates artifact-free images with neither over-saturated colors nor undesirable splotches*

![[assets/figures/papers/paper_list_l2628_https_openaccess_thecvf_com_content_CVPR2026_html_Chang_What_Is_It_Like/figures/006_Table_2.jpg]]
*Table 2: Aesthetic Image Generation (top) and Brightness Minimization Reward (bottom) with SDXL-Turbo [52]. We use a set of animal prompts from DDPO [6] in the format A photo of a/an [animal] (top) and A photo of a white [animal] (bottom)*

**美学分数优化（SDXL-Turbo, DDPO 动物提示集）**：
- 无正则化或弱正则化（KL, Pix2Pix-Zero）方法产生过饱和色彩和非自然纹理，美学分数虚高但视觉质量差。
- EGNR 在保持高美学分数（6.478）的同时，生成无伪影的自然图像，证明正则化器有效约束了优化过程停留在高斯典型集内。

**亮度最小化**：
- 无约束优化导致模型“作弊”——生成纯黑图像或噪声斑块。
- EGNR 实现了最低亮度（0.270）且无退化伪影，相比 ReNO、ReNoise 等方法优势明显。

这些结果验证了 Eq. (12) 中奖励与正则化平衡设计的有效性：`λ` 控制任务目标与高斯性约束的权衡，使优化轨迹不脱离扩散模型的训练分布。

### 计算开销

Table 1 报告了各方法的每步耗时。EGNR 的完整多尺度实现为 15.02 ms/步，虽高于简单 ℓ₂ 约束（约 2-5 ms），但低于 ReNO（约 25 ms）和 ReNoise（约 18 ms）。通过使用固定 bins（如 128 个）计算成对距离，可将 KDE 复杂度从 O(N²) 降至 O(N)，在 Table 1 中即采用此线性实现。

![[assets/figures/papers/paper_list_l2628_https_openaccess_thecvf_com_content_CVPR2026_html_Chang_What_Is_It_Like/figures/003_Table_1.jpg]]
*Table 1: Time/step (ms) for various baselines and our approach*

### 失败模式与局限

Figure 6 展示了典型失败案例：当从纯干净潜变量（“一只蝙蝠的照片”）开始优化且使用较低学习率时，成对 MRF 假设无法解析复杂的全局长程结构，导致去噪输出退化。作者指出，**在实际应用中，输入很少会如此远离目标噪声分布**，但这一局限揭示了当前 MRF 成对假设的根本边界——无法显式捕获非邻域的长程依赖关系。

![[assets/figures/papers/paper_list_l2628_https_openaccess_thecvf_com_content_CVPR2026_html_Chang_What_Is_It_Like/figures/008_Figure_6.jpg]]
*Figure 6: Failure Case. As shown on the left, when optimizing from a purely clean latent (A photo of a bat) with a lower learning rate, our multilevel MRF assumption may still fail to resolve complex, long-range structures (middle). This yields the degraded diffusion outputs seen on the right (A photo of a house). In practical applications, however, inputs are rarely this far removed from the target noise distribution*

此外，KDE 差分熵估计的计算开销虽经线性化优化，在高分辨率或实时场景中仍构成瓶颈；多尺度策略扩展了空间范围但未解决全局依赖建模问题。

## 定位与知识库关联

### 问题谱系：扩散模型中的噪声高斯性危机

扩散模型的核心假设是推理时的初始噪声严格服从独立同分布的高斯分布。然而，当对噪声潜变量进行优化以追求特定目标（如美学评分最大化、亮度最小化或图像反演）时，优化过程会不可逆地将噪声推离高斯典型集。这一现象的根本瓶颈在于：**推理时对扩散噪声潜变量进行优化会使其偏离真实高斯噪声的统计结构，导致模型被迫对分布外样本去噪，产生伪影、脆性行为和奖励攻击**。

现有方法对这一问题的应对策略可分为三类，但均存在根本性缺陷：

- **逐点概率约束**：以VAE风格的KL正则化（Kingma & Welling, 2013）为代表，通过惩罚单个像素值偏离零均值单位方差的程度来约束噪声。这种方法的致命缺陷在于将高斯性误解为逐点属性——一个完全打乱的棋盘纹理可以在逐点统计上完美匹配高斯分布，却与真实高斯噪声的统计结构相去甚远（Figure 1提供了直观证据）。

- **范数与频谱匹配**：**ReNO**（Eyring et al., 2024）和**ReNoise**（Garibi et al., ECCV 2024）等方法通过约束ℓ₂距离或强制频谱特性来维持噪声质量。这些方法虽然比纯逐点约束更进一步，但本质上仍是在匹配全局矩或频率特性，无法捕获决定生成质量的关键局部空间依赖关系。

- **后处理投影**：**Pix2Pix-Zero**（Parmar et al., 2023）和**Hwang et al.**（2025）等方法试图在优化后将噪声投影回高斯分布，但这种事后补救无法在优化过程中防止噪声偏离典型集，往往导致生成质量与任务目标之间的两难权衡。

### 核心洞察：从点到分布的范式转换

本文提出的**基于熵的高斯噪声正则化**（Entropy-based Gaussian Noise Regularization, EGNR）的根本突破在于一个认识论的转换：**不应将高斯性视为逐点概率，而应看作分布性质**。具体而言，该方法将单个噪声样本提升为其局部统计量诱导的经验分布，并度量该经验分布与目标高斯分布之间的KL散度——而非计算单个样本点的似然。

这一转换解决了前序方法的核心矛盾：逐点约束无法区分“统计上高斯”与“逐点高斯”之间的本质差异。一个样本可以在每个像素值上都接近零均值，却呈现出完全非高斯的空间结构（如棋盘纹理）；反之，一个真实的高斯噪声样本必然同时满足1D边际分布和2D空间关联的统计特征。EGNR通过同时约束这两个维度，实现了对高斯性的完整刻画。

### 技术谱系：从MRF到Bethe-Kikuchi逼近

EGNR的技术实现建立在对统计物理和概率图模型经典工具的创造性应用之上：

- **成对马尔可夫随机场（MRF）建模**：将噪声样本的像素网格建模为成对MRF，其中节点势函数捕获单像素值的1D分布，边势函数捕获相邻像素对的2D联合分布。这一建模选择并非任意——它精确对应了高斯噪声的两个关键统计特征：边际正态性和空间独立性。

- **Bethe-Kikuchi团簇展开**：直接计算经验分布与高斯分布之间的全局KL散度在计算上不可行。该方法通过限制团簇展开到节点和边层级，将KL散度近似分解为**空间熵项**（2D Spatial Entropy Term）和**值熵项**（1D Value Entropy Term）的加权和，并通过Bethe修正因子γ处理低分辨率直方图中的过分计数问题。这一逼近在保持计算可处理性的同时，捕获了决定生成质量的关键统计结构。

- **可微熵估计**：通过将KL散度分解为交叉熵（对目标高斯的解析形式进行蒙特卡洛积分）和差分熵（通过核密度估计从样本点集近似），整个正则化器实现了端到端可微。这一设计使得正则化项可以直接嵌入任意基于梯度的噪声优化流程。

- **多尺度金字塔扩展**：成对MRF假设天然局限于局部邻域。为惩罚长程空间关联，该方法在多个分辨率层级上施加正则化——通过对噪声样本执行方差保持的下采样（均值池化后缩放√n），将局部约束延伸为对全局统计结构的控制。实验表明，前三个尺度（1, 1/2, 1/4）已足以实现有效的高斯化投影。

### 与基线方法的本质差异

EGNR与现有基线方法的差异不仅是技术路径的不同，更是对“什么是高斯性”这一根本问题的不同回答：

| 方法 | 高斯性定义 | 约束粒度 | 空间依赖处理 |
|------|-----------|---------|------------|
| KL先验（Kingma & Welling, 2013） | 逐点概率密度 | 单像素 | 无 |
| ReNO（Eyring et al., 2024） | ℓ₂范数约束 | 全局向量 | 无 |
| ReNoise（Garibi et al., ECCV 2024） | 频谱匹配 | 全局频率 | 隐式 |
| **EGNR（本文）** | **经验分布KL散度** | **1D边际+2D空间+多尺度** | **显式成对MRF** |

这一差异在实验中得到直接验证：Figure 2的消融实验表明，仅使用1D熵（匹配一阶统计量）无法产生高质量噪声——2D空间熵项对于捕获空间相关性是不可或缺的。Bethe修正细化了低分辨率直方图的KL估计，而多尺度监督与任何配置结合都能进一步改善投影质量。所有组件对于最终的高质量噪声投影都是必要的。

### 适用边界与局限

尽管EGNR在多个任务上展现出显著优势，其适用边界和局限同样明确：

**计算开销**：差分熵的核密度估计（KDE）计算开销为O(N²)，即使通过固定bin集合简化至O(N)，每步仍需约15ms（Table 1），显著高于ReNO等轻量级方法。这一开销限制了其在高分辨率或实时场景中的应用。

**长程结构失效**：当成对MRF假设遭遇严重偏离高斯噪声的输入时（如干净图像潜变量），方法可能无法解析复杂的非局部结构。Figure 6的失败案例明确展示了这一局限：从纯干净潜变量出发优化时，即使使用较低学习率，多层级MRF假设仍可能无法消除长程结构，导致去噪输出退化。论文坦承，在实际应用中输入很少如此远离目标噪声分布，但这一边界值得注意。

**全局依赖的缺失**：多尺度策略虽然扩展了空间范围，但本质上仍是局部约束的层级叠加，未能显式捕获全局非邻域的长程依赖关系。这限制了方法在需要精确全局结构控制的任务（如严格的图像反演）中的保真度。

### 开放问题与未来方向

论文揭示的开放问题指向了该方法进一步发展的关键方向：

1. **高效熵估计**：如何设计计算复杂度更低的差分熵估计方法（例如利用随机投影或神经估计器），是降低EGNR应用门槛的核心挑战。

2. **超越成对依赖**：如何扩展现有MRF成对假设以捕获高阶或非局部依赖，而又不显著增加计算复杂度，是提升方法对复杂结构处理能力的关键。

3. **模型无关反演的深化**：Figure 5展示的模型无关图像到噪声匹配（使用Pearson相关系数作为奖励，无需查询扩散模型）已初步展示了跨模型迁移能力，但将其发展为严格且高保真的图像反演技术仍是开放挑战。

4. **高维扩展**：在更高维度噪声或条件生成任务中，正则化器是否仍然有效，需要进一步验证。

### 知识库定位

EGNR在扩散模型知识库中的定位可概括为：**第一个将高斯性从逐点属性重新定义为分布性质，并通过统计物理工具（MRF + Bethe-Kikuchi）实现可微正则化的方法**。它桥接了三个通常独立的领域——扩散模型的噪声优化、概率图模型的变分推断、以及信息论中的熵估计——为解决奖励攻击和分布外生成问题提供了新的理论框架。

该方法不替代现有的扩散采样策略或奖励设计方法，而是作为一个即插即用的正则化模块，可与任何基于梯度的噪声优化流程结合。其在美学优化和亮度最小化任务上的定量优势（Table 2：美学分数6.478，亮度0.270）和定性优势（Figure 4：无伪影、无过饱和、无异常色块）表明，保持噪声的高斯性是实现稳健生成质量的关键——这一洞察可能对扩散模型的设计哲学产生深远影响。

## 原文 PDF

![[paperPDFs/CVPR_2026/What_Is_It_Like_to_Be_a_Noise_An_Entropy_based_Gaussian_Noise_Regularization_for_Diffusion_Models.pdf]]
