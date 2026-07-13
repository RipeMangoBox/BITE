---
title: "ActionPlan: Future-Aware Streaming Motion Synthesis via Frame-Level Action Planning"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/ActionPlan_Future_Aware_Streaming_Motion_Synthesis_via_Frame_Level_Action_Planning.pdf
code_link: null
project_link: https://coral79.github.io/ActionPlan/
aliases:
- ActionPlan
tags:
- CVPR_2026
- topic/motion_animation
- topic/motion_animation/human_motion_generation
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
- topic/diffusion_model
core_operator: "引入逐帧动作计划（frame-level action plan）作为密集语义锚点，使模型先“预见”完整动作序列，再通过异构扩散时间步（每帧独立时间步）实现灵活的去噪调度，从而打通离线高质量与在线低延迟生成。"
primary_logic: "将高层动作规划与低层运动合成解耦：首先生成与运动帧严格对齐的文本潜在表示作为动作计划，再以动作计划为条件，采用重叠窗口渐进去噪（随机或顺序）生成运动。该两阶段范式在保持未来感知的同时支持流式输出、零样本编辑和插帧。"
claims:
- "引入动作计划后，流式模式FID从8.018降至5.878，R-Precision@3从0.854升至0.875（Table 2 E vs B），证明动作计划有效提升了在线生成质量。"
- "在完整HumanML3D-272数据集上训练并使用动作计划（Table 2E）显著优于仅使用部分重叠子集（A, B）和联合生成（D），验证了masked loss和两阶段采样的必要性。"
- "渐进采样重叠窗口K=2在FID（5.522）和R-Precision@3（0.892）之间达到最佳平衡，优于完全并行或完全串行调度（Table 3）。"
- "在四个复杂文本提示上，ActionPlan正确执行了所有指定动作，而MARDM和MotionStreamer频繁遗漏或错序关键动作（Fig. 4）。"
---

# ActionPlan: Future-Aware Streaming Motion Synthesis via Frame-Level Action Planning

> [!tip] 核心洞察
> 将高层动作规划与低层运动合成解耦：首先生成与运动帧严格对齐的文本潜在表示作为动作计划，再以动作计划为条件，采用重叠窗口渐进去噪（随机或顺序）生成运动。该两阶段范式在保持未来感知的同时支持流式输出、零样本编辑和插帧。

| 字段 | 内容 |
|------|------|
| 中文题名 | ActionPlan：基于逐帧动作规划的未来感知流式运动合成 |
| 英文题名 | ActionPlan: Future-Aware Streaming Motion Synthesis via Frame-Level Action Planning |
| 会议/期刊 | arXiv 2026 |
| Links | [paper](https://arxiv.org/abs/2603.13500) · [Project](https://coral79.github.io/ActionPlan/) |
| Topic | #topic/streaming_motion_synthesis #topic/text_to_motion #topic/action_planning #topic/diffusion_model |
| Method | Frame-level action plan, two-stage hierarchical diffusion, heterogeneous timesteps, progressive denoising |
| Dataset | HumanML3D-272, BABEL frame-level annotations |

> [!tip] 效果简介
> - HumanML3D-272 test set 上，FID↓ 为 5.522 (Offline) / 5.735 (Streaming)，对比 7.044 (MARDM, best offline)，变化 ↓22%。
> - HumanML3D-272 test set 上，R-Precision@3↑ 为 0.892 (Offline) / 0.877 (Streaming)，对比 0.860 (MARDM)，变化 ↑0.032 / ↑0.017。
> - HumanML3D-272 test set 上，FID↓ (streaming) 为 5.735，对比 11.790 (MotionStreamer)，变化 ↓51%。

## 概要

现有流式运动合成方法因缺乏未来上下文而产生语义漂移和动作遗漏，离线方法虽质量高但无法实时推理，两者长期割裂，难以在单一模型中统一。ActionPlan 提出一种两阶段分层扩散框架，将高层动作规划与低层运动合成解耦：首先生成与运动帧严格对齐的逐帧动作计划（frame-level action plan）作为密集语义锚点，再以动作计划为条件，采用重叠窗口渐进去噪生成运动。该框架在保持未来感知的同时支持流式输出、零样本编辑和插帧。

核心结论如下：

- **离线模式**：ActionPlan 在 HumanML3D-272 测试集上取得 FID 5.522、R-Precision@3 0.892，较最佳离线方法 MARDM（FID 7.044）改善约22%（Table 1）。
- **流式模式**：ActionPlan 以 FID 5.735 显著优于现有流式方法 MotionStreamer（FID 11.790，改善约51%），且首 token 延迟仅 146 ms，持续生成每 token 40 ms，较对比方法加速 1.44×–9×（Table 1 及运行时性能表）。
- **消融验证**：引入动作计划后，流式模式 FID 从 8.018 降至 5.878（Table 2 E vs B）；渐进采样窗口大小 K=2 在 FID 与 R-Precision 之间取得最佳平衡（Table 3）。
- **定性评估**：在四个复杂文本提示上，ActionPlan 正确执行所有指定动作，而 MARDM 和 MotionStreamer 频繁遗漏或错序关键动作（Fig. 4）；用户研究中，ActionPlan 在文本到运动任务获得 67.5% 偏好，在长序列流式任务获得 67.7% 偏好。

方法定位上，ActionPlan 属于**扩散模型 + 分层规划**范式，通过异构扩散时间步（每帧独立时间步）和掩码损失实现全数据集训练，打通了离线高质量与在线低延迟生成。其两阶段采样策略（Stage 1 生成完整动作计划，Stage 2 以随机或光栅顺序渐进去噪）为流式运动合成提供了新的设计空间。



### 文本驱动运动合成的现状与瓶颈

文本驱动的人体运动合成旨在根据自然语言描述生成逼真的三维人体动作序列，在虚拟人动画、游戏开发和具身智能等领域具有广泛应用。近年来，扩散模型和自回归模型在该领域取得了显著进展，催生了**MDM**（Tevet et al., NeurIPS 2023）、**T2M-GPT**（Zhang et al., CVPR 2023）、**MoMask**（Guo et al., 2024）等代表性方法。然而，现有工作长期处于两极化状态：

- **离线方法**（如MDM、MLD、MoMask）在生成完整运动序列时质量较高，但需要完整的未来上下文，无法支持增量式实时推理。这从根本上限制了它们在交互式应用中的部署。
- **流式方法**（如**MotionStreamer**（Xiao et al., arXiv 2025）和**MARDM**（Mu et al., ICLR 2025））通过因果架构或自回归采样实现了逐帧输出，但由于缺乏对未来动作的全局感知，普遍存在**语义漂移**和**动作遗漏**问题——模型可能在生成过程中“忘记”文本中指定的关键动作，或错误地改变动作执行顺序。

这一瓶颈的本质在于：现有方法将高层动作规划与低层运动合成耦合在同一生成过程中，导致流式模式无法获得全局语义指导。离线模式虽能保持语义一致性，却以牺牲实时性为代价。

### 核心动机：打通离线高质量与在线低延迟

本文的核心动机是**在一个统一生成框架内同时实现离线模式的高质量和流式模式的低延迟**。实现这一目标的关键挑战在于：如何让模型在逐帧输出的同时，仍然“预见”完整的动作序列？

ActionPlan的解决方案是将动作规划与运动合成解耦为两阶段过程：
1. **第一阶段**：生成与运动帧严格对齐的逐帧文本潜在表示（称为“动作计划”），作为密集语义锚点。
2. **第二阶段**：以动作计划为条件，采用重叠窗口渐进去噪生成运动序列。

这一设计使模型在流式输出时仍具备未来感知能力，从根本上缓解了语义漂移问题。同时，通过异构扩散时间步（每帧独立时间步）和灵活的采样调度，ActionPlan在离线与流式模式间共享同一模型权重，无需针对不同场景重新训练。

### 技术挑战与本文贡献

实现上述目标面临三个核心技术挑战：

1. **如何获取帧级语义监督？** 现有的运动‑文本数据集（如HumanML3D）仅提供序列级描述，缺乏帧级标注。ActionPlan通过引入BABEL数据集的帧级动作标注，并设计掩码损失函数，使得模型可以在缺失帧级标注的序列上正常训练，从而充分利用全部HumanML3D-272数据。
2. **如何统一离线与流式的去噪调度？** 传统扩散模型对所有帧使用单一时间步，无法支持渐进式生成。ActionPlan提出异构时间步采样策略，为每帧运动潜在分配独立噪声水平，使模型在训练时即学习处理不同去噪阶段的帧。
3. **如何平衡生成质量与推理延迟？** 完全并行去噪质量最优但无法流式输出，完全串行去噪延迟过高。ActionPlan通过渐进采样窗口（重叠大小K=2）在FID与R-Precision之间取得最佳权衡，同时实现首token 146 ms、后续token仅40 ms的高效推理。



## 核心方法与创新机理

ActionPlan 的核心创新在于将**高层动作规划**与**低层运动合成**解耦为两阶段生成范式，从而在单一扩散模型中统一离线高质量生成与在线低延迟流式推理。这一解耦通过以下四个关键机制实现：

### 1. 逐帧动作计划作为密集语义锚点

现有文本到运动（T2M）方法仅使用全局文本描述作为条件信号，在流式生成中缺乏未来上下文，导致语义漂移和动作遗漏。ActionPlan 引入**逐帧动作计划**（frame-level action plan）：模型首先生成与运动帧一一对齐的 CLIP 文本潜在向量，再将这些潜在向量作为密集语义锚点，在去噪全程为运动潜在提供帧级条件信号。

具体而言，动作计划潜在 $\mathbf{y}_i$ 与运动潜在 $\mathbf{x}_i$ 在每帧拼接为联合向量 $(\mathbf{x}_i, \mathbf{y}_i)$，共同输入 Transformer 去噪器。这一设计使模型在生成任意帧时都能“预见”该帧应承载的语义意图，从根本上解决了流式方法因因果约束而缺失未来信息的问题。消融实验（Table 2）表明，引入动作计划后，流式模式 FID 从 8.018 降至 5.878，R-Precision@3 从 0.854 升至 0.875，验证了密集语义锚点的核心作用。

### 2. 异构扩散时间步：每帧独立噪声调度

传统扩散模型对所有潜在变量分配单一全局时间步，无法灵活控制不同帧的去噪进度。ActionPlan 提出**异构扩散时间步**（heterogeneous timesteps）：训练时对每个运动潜在 $\mathbf{x}_i$ 独立采样时间步 $t_i^x$，而动作计划潜在 $\mathbf{y}_i$ 共享一个全局时间步 $t^y$。

$$
t_i^x = \mathrm{clip}( \bar{t}^x + \delta_i, 0, 1 ), \quad \delta_i \sim \mathcal{N}(0, \sigma_t^2)
$$

通过在均值时间步 $\bar{t}^x$ 上叠加高斯扰动，确保训练阶段噪声水平均匀覆盖，避免贝茨分布坍缩。这一机制是后续渐进采样策略的基础——它使模型学会在任意噪声水平下重建运动，从而支持推理时对不同帧施加不同去噪步数的灵活调度。

### 3. 两阶段渐进采样：重叠窗口渐进去噪

推理时，ActionPlan 采用**两阶段生成**策略：

- **第一阶段**：从纯噪声出发，生成完整动作计划序列。该阶段使模型在运动合成前“预览”全部语义结构。
- **第二阶段**：以动作计划为条件，采用**重叠窗口渐进去噪**生成运动。每个运动潜在在激活后经历 $K$ 步去噪，然后激活下一潜在，形成滑动窗口式调度。离线模式使用随机顺序（random pyramid）激活，流式模式使用光栅顺序（raster）逐帧激活。

这一策略的关键优势在于：重叠窗口（$K=2$）使相邻帧共享部分去噪步骤，既保持帧间连贯性，又避免完全并行带来的语义混乱或完全串行带来的效率损失。消融实验（Table 3）证实，$K=2$ 在 FID（5.522）和 R-Precision@3（0.892）之间取得最佳平衡，优于完全并行（FID 5.420）和完全串行（FID 5.566）。

### 4. 掩码损失：突破标注数据瓶颈

逐帧动作计划的训练需要帧级文本标注，但此类数据稀缺（仅 BABEL 数据集提供，且与 HumanML3D 重叠约 30%）。ActionPlan 提出**掩码文本损失**（masked text loss），使模型可在完整 HumanML3D-272 数据集上训练：

$$
\mathcal{L}_{\mathrm{text}} = w \left\| \hat{\mathbf{y}}_v - ( \mathbf{y}_0 - \boldsymbol{\epsilon} ) \right\|_2^2
$$

其中指示变量 $w$ 在存在帧级标注时为 1，否则为 0，动态忽略缺失标注的帧。这一设计使模型在 100% 数据上学习运动重建，同时在约 30% 数据上学习帧级语义对齐。消融实验（Table 2）表明，使用完整数据集训练（E）相比仅使用重叠子集（B），离线 FID 降低 2.341，流式 FID 降低 2.14，验证了掩码损失对数据效率的关键提升。

### 与基线方法的系统性差异

| 设计维度 | 基线方法 | ActionPlan |
|---------|---------|------------|
| **语义条件** | 全局文本描述（MDM, MLD, MARDM） | 逐帧 CLIP 文本潜在（动作计划） |
| **时间步分配** | 单一全局时间步 | 每帧独立时间步 + 动作计划全局时间步 |
| **采样策略** | 完全并行（离线）或严格自回归（流式） | 两阶段生成 + 重叠窗口渐进去噪 |
| **训练数据** | 仅使用重叠子集（MotionStreamer） | 全量 HumanML3D-272 + 掩码损失 |
| **模式切换** | 离线/流式需分别训练或微调 | 同一 checkpoint 仅切换采样策略 |

这些创新使 ActionPlan 在流式模式下 FID 达 5.735，相较最佳流式基线 MotionStreamer（FID 11.790）改善 51%，同时首 token 延迟仅 146 ms，持续生成每 token 40 ms，在质量与效率之间取得了突破性平衡。



ActionPlan 是一个**两阶段、未来感知的流式运动合成框架**，其核心设计理念是将高层动作规划与低层运动生成解耦，从而在单一模型中同时实现离线高质量生成与在线低延迟流式输出。

### 总体流程

框架的运作分为两个阶段：

1. **动作计划生成（Stage 1）**：给定全局文本描述，模型首先生成一组与运动帧严格对齐的**逐帧动作计划潜在向量**。这些向量是 CLIP 文本空间中的 16 维潜在表示，作为密集语义锚点，使模型在运动合成之前即“预见”完整的动作序列。
2. **运动合成（Stage 2）**：以第一阶段生成的动作计划为条件，模型采用**重叠窗口渐进去噪**策略生成运动潜在序列，最终通过因果时序自编码器解码为 272 维 SMPL 姿态序列。

两阶段共用同一个 Transformer 去噪器，仅在推理时切换采样策略，无需重新训练或微调即可支持离线与流式两种模式（见 Table 2 E）。

### 模块架构与数据流

整个框架由以下核心模块构成：

| 模块 | 功能 | 输入 | 输出 |
|------|------|------|------|
| **因果时序自编码器 (Causal TAE)** | 将原始运动序列压缩至因果连续潜在空间，仅依赖过去帧，支持在线解码 | 272 维姿态序列 $m$ | 运动潜在 $\mathbf{x}$ |
| **动作自编码器 (Action AE)** | 将逐帧文本标注映射至 16 维 CLIP 潜在空间，并沿时间轴 4× 下采样以与运动潜在对齐 | 逐帧文本标注 | 动作计划潜在 $\mathbf{y}$ |
| **Transformer 去噪器** | 接收拼接的运动-文本潜在向量及各自时间步，预测速度场以完成联合去噪 | $\{(\mathbf{x}_i, \mathbf{y}_i)\}$、时间步 $\mathbf{t}^x, t^y$、全局文本条件 $c$ | 预测速度场 $(\hat{\mathbf{x}}_v, \hat{\mathbf{y}}_v)$ |
| **异构噪声调度器** | 训练时为每个运动潜在独立采样时间步，动作计划潜在共享单一全局时间步 | — | 异构时间步 $\mathbf{t}^x, t^y$ |
| **渐进采样器** | 推理时管理活跃潜在集，按任务模式（离线/流式/编辑/插帧）激活并渐进去噪 | 噪声潜在、动作计划、模式选择 | 去噪后的运动潜在序列 |

### 训练时的异构加噪机制

训练阶段的关键创新在于**异构扩散时间步**（Fig. 3a）：

- 每个运动潜在 $\mathbf{x}_i$ 被分配一个独立的时间步 $t_i^x$，通过先采样均值时间步再加高斯扰动的方式确保训练时噪声阶段均匀分布：
  $$t_i^x = \mathrm{clip}( \bar{t}^x + \delta_i, 0, 1 ), \quad \delta_i \sim \mathcal{N}(0, \sigma_t^2)$$
- 所有动作计划潜在 $\mathbf{y}_i$ 共享一个全局时间步 $t^y$，因为动作计划的语义信息需要全局一致性。

这种设计使模型学会在任意噪声组合下进行去噪，为推理时的灵活采样调度奠定基础。

### 推理时的双模式采样

推理时，渐进采样器根据任务需求切换两种模式（Fig. 3b-c）：

- **离线模式**：首先生成完整动作计划，然后以随机顺序（random pyramid order）对运动潜在进行重叠窗口去噪，保证全局上下文感知。
- **流式模式**：动作计划与第一帧运动潜在并行去噪，随后以光栅顺序（raster order）逐帧激活并去噪后续潜在，实现低延迟在线输出。首 token 延迟 146 ms，后续 token 仅 40 ms。

两种模式共享同一模型权重，仅在采样调度上存在差异，这从根本上打破了离线高质量与在线低延迟之间的传统割裂。

### 补充图表

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2603_13500/figures/003_Figure_3.jpg]]
*Figure 3: Overview of our ActionPlan. (a) During training, motion latents are noised with per-frame heterogeneous timesteps while frame-level text latents share a single global timestep. A Transformer Denoiser is trained to jointly reconstruct both. During inference, the model operates in two modes: in offline mode (b), the action plan is fully generated first and then motion latents are denoised in random pyramid order; in streaming mode (c), the action plan is denoised alongside the first motion frame, followed by raster progressive denoising of the remaining latents*



### 3.1 因果时序自编码器（Causal TAE）

ActionPlan 采用因果时序自编码器将原始运动序列压缩至连续潜在空间。该模块基于 1D 因果卷积构建，编码时仅依赖过去帧信息，从而天然支持在线解码。输入为 272 维 SMPL 6D 旋转姿态表示：

$$m = \{ \dot{r}^x, \dot{r}^z, \dot{r}^a, \dot{\jmath}^p, \dot{\jmath}^v, \dot{\jmath}^r \}$$

其中 $\dot{r}^x, \dot{r}^z$ 为根节点平面速度，$\dot{r}^a$ 为根节点角速度，$\dot{\jmath}^p, \dot{\jmath}^v, \dot{\jmath}^r$ 分别为关节位置、速度和旋转。编码器将长度为 $T$ 的原始运动序列下采样 4 倍，得到 $N = T/4$ 个运动潜在向量 $\mathbf{x} = \{x_i\}_{i=1}^N$。

### 3.2 动作计划生成器

动作计划是 ActionPlan 的核心创新。该模块从 BABEL 数据集的逐帧文本标注中学习，将每帧对应的 CLIP 文本嵌入经动作自编码器压缩为 16 维潜在向量 $\mathbf{y} = \{y_i\}_{i=1}^N$。动作自编码器的训练损失由三项组成：

**重建损失**（CLIP 空间 MSE）：
$$\mathcal{L}_{\mathrm{recon}} = \| \hat{e} - e \|_2^2$$

**近邻保持损失**（基于余弦相似度的动作标签检索交叉熵）：
$$\mathcal{L}_{\mathrm{neighbor}} = -\log \frac{\exp(s_y/\tau)}{\sum_{j=1}^{K} \exp(s_j/\tau)}$$

**方差正则化**（防止维度坍缩，鼓励每个潜在维度维持单位方差）：
$$\mathcal{L}_{\mathrm{var}} = \sum_{j=1}^{16} \left( \mathrm{Var}(z_j) - 1 \right)^2$$

文本潜在与运动潜在在时间轴上对齐（下采样因子同为 4），并在每帧拼接为联合向量 $(x_i, y_i)$，作为后续 Transformer 去噪器的输入。

### 3.3 Transformer 去噪器与异构噪声调度

去噪器 $G_\theta$ 是一个 Transformer 网络，接收拼接的噪声运动-文本潜在序列及各自的时间步，预测流匹配框架下的速度场：

$$\left( \hat{\mathbf{x}}_v, \hat{\mathbf{y}}_v \right) = G_\theta ( \mathbf{x}_{\mathbf{t}^x}, \mathbf{y}_{t^y}; \mathbf{t}^x, t^y, c )$$

其中 $\mathbf{t}^x = \{t_i^x\}_{i=1}^N$ 为每个运动潜在独立的噪声时间步，$t^y$ 为所有文本潜在共享的单一全局时间步，$c$ 为全局文本 CLIP 嵌入。

**异构时间步采样**是训练的关键设计。为避免所有运动帧共享同一时间步导致的训练-推理分布偏移，对每个运动潜在独立采样时间步，并通过高斯扰动保证噪声阶段均匀覆盖：

$$t_i^x = \mathrm{clip}( \bar{t}^x + \delta_i, 0, 1 ), \quad \delta_i \sim \mathcal{N}(0, \sigma_t^2)$$

其中 $\bar{t}^x \sim \mathcal{U}(0,1)$ 为均值时间步，$\delta_i$ 为逐帧高斯扰动。此设计避免了贝茨分布坍缩问题。

**掩码文本损失**使模型能利用全部 HumanML3D-272 数据训练，即使大部分样本缺少帧级文本标注：

$$\mathcal{L}_{\mathrm{text}} = w \left\| \hat{\mathbf{y}}_v - ( \mathbf{y}_0 - \boldsymbol{\epsilon} ) \right\|_2^2$$

其中 $w \in \{0, 1\}$ 为指示变量：当帧级标注存在时 $w=1$，否则 $w=0$，动态屏蔽无标注帧的文本损失。

总训练损失为运动重建与文本预测的加权和：

$$\mathcal{L} = \lambda_x \mathcal{L}_{\mathrm{motion}} + \lambda_y \mathcal{L}_{\mathrm{text}}$$

### 3.4 渐进采样器

推理时，渐进采样器管理活跃潜在集，按任务模式激活并渐进去噪。核心机制是**重叠窗口渐进去噪**：每步仅对当前活跃窗口内的潜在向量执行去噪，窗口大小 $K$ 控制相邻激活帧之间的去噪步数重叠。离线模式采用随机金字塔顺序激活，流式模式采用光栅顺序（从左至右逐帧激活）。流式模式下，动作计划与首帧运动潜在同步去噪，随后逐帧推进，总步数仅需 $N + T - 1$（$N$ 为运动帧数，$T$ 为流匹配总步数），实现低延迟在线生成。



## 实验与关键发现

### 核心定量结果

ActionPlan 在 HumanML3D-272 测试集上同时评估了离线（offline）和流式（streaming）两种推理模式，结果汇总于 **Table 1**。在离线模式下，ActionPlan 取得 FID **5.522**、R-Precision@3 **0.892**，相比此前最优离线方法 MARDM（FID 7.044，R-Precision@3 0.860）分别改善约 22% 和 3.2%。在流式模式下，ActionPlan 的 FID 为 **5.735**，不仅优于离线基线 MARDM 达 18%，更大幅领先现有流式方法 MotionStreamer（FID 11.790）达 51%。值得注意的是，R-Precision@3 在从离线切换至流式时仅下降 0.015（0.892 → 0.877），说明动作计划提供的未来感知语义锚点有效抑制了流式生成中常见的语义漂移。所有对比方法均在相同的 272 维 SMPL 6D 旋转表示和 TMR-based evaluator 上重训与评估，保证指标可比性。

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2603_13500/figures/005_Table_1.jpg]]
*Table 1: Quantitative comparison with SOTA T2M generation methods on HumanML3D-272 [21, 60] test set. MatchS and Div denote the matching score and diversity respectively. Bold indicates best results, underline indicates second best. ActionPlan achieves better performance in both offline and online-streaming mode, maintaining both efficiency and high quality motion generation*

### 推理效率

在 NVIDIA A100 GPU 上的延迟测量显示，ActionPlan 的流式模式首 token 延迟为 **146 ms**，后续每个 token 仅需 **40 ms**。相比之下，MARDM 每 token 固定 210 ms，MotionStreamer 每 token 固定 360 ms。这意味着 ActionPlan 在首 token 上加速 1.44×–2.47×，在持续流式生成中加速 5.25×–9×。首 token 的额外开销源于动作计划的生成需与第一个运动潜在同步去噪，但后续帧仅需渐进去噪新激活的潜在，因此吞吐量大幅提升。

### 消融实验

**Table 2** 系统消融了三个关键设计选择：训练数据范围、帧级文本预测、以及动作计划的两阶段生成。

- **训练数据范围（A–B vs C–E）**：仅使用 BABEL 与 HumanML3D 重叠子集（约 30% 数据）训练时，离线 FID 为 8.219（B），而利用完整 HumanML3D-272 数据集配合掩码损失训练（E）将 FID 降至 5.522，降幅达 2.697。这验证了 masked loss（式 3）能有效利用缺乏逐帧标注的大规模数据。
- **帧级文本预测（C vs D）**：即使不采用两阶段动作计划，仅将逐帧文本预测作为联合生成的一部分（D），相比完全不预测帧级文本（C）仍使离线 FID 改善 0.859（6.449 → 5.590），表明细粒度语义对齐本身即有益于运动质量。
- **动作计划两阶段生成（D vs E）**：将帧级文本预测升级为独立的动作计划生成阶段（E），在离线模式下 FID 进一步从 5.590 降至 5.522，流式模式下从 6.018 降至 5.878。R-Precision@3 也同步提升（离线 0.879 → 0.892，流式 0.854 → 0.875），证明先“预见”完整动作序列再合成运动的两阶段范式是打通离线高质量与在线低延迟的关键。

**Table 3** 消融了渐进采样策略中连续激活运动潜在之间的重叠程度。在固定总计 25 步去噪的约束下，完全并行激活（FID 5.420，R-Precision@3 0.887）与完全串行无重叠去噪（FID 5.566，R-Precision@3 0.887）分别处于两个极端。所选窗口大小 **K=2**（每个潜在去噪 2 步后激活下一个）在 FID（5.522）和 R-Precision@3（0.892）之间取得最佳平衡，验证了适度重叠既能保持帧间一致性，又不牺牲文本-运动对齐精度。

### 定性分析

**Fig. 4** 展示了四个复杂文本提示下的定性对比。提示包含多动作序列（如“一个人先向前走，然后转身，再蹲下”），ActionPlan 正确执行了所有指定动作且顺序无误，而 MARDM 和 MotionStreamer 频繁遗漏或错序关键动作（图中以 × 标记）。这直观印证了动作计划作为密集语义锚点的作用：模型在合成运动前已“知道”完整动作序列，从而避免了流式因果模型因缺乏未来上下文而导致的动作遗漏。

### 用户研究

用户研究分为两个任务：文本到运动（T2M）生成和长序列流式生成。在 T2M 任务中，参与者对三个方法生成的动画进行偏好选择，ActionPlan 获得 **67.5%** 的偏好率。在长序列流式任务中，参与者比较两个方法从相同文本提示序列生成的动画，ActionPlan 获得 **67.7%** 的偏好率。两项任务均显著优于对比方法，表明动作计划带来的语义忠实性和运动连贯性在主观感知层面同样显著。

### 失败模式与局限

尽管 ActionPlan 在定量和定性评估中均表现优异，仍存在以下局限：

1. **细粒度运动缺失**：当前动作表示仅覆盖身体关节，未包含手指关节和面部表情，因此无法生成手部精细动作或面部动画。
2. **标注数据依赖**：动作计划生成依赖于 BABEL 数据集的帧级文本标注，尚未探索仅利用全局文本描述的自监督或弱监督训练方式，限制了向无标注数据集的扩展。
3. **场景交互缺失**：模型未建模场景几何或物体信息，无法生成与环境和物体交互的动作（如“拿起桌上的杯子”），这需要额外的场景感知模块。
4. **首 token 延迟**：流式模式首 token 延迟 146 ms，虽已显著优于对比方法，但对于部分要求端到端延迟低于 100 ms 的高实时性应用（如游戏引擎中的实时角色控制）仍存瓶颈。

### 补充图表

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2603_13500/figures/001_Figure_1.jpg]]
*Figure 1: ActionPlan decouples high-level action planning from low-level motion generation in a single generative model (a). By conditioning motion synthesis on generated action plans, ActionPlan achieves online generation (b) without the typical accuracy drop that happens in existing streaming methods and supports localized edits (c)*

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2603_13500/figures/006_Table.jpg]]

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2603_13500/figures/007_Table_2.jpg]]
*Table 2: Ablation studies for both Offline and Streaming modes. Training on the full dataset (C–E) consistently outperforms the partial intersection subset (A–B), validating our masked loss design. Frame-level text prediction (D, E) improves over no frame text (C). Action plan generation (E) further outperforms joint co-generation (D). These gains hold across both inference modes. Bold: best, underline: second best*

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2603_13500/figures/008_Table_3.jpg]]
*Table 3: Ablation on sampling strategy. All rows use the same trained model with a fixed total of 25 denoising steps, differing only in the overlap between consecutively activated motion latents, ranging from fully parallel activation to fully sequential (nonoverlapping) denoising. Our chosen schedule denoises each activated latent for 2 steps before activating the next, achieving the best trade-off between motion quality (FID) and text-motion alignment (R-Precision)*



## 定位与知识库关联

### 1. 与离线运动合成方法的对比与继承

ActionPlan 继承了离线扩散式运动合成的基本范式，但与现有离线方法存在根本性差异。离线扩散模型如 **MDM** (Tevet et al., NeurIPS 2023) 和 **MLD** (Chen et al., AAAI 2024) 采用全并行去噪策略，所有运动帧共享单一扩散时间步，以全局文本描述为条件一次生成完整序列。这类方法虽然质量较高，但缺乏帧级语义约束，在复杂多动作指令下容易遗漏或错序关键动作。离散 VAE 路线的方法如 **T2M-GPT** (Zhang et al., CVPR 2023)、**MotionGPT** (Zhang et al., 2024) 和 **MoMask** (Guo et al., 2024) 通过自回归或掩码建模生成离散运动 token，同样受限于全局条件，无法细粒度控制每帧语义。

ActionPlan 的核心突破在于将高层动作规划与低层运动合成解耦：首先生成与运动帧严格对齐的逐帧 CLIP 文本潜在向量作为动作计划，再以动作计划为条件进行运动去噪。这一两阶段范式使模型在生成运动之前先“预见”完整的动作序列，从而为每帧提供密集语义锚点。消融实验（Table 2 E vs D）表明，引入动作计划后，离线模式 FID 从 6.093 降至 5.522，R-Precision@3 从 0.877 升至 0.892，验证了这种解耦设计的有效性。

### 2. 与流式运动合成方法的对比

现有流式方法如 **MotionStreamer** (Xiao et al., arXiv 2025) 和 **MARDM** (Mu et al., ICLR 2025) 分别采用因果扩散和掩码自回归连续潜在扩散实现逐帧或逐块输出。然而，这些方法因缺乏未来上下文，普遍存在语义漂移和动作遗漏问题：MotionStreamer 的流式 FID 高达 11.790，MARDM 在定性对比中频繁遗漏关键动作（Fig. 4）。

ActionPlan 通过动作计划机制从根本上解决了这一瓶颈。动作计划在流式模式中与第一帧运动潜在同时去噪，为后续所有帧提供完整的未来语义信息。即使采用因果时序自编码器（Causal TAE）确保每帧仅依赖过去运动信息，动作计划的存在使模型在生成当前帧时已“知晓”未来将发生的动作。定量结果验证了这一设计的有效性：ActionPlan 流式 FID 为 5.735，较 MotionStreamer 降低 51%（Table 1）。定性对比中，ActionPlan 在四个复杂文本提示上正确执行了所有指定动作，而 MARDM 和 MotionStreamer 频繁遗漏或错序关键动作（Fig. 4）。

### 3. 关键设计选择与消融证据

**异构扩散时间步**。ActionPlan 为每个运动潜在分配独立时间步，动作计划潜在则共享全局时间步。训练时通过均值扰动（$\delta_i \sim \mathcal{N}(0, \sigma_t^2)$）避免贝茨分布坍缩，确保噪声阶段均匀覆盖。这一设计使模型能灵活处理不同帧处于不同去噪阶段的情况，是实现渐进采样的前提。

**渐进采样窗口**。推理时采用重叠窗口渐进去噪：窗口大小 K=2（每个潜在去噪 2 步后激活下一个）在 FID（5.522）和 R-Precision@3（0.892）之间达到最佳平衡（Table 3）。完全并行（K=25）FID 略优但 R-Precision 下降，完全串行（K=1）则 FID 显著恶化至 5.566。这表明适度的重叠去噪能在保持帧间一致性的同时维持语义对齐精度。

**Masked Loss 与数据利用**。BABEL 数据集提供帧级文本标注，但与 HumanML3D 的重叠子集仅占约 30%。ActionPlan 通过掩码损失（式 3）动态忽略缺失的帧级标注，从而利用全部 HumanML3D-272 数据训练。消融实验（Table 2 E vs B）表明，在完整数据集上训练使离线 FID 降低 2.341，流式 FID 降低 2.14，验证了 masked loss 设计的必要性。

### 4. 适用边界与能力范围

**已验证的能力边界**：
- **离线高质量生成**：FID 5.522，R-Precision@3 0.892，全面超越现有离线方法。
- **流式低延迟生成**：首 token 146 ms，后续 token 40 ms，持续生成速度较 MARDM 快 5.25 倍，较 MotionStreamer 快 9 倍。
- **零样本局部编辑**：可重新生成选定帧的运动潜在，以新提示为条件，同时保留其他帧不变（Fig. 5 top）。
- **长序列流式生成**：支持跨提示的连续长时域运动生成（Fig. 5 middle）。
- **插帧**：给定固定起始和结束姿态，填充中间运动（Fig. 5 bottom）。
- **用户偏好**：在文本到运动任务获得 67.5% 偏好，在长序列流式任务获得 67.7% 偏好（Section 4.4）。

**未覆盖的能力与局限**：
- 目前仅考虑人体动作，未包含手指关节和面部表情的精细运动。
- 动作计划生成依赖于成对标注数据（BABEL），未探索仅靠全局文本的自监督训练方式。
- 尚不能与场景和物体交互，缺乏对环境上下文的理解。
- 推理时首 token 开销（146 ms）仍可能影响部分高实时性（<100 ms）应用场景。

### 5. 开放问题

1. **精细运动扩展**：如何将手指关节和面部表情纳入层级规划框架？这可能需要更高维度的动作计划表示，或引入多尺度计划结构。

2. **场景与物体交互**：如何在保持动作计划未来感知优势的同时，加入场景/物体感知能力？可能的路径是将环境上下文作为额外条件注入去噪器，或扩展动作计划以包含交互语义。

3. **弱监督动作计划学习**：当前动作计划依赖 BABEL 的帧级标注，能否通过弱监督或自监督方式自动获取帧级语义锚点？例如利用视频文本对齐模型或运动-语言对比学习自动挖掘帧级对应关系。

4. **首 token 延迟优化**：首 token 146 ms 的开销主要来自动作计划的完整生成。能否通过动作计划的渐进式生成或预测性初始化进一步降低这一延迟，使系统适用于更严格的实时场景？



## 原文 PDF

![[paperPDFs/CVPR_2026/ActionPlan_Future_Aware_Streaming_Motion_Synthesis_via_Frame_Level_Action_Planning.pdf]]
