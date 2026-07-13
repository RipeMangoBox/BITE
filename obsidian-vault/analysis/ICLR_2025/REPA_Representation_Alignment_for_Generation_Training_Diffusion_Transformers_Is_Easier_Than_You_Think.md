---
title: "REPA: Representation Alignment for Generation: Training Diffusion Transformers Is Easier Than You Think"
type: paper
paper_level: A
venue: ICLR
year: 2025
pdf_ref: paperPDFs/ICLR_2025/REPA_Representation_Alignment_for_Generation_Training_Diffusion_Transformers_Is_Easier_Than_You_Think.pdf
project_link: null
code_link: null
aliases:
- RRA
- REPA
tags:
- ICLR_2025
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/representation_self_supervised_transfer
core_operator: 将扩散变压器内部的隐含状态与外部预训练自监督视觉表示（如DINOv2）对齐的正则化项（REPA loss）。
primary_logic: 通过简单地在扩散变压器前几层对齐其隐含状态与预训练自监督视觉表示（如DINOv2），可以大幅加速训练并提升生成性能，因为这使得模型能够更早地关注语义信息，而后几层专注于高频细节。
claims:
- REPA使SiT训练速度提升>17.5倍，在不到400K次迭代下匹配SiT-XL 7M步的性能（无分类器指导）。
- 在不使用无分类器指导的情况下，REPA在SiT-XL/2上仅用400K次迭代即达到FID=7.9，优于原始SiT-XL/2在7M次迭代的8.3。
- 使用无分类器指导并结合引导间隔，REPA达到FID=1.42的最先进结果。
- ImageNet 256×256 类条件生成 上 FID（无分类器指导） = 7.9
---

# REPA: Representation Alignment for Generation: Training Diffusion Transformers Is Easier Than You Think

> [!tip] 核心洞察
> 通过简单地在扩散变压器前几层对齐其隐含状态与预训练自监督视觉表示（如DINOv2），可以大幅加速训练并提升生成性能，因为这使得模型能够更早地关注语义信息，而后几层专注于高频细节。

| 字段 | 内容 |
|------|------|
| 中文题名 | REPA：生成式表示对齐——训练扩散变压器比你想象的更容易 |
| 英文题名 | REPA: Representation Alignment for Generation: Training Diffusion Transformers Is Easier Than You Think |
| 会议/期刊 | ICLR 2025 |
| Links | [paper](https://arxiv.org/abs/2410.06940) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/representation_self_supervised_transfer |
| Method | REPA (REPresentation Alignment) |
| Dataset | ImageNet 256×256 类条件生成, ImageNet 512×512 类条件生成 |

> [!tip] 效果简介
> - ImageNet 256×256 类条件生成 上，FID（无分类器指导） 7.9 vs 8.3 (-0.4)；FID（有分类器指导+引导间隔） 1.42 vs 2.06 (-0.64)。
> - ImageNet 512×512 类条件生成 上，FID（有分类器指导） 2.08 vs 2.62 (-0.54)。

## 概要

训练大规模扩散模型的核心瓶颈并非模型容量或数据规模不足，而是**扩散变压器无法高效学习高质量的判别性内部表示**。尽管扩散模型在生成任务上取得了显著成功，但现有工作（如 **DiT** (Peebles & Xie, 2023) 和 **SiT** (Ma et al., 2024a)）在训练过程中，其内部特征与预训练自监督视觉表示（如 DINOv2）之间存在明显的“语义鸿沟”，且这种对齐的改善极为缓慢。

本文提出的 **REPA (REPresentation Alignment)** 方法，通过一个简洁的正则化项直接操控这一瓶颈：将扩散变压器前几层的隐含状态投影，与外部预训练自监督视觉编码器（如 DINOv2）提取的干净图像表示进行逐块对齐。其核心洞见在于，仅需在 Transformer 的前几层施加这种表示对齐，即可使模型早期关注全局语义信息，而将后几层解放出来专注于高频细节的建模。

该方法带来了显著的训练效率与性能提升：
- **收敛加速**：REPA 使 SiT 的训练速度提升超过 **17.5 倍**，在不到 400K 次迭代下即可匹配 SiT-XL/2 原始训练 7M 步的性能（无分类器指导 FID 分别为 7.9 与 8.3）。
- **性能突破**：结合分类器指导与引导间隔技术后，REPA 在 ImageNet 256×256 类条件生成上达到 **FID=1.42** 的领先结果。
- **可扩展性**：该方法在不同模型规模、不同目标编码器（DINOv2、MoCov3、MAE）以及更高分辨率（512×512）和文本到图像生成任务上均表现出一致的增益。

REPA 本质上是一种**表示蒸馏正则化**，其简洁性使得它可以即插即用地集成到现有扩散变压器框架中，无需修改基础架构或采样过程。



### 扩散生成模型的训练效率瓶颈

扩散模型已成为高保真图像生成的主流范式。当前最具竞争力的架构——扩散变压器（Diffusion Transformers，如 **DiT**（Peebles & Xie, 2023）和 **SiT**（Ma et al., 2024a）——通过在潜在空间中对图像进行去噪或速度预测来实现生成。这些模型通常遵循一个标准流程：使用 VAE 编码器将图像压缩为低维潜在表示 $z = E(x)$，然后由扩散变压器编码器 $f_\theta$ 从噪声潜变量 $z_t$ 提取分层隐藏表示 $h_t = f_\theta(z_t)$，最终由解码器 $g_\theta$ 基于 $h_t$ 预测速度场 $v_t$ 或噪声。

然而，训练大规模扩散变压器面临一个核心瓶颈：**模型无法有效地学习高质量的判别性内部表示**。尽管这些模型最终能生成逼真的图像，但其内部隐藏状态与强大的预训练视觉表示（如 DINOv2）之间存在显著的语义差距。这一瓶颈直接制约了训练效率和生成性能的上限。

### 语义差距的实证发现

作者通过系统性的实证分析揭示了这一问题的严重性。如 Figure 2 所示，即使经过 7M 次迭代训练的 SiT-XL/2 模型，其内部表示与 DINOv2-g 之间仍存在显著差距。具体表现为：

- **线性探测性能不足**：预训练 SiT 模型虽然学到了具有语义意义的表示，但与 DINOv2 相比仍有较大差距。
- **CKNNA 对齐度较低**：使用 CKNNA（Centered Kernel Alignment with Normalized Neighborhood Analysis）度量时，SiT 确实展现出与 DINOv2 的一定对齐，但其绝对值远低于其他视觉编码器。
- **对齐进展缓慢**：虽然增大模型规模和延长训练时间可以改善对齐程度，但这一进展极其缓慢且不充分。

同样的现象在 DiT-XL/2 模型上也被观察到（Figure 10），表明这是扩散变压器架构的共性问题，而非特定模型的缺陷。

### 现有方法的局限

现有加速扩散模型训练的方法主要集中在改进采样过程或优化网络架构本身，但鲜有方法直接针对**内部表示质量**这一根本瓶颈。自监督视觉表示学习（如 DINOv2、MoCov3、MAE）近年来取得了显著进展，能够从干净图像中提取高度语义化、判别性强的特征，但这些强大的表示尚未被有效利用来提升扩散模型的训练过程。

### 核心动机与研究思路

本文的核心洞察是：**通过简单地在扩散变压器前几层对齐其隐含状态与预训练自监督视觉表示（如 DINOv2），可以大幅加速训练并提升生成性能**。这一洞察基于以下关键观察：

1. **语义信息与高频细节的分工**：扩散变压器的早期层更适合捕捉全局语义信息，而后几层则专注于高频细节的恢复。因此，仅在前几层进行表示对齐即可实现高效的语义蒸馏。
2. **表示对齐的涟漪效应**：当早期层获得了高质量的语义表示后，后续层可以更有效地利用这些信息进行去噪或速度预测，从而整体提升生成质量。
3. **正则化的简单性**：表示对齐可以作为一个简单的正则化项添加到现有训练目标中，无需修改网络架构或采样过程。

基于这一思路，作者提出了 **REPA（REPresentation Alignment）** 方法——一种将扩散变压器内部隐藏状态与外部预训练视觉表示对齐的正则化技术，旨在从根本上解决扩散模型训练效率低下的问题。



## 核心方法与创新机理

### 问题瓶颈：扩散模型内部的表示学习鸿沟

大规模扩散模型（如 DiT、SiT）虽然在生成质量上取得了显著进展，但其内部隐藏状态所蕴含的判别性表示质量远低于专用自监督视觉编码器（如 DINOv2）。实证分析（Figure 2）表明，即使经过 7M 步训练的 SiT-XL/2 模型，其与 DINOv2-g 之间的语义对齐仍然存在显著差距——线性探测准确率远低于 DINOv2 本身，且 CKNNA 对齐度量值也明显弱于其他视觉编码器。尽管更大的模型和更长的训练能带来一定改善，但进展缓慢且不充分。这一"语义鸿沟"构成了训练效率与生成性能提升的核心瓶颈。

### 因果调节变量：REPA 正则化项

REPA 的核心创新在于引入一个简洁的正则化项，将扩散变压器内部的隐含状态与外部预训练自监督视觉表示显式对齐。具体而言：

- **对齐目标**：使用预训练视觉编码器 $f$（如 DINOv2）对干净图像 $x_*$ 提取的逐块表示 $y_* = f(x_*)$ 作为目标。
- **对齐对象**：从扩散变压器编码器 $f_\theta$ 的某一中间层提取隐含状态 $h_t = f_\theta(z_t)$，通过可学习的投影头 $h_\phi$（MLP）将其映射到与 $y_*$ 相同的特征空间。
- **对齐损失**：最大化投影后表示与目标表示之间的逐块余弦相似度：

$$\mathcal{L}_{\mathrm{REPA}}(\theta, \phi) := -\mathbb{E}_{x_*, \epsilon, t} \Big[ \frac{1}{N} \sum_{n=1}^{N} \mathrm{sim}(y_*^{[n]}, h_{\phi}(h_t^{[n]})) \Big]$$

- **总损失**：将 REPA 损失作为正则化项叠加到原有的速度预测损失上：

$$\mathcal{L} := \mathcal{L}_{\mathrm{velocity}} + \lambda \mathcal{L}_{\mathrm{REPA}}$$

其中 $\lambda$ 控制正则化强度。

### 相对于基准的关键变更

与经典扩散变压器基准 **DiT**（Peebles & Xie, 2023）和 **SiT**（Ma et al., 2024a）相比，REPA 的 changed slot 集中在**损失函数**层面：

| 变更维度 | 基准方法 | REPA |
|---------|---------|------|
| 损失函数 | 仅包含去噪/速度预测损失（如 $\mathcal{L}_{\mathrm{velocity}}$ 或 $\mathcal{L}_{\mathrm{simple}}$） | 原始损失 + $\lambda \cdot \mathcal{L}_{\mathrm{REPA}}$，其中 $\mathcal{L}_{\mathrm{REPA}}$ 最大化隐藏状态投影与预训练表示之间的逐块余弦相似度 |

值得注意的是，REPA 并未修改扩散变压器的网络架构、采样器设计或数据预处理流程，仅通过在训练目标中增加一个轻量级的表示对齐正则化项，便实现了显著的训练加速和性能提升。

### 关键设计洞察：仅对齐前几层即可

REPA 的另一重要发现是**表示对齐仅需作用于 Transformer 的前几层**。组件分析实验（Table 2）表明，在 SiT-L/2 上，将 REPA 应用于第 8 层时达到最优生成性能（FID=10.0），而对齐更深层反而导致性能下降。这意味着 REPA 使得模型能够在早期层快速捕获语义信息，而将后几层的容量释放给高频细节建模——这一"由粗到细"的分工机制是 REPA 高效性的关键所在。



REPA（REPresentation Alignment）是一个即插即用的训练正则化框架，其核心思想是将扩散变压器内部的隐含表示与外部预训练视觉编码器的干净图像表示进行显式对齐。该框架不改变扩散模型的推理架构，仅在训练时引入一个额外的对齐损失项。

### 模块关系与数据流

整个训练pipeline由六个核心模块构成，数据流从图像到生成的路径如下：

1. **VAE编码器** $E$：输入图像 $x$ 首先被压缩为低维潜在表示 $z = E(x) \in \mathbb{R}^{32 \times 32 \times 4}$，使用Stable Diffusion的预训练VAE（Rombach et al., 2022）。这一步将高维像素空间映射到计算上更高效的潜在空间。

2. **扩散Transformer编码器** $f_\theta$：从噪声潜变量 $z_t$ 出发，提取分层隐藏表示 $h_t = f_\theta(z_t)$。$z_t$ 由干净潜变量 $z_*$ 和噪声 $\epsilon$ 通过随机插值过程 $z_t = \alpha_t z_* + \sigma_t \epsilon$ 得到，其中 $\alpha_t$ 和 $\sigma_t$ 随时间 $t$ 单调变化。

3. **REPA投影头** $h_\phi$：将编码器某中间层（通常为前8层）的隐藏表示 $h_t$ 线性投影到与目标表示相同的特征空间，输出 $h_\phi(h_t) \in \mathbb{R}^{N \times D}$。该投影头实现为一个简单的MLP。

4. **预训练视觉编码器** $f$：以干净图像 $x_*$ 为输入，提供目标表示 $y_* = f(x_*)$ 作为对齐目标。默认使用DINOv2（Oquab et al., 2024），也可替换为MoCov3、MAE等其他自监督编码器。

5. **扩散Transformer解码器** $g_\theta$：基于 $h_t$ 预测速度场 $v_t = g_\theta(h_t)$ 或噪声，用于后续采样。

6. **SDE/ODE采样器**：在推理阶段，根据学习到的速度场通过反向SDE或概率流ODE从噪声逐步生成图像。

### 训练机制

训练时，模型同时优化两个损失：

- **速度预测损失** $\mathcal{L}_{\text{velocity}}$：标准的均方误差损失，使模型学习从噪声潜变量预测速度场：
  $$\mathcal{L}_{\text{velocity}}(\theta) := \mathbb{E}_{x_*, \epsilon, t} \big[ || v_\theta(z_t, t) - \dot{\alpha}_t z_* - \dot{\sigma}_t \epsilon ||^2 \big]$$

- **REPA对齐损失** $\mathcal{L}_{\text{REPA}}$：最大化投影后的隐藏状态与预训练干净图像表示之间的逐块相似度：
  $$\mathcal{L}_{\text{REPA}}(\theta, \phi) := -\mathbb{E}_{x_*, \epsilon, t} \Big[ \frac{1}{N} \sum_{n=1}^{N} \text{sim}(y_*^{[n]}, h_{\phi}(h_t^{[n]})) \Big]$$

总损失为两者的加权组合：
$$\mathcal{L} := \mathcal{L}_{\text{velocity}} + \lambda \mathcal{L}_{\text{REPA}}$$

其中 $\lambda$ 控制正则化强度，消融实验表明 $\lambda=0.5$ 时性能最优（FID=7.9），继续增大则趋于饱和。

### 关键设计选择

REPA框架有三个关键设计维度，均在组件分析（Table 2）中得到了系统验证：

- **对齐层深度**：仅在前8层应用REPA即可获得最佳生成性能（FID=10.0），对齐更深层反而有所下降。这表明早期层负责语义信息的提取，后期层则专注于高频细节的建模。

- **目标表示选择**：更强的预训练编码器（如DINOv2-L vs DINOv2-B）能同时提升判别性能和生成质量。对齐DINOv2-L后，SiT-L/2的FID从18.8降至10.0（400K迭代）。

- **相似度函数**：NT-Xent和负余弦相似度均有效，后者因简洁性被选为默认选项。

### 框架特点

REPA的核心优势在于其**极简性**：不修改扩散模型推理架构，不增加推理计算量，仅通过训练时的一个正则化项即可实现>17.5倍的训练加速（SiT-XL在400K步内匹配原始模型7M步的性能）。该框架在DiT和SiT两种扩散变压器架构上均验证有效，展现出良好的通用性。

### 补充图表

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2410_06940/figures/001_Figure_1.jpg]]
*Figure 1: Representation alignment makes diffusion transformer training significantly easier. Our framework, REPA, explicitly aligns the diffusion model representation with powerful pretrained visual representation through a simple regularization. Notably, model training becomes significantly more efficient and effective, and achieves >17.5× faster convergence than the vanilla model*

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2410_06940/figures/014_Figure_9.jpg]]
*Figure 9: DiT block illustration*



### 1. 生成框架：随机插值与速度预测

REPA 建立在基于随机插值的扩散框架之上。给定干净数据 $\mathbf{x}_*$ 和高斯噪声 $\epsilon \sim \mathcal{N}(0, \mathbf{I})$，连续时间插值过程定义为：

$$\mathbf{x}_t = \alpha_t \mathbf{x}_* + \sigma_t \epsilon$$

其中 $\alpha_t$ 和 $\sigma_t$ 是单调函数，满足 $t=0$ 时 $(\alpha_0, \sigma_0) = (1, 0)$，$t=1$ 时 $(\alpha_1, \sigma_1) = (0, 1)$。该过程诱导了一个概率流 ODE $\dot{\mathbf{x}}_t = \mathbf{v}(\mathbf{x}_t, t)$，速度场 $\mathbf{v}$ 由神经网络 $\mathbf{v}_\theta$ 参数化，通过最小化速度预测损失训练：

$$\mathcal{L}_{\mathrm{velocity}}(\theta) := \mathbb{E}_{\mathbf{x}_*, \epsilon, t} \big[ \| \mathbf{v}_\theta(\mathbf{x}_t, t) - \dot{\alpha}_t \mathbf{x}_* - \dot{\sigma}_t \epsilon \|^2 \big]$$

训练完成后，可通过求解反向 SDE（如 Euler-Maruyama 采样器）或概率流 ODE 从噪声生成图像。

### 2. 扩散 Transformer 的编码器-解码器视角

REPA 将扩散模型 $\mathbf{v}_\theta$ 显式拆分为编码器 $f_\theta$ 和解码器 $g_\theta$ 的复合：

- **编码器 $f_\theta$**：从噪声潜变量 $\mathbf{z}_t$ 提取分层隐藏表示 $\mathbf{h}_t = f_\theta(\mathbf{z}_t)$
- **解码器 $g_\theta$**：基于 $\mathbf{h}_t$ 预测速度场 $\mathbf{v}_t = g_\theta(\mathbf{h}_t)$

其中 $\mathbf{z}_t$ 是图像经 Stable Diffusion VAE 编码器 $E$ 压缩后的潜在表示 $\mathbf{z} = E(\mathbf{x}) \in \mathbb{R}^{32 \times 32 \times 4}$，再经扩散过程加噪得到。

### 3. REPA 对齐机制

**核心思想**：将编码器的中间隐藏状态 $\mathbf{h}_t$ 与预训练自监督视觉编码器 $f$ 从干净图像 $\mathbf{x}_*$ 提取的表示 $\mathbf{y}_* = f(\mathbf{x}_*)$ 对齐。

**投影头**：引入一个可训练的投影头 $h_\phi$（实现为 MLP），将 $\mathbf{h}_t$ 映射到与 $\mathbf{y}_*$ 相同的特征空间：

$$h_\phi(\mathbf{h}_t) \in \mathbb{R}^{N \times D}$$

其中 $N$ 为 patch 数量，$D$ 为目标表示维度。

**REPA 损失**：通过最大化投影表示与目标表示之间的逐块相似度实现对齐：

$$\mathcal{L}_{\mathrm{REPA}}(\theta, \phi) := -\mathbb{E}_{\mathbf{x}_*, \epsilon, t} \Big[ \frac{1}{N} \sum_{n=1}^{N} \mathrm{sim}(\mathbf{y}_*^{[n]}, h_\phi(\mathbf{h}_t^{[n]})) \Big]$$

其中 $\mathbf{y}_*^{[n]}$ 和 $\mathbf{h}_t^{[n]}$ 分别表示第 $n$ 个 patch 的目标表示和隐藏状态，$\mathrm{sim}(\cdot, \cdot)$ 为余弦相似度（实验表明负余弦相似度与 NT-Xent 效果相当，最终选用前者）。

### 4. 总训练目标

REPA 作为正则化项与原始速度预测损失联合优化：

$$\mathcal{L} := \mathcal{L}_{\mathrm{velocity}} + \lambda \mathcal{L}_{\mathrm{REPA}}$$

其中 $\lambda$ 控制正则化强度。消融实验表明（Table 5），$\lambda$ 从 0.25 增至 0.5 时 FID 持续改善，之后趋于饱和（$\lambda=0.5$ 时 FID=7.9，$\lambda=1.0$ 时 FID=7.8）。

### 5. 关键设计选择

- **对齐深度**：REPA 损失仅施加于 Transformer 前几层（默认前 8 层）。组件分析（Table 2）表明，对齐深度 6-8 层时生成性能最优（FID=10.0），对齐更深层反而下降。这暗示前几层负责语义建模，后几层聚焦高频细节。
- **目标编码器**：默认使用 DINOv2（Oquab et al., 2024）作为对齐目标，实验显示更强的编码器同时提升判别性能和生成质量（Figure 5a）。REPA 对 MoCov3-L 和 MAE-L 等不同目标表示均有效（Figure 8），表明方法具有通用性。
- **架构配置**：沿用 DiT（Peebles & Xie, 2023）和 SiT（Ma et al., 2024a）的 B/2、L/2、XL/2 架构（Table 1），patch size 为 2，处理 $32 \times 32$ 的潜在空间。

### 补充图表

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2410_06940/figures/002_Figure_2.jpg]]
*Figure 2: Alignment behavior for a pretrained SiT model. We empirically investigate the feature alignment between*



## 实验与关键发现

### 核心发现

REPA 的核心价值在于以极小的实现代价换取了显著的训练加速与生成质量提升。在 ImageNet 256×256 类条件生成任务上，REPA 使 SiT-XL/2 模型的收敛速度提升超过 17.5 倍——仅需不到 400K 次迭代即可匹配原始 SiT-XL/2 训练 7M 次迭代的性能（无分类器指导，FID 分别为 7.9 与 8.3，见 Table 3）。在引入无分类器指导（CFG）与引导间隔后，REPA 进一步将 FID 推至 1.42，达到当时的最先进水平（Table 4）。

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2410_06940/figures/010_Table_3.jpg]]
*Table 3: FID comparisons with vanilla DiTs and SiTs on ImageNet 256×256. We do not use classifier-free guidance (CFG). ↓ denotes lower values are better. Iter. indicates the training iteration*

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2410_06940/figures/011_Table_4.jpg]]
*Table 4: System-level comparison on ImageNet 256×256 with CFG. ↓ and ↑ indicate whether lower or higher values are better, respectively. Results that include additional CFG scheduling are marked with an asterisk (*), where the guidance interval from (Kynka¨anniemi et al. ¨ , 2024) is applied for REPA*

### 主要结果

**无分类器指导下的效率对比（Table 3）**：在公平的实验设置下（相同批量大小、学习率与评估协议），REPA 对 DiT 和 SiT 两种扩散变压器架构均带来一致的 FID 改善。以 SiT-XL/2 为例，REPA 在 400K 迭代时 FID 为 7.9，优于原始模型 7M 迭代的 8.3；DiT-XL/2 在 400K 迭代时 FID 从原始模型的 19.2 降至 12.3。这一结果表明，REPA 的加速效应不依赖于特定的扩散框架。

**有分类器指导下的系统级对比（Table 4）**：当结合 CFG 与引导间隔（Kynkäänniemi et al., 2024）时，SiT-XL/2+REPA 在 4M 迭代下取得 FID=1.42、sFID=4.06、IS=328.8 的综合指标，全面超越此前的方法。即使在未使用引导间隔的情况下，REPA 也将 FID 从原始 SiT 的 2.06 降至 1.80。

**高分辨率扩展（Table 11）**：在 ImageNet 512×512 任务上，SiT-XL/2+REPA 仅训练 200 个 epoch 即取得 FID=2.08，优于原始 SiT-XL/2 训练 600 个 epoch 的 2.62，表明 REPA 的加速效应可跨分辨率迁移。

**文本到图像生成（Table 12）**：在 MS-COCO 上，REPA 同样展现出对文本条件扩散模型的改善能力，验证了该方法在跨模态场景下的初步可扩展性。

### 组件分析

Table 2 系统拆解了 REPA 各设计选择对 SiT-L/2 在 400K 迭代下的影响（无 CFG，NFE=250）：

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2410_06940/figures/006_Table_2.jpg]]
*Table 2: Component-wise analysis on ImageNet 256×256. All models are SiT-L/2 trained for 400K iterations. All metrics except accuracy (Acc.) are measured with the SDE Euler-Maruyama sampler with NFE=250 and without classifier-free guidance. For Acc., we report linear probing results on the ImageNet validation set using the latent features aligned with the target representation. We fix λ = 0.5 here. ↓ and ↑ indicate whether lower or higher values are better, respectively*

- **目标表示（Target Encoder）**：与 DINOv2-B 对齐时 FID 从原始模型的 18.8 降至 9.7；使用更强的 DINOv2-L 进一步降至 10.0，同时线性探测准确率从 53.2% 提升至 68.9%。这表明更强的预训练编码器能同时提升生成质量与判别表示质量。
- **对齐深度（Depth）**：仅在前 8 层应用 REPA 即可获得最佳 FID（10.0），对齐更深层（如第 20 层）反而导致 FID 回升至 11.3。这一反直觉现象揭示了扩散变压器的分层功能分工：浅层负责语义对齐，深层专注于高频细节合成。
- **相似度函数（Similarity）**：负余弦相似度（cos. sim.）与 NT-Xent 效果相当（FID 分别为 10.0 与 10.1），但余弦相似度实现更简洁，因此被选为默认配置。

### 消融实验

**正则化系数 λ（Table 5）**：λ 从 0.25 增至 0.5 时 FID 从 8.3 改善至 7.9，继续增大至 1.0 时 FID 为 7.8，性能趋于饱和。这表明 REPA 的正则化强度存在一个较宽的鲁棒区间，无需精细调参即可获得接近最优的性能。

**预训练编码器的数据集影响（Table 6）**：不同预训练数据集（ImageNet-1K vs. ImageNet-21K）对最终生成性能的影响有限，说明 REPA 主要受益于表示质量本身而非数据规模。

### 可扩展性分析

Figure 5 从三个维度揭示了 REPA 的扩展特性：

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2410_06940/figures/008_Figure_5.jpg]]
*Figure 5: Scalability of REPA. (a) Linear probing vs. FID plot of REPA with different target encoders (400K iterations). A stronger encoder improves both discrimination and generation performance. (b) The relative improvement of REPA over the vanilla model becomes increasingly significant as the model size grows. (c) With a fixed target encoder, larger models reach better performance more quickly. In the line plot, results are marked at 50K, 100K, 200K, and 400K iters*

1. **编码器强度**（Figure 5a）：更强的目标编码器在 FID-线性探测准确率平面上形成清晰的帕累托前沿，即更强的表示同时推动生成与判别性能的联合提升。
2. **模型规模**（Figure 5b）：REPA 的相对收益随模型规模增大而递增——在 SiT-B/2 上 FID 改善约 2 点，在 SiT-XL/2 上改善超过 10 点。这表明大模型对表示正则化的需求更为迫切。
3. **训练效率**（Figure 5c）：在固定目标编码器下，更大模型以更少的迭代达到更低的 FID，REPA 的加速效应与模型规模正相关。

### 表示差距的定量证据

**跨时间步分析（Figure 7）**：通过线性探测与 CKNNA 两种度量，REPA 在不同扩散噪声水平下一致缩小了扩散模型与 DINOv2 之间的表示差距。原始 SiT 在高噪声时间步的表示质量急剧下降，而 REPA 模型在所有时间步均维持较高的表示质量。

**对齐泛化性（Figure 8）**：REPA 不仅对 DINOv2 有效，对 MoCov3-L 和 MAE-L 等不同类型的自监督表示同样能显著提升 CKNNA 对齐度，验证了该方法的通用性。

### 定性分析

**早期训练可视化（Figure 4）**：在训练的前 400K 迭代内，REPA 模型生成的图像在全局结构与局部纹理上均明显优于原始模型，即使两者共享相同的噪声、采样器和采样步数。这直观地印证了表示对齐对生成质量的加速效应。

**特征可视化（Figure 38）**：PCA 可视化显示，SiT-XL/2+REPA 的逐层特征图呈现出由粗到细的层次化结构，而原始 SiT 在高噪声水平下的特征图呈现明显的噪声模式。这为“浅层语义对齐、深层细节合成”的功能分工提供了视觉证据。

### 失败模式与局限性

1. **深层对齐的退化**：当 REPA 应用于 Transformer 的后几层时，生成性能反而下降（Table 2）。目前缺乏对这一现象的理论解释，可能源于深层表示已被强约束于去噪任务，额外的语义对齐与去噪目标产生冲突。
2. **模态与架构限制**：所有实验均在潜在扩散模型（基于 Stable Diffusion VAE）上进行，尚未在像素级扩散模型或视频等其他模态上验证。在大规模通用文本到图像场景下，仅通过 MS-COCO 进行了初步验证，更广泛的可扩展性有待确认。
3. **时间加权缺失**：当前 REPA 对所有扩散时间步施加均匀的正则化权重。考虑到不同噪声水平下表示学习的难度不同，设计时间加权的 REPA（如在高噪声阶段加强对齐）可能进一步提升性能，但尚未被探索。

### 证据强度评估

| 核心主张 | 证据类型 | 置信度 |
|---------|---------|-------|
| REPA 使 SiT 训练加速 >17.5× | Table 3 定量对比 | 高（0.95） |
| REPA 在无 CFG 下 FID=7.9 优于原始 SiT 的 8.3 | Table 3 直接对比 | 高（0.98） |
| REPA 结合 CFG+引导间隔取得 FID=1.42 | Table 4 系统级对比 | 高（0.95） |
| 仅前几层对齐即足够 | Table 2 深度消融 | 高（0.90） |
| 对齐更深层导致性能下降 | Table 2 深度消融 | 高（0.90） |
| REPA 在高分辨率下同样有效 | Table 11 跨分辨率实验 | 中高（0.90） |

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2410_06940/figures/047_Table_11.jpg]]
*Table 11: System-level comparison on ImageNet 512×512. We use CFG with w = 1.35*

总体而言，REPA 的核心主张有充分的定量消融与跨架构/跨分辨率实验支撑，证据链完整且一致。关于深层对齐退化的理论解释和跨模态泛化性是目前的主要开放问题，需要后续工作进一步探索。

### 补充图表

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2410_06940/figures/012_Figure_7.jpg]]
*Figure 7: Representation gap across different timesteps. We plot the linear probing results and maximum CKNNA values (using DINOv2- g) at different timesteps, comparing the vanilla SiT-XL/2 model and the same model trained using REPA. REPA consistently reduces the representation gap across different noise levels*

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2410_06940/figures/013_Table_5.jpg]]
*Table 5: Ablation study for λ*

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2410_06940/figures/050_Figure_38.jpg]]
*Figure 38: PCA visualization of layer-wise features of SiT-XL/2 and SiT-XL/2+REPA*

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2410_06940/figures/004_Figure_4.jpg]]
*Figure 4: REPA improves visual scaling. We compare the images generated by two SiT-XL/2 models during the first 400K iterations, with REPA applied to one of the models. Both models share the same noise, sampler, and number of sampling steps, and neither uses classifier-free guidance*



## 定位与知识库关联

### 1. 核心基线与方法锚点

REPA建立在两大基线架构之上：

- **DiT**（Peebles & Xie, 2023）：扩散变压器（Diffusion Transformer）的奠基性工作，将标准ViT架构引入扩散模型的潜在空间去噪过程，取代了传统的U-Net骨干网络。
- **SiT**（Ma et al., 2024a）：基于随机插值（stochastic interpolant）框架的扩散变压器，将生成过程建模为数据与噪声之间的连续时间插值，通过速度场预测实现更高效的采样。

REPA在这两个基线上的改动极为集中——仅在损失函数层面增加一项正则化项，不修改模型架构、采样器或数据流水线。具体而言：

- **基线损失**：仅包含去噪/速度预测损失（如SiT中的 $\mathcal{L}_{\mathrm{velocity}}$ 或DiT中的 $\mathcal{L}_{\mathrm{simple}}$）。
- **REPA损失**：原始损失 + $\lambda \cdot \mathcal{L}_{\mathrm{REPA}}$，其中 $\mathcal{L}_{\mathrm{REPA}}$ 最大化扩散变压器隐藏状态的逐块投影与预训练自监督表示之间的余弦相似度。

这种“零架构改动”的设计使得REPA可即插即用地应用于任何基于变压器的扩散模型，无需重新设计骨干网络或调整训练策略。

### 2. 与表示学习方法的谱系关系

REPA的核心思想——将预训练视觉表示蒸馏到生成模型中——与以下方法谱系存在交叉与边界：

**对比学习与自监督表示**：REPA的对齐目标来自预训练自监督视觉编码器，主要使用**DINOv2**（Oquab et al., 2024），同时验证了对**MoCov3**和**MAE**等编码器的兼容性。对齐损失函数直接借鉴了对比学习中的NT-Xent（Chen et al., 2020a）和负余弦相似度。但与SimCLR等方法不同，REPA不是从头学习表示，而是将已有的强表示作为“教师信号”注入生成模型。

**知识蒸馏在生成模型中的应用**：REPA属于表示蒸馏（representation distillation）范畴，但与传统的logit蒸馏或特征匹配不同，它对齐的是扩散过程中间层（前几层）的隐藏状态与干净图像的表示，而非最终输出或教师模型的特征。这种“跨噪声水平”的对齐是REPA的独特之处。

**与扩散模型正则化方法的区别**：已有工作通过对比学习或自监督目标增强扩散模型训练，但REPA的关键差异在于：(1) 仅对齐前几层而非全部层；(2) 使用外部预训练编码器而非在线学习的表示；(3) 对齐目标是干净图像的表示而非噪声图像的表示。这三点共同构成了REPA的方法边界。

### 3. 适用边界与已验证范围

**已验证的有效域**：
- **图像生成**：ImageNet 256×256和512×512的类条件生成，MS-COCO文本到图像生成
- **骨干网络**：DiT和SiT架构的B/2、L/2、XL/2变体
- **目标编码器**：DINOv2（主要）、MoCov3-L、MAE-L
- **潜在空间**：基于Stable Diffusion VAE的压缩表示（$\mathbf{z} \in \mathbb{R}^{32\times32\times4}$）

**未验证的边界**（论文明确指出的局限）：
- 像素级扩散模型（仅在潜在扩散模型上验证）
- 视频生成或其他数据模态
- 大规模通用文本到图像生成（仅MS-COCO初步验证）
- 时间加权的REPA（根据扩散噪声时间步动态调整 $\lambda$）

### 4. 开放问题与理论缺口

**机制层面的未解问题**：
1. **为什么前几层对齐最有效？** 实验表明仅对齐前8层即可获得最佳生成性能，对齐更深层反而有所下降。论文推测前几层负责语义理解，后几层专注于高频细节，但缺乏严格的理论解释。
2. **去噪目标与实例判别目标的理论关联**：REPA本质上是将去噪扩散目标与实例判别（instance discrimination）目标耦合，二者之间的理论关系尚不明确。
3. **跨模态泛化机制**：REPA在图像领域的成功是否源于视觉表示的特定属性，还是可以迁移到其他模态的通用表示对齐框架？

**工程层面的待探索方向**：
- 时间加权的REPA损失（根据噪声水平动态调整对齐强度）
- 与其他扩散模型加速技术的组合效应（如蒸馏采样、一致性模型等）
- 在更大规模模型（如DiT-G/2及以上）上的表现上限

### 5. 证据强度评估

**高置信度结论**（需手动核实的具体数值除外）：
- REPA在SiT-XL/2上以400K迭代达到FID=7.9，匹配原始SiT-XL/2训练7M步的8.3，加速比>17.5倍
- 使用无分类器指导+引导间隔达到FID=1.42的最先进结果
- 与DINOv2对齐后，SiT-L/2的FID从18.8降至10.0（400K迭代）

**需手动验证的声明**：
- 文本到图像生成（MS-COCO）的定量对比结果（Table 12）在分析中缺乏具体数值锚点，建议查阅原文确认
- ImageNet 512×512的FID对比（Table 11）仅给出部分数据，完整对比需核实原文
- 不同目标编码器的数据集差异对性能的影响（Table 6）在分析中未展开，可能影响公平性判断

**公平性说明**：所有实验均严格遵循DiT和SiT的官方实现设置，使用相同的批量大小（256）、学习率和评估协议，确保与基线的公平比较。



## 原文 PDF

![[paperPDFs/ICLR_2025/REPA_Representation_Alignment_for_Generation_Training_Diffusion_Transformers_Is_Easier_Than_You_Think.pdf]]
