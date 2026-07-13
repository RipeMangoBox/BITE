---
title: "StyleMotif: Multi-Modal Motion Stylization using Style-Content Cross Fusion"
type: paper
paper_level: A
venue: ICCV
year: 2025
pdf_ref: paperPDFs/ICCV_2025/StyleMotif_Multi_Modal_Motion_Stylization_using_Style_Content_Cross_Fusion.pdf
project_link: https://stylemotif.github.io
code_link: null
aliases:
- StyleMotif
tags:
- ICCV_2025
- topic/vision_multimodal_applications
- topic/representation_self_supervised_transfer
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 将双分支架构替换为单分支扩散框架，并通过风格-内容交叉归一化（Style-Content Cross Normalization）以统计变换方式直接向内容特征中注入风格信息，同时利用多模态对比学习对齐风格编码器与ImageBind，实现多模态风格控制。
primary_logic: 风格特征可以通过内容特征的均值与方差进行归一化后，以加性融合方式注入扩散去噪过程，无需额外可学习参数；多模态对比学习将风格编码器与预训练多模态模型（ImageBind）统一至共享特征空间，从而支持文本、图像、音频、视频等多种风格输入。
claims:
- STYLEMOTIF采用单分支结构，以统计变换（风格-内容交叉归一化）替代SMooDi的零初始化线性层分支，直接在主去噪分支内进行风格注入，融合仅在单个去噪块后执行一次。
- 单分支设计使推理速度提升22.5%，可学习参数减少43.9%，显著超越SMooDi的双分支结构。
- 在运动引导风格化任务上，STYLEMOTIF的SRA达到77.65，FID为1.551，均优于所有基线方法，SRA相对SMooDi提升5.23%。
- 多模态对齐使模型能够从文本、图像、视频、音频中提取风格特征，并检索最相似的运动风格特征进行引导，实现统一的多模态风格控制。
---

# StyleMotif: Multi-Modal Motion Stylization using Style-Content Cross Fusion

> [!tip] 核心洞察
> 风格特征可以通过内容特征的均值与方差进行归一化后，以加性融合方式注入扩散去噪过程，无需额外可学习参数；多模态对比学习将风格编码器与预训练多模态模型（ImageBind）统一至共享特征空间，从而支持文本、图像、音频、视频等多种风格输入。

| 字段 | 内容 |
|------|------|
| 中文题名 | StyleMotif：基于风格-内容交叉融合的多模态运动风格化 |
| 英文题名 | StyleMotif: Multi-Modal Motion Stylization using Style-Content Cross Fusion |
| 会议/期刊 | ICCV 2025 |
| Links | [Project](https://stylemotif.github.io) · [paper](https://arxiv.org/abs/2503.21775) |
| Topic | #topic/vision_multimodal_applications #topic/representation_self_supervised_transfer #topic/vision_multimodal_applications/image_and_video_generation |
| Method | STYLEMOTIF |
| Dataset | Motion-Guided Stylization, Text-Guided Stylization, Motion Style Transfer |

> [!tip] 效果简介
> - Motion-Guided Stylization (100STYLE/HumanML3D) 上，SRA (Style Recognition Accuracy) 77.65 vs 72.42 (SMooDi) (+5.23)。
> - Text-Guided Stylization (HumanML3D + text style descriptions) 上，SRA 56.71 vs 4.82 (ChatGPT+MLD) (+51.89)。
> - Motion Style Transfer (HumanML3D) 上，SRA 68.81 vs 65.15 (previous best) (+3.66)。

## 概要

**问题瓶颈**：现有风格化运动生成方法（如 **SMooDi**，Zhong et al., ECCV 2024）普遍采用双分支架构，通过在每个去噪块中添加零初始化线性层作为并行风格分支来注入风格条件。这种设计虽然有效，但显著增加了模型复杂度和训练开销，且风格输入局限于单一运动模态，限制了多模态灵活性与生成效率。

**核心思路**：STYLEMOTIF 提出将双分支架构替换为**单分支扩散框架**，核心创新在于**风格-内容交叉归一化**——以内容特征的均值与方差对风格特征进行统计变换后，通过加性融合方式直接注入主去噪分支，无需额外可学习参数。同时，通过多模态对比学习将风格编码器与预训练多模态模型 ImageBind 对齐至共享特征空间，使模型支持文本、图像、视频、音频等多种风格输入模态。

**方法定位**：STYLEMOTIF 以预训练运动潜变量扩散模型 **MLD**（Chen et al., ICLR 2023）为基础内容生成器，在单分支结构内完成风格注入，区别于 SMooDi 的双分支 ControlNet 范式。其风格编码器由 MLD 的 VAE 编码器在 100STYLE 数据集上微调得到，多模态对齐模块通过冻结 ImageBind 文本编码器并添加轻量投影层实现。

**主要结果**：
- 在运动引导风格化任务上，STYLEMOTIF 的 SRA 达到 **77.65**，FID 为 **1.551**，均优于所有基线方法，SRA 相对 SMooDi 提升 **5.23%**。
- 在文本引导风格化任务上，SRA 达到 **56.71**，远超 ChatGPT+MLD 的 4.82，提升 **51.89%**。
- 单分支设计使推理速度提升 **22.5%**，可学习参数减少 **43.9%**。

### 问题背景：运动风格化的需求与挑战

在计算机动画、虚拟现实和人机交互等领域，生成具有特定风格的自然人体运动是一项核心任务。运动风格化旨在将风格特征（如“优雅地”、“机器人式地”、“愤怒地”）注入到内容运动（如“行走”、“跳跃”）中，使生成的运动既保留内容语义，又呈现目标风格的表现力。这一任务的本质挑战在于**风格与内容的解耦与融合**：风格特征需要从参考样本中提取并迁移，同时不能破坏内容运动的语义完整性和物理合理性。

### 现有方法及其局限

早期运动风格化方法主要依赖生成对抗网络或Transformer架构，在风格迁移任务上取得了一定进展，例如**Aberman et al.**（CVPR 2020）通过解耦风格与内容实现运动风格迁移，**Motion Puzzle**（Jang et al., ACM TOG 2022）采用分身体部位的方式处理风格化，以及**MOST**（Kim et al., CVPR 2024）基于Transformer进行风格转换。然而，这些方法通常局限于运动序列之间的风格迁移，无法灵活地接受其他模态的风格输入。

随着扩散模型在运动生成领域的突破，**MLD**（Chen et al., ICLR 2023）作为文本到运动生成的潜变量扩散模型，展现了强大的内容生成能力。在此基础上，**SMooDi**（Zhong et al., ECCV 2024）将ControlNet风格的双分支架构引入运动风格化，通过在MLD的每个去噪块旁添加零初始化线性层作为并行风格分支，实现了运动引导的风格化生成。

然而，SMooDi的双分支设计带来了两个核心瓶颈：

1. **模型复杂度与训练开销增高**：每个去噪块都需要额外的风格分支，导致可学习参数显著增加，训练和推理效率受限。
2. **风格输入模态单一**：仅支持运动序列作为风格参考，无法利用文本、图像、音频、视频等多模态风格描述，限制了应用的灵活性和用户友好性。

此外，直接使用ChatGPT生成风格提示词并输入MLD（ChatGPT+MLD）的方式，由于缺乏专门的风格注入机制，风格控制能力极弱，在文本引导风格化任务上的风格识别准确率（SRA）仅为4.82%，几乎无法有效迁移风格。

### 本文动机

针对上述瓶颈，本文提出**STYLEMOTIF**，核心动机在于：

- **架构简化**：用单分支扩散框架替代双分支设计，通过统计变换的方式直接在去噪主分支内完成风格注入，消除额外的可学习参数分支，降低模型复杂度和训练开销。
- **多模态风格控制**：将风格编码器与预训练多模态模型ImageBind对齐，构建统一的风格特征空间，使模型能够从文本、图像、视频、音频等多种模态中提取风格特征，实现灵活的多模态风格化。
- **高效融合机制**：设计风格-内容交叉归一化（Style-Content Cross Normalization），利用内容特征的统计量对风格特征进行自适应归一化后加性融合，无需引入额外参数，在保持内容保真度的同时有效注入风格信息。

## 核心方法与创新机理

### 从双分支到单分支：架构简化的因果逻辑

现有风格化运动生成方法（以 **SMooDi**（Zhong et al., ECCV 2024）为代表）普遍采用类 ControlNet 的双分支架构：一个内容生成分支负责文本到运动的扩散去噪，另一个并行的风格分支通过零初始化线性层注入风格条件。这种设计虽然有效，但引入了显著的模型复杂度和训练开销——每个 MLD 去噪块都需要额外的可学习参数来处理风格信息，且双分支协同训练增加了优化难度。

**STYLEMOTIF** 的核心创新在于将这一范式替换为单分支扩散框架。其因果逻辑是：风格注入本质上可以视为特征空间的统计变换，而非必须依赖独立的网络分支。据此，模型仅在原始 MLD 去噪分支内部，通过**风格-内容交叉归一化**（Style-Content Cross Normalization）以加性融合方式直接注入风格信息，融合操作仅在单个去噪块后执行一次。这一设计消除了所有额外的可学习参数，从根本上降低了模型复杂度。

### 风格-内容交叉归一化：无参风格注入机制

该机制是 STYLEMOTIF 实现单分支架构的关键技术。给定内容特征 $\mathcal{F}_c$ 和风格特征 $\mathcal{F}_s$，首先计算内容特征沿特征维度的均值与方差：

$$\mu_c = \frac{1}{D} \sum_{j=1}^{D} \mathcal{F}_c^{i,j}, \quad \sigma_c^2 = \frac{1}{D} \sum_{j=1}^{D} (\mathcal{F}_c^{i,j} - \mu_c)^2$$

随后，使用内容特征的统计量对风格特征进行归一化，使其适应内容特征的分布特性：

$$\widetilde{\mathcal{F}}_{s,c} = \frac{\mathcal{F}_s - \mu_c}{\sqrt{\sigma_c^2 + \eta}}$$

最终，归一化后的风格特征以缩放因子 $\gamma$ 加性融合到内容特征中：

$$\mathcal{F}^{i}(z_t, t, \tau_{\theta}(c), \psi_{\theta_s}(s); \theta_c) = \mathcal{F}_c^{i} + \gamma \cdot \widetilde{\mathcal{F}}_{s,c}$$

这一设计的核心洞察在于：风格特征可以通过内容特征的均值与方差进行归一化后，以加性方式注入扩散去噪过程，无需额外可学习参数。与 SMooDi 在每个 MLD 块添加零初始化线性层的做法相比，STYLEMOTIF 的融合仅在去噪过程的第 $m$ 个块后执行一次，实现了极致的参数效率。

### 多模态风格空间统一：从单一运动到跨模态控制

SMooDi 的风格输入局限于运动序列本身，无法利用文本、图像、音频等其他模态的风格描述。STYLEMOTIF 通过**多模态对比学习对齐**突破了这一限制。

具体而言，模型冻结预训练的多模态模型 **ImageBind** 的文本编码器，添加轻量投影层，通过对称对比损失将运动风格特征与多模态文本特征对齐至统一空间：

$$\mathcal{L}_{\mathrm{align}} = -\frac{1}{2}\sum_{(i,j)}\log\frac{\exp(\mathcal{F}_t^{i}\cdot\mathcal{F}_s^{j}/\tau_0)}{\sum_k\exp(\mathcal{F}_t^{i}\cdot\mathcal{F}_s^{k}/\tau_0)} + \log\frac{\exp(\mathcal{F}_t^{i}\cdot\mathcal{F}_s^{j}/\tau_0)}{\sum_k\exp(\mathcal{F}_t^{k}\cdot\mathcal{F}_s^{j}/\tau_0)}$$

对齐完成后，给定任意模态 $m$（文本、图像、视频、音频），通过 ImageBind 提取全局特征 $\mathcal{F}_m = \mathcal{E}_{\mathrm{ImageBind}}(m)$，并在统一空间中检索语义最相似的运动风格特征进行引导。这使得模型首次实现了真正统一的多模态运动风格化控制。

### 关键改进量化

消融实验和效率对比验证了上述创新的实际效果：

- **架构简化**：单分支设计使可学习参数减少 43.9%，推理速度提升 22.5%（Table 4，单卡 NVIDIA A100）。
- **风格控制精度**：在运动引导风格化任务上，SRA 达到 77.65，相对 SMooDi 的 72.42 提升 5.23%，同时 FID 降至 1.551（Table 1）。
- **多模态泛化**：文本引导风格化的 SRA 达到 56.71，远超 ChatGPT+MLD 的 4.82（Table 1），证明了跨模态对齐的有效性。
- **融合参数**：缩放因子 $\gamma = 0.6$ 在风格表现（SRA）和内容保真（FID）之间取得了最佳平衡（Figure 7）。

### 局限与待解决问题

当前方法仍存在以下局限：多模态对齐的训练数据来源于 100STYLE 子集，风格运动-文本配对数据有限，可能限制模型对广泛风格的泛化能力；交叉归一化假定风格可通过简单统计变换迁移，对复杂或细粒度风格可能表现不足。开放问题包括：最优融合位置 $m$ 的自动确定、$\gamma$ 的自适应动态学习、以及如何更有效地整合图像和音频等模态的风格描述。

STYLEMOTIF 是一个基于单分支扩散架构的多模态运动风格化框架，其核心设计理念是以极简的结构实现高效、灵活的风格注入。与 SMooDi（Zhong et al., ECCV 2024）采用的双分支 ControlNet 范式不同，STYLEMOTIF 将风格注入完全整合进预训练运动潜变量扩散模型（MLD, Chen et al., ICLR 2023）的单一去噪分支中，从而避免了额外分支带来的模型复杂度和训练开销。

框架的输入由两部分组成：**内容提示**（文本描述的目标动作语义）和**风格参考**（可来自运动序列、文本、图像、视频、音频等多种模态）。其整体流程可概括为以下模块链：

1. **预训练运动潜变量扩散模型（MLD）**：作为内容生成的基础模型，MLD 将文本提示 $c$ 通过 CLIP 编码器 $\tau_{\theta}(c)$ 转化为内容条件，在潜变量空间中对随机噪声 $z_t$ 执行迭代去噪，逐步恢复出目标运动潜变量。该模型在整个风格化训练过程中保持冻结，仅作为内容保真度的锚点。

2. **风格编码器**：从参考运动序列 $s$ 中提取紧凑的风格特征。该编码器由 MLD 的 VAE 编码器在 100STYLE 数据集上以变分自编码方式微调得到，训练后仅保留编码器部分作为风格提取器 $\psi_{\theta_s}(s)$。对于非运动模态的风格输入（如文本、图像等），则通过多模态对齐模块间接获取对应的运动风格特征。

3. **多模态对齐模块**：为实现跨模态风格控制，框架冻结 ImageBind 的文本编码器，在其上添加一个轻量投影层 $\pi$，通过对称对比损失将运动风格特征与文本特征对齐至统一的共享特征空间。对于任意模态 $m$ 的风格输入，首先通过 ImageBind 提取全局特征 $\mathcal{F}_m = \mathcal{E}_{\mathrm{ImageBind}}(m)$，随后在该统一空间中检索语义最相似的运动风格特征，作为后续融合的风格条件。这一设计使得模型无需为每种模态单独训练风格编码器。

4. **风格-内容交叉融合模块**：这是 STYLEMOTIF 区别于双分支方法的核心创新。在 MLD 去噪过程的第 $m$ 个 Transformer 块之后，模块计算内容特征 $\mathcal{F}_c$ 的均值 $\mu_c$ 与方差 $\sigma_c^2$，并用这些统计量对风格特征 $\mathcal{F}_s$ 进行归一化：

   $$\widetilde{\mathcal{F}}_{s,c} = \frac{\mathcal{F}_{s} - \mu_c}{\sqrt{\sigma_c^2 + \eta}}$$

   归一化后的风格特征以缩放因子 $\gamma$ 加性融合到内容特征中：

   $$\mathcal{F}^{i}(z_t, t, \tau_{\theta}(c), \psi_{\theta_s}(s); \theta_c) = \mathcal{F}_c^{i} + \gamma \cdot \widetilde{\mathcal{F}}_{s,c}$$

   该融合仅在单个去噪块后执行一次，整个过程不引入任何额外可学习参数，完全基于统计变换完成风格注入。消融实验表明，$\gamma=0.6$ 在风格表现（SRA）与内容保真度（FID）之间取得了最优平衡。

5. **混合引导扩散采样**：在推理采样阶段，框架结合无分类器引导和分类器引导策略，在内容保真度与风格遵循度之间进行动态平衡，确保生成的运动既忠实于文本内容描述，又充分体现目标风格特征。

**效率优势**：得益于单分支设计和无参数融合机制，STYLEMOTIF 相比 SMooDi 的可学习参数减少 43.9%，单样本推理速度提升 22.5%（单卡 NVIDIA A100 测试），在显著降低计算成本的同时实现了更优的风格化质量。

### 风格-内容交叉融合

STYLEMOTIF 的核心创新在于将 SMooDi 的双分支 ControlNet 风格注入架构替换为单分支统计变换机制。在 SMooDi 中，每个 MLD 去噪块的输出需通过零初始化线性层添加并行风格分支：

$$\mathcal{F}^{i}(z_{t}, t, \tau_{\theta}(c), \psi_{\theta_{s}}(s); \theta_{c}) = \mathcal{F}^{i}(z_{t}, t, \tau_{\theta}(c); \theta_{c}) + \mathcal{Z}(\mathcal{F}^{i}(z_{t}, t, \tau_{\theta}(c), \psi_{\theta_{s}}(s); \theta_{c}))$$

其中 $\mathcal{Z}$ 为零初始化线性层，$\tau_{\theta}(c)$ 为文本条件，$\psi_{\theta_{s}}(s)$ 为风格条件。这种设计在每个去噪块均需额外计算，导致参数和推理开销显著增加。

STYLEMOTIF 将上述机制替换为**风格-内容交叉归一化**（Style-Content Cross Normalization），仅在单个去噪块后执行一次融合，且无需额外可学习参数。具体流程如下：

**步骤一：内容特征统计量计算。** 对于第 $m$ 个去噪块输出的内容特征 $\mathcal{F}_c^{i}$（维度为 $D$），计算其均值与方差：

$$\mu_c = \frac{1}{D}\sum_{j=1}^{D}\mathcal{F}_c^{i,j}$$

$$\sigma_c^{2} = \frac{1}{D}\sum_{j=1}^{D}\left(\mathcal{F}_c^{i,j} - \mu_c\right)^{2}$$

**步骤二：风格特征交叉归一化。** 使用内容特征的统计量对风格嵌入 $\mathcal{F}_s$ 进行归一化，使风格特征适应内容特征的分布特性：

$$\widetilde{\mathcal{F}}_{s,c} = \frac{\mathcal{F}_{s} - \mu_c}{\sqrt{\sigma_c^2 + \eta}}$$

其中 $\eta$ 为数值稳定常数。该操作将风格特征的均值与方差对齐至内容特征空间，本质是以内容统计量为“锚点”对风格信息进行重参数化。

**步骤三：加性融合。** 将归一化后的风格特征以缩放因子 $\gamma$ 加性注入内容特征：

$$\mathcal{F}^{i}(z_t, t, \tau_{\theta}(c), \psi_{\theta_s}(s); \theta_c) = \mathcal{F}_c^{i} + \gamma \cdot \widetilde{\mathcal{F}}_{s,c}$$

融合仅在去噪过程的第 $m$ 个块后执行一次，而非在每个块重复。这一设计消除了零初始化线性层的可学习参数，将风格注入简化为纯统计变换。

### 多模态对齐模块

为实现文本、图像、视频、音频等多模态风格控制，STYLEMOTIF 构建了统一的风格特征空间。具体包含两个子模块：

**风格编码器预训练。** 风格编码器由 MLD 的 VAE 编码器在 100STYLE 数据集上以变分自编码方式微调得到，训练完成后仅保留编码器部分，用于从参考运动序列中提取风格特征。

**多模态对比对齐。** 冻结 ImageBind 的文本编码器 $\mathcal{E}_{\text{text}}$，添加轻量投影层 $\pi$，将文本标签 $l$ 映射为特征：

$$\mathcal{F}_t = \pi\big(\mathcal{E}_{\text{text}}(l)\big)$$

通过对称对比损失将运动风格特征 $\mathcal{F}_s$ 与文本特征 $\mathcal{F}_t$ 对齐至共享空间：

$$\mathcal{L}_{\text{align}} = -\frac{1}{2}\sum_{(i,j)}\log\frac{\exp(\mathcal{F}_t^{i}\cdot\mathcal{F}_s^{j}/\tau_0)}{\sum_k\exp(\mathcal{F}_t^{i}\cdot\mathcal{F}_s^{k}/\tau_0)} + \log\frac{\exp(\mathcal{F}_t^{i}\cdot\mathcal{F}_s^{j}/\tau_0)}{\sum_k\exp(\mathcal{F}_t^{k}\cdot\mathcal{F}_s^{j}/\tau_0)}$$

其中 $\tau_0$ 为温度参数。对齐完成后，任意模态 $m$（文本、图像、视频、音频）均可通过 ImageBind 提取全局特征：

$$\mathcal{F}_m = \mathcal{E}_{\text{ImageBind}}(m)$$

利用 $\mathcal{F}_m$ 在统一空间中检索语义最相似的运动风格特征进行引导，实现多模态风格的统一表达。

![[assets/figures/papers/paper_list_l3_StyleMotif_Multi_Modal_Motion_Stylization_using_Style_Content_Cross_Fusi_motion20v/figures/001_Figure_1.jpg]]
*Figure 1: Comparison of Our Proposed STYLEMOTIF Framework with SMooDi. Unlike SMooDi’s dual-branch design, which increases model complexity and training overhead, STYLEMOTIF employs a streamlined single-branch structure, enabling efficient multi-modal motion stylization while preserving motion realism*

## 实验与关键发现

### 运动引导风格化主结果

Table 1（上）报告了在100STYLE/HumanML3D基准上的运动引导风格化结果。STYLEMOTIF在风格识别准确率（SRA）上达到77.65，相较最强基线SMooDi的72.42提升5.23个百分点，同时FID降至1.551，表明生成运动在风格遵循度与内容保真度之间取得了更优平衡。定性对比（Figure 3）进一步验证了这一优势：在“画圆轨迹”（第一列）和“跳跃”（第三列）等案例中，STYLEMOTIF生成的连贯运动既能忠实保留内容语义，又能准确迁移参考风格；而SMooDi在“左侧电话”案例（第二列）中则未能有效反映指定风格，且内容保真度有所损失。

![[assets/figures/papers/paper_list_l3_StyleMotif_Multi_Modal_Motion_Stylization_using_Style_Content_Cross_Fusi_motion20v/figures/004_Table_1.jpg]]
*Table 1: Quantitative Results for Motion-Guided and Text-Guided Stylization. Bold values denote the best performance. As there is no ground-truth reference for Diversity, no value is highlighted in bold; but the metric is provided for reference*

![[assets/figures/papers/paper_list_l3_StyleMotif_Multi_Modal_Motion_Stylization_using_Style_Content_Cross_Fusi_motion20v/figures/005_Figure_3.jpg]]
*Figure 3: Qualitative Results of Motion-Guided Stylization. Our model generates cohesive and realistic motions that effectively align style and content, such as preserving the ‘circular’ trajectory (first column) and ‘hop’ content (third column). In contrast, SMooDi [71] struggles to maintain content fidelity and sometimes fails to reflect the specified style (e.g., ‘phone on the left’ in the second colum)*

### 文本引导风格化主结果

在仅使用文本风格描述（无参考运动序列）的文本引导风格化任务上，STYLEMOTIF的SRA达到56.71，远超ChatGPT+MLD的4.82（Table 1下）。这一巨大差距源于多模态对齐模块将文本风格特征与运动风格特征映射至统一空间，使模型能够从文本描述中提取有效的风格信号，而非依赖不可靠的提示词工程。Figure 4的定性结果展示了模型将文本风格描述与内容无缝整合的能力。

### 运动风格迁移结果

Table 2展示了在HumanML3D上的运动风格迁移结果。STYLEMOTIF在所有指标上均优于先前最优方法，SRA达到68.81（提升3.66）。这一结果表明风格-内容交叉融合机制不仅适用于风格化生成，也为风格迁移等下游任务提供了有效支撑。

### 消融研究

**风格编码器预训练策略**（Table 3）：在100STYLE和HumanML3D上联合预训练风格编码器，相比仅使用单一数据集，取得了最高的SRA（77.65）和最低的FID（1.551）。这表明联合预训练有助于编码器学习更通用的风格表征，避免对单一数据分布的过拟合。

**多模态对齐文本表达**（Table 3）：使用单一文本标签进行对比对齐，优于使用完整句子或标签组合。可能原因是单标签提供了更干净、更具判别力的监督信号，减少了文本噪声对对齐质量的干扰。

**融合缩放比例γ**（Figure 7）：γ=0.6在SRA和FID之间取得了最佳平衡。过小的γ削弱风格注入效果，过大的γ则损害内容保真度。当前γ通过人工调节确定，自适应动态学习机制是值得探索的方向。

### 效率分析

Table 4对比了STYLEMOTIF与SMooDi的参数量和推理速度。单分支设计使可学习参数减少43.9%，推理速度提升22.5%（单卡NVIDIA A100上每样本平均时间）。效率提升的核心在于：风格-内容交叉归一化以无参数统计变换替代了SMooDi在每个MLD块中插入的零初始化线性层，且融合仅在单个去噪块后执行一次。

### 失败模式与局限性

当前方法存在以下已知局限：其一，多模态对齐的训练数据来源于100STYLE子集，风格运动-文本配对数据有限，可能限制模型对广泛风格的泛化能力；其二，交叉归一化假定风格可通过简单统计变换迁移，对复杂或细粒度风格（如特定节奏模式、细微情感表达）可能表现不足。这些场景下，SRA可能出现显著下降，需要更精细的风格解耦与注入机制。

![[assets/figures/papers/paper_list_l3_StyleMotif_Multi_Modal_Motion_Stylization_using_Style_Content_Cross_Fusi_motion20v/figures/003_Table_2.jpg]]
*Table 2: Quantitative Results of Motion Style Transfer on HumanML3D [13] dataset. Our method outperforms previous works in all metrics, which demonstrates effective style-content fusion for high-quality motion style transfer, providing significant advantages for downstream tasks besides motion stylization*

![[assets/figures/papers/paper_list_l3_StyleMotif_Multi_Modal_Motion_Stylization_using_Style_Content_Cross_Fusi_motion20v/figures/006_Figure_4.jpg]]
*Figure 4: Qualitative Results of Text-Guided Stylization. Our model seamlessly integrates textual style descriptions with content, producing visually coherent and stylistically consistent results*

![[assets/figures/papers/paper_list_l3_StyleMotif_Multi_Modal_Motion_Stylization_using_Style_Content_Cross_Fusi_motion20v/figures/008_Table_3.jpg]]
*Table 3: Ablation Study on Style Encoder Pre-training Strategies and Text Expression for Multi-modal Alignment. ‘w. HumanML3D’ and ‘w. 100STYLE’ denote pre-training with HumanML3D [13] and 100STYLE [35] data respectively*

## 定位与知识库关联

### 核心瓶颈与因果调控

现有风格化运动生成方法的瓶颈在于**双分支架构的复杂性与模态局限性**。以 **SMooDi**（Zhong et al., ECCV 2024）为代表的方案，采用 ControlNet 风格的双分支设计——在预训练运动潜变量扩散模型（**MLD**, Chen et al., ICLR 2023）的每个去噪块旁添加零初始化线性层作为并行风格注入分支。这种设计虽然实现了风格控制，但引入了显著的模型复杂度和训练开销，且风格输入局限于单一运动序列模态。

STYLEMOTIF 的因果调控旋钮在于**将双分支架构替换为单分支扩散框架**，核心操作是风格-内容交叉归一化（Style-Content Cross Normalization）。该方法以统计变换方式直接向内容特征中注入风格信息：计算内容特征的均值与方差，对风格特征进行归一化后以缩放因子 $\gamma$ 加性融合到内容特征中，整个过程无额外可学习参数，且融合仅在单个去噪块后执行一次。同时，通过多模态对比学习将风格编码器与预训练多模态模型 ImageBind 对齐至共享特征空间，实现文本、图像、音频、视频等多种风格输入的统一控制。

### 与基线方法的关系

**（1）与 MLD（Chen et al., ICLR 2023）的关系**

MLD 是 STYLEMOTIF 的内容生成基础模型，提供文本到运动潜变量的扩散去噪能力。STYLEMOTIF 保留了 MLD 的完整去噪分支，但在其内部嵌入了风格-内容交叉融合模块，使原本仅支持文本条件的基础模型获得多模态风格控制能力，而无需修改 MLD 的核心架构。

**（2）与 SMooDi（Zhong et al., ECCV 2024）的关系**

SMooDi 是 STYLEMOTIF 最直接的前驱工作，也是主要对比基线。两者的关键差异体现在三个维度：

- **架构分支数**：SMooDi 采用双分支（内容生成分支 + 风格注入分支），STYLEMOTIF 采用单分支（融合在内部完成）。这一简化使可学习参数减少 43.9%，推理速度提升 22.5%（Table 4）。
- **风格注入机制**：SMooDi 在每个 MLD 块添加零初始化线性层作为风格分支，STYLEMOTIF 以统计变换（风格-内容交叉归一化）替代，仅在单个去噪块后执行一次融合。
- **风格输入模态**：SMooDi 仅支持运动序列作为风格参考，STYLEMOTIF 通过多模态对齐支持运动、文本、图像、视频、音频等多模态输入。

在运动引导风格化任务上，STYLEMOTIF 的 SRA 达到 77.65，相对 SMooDi 的 72.42 提升 5.23%，同时 FID 降至 1.551（Table 1）。

**（3）与运动风格迁移方法的关系**

传统运动风格迁移方法聚焦于从参考运动序列中解耦并迁移风格。**Aberman et al.**（CVPR 2020）基于生成对抗网络解耦风格与内容，**Motion Puzzle**（Jang et al., ACM TOG 2022）采用分身体部位的风格迁移策略，**MOST**（Kim et al., CVPR 2024）基于 Transformer 实现风格转换。STYLEMOTIF 在运动风格迁移任务上 SRA 达到 68.81，超越此前最佳结果 65.15（Table 2），验证了风格-内容交叉融合在风格迁移下游任务上的有效性。

**（4）与 ChatGPT+MLD 的关系**

文本引导风格化任务中，基线方法 ChatGPT+MLD 使用 ChatGPT 生成风格描述提示词后输入 MLD，SRA 仅为 4.82。STYLEMOTIF 通过多模态对齐将风格编码器与 ImageBind 文本编码器统一至共享特征空间，SRA 达到 56.71，提升 51.89 个百分点（Table 1 bottom），表明直接对齐的风格特征空间远优于间接的文本提示工程。

### 适用边界

**（1）风格输入模态的覆盖范围**

STYLEMOTIF 支持运动、文本、图像、视频、音频五种模态的风格输入。多模态对齐的核心机制是：冻结 ImageBind 文本编码器，添加轻量投影层，通过对称对比损失将运动风格特征与文本特征对齐至统一空间；其他模态（图像、视频、音频）通过 ImageBind 提取全局特征后，在该统一空间中检索最语义相似的运动风格特征进行引导。然而，多模态对齐的训练数据来源于 100STYLE 子集的风格运动-文本配对数据，数据规模有限，可能限制模型对广泛风格的泛化能力。

**（2）风格迁移的粒度限制**

当前的交叉归一化方法假定风格可以通过简单统计变换（均值与方差归一化后加性融合）进行迁移。这一假设对宏观风格特征（如运动节奏、幅度、轨迹特征）有效，但对复杂或细粒度风格（如特定关节的微动作模式、分身体部位的差异化风格）可能表现不足。消融实验中融合缩放比例 $\gamma=0.6$ 在风格表现（SRA）和内容保真（FID）之间取得最佳平衡（Figure 7），说明风格注入强度需要人工调节，缺乏自适应机制。

**（3）内容保真度约束**

混合引导扩散采样结合无分类器引导和分类器引导，在采样过程中平衡内容保真度与风格遵循度。当风格与内容存在语义冲突时（如“优雅”风格与“拳击”内容），模型需要在两者间进行折中，可能导致风格表达不充分或内容失真。

### 局限与开放问题

**已知局限：**

1. **训练数据规模约束**：多模态对齐的训练数据来源于 100STYLE 子集，风格运动-文本配对数据有限，可能限制模型对长尾风格和开放域风格的泛化能力。
2. **统计变换假设的简化性**：交叉归一化假定风格可通过均值-方差归一化进行迁移，对复杂或细粒度风格可能表现不足。
3. **融合超参数需人工调节**：缩放因子 $\gamma$ 和融合块索引 $m$ 需人工设定，缺乏数据驱动的自适应机制。

**开放问题：**

1. 如何在有限的风格运动-文本数据下提升对更广泛运动风格的泛化能力？可能的路径包括数据增强、半监督对齐或利用大规模多模态预训练模型的知识蒸馏。
2. 最优融合位置（块索引 $m$）能否通过可微分搜索或基于内容的动态路由自动确定？
3. 缩放参数 $\gamma$ 能否通过自适应机制（如基于内容-风格相似度的门控网络）动态学习，而非人工调节？
4. 多模态对齐中，除了文本作为桥梁模态，如何更有效地直接整合图像、音频等模态的风格描述，减少文本中介带来的语义损失？
5. 风格-内容交叉归一化是否可扩展至分身体部位或分时间尺度的层次化风格注入，以支持更细粒度的风格控制？

## 原文 PDF

![[paperPDFs/ICCV_2025/StyleMotif_Multi_Modal_Motion_Stylization_using_Style_Content_Cross_Fusion.pdf]]
