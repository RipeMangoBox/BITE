---
title: Learning Generalizable Human Motion Generator with Reinforcement Learning
type: paper
paper_level: A
venue: arXiv
year: 2024
pdf_ref: paperPDFs/arxiv_2024/Learning_Generalizable_Human_Motion_Generator_with_Reinforcement_Learning.pdf
project_link: null
code_link: null
aliases:
- LGHMGRL
tags:
- arxiv_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/benchmarks_datasets_evaluation
core_operator: 将文本到运动生成形式化为马尔可夫决策过程（MDP），并利用基于对比预训练文本与运动编码器的奖励函数进行强化学习微调，无需真实运动序列即可优化模型对新文本描述的泛化能力。
primary_logic: 受 RLHF 启发，通过设计基于对比预训练编码器（负欧氏距离）的奖励函数，可在仅有合成文本数据或配对数据的情况下，使用 PPO 有效地对齐运动生成与文本描述，从而解决数据稀缺导致的泛化问题。
claims:
- 现有方法在训练数据稀缺时对特定运动表达过拟合，难以生成未见过的运动组合。
- 使用基于对比预训练编码器的奖励函数，可有效衡量生成运动与文本的语义对齐，指导强化学习。
- InstructMotion 在人类评估中大幅超越 MoMask 和 T2M-GPT，展现出更强的泛化能力。
- HumanML3D 上 R-Precision Top-1 = 0.505 (InstructMotion)
---

# Learning Generalizable Human Motion Generator with Reinforcement Learning

> [!tip] 核心洞察
> 受 RLHF 启发，通过设计基于对比预训练编码器（负欧氏距离）的奖励函数，可在仅有合成文本数据或配对数据的情况下，使用 PPO 有效地对齐运动生成与文本描述，从而解决数据稀缺导致的泛化问题。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于强化学习的可泛化人体运动生成器 |
| 英文题名 | Learning Generalizable Human Motion Generator with Reinforcement Learning |
| 会议/期刊 | arXiv 2024 |
| Links | [paper](https://arxiv.org/abs/2405.15541) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/benchmarks_datasets_evaluation |
| Method | InstructMotion |
| Dataset | HumanML3D, KIT-ML, Human Evaluation |

> [!tip] 效果简介
> - HumanML3D 上，R-Precision Top-1 0.505 (InstructMotion) vs T2M-GPT (见原文) (显著提升)；FID 0.099 (ablated) / 0.381 (main) vs T2M-GPT (见原文) (提升)；MM-Dist 2.815 vs T2M-GPT (见原文) (降低)。
> - KIT-ML 上，R-Precision Top-1 0.505 (可能为误标，见分析) vs T2M-GPT (提升)。
> - Human Evaluation (Novel Prompts) 上，Normalized Score 0.37 (Unpaired Train) / 0.43 (Unpaired Test) vs MoMask / T2M-GPT (lower) (大幅领先)。

## 概要

文本驱动的人体运动生成在实际应用中面临一个关键瓶颈：现有方法因配对训练数据稀缺，往往过度拟合训练集中特定的运动表达，难以泛化到未见过的动作组合描述。针对这一问题，本文提出 **InstructMotion**，将文本到运动生成形式化为马尔可夫决策过程（MDP），并借鉴 RLHF 的思想，利用基于对比预训练文本与运动编码器的奖励函数，通过强化学习（PPO）对预训练的自回归运动生成器进行微调，从而在无需真实运动序列的情况下，显著提升模型对新文本描述的泛化能力。

核心思路在于：以 **T2M-GPT**（Zhang et al., CVPR 2023）作为基础自回归模型，将其下一运动 token 的预测过程解释为 MDP；设计奖励函数时，采用对比预训练编码器计算文本与生成运动嵌入之间的负欧氏距离作为对齐度量，并可选择性地加入运动-运动对齐项。此外，方法利用大语言模型（LLM）合成大量无配对运动的新颖文本描述，进一步扩展训练数据的覆盖范围。

在 HumanML3D 和 KIT-ML 两个标准基准上，InstructMotion 在 R-Precision Top-1、FID 和 MM-Dist 等指标上均取得显著提升。更具说服力的是人类评估结果：在针对新颖运动组合描述的测试中，InstructMotion 的归一化得分（0.37/0.43）大幅领先 **MoMask**（Guo et al., arXiv 2023）和 T2M-GPT，直接验证了其在泛化能力上的优势。消融实验进一步确认了组合奖励设计、评论家网络共享策略以及 PPO 超参数设置的有效性。

该方法的主要局限在于其泛化能力受限于奖励模型——后者仅在有限配对数据上训练，可能无法捕捉细粒度运动细节，且优先关注语义对齐而非精确控制。未来的方向包括利用合成配对数据训练更强的奖励模型，以及探索该框架在扩散模型等其他生成范式上的扩展。

文本驱动的人体运动生成旨在根据自然语言描述合成逼真的三维人体动作序列，在动画制作、虚拟现实和人机交互等领域具有广泛应用。近年来，基于自回归变换器（如 **T2M-GPT**，Zhang et al., CVPR 2023）和扩散模型（如 **MDM**，Tevet et al., arXiv 2022；**MotionDiffuse**，Zhang et al., TPAMI 2024）的方法在标准基准上取得了显著进展。

然而，实际应用揭示了一个共同的瓶颈：**现有方法往往对训练数据中的特定运动表达产生过拟合，难以泛化到未见过的运动组合描述**。这一问题根源于文本-运动配对训练数据的稀缺性——收集大规模、多样化的高质量配对数据成本极高，导致模型在监督学习范式下只能覆盖有限的运动语义空间。当面对诸如“边走边挥手”这类训练集中未直接出现的组合动作时，已有方法的生成质量会显著下降。

本文的核心动机正是解决这一泛化难题。受大语言模型对齐中 RLHF（基于人类反馈的强化学习）范式的启发，作者提出将文本到运动生成重新形式化为马尔可夫决策过程（MDP），并引入强化学习的试错机制来突破配对数据的限制。其核心洞见在于：**通过设计基于对比预训练文本与运动编码器的奖励函数，可以在仅有合成文本描述或少量配对数据的情况下，利用 PPO 算法有效地将运动生成与文本语义对齐**，从而在不依赖真实运动序列的条件下提升模型对新描述的泛化能力。

## 核心方法与创新机理

InstructMotion 的核心创新在于将**文本驱动运动生成重新形式化为强化学习问题**，从而绕过传统监督学习对大规模配对数据的强依赖。具体而言，该方法在三个关键维度上改变了基线模型 T2M-GPT（Zhang et al., CVPR 2023）的设计逻辑：

### 1. 训练范式：从监督模仿到强化探索

基线方法 T2M-GPT 采用标准的自回归交叉熵损失进行训练，其优化目标是最小化生成的运动 token 序列与真实运动 token 序列之间的差异。这种“模仿学习”范式在训练数据覆盖不足时，会直接导致模型对训练集中出现的特定运动模式产生过拟合。

InstructMotion 将自回归生成过程解释为**马尔可夫决策过程（MDP）**，其中：
- **状态**：当前已生成的运动 token 序列与文本条件；
- **动作**：下一个运动 token 的预测；
- **策略**：自回归 Transformer 生成器。

在此框架下，模型不再需要“标准答案”式的真实运动序列作为监督信号，而是通过**试错探索**来最大化一个精心设计的奖励函数。这种范式转变使得模型可以在仅有文本描述（无配对运动数据）的条件下进行有效学习。

### 2. 奖励信号：基于对比预训练编码器的语义对齐度量

传统方法仅依赖真实运动序列的损失作为训练信号，这从根本上限制了模型在未见文本描述上的泛化能力。InstructMotion 设计了一个**基于对比预训练文本与运动编码器的奖励函数**，其核心是编码器输出嵌入之间的负欧氏距离：

$$r(\mathbf{t}, \mathbf{m}) = \begin{cases} -\lambda_t \|\mathbf{f_t} - \mathbf{f_{m_{pred}}}\|^2, & \text{text-only} \\ -\lambda_t \|\mathbf{f_t} - \mathbf{f_{m_{pred}}}\|^2 - \lambda_m \|\mathbf{f_{m_{gt}}} - \mathbf{f_{m_{pred}}}\|^2, & \text{paired} \end{cases}$$

这一设计的核心洞见在于：**奖励模型无需看到过未见动作组合的真实运动序列，即可评估生成运动与文本描述之间的语义对齐程度**。该能力来源于编码器在对比学习（Eq. 1）中习得的跨模态语义空间，使得语义相近的文本-运动对在嵌入空间中距离更近。

当仅有纯文本数据（无配对运动）时，奖励函数仅包含运动-文本对齐项；当有配对数据时，可额外加入运动-运动对齐项以提供更细粒度的监督。

### 3. 训练数据：LLM 合成文本扩展训练分布

传统方法仅使用数据集中已有的配对文本-运动数据进行训练。InstructMotion 引入了**LLM 辅助的新颖运动描述生成流水线**：首先从训练数据中提取元运动（meta motions）类别，然后随机组合这些元运动，利用大语言模型生成自然语言描述，最后经人工筛选确保描述的合理性与流畅性。

这一数据扩展策略使得模型在训练阶段就能接触到训练集中未曾出现的运动组合描述，从而在强化学习微调过程中主动学习如何泛化到这些新颖描述。消融实验（Figure 5b）证实，**增加合成数据量可以持续提升模型的泛化能力**。

### 方法谱系与知识库定位

InstructMotion 处于**文本驱动人体运动生成**与**基于人类反馈的强化学习（RLHF）**的交叉点。其方法论谱系可梳理如下：

- **基础生成架构**：继承自 T2M-GPT（Zhang et al., CVPR 2023）的 VQ-VAE + 自回归 Transformer 框架，包括 CLIP 文本编码器、运动 VQ-VAE 离散化、以及逐 token 自回归解码。
- **强化学习范式**：受 RLHF 启发，将生成过程形式化为 MDP，使用 PPO 算法（clip 损失 + 价值函数损失 + KL 惩罚）进行策略优化，这与语言模型中 RLHF 的技术路线高度一致。
- **奖励建模**：借鉴对比学习在跨模态检索中的成功经验，使用 Guo et al. 提出的对比预训练运动-文本编码器构建奖励函数，而非训练独立的奖励模型。
- **数据增强**：利用 LLM 进行组合式文本生成，类似于指令微调中的数据合成思路。

与同期方法相比，**MDM**（Tevet et al., arXiv 2022）和 **MotionDiffuse**（Zhang et al., TPAMI 2024）基于扩散模型，**MoMask**（Guo et al., arXiv 2023）采用掩码建模，它们均依赖完整的配对数据进行监督训练。InstructMotion 的独特之处在于**将泛化能力的提升机制从“更好的数据拟合”转向“更灵活的奖励引导”**，这使得模型在训练数据覆盖不足的场景下具有本质优势。

### 关键限制

奖励模型本身仅在有限的配对数据上训练，其语义判别能力受限于训练数据的覆盖范围。这意味着对于奖励模型无法准确评估的细粒度运动细节，强化学习优化可能无法提供有效引导。此外，奖励函数优先考虑全局语义对齐，可能导致生成的运动在局部细节上不够精确。

InstructMotion 将文本到运动生成形式化为一个马尔可夫决策过程（MDP），并在此基础上构建强化学习微调框架。其核心流程由四个关键模块串联而成：**文本编码器**、**运动生成器（演员网络）**、**奖励模型**和**PPO 优化器**，如 Figure 2 所示。

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2405_15541/figures/002_Figure_2.jpg]]
*Figure 2: The over pipeline of InstructMotion. Given a batch of textual prompts, the pre-trained autoregressive generator first produces the corresponding motion sequences, which is fed into the reward model along with the text prompts to assess the generation quality, yielding a matching score. The score, combined with the prediction logits and the the critic model output (omitted in the figure), is then organized by the PPO algorithm to optimize the generator in a inner training loop*

### 输入输出流

给定一批文本提示 $\mathbf{t}$，预训练的自回归 Transformer 生成器（演员网络）首先逐 token 生成对应的运动序列 $\mathbf{m}_{\text{pred}}$。这一生成过程天然符合 MDP 结构：每个运动 token 的预测可视为一个动作，已生成的 token 序列构成状态，文本嵌入作为条件上下文贯穿整个生成过程。

生成的预测运动随后与文本提示一同送入奖励模型。奖励模型基于对比预训练的文本编码器和运动编码器，计算文本嵌入 $\mathbf{f_t}$ 与预测运动嵌入 $\mathbf{f_{m_{pred}}}$ 之间的负欧氏距离作为对齐分数：

$$r(\mathbf{t}, \mathbf{m}) = \begin{cases} -\lambda_t \|\mathbf{f_t} - \mathbf{f_{m_{pred}}}\|^2, & \text{text-only} \\ -\lambda_t \|\mathbf{f_t} - \mathbf{f_{m_{pred}}}\|^2 - \lambda_m \|\mathbf{f_{m_{gt}}} - \mathbf{f_{m_{pred}}}\|^2, & \text{paired} \end{cases}$$

该奖励函数的关键设计在于**支持两种数据模式**：当仅有纯文本（无配对运动）时，仅使用运动-文本对齐项；当存在配对数据时，额外加入运动-运动对齐项以约束生成质量。

### 优化闭环

PPO 优化器接收奖励分数、演员网络的预测 logits 以及评论家网络输出的状态价值估计，通过裁剪的替代损失和价值损失更新演员与评论家参数。优化的目标是最大化期望奖励，同时通过 KL 散度惩罚项约束当前策略 $\pi_\theta$ 不偏离参考策略 $\pi_{\text{ref}}$ 过远：

$$\mathcal{T}_r(\pi_\theta) = \mathbb{E}_{\mathbf{t}\sim p_{data}, \mathbf{m}\sim \pi_\theta} \left[ r(\mathbf{t}, \mathbf{m}) - \beta \log \frac{\pi_\theta(\mathbf{m} \mid \mathbf{t})}{\pi_{ref}(\mathbf{m} \mid \mathbf{t})} \right]$$

评论家网络与演员共享底层参数以提升计算效率，消融实验证实该设计在保证性能的同时降低了训练开销（Table 3b）。

### 数据层面的关键创新

区别于传统监督学习仅依赖配对文本-运动数据，InstructMotion 额外引入 LLM 辅助生成的合成文本描述（Figure 3）。这些描述通过随机组合“元动作”并由 LLM 润色生成，经人工筛选确保合理性后，作为无配对运动的纯文本数据参与训练。这一数据扩充策略直接针对配对数据稀缺这一瓶颈，使模型能够接触到训练集中未出现的动作组合描述，从而在强化学习过程中习得对新颖组合的泛化能力。

整个框架的模块依赖关系清晰：文本编码器和运动 VQ-VAE 提供嵌入空间基础，奖励模型定义优化方向，PPO 算法执行策略搜索，合成数据注入打破训练分布边界。这一闭环使得生成器无需真实运动序列即可通过试错学习对齐文本语义，是实现泛化能力的结构保障。

InstructMotion 将文本驱动运动生成形式化为马尔可夫决策过程（MDP），并围绕三个核心模块构建强化学习微调框架：**奖励模型**、**演员网络**与**评论家网络**、**PPO 优化器**。各模块协同完成“生成-评估-优化”的闭环。

### 奖励模型与对比预训练编码器

奖励模型是整个框架的因果旋钮。它基于对比预训练的文本编码器和运动编码器，计算生成运动与文本描述之间的语义对齐分数。

**编码器训练**：文本编码器与运动编码器采用对比损失联合训练，使匹配的文本-运动对在嵌入空间中靠近，不匹配的对相互远离：

$$\mathcal{L}_{CL} = (1-y) (\|\mathbf{f_t} - \mathbf{f_m}\|)^2 + y (max(0, m - \|\mathbf{f_t} - \mathbf{f_m}\|))^2$$

其中 $y$ 指示文本与运动是否匹配（$y=0$ 匹配，$y=1$ 不匹配），$m$ 为边界超参数。$\mathbf{f_t}$ 和 $\mathbf{f_m}$ 分别为文本和运动的全局嵌入向量。

**奖励函数设计**：基于上述编码器，奖励函数定义为嵌入空间中的负欧氏距离。针对不同数据可用性，奖励函数分为两种模式：

$$r(\mathbf{t}, \mathbf{m}) = \begin{cases} -\lambda_t \|\mathbf{f_t} - \mathbf{f_{m_{pred}}}\|^2, & \text{text-only} \\ -\lambda_t \|\mathbf{f_t} - \mathbf{f_{m_{pred}}}\|^2 - \lambda_m \|\mathbf{f_{m_{gt}}} - \mathbf{f_{m_{pred}}}\|^2, & \text{paired} \end{cases}$$

- **纯文本模式**：仅使用预测运动嵌入 $\mathbf{f_{m_{pred}}}$ 与文本嵌入 $\mathbf{f_t}$ 的距离，权重为 $\lambda_t$。
- **配对数据模式**：额外加入预测运动与真实运动嵌入 $\mathbf{f_{m_{gt}}}$ 的距离项，权重为 $\lambda_m$，用于约束运动质量。

这一设计使 InstructMotion 能够同时利用配对数据和 LLM 生成的纯文本描述进行训练，从根本上缓解了配对数据稀缺导致的过拟合问题。

### 演员网络与评论家网络

**演员网络**沿用了预训练的自回归 Transformer 生成器（基于 **T2M-GPT**，Zhang et al., CVPR 2023）。在 MDP 框架下，状态 $s_t$ 为已生成的部分运动 token 序列与文本嵌入的拼接，动作 $a_t$ 为下一个运动 token 的预测。该 Transformer 包含 18 层，维度 1024，16 个注意力头。

**评论家网络**与演员网络共享底层表示，但在计算价值估计时对共享特征进行 detach 操作，以防止价值损失的梯度干扰策略学习。消融实验表明，共享底层且使用 detach 的设计在保证性能的同时提升了计算效率。

### PPO 优化目标

强化学习的目标是最大化期望奖励，同时约束策略不偏离参考策略过远。总体优化目标为：

$$\mathcal{T}_r(\pi_\theta) = \mathbb{E}_{\mathbf{t}\sim p_{data}, \mathbf{m}\sim \pi_\theta} \left[ r(\mathbf{t}, \mathbf{m}) - \beta \log \frac{\pi_\theta(\mathbf{m} \mid \mathbf{t})}{\pi_{ref}(\mathbf{m} \mid \mathbf{t})} \right]$$

其中 $\beta$ 控制 KL 惩罚的强度，$\pi_{ref}$ 为预训练生成器的参考策略。

具体实现采用 PPO 算法，其策略损失为裁剪的替代目标：

$$\mathcal{L}^{PM}(\theta) = \mathbb{E}_t \left[ \min \left( \frac{\pi_\theta(a_t|s_t)}{\pi_{\theta_{old}}(a_t|s_t)} A_t, \; \text{clip}\left(\frac{\pi_\theta(a_t|s_t)}{\pi_{\theta_{old}}(a_t|s_t)}, 1-\epsilon, 1+\epsilon\right) A_t \right) \right]$$

价值网络损失为预测价值与回报的均方误差：

$$\mathcal{L}^{VF}(\phi) = \mathbb{E}_t \left[ (V_\phi(s_t) - G_t)^2 \right]$$

其中 $A_t$ 为优势函数，$G_t$ 为折扣回报，$\epsilon$ 为裁剪范围。消融实验确定 PPO 内部 epoch 数为 2、内部 batch 比率为 1/2 时获得最佳性能。

### 合成文本数据生成流水线

为支持纯文本模式的训练，InstructMotion 引入 LLM 辅助的新颖运动描述生成流水线：首先从现有数据集中提取元运动标签，随机组合后由 LLM 生成自然语言描述，再经人工筛选剔除不合理的组合。该流水线为强化学习提供了大量无配对运动的文本描述，是泛化能力提升的关键数据基础。

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2405_15541/figures/003_Figure_3.jpg]]
*Figure 3: An illustration of the LLM-assisted novel motion description generation pipeline*

## 实验与关键发现

### 瓶颈与核心发现

文本驱动运动生成的核心瓶颈在于：现有模型在配对训练数据稀缺时，会过度拟合训练集中的特定运动表达，难以泛化到未见过的运动组合描述（Introduction）。InstructMotion 的核心发现是，将文本到运动生成形式化为马尔可夫决策过程（MDP），并利用基于对比预训练编码器的奖励函数进行强化学习微调，可以在仅有合成文本或配对数据的情况下，有效对齐运动生成与文本描述，从而突破数据稀缺导致的泛化边界。

### 主实验：HumanML3D 与 KIT-ML 基准

**Table 1** 报告了 HumanML3D 测试集上的定量比较。InstructMotion 在 R-Precision Top-1 上达到 0.505，显著超越基线 **T2M-GPT**（Zhang et al., CVPR 2023）。MM-Dist 降至 2.815，表明生成运动与文本的语义对齐更紧密。FID 在主实验配置下为 0.381，消融最佳配置下可进一步压缩至 0.099。与扩散模型 **MDM**（Tevet et al., arXiv 2022）和 **MotionDiffuse**（Zhang et al., TPAMI 2024）相比，InstructMotion 在语义对齐指标上保持优势，但需注意部分方法依赖真实序列长度（§A 标记），可能影响公平性。

**Table 2** 展示了 KIT-ML 测试集上的结果。InstructMotion 在 R-Precision Top-1 上达到 0.505（原文标注可能存在歧义，置信度 0.5，建议手动对照原文验证），同样优于 T2M-GPT 基线。两个基准上的提升幅度一致，表明方法跨数据集具有稳定性。

### 人类评估：泛化能力的决定性证据

**Figure 5a** 提供了最关键的泛化证据。在人类评估中，使用三种不同的提示集（配对训练集、未配对训练集、未配对测试集）对 InstructMotion、**MoMask**（Guo et al., arXiv 2023）和 T2M-GPT 进行比较。InstructMotion 在未配对训练集和未配对测试集上分别获得 0.37 和 0.43 的归一化分数，大幅领先 MoMask 和 T2M-GPT。这一结果直接验证了核心主张：强化学习微调使模型能够生成训练数据中未见过的运动组合，泛化能力显著优于监督学习范式。

### 消融实验：奖励设计、评论家网络与 PPO 设置

**Table 3** 系统消融了三个关键设计维度：

| 消融维度 | 关键发现 | 证据锚点 |
|---------|---------|---------|
| 奖励设计 | 组合奖励（运动-文本对齐 + 运动-运动对齐）在配对测试集上同时改善 FID 和 Top-1 | Table 3a |
| 评论家网络 | 与演员共享底层并使用 detach 操作，在保持性能的同时提升计算效率 | Table 3b |
| PPO 训练设置 | epoch 数为 2、内部 batch 比率为 1/2 时获得最佳性能 | Table 3c |

**Figure 5c** 的奖励设计消融揭示了反直觉发现：在泛化能力（人类评估）上，仅使用运动-文本对齐的奖励反而获得更多正向反馈，加入运动-运动对齐项并未带来额外增益。这可能说明奖励模型对细粒度运动细节的捕捉能力有限，与论文自述的局限性一致。

### 数据规模效应

**Figure 5b** 展示了合成数据规模的缩放实验。结果表明，增加 LLM 生成的合成文本描述数量可以持续提升模型在未配对测试集上的泛化性能。这一趋势支持了核心方法论：利用合成数据缓解配对数据稀缺是可行的，且边际收益尚未出现明显饱和。

### 失败模式与局限性

论文明确指出的局限性包括：
1. **奖励模型瓶颈**：奖励模型仅在有限的配对数据上训练，可能无法捕捉细粒度运动细节，导致生成运动在精确控制上存在不足。
2. **语义对齐优先于精细控制**：奖励函数优先考虑全局语义对齐，可能牺牲局部运动细节的精确性。

此外，Figure 5c 的消融结果显示运动-运动对齐奖励在泛化评估中未带来增益，暗示当前奖励设计在捕捉运动质量方面仍有改进空间。这些局限性需要在手动验证中进一步确认其具体表现形式。

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2405_15541/figures/004_Table_1.jpg]]
*Table 1: Quantitative comparison on HumanML3D [16] test set. The evaluation metrics are computed following Guo et al. [16]. The evaluation is repeated 20 times for confidence interval estimation. § A indicates reliance on ground-truth sequence length for generation*

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2405_15541/figures/005_Table_2.jpg]]
*Table 2: Quantitative comparison on KIT-ML [36] test set. The evaluation metrics are computed following Guo et al. [16]. The evaluation is repeated 20 times for confidence interval estimation*

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2405_15541/figures/001_Figure_1.jpg]]
*Figure 1: Examples generated from simple and compositional given textual descriptions. Our method significantly outperforms previous state-of-the-art method MoMask [15] in terms of generalization capability to novel motion compositions. The compositional descriptions are generated with the aid of large language models, as discussed in Section 4.2*

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2405_15541/figures/006_Figure_4.jpg]]
*Figure 4: Qualitative comparisons with top-performing methods. Our InstructMotion exhibits enhanced generalization capability and accurately interpret novel combinations of motion instructions*

## 定位与知识库关联

### 1. 与基线方法的关系

**InstructMotion** 的起点是自回归运动生成器 **T2M-GPT**（Zhang et al., CVPR 2023），其核心组件——CLIP 文本编码器、运动 VQ-VAE 和自回归 Transformer——均直接继承自 T2M-GPT 的预训练权重。两者的本质差异在于**训练范式**：T2M-GPT 采用标准的监督学习（交叉熵损失），仅在配对文本-运动数据上优化；InstructMotion 则将其重新形式化为马尔可夫决策过程（MDP），引入强化学习微调。

这种范式转换的关键在于**奖励信号的重构**。T2M-GPT 的优化目标完全依赖真实运动序列的逐 token 损失，而 InstructMotion 使用基于对比预训练编码器的嵌入距离作为奖励函数（负欧氏距离），使得模型可以在**仅有文本描述、无配对运动**的数据上进行有效优化。这一设计直接回应了配对数据稀缺导致的过拟合瓶颈。

与扩散模型路线的方法相比，**MDM**（Tevet et al., arXiv 2022）和 **MotionDiffuse**（Zhang et al., TPAMI 2024）同样面临泛化挑战，但其生成范式不同（去噪过程 vs. 自回归采样），InstructMotion 的 RL 微调框架在原理上并不限于自回归架构，论文也将其列为开放问题。**MoMask**（Guo et al., arXiv 2023）作为对比的 SOTA 方法，在人类评估的泛化测试中被 InstructMotion 大幅超越（标准化得分 0.37 vs. 更低值，Figure 5a），但其残差量化设计本身并非本工作的改进对象。

### 2. 适用边界

**有效范围：**
- 适用于以文本描述为条件、需要生成未见过的动作组合（compositional motion）的场景，尤其是训练数据中缺乏对应配对样本的情况。
- 框架依赖一个预训练的自回归运动生成器作为 actor，且需要额外的对比预训练文本与运动编码器作为 reward model，因此要求基础模型已在足够规模的配对数据上完成预训练。
- 合成文本数据的生成依赖 LLM 和人工筛选（Figure 3 所示流程），适用于可以定义“元动作”类别并组合描述的任务域。

**边界条件：**
- 奖励模型本身仅在有限的配对数据上训练，其语义对齐能力构成了泛化性能的上限——如果 reward model 无法准确评估某类细粒度运动与文本的匹配度，RL 优化将缺乏有效指导。
- 论文明确指出，奖励函数优先考虑语义对齐而非细粒度控制，因此生成运动的局部精确性可能弱于完全依赖真实运动监督的方法。
- 当前验证限于 HumanML3D 和 KIT-ML 两个基准，向更大规模、更高自由度运动域的迁移尚待验证。

### 3. 局限与待解决问题

**已确认的局限：**
1. **奖励模型的容量瓶颈**：对比预训练编码器仅在有限配对数据上训练，可能无法捕捉细粒度运动细节（如手指动作、面部表情），导致 RL 优化在这些维度上缺乏有效反馈。
2. **语义对齐与精细控制的权衡**：奖励函数的设计偏向全局语义匹配，生成的运动在整体语义上正确，但局部细节可能不够精确——消融实验（Figure 5c）也显示，仅使用运动-文本对齐奖励在人类评估中获得更多正向反馈，说明运动-运动对齐项的引入在某些情况下反而干扰了泛化质量。
3. **合成数据的质量控制**：LLM 生成的组合描述需经人工筛选以排除不合理组合，这一步骤限制了全自动化扩展的可能性。

**待解决的开放问题：**
- 能否通过合成配对数据（如运动拼接）来训练更强的奖励模型，从而突破当前 reward model 的容量上限？
- 该 RL 微调框架能否有效扩展到扩散模型（如 MDM、MotionDiffuse）等非自回归架构？
- 奖励函数中运动-文本对齐项（$\lambda_t$）与运动-运动对齐项（$\lambda_m$）的最优权重在不同数据集和任务上如何变化？Table 3a 的消融仅在 HumanML3D 上进行，缺乏跨数据集的系统性结论。
- 合成文本数据的规模与多样性对泛化性能的边际效应是否存在上限？Figure 5b 显示了持续提升趋势，但未达到饱和点，更大规模实验尚缺。

### 4. 知识库定位

InstructMotion 处于**文本驱动运动生成**与**基于人类反馈的强化学习（RLHF）**的交叉点。其核心贡献不在于提出新的生成架构，而在于**将 RLHF 的对齐思想迁移到运动生成领域**，用对比预训练编码器替代人工反馈作为奖励信号源，从而绕过了 RLHF 通常依赖的人类标注成本。

在方法谱系上，它属于“预训练 + RL 微调”范式，与语言模型领域的 InstructGPT 共享概念框架，但针对连续-离散混合的动作空间做了适配（运动 token 化 + PPO 裁剪损失）。其独特之处在于利用了**合成文本数据**（LLM 生成的无配对描述）来扩展 RL 的训练分布，这在现有运动生成方法中尚无先例。

对于后续工作，该框架提示了两个可拓展方向：一是用更强的 reward model（如基于大规模运动-文本对比预训练的编码器）替换当前的奖励函数；二是将 MDP 形式化推广到其他条件生成任务中，只要能够定义合理的状态、动作和奖励空间。

## 原文 PDF

![[paperPDFs/arxiv_2024/Learning_Generalizable_Human_Motion_Generator_with_Reinforcement_Learning.pdf]]
