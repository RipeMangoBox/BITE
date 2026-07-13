---
title: "From Language to Locomotion: Retargeting-free Humanoid Control via Motion Latent Guidance"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/From_Language_to_Locomotion_Retargeting_free_Humanoid_Control_via_Motion_Latent_Guidance.pdf
project_link: null
code_link: null
openreview_forum_id: k3Cyx3Uets
aliases:
- FLLRFHCMLG
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/robotics
core_operator: "是否去除显式运动解码与重定向步骤，直接以语言-运动潜变量作为策略条件信号。"
primary_logic: "将运动潜变量视为一级条件信号，通过扩散策略直接从噪声中降噪生成可执行动作，消除中间环节误差，实现端到端的实时、鲁棒控制。"
claims:
- "RoboGhost将端到端流水线时间从17.85秒缩短至5.84秒。"
- "与基线方法相比，成功率提高5%，跟踪误差降低。"
- "在相同仿真环境下，潜变量驱动策略（Ours-Implicit）的成功率和跟踪误差均优于显式重定向流水线（Ours-Explicit）。"
- "扩散策略在未见运动子集上的泛化成功率（0.68）远高于MLP策略（0.54）。"
---

# From Language to Locomotion: Retargeting-free Humanoid Control via Motion Latent Guidance

> [!tip] 核心洞察
> 将运动潜变量视为一级条件信号，通过扩散策略直接从噪声中降噪生成可执行动作，消除中间环节误差，实现端到端的实时、鲁棒控制。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 从语言到运动：基于运动潜变量引导的无重定向人形机器人控制 |
| 英文题名 | From Language to Locomotion: Retargeting-free Humanoid Control via Motion Latent Guidance |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=k3Cyx3Uets) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/robotics |
| Method | RoboGhost |
| Dataset | HumanML (MotionMillion) - IsaacGym, HumanML3D, Kungfu (MotionMillion) - IsaacGym |

> [!tip] 效果简介
> - HumanML (MotionMillion) - IsaacGym 上，Success Rate (Succ ↑) 为 0.97 (Ours-DDPM)，对比 0.92 (Baseline)，变化 +0.05。
> - HumanML (MotionMillion) - IsaacGym 上，E_mpjpe ↓ 为 0.12 (Ours-DDPM)，对比 0.23 (Baseline)，变化 -0.11。
> - HumanML3D 上，FID ↓ 为 11.706 (Ours-DDPM)，对比 11.790 (MotionStreamer, 次优)，变化 -0.084 (略优)。

## 概要

**问题瓶颈**：传统语言驱动人形机器人运动控制依赖多阶段流水线——先将文本解码为显式人体运动序列，再通过重定向将运动映射到机器人关节空间，最后由跟踪策略执行。这一范式导致三个核心问题：(1) 各阶段误差逐级累积，最终控制精度受损；(2) 重定向环节成为推理延迟的主要瓶颈，完整流水线耗时高达17.85秒；(3) 语言语义与控制信号之间耦合松散，难以实现端到端优化。

**核心思路**：RoboGhost 提出了一种无重定向（retargeting-free）的潜变量驱动控制框架。其关键洞察在于：将运动潜变量视为一级条件信号，直接驱动策略生成可执行动作，从而彻底消除显式运动解码与重定向这两个中间环节。具体而言，框架由三个核心模块构成——连续自回归运动生成器从文本提示中产生紧凑的运动潜变量，基于混合专家（MoE）的教师策略在仿真中通过强化学习获取专家动作监督，基于扩散模型的学生策略以运动潜变量为条件，通过去噪过程直接输出关节动作。

**方法定位**：RoboGhost 在方法谱系上同时推进了文本到运动生成与运动跟踪控制两条技术线。在生成侧，采用因果自回归Transformer–扩散混合架构替代传统的离散Transformer或纯扩散模型；在控制侧，将策略架构从确定性MLP映射升级为扩散去噪策略，并引入因果自适应采样机制动态优先训练困难运动片段。与显式重定向流水线（如PHC + 运动解码）相比，RoboGhost 的隐式潜变量驱动方案在成功率和跟踪误差上均表现更优。

**主要结果**：
- **推理效率**：端到端流水线时间从17.85秒缩短至5.84秒。
- **跟踪性能**：在HumanML测试集上，成功率从基线方法的0.92提升至0.97，平均关节位置误差（E_mpjpe）从0.23降至0.12。
- **泛化能力**：扩散策略在未见运动子集上的泛化成功率达到0.68，远高于MLP策略的0.54。
- **消融验证**：去除因果自适应采样导致成功率下降5个百分点；x0-prediction优化目标（成功率0.97）显著优于ε-prediction（0.79）；DDIM仅需2步去噪即可达到最优性能，进一步降低推理延迟。

**局限性提示**：当前实验限于平坦地面运动，训练数据过滤了非平面地形和不可行接触；真机演示仅在部分任务上进行，极端动态动作（如后空翻）的真实世界鲁棒性尚待验证。



语言指令驱动机器人运动一直是具身智能领域的核心目标。在人形机器人这一类别中，传统方法遵循一条多阶段流水线：首先通过文本到运动生成模型将语言指令解码为显式的人体运动序列，随后利用重定向算法将人体运动映射到目标人形机器人的关节空间，最后由运动跟踪策略执行这些参考轨迹。这条流水线虽然逻辑清晰，但其固有的结构性缺陷正在成为制约系统实时性与鲁棒性的关键瓶颈。

**误差累积与语义–控制弱耦合。** 多阶段流水线中的每个模块独立优化，模块间的误差在级联过程中逐步放大。文本到运动生成阶段引入的语义歧义或运动伪影，在重定向阶段被进一步扭曲为物理不可行的关节目标，最终导致跟踪策略的失败。更重要的是，语言语义与底层控制动作之间仅通过显式运动序列间接关联，这种松散的耦合使得系统难以对语言指令的细微变化做出鲁棒响应。

**高延迟阻碍实时部署。** 传统流水线的端到端延迟令人难以接受。重定向步骤通常需要数百至上千次迭代优化才能收敛，例如 **PHC** (Luo et al., 2023) 在1000次迭代下的重定向时间高达11.89秒，加上运动生成与策略推理的时间，整个流水线耗时可达17.85秒。这一延迟量级使得系统完全无法满足实时交互的需求。

**运动表示与策略接口的错配。** 现有框架将运动表示为显式的关节角度或关键点序列，这种高维、冗余的表示不仅增加了重定向的计算负担，也迫使跟踪策略在庞大的状态空间中学习复杂的映射关系。一个根本性的问题是：是否必须保留显式的运动解码与重定向步骤？能否将紧凑的运动语义直接作为策略的条件信号，从而消除中间环节？

基于上述分析，本文的核心动机在于：**去除显式运动解码与重定向步骤，将语言–运动潜变量作为一级条件信号，通过扩散策略直接从噪声中降噪生成可执行动作**。这一设计有望从根本上消除中间环节的误差累积，实现端到端的实时、鲁棒控制，同时保持语言语义与运动控制之间的紧密耦合。



## 核心方法与创新机理

RoboGhost 的核心创新在于将传统语言驱动人形机器人运动控制中的**多阶段流水线压缩为端到端的潜变量驱动范式**，从根本上消除了运动解码与重定向环节带来的误差累积和延迟瓶颈。

### 1. 从显式运动序列到隐式运动潜变量

传统方法（如 **PHC**（Luo et al., 2023）配合 **MDM**（Tevet et al., 2023）等文本到运动模型）的流程是：文本 → 显式人体运动序列 → 重定向到机器人关节 → 跟踪策略执行。这一多阶段设计存在三个固有问题：各模块独立优化导致误差累积；重定向计算（如 PHC 的迭代优化）引入显著延迟；语义指令与控制策略之间缺乏直接耦合。

RoboGhost 将这一接口彻底替换：**连续自回归运动生成器**直接输出紧凑的运动潜变量 $l_{ref}$，该潜变量作为一级条件信号输入策略网络，无需经过运动解码和重定向。这一设计将“语言到运动”与“运动到控制”两个阶段解耦为“语言到潜变量”与“潜变量到动作”，使策略直接学习从语义条件到可执行动作的映射。

### 2. 扩散策略替代确定性 MLP 策略

传统跟踪策略通常采用基于 MLP 的确定性映射（如 **Exbody2**（Ji et al., 2024）、**GMT**（Chen et al., 2025）），这类架构在面临运动分布多样性或潜变量噪声时鲁棒性不足。

RoboGhost 引入**基于扩散模型的去噪策略**：训练时向教师动作注入高斯噪声，学生策略学习从噪声中恢复原始动作（$x_0$-prediction）；推理时通过 DDIM 确定性采样快速生成动作。这一设计使策略能够捕获多模态动作分布，对不完美的运动潜变量具有更强的容错能力。消融实验证实，扩散策略在未见运动子集上的泛化成功率（0.68）远高于 MLP 策略（0.54），且引入噪声后性能衰减更小。

### 3. 因果自适应采样

传统训练中均匀采样运动片段会导致策略在简单片段上过拟合，在困难片段上欠拟合。RoboGhost 提出**因果自适应采样**策略：当策略在时刻 $t$ 失败时，通过指数衰减核将采样概率增量 $\Delta p_i = \alpha(t-i) \cdot p$ 分配给失败前的因果前导区间 $[t-s, t]$，从而动态提高困难片段的训练频率。消融实验表明，去除该策略后成功率从 0.97 降至 0.92。

### 4. 混合架构运动生成器

运动生成器采用**连续自回归因果 transformer-扩散混合架构**，通过因果注意力掩码和掩码自回归机制确保长时序运动的一致性，避免了标准离散 transformer（如 **T2M-GPT**（Zhang et al., 2023a）、**MoMask**（Guo et al., 2023））在连续运动空间中的量化误差。

### 5. 关键性能增益

上述创新带来的端到端效果体现在两个核心指标上：**全流水线时间从 17.85 秒缩短至 5.84 秒**（约 3 倍加速），**成功率比基线方法提高 5%**，同时跟踪误差（E_mpjpe）从 0.23 降至 0.12。与包含显式重定向的流水线（Ours-Explicit）相比，隐式潜变量驱动方案（Ours-Implicit）在成功率和跟踪精度上均有显著优势，直接验证了去除重定向环节的因果效应。



![[assets/figures/papers/paper_list_l43_https_openreview_net_forum_id_k3Cyx3Uets/figures/003_Figure_2.jpg]]
*Figure 2: Overview of RoboGhost. We propose a two-stage approach: a motion latent is first generated, then a MoE-based teacher policy is trained with RL and a diffusion-based student policy is trained to denoise actions conditioned on motion latent. This latent-driven scheme bypasses the need for motion retargeting*

RoboGhost 提出了一种**无重定向、潜变量驱动**的人形机器人运动控制框架，将语言指令到机器人执行动作的端到端流程压缩为两个核心阶段，彻底移除了传统流水线中显式的运动解码与运动重定向环节。

### 两阶段流水线

如图 2 所示，整个框架由三个核心模块串联构成，按执行顺序分为两个阶段：

**阶段一：运动潜变量生成。** 给定自然语言提示 $T$，连续自回归运动生成器 $G$ 直接输出一个紧凑的运动潜变量表示 $l_{ref}$，即 $l_{ref} = G(T)$。该潜变量编码了目标运动的语义与动态特征，但无需解码为显式的人体关节序列，从而避免了传统文本到运动生成中解码误差的引入。

**阶段二：潜变量条件策略执行。** 运动潜变量 $l_{ref}$ 与机器人本体感知状态、历史观测共同作为条件信号，输入扩散学生策略 $\pi_s$。该策略通过去噪过程直接从噪声中生成可执行的动作指令，驱动机器人完成目标运动。

### 模块间数据流与接口

三个核心模块的职责与接口关系如下：

1. **连续自回归运动生成器**（见 3.2 节）：采用因果自编码器与掩码自回归架构，以因果注意力掩码确保时序一致性。训练时按余弦调度 $\gamma(\tau) = \cos(\pi\tau/2)$ 进行时间掩码，推理时自回归生成紧凑潜变量 $l_{ref}$，作为下游策略的条件输入。

2. **基于 MoE 的教师策略**（见 3.3.1 节）：在仿真环境中通过强化学习训练，利用特权信息优化目标 $\pi_t = \arg\max_\pi \mathbb{E}_{s \in \mathcal{D}}[\mathrm{Performance}(\pi, s)]$。多个专家策略的输出按其门控概率分布加权组合，产生高质量的参考动作序列，为学生策略提供监督信号。

3. **潜变量驱动扩散学生策略**（见 3.3.2 节）：以运动潜变量 $l_{ref}$、本体感知和历史观测为联合条件，采用类 DAgger 方式训练。训练时向教师动作注入高斯噪声（前向过程 $q(x_t|x_{t-1}) = \mathcal{N}(x_t; \sqrt{1-\alpha_t} \cdot x_{t-1}, \alpha_t \mathbf{I})$），以 $x_0$-prediction 为目标进行监督；推理时通过 DDIM 确定性逆向采样 $x_{t-1} = \sqrt{\alpha_{t-1}}(\frac{x_t - \sqrt{1-\alpha_t} \cdot \epsilon_\theta(x_t, t)}{\sqrt{\alpha_t}}) + \sqrt{1-\alpha_{t-1}} \cdot \epsilon_\theta(x_t, t)$ 快速生成动作。

### 因果自适应采样

为提升对困难运动片段的鲁棒性，框架引入因果自适应采样策略（见 3.4 节）。当策略在时刻 $t$ 发生失败时，该机制将失败归因于其因果前导区间 $[t-s, t]$，并按指数衰减核对采样概率进行增量更新：$\Delta p_i = \alpha(t-i) \cdot p,\ i \in [t-s, t]$，随后 $p_i' \gets p_i + \Delta p_i$。这一机制动态提高了困难片段的训练频率，无需人工设计课程。

### 与传统流水线的关键差异

传统语言驱动运动控制流水线需要依次完成：文本→显式运动序列解码→运动重定向→跟踪控制，各阶段误差累积且总耗时高达 17.85 秒。RoboGhost 将运动潜变量作为一级条件信号，直接跳过解码与重定向步骤，将全流程时间压缩至 5.84 秒。消融实验（Table 4）证实，隐式潜变量驱动方案（Ours-Implicit）的成功率和跟踪误差均优于包含 PHC 重定向的显式流水线（Ours-Explicit），验证了去除中间环节对系统性能的因果性增益。



RoboGhost 框架由三个核心模块构成：连续自回归运动生成器、基于 MoE 的教师策略，以及潜变量驱动的扩散学生策略。以下逐一展开各模块的关键设计与公式。

### 3.2 连续自回归运动生成器

运动生成器的目标是：给定文本提示 $T$，输出紧凑的运动潜变量 $l_{ref}$，即

$$l_{ref} = G(T)$$

该生成器采用因果自编码器与连续掩码自回归架构，并引入因果注意力掩码以保证时序一致性。训练时，对运动序列施加时间掩码，掩码比率遵循余弦调度：

$$\gamma(\tau) = \cos\left(\frac{\pi\tau}{2}\right) \tag{1}$$

其中 $\tau \in [0, 1]$ 均匀采样。这一调度使得模型在训练早期看到更多上下文，逐步过渡到高掩码比率的生成任务，从而学习鲁棒的时序依赖。

### 3.3.1 基于 MoE 的教师策略

教师策略在仿真环境中通过强化学习训练，能够访问特权信息（如地面真值运动、接触力等），优化目标为最大化在运动数据集 $\mathcal{D}$ 上的期望表现：

$$\pi_t = \arg\max_{\pi} \mathbb{E}_{s \in \mathcal{D}}\left[\text{Performance}(\pi, s)\right] \tag{2}$$

最终动作为多个专家策略输出的加权组合：$a = \sum_{i=1}^{n} p_i \cdot a_i$，其中 $p_i$ 为门控网络输出的概率分布，$a_i$ 为第 $i$ 个专家的动作。MoE 结构使教师策略能覆盖多样化的运动模式，为后续学生策略蒸馏提供高质量监督信号。

### 3.3.2 潜变量驱动的扩散学生策略

学生策略的核心创新在于：以运动潜变量 $l_{ref}$ 替代显式参考运动序列，结合本体感知状态和历史观测作为条件，通过扩散过程直接生成可执行动作。

**训练阶段** 采用 DAgger 式方法，向教师动作逐步注入高斯噪声，前向扩散过程为马尔可夫链：

$$q(x_t | x_{t-1}) = \mathcal{N}\left(x_t; \sqrt{1 - \alpha_t} \cdot x_{t-1}, \alpha_t \mathbf{I}\right) \tag{3}$$

其中 $x_0$ 为教师动作，$\alpha_t$ 为噪声调度参数。学生策略学习从噪声中恢复原始动作，采用 **x0-prediction** 目标（消融实验表明其成功率 0.97 远优于 ε-prediction 的 0.79，见 Table 17）。

**推理阶段** 使用 DDIM 确定性逆向采样实现快速动作生成：

$$x_{t-1} = \sqrt{\alpha_{t-1}} \left(\frac{x_t - \sqrt{1 - \alpha_t} \cdot \epsilon_\theta(x_t, t)}{\sqrt{\alpha_t}}\right) + \sqrt{1 - \alpha_{t-1}} \cdot \epsilon_\theta(x_t, t) \tag{4}$$

其中 $\epsilon_\theta$ 为学生策略网络。DDIM 采样使得仅需少量去噪步数即可生成高质量动作，实验表明增加步数几乎不提升追踪性能但显著增加推理延迟（Table 14）。

### 3.4 因果自适应采样

为提升对困难运动片段的训练效率，引入因果自适应采样策略。当策略在时刻 $t$ 失败时，将失败归因到前导区间 $[t-s, t]$，并按指数衰减核对各时刻的采样概率进行增量更新：

$$\Delta p_i = \alpha(t - i) \cdot p, \quad i \in [t-s, t] \tag{5}$$

更新后的概率为 $p_i' \gets p_i + \Delta p_i$。其中 $\alpha$ 为衰减因子，$p$ 为基础增量。该机制使训练分布动态偏向失败因果链上的关键片段，消融实验表明去除 CAS 后成功率从 0.97 降至 0.92（Table 12）。



## 实验与关键发现

### 文本到运动生成评估

RoboGhost 的运动生成器在 HumanML3D 基准和 HumanML 子集上均取得有竞争力的 FID 指标（Table 1），其中 Ours-DDPM 在 HumanML3D 上达到 11.706，略优于次优的 MotionStreamer（11.790）。这表明连续自回归因果 transformer-扩散混合架构能够生成高质量的运动潜变量，为下游控制提供可靠的语义条件信号。

![[assets/figures/papers/paper_list_l43_https_openreview_net_forum_id_k3Cyx3Uets/figures/005_Table_1.jpg]]
*Table 1: Quantitative results of text-to-motion generation on the HumanML3D dataset and HumanML subset. → denotes that if the value is closer to the ground truth, the metric is better. Table 2: Motion tracking performance comparison in simulation on the HumanML and Kungfu test sets*

### 运动跟踪主结果

在 IsaacGym 仿真环境中，RoboGhost 在 HumanML 测试集上取得 **0.97 的成功率**，较基线（0.92）提升 5 个百分点，同时平均每关节位置误差（E_mpjpe）从 0.23 降至 0.12，降幅约 48%（Table 2）。在更具挑战性的 Kungfu 数据集上，成功率从 0.66 提升至 0.72，增长 6 个百分点。在 MuJoCo 仿真器中的跨引擎评估同样验证了该趋势（Table 4），Ours-Implicit 的 Succ/E_mpjpe/E_mpkpe 均优于包含 PHC 重定向的显式流水线（Ours-Explicit），说明去除显式运动解码与重定向步骤能够有效消除多阶段流水线中的误差累积。

![[assets/figures/papers/paper_list_l43_https_openreview_net_forum_id_k3Cyx3Uets/figures/010_Table_4.jpg]]
*Table 4: Motion tracking performance comparison across different simulators on the HumanML and Kungfu test sets. Explicit version including PHC retargeting (1000 interations) and latent decode processes*

### 流水线效率

传统语言驱动人形机器人运动流程需依次执行文本到运动生成、运动重定向和跟踪控制，总耗时约 17.85 秒。RoboGhost 将这一端到端流水线压缩至 **5.84 秒**（Table 6 中 MLP 骨干的 Time Cost），加速约 3 倍。这一提升的核心机制在于：运动潜变量直接作为策略的条件信号，省去了显式运动序列解码和逐帧重定向的计算开销。

### 扩散策略 vs. MLP 策略

Table 5 的左表显示，在 HumanML 子集上，扩散策略（Succ 0.97, E_mpjpe 0.12）在跟踪性能上优于 MLP 策略（Succ 0.96, E_mpjpe 0.17）。更关键的是泛化能力差异：在未见运动子集上，扩散策略的成功率达到 **0.68**，远高于 MLP 策略的 **0.54**（Table 5 右表）。Figure 4 进一步揭示，在注入噪声后，扩散策略的跟踪性能下降幅度明显小于 MLP 策略，说明去噪过程赋予了策略对潜变量扰动更强的鲁棒性。

![[assets/figures/papers/paper_list_l43_https_openreview_net_forum_id_k3Cyx3Uets/figures/011_Table_5.jpg]]
*Table 5: Comparison of MLP-based and diffusion-based policy. The left table shows the tracking performance on HumanML subset, and the right table presents the generalization ability of two different policy architectures*

### 扩散骨干网络选择

Table 6 对比了 DiT 和 MLP 两种扩散骨干网络。MLP 骨干在 IsaacGym 上取得 0.97 的成功率，略高于 DiT 的 0.96，同时推理耗时仅 5.84 秒，远低于 DiT 的 14.28 秒。这表明在运动跟踪任务中，轻量 MLP 骨干即可有效建模动作分布，无需复杂的 transformer 架构。

### 消融研究

**因果自适应采样（CAS）**：去除 CAS 后，HumanML 上的成功率从 0.97 降至 0.92，跟踪误差同步增大（Table 12）。CAS 通过失败因果归因动态提高困难运动片段的采样概率，使训练资源聚焦于策略的薄弱环节。

**优化目标**：x0-prediction 优化目标（Succ 0.97）显著优于 ε-prediction（Succ 0.79）（Table 17），说明直接预测干净动作比预测噪声更适合运动跟踪的蒸馏场景。

![[assets/figures/papers/paper_list_l43_https_openreview_net_forum_id_k3Cyx3Uets/figures/035_Table_17.jpg]]
*Table 17: Tracking performance on different optimization objectives*

**DDIM 采样步数**：增加 DDIM 去噪步数几乎不提升跟踪性能，但显著增加推理延迟（Table 14），因此实际部署中可使用较少步数以换取实时性。

**运动生成器兼容性**：Table 19 显示，当学生策略使用其他生成器（如 MLD、T2M-GPT、MoMask）的潜变量时，跟踪性能均有下降。此外，对离散 transformer 生成器进行微调可能导致其生成指标退化，揭示了生成器与策略之间的耦合敏感性。

### 与其他跟踪策略对比

Table 13 将 RoboGhost 与 Exbody2（Ji et al., 2024）和 GMT（Chen et al., 2025）在仿真中进行对比。在 HumanML 和 Kungfu 两个测试集、IsaacGym 和 MuJoCo 两个仿真器上，RoboGhost 的成功率和跟踪误差均优于这两种专门的运动跟踪策略。这表明潜变量驱动范式在跟踪精度上具有结构优势，而非仅依赖更强的策略网络。

### 重定向方法的效率-精度权衡

Table 3 展示了不同 PHC 迭代步数下的推理时间与跟踪性能。将迭代步数从 1000 降至 100 可将推理时间从 11.89 秒压缩至 1.63 秒，但成功率从 0.93 骤降至 0.81，跟踪误差同步放大。这一权衡揭示了显式重定向流水线的根本瓶颈：加速与精度不可兼得，而 RoboGhost 的隐式方案从根本上绕开了这一矛盾。

### 失败模式与局限

当前实验仅限于平坦地面运动，训练数据过滤了非平面地形和不可行接触。在真机演示中，RoboGhost 在部分任务上展示了可行性（Figure 6），但极端动态任务（如后空翻）的真实世界鲁棒性尚未充分验证。此外，框架在不同人形机器人形态间的迁移能力，以及向楼梯、斜坡等非平坦地形的泛化，仍属开放问题。

### 补充图表

![[assets/figures/papers/paper_list_l43_https_openreview_net_forum_id_k3Cyx3Uets/figures/008_Figure_3.jpg]]
*Figure 3: Qualitative results in the IsaacGym and MuJoCo. Table 3: Average inference time and tracking performance on different retargeting methods*



## 定位与知识库关联

### 1. 与现有工作的关系

RoboGhost 的核心贡献在于消除了传统语言驱动人形机器人运动控制中“运动解码→重定向→跟踪”的多阶段流水线。在现有范式中，系统首先通过文本到运动生成模型（如 **MLD** (Chen et al., 2023)、**T2M-GPT** (Zhang et al., 2023a)、**MoMask** (Guo et al., 2023)、**MDM** (Tevet et al., 2023)）将语言指令解码为显式人体运动序列，随后依赖重定向方法（如 **GMR** (Araujo et al., 2025) 或 **PHC** (Luo et al., 2023)）将人体运动映射到机器人关节空间，最后由运动跟踪策略（如 **Exbody2** (Ji et al., 2024)、**GMT** (Chen et al., 2025)）执行。这一流程的瓶颈在于：各阶段独立优化导致误差累积，重定向迭代（如 PHC 1000 步）带来显著推理延迟，且语义指令与控制策略之间仅存在弱耦合。

RoboGhost 的方法定位是**以运动潜变量为一级条件信号的端到端控制框架**。其关键改造体现在五个维度：

- **运动表示与接口**：将显式运动序列替换为紧凑的运动潜变量 $l_{ref}$，直接作为策略的条件信号，绕过解码与重定向步骤。
- **策略架构**：从基于 MLP 的确定性映射升级为基于扩散模型的去噪策略，采用 DDIM 加速采样，以更好地捕获多模态动作分布。
- **运动生成器架构**：设计连续自回归因果 transformer-扩散混合架构（因果注意力 + 掩码自回归），替代标准离散 transformer 或扩散模型，确保长时序运动一致性。
- **训练采样策略**：从均匀采样升级为因果自适应采样，根据失败统计动态优先采样困难运动片段。
- **知识蒸馏目标**：学生策略从 ε-prediction 切换为 x0-prediction，直接预测干净动作而非噪声。

### 2. 适用边界

RoboGhost 的当前适用边界由以下条件界定：

- **地形限制**：训练与评估数据均过滤了非平面地形和不可行接触，因此框架仅在平坦地面上得到验证。Table 2 中的仿真结果（IsaacGym 和 MuJoCo）均基于平坦地形设定。
- **运动类型**：支持高动态运动（如后空翻、舞蹈跳跃），但真机演示仅在部分任务（Unitree G1，Figure 6）上进行，极端动态任务在真实世界中的鲁棒性尚未充分验证。
- **机器人形态**：实验基于 Unitree G1 人形机器人平台。框架是否可直接迁移到不同关节配置的人形机器人，或是否需要重新训练生成器与策略，目前未经验证。
- **输入模态**：当前仅支持语言指令作为输入。其他模态（图像、音频）的融合是否会引入新的延迟或性能瓶颈，仍是开放问题。

### 3. 局限与开放问题

**已识别的局限**：

1. **地形泛化不足**：框架在平坦地面上的性能已得到充分验证（HumanML 成功率 0.97，Kungfu 成功率 0.72），但能否直接泛化到楼梯、斜坡等非平坦地形，需要进一步实验确认。
2. **真机验证有限**：虽然仿真中展示了高动态运动，但真机实验覆盖的运动类型有限，极端动态任务（如后空翻）的真实世界鲁棒性有待验证。
3. **生成器依赖性**：Table 19 的消融实验表明，使用其他生成器的潜变量时追踪性能均有下降，且微调离散 transformer 生成器可能导致生成指标退化。这意味着运动生成器与策略之间存在较强的耦合，限制了模块的即插即用性。

**开放问题**：

- 运动潜变量是否包含足够的物理可行性信息，以支持长时间、不间断的复杂动作序列？当前实验主要评估固定长度运动片段的跟踪性能，未系统考察长时间序列的累积误差行为。
- 在不同人形机器人形态下，是否需要重新训练生成器或策略？框架的“无重定向”特性依赖于生成器与策略在特定机器人上的联合训练，其跨形态迁移能力尚未被研究。
- 除语言外，其他模态（图像、音频）的输入如何与现有框架无缝融合？是否需要在潜变量空间中引入额外的对齐机制？
- 因果自适应采样（CAS）的失效归因机制依赖于仿真中的特权信息（如精确的关节位置误差），在真实世界部署时如何构建等效的失败检测与归因机制，是工程落地的关键挑战。



## 原文 PDF

![[paperPDFs/ICLR_2026/From_Language_to_Locomotion_Retargeting_free_Humanoid_Control_via_Motion_Latent_Guidance.pdf]]
