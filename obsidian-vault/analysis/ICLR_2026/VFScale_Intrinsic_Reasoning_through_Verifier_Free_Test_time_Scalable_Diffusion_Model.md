---
title: "VFScale: Intrinsic Reasoning through Verifier-Free Test-time Scalable Diffusion Model"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/VFScale_Intrinsic_Reasoning_through_Verifier_Free_Test_time_Scalable_Diffusion_Model.pdf
project_link: null
code_link: https://github.com/AI4Science-WestlakeU/VFScale
openreview_forum_id: 8ta0xgtsJK
aliases:
- VFScale
tags:
- ICLR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: "通过MRNCL损失和KL正则化改善能量景观的训练目标，以及将混合蒙特卡洛树搜索引入去噪过程的推理方法。"
primary_logic: "扩散模型自身的能量函数可以作为内在验证器，通过训练使其更好地与样本质量对齐，并结合高效搜索策略，无需外部验证器即可实现测试时扩展。"
claims:
- "VFScale在15×15迷宫任务上解决88.28%的问题，而标准扩散模型完全失败。"
- "通过MRNCL和KL训练，能量指导的Best-of-N在N=161时迷宫成功率从6.25%提升至70.31%。"
- "混合蒙特卡洛树搜索（hMCTS）进一步将迷宫成功率提升至88.28%（N=161），较Best-of-N提高约18%。"
- "性能-能量一致性指标从~73%提升至~84%，直接证明了MRNCL损失对能量景观的改善。"
---

# VFScale: Intrinsic Reasoning through Verifier-Free Test-time Scalable Diffusion Model

> [!tip] 核心洞察
> 扩散模型自身的能量函数可以作为内在验证器，通过训练使其更好地与样本质量对齐，并结合高效搜索策略，无需外部验证器即可实现测试时扩展。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | VFScale：通过免验证器测试时扩展的扩散模型实现内在推理 |
| 英文题名 | VFScale: Intrinsic Reasoning through Verifier-Free Test-time Scalable Diffusion Model |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=8ta0xgtsJK) · [GitHub](https://github.com/AI4Science-WestlakeU/VFScale) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | VFScale |
| Dataset | Maze-15×15, Sudoku (harder, 17-33 givens) |

> [!tip] 效果简介
> - Maze-15×15 上，Success Rate 为 0.8828 (VFScale + hMCTS, N=161)，对比 0.1094 (Original + BoN, N=161)，变化 +0.7734。
> - Sudoku (harder, 17-33 givens) 上，Success Rate 为 0.4297 (VFScale + hMCTS, N=321)，对比 0.2812 (Original + BoN, N=321)，变化 +0.1485。
> - Maze-15×15 上，Success Rate 为 0.7031 (VFScale training, BoN, N=161)，对比 0.1094 (Original training, BoN, N=161)，变化 +0.5937。

## 概要

扩散模型在生成任务上取得了显著成功，但在推理任务（如迷宫求解、数独）上的测试时扩展（test-time scaling）面临根本性瓶颈：**标准扩散模型的能量景观质量差，缺乏性能-能量一致性**，导致单纯增加采样数量（Best-of-N）带来的增益十分有限。

针对这一问题，**VFScale** 提出了一条无需外部验证器的测试时扩展路径。其核心洞察在于：**扩散模型自身的能量函数可以作为内在验证器**，关键在于通过训练使其与样本质量对齐，并配合高效的搜索策略加以利用。

方法层面，VFScale 包含两个关键改变：

1. **训练阶段**：在标准 MSE 损失和对比损失之上，引入**单调回归负对比学习（MRNCL）损失**和 **KL 正则化**。MRNCL 通过强制能量与 L2 距离之间的单调线性关系，显著提升性能-能量一致性；KL 正则化则平滑能量景观并提高采样多样性。
2. **推理阶段**：将**混合蒙特卡洛树搜索（hMCTS）** 引入去噪过程——早期噪声较大时使用 Best-of-N 并行探索，后期噪声较小时切换为 MCTS 深度利用，并利用能量方差自适应决定切换时机。

主要实验结果：

- 在 15×15 迷宫任务上，VFScale + hMCTS 达到 **88.28%** 的成功率，而标准扩散模型完全失败（Table 5）。
- 仅通过 MR-NCL 和 KL 训练，能量引导的 Best-of-N 在 N=161 时便将迷宫成功率从 6.25% 提升至 **70.31%**（Table 3）。
- 性能-能量一致性指标从约 73% 提升至约 **84%**，直接验证了 MR-NCL 对能量景观的改善（Table 4）。
- 内在能量验证器在 Kendall-τ 秩相关性上显著优于外部验证器，尤其在去噪中间阶段保持强正相关（>0.4）（Table 19）。

VFScale 的方法定位清晰：它不属于需要外部奖励模型或验证器的测试时扩展范式，而是通过**重塑扩散模型的能量景观**，使内在能量函数本身成为可靠的质量指示器，再结合树搜索提升推理效率。这一思路在方法谱系上介于基于能量的扩散模型（Du et al., 2024）与测试时搜索方法之间，为扩散模型在推理任务上的扩展提供了新的技术路线。



### 扩散模型在推理任务上的测试时扩展困境

扩散模型在图像生成领域展现出强大的能力，但其在组合推理任务（如迷宫求解、数独）上的应用仍面临根本性瓶颈。标准扩散模型通常采用均方误差损失（$\mathcal{L}_{\mathrm{MSE}}$）与对比损失（$\mathcal{L}_{\mathrm{Contrast}}$）进行训练（Du et al., 2024），然而这类训练目标并未显式优化模型在测试时的扩展能力。

核心问题在于**能量景观质量差**：扩散模型内在的能量函数与样本质量之间缺乏一致性，即低能量样本未必对应高质量解。这种性能-能量一致性的缺失，导致即便在推理时大幅增加采样数量（如Best-of-N策略），性能增益也极为有限。以15×15迷宫任务为例，原始训练方法在N=1时成功率仅为6.25%，即便将采样预算扩展至N=161，成功率也仅提升至10.94%（Table 3）——测试时扩展几乎失效。

### 现有方法的缺口

当前利用扩散模型进行推理的方法通常依赖两类策略：

1. **外部验证器引导**：训练独立的判别模型对生成样本进行评分筛选。这一路径不仅需要额外的模型设计与训练成本，更关键的是，外部验证器与生成模型之间存在分布偏移，限制了测试时扩展的上限。实验表明，使用外部训练验证器的Best-of-N在迷宫任务上的成功率（N=81时为32.03%）远低于使用内在能量函数的方案（68.75%）（Table 10）。

2. **简单重采样策略**：如Best-of-N（BoN）在原始能量函数引导下进行选择，但由于能量景观未经过针对性优化，能量排序与真实质量排序之间的Kendall-τ秩相关性较弱，尤其在去噪早期阶段更为明显（Table 19），导致搜索效率低下。

上述缺口指向一个明确的研究动机：**能否通过改善扩散模型自身的能量景观，使其内在能量函数直接充当可靠的验证器，从而在无需外部模型的情况下实现有效的测试时扩展？**

### 本文动机与核心思路

VFScale的提出正是为了填补这一缺口。其核心洞察在于：扩散模型天然具备能量函数，若能通过定制化训练使其能量值与样本质量建立单调且一致的对齐关系，则该内在能量可直接作为验证器，驱动测试时搜索。在此基础上，进一步设计高效的推理搜索策略，即可在相同计算预算下显著提升推理性能。

具体而言，VFScale从两个层面回应上述挑战：

- **训练层面**：引入单调回归负对比学习损失（MRNCL）强制能量与样本L2距离之间的单调线性关系，辅以KL正则化平滑能量景观并提升采样多样性，从而系统性改善性能-能量一致性（Table 4显示一致性指标从约73%提升至约84%）。
- **推理层面**：将混合蒙特卡洛树搜索（hMCTS）嵌入去噪过程——在早期高噪声阶段采用Best-of-N并行探索，后期低噪声阶段切换为MCTS深度利用，以自适应策略平衡探索与利用，克服纯BoN在高预算下的收益递减问题。



## 核心方法与创新机理

VFScale 的核心创新围绕一个关键瓶颈展开：**标准扩散模型在推理任务上的测试时扩展受限于能量景观质量差，缺乏性能-能量一致性**，导致单纯增加采样数量（Best-of-N）带来的增益十分有限。针对这一瓶颈，VFScale 通过两个相互协同的“changed slots”实现突破——训练端的损失函数重构与推理端的搜索策略升级，使扩散模型无需外部验证器即可实现有效的测试时扩展。

### 训练端：重塑能量景观的损失函数

原始基于能量的扩散模型（Du et al., 2024）使用 $`\mathcal{L}_{\mathrm{MSE}}`$ 与 $`\mathcal{L}_{\mathrm{Contrast}}`$ 进行训练，其能量函数虽能区分正负样本，但能量值与样本真实质量之间缺乏单调且一致的对应关系。VFScale 在训练目标中引入两个新组件：

**MRNCL 损失（单调回归负对比学习）** 是改善性能-能量一致性的核心机制。该损失通过线性回归约束，强制能量值 $`E`$ 与样本到真实解的 L2 距离之间保持单调且线性的关系：

$$`\mathcal{L}_{\mathrm{MRNCL}} = \mathbb{E}_{\mathbf{x}_0,\mathbf{x}_0^-,\mathbf{x}_0^{--},\epsilon,t} \big[ \max(0,\gamma - k_t) + \|E_t^+ - \hat{E}_t^+\|_2^2 + \|E_t^- - \hat{E}_t^-\|_2^2 + \|E_t^{--} - \hat{E}_t^{--}\|_2^2 \big]`$$

其中 $`k_t`$ 为回归斜率，$`\hat{E}`$ 为根据 L2 距离线性预测的能量值。这一约束直接解决了“低能量样本未必高质量”的根本问题——消融实验表明，移除 MRNCL 后，迷宫任务在 N=161 时的成功率从 0.7031 骤降至 0.4141（Table 3）；性能-能量一致性指标也从约 73% 提升至约 84%（Table 4）。

**KL 正则化** 进一步平滑能量景观并提升采样多样性：

$$`\mathcal{L}_{\mathrm{KL}} = \mathbb{E}_{t,p_{\theta,t}(\mathbf{x})} [E_{\mathrm{stop-grad}(\theta)}(\mathbf{x})] + \mathbb{E}_{t,p_{\theta,t}(\mathbf{x})} [\log p_{\theta,t}(\mathbf{x})]`$$

该损失鼓励采样点具有低能量和高熵，使搜索过程更容易在能量景观中导航。完整训练目标为：

$$`\mathcal{L} = \mathcal{L}_{\mathrm{MSE}} + \mathcal{L}_{\mathrm{Contrast}} + \mathcal{L}_{\mathrm{MRNCL}} + \mathcal{L}_{\mathrm{KL}}`$$

### 推理端：混合蒙特卡洛树搜索去噪

原始方法在推理时或使用单次迭代去噪，或使用 Best-of-N（BoN）并行采样后选择能量最低的样本。BoN 虽然能利用改进后的能量景观，但其纯探索策略在计算预算增大时效率递减。VFScale 提出 **hMCTS（混合蒙特卡洛树搜索）去噪**，将搜索过程嵌入扩散模型的迭代去噪步骤中：

- **早期阶段（噪声较大时）**：采用 BoN 的并行探索策略，快速覆盖解空间。
- **后期阶段（噪声较小时）**：切换为 MCTS 的树搜索，通过选择-扩展-模拟-回溯四步循环进行深度利用。MCTS 使用能量函数作为内在验证器计算节点价值，并通过 UCB 公式平衡探索与利用：

$$`\mathrm{UCB}(\mathbf{x}_t, \mathbf{a}_t) = Q(\mathbf{x}_t, \mathbf{a}_t) + c \sqrt{\frac{\ln N_i}{n_i}}`$$

扩展步骤通过添加不同高斯噪声产生多个分支子节点：

$$`\mathbf{x}_{t'-1}^{(k)} = \sqrt{\bar{\alpha}_{t'-1}} \frac{\mathbf{x}_{t'} - \sqrt{1-\bar{\alpha}_{t'}} \epsilon_\theta(\mathbf{x}_{t'},t')}{\sqrt{\bar{\alpha}_{t'}}} + \sqrt{1-\bar{\alpha}_{t'-1} - \sigma_{t'}^2} \epsilon_\theta(\mathbf{x}_{t'},t') + \sigma_{t'} \epsilon^{(k)}`$$

从 BoN 到 MCTS 的切换时机通过**能量方差自适应确定**，无需手动调优（Table 13 验证了自适应机制的有效性）。

### 创新协同效应

训练与推理两个 changed slots 高度协同：MRNCL 和 KL 正则化使能量函数成为可靠的内在验证器（Kendall-τ 秩相关性在去噪中间阶段保持 >0.4，显著优于外部验证器，Table 19）；hMCTS 则充分利用这一高质量能量信号进行高效搜索。在 15×15 迷宫任务上，VFScale + hMCTS（N=161）成功率达到 88.28%，较原始方法 + BoN 的 10.94% 提升超过 77 个百分点；相比仅改进训练的 VFScale + BoN（70.31%），hMCTS 进一步贡献约 18 个百分点的增益（Table 5）。在数独任务上同样展现出一致的扩展性优势。



![[assets/figures/papers/paper_list_l44_https_openreview_net_forum_id_8ta0xgtsJK/figures/002_Figure_2.jpg]]
*Figure 2: Overview of VFScale. This figure illustrates the key aspects of VFScale by contrasting its training and inference strategies with those of the previous method. (1) To qualify the intrinsic energy of diffusion models as a verifier, VFScale introduces $\mathcal { L } _ { \mathrm { M R N C L } }$ and $\mathcal { L } _ { \mathrm { K L } }$ to improve the energy landscape during training. (2) In order for a higher search efficiency, VFScale proposes hybrid Monte Carlo Tree Search (hMCTS) that achieves a balance between best-of-N and MCTS

![[assets/figures/papers/paper_list_l44_https_openreview_net_forum_id_8ta0xgtsJK/figures/001_Figure_1.jpg]]
*Figure 1: Visualizations of Maze training data and solutions generated by hMCTS denoising of our VFScale framework*

VFScale 的整体设计围绕一个核心洞察展开：**扩散模型自身的能量函数可以作为内在验证器**，为测试时扩展提供可靠的样本质量信号，从而摆脱对外部验证器的依赖。然而，标准扩散模型的能量景观质量较差，缺乏性能-能量一致性，导致增加采样数量带来的增益极为有限。VFScale 通过**训练阶段的能量景观改良**与**推理阶段的高效搜索策略**双管齐下，系统性地解决了这一瓶颈。

### 训练流水线：塑造可验证的能量景观

VFScale 的训练流水线在标准扩散训练基础上引入两个关键损失项，旨在将模型内在能量函数塑造为可靠的质量指示器。

**基础训练目标**沿用基于能量的扩散模型框架（Du et al., 2024），包含两个损失：

- **去噪损失** $ \mathcal{L}_{\mathrm{MSE}} $：标准 DDPM 噪声预测损失，确保模型具备基本的生成能力。
- **对比损失** $ \mathcal{L}_{\mathrm{Contrast}} $：促使正样本成为局部能量极小值，为能量函数赋予初步的判别能力。

**VFScale 新增的训练模块**直接针对能量景观的质量缺陷：

1. **单调回归负对比学习损失（MRNCL）** $ \mathcal{L}_{\mathrm{MRNCL}} $：该损失是 VFScale 训练的核心创新，通过强制能量值与样本质量（以 L2 距离为代理）之间保持单调且线性的关系，直接提升**性能-能量一致性**。具体而言，MRNCL 约束正样本、负样本和更负样本的能量预测满足线性回归关系，并惩罚斜率为负的情况。消融实验表明，移除 MRNCL 后，在 N=161 时迷宫成功率从 0.7031 骤降至 0.4141，性能-能量一致性指标也从约 84% 回落至约 73%，证实了 MRNCL 对能量景观质量的决定性作用。

2. **KL 正则化** $ \mathcal{L}_{\mathrm{KL}} $：在 MRNCL 基础上进一步平滑能量景观，鼓励采样点具有低能量和高熵，从而提升采样多样性并使搜索过程更容易导航。消融显示移除 KL 正则化同样导致性能下降，但影响较 MRNCL 略小。

完整的训练目标为：
$$ \mathcal{L} = \mathcal{L}_{\mathrm{MSE}} + \mathcal{L}_{\mathrm{Contrast}} + \mathcal{L}_{\mathrm{MRNCL}} + \mathcal{L}_{\mathrm{KL}} $$

值得注意的是，MRNCL 和 KL 的联合作用会**有意牺牲单次采样（N=1）的精度**，以换取能量景观的全局可导航性。这一设计选择是 VFScale 实现测试时扩展的关键——平坦而一致的能量景观使得增加采样预算能够持续带来性能提升，而非像标准模型那样迅速饱和。

### 推理流水线：混合蒙特卡洛树搜索去噪

VFScale 的推理流水线将测试时扩展从简单的 Best-of-N 选择升级为**混合蒙特卡洛树搜索（hMCTS）去噪**，充分利用改良后的能量景观进行高效搜索。

**能量函数预测器**是推理阶段的内在验证器：在去噪的每一步，模型前向传播输出能量值 $ E_\theta(\mathbf{x}_t, t) $，该能量直接作为样本质量的评分信号，无需任何外部验证器。实验表明，这一内在能量验证器在 Kendall-τ 秩相关性上显著优于外部训练的验证器，尤其在去噪中间阶段保持强正相关（>0.4），且性能几乎与完美的连续真实分数验证器相当，明显优于稀疏 0/1 验证器。

**hMCTS 去噪策略**采用两阶段设计，自适应地在探索与利用之间切换：

- **早期阶段（高噪声）**：使用 Best-of-N 并行探索，从同一噪声状态生成多个候选去噪路径，利用能量函数筛选优质分支。此时噪声较大，状态评估的可靠性有限，广泛的并行探索更为有效。
- **后期阶段（低噪声）**：切换为 MCTS 深度利用，通过选择、扩展、模拟、回溯四步循环进行树搜索。扩展步骤通过添加不同高斯噪声产生多个分支子节点，UCB 公式平衡探索与利用，最终选择累积价值最高的状态进入下一步去噪。

**自适应切换机制**利用能量方差自动确定从 BoN 切换到 MCTS 的时机，避免手动调优。实验显示，hMCTS 在相同函数评估次数（NFE）下将迷宫成功率从 BoN 的 0.7031 提升至 0.8828（N=161），增幅约 18%，而墙钟时间最多仅增加 31%。

### 模块关系与数据流

整体数据流如下：训练阶段，模型接收带噪样本，通过 MRNCL 和 KL 正则化学习性能-能量一致的能量景观；推理阶段，从纯噪声出发，hMCTS 在每一步去噪中利用内在能量函数评估候选状态，自适应地在 BoN 探索与 MCTS 利用之间切换，最终生成高质量解。

**局限性**：MCTS 的串行性质限制了并行加速能力，早期去噪阶段节点评估质量有限，且当前仅使用高斯噪声进行分支扩展，其他扩散分支机制仍有待探索。



### 3.1 瓶颈诊断：能量景观的质量缺陷

VFScale的设计出发点源于一个关键发现：标准扩散模型在推理任务上测试时扩展（test-time scaling）收益微薄，其根本原因并非采样数量不足，而是**能量景观（energy landscape）质量低下**，具体表现为**性能-能量一致性（performance-energy consistency）缺失**。原始训练方法下，Best-of-N（BoN）策略在N=161时迷宫成功率仅从6.25%提升至10.94%（Table 3），能量引导几乎无法区分高质量解与低质量解。这一瓶颈直接催生了VFScale的两大核心改进方向：通过训练改善能量景观质量，以及设计更高效的搜索策略来利用改善后的能量函数。

### 3.2 训练模块：MRNCL损失与KL正则化

VFScale在标准扩散训练损失（$\mathcal{L}_{\mathrm{MSE}}$ + $\mathcal{L}_{\mathrm{Contrast}}$）之上引入两个新增训练目标，共同改善能量景观。

**MRNCL损失（Monotonic-Regression Negative Contrastive Learning）**

该损失的核心动机是强制能量函数与样本质量之间建立单调且线性的关系。具体而言，对于每个正样本 $\mathbf{x}_0$，采样三个负样本 $\mathbf{x}_0^-$、$\mathbf{x}_0^{--}$ 以及正样本本身，在扩散时间步 $t$ 下分别计算其能量值 $E_t^+$、$E_t^-$、$E_t^{--}$，并基于它们与真实解之间的L2距离设定目标能量值 $\hat{E}_t^+$、$\hat{E}_t^-$、$\hat{E}_t^{--}$。MRNCL损失的完整形式为：

$$\mathcal{L}_{\mathrm{MRNCL}} = \mathbb{E}_{\mathbf{x}_0,\mathbf{x}_0^-,\mathbf{x}_0^{--},\epsilon,t} \big[ \max(0,\gamma - k_t) + \|E_t^+ - \hat{E}_t^+\|_2^2 + \|E_t^- - \hat{E}_t^-\|_2^2 + \|E_t^{--} - \hat{E}_t^{--}\|_2^2 \big]$$

其中 $k_t$ 为线性回归的斜率，$\gamma$ 为斜率下界阈值。该损失通过两项机制发挥作用：**$\max(0,\gamma - k_t)$** 强制能量-L2距离回归线的斜率为正（即质量越高的样本能量越低），**三个均方误差项** 则约束这种关系接近线性。消融实验直接验证了MRNCL的核心作用：移除该损失后，N=161时迷宫BoN成功率从0.7031骤降至0.4141（Table 3），性能-能量一致性指标从约84%回落至约73%（Table 4）。

**KL正则化**

在MRNCL改善能量-性能对齐的基础上，KL正则化进一步平滑能量景观并提高采样多样性：

$$\mathcal{L}_{\mathrm{KL}} = \mathbb{E}_{t,p_{\theta,t}(\mathbf{x})} [E_{\mathrm{stop-grad}(\theta)}(\mathbf{x})] + \mathbb{E}_{t,p_{\theta,t}(\mathbf{x})} [\log p_{\theta,t}(\mathbf{x})]$$

该损失鼓励模型采样分布 $p_{\theta,t}(\mathbf{x})$ 中的点同时具有低能量（第一项）和高熵（第二项），从而使得能量景观中的低能量区域更广阔、更易通过采样到达。消融表明移除KL正则化同样导致性能下降，但影响较MRNCL略小（Table 3）。

**完整训练目标**

VFScale的最终训练损失为四项之和：

$$\mathcal{L} = \mathcal{L}_{\mathrm{MSE}} + \mathcal{L}_{\mathrm{Contrast}} + \mathcal{L}_{\mathrm{MRNCL}} + \mathcal{L}_{\mathrm{KL}}$$

其中 $\mathcal{L}_{\mathrm{MSE}}$ 为标准扩散噪声预测损失，$\mathcal{L}_{\mathrm{Contrast}}$ 为对比损失（促使正样本成为局部能量极小值）。论文透明报告了训练开销：增加MRNCL和KL后训练时间约为原始方法的3倍，GPU内存占用也有所增加（Table 21, Table 22）。

### 3.3 推理模块：混合蒙特卡洛树搜索去噪（hMCTS）

改善后的能量函数作为内在验证器，仍需高效的搜索策略来充分释放测试时扩展潜力。VFScale提出**混合蒙特卡洛树搜索去噪（hMCTS）**，将去噪过程重构为树搜索问题。

**核心思想**：在去噪早期（$t$ 较大，噪声水平高），节点状态评估质量有限，采用**Best-of-N（BoN）并行探索**以覆盖多样解空间；在去噪后期（$t$ 较小，噪声水平低），切换为**MCTS深度利用**以精细优化当前候选解。

**MCTS节点选择**采用标准置信上限公式：

$$\mathrm{UCB}(\mathbf{x}_t, \mathbf{a}_t) = Q(\mathbf{x}_t, \mathbf{a}_t) + c \sqrt{\frac{\ln N_i}{n_i}}$$

其中 $Q(\mathbf{x}_t, \mathbf{a}_t)$ 为状态-动作对的累积价值（由能量函数反向传播获得），$N_i$ 为父节点访问次数，$n_i$ 为子节点访问次数，$c$ 为探索常数。

**MCTS扩展步骤**通过向去噪过程注入不同高斯噪声产生多个分支子节点：

$$\mathbf{x}_{t'-1}^{(k)} = \sqrt{\bar{\alpha}_{t'-1}} \frac{\mathbf{x}_{t'} - \sqrt{1-\bar{\alpha}_{t'}} \epsilon_\theta(\mathbf{x}_{t'},t')}{\sqrt{\bar{\alpha}_{t'}}} + \sqrt{1-\bar{\alpha}_{t'-1} - \sigma_{t'}^2} \epsilon_\theta(\mathbf{x}_{t'},t') + \sigma_{t'} \epsilon^{(k)}$$

其中 $\epsilon^{(k)}$ 为第 $k$ 个分支的独立高斯噪声，$\sigma_{t'}$ 控制分支多样性。模拟阶段使用DDIM快速采样获得预测的 $\hat{\mathbf{x}}_0$，并以能量函数 $E_\theta$ 作为奖励进行反向传播。

**自适应切换机制**利用能量方差自动确定从BoN切换到MCTS的时机，避免手动调参。消融实验表明自适应机制与手动调优的最优固定切换步性能相当（Table 13），且hMCTS在相同函数评估次数（NFE）下将迷宫成功率从BoN的0.7031提升至0.8828（Table 5），额外墙钟时间开销最多31%（Table 23）。

### 3.4 模块协同机制

VFScale的训练模块与推理模块形成闭环协同：MRNCL和KL正则化使能量函数成为可靠的内在验证器（Kendall-$\tau$ 秩相关性在去噪中间阶段保持 $>0.4$，Table 19），hMCTS则高效利用这一验证器进行结构化搜索。消融实验提供了因果证据：使用外部训练的验证器替代内在能量函数，迷宫成功率下降超过30个百分点（Table 10）；内在能量验证器几乎与完美的连续真实分数验证器性能相当，明显优于稀疏0/1验证器（Table 11）。这证实了VFScale的核心主张——**扩散模型自身的能量函数经适当训练后，可以作为无需外部验证器的测试时扩展内在验证器**。



## 实验与关键发现

### 核心瓶颈：能量景观质量限制了测试时扩展

标准扩散模型在推理任务上的测试时扩展面临一个根本性瓶颈：**能量景观质量差，缺乏性能-能量一致性**。这意味着模型的能量函数无法可靠地反映样本质量，导致增加采样数量（Best-of-N）带来的增益极为有限。如表2所示，原始训练方法使用能量引导的Best-of-N在迷宫15×15任务上，N从1增加到161时成功率仅从6.25%提升至10.94%；在困难数独任务上，N=321时也仅达到28.12%。这一现象揭示了问题的本质：单纯增加计算预算无法弥补能量函数与样本质量之间的错位。

![[assets/figures/papers/paper_list_l44_https_openreview_net_forum_id_8ta0xgtsJK/figures/006_Table_2.jpg]]
*Table 2: Success rate of BoN for different training methods on Maze with grid size 15 and Sudoku harder dataset guided with ground truth. Here, L = N*

### 训练改进：MRNCL损失与KL正则化的消融分析

VFScale通过两个关键训练组件改善能量景观：**单调回归负对比学习（MRNCL）损失**和**KL正则化**。表3的消融实验量化了各组件的贡献：

![[assets/figures/papers/paper_list_l44_https_openreview_net_forum_id_8ta0xgtsJK/figures/007_Table_3.jpg]]
*Table 3: Success rate on Maze with grid size 15 and Sudoku harder dataset for comparison of the model’s ability to scale up under BoN with different training methods. Here, L = N*

- **完整VFScale训练**（含MRNCL+KL）在BoN推理下，迷宫15×15成功率从原始训练的10.94%（N=161）大幅提升至**70.31%**，数独任务从28.12%提升至**39.06%**（N=321）。
- **移除MRNCL损失**（w/o MRNCL）使迷宫成功率骤降至41.41%，降幅近29个百分点，证明MRNCL是测试时扩展能力的核心驱动力。
- **移除KL正则化**（w/o KL）同样导致性能下降，但影响较MRNCL略小，在N=161时迷宫成功率为64.06%。

表4进一步从机制层面验证了MRNCL的作用：**性能-能量一致性指标**从原始训练的约73%提升至约84%（VFScale w/o KL），提升超过10个百分点。这一指标直接量化了能量排序与样本质量排序之间的一致性，是测试时扩展能否奏效的关键前提。

![[assets/figures/papers/paper_list_l44_https_openreview_net_forum_id_8ta0xgtsJK/figures/008_Table_4.jpg]]
*Table 4: Performance-energy consistency of BoN on Maze with grid size 15 to test the effect of MRNCL loss. Here, L = N . Details of consistency calculation can be found in Appendix A*

值得注意的是，VFScale训练在单次生成（N=1）时的表现并非最优：原始训练在迷宫15×15上N=1成功率为6.25%，而VFScale训练为28.12%（表1）。论文明确指出，联合目标（MRNCL+KL）的设计意图是**平滑能量景观以确保全局可导航性**，这有意牺牲了单点精度以换取测试时扩展的巨大增益——这正是“内在推理”范式的核心取舍。

![[assets/figures/papers/paper_list_l44_https_openreview_net_forum_id_8ta0xgtsJK/figures/005_Table_1.jpg]]
*Table 1: Success rate across different grid sizes of Maze and various number of given entries for naïve inference (N = 1) for comparison of the generalization ability of models obtained by different training methods. Let M denote the grid size of Maze and D denote the number of given digits in Sudoku. Original denotes the original training method in Du et al. (2024). VFScale tr. (ours) denotes our full training method, and this naming convention is used for following figures and tables. Bold font denotes the best model, and an underline denotes the second-best model. The same markings are used in the tables below*

### 推理改进：混合蒙特卡洛树搜索（hMCTS）的关键增益

在改善能量景观的基础上，VFScale进一步将**混合蒙特卡洛树搜索（hMCTS）**引入去噪过程。表5展示了完整方法的主要结果：

![[assets/figures/papers/paper_list_l44_https_openreview_net_forum_id_8ta0xgtsJK/figures/010_Table_5.jpg]]
*Table 5: Success rate of different approaches on Maze with grid size 15 and Sudoku harder dataset. Here, N _ { r } = N , K = N , L = N*

- **迷宫15×15**：VFScale + hMCTS在N=161时达到**88.28%**成功率，相比VFScale + BoN（70.31%）提升约18个百分点，相比原始训练+BoN（10.94%）提升超过77个百分点。标准扩散模型在此任务上完全失败。
- **困难数独**（17-33个给定数字）：VFScale + hMCTS在N=321时达到**42.97%**成功率，相比VFScale + BoN（39.06%）和原始训练+BoN（28.12%）均有显著提升。

hMCTS的核心设计在于**自适应切换策略**：在早期噪声较大时使用Best-of-N进行并行探索，后期噪声较小时切换为MCTS进行深度利用。表13显示，自适应切换机制在较小计算预算下（N=11时成功率21.09% vs 手动调优的14.06%）展现出明显优势。表14进一步分析了MCTS起始步的影响，验证了在适当去噪阶段启动树搜索对性能至关重要。

### 内在能量验证器的优越性

VFScale的一个核心主张是**扩散模型自身的能量函数可以作为内在验证器**，无需额外训练外部验证器。表10直接对比了两种方案：内在能量验证器在N=81时迷宫成功率达68.75%，而使用相同样本集训练的外部验证器仅为32.03%，**性能差距超过36个百分点**。更关键的是，外部验证器在N>21后出现性能退化，表明其泛化能力不足。

![[assets/figures/papers/paper_list_l44_https_openreview_net_forum_id_8ta0xgtsJK/figures/018_Table_10.jpg]]
*Table 10: Comparison of test-time scaling performance on the 15 × 15 Maze task using our intrinsic energy verifier versus a trained external verifier. Both methods use the same set of generated samples under the Best-of-N (BoN) framework. Success rates are reported for different compute budgets (N )*

表11将内在验证器与两种**完美真实值预言机**对比：内在能量引导的hMCTS性能几乎与连续真实分数验证器相当，并明显优于稀疏0/1验证器。这一结果说明，经过MRNCL和KL训练的能量函数已能高度逼近真实质量信号。

表19从秩相关性角度提供了更深层证据：内在能量验证器在去噪中间阶段与真实质量的**Kendall-τ相关性保持在0.4以上**，而外部验证器与基线方法的相关性显著更低。这种全局对齐能力是内在验证器成功的关键。

### MRNCL变体与设计选择

表12对比了不同单调回归约束变体：**线性回归MRNCL（LRNCL）**虽然在N=1时（35.16%）不及二次回归QRNCL（35.16%持平），但在测试时扩展上表现最佳，N=81时达到58.59%，超过所有其他变体。这表明严格的线性约束可能为能量景观提供了更稳定的全局结构。

表17进一步分析了负样本生成策略对LRNCL的影响，验证了当前策略的有效性。

### 计算开销与效率权衡

论文透明报告了训练与推理的额外开销：

- **训练开销**：完整VFScale训练（+MRNCL+KL）时间约为原始方法的3倍（表21），GPU内存消耗也有所增加（表22）。
- **推理开销**：hMCTS在相同函数评估次数（NFE）下，墙钟时间最多增加约31%（如N=81时26.48秒 vs BoN的20.16秒，表23）。这一开销源于MCTS的串行性质，是搜索效率与并行能力之间的固有权衡。

所有推理对比均在相同NFE下进行，确保计算预算公平。

### 失败模式与局限性

尽管VFScale取得了显著进展，仍存在明确的局限性：

1. **MCTS串行瓶颈**：MCTS固有的串行性质限制了并行加速能力，导致推理时间额外开销，在需要极低延迟的场景中可能不适用。
2. **早期去噪阶段评估质量有限**：在噪声较大的早期步骤，节点状态评估的可靠性不足，可能影响搜索树的质量。
3. **能量引导与真实值引导之间的剩余差距**：表2和表5的对比显示，能量引导的测试时扩展仍与真实值引导存在差距，表明能量景观尚有优化空间。
4. **MRNCL严格约束的灵活性不足**：线性回归约束可能对某些任务不够灵活，需进一步探索替代正则化方案。
5. **分支扩展机制单一**：当前仅使用高斯噪声进行MCTS分支扩展，其他扩散分支机制仍有待研究。

### 补充图表

![[assets/figures/papers/paper_list_l44_https_openreview_net_forum_id_8ta0xgtsJK/figures/004_Figure_3.jpg]]
*Figure 3: Scalability of different approaches on Maze and Sudoku*

![[assets/figures/papers/paper_list_l44_https_openreview_net_forum_id_8ta0xgtsJK/figures/011_Figure_5.jpg]]
*Figure 5: The model architecture for VFScale on Sudoku task. The energy value is computed using the L2 norm of the final predicted output similar to Du et al. (2023), while the output is directly used as noise prediction for the diffusion baseline*

![[assets/figures/papers/paper_list_l44_https_openreview_net_forum_id_8ta0xgtsJK/figures/012_Table_6.jpg]]
*Table 6: Details of training for Sudoku task*

![[assets/figures/papers/paper_list_l44_https_openreview_net_forum_id_8ta0xgtsJK/figures/013_Figure_6.jpg]]
*Figure 6: The model architecture for VFScale on Maze task. The energy value is computed using the L2 norm of the final predicted output similar to Du et al. (2023), while the output is directly used as noise prediction for the diffusion baseline*



## 定位与知识库关联

### 核心瓶颈与因果机制

VFScale 的核心诊断是：标准扩散模型在推理任务上的测试时扩展（test-time scaling）受限于**能量景观（energy landscape）质量差**，具体表现为缺乏**性能-能量一致性（performance-energy consistency）**。这意味着模型内在能量函数对样本质量的排序能力弱，导致增加采样数量（如 Best-of-N）带来的增益有限——在 15×15 迷宫任务上，原始训练的 BoN 在 N=161 时成功率仅从 6.25% 提升至 10.94%（Table 3），扩展几乎无效。

因果调节变量有两个层面：
1. **训练层面**：通过 MRNCL 损失（单调回归负对比学习）强制能量与样本质量（L2 距离）之间的单调线性关系，辅以 KL 正则化平滑能量景观并提高采样多样性。
2. **推理层面**：将混合蒙特卡洛树搜索（hMCTS）引入去噪过程，早期噪声大时使用 BoN 并行探索，后期噪声小时切换为 MCTS 深度利用，由能量方差自适应决定切换时机。

核心洞察在于：**扩散模型自身的能量函数可以作为内在验证器（intrinsic verifier）**，无需额外训练外部验证模型，只要通过定制训练使能量景观与样本质量对齐，再结合高效搜索策略，即可实现免验证器的测试时扩展。

### 与基线工作的关系

VFScale 直接建立在基于能量的扩散模型工作之上，其基线方法为 **energy-based diffusion model**（Du et al., 2024），该基线使用 $L_{\text{MSE}} + L_{\text{Contrast}}$ 训练，但未针对测试时扩展设计专门的训练或推理策略。VFScale 在此基础上的关键改动如下表所示：

| 改动槽位 | 基线值 | VFScale 值 | 证据锚点 |
|---------|--------|-----------|---------|
| 训练损失函数 | $L_{\text{MSE}} + L_{\text{Contrast}}$ | $L_{\text{MSE}} + L_{\text{Contrast}} + L_{\text{MRNCL}} + L_{\text{KL}}$ | Eq.6, Section 4.2 |
| 推理搜索策略 | 原始迭代去噪或 Best-of-N | 混合蒙特卡洛树搜索去噪（hMCTS） | Section 4.3, Algorithm 1 |

MRNCL 损失是该工作的核心训练创新，其数学形式为：

$$\mathcal{L}_{\mathrm{MRNCL}} = \mathbb{E}_{\mathbf{x}_0,\mathbf{x}_0^-,\mathbf{x}_0^{--},\epsilon,t} \big[ \max(0,\gamma - k_t) + \|E_t^+ - \hat{E}_t^+\|_2^2 + \|E_t^- - \hat{E}_t^-\|_2^2 + \|E_t^{--} - \hat{E}_t^{--}\|_2^2 \big]$$

该损失通过三个负样本（$x_0^-$、$x_0^{--}$ 及正样本 $x_0^+$）构建能量-L2 距离的单调回归约束，强制斜率 $k_t > \gamma$ 且关系接近线性。消融实验（Table 3）表明，移除 MRNCL 使迷宫成功率从 0.7031 降至 0.4141（N=161），证明其是测试时扩展能力的关键来源。

KL 正则化损失进一步鼓励采样点具有低能量和高熵：

$$\mathcal{L}_{\mathrm{KL}} = \mathbb{E}_{t,p_{\theta,t}(\mathbf{x})} [E_{\mathrm{stop-grad}(\theta)}(\mathbf{x})] + \mathbb{E}_{t,p_{\theta,t}(\mathbf{x})} [\log p_{\theta,t}(\mathbf{x})]$$

移除 KL 同样导致性能下降，但影响较 MRNCL 略小（Table 3）。

### 方法谱系定位

VFScale 处于**扩散模型推理优化**与**测试时计算扩展（test-time compute scaling）**的交叉点。其方法谱系可沿两条线索追溯：

1. **基于能量的扩散模型**：继承自 Du et al.（2024）的对比训练框架，但 VFScale 的关键突破在于认识到原始能量景观的“不可导航性”是测试时扩展失败的根本原因，并通过 MRNCL 和 KL 显式重塑能量景观。Table 4 的性能-能量一致性指标从约 73% 提升至约 84%，直接量化了这一改善。

2. **测试时搜索策略**：hMCTS 将 MCTS 引入扩散去噪过程，区别于传统的 Best-of-N（纯并行探索）和完全的 MCTS（串行搜索）。其设计逻辑利用了扩散过程的特性——早期步骤噪声大、状态评估不可靠，适合 BoN 的广度探索；后期步骤信号清晰，适合 MCTS 的深度利用。Table 5 显示，在相同 NFE 下，hMCTS 较 BoN 将迷宫成功率从 0.7031 提升至 0.8828（N=161），提升约 18 个百分点。

### 适用边界与局限

**适用边界**：
- VFScale 在组合推理任务（迷宫、数独）上验证有效，这些任务具有明确的离散约束和可评估的正确性标准。
- 方法假设扩散模型的能量函数可通过训练与样本质量对齐，适用于能量预测架构（如 Du et al., 2024 的框架）。
- hMCTS 的自适应切换机制依赖能量方差作为信号，在去噪过程具有明显阶段转换特征的任务上效果更好。

**明确局限**（论文自述）：
1. **MCTS 的串行瓶颈**：MCTS 固有的串行性质限制了并行加速能力。Table 23 显示，相同 NFE 下 hMCTS 墙钟时间最多增加 31%（如 N=81 时 26.48s vs BoN 20.16s），性能提升以额外推理时间为代价。
2. **早期阶段评估质量有限**：去噪早期步骤节点状态评估质量有限，可能影响搜索效果。Table 14 显示 MCTS 起始步的选择对性能有显著影响。
3. **MRNCL 的刚性约束**：线性回归约束对全局能量排序的强制可能对某些任务不够灵活。Table 12 的消融显示线性回归变体（LRNCL）在测试时扩展上表现最佳，但其他单调约束形式（如二次回归）在某些设置下可能更有优势。
4. **分支机制单一**：当前仅使用高斯噪声进行分支扩展（Eq.8），其他扩散分支机制仍有待研究。

**训练开销**：Table 21 显示，增加 MRNCL+KL 训练后，训练时间约为原始方法的 3 倍（迷宫任务从 6.5h 增至 19.5h，数独任务从 4.5h 增至 13.5h），GPU 内存也有增加（Table 22）。论文透明报告了这些成本。

### 开放问题

1. **能量引导与真实值引导的剩余差距**：Table 2 显示，即使经过 VFScale 训练，能量引导的 BoN 与真实解引导的 BoN 之间仍存在显著差距（迷宫 N=161 时 0.7031 vs 0.9844）。如何进一步改善训练方法以消除这一差距，是完全释放测试时扩展潜力的关键。

2. **更高效的搜索算法设计**：BoN 面临性能平台化，MCTS 存在串行开销，两者各有短板。能否设计结合二者优势且更易并行的搜索策略，是该方向的开放挑战。

3. **MRNCL 的数学理解**：线性回归约束对全局能量排序的影响是否有更深的数学解释？Table 19 显示内在能量验证器在 Kendall-τ 秩相关性上显著优于外部验证器，尤其在去噪中间阶段保持强正相关（>0.4），但其理论保证尚不明确。

4. **跨领域推广**：hMCTS 的自适应切换机制能否推广到连续控制或自然语言等其他推理领域？当前仅在离散组合任务上验证，泛化性需要进一步研究。

5. **负样本策略的影响**：Table 17 显示不同负样本生成策略对 LRNCL 效果有影响，最优负样本构造方式仍有探索空间。



## 原文 PDF

![[paperPDFs/ICLR_2026/VFScale_Intrinsic_Reasoning_through_Verifier_Free_Test_time_Scalable_Diffusion_Model.pdf]]
