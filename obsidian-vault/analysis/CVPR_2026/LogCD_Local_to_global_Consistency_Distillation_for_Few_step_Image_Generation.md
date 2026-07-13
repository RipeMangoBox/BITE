---
title: "LogCD: Local-to-global Consistency Distillation for Few-step Image Generation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/LogCD_Local_to_global_Consistency_Distillation_for_Few_step_Image_Generation.pdf
project_link: null
code_link: "https://github.com/blackforest-labs/flux"
huggingface_link: "https://huggingface.co/blackforest-labs/FLUX.1-dev"
aliases:
- LGCDL
- LogCD
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 采用分治策略：首先将时间轴划分区间进行局部一致性蒸馏（Local CD），再进行全局一致性蒸馏（Global CD）以跨区间对齐，并利用Latent LPIPS保持感知一致性、图像免采样策略消除对训练数据的依赖。
primary_logic: 将复杂全轨迹一致性映射分解为局部子问题，在局部阶段固定终点（里程碑）加速收敛，在全局阶段采用多步ODE求解器和GAN/DMD损失提升全局连贯性与视觉质量，整体仅需70 A100 GPU小时。
claims:
- 在仅70 A100 GPU小时的训练下，3步LogCM在MSCOCO上达到33.5 CLIP Score，超过多数4步SOTA方法，并与25步teacher相当。
- 全局一致性蒸馏大幅提升局部蒸馏的图文对齐（IR）和CLIP Score，GAN和DMD损失均有显著增益。
- MSCOCO-2017 5K 上 CLIP Score = 33.5 (LogCM 3-step)
- MSCOCO-2017 5K 上 Image Reward = 0.95 (LogCM 3-step)
---

# LogCD: Local-to-global Consistency Distillation for Few-step Image Generation

> [!tip] 核心洞察
> 将复杂全轨迹一致性映射分解为局部子问题，在局部阶段固定终点（里程碑）加速收敛，在全局阶段采用多步ODE求解器和GAN/DMD损失提升全局连贯性与视觉质量，整体仅需70 A100 GPU小时。

| 字段 | 内容 |
|------|------|
| 中文题名 | LogCD：用于少步图像生成的局部到全局一致性蒸馏 |
| 英文题名 | LogCD: Local-to-global Consistency Distillation for Few-step Image Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Xie_LogCD_Local-to-global_Consistency_Distillation_for_Few-step_Image_Generation_CVPR_2026_paper.html) · [Code](https://github.com/blackforest-labs/flux) · [HuggingFace](https://huggingface.co/blackforest-labs/FLUX.1-dev) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Local-to-global Consistency Distillation (LogCD) |
| Dataset | MSCOCO-2017 5K, MJHQ-5K |

> [!tip] 效果简介
> - MSCOCO-2017 5K 上，CLIP Score 33.5 (LogCM 3-step) vs 33.5 (SDXL teacher 25-step, est.) (comparable)；Image Reward 0.95 (LogCM 3-step) vs 0.90 (SDXL teacher 25-step, est.) (+0.05)；CLIP Score 32.6 (LogCM 4-step on FLUX.1-dev) vs 32.6 (FLUX.1-dev teacher 25-step, est.) (comparable)。
> - MJHQ-5K 上，CLIP Score 35.2 (LogCM 3-step) vs - (-)。

## 概要

扩散模型与基于流的生成模型在文本到图像合成中取得了显著成功，但其迭代采样过程导致推理速度缓慢，限制了实际部署。现有加速方法在减少采样步数的同时，往往面临图文对齐能力下降、训练资源需求过大或性能严重退化等问题。特别是在2–4步的极低步数区间，如何在保持生成质量与图文一致性的前提下实现高效蒸馏，仍是一个未充分解决的瓶颈。

针对上述挑战，本文提出**LogCD（Local-to-global Consistency Distillation）**，一种局部到全局的一致性蒸馏框架。其核心洞察在于：将复杂的全轨迹一致性映射分解为局部子问题——先在划分的时间区间内进行局部一致性蒸馏以加速收敛，再通过全局一致性蒸馏跨区间对齐，从而在极低采样步数下恢复全局连贯性。方法整体仅需**70 A100 GPU小时**的训练开销，且完全无需真实图文配对数据，通过图像免采样策略消除了对训练数据集的依赖。

在SDXL架构上，3步采样的**LogCM**在MSCOCO-2017 5K上达到**33.5 CLIP Score**，与25步教师模型相当，并超越多数4步SOTA方法；在MJHQ-5K上达到35.2 CLIP Score。在FLUX.1-dev上，4步LogCM同样取得了与25步教师模型可比的性能。消融实验表明，局部一致性蒸馏奠定了性能基础，而全局一致性蒸馏中的GAN损失和DMD损失分别带来了显著的图文对齐与视觉质量增益。



扩散模型已成为文本到图像生成的主流范式，但其迭代采样机制导致推理速度缓慢。以SDXL为例，单张1024×1024图像生成需25步去噪，在A100 GPU上耗时约2.2秒，难以满足实时交互需求。为此，研究者提出多种加速策略：**渐进蒸馏**（如SDXL-Lightning）将多步教师逐步压缩至少步学生；**对抗蒸馏**（如Flash SDXL）引入GAN损失提升单步质量；**一致性蒸馏**则利用ODE轨迹自洽性，将任意噪声点直接映射到数据端点。

然而，现有一致性蒸馏方法面临一个核心瓶颈：**在保持图文对齐的同时大幅减少采样步数极为困难**。单阶段全局一致性蒸馏（如**LCM**）试图在完整时间轴上强制执行自洽性，但长跳步导致离散化误差累积，训练不稳定且收敛缓慢。分段一致性方法（如**PCM**）将时间轴分块处理，虽缓解了跳步过大问题，却因缺乏跨区间约束而牺牲全局连贯性。多阶段轨迹方法（如**HyperSD**）引入随机终点时间步，却带来冗余训练目标，增加了收敛难度。这些方法的共同困境在于：**2-4步的高质量生成——一个兼具效率与质量的实用中间地带——尚未被充分探索**。

LogCD的动机正是填补这一空白。其核心洞察是：**将复杂的全轨迹一致性映射分解为局部子问题，在局部阶段固定终点（里程碑）以加速收敛，在全局阶段引入多步ODE求解器与GAN/DMD损失以恢复跨区间连贯性**。这一分治策略使得仅需70 A100 GPU小时的训练即可实现与25步教师模型相当的图文对齐质量，为少步生成提供了高效且可扩展的解决方案。



## 核心方法与创新机理

LogCD 的核心创新在于将一致性蒸馏这一复杂全轨迹映射问题，分解为**局部到全局**的分治策略，并通过三个关键设计实现高效、高质量的少步生成。

### 1. 两阶段局部到全局一致性蒸馏范式

现有的一致性蒸馏方法（如 **LCM**、**PCM**）通常采用单阶段全局一致性训练，试图一次性将整个去噪轨迹映射到数据分布。然而，这种全局映射在少步（2-4步）场景下难以同时保持图文对齐和视觉质量。LogCD 将这一过程拆解为两个阶段：

- **局部一致性蒸馏（Local CD）**：将完整时间轴 $[0, T]$ 划分为 $M$ 个子区间，在每个区间内独立执行一致性蒸馏。其核心操作是将区间内的任意噪声点映射到该区间的固定终点（里程碑），从而将复杂的全局映射分解为多个局部子问题，加速收敛。这一设计的关键在于**固定里程碑**策略——与 **CTM** 或 **HyperSD** 中随机选择终点时间步不同，LogCD 使用预定义的里程碑消除了冗余的训练目标。

- **全局一致性蒸馏（Global CD）**：在局部蒸馏的基础上，跨里程碑执行一致性对齐。Global CD 仅需在预定义的时间步（间隔为 $T/M$）之间建立一致性，而非覆盖整个轨迹。这一阶段引入了多步 ODE 求解器（$p$ 步）来减少离散化误差，并结合 GAN 损失和可选的 DMD 损失来提升全局连贯性与视觉质量。

这种分治范式的优势在于：局部阶段降低了单个子问题的难度，全局阶段则专注于跨区间的连贯性，二者协同使得仅需 **70 A100 GPU 小时**即可完成蒸馏。

### 2. 隐空间感知一致性损失（Latent LPIPS）

传统一致性蒸馏通常使用隐空间 MSE 作为损失函数，但 MSE 对感知差异不敏感，容易导致生成结果模糊或细节丢失。LogCD 提出在 **BAPPS 数据集**上训练一个专门的 Latent LPIPS（L-LPIPS）模型，直接在隐空间计算感知相似度。

L-LPIPS 的设计要点包括：
- 基于 VGG 网络，但将输入通道改为隐空间表示 $z_0$ 的通道数，并移除 3 个最大池化层以适应隐空间分辨率。
- 在局部 CD 和全局 CD 中分别替代 MSE 损失，形成 $\mathcal{L}_{LoCD}^{LLP}$ 和 $\mathcal{L}_{GoCD}^{LLP}$。

消融实验（Table 3）证实，用 L-LPIPS 替换 MSE 后，所有指标（CLIP Score、FID、Image Reward）均获得提升，验证了感知一致性在蒸馏过程中的关键作用。

### 3. 图像免采样训练策略

大多数蒸馏方法依赖图文配对数据集进行训练，这限制了其在实际应用中的灵活性。LogCD 在两个阶段均实现了**图像免采样**：

- **局部 CD**：使用教师模型从随机噪声生成的样本作为训练目标，无需真实图像。
- **全局 CD**：进一步采用学生模型自身合成的数据 $\hat{z}_0$，完全消除了对图文配对数据集的依赖。

这一设计不仅降低了数据需求，还使得蒸馏过程更加自洽——学生模型在全局阶段学习的是自身分布的一致性，而非外部数据分布的拟合。

### 4. 全局 CD 中的多目标联合优化

全局 CD 阶段的总损失函数为：

$$\mathcal{L}_{GoCD} = \mathcal{L}_{GoCD}^{MSE/LLP} + \lambda_1 \mathcal{L}_{GoCD}^{GAN} + \lambda_2 \mathcal{L}_{GoCD}^{DMD}$$

其中：
- **$\mathcal{L}_{GoCD}^{GAN}$**：基于教师 U-Net 构建的相对论 GAN 判别器，强制学生在不同里程碑处的输出分布一致。
- **$\mathcal{L}_{GoCD}^{DMD}$**（可选）：分布匹配蒸馏损失，通过预训练的真实和虚假分数模型最小化分布差异。

消融实验（Table 3）表明，GAN 损失在局部蒸馏基础上显著提升 CS 和 IR，DMD 损失则带来额外的全指标增益。这种多目标联合优化是 LogCD 在 3 步采样下达到与 25 步教师模型相当性能的关键因素之一。

### 5. 参数高效训练

所有蒸馏阶段仅训练秩为 64 的 **LoRA 适配器**，而非全量微调 UNet/DiT。这一设计大幅降低了训练资源需求（70 A100 GPU 小时），同时保持了模型质量，使得 LogCD 成为目前最高效的少步蒸馏方法之一。



LogCD 采用**分治蒸馏**策略，将复杂的全轨迹一致性映射分解为两个阶段：**局部一致性蒸馏（Local CD）** 与**全局一致性蒸馏（Global CD）**。整个框架的输入为预训练的扩散教师模型（如 SDXL 或 FLUX.1-dev），输出为支持 2–4 步采样的轻量学生模型，全程仅训练秩为 64 的 LoRA 适配器。

### 两阶段蒸馏流程

**第一阶段：局部一致性蒸馏。** 将扩散过程的时间轴 $[0, T]$ 均匀划分为 $M$ 个子区间，每个区间指定一个固定的终点时间步作为“里程碑”。在该区间内，学生模型学习将任意噪声隐变量映射到区间起点的里程碑隐变量。这一设计将原本需要跨越整个轨迹的一致性约束，分解为 $M$ 个独立的局部子问题，大幅降低了学习难度。局部 CD 采用图像免采样策略——里程碑隐变量由教师模型通过带 CFG 的 ODE 求解器生成，无需真实图文配对数据。

**第二阶段：全局一致性蒸馏。** 在局部 CD 收敛后，以 $T/M$ 为跳步，在相邻里程碑之间强制执行跨区间一致性。此时学生模型以自身合成的数据为输入，通过多步 ODE 求解器（$p$ 步）估计教师轨迹，并结合 MSE、GAN 和 DMD 三种损失联合优化，确保推理路径的全局连贯性与视觉质量。

### 关键模块与数据流

1. **教师 ODE 求解器**：在局部 CD 中生成里程碑隐变量；在全局 CD 中以 $p$ 步求解提供高精度监督信号。
2. **LoRA 适配器**：秩 64 的低秩矩阵，附加于教师 U-Net 的所有线性层，两阶段蒸馏仅更新此适配器，参数量极小。
3. **L-LPIPS 感知模型**：在 BAPPS 数据集上训练的隐空间感知相似度网络，替代 MSE 作为一致性损失，提升生成图像的感知质量。
4. **鉴别器**：基于教师 U-Net 的 GAN 判别器，在全局 CD 中强制学生输出在相邻里程碑处的分布一致性。
5. **DMD 分数模型**（可选）：预训练的真实/虚假分数网络，用于分布匹配蒸馏，进一步缩小学生与教师分布差异。

整个框架的数据流如图 2 所示：局部 CD 以教师生成的里程碑为锚点，将区间内任意点对齐至锚点；全局 CD 则在里程碑之间建立跳跃连接，最终形成从纯噪声到清晰图像的完整一致性映射。

### 补充图表

![[assets/figures/papers/paper_list_l896_https_openaccess_thecvf_com_content_CVPR2026_html_Xie_LogCD_Local_to_glo/figures/002_Figure_2.jpg]]
*Figure 2: The overview of the proposed LogCD. LogCD first executes local consistency distillation, illustrated in the left part, where the entire time range is divided into multiple sub-intervals and CD is performed in individual intervals. Then, global consistency distillation is proposed to enforce global consistency, shown in the right part*



LogCD 的核心设计思想是将复杂的全轨迹一致性映射分解为两个顺序阶段：**局部一致性蒸馏（Local CD）** 和 **全局一致性蒸馏（Global CD）**。这一分治策略的本质在于，先在局部时间区间内快速建立稳定的映射关系，再跨区间对齐以保障整条推理路径的连贯性。

### 局部一致性蒸馏模块（Local CD）

局部 CD 的目标是在单个时间子区间内强制一致性。具体而言，将扩散过程的完整时间范围 $[0, T]$ 划分为 $M$ 个预定义子区间，每个区间以固定的**里程碑时间步** $t_m$ 作为终点。对于区间内的任意时间步 $t_n$，模型需将噪声隐变量 $z_{t_n}$ 映射到与里程碑 $z_{t_m}$ 一致的去噪结果。

该阶段的均方误差损失定义为：

$$
\mathcal{L}_{LoCD}^{MSE} = \| g_\theta(z_{t_m}, t_m, t_{step}^s, c), sg(g_\theta(z_{t_n}, t_n, t_{step}^s, c)) \|_2^2
$$

其中 $g_\theta$ 为学生模型的一致性函数，$sg(\cdot)$ 表示停止梯度操作，$t_{step}^s$ 为学生采样步长，$c$ 为文本条件。通过固定里程碑作为目标，局部 CD 避免了随机终点时间步带来的冗余优化目标，从而加速收敛。

为将分类器自由引导（CFG）集成到局部 CD 的目标估计中，目标隐变量 $z_{t_n}$ 由教师模型 $\hat{\epsilon}_{\theta_0}$ 在 CFG 尺度 $w$ 下通过 ODE 求解器 $\Psi$ 从 $z_{t_m}$ 推演得到：

$$
z_{t_n} = \Psi(\hat{\epsilon}_{\theta_0}(z_{t_m}, c, w, t_m), t_m, t_n)
$$

该阶段采用**图像免采样**策略：教师模型从纯噪声生成样本，完全消除对图文配对训练数据的依赖。

### 全局一致性蒸馏模块（Global CD）

局部 CD 仅保证各区间内的自洽性，跨区间的全局连贯性由全局 CD 阶段建立。全局 CD 在预定义的里程碑时间步之间执行一致性蒸馏，跳跃步长设为 $T/M$。

该阶段的 MSE 损失为：

$$
\mathcal{L}_{GoCD}^{MSE} = \| f_\theta(\hat{z}_{t_m}, c, t_m), sg(f_\theta(\hat{z}_{t_n}, c, t_n)) \|_2^2
$$

其中 $f_\theta$ 为经局部 CD 初始化后的学生模型，$\hat{z}_t$ 为由学生自身合成的隐变量——这一设计同样消除了对真实图像数据的依赖。

全局 CD 的独特之处在于引入了两个额外目标以提升视觉质量和分布一致性：

**GAN 损失** 采用相对论判别器，强制学生在 $t_m$ 和 $t_n$ 处的输出分布一致：

$$
\mathcal{L}_{GoCD}^{GAN} = R(1 - D(FD(\widetilde{z}_{t_n}^0, t'), c, t')) + R(1 + D(FD(\widetilde{z}_{t_m}^0, t'), c, t'))
$$

其中 $FD$ 为冻结的解码器，将隐变量解码回像素空间供判别器 $D$ 评估，$R$ 为相对论函数，$\widetilde{z}^0$ 为预测的干净隐变量。

**DMD 损失** 通过预训练的真实分数模型 $s_{real}$ 和虚假分数模型 $s_{fake}$ 进行分布匹配：

$$
\mathcal{L}_{GoCD}^{DMD} = -\mathbb{E}_{t,\epsilon,\hat{z}_t} [ s_{real}(FD(f_\theta(\hat{z}_t, t, c), t'), c, t') - s_{fake}(FD(f_\theta(\hat{z}_t, t, c), t'), c, t') \nabla_\theta f_\theta(\epsilon) ]
$$

全局 CD 的总损失为三者的加权组合：

$$
\mathcal{L}_{GoCD} = \mathcal{L}_{GoCD}^{MSE} + \lambda_1 \mathcal{L}_{GoCD}^{GAN} + \lambda_2 \mathcal{L}_{GoCD}^{DMD}
$$

其中 $\lambda_1$ 和 $\lambda_2$ 为平衡超参数。此外，全局 CD 阶段使用带 CFG 的**多步 ODE 求解器**（$p$ 步）作为教师，有效减少了单步求解引入的离散化误差。消融实验表明 $p=3$ 时性能最优。

### L-LPIPS 感知损失模块

为替代隐空间 MSE 损失在感知层面的不足，LogCD 引入在 BAPPS 数据集上训练的**隐空间 LPIPS（L-LPIPS）** 模型。该模型采用 VGG 网络，将输入通道改为隐变量 $z_0$ 的通道数，并移除 3 个最大池化层以适配隐空间分辨率。

在局部和全局 CD 阶段，分别用 $\mathcal{L}_{LoCD}^{LLP}$ 和 $\mathcal{L}_{GoCD}^{LLP}$ 替换对应的 MSE 损失。消融实验证实，L-LPIPS 在所有评估指标上均优于 MSE，是 LogCD 性能提升的关键因素之一。

### 参数高效训练

所有蒸馏阶段均采用秩为 64 的 **LoRA 适配器**进行训练，而非全量微调 UNet/DiT 参数。这一设计使得整个蒸馏过程仅需约 70 A100 GPU 小时，在计算资源受限的场景下具有显著优势。



## 实验与关键发现

### 主实验结果

LogCD在SDXL和FLUX.1-dev两种架构上均展现出优异的少步生成性能。在SDXL架构上，仅需3步采样的LogCM在MSCOCO-2017 5K验证集上达到33.5的CLIP Score（CS），与25步teacher模型持平，并在Image Reward（IR）上以0.95超越teacher的约0.90（Table 1）。在MJHQ-5K上，3步LogCM取得35.2 CS和17.8 FID，同样表现出色。值得注意的是，整个蒸馏过程仅消耗70 A100 GPU小时，且无需任何训练图像，在资源效率上显著优于多数现有方法。

![[assets/figures/papers/paper_list_l896_https_openaccess_thecvf_com_content_CVPR2026_html_Xie_LogCD_Local_to_glo/figures/003_Table_1.jpg]]
*Table 1: Performance comparison on GenEval, MSCOCO-2017 5K, and MJHQ-5K validation datasets with state-of-the-art methods. All models adopt SDXL architecture. We use “-” to represent a metric when it is missing in the corresponding paper. Time: inference time (second) on A100. TH: The default unit is training hours using A100 except that marked by H denoting training time with H100*

在FLUX.1-dev架构上，4步LogCM在MSCOCO-2017 5K上达到32.6 CS，与25步teacher相当（Table 2），验证了该方法跨架构的泛化能力。由于显存限制，FLUX.1-dev的蒸馏未使用DMD损失，提示该组件可能带来进一步增益空间。

![[assets/figures/papers/paper_list_l896_https_openaccess_thecvf_com_content_CVPR2026_html_Xie_LogCD_Local_to_glo/figures/005_Table_2.jpg]]
*Table 2: LogCM’s performance on GenEval, MSCOCO-2017 5K, and MJHQ-5K validation dataset for FLUX.1-dev acceleration, with a guidance scale of 7.0*

与基线方法的对比揭示了LogCD在少步场景下的独特优势：在3-4步区间，LogCM在图文对齐（CS/IR）上系统性超越LCM、SDXL-Lightning、PCM、Flash SDXL等SOTA加速方法，而多数基线方法在4步以下时性能退化严重。

### 消融实验

Table 3系统拆解了LogCD各组件在4步采样器、SDXL架构下的贡献：

**局部一致性蒸馏（Local CD）基线**：仅使用MSE损失进行图像免采样的局部CD，可获得32.4 CS、27.9 FID和0.52 IR，构成有效但有限的起点。

**Latent LPIPS的增益**：将局部CD的MSE损失替换为在BAPPS数据集上训练的Latent LPIPS（L-LPIPS）后，所有指标均有提升。L-LPIPS在隐空间计算感知相似度，相比逐像素MSE更好地保持了生成图像的感知质量。

**全局一致性蒸馏（Global CD）的核心作用**：在局部CD基础上引入全局CD（使用L-LPIPS），CLIP Score和Image Reward均显著提升。这表明仅靠局部区间对齐无法保证跨区间的轨迹一致性，全局CD通过跨里程碑对齐有效弥补了这一缺陷。

**GAN损失的补充效应**：在全局CD中加入基于教师U-Net的GAN损失后，CS、美学分数（AS）和IR进一步提升。GAN判别器强制学生在不同里程碑处的输出分布与教师一致，改善了视觉质量。

**DMD损失的额外增益**：进一步叠加分布匹配蒸馏（DMD）损失，在所有指标上带来额外提升，验证了分布级对齐对一致性蒸馏的补充价值。

### 超参数分析

**时间区间数M**（Table 4）：M=8时达到最佳性能。过小的M导致局部区间过大，一致性映射难度增加；过大的M则使全局CD的里程碑间距过密，跨区间对齐的增益递减。

**教师多步求解器步数p**（Table 5）：全局CD阶段教师使用p=3步ODE求解器时效果最优。单步求解器（p=1）的离散化误差较大，而过多步数（p>3）带来的边际改善有限，且增加计算开销。

**学生生成步数q**（Table 6）：全局CD阶段学生使用q=3步已足够，进一步增加q未能带来显著增益，说明3步学生模型已能充分捕捉全局CD所需的分布特性。

### 定性分析

Figure 3的视觉对比显示，3步LogCM生成的1024×1024图像在细节保真度、色彩一致性和图文对齐方面与25步teacher高度接近，且在复杂场景下优于同等步数的LCM和SDXL-Lightning。然而，在部分复杂构图或细粒度文本描述场景下，少步生成仍可能出现微弱的图文不对齐，这是当前少步蒸馏方法的共性瓶颈。

### 失败模式与局限性

1. **DMD损失的架构限制**：在FLUX.1-dev蒸馏时因显存约束未使用DMD损失，可能限制了该模型上的性能上限。
2. **分辨率边界**：所有实验均在1024×1024及以下分辨率进行，未验证更高分辨率下的稳定性。
3. **复杂场景的残余不对齐**：尽管整体IR超越teacher，但在需要精确属性绑定的复杂提示下，少步生成仍可能出现局部细节与文本描述不一致的情况。
4. **与完全免训练方法的对比缺失**：论文未与Schnell等完全无需训练数据的方法进行公平实验对比，LogCD在该场景下的相对优势尚需手动验证。

### 补充图表

![[assets/figures/papers/paper_list_l896_https_openaccess_thecvf_com_content_CVPR2026_html_Xie_LogCD_Local_to_glo/figures/006_Table_3.jpg]]
*Table 3: Ablation study of LogCD with respect to L-LPIPS, Local CD, Global CD. All models adopt a 4-step sampler and SDXL architecture*

![[assets/figures/papers/paper_list_l896_https_openaccess_thecvf_com_content_CVPR2026_html_Xie_LogCD_Local_to_glo/figures/008_Table_4.jpg]]
*Table 4: Performance comparison on MSCOCO-2017 5K validation dataset with different time interval number M . All models adopt SDXL architecture and a 4-step sampler during the inference stage*

![[assets/figures/papers/paper_list_l896_https_openaccess_thecvf_com_content_CVPR2026_html_Xie_LogCD_Local_to_glo/figures/009_Table_5.jpg]]
*Table 5: Performance comparison when teacher uses different sampling steps p for global CD in the second stage. All models adopt SDXL architecture and a 4-step sampler during the inference stage*

![[assets/figures/papers/paper_list_l896_https_openaccess_thecvf_com_content_CVPR2026_html_Xie_LogCD_Local_to_glo/figures/007_Table_6.jpg]]
*Table 6: Performance comparison on MSCOCO-2017 5K validation dataset when student adopts different denoising steps q in global consistency distillation. All models adopt SDXL architecture and a 4-step sampler during the inference stage*



## 定位与知识库关联

### 1. 从单阶段全局蒸馏到两阶段局部-全局蒸馏

LogCD 的核心定位在于解决一致性蒸馏（Consistency Distillation, CD）范式中的一个深层瓶颈：**将复杂全轨迹一致性映射分解为局部子问题**。现有 CD 方法可大致归为两类：

- **单阶段全局一致性蒸馏**：以 **LCM**（Luo et al., ICML 2023）为代表，直接在完整时间轴 $[0, T]$ 上强制任意两点间的一致性。这类方法面临收敛困难与训练不稳定问题，通常需要大量训练资源或造成图文对齐性能的严重下降。**PCM**（Wang et al., ICML 2024）引入了分段一致性，但仍属单阶段训练框架，未将局部收敛与全局连贯性解耦优化。

- **多阶段轨迹一致性**：**HyperSD**（Ren et al., ICLR 2024）通过多阶段训练逐步缩短时间区间，但各阶段目标函数同质化，缺乏对局部感知质量和全局跨区间连贯性的差异化处理。**CTM**（Kim et al., ICLR 2024）允许随机终点时间步，虽增加了灵活性，却引入了冗余目标，增加了优化难度。

LogCD 的**分治策略**改变了上述格局：先执行**局部一致性蒸馏（Local CD）**，将时间轴划分为 $M$ 个区间，在每个区间内以固定里程碑为终点进行一致性映射；再执行**全局一致性蒸馏（Global CD）**，跨里程碑对齐，并引入多步 ODE 求解器、GAN 损失和可选的 DMD 损失以提升全局连贯性与视觉质量。这一两阶段设计的关键优势在于：局部阶段快速收敛于子问题，全局阶段在已收敛的局部模型基础上进行轻量级跨区间微调，整体仅需 **70 A100 GPU 小时**。

### 2. 与对抗蒸馏和分布匹配蒸馏的关系

在少步生成领域，LogCD 与两类主流加速范式形成互补而非替代：

- **渐进对抗蒸馏**：**SDXL-Lightning**（Lin et al., 2024）和 **Flash SDXL**（Chadebec et al., 2024）通过对抗训练逐步减少学生采样步数。这类方法在视觉质量上表现优异，但通常需要大规模图文配对数据集进行训练。LogCD 的**图像免采样策略**——局部 CD 使用教师生成样本、全局 CD 使用学生合成数据——使其完全摆脱了对训练图像的依赖，在数据隐私或数据稀缺场景下具有明显优势。

- **分布匹配蒸馏**：**DMD2**（Yin et al., 2024）通过最小化真实与虚假分数模型的差异来匹配分布，在单步生成上表现突出。LogCD 在全局 CD 阶段可选地集成了 DMD 损失（公式 $\mathcal{L}_{GoCD}^{DMD}$），将其作为 MSE 和 GAN 损失的补充，而非独立依赖。这种组合策略在 2-4 步的中间地带取得了更均衡的图文对齐与视觉质量。

### 3. 技术贡献的差异化定位

LogCD 在以下技术维度上形成了明确的差异化优势：

| 技术维度 | 基线方法 | LogCD 方案 | 差异化价值 |
|---------|---------|-----------|-----------|
| **一致性范式** | 单阶段全局（LCM, PCM） | 两阶段局部到全局 | 降低优化难度，加速收敛 |
| **局部 CD 目标** | 随机终点（CTM, HyperSD） | 固定里程碑 | 消除冗余目标，提升训练效率 |
| **感知损失** | 隐空间 MSE | Latent LPIPS（BAPPS 训练） | 提升感知一致性，改善图文对齐 |
| **训练数据** | 需要图文配对数据集 | 图像免采样 | 零训练图像依赖 |
| **全局 CD 求解器** | 单步 ODE | 带 CFG 的多步求解器（$p$ 步） | 减少离散化误差 |
| **全局 CD 目标** | 仅 MSE | MSE + GAN + DMD | 提升分布匹配与视觉质量 |
| **参数效率** | 全量 UNet/DiT 微调 | 秩 64 的 LoRA | 显著降低显存与训练成本 |

### 4. 适用边界与局限

LogCD 的验证范围界定了其当前的适用边界：

- **架构覆盖**：已在 SDXL-base-1.0（UNet 架构）和 FLUX.1-dev（DiT 架构）上验证，但尚未测试更大规模模型（如 SD3）或更少步数（1 步）场景。FLUX.1-dev 上的蒸馏因显存限制未使用 DMD 损失，4 步 LogCM 的 CLIP Score 为 32.6，与 25 步 teacher 相当但未显著超越，暗示 DMD 损失在 DiT 架构上可能具有额外增益潜力。
- **分辨率限制**：所有实验均在 1024×1024 分辨率下进行，更高分辨率下的性能未经验证。
- **复杂场景对齐**：少步生成在某些复杂场景下可能仍存在微弱的图文不对齐，这是当前蒸馏方法的共性局限。Latent LPIPS 在 BAPPS 数据集上训练，其对人类感知的匹配度仍可进一步改进。
- **与完全免训练方法的对比缺失**：与 **Schnell**（Black Forest Labs, 2024）等完全无训练数据的方法缺乏公平实验对比，LogCD 在该场景下的相对优劣尚不明确。

### 5. 开放问题与后续方向

基于上述分析，LogCD 框架指向以下开放问题：

1. **一步生成的可达性**：Local CD + Global CD 的两阶段范式能否通过调整里程碑密度和全局 CD 损失权重扩展到 1 步生成？当前在 3 步已接近 teacher 性能，进一步压缩步数可能需要在局部阶段引入更强的分布匹配约束。

2. **Latent LPIPS 的感知对齐上限**：当前 L-LPIPS 基于 VGG 网络在 BAPPS 上训练，是否可以通过引入更大的感知骨干网络（如 ViT-based 模型）或在大规模隐空间数据上预训练来进一步提升？这直接影响图文对齐指标（如 Image Reward）的上限。

3. **跨架构泛化性**：LogCD 在 UNet（SDXL）和 DiT（FLUX）上的成功表明其范式具有架构无关性，但视频生成模型（如 SVD）或 3D 生成模型上的适用性尚未探索。局部-全局分解策略在更高维度的生成空间中可能带来更显著的收敛优势。

4. **CFG 引导强度的动态调度**：当前 LogCD 在局部和全局 CD 阶段使用固定的 CFG 引导强度 $w$。是否可以在不同时间区间或里程碑处动态调整 $w$，以在图文对齐和多样性之间取得更精细的权衡？

5. **与推理端加速的协同**：LogCD 的 3-4 步采样是否可与推理端的 token 合并、缓存复用等技术协同，进一步降低端到端延迟？当前仅记录了单张图像推理时间，系统级优化空间尚待挖掘。



## 原文 PDF

![[paperPDFs/CVPR_2026/LogCD_Local_to_global_Consistency_Distillation_for_Few_step_Image_Generation.pdf]]
