---
title: "DenseGRPO: From Sparse to Dense Reward for Flow Matching Model Alignment"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/DenseGRPO_From_Sparse_to_Dense_Reward_for_Flow_Matching_Model_Alignment.pdf
project_link: null
code_link: null
openreview_forum_id: nIwFge9nW0
aliases:
- DenseGRPO
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "通过引入基于ODE的稠密奖励估计，为每个去噪步骤提供与贡献对齐的逐步奖励信号，并根据估计的奖励分布自适应校准SDE采样器中的时间步特定噪声注入，以平衡探索空间。"
primary_logic: "利用流匹配模型ODE采样器的确定性映射，将中间潜变量解码为相应的干净图像，借助现成的奖励模型评估其未来价值，然后通过计算相邻步骤间的奖励增益（ΔR_t^i = R_{t-1}^i - R_t^i）获得精确的逐步稠密奖励；同时，基于稠密奖励的分布，动态调整每个时间步的噪声强度ψ(t)，使环境探索更加合理，从而显著提升GRPO训练效果。"
claims:
- "DenseGRPO估计每个去噪步骤的奖励增益作为稠密奖励，解决了稀疏奖励导致的反馈-贡献不匹配问题。"
- "通过ODE去噪将中间潜变量映射为干净图像，利用现有奖励模型评估其奖励，作为潜变量的奖励。"
- "用逐步稠密奖励替代终端奖励计算优势，实现步骤级优化。"
- "提出奖励感知的探索空间校准策略，自适应调整SDE采样器的噪声注入，平衡正负奖励分布。"
---

# DenseGRPO: From Sparse to Dense Reward for Flow Matching Model Alignment

> [!tip] 核心洞察
> 利用流匹配模型ODE采样器的确定性映射，将中间潜变量解码为相应的干净图像，借助现成的奖励模型评估其未来价值，然后通过计算相邻步骤间的奖励增益（ΔR_t^i = R_{t-1}^i - R_t^i）获得精确的逐步稠密奖励；同时，基于稠密奖励的分布，动态调整每个时间步的噪声强度ψ(t)，使环境探索更加合理，从而显著提升GRPO训练效果。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | DenseGRPO：从稀疏到稠密奖励的流匹配模型对齐 |
| 英文题名 | DenseGRPO: From Sparse to Dense Reward for Flow Matching Model Alignment |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=nIwFge9nW0) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | DenseGRPO |
| Dataset | Compositional Image Generation, Visual Text Rendering, Human Preference Alignment |

> [!tip] 效果简介
> - Compositional Image Generation 上，GenEval 为 0.97，对比 0.95 (Flow-GRPO)，变化 +0.02。
> - Visual Text Rendering 上，OCR Acc 为 0.95，对比 0.92 (Flow-GRPO)，变化 +0.03。
> - Human Preference Alignment 上，PickScore 为 24.64，对比 23.31 (Flow-GRPO)，变化 +1.33。

## 概要

现有基于GRPO的流匹配模型对齐方法（如Flow-GRPO、DanceGRPO）面临一个核心瓶颈：它们仅在整个去噪轨迹终点生成单一的稀疏奖励信号，并将该终端奖励不加区分地应用于所有中间步骤的优化。这种全局反馈与每个去噪步骤的细粒度贡献之间存在严重的不匹配（mismatch），导致策略学习被误导。

DenseGRPO针对这一瓶颈提出了两个关键改进。首先，它利用流匹配模型ODE采样器的确定性映射性质，将中间潜变量解码为对应的干净图像，借助现成的奖励模型评估其未来价值，然后通过计算相邻步骤间的奖励增益（$\Delta R_t^i = R_{t-1}^i - R_t^i$）获得精确的逐步稠密奖励，从而为每个去噪步骤提供与其贡献对齐的反馈信号。其次，它提出了一种奖励感知的探索空间校准策略，根据估计的稠密奖励分布，自适应调整SDE采样器中每个时间步的噪声强度 $\psi(t)$，以平衡正负奖励的探索空间，使环境探索更加合理。

在组合图像生成（GenEval）、视觉文本渲染（OCR Acc）和人类偏好对齐（PickScore）三个基准任务上，DenseGRPO均取得了优于Flow-GRPO等基线方法的结果。例如，在GenEval上达到0.97（+0.02），OCR Acc达到0.95（+0.03），PickScore达到24.64（+1.33）。消融实验证实，逐步稠密奖励和时间步特定的噪声校准各自对性能提升均有显著贡献。该方法还展现出良好的泛化性，在FLUX.1-dev、高分辨率SD 3.5-M以及扩散模型SD 1.5上均可带来一致的性能增益。

### 流匹配模型与偏好对齐

流匹配模型（Flow Matching）通过常微分方程（ODE）定义从噪声到数据的确定性映射，已成为文本到图像生成的主流范式。为了提高生成图像与人类偏好的对齐度，近期工作将迭代去噪过程形式化为马尔可夫决策过程（MDP），并引入群组相对策略优化（GRPO）进行强化学习微调。在该框架下，状态定义为 $\mathbf{s}_t \triangleq (c, t, x_t)$，策略对应条件去噪分布 $\pi(\mathbf{a}_t \mid \mathbf{s}_t) \triangleq p(x_{t-1} \mid x_t, c)$，动作 $\mathbf{a}_t \triangleq x_{t-1}$ 为前一步潜变量。

### 稀疏奖励的核心瓶颈

现有基于GRPO的流匹配对齐方法（如 **Flow-GRPO**（Liu et al., 2025）和 **DanceGRPO**（Xue et al., 2025））存在一个结构性缺陷：**反馈-贡献不匹配（feedback-contribution mismatch）**。具体而言，这些方法仅在整个去噪轨迹的终点通过奖励模型 $\mathscr{R}(x_0, c)$ 生成一个稀疏的终端奖励，并将该全局信号直接应用于所有中间步骤的优化：

$$
R(\mathbf{s}_t, \mathbf{a}_t) \triangleq \begin{cases}
\mathscr{R}(x_0, c), & \text{if } t = 0 \\
0, & \text{otherwise}
\end{cases}
$$

这种做法隐含假设每个去噪步骤对最终图像质量的贡献是均等的，但实际上去噪过程中不同时间步的作用存在显著差异——早期步骤决定全局结构，后期步骤细化局部细节。将终端奖励均匀分配给所有步骤，会导致对早期关键步骤的反馈不足，而对后期微调步骤的反馈过度，从而误导策略梯度方向。

**Flow-GRPO+CoCA**（Liao et al., 2025）尝试通过潜在相似度进行轨迹级奖励分配，但本质上仍是对单一终端奖励的重新加权，未能从根本上解决步骤级贡献的精确度量问题。

### 探索空间的不合理设计

除奖励信号外，现有方法在SDE采样器的噪声注入策略上同样存在缺陷。Flow-GRPO等采用统一的标量噪声水平 $a$，即 $\sigma_t = a \sqrt{t/(1-t)}$，对所有时间步施加相同的随机扰动强度。然而，不同去噪阶段所需的探索空间并不相同：早期高噪声阶段需要更大的探索范围以发现多样化的结构，而后期低噪声阶段则需要更精细的局部搜索。统一的噪声设置导致探索空间与奖励分布不匹配——某些时间步的探索不足限制了生成多样性，而另一些时间步的过度探索则引入了破坏性噪声。

### 本文动机

针对上述两个核心问题，本文提出 **DenseGRPO**，核心思路包括：

1. **稠密奖励估计**：利用流匹配模型ODE采样器的确定性映射特性，将中间潜变量通过ODE去噪解码为对应的干净图像，借助现成的奖励模型评估其未来价值，再通过计算相邻步骤间的奖励增益 $\Delta R_t^i = R_{t-1}^i - R_t^i$ 获得精确的逐步稠密奖励，使每个去噪步骤获得与其贡献对齐的反馈信号。

2. **奖励感知的探索空间校准**：基于稠密奖励的分布，动态调整每个时间步的噪声强度 $\psi(t)$，使正负奖励样本数量保持平衡，从而为每个去噪阶段创造合适的探索空间。

## 核心方法与创新机理

DenseGRPO 的核心创新在于将现有基于 GRPO 的流匹配模型对齐方法从**稀疏终端奖励**升级为**逐步稠密奖励**，并配套设计了**奖励感知的探索空间校准**机制。这两个 changed slot 共同解决了 Flow-GRPO（Liu et al., 2025）等现有方法中全局反馈信号与每个去噪步骤细粒度贡献不匹配（mismatch）的根本瓶颈。

### 从稀疏奖励到逐步稠密奖励

现有方法（如 Flow-GRPO、DanceGRPO）仅在去噪轨迹的终点生成一个稀疏的终端奖励 $R(x_0^i, c)$，并将其均匀应用于所有中间步骤的优化。这种设计隐含假设每个步骤对最终图像质量的贡献相同，但实际上不同时间步的去噪操作对最终结果的边际收益差异显著——早期步骤负责布局生成，后期步骤负责细节精修。稀疏奖励无法区分这些差异，导致策略学习被误导。

DenseGRPO 通过 ODE 去噪实现了对每个中间步骤贡献的精确量化。具体而言，对于任意中间潜变量 $x_t^i$，利用流匹配模型 ODE 采样器的确定性映射将其解码为对应的干净潜变量：

$$\hat{x}_{t,0}^i = \mathrm{ODE}_n(x_t^i, c)$$

随后借助现成的奖励模型评估该干净图像的奖励值，并将其赋值给原中间潜变量：

$$R_t^i \triangleq R_{t,0}^i = \mathscr{R}(\hat{x}_{t,0}^i, c)$$

在此基础上，定义时间步 $t$ 的**逐步稠密奖励**为相邻步骤间的奖励增益：

$$\Delta R_t^i = R_{t-1}^i - R_t^i$$

这一差分形式精确刻画了从 $x_t^i$ 去噪到 $x_{t-1}^i$ 这一单步操作所带来的奖励提升，从而实现了奖励反馈与步骤贡献的对齐。在 GRPO 的优势计算中，用 $\Delta R_t^i$ 替代原有的稀疏终端奖励：

$$\hat{A}_t^i = \frac{\Delta R_t^i - \mathrm{mean}(\{\Delta R_t^i\}_{i=1}^G)}{\mathrm{std}(\{\Delta R_t^i\}_{i=1}^G)}$$

消融实验证实，逐步稠密奖励在每一步提供与贡献对齐的反馈信号，显著优于轨迹级稀疏奖励（Fig. 6a）。此外，增加 ODE 去噪步数 $n$ 可提高稠密奖励的准确性，从而进一步提升性能（Fig. 6c）。

### 奖励感知的探索空间校准

GRPO 训练依赖 SDE 采样器注入随机噪声来构建探索空间，噪声强度 $\sigma_t$ 直接决定探索范围。现有方法采用统一标量 $a$ 控制所有时间步的噪声水平（$\sigma_t = a\sqrt{t/(1-t)}$），忽略了不同时间步对探索需求的差异。如图 3 所示，固定的 $a$ 值会导致某些时间步的正负奖励分布严重失衡——要么正奖励过多使探索不足，要么负奖励过多使训练信号退化。

DenseGRPO 提出了**奖励感知的探索空间校准**策略，将统一噪声水平替换为时间步特定的函数 $\psi(t)$：

$$\sigma_t = \psi(t)$$

校准过程（Algorithm 1）通过迭代调整各时间步的噪声强度来平衡正负奖励数量：当某时间步的正负奖励数量差小于阈值 $\varepsilon_1$ 时，增加 $\psi(t)$ 以扩大探索；反之则减小 $\psi(t)$ 以收缩探索。这一设计使 SDE 采样器能够在所有时间步创造更合理的探索空间，消融实验验证了其有效性（Fig. 6b）。

值得注意的是，Flow-GRPO+CoCA（Liao et al., 2025）虽然也尝试改进奖励分配，但其基于潜在相似度的轨迹级分配方法仍停留在全局层面，未能实现 DenseGRPO 的步骤级精确反馈。

![[assets/figures/papers/paper_list_l29_https_openreview_net_forum_id_nIwFge9nW0/figures/002_Figure_1.jpg]]
*Figure 1: (a) Existing approaches only predict a single, sparse reward at the end of the denoising trajectory, which is naively applied to optimize all intermediate steps. (b) DenseGRPO estimates step-wise rewards of individual steps, densifying the feedback signal for the denoising process*

![[assets/figures/papers/paper_list_l29_https_openreview_net_forum_id_nIwFge9nW0/figures/003_Figure_2.jpg]]
*Figure 2: Overview of DenseGRPO. Given the i-th trajectory within a GRPO group, we first predict the rewards $\{ R _ { t } ^ { i } \}$ of latents $\{ x _ { t } ^ { i } \}$ via ODE denoising. By capturing the reward gain $\{ \Delta R _ { t } ^ { i } \}$ at each step, we obtain the dense reward that reliably evaluates the step-wise contribution*

DenseGRPO 的整体框架围绕一个核心矛盾展开：现有基于 GRPO 的流匹配模型对齐方法（如 **Flow-GRPO**（Liu et al., 2025）和 **DanceGRPO**（Xue et al., 2025））仅在整个去噪轨迹末端生成单一的稀疏终端奖励，并将该全局信号不加区分地应用于所有中间时间步的优化。这种“反馈-贡献不匹配”（mismatch）是制约策略学习效果的关键瓶颈，因为每一步去噪对最终图像质量的贡献并不相同，却被迫接收相同的奖励信号。

DenseGRPO 通过两个相互协同的模块化解这一瓶颈，其整体流程如图 2 所示。

**1. 逐步稠密奖励估计（Step-wise Dense Reward Estimation）**

框架的第一阶段将稀疏反馈“稠密化”。对于 GRPO 组内的第 i 条轨迹，SDE 采样器首先生成一系列中间潜变量 $\{x_t^i\}_{t=T}^{1}$。随后，系统利用流匹配模型 ODE 采样器的确定性映射特性，通过 n 步 ODE 去噪将每个中间潜变量 $x_t^i$ 解码为对应的干净潜变量 $\hat{x}_{t,0}^i$：

$$\hat{x}_{t,0}^i = \mathrm{ODE}_n(x_t^i, c)$$

接着，借助现成的奖励模型 $\mathscr{R}$ 对该干净潜变量进行评估，将其输出作为原中间潜变量 $x_t^i$ 的奖励值：

$$R_t^i \triangleq R_{t,0}^i = \mathscr{R}(\hat{x}_{t,0}^i, c)$$

完成所有时间步的奖励预测后，系统通过计算相邻步骤间的奖励增益来定义逐步稠密奖励：

$$\Delta R_t^i = R_{t-1}^i - R_t^i$$

这一差值精确量化了从时间步 t 到 t-1 的单步去噪对最终奖励的贡献，从而将原本的全局稀疏信号转化为与每步贡献对齐的细粒度反馈。

**2. 步骤级优势计算与策略优化**

在获得逐步稠密奖励后，DenseGRPO 将其替代原有的终端奖励，用于计算组归一化优势：

$$\hat{A}_t^i = \frac{\Delta R_t^i - \mathrm{mean}(\{\Delta R_t^i\}_{i=1}^G)}{\mathrm{std}(\{\Delta R_t^i\}_{i=1}^G)}$$

该优势信号驱动策略 $\pi_\theta$ 在每个时间步上分别进行优化，使模型能够区分不同去噪步骤的差异化贡献，而非像 Flow-GRPO 那样对所有步骤施加相同的更新方向。

**3. 奖励感知的探索空间校准**

框架的第二阶段解决探索空间的适配问题。SDE 采样器的噪声强度 $\sigma_t$ 决定了策略探索的范围。现有方法通常采用统一标量 a 设定噪声水平（$\sigma_t = a\sqrt{t/(1-t)}$），但这忽略了不同时间步对探索强度的差异化需求。DenseGRPO 提出奖励感知的校准策略：在预热阶段，系统统计各时间步上正负稠密奖励的分布，并自适应调整时间步特定的噪声强度 $\psi(t)$，使正负奖励的数量趋于平衡。当正奖励样本过多时，算法增大噪声以扩大探索范围；当负奖励样本过多时，则减小噪声以收缩探索空间。最终，SDE 采样器采用校准后的噪声水平：

$$\sigma_t = \psi(t)$$

这一机制确保策略在每个时间步都能在合适的探索空间内采样，从而提升 GRPO 训练的稳定性和最终效果。

**模块间的数据流关系**

整个框架的数据流可概括为：SDE 采样器生成轨迹 → ODE 去噪模块将中间潜变量映射为干净图像 → 奖励模型评估各步奖励 → 稠密奖励计算模块输出 $\Delta R_t^i$ → 优势计算模块生成步骤级优势 → 策略更新。探索空间校准模块则通过监测稠密奖励分布，反馈调节 SDE 采样器的噪声强度，形成闭环优化。

### 核心瓶颈：稀疏奖励的反馈‑贡献失配

现有基于 GRPO 的流匹配对齐方法（如 **Flow‑GRPO**，Liu et al., 2025；**DanceGRPO**，Xue et al., 2025）将去噪过程建模为马尔可夫决策过程（MDP），但仅在轨迹终点给出单一稀疏奖励 $R(x_0^i, c)$，并将其不加区分地应用于所有中间步骤的优化。这一做法忽略了各去噪步骤对最终图像质量的差异化贡献，导致**全局反馈信号与步骤级贡献之间的失配（mismatch）**，误导策略学习。

DenseGRPO 的核心调控旋钮在于：**为每个去噪步骤提供与其贡献对齐的逐步稠密奖励**，并基于估计的奖励分布**自适应校准 SDE 采样器的时间步特定噪声注入**，以平衡探索空间。

---

### 模块一：基于 ODE 的逐步稠密奖励估计

该模块的目标是将稀疏终端奖励“稠密化”为每个去噪步骤的奖励增益，从而实现对单步贡献的精确评估。其流程如 Figure 2 所示，包含三个子步骤。

#### 1.1 ODE 去噪：从中间潜变量到干净图像

利用流匹配模型中常微分方程（ODE）采样器的确定性映射，将任意中间时间步 $t$ 的潜变量 $x_t^i$ 解码为对应的干净潜变量 $\hat{x}_{t,0}^i$：

$$\hat{x}_{t,0}^i = \mathrm{ODE}_n(x_t^i, c) \tag{Eq. 8}$$

其中 $c$ 为文本条件，$n$ 为 ODE 去噪步数。ODE 的确定性保证了映射的一致性，使得中间潜变量的奖励可以被可靠地赋值。

#### 1.2 潜变量奖励赋值

将 ODE 去噪得到的干净潜变量送入现成的奖励模型 $\mathscr{R}$，获得其奖励值，并将该奖励直接赋值给原始中间潜变量 $x_t^i$：

$$R_t^i \triangleq R_{t,0}^i = \mathscr{R}(\hat{x}_{t,0}^i, c) \tag{Eq. 9}$$

这一步的核心洞察是：**中间潜变量的奖励可被可靠地赋值为其对应干净图像的奖励**，从而绕过了直接对噪声潜变量评估的困难。

#### 1.3 逐步稠密奖励计算

定义时间步 $t$ 的稠密奖励为相邻步骤间的奖励增益：

$$\Delta R_t^i = R_{t-1}^i - R_t^i \tag{Eq. 7}$$

$\Delta R_t^i$ 量化了从 $x_t^i$ 去噪到 $x_{t-1}^i$ 这一单步操作所带来的奖励提升，因此能够**精确反映该步骤对最终图像质量的边际贡献**。

---

### 模块二：基于稠密奖励的优势计算

将原始 GRPO 中的稀疏终端奖励替换为逐步稠密奖励，计算组归一化优势：

$$\hat{A}_t^i = \frac{\Delta R_t^i - \mathrm{mean}(\{\Delta R_t^i\}_{i=1}^G)}{\mathrm{std}(\{\Delta R_t^i\}_{i=1}^G)} \tag{Eq. 10}$$

其中 $G$ 为 GRPO 组大小。与原始 Flow‑GRPO 使用 $R(x_0^i, c)$ 计算优势不同，此处的 $\hat{A}_t^i$ 在**每个时间步独立计算**，实现了真正的步骤级优化。

---

### 模块三：奖励感知的探索空间校准

现有方法采用统一标量 $a$ 控制 SDE 采样器的噪声水平 $\sigma_t = a \sqrt{t/(1-t)}$，导致探索空间在不同时间步失衡（Figure 3）。DenseGRPO 提出**奖励感知的探索空间校准**，输出时间步特定的噪声函数 $\psi(t)$：

$$\sigma_t = \psi(t) \tag{Eq. 11}$$

校准过程（Algorithm 1）基于稠密奖励的分布进行自适应调整：在每个校准步骤中，统计正奖励样本数 $\mathrm{num}(\{\Delta R_t^i > 0\})$ 与负奖励样本数 $\mathrm{num}(\{\Delta R_t^i < 0\})$ 的差异。若二者数量接近（差异小于阈值 $\varepsilon_1$），则增大 $\psi(t)$ 以扩展探索空间；反之则减小 $\psi(t)$ 以收缩探索范围。通过迭代调整，最终使各时间步的正负奖励分布趋于平衡，从而创造更合理的探索环境。

---

### 关键公式速查

| 公式 | 变量含义 | 锚点 |
|------|----------|------|
| $\Delta R_t^i = R_{t-1}^i - R_t^i$ | 时间步 $t$ 的逐步稠密奖励，量化单步贡献 | Eq. 7 |
| $\hat{x}_{t,0}^i = \mathrm{ODE}_n(x_t^i, c)$ | $n$ 步 ODE 去噪，将中间潜变量解码为干净潜变量 | Eq. 8 |
| $R_t^i \triangleq \mathscr{R}(\hat{x}_{t,0}^i, c)$ | 将干净图像的奖励赋值给中间潜变量 | Eq. 9 |
| $\hat{A}_t^i = \frac{\Delta R_t^i - \mathrm{mean}(\{\Delta R_t^i\})}{\mathrm{std}(\{\Delta R_t^i\})}$ | 基于稠密奖励的组归一化优势 | Eq. 10 |
| $\sigma_t = \psi(t)$ | 时间步特定的 SDE 噪声水平 | Eq. 11 |

## 实验与关键发现

### 主要结果

DenseGRPO 在三个核心基准任务上均取得最优表现，验证了稠密奖励与探索校准机制的有效性。

**组合图像生成（Compositional Image Generation）** 任务使用 GenEval 指标评估模型对复杂组合指令的遵循能力。DenseGRPO 达到 **0.97**，较 Flow-GRPO 的 0.95 提升 0.02（Table 1）。这表明逐步奖励信号使模型在每个去噪步骤都能获得与局部贡献对齐的反馈，从而更精确地执行组合约束。

![[assets/figures/papers/paper_list_l29_https_openreview_net_forum_id_nIwFge9nW0/figures/008_Table_1.jpg]]
*Table 1: Performance on Compositional Image Generation, Visual Text Rendering, and Human Preference benchmarks, evaluated by task performance on test prompts, and by image quality and preference scores on DrawBench prompts. ImgRwd: ImageReward; UniRwd: UnifiedReward. UniRwd*: our evaluation results of the official checkpoints and our method with UnifiedReward. 1*

**视觉文本渲染（Visual Text Rendering）** 任务以 OCR 准确率衡量文字生成质量。DenseGRPO 取得 **0.95**，相比 Flow-GRPO 的 0.92 提升 0.03（Table 1）。文字渲染对中间步骤的细节保持要求极高，稠密奖励在此场景下的增益尤为显著。

**人类偏好对齐（Human Preference Alignment）** 是综合性最强的任务。在 PickScore 指标上，DenseGRPO 达到 **24.64**，较 Flow-GRPO 的 23.31 提升 1.33，较 Flow-GRPO+CoCA 的 23.63 亦有 1.01 的显著优势（Table 1）。在 ImageReward 上，DenseGRPO 取得 1.41，同样领先于 Flow-GRPO。这一结果说明，仅对轨迹级稀疏奖励进行优化会因反馈-贡献不匹配而限制对齐效果，而 DenseGRPO 的步骤级稠密信号从根本上解决了该瓶颈。

Figure 4 的训练曲线进一步揭示：DenseGRPO 在三个任务上的学习速度和最终收敛水平均持续优于 Flow-GRPO 和 Flow-GRPO+CoCA，尤其在人类偏好对齐任务上，优势随训练步数增加而扩大。Figure 5 的定性对比显示，DenseGRPO 在颜色准确性、文本保真度和内容对齐方面均产生更高质量的输出。

![[assets/figures/papers/paper_list_l29_https_openreview_net_forum_id_nIwFge9nW0/figures/011_Figure_4.jpg]]
*Figure 4: Comparison of learning curves. Figures (a) to (c) correspond to the tasks of compositional image generation, visual text rendering, and human preference alignment, respectively*

### 消融实验

Figure 6 系统验证了 DenseGRPO 三个关键设计的独立贡献，所有消融均以 PickScore 为评价指标。

![[assets/figures/papers/paper_list_l29_https_openreview_net_forum_id_nIwFge9nW0/figures/026_Figure_6.jpg]]
*Figure 6: Ablation studies on our critical designs. (a) Step-wise dense reward aligns with contribution, surpassing trajectory-wise sparse reward. (b) Our time-specific noise level enables a suitable exploration space. (c) Increased ODE denoising steps (n) improve dense reward accuracy, yielding superior results. The vertical axis denotes the PickScore results. The horizontal axis of (a) and (b) is training steps, while the horizontal axis of (c) denotes training time for training cost comparison*

**稠密奖励 vs. 稀疏奖励（Figure 6a）**：将 DenseGRPO 的逐步稠密奖励替换为轨迹级稀疏奖励（即仅使用终端奖励均匀应用于所有步骤），性能显著下降。这直接证实了核心瓶颈——稀疏奖励与各步骤贡献之间的不匹配会误导策略学习，而步骤级奖励增益 $\Delta R_t^i = R_{t-1}^i - R_t^i$ 能够精确量化单步贡献，提供与贡献对齐的反馈信号。

**时间步特定噪声水平 $\psi(t)$ vs. 统一噪声标量（Figure 6b）**：将校准后的时间步特定噪声水平替换为统一的标量 $a$（即 Flow-GRPO 的默认设置），训练效果明显变差。这验证了奖励感知的探索空间校准策略的必要性：不同时间步的正负奖励分布存在差异，统一噪声水平会导致探索空间不合理（如 Figure 3 所示），而自适应调整 $\psi(t)$ 能够平衡各步骤的探索空间，使 GRPO 训练更加有效。

**ODE 去噪步数 $n$（Figure 6c）**：增加 ODE 去噪步数 $n$ 可提高稠密奖励的估计精度，从而带来更好的性能表现。该结果以训练时间为横轴进行公平比较，表明在相同计算预算下，更高的奖励估计精度能更有效地指导策略优化。但需注意，$n$ 的增大也意味着额外的推理开销，实际应用中需在精度与效率之间权衡。

### 泛化性验证

Figure 9 展示了 DenseGRPO 在不同模型和分辨率上的泛化能力。在 FLUX.1-dev 模型上，DenseGRPO 的 PickScore 训练曲线始终高于 Flow-GRPO；在 SD 3.5-M 的 1024×1024 高分辨率设定下，DenseGRPO 同样保持一致的性能优势；在扩散模型（diffusion model）上的实验也证实了该方法的跨架构适用性。这表明基于 ODE 的稠密奖励估计和探索空间校准策略不依赖于特定的流匹配架构，具有较好的通用性。

![[assets/figures/papers/paper_list_l29_https_openreview_net_forum_id_nIwFge9nW0/figures/033_Figure_9.jpg]]
*Figure 9: Performance of DenseGRPO compared with Flow-GRPO on additional models: (a) FLUX.1-dex, (b) SD 3.5-M on 1024 × 1024 resolution, and (c) diffusion model*

### 局限性与失败模式

尽管 DenseGRPO 在主要指标上表现优异，但步骤级稠密奖励存在奖励黑客（reward hacking）风险。由于每个中间步骤都直接接收来自奖励模型的反馈信号，模型可能学会利用奖励模型的盲区来获取高分，而非真正提升图像质量。论文在 Figure 10 中展示了特定任务下图像质量下降的案例，提示该方法需要配合适当的正则化或更大规模、更鲁棒的奖励模型来缓解此问题。

探索空间校准策略依赖预热步骤和超参数 $\varepsilon_1$、$\varepsilon_2$（Algorithm 1），这些参数控制正负奖励数量平衡的容忍度和噪声调整步长。在不同任务或奖励模型下，最优参数可能发生变化，需要额外调参成本。该策略的自适应调整方案及其理论解释仍有待进一步研究。

## 定位与知识库关联

### 与基线方法的关系

DenseGRPO 直接建立在 **Flow-GRPO**（Liu et al., 2025）的框架之上。Flow-GRPO 首次将流匹配模型的迭代去噪过程形式化为马尔可夫决策过程（MDP），并应用组相对策略优化（GRPO）进行对齐训练。然而，Flow-GRPO 仅在整个去噪轨迹的终端生成一个稀疏奖励信号 $R(x_0^i, c)$，并将其均匀应用于所有中间步骤的优化。这种“全局反馈—局部应用”的错配构成了 DenseGRPO 的核心改进动机：**全局终端奖励无法区分各去噪步骤的细粒度贡献，导致策略学习被误导**。

**DanceGRPO**（Xue et al., 2025）同样沿用了稀疏奖励的 GRPO 范式，面临相同的反馈-贡献不匹配问题。**Flow-GRPO+CoCA**（Liao et al., 2025）则尝试通过潜在相似度对轨迹级奖励进行重新分配，但其奖励信号本质上仍是轨迹级别的，未实现真正的步骤级稠密化。

DenseGRPO 的关键突破在于将奖励信号从“轨迹级稀疏”转变为“步骤级稠密”：通过 ODE 去噪将中间潜变量 $x_t^i$ 映射为干净潜变量 $\hat{x}_{t,0}^i$，利用现成奖励模型评估其价值 $R_t^i$，再计算相邻步骤间的奖励增益 $\Delta R_t^i = R_{t-1}^i - R_t^i$ 作为逐步稠密奖励。这一设计使得每个去噪步骤都能获得与其贡献对齐的反馈信号，从根本上解决了稀疏奖励的错配问题。

### 适用边界

DenseGRPO 的设计依赖以下前提条件，超出这些边界时方法有效性可能下降：

1. **流匹配模型架构**：方法的核心组件——ODE 去噪模块和 SDE 采样器——均基于流匹配模型的确定性映射特性。虽然论文在扩散模型上展示了初步泛化结果（Figure 9c），但该方法在非流匹配架构上的适用性仍需进一步验证。

2. **现成奖励模型的可用性**：步骤级稠密奖励的估计依赖于外部奖励模型 $\mathscr{R}$ 对中间干净图像进行评估。当目标任务缺乏高质量奖励模型，或奖励模型本身存在系统性偏差时，稠密奖励的准确性将受到直接影响。

3. **计算预算约束**：ODE 去噪步数 $n$ 直接影响稠密奖励的准确性和训练成本。消融实验表明增加 $n$ 可提升性能，但相应的计算开销也随之增长（Figure 6c），需要在精度和效率之间权衡。

### 局限与开放问题

**奖励黑客风险**：步骤级稠密奖励虽然提供了更精确的反馈，但也增加了模型对奖励模型的过拟合风险。论文明确指出，在特定任务下，稠密奖励可能引发奖励黑客现象，导致图像质量下降（如图 10 所示）。如何在不依赖大规模奖励模型的情况下缓解这一问题，是 DenseGRPO 面临的核心挑战。

**探索空间校准的超参数敏感性**：探索空间校准策略（Algorithm 1）依赖超参数 $\varepsilon_1$ 和 $\varepsilon_2$ 来平衡正负奖励分布，且需要额外的预热步骤。这些超参数在不同任务中可能需要调整，其自适应调整方案和理论解释目前尚不明确。

**长时序任务的可扩展性**：当前方法在图像生成的有限去噪步骤上验证有效，但其奖励估计和探索校准机制能否有效扩展到更长时序的视频生成或多步骤推理任务，仍是一个开放问题。时序增长将显著增加 ODE 去噪的计算成本和奖励估计的累积误差。

**需要人工核验**：论文未提供会议/期刊信息，部分基线工作的引用元数据（如 SD 3.5-M 的出处）在分析中缺失，建议在正式引用时补充完整的出版信息。

## 原文 PDF

![[paperPDFs/ICLR_2026/DenseGRPO_From_Sparse_to_Dense_Reward_for_Flow_Matching_Model_Alignment.pdf]]
