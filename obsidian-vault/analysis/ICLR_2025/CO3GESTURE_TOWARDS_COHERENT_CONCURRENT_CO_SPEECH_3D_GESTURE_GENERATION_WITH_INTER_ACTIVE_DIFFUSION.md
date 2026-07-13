---
title: "CO3GESTURE: TOWARDS COHERENT CONCURRENT CO-SPEECH 3D GESTURE GENERATION WITH INTER- ACTIVE DIFFUSION"
type: paper
paper_level: A
venue: ICLR
year: 2025
pdf_ref: paperPDFs/ICLR_2025/CO3GESTURE_TOWARDS_COHERENT_CONCURRENT_CO_SPEECH_3D_GESTURE_GENERATION_WITH_INTER_ACTIVE_DIFFUSION.pdf
project_link: https://mattie-e.github.io/Co3/
code_link: null
aliases:
- CO3GESTURE
tags:
- ICLR_2025
- topic/benchmarks_datasets_evaluation
- topic/benchmarks_datasets_evaluation/benchmark_eval
core_operator: "提出双边协作扩散生成框架Co3Gesture，使用分离的说话人音频分别驱动两个生成分支，并通过时序交互模块（TIM）显式建模两位说话人手势序列间的时序关联，以及互注意力机制增强跨说话人的特征交互，从而实现连贯的并发交互手势生成。"
primary_logic: "两人对话时身体动态呈不对称性，因此分别条件于不同说话人音频生成手势比分主模式合成更自然；利用混合音频提取全局交互线索，通过可学习权重平衡自身语音驱动与交互驱动，再通过互注意力交换跨说话人特征，能够有效确保手势的时序一致与交互连贯。"
claims:
- "Co3Gesture 在 GES-Inter 数据集上的 FGD 为 0.769，相较于次优方法 InterGen 的 1.012 降低 24%，且 BC 和 Diversity 均明显领先。"
- "消融研究中移除 TIM 导致 FGD 从 0.769 升至 1.297，移除互注意力则升至 0.924，验证了两个模块对交互建模的关键作用。"
- "移除双边分支、单独使用混合音频或移除脚部接触损失均导致 FGD/BC 显著恶化，进一步证实各设计组件的重要性。"
- "用户研究（15 名参与者）显示 Co3Gesture 在自然度(4.4)、流畅度(4.5)和交互连贯性(4.2)上均获最高评分，t 检验表明显著优于所有对比方法（p < 0.05）。"
---

# CO3GESTURE: TOWARDS COHERENT CONCURRENT CO-SPEECH 3D GESTURE GENERATION WITH INTER- ACTIVE DIFFUSION

> [!tip] 核心洞察
> 两人对话时身体动态呈不对称性，因此分别条件于不同说话人音频生成手势比分主模式合成更自然；利用混合音频提取全局交互线索，通过可学习权重平衡自身语音驱动与交互驱动，再通过互注意力交换跨说话人特征，能够有效确保手势的时序一致与交互连贯。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Co3Gesture：面向交互式扩散的连贯并发语音驱动3D手势生成 |
| 英文题名 | CO3GESTURE: TOWARDS COHERENT CONCURRENT CO-SPEECH 3D GESTURE GENERATION WITH INTER- ACTIVE DIFFUSION |
| 会议/期刊 | ICLR 2025 |
| Links | [paper](https://openreview.net/pdf?id=VaowElpVzd) · [Project](https://mattie-e.github.io/Co3/) |
| Topic | #topic/benchmarks_datasets_evaluation #topic/benchmarks_datasets_evaluation/benchmark_eval |
| Method | Co3Gesture |
| Dataset | GES-Inter Dataset |

> [!tip] 效果简介
> - GES-Inter Dataset 上，FGD (↓) 为 0.769，对比 1.012 (InterGen, sub-optimal)，变化 -0.243 (↓24.0%)。
> - GES-Inter Dataset 上，BC (Beat Consistency ↑) 为 0.692，对比 0.670 (InterGen)，变化 +0.022。
> - GES-Inter Dataset 上，Diversity (↑) 为 72.824，对比 69.455 (InterGen)，变化 +3.369。

## 概要

当前语音驱动的3D手势生成方法均聚焦于单人自述场景，无法处理实时对话中双人异步、交互并发的动态手势。这一瓶颈的根源在于两方面：其一，现有方法缺乏对两位说话人之间时序关联与跨说话人依赖的显式建模；其二，该方向长期缺少大规模、高质量的双人并发语音-手势数据集。

针对上述问题，本文提出 **Co3Gesture**，一个基于双边协作扩散的并发语音手势生成框架。其核心思路是：利用分离的说话人音频分别驱动两个生成分支，通过时序交互模块（TIM）显式建模两人手势序列间的时序关联，并引入互注意力机制实现跨说话人的特征交换，从而确保生成手势的时序一致与交互连贯。此外，本文构建了 **GES-Inter** 数据集，包含超过 70 小时、700 万帧的高质量双人对话语音-手势数据，为这一方向提供了基准。

在 GES-Inter 上的实验表明，Co3Gesture 的 FGD 达到 0.769，较次优方法 InterGen（1.012）降低 24%，同时在节拍一致性（BC 0.692）和多样性（Diversity 72.824）上均显著领先。消融研究证实，TIM 和互注意力机制是交互建模的关键组件：移除 TIM 后 FGD 升至 1.297，移除互注意力后升至 0.924。用户研究进一步验证了 Co3Gesture 在自然度（4.4）、流畅度（4.5）和交互连贯性（4.2）上的感知优势（p < 0.05）。

**方法定位**：Co3Gesture 属于并发交互手势生成的扩散模型方法，其双边分支架构、时序交互模块与互注意力机制构成了区别于单人生成基线（如 TalkSHOW、DiffSHEG、EMAGE）和人-人交互基线（如 InterGen、InterX）的核心差异。



语音驱动的 3D 手势生成（co-speech gesture generation）旨在根据语音信号合成与说话内容节奏同步、语义匹配的肢体动作，在虚拟数字人、沉浸式交互等领域具有重要应用。近年来，基于扩散模型的方法在该任务上取得了显著进展，代表性工作包括 **TalkSHOW**（Yi et al., CVPR 2023）、**ProbTalk**（Liu et al., CVPR 2024b）、**DiffSHEG**（Chen et al., CVPR 2024）和 **EMAGE**（Liu et al., CVPR 2024a）等。然而，这些方法存在一个根本性局限：它们均面向**单人自述场景**设计，无法处理真实对话中两人交替发言、手势彼此呼应的复杂交互动态。

从问题本质来看，两人对话场景的挑战远非将单人生成模型简单叠加所能解决。首先，对话双方的身体动态呈现**不对称性**——一方说话时，另一方可能以点头、手势回应或保持静默倾听，这种主次分明的交互模式需要模型显式区分不同说话人的音频条件。其次，并发手势之间存在**时序关联**：一方的动作往往是对另一方语音或手势的响应，缺乏跨说话人的时序建模将导致生成的动作各自孤立，丧失交互连贯性。此外，现有数据集几乎全部采集自单人独白场景，**缺乏大规模、高质量的双人并发语音-手势数据**，进一步制约了这一方向的研究。

在交互动作生成领域，**InterGen**（Liang et al., IJCV 2024b）和 **InterX**（Xu et al., CVPR 2024）等工作探索了基于文本描述的双人交互动作合成，但它们以文本而非语音为条件，无法捕捉语音韵律与手势节奏之间的细粒度耦合关系。因此，如何在语音驱动框架下实现连贯的并发交互手势生成，仍是一个开放问题。

Co3Gesture 正是在这一背景下提出的。其核心动机可以概括为三个层次：第一，**填补并发语音手势生成的任务空白**，将研究从单人场景拓展至双人对话；第二，**构建首个大规模双人并发语音-手势数据集 GES-Inter**，为该方向提供数据基础；第三，**设计双边协作扩散框架**，通过分离音频条件、时序交互建模和跨说话人注意力机制，确保生成手势既保持个体与自身语音的同步，又具备双方之间的交互连贯性。



## 核心方法与创新机理

Co3Gesture 的核心创新在于将并发语音驱动手势生成从单人独白范式推向了双人交互范式，其关键设计围绕三个紧密耦合的“changed slots”展开。

**1. 双边协作扩散架构（Bilateral Cooperative Diffusion Branches）**

现有方法（如 **TalkSHOW** (Yi et al., CVPR 2023)、**InterGen** (Liang et al., IJCV 2024b)）采用单一生成分支处理双人姿态，无法捕捉对话中两人身体动态的天然不对称性。Co3Gesture 建立了两个共享权重的 Transformer 扩散去噪分支，每个分支分别条件于对应说话人的分离音频（separated speaker audio），从结构上解耦了两位说话人的手势生成过程。这一设计使模型能够独立响应各自语音的韵律与节奏，同时通过后续交互模块实现协同。消融实验表明，将双边分支替换为单分支后，FGD 从 0.769 骤升至 1.669（Table 4），验证了双边架构对处理非对称并发动态的必要性。

**2. 时序交互模块（Temporal Interaction Module, TIM）**

单纯的音频分离会丢失对话双方的交互线索。TIM 通过交叉注意力机制和可学习权重 $\sigma$，显式建模两位说话人手势序列间的时序关联。具体而言，TIM 以当前说话人的音频嵌入作为查询 $\mathbf{Q}$，以其运动嵌入作为键 $\mathbf{K}$ 和值 $\mathbf{V}$ 进行交叉注意力计算（Eq. 1），随后利用从时序相关矩阵 $\mathbf{M}$ 学到的权重 $\sigma$，将说话人自身的语音驱动嵌入 $\mathbf{f}_{x_a, C_a}$ 与混合音频（mixed audio）驱动的交互嵌入 $\mathbf{f}_{x_a, C_{mix}}$ 进行加权融合：

$$\mathbf{f}_{x_a, C_a} = \sigma \odot \mathbf{f}_{x_a, C_a} + (1 - \sigma) \odot \mathbf{f}_{x_a, C_{mix}}, \quad \sigma = \text{sigmoid}(\text{Enc}(\mathbf{M}))$$

这一公式（Eq. 2）是平衡“个体节奏保持”与“交互依赖建模”的核心因果旋钮。移除 TIM 后，FGD 从 0.769 升至 1.297，BC 和 Diversity 均大幅下降（Table 3），证明时序交互建模对并发手势同步性具有决定性作用。

**3. 互注意力机制（Mutual Attention Mechanism）**

在双边去噪器之间引入互注意力层，以对方分支的特征作为多头注意力中的查询 $\mathbf{Q}$，实现跨说话人的特征交换与共享权重更新。该机制使每个分支在去噪过程中能够感知对方当前的手势状态，从而增强交互的连贯性与响应性。消融实验显示，移除互注意力后 FGD 升至 0.924（Table 3），表明跨说话人特征交换对交互连贯性有显著贡献。

**4. 损失函数的增强**

在标准简单扩散损失 $\mathcal{L}_{simple}$（Eq. 3）基础上，引入速度损失 $\mathcal{L}_{vel}$ 和脚部接触损失 $\mathcal{L}_{foot}$，构成总训练目标：

$$\mathcal{L}_{total} = \lambda_{simple} \mathcal{L}_{simple} + \mathcal{L}_{vel} + \mathcal{L}_{foot}$$

其中 $\lambda_{simple}=15$。速度损失约束运动平滑性，脚部接触损失则针对下半身关节（以 T-pose 补全）施加物理合理性约束。移除 $\mathcal{L}_{foot}$ 后 FGD 升至 1.082（Table 5），验证了该损失对提升生成姿态物理合理性的作用。

综上，Co3Gesture 通过“双边分支解耦个体动态 + TIM 融合交互线索 + 互注意力交换跨说话人特征”的三层递进设计，系统性地解决了并发手势生成中的个体响应与交互连贯这一核心矛盾。



![[assets/figures/papers/paper_list_l20_https_openreview_net_pdf_id_VaowElpVzd/figures/004_Figure_3.jpg]]
*Figure 3: The overall pipeline of our $\mathrm { C o ^ { 3 } G e s t u r e }$ . Given conversational speech audios, our framework generates concurrent co-speech gestures with coherent interactions*

Co3Gesture 的整体 pipeline 围绕一个核心洞察构建：双人对话中的身体动态具有天然的不对称性，因此分别以不同说话人的分离音频作为条件生成手势，比分主模式（即以单一混合音频驱动双方姿态）更符合真实交互规律。基于此，框架采用**双边协作扩散生成架构**，其输入输出流与模块关系如下。

**输入与条件信号。** 系统接收一段双人对话音频，并从中提取三类条件信息：
- 说话人 A 的分离音频 $C_a$ 与说话人 B 的分离音频 $C_b$，分别作为各自手势生成分支的主要驱动信号；
- 原始混合对话音频 $C_{mix}$，用于提供全局交互线索。

**双边扩散去噪主干。** 框架包含两个共享权重更新策略的 Transformer 去噪分支，分别负责生成说话人 A 和 B 的上半身手势序列 $x_a$ 与 $x_b$。每个分支以对应说话人的分离音频为条件，在扩散时间步 $t$ 的引导下，从噪声手势逐步恢复出干净手势。这种双边设计使得两个分支能够独立捕捉各自说话人的语音节奏与个体运动特征，同时保留交互协同的空间。

**时序交互模块（TIM）。** 在每一分支内部，TIM 负责将“自身语音驱动”与“交互驱动”进行融合。具体而言，TIM 首先以当前说话人的音频嵌入作为查询 $Q$、以该说话人的运动嵌入作为键 $K$ 和值 $V$，通过交叉注意力计算自身语音驱动的嵌入表示 $f_{x_a, C_a}$。随后，TIM 利用混合音频 $C_{mix}$ 提取交互嵌入 $f_{x_a, C_{mix}}$，并通过一个可学习的时序相关权重 $\sigma$ 对两者进行加权融合：

$$f_{x_a, C_a} = \sigma \odot f_{x_a, C_a} + (1 - \sigma) \odot f_{x_a, C_{mix}}, \quad \sigma = \text{sigmoid}(\text{Enc}(M))$$

其中 $M$ 为时序相关矩阵，$\sigma$ 动态平衡个体节奏保持与交互依赖建模。这一机制确保了手势在时间维度上既与自身语音同步，又能响应对话伙伴的节奏变化。

**互注意力机制。** 在双边去噪器之间，框架引入互注意力层以增强跨说话人特征交互。具体做法是，每个分支将对方分支的特征作为多头注意力中的查询 $Q$，实现特征级别的双向交换。这使得两位说话人的手势生成过程不再彼此独立，而是能够显式感知并协调对方的运动状态，从而提升交互连贯性。

**输出与训练目标。** 两个分支最终输出说话人 A 和 B 的并发 3D 手势序列，包含 46 个上半身关节的旋转表示。训练时，总损失函数由三项构成：

$$\mathcal{L}_{total} = \lambda_{simple} \mathcal{L}_{simple} + \mathcal{L}_{vel} + \mathcal{L}_{foot}$$

其中 $\mathcal{L}_{simple}$ 为简单扩散重建损失（$\lambda_{simple}=15$），分别约束两位说话人的去噪输出与真实手势之间的均方误差；$\mathcal{L}_{vel}$ 为速度损失，保证运动平滑性；$\mathcal{L}_{foot}$ 为脚部接触损失，用于提升姿态的物理合理性。

综上，Co3Gesture 通过“分离音频驱动双边分支—TIM 融合交互信息—互注意力交换跨说话人特征”的级联设计，实现了从对话音频到连贯并发手势的端到端生成。消融实验表明，移除 TIM 会导致 FGD 从 0.769 升至 1.297，移除互注意力则升至 0.924，验证了各模块在交互建模中的关键作用（Table 3）。



### 双边协作扩散主干

Co3Gesture 的核心架构由两个共享权重的 Transformer 扩散分支构成，分别以分离后的说话人音频 $C_a$、$C_b$ 作为条件，驱动对应说话人的手势去噪过程。与以往使用单一分支整体生成双人姿态的方法（如 **InterGen**，Liang et al., IJCV 2024）不同，双边设计显式建模了对话中两人身体动态的不对称性——消融实验表明，移除双边分支使 FGD 从 0.769 骤升至 1.669（Table 4），验证了该架构对并发手势生成的关键作用。

### 时序交互模块（TIM）

TIM 是确保手势时序同步与交互连贯的核心组件。其工作流程分为两步：

**第一步：交叉注意力投影。** 以当前说话人音频嵌入 $\mathbf{f}_{C_a}$ 作为查询 $Q$，以该说话人的运动嵌入 $\mathbf{f}_{x_a}$ 作为键 $K$ 和值 $V$，进行多头交叉注意力计算：

$$Q = \mathbf{f}_{C_a} \mathbf{W},\quad K = \mathbf{f}_{x_a} \mathbf{W},\quad V = \mathbf{f}_{x_a} \mathbf{W}$$

**第二步：时序交互增强嵌入。** 模型通过时序相关矩阵 $M$ 学习权重 $\sigma = \text{sigmoid}(\text{Enc}(M))$，将说话人自身的语音驱动嵌入 $\mathbf{f}_{x_a, C_a}$ 与混合音频提取的交互嵌入 $\mathbf{f}_{x_a, C_{mix}}$ 进行加权融合：

$$\mathbf{f}_{x_a, C_a} = \sigma \odot \mathbf{f}_{x_a, C_a} + (1 - \sigma) \odot \mathbf{f}_{x_a, C_{mix}}$$

其中混合音频条件 $C_{mix} = \bar{C}_a + C_b$ 携带全局对话交互线索。可学习权重 $\sigma$ 使模型能根据时序上下文动态平衡个体节奏保持与交互依赖建模。消融实验证实，移除 TIM 后 FGD 从 0.769 升至 1.297，BC 和 Diversity 均大幅下降（Table 3），表明该模块对并发手势同步性不可或缺。

### 互注意力机制

在双边去噪器之间引入互注意力层，以对方分支的特征作为多头注意力中的查询 $Q$，实现跨说话人特征交换。该机制使每个分支在去噪过程中能感知对方手势状态，从而增强交互连贯性。移除互注意力后 FGD 升至 0.924（Table 3），证明跨说话人信息交换对生成质量有显著贡献。

### 训练目标

总损失函数由三项组成：

$$\mathcal{L}_{total} = \lambda_{simple} \mathcal{L}_{simple} + \mathcal{L}_{vel} + \mathcal{L}_{foot}$$

其中简单扩散损失 $\mathcal{L}_{simple}$ 分别对说话人 A 和 B 计算去噪输出与真实手势的均方误差：

$$\mathcal{L}_{simple} = \mathbb{E}_{x,t,\epsilon} \left[ \| x_a - \mathcal{D}(x_a^{(t)}, C_a, C_{mix}, t) \|_2^2 + \| x_b - \mathcal{D}(x_b^{(t)}, C_b, C_{mix}, t) \|_2^2 \right]$$

$\mathcal{L}_{vel}$ 为速度损失，约束相邻帧间运动平滑性；$\mathcal{L}_{foot}$ 为脚部接触损失，确保下半身（补全为 T-pose）的物理合理性。消融实验显示，移除 $\mathcal{L}_{foot}$ 后 FGD 升至 1.082、BC 同步下降（Table 5），验证了该损失对姿态物理合理性的贡献。权重 $\lambda_{simple}$ 设为 15。



## 实验与关键发现

### 主实验结果

Co3Gesture 在自建的双人对话数据集 GES-Inter 上与一系列单人生成基线和人-人交互基线进行了全面对比（Table 2）。单人生成基线包括 **TalkSHOW**（Yi et al., CVPR 2023）、**ProbTalk**（Liu et al., CVPR 2024b）、**DiffSHEG**（Chen et al., CVPR 2024）和 **EMAGE**（Liu et al., CVPR 2024a）；文本驱动动作基线与人-人交互基线包括 **MDM**（Tevet et al., ICLR 2023）、**InterX**（Xu et al., CVPR 2024）和 **InterGen**（Liang et al., IJCV 2024b）。所有方法均使用官方代码或预训练模型在 GES-Inter 上重新训练或微调，文本驱动基线则统一采用与 Co3Gesture 相同的音频编码器以确保特征提取的一致性。

![[assets/figures/papers/paper_list_l20_https_openreview_net_pdf_id_VaowElpVzd/figures/005_Table_2.jpg]]
*Table 2: Comparison with the state-of-the-art counterparts on our newly collected GES-Inter dataset. ↑ means the higher the better, and ↓ indicates the lower the better. ± means 95% confidence interval. The dotted line separates whether the methods are adopted from single-person co-speech generation or text2motion counterparts*

Co3Gesture 在核心指标 **FGD（Fréchet Gesture Distance）** 上达到 0.769，较次优方法 InterGen 的 1.012 降低了 24.0%，表明生成手势的分布与真实手势分布更为接近。在节拍一致性 **BC（Beat Consistency）** 上，Co3Gesture 取得 0.692，优于 InterGen 的 0.670；在多样性 **Diversity** 上达到 72.824，同样领先于 InterGen 的 69.455。这些结果验证了双边协作扩散框架在建模双人并发手势交互方面的显著优势。

值得注意的是，单人生成基线（如 EMAGE、DiffSHEG）在 FGD 和 BC 上均表现较差，因为它们缺乏对双人交互动态的建模能力。而人-人交互基线 InterGen 虽能生成双人动作，但其设计面向文本驱动场景，未针对语音驱动的并发手势进行优化，因此在 BC 指标上仍不及 Co3Gesture。这进一步说明，专门为语音驱动的并发交互设计生成架构是必要的。

### 消融实验

为验证各核心组件的贡献，论文进行了系统的消融研究（Table 3、Table 4、Table 5）。

![[assets/figures/papers/paper_list_l20_https_openreview_net_pdf_id_VaowElpVzd/figures/006_Table_3.jpg]]
*Table 3: Ablation study of TIM and mutual attention mechanism on our GES-Inter dataset*

![[assets/figures/papers/paper_list_l20_https_openreview_net_pdf_id_VaowElpVzd/figures/007_Table_4.jpg]]
*Table 4: Ablation study of bilateral branches and audio mixed/ separation on our GES-Inter dataset*

![[assets/figures/papers/paper_list_l20_https_openreview_net_pdf_id_VaowElpVzd/figures/008_Table_5.jpg]]
*Table 5: Ablation study of foot contact loss on our GES-Inter dataset*

**时序交互模块（TIM）的消融**（Table 3）：移除 TIM 后，FGD 从 0.769 急剧上升至 1.297，BC 和 Diversity 也大幅下降。这表明 TIM 通过交叉注意力机制和可学习权重 σ 融合说话人自身语音驱动嵌入与混合音频交互嵌入，对于确保手势的时序同步与交互连贯性至关重要。缺少 TIM 时，两个生成分支各自独立去噪，无法感知对方的运动状态，导致生成的并发手势失去交互关联。

**互注意力机制的消融**（Table 3）：移除互注意力后，FGD 升至 0.924，BC 和 Diversity 同样恶化。互注意力机制以对方分支的特征作为查询 Q 进行多头注意力计算，实现了跨说话人的特征交换。消融结果表明，仅靠 TIM 的交互嵌入融合不足以完全捕获双人之间的动态交互，显式的跨分支特征交换是提升交互质量的关键补充。

**双边分支的消融**（Table 4）：将双边协作分支替换为单一生成分支后，FGD 从 0.769 骤升至 1.669。这一结果直接验证了论文的核心洞察——两人对话时的身体动态呈不对称性，分别条件于不同说话人的音频生成手势，比以单一主模式合成双人姿态更为自然。单分支架构无法有效处理两位说话人各自独立的语音节奏与动作模式。

**音频分离与混合的消融**（Table 4）：移除分离音频、仅使用混合音频驱动生成时，BC 指标显著下降。这说明音频分离对于保持个体节拍一致性至关重要——每位说话人的手势应与自身语音的韵律紧密对齐，而混合音频会模糊这种对应关系。同时，移除混合音频后 FGD 和 BC 也均变差，验证了混合音频提供的全局交互线索对增强双人交互建模具有不可替代的作用。

**脚部接触损失的消融**（Table 5）：去掉脚部接触损失 $\mathcal{L}_{foot}$ 后，FGD 升至 1.082，BC 也出现退化。该损失函数约束下肢关节的物理合理性（尽管模型仅生成上半身手部，下肢保持 T-pose），其消融结果表明，显式施加物理约束有助于提升整体姿态的自然度和运动质量，即使对于非主要生成区域也有正向影响。

### 用户研究

为从主观感知角度评估生成质量，论文邀请了 15 名参与者进行用户研究，从**自然度（Naturalness）**、**流畅度（Smoothness）** 和**交互连贯性（Interaction Coherency）** 三个维度对 Co3Gesture 与各基线方法进行盲评（Table 6）。Co3Gesture 在所有维度上均获得最高评分：自然度 4.4、流畅度 4.5、交互连贯性 4.2（5 分制）。配对 t 检验结果（Table 7）显示，Co3Gesture 在三个维度上均显著优于所有对比方法（p < 0.05）。

![[assets/figures/papers/paper_list_l20_https_openreview_net_pdf_id_VaowElpVzd/figures/012_Table_6.jpg]]
*Table 6: Statistical results in User Study. ± denotes standard deviation*

![[assets/figures/papers/paper_list_l20_https_openreview_net_pdf_id_VaowElpVzd/figures/013_Table_7.jpg]]
*Table 7: Significance Analysis of User Study*

为确保评估的可靠性，用户研究采用了严格的实验设计：所有参与者先观看数据集中的标注示例作为参考标准；评估顺序随机化且匿名；60% 的参与者在两周后重新打分进行交叉验证，未发现显著偏差。交互连贯性维度的高分尤其值得关注，因为它直接衡量了双人手势之间的时序配合与互动自然程度，这正是 Co3Gesture 相较于其他方法的核心优势所在。

### 失败模式与局限性

尽管 Co3Gesture 在定量和定性评估中均表现优异，但仍存在若干值得关注的局限：

1. **生成范围受限**：当前模型仅生成上半身手部（含手指），下肢保持 T-pose 且不包含面部表情和身体形状参数。在需要全身同步驱动的场景中，模型无法提供完整的交互姿态。

2. **数据噪声残留**：GES-Inter 数据集通过 Pymaf-X 从野外视频中伪标签估计得到，虽经过多层过滤和人工修正，但仍可能残留姿态估计误差和时序抖动。这些噪声在训练过程中可能被模型学习，影响生成精度。

3. **个性化缺失**：模型未显式建模说话人的情感、身份等个性化因素，生成手势的风格多样性受限于数据集的分布。对于需要特定风格或情感表达的应用场景，当前框架缺乏可控性。

4. **空间假设固定**：训练和推理时假设两位说话人的相对位置固定，未考虑野外视频中多变的摄像头角度和空间布局。这限制了模型在非标准化拍摄条件下的泛化能力。

5. **评估指标不足**：交互质量的评估仍依赖通用指标（FGD、BC）和主观研究，缺少针对并发手势交互一致性的精细化客观度量，如交互同步率、响应时滞等。

### 补充图表

![[assets/figures/papers/paper_list_l20_https_openreview_net_pdf_id_VaowElpVzd/figures/003_Table_1.jpg]]
*Table 1: Statistical comparison of our GES-Inter with existing datasets. The dotted line separates whether the speech content in the dataset is built based on the conversational corpus*



## 定位与知识库关联

### 1. 方法定位与谱系

Co3Gesture 的核心贡献在于将语音驱动手势生成从单人独白场景首次系统性地拓展至双人并发对话场景。此前的主流方法——包括 **TalkSHOW** (Yi et al., CVPR 2023)、**ProbTalk** (Liu et al., CVPR 2024b)、**DiffSHEG** (Chen et al., CVPR 2024) 和 **EMAGE** (Liu et al., CVPR 2024a)——均以单说话人音频为条件，生成单人的共语音手势，完全不具备建模两人交互动态的能力。另一条相关技术路线是文本驱动的人-人交互动作生成，代表方法包括 **MDM** (Tevet et al., ICLR 2023)、**InterX** (Xu et al., CVPR 2024) 和 **InterGen** (Liang et al., IJCV 2024b)。这些方法虽然能生成双人交互动作，但其条件模态是文本标签或动作描述，而非自然对话语音，因此无法捕捉语音韵律、节奏与交互手势之间的细粒度耦合关系。

Co3Gesture 填补了这一空白。其方法设计的关键差异体现在四个维度：

**生成架构**：此前的双人动作生成方法（如 InterGen）采用单一生成分支，以整体方式一次性输出两人姿态。Co3Gesture 转而采用**双边协作扩散分支**——两个共享权重的 Transformer 去噪器分别以说话人 A 和 B 的分离音频为条件，各自生成对应的手势序列。这一设计源自一个核心观察：对话中两人的身体动态具有天然的不对称性，分别条件于各自的语音信号比分主模式合成更自然。

**时序交互建模**：单分支方法缺乏对两人手势时序关联的显式建模。Co3Gesture 引入**时序交互模块（TIM）**，通过交叉注意力机制将当前说话人的运动嵌入与其自身音频嵌入对齐，再利用从混合对话音频中提取的全局交互线索，通过可学习权重 σ 动态融合“自身语音驱动”与“交互驱动”两部分信息（见 Eq. (2)），从而平衡个体节奏保持与交互依赖。

**跨说话人注意力**：现有方法无跨说话人的特征交换机制。Co3Gesture 在双边去噪器之间引入**互注意力层**，以对方分支的特征作为多头注意力的查询 Q，实现跨说话人的特征交互与共享更新，这是确保交互连贯性的关键设计。

**损失函数**：相比仅使用重建损失的单人基线，Co3Gesture 在简单扩散损失 $L_{simple}$ 之外增加了速度损失 $L_{vel}$ 和脚部接触损失 $L_{foot}$（见 Eq. (4)），分别约束运动平滑性和下肢物理合理性。

### 2. 适用边界与局限

Co3Gesture 的适用边界受以下因素制约：

**生成范围**：当前框架仅生成上半身手势（含手指，共 46 个关节），未包含面部表情和身体形状参数。这限制了其在需要全人同步驱动（如虚拟人完整行为合成）的场景中的应用。

**数据质量依赖**：GES-Inter 数据集通过伪标签方式从野外视频中估计 3D 姿态（使用 Pymaf-X），虽然经过多层自动过滤和人工修正，但仍可能残留姿态估计误差和时序抖动。在极端遮挡或复杂光照条件下，生成质量可能受到影响。

**说话人建模简化**：框架未显式建模说话人的情感状态、身份特征或个性化手势风格。生成手势的风格多样性受限于 GES-Inter 数据集的分布，难以针对特定说话人进行风格定制。

**空间假设固定**：训练和推理均假设两位说话人的相对位置固定。在野外视频中常见的摄像头角度变化、空间布局差异等场景下，模型的泛化能力尚未得到验证。

**交互质量评估不足**：当前评估仍依赖通用指标（FGD、BC）和主观用户研究，缺少专门衡量并发手势交互一致性的精细化客观度量（如交互同步率、响应时滞等）。

### 3. 开放问题

基于上述局限，以下几个方向值得进一步探索：

1. **全人并发交互生成**：如何将面部表情、下半身动作与身体形状参数无缝集成到双边扩散框架中，实现三维全人的并发交互生成？

2. **交互质量精细化度量**：能否提出专门衡量并发手势交互质量的客观指标，例如基于互信息或因果发现的交互同步率、基于时间延迟估计的响应时滞等？

3. **数据质量提升**：如何利用多视角重建、惯性传感器融合等更强健的数据采集技术，减少伪标签数据中的噪声和时序抖动，从根本上提升训练数据的质量？

4. **多人场景泛化**：当前的双边架构能否拓展到三人及以上的群体讨论场景？如何处理更复杂的多人遮挡、空间布局变化和说话人切换问题？

5. **个性化与表现力增强**：可否将文本语义、语音韵律特征、说话人性格特质等额外条件显式注入生成过程，以实现更具表现力和个性化的交互手势合成？



## 原文 PDF

![[paperPDFs/ICLR_2025/CO3GESTURE_TOWARDS_COHERENT_CONCURRENT_CO_SPEECH_3D_GESTURE_GENERATION_WITH_INTER_ACTIVE_DIFFUSION.pdf]]
