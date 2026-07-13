---
title: "Fast-ThinkAct: Efficient Vision-Language-Action Reasoning via Verbalizable Latent Planning"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Fast_ThinkAct_Efficient_Vision_Language_Action_Reasoning_via_Verbalizable_Latent_Planning.pdf
project_link: null
code_link: null
aliases:
- FT
- Fast-ThinkAct
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 将冗长的文本思维链压缩为少量连续隐式向量（如6个），通过偏好引导蒸馏（preference-guided distillation）将教师模型中高质量推理模式传递给学生，同时利用并行空间令牌高效预测视觉轨迹。
primary_logic: 利用教师模型通过GRPO训练产生的奖励信号构造偏好对，学生VLM在连续隐空间中编码推理信息，并通过口头化器（verbalizer LLM）保证其可解释性；同时通过隐空间蒸馏和空间令牌并行预测，将语言推理与视觉规划紧密结合，最终通过KV cache将紧凑的隐式视觉计划注入扩散动作模型，实现高效且高性能的决策。
claims:
- Fast-ThinkAct在SimplerEnv-Google上比ThinkAct-7B快9.3倍，且成功率达到68.7（3B模型）优于ThinkAct-3B的64.7。
- 在RoboTwin2.0双机械臂长程任务上，Fast-ThinkAct相比RDT在Easy和Hard设置上分别提升9.3%和3.6%成功率，平均成功率达65.7/26.4。
- 消融实验表明，移除口头化损失(L_verb)和蒸馏损失(L_distill)会逐步降低性能，完整模型在三个机器人操作基准上平均得分最高。
- 在具身推理基准EgoPlan-Bench2、RoboVQA、OpenEQA上，Fast-ThinkAct-3B以52.8-Overall Avg. 显著超过所有对比方法，包括GPT-4V和Gemini-2.5-Flash。
---

# Fast-ThinkAct: Efficient Vision-Language-Action Reasoning via Verbalizable Latent Planning

> [!tip] 核心洞察
> 利用教师模型通过GRPO训练产生的奖励信号构造偏好对，学生VLM在连续隐空间中编码推理信息，并通过口头化器（verbalizer LLM）保证其可解释性；同时通过隐空间蒸馏和空间令牌并行预测，将语言推理与视觉规划紧密结合，最终通过KV cache将紧凑的隐式视觉计划注入扩散动作模型，实现高效且高性能的决策。

| 字段 | 内容 |
|------|------|
| 中文题名 | Fast-ThinkAct：基于可口头化隐式规划的高效视觉-语言-动作推理 |
| 英文题名 | Fast-ThinkAct: Efficient Vision-Language-Action Reasoning via Verbalizable Latent Planning |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2601.09708) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Fast-ThinkAct |
| Dataset | SimplerEnv-Google, RoboTwin2.0 Hard, LIBERO-Long, EgoPlan-Bench2 |

> [!tip] 效果简介
> - SimplerEnv-Google 上，success rate 68.7 (3B) vs 64.7 (ThinkAct-3B) (+4.0)。
> - RoboTwin2.0 Hard 上，average success rate 26.4 vs 22.8 (RDT) (+3.6)。
> - LIBERO-Long 上，success rate 最高 vs - (优于所有对比方法)。

## 概要

具身智能体在真实环境中执行操作任务时，面临一个根本矛盾：**推理深度与决策速度之间的冲突**。以 **ThinkAct**（Huang et al., arXiv 2025）为代表的推理型视觉-语言-动作（VLA）模型，通过生成约250个tokens的显式文本思维链来提升任务理解与规划能力，但这一过程引入了数秒的推理延迟，难以满足具身任务对1–15 Hz快速决策的实时需求。

**Fast-ThinkAct** 针对上述瓶颈提出了一种新的解决范式：将冗长的文本推理压缩为**少量连续隐式向量**（如6个），同时利用**并行空间令牌**高效预测视觉轨迹。其核心机制是通过偏好引导蒸馏（preference-guided distillation），从教师模型在GRPO训练中产生的奖励信号构造偏好对，将高质量推理模式传递给学生VLM，并通过口头化器（verbalizer LLM）保证隐式表示的可解释性。最终，通过KV cache将紧凑的隐式视觉计划注入扩散动作模型，实现从高层推理到低层动作的高效桥接。

关键实证结果包括：
- 在SimplerEnv-Google基准上，Fast-ThinkAct-3B的成功率达**68.7**，优于ThinkAct-3B的64.7，且推理速度比ThinkAct-7B快**9.3倍**（Figure 1）。
- 在RoboTwin2.0双机械臂长程任务上，Hard设置下平均成功率**26.4**，相比RDT提升3.6个百分点（Table 1）。
- 在EgoPlan-Bench2、RoboVQA、OpenEQA三个具身推理基准上，3B模型以**52.8**的Overall Avg.显著超过GPT-4V和Gemini-2.5-Flash等大规模模型（Table 2）。
- 消融实验证实，口头化损失（L_verb）和蒸馏损失（L_distill）的移除会逐步降低性能，验证了偏好蒸馏与隐空间对齐的必要性（Table 3, Table 7）。

该方法在方法谱系中定位为**高效推理型VLA**，区别于OpenVLA（Kim et al., arXiv 2024）等基础VLA的纯端到端映射、ThinkAct的显式文本CoT、以及CoT-VLA（Zhao et al., CVPR 2025）的视觉目标生成。其知识库贡献在于：首次将GRPO驱动的偏好信号与连续隐空间蒸馏相结合，在保持推理可解释性的同时实现数量级的推理加速。



### 具身推理的实时性困境

视觉-语言-动作（VLA）模型在机器人操作领域取得了显著进展，尤其是引入显式推理链的模型，通过生成文本思维链（Chain-of-Thought, CoT）来理解复杂指令、分析场景并规划动作，在长程任务和复杂操作中展现出更强的泛化能力。然而，这一范式的核心瓶颈在于**推理效率**：典型的推理型VLA（如 **ThinkAct** (Huang et al., arXiv 2025)）在每一步决策时需自回归生成约250个文本tokens，导致单步推理延迟高达数秒。具身任务对控制频率的要求通常在1–15 Hz之间，这种"思考即等待"的模式严重制约了推理型VLA在真实场景中的实用性。

### 现有方法的效率缺口

当前提升VLA推理效率的尝试主要沿两条路径展开：

- **文本侧压缩**：通过提示工程或训练策略缩短显式CoT的长度，但受限于自然语言的冗余性，压缩幅度有限，且过度压缩会损害推理质量。
- **隐式推理**：部分方法完全放弃文本推理，转而使用连续隐向量进行规划（如 **CoT-VLA** (Zhao et al., CVPR 2025) 的视觉目标生成），但此类方法往往牺牲了推理过程的可解释性，难以在安全关键场景中进行审计和调试。

这两种路径之间存在明显的**效率-可解释性权衡**：文本推理可解释但低效，隐式推理高效但不可审计。此外，现有隐式方法通常仅关注语言推理的压缩，未能将视觉规划（如末端执行器轨迹预测）同步纳入紧凑表示，导致语言推理与视觉规划之间存在信息断层。

### 教师模型的潜力与利用不足

以 **ThinkAct** 为代表的推理型VLA通过GRPO（Group Relative Policy Optimization）训练，能够在轨迹奖励的引导下自主探索出高质量的推理模式。这些模式蕴含了丰富的任务理解和空间推理知识，但现有方法仅将其用于直接执行，未将其作为知识蒸馏的来源。若能以紧凑的隐式表示高效继承教师模型的推理能力，同时保留其可口头化验证的特性，则有望在保持高性能的前提下大幅降低推理延迟。

### 本文的核心动机

基于上述分析，本文的核心动机可概括为三个层面：

1. **打破效率瓶颈**：将冗长的文本推理链压缩为极少量（如6个）连续隐式向量，从根本上降低自回归生成的token数量，实现数量级的推理加速。
2. **保留可解释性**：在隐式推理的基础上引入口头化器（Verbalizer），将紧凑的隐式表示解码为自然语言，确保推理过程可被人类理解和审计。
3. **统一语言推理与视觉规划**：将视觉轨迹预测从自回归文本生成（60–70 tokens）转变为并行空间令牌预测，并与隐式语言推理在统一框架内协同训练，实现高效且高保真的视觉-语言-动作推理。

这一动机直接催生了 **Fast-ThinkAct** 框架：通过偏好引导蒸馏（Preference-guided Distillation）将教师模型的高质量推理模式传递给学生模型的紧凑隐式表示，并利用空间令牌并行预测视觉轨迹，最终通过KV cache将隐式视觉计划注入扩散动作模型，实现快速、可解释且高性能的具身决策。



## 核心方法与创新机理

Fast-ThinkAct 的核心创新在于将推理型 VLA 中冗长的显式文本思维链（约 250 tokens）压缩为**少量连续隐式向量**（默认 M=6），并通过**偏好引导蒸馏**（preference-guided distillation）将教师模型的高质量推理模式传递给学生，同时引入**并行空间令牌**高效预测视觉轨迹，最终将紧凑的隐式视觉计划注入扩散动作模型，实现推理效率与任务性能的双重突破。

### 创新一：从文本思维链到可口头化隐式推理

传统推理型 VLA（如 **ThinkAct**（Huang et al., arXiv 2025））依赖自回归生成长篇文本思维链，导致数秒级的推理延迟，无法满足具身任务 1–15 Hz 的实时决策需求。Fast-ThinkAct 将推理表示从**长篇显式文本思维链（~250 tokens）**重构为**少量连续隐式向量 + 空间令牌并行预测轨迹**，推理 token 数压缩近 40 倍。

这一压缩并非简单的维度削减，而是通过“教师 GRPO → 偏好对选择 → 学生隐空间蒸馏”的三阶段训练范式实现的。教师 VLM $\mathcal{F}_{\theta}^{T}$ 首先通过 GRPO 从轨迹奖励中学习生成显式思维链，其训练目标为：

$$\mathcal{I}_{\mathrm{GRPO}}(\theta) = \mathbb{E}_{\tau \sim \mathcal{F}_{\theta}^{T}} \left[ \min \left( r_{\theta}(\tau) A(\tau), \mathrm{clip}( r_{\theta}(\tau), 1-\epsilon, 1+\epsilon) A(\tau) \right) \right]$$

其中优势函数 $A(\tau)$ 通过组内标准化衡量每条推理轨迹的质量：

$$A(\tau) = \frac{R_{\tau} - \mathrm{mean}(\{R_i\}_{i \in G(\tau)})}{\mathrm{std}(\{R_i\}_{i \in G(\tau)})}$$

从每个 rollout 群组中选取最高和最低优势的轨迹构成偏好对：

$$\tau^{+} = \arg\max_{\tau \in G} A(\tau), \quad \tau^{-} = \arg\min_{\tau \in G} A(\tau)$$

学生 VLM $\mathcal{F}_{\theta}$ 将教师推理压缩为 $M$ 个连续隐式向量 $\mathbf{z} = \{z_m\}_{m=1}^{M}$，同时引入**口头化器**（verbalizer LLM）$\nu_{\psi}$ 通过 DPO 式损失将隐式表示解码为自然语言，保证其可解释性：

$$\mathcal{L}_{\mathrm{verb}} = -\mathbb{E} \left[ \log \sigma \left( \beta \left( \log \frac{p_{\psi}(\tau^{+} | \mathbf{z})}{p_{\mathrm{ref}}(\tau^{+})} - \log \frac{p_{\psi}(\tau^{-} | \mathbf{z})}{p_{\mathrm{ref}}(\tau^{-})} \right) \right) \right]$$

这一设计的因果逻辑链为：**教师 GRPO 探索高质量推理 → 偏好信号引导学生隐空间编码 → 口头化器保证隐式表示可解释**，三者构成闭环，使学生在不生成显式文本的情况下继承教师的推理能力。

### 创新二：并行空间令牌替代自回归视觉轨迹预测

传统方法（如 ThinkAct）通过自回归生成文本坐标序列（60–70 tokens）来预测视觉路径点，推理开销高。Fast-ThinkAct 引入 $K$ 个可学习空间令牌，**并行预测** Waypoints，通过 MLP 直接输出，将视觉规划从顺序生成转变为单步前向计算。

学生总损失将语言推理蒸馏与视觉规划统一：

$$\mathcal{L}_{\mathrm{student}} = \mathcal{L}_{\mathrm{verb}} + \mathcal{L}_{\mathrm{distill}} + \mathcal{L}_{\mathrm{ans}}, \quad \mathcal{L}_{\mathrm{ans}} = \sum_{i=1}^{K} \| p_i - \hat{p}_i \|_2^{2}$$

其中 $\mathcal{L}_{\mathrm{distill}} = \| h_{t}^{T} - h_{t} \|_{2}^{2}$ 对齐教师和学生 VLM 的轨迹级隐状态，传递空间推理能力。

### 创新三：隐式视觉计划桥接高层规划与低层动作

传统方法将文本规划直接馈入动作模型，或完全跳过规划。Fast-ThinkAct 从空间令牌的 KV cache 中提取隐式视觉计划 $c_t$，通过**交叉注意力**条件化扩散动作模型 $\pi_{\phi}$：

$$\mathcal{L}_{\mathrm{IL}}(\phi) = \ell \left( \pi_{\phi}(o_t, l, c_t), \hat{a}_t \right)$$

消融实验（Table 7, Appendix B.3）表明，早期层 KV cache 条件化（LIBERO 89.7）优于晚期层 KV（88.3）和输出隐状态（87.1），验证了早期层特征更利于动作预测。这一发现揭示了隐式视觉计划的有效性并非来自深层语义，而是来自与动作执行更紧密耦合的中间表示。

### 创新四：偏好引导蒸馏替代监督微调

与传统的 CoT-SFT 或纯 GRPO 文本生成不同，Fast-ThinkAct 的蒸馏阶段利用教师 GRPO 产生的**奖励信号构造偏好对**，学生通过 $\mathcal{L}_{\mathrm{verb}}$ 和 $\mathcal{L}_{\mathrm{distill}}$ 在隐空间中对齐高质量推理模式。消融实验（Table 3 & Table 7）提供了决定性证据：移除 $\mathcal{L}_{\mathrm{verb}}$ 导致性能明显下降，进一步移除 $\mathcal{L}_{\mathrm{distill}}$ 后性能继续退化；仅使用 SFT 或 CoT-SFT（无教师-学生训练）在 LIBERO/SimplerEnv 上得分明显低于完整模型。

### 创新边界与局限

需要指出，偏好蒸馏的质量高度依赖于教师模型 GRPO 训练的稳定性和探索能力——当教师未能生成多样化高质量推理时，学生可能收敛到次优解。此外，口头化器偶尔会产生幻觉或不忠实于隐式表示的文本，当前框架尚未显式引入防幻觉机制。隐式推理的紧凑性虽然带来了效率，但牺牲了完全的透明度，在安全关键应用中可能不如可审核的文本链。这些局限为后续研究指明了方向：引入 grounding-aware 或幻觉抑制目标、动态调整隐式令牌数量以适应不同复杂度场景。



Fast-ThinkAct 的整体 pipeline 围绕一个核心矛盾展开：**推理型 VLA 的显式文本思维链（约250 tokens）提供了丰富的规划能力，但其自回归生成带来了数秒的推理延迟，使系统难以满足具身任务 1–15 Hz 的实时决策需求**。框架的设计目标是在保留推理质量的前提下，将推理过程从冗长的文本空间压缩到紧凑的连续隐空间，并通过可口头化约束保证其可解释性。

### 核心模块与数据流

系统由四个核心模块构成，形成“教师探索 → 学生压缩 → 口头化对齐 → 动作执行”的级联流水线：

1. **文本教师 VLM（Textual Teacher VLM）** $\mathcal{F}_{\theta}^{T}$：基于 GRPO（Group Relative Policy Optimization）训练，从轨迹执行奖励中学习生成显式文本思维链。教师不直接参与推理部署，其唯一作用是提供偏好信号——在每个 rollout 群组内，按标准化优势函数 $A(\tau)$ 选出最优和最劣推理轨迹，构造偏好对 $(\tau^+, \tau^-)$。

2. **隐式学生 VLM（Latent Student VLM）** $\mathcal{F}_{\theta}$：将教师的冗长推理压缩为 $M$ 个连续隐式向量 $\mathbf{z} = \{z_m\}_{m=1}^M$（典型值 $M=6$），同时通过 $K$ 个可学习空间令牌并行预测视觉路径点。学生模型是实际推理部署的载体，其输出包含两个关键信息流：
   - **隐式推理向量** $\mathbf{z}$：编码了语言推理的语义信息，通过口头化器解码为文本以供验证；
   - **空间令牌 KV cache**：编码了视觉轨迹规划的结构信息，作为隐式视觉计划 $c_t$ 注入下游动作模型。

3. **口头化器 LLM（Verbalizer LLM）** $\nu_{\psi}$：将隐式推理 $\mathbf{z}$ 解码为自然语言。其训练采用 DPO 式偏好损失 $\mathcal{L}_{\mathrm{verb}}$，鼓励对高质量推理轨迹 $\tau^+$ 赋予更高似然，从而保证隐式表示的可解释性——即“隐式空间中的推理可以被口头化为有意义的文本”。

4. **动作模型（Action Model）** $\pi_{\phi}$：基于扩散 Transformer 的低层动作生成器（DiT-Policy 或 RDT）。其关键创新在于通过交叉注意力接收隐式视觉计划 $c_t$——具体实现为：提取学生 VLM 早期层中空间令牌的 KV cache，与动作模型自身状态编码器的 KV 对拼接，使扩散去噪过程能够条件化于高层视觉规划。

### 输入输出流

在推理时，给定观测 $o_t$ 和语言指令 $l$，数据流如下：

1. 学生 VLM $\mathcal{F}_{\theta}$ 接收 $o_t$ 和 $l$，自回归生成 $M$ 个隐式推理向量 $\mathbf{z}$，同时空间令牌并行预测 $K$ 个路径点 $\{\hat{p}_i\}_{i=1}^K$。
2. 口头化器 $\nu_{\psi}$（可选调用）将 $\mathbf{z}$ 解码为文本推理链，用于人工审核或调试。
3. 从空间令牌的早期层 KV cache 中提取隐式视觉计划 $c_t$。
4. 动作模型 $\pi_{\phi}$ 以 $o_t$、$l$ 和 $c_t$ 为条件，通过扩散去噪生成机器人关节动作 $\hat{a}_t$。

### 训练流水线

训练分为两个阶段，如图 Figure 2 所示：

- **阶段一（推理蒸馏）**：教师 VLM 通过 GRPO 从轨迹奖励中学习，产生偏好对；学生 VLM 和口头化器联合训练，总损失为 $\mathcal{L}_{\mathrm{student}} = \mathcal{L}_{\mathrm{verb}} + \mathcal{L}_{\mathrm{distill}} + \mathcal{L}_{\mathrm{ans}}$，其中 $\mathcal{L}_{\mathrm{distill}}$ 对齐教师与学生的轨迹级隐状态（L2 距离），$\mathcal{L}_{\mathrm{ans}}$ 回归空间令牌预测的路径点与真实路径点之间的 L2 误差。
- **阶段二（策略学习）**：冻结学生 VLM 和状态编码器，仅训练动作模型 $\pi_{\phi}$，使用模仿学习损失 $\mathcal{L}_{\mathrm{IL}}$ 拟合真实动作。

### 关键设计决策

- **早期层 KV cache 条件化**：消融实验表明，使用早期层（而非晚期层或输出隐状态）的空间令牌 KV cache 条件化动作模型，能取得最优性能（LIBERO 上 89.7 vs. 88.3/87.1），揭示早期层特征包含更丰富的空间结构信息，更利于动作预测。
- **隐式推理步数** $K=6$：过多或过少的隐式推理步数均导致性能下降，6 步在效率与表达能力之间取得平衡。
- **并行空间令牌预测**：相比教师模型自回归生成文本坐标序列（60–70 tokens），学生通过 $K$ 个空间令牌并行输出路径点，消除了视觉规划部分的序列依赖。

### 补充图表

![[assets/figures/papers/paper_list_l2154_https_arxiv_org_abs_2601_09708/figures/001_Figure_1.jpg]]
*Figure 1: Overview of Fast-ThinkAct. Previous reasoning VLAs generate lengthy reasoning traces (∼250 tokens). Our approach learns compact continuous tokens (e.g., 6) (blue) and parallel spatial tokens (green) as internal reasoning. The bottom-right plot shows that we achieve 9.3× faster inference than ThinkAct-7B Huang et al. (2025), while delivering improved performance on the SimplerEnv-Google benchmark*



Fast-ThinkAct 的核心架构由四个关键模块构成，围绕“将冗长文本思维链压缩为可口头化隐式向量”这一中心目标协同工作。

### 1. 文本教师 VLM（Textual Teacher VLM $\mathcal{F}_{\theta}^{T}$）

教师模型承担探索高质量推理模式的任务。给定观测 $o_t$ 和语言指令 $l$，教师 VLM 自回归地生成显式文本思维链 $\tau$。其训练目标为组相对策略优化（GRPO）：

$$
\mathcal{I}_{\mathrm{GRPO}}(\theta) = \mathbb{E}_{\tau \sim \mathcal{F}_{\theta}^{T}} \left[ \min \left( r_{\theta}(\tau) A(\tau), \mathrm{clip}( r_{\theta}(\tau), 1-\epsilon, 1+\epsilon) A(\tau) \right) \right]
$$

其中 $r_{\theta}(\tau)$ 为轨迹概率比，优势函数 $A(\tau)$ 通过组内标准化定义：

$$
A(\tau) = \frac{R_{\tau} - \mathrm{mean}(\{R_i\}_{i \in G(\tau)})}{\mathrm{std}(\{R_i\}_{i \in G(\tau)})}
$$

$R_{\tau}$ 为轨迹 $\tau$ 对应的任务奖励（如操作成功率），$G(\tau)$ 为同一观测下的 rollout 群组。教师 GRPO 的核心作用不是直接部署推理，而是产生高质量的偏好信号：从每个群组中选取最高和最低优势的轨迹作为正负偏好对：

$$
\tau^{+} = \arg\max_{\tau \in G} A(\tau), \quad \tau^{-} = \arg\min_{\tau \in G} A(\tau)
$$

### 2. 隐式学生 VLM（Latent Student VLM $\mathcal{F}_{\theta}$）

学生 VLM 将教师的长篇推理压缩为 $M$ 个连续隐式向量 $\mathbf{z} = \{z_m\}_{m=1}^{M}$（典型值 $M=6$），以极低的 token 开销编码推理信息。同时，学生 VLM 利用 $K$ 个可学习的空间令牌（spatial tokens）并行预测视觉路径点 $\hat{p}_i$，替代教师自回归生成文本坐标序列（60–70 tokens）的低效方式。

学生总损失由三项组成：

$$
\mathcal{L}_{\mathrm{student}} = \mathcal{L}_{\mathrm{verb}} + \mathcal{L}_{\mathrm{distill}} + \mathcal{L}_{\mathrm{ans}}, \quad \mathcal{L}_{\mathrm{ans}} = \sum_{i=1}^{K} \| p_i - \hat{p}_i \|_2^{2}
$$

- $\mathcal{L}_{\mathrm{ans}}$：空间令牌预测路径点与真值 $p_i$ 的 L2 回归损失，确保视觉轨迹规划能力。
- $\mathcal{L}_{\mathrm{distill}}$：视觉规划蒸馏损失（见下文）。
- $\mathcal{L}_{\mathrm{verb}}$：口头化偏好损失（见下文）。

### 3. 口头化器 LLM（Verbalizer LLM $\nu_{\psi}$）

口头化器将学生 VLM 的隐式推理 $\mathbf{z}$ 解码为自然语言，其训练采用 DPO 式偏好损失，鼓励将隐式表示解码为高质量推理文本：

$$
\mathcal{L}_{\mathrm{verb}} = -\mathbb{E} \left[ \log \sigma \left( \beta \left( \log \frac{p_{\psi}(\tau^{+} | \mathbf{z})}{p_{\mathrm{ref}}(\tau^{+})} - \log \frac{p_{\psi}(\tau^{-} | \mathbf{z})}{p_{\mathrm{ref}}(\tau^{-})} \right) \right) \right]
$$

其中 $\sigma$ 为 sigmoid 函数，$\beta$ 为温度系数，$p_{\mathrm{ref}}$ 为参考模型。口头化器仅在训练时使用，其损失反向传播至学生 VLM，迫使隐式向量 $\mathbf{z}$ 保持可解释性——这是“verbalizable”的关键保证。推理时口头化器不参与前向计算，因此不引入额外延迟。

### 4. 视觉规划蒸馏与动作模型桥接

教师 VLM 在生成文本思维链的同时也隐式编码了空间推理能力。为将此能力传递给学生，引入视觉规划蒸馏损失：

$$
\mathcal{L}_{\mathrm{distill}} = \| h_{t}^{T} - h_{t} \|_{2}^{2}
$$

其中 $h_{t}^{T}$ 和 $h_{t}$ 分别为教师和学生 VLM 在轨迹级的隐状态表示，通过 L2 距离对齐，确保学生继承教师的空间推理能力。

在动作执行阶段，从学生 VLM 空间令牌的 KV cache 中提取隐式视觉计划 $c_t$（实验表明早期层 KV cache 效果最优，LIBERO 上达 89.7，优于晚期层 KV 的 88.3 和输出隐状态的 87.1）。动作模型 $\pi_{\phi}$（基于扩散 Transformer 的 DiT-Policy 或 RDT）通过交叉注意力接收 $c_t$，结合观测 $o_t$ 和语言指令 $l$ 预测动作：

$$
\mathcal{L}_{\mathrm{IL}}(\phi) = \ell \left( \pi_{\phi}(o_t, l, c_t), \hat{a}_t \right)
$$

其中 $\ell$ 为扩散去噪损失，$\hat{a}_t$ 为真值动作。此设计将高层隐式规划与低层动作生成解耦，学生 VLM 在动作训练阶段冻结，仅微调动作模型。

### 5. 关键设计的选择依据

消融实验（Table 3 及 Table 7）揭示了各模块的必要性：移除 $\mathcal{L}_{\mathrm{verb}}$ 导致性能明显下降，进一步移除 $\mathcal{L}_{\mathrm{distill}}$ 后性能继续退化，验证了偏好蒸馏和隐空间对齐的双重价值。隐式推理步数 $K=6$ 取得最优性能（Table 8），过多或过少步数均导致性能下降，表明 6 个隐式向量在压缩效率与信息保真度之间达到最佳平衡。

### 补充图表

![[assets/figures/papers/paper_list_l2154_https_arxiv_org_abs_2601_09708/figures/002_Figure_2.jpg]]
*Figure 2: Overview of Fast-ThinkAct. (a) Given observation*



## 实验与关键发现

### 核心定量结果：操作能力与推理效率

Fast-ThinkAct 在机器人操作和具身推理两大维度上均展现出显著优势，其核心突破在于**同时实现了更高的任务成功率和大幅降低的推理延迟**。

在机器人操作方面，**Table 1** 展示了 RoboTwin2.0 双机械臂长程任务上的表现。Fast-ThinkAct 在 Easy 和 Hard 设置上相比扩散策略基线 **RDT** (Liu et al., arXiv 2024) 分别提升 **9.3%** 和 **3.6%** 成功率，平均成功率达 **65.7** / **26.4**，尤其在长时序任务（270–470步）中优势更为明显。在 SimplerEnv-Google 基准上，**Table 5** 显示 Fast-ThinkAct-3B 成功率达 **68.7**，优于 ThinkAct-3B 的 64.7，且推理速度提升 **9.3 倍**（Figure 1 底部图表）。在 LIBERO-Long 上，Figure 3(d) 表明 Fast-ThinkAct 同样取得最高成功率，验证了隐式规划对长程任务的有效支撑。

![[assets/figures/papers/paper_list_l2154_https_arxiv_org_abs_2601_09708/figures/003_Figure_3.jpg]]
*Figure 3: Evaluation of robot manipulation and reasoning efficiency. (a)-(e) Success rates on LIBERO Liu et al. (2023) and SimplerEnv Li et al. (2024) benchmarks compared with state-of-the-art 7B reasoning VLAs. (f) Latency comparison across 3B and 7B reasoning VLAs. Our approach achieves up to 89.3% inference latency reduction while maintaining superior task success rates*

![[assets/figures/papers/paper_list_l2154_https_arxiv_org_abs_2601_09708/figures/004_Table_1.jpg]]
*Table 1: Quantitative evaluation on RoboTwin2.0 Chen et al. (2025). E and H denote easy and hard settings (without/with domain randomization). Background colors indicate task length based on expert demonstrations: short (80-100) , medium (110-220) , long (270-470) steps*

![[assets/figures/papers/paper_list_l2154_https_arxiv_org_abs_2601_09708/figures/012_Table_5.jpg]]
*Table 5: Results on LIBERO and SimplerEnv benchmarks with additional ThinkAct-3B comparison*

在具身推理方面，**Table 2** 汇总了 EgoPlan-Bench2、RoboVQA 和 OpenEQA 三个基准的结果。Fast-ThinkAct-3B 以 **52.8** 的 Overall Avg. 显著超过所有对比方法，包括 GPT-4V 和 Gemini-2.5-Flash。其中 RoboVQA 的 BLEU-Avg. 达到 **60.8**，较 ThinkAct-3B 提升 **+5.5**；EgoPlan-Bench2 准确率 **46.4**，提升 **+2.4**。值得注意的是，**Table 4** 显示将模型扩展至 7B/8B 后，在具身推理基准上仍保持竞争力，但与专用大模型（如 GPT-4V）的差距缩小，提示 3B 规模的性价比优势更为突出。

![[assets/figures/papers/paper_list_l2154_https_arxiv_org_abs_2601_09708/figures/005_Table_2.jpg]]
*Table 2: Quantitative evaluation on EgoPlan-Bench2 Qiu et al. (2024), RoboVQA Sermanet et al. (2024), and OpenEQA Majumdar et al. (2024) benchmarks for embodied reasoning*

推理延迟方面，**Figure 3(f)** 给出了系统对比：Fast-ThinkAct 相比 ThinkAct-7B 和 MolmoAct-7B 分别实现 **89.3%** 和 **88.0%** 的延迟降低，相比 ThinkAct-3B 加速约 **7 倍**。这一效率提升源于将约 250 个文本 tokens 的思维链压缩为仅 6 个连续隐式向量（M=6），从根本上削减了自回归解码的计算开销。

### 消融研究：训练目标与架构选择

**Table 3** 和 **Table 7** 系统拆解了各训练组件的贡献。完整模型在 LIBERO 和 SimplerEnv 上平均得分最高。移除口头化损失 $\mathcal{L}_{\mathrm{verb}}$ 后性能出现明显下降，进一步移除蒸馏损失 $\mathcal{L}_{\mathrm{distill}}$ 后性能继续退化——这验证了**偏好引导蒸馏**和**隐空间对齐**对传递高质量推理模式的必要性。仅使用 SFT 或 CoT-SFT（无教师-学生蒸馏阶段）的变体在 Libero/SimplerEnv 上得分显著低于完整模型，表明 GRPO 教师提供的偏好信号是压缩推理质量的关键保障。

在架构层面，**Table 8** 对隐式推理步数 $K$ 进行了消融：$K=6$ 取得最佳性能，过多或过少步数均导致下降——步数过少时推理信息不足，过多则可能引入噪声或过拟合。此外，Appendix B.3 报告了 KV cache 条件化层位的选择：**早期层 KV cache** 条件化在 LIBERO 上取得 89.7 的成功率，优于晚期层 KV（88.3）和输出隐状态（87.1），揭示早期层特征包含更丰富的空间-语义信息，更利于动作预测。

![[assets/figures/papers/paper_list_l2154_https_arxiv_org_abs_2601_09708/figures/017_Table_8.jpg]]
*Table 8: Ablation of Latent Reasoning Steps ??*

### 与高效文本推理方法的公平对比

**Table 6** 将 Fast-ThinkAct 与使用相同数量推理 tokens（0 或 6）的高效文本推理方法进行了公平对比。结果显示，在 token 预算严格匹配的条件下，隐式推理仍优于文本推理变体，排除了 token 数量差异带来的偏差，证明**连续隐空间表示本身**具备比离散文本更高的信息密度和规划质量。

### 失败恢复与小样本自适应

**Figure 5** 展示了 Fast-ThinkAct 在 RoboFAC 上的失败恢复能力。在仿真和真实机器人场景中，模型不仅能识别失败类型和执行阶段（Figure 9），还能生成纠正性引导动作。定量评估显示其恢复成功率显著优于无推理能力的基线策略，表明隐式规划在异常检测与在线纠偏中具有实用价值。

**Figure 6** 展示了 RoboTwin2.0 上的小样本自适应结果：每任务仅使用 10 条演示进行微调后，Fast-ThinkAct 在多个任务上取得明显提升，尤其在 Hard 设置下对新视觉扰动的泛化能力优于从头训练的 RDT，验证了预训练隐式推理先验对数据高效迁移的支撑作用。

### 可视化分析：轨迹预测与推理痕迹

**Figure 4** 可视化了 SimplerEnv-Google、LIBERO-Long 和 RoboTwin2.0-Hard 上的预测视觉轨迹与动作执行结果。黄色轨迹表示单臂/左夹爪路径，红色表示右夹爪路径。在长达 278 步的双臂协调任务中，预测轨迹与专家演示高度吻合，验证了空间令牌并行预测的准确性。

**Figure 7** 和 **Figure 10** 分别对比了 RoboVQA 和 OpenEQA 上教师文本推理与学生口头化隐式推理的痕迹。绿色标注相关内容，橙色/红色标注不相关或错误内容。学生的口头化输出（经 $\nu_\psi$ 解码）保留了教师推理的核心逻辑链条，同时过滤了冗余描述，从侧面印证了 $\mathcal{L}_{\mathrm{verb}}$ 在偏好蒸馏中起到了“压缩-精炼”的双重作用。

### 失败模式与局限性

尽管整体表现优异，分析揭示了以下值得关注的失败模式：

1. **教师质量依赖**：偏好蒸馏的质量高度依赖于教师模型 GRPO 训练的稳定性和探索能力。当教师未能生成多样化高质量推理时，学生可能收敛到次优解——这一问题在奖励稀疏的长程任务中尤为突出。

2. **口头化器幻觉**：$\nu_\psi$ 偶尔会产生不忠实于隐式表示 $\mathbf{z}$ 的文本（Figure 10 红色标注示例），虽然提供了可解释性，但缺乏显式防幻觉机制，在安全关键应用中需谨慎使用。

3. **真实世界泛化**：当前验证主要基于仿真器（LIBERO、SimplerEnv、RoboTwin2.0）和有限真实机器人数据（仅 RoboFAC 部分场景），大规模真实世界部署中的泛化性有待进一步验证。

4. **透明度折衷**：隐式推理的紧凑性虽然带来了效率，但牺牲了完全的透明度——6 个连续向量无法像文本链那样逐句审核，这在需要可追溯决策的领域可能构成合规障碍。

5. **单步推理限制**：当前框架仅考虑单步推理与动作预测，未处理需要多轮对话或在线动态上下文更新的任务，限制了其在交互式场景中的适用性。

### 补充图表

![[assets/figures/papers/paper_list_l2154_https_arxiv_org_abs_2601_09708/figures/010_Table_3.jpg]]
*Table 3: Ablation study of training objectives and learning stages. Note that Fast-ThinkAct w/o*

![[assets/figures/papers/paper_list_l2154_https_arxiv_org_abs_2601_09708/figures/013_Table_6.jpg]]
*Table 6: Comparison with efficient textual reasoning methods*

![[assets/figures/papers/paper_list_l2154_https_arxiv_org_abs_2601_09708/figures/018_Table_7.jpg]]
*Table 7: Additional ablation study of training objectives and learning stages on robot manipulation benchmarks*

![[assets/figures/papers/paper_list_l2154_https_arxiv_org_abs_2601_09708/figures/006_Figure_4.jpg]]
*Figure 4: Visualization of predicted visual trajectories and action execution results on long-horizon tasks. Examples from (a) SimplerEnv-Google, (b) LIBERO-Long, and (c) RoboTwin2.0-Hard with long (278) steps. Yellow traces indicate single-arm/left gripper trajectories; red traces indicate right gripper trajectories for bimanual tasks*

![[assets/figures/papers/paper_list_l2154_https_arxiv_org_abs_2601_09708/figures/009_Figure_7.jpg]]
*Figure 7: Reasoning trace comparison on RoboVQA. (a) Teacher’s textual reasoning. (b) Student’s verbalized latent reasoning. Green: relevant content; orange: less relevant content*



## 定位与知识库关联

### 1. 方法谱系：从文本思维链到隐式推理的演进

Fast-ThinkAct 处于具身视觉-语言-动作模型从“慢思考”向“快思考”演进的关键节点。其方法谱系可沿三条主线追溯：

**主线一：基础VLA → 推理型VLA。** 早期通用VLA如 **OpenVLA**（Kim et al., arXiv 2024）直接建立视觉-语言-动作的端到端映射，缺乏显式推理能力。后续工作引入思维链机制：**ThinkAct**（Huang et al., arXiv 2025）通过GRPO训练文本教师模型生成显式推理链；**CoT-VLA**（Zhao et al., CVPR 2025）进一步生成视觉子目标作为规划中间表示；**MolmoAct**（Lee et al., arXiv 2025）利用空间表征增强推理的几何精度。Fast-ThinkAct 继承了ThinkAct的教师-学生蒸馏框架和GRPO偏好信号，但将推理形式从约250个token的文本链压缩为仅6个连续隐式向量，从根本上改变了推理效率的上界。

**主线二：扩散策略 → 规划引导的动作生成。** 低层动作模型从纯反应式向规划引导式演进：**DP（Diffusion Policy）**（Chi et al., IJRR 2023）和 **ACT**（Zhao et al., arXiv 2023）仅基于观测和语言指令生成动作；**RDT**（Liu et al., arXiv 2024）将扩散Transformer扩展至双机械臂长程任务；**π0**（Black et al., arXiv 2024）引入流匹配。Fast-ThinkAct 在RDT基础上引入隐式视觉计划$c_t$，通过交叉注意力将高层空间推理注入扩散去噪过程，形成“先规划后执行”的层级结构。

**主线三：语言模型推理 → 隐空间推理。** 大语言模型的推理能力已从显式文本链扩展至隐空间：相关工作探索了连续向量替代离散token的可能性。Fast-ThinkAct 的关键创新在于将隐式推理与视觉规划统一在同一VLM中——M个隐式推理token编码语言推理，K个空间token并行预测视觉轨迹——并通过口头化器（verbalizer LLM）保证隐式表示的可解释性，避免了完全黑箱推理的不可审核风险。

### 2. 知识库定位：核心增量与适用边界

**核心增量贡献：**

1. **推理效率的结构性突破。** 将VLA推理延迟降低89.3%（相对ThinkAct-7B），同时保持或提升成功率——这在现有推理型VLA中尚无先例。关键机制是隐式向量替代文本自回归，将推理的序列依赖从O(N)压缩为O(M)，M≪N。

2. **偏好引导的隐空间对齐。** 不同于传统知识蒸馏仅对齐输出分布，Fast-ThinkAct 利用GRPO产生的组内标准化优势函数$A(\tau)$构造偏好对，通过DPO式口头化损失$\mathcal{L}_{\mathrm{verb}}$和L2蒸馏损失$\mathcal{L}_{\mathrm{distill}}$双通道传递教师推理质量。这比直接SFT或CoT-SFT更有效地筛选高质量推理模式（消融实验证实移除$\mathcal{L}_{\mathrm{verb}}$和$\mathcal{L}_{\mathrm{distill}}$后性能逐步退化）。

3. **隐式视觉计划到动作的条件化桥接。** 提取空间token的KV cache作为隐式视觉计划$c_t$，通过交叉注意力条件化扩散动作模型——这一设计使高层空间推理直接参与低层动作生成，而非仅作为文本提示。消融表明早期层KV cache（89.7 LIBERO）优于晚期层（88.3）和输出隐状态（87.1），揭示了早期视觉特征对动作预测的特殊价值。

**适用边界：**

- **任务类型：** 当前验证覆盖单臂/双机械臂操作（LIBERO、SimplerEnv、RoboTwin2.0）和具身推理问答（EgoPlan-Bench2、RoboVQA、OpenEQA），但均为单步推理与动作预测场景。未涉及需要多轮对话、在线动态上下文更新或长程任务分解的复杂交互。
- **输入模态：** 仅使用视觉和语言输入，未扩展到力触觉、声音等多模态信号。
- **部署环境：** 主要验证在仿真器上完成，真实机器人验证仅限RoboFAC的部分场景，大规模真实世界泛化性待确认。
- **模型规模：** 3B和7B骨干均验证有效，但隐式推理的压缩效率是否随模型规模进一步扩大而保持优势，尚缺乏证据。

### 3. 局限与开放问题

**已识别的局限：**

1. **教师依赖瓶颈。** 偏好蒸馏的质量高度依赖于教师模型GRPO训练的稳定性和探索能力。当教师未能生成多样化高质量推理时（例如任务奖励稀疏或难以定义），学生可能收敛到次优解。这一依赖关系使方法在缺少显式轨迹奖励的开放域任务中面临根本性挑战。

2. **口头化器的忠实度问题。** 口头化器偶尔会产生幻觉或不忠实于隐式表示的文本（Figure 7和Figure 10中标注了不相关内容）。虽然提供了可解释性接口，但尚未引入grounding-aware或防幻觉机制，在安全关键应用中可能产生误导性解释。

3. **透明度与效率的权衡。** 隐式推理的紧凑性牺牲了完全的可审核性——虽然口头化器提供文本输出，但隐式向量本身不可直接检查，在需要严格审计的场景中不如显式文本链可靠。

4. **验证覆盖不足。** 真实机器人实验仅限RoboFAC的失败恢复场景，缺少大规模、多场景真实世界部署的统计证据。小样本自适应实验（Figure 6）使用每任务10个演示，但泛化到全新任务的能力未充分评估。

**开放问题：**

1. **幻觉抑制与忠实度提升。** 如何引入grounding-aware损失或对比学习目标，使口头化器的输出更忠实地反映隐式表示的内容？是否可以通过视觉grounding信号（如空间token的注意力图）约束口头化过程？

2. **多模态隐式推理的扩展。** 能否将隐式推理框架扩展到力触觉、声音等多模态输入，同时保持压缩效率？多模态信号的隐空间对齐可能面临额外的模态差距挑战。

3. **无奖励场景的偏好构造。** 在缺少显式轨迹奖励的任务（如开放域物体重排、社交导航）中，如何构造有效的偏好对进行隐式蒸馏？可能的替代方案包括人类偏好标注、基于基础模型的自动评估、或自监督的规划质量度量。

4. **自适应推理深度。** 能否动态调整隐式token数量以适应不同复杂度的场景？消融显示K=6为当前最优，但固定步数可能在简单任务上浪费计算、在极复杂任务上推理不足。自适应机制可进一步优化推理开销。

5. **向更高安全要求的领域推广。** 如何将这一框架推广至自动驾驶或移动机器人等对延迟更敏感且安全要求更高的领域？这些领域对可解释性和故障可追溯性的要求可能超出当前口头化器能提供的保证。



## 原文 PDF

![[paperPDFs/CVPR_2026/Fast_ThinkAct_Efficient_Vision_Language_Action_Reasoning_via_Verbalizable_Latent_Planning.pdf]]
