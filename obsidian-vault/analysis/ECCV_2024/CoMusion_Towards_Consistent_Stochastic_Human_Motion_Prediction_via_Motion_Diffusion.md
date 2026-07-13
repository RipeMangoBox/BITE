---
title: "CoMusion: Towards Consistent Stochastic Human Motion Prediction via Motion Diffusion"
type: paper
paper_level: A
venue: ECCV
year: 2024
pdf_ref: paperPDFs/ECCV_2024/CoMusion_Towards_Consistent_Stochastic_Human_Motion_Prediction_via_Motion_Diffusion.pdf
project_link: null
code_link: https://github.com/jsun57/CoMusion/
aliases:
- CoMusion
tags:
- ECCV_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 在扩散模型的反向过程中，首先使用Transformer模块从噪声中重建出平滑的未来运动初始值（y~0），然后将其与历史运动拼接，通过GCN在DCT空间中优化整个运动序列；同时采用直接预测未来运动（而非噪声）的策略，并结合修改的余弦方差调度器（使初始ᾱ0=0.5），以保持学习任务的难度，防止过拟合。
primary_logic: 通过平滑的初始重建将随机运动预测任务转化为类似确定性预测的简化问题，从而能够利用GCN-DCT设计显式建模时空关节关系，生成与历史运动一致且真实的多模态未来序列。
claims:
- 移除Transformer重建模块F(·)后，CMD从3.202急剧升至197.105（无F和R时）或259.037（有R无F），表明平滑初始化对一致性至关重要。
- 直接预测未来运动y0（而非噪声）显著优于噪声预测，ADE从0.502降至0.350，FID从0.167降至0.102。
- 提出的修改余弦调度器在所有指标上均优于标准余弦和平方根调度器，使ADE从0.382降至0.350，CMD从3.323降至3.202。
- Human3.6M 上 ADE = 0.350
---

# CoMusion: Towards Consistent Stochastic Human Motion Prediction via Motion Diffusion

> [!tip] 核心洞察
> 通过平滑的初始重建将随机运动预测任务转化为类似确定性预测的简化问题，从而能够利用GCN-DCT设计显式建模时空关节关系，生成与历史运动一致且真实的多模态未来序列。

| 字段 | 内容 |
|------|------|
| 中文题名 | CoMusion：通过运动扩散实现一致性的随机人体运动预测 |
| 英文题名 | CoMusion: Towards Consistent Stochastic Human Motion Prediction via Motion Diffusion |
| 会议/期刊 | ECCV 2024 |
| Links | [Code](https://github.com/jsun57/CoMusion/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | CoMusion |
| Dataset | Human3.6M, AMASS |

> [!tip] 效果简介
> - Human3.6M 上，ADE 0.350 vs 0.372 (BeLFusion) (-0.022)；FDE 0.458 vs 0.474 (BeLFusion) (-0.016)；CMD 3.202 vs 5.988 (BeLFusion) (-2.786 (↓46.5%))。
> - AMASS 上，CMD 9.636 vs 16.995 (BeLFusion) (-7.359 (↓43.3%))。

## 概要

人体运动预测（Human Motion Prediction, HMP）的目标是根据观察到的历史姿态序列，生成未来一段时间的合理人体运动。确定性方法只能输出单一未来，而**随机运动预测**则需捕捉未来运动的固有不确定性，生成多模态、真实且与历史一致的样本。现有随机方法（尤其是基于扩散模型的方法）面临一个核心瓶颈：它们通常预测扩散过程中的噪声而非直接预测运动，导致输入与真值差异过大，难以利用在确定性预测中非常成功的**图卷积网络-离散余弦变换（GCN-DCT）**设计；同时，缺乏平滑的未来姿态初始化，使得预测与历史运动不一致，且常需复杂的多阶段训练。

**CoMusion** 针对上述瓶颈提出了一个单阶段、端到端的条件扩散框架。其核心洞察在于：通过从噪声中**先重建出一个平滑的未来运动初始值**，将随机运动预测任务转化为一个近似确定性预测的简化问题，从而能够显式利用 GCN-DCT 在时空关节关系建模上的优势，生成与历史一致且真实的多模态未来序列。具体而言，CoMusion 做出了三项关键设计：

1. **直接预测未来运动**（而非噪声），使预测目标与最终输出对齐。
2. **Transformer 重建模块 + GCN 优化模块**：先用 Transformer 从当前噪声运动中重建平滑的 $\tilde{y}_0$，再将其与历史运动拼接，通过 GCN 在 DCT 空间中优化整个序列。
3. **修改的余弦方差调度器**：设定初始 $\bar{\alpha}_0 = 0.5$，使运动预测任务在整个去噪过程中保持非平凡，防止模型过拟合到历史运动。

在 Human3.6M 和 AMASS 两个基准数据集上，CoMusion 在准确性和一致性指标上全面超越现有方法。在 Human3.6M 上，与之前最优的 **BeLFusion**（Barquero et al., CVPR 2023）相比，**CMD（运动分布一致性）下降 46.5%**（3.202 vs. 5.988），**FID 下降 51.2%**（0.102 vs. 0.209），同时 ADE 和 FDE 也取得最优。在 AMASS 上，CMD 相对 BeLFusion 降低 43.3%。消融实验证实，移除 Transformer 重建模块会导致 CMD 急剧恶化至 197–259，验证了平滑初始化对一致性的决定性作用；直接预测运动策略使 ADE 从 0.502 降至 0.350；修改的余弦调度器在所有指标上均优于标准调度器。

CoMusion 的方法设计使其在**方法谱系**中处于一个独特位置：它既继承了扩散模型的多模态生成能力，又融合了确定性预测中 GCN-DCT 架构的时空建模优势，并通过预测目标与调度器的协同设计，在单阶段框架内实现了准确性与多样性的平衡。该方法为条件扩散模型在结构化时序预测任务中的应用提供了新的范式参考。



### 人体运动预测：从确定性到随机建模

人体运动预测（Human Motion Prediction, HMP）旨在基于观察到的历史姿态序列，预测未来一段时间内的人体运动轨迹。早期工作主要聚焦于**确定性预测**，即对每个历史输入仅生成唯一的未来序列。这类方法通常采用图卷积网络（GCN）在离散余弦变换（DCT）空间中建模时空关节依赖关系，在预测精度上取得了显著进展。

然而，人体运动本质上是**多模态的**——给定相同的历史动作，未来存在多种合理的发展可能（例如“走过去”还是“停下来”）。确定性方法无法捕捉这种内在的不确定性，因此近年来研究者将目光转向**随机人体运动预测**（Stochastic HMP），期望模型能从条件分布中采样出多样化且逼真的未来运动序列。

### 扩散模型在随机预测中的困境

扩散模型（Diffusion Models）因其强大的生成能力，已成为随机HMP的主流范式。现有方法（如**MotionDiff**, Wei et al., ECCV 2022；**BeLFusion**, Barquero et al., CVPR 2023；**HumanMAC**, Chen et al., ICCV 2023）通常将运动预测建模为**条件去噪过程**：以历史运动为条件，从纯噪声中逐步恢复未来运动。

但这些方法存在一个被忽视的关键瓶颈：**它们普遍采用“预测噪声ε”而非“直接预测运动”的策略**。这带来了两个连锁问题：

1. **DCT空间优势的丧失**：在确定性预测中被验证极为有效的GCN-DCT设计，难以直接迁移到噪声预测框架中。原因在于，扩散过程的中间状态 $y_t$ 是真实运动 $y_0$ 与高斯噪声的混合，其DCT系数与干净运动差异巨大，无法受益于DCT空间的平滑性和稀疏性。如Figure 1所示，噪声填充序列的DCT系数与真值序列相去甚远，而零填充序列则相对接近——这暗示着，若能在去噪早期获得一个“接近真值”的初始估计，DCT空间的优势就能被重新激活。

2. **历史一致性的缺失**：噪声预测模型缺乏对“未来运动应与历史运动平滑衔接”的显式约束。从纯噪声出发的迭代去噪，在早期步骤中生成的中间结果可能与历史姿态存在严重的空间跳跃，导致最终预测与观察序列之间出现不自然的过渡。

此外，现有方法往往需要复杂的多阶段训练策略（如VAE先验学习加扩散先验学习），增加了训练难度和不稳定性。

### CoMusion的核心动机

基于上述分析，本文提出**CoMusion**，其核心动机可以概括为三个层面的改进：

- **化随机为确定**：在扩散反向过程的初始阶段，使用一个专用的Transformer重建模块 $F(\cdot)$，从当前噪声运动 $y_t$ 中直接重建出一个平滑的未来运动初始估计 $\tilde{y}_0$。如Figure 5所示，该模块能将高斯噪声轨迹转化为具有合理时间模式的平滑轨迹，从而将后续的优化问题转化为“基于良好初始值的确定性精修”。

- **重拾GCN-DCT设计**：获得平滑的 $\tilde{y}_0$ 后，将其与历史运动 $x$ 拼接，输入基于GCN的精修模块 $R(\cdot)$，在DCT系数空间中显式建模时空关节关系。这使得CoMusion能够继承确定性方法中GCN-DCT架构的全部优势。

- **直接预测运动与调度器适配**：采用**直接预测未来运动 $y_0$** 的策略替代噪声预测，并配套提出**修改的余弦方差调度器**，将初始累积信噪比 $\bar{\alpha}_0$ 设为0.5（而非标准余弦调度器的接近1）。这一设计使 $y_0$ 预测任务在整个去噪过程中保持非平凡难度，防止模型过早过拟合到历史运动，从而在准确性与多样性之间取得平衡。

通过上述设计，CoMusion以单阶段、端到端的方式，在保持扩散模型多模态生成能力的同时，实现了与确定性方法相媲美的预测一致性，显著缩小了随机预测与确定性预测之间的性能鸿沟。



## 核心方法与创新机理

CoMusion 的核心创新在于将随机人体运动预测（stochastic HMP）重新表述为一个**先平滑重建、后时空优化**的两阶段问题，从而突破了现有扩散模型方法无法利用确定性预测中成功的 GCN‑DCT 设计的瓶颈。这一思路由三个相互耦合的 **changed slots** 共同实现。

### 1. 预测目标：从预测噪声转向直接预测未来运动

现有条件扩散模型（如 **BeLFusion** (Barquero et al., CVPR 2023)、**HumanMAC** (Chen et al., ICCV 2023)）普遍遵循标准去噪扩散范式，即网络学习预测注入的噪声 $\epsilon$。然而，在 HMP 任务中，历史运动 $x$ 与未来运动 $y_0$ 之间存在显著的输入‑真值差异，噪声预测策略使模型难以受益于 DCT 空间的平滑性（见 Fig. 1 的动机示意）。

CoMusion 转而采用**直接预测未来运动** $y_0$ 的策略：
$$ \hat{y}_0 \leftarrow G_\theta(y_t, x, t) $$
其中 $y_t = \sqrt{\bar{\alpha}_t} y_0 + \sqrt{1 - \bar{\alpha}_t} \epsilon$ 为噪声化的目标序列。这一改变使生成器始终在“运动空间”而非“噪声空间”中操作，为后续引入 GCN‑DCT 时空建模铺平了道路。消融实验（Table 4a）证实：直接预测 $y_0$ 使 ADE 从 0.502 降至 0.350，FID 从 0.167 降至 0.102，效果显著。

### 2. 网络架构：Transformer 重建 + GCN 优化的双模块生成器

CoMusion 的生成器 $G_\theta(\cdot)$ 由两个功能互补的模块级联构成（Fig. 2）：

- **运动重建模块 $F(\cdot)$**：一个基于 Transformer 编码器的网络，仅从当前噪声运动 $y_t$ 和时间步 $t$ 重建出**平滑的未来运动初始值** $\tilde{y}_0$。该模块不依赖历史运动 $x$，其作用是将高度噪声化的 $y_t$ 映射为一个具有合理时间结构的粗糙预测，为后续精细化提供良好的初始化。Fig. 5 直观展示了 $F(\cdot)$ 将高斯噪声轨迹转化为平滑运动模式的能力。

- **运动优化模块 $R(\cdot)$**：一个基于 GCN 的网络，将运动历史 $x$ 与重建的 $\tilde{y}_0$ 拼接后，在 **DCT 系数空间**中对整个序列进行优化，输出最终预测 $\hat{y}_0$。GCN 显式建模人体骨架的时空关节关系，DCT 变换则将运动压缩到低频主导的紧凑表示，两者结合使 $R(\cdot)$ 能够高效地协调历史一致性与未来合理性。

这一架构的关键洞察在于：**$F(\cdot)$ 提供的平滑初始值将随机预测问题转化为一个近似确定性预测的简化问题**，从而使 $R(\cdot)$ 能够复用 DCT‑GCN 设计，生成与历史一致且真实的多模态未来。消融实验（Table A.2）提供了决定性证据：移除 $F(\cdot)$ 后，即使保留 $R(\cdot)$，CMD 也从 3.202 急剧恶化至 259.037，表明平滑初始化对一致性至关重要。

### 3. 方差调度器：修改的余弦调度器

标准扩散调度器（线性或余弦）的初始信噪比极高（$\bar{\alpha}_0 \approx 1$），此时 $y_t \approx y_0$，模型容易简单地复制历史运动来“预测”未来，导致过拟合和多样性丧失。CoMusion 提出一种**修改的余弦调度器**，通过引入偏移量使初始 $\bar{\alpha}_0 = 0.5$：
$$ \bar{\alpha}_t = \cos\left( \frac{t/T + 1}{2} \cdot \frac{\pi}{2} \right)^2 $$
这一设计确保在去噪过程的**所有阶段**（包括 $t=0$），预测任务都保持非平凡难度，迫使模型真正学习从噪声中重建未来运动，而非依赖历史捷径。Table 4b 和 Table 5 的消融表明：该调度器在所有指标上均优于标准余弦和平方根调度器，使 ADE 从 0.382 进一步降至 0.350，CMD 从 3.323 降至 3.202；而标准线性调度器甚至导致训练发散。

### 创新间的因果耦合关系

上述三个 changed slots 并非独立改进，而是存在深层因果依赖：
1. **直接预测 $y_0$** 是引入 $F(\cdot)$ 和 $R(\cdot)$ 的前提——只有在运动空间中操作，$F(\cdot)$ 才能重建有意义的平滑轨迹，$R(\cdot)$ 才能在 DCT 空间中优化关节关系。
2. **$F(\cdot)$ 的平滑初始化**是 $R(\cdot)$ 发挥 GCN‑DCT 优势的必要条件——若输入高度噪声化的 $y_t$ 直接进入 $R(\cdot)$，输入‑真值差异巨大，DCT 空间的平滑性无法被有效利用。
3. **修改的余弦调度器**通过降低初始 $\bar{\alpha}_0$，防止模型在 $F(\cdot)$ 已经提供良好初始值的条件下仍然过拟合历史运动，从而保障了多样性与准确性的平衡。

三者协同作用，使 CoMusion 在 Human3.6M 数据集上相较此前最优方法 **BeLFusion** 实现了 CMD 下降 46.5%、FID 下降 51.2% 的一致性飞跃（Table 1），同时在 AMASS 数据集上 CMD 下降 43.3%（Table 2），验证了该创新组合的跨数据集泛化能力。



CoMusion 是一个**单阶段、端到端的条件扩散模型**，用于随机人体运动预测（stochastic HMP）。其核心思路是将扩散模型的去噪过程重新组织为“平滑初始化 + 时空精炼”的两阶段生成管线，从而在保持多模态生成能力的同时，大幅提升预测与历史运动的一致性。

### 输入输出定义

给定一段观测到的运动历史 $x \in \mathbb{R}^{H \times J \times D}$（$H$ 帧历史，$J$ 个关节，$D$ 维关节表示），模型需要生成 $K$ 条可能的未来运动序列 $\hat{y} \in \mathbb{R}^{F \times J \times D}$（$F$ 帧未来）。整个过程以 $x$ 为条件，从纯高斯噪声出发，通过 $T$ 步迭代去噪逐步生成未来运动。

### 生成器 $G_\theta$ 的两阶段架构

CoMusion 的核心组件是条件运动生成器 $G_\theta(y_t, x, t)$，它在每个去噪时间步 $t$ 接收三个输入——当前噪声运动 $y_t$、运动历史 $x$ 和时间步 $t$——并输出对未来干净运动 $y_0$ 的直接预测 $\hat{y}_0$。生成器由两个功能互补的模块串联构成（见 Fig. 2）：

![[assets/figures/papers/paper_list_l1872_CoMusion_Towards_Consistent_Stochastic_Human_Motion_Prediction_via_Motio/figures/002_Figure_2.jpg]]
*Figure 2: Architecture of CoMusion’s predictor*

**阶段一：运动重建模块 $F(\cdot)$（Motion Reconstruction Module）**

$F(\cdot)$ 是一个基于 Transformer 编码器的网络，其任务是**仅从当前噪声运动 $y_t$ 和时间步 $t$ 中重建出一个平滑的未来运动初始估计 $\tilde{y}_0$**，不依赖运动历史 $x$。该模块通过 Transformer 的自注意力机制捕捉未来帧之间的时间相关性，将高噪声、高方差的 $y_t$ 转化为具有合理时间结构的粗糙预测。如 Fig. 5 所示，纯高斯噪声轨迹 $y_T$ 经 $F(y_T, T)$ 重建后呈现出显著更平滑的时间模式，方差大幅降低。这一平滑初始化是整个框架的**关键因果节点**——消融实验（Table A.2）表明，移除 $F(\cdot)$ 后一致性指标 CMD 从 3.202 急剧恶化至 197.105（仅保留 $R$ 无调度器）或 259.037（保留 $R$ 和调度器），说明没有平滑初始化，后续精炼模块几乎无法恢复与历史一致的运动。

**阶段二：运动精炼模块 $R(\cdot)$（Motion Refinement Module）**

$R(\cdot)$ 是一个基于图卷积网络（GCN）的精炼网络，它在**离散余弦变换（DCT）系数空间**中运行。具体流程为：
1. 将运动历史 $x$ 与重建的 $\tilde{y}_0$ 在时间维度上拼接，形成完整的“历史-未来”运动序列；
2. 通过 DCT 将拼接序列变换到频域；
3. 利用 GCN 在 DCT 空间中显式建模人体骨架的**时空关节关系**——空间边捕捉同一帧内关节间的运动学依赖，时间边捕捉同一关节跨帧的时序演化；
4. 经逆 DCT（IDCT）还原为时域运动，输出最终预测的未来运动 $\hat{y}_0$。

这一设计使得原本困难的“从噪声直接生成与历史一致的未来运动”问题，被转化为一个类似于确定性预测的简化问题：在已有平滑初始估计 $\tilde{y}_0$ 的前提下，$R(\cdot)$ 只需在 DCT 空间中联合优化历史与未来，利用 GCN 的归纳偏置即可高效完成时空一致性精炼。消融实验（Table 3）证实，完整的 $F(\cdot) + R(\cdot)$ 组合在所有指标上均显著优于仅使用其中任一模块的变体。

### 预测目标与方差调度器的协同设计

CoMusion 在扩散范式中做了两个关键的策略选择，二者相互配合共同保障了框架的有效性：

**直接预测运动 $y_0$ 而非噪声 $\epsilon$。** 传统扩散模型通常训练网络预测添加的噪声，但 CoMusion 选择直接预测未来运动本身。这一选择与两阶段架构深度耦合：$F(\cdot)$ 需要从 $y_t$ 中重建出有意义的 $\tilde{y}_0$，而非仅仅估计一个噪声向量。Table 4(a) 的消融实验证实，直接预测 $y_0$ 在所有指标上显著优于噪声预测（ADE 从 0.502 降至 0.350，FID 从 0.167 降至 0.102）。

**修改的余弦方差调度器。** 标准扩散调度器（线性或余弦）在 $t=0$ 时 $\bar{\alpha}_0 \approx 1$，意味着初始阶段 $y_t$ 几乎等于干净数据，模型可以轻易地“抄近道”直接从 $y_t$ 复制出 $y_0$，从而**过拟合到运动历史**（因为 $y_t$ 与 $x$ 在训练早期几乎无噪声差异），损害生成多样性。CoMusion 提出修改的余弦调度器，通过将相位偏移 1 使得 $\bar{\alpha}_0 = \cos(\pi/4)^2 = 0.5$：

$$\bar{\alpha}_t = \cos\left(\frac{t/T + 1}{2} \cdot \frac{\pi}{2}\right)^2$$

这使得即使在 $t=0$ 时，$y_t$ 仍包含显著噪声（信噪比 1:1），迫使模型在整个去噪过程中都必须真正学习从噪声中重建运动，从而防止对历史运动的过拟合。Table 4(b) 和 Table 5 表明，该调度器在准确性和多样性上均优于标准余弦和平方根调度器，且标准线性调度器直接导致训练发散。

### 训练策略：结构感知损失与多样性松弛

训练时，模型对每个运动历史 $x$ 生成 $k$ 条未来轨迹，并采用**多样性松弛**策略——仅优化损失最小的那条轨迹：

$$\mathcal{L}_{\mathrm{final}} = \min_k \mathcal{L}_{\theta}(G^k, y_0, x)$$

这鼓励模型在不同的随机噪声下产生多样化的输出，避免后验崩溃（即所有样本坍缩到同一模式）。损失函数 $\mathcal{L}_{\mathrm{rec}}$ 为结构感知的加权 L1 损失，同时监督历史运动重建和未来运动预测，关节权重 $\lambda^j$ 基于人体运动学链的层级结构设定，使末端关节（如手腕、脚踝）获得更高权重。Table 6(a) 显示，移除历史重建（$\gamma=0$）或使用均匀关节权重（$\lambda^j=1$）均会导致性能下降；Table 6(b) 表明 $k=2$ 在多样性、准确性和保真度之间实现了最佳平衡。

### 推理流程

推理时，从纯高斯噪声 $y_T \sim \mathcal{N}(0, \mathrm{I})$ 出发，通过 $T=10$ 步 DDPM 采样迭代调用 $G_\theta$，每一步执行“$F(\cdot)$ 重建 $\to$ $R(\cdot)$ 精炼”的两阶段计算，最终输出 $\hat{y}_0$ 作为预测的未来运动。10 步扩散的设计在推理效率上具有优势（Table A.1），同时保持了生成质量。



### 3.1 条件运动扩散建模

CoMusion 将随机人体运动预测建模为条件扩散生成问题。给定历史运动序列 $x$，目标是学习未来运动 $y_0$ 的条件分布 $p(y_0 | x)$。扩散模型通过前向加噪和反向去噪两个过程实现这一目标。

**前向扩散过程**定义为马尔可夫链，逐步向干净数据 $y_0$ 注入高斯噪声：

$$q(y_t | y_{t-1}) = \mathcal{N}(y_t; \sqrt{\alpha_t} y_{t-1}, (1-\alpha_t)\mathrm{I}) \tag{1}$$

其中 $\alpha_t \in (0,1)$ 为噪声调度参数。通过重参数化技巧，可直接从 $y_0$ 采样任意噪声级别的 $y_t$：

$$q(y_t | y_0) = \mathcal{N}(y_t; \sqrt{\bar{\alpha}_t} y_0, (1-\bar{\alpha}_t) \mathrm{I}) \tag{4}$$

$$y_t = \sqrt{\bar{\alpha}_t} y_0 + \sqrt{1-\bar{\alpha}_t} \epsilon \tag{6}$$

其中 $\bar{\alpha}_t = \prod_{i=1}^t \alpha_i$，$\epsilon \sim \mathcal{N}(0, \mathrm{I})$。

**条件反向扩散过程**以历史运动 $x$ 为条件，逐步从噪声 $y_T \sim \mathcal{N}(0, \mathrm{I})$ 去噪恢复 $y_0$：

$$p_\theta(y_{t-1} | y_t, x) = \mathcal{N}(y_{t-1}; \mu_\theta(y_t, x, t), \sigma_\theta^2(y_t, x, t) \mathrm{I}) \tag{3}$$

其中 $\mu_\theta$ 和 $\sigma_\theta$ 由生成器网络 $G_\theta$ 参数化。

### 3.2 核心设计一：直接运动预测策略

不同于主流扩散方法预测噪声 $\epsilon$，CoMusion 采用**直接预测未来运动**的策略（prediction target = $y_0$）。生成器直接输出对干净运动的重建：

$$\hat{y}_0 \gets G_\theta(y_t, x, t)$$

这一设计的关键动机在于：预测噪声时，输入 $y_t$ 与目标 $y_0$ 的差异随噪声级别增大而急剧扩大，导致网络难以受益于 DCT 空间的平滑性优势。直接预测 $y_0$ 将任务转化为运动重建问题，使得后续的 GCN-DCT 设计能够有效发挥作用。消融实验（Table 4a）证实：直接预测 $y_0$ 相比噪声预测使 ADE 从 0.502 降至 0.350，FID 从 0.167 降至 0.102。

### 3.3 核心设计二：修改的余弦方差调度器

标准余弦调度器的 $\bar{\alpha}_t$ 从 $\bar{\alpha}_0 \approx 1$ 开始衰减，意味着在扩散初期 $y_t \approx y_0$。当模型直接预测 $y_0$ 并以 $x$ 为条件时，这种设置使得网络可以通过简单复制历史运动来“偷懒”，导致过拟合和多样性不足。

CoMusion 提出**修改的余弦调度器**，通过引入偏移量 $s=1$ 使初始 $\bar{\alpha}_0 = 0.5$：

$$\bar{\alpha}_t = \cos\left(\frac{t/T + 1}{2} \cdot \frac{\pi}{2}\right)^2 \tag{7}$$

该设计确保即使在 $t=0$ 时，$y_0$ 也包含显著噪声（$\bar{\alpha}_0 = 0.5$ 意味着信号与噪声各占一半），迫使模型在整个去噪过程中真正学习从噪声中重建运动，而非记忆历史。消融实验（Table 4b）表明该调度器在所有指标上均优于标准余弦和平方根调度器，ADE 从 0.382 降至 0.350，CMD 从 3.323 降至 3.202。

### 3.4 核心设计三：两阶段生成器架构

CoMusion 的生成器 $G_\theta$ 由两个功能互补的模块组成（Figure 2）：

**（1）Transformer 运动重建模块 $F(\cdot)$**

该模块从当前噪声运动 $y_t$ 和时间步 $t$ 中重建出平滑的未来运动初始估计 $\tilde{y}_0$：

$$\tilde{y}_0 = F(y_t, t)$$

$F(\cdot)$ 采用 8 层 Transformer 编码器（隐维度 512），仅建模未来帧之间的时间相关性，不依赖历史运动 $x$。其作用是将高噪声的 $y_t$ 转化为具备合理时间平滑性的初始猜测，为后续精细化提供良好起点。Figure 5 的可视化表明，$F(y_T, T)$ 能将纯高斯噪声轨迹重建为具有低方差和平滑时间模式的运动。

![[assets/figures/papers/paper_list_l1872_CoMusion_Towards_Consistent_Stochastic_Human_Motion_Prediction_via_Motio/figures/008_Figure_5.jpg]]
*Figure 5: Left: yT , a Gaussian trajectory with*

**（2）GCN 运动精细化模块 $R(\cdot)$**

该模块将历史运动 $x$ 与重建的 $\tilde{y}_0$ 拼接，在 DCT 系数空间中通过图卷积网络显式建模时空关节关系，输出最终预测 $\hat{y}_0$：

$$\hat{y}_0 = R(x, \tilde{y}_0)$$

具体流程为：拼接后的序列经 DCT 变换进入频域，GCN 在 DCT 系数上操作以捕捉关节间的运动学依赖和时间模式，再经 IDCT 变换回时域。这一设计的关键在于：$\tilde{y}_0$ 已具备平滑性，使得拼接后的完整序列在 DCT 空间中呈现紧凑表示，GCN 能够高效地优化全局运动一致性。

消融实验（Table 3 / Table A.2）揭示了 $F(\cdot)$ 的不可替代性：移除 Transformer 重建模块后，CMD 从 3.202 急剧恶化至 259.037（有 $R$ 无 $F$）或 197.105（仅 $R$ 无调度器），表明平滑初始化是模型一致性的基石。

### 3.5 结构感知损失与多样性松弛

**结构感知重建损失**基于人体运动学链定义关节权重 $\lambda^j$，对历史重建和未来预测进行联合监督：

$$\mathcal{L}_{\mathrm{rec}} = \frac{1}{J} \sum_{j=1}^{J} \left( \gamma \cdot \| (x^{j} - \hat{x}^{j}) \cdot \lambda^{j} \|_1 + \| (y_0^{j} - \hat{y}_0^{j}) \cdot \lambda^{j} \|_1 \right) \tag{9}$$

其中 $\gamma$ 控制历史重建损失的权重，$\lambda^j$ 根据关节在运动学链中的层级位置赋予不同重要性（末端关节权重更高）。总体损失为训练数据分布下的期望：

$$\mathcal{L}_{\boldsymbol{\theta}}(G, y_0, x) = \mathbb{E}_{y_0 \sim \boldsymbol{q}(\cdot | x)} \mathcal{L}_{\mathrm{rec}}(G_{\boldsymbol{\theta}}(y_t, x, t), y_0, x) \tag{8}$$

**多样性松弛目标**为避免后验崩溃，对每个历史 $x$ 生成 $k$ 条轨迹，仅优化损失最小的那条：

$$\mathcal{L}_{\mathrm{final}} = \min_k \mathcal{L}_{\theta}(G^k, y_0, x) \tag{10}$$

消融实验（Table 6b）表明 $k=2$ 在样本多样性、准确性和保真度之间实现最佳平衡。

### 补充图表

![[assets/figures/papers/paper_list_l1872_CoMusion_Towards_Consistent_Stochastic_Human_Motion_Prediction_via_Motio/figures/001_Figure_1.jpg]]
*Figure 1: Top: Three joint motion trajectories (length 20), last 10 features vary among the last-observation-padded, noisepadded and groundtruth sequences. Bottom: Their corresponding DCT values*



## 实验与关键发现

### 主实验结果

CoMusion 在两个主流人体运动预测基准上均表现出显著优势，尤其在一致性与保真度指标上实现了跨越式提升。

**Human3.6M 数据集**（Table 1）：CoMusion 在全部八项指标上均达到最优。在准确性方面，ADE 达到 0.350，FDE 达到 0.458，分别优于此前最优的 **BeLFusion**（Barquero et al., CVPR 2023）的 0.372 和 0.474。更关键的是，在衡量运动行为一致性的 CMD 指标上，CoMusion 取得 3.202，相比 BeLFusion 的 5.988 降低 46.5%；在衡量生成分布质量的 FID 指标上，CoMusion 取得 0.102，相比 BeLFusion 的 0.209 降低 51.2%。这表明 CoMusion 生成的未来运动不仅在逐帧精度上更优，在整体运动模式和分布真实性上也大幅领先。

**AMASS 数据集**（Table 2）：在更具多样性的 AMASS 基准上，CoMusion 同样展现出强泛化能力。CMD 从 BeLFusion 的 16.995 降至 9.636，降幅达 43.3%；ADE 和 FDE 也分别取得 0.494 和 0.547 的最优结果。值得注意的是，CoMusion 在 APDE（多样性误差）指标上同样最优，说明其生成样本的多样性分布更贴近真实多模态分布，而非简单地扩大样本散布范围。

**逐帧行为分析**（Figure 3）：逐帧 ADE 曲线显示，CoMusion 在预测时域内的每一帧均保持最低误差，且误差增长斜率明显缓于其他方法。逐帧 CMD 曲线进一步揭示，基线方法（如 BeLFusion、MotionDiff）的累积位移分布误差随预测帧数增加而快速发散，而 CoMusion 的 CMD 增长受到有效抑制，验证了其生成运动与真值在行为模式上的长期一致性。

### 消融实验

消融实验系统性地验证了 CoMusion 三个核心设计选择的因果效应：双阶段架构、直接运动预测策略、以及修改的余弦方差调度器。

**架构组件消融**（Table 3 和 Table A.2）：移除 Transformer 重建模块 F(·) 会导致性能灾难性崩溃——在有 GCN 优化模块 R(·) 但无 F(·) 的配置下，CMD 从完整模型的 3.202 飙升至 259.037；同时移除 F(·) 和 R(·) 时，CMD 也高达 197.105。这确证了平滑的初始运动重建对后续 GCN 优化的不可或缺性：若直接将高噪声运动与历史拼接送入 GCN，输入-真值差异过大，DCT 空间的平滑性优势无法发挥。单独移除 R(·) 同样使所有指标恶化，证明 GCN 在 DCT 空间中的时空关系显式建模对最终预测质量有实质贡献。

**预测目标消融**（Table 4a）：将预测目标从直接预测未来运动 y₀ 切换为预测噪声 ε 后，ADE 从 0.350 恶化至 0.502，FID 从 0.102 恶化至 0.167。直接预测 y₀ 的策略使模型能够更有效地利用历史运动提供的强条件信号，将随机生成问题转化为接近确定性预测的简化问题，从而受益于 GCN-DCT 设计。

**方差调度器消融**（Table 4b 和 Table 5）：标准余弦调度器在 CoMusion 框架下表现次优（ADE 0.382，CMD 3.323），而标准线性调度器直接导致训练发散。提出的修改余弦调度器通过偏移量设计使初始 $\bar{\alpha}_0 = 0.5$，在所有指标上均取得最优。Table 5 进一步扫描 $\bar{\alpha}_0$ 取值，确认 0.5 在准确性与多样性之间达到最佳平衡：过高的 $\bar{\alpha}_0$ 使预测任务过于简单，模型倾向于过拟合历史运动而丧失多样性；过低的 $\bar{\alpha}_0$ 则使初始噪声过大，重建模块难以产生合理的初始估计。

**损失配置消融**（Table 6a）：同时重建运动历史 x（即 $\gamma > 0$）对性能有正向贡献，移除历史重建项会导致各指标下降。将结构感知的关节权重 $\lambda^j$ 替换为等权重建（$\lambda^j = 1$）同样使性能退化，验证了基于运动学链的加权策略对提升预测精度的有效性。

**多样性松弛参数**（Table 6b）：隐式多样性松弛中的采样数 k=2 实现了最佳整体性能。过大的 k 值虽略微提升样本多样性（APD），但会损害准确性和保真度指标，表明 k=2 在鼓励多模态与维持预测质量之间取得了最优权衡。

### 推理效率

CoMusion 采用仅 10 步扩散过程进行训练和推理（Figure 6），在 Human3.6M 上的单样本推理时间约为 0.05 秒（Table A.1），参数量与 BeLFusion 相当，显著低于 MotionDiff。扩散步数消融显示，10 步在质量与效率之间达到帕累托最优，进一步增加步数带来的性能增益边际递减，而计算成本线性增长。

![[assets/figures/papers/paper_list_l1872_CoMusion_Towards_Consistent_Stochastic_Human_Motion_Prediction_via_Motio/figures/009_Figure_6.jpg]]
*Figure 6: Ablation results on the number of diffusion steps. The bottom rightmost subfigure shows the per-sample time spent in seconds on Human3.6M inference*

### 失败模式与局限性

尽管 CoMusion 在整体指标上表现优异，仍需注意以下局限：

1. **调度器敏感性**：标准线性调度器导致训练发散（Table 4b 明确排除），表明框架对方差调度器的选择高度敏感，限制了调度器设计的通用性。
2. **绝对多样性并非最高**：CoMusion 的 APD 值为 7.632，低于部分基线方法（如 DLow 的 11.741）。虽然其 APDE（多样性误差）最优，说明多样性建模更贴合真实分布，但生成样本的绝对分布范围相对保守。
3. **DCT 系数依赖**：模型需要全部 DCT 系数才能达到最佳性能（Table A.5），截断系数会导致性能单调下降，这可能增加计算开销，不利于资源受限场景的部署。
4. **结构权重的领域限制**：结构感知损失依赖预定义的人体关节运动学权重，不适用于非人体骨架的运动数据类型，限制了跨领域迁移能力。
5. **高噪声下的重建质量**：当噪声水平极高（接近纯高斯噪声）时，Transformer 重建模块可能产生不合理的初始运动估计，影响后续 GCN 优化——该边界情形在文中未得到充分验证，需在实际部署中注意。

### 补充图表

![[assets/figures/papers/paper_list_l1872_CoMusion_Towards_Consistent_Stochastic_Human_Motion_Prediction_via_Motio/figures/003_Table_1.jpg]]
*Table 1: Quantitative results for Human3.6M dataset [27]. The best results are highlighted in bold. The symbol ‘-’ indicates that the results are not reported in the baseline work. For all metrics except for APD, lower is better*

![[assets/figures/papers/paper_list_l1872_CoMusion_Towards_Consistent_Stochastic_Human_Motion_Prediction_via_Motio/figures/004_Table_2.jpg]]
*Table 2: Quantitative results for AMASS dataset [48]. The best results are highlighted in bold. The symbol ‘-’ indicates that the results are not reported in the baseline work. As AMASS does not contain class labels, the FID metric is not used for evaluation*

![[assets/figures/papers/paper_list_l1872_CoMusion_Towards_Consistent_Stochastic_Human_Motion_Prediction_via_Motio/figures/007_Table_3.jpg]]
*Table 3: Ablation on CoMusion’s general architecture. In the Sched. column, ✓ denotes use of our proposed scheduler*

![[assets/figures/papers/paper_list_l1872_CoMusion_Towards_Consistent_Stochastic_Human_Motion_Prediction_via_Motio/figures/010_Table_4.jpg]]
*Table 4: Left (a): Ablation on prediction target. Right (b): Ablation on variance scheduler. Linear scheduler’s results are not included as it causes CoMusion to diverge*

![[assets/figures/papers/paper_list_l1872_CoMusion_Towards_Consistent_Stochastic_Human_Motion_Prediction_via_Motio/figures/011_Table_5.jpg]]
*Table 5: Effect of*

![[assets/figures/papers/paper_list_l1872_CoMusion_Towards_Consistent_Stochastic_Human_Motion_Prediction_via_Motio/figures/012_Table_6.jpg]]
*Table 6: Left (a): Ablation on loss configurations*

![[assets/figures/papers/paper_list_l1872_CoMusion_Towards_Consistent_Stochastic_Human_Motion_Prediction_via_Motio/figures/006_Figure_4.jpg]]
*Figure 4: Qualitative results of CoMusion compared with baseline methods. The upper block of rows corresponds to results obtained from the Human3.6M dataset, while the lower block of rows represents results from the AMASS dataset. The green-purple and the blue-orange skeletons denote the observed history and the predictions respectively*

![[assets/figures/papers/paper_list_l1872_CoMusion_Towards_Consistent_Stochastic_Human_Motion_Prediction_via_Motio/figures/005_Figure_3.jpg]]
*Figure 3: Left: ADE computed at each prediction frame of state-of-the-art methods. Right: CMD computed up to each prediction frame. Both experiments are conducted on Human3.6M dataset*



## 定位与知识库关联

### 1. 方法脉络与核心突破

CoMusion 处于随机人体运动预测（stochastic HMP）的扩散模型分支，其核心贡献在于弥合了确定性预测中成熟的时空建模设计与现有随机方法之间的鸿沟。

**瓶颈诊断。** 此前基于扩散模型的随机 HMP 方法（如 **MotionDiff** (Wei et al., ECCV 2022)、**BeLFusion** (Barquero et al., CVPR 2023)、**HumanMAC** (Chen et al., ICCV 2023)）普遍采用噪声预测范式，即网络直接预测扩散过程中的噪声 $\epsilon$，而非未来运动本身。这导致两个深层问题：其一，输入（噪声 $y_t$）与真值（未来运动 $y_0$）之间的差异巨大，使得网络难以受益于 DCT 空间的平滑性——而 DCT 空间已被确定性 HMP 广泛验证为对运动建模极为友好（见 Fig. 1 中噪声填充序列在 DCT 域的高频混乱）；其二，缺乏一个平滑的未来姿态初始化，使得预测与历史运动的一致性难以保证，往往需要复杂的多阶段训练来弥补。

**因果杠杆。** CoMusion 通过三个相互耦合的设计扭转了这一局面：

1. **预测目标切换**（噪声 $\epsilon$ → 未来运动 $y_0$）：直接预测 $y_0$ 将任务转化为一个更接近确定性预测的回归问题，使网络能够充分利用 DCT 空间的平滑先验。消融实验（Table 4a）表明，仅此一项便将 ADE 从 0.502 降至 0.350，FID 从 0.167 降至 0.102。

2. **平滑初始重建模块 $F(\cdot)$**：一个 8 层 Transformer 编码器从当前噪声 $y_t$ 中重建出平滑的 $\tilde{y}_0$，不依赖历史运动。这一模块是整个框架的基石——移除 $F(\cdot)$ 后，CMD 从 3.202 急剧恶化至 197.105（Table A.2），表明没有平滑初始化，后续的 GCN 优化几乎无法产生与历史一致的预测。

3. **修改的余弦方差调度器**：标准余弦调度器的初始 $\bar{\alpha}_0 \approx 1$，意味着在扩散初期 $y_t$ 几乎等于干净数据 $y_0$，网络可以直接从历史 $x$ 推断未来而无需真正“去噪”，导致过拟合。CoMusion 通过偏移调度器使 $\bar{\alpha}_0 = 0.5$（Eq. 7），确保整个去噪过程中预测任务保持非平凡，从而迫使网络真正学习从噪声中重建运动（Table 4b, Table 5）。

这三个设计形成了因果闭环：平滑初始化 $\tilde{y}_0$ 为 GCN 提供了良好的起点，GCN 在 DCT 空间中显式建模时空关节关系以优化整个序列，而修改的调度器则确保训练信号在整个扩散过程中保持有效。

### 2. 与基线方法的系统对比

**与扩散模型基线的本质差异。** 不同于 **MotionDiff**、**BeLFusion** 和 **HumanMAC** 等预测噪声的扩散方法，CoMusion 的直接运动预测策略使其网络架构可以自然地嵌入 GCN-DCT 设计。BeLFusion 虽然也关注行为一致性，但其 VAE 编码器-解码器结构并未显式建模关节间的空间关系；HumanMAC 则依赖掩码自编码器，同样缺乏对骨架拓扑的显式利用。

**与 GAN/VAE 基线的代际优势。** 相较于 **DLow** (Yuan and Kitani, ECCV 2020)、**GSPS** (Mao et al., ECCV 2020)、**DivSamp** (Dang et al., ICCV 2021) 等基于 GAN 或 VAE 的方法，CoMusion 在保真度指标上实现了代际跨越：在 Human3.6M 上，CMD 较 BeLFusion 降低 46.5%（3.202 vs 5.988），FID 降低 51.2%（0.102 vs 0.209），且 ADE/FDE 也达到最优（Table 1）。在 AMASS 上，CMD 较 BeLFusion 降低 43.3%（9.636 vs 16.995）（Table 2）。Fig. 3 的逐帧分析进一步揭示，CoMusion 的 ADE 优势随预测帧数增加而扩大，CMD 优势则从早期帧即已显现，表明其一致性和准确性在长时域预测中尤为突出。

**确定性方法的隐性继承。** CoMusion 并未直接继承某一具体确定性 HMP 方法的架构，但其 GCN-DCT 设计灵感显然源于该领域的成功实践。通过将随机预测转化为“平滑初始化 + 确定性优化”的两阶段过程，CoMusion 间接验证了 GCN-DCT 设计对运动时空关系的建模能力，并首次将其成功引入随机生成场景。

### 3. 适用边界与局限

**调度器敏感性。** 标准线性调度器直接导致训练发散（Table 4b），这表明 CoMusion 的预测范式对方差调度器的选择极为敏感。虽然修改的余弦调度器（$\bar{\alpha}_0 = 0.5$）在 Human3.6M 和 AMASS 上均表现优异，但该设计的通用性尚未在其他条件扩散任务中验证。

**绝对多样性与相对多样性的权衡。** CoMusion 的 APD（平均成对距离）并非最高，但其 APDE（多样性误差）达到最优（Table 1），这意味着模型生成的样本多样性更贴合真实分布，但绝对分布范围可能略小于某些 GAN 基方法。这一特性在需要覆盖极端多模态场景的应用中可能成为限制。

**计算与骨架依赖性。** 模型需要全部 DCT 系数才能达到最佳性能（Table A.5），这增加了计算开销。此外，结构感知损失（Eq. 9）依赖于预定义的关节运动学权重 $\lambda^j$，使其难以直接迁移到非人体骨架的运动数据（如动物运动或通用轨迹预测）。

**极端噪声下的初始重建质量。** 当噪声水平极高时（如 $t$ 接近 $T$），$F(\cdot)$ 的初始重建 $\tilde{y}_0$ 可能产生不合理的预测，进而影响后续 GCN 优化。虽然文中通过 Fig. 5 展示了 $F(y_T, T)$ 的平滑效果，但该图仅展示了单条轨迹的定性结果，未对极端噪声下的失效模式进行系统量化。

### 4. 开放问题与延伸方向

1. **调度器的跨任务泛化。** 修改的余弦调度器（$\bar{\alpha}_0 = 0.5$）是否适用于其他条件扩散模型任务（如文本到运动生成、图像生成）？其核心机制——通过降低初始信噪比来防止条件过拟合——可能具有更广泛的适用性，但需要跨领域验证。

2. **多样性与一致性的帕累托前沿。** 如何在保持高 CMD 和低 FID 的前提下进一步提升 APD？多样性松弛参数 $k=2$ 在 Table 6b 中实现了最佳平衡，但更大的 $k$ 值是否能通过调整其他超参来释放更多多样性，仍需探索。

3. **GCN-DCT 与加速采样的结合。** 当前模型使用 10 步 DDPM 采样，每样本推理时间约 0.05 秒（Table A.1）。GCN-DCT 设计是否能与 DDIM、一致性模型等更先进的加速采样技术结合，进一步减少去噪步数至 2-3 步而保持生成质量？

4. **长时域与复杂场景扩展。** 当前实验设定为预测 1 秒（25 帧）的未来运动。该框架能否扩展到 5 秒以上的长时域预测？在涉及人体-物体交互或多智能体交互的场景中，GCN 的图结构是否能自然地扩展为多骨架交互图？

5. **直接预测 $y_0$ 的容量上限。** 直接预测运动（而非噪声）是否在理论上限制了模型对极端多模态分布的捕捉能力？噪声预测范式允许网络通过预测一个简单的分布（高斯噪声）来间接建模复杂的数据分布，而 $y_0$ 预测则要求网络直接输出多模态的未来运动——这是否需要在网络中引入额外的随机单元（如隐变量或噪声注入）来弥补？



## 原文 PDF

![[paperPDFs/ECCV_2024/CoMusion_Towards_Consistent_Stochastic_Human_Motion_Prediction_via_Motion_Diffusion.pdf]]
