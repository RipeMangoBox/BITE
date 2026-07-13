---
title: GraspDiff Grasping Generation for Hand Object Interaction with Multimodal Guided Diffusion
type: paper
paper_level: A
venue: TVCG
year: 2024
pdf_ref: paperPDFs/TVCG_2024/GraspDiff_Grasping_Generation_for_Hand_Object_Interaction_with_Multimodal_Guided_Diffusion.pdf
project_link: null
code_link: null
aliases:
- GGGHOIMGD
tags:
- TVCG_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 扩散模型的迭代去噪过程可替代传统优化，直接从潜在空间生成抓取姿态，消除对接触图优化的依赖。
primary_logic: 利用潜在扩散模型，将抓取姿态嵌入标准正态分布，并通过跨注意力机制融合多模态条件（点云、接触图、部件图、图像），实现快速、多样且逼真的抓取生成。
claims:
- 扩散模型的迭代去噪步骤可以取代现有优化方法中的迭代优化例程。
- GraspDiff在穿透体积（4.32 cm³）上优于最佳基线ContactGen（4.49 cm³），且生成速度（0.795秒）远快于传统方法。
- 消融实验证实VAE模块对于紧凑扩散生成至关重要，移除后性能显著下降。
- ObMan (in-domain) 上 Penetration Volume (cm³) = 4.32
---

# GraspDiff Grasping Generation for Hand Object Interaction with Multimodal Guided Diffusion

> [!tip] 核心洞察
> 利用潜在扩散模型，将抓取姿态嵌入标准正态分布，并通过跨注意力机制融合多模态条件（点云、接触图、部件图、图像），实现快速、多样且逼真的抓取生成。

| 字段 | 内容 |
|------|------|
| 中文题名 | GraspDiff：基于多模态引导扩散的手物交互抓取生成 |
| 英文题名 | GraspDiff Grasping Generation for Hand Object Interaction with Multimodal Guided Diffusion |
| 会议/期刊 | TVCG 2024 |
| Links |  [paper](https://doi.org/10.1109/TVCG.2024.3466190)|
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | GraspDiff |
| Dataset | ObMan, HO-3D, FPHAB |

> [!tip] 效果简介
> - ObMan (in-domain) 上，Penetration Volume (cm³) 4.32 vs 4.49 (ContactGen) (-0.17)；Simulation Displacement (cm) 1.91 vs 2.59 (GraspTTA) (-0.68)。
> - HO-3D (out-of-domain) 上，Penetration Volume (cm³) 4.66 vs 4.72 (GraspTTA) (-0.06)；Simulation Displacement (cm) 4.46 vs 4.68 (GraspTTA) (-0.22)。
> - FPHAB (out-of-domain) 上，Penetration Volume (cm³) 4.47 vs 5.17 (GraspTTA) (-0.70)。

## 概要

### 问题瓶颈
现有手物交互抓取生成方法（如**Grasping Field**、**GrabNet**、**GraspTTA**、**ContactGen**）普遍依赖VAE或GAN架构，并辅以接触图的迭代优化来提升抓取质量。这一范式存在两个核心缺陷：一是迭代优化导致生成速度缓慢；二是生成质量对接触图的精度高度敏感，难以在保证物理逼真性的同时维持抓取的多样性。

### 核心思路
GraspDiff的核心洞察在于：**扩散模型固有的迭代去噪过程可以替代传统方法中的迭代优化例程**。具体而言，该方法将MANO手部参数通过VAE嵌入到标准正态分布的潜在空间，使扩散模型能够在紧凑的潜在表示上进行去噪生成，从而消除对外部接触图优化的依赖。同时，通过交叉注意力机制融合多模态条件（物体点云、接触图、部件图、二维图像），实现可控且多样化的抓取生成。

### 方法定位
GraspDiff属于**基于潜在扩散模型的抓取生成方法**，在方法谱系上区别于VAE/GAN加优化的传统路线。其技术栈包含四个关键模块：
- **VAE编解码器**：将手部姿态压缩至低维潜在空间，保证生成紧凑性。
- **条件编码器与交叉注意力**：分别提取多模态条件特征，并在去噪U-Net中通过交叉注意力融合。
- **扩散去噪网络**：在潜在空间中迭代去噪，生成多样化抓取候选。
- **可选RefineNet**：轻量级后优化网络，基于手物距离进一步微调抓取姿态。

### 主要结果
在域内（ObMan）和域外（HO-3D、FPHAB）三个基准上的实验表明：
- **物理合理性**：GraspDiff在穿透体积上达到4.32 cm³（ObMan），优于最强基线ContactGen的4.49 cm³；在域外FPHAB上，穿透体积较GraspTTA降低0.70 cm³。
- **生成速度**：单次抓取生成仅需0.795秒，显著快于依赖迭代优化的传统方法。
- **消融验证**：移除VAE模块导致穿透体积从4.32升至5.85，证实潜在空间对扩散生成的必要性；交叉注意力机制同样被证明优于简单的特征拼接。

### 局限与开放问题
模型在以下方面仍存在不足：对未见物体有时生成相似抓取姿态；部件图引导的接触匹配精度有限。开放问题包括极端未见形状的泛化边界、扩散采样步数对质量与速度的权衡，以及引入真实数据集（如GRAB）以改善抓取自然度的可行性。



手物交互中的灵巧抓取生成是计算机视觉与机器人学中的核心问题，其目标是为给定物体自动合成自然、无穿透且物理合理的手部姿态。这一任务面临两大根本挑战：一是生成结果的**多样性**——同一物体往往存在多种合理的抓取方式；二是生成结果的**逼真性**——抓取姿态必须在几何上避免手-物穿透，并在物理上保持稳定。

现有抓取生成方法主要依赖变分自编码器（VAE）或生成对抗网络（GAN）作为生成骨干，并辅以迭代优化例程来精修接触图。代表性工作包括**Grasping Field**（Karunratanakul et al., 3DV 2020）、**GrabNet**（Taheri et al., ECCV 2020）、**GraspTTA**（Jiang et al., ICCV 2021）以及**ContactGen**（Liu et al., ICCV 2023）。这些方法的共同范式是：先生成一个初始抓取姿态，再通过基于接触图的迭代优化来减少穿透、改善接触质量。

然而，这一范式存在两个结构性的瓶颈。第一，**迭代优化过程速度慢**：优化例程通常需要数十至上百次迭代才能收敛，严重制约了实时应用的可能性。第二，**对接触图精度高度敏感**：接触图的质量直接决定优化结果的上限，而接触图本身的预测误差会在优化过程中被放大，导致生成结果在多样性与逼真性之间难以兼得——过于保守的优化会牺牲多样性，而过于宽松的优化又会导致穿透。

扩散模型在图像与三维生成领域的成功为解决上述困境提供了新的思路。扩散模型的核心机制——从噪声中逐步恢复干净信号——与抓取生成中的迭代优化在形式上具有天然的对应关系。GraspDiff的核心洞察在于：**扩散模型的迭代去噪步骤可以直接取代现有方法中的迭代优化例程**，从而消除对接触图优化的依赖。通过在潜在空间中执行扩散过程，模型可以从标准正态分布出发，一次性生成多样且逼真的抓取姿态，而无需后验优化。

此外，真实世界的抓取生成往往需要融合多种粒度的条件信息——从粗粒度的物体点云，到细粒度的接触图、部件图，乃至二维图像。现有方法通常将这些条件直接拼接或仅用于后处理阶段，缺乏灵活的多模态条件融合机制。GraspDiff通过为每种模态设计专用编码器，并利用交叉注意力机制在去噪网络中动态融合条件特征，实现了从单模态到多模态的统一生成框架。

综上，GraspDiff的动机可归结为三个层面：**（1）用扩散模型的迭代去噪替代传统优化，从根本上解决速度与精度矛盾；（2）在潜在空间中执行紧凑的扩散生成，保证多样性的同时提升效率；（3）通过交叉注意力实现多模态条件的灵活融合，使生成过程可被不同粒度的信息引导。**



## 核心方法与创新机理

GraspDiff 的核心创新在于**用潜在扩散模型的迭代去噪过程替代传统方法中依赖接触图的后处理优化**，从而在单一框架内同时提升抓取姿态的生成质量、多样性与推理速度。

### 1. 生成范式的根本转变：从“VAE+优化”到“潜在扩散”

现有抓取生成方法（如 **Grasping Field** (Karunratanakul et al., 3DV 2020)、**GrabNet** (Taheri et al., ECCV 2020)、**GraspTTA** (Jiang et al., ICCV 2021) 以及 **ContactGen** (Liu et al., ICCV 2023)）普遍遵循“VAE/GAN 生成初始姿态 + 接触图迭代优化”的范式。这一流程存在两个瓶颈：一是迭代优化步骤耗时，二是生成质量高度依赖接触图的精度，难以在保证物理合理性的同时维持姿态多样性。

GraspDiff 的因果调控旋钮在于识别出：扩散模型固有的迭代去噪步骤可以天然地取代外部优化例程。论文明确指出：

> “our key idea is that the iterative denoising steps inherent to diffusion models can supplant the iterative optimization routines in existing optimization methods”

具体而言，GraspDiff 将 MANO 手部参数（$\theta, \beta, t$，共 61 维）通过 VAE 编码器 $\mathcal{E}$ 嵌入到 64 维的紧凑潜在空间 $z = \mathcal{E}(H)$ 中，使其分布逼近标准正态分布 $\mathcal{N}(0, \mathbf{I})$。扩散模型在该潜在空间上执行去噪过程，直接生成抓取姿态的潜在表示，再通过 VAE 解码器 $\mathcal{D}$ 还原为手部参数。这一设计消除了对接触图优化的依赖，将生成过程统一为端到端的扩散采样。

### 2. 条件融合机制的升级：从“拼接/后优化”到“跨注意力多模态融合”

传统方法通常将接触图作为后优化目标或直接拼接到输入中，条件信息的利用方式较为粗糙。GraspDiff 将条件集成方式升级为**多模态编码器 + 跨注意力融合**：

- **多模态条件编码**：针对不同粒度的引导信号——物体点云、接触图（contact map）、部件图（part map）以及 2D 图像——设计了专用的条件编码器 $\phi_i$，分别提取特征。
- **跨注意力注入**：这些条件特征通过跨注意力模块（cross-attention）注入到去噪 U-Net $\Psi$ 的中间层，使得扩散过程能够在每一步都感知条件信息，而非仅在输入阶段进行一次性的条件拼接。

消融实验证实了这一设计的有效性：将跨注意力替换为简单拼接后，穿透体积从 4.32 cm³ 升高至 4.73 cm³（Table VII），表明跨注意力机制对生成保真度有实质贡献。

### 3. 模块化 RefineNet：可选的后处理增强

GraspDiff 在扩散生成之后集成了一个轻量级的可选的 RefineNet 模块，基于手-物体距离进一步优化抓取姿态。消融实验显示，移除 RefineNet 后穿透体积升至 4.93 cm³，但仍优于所有基线方法，说明扩散模型本身已能生成合理的抓取，RefineNet 提供的是锦上添花的物理合理性增强。

### 4. VAE 潜在空间的必要性

一个关键的架构决策是将扩散过程置于 VAE 的潜在空间而非原始参数空间。消融实验强有力地支撑了这一设计：移除 VAE 模块（即直接在 61 维手部参数上执行扩散）导致穿透体积从 4.32 cm³ 急剧恶化至 5.85 cm³，且出现了“虚假多样性”问题（Table VII）。这表明 VAE 对高维手部参数的压缩和正则化是扩散模型有效生成的前提——紧凑的潜在空间使得去噪网络更容易学习数据分布，同时 KL 散度约束 $\mathcal{L}_{KL} = KL(q(z \mid \mu, \delta^2) \| \mathcal{N}(0, \mathbf{I}))$ 确保了采样时的数值稳定性。

### 5. 速度优势的结构性来源

由于消除了外部迭代优化，GraspDiff 的单次生成仅需 0.795 秒（Table V），显著快于依赖优化的传统方法。这一速度优势源于扩散采样的固定步数特性——去噪过程在训练时已学会直接预测干净潜在向量 $z_0$，推理时无需对每个样本执行耗时的接触图优化循环。



GraspDiff 的整体 pipeline 围绕一个**潜在扩散模型（Latent Diffusion Model）**构建，其核心设计思想是用扩散模型的迭代去噪过程取代传统方法中依赖接触图的后优化步骤，从而在保证抓取多样性的同时提升生成速度与物理合理性。整个框架由四个主要模块串联构成：**VAE 潜在空间嵌入**、**多模态条件编码与交叉注意力融合**、**潜在扩散去噪生成**，以及**可选的 RefineNet 后优化**。图 2 给出了完整的架构概览。

### 1. 数据流与模块关系

**输入**：框架接受多模态条件信号 $y$，包括物体点云（必选），以及可选的接触图（contact map）、部件图（part map）或 2D 图像。这些条件以不同粒度描述抓取意图。

**VAE 潜在嵌入（训练阶段）**：首先将手部参数 $H = [\theta \,|\, \beta \,|\, t] \in \mathbb{R}^{61}$（MANO 模型的姿态、形状、全局平移）通过 VAE 编码器 $\mathcal{E}$ 映射到紧凑的潜在向量 $z = \mathcal{E}(H)$，并在训练时通过解码器 $\mathcal{D}$ 重建 $\hat{H} = \mathcal{D}(z)$。VAE 的 KL 散度损失强制潜在空间趋近标准正态分布 $\mathcal{N}(0, \mathbf{I})$，为后续扩散生成提供规整的采样空间。这一映射是框架的关键因果旋钮——消融实验表明，移除 VAE 模块后穿透体积从 4.32 cm³ 升至 5.85 cm³，且生成结果的虚假多样性显著增加（Table VII），证明紧凑的潜在空间对扩散生成至关重要。

**多模态条件编码**：不同模态的条件 $y$ 分别由专用的编码器 $\phi_0, \phi_1, \phi_2, \phi_3$ 提取特征。这些条件特征随后通过**交叉注意力机制（Cross-Attention）**注入到去噪网络 $\Psi$ 的中间层，引导去噪过程朝向符合条件的方向。与直接拼接（concatenation）相比，交叉注意力融合在保真度上有明显优势（Table VII 中拼接方案穿透体积升至 4.73 cm³）。

**潜在扩散去噪（推理核心）**：推理时，从标准正态分布采样随机噪声 $z_T \sim \mathcal{N}(0, \mathbf{I})$，在条件特征 $\phi_i(y)$ 的引导下，通过去噪网络 $\Psi$ 迭代去噪 $T$ 步（$T=1000$，线性噪声调度），得到干净的潜在向量 $z_0$。去噪网络直接预测干净潜在向量 $z_0$ 而非噪声，损失函数为 $\mathcal{L}_{Diff} = \mathbb{E}_{\mathcal{E}(H), t, y} \left[ \| z_0 - \Psi(z_t, t \mid \phi_i(y)) \|_2^2 \right]$（Eq. 8）。为进一步增强泛化性，框架采用无分类器引导（classifier-free guidance），在推理时对条件输出与无条件输出进行插值：$\Psi(z_t, \phi_i(y)) = (1-w)\Psi(z_t, \phi_i(y)) + w\Psi(z_t, \emptyset)$（Eq. 9）。

**解码与后优化**：去噪得到的 $z_0$ 通过冻结的 VAE 解码器 $\mathcal{D}$ 重建为手部参数 $\hat{H}$，再经 MANO 层映射为手部网格。之后，一个轻量级的**可选 RefineNet 模块**基于手-物距离 $D$ 对抓取姿态进行微调，进一步减少穿透与浮空。消融实验显示，移除 RefineNet 后穿透体积升至 4.93 cm³，但仍优于所有基线（Table VII），说明扩散模型本身已能生成合理的抓取姿态，RefineNet 起锦上添花的作用。

### 2. 训练策略

训练分两阶段进行：
- **阶段一**：独立训练 VAE，损失函数为 $\mathcal{L}_{VAE} = \lambda_1 \mathcal{L}_{KL} + (\lambda_2 \mathcal{L}_{MSE} + \lambda_3 \mathcal{L}_{CD} + \lambda_4 \mathcal{L}_{Pene.})$（Eq. 5），同时优化重构精度与潜在空间的正则性。
- **阶段二**：固定 VAE 编码器，训练条件扩散模型 $\Psi$，最小化 $\mathcal{L}_{Diff}$。之后可进行端到端微调，总损失为 $\mathcal{L}_{Total} = \mathcal{L}_{VAE} + \mathcal{L}_{Diff} + \| H - \mathcal{D}(\psi(z_t, t \mid \phi_i(y))) \|_2^2$（Eq. 10）。

### 3. 关键设计决策总结

| 设计选择 | 作用 | 消融验证 |
|----------|------|----------|
| VAE 潜在空间（dim=64） | 压缩手部参数，提供规整的扩散采样空间 | 移除后穿透体积 +1.53 cm³ |
| 交叉注意力融合条件 | 将多模态条件有效注入去噪过程 | 替换为拼接后穿透体积 +0.41 cm³ |
| 预测 $z_0$ 而非噪声 | 直接优化潜在向量的重构精度 | 框架核心公式设计 |
| 无分类器引导 | 平衡条件一致性与生成多样性 | 推理时的关键超参数 |
| 可选 RefineNet | 基于物理距离的后优化 | 移除后穿透体积 +0.61 cm³，但仍优于基线 |

> **证据强度说明**：上述模块关系与数据流均来自论文方法章节（Section IV）及 Fig. 2 的明确描述，消融结论由 Table VII 的定量结果支撑（置信度 0.98）。VAE 必要性、交叉注意力优势、RefineNet 贡献均有对应消融实验锚点。

![[assets/figures/papers/paper_list_l1811_GraspDiff_Grasping_Generation_for_Hand_Object_Interaction_with_Multimoda/figures/003_Figure_2.jpg]]
*Figure 2: Overview of our GraspDiff framework. We first embed the training data into the latent space with a VAE module and employ the diffusion model to generate hand grasps. Multimodal conditions are considered for varying granularity and are optionally supplemented onto the point clouds. With a frozen VAE decoder, the desired grasps are obtained. A refinement module is also integrated to further improve the plausibility of grasps*



### 1. 潜在空间嵌入与VAE模块

GraspDiff 的核心思路是将抓取姿态的生成问题从高维参数空间迁移至紧凑的潜在空间。为此，方法首先训练一个**VAE模块**（编码器 $\mathcal{E}$ 与解码器 $\mathcal{D}$），将 MANO 手部参数 $H = [\theta \mid \beta \mid t] \in \mathbb{R}^{61}$ 映射到潜在向量 $z$ 并重建：

$$z = \mathcal{E}(H), \quad \hat{H} = \mathcal{D}(z)$$

这一嵌入步骤将训练数据分布规约到标准正态分布附近，使后续扩散模型能够在紧凑、规整的潜在空间中进行生成。VAE 的总损失函数为：

$$\mathcal{L}_{VAE} = \lambda_1 \mathcal{L}_{KL} + (\lambda_2 \mathcal{L}_{MSE} + \lambda_3 \mathcal{L}_{CD} + \lambda_4 \mathcal{L}_{Pene.})$$

其中：
- $\mathcal{L}_{KL} = KL(q(z \mid \mu, \delta^2) \| \mathcal{N}(0, \mathbf{I}))$ 为 KL 散度损失，迫使潜在分布逼近标准正态分布；
- $\mathcal{L}_{MSE}$ 为手部参数的重构均方误差；
- $\mathcal{L}_{CD}$ 为重建手部顶点与真实顶点之间的 Chamfer 距离；
- $\mathcal{L}_{Pene.}$ 为穿透惩罚项，抑制手部与物体的非物理穿透。

消融实验证实，移除 VAE 模块后穿透体积从 4.32 cm³ 急剧上升至 5.85 cm³，且生成多样性出现虚假膨胀，表明潜在空间对扩散生成的紧凑性和质量至关重要（Table VII）。

### 2. 潜在扩散去噪模型

在获得潜在向量 $z_0 = \mathcal{E}(H)$ 后，GraspDiff 采用标准 DDPM 框架进行扩散生成。前向过程逐步向 $z_0$ 添加高斯噪声：

$$q(z_t \mid z_{t-1}) = \mathcal{N}(z_t; \sqrt{1-\beta_t}\,z_{t-1}, \beta_t \mathbf{I})$$

其中 $\beta_t$ 为噪声调度参数。扩散模型 $\Psi$ 的训练目标是最小化干净潜在向量与去噪预测之间的均方误差：

$$L_{Diff} = \mathbb{E}_{\mathcal{E}(H), t} \left[ \| z_0 - \Psi(z_t, t) \|_2^2 \right]$$

这一设计的核心洞察在于：**扩散模型的迭代去噪步骤可以取代现有优化方法中的迭代优化例程**，从而直接从潜在空间生成抓取姿态，消除了对接触图后优化步骤的依赖。实验设置中，扩散总步数 $T=1000$，采用线性噪声调度，潜在空间维度设为 64。

### 3. 多模态条件编码与交叉注意力融合

为支持不同粒度的引导信号，GraspDiff 设计了专门的**条件编码器** $\phi_i$（$i=0,1,2,3$），分别处理物体点云、接触图、部件图和 2D 图像四种模态。提取的条件特征通过**交叉注意力机制**融入去噪网络 $\Psi$ 的中间层，实现条件引导下的生成。对应的条件扩散损失为：

$$L_{Diff} = \mathbb{E}_{\mathcal{E}(H), t, y} \left[ \| z_0 - \Psi(z_t, t \mid \phi_i(y)) \|_2^2 \right]$$

在推理阶段，采用**无分类器引导**策略增强泛化能力，通过对条件输出与无条件输出的插值实现：

$$\Psi(z_t, \phi_i(y)) = (1-w)\Psi(z_t, \phi_i(y)) + w\Psi(z_t, \emptyset)$$

其中 $w$ 为引导权重，$\emptyset$ 表示空条件。消融研究表明，将交叉注意力替换为简单的特征拼接会导致穿透体积上升至 4.73 cm³，验证了交叉注意力融合机制的有效性（Table VII）。

### 4. 可选的 RefineNet 优化模块

GraspDiff 集成了一个模块化且可选的 **RefineNet**，基于手-物距离对生成的抓取姿态进行进一步优化。该模块作为后处理步骤，可在扩散生成的基础上微调手部参数以进一步减少穿透。消融实验显示，移除 RefineNet 后穿透体积升至 4.93 cm³，但仍优于所有基线方法，说明扩散模型本身已具备生成合理抓取的能力（Table VII）。

### 5. 端到端微调

最终，GraspDiff 支持端到端的联合微调，总损失函数为：

$$\mathcal{L}_{Total} = \mathcal{L}_{VAE} + \mathcal{L}_{Diff} + \left\| H - \mathcal{D}(\Psi(z_t, t \mid \phi_i(y))) \right\|_2^2$$

该损失在 VAE 损失和扩散损失的基础上，额外加入手部参数的重构 MSE，使整个流水线能够协同优化。

### 补充图表

![[assets/figures/papers/paper_list_l1811_GraspDiff_Grasping_Generation_for_Hand_Object_Interaction_with_Multimoda/figures/014_Figure_8.jpg]]
*Figure 8: Grasping generation with multimodal conditions as guidance. We show more fine-grained generations in different conditions, including (a) the basic conditions with object point clouds only; (b) joint conditions with contact map; (c) joint conditions with part map; (d) joint conditions with 2D image*



## 实验与关键发现

### 核心实验设计

GraspDiff的实验围绕三个核心问题展开：扩散范式能否取代传统VAE/GAN+迭代优化的抓取生成流程？多模态条件引导是否有效？各模块的贡献如何？实验采用**ObMan**合成数据集作为域内（in-domain）训练与测试基准，并在**HO-3D**和**FPHAB**两个真实场景数据集上进行跨域（out-of-domain）泛化测试。所有基线方法（**Grasping Field** (Karunratanakul et al., 3DV 2020)、**GrabNet** (Taheri et al., ECCV 2020)、**GraspTTA** (Jiang et al., ICCV 2021)、**ContactGen** (Liu et al., ICCV 2023)）均在相同的ObMan训练集上重新训练，超参数与原作者设置一致，评估指标标准化，保证了对比的公平性。

评估体系覆盖物理合理性、交互质量与多样性三个维度：**穿透深度**（Penetration Depth, cm）、**穿透体积**（Penetration Volume, cm³）、**接触率**（Contact Ratio, %）、**仿真位移**（Simulation Displacement, cm）——后者通过将生成的抓取网格导入物理仿真器并测量手部被推开的最小距离来量化抓取稳定性。多样性则通过K-Means聚类（20类）后计算**聚类分配的熵**和**平均簇大小**来衡量。

### 主实验结果

#### 域内性能（ObMan）

在ObMan测试集上（Table II），GraspDiff在穿透体积上达到**4.32 cm³**，优于最强基线ContactGen的4.49 cm³（Δ=−0.17），穿透深度0.48 cm与ContactGen持平。在仿真位移指标上，GraspDiff取得**1.91 cm**，显著优于GraspTTA的2.59 cm（Δ=−0.68），表明生成的抓取在物理仿真中更加稳定。接触率93.81%与ContactGen的93.93%接近，说明扩散模型在保持高接触质量的同时减少了穿透。多样性方面，GraspDiff的聚类熵为2.85，簇大小3.13，与ContactGen（2.84/3.10）相当，证明扩散生成并未牺牲多样性。

定性对比（Fig. 3）进一步印证了定量结论——红色圆圈标注的穿透区域和绿色圆圈标注的浮空/仅手掌接触的不稳定抓取在GraspDiff中明显更少。

![[assets/figures/papers/paper_list_l1811_GraspDiff_Grasping_Generation_for_Hand_Object_Interaction_with_Multimoda/figures/004_Figure_3.jpg]]
*Figure 3: Qualitative comparisons on in-domain objects from ObMan. We display two views for each generated hand grasp. The regions with red circles denote that the hand penetrates the object, while green circles denote unstable grasping where the fingers float on the object surface or only the palm is close to the object. The visualizations depict more plausible and realistic interactions of ours*

#### 跨域泛化性能

在HO-3D（Table III）和FPHAB（Table IV）两个真实场景数据集上，GraspDiff展现了稳定的泛化能力。HO-3D上穿透体积**4.66 cm³**，略优于GraspTTA的4.72 cm³（Δ=−0.06）；仿真位移**4.46 cm**，优于GraspTTA的4.68 cm（Δ=−0.22）。FPHAB上的优势更为明显：穿透体积**4.47 cm³** vs. GraspTTA的5.17 cm³（Δ=−0.70），仿真位移**2.24 cm** vs. 3.34 cm（Δ=−1.10）。值得注意的是，部分方法（如Grasping Field）在跨域场景下出现严重的穿透和浮空问题，而GraspDiff保持了相对稳定的表现（Fig. 5）。

![[assets/figures/papers/paper_list_l1811_GraspDiff_Grasping_Generation_for_Hand_Object_Interaction_with_Multimoda/figures/010_Figure_5.jpg]]
*Figure 5: Qualitative comparisons on out-of-domain objects from HO-3D (left) and FPHAB (right). We display two views for the generated grasps. Although for these unseen objects, our method could produce interactions with fewer penetrations and floats. The penetrations are circled in red, while the floats or only the palm close to the object are circled in green*

#### 生成效率

Table V的生成时间对比揭示了扩散范式的效率优势。GraspDiff的单次生成仅需**0.795秒**，而基于迭代优化的ContactGen需要约1.5秒，GraspTTA因测试时自适应优化耗时更长。这一结果直接验证了核心洞察——扩散模型的迭代去噪步骤可以取代传统方法中耗时的迭代优化例程。

#### 用户感知研究

Table VI和Fig. 6展示了人类感知评分分布。参与者对域内和域外物体的生成结果进行Likert量表评分，GraspDiff在“强烈同意”区间获得最高分布密度，表明人类评判者认为其生成的抓取在逼真度上优于或可比于现有方法。

### 消融实验

Table VII的消融研究系统验证了各模块的贡献：

1. **移除VAE模块（w/o VAE）**：穿透体积从4.32 cm³急剧升至**5.85 cm³**，且虚假多样性增加。这证实了VAE将MANO手部参数嵌入紧凑潜在空间对于扩散模型有效生成至关重要——直接在原始参数空间扩散会导致生成质量显著下降。

2. **移除RefineNet（w/o RefineNet）**：穿透体积升至4.93 cm³，但仍优于ContactGen的4.49 cm³。这说明扩散模型本身已能生成合理的抓取姿态，RefineNet作为可选模块提供了额外的物理合理性优化。

3. **用拼接取代交叉注意力（concatenation）**：穿透体积升至4.73 cm³，生成保真度下降，证明了跨注意力机制在融合多模态条件特征方面的有效性。

### 多模态条件引导效果

Fig. 8展示了不同模态条件引导下的生成效果：（a）仅点云条件可生成基本合理的抓取；（b）加入接触图（contact map）引导后，手部接触区域更加精确；（c）部件图（part map）引导的效果相对较弱，生成的抓取无法精确匹配指定接触区域——这被列为方法的已知局限之一；（d）2D图像条件也能有效引导抓取生成。多模态条件的灵活组合使GraspDiff能够适应不同粒度的控制需求。

### 失败模式分析

Fig. 11揭示了两个主要失败模式：

1. **姿态同质化**：对于形状差异较大的未见物体，生成的手部抓取有时趋于相似。这在训练数据中某些抓取姿态占主导时尤为明显，反映了扩散模型在极端未见形状上的泛化瓶颈。

2. **部件图引导不准确**：当使用部件图作为条件时，生成的手部部件无法精确接触物体表面对应区域。这表明当前的部件图编码和跨注意力融合机制在处理细粒度空间对应关系时仍有不足。

### 扩展实验

GraspDiff展现出良好的可扩展性：Fig. 9展示了物体尺度动态变化时的抓取生成能力，模型能够自适应调整手部姿态以保持合理的交互。Fig. 10进一步将方法扩展到**InterHand2.6M**数据集上的双手交互生成，证明了框架的通用性。

### 补充图表

![[assets/figures/papers/paper_list_l1811_GraspDiff_Grasping_Generation_for_Hand_Object_Interaction_with_Multimoda/figures/006_Table.jpg]]
*Table: II QUANTITATIVE COMPARISONS ON IN-DOMAIN OBJECTS FROM OBMAN TABLE III QUANTITATIVE COMPARISONS ON OUT-OF-DOMAIN OBJECTS FROM HO-3D*

![[assets/figures/papers/paper_list_l1811_GraspDiff_Grasping_Generation_for_Hand_Object_Interaction_with_Multimoda/figures/007_Table.jpg]]
*Table: IV QUANTITATIVE COMPARISONS ON OUT-OF-DOMAIN OBJECTS FROM FPHAB*

![[assets/figures/papers/paper_list_l1811_GraspDiff_Grasping_Generation_for_Hand_Object_Interaction_with_Multimoda/figures/015_Table.jpg]]
*Table: VII ABLATION STUDIES*

![[assets/figures/papers/paper_list_l1811_GraspDiff_Grasping_Generation_for_Hand_Object_Interaction_with_Multimoda/figures/012_Table.jpg]]
*Table: V GENERATION TIME COST (IN SECONDS)*

![[assets/figures/papers/paper_list_l1811_GraspDiff_Grasping_Generation_for_Hand_Object_Interaction_with_Multimoda/figures/011_Figure_6.jpg]]
*Figure 6: Human perceptual score distribution. Higher distribution in ”Strongly agree” shows that our method produces realistic and comparable performance compared to previous works. The left side corresponds to the in-domain objects and the right side corresponds to the out-of-domain objects*

![[assets/figures/papers/paper_list_l1811_GraspDiff_Grasping_Generation_for_Hand_Object_Interaction_with_Multimoda/figures/018_Figure_11.jpg]]
*Figure 11: Failure cases of our method. The left side shows that for different objects, the generated grasps sometimes tend to be similar. The right side shows failure cases of invalid conditional guidance, where the generated hand parts inaccurately contact with part maps on the object surface*

![[assets/figures/papers/paper_list_l1811_GraspDiff_Grasping_Generation_for_Hand_Object_Interaction_with_Multimoda/figures/002_Table.jpg]]
*Table: I FRAMEWORKS OF GRASPING GENERATION*

![[assets/figures/papers/paper_list_l1811_GraspDiff_Grasping_Generation_for_Hand_Object_Interaction_with_Multimoda/figures/009_Table.jpg]]
*Table: VI USER STUDY STATISTICS*



## 定位与知识库关联

### 1. 生成范式演进：从 VAE/GAN + 优化到潜在扩散

GraspDiff 的核心突破在于生成范式的根本性切换。此前的主流抓取生成方法普遍采用“VAE/GAN 编码 + 接触图迭代优化”的两阶段路线：

- **Grasping Field (GF)**（Karunratanakul et al., 3DV 2020）和 **GrabNet**（Taheri et al., ECCV 2020）代表了 VAE 路线的早期尝试，前者将手物交互建模为有符号距离场，后者利用基点点集（BPS）编码物体形状并通过 VAE 生成抓取姿态。这类方法的瓶颈在于生成多样性受限于 VAE 的连续潜在空间表达能力，且缺乏对接触约束的显式建模。

- **GraspTTA**（Jiang et al., ICCV 2021）在 VAE 基础上引入了测试时自适应（test-time adaptation），通过在线优化接触图来改善抓取质量。这虽然提升了物理合理性，但代价是推理速度显著下降——每次生成都需要额外的优化迭代。

- **ContactGen**（Liu et al., ICCV 2023）将接触图条件进一步细化为部件级接触图（part-wise contact maps），并通过 VAE 生成多样化的抓取候选。该方法在穿透体积（4.49 cm³）上达到了此前的最佳水平，但依然依赖于接触图的后处理优化，且对接触图精度高度敏感。

GraspDiff 的方法论创新在于**用扩散模型的迭代去噪过程直接替代传统优化例程**。如论文所述：“our key idea is that the iterative denoising steps inherent to diffusion models can supplant the iterative optimization routines in existing optimization methods”。这一替换消除了对接触图优化的依赖，使得生成过程从“编码 + 优化”的两阶段流水线转变为“潜在空间扩散 + 单步解码”的端到端范式。

### 2. 条件融合机制的升级

在条件信息的整合方式上，GraspDiff 相比基线方法实现了质的飞跃：

- **传统方法**（如 ContactGen）将接触图作为后处理优化目标或直接拼接到网络输入中，条件与生成过程之间缺乏深层的特征交互。

- **GraspDiff** 设计了专门的模态编码器（φ₀ 至 φ₃）分别处理点云、接触图、部件图和 2D 图像，并通过**交叉注意力机制**将这些多模态特征融合到去噪 U-Net 的中间层。如论文所述：“these extracted features are incorporated into the denoising process via a cross-attention mechanism in the denoising estimator Ψ”。这使得不同粒度的条件信息能够在去噪过程中持续引导生成方向，而非仅在输入或输出端施加约束。

消融实验证实了这一设计的有效性：将交叉注意力替换为简单拼接后，穿透体积从 4.32 cm³ 升至 4.73 cm³（Table VII），表明交叉注意力机制对多模态条件的深度融合至关重要。

### 3. 关键模块的消融贡献

GraspDiff 的流水线由四个核心模块构成，消融实验揭示了各自的贡献权重：

| 消融配置 | 穿透体积 (cm³) | 关键发现 |
|---------|---------------|---------|
| 完整 GraspDiff | 4.32 | 基准性能 |
| 移除 VAE（直接在参数空间扩散） | 5.85 | 性能严重退化，虚假多样性增加 |
| 移除 RefineNet | 4.93 | 性能下降但仍优于 ContactGen (4.49) |
| 拼接替代交叉注意力 | 4.73 | 条件融合效果减弱 |

**VAE 模块**的移除导致穿透体积飙升 35%，且生成样本的虚假多样性增加。这表明将 MANO 手部参数（61 维）嵌入到标准正态分布的潜在空间（64 维）是实现紧凑、可控扩散生成的必要条件——直接在原始参数空间扩散会因维度诅咒和分布不匹配导致生成质量急剧下降。

**RefineNet** 作为可选的轻量级优化模块，基于手物距离 D 对初始生成结果进行微调。移除后性能虽有下降（4.93 cm³），但仍优于 ContactGen 的最佳结果（4.49 cm³），说明扩散模型本身已能生成物理上合理的抓取姿态，RefineNet 起到锦上添花的作用。

### 4. 速度与质量的权衡突破

Table V 的生成时间对比揭示了 GraspDiff 在效率上的显著优势：扩散模型的单次前向去噪（0.795 秒）远快于依赖迭代优化的传统方法。这一速度优势源于扩散模型的推理过程是固定的前向计算，而非针对每个样本的自适应优化循环。

### 5. 适用边界与已知局限

尽管 GraspDiff 在多个基准上取得了领先性能，其方法存在以下适用边界：

1. **跨物体泛化的姿态坍缩**：对于训练数据中未见过的物体形状，模型有时会生成相似的抓取姿态（Fig. 11 左），尤其是在某些抓取模式在训练集中占主导地位时。这表明潜在扩散模型虽然能生成多样化的样本，但其多样性仍受限于训练分布。

2. **部件图条件的精度不足**：部件图（part map）引导的效果明显弱于点云和接触图等其他模态，生成的抓取无法精确匹配指定的接触区域（Fig. 11 右）。这暗示当前的交叉注意力机制在空间精度要求极高的细粒度条件上存在瓶颈。

3. **训练数据偏差**：模型在 ObMan 合成数据集上训练，该数据集的抓取姿态分布可能与真实交互数据（如 GRAB）存在偏差，导致生成结果中可能出现“强迫姿态”。

### 6. 开放问题

基于上述分析，以下几个方向值得后续工作关注：

- **极端未见形状的泛化**：当物体形状与训练集差异极大时，扩散模型的去噪轨迹是否会偏离合理流形？是否需要引入几何先验或测试时引导来约束生成空间？

- **扩散步数与质量 - 速度的帕累托前沿**：当前使用 T=1000 步的完整扩散过程，更少的采样步数（如通过 DDIM 加速）对生成质量和多样性的影响尚未被系统探索。

- **真实数据融合**：如何将 GRAB 等真实抓取数据集纳入训练，以减少合成数据带来的分布偏移，同时保持生成多样性？

- **部件图条件的空间精度提升**：是否需要引入显式的空间注意力或几何对齐损失来改善部件图引导的接触匹配精度？



## 原文 PDF

![[paperPDFs/TVCG_2024/GraspDiff_Grasping_Generation_for_Hand_Object_Interaction_with_Multimodal_Guided_Diffusion.pdf]]
