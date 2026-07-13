---
title: "MotionDiffuse: Text-Driven Human Motion Generation with Diffusion Model"
type: paper
paper_level: A
venue: TPAMI
year: 2023
pdf_ref: paperPDFs/TPAMI_2023/MotionDiffuse_Text_Driven_Human_Motion_Generation_with_Diffusion_Model.pdf
project_link: https://mingyuan-zhang.github.io/projects/MotionDiffuse.html
code_link: null
aliases:
- MotionDiffuse
tags:
- TPAMI_2023
- topic/motion_animation
- topic/motion_animation/human_motion_generation
core_operator: "引入去噪扩散概率模型（DDPM）作为生成框架，通过预测噪声并迭代去噪，将文本条件软性地注入生成过程，从而在采样时引入随机性，并支持通过噪声插值实现身体部位独立控制和长序列生成。"
primary_logic: "扩散模型保留了运动序列的显式形式，允许在去噪过程中施加额外约束（如身体部位掩码和时序分段），从而自然实现多层次操控，同时保持高保真度和多样性。"
claims:
- "MotionDiffuse is the first diffusion model-based text-driven motion generation framework."
- "Body-part independent control is achieved via noise interpolation with correction terms."
- "Significant improvements over existing methods on HumanML3D (FID 0.630, Top-1 R Precision 0.491) and KIT-ML (FID 1.954, Top-1 R Precision 0.417)."
- "HumanML3D (text-driven) 上 Top-1 R Precision = 0.491"
---

# MotionDiffuse: Text-Driven Human Motion Generation with Diffusion Model

> [!tip] 核心洞察
> 扩散模型保留了运动序列的显式形式，允许在去噪过程中施加额外约束（如身体部位掩码和时序分段），从而自然实现多层次操控，同时保持高保真度和多样性。

| 字段 | 内容 |
|------|------|
| 中文题名 | MotionDiffuse：基于扩散模型的文本驱动人体运动生成 |
| 英文题名 | MotionDiffuse: Text-Driven Human Motion Generation with Diffusion Model |
| 会议/期刊 | TPAMI 2023 |
| Links | [paper](https://arxiv.org/abs/2208.09601) · [Project](https://mingyuan-zhang.github.io/projects/MotionDiffuse.html) |
| Topic | #topic/motion_animation #topic/motion_animation/human_motion_generation |
| Method | MotionDiffuse |
| Dataset | HumanML3D (text-driven), HumanML3D, KIT-ML (text-driven), KIT-ML |

> [!tip] 效果简介
> - HumanML3D (text-driven) 上，Top-1 R Precision 为 0.491。
> - HumanML3D 上，Top-1 R Precision, FID, MultiModal Dist, Diversity 为 0.630。
> - KIT-ML (text-driven) 上，Top-1 R Precision 为 0.417。

## 概要

**核心问题**：文本驱动人体运动生成的主流方法（如TEMOS、MotionCLIP、Guo et al. CVPR 2022的T2M等）通常采用确定性映射，将文本直接嵌入到生成器或VAE/GAN框架中。这类硬性条件注入导致两个关键瓶颈：（1）生成结果的多样性严重不足，同一文本几乎只能产生单一运动；（2）难以处理描述多个身体部位或包含多时间段的复杂、细粒度文本提示。

**核心思路**：本文提出MotionDiffuse，首次将去噪扩散概率模型（DDPM）引入文本驱动运动生成。其核心洞察在于：扩散模型在去噪过程中保留了运动序列的显式形式，使得可以在逐步去噪时软性地注入文本条件并施加额外约束。这一性质天然支持多层次的生成操控——通过在不同身体部位或不同时间段上独立估计噪声，再进行插值与梯度校正，即可实现部位独立控制和长序列多动作生成，同时保持高保真度和多样性。

**方法定位**：MotionDiffuse将生成模型类型从确定性的VAE/GAN替换为DDPM；文本融合策略从直接联合嵌入或硬条件改为通过交叉注意力与风格化模块的软性注入；首次提出了身体部位噪声插值与时间区间噪声插值两种机制，实现了对运动生成的细粒度操控。文本编码器使用CLIP预训练权重初始化并冻结前几层，运动解码器采用Cross-Modality Linear Transformer以降低注意力计算复杂度。

**主要结果**：在文本驱动运动生成任务上，MotionDiffuse在HumanML3D数据集上取得FID 0.630、Top-1 R Precision 0.491，在KIT-ML数据集上取得FID 1.954、Top-1 R Precision 0.417，显著超越现有方法（见Table 1、Table 2）。在动作条件运动生成任务上，HumanAct12数据集FID低至0.07，UESTC数据集FID为9.10（见Table 5）。消融实验证实，CLIP预训练和高效注意力机制对性能至关重要——在KIT-ML上移除二者后，Top-1 R Precision从0.417骤降至0.136（见Table 3）；潜在维度512配合8-12层Transformer达到最优效果（见Table 4、Table 6）。

**局限性**：扩散模型需要大量去噪步骤，难以实现实时生成；当前pipeline仅适配单一运动表征形式，向多数据集通用框架的扩展仍是开放问题。

**文本驱动人体运动生成**旨在从自然语言描述中合成逼真的三维人体动作序列，在动画制作、虚拟人交互、游戏开发等领域具有重要应用价值。然而，该任务面临一个根本性瓶颈：**从文本到运动的映射本质上是“一对多”的**——同一段文字描述可以对应多种合理的运动表现，而现有方法大多采用确定性的映射策略，导致生成结果的**多样性严重不足**。

具体而言，早期工作如**Language2Pose**（Ahuja and Morency, 3DV 2019）和**T2M**（Guo et al., CVPR 2022）通常将文本编码后直接解码为运动序列，其生成过程缺乏随机性机制，难以捕捉文本描述背后丰富的运动变化空间。此外，这些方法在处理**复杂、细粒度、多时间段的文本描述**时表现乏力——例如，“一个人先挥手然后蹲下”这类包含时序组合的指令，往往无法被准确执行。动作条件生成方法如**Action2Motion**（Guo et al., ACM Multimedia 2020）和**ACTOR**（Petrovich et al., ICCV 2021）虽然引入了一定的条件控制，但本质上仍受限于单动作、固定长度的生成范式。

与此同时，**去噪扩散概率模型**（Denoising Diffusion Probabilistic Model, DDPM）在图像生成领域取得了显著成功，其核心优势在于：通过逐步去噪的随机采样过程，天然支持多样化的输出；同时，扩散模型在去噪过程中保留了数据的显式形式，使得**施加额外约束**成为可能。这为突破文本驱动运动生成的多样性瓶颈提供了新的思路。

本文提出**MotionDiffuse**，作为**首个基于扩散模型的文本驱动运动生成框架**。其核心动机在于：将DDPM引入运动生成，利用其概率映射特性解决多样性问题；同时利用扩散过程保留运动序列显式形式的优势，通过噪声插值等机制实现**身体部位独立控制**和**长序列多动作生成**，从而支持对复杂文本描述的多层次操控。

## 核心方法与创新机理

MotionDiffuse 的核心创新在于将**去噪扩散概率模型（DDPM）**引入文本驱动人体运动生成，从根本上改变了语言到运动的映射范式。相比先前方法（如 **TEMOS**、**MotionCLIP**、**Guo et al. (2022) T2M** 等）采用的确定性 VAE 或 GAN 框架，MotionDiffuse 通过预测并迭代消除噪声来实现生成，从而在采样过程中天然引入随机性，解决了生成多样性不足的瓶颈。

具体而言，该方法在以下五个关键维度上实现了范式转换：

**1. 生成模型类型：从确定性映射到概率扩散**

基线方法通常学习从文本到运动序列的确定性映射，导致给定同一文本时生成的多样性受限。MotionDiffuse 采用 DDPM 作为生成主干，前向过程逐步向真实运动序列添加高斯噪声（$q(\mathbf{x}_t | \mathbf{x}_{t-1}) := \mathcal{N}(\mathbf{x}_t; \sqrt{1-\beta_t} \mathbf{x}_{t-1}, \beta_t \mathbf{I})$），逆向过程则从纯噪声出发，通过预测并消除噪声逐步恢复运动序列。这一设计使得模型在推理时能够从同一文本条件出发采样出多样化的运动结果，实现了从“确定性映射”到“概率映射”的转变。

**2. 文本融合策略：从硬条件注入到软性条件引导**

先前方法通常将文本特征直接嵌入或作为硬性条件注入生成器。MotionDiffuse 提出通过**跨模态线性Transformer**实现文本的软性注入：文本条件通过交叉注意力机制与运动特征交互，同时时间步嵌入通过**风格化模块（Stylization Block）** 以尺度和偏置的形式调制运动特征（$\mathbf{Y}' = \mathbf{Y} \cdot \mathbf{W} + \mathbf{B}$）。这种软性融合方式使得文本条件能够更灵活地影响生成过程，而非强制约束输出。

**3. 身体部位控制：从整体生成到部位独立操控**

基线方法只能根据单一文本生成全身运动。MotionDiffuse 利用扩散模型保留运动序列显式形式的优势，提出了**身体部位噪声插值**机制：将全身运动划分为多个近似独立的部位，对每个部位分别估计噪声 $\epsilon_i^{\mathrm{part}}$，再通过掩码合并并加入梯度校正项（$\bar{\epsilon}^{\mathrm{part}} = \sum \epsilon_i^{\mathrm{part}} \cdot M_i + \lambda_1 \cdot \nabla(\sum \| \epsilon_i^{\mathrm{part}} - \epsilon_j^{\mathrm{part}} \|)$），实现不同身体部位的独立文本控制。这是扩散模型在运动生成领域的独特能力，VAE 或 GAN 框架难以实现。

**4. 长序列生成：从固定长度到时间分段多动作合成**

基线方法通常生成固定长度或单动作的运动序列。MotionDiffuse 扩展了噪声插值思想，提出**时间变化噪声插值**：将时间轴划分为多个区间，每个区间对应不同的文本描述，独立估计各区间噪声后通过校正项实现平滑过渡。这使得模型能够根据“先走路、再挥手、然后坐下”这类多时间段复杂描述生成连贯的长序列运动。

**5. 文本编码器初始化：从随机初始化到 CLIP 预训练迁移**

MotionDiffuse 使用 CLIP 预训练权重初始化文本编码器的前几层并冻结，将大规模视觉-语言预训练知识迁移到运动生成任务中。消融实验（Table 3）表明，这一设计对性能至关重要——去除 CLIP 预训练后，KIT-ML 上的 Top-1 R Precision 从 0.417 骤降至 0.136。

这些创新共同构成了一个统一的框架，使得 MotionDiffuse 在保持高保真度和多样性的同时，天然支持多层次操控（身体部位独立控制和长序列多动作生成），这是先前确定性生成范式难以实现的能力。

MotionDiffuse 的整体框架围绕**去噪扩散概率模型（DDPM）**构建，将文本驱动的运动生成建模为一个条件去噪过程。如 Figure 2 所示，pipeline 由两条核心数据流组成：训练阶段（蓝色箭头）和推理阶段（红色箭头），文本编码与运动解码模块则为两者共享（黑色箭头）。

### 输入输出流

系统的输入是自然语言文本描述，输出是与之匹配的人体运动序列。具体而言：

1. **文本编码**：输入文本首先经过一个基于 CLIP 预训练权重的文本编码器，转换为文本特征向量。该编码器的前几层参数冻结，以保留预训练的语言-视觉对齐知识。
2. **扩散前向过程**：在训练时，真实运动序列 $x_0$ 按方差时间表 $\beta_t$ 逐步加入高斯噪声，得到噪声化序列 $x_t$。这一过程遵循马尔可夫链：
   $$q(\mathbf{x}_{1:T} | \mathbf{x}_0) := \prod_{t=1}^T q(\mathbf{x}_t | \mathbf{x}_{t-1}), \quad q(\mathbf{x}_t | \mathbf{x}_{t-1}) := \mathcal{N}(\mathbf{x}_t; \sqrt{1-\beta_t} \mathbf{x}_{t-1}, \beta_t \mathbf{I})$$
   为提高训练效率，可直接从干净数据采样任意时间步的噪声版本：
   $$q(\mathbf{x}_t | \mathbf{x}_0) = \sqrt{\bar{\alpha_t}} \mathbf{x}_0 + \epsilon \sqrt{1 - \bar{\alpha_t}}, \epsilon \sim \mathcal{N}(\mathbf{0}, \mathbf{I})$$
3. **运动解码（噪声预测）**：噪声化运动序列 $x_t$ 与文本特征、时间步嵌入一同送入**跨模态线性 Transformer**。该模块的核心是一个运动解码器，由多个 Transformer 解码层堆叠而成，每层包含三个关键子模块：
   - **线性自注意力**：对运动序列自身建模，通过计算全局特征图 $\mathbf{F}_g = \mathrm{softmax}(\mathbf{K}^{\top}) \otimes \mathbf{V}$ 将复杂度从 $O(n^2 d)$ 降至 $O(d d_k n)$。
   - **线性交叉注意力**：以文本特征替代自注意力中的键（K）和值（V）计算，将文本语义软性注入运动序列。
   - **风格化模块**：以时间步和文本条件的联合嵌入 $e$ 生成尺度参数 $W$ 和偏置参数 $B$，对运动特征进行逐元素调制：$\mathbf{Y}' = \mathbf{Y} \cdot \mathbf{W} + \mathbf{B}$。
   
   解码器的输出是对当前时间步噪声 $\epsilon$ 的预测 $\epsilon_\theta(\mathbf{x}_t, t, \text{text})$，训练目标是最小化预测噪声与真实噪声之间的均方误差：
   $$\mathcal{L} = \mathrm{E}_{t \in [1, T], \mathbf{x}_0 \sim q(\mathbf{x}_0), \epsilon \sim \mathcal{N}(\mathbf{0}, \mathbf{I})} [|| \epsilon - \epsilon_\theta(\mathbf{x}_t, t, \mathrm{text}) ||]$$
4. **逆向去噪（推理）**：推理时从纯噪声 $x_T \sim \mathcal{N}(0, I)$ 出发，利用训练好的噪声预测网络逐步去噪。每一步通过估计的去噪均值更新运动序列：
   $$\mu_\theta(\mathbf{x}_t, t, \mathrm{text}) = \frac{1}{\sqrt{\alpha_t}} (\mathbf{x}_t - \frac{1 - \alpha_t}{\sqrt{1 - \bar{\alpha}_t}} \epsilon_\theta(\mathbf{x}_t, t, \mathrm{text}))$$
   经过 $T$ 步迭代后得到最终的运动序列 $x_0$。

### 模块关系与核心设计逻辑

框架的关键设计在于**保留运动序列的显式形式**。与 VAE 或 GAN 等将运动映射到隐空间的方法不同，DDPM 在去噪的每一步都直接操作完整的运动序列表示。这一特性使得在去噪过程中可以自然施加额外约束，从而衍生出两个扩展模块：

- **身体部位噪声插值模块**：将全身运动按身体部位划分，对各部位独立估计噪声后通过掩码 $M_i$ 加权合并，并加入梯度校正项 $\lambda_1 \cdot \nabla(\sum \| \epsilon_i^{\text{part}} - \epsilon_j^{\text{part}} \|)$ 以保证部位间过渡平滑。
- **时序噪声插值模块**：将长序列按时段划分，对各时段独立估计噪声后进行插值，同样以校正项保证时序上的连贯性。

这两个模块共享同一个预训练好的去噪网络，无需额外训练即可实现身体部位独立控制和长序列多动作生成，体现了“一次训练、多层次操控”的框架优势。

### 与基线方法的架构差异

相较于确定性映射方法（如 **TEMOS**、**MotionCLIP**、**Guo et al. (2022) T2M**），MotionDiffuse 的核心差异在于：**用扩散模型的随机去噪过程替代了确定性的编码-解码映射**。文本条件通过交叉注意力和风格化模块软性地注入，而非作为硬性条件直接拼接或映射到隐变量。这一设计使得每次采样可产生不同的运动序列，从根源上解决了多样性不足的问题。

MotionDiffuse 以**去噪扩散概率模型（DDPM）**为生成骨架，将文本条件通过**交叉模态线性Transformer**软性地注入去噪过程，并在此基础上构建**身体部位噪声插值**与**时间区间噪声插值**两个操控模块，实现多层次运动控制。

---

### 扩散过程

前向过程按方差时间表 $\{\beta_t\}_{t=1}^T$ 逐步向干净运动序列 $\mathbf{x}_0$ 添加高斯噪声，形成马尔可夫链：

$$q(\mathbf{x}_{1:T} | \mathbf{x}_0) := \prod_{t=1}^T q(\mathbf{x}_t | \mathbf{x}_{t-1}), \quad q(\mathbf{x}_t | \mathbf{x}_{t-1}) := \mathcal{N}(\mathbf{x}_t; \sqrt{1-\beta_t} \mathbf{x}_{t-1}, \beta_t \mathbf{I})$$

为提升训练效率，可直接从 $\mathbf{x}_0$ 采样任意时间步的加噪数据：

$$q(\mathbf{x}_t | \mathbf{x}_0) = \sqrt{\bar{\alpha_t}} \mathbf{x}_0 + \epsilon \sqrt{1 - \bar{\alpha_t}}, \quad \epsilon \sim \mathcal{N}(\mathbf{0}, \mathbf{I})$$

其中 $\bar{\alpha}_t = \prod_{s=1}^t \alpha_s$，$\alpha_t = 1 - \beta_t$。

逆向过程学习高斯转移 $p_\theta(\mathbf{x}_{t-1} | \mathbf{x}_t)$，逐步消除噪声：

$$p_\theta(\mathbf{x}_{0:T}) := p(\mathbf{x}_T) \prod_{t=1}^T p_\theta(\mathbf{x}_{t-1} | \mathbf{x}_t), \quad p_\theta(\mathbf{x}_{t-1} | \mathbf{x}_t) := \mathcal{N}(\mathbf{x}_{t-1}; \mu_\theta(\mathbf{x}_t, t), \Sigma_\theta(\mathbf{x}_t, t))$$

模型不直接预测 $\mathbf{x}_{t-1}$，而是预测噪声项 $\epsilon$，训练损失为：

$$\mathcal{L} = \mathrm{E}_{t \in [1, T], \mathbf{x}_0 \sim q(\mathbf{x}_0), \epsilon \sim \mathcal{N}(\mathbf{0}, \mathbf{I})} \left[|| \epsilon - \epsilon_\theta(\mathbf{x}_t, t, \mathrm{text}) ||\right]$$

预测噪声 $\epsilon_\theta$ 后，去噪均值由下式估计：

$$\mu_\theta(\mathbf{x}_t, t, \mathrm{text}) = \frac{1}{\sqrt{\alpha_t}} \left( \mathbf{x}_t - \frac{1 - \alpha_t}{\sqrt{1 - \bar{\alpha}_t}} \epsilon_\theta(\mathbf{x}_t, t, \mathrm{text}) \right)$$

---

### 交叉模态线性Transformer（运动解码器）

该模块是噪声预测网络 $\epsilon_\theta$ 的核心，由**文本编码器**和**运动解码器**组成。文本编码器使用**CLIP预训练权重**初始化并冻结前几层，将输入文本转化为特征向量。运动解码器由若干Transformer层堆叠而成，每层包含以下子模块：

**线性自注意力。** 为降低标准自注意力的 $O(n^2 d)$ 复杂度，采用高效注意力机制，通过全局特征图 $\mathbf{F}_g$ 避免逐对计算：

$$\mathbf{F}_g = \mathrm{softmax}(\mathbf{K}^{\top}) \otimes \mathbf{V}, \quad \mathbf{Y} = \mathrm{softmax}(\mathbf{Q}) \otimes \mathbf{F}_g$$

复杂度降至 $O(d d_k n)$。

**线性交叉注意力。** 将自注意力中 $\mathbf{K}$、$\mathbf{V}$ 的计算替换为文本特征，其余公式与线性自注意力一致，从而将文本条件软性地注入运动序列。

**风格化模块。** 将时间步嵌入与文本条件融合为尺度 $\mathbf{W}$ 和偏置 $\mathbf{B}$，对运动特征进行调制：

$$\mathbf{B} = \psi_b(\phi(\mathbf{e})), \quad \mathbf{W} = \psi_w(\phi(\mathbf{e})), \quad \mathbf{Y}' = \mathbf{Y} \cdot \mathbf{W} + \mathbf{B}$$

其中 $\mathbf{e}$ 为时间步嵌入与文本特征的联合表示，$\psi_b$、$\psi_w$ 为可学习映射。

---

### 身体部位噪声插值

为实现对身体不同部位的独立控制，MotionDiffuse 将全身运动按关节分组划分为 $m$ 个近独立部位。对每个部位 $i$，以对应的部位文本提示为条件，独立估计噪声 $\epsilon_i^{\mathrm{part}}$。然后通过**掩码合并**与**梯度校正项**进行插值，确保部位交界处平滑过渡：

$$\bar{\epsilon}^{\mathrm{part}} = \sum_{i=1}^{m} \epsilon_i^{\mathrm{part}} \cdot M_i + \lambda_1 \cdot \nabla\left(\sum_{1 \leq i, j \leq m} \| \epsilon_i^{\mathrm{part}} - \epsilon_j^{\mathrm{part}} \|\right)$$

$M_i$ 为部位 $i$ 的二值掩码，$\lambda_1$ 控制校正强度，梯度项推动相邻部位噪声估计趋于一致。

---

### 时间区间噪声插值

对于长序列多动作生成，给定一组文本-时间区间对 $\{\mathrm{text}_{i,j}, [l_{i,j}, r_{i,j}]\}$，首先对每个区间独立估计噪声 $\epsilon_i^{\mathrm{time}}$，再进行插值与校正：

$$\overline{\epsilon}^{\mathrm{time}} = \sum_{i=1}^{m} \overline{\epsilon}_i^{\mathrm{time}} + \lambda_2 \cdot \nabla\left(\sum_{1\leq i,j\leq m} \| \overline{\epsilon}_i^{\mathrm{time}} - \overline{\epsilon}_j^{\mathrm{time}} \|\right)$$

$\overline{\epsilon}_i^{\mathrm{time}}$ 为区间 $i$ 的噪声估计经掩码填充后的全时序噪声，校正项保证不同动作片段之间的自然过渡。

## 实验与关键发现

### 主实验结果

MotionDiffuse 在文本驱动运动生成和动作条件运动生成两个任务上均表现出显著优势。在文本驱动任务上，作者选用 **HumanML3D** 和 **KIT-ML** 两个数据集，与 **TEMOS**、**MotionCLIP**、**Guo et al. (CVPR 2022) 的 T2M**、**Language2Pose** (Ahuja and Morency, 3DV 2019) 等方法进行对比。

**HumanML3D 数据集**（Table 1）上，MotionDiffuse 的 Top-1 R Precision 达到 0.491，FID 为 0.630，MultiModal Dist 和 Diversity 指标同样领先。这些指标衡量生成运动与真实运动在语义匹配度、分布相似度、多模态保持度和多样性上的表现，FID 越低越好，其余指标越接近真实运动越好。相比确定性映射方法，扩散模型的概率采样机制使 MotionDiffuse 在多样性与保真度之间取得了更好的平衡。

**KIT-ML 数据集**（Table 2）上，MotionDiffuse 的 Top-1 R Precision 为 0.417，FID 为 1.954，同样优于基线方法。KIT-ML 规模较小，对模型的泛化能力要求更高，MotionDiffuse 在此数据集上的表现验证了其文本条件软注入策略的有效性。

在 **动作条件运动生成**任务（Table 5）上，MotionDiffuse 在 **HumanAct12** 数据集上取得 FID 0.07，在 **UESTC** 数据集上取得 FID 9.10，均优于 **Action2Motion** (Guo et al., ACM Multimedia 2020) 和 **ACTOR** (Petrovich et al., ICCV 2021) 等基线。这表明扩散模型框架对动作标签条件同样具有良好的适应性。

![[assets/figures/papers/paper_list_l11_MotionDiffuse_Text_Driven_Human_Motion_Generation_with_Diffusion_Model/figures/009_Table_5.jpg]]
*Table 5: Quantitative results for Action-conditioned Motion Generation. As for UESTC dataset, we report FID on the test split. MM: MultiModality*

定性结果（Figure 4）显示，MotionDiffuse 对同一文本提示能生成语义准确且姿态多样的运动序列，而 Guo et al. (2022) 的确定性方法在多样性上明显受限。

### 消融实验

消融实验围绕三个关键设计展开：CLIP 预训练权重、高效注意力机制、潜在维度和 Transformer 层数。

**CLIP 预训练与高效注意力**（Table 3）：在 KIT-ML 测试集上，移除 CLIP 预训练权重且不使用高效注意力时，Top-1 R Precision 从 0.417 骤降至 0.136，FID 从 1.954 升至 5.186。仅恢复 CLIP 预训练可提升 Top-1 R Precision 至 0.367，仅恢复高效注意力可提升至 0.157，两者同时启用才达到最佳性能。这表明 CLIP 的语义先验和高效注意力对文本-运动对齐至关重要。

**潜在维度与层数**（Table 4）：在 KIT-ML 上，潜在维度从 256 提升至 512 时，Top-1 R Precision 从 0.095–0.209 跃升至 0.405–0.417，FID 从 3.0–5.0 降至 1.9–2.1。相比之下，层数从 4 层增至 12 层的收益较小。这说明潜在维度是比层数更关键的容量瓶颈。

在 HumanAct12 动作条件任务上（Table 6），潜在维度 512 配合 8–12 层 Transformer 取得最优 FID 0.07 和 Accuracy 0.996，与文本驱动任务的结论一致。

![[assets/figures/papers/paper_list_l11_MotionDiffuse_Text_Driven_Human_Motion_Generation_with_Diffusion_Model/figures/010_Table_6.jpg]]
*Table 6: Ablation of the latent dimension and the number of transformer layers. All results are reported on the HumanAct12 dataset*

### 多层次操控能力验证

MotionDiffuse 的核心创新之一是通过噪声插值实现身体部位独立控制和长序列多动作生成。在 **BABEL 数据集**（Figure 5）上的定性实验表明：
- **身体部位控制**：给定“左臂挥手，右臂保持静止”等复合文本描述，模型能对躯干、四肢分别施加独立的噪声估计，并通过掩码和梯度校正项（见 Body-part noise interpolation 公式）实现平滑过渡，避免部位交界处的运动断裂。
- **长序列生成**：给定分段文本描述（如“先走路，然后坐下”），模型对每个时间区间独立估计噪声，再通过时间插值与校正项（见 Time-varied noise interpolation 公式）合成连贯的长序列运动。这突破了固定长度或单动作生成的限制。

### 失败模式与局限

尽管整体性能优异，MotionDiffuse 存在以下局限：
1. **推理速度慢**：扩散模型需要多步迭代去噪（通常数十至上百步），难以满足实时运动生成需求。这是 DDPM 框架的固有瓶颈，作者将此列为未来工作方向。
2. **运动表征单一**：当前 pipeline 仅接受一种运动表征形式，无法跨数据集泛化。作者提出未来需构建能同时适配多种运动表征的通用框架，但未给出具体方案。
3. **复杂文本的边界情况**：对于涉及多个身体部位且动作语义冲突的描述（如“左手画圆，右手画方”），噪声插值的校正项可能不足以消除部位间的运动伪影，该点需通过更多定性样本进行人工验证。

![[assets/figures/papers/paper_list_l11_MotionDiffuse_Text_Driven_Human_Motion_Generation_with_Diffusion_Model/figures/004_Table_1.jpg]]
*Table 1: Quantitative results on the HumanML3D test set. All methods use the real motion length from the ground truth. ‘→’ means results are better if the metric is closer to the real motions. We run all the evaluation 20 times and ± indicates the 95% confidence interval. The best results are in bold*

![[assets/figures/papers/paper_list_l11_MotionDiffuse_Text_Driven_Human_Motion_Generation_with_Diffusion_Model/figures/005_Table_2.jpg]]
*Table 2: Quantitative results on the KIT-ML test set. All methods use the real motion length from the ground truth*

![[assets/figures/papers/paper_list_l11_MotionDiffuse_Text_Driven_Human_Motion_Generation_with_Diffusion_Model/figures/006_Table_3.jpg]]
*Table 3: Ablation of the pretrained CLIP and the efficient attention technique. All results are reported on the KIT-ML test set*

![[assets/figures/papers/paper_list_l11_MotionDiffuse_Text_Driven_Human_Motion_Generation_with_Diffusion_Model/figures/008_Table_4.jpg]]
*Table 4: Ablation of the latent dimension and the number of transformer layers. All results are reported on the KIT-ML test set*

## 定位与知识库关联

### 与现有方法的关系

MotionDiffuse 将文本驱动运动生成从确定性映射范式推向了概率生成范式。在它之前，主流方法可归为两类：基于 VAE/GAN 的确定性生成和基于动作标签的条件生成。

**确定性文本-运动映射方法**构成了直接的前置基线。**TEMOS** 和 **MotionCLIP** 采用 VAE 或 CLIP 引导的联合嵌入，将文本直接映射为单一运动序列，缺乏对“一对多”映射的建模能力。**T2M**（Guo et al., CVPR 2022）引入了 VAE 与 Transformer 的组合，在 HumanML3D 上取得了当时最优的文本-运动匹配精度，但其生成过程仍是确定性的——给定同一文本，输出缺乏多样性。**Language2Pose**（Ahuja and Morency, 3DV 2019）则采用序列到序列的回归方式，同样受限于确定性输出。

**动作条件运动生成方法**为 MotionDiffuse 提供了另一个参照系。**Action2Motion**（Guo et al., ACM Multimedia 2020）和 **ACTOR**（Petrovich et al., ICCV 2021）分别使用 VAE 和 Transformer 进行动作类别到运动的生成，但它们的条件信号是离散的动作标签，而非自由形式的自然语言描述，因此无法处理细粒度、多时间段的文本指令。

MotionDiffuse 的核心差异在于将**去噪扩散概率模型（DDPM）**引入运动生成。这一选择带来了三个根本性变化：
1. **概率映射**：扩散模型天然支持从同一文本条件中采样出多样化的运动序列，解决了确定性方法的多样性瓶颈。
2. **显式序列保留**：DDPM 在去噪过程中始终保留运动序列的显式形式（而非压缩到隐变量后再解码），使得在生成过程中施加额外约束成为可能——这是 VAE 和 GAN 架构难以实现的。
3. **软性文本注入**：通过交叉注意力（Cross-Attention）和风格化模块（Stylization Block）将文本条件软性地融入去噪过程，而非硬性地将文本编码为单一条件向量。

### 适用边界

MotionDiffuse 的能力边界由其扩散模型架构和训练数据共同定义：

**适用场景**：
- **文本驱动的全身运动生成**：在 HumanML3D 和 KIT-ML 等文本-运动配对数据集上表现优异，能够处理从简单动作（如“走路”）到复杂描述（如“一个人先走几步然后停下来挥手”）的多层次文本。
- **身体部位独立控制**：通过噪声插值（Noise Interpolation）机制，可以对不同身体部位分别指定文本条件，实现“上半身挥手、下半身走路”等复合控制。
- **长序列多动作生成**：通过时间区间噪声插值，支持将多个时间段的文本描述拼接为连贯的长序列运动。
- **动作条件生成**：在 HumanAct12 和 UESTC 等动作标签数据集上同样有效，表明框架对条件信号类型具有一定的通用性。

**不适用或受限场景**：
- **实时生成**：扩散模型需要多步迭代去噪（通常数十到数百步），推理延迟远高于单步前向的 VAE 或 GAN 方法，不适合需要实时响应的交互式应用。
- **跨数据集泛化**：当前 pipeline 仅接受单一形式的运动表征（如关节旋转或位置），无法同时适配不同骨骼拓扑或运动格式的数据集。论文明确将此列为未来工作方向。
- **物理合理性保证**：生成的运动会通过数据驱动的分布学习来逼近真实运动，但缺乏显式的物理约束（如足部滑动、关节角度限制），在极端文本条件下可能产生违反物理规律的结果。

### 局限与开放问题

论文明确指出的局限性和开放问题包括：

**推理效率瓶颈**：扩散模型的多步去噪是推理速度的主要障碍。如何减少去噪步骤数（如通过蒸馏、隐空间扩散或高阶求解器）以实现接近实时的运动生成，是直接的技术挑战。

**运动表征的统一性**：当前方法针对特定数据集设计运动表征，无法在多个数据集上联合训练或迁移。构建一种通用的运动表征框架，使其同时适应 HumanML3D、KIT-ML、HumanAct12 等不同数据集的骨骼结构和标注格式，是扩展方法适用性的关键。

**文本理解的深度**：虽然 CLIP 预训练文本编码器提供了较强的语义理解能力，但对于涉及空间关系（如“绕过障碍物”）、物理交互（如“推一个重物”）或情感表达（如“沮丧地走”）的复杂文本，生成质量仍有提升空间。这些场景可能需要引入场景上下文或物理仿真作为额外条件。

**评估指标的对齐**：论文使用 FID、R Precision、MultiModal Dist 和 Diversity 等指标，但这些指标与人类感知质量的对应关系尚未充分验证。特别是 Diversity 指标可能被模型通过生成不合理的抖动来“作弊”提升，需要更可靠的多样性评估方法。

> **注意**：以上适用边界分析和开放问题中的部分推断（如物理合理性、评估指标对齐的具体机制）基于对方法架构的分析，论文原文未对此进行系统性实验验证，需要后续研究确认。

## 原文 PDF

![[paperPDFs/TPAMI_2023/MotionDiffuse_Text_Driven_Human_Motion_Generation_with_Diffusion_Model.pdf]]
