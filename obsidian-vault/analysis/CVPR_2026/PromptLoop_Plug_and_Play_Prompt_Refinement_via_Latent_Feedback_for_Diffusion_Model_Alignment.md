---
title: "PromptLoop: Plug-and-Play Prompt Refinement via Latent Feedback for Diffusion Model Alignment"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/PromptLoop_Plug_and_Play_Prompt_Refinement_via_Latent_Feedback_for_Diffusion_Model_Alignment.pdf
project_link: null
code_link: "https://github.com/LAION-AI/LAION-SAFETY"
aliases:
- PromptLoop
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
- topic/representation_self_supervised_transfer
core_operator: 在去噪过程的每个时间步引入隐空间反馈，通过多模态大语言模型（MLLM）动态优化提示文本。
primary_logic: 将提示优化建模为闭环MDP，使MLLM策略在时间步上根据去噪隐空间状态迭代优化提示，从而在功能上等价于扩散模型RL，同时保留提示方法即插即用的灵活性、泛化性和组合性。
claims:
- PromptLoop在ImageReward等单一奖励和复合奖励上的表现均优于基线方法，且能与DDPO、ReFL等现有对齐方法正交组合，并缓解奖励破解和过优化。
- 消融实验证实，视觉反馈和多次提示优化是闭环MDP有效性的关键组件。
- 训练好的策略在未见过的扩散模型（包括flow-matching模型）上表现出强大的泛化能力。
- SDXL + ImageReward (single reward) 上 Image Reward = 1.0948
---

# PromptLoop: Plug-and-Play Prompt Refinement via Latent Feedback for Diffusion Model Alignment

> [!tip] 核心洞察
> 将提示优化建模为闭环MDP，使MLLM策略在时间步上根据去噪隐空间状态迭代优化提示，从而在功能上等价于扩散模型RL，同时保留提示方法即插即用的灵活性、泛化性和组合性。

| 字段 | 内容 |
|------|------|
| 中文题名 | PromptLoop：基于隐空间反馈的即插即用提示优化框架用于扩散模型对齐 |
| 英文题名 | PromptLoop: Plug-and-Play Prompt Refinement via Latent Feedback for Diffusion Model Alignment |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2510.00430) · [Code](https://github.com/LAION-AI/LAION-SAFETY) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video #topic/representation_self_supervised_transfer |
| Method | PromptLoop |
| Dataset | SDXL + ImageReward, SD1.5 + ImageReward, SDXL + Diffusion-DPO + PromptLoop, SDXL-turbo + RePrompt + PromptLoop |

> [!tip] 效果简介
> - SDXL + ImageReward (single reward) 上，Image Reward 1.0948 vs 0.7244 (+0.3704)。
> - SD1.5 + ImageReward (single reward) 上，Image Reward 0.6320 vs 0.0816 (+0.5504)。
> - SDXL + Diffusion-DPO + PromptLoop (orthogonality) 上，Image Reward 1.2898 vs 0.9921 (+0.2977)。

## 概要

扩散模型在文本到图像生成中取得了显著成功，但如何使生成结果与复杂的人类偏好对齐仍是一个核心挑战。现有对齐方法主要分为两类：一类是**参数级微调方法**（如 **DDPO** (Black et al., ICLR 2024)、**ReFL** (Xu et al., NeurIPS 2024)），直接对扩散模型权重进行强化学习优化，但存在泛化性差、易出现奖励破解（reward hacking）和过优化、且难以与现有方法组合等问题；另一类是**前馈式提示优化方法**（如 **RePrompt** (Wu et al., 2024)），通过优化输入提示文本来引导生成，虽保留了即插即用的灵活性，但因未能利用扩散过程的时序信息，导致对齐能力不足。

**PromptLoop** 针对上述瓶颈提出了一个新的解决思路：将提示优化建模为一个闭环马尔可夫决策过程（MDP），在去噪过程的每个时间步引入**隐空间反馈**（latent feedback），使多模态大语言模型（MLLM）策略能够根据中间隐空间状态动态优化提示文本。这一设计的核心洞察在于：通过在时间步上迭代优化提示，PromptLoop 在功能上等价于扩散模型 RL，同时完整保留了提示方法的即插即用特性、泛化能力和组合性。

实验结果表明，PromptLoop 在 ImageReward 等单一奖励和复合奖励场景下均显著优于现有基线方法。在 SDXL 上，ImageReward 从基线的 0.7244 提升至 1.0948；在 SD1.5 上，从 0.0816 提升至 0.6320。更重要的是，PromptLoop 可以与 **Diffusion-DPO** (Wallace et al., 2024) 等现有对齐方法正交组合，进一步将 ImageReward 提升至 1.2898，并有效缓解了奖励破解和过优化问题。训练好的策略在未见过的扩散模型（包括 flow-matching 模型如 FLUX.1-dev）上也展现出强大的零样本泛化能力。

在方法谱系上，PromptLoop 位于提示优化与强化学习的交叉点：它改变了四个关键设计槽位——对齐目标从直接微调模型参数转向动态优化提示文本（冻结扩散模型）、反馈机制从无反馈或仅终态反馈转向时间步感知的隐空间反馈、训练策略从监督学习转向在线 GRPO 强化学习、推理开销通过稀疏优化策略控制在 23% 以内。这一框架为扩散模型对齐提供了一条兼具有效性与灵活性的新路径。

扩散模型在文本到图像生成领域取得了显著进展，但其输出质量与人类偏好之间的对齐仍面临根本性挑战。用户提供的自然语言提示往往无法精确传达视觉意图，导致生成结果与人类期望之间存在系统性偏差。解决这一问题的现有路径可大致分为两类：**参数级对齐**与**提示级对齐**，两者各自存在难以调和的矛盾。

### 参数级对齐的困境：泛化性、组合性与奖励破解

以 **DDPO**（Black et al., ICLR 2024）为代表的参数级方法，通过强化学习直接微调扩散模型的权重，本质上将去噪过程建模为马尔可夫决策过程（MDP）。这类方法虽然能在特定奖励函数上取得显著的对齐效果，却面临三个核心瓶颈：

1. **泛化性差**：微调后的模型权重与训练时使用的奖励函数和提示分布高度耦合，难以迁移到未见过的奖励函数或扩散模型架构。
2. **组合性缺失**：参数级微调改变了模型的底层权重空间，使其难以与现有的其他对齐方法（如偏好优化、美学微调）正交组合。
3. **奖励破解与过优化**：直接优化模型参数容易导致模型利用奖励函数的漏洞生成高奖励但语义偏离的图像——即“奖励破解”（reward hacking），同时伴随图像多样性的急剧下降。

**ReFL**（Xu et al., NeurIPS 2024）等基于奖励加权回归的微调方法，以及 **Diffusion-DPO**（Wallace et al., 2024）等直接偏好优化方法，虽然在一定程度上缓解了训练不稳定性，但仍未突破参数级方法在泛化性和组合性上的根本局限。

### 提示级对齐的缺口：缺乏时序感知的反馈机制

提示级对齐方法通过优化输入提示文本来间接引导生成过程，天然具备即插即用的灵活性、跨模型泛化能力和与现有方法的组合性。然而，现有提示优化方法——如 **RePrompt**（Wu et al., 2024）——采用前馈式策略，仅在采样开始前或结束后对提示进行一次性优化。这种设计存在一个关键的功能性缺口：**未能利用扩散过程丰富的时序信息**。

扩散模型的去噪过程是一个逐步细化的动态过程：早期时间步决定图像的全局布局和氛围，后期时间步则填充纹理和细节。前馈式提示优化将整个生成过程视为黑箱，无法根据中间隐空间状态动态调整语义引导，导致对齐能力存在理论上限。

### 核心洞察：隐空间反馈建立功能等价性

本文的核心洞察在于揭示了一个结构性的对应关系：如果在去噪过程的每个时间步引入隐空间反馈，使多模态大语言模型（MLLM）能够根据当前噪声隐变量的去噪估计动态优化提示文本，那么这一闭环提示优化过程在功能上等价于扩散模型RL。具体而言：

- 扩散模型RL将去噪过程建模为MDP，动作空间是模型参数的梯度更新；
- PromptLoop同样将去噪过程建模为闭环MDP，但动作空间变为提示文本的语义优化。

两者共享相同的状态转移机制（扩散模型的去噪动力学），区别仅在于动作施加的层面——前者修改模型权重，后者修改条件输入。这一功能等价性意味着：**提示级方法在理论上具备与参数级方法同等的对齐潜力，同时保留了即插即用的工程优势**。

### 本文动机

基于上述分析，本文提出 **PromptLoop**——一个即插即用的提示优化框架，其设计目标是在三个维度上同时取得突破：

- **对齐能力**：通过隐空间反馈驱动的闭环MDP，实现与扩散模型RL功能等价的奖励优化效果；
- **泛化性与组合性**：冻结扩散模型权重，仅训练提示优化策略，使其能够泛化到未见过的扩散模型（包括flow-matching架构），并与现有对齐方法正交组合；
- **抗过优化能力**：隐空间反馈为策略模型提供了对生成过程的细粒度感知，有助于缓解奖励破解和语义漂移。

## 核心方法与创新机理

PromptLoop 的核心创新在于将扩散模型的对齐问题从**参数空间**迁移到**提示空间**，并通过**时间步感知的隐空间反馈闭环**，实现了功能上等价于扩散模型 RL、但保留即插即用灵活性的全新范式。其关键创新点可从以下四个维度解构：

### 1. 对齐目标的范式迁移：从参数微调到提示动态优化

传统扩散模型对齐方法（如 **DDPO** (Black et al., ICLR 2024)、**ReFL** (Xu et al., NeurIPS 2024)）直接微调扩散模型参数，存在泛化性差、易出现奖励破解（reward hacking）和过优化、且难以与现有方法组合等瓶颈。前馈式提示优化方法（如 **RePrompt** (Wu et al., 2024)）虽保持了即插即用的灵活性，但未利用扩散过程的时序信息，对齐能力不足。

PromptLoop 将优化目标从模型权重转移到提示文本：**冻结扩散模型，在去噪过程中动态优化提示词**。这一迁移使得方法天然具备即插即用性、泛化性（训练好的策略可直接应用于未见过的扩散模型）和正交组合性（可与 DDPO、Diffusion-DPO 等参数级对齐方法叠加使用）。

### 2. 闭环 MDP 建模：时间步感知的隐空间反馈机制

这是 PromptLoop 最根本的方法创新。现有提示优化方法缺乏反馈机制或仅在采样结束后反馈，未能利用去噪过程的中间状态信息。PromptLoop 将提示优化建模为闭环马尔可夫决策过程（MDP），在每个去噪时间步引入隐空间反馈：

- **状态定义**：$s_t = (x_t, c_t, q, t)$，其中 $x_t$ 为当前噪声隐变量，$c_t$ 为当前提示，$q$ 为用户查询，$t$ 为时间步。
- **动作定义**：$a_t = c_{t-1}$，即策略模型生成的优化提示，作为下一时间步的条件输入。
- **视觉反馈**：从噪声隐变量计算去噪估计 $\hat{\pmb{x}}_t = \frac{1}{\sqrt{\bar{\alpha}_t}} \big( \pmb{x}_{t+1} - \sqrt{1 - \bar{\alpha}_t} \hat{\pmb{\epsilon}}_{\phi}(\pmb{x}_{t+1}, \pmb{c}_t, t) \big)$，作为策略 MLLM 的视觉输入，使其能够感知当前生成状态并据此调整提示。

这一设计建立了与扩散模型 RL 在 MDP 结构上的功能对应关系（见 Figure 3），但 PromptLoop 通过时间步感知的提示作为动作来调控扩散动态，而非直接修改模型参数。消融实验证实，视觉反馈是闭环有效性的关键组件：引入视觉反馈后，ImageReward 从 0.4912 提升至 0.6320，且其他指标未出现下降，表明视觉反馈有效缓解了奖励破解（Table 3, Figure 6）。

### 3. 在线 GRPO 强化学习训练策略

PromptLoop 采用在线的 GRPO（Group Relative Policy Optimization）训练策略，与监督学习或分段 RL 微调形成对比。GRPO 通过组内归一化优势函数 $A_i = \frac{r_i - \mathrm{mean}(\{r_j\}_{j=1}^G)}{\mathrm{std}(\{r_j\}_{j=1}^G)}$ 降低训练方差，同时优化整个生成轨迹而非单步决策。消融实验表明，引入 GRPO 训练后，ImageReward 从 0.0816 提升至 0.4344，验证了强化学习相对于监督学习的必要性（Table 3）。

值得注意的是，扩散模型和奖励模型在训练过程中均被视为黑箱组件，无梯度流经它们，这保证了方法的模块化和即插即用特性。

### 4. 稀疏优化策略：兼顾对齐效果与推理效率

尽管闭环 MDP 要求在多个时间步进行提示优化，PromptLoop 通过稀疏优化策略将额外推理开销控制在可接受范围内。在 5 步提示优化的设置下，总推理时间仅从 15 秒增加至约 18 秒（增幅约 23%），对用户体验影响很小（Table 4）。此外，策略模型学习到扩散过程的转移动态后，可在推理时提前生成所有时间步的优化提示，使扩散过程无中断地进行。

PromptLoop 的整体设计围绕一个核心洞察展开：将提示优化建模为闭环马尔可夫决策过程（MDP），使多模态大语言模型（MLLM）策略能够在去噪过程的每个时间步上，根据隐空间状态迭代优化提示文本。这一设计在功能上等价于直接对扩散模型进行参数级强化学习微调，同时保留了提示方法即插即用的灵活性、泛化性和组合性。

### 闭环提示优化的 MDP 建模

框架将扩散模型的去噪过程重新形式化为一个有限时域的 MDP。在每个去噪时间步 $t$，系统状态定义为：

$$s_t = (x_t, c_t, q, t), \quad a_t = c_{t-1}$$

其中 $x_t$ 为当前噪声隐变量，$c_t$ 为当前提示词，$q$ 为用户原始查询，动作 $a_t$ 即为下一个时间步的优化提示 $c_{t-1}$。这一形式化建立了扩散模型 RL 与提示优化框架之间的结构对应关系，如 Figure 3 所示。

Figure 2 完整展示了闭环提示优化框架的流程。在每一个去噪步骤中：

![[assets/figures/papers/paper_list_l2337_https_arxiv_org_abs_2510_00430/figures/002_Figure_2.jpg]]
*Figure 2: (a) Closed-loop prompt refinement framework with RL. (b) The proposed framework enhances human preference in a plug-and-play manner with minimal additional inference cost. At each denoising step, the policy MLLM takes the current state—denoised estimates, the user query, and prior refinements—and generates an action, a refined prompt. The diffusion model then updates the state, and this loop continues until the final image is produced and scored by the reward model*

1. **状态感知**：策略 MLLM 接收当前状态——包括从噪声隐变量计算得到的去噪估计、用户原始查询以及先前的优化记录。
2. **动作生成**：MLLM 基于当前状态生成优化后的提示词，作为动作 $a_t = c_{t-1}$。
3. **状态转移**：冻结的扩散模型根据优化后的提示执行一步去噪，产生新的隐变量状态 $x_{t-1}$。
4. **闭环迭代**：上述循环持续进行，直至生成最终图像 $x_0$，由奖励模型给出奖励信号 $R = r(x_0, q)$。

### 四大核心模块

框架由四个松耦合的模块组成，扩散模型和奖励模型均被视为黑箱组件，无梯度流经它们：

- **Policy MLLM**（策略多模态大语言模型）：决策核心，接收状态并生成优化后的提示词作为动作。训练时采用在线 GRPO 强化学习，同时优化整个生成轨迹。
- **Diffusion Model (frozen)**（冻结的扩散模型）：被冻结的图像生成器，根据当前提示生成下一状态（图像隐变量），不参与梯度更新。
- **Reward Model**（奖励模型）：黑箱奖励函数，仅在最终图像生成后提供标量奖励信号，用于计算 GRPO 的组内归一化优势函数 $A_i = \frac{r_i - \mathrm{mean}(\{r_j\}_{j=1}^G)}{\mathrm{std}(\{r_j\}_{j=1}^G)}$。
- **Visual Feedback Processor**（视觉反馈处理器）：从当前噪声隐变量计算去噪估计 $\hat{\pmb{x}}_t = \frac{1}{\sqrt{\bar{\alpha}_t}} \big( \pmb{x}_{t+1} - \sqrt{1 - \bar{\alpha}_t} \hat{\pmb{\epsilon}}_{\phi}(\pmb{x}_{t+1}, \pmb{c}_t, t) \big)$，作为策略模型的视觉输入，是隐空间反馈机制的关键组件。

### 训练与推理的分离设计

训练阶段，策略 MLLM 通过 GRPO 在线学习扩散过程的转移动态和奖励模型的偏好。推理阶段，由于策略已学会环境动态，可以在去噪开始前一次性生成所有时间步的优化提示，使扩散过程不间断进行。稀疏优化策略将额外推断时间控制在 23% 以内（5 步优化设置下，从约 15 秒增至约 18 秒/图，见 Table 4），对用户体验影响很小。

### 与扩散模型 RL 的结构对应

Figure 3 揭示了 PromptLoop 与扩散模型 RL 之间的结构性类比与关键差异。传统的扩散模型 RL（如 **DDPO**，Black et al., ICLR 2024）直接微调模型参数，而 PromptLoop 通过时间步感知的提示词作为动作来调控扩散动态。隐空间反馈机制建立了两者之间的功能对应——去噪估计作为策略模型的视觉输入，使 MLLM 能够感知生成过程的中间状态，从而做出与参数级微调等效的优化决策，同时避免了参数更新的泛化性损失和奖励破解风险。

### 即插即用的正交性

框架的核心优势在于其即插即用特性：策略模型仅在原始扩散模型环境中训练一次，即可直接应用于多种已对齐的基线方法（如 **Diffusion-DPO**、**ReFL** 等）和未见过的扩散模型（包括 flow-matching 模型如 **FLUX.1-dev**），无需重新训练。这一特性源于提示优化与参数优化的解耦——策略模型保持固定大小，通过调控文本输入而非模型权重来实现对齐。

### 3.1 闭环MDP形式化

PromptLoop 将提示优化建模为一个有限时域的马尔可夫决策过程（MDP），其状态空间、动作空间和转移动态与扩散模型的去噪过程深度耦合。该形式化的核心洞察在于：**通过在每个去噪时间步引入隐空间反馈，提示优化在功能上等价于对扩散模型参数的强化学习微调，同时保留了提示方法的即插即用特性**。

MDP 的状态与动作定义如下：

$$s_t = (x_t, c_t, q, t), \quad a_t = c_{t-1}$$

其中 $x_t$ 为时间步 $t$ 的噪声隐变量，$c_t$ 为当前提示文本，$q$ 为用户原始查询，$t$ 为去噪时间步索引。动作 $a_t$ 即为策略模型生成的优化提示 $c_{t-1}$，该提示将用于下一步去噪。转移动态由冻结的扩散模型 $p_{\phi}$ 决定：

$$x_{t-1} \sim p_{\phi}^{(t)}(x_{t-1} \mid x_t, c_{t-1})$$

奖励信号仅在最终图像生成后由黑箱奖励函数 $r$ 给出：$R = r(x_0, q)$。扩散模型和奖励模型在整个过程中均被视为黑箱组件，无梯度流经它们。

### 3.2 策略优化：GRPO 训练

策略模型 $\pi_{\theta}$（一个多模态大语言模型）通过在线强化学习进行训练。为降低训练方差，PromptLoop 采用 **Group Relative Policy Optimization (GRPO)**，其组内归一化优势函数为：

$$A_i = \frac{r_i - \mathrm{mean}(\{r_j\}_{j=1}^G)}{\mathrm{std}(\{r_j\}_{j=1}^G)}$$

其中 $G$ 为每组采样轨迹的数量。策略更新使用 PPO 风格的裁剪替代目标与 KL 惩罚：

$$\mathcal{L}_{\mathrm{PPO}}(\boldsymbol{\theta}) = \mathbb{E}_t \left[ \min \Bigl( \rho_t(\boldsymbol{\theta}) \hat{A}_t, \; \mathrm{clip}(\rho_t(\boldsymbol{\theta}), 1 - \epsilon, 1 + \epsilon) \hat{A}_t \Bigr) \right] - \beta \mathrm{KL}[\pi_{\theta_{\mathrm{old}}}(\cdot | s_t) \| \pi_{\theta}(\cdot | s_t) ]$$

其中 $\rho_t(\boldsymbol{\theta})$ 为新旧策略的概率比，$\epsilon$ 为裁剪阈值，$\beta$ 控制 KL 惩罚强度。整个生成轨迹（从 $t=T$ 到 $t=0$）被联合优化，而非分段训练。

### 3.3 隐空间视觉反馈

视觉反馈是 PromptLoop 区别于前馈式提示优化方法的核心组件。在每个时间步 $t$，从当前噪声隐变量 $x_{t+1}$ 计算去噪估计 $\hat{\pmb{x}}_t$，作为策略模型的视觉输入：

$$\hat{\pmb{x}}_t = \frac{1}{\sqrt{\bar{\alpha}_t}} \big( \pmb{x}_{t+1} - \sqrt{1 - \bar{\alpha}_t} \hat{\pmb{\epsilon}}_{\phi}(\pmb{x}_{t+1}, \pmb{c}_t, t) \big)$$

该去噪估计向策略模型揭示了当前生成轨迹的中间状态信息，使 MLLM 能够感知图像内容的演化趋势，从而做出时间步感知的提示调整。消融实验证实，移除视觉反馈会导致奖励对齐效果显著下降，且更容易出现奖励破解（reward hacking）现象。

### 3.4 稀疏优化策略

为控制推理开销，PromptLoop 并非在每个去噪步都调用策略模型。实验表明，在 50 步去噪过程中仅进行 5 次提示优化（均匀分布），即可实现大部分性能增益，同时将总推理时间从 15 秒仅增加至约 18 秒（增加约 23%）。此外，训练收敛后的策略模型可以在推理前预先计算所有时间步的优化提示，使扩散过程无需中断。

## 实验与关键发现

### 核心实验设计

PromptLoop 的实验设计围绕三个核心目标展开：验证闭环提示优化的对齐有效性、证明其与现有方法的正交组合能力、以及测试其跨模型的泛化性能。实验采用 ImageReward 作为主要单一奖励信号，并在 SDXL 和 SD1.5 两个主流扩散模型上进行评估。复合奖励实验则引入 Aesthetic Score 和 CLIP Score 等多维度指标，在 SDXL-turbo 上验证方法对多目标对齐的适应性。

策略模型基于 Qwen2.5-VL-3B 初始化，使用 GRPO 算法在 4 块 NVIDIA A100 (80GB) GPU 上训练约 3 天。扩散模型和奖励模型在训练过程中完全冻结，作为黑箱环境组件。推理时采用稀疏优化策略，仅在 5 个关键时间步进行提示优化，将额外推理时间控制在 23% 以内（约 18 秒/图，见 Table 4）。

### 单一奖励对齐：主结果

Table 1 报告了 PromptLoop 在单一奖励对齐任务上的核心结果。在 SDXL + ImageReward 设置下，PromptLoop 取得 **1.0948** 的 ImageReward 分数，相比原始扩散模型的 0.7244 提升 **+0.3704**，显著优于 RePrompt（前馈式提示优化基线）的 0.7876。在 SD1.5 上，提升幅度更为显著：从 0.0816 跃升至 **0.6320**（+0.5504）。

![[assets/figures/papers/paper_list_l2337_https_arxiv_org_abs_2510_00430/figures/005_Table_1.jpg]]
*Table 1: Quantitative evaluation on single-reward alignment with SD1.5 and SDXL, showing comparison with baselines and demonstrating orthogonality and generalizability*

值得注意的是，PromptLoop 在性能上接近甚至超越了需要微调扩散模型参数的方法。在 SDXL 上，DDPO（Black et al., ICLR 2024）取得 0.9495，ReFL（Xu et al., NeurIPS 2024）取得 1.0783，而 PromptLoop 的 1.0948 均高于两者。这一结果表明，通过隐空间反馈驱动的提示优化，可以在不触碰扩散模型权重的前提下，实现与参数级微调相当甚至更优的对齐效果。

**正交组合能力**：Table 1 进一步展示了 PromptLoop 与现有对齐方法的组合效果。将 PromptLoop 应用于已通过 Diffusion-DPO（Wallace et al., 2024）对齐的 SDXL 模型时，ImageReward 从 0.9921 进一步提升至 **1.2898**（+0.2977）。这验证了 PromptLoop 作为即插即用模块，可以与参数级对齐方法正交叠加，且无需针对新环境重新训练策略模型。

### 复合奖励对齐

Table 2 展示了在复合奖励设置下的对齐结果。在 SDXL-turbo 上，PromptLoop 在 ImageReward 上取得 **0.8516**，优于 RePrompt 的 0.7876。同时，Aesthetic Score 从 5.41 提升至 5.62，CLIP Score 保持稳定（0.313 vs 0.312），表明方法在优化主要奖励时未对其他指标造成显著负面影响。与单一奖励实验类似，PromptLoop 与 RePrompt 的组合进一步将 ImageReward 提升至 0.8516，验证了其在复合奖励场景下的正交性。

![[assets/figures/papers/paper_list_l2337_https_arxiv_org_abs_2510_00430/figures/006_Table_2.jpg]]
*Table 2: Quantitative evaluation on composite-reward alignment with SDXL-turbo, showing comparison with baselines and demonstrating orthogonality and generalizability*

### 消融实验：闭环反馈的关键性

Table 3 和 Figure 6 的系统消融揭示了 PromptLoop 各组件的贡献层级：

![[assets/figures/papers/paper_list_l2337_https_arxiv_org_abs_2510_00430/figures/004_Table_3.jpg]]
*Table 3: Ablation study results showing the effectiveness of each proposed component*

![[assets/figures/papers/paper_list_l2337_https_arxiv_org_abs_2510_00430/figures/010_Figure_6.jpg]]
*Figure 6: Ablation study demonstrating that incorporating visual feedback and increasing the number of refinement steps consistently enhances reward alignment. (Left: SDXL, Right: SD1.5; reward: ImageReward)*

1. **RL 训练的必要性**：移除 GRPO 训练后（仅使用监督微调），SD1.5 上的 ImageReward 从 0.6320 降至 0.0816（原始扩散模型水平），表明强化学习是驱动提示优化的核心机制。单独引入 GRPO（无视觉反馈）可将分数提升至 0.4344，验证了在线奖励信号对策略学习的驱动作用。

2. **视觉反馈的关键作用**：在 GRPO 基础上引入视觉反馈（去噪估计 $\hat{\pmb{x}}_t$），ImageReward 从 0.4912 进一步提升至 **0.6320**，且其他指标（如 CLIP Score、Aesthetic Score）未出现下降。Figure 6 的曲线显示，无视觉反馈时，增加优化步数带来的收益趋于饱和甚至波动；而有视觉反馈时，奖励随优化步数单调递增。这表明视觉反馈有效缓解了奖励破解（reward hacking）和过优化问题——策略模型能够根据当前生成状态动态调整提示，而非盲目堆砌高奖励关键词。

3. **策略模型规模的影响**：将策略模型从 Qwen2.5-VL-3B 替换为更强的 Qwen3-VL-4B 后，ImageReward 从 0.6320 提升至 **0.6922**（Table 7），说明更强的视觉-语言理解能力有助于更精准的隐空间状态感知和提示优化。

### 泛化能力：零样本迁移

Table 6 展示了策略模型在未见过的扩散模型上的零样本泛化能力。在 FLUX.1-dev（flow-matching 模型）上，PromptLoop 将 ImageReward 从 1.001 提升至 **1.246**（+0.245），证明了方法对不同扩散范式的适应性。这一泛化能力源于策略模型仅依赖去噪估计作为视觉输入，而该信号在 DDPM 和 flow-matching 框架中均可计算，使策略无需针对新骨干网络重新训练。

![[assets/figures/papers/paper_list_l2337_https_arxiv_org_abs_2510_00430/figures/017_Table_6.jpg]]
*Table 6: Quantitative results demonstrating zero-shot generalization to recent flow-matching models*

### 提示演变与语义保持

Table 5 揭示了提示词在不同时间步的演变模式：早期时间步（高噪声阶段）的优化提示倾向于强调整体氛围和风格属性；中间时间步逐步扩展为具体细节描述；后期时间步则维持或微调这些细节。Figure 11 显示提示长度随优化步数平缓增长，未出现灾难性膨胀或超出文本编码器限制。Figure 12 的语义漂移分析表明，BERTScore-recall 和 LLM-based recall 均保持在较高水平，核心用户意图在优化过程中得到良好保留。

### 失败模式与局限

尽管 PromptLoop 在多项指标上表现优异，仍需注意以下局限：

1. **奖励模型依赖性**：方法的优化方向完全由奖励模型决定。Figure 4 的定性对比显示，ReFL 虽然获得较高奖励分数，但存在明显的奖励破解现象（生成图像过度迎合奖励模型的浅层特征）。PromptLoop 通过视觉反馈机制部分缓解了这一问题，但无法从根本上纠正奖励模型的系统性偏差。

2. **训练资源需求**：4 块 A100 GPU 训练 3 天的资源门槛对学术研究团队构成一定障碍。策略模型的蒸馏或轻量化可能是降低训练成本的可行方向。

3. **推理延迟的固有增加**：尽管 23% 的额外时间开销在可接受范围内，但在实时或大规模生成场景下仍需进一步优化。稀疏优化步数的自适应选择（根据任务复杂度动态调整）可能是一个改进方向。

4. **定性评估的局限性**：现有自动评估指标（如 ImageReward）可能未能完全捕捉人类主观偏好。部分定性结果显示，高奖励分数并不总是对应更符合人类审美的图像，提示需要更全面的评估体系。

## 定位与知识库关联

### 1. 扩散模型对齐的范式地图

当前扩散模型对齐方法主要分为两大范式：**参数级微调**与**提示级优化**。PromptLoop 在这张地图中占据了一个独特的交叉位置——它以提示优化的形式实现了参数级微调的功能等价性。

**参数级微调范式**的代表工作包括：
- **DDPO**（Black et al., ICLR 2024）：将扩散模型的去噪过程建模为 MDP，使用策略梯度直接更新 UNet 权重。这是扩散模型 RL 微调的开创性工作，但存在泛化性差、易出现奖励破解（reward hacking）和过优化等问题。
- **ReFL**（Xu et al., NeurIPS 2024）：基于奖励加权回归的微调方法，通过偏好数据调整模型参数。
- **Diffusion-DPO**（Wallace et al., 2024）：将直接偏好优化（DPO）引入扩散模型，利用成对偏好数据对齐。
- **DanceGRPO**（2024）：扩散模型专用的 GRPO 变体，在参数空间进行组相对策略优化。
- **NPNet**（2024）：噪声优化方法，通过优化初始噪声而非模型参数来改善生成质量。

这些方法的共同瓶颈在于：直接修改扩散模型权重，导致**泛化性受限**（训练后的策略难以迁移到其他扩散模型），**组合性差**（不同对齐方法之间无法正交叠加），且**计算成本高**（每次更换奖励函数或下游模型都需要重新微调）。

**提示级优化范式**的代表工作包括：
- **RePrompt**（Wu et al., 2024）：前馈式提示优化方法，在采样开始前一次性生成优化提示。其核心局限在于**未利用扩散过程的时序信息**——去噪过程的不同阶段对应从全局结构到局部细节的渐进生成，单一的前馈优化无法感知这一动态变化，导致对齐能力不足。

### 2. PromptLoop 的定位：闭环提示优化

PromptLoop 的核心理念是将提示优化建模为**闭环 MDP**，使 MLLM 策略在去噪过程的每个时间步上根据隐空间状态迭代优化提示。这一设计在功能上等价于扩散模型 RL（见图 3），但保留了提示方法的三个关键优势：

1. **即插即用（Plug-and-Play）**：冻结扩散模型权重，仅训练一个轻量级 MLLM 策略。训练好的策略可直接应用于未见过的扩散模型（包括 flow-matching 模型如 FLUX.1-dev），无需重新训练（Table 6 验证，ImageReward 从 1.001 提升至 1.246）。

2. **正交组合性**：可与现有对齐方法叠加使用。Table 1 显示，将 PromptLoop 应用于已对齐的 Diffusion-DPO 模型，ImageReward 从 0.9921 进一步提升至 1.2898（+0.2977）。Table 2 验证了在复合奖励场景下与 RePrompt 的正交组合效果。

3. **缓解奖励破解**：视觉反馈机制使策略能够感知生成过程中的语义漂移，避免过度优化单一奖励指标。Figure 6 的消融实验证实，引入视觉反馈后 ImageReward 从 0.4912 提升至 0.6320，同时其他指标未下降。

### 3. 关键设计差异与因果机制

PromptLoop 与两类基线方法的核心差异体现在三个维度：

**反馈机制**（changed_slot: feedback_mechanism）：
- 参数微调方法通过奖励信号的梯度反向传播获取反馈，但这一反馈是**稀疏的**（仅在采样结束后获得）。
- RePrompt 等前馈方法**无反馈**机制，一次性生成优化提示后不再调整。
- PromptLoop 引入**时间步感知的隐空间反馈**：在每个去噪步骤，通过去噪估计 $\hat{\pmb{x}}_t = \frac{1}{\sqrt{\bar{\alpha}_t}} \big( \pmb{x}_{t+1} - \sqrt{1 - \bar{\alpha}_t} \hat{\pmb{\epsilon}}_{\phi}(\pmb{x}_{t+1}, \pmb{c}_t, t) \big)$ 将当前噪声隐变量重构为近似干净图像，作为策略模型的视觉输入。这一设计使 MLLM 能够感知生成过程中的结构演变，从而在不同时间步生成适配的提示优化（Table 5 展示了早期提示强调氛围、中期扩展细节、后期保持或回归原型描述符的演变模式）。

**训练策略**（changed_slot: training_strategy）：
- 监督学习方法依赖人工标注的提示对，泛化能力受限于训练数据分布。
- 参数级 RL 方法直接优化模型权重，存在训练不稳定、模式坍塌等风险。
- PromptLoop 采用**在线 GRPO 强化学习**，使用组内归一化优势函数 $A_i = \frac{r_i - \mathrm{mean}(\{r_j\}_{j=1}^G)}{\mathrm{std}(\{r_j\}_{j=1}^G)}$ 降低训练方差，同时优化整个生成轨迹。Table 3 的消融实验显示，引入 GRPO 训练后 ImageReward 从 0.0816 提升至 0.4344，验证了强化学习的必要性。

**推理开销**（changed_slot: inference_overhead）：
- 参数微调方法在推理时无额外开销，但训练成本高且泛化性差。
- PromptLoop 通过**稀疏优化策略**将额外推理时间控制在 23% 以内（Table 4：5 步优化从 15s 增至 18.43s/图，A100×1，batch size=8）。更重要的是，一旦策略学会环境转移动态，可在推理前预生成所有时间步的优化提示，使扩散过程无中断执行。

### 4. 适用边界与局限

尽管 PromptLoop 展现了强大的泛化性和组合性，其适用边界仍需明确：

1. **训练资源需求较高**：每次训练需 4 块 NVIDIA A100 (80GB) GPU，耗时约 3 天。对于计算资源有限的研究团队，这一门槛可能限制复现和后续改进。

2. **推理时额外 MLLM 调用**：虽然稀疏优化已将时间开销控制在 23% 以内，但对于实时交互场景（如在线对话式图像生成），额外的 3-4 秒延迟仍可能影响用户体验。

3. **奖励模型依赖**：方法的对齐效果高度依赖奖励模型的质量。如果奖励函数未能正确反映人类偏好（例如 ImageReward 在某些场景下与人类判断存在偏差），优化方向可能出现系统性偏差。Figure 4 的定性结果显示，ReFL 虽然获得高奖励但存在明显的奖励破解现象，提示现有自动评估指标可能未能完全捕捉人类主观偏好。

4. **策略模型容量限制**：消融实验（Table 7）显示，更强的策略初始化（Qwen3-VL-4B vs Qwen2.5-VL-3B）使 ImageReward 从 0.6320 提升至 0.6922，表明策略模型的视觉理解和语言生成能力是性能上限的关键因素。在极端复杂的多目标对齐场景下，当前规模的 MLLM 可能不足以捕捉所有偏好维度。

### 5. 开放问题

1. **推理效率的进一步优化**：是否可以通过知识蒸馏训练一个轻量级策略模型（如将 MLLM 蒸馏为仅保留视觉-语言对齐能力的专用网络），使其在消费级 GPU 上也能高效运行？

2. **视频扩散模型的扩展**：当前方法在图像扩散模型上验证有效，但视频生成涉及更高维度的时序隐空间状态。时序反馈机制在视频扩散模型中的有效性，以及如何处理帧间一致性与奖励对齐之间的潜在冲突，仍有待探索。

3. **训练效率提升**：是否可以通过 curriculum learning（从简单奖励函数逐步过渡到复杂复合奖励）或分阶段训练策略（先预训练视觉编码器，再联合优化提示生成）进一步提升收敛速度和对齐效果？

4. **多目标偏好冲突的解决**：在同时兼顾美观性、安全性、多样性和文本对齐度的复合奖励场景下，不同奖励函数之间可能存在冲突（如高美观性可能导致多样性下降）。如何设计奖励聚合机制或帕累托优化策略，避免优化方向的相互抵消，是一个重要的开放问题。

5. **评估指标的局限性**：现有自动评估指标（如 ImageReward、Aesthetic Score）与人类主观判断之间的 gap 尚未完全弥合。开发更鲁棒的、能检测奖励破解现象的评估基准，对于推动该领域的发展至关重要。

## 原文 PDF

![[paperPDFs/CVPR_2026/PromptLoop_Plug_and_Play_Prompt_Refinement_via_Latent_Feedback_for_Diffusion_Model_Alignment.pdf]]
