---
title: "MOSPA: Human Motion Generation Driven by Spatial Audio"
type: paper
paper_level: A
venue: NEURIPS
year: 2025
pdf_ref: paperPDFs/NEURIPS_2025/MOSPA_Human_Motion_Generation_Driven_by_Spatial_Audio.pdf
project_link: null
code_link: null
aliases:
- MOSPA
tags:
- NEURIPS_2025
- topic/motion_animation
- topic/motion_animation/human_motion_generation
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 引入双耳空间音频特征（MFCC、Tempogram、RMS能量）以及声源位置、运动风格作为条件，利用扩散模型建模条件分布以生成空间响应的运动。
primary_logic: 通过将空间音频分解为语义、时空和能量特征，并与扩散生成模型结合，MOSPA能够生成与空间音频高度对齐的多样化人类运动。
claims:
- MOSPA在SAM数据集上取得SOTA性能，FID显著低于所有基线方法（7.981 vs EDGE 13.993）。
- 引入运动风格作为条件后，FID从10.930降至7.981，R-precision大幅度提升。
- SAM 上 FID = 7.981
- SAM 上 R-precision Top1 = 0.937
---

# MOSPA: Human Motion Generation Driven by Spatial Audio

> [!tip] 核心洞察
> 通过将空间音频分解为语义、时空和能量特征，并与扩散生成模型结合，MOSPA能够生成与空间音频高度对齐的多样化人类运动。

| 字段 | 内容 |
|------|------|
| 中文题名 | MOSPA：空间音频驱动的人体运动生成 |
| 英文题名 | MOSPA: Human Motion Generation Driven by Spatial Audio |
| 会议/期刊 | NEURIPS 2025 |
| Links | [paper](https://openreview.net/forum?id=X2r9D46kvI) |
| Topic | #topic/motion_animation #topic/motion_animation/human_motion_generation #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | MOSPA |
| Dataset | SAM |

> [!tip] 效果简介
> - SAM 上，FID 7.981 vs 13.993 (EDGE) (降低6.012)；R-precision Top1 0.937 vs 0.886 (EDGE) (提升0.051)；Diversity 23.575 vs 23.616 (Real Motion) (接近真实运动（差异0.041）)。

## 概要

**问题瓶颈**：现有音频驱动的人体运动生成方法（如音乐到舞蹈、语音到手势）依赖单声道音频特征，完全忽视了空间音频中编码的声源方向、距离等空间线索对人类运动反应的影响。同时，领域长期缺乏专用的空间音频-运动配对数据集，使得该任务无法被系统建模。

**核心思路**：MOSPA 将空间音频分解为语义特征（MFCC）、时空节奏特征（Tempogram）和能量特征（RMS），并与声源位置、运动风格共同作为条件信号，注入基于 Transformer 的扩散模型，从噪声中逐步重建与空间音频高度对齐的多样化人体运动。

**方法与知识库定位**：MOSPA 属于条件扩散生成范式。与音乐驱动舞蹈生成的 **EDGE**（Tseng et al., CVPR 2023）、**POPDG**（Luo et al., CVPR 2024）、**LODGE**（Li et al., CVPR 2024）以及 **Bailando**（Siyao et al., CVPR 2022）等基线相比，MOSPA 的关键差异在于：(1) 将输入从单声道音频替换为双耳空间音频特征（维度 2272）；(2) 引入声源位置和运动风格作为显式空间条件；(3) 采用随机掩码与残差特征融合机制增强条件利用效率。基线方法虽被适配为空间音频输入，但其架构设计未针对空间信息优化，比较存在一定局限性。

**主要结果**：在 SAM 数据集上，MOSPA 的 FID 达到 7.981，显著优于最强基线 EDGE 的 13.993（降低 6.012）；R-precision Top1 达到 0.937（EDGE 为 0.886）；多样性指标（Diversity 23.575、APD 53.915）均接近真实运动分布。消融实验表明，运动风格条件的引入是性能提升的关键因素（移除后 FID 升至 10.930），MFCC 与 Tempogram 的组合使用也显著优于单一特征。用户调研进一步验证了 MOSPA 在意图对齐、运动质量和真实相似度三个维度上的优势。

### 问题背景

空间音频（Spatial Audio）是一种携带声源方向、距离和环境反射信息的多通道音频信号，在虚拟现实、增强现实、游戏和影视制作中已被广泛采用。人类对空间音频的自然反应不仅是听觉感知，更包含丰富的身体运动——例如转头朝向声源、后退远离突然的巨响、或随环绕音乐律动。然而，现有的人体运动生成研究主要集中在两个范式：**音乐到舞蹈生成**（如 **EDGE** (Tseng et al., CVPR 2023)、**POPDG** (Luo et al., CVPR 2024)、**Bailando** (Siyao et al., CVPR 2022)）和**语音到手势生成**。这些方法处理的都是单声道或普通音频信号，完全忽视了空间音频中编码的空间特征对运动的驱动作用。

### 现有方法缺口

当前主流方法的瓶颈可归结为三个层面：

1. **特征层面的空间盲区**：现有方法提取的音频特征（如Mel频谱、MFCC）仅捕获音频的语义和节奏信息，无法表征声源的方向、距离和空间强度分布。这导致生成的运动无法对声源位置做出响应——例如，无法区分“左侧传来的脚步声”与“右侧传来的脚步声”。

2. **条件信号的单一性**：音乐到舞蹈模型通常仅以音频节奏或音乐类别作为条件，缺少对声源空间位置和运动风格的显式建模。这使得生成的运动缺乏空间指向性和风格可控性。

3. **数据集的缺失**：在MOSPA之前，不存在包含空间音频与3D人体运动配对的数据集。现有数据集（如AIST++、TED-Gesture）仅提供单声道音频与运动标注，无法支持空间音频驱动的运动生成研究。

### 本文动机

针对上述缺口，MOSPA的核心动机是提出一个**空间音频驱动的人体运动生成新任务**，并为此构建完整的数据与模型基础。具体而言：

- **新任务定义**：给定双耳空间音频信号，生成与音频的语义内容、节奏特征和空间指向性高度对齐的3D人体运动序列。
- **数据集构建**：构建**SAM（Spatial Audio-Driven Human Motion）数据集**，包含27种日常空间音频场景、49种反应类型、超过34,000秒的配对数据，并标注声源位置（SSL）。
- **方法设计**：提出**MOSPA**框架，通过提取双耳空间音频特征（MFCC、Tempogram、RMS能量），并将其与声源位置、运动风格共同作为条件，利用扩散模型建模条件分布，实现空间响应的多样化运动生成。

这一任务填补了空间音频感知与人体运动生成之间的空白，为虚拟人交互、机器人空间感知等下游应用提供了新的技术路径。

## 核心方法与创新机理

MOSPA的核心创新在于首次将**空间音频**（而非传统单声道音频）作为人体运动生成的条件信号，并通过三个“changed slots”系统性地解决了现有方法的瓶颈。

### 从单声道到双耳空间音频的特征跃迁

现有音乐/语音驱动运动生成方法（如**EDGE**、**POPDG**、**Bailando**）依赖单声道音频特征（如Mel频谱），完全忽视了空间音频中编码的**声源方向**和**距离**信息。MOSPA的关键突破是将输入特征替换为**双耳空间音频特征**（Sec 4.1），具体包括：

- **MFCC**（Mel频率倒谱系数）：捕捉音频的语义和音色特征
- **Tempogram**：建模音频的时间节奏特性
- **RMS能量**：表征空间音频的强度和空间分布

三者拼接形成2272维特征向量，使模型能够区分来自不同方位的相同声音并生成方向性响应运动。消融实验（Table 4）证实，单独移除MFCC或Tempogram均导致性能下降，组合使用取得最佳效果。

### 条件信号的语义增强：声源位置与运动风格

MOSPA将条件信号从“仅音频特征”扩展为三元组：**音频特征 + 声源位置（SSL）+ 运动风格（genre）**（Sec 4.2）。其中：

- **声源位置**显式编码了声音的空间来源，使模型能够生成朝向/远离声源的运动（如转头、走近）
- **运动风格**作为高层语义约束，引导模型生成符合特定反应类型（如“惊讶转身”、“跟随节奏”）的运动

消融实验（Table 3）提供了决定性证据：移除运动风格条件后，FID从**7.981**急剧上升至**10.930**，R-precision Top1从**0.937**降至**0.888**，表明风格条件对生成质量和音频-运动对齐度至关重要。

### 随机掩码与残差特征融合机制

不同于基线方法的简单拼接或交叉注意力，MOSPA采用**随机掩码与残差特征融合**（Sec 4.2, Fig. 5）。训练时对音频特征和SSL施加随机掩码，迫使模型学习鲁棒的条件依赖关系，避免过拟合到特定特征维度。所有条件信号与时间步编码拼接为统一token序列后，送入encoder-only Transformer进行去噪预测。

### 运动表示的空间感知增强

运动表示从传统关节旋转扩展为**全局位置 + 局部6D旋转 + 速度**的300维向量（Sec 4.1），使模型能够显式建模人体在空间中的位移和朝向变化，这对于“走向声源”或“远离声源”等空间响应运动至关重要。

MOSPA 是一个基于扩散模型的概率生成框架，将空间音频驱动的运动生成建模为条件分布学习问题。其核心思路是：将双耳空间音频分解为语义、时空和能量三类特征，并与声源位置、运动风格共同作为条件信号，引导一个编码器-仅Transformer从噪声中逐步重建干净的运动序列。

### 整体流程

框架的输入-输出流可概括为三条并行的编码路径汇聚于扩散去噪器：

1. **空间音频特征提取**：输入为双耳空间音频，经特征提取器输出 2272 维特征向量 $\mathbf{a}$，包含 MFCC（Mel频率倒谱系数）、Tempogram（节奏图）和 RMS 能量三个分量。
2. **条件信号构建**：将音频特征 $\mathbf{a}$ 与声源位置 $\mathbf{s}$、运动风格 $g$ 拼接，形成完整的条件表示。
3. **运动表示与扩散过程**：原始运动 $\mathbf{x}_0$ 被表示为 300 维向量（全局位置 + 6D局部旋转 + 速度）。前向扩散过程按马尔可夫链逐步添加高斯噪声：

$$q(\mathbf{x}_t|\mathbf{x}_{t-1}) = \mathcal{N}(\sqrt{\alpha_t}\mathbf{x}_{t-1}, (1-\alpha_t)I)$$

4. **去噪与重建**：编码器-仅Transformer作为去噪器 $\mathcal{G}$，从噪声运动 $\mathbf{x}_t$ 预测干净运动：

$$\hat{\mathbf{x}}_0 = \mathcal{G}(\mathbf{x}_t, t; \mathbf{a}, \mathbf{s}, g)$$

### 模块关系

| 模块 | 功能 | 关键设计 |
|------|------|----------|
| Spatial Audio Feature Extractor | 提取双耳 MFCC、Tempogram、RMS 特征 | 2272 维联合表示，捕获空间、时序和能量信息 |
| Motion Representation Module | 将运动数据编码为 300 维向量 | 全局位置 + 6D旋转 + 速度，避免欧拉角歧义 |
| Conditioning Fusion | 将条件信号融合为 token 序列 | 对音频特征和 SSL 施加随机掩码后进行残差特征融合 |
| Diffusion Denoiser | 从噪声运动预测干净运动 | 编码器-仅Transformer，以时间步 $t$ 和条件信号为引导 |

### 训练目标

总损失函数为五个分量的加权和：

$$\mathcal{L} = \lambda_{data}\mathcal{L}_{data} + \lambda_{geo}\mathcal{L}_{geo} + \lambda_{foot}\mathcal{L}_{foot} + \lambda_{traj}\mathcal{L}_{rot}$$

其中 $\mathcal{L}_{data}$ 在干净样本及其变化率上施加 MSE，$\mathcal{L}_{geo}$ 在前向运动学（FK）输出的位置和速度上施加约束，$\mathcal{L}_{foot}$、$\mathcal{L}_{traj}$、$\mathcal{L}_{rot}$ 分别惩罚脚步滑动、轨迹偏差和旋转误差。训练至第 5000 个 epoch 时，$\lambda_{traj}$ 和 $\lambda_{rot}$ 的权重从初始值提升至 3，以强化对轨迹和旋转的监督。

### 与基线方法的关键差异

现有音乐/语音驱动方法（如 **EDGE** (Tseng et al., CVPR 2023)、**POPDG** (Luo et al., CVPR 2024)、**LODGE** (Li et al., CVPR 2024)、**Bailando** (Siyao et al., CVPR 2022)）使用单声道音频特征，缺少空间信息编码。MOSPA 在三个关键槽位上做了替换：音频特征从单声道 Mel 频谱改为双耳空间特征（MFCC + Tempogram + RMS）；条件信号增加了声源位置和运动风格；融合机制引入了随机掩码与残差特征融合，而非简单的拼接或交叉注意力。这些改动使模型能够响应声源的空间位置变化，生成方向性和风格可控的运动。

MOSPA 是一个基于扩散的概率生成框架，其核心思想是将空间音频分解为语义、时空和能量三类特征，并与声源位置、运动风格共同作为条件信号，引导扩散模型从噪声中重建与空间音频高度对齐的人体运动序列。

### 关键模块

**空间音频特征提取器**从双耳音频中提取三类特征，拼接为 2272 维向量：
- **MFCC**（Mel-Frequency Cepstral Coefficients）建模音频的语义与音色特征；
- **Tempogram** 捕捉节奏和时域变化模式；
- **RMS 能量** 编码声音强度及空间能量分布信息。

**运动表示模块**将人体运动序列编码为 300 维向量，包含全局位置、局部旋转（采用 6D 连续旋转表示）和速度信息。

**扩散去噪器**采用 Encoder-Only Transformer 架构，以噪声运动 $\mathbf{x}_t$ 为输入，在时间步 $t$、音频特征 $\mathbf{a}$、声源位置 $\mathbf{s}$ 和运动风格 $g$ 的条件下预测干净运动 $\hat{\mathbf{x}}_0$。

**条件融合机制**将音频特征、声源位置、运动风格和时间步编码拼接为 token 序列，并在训练时对音频特征和声源位置施加随机掩码，通过残差特征融合增强模型的鲁棒性和条件利用率。

### 核心公式推导

**扩散前向过程**定义为一个马尔可夫链，逐步向干净运动 $\mathbf{x}_0$ 添加高斯噪声：

$$q(\mathbf{x}_t|\mathbf{x}_{t-1}) = \mathcal{N}(\sqrt{\alpha_t}\mathbf{x}_{t-1}, (1-\alpha_t)I)$$

其中 $\alpha_t$ 为噪声调度参数，控制每一步添加的噪声量。

**干净样本预测**由去噪器 $\mathcal{G}$ 完成：

$$\hat{\mathbf{x}}_0 = \mathcal{G}(\mathbf{x}_t, t; \mathbf{a}, \mathbf{s}, g)$$

该公式是 MOSPA 的核心——去噪器从带噪运动 $\mathbf{x}_t$ 出发，在时间步 $t$、空间音频特征 $\mathbf{a}$、声源位置 $\mathbf{s}$ 和运动风格 $g$ 的联合条件下，直接预测原始干净运动 $\hat{\mathbf{x}}_0$。这是实现空间音频-运动对齐的关键机制。

**总损失函数**由五个加权分量组成：

$$\mathcal{L} = \lambda_{data}\mathcal{L}_{data} + \lambda_{geo}\mathcal{L}_{geo} + \lambda_{foot}\mathcal{L}_{foot} + \lambda_{traj}\mathcal{L}_{traj} + \lambda_{rot}\mathcal{L}_{rot}$$

各分量含义：
- $\mathcal{L}_{data}$：干净运动及其变化率的 MSE 损失；
- $\mathcal{L}_{geo}$：前向运动学（FK）输出位置及其速度的 MSE 损失；
- $\mathcal{L}_{foot}$：脚步滑动惩罚损失；
- $\mathcal{L}_{traj}$：轨迹一致性损失；
- $\mathcal{L}_{rot}$：旋转平滑性损失。

训练策略上，$\lambda_{traj}$ 和 $\lambda_{rot}$ 在第 5000 个 epoch 时从初始值提升至 3（总训练 epoch 为 6000），以在训练后期强化轨迹和旋转的约束。

**多样性评估指标** APD（Average Pairwise Distance）定义为生成运动集合 $M$ 中所有样本对的平均距离：

$$APD(M) = \frac{1}{N(N-1)}\sum_{i=1}^{N}\sum_{j=1}^{N}\left(\sum_{t=1}^{L}\|\mathbf{s}_t^i - \mathbf{s}_t^j\|^2\right)^{1/2}$$

其中 $N$ 为样本数，$L$ 为序列长度，$\mathbf{s}_t^i$ 为第 $i$ 个样本在时刻 $t$ 的运动特征。该指标用于衡量生成运动的多样性，值越接近真实运动分布越好。

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_X2r9D46kvI/figures/006_Figure_5.jpg]]
*Figure 5: The framework of MOSPA. We perform diffusion-based motion generation given spatial audio inputs. Specifically, Gaussian noise is added to the clean motion sample*

## 实验与关键发现

### 主实验结果

MOSPA 在 SAM 数据集上与四个主流基线进行了系统对比：**EDGE**（Tseng et al., CVPR 2023）、**POPDG**（Luo et al., CVPR 2024）、**LODGE**（Li et al., CVPR 2024）和 **Bailando**（Siyao et al., CVPR 2022）。这些方法原本为音乐或语音驱动设计，本文将其音频输入替换为空间音频以适配任务。需要注意的是，这种适配可能未充分利用空间信息，比较存在一定局限性。

**Table 2** 报告了核心定量结果。MOSPA 在运动质量与音频对齐度上全面领先：

- **FID** 降至 **7.981**，相比最强基线 EDGE 的 13.993 降低了 6.012（降幅约 43%），表明生成运动与真实运动的分布高度接近。
- **R-precision** Top1 达到 **0.937**（EDGE 为 0.886），Top2 为 0.984，Top3 为 0.996，说明模型能精确地将生成运动与对应音频匹配。
- **Diversity** 为 **23.575**，与真实运动的 23.616 仅差 0.041，证明生成结果保持了接近真实的多样性。
- **APD**（平均成对距离）为 53.915，与真实运动的 59.435 接近，进一步验证多样性保持良好。

**Figure 6** 的定性对比展示了五个案例。MOSPA 生成的运动在语义和空间响应上均与输入空间音频高度一致，而基线方法常出现动作与音频不匹配或运动质量退化的问题。

### 消融实验

**Table 3** 系统验证了各设计选择的影响：

- **运动风格条件**：移除运动风格（genre）条件后，FID 从 7.981 恶化至 **10.930**，R-precision 全面下降。这是性能退化的最大单一因素，证明风格条件对生成质量至关重要。
- **潜在维度**：将潜在维度从 512 降至 256 导致 FID 升至 9.226，R-precision 同步下降，说明足够的表示容量是高质量生成的前提。
- **注意力头数与扩散步数**：减少注意力头数（8→4）或大幅压缩扩散步数（1000→100/4）均使性能小幅退化，但影响程度小于风格条件和潜在维度。
- **音频特征组合**（**Table 4**）：单独移除 MFCC 或 Tempogram 均导致性能下降，二者组合使用取得最佳效果，验证了语义-时空特征互补的必要性。

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_X2r9D46kvI/figures/014_Table_4.jpg]]
*Table 4: Ablation study on the effect of MFCC [17] and tempogram [28] features*

### 失败模式与局限性

尽管 MOSPA 在主任务上表现优异，仍存在以下已知局限：

1. **手指细节缺失**：模型仅关注身体运动，未包含手指动作（见 Sec 4.1），限制了其在需要精细手势的场景中的应用。
2. **物理合理性不足**：生成的运动未考虑物理约束和场景交互，可能不适用于需要物理模拟的下游任务（如机器人控制）。
3. **分布外泛化有限**：在未见过的音频场景下，生成质量可能下降，需要额外微调或扩展数据集。**Figure 8** 展示了分布外鲁棒性测试的部分结果，但覆盖范围有限。
4. **反应类型覆盖不足**：SAM 数据集涵盖约 20 种反应类型，无法覆盖所有真实世界空间音频响应场景。

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_X2r9D46kvI/figures/012_Figure_8.jpg]]
*Figure 8: Test of MOSPA on out-of-distribution spatial audios. Descriptions of motions are provided for reference*

### 用户调研

**Figure 7** 的用户调研从意图对齐、运动质量和与真值相似度三个维度评估。MOSPA 在所有维度上均获得最高票数，进一步验证了定量指标的优势。

### 关键图表结论总结

| 图表 | 核心结论 |
|------|----------|
| **Table 2** | MOSPA 在 FID、R-precision 等指标上全面超越基线，且多样性接近真实运动 |
| **Table 3** | 运动风格条件是最大贡献因素；潜在维度和特征组合对性能有显著影响 |
| **Table 4** | MFCC 与 Tempogram 互补，联合使用效果最优 |
| **Figure 6** | 定性结果验证 MOSPA 在空间响应和语义一致性上的优势 |
| **Figure 7** | 用户调研确认 MOSPA 在主观评估中同样领先 |

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_X2r9D46kvI/figures/008_Table_2.jpg]]
*Table 2: Quantitative evaluation on the SAM, where MOSPA achieves higher alignment with the GT motion while maintaining high diversity, as reflected by the metrics. The error bar is the 95% confidence interval assuming normal distribution, and → means the closer to Real Motion the better*

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_X2r9D46kvI/figures/009_Table_3.jpg]]
*Table 3: Ablation study on MOSPA on the spatial audio-driven motion generation performance. The error bar is the 95% confidence interval assuming normal distribution, and → means the closer to real motions the better*

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_X2r9D46kvI/figures/007_Figure_6.jpg]]
*Figure 6: Qualitative comparison of state-of-the-art methods for the spatial audio-to-motion task. We visualize motion results from five cases. MOSPA produces high-quality movements that closely correspond to the input spatial audio. We provide Expected Motion as a description for reference*

## 定位与知识库关联

### 任务定位与基线关系

MOSPA 提出“空间音频驱动的人体运动生成”这一新任务，并构建了首个专用数据集 SAM。在实验对比中，作者将四类现有方法适配为基线：**EDGE**（Tseng et al., CVPR 2023）、**POPDG**（Luo et al., CVPR 2024）、**LODGE**（Li et al., CVPR 2024）和 **Bailando**（Siyao et al., CVPR 2022）。这些方法原本分别面向音乐到舞蹈生成、流行舞蹈生成、长时序舞蹈生成和音乐驱动舞蹈生成，均通过替换音频输入的方式适配到空间音频任务。公平性方面需注意：这些基线在设计时未考虑空间音频特征，因此其性能差距部分源于架构对空间信息利用不足，而非纯粹的任务能力差异。

从方法谱系看，MOSPA 属于条件扩散生成模型在人体运动合成领域的延伸。其核心改造体现在四个关键槽位：

- **音频特征**：从单声道 Mel 频谱转向双耳空间音频特征（MFCC + Tempogram + RMS 能量），形成 2272 维表征。
- **条件信号**：在音频特征之上叠加声源位置（SSL）和运动风格（genre）作为联合条件。
- **运动表示**：采用全局位置 + 局部 6D 旋转 + 速度的 300 维表示，取代仅用关节旋转或位置的方案。
- **融合机制**：引入随机掩码与残差特征融合，替代简单拼接或交叉注意力。

消融实验（Table 3, Table 4）表明，移除运动风格条件后 FID 从 7.981 升至 10.930，移除 MFCC 或 Tempogram 均导致性能退化，验证了各模块的独立贡献。

### 适用边界与局限

MOSPA 的适用边界受以下因素制约：

1. **运动粒度有限**：模型仅关注身体运动，未包含手指细节动作（Sec 4.1），因此不适用于需要精细手部交互的场景。
2. **物理合理性未约束**：生成的运动未考虑物理约束和场景交互，直接用于物理模拟下游任务时可能产生不合理的运动轨迹。
3. **分布外泛化受限**：在未见过的空间音频场景下生成质量可能下降，需要额外微调或数据集扩展。
4. **反应类型覆盖有限**：SAM 数据集覆盖约 20 种反应类型（不含运动风格），无法涵盖真实世界中所有的空间音频响应模式。

### 开放问题

论文指出的开放方向包括：

- **物理基控制集成**：如何将物理模拟控制方法（如文中引用的 ）与扩散生成结合，提升运动的物理正确性。
- **全身运动扩展**：如何将生成范围扩展到包含手部手势和面部表情的全身运动。
- **场景感知引入**：如何引入虚拟环境的场景信息，使生成的运动与场景约束保持一致。

这些方向指向从“音频-运动对齐”向“音频-运动-环境协同”的演进路径，需在数据集构建和模型架构两个层面进行突破。

## 原文 PDF

![[paperPDFs/NEURIPS_2025/MOSPA_Human_Motion_Generation_Driven_by_Spatial_Audio.pdf]]
