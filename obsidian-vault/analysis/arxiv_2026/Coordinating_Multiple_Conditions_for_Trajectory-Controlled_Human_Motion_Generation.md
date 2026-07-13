---
title: Coordinating Multiple Conditions for Trajectory-Controlled Human Motion Generation
type: paper
paper_level: A
venue: arXiv
year: 2026
pdf_ref: paperPDFs/arxiv_2026/Coordinating_Multiple_Conditions_for_Trajectory-Controlled_Human_Motion_Generation.pdf
project_link: "https://cdlchoi.github.io/cmc_page/"
code_link: null
aliases:
- CCMC
- CMCTCHMG
tags:
- arxiv_2026
- topic/motion_animation
- topic/motion_animation/human_motion_generation
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 将条件解耦为两个独立阶段：第一阶段用简化表示进行轨迹控制，第二阶段在纯文本条件下完成全身运动修复；引入选择性修复机制(SIM)以交替任务训练防止过拟合。
primary_logic: 采用分而治之策略解耦多模态条件，避免文本语义与精细轨迹之间的冲突；利用简化表示稳定轨迹引导，并依赖仅文本的扩散修复模型生成高质量运动。
claims:
- 同时应用文本和轨迹条件会在去噪过程中产生冲突，导致运动质量下降，如图3所示。
- 简化表示相比冗余表示在整个去噪过程中显著降低控制误差且更稳定（图4和图11）。
- CMC在HumanML3D骨盆控制任务上达到FID=0.097，平均误差0.51cm，远超先前最佳方法（表I）。
- 消融实验证实解耦框架和SIM均带来显著的性能增益（表III和表IV）。
---

# Coordinating Multiple Conditions for Trajectory-Controlled Human Motion Generation

> [!tip] 核心洞察
> 采用分而治之策略解耦多模态条件，避免文本语义与精细轨迹之间的冲突；利用简化表示稳定轨迹引导，并依赖仅文本的扩散修复模型生成高质量运动。

| 字段      | 内容                                                                                                                                         |
| ------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| 中文题名    | 面向轨迹控制人体运动生成的多条件协调框架                                                                                                                       |
| 英文题名    | Coordinating Multiple Conditions for Trajectory-Controlled Human Motion Generation                                                         |
| 会议/期刊   | arXiv 2026                                                                                                                                 |
| Links   | [paper](https://arxiv.org/abs/2605.13729) · [Project](https://cdlchoi.github.io/cmc_page/)                                                 |
| Topic | #topic/motion_animation #topic/motion_animation/human_motion_generation #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method  | CMC (Coordinating Multiple Conditions)                                                                                                     |
| Dataset | HumanML3D, KIT-ML                                                                                                                          |

> [!tip] 效果简介
> - HumanML3D (Pelvis control on all frames) 上，FID↓ 0.097 vs 0.218 (Omnicontrol) (-0.121)；R-precision Top-3↑ 0.784 vs 0.687 (Omnicontrol) / 0.779 (TLControl) (+0.097 / +0.005)；Avg. err. (cm)↓ 0.51 vs 3.38 (Omnicontrol) / 1.08 (TLControl) (-2.87 / -0.57)。
> - KIT-ML (Pelvis control on all frames) 上，FID↓ 0.259 vs 0.310 (Omnicontrol) (-0.051)；Avg. err. (cm)↓ 0.41 vs 2.20 (Omnicontrol) (-1.79)。

## 概要

轨迹控制的人体运动生成面临一个关键瓶颈：**文本语义条件与精细轨迹条件在单一阶段中同时施加时会产生相互干扰**，破坏扩散模型的去噪过程，导致运动语义不一致、控制精度下降。现有主流框架——无论是 **GMD** (Karunratanakul et al., ICCV 2023) 的双阶段交替条件注入，还是 **Omnicontrol** (Xie et al., ICLR 2024) 的单阶段集成控制——均未有效解决这一冲突。

本文提出 **CMC (Coordinating Multiple Conditions)**，采用**分而治之的解耦策略**协调多模态条件。核心思路是将问题拆分为两个级联阶段：第一阶段在简化运动表示空间中进行纯轨迹控制，第二阶段在仅文本条件下完成全身运动修复。这一设计从根本上避免了文本语义与精细轨迹之间的冲突，同时引入**选择性修复机制 (SIM)** 以交替任务训练防止过拟合，提升泛化能力。

实验结果表明，CMC 在 HumanML3D 骨盆全帧控制任务上达到 **FID=0.097**、平均控制误差仅 **0.51 cm**，远超先前最佳方法（Omnicontrol 的 FID=0.218、误差 3.38 cm），同时在文本-运动语义一致性（R-precision Top-3=0.784）上也保持领先。消融实验进一步证实，解耦框架与 SIM 各自带来显著的性能增益，简化运动表示相比冗余表示在整个去噪过程中显著降低控制误差且更稳定。



### 问题域：轨迹控制下的人体运动生成

人体运动生成旨在根据给定条件合成自然且多样化的人体动作序列。当条件扩展为文本描述与空间轨迹的联合约束时，任务演变为**轨迹控制的人体运动生成**——要求生成的运动既要精确遵循指定的关节空间路径，又要忠实体现文本所描述的语义（如“一个人绕圈行走”）。这一能力对动画制作、虚拟现实和具身智能体控制等应用至关重要。

### 现有方法的瓶颈：多条件冲突与表示冗余

当前主流方法在处理文本和轨迹双重条件时，普遍采用**单阶段联合条件注入**策略。例如，**GMD**（Karunratanakul et al., ICCV 2023）在运动生成阶段同时施加文本和轨迹条件；**Omnicontrol**（Xie et al., ICLR 2024）则在单一集成阶段中同时利用两类条件。这种设计存在两个核心瓶颈：

**瓶颈一：条件冲突导致语义不一致。** 当文本条件和轨迹条件在同一去噪过程中同时作用时，二者会产生相互干扰。如 Fig. 3 所示，存在条件冲突时，网络对文本条件的理解不充分，生成的运动语义质量下降；而在无冲突情况下，网络能够充分映射文本语义并精确跟随轨迹。根本原因在于，文本语义的抽象约束与轨迹的精细空间约束在梯度空间中可能指向不一致的方向，破坏了去噪过程的稳定性。

**瓶颈二：冗余运动表示导致控制不稳定。** 现有方法（如 Omnicontrol）通常采用冗余表示 $(\mathbf{r}^{a}, \mathbf{r}^{x}, \mathbf{r}^{z}, \mathbf{r}^{y}, \mathbf{j}^{p}, \mathbf{j}^{r}, \mathbf{j}^{v}, \mathbf{c}^{f})$，包含根角速度、根线速度、根高度、关节位置、旋转、速度及足部接触标签。在轨迹引导下，这些分量之间存在内在约束关系（如位置与速度的微分关系），但扩散模型在每个去噪步独立预测各分量时，难以保证分量间的一致性。如 Fig. 4 和 Fig. 11 所示，冗余表示在整个去噪过程中控制误差波动剧烈，且误差均值显著高于简化表示。

### 核心动机：分而治之的解耦策略

针对上述瓶颈，本文提出**CMC（Coordinating Multiple Conditions）**框架，核心理念是**将多模态条件解耦为两个独立阶段**，避免文本语义与精细轨迹之间的直接冲突：

- **第一阶段（Trajectory Control）：** 仅使用简化表示（仅保留 $\mathbf{j}^{p}$ 关节局部位置和根运动参数，丢弃旋转、速度等冗余分量）进行轨迹控制，稳定地生成骨盆和受控关节的轨迹。
- **第二阶段（Motion Completion）：** 在纯文本条件下，以前一阶段输出为部分观测，通过扩散修复模型完成全身运动生成，确保语义质量不受轨迹约束干扰。

这种“控制-然后-生成”的范式从根本上规避了单阶段方法中条件冲突的问题，同时通过简化表示降低了轨迹控制阶段的不稳定性。此外，为防止第二阶段修复模型对固定观测模式过拟合，CMC 引入**选择性修复机制（SIM）**，在训练时以 50% 概率交替执行标准文本到运动生成与运动修复任务，提升模型对分布外观测的泛化能力。



## 核心方法与创新机理

CMC 的核心创新在于将多条件人体运动生成中的**文本语义与精细轨迹控制解耦为两个独立阶段**，以此规避单阶段框架中两类条件在去噪过程中的相互干扰。具体而言，CMC 通过三个关键设计实现这一目标：

### 1. 解耦式两阶段框架

现有主流方法在单一阶段中同时施加文本和轨迹条件：**GMD**（Karunratanakul et al., ICCV 2023）在两个阶段均使用双条件，**Omnicontrol**（Xie et al., ICLR 2024）则在单一集成阶段中同时利用文本与轨迹条件。然而，这种设计导致条件冲突——如图 3 所示，同时施加文本和轨迹条件会破坏去噪过程，使网络对文本条件的理解不充分，最终生成语义不一致的运动。

CMC 采用“分而治之”策略，将流程解耦为两个级联阶段：
- **轨迹控制阶段（Trajectory Control Stage）**：仅基于文本描述和受控关节的空间轨迹，在简化表示空间中预测骨盆及受控关节的局部位置，并通过轨迹引导优化。
- **运动补全阶段（Motion Completion Stage）**：仅使用文本条件，以前一阶段输出作为部分观测，通过扩散修复模型生成全身运动。

这一设计使文本条件与轨迹条件在各自独立的阶段中发挥作用，从根本上避免了条件冲突。

### 2. 简化运动表示

在轨迹控制阶段，现有方法通常采用**冗余表示**（包含根角速度 $r^{a}$、根线速度 $r^{x}, r^{z}$、根高度 $r^{y}$、关节位置 $\mathbf{j}^{p}$、旋转 $\mathbf{j}^{r}$、速度 $\mathbf{j}^{v}$ 及足部接触标签 $\mathbf{c}^{f}$）。然而，在轨迹引导下，冗余表示中位置、旋转、速度等分量之间存在不一致性，导致控制误差在整个去噪过程中波动剧烈且呈上升趋势（图 4、图 11）。

CMC 提出使用**简化表示**，仅保留关节局部位置 $\mathbf{j}^{p}$ 和根运动参数 $(r^{a}, r^{x}, r^{z}, r^{y})$，丢弃旋转、速度及接触标签。该设计的核心洞察在于：轨迹控制本质上仅需约束关节的空间位置，冗余的旋转和速度信息不仅无益，反而在梯度引导中引入噪声。实验表明，简化表示在整个去噪过程中的控制误差显著低于冗余表示，且标准差更小、过程更稳定（图 11、图 12）。

### 3. 选择性修复机制（SIM）

在运动补全阶段，若仅训练修复任务，扩散模型易对固定的掩码模式过拟合，导致对分布外部分观测的泛化能力下降。CMC 提出**选择性修复机制（Selective Inpainting Mechanism, SIM）**：训练时以 50% 概率交替进行标准文本到运动生成任务和运动修复任务（图 6）。这一设计使非修复训练充当正则化手段，在保持修复精度的同时显著提升了模型的泛化能力（图 10）。

消融实验（TABLE III、TABLE IV）证实，解耦框架和 SIM 均带来显著的性能增益：解耦框架相较单阶段框架在 FID 和 R-precision 上均有大幅提升，控制误差降低数倍；引入 SIM 后，文本到运动生成任务的 FID 和 R-precision 明显改善，且修复模型对分布外观测的泛化能力增强。

### 创新总结

| 创新维度 | 现有方案 | CMC 方案 | 关键证据 |
|---------|---------|---------|---------|
| 条件协调方式 | 单阶段同时施加文本与轨迹条件 | 解耦为轨迹控制与运动补全两阶段 | Fig. 1, Fig. 3, TABLE III |
| 轨迹控制表示 | 冗余表示（含旋转、速度等） | 简化表示（仅关节位置与根运动） | Fig. 4, Fig. 11, Fig. 12 |
| 补全训练策略 | 仅训练修复任务 | SIM 以 50% 概率交替修复与生成任务 | Fig. 6, Fig. 10, TABLE IV |

三者协同作用，使 CMC 在 HumanML3D 骨盆控制任务上达到 FID=0.097、平均误差仅 0.51 cm，远超先前最佳方法（TABLE I）。



CMC 采用**分而治之**策略，将文本条件与轨迹条件的协调解耦为两个级联阶段，从根本上避免了单阶段框架中两类条件在去噪过程中相互干扰的问题（Fig. 1）。整体流水线如 Fig. 5 所示，两个阶段共享一个 CLIP 文本编码器（ViT-B/32），均以扩散模型为基础，骨干网络为 8 层 Transformer 编码器（特征维度 512）。

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2605_13729/figures/001_Figure_1.jpg]]
*Figure 1: Comparison of frameworks between our approach and two mainstream frameworks. (a) GMD [22] applies both text and trajectory conditions at both stages, particularly during the motion generation stage. (b) Omnicontrol [51] generates motion in a single integrated stage, utilizing both text and trajectory conditions simultaneously. (c) In contrast, our CMC decouples the trajectory control and motion generation stages, thereby avoiding conflicts between the text and trajectory conditions*

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2605_13729/figures/005_Figure_5.jpg]]
*Figure 5: Overview of our CMC. It consists of two stages: Trajectory Control and Motion Completion. In the Trajectory Control stage, we utilize textual descriptions and spatial trajectories of the controlled joints to predict the trajectories of both the pelvis and the controlled joints within a simplified representation space. Subsequently, the Motion Completion stage takes these trajectories as partial observations and completes the full-body motion using a TMM 改 ，加入CLIPdiffusion inpainting model. Both stages use CLIP as the text encoder*

### 第一阶段：轨迹控制

该阶段仅使用**简化运动表示**，即仅保留关节局部位置 $\mathbf{j}^{p}$ 与根运动参数 $(r^{a}, r^{x}, r^{z}, r^{y})$，丢弃了冗余表示中的关节旋转、速度及足部接触标签等分量。给定文本描述与受控关节的空间轨迹，扩散模型首先生成骨盆及受控关节的合理局部位置，随后在每个去噪步施加轨迹引导：

$$\mu_t = \mu_t - \tau \nabla_{\mu_t} G(R(\mu_t), C)$$

其中 $R(\cdot)$ 将运动转换到世界坐标系，$C$ 为给定的空间轨迹条件，$\tau$ 为引导强度。这一阶段的核心产出是骨盆与受控关节的简化局部位置序列。

### 第二阶段：运动补全

第二阶段**仅使用文本条件**，将第一阶段的输出作为部分观测，通过扩散修复模型生成全身运动。该阶段采用冗余运动表示 $(r^{a}, r^{x}, r^{z}, r^{y}, \mathbf{j}^{p}, \mathbf{j}^{r}, \mathbf{j}^{v}, \mathbf{c}^{f})$，以完整描述全身运动学信息。

### 选择性修复机制

为防止修复模型在训练中过拟合于特定部分观测模式，CMC 引入**选择性修复机制**：以 50% 概率在标准文本到运动生成任务与运动修复任务之间随机切换（Fig. 6, Fig. 7）。这一多任务训练策略相当于正则化，显著增强了模型对分布外部分观测的泛化能力。

### 训练损失

第一阶段训练时同时优化两个目标：

$$\mathcal{L}_{elem} = \frac{1}{N_{elem}} \sum_{i=1}^{N_{elem}} \| \mathbf{x}_0 - \hat{\mathbf{x}}_0 \|_2^2$$

$$\mathcal{L}_{global} = \frac{1}{N_{cont}} \sum_{i=1}^{N_{cont}} \| R(\hat{\mathbf{x}}_0) - C \|_2^2$$

总损失为 $\mathcal{L} = \mathcal{L}_{elem} + \mathcal{L}_{global}$，分别约束局部元素精度与全局轨迹跟随精度。



### 扩散模型基础

CMC的两个阶段均建立在扩散模型之上。给定原始运动序列 $\mathbf{x}_0$，前向过程通过一步采样直接得到第 $t$ 步的噪声数据：

$$\mathbf{x}_t = \sqrt{1 - \beta_t} \mathbf{x}_0 + \sqrt{\beta_t} \epsilon = \alpha_t \mathbf{x}_0 + \sigma_t \epsilon$$

其中 $\alpha_t$ 和 $\sigma_t$ 为噪声调度系数，$\epsilon$ 为标准高斯噪声。该公式支撑后续去噪网络以 $\mathbf{x}_t$ 为输入预测清洁运动 $\hat{\mathbf{x}}_0$。

### 第一阶段：轨迹控制

**运动表示选择**是该阶段的核心设计。常规的冗余运动表示定义为：

$$(r^{a}, r^{x}, r^{z}, r^{y}, \mathbf{j}^{p}, \mathbf{j}^{r}, \mathbf{j}^{v}, \mathbf{c}^{f})$$

包含根角速度、根线速度、根高度、关节位置、旋转、速度及足部接触标签。CMC在第一阶段改用简化表示：

$$(r^{a}, r^{x}, r^{z}, r^{y}, \mathbf{j}^{p})$$

仅保留根运动参数和关节局部位置，丢弃旋转、速度等冗余分量。这一选择的因果机制在于：冗余表示中各分量（位置、旋转、速度）在轨迹引导下相互不一致，导致去噪过程中控制误差波动剧烈且随步数增加而发散（Fig. 4, Fig. 11）。简化表示消除了分量间的冲突，使引导梯度更稳定地作用于位置空间。

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2605_13729/figures/003_Figure_4.jpg]]
*Figure 4: Comparisons of the control error for the redundant and simplified representations across all denoising steps*

**轨迹引导更新**遵循标准范式，在每个去噪步中通过最小化合成的运动与给定轨迹条件 $C$ 之间的目标函数来优化后验均值 $\mu_t$：

$$\mu_t = \mu_t - \tau \nabla_{\mu_t} G(R(\mu_t), C)$$

其中 $R(\cdot)$ 将运动表示转换到世界坐标系，$G$ 为位置误差函数，$\tau$ 为引导强度。训练时同时优化两个损失：

$$\mathcal{L}_{elem} = \frac{1}{N_{elem}} \sum_{i=1}^{N_{elem}} \| \mathbf{x}_0 - \hat{\mathbf{x}}_0 \|_2^2$$

$$\mathcal{L}_{global} = \frac{1}{N_{cont}} \sum_{i=1}^{N_{cont}} \| R(\hat{\mathbf{x}}_0) - C \|_2^2$$

$$\mathcal{L} = \mathcal{L}_{elem} + \mathcal{L}_{global}$$

$\mathcal{L}_{elem}$ 约束预测运动与真实运动在每个元素上的均方误差，$\mathcal{L}_{global}$ 约束转换后的全局位置与给定轨迹之间的L2距离。两损失联合优化使模型在保持运动自然度的同时精确跟随空间约束。

### 第二阶段：运动补全

第二阶段以第一阶段的简化表示输出（骨盆及受控关节的局部位置）为部分观测，仅使用文本条件通过扩散修复生成全身运动。该阶段使用冗余表示作为完整运动空间，扩散模型以部分观测为条件补全缺失的关节旋转、速度等信息。

### 选择性修复机制

为防止第二阶段修复模型过拟合到固定的部分观测模式，CMC引入选择性修复机制。训练时以50%概率随机切换两种数据准备方式：标准文本到运动生成（非修复数据）和运动修复（修复数据）。该机制作为正则化手段，迫使模型同时保持生成能力和修复能力，增强对分布外部分观测的泛化能力（Fig. 6, Fig. 7）。

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2605_13729/figures/006_Figure_6.jpg]]
*Figure 6: The workflow of SIM to train the diffusion inpainting model. SIM prepares non-inpainting data and inpainting data with a probability of 50% respectively*

### 共享文本编码器

两个阶段共享CLIP文本编码器（ViT-B/32），将文本描述编码为嵌入向量，确保语义信息在两个阶段间一致传递。骨干网络为8层Transformer编码器，特征维度512。

### 补充图表

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2605_13729/figures/004_Figure_3.jpg]]
*Figure 3: (a) With conflict: insufficient understanding of the text condition leads to suboptimal motion quality. (b) Without conflict: the network fully maps the text to motion while achieves accurate trajectory following*

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2605_13729/figures/016_Figure_12.jpg]]
*Figure 12: Statistical mean and standard deviation of the control error across denoising steps. Darker-colored and lighter-colored curves indicate the use of simplified and redundant representations, respectively*



## 实验与关键发现

### 主实验结果

CMC在两个主流基准上均以显著优势超越先前方法。在HumanML3D骨盆全帧控制设置下，CMC取得FID=0.097，较Omnicontrol（0.218）降低55.5%；平均控制误差仅0.51 cm，而Omnicontrol为3.38 cm，TLControl为1.08 cm（TABLE I）。同时，R-precision Top-3达到0.784，与TLControl的0.779相当，但运动质量与控制精度同步占优。在KIT-ML数据集上，CMC同样保持领先：FID=0.259（Omnicontrol为0.310），平均误差0.41 cm（Omnicontrol为2.20 cm），验证了跨数据集的稳健性（TABLE II）。

效率方面，配合DDIM采样后CMC平均延迟降至0.41 s，FPS达478，在保持高精度的同时优于多数基线（TABLE VII）。DDIM采样下控制误差和FID略有上升但仍具竞争力（TABLE VI），表明该方法在精度-效率权衡上具备灵活调节空间。

### 消融实验

消融实验系统验证了三个核心设计选择的因果贡献（TABLE III）。

**解耦框架 vs. 单阶段框架**：将两阶段解耦框架替换为单阶段联合条件框架后，FID从0.097升至0.218，平均误差从0.51 cm升至3.38 cm（TABLE III Row 1 vs Row 7）。这一对比直接量化了文本与轨迹条件在单阶段中相互干扰的代价——去噪过程被破坏，运动语义一致性显著下降。

**选择性修复机制（SIM）**：移除SIM后，文本到运动生成任务的FID从0.097恶化至0.218，R-precision从0.784降至0.687（TABLE IV）。同时，修复模型对分布外部分观测的泛化能力减弱（Fig. 10）。SIM以50%概率交替进行标准生成与修复训练，有效防止了修复任务上的过拟合，使第二阶段扩散模型在仅见受控关节局部位置时仍能生成高质量全身运动。

**传递关节数量的影响**：向第二阶段传递的关节越多，FID和R-precision越差（TABLE III Rows 5-7）。仅传递受控关节及骨盆时性能最优；传递全部关节时性能退化至接近单阶段框架水平。Fig. 9的定性对比直观展示了这一趋势：传递全部关节时，模型难以同时满足文本语义与轨迹约束，出现肢体不自然或语义偏离。

**简化表示 vs. 冗余表示**：Fig. 11和Fig. 12给出关键证据——冗余表示（含关节旋转、速度、足部接触标签）在整个去噪过程中控制误差波动剧烈，且后期呈发散趋势；简化表示（仅关节局部位置和根运动参数）则保持低误差且稳定。TABLE V进一步表明，简化表示在1帧控制和全帧控制下均显著优于冗余表示。Fig. 13揭示，文本条件对冗余表示的控制稳定性有辅助作用，但无法根本解决其内在的不一致性。

### 失败模式与局限性

尽管整体性能领先，CMC在以下场景存在已知局限：

1. **分布外轨迹泛化不足**：当给定极端轨迹（如骨盆高度3米）时，模型仍倾向生成地面行走运动，未能适应大幅偏离训练分布的绝对坐标条件。这源于绝对坐标表示缺乏对高度维度的归一化或相对编码。

2. **轨迹引导的梯度不均匀性**：当前轨迹引导在原始运动空间而非潜在空间中实施，导致序列数据上梯度累积不均匀，部分帧的轨迹跟随精度仍有波动。这一机制性限制在长序列或复杂轨迹上更为明显。

3. **控制误差未完全消除**：尽管平均误差已降至亚厘米级，但极端姿态或快速转向场景下仍存在可观测的位置偏差，表明简化表示与引导策略仍有优化空间。

### 重要图表结论汇总

- **Fig. 3**：定性展示了条件冲突的核心现象——同时施加文本和轨迹条件时，网络对文本语义理解不足，运动质量下降；解耦后文本条件得到充分映射，运动质量与轨迹精度兼得。
- **Fig. 4**：冗余表示与简化表示的控制误差动态对比，为简化表示的选择提供了直接动机。
- **TABLE III**：系统性消融证据，量化了解耦框架、SIM和关节传递策略各自的性能贡献。
- **TABLE IV**：SIM对文本到运动生成任务的独立增益，证明该训练策略不仅服务于修复阶段，还提升了基础生成能力。
- **Fig. 11 & Fig. 12**：简化表示的低误差与高稳定性优势，构成第一阶段设计选择的核心实证支撑。

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2605_13729/figures/015_Figure_11.jpg]]
*Figure 11: Average control error across denoising steps. Darker-colored and lighter-colored curves indicate the use of simplified and redundant representations, respectively*

### 补充图表

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2605_13729/figures/007_Table.jpg]]
*Table: QUANTITATIVE RESULTS ON THE HUMANML3D TESTING SET. ALL RESULTS ARE TESTED ON THE PREMISE OF CONTROLLING ALL FRAMES. THE BEST SCORES ARE HIGHLIGHTED IN BOLD. → MEANS CLOSER TO REAL DATA IS BETTER. TABLE I TABLE II QUANTITATIVE RESULTS ON THE KIT-ML TESTING SET. ALL DATA IS TESTED ON THE PREMISE OF CONTROLLING ALL FRAMES. THE BEST SCORES ARE HIGHLIGHTED IN BOLD. → MEANS CLOSER TO REAL DATA IS BETTER. BUN MEANS BODY UPPER NECK, DEFINED IN KIT-ML*

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2605_13729/figures/010_Table.jpg]]
*Table: III ABLATION RESULTS OF DIFFERENT COMBINATIONS OF PROPOSED COMPONENTS ON THE HUMANML3D TESTING SET. EACH RESULT IS THE AVERAGE OF THE PERFORMANCE METRICS FOR THE PELVIS AND FIVE END-EFFECTORS*

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2605_13729/figures/011_Table.jpg]]
*Table: IV QUANTITATIVE RESULTS UNDER THE TEXT-TO-MOTION GENERATION SETTING ON THE HUMANML3D TESTING SET. BOLD INDICATES THE BEST RESULT, WHILE UNDERSCORE REFERS TO THE SECOND-BEST. “→” DENOTES CLOSER TO THAT OF THE REAL DATA IS BETTER*

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2605_13729/figures/012_Figure.jpg]]
*Figure: (a) with SIM (b) without SIM*

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2605_13729/figures/009_Figure_9.jpg]]
*Figure 9: Two visual comparisons (a) and (b) to qualitatively prove the existence of the conflict between text and trajectory conditions. The difference between the three columns is the number of joints that passed to the second stage, including: only the controlled joints and the pelvis (left), the controlled joints and joints belonging to the torso (middle), and all joints (right)*



## 定位与知识库关联

### 条件协调方式的谱系定位

CMC 的核心贡献在于将文本与轨迹条件的协调方式从“单阶段混合”推进到“分阶段解耦”。此前的方法大体沿两条路径发展：

- **显式轨迹引导**：**GMD**（Karunratanakul et al., ICCV 2023）在运动生成阶段同时施加文本和轨迹条件，但条件间的冲突导致语义理解不充分。**Omnicontrol**（Xie et al., ICLR 2024）在单一集成阶段中同时使用两种条件，虽实现了任意关节任意时刻的控制，但控制精度受限于条件干扰。
- **后优化方法**：**TLControl**（Wan et al., ECCV 2024）采用后处理优化策略，在生成后调整运动以匹配轨迹，避免了生成阶段的内部冲突，但优化过程独立于生成过程，难以保证语义一致性。

CMC 的“分而治之”策略将上述两类方法的优势结合：第一阶段仅用简化表示进行轨迹控制，避免文本条件干扰；第二阶段仅用文本条件完成运动修复，避免轨迹条件干扰语义生成。这一解耦设计从根本上改变了条件协调的因果机制——不是在去噪过程中让两种条件互相博弈，而是让它们在不同阶段各自发挥主导作用。

### 运动表示设计的定位

运动表示的选择直接决定了轨迹引导的稳定性。CMC 在此做出了关键区分：

- **冗余表示** $(\mathbf{r}^{a}, \mathbf{r}^{x}, \mathbf{r}^{z}, \mathbf{r}^{y}, \mathbf{j}^{p}, \mathbf{j}^{r}, \mathbf{j}^{v}, \mathbf{c}^{f})$：包含根角速度、根线速度、根高度、关节位置、旋转、速度及足部接触标签。在轨迹引导下，各分量（位置、旋转、速度）之间缺乏一致性约束，导致控制误差在整个去噪过程中波动剧烈（Fig. 4, Fig. 11）。
- **简化表示** $(\mathbf{r}^{a}, \mathbf{r}^{x}, \mathbf{r}^{z}, \mathbf{r}^{y}, \mathbf{j}^{p})$：仅保留根运动参数和关节局部位置，丢弃旋转、速度和足部接触标签。这一精简使轨迹引导的梯度信号更集中，控制误差显著降低且更稳定（Fig. 11, Fig. 12）。

该设计的深层洞察在于：轨迹控制本质上只需要位置信息，冗余分量（旋转、速度）在引导过程中反而成为噪声源。这一发现对后续多条件生成任务的表示设计具有参考价值。

### 选择性修复机制（SIM）的定位

运动修复阶段的训练策略是 CMC 的另一创新点。传统修复模型（如 **PriorMDM**，Shafir et al., ICLR 2024）仅训练修复任务，容易对特定掩码模式过拟合，导致对分布外部分观测的泛化能力不足。

SIM 以 50% 概率交替进行标准文本到运动生成和运动修复训练（Fig. 6, Fig. 7），本质上是一种多任务正则化策略。消融实验（TABLE IV）表明，引入 SIM 后，文本到运动生成任务的 FID 和 R-precision 均有明显改善，且修复模型对分布外观测的泛化能力增强（Fig. 10）。这一策略可迁移至其他需要修复能力的多条件生成场景（如人体与物体交互生成）。

### 适用边界与局限

尽管 CMC 在控制精度和运动质量上达到最优，其适用边界和局限值得关注：

1. **分布外轨迹泛化不足**：在极端轨迹（如骨盆高度 3 米）下，CMC 仍可能生成地面行走运动。原因在于绝对坐标表示缺乏对高度维度的归一化，模型难以泛化到训练分布外的空间范围。采用相对高度表示或其他归一化坐标可能是改进方向。

2. **轨迹引导空间的选择**：当前轨迹引导在原始运动空间而非潜在空间中实施，导致序列数据上梯度累积不均匀，影响部分轨迹的精确跟随。如何在潜在空间中施加轨迹引导，是克服这一局限的开放问题。

3. **误差未完全消除**：尽管平均控制误差已降至 0.51 cm（HumanML3D 骨盆控制），轨迹误差和位置误差仍未完全消除，存在进一步优化空间。

### 知识库定位总结

CMC 在轨迹控制人体运动生成的方法谱系中处于“解耦式多条件协调”节点，其贡献可归纳为三个可迁移的设计原则：

| 设计原则 | 具体实现 | 可迁移场景 |
|---------|---------|-----------|
| 条件分阶段解耦 | 轨迹控制 → 运动修复 | 多条件生成任务中条件间存在冲突的场景 |
| 任务导向的表示简化 | 简化表示丢弃非位置分量 | 需要稳定引导信号的扩散模型应用 |
| 多任务正则化训练 | SIM 交替生成与修复 | 需要修复能力的条件生成模型 |

这些原则的共同基础是“减少条件间干扰”这一核心洞察，其有效性已在文本-轨迹双条件场景中得到充分验证（TABLE III 消融实验：解耦框架相较单阶段框架 FID 和 R-precision 显著提升，控制误差大幅降低）。后续工作可沿三个方向推进：潜在空间引导机制设计、归一化坐标表示、以及 SIM 策略向其他多条件生成任务的迁移。



## 原文 PDF

![[paperPDFs/arxiv_2026/Coordinating_Multiple_Conditions_for_Trajectory-Controlled_Human_Motion_Generation.pdf]]
