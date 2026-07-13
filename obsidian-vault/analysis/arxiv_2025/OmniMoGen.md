---
title: OmniMoGen
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: paperPDFs/arxiv_2025/OmniMoGen.pdf
project_link: https://OmniMoGen.github.io/
code_link: null
aliases:
- OmniMoGen
tags:
- arxiv_2025
- topic/motion_animation
- topic/motion_animation/human_motion_generation
- topic/generative_models_diffusion
core_operator: 将多样化的动作生成任务统一表示为交叉文本-动作指令，并采用基于残差向量量化变分自编码器 (RVQ-VAE) 的离散 token 化与统一自回归 transformer 进行端到端的学习。
primary_logic: 借鉴大语言模型统一自然语言处理任务的范式，通过构建大规模多任务交叉指令数据集 (X2Mo) 和两阶段训练 (多任务监督微调 SFT + 基于 GRPO 的强化学习 RL)，单一模型可以在不添加任何额外模块的情况下实现从文本到动作生成、风格/轨迹编辑、内插、外插、组合编辑等全能动作生成，并涌现出自我反思等新能力。
claims:
- OmniMoGen 在 HumanML3D 文本到动作基准上超越所有多任务基线，R@1 相对次优方法提升 1.3%。
- 在 MotionFix 运动编辑基准上，OmniMoGen 的 Edited-to-Target R@1 达到最优，比先前最佳方法提高 1.4%。
- 在 AnyContext 交叉指令基准上，现有方法 R@1 普遍低于 30%、物理指标低于 0.91，而 OmniMoGen 达到 37.5 的 R@1 且物理指标 0.95，显著领先，验证了统一架构高效处理交叉指令的能力。
- 消融实验证实移除监督微调 (SFT) 阶段导致 MotionFix R@1 从 68.33 骤降至 42.09，AnyContext R@1 从 36.7 降至 19.3；移除 GRPO RL 阶段使物理指标从 0.95 降至 0.91。
---

# OmniMoGen

> [!tip] 核心洞察
> 借鉴大语言模型统一自然语言处理任务的范式，通过构建大规模多任务交叉指令数据集 (X2Mo) 和两阶段训练 (多任务监督微调 SFT + 基于 GRPO 的强化学习 RL)，单一模型可以在不添加任何额外模块的情况下实现从文本到动作生成、风格/轨迹编辑、内插、外插、组合编辑等全能动作生成，并涌现出自我反思等新能力。

| 字段 | 内容 |
|------|------|
| 中文题名 | OmniMoGen：通过交叉文本-动作指令学习统一人体动作生成 |
| 英文题名 | OmniMoGen |
| 会议/期刊 | arXiv 2025 |
| Links | [paper](https://arxiv.org/abs/2509.21582) · [Project](https://OmniMoGen.github.io/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | OmniMoGen |
| Dataset | HumanML3D, MotionFix, AnyContext |

> [!tip] 效果简介
> - HumanML3D (Text-to-Motion) 上，R@1 (Top-1 RPrecision) 0.550 (OmniMoGen-Think) vs 0.543 (MotionGPT3, second-best multi-task) (+1.3% (relative improvement))；FID 0.061 (OmniMoGen-Think) vs 0.217 (MotionGPT3, second-best multi-task) (-0.156)。
> - MotionFix (Motion Editing) 上，Edited-to-Target R@1 81.28 (OmniMoGen) vs 79.78 (MotionGPT, previous best) (+1.5% (absolute))。
> - AnyContext (Style-based) 上，R@1 42.9 (OmniMoGen-Think) vs Below 30 (best existing baseline) (>12.9 (significant improvement))。

## 概要

现有的人体动作生成方法将文本到动作、运动编辑、动作内插等任务视为独立问题，各自依赖任务特定的架构与输入格式，无法遵循自由形式的交叉文本‑动作指令。这种碎片化范式限制了模型在多任务场景下的泛化能力与统一性。**OmniMoGen** 借鉴大语言模型统一自然语言处理任务的思想，提出将多样化的动作生成任务统一表示为交叉文本‑动作指令序列，并采用基于残差向量量化变分自编码器（RVQ‑VAE）的离散 token 化与统一自回归 transformer 进行端到端学习，从而在单一模型中实现文本到动作生成、风格/轨迹编辑、内插、外插、组合编辑乃至自我反思等全能动作生成能力。

方法的核心机制可概括为三个关键环节。首先，所有任务均通过统一的交叉文本‑动作指令序列表示，指令中包含自然语言描述、`<Motion>` 标记和动作 token，使单模型能够解析任意类型的指令，无需为不同任务设计异构输入格式。其次，模型架构由 RVQ‑VAE 运动 tokenizer 与自回归 transformer 组成：RVQ‑VAE 将连续动作序列压缩为多层残差离散 token，transformer 则对交叉排列的文本与动作 token 进行自回归建模，所有任务共享同一骨干网络，不引入任何额外模块。第三，训练采用两阶段策略——第一阶段在构建的大规模多任务交叉指令数据集 **X2Mo**（137K 条指令）上进行监督微调（SFT），使模型学会遵循交叉指令；第二阶段采用基于 GRPO 的强化学习，同时优化语义正确性奖励（对比检索相似度）与物理合理性奖励（足部滑步惩罚），进一步提升生成质量与物理逼真度。

实验结果显示，OmniMoGen 在多个基准上均取得领先性能，验证了统一架构的高效性。在 **HumanML3D** 文本到动作基准上，OmniMoGen‑Think 的 R@1 达到 0.550，相对次优多任务方法提升 1.3%，FID 降至 0.061（Table 1）。在 **MotionFix** 运动编辑基准上，Edited‑to‑Target R@1 达到 81.28，比先前最佳方法提高 1.4 个百分点（Table 2）。在专门设计的 **AnyContext** 交叉指令基准上，现有方法的 R@1 普遍低于 30%、物理指标低于 0.91，而 OmniMoGen‑Think 的 R@1 达到 37.5、物理指标达到 0.97，显著领先（Table 3）。消融实验进一步证实，移除 SFT 阶段会使 MotionFix R@1 从 68.33 骤降至 42.09，移除 GRPO RL 阶段则使物理指标从 0.95 降至 0.91，表明多任务指令微调与强化学习两者缺一不可（Table 4）。

在方法谱系中，OmniMoGen 区别于以 **T2M‑GPT**、**MoMask** 为代表的纯文本到动作自回归/掩码模型，也不同于 **MotionGPT3** 等混合多任务基线或 **MotionReFit**、**SALAD** 等扩散式方法。其核心革新在于将“任务统一”从模型架构层面推进到输入表示与训练范式层面，并通过 GRPO 强化学习引入生成质量反馈，使单一模型能够涌现出自我反思等新能力。当前局限在于反思轮次超过 4 轮后性能下降，归因于 transformer 的有效上下文窗口限制，这为后续扩展长序列动作生成与交互式编辑指明了方向。

人体动作生成是计算机视觉与图形学中的核心问题，其目标是根据给定的控制信号（如文本描述、动作片段、编辑指令等）合成自然、逼真的人体运动序列。该任务在人机交互、虚拟现实、影视动画和游戏开发中具有广泛的应用前景。

近年来，随着深度学习和大规模运动捕捉数据的发展，人体动作生成取得了显著进展。然而，现有方法普遍存在一个根本性的瓶颈：**将不同的动作生成任务视为彼此独立的问题**。文本到动作生成、运动编辑、动作内插/外插、风格迁移等任务通常依赖各自特定的模型架构、输入格式和训练范式。例如，基于掩码 transformer 的方法（如 MoMask）需要预定义掩码位置来限制任务范围，扩散模型（如 MotionReFit、MLD）则使用特定的条件信号注入机制，不同任务之间无法共享输入表示或模型参数。这种“一任务一模型”的碎片化范式严重限制了动作生成系统的通用性和灵活性，使得单一模型难以遵循自由形式的交叉文本-动作指令来完成多样化的生成目标。

借鉴大语言模型（LLM）在自然语言处理领域统一各类任务的范式，一个自然的思路浮现出来：**能否将多样化的动作生成任务统一表示为交叉文本-动作指令，并用单一模型进行端到端学习？** 这一思路面临两个核心挑战。其一，需要一种统一的表示格式，能够将文本描述、源动作片段、编辑需求等信息自然地交织在一起，形成模型可解析的指令序列。其二，需要构建大规模、多任务的交叉指令数据集来支撑统一模型的训练，而现有数据集普遍只覆盖单一任务类型。

OmniMoGen 正是在这一动机下提出的。其核心洞察在于：通过构建大规模多任务交叉指令数据集 X2Mo（包含 137K 条交叉文本-动作指令），并采用两阶段训练策略（多任务监督微调 SFT + 基于 GRPO 的强化学习 RL），单一模型可以在不添加任何额外模块的情况下，实现从文本到动作生成、风格/轨迹编辑、内插、外插、组合编辑等全能动作生成，甚至涌现出自我反思等新能力。这一思路将人体动作生成从“多模型协作”推向“单模型统一”，为构建通用动作生成基础模型提供了可行的技术路径。

## 核心方法与创新机理

OmniMoGen 的核心创新在于将人体动作生成从“多任务异构”范式彻底转变为“单模型统一”范式。其关键突破体现在三个相互耦合的维度：任务表示的统一、模型架构的统一，以及训练策略的统一。

### 1. 统一的任务表示：交叉文本-动作指令

现有方法将文本到动作生成、运动编辑、内插等任务视为独立问题，依赖任务特定的输入格式（例如，编辑任务需要显式指定源动作和编辑区域），不同任务之间无法共享输入表示。OmniMoGen 打破了这一壁垒，将所有任务统一表示为**交叉文本-动作指令序列**。该序列由自然语言描述、`<Motion>` 标记和离散动作 token 交替排列构成，单一模型可解析任意指令格式（§3.1.1；Figure 2(b)）。

具体而言，论文构建了四类交叉指令模板：**上下文生成**（给定参考动作和文本描述生成新动作）、**运动编辑**（基于文本指令修改源动作）、**多轮编辑**（连续多次编辑同一动作）、以及**反思**（模型自我评估并改进生成结果）。这种统一表示使得模型能够以类似 ChatGPT 处理自然语言的方式，灵活处理多样化的动作生成需求，而无需为每个任务设计专用的输入接口。

### 2. 统一的模型架构：RVQ-VAE + 自回归 Transformer

基线方法通常依赖任务特定的异构模块：掩码 transformer 使用预定义掩码位置限制任务范围，扩散模型使用特定条件信号，不同任务往往需要不同的网络结构。OmniMoGen 采用**单一的自回归 Transformer 骨干网络**，所有任务共享同一架构，无需任何额外模块（§3.2.1；Figure 2）。

该架构由两个核心组件构成：

- **RVQ-VAE 运动 Tokenizer**：将连续人体动作序列编码为离散 token 序列。它包含 6 层残差码本，每层 512 个码向量（维度 512），通过残差量化方式逐步细化潜在表示，以提升重建保真度。其残差量化过程为：
  $$\hat{\mathbf{z}}_t = \sum_{l=1}^{L} q^{(l)}(\mathbf{r}_t^{(l-1)}), \quad \mathbf{r}_t^{(l)} = \mathbf{r}_t^{(l-1)} - q^{(l)}(\mathbf{r}_t^{(l-1)})$$

- **自回归 Transformer（Gemma2-2B）**：接收交叉排列的文本 token 和动作 token 序列，以标准语言建模方式预测下一个 token：
  $$\mathcal{L}_{\mathrm{LLM}} = \sum_{t} \log p_{\psi}(s_t \mid s_{<t})$$

这种“动作即外语”的设计理念，使得动作生成自然地融入大语言模型的序列建模框架，无需任何架构层面的任务适配。

### 3. 统一的训练策略：SFT + GRPO 强化学习

基线方法通常仅采用单一任务监督学习或针对特定任务的数据微调，缺少多任务联合训练和基于反馈的策略优化。OmniMoGen 引入**两阶段训练策略**（§3.2.2–§3.2.3）：

- **第一阶段：多任务监督微调（SFT）**。在包含 137K 条交叉指令的 X2Mo 数据集上进行指令微调，使基础模型具备遵循多样化交叉指令的能力。SFT 损失为标准负对数似然：
  $$\mathcal{L}_{\mathrm{SFT}} = - \sum_{t=1}^{T} \log p_{\theta}(x_t \mid x_{<t})$$

- **第二阶段：基于 GRPO 的强化学习（RL）**。为超越模仿学习的上限，采用 GRPO 算法同时优化两项奖励——**语义正确性奖励**（基于对比学习的检索相似度）和**物理合理性奖励**（基于足部滑步惩罚）：
  $$\mathcal{R} = \lambda_{\mathrm{sem}} \mathcal{R}_{\mathrm{sem}} + \lambda_{\mathrm{phy}} \mathcal{R}_{\mathrm{phy}}$$

  其中语义奖励通过 softmax 归一化的余弦相似度计算：
  $$\mathcal{R}_{\mathrm{sem}}^{(i)} = \frac{\exp\left(\operatorname{sim}\left(f_m(\hat{M}_i), f_t(T_i)\right) / \tau\right)}{\sum_{j=1}^{N} \exp\left(\operatorname{sim}\left(f_m(\hat{M}_i), f_t(T_j)\right) / \tau\right)}$$

  物理奖励在足部接触帧上约束脚的水平速度以减少滑步：
  $$\mathcal{R}_{\mathrm{phy}} = -\frac{1}{T} \sum_{t} \sum_{i \in \{\mathrm{LA, LT, RA, RT}\}} c_i^t \left\| \dot{p}_i^t(x,y) \right\|_2^2$$

消融实验证实了该两阶段策略的必要性：移除 SFT 阶段导致 MotionFix R@1 从 68.33 骤降至 42.09，AnyContext R@1 从 36.7 降至 19.3；移除 GRPO RL 阶段使物理指标从 0.95 降至 0.91（Table 4(B)）。移除语义奖励使 MotionFix R@1 降至 63.62，移除物理奖励使物理指标降至 0.92，验证了双奖励设计的必要性（Table 4(D)）。此外，使用 RVQ-VAE 作为 tokenizer 优于普通 VQ-VAE（R@1 68.33 vs 64.91），进一步确认了残差量化的贡献（Table 4(F)）。

### 4. 涌现能力：自我反思生成

作为统一框架的延伸，OmniMoGen 还涌现出**自我反思**能力（OmniMoGen-Think）。模型在生成动作后自动进行自我评估，并根据反思结果重新生成，支持多轮迭代改进（默认最多 3 轮）。实验表明，反思轮次从 0 增加到 3 持续提升检索性能和物理指标，但扩展到 5 轮后性能下降，揭示当前 Transformer 的有效上下文窗口成为长链反思的瓶颈（Figure 8；Appendix D.1）。

综上，OmniMoGen 通过“统一表示—统一架构—统一训练”的三位一体设计，实现了从文本到动作生成、风格/轨迹编辑、内插、外插、组合编辑到自我反思的全能动作生成，在无需任何额外模块的前提下，显著超越了所有多任务基线方法。

OmniMoGen 的整体框架遵循“离散 token 化 + 统一自回归建模”的设计范式，其核心思想借鉴了大语言模型统一自然语言处理任务的思路：将多样化的人体动作生成任务统一表示为**交叉文本-动作指令**，并通过单一的自回归 transformer 进行端到端的序列预测，无需为不同任务设计异构模块。

### 两阶段流水线

框架由两个紧密耦合的阶段构成：

1.  **RVQ-VAE 运动 Tokenizer**：将连续的 3D 人体动作序列压缩为离散 token 序列。该模块采用 6 层残差码本（每层 512 个码向量，维度 512），通过残差量化逐层细化潜在表示，在保持高重建保真度的同时将动作转化为类似“外语”的离散符号。
2.  **自回归 Transformer 骨干**：接收交叉排列的文本 token 与动作 token 序列，以自回归方式预测下一个 token。模型采用轻量级开源大语言模型 **Gemma2-2B** 作为骨干网络，所有任务共享同一 transformer，不引入任何额外模块。

### 数据流与指令格式

整个系统的数据流如下：

-   **输入**：用户提供的交叉文本-动作指令。指令中包含自然语言描述、`<Motion>` 标记以及动作 token，格式统一，可灵活组合以表示文本到动作生成、风格/轨迹编辑、内插、外插、组合编辑等多种任务。
-   **Token 化**：连续动作经 RVQ-VAE 编码为离散 token 后，与文本 token 拼接为交叉序列。
-   **自回归生成**：Transformer 逐 token 预测输出序列，其中动作部分随后由 RVQ-VAE 解码器重建为连续动作。
-   **输出**：符合指令语义与物理约束的 3D 人体动作序列。

### 训练策略

OmniMoGen 采用**两阶段训练**以赋予模型指令跟随能力并提升生成质量：

-   **阶段一：多任务监督微调 (SFT)**。在大规模交叉指令数据集 **X2Mo**（包含 137K 条指令，涵盖 in-context 生成、运动编辑、多轮编辑和反思四种任务类型）上进行指令微调，使基础模型学会解析并执行自由形式的交叉指令。
-   **阶段二：基于 GRPO 的强化学习 (RL)**。在 SFT 基础上，采用 GRPO 算法进行策略优化，奖励信号由两部分加权求和构成：**语义正确性奖励**（基于对比学习的检索相似度）和**物理合理性奖励**（基于足部滑步惩罚）。这一阶段显著提升了生成动作的语义对齐度和物理逼真度。

### 可选反思机制

框架还引入了 **OmniMoGen-Think** 变体：在生成动作后，模型自动进行自我评估与反思，并根据反思结果重新生成。默认支持最多 3 轮迭代改进，使模型涌现出自我纠错能力。实验表明，反思轮次从 0 增至 3 可持续提升检索准确率与物理指标，但扩展至 5 轮后性能下降，当前 transformer 的上下文窗口成为限制因素。

![[assets/figures/papers/2512.19159_42baaa9101bd/figures/001_Figure_1.jpg]]
*Figure 1: Similar to ChatGPT in NLP, OmniMoGen unifies all motion generation tasks in a unified architecture, such as text-to-motion, style editing, trajectory editing, inpainting, in-betweening, compositional editing, self-reflective generation, and knowledge-informed generation. OmniMoGen enables seamless and flexible motion generation across diverse objectives by merely adjusting the interleaved text-motion instructions*

OmniMoGen 的核心架构由两个关键模块组成：**RVQ-VAE 运动 Tokenizer** 和**统一自回归 Transformer**，辅以两阶段训练策略实现多任务指令跟随。

### RVQ-VAE 残差量化

连续人体动作序列通过残差向量量化变分自编码器（RVQ-VAE）被离散化为 token 序列。该 tokenizer 包含 6 层残差码本（每层 512 个码向量，维度 512），采用分层渐进的方式细化潜在表示。对于第 $t$ 帧的潜在特征 $\mathbf{z}_t$，残差量化过程为：

$$\hat{\mathbf{z}}_t = \sum_{l=1}^{L} q^{(l)}(\mathbf{r}_t^{(l-1)}), \quad \mathbf{r}_t^{(l)} = \mathbf{r}_t^{(l-1)} - q^{(l)}(\mathbf{r}_t^{(l-1)})$$

其中 $\mathbf{r}_t^{(0)} = \mathbf{z}_t$ 为初始残差，$q^{(l)}(\cdot)$ 表示第 $l$ 层码本的最近邻查找，$L=6$ 为总层数。每层量化上一层的残差，最终重建为各层量化结果之和。这种残差设计相比普通 VQ-VAE 显著提升了重建保真度——消融实验证实，使用 RVQ-VAE 替代普通 VQ-VAE 使 MotionFix 上的 Edited-to-Target R@1 从 64.91 提升至 68.33（Table 4(F)）。

### 自回归序列建模

动作 token 与文本 token 被拼接成交叉序列，送入基于 Gemma2-2B 的自回归 transformer 进行统一建模。模型以标准语言建模方式预测下一个 token，损失函数为：

$$\mathcal{L}_{\mathrm{LLM}} = \sum_{t} \log p_{\psi}(s_t \mid s_{<t})$$

其中 $s_t$ 为交叉序列中第 $t$ 个 token（可以是文本 token 或动作 token），$\psi$ 为模型参数。该统一范式无需任何任务特定模块，仅通过调整交叉文本-动作指令即可覆盖文本到动作生成、编辑、内插、外插等多种任务。

### 两阶段训练

**第一阶段：监督微调（SFT）。** 在包含 137K 条交叉指令的 X2Mo 数据集上进行多任务指令微调，损失函数为：

$$\mathcal{L}_{\mathrm{SFT}} = - \sum_{t=1}^{T} \log p_{\theta}(x_t \mid x_{<t})$$

其中 $x_t$ 为交叉文本-动作 token 序列中的第 $t$ 个 token。此阶段使基础模型获得遵循自由形式交叉指令的能力。消融实验表明，移除 SFT 阶段导致 MotionFix R@1 从 68.33 骤降至 42.09，AnyContext R@1 从 36.7 降至 19.3（Table 4(B)），验证了多任务指令微调是不可或缺的。

**第二阶段：GRPO 强化学习。** 在 SFT 基础上，采用 GRPO（Group Relative Policy Optimization）算法进一步优化生成质量。总奖励由语义正确性和物理合理性两项加权求和：

$$\mathcal{R} = \lambda_{\mathrm{sem}} \mathcal{R}_{\mathrm{sem}} + \lambda_{\mathrm{phy}} \mathcal{R}_{\mathrm{phy}}$$

**语义正确性奖励**基于对比检索设计，计算生成动作 $\hat{M}_i$ 与对应文本指令 $T_i$ 的余弦相似度，并通过 softmax 归一化：

$$\mathcal{R}_{\mathrm{sem}}^{(i)} = \frac{\exp\left(\operatorname{sim}\left(f_m(\hat{M}_i), f_t(T_i)\right) / \tau\right)}{\sum_{j=1}^{N} \exp\left(\operatorname{sim}\left(f_m(\hat{M}_i), f_t(T_j)\right) / \tau\right)}$$

其中 $f_m$ 和 $f_t$ 分别为 TMR 的动作编码器和文本编码器，$\tau$ 为温度参数，$N$ 为批次大小。

**物理合理性奖励**通过惩罚足部滑步来约束动作的物理可信度：

$$\mathcal{R}_{\mathrm{phy}} = -\frac{1}{T} \sum_{t} \sum_{i \in \{\mathrm{LA, LT, RA, RT}\}} c_i^t \left\| \dot{p}_i^t(x,y) \right\|_2^2$$

其中 $c_i^t$ 为足部 $i$ 在第 $t$ 帧的接触标志（接触地面时为 1），$\dot{p}_i^t(x,y)$ 为足部水平速度，LA/LT/RA/RT 分别表示左脚踝、左脚尖、右脚踝、右脚尖。该奖励在接触帧上约束脚的水平速度，有效减少滑步伪影。

GRPO 策略优化采用带裁剪的代理目标函数：

$$\mathcal{L}_{\mathrm{GRPO}} = \mathbb{E}_t \left[ \min \left( r_t(\theta) A_t, \operatorname{clip}(r_t(\theta), 1-\epsilon, 1+\epsilon) A_t \right) - \beta D_{\mathrm{KL}}[p_{\theta_{\mathrm{old}}} \parallel p_{\theta}] \right]$$

其中 $r_t(\theta)$ 为新旧策略概率比，$A_t$ 为优势函数，$\epsilon$ 为裁剪范围，$\beta D_{\mathrm{KL}}$ 为 KL 散度正则项，用于稳定策略更新。消融实验证实，移除 GRPO RL 阶段使 AnyContext 物理指标从 0.95 降至 0.91，AvgR 从 6.1 恶化到 8.0（Table 4(B)）；单独移除语义奖励使 MotionFix R@1 从 68.33 降至 63.62，移除物理奖励使物理指标从 0.95 降至 0.92（Table 4(D)），验证了双奖励设计的必要性。

### 物理接触评估指标

除训练中的物理奖励外，评估阶段使用物理接触得分衡量生成动作的合理性：

$$s_{\mathrm{contact}} = \exp \Big( - ( | z_{\min} | - \tau_h )^{+} \Big) \cdot \exp \Big( - ( \| v_{\min} \|_2 - \tau_v )^{+} \Big)$$

其中 $z_{\min}$ 为足部最小离地高度，$v_{\min}$ 为足部最小水平速度，阈值 $\tau_h = 0.05\mathrm{m}$、$\tau_v = 0.075\mathrm{m/s}$，$(\cdot)^{+}$ 表示 ReLU 操作。该指标同时惩罚脚部浮空和滑地现象。

![[assets/figures/papers/2512.19159_42baaa9101bd/figures/002_Figure_2.jpg]]
*Figure 2: An overview of OmniMoGen, comprising (a) an RVQ-VAE and (b) an autoregressive transformer. Motions are encoded into discrete tokens like a foreign language by the RVQ-VAE, and then concatenated with text tokens as input to a unified autoregressive transformer for next-token prediction*

## 实验与关键发现

### 核心实验设计

OmniMoGen 在三个互补基准上进行了系统评估：**HumanML3D**（文本到动作生成）、**MotionFix**（运动编辑）和 **AnyContext**（交叉文本-动作指令生成）。这一设计覆盖了从单一任务到复杂组合指令的完整能力谱系，所有评估均进行 20 次重复以获取 95% 置信区间。

### 文本到动作生成：HumanML3D 基准

在 HumanML3D 上，OmniMoGen 与三类方法进行了对比：扩散模型（MDM、MLD、MotionDiffuse、SALAD）、自回归模型（T2M-GPT、MoMask）以及多任务方法（MotionGPT3）。核心结果如 Table 1 所示。

![[assets/figures/papers/2512.19159_42baaa9101bd/figures/005_Table_1.jpg]]
*Table 1: Comparison with existing motion generation methods. The evaluations are conducted 20 times to obtain a 95% confidence interval (±). Best results are highlighted in bold and the second best in underline*

**OmniMoGen-Think 在所有多任务方法中取得最优**，R@1 达到 0.550，相对次优的多任务方法 MotionGPT3（R@1 0.543）提升 1.3%。更重要的是，OmniMoGen 的 FID 仅为 0.061，而 MotionGPT3 为 0.217，差距达 0.156，表明生成质量在分布层面显著更优。MMDist 同样从 MotionGPT3 的 2.29% 降至更低水平。

值得注意的是，OmniMoGen 作为统一架构模型，其性能甚至超越了部分专用文本到动作方法。例如，OmniMoGen-Think 的 FID 优于扩散模型 MDM（0.544）和 MLD（0.473），R@1 也接近当前最优的专用掩码模型 MoMask（0.571）。这一结果验证了统一架构不会因任务泛化而牺牲单一任务性能。

定性对比（Figure 4）进一步揭示，基线方法在复杂语义场景下容易出现动作与文本的错位，而 OmniMoGen 生成的序列与文本描述更为一致。

![[assets/figures/papers/2512.19159_42baaa9101bd/figures/004_Figure_4.jpg]]
*Figure 4: Qualitative comparison of text-to-motion generation on HumanML3D. The red words and boxes highlight the misaligned motions*

### 运动编辑：MotionFix 基准

MotionFix 基准评估模型在“保留源动作特征”与“准确执行编辑指令”之间的平衡能力，核心指标包括 Edited-to-Source R@1 和 Edited-to-Target R@1。

OmniMoGen 在两项指标上均达到最优：Edited-to-Source R@1 比次优方法提升 5.3%，Edited-to-Target R@1 比先前最佳方法提升 1.4%（Table 2）。这一结果的关键瓶颈突破在于：现有编辑方法通常依赖掩码位置预设或扩散条件注入，限制了编辑的灵活性；而 OmniMoGen 通过交叉指令格式自回归解码，模型自动在“保留”与“修改”之间分配注意力，无需显式指定编辑区域。

![[assets/figures/papers/2512.19159_42baaa9101bd/figures/007_Table_2.jpg]]
*Table 2: Quantitative comparison on MotionFix*

### 交叉指令生成：AnyContext 基准

AnyContext 是本文构建的交叉文本-动作指令基准，包含三类任务：**Style-based**（风格编辑）、**Trajectory-based**（轨迹编辑）和 **Speed-based**（速度编辑）。这些任务要求模型同时理解文本指令和输入动作，生成符合组合约束的新动作。

**现有方法在 AnyContext 上普遍失效**：所有基线的 R@1 均低于 30%，物理合理性指标低于 0.91（Table 3）。这揭示了当前方法的根本局限——它们缺乏处理交叉指令的机制，无法同时解析文本约束和动作上下文。

OmniMoGen 在此基准上取得突破性优势：R@1 达到 37.5（OmniMoGen-Think 为 42.9），物理指标达到 0.95（OmniMoGen-Think 为 0.97）。这一性能差距（>12.9 的 R@1 提升）证实了统一交叉指令架构在复杂多模态任务上的不可替代性。

### 消融研究：训练策略与数据组成

Table 4 的系统消融揭示了 OmniMoGen 各组件的作用机制。

![[assets/figures/papers/2512.19159_42baaa9101bd/figures/010_Table_4.jpg]]
*Table 4: Comprehensive ablation study of OmniMoGen. We report Edited-to-Target R@1 and AvgR on MotionFix, and R@1, AvgR, and Physical across all task types in AnyContext*

**训练阶段消融（Table 4B）**：移除监督微调（SFT）阶段导致 MotionFix R@1 从 68.33 骤降至 42.09，AnyContext R@1 从 36.7 降至 19.3。这表明 X2Mo 数据集上的多任务指令微调是模型获得指令跟随能力的核心环节，仅靠预训练语言模型无法自然涌现此类能力。移除 GRPO 强化学习阶段使 AnyContext AvgR 从 6.1 恶化至 8.0，物理指标从 0.95 降至 0.91，验证了 RL 阶段对语义对齐和物理合理性的双重提升。

**数据组成消融（Table 4C）**：从训练数据中移除运动编辑子任务使 MotionFix R@1 从 68.33 降至 56.25；移除多轮编辑导致 R@1 降至 59.07。这说明多任务数据之间存在正向迁移，编辑能力受益于多样化的指令格式训练。

**奖励函数消融（Table 4D）**：移除语义奖励使 MotionFix R@1 从 68.33 降至 63.62；移除物理奖励使物理指标从 0.95 降至 0.92。双奖励设计的必要性得到验证——语义奖励驱动指令对齐，物理奖励抑制滑步等伪影，二者互补。

**Token 化方法消融（Table 4F）**：RVQ-VAE 优于普通 VQ-VAE，MotionFix R@1 从 64.91 提升至 68.33。残差量化通过逐层细化潜在表示，在相同码本容量下实现了更高的重建保真度，为下游生成提供了更精确的动作离散表示。

### 反思机制与上下文窗口瓶颈

OmniMoGen-Think 在生成后自动评估并反思，支持多轮迭代改进。Figure 8 展示了反思轮次对性能的影响：从 0 轮增加到 3 轮，MotionFix 和 AnyContext 的检索性能持续提升，物理指标同步改善。然而，当反思轮次扩展到 5 轮时，性能出现下降。

**这一转折点揭示了当前架构的瓶颈**：自回归 transformer 的有效上下文窗口限制了长链反思的收益。超过 4 轮后，历史 token 积累超出模型的有效建模范围，导致注意力分散和生成质量退化。这是统一架构在实际部署中需要关注的核心限制。

### 失败模式与局限性

除上下文窗口限制外，分析中还隐含以下关键局限：

1. **物理奖励的手工设计依赖**：当前物理合理性奖励基于足部接触的启发式规则，虽然有效降低了滑步，但无法覆盖更复杂的物理约束（如关节角度限制、动力学一致性）。GRPO 框架本身具备从数据中学习奖励的潜力，但本文未探索自动奖励发现。

2. **动作 Token 化效率**：RVQ-VAE 使用 6 层残差码本，每帧动作被编码为 6 个离散 token。对于长序列动作，token 数量线性增长，加剧了上下文窗口压力。更高压缩率的 token 化方法可能是缓解这一问题的方向。

3. **数据覆盖的边界**：X2Mo 数据集基于 AMASS 构建，动作类型以日常运动和舞蹈为主。对于极端运动（如体育竞技、杂技）或人-物交互场景，数据覆盖不足可能导致生成质量下降。

## 定位与知识库关联

### 1. 任务统一范式的谱系定位

OmniMoGen 的核心思想是将多样化的人体动作生成任务统一为“交叉文本-动作指令”的序列建模问题，这与大语言模型统一 NLP 任务的范式一脉相承。在此之前的动作生成方法普遍将文本到动作、运动编辑、内插等视为独立问题，依赖任务特定的架构和输入格式。

**与自回归动作生成方法的对比。** **T2M-GPT** 首次将动作序列离散化为 token 并采用自回归 transformer 进行文本到动作生成，证明了离散 token 化在动作生成中的可行性。然而，其输入格式仅限于纯文本提示，无法处理需要源动作上下文的编辑或组合任务。**MoMask** 则采用掩码 transformer 架构，通过预定义的掩码位置限制生成范围，在文本到动作任务上取得了当时的最优性能，但其掩码机制天然绑定了特定的任务模式，难以泛化到自由形式的交叉指令。OmniMoGen 继承了离散 token 化的思路，但通过 RVQ-VAE 的残差量化替代了普通 VQ-VAE（消融实验中 RVQ-VAE 使 MotionFix R@1 从 64.91 提升至 68.33，见 Table 4(F)），并将自回归 transformer 的输入扩展为文本 token 与动作 token 的交叉序列，从而在单一架构内同时支持文本到动作生成、风格/轨迹编辑、内插、外插和组合编辑等多种任务。

**与多任务动作生成方法的对比。** **MotionGPT3** 是此前最具代表性的多任务动作生成方法，结合了自回归和对比学习目标，能够处理生成和编辑任务。在 HumanML3D 文本到动作基准上，MotionGPT3 的 R@1 为 0.543，是此前多任务方法中的最佳水平。OmniMoGen 在此基础上将 R@1 提升至 0.550（相对提升 1.3%），同时将 FID 从 0.217 大幅降至 0.061（Table 1）。更关键的差异体现在统一性上：MotionGPT3 仍需要针对不同任务设计不同的输入模板和训练目标，而 OmniMoGen 通过统一的交叉指令格式和两阶段训练（SFT + GRPO RL）实现了真正的端到端多任务学习，无需任何任务特定的模块或目标函数。

**与扩散模型方法的对比。** **SALAD** 和 **MLD** 等扩散模型在文本到动作生成中取得了具有竞争力的性能，**MotionReFit** 则将扩散模型应用于运动编辑。扩散模型的核心优势在于生成多样性和迭代细化的能力，但其条件机制通常需要针对不同任务设计不同的条件信号注入方式。例如，MotionReFit 的编辑流程需要明确指定源动作和编辑区域，无法像 OmniMoGen 那样通过自由形式的文本指令灵活组合多种编辑需求。在 AnyContext 交叉指令基准上，现有扩散方法（如 MotionReFit）的 R@1 普遍低于 30%，物理指标低于 0.91，而 OmniMoGen 的 R@1 达到 37.5，物理指标达到 0.95（Table 3），这揭示了扩散模型在处理交叉指令时的根本性局限——其条件机制难以灵活融合文本与动作的双模态上下文。

### 2. 关键设计选择的因果机制

**两阶段训练的必要性。** 消融实验揭示了 SFT 和 RL 两个阶段各自的不可替代性。移除 SFT 阶段导致 MotionFix R@1 从 68.33 骤降至 42.09，AnyContext R@1 从 36.7 降至 19.3（Table 4(B)），说明单纯依靠强化学习的探索无法使模型习得遵循交叉指令的基本能力——多任务监督微调为模型提供了必要的指令理解先验。移除 GRPO RL 阶段则使 AnyContext 的 AvgR 从 6.1 恶化到 8.0，物理指标从 0.95 降至 0.91（Table 4(B)），表明 SFT 阶段的模仿学习虽然建立了指令跟随能力，但无法自动优化物理合理性——RL 阶段的物理奖励（基于足部滑步惩罚）是提升动作逼真度的关键驱动力。

**双奖励设计的互补性。** GRPO RL 阶段的语义奖励（基于对比检索的余弦相似度）和物理奖励（基于接触帧足部速度约束）分别解决了不同维度的问题。移除语义奖励使 MotionFix R@1 从 68.33 降至 63.62，移除物理奖励使物理指标从 0.95 降至 0.92（Table 4(D)），两者呈现出清晰的互补关系：语义奖励主要提升生成动作与文本指令的对齐程度，物理奖励则专门抑制滑步等物理不合理现象。这一设计的洞察在于，单一奖励函数（如仅使用检索相似度）会导致奖励黑客行为——模型可能生成语义相关但物理上不可行的动作。

**多任务数据构成的贡献。** 从训练数据中移除运动编辑子任务使 MotionFix R@1 从 68.33 骤降至 56.25，移除多轮编辑导致 R@1 下降到 59.07（Table 4(C)），这表明模型在编辑任务上的能力并非来自架构本身，而是来自训练数据中多样化指令格式的覆盖。X2Mo 数据集通过运动图构建了 137K 条交叉指令，覆盖了 in-context 生成、运动编辑、多轮编辑和反思四种类型（Figure 7），这种数据多样性是 OmniMoGen 统一能力的基础。

### 3. 适用边界与局限

**上下文窗口瓶颈。** 反思轮次的实验揭示了当前架构的显著局限：反思轮次从 0 增加到 3 持续提升检索性能和物理指标，但扩展到 5 轮后性能反而下降（Figure 8; Appendix D.1）。论文将此归因于当前 transformer 的有效上下文窗口限制。这意味着 OmniMoGen 在处理需要长链推理或多轮交互编辑的任务时存在硬性天花板，无法通过简单增加反思轮次来持续提升性能。这一局限的根源在于自回归 transformer 的注意力机制在长序列上的退化，而非反思机制本身的问题。

**手工奖励设计的依赖。** GRPO RL 阶段依赖手工设计的物理奖励函数（基于足部接触帧的速度约束），这限制了模型在其他物理约束（如关节角度限制、动力学可行性）上的自动发现能力。当前奖励设计仅覆盖了滑步问题，对于更复杂的物理不合理现象（如肢体穿透、关节超伸）缺乏显式约束，模型在这些维度上的表现依赖于 SFT 阶段从数据中隐式学习到的模式，而非 RL 阶段的显式优化。

**动作数据覆盖范围。** X2Mo 数据集基于 AMASS 构建，其动作类型主要集中在日常人体运动（行走、跑步、跳跃等）。对于更极端的动作类型（如杂技、舞蹈、体育专项动作）或需要精确物理交互的动作（如与物体的接触操作），当前框架的适用性尚未验证。RVQ-VAE 的 6 层残差码本（每层 512 码向量，维度 512）在重建保真度上可能存在上限，对于高动态或精细手部动作的 token 化质量需要进一步评估。

### 4. 开放问题

1. **长序列扩展**：如何突破当前 transformer 的上下文窗口限制，使模型能够处理更长序列的动作生成或更多轮的交互编辑？可能的路径包括采用状态空间模型（如 Mamba）作为骨干，或设计层次化的动作 token 化方法以降低序列长度。

2. **自动奖励发现**：能否在 GRPO 框架中引入自动的物理约束发现机制，减少对手工设计奖励的依赖？例如，通过对抗训练或基于物理模拟器的可微奖励来自动识别和惩罚物理不合理现象。

3. **数据扩展潜力**：该统一框架是否能从更广泛的动作数据源（如视频中的 3D 人体姿态估计、虚拟现实动作捕捉）中受益，从而覆盖更丰富的动作类型和任务？这需要解决跨数据源的 token 化一致性问题。

4. **最优反思轮数的自适应决策**：反思超过一定轮数后性能下降的机制尚不完全清晰——是由于注意力分散、错误累积还是其他原因？能否设计自适应的反思终止策略，使模型在性能达到峰值时自动停止？

5. **更大模型的缩放效应**：当前使用 Gemma2-2B 作为骨干，更高效的 token 化方法（如更高压缩率的 RVQ-VAE）或更大的语言模型是否能进一步提升统一生成质量？这需要系统性的缩放实验来验证。

## 原文 PDF

![[paperPDFs/arxiv_2025/OmniMoGen.pdf]]
