---
title: "Grid Distillation: Compositional Image Distillation via Structured Generative Grids"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Grid_Distillation_Compositional_Image_Distillation_via_Structured_Generative_Grids.pdf
project_link: null
code_link: null
aliases:
- GD
- GDCIDSGG
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 谱子模优化（Spectral-Submodular Grid Selection）驱动的结构化网格构建与单步扩散细节增强
primary_logic: 通过将图像选择建模为谱子模优化，最大化覆盖、多样性与光谱信息，构造包含类内多样性和空间上下文的高分辨率组合网格，再下采样为紧凑表示，并利用单步扩散恢复丢失的细节，从而在保持空间结构和语义保真度的同时实现高效蒸馏。
claims:
- 在ImageWoof所有IPC设置下，Grid Distillation大幅超越现有扩散蒸馏方法，IPC=10 ResNet-18准确率达65.5%，比VLCP提升25.6%。
- 消融实验表明，扩散细节增强相比双线性上采样在所有数据集上均带来显著提升，证实恢复高频纹理的必要性。
- 子模优化参数消融显示，同时使用覆盖、多样性和光谱信息（α=1.0,β=0.6,γ=0.3）取得最佳准确率78.6%，去除任一项均导致性能下降。
- ImageWoof 上 Top-1 Accuracy (%) = 65.5
---

# Grid Distillation: Compositional Image Distillation via Structured Generative Grids

> [!tip] 核心洞察
> 通过将图像选择建模为谱子模优化，最大化覆盖、多样性与光谱信息，构造包含类内多样性和空间上下文的高分辨率组合网格，再下采样为紧凑表示，并利用单步扩散恢复丢失的细节，从而在保持空间结构和语义保真度的同时实现高效蒸馏。

| 字段 | 内容 |
|------|------|
| 中文题名 | 网格蒸馏：通过结构化生成网格的组合图像蒸馏 |
| 英文题名 | Grid Distillation: Compositional Image Distillation via Structured Generative Grids |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Das_Grid_Distillation_Compositional_Image_Distillation_via_Structured_Generative_Grids_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Grid Distillation |
| Dataset | ImageWoof, ImageNet-1K |

> [!tip] 效果简介
> - ImageWoof 上，Top-1 Accuracy (%) 65.5 vs 39.9 (+25.6)；Top-1 Accuracy (%) 84.3 vs 58.9 (+25.4)；Top-1 Accuracy (%) 75.2 vs 44.5 (+30.7)。
> - ImageNet-1K 上，Mean Accuracy (%) 50.01 vs ~45.3 (~+4.7)。

## 概要

**核心问题**：现有数据集蒸馏方法在构造紧凑的合成数据时，难以同时编码空间组合结构与注入世界知识。基于优化的方法（如 **SRe2L** (Yin et al., NeurIPS 2023)）虽能恢复大规模压缩图像，但蒸馏数据空间碎片化；基于扩散的方法（如 **VLCP** (Zou et al., arXiv 2025)、**Minimax** (Gu et al., CVPR 2024)）引入生成先验，却牺牲了类内多样性和空间上下文的结构化表达，导致语义浅薄或信息冗余。

**方法定位**：**Grid Distillation** 提出了一种新的数据集蒸馏范式——将图像选择建模为**谱子模优化（Spectral-Submodular Grid Selection）**，在CLIP嵌入空间中同时最大化覆盖、多样性与光谱信息，构造包含类内多样性和空间上下文的高分辨率组合网格；随后下采样为紧凑表示，并利用**单步扩散细节增强**恢复丢失的高频纹理。这一设计将网格构建从启发式采样提升为原则性优化，在保持空间结构和语义保真度的同时实现高效蒸馏。

**核心结论**：
- 在ImageWoof数据集上，Grid Distillation在所有IPC设置下大幅超越现有扩散蒸馏方法：IPC=10时ResNet-18准确率达**65.5%**，比VLCP提升**25.6个百分点**；IPC=50时达**84.3%**，提升**25.4个百分点**（Table 1）。
- 消融实验证实，扩散细节增强相比双线性上采样在所有数据集上均带来显著提升，验证了恢复高频纹理的必要性（Table 5）；子模优化的覆盖、多样性与光谱信息三项参数缺一不可，联合使用取得最优准确率**78.6%**（Table 6）。
- 在ImageNet-1K（IPC=10）上，Grid Distillation的均值准确率达**50.01%**，优于现有方法约4.7个百分点（Table 4），展示了该方法在大规模场景下的扩展潜力。



数据集蒸馏（Dataset Distillation）旨在将大规模训练数据压缩为极少量合成样本，使下游模型在这些样本上训练后仍能逼近在全量数据上的性能。这一范式在降低存储与计算开销、加速模型迭代方面具有重要价值，但其核心瓶颈始终在于：**如何在极低数据预算下同时保留空间组合结构与注入世界知识**。

现有的蒸馏方法可大致归为四类范式，它们在可解释性、信息密度与世界知识之间呈现出不同的权衡（Figure 1）：

- **基于分布匹配的方法**（如 **DM**，Zhao and Bilen, CVPR 2023）通过最小化合成数据与真实数据在特征空间中的分布差异来生成样本。这类方法产生的图像通常缺乏可解释的视觉结构，信息密度较低。
- **基于参数化合成的方法**（如 **IDC-1**，Kim et al., ICML 2022）将合成数据编码为可学习参数，但生成的样本往往呈现碎片化的纹理模式，难以承载语义完整的对象表示。
- **基于恢复压缩的方法**（如 **SRe2L**，Yin et al., NeurIPS 2023；**RDED**，Sun et al., CVPR 2024）通过对大规模压缩图像进行解码恢复来生成蒸馏数据，虽能保留一定的空间结构，但缺乏对世界知识的显式建模。
- **基于扩散模型的方法**（如 **Minimax**，Gu et al., CVPR 2024；**D4M**，Su et al., CVPR 2024；**VLCP**，Zou et al., arXiv 2025）利用扩散先验生成蒸馏图像，能够注入丰富的世界知识，但生成的样本往往以独立图像为单位，缺乏对空间组合结构的显式编码。

上述方法的共同缺陷在于：**它们将蒸馏数据视为孤立的合成图像集合，忽视了图像之间的空间组织关系与类内多样性结构**。随机采样或简单聚类无法保证所选样本在语义空间中的覆盖度与互补性，导致蒸馏数据在空间上碎片化、在语义上浅薄。这构成了本文的核心动机——**能否通过结构化的数据组织方式，在蒸馏过程中同时编码空间组合结构与世界知识，从而突破现有范式的性能上限？**



## 核心方法与创新机理

### 瓶颈与动机

现有数据集蒸馏方法面临一个根本性矛盾：基于合成的范式（如 **SRe2L**，Yin et al., NeurIPS 2023；**RDED**，Sun et al., CVPR 2024）能注入生成模型的世界知识，但难以编码多实例间的空间组合结构；而基于选择的范式虽能保留真实分布，却缺乏语义增强能力。这导致蒸馏数据要么空间碎片化，要么语义浅薄，无法同时满足覆盖性、多样性与信息密度的要求。

Grid Distillation 的应对策略是将图像蒸馏重新定义为**结构化网格构建问题**：不再生成或选择孤立样本，而是构造一张编码类内多样性与空间上下文的组合网格图像。其核心创新可分解为三个耦合的 changed slots。

### 创新一：谱子模网格选择（SSDIM）——从随机采样到优化驱动

传统蒸馏的样本选择依赖随机采样或聚类（如 **DM**，Zhao and Bilen, CVPR 2023），缺乏对覆盖性、多样性与光谱信息量的显式建模。Grid Distillation 将网格构建形式化为**谱子模优化**问题，在三个维度上同时优化：

- **覆盖性**（α）：确保所选子集对类内所有样本的亲和度最大化，避免语义盲区；
- **多样性**（β）：通过 $\log\det(\mathbf{K}_{S,S} + \epsilon\mathbf{I})$ 鼓励所选样本在特征空间中分散，抑制冗余；
- **光谱信息量**（γ）：引入谱能量分数 $s_i = \sum_{k=1}^{r} \lambda_k u_{ik}^2$，优先选取对类流行前 $r$ 个主模式贡献大的样本，保留数据结构的主成分。

三者通过子模函数 $\mathcal{F}(S) = \alpha\sum_{i\in\mathcal{U}}\max_{j\in\mathcal{S}}K_{ij} + \beta\log\det(\mathbf{K}_{S,S}+\epsilon\mathbf{I}) + \gamma\sum_{i\in\mathcal{S}}s_i$ 联合优化，经贪心算法在多项式时间内求得 $L^2$ 个样本构成网格。Figure 3 的定性对比直观展示了这一改进：随机选择产生大量语义冗余（红框标注），而谱子模优化生成的网格在语义多样性与空间互补性上显著占优。

### 创新二：单步扩散细节增强——从简单上采样到生成式纹理恢复

网格图像需从高分辨率下采样至紧凑尺寸以控制存储开销，但双线性插值等朴素上采样会永久丢失高频纹理。Grid Distillation 引入**单步扩散解码**作为细节增强模块：将下采样后的蒸馏网格 $\mathbf{y}_0$ 通过条件噪声预测构造扩散反演的初始潜在状态 $\mathbf{x}_{\tau_S} = \sqrt{\bar{\alpha}_{\tau_S}}\mathbf{y}_0 + \sqrt{1-\bar{\alpha}_{\tau_S}} f_w(\mathbf{y}_0, \mathbf{p}, \tau_S)$，再经单步反向扩散 $\mathbf{x}_0 = g_{\theta}(\mathbf{x}_{\tau_S}, \tau_S)$ 恢复细节。该模块利用 Stable Diffusion Turbo 的生成先验，仅需一次前向传播即可重建边缘与纹理，在保持语义一致性的前提下提升信息密度。消融实验（Table 5）证实，扩散增强在所有数据集和 IPC 设置下均一致优于双线性上采样，是性能增益的关键来源。

### 创新三：网格感知概率裁剪——从随机裁剪到结构对齐

标准训练中的随机裁剪可能破坏网格的空间语义布局。Grid Distillation 提出**网格感知裁剪**策略：以概率 $p_{\mathrm{align}}$ 在网格边界对齐的偏移量上裁剪，保留子图像间的空间关系；以概率 $1-p_{\mathrm{align}}$ 执行随机裁剪，注入局部变化。这种混合策略在结构保真度与数据增强之间取得平衡，实验设置 $p_{\mathrm{align}}=0.6$。

### 创新间的因果耦合

三个创新并非独立叠加，而是形成因果链条：SSDIM 提供高质量的空间组合骨架，下采样压缩为紧凑表示，扩散增强恢复压缩损失的高频细节，网格感知裁剪则在训练阶段保护这一空间结构不被破坏。消融实验（Table 6）验证了子模目标中三项的互补性——同时使用覆盖、多样性与光谱信息（α=1.0, β=0.6, γ=0.3）取得最佳准确率 78.6%，去除任一项均导致性能下降，证实三者缺一不可。



Grid Distillation 的整体流水线围绕一个核心洞察展开：**将图像选择建模为谱子模优化问题**，以构造高分辨率组合网格，并在下采样为紧凑表示后通过单步扩散恢复丢失的细节。该流程由四个顺序模块构成，形成从原始数据到下游训练数据的完整转换链路。

### 流水线总览

整个框架如 Figure 2 所示，包含以下四个模块：

![[assets/figures/papers/paper_list_l882_https_openaccess_thecvf_com_content_CVPR2026_html_Das_Grid_Distillation/figures/003_Figure_2.jpg]]
*Figure 2: Spectral-submodular grid distillation pipeline. Starting from a pool of class images, we (1) extract normalized embeddings using a pretrained encoder, (2) build an affinity kernel and compute a spectral decomposition to obtain per-sample spectral energy scores*

1. **Spectral-Submodular Grid Selection (SSDIM)**：从类内图像池中选取 $L^2$ 张代表性图像，排列为 $L \times L$ 的结构化网格。
2. **下采样与紧凑表示**：将高分辨率网格下采样至目标蒸馏尺寸，形成紧凑的蒸馏图像。
3. **Diffusion-Based Detail Enhancement**：利用单步扩散模型（Stable Diffusion Turbo）恢复下采样过程中丢失的高频细节。
4. **Downstream Classifier Training**：在增强后的蒸馏网格上训练下游分类器，采用网格感知裁剪策略。

### 模块间数据流

输入为每类一个图像池 $\mathcal{D}_c$。首先通过预训练编码器（CLIP）提取归一化嵌入，构建类内亲和矩阵 $\mathbf{K}$，并对其进行谱分解：

$$\mathbf{K} = \mathbf{U} \mathbf{\Lambda} \mathbf{U}^{\top}$$

基于特征向量和特征值，为每张图像计算光谱能量分数 $s_i = \sum_{k=1}^{r} \lambda_k u_{ik}^2$，衡量其对类流行前 $r$ 个主模式的能量贡献。随后，SSDIM 通过最大化子模目标函数 $\mathcal{F}(S)$ 选取 $L^2$ 张图像：

$$\mathcal{F}(S) = \alpha \sum_{i \in \mathcal{U}} \max_{j \in \mathcal{S}} K_{ij} + \beta \log \det(\mathbf{K}_{S,S} + \epsilon \mathbf{I}) + \gamma \sum_{i \in \mathcal{S}} s_i$$

该目标函数的三个项分别控制**覆盖性**（$\alpha$）、**多样性**（$\beta$）和**光谱信息量**（$\gamma$）。选取的 $L^2$ 张图像被排列为 $L \times L$ 网格，形成包含类内多样性与空间上下文的高分辨率组合表示。

接着，网格被下采样至目标分辨率。下采样不可避免地损失高频纹理信息，因此引入扩散细节增强模块：基于蒸馏图像 $\pmb{y}_0$ 和文本提示 $\pmb{p}$ 构造扩散反演的初始潜在状态：

$$\pmb{x}_{\tau_S} = \sqrt{\bar{\alpha}_{\tau_S}}\pmb{y}_0 + \sqrt{1 - \bar{\alpha}_{\tau_S}} f_w(\pmb{y}_0, \pmb{p}, \tau_S)$$

随后通过单步反向扩散 $\pmb{x}_0 = g_{\theta}(\pmb{x}_{\tau_S}, \tau_S)$ 重建细节增强的网格图像。

### 训练时的网格感知裁剪

下游分类器训练阶段采用网格感知裁剪策略：

$$\mathcal{C}(\mathbf{I}; p_{\mathrm{align}}) = \begin{cases} \mathrm{AlignedCrop}(\mathbf{I}), & \mathrm{w.p.}~ p_{\mathrm{align}} \\ \mathrm{RandomCrop}(\mathbf{I}), & \mathrm{w.p.}~ 1 - p_{\mathrm{align}} \end{cases}$$

以概率 $p_{\mathrm{align}}$ 在网格边界的整数倍位置进行对齐裁剪，保留网格的语义布局；以 $1-p_{\mathrm{align}}$ 的概率进行随机裁剪，增加局部变化。默认设置 $p_{\mathrm{align}}=0.6$。

### 关键设计选择

默认配置中，网格尺寸固定为 $L=4$（即 $4 \times 4$ 网格），谱分解秩 $r=32$，子模权重 $\alpha=1.0, \beta=0.6, \gamma=0.3$。消融实验（Table 6）证实，三个子模项缺一不可——去除任一项均导致性能下降，三者联合取得最高准确率 78.6%。扩散细节增强相比双线性上采样在所有数据集和 IPC 设置下均带来一致且显著的提升（Table 5），验证了恢复高频纹理对蒸馏质量的关键作用。



Grid Distillation 的核心由三个模块构成：谱子模网格选择（SSDIM）、基于扩散的细节增强，以及网格感知裁剪策略。三者协同，将类别图像池转化为紧凑的结构化蒸馏网格，并在下游训练中保持空间语义。

### 2.1 谱子模网格选择（SSDIM）

该模块将网格构建形式化为定义在图像嵌入上的子模优化问题，目标是选出 $L^2$ 张代表性图像，排列成 $L \times L$ 网格，以最大化类内覆盖、多样性与光谱信息量。

**亲和矩阵谱分解。** 给定某类的 $n$ 张图像，用预训练 CLIP 编码器提取归一化嵌入，构建亲和矩阵 $\mathbf{K} \in \mathbb{R}^{n \times n}$，其中 $K_{ij}$ 度量图像 $i$ 与 $j$ 的语义相似度。对 $\mathbf{K}$ 做谱分解：

$$\mathbf{K} = \mathbf{U} \mathbf{\Lambda} \mathbf{U}^{\top} \tag{1}$$

其中 $\mathbf{U}$ 的列为特征向量，$\mathbf{\Lambda}$ 为特征值对角矩阵。

**光谱能量分数。** 为量化每张图像对类流行主要模式的贡献，定义光谱能量分数：

$$s_i = \sum_{k=1}^{r} \lambda_k u_{ik}^2 \tag{2}$$

其中 $r$ 为保留的前 $r$ 个主模式数（默认 $r=32$），$\lambda_k$ 为第 $k$ 个特征值，$u_{ik}$ 为第 $i$ 张图像在第 $k$ 个特征向量上的分量。$s_i$ 越大，表示该图像对类流行结构的解释力越强。

**子模优化目标。** 在候选集 $\mathcal{U}$ 上选择子集 $\mathcal{S}$（$|\mathcal{S}| = L^2$），最大化以下子模函数：

$$\mathcal{F}(S) = \alpha \underbrace{\sum_{i \in \mathcal{U}} \max_{j \in \mathcal{S}} K_{ij}}_{\text{覆盖性}} + \beta \underbrace{\log \det(\mathbf{K}_{S,S} + \epsilon \mathbf{I})}_{\text{多样性}} + \gamma \underbrace{\sum_{i \in \mathcal{S}} s_i}_{\text{光谱信息量}} \tag{4}$$

- **覆盖性项**：鼓励所选子集 $\mathcal{S}$ 在语义空间中“覆盖”尽可能多的候选图像，使每个候选图像至少与一个被选图像高度相似。
- **多样性项**：对数行列式函数 $\log\det$ 促进所选图像之间保持语义差异，避免冗余。
- **光谱信息量项**：直接累加光谱能量分数，优先选择对类流行主模式贡献大的图像。

三项通过权重 $\alpha, \beta, \gamma$ 平衡。消融实验（Table 6）表明，三者联合（$\alpha=1.0, \beta=0.6, \gamma=0.3$）取得最优准确率 78.6%，去除任一项均导致性能下降，证实覆盖性、多样性与光谱信息量缺一不可。

### 2.2 基于扩散的细节增强

选出的 $L^2$ 张图像排列成高分辨率网格后，需下采样至目标蒸馏尺寸。朴素下采样（如双线性插值）会丢失高频纹理和边缘细节。为此，Grid Distillation 引入单步扩散模型（Stable Diffusion Turbo）进行细节恢复。

**扩散反演初始潜在状态。** 给定下采样后的蒸馏网格 $\pmb{y}_0$ 和类别提示 $\pmb{p}$，构造反演的初始潜在表示：

$$\pmb{x}_{\tau_S} = \sqrt{\bar{\alpha}_{\tau_S}}\pmb{y}_0 + \sqrt{1 - \bar{\alpha}_{\tau_S}} f_w(\pmb{y}_0, \pmb{p}, \tau_S) \tag{5}$$

其中 $\tau_S$ 为起始时间步，$\bar{\alpha}_{\tau_S}$ 为噪声调度参数，$f_w$ 为条件噪声预测网络。该公式将蒸馏图像与基于提示的噪声估计混合，为后续逆向扩散提供起点。

**逆向扩散重建。** 从 $\pmb{x}_{\tau_S}$ 出发，执行单步（或少步）逆向扩散，恢复精细细节：

$$\pmb{x}_0 = g_{\theta}(\pmb{x}_{\tau_S}, \tau_S) \tag{6}$$

消融实验（Table 5）强有力地证明该模块的必要性：在所有数据集和 IPC 设置下，扩散细节增强相比双线性上采样均带来一致且显著的性能提升，验证了恢复高频纹理对蒸馏质量的关键作用。

### 2.3 网格感知裁剪

训练下游分类器时，标准随机裁剪可能割裂网格中的语义单元。Grid Distillation 提出网格感知裁剪策略，以概率 $p_{\mathrm{align}}$ 对齐网格边界进行裁剪：

$$\mathcal{C}(\mathbf{I}; p_{\mathrm{align}}) = \begin{cases} \mathrm{AlignedCrop}(\mathbf{I}), & \mathrm{w.p.}~ p_{\mathrm{align}} \\ \mathrm{RandomCrop}(\mathbf{I}), & \mathrm{w.p.}~ 1 - p_{\mathrm{align}} \end{cases} \tag{7}$$

对齐裁剪的起始坐标取 $(h, w)$ 的整数倍（$h, w$ 为网格子图尺寸），从而保留网格的语义布局；随机裁剪则引入局部变化，增强鲁棒性。默认 $p_{\mathrm{align}}=0.6$，在保持结构完整性与注入数据多样性之间取得平衡。

### 补充图表

![[assets/figures/papers/paper_list_l882_https_openaccess_thecvf_com_content_CVPR2026_html_Das_Grid_Distillation/figures/005_Figure_4.jpg]]
*Figure 4: Illustration of Grid-Aware Cropping An aligned crop starts at multiples of*



## 实验与关键发现

### 实验设置与基准

所有实验在256×256分辨率下进行，评估协议与现有数据集蒸馏工作保持一致。蒸馏网格大小固定为 $L=4$（即4×4网格，每类IPC=16），谱分解保留前 $r=32$ 个主模式。子模优化权重设为 $\alpha=1.0$、$\beta=0.6$、$\gamma=0.3$，网格感知裁剪对齐概率 $p_{\mathrm{align}}=0.6$。SSDIM模块基于OpenAI CLIP实现，采用批量GPU操作以保证效率。下游分类器训练使用ResNetAP-10、ResNet-18和ConvNet-6三种架构，在ImageWoof、ImageNette、ImageIDC和ImageNet-1K四个数据集上进行评估。

### 主实验结果

**ImageWoof上的性能突破。** Grid Distillation在所有IPC设置和模型架构下均大幅超越现有方法（Table 1）。在IPC=10设置下，ResNet-18准确率达**65.5%**，比次优方法VLCP（Zou et al., arXiv 2025）的39.9%高出**25.6个百分点**；ResNetAP-10准确率63.9%，比VLCP的39.1%高出24.8个百分点。当IPC增至50时，ResNet-18准确率进一步提升至**84.3%**，领先VLCP（58.9%）达25.4个百分点。这一显著优势源于结构化网格同时编码了类内多样性和空间上下文，而现有扩散蒸馏方法生成的独立合成图像缺乏这种组合结构。

**ImageNette与ImageIDC上的验证。** 在ImageNette数据集上（Table 2），Grid Distillation在IPC=10时ResNetAP-10准确率达83.3%，IPC=1时达76.4%，均显著优于VLCP等基线方法。在ImageIDC医学图像数据集上（Table 3），所提方法同样保持领先，验证了结构化网格蒸馏在细粒度分类和领域特定数据上的泛化能力。

**ImageNet-1K大规模验证。** 在ImageNet-1K全量1000类、IPC=10的设置下（Table 4），Grid Distillation取得**50.01%**的平均准确率，显著超越VLCP等近期扩散蒸馏方法。扩散细节增强相比双线性预处理带来约4.7个百分点的提升，证明恢复高频纹理对大规模复杂场景蒸馏至关重要。

### 消融实验

**扩散细节增强的关键作用。** Table 5的消融实验直接对比了双线性上采样与扩散细节增强的效果。在ImageNette和ImageWoof的所有IPC设置下，扩散增强均带来一致且显著的性能提升。例如，ImageWoof IPC=10下准确率从双线性上采样的基线提升至63.9%，ImageNette IPC=10下提升至83.3%。这验证了核心假设：下采样过程中丢失的高频纹理和边缘信息可通过单步扩散先验有效恢复，而简单的插值无法弥补这一信息损失。

**子模优化参数的互补性。** Table 6系统消融了子模目标函数中三个分量的作用。在ImageWoof IPC=20、ResNetAP-10的设置下，同时使用覆盖（$\alpha=1.0$）、多样性（$\beta=0.6$）和光谱信息（$\gamma=0.3$）取得最高准确率**78.6%**。单独去除任一分量均导致性能下降：仅用覆盖和多样性（$\gamma=0$）降至77.1%，仅用多样性和光谱（$\alpha=0$）降至76.4%，仅用覆盖和光谱（$\beta=0$）降至75.8%。这表明三个维度——全局覆盖、样本间互补性和光谱代表性——对构建高质量蒸馏网格缺一不可。

### 定性分析

Figure 3直观对比了随机选择与谱子模优化构建的网格。在UCF-101 Mid-Frames数据集上，随机选择常产生语义冗余的子图（红色标注区域），而SSDIM产生的网格在语义多样性和空间互补性上明显更优。Figure 4展示了网格感知裁剪策略的效果：对齐裁剪从网格边界的整数倍偏移量起始，保留结构化布局；随机裁剪则引入局部变化，二者以概率 $p_{\mathrm{align}}$ 混合使用。

### 失败模式与局限性

尽管Grid Distillation在多个基准上取得显著提升，仍存在以下局限：（1）网格尺寸固定为4×4，未探索自适应网格大小以适应不同类别的密度分布；（2）子模优化依赖CLIP嵌入，在极端领域外数据上的有效性未经验证；（3）扩散细节增强引入约16.9%的一次性计算开销，需要额外GPU推理；（4）仅在ImageNet子集和UCF-101上评估，未在更大规模或更复杂数据集上验证扩展性。这些限制为后续工作提供了明确的改进方向。

### 补充图表

![[assets/figures/papers/paper_list_l882_https_openaccess_thecvf_com_content_CVPR2026_html_Das_Grid_Distillation/figures/006_Table_1.jpg]]
*Table 1: Comparison of state-of-the-art methods on ImageWoof under various IPC settings and model architectures. “Ours” column reports accuracies from our Grid-Distil experiments. All results are measured at 256×256 resolution. The best results are in bold, and the secondbest are underlined (in VLCP)*

![[assets/figures/papers/paper_list_l882_https_openaccess_thecvf_com_content_CVPR2026_html_Das_Grid_Distillation/figures/010_Table_5.jpg]]
*Table 5: Ablation study on detail enhancement preprocessing. Comparison between Bilinear Upsampling and our Diffusion-Based Detail Enhancement across three datasets using ResNetAP-10 at varying IPC values. Our preprocessing consistently preserves finegrained visual detail, leading to improved classification performance on ImageNette and ImageWoof*

![[assets/figures/papers/paper_list_l882_https_openaccess_thecvf_com_content_CVPR2026_html_Das_Grid_Distillation/figures/012_Table_6.jpg]]
*Table 6: Ablation of submodular ooptimization parameters. Results on real ImageWoof grids (IPC=20) using ResNetAP-10. The study isolates the role of coverage (α), diversity (β), and spectral information (γ)*

![[assets/figures/papers/paper_list_l882_https_openaccess_thecvf_com_content_CVPR2026_html_Das_Grid_Distillation/figures/009_Table_4.jpg]]
*Table 4: Performance comparison on ImageNet-1K (IPC = 10). Our diffusion-based detail enhancement significantly improves classification accuracy compared to bilinear preprocessing and recent distillation methods*

![[assets/figures/papers/paper_list_l882_https_openaccess_thecvf_com_content_CVPR2026_html_Das_Grid_Distillation/figures/007_Table_2.jpg]]
*Table 2: Comparison of dataset distillation methods on ImageNette using ResNetAP-10 under various IPC settings. Best results are in bold; second-best method (VLCP) is underlined*

![[assets/figures/papers/paper_list_l882_https_openaccess_thecvf_com_content_CVPR2026_html_Das_Grid_Distillation/figures/008_Table_3.jpg]]
*Table 3: Comparison of dataset distillation methods on ImageIDC using ResNetAP-10 under various IPC settings. Best results are in bold; second-best method (VLCP) is underlined*

![[assets/figures/papers/paper_list_l882_https_openaccess_thecvf_com_content_CVPR2026_html_Das_Grid_Distillation/figures/011_Table_7.jpg]]
*Table 7: Few-shot classification accuracy (%) on UCF-101 Mid-Frames. Our method (Grid-LDC) consistently outperforms prior CLIP adaptation techniques across all few-shot settings, demonstrating the benefit of grid-level distillation for motioncentric visual reasoning*

![[assets/figures/papers/paper_list_l882_https_openaccess_thecvf_com_content_CVPR2026_html_Das_Grid_Distillation/figures/004_Figure_3.jpg]]
*Figure 3: Effect of Submodular Grid Selection. Comparison of grids constructed from the UCF Mid-Frames dataset (selected to show the visible effect of our algorithm). Left: Random selection often yields redundant sub-images (highlighted in red). Right: Our spectral submodular optimization produces semantically diverse and spatially complementary grids. The figure demonstrates how submodular selection improves coverage and diversity over naive random sampling*

![[assets/figures/papers/paper_list_l882_https_openaccess_thecvf_com_content_CVPR2026_html_Das_Grid_Distillation/figures/001_Figure.jpg]]
*Figure: (b) RDED (c) VLCP (d) Grid-Distil*

![[assets/figures/papers/paper_list_l882_https_openaccess_thecvf_com_content_CVPR2026_html_Das_Grid_Distillation/figures/002_Figure.jpg]]
*Figure: (a) SRe2L*



## 定位与知识库关联

### 1. 与现有数据集蒸馏范式的继承与分叉

Grid Distillation 的核心动机源于对现有数据集蒸馏方法两个结构性瓶颈的观察：**空间组合结构的缺失**与**世界知识的浅层注入**。从方法谱系上看，该方法与三类主流范式形成明确的继承与分叉关系。

**基于分布匹配的蒸馏（Distribution Matching）**：以 **DM**（Zhao and Bilen，CVPR 2023）为代表的方法通过匹配真实与合成数据的特征分布来生成蒸馏样本。这类方法将每张蒸馏图像视为独立的分布载体，未显式编码样本间的空间关系。Grid Distillation 继承了“以紧凑表示覆盖类别分布”的目标，但将其从独立样本的集合重构为一张结构化网格——通过谱子模优化将类内多样性与空间上下文同时压缩进单张图像，从而将分布匹配从特征空间扩展到了空间布局层面。

**基于参数化合成的蒸馏（Parameterization-Based）**：**IDC-1**（Kim et al.，ICML 2022）将合成数据表示为可学习参数，通过优化分类性能反向更新合成图像。这类方法赋予合成数据极高的自由度，但缺乏对视觉真实性的约束。Grid Distillation 放弃了端到端可微的合成路径，转而采用“选择-组装-增强”的离散-连续混合管线：先用子模优化从真实图像中选取最具代表性的样本，再通过扩散模型恢复下采样丢失的细节。这一设计在保留真实图像纹理先验的同时，获得了参数化方法难以实现的语义保真度。

**基于扩散先验的蒸馏（Diffusion-Based）**：这是 Grid Distillation 最直接的方法近邻。**SRe2L**（Yin et al.，NeurIPS 2023）率先将大规模扩散模型引入数据集蒸馏，通过恢复压缩图像的高频细节来提升合成质量。**D4M**（Su et al.，CVPR 2024）进一步解耦扩散模型的不同组件以精细化控制生成过程。**Minimax**（Gu et al.，CVPR 2024）采用极小极大优化目标平衡多样性与真实性。**RDED**（Sun et al.，CVPR 2024）通过分片多样化补丁提升样本多样性。**VLCP**（Zou et al.，arXiv 2025）引入视觉-语言原型指导扩散生成。这些方法的核心贡献在于“如何生成更好的单张蒸馏图像”，而 Grid Distillation 的关键分叉在于**将生成问题转化为选择问题**：它不生成新像素，而是通过子模优化选择真实图像子集构建网格，再用单步扩散恢复下采样损失的细节。这一设计使该方法在 ImageWoof IPC=10 下以 65.5% 的准确率大幅超越 VLCP 的 39.9%（+25.6%），在 IPC=50 下达到 84.3%（+25.4%），构成了当前扩散蒸馏方法在该基准上的最强性能。

### 2. 知识库定位：组合性、子模优化与扩散先验的交叉点

Grid Distillation 位于三个技术脉络的交汇处：

**组合表示学习**：该方法将类别知识编码为 $L \times L$ 的网格布局，每张子图承载类内流形的一个局部模式。这种组合设计使得单张蒸馏图像能够同时编码多个互补的视觉概念，与传统的“一张图一个样本”范式形成根本差异。网格感知裁剪策略（Eq.7）进一步在训练时保持这种组合结构，以概率 $p_{\text{align}}$ 对齐网格边界进行裁剪，确保下游模型能够感知到子图间的空间关系。

**子模优化与数据摘要**：将图像选择建模为子模函数最大化（Eq.4）是该方法的理论支柱。目标函数 $\mathcal{F}(S) = \alpha \sum_{i \in \mathcal{U}} \max_{j \in \mathcal{S}} K_{ij} + \beta \log \det(\mathbf{K}_{S,S} + \epsilon \mathbf{I}) + \gamma \sum_{i \in \mathcal{S}} s_i$ 分别编码覆盖性（Facility Location）、多样性（Log-Determinant）和光谱信息量（Spectral Energy Score），其中光谱能量分数 $s_i = \sum_{k=1}^{r} \lambda_k u_{ik}^2$ 通过亲和矩阵 $\mathbf{K} = \mathbf{U} \mathbf{\Lambda} \mathbf{U}^{\top}$ 的谱分解（Eq.1-2）衡量每张图像对类流行主模式的贡献。这一谱子模形式将传统的基于聚类的样本选择提升为具有理论保证的优化问题，消融实验（Table 6）证实三个项缺一不可。

**扩散先验作为细节恢复器**：与将扩散模型作为生成器的方法不同，Grid Distillation 将 Stable Diffusion Turbo 定位为“细节增强解码器”——输入是下采样后的网格图像，输出是恢复高频纹理的增强版本。这一单步反演-重建过程（Eq.5-6）的计算开销约占 16.9%，但消融实验（Table 5）表明其在所有数据集和 IPC 设置下均显著优于双线性上采样，证实了恢复空间细节对蒸馏质量的关键作用。

### 3. 适用边界与局限

**数据分布依赖**：SSDIM 模块依赖 CLIP 嵌入计算亲和矩阵和光谱能量分数。在 CLIP 训练分布覆盖良好的自然图像领域（如 ImageNet 子集），该方法表现优异；但在极端领域外数据（如医学影像、遥感图像）上，CLIP 嵌入的语义质量可能下降，进而影响子模优化的选择质量。这一局限在论文中未被实验验证，属于需要手动验证的边界条件。

**网格尺寸固定**：当前实现将网格尺寸固定为 $L=4$（即 $4 \times 4$ 网格），未根据类别内样本密度或视觉复杂度自适应调整。对于类内多样性极高的类别（如 ImageNet-1K 中的某些细粒度类别），固定 16 个子图可能不足以覆盖所有主要模式；对于简单类别，则可能引入冗余。论文将自适应网格大小列为开放问题。

**计算开销的非对称性**：扩散细节增强虽有效，但引入了一次性推理开销（约 16.9% 的额外计算量），且需要 GPU 推理 Stable Diffusion Turbo。在资源受限场景下，双线性上采样可作为轻量替代，但会牺牲性能。此外，子模优化的贪心求解（Algorithm 1）本身在大规模类别上可能成为瓶颈，尽管论文采用了批量化 GPU 操作来缓解。

**评估范围的局限**：实验覆盖 ImageWoof、ImageNette、ImageIDC 和 ImageNet-1K 四个图像分类基准，以及 UCF-101 Mid-Frames 上的小样本分类。未在目标检测、分割等更复杂的下游任务上验证蒸馏数据的泛化性，也未在更大规模数据集（如完整 ImageNet-21K）上测试扩展性。

### 4. 开放问题与未来方向

**自适应网格构建**：如何根据类别统计特性自动选择网格大小 $L$ 和子模权重 $\alpha/\beta/\gamma$，而非依赖人工调参？一个可能的方向是将这些超参数建模为类别嵌入的函数，通过元学习或贝叶斯优化实现自适应。

**选择与生成的联合优化**：当前管线将子模选择与扩散增强分离为两个独立阶段。能否将二者联合优化——例如，在选择阶段就考虑扩散模型的重建质量，或在扩散增强时利用网格结构信息引导细节恢复？这需要设计可微的子模松弛或基于强化学习的端到端训练策略。

**跨模态扩展**：谱子模网格的核心思想——通过子模优化选择代表性元素构建结构化表示——在理论上不限于视觉数据。文本、图数据、甚至表格数据都可以定义亲和矩阵和光谱能量分数，从而构建类似的结构化蒸馏表示。这一扩展方向尚未被探索。

**更大规模验证**：在 ImageNet-1K IPC=10 下，Grid Distillation 达到 50.01% 的平均准确率，超越 VLCP 约 4.7 个百分点，但与完整数据集训练的差距仍然显著。在 IPC=50 或更高设置下，该方法的扩展行为及其与纯生成式方法的性能交叉点值得进一步研究。



## 原文 PDF

![[paperPDFs/CVPR_2026/Grid_Distillation_Compositional_Image_Distillation_via_Structured_Generative_Grids.pdf]]
