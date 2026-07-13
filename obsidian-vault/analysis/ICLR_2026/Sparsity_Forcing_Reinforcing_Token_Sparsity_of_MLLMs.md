---
title: "Sparsity Forcing: Reinforcing Token Sparsity of MLLMs"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Sparsity_Forcing_Reinforcing_Token_Sparsity_of_MLLMs.pdf
project_link: null
code_link: null
aliases:
- SF
- SFRTSM
tags:
- ICLR_2026
- topic/other_unclear
- topic/other_unclear/general
core_operator: "通过多预算 rollout 探索最小必要 token 集，并使用 GRPO 联合优化答案正确性与 token 减少率，直接将 token 节省作为端到端优化目标。"
primary_logic: "将 token 节省转化为端到端、推理一致的优化目标，通过对比不同预算的 rollout 奖励来动态确定最小必要 token 集，从而在极低 token 比下仍能保持准确性。"
claims:
- "Sparsity Forcing 大幅提升了 MLLM 的 token 减少率，在 Qwen2/2.5-VL 上从约 20% 提高到 75%，同时准确性下降极小。"
- "在 13 个图像和视频基准测试中，Sparsity Forcing 仅保留约 25% token，平均准确率与全量模型接近（如 Qwen2.5-VL-7B 图像 Avg. 73.6 vs Full 73.8）。"
- "与训练后稀疏增强方法相比，Sparsity Forcing 在 token 比 26.4% 时达到 72.8 平均得分，显著优于 MOBA（66.6）、Sharpness loss（67.6）等方法。"
- "在长序列推理中，Sparsity Forcing 实现高达 3.3× 的解码加速和 3.0× 的内存节省，证明其实用性。"
---

# Sparsity Forcing: Reinforcing Token Sparsity of MLLMs

> [!tip] 核心洞察
> 将 token 节省转化为端到端、推理一致的优化目标，通过对比不同预算的 rollout 奖励来动态确定最小必要 token 集，从而在极低 token 比下仍能保持准确性。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 稀疏性强制：增强多模态大语言模型的 Token 稀疏性 |
| 英文题名 | Sparsity Forcing: Reinforcing Token Sparsity of MLLMs |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=gxNTP2eER3) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | Sparsity Forcing |
| Dataset | 7 Image Benchmarks Average (Qwen2.5-VL-7B), 6 Video Benchmarks Average (Qwen2-VL-7B), MME (Qwen2.5-VL-7B), VideoMME (Qwen2.5-VL-7B) |

> [!tip] 效果简介
> - 7 Image Benchmarks Average (Qwen2.5-VL-7B) 上，Accuracy 为 73.6，对比 73.8 (Full)，变化 -0.2。
> - 6 Video Benchmarks Average (Qwen2-VL-7B) 上，Accuracy 为 61.9，对比 62.1 (Full)，变化 -0.2。
> - MME (Qwen2.5-VL-7B) 上，Score 为 2286，对比 2303 (Full)，变化 -17。

## 概要

多模态大语言模型（MLLMs）在理解视觉内容时需要处理大量视觉 token，导致自注意力计算的开销随序列长度平方增长，成为长上下文推理的核心瓶颈。现有的无训练稀疏注意力方法（如 ZipVL、FastV）仅利用模型固有的稀疏性，无法在极低的 token 预算下保持准确性；而基于代理目标（如注意力锐度正则化）的稀疏增强方法缺少对 token 预算的直接控制，且训练与推理策略不一致，进一步限制了推理效率的提升。

**Sparsity Forcing** 提出了一种将 token 稀疏性强化为端到端优化目标的后训练框架。该方法不再依赖静态的剪枝规则或间接的代理信号，而是通过多预算 rollout 动态探索保持答案正确所需的最小 token 集，并利用分组相对策略优化（GRPO）直接最大化联合效率-性能奖励——该奖励在同一组 rollout 至少有一个正确答案时才激活效率项，“节省 token 但保持正确”的行为被奖励，而“低效或错误”的 rollout 则被压制。这一机制使得模型在训练过程中就能学会在极端的 token 压缩比下维持答案质量，且训练时使用的稀疏注意力和 KV 缓存管理与推理完全一致，消除了训练-推理 gap。

实验表明，Sparsity Forcing 将 MLLM（Qwen2/2.5‑VL 系列）的 token 保留比从约 20% 提升至 75%（即仅使用 25% token），在 13 个图像与视频基准上的平均准确率几乎与全量模型持平（如 Qwen2.5-VL-7B 图像平均 73.6 vs 全量 73.8），显著优于 MOBA、Sharpness loss 等后训练基线。在 LLaVA-Video-7B 上，长序列推理可实现最高 3.3× 的解码加速与 3.0× 的内存节省，证明其实际部署价值。然而，该方法在跨帧空间推理等场景下仍会出现准确性下降，且训练时间因多 rollout 而略长于 SFT 基线，这些局限有待进一步探索。



多模态大语言模型（MLLM）在处理高分辨率图像和长视频时面临高昂的计算成本，其核心瓶颈在于注意力机制的序列二次方复杂度。为缓解这一问题，稀疏注意力方法通过抛弃低重要性 token 来降低计算量，目前主要分为两类：推理时训练无关的剪枝方法（如 FastV、VisionZip、ZipVL）和训练后稀疏增强方法（如 MOBA、Sharpness loss）。然而，这些方法存在两个根本性局限。

**第一，现有稀疏注意力方法仅被动利用模型的固有稀疏性，无法在极低 token 预算下保持准确性。** 训练无关方法通常单次设定固定剪枝比例或阈值，缺乏对预算的主动控制；当 token 保留率压低至 30% 以下时，准确性急剧退化。例如，ZipVL 在 Qwen-VL 系列模型上虽可将 token 比例降至约 80%，但进一步压缩时会引发明显的性能崩塌。这暴露出一个关键缺口：模型自身并未内化“节省 token”这一目标，而是依赖外部硬性截断。

**第二，基于代理目标的训练后稀疏增强方法缺乏对 token 预算的直接约束，且训练与推理不一致。** 例如，通过增强注意力分布的锐度（Sharpness loss）或调节 Softmax 温度，模型在训练时可能表现出更高的稀疏性，但这些代理指标与实际的 token 节省量之间并非单调对应；同时，训练阶段常用的教师强制（teacher forcing）策略与推理时的自回归采样之间存在分布偏移，限制了极低预算场景下的效率收益。

上述瓶颈的本质在于：token 节省未被视作与答案正确性同等重要的端到端优化目标，因而模型无法在正确性与效率之间自主寻找到最经济的均衡点。为此，本文提出 **Sparsity Forcing**，将 token 节省转化为推理一致的强化学习奖励，并通过多预算 rollout 对比在正确前提下所能承受的最低 token 数。其核心动机在于：**通过对比不同 token 预算下的答案质量，模型可以在奖励信号的驱动下学习主动抛弃冗余 token，从而在不牺牲准确性的前提下大幅提升稀疏率。** 初步实验即表明，该方法将 Qwen2/2.5-VL 的 token 减少率从约 20% 提升至 75%，且在 13 个图像和视频基准上仅保留约 25% token 时，平均准确率与全量模型几乎持平，证明了端到端稀疏优化的可行性与优越性。



## 核心方法与创新机理

现有 token 稀疏注意力方法主要依赖模型自身的固有稀疏性（如 FastV、VisionZip）或基于代理目标的训练（如注意力锐度损失），缺乏对 token 预算的直接控制，且在训练与推理之间存在不一致，导致极低预算下准确率大幅下降。Sparsity Forcing 的核心创新在于将 token 节省这一目标**显式转化为端到端、推理一致的强化学习优化过程**，通过多预算 rollout 探索最小必要 token 集，并借助 GRPO 直接最大化正确性约束下的 token 减少率。相较于 baseline，其关键 changed slot 体现在以下四个层面。

- **训练范式：从静态剪枝到基于 GRPO 的稀疏性强化**  
  此前的稀疏方法多为训练无关的静态剪枝（ZipVL、Minference 等）或基于 SFT 的间接优化，缺乏对 token 预算的动态反馈。Sparsity Forcing 将 GRPO 引入 MLLM 的 token 稀疏优化，使模型在强化学习的框架下主动权衡效率与性能。训练时使用带稀疏注意力的策略模型，并以标准因果注意力的冻结模型作为参考模型，通过 KL 散度保持训练稳定（`Section 3.2`）。

- **优化目标：从代理信号到联合性能-效率奖励**  
  baseline 依赖注意力锐度（Sharpness loss）、温度调节等代理目标来诱导稀疏性，无法直接控制最终推理效率或保证准确率。Sparsity Forcing 设计了联合奖励函数 $r_i = r_{\text{per},i} + C \cdot r_{\text{eff},i}$，其中性能奖励度量答案正确性，效率奖励度量 token 减少率（见 `Eq.9`）。效率奖励仅在采样组中至少存在一个正确回答时才激活，确保模型不会为了减少 token 而牺牲正确性。

- **预算探索：从固定预算到多预算 rollout 的动态最小集搜索**  
  传统方法通常采用固定的 token 保留比（如 top-k 剪枝）。Sparsity Forcing 通过在同一输入上以不同 top-p 阈值（训练范围 $[0.94,0.975]$）生成多个 rollout，构造采样组（`Figure 1`）。组内通过 GRPO 对比不同预算回答的正确性与效率，对更高效的正确回答赋予正的相对优势，对低效或错误回答施加惩罚，从而**自适应地探索每个样本的最小必要 token 集**（核心洞察）。这种"低显著性 token 测试"使模型学会了在准确率不受损的前提下最大程度压缩 token 使用。

- **推理一致性：训练与推理使用相同的稀疏策略**  
  基于代理目标的训练常出现 teacher forcing 与自回归推理不一致的问题。Sparsity Forcing 在训练阶段直接部署与推理完全相同的 top-p 稀疏注意力和 KV 缓存管理方式，**消除了训练-推理偏差**，保障训练习得的稀疏行为在部署时被精确复现。这一设计使其在 13 个图像与视频基准上仅保留约 25% 的 token，平均准确率与全量模型几乎持平（如 Qwen2.5‑VL‑7B 图像 Avg. 73.6 vs Full 73.8），并带来最高 3.3× 解码加速和 3.0× 内存节省（`Figure 4(c)(d)`）。

上述创新共同构成了一个统一的后训练框架：**将 token 节省从间接目标升级为端到端的强化学习目标，使 MLLM 在保持精度的同时实现前所未有的 token 减少率**（在 Qwen‑VL 系列上从原来的约 20% 提升至 75%，`ABSTRACT`）。



![[assets/figures/papers/iclr26_0015_gxNTP2eER3_Sparsity_Forcing_Reinforcing_Token_Sparsity_of_M/figures/001_Figure_1.jpg]]
*Figure 1: Overview of the proposed Sparsity Forcing. We use an MLLM with sparse attention as a policy model, e.g., Qwen2-VL+ZipVL, and the original model with standard causal attention as the reference model. The sampling group is to explore the minimum token ratio required to maintain the current answer under different attention score retention thresholds p*

Sparsity Forcing 是一种基于强化学习的后训练框架，旨在多模态大语言模型（MLLM）中端到端地增强 token 稀疏性，其核心思想是将 token 节省转化为可直接优化的联合奖励，并通过多预算 rollout 探测最小必要 token 集，从而在保持准确性的前提下大幅降低参与注意力计算的 token 数量。图 1 给出了框架的整体结构，以下按模块对 pipeline 进行描述。

**1. 策略模型 (Policy Model)**  
采用带有稀疏注意力机制的 MLLM 作为可训练的 π_θ，例如 Qwen2‑VL 或 Qwen2.5‑VL 结合训练时使用的 top‑p 稀疏注意力策略（如 ZipVL）。该模型接收图像/视频和问题作为输入，在执行自回归生成时，根据注意力分数动态筛选 query 和 key token，仅保留累计注意力质量不低于 p 的 token 子集，从而控制实际参与计算的 token 比例。策略模型是强化学习优化的主体，其参数通过下游奖励信号进行更新。

**2. 参考模型 (Reference Model)**  
使用同一 MLLM 的冻结版本，但保留标准的因果注意力（无 token 剪枝），作为稳定训练的锚点。在 GRPO 损失中加入 KL 散度惩罚项，防止策略模型因稀疏性引入而偏离原始分布过远，从而缓解语言能力退化。

**3. 多预算 rollout 生成器 (Multi‑budget Rollout Generator)**  
对于每一个输入样本，策略模型以不同的 top‑p 阈值（训练时 p ∈ [0.94, 0.975]，步长 0.005）运行 N 次前向传播，生成一组回答序列 {o₁, o₂, …, o_N}。阈值 p 越小，保留的 token 越少，回答越精简；p 越大，保留的 token 越多，回答越接近全量模型。这种多预算 rollout 机制显式地探索了效率‑性能权衡空间，为后续奖励计算和策略更新提供对比信号（图 1 采样组部分，图 2 渐进式 top‑p 采样示意）。

**4. 联合奖励计算器 (Joint Reward Calculator)**  
对每一个 rollout 计算两个奖励分量：  
- **性能奖励 rₚₑᵣ, i**：根据回答是否正确赋分（例如通过规则匹配或字符串比较判定）。  
- **效率奖励 rₑff, i**：定义为 token 减少率，即 1 − (实际参与注意力计算的 token 数 / 原始输入 token 数)。效率奖励仅在**小组内至少存在一个正确回答时**激活，以避免模型在无法正确作答的情况下一味减少 token。  
最终每一样本的奖励为 rᵢ = rₚₑᵣ, i + C · rₑff, i，其中 C 为组级指示变量（组内有正确回答则为 1，否则为 0）。该设计确保模型只在掌握正确路径后才被鼓励提升稀疏性。

**5. GRPO 策略更新器 (GRPO Policy Updater)**  
在组内对所有奖励进行归一化，计算相对优势 Aᵢ。以裁剪的重要性采样比率和 KL 散度惩罚构成 GRPO 目标函数，更新策略模型参数 θ。优化方向是：给予高效且正确的回答更高的优势，抑制低效或错误的回答，同时在参考模型的约束下保持生成质量。训练后，推理时固定 p = 0.975，以在准确性和 token 减少率之间取得平滑折中。

**整体数据流**：输入样本 → 策略模型（稀疏注意力）→ 多预算 rollout（N 个不同 p）→ 回答序列和 token 使用统计 → 联合奖励（性能 + 门控效率奖励）→ 组内优势计算 → GRPO 损失（含 KL 惩罚）→ 反向传播更新 θ。参考模型仅用于计算 KL 散度，不参与梯度更新。整个训练过程将 token 稀疏性直接纳入端到端的优化回路，使模型学会在生成正确回答的同时自适应地压缩 token 预算，进而实现推理阶段的显著加速与内存节省。



Sparsity Forcing 通过强化学习将 token 节省端到端地纳入 MLLM 的优化目标，其核心由五个功能模块协同实现，关键公式则定义了稀疏注意力、奖励函数和策略更新的数学形式。

### 关键模块

- **策略模型（Policy Model）**  
  采用带稀疏注意力的 MLLM（例如 Qwen2‑VL + ZipVL），负责在多预算条件下生成回答序列并执行 token 级剪枝。训练中通过 top‑p 阈值控制注意力保留比例，推理时可固定为单一阈值以保证准确性。

- **参考模型（Reference Model）**  
  冻结的原始 MLLM（标准因果注意力），用于计算 KL 散度惩罚项，防止策略模型因引入强稀疏约束而产生过度分布偏移，从而稳定 RL 训练过程。

- **多预算 Rollout 生成器（Multi‑budget Rollout Generator）**  
  对同一输入，通过改变注意力得分保留阈值 $p$（例如在训练时 $p \in [0.94, 0.975]$）生成一组不同 token 预算的回答。该设计显式探索最小必要 token 集，使得模型能够学习在正确作答的前提下降低计算开销。

- **联合奖励计算器（Joint Reward Calculator）**  
  将性能奖励（答案正确性）与效率奖励（token 减少率）组合为单个奖励值，且仅在采样组内至少有一个正确回答时才激活效率奖励。具体形式为 $r_i = r_{\mathrm{per}, i} + C \cdot r_{\mathrm{eff}, i}$，其中 $C$ 是组级正确性指示器（公式 9）。这一门控机制确保模型在掌握任务后再追求效率，避免盲目削减 token 导致性能崩溃。

- **GRPO 策略更新器（GRPO Policy Updater）**  
  基于组内相对优势更新策略参数：对同一输入的一组回答，计算标准化优势（公式 10），然后通过含裁剪项的重要性采样和 KL 惩罚来最大化期望奖励（公式 11）。该设计无需显式配对偏好数据，直接利用 on‑policy 样本对比驱动策略向“准确且高效”的方向演进。

### 关键公式

Sparsity Forcing 的优化过程建立在以下核心公式之上（均取自原文 Section 3）。

**稀疏注意力输出**  
$$\hat{\mathbf{O}}_{\mathrm{sparse}} = \sigma\left( \frac{ ( {\mathbf{Q}} \odot {\mathbf{M}}_{Q} ) ( {\mathbf{K}} \odot {\mathbf{M}}_{K} ) ^ { \top } }{ \sqrt{d} } \right) {\mathbf{V}} \quad \text{(Eq. 2)}$$

其中 $\mathbf{Q}, \mathbf{K}, \mathbf{V}$ 分别为查询、键和值矩阵，$\mathbf{M}_Q, \mathbf{M}_K$ 为对应的二进制掩码，$\sigma$ 表示 softmax，$d$ 为键的维度。掩码决定了哪些 token 参与注意力计算，是控制稀疏性的基础操作。

**Top‑p 掩码优化问题**  
$$\mathbf{M}_{Q}^{*}, \mathbf{M}_{K}^{*} = \operatorname*{argmin}_{\mathbf{M}_{Q},\mathbf{M}_{K}} b, \quad \mathrm{s.t.} \sum_{i=1}^{\ell} \sum_{j=1}^{\ell} \left[ \sigma\left( \frac{\mathbf{Q}\mathbf{K}^{\top}}{\sqrt{d}} \right) \right]_{ij} ( \mathbf{m}_{Q} )_{i} ( \mathbf{m}_{K} )_{j} \geq \ell \times p \quad \text{(Eq. 3)}$$

该约束优化以最小化 token 预算 $b$ 为目标，要求保留的注意力质量总和不低于 $\ell \times p$（$p$ 为注意力保留阈值，$\ell$ 为序列长度）。通过求解该问题，可动态得到 Top‑p 稀疏掩码，实现根据注意力分布灵活调整保留 token 数量。

**联合奖励函数**  
$$r_{i} = r_{\mathrm{per}, i} + C \cdot r_{\mathrm{eff}, i} \quad \text{(Eq. 9)}$$

$r_{\mathrm{per}, i}$ 为答案正确性奖励（通常为 0/1 或基于规则评分），$r_{\mathrm{eff}, i}$ 为 token 减少率奖励，$C$ 为组内正确性指示器：当至少有一个 rollout 正确时 $C=1$，否则 $C=0$。这一设计使效率奖励仅在学习产生正确答案的基础上生效，避免以牺牲准确性为代价换取稀疏性。

**组内优势标准化**  
$$A_i = \frac{ r_i - \operatorname{mean}( r_1, r_2, \ldots, r_N ) }{ \operatorname{std}( r_1, r_2, \ldots, r_N ) } \quad \text{(Eq. 10)}$$

将同组 $N$ 个回答的奖励转换为相对优势，消除奖励尺度波动影响，使策略更新更稳定。

**GRPO 裁剪代理目标**  
$$\mathcal{I}(\theta) = \mathbb{E}_{ \mathbf{x} \sim \mathcal{X}, n \in \mathcal{U}([N]) } \left[ \left( \operatorname{min} \left( \frac{ \pi_{\theta} \left( \mathbf{o}_n \mid \mathbf{x} \right) }{ \pi_{\theta_{\mathrm{od}}} \left( \mathbf{o}_n \mid \mathbf{x} \right) } A_i, \kappa \left( \frac{ \pi_{\theta} \left( \mathbf{o}_n \mid \mathbf{x} \right) }{ \pi_{\theta_{\mathrm{od}}} \left( \mathbf{o}_n \mid \mathbf{x} \right) } \right) A_i \right) - \beta \mathbb{D}_{\mathrm{KL}} \left( \pi_{\theta} \| \pi_{\mathrm{ref}} \right) \right) \right] \quad \text{(Eq. 11)}$$

其中 $\pi_{\theta}$ 和 $\pi_{\theta_{\mathrm{od}}}$ 分别为当前和旧策略，$\kappa$ 为裁剪函数（如 clip to $[1-\epsilon, 1+\epsilon]$），$\beta$ 控制 KL 惩罚强度，$\mathbb{D}_{\mathrm{KL}}$ 度量策略分布差异，$\pi_{\mathrm{ref}}$ 为参考策略。该目标中的裁剪项保证更新步长可控，KL 惩罚项防止稀疏化导致的分布坍塌，整体驱动策略在保持回答质量的前提下最大化 token 节省。

上述方程共同构成了 Sparsity Forcing 的训练闭环：稀疏注意力提供可微的 token 剪枝基础，多预算 rollout 探索效率-性能边界，联合奖励与 GRPO 更新则端到端地强化最小必要 token 集的选择能力。



## 实验与关键发现

### 主结果与性能对比

实验在 7 个图像基准和 6 个视频基准上系统评估了 Sparsity Forcing 的性能‑效率权衡。在 Qwen2‑VL‑7B 图像评测上（表 1），Sparsity Forcing 仅保留约 23.6% 的 token 参与注意力计算，即取得 70.8 的平均得分，几乎完全匹配全量模型的 70.9；对更强的 Qwen2.5‑VL‑7B，保留 24.7% token 时平均分达到 73.6（全量 73.8），在 Qwen2.5‑VL‑3B 上亦能以 22.9% 的 token 比守住 68.7（全量 69.1）。视频理解场景（表 2）展现出同样的趋势：Qwen2‑VL‑7B 在 23.8% token 预算下平均 61.9（全量 62.1），LLaVA‑Video‑7B 以约 29% 的 token 比例获得 61.3（全量 62.2），表明该方法不受模态和模型大小的限制。

![[assets/figures/papers/iclr26_0015_gxNTP2eER3_Sparsity_Forcing_Reinforcing_Token_Sparsity_of_M/figures/003_Table_1.jpg]]
*Table 1: Performance comparisons with training-free sparse attention on 7 image benchmarks. Here, “Ratio” denotes the average proportion of tokens participating in attention computation over all benchmarks*

![[assets/figures/papers/iclr26_0015_gxNTP2eER3_Sparsity_Forcing_Reinforcing_Token_Sparsity_of_M/figures/004_Table_2.jpg]]
*Table 2: Performance comparisons with training-free sparse attention on 6 video benchmarks. For Minference (Jiang et al., 2024), we report a FLOPs-equivalent token ratio*

与训练后稀疏增强基线的对比（表 3）凸显了端到端优化的优势。在 Qwen2.5‑VL‑7B 上，Sparsity Forcing 仅使用 26.4% 的 token 即获得 72.8 的 5 项基准平均得分（分别达到 MME 2286、MMStar 62.5、ChartQA 83.1、VideoMME 64.0），显著优于 MOBA（66.6）、Sharpness loss（67.6）以及经 SP 微调的 ZipVL†（71.5）。其核心差异在于：Sparsity Forcing 将 token 节省纳入 GRPO 联合奖励 —— 性能奖励由答案正确性决定，效率奖励 $r_{\mathrm{eff}, i}$ 仅在组内至少存在一个正确回答时激活（Eq.9）—— 并采用多预算 rollout 动态探索最小必要 token 集，从而在强化学习过程中直接学习“用更少 token 答对题”。

![[assets/figures/papers/iclr26_0015_gxNTP2eER3_Sparsity_Forcing_Reinforcing_Token_Sparsity_of_M/figures/014_Table_3.jpg]]
*Table 3: Comparisons with baseline methods of enhancing token sparsity on Qwen2.5VL-7b. † denotes post-training MLLMs with ZipVL*

### 实际加速与内存节省

长序列推理的效率提升直接证实了 token 稀疏性的实际价值。在 LLaVA‑Video‑7B 上，Sparsity Forcing 相对于 FlashAttention-2 实现了最高 3.3× 的解码加速和 3.0× 的内存节省（图 4(c)(d)）。更值得关注的是，随着输入序列增长，保留 token 比例自适应下降，而准确率几乎不变（图 4(b)），说明优化后的模型习得了按需分配计算资源的能力。在推理侧，只需固定 top‑p 阈值为 0.975 即可在 24.1% 的 token 比下维持高准确率，为实际部署提供了便捷的静态配置。

![[assets/figures/papers/iclr26_0015_gxNTP2eER3_Sparsity_Forcing_Reinforcing_Token_Sparsity_of_M/figures/013_Figure_4.jpg]]
*Figure 4: (a) The effect of attention scores retention threshold p on token ratio and performance. (b) Accuracy and token budget with respect to increasing token sequence. (c)(d) Prefill latency and decoding memory usage under varying sequence lengths on LLaVA-Video-7b*

### 消融实验

消融实验验证了 Sparsity Forcing 各设计选择的必要性：

- **稀疏注意力类型**（表 4）：与 top‑k 和固定阈值剪枝相比，top‑p 策略在 24.1% token 比下获得最高的 MME（2286）和 VideoMME（64.0），其优势源于能够根据注意力分数的实时分布动态调整保留集合，避免固定预算下重要 token 被误剪。
- **训练超参数**（表 5）：top‑p 训练范围设为 [0.94, 0.975]、GRPO 组大小为 8 时，达到最优的性能‑效率权衡（MME 2286、VideoMME 64.0），进一步增大组规模或放宽 budget 范围未带来额外收益。
- **效率奖励设计**（表 6）：仅使用 token 减少率作为效率奖励时，LLaVA‑Video‑7B 六视频基准平均分为 61.3；额外加入硬件延迟奖励后几乎无变化（61.2），表明 token 预算本身即是一个足够有效的代理目标，无需依赖特定硬件的测量。
- **与温度调整 baseline 的比较**（表 8）：通过增大 Softmax 温度强制稀疏性的方法在中低预算下平均分仅为 67.4，而 Sparsity Forcing 在几乎相同的 token 比（26.4%）下达到 70.0，逼近全量模型的 70.2，进一步证明将 token 节省作为端到端优化目标远优于启发式代理损失。
- **训练成本**（表 7）：Sparsity Forcing 的训练耗时约为 110.4 小时（每 rollout 延迟 12.0s），虽高于基于 SFT 的 MOBA（75.6h / 11.6s），但考虑到显著的推理加速与精度保持，其性价比仍具竞争力。

![[assets/figures/papers/iclr26_0015_gxNTP2eER3_Sparsity_Forcing_Reinforcing_Token_Sparsity_of_M/figures/018_Table_4.jpg]]
*Table 4: Ablation study on different sparse attention with top-k, top-p, and threshold-based pruning. Table 5: Ablation study of different ranges of p and group sizes for training*

### 注意力分布的发展

训练前后注意力图的可视化（图 5）揭示了学习过程的机理：经过 Sparsity Forcing 后，MLLM 的注意力明显向更小的关键 token 子集集中，且不同层的最终稀疏度差异显著，高层可能保留更少的 token。这既验证了强化训练有效重塑了模型的注意力模式，也为未来分层设置差异化预算提供了依据。

### 失败模式与局限

尽管整体表现优异，Sparsity Forcing 在空间推理任务上暴露出脆性。在需要准确估计相对物体距离、房间面积等场景中（图 7），token 剪枝容易破坏跨帧的空间对应关系，导致预测大幅度偏离真值（例如预测房间面积为 15.0 m²，而实际为 26.2 m²）。这一局限源于当前稀疏策略仅基于注意力质量选 token，未显式保护空间连贯性所需的长距离依赖。

此外，现有方法仍有几点待改进之处：（1）效率奖励仅使用 token 比例作为代理，未直接优化硬件感知指标（延迟、能耗）；（2）优化仅针对单轮 VQA，未涉及多轮对话或工具调用等场景下的 token 预算分配；（3）训练时间虽可接受，但 GRPO 的多 rollout 生成仍带来一定额外开销。未来的工作可将硬件反馈纳入奖励设计，并结合头/层/专家的联合 gating 将稀疏性扩展至更广义的推理预算控制。



## 定位与知识库关联

Sparsity Forcing 提出了一种将 token 级稀疏注意力从“事后修剪”转变为“端到端、推理一致优化目标”的范式。该方法通过多预算 rollout 与 GRPO 联合优化正确性与 token 减少率，并在后训练中将稀疏性从 MLLM 的固有特性提升为模型主动优化的行为。其所处的谱系可从训练无关稀疏注意力、基于代理目标的后训练增强、以及纯后训练基线三个维度定位。

### 与训练无关稀疏注意力的关系
ZipVL、FastV、VisionZip、Minference 等训练无关方法依赖模型固有的注意力稀疏性，通过静态或基于简易启发式的掩码过滤 token，无需额外训练。它们能在 80% 左右 token 保留率下保持性能，但当预算压至极低（~25%）时准确性普遍陡降。Sparsity Forcing 在同样的 ZipVL 掩码基座上引入 RL 后训练，使 Qwen2/2.5-VL 的 token 保留比从约 80% 进一步降至 **25% 左右**，而 7 个图像基准平均准确率仅下降 0.2 个百分点（Qwen2.5-VL-7B: 73.6 vs Full 73.8，Table 1），在视频基准上同样几乎无损（Table 2）。这表明通过端到端奖励信号，模型能学会在远低于自然稀疏度的预算下重新分配注意力质量，属于训练无关方法的有效增强，而非替代。

### 与基于代理目标的后训练方法的区别
此前增强稀疏性的训练方案（如 Sharpness loss、Temperature adjustment）通常通过正则项间接提升注意力锐度，缺乏对 token 预算的直接控制，且训练阶段采用标准因果注意力，与推理时的掩码策略不一致，导致训练/推理 gap。Sparsity Forcing 的核心差异在于：

| 改进维度 | 基线方法 | Sparsity Forcing | 证据 |
|----------|----------|------------------|------|
| 优化目标 | 代理损失（如注意力锐度最大化）或无组合 | 联合性能‑效率奖励（式 9），直接最大化 token 减少且保持正确性 | Section 3.2 |
| 预算探索 | 固定预算或仅凭温度控制 | 多 budget rollout，在线探索最小必要 token 数（top-p 阈值采样） | Figure 1, Table 5 |
| 训练/推理一致性 | 训练时全注意力，推理时剪枝 | 训练与推理使用同一套稀疏注意力掩码与 KV 缓存策略 | Section 3.2 |
| 反馈机制 | 离线样本对（如 DPO）难以反映效率‑性能权衡 | 组内相对优势（GRPO）奖励高效正确答案并惩罚低效或错误回答 | 式 10–11 |

实验显示，在 Qwen2.5-VL-7B 上，Sparsity Forcing 在 token 比 26.4% 时取得 **72.8** 的平均得分，显著优于 MOBA（66.6）、Sharpness loss（67.6）以及 ZipVL† 后训练基线（Table 3），且接近全量模型的 73.2。Temperature adjustment 仅能达到 67.4（Table 8），进一步说明端到端、以 token 节省为目标的 RL 优化的重要性。

### 适用边界
**模型与任务覆盖**：当前验证集中于 Qwen2-VL、Qwen2.5-VL 和 LLaVA-Video 的单轮视觉问答（图像/视频），未测试多轮对话、工具调用或检索增强场景。训练数据为 Video-R1-260k 或 LLaVA-Video-178k 子集，可能引入域偏差，但基座模型未做额外指令微调，对比公平。

**稀疏机制与推理控制**：方法依赖 token 粒度 top-p 注意力掩码，推理时 p 固定为 0.975 以保精度，但可通过调整 p 值在效率和准确率之间平滑权衡（Figure 4a）。在长序列下，保留 token 比例自适应降低，准确率几乎不变（Figure 4b），显示出良好的序列长度鲁棒性。

**效率收益的硬件依赖**：实测在 LLaVA-Video-7B 上，200k 序列长度时相对 FlashAttention-2 实现了 **3.3×** 解码加速和 **3.0×** 内存节省（Figure 4c,d），但该收益与特定 GPU 环境相关，不同硬件上的 latency 表现可能不同。

### 局限性
1. **空间推理退化**：当任务需要估计物体间距离、房间尺寸等跨帧对应关系时，token 剪枝可能破坏关键的空间线索，导致准确性下降（Figure 7 提供了失败案例）。
2. **训练开销**：GRPO 的多 rollout 生成使训练时间增至 110.4 小时，高于 MOBA 的 75.6 小时（Table 7），虽然仍在可接受范围内，但限制了快速迭代。
3. **任务单一性**：目前仅针对单轮 VQA 优化，未覆盖多轮对话中 KV 缓存预算的动态分配。
4. **效率奖励粒度**：奖励中的效率项仅以 token 减少率作为代理，未显式纳入硬件延迟、内存带宽或能耗等指标（Table 6 显示增加硬件延迟奖励并未带来额外提升，但并不意味着未来更精细的硬件感知奖励无用）。

### 开放问题
* 如何将 Sparsity Forcing 的强化稀疏性范式扩展到 **硬件感知** 目标（延迟/内存/能耗），使奖励信号直接对齐部署环境？
* 如何将同一框架应用于 **多轮对话、工具调用和检索** 的动态 token 预算分配，而不仅仅是单轮 VQA？
* 能否将 token 稀疏性与 **注意力头/层剪枝、MoE 专家门控、KV/激活量化** 等联合优化，形成多维度的效率‑性能 RL 策略？
* 在 **极度低预算**（<20%）下，如何保持视频理解中跨帧对应关系等空间推理能力，可能需要探索结构化的稀疏模式而非纯基于注意力分数的剪枝？
* 不同模型尺寸与架构对多预算 rollout 和奖励信号的响应不同，如何设计 **自适应预算范围** 和 **元学习策略** 以降低迁移成本？

Sparsity Forcing 将 token 节省从一次性的工程技巧升格为可被 RL 端到端优化的核心目标，其“多预算对比 + 组内优势”的框架为后续将大模型效率优化融入对齐训练提供了可复用的知识模板。



## 原文 PDF

![[paperPDFs/ICLR_2026/Sparsity_Forcing_Reinforcing_Token_Sparsity_of_MLLMs.pdf]]
