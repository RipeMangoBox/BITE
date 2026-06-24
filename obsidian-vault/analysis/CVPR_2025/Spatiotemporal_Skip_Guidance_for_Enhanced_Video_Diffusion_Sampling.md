---
title: Spatiotemporal Skip Guidance for Enhanced Video Diffusion Sampling
type: paper
paper_level: A
venue: CVPR
year: 2025
pdf_ref: paperPDFs/CVPR_2025/Spatiotemporal_Skip_Guidance_for_Enhanced_Video_Diffusion_Sampling.pdf
aliases:
- SSGS
- SSGEVDS
tags:
- CVPR_2025
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 跳过视频扩散模型中的时空层（残差块或注意力层），构造一个与主模型对齐的、质量略低的隐式弱模型，并利用该弱模型进行引导。
primary_logic: 通过选择性地跳过网络层，可以在不额外训练的情况下获得一个与主模型任务一致但性能稍差的弱模型；使用该弱模型进行引导，能在提升生成质量的同时保持样本多样性和动态特性。
claims:
- STG 显著提升 Mochi 和 Open‑Sora 的 VBench 成像质量，同时保持动态程度和运动平滑度，优于 CFG。
- STG 在 SVD 上降低 FVD 并提升动态程度，避免了 CFG 中质量–多样性权衡；FVD‑Imaging Quality 曲线显示 STG 在不牺牲多样性的前提下提升质量。
- 消融实验证实，空间引导和时序引导分别独立贡献，二者结合效果最佳。
- VBench T2V (Mochi) 上 Imaging Quality = 0.628
---

# Spatiotemporal Skip Guidance for Enhanced Video Diffusion Sampling

> [!tip] 核心洞察
> 通过选择性地跳过网络层，可以在不额外训练的情况下获得一个与主模型任务一致但性能稍差的弱模型；使用该弱模型进行引导，能在提升生成质量的同时保持样本多样性和动态特性。

| 字段 | 内容 |
|------|------|
| 中文题名 | 时空跳跃引导增强视频扩散采样 |
| 英文题名 | Spatiotemporal Skip Guidance for Enhanced Video Diffusion Sampling |
| 会议/期刊 | CVPR 2025 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2025/papers/Hyung_Spatiotemporal_Skip_Guidance_for_Enhanced_Video_Diffusion_Sampling_CVPR_2025_paper.pdf) · [Code](https://github.com/) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | Spatiotemporal Skip Guidance (STG) |
| Dataset | VBench T2V, VBench I2V |

> [!tip] 效果简介
> - VBench T2V (Mochi) 上，Imaging Quality 0.628 vs 0.524 (CFG) (+0.104)。
> - VBench T2V (Open‑Sora) 上，Imaging Quality 0.606 vs 0.561 (CFG) (+0.045)。
> - VBench I2V (SVD) 上，FVD (↓) 128.7 vs 151.3 (CFG) (−22.6)。

## 概述

视频扩散模型在生成高质量视频方面取得了显著进展，但其采样过程仍面临一个核心瓶颈：现有的引导方法（如 **Classifier-Free Guidance, CFG**，Ho et al., arXiv 2022）在提升生成质量的同时，往往会抑制样本的多样性并削弱视频的动态特性。此外，**Autoguidance** 等方法虽能缓解这一权衡，却需要对弱模型进行额外训练，难以直接应用于大规模视频扩散模型。

针对上述问题，本文提出 **时空跳跃引导（Spatiotemporal Skip Guidance, STG）**。其核心思路是：通过在视频扩散模型的采样过程中选择性地跳过特定的时空层（残差块或注意力层），构造一个与主模型任务对齐、但质量略低的隐式弱模型，并利用该弱模型进行引导。该方法无需额外训练或外部模型，即可在提升生成质量的同时，有效保持样本的多样性和动态特性。

在方法定位上，STG 属于扩散模型引导采样技术的改进。与 CFG 依赖独立无条件模型、Autoguidance 依赖单独训练的弱模型不同，STG 的弱模型直接通过对主模型进行自扰动获得，其引导方程可表示为：

$$\tilde{\epsilon}_{\theta}^{w}(x_t) = \epsilon_{\theta}(x_t) + w(\epsilon_{\theta}(x_t) - \epsilon_{\theta}^{b}(x_t))$$

其中 $\epsilon_{\theta}^{b}$ 为扰动后的弱模型预测。扰动方式包括跳过残差块（STG‑R）或跳过注意力计算（STG‑A），且同时作用于空间与时间维度。

实验结果表明，STG 在多个视频扩散模型和基准上均取得显著提升：在 **Mochi** 和 **Open‑Sora** 的 VBench T2V 基准上，成像质量（Imaging Quality）分别从 0.524 和 0.561 提升至 0.628 和 0.606（Table 1）；在 **SVD** 上，FVD 从 151.3 降至 128.7，动态程度（Dynamic Degree）从 0.562 提升至 0.694（Table 2）。消融实验进一步证实，空间引导与时序引导各自独立贡献，二者结合效果最佳（Table 4）。

## 背景与动机

扩散模型已成为视觉生成的核心范式，其采样质量高度依赖引导机制。当前最主流的 **Classifier-Free Guidance (CFG)**（Ho et al., arXiv 2022）通过外推条件预测与无条件预测之差来强化条件信号，但存在一个根本性困境：增大引导尺度虽然提升成像质量，却会压缩样本多样性并抑制视频中的动态表现。这一质量-多样性权衡在视频生成任务中尤为致命——过强的 CFG 往往导致生成视频趋于静态、丧失运动信息。

Autoguidance 方法尝试通过引入一个独立训练的弱模型来缓解上述问题，但其前提是需要对弱模型进行额外训练。对于当前的大规模视频扩散模型而言，这一要求既不经济也不实际：重新训练或微调一个与主模型对齐的弱模型意味着高昂的计算开销和工程复杂度。

论文 **Spatiotemporal Skip Guidance for Enhanced Video Diffusion Sampling**（CVPR 2025）正是针对这一瓶颈提出解决方案。其核心动机源于一个关键观察：视频扩散模型中的时空层（残差块或注意力层）承载着生成质量的关键信息，如果选择性地跳过这些层，就可以在无需任何额外训练的条件下，直接从主模型的前向传播中构造出一个与主模型任务对齐、但性能稍低的隐式弱模型。利用该弱模型进行引导，理论上能够在提升质量的同时保持多样性和动态特性，从而突破 CFG 的质量-多样性僵局。

## 核心创新

### 瓶颈突破：从“外部弱模型”到“隐式自扰动”

现有扩散模型采样引导方法面临一个根本性困境：**Classifier-Free Guidance (CFG)**（Ho et al., arXiv 2022）通过引入无条件模型作为弱模型来提升生成质量，但这一操作会显著降低样本多样性并抑制视频动态特性；**Autoguidance** 虽可缓解质量–多样性权衡，却需要对弱模型进行额外训练，这对参数规模动辄数十亿的大规模视频扩散模型而言代价高昂，难以实际部署。

STG 的核心突破在于**彻底消除了对外部弱模型的依赖**。它不引入独立的无条件模型，也不进行任何额外训练，而是直接在主模型的前向传播中通过选择性跳过时空层，构造出一个与主模型任务对齐、但质量略低的“隐式弱模型”。这一设计使得引导方向始终沿着“提升质量”的单一维度，避免了 CFG 中弱/强模型在质量和多样性两个维度上同时偏离的问题（参见 Figure 2 的概念对比）。

### 关键改动槽位（Changed Slots）

| 改动维度 | 基线方法（CFG / Autoguidance） | STG 方案 | 证据锚点 |
|---------|-------------------------------|---------|---------|
| **弱模型来源** | 独立的无条件模型（CFG）或单独训练的弱模型（Autoguidance） | 通过跳跃主模型中的时空层得到的隐式弱模型，无需额外训练 | Sec. 4.1, Sec. 4.3, Eq. 13 |
| **引导方程** | $\tilde{\epsilon}_{\theta}^{\lambda} = \epsilon_{\theta}(x_t) + \lambda(\epsilon_{\theta}(x_t) - \epsilon_{\theta}(x_t|\phi))$ | $\tilde{\epsilon}_{\theta}^{w}(x_t) = \epsilon_{\theta}(x_t) + w(\epsilon_{\theta}(x_t) - \epsilon_{\theta}^{b}(x_t))$，其中 $\epsilon_{\theta}^{b}$ 为扰动前向传播的结果 | Eq. 6 vs Eq. 13 |
| **扰动方式** | 无（CFG 不扰动主模型）；或对图像注意力图替换为单位阵（PAG/SEG，仅限于 2D 空间注意力） | 跳过残差块（STG‑R）或跳过注意力计算（STG‑A），同时作用于空间和时间（或 3D 时空）层 | Sec. 4.3, Eq. 14–17 |

### 创新机理：层跳跃如何构造“对齐的弱模型”

STG 的隐式弱模型通过两种互补的扰动方式实现：

- **残差跳跃（STG‑R）**：将残差块的输出直接设为输入特征，即 $\mathrm{Res}'(z_l) = z_{l+1} = z_l$（Eq. 15）。这等效于跳过该层的非线性变换，使模型容量局部降低。
- **注意力跳跃（STG‑A）**：将自注意力计算中的注意力矩阵替换为单位阵，即 $\mathrm{SA}'(Q,K,V) = \mathbf{I}V$（Eq. 17）。这等价于取消 token 间的信息交互，使每个 token 仅保留自身特征。

论文的一个重要发现是：**跳过网络层是构造对齐弱模型的有效途径**。与引入外部模型不同，层跳跃产生的弱模型与主模型共享绝大部分参数，其预测偏差自然地指向“质量提升”方向，而非随机偏离。这一特性是 STG 能在提升成像质量的同时保持视频多样性和动态程度的关键原因——引导向量 $\epsilon_{\theta}(x_t) - \epsilon_{\theta}^{b}(x_t)$ 始终沿着数据流形上质量递增的方向。

### 从空间到时空：扰动维度的扩展

此前的方法（如 PAG、SEG）仅在 2D 空间注意力上施加扰动，而 STG 将扰动扩展至**时间注意力层**和**3D 时空注意力层**。对于采用因子化时空注意力的架构（如 SVD），STG 分别对空间和时间注意力施加独立扰动，对应的评分函数为：

$$
\nabla_{x_t}\log\tilde{p}_\theta(x_t|y_g) = \nabla_{x_t}\log p_\theta(x_t) + w\nabla_{x_t}(\log p_\theta(x_t) - \log p_\theta(x_t|y_{sb})) + w\nabla_{x_t}(\log p_\theta(x_t) - \log p_\theta(x_t|y_{tb}))
$$

这一因子化设计允许独立调节空间质量和时序动态的引导强度，为视频生成提供了更精细的控制维度。消融实验（Table 4）证实，空间引导和时序引导各自独立贡献，二者结合效果最优——在 SVD 上，单独添加空间引导使 FVD 从 151.3 降至 133.8，进一步添加时序引导后降至 128.7。

### 与基线方法的本质差异

| 特性 | CFG | Autoguidance | STG |
|-----|-----|-------------|-----|
| 弱模型来源 | 无条件模型 | 单独训练的弱模型 | 主模型自扰动 |
| 额外训练 | 需要（无条件模型） | 需要 | **不需要** |
| 质量–多样性权衡 | 明显 | 缓解 | **基本消除** |
| 动态保持 | 受抑制 | 部分保持 | **保持** |
| 扰动维度 | 无扰动 | 无扰动 | 空间 + 时间 |
| 计算开销 | 2× 前向传播 | 2× 前向传播 | 2× 前向传播（可比） |

STG 的创新本质在于：**用“跳过层”替代“换模型”**，以零额外训练成本实现了与 Autoguidance 类似的对齐引导效果，同时通过时空维度的扰动扩展，在视频生成这一高维序列任务上展现出 CFG 无法达到的质量–多样性平衡。

## 整体框架

STG 的整体采样流程围绕一个核心洞察构建：**通过选择性跳过视频扩散模型中的时空层，可以在不引入额外训练或外部模型的前提下，获得一个与主模型“对齐”的隐式弱模型**，并利用该弱模型进行引导（guidance），从而在提升生成质量的同时保持样本多样性与动态特性。

### 核心瓶颈与因果机制

现有扩散模型采样引导方法（如 **CFG**，Ho et al., arXiv 2022）面临一个根本性权衡：提高引导强度可以增强成像质量，但会显著抑制样本多样性和视频动态。**Autoguidance** 虽然通过引入一个独立训练的弱模型缓解了这一问题，但其额外训练成本使其难以直接应用于大规模视频扩散模型。STG 的关键创新在于**将“弱模型”的构造从“训练”转化为“扰动”**——直接在主模型的前向传播中施加时空扰动，生成一个质量略低但任务方向一致的隐式弱模型，从而绕开了额外训练这一瓶颈。

### Pipeline 模块与数据流

STG 的采样流程由三个核心模块串联构成，其输入输出关系如下：

1.  **时空扰动模块（隐式弱模型构造）**
    -   **输入**：当前噪声隐变量 $x_t$ 与主模型 $\epsilon_\theta$。
    -   **处理**：在主模型的一次额外前向传播中，选择性地跳过特定的时空层，得到弱模型输出 $\epsilon_\theta^b(x_t)$。论文提出了两种具体的扰动方式：
        -   **STG‑R（残差跳跃）**：将残差块的输出直接设为输入，即 $\mathrm{Res}'(z_l) = z_{l+1} = z_l$（Eq. 15）。
        -   **STG‑A（注意力跳跃）**：将自注意力矩阵替换为单位阵，即 $\mathrm{SA}'(Q,K,V) = \mathbf{I}V$（Eq. 17），等价于跳过注意力加权。
    -   **输出**：弱模型的噪声预测 $\epsilon_\theta^b(x_t)$。

2.  **引导组合模块**
    -   **输入**：主模型预测 $\epsilon_\theta(x_t)$ 与弱模型预测 $\epsilon_\theta^b(x_t)$。
    -   **处理**：按引导权重 $w$ 组合两者，形成最终的去噪估计：
        $$\tilde{\epsilon}_{\theta}^{w}(x_t) = \epsilon_{\theta}(x_t) + w(\epsilon_{\theta}(x_t) - \epsilon_{\theta}^{b}(x_t)) \quad \text{(Eq. 13)}$$
    -   **输出**：引导后的噪声预测 $\tilde{\epsilon}_{\theta}^{w}(x_t)$，用于下一步去噪采样。

3.  **流形约束模块（可选）**
    -   **输入**：引导后的去噪轨迹。
    -   **处理**：通过重缩放（rescaling）和重启（restart）采样策略，防止高引导强度下样本偏离数据流形。
    -   **输出**：受约束的采样路径。

### 空间与时序引导的因子化

对于采用**因子化时空注意力**的架构（如 SVD），STG 进一步将扰动分解为空间引导和时序引导两个独立分量。其评分函数可写为：

$$\nabla_{x_t}\log\tilde{p}_\theta(x_t|y_g) = \nabla_{x_t}\log p_\theta(x_t) + w\nabla_{x_t}(\log p_\theta(x_t) - \log p_\theta(x_t|y_{sb})) + w\nabla_{x_t}(\log p_\theta(x_t) - \log p_\theta(x_t|y_{tb})) \quad \text{(Eq. 19)}$$

对应的去噪估计为：

$$\tilde{\epsilon}_{\theta}^{w}(x_t) = \epsilon_{\theta}(x_t) + w_1 \Delta_s + w_2 \Delta_t \quad \text{(Eq. 20)}$$

其中 $\Delta_s = \epsilon_\theta(x_t) - \epsilon_\theta^s(x_t)$、$\Delta_t = \epsilon_\theta(x_t) - \epsilon_\theta^t(x_t)$ 分别为空间和时序引导分量，$w_1$、$w_2$ 为各自独立的引导尺度。为处理空间与时间扰动之间可能存在的相关性，论文还提出了正交化变体（Eq. 21），将时序分量与空间分量正交化以避免重复计数。

### 与 CFG 的本质区别

从引导方程的形式看，STG 与 CFG（$\tilde{\epsilon}_\theta^\lambda = \epsilon_\theta(x_t) + \lambda(\epsilon_\theta(x_t) - \epsilon_\theta(x_t|\phi))$）结构相似，但弱模型的来源截然不同：CFG 依赖一个独立的无条件模型（需额外训练或联合训练），而 STG 的弱模型通过对主模型自身施加时空扰动获得，**无需任何额外训练**。这一差异使得 STG 能够直接应用于任意预训练视频扩散模型，且计算开销与 CFG 可比。

### 补充图表

![[assets/figures/papers/paper_list_l5_https_openaccess_thecvf_com_content_CVPR2025_papers_Hyung_Spatiotemporal/figures/001_Figure_2.jpg]]
*Figure 2: Comparison between CFG and STG, with the band conceptually representing the noisy data manifold. In STG, the weak model and the main model are aligned along the direction of increasing quality. In contrast, the two models in CFG differ not only in quality but also in aspects such as diversity and prompt alignment capabilities*

## 核心模块与公式推导

### 方法总览：隐式弱模型引导范式

STG 的核心思想是**在不引入额外模型或额外训练的前提下，通过扰动主模型的前向传播过程构造一个“隐式弱模型”**，并利用该弱模型进行引导采样。与 CFG 需要独立训练无条件模型、Autoguidance 需要单独训练弱模型不同，STG 的弱模型直接来源于主模型本身——通过选择性地跳过视频扩散模型中的时空层，使网络输出一个质量略低但与主模型在质量提升方向上高度对齐的预测。

这一设计的关键洞察在于（Figure 2 概念示意）：CFG 中条件模型与无条件模型在质量和多样性两个维度上均存在差异，导致引导时不可避免地牺牲多样性换取质量；而 STG 的弱模型与主模型在“质量提升方向”上对齐，即弱模型仅仅是在生成质量上略逊于主模型，但其样本分布的其他特性（多样性、动态程度）与主模型保持一致。因此，沿该方向施加引导可以在提升质量的同时保持样本的多样性和动态特性。

### 核心模块一：时空扰动模块

时空扰动模块负责从主模型生成弱模型的输出预测 $\epsilon_\theta^b(x_t)$。该模块通过两种互补的跳跃策略实现：

**残差跳跃（STG‑R）**：对于网络中的残差块，将其输出直接设为输入，即跳过残差变换：

$$\mathrm{Res}'(z_l) = z_{l+1} = z_l$$

其中 $z_l$ 为第 $l$ 层的输入特征，$f_l$ 为残差块内的变换函数。原本的残差计算 $\mathrm{Res}(z_l) = f_l(z_l) + z_l$ 被简化为恒等映射，使网络在该层失去非线性建模能力，从而获得弱化的输出。

**注意力跳跃（STG‑A）**：对于自注意力或交叉注意力层，将注意力加权矩阵替换为单位阵，即跳过注意力计算：

$$\mathrm{SA}'(Q, K, V) = \mathbf{I}V$$

这等价于让每个查询位置直接取所有值向量的平均，消除了注意力机制对特征的选择性聚合能力，同样产生弱化的模型输出。

两种跳跃策略均可作用于空间注意力层、时间注意力层或 3D 全注意力层。具体选择取决于目标视频扩散模型的架构：对于使用因子化时空注意力的模型（如 SVD），可分别对空间和时间注意力施加扰动；对于使用 3D 全注意力的模型（如 Mochi 的 AsymmDiT），扰动作用于整个注意力层。

### 核心模块二：引导组合模块

引导组合模块将主模型预测 $\epsilon_\theta(x_t)$ 与弱模型预测 $\epsilon_\theta^b(x_t)$ 按引导权重 $w$ 组合，形成最终的去噪估计：

$$\tilde{\epsilon}_{\theta}^{w}(x_t) = \epsilon_{\theta}(x_t) + w(\epsilon_{\theta}(x_t) - \epsilon_{\theta}^{b}(x_t))$$

该公式与 CFG 的引导方程在形式上一致，但本质区别在于 $\epsilon_\theta^b$ 的来源：CFG 使用独立训练的无条件模型，而 STG 使用通过自扰动得到的隐式弱模型。引导权重 $w$ 控制弱模型与主模型差异的放大程度——$w$ 越大，生成结果的质量提升越显著（色彩更鲜艳、细节更丰富），同时由于弱模型与主模型在多样性维度上对齐，FVD 不会随之升高（Figure 4 验证了这一特性）。

### 核心模块三：因子化空间‑时序引导（可选扩展）

对于使用因子化时空注意力的架构，STG 可进一步分解为空间引导和时序引导两个独立分量。假设空间扰动和时序扰动对模型输出的影响相互独立，则引导评分函数可写为：

$$\nabla_{x_t}\log\tilde{p}_\theta(x_t|y_g) = \nabla_{x_t}\log p_\theta(x_t) + w\nabla_{x_t}(\log p_\theta(x_t) - \log p_\theta(x_t|y_{sb})) + w\nabla_{x_t}(\log p_\theta(x_t) - \log p_\theta(x_t|y_{tb}))$$

对应的去噪估计为：

$$\tilde{\epsilon}_{\theta}^{w}(x_t) = \epsilon_{\theta}(x_t) + w_1(\epsilon_{\theta}(x_t) - \epsilon_{\theta}^{s}(x_t)) + w_2(\epsilon_{\theta}(x_t) - \epsilon_{\theta}^{t}(x_t))$$

其中 $\epsilon_{\theta}^{s}$ 和 $\epsilon_{\theta}^{t}$ 分别为仅施加空间扰动和仅施加时序扰动得到的弱模型预测，$w_1$ 和 $w_2$ 为各自独立的引导尺度。

当空间扰动与时序扰动存在相关性时，上述独立假设可能导致引导分量重叠。为此，论文进一步提出**正交化 STG**，将时序引导分量与空间引导分量正交化以避免重复计数：

$$\tilde{\epsilon}_{\theta}^{w}(x_t) = \epsilon_{\theta}(x_t) + w_1 \Delta_s + w_2 \big( \Delta_t - \frac{\langle \Delta_s, \Delta_t \rangle}{\|\Delta_s\|^2} \Delta_s \big)$$

其中 $\Delta_s = \epsilon_{\theta}(x_t) - \epsilon_{\theta}^{s}(x_t)$，$\Delta_t = \epsilon_{\theta}(x_t) - \epsilon_{\theta}^{t}(x_t)$。该正交化处理从时序引导向量中减去其在空间引导方向上的投影，确保两个引导分量互不冗余。

### 流形约束（可选）

为防止高引导尺度下样本偏离数据流形，STG 沿用了扩散模型中常见的**重缩放（rescaling）和重启（restart）**采样策略，对去噪过程中的噪声预测进行规范化处理，维持样本在数据流形附近的合理分布。该模块为可选组件，所有对比实验均在相同设置下进行以保证公平性。

### 关键公式汇总

| 公式 | 表达式 | 含义 | 锚点 |
|------|--------|------|------|
| STG 噪声预测 | $\tilde{\epsilon}_{\theta}^{w}(x_t) = \epsilon_{\theta}(x_t) + w(\epsilon_{\theta}(x_t) - \epsilon_{\theta}^{b}(x_t))$ | 使用隐式弱模型进行引导的去噪估计 | Eq. (13) |
| 残差跳跃 | $\mathrm{Res}'(z_l) = z_{l+1} = z_l$ | 跳过残差块，直接传递输入特征 | Eq. (15) |
| 注意力跳跃 | $\mathrm{SA}'(Q,K,V) = \mathbf{I}V$ | 跳过注意力加权，等同于将注意力矩阵替换为单位阵 | Eq. (17) |
| 因子化空间‑时序引导评分 | $\nabla_{x_t}\log\tilde{p}_\theta(x_t\|y_g) = \nabla_{x_t}\log p_\theta(x_t) + w\nabla_{x_t}(\log p_\theta(x_t) - \log p_\theta(x_t\|y_{sb})) + w\nabla_{x_t}(\log p_\theta(x_t) - \log p_\theta(x_t\|y_{tb}))$ | 分别施加空间和时序扰动后的评分函数 | Eq. (19) |
| 正交化 STG 去噪 | $\tilde{\epsilon}_{\theta}^{w}(x_t) = \epsilon_{\theta}(x_t) + w_1 \Delta_s + w_2 ( \Delta_t - \frac{\langle \Delta_s, \Delta_t \rangle}{\|\Delta_s\|^2} \Delta_s )$ | 将时序与空间引导分量正交化，避免重复计数 | Eq. (21) |

## 实验与分析

### 主结果：T2V 与 I2V 基准

STG 在 VBench 文本生成视频（T2V）和图像生成视频（I2V）基准上，相比 CFG 均取得了显著的成像质量提升，同时避免了质量–多样性权衡。Table 1 汇总了 Mochi 和 Open‑Sora 两个 T2V 模型的结果：Mochi 的 Imaging Quality 从 CFG 的 0.524 提升至 STG 的 0.628（+0.104），Open‑Sora 从 0.561 提升至 0.606（+0.045）。在 I2V 任务上，Table 2 显示 SVD 的 FVD 从 CFG 的 151.3 降至 STG 的 128.7（−22.6），同时 Dynamic Degree 从 0.562 显著提升至 0.694（+0.132），表明 STG 在增强画面质量的同时，保持了甚至增强了视频的动态特性。

![[assets/figures/papers/paper_list_l5_https_openaccess_thecvf_com_content_CVPR2025_papers_Hyung_Spatiotemporal/figures/002_Table_1.jpg]]
*Table 1: Quantitative results for Mochi [33] and Open-Sora [38] on VBench [15] T2V benchmarks*

![[assets/figures/papers/paper_list_l5_https_openaccess_thecvf_com_content_CVPR2025_papers_Hyung_Spatiotemporal/figures/003_Table_2.jpg]]
*Table 2: Quantitative results for SVD [4] on FVD, IS, and VBench [15] I2V benchmarks*

Figure 4 进一步揭示了引导尺度对质量–多样性权衡的影响。随着引导尺度增大，CFG 的 FVD 急剧上升（多样性下降），而 STG 的 FVD 保持稳定甚至略有下降，同时 Imaging Quality 持续提升。这说明 STG 的隐式弱模型与主模型在“质量提升方向”上高度对齐，引导过程不会将样本推离数据流形，从而在提升质量的同时维持多样性。

![[assets/figures/papers/paper_list_l5_https_openaccess_thecvf_com_content_CVPR2025_papers_Hyung_Spatiotemporal/figures/005_Figure_4.jpg]]
*Figure 4: Comparison of CFG and STG across varying scales in terms of Imaging Quality and FVD*

### 消融实验

#### 空间引导与时序引导的贡献

Table 4 展示了在 SVD 上分别施加空间引导和时序引导的消融结果。仅添加空间引导时，FVD 从 CFG 的 151.3 降至 133.8；进一步叠加时序引导后，FVD 进一步降至 128.7。Imaging Quality 和 Dynamic Degree 也呈现递增趋势。这表明空间扰动和时序扰动各自独立贡献，二者结合产生叠加效应，验证了论文中因子化空间‑时序引导设计的有效性。

![[assets/figures/papers/paper_list_l5_https_openaccess_thecvf_com_content_CVPR2025_papers_Hyung_Spatiotemporal/figures/008_Table_4.jpg]]
*Table 4: Ablation study results on SVD [4] factorized attention, showing the impact of adding spatial and temporal guidance*

#### 扰动方式的选择：STG‑R 与 STG‑A

Table 3 对比了两种弱模型构造方式——残差跳跃（STG‑R）和注意力跳跃（STG‑A）——在三个模型上的表现。在 Mochi（深层 Transformer 架构，AsymmDiT）上，STG‑R 的 Imaging Quality（0.628）和 Aesthetic Quality（0.554）均优于 STG‑A；而在 Open‑Sora 和 SVD 上，STG‑A 表现更佳。这一差异与模型架构和层深度相关：深层 Transformer 中残差块的跳跃能产生更合适的弱模型，而注意力跳跃在较浅或 UNet 架构中更为有效。

![[assets/figures/papers/paper_list_l5_https_openaccess_thecvf_com_content_CVPR2025_papers_Hyung_Spatiotemporal/figures/007_Table_3.jpg]]
*Table 3: Comparison of STG-R (residual skip) and STG-A (attention skip) across Mochi [33], Open-Sora [38], and SVD [4]. STG-R shows stronger performance on Mochi, while STG-A yields better results on Open-Sora and SVD*

#### 引导尺度的影响

Figure 3 展示了 Mochi 在不同 STG 尺度下的生成帧序列。随着引导尺度 $w$ 增大，画面色彩更鲜艳、细节更丰富，但视频的语义一致性和动态自然度未出现退化。这与 Figure 4 的定量趋势一致：STG 的 FVD 不随尺度增大而升高，避免了 CFG 中常见的“质量提升以多样性为代价”的现象。

![[assets/figures/papers/paper_list_l5_https_openaccess_thecvf_com_content_CVPR2025_papers_Hyung_Spatiotemporal/figures/004_Figure_3.jpg]]
*Figure 3: Selected frames from videos generated by Mochi [33] with increasing STG scales*

### 计算开销与公平性说明

所有对比实验均采用相同的重缩放（rescaling）和重启（restart）采样设置，确保仅引导方法不同。STG 不引入额外训练，其计算开销与 CFG 可比——仅需一次额外的前向传播（弱模型预测），且该前向传播可通过层跳过实现部分计算节省。

### 失败模式与局限性

尽管 STG 在多个模型和基准上表现出一致的优势，但其性能依赖于引导尺度和跳跃层的选择。最优配置因模型架构而异，目前需要启发式调参确定。此外，空间与时序扰动之间的独立性假设在更复杂的跨帧关联下可能不完全成立，论文提出的正交化处理（Eq. 21）的实际效果尚需在更多场景下验证。视频质量的提升也可能被滥用，需负责任地使用该技术。

### 补充图表

![[assets/figures/papers/paper_list_l5_https_openaccess_thecvf_com_content_CVPR2025_papers_Hyung_Spatiotemporal/figures/006_Figure_5.jpg]]
*Figure 5: Qualitative comparison between CFG and STG on videos generated by Mochi [33]*

## 方法谱系与知识库定位

### 与现有引导范式的结构性对比

**STG 的核心定位**：现有扩散模型的采样引导方法在提升生成质量时普遍面临质量–多样性权衡（quality–diversity trade-off），且该问题在视频扩散模型中因时序动态的引入而更加突出。STG 通过“自扰动隐式弱模型”的设计，在不引入额外训练的前提下，实现了对视频生成质量与多样性的同步提升。

**与 CFG 的根本差异**：
- **Classifier-Free Guidance (CFG)**（Ho et al., arXiv 2022）通过一个独立训练的无条件模型作为弱模型进行引导。在视频扩散中，CFG 的弱模型与主模型在“质量”和“多样性”两个维度上均存在偏差，导致增大引导尺度时虽然提升成像质量，却显著抑制动态程度和样本多样性。
- **STG** 的弱模型通过对主模型进行时空层跳跃（spatiotemporal skip）直接构造。由于扰动仅改变模型容量而不改变任务分布，弱模型与主模型沿“质量提升方向”对齐（Figure 2 概念示意），从而在引导时仅放大质量差异，而不引入多样性偏差。定量上，SVD 的 FVD 从 CFG 的 151.3 降至 STG 的 128.7，同时 Dynamic Degree 从 0.562 提升至 0.694（Table 2），证实 STG 有效规避了 CFG 的质量–多样性权衡。

**与 Autoguidance 的区别**：
- Autoguidance 同样利用弱模型进行引导以缓解 CFG 的多样性损失，但其弱模型需要单独训练（如使用更小容量或更少训练步数的模型）。对于参数量达 10B 的 Mochi 等大规模视频扩散模型，额外训练弱模型的成本不可接受。
- STG 通过“跳过网络层”隐式获得弱模型，无需任何额外训练，计算开销与 CFG 相当（仅增加一次扰动前向传播），使其可直接应用于任意预训练视频扩散模型。

**与 PAG/SEG 的边界**：
- PAG（Perturbed Attention Guidance）和 SEG（Self-Enhanced Guidance）同样通过对主模型施加扰动来构造弱模型，但其扰动方式仅限于将图像自注意力矩阵替换为单位阵，仅作用于 2D 空间注意力层。
- STG 将扰动扩展至**时空联合域**：残差跳跃（STG‑R）跳过整个残差块，注意力跳跃（STG‑A）跳过注意力计算，且同时作用于空间层和时间层（或 3D 时空注意力层）。这一扩展使 STG 能够独立控制空间质量和时序动态，为视频扩散模型提供了更精细的引导维度。

### 方法谱系中的定位

STG 处于“免训练引导采样”与“视频扩散模型”两条研究线的交汇点：

1. **免训练引导采样线**：从 CFG 到 PAG、SEG，再到 STG，扰动方式从“独立弱模型”演进为“自扰动隐式弱模型”，扰动域从纯空间扩展至时空联合。
2. **视频扩散模型线**：STG 在 Mochi（10B AsymmDiT）、Open‑Sora（1.1B STDiT）、SVD（1.5B UNet）三种不同架构上均有效，表明其方法不依赖于特定模型结构，具有较好的泛化性。

### 适用边界与局限

**架构依赖性**：
- STG‑R（残差跳跃）在 Mochi（深度 Transformer 架构）上表现更强（Imaging Quality 0.628），而 STG‑A（注意力跳跃）对 SVD 和 Open‑Sora 更有效（Table 3）。这表明最优跳跃策略与模型架构和层深度相关，用户需根据具体模型进行启发式选择。
- 论文未给出自动选择跳跃层和引导尺度的机制，当前依赖人工调参。

**超参数敏感性**：
- 引导尺度 $w$ 和跳跃层的选择共同决定 STG 的性能。增大 $w$ 可使画面色彩更鲜艳、细节更丰富（Figure 3），但过大的 $w$ 可能导致伪影或偏离数据流形。论文引入了重缩放（rescaling）和重启（restart）采样作为流形约束（Sec. 4.4），但并未完全消除超参数敏感性。

**独立性假设的局限**：
- 空间引导和时序引导的因子化公式（Eq. 19）基于空间扰动与时间扰动独立的假设。论文提出了正交化处理（Eq. 21）以消除二者间的冗余，但该处理在更复杂的跨帧关联场景下的有效性尚需进一步验证。

**伦理风险**：
- 视频生成质量的提升可能被滥用于制造深度伪造内容，需负责任地使用该技术。

### 开放问题

1. **自动层选择与尺度优化**：如何为新的视频扩散模型架构自动或高效地确定最优的跳跃层和引导尺度，减少人工调参成本？
2. **时空扰动独立性的鲁棒性**：空间与时序扰动之间的独立性假设在更复杂的跨帧关联（如大范围运动、遮挡）下是否仍然成立？正交化处理的实际增益边界在哪里？
3. **与其他引导方法的复合**：STG 能否与基于文本的引导（如文本 CFG）或基于能量的引导进行有效复合，进一步提升可控生成能力？
4. **更广泛架构的验证**：STG 在基于 3D 全注意力（非因子化时空注意力）的视频扩散模型上的表现如何？论文仅在 SVD 的因子化注意力上验证了空间/时序引导的独立贡献（Table 4），在完全 3D 注意力架构下的行为尚待探索。

## 原文 PDF

![[paperPDFs/CVPR_2025/Spatiotemporal_Skip_Guidance_for_Enhanced_Video_Diffusion_Sampling.pdf]]