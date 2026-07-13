---
title: Multi-view Consistent 3D Gaussian Head Avatars 'without' Multi-view Generation
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Multi_view_Consistent_3D_Gaussian_Head_Avatars_without_Multi_view_Generation.pdf
project_link: "https://humansensinglab.github.io/MVCHead/"
code_link: null
aliases:
- MVC3GHAWMVG
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 利用HiBiSS双向状态扫描对齐多视图不一致的水平和垂直主轴，以及SE(3)多视图评判器显式奖励跨视图像素对齐，从而在不依赖多视图数据的情况下诱导多视图一致性。
primary_logic: 两个关键洞察：(1) 头部化身的多视图不一致主要表现为水平（偏航引起的左右位移）和垂直（俯仰引起的上下位移）漂移，因此沿行列的双向状态空间扫描可以有效地建模和补正跨视图变化；(2) 固定3D模型的自渲染视图天然具有几何一致性，所以可以训练一个评判器来区分一致与不一致的渲染集合，从而在没有真实多视图对的情况下为生成器提供一致性信号。
claims:
- 移除SE(3)多视图评判器损失后，FID从4.94升至5.41，MEt3R从0.2620升至0.3144（表4），表明该损失对感知质量和几何一致性至关重要。
- MVCHead在所有多视图一致性指标上均超越CGSGAN：cPSNR 22.08 vs 19.89，cSSIM 0.764 vs 0.740，cLPIPS 0.053 vs 0.066，MEt3R 0.262 vs 0.316（表3）。
- 自渲染图与真值和中间视图合成的对比显示，MVCHead的MEt3R为0.231，远低于CAP4D的0.312，接近真值0.207（图4），证实自渲染一致性先验的有效性。
- 用Quad-Attn替代HiBiSS导致MEt3R上升至0.2792，完全移除扫描导致FID升至5.66，证明对齐扫描方向的必要性（表4）。
---

# Multi-view Consistent 3D Gaussian Head Avatars 'without' Multi-view Generation

> [!tip] 核心洞察
> 两个关键洞察：(1) 头部化身的多视图不一致主要表现为水平（偏航引起的左右位移）和垂直（俯仰引起的上下位移）漂移，因此沿行列的双向状态空间扫描可以有效地建模和补正跨视图变化；(2) 固定3D模型的自渲染视图天然具有几何一致性，所以可以训练一个评判器来区分一致与不一致的渲染集合，从而在没有真实多视图对的情况下为生成器提供一致性信号。

| 字段 | 内容 |
|------|------|
| 中文题名 | 无需多视图生成的多视角一致3D高斯头部化身 |
| 英文题名 | Multi-view Consistent 3D Gaussian Head Avatars 'without' Multi-view Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Chharia_Multi-view_Consistent_3D_Gaussian_Head_Avatars_without_Multi-view_Generation_CVPR_2026_paper.html) · [Project](https://humansensinglab.github.io/MVCHead/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | MVCHead |
| Dataset | FFHQ, FFHQ-C |

> [!tip] 效果简介
> - FFHQ 上，FID↓ 4.39 vs 4.94 (CGSGAN) (-0.55)；FID3D↓ 4.39 vs 4.94 (CGSGAN) (-0.55)。
> - FFHQ-C 上，FID↓ 3.94 vs 4.53 (CGSGAN) (-0.59)；FID3D↓ 3.94 vs 4.53 (CGSGAN) (-0.59)。
> - FFHQ-C (MVC) 上，Chamfer Distance↓ 0.6654 vs 0.7181 (CGSGAN) (-0.0527)。

## 概要

**问题背景**：生成高保真、多视角一致的3D头部化身通常依赖昂贵的多视图采集或中间视图合成。现有前馈3D高斯生成方法（如**CGSGAN**，Barthel et al., NeurIPS 2025）在仅使用2D图像、无3D或多视图监督的“极小资源设定”下，因缺乏显式跨视图约束，纹理与几何在视图间产生显著漂移，限制了化身在自由视角下的可用性。

**核心瓶颈**：多视图不一致主要表现为沿图像水平轴（偏航引起的左右位移）和垂直轴（俯仰引起的上下位移）的漂移。传统基于自注意力或单向状态空间扫描的架构无法有效对齐这些轴向漂移，而单纯依赖对抗损失又不足以约束跨视图几何一致性。

**本文方案**：MVCHead提出两个关键机制来应对上述瓶颈：
1. **HiBiSS（层次化双向状态扫描）**：在层次化状态空间块（HiSS block）内部，沿行和列执行四向双向状态扫描，使循环方向与多视图漂移的主轴对齐，从而在3D高斯参数回归过程中显式建模和补正跨视图变化。
2. **SE(3)多视图评判器**：基于固定3D模型的自渲染视图天然具有几何一致性这一洞察，训练一个相机位姿感知的评判器来区分一致与不一致的渲染集合，为生成器提供多视图一致性奖励信号，而无需真实多视图对。

**方法定位**：MVCHead属于前馈单次3D高斯头部生成方法，在**GSGAN**（Hyun et al., NeurIPS 2024）的分层生成架构基础上，将纯Transformer自注意力替换为“自注意力 + 状态空间块”双混合器，并引入无多视图数据的一致性监督范式。与需要中间视图合成的**CAP4D**（Taubner et al., CVPR 2025）等方法形成鲜明对比。

**主要结果**：在FFHQ和FFHQ-C数据集上，MVCHead在感知质量（FID 4.39 vs. CGSGAN 4.94）和多视图一致性指标（cPSNR 22.08 vs. 19.89，MEt3R 0.262 vs. 0.316）上均超越现有方法。消融实验证实，移除SE(3)评判器损失后MEt3R从0.262升至0.314，将HiBiSS替换为四向自注意力后MEt3R升至0.279，表明两个组件对多视图一致性均不可或缺。



### 3D头部化身的生成范式演进

高保真3D头部化身在远程通信、虚拟现实和数字人等应用中需求迫切，但其生成长期以来面临数据获取成本与生成质量的尖锐矛盾。图2概括了当前三种主流范式：

**范式一：多视图工作室采集重建。** 依赖昂贵的光场相机阵列和受控环境（如Light Stage）捕获同一人物在多视角下的一致外观，再通过3D高斯泼溅（3DGS）重建高质量头部化身。该路线数据成本极高，难以规模化。

**范式二：中间视图合成后重建。** 先利用2D生成模型（如扩散模型）合成中间视图，再将这些视图作为多视图输入进行3D重建。代表工作包括**CAP4D**（Taubner et al., CVPR 2025）等基于多视图扩散的方法。然而，中间视图本身缺乏显式的跨视图一致性约束，合成误差会传播至重建阶段，导致纹理漂移和几何伪影。

**范式三：从2D图像直接前馈生成3D高斯。** 在仅使用单视图2D图像（如FFHQ数据集）且无任何3D或多视图监督的“极小资源设定”下，通过生成对抗网络直接回归3D高斯参数。代表方法包括**GSGAN**（Hyun et al., NeurIPS 2024）、**GGHead**（Kirschstein et al., SIGGRAPH Asia 2024）以及引入相机条件的**CGSGAN**（Barthel et al., NeurIPS 2025）。这类方法摆脱了对3D数据的依赖，极大降低了数据门槛，但面临一个核心瓶颈。

### 核心瓶颈：无多视图监督下的跨视图一致性

在范式三的极小资源设定下，模型仅从2D图像分布中学习，缺乏显式的多视图几何约束。这导致生成的3D高斯化身在单视图渲染时可能逼真，但**从不同视角观察时，纹理和几何会发生漂移**——即所谓的多视图不一致问题。具体表现为：

- **水平漂移**：偏航角变化引起左右方向的纹理错位与几何偏移。
- **垂直漂移**：俯仰角变化引起上下方向的外观不一致。

以CGSGAN为代表的现有SOTA方法主要依赖对抗损失和条件损失来约束单视图渲染质量，但对抗训练本身不提供跨视图的显式对齐信号，无法从根本上解决多视图一致性退化。

### 本文动机：在不依赖多视图数据的前提下实现多视图一致性

本文的核心动机是回答一个关键问题：**能否在保持范式三“极小资源设定”的前提下——即不使用任何多视图数据、3D监督或中间视图合成——使前馈3D高斯生成模型获得多视图一致性？**

这一目标的实现面临双重挑战：
1. **架构层面**：需要设计一种生成器内部机制，能够建模和补偿跨视图的漂移模式，而不仅仅是逐像素的纹理生成。
2. **监督层面**：缺乏真实多视图对意味着无法直接施加跨视图一致性损失，必须寻找替代的监督信号来源。

MVCHead正是围绕这两条线索展开：在架构上提出层次化双向状态扫描（HiBiSS）以对齐多视图漂移的主轴方向，在监督上提出基于自渲染先验的SE(3)多视图评判器以提供无真实多视图对的一致性奖励信号。



## 核心方法与创新机理

MVCHead 在“极小资源设定”（仅2D图像、无3D数据、无多视图监督）下，针对前馈3D高斯头部化身生成中的多视图不一致问题，提出了三个相互协同的核心创新。

### 1. 层次化双向状态空间扫描（HiBiSS）

**问题根因**：头部化身的多视图不一致集中表现为水平漂移（偏航引起的左右位移）和垂直漂移（俯仰引起的上下位移），即漂移主轴与图像的行、列方向高度对齐。传统Transformer自注意力无法有效建模这种轴对齐的跨视图变化。

**创新机制**：HiBiSS将Mamba的单向扫描改造为沿行和列的四方向层次化双向状态扫描：
- 行方向：左→右、右→左
- 列方向：上→下、下→上

在每个HiSS块内，特征令牌先经过自注意力混合器，再通过HiBiSS沿四个方向传播长程上下文，最后融合所有扫描结果。这种设计使状态空间递推方向与多视图漂移主轴精确对齐，从而在无跨视图显式约束的情况下，通过层次化扫描逐步补正粗到细的高斯参数中的视图间偏差。

**消融证据**：将HiBiSS替换为四向自注意力（Quad-Attn）后，MEt3R从0.2620升至0.2792；完全移除扫描模块后，FID升至5.66、MEt3R升至0.2904（Table 4），证实单纯自注意力无法有效对齐多视图漂移，状态空间扫描是保持多视图一致性的关键。

### 2. SE(3)多视图评判器与一致性损失

**问题根因**：在无真实多视图对的情况下，生成器缺乏跨视图一致性信号，仅靠对抗损失和正则项无法约束视图间纹理与几何的漂移。

**创新机制**：利用“固定3D模型的自渲染视图天然具有几何一致性”这一先验（Figure 4验证：自渲染视图的MEt3R为0.231，接近真值0.207，远低于CAP4D的0.312），训练一个外参感知的评判器 $E_{\psi}$，输入一组渲染图及其相机位姿 $\{T_k\}$，输出一致性得分。评判器以同一身份的自渲染集为正样本、不同身份的渲染集为负样本进行训练。生成器通过最大化评判器得分（即最小化 $\mathcal{L}_{mvc} = -\mathbb{E}[E_{\psi}]$）来获得多视图一致性奖励信号。

**消融证据**：移除 $\mathcal{L}_{mvc}$ 后，FID从4.94升至5.41，MEt3R从0.2620升至0.3144（Table 4），表明该损失对感知质量和几何一致性均有显著贡献。

### 3. 双混合器HiSS块与无相机条件的层次化细化

**架构改进**：每个HiSS块包含两个互补的混合器——自注意力混合器和状态空间块（HiBiSS），替代纯Transformer自注意力。同时，HiSS块内**显式省略相机条件注入**，相机条件仅用于判别器和评判器。这一设计迫使生成器学习与视角无关的3D表示，而非依赖相机条件来“补偿”视图间的不一致。

**层次化细化**：细粒度高斯参数显式表示为粗层级锚点的偏移量（$\mu_{fine} = \mu_{coarse} + \Delta\mu$ 等），并在细化前通过HiBiSS传播全局上下文，使偏移量跨视图保持一致。

### 与基线方法的关键差异（Changed Slots）

| 模块 | 基线（CGSGAN/GSGAN） | MVCHead |
|------|---------------------|---------|
| 特征混合器 | 纯Transformer自注意力 | 双混合器（自注意力 + 状态空间块） |
| 状态空间扫描 | 标准Mamba单向扫描或未使用 | 四方向层次化双向扫描（HiBiSS） |
| 多视图一致性监督 | 无显式MVC奖励 | SE(3)多视图评判器 + $\mathcal{L}_{mvc}$ |
| 相机条件注入位置 | 生成器内部注入 | HiSS块中显式省略，仅用于评判器/判别器 |
| 高斯细化方式 | 层次化生成 | 基于锚点偏移 + HiBiSS全局上下文传播 |

**协同效应**：消融实验完整模型在所有指标上均取得最佳（Table 4），验证了三个创新的协同作用——HiBiSS对齐漂移主轴、评判器提供一致性奖励信号、层次化细化传播全局上下文，共同实现在无多视图数据下的多视图一致生成。



MVCHead 是一个单次前馈的 3D 高斯头部化身生成模型，其核心设计目标是在仅使用 2D 图像训练、无任何 3D 或多视图监督的“极小资源设定”下，显式地强制多视图一致性。整体 pipeline 由三个关键阶段串联而成：**层次化高斯参数回归**、**多视图一致性评判** 以及 **可微分渲染与对抗监督**。

### 输入与初始化

模型以随机隐变量 $z \sim \mathcal{N}(0, I)$ 为输入，不依赖任何显式的 3D 先验（如模板网格或参数化人脸模型）。隐变量首先通过一个映射网络转换为初始特征 token，随后进入由 $L$ 层 HiSS（Hierarchical State Space）块组成的堆叠结构。

### 层次化 HiSS 块：从粗到细的高斯参数回归

HiSS 块是 MVCHead 的核心计算单元，负责从粗到细地逐步细化 3D 高斯参数。每一层 HiSS 块输出一组高斯参数 $g_i = (\mu_i, s_i, q_i, \alpha_i, c_i)$，分别对应中心位置、尺度、四元数旋转、不透明度和颜色。精细层的高斯被显式参数化为粗层锚点的偏移量，而非独立预测，这种层次化锚点机制增强了多尺度几何的一致性。

在每一层 HiSS 块内部，token 依次通过两个互补的特征混合器：

1. **自注意力混合器**：捕获全局 token 间的长程依赖关系，保证生成质量。
2. **状态空间混合器**：执行 Hierarchical Bi-directional State Scan（HiBiSS），沿水平和垂直两个主轴进行四方向双向扫描，显式对齐多视图漂移的轴向。

值得注意的是，HiSS 块内部**刻意省略了相机条件注入**——相机位姿仅在后续的评判器和判别器中使用。这一设计选择迫使生成器学习与视角无关的 3D 表示，而非记忆特定视角的外观。

### HiBiSS：轴向对齐的双向状态空间扫描

HiBiSS 是 MVCHead 实现多视图一致性的第一个关键机制。其设计动机来自一个几何洞察：3D 高斯头部化身中的多视图不一致主要表现为**水平漂移**（偏航引起的左右位移）和**垂直漂移**（俯仰引起的上下位移），这两个方向恰好与图像的像素行列对齐。

基于此，HiBiSS 在每层 HiSS 块内对 token 的 2D 布局执行四种互补扫描：
- 行向从左到右
- 行向从右到左
- 列向从上到下
- 列向从下到上

四种扫描结果通过可学习的融合权重聚合，使得每个 token 能够同时感知来自其上下左右四个方向的状态信息，从而在粗到细的细化过程中传播一致的外观和几何线索。

### SE(3) 多视图评判器：无需多视图数据的一致性监督

MVCHead 的第二个关键机制是 **SE(3) 多视图评判器**。其设计基于另一个核心洞察：**任何固定 3D 模型的自渲染视图天然具有几何一致性**（见 Figure 4）。因此，可以训练一个评判器来区分“一致”与“不一致”的渲染集合，而无需真实的配对多视图数据。

评判器 $E_{\psi}$ 是一个外参感知的 ViT 编码器，它接收一组渲染图像及其对应的相机位姿 $\{T_k\}_{k=1}^K$，输出一个标量一致性分数。训练评判器时：
- **正样本**：来自同一 3D 模型的多视角自渲染图，天然一致。
- **负样本**：将不同身份的渲染图混合，构造出明显不一致的图像集合。

生成器的多视图一致性损失 $\mathcal{L}_{mvc}$ 定义为评判器得分的负期望，鼓励生成器产生高一致性分数的渲染集合。

### 可微分渲染与综合训练目标

生成器输出的高斯集合 $S_{\theta}(z)$ 通过可微分 3D 高斯泼溅渲染器 $\mathcal{R}$ 与相机位姿 $T$ 映射为 2D 图像 $\mathbf{I} = \mathcal{R}(S_{\theta}(z), T)$。综合训练目标由以下分量组成：

$$\mathcal{L}_{\mathrm{total}} = \lambda_{mvc}\mathcal{L}_{mvc} + \text{Adv Loss} + \lambda_{knn}\mathcal{L}_{knn} + \lambda_{ctr}\mathcal{L}_{ctr}$$

其中：
- $\mathcal{L}_{mvc}$：多视图一致性损失，由 SE(3) 评判器提供奖励信号。
- **对抗损失**：相机条件化的判别器确保渲染图像与真实图像分布对齐，维持高频纹理真实感。
- $\mathcal{L}_{knn}$：近邻正则化，约束邻近高斯的参数平滑性。
- $\mathcal{L}_{ctr}$：中心漂移正则化，防止高斯中心过度偏离锚点。

### 与基线方法的架构差异

相较于前代方法 **GSGAN**（Hyun et al., NeurIPS 2024）和 **CGSGAN**（Barthel et al., NeurIPS 2025），MVCHead 在三个关键维度上进行了结构性改进：(1) 将纯 Transformer 自注意力替换为双混合器架构（自注意力 + 状态空间块）；(2) 引入 HiBiSS 四方向双向扫描替代标准单向 Mamba 扫描；(3) 新增 SE(3) 多视图评判器提供显式的一致性监督，而此前方法仅依赖对抗和条件损失。

### 补充图表

![[assets/figures/papers/paper_list_l2550_https_openaccess_thecvf_com_content_CVPR2026_html_Chharia_Multi_view_Con/figures/003_Figure_3.jpg]]
*Figure 3: Model Architecture. MVCHead along with its key proposed components, including HiSS blocks which hierarchically regress the 3D Gaussian parameters (Gaussian S0 becomes the anchor A0 for computing the next Gaussian*

![[assets/figures/papers/paper_list_l2550_https_openaccess_thecvf_com_content_CVPR2026_html_Chharia_Multi_view_Con/figures/002_Figure_2.jpg]]
*Figure 2: Motivation. Paradigms for 3D Gaussian head avatar generation. (a) Requires expensive studio captures; (b) Synthesizes intermediate views before reconstruction; (c) Learns an unconditional 3D Gaussian head directly from 2D images w/o intermediate generation or even 3D data*



### 层次化状态空间块 (HiSS Blocks)

MVCHead 的核心生成架构由 **L 层层次化状态空间块 (HiSS blocks)** 堆叠而成，从粗到细逐步回归 3D 高斯参数。每一层 HiSS 块接收上一层的输出作为锚点 (anchor)，并通过偏移量参数化更细粒度的高斯：

- **粗层高斯** $S_0$ 作为锚点 $A_0$，用于计算下一层高斯 $S_1$，以此类推。
- 细层高斯的参数显式表示为相对于粗层锚点的偏移量，这一设计与 **GSGAN** (Hyun et al., NeurIPS 2024) 的层次化生成范式一致。
- 经过 $L$ 层 HiSS 块后，总高斯原语数量为 $\sum_{l=0}^{L-1} N r^{l}$，其中 $r$ 为上采样比率。

每个 3D 高斯由以下参数定义：

$$g_i = (\mu_i, s_i, q_i, \alpha_i, c_i)$$

其中 $\mu_i$ 为中心位置，$s_i$ 为尺度，$q_i$ 为四元数旋转，$\alpha_i$ 为不透明度，$c_i$ 为颜色。

可微分泼溅渲染器将高斯集合 $S_{\theta}(z)$ 和相机位姿 $T$ 映射为 2D 图像：

$$\mathbf{I} = \mathcal{R}(S_{\theta}(z), T)$$

在每个 HiSS 块内部，token 经过两个互补的混合器：**自注意力** 和 **状态空间块**。值得注意的是，HiSS 块中明确省略了相机条件注入——相机条件仅用于后续的评判器和判别器，这与 **CGSGAN** (Barthel et al., NeurIPS 2025) 在生成器内部注入相机条件的设计形成关键差异。

---

### 层次化双向状态空间扫描 (HiBiSS)

#### 设计动机：轴对齐的多视图漂移

MVCHead 的关键洞察之一是：3D 高斯头部化身的多视图不一致性强烈地与图像轴对齐。具体而言：

- **偏航 (yaw)** 变化主要引起水平位移（左右漂移）；
- **俯仰 (pitch)** 变化主要产生垂直位移（上下漂移）。

这一现象可以从投影几何中得到形式化解释。在规范位姿下，3D 点 $\mathbf{X} = (X, Y, Z)^\top$ 投影到像素坐标：

$$\mathbf{u} = (x, y)^\top = \left( f_x \frac{X}{Z}, f_y \frac{Y}{Z} \right)^\top$$

对于小旋转 $\delta\theta_x$ (pitch) 和 $\delta\theta_y$ (yaw)，一阶位移近似为：

$$\delta \mathbf{u} \approx J_x(\mathbf{X}) \delta\theta_x + J_y(\mathbf{X}) \delta\theta_y$$

这表明多视图漂移在像素空间中主要表现为沿水平和垂直方向的分量。

#### 扫描机制

基于上述洞察，MVCHead 引入 **HiBiSS (Hierarchical Bi-directional State Space Scanning)**，将标准 Mamba 的单向扫描改造为四向 2D 扫描：

- **行向从左到右** (→)
- **行向从右到左** (←)
- **列向从上到下** (↓)
- **列向从下到上** (↑)

HiBiSS 层次化地运行所有四个方向的扫描，并将结果特征融合。以水平前向扫描为例，其状态空间递推公式为：

$$h_{i,j+1} = A_h h_{i,j} + B_h F_{i,j}, \quad \tilde{F}_{i,j}^{\mathrm{hor}} = C_h h_{i,j} + D_h F_{i,j}$$

其中 $F_{i,j}$ 为位置 $(i,j)$ 的输入特征，$h_{i,j}$ 为隐藏状态，$A_h, B_h, C_h, D_h$ 为可学习参数。其他三个方向采用类似但独立参数化的递推。

通过沿行列双向扫描，HiBiSS 使递推方向与多视图漂移的主轴对齐，从而在细化高斯参数之前实现外观和几何线索的连贯传播，提升跨视图一致性。

---

### SE(3) 多视图评判器

#### 自渲染一致性先验

第二个核心洞察是：任何固定 3D 模型的自渲染视图在几何上天然具有一致性（见 Figure 4 的验证）。基于此，可以训练一个评判器来区分一致与不一致的渲染集合，从而在无需真实多视图对的情况下为生成器提供一致性信号。

![[assets/figures/papers/paper_list_l2550_https_openaccess_thecvf_com_content_CVPR2026_html_Chharia_Multi_view_Con/figures/004_Figure_4.jpg]]
*Figure 4: Self-Renders provide strong MVC prior. We evaluate MVC between view pairs from (a) studio-captured data [42], (b) intermediate view synthesis [69], and (c) self-renders from 3D. Using MASt3R [46] for estimating epipolar-consistent correspondence and FeatUp-DINO [8, 23] for measuring feature agreement with a view-invariant encoder, we compute a per-pixel consistency score map over the overlapping region. For each case, we visualize: Left: inputs; Middle: reprojected views A→B and B→A; Right: overlap mask and consistency map (dark = consistent, bright = inconsistent). MEt3R [4] is the spatial average of the error*

#### 评判器架构与损失

SE(3) 多视图评判器 $E_{\psi}$ 是一个外参感知的编码器，将一组图像及其对应相机位姿映射为标量一致性得分。其核心组件包括 ViT 编码器和几何变换注意力机制。

多视图一致性损失鼓励生成器产生高评判器得分：

$$\mathcal{L}_{mvc} = -\mathbb{E}_{z,\{T_k\}}\left[E_{\psi}\left(\{\mathcal{R}(S_{\theta}(z), T_k)\}_{k=1}^K, \{T_k\}_{k=1}^K\right)\right]$$

评判器的训练负样本使用了不同身份的组合，而正样本来自固定 3D 模型的自渲染。

---

### 综合训练目标

完整训练目标由多视图一致性损失、对抗性纹理损失和高斯正则化项组成：

$$\mathcal{L}_{\mathrm{total}} = \lambda_{mvc}\mathcal{L}_{mvc} + \text{Adv Loss} + \lambda_{knn}\mathcal{L}_{knn} + \lambda_{ctr}\mathcal{L}_{ctr}$$

其中：
- $\mathcal{L}_{mvc}$ 为多视图一致性损失
- $\text{Adv Loss}$ 为相机条件化的对抗判别器损失，确保渲染图像的高频纹理真实感
- $\mathcal{L}_{knn}$ 为近邻正则化，约束高斯原语的空间分布
- $\mathcal{L}_{ctr}$ 为中心漂移正则化

需要指出的是，消融实验（Table 4）表明，移除对抗损失会导致训练崩溃，说明在无 3D 数据设定下，仅依靠一致性损失不足以约束纹理分布，对抗监督对维持纹理真实感仍不可或缺。



## 实验与关键发现

### 实验设置

MVCHead 在 FFHQ 和 FFHQ-C 两个数据集上进行训练，分辨率为 512×512。训练使用 Adam 优化器，在 4 块 NVIDIA H100 GPU 上训练 1000 万步，耗时约 3 天。所有对比方法均遵循相同的评估协议，MVC 评价指标（如 cPSNR、MEt3R）基于 100 个随机化身取平均，以保证统计可靠性。

### 感知真实性

表 1 和表 2 分别报告了标准视角和极端视角下的感知质量。MVCHead 在 FFHQ 上取得 FID 4.39，在 FFHQ-C 上取得 FID 3.94，均优于此前最优方法 CGSGAN（FFHQ: 4.94, FFHQ-C: 4.53），降幅分别达 0.55 和 0.59。在极端视角下的 FID3D 指标上，MVCHead 同样以相同数值全面领先，表明模型不仅在正面视角生成高保真纹理，在偏航和俯仰等大角度变化下仍能维持感知质量。

### 多视图一致性

表 3 系统评估了生成化身的多视图一致性。MVCHead 在所有六项指标上均超越 CGSGAN：cPSNR 从 19.89 提升至 22.08（+2.19），cSSIM 从 0.740 升至 0.764，cLPIPS 从 0.066 降至 0.053，MEt3R 从 0.316 降至 0.262。几何一致性方面，Chamfer Distance 从 0.718 降至 0.665，Depth Error 从 7.995 降至 6.665。这些提升表明 HiBiSS 扫描与 SE(3) 多视图评判器的协同作用有效抑制了跨视图的纹理漂移和几何错位。

图 4 进一步验证了自渲染一致性先验的有效性。将 MVCHead 自渲染视图对与真值（studio-captured data）和 CAP4D 的中间视图合成进行对比：MVCHead 的 MEt3R 为 0.231，远低于 CAP4D 的 0.312，接近真值的 0.207。这证实了“固定 3D 模型的自渲染天然具有几何一致性”这一核心洞察——即便在无真实多视图对的情况下，该先验也能为评判器提供有效的训练信号。

### 消融实验

表 4 的消融实验揭示了各组件的因果贡献：

- **移除对抗损失**：训练直接崩溃，无法生成有意义的输出。这说明在无 3D 监督的极小资源设定下，仅靠一致性损失不足以约束纹理分布，对抗监督对维持高频纹理真实感仍不可或缺。
- **移除 SE(3) 多视图评判器损失（$\mathcal{L}_{mvc}$）**：FID 从 4.94 升至 5.41，MEt3R 从 0.2620 升至 0.3144。该损失同时对感知质量和几何一致性产生显著贡献，验证了评判器提供的跨视图对齐信号的关键作用。
- **将 HiBiSS 替换为四向自注意力（Quad-Attn）**：FID 升至 5.35，MEt3R 升至 0.2792。单纯的自注意力无法有效对齐多视图漂移，证明状态空间扫描的序列归纳偏置对于建模水平/垂直轴向漂移具有本质优势。
- **完全移除扫描模块**：FID 升至 5.66，MEt3R 升至 0.2904，性能退化为所有消融中最差。这确认了沿行列的双向状态扫描是维持多视图一致性的核心机制。
- **完整模型（MVCHead）**：在所有指标上均取得最优，验证了 HiBiSS 扫描、SE(3) 评判器与对抗损失的协同作用。

### 失败模式与局限

尽管 MVCHead 在感知质量与多视图一致性上取得显著提升，仍存在以下局限：

1. **后脑勺缺失**：模型无法生成完整的 360° 头部化身，缺乏后脑勺覆盖，不能用于全视角应用。这源于训练数据仅包含正面及半侧面视角。
2. **几何对称性不足**：几何先验完全从 2D 监督中学习，缺乏显式的双侧对称约束，可能导致非对称的面部几何结构。
3. **评判器负样本质量有限**：SE(3) 多视图评判器的训练负样本仅使用了不同身份的组合，未能对同身份但不一致的渲染进行判别。引入更难负样本有望进一步增强评判器的判别力。
4. **对抗训练依赖**：移除对抗损失即崩溃，表明当前一致性损失单独不足以完全替代对抗训练来约束纹理分布。
5. **泛化边界未验证**：模型尚未在大规模无约束视频数据上测试，极端光照与遮挡场景下的鲁棒性待进一步考察。

### 补充图表

![[assets/figures/papers/paper_list_l2550_https_openaccess_thecvf_com_content_CVPR2026_html_Chharia_Multi_view_Con/figures/006_Table_1.jpg]]
*Table 1: Perceptual Realism. Comparison of FID scores. 512 × 512 resolution was used for the experiments. †Uses superresolution network. *We report the results from the original paper*

![[assets/figures/papers/paper_list_l2550_https_openaccess_thecvf_com_content_CVPR2026_html_Chharia_Multi_view_Con/figures/007_Table_2.jpg]]
*Table 2: Perceptual Realism at extremes. Comparison of FID3D scores. 512 × 512 resolution was used for the experiments*

![[assets/figures/papers/paper_list_l2550_https_openaccess_thecvf_com_content_CVPR2026_html_Chharia_Multi_view_Con/figures/005_Table_3.jpg]]
*Table 3: Multi-view Consistency. Consistency scores of the synthesized 3D Gaussian heads averaged over 100 avatars*

![[assets/figures/papers/paper_list_l2550_https_openaccess_thecvf_com_content_CVPR2026_html_Chharia_Multi_view_Con/figures/008_Table_4.jpg]]
*Table 4: Ablation Study. Performed on the FFHQ-C [6] dataset with 512 × 512 resolution to verify the proposed components*



## 定位与知识库关联

### 问题定位与范式边界

MVCHead 解决的核心瓶颈是：在仅使用 2D 图像、无 3D 数据、无多视图监督的“极小资源设定”下，前馈 3D 高斯生成模型难以保持跨视图的纹理与几何一致性，导致视图间出现水平（偏航引起）和垂直（俯仰引起）的漂移。Figure 2 将这一设定置于 3D 高斯头部化身生成的三大范式之中：(a) 需要昂贵影棚采集的多视图重建；(b) 先合成中间视图再重建的间接方法；(c) MVCHead 所代表的直接从 2D 图像学习无条件 3D 高斯头部的直接生成范式。MVCHead 的独特之处在于，它在范式 (c) 中首次实现了对多视图一致性的显式建模，而不依赖任何中间视图合成或 3D 监督。

### 直接基线与继承关系

MVCHead 在架构上直接继承自分层 3D 高斯生成对抗网络 **GSGAN**（Hyun et al., NeurIPS 2024），保留了其层次化高斯生成框架和对抗训练范式。在此基础上，MVCHead 与两个同期或后续工作形成直接对比：

- **CGSGAN**（Barthel et al., NeurIPS 2025）：在 GSGAN 基础上引入相机条件注入，是当前 SOTA 方法。MVCHead 在感知质量（FID：4.39 vs 4.94）和多视图一致性（MEt3R：0.262 vs 0.316）上全面超越 CGSGAN，且明确省略了 HiSS 块内的相机条件注入，转而将相机信息仅用于评判器和判别器——这一设计选择说明，在状态空间扫描框架下，显式的相机条件可能反而干扰跨视图特征的对齐过程。

- **GGHead**（Kirschstein et al., SIGGRAPH Asia 2024）：基于 UV 模板的前馈 3D 高斯头部生成器，代表另一种技术路线。MVCHead 与 GGHead 的对比体现在 FID3D 指标上（Table 2），MVCHead 在极端视角下同样表现更优。

- **CAP4D**（Taubner et al., CVPR 2025）：基于多视图扩散的头部化身生成方法，属于范式 (b)。Figure 4 显示，CAP4D 的自渲染多视图一致性（MEt3R 0.312）显著弱于 MVCHead（0.231），且远差于真值（0.207），这从侧面验证了间接合成中间视图再重建的路线会引入额外的不一致性。

### 关键改动槽位与方法创新

MVCHead 相对于基线的核心改动集中在五个槽位，每个槽位对应一个明确的设计选择：

1. **特征混合器**：从纯 Transformer 自注意力改为“自注意力 + 状态空间块”的双混合器架构。消融实验（Table 4）表明，将 HiBiSS 替换为四向自注意力（Quad-Attn）会导致 FID 升至 5.35、MEt3R 升至 0.2792，证明单纯的自注意力无法有效对齐多视图漂移——状态空间扫描的递推结构对建模跨视图的长程依赖具有本质优势。

2. **状态空间扫描方向**：从标准 Mamba 的单向扫描改为沿行和列的四方向 HiBiSS。这一设计的理论依据来自对多视图漂移轴向的分析：偏航主要引起水平位移，俯仰主要引起垂直位移，因此行列方向的双向扫描恰好对齐了多视图不一致的主轴。完全移除扫描模块时 FID 升至 5.66、MEt3R 升至 0.2904，验证了扫描方向选择的关键性。

3. **多视图一致性监督**：从无显式 MVC 奖励（仅用对抗和正则损失）改为增加 SE(3) 多视图评判器及对应损失 $\mathcal{L}_{mvc}$。这是 MVCHead 与 GSGAN/CGSGAN 最根本的差异。评判器的训练利用了“固定 3D 模型的自渲染视图天然具有几何一致性”这一先验（Figure 4 提供了实证支持），从而在无需真实多视图对的情况下提供一致性信号。移除该损失后 FID 升至 5.41、MEt3R 升至 0.3144，表明其对感知质量和几何一致性均有显著贡献。

4. **相机条件注入位置**：从生成器内部注入（如 CGSGAN）改为仅在评判器和判别器中注入。这一设计选择与 HiBiSS 的扫描机制形成配合——生成器内部的无相机条件设计迫使模型学习视角无关的 3D 表示，而将视角依赖的判别留给外部模块。

5. **高斯细化方式**：在 GSGAN 层次化生成的基础上，引入基于锚点偏移的细化机制，并在细化前通过 HiBiSS 传播全局上下文。这使得细粒度高斯的生成能够利用已对齐的粗粒度特征，进一步提升跨层级的一致性。

### 适用边界与局限

MVCHead 的适用边界受以下因素制约：

- **视角覆盖范围**：模型无法生成完整的 360° 头部化身，缺乏后脑勺覆盖，不能用于全视角应用。这源于训练数据（FFHQ/FFHQ-C）本身的视角分布限制，而非方法层面的根本缺陷。

- **几何先验的隐式性**：几何先验完全从 2D 监督中学习，缺乏显式的结构性约束（如双侧对称）。这可能导致生成的面部几何出现非对称性，在极端视角下尤为明显。

- **评判器的训练策略**：SE(3) 多视图评判器的训练负样本仅使用了不同身份的组合，未能对同身份但不一致的渲染进行判别。这意味着评判器可能主要学会区分身份差异而非一致性差异，未来引入更难负样本（如同身份的错误渲染）有望增强评判器的判别能力。

- **对抗训练的不可替代性**：移除对抗损失会导致训练崩溃（Table 4），说明仅依靠一致性损失不足以约束纹理分布。这一发现表明，在无 3D 监督的条件下，对抗监督对维持高频纹理真实感仍不可或缺——这与当前社区中“纯一致性损失可能替代对抗训练”的假设形成对照，需要进一步验证。

- **泛化性未经验证**：模型尚未在大规模无约束视频数据上测试，泛化至极端光照、遮挡和多样化表情的场景可能受限。此外，方法是否可扩展到全身化身或通用物体类别仍是一个开放问题。

### 开放问题与社区定位

MVCHead 揭示了若干待解决的方向：

1. **多视图一致性评价标准**：目前缺乏统一的多视图一致性评价基准。现有指标（如 MEt3R、cPSNR）仅能部分衡量一致性，社区需建立更完善的 3D 头部 MVC 评估协议。MVCHead 在 Table 3 中使用的六项指标（cPSNR、cSSIM、cLPIPS、MEt3R、Chamfer Distance、Depth Error）构成了当前较为全面的评估体系，但仍缺乏对时序一致性和动态表情的覆盖。

2. **对抗训练的替代路径**：如何在不需要对抗训练的情况下，仅靠一致性损失实现同等纹理质量，是一个具有理论价值的方向。MVCHead 的消融实验表明当前尚不可行，但该问题的解决将显著简化训练流程并提升稳定性。

3. **时序一致性的扩展**：能否将时间一致性纳入 HiBiSS 框架，用于动态头部生成？状态空间模型天然适合序列建模，将 HiBiSS 的扫描维度从空间扩展到时空是一个自然的技术延伸方向。

4. **跨类别泛化**：MVCHead 的多视图漂移轴向分析基于头部姿态的先验（偏航-水平、俯仰-垂直），该先验是否适用于其他类别（如全身人体、通用物体）尚待验证。若漂移轴向与图像坐标轴的对齐关系在跨类别时不再成立，HiBiSS 的扫描方向设计可能需要重新校准。



## 原文 PDF

![[paperPDFs/CVPR_2026/Multi_view_Consistent_3D_Gaussian_Head_Avatars_without_Multi_view_Generation.pdf]]
