---
title: "Diffuse-CLoC: Guided Diffusion for Physics-based Character Look-ahead Control"
type: paper
paper_level: A
venue: SIGGRAPH
year: 2025
pdf_ref: paperPDFs/SIGGRAPH_2025/Diffuse_CLoC_Guided_Diffusion_for_Physics_based_Character_Look_ahead_Control.pdf
project_link: "https://s2025.conference-schedule.org/presentation/?id=papers_1047&sess=sess156"
code_link: null
aliases:
- DC
- Diffuse-CLoC
tags:
- SIGGRAPH_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 共同扩散（co-diffusion）状态与动作的联合分布，通过预测的状态为动作生成提供条件，从而允许在状态空间施加分类器引导（classifier guidance），使运动学引导信号能够影响动作输出，实现可引导的物理控制。
primary_logic: 在单一扩散模型中对状态和动作的联合分布进行建模，使得动作生成可以通过对预测状态的条件化而变得可引导，从而能够迁移运动学生成中的成熟引导技术（如分类器引导和修复）到基于物理的角色控制中。
claims:
- 对状态和动作的联合分布进行建模，使得动作生成可以通过预测的状态进行条件化引导。
- 共同扩散状态和动作使得运动学引导能够有效条件化动作生成，以完成复杂任务。
- 定制的注意力掩码（非因果注意力用于状态，因果注意力用于动作）使未来状态的引导信息能够传播到当前动作。
- Walk+Perturb 上 FID = 0.074
---

# Diffuse-CLoC: Guided Diffusion for Physics-based Character Look-ahead Control

> [!tip] 核心洞察
> 在单一扩散模型中对状态和动作的联合分布进行建模，使得动作生成可以通过对预测状态的条件化而变得可引导，从而能够迁移运动学生成中的成熟引导技术（如分类器引导和修复）到基于物理的角色控制中。

| 字段 | 内容 |
|------|------|
| 中文题名 | Diffuse-CLoC：基于物理的角色前瞻控制引导扩散框架 |
| 英文题名 | Diffuse-CLoC: Guided Diffusion for Physics-based Character Look-ahead Control |
| 会议/期刊 | SIGGRAPH 2025 |
| Links | [paper](http://arxiv.org/abs/2503.11801v3) · [arXiv](https://arxiv.org/abs/2503.11801v3) · [Project](https://s2025.conference-schedule.org/presentation/?id=papers_1047&sess=sess156) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | Diffuse-CLoC |
| Dataset | Walk+Perturb, Forest, Jump, Motion In-betweening |

> [!tip] 效果简介
> - Walk+Perturb 上，FID 0.074 vs Kin+PHC (MDM+PHC) (显著更低（更好）)；% Fall 16% vs Kin+PHC (MDM+PHC) (显著更低)。
> - Forest 上，% Success 96% vs Kin+PHC (MDM+PHC) (显著更高)。
> - Jump 上，% Success 71% vs Kin+PHC (MDM+PHC) (显著更高)。

## 概要

现有基于扩散模型的物理角色控制方法存在根本性瓶颈：运动学扩散模型（如MDM）虽能生成多样运动，却无法保证物理可行性；而纯动作扩散策略（如Diffusion Policy）因缺乏状态预测能力，不能在推理时利用直观的状态空间引导进行控制，导致模型无法零样本迁移到未见的下游任务。

**Diffuse-CLoC** 的核心洞见在于，在单一扩散模型中对状态和动作的联合分布进行建模，使动作生成可通过预测的状态进行条件化，从而将运动学生成中成熟的引导技术（分类器引导与修复）迁移到基于物理的角色控制中。具体而言，该方法采用基于Transformer解码器的共同扩散架构，并设计了定制注意力掩码——动作为因果注意力（仅关注过去），状态为非因果注意力（可关注未来状态）——使未来状态的引导信息能反向传播到当前动作决策。配合基于FIFO缓冲区的滚动推理方案，模型在保持运动一致性的同时加速了自回归执行。

实验表明，Diffuse-CLoC在多项零样本物理任务上显著优于层次化基线Kin+PHC（MDM+PHC）：森林避障成功率96%（基线未报告可比数值），跳跃任务成功率71%，行走扰动场景的FID降至0.074且摔倒率仅16%。消融实验证实，1秒预测视界、定制注意力掩码和状态滚动推理是性能的关键保障。

本方法定位为基于联合分布扩散的物理角色控制框架，区别于分别建模规划与跟踪的因子化方法，以及仅建模动作的免模型方法，为可引导的物理运动生成提供了新范式。

## 核心方法与创新机理

### 瓶颈与核心洞察

现有基于扩散的物理角色控制方法面临一个根本性瓶颈：运动学扩散模型（如MDM）虽能生成高质量运动，但缺乏物理可行性保证，需依赖独立的跟踪控制器（如PHC）将运动学规划转化为物理动作；而纯动作扩散策略（如Diffusion Policy）虽直接输出物理动作，却因不建模状态预测而无法在推理时利用直观的状态空间引导。**Diffuse-CLoC** 的核心洞察在于：**在单一扩散模型中对状态和动作的联合分布进行建模，使动作生成可以通过对预测状态的条件化而变得可引导**，从而将运动学生成中成熟的分类器引导和修复技术迁移到基于物理的角色控制中。

这一设计的因果机制在于：共同扩散（co-diffusion）状态与动作的联合分布 $p(\tau) = p(s_t, a_t, s_{t+1}, a_{t+1}, \dots)$，使得扩散过程中预测的状态为动作生成提供条件信号。当在状态空间施加分类器引导时，引导梯度通过状态-动作的联合建模自然地传播到动作输出，实现“在状态空间引导，在动作空间执行”的统一范式。

### 关键设计变更

相较于层次化基线 **Kin+PHC**（MDM运动学规划 + PHC通用跟踪控制器），Diffuse-CLoC 在以下三个核心维度上进行了根本性重构：

1. **分布建模：从分解式到联合式。** 基线方法分别建模运动学规划分布 $p(s)$ 和跟踪控制分布 $p(a|s)$，两者在推理时串联但本质解耦。Diffuse-CLoC 在单个Transformer扩散模型中直接建模 $p(s, a)$ 的联合分布，使状态预测和动作生成共享同一表示空间，为引导信号的端到端传播奠定基础。

2. **引导机制：从运动学空间引导到状态空间引导。** 基线方法只能在运动学规划阶段施加引导（如MDM的分类器引导），随后由跟踪策略被动执行。Diffuse-CLoC 允许在扩散过程中直接对状态空间施加分类器引导，通过可微成本函数 $G_\tau(\tau)$ 的梯度 $\nabla_\tau G_\tau(\tau)$ 条件化动作生成，实现零样本（zero-shot）任务迁移。

3. **注意力模式：定制化状态-动作注意力掩码。** 这是实现状态引导信号有效传播的关键架构设计。Diffuse-CLoC 采用解码器型Transformer，对状态和动作token施加差异化的注意力掩码：
   - **动作使用因果注意力**：动作token仅关注过去的状态和动作，保证自回归执行时的因果一致性。
   - **状态使用非因果注意力**：状态token可关注未来的状态（但不可关注动作），使未来状态的引导信息能够通过状态端的反向传播影响当前动作生成。

   这一设计解决了联合分布建模中的一个关键矛盾：动作生成需要因果性以保证物理可行性，而状态引导需要非因果性以利用前瞻信息进行规划。

### 框架与推理流程

Diffuse-CLoC 的完整推理流程（Fig. 3）由三个协同模块构成：

![[assets/figures/papers/paper_list_l6_http_arxiv_org_abs_2503_11801v3/figures/003_Figure_3.jpg]]
*Figure 3: Framework of Diffuse-CLoC. The rolling scheme (Left) is implemented as a FIFO buffer, where at every timestep ??, a state and action pair of pure noise is pushed into the denoiser, while the earliest clean pair is popped out and used to step the simulator. The denoiser architecture (Middle) denoises the buffer of states and actions with an increasing noise level along the trajectory. The observation*

**滚动推理方案（Rolling Scheme）。** 受Zhang et al. (2024)启发，采用FIFO缓冲区实现自回归执行中的运动一致性。在每个时间步 $t$，将一对纯噪声的状态-动作token推入去噪器，同时弹出最早的一对干净token用于驱动物理模拟器。这一方案重用前次扩散结果作为热启动（warmup），在减少扩散步数的同时保持运动平滑性。

**共同扩散去噪器。** 基于解码器型Transformer架构，接收带噪的轨迹token序列 $[a_t^k, s_{t+1}^k, a_{t+1}^k, \dots, s_{t+H}^k, a_{t+H}^k]$ 和观测 $O_t$，预测干净的轨迹 $\hat{\tau}_t$。训练目标为预测干净轨迹与真实轨迹之间的均方误差：

$$\mathcal{L} = \text{MSE}\big(x_{0,\theta}(\tau_t^k, O_t, k), \tau_t\big)$$

其中 $x_{0,\theta}$ 为去噪器预测的干净轨迹，$\tau_t^k$ 为噪声水平 $k$ 下的轨迹。

**分类器引导。** 在推理时，通过可微成本函数 $G_\tau(\tau)$ 的梯度引导去噪过程，使生成的动作满足下游任务约束。核心成本函数包括：
- **静态障碍物避让**：$G_{\tau}^{\text{obs}}(\tau) = \sum_{j} \sum_{t'=t}^{t+H} \exp\big(-c \cdot \text{SDF}^{j}(s_{t'})\big)$，利用有符号距离函数惩罚轨迹穿透障碍物。
- **航点导航**：$G_{\tau}^{\text{wp}}(\tau) = \sum_{t'=t}^{t+H} \| P_{\text{root}}(s_{t'}) - g \|^2$，最小化角色根部位姿与目标的距离。
- **动态避障**：$G_{\tau,i}^{\text{sa}}(\tau) = \sum_{j\neq i} \sum_{t'=t}^{t+H} \exp\big(-c \cdot \|P_{\text{root}}(s_{t'}^i) - P_{\text{root}}(s_{t'}^j)\|^2\big)$，惩罚多角色间的过近距离。
- **运动内插**：通过将关键帧时刻的状态设置为干净数据（$s_t = \hat{s}_t, k_{st} = 0$），利用扩散模型的修复能力实现物理可行的运动内插。

### 关键公式与变量含义

扩散采样采用随机Langevin动力学步：

$$\tau_t^{k-1} = \alpha_k \big(\tau_t^k - \gamma_k \epsilon_\theta(\tau_t^k, O_t, k) + \mathcal{N}(0, \sigma_k^2 I)\big)$$

其中 $\tau_t^k$ 为噪声水平 $k$ 下的轨迹，$\epsilon_\theta$ 为去噪网络，$\alpha_k, \gamma_k, \sigma_k$ 为噪声调度参数，$O_t$ 为当前观测。分类器引导通过将 $\nabla_\tau G_\tau(\tau)$ 注入采样过程，实现任务特定的轨迹优化。

![[assets/figures/papers/paper_list_l6_http_arxiv_org_abs_2503_11801v3/figures/006_Figure_4.jpg]]
*Figure 4: Downstream Tasksf) a) Task is to touch the red ball with the character’s right hand via classifier guidance. The red ball is re-located when the character achieves the task. b) Root path following via classifier guidance. We can further refine styles by constraining parameters like base velocity and heading. c) Walk and jump over two consecutive obstacles. d) Run and jump over obstacles. e) Jumping on different platforms using penetration cost and waypoint to each platform. f ) A sequence of tasks in a single run, including route path following, platform jumping, and reaching a waypoint behind cylindrical barriers*

![[assets/figures/papers/paper_list_l6_http_arxiv_org_abs_2503_11801v3/figures/002_Figure_2.jpg]]
*Figure 2: Three Formulations in Physics-based Control using Diffusion. (a) The factored distribution approach separately learns planning ?? (?? ) and control CLoSD [Tevet 2024] Diffuse-CLoC (Ours) ?? (??|?? ), using kinematics planners [Karunratanakul et al. 2023; Tevet et al. 2023; Zhang et al. 2024] and tracking policies [Luo et al. 2023]. Examples of this Diffusion Policy [Chi 2023]Box Loco [Xie 2023]category are [Ajay et al. 2023; Tevet et al. 2024; Xie et al. 2023]. (b) The model-free approach learns ?? (??|?? ) only and does not allow inference-time planning Kinematics +Tracking[Chi et al. 2023; Huang et al. 2024a; Truong et al. 2024]. (c) The joint distribution approach models ?? (??, ??) dire...*

## 实验与关键发现

### 主结果：Diffuse-CLoC 在多项任务上全面超越 Kin+PHC 基线

**Table 1** 汇总了 Diffuse-CLoC 与 Kin+PHC（MDM + PHC 层次化基线）在五项下游任务上的定量对比。核心发现如下：

**运动质量与稳定性**：在 Walk+Perturb 任务上，Diffuse-CLoC 的 FID 降至 **0.074**，远优于 Kin+PHC；摔倒率从基线的高水平降至 **16%**。这表明共同扩散框架生成的物理动作不仅运动学上更自然，在外部扰动下的鲁棒性也显著更强。

**导航与避障**：在 Forest 森林避障任务上，Diffuse-CLoC 以 **96%** 的成功率大幅领先基线。该任务要求角色在密集柱状障碍物中穿行到达目标点，基线方法因运动学规划与物理执行分离，规划出的运动学轨迹可能物理不可行，导致跟踪失败。Diffuse-CLoC 通过在状态空间直接施加 SDF 障碍物成本（$G_{\tau}^{\mathrm{obs}}$），将避障信号端到端地注入动作生成，避免了规划-执行鸿沟。

**敏捷运动**：在 Jump 跳跃任务上，Diffuse-CLoC 取得 **71%** 成功率，同样显著优于基线。如 **Fig. 5** 所示，Kin+PHC 的运动学预测产生伪影，在敏捷动作中失败；而 Diffuse-CLoC 保持鲁棒并完成任务。这验证了联合分布建模在需要精确时序协调的敏捷任务上的关键优势。

**运动内插**：在 Motion In-betweening 任务上，Diffuse-CLoC 将摔倒率降至 **31%**，表明基于修复（inpainting）的状态空间引导同样适用于约束满足类任务。

### 关键消融：视界长度与注意力机制是性能瓶颈

**Table 2** 的系统消融揭示了几个因果性结论：

**预测视界的双刃剑效应**：将预测视界从 0.5 秒（16 步）延长到 **1 秒（32 步）** 是性能跃升的关键——森林任务成功率从较低水平跃升至 96%，跳跃任务达到 71%。然而，进一步延长至 2 秒（64 步）反而导致森林任务成功率下降，原因如 **Fig. 6** 所示：过长视界使策略对次优未来路径过度承诺（overcommit），在接近目标时与障碍物碰撞。这揭示了预测视界存在一个“甜区”——足够长以规划避障，但不能长到引入有害的未来偏差。

**定制注意力掩码的必要性**：将 Diffuse-CLoC 的定制注意力（状态非因果、动作因果）替换为全注意力（所有 token 互相可见），森林成功率骤降至 **58%**，跳跃降至 **53%**。这直接验证了：允许状态关注未来状态、同时阻止动作关注未来状态的设计，对于将未来引导信息反向传播到当前动作至关重要。全注意力破坏了这种信息流控制，使引导信号失效。

**滚动推理的贡献**：移除状态滚动推理（即每步从头扩散）导致跳跃成功率降至 **43%**，证明重用前次扩散结果作为热启动对运动一致性和任务成功有实质贡献。而动作滚动对性能影响极小，却能加速扩散过程 **25%**。

**与 Diffuser 的对比**：采用 Diffuser（Janner et al., 2022，一种先前的联合分布方法）在森林和跳跃任务上成功率均为 **0%**。这说明仅有联合分布建模不足以保证复杂任务的成功——Diffuse-CLoC 的定制注意力、滚动推理和分类器引导机制共同构成了性能的充分条件。

### 失败模式与适用边界

**历史依赖导致的响应滞后**：模型对历史观测的依赖使其偏向已见过的运动模式，部分角色在视频中对引导信号的响应不够灵敏。这在需要即时响应的任务（如突然避障）中可能成为瓶颈。

**复合误差与运动平滑性**：自回归执行中的复合误差仍然存在，运动平滑性有改进空间。这限制了极长序列（如 **Fig. 8** 的多任务组合）中的长期稳定性。

**任务覆盖边界**：当前方法未涉及人-物交互和接触丰富的动作（如搬运、推拉），扩展到这些领域需要进一步研究。所有验证任务均基于 AMASS 数据集的 54 个运动片段训练，泛化到训练分布外的运动风格尚待验证。

![[assets/figures/papers/paper_list_l6_http_arxiv_org_abs_2503_11801v3/figures/004_Table_1.jpg]]
*Table 1: Benchmark for Kinematic-tracking baselines v.s. Diffuse-CLoC across various tasks*

![[assets/figures/papers/paper_list_l6_http_arxiv_org_abs_2503_11801v3/figures/005_Table_2.jpg]]
*Table 2: Ablation study on horizon lengths, diffusion steps, attention styles, and rolling schemes. * marks the final model choice*

![[assets/figures/papers/paper_list_l6_http_arxiv_org_abs_2503_11801v3/figures/011_Table_3.jpg]]
*Table 3: Task Weights Table*

![[assets/figures/papers/paper_list_l6_http_arxiv_org_abs_2503_11801v3/figures/007_Figure_6.jpg]]
*Figure 6: Rollouts in the forest task for 0.5s prediction (Top), 1s prediction (Middle), and 2s prediction (Bottom). Starting at the triangle, the character aims to reach the goal marked by a star. The 0.5s policy circles within the forest and fails to reach the waypoint, while the 1s policy successfully navigates through the forest with diverse trajectories. In contrast, the 2s policy sometimes overcommits to suboptimal future paths and collides with obstacles near the goal*

![[assets/figures/papers/paper_list_l6_http_arxiv_org_abs_2503_11801v3/figures/008_Figure_5.jpg]]
*Figure 5: Rollouts in jump task for Kin+PHC (Left) vs. Diffuse-CLoC (Right). Kin+PHC suffers from artifacts in kinematics prediction and fails in agile motions, while Diffuse-CLoC remains robust and completes the task*

## 定位与知识库关联

### 与现有扩散控制范式的本质差异

Diffuse-CLoC 的核心定位落在扩散式物理角色控制的第三范式——**联合分布建模**，与两类既有路线形成根本区别：

**（a）因子化分布路线**（运动学规划 + 跟踪控制分离）：
- 代表工作：**MDM**（Tevet et al., ICLR 2023）作为运动学扩散规划器，**PHC**（Luo et al., ICCV 2023）作为通用跟踪控制器，二者串行组合为 Kin+PHC 基线。
- 本质瓶颈：运动学规划器生成的状态序列可能物理不可行，而跟踪控制器缺乏对规划过程的反馈通道，导致敏捷任务（如跳跃）中运动学伪影直接引发摔倒（Fig. 5）。引导信号只能作用于运动学空间，无法影响动作生成。

**（b）无模型动作扩散路线**（仅建模动作分布）：
- 代表工作：**Diffusion Policy**（Chi et al., 2023）、**Box Loco**（Xie et al., 2023）等。
- 本质瓶颈：模型仅学习 $p(a|s)$，推理时无法利用状态空间的直观引导（如“靠近目标点”），因为模型不预测未来状态，分类器引导缺乏可施加的状态表示。

**（c）联合分布路线**（本文）：
- 先前探索：**Diffuser**（Janner et al., 2022）首次在扩散模型中联合建模状态-动作，但在复杂角色控制任务上成功率为 0%（Table 2），说明仅有联合分布建模不足以完成任务。
- Diffuse-CLoC 的关键突破在于：通过**定制注意力掩码**（动作因果、状态非因果）和**共同扩散架构**，将联合分布建模从“能建模”推进到“可引导且物理可行”。这使得运动学引导（分类器梯度）能够通过预测的状态反向传播到动作生成，实现零样本任务迁移。

### 知识库挂载点

**扩散模型引导技术**：
- 继承自分类器引导（Dhariwal & Nichol, NeurIPS 2021）和运动学生成中的引导实践（Karunratanakul et al., 2023），但将其从运动学空间迁移到物理控制的状态空间。
- 成本函数设计（SDF 障碍物惩罚、航点距离、动态避障指数距离）借鉴了轨迹优化中的经典形式，但在扩散采样过程中以梯度引导方式注入。

**滚动推理与一致性**：
- FIFO 缓冲区的滚动方案受 **Zhang et al.（2024）** 启发，但 Diffuse-CLoC 将其适配到状态-动作联合扩散场景，并通过状态滚动（而非动作滚动）作为性能关键组件（消融实验：移除状态滚动使跳跃成功率降至 43%）。

**数据驱动物理角色控制**：
- 训练数据来自 AMASS 运动捕捉数据集（54 个运动片段，每段约 40 次物理仿真 rollout），延续了基于运动学数据训练物理策略的范式（如 PHC）。
- 架构上采用 decoder-only Transformer，与运动生成领域的扩散 Transformer 趋势一致。

### 适用边界

- **强项**：需要前瞻规划和状态空间引导的零样本任务，包括静态/动态避障、点对点导航、敏捷跳跃、运动内插。同一预训练模型无需微调即可泛化到这些任务。
- **边界**：模型对历史观测的依赖使其偏向已见过的运动模式，可能限制运动过渡的自然性和对引导信号的即时响应。当前工作未涉及人-物交互和接触丰富的动作（如搬运、推拉），这些场景需要额外的物理约束建模。
- **预测视界敏感**：1 秒视界（32 步）最优；0.5 秒视界规划不足导致失败，2 秒视界则过度承诺次优路径（Fig. 6）。这意味着方法在需要更长前瞻的任务上可能需要架构调整。

### 后续研究启发

- **引导形式的丰富化**：当前引导基于手工设计的成本函数梯度，未来可探索结合未来回报（return-conditioned guidance）或信任区域约束（trust region）来提升引导的稳定性和灵活性。
- **复合误差缓解**：自回归执行中的复合误差仍是开放问题，替代的数据增强策略（如扰动训练）或扩散步数动态调整可能进一步改善运动平滑度。
- **接触丰富任务的扩展**：将共同扩散框架扩展到物体操纵场景，需要在状态空间中引入物体状态和接触约束，这为联合分布建模提供了自然的扩展接口。
- **响应性提升**：减少对历史观测的依赖（如通过条件机制的解耦设计），可能提高对实时引导信号的响应速度，这对交互式应用（如游戏手柄控制）至关重要。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2025/Diffuse_CLoC_Guided_Diffusion_for_Physics_based_Character_Look_ahead_Control.pdf]]