---
title: "FloodDiffusion: Tailored Diffusion Forcing for Streaming Motion Generation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/FloodDiffusion_Tailored_Diffusion_Forcing_for_Streaming_Motion_Generation.pdf
project_link: https://shandaai.github.io/FloodDiffusion/
code_link: null
aliases:
- FloodDiffusion
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 三个关键修改：(i) 用双向注意力替代因果注意力；(ii) 用下三角时间调度器替代随机调度；(iii) 用连续时间变化的文本条件融合替代显式刷新机制。
primary_logic: 通过向量化时间调度和双向注意力，可以在保持精确似然（非ELBO代理）的同时实现有界延迟的流式生成；这些订制使扩散强制首次在流式运动生成上达到与离线方法竞争的SOTA性能。
claims:
- 移除双向注意力（改用因果注意力）导致FID从0.057恶化至3.377，完全失效。
- 移除下三角调度（改用随机调度）导致FID从0.057恶化至3.883，证明该调度对训练–测试匹配至关重要。
- 在HumanML3D上取得FID 0.057，优于所有现有流式方法，并与离线SOTA方法相当。
- HumanML3D 上 FID↓ = 0.057
---

# FloodDiffusion: Tailored Diffusion Forcing for Streaming Motion Generation

> [!tip] 核心洞察
> 通过向量化时间调度和双向注意力，可以在保持精确似然（非ELBO代理）的同时实现有界延迟的流式生成；这些订制使扩散强制首次在流式运动生成上达到与离线方法竞争的SOTA性能。

| 字段 | 内容 |
|------|------|
| 中文题名 | FloodDiffusion：用于流式运动生成的定制扩散强制 |
| 英文题名 | FloodDiffusion: Tailored Diffusion Forcing for Streaming Motion Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Cai_FloodDiffusion_Tailored_Diffusion_Forcing_for_Streaming_Motion_Generation_CVPR_2026_paper.html) · [Project](https://shandaai.github.io/FloodDiffusion/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | FloodDiffusion |
| Dataset | HumanML3D, BABEL |

> [!tip] 效果简介
> - HumanML3D 上，FID↓ 0.057 vs 0.109 (MoMask, 非流式 SOTA) (优于所有流式基线，与离线SOTA持平)；R@1↑ 0.523 vs 0.433 (MotionStreamer) (+0.090)。
> - BABEL 上，PJ→ (closer to real is better) 0.713 vs 0.641 (PRIMAL) (优于所有流式基线)；AUJ↓ 14.05 vs 17.20 (PRIMAL) (-3.15)。

## 概要

### 问题与瓶颈

流式人体运动生成要求模型根据连续到达的文本提示实时产生连贯的动作序列，延迟必须可控。现有方案主要分两类：**离线方法**（如 **MoMask** (Guo et al., CVPR 2024)、**MDM**、**MotionDiffuse** (Zhang et al., TPAMI 2024)）需等待完整提示序列才能生成，无法满足流式场景；**流式方法**（如 **PRIMAL**、**MotionStreamer**）虽支持逐帧输出，但生成质量与文本对齐精度均显著落后于离线方法。

扩散强制（diffusion forcing）是一种为视频生成设计的流式框架，理论上具备精确似然和低延迟。然而，**原始扩散强制的三个设计选择——因果注意力、随机时间步调度、显式文本刷新机制——直接阻碍了它在运动生成上的有效迁移**，导致生成质量严重退化。

### 核心方法：FloodDiffusion

**FloodDiffusion** 对扩散强制进行了三项关键订制，使其首次适配流式运动生成：

1. **双向注意力替代因果注意力**：在激活窗口内使用双向自注意力，保证缓冲帧始终基于最新文本提示去噪，而非被历史帧单向约束。
2. **下三角时间调度器替代随机调度**：定义向量化调度 $\alpha_t^k = \mathrm{clamp}(t - \frac{k}{n_s}, 0, 1)$，使训练与推理的噪声–数据插值严格匹配，同时实现有界延迟的逐帧流式输出。
3. **连续时变文本条件融合替代显式刷新**：通过逐帧注入 T5 文本特征并结合旋转嵌入与偏置注意掩码，实现无需显式提示变化检测的平滑条件切换。

整体框架由三个模块构成：**因果 VAE** 将 263 维运动流压缩为 4 维潜在序列并支持因果解码；**DiT 去噪器**在潜在空间预测速度场；**时变文本条件注入**实现连续的条件融合。

### 主要结果

在 **HumanML3D** 基准上，FloodDiffusion 取得 **FID 0.057**，不仅显著优于所有现有流式方法，更与离线 SOTA 方法 **MoMask**（FID 0.109）相当甚至更优；文本对齐指标 **R@1 达到 0.523**，较最强流式基线 MotionStreamer 提升 0.090。在 **BABEL** 基准上，FloodDiffusion 在流式质量指标 PJ 和 AUJ 上均超越所有流式基线。

消融实验揭示了订制设计的决定性作用：移除双向注意力（改用因果注意力）导致 FID 从 0.057 飙升至 **3.377**；将下三角调度替换为随机调度使 FID 恶化至 **3.883**，验证了这两个修改对模型性能的根本性影响。

### 方法谱系与知识库定位

FloodDiffusion 处于**扩散生成 × 流式推理 × 人体运动建模**的交汇点。它继承扩散强制的精确似然框架，但通过向量化时间调度和双向注意力将其从视频域迁移至运动域。与基于块的扩散方法（如 PRIMAL）不同，FloodDiffusion 的三角调度实现了帧级粒度的渐进去噪，延迟更低；与基于因果 VAE + 自回归扩散头的 MotionStreamer 相比，FloodDiffusion 的双向注意力在激活窗口内保留了更强的上下文建模能力。

### 流式人体运动生成的任务特性

人体运动生成任务旨在根据文本描述合成逼真的三维人体动作序列。在交互式应用（如游戏、虚拟现实、具身智能体控制）中，系统必须在接收到新的文本指令后**实时、连续地输出运动帧**，而不能等待完整序列生成完毕——这种设定被称为**流式运动生成**（streaming motion generation）。与离线生成不同，流式生成面临三个核心约束：

1. **低延迟响应**：新指令到达后，系统需在极短帧数内完成动作语义切换。
2. **时序因果性**：生成当前帧时只能依赖已观察到的历史帧和当前条件，不能“窥视”未来帧。
3. **连续条件融合**：文本指令随时间动态变化，模型需无缝融合新旧条件，避免运动突变或语义断裂。

### 扩散强制（Diffusion Forcing）的潜力与原生缺陷

扩散强制（Diffusion Forcing）是近期提出的一种用于序列生成的概率框架。其核心思想是将扩散模型的时间步与序列帧索引进行耦合，通过调节每帧的噪声水平来控制生成进度，从而在**保持精确似然（而非ELBO代理）**的同时实现有界延迟的流式生成。这一特性使其天然适合流式运动生成任务。

然而，**原始扩散强制（vanilla diffusion forcing）是为视频生成设计的**，其三个关键设计选择在运动生成场景下构成了根本性瓶颈：

- **因果注意力（causal attention）**：视频生成中为保证时序因果性采用因果掩码，但这限制了当前帧对最新文本条件的充分利用。在运动生成中，缓存窗口内的帧需要基于最新文本提示进行去噪，因果注意力无法做到这一点。
- **随机时间步调度（random timestep sampling）**：训练时随机采样各帧的噪声水平，导致激活窗口大小不确定，且训练与推理的调度分布不匹配，严重损害生成质量。
- **显式文本刷新机制（explicit refresh mechanism）**：当新提示到达时触发显式条件切换，这种方式在运动生成中容易引入不自然的动作断裂。

### 本文动机与核心洞察

本文的核心洞察是：**通过订制扩散强制的注意力模式、时间调度和条件融合机制，可以使其首次在流式运动生成上达到与离线方法竞争的SOTA性能**。具体而言，FloodDiffusion 提出三个针对性修改：

| 修改维度 | 原始扩散强制 | FloodDiffusion | 作用机制 |
|---------|------------|---------------|---------|
| 注意力模式 | 因果注意力 | 双向自注意力 | 保证缓存窗口内所有帧基于最新文本条件去噪 |
| 时间调度 | 随机采样 | 下三角调度 $\alpha_t^k = \mathrm{clamp}(t - \frac{k}{n_s}, 0, 1)$ | 固定激活窗口大小，消除训练–推理分布失配 |
| 条件融合 | 显式刷新机制 | 连续时变文本条件注入 | 逐帧通过偏置注意掩码融合T5特征，无需检测提示切换 |

这三个修改相互协同：下三角调度确定了每步去噪的激活帧范围，双向注意力使该范围内的帧能充分感知当前条件，而连续条件注入则保证文本语义随时间平滑过渡。实验表明，**移除双向注意力使FID从0.057恶化至3.377，移除下三角调度使FID恶化至3.883**（Table 3），验证了每个修改的决定性作用。

### 与现有流式方法的差距

在FloodDiffusion之前，流式运动生成方法主要分为两类：

- **基于块扩散的方法**（如PRIMAL）：将运动流分割为固定块，块内统一去噪。这种方法响应延迟高，且块边界处容易产生不连续。
- **因果VAE + 自回归扩散头**（如MotionStreamer）：使用因果VAE编码运动，再通过自回归扩散头逐帧生成。该方法受限于自回归的误差累积和有限的全局感知能力。

这些方法在HumanML3D基准上的FID均显著弱于离线SOTA方法（如MoMask的0.109），且无法同时保证低延迟和高质量。FloodDiffusion通过订制扩散强制框架，在保持流式生成能力的同时，将FID提升至0.057，**首次实现流式方法与离线SOTA的性能持平**。

## 核心方法与创新机理

FloodDiffusion 的核心创新在于对扩散强制（diffusion forcing）框架进行了三项针对性订制，使其从视频生成领域成功迁移至流式人体运动生成任务。原始扩散强制为视频生成设计，采用因果注意力、随机时间步调度和显式文本刷新机制，但这些设计无法正确建模运动分布，导致生成质量严重退化。FloodDiffusion 通过以下三个关键修改解决了这一瓶颈：

### 1. 双向注意力替代因果注意力

原始扩散强制使用因果自注意力，每个帧只能看到过去的信息。在流式运动生成中，激活窗口内的帧需要基于最新的文本提示进行联合去噪，因果注意力限制了帧间信息交互。FloodDiffusion 将因果注意力替换为**双向自注意力**，确保缓冲窗口内的所有帧能够基于当前文本条件进行充分交互。消融实验表明，移除双向注意力（改用因果注意力）会导致 FID 从 0.057 急剧恶化至 3.377，MM-Dist 从 2.852 升至 12.42，模型完全失效。

### 2. 下三角时间调度器替代随机调度

原始扩散强制为每个帧随机采样独立的时间步，导致训练与推理阶段的时间调度不匹配，且激活窗口边界不确定。FloodDiffusion 提出**下三角时间调度器**（lower-triangular schedule），定义第 $k$ 帧在时刻 $t$ 的噪声-数据插值系数为：

$$\alpha_t^k = \mathrm{clamp}\left(t - \frac{k}{n_s}, 0, 1\right)$$

其中 $n_s$ 为流式斜率大小。该调度创建了一种级联激活模式：每一帧从纯噪声到干净数据的过渡在时间轴上依次展开，激活窗口随推理时间步以恒定速率推进。这不仅保证了训练与测试阶段的时间调度严格匹配，还实现了有界延迟的逐帧流式生成。消融实验表明，将下三角调度替换为随机调度会导致 FID 恶化至 3.883，证明该调度对训练-测试匹配至关重要。

### 3. 连续时变文本条件融合替代显式刷新机制

原始扩散强制依赖显式检测新提示到来并触发刷新操作，这在运动生成中引入不自然的条件切换。FloodDiffusion 采用**连续时变文本条件融合**：将预训练 T5 编码器提取的文本特征逐帧注入，通过旋转位置嵌入和偏置注意力掩码实现平滑的条件过渡，无需显式刷新检测。这使得模型能够自然处理随时间变化的文本提示，生成与文本时序对齐的连续运动。

### 关键设计洞察

通过向量化时间调度与双向注意力的结合，FloodDiffusion 在保持精确似然（非 ELBO 代理）的同时实现了有界延迟的流式生成。这三项订制使扩散强制首次在流式运动生成任务上达到与离线方法竞争的 SOTA 性能：在 HumanML3D 上取得 FID 0.057，优于所有现有流式方法，并与离线 SOTA 方法 **MoMask**（Guo et al., CVPR 2024）的 0.109 相当甚至更优。

FloodDiffusion 是一种基于**扩散强制（diffusion forcing）**的潜在扩散框架，专为流式人体运动生成设计。其核心流水线由三个紧密协作的模块构成：**因果 VAE（Causal VAE）**、**双向注意力 DiT 去噪器**，以及**连续时变文本条件注入**。整个框架的输入为时变文本提示序列，输出为与之对齐的连续人体运动流。

**因果 VAE 压缩运动流。** 原始运动序列为 263 维的高维表示。因果 VAE 首先将其编码为紧凑的 4 维潜在序列（时间下采样因子为 4），随后通过因果解码器逐帧重建，保证流式输出时不会发生信息泄漏。这一步将高维运动生成问题转化为低维潜在空间中的条件序列建模问题。

**下三角时间调度驱动流式生成。** 框架的核心创新在于用**向量化下三角时间调度**替代传统扩散强制中的随机调度。对于长度为 $K$ 的序列，第 $k$ 帧在时刻 $t$ 的噪声-数据插值系数定义为：
$$\alpha_t^k = \mathrm{clamp}(t - \frac{k}{n_s}, 0, 1)$$
其中 $n_s$ 为流式斜率（streaming slope size），控制每步去噪的帧数。该调度产生级联式激活模式：每个时刻仅有一个“激活窗口”内的帧参与去噪，窗口以恒定速率向前推进，从而实现了**有界延迟的流式推理**。

**DiT 去噪器预测速度场。** 在潜在空间中，一个扩散 Transformer（DiT）被训练来预测条件速度场 $u_t(\mathbf{x} \mid \mathbf{z})$。训练目标为流匹配损失：
$$\hat{u}_t(\mathbf{x},\mathbf{c}) = \arg\min_{u_t^\theta} \mathbb{E}_{t,\mathbf{z},\epsilon}\left[\|u_t^\theta(\mathbf{x}_t,\mathbf{c}) - u_t(\mathbf{x}_t \mid \mathbf{z})\|^2\right]$$
与原始扩散强制采用**因果注意力**不同，FloodDiffusion 在激活窗口内使用**双向自注意力**，确保缓冲区内所有帧都能基于最新的文本提示进行去噪。这一设计被消融实验证明是决定性的：切换为因果注意力后，FID 从 0.057 急剧恶化至 3.377。

**时变文本条件连续融合。** 文本条件通过预训练的 T5 编码器提取逐帧特征，并借助旋转位置嵌入和偏置注意力掩码注入去噪网络。与原始扩散强制中需要显式检测提示刷新并触发条件切换的机制不同，FloodDiffusion 的时变条件融合是**连续且无缝的**——文本提示的变化通过注意力掩码自然传导至对应帧，无需推理阶段的额外优化。

**推理流程。** 推理时，模型从标准高斯噪声 $\mathcal{N}(\mathbf{0}, \mathbf{I})$ 初始化，按固定步长推进时间 $t$。在每个时间步，仅对激活窗口 $[m(t), n(t))$ 内的潜在帧计算速度并更新，已完成的帧直接输出。这种设计使得模型能够以恒定速率逐帧生成运动，同时保持精确似然（而非 ELBO 代理），在流式人体运动生成任务上首次达到了与离线方法竞争的 SOTA 性能。

![[assets/figures/papers/paper_list_l15_https_openaccess_thecvf_com_content_CVPR2026_html_Cai_FloodDiffusion_Tai/figures/002_Figure_2.jpg]]
*Figure 2: Pipeline Overview. FloodDiffusion is a latent diffusion based framework, the 263D motion stream is encoded to a compact 4D latent sequence via our causal VAE. Then the model predicts the velocity for the latent*

FloodDiffusion 的核心架构由三个紧密耦合的模块构成，共同实现从时变文本提示到连续运动序列的流式生成。图2给出了整体流水线概览：263维运动流经因果VAE压缩为4维潜在序列，随后由DiT去噪器在向量化时间调度下预测速度场，并通过逐帧文本条件注入实现连续语义控制。

### 3.1 向量化时间调度：流式生成的数学基础

传统扩散模型使用标量时间步 $t \in [0,1]$ 统一控制全序列的噪声水平，这无法支持逐帧异步去噪的流式场景。FloodDiffusion 将标量调度推广为**向量化时间调度**（Vectorized Time Schedule），为每一帧分配独立的时间变量。

**初始化分布**：扩散过程从标准高斯白噪声起始：

$$p_{\mathrm{init}} = \mathcal{N}(\mathbf{0}, \mathbf{I})$$

**条件腐蚀路径**：对于单帧数据 $\mathbf{z}$，其在时刻 $t$ 的条件分布为高斯：

$$p_t(\mathbf{x} \mid \mathbf{z}) = \mathcal{N}\big(\mathbf{x}; \alpha_t\mathbf{z}, \beta_t^2\mathbf{I}\big)$$

其中 $\alpha_t$ 和 $\beta_t$ 分别控制信号保留与噪声注入的程度。当 $t=0$ 时 $\alpha_0=1, \beta_0=0$（纯数据），$t=1$ 时 $\alpha_1=0, \beta_1=1$（纯噪声）。

**下三角调度**（核心创新）：将上述标量路径推广到长度为 $K$ 的序列，定义第 $k$ 帧在时刻 $t$ 的噪声-数据插值系数：

$$\alpha_t^k = \mathrm{clamp}\left(t - \frac{k}{n_s}, 0, 1\right)$$

其中 $n_s$ 为流式斜率（streaming slope size），控制激活窗口的宽度。该调度具有下三角结构：对于任意时刻 $t$，只有索引满足 $k < t \cdot n_s$ 的帧已完成或正在进行去噪，其余帧仍为纯噪声。图3对比了三种调度策略：扩散强制的随机调度存在训练-测试不匹配且激活窗口不确定；分块扩散对块内所有帧统一去噪导致高响应延迟；而下三角调度仅对激活窗口去噪，以恒定逐帧速率推进，实现了有界延迟的流式生成。

### 3.2 速度场预测与训练目标

FloodDiffusion 采用流匹配（flow matching）范式，直接回归条件速度场而非噪声或分数。

**向量化条件速度场**：在向量化时间调度下，条件速度场 $u_t(\mathbf{x} \mid \mathbf{z})$ 的解析形式为：

$$u_t(\mathbf{x} \mid \mathbf{z}) = \left(\dot{\alpha}_t - \frac{\dot{\beta}_t}{\beta_t} \odot \alpha_t\right) \odot \mathbf{z} + \left(\frac{\dot{\beta}_t}{\beta_t}\right) \odot \mathbf{x}$$

其中 $\odot$ 表示逐元素乘法，$\dot{\alpha}_t$ 和 $\dot{\beta}_t$ 为对应系数的时间导数。该公式给出了从当前状态 $\mathbf{x}$ 指向数据 $\mathbf{z}$ 的真实速度方向。

**速度训练目标**：神经网络 $u_t^\theta$ 通过最小化与真实速度场的均方误差进行训练：

$$\hat{u}_t(\mathbf{x}, \mathbf{c}) = \arg\min_{u_t^\theta} \mathbb{E}_{t, \mathbf{z}, \epsilon}\left[\|u_t^\theta(\mathbf{x}_t, \mathbf{c}) - u_t(\mathbf{x}_t \mid \mathbf{z})\|^2\right]$$

其中 $\mathbf{x}_t = \alpha_t \odot \mathbf{z} + \beta_t \odot \epsilon$ 为加噪样本，$\mathbf{c}$ 为文本条件。该目标直接优化速度预测精度，避免了ELBO代理损失带来的偏差。

### 3.3 因果VAE：低延迟潜在压缩

为实现高效流式推理，FloodDiffusion 首先将263维原始运动表示压缩至紧凑潜在空间。因果VAE采用时序下采样因子4，潜在通道维度设为4，将运动序列编码为低维潜在序列。其因果解码器确保每一帧的解码仅依赖当前及过去帧的潜在表示，不访问未来信息，从而天然支持流式输出。消融实验（Table 4）表明，该因果VAE在重建质量上与VQ-VAE及MotionStreamer的CausalVAE性能相当。

### 3.4 DiT去噪器与双向注意力

去噪器采用扩散Transformer（DiT）架构，在潜在空间预测速度场。与原始扩散强制使用因果注意力不同，FloodDiffusion在激活窗口内采用**双向自注意力**，使缓冲区内的帧能够基于最新文本提示进行联合去噪。这一设计的关键在于：在流式场景中，新提示到达时，已生成但尚未完全去噪的帧需要重新条件化，双向注意力允许这些帧充分利用当前语义信息进行修正。

### 3.5 时变文本条件注入

文本条件通过逐帧注入机制实现连续融合：从预训练T5编码器提取文本token特征，应用旋转位置嵌入后，通过偏置注意力掩码注入到每一帧的DiT层中。该设计取代了原始扩散强制的显式刷新检测机制，使模型能够自然地响应任意时刻的提示变化，无需推理时的额外优化。图4展示了时变条件注入的效果——相同文本提示在不同时刻给出，模型生成的动作序列呈现出符合时序逻辑的差异。

![[assets/figures/papers/paper_list_l15_https_openaccess_thecvf_com_content_CVPR2026_html_Cai_FloodDiffusion_Tai/figures/003_Figure_3.jpg]]
*Figure 3: Noise Schedule Comparison. Diffusion forcing samples a random schedule with uncertain active window and mismatches train–test schedule; Chunk diffusion denoises all frames within each chunk uniformly, incurring high response latency. Our triangular schedule denoises only the active window and advances at a constant per-frame rate*

![[assets/figures/papers/paper_list_l15_https_openaccess_thecvf_com_content_CVPR2026_html_Cai_FloodDiffusion_Tai/figures/004_Figure_4.jpg]]
*Figure 4: Comparison of time-varying conditioning. Our model generates different resulting motions from the same text prompts based on their delivery timing. (Top Left) Prompts are given separately at different frames. (Top Right) All conditions are fed as a single prompt at once. (Bottom Left) Two separate prompts are input early in the sequence. (Bottom Right) The same two separate prompts are input later in the sequence*

## 实验与关键发现

### 主实验结果

FloodDiffusion 在两个主流文本驱动运动生成基准 HumanML3D 和 BABEL 上进行了系统评估，评估维度覆盖对齐性（R@k）、质量（FID）、多模态性（MM-Dist）和流式质量（PJ→、AUJ↓）。**Table 1** 汇总了与离线 SOTA 方法和流式基线的全面对比。

![[assets/figures/papers/paper_list_l15_https_openaccess_thecvf_com_content_CVPR2026_html_Cai_FloodDiffusion_Tai/figures/006_Table_1.jpg]]
*Table 1: Quantitative evaluation on HumanML3D and BABEL test sets. We report alignment (R@k↑), quality (FID↓), multimodality (MM-Dist↓), and streaming quality (PJ→, AUJ↓). → means closer to ‘Real motion’ is better; ± indicates 95% confidence intervals; ‘–’ means not applicable. We compare against SOTA non-streaming (MoMask [8]), etc., and streaming (PRIMAL [38], MotionStreamer [30]) methods. FloodDiffusion achieves the best R@k and MM-Dist, a competitive FID (0.057) on HumanML3D, and outperforms all streaming baselines on BABEL*

在 HumanML3D 上，FloodDiffusion 取得了 **FID = 0.057**，显著优于所有流式基线，并与离线 SOTA 方法 **MoMask**（Guo et al., CVPR 2024，FID = 0.109）持平甚至略优。在对齐性方面，FloodDiffusion 的 **R@1 = 0.523**，比最强流式基线 **MotionStreamer**（R@1 = 0.433）提升 +0.090，且 R@2（0.717）和 R@3（0.810）同样领先。多模态性 MM-Dist 达到 2.852，也优于所有对比方法。这表明模型在保持运动质量的同时，对文本条件的语义对齐能力达到了新高度。

在 BABEL 数据集上，FloodDiffusion 在流式质量指标上全面超越现有流式方法：**PJ→ = 0.713**（越接近真实运动的 0.732 越好），优于 **PRIMAL**（0.641）；**AUJ↓ = 14.05**，同样优于 PRIMAL（17.20）。这验证了定制扩散强制在长序列流式生成场景下的鲁棒性。

用户研究（**Table 2**）采用 Bradley-Terry 模型，100 名参与者将三种生成模型（PRIMAL、MotionStreamer、FloodDiffusion）与真实运动在三个感知维度上进行比较。FloodDiffusion 在所有维度上获得最高的偏好分数（0.024），表明其生成的运动在自然度和文本契合度上最接近真实数据。

### 消融实验

**Table 3** 揭示了两个核心设计选择的决定性作用：

1. **双向注意力的必要性**：将双向自注意力替换为因果注意力后，FID 从 0.057 急剧恶化至 **3.377**，MM-Dist 从 2.852 飙升至 12.42。这表明在扩散强制的流式框架中，因果注意力无法有效利用当前文本条件对缓冲帧进行去噪，是导致生成质量崩溃的直接原因。

2. **下三角时间调度器的不可替代性**：将下三角调度替换为原始扩散强制的随机调度后，FID 恶化至 **3.883**，MM-Dist 升至 9.58。这验证了随机调度导致的训练-测试不匹配对运动分布建模的破坏性影响——下三角调度通过确定的激活窗口和恒定的逐帧推进速率，保证了训练与推理的一致性。

3. **分类器自由引导（CFG）尺度的影响**：**Figure 6** 展示了 CFG 尺度从 1 到 8 的变化曲线。当 CFG = 1（无引导）时性能显著下降；随着尺度增大，FID 和 MM-Dist 持续改善，在 **CFG = 6** 处取得最优折中（FID = 0.057，MM-Dist = 2.852）。进一步增大尺度会导致运动多样性降低。

![[assets/figures/papers/paper_list_l15_https_openaccess_thecvf_com_content_CVPR2026_html_Cai_FloodDiffusion_Tai/figures/010_Figure_6.jpg]]
*Figure 6: Effect of Classifier-Free Guidance (CFG) scale. We report FID (left axis, ↓) and MM-Dist (right axis, ↓) with the CFG scale. Both metrics improve significantly as the scale increases from 1, achieving an optimal trade-off at CFG=6 (FID=0.057, MM-Dist=2.852)*

因果 VAE 架构的消融（**Table 4**）表明，采用 Wan CausalVAE 的变体在重建质量上与 VQ-VAE 和 MotionStreamer 的 CausalVAE 相当，验证了 VAE 组件选择的合理性。

![[assets/figures/papers/paper_list_l15_https_openaccess_thecvf_com_content_CVPR2026_html_Cai_FloodDiffusion_Tai/figures/008_Table_4.jpg]]
*Table 4: Ablation on Causal VAE architectures. We compare VAE reconstruction quality using VQ-VAE [35], Motion-Streamer’s CausalVAE [30], and our adopted Wan CausalVAE [29]. The results show comparable performance across the different causal variants*

### 失败模式与局限

尽管 FloodDiffusion 在定量指标上表现优异，论文明确指出了两个主要局限：

1. **缺乏历史感知能力**：模型未经过指令微调，也不具备对已生成动作的显式语义记忆。当文本提示涉及对过去动作的引用（如“重复上一个动作”）时，模型无法正确理解和执行。这限制了其在需要长程上下文理解的交互场景中的应用。

2. **风格与长期一致性未覆盖**：由于缺乏长期风格化数据，模型未针对风格切换或长期一致性问题进行训练和客观评估。论文提出伪标记长运动数据可能缓解这一问题，但当前版本尚未实现。

此外，用户研究虽采用 Bradley-Terry 模型，但未报告参与者间一致性指标（如 Krippendorff's α），其统计可靠性需结合原始数据进一步验证。

## 定位与知识库关联

### 1. 在扩散运动生成谱系中的位置

FloodDiffusion 处于**扩散运动生成**和**流式序列建模**的交叉点。其核心架构继承自三个技术脉络：

- **扩散强制（Diffusion Forcing）**：直接继承自视频生成的扩散强制范式，但针对运动生成任务做了三项关键订制（双向注意力、下三角调度、连续文本条件融合），使其首次在流式运动生成上达到与离线方法竞争的性能。
- **潜在扩散（Latent Diffusion）**：采用因果 VAE 将 263 维运动流压缩至 4 维潜在空间（时域下采样因子 4），在潜在空间执行扩散过程，显著降低计算开销。
- **流匹配（Flow Matching）**：训练目标直接回归条件速度场 $u_t(\mathbf{x} \mid \mathbf{z})$，而非噪声预测，与下三角向量化调度天然兼容。

### 2. 与基线方法的对比关系

FloodDiffusion 的基线可划分为**非流式（离线）方法和流式方法**两个阵营，论文在 HumanML3D 和 BABEL 上进行了系统比较。

**非流式方法（离线生成）**：
- **MoMask**（Guo et al., CVPR 2024）：基于掩码建模的 SOTA 离线方法，FID 0.109。FloodDiffusion 以 FID 0.057 显著超越，且在 R@1 上达到 0.523（MoMask 未报告流式指标）。
- **MDM**：扩散运动生成基线，论文 Table 1 中 FloodDiffusion 在全部对齐和质量指标上均优于 MDM。
- **MotionDiffuse**（Zhang et al., TPAMI 2024）：文本驱动扩散方法，FloodDiffusion 在 FID 和 R@k 上均取得更优结果。

**流式方法（在线生成）**：
- **PRIMAL**：基于块扩散的流式方法。在 BABEL 上 FloodDiffusion 的 PJ→ 为 0.713（PRIMAL 为 0.641），AUJ↓ 为 14.05（PRIMAL 为 17.20），在所有流式指标上均占优。
- **MotionStreamer**：采用因果 VAE + 自回归扩散头。FloodDiffusion 在 HumanML3D 上 R@1 为 0.523（MotionStreamer 为 0.433），FID 为 0.057（MotionStreamer 更高），且用户研究中 Bradley-Terry 得分最高。

**关键差异机制**：
- PRIMAL 和 MotionStreamer 均采用**因果注意力**和**逐块/逐帧自回归**生成策略，导致误差累积和文本条件滞后。
- FloodDiffusion 通过**双向注意力 + 下三角调度**，使激活窗口内的帧能基于最新文本提示联合去噪，在保持有界延迟的同时避免了误差累积。

### 3. 核心适用边界

FloodDiffusion 的设计假设决定了其适用边界：

- **输入模态**：当前仅支持文本提示作为控制信号。论文将控制信号记为 $\mathbf{c}^{0:K}$，但实验仅验证了文本条件。扩展到音频、力反馈等多模态条件需要重新设计条件融合机制。
- **运动表征**：依赖 263 维 SMPL-H 参数化（包含根位移、关节旋转等），适用于人体运动生成。泛化到其他骨架拓扑或非人体运动需要重新训练 VAE 和扩散主干。
- **流式假设**：要求控制信号以流式方式到达，且模型不维护对已生成动作的显式语义记忆。这意味着难以处理“重复上一个动作”等需要理解历史的指令。
- **生成质量与延迟的折中**：下三角调度的斜率 $n_s$ 控制激活窗口大小。论文使用 $n_s = 5$ 作为默认值，但未系统研究不同 $n_s$ 对延迟–质量的 Pareto 前沿影响。

### 4. 已知局限与未解决问题

**论文明确指出的局限**：
1. **缺乏指令微调与语义记忆**：模型未经过指令微调，不具备对已生成动作的显式语义记忆，难以处理需要理解过去动作的提示（如“重复上一个动作”或“加快当前动作”）。
2. **风格切换与长期一致性未评估**：由于缺乏长期风格化数据，模型未针对风格切换或长期一致性问题进行训练或客观评估。论文建议通过伪标记长运动数据（如从视频或游戏提取）来缓解这一问题。
3. **条件模态单一**：当前仅验证了文本条件，未探索音频、力反馈、环境反馈等多模态流式条件的融合。

**开放问题**：
- 如何在保持流式低延迟的前提下，引入指令微调或显式记忆机制，使模型能理解并执行依赖于过去动作序列的复杂指令？
- 如何有效获取或生成伪标注的长时运动数据，以支持风格迁移和长期一致性等下游评估？
- 能否将下三角调度推广到更一般的条件分布（如非均匀时间步、变长度文本段），以处理真实应用中不规则的提示到达模式？
- 当前框架要求控制信号 $\mathbf{c}^{0:K}$ 与运动帧一一对应，如何处理无对齐标注的弱监督流式条件（如段落级文本描述）？

### 5. 知识库定位

FloodDiffusion 的方法贡献可定位于以下知识节点：

- **扩散强制订制**：首次证明扩散强制可通过三项订制（双向注意力、下三角调度、连续文本融合）适配流式运动生成，为扩散强制在其他时序生成任务（如语音、音乐）上的应用提供了订制范式。
- **向量化时间调度**：提出的下三角调度 $\alpha_t^k = \mathrm{clamp}(t - k/n_s, 0, 1)$ 是一种通用的流式扩散调度方案，可独立于运动生成应用于其他需要有界延迟的序列生成任务。
- **流式运动生成基准**：在 HumanML3D 和 BABEL 上建立了流式运动生成的强基线，首次在 FID 上达到与离线 SOTA 竞争的水平（0.057 vs. MoMask 0.109），为后续流式方法提供了明确的性能标杆。

## 原文 PDF

![[paperPDFs/CVPR_2026/FloodDiffusion_Tailored_Diffusion_Forcing_for_Streaming_Motion_Generation.pdf]]
