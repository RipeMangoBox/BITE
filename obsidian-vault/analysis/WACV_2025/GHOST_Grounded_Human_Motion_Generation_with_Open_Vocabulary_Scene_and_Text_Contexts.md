---
title: GHOST Grounded Human Motion Generation with Open Vocabulary Scene and Text Contexts
type: paper
paper_level: A
venue: WACV
year: 2025
pdf_ref: paperPDFs/WACV_2025/GHOST_Grounded_Human_Motion_Generation_with_Open_Vocabulary_Scene_and_Text_Contexts.pdf
project_link: null
code_link: null
aliases:
- GGHMGOVSTC
tags:
- WACV_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 将封闭词汇场景编码器替换为通过开放词汇知识蒸馏获得的、与CLIP文本特征空间对齐的点云编码器，并在微调时加入目标物体边界框回归和类别分类正则化，从而简化并强化文本-场景对齐。
primary_logic: 通过蒸馏开放词汇图像分割模型（如OpenSeg）的文本对齐2D特征到3D场景编码器，可以在预训练阶段即建立鲁棒的文本-场景共享特征空间；在条件运动生成微调时，额外回归目标物体边界框和分类物体类别，能显著提升模型对物体位置、尺寸和语义的理解，大幅减少目标物体距离。
claims:
- GHOST将开放词汇场景编码器集成到cVAE架构中，建立了文本与场景之间的鲁棒连接。
- 通过知识蒸馏从开放词汇语义图像分割模型获得共享文本-场景特征空间，并在微调时加入回归目标物体类别和尺寸的正则化损失。
- 在HUMANISE数据集上，目标物体距离指标相比先前最优基线模型最高降低30%。
- 在walk子集上，GHOST OpenSeg将目标物体距离从1.370 m降至0.952 m，在整个数据集上从1.008 m降至0.732 m。
---

# GHOST Grounded Human Motion Generation with Open Vocabulary Scene and Text Contexts

> [!tip] 核心洞察
> 通过蒸馏开放词汇图像分割模型（如OpenSeg）的文本对齐2D特征到3D场景编码器，可以在预训练阶段即建立鲁棒的文本-场景共享特征空间；在条件运动生成微调时，额外回归目标物体边界框和分类物体类别，能显著提升模型对物体位置、尺寸和语义的理解，大幅减少目标物体距离。

| 字段 | 内容 |
|------|------|
| 中文题名 | GHOST：基于开放词汇场景与文本上下文的人体动作生成 |
| 英文题名 | GHOST Grounded Human Motion Generation with Open Vocabulary Scene and Text Contexts |
| 会议/期刊 | WACV 2025 |
| Links |  |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | GHOST |
| Dataset | HUMANISE, Perceptual Study |

> [!tip] 效果简介
> - HUMANISE (walk subset) 上，Goal Object Distance (m) 0.952 (GHOST OpenSeg) vs 1.370 (HUMANISE cVAE) (-0.418 (30.5% reduction))。
> - HUMANISE (all actions) 上，Goal Object Distance (m) 0.732 (GHOST OpenSeg) vs 1.008 (HUMANISE cVAE) (-0.276 (27.4% reduction))。
> - Perceptual Study 上，User Preference Rate (%) 63.27 (GHOST OpenSeg) vs 36.73 (HUMANISE cVAE, by complement) (+26.54 percentage points)。

## 概要

**问题瓶颈**：现有文本-场景条件人体动作生成方法（如 HUMANISE cVAE，Wang et al., NeurIPS 2022）采用封闭词汇场景编码器，其输出特征空间与开放词汇文本编码器不匹配，迫使融合模块从有限的合成数据中从头学习文本-场景对齐，导致动作定位不准确，频繁偏向场景中心。

**核心洞察**：GHOST 通过两步策略建立文本-场景之间的鲁棒连接——首先利用开放词汇知识蒸馏，将 2D 图像分割模型（如 OpenSeg）中文本对齐的像素级特征迁移至 3D 点云编码器，在预训练阶段即构建共享的视觉-语言特征空间；随后在条件运动生成微调时，引入目标物体边界框回归和类别分类两项正则化损失，显著增强模型对物体位置、尺寸和语义的理解能力。

**方法定位**：GHOST 延续 cVAE 条件生成框架，关键改动在于将封闭词汇场景编码器替换为 Point Transformer U-Net 架构的开放词汇编码器，并通过 OpenScene 蒸馏损失实现与 CLIP 文本特征空间的对齐。运动编码器-解码器模块与 HUMANISE cVAE 保持一致。

**主要结果**：在 HUMANISE 数据集上，GHOST OpenSeg 变体将目标物体距离指标相比先前最优基线降低最高约 30%（walk 子集从 1.370 m 降至 0.952 m，全动作集从 1.008 m 降至 0.732 m）。感知研究中，63.27% 的参与者偏好 GHOST 生成的样本。消融实验确认，文本与场景编码器的对齐替换对 grounding 改善贡献最为显著。

### 问题定义：文本与场景条件化的人体动作生成

文本与场景条件化的人体动作生成任务要求模型根据给定的自然语言描述 $\boldsymbol{L}$ 和 3D 场景点云 $\boldsymbol{S}$，生成符合语义且与场景几何一致的人体运动序列 $\pmb \Theta = \{ t , r , \pmb \theta \} \in \mathbb { R } ^ { T \times ( 3 + 6 + J \cdot 3 ) }$，即建模条件概率 $p \left( \boldsymbol { \Theta } | \boldsymbol { L } , \boldsymbol { S } \right)$。其中 $t$ 为全局平移、$r$ 为全局朝向、$\pmb \theta$ 为身体姿态参数，$T$ 为序列长度，$J$ 为关节数。该任务的核心挑战在于实现精确的 grounding——使生成的人体动作在空间位置上与文本指定的目标物体紧密关联，而非仅生成场景中心偏向的泛化动作。

### 现有方法的瓶颈：封闭词汇场景编码导致的模态失配

当前最优基线模型 **HUMANISE cVAE**（Wang et al., NeurIPS 2022）采用封闭词汇场景编码器，其输出特征空间仅覆盖预定义的一组语义类别，与开放词汇的文本编码器（如 CLIP）的特征空间存在根本性不匹配。这种模态失配迫使融合模块在有限的合成数据上从零开始学习文本-场景对齐关系，导致以下两个关键问题：

1. **定位偏差**：模型倾向于将动作生成在场景中心位置，而非文本指定的目标物体附近（见 Fig. 1a）。
2. **语义理解薄弱**：由于缺乏预训练的文本-场景共享表示，模型对物体位置、尺寸和类别的语义理解不足，难以实现精确的 goal object grounding。

从架构层面看，HUMANISE cVAE 仅通过回归目标物体中心点坐标（$L_{center}$）作为 grounding 正则化，这种弱监督信号无法充分约束模型学习物体边界和类别信息。

### 本文动机：建立开放词汇的文本-场景共享特征空间

针对上述瓶颈，GHOST 的核心动机是通过引入开放词汇知识蒸馏，在预训练阶段即建立文本与场景之间的鲁棒共享特征空间，从而从根本上解决模态失配问题。具体而言：

- **开放词汇场景编码**：将封闭词汇场景编码器替换为通过知识蒸馏获得的、与 CLIP 文本特征空间对齐的点云编码器，使文本和场景模态在预训练阶段即实现初始对齐（见 Fig. 2b）。
- **强化 grounding 正则化**：在条件运动生成微调阶段，除保留中心点回归外，额外引入目标物体边界框角点回归（$L_{bbox}$）和类别分类（$L_{class}$）正则化，提升模型对物体位置、尺寸和语义的感知能力。

这一设计使得融合模块无需从零学习文本-场景对齐，而是从一个已具备开放词汇语义理解能力的共享特征空间出发，显著简化了 grounding 的学习难度，从而大幅降低目标物体距离指标（最高达 30% 的降低）。

## 核心方法与创新机理

GHOST 的核心创新在于**将开放词汇知识蒸馏引入场景编码器，并与文本编码器在 CLIP 空间中对齐**，从根本上解决了 HUMANISE cVAE（Wang et al., NeurIPS 2022）中文本-场景特征空间不匹配的问题。具体而言，GHOST 通过三个关键变更槽位（changed slots）实现了这一突破：

### 1. 从封闭词汇到开放词汇的场景编码器

HUMANISE cVAE 采用封闭词汇场景编码器，其输出为固定类别的语义标签，与开放词汇的文本编码器特征空间存在本质性错配。这迫使融合模块从有限的合成数据中**从头学习文本-场景对齐**，导致模型倾向于将动作生成在场景中心，而非目标物体附近。

GHOST 将场景编码器替换为通过 **OpenScene 损失**预训练的 Point Transformer U-Net，该损失最大化 3D 场景特征与来自开放词汇图像分割教师模型（如 OpenSeg）的文本对齐 2D 像素特征之间的余弦相似度：

$$\mathcal{L}_{cos} = 1 - \cos \left( \frac{1}{R} \sum_{j=1}^{R} \left[ \mathcal{E}^{2D}(I_j) \right]_{(S_{\cdot,:3}P_j),\cdot} \mathcal{E}^{3D}(S) \right)$$

这一蒸馏过程使 3D 场景编码器的输出特征与 CLIP 文本特征共享同一空间，**在预训练阶段即建立了文本-场景的初始对齐**，大幅降低了后续融合模块的学习负担。

### 2. 增强的目标物体正则化

HUMANISE cVAE 仅通过回归目标物体中心点（$\mathcal{L}_{center}$）来正则化 grounding，缺乏对物体尺寸和类别的感知。GHOST 引入了两个新颖的正则化损失：

- **$\mathcal{L}_{bbox}$**：对目标物体的轴对齐边界框角点坐标进行均方误差回归，使模型显式感知物体的空间范围和尺寸。
- **$\mathcal{L}_{class}$**：对目标物体进行 9 类 ScanNet 类别分类，强化模型对物体语义的判别能力。

整体正则化损失为：

$$\mathcal{L}_{reg} = \lambda_{kl} \mathcal{L}_{kl} + \lambda_{action} \mathcal{L}_{action} + \lambda_{center} \mathcal{L}_{center} + \lambda_{bbox} \mathcal{L}_{bbox} + \lambda_{class} \mathcal{L}_{class}$$

消融实验证实，移除 $\mathcal{L}_{bbox}$ 和 $\mathcal{L}_{class}$ 会导致目标物体距离显著增加（Table 3, Fig. 5），证明这两项正则化对精确定位不可或缺。

### 3. 文本-场景对齐的根本性改进

消融实验揭示了模态对齐的决定性作用：在 walk 子集上，将 BERT 文本编码器替换为与场景编码器共享开放词汇特征空间的 OpenSeg 文本编码器，目标物体距离从 1.425 m 降至 0.952 m；将封闭词汇场景编码器替换为 OpenSeg 蒸馏的开放词汇场景编码器，距离从 1.021 m 降至 0.952 m（Table 3）。这表明**文本和场景编码器的对齐是 grounding 改善的最关键因素**，其影响远大于其他组件变更。

综合来看，GHOST 的创新并非简单的模块堆砌，而是通过**预训练阶段的开放词汇知识蒸馏**和**微调阶段的增强正则化**，构建了一条从场景理解到动作定位的因果链条：开放词汇场景编码器提供了与文本对齐的丰富语义特征，边界框回归和类别分类进一步强化了模型对目标物体的位置、尺寸和语义的精确感知，最终实现了目标物体距离最高 30% 的降低（Table 1）。

GHOST 的整体框架遵循条件变分自编码器（cVAE）范式，其核心目标是建模给定文本描述 $\boldsymbol{L}$ 和场景点云 $\boldsymbol{S}$ 时人体运动参数 $\boldsymbol{\Theta}$ 的条件概率 $p(\boldsymbol{\Theta} | \boldsymbol{L}, \boldsymbol{S})$。与基线模型 **HUMANISE cVAE**（Wang et al., NeurIPS 2022）相比，GHOST 在三个关键环节上进行了重构：场景编码器的词汇类型、文本-场景对齐的建立方式，以及目标物体的正则化策略。

### 两阶段训练流程

GHOST 采用“预训练-微调”的两阶段策略，从根本上解决了 HUMANISE cVAE 中文本与场景特征空间不匹配的问题。

**第一阶段：开放词汇场景编码器预训练。** 如图 3 所示，该阶段的目标是通过知识蒸馏，将开放词汇图像分割教师模型（如 OpenSeg）的文本对齐 2D 特征迁移到 3D 场景编码器中。具体而言，对于给定的场景点云 $\boldsymbol{S}$ 及其 $R$ 个渲染视角的图像 $\{I_j\}$，预训练损失最大化 3D 编码器输出与对应像素的 2D 文本对齐特征之间的余弦相似度：

$$\mathcal{L}_{cos} = 1 - \cos \left( \frac{1}{R} \sum_{j=1}^{R} \left[ \mathcal{E}^{2D}(I_j) \right]_{(S_{\cdot,:3}P_j),\cdot} \mathcal{E}^{3D}(S) \right)$$

这一过程在预训练阶段即建立了文本与场景之间的共享视觉-语言特征空间，使得场景编码器的输出天然与 CLIP 文本特征空间对齐。场景编码器采用 Point Transformer U-Net 架构，包含编码器-解码器及跳跃连接，以捕获多尺度场景几何信息。

**第二阶段：条件运动生成微调。** 预训练完成后，场景编码器被集成到 cVAE 框架中进行端到端微调。整个 pipeline 的模块组成与数据流如下：

- **文本编码器（冻结）**：采用开放词汇文本编码器，将文本描述 $\boldsymbol{L}$ 映射到与场景特征对齐的共享空间。
- **场景编码器（Point Transformer U-Net）**：从 RGB 场景点云中提取文本对齐的 3D 特征，权重由预训练阶段初始化。
- **融合模块（Self-Attention + MLP）**：将文本特征与场景特征融合，生成条件潜变量 $\boldsymbol{z}_c$，作为运动解码器的条件输入。
- **运动编码器（双向 GRU）**：将运动参数序列编码为高斯分布的均值 $\boldsymbol{\mu}$ 和协方差 $\boldsymbol{\Sigma}$。
- **运动解码器（Transformer Decoder）**：从隐变量 $\boldsymbol{z}$ 和条件 $\boldsymbol{z}_c$ 重建运动参数序列 $\boldsymbol{\Theta} = \{ \boldsymbol{t}, \boldsymbol{r}, \boldsymbol{\theta} \}$，分别对应全局平移、全局朝向和身体姿态。
- **目标物体边界框回归器**：预测目标物体的轴对齐边界框角点坐标，以 MSE 损失 $\mathcal{L}_{bbox}$ 监督。
- **目标物体类别分类器**：对目标物体进行 9 类 ScanNet 类别分类，以交叉熵损失 $\mathcal{L}_{class}$ 监督。

运动模块（运动编码器与解码器）的架构与 HUMANISE cVAE 保持一致，确保对比的公平性。

### 训练损失函数

微调阶段的总损失由运动重建损失和正则化损失组成：

$$\mathcal{L} = \mathcal{L}_{rec} + \mathcal{L}_{reg}$$

其中，重建损失对全局平移、全局朝向、身体姿态和规范化网格顶点施加 L1 损失：

$$\mathcal{L}_{rec} = \mathcal{L}_{t} + \lambda_{r} \mathcal{L}_{r} + \lambda_{\theta} \mathcal{L}_{\theta} + \lambda_{M} \mathcal{L}_{M}$$

正则化损失在 HUMANISE cVAE 原有的 KL 散度（$\mathcal{L}_{kl}$）、动作分类（$\mathcal{L}_{action}$）和目标物体中心点回归（$\mathcal{L}_{center}$）基础上，新增了 GHOST 的两个核心正则化项：

$$\mathcal{L}_{reg} = \lambda_{kl} \mathcal{L}_{kl} + \lambda_{action} \mathcal{L}_{action} + \lambda_{center} \mathcal{L}_{center} + \lambda_{bbox} \mathcal{L}_{bbox} + \lambda_{class} \mathcal{L}_{class}$$

边界框回归和类别分类正则化的引入，使模型不仅关注目标物体的位置，还能感知其尺寸和语义类别，从而显著提升 grounding 精度。

### 与 HUMANISE cVAE 的关键差异

图 2 清晰地对比了两者的架构差异。HUMANISE cVAE 使用封闭词汇场景编码器，其输出特征空间与开放词汇文本编码器不匹配，迫使融合模块从有限的合成数据中从头学习文本-场景对齐；其 grounding 仅通过回归目标物体中心点进行弱正则化。GHOST 则通过开放词汇知识蒸馏在预训练阶段建立初始对齐，并在微调时以边界框回归和类别分类强化 grounding，形成了更鲁棒的文本-场景连接。

![[assets/figures/papers/paper_list_l1813_GHOST_Grounded_Human_Motion_Generation_with_Open_Vocabulary_Scene_and_Te/figures/005_Figure_3.jpg]]
*Figure 3: Schematic diagram of the pretraining and training phases of our proposed GHOST framework for text-and-scene-conditional human motion generation. (a) Pretraining involves maximizing the cosine similarity between our scene point cloud encoder and corresponding text-aligned 2D viewpoint pixel features, computed by an open vocabulary image segmentation teacher model. This ensures that our features align with text embeddings in a shared space. We use a Point Transformer U-Net scene encoder. (b) Training employs a Conditional Variational Autoencoder (cVAE) architecture for motion generation, conditioned on both text and scene encoder outputs. The pretrained scene encoder weights are fine-tuned wi...*

### 问题定义与条件概率建模

GHOST 延续 HUMANISE cVAE 的条件生成框架，将文本-场景条件人体动作生成建模为条件概率分布的学习问题。给定自然语言描述 $\boldsymbol{L}$ 和 3D 场景点云 $\boldsymbol{S}$，目标是建模人体运动参数序列 $\pmb\Theta$ 的条件分布：

$$p(\boldsymbol{\Theta} | \boldsymbol{L}, \boldsymbol{S})$$

其中运动参数 $\pmb\Theta = \{ t, r, \pmb\theta \} \in \mathbb{R}^{T \times (3 + 6 + J \cdot 3)}$ 包含 $T$ 帧的全局平移 $t$、全局朝向 $r$ 和 $J$ 个关节的身体姿态 $\pmb\theta$。该分布的建模通过条件变分自编码器（cVAE）实现，运动模块架构与原始 HUMANISE cVAE 保持一致，核心改动集中在场景编码器及其与文本模态的对齐机制上。

### 开放词汇场景编码器预训练

GHOST 的核心创新之一是将封闭词汇场景编码器替换为通过知识蒸馏获得的开放词汇场景编码器。预训练阶段采用 Point Transformer U-Net 架构（含编码器-解码器及跳跃连接）作为 3D 场景编码器 $\mathcal{E}^{3D}$，通过 OpenScene 损失函数最大化其输出与开放词汇 2D 图像分割教师模型 $\mathcal{E}^{2D}$ 提取的文本对齐像素特征之间的余弦相似度：

$$\mathcal{L}_{cos} = 1 - \cos\left(\frac{1}{R}\sum_{j=1}^{R}\left[\mathcal{E}^{2D}(I_j)\right]_{(S_{\cdot,:3}P_j),\cdot}\mathcal{E}^{3D}(S)\right)$$

其中 $R$ 为渲染的视角数量，$I_j$ 为第 $j$ 个视角的 2D 图像，$P_j$ 为对应的投影矩阵，$S_{\cdot,:3}P_j$ 将 3D 点云投影到 2D 像素坐标以索引对应的文本对齐特征。该损失函数的核心作用是在预训练阶段即建立 3D 场景特征与 CLIP 文本特征空间的对齐，使得场景编码器输出天然与文本编码器（如 OpenSeg 文本编码器）处于共享的视觉-语言特征空间，从而在后续 cVAE 微调前即获得初始的文本-场景对齐能力。

### cVAE 训练与多层级正则化

在微调阶段，预训练的场景编码器权重被加载并随 cVAE 整体进行端到端优化。总损失函数由运动重建损失 $\mathcal{L}_{rec}$ 和正则化损失 $\mathcal{L}_{reg}$ 组成：

$$\mathcal{L} = \mathcal{L}_{rec} + \mathcal{L}_{reg}$$

**运动重建损失**对生成的运动参数与真实运动参数之间的差异进行约束，包含四个分量的 L1 损失：

$$\mathcal{L}_{rec} = \mathcal{L}_{t} + \lambda_{r} \mathcal{L}_{r} + \lambda_{\theta} \mathcal{L}_{\theta} + \lambda_{M} \mathcal{L}_{M}$$

其中 $\mathcal{L}_{t}$ 为全局平移损失，$\mathcal{L}_{r}$ 为全局朝向损失，$\mathcal{L}_{\theta}$ 为身体姿态损失，$\mathcal{L}_{M}$ 为规范化网格顶点损失。对应的权重设置为 $\lambda_{r}=1.0$，$\lambda_{\theta}=\lambda_{M}=10.0$。

**正则化损失**包含五项，其中三项继承自 HUMANISE cVAE，两项为 GHOST 新增的目标物体定位正则化：

$$\mathcal{L}_{reg} = \lambda_{kl} \mathcal{L}_{kl} + \lambda_{action} \mathcal{L}_{action} + \lambda_{center} \mathcal{L}_{center} + \lambda_{bbox} \mathcal{L}_{bbox} + \lambda_{class} \mathcal{L}_{class}$$

- $\mathcal{L}_{kl}$：KL 散度损失，约束潜变量分布接近标准正态分布（$\lambda_{kl}=0.1$）
- $\mathcal{L}_{action}$：动作类别分类损失（$\lambda_{action}=0.5$）
- $\mathcal{L}_{center}$：目标物体中心点回归的 MSE 损失（$\lambda_{center}=0.1$）
- $\mathcal{L}_{bbox}$：**新增**，目标物体轴对齐边界框角点坐标的 MSE 回归损失（$\lambda_{bbox}=0.1$），使模型显式感知物体的空间范围和尺寸
- $\mathcal{L}_{class}$：**新增**，目标物体在 9 个 ScanNet 类别上的交叉熵分类损失（$\lambda_{class}=0.5$），强化对物体语义类别的判别能力

新增的 $\mathcal{L}_{bbox}$ 和 $\mathcal{L}_{class}$ 是 GHOST 在 grounding 精度上取得显著提升的关键。原始 HUMANISE cVAE 仅通过 $\mathcal{L}_{center}$ 回归目标物体中心点，但单一中心点坐标无法传递物体的尺寸和边界信息，导致生成的角色常偏向场景中心而非精确抵达目标物体附近。边界框角点回归迫使模型理解物体的三维占据范围，类别分类则强化了语义判别，两者协同作用使 grounding 精度大幅提升——消融实验表明移除这两项正则化会导致目标物体距离显著增加。

### 评估指标：目标物体距离

为量化 grounding 精度，GHOST 采用目标物体距离（Goal Object Distance）作为核心评估指标。对于给定的文本描述 $L$ 和场景 $S$，该指标计算 $K$ 个生成的人体网格与目标物体点云之间的平均最小正有符号距离：

$$d(L,S) = \frac{1}{K} \sum_{j=1}^{K} \mathrm{ReLU} \left[ \min \left( \mathrm{SDF}_{\hat{\mathcal{M}}_t^{(j)}}^{+} \left[ \mathbf{S}_{goal,:3} \right] \right) \right]$$

其中 $\hat{\mathcal{M}}_t^{(j)}$ 为第 $j$ 个生成样本在关键帧 $t$ 的人体网格，$\mathrm{SDF}^{+}$ 为正有符号距离函数，$\mathbf{S}_{goal,:3}$ 为目标物体点云的三维坐标。对于 walk、sit、lie 动作使用最后一帧 $t=T$，对于 stand up 动作使用第一帧 $t=1$，采样数 $K=10$。ReLU 函数确保仅惩罚人体网格外部的目标物体点（即未到达目标的情况），距离越小表示角色越接近目标物体。

![[assets/figures/papers/paper_list_l1813_GHOST_Grounded_Human_Motion_Generation_with_Open_Vocabulary_Scene_and_Te/figures/004_Figure_2.jpg]]
*Figure 2: Overview of our idea. Best viewed in color. We compare our GHOST cVAE with the HUMANISE cVAE [71] model. The major differences are in the text and 3D scene point cloud representations, grounding and regularization. (a) The HUMANISE cVAE architecture utilizes a closed vocabulary scene encoder producing a finite set of labels, resulting in a misalignment with the open vocabulary text feature space. This requires the fusion module to learn grounding from scratch. Grounding is regularized by regressing the center point of the goal object. (b) In contrast, our GHOST cVAE architecture employs a shared open vocabulary vision-language space for both modalities, establishing initial grounding betwee...*

## 实验与关键发现

### 核心定量结果

GHOST 在 HUMANISE 数据集上显著提升了人体动作的场景定位精度，核心指标为**目标物体距离**（Goal Object Distance），该指标衡量生成的人体网格与指定目标物体点云之间的平均最小正有符号距离，距离越小表示定位越准确。

在 walk 动作子集上，GHOST OpenSeg 将目标物体距离从 HUMANISE cVAE 的 1.370 m 降至 **0.952 m**，降幅达 30.5%。在整个数据集（全部动作类别）上，距离从 1.008 m 降至 **0.732 m**，降幅为 27.4%（Table 1）。这一结果验证了开放词汇知识蒸馏所建立的共享文本-场景特征空间，能够从根本上改善条件生成中的模态对齐质量。

![[assets/figures/papers/paper_list_l1813_GHOST_Grounded_Human_Motion_Generation_with_Open_Vocabulary_Scene_and_Te/figures/006_Table_1.jpg]]
*Table 1: Quantitative results of generation experiments on the HUMANISE dataset. The winning numbers are highlighted in bold for each action subset*

### 感知研究验证

为评估生成动作的主观自然度，研究进行了双盲感知用户实验（27 名参与者）。GHOST OpenSeg 生成的样本在 **63.27%** 的对比中被参与者偏好，显著优于 HUMANISE cVAE 基线（Table 2）。所有 27 名参与者均表现出对 GHOST 的总体偏好，表明开放词汇场景理解不仅提升了数值指标，也带来了可感知的交互质量改进。

![[assets/figures/papers/paper_list_l1813_GHOST_Grounded_Human_Motion_Generation_with_Open_Vocabulary_Scene_and_Te/figures/007_Table_2.jpg]]
*Table 2: Quantitative results of the perceptual study of agnostic all-actions models trained on the entire HUMANISE dataset. The winning numbers are highlighted in bold*

### 消融实验

消融实验在 walk 动作子集上进行，系统拆解了各组件的贡献（Table 3）：

![[assets/figures/papers/paper_list_l1813_GHOST_Grounded_Human_Motion_Generation_with_Open_Vocabulary_Scene_and_Te/figures/008_Table_3.jpg]]
*Table 3: Quantitative results of ablation experiments on the walk action subset of the HUMANISE dataset. The winning number is highlighted in bold*

- **文本编码器的影响**：将 GHOST 的 OpenSeg 文本编码器替换为 BERT 编码器后，目标物体距离从 0.952 m 上升至 1.425 m。这直接证明了与场景编码器共享开放词汇特征空间对于文本-场景对齐的关键作用。
- **场景编码器的影响**：将开放词汇场景编码器替换为封闭词汇场景编码器后，距离从 0.952 m 上升至 1.021 m。这表明通过 OpenScene 蒸馏获得的文本对齐 3D 特征，比传统封闭词汇语义特征更有利于 grounding 任务。
- **正则化损失的影响**：移除边界框回归（$\mathcal{L}_{bbox}$）和类别分类（$\mathcal{L}_{class}$）正则化后，目标物体距离显著增加。定性结果（Figure 5）也显示，缺少这两个正则化项时，生成的角色往往无法精确抵达目标物体附近，验证了回归物体边界框角点坐标和分类物体类别对于提升模型对物体位置、尺寸和语义理解的必要性。

![[assets/figures/papers/paper_list_l1813_GHOST_Grounded_Human_Motion_Generation_with_Open_Vocabulary_Scene_and_Te/figures/010_Figure_5.jpg]]
*Figure 5: Qualitative generation results of ablation on the walk action subset of the HUMANISE dataset. We display 3 samples for the same text, with 1 generated by each model. Ground truth goal object is highlighted in red. Our GHOST model places the character significantly closer to the goal with our proposed regularization losses*

### 定性分析

Figure 4 展示了 GHOST 与 HUMANISE cVAE 在相同文本条件下的生成对比。GHOST 能够将角色放置在显著更接近目标物体的位置，注意力图（紫色相机视锥）也表明模型对目标物体区域有更强的空间关注。然而，论文也坦承仍存在目标物体识别错误、角色朝向错误和场景穿透等问题，这些失败模式提示当前开放词汇教师模型（如 OpenSeg）的视觉语言理解能力仍有提升空间。

### 公平性说明

所有模型采用相同的训练超参数（Adam 优化器，学习率 $1\times10^{-4}$，batch size 24，150 epochs），评估采用统一的 Goal Object Distance 指标和相同的 $K=10$ 采样数。消融实验因计算量限制仅在 walk 子集上进行，但其结论与全数据集趋势一致，具有代表性。

## 定位与知识库关联

### 方法沿革与基线关系

GHOST 的核心技术路线建立在对 **HUMANISE cVAE**（Wang et al., NeurIPS 2022）的批判性继承之上。HUMANISE 首次将条件变分自编码器（cVAE）引入文本-场景双条件人体动作生成任务，但其架构存在一个关键瓶颈：场景编码器采用在固定类别语义分割上预训练的封闭词汇模型，输出的特征空间与开放词汇的文本编码器（如 CLIP）不兼容。这迫使融合模块必须在有限的合成数据上从零开始学习文本-场景对齐，导致模型倾向于将动作生成在场景中心位置，而非精确地定位于目标物体附近。

GHOST 从两个维度突破了这一瓶颈：

1. **特征空间对齐**：将封闭词汇场景编码器替换为通过开放词汇知识蒸馏获得的点云编码器。具体而言，GHOST 在预训练阶段使用 OpenScene 损失函数，最大化 3D 场景编码器输出与开放词汇 2D 图像分割模型（如 OpenSeg）的文本对齐像素特征之间的余弦相似度，从而在 CLIP 共享空间中建立文本-场景的初始对齐。这一策略使得场景编码器在进入 cVAE 微调之前，已具备与文本编码器兼容的特征表示。

2. **目标物体正则化强化**：在 cVAE 微调阶段，GHOST 在原有中心点回归（L_center）的基础上，新增了目标物体边界框角点回归（L_bbox）和类别分类（L_class）两个正则化损失。这使得模型不仅需要预测目标物体的位置，还需要理解其尺寸和语义类别，从而显著提升了 grounding 精度。

从架构层面看，GHOST 的场景编码器从 HUMANISE 的 Point Transformer 编码器升级为 Point Transformer U-Net（含编码器-解码器及跳跃连接），以更好地支持逐点特征蒸馏。运动模块（Motion Encoder 和 Motion Decoder）则保持与 HUMANISE cVAE 完全相同的架构，确保了对比的公平性。

### 在文本-场景条件动作生成中的定位

GHOST 在文本-场景条件人体动作生成任务中处于当前最优水平。其三个变体（GHOST OpenSeg、GHOST LSeg、GHOST OpenScene）在目标物体距离指标上均显著优于 HUMANISE cVAE 基线，同时参数量约为基线的 1.5 至 3.9 倍（Fig. 1c）。

该方法的核心贡献在于揭示了**模态对齐**对 grounding 性能的决定性作用。消融实验（Table 3）提供了强有力的证据：将 BERT 文本编码器替换为 OpenSeg 文本编码器（共享开放词汇特征空间），目标物体距离从 1.425 m 降至 0.952 m；将封闭词汇场景编码器替换为 OpenSeg 蒸馏的开放词汇场景编码器，距离从 1.021 m 降至 0.952 m。这两项替换带来的改善幅度最大，验证了文本-场景特征空间对齐是突破性能瓶颈的关键因果杠杆。

### 适用边界与局限

尽管 GHOST 在 HUMANISE 数据集上取得了显著的性能提升，其适用边界仍受以下因素制约：

1. **数据分布限制**：模型仅在合成数据集 HUMANISE 上训练和评估。HUMANISE 基于 ScanNet 场景和 AMASS 动作捕捉数据构建，其场景点云来自 RGB-D 重建，动作来自模板化的文本描述。模型对真实扫描场景（如含噪声的 LiDAR 点云）和更自由的自然语言描述的泛化能力尚待验证。

2. **目标物体范围**：当前 grounding 机制仅针对文本指定的单个目标物体（如“走向椅子”中的椅子）。场景中其他交互对象（如障碍物、路径上的其他家具）未被显式建模，模型无法处理多物体协调的复杂交互场景。

3. **生成范式限制**：框架基于 cVAE，未探索扩散模型等可能提升生成质量和多样性的替代方案。cVAE 的隐变量采样可能限制动作的多样性和细粒度控制能力。

4. **物理合理性缺陷**：论文明确指出，生成结果仍存在目标物体识别错误、朝向错误和场景穿透问题。这表明当前的视觉语言对齐和正则化策略尚不足以完全解决物理合理性约束。

### 开放问题与后续方向

基于 GHOST 的局限性和实验结果，以下开放问题值得后续工作关注：

1. **扩散模型替代 cVAE 的可行性**：扩散模型在图像和运动生成领域已展现出优于 VAE 的生成质量和多样性。将其引入文本-场景条件动作生成，是否能进一步提升 grounding 精度和动作自然度，是一个直接且重要的研究方向。

2. **多物体 grounding 扩展**：将 grounding 机制从单一目标物体扩展到场景中的多个交互对象（如同时考虑目标物体、障碍物和支撑面），有望使模型适应更复杂的日常活动场景。

3. **接触优化后处理**：通过接触优化（contact optimization）作为后处理步骤，减少或消除场景穿透，可能是提升物理合理性的低成本路径。这一方向不改变生成模型本身，具有较高的工程可行性。

4. **开放词汇泛化**：当前模型依赖 ScanNet 的 9 个预定义物体类别。如何利用更大规模的视觉语言模型（如更强的开放词汇分割教师模型）实现真正开放词汇的目标物体理解，使其泛化到训练中未见过的物体类别，是提升实用性的关键。

5. **真实场景迁移**：将 HUMANISE 上训练的模型迁移到真实 3D 场景（如 Matterport3D 或真实室内扫描数据），需要解决合成-真实域差异问题。域自适应或基于真实数据的弱监督微调是可能的解决方案。

## 原文 PDF

![[paperPDFs/WACV_2025/GHOST_Grounded_Human_Motion_Generation_with_Open_Vocabulary_Scene_and_Text_Contexts.pdf]]
