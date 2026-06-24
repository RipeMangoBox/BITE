---
title: End-to-End Language-Action Model for Humanoid Whole Body Control
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/End_to_End_Language_Action_Model_for_Humanoid_Whole_Body_Control.pdf
project_link: "https://youtu.be/U5B5Pgw1N3A"
code_link: "https://github.com/huggingface/lerobot"
aliases:
- EELAMHWBC
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 通过构建物理交互数据集并采用端到端流匹配模型，将语言指令与本体感受历史直接映射到底层关节动作，消除了中间运动表示。同时，多尺度观察、动态预测、完成预测和残差强化学习后训练等组件协同作用，使模型能够学习物理上可执行的控制策略。
primary_logic: 在物理仿真中收集大规模语言-动作轨迹，并利用流匹配直接学习从语言和机器人状态到动作的映射，可以实现比模块化生成-跟踪范式更强的语义-物理一致性和更高的执行成功率。端到端的梯度流是达成此效果的关键。
claims:
- SENTINEL在文本全身控制的主实验中，成功率达到99.45%，显著优于最高基线MDM+Retarget的94.94%（Table 2）。
- 移除长期观察后，语义对齐指标R@1从0.582剧降至0.153，MMD从3.438飙升至72.468（Table 3），证明多尺度状态历史对理解长时间跨度命令至关重要。
- 在定性对比中，MDM+Retarget因缺乏物理约束执行“jumps up in a tight twirl.”命令时失去平衡，而SENTINEL直接生成物理可行的动作，稳健完成指令（Figure 3）。
- HumanML3D test set on AMASS 上 MM-Dist ↓ = 0.487
---

# End-to-End Language-Action Model for Humanoid Whole Body Control

> [!tip] 核心洞察
> 在物理仿真中收集大规模语言-动作轨迹，并利用流匹配直接学习从语言和机器人状态到动作的映射，可以实现比模块化生成-跟踪范式更强的语义-物理一致性和更高的执行成功率。端到端的梯度流是达成此效果的关键。

| 字段 | 内容 |
|------|------|
| 中文题名 | 端到端语言-动作人形机器人全身控制模型SENTINEL |
| 英文题名 | End-to-End Language-Action Model for Humanoid Whole Body Control |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2511.19236) · [Project](https://youtu.be/U5B5Pgw1N3A) · [Code](https://github.com/huggingface/lerobot) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | SENTINEL |
| Dataset | HumanML3D test set on AMASS |

> [!tip] 效果简介
> - HumanML3D test set on AMASS 上，MM-Dist ↓ 0.487 vs 0.577 (T2M-GPT+Retarget) (-0.090)；R@1 ↑ 0.582 vs 0.481 (T2M-GPT+Retarget) (+0.101)；R@2 ↑ 0.717 vs 0.637 (T2M-GPT+Retarget) (+0.080)。

## 概述

人形机器人的语言指令全身控制长期依赖模块化流水线：先由文本生成人体运动序列，再通过全身控制器进行物理跟踪。这种范式存在根本性瓶颈——语言命令与物理动作之间缺乏紧密对齐，导致语义上合理的运动在物理执行中不可行（例如MDM+Retarget在执行“jumps up in a tight twirl.”时因大角度旋转而摔倒）。中间运动表示的设计阻断了从物理执行反馈到语言理解的梯度信号，造成跨模态一致性差。

SENTINEL针对上述瓶颈提出了范式转变：构建首个完全端到端的语言-动作模型，直接将语言指令与本体感受历史映射到底层关节动作，消除了中间运动表示。其核心机制包括：（1）在物理仿真中利用预训练的Mixture-of-Expert全身控制器跟随人体运动，构建大规模语言-动作轨迹数据集；（2）采用流匹配（flow matching）模型预测动作块，并融合多尺度状态历史（高频短期+低频长期）以捕获长时程语义；（3）通过残差强化学习后训练修正开环漂移，增强sim-to-real迁移能力。

实验结果表明，SENTINEL在文本全身控制主测试中成功率达到99.45%，显著优于最强基线MDM+Retarget的94.94%（Table 2）。语义对齐指标R@1达到0.582，MMD降至3.438，均超越T2M-GPT+Retarget等模块化方法。消融实验揭示，移除长期观察会导致R@1从0.582剧降至0.153，MMD从3.438飙升至72.468（Table 3），验证了多尺度状态历史对理解长时间跨度命令的关键作用。在真实机器人Unitree G1上的部署进一步证实了该方法的零样本sim-to-real迁移能力。

## 背景与动机

### 问题背景

使机器人能够理解自然语言指令并执行全身运动控制，是实现通用人机交互和自主操作的核心目标。对于人形机器人而言，这一任务尤为复杂：它不仅需要解析语言的语义内容，还必须在高维连续动作空间中生成物理上可执行的控制序列，同时维持动态平衡和运动稳定性。

### 现有方法及其缺口

当前的主流方案采用**模块化流水线**范式：首先利用文本到运动生成模型（如MDM、T2M-GPT）合成人体运动序列，再通过全身控制器或重定向策略将运动映射到机器人的底层关节指令。这一范式存在两个根本性缺陷：

1. **语义-物理对齐断裂**：语言命令与最终执行之间插入的中间运动表示（如人体姿态序列）阻断了梯度信号从物理执行反馈到语言理解的传递。模块化设计使得上游生成器无法感知物理可行性约束，导致语义上相似的运动在物理执行中不可行。例如，当执行“jumps up in a tight twirl.”指令时，MDM+Retarget因缺乏物理约束而生成大角度旋转，导致机器人在仿真中失去平衡摔倒（Figure 3）。

2. **跨模态一致性差**：中间运动表示的设计需要人为定义映射规则，这一过程不可避免地引入信息损失和偏差，使得语言命令与最终执行动作之间的语义对齐难以保证。

部分工作尝试直接从文本映射到机器人姿态（如UH-1）或使用CVAE+DAgger架构（如LangWBC），但前者仍需通过控制器跟踪中间姿态，后者则受限于短时本体感受输入（仅2秒历史）和相对简单的MLP架构，难以处理长时间跨度的复杂指令。

### 本文动机

上述分析揭示了一个核心瓶颈：**模块化设计无法建立语言命令与物理动作之间的紧密对齐**。要突破这一瓶颈，需要一种能够将语言理解、状态感知和物理执行统一在端到端框架中的方法。本文提出SENTINEL，旨在通过以下关键设计实现这一目标：

- **端到端映射**：直接从语言指令和本体感受历史映射到底层关节动作，消除所有中间表示，使梯度信号能够贯通整个管道。
- **物理交互数据驱动**：在物理仿真中构建大规模语言-动作轨迹数据集，使模型从数据中学习物理上可执行的控制策略。
- **多尺度状态感知**：融合高频短期（50Hz）和低频长期（4Hz）状态历史，使模型能够理解跨越数十秒的复杂指令。
- **残差强化学习后训练**：在域随机化下通过PPO微调，修正开环预测的累积漂移，增强sim-to-real迁移能力。

## 核心创新

SENTINEL在人形机器人语言到全身控制领域引入了一项**范式级转变**：从传统的“文本→中间运动表示→全身控制器”模块化流水线，转向**完全端到端的语言-动作模型**。这一转变的核心在于消除了对中间运动表示（如人体骨骼序列、关节角度轨迹）的依赖，使模型能够直接从自然语言指令和本体感受历史映射到底层关节动作。分析表明，该范式的关键优势在于打通了从物理执行反馈到语言理解的梯度流，从而解决了模块化方法中普遍存在的“语义相似但物理不可行”问题——例如MDM+Retarget在执行“jumps up in a tight twirl.”时因缺乏物理约束而失去平衡（Figure 3）。

为实现这一范式，SENTINEL在方法层面做出了以下关键创新：

**1. 动作生成机制：从扩散模型到流匹配动作块预测**

传统文本到运动生成方法（如MDM、T2M-GPT）依赖扩散模型或自回归Transformer生成人体运动序列，这些方法在物理执行前需要额外的重定向和控制步骤。SENTINEL将动作生成重新定义为**流匹配（flow matching）问题**，在连续时间框架下学习从简单先验分布到目标动作分布的矢量场变换。具体而言，动作专家被实现为一个流匹配模型，预测未来H步的动作块，其训练目标为最小化预测速度场与目标速度场之间的距离：

$$\mathcal{L}(\theta) = \mathbb{E}_{p(\mathbf{A}_t|c_t), q(\mathbf{A}_t^\tau|\mathbf{A}_t)} \left\| v_\theta(\mathbf{A}_t^\tau, \tau, c_t) - u(\mathbf{A}_t^\tau|\mathbf{A}_t) \right\|^2$$

其中目标速度定义为 $u = \epsilon - \mathbf{A}_t$，推断时通过离散时间步积分得到动作块：

$$\mathbf{A}_t^{\tau-\Delta t} = \mathbf{A}_t^{\tau} - v_\theta(\mathbf{A}_t^\tau, \tau, c_t) \cdot \Delta t$$

这一设计使模型能够在统一的概率框架下处理多模态的动作分布，同时保持与语言条件的紧密耦合。

**2. 观察输入：从短时本体感受到多尺度状态历史**

基线方法LangWBC仅使用约2秒的短时本体感受历史，这限制了模型对长时程语言命令（如“先向前走，然后挥手”）的理解能力。SENTINEL引入了**多尺度状态历史**机制，同时维护高频短时状态（50Hz，10步）和低频长时状态（4Hz，10秒）：

$$\mathbf{s}_t^{\mathrm{hist}} = [\mathbf{s}_t^{\mathrm{long\_term}}, \mathbf{s}_t^{\mathrm{short\_term}}]$$

这一设计的必要性在消融实验中得到强有力验证：移除长期观察后，语义对齐指标R@1从0.582剧降至0.153，MMD从3.438飙升至72.468（Table 3），证明多尺度历史对于理解跨时间尺度的语言指令至关重要。

**3. 训练策略：从行为克隆到大规模预训练+残差强化学习后训练**

LangWBC采用基于CVAE和DAgger的行为克隆策略，这在分布外场景下容易出现复合误差。SENTINEL采用**两阶段训练策略**：首先在大规模语言-动作数据集上进行流匹配预训练，学习通用的语言到动作映射；随后引入轻量级**残差动作头** $\pi_\Delta$，通过PPO在域随机化下进行后训练，修正预训练模型的开环漂移：

$$\Delta a_t = \pi_\Delta(s_t, \tilde{a}_t)$$

残差后训练将sim-to-real成功率从95.44%提升至99.11%（Table 5），且通过主动终止奖励（Active Termination）等设计保持了语言跟随能力——移除该奖励项导致R@1从0.392降至0.255（Table 10）。

**4. 任务终止：从被动超时到主动完成预测**

传统方法依赖固定时长或超时机制终止任务，无法感知命令是否已完成。SENTINEL引入了**完成预测头**（两层MLP），预测任务是否将在未来H步内完成，使机器人能够主动终止当前命令并平滑过渡到下一个指令（Figure 8）。训练时通过加权组合流匹配损失和完成预测损失进行联合优化：

$$\mathcal{L} = \mathcal{L}_{\mathrm{fm}} + \lambda \mathcal{L}_{\mathrm{done}}$$

其中 $\lambda=0.01$。这一机制使SENTINEL具备了自主顺序执行多条指令的能力，在真实机器人部署中展现出平滑的指令间过渡。

**5. 动作表示：从纯关节目标到动力学感知增强动作**

SENTINEL的动作专家不仅预测关节目标，还输出**增强动作块**，包含下一时刻的根速度、角速度及关节位置预测：

$$\tilde{a}_t = [a_t, v_{t+1}^{\mathrm{root}}, \omega_{t+1}^{\mathrm{root}}, q_{t+1}]$$

这种动力学感知设计为模型提供了关于动作物理后果的辅助监督信号。消融实验表明，去除状态预测后成功率从99.45%降至98.67%（Table 3），证实了动力学预测对动作稳定性的贡献。

综上，SENTINEL通过上述五项关键创新，实现了从模块化生成-跟踪范式到端到端语言-动作范式的跨越。其核心洞察在于：**在物理仿真中收集大规模语言-动作轨迹，并利用流匹配直接学习从语言和机器人状态到动作的映射，可以获得比模块化方法更强的语义-物理一致性和更高的执行成功率**——在主实验中成功率高达99.45%，显著优于最高基线MDM+Retarget的94.94%（Table 2）。

## 整体框架

SENTINEL 是一套完全端到端的语言-动作模型，用于人形机器人的全身控制。其核心设计理念是消除传统模块化流水线中必须存在的中间运动表示（如人体动捕序列或隐式运动潜变量），直接将自然语言命令和机器人本体感受历史映射到底层关节动作。这一范式转换的关键动机在于：模块化方法（如 MDM+Retarget）在“文本→人体运动→全身控制器跟踪”的串联过程中，语言语义与物理执行之间缺乏紧密的梯度耦合，导致生成的语义相似运动在物理仿真中不可行（例如执行“jumps up in a tight twirl.”时因大角度旋转而失去平衡摔倒）。

整个框架由三个顺序阶段构成，如 Figure 1 所示：

![[assets/figures/papers/paper_list_l1016_https_arxiv_org_abs_2511_19236/figures/001_Figure_1.jpg]]
*Figure 1: Overview of SENTINEL. Our framework consists of three stages. (1) We construct a languageaction dataset by using a whole body controller to track human motion data paired with natural language descriptions. (2) We train an end-to-end language–action model with flow matching action head, which predicts a robot action chunk conditioned on both the proprioceptive state history and the language command. (3) A post-training stage with a residual action head is introduced to enhance its performance*

**阶段一：物理交互数据集的构建。** 利用一个预训练的 Mixture-of-Expert 全身控制器，在物理仿真中跟踪大规模人体运动数据（AMASS），同时施加域随机化，生成大量“语言命令-机器人关节动作轨迹”的配对数据。每条轨迹包含自然语言描述、本体感受状态序列以及对应的底层关节目标，为端到端模型提供了物理上可行的监督信号。

**阶段二：语言-动作流匹配模型训练。** 核心模型是一个基于 Transformer 的端到端架构，由三个关键模块组成：
- **语言-状态编码器**：融合 CLIP 编码的语言标记与多尺度状态历史（50 Hz 短期状态 + 4 Hz 长期状态），产生统一的上下文表示 $c_t = [l, \mathbf{s}_t^{\mathrm{hist}}]$。
- **流匹配动作专家**：以流匹配（flow matching）方式预测未来 $H$ 步的动作块，同时包含增强的动力学预测——下一时刻的根速度、角速度及关节位置 $\tilde{a}_t = [a_t, v_{t+1}^{\mathrm{root}}, \omega_{t+1}^{\mathrm{root}}, q_{t+1}]$，使模型隐式学习环境动力学。
- **完成预测头**：一个两层 MLP，预测任务是否将在未来 $H$ 步内完成，用于主动终止当前命令，避免固定时长的僵硬执行。

训练目标为流匹配损失与完成预测损失的加权和 $\mathcal{L} = \mathcal{L}_{\mathrm{fm}} + \lambda \mathcal{L}_{\mathrm{done}}$（$\lambda=0.01$），其中流匹配损失最小化预测速度场与目标速度场 $u = \epsilon - \mathbf{A}_t$ 的距离。推理时通过分类器自由引导（classifier-free guidance）增强语言对齐，引导权重 $w=2.0$ 时在语义一致性和物理成功率之间取得最佳平衡。

**阶段三：残差强化学习后训练。** 在预训练模型基础上，引入一个轻量的三层 MLP 残差动作头 $\Delta a_t = \pi_\Delta(s_t, \tilde{a}_t)$，通过 PPO 在域随机化下训练。该阶段的核心奖励项包括关节跟踪精度和残差动作范数惩罚（见 Table 1），旨在修正开环执行中的累积漂移，同时保持语义对齐。消融实验表明，移除主动终止奖励会使语义跟随指标 R@1 从 0.392 剧降至 0.255，验证了该机制对语言理解的关键作用。

**视觉-语言扩展。** 为支持导航任务，SENTINEL 集成了 RGB-D 相机与 FoundationPose 位姿估计模块（Figure 2）。机载 D435 相机捕获前视 RGB-D 图像，经 FoundationPose 估计目标在机器人自坐标系下的位姿，随后将估计的路径点插入自然语言命令模板，与本体感受状态一同输入 SENTINEL，形成闭环的“感知-语言-动作”控制回路。

整个框架的输入输出流可以概括为：**语言命令 + 多尺度状态历史 → 语言-状态编码器 → 上下文表示 → 流匹配动作专家（+ 完成预测头）→ 动作块 + 残差修正 → 底层关节目标**。这一设计消除了中间运动表示，使梯度信号能够从物理执行结果直接反馈到语言理解，从而实现了比模块化生成-跟踪范式更强的语义-物理一致性。

## 核心模块与公式推导

SENTINEL 的核心架构由三个紧密协作的模块构成：**语言-状态编码器**、**流匹配动作专家**与**完成预测头**，辅以多尺度观察机制和残差后训练策略。

### 3.1 本体感受状态与上下文表示

机器人时刻 $t$ 的本体感受状态定义为：

$$s_t = [v_t^{\mathrm{root}}, \omega_t^{\mathrm{root}}, g_t, q_t, \dot{q}_t, a_{t-1}] \tag{1}$$

其中 $v_t^{\mathrm{root}}$ 为根线速度，$\omega_t^{\mathrm{root}}$ 为根角速度，$g_t$ 为投影重力向量，$q_t$ 与 $\dot{q}_t$ 分别为关节位置和速度，$a_{t-1}$ 为上一时刻的动作。该状态向量构成了模型理解机器人当前动力学状态的基础。

语言-状态编码器将自然语言命令 $l$ 与多尺度状态历史融合为统一的上下文表示：

$$c_t = [l, \mathbf{s}_t^{\mathrm{hist}}] \tag{2}$$

语言命令通过 CLIP 文本编码器提取语义特征，而状态历史则采用双尺度设计：

$$\mathbf{s}_t^{\mathrm{hist}} = [\mathbf{s}_t^{\mathrm{long\_term}}, \mathbf{s}_t^{\mathrm{short\_term}}] \tag{5}$$

其中 $\mathbf{s}_t^{\mathrm{short\_term}}$ 以 50Hz 频率采样最近 10 步的精细状态，$\mathbf{s}_t^{\mathrm{long\_term}}$ 以 4Hz 频率覆盖过去 10 秒的粗粒度状态。这种多尺度设计使模型既能感知瞬时动力学变化，又能理解长时间跨度的运动上下文——消融实验表明，移除长期观察会导致 R@1 从 0.582 骤降至 0.153（Table 3），证明其对语义理解的关键作用。

### 3.2 流匹配动作专家

动作专家基于 Transformer 解码器架构，以流匹配方式预测未来 $H$ 步的动作块。其核心思想是将动作生成建模为从简单先验分布到目标动作分布的概率流变换。

**训练目标**：流匹配训练最小化预测速度场 $v_\theta$ 与目标速度场之间的 $L_2$ 距离：

$$\mathcal{L}(\theta) = \mathbb{E}_{p(\mathbf{A}_t|c_t), q(\mathbf{A}_t^\tau|\mathbf{A}_t)} \left\| v_\theta(\mathbf{A}_t^\tau, \tau, c_t) - u(\mathbf{A}_t^\tau|\mathbf{A}_t) \right\|^2 \tag{3}$$

其中 $\mathbf{A}_t$ 为目标动作块，$\mathbf{A}_t^\tau$ 为扩散时间 $\tau$ 处的噪声化动作，目标速度场定义为 $u = \epsilon - \mathbf{A}_t$（$\epsilon$ 为标准高斯噪声）。模型学习从噪声样本指向目标分布的向量场。

**推断过程**：通过离散时间步对预测速度场进行积分，从纯噪声 $\mathbf{A}_t^1 \sim \mathcal{N}(0, I)$ 逐步去噪得到动作块：

$$\mathbf{A}_t^{\tau-\Delta t} = \mathbf{A}_t^{\tau} - v_\theta(\mathbf{A}_t^\tau, \tau, c_t) \cdot \Delta t \tag{4}$$

**增强动作预测**：动作专家不仅预测关节目标位置，还同时输出下一时刻的动力学状态，形成增强动作块：

$$\tilde{a}_t = [a_t, v_{t+1}^{\mathrm{root}}, \omega_{t+1}^{\mathrm{root}}, q_{t+1}] \tag{6}$$

这种动力学感知预测为模型提供了辅助的自我监督信号——消融显示，移除状态预测导致成功率从 99.45% 降至 98.67%（Table 3），说明预测未来状态有助于动作的物理一致性。

**分类器自由引导**：为增强语言对齐，推断时采用引导采样：

$$v_{\mathrm{cfg}} = v_{\mathrm{uncond}} + w (v_{\mathrm{cond}} - v_{\mathrm{uncond}}) \tag{16}$$

其中 $v_{\mathrm{cond}}$ 为条件速度预测，$v_{\mathrm{uncond}}$ 为无条件预测，$w$ 为引导权重。实验表明 $w=2.0$ 时在语义对齐（R@1）和物理成功率之间取得最佳平衡（Figure 7）。

### 3.3 完成预测头

完成预测头是一个两层 MLP，基于上下文表示 $c_t$ 预测当前任务是否将在未来 $H$ 步内完成。训练时将其与流匹配损失联合优化：

$$\mathcal{L} = \mathcal{L}_{\mathrm{fm}} + \lambda \mathcal{L}_{\mathrm{done}} \tag{13}$$

其中 $\lambda=0.01$ 为权重系数。该模块使机器人能够主动判断指令执行完毕并切换至下一任务，而非依赖固定时长或超时机制。

### 3.4 残差后训练

为增强 sim-to-real 迁移能力并修正开环执行中的累积漂移，SENTINEL 引入轻量残差动作头 $\pi_\Delta$（三层 MLP），通过 PPO 在域随机化下训练：

$$\Delta a_t = \pi_\Delta(s_t, \tilde{a}_t) \tag{7}$$

残差头以当前状态 $s_t$ 和预训练模型的预测动作 $\tilde{a}_t$ 为输入，输出修正量 $\Delta a_t$。后训练奖励包括关节跟踪精度、残差动作范数惩罚、主动终止奖励等（Table 1）。实验表明，Base+$\pi_\Delta$ 将 sim-to-real 成功率从 95.44% 提升至 99.11%（Table 5），且移除主动终止奖励会导致 R@1 从 0.392 降至 0.255（Table 10），验证了各奖励项的必要性。

### 补充图表

![[assets/figures/papers/paper_list_l1016_https_arxiv_org_abs_2511_19236/figures/003_Figure_2.jpg]]
*Figure 2: Integration of visual perception into SENTINEL for navigation tasks. The onboard D435 camera captures front-view RGB-D images, which are processed by FoundationPose [60] to estimate the target position in the robot’s egocentric frame. The estimated waypoint is then inserted into natural-language command templates and provided to SENTINEL, together with the robot’s proprioceptive state, to generate whole body control actions. This closed-loop process enables the robot to iteratively approach the visual target*

## 实验与分析

### 文本全身控制主实验

SENTINEL在基于HumanML3D测试集与AMASS动作数据的文本全身控制任务上，与四种模块化基线进行了全面对比。所有基线均采用相同的Unitree G1全身控制跟踪策略进行运动执行或策略蒸馏，以消除控制器差异带来的不公平比较。

**Table 2**报告了核心结果。在物理执行成功率上，SENTINEL达到**99.45%**，显著优于最强基线MDM+Retarget的94.94%（+4.51个百分点）。在语义对齐方面，SENTINEL的MM-Dist降至**0.487**，优于T2M-GPT+Retarget的0.577；R@1达到**0.582**，显著超过T2M-GPT+Retarget的0.481（+0.101）。MMD指标上，SENTINEL的3.438同样优于所有基线（T2M-GPT+Retarget为4.115）。这些结果表明，端到端范式在语义-物理一致性和执行可靠性两个维度上均实现了对模块化管线的系统性超越。

**Figure 3**提供了定性证据。在执行“jumps up in a tight twirl.”指令时，MDM+Retarget因中间运动表示缺乏物理约束，生成的动作导致机器人在大角度旋转中失去平衡并摔倒；而SENTINEL直接生成物理可行的关节动作，稳健完成整个旋转跳跃序列。这直观展示了消除中间运动表示后，梯度信号从物理执行反馈到语言理解的端到端流动所带来的跨模态一致性增益。

### 消融实验

**Table 3**系统拆解了模型设计的关键组件。

**多尺度观察的消融**揭示了最剧烈的性能退化。移除长期观察（仅保留0.2秒短时历史）后，R@1从0.582剧降至**0.153**，MMD从3.438飙升至**72.468**。这一现象表明，长时间跨度的状态历史对于理解复杂语言命令的时序语义是不可或缺的——仅靠瞬时本体感受无法建立“行走后转圈”这类时序依赖关系。

**状态预测的消融**中，移除动力学感知预测（即增强动作块中的未来根速度、角速度、关节位置预测）导致成功率从99.45%降至**98.67%**。虽然降幅相对温和，但印证了辅助的动力学预测为动作生成提供了有益的正则化信号。

**动作块大小与rollout步数**在**Figure 4**中进行了系统扫描。更长的动作块（H=50 vs H=5）训练带来更好的MMD和成功率，表明更大的预测范围有助于模型学习时序连贯的运动模式。在推理阶段，K=5被确定为最优rollout步数，在计算开销与动作质量之间取得平衡。

**模型规模**的影响在**Table 4**中量化。600M参数的大模型相比60M的小模型，R@1从0.099跃升至0.582，提升近6倍。这一结果强烈暗示，语言到物理动作的端到端映射需要充分的模型容量来同时编码语义理解和动力学知识。

### 残差后训练与Sim-to-Real迁移

**Table 5**展示了残差后训练的关键作用。基础预训练模型在域随机化环境中的sim-to-real成功率为95.44%，而经过PPO训练的残差动作头将其提升至**99.11%**。更重要的是，**Table 10**的消融表明，移除主动终止（Active Termination）奖励后，R@1从0.392降至**0.255**，语言跟随能力大幅退化。这说明残差后训练不仅修正了开环漂移，其奖励设计中的任务完成信号对维持语义对齐同样至关重要。

分类器自由引导权重w的调优结果见**Figure 7**。w=2.0时在语义对齐（R@1）和物理成功率之间取得最佳平衡，过高的引导强度虽提升语义匹配但会损害动作可行性。

![[assets/figures/papers/paper_list_l1016_https_arxiv_org_abs_2511_19236/figures/015_Figure_7.jpg]]
*Figure 7: Effect of classifier-free guidance weight w*

### 视觉-语言闭环导航

**Figure 2**展示了视觉感知的集成方案：机载D435相机捕获RGB-D图像，FoundationPose估计目标在机器人自我中心坐标系下的位姿，估计的路径点被插入自然语言命令模板后送入SENTINEL。**Figure 5**记录了导航过程中机器人位置的可视化，平均距离从5.06米逐步减小至2.85米（第一轮）和1.99米（第二轮），验证了闭环控制的有效性。

### 真实机器人部署

**Figure 6**展示了SENTINEL在Unitree G1实体机器人上的文本全身控制部署示例。**Figure 8**进一步验证了连续指令的自主顺序执行能力——机器人平滑地从“a man walks forward”过渡到“a man is waving his right hand”，展示了完成预测模块在主动终止和任务切换中的作用。

### 推理效率

**Table 11**报告了不同流匹配步数下的推理耗时。在NVIDIA GeForce RTX 4090 GPU上，模型可实现满足实时控制需求的推理速度，具体数值需参考原表。

### 补充图表

![[assets/figures/papers/paper_list_l1016_https_arxiv_org_abs_2511_19236/figures/004_Table_2.jpg]]
*Table 2: Text-based whole body control evaluation results. Our method outperforms all baselines in both generation quality and physical execution success. → means the closer to Ground Truth the better*

![[assets/figures/papers/paper_list_l1016_https_arxiv_org_abs_2511_19236/figures/005_Figure_3.jpg]]
*Figure 3: Comparison between MDM + Retarget [7] and our method on an example text prompt: “jumps up in a tight twirl.”*

![[assets/figures/papers/paper_list_l1016_https_arxiv_org_abs_2511_19236/figures/007_Table_3.jpg]]
*Table 3: Ablation study results for model design*

![[assets/figures/papers/paper_list_l1016_https_arxiv_org_abs_2511_19236/figures/006_Figure_4.jpg]]
*Figure 4: Results for different action chunk sizes H (training) and rollout steps K (inference)*

![[assets/figures/papers/paper_list_l1016_https_arxiv_org_abs_2511_19236/figures/008_Table_4.jpg]]
*Table 4: Results for different model sizes*

![[assets/figures/papers/paper_list_l1016_https_arxiv_org_abs_2511_19236/figures/009_Table_5.jpg]]
*Table 5: Results for residual post-training*

![[assets/figures/papers/paper_list_l1016_https_arxiv_org_abs_2511_19236/figures/017_Table_10.jpg]]
*Table 10: Ablation study results for residual posttraining*

![[assets/figures/papers/paper_list_l1016_https_arxiv_org_abs_2511_19236/figures/002_Table_1.jpg]]
*Table 1: Main reward terms for residual post-training*

![[assets/figures/papers/paper_list_l1016_https_arxiv_org_abs_2511_19236/figures/011_Figure_6.jpg]]
*Figure 6: Real world deployment of our method on a Unitree G1 for text-based whole body control*

## 方法谱系与知识库定位

### 端到端语言-动作范式的确立

SENTINEL 在文本驱动人形机器人全身控制领域明确划分了“模块化流水线”与“端到端模型”两条技术路线。此前的主流范式遵循“文本→中间运动表示→全身控制器”的级联架构：**MDM**（扩散式人体运动生成模型）与 **T2M-GPT**（GPT风格的文本到动捕生成）负责从语言合成人体运动序列，随后通过 Unitree G1 的 Mixture-of-Expert 全身控制器进行运动跟踪执行。这种解耦设计虽然允许各模块独立优化，却引入了一个关键瓶颈——语言命令与物理动作之间缺乏直接的梯度通路，导致语义上相似的运动在物理执行中可能不可行。Figure 3 的定性对比直观地暴露了这一缺陷：当执行“jumps up in a tight twirl.”时，MDM+Retarget 因大角度旋转失去平衡而摔倒，而 SENTINEL 直接生成物理可行的动作，稳健完成指令。

SENTINEL 的贡献在于彻底移除了中间运动表示层，构建了首个完全端到端的语言-动作模型。其核心机制是将语言指令与本体感受历史直接映射到底层关节动作，使梯度信号能够从物理执行结果反向传播至语言理解模块，从而实现跨模态的紧密对齐。这一设计选择在对比实验中得到了充分验证：在 HumanML3D 测试集上，SENTINEL 的成功率达到 99.45%，显著优于最强基线 MDM+Retarget 的 94.94%（Table 2），同时在语义对齐指标 R@1 上取得 0.582，优于 T2M-GPT+Retarget 的 0.481。

### 与基线方法的关键差异

与 SENTINEL 形成直接对比的基线方法包括两类：一类是“生成-跟踪”模块化方案（MDM+Retarget、T2M-GPT+Retarget），另一类是同样直接从文本生成机器人动作的端到端方案（**UH-1** 和 **LangWBC**）。后者虽然也试图跳过中间运动表示，但在架构设计上与 SENTINEL 存在本质差异，这些差异恰好构成了 SENTINEL 性能优势的技术解释：

**观察范围。** LangWBC 仅使用约 2 秒的短时本体感受历史，而 SENTINEL 引入了多尺度状态历史——同时维护 50Hz 高频短期状态（10步）和 4Hz 低频长期状态（覆盖 10 秒窗口）。消融实验（Table 3）表明，移除长期观察后，R@1 从 0.582 剧降至 0.153，MMD 从 3.438 飙升至 72.468，这证明长时程状态上下文对于理解“walk forward then turn left”这类跨时间段的复合指令至关重要。

**动作生成机制。** LangWBC 采用基于 CVAE 和 DAgger 的 MLP 架构，而 SENTINEL 使用基于流匹配（flow matching）的 Transformer 动作专家。流匹配通过直接建模从简单分布到目标动作分布的连续速度场，避免了扩散模型的多步去噪开销，同时保留了生成多样性。动作专家还预测增强动作块，包含未来根速度、角速度和关节位置，形成隐式的动力学预测辅助任务。消融实验显示，移除状态预测后成功率从 99.45% 降至 98.67%，验证了动力学感知设计对动作稳定性的贡献。

**训练策略。** SENTINEL 采用两阶段训练：首先在大规模语言-动作轨迹数据集上进行流匹配预训练，随后通过 PPO 强化学习进行残差后训练。残差动作头是一个轻量三层 MLP，仅对预训练模型的输出施加修正，在域随机化环境下优化跟踪精度和动作平滑性。Table 5 显示，残差后训练将 sim-to-real 迁移成功率从 95.44% 提升至 99.11%，同时保持了语义对齐性能。这一策略与 LangWBC 的单阶段 DAgger 训练形成对比，体现了“先学语义-物理映射，再精调执行鲁棒性”的分解优势。

**主动终止机制。** SENTINEL 配备了基于 done 概率预测的主动任务终止模块，使机器人能够在完成任务后自主停止当前命令并准备接收下一条指令，实现平滑的指令间过渡（Figure 8）。基线方法通常依赖固定时长或超时终止，缺乏对任务完成状态的显式建模。

### 模型规模与推理效率的权衡

SENTINEL 的性能与模型规模呈强正相关。Table 4 显示，600M 参数模型的 R@1 为 0.582，而 60M 小模型的 R@1 仅为 0.099，表明语言-动作映射中的语义理解需要足够的模型容量。这一发现与当前大语言模型领域的 scaling law 趋势一致，但在具身控制领域尚属少见的实证证据。

在推理效率方面，SENTINEL 在 NVIDIA GeForce RTX 4090 上的推理耗时随流匹配步数增加而线性增长（Table 11），但通过调整步数可在生成质量和实时性之间取得折中。分类器自由引导权重 w=2.0 被确定为语义对齐与成功率之间的最佳平衡点（Figure 7）。

### 适用边界与局限

SENTINEL 的端到端设计在带来语义-物理一致性的同时，也引入了若干适用边界：

**数据依赖性。** 模型的预训练依赖于物理仿真中收集的大规模语言-动作轨迹数据集。这些数据通过预训练的全身控制器跟踪人体运动生成，因此数据质量受限于控制器本身的跟踪能力和仿真到现实的域差距。虽然域随机化和残差后训练缓解了这一问题，但训练数据的覆盖范围仍决定了模型可执行动作的上限。

**视觉-语言扩展的间接性。** SENTINEL 的视觉感知能力通过将 FoundationPose 估计的位姿转换为语言命令模板来实现（Figure 2），而非直接端到端地处理视觉输入。这种设计保持了语言-动作主干的纯净性，但也意味着视觉感知的错误会传播到下游控制，且模型无法学习视觉-动作之间的直接映射。在导航实验中，平均距离从 5.06m 降至 1.99m 需要两轮迭代（Figure 5），表明闭环效率仍有提升空间。

**长时程任务的累积漂移。** 虽然多尺度观察和动力学预测缓解了开环漂移，但在极长时程的连续执行中，累积误差仍可能导致动作偏离语义意图。残差后训练的奖励设计（Table 1）主要关注单步跟踪精度和动作平滑性，缺乏对全局语义一致性的显式约束。

### 开放问题

1. **多模态感知的端到端融合。** 当前 SENTINEL 将视觉信息转换为语言命令的做法虽然有效，但割裂了视觉-动作的直接学习通路。如何将 RGB-D 或点云输入直接融入流匹配动作专家，同时保持训练稳定性和 sim-to-real 迁移能力，是一个值得探索的方向。

2. **开放词汇的动作泛化。** SENTINEL 在 HumanML3D 测试集上展现了强语义对齐能力，但该数据集的文本描述覆盖范围有限。模型能否泛化到训练中未见过的动作描述（如“像企鹅一样走路”）仍需验证，这可能需要在数据构建阶段引入更丰富的语言多样性或利用大语言模型进行文本增强。

3. **多机器人平台的迁移。** 当前实验均在 Unitree G1 平台上进行。端到端语言-动作模型能否通过少量微调迁移到具有不同运动学结构的人形机器人（如 Tesla Optimus、Figure 02），以及模型规模与迁移效率之间的关系，是具身基础模型方向的核心问题。

4. **安全性与可解释性。** 端到端黑盒模型在物理世界中执行动作时，缺乏可审计的中间表示。如何在保持端到端优势的同时，引入可解释的动作表征或安全约束机制，是人形机器人实际部署中不可回避的挑战。

## 原文 PDF

![[paperPDFs/CVPR_2026/End_to_End_Language_Action_Model_for_Humanoid_Whole_Body_Control.pdf]]