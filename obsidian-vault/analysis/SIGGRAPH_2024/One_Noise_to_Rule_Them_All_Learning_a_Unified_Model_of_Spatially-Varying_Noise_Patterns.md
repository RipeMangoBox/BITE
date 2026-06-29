---
title: "One Noise to Rule Them All: Learning a Unified Model of Spatially-Varying Noise Patterns"
type: paper
paper_level: A
venue: SIGGRAPH
year: 2024
pdf_ref: paperPDFs/SIGGRAPH_2024/One_Noise_to_Rule_Them_All_Learning_a_Unified_Model_of_Spatially_Varying_Noise_Patterns.pdf
project_link: null
code_link: null
aliases:
- UNDON
- ONRTALUMSVNP
tags:
- SIGGRAPH_2024
- topic/benchmarks_datasets_evaluation
core_operator: 通过CutMix数据增强在训练时模拟空间变化的局部条件信号，结合SPADE空间自适应条件化模块，迫使去噪扩散模型学习将局部条件与生成纹理的局部区域绑定。
primary_logic: 使用CutMix将不同噪声样本及其对应的条件嵌入随机裁剪拼贴，构造具有空间变化条件的人工训练样本；结合球面正则化的类别嵌入和SPADE条件架构，使单一DDPM能够在没有空间变化训练数据的情况下，生成多种噪声类型的平滑空间混合，并支持通过可解释参数和随机种子进行控制。
claims:
- 移除CutMix数据增强会严重削弱模型对局部条件信号的响应能力，导致无法生成具有非均匀特性的噪声图。
- 提出的方法在18种噪声类型上的平均FID为20.9，远优于PSGAN的99.2。
- 模型能够生成具有空间变化特性的噪声图，即使训练数据中不包含此类样本。
- Custom noise dataset (18 noise types from Adobe Substance 3D Designer) 上 FID (Frechet Inception Distance) = mean 20.9, median 13.1
---

# One Noise to Rule Them All: Learning a Unified Model of Spatially-Varying Noise Patterns

> [!tip] 核心洞察
> 使用CutMix将不同噪声样本及其对应的条件嵌入随机裁剪拼贴，构造具有空间变化条件的人工训练样本；结合球面正则化的类别嵌入和SPADE条件架构，使单一DDPM能够在没有空间变化训练数据的情况下，生成多种噪声类型的平滑空间混合，并支持通过可解释参数和随机种子进行控制。

| 字段 | 内容 |
|------|------|
| 中文题名 | 一噪统天下：学习空间变化噪声模式的统一模型 |
| 英文题名 | One Noise to Rule Them All: Learning a Unified Model of Spatially-Varying Noise Patterns |
| 会议/期刊 | SIGGRAPH 2024 |
| Links | [paper](https://armanmaesumi.github.io/onenoise/) |
| Topic | #topic/benchmarks_datasets_evaluation |
| Method | Unified Noise DDPM (One Noise) |
| Dataset | Custom noise dataset |

> [!tip] 效果简介
> - Custom noise dataset (18 noise types from Adobe Substance 3D Designer) 上，FID (Frechet Inception Distance) mean 20.9, median 13.1 vs PSGAN: mean 99.2, median 87.5 (mean 78.3 lower)。

## 概要

传统程序化噪声生成依赖多种离散算法，设计者须提前选定噪声类型，无法实现不同噪声特性在空间上的平滑过渡；常用的Alpha混合会产生叠影和不自然的过渡。本文提出**Unified Noise DDPM (One Noise)**，以单一条件去噪扩散概率模型（DDPM）统一多种噪声的生成。核心思路是：通过**CutMix数据增强**在训练时随机拼贴不同噪声样本及其条件嵌入，构造具有空间变化条件的人工训练样本；配合**SPADE空间自适应条件化模块**和**球面正则化**的类别嵌入，迫使模型将局部条件信号与生成纹理的局部区域绑定。在推理时，只需构建任意空间变化的条件网格，即可生成多种噪声类型的平滑空间混合，并支持通过可解释参数和随机种子进行控制。

在18种噪声类型上的实验表明，本方法平均FID为**20.9**（中位数13.1），远优于PSGAN的99.2（中位数87.5）。模型还能生成训练数据中不存在的空间变化噪声图，支持超出训练分辨率的任意尺寸合成和无缝平铺。该方法将离散的噪声生成器统一为单一可微模型，为程序化材质设计中的噪声节点提供了连续可优化的生成先验。

## 核心方法与创新机理

### 问题瓶颈：从离散生成到统一建模

传统程序化噪声生成器由多种独立算法构成——Perlin噪声、Voronoi噪声、细胞噪声等各有独立的参数空间和生成逻辑。设计者必须在创作前选定噪声类型，一旦确定便无法在同一纹理中实现不同噪声特性在空间上的平滑过渡。实践中常用的Alpha混合方案将两种噪声图像按透明度叠加，但这仅作用于像素层面，会产生重叠的视觉特征、不一致的特征不透明度，以及缺乏语义连贯性的过渡（Fig. 2），无法实现噪声内在特性（如尺度、扭曲、波纹等）的自然演变。

![[assets/figures/papers/paper_list_l28_https_armanmaesumi_github_io_onenoise/figures/002_Figure_2.jpg]]
*Figure 2: Our model produces noise pa!erns whose characteristics (i.e. scale, ripples, distortion, etc.) interpolate naturally, creating seamless and coherent transitions. By contrast, traditional alpha-blending results in images with overlapping features, inconsistent feature opacity, and a lack of sensible transitions between the noise characteristics*

这一瓶颈的根源在于：传统方法将噪声类型视为离散的、互不相通的生成模式，缺乏一个统一的连续表示空间来编码和插值不同噪声的结构特征。因此，核心挑战在于构建一个既能覆盖多种噪声类型的生成分布，又能响应空间局部条件信号的单一模型。

### 核心洞察：CutMix驱动的空间条件绑定

本文的核心洞察是：通过在训练阶段构造具有空间变化条件的人工样本，迫使去噪扩散模型（DDPM）学习将局部条件信号与生成纹理的局部区域严格绑定。具体而言，采用**CutMix数据增强**将不同噪声样本及其对应的条件嵌入随机裁剪拼贴，形成一张训练图像同时包含多种噪声类型/参数的区域（Fig. 3）；结合**SPADE空间自适应条件化模块**，使U-Net的去噪过程在每个空间位置仅响应其对应的局部条件。这一机制使得模型在推理时即使面对从未见过的空间变化条件网格，也能生成具有对应局部特性的噪声图（Fig. 4），而训练数据本身并不包含任何空间变化样本（Fig. 5）。

![[assets/figures/papers/paper_list_l28_https_armanmaesumi_github_io_onenoise/figures/003_Figure_3.jpg]]
*Figure 3: Our DDPM is trained using CutMix data augmentation. We first transform the current data sample (highlighted in blue) by cu!ing and patching together a set of other random samples from the dataset, resulting in a training image x0. The noise parameters for each image patch are passed to an MLP, which projects the parameter sets into an embedding space that encodes both the noise type (class) and the noise parameters. The resulting feature vectors are tiled to form a feature grid, which is used as a conditioning signal in the U-Net’s SPADE blocks, as outlined in Section 3.1*

![[assets/figures/papers/paper_list_l28_https_armanmaesumi_github_io_onenoise/figures/004_Figure_4.jpg]]
*Figure 4: At inference time, we query our network using artificially constructed feature grids, enabling a flexible way to synthesize spatially-varying noise pa!erns. Here we embed four sets of noise parameters, pictorially shown as one of four colors. We blend the feature vectors using bilinear interpolation, creating a smoothly-varying feature grid, which our U-Net is able to transform into a Voronoi noise pa!ern with non-uniform scale and distortion characteristics*

### 三个关键 Changed Slots

| 维度 | 基线方案 | 本文方案 | 因果作用 |
|------|---------|---------|---------|
| **噪声生成模型** | 多种独立算法/离散生成器 | 单一条件DDPM | 将离散的噪声类型统一到连续的扩散生成空间 |
| **空间变化处理** | 无或Alpha像素混合 | SPADE空间自适应条件化 + CutMix训练 | 建立局部条件到局部纹理的因果绑定，实现特性级插值 |
| **类别嵌入正则化** | 无 | 球面正则化（spherical regularization） | 将类别嵌入约束在球面上，改善类别间插值的平滑性 |

### 方法框架与模块顺序

整个方法由训练和推理两条路径组成，核心模块的因果关系链如下：

#### 1. 条件信号构建（Class Embedding MLP + Parameter MLP）

给定一个噪声样本，其条件信号由两个向量组成：
- **类别嵌入** $\mathbf{f}_c$：通过可学习的嵌入矩阵将噪声类型（共18类，如Gaussian、Voronoi、Damascus Steel等）编码为$d$维向量。
- **参数向量** $\mathbf{f}_p$：将连续噪声参数（如尺度、扭曲强度、密度等）通过Parameter MLP映射为特征向量。

两者拼接后通过一个共享的MLP投影到统一的嵌入空间，形成该噪声样本的条件特征向量。

#### 2. 球面正则化（Spherical Regularization）

为改善类别嵌入空间的几何结构，引入球面正则化损失：

$$\mathcal{L}_{\mathrm{reg}} = \frac{1}{|C|} \sum_{c \in C} ( \|\mathbf{f}_c\|_2^2 - T_d^2 )^2$$

其中目标范数$T_d^2$为$d$维标准高斯向量的期望平方范数：

$$T_d^n := \mathbb{E}_{\mathbf{f}_c \sim \mathcal{N}^d(0,\mathbf{I}_d)} \left[ \|\mathbf{f}_c\|_2^n \right] = 2^{n/2} \frac{\Gamma((d+n)/2)}{\Gamma(d/2)}$$

该正则化将类别嵌入约束在半径为$T_d$的球面附近，使得类别间的测地线插值更自然，减少过渡区域的伪影（Fig. 15 验证了这一效果）。

#### 3. 特征网格平铺（Feature Grid Tiling）

将条件特征向量在空间上平铺为与噪声图像分辨率一致的特征网格$\mathbf{Z} \in \mathbb{R}^{H \times W \times D}$。在标准训练中，整个网格由单一条件向量重复填充；在CutMix增强训练中，不同空间区域对应不同的条件向量（详见第4步）。

#### 4. CutMix数据增强（训练路径核心）

训练时以概率0.5应用CutMix增强（Fig. 3）：

- 从数据集中随机采样1至4个辅助噪声样本；
- 对每个辅助样本随机裁剪矩形区域，并施加随机旋转$\theta \in \{0°, 90°, 180°, 270°\}$；
- 将这些裁剪区域拼贴到当前训练样本上，同时将对应区域的条件特征向量替换为辅助样本的条件向量；
- 形成一张包含多种噪声类型/参数区域的合成训练图像$\mathbf{x}_0$及其对应的空间变化条件网格。

这一操作的关键在于：它迫使U-Net在去噪过程中必须依赖局部条件信号来区分不同区域的噪声特性，从而学习到条件信号与生成纹理之间的空间局部绑定关系。消融实验（Fig. 13）证实，移除CutMix后U-Net完全无法处理非均匀条件信号——例如在类别混合场景中，galvanic噪声模式会完全消失。

#### 5. SPADE条件化U-Net去噪器

U-Net的去噪过程在每个ResNet块中同时接收三种条件信号：

- **时间步条件**：通过标量$\gamma_1(t), \beta_1(t)$对Group Normalization后的特征进行全局调制；
- **SPADE空间条件**：通过特征网格$\mathbf{Z}$预测的逐像素尺度$\gamma_2(\mathbf{Z})$和偏移$\beta_2(\mathbf{Z})$进行空间自适应调制。

组合形式为：

$$\gamma_2(\mathbf{Z}) \odot ( \gamma_1(t) \cdot \mathrm{GroupNorm}(\mathbf{h}) + \beta_1(t) ) + \beta_2(\mathbf{Z})$$

其中SPADE的核心操作定义为：

$$S(\mathbf{h}, \mathbf{F}) = \gamma(\mathbf{F}) \odot \mathrm{GroupNorm}(\mathbf{h}) + \beta(\mathbf{F})$$

Group Normalization对通道组$g$进行归一化：

$$\mathrm{GroupNorm}_g(\mathbf{h}) = \frac{\mathbf{h}_g - \mu_g}{\sqrt{\sigma_g^2 + \epsilon}}$$

SPADE模块的因果作用在于：$\gamma(\mathbf{F})$和$\beta(\mathbf{F})$是从条件特征网格$\mathbf{F}$通过卷积层预测得到的空间变化调制参数，使得U-Net的中间层激活在每个空间位置都受到对应局部条件的独立调控。这建立了从“条件网格空间变化”到“生成纹理空间变化”的直接映射通道。

#### 6. 训练目标

整体训练损失为噪声预测损失与球面正则化项的加权组合：

$$\mathcal{L} = \mathbb{E}_{\epsilon \sim \mathcal{N}(0,1), t \sim \mathcal{U}(0,1)} \| \epsilon - \epsilon_\theta(\mathbf{x}_t, t, \mathbf{f}_c, \mathbf{f}_p) \|^2 + \lambda \mathcal{L}_{\mathrm{reg}}$$

其中$\epsilon_\theta$为U-Net预测的噪声，$\mathbf{x}_t$为加噪后的图像，$\lambda$控制正则化强度。

#### 7. 推理路径

推理时（Fig. 4），用户可以自由构造空间变化的条件网格：

- 在画布上定义多个“条件锚点”，每个锚点指定一种噪声类型及其参数；
- 通过双线性插值生成平滑过渡的特征网格；
- 将该网格输入训练好的DDPM，使用DDIM采样器在30步内生成最终噪声图像。

由于CutMix训练已使U-Net学会了将局部条件绑定到局部纹理，推理时即使面对从未见过的条件网格配置，模型也能生成具有对应局部特性的噪声图——例如Voronoi噪声的尺度从左到右逐渐增大，同时扭曲特性从弱到强演变（Fig. 4, Fig. 7）。

### 因果链路总结

**CutMix构造空间变化训练样本 → SPADE提供空间自适应条件注入通道 → 球面正则化优化类别嵌入几何 → 训练迫使局部条件-局部纹理绑定 → 推理时任意条件网格均可生成对应空间变化噪声。**

这一因果链的核心在于CutMix与SPADE的协同：CutMix创造了“局部条件多样化”的训练信号需求，SPADE提供了满足该需求的架构能力。缺少任一环节，模型要么无法接收空间变化条件（无SPADE），要么无法学会响应空间变化条件（无CutMix）。

![[assets/figures/papers/paper_list_l28_https_armanmaesumi_github_io_onenoise/figures/013_Figure_12.jpg]]
*Figure 12: Our model is able to produce seamless tileable images, as shown by the green regions, which are tiled into 2-by-2 noise maps. We also support synthesizing noise on an arbitrary canvas, avoiding noticeable repeated pa!erns, which is a common problem with tileable textures*

## 实验与关键发现

### 主结果：噪声生成质量

模型在来自Adobe Substance 3D Designer的18种噪声类型数据集上进行评估，以FID（Fréchet Inception Distance）作为主要定量指标。**Unified Noise DDPM**取得了平均FID 20.9、中位数FID 13.1的成绩，而基线方法**PSGAN**（Bergmann et al., 2017）的对应值为平均99.2、中位数87.5，本方法将平均FID降低了78.3。这一巨大差距表明，基于条件扩散模型的生成范式在捕捉多样噪声纹理分布方面，远优于基于神经纹理合成的PSGAN方法。

定性对比（Fig. 6）进一步揭示了PSGAN和**Image Melding**（Darabi et al., 2012）的典型失效模式：PSGAN生成的噪声纹理出现各向异性条纹伪影（如水平拖痕），且视觉细节重复明显；Image Melding在填充过渡区域时产生模糊和不自然的拼接痕迹。相比之下，本方法能在整个画布上合成新颖的噪声细节，同时保持平滑的语义过渡。

![[assets/figures/papers/paper_list_l28_https_armanmaesumi_github_io_onenoise/figures/006_Figure_6.jpg]]
*Figure 6: We compare our method to a neural texture synthesizer, PSGAN [2017], as well as a non-parametric texture blending method, Image Melding [2012]. In the case of Image Melding, the first and last quarter of the image are given, only the remaining interior region is filled in. Both prior methods su"er from artifacts and repeated visual details, whereas our method is able to blend smoothly while synthesizing novel details throughout the canvas. We note that PSGAN produces anisotropic features that are not characteristic of the data distribution (e.g. horizontal streaks in bo!om le# example)*

### 消融实验：CutMix数据增强的决定性作用

CutMix数据增强是模型获得空间变化响应能力的关键机制。消融实验（Fig. 13）表明：

![[assets/figures/papers/paper_list_l28_https_armanmaesumi_github_io_onenoise/figures/012_Figure_13.jpg]]
*Figure 13: Ablation study of CutMix data augmentation. Without CutMix, the U-Net fails to resolve noise maps that contain non-uniform characteristics. For instance, in row 3 of the class blending panel, the network cannot adequately blend between noise classes, causing the galvanic noise pa!ern to disappear entirely. We include models with one and four applications of CutMix, as detailed in Section 5. Finally, the uniform panel (no blending) acts as a control group – as expected, all outputs are similar*

- **移除CutMix后**，U-Net完全无法处理非均匀条件信号。在类别混合场景中，当特征网格从一种噪声类型平滑过渡到另一种时，无CutMix的模型表现出“类别消失”现象——例如电镀噪声（galvanic noise）图案在过渡区域完全消失，仅剩另一种噪声的特性。这说明模型在没有CutMix训练的情况下，学习到的条件映射是全局性的，缺乏对局部条件信号的响应能力。
- **CutMix补丁数量**：使用1个补丁和4个补丁的效果整体相似，但4个补丁在某些情况下能产生更平滑的噪声特性过渡。这一发现表明，增加CutMix的多样性对模型的局部条件解耦有边际增益，但即使最简配置（1个补丁）也足以建立基本的空间变化响应机制。
- **对照组验证**：在均匀条件（无混合）的对照组中，所有配置的输出质量接近，排除了CutMix本身对生成质量产生负面影响的可能。

### 球面正则化的插值质量影响

类别嵌入的球面正则化（spherical regularization）对噪声类型间的插值质量有显著改善（Fig. 15 vs Fig. 14）。正则化项 $\mathcal{L}_{\mathrm{reg}} = \frac{1}{|C|} \sum_{c \in C} ( \|\mathbf{f}_c\|_2^2 - T_d^2 )^2$ 强制类别嵌入分布在球面上，使得类别间的插值路径保持在嵌入空间的高密度区域。实验显示，经过球面正则化后，噪声类型间的过渡更加自然，基本消除了Fig. 14中展示的过渡区域伪影。这一结果验证了嵌入空间几何结构对生成质量的重要性：当嵌入向量范数不受约束时，类别间的线性插值可能穿过嵌入空间的低密度区域，导致解码器产生不自然的纹理。

### 推理效率

在推理速度方面，模型在单张NVIDIA RTX 3090 GPU上以全精度（fp32）进行256×256分辨率生成时，每秒可执行80个扩散步骤。使用DDIM采样器只需30步即可完成一次生成，这意味着单次噪声图像生成的时间约为0.375秒，对于交互式材质编辑场景具有实用价值。

### 高分辨率与可平铺能力

模型展现出超越训练分辨率的生成能力。Fig. 10展示了2048×2048像素的大马士革钢噪声（Damascus steel）图案，包含丰富的精细细节，且通过单次扩散过程生成。此外，模型支持无缝平铺（Fig. 12），能够生成可平铺的噪声纹理，同时支持在任意画布上合成噪声而避免明显的重复图案——这是传统平铺纹理的常见问题。

### 失败模式与适用边界

尽管模型在多数场景下表现优异，实验揭示了以下明确的失败模式和边界条件：

1. **噪声类型对的不兼容性**（Fig. 14）：并非所有噪声类型对都能平滑插值。当两种噪声的几何特征差异过大时——例如一种噪声具有明显的方向性结构而另一种是完全随机的——过渡区域会出现模糊或视觉上的不自然伪影。这表明模型的插值能力受限于训练数据中噪声类型之间的语义距离，嵌入空间的全局几何结构无法完全弥合所有类型间的鸿沟。

2. **低密度模态的生成退化**：扩散模型对数据分布中的低密度模态捕捉不佳。部分噪声函数的参数空间中存在低密度区域（例如极端参数值对应的噪声样本在训练集中较少），模型在这些区域的生成质量下降。这是扩散模型固有的分布覆盖偏差，而非本方法特有的缺陷。

3. **确定性图案的不兼容性**：当前模型无法包含确定性图案生成器（如砖块拼贴、规则网格纹理），因为确定性特性与扩散模型的随机生成本质存在根本性不匹配。这一边界限制了模型统一“所有”程序化纹理的愿景，使其适用范围主要局限在随机噪声类纹理。

4. **逆材质图优化的概念验证状态**：虽然模型在逆过程式材质设计应用（Fig. 8, Fig. 9）中展示了潜力——能够作为噪声函数空间的先验辅助恢复目标照片中的非平凡图案，并支持优化后的材质图编辑——但该应用仍处于概念验证阶段，尚未在实际生产环境中进行大规模验证。优化结果依赖于MATch（Shi et al., 2020）的材质图框架，其适用范围受限于该框架支持的噪声节点类型。

### 实验公平性说明

训练数据来源于Adobe Substance 3D Designer的专有噪声函数。虽然模型代码已开源，但原始噪声数据集可能受Adobe的许可证限制，复现完整训练流程可能需要获取相应的商业软件授权。

## 定位与知识库关联

本文的核心贡献在于改变了**噪声生成模型**这一 slot：将传统图形学中由多个离散算法（Perlin、Voronoi、分形等）组成的噪声生成器，替换为一个**单一的条件去噪扩散概率模型（Unified Noise DDPM）**。这一替换并非单纯的“用神经网络替代程序化函数”，而是从根本上改变了噪声生成的控制范式——从“选择算法并调参”变为“在连续嵌入空间中插值与采样”。

### 相对已有方法的本质差异

与现有纹理合成/混合方法相比，本文改变的关键 slot 是**空间变化处理机制**：

- **PSGAN**（Bergmann et al., 2017）作为神经纹理合成基线，其本质是在像素空间或特征空间进行纹理的渐进式生成与混合，但缺乏对噪声类型语义的显式建模，产生的纹理常带有各向异性伪影，且无法在语义层面实现不同噪声特性的平滑过渡。本文方法在 FID 指标上达到均值 20.9，而 PSGAN 为 99.2，差距达 78.3，属于压倒性优势（Appendix Table 2）。

- **Image Melding**（Darabi et al., 2012）是非参数纹理混合方法，需要给定源图像的边界区域作为约束，仅填充中间过渡区域。该方法容易产生重复视觉细节和拼接伪影，而本文模型可在整个画布上合成新颖细节，无需源图像边界约束。

- **传统 Alpha 混合**是最直接的噪声融合手段，但其本质是对已生成像素的线性叠加，导致特征重叠、透明度不一致，且缺乏语义连贯的过渡。本文通过 SPADE 空间自适应条件化模块，在特征层面进行条件调制，使噪声特性（如尺度、扭曲、波纹）自然插值，而非像素层面的简单叠加。

- **MATch**（Shi et al., 2020）是可微材质图库，用于逆过程式材质设计。本文方法在该应用中充当噪声函数的可微先验，改善了 MATch 对目标照片中复杂噪声图案的恢复能力（Fig. 8），但这一应用仍处于概念验证阶段。

### 知识库挂载点

本文在知识库中的核心挂载点位于**“生成模型 × 程序化纹理”**交叉领域，具体可分解为三个层面：

1. **条件扩散模型的架构创新**：在标准 DDPM（Ho et al., 2020）的 U-Net 基础上，本文引入了 SPADE 空间自适应条件化（Park et al., 2019），将全局条件信号替换为**空间变化的特征网格**。这一改造使得去噪过程能够感知条件信号的空间位置差异，是实现空间变化噪声生成的关键架构支撑。

2. **CutMix 数据增强的创造性迁移**：CutMix（Yun et al., 2019）最初为图像分类任务设计，本文将其迁移到生成模型的训练中，通过随机拼贴不同噪声样本及其对应条件嵌入，**强制模型学习局部条件与局部纹理的绑定关系**。这一训练策略是模型能够在推理时响应非均匀条件信号的根本原因——消融实验（Fig. 13）证实，移除 CutMix 后 U-Net 无法处理非均匀条件，噪声特性变得模糊甚至消失。

3. **球面正则化的嵌入空间设计**：类别嵌入的球面正则化（Section 3.1.1）使得不同噪声类型的嵌入向量分布在超球面上，显著改善了类别间插值的质量，减少了过渡区域的伪影（Fig. 15）。这一设计为连续嵌入空间中的语义插值提供了几何约束。

### 适用边界与局限

本文方法的适用边界受以下因素制约：

- **噪声类型间的可混合性有限**：并非所有噪声类型对都能平滑插值。当两种噪声的几何特征差异过大时（如高度结构化的 Damascus 钢纹与随机纤维噪声），过渡区域会出现模糊或视觉伪影（Fig. 14）。这表明模型学习到的嵌入空间并非对所有噪声类型对都具有语义上的平滑流形。

- **确定性图案生成器的缺失**：当前模型无法包含确定性图案生成器（如砖块拼贴），因为扩散模型的随机本质与确定性输出需求存在根本性矛盾。这限制了模型在需要精确可重复图案的场景中的应用。

- **低密度模态的生成质量下降**：扩散模型对训练数据分布中的低密度区域捕捉不佳，部分噪声函数的极端参数区域生成质量会下降。这是扩散模型的内在局限，而非本文方法的特有问题。

- **逆材质设计的规模化待验证**：尽管展示了与 MATch 结合的优化结果，但该应用尚未在实际生产环境中大规模验证，其鲁棒性和泛化性仍需进一步评估。

### 后续启发

本文为后续研究提供了以下方向性启发：

1. **统一纹理生成模型的可能性**：若能解决确定性图案的建模问题（例如引入离散潜变量或混合模型），有望将更多程序化纹理类型纳入统一框架，真正实现“一模型统天下”。

2. **交互式噪声设计的新范式**：推理时通过人工构造特征网格即可控制空间变化噪声（Fig. 4），这暗示了更自然的交互方式——例如在画布上“滴落”噪声点并通过扩散方程传播，实现直观的噪声纹理创作。

3. **扩散模型在图形学管线中的深度集成**：将模型蒸馏为单步扩散模型，可使其在材质图的每个噪声节点中高效使用，进而实现整个材质图结构的端到端连续优化，这将是过程式材质设计工具的重要进化方向。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2024/One_Noise_to_Rule_Them_All_Learning_a_Unified_Model_of_Spatially_Varying_Noise_Patterns.pdf]]