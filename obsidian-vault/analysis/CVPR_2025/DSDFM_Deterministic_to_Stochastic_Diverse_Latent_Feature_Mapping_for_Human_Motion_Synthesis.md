---
title: Deterministic-to-Stochastic Diverse Latent Feature Mapping for Human Motion Synthesis
type: paper
paper_level: A
venue: CVPR
year: 2025
pdf_ref: paperPDFs/CVPR_2025/DSDFM_Deterministic_to_Stochastic_Diverse_Latent_Feature_Mapping_for_Human_Motion_Synthesis.pdf
project_link: null
code_link: null
aliases:
- DDSDLFM
- DSDLFMHMS
tags:
- CVPR_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
- topic/representation_self_supervised_transfer
core_operator: 通过最优传输将高斯分布到潜空间的映射线性化（DerODE），并在推理阶段引入可控的随机微分方程（DivSDE），实现稳定训练与多样性增强的分离。
primary_logic: 将确定性直线映射与随机多样性生成分离，使得无需重新训练即可实现高效且多样化的运动合成。
claims:
- DerODE 采用最优传输匹配的直线路径训练，消除了复杂的去噪或分数估计过程。
- DivSDE 在采样阶段复用 DerODE 输出，通过噪声水平 η 控制多样性，无需额外训练。
- DSDFM 在 HumanAct12 无条件生成上取得了最优 FID (12.86) 和多样性 (18.41)，且参数量最少 (15M)。
- HumanAct12 Unconditional 上 FID↓ = 12.86
---

# Deterministic-to-Stochastic Diverse Latent Feature Mapping for Human Motion Synthesis

> [!tip] 核心洞察
> 将确定性直线映射与随机多样性生成分离，使得无需重新训练即可实现高效且多样化的运动合成。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向人体运动合成的确定性-随机化多样化潜特征映射方法 |
| 英文题名 | Deterministic-to-Stochastic Diverse Latent Feature Mapping for Human Motion Synthesis |
| 会议/期刊 | CVPR 2025 |
| Links |  |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion #topic/representation_self_supervised_transfer |
| Method | DSDFM (Deterministic-to-Stochastic Diverse Latent Feature Mapping) |
| Dataset | HumanAct12 Unconditional, HumanAct12 Action-to-Motion |

> [!tip] 效果简介
> - HumanAct12 Unconditional 上，FID↓ 12.86 vs 13.03 (Modi) (-1.31%)；Diversity↑ 18.41 vs 17.57 (Modi) (+4.78%)。
> - HumanAct12 Action-to-Motion 上，FID↓ 0.068 vs 0.072 (MotionDiffuse) (-5.6%)；Accuracy↑ 0.994 vs 0.991 (MotionDiffuse) (+0.3%)。

## 概要

### 问题定位

人体运动合成是计算机视觉与图形学中的核心任务，其目标是从高斯噪声或动作标签生成多样且逼真的三维人体运动序列。近年来，基于分数的生成模型（SGMs）和流匹配（Flow Matching）方法在该领域取得了显著进展，但它们在训练过程中普遍采用**弯曲的随机微分方程（SDE）轨迹**（如 VPSDE、VESDE），导致三个关键瓶颈：

1. **训练不稳定**：弯曲轨迹需要复杂的去噪或分数估计过程，收敛缓慢且对超参数敏感。
2. **采样效率低**：推理时需要大量离散化步数才能保证生成质量。
3. **质量-多样性难以兼得**：确定性ODE采样虽稳定但多样性不足，而随机采样在增强多样性的同时容易引入失真。

### 核心方法

针对上述问题，本文提出 **DSDFM**（Deterministic-to-Stochastic Diverse Latent Feature Mapping），其核心思想是**将确定性映射与随机多样性生成解耦**，使两者各司其职、互不干扰。DSDFM 包含两个关键模块：

- **DerODE（确定性常微分方程映射）**：利用最优传输（Optimal Transport）构建高斯分布到运动潜空间的**直线路径**，训练时仅需预测漂移量 $z_1 - z_0$，无需估计分数或执行去噪操作。这从根本上消除了弯曲轨迹带来的训练负担。
- **DivSDE（多样性随机微分方程生成）**：在推理阶段，DerODE 输出确定性结果后，DivSDE 通过注入可调噪声水平 $\eta$ 的随机过程来增强多样性。DivSDE **直接复用** DerODE 已计算的中间结果进行二次运算，无需引入任何额外训练。

这种“先确定、后随机”的两阶段设计，使得 DSDFM 在训练时享受直线轨迹的高效与稳定，在推理时又能灵活控制生成多样性。

### 主要结果

在 HumanAct12 数据集上，DSDFM 以仅 **15M** 的训练参数量（所有对比方法中最少），在无条件生成任务上取得了：

- **FID = 12.86**，优于此前最优的 Modi（13.03）及其他基于分数的生成方法；
- **Diversity = 18.41**，同样超越所有基线方法。

在动作到运动（Action-to-Motion）任务上，DSDFM 的 FID 达到 **0.068**，动作识别准确率达到 **0.994**，均优于 MotionDiffuse 等 SOTA 方法。

消融实验进一步验证了方法的高效性：相比 VPSDE 和 VESDE，DSDFM 的训练时间缩短约 **33%**（25.33 min vs. 37.68/37.70 min），且在使用仅 100 步推理时仍能保持较低 FID（13.61），体现了直线轨迹在采样效率上的显著优势。

### 方法定位

DSDFM 属于**基于潜空间的生成式人体运动合成方法**，其知识定位如下：

| 维度 | 定位 |
|------|------|
| **表征学习** | VQVAE（Transformer 编码器 + GRU 解码器）将运动序列压缩为离散潜变量 |
| **生成范式** | 确定性 ODE 映射（DerODE）+ 随机 SDE 增强（DivSDE），非扩散去噪范式 |
| **训练策略** | 最优传输配对 + 直线漂移预测，避免分数估计 |
| **推理策略** | 单次 DerODE 前向 + 可调噪声 DivSDE 反向，无需重训练 |
| **基线参照** | MDM (ICLR'23)、MLD (CVPR'23)、MotionDiffuse、Modi (CVPR'23) 等 |

> **注意**：本文未提供发表年份与会议信息，以上定位基于分析文本中的方法对比与引用推断，建议在正式引用时核实原始论文的发表状态。



人体运动合成旨在生成自然、逼真且多样化的人体动作序列，在动画制作、虚拟现实、人机交互等领域具有广泛应用。近年来，深度生成模型在该领域取得了显著进展，其中基于分数的生成模型（Score-based Generative Models, SGMs）和流匹配（Flow Matching）方法展现出强大的生成能力。然而，这些方法在人体运动生成中面临一个核心瓶颈：**训练过程采用曲线轨迹，导致训练不稳定、采样效率低，且难以同时保证生成质量与多样性**。

具体而言，当前主流方法（如 VPSDE、VESDE）在训练阶段需要估计复杂的分数函数或执行去噪过程，其扩散路径本质上是弯曲的 SDE 轨迹。这种弯曲路径不仅增加了训练的收敛难度，还迫使模型在推理时需要大量采样步数才能获得高质量结果。此外，这些方法的多样性完全依赖于固定的随机后验或确定性 ODE 演化，缺乏可控的多样性调节机制——一旦训练完成，生成样本的多样性便被锁定，无法在不重新训练的情况下按需调整。

上述问题形成了一个“质量-多样性-效率”的三元困境：提升生成质量往往需要更多采样步数，牺牲效率；增强多样性可能引入失真，损害质量；而追求训练效率则可能限制模型的表达能力。因此，**如何设计一种能够稳定训练、高效采样，且在推理阶段可灵活控制多样性的生成框架**，成为该领域亟待解决的关键问题。

本文的动机正是源于对这一困境的深入观察。作者提出 DSDFM（Deterministic-to-Stochastic Diverse Latent Feature Mapping），其核心思路是将确定性映射与随机多样性生成**解耦**：在训练阶段，通过最优传输（Optimal Transport）将高斯分布到潜空间的映射线性化，使模型仅需学习直线漂移量，从而消除复杂的去噪或分数估计过程，实现稳定高效的训练；在推理阶段，引入可调噪声水平的随机微分方程（DivSDE），复用确定性映射的输出进行二次计算，在无需额外训练的前提下实现多样性增强。这种“先确定、后随机”的设计哲学，使得模型既能享受直线轨迹带来的训练与采样效率优势，又能获得可控的生成多样性。



## 核心方法与创新机理

DSDFM 的核心创新在于将人体运动生成中的**确定性映射**与**随机多样性生成**解耦为两个独立阶段，从而在无需重新训练的情况下同时保证生成质量、多样性与采样效率。相较于现有基于分数的生成模型（SGMs）和流匹配方法，DSDFM 在以下三个关键维度上实现了根本性改变：

### 1. 训练轨迹的线性化：从弯曲路径到最优传输直线

传统 SGMs（如 VPSDE、VESDE）在训练过程中依赖弯曲的 SDE 路径，需要估计复杂的分数函数或执行多步去噪，导致训练不稳定且收敛缓慢。DSDFM 通过引入最优传输（Optimal Transport）理论，将高斯分布到潜空间的映射线性化。具体而言，DerODE 模块利用最优传输匹配样本对 $(z_0, z_1) \sim \pi$，直接学习从标准高斯噪声到潜变量的**直线漂移量** $z_1 - z_0$，训练损失简化为：

$$\min_{\theta} J_{drift} = \mathbb{E}_{(z_0, z_1) \sim \pi}[||v_{\theta}(z_t, t) - (z_1 - z_0)||_2^2]$$

这一设计使得 DerODE **无需涉及复杂的去噪或分数估计过程**（Section 4.2.1），从根本上简化了训练范式。

### 2. 多样性生成机制的后置化：DivSDE 的推理时注入

现有方法通常将多样性完全耦合在确定性 ODE 或固定的 SDE 后验中，难以灵活控制生成结果的多样性。DSDFM 提出了 DivSDE（Diverse Stochastic Differential Equation），在推理阶段引入可控的随机微分方程：

$$dz_t = \left(-\frac{1}{1-t}\right) z_t dt + \eta \sqrt{\frac{2t}{1-t}} d w_t$$

DivSDE 的关键优势在于**直接复用 DerODE 的确定性输出** $\widetilde{z}_{0,i}$ 进行二次计算，无需引入额外的训练过程（Section 4.2.2）。通过调节噪声水平 $\eta$，用户可以在推理时动态控制多样性强度——$\eta$ 越大，生成的运动序列越多样化。这一设计实现了训练效率与推理灵活性的双重提升。

### 3. 效率-质量-多样性的三赢架构

上述两个 changed slots 的组合带来了系统性的性能提升：

- **训练效率**：在 HumanAct12 数据集上，DSDFM 的训练时间仅为 25.33 分钟，显著低于 VPSDE（37.68 分钟）和 VESDE（37.70 分钟）（Table 5）。在更大的 HumanML3D 数据集上，训练时间进一步缩短至 7.02 分钟（Table 4）。
- **生成质量**：在 HumanAct12 无条件生成任务上，DSDFM 取得了最优 FID（12.86），优于 Modi（13.03）等 SOTA 方法（Table 1）。
- **多样性**：多样性指标达到 18.41，同样超越 Modi（17.57），验证了 DivSDE 的有效性（Table 1）。
- **参数效率**：DSDFM 仅需 15M 参数即可实现上述性能，在所有对比方法中参数量最少（Table 1）。

### 方法对比总结

| 创新维度 | 基线方法（SGMs/流匹配） | DSDFM |
|---------|----------------------|-------|
| 训练轨迹 | 弯曲的 SDE 路径 | 最优传输直线路径 |
| 训练过程 | 需要估计分数或去噪 | 仅需预测漂移量 $(z_1 - z_0)$ |
| 多样性机制 | 耦合在训练过程中 | 推理时通过 $\eta$ 独立控制 |
| 重新训练需求 | 改变多样性需重新训练 | 无需重新训练 |

这种“确定性骨架 + 随机性外挂”的架构设计，使得 DSDFM 在保持高质量生成的同时，实现了训练与推理的双重高效，为人体运动合成提供了一种更优雅且实用的解决方案。



DSDFM（Deterministic-to-Stochastic Diverse Latent Feature Mapping）将人体运动合成分解为两个解耦的阶段，分别对应**潜空间重建**与**多样化生成**，其总览如 **Figure 2** 所示。第一阶段（红色箭头）通过 VQVAE 学习人体运动的紧凑潜表征；第二阶段（绿色箭头）先利用确定性常微分方程（DerODE）建立高斯分布到潜空间的直线映射，再在推理时注入可控的随机微分方程（DivSDE）以产生多样化输出。两阶段分离的核心动机在于：传统基于分数的生成模型（SGMs）与流匹配方法依赖弯曲的 SDE 训练轨迹，导致训练不稳定、采样效率低，且生成质量与多样性难以兼得。DSDFM 将确定性直线映射与随机多样性生成解耦，从而无需重新训练即可灵活调节多样性。

![[assets/figures/papers/paper_list_l1856_DSDFM_Deterministic_to_Stochastic_Diverse_Latent_Feature_Mapping_for_Hum/figures/002_Figure_2.jpg]]
*Figure 2: The overview of the proposed method DSDFM. The red arrow denotes the first stage and the green arrow denotes the second stage of DSDFM*

**阶段一：人体运动重建（Human Motion Reconstruction）**  
该阶段的目标是获得能够紧凑表达人体运动序列的潜空间。输入为人体运动序列 $\boldsymbol{E}$，经过由 Transformer 编码器与 GRU 解码器构成的 VQVAE 网络，得到重建运动 $\hat{\boldsymbol{E}}$ 及其对应的离散潜变量 $\boldsymbol{z}$。训练损失 $\mathcal{L}_{VQ}$ 包含三项：重建误差、码本向潜变量靠拢的承诺损失，以及潜变量向码本靠拢的编码器损失，具体形式为  

$$
\mathcal{L}_{VQ} = \mathcal{L}(\boldsymbol{E}, \hat{\boldsymbol{E}}) + ||\hat{\boldsymbol{z}} - \mathrm{sg}(\boldsymbol{z})||_2^2 + \beta ||\mathrm{sg}(\hat{\boldsymbol{z}}) - \boldsymbol{z}||_2^2,
$$

其中 $\mathrm{sg}(\cdot)$ 表示停止梯度算子，$\beta$ 为平衡系数。该阶段训练完成后，编码器输出的潜变量 $\boldsymbol{z}$ 将作为第二阶段生成模块的目标分布。

**阶段二：多样化运动生成（Diverse Motion Generation）**  
该阶段进一步分为两个子模块——确定性特征映射（DerODE）与随机多样化输出生成（DivSDE），二者在训练与推理阶段承担不同角色。

- **DerODE（训练 + 推理）**：训练时，DerODE 学习从标准高斯分布 $\mathcal{N}(0, I)$ 到阶段一潜空间分布的直线映射。为使训练路径尽量平直，引入最优传输（Optimal Transport）为两个分布的样本建立匹配对 $(z_0, z_1)$，并最小化漂移预测损失  

  $$
  \min_{\theta} J_{drift} = \mathbb{E}_{(z_0, z_1) \sim \pi}\left[||v_{\theta}(z_t, t) - (z_1 - z_0)||_2^2\right],
  $$

  其中 $v_{\theta}$ 为待学习的漂移网络，$\pi$ 为最优传输方案。该设计使 DerODE 在训练阶段完全避免了复杂的去噪或分数估计过程。推理时，给定高斯噪声 $\widetilde{z}_{1}$，通过单步确定性映射即可获得潜变量  

  $$
  \widetilde{z}_{0} = \widetilde{z}_{1} - v_{\theta}(\widetilde{z}_{1}, t=1) = \mathrm{DerODE}(\widetilde{z}_{1}).
  $$

- **DivSDE（仅推理）**：为在不重新训练的前提下增强生成多样性，DivSDE 在推理阶段复用 DerODE 的输出 $\widetilde{z}_{0}$，通过正向与反向 SDE 注入可控噪声。其正向过程为  

  $$
  dz_t = \left(-\frac{1}{1-t}\right) z_t dt + \eta \sqrt{\frac{2t}{1-t}} dw_t,
  $$

  反向过程的离散更新步为  

  $$
  z_{i,t} = z_{t+\Delta t,i} + \frac{\Delta t}{1-t} z_{t+\Delta t,i} + \frac{2t\Delta t}{1-t} \frac{(1-t)\widetilde{z}_{0,i} - z_{t,i}}{t^2} + \eta \varepsilon \sqrt{\frac{2t}{1-t}} \sqrt{\Delta t},
  $$

  其中 $\eta$ 为多样性强度系数——增大 $\eta$ 可获得更丰富的运动变化，减小 $\eta$ 则趋于确定性结果。DivSDE 的更新直接借用 DerODE 已计算的 $\widetilde{z}_{0}$，无需引入额外训练过程。

**整体数据流**  
1. 从标准高斯分布采样噪声 $\widetilde{z}_1$。  
2. 经 DerODE 确定性映射得到潜变量 $\widetilde{z}_0$。  
3. 将 $\widetilde{z}_0$ 送入 DivSDE 反向过程，以 $\eta$ 控制多样性，得到多样化潜变量 $z_{0,i}$。  
4. 通过阶段一的 VQVAE 解码器将 $z_{0,i}$ 重建为多样化的人体运动序列。  

这一 pipeline 将训练复杂度压缩至直线路径上的漂移预测，同时将多样性控制完全置于推理阶段，实现了训练稳定性、采样效率与生成多样性的分离优化。



DSDFM 由两个核心阶段构成：第一阶段通过 VQVAE 学习人体运动的紧凑潜空间表征；第二阶段通过确定性特征映射（DerODE）与随机多样化生成（DivSDE）实现从高斯噪声到多样化运动潜变量的高效转换。以下分别阐述各模块的设计逻辑与关键公式。

### 运动重建模块：VQVAE

第一阶段旨在将原始运动序列压缩为低维潜变量，同时保留时空动态特征。编码器由 Transformer 与 GRU 组合实现，解码器对称设计。训练目标为：

$$
\mathcal{L}_{VQ} = \mathcal{L}(E, \hat{E}) + \|\hat{z} - \text{sg}(z)\|_2^2 + \beta \|\text{sg}(\hat{z}) - z\|_2^2
$$

其中 $\mathcal{L}(E, \hat{E})$ 为运动重建损失，$\hat{z}$ 为编码器输出，$z$ 为码本中最近邻向量，$\text{sg}(\cdot)$ 为梯度截断算子。第二项约束码本向编码器输出靠拢，第三项约束编码器输出向码本靠拢，$\beta$ 为平衡系数。该模块为后续生成阶段提供结构化的潜空间。

### 确定性特征映射：DerODE

第二阶段的核心是将标准高斯分布映射到 VQVAE 潜空间。传统基于分数的生成模型（如 VPSDE/VESDE）依赖弯曲的随机轨迹进行训练，需要估计分数函数或执行复杂去噪。DerODE 通过最优传输（OT）将映射路径线性化，使训练目标简化为直接预测漂移量。

**漂移函数导出**：给定高斯概率路径 $z_t \sim \mathcal{N}(\mu(t), \sigma^2(t)I)$，其漂移函数由命题 1 给出：

$$
u(z_t, t) = \sigma'(t) \cdot \frac{z(t) - \mu(t)}{\sigma(t)} + \mu'(t)
$$

该漂移完全由高斯路径的均值与方差的时间导数决定，无需估计分数。

**最优传输配对**：为获得更直的训练路径，引入 OT 理论寻找两个分布间的最小位移配对 $\pi$：

$$
\min_{\pi \in \Delta} J_{OT} = \langle \pi, C \rangle
$$

其中 $C$ 为代价矩阵。通过 OT 配对 $(z_0, z_1) \sim \pi$，漂移预测网络 $v_\theta$ 的损失函数简化为：

$$
\min_{\theta} J_{drift} = \mathbb{E}_{(z_0, z_1) \sim \pi}\left[\|v_\theta(z_t, t) - (z_1 - z_0)\|_2^2\right]
$$

该损失仅需预测起点到终点的直线漂移量 $(z_1 - z_0)$，避免了去噪或分数估计的复杂训练过程。

**确定性生成**：推理时，给定高斯噪声 $\widetilde{z}_{1,i}$，DerODE 通过一步映射得到确定性潜变量：

$$
\widetilde{z}_{0,i} = \widetilde{z}_{1,i} - v_\theta(\widetilde{z}_{1,i}, t=1) = \text{DerODE}(\widetilde{z}_{1,i})
$$

### 随机多样化生成：DivSDE

DerODE 输出为确定性结果，为增强多样性，DivSDE 在推理阶段注入可控噪声，复用 DerODE 的输出进行二次计算，无需额外训练。

**DivSDE 前向过程**定义为：

$$
dz_t = \left(-\frac{1}{1-t}\right) z_t dt + \eta \sqrt{\frac{2t}{1-t}} dw_t
$$

其中 $\eta$ 为多样性强度控制参数——$\eta$ 越大，生成运动的多样性越高。该 SDE 的漂移项将潜变量推向原点，扩散项引入随机扰动。

**DivSDE 反向离散更新**：为从噪声恢复多样化潜变量，反向过程利用 DerODE 的输出 $\widetilde{z}_{0,i}$ 作为条件，单步离散更新为：

$$
z_{i,t} = z_{t+\Delta t,i} + \frac{\Delta t}{1-t} z_{t+\Delta t,i} + \frac{2t\Delta t}{1-t} \frac{(1-t)\widetilde{z}_{0,i} - z_{t,i}}{t^2} + \eta \varepsilon \sqrt{\frac{2t}{1-t}} \sqrt{\Delta t}
$$

其中 $\varepsilon \sim \mathcal{N}(0,I)$，$\Delta t$ 为时间步长。该更新包含三项：漂移项将 $z$ 推向原点，确定性引导项利用 $\widetilde{z}_{0,i}$ 提供结构约束，噪声项通过 $\eta$ 调节多样性强度。DivSDE 直接借用 DerODE 已计算的结果，无需重新引入其他训练过程，实现了确定性映射与随机多样性的解耦。



## 实验与关键发现

### 评估设置

实验在两个主流人体运动数据集上开展：**HumanAct12**（12 类动作，无条件生成与动作条件生成）和 **HumanML3D**（更大规模文本-运动数据集，用于效率消融）。评估指标覆盖质量与多样性两个维度：FID↓ 和 KID↓ 衡量生成分布与真实分布的差异；Precision↑ / Recall↑ 分别反映生成样本的保真度和覆盖度；Diversity↑ 度量生成运动之间的平均差异；Multimodality↑ 用于条件生成任务，评估同一条件生成不同运动的能力。所有实验均在 NVIDIA A100 GPU 上完成，训练与推理时间在同一硬件条件下测量，确保公平可比。

### 无条件生成主结果

Table 1 报告了 HumanAct12 无条件生成任务的全面对比。DSDFM 在所有指标上均达到最优：

![[assets/figures/papers/paper_list_l1856_DSDFM_Deterministic_to_Stochastic_Diverse_Latent_Feature_Mapping_for_Hum/figures/003_Table_1.jpg]]
*Table 1: The comparison results of unconditional human motion synthesis between our method and state-of-the-art methods on HumanAct12 dataset. Bold and underline indicate the best and the second best result*

- **FID↓：12.86**，优于 Modi（13.03）、MLD（14.24）、MDM（15.21）等强基线，相对 Modi 提升约 1.3%。
- **KID↓：0.10**，显著低于第二名 Modi 的 0.20，表明生成分布与真实分布在特征空间中的差异极小。
- **Diversity↑：18.41**，超过 Modi 的 17.57 和真实数据的 17.86，说明 DSDFM 不仅覆盖了真实运动的多样性，还产生了更丰富的变体。
- **Precision↑ / Recall↑：0.75 / 0.85**，同时保持高保真度和高覆盖度，避免了生成模型中常见的质量-多样性权衡困境。

值得注意的是，DSDFM 的参数量仅为 **15M**，远低于 Modi（30M）、MDM（233M）、MotionDiffuse（318M）等方法，实现了性能与效率的双重优势。

### 动作条件生成主结果

在 HumanAct12 的 Action-to-Motion 任务上（Table 2），DSDFM 同样展现出领先性能：

![[assets/figures/papers/paper_list_l1856_DSDFM_Deterministic_to_Stochastic_Diverse_Latent_Feature_Mapping_for_Hum/figures/005_Table_2.jpg]]
*Table 2: The comparison results of Action-to-Motion task on HumanAct12 dataset. ± indicates 95% confidence interval, → indicates that closer to real is better. The best results are in bold*

- **FID↓：0.068**，优于 MotionDiffuse 的 0.072 和 MDM 的 0.320，相对 MotionDiffuse 提升约 5.6%。
- **Accuracy↑：0.994**，略高于 MotionDiffuse 的 0.991，表明生成的运动与输入动作类别高度一致。
- **Diversity↑：17.99** 和 **Multimodality↑：16.60**，均接近真实数据水平（18.10 / 17.19），证明条件控制并未牺牲多样性。

这些结果验证了 DerODE 的确定性映射能够精准捕捉动作条件与运动潜变量之间的对应关系，而 DivSDE 在推理阶段注入的随机性则有效丰富了运动表现。

### 消融研究

#### 生成机制对比

Table 5 将 DSDFM 与基于分数的生成模型（VPSDE、VESDE）进行直接对比。在相同实验设置下：

![[assets/figures/papers/paper_list_l1856_DSDFM_Deterministic_to_Stochastic_Diverse_Latent_Feature_Mapping_for_Hum/figures/006_Table_5.jpg]]
*Table 5: Ablation studies of the proposed method. We compare our method with other score-based methods and provide the comparison results under the accuracy and diversity metrics, as well as the number of training parameters*

- **训练时间**：DSDFM 仅需 **25.33 min**，而 VPSDE 和 VESDE 分别需要 37.68 min 和 37.70 min，效率提升约 33%。
- **FID↓**：DSDFM 的 12.86 显著优于 VPSDE 的 14.92 和 VESDE 的 14.94。
- **参数量**：DSDFM 的 15M 同样低于 VPSDE（23M）和 VESDE（23M）。

这一消融直接验证了核心设计动机：曲线轨迹训练（VPSDE/VESDE）不仅增加了训练复杂度，还导致生成质量下降；而 DerODE 通过最优传输获得的直线路径，使得模型只需学习简单的漂移预测，无需复杂的去噪或分数估计过程。

#### 推理步数影响

Table 3 考察了推理步数对性能的影响。DSDFM 在仅使用 **100 步**时即可达到 FID 13.61，而使用 1000 步时 FID 为 12.86。相比之下，VPSDE 在 100 步时 FID 高达 18.41，VESDE 为 18.13。这一结果验证了直线轨迹的核心优势：由于 DerODE 学习的映射路径接近直线，即使使用较少步数的离散化求解，累积误差也远小于曲线路径上的方法。

![[assets/figures/papers/paper_list_l1856_DSDFM_Deterministic_to_Stochastic_Diverse_Latent_Feature_Mapping_for_Hum/figures/007_Table_3.jpg]]
*Table 3: Ablation study on the comparison results of training and inference time on the HumanAct12 dataset. m denotes minute, s denotes second*

#### 跨数据集效率验证

Table 4 在更大规模的 HumanML3D 数据集上进一步验证效率优势。DSDFM 的训练时间仅为 **7.02 min**，推理时间 1.21 s，均显著低于 VPSDE（11.94 min / 2.78 s）和 VESDE（11.96 min / 2.75 s）。这证明了最优传输配对策略和直线漂移学习在不同数据规模下的稳定高效性。

![[assets/figures/papers/paper_list_l1856_DSDFM_Deterministic_to_Stochastic_Diverse_Latent_Feature_Mapping_for_Hum/figures/004_Table_4.jpg]]
*Table 4: Ablation study on the comparison results of training and inference time on the HumanML3D dataset*

### 可视化分析

Figure 3 展示了 DSDFM 在不同设置下的生成结果，包括无条件生成和动作条件生成。可视化结果表明，生成的运动序列在时序连贯性和动作自然度上均表现良好。Figure 7 提供了与 SOTA 方法的定性对比，DSDFM 生成的运动在多样性和准确性上均具有竞争力。Figure 8 以散点图形式呈现了参数量与 FID 的关系，DSDFM 位于左下角区域，即最少参数量与最低 FID 的交汇点，直观体现了方法的效率优势。

![[assets/figures/papers/paper_list_l1856_DSDFM_Deterministic_to_Stochastic_Diverse_Latent_Feature_Mapping_for_Hum/figures/008_Figure_3.jpg]]
*Figure 3: Qualitative results of DSDFM. We present the generated human motion sequences under different settings. The unconditional human motion sequences (top) are generated from the HumanAct12 dataset. The Action-to-Motion results (bottom) show the generated diverse motion sequences under the Sit and Run action labels, which are sampled from the HumanML3D dataset*

![[assets/figures/papers/paper_list_l1856_DSDFM_Deterministic_to_Stochastic_Diverse_Latent_Feature_Mapping_for_Hum/figures/012_Figure_7.jpg]]
*Figure 7: The qualitative comparison results of the state-of-the-art methods and our proposed DSDFM*

![[assets/figures/papers/paper_list_l1856_DSDFM_Deterministic_to_Stochastic_Diverse_Latent_Feature_Mapping_for_Hum/figures/013_Figure_8.jpg]]
*Figure 8: Comparison of the training parameter and the corresponding FID metric*

### 失败模式与局限

尽管 DSDFM 在定量指标上表现优异，论文未系统报告失败案例或特定动作类型上的退化情况。从方法设计角度，以下潜在局限值得关注：

1. **极端动作的覆盖**：最优传输配对依赖于训练集中存在的运动模式，对于罕见或极端动作，OT 配对可能无法提供高质量的对应关系，导致生成质量下降。这一点在论文中未被验证。
2. **η 参数敏感性**：DivSDE 的多样性强度由噪声水平 η 控制，论文未提供 η 的自动调节机制或不同 η 值下的系统对比，实际应用中可能需要手动调参以平衡质量与多样性。
3. **长序列生成**：实验主要在 HumanAct12 和 HumanML3D 上进行，未涉及超长运动序列的生成评估，直线轨迹假设在长时序场景下的累积误差特性尚不明确。

以上局限需结合实际应用场景进行手动验证。

### 补充图表

![[assets/figures/papers/paper_list_l1856_DSDFM_Deterministic_to_Stochastic_Diverse_Latent_Feature_Mapping_for_Hum/figures/001_Figure_1.jpg]]
*Figure 1: Examples of the inference process for human motion synthesis. Our method aims to generate diverse and accurate human motion sequences through the designed generative model*

![[assets/figures/papers/paper_list_l1856_DSDFM_Deterministic_to_Stochastic_Diverse_Latent_Feature_Mapping_for_Hum/figures/010_Figure_5.jpg]]
*Figure 5: Qualitative results of DSDFM. We present more generated unconditional human motion sequences*

![[assets/figures/papers/paper_list_l1856_DSDFM_Deterministic_to_Stochastic_Diverse_Latent_Feature_Mapping_for_Hum/figures/011_Figure_6.jpg]]
*Figure 6: Qualitative results of DSDFM. We present the diverse human motion sequences under different actions*



## 定位与知识库关联

### 1. 问题定位：分数生成模型的瓶颈

DSDFM（Deterministic-to-Stochastic Diverse Latent Feature Mapping）的提出根植于对当前主流人体运动生成范式的系统性反思。基于分数的生成模型（Score-based Generative Models, SGMs）和流匹配（Flow Matching）方法虽然在图像、音频等领域取得了显著成功，但在人体运动合成任务中暴露出结构性缺陷：**训练轨迹的弯曲性**。具体而言，VPSDE（Variance Preserving SDE）和VESDE（Variance Exploding SDE）等标准扩散框架依赖曲线路径将高斯噪声逐步转化为目标分布，这导致了三个连锁问题：

1. **训练不稳定**：曲线轨迹要求网络学习复杂的分数函数或去噪过程，梯度信号在时间维度上高度非均匀。
2. **采样效率低**：推理时需要大量离散化步骤（通常1000步）才能逼近真实分布，限制了实时应用。
3. **质量-多样性权衡困难**：现有方法将确定性生成与随机多样性耦合在同一训练过程中，难以独立优化其中任一维度。

DSDFM的核心洞察在于：**将确定性直线映射与随机多样性生成解耦为两个独立阶段**，从而在不重新训练的前提下，同时实现高效采样与可控多样性。

### 2. 与现有工作的关系图谱

#### 2.1 运动生成基线对比

DSDFM在HumanAct12数据集上的无条件生成任务中，与以下代表性方法进行了直接对比（Table 1）：

- **VPoser**（CVPR 2019）：基于变分自编码器的姿态先验模型，参数化人体姿态的潜空间分布，但缺乏时序建模能力。
- **Action2Motion**（MM 2021）：条件VAE框架，通过动作标签引导运动生成，但多样性受限于VAE的先验假设。
- **ACTOR**（CVPR 2021）：Transformer-based的VAE，引入动作条件编码器，在条件生成任务上表现优异。
- **MDM**（ICLR 2023）：基于扩散模型的运动生成方法，直接对原始运动数据建模，但训练和推理成本较高。
- **MLD**（CVPR 2023）：潜空间扩散模型，通过将扩散过程压缩到潜空间加速采样，但仍需估计分数函数。
- **Modi**（CVPR 2023）：当时SOTA方法，在FID和Diversity指标上均取得领先。
- **MotionDiffuse**：基于文本条件的扩散模型，在Action-to-Motion任务中表现突出。

DSDFM在参数量最少（15M）的条件下，以FID=12.86超越了Modi的13.03（↓1.31%），Diversity达到18.41（↑4.78%），验证了直线轨迹训练与多样性注入分离策略的有效性。

#### 2.2 训练范式演进

DSDFM的方法论定位可追溯至三个关键范式的交叉点：

**（1）从SGM到流匹配的路径简化**

传统SGMs（如DDPM、Score SDE）的弯曲轨迹迫使网络学习复杂的分数估计。流匹配方法（Flow Matching）通过构造直线条件概率路径简化训练目标，但仍需在推理时求解ODE。DSDFM的DerODE模块继承了流匹配的直线路径思想，但通过**最优传输（Optimal Transport, OT）**显式配对高斯样本与潜变量样本，将训练目标进一步简化为直接预测漂移量 $z_1 - z_0$（Eq. 8），完全避免了去噪或分数估计过程。这一设计在概念上类似于Rectified Flow的直线化策略，但DSDFM将其应用于潜空间且无需迭代矫正。

**（2）两阶段生成架构**

DSDFM采用“重建-生成”两阶段架构：第一阶段使用VQVAE学习运动潜空间（Section 4.1），第二阶段在该潜空间上进行生成（Section 4.2）。这与MLD的潜空间扩散策略相似，但关键区别在于：
- MLD在潜空间仍使用扩散模型的去噪范式。
- DSDFM的第二阶段完全基于最优传输驱动的确定性映射（DerODE）和推理时注入的随机微分方程（DivSDE），训练过程无需估计分数或去噪。

**（3）可控多样性的推理时注入**

DivSDE的噪声水平 $\eta$ 作为可控旋钮，允许用户在推理时调节多样性强度（Section 4.2.2）。这与条件扩散模型中的引导尺度（guidance scale）有功能相似性，但机制不同：DivSDE通过修改反向SDE的扩散项直接注入噪声，而非修改分数估计的梯度方向。这种设计使得多样性增强完全独立于训练过程，无需重新训练即可适应不同应用场景。

### 3. 方法适用边界

#### 3.1 任务适配性

DSDFM的设计主要针对以下场景：

- **无条件生成**：从随机噪声生成多样化的人体运动序列，适用于数据增强、动画素材生成等。
- **动作条件生成**（Action-to-Motion）：给定动作标签（如“走路”、“跳跃”），生成符合该动作类别的运动序列。Table 2显示DSDFM在FID（0.068 vs 0.072）和Accuracy（0.994 vs 0.991）上均超越MotionDiffuse。
- **高效推理需求**：Table 3和Table 4的消融实验表明，DSDFM在HumanAct12上训练仅需25.33分钟（vs VPSDE的37.68分钟），在HumanML3D上仅需7.02分钟，且使用100步推理即可达到FID=13.61，验证了其在资源受限场景下的优势。

#### 3.2 潜在局限与未验证边界

尽管DSDFM在现有基准上表现优异，以下边界条件尚待验证或需谨慎对待：

1. **复杂运动类型的泛化性**：HumanAct12和HumanML3D主要包含单人、日常动作。对于双人交互、体育动作、舞蹈等高度动态或接触密集的运动类型，VQVAE的潜空间表达能力及最优传输配对策略是否依然有效，论文未提供证据。

2. **噪声水平 $\eta$ 的自动调节**：DivSDE的多样性控制依赖人工设定 $\eta$ 值。论文未讨论如何根据输入条件或期望多样性自动调节该参数，在实际部署中可能需要额外的标定流程。

3. **最优传输的计算开销**：虽然训练时间缩短，但最优传输配对本身引入的计算成本（尤其在潜空间维度较高或批次较大时）未被详细分析。对于更大规模数据集，OT的离散化误差和计算瓶颈可能成为限制因素。

4. **与其他模态的跨域迁移**：DSDFM的两阶段框架和直线化策略理论上可迁移至图像、音频等生成任务，但论文未提供实验验证。潜空间VQVAE的离散表示特性是否适用于连续信号生成，需要进一步研究。

### 4. 开放问题

基于DSDFM的当前设计，以下开放问题值得后续工作探索：

1. **DivSDE机制的训练端融合**：当前DivSDE仅在推理时注入噪声。是否可以将多样性增强机制融入训练过程（例如通过对抗训练或信息瓶颈），使模型学习到更鲁棒的多样性表征？

2. **多条件可控生成**：DSDFM目前支持动作类别条件。扩展到文本描述、风格标签、物理约束等多模态条件时，DerODE的确定性映射如何与条件信息交互？

3. **长序列生成的稳定性**：人体运动的长序列生成容易出现漂移和伪影。DSDFM的直线轨迹是否在长时域（>10秒）仍能保持稳定，以及DivSDE的噪声累积效应如何，需要系统评估。

4. **与物理模拟器的结合**：生成的运动可能违反物理约束（如脚部滑动、关节超限）。将DSDFM与物理模拟器或运动学约束结合，在保持多样性的同时提升物理合理性，是一个有前景的方向。

5. **最优传输策略的改进**：当前使用离散OT进行配对。引入连续归一化流（Continuous Normalizing Flows）或熵正则化OT是否能进一步提升配对质量与训练稳定性？

### 5. 知识库定位总结

DSDFM在人体运动生成领域的方法谱系中占据以下位置：

- **训练范式**：从“弯曲轨迹+分数估计”（SGMs）演进为“直线轨迹+漂移预测”（流匹配+OT），属于**训练效率优化**分支。
- **生成架构**：从“端到端扩散”演进为“潜空间VQVAE+两阶段映射”，属于**解耦式生成**分支。
- **多样性控制**：从“训练时隐式学习”演进为“推理时显式注入”，属于**可控多样性**分支。

该方法的核心贡献在于**通过最优传输实现训练与推理的机制分离**，为生成模型的设计提供了一个可泛化的范式：确定性映射负责质量，随机注入负责多样性，两者独立优化、协同工作。



## 原文 PDF

![[paperPDFs/CVPR_2025/DSDFM_Deterministic_to_Stochastic_Diverse_Latent_Feature_Mapping_for_Human_Motion_Synthesis.pdf]]
