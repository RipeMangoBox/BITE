---
title: "Multimodal Motion Conditioned Diffusion Model for Skeleton-based Video Anomaly Detection"
type: paper
paper_level: A
venue: ICCV
year: 2023
pdf_ref: paperPDFs/ICCV_2023/Multimodal_Motion_Conditioned_Diffusion_Model_for_Skeleton_based_Video_Anomaly_Detection.pdf
aliases:
- MMCDMSBVAD
tags:
- ICCV_2023
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/vision_models_multimodal
core_operator: "通过条件扩散模型生成多种可能的未来运动，并利用统计聚合（尤其是最小重建误差）捕捉生成运动与真实未来运动的贴近度：正常条件下生成的运动虽多样但偏向真实未来，异常条件下则缺乏这种贴近度。"
primary_logic: "正常行为条件生成的多模态未来运动会在真实未来附近聚集，而异常条件下生成的运动尽管同样多样，却偏离真实未来；利用最小生成误差能够有效区分正常与异常，突出了多模态生成在异常检测中的关键作用。"
claims:
- "MoCoDAD 在 UBnormal、HR-UBnormal、HR-STC、HR-Avenue 四个基准上均取得最优 AUC，相对此前最佳方法分别提升 5.1%、4.4%、0.5%、0.8%。"
- "采用 AE-embedding 条件化策略（自编码器嵌入）显著优于输入拼接和端到端嵌入，在 UBnormal 和 HR-UBnormal 上分别达到 68.3 和 68.4 AUC。"
- "对多次生成结果取最小平滑损失作为异常分数效果最佳，且 AUC 随生成数量增加而提升（饱和于 m≈50）。"
- "缺少过去动作条件时，性能降至接近随机水平（AUC 54.1），验证了运动条件化对异常检测的必要性。"
---

# Multimodal Motion Conditioned Diffusion Model for Skeleton-based Video Anomaly Detection

> [!tip] 核心洞察
> 正常行为条件生成的多模态未来运动会在真实未来附近聚集，而异常条件下生成的运动尽管同样多样，却偏离真实未来；利用最小生成误差能够有效区分正常与异常，突出了多模态生成在异常检测中的关键作用。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 基于骨骼的视频异常检测的多模态运动条件扩散模型 |
| 英文题名 | Multimodal Motion Conditioned Diffusion Model for Skeleton-based Video Anomaly Detection |
| 会议/期刊 | ICCV 2023 |
| Links | [paper](https://arxiv.org/abs/2307.07205); [GitHub](https://github.com/aleflabo/MoCoDAD) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal |
| Method | MoCoDAD |
| Dataset | UBnormal, HR-UBnormal, HR-STC, HR-Avenue |

> [!tip] 效果简介
> - UBnormal 上，AUC-ROC 为 68.3，对比 65.0 (COSKAD)，变化 +3.3。
> - HR-UBnormal 上，AUC-ROC 为 68.4，对比 65.5 (COSKAD)，变化 +2.9。
> - HR-STC 上，AUC-ROC 为 77.6，对比 77.1 (COSKAD)，变化 +0.5。

## 概述

### 问题瓶颈

基于骨骼的视频异常检测（VAD）通常采用单分类（OCC）范式——模型仅在正常数据上训练，期望对未见异常产生高重建误差。然而，现有OCC方法（如基于RNN、GCN或VAE的确定性预测模型）将正常行为映射到有限的潜在空间，**无法建模正常行为固有的多模态性**：同一动作存在多种正常执行方式（如走路的速度、步幅差异），这些多样但正常的变体容易被误判为异常。核心瓶颈在于，单一预测输出无法区分“偏离单一原型”与“真正异常”。

### 核心思路：MoCoDAD

**MoCoDAD**（Multimodal Motion Conditioned Diffusion Model for Skeleton-based Video Anomaly Detection）首次将条件扩散概率模型引入骨骼VAD，通过生成多种可能的未来运动来捕捉正常行为的多模态分布。其核心洞察是：

- **正常条件下**：以过去骨骼帧为条件生成的多种未来运动，虽然多样，但会在真实未来运动附近聚集——真实未来落入生成分布的主模态内。
- **异常条件下**：生成的运动同样具有多模态性，但真实未来运动偏离生成分布的主模态，位于分布的尾部。

因此，异常检测的关键不在于生成多样性本身，而在于**生成运动与真实未来运动的贴近度**。MoCoDAD通过对多次生成结果取最小重建误差作为异常分数，有效区分正常与异常。

### 方法定位

MoCoDAD属于**基于重建的OCC方法**，在方法谱系中占据独特位置：

- **预测模型**：从确定性单次预测（如GRU、GCN、VAE）升级为条件扩散概率模型，生成多种可能的未来运动。
- **条件化策略**：采用AE-embedding方案——利用辅助重建损失训练自编码器，将其潜在嵌入与扩散时间步嵌入融合后注入U-Net各层，显著优于简单的输入拼接或端到端嵌入。
- **异常评分**：从单次预测误差升级为统计聚合m次生成的最小平滑损失，辅以帧级对数归一化得分。

在知识库定位上，MoCoDAD与**COSKAD**（将正常嵌入约束到公共中心）、**GEPC**（ST-GCN编码后聚类）、**MPED-RNN**（双分支RNN重建与预测）等骨架OCC方法同属无监督异常检测分支，但通过扩散模型的多模态生成能力，在建模正常行为分布方面具有本质优势。

### 主要结果

在四个基准数据集上，MoCoDAD均取得最优AUC-ROC：

| 数据集 | MoCoDAD AUC | 此前最佳 (COSKAD) | 提升 |
|--------|-------------|-------------------|------|
| UBnormal | 68.3 | 65.0 | +3.3 |
| HR-UBnormal | 68.4 | 65.5 | +2.9 |
| HR-STC | 77.6 | 77.1 | +0.5 |
| HR-Avenue | 89.0 | 87.8 | +1.2 |

关键消融发现：移除过去动作条件后AUC降至54.1（接近随机水平），验证了运动条件化对检测的必要性；采用最小聚合且生成数量m>50时性能趋于饱和；多样性指标rF完全无法区分正常与异常（性能低于随机水平），进一步证实异常检测的核心在于贴近度而非多样性本身。

## 背景与动机

基于骨骼的视频异常检测（Skeleton-based VAD）旨在仅利用人体关节点坐标序列识别偏离正常模式的行为，因其对光照、背景变化的鲁棒性及隐私保护优势而受到广泛关注。该任务的主流范式是单分类（One-Class Classification, OCC）学习：仅使用正常样本训练模型，在推理时将偏离正常分布的样本判定为异常。

### 现有方法的瓶颈：正常行为多模态性的建模缺失

现有 OCC 骨架异常检测方法，无论是基于重建的 **Conv-AE**（Hasan et al., CVPR 2016）、**MPED-RNN**（Morais et al., CVPR 2019），还是基于预测的 **Pred**（Liu et al., CVPR 2018）、**PoseCVAE**（Rodrigues et al., ICPR 2021），均隐含一个共同假设——正常行为可以被压缩到某个有限的潜在流形或确定性映射中。然而，这一假设忽略了正常行为固有的**多模态性**（multimodality）：同一动作（如“挥手”）存在多种同样正常的执行方式（不同幅度、速度、风格）。当模型只能输出单一确定性预测或受限的潜在表示时，多样但正常的变体容易被误判为异常，造成高误报率。

近期工作如 **COSKAD**（Flaborea et al., arXiv 2023）尝试将正常嵌入约束到公共中心，**GEPC**（Markovitz et al., CVPR 2020）采用聚类方式组织正常模式，但这些方法本质上仍在有限的表示空间中建模正常性，未能显式捕捉正常行为的完整分布。

### 核心动机：以多模态生成捕捉正常性的开放集本质

异常检测的根本挑战在于异常的开放集特性——异常类型在训练时完全未知，任何偏离正常分布的样本都可能是异常。如果模型能够生成给定过去动作条件下的**多种可能的正常未来运动**，那么正常样本的真实未来应当落在生成分布的某个主模态内，而异常样本的真实未来则会偏离所有生成模态。这一直觉构成了 MoCoDAD 的核心动机：**利用条件扩散概率模型的多模态生成能力，通过统计聚合生成运动与真实未来运动的贴近度来区分正常与异常**。

扩散模型（Diffusion Probabilistic Models）在图像和运动生成领域已展现出强大的多模态分布建模能力，但在视频异常检测领域尚未被探索。MoCoDAD 首次将扩散模型引入骨架 VAD，通过在过去运动条件下生成多样化的未来运动候选，并取最小重建误差作为异常分数，有效缓解了正常行为多模态性导致的误检问题。

## 核心创新

MoCoDAD 的核心创新在于将**条件扩散概率模型**引入基于骨骼的视频异常检测（VAD），从根本上改变了传统单分类（OCC）方法对正常行为的建模方式。其关键设计体现在以下三个“changed slots”上。

### 从确定性预测到多模态条件生成

现有骨架 OCC 方法——无论是基于重建的 **Conv-AE**（CVPR 2016）、**MPED-RNN**（CVPR 2019），还是基于预测的 **PoseCVAE**（ICPR 2021）、**BiPOCO**（arXiv 2022）——均依赖确定性单次预测或潜在空间距离来判定异常。这类方法隐含假设正常行为可被映射到有限的潜在流形上，然而真实场景中同一动作存在多种正常执行方式（多模态性），确定性模型容易将偏离训练分布的多样但正常行为误判为异常。

MoCoDAD 将预测模型替换为**条件扩散概率模型**（Section 3.1）。训练时，前向扩散过程向未来骨骼序列 $X^{k+1:N}$ 的关节坐标添加随机平移噪声，逐步破坏其结构；反向扩散过程则学习以过去 $k$ 帧的编码 $h$ 为条件，估计并去除噪声。推理时从纯噪声出发，经 $T$ 步迭代去噪生成多种可能的未来运动轨迹。这一设计使得模型能够显式捕捉正常行为的多模态分布：正常条件下生成的多样未来运动会在真实未来附近聚集，而异常条件下尽管生成同样多样，却偏离真实未来（Figure 1, Figure 5）。

### AE-embedding 条件化策略

如何将过去运动信息注入扩散模型是性能的关键。MoCoDAD 对比了三种条件化方案（Figure 3, Table 3）：
- **输入拼接（Input concatenation）**：直接将过去帧与噪声未来帧拼接输入 U-Net，AUC 仅 59.3（UBnormal）；
- **端到端嵌入（E2E-embedding）**：通过可学习编码器提取条件向量，但缺乏显式监督，AUC 仅 58.4；
- **AE-embedding**（MoCoDAD 采用）：编码器 $E$ 将过去 $k$ 帧映射为潜在向量 $h$，并耦合对称解码器 $D$ 以辅助重构损失 $\mathcal{L}_{rec} = \| D(E(X^{1:k})) - X^{1:k} \|_2^2$ 强化表示。$h$ 与扩散时间步嵌入 $\tau_\theta(t)$ 融合后注入 U-Net 各层。

AE-embedding 在 UBnormal 和 HR-UBnormal 上分别取得 68.3 和 68.4 AUC，显著优于其他两种方案（Table 3）。其优势在于：辅助重构损失迫使编码器保留过去动作的结构信息，为条件生成提供了更具判别力的引导信号，同时避免了端到端方案中条件信号随扩散损失退化的问题。

### 统计聚合的异常评分机制

传统方法使用单次预测误差或潜在距离作为异常分数，无法利用多模态生成的优势。MoCoDAD 提出**多模态统计聚合**策略（Section 3.1, Algorithm 2）：对每个测试样本生成 $m$ 条候选未来轨迹，计算各自与真实未来的平滑损失 $\mathcal{L}_{smooth}$，取**最小值**作为个体异常分数，再在帧/多演员层面进行对数归一化聚合。

关键发现是：**最小聚合**效果最佳，且 AUC 随生成数量 $m$ 增加而提升，在 $m \approx 50$ 时趋于饱和（Figure 4 right）。这表明正常条件下，多模态生成中至少有一条轨迹会贴近真实未来（最小误差小），而异常条件下即使生成多样，也难以产生贴近真实未来的轨迹（最小误差仍大）。相反，多样性指标 rF 完全无法区分正常与异常——因为两者均具有多模态性，rF 的检测性能低于随机水平（Figure 6）。

### 消融验证的关键支撑

消融实验进一步验证了上述创新的必要性：
- **移除过去动作条件**（仅噪声生成）使 AUC 降至 54.1，接近随机水平 50%（Table 7），证实条件化对有效检测至关重要；
- **扩散在原始关节空间**优于潜在空间（AUC 68.3 vs 54.4，Table 5），说明骨骼运动的精细空间结构在潜在压缩中丢失，直接建模关节位移对异常判别更为关键；
- **预测（Forecasting）代理任务**优于随机插补和中间帧插补（Table 4），验证了“过去→未来”的因果条件方向最有利于暴露异常。

## 整体框架

![[assets/figures/papers/paper_list_l42_Multimodal_Motion_Conditioned_Diffusion_Model_for_Skeleton_based_Video_A/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the proposed MoCoDAD. A sequence of N skeletal motions ( N = 6 in the example) is split into past (top-right X ^ { 1 : k } frames, k = 3 in the example) and future (top-left X ^ { k + 1 : N } frames). During training, the Forward Diffusion block adds noise to the future frames, shifting each joint by a random vector displacement of varying intensity (increasing with the diffusion timestep t). Then the Reverse Diffusion learns to estimate the noise. A key aspect of MoCoDAD is the conditioning, i.e. how to encode the past clean k frames and guide the synthesis of relevant futures*

MoCoDAD 的核心设计是将视频异常检测重新表述为一个**条件式未来运动生成与统计验证问题**。其 pipeline 由三个紧密耦合的模块构成，形成一个“编码—生成—评估”的闭环。

### 输入输出流

给定一段包含 $N$ 帧的骨骼序列，模型将其切分为**过去窗口** $X^{1:k}$（前 $k$ 帧）与**未来窗口** $X^{k+1:N}$（后 $N-k$ 帧）。过去窗口作为条件信号输入，未来窗口在训练时作为监督目标、在推理时则被完全破坏为随机噪声。MoCoDAD 的核心任务是：**以过去 $k$ 帧的干净骨骼为条件，从噪声中重建出多样但合理的未来运动轨迹**。

推理阶段，模型对每个测试样本独立生成 $m$ 条候选未来轨迹，计算每条轨迹与真实未来运动的**平滑位移损失**（$\mathcal{L}_{smooth}$），再通过统计聚合（取 $m$ 次生成中的最小值）得到帧级异常分数。最终分数经对数归一化处理，放大分布离散帧的异常信号（见 Eq. (10)）。

### 三大模块关系

**1. 条件自编码器（Conditioning AE）**  
该模块以过去 $k$ 帧骨骼 $X^{1:k}$ 为输入，通过 STS-GCN 编码器 $E$ 将其压缩为潜在向量 $h$，并利用对称解码器 $D$ 辅助重建过去帧，以强化条件表示的判别力。辅助重建损失 $\mathcal{L}_{rec} = \| D(E(X^{1:k})) - X^{1:k} \|_2^2$ 与主损失联合优化，构成总目标 $\mathcal{L}_{tot} = \lambda_1 \mathcal{L}_{smooth} + \lambda_2 \mathcal{L}_{rec}$。潜在向量 $h$ 随后与扩散时间步嵌入 $\tau_\theta(t)$ 融合，注入到 U-Net 去噪网络的各层，作为生成过程的“运动上下文”引导。

**2. U-Net 去噪网络（Reverse Diffusion）**  
该模块是扩散过程的核心执行者。训练时，前向扩散过程向未来帧 $X^{k+1:N}$ 逐关节添加随机平移噪声，逐步破坏其坐标信息；U-Net 以当前噪声序列 $X_t$、时间步 $t$ 及条件信号 $(h + \tau_\theta(t))$ 为输入，预测所添加的位移噪声 $\varepsilon_\theta$，通过最小化位移估计损失 $\mathcal{L}_{disp} = \mathbb{E}[\| \varepsilon - \varepsilon_\theta(X_t, t, h) \|]$ 来学习去噪。推理时，网络从纯噪声 $X_T$ 出发，迭代执行反向扩散采样步骤（Eq. (3)），逐步去噪生成未来运动。U-Net 的骨干由空间-时间可分离图卷积层（STS-GCN）堆叠而成，以适配骨骼图的结构化时空特性。

**3. 多模态统计聚合（Statistical Aggregation）**  
这是 MoCoDAD 区分正常与异常的关键机制。由于扩散模型的随机采样特性，每次生成都会产生不同的未来轨迹。正常条件下，尽管生成的运动具有多模态性，但其分布会在真实未来附近形成主模式（见图 1 和图 5）；异常条件下，生成的运动虽然同样多样，却缺乏与真实未来的贴近度。因此，对 $m$ 次生成结果取**最小平滑损失**作为异常分数，能够有效捕捉这种“贴近度”差异。消融实验证实，最小聚合显著优于均值或分位数聚合，且 AUC 随 $m$ 增加而提升，在 $m \approx 50$ 时趋于饱和（见 Figure 4 右侧）。

### 关键设计决策

- **条件化策略**：在三种候选方案（输入拼接、端到端嵌入、自编码器嵌入）中，**AE-embedding 方案**表现最优（UBnormal AUC 68.3 vs. 输入拼接 59.3 vs. 端到端嵌入 58.4），验证了辅助重建损失对条件表示学习的强化作用（Table 3）。
- **代理任务选择**：采用**预测未来帧**（Forecasting）作为生成目标，显著优于随机帧插补和中间帧插补（Table 4），表明“从过去推断未来”的因果结构对异常检测至关重要。
- **扩散空间**：在**原始关节点空间**进行扩散操作，效果远优于在 VAE 潜在空间中扩散（AUC 68.3 vs. 54.4，Table 5）。潜在空间扩散在此任务中的失效原因仍是一个开放问题，可能与骨骼运动的低维流形特性及潜在变量建模的信息损失有关。

## 核心模块与公式推导

MoCoDAD 的核心由四个模块构成：**前向扩散过程**、**条件自编码器**、**U-Net 去噪网络** 和 **多模态统计聚合**。以下逐一阐述其机理与关键公式。

### 前向扩散过程

与标准 DDPM 在像素空间添加高斯噪声不同，MoCoDAD 在骨骼关节的**原始坐标空间**进行操作。前向过程 $q$ 向未来 $N-k$ 帧的关节坐标逐步添加**随机平移噪声**——即对每个关节施加一个随机位移向量，而非独立破坏每个坐标值。这一设计保持了骨骼结构的空间连续性，且消融实验证实原始空间扩散（AUC 68.3）远优于潜在空间扩散（AUC 54.4，Table 5），说明骨骼运动的内在几何约束在低维潜在变量中难以保留。

去噪网络 $\varepsilon_\theta$ 的训练目标是最小化位移估计损失：

$$\mathcal{L}_{disp} = \mathbb{E}_{t, X, \varepsilon} \big[ \| \varepsilon - \varepsilon_\theta(X_t, t, h) \| \big] \quad \text{(Eq. 1)}$$

其中 $X_t$ 为扩散步 $t$ 时的噪声未来序列，$h$ 为条件自编码器从过去 $k$ 帧提取的潜在嵌入，$\varepsilon$ 为真实添加的平移噪声。为提高训练稳定性，实际采用平滑损失 $\mathcal{L}_{smooth}$（Huber 型，Eq. 2），在 $|\mathcal{L}_{disp}|<1$ 时退化为平方损失，否则为线性损失。

推理时通过反向采样逐步去噪，从纯噪声 $X_T \sim \mathcal{N}(0,I)$ 出发，迭代生成未来姿态：

$$X_{t-1} = \frac{1}{\sqrt{\alpha_t}} \left( X_t - \frac{1-\alpha_t}{\sqrt{1-\bar{\alpha}_t}} \varepsilon_\theta(X_t, t, h) \right) + z \sqrt{\beta_t} \quad \text{(Eq. 3)}$$

其中 $\alpha_t$、$\bar{\alpha}_t$、$\beta_t$ 为标准扩散噪声调度参数，$z \sim \mathcal{N}(0,I)$ 为随机噪声。

### 条件自编码器（AE-embedding）

条件化策略是 MoCoDAD 的关键设计。论文对比了三种方案（Figure 3）：输入拼接（Input concatenation）、端到端嵌入（E2E-embedding）和自编码器嵌入（AE-embedding）。其中 **AE-embedding 显著最优**（Table 3：UBnormal 68.3 vs 59.3/58.4），其核心在于引入辅助重构损失来强化条件表示的判别力。

具体而言，编码器 $E$（基于 STS-GCN）将过去 $k$ 帧骨骼序列 $X^{1:k}$ 映射为潜在向量 $h$，对称解码器 $D$ 则从 $h$ 重构 $X^{1:k}$，辅助损失为：

$$\mathcal{L}_{rec} = \| D(E(X^{1:k})) - X^{1:k} \|_2^2 \quad \text{(Eq. 4)}$$

该重构任务迫使 $h$ 保留过去运动的细粒度时空结构，而非仅学习一个松散的条件信号。随后 $h$ 与扩散时间步嵌入 $\tau_\theta(t)$ 融合，注入 U-Net 各层引导去噪过程。

总训练目标联合优化去噪与重构：

$$\mathcal{L}_{tot} = \lambda_1 \mathcal{L}_{smooth} + \lambda_2 \mathcal{L}_{rec} \quad \text{(Eq. 5)}$$

### U-Net 去噪网络

去噪骨干采用 **STS-GCN 层构成的 U-Net 架构**（Section 3.3）。STS-GCN 将空间图卷积与时间卷积解耦，先沿骨骼图的空间边聚合关节特征，再沿时间轴卷积，从而高效捕获骨架序列的时空依赖。U-Net 的编码器-解码器结构通过跳跃连接保留细粒度空间信息，条件信号 $(h + \tau_\theta(t))$ 在每层注入，引导网络预测与过去运动一致的未来姿态。

### 多模态统计聚合

推理时，MoCoDAD 从同一过去条件出发，通过不同随机噪声种子生成 $m$ 条候选未来轨迹 $\{\hat{X}^{(i)}\}_{i=1}^m$。对每条轨迹计算其与真实未来 $X^{k+1:N}$ 的平滑损失，取**最小值**作为该样本的异常分数：

$$AS = \min_{i \in \{1,\dots,m\}} \mathcal{L}_{smooth}(\hat{X}^{(i)}, X^{k+1:N})$$

取最小值而非均值的直觉在于（Section 3.1, Figure 4）：正常条件下，多模态生成虽多样，但至少有一条轨迹贴近真实未来（落入分布主模态内），最小误差因此较小；异常条件下，真实未来偏离所有生成模态，即便最优轨迹的误差也较大。消融证实，最小聚合效果最优，且 AUC 随 $m$ 增加而提升，在 $m \approx 50$ 时趋于饱和（Figure 4 right）。

对于多演员场景，帧级异常得分进一步通过均值与极值范围的对数归一化增强：

$$\mathrm{AS}[f_1:f_N] = \operatorname{mean}(S) + \log\frac{1 + \max(S)}{1 + \min(S)} \quad \text{(Eq. 10, Appendix C)}$$

其中 $S$ 为窗口内各演员的个体得分。该公式在均值基础上叠加极值范围的对数项，放大帧内得分分布较散的异常窗口，抑制所有演员得分均匀偏高的正常波动。

### 关键设计选择

- **代理任务**：预测未来（Forecasting）优于随机插补和中间帧插补（Table 4），因为异常行为的时序不连续性在未来帧中最显著。
- **扩散空间**：原始关节点空间（AUC 68.3）远优于 VAE 潜在空间（AUC 54.4），后者几乎退化为随机水平（Table 5），提示骨骼运动的低维潜在建模在此任务中失效。
- **多样性指标失效**：尽管异常生成理论上可能更离散，但多样性比率 $rF$ 作为异常分数时性能低于随机水平（Figure 6），原因是正常与异常条件均产生多模态生成，仅凭生成多样性无法区分。

## 实验与分析

### 核心瓶颈与设计动机

现有基于单分类（OCC）的骨骼异常检测方法（如 **MPED-RNN** (Morais et al., CVPR 2019)、**GEPC** (Markovitz et al., CVPR 2020)、**COSKAD** (Flaborea et al., arXiv 2023)）将正常行为映射到有限的潜在空间，无法建模正常行为固有的**多模态性**——即同一动作存在多种正常执行方式。这导致对多样但正常的行为产生误检。MoCoDAD 的核心假设是：**以正常过去运动为条件生成的未来运动虽具多模态性，但会在真实未来附近聚集；而异常条件下生成的运动则偏离真实未来**（Figure 1）。通过统计聚合多次生成的最小重建误差，可有效区分正常与异常。

### 主要结果

Table 1 展示了 MoCoDAD 在四个基准上的 AUC-ROC 性能。MoCoDAD 在全部数据集上均取得最优结果：


![[assets/figures/papers/paper_list_l42_Multimodal_Motion_Conditioned_Diffusion_Model_for_Skeleton_based_Video_A/figures/004_Table_1.jpg]]
*Table 1: Comparison of MoCoDAD against SoA in terms of AUC on the three Human-Related datasets (i.e., HR-STC, HR-Avenue and HR-UBnormal) and UBnormal. OCC skeleton-based techniques are marked with a ∗*

- **UBnormal**: MoCoDAD 达到 **68.3** AUC，较此前最佳的 COSKAD（65.0）提升 **+3.3**，相对提升约 5.1%。
- **HR-UBnormal**: 达到 **68.4** AUC，优于 COSKAD（65.5）**+2.9**。
- **HR-STC**: 达到 **77.6** AUC，略优于 COSKAD（77.1）**+0.5**。
- **HR-Avenue**: 达到 **89.0** AUC，优于 COSKAD（87.8）**+1.2**。

值得注意的是，HR-STC 和 HR-Avenue 上所有方法性能已较高，提升空间有限；而 UBnormal 和 HR-UBnormal 作为更具挑战性的数据集，MoCoDAD 的优势更为显著。

Table 2 将 MoCoDAD 与监督/弱监督方法进行了补充比较。MoCoDAD（68.3）在仅使用正常数据训练的条件下，优于弱监督方法 AED-SSMTL（59.3），并与全监督的 TimeSformer（68.5）竞争力相当。此比较旨在展示 OCC 方法的参数效率，并非公平的精度竞赛。


![[assets/figures/papers/paper_list_l42_Multimodal_Motion_Conditioned_Diffusion_Model_for_Skeleton_based_Video_A/figures/005_Table_2.jpg]]
*Table 2: Comparison of MoCoDAD against supervised (†) and weakly supervised (‡) methods introduced in [1] in terms of AUC on the UBnormal dataset*

### 多模态生成与异常评分机制

Figure 4（左）展示了在 HR-UBnormal 测试集上，正常与异常条件分别生成 50 条未来运动的**重建误差直方图**。正常条件下，误差集中在低值区域；异常条件下，误差分布更分散且整体偏高。这验证了核心假设：正常条件生成的运动更贴近真实未来。


![[assets/figures/papers/paper_list_l42_Multimodal_Motion_Conditioned_Diffusion_Model_for_Skeleton_based_Video_A/figures/006_Figure_4.jpg]]
*Figure 4: (left) Histograms of the reconstruction errors for 50 synthesized future motions, computed on the HR-UBnormal test set, for the case of conditioning on normal and abnormal past motions. (right) Correlation between the AUC scores and the number of generations, with each curve corresponding to a different aggregation statistic*

Figure 4（右）分析了**生成数量 m 与 AUC 的关系**。关键发现：
- 采用**最小值聚合**（minimum）时，AUC 随 m 增加而提升，在 **m ≈ 50** 时趋于饱和。
- 采用均值聚合时，AUC 随 m 增加反而下降。这是因为均值聚合会稀释异常样本中少数贴近真实未来的生成，降低区分度。
- 分位数 Q < 0.5 的聚合与 AUC 正相关，而 Q > 0.5 的聚合呈负相关。

这揭示了统计聚合策略的选择至关重要：**取最小重建误差**最能捕捉“生成分布是否覆盖真实未来”这一判别信号。

### 多样性指标的失败

Figure 5（右）和 Figure 6 揭示了**多样性指标 rF 完全无法作为异常分数**。尽管直觉上异常条件可能产生更离散的生成，但实验表明：

![[assets/figures/papers/paper_list_l42_Multimodal_Motion_Conditioned_Diffusion_Model_for_Skeleton_based_Video_A/figures/013_Figure_6.jpg]]
*Figure 6: Anomaly detection performance trend when assuming a diversity metric as the anomaly score. It is worth noting that the r F metric yields results that are below the chance level*

- 正常与异常条件下生成的 rF 值**高度可比**，因为扩散模型在两种条件下均产生多模态输出（Figure 5 右）。
- 以 rF 作为异常分数时，检测性能**低于随机水平**（AUC < 50%，Figure 6）。

这一失败模式说明：**多模态性本身并非异常的标志，关键在于生成分布与真实未来的贴近度**。仅凭生成多样性无法区分正常与异常，必须依赖与真实未来的对比。

### 消融实验

#### 条件化策略

Table 3 比较了三种条件化信息集成方式：

![[assets/figures/papers/paper_list_l42_Multimodal_Motion_Conditioned_Diffusion_Model_for_Skeleton_based_Video_A/figures/009_Table_3.jpg]]
*Table 3: Ablation study on the different methods for integrating conditioning information into the model*

- **Input concatenation**: 直接将过去帧与噪声未来帧拼接输入 U-Net，AUC 仅 **59.3**。
- **E2E-embedding**: 端到端学习条件嵌入，AUC 为 **58.4**。
- **AE-embedding（MoCoDAD）**: 通过辅助重构损失训练自编码器，将其潜在嵌入与扩散时间步嵌入融合注入 U-Net 各层，AUC 达 **68.3**。

AE-embedding 的优势在于：辅助重构损失强制编码器保留过去运动的有效表示，避免了端到端训练中条件信号被扩散损失主导而退化的问题。

#### 代理任务选择

Table 4 比较了不同的条件化任务：

![[assets/figures/papers/paper_list_l42_Multimodal_Motion_Conditioned_Diffusion_Model_for_Skeleton_based_Video_A/figures/011_Table_4.jpg]]
*Table 4: Ablation study on the type of conditioning information to feed into the model to generate the missing frame*

- **Forecasting**（预测未来，即 MoCoDAD）: AUC 68.3 / 68.4。
- **Random imputation**（随机插补）: 性能显著下降。
- **In-between imputation**（中间帧插补）: 同样劣于预测任务。

预测未来作为代理任务更有效，因为异常行为往往表现为对未来预期的违背，这一任务天然契合异常检测的目标。

#### 扩散空间选择

Table 5 比较了在**原始关节点空间**与**潜在空间**中执行扩散的性能：

![[assets/figures/papers/paper_list_l42_Multimodal_Motion_Conditioned_Diffusion_Model_for_Skeleton_based_Video_A/figures/010_Table_5.jpg]]
*Table 5: AUC-ROC performance of diffusion on latent vs original space*

- **原始空间（MoCoDAD）**: AUC 68.3 / 68.4。
- **潜在空间（Latent-MoCoDAD）**: AUC 仅 **54.4**，接近随机水平。

这一结果出人意料：通常潜在空间扩散在图像生成中表现优异，但在骨骼 VAD 中完全失效。可能的原因包括：VAE 的潜在压缩丢失了对异常检测至关重要的细粒度关节位移信息；潜在空间中的重建误差无法准确反映原始空间中的运动偏差。这一现象值得进一步研究。

#### 运动条件化的必要性

Table 7 的消融显示：**移除过去动作条件**（仅从噪声生成，无运动条件）使 AUC 降至 **54.1**（接近随机 50%）。这直接验证了运动条件化对异常检测的不可或缺性——模型必须依赖过去运动信息才能生成有意义的未来预测，进而判断异常。


![[assets/figures/papers/paper_list_l42_Multimodal_Motion_Conditioned_Diffusion_Model_for_Skeleton_based_Video_A/figures/014_Table_7.jpg]]
*Table 7: Impact of different noise distributions and sampling strategies on performance in terms of AUC-ROC. MoCo refers to Motion Condition; T represents the diffusion step at which samples are completely corrupted; γ represents the step up to which samples are corrupted during inference. The last row illustrates our proposed method, MoCoDAD*

#### 噪声类型与采样策略

Table 7 还比较了不同噪声分布和采样策略：
- **高斯噪声**优于 Simplex 噪声（Figure 7 展示了两者的加噪效果差异）。
- 在推理时从完全损坏（T = 1000）逐步去噪，优于从部分损坏（γ < T）开始采样。完全去噪过程使模型能更充分地利用条件信息引导生成。

### 方法谱系与知识库定位

MoCoDAD 位于**基于重建/预测的骨骼 OCC 异常检测**脉络中，但其核心创新在于将确定性单次预测替换为**条件扩散概率模型的多模态生成**。相较于：

- 确定性预测方法（**Pred** (Liu et al., CVPR 2018)、**Multi-timescale Prediction** (Rodrigues et al., WACV 2020)）仅生成单一未来，无法建模正常行为的多模态性。
- VAE 方法（**PoseCVAE** (Jain et al., ICPR 2021)、**BiPOCO** (Flaborea et al., arXiv 2022)）虽能生成多样本，但其潜在空间约束限制了生成质量。
- 基于聚类的 OCC 方法（**GEPC**、**COSKAD**）将正常行为压缩到紧凑表示，本质上与多模态建模相悖。

MoCoDAD 的扩散框架通过迭代去噪生成高质量多样本，配合最小误差聚合，在保持多模态性的同时捕捉与真实未来的贴近度，形成了新的技术路径。

### 补充图表

![[assets/figures/papers/paper_list_l42_Multimodal_Motion_Conditioned_Diffusion_Model_for_Skeleton_based_Video_A/figures/008_Figure.jpg]]

![[assets/figures/papers/paper_list_l42_Multimodal_Motion_Conditioned_Diffusion_Model_for_Skeleton_based_Video_A/figures/012_Table.jpg]]

![[assets/figures/papers/paper_list_l42_Multimodal_Motion_Conditioned_Diffusion_Model_for_Skeleton_based_Video_A/figures/016_Table_8.jpg]]
*Table 8: Comparison of MoCoDAD against SoA in terms of AUC-ROC on the validation set of UBnormal. OCC skeleton-based techniques (∗) are directly comparable to MoCoDAD. Supervised (†) and weakly supervised (‡) methods are also reported, grayed-out since they leverage extra annotations*


## 方法谱系与知识库定位

### 骨架视频异常检测的方法谱系

MoCoDAD 处于基于骨骼的 one-class classification（OCC）视频异常检测（VAD）脉络中。该脉络的核心思路是仅用正常样本训练模型，通过建模正常行为的分布来识别偏离该分布的异常。现有方法可大致分为两类：**基于重建**和**基于预测**。

基于重建的方法将正常样本编码到低维潜在空间后解码重建，假设异常样本无法被准确重建。代表性工作包括 **Conv-AE**（Hasan et al., CVPR 2016）、**STGCAE-LSTM**（Morais et al., Neurocomputing 2022）以及 **SSMTL++**（Georgescu et al., CVIU 2023）。基于预测的方法则利用过去帧预测未来帧，通过预测误差检测异常，如 **Pred**（Liu et al., CVPR 2018）、**Multi-timescale Prediction**（Rodrigues et al., WACV 2020）和 **PoseCVAE**（Jain et al., ICPR 2021）。

近年来，专门针对骨架输入的 OCC 方法涌现，它们通常采用图卷积网络（GCN）或 RNN 建模人体关节的时空关系。**MPED-RNN**（Morais et al., CVPR 2019）采用双分支 RNN 同时进行重建和预测；**GEPC**（Markovitz et al., CVPR 2020）使用 ST-GCN 编码后聚类；**Normal Graph**（Luo et al., Neurocomputing 2021）直接利用 ST-GCN 编码骨架序列；**COSKAD**（Flaborea et al., arXiv 2023）则将正常嵌入约束到公共中心。这些方法在 MoCoDAD 提出前代表了该方向的最高水平。

### MoCoDAD 的方法定位与核心创新

MoCoDAD 在方法谱系中的独特位置在于它是**首个将扩散概率模型引入视频异常检测的工作**，并且专门针对骨架模态设计了条件扩散框架。其核心创新体现在三个维度：

1. **从确定性预测到多模态生成**：现有方法（无论是重建还是预测）本质上都是确定性的——给定过去输入，模型输出单一的未来预测或重建。MoCoDAD 通过条件扩散模型生成多种可能的未来运动，首次显式建模了正常行为固有的多模态性（同一动作的多种正常执行方式）。这一转变直接回应了现有 OCC 方法的根本瓶颈：将正常行为映射到有限的潜在空间，无法容纳正常行为的多样性，导致对多样但正常的行为产生误检。

2. **条件化策略的系统设计**：MoCoDAD 探索了三种将过去运动信息注入扩散过程的方式——输入拼接（Input concatenation）、端到端嵌入（E2E-embedding）和自编码器嵌入（AE-embedding）。消融实验（Table 3）表明，AE-embedding 在 UBnormal 和 HR-UBnormal 上分别达到 68.3 和 68.4 AUC，显著优于输入拼接（59.3）和端到端嵌入（58.4）。AE-embedding 通过辅助重构损失训练编码器，使条件嵌入更具判别力，这一设计选择对最终性能至关重要。

3. **统计聚合驱动的异常评分**：不同于单次预测误差，MoCoDAD 生成 m 条候选未来轨迹，取最小平滑损失（$\mathcal{L}_{smooth}$）作为异常分数。实验（Figure 4 right）表明 AUC 随生成数量 m 增加而提升，在使用最小聚合且 m≈50 时趋于饱和。这一策略的有效性源于核心洞察：正常条件下生成的多模态未来运动会在真实未来附近聚集（最小误差小），而异常条件下生成的运动尽管同样多样，却偏离真实未来（最小误差仍大）。

### 与同期/后续工作的关系

MoCoDAD 在 UBnormal 基准上与监督/弱监督方法的比较（Table 2）展示了其参数效率优势：作为 OCC 方法（仅需正常样本训练），其 AUC 68.3 超过了弱监督方法 AED-SSMTL（59.3），并与全监督方法 TimeSformer（68.5）接近。这一比较并非公平的精度竞赛（训练设置不同），而是凸显了扩散生成范式在标签稀缺场景下的实用价值。

在扩散模型应用于视频理解的大背景下，MoCoDAD 与视频扩散模型（如 Video Diffusion Models）共享条件生成的思想，但将其重新定位为异常检测的代理任务——通过“预测未来”而非“生成内容”来构建检测信号。该工作还启发了后续将扩散模型用于其他安全关键场景（如工业检测、监控）的研究方向。

### 适用边界与局限

1. **模态依赖**：MoCoDAD 假设输入为准确的骨架序列。在真实场景中，骨架估计器（如 OpenPose、HRNet）的输出可能包含噪声、遮挡或误检，方法对这些低质量输入的鲁棒性尚未验证。当骨架提取失败时，整个异常检测流水线将失效。

2. **扩散空间选择**：消融实验（Table 5）显示，在原始关节点空间进行扩散（AUC 68.3）远优于在潜在空间（VAE 隐变量，AUC 54.4）。这一现象的原因未深入分析——潜在变量建模在此任务中失效的本质仍需探究。可能的解释是，VAE 的潜在空间压缩丢失了对异常检测至关重要的关节级细节。

3. **多样性指标的失效**：一个反直觉的发现是，多样性指标 rF 完全无法作为异常分数（Figure 6），其检测性能低于随机水平。尽管直观上异常生成可能更离散，但实验表明正常和异常条件下的生成都具有多模态性，rF 无法区分两者。这一现象的统计根源值得进一步研究。

4. **计算开销**：为获得最佳性能需要生成约 50 条候选轨迹，推理时的多次采样带来了额外的计算成本，可能限制在实时场景中的部署。

### 开放问题

- 扩散过程在原始骨骼空间优于潜在空间的原因是什么？是否存在既能保留关节级细节又能降低计算量的潜在表示？
- 为何多样性指标 rF 完全无法区分正常与异常生成？是否存在其他能捕捉“生成偏离真实”这一信号的统计量？
- 该方法对低质量骨架输入的鲁棒性如何？能否与骨架估计器联合优化或引入不确定性建模？
- 条件扩散框架能否扩展到多模态输入（RGB + 骨架）或多演员交互场景？当前帧级聚合策略（Eq. 10）在多演员场景中的扩展性有待验证。

## 原文 PDF

![[paperPDFs/ICCV_2023/Multimodal_Motion_Conditioned_Diffusion_Model_for_Skeleton_based_Video_Anomaly_Detection.pdf]]
