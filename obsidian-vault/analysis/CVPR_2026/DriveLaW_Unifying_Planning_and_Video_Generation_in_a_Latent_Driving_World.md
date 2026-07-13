---
title: "DriveLaW: Unifying Planning and Video Generation in a Latent Driving World"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/DriveLaW_Unifying_Planning_and_Video_Generation_in_a_Latent_Driving_World.pdf
project_link: null
code_link: "https://github.com/xiaomiresearch/drivelaw"
aliases:
- DriveLaW
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/generative_models_diffusion
core_operator: 将视频生成扩散模型中的中间去噪潜在特征（mid-denoising video latents）作为规划扩散模型的条件输入，实现从生成到规划的链式统一表征。
primary_logic: 大规模视频生成学得的中间潜在表示蕴含丰富的驾驶先验（场景语义、智能体动态、物理一致性），可作为强规划状态，无需额外的BEV或VLM特征工程。
claims:
- 通过将视频生成器的潜在表征直接注入规划器，DriveLaW 确保了高保真未来生成与可靠轨迹规划之间的内在一致性。
- DriveLaW 是首个利用视频生成器的中间潜在特征作为规划表征的方法，实现了更稳定的闭环驾驶。
- 视频潜在特征作为扩散条件显著优于 BEV 特征 (PDMS 89.1 vs 84.1) 和 VLM 隐藏状态 (89.1 vs 86.5)，验证了链式生成表征的优越性。
- 扩展视频预训练数据量 (0→7.6M samples) 将 PDMS 从 85.9 提升至 89.1，证明大规模视频生成学习对规划的迁移价值。
---

# DriveLaW: Unifying Planning and Video Generation in a Latent Driving World

> [!tip] 核心洞察
> 大规模视频生成学得的中间潜在表示蕴含丰富的驾驶先验（场景语义、智能体动态、物理一致性），可作为强规划状态，无需额外的BEV或VLM特征工程。

| 字段 | 内容 |
|------|------|
| 中文题名 | DriveLaW：在潜在驾驶世界中统一规划与视频生成 |
| 英文题名 | DriveLaW: Unifying Planning and Video Generation in a Latent Driving World |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Xia_DriveLaW_Unifying_Planning_and_Video_Generation_in_a_Latent_Driving_CVPR_2026_paper.html) · [Code](https://github.com/xiaomiresearch/drivelaw) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/generative_models_diffusion |
| Method | DriveLaW |
| Dataset | nuScenes validation, NAVSIM Navtest |

> [!tip] 效果简介
> - nuScenes validation (single-view video generation) 上，FID↓ 4.6 vs 6.9 (Vista) (-33.3%)。
> - nuScenes validation 上，FVD↓ 81.3 vs 82.8 (Epona) (-1.8%)。
> - NAVSIM Navtest (closed-loop planning) 上，PDMS↑ 89.1 vs 88.1 (PWM) (+1.0)。

## 概要

自动驾驶世界模型长期面临一个结构性的瓶颈：视频生成（未来帧预测）与运动规划被设计为两个解耦的模块。生成模型虽然内化了丰富的物理规律和场景语义，但规划器通常依赖显式的 BEV 特征或 VLM 隐藏状态进行决策，导致从生成到规划的**表征断裂**，闭环稳定性不足。

DriveLaW 的核心洞见在于：大规模视频生成扩散模型在去噪过程中产生的**中间潜在特征**（mid-denoising video latents）天然蕴含了场景语义、智能体动态和物理一致性等驾驶先验，可以直接作为规划器的强条件输入。基于这一洞见，DriveLaW 将视频生成与轨迹规划**链式耦合**——将 Video DiT 的去噪潜在特征注入 Action DiT 规划器，实现了从生成到规划的统一表征。

具体而言，DriveLaW 由两个核心组件构成：

- **DriveLaW-Video**：基于时空 VAE 和 Video DiT 的世界模型，引入噪声重注入机制（Noise Reinjection）以在激进压缩下恢复高频细节，负责高保真未来帧生成。
- **DriveLaW-Act**：基于流匹配的扩散规划器（Action DiT），以 Video DiT 的中间潜在特征为条件直接生成轨迹，无需额外的 BEV 或 VLM 特征工程。

训练采用**三阶段渐进式课程**：先学习长时段运动，再细化空间细节，最后链式微调规划器，确保训练稳定。

在实验上，DriveLaW 在 nuScenes 单视图视频生成中 FID 达到 4.6（较先前最优方法 Vista 提升 33.3%），FVD 达到 81.3；在 NAVSIM 闭环规划基准上 PDMS 达到 89.1，刷新纪录。消融实验进一步证实：视频潜在特征作为规划条件显著优于 BEV 特征（PDMS 89.1 vs 84.1）和 VLM 隐藏状态（89.1 vs 86.5），且扩展视频预训练数据量（0→7.6M 样本）可将 PDMS 从 85.9 提升至 89.1，验证了大规模视频生成学习对规划的迁移价值。



### 自动驾驶世界模型的表征断裂困境

自动驾驶系统需要在高度动态和不确定的环境中同时完成未来场景预测与运动规划。近年来，世界模型（world models）作为学习环境动态的内部表征工具，在视频生成和规划任务中展现出巨大潜力。然而，现有世界模型方法普遍存在一个深层瓶颈：**视频生成与运动规划被解耦为两个独立或弱耦合的模块**，导致规划器无法直接利用生成模型在大量视频数据中学到的物理规律和场景语义。

具体而言，当前主流范式存在两类表征断裂：

1. **并行生成-规划架构**：以 **Epona**（Zhang et al., ICCV 2025）为代表的统一世界模型，虽然同时输出未来视频和规划轨迹，但其规划模块仍依赖显式的 BEV（Bird's-Eye-View）特征或 VLM（Vision-Language Model）隐藏状态作为输入条件，而非直接复用视频生成过程中形成的内部表征。这种设计使得规划器与生成器在表征空间上存在鸿沟，生成模型内化的智能体动态、物理一致性和场景语义无法有效传递至规划决策。

2. **分离式流水线架构**：**DriveVLA-W0**（Li et al., arXiv 2025）等方法将世界模型作为监督信号训练端到端规划器，但世界模型本身并不参与推理阶段的规划过程；**PWM**（Zhao et al., NeurIPS 2025）等预测-规划统一模型则侧重于任务层面的联合优化，未在表征层面实现深度耦合。这些方法虽然取得了一定进展，但均未解决一个核心问题——**如何让规划直接受益于视频生成模型从大规模数据中学到的强驾驶先验**。

上述表征断裂带来的直接后果是**闭环稳定性不足**：当规划器仅依赖人工设计的特征工程（如 BEV 编码）或与生成过程脱节的 VLM 表征时，其对场景动态的理解往往是浅层的，难以在复杂交互场景中做出与未来视觉演化一致的安全决策。

### 链式生成-规划范式的动机

本文的核心洞察在于：**大规模视频生成模型在去噪过程中形成的中间潜在表征，天然蕴含了丰富的驾驶先验**——包括场景语义布局、智能体运动趋势、物理一致性约束等。这些表征是在海量驾驶视频的生成学习中被隐式编码的，其信息密度和任务相关性远超人工设计的 BEV 特征或通用 VLM 隐藏状态。

基于此，DriveLaW 提出了一种**链式耦合（chained coupling）** 范式：将视频生成扩散模型中的中间去噪潜在特征（mid-denoising video latents）直接注入规划扩散模型作为条件输入，实现从生成到规划的端到端表征共享。这一设计打破了传统分离式架构的表征壁垒，使得规划器能够“看见”生成器所“预见”的未来。

该范式的关键优势在于：
- **表征一致性**：规划与生成共享同一潜在空间，确保规划轨迹与预测的未来视觉场景内在对齐；
- **数据效率**：视频生成模型的大规模预训练（百万级样本）可迁移至规划任务，减少对昂贵规划标注数据的依赖；
- **架构简洁性**：无需额外的 BEV 编码器或 VLM 特征提取器，规划器直接以视频潜在特征为条件进行流匹配扩散。

### 本文贡献与章节导引

DriveLaW 的主要贡献包括：
1. 首次将视频生成器的中间潜在特征作为规划表征，实现生成与规划的链式统一；
2. 提出噪声重注入机制（Noise Reinjection）以在激进压缩下保持视频生成的高频细节和结构一致性；
3. 设计三阶段渐进式课程训练策略，稳定地联合优化视频生成与规划模块；
4. 在 nuScenes 视频生成和 NAVSIM 闭环规划基准上均取得 state-of-the-art 性能。

后续章节将依次展开：相关工作对比、DriveLaW-Video 和 DriveLaW-Act 的详细设计、三阶段训练策略，以及全面的实验验证与消融分析。



## 核心方法与创新机理

### 问题瓶颈：规划与生成之间的表征断裂

当前驾驶世界模型的主流范式将视频生成与运动规划视为两个独立或仅松散耦合的任务。以 **Epona**（Zhang et al., ICCV 2025）为代表的统一世界模型采用并行架构，规划模块依赖显式的 BEV 特征或 VLM 隐藏状态作为条件输入，而视频生成器内化的丰富场景语义和物理规律并未直接参与规划过程。这种解耦设计导致两个关键问题：

1. **表征断裂**：生成模型通过大规模视频预训练学得的中间潜在表示蕴含了场景语义、智能体动态和物理一致性等强驾驶先验，但这些信息在流向规划模块时被丢弃，规划器只能从人工设计的特征工程（如 BEV 栅格化或 VLM 编码）中重新提取环境理解。
2. **闭环稳定性不足**：由于规划轨迹与未来视觉演化之间缺乏内在一致性约束，生成的高保真视频与规划的可靠轨迹难以保证在物理层面相互对齐，限制了闭环驾驶性能的上限。

### 核心洞察：中间去噪潜在特征作为强规划状态

DriveLaW 的核心洞察是：**大规模视频生成扩散模型在去噪过程中产生的中间潜在特征（mid-denoising video latents），天然蕴含了丰富的驾驶先验，可以直接作为规划器的条件输入，无需额外的 BEV 或 VLM 特征工程**。

具体而言，视频扩散模型在从纯噪声逐步去噪生成未来帧的过程中，其内部潜在变量 $z_t$ 在不同去噪步骤 $t$ 编码了不同粒度的场景信息——早期步骤（$t$ 较大）包含粗粒度的场景布局和运动趋势，中期步骤则融合了精细的语义和几何细节。通过从去噪轨迹的中间步骤提取特征 $h_t = \phi_{\theta}(z_t)$，可以构建一个信息密集的感知潜在变量，直接注入规划扩散模型。

这一设计的因果逻辑是链式的：视频生成器首先将历史观测（图像、动作）压缩为统一的潜在世界表征，然后通过去噪过程逐步“想象”未来场景演化；规划器则直接读取这一想象过程中的中间表征，生成与视觉演化内在一致的轨迹。这种链式耦合确保了“所见即所规划”，从根本上解决了表征断裂问题。

### 关键变更槽位（Changed Slots）

相较于现有方法，DriveLaW 在以下四个维度实现了根本性创新：

#### 1. 规划与生成的耦合方式：从并行到链式

| 维度 | 基线方法 | DriveLaW |
|------|----------|----------|
| 耦合架构 | 并行或分离训练，生成与规划之间仅通过最终输出间接关联 | 链式耦合，规划器直接以视频生成器的中间潜在特征为条件 |
| 信息流 | 生成 → 解码为像素 → 规划器重新编码，或规划器使用独立特征提取器 | 生成器去噪过程的潜在变量直接注入规划器，形成端到端的潜在空间信息流 |

这一变更的证据来自论文核心声明：“By directly injecting the latent representation from its video generator into the planner, DriveLaW ensures inherent consistency between high-fidelity future generation and reliable trajectory planning.”（摘要）DriveLaW 被明确标定为“首个利用视频生成器的中间潜在特征作为规划表征的方法”（Sec. 2.1）。

#### 2. 规划器条件输入：从 BEV/VLM 到视频潜在特征

消融实验（Table 5）提供了决定性证据：在 NAVSIM Navtest 闭环规划基准上，使用视频潜在特征作为扩散条件的 PDMS 达到 **89.1**，显著优于 BEV 特征的 **84.1**（+5.0）和 VLM 隐藏状态的 **86.5**（+2.6）。这一结果直接验证了链式生成表征相较于传统显式特征工程的优越性——视频生成器在去噪过程中自发涌现的场景理解，比人工设计的 BEV 栅格或 VLM 编码更适配规划任务。

#### 3. 视频生成质量优化：噪声重注入机制

为平衡激进压缩与视觉保真度之间的矛盾，DriveLaW 引入了**噪声重注入机制（Noise Reinjection）**。该机制通过以下步骤恢复高频细节：

- 计算拉普拉斯响应图 $H_f$ 并基于自适应阈值 $\tau = \beta \cdot \mathrm{std}(H_f)$ 生成高频区域掩码 $M_f$（Eq. 5）；
- 在掩码区域注入受控噪声，生成扰动潜在变量 $L_t' = L_t + \sigma_t' \cdot M \odot \varepsilon_t$（Eq. 6）；
- 对扰动后的潜在变量进行额外去噪步骤，促使模型重新生成高频细节。

如图 2 所示，该机制有效恢复了动态物体和道路标记的锐度与纹理，同时保持了天空等区域的自然平滑度，解决了基线方法中常见的模糊、结构不一致和伪影问题。

#### 4. 训练策略：三阶段渐进式课程

DriveLaW 采用三阶段渐进式训练策略，解决了链式架构中视频生成与规划联合训练的稳定性问题：

- **阶段一**：低分辨率长序列学习——使用低分辨率（如 256×256）的长视频片段（如 25 帧）训练视频生成器，使其掌握长时段运动建模能力；
- **阶段二**：高分辨率短序列精炼——切换到高分辨率（如 512×512）的短视频片段，细化空间细节和纹理质量；
- **阶段三**：链式微调——将视频生成器的中间潜在特征注入规划器，联合微调视频 DiT 和动作 DiT，实现从生成到规划的端到端对齐。

消融实验（Table 7）证明，完整的三阶段训练同时取得了最低的 FID（4.6）和 FVD（81.3），优于仅使用单阶段或双阶段的训练方案。此外，视频预训练数据规模的扩展实验（Table 4）显示，将预训练样本从 0 增至 7.6M，PDMS 从 85.9 提升至 89.1，验证了大规模视频生成学习对规划任务的迁移价值。

### 创新边界与待验证问题

DriveLaW 的创新聚焦于单视图设定下的链式生成-规划统一架构。论文明确指出的局限性包括：未测试多相机输入或交互式闭环驾驶场景。以下问题需要进一步验证：

- **多视图扩展**：当前架构仅处理单视图输入，如何扩展到多相机一致生成与规划是实际部署的关键挑战；
- **噪声重注入的自动化**：自适应阈值 $\tau$ 依赖超参数 $\beta$，其跨场景泛化性需要更系统的调优研究；
- **实时性优化**：链式架构涉及两次扩散过程（视频生成 + 轨迹规划），推理延迟是否满足实时驾驶需求尚待评估；
- **规模定律**：视频预训练数据量与模型规模之间的关系曲线尚未完整刻画，更大规模预训练的收益边界仍不明确。



DriveLaW 的核心理念是将视频生成与运动规划**链式耦合**：不再将世界模型仅作为独立的预测器，而是将其扩散去噪过程中产出的中间潜在特征直接注入规划器，作为强驾驶先验。这一设计使得规划器能够内化视频生成模型从大规模数据中学得的场景语义、智能体动态与物理一致性，从而在生成与规划之间建立**内在一致性**。

### 模块架构

DriveLaW 由两个核心模块构成，并通过统一的潜在空间实现表征共享：

- **DriveLaW-Video（世界模型）**：基于时空 VAE 与 Video DiT 的高保真未来帧生成器。该模块将历史观测（图像、自车动作）编码为潜在世界表征，执行多步扩散去噪以生成未来视频帧。为平衡压缩率与视觉保真度，模型引入了**噪声重注入机制**（Noise Reinjection），在去噪早期阶段对高频区域施加受控噪声扰动，促使模型重新生成锐利细节与稳定结构（Fig. 2）。

- **DriveLaW-Act（规划器）**：基于流匹配的轻量级 Action DiT，以 DriveLaW-Video 在去噪过程中产出的**中间视频潜在特征**（mid-denoising video latents）为条件，生成与场景演化对齐的未来轨迹。具体而言，规划器从 Video DiT 的特定去噪步骤 $t^\star$ 提取特征 $h_{t^\star}$，将其作为扩散条件注入 Action DiT 的去噪过程，驱动轨迹生成。

### 数据流与输入输出

整体数据流如 Fig. 1 所示，遵循“编码→生成→规划”的链式通路：

![[assets/figures/papers/paper_list_l2467_https_openaccess_thecvf_com_content_CVPR2026_html_Xia_DriveLaW_Unifying/figures/001_Figure_1.jpg]]
*Figure 1: Overview of the overall architecture of DriveLaW. The model first encodes historical observations (images, actions) into a unified latent world representation through a powerful video diffusion model. In order to improve the generation quality, we introduced the Noise Reinjection mechanism to explore and select the optimal generation path in the early stage of denoising. The denoised video latents produced by the Video DiT are then passed as conditioning signals to the action planner. Leveraging these latents, the lightweight Action DiT predicts future trajectories that are aligned with the visual scene evolution. In this chained design, the Video Model and Action Model share the same laten...*

1. **输入**：历史多帧图像序列与自车动作序列。
2. **编码**：时空 VAE 将原始观测压缩至紧凑的潜在空间。
3. **视频生成**：Video DiT 在条件 $c$（包含历史上下文与运动提示）下执行去噪，产生去噪轨迹 $z_{t-1} = \Psi_{\theta}(z_t, t, c)$。在此过程中，模型从中间步骤提取特征 $h_t = \phi_{\theta}(z_t)$，构成感知潜在变量。
4. **噪声重注入**：在去噪早期，模型计算高频区域掩码 $M_f(x, y)$，并对掩码区域注入受控噪声 $L_t' = L_t + \sigma_t' \cdot M \odot \varepsilon_t$，以恢复高频细节。
5. **规划**：Action DiT 接收缓存的视频潜在特征 $\{f_i\}_{i=1}^{B}$ 与驾驶上下文编码 $h_{\mathrm{ctx}} = E_{\mathrm{ctx}}([s_t; g_t])$，通过流匹配目标 $\mathcal{L}_{\mathrm{FM}} = \mathbb{E}_{t, a_0, \epsilon}\big[\big\|f_{\theta}(a_t, t) - (a_0 - \epsilon)\big\|_2^2\big]$ 生成最终轨迹。

### 训练策略

为稳定训练并兼顾长时序运动建模与空间细节保真，DriveLaW 采用**三阶段渐进式课程训练**：

- **阶段一**：低分辨率长序列视频预训练，学习长时段运动模式。
- **阶段二**：高分辨率短序列微调，细化空间细节与纹理质量。
- **阶段三**：冻结或部分解冻 Video DiT，将视频潜在特征链式注入规划器，进行联合微调。

消融实验证实，三阶段训练策略同时取得了最优的视频生成质量（FID 4.6, FVD 81.3），优于仅单阶段或双阶段训练方案（Table 7）。

### 关键设计决策

与现有世界模型方法的根本差异在于**规划与生成的耦合方式**：Epona（Zhang et al., ICCV 2025）等并行架构将生成与规划分离训练，规划模块依赖显式的 BEV 特征或 VLM 隐藏状态；而 DriveLaW 直接复用视频生成器内部的中间潜在表征，避免了额外的特征工程。表征消融实验表明，视频潜在特征作为扩散条件显著优于 BEV 特征（PDMS 89.1 vs 84.1）和 VLM 隐藏状态（89.1 vs 86.5），验证了链式表征的优越性（Table 5）。

此外，**去噪步骤的选择**对规划性能至关重要：在去噪早期（$t=1$）提取的视频潜在特征可获得最强规划性能（PDMS 89.1），而越接近完全去噪（$t=10$）性能急剧下降至 23.2，表明噪声中蕴含的语义信息对规划具有关键价值（Table 6）。



### 3.1 链式生成-规划统一架构

DriveLaW 的核心创新在于将视频生成与运动规划构建为**链式耦合**架构，而非传统的并行或分离设计。其关键洞察是：大规模视频生成扩散模型在去噪过程中习得的中间潜在表示，蕴含了丰富的驾驶先验——包括场景语义、智能体动态和物理一致性——这些表示可以作为强规划状态直接注入规划器，无需额外的 BEV 或 VLM 特征工程。

架构由两个核心模块串联构成：

- **DriveLaW-Video（世界模型）**：基于时空 VAE 与 Video DiT 的视频生成器，负责从历史观测（图像、动作）生成高保真未来帧预测。其内部去噪过程产生的中间潜在特征，承载了场景演化的结构化信息。
- **DriveLaW-Act（规划器）**：基于流匹配的轻量级扩散规划器（Action DiT），以 Video DiT 的中间去噪潜在特征为条件，生成与视觉场景演化对齐的未来轨迹。

这种链式设计的本质优势在于：规划器直接复用视频生成模型内化的物理规律和场景语义，避免了传统方法中从生成表征到规划表征的“翻译”断裂，从而实现了高保真未来生成与可靠轨迹规划之间的内在一致性。

### 3.2 中间去噪特征提取

视频扩散模型的标准去噪过程可描述为单步潜在更新：

$$z_{t-1} = \Psi_{\theta}(z_t, t, c)$$

其中 $z_t$ 为当前去噪步骤的潜在表示，$t$ 为扩散时间步，$c$ 为条件信息（历史帧与自车动作），$\Psi_{\theta}$ 为去噪网络。

DriveLaW 的关键操作是在去噪轨迹的**中间步骤**提取特征，而非使用完全去噪后的干净潜在。具体而言，从去噪过程的早期步骤 $t \in \mathcal{T}$ 提取特征：

$$h_t = \phi_{\theta}(z_t), \quad t \in \mathcal{T}$$

其中 $\phi_{\theta}$ 为 Video DiT 内部的特征提取函数，$h_t$ 即为承载场景语义与动态先验的感知潜在表示。实验表明，在去噪过程的早期步骤（$t=1$）提取特征可获得最强规划性能（PDMS 89.1），而越接近完全去噪（$t=10$）性能急剧下降至 23.2，证明噪声中保留的语义信息对规划至关重要。

### 3.3 噪声重注入机制

为平衡视频生成中的压缩效率与视觉保真度，DriveLaW-Video 引入了**噪声重注入机制**（Noise Reinjection）。该机制针对去噪后潜在中高频细节丢失的问题，通过自适应掩码与受控噪声注入，促使模型在关键区域重新生成纹理和结构。

首先，通过拉普拉斯算子计算响应图，并基于自适应阈值 $\tau = \beta \cdot \mathrm{std}(H_f)$ 生成高频区域二值掩码：

$$M_f(x, y) = \begin{cases} 1, & H_f(x, y) > \tau \\ 0, & \text{otherwise} \end{cases}$$

随后，在掩码区域注入受控噪声以扰动潜在表示：

$$L_t' = L_t + \sigma_t' \cdot M \odot \varepsilon_t, \quad \varepsilon_t \sim \mathcal{N}(0, \mathbf{I})$$

其中 $L_t$ 为当前潜在，$\sigma_t'$ 为噪声强度，$M$ 为高频掩码，$\varepsilon_t$ 为标准高斯噪声。这一操作迫使模型在后续去噪步骤中重新生成高频细节，从而恢复动态物体（车辆、行人）的清晰边缘和道路标线的纹理，同时保持天空等平滑区域的自然过渡。

### 3.4 流匹配扩散规划器

DriveLaW-Act 采用流匹配（Flow Matching）范式进行轨迹规划。给定视频生成器缓存的中间特征 $\{f_i\}_{i=1}^{B}$，规划器将带噪动作 $a_t$ 与驾驶上下文（自车状态 $s_t$、高层指令 $g_t$）分别编码：

$$h_{\mathrm{act}} = E_{\mathrm{act}}(a_t), \quad h_{\mathrm{ctx}} = E_{\mathrm{ctx}}([s_t; g_t])$$

随后，Action DiT 以上下文嵌入和缓存的视频特征为条件执行去噪：

$$f_{\theta}(a_t, t) = \mathrm{DiT}_{\mathrm{act}}\big([h_{\mathrm{act}}; t] \big| h_{\mathrm{ctx}}, \{f_i\}_{i=1}^{B}\big)$$

训练目标为流匹配损失，使预测输出与目标流对齐：

$$\mathcal{L}_{\mathrm{FM}} = \mathbb{E}_{t, a_0, \epsilon}\Big[\big\|f_{\theta}(a_t, t) - (a_0 - \epsilon)\big\|_2^2\Big]$$

其中 $a_0$ 为真实轨迹，$\epsilon$ 为噪声项。该目标引导规划器学习从噪声到轨迹分布的确定性映射，在推理时通过多步去噪生成平滑、物理可行的未来轨迹。

### 3.5 三阶段渐进式课程训练

为稳定训练链式架构并同时获得高质量视频生成与可靠规划能力，DriveLaW 采用三阶段渐进式课程训练策略：

1. **阶段一（低分辨率长序列）**：在低分辨率下训练长时段视频生成，使模型优先学习时序运动规律和粗粒度场景动态，避免高分辨率细节对运动建模的干扰。
2. **阶段二（高分辨率短序列）**：提升分辨率并缩短序列长度，细化空间细节和纹理质量，同时引入噪声重注入机制以恢复高频信息。
3. **阶段三（链式微调）**：冻结 Video DiT 主体权重，将中间去噪特征注入 Action DiT，联合微调规划器，使轨迹预测与视频生成表征对齐。

消融实验证实，该三阶段策略同时取得最低 FID（4.6）和 FVD（81.3），优于任何单阶段或双阶段变体，验证了渐进式课程对链式架构训练的必要性。

### 补充图表

![[assets/figures/papers/paper_list_l2467_https_openaccess_thecvf_com_content_CVPR2026_html_Xia_DriveLaW_Unifying/figures/002_Figure_2.jpg]]
*Figure 2: Restoring Structural and Temporal Consistency via Noise Reinjection. This comparison highlights the impact of our method. The baseline generation shows significant degradation, including (a) blurring, (b) structural inconsistency, and (c) artifacts. By integrating noise reinjection, our model preserves sharp details, maintains object structures, and produces clean, artifact-free frames, demonstrating a crucial improvement in video quality*



## 实验与关键发现

### 实验设置

DriveLaW 基于一个 **2B 参数**的视频扩散 Transformer（Video DiT）和一个 **133M 参数**的扩散规划器（Action DiT）构建。视频 DiT 使用 **LTX-Video** 的预训练权重初始化，规划器则从头训练。训练采用**三阶段渐进式课程**：阶段一在低分辨率（如 256×256）长序列（如 25 帧）上学习长时段运动模式；阶段二切换至高分辨率（如 512×512）短序列以细化空间细节与纹理；阶段三冻结视频生成器，将其中间潜在特征链式注入规划器进行轨迹微调。所有规划结果均在**无后续强化学习（RL）训练和无后处理打分器（scorers）**的条件下获得，确保与使用同类数据的方法公平比较。

### 视频生成主结果

在 nuScenes 验证集单视图视频生成任务上，DriveLaW 取得了 **FID 4.6** 和 **FVD 81.3** 的当前最优结果（Table 1）。相比此前最好的单视图方法 **Vista**（Gao et al., NeurIPS 2024）的 FID 6.9，DriveLaW 将 FID 降低了 **33.3%**；相比统一世界模型 **Epona**（Zhang et al., ICCV 2025）的 FVD 82.8，FVD 进一步降低了 **1.8%**。这一提升主要归因于噪声重注入机制对高频细节的有效恢复——基线生成常出现模糊、结构不一致和伪影，而 DriveLaW 能保持锐利细节、稳定的物体结构和干净的帧输出（Figure 2）。

![[assets/figures/papers/paper_list_l2467_https_openaccess_thecvf_com_content_CVPR2026_html_Xia_DriveLaW_Unifying/figures/003_Table_1.jpg]]
*Table 1: Quantitative evaluation of video generation on the NuScenes validation set. Our method outperforms prior single-view state-of-the-art methods in generation quality*

### 闭环规划主结果

在 NAVSIM Navtest 闭环规划基准上，DriveLaW 以 **PDMS 89.1** 刷新纪录（Table 2）。相比预测-规划统一模型 **PWM**（Zhao et al., NeurIPS 2025）的 88.1，提升 **+1.0**；相比统一世界模型 **Epona** 的 86.2，提升 **+2.9**。值得注意的是，DriveLaW 是首个利用视频生成器中间潜在特征作为规划表征的方法，其性能超越了所有显式使用世界模型的方法，也优于传统端到端方法（如 **DiffusionDrive**，Liao et al., CVPR 2025）。

![[assets/figures/papers/paper_list_l2467_https_openaccess_thecvf_com_content_CVPR2026_html_Xia_DriveLaW_Unifying/figures/004_Table_2.jpg]]
*Table 2: Performance comparison on NAVSIM Navtest using closed-loop metrics. Methods are grouped by whether they employ an explicit world model: Traditional End-to-End Methods and World Model Methods. † denotes methods trained with the same flow-matching objective*

### 开放环路规划结果

在 nuScenes 验证集开放环路规划上（Table 3），DriveLaW 的平均 L2 位移误差为 **1.15 m**，优于 Epona 的 1.25 m（-0.10 m）；平均碰撞率为 **0.24%**，低于 Epona 的 0.36%（-0.12%）。这表明链式耦合架构不仅在闭环场景中稳定，在开放环路评估中同样具备一致的轨迹预测精度和安全性。

![[assets/figures/papers/paper_list_l2467_https_openaccess_thecvf_com_content_CVPR2026_html_Xia_DriveLaW_Unifying/figures/005_Table_3.jpg]]
*Table 3: Planning performance on NuScenes. We report L2 displacement error and collision rate at 1s, 2s, 3s, and averaged*

### 关键消融实验

**视频预训练数据规模（Table 4）**：将视频预训练样本从 0 逐步扩展至 760 万，PDMS 从 85.9 单调提升至 89.1。这一趋势强有力地证明：**大规模视频生成学习内化的驾驶先验（场景语义、智能体动态、物理一致性）可直接迁移至规划任务**，且尚未出现饱和迹象。

**规划器条件表征（Table 5）**：以视频潜在特征作为扩散条件（PDMS 89.1）显著优于 **BEV 特征**（84.1，-5.0）和 **VLM 隐藏状态**（86.5，-2.6）。这验证了链式生成表征的不可替代性——视频扩散模型的中间去噪潜在空间蕴含的信息密度和任务相关性远超手工设计的感知特征。

**视频去噪步骤选择（Table 6）**：在去噪过程的**早期步骤（t=1）**提取视频潜在特征可获得最强规划性能（PDMS 89.1）；随着去噪步数增加至 t=10，性能急剧下降至 23.2。这一现象揭示了一个关键洞察：**噪声中承载的语义信息对规划至关重要**，完全去噪后的干净潜在反而丢失了丰富的场景动态表征。

**训练策略（Table 7）**：三阶段渐进式训练同时取得最低 FID（4.6）和 FVD（81.3），优于仅单阶段或双阶段训练的变体。先学习长时段运动、再细化空间细节、最后链式微调的课程设计，有效平衡了视频生成质量与规划表征的稳定性。

### 失败模式与局限性

当前 DriveLaW 仅评估了**单视图**视频生成和基于既定轨迹的规划，尚未测试多相机输入或交互式闭环驾驶场景。噪声重注入的阈值选择依赖自适应标准差倍数（$\beta \cdot \text{std}(H_f)$），其最优超参数可能随场景分布漂移而需要重新调优。此外，链式架构中视频生成器的推理延迟是实时部署的瓶颈，轻量化与蒸馏路径有待探索。

### 定性分析

Figure 3 展示了 DriveLaW 与 Epona 在 nuScenes 验证集上的定性对比。DriveLaW 生成的视频在三个方面显著优于 Epona：(1) 车辆细节更清晰，结构完整性更稳定；(2) 行人形状保持完好，易于辨识；(3) 对不显眼物体（如黄色厢式货车）的识别与维持正确，展现了更强的语义理解能力。这些优势源于噪声重注入对高频细节的恢复以及大规模预训练对场景语义的内化。

![[assets/figures/papers/paper_list_l2467_https_openaccess_thecvf_com_content_CVPR2026_html_Xia_DriveLaW_Unifying/figures/007_Figure_3.jpg]]
*Figure 3: Qualitative Comparison with state-of-the-art driving world model. We compare DriveLaW with Epona [81] on nuScenes validation set. DriveLaW generates videos with (1) clearer vehicle details and more stable structural integrity, (2) well-preserved pedestrian shapes that remain easily identifiable, and (3) correct recognition and maintenance of inconspicuous objects (e.g., the yellow van), demonstrating superior visual quality, subject preservation, and semantic understanding*

### 补充图表

![[assets/figures/papers/paper_list_l2467_https_openaccess_thecvf_com_content_CVPR2026_html_Xia_DriveLaW_Unifying/figures/006_Table_4.jpg]]
*Table 4: Scaling video pretraining improves planning on NAVSIM Navtest. Rows vary the number of video pretraining samples used before fine-tuning the diffusion planner on NAVSIM*

![[assets/figures/papers/paper_list_l2467_https_openaccess_thecvf_com_content_CVPR2026_html_Xia_DriveLaW_Unifying/figures/008_Table_7.jpg]]
*Table 7: Comparison of different training strategies with FID and FVD scores*

![[assets/figures/papers/paper_list_l2467_https_openaccess_thecvf_com_content_CVPR2026_html_Xia_DriveLaW_Unifying/figures/009_Table_5.jpg]]
*Table 5: Representation ablation on NAVSIM Navtest. We compare BEV features, VLM hidden states, and video latents as diffusion condition*

![[assets/figures/papers/paper_list_l2467_https_openaccess_thecvf_com_content_CVPR2026_html_Xia_DriveLaW_Unifying/figures/010_Table_6.jpg]]
*Table 6: Which video denoising step feeds the Action DiT. We evaluate planning when conditioning on video latents taken from different diffusion denoising steps*



## 定位与知识库关联

### 核心创新与差异化定位

DriveLaW 的根本创新在于**链式耦合生成与规划**：将视频生成扩散模型的中间去噪潜在特征直接注入规划扩散模型，作为规划条件。这与现有世界模型范式形成鲜明对比。

**与并行/分离式世界模型的区别**：现有方法如 **Epona** (Zhang et al., ICCV 2025) 和 **PWM** (Zhao et al., NeurIPS 2025) 虽也同时具备视频生成与运动规划能力，但二者在架构上是并行或分离训练的——规划模块依赖显式的 BEV 特征或 VLM 隐藏状态，而非生成模型内化的表征。这种解耦导致规划未能直接利用视频生成器从大规模数据中学得的物理规律和场景语义，存在表征断裂。DriveLaW 的链式设计使规划器直接读取生成器的“世界理解”，实现了从生成到规划的端到端表征一致性。

**与端到端规划方法的区别**：**DiffusionDrive** (Liao et al., CVPR 2025) 等端到端方法直接输出轨迹，缺乏显式的世界模型。DriveLaW 保留了世界模型对未来场景的显式预测能力，同时将这种预测能力转化为规划器的强先验。

**与 VLM 监督方法的区别**：**DriveVLA-W0** (Li et al., arXiv 2025) 利用视觉语言模型提供世界模型监督，而 DriveLaW 证明了视频生成扩散模型自身的中间潜在特征（PDMS 89.1）优于 VLM 隐藏状态（86.5）和 BEV 特征（84.1）（Table 5），无需额外的多模态对齐工程。

### 方法谱系中的技术锚点

DriveLaW 的方法设计融合了多个技术脉络的关键思想：

1. **视频扩散生成**：继承自 **LTX-Video** 的预训练权重（2B Video DiT 初始化），沿袭了基于 DiT 的视频生成框架。与 **Vista** (Gao et al., NeurIPS 2024) 等驾驶视频生成方法相比，DriveLaW 引入了噪声重注入机制（Noise Reinjection），在去噪早期阶段通过自适应高频掩码选择性注入噪声，以恢复激进压缩带来的细节损失，在 nuScenes 上取得 FID 4.6（Vista 为 6.9）。

2. **扩散规划**：采用流匹配（Flow Matching）目标训练 Action DiT，与 **PWM** 等方法的规划范式同属扩散规划家族（Table 2 中 † 标注了使用相同流匹配目标的方法）。DriveLaW 的差异化在于规划扩散模型的条件信号来源——视频生成中间潜在特征，而非自车状态编码或 BEV 特征。

3. **世界模型表征学习**：受 Genie envisioner 的链式生成-规划理念启发，但 DriveLaW 首次将视频生成器的中间去噪特征作为规划表征。消融实验（Table 6）揭示了关键发现：在去噪过程早期步骤（t=1）提取的潜在特征可提供最强规划性能（PDMS 89.1），而接近完全去噪（t=10）时性能急剧下降至 23.2，表明噪声中蕴含的语义信息对规划至关重要——这是此前方法未系统探索的表征特性。

### 训练范式的演进

DriveLaW 的三阶段渐进式课程训练策略解决了链式架构的训练稳定性问题：

- **阶段一**：低分辨率长序列视频预训练，学习长时段运动先验
- **阶段二**：高分辨率短序列微调，细化空间细节
- **阶段三**：联合视频生成与规划微调，建立链式表征连接

消融实验（Table 7）表明，完整三阶段训练同时取得最优 FID（4.6）和 FVD（81.3），验证了渐进式课程对链式架构训练的必要性。

### 适用边界与局限

1. **单视图限制**：当前仅评估了单视图视频生成和基于既定轨迹的规划，未测试多相机输入或交互式闭环驾驶场景。多视图一致生成与规划是明确的扩展方向，但链式架构在多视图条件下的表征融合与计算开销尚未验证。

2. **实时性未验证**：2B Video DiT 的推理延迟在实际部署中的可行性未在论文中讨论。链式架构的实时性优化路径（如模型蒸馏、潜在空间缓存、去噪步数缩减）是开放问题。

3. **噪声重注入的超参数敏感性**：自适应阈值 $au$ 依赖拉普拉斯响应图的标准差缩放（$\beta \cdot \text{std}(H_f)$），该超参数的选择策略和跨场景泛化性未充分讨论。

4. **预训练数据依赖**：视频预训练数据量从 0 扩展到 7.6M 样本时，PDMS 从 85.9 提升至 89.1（Table 4），表明方法对大规模预训练数据有较强依赖。数据规模与模型规模的 scaling law 关系尚未建立。

### 开放问题

- **多视图扩展**：如何将链式表征从单视图推广到多视图一致生成与规划？
- **实时部署**：链式架构的推理延迟优化路径（模型压缩、缓存策略、早期退出）？
- **闭环交互**：在交互式闭环驾驶中，视频生成与规划的动态耦合机制如何设计？
- **表征可解释性**：中间去噪潜在特征中具体编码了哪些驾驶先验（语义、几何、物理）？



## 原文 PDF

![[paperPDFs/CVPR_2026/DriveLaW_Unifying_Planning_and_Video_Generation_in_a_Latent_Driving_World.pdf]]
