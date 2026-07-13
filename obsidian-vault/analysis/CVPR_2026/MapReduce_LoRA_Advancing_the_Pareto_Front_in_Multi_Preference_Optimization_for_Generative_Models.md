---
title: "MapReduce LoRA: Advancing the Pareto Front in Multi-Preference Optimization for Generative Models"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/MapReduce_LoRA_Advancing_the_Pareto_Front_in_Multi_Preference_Optimization_for_Generative_Models.pdf
project_link: null
code_link: "https://github.com/SHI-Labs/MapReduce-LoRA"
aliases:
- MLRATER
- MLAPFMPOGM
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 将多目标分解为并行训练奖励特定LoRA专家（Map）并迭代合并（Reduce），通过渐进取平均逐步逼近联合最优；同时利用奖励感知token嵌入实现轻量推理时偏好控制。
primary_logic: 迭代平均LoRA专家权重相当于执行平均近端共识优化，在局部PL条件下几何收缩至联合最优，从而持续扩大帕累托前沿；将每个偏好蒸馏为特殊token嵌入，可在不修改基础模型的情况下组合多种偏好。
claims:
- MapReduce LoRA 在 SD 3.5 M 上 GenEval 提升 36.1%，PickScore 提升 4.6%，OCR 提升 55.7%，同时在 FLUX.1-dev 上也有类似大幅提升。
- 迭代合并次数的消融实验表明，增加合并次数（k=1→4→10）能持续提高三项奖励指标，且减小专家合并带来的性能退化。
- 帕累托前沿对比显示 MapReduce LoRA 在 3D 和 2D 前沿上均显著优于 Rewarded Soup 和 MORL-D，后者在 PickScore 上提升有限。
- 理论分析证明，在目标满足局部光滑和 PL 条件时，迭代合并（渐进取平均）以几何速率收敛到联合最优，优于一次性模型汤。
---

# MapReduce LoRA: Advancing the Pareto Front in Multi-Preference Optimization for Generative Models

> [!tip] 核心洞察
> 迭代平均LoRA专家权重相当于执行平均近端共识优化，在局部PL条件下几何收缩至联合最优，从而持续扩大帕累托前沿；将每个偏好蒸馏为特殊token嵌入，可在不修改基础模型的情况下组合多种偏好。

| 字段 | 内容 |
|------|------|
| 中文题名 | MapReduce LoRA：推进生成模型多偏好优化帕累托前沿 |
| 英文题名 | MapReduce LoRA: Advancing the Pareto Front in Multi-Preference Optimization for Generative Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2511.20629) · [Code](https://github.com/SHI-Labs/MapReduce-LoRA) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | MapReduce LoRA and Reward-aware Token Embedding (RaTE) |
| Dataset | Text-to-Image, Text-to-Video, Language |

> [!tip] 效果简介
> - Text-to-Image (SD 3.5 Medium) 上，GenEval / PickScore / OCR 0.92 / 22.777 / 0.936 (MapReduce LoRA + RaTE) vs 0.68 / 21.784 / 0.601 (SD 3.5 M base) (+36.1% / +4.6% / +55.7%)。
> - Text-to-Image (FLUX.1-dev) 上，GenEval / PickScore / OCR 0.89 / 22.951 / 0.957 (MapReduce LoRA) vs 0.67 / 22.006 / 0.573 (FLUX.1-dev base) (+32.7% / +4.3% / +67.1%)。
> - Text-to-Video (HunyuanVideo) 上，Visual Quality / Motion Quality 4.81 / 1.81 (MapReduce LoRA) vs 3.25 / 0.95 (HunyuanVideo base) (+48.1% / +90.0%)。

## 概要

生成模型的多偏好对齐面临一个核心瓶颈：**联合优化多个奖励模型时，加权求和或一次性模型合并等现有方法无法有效平衡冲突目标，导致“对齐税”——提升某一维度时其他维度性能显著下降，帕累托前沿推进困难**。这一困境在文本到图像、文本到视频和语言生成任务中普遍存在。

本文提出 **MapReduce LoRA**，将多目标分解为并行训练奖励特定LoRA专家的**Map阶段**与迭代加权平均合并的**Reduce阶段**，通过渐进式模型汤（progressive souping）逐步逼近联合最优。理论分析表明，当各目标满足局部光滑和Polyak-Łojasiewicz条件时，该迭代合并过程以几何速率收敛至联合最优，优于一次性Rewarded Soup。同时，**Reward-aware Token Embedding (RaTE)** 将每个偏好蒸馏为特殊token嵌入，在推理时通过附加token实现轻量、可组合的偏好控制，无需切换模型或重训练。

**跨模态核心结果**：
- **文本到图像**（Stable Diffusion 3.5 Medium）：GenEval +36.1%，PickScore +4.6%，OCR +55.7%；在FLUX.1-dev上同样获得大幅提升（Table 1）。
- **文本到视频**（HunyuanVideo）：视觉质量 +48.1%，运动质量 +90.0%（Table 2）。
- **语言任务**（Llama-2 7B Helpful Assistant）：Helpful +43.4%，Harmless +136.7%（Figure 8）。

消融实验证实，增加合并迭代次数（k=1→4→10）持续提升所有奖励指标，且扩展到5个奖励时性能增益无明显递减（Figure 6, Figure 11）。帕累托前沿对比显示，MapReduce LoRA在3D和2D前沿上均显著优于Rewarded Soup和MORL-D（Figure 9, Figure 10）。

### 问题背景：多偏好优化的对齐税困境

生成模型的对齐通常依赖多个奖励模型来评估不同维度的质量。在文本到图像生成中，这些维度包括指令遵循（如 GenEval）、图像美学（如 PickScore）和文本渲染准确性（如 OCR）；在文本到视频生成中，则涵盖视觉质量和运动质量；在语言任务中，则涉及有用性和无害性等。然而，当试图同时优化多个奖励时，现有方法普遍遭遇“对齐税”——提升某一维度性能往往导致其他维度下降，难以有效推进帕累托前沿。

这一困境的根源在于：不同奖励模型之间存在天然冲突。例如，追求更高的美学评分可能导致模型牺牲对复杂文本提示的精确遵循，反之亦然。联合优化多个奖励模型时，简单的加权求和或一次性模型合并方法无法有效平衡这些冲突目标，导致帕累托前沿的推进陷入瓶颈。

### 现有方法缺口

当前主流的多偏好优化方法可分为两类，但各自存在明显局限：

**先验方法**（如 **CaPO**）在训练过程中使用固定权重将多个奖励合并为单一目标进行联合优化。这种方法假设权重在训练前已知且固定，无法灵活适应不同的偏好权衡需求，且在面对奖励冲突时优化效率低下。

**后验方法**（如 **Rewarded Soup**）先独立训练多个奖励特定的专家模型，然后通过一次性权重平均（model souping）进行合并。虽然避免了训练时的权重预设问题，但一次性平均本质上是一种粗糙的近似，无法有效逼近多个冲突目标下的联合最优解。其结果是，合并后的模型往往在各项指标上均显著弱于对应的单奖励专家（性能退化），帕累托前沿的推进幅度有限。

此外，**多目标强化学习基线**（如 **MORL-D** / **MORL-DR**）尝试通过混合数据或混合奖励信号进行直接联合优化，但在实际表现中同样未能有效解决奖励冲突问题，尤其在 PickScore 等美学指标上提升有限。

### 本文动机

针对上述瓶颈，本文提出两个核心动机：

1. **迭代合并替代一次性合并**：一次性模型汤无法充分逼近联合最优，而通过多轮“训练-合并-再训练”的迭代过程，可以逐步缩小与联合最优的差距，持续扩大帕累托前沿。这需要一种系统化的框架来协调多个奖励特定专家的并行训练与渐进式合并。

2. **轻量推理时偏好控制**：即使获得了覆盖广泛权衡关系的帕累托前沿模型，用户在实际推理时仍需灵活控制不同偏好的组合比例。直接切换整个 LoRA 适配器或重新训练模型均不现实。因此，需要一种能够在推理时通过简单提示词修改即可实现偏好组合控制的轻量机制。

这两个动机分别对应本文提出的 **MapReduce LoRA** 框架和 **Reward-aware Token Embedding (RaTE)** 方法，共同构成了推进多偏好优化帕累托前沿的完整解决方案。

## 核心方法与创新机理

MapReduce LoRA 的核心创新在于将多偏好优化重新表述为一个 **Map-Reduce 迭代范式**，并通过 **奖励感知令牌嵌入（RaTE）** 实现推理时的灵活偏好控制。这两项设计直接回应了现有方法在联合优化多个奖励模型时面临的“对齐税”瓶颈——即提升某一维度时其他维度性能下降，导致帕累托前沿难以推进。

### 从一次性合并到渐进式迭代逼近

现有后验方法（如 **Rewarded Soup**）将多个奖励特定专家一次性加权平均，本质上是单步参数空间插值，缺乏对联合最优解的收敛保证。先验方法（如 **CaPO**）则通过固定加权和联合训练，在优化初期就引入目标间冲突，限制了各维度的充分探索。MapReduce LoRA 将这一过程分解为交替执行的 **Map 阶段**与 **Reduce 阶段**：

- **Map 阶段**：从当前合并模型出发，并行训练多个奖励特定的 LoRA 专家，每个专家仅优化单一奖励函数。这等价于在局部执行近端优化步骤：

  $$\theta_i^k = \arg\max_{\theta} \left( f_i(\theta) - \frac{1}{2\eta} \|\theta - \theta^k\|^2 \right)$$

- **Reduce 阶段**：将各专家权重按用户指定系数加权平均并合并，作为下一轮迭代的初始参数：

  $$\theta^{k+1} = \frac{1}{n} \sum_{i=1}^{n} \theta_i^k$$

这一迭代平均过程被论文形式化为 **渐进式模型汤（progressive souping）**，本质上是平均近端共识优化。理论分析证明，当各目标函数满足局部光滑和 PL（Polyak-Łojasiewicz）条件时，迭代合并以几何速率收缩到联合最优解：

$$\|F(\theta^{k+1}) - F^*\| \leq (1 - c\eta\mu) \|F(\theta^k) - F^*\|$$

这一收敛性质是一次性模型汤所不具备的。消融实验直接验证了迭代次数的关键作用：在固定总训练步数下，将合并次数从 $k=1$ 增加到 $k=4$ 再到 $k=10$，GenEval、PickScore 和 OCR 三项指标持续提升，且合并带来的性能退化逐步减小（Figure 6）。扩展到 5 个奖励时，MapReduce LoRA 仍能同时提升所有指标（+22% GenEval，+3% PickScore，+44% OCR，+6% VQAScore，+7% MPS），且性能随合并次数递增，未出现递减趋势（Figure 11）。

### 从切换适配器到令牌级偏好组合

现有方法在推理时切换偏好通常需要替换整个 LoRA 适配器或重新训练，灵活性差且计算开销大。RaTE 将每个偏好专家蒸馏为 **单个可学习的特殊令牌嵌入**，通过 Flow Matching 目标训练：

$$\mathcal{L}(\theta_{\text{token}_i}) = \mathbb{E}_{p, z_{0,i}^{\text{teacher}}, \epsilon, t} \left[ \left\| M(z_t, t, c(p, \theta_{\text{token}_i})) - v_{\text{target}} \right\|_2^2 \right]$$

在推理时，用户只需向提示词附加对应偏好令牌（如 `<GE>`、`<PS>`、`<OCR>`），即可在不修改基础模型的情况下实现多偏好的灵活组合控制（Figure 5）。令牌数量消融显示，不同奖励对令牌数量敏感度各异：GenEval 在 2-3 个令牌时饱和，PickScore 在 1 个令牌时最优，OCR 在 3 个令牌时最优（Table 4）。RaTE 的一个已知局限是对联合文本-图像序列建模架构（如 FLUX.1-dev）的稳定性较差，需要探索模型无关的设计方案。

### 与基线的关键差异总结

| 设计维度 | 现有方法 | MapReduce LoRA |
|---------|---------|---------------|
| 多奖励优化策略 | 单次平均（Rewarded Soup）或固定加权联合优化（CaPO） | 多轮 Map-Reduce 迭代，渐进逼近联合最优 |
| 推理时偏好控制 | 无或需切换整个 LoRA 适配器 | RaTE 令牌嵌入，附加到提示词即可组合控制 |
| 收敛保证 | 一次性合并无收敛保证 | 局部 PL 条件下几何速率收敛 |
| 扩展性 | 奖励增多时冲突加剧 | 5 个奖励下仍持续提升所有指标 |

MapReduce LoRA 的核心设计是将多偏好优化分解为两个正交的协作机制：**迭代权重合并（MapReduce LoRA）** 负责在训练阶段持续推进帕累托前沿，**奖励感知令牌嵌入（RaTE）** 负责在推理阶段实现轻量、可组合的偏好控制。二者共享同一组奖励特定 LoRA 专家，但作用于模型生命周期的不同阶段。

### 训练管线：Map 与 Reduce 的迭代循环

整个训练管线围绕一个冻结的基础生成模型 $M$ 展开，所有可训练参数仅存在于 LoRA 低秩适配器 $\Delta W = BA$ 中。管线包含三个核心模块：

1. **Map 阶段（并行专家训练）**：给定 $n$ 个奖励模型 $R_1, \dots, R_n$，从当前共享基础模型 $\theta^k$ 出发，并行训练 $n$ 个奖励特定的 LoRA 专家。每个专家 $\theta_i^k$ 使用 GRPO（Group Relative Policy Optimization）目标独立优化其对应的奖励函数：
   $$
   \mathcal{I}_{\mathrm{GRPO}} = \mathbb{E}_{p} \left[ \frac{1}{G} \sum_{g=1}^{G} \frac{1}{T} \sum_{t=1}^{T} \min\left( r_{t}^{g} \hat{A}^{g}, \exp(r_{t}^{g}, 1-\epsilon, 1+\epsilon) \hat{A}^{g} \right) \right] - \beta D_{KL}\left( \pi_{\theta}(\cdot|p) \| \pi_{\mathrm{ref}}(\cdot|p) \right)
   $$
   其中优势函数 $\hat{A}^{g}$ 通过组内 z-score 标准化计算。这一阶段将多目标联合优化问题解耦为 $n$ 个独立的单目标 proximal 优化步骤。

2. **Reduce 阶段（加权平均与合并）**：按用户指定的偏好系数对 $n$ 个专家权重进行加权平均，得到新一轮的共享基础模型 $\theta^{k+1} = \frac{1}{n} \sum_{i=1}^{n} \theta_i^k$。这一操作在数学上等价于平均近端共识优化的一次迭代，将各专家向联合最优方向拉近。

3. **迭代合并循环**：将 Reduce 阶段输出的合并模型作为下一轮 Map 阶段的初始参数，重复上述过程 $K$ 次。理论分析表明，当各奖励目标满足局部光滑和 PL（Polyak-Łojasiewicz）条件时，该渐进式合并以几何速率收缩至联合最优：
   $$
   ||F(\theta^{k+1}) - F^{*}|| \leq (1 - c \eta \mu) ||F(\theta^{k}) - F^{*}||
   $$
   其中 $F(\theta) = \frac{1}{n} \sum_{i=1}^{n} f_i(\theta)$ 为多奖励联合目标。这一收敛性质是 MapReduce LoRA 区别于一次性模型汤（Rewarded Soup）的核心理论优势——后者仅执行单次平均，无法利用迭代带来的渐进改进。

Figure 3 给出了上述流程与单专家训练（Flow-GRPO）及多目标强化学习基线（CaPO、Rewarded Soup）的对比：单专家方法仅优化单一奖励，无法平衡多目标；CaPO 在训练中固定加权联合优化，灵活性受限；Rewarded Soup 在训练后一次性合并，缺乏迭代精炼。MapReduce LoRA 通过“训练-合并-再训练”的循环，使模型在每一轮中都能从上一轮的合并结果出发，逐步逼近更优的帕累托前沿。

![[assets/figures/papers/paper_list_l2692_https_arxiv_org_abs_2511_20629/figures/003_Figure_3.jpg]]
*Figure 3: Overview of MapReduce LoRA and comparison with (a) individual experts, e.g., Flow-GRPO [26], and (b) Multi-Objective Reinforcement Learning, e.g., CaPO [21] and Rewarded soup [36]. All methods begin from a base model M and optimize with respect to reward R. Our proposed MapReduce LoRA iteratively trains per-reward LoRA experts and initializes iteration k + 1 using the merged model from iteration k. Notably, the black dashed curve for MapReduce LoRA indicates fewer training steps compared with the black solid curves representing other methods*

### 推理管线：RaTE 的偏好组合控制

训练完成后，MapReduce LoRA 产出一组奖励特定 LoRA 专家。RaTE 将这些专家的行为蒸馏到可组合的令牌嵌入中，实现推理时的灵活偏好控制：

1. **RaTE 训练**：为每个奖励 $R_i$ 学习一个特殊的令牌嵌入 $\theta_{\mathrm{token}_i}$（如 `<GE>` 对应 GenEval，`<PS>` 对应 PickScore，`<OCR>` 对应 OCR）。训练目标为 Flow Matching 的 MSE 损失：
   $$
   \mathcal{L}(\theta_{\mathrm{token}_{i}}) = \mathbb{E}_{p, z_{0,i}^{\mathrm{teacher}}, \epsilon, t} \left[ \left|\left| M(z_{t}, t, c(p, \theta_{\mathrm{token}_{i}})) - v_{\mathrm{target}} \right|\right|_{2}^{2} \right]
   $$
   其中教师信号 $v_{\mathrm{target}}$ 来自对应的奖励特定 LoRA 专家，仅更新令牌嵌入而冻结模型其余部分。

2. **推理时组合**：用户只需在提示词中附加相应的偏好令牌（如 `"a cat <GE><PS>"`），即可在无需切换模型或重新训练的情况下，组合多个偏好的控制效果。Table 3 的实验结果验证了这种令牌级控制的有效性——不同令牌组合可灵活调节各奖励维度的表现。

### 输入输出流与模块关系

- **输入**：冻结的基础生成模型 $M$、$n$ 个奖励函数、用户偏好权重向量、训练提示词集。
- **Map 阶段输出**：$n$ 个奖励特定 LoRA 专家权重。
- **Reduce 阶段输出**：合并后的共享基础模型，作为下一轮迭代的起点。
- **迭代循环输出**：经过 $K$ 轮精炼的最终合并模型，同时保留各轮专家用于 RaTE 蒸馏。
- **RaTE 训练输出**：$n$ 个偏好令牌嵌入，可独立于 LoRA 权重使用。
- **推理输入**：用户提示词 + 可选偏好令牌组合；**推理输出**：受控生成的图像、视频或文本。

两个机制在模块关系上形成互补：MapReduce LoRA 在训练时通过迭代合并逼近全局帕累托最优，RaTE 在推理时通过令牌嵌入提供细粒度的偏好调节能力。消融实验（Figure 6）表明，增加合并迭代次数 $K$ 可持续提升三项奖励指标并减小合并带来的性能退化；Table 4 的令牌数量消融则揭示了不同奖励的最佳令牌数量配置（GenEval 在 2-3 个令牌时饱和，PickScore 在 1 个令牌时最优，OCR 在 3 个令牌时最优）。

### 3.1 基础组件：LoRA 与 GRPO

MapReduce LoRA 构建在两个基础组件之上：低秩适配（LoRA）和组相对策略优化（GRPO）。

**LoRA 低秩适配**。对于预训练权重 $W$，LoRA 学习一个低秩更新 $\Delta W = BA$，其中 $A$ 和 $B$ 为低秩矩阵。适配后的层计算为：

$$(W + \Delta W) x = W x + B A x$$

冻结 $W$，仅训练 $A$ 和 $B$，大幅减少可训练参数量。本文在所有实验中均使用 LoRA 而非全参数微调，以保证各方法间的公平比较。

**GRPO 目标函数**。GRPO 是一种用于生成模型微调的强化学习目标，通过组内奖励归一化来估计优势。其损失函数为：

$$\mathcal{I}_{\mathrm{GRPO}} = \mathbb{E}_{p} \left[ \frac{1}{G} \sum_{g=1}^{G} \frac{1}{T} \sum_{t=1}^{T} \min\left( r_{t}^{g} \hat{A}^{g}, \exp(r_{t}^{g}, 1-\epsilon, 1+\epsilon) \hat{A}^{g} \right) \right] - \beta D_{KL}\left( \pi_{\theta}(\cdot|p) \| \pi_{\mathrm{ref}}(\cdot|p) \right)$$

其中，$p$ 为提示词，$G$ 为组大小，$T$ 为序列长度，$r_t^g$ 为似然比，$\epsilon$ 为裁剪参数，$\beta$ 控制 KL 惩罚强度，$\pi_\theta$ 和 $\pi_{\mathrm{ref}}$ 分别为当前策略和参考策略。

**优势归一化**。组内优势通过 z-score 标准化计算：

$$\hat{A}^{g} = \frac{ R( y^{g}, p ) - \operatorname{mean}[ R( y^{g}, p ) ]_{g=1}^{G} }{ \mathrm{std}[ R( y^{g}, p ) ]_{g=1}^{G} }$$

其中 $R(y^g, p)$ 为第 $g$ 组生成样本的奖励分数。该归一化消除了不同奖励模型间的尺度差异，使训练更稳定。

### 3.2 MapReduce LoRA：渐进式合并优化

**问题形式化**。多偏好优化的目标是联合最大化 $n$ 个奖励函数。将问题转化为最小化形式，定义联合目标为各奖励函数的简单平均：

$$F(\theta) = \frac{1}{n} \sum_{i=1}^{n} f_{i}(\theta)$$

其中 $f_i(\theta)$ 对应第 $i$ 个奖励的负奖励函数。

**Map 阶段**。在第 $k$ 轮迭代中，以当前共享参数 $\theta^k$ 为起点，并行训练 $n$ 个奖励特定的 LoRA 专家。每个专家 $\theta_i^k$ 通过 GRPO 优化其对应的奖励函数 $f_i$。从优化视角看，这等价于执行一步近端优化：

$$\theta_{i}^{k} = \mathrm{prox}_{\eta f_{i}}(\theta^{k}) = \arg\max_{\theta} \left( f_{i}(\theta) - \frac{1}{2\eta} ||\theta - \theta^{k}||^{2} \right)$$

其中 $\eta > 0$ 为步长参数，近端项约束专家偏离当前共享参数的程度。

**Reduce 阶段**。将 $n$ 个专家的 LoRA 权重按用户指定的偏好系数加权平均，合并回基础模型，作为下一轮的初始参数：

$$\theta^{k+1} = \frac{1}{n} \sum_{i=1}^{n} \theta_{i}^{k}$$

这一“渐进式模型汤”（progressive souping）过程是 MapReduce LoRA 的核心创新。与一次性模型汤（Rewarded Soup）不同，迭代合并允许模型在每轮中重新探索，逐步逼近联合最优。

**收敛性保证**。当各奖励函数 $f_i$ 满足局部光滑性和 Polyak-Łojasiewicz (PL) 条件时，渐进式合并以几何速率收敛到联合最优 $F^*$：

$$||F(\theta^{k+1}) - F^{*}|| \leq (1 - c \eta \mu) ||F(\theta^{k}) - F^{*}||$$

其中 $\mu$ 为 PL 常数，$c > 0$ 为与光滑性相关的常数。该收缩界从理论上解释了为什么增加合并迭代次数能持续提升性能——每轮迭代将次优间隙按固定比例压缩。

### 3.3 RaTE：奖励感知令牌嵌入

**动机**。MapReduce LoRA 的合并模型固定了各偏好的权重比例，无法在推理时灵活调整。RaTE 将每个偏好专家蒸馏为一个可学习的特殊令牌嵌入，通过向提示词附加令牌实现推理时偏好组合控制。

**蒸馏损失**。对于第 $i$ 个奖励的专家，RaTE 使用 Flow Matching 的均方误差损失，将专家知识转移到令牌嵌入 $\theta_{\mathrm{token}_i}$ 中：

$$\mathcal{L}(\theta_{\mathrm{token}_{i}}) = \mathbb{E}_{p, z_{0,i}^{\mathrm{teacher}}, \epsilon, t} \left[ \left|\left| M(z_{t}, t, c(p, \theta_{\mathrm{token}_{i}})) - v_{\mathrm{target}} \right|\right|_{2}^{2} \right]$$

其中 $M$ 为流匹配模型，$z_t$ 为时间步 $t$ 的噪声潜变量，$c(p, \theta_{\mathrm{token}_i})$ 为附加了偏好令牌的提示词条件，$v_{\mathrm{target}}$ 为专家模型预测的目标速度场。训练时仅更新 $\theta_{\mathrm{token}_i}$，冻结模型其余部分。

**推理时组合**。推理时，用户可将多个偏好令牌（如 `<GE>`、`<PS>`、`<OCR>`）同时附加到提示词中，实现灵活的多偏好控制，无需切换模型或重新训练。

## 实验与关键发现

### 核心瓶颈与因果机制

联合优化多个奖励模型时，现有方法面临显著的对齐税（alignment tax）：提升某一维度（如美学质量）往往导致其他维度（如文本渲染准确性）下降。加权和（如 **CaPO**）或一次性模型合并（如 **Rewarded Soup**）无法有效平衡冲突目标，帕累托前沿推进困难。MapReduce LoRA 的核心机制是将多目标分解为并行训练奖励特定 LoRA 专家（Map 阶段）并迭代合并（Reduce 阶段），通过渐进取平均（progressive souping）逐步逼近联合最优。理论分析表明，在目标函数满足局部光滑和 PL 条件时，迭代合并以几何速率收敛至联合最优，收敛界为 $\|F(\theta^{k+1}) - F^{*}\| \leq (1 - c \eta \mu) \|F(\theta^{k}) - F^{*}\|$，优于一次性模型汤。

### 文本到图像主结果

Table 1 报告了在 SD 3.5 Medium 和 FLUX.1-dev 上的全面对比。MapReduce LoRA + RaTE 在 SD 3.5 M 上实现 GenEval 0.92（基线的 0.68，+36.1%）、PickScore 22.777（+4.6%）、OCR 0.936（+55.7%）；在 FLUX.1-dev 上 GenEval 0.89（+32.7%）、PickScore 22.951（+4.3%）、OCR 0.957（+67.1%）。域外奖励（VQAScore、MPS、VILA）同样全面提升，表明方法未过拟合训练奖励。与单专家 Flow-GRPO 相比，MapReduce LoRA 在所有三项指标上均超越或持平各自专家上界，同时避免了单专家在其他维度上的性能塌陷。

![[assets/figures/papers/paper_list_l2692_https_arxiv_org_abs_2511_20629/figures/005_Table_1.jpg]]
*Table 1: Text-to-Image performance comparison on in-domain rewards (GenEval [14], PickScore [18], and OCR [8]) within corresponding datasets and out-of-domain rewards (VQAScore [24], MPS [47], and VILA [17]) within PartiPrompts [46] and GenAI-Bench [22]. The performance is evaluated with fp32 precision. Red color means the performance is degraded compared to the baseline*

### 文本到视频与语言任务

在 HunyuanVideo 上（Table 2），MapReduce LoRA 将视觉质量从 3.25 提升至 4.81（+48.1%），运动质量从 0.95 提升至 1.81（+90.0%），且优于单独训练的专家。语言任务方面，在 Reddit Summary 和 Helpful Assistant（Llama-2 7B）上，MapReduce LoRA 均推进了帕累托前沿，其中 Helpful 提升 43.4%，Harmless 提升 136.7%，验证了方法的跨模态通用性。

![[assets/figures/papers/paper_list_l2692_https_arxiv_org_abs_2511_20629/figures/008_Table_2.jpg]]
*Table 2: Text-to-Video comparison on Visual and Motion Quality*

### 帕累托前沿对比

Figure 10 和 Table 5、Table 6 展示了与 Rewarded Soup 和 MORL-D 的 3D/2D 帕累托前沿对比。MapReduce LoRA 在所有合并比例下均支配（dominate）基线方法，尤其在 PickScore 维度上，Rewarded Soup 和 MORL-D 提升有限甚至退化，而 MapReduce LoRA 持续扩大前沿覆盖范围。Figure 9 进一步验证了在 SD 3.5 M、FLUX.1-dev 和 HunyuanVideo 上的非支配解分布。

![[assets/figures/papers/paper_list_l2692_https_arxiv_org_abs_2511_20629/figures/015_Table_5.jpg]]
*Table 5: 3D merging results on Text-to-Image tasks: SD 3.5 M [2] and FLUX.1-dev [20]*

![[assets/figures/papers/paper_list_l2692_https_arxiv_org_abs_2511_20629/figures/017_Figure_10.jpg]]
*Figure 10: Merging performance comparison across Rewarded Soup [36], MORL-D, and MapReduce LoRA. Left: 3D Pareto-front comparison. Right: 2D projections of the 3D Pareto front (for readability), which are not 2D Pareto fronts. Unlike Fig. 9, these are projections rather than a 2D merge with the third reward fixed to 0. MORL-D performance is confined to a small region across the three rewards and yields only limited improvement on PickScore*

### 关键消融实验

**合并迭代次数**（Figure 6）：在固定总训练步数下，将合并次数从 k=1 增至 k=4 再至 k=10，GenEval、PickScore 和 OCR 三项指标持续提升，且合并带来的性能退化逐步减小。这直接支持了迭代合并的渐进收敛理论。

**RaTE 令牌数量**（Table 4）：GenEval 在 2-3 个令牌时饱和，PickScore 在 1 个令牌时最优，OCR 在 3 个令牌时最优。表明不同偏好对令牌容量的需求存在差异，但总体在极少令牌（1-3 个）下即可实现有效控制。

**奖励数量扩展**（Figure 11）：将奖励扩展至 5 个（GenEval、PickScore、OCR、VQAScore、MPS），MapReduce LoRA 仍能提升所有奖励（+22%、+3%、+44%、+6%、+7%），且性能随合并次数（1→3）提升，无明显递减趋势，初步验证了方法的可扩展性。

### RaTE 推理时控制

Table 3 展示了 RaTE 的令牌组合控制效果。通过附加不同偏好令牌（`<GE>`、`<PS>`、`<OCR>`），可在推理时灵活调节各维度性能，无需切换模型或重训。例如，仅附加 `<GE>` 令牌时 GenEval 最高但 PickScore 较低，组合 `<GE>+<PS>+<OCR>` 则实现三项均衡最优。Figure 5 提供了定性示例，展示同一提示词下通过不同令牌组合控制生成风格和文本渲染质量。

### 局限与失败模式

1. **大规模偏好扩展**：目前仅验证至 5 个偏好，更多偏好下的计算成本和合并退化需进一步研究。
2. **合并策略固化**：默认采用均匀加权和固定合并频率，自适应或学习的合并策略可能带来额外收益。
3. **RaTE 架构兼容性**：RaTE 在 SD 等使用显式交叉注意力的模型上有效，但在 FLUX.1-dev 等联合文本-图像序列模型上稳定性较差，需要探索模型无关的偏好注入设计。
4. **域外泛化边界**：虽然域外奖励有提升，但提升幅度（如 VILA +3.0%）小于域内奖励，长尾偏好的泛化能力需进一步验证。

![[assets/figures/papers/paper_list_l2692_https_arxiv_org_abs_2511_20629/figures/007_Figure_6.jpg]]
*Figure 6: Ablation study on merging iterations (k = 1 vs. 4 vs. 10). The performance is evaluated during training with mixed precision, where the text encoder is set to fp16 precision and the rest of the model to fp32*

## 定位与知识库关联

### 1. 问题定位：多偏好优化中的“对齐税”瓶颈

当前生成模型的多偏好对齐面临一个核心瓶颈：**联合优化多个奖励模型时，现有方法无法有效平衡冲突目标，导致“对齐税”——提升某一维度性能时其他维度显著下降，帕累托前沿推进困难。** 这一瓶颈的根源在于不同奖励函数之间存在内在冲突（例如，图像美学质量与文本渲染准确性往往此消彼长），而现有策略在协调这些冲突时存在结构性缺陷。

### 2. 方法谱系：从单奖励到多奖励优化的演进

MapReduce LoRA 的方法设计处于多目标偏好优化方法谱系中的一个特定位置，其与现有工作的关系可从以下维度进行定位：

#### 2.1 单奖励专家训练（性能上界基线）

**Flow-GRPO** 作为单奖励 LoRA 专家训练方法，为每个偏好维度独立训练一个适配器，代表了该维度的性能上界。然而，这种方法无法同时满足多个偏好——切换偏好需要更换整个 LoRA 模块，且不同专家之间存在性能冲突。MapReduce LoRA 的 Map 阶段继承了这一单奖励训练范式，但将其作为迭代优化的子步骤而非最终方案。

#### 2.2 先验多目标联合优化（固定加权策略）

**CaPO** 代表了一类先验多目标优化方法，通过在训练过程中使用固定权重将多个奖励组合为单一目标进行联合优化。这类方法的核心局限在于：**固定的加权系数无法灵活适应推理时不同的偏好需求，且权重选择对最终性能高度敏感。** 实验证据表明（Figure 10, Table 5-6），CaPO 在 PickScore 上的提升有限，未能有效推进帕累托前沿。MapReduce LoRA 通过迭代合并策略绕开了固定加权的限制，同时配合 RaTE 实现推理时的灵活偏好组合。

#### 2.3 后验模型合并（一次性平均策略）

**Rewarded Soup** 采用后验模型汤策略：先独立训练多个奖励专家，再通过一次性权重平均进行合并。这一方法的问题在于：**单次平均无法处理专家间的非线性冲突，合并后的模型往往在多个维度上均出现性能退化。** 理论分析（Section 3.2, Eqn. 7-8）证明，在目标函数满足局部光滑和 PL 条件时，一次性平均缺乏收敛保证，而迭代合并（渐进取平均）以几何速率收缩至联合最优：
$$
\|F(\theta^{k+1}) - F^{*}\| \leq (1 - c \eta \mu) \|F(\theta^{k}) - F^{*}\|
$$
实验证据（Figure 10, Table 5-6）直接验证了这一理论优势：MapReduce LoRA 在 3D 和 2D 帕累托前沿上均显著优于 Rewarded Soup。

#### 2.4 多目标强化学习基线（混合数据/混合奖励）

**MORL-D** 和 **MORL-DR** 分别采用混合数据和混合奖励的策略进行多目标 RL 训练。这些方法的不足在于：**直接联合优化时，梯度冲突导致优化过程不稳定，难以同时提升所有奖励维度。** Figure 10 的帕累托前沿对比显示，MORL-D 在 PickScore 上的提升同样有限，其非支配解集明显劣于 MapReduce LoRA。

### 3. 核心机制差异：迭代合并 vs. 一次性合并

MapReduce LoRA 与上述方法的关键区别在于其 **Map-Reduce 迭代框架**：

| 方法 | 合并策略 | 收敛性质 | 推理时偏好控制 |
|------|---------|---------|--------------|
| Flow-GRPO | 无合并（单专家） | 仅优化单奖励 | 需切换整个 LoRA |
| CaPO | 训练时固定加权 | 依赖权重选择 | 无灵活控制 |
| Rewarded Soup | 一次性后验平均 | 无收敛保证 | 需重新合并 |
| MORL-D/R | 训练时混合 | 梯度冲突不稳定 | 无灵活控制 |
| **MapReduce LoRA + RaTE** | **迭代渐进取平均** | **几何速率收敛** | **令牌嵌入组合控制** |

迭代合并的核心优势在于：每一轮 Reduce 阶段将专家权重加权平均并合并到基础模型，作为下一轮 Map 阶段的初始化参数。这一过程相当于执行平均近端共识优化（averaged proximal consensus optimization），使得模型在多个奖励函数之间逐步逼近联合最优。消融实验（Figure 6）直接验证了这一机制的有效性：**增加合并迭代次数（k=1→4→10）在固定总训练步数下持续提升 GenEval、PickScore 和 OCR 三项指标，且减小了合并带来的性能退化。**

### 4. RaTE 的独特定位：推理时偏好控制

RaTE（Reward-aware Token Embedding）在方法谱系中填补了一项空白：**在不修改基础模型的情况下实现推理时的灵活偏好组合控制。** 与需要切换整个 LoRA 适配器的方案不同，RaTE 将每个偏好专家的知识蒸馏到特殊令牌嵌入中，通过向提示词附加令牌即可组合多种偏好：
$$
\mathcal{L}(\theta_{\mathrm{token}_{i}}) = \mathbb{E}_{p, z_{0,i}^{\mathrm{teacher}}, \epsilon, t} \left[ \left\| M(z_{t}, t, c(p, \theta_{\mathrm{token}_{i}})) - v_{\mathrm{target}} \right\|_{2}^{2} \right]
$$
Table 3 的实验结果表明，不同令牌组合可以灵活调节各项指标的表现，验证了 RaTE 的偏好控制能力。

### 5. 适用边界与局限

#### 5.1 已验证的适用边界

- **模态范围**：文本到图像（SD 3.5 Medium, FLUX.1-dev）、文本到视频（HunyuanVideo）、语言任务（Llama-2 7B），跨模态有效性已得到验证。
- **奖励数量**：已验证至 5 个奖励（Figure 11），在 5 个奖励下仍能提升所有指标（+22% GenEval, +3% PickScore, +44% OCR, +6% VQAScore, +7% MPS），且性能随合并次数提升，无明显递减趋势。
- **基础架构**：基于 LoRA 的参数高效微调范式，适用于支持低秩适配的生成模型。

#### 5.2 已知局限

1. **扩展到更多偏好**：目前仅验证到 5 个偏好，更大数量（数十个）偏好的扩展性需要进一步研究，计算成本可能成为瓶颈。
2. **合并策略与调度**：本文默认使用均匀平均和固定合并频率，自适应或学习的合并策略（根据奖励冲突程度动态调整权重和频率）可能带来额外收益。
3. **RaTE 的架构依赖性**：RaTE 在 Stable Diffusion 等使用显式交叉注意力的模型上有效，但在 FLUX.1-dev 等联合文本-图像序列建模架构上稳定性较差，需要探索模型无关的设计。

### 6. 开放问题

1. **可扩展性**：如何将 MapReduce LoRA 扩展到数十个甚至更多奖励模型而不过度增加计算成本？是否需要引入奖励分组或层次化合并策略？
2. **自适应合并**：能否设计一种自适应合并策略，根据奖励冲突程度动态调整合并权重和频率，以进一步优化帕累托前沿？
3. **RaTE 架构泛化**：在联合文本-图像序列建模架构上的 RaTE 稳定化方法是什么？是否需要修改令牌注入机制或训练目标？
4. **知识遗忘**：迭代合并过程中是否可以引入正则化或约束，以进一步保证合并后的模型不会遗忘已学到的部分知识？
5. **理论边界**：在非凸或非 PL 条件下，迭代合并的收敛性质如何？是否存在理论上的最优合并频率？

### 7. 知识库定位总结

MapReduce LoRA 在多偏好优化方法谱系中占据了一个独特位置：**它通过迭代 Map-Reduce 框架架起了单奖励专家训练与多目标联合优化之间的桥梁，同时以 RaTE 提供了轻量级的推理时偏好控制机制。** 其理论根基（平均近端共识优化的几何收敛）与实验证据（跨模态、跨奖励数量的帕累托前沿推进）共同支撑了该方法在多偏好生成模型对齐领域的贡献。与现有方法的对比清晰表明，迭代合并策略是突破“对齐税”瓶颈的关键机制，而 RaTE 则解决了实际部署中的灵活控制需求。

## 原文 PDF

![[paperPDFs/CVPR_2026/MapReduce_LoRA_Advancing_the_Pareto_Front_in_Multi_Preference_Optimization_for_Generative_Models.pdf]]
