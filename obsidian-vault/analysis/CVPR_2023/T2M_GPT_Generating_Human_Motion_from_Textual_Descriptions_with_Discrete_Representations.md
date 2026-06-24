---
title: "T2M-GPT: Generating Human Motion from Textual Descriptions with Discrete Representations"
type: paper
paper_level: A
venue: CVPR
year: 2023
pdf_ref: paperPDFs/CVPR_2023/T2M_GPT_Generating_Human_Motion_from_Textual_Descriptions_with_Discrete_Representations.pdf
aliases:
- TG
- T2M-GPT
tags:
- CVPR_2023
- topic/motion_animation
- topic/motion_animation/human_motion_generation
core_operator: "VQ-VAE训练中的EMA和Code Reset策略有效缓解码本坍缩，提升离散表示质量；GPT训练时随机替换部分真实码本索引为随机索引（corruption策略）缩小了训练-推理差距。"
primary_logic: "简单的VQ-VAE+GPT框架，配合经典的量化训练技巧（EMA、Code Reset）和一种轻量序列破坏策略，无需复杂设计即可在文本到动作生成任务上取得超越扩散模型的性能，尤其在大幅降低FID的同时保持文本-动作一致性。"
claims:
- "T2M-GPT在HumanML3D上取得了FID 0.116，显著优于MotionDiffuse的0.630，生成质量大幅领先同期扩散方法。"
- "EMA与Code Reset联合使用是VQ-VAE成功的关键，仅使用naive VQ-VAE无法生成高质量动作，重建和生成FID极差（Table 3）。"
- "数据集规模是当前方法的瓶颈，使用10%训练数据时文本-动作一致性较差，随着数据增加性能持续提升（Figure 5）。"
- "HumanML3D 上 FID = 0.116"
---

# T2M-GPT: Generating Human Motion from Textual Descriptions with Discrete Representations

> [!tip] 核心洞察
> 简单的VQ-VAE+GPT框架，配合经典的量化训练技巧（EMA、Code Reset）和一种轻量序列破坏策略，无需复杂设计即可在文本到动作生成任务上取得超越扩散模型的性能，尤其在大幅降低FID的同时保持文本-动作一致性。

| 字段 | 内容 |
|------|------|
| 中文题名 | T2M-GPT：基于离散表示的文本到人体动作生成 |
| 英文题名 | T2M-GPT: Generating Human Motion from Textual Descriptions with Discrete Representations |
| 会议/期刊 | CVPR 2023 |
| Links | [paper](https://arxiv.org/abs/2301.06052) · [Project](https://mael-zys.github.io/T2M-GPT/) |
| Topic | #topic/motion_animation #topic/motion_animation/human_motion_generation |
| Method | T2M-GPT |
| Dataset | HumanML3D |

> [!tip] 效果简介
> - HumanML3D 上，FID 为 0.116，对比 0.630 (MotionDiffuse)，变化 -0.514。
> - HumanML3D 上，R-Precision Top-3 为 0.775，对比 0.772 (MLD)，变化 +0.003。
> - HumanML3D 上，MM-Dist 为 3.118，对比 3.347 (Guo et al.)，变化 -0.229。

## 概述

文本到人体动作生成的核心挑战在于：如何从自然语言描述中合成语义一致、视觉逼真且多样化的三维人体动作序列。现有方法多依赖扩散模型，在生成质量（FID）上仍有较大提升空间。T2M-GPT 提出了一种简洁的两阶段框架，将动作生成建模为离散空间中的自回归序列生成问题，绕开了扩散模型的复杂设计。

**核心瓶颈**：VQ-VAE 在动作序列建模中容易发生码本坍缩，导致离散表示质量差；GPT 自回归生成存在训练-推理不一致（曝光偏差），限制了简单框架在文本到动作生成上的性能。

**因果调控**：VQ-VAE 训练中引入 EMA 和 Code Reset 策略有效缓解码本坍缩，提升离散表示质量；GPT 训练时随机替换部分真实码本索引为随机索引（corruption 策略）缩小了训练-推理差距。

**核心洞见**：简单的 VQ-VAE + GPT 框架，配合经典的量化训练技巧（EMA、Code Reset）和一种轻量序列破坏策略，无需复杂设计即可在文本到动作生成任务上取得超越扩散模型的性能，尤其在大幅降低 FID 的同时保持文本-动作一致性。

**方法定位**：T2M-GPT 属于离散表示驱动的自回归生成范式，与当前主流的扩散方法（如 MDM、MotionDiffuse、MLD）形成鲜明对比。其框架由冻结的 CLIP 文本编码器、Motion VQ-VAE（编码器-码本-解码器）和因果自回归 Transformer 三个模块构成，通过可学习的 End token 隐式控制生成运动长度，无需额外长度预测模块。

**关键证据**：
- 在 HumanML3D 数据集上，T2M-GPT 取得 FID **0.116**，显著优于 MotionDiffuse 的 0.630（Table 1），生成质量大幅领先同期扩散方法。
- EMA 与 Code Reset 联合使用是 VQ-VAE 成功的关键——仅使用 naive VQ-VAE 时，重建和生成 FID 极差（Table 3）。
- 数据集规模是当前方法的瓶颈：使用 10% 训练数据时文本-动作一致性较差，随着数据增加性能持续提升（Figure 5），暗示更大规模数据可进一步释放方法潜力。

## 背景与动机

人体动作生成是计算机视觉与图形学中的核心任务，在游戏、影视、虚拟现实和机器人仿真等领域具有广泛的应用需求。近年来，基于文本描述驱动动作生成（Text-to-Motion）逐渐成为研究热点，其目标是根据自然语言描述合成与之语义一致且物理合理的三维人体动作序列。

该任务面临双重挑战。在表示层面，人体动作是连续的高维时间序列，直接建模计算代价高昂且难以捕捉长程依赖；在生成层面，文本与动作之间存在天然的跨模态语义鸿沟，要求模型同时理解语言语义与运动动力学。早期方法通常采用多阶段流水线，例如 **Guo et al.**（CVPR 2022）提出的三阶段框架，需要分别处理动作长度预测、初始动作生成和动作细化，流程复杂且各阶段误差容易累积。后续工作转向扩散模型，如 **MDM**（Tevet et al., arXiv 2022）和 **MotionDiffuse**（Zhang et al., arXiv 2022），虽然提升了生成质量，但扩散模型在推理时依赖多步去噪过程，计算开销较大。基于VAE的方法如 **TEMOS**（Petrovich et al., ECCV 2022）和基于离散标记的方法如 **TM2T**（Guo et al., ECCV 2022）也进行了有益探索，但在生成质量与文本一致性之间仍存在权衡。

一个关键的技术瓶颈在于离散表示的质量。将连续动作序列量化为离散码本索引可以显著压缩表示空间，使自回归生成成为可能，但标准VQ-VAE在动作序列建模中极易发生**码本坍缩**——即大部分码本向量在训练中失效，只有极少数码本被实际使用，导致离散表示的信息容量急剧下降。这直接限制了后续生成模型的上限。与此同时，自回归生成框架（如GPT）存在经典的**训练-推理不一致**问题：训练时使用真实序列作为上下文（Teacher Forcing），推理时却依赖模型自身生成的序列，这种曝光偏差会随着序列增长而累积误差。

T2M-GPT的核心动机正是直面上述两个瓶颈。作者观察到，VQ-VAE在图像生成领域已有成熟的训练策略（EMA参数更新和Code Reset机制）来对抗码本坍缩，但在动作生成任务中尚未被系统性地验证和应用。同时，通过一种轻量级的序列破坏策略（在训练时随机替换部分真实码本索引为随机索引），可以有效缩小自回归模型的训练-推理差距。基于这些观察，T2M-GPT提出了一种极简的两阶段框架：先使用VQ-VAE学习动作的离散码本表示，再以冻结的CLIP文本编码器为条件，用因果自回归Transformer生成码本索引序列。该框架无需复杂的多阶段设计或扩散过程，在HumanML3D数据集上取得了FID 0.116的生成质量，显著优于同期扩散方法MotionDiffuse的0.630，同时保持了相当的文本-动作一致性。

## 核心创新

T2M-GPT的核心创新在于**以极简的VQ-VAE+GPT框架，配合三项关键训练策略，在文本到动作生成任务上超越同期扩散模型**。该方法并未引入复杂的多阶段设计或扩散过程，而是通过解决离散表示学习中的两个根本性瓶颈——**码本坍缩**与**训练-推理不一致**——实现了生成质量的大幅提升。

### 1. 量化策略改进：EMA与Code Reset联合缓解码本坍缩

VQ-VAE在动作序列建模中的核心痛点是码本坍缩：大量连续帧的编码特征被映射到极少数码本向量上，导致离散表示的表征能力急剧退化。T2M-GPT采用了两项经典的量化训练技巧来应对这一问题：

- **EMA（指数移动平均）**：在码本更新时使用EMA替代直接梯度更新，使码本向量更平滑地追踪编码器输出的分布变化，避免少数码本被过度激活。
- **Code Reset**：定期检测并重置使用频率过低的“死”码本，将其重新初始化到编码器输出的高密度区域，确保码本容量被充分利用。

消融实验（Table 3）给出了决定性证据：单独使用naive VQ-VAE时，重建FID高达0.399，生成FID更是恶化到24.86，几乎无法产生有意义的动作；单独使用EMA或Code Reset均能部分改善，但只有**EMA+Code Reset联合使用**才能将重建FID降至0.070、生成FID降至0.116。这表明两项策略存在协同效应：EMA维持码本更新的稳定性，Code Reset则主动修复失效的码本向量，二者共同保障了离散表示的质量。

### 2. 训练-推理一致性：Corruption策略缩小曝光偏差

自回归GPT在训练时使用teacher forcing（输入完全真实的码本序列），推理时却依赖自身生成的、可能包含错误的序列，这种**曝光偏差**会导致误差累积。T2M-GPT提出了一种轻量级的corruption策略：训练时随机将τ比例的真实码本索引替换为随机索引，使模型在训练阶段即接触到带噪声的输入序列，从而缩小训练与推理之间的分布差距。

实验对比了固定τ=0.5与τ从均匀分布U[0,1]采样的两种设置（Table 1）。τ=0.5在FID上略优（0.116 vs 0.141），而τ~U[0,1]在MM-Dist上相当（3.121 vs 3.118）。这一策略无需额外的对抗训练或强化学习，仅通过数据层面的简单破坏即可有效提升文本-动作一致性。

### 3. 运动长度隐式控制：可学习End Token

与Guo et al.（CVPR 2022）等基线方法需要额外模块预测运动长度不同，T2M-GPT引入了一个可学习的End Token。在自回归生成过程中，模型逐索引生成码本序列，当输出End Token时自动停止，**隐式地决定运动长度**。这一设计消除了对显式长度预测器的依赖，使框架更加简洁统一。在HumanML3D上，即使不使用真实运动长度，T2M-GPT的FID（0.116）仍显著优于使用真实长度的MotionDiffuse（0.630），表明End Token机制能够可靠地学习文本描述与运动时长之间的对应关系。

### 4. 方法定位：简单框架的有效性

与同期方法相比，T2M-GPT的独特之处在于**以简单对抗复杂**：

- 相比Guo et al.（CVPR 2022）的三阶段方法（文本到长度、长度到动作、动作细化），T2M-GPT仅需两阶段且无需显式长度预测。
- 相比MDM（Tevet et al., arXiv 2022）和MotionDiffuse（Zhang et al., arXiv 2022）等扩散方法，T2M-GPT避免了多步去噪推理，生成效率更高，且FID大幅领先（0.116 vs 0.630）。
- 相比MLD（Xin et al., arXiv 2022）的潜在扩散设计，T2M-GPT在保持相当R-Precision（Top-3: 0.775 vs 0.772）的同时，FID降低近一半。

核心启示在于：**在文本到动作生成任务中，离散表示的质量是性能上限的关键决定因素**。通过EMA+Code Reset保障VQ-VAE的码本利用率，通过corruption策略弥合自回归模型的训练-推理差距，即可在不引入复杂架构的前提下取得领先性能。

## 整体框架

T2M-GPT 采用两阶段生成范式，将文本到动作的映射问题分解为离散表示学习与条件序列生成两个子任务。整体流程如 Figure 2 所示，包含两个核心模块：**Motion VQ-VAE** 与 **T2M-GPT**（因果自回归 Transformer）。

![[assets/figures/papers/paper_list_l8_T2M_GPT_Generating_Human_Motion_from_Textual_Descriptions_with_Discrete/figures/002_Figure_2.jpg]]
*Figure 2: Overview of our framework for text-driven motion generation. It includes two modules: Motion VQ-VAE (Figure 2a) and T2M-GPT (Figure 2b). In T2M-GPT, an additional learnable End token is inserted to indicate the stop of the generation. During the inference, we first generate code indexes in an auto-regressive fashion and then obtain the motion using the decoder in Motion VQ-VAE*

### 阶段一：运动离散表示学习

Motion VQ-VAE 负责建立连续运动空间与离散码本序列之间的双向映射。给定一段人体运动序列 $X$，编码器将其压缩为潜在特征序列 $Z$，随后通过量化操作将每个特征向量映射到共享码本 $C$ 中的最近邻条目：

$$\hat{z}_i = \underset{c_k \in C}{\arg \min} \| z_i - c_k \|_2$$

量化后的码本索引序列 $S$ 经解码器重建为运动序列 $X_{re}$。训练时采用联合损失函数：

$$\mathcal{L}_{vq} = \mathcal{L}_{re} + \| Z - sg[\hat{Z}] \|_2 + \beta \| sg[Z] - \hat{Z} \|_2$$

其中重建损失 $\mathcal{L}_{re}$ 使用 L1 平滑损失，并额外引入速度正则项以提升生成质量：

$$\mathcal{L}_{re} = \mathcal{L}_1^{smooth}(X, X_{re}) + \alpha \mathcal{L}_1^{smooth}(V(X), V(X_{re}))$$

编码器-解码器采用标准一维卷积架构（Figure 3），包含 1D 卷积、残差块和 ReLU 激活，通过步长为 2 的卷积和最近邻插值实现时间维度的下采样与上采样，下采样率 $l = 2^L$（$L$ 为残差块数量，实际设置为 $l=4$）。码本大小为 $512 \times 512$。

### 阶段二：文本条件码本序列生成

T2M-GPT 是一个因果自回归 Transformer，以冻结的 CLIP 文本编码器提取的文本嵌入 $c$ 为条件，逐索引生成动作码本序列。训练目标为最大化给定文本条件下码本索引序列的对数似然：

$$\mathcal{L}_{trans} = \mathbb{E}_{S \sim p(S)} [ -\log p(S | c) ]$$

Transformer 采用带因果掩码的缩放点积注意力，确保每个位置的预测仅依赖已生成的前缀索引：

$$\mathrm{Attention} = \mathrm{Softmax} \left( \frac{ Q K^{T} \times mask }{ \sqrt{d_k} } \right)$$

其中因果掩码 $mask_{i,j} = -\infty \times \mathbf{1}(i > j) + \mathbf{1}(i \leq j)$，阻止未来位置的信息泄露。

### 运动长度控制

T2M-GPT 引入一个可学习的 **End token** 作为特殊标记，拼接在码本索引序列末尾。在自回归生成过程中，当模型预测输出 End token 时自动停止，从而隐式决定生成运动的长度，无需额外的长度预测模块。

### 推理流程

推理时，首先使用 CLIP 编码输入文本描述获得条件嵌入，随后 T2M-GPT 自回归生成码本索引序列直至遇到 End token，最后将生成的索引序列送入 Motion VQ-VAE 的解码器重建为连续运动序列。整个流程无需真实运动长度作为先验，实现了端到端的文本到运动生成。

## 核心模块与公式推导

T2M-GPT 采用两阶段框架：**Motion VQ-VAE** 负责学习动作的离散表示，**T2M-GPT** 负责以文本为条件自回归生成离散码本序列（Figure 2）。

### Motion VQ-VAE

该模块将连续动作序列映射为离散码本索引序列，并可逆向重建。编码器采用标准 1D 卷积架构，包含 Conv1D、残差块和 ReLU 激活，通过步长为 2 的卷积进行时序下采样，下采样率 $l = 2^L$（$L$ 为残差块数量，论文设置 $l=4$）。码本大小为 $512 \times 512$（Figure 3）。

**量化过程**：对编码器输出的每个特征向量 $z_i$，在码本 $C = \{c_k\}_{k=1}^{K}$ 中寻找最近邻作为量化表示：

$$\hat{z}_i = \underset{c_k \in C}{\arg \min} \| z_i - c_k \|_2 \quad \text{(Equation 1)}$$

**损失函数**：VQ-VAE 总损失由三部分组成：

$$\mathcal{L}_{vq} = \mathcal{L}_{re} + \| Z - sg[\hat{Z}] \|_2 + \beta \| sg[Z] - \hat{Z} \|_2 \quad \text{(Equation 2)}$$

其中 $sg[\cdot]$ 为 stop-gradient 操作。第二项为嵌入损失（更新码本向量靠近编码器输出），第三项为承诺损失（约束编码器输出靠近码本向量），$\beta$ 为权重系数。

**重建损失**采用 L1 平滑损失，并引入速度正则化以提升生成质量：

$$\mathcal{L}_{re} = \mathcal{L}_1^{smooth}(X, X_{re}) + \alpha \mathcal{L}_1^{smooth}(V(X), V(X_{re})) \quad \text{(Equation 3)}$$

其中 $V(\cdot)$ 计算相邻帧之间的速度（位置差分），$\alpha$ 为速度正则化权重。

**关键训练策略**：naive VQ-VAE 在动作序列建模中极易发生码本坍缩（codebook collapse），导致离散表示质量极差。T2M-GPT 采用两项经典策略联合缓解此问题：**EMA**（指数移动平均更新码本向量）和 **Code Reset**（定期重置使用频率过低的码本条目）。消融实验（Table 3）表明，单独使用任一策略或两者均不使用时，重建 FID 和生成 FID 均大幅恶化，EMA 与 Code Reset 联合使用是 VQ-VAE 成功的关键。

### T2M-GPT（Transformer）

该模块为因果自回归 Transformer，以冻结的 CLIP 文本编码器提取的文本嵌入 $c$ 为条件，逐索引生成动作码本序列 $S = [s_1, s_2, ..., s_n, end]$。

**训练目标**为最大化给定文本条件下的码本序列对数似然：

$$\mathcal{L}_{trans} = \mathbb{E}_{S \sim p(S)} [ -\log p(S | c) ] \quad \text{(Equation 4)}$$

**因果自注意力**：采用带因果掩码的缩放点积注意力，防止未来位置信息泄露：

$$\mathrm{Attention} = \mathrm{Softmax} \left( \frac{ Q K^{T} \times mask }{ \sqrt{d_k} } \right) \quad \text{(Equation 5)}$$

其中因果掩码 $mask_{i,j} = -\infty \cdot \mathbf{1}(i > j) + \mathbf{1}(i \leq j)$，确保位置 $i$ 只能关注位置 $j \leq i$。

**训练-推理不一致的缓解**：标准 teacher forcing 训练使用完全真实序列，而推理时模型依赖自身预测的历史，存在曝光偏差。T2M-GPT 采用一种轻量 **corruption 策略**：训练时随机替换 $\tau \times 100\%$ 的真实码本索引为随机索引，$\tau$ 可为固定值（如 0.5）或从 $\tau \in U[0,1]$ 均匀采样，从而缩小训练与推理之间的分布差距。

**运动长度控制**：不同于需要额外模块预测运动长度的方法（如 Guo et al., CVPR 2022），T2M-GPT 在码本序列末尾插入一个可学习的 **End token**，自回归生成至该标记时自动停止，隐式决定运动长度，简化了框架设计。

## 实验与分析

### 主实验性能对比

T2M-GPT在HumanML3D和KIT-ML两个标准基准上取得了全面的领先或可比性能。在HumanML3D测试集上（Table 1），T2M-GPT以**FID 0.116**大幅领先同期扩散方法，相比**MotionDiffuse**（Zhang et al., arXiv 2022）的0.630降低了0.514，相比**MDM**（Tevet et al., arXiv 2022）的0.544也有显著优势。这一结果表明，简单的VQ-VAE+GPT框架在生成动作的视觉质量上远超扩散模型。

![[assets/figures/papers/paper_list_l8_T2M_GPT_Generating_Human_Motion_from_Textual_Descriptions_with_Discrete/figures/004_Table_1.jpg]]
*Table 1: Comparison with the state-of-the-art methods on HumanML3D [22] test set. We compute standard metrics following Guo et al. [22]. For each metric, we repeat the evaluation 20 times and report the average with 95% confidence interval. Red and Blue indicate the best and the second best result. § reports results using ground-truth motion length*

在文本-动作一致性方面，T2M-GPT同样表现优异：R-Precision Top-3达到**0.775**，与**MLD**（Xin et al., arXiv 2022）的0.772持平，优于**Guo et al.**（CVPR 2022）的0.735；MM-Dist为**3.118**，低于Guo et al.的3.347和MotionDiffuse的3.113，表明生成动作与文本描述的语义距离更小。在多样性指标上，T2M-GPT的Diversity为**9.761**，与真实动作分布（9.503）最为接近，而扩散方法如MotionDiffuse（9.410）和MDM（9.559）均略低于真实分布。MModality为1.856，处于合理范围。

在KIT-ML数据集上（Table 2），T2M-GPT同样展现出竞争力：FID为**0.514**，R-Precision Top-1为0.416，Top-3为0.681，MM-Dist为3.032。需要指出的是，KIT-ML数据集规模较小，各方法在该基准上的性能差距不如HumanML3D显著，但T2M-GPT仍保持了与最先进方法相当的水平。

![[assets/figures/papers/paper_list_l8_T2M_GPT_Generating_Human_Motion_from_Textual_Descriptions_with_Discrete/figures/005_Table_2.jpg]]
*Table 2: Comparison with the state-of-the-art methods on KIT-ML [54] test set. We compute standard metrics following Guo et al. [22]. For each metric, we repeat the evaluation 20 times and report the average with 95% confidence interval. Red and Blue indicate the best and the second best result.§ reports results using ground-truth motion length*

所有评估均遵循Guo et al.（CVPR 2022）的标准协议，每项指标重复评估20次并报告平均值及95%置信区间，确保比较的公平性。

### 消融实验：关键设计选择

**VQ-VAE量化策略的消融**（Table 3）揭示了码本坍缩问题的严重性及解决方案的有效性。实验对比了三种设置：

- **Naive VQ-VAE**（无EMA、无Code Reset）：重建FID高达0.494，生成FID更是恶化至24.53，表明码本坍缩导致离散表示几乎失效，无法支撑后续生成任务。
- **仅使用EMA**：重建FID降至0.091，生成FID改善至1.027，但仍不理想。
- **EMA + Code Reset联合使用**：重建FID进一步降至0.070，生成FID大幅提升至0.116。

这一消融明确证实，EMA和Code Reset是VQ-VAE在动作序列建模中成功的关键因素。EMA通过动量更新保持码本稳定性，Code Reset通过定期重置低使用率码字防止码本容量浪费，二者协同作用才能产生高质量的离散表示。若缺乏这些策略，即使GPT生成能力再强，也无法弥补VQ-VAE阶段的信息损失。

**序列破坏策略（Corruption）的消融**（Section 4.1）：标准teacher forcing训练使用完全真实的历史序列，而推理时模型仅能依赖自身生成的、可能包含错误的序列，这种训练-推理不一致（曝光偏差）会损害生成质量。T2M-GPT在训练时随机替换τ比例的真实码本索引为随机索引，模拟推理时的误差分布。实验对比了不同τ设置的影响：固定τ=0.5时FID为0.116，而τ从均匀分布U[0,1]随机采样时FID为0.141，表明适度的破坏策略能有效缩小训练-推理差距。

**数据集规模的影响**（Figure 5）：实验分别使用HumanML3D训练集的10%、20%、50%、80%和100%训练VQ-VAE和GPT，并在完整测试集上评估。结果显示，随着数据量增加，重建FID从约0.35持续下降至0.07，生成FID从约3.0持续下降至0.116，同时R-Precision Top-1和Top-3持续上升。这一趋势表明，当前方法明显受限于训练数据规模，扩大数据集有望进一步提升性能。在10%数据训练时，文本-动作一致性较差，说明小样本条件下模型难以建立鲁棒的文本-动作映射。

### 定性分析与可视化

Figure 1和Figure 4展示了T2M-GPT在HumanML3D上的生成实例及与基线方法的对比。定性结果表明，T2M-GPT能够生成与具有挑战性的文本描述高度一致的人体动作序列。与Guo et al.、MDM和MotionDiffuse的对比中，T2M-GPT生成的动作品质更高，减少了扭曲（红色标注）和滑步（黄色标注）等常见伪影。这得益于VQ-VAE在重建阶段通过速度正则化（公式3中的$\mathcal{L}_1^{smooth}(V(X), V(X_{re}))$项）对运动平滑性的显式约束，以及离散码本对动作空间的紧凑表示能力。

### 失败模式与局限性

尽管T2M-GPT在整体指标上表现优异，但仍存在以下限制：

1. **VQ-VAE重建误差作为性能上限**：VQ-VAE的重建FID为0.070，这意味着即使GPT完美生成码本序列，最终动作的FID也无法低于此值。进一步降低重建损失是提升生成质量上限的关键方向。

2. **数据集规模瓶颈**：Figure 5明确显示性能随数据量单调提升，而HumanML3D（规模见[[../../references/T2M_Common_Datasets#HumanML3D|HumanML3D]]）远未达到饱和。当前方法可能在大规模数据集上获得更显著的性能增益。

3. **自回归生成的固有缺陷**：长序列生成时自回归方式存在推理效率低和误差累积的问题。虽然corruption策略部分缓解了曝光偏差，但推理时一旦早期生成错误码本索引，后续序列可能偏离正确轨迹。

4. **评估范围有限**：仅在HumanML3D和KIT-ML两个数据集上验证，缺乏在大规模、多风格、多语言描述场景下的测试。KIT-ML上的FID（0.514）与真实动作上限（0.031）仍有较大差距，表明在小数据集上方法优势不如HumanML3D明显。

### 补充图表

![[assets/figures/papers/paper_list_l8_T2M_GPT_Generating_Human_Motion_from_Textual_Descriptions_with_Discrete/figures/001_Figure_1.jpg]]
*Figure 1: Visual results on HumanML3D [22]. Our approach is able to generate precise and high-quality human motion consistent with challenging text descriptions. More visual results are on the project page*

![[assets/figures/papers/paper_list_l8_T2M_GPT_Generating_Human_Motion_from_Textual_Descriptions_with_Discrete/figures/008_Figure_5.jpg]]
*Figure 5: Impact of dataset size on HumanML3D [22]. We train our motion VQ-VAE (Reconstruction) and T2M-GPT (Generation) on the subsets of HumanML3D [22] composed of 10%, 20%, 50%, 80%, and 100% training set respectively. All the models are evaluated on the entire test set. We report FID, MM-Dist, Top-1, and Top-3 accuracy for all the models. Results suggest that our model might benefit from more training data*

![[assets/figures/papers/paper_list_l8_T2M_GPT_Generating_Human_Motion_from_Textual_Descriptions_with_Discrete/figures/007_Table_3.jpg]]
*Table 3: Analysis of VQ-VAE quantizers on HumanML3D [22] test set. For all the quantizers, we set τ = 0.5 and use the same architectures (VQ-VAE and GPT) described in Section 4.1. We report FID and Top-1 for both reconstruction and generation. For each metric, we repeat the evaluation 20 times and report the average with 95% confidence interval*

## 方法谱系与知识库定位

T2M-GPT 的提出背景是文本到动作生成领域在 2022 年前后经历了一轮快速的方法迭代：从早期的多阶段流水线方法，到基于 VAE 的生成框架，再到扩散模型的引入。理解 T2M-GPT 在这一谱系中的位置，有助于把握其设计动机与适用边界。

### 与同期方法的谱系关系

在 T2M-GPT 之前，文本到动作生成的主流方法可大致分为三类：

**多阶段流水线方法**。以 **Guo et al.**（CVPR 2022）为代表，该方法将文本到动作生成分解为多个独立阶段，包括动作长度预测、文本-动作匹配等。这类方法流程复杂，各阶段之间的误差可能累积，且需要额外的长度预测模块来显式控制生成运动的时长。

**基于 VAE 的生成框架**。**TEMOS**（Petrovich et al., ECCV 2022）采用 Transformer VAE 架构，在连续潜在空间中进行动作生成。该方法在文本-动作一致性上表现良好，但生成动作的质量（以 FID 衡量）往往不如后续的扩散方法。

**扩散模型方法**。2022 年涌现了多篇基于扩散的文本到动作生成工作，包括 **MDM**（Tevet et al., arXiv 2022）、**MotionDiffuse**（Zhang et al., arXiv 2022）和 **MLD**（Xin et al., arXiv 2022）。这些方法在生成多样性和质量上取得了显著进展，尤其是 MotionDiffuse 在 HumanML3D 上取得了当时领先的 FID 0.630。然而，扩散模型通常需要多步迭代去噪，推理速度较慢，且连续空间的建模方式引入了额外的复杂度。

T2M-GPT 的定位在于：**用极简的 VQ-VAE + GPT 框架挑战扩散模型的性能上限**。其核心赌注是，离散表示配合经典的自回归生成，只要解决了 VQ-VAE 的码本坍缩问题和 GPT 的训练-推理不一致问题，就可以在生成质量（FID）上大幅超越扩散方法，同时保持相当的文本-动作一致性。

### 关键设计差异与改进槽位

T2M-GPT 与前述方法的关键差异体现在三个设计槽位上：

**量化策略**。基线方法若直接使用 naive VQ-VAE（无额外稳定性策略），极易发生码本坍缩——码本中大量条目未被使用，导致离散表示质量极差。T2M-GPT 的改进在于引入两个经典但被同期工作忽视的训练技巧：EMA（指数移动平均）更新码本向量和 Code Reset（将长期未被使用的码本条目随机重置）。消融实验（Table 3）表明，EMA 与 Code Reset 联合使用是 VQ-VAE 成功的关键：仅使用 naive VQ-VAE 时，重建 FID 和生成 FID 均极差，单独使用 EMA 或 Code Reset 也无法达到可用的生成质量。

**GPT 训练数据构造**。标准自回归训练使用 teacher forcing，即每一步的输入都是真实的前缀序列。但在推理时，模型只能看到自己生成的序列，这种训练-推理不一致（曝光偏差）会损害生成质量。T2M-GPT 的改进是引入 corruption 策略：训练时随机替换 τ 比例的真实码本索引为随机索引，使模型在训练过程中就接触到“不完美”的前缀，从而缩小训练-推理差距。实验对比了固定 τ=0.5 和 τ 从 U[0,1] 随机采样两种设置，均在多个指标上取得了有竞争力的结果。

**运动长度处理**。Guo et al.（CVPR 2022）等方法需要额外的模块来显式预测运动长度，增加了系统复杂度。T2M-GPT 采用更优雅的方案：在码本序列末尾附加一个可学习的 End token，自回归生成过程遇到该标记时自动停止，隐式地决定运动长度。这一设计简化了框架，同时使长度控制内化于生成过程本身。

### 适用边界与局限

T2M-GPT 的适用边界受以下因素制约：

**数据规模瓶颈**。Figure 5 的实验明确显示，当仅使用 10% 训练数据时，文本-动作一致性较差；随着数据量从 10% 增加到 100%，FID 持续下降，Top-1/Top-3 准确率持续上升。这一趋势表明当前方法受限于 HumanML3D 的数据规模，在更大规模数据集上可能仍有提升空间。但这一结论目前仅在 HumanML3D 上得到验证，缺乏跨数据集的大规模扩展实验支持。

**VQ-VAE 重建上限**。VQ-VAE 的重建 FID 为 0.070（HumanML3D），这为下游生成设置了不可逾越的性能天花板。即使 T2M-GPT 的生成 FID 达到 0.116，与重建上限之间仍存在约 0.046 的差距，这部分差距来自 GPT 生成过程的误差。进一步降低重建损失（如改进 VQ-VAE 架构或增加码本容量）可能同时提升重建和生成质量，但论文未对此进行深入探索。

**长序列生成的潜在挑战**。自回归生成方式在长序列场景下可能面临推理效率低和误差累积的问题。T2M-GPT 未直接评估在超长运动序列（如超过 10 秒）上的表现，也未讨论自回归解码的加速策略（如投机解码、非自回归解码等）。这一点在需要实时生成或超长序列生成的场景中可能成为瓶颈。

**数据集与评估的局限性**。T2M-GPT 仅在 HumanML3D 和 KIT-ML 两个标准数据集上进行了验证。这两个数据集的动作风格和文本描述类型相对有限，缺乏大规模、多风格、多语言描述下的测试。此外，所有评估均使用 Guo et al.（CVPR 2022）提出的标准协议，这些指标（FID、R-Precision、MM-Dist 等）虽然被广泛采用，但能否完全反映人类对动作质量的感知仍有争议。

### 开放问题

基于以上分析，T2M-GPT 留下的开放问题包括：

1. **数据扩展的边际收益**：扩大数据集（如超过 HumanML3D 的约 15K 条动作序列）能否持续提升生成质量和文本-动作一致性？是否存在数据收益递减的拐点？

2. **跨任务迁移能力**：T2M-GPT 的离散表示框架能否迁移至其他运动生成任务，如音乐驱动舞蹈、动作预测、动作修复或动作补全？离散码本是否具有任务无关的通用性？

3. **离散与扩散的融合可能**：能否结合离散表示的简洁性与扩散模型的多样性优势？例如，在离散码本空间中进行扩散去噪，可能同时获得离散空间的高效性和扩散模型的渐进式生成能力。

4. **长序列生成效率**：对于长运动序列（如舞蹈编排、体育动作序列），自回归框架在效率与连贯性方面还有哪些改进空间？非自回归解码或层次化生成是否可行？

5. **精细运动控制与编辑**：如何在保持简单框架的同时实现更精细的运动控制，如局部关节编辑、时序组合、风格迁移等？End token 机制虽然优雅，但缺乏对运动长度的显式控制能力，这在某些应用场景中可能是缺陷而非优势。

## 原文 PDF

![[paperPDFs/CVPR_2023/T2M_GPT_Generating_Human_Motion_from_Textual_Descriptions_with_Discrete_Representations.pdf]]
