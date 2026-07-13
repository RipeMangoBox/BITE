---
title: "QeRL: Beyond Efficiency - Quantization-enhanced Reinforcement Learning for LLMs"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/QeRL_Beyond_Efficiency_Quantization_enhanced_Reinforcement_Learning_for_LLMs.pdf
project_link: null
code_link: https://github.com/NVlabs/QeRL
aliases:
- QeRL
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "NVFP4量化固有的噪声作为隐式探索机制，结合自适应量化噪声（AQN）动态调整策略熵，从而影响探索与利用平衡。"
primary_logic: "量化噪声在RL训练中并非有害，反而通过增加策略熵促进探索，逆转了有监督微调中的负面认知。利用这一特性，QeRL将NVFP4低位数量化与LoRA相结合，不仅大幅加速推理并降低内存，还通过AQN机制实现了优于16位LoRA的奖励增长和最终性能。"
claims:
- "QeRL在Qwen2.5-7B上GSM8K准确率达90.8%，超过16位LoRA（88.1%），接近全参数微调（91.2%）。"
- "QeRL在Qwen2.5-7B rollout速度比BF16 LoRA快约1.3倍（batch=8），端到端训练相对QLoRA整体快约1.8倍。"
- "量化噪声提高了初始策略熵，使量化模型在RL训练中奖励增长更快，并最终获得更高评价得分。"
- "自适应量化噪声（AQN）消融实验表明，添加AQN后3B模型GSM8K性能提升22.6个点，7B模型提升13.5个点（相对于未训练的BF16基线），且在不同量化格式和全精度下均有一致增益。"
---

# QeRL: Beyond Efficiency - Quantization-enhanced Reinforcement Learning for LLMs

> [!tip] 核心洞察
> 量化噪声在RL训练中并非有害，反而通过增加策略熵促进探索，逆转了有监督微调中的负面认知。利用这一特性，QeRL将NVFP4低位数量化与LoRA相结合，不仅大幅加速推理并降低内存，还通过AQN机制实现了优于16位LoRA的奖励增长和最终性能。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | QeRL: 超越效率——量化增强的大语言模型强化学习 |
| 英文题名 | QeRL: Beyond Efficiency - Quantization-enhanced Reinforcement Learning for LLMs |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=zw8zxMJJlm) · [GitHub](https://github.com/NVlabs/QeRL) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | QeRL |
| Dataset | GSM8K (Qwen2.5-7B-Instruct), MATH500 (Qwen2.5-7B-Instruct), Average over 4 math benchmarks (AIME24, AIME25, MATH500, AMC23) on Qwen2.5-7B, GSM8K (Qwen2.5-3B-Instruct) |

> [!tip] 效果简介
> - GSM8K (Qwen2.5-7B-Instruct) 上，accuracy (Pass@1) 为 90.8 (NVFP4 LoRA+AQN)，对比 88.1 (BF16 LoRA)，变化 +2.7。
> - MATH500 (Qwen2.5-7B-Instruct) 上，accuracy (Pass@1) 为 77.4 (NVFP4 LoRA+AQN)，对比 77.0 (BF16 LoRA)，变化 +0.4。
> - Average over 4 math benchmarks (AIME24, AIME25, MATH500, AMC23) on Qwen2.5-7B 上，average accuracy 为 36.4 (NVFP4 LoRA+AQN)，对比 35.7 (BF16 LoRA)，变化 +0.7。

## 概要

大语言模型（LLM）的强化学习（RL）训练面临rollout阶段推理速度慢、内存占用高的核心瓶颈。现有参数高效方法（如LoRA）虽减少了可训参数，但未加速推理；QLoRA因NF4解包开销甚至更慢。QeRL重新审视量化在RL中的角色，发现低位数量化引入的噪声并非有害：它能够提高策略熵、促进探索，从而逆转有监督微调下对量化噪声的负面认知。

基于此洞察，QeRL将NVFP4 4位浮点量化与LoRA结合，并引入自适应量化噪声（AQN）机制。NVFP4量化配合Marlin高效内核显著降低内存并加速rollout；AQN通过LayerNorm注入随机噪声并指数衰减，动态调节探索强度。冻结量化主干、仅训练LoRA适配器，实现了零额外参数开销的高效RL训练。

在Qwen2.5-7B模型上，QeRL的GSM8K准确率达到90.8%，超越BF16 LoRA（88.1%）并逼近全参数微调（91.2%），同时rollout吞吐提升约1.3倍（batch=8），端到端训练速度相对QLoRA提高约1.8倍。量化噪声使初始策略熵更高、奖励增长更快；AQN消融实验显示，添加AQN后3B和7B模型性能分别提升22.6和13.5个点（相对未训练BF16基线），且在不同量化格式下均有一致增益。这些结果揭示了量化噪声在RL中的探索价值，为LLM高效RL训练提供了新范式。



大语言模型（LLM）的强化学习（RL）训练已在数学推理、安全对齐等任务中取得显著提升，但其计算开销主要集中于 **rollout（采样生成）阶段**：每一轮策略更新都需要通过当前模型生成大量候选输出，这一过程的推理速度和GPU显存占用成为瓶颈。已有的高效微调方法，如低秩适应（LoRA）仅缩减可训练参数，**并未加速基础模型的推理**；而将低秩适应与权重量化结合的QLoRA（NF4+LoRA）虽降低了参数精度，却因NormalFloat 4（NF4）需要解包为浮点格式才能计算，**在前向推理中反而慢于16位LoRA**（Figure 1/2），无法解决rollout的效率问题。

进一步，量化引入的噪声在监督微调（SFT）中被普遍视为精度损失的有害因素，需要尽可能消除。然而，QeRL的作者通过分析发现，这一认知在RL训练中可能被**逆转**：量化噪声并非必然破坏策略学习，相反，它能**提高初始策略的熵（entropy）**，从而增强探索性（Figure 3）。这揭示了一个新的因果机制：**低位量化（如NVFP4的4-bit浮点）固有的量化误差可以作为隐式的探索驱动，加速奖励增长并提升最终评价得分**（Figure 4,5）。这意味着，若能在RL训练中主动利用并调控量化噪声，就有可能同时获得推理加速和更优的策略性能。

正是基于这一洞察，QeRL的工作动机双线并进：**效率侧**，采用NVFP4权重格式并配合高吞吐Marlin乘法内核，实现高质量4-bit推理，大幅降低显存并提升rollout吞吐（对7B模型，相比BF16 LoRA加速约1.3倍，端到端相对于QLoRA整体加速约1.8倍；32B模型可达2倍吞吐，Table 3,12）；**性能侧**，设计自适应量化噪声（AQN）机制，在LayerNorm权重中注入可调控的高斯噪声，结合指数衰减调度器，**动态平衡探索与利用**，无需额外训练参数。消融实验表明，仅加入AQN即可在3B模型中相对未训练的BF16基线提升22.6个点的GSM8K准确率（Table 1），且该收益在不同量化格式甚至全精度设定下均一致存在。最终，QeRL在GSM8K（7B模型）上达到90.8%准确率，超越BF16 LoRA的88.1%，逼近全参数微调的91.2%（Table 1），以更低的资源消耗实现了更强的数学推理能力。



## 核心方法与创新机理

### 瓶颈与动机
LLM强化学习（RL）训练中，rollout阶段的逐token自回归推理构成核心吞吐瓶颈。现有参数高效方法（如BF16 LoRA）虽压缩了可训参数量，却不减少推理计算量；QLoRA引入NF4权重量化来降内存，但因NF4解包开销反而使推理变慢。因此，**加速推理、降低显存同时不损害训练信号质量**，成为RL训练的关键需求。

### 核心洞察：量化噪声作为隐式探索
QeRL转变了对低精度权重的认知：在SFT中，量化噪声被视为精度损失；但在RL中，量化引入的权重扰动天然地增大了策略的采样熵，**相当于隐式注入了探索噪声**，有助于跳出局部最优、加速奖励增长。由此，QeRL故意保留并动态调节此噪声，将其从缺陷变为特性，逆转了以往只关注精度损失的范式。

### 关键创新：Changed Slots vs. Baselines

| 创新维度 | Baseline（BF16 LoRA / QLoRA） | QeRL 变更 | 带来的效果 |
|----------|-------------------------------|-----------|------------|
| **权重量化格式** | BF16（16位浮点）或 NF4（4位 NormalFloat） | **NVFP4（4位浮点，双缩放机制）**：全局FP32缩放+块级FP8缩放 | 推理速度提升 1.3–2.0×（7B/32B模型，batch=8）；单卡H100可训练32B模型  |
| **探索噪声注入** | 无额外噪声 | **自适应量化噪声（AQN）**：在LayerNorm权重中注入高斯噪声，等效于对下游权重施加乘法噪声，随训练阶段指数衰减 | 3B模型GSM8K性能提升22.6点（vs 未训练BF16基线）；7B提升13.5点；在不同量化格式甚至全精度下均有增益 |
| **推理加速内核** | 标准BF16 GEMM | **针对NVFP4优化的Marlin内核**，高效执行NVFP4×BF16矩阵乘法 | 降低rollout延迟，端到端训练速度较QLoRA快约1.8× |
| **可训参数策略** | LoRA适配器训练（BF16）或 QLoRA（NF4+LoRA，反量化后计算） | **冻结4-bit量化主干**，仅训练LoRA低秩适配器；AQN融入LayerNorm权重，**零额外参数开销** | 保持参数效率；量化噪声与LoRA解耦，避免对训练精度的干扰 |

### 因果机制与决定性证据
- **量化→高熵→强探索**：NF4/MXFP4/NVFP4等4-bit量化模型的采样熵均显著高于BF16模型（Figure 5），训练初期奖励上升斜率更陡，终期评估分数更高（Figure 4）。NVFP4虽早期不如MXFP4，但后期收敛到更优奖励，最终在7B模型GSM8K上达90.8%，超过BF16 LoRA的88.1%，接近全参数微调的91.2%（Table 1(b)）。
- **AQN动态调节探索-利用平衡**：指数衰减噪声调度（σ(k) = σ_start · (σ_end/σ_start)^((k-1)/(K-1))）在前期鼓励大尺度探索，后期逐渐关闭噪声转向利用，消融实验显示移除AQN后3B模型准确率下降1.1点（Table 1(a)、Figure 8）。并在不同量化格式（NF4、MXFP4、NVFP4）及全精度BF16下追加AQN，均带来一致正收益（Table 7），表明该机制对量化噪声的普适增强。
- **系统级效率**：得益于NVFP4的4-bit存储和Marlin快速内核，Qwen2.5-7B的rollout吞吐约2092 tok/s，较BF16 LoRA（1641 tok/s）提升27%；32B模型吞吐提升近一倍（344→688 tok/s）（Table 10、12），端到端训练时间从7.20s降至4.75s/step（7B模型，Table 4）。

上述创新协同，使QeRL不仅比原有LoRA/QLoRA方案更快、更省显存，还在数学推理基准上达到甚至超越16位全精度性能，并保持了训练过程对更高学习率（1e-5）的鲁棒性——该学习率下BF16 LoRA会出现训练崩溃（Figure 16、17）。



![[assets/figures/papers/iclr26_0013_zw8zxMJJlm_QeRL_Beyond_Efficiency_-_Quantization-enhanced_R/figures/005_Figure_2.jpg]]
*Figure 2: The illustration of QeRL. (a) RL via LoRA: reducing trainable parameters, but does not alleviate the rollout bottleneck. (b) RL via QLoRA: NF4 quantization with LoRA, but NF4 is slower than LoRA. (c) QeRL: NVFP4 quantization with LoRA, reducing memory and enabling faster RL while matching full-parameter finetuning performance with adaptive quantization noise. AQN dynamically adjusts quantization noise, enhancing exploration in LoRA-based RL*

当前 LLM 强化学习（RL）训练的核心瓶颈在于 rollout 阶段的推理速度与内存占用：参数高效方法（如 LoRA）虽降低了可训参数量，却未加速推理，而 QLoRA（NF4+LoRA）因 NF4 解包开销反而更慢。QeRL 的核心设计思路是将 4 位浮点量化与低秩适配结合，同时利用量化噪声促进探索，并通过自适应噪声调度在训练过程中动态调节探索–利用平衡。整体框架以 **NVFP4 量化主干**、**Marlin 加速内核**、**LoRA 适配器** 和 **自适应量化噪声（AQN）** 为主体，部署于 GRPO 或 DAPO 策略优化流程中。

如图 2 所示，QeRL 的运行时管道由以下模块串联构成：

1. **NVFP4 量化主干**（Section 3.3）：将 LLM 的全部线性层权重量化为 NVFP4 格式（全局 FP32 缩放因子 + 块级 FP8 缩放因子），冻结后仅作为前向计算引擎。量化后的模型内存占用降至约原 BF16 模型的 1/4，显著降低显存压力，使 32B 模型可在单张 H100 80GB GPU 上完成 RL 训练。
2. **Marlin 乘法内核**（Section 3.1, Appendix J）：针对 NVFP4 设计的优化矩阵乘法核心，执行高效的 NVFP4 × BF16 运算，用于 rollout 生成和 prefilling 阶段。该内核是推理吞吐提升的关键，在 batch=8 时将 7B 模型的 rollout 速度提升至 BF16 LoRA 的约 1.27 倍，相比 QLoRA 端到端训练快约 1.8 倍。
3. **LoRA 适配器**（Section 2, 3.1）：在注意力与前馈子层的权重矩阵旁路插入低秩矩阵 $\mathbf{B}\mathbf{A}$，仅训练这些适配器参数。推理时 LoRA 的加权输出与 NVFP4 去量化后的主干权重相加，更新规则为 $\mathbf{W} + \Delta\mathbf{W} = \mathbf{W} + \mathbf{B}\mathbf{A}$。适配器与量化主干无缝协作，实现零额外推理参数开销的参数高效微调。
4. **自适应量化噪声（AQN）注入**（Section 3.3, Figure 6）：将静态量化误差 $\Delta\epsilon = \hat{\mathbf{W}} - \mathbf{W}$ 与一个动态随机噪声向量 $\mathbf{Z}_{\text{noisy}}$ 结合，形成可控的向量化扰动 $\Delta\epsilon' = \mathbf{Z}_{\text{noisy}} + \Delta\epsilon$。该扰动被注入 LayerNorm（如 RMSNorm）的权重通道，等效于对下游的权重矩阵施加行方向乘法噪声，从而增加采样时的策略熵，促使模型在 RL 训练早期进行更充分的探索。AQN 不引入额外可训参数，其注入后利用 LayerNorm 的分配律将加性噪声转移至输入侧并与权重缩放因子融合（Eq 9），保证了推理内核兼容性。
5. **指数衰减噪声调度器**（Section 3.3, 4.2）：噪声标准差 $\sigma$ 按 $\sigma(k) = \sigma_{\text{start}} \cdot (\sigma_{\text{end}} / \sigma_{\text{start}})^{\frac{k-1}{K-1}}$ 在 $K$ 个阶段内从初始值 $\sigma_{\text{start}}$ 指数衰减至 $\sigma_{\text{end}}$。阶段 0 只保留静态量化噪声（$\sigma=0$），随后逐渐注入并衰减动态噪声，使得训练从高探索逐步过渡到高利用，从而在 Reward 增长和最终评估得分上稳定超越恒定噪声方案。
6. **GRPO / DAPO 策略优化**（Section 3.1, 3.2）：给定输入问题 $q$，策略模型（NVFP4 主干 + LoRA + 实时噪声）采样一组 $G$ 个候选回答 $\{o_i\}$，由外部奖励模型或规则计算奖励 $r_i$，进而求得组内标准化优势 $A_i$。优化目标基于剪切后的重要性采样比率与 KL 惩罚项（Eq 3），仅更新 LoRA 适配器参数，冻结量化主干与噪声参数（噪声权重在训练过程中固定合并）。

整个训练过程的端到端数据流为：输入提示 → (Marlin 加速的) NVFP4 量化主干前向推理 + LoRA 适配器输出 → 通过 LayerNorm 注入的 AQN 扰动影响 token 分布 → 采样获得候选序列 → 奖励计算 → GRPO/DAPO 计算梯度并更新 LoRA 权重。训练完成后，推理阶段可关闭 AQN（$\sigma=0$），仅保留量化主干与精确适配器，以获得最佳数学推理性能。在 Qwen2.5-7B 的 GSM8K 基准上，该框架达到 90.8% 的准确率，超过 BF16 LoRA 的 88.1% 并接近全参数微调的 91.2%（Table 1b），同时保持了显著的内存与延迟优势。



QeRL 以提升 LLM 强化学习训练效率与效果为目标，构建了四个协同工作的关键模块：
1) **NVFP4 量化与 Marlin 加速推理**，将权重压缩为 4 位浮点并在 rollout 阶段高速计算；
2) **LoRA 低秩适配**，冻结量化主干，仅训练注入的低秩矩阵，大幅减少显存与通信开销；
3) **自适应量化噪声（AQN）注入与调度**，将量化误差与可控高斯噪声叠加，动态调节探索—利用平衡，且不引入额外参数；
4) **GRPO/DAPO 策略优化**，利用组内相对优势更新策略，保持与主流 RL 算法兼容。

### NVFP4 量化与 Marlin 内核
对权重矩阵 $\mathbf{W}$ 执行 NVFP4 格式的逐块量化，推理时通过全局 FP32 缩放因子 $S_{\mathrm{FP32}}$ 和块级 E4M3 缩放因子 $S_{\mathrm{E4M3}}$ 恢复高精度值：
$$
\hat{\mathbf{W}} = \mathrm{Dequant}(\tilde{\mathbf{W}}) = S_{\mathrm{FP32}} \cdot \big( S_{\mathrm{E4M3}} \odot \tilde{\mathbf{W}} \big), \tag{6}
$$
其中 $\tilde{\mathbf{W}}$ 为 4 位量化权重，$\odot$ 为逐元素乘法。相比 NF4，该双缩放机制保留了更细粒度的幅值分布，是后续噪声利用的基础。
Marlin 定制化 CUDA 内核专门加速 $\text{NVFP4} \times \text{BF16}$ 运算，使 Qwen2.5‑7B 的 rollout 吞吐较 BF16 LoRA 提升约 1.3 倍，较 QLoRA 提升 1.5 倍以上（Table 10，Figure 1）。

### LoRA 低秩适应
在注意力/前馈层的权重旁路插入可训低秩矩阵 $\mathbf{B}$ ($d_{\text{out}}\times r$) 和 $\mathbf{A}$ ($r\times d_{\text{in}}$)，秩 $r$ 典型取 16 或 32，可训参数量约为全量的 0.5%。前向传播等效为：
$$
\mathbf{W} + \Delta \mathbf{W} = \mathbf{W} + \mathbf{B}\mathbf{A}. \tag{2}
$$
RL 训练时仅更新 LoRA 适配器，冻结量化主干，从而在获得 4 位内存收益的同时避免 QLoRA 中 NF4 解包带来的额外延迟。

### 自适应量化噪声
量化引入的静态误差 $\Delta\epsilon = \hat{\mathbf{W}} - \mathbf{W}$（式 5）在 SFT 中是有害噪声，但在 RL 中会提高初始策略熵（Figure 5），加速早期奖励增长（Figure 4）。然而固定噪声在后期会损害收敛。为此，QeRL 提出 **AQN**，将静态误差与动态高斯噪声融合，并通过指数衰减调度控制噪声强度。

**噪声注入**：在每一 Transformer 块的 RMSNorm 权重上叠加服从 $\mathcal{N}(0,\sigma^2(k))$ 的随机向量 $\mathbf{Z}_{\text{noisy}}$，得到总噪声：
$$
\Delta \epsilon' = \mathbf{Z}_{\text{noisy}} + \Delta\epsilon = \mathbf{Z}_{\text{noisy}} + (\hat{\mathbf{W}} - \mathbf{W}). \tag{7}
$$
$\sigma(k)$ 为第 $k$ 阶段的标准差，$\sigma(k)=0$ 时退化回纯量化 LoRA。

**指数衰减调度**：$\sigma$ 依下式从初值 $\sigma_{\text{start}}$ 指数降低至终值 $\sigma_{\text{end}}$（共 $K$ 个阶段）：
$$
\sigma(k) = \sigma_{\text{start}} \cdot \left( \frac{\sigma_{\text{end}}}{\sigma_{\text{start}}} \right)^{\frac{k-1}{K-1}}. \tag{8}
$$
消融研究证实指数衰减比线性、余弦等方案提供更稳定的性能提升（Figure 9）。

**零参数开销的等效实现**：利用分配律将加性噪声移入 LayerNorm 的缩放因子，形成对下游权重 $\hat{\mathbf{W}}$ 的行乘性噪声：
$$
\mathbf{X}(\mathbf{Z}_{\text{noisy}} + \hat{\mathbf{W}}) = \mathbf{X}\cdot\mathbf{Z}_{\text{noisy}} + \mathbf{X}\cdot\hat{\mathbf{W}}.
$$
经 RMSNorm 变形后，该扰动等价于 $\hat{\mathbf{W}}$ 的每一行乘上一个由 $\mathbf{Z}_{\text{noisy}}$ 决定的因子（详见附录 G），整个过程不引入任何额外可训参数。

### 策略优化目标
QeRL 不修改底层 RL 算法，默认采用 GRPO 目标：
$$
\mathcal{I}(\theta) = \mathbb{E}_{q,\{o_i\}} \Bigg[ \frac{1}{G}\sum_{i=1}^{G}\frac{1}{|o_i|}\sum_{t=1}^{|o_i|} \min\Big( \frac{\pi_\theta(o_{i,t}|q)}{\pi_{\theta_{\text{old}}}(o_{i,t}|q)}A_{i,t},\ \operatorname{clip}\big(\frac{\pi_\theta(o_{i,t}|q)}{\pi_{\theta_{\text{old}}}(o_{i,t}|q)}, 1-\alpha, 1+\alpha\big) A_{i,t} \Big) - \beta\,\mathbb{D}_{\text{KL}}(\pi_\theta\|\pi_{\text{ref}}) \Bigg],
$$
其中优势 $A_i$ 为组内标准化奖励：
$$
A_i = \frac{r_i - \operatorname{mean}(\{r_1,r_2,\dots,r_G\})}{\operatorname{std}(\{r_1,r_2,\dots,r_G\})}.
$$
$q$ 为输入 prompt，$G$ 为每组采样数，$\pi_{\theta_{\text{old}}}$ 为旧策略，$\pi_{\text{ref}}$ 为参考策略，$\alpha$ 为裁剪范围，$\beta$ 控制 KL 惩罚。在更大规模训练中可切换为 DAPO 算法，其核心思想类似但引入了动态采样和过滤策略。

上述模块与公式共同构成了 QeRL 效率与效果兼顾的技术路径：NVFP4 量化加 Marlin 内核破解 rollout 速度瓶颈，LoRA 保持参数高效，而 AQN 将量化噪声转化为可控探索源，使 4 位量化模型在 GSM8K（90.8%）等基准上不仅超越 16 位 LoRA（88.1%），且逼近全参数微调（91.2%）。



## 实验与关键发现

### 模型与基准概览

QeRL 主要在 Qwen2.5 系列（3B、7B、14B、32B）上评估，覆盖数学推理（GSM8K、MATH500、AIME24/25、AMC23）与安全对齐（SafeRLHF-QA）场景。所有 RL 训练使用相同输入长度限制（256 tokens）、最大生成长度（2048 tokens）、采样温度 1.0、批量大小 128，并固定 vLLM GPU 内存预算以确保推理速度对比公平。数学任务采用 GRPO 或 DAPO 算法，具体配置见 Table 6。

### 主实验结果

**GSM8K 单基准性能。** Qwen2.5-7B-Instruct 在 GSM8K 上，QeRL（NVFP4 LoRA + AQN）达到 **90.8%** 准确率，超过 BF16 LoRA 的 88.1% (+2.7)，接近全参数微调的 91.2%（Table 1(b)）。3B 模型上，QeRL 达到 83.7%，相比未训练的 BF16 基线提升 **+22.6** 个点，显著超越同配置的 BF16 LoRA，并逼近全参数微调水平（Table 1(a)）。该结果证实 4 比特量化结合自适应噪声不但未损害精度，反而带来正向增益。

![[assets/figures/papers/iclr26_0013_zw8zxMJJlm_QeRL_Beyond_Efficiency_-_Quantization-enhanced_R/figures/012_Table_1.jpg]]
*Table 1: Qwen2.5 Performance on GSM8K. GRPO algorithm is used to train 3B and 7B models on LoRAyR LoRA GSM8K dataset, while “Full” denotes the full-parameter training and0.2ura $\mathbf { \Delta } ^ { 6 6 } \mathbf { W }$ \# $\mathbf { \Sigma } ^ { 9 }$ represents the bit-width0.2 and data format of weight. + and - are compared with original bfloat-16 (BF16) models.Ac

![[assets/figures/papers/iclr26_0013_zw8zxMJJlm_QeRL_Beyond_Efficiency_-_Quantization-enhanced_R/figures/011_Table_1.jpg]]
*Table 1: (a) Performance of Qwen2.5-3B-Instruct*

**多数学基准平均表现。** 在 AIME24、AIME25、MATH500、AMC23 四个基准上对 7B 模型进行 DAPO 训练，QeRL 的平均准确率达到 **36.4**，高于 BF16 LoRA 的 35.7（Table 2）。其中 MATH500 上 QeRL 得分 77.4，与 BF16 LoRA 的 77.0 持平（差距在波动范围内），表明量化策略在复杂推理上同样具备竞争力。

**安全对齐与常识问答。** 在 SafeRLHF-QA 上，QeRL 将 3B 模型准确率从 BF16 的 78.4% 提升至 **85.3%**，比 BF16 LoRA 的 83.5% 高出 1.8 个点（Table 5(a)）。在 CommonsenseQA 上，QeRL 达到 73.2%，与 LoRA 基线（73.5%）基本持平，表明该方法在非数学任务上仍具潜力。

**推理加速与内存节省。** QeRL 的推理加速来自 NVFP4 量化和 Marlin 优化内核。7B 模型在 batch=8 的 rollout 吞吐量达到 **2091.8 tokens/s**，相对于 BF16 LoRA 的 1641.1 tokens/s 提升约 1.27 倍；端到端 GRPO 训练每步总时间从 7.20 s 降至 4.75 s（Table 4）。14B 和 32B 模型受益更显著：32B 模型在 batch=8 下吞吐量从 344.3 tokens/s 提升至 688.2 tokens/s，**加速比达 2.0 倍**（Table 12），使得单张 H100 80GB GPU 即可完成 32B 模型的 RL 训练。

### 消融实验

**自适应量化噪声 (AQN) 的作用。** 移除 AQN 后，NVFP4 LoRA 在 GSM8K 上的 3B 模型准确率从 83.7 降至 82.6，7B 模型从 90.8 降至约 89.5（Table 1、Figure 8），显示 AQN 对最终性能有稳定增益。该增益在不同量化格式（NF4、MXFP4、NVFP4）甚至全精度设置下均一致存在（Table 7），且在 LoRA 模式下的提升幅度大于全参数微调，表明噪声机制与低秩适应协同良好。

![[assets/figures/papers/iclr26_0013_zw8zxMJJlm_QeRL_Beyond_Efficiency_-_Quantization-enhanced_R/figures/014_Figure_8.jpg]]
*Figure 8: Ablation of AQN on 3/7B model*

**噪声调度器设计。** 指数衰减策略（Exponential Decay）在最终奖励上优于线性、余弦和对数衰减，带来更平稳的进步曲线（Figure 9）。初始噪声标准差 σ_start 和终止 σ_end 的选择需要手动调节，但指数形式本身提供了稳健的探索‑利用过渡。

**LoRA 秩的选择。** LoRA rank 从 4 增加到 64 的过程中，rank=16 的收敛速度和最终奖励最优；更高秩（如 64）导致吞吐量下降且训练增益递减（Figure 10、Table 14）。因此实际部署中推荐 rank=16 以平衡效率与效果。

**训练稳定性。** QeRL 允许使用更高的策略学习率（1e-5），而 BF16 LoRA 在同样设置下出现训练崩溃（Figure 16、Figure 17）。量化噪声在训练早期引入的熵增加充当了隐式正则化器，抑制了策略的过早坍塌，从而提升优化稳定性。

### 量化噪声对训练动态的影响

量化噪声并非有害扰动，而是**隐式探索**的来源。实验显示，量化模型的初始策略熵明显高于 16 位模型（Figure 5），在 RL 训练初期就带来更高的奖励增长速率（Figure 4、Figure 7）。NVFP4 在早期可能落后于 MXFP4，但最终收敛到更优的奖励水平，表明其噪声特性更适合长期训练。结合指数衰减的 AQN，噪声从探索主导向利用平滑过渡，实现了比纯量化噪声更优的最终表现（Figure 8）。

![[assets/figures/papers/iclr26_0013_zw8zxMJJlm_QeRL_Beyond_Efficiency_-_Quantization-enhanced_R/figures/009_Figure_4.jpg]]
*Figure 4: Training reward performance. The upper figures illustrate the training rewards under DAPO, while the lower one is GRPO. Although MXFP4 achieves higher scores in the early stages of training, NVFP4 ultimately converges to better final rewards. LoRA rank is set to 32*

### 局限与待验证方向

1. **模型规模上限：** 当前实验仅覆盖 3B‑32B 参数；在 70B 及以上模型上 QeRL 的效率优势和性能增益是否保持尚需检验。
2. **任务范围：** 评估集中于数学推理，安全对齐和常识问答仅初步测试；在代码生成、多轮对话等更复杂任务上，量化噪声的作用机制可能不同。
3. **数据与设置多样性：** RL 训练本身资源消耗巨大，实验未在更多样化的数据集或不同模型架构（如非 Transformer）上全面验证。
4. **超参数敏感性：** AQN 的 σ_start、σ_end 以及衰减阶梯数 K 需针对模型和任务进行调节，缺乏自动化选择策略。

整体而言，QeRL 在保持或超越 16 位 LoRA 性能的同时，显著提升了推理速度和内存效率，其核心机制 —— 利用并主动调控量化噪声 —— 为低比特 LLM 的强化学习训练提供了新的设计空间。

### 补充图表

![[assets/figures/papers/iclr26_0013_zw8zxMJJlm_QeRL_Beyond_Efficiency_-_Quantization-enhanced_R/figures/004_Figure_1.jpg]]
*Figure 1: Rollout speedup and accuracy of QeRL on Qwen2.5-7B-Instruct. QeRL achieves faster RL rollout and end-to-end training speeds (batch=8), while delivering performance superior to vanilla LoRA and QLoRA, also comparable to full-parameter RL on mathematical benchmarks*



## 定位与知识库关联

QeRL 承接 LLM 强化学习（RL）中参数高效微调与推理加速的双重需求，在方法谱系上居于“量化基础模型 + LoRA + 动态探索”的交汇点。  
与现有高效 RL 方案的核心区别可通过三条基线刻画：

1. **BF16 LoRA**：虽减少了可训练参数，但未解决 rollout 阶段的推理瓶颈；QeRL 将主干权重量化为 NVFP4，配合 Marlin 内核，在相同 batch 下实现约 1.3× 的推理速度提升（Qwen2.5‑7B）[Table 10]，同时因量化噪声的内生探索效应，最终准确率反超 BF16 LoRA（GSM8K 90.8% vs. 88.1%）[Table 1(b)]。
2. **QLoRA（NF4 + LoRA）**：NF4 解包反而使推理慢于标准 LoRA，且未利用量化噪声；QeRL 改用 NVFP4 格式（含全局 FP32 缩放与块级 E4M3 缩放），既消除解包延迟，又通过 AQN 将静态量化误差转化为可控的探索信号 [Figure 2]。
3. **全参数 BF16 RL**：作为精度上界，QeRL 在数学推理任务上与之基本持平（GSM8K 90.8% vs. 91.2%；MATH500 77.4% vs. 77.4%）[Figure 1, Table 2]，但极大降低了显存和训练时间，使 32B 模型能在单张 H100 80GB GPU 上完成 RL 训练 [Table 12]。

在上述基线之外，**FlashRL** 也曾探讨 8‑bit 量化 rollout 与重要性采样，但未触及量化噪声对探索的系统性影响。QeRL 首次揭示：在 LoRA‑based RL 中，量化噪声天然提高策略熵 [Figure 5]，加速奖励增长 [Figure 3, Figure 4]，并据此设计**自适应量化噪声（AQN）**——通过在 LayerNorm 权重中嵌入随机噪声并指数衰减 [Eq. 7‑8]，以零额外参数开销实现从探索到利用的平滑过渡 [Figure 6]。AQN 在不同量化格式（NF4, MXFP4, NVFP4）甚至全精度 LoRA 下均带来一致增益 [Table 7]，且在低秩适配下的增益大于全参数微调，表明其作用并非单纯补偿精度损失，而是改变了 RL 的训练轨迹。

**适用边界**  
- 当前验证集中在数学推理任务（GSM8K, MATH500, AIME, AMC23）和参数规模 3B–32B 的 Qwen2.5‑Instruct / Base 模型。  
- 训练算法限定为 GRPO 与 DAPO，LoRA rank 通常设为 16（收敛最快且吞吐最优）[Figure 10]。  
- 速度收益依赖 NVFP4 的 Marlin 内核，硬件需支持 4‑bit 浮点运算；若无法使用 Marlin，回退到较慢的反量化路径，收益会衰减。  
- AQN 的噪声衰减采用指数调度，在已见场景下较线性/余弦/对数调度更稳定 [Figure 9]，但其对噪声初始值 σ_start、终值 σ_end 的敏感性尚未在更广任务内充分扫描。

**局限与开放问题**  
本文报告的局限（需读者手工验证）：  
1. 实验仅覆盖 ≤32B 模型，QeRL 在 70B+ 模型上的效率与性能提升未知。  
2. 评估集中于数学推理，对代码生成、通用对话等场景缺乏支撑。  
3. RL 训练本已资源密集，虽显著加速，但未在多样性更强的数据集（如混合任务）上进行全面测试。  

由此引申的开放问题包括：  
- QeRL 能否在更大规模模型（≥70B）上维持相似的精度‑效率折衷？量化位宽（如 3‑bit 或 2‑bit）是否会打破当前探索与利用的平衡？  
- 在非推理任务中，量化噪声是否仍能有效提升策略熵并促进探索？多轮交互与密集奖励建模下 AQN 的收益是否依然成立？  
- 本方法对非 Transformer 架构、或与更复杂的 RL 算法（如 Online RLHF、PPO 变体）结合时的通用性如何？  
- AQN 的动态噪声调节与显式熵正则化（如 policy entropy bonus）存在何种互补或替代关系？这些问题的回答将决定 QeRL 能否从数学推理的“特化方案”升维为高效 LLM RL 训练的一般化组件。



## 原文 PDF

![[paperPDFs/ICLR_2026/QeRL_Beyond_Efficiency_Quantization_enhanced_Reinforcement_Learning_for_LLMs.pdf]]
