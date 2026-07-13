---
title: "SARM: Stage-Aware Reward Modeling for Long Horizon Robot Manipulation"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/SARM_Stage_Aware_Reward_Modeling_for_Long_Horizon_Robot_Manipulation.pdf
project_link: https://qianzhong-chen.github.io/sarm.github.io/
code_link: null
openreview_forum_id: aemqAxScl9
aliases:
- SRB
- SARM
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "通过自然语言子任务注释自动推导任务进度标签，并训练一个双头视频奖励模型——同时预测任务阶段和细粒度进度，从而提供稳定、高分辨率的奖励信号。"
primary_logic: "将长程任务分解为语义子任务，利用数据集平均时间比例生成跨演示一致的密集进度标签，克服了帧索引标签的不稳定性，使奖励模型对演示变化和分布外场景具有鲁棒性。"
claims:
- "SARM 框架使用自然语言子任务注释自动推导任务进度标签，并联合预测任务阶段和细粒度进度，从而稳定长期操作的奖励信号。"
- "在 T 恤折叠任务上，SARM 在奖励建模中显著优于所有基线：演示 MSE 最低（0.009），真实策略展开的 ρ 最高（0.94），并成功分类 12/12 成功、11/12 部分成功和 12/12 失败案例。"
- "RA-BC 框架利用 SARM 奖励模型对演示进行加权，在困难 T 恤折叠任务上实现 67% 成功率（crumpled state），而普通 BC 为 0%。"
- "T-shirt folding reward model evaluation 上 Rollout ρ ↑ = 0.94 (SARM)"
---

# SARM: Stage-Aware Reward Modeling for Long Horizon Robot Manipulation

> [!tip] 核心洞察
> 将长程任务分解为语义子任务，利用数据集平均时间比例生成跨演示一致的密集进度标签，克服了帧索引标签的不稳定性，使奖励模型对演示变化和分布外场景具有鲁棒性。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 面向长期机器人操作的阶段感知奖励建模 |
| 英文题名 | SARM: Stage-Aware Reward Modeling for Long Horizon Robot Manipulation |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=aemqAxScl9) · [Project](https://qianzhong-chen.github.io/sarm.github.io/) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | SARM and RA-BC |
| Dataset | T-shirt folding reward model evaluation, T-shirt folding policy learning (Hard task), Dish unloading reward model evaluation |

> [!tip] 效果简介
> - T-shirt folding reward model evaluation 上，Rollout ρ ↑ 为 0.94 (SARM)，对比 0.50 (ReWiND)，变化 +0.44 (88% improvement)。
> - T-shirt folding policy learning (Hard task) 上，Success Rate 为 67% (SARM + RA-BC, 40K steps)，对比 0% (Vanilla BC on D_all, 40K steps)，变化 +67%。
> - Dish unloading reward model evaluation 上，Rollout ρ ↑ 为 0.67 (SARM)，对比 0.55 (ReWiND)，变化 +0.12。

## 概要

长期机器人操作任务（尤其是涉及可变形物体的接触丰富型任务）面临一个核心瓶颈：演示数据质量参差不齐，而传统的基于帧索引的进度标签存在严重噪声，导致现有奖励模型和模仿学习方法性能急剧下降。SARM（Stage-Aware Reward Modeling）框架针对这一问题，通过自然语言子任务注释自动推导出跨演示一致的密集进度标签，并训练一个双头视频奖励模型——同时预测离散的任务阶段和阶段内的细粒度进度，从而提供稳定、高分辨率的奖励信号。

在此基础上，RA-BC（Reward-Aligned Behavior Cloning）利用学习到的奖励模型对演示数据进行过滤和重加权，使策略训练聚焦于高质量、有实际进度的样本。在真实世界的 T 恤折叠任务上，SARM 的奖励建模显著优于所有基线：演示 MSE 低至 0.009，真实策略展开的分类评分 ρ 达到 0.94，并成功分类 12/12 成功、11/12 部分成功和 12/12 失败案例。在策略学习方面，RA-BC 结合 SARM 在困难任务（crumpled 初始状态）上实现 67% 成功率，而普通行为克隆为 0%。在餐具卸载任务上，SARM 同样以 0.67 的 Rollout ρ 优于 ReWiND 的 0.55，验证了方法的跨任务泛化能力。

方法谱系与知识库定位上，SARM 的奖励建模基线包括 **GVL**（Ma et al., 2024b）、**VLC**（Alakuijala et al., 2024）、**LIV**（Ma et al., 2023）、**REDS**（Kim et al., 2025）、**VICtoR**（Hung et al., 2024）和 **ReWiND**（Zhang et al., 2025），其中 ReWiND 同时作为 RA-BC 的策略学习骨干。SARM 在三个关键设计槽位上做出改进：进度标签方案从帧索引插值改为基于子任务注释的数据集级平均时间比例插值；模型架构从单进度回归头改为阶段估计与子任务进度估计的双头结构；策略训练目标从均匀加权的行为克隆改为基于进度增量和在线统计量的奖励对齐加权。



长期机器人操作任务——尤其是涉及可变形物体（如衣物折叠）的接触丰富场景——对现有模仿学习和奖励建模方法构成了根本性挑战。这类任务的核心瓶颈在于**演示质量不一致**：即使是专家演示，其执行速度、路径选择和中间状态也存在显著差异，导致基于帧索引（frame-index）的进度标签产生严重噪声。现有方法（如 **ReWiND**，Zhang et al., 2025）通过帧数线性插值分配进度值，假设所有演示在时间上均匀推进，这一假设在长程操作中几乎从不成立。

噪声进度标签的后果是双重的：其一，奖励模型学习到的进度信号不稳定，难以泛化到分布外（out-of-distribution）的策略展开；其二，行为克隆（Behavior Cloning, BC）在包含次优片段的多样化数据集上训练时，无法区分高质量与低质量演示，导致策略性能退化。在 T 恤折叠任务中，普通 BC 在 crumpled 初始状态下成功率为 0%，直接反映了这一困境。

现有奖励建模方法——包括 **GVL**（Ma et al., 2024b）、**VLC**（Alakuijala et al., 2024）、**LIV**（Ma et al., 2023）、**REDS**（Kim et al., 2025）和 **VICtoR**（Hung et al., 2024）——虽然在特定基准上取得了进展，但普遍依赖单头回归架构预测连续进度，缺乏对任务语义结构的显式建模。这使它们难以捕捉长程任务中不同阶段之间的质变边界，在阶段转换处产生不连续的奖励信号。

本文的动机源于一个关键洞察：**将长程任务分解为语义子任务，并利用数据集级别的平均时间比例生成跨演示一致的密集进度标签，可以克服帧索引标签的不稳定性**。通过自然语言子任务注释自动推导进度标签，奖励模型能够学习到对演示变化和分布外场景具有鲁棒性的进度表征。在此基础上，利用奖励模型对演示进行加权，使策略训练聚焦于实际取得进展的片段，从而在多样化数据中提取有效学习信号。



## 核心方法与创新机理

SARM 框架针对长期机器人操作中的奖励建模，提出了三项相互耦合的关键创新，分别从**进度标签生成**、**模型架构**和**策略训练目标**三个层面改变了现有范式。

### 创新一：基于子任务注释的进度标签生成（Progress Labeling Scheme）

**瓶颈**：现有方法（如 **ReWiND**（Zhang et al., 2025））采用基于帧索引的线性插值方案——将任务进度视为帧数的线性函数。在长期、接触丰富的操作任务（尤其是 T 恤折叠这类可变形物体操作）中，演示的长度和质量高度不一致，帧索引标签存在严重噪声，导致奖励模型在跨演示泛化和分布外场景中性能急剧下降。

**方案**：SARM 利用自然语言子任务注释自动推导任务进度标签，核心步骤为：

1. **数据集级先验比例计算**：对每个子任务 $k$，在所有 $M$ 条演示轨迹上计算其平均时间占比：
   $$\bar{\alpha}_k = \frac{1}{M} \sum_{i=1}^{M} \frac{L_{i,k}}{T_i}$$
   其中 $L_{i,k}$ 为轨迹 $i$ 中子任务 $k$ 的帧数，$T_i$ 为轨迹总帧数。这一先验反映了任务的自然节奏（例如 T 恤折叠中“展平”占 26%，“折叠”占 55%），而非单条演示的偶然波动。

2. **帧级归一化进度目标**：对于帧 $t$，其进度标签由累积先验与子任务内线性插值组合而成：
   $$y_t = P_{k-1} + \bar{\alpha}_k \tau_t$$
   其中 $P_{k-1}$ 为前 $k-1$ 个子任务的累积先验比例，$\tau_t$ 为帧 $t$ 在当前子任务内的归一化位置。

**效果**：该方案使进度标签在跨演示间保持一致，不受单条演示长度或速度变化的影响。Figure 3 的可视化对比显示，SARM 的预测进度比 ReWiND 更准确且校准更好。这一标签生成策略是后续双头架构和策略加权的基础。

### 创新二：阶段感知的双头奖励模型架构（Reward Model Architecture）

**瓶颈**：现有奖励模型（如 ReWiND）采用单头回归架构，直接预测全局进度值。这种扁平结构难以捕捉长程任务的层次化语义结构，且对演示中的局部停滞或回退敏感。

**方案**：SARM 采用**双头架构**，将奖励预测分解为两个层次（Figure 2）：

1. **阶段估计器（Stage Estimator）**：通过交叉熵损失预测当前帧所属的离散任务阶段 $\hat{S}_{1:N}$，提供粗粒度的语义锚定。
2. **子任务进度估计器（Subtask Estimator）**：以阶段预测为条件，通过 MSE 损失预测当前阶段内的细粒度进度 $\hat{\tau}_{1:N}$。

最终归一化进度由两者组合：
$$\hat{y}_{1:N} = \hat{P}_{k-1,1:N} + \bar{\alpha}_{k,1:N} \hat{\tau}_{1:N}$$

输入管线使用冻结的 CLIP 编码器提取视觉特征，仅对首帧施加显式位置偏置，经投影后送入 Transformer 编码器。两个估计器共享 Transformer 主干，仅在头部进行任务特化。

**效果**：阶段预测为细粒度进度估计提供了稳定的语义上下文，使模型对演示中的局部变化具有鲁棒性。消融实验（Table 5）表明，将 Transformer 层数从 4 增至 8 时，Rollout $\rho$ 从 0.72 提升至 0.94；进一步增至 12 层获得有限增益（0.88），说明 8 层已能充分建模任务的层次化结构。

### 创新三：奖励对齐的行为克隆（RA-BC）

**瓶颈**：普通行为克隆（Vanilla BC）对所有演示样本赋予均等权重，在包含次优轨迹的多样化数据集中，噪声样本会严重损害策略性能。在困难 T 恤折叠任务（crumpled state）上，普通 BC 的成功率为 0%。

**方案**：RA-BC 将 BC 的均匀先验替换为**奖励对齐加权**，核心机制为：

1. **进度增量计算**：利用训练好的 SARM 奖励模型 $\phi$，计算时间窗口 $\Delta$ 内的进度增量：
   $$\widehat{r}_i = \phi(o_i^{t+\Delta}) - \phi(o_i^t)$$

2. **在线统计校准**：维护进度增量的在线运行均值 $\mu$ 和标准差 $\sigma$，将原始增量映射为 $[0,1]$ 软权重，无需固定启发式阈值：
   $$\tilde{w}_i = \mathrm{clip}\left(\frac{\widehat{r}_i - (\mu - 2\sigma)}{4\sigma + \epsilon}, 0, 1\right)$$

3. **先验覆盖**：引入轻量先验阈值 $\kappa > 0$，对明显好/坏的样本施加决定性权重。

4. **加权损失**：最终训练目标为：
   $$\mathcal{L}_{\mathrm{RA-BC}}(\theta) = \frac{\sum_{i=1}^{N} w_i \ell(\pi_\theta(o_i), a_i)}{\sum_{i=1}^{N} w_i + \varepsilon}$$

**效果**：RA-BC 是 Eq. 5 的直接替换，通过归一化保持训练稳定性。在困难 T 恤折叠任务上，SARM + RA-BC 在 40K 步达到 67% 成功率，而普通 BC 为 0%（Table 3）。值得注意的是，RA-BC 的性能高度依赖奖励模型质量——使用 ReWiND 奖励模型的 RA-BC 在中等任务上仅达 50%，远低于 SARM 的 83%，说明阶段感知奖励信号对策略学习的赋能作用。



![[assets/figures/papers/paper_list_l45_https_openreview_net_forum_id_aemqAxScl9/figures/001_Figure_1.jpg]]
*Figure 1: Overview of our method’s framework for (a) data processing, (b) reward model training, and (c) policy training with reward signals. $\mathcal { D } _ { \mathrm { a n n o } }$ denotes the annotated dataset used for training the reward model, with examples shown in Fig. 5 and Fig. 6. $\mathcal { D } _ { \mathrm { d i v e r s e } }$ refers to a diverse expert dataset without annotations, which contains many suboptimal trajectories

![[assets/figures/papers/paper_list_l45_https_openreview_net_forum_id_aemqAxScl9/figures/002_Figure_2.jpg]]
*Figure 2: Overview of SARM, stage-aware reward modeling. Left: SARM overview, which includes both a stage estimator and subtask estimator. First the task stage is predicted from the observations. This prediction is additionally passed into the subtask estimator which predicts a scale value of the progress within the stage. Right: An overview of the estimator architecture which is replicated for both the stage estimator and the subtask estimator*

SARM 方法体系由三个紧密耦合的模块构成，形成“数据标注→奖励建模→策略训练”的完整闭环（Figure 1）。核心设计逻辑在于：**用自然语言子任务注释替代基于帧索引的进度标签，从根本上消除演示长度不一致引入的标签噪声**，进而训练一个双头视频奖励模型，为下游策略学习提供稳定、高分辨率的奖励信号。

### 数据预处理：从子任务注释到密集进度标签

该模块的输入是带有自然语言子任务边界注释的专家演示数据集 $\mathcal{D}_{\text{anno}}$（Figure 5、Figure 6 分别展示了稀疏标注与密集标注的示例）。处理流程如下：

1. **计算数据集级先验比例**：对每个子任务 $k$，统计其在所有 $M$ 条演示中的平均时间占比：
   $$\bar{\alpha}_k = \frac{1}{M} \sum_{i=1}^{M} \frac{L_{i,k}}{T_i}$$
   其中 $L_{i,k}$ 为子任务 $k$ 在演示 $i$ 中的帧数，$T_i$ 为演示 $i$ 的总帧数。这一先验平滑了单条演示的时序波动，使跨演示的进度标签具有一致性。

2. **生成帧级归一化进度目标**：对任意帧 $t$，其进度标签由累积先验与子任务内线性插值合成：
   $$y_t = P_{k-1} + \bar{\alpha}_k \tau_t$$
   其中 $P_{k-1}$ 为前 $k-1$ 个子任务的累积先验比例，$\tau_t$ 为帧 $t$ 在当前子任务内的归一化位置。这一方案使进度标签在子任务边界处精确对齐，在子任务内部平滑递增，从根本上规避了帧索引标签因演示速度差异导致的错位问题。

### 奖励模型架构：双头阶段感知预测

SARM 奖励模型采用**共享视觉主干 + 双预测头**的架构（Figure 2）：

- **输入管线**：一段 RGB 帧序列首先通过冻结的 CLIP 编码器提取视觉特征，与关节状态拼接后投影到统一维度。仅对首帧施加显式位置偏置，随后由 Transformer 编码器进行时序建模。

- **阶段估计器（Stage Estimator）**：以交叉熵损失训练，将当前观测分类到 $K$ 个离散任务阶段之一：
  $$\hat{S}_{1:N} = \arg\max_{i \in \{1,\dots,k\}} \Pi_{1:N,i}$$

- **子任务进度估计器（Subtask Progress Estimator）**：以 MSE 损失训练，在阶段预测结果的条件作用下，估计当前阶段内的细粒度进度 $\hat{\tau}$。最终归一化进度由两者合成：
  $$\hat{y}_{1:N} = \hat{P}_{k-1,1:N} + \bar{\alpha}_{k,1:N} \hat{\tau}_{1:N}$$

这种“先定阶段、再估进度”的分层设计，使模型能够将长程任务分解为语义上有意义的子单元，从而在接触丰富、演示质量参差不齐的场景下提供更稳定的奖励信号。消融实验表明，回放增强（Rewind augmentation）对模型泛化至真实策略展开至关重要——移除该增强后，Rollout $\rho$ 从 0.94 骤降至 0.67（Table 1）。

### 策略训练：RA-BC 奖励对齐行为克隆

RA-BC 模块利用训练好的 SARM 奖励模型，对多样化演示数据集 $\mathcal{D}_{\text{diverse}}$ 中的样本进行软性筛选与重加权，替代标准行为克隆中的均匀先验：

1. **进度增量计算**：对每个训练样本，计算时间窗口 $\Delta$ 内的进度变化：
   $$\widehat{r}_i = \phi(o_i^{t+\Delta}) - \phi(o_i^t)$$

2. **在线统计校准**：维护进度增量的在线均值 $\mu$ 和标准差 $\sigma$，将原始增量映射为 $[0,1]$ 软权重：
   $$\tilde{w}_i = \text{clip}\left(\frac{\widehat{r}_i - (\mu - 2\sigma)}{4\sigma + \epsilon}, 0, 1\right)$$

3. **先验覆盖**：引入阈值 $\kappa$，对权重施加轻量级先验知识，使明显优质或劣质的样本获得决定性权重。

4. **加权损失**：最终训练目标为加权行为克隆损失：
   $$\mathcal{L}_{\text{RA-BC}}(\theta) = \frac{\sum_{i=1}^{N} w_i \ell(\pi_\theta(o_i), a_i)}{\sum_{i=1}^{N} w_i + \varepsilon}$$

该设计使 RA-BC 成为一个即插即用的替代方案：它不改变底层策略架构，仅通过奖励信号自动识别并强调真正推进任务进度的演示片段，同时抑制停滞或回退的噪声数据。



### 数据预处理：子任务注释驱动的进度标签生成

长期操作任务中，基于帧索引的线性进度标签对演示长度和速度变化高度敏感，是现有奖励模型性能瓶颈的核心来源。SARM 通过自然语言子任务注释自动推导跨演示一致的密集进度标签，从根本上解决了这一问题。

给定包含 $M$ 条轨迹的注释数据集，每条轨迹 $i$ 被划分为 $K$ 个子任务，第 $k$ 个子任务的长度为 $L_{i,k}$，轨迹总长度为 $T_i$。首先计算每个子任务在整个数据集上的平均时间比例作为先验：

$$
\bar{\alpha}_k = \frac{1}{M} \sum_{i=1}^{M} \frac{L_{i,k}}{T_i}
$$

该先验比例 $\bar{\alpha}_k$ 反映了子任务 $k$ 在所有演示中平均占据的时间份额，有效平滑了个体演示的节奏差异。

对于轨迹内的第 $t$ 帧，其归一化进度目标由累积先验与子任务内线性插值两部分组成：

$$
y_t = P_{k-1} + \bar{\alpha}_k \tau_t
$$

其中 $P_{k-1} = \sum_{j=1}^{k-1} \bar{\alpha}_j$ 是前 $k-1$ 个子任务的累积先验进度，$\tau_t \in [0, 1]$ 是当前帧在子任务 $k$ 内的相对位置（通过帧索引线性归一化）。该方案确保不同演示中同一语义阶段的帧获得相近的进度标签，从根本上克服了帧索引标签的不稳定性。

### 双头奖励模型架构

SARM 采用共享骨干网络与两个任务专用头部的双头架构，联合预测离散任务阶段和阶段内细粒度进度。

**阶段估计器**接收观测序列 $o_{1:N}$（包括 RGB 帧和可选的关节状态），通过冻结的 CLIP 编码器提取视觉特征，经投影后送入 Transformer 编码器，最终输出 $K$ 类 softmax 概率 $\Pi_{1:N} \in \mathbb{R}^{K}$。阶段预测取最大概率类别：

$$
\hat{S}_{1:N} = \arg\max_{i \in \{1,\dots,K\}} \Pi_{1:N,i}
$$

阶段估计器使用交叉熵损失训练，为后续的细粒度进度预测提供高层语义锚定。

**子任务进度估计器**共享同一骨干网络，但额外接收阶段预测结果作为条件输入。它输出当前阶段内的连续进度值 $\hat{\tau}_{1:N} \in [0, 1]$，训练目标为 MSE 损失。最终归一化进度由阶段累积先验与子任务内进度组合得到：

$$
\hat{y}_{1:N} = \hat{P}_{k-1,1:N} + \bar{\alpha}_{k,1:N} \hat{\tau}_{1:N}
$$

这种“先阶段后进度”的级联设计使模型能够先建立粗粒度的任务理解，再聚焦于阶段内的精细进度估计，显著提升了长期任务中奖励信号的稳定性和分辨率。

### RA-BC：奖励对齐的行为克隆

RA-BC 将标准行为克隆中的均匀先验替换为基于奖励模型的加权方案，使策略训练聚焦于真正推进任务的高质量演示片段。

对于每个训练样本 $(o_i, a_i)$，使用奖励模型 $\phi$ 计算其进度增量：

$$
\widehat{r}_i = \phi(o_i^{t+\Delta}) - \phi(o_i^t)
$$

其中 $\Delta$ 为时间窗口间隔，$\widehat{r}_i$ 反映了该样本在任务进度上的推进程度。

为消除固定超参的依赖，RA-BC 维护进度增量的在线运行统计量（均值 $\mu$ 和标准差 $\sigma$），并通过软映射将原始增量转换为 $[0,1]$ 范围内的权重：

$$
\tilde{w}_i = \mathrm{clip}\left(\frac{\widehat{r}_i - (\mu - 2\sigma)}{4\sigma + \epsilon}, 0, 1\right)
$$

该映射使权重自适应于当前数据分布：进度增量显著高于平均水平的样本获得接近 1 的权重，而低于平均水平的样本权重趋近于 0。

此外，RA-BC 引入轻量级先验知识：当 $|\widehat{r}_i| < \kappa$ 时强制设为零权重，使模型对无明显进展的噪声片段具有明确的拒绝能力。最终权重经归一化后用于加权行为克隆损失：

$$
\mathcal{L}_{\mathrm{RA-BC}}(\theta) = \frac{\sum_{i=1}^{N} w_i \ell(\pi_\theta(o_i), a_i)}{\sum_{i=1}^{N} w_i + \varepsilon}
$$

该目标函数可无缝替换标准 BC 的均匀加权方案，在保持训练稳定性的同时，软性地过滤低质量数据。



## 实验与关键发现

### 核心瓶颈与评估逻辑

长期接触丰富的操作任务（尤其是可变形物体折叠）面临双重挑战：演示质量不一致，且基于帧索引的进度标签存在严重噪声。这导致现有奖励模型在真实策略展开中给出过于乐观或错误的进度估计，进而误导策略学习。SARM 通过自然语言子任务注释自动推导任务进度标签，并训练一个双头视频奖励模型——同时预测任务阶段和细粒度进度——来提供稳定、高分辨率的奖励信号。评估围绕两个层次展开：(1) 奖励模型本身的准确性和鲁棒性，(2) 奖励信号对下游策略学习的实际增益。

---

### 奖励模型评估

**T 恤折叠任务（Table 1）** 是核心 benchmark。SARM 在验证集演示上取得最低的单步 MSE（Demo $\mathcal{L}$ = 0.009），相比最强基线 ReWiND（0.013）降低约 31%。更关键的是在真实策略展开上的表现：SARM 的 Rollout $\rho$ 达到 0.94，而 ReWiND 仅为 0.50，提升 88%。分类细粒度显示 SARM 正确识别了 12/12 成功案例（SE）、11/12 部分成功案例（PSE）和 12/12 失败案例（FE），表明其奖励信号在分布外策略轨迹上仍保持校准。


![[assets/figures/papers/paper_list_l45_https_openreview_net_forum_id_aemqAxScl9/figures/004_Table_1.jpg]]
*Table 1: Evaluation of reward models. “Demo $\mathcal { L } ^ { \mathfrak { s } }$ denotes the single-step MSE of reward models on the validation set. All models are evaluated on 70 trajectories (50 from $\mathcal { D } _ { \mathrm { s p a r s e } }$ and 20 from $\mathcal { D } _ { \mathrm { d e n s e } }$ ) . , where both ground-truth progress and model predictions are normalized to the [0, 1] range. The twoscheme models (last two columns) are evaluated in “sparse mode.” “Rollout $\rho ^ { \dagger }$ reports performance on real policy rollouts. Visualization examples of reward model predictions on both demonstration data and policy rollouts are provided in Appendix A.5

**餐具卸载任务（Table 2）** 进一步验证跨任务泛化。SARM 的 Rollout $\rho$ 为 0.67，优于 ReWiND 的 0.55，且 Demo $\mathcal{L}$ 为 0.013，相对最强基线提升超过 50%。分类方面，SARM 达到 SE 10/12、PSE 9/12、FE 11/12，说明阶段感知建模在非折叠类长程任务中同样有效。

**关键消融发现：**

- **回放增强（w/o R）至关重要**：移除回放增强后，Rollout $\rho$ 从 0.94 骤降至 0.67（Table 1），模型在真实策略展开中变得过于乐观。这证实了回放增强是奖励模型泛化到真实策略的必要条件。
- **模型规模**：将 transformer 层数从 4 增至 8，Rollout $\rho$ 从 0.72 提高到 0.94；进一步增至 12 层获得有限增益（0.88，Table 5），表明 8 层在性能与效率间取得最佳平衡。
- **时序覆盖**：8 个观察步数和 30 帧间隔在时序覆盖与计算效率间取得最优（Table 8、Table 9）。
- **关节状态**：仅靠视觉输入的变体仍取得强性能，加入关节状态可小幅提升估计精度（Table 6），但效果有限。
- **腕部相机**：使用与否几乎无差异（Table 7），表明外部视角已提供足够信息。


![[assets/figures/papers/paper_list_l45_https_openreview_net_forum_id_aemqAxScl9/figures/022_Table_5.jpg]]
*Table 5: Scalability analysis of reward model on T-shirt folding task*

---

### 策略学习评估

**RA-BC 框架** 利用 SARM 奖励模型对演示进行加权，在 T 恤折叠任务上展现出显著增益（Table 3）：


![[assets/figures/papers/paper_list_l45_https_openreview_net_forum_id_aemqAxScl9/figures/006_Table_3.jpg]]
*Table 3: Success rates (SR) of T-shirt folding policies at 20K and 40K training steps. Each block reports the overall SR for each task. Detailed per-color results are provided in Table A.7*

- **简单任务**：所有方法均达到 12/12 成功率，说明基础操作不存在困难。
- **中等任务（flattened state）**：SARM + RA-BC 在 40K 步达到 83%（10/12），远超 Vanilla BC on D_all 的 8%（1/12）和 BC-2min 的 58%（7/12）。RA-BC-ReWiND 为 50%（6/12），进一步证明 SARM 奖励质量对策略学习的关键作用。
- **困难任务（crumpled state）**：SARM + RA-BC 在 40K 步达到 67%（8/12），而 Vanilla BC on D_all 为 0%（0/12），BC-2min 也为 0%。这是最具挑战性的场景——从揉皱状态开始折叠——SARM 是唯一能可靠完成该任务的方法。

**因果链条**：困难任务中 D_all 包含大量低质量演示，均匀加权的 BC 被噪声淹没；BC-2min 通过人工筛选改善数据质量，但在困难初始状态下仍失效。SARM 的奖励模型自动识别进度良好的演示片段并赋予高权重，从而在无需人工筛选的情况下实现鲁棒学习。

---

### 进度标签质量分析

**Figure 3** 可视化对比了 SARM 与 ReWiND 在 T 恤折叠演示上的进度预测。SARM 提供的估计更准确且校准更好，尤其在任务阶段转换处避免了 ReWiND 常见的突变和平台期。这归因于 SARM 使用数据集级子任务时间比例（Table 4）生成跨演示一致的密集进度标签，克服了帧索引标签在不同速度演示间的不稳定性。


![[assets/figures/papers/paper_list_l45_https_openreview_net_forum_id_aemqAxScl9/figures/003_Figure_3.jpg]]
*Figure 3: A visualization of the predicted task progress for T-shirt folding demonstrations. Compared with ReWiND, SARM provides more accurate and calibrated estimates*

**Table 4** 揭示了两类数据集的子任务结构差异：稀疏标注数据集（5 个子任务）中折叠操作占 55%，密集标注数据集（8 个子任务）将折叠拆分为更细粒度操作，其中展平占 26%。SARM 的标签生成机制能自动适应这种粒度差异。

---

### 证据强度总结

| 声明 | 证据强度 | 关键锚点 |
|------|---------|---------|
| SARM 奖励模型显著优于所有基线 | 强 | Table 1: Rollout $\rho$ 0.94 vs 0.50 (ReWiND)；Table 2: $\rho$ 0.67 vs 0.55 |
| RA-BC 在困难折叠任务上实现 67% 成功率 | 强 | Table 3: Hard task 40K, SARM 8/12 vs D_all 0/12 |
| 回放增强是泛化的必要条件 | 强 | Table 1: w/o R 使 $\rho$ 从 0.94 降至 0.67 |
| 阶段感知双头架构优于单头回归 | 中 | 通过 ReWiND 对比间接支持；无直接架构消融 |
| 关节状态提供有限增益 | 中 | Table 6：视觉-only 变体仍强，需进一步验证 |

**需手动验证的点**：论文未提供直接的双头 vs 单头架构消融实验，阶段感知的优势主要通过 ReWiND 等单头基线的性能差距间接体现。若需严格归因，建议补充架构对比实验。



## 定位与知识库关联

### 核心瓶颈与设计动机

长期机器人操作任务（尤其是涉及可变形物体的T恤折叠）面临双重挑战：**演示质量不一致**与**任务进度标签噪声**。传统方法依赖帧索引进行线性进度插值（如ReWiND），但不同演示的时序节奏差异巨大——例如，某些演示者可能快速完成抓取但缓慢执行折叠，帧索引标签因此产生严重偏差，导致奖励模型在分布外策略展开中给出错误信号。SARM的核心洞察在于：**通过自然语言子任务注释自动推导跨演示一致的密集进度标签**，将长程任务分解为语义子任务，并利用数据集级平均时间比例进行插值，从而克服帧索引标签的不稳定性。

### 方法谱系与基线对比

SARM处于**视频奖励建模**与**模仿学习**的交叉领域，其直接对话的基线包括：

- **ReWiND**（Zhang et al., 2025）：作为RA-BC的backbone基线，ReWiND采用帧索引线性插值生成进度标签，使用单一进度回归头。SARM将其进度标注方案替换为子任务注释推导的标签（式1-2），并将架构升级为双头（阶段估计器+子任务估计器），在T恤折叠任务上将Rollout ρ从0.50提升至0.94（+88%）。
- **GVL**（Ma et al., 2024b）、**VLC**（Alakuijala et al., 2024）、**LIV**（Ma et al., 2023）、**REDS**（Kim et al., 2025）、**VICtoR**（Hung et al., 2024）：这些基线奖励模型在相同规模的Transformer编码器和相同训练数据下评估，SARM在演示MSE和真实策略展开分类评分上均显著领先（Table 1）。
- **Vanilla Behavior Cloning**：作为策略学习基线，在困难T恤折叠任务（crumpled state）上成功率为0%，而SARM+RA-BC达到67%（Table 3）。

### 关键设计变更与因果机制

SARM对基线方法的三个关键槽位进行了系统性改进：

| 设计槽位 | 基线方案 | SARM方案 | 因果作用 |
|---------|---------|---------|---------|
| 进度标注方案 | 帧索引线性插值（ReWiND） | 子任务注释推导：计算数据集级平均时间比例，子任务内线性插值（式1-2） | 消除演示间时序差异噪声，提供跨演示一致的密集标签 |
| 奖励模型架构 | 单一进度回归头（ReWiND） | 双头：阶段估计器（交叉熵）+ 子任务估计器（MSE），子任务估计以阶段预测为条件 | 解耦高层阶段识别与细粒度进度估计，提升泛化能力 |
| 策略训练目标 | 均匀加权行为克隆 | RA-BC：基于进度增量的奖励对齐加权，配合在线运行统计和先验阈值（式6-9） | 自动过滤低质量/非进展演示，保留训练稳定性 |

**回放增强（Rewind augmentation）** 被证明是关键组件：移除后Rollout ρ从0.94骤降至0.67（Table 1），模型在真实策略展开中变得过于乐观，表明该增强对于从稀疏/密集标注数据中学习鲁棒的奖励模型必不可少。

### 适用边界与证据强度

**强证据支撑的结论**：
- T恤折叠任务上，SARM在奖励建模中显著优于所有基线：演示MSE最低（0.009），Rollout ρ最高（0.94），成功分类12/12成功、11/12部分成功和12/12失败案例（Table 1，置信度0.98）。
- RA-BC框架在困难T恤折叠任务上实现67%成功率（crumpled state），而普通BC为0%（Table 3，置信度0.99）。
- 餐具卸载任务上，SARM的Rollout ρ为0.67，相比ReWiND的0.55提升约22%（Table 2，置信度0.97）。

**需要手动验证的边界**：
- 论文未明确讨论SARM在非操作任务（如导航）或非可变形物体上的泛化性，其子任务注释方案的有效性依赖于任务具有清晰的语义阶段分解。
- 消融实验显示仅靠视觉输入即可取得较强性能，加入关节状态仅小幅提升（Table 6，置信度0.85），但该结论可能受限于特定机器人平台和任务。
- Transformer层数从8增至12层时性能反而下降（Rollout ρ从0.94降至0.88，Table 5），暗示模型容量与数据规模之间存在未充分探索的平衡点。

### 局限与开放问题

论文本身未明确列出局限性，但从实验设计和结果中可推断以下潜在边界：

1. **注释依赖性**：SARM的进度标签生成依赖于自然语言子任务注释，虽然相比逐帧标注成本更低，但对于缺乏清晰子任务边界的任务（如连续运动技能）可能难以应用。
2. **数据集级先验的静态性**：平均时间比例$\bar{\alpha}_k$在数据集级别固定计算（式1），若测试场景的任务节奏与训练集显著不同，进度标签可能出现系统性偏差。
3. **RA-BC的在线统计敏感性**：权重校准依赖于运行统计量$\mu$和$\sigma$（式8），在训练初期样本量不足时可能导致不稳定的权重分配。
4. **多任务扩展性**：论文在两个任务上验证，但子任务注释方案和阶段估计器的扩展性（如任务数量增加时阶段分类精度的退化）未经充分测试。

**开放问题**：
- 能否通过弱监督或自监督方式自动发现子任务结构，进一步降低注释成本？
- 阶段估计器的预测置信度能否用于在线检测分布外场景并触发安全回退策略？
- RA-BC的加权机制是否可与其他策略优化方法（如RL微调）结合，形成更完整的训练pipeline？



## 原文 PDF

![[paperPDFs/ICLR_2026/SARM_Stage_Aware_Reward_Modeling_for_Long_Horizon_Robot_Manipulation.pdf]]
