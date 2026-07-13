---
title: "Matrix-Game 3.0: Real-Time and Streaming Interactive World Model with Long-Horizon Memory"
type: paper
paper_level: A
venue: arXiv
year: 2026
pdf_ref: "paperPDFs/arxiv_2026/Matrix-Game_3.0:_Real-Time_and_Streaming_Interactive_World_Model_with_Long-Horizon_Memory.pdf"
project_link: https://matrix-game-v3.github.io/
code_link: https://github.com/SkyworkAI/Matrix-Game
aliases:
- MG30
tags:
- arxiv_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/generative_models_diffusion
core_operator: 引入相机感知的显式记忆检索，并与基于残差收集和注入的自校正训练相结合，使模型能够在统一的双向DiT中利用历史与记忆信息进行鲁棒预测，从而打破误差累积循环。
primary_logic: 通过将检索到的记忆帧、近期历史帧和当前待预测帧在同一个自注意力空间中联合建模，并在训练时人为注入生成帧的预测残差，模型学会了从带噪声的条件信息中自校正，使得在实时推理中也能维持长时记忆和场景一致性。
claims:
- Matrix-Game 3.0 achieves up to 40 FPS real-time generation at 720p resolution with a 5B model.
- Camera-aware memory retrieval and injection enable the base model to achieve long horizon spatiotemporal consistency.
- Error-aware training learns self-correction for the base model by modeling prediction residuals and re-injecting imperfect generated frames.
- Multi-segment autoregressive distillation strategy based on Distribution Matching Distillation (DMD) aligns training and inference for efficient real-time generation.
---

# Matrix-Game 3.0: Real-Time and Streaming Interactive World Model with Long-Horizon Memory

> [!tip] 核心洞察
> 通过将检索到的记忆帧、近期历史帧和当前待预测帧在同一个自注意力空间中联合建模，并在训练时人为注入生成帧的预测残差，模型学会了从带噪声的条件信息中自校正，使得在实时推理中也能维持长时记忆和场景一致性。

| 字段 | 内容 |
|------|------|
| 中文题名 | Matrix-Game 3.0：具备长时记忆的实时流式交互世界模型 |
| 英文题名 | Matrix-Game 3.0: Real-Time and Streaming Interactive World Model with Long-Horizon Memory |
| 会议/期刊 | arXiv 2026 |
| Links | [paper](https://arxiv.org/abs/2604.08995) · [Project](https://matrix-game-v3.github.io/) · [Code](https://github.com/SkyworkAI/Matrix-Game) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/generative_models_diffusion |
| Method | Matrix-Game 3.0 |
| Dataset | VAE Reconstruction Quality, VAE Decoding Speed, Inference FPS |

> [!tip] 效果简介
> - VAE Reconstruction Quality 上，PSNR 31.84 (50% pruned) vs 33.79 (Wan2.2 VAE) (-1.95)；SSIM 0.99 vs 0.99 (Wan2.2 VAE) (0)。
> - VAE Decoding Speed 上，Time (s) 0.30 (50% pruned Dec.) vs 0.76 (Wan2.2 VAE Dec.) (-0.46)。
> - Inference FPS (720p, 5B model) 上，FPS ~40。

## 概要

现有交互式世界模型面临一个根本瓶颈：在自回归生成过程中缺乏长时记忆能力，误差随时间累积，导致分钟级序列的时空一致性崩溃，同时难以兼顾高分辨率实时生成。**Matrix-Game 3.0** 针对这一问题，提出了一种记忆增强的交互式世界模型，核心思路是将**相机感知的显式记忆检索**与**基于残差收集和注入的自校正训练**相结合，使模型在统一的双向 DiT 框架中联合建模检索到的记忆帧、近期历史帧和当前待预测帧，从而打破误差累积循环。

该框架由四个关键模块构成：误差感知交互基础模型、相机感知长时记忆机制、训练-推理对齐的少步蒸馏管线，以及实时推理加速模块。在 5B 参数规模下，模型实现了 720p 分辨率下最高约 40 FPS 的实时生成性能；扩展到 2×14B 规模后，生成质量、动态表现和泛化能力进一步提升。

方法定位上，Matrix-Game 3.0 区别于前代 **Matrix-Game 2.0**（He et al., arXiv 2025）缺乏显式记忆和自校正机制的局限，也不同于 **Genie 3**（Ball et al., 2025）约 24 FPS 的实时性能上限或 **Lingbot-World**（Robbyant Team, arXiv 2026）因长上下文建模而牺牲实时性的设计。与 **RELIC**（Hong et al., arXiv 2025）通过额外记忆分支注入历史信息的方式相比，本工作将记忆帧直接纳入统一自注意力空间，并结合误差感知训练实现端到端的自校正，在长时一致性与实时效率之间取得了更优的平衡。

交互式世界模型的目标是在用户实时操控下生成时空一致的长视频，从而为游戏、仿真和具身智能提供可交互的虚拟环境。这一任务面临双重挑战：一方面，模型必须在自回归生成过程中维持分钟级序列的时空一致性，避免误差累积导致的场景漂移；另一方面，系统还需满足高分辨率（如720p）下的实时交互需求，这对模型容量和推理效率提出了严苛约束。

现有方法在这两个维度上存在明显缺口。**Matrix-Game 2.0**（He et al., arXiv 2025）作为前代实时交互世界模型，虽然具备基本的动作可控性，但缺乏显式记忆模块，难以在长序列中抑制误差累积，导致时空一致性随时间推移而崩溃。**Genie 3**（Ball et al., 2025）隐式地具备一定记忆能力，但其推理速度仅约24 FPS，无法满足高帧率实时交互需求。**Lingbot-World**（Robbyant Team, arXiv 2026）尝试通过长上下文建模提升几何一致性，却以牺牲实时性为代价。**RELIC**（Hong et al., arXiv 2025）引入了相机感知的记忆增强机制，通过额外的记忆分支注入历史信息，但其记忆模块与生成主干相对独立，未能实现历史、记忆与当前帧在统一注意力空间中的联合建模。

上述方法的根本瓶颈在于：自回归生成中的误差累积循环未被有效打破。当模型仅依赖干净的真实帧进行训练，而推理时却必须基于自身先前生成的、可能包含误差的帧进行预测时，训练与推理之间的分布偏移会持续放大预测误差，最终导致场景结构扭曲和细节丢失。因此，核心问题转化为：**如何让模型学会从带噪声的条件信息中自校正，并在实时推理中维持长时记忆和场景一致性。**

Matrix-Game 3.0 针对这一瓶颈提出了系统性解决方案。其核心洞察是：通过将检索到的记忆帧、近期历史帧和当前待预测帧在同一个自注意力空间中联合建模，并在训练时人为注入生成帧的预测残差，模型能够学会从带噪声的条件信息中进行自校正。这一设计使得模型在实时推理中即使面对自身生成的不完美帧，也能借助记忆信息维持长时一致性。配合基于分布匹配蒸馏（DMD）的多段自生成滚动方案和系统级推理加速，Matrix-Game 3.0 最终实现了720p分辨率下最高40 FPS的实时交互世界模型。

## 核心方法与创新机理

Matrix-Game 3.0 相对于前代交互式世界模型的核心突破在于，它首次将**显式长时记忆**与**自校正生成**统一到实时推理框架中。此前的 **Matrix-Game 2.0**（He et al., arXiv 2025）虽能实现实时交互，但缺乏记忆机制，在分钟级自回归生成中会因误差累积而导致时空一致性崩溃；**Genie 3**（Ball et al., 2025）虽隐式具备记忆能力，但实时性仅约 24 FPS；**Lingbot-World**（Robbyant Team, arXiv 2026）通过长上下文建模提升了几何一致性，却难以同时维持实时性；**RELIC**（Hong et al., arXiv 2025）则通过额外的记忆分支注入历史信息，但记忆与主模型之间是分离的。Matrix-Game 3.0 的关键创新在于四个相互耦合的 changed slots，它们共同打破了“长时一致性”与“高分辨率实时生成”之间的既有权衡。

### 1. 相机感知的联合记忆建模

传统记忆增强方法（如 RELIC）将记忆作为外部分支处理，而 Matrix-Game 3.0 采用**统一 DiT 框架**，将检索到的记忆帧、近期历史帧和当前待预测帧置于同一个自注意力空间中联合建模（Figure 4、Figure 5）。这一设计的因果作用是：记忆信息不再通过独立的交叉注意力注入，而是与历史和当前帧在相同的注意力模式下交互，使模型能够直接学习三者之间的时空依赖关系。

记忆检索本身是**相机感知**的：系统根据当前查询视角与历史帧之间的几何重叠度来选择记忆帧。检索分数基于三维截椎体相交体积（精确方案）或采样点投影近似（GPU 加速方案）。这一机制使得模型在场景重访时能够恢复此前观察到的结构（见 Figure 9 的消融定性结果），从而从根本上缓解了长序列生成中的遗忘问题。

### 2. 误差感知的自校正训练

自回归世界模型的核心瓶颈在于：训练时模型接收的是干净的真实帧，而推理时接收的却是自身生成的、含有累积误差的帧。Matrix-Game 3.0 通过**误差缓冲器**机制打破了这一暴露偏差循环。

具体而言，训练过程中系统在线收集每一步的预测残差 $\delta = \hat{x}^i - x^i$（Eq. (1)），并将其重新注入到历史隐帧和记忆隐帧中：
$$\tilde{x}^i = x^i + \gamma \delta \quad \text{(Eq. (2))}, \quad \tilde{m}^{1:r} = m^{1:r} + \gamma_m \delta \quad \text{(Eq. (5))}$$

这意味着模型在训练时就被迫从带噪声的条件信息中进行预测，学会了**自校正**——即使输入的历史和记忆帧存在误差，模型仍能输出一致的预测。Figure 8 的定性结果表明，经过误差感知训练的基础模型在长序列生成中能够维持稳定的背景，未出现明显的漂移。

### 3. 训练-推理对齐的少步蒸馏

为了实现实时推理，Matrix-Game 3.0 需要将多步基础模型蒸馏为少量步数的学生模型。与标准因果学生蒸馏不同，该方法采用基于 **Distribution Matching Distillation (DMD)** 的多段自生成滚动方案（Figure 6）。

核心机制是：双向学生模型执行多段自回归滚动，仅将最后一段用于分布匹配。这使学生在蒸馏过程中暴露于自身的累积误差，从而对齐了训练与推理时的数据分布。DMD 梯度近似为：
$$\nabla_{\theta} \mathcal{L}_{\mathrm{DMD}} \approx - \mathbb{E}_t \left[ \int \left( s_{\mathrm{data}} - s_{\mathrm{gen},\xi} \right) \nabla_{\theta} x_t d\epsilon \right] \quad \text{(Eq. (8))}$$

该方案确保了蒸馏后的少步模型在实际推理中不会因分布偏移而产生严重的质量退化。

### 4. 系统级实时推理加速

在方法创新的基础上，Matrix-Game 3.0 通过三项系统优化实现了 720p 分辨率下最高 40 FPS 的实时推理（Table 1）：

- **INT8 量化**：对注意力投影层进行量化，降低计算开销。
- **MG-LightVAE 剪枝**：对 VAE 解码器进行 50% 或 75% 的通道剪枝。50% 剪枝方案在 PSNR 仅下降 1.95（从 33.79 到 31.84）的代价下，将解码时间从 0.76s 降至 0.30s，实现了 2.6× 加速（Table 2）。
- **GPU 加速的采样式记忆检索**：将原本基于精确截椎体相交体积的 CPU 检索替换为基于采样点投影的 GPU 近似计算。消融实验表明，移除 GPU 检索会导致 FPS 骤降至 6.60，是实时性能最关键的单点瓶颈。

值得注意的是，这四个创新并非孤立存在：误差感知训练使基础模型能够容忍记忆检索中的噪声，联合自注意力让记忆信息直接参与自校正过程，而蒸馏和加速模块则将这一能力压缩到实时推理的约束之内。这种**跨模块的因果耦合**是 Matrix-Game 3.0 超越此前方法的核心原因。

Matrix‑Game 3.0 的整体 pipeline 由四个核心模块串联而成，形成一个从数据生成到实时部署的闭环系统（图 2）。其设计目标是在维持双向 DiT 先验优势的前提下，引入长时记忆与自校正能力，并最终通过系统优化实现 720p@40 FPS 的实时交互式世界模型。

**数据引擎**位于 pipeline 最上游，基于 Unreal Engine 生成带动作标签与相机姿态标注的长时域训练视频。这一阶段为后续的记忆检索、误差训练和蒸馏提供了精确的相机‑动作配对监督信号。

**误差感知的交互式基础模型**（Sec 3.1）是框架的第一个核心模块。它采用统一的双向架构，同时服务于多步基础模型和后续的少步蒸馏学生模型。该模块的关键机制在于：训练时不再仅使用干净的 Ground‑Truth 历史帧，而是通过误差缓冲器在线收集预测残差 $\delta = \hat{x}^i - x^i$，并将其重新注入到历史隐帧中 $\tilde{x}^i = x^i + \gamma \delta$，迫使模型学会从带噪声的条件信息中自校正，从而打破自回归生成中的误差累积循环。

**相机感知的长时记忆机制**（Sec 3.2）在基础模型之上叠加。它通过相机姿态和视场重叠度检索历史记忆帧，并将检索到的记忆隐帧、近期历史隐帧与当前待预测噪声隐帧置于同一个联合自注意力空间中进行建模（图 4、图 5）。训练时，误差缓冲器同样被扩展至记忆帧，对历史和记忆同时施加扰动，增强模型对不完美条件信息的鲁棒性。此外，该模块引入头向扰动的旋转位置编码（Head‑wise Perturbed RoPE），通过为不同注意力头赋予不同的基频 $\hat{\theta}_h = \theta_{\mathrm{base}}(1 + \sigma_{\theta} \epsilon_h)$ 来打破周期性同步，缓解远距离记忆的位置混叠。

**训练‑推理对齐的少步蒸馏**（Sec 3.3）将多步基础模型压缩为少量采样步数的学生模型。其核心创新在于采用基于 Distribution Matching Distillation（DMD）的多段自生成滚动方案：双向学生模型执行多段连续 rollout 以模拟真实少步推理过程，仅将最后一段用于分布匹配，从而对齐训练与推理分布，避免标准因果蒸馏中的曝光偏差。

**实时推理加速模块**（Sec 3.4）负责将蒸馏后的模型推向实时部署。该模块包含三项关键优化：(1) 对注意力投影层进行 INT8 量化；(2) 设计 MG‑LightVAE，通过 50% 或 75% 的通道剪枝将 VAE 解码速度提升至 2.6 倍，PSNR 仅从 33.79 dB 降至 31.84 dB（Table 2）；(3) 将基于截椎体相交体积的精确记忆检索 $s_{\mathrm{exact}}(i, j)$ 替换为基于采样点投影的 GPU 加速近似 $s_{\mathrm{approx}}(i, j)$，该优化对实时性贡献最大——移除后 FPS 骤降至 6.60（Table 1）。最终，5B 模型在 720p 分辨率下达到约 40 FPS 的实时生成。

整个 pipeline 的输入为初始图像帧与用户动作指令，输出为实时、动作可控且具备长时一致性的视频流。四个模块的串行依赖关系决定了：基础模型的自校正能力是记忆机制有效的前提，而蒸馏与加速模块则在不破坏前序模块所建立的一致性的前提下，将系统推向实时性能边界。

### 补充图表

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2604_08995/figures/002_Figure_2.jpg]]
*Figure 2: Overview of Matrix-Game 3.0. Our framework unifies Unreal Engine–based data generation, memory-augmented DiT training with an error buffer, and accelerated real-time deployment. It generates long-horizon training videos with paired action and camera-pose supervision, learns action-conditioned generation with memory-enhanced consistency, and supports real-time inference through few-step sampling, quantization, and pruning, achieving 720p@40FPS with a 5B model*

Matrix-Game 3.0 的系统架构由四个关键模块级联而成，每个模块针对长时交互世界模型的一个核心瓶颈进行设计。以下逐一剖析各模块的机制与关键公式。

### 3.1 误差感知的交互式基础模型

基础模型的核心设计理念是**在训练阶段主动暴露于推理时可能出现的误差累积**，从而学会自校正。传统方法仅在干净的真实帧上训练，推理时一旦前序帧产生微小偏差，自回归循环会迅速放大该误差，导致场景漂移。

为解决此问题，模型引入**误差缓冲器（Error Buffer）**机制。在训练过程中，模型对历史帧的预测残差进行在线收集：

$$\delta = \hat{x}^i - x^i \quad \text{(Eq. 1)}$$

其中 $\hat{x}^i$ 为模型对第 $i$ 帧隐变量的干净估计，$x^i$ 为真实隐帧。该残差 $\delta$ 被存入缓冲器，随后用于扰动历史条件帧：

$$\tilde{x}^i = x^i + \gamma \delta \quad \text{(Eq. 2)}$$

$\gamma$ 为缩放因子，控制扰动强度。通过将带噪声的历史帧 $\tilde{x}^{1:k}$ 作为条件输入，基础模型的流匹配训练目标变为：

$$\mathcal{L} = \mathbb{E}_{x, t, \epsilon, \delta} \left[ \left\| \left( \epsilon - x^{k+1:N} \right) - v_{\theta} \left( x_t^{k+1:N}, t \mid \tilde{x}^{1:k}, c \right) \right\|_2^2 \right] \quad \text{(Eq. 3)}$$

其中 $c$ 为动作条件，$v_{\theta}$ 为速度预测网络。该设计的因果机制在于：**模型被迫从被污染的上下文中恢复干净预测，从而习得对历史误差的鲁棒性**，打破了自回归生成中的误差累积循环。

### 3.2 相机感知的长时记忆机制

在基础模型之上，记忆模块引入相机感知的显式记忆检索，使模型能够利用远超近期历史帧的长时上下文。其关键设计包括两个层面。

**统一自注意力建模。** 不同于将记忆作为外部分支注入（如 **RELIC**, Hong et al., arXiv 2025），Matrix-Game 3.0 将检索到的记忆隐变量 $m^{1:r}$、时序对齐的近期历史隐变量 $x^{1:k}$ 和当前待预测的噪声隐变量 $x_t^{k+1:N}$ 置于同一个自注意力空间中联合建模。这一设计使得记忆信息能够直接参与跨帧注意力交互，而非仅通过交叉注意力间接影响。

**误差感知的记忆训练。** 记忆模块同样受益于误差缓冲器机制。训练时对记忆帧和历史帧分别施加扰动：

$$\tilde{x}^{1:k} = x^{1:k} + \gamma_h \delta, \quad \tilde{m}^{1:r} = m^{1:r} + \gamma_m \delta \quad \text{(Eq. 5)}$$

其中 $\delta$ 来自扩展后的误差缓冲器，覆盖记忆、历史及当前帧的预测残差（Eq. 4）。记忆增强模型的训练目标为：

$$\mathcal{L}_{\mathrm{mem}} = \mathbb{E}_{x, m, t, \epsilon, \delta} \left[ \left\| \left( \epsilon - x^{k+1:N} \right) - v_{\theta} \left( x_t^{k+1:N}, t \mid \tilde{x}^{1:k}, \tilde{m}^{1:r}, c, g \right) \right\|_2^2 \right] \quad \text{(Eq. 6)}$$

$g$ 为相机姿态条件。该目标使模型学会从带噪声的记忆和历史中同时进行自校正预测。

**时序编码优化。** 为缓解远距离记忆帧的位置编码混叠问题，模型引入头级扰动旋转位置编码（Head-wise Perturbed RoPE）：

$$\hat{\theta}_h = \theta_{\mathrm{base}} (1 + \sigma_{\theta} \epsilon_h) \quad \text{(Eq. 7)}$$

通过对不同注意力头赋予不同的 RoPE 基频，打破周期性同步，使模型能够区分相隔较远的记忆帧与近期帧。

### 3.3 训练-推理对齐的少步蒸馏

蒸馏模块的目标是将多步基础模型压缩为少量采样步数的学生模型，同时保持训练与推理的分布一致性。其核心创新在于**多段自生成滚动方案**：双向学生模型在蒸馏过程中执行多段自回归生成，仅将最后一段的输出用于分布匹配蒸馏（Distribution Matching Distillation, DMD）。DMD 的梯度近似为：

$$\nabla_{\theta} \mathcal{L}_{\mathrm{DMD}} \triangleq \mathbb{E}_t [ \nabla_{\theta} D_{\mathrm{KL}} ( p_{\theta,t} \parallel p_{\mathrm{data},t} ) ] \approx - \mathbb{E}_t \left[ \int \left( s_{\mathrm{data}} - s_{\mathrm{gen},\xi} \right) \nabla_{\theta} x_t d\epsilon \right] \quad \text{(Eq. 8)}$$

其中 $s_{\mathrm{data}}$ 和 $s_{\mathrm{gen},\xi}$ 分别为数据分布和生成分布的分数函数。多段滚动的设计使得学生模型在训练时即暴露于自生成的条件分布中，避免了标准蒸馏中训练-推理分布失配的问题。

### 3.4 实时推理加速

加速模块通过系统级优化实现最高 40 FPS 的 720p 实时生成。主要技术包括：INT8 量化注意力投影层、MG-LightVAE 解码器剪枝（50%/75% 通道剪枝），以及 GPU 加速的采样式记忆检索。记忆检索的近似重叠分数计算为：

$$s_{\mathrm{approx}}(i, j) = \frac{1}{N} \sum_{n=1}^{N} \mathbf{1}_n^{(j)}$$

通过采样点投影替代精确截椎体相交计算（$s_{\mathrm{exact}}$），将检索从 CPU 瓶颈迁移至 GPU 并行执行。消融实验表明，移除 GPU 化检索会导致 FPS 骤降至 6.60，验证了该组件对实时性能的关键作用。

### 补充图表

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2604_08995/figures/003_Figure_3.jpg]]
*Figure 3: Illustration of our interactive base model. We jointly perform error-aware modeling over the past and current latent frames, while explicitly injecting action conditions into the model. This design enables autoregressive, long-horizon interactive generation and maintains consistency with the subsequent distillation stage*

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2604_08995/figures/005_Figure_5.jpg]]
*Figure 5: Frame-level self-attention visualization for the memory-enhanced DiT*

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2604_08995/figures/006_Figure_6.jpg]]
*Figure 6: Illustration of our few-step distillation stage. The bidirectional student performs multisegment rollouts to mimic actual few-step inference, with the final segment used for distribution matching, thereby ensuring training-inference consistency*

## 实验与关键发现

### 主结果

Matrix-Game 3.0 的核心性能指标围绕实时性与重建质量展开。在 5B 参数规模下，模型实现了 **720p 分辨率约 40 FPS** 的实时生成（Abstract, Table 1），这一速度建立在多项系统级优化的协同之上。当模型规模扩展至 2×14B 时，生成质量、动态表现和泛化能力进一步提升（Abstract）。

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2604_08995/figures/012_Table_1.jpg]]
*Table 1: Ablation on major acceleration components with 75% VAE pruning. We report the FPS change after removing each major acceleration component from the full inference setup*

VAE 重建质量与效率的权衡是实时系统的关键瓶颈。原始 Wan2.2 VAE 解码单帧耗时 0.76 秒，无法满足实时需求。经 50% 剪枝的 MG-LightVAE 将解码时间降至 **0.30 秒（2.6× 加速）**，PSNR 从 33.79 降至 31.84（-1.95 dB），但 SSIM 保持 0.99 不变（Table 2），表明结构保真度损失极小。进一步剪枝至 75% 可换取更高吞吐，但 PSNR 下降更为显著，需在具体部署场景中权衡。

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2604_08995/figures/013_Table_2.jpg]]
*Table 2: Reconstruction quality and efficiency comparison between the original Wan2.2 VAE and MG-LightVAE with 50% and 75% pruning. Full denotes encoder+decoder time, and Dec. denotes decoder-only time. Higher PSNR and SSIM indicate better reconstruction fidelity*

### 加速组件消融

Table 1 展示了在 75% VAE 剪枝基础上逐项移除加速组件对 FPS 的影响。**移除 GPU 加速的采样式记忆检索导致 FPS 降至 6.60**，降幅最大，说明记忆检索是实时推理的最大瓶颈——这一结论与直觉一致，因为每帧需在历史帧集合中计算截椎体重叠并检索最相关记忆帧。INT8 量化注意力投影层和 MG-LightVAE 剪枝各自贡献显著的加速增益，三者叠加才使 40 FPS 成为可能。

### 定性验证：自校正与记忆检索

Figure 8 展示了交互式基础模型的定性结果。在仅依赖近期历史帧（无记忆模块）的条件下，双向基础模型配合误差感知训练能够维持稳定的背景，未出现明显的漂移现象，验证了自校正机制的有效性。这归因于训练时人为注入预测残差 $\gamma\delta$ 到历史隐帧中（Eq. (2)-(3)），迫使模型学会从带噪声的条件信息中恢复干净预测。

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2604_08995/figures/008_Figure_8.jpg]]
*Figure 8: Qualitative results of our interactive base model. The action symbol denotes the action of the current frame*

Figure 9 展示了记忆增强模型在长视频中的场景重访能力。当智能体沿原路径反向运动时，**记忆增强模型能够恢复首次访问时的场景结构**，而基线方法则出现明显的几何退化。这直接验证了相机感知记忆检索的核心价值：通过截椎体重叠分数 $s(i,j)$ 选择与当前视角几何重叠度最高的历史帧作为记忆条件，并在统一自注意力空间中联合建模（Figure 4, Figure 5），使模型能够跨越长时间间隔复用历史信息。

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2604_08995/figures/009_Figure_9.jpg]]
*Figure 9: Memory-based scene revisitation in long videos. Each row is sampled uniformly in time; the first frame is the input image, and the second-half actions reverse the first-half actions*

### 失败模式与局限

尽管整体性能令人印象深刻，以下局限需在解读时注意：

1. **分辨率与序列长度的扩展性**：当前优化目标锁定在 720p，更高分辨率或更长序列下的效率尚未验证。这涉及 DiT 主干的自注意力计算复杂度与 VAE 潜在空间分辨率的双重约束。

2. **记忆机制的鲁棒性边界**：记忆检索依赖相机姿态和视场重叠度量 $s_{\mathrm{approx}}(i,j)$，在动态遮挡、剧烈光照变化或场景突变（如穿墙传送）等条件下，检索到的记忆帧可能与当前观测产生语义冲突，此时模型的鲁棒性缺乏定量评估。

3. **蒸馏质量退化**：从多步教师模型到少步学生模型的蒸馏过程中，尽管多段滚动方案（Figure 6）对齐了训练-推理分布，但 VAE 剪枝带来的 PSNR 下降（-1.95 dB）表明质量退化客观存在。蒸馏模型在快速运动或细粒度纹理区域的生成质量仍需进一步检验。

### 关键图表结论速览

- **Table 1**：GPU 加速记忆检索是实时推理的最大单一瓶颈，移除后 FPS 骤降至 6.60。
- **Table 2**：50% 剪枝的 MG-LightVAE 以 1.95 dB PSNR 代价换取 2.6× 解码加速，SSIM 无损。
- **Figure 8**：误差感知训练使基础模型在无记忆条件下仍能维持背景稳定性。
- **Figure 9**：相机感知记忆检索使模型在场景重访时恢复结构信息，是长时一致性的关键使能因素。

### 补充图表

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2604_08995/figures/011_Figure_11.jpg]]
*Figure 11: Qualitative results of our distilled model. Each row is sampled uniformly over time*

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2604_08995/figures/014_Figure_12.jpg]]
*Figure 12: For each case, the top row shows the original video and the bottom row shows the reconstruction by the 50% pruned MG-LightVAE*

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2604_08995/figures/010_Figure_10.jpg]]
*Figure 10: Qualitative results of our 28B model on third-person video generation*

## 定位与知识库关联

### 与现有交互式世界模型的关系

Matrix-Game 3.0 的核心定位是**在实时交互式世界模型中引入显式长时记忆与自校正能力**，其直接的前代工作是 **Matrix-Game 2.0**（He et al., arXiv 2025），后者虽已实现实时交互生成，但缺乏显式记忆模块，导致自回归生成长序列时误差累积、时空一致性崩溃。Matrix-Game 3.0 在此基础上补全了三个关键缺失：相机感知记忆检索、误差感知训练、以及训练-推理对齐的少步蒸馏。

在更广的交互式世界模型谱系中，**Genie 3**（Ball et al., 2025）是领先的隐式记忆方案，可达约 24 FPS，但记忆能力并非显式设计；**Lingbot-World**（Robbyant Team, arXiv 2026）通过长上下文建模提升几何一致性，却难以同时维持实时性；**RELIC**（Hong et al., arXiv 2025）则采用额外的记忆分支注入历史信息，属于相机感知记忆增强的早期尝试。Matrix-Game 3.0 区别于这些工作的关键设计在于：将记忆帧、近期历史帧和当前预测帧置于**同一个自注意力空间**中联合建模，而非作为外部分支处理，从而更充分地利用双向 DiT 的先验能力。

### 核心方法谱系：四个递进模块

Matrix-Game 3.0 的方法体系由四个递进模块构成，每个模块解决一个瓶颈问题：

1. **误差感知交互基础模型（Sec 3.1）**：建立动作可控的基础生成能力。与传统仅在干净真实帧上训练不同，该模块引入误差缓冲器（error buffer），在线收集预测残差 $\delta = \hat{x}^i - x^i$（Eq. 1），并将采样到的残差重新注入历史隐帧 $\tilde{x}^i = x^i + \gamma \delta$（Eq. 2），使模型学会从带噪声的条件信息中自校正。这一设计打破了自回归生成中“误差累积→条件恶化→更大误差”的恶性循环。

2. **相机感知长时记忆机制（Sec 3.2）**：在基础模型之上增加显式记忆检索。记忆帧的选择基于相机截椎体（frustum）重叠度，采用精确体积交叠度量 $s_{\mathrm{exact}}(i, j)$ 或 GPU 加速的采样近似 $s_{\mathrm{approx}}(i, j)$（Sec 3.4）。检索到的记忆隐帧与历史帧一同接受误差扰动（Eq. 5），并在统一的自注意力空间中与当前预测帧联合建模（Eq. 6, Figure 4）。为缓解远距离记忆的位置编码混叠，引入头向扰动 RoPE $\hat{\theta}_h = \theta_{\mathrm{base}} (1 + \sigma_{\theta} \epsilon_h)$（Eq. 7），打破不同注意力头的周期性同步。

3. **训练-推理对齐的少步蒸馏（Sec 3.3）**：基于 Distribution Matching Distillation（DMD），将多步基础模型蒸馏为少步学生模型。关键创新是多段自生成滚动（multi-segment rollouts），使学生模型在训练时即模拟实际推理中的自回归生成过程，仅将最后一段用于分布匹配（Eq. 8, Figure 6），从而消除标准因果学生蒸馏中的训练-推理分布偏移。

4. **实时推理加速（Sec 3.4）**：通过 INT8 量化注意力投影层、MG-LightVAE 解码器剪枝（50%/75%）、GPU 加速的采样式记忆检索等系统优化，将 5B 模型推理速度推至约 40 FPS（720p）。消融实验（Table 1）表明，移除 GPU 化记忆检索导致 FPS 骤降至 6.60，是实时性能的最大瓶颈。

### 适用边界与局限

Matrix-Game 3.0 的适用场景主要限定在**已知相机姿态和动作序列的交互式环境漫游**，其记忆机制的核心假设是场景静态性——记忆检索依赖相机视场重叠，对于动态场景中的遮挡、光照变化或场景突变，检索到的记忆帧可能与当前观测不匹配，鲁棒性有待验证（该点需人工确认具体实验覆盖范围）。

当前模型主要针对 720p 分辨率优化，扩展到更高分辨率或更长序列时效率受限。50% 剪枝的 MG-LightVAE 虽实现 2.6× 解码加速（0.76s → 0.30s），但 PSNR 从 33.79 降至 31.84（Table 2），存在可感知的质量退化。蒸馏后的学生模型相对于教师模型的质量差距尚未量化报告，需人工核实。

### 开放问题

- 模型规模和数据量的进一步扩展能否带来生成质量和泛化能力的质的提升？目前仅报告了 5B 和 2×14B 两个规模。
- 能否设计更高效的架构（如稀疏注意力、状态空间模型）以支持更高分辨率和更长序列的实时生成？
- 记忆机制能否从单纯的相机视场重叠扩展到语义级别的检索，以更好地处理动态环境和复杂交互？
- 蒸馏过程是否可以在保持实时性的前提下进一步缩小与教师模型的质量差距？

## 原文 PDF

![[paperPDFs/arxiv_2026/Matrix-Game_3.0:_Real-Time_and_Streaming_Interactive_World_Model_with_Long-Horizon_Memory.pdf]]
